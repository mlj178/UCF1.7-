// navfix.c - A* PointGraph waypoints + missing AI markers for the hidden map.
// 2026-11-15: exit gate + main-thread il2cpp; spawn node coverage; runtime ghost guard areas.
#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>
#include <math.h>
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

/* editor.c 用：拿 AstarPath.active（grow 模式要它的 pathProcessor 来阻塞寻路） */
P navfix_astar(void) { return astar_active(); }

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
  /* 2026-11-17 13:03 实测：就是这段把数组写花的。
   * 原写法把「读槽位、判活、写回同一下标」压在一行里（*(P*)(items+..+w++) = o），
   * -O2 内联后写回的地址/宽度不可靠：purge-before 三个槽位全是合法对象，
   * purge-after 就变成 0x5050f0d8 / 0x02790279 这种半截数据（16 位错位）。
   * 现在改成：显式 4 字节读 → 只在 w != i 时才 4 字节搬，绝不原地写。 */
  for (i = 0; i < n; i++) {
    unsigned tmp = 0;
    P o;
    memcpy(&tmp, (char*)items + 0x10 + i*4, 4);
    o = (P)tmp;
    if (!o) continue;
    if (n_live(o)) {
      if (w != i) memcpy((char*)items + 0x10 + w*4, &tmp, 4);
      w++;
    } else dead++;
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
/* 2026-11-16：暴风图在细扫阶段把游戏卡死（WER AppHangB1）。
 * 根因是 maxZ 的初值写成了 +1e9（应为 -1e9）：粗扫更新 maxZ 的条件是
 * hit.z > maxZ，正常地图永远不成立，maxZ 一直是 1e9。
 * 细扫 for (fz = minZ-4; fz <= maxZ+4; fz += 4) 于是从 -134 跑到 1e9，
 * 约 (1e9/4) × 列数 ≈ 五十多亿次，主线程直接卡死。
 * 日志里的 z[-130,1000000000] 就是初值，不是命中点。
 * 现在：初值修正为 -1e9；再加命中点校验、包络校验、列数上限三重保险。 */
static int hit_sane(const char* hit, float fx, float fz, V3* out) {
  float hx = *(const float*)hit;
  float hy = *(const float*)(hit + 4);
  float hz = *(const float*)(hit + 8);
  if (!isfinite(hx) || !isfinite(hy) || !isfinite(hz)) return 0;
  if (fabsf(hx - fx) > 0.75f || fabsf(hz - fz) > 0.75f) return 0;
  if (hy < -500.0f || hy > 500.0f) return 0;
  if (out) { out->x = hx; out->y = hy; out->z = hz; }
  return 1;
}

static int survey(void) {
  raycast_t rc;
  char hit[96];
  float minX = 1e9f, maxX = -1e9f, minZ = 1e9f, maxZ = -1e9f;
  int ch = 0, bad = 0, cols = 0;
  float fx, fz;
  int layer;

  if (g_survOk) return 1;
  rc = (raycast_t)RVA(0xABB0A0);

  /* 粗扫：确定这张图的可走范围 */
  for (fx = -250.0f; fx <= 250.0f; fx += 20.0f)
    for (fz = -250.0f; fz <= 250.0f; fz += 20.0f) {
      V3 o = { fx, 300.0f, fz }, d = { 0.0f, -1.0f, 0.0f };
      if (!rc(o, d, hit, 700.0f, 1, 0)) continue;
      if (!hit_sane(hit, fx, fz, 0)) {
        if (!bad) nlog("survey: bad hit at %.1f,%.1f -> %.1f,%.1f,%.1f", fx, fz, *(float*)hit, *(float*)(hit + 4), *(float*)(hit + 8));
        bad++; continue;
      }
      if (*(float*)(hit + 16) < 0.6f) continue;
      ch++;
      if (*(float*)hit < minX) minX = *(float*)hit;
      if (*(float*)hit > maxX) maxX = *(float*)hit;
      if (*(float*)(hit + 8) < minZ) minZ = *(float*)(hit + 8);
      if (*(float*)(hit + 8) > maxZ) maxZ = *(float*)(hit + 8);
    }
  if (bad) nlog("survey: dropped %d bogus hits", bad);
  if (ch < 8) { nlog("survey: too few ground hits (%d), retry later", ch); return 0; }
  {
    float w = maxX - minX, h = maxZ - minZ;
    if (!isfinite(w) || !isfinite(h) || w < 1.0f || h < 1.0f || w > 700.0f || h > 700.0f) {
      nlog("survey: rejected bounds x[%.1f,%.1f] z[%.1f,%.1f]", minX, maxX, minZ, maxZ);
      return 0;
    }
  }
  nlog("survey: coarse hits=%d bounds x[%.1f,%.1f] z[%.1f,%.1f]", ch, minX, maxX, minZ, maxZ);
  g_minX = minX; g_maxX = maxX; g_minZ = minZ; g_maxZ = maxZ;

  /* 细扫：单条向下射线只会打到屋顶，室内（幽灵出生洞）就没点了。
   * 所以每列往下追射最多 5 层。 */
  g_nall = 0; g_nspots = 0;
  for (fx = minX - 4.0f; fx <= maxX + 4.0f; fx += 4.0f)
    for (fz = minZ - 4.0f; fz <= maxZ + 4.0f; fz += 4.0f) {
      float y = 300.0f;
      if (++cols > 50000) { nlog("survey: column cap %d hit, abort", cols); return 0; }
      for (layer = 0; layer < 5; layer++) {
        V3 o = { fx, y, fz }, d = { 0.0f, -1.0f, 0.0f };
        V3 pos;
        if (!rc(o, d, hit, 700.0f, 1, 0)) break;
        if (!hit_sane(hit, fx, fz, &pos)) {
          if (!bad) nlog("survey: bad hit at %.1f,%.1f -> %.1f,%.1f,%.1f", fx, fz, *(float*)hit, *(float*)(hit + 4), *(float*)(hit + 8));
          bad++; break;
        }
        if (*(float*)(hit + 16) < 0.65f) break;
        pos.y = *(float*)(hit + 4) + 0.2f;
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
  nlog("survey: spots=%d guardCandidates=%d dropped=%d", g_nall, g_nspots, bad);
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
  int gridOn = 1, pmN = 0;
  float cx, cz;

  if (g_crDone) return;
  g_crDone = 1;
  /* auto_crouch 只管 9 m 网格撒点；玩家记录点是用户亲自站过的位置，始终要造，
   * 否则关掉网格就一条蹲守点都没有，人机又没目标了。 */
  {
    extern int editor_pm_count(void);
    gridOn = cfg_bool("auto_crouch", 1);
    pmN = editor_pm_count();
    if (!gridOn && pmN <= 0) { nlog("[cfg] auto_crouch = off and no player marks, skip crouch"); return; }
  }
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
  rc = (raycast_t)RVA(0xABB0A0);
  ctor = (ctor_str_t)RVA(0x331EA0);
  gtr = (get_tr_t)RVA(0x332010);
  sp = (set_pos_t)RVA(0x3F4840);
  typeObj = i_type_get_object(i_class_get_type(g_crouchCls));
  addComp = (addcomp_t)RVA(0x331A90);
  nameStr = i_string_new("CrouchPos");
  if (i_gchandle_new) hname2 = (P)i_gchandle_new(nameStr, 0);

  if (!gridOn) {
    nlog("crouch: grid off, player marks only");
  } else if (existing > 0) {
    nlog("crouch: map already has %d, skip grid", existing);
  } else {
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
  }

  /* 玩家坐标记录：每个记录点直接造一个蹲守点（记录的就是脚下地面，不再向下打射线）。
   * 这样用户站在箱子顶 / 任意路口记一条，人机就会把那里当成目标走过去。 */
  {
    extern int editor_pm_get(int idx, float* x, float* y, float* z);
    int k2, made3 = 0;
    for (k2 = 0; k2 < pmN; k2++) {
      float px, py, pz;
      P co, comp, ct;
      V3 cpos;
      if (!editor_pm_get(k2, &px, &py, &pz)) continue;
      co = i_object_new(g_goCls);
      if (!co) continue;
      ctor(co, nameStr, 0);
      comp = addComp(co, typeObj, 0);
      if (!comp) continue;
      ct = gtr(co, 0);
      cpos.x = px;
      cpos.y = py + 0.05f;
      cpos.z = pz;
      sp(ct, cpos, 0);
      made3++;
    }
    if (made3) nlog("crouch: player marks -> %d crouch points", made3);
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

/* ---- 动作 3：守卫区 ---- */
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
    purge_guard_areas();
    nlog("scene astar=%p (purge done, notify editor)", a);
    { void editor_gc_probe(void); editor_gc_probe(); }   /* gc_probe 调试开关 */
    { void editor_on_scene(void*); editor_on_scene((void*)a); }
    navfix_diag_graphs();
    nlog("scene astar=%p (editor notified)", a);
    {
      P pg0 = point_graph(a);
      { int editor_nogen(void);
        if (!editor_nogen() && pg0 && *(int*)((char*)pg0 + 0xEC) == 0) { nlog("scene change: running setup immediately"); run_setup(); } }
    }
  }
  pg = point_graph(a);
  nodes = pg ? *(int*)((char*)pg + 0xEC) : -1;
  if (pg && nodes == 0) {
    g_zeroStreak++;
    { int editor_nogen(void);
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
  { void navfix_hires_kick(void); navfix_hires_kick(); }   /* 采样定时器没起来就再补一次 */
}

static WNDPROC g_oldProc;
static HWND g_hwnd;
static volatile LONG g_buildCount;

HWND navfix_hwnd(void) { return g_hwnd; }

/* 录制 / 轨迹采集用的采样定时器（WM_TIMER 0xF3C1）。
 *
 * 采样入口只有两个：nav_tick() 的 4 Hz WM_UCF_TICK（editor_tick 里调
 * rec_tick/trace_tick）和这个 WM_TIMER。以前只有 UCF_FREECAM=1 才 SetTimer，
 * 所以控制台选 10/20/30/60 Hz 全都退化成 4 Hz（2026-11-24 的 trace 实测 4.0 Hz）。
 * 现在按需启停：rec/trace 开始时 +1 引用，最后一个停了 -1；车测自由视角共用。
 *
 * 周期用 10 ms（USER_TIMER_MINIMUM，再小 Windows 也只按 10 ms 给）而不是 1/hz：
 * WM_TIMER 只负责「给机会」，具体按 hz 取样本由 editor.c 的 QPC 闸门（g_trNextT）
 * 决定。机会给得比样本密，闸门才能把样本落在正确时刻；反过来（周期 ≥ 样本间隔）
 * 会变成「定时器多快就采多快」，档位就没意义了。
 *
 * WM_TIMER 只在游戏主循环泵消息时才会派发，所以实际上限 = 游戏帧率：
 * 60 fps 的机器 60 Hz 档能跑满，30 fps 的机器顶到 ~30 Hz（日志会喊没跑满）。 */
#define UCF_HI_TIMER_ID  0xF3C1
#define UCF_HI_PERIOD_MS 10

static int g_hiRefs;        /* rec/trace 正在用这个定时器的数量 */
static int g_hiTimer;       /* 定时器当前是否已启动 */
static int g_hiFreecam;     /* UCF_FREECAM=1：车测要求常驻 */
static volatile LONG g_hiTicks;   /* 0xF3C1 真的到过多少次：设了定时器 ≠ 它会来 */
static int g_hiRes;         /* timeBeginPeriod(1) 是否已生效 */

/* editor.c 用它算「这次采集到底有几个样本是定时器给的」 */
long navfix_hires_ticks(void) { return g_hiTicks; }

/* winmm 的 timeBeginPeriod(1)：把系统定时器精度提到 1 ms。不调的话默认 15.6 ms
 * 量子，SetTimer(10 ms) 实际 ~15.6 ms 一跳，60 Hz 档会一帧采一次、一帧漏一次。
 * 动态取地址：不用给 build.ps1 加 -lwinmm，DLL 的依赖面不变。 */
static void hi_timer_res(int on) {
  static HMODULE mm;
  UINT (WINAPI *fn)(UINT);
  if (on == g_hiRes) return;
  if (!mm) { mm = GetModuleHandleA("winmm.dll"); if (!mm) mm = LoadLibraryA("winmm.dll"); }
  if (!mm) return;
  fn = (UINT (WINAPI*)(UINT))GetProcAddress(mm, on ? "timeBeginPeriod" : "timeEndPeriod");
  if (!fn) return;
  fn(1);
  g_hiRes = on;
}

static void hi_timer_sync(void) {
  int want = (g_hiRefs > 0) || g_hiFreecam;
  if (!g_hwnd) return;              /* 窗口还没钩上：nav_tick 每 250 ms 会再试一次 */
  if (want && !g_hiTimer) {
    hi_timer_res(1);
    if (SetTimer(g_hwnd, UCF_HI_TIMER_ID, UCF_HI_PERIOD_MS, 0)) {
      g_hiTimer = 1;
      nlog("hires: on id=0x%X period=%dms timer_res=%d refs=%d freecam=%d",
           UCF_HI_TIMER_ID, UCF_HI_PERIOD_MS, g_hiRes, g_hiRefs, g_hiFreecam);
    } else {
      nlog("hires: SetTimer FAILED err=%lu (refs=%d freecam=%d) - 采样只能回落到 4 Hz",
           GetLastError(), g_hiRefs, g_hiFreecam);
    }
  } else if (!want && g_hiTimer) {
    KillTimer(g_hwnd, UCF_HI_TIMER_ID);
    g_hiTimer = 0;
    hi_timer_res(0);
    nlog("hires: off (ticks=%ld)", g_hiTicks);
  }
}

void navfix_hires_acquire(void) { g_hiRefs++; hi_timer_sync(); }
void navfix_hires_release(void) { if (g_hiRefs > 0) g_hiRefs--; hi_timer_sync(); }

/* 4 Hz 心跳顺带自愈：有的时序里 acquire() 比窗口钩子先到（g_hwnd 还是 0），
 * 那时 hi_timer_sync() 只能空转；这里每 250 ms 补一次，别让一次错过的时序
 * 变成整场 4 Hz。 */
void navfix_hires_kick(void) { if (!g_hiTimer) hi_timer_sync(); }

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
    { void autotest_tick(void); autotest_tick(); }   /* 只在 UCF_AUTOTEST 设了时动作 */
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
  if (msg == WM_TIMER && w == UCF_HI_TIMER_ID) {
    void editor_freecam_tick(void);
    void editor_compass_tick(void);
    void editor_rec_tick(void);
    void editor_spawn_tick(void);
    InterlockedIncrement(&g_hiTicks);   /* 诊断：这个定时器到底有没有在派发 */
    editor_freecam_tick();
    editor_compass_tick();      /* 方向罗盘跟着镜头转（函数内部节流到 ~30 Hz） */
    editor_rec_tick();          /* rec/trace 在这里按各自 hz 取样本（QPC 闸门） */
    /* 出生点：进房间时 MapManager 一就绪就写数组（≈15 ms 一跳）。
     * 等 4 Hz 的 editor_tick 或 navfix 的场景通知都太晚 —— 人机第一次出生已经过去了。 */
    editor_spawn_tick();
    return 0;
  }
  if (msg == WM_CHAR || msg == WM_SYSCHAR) {
    int editor_menu_is_open(void);
    if (editor_menu_is_open()) return 0;   /* 菜单模态：不再把字符送进游戏聊天框 */
  }
  if (msg == WM_KEYDOWN) {
    int ext = (l & 0x1000000) ? 1 : 0;
    int editor_menu_key(unsigned, int);
    int editor_menu_is_open(void);
    /* 菜单键 / F2 / 长按 E 先在插件里处理；返回 1 表示已消费，不再传游戏。 */
    if (editor_menu_key((unsigned)w, ext)) return 0;
    if (w == VK_DELETE) {
      void editor_delete_nearest(void);
      editor_delete_nearest();
    } else if (w == VK_F7) {
      void editor_freecam_toggle(void);
      editor_freecam_toggle();
    } else if (GetAsyncKeyState(VK_CONTROL) & 0x8000) {
      /* 菜单开着时 W/A/S/D 要留给游戏走路，所以「只按 Ctrl」的编辑器热键在菜单里不触发。
       * 但 Ctrl+Shift+字母 是编辑器专用组合（选 A 点 / 连边 / 落地…），菜单开着也必须能用：
       * 否则选 A 只剩「建立路径」第 1 步那一条路，而它一进主菜单就被清掉，
       * 跳跃点（要 A -> B 两个点）在菜单里根本建不出来（2026-11-20 用户现场）。 */
      int shift = (GetAsyncKeyState(VK_SHIFT) & 0x8000) ? 1 : 0;
      /* Ctrl+S = 唯一保存键（2026-11-25 用户要求）。菜单把 S 留给游戏走路，
       * 所以 editor_menu_key 不会消费它；这里不管菜单开没开都要放行，
       * 否则「开着菜单想保存」就按不出来。 */
      if (w == 'S' && !shift) {
        void editor_save_all(void);
        editor_save_all();
      } else if (!editor_menu_is_open() || shift) {
        void editor_on_key_mod(unsigned, int);
        editor_on_key_mod((unsigned)w, shift);
      }
    }
  }
  if (msg == WM_LBUTTONDOWN || msg == WM_RBUTTONDOWN) {
    int editor_menu_is_open(void);
    void editor_on_mouse(int);
    int open = editor_menu_is_open();
    editor_on_mouse(msg == WM_LBUTTONDOWN ? 1 : 2);
    /* 菜单开着时连右键也吞掉，避免右键瞄准/退出菜单被游戏接走 */
    if (open) return 0;
  }
  if (msg == WM_MOUSEWHEEL) {
    int editor_menu_is_open(void);
    if (editor_menu_is_open()) {
      void editor_menu_wheel(int);
      editor_menu_wheel((int)GET_WHEEL_DELTA_WPARAM(w));
      return 0;   /* 避免菜单开着时滚轮切枪 */
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
  {  /* 车测自由视角也共用这个采样定时器（10 ms）；录制/轨迹采集开启时由 navfix_hires_acquire() 启动 */
    char v[8];
    g_hiFreecam = (GetEnvironmentVariableA("UCF_FREECAM", v, sizeof v) > 0 && v[0] == '1');
    if (g_hiFreecam) nlog("freecam: hires timer requested");
    hi_timer_sync();
  }
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
  ucf_log_file(g_log, sizeof g_log, modDir, "ucf_mod.log");
  CreateThread(0, 0, nav_worker, 0, 0, 0);
}
