// navfix.c - A* PointGraph waypoints + missing AI markers for the hidden map.
// 2026-11-15: exit gate + main-thread il2cpp; spawn node coverage; runtime ghost guard areas.
#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>
#include "cfg.h"

typedef void* P;
typedef struct { float x, y, z; } V3;

/* shared quit gate: set from WndProc / DllMain, polled by every worker thread */
volatile LONG g_appQuit = 0;

static HMODULE g_ga;
static char g_log[MAX_PATH];
static int g_ready;

static void nlog(const char* fmt, ...) {
  FILE* f = fopen(g_log, "a");
  if (!f) return;
  SYSTEMTIME st; GetLocalTime(&st);
  fprintf(f, "%04d-%02d-%02d %02d:%02d:%02d [nav] ", st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond);
  va_list ap; va_start(ap, fmt); vfprintf(f, fmt, ap); va_end(ap);
  fprintf(f, "\n"); fclose(f);
}

static P (*i_domain_get)(void);
static P (*i_domain_get_assemblies)(P,int*);
static P (*i_assembly_get_image)(P);
static const char* (*i_image_get_name)(P);
static P (*i_class_from_name)(P,const char*,const char*);
static P (*i_class_get_field_from_name)(P,const char*);
static void (*i_field_static_get_value)(P,void*);
static void (*i_wbarrier)(P,P,P);
static P (*i_object_new)(P);
static P (*i_string_new)(const char*);
static P (*i_thread_attach)(P);
static const char* (*i_class_get_name)(P);
static P (*i_class_get_type)(P);
static P (*i_type_get_object)(P);
static P (*i_class_get_parent)(P);
static P (*i_class_get_method_from_name)(P,const char*,int);
static P (*i_runtime_invoke)(P,P,void**,void**);
static P (*i_field_get_type)(P);
static P (*i_class_from_il2cpp_type)(P);
static P (*i_array_new)(P,unsigned int);
static P (*i_class_get_element_class)(P);
static void (*i_field_static_set_value)(P,void*);
static P (*i_gchandle_new)(P,unsigned char);
static void (*i_gchandle_free)(P);

#define RVA(x) ((void*)((char*)g_ga + (unsigned)(x)))

typedef unsigned char (*raycast_t)(V3, V3, void*, float, int, void*);
typedef void (*ctor_str_t)(P, P, void*);
typedef P    (*get_tr_t)(P, void*);
typedef void (*set_pos_t)(P, V3, void*);
typedef void (*set_parent_t)(P, P, unsigned char, void*);
typedef void (*set_active_t)(P, unsigned char, void*);
typedef void (*scan_t)(P, void*);
typedef P    (*addcomp_t)(P, P, void*);

static P g_goCls;
static P g_astarCls;
static P g_crouchCls;
static P g_areaCls;
static P g_posCls;
static P g_vec3Cls;
static P g_mmCls;
static P g_mmInstField;
static P g_listCls;
static P g_listCtor;
static P g_listAdd;
static P g_botCls;
static P g_stopField;
static int g_stopHeld;

static P rptr(P o, int off) { return *(P*)((char*)o + off); }
/* UnityEngine.Object.m_CachedPtr; 0 means the native object was destroyed. */
static int n_live(P o) { return o && *(P*)((char*)o + 0x8) != 0; }
static void wfield(P o, int off, P v) {
  if (i_wbarrier) i_wbarrier(o, (char*)o + off, v);
  *(P*)((char*)o + off) = v;
}

/* Keep bots frozen while the graph is being rebuilt: bots that update against an
 * empty graph throw NRE every frame (the 1000+ Bot.Update lines in Player.log). */
static void hold_bots(int on) {
  if (!g_stopField || !i_field_static_set_value) return;
  if (on) {
    char cur = 0;
    i_field_static_get_value(g_stopField, &cur);
    if (!cur) { char one = 1; i_field_static_set_value(g_stopField, &one); g_stopHeld = 1; }
  } else if (g_stopHeld) {
    char zero = 0;
    i_field_static_set_value(g_stopField, &zero);
    g_stopHeld = 0;
  }
}

static P find_image(const char* name) {
  int n = 0;
  P arr = i_domain_get_assemblies(i_domain_get(), &n);
  if (!arr) return 0;
  for (int i = 0; i < n; i++) {
    P asm_ = *(P*)((char*)arr + 0x10 + i*4);
    P img;
    if (!asm_) break;
    img = i_assembly_get_image(asm_);
    if (img && strcmp(i_image_get_name(img), name) == 0) return img;
  }
  return 0;
}

static P astar_active(void) {
  if (!g_astarCls) return 0;
  static P f = 0;
  if (!f) f = i_class_get_field_from_name(g_astarCls, "active");
  if (!f) return 0;
  P v = 0;
  i_field_static_get_value(f, &v);
  return n_live(v) ? v : 0;
}

static P point_graph(P astar) {
  if (!n_live(astar)) return 0;
  P data = *(P*)((char*)astar + 0x10);
  if (!data) return 0;
  P graphs = *(P*)((char*)data + 0x20);
  if (!graphs) return 0;
  int n = *(int*)((char*)graphs + 0xC);
  P pg = 0;
  for (int i = 0; i < n; i++) {
    P g = *(P*)((char*)graphs + 0x10 + i*4);
    if (!g) continue;
    P k = *(P*)g;
    const char* cn = k ? i_class_get_name(k) : 0;
    if (cn && strcmp(cn, "PointGraph") == 0) pg = g;
  }
  return pg;
}

/* 诊断：把 AstarPath 里每一张图都打出来（类型名 + 关键字段），
 * 用来确认“真实的路点图”到底是哪一张、是不是 PointGraph。 */
void navfix_diag_graphs(void) {
  P a = astar_active();
  if (!a) { nlog("diag: no AstarPath.active"); return; }
  P data = *(P*)((char*)a + 0x10);
  if (!data) { nlog("diag: AstarPath.data null"); return; }
  P graphs = *(P*)((char*)data + 0x20);
  int n = graphs ? *(int*)((char*)graphs + 0xC) : -1;
  nlog("diag: graphs=%d", n);
  for (int i = 0; i < n && i < 10; i++) {
    P g = *(P*)((char*)graphs + 0x10 + i * 4);
    if (!g) { nlog("diag:  [%d] null", i); continue; }
    P k = *(P*)g;
    const char* cn = k ? i_class_get_name(k) : 0;
    nlog("diag:  [%d] %-22s +E8=%p +EC=%-7d +C0=%-7d +D0=%d",
         i, cn ? cn : "?",
         *(P*)((char*)g + 0xE8), *(int*)((char*)g + 0xEC),
         *(int*)((char*)g + 0xC0), *(unsigned char*)((char*)g + 0xD0));
    if (cn && strstr(cn, "NavMesh")) {
      P tiles = *(P*)((char*)g + 0xD0);
      int ntile = tiles ? *(int*)((char*)tiles + 0xC) : 0;
      int nv = 0, ntr = 0;
      if (ntile > 0) {
        P t0 = *(P*)((char*)tiles + 0x10);
        if (t0) {
          P tr = *(P*)((char*)t0 + 0x8), vr = *(P*)((char*)t0 + 0xC);
          ntr = tr ? *(int*)((char*)tr + 0xC) : 0;
          nv = vr ? *(int*)((char*)vr + 0xC) : 0;
        }
      }
      nlog("diag:      tileX=%d tileZ=%d tiles=%d  tile0: verts=%d tris=%d",
           *(int*)((char*)g + 0xC8), *(int*)((char*)g + 0xCC), ntile, nv, ntr);
    }
  }
}

/* ---- NavMeshGraph（A* 烘焙出来的可走面）-------------------------------
 * 偏移来自 dump.cs：NavmeshBase{tileXCount 0xC8, tileZCount 0xCC, tiles 0xD0}
 *                   NavmeshTile{tris 0x8, verts 0xC, nodes 0x24}
 *                   TriangleMeshNode{v0 0x24, v1 0x28, v2 0x2C}
 * Int3 = 3 个 int32，单位 1/1000 m。写出的二进制：
 *   "UCFNM1\0" | int32 nv | int32 nt | int32 verts[nv*3] | int32 tris[nt*3]
 */
static P find_navmesh_graph(P astar) {
  P data, graphs, g = 0;
  int n, i;
  if (!astar) return 0;
  data = *(P*)((char*)astar + 0x10);
  if (!data) return 0;
  graphs = *(P*)((char*)data + 0x20);
  if (!graphs) return 0;
  n = *(int*)((char*)graphs + 0xC);
  for (i = 0; i < n; i++) {
    P gg = *(P*)((char*)graphs + 0x10 + i * 4);
    P k;
    const char* cn;
    if (!gg) continue;
    k = *(P*)gg;
    cn = k ? i_class_get_name(k) : 0;
    if (cn && strstr(cn, "NavMesh")) g = gg;
  }
  return g;
}

/* 导出逻辑移到 editor.c（那里有 Transform / 矩阵的调用约定） */

static P new_go(const char* name) {
  P go = i_object_new(g_goCls);
  if (!go) return 0;
  ((ctor_str_t)RVA(0x331EA0))(go, i_string_new(name), 0);
  return go;
}

static P addcomp_cls(P go, P cls) {
  P type, comp;
  if (!go || !cls || !i_class_get_type || !i_type_get_object) return 0;
  type = i_type_get_object(i_class_get_type(cls));
  if (!type) return 0;
  comp = ((addcomp_t)RVA(0x331A90))(go, type, 0);
  return comp;
}

static void set_pos_of(P go, V3 p) {
  P tr = ((get_tr_t)RVA(0x332010))(go, 0);
  if (tr) ((set_pos_t)RVA(0x3F4840))(tr, p, 0);
}

/* Add one waypoint child under the graph root. */
static void add_wp(P rootTr, P nameStr, V3 pos) {
  P c = new_go("wp");   /* name passed below for a single allocation */
  P t;
  if (!c) return;
  /* new_go already named it; overwrite with shared name to avoid churn */
  (void)nameStr;
  t = ((get_tr_t)RVA(0x332010))(c, 0);
  if (!t) return;
  ((set_pos_t)RVA(0x3F4840))(t, pos, 0);
  ((set_parent_t)RVA(0x3F3AB0))(t, rootTr, 0, 0);
}

/* ---- MapManager spawn points -> extra graph nodes ---------------------- */
static P get_mm(void) {
  P v = 0;
  if (!g_mmInstField) return 0;
  i_field_static_get_value(g_mmInstField, &v);
  return n_live(v) ? v : 0;
}

static int add_spawn_nodes(P rootTr) {
  static const int offs[3] = { 0x10, 0x14, 0x1C }; /* SP_BL / SP_GR / SP_SupplyBox */
  P mm = get_mm();
  int made = 0;
  if (!mm) { nlog("spawn nodes: no MapManager instance"); return 0; }
  for (int k = 0; k < 3; k++) {
    P arr = *(P*)((char*)mm + offs[k]);
    int n = arr ? *(int*)((char*)arr + 0xC) : 0;
    for (int i = 0; i < n; i++) {
      V3 p = *(V3*)((char*)arr + 0x10 + i*16);
      V3 o, d;
      char hit[96];
      add_wp(rootTr, 0, p);
      made++;
      /* also put a node on the floor directly below the spawn point */
      o.x = p.x; o.y = 300.0f; o.z = p.z;
      d.x = 0.0f; d.y = -1.0f; d.z = 0.0f;
      if (((raycast_t)RVA(0xABB0A0))(o, d, hit, 700.0f, 1, 0)) {
        V3 g;
        g.x = *(float*)hit;
        g.y = *(float*)(hit + 4) + 0.2f;
        g.z = *(float*)(hit + 8);
        add_wp(rootTr, 0, g);
        made++;
      }
    }
  }
  nlog("spawn nodes added=%d", made);
  return made;
}

/* ---- missing ghost guard areas (Bot_NanoGuardArea / Bot_NanoGuardPos) -- */
static P arr_new(P cls, int n) {
  if (!cls) return 0;
  return i_array_new(cls, (unsigned int)n);
}

static P vec3_arr(const V3* v, int n) {
  P a = arr_new(g_vec3Cls, n);
  if (a && n > 0) memcpy((char*)a + 0x10, v, (size_t)n * 12);
  return a;
}

static P make_guard_area(V3 p, int npos) {
  P go, comp, list, nameStr;
  P hlist = 0, hname = 0;
  P posgo[4];
  P tr;
  V3 zero = { 0, 0, 0 };
  int i;
  int madePos = 0;
  if (!g_areaCls || !g_posCls || !g_vec3Cls || !g_listCls || !g_listCtor || !g_listAdd) return 0;
  if (npos < 1) npos = 1;
  if (npos > 4) npos = 4;

  go = new_go("UCF_GuardArea");
  if (!go) return 0;
  ((set_active_t)RVA(0x331CF0))(go, 0, 0);   /* keep inactive so Awake is deferred */
  comp = addcomp_cls(go, g_areaCls);
  if (!comp) { nlog("area: AddComponent failed"); return 0; }

  wfield(comp, 0x0C, vec3_arr(0, 0));             /* entrancePos  */
  wfield(comp, 0x14, arr_new(g_areaCls, 0));      /* neighborAreas */
  wfield(comp, 0x18, arr_new(g_areaCls, 0));      /* escapeAreas  */
  wfield(comp, 0x1C, vec3_arr(0, 0));             /* escapePos    */

  list = i_object_new(g_listCls);
  if (!list) return 0;
  if (i_gchandle_new) hlist = (P)i_gchandle_new(list, 0);   /* List is not native-rooted */
  i_runtime_invoke(g_listCtor, list, 0, 0);
  wfield(comp, 0x10, list);                       /* posList (non-null, Awake iterates it) */

  nameStr = i_string_new("UCF_GuardPos");
  if (i_gchandle_new) hname = (P)i_gchandle_new(nameStr, 0);
  for (i = 0; i < npos; i++) {
    V3 zdir = { 0.0f, 0.0f, 1.0f };
    V3 pp;
    P pgo, pcomp, zoom;
    void* args[1];
    pgo = i_object_new(g_goCls);
    if (!pgo) break;
    ((ctor_str_t)RVA(0x331EA0))(pgo, nameStr, 0);
    ((set_active_t)RVA(0x331CF0))(pgo, 0, 0);
    pcomp = addcomp_cls(pgo, g_posCls);
    if (!pcomp) break;
    zoom = vec3_arr(&zdir, 1);
    wfield(pcomp, 0x10, zoom);                    /* zoomPos: >=1 so GetRandomZoomPos works */
    *(int*)((char*)pcomp + 0x1C) = i % 5;         /* safety */
    pp.x = p.x + (float)(i * 2) - 1.0f;
    pp.y = p.y;
    pp.z = p.z + (float)(i * 2) - 1.0f;
    set_pos_of(pgo, pp);
    args[0] = pcomp;
    i_runtime_invoke(g_listAdd, list, args, 0);   /* posList.Add(pos) */
    posgo[madePos++] = pgo;
  }
  if (madePos == 0) {
    nlog("area: no pos created");
    if (hname && i_gchandle_free) i_gchandle_free(hname);
    if (hlist && i_gchandle_free) i_gchandle_free(hlist);
    return 0;
  }

  set_pos_of(go, p);
  ((set_active_t)RVA(0x331CF0))(go, 1, 0);        /* Awake: fills refs + registers area */
  for (i = 0; i < madePos; i++) ((set_active_t)RVA(0x331CF0))(posgo[i], 1, 0);
  if (hname && i_gchandle_free) i_gchandle_free(hname);
  if (hlist && i_gchandle_free) i_gchandle_free(hlist);
  return comp;
}

static void purge_guard_areas(void) {
  P f, list, items;
  int n, i, w = 0, dead = 0;
  if (!g_areaCls) return;
  f = i_class_get_field_from_name(g_areaCls, "SpareAreaList");
  if (!f) return;
  list = 0;
  i_field_static_get_value(f, &list);
  if (!list) return;
  items = *(P*)((char*)list + 0x8);
  n = *(int*)((char*)list + 0xC);
  if (!items || n <= 0) return;
  {
    int cap = *(int*)((char*)items + 0xC);   /* array length, not list size */
    if (cap <= 0 || n > cap) { nlog("guard areas: bad list size %d/%d, skip purge", n, cap); return; }
  }
  for (i = 0; i < n; i++) {
    P o = *(P*)((char*)items + 0x10 + i*4);
    if (n_live(o)) *(P*)((char*)items + 0x10 + w++) = o;
    else dead++;
  }
  if (w != n) {
    *(int*)((char*)list + 0xC) = w;
    (*(int*)((char*)list + 0x10))++;
    nlog("guard areas: purged %d dead entries (now %d)", dead, w);
  }
}

static V3 g_spots[64];
static int g_nspots;
static P  g_areaComps[64];
static int g_madeAreas;

/* give the areas neighbours: after a ghost arrives it re-targets a linked area */
static void link_guard_areas(void) {
  int n = g_madeAreas, i;
  if (n < 2) return;
  for (i = 0; i < n; i++) {
    P arr = arr_new(g_areaCls, 3);
    P esc = 0;
    P harr = 0, hesc = 0;
    if (arr && i_gchandle_new) harr = (P)i_gchandle_new(arr, 0);
    esc = arr_new(g_areaCls, 2);
    if (esc && i_gchandle_new) hesc = (P)i_gchandle_new(esc, 0);
    if (!arr) {
      if (hesc && i_gchandle_free) i_gchandle_free(hesc);
      continue;
    }
    {
      P* d = (P*)((char*)arr + 0x10);
      d[0] = g_areaComps[(i + 1) % n];
      d[1] = g_areaComps[(i + 5) % n];
      d[2] = g_areaComps[(i + 11) % n];
    }
    wfield(g_areaComps[i], 0x14, arr);
    if (esc) {
      P* e = (P*)((char*)esc + 0x10);
      e[0] = g_areaComps[(i + 3) % n];
      e[1] = g_areaComps[(i + 7) % n];
      wfield(g_areaComps[i], 0x18, esc);
    }
    if (hesc && i_gchandle_free) i_gchandle_free(hesc);
    if (harr && i_gchandle_free) i_gchandle_free(harr);
  }
  nlog("guard areas: neighbour links set for %d areas", n);
}

static int g_graphOurs;   /* 1 = build_waypoints generated the current graph */
static int g_collectOnly; /* 1 = 只读采集：不改动游戏里的任何状态 */
int  navfix_collect_only(void) { return g_collectOnly; }
void navfix_set_collect_only(int on) { g_collectOnly = on ? 1 : 0; nlog("collect-only %s", on ? "ON" : "OFF"); }

/* ===================== 地面采样 + 三个独立动作 ==========================
 * 2026-11-16 拆解：原来 build_waypoints() 把「铺路点 / 补蹲守点 / 造守卫区」
 * 写死在同一个函数里，第一个不跑后两个永远不会执行 —— 那三个开关是假的。
 * 现在：
 *     survey()          只做射线采样，把坐标填进 g_all[]，不创建任何对象
 *     act_waypoints()   建 UCF_WayPoints + Scan + ConnectNodes
 *     act_crouch()      补 Bot_CrouchPos
 *     act_guard()       造 Bot_NanoGuardArea / Bot_NanoGuardPos
 * 三者各自读自己的 cfg 开关，互不为前提；日志里各打一行，关掉也看得见。
 */
#define MAX_SPOTS 16384
static V3   g_all[MAX_SPOTS];
static int  g_nall;
static float g_minX, g_maxX, g_minZ, g_maxZ;
static int  g_survOk;   /* 本场景采样成功 */
static int  g_crDone;   /* 本场景蹲守点已处理 */
static int  g_gaDone;   /* 本场景守卫区已处理 */

static void setup_reset(void) {
  g_survOk = 0; g_crDone = 0; g_gaDone = 0;
  g_nall = 0; g_nspots = 0;
}

static int survey(void) {
  raycast_t rc;
  char hit[96];
  float minX = 1e9f, maxX = -1e9f, minZ = 1e9f, maxZ = 1e9f;
  int ch = 0;
  float fx, fz;
  int layer;

  if (g_survOk) return 1;
  rc = (raycast_t)RVA(0xABB0A0);

  /* 粗扫：确定这张图的可走范围 */
  for (fx = -250.0f; fx <= 250.0f; fx += 20.0f)
    for (fz = -250.0f; fz <= 250.0f; fz += 20.0f) {
      V3 o = { fx, 300.0f, fz }, d = { 0.0f, -1.0f, 0.0f };
      if (!rc(o, d, hit, 700.0f, 1, 0)) continue;
      if (*(float*)(hit + 16) < 0.6f) continue;
      ch++;
      if (*(float*)hit < minX) minX = *(float*)hit;
      if (*(float*)hit > maxX) maxX = *(float*)hit;
      if (*(float*)(hit + 8) < minZ) minZ = *(float*)(hit + 8);
      if (*(float*)(hit + 8) > maxZ) maxZ = *(float*)(hit + 8);
    }
  if (ch < 8) { nlog("survey: too few ground hits (%d), retry later", ch); return 0; }
  nlog("survey: coarse hits=%d bounds x[%.1f,%.1f] z[%.1f,%.1f]", ch, minX, maxX, minZ, maxZ);
  g_minX = minX; g_maxX = maxX; g_minZ = minZ; g_maxZ = maxZ;

  /* 细扫：单条向下射线只会打到屋顶，室内（幽灵出生洞）就没点了。
   * 所以每列往下追射最多 5 层。 */
  g_nall = 0; g_nspots = 0;
  for (fx = minX - 4.0f; fx <= maxX + 4.0f; fx += 4.0f)
    for (fz = minZ - 4.0f; fz <= maxZ + 4.0f; fz += 4.0f) {
      float y = 300.0f;
      for (layer = 0; layer < 5; layer++) {
        V3 o = { fx, y, fz }, d = { 0.0f, -1.0f, 0.0f };
        V3 pos;
        if (!rc(o, d, hit, 700.0f, 1, 0)) break;
        if (*(float*)(hit + 16) < 0.65f) break;
        pos.x = *(float*)hit;
        pos.y = *(float*)(hit + 4) + 0.2f;
        pos.z = *(float*)(hit + 8);
        /* y=39..57 是天空盒/天花板碰撞体，不是可走的地面 */
        if (pos.y < -30.0f || pos.y > 15.0f) {
          y = *(float*)(hit + 4) - 1.5f;
          if (y < -80.0f) break;
          continue;
        }
        /* 守卫区只建在真正的地面上：高处会让幽灵尝试飞行 */
        if ((g_nall % 11) == 0 && g_nspots < 64 && pos.y > -3.0f && pos.y < 9.0f) g_spots[g_nspots++] = pos;
        if (g_nall < MAX_SPOTS) g_all[g_nall++] = pos;
        y = *(float*)(hit + 4) - 1.5f;
        if (y < -80.0f) break;
      }
    }
  nlog("survey: spots=%d guardCandidates=%d", g_nall, g_nspots);
  if (g_nall < 8) { nlog("survey: too few spots (%d), retry later", g_nall); return 0; }
  g_survOk = 1;
  return 1;
}

/* ---- 动作 1：铺 A* 路点 ---- */
static void act_waypoints(void) {
  P astar, pg, root, rootTr, childName, hchild = 0;
  ctor_str_t ctor;
  get_tr_t gtr;
  set_pos_t sp;
  set_parent_t sparent;
  int before, made = 0, k;

  if (!cfg_bool("auto_waypoints", 1)) { nlog("[cfg] auto_waypoints = off, skip waypoints"); return; }
  astar = astar_active();
  if (!astar) { nlog("waypoints: no AstarPath.active"); return; }
  pg = point_graph(astar);
  if (!pg) { nlog("waypoints: no PointGraph in scene"); return; }
  before = *(int*)((char*)pg + 0xEC);
  if (before > 0) { nlog("waypoints: graph already has %d nodes, skip", before); return; }
  if (!g_goCls) { nlog("waypoints: GameObject class missing"); return; }

  ctor = (ctor_str_t)RVA(0x331EA0);
  gtr = (get_tr_t)RVA(0x332010);
  sp = (set_pos_t)RVA(0x3F4840);
  sparent = (set_parent_t)RVA(0x3F3AB0);

  root = i_object_new(g_goCls);
  ctor(root, i_string_new("UCF_WayPoints"), 0);
  rootTr = gtr(root, 0);
  { V3 zero = { 0, 0, 0 }; sp(rootTr, zero, 0); }

  childName = i_string_new("wp");
  if (i_gchandle_new) hchild = (P)i_gchandle_new(childName, 0);
  for (k = 0; k < g_nall; k++) {
    P c = i_object_new(g_goCls);
    P t;
    if (!c) break;
    ctor(c, childName, 0);
    t = gtr(c, 0);
    sp(t, g_all[k], 0);
    sparent(t, rootTr, 0, 0);
    made++;
  }
  nlog("waypoint objects created=%d", made);
  if (made < 8) {
    nlog("waypoints too few, abort");
    if (hchild && i_gchandle_free) i_gchandle_free(hchild);
    return;
  }

  /* 地图自带的出生点上补节点：保证 Bot.Update 的起始节点非空 */
  add_spawn_nodes(rootTr);
  if (i_wbarrier) i_wbarrier(pg, (char*)pg + 0xB8, rootTr);
  *(P*)((char*)pg + 0xB8) = rootTr;

  *(float*)((char*)pg + 0xC0) = 4.6f;        /* maxDistance：4m 栅格连得上，5m 以上地面缝连不上 */
  /* 只按距离连线会穿墙，A* 会把幽灵直接送去撞墙。
   * PointGraph.raycast 让 ConnectNodes 做线检测，被挡住的一对直接丢掉。 */
  *(unsigned char*)((char*)pg + 0xD0) = 1;   /* raycast */
  *(unsigned char*)((char*)pg + 0xD2) = 0;   /* thickRaycast */
  *(int*)((char*)pg + 0xDC) = -1;            /* mask: 全部 */

  { scan_t scan = (scan_t)RVA(0x581640); scan(pg, 0); }
  nlog("scan done: nodes=%d (was %d)", *(int*)((char*)pg + 0xEC), before);
  g_graphOurs = 1;

  {
    typedef void (*connect_t)(P, void*);
    connect_t connectNodes = (connect_t)RVA(0x5EE8E0);
    P nodes;
    int cnt2, withLinks = 0, totalLinks = 0, sampleN, n2;
    connectNodes(pg, 0);
    nodes = *(P*)((char*)pg + 0xE8);
    cnt2 = nodes ? *(int*)((char*)nodes + 0xC) : 0;
    sampleN = cnt2 < 300 ? cnt2 : 300;
    for (n2 = 0; n2 < sampleN; n2++) {
      P nd = *(P*)((char*)nodes + 0x10 + n2*4);
      P cc;
      if (!nd) continue;
      cc = *(P*)((char*)nd + 0x20);
      if (cc) { int L = *(int*)((char*)cc + 0xC); if (L > 0) withLinks++; totalLinks += L; }
    }
    nlog("connected: sampled=%d withLinks=%d totalLinks=%d", sampleN, withLinks, totalLinks);
  }
  if (hchild && i_gchandle_free) i_gchandle_free(hchild);
}

/* ---- 动作 2：补蹲守点 ---- */
static void act_crouch(void) {
  P spareField, spareList = 0, typeObj, nameStr, hname2 = 0;
  addcomp_t addComp;
  ctor_str_t ctor;
  get_tr_t gtr;
  set_pos_t sp;
  raycast_t rc;
  char hit[96];
  int existing, made2 = 0;
  float cx, cz;

  if (g_crDone) return;
  g_crDone = 1;
  if (!cfg_bool("auto_crouch", 1)) { nlog("[cfg] auto_crouch = off, skip crouch points"); return; }
  if (!g_crouchCls || !i_class_get_type || !i_type_get_object) { nlog("crouch: Bot_CrouchPos class missing"); return; }

  spareField = i_class_get_field_from_name(g_crouchCls, "SpareList_BL");
  if (spareField) i_field_static_get_value(spareField, &spareList);
  existing = spareList ? *(int*)((char*)spareList + 0xC) : -1;
  {
    extern int editor_crouch_made(void);
    int own = editor_crouch_made();
    nlog("crouch: existing SpareList_BL count=%d (editor-made=%d)", existing, own);
    if (existing > 0 && own > 0) existing -= own;
  }
  if (existing > 0) { nlog("crouch: map already has %d, skip", existing); return; }

  rc = (raycast_t)RVA(0xABB0A0);
  ctor = (ctor_str_t)RVA(0x331EA0);
  gtr = (get_tr_t)RVA(0x332010);
  sp = (set_pos_t)RVA(0x3F4840);
  typeObj = i_type_get_object(i_class_get_type(g_crouchCls));
  addComp = (addcomp_t)RVA(0x331A90);
  nameStr = i_string_new("CrouchPos");
  if (i_gchandle_new) hname2 = (P)i_gchandle_new(nameStr, 0);

  for (cx = g_minX - 2.0f; cx <= g_maxX + 2.0f; cx += 9.0f)
    for (cz = g_minZ - 2.0f; cz <= g_maxZ + 2.0f; cz += 9.0f) {
      V3 o = { cx, 300.0f, cz }, d = { 0.0f, -1.0f, 0.0f };
      P co, comp, ct;
      V3 cpos;
      if (!rc(o, d, hit, 700.0f, 1, 0)) continue;
      if (*(float*)(hit + 16) < 0.8f) continue;
      co = i_object_new(g_goCls);
      ctor(co, nameStr, 0);
      comp = addComp(co, typeObj, 0);
      if (!comp) continue;
      ct = gtr(co, 0);
      cpos.x = *(float*)hit;
      cpos.y = *(float*)(hit + 4) + 0.05f;
      cpos.z = *(float*)(hit + 8);
      sp(ct, cpos, 0);
      made2++;
    }
  {
    P list2 = 0;
    int now;
    if (spareField) i_field_static_get_value(spareField, &list2);
    now = list2 ? *(int*)((char*)list2 + 0xC) : -1;
    nlog("crouch: created=%d registered=%d", made2, now);
  }
  if (hname2 && i_gchandle_free) i_gchandle_free(hname2);
}

/* ---- 动作 3：幽灵守卫区 ---- */
static void act_guard(void) {
  P f = 0, list = 0;
  int madeA = 0, k, existing = -1;

  if (g_gaDone) return;
  g_gaDone = 1;
  if (!cfg_bool("ghost_areas", 1)) { nlog("[cfg] ghost_areas = off, skip guard areas"); return; }
  if (!g_areaCls || !g_posCls || !g_vec3Cls || !g_listCls || !g_listCtor || !g_listAdd) {
    nlog("guard areas: classes missing area=%p pos=%p vec3=%p list=%p", g_areaCls, g_posCls, g_vec3Cls, g_listCls);
    return;
  }
  if (g_nspots == 0) { nlog("guard areas: no candidate spots, skip"); return; }

  f = i_class_get_field_from_name(g_areaCls, "SpareAreaList");
  if (f) i_field_static_get_value(f, &list);
  if (list) existing = *(int*)((char*)list + 0xC);
  if (existing > 0) { nlog("guard areas: map already has %d, skip", existing); return; }

  g_madeAreas = 0;
  for (k = 0; k < g_nspots && g_madeAreas < 64; k++) {
    P comp = make_guard_area(g_spots[k], 1 + (k % 2));
    if (comp) { g_areaComps[g_madeAreas++] = comp; madeA++; }
  }
  link_guard_areas();
  {
    P l2 = 0;
    if (f) i_field_static_get_value(f, &l2);
    nlog("guard areas: created=%d spots=%d SpareAreaList=%d", madeA, g_nspots, l2 ? *(int*)((char*)l2 + 0xC) : -1);
  }
}

/* ---- 调度：采样一次，三个动作按开关各跑各的 ---- */
static void run_setup(void) {
  int wp, cr, ga;
  if (InterlockedCompareExchange(&g_appQuit, 0, 0)) return;
  if (g_collectOnly) { nlog("readonly: skip setup (collect-only)"); return; }
  wp = cfg_bool("auto_waypoints", 1);
  cr = cfg_bool("auto_crouch", 1);
  ga = cfg_bool("ghost_areas", 1);
  if (!wp && !cr && !ga) { nlog("[cfg] all setup actions are off, nothing to do"); return; }
  if (!astar_active()) { nlog("no AstarPath.active"); return; }
  if (!survey()) return;

  nlog("setup: waypoints=%s crouch=%s guard=%s spots=%d",
       wp ? "on" : "off", cr ? "on" : "off", ga ? "on" : "off", g_nall);
  hold_bots(1);
  if (wp) act_waypoints();
  if (cr) act_crouch();
  if (ga) act_guard();
  hold_bots(0);
}

/* ---- main-thread scene tick (all il2cpp calls happen here) -------------- */
static P g_lastAstar;
static int g_zeroStreak;

static void nav_tick(void) {
  P a, pg;
  int nodes;
  if (InterlockedCompareExchange(&g_appQuit, 0, 0)) return;
  a = astar_active();
  if (a && a != g_lastAstar) {
    g_lastAstar = a;
    g_zeroStreak = 0;
    g_graphOurs = 0;
    setup_reset();
    nlog("scene astar=%p (purge start)", a);
    if (!g_collectOnly) purge_guard_areas();
    nlog("scene astar=%p (purge done, notify editor)", a);
    { void editor_on_scene(void*); editor_on_scene((void*)a); }
    navfix_diag_graphs();
    nlog("scene astar=%p (editor notified)", a);
    {
      P pg0 = point_graph(a);
      { int editor_nogen(void);
        if (!g_collectOnly && !editor_nogen() && pg0 && *(int*)((char*)pg0 + 0xEC) == 0) { nlog("scene change: running setup immediately"); run_setup(); } }
    }
  }
  pg = point_graph(a);
  nodes = pg ? *(int*)((char*)pg + 0xEC) : -1;
  if (pg && nodes == 0) {
    g_zeroStreak++;
    if (g_collectOnly) {
      if ((g_zeroStreak % 20) == 0) nlog("collect-only: graph still empty (~%.0f s)", g_zeroStreak * 0.25f);
    } else { int editor_nogen(void);
      if (!editor_nogen() && (g_zeroStreak == 4 || (g_zeroStreak > 4 && (g_zeroStreak % 10) == 0))) {
        run_setup();
      }
    }
  } else if (!pg) {
    g_zeroStreak++;
    if ((g_zeroStreak % 8) == 0) nlog("waiting for PointGraph (tick %d)", g_zeroStreak);
  } else {
    g_zeroStreak = 0;
  }
  { void editor_tick(void); editor_tick(); }
  if (g_collectOnly) {
    static int diagTick;
    if ((++diagTick % 40) == 0) navfix_diag_graphs();   /* 每 ~10 s 再打一次，看会不会后来长出来 */
  }
}

static WNDPROC g_oldProc;
static HWND g_hwnd;
static volatile LONG g_buildCount;

HWND navfix_hwnd(void) { return g_hwnd; }

#define WM_UCF_TICK   (WM_APP + 0x50)
#define WM_UCF_BUILD  (WM_APP + 0x51)
#define WM_UCF_SCENE  (WM_APP + 0x52)
#define WM_UCF_KEY    (WM_APP + 0x53)
#define WM_UCF_INJECT (WM_APP + 0x54)

static LRESULT CALLBACK NavProc(HWND h, UINT msg, WPARAM w, LPARAM l) {
  if (msg == WM_CLOSE || msg == WM_QUERYENDSESSION || msg == WM_ENDSESSION) {
    if (InterlockedExchange(&g_appQuit, 1) == 0) nlog("quit: msg=0x%X", msg);
    if (!g_oldProc) return DefWindowProcA(h, msg, w, l);
    return CallWindowProcA(g_oldProc, h, msg, w, l);
  }
  if (msg == WM_DESTROY || msg == WM_NCDESTROY) {
    WNDPROC old = g_oldProc;
    if (InterlockedExchange(&g_appQuit, 1) == 0) nlog("quit: destroy msg=0x%X", msg);
    { void editor_on_quit(void); editor_on_quit(); }
    if (old) {
      SetWindowLongPtrA(h, GWLP_WNDPROC, (LONG_PTR)old);
      g_oldProc = 0;
      nlog("quit: wndproc restored");
      return CallWindowProcA(old, h, msg, w, l);
    }
    return 0;
  }
  if (InterlockedCompareExchange(&g_appQuit, 0, 0)) return 0;

  if (msg == WM_UCF_TICK) {
    static int warmed;
    if (!warmed) { void editor_ensure_init(void); editor_ensure_init(); warmed = 1; }
    nav_tick();
    return 0;
  }
  if (msg == WM_UCF_INJECT) {
    void plugin_tick(void);
    plugin_tick();
    return 0;
  }
  if (msg == WM_UCF_BUILD) {
    if (!g_oldProc) return 0;
    InterlockedIncrement(&g_buildCount);
    nlog("build request #%d", g_buildCount);
    setup_reset();
    run_setup();
    return 0;
  }
  if (msg == WM_UCF_SCENE) {
    void editor_on_scene(void*);
    editor_on_scene((void*)w);
    return 0;
  }
  if (msg == WM_UCF_KEY) {
    void editor_on_key_any(unsigned, int);
    editor_on_key_any((unsigned)w, (int)l);
    return 0;
  }
  if (msg == WM_KEYDOWN) {
    if (w == VK_DELETE) {
      void editor_delete_nearest(void);
      editor_delete_nearest();
    } else if (GetAsyncKeyState(VK_CONTROL) & 0x8000) {
      int shift = (GetAsyncKeyState(VK_SHIFT) & 0x8000) ? 1 : 0;
      void editor_on_key_mod(unsigned, int);
      editor_on_key_mod((unsigned)w, shift);
    }
  }
  if (!g_oldProc) return DefWindowProcA(h, msg, w, l);
  return CallWindowProcA(g_oldProc, h, msg, w, l);
}

typedef struct { DWORD pid; HWND hwnd; } FindCtx;
static BOOL CALLBACK EnumProc(HWND h, LPARAM lp) {
  FindCtx* c = (FindCtx*)lp;
  DWORD pid = 0;
  GetWindowThreadProcessId(h, &pid);
  if (pid != c->pid) return TRUE;
  if (!IsWindowVisible(h)) return TRUE;
  if (GetWindowTextLengthA(h) == 0) return TRUE;
  RECT r; GetClientRect(h, &r);
  if (r.right - r.left < 200) return TRUE;
  c->hwnd = h;
  return FALSE;
}

static HWND find_window(void) {
  FindCtx c; c.pid = GetCurrentProcessId(); c.hwnd = 0;
  EnumWindows(EnumProc, (LPARAM)&c);
  return c.hwnd;
}

static DWORD WINAPI nav_worker(LPVOID x) {
  for (int i = 0; i < 600 && !g_ga; i++) { g_ga = GetModuleHandleA("GameAssembly.dll"); if (!g_ga) Sleep(200); }
  if (!g_ga) { nlog("GameAssembly not found"); return 0; }
#define RE(n) *(void**)&i_##n = GetProcAddress(g_ga, "il2cpp_" #n)
  RE(domain_get); RE(domain_get_assemblies); RE(assembly_get_image); RE(image_get_name);
  RE(class_from_name); RE(class_get_field_from_name); RE(field_static_get_value);
  RE(object_new); RE(string_new); RE(thread_attach); RE(class_get_name);
  RE(class_get_type); RE(type_get_object); RE(class_get_parent);
  RE(class_get_method_from_name); RE(runtime_invoke); RE(field_get_type);
  RE(class_from_il2cpp_type); RE(array_new); RE(class_get_element_class);
  RE(field_static_set_value);
  RE(field_static_get_value);
  RE(gchandle_new); RE(gchandle_free);
  *(void**)&i_wbarrier = GetProcAddress(g_ga, "il2cpp_gc_wbarrier_set_field");
#undef RE
  if (!i_domain_get || !i_class_from_name) { nlog("il2cpp exports missing"); return 0; }
  for (int i = 0; i < 600; i++) { if (i_domain_get()) break; Sleep(200); }
  if (!i_domain_get()) { nlog("domain not ready"); return 0; }
  if (i_thread_attach) i_thread_attach(i_domain_get());

  P imgUE = find_image("UnityEngine.CoreModule.dll");
  if (imgUE) {
    g_goCls = i_class_from_name(imgUE, "UnityEngine", "GameObject");
    g_vec3Cls = i_class_from_name(imgUE, "UnityEngine", "Vector3");
  }
  P imgCS = find_image("Assembly-CSharp.dll");
  if (imgCS) {
    g_botCls = i_class_from_name(imgCS, "", "Bot");
    if (g_botCls) g_stopField = i_class_get_field_from_name(g_botCls, "stopAllBot");
    g_crouchCls = i_class_from_name(imgCS, "", "Bot_CrouchPos");
    g_areaCls = i_class_from_name(imgCS, "", "Bot_NanoGuardArea");
    g_posCls = i_class_from_name(imgCS, "", "Bot_NanoGuardPos");
    g_mmCls = i_class_from_name(imgCS, "", "MapManager");
    if (g_mmCls) {
      P base = i_class_get_parent(g_mmCls);
      if (base) g_mmInstField = i_class_get_field_from_name(base, "<instance>k__BackingField");
    }
    if (g_areaCls && i_class_get_field_from_name) {
      P fld = i_class_get_field_from_name(g_areaCls, "posList");
      if (fld) {
        P ft = i_field_get_type(fld);
        g_listCls = ft ? i_class_from_il2cpp_type(ft) : 0;
        if (g_listCls) {
          g_listCtor = i_class_get_method_from_name(g_listCls, ".ctor", 0);
          g_listAdd = i_class_get_method_from_name(g_listCls, "Add", 1);
        }
      }
    }
  }
  int n = 0; P arr = i_domain_get_assemblies(i_domain_get(), &n);
  for (int i = 0; i < n && !g_astarCls; i++) {
    P asm_ = *(P*)((char*)arr + 0x10 + i*4);
    P img = i_assembly_get_image(asm_);
    if (!img) continue;
    g_astarCls = i_class_from_name(img, "", "AstarPath");
  }
  nlog("ready: GameObject=%p AstarPath=%p area=%p pos=%p list=%p mm=%p",
       g_goCls, g_astarCls, g_areaCls, g_posCls, g_listCls, g_mmCls);
  if (!g_goCls || !g_astarCls) return 0;

  for (int i = 0; i < 200 && !g_hwnd; i++) { g_hwnd = find_window(); if (!g_hwnd) Sleep(300); }
  if (!g_hwnd) { nlog("game window not found"); return 0; }
  g_oldProc = (WNDPROC)SetWindowLongPtrA(g_hwnd, GWLP_WNDPROC, (LONG_PTR)NavProc);
  nlog("window hooked %p old=%p", g_hwnd, g_oldProc);
  g_ready = 1;

  for (;;) {
    if (InterlockedCompareExchange(&g_appQuit, 0, 0)) { nlog("quit: nav worker stop"); break; }
    if (g_hwnd) PostMessageA(g_hwnd, WM_UCF_TICK, 0, 0);
    Sleep(250);
  }
  return 0;
}

/* ---- exports used by the in-game visual editor (editor.c) -------------- */
P navfix_point_graph(void) { return point_graph(astar_active()); }

/* 给 editor.c 用：A* 的第 [0] 张图 NavMeshGraph（真正的人机可走面） */
P navfix_navmesh_graph(void) { return find_navmesh_graph(astar_active()); }

/* 1 = the current graph was generated by build_waypoints (we own the points),
 * 0 = the game scanned its own scene graph.  The JSON exporter records this as
 * map.source so the offline editor knows whether node positions are editable. */
int navfix_graph_ours(void) { return g_graphOurs; }

P navfix_add_guard_area(float x, float y, float z) {
  V3 p;
  p.x = x; p.y = y; p.z = z;
  return make_guard_area(p, 2);
}

void navfix_start(const char* modDir) {
  sprintf(g_log, "%s\\ucf_mod.log", modDir);
  CreateThread(0, 0, nav_worker, 0, 0, 0);
}
