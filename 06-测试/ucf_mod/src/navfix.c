// navfix.c - A* PointGraph waypoints + missing AI markers for the hidden map.
// 2026-11-15: exit gate + main-thread il2cpp; spawn node coverage; runtime ghost guard areas.
#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>

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
  return v;
}

static P point_graph(P astar) {
  if (!astar) return 0;
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
  return v;
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
  i_runtime_invoke(g_listCtor, list, 0, 0);
  wfield(comp, 0x10, list);                       /* posList (non-null, Awake iterates it) */

  nameStr = i_string_new("UCF_GuardPos");
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
  if (madePos == 0) { nlog("area: no pos created"); return 0; }

  set_pos_of(go, p);
  ((set_active_t)RVA(0x331CF0))(go, 1, 0);        /* Awake: fills refs + registers area */
  for (i = 0; i < madePos; i++) ((set_active_t)RVA(0x331CF0))(posgo[i], 1, 0);
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
  for (i = 0; i < n; i++) {
    P o = *(P*)((char*)items + 0x10 + i*4);
    if (o && *(P*)((char*)o + 0x8)) *(P*)((char*)items + 0x10 + w++) = o;
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
    P esc = arr_new(g_areaCls, 2);
    if (!arr) continue;
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
  }
  nlog("guard areas: neighbour links set for %d areas", n);
}

static int g_graphOurs;   /* 1 = build_waypoints generated the current graph */
static int g_collectOnly; /* 1 = 只读采集：不改动游戏里的任何状态 */
int  navfix_collect_only(void) { return g_collectOnly; }
void navfix_set_collect_only(int on) { g_collectOnly = on ? 1 : 0; nlog("collect-only %s", on ? "ON" : "OFF"); }

static void build_waypoints(void) {
  if (InterlockedCompareExchange(&g_appQuit, 0, 0)) return;
  if (g_collectOnly) { nlog("readonly: skip build (collect-only)"); return; }
  P astar = astar_active();
  if (!astar) { nlog("no AstarPath.active"); return; }
  P pg = point_graph(astar);
  if (!pg) { nlog("no PointGraph in scene"); return; }
  int before = *(int*)((char*)pg + 0xEC);
  if (before > 0) { nlog("point graph already has %d nodes, skip", before); return; }
  if (!g_goCls) { nlog("GameObject class missing"); return; }
  hold_bots(1);

  raycast_t rc = (raycast_t)RVA(0xABB0A0);
  char hit[96];
  float minX = 1e9f, maxX = -1e9f, minZ = 1e9f, maxZ = -1e9f;
  int ch = 0;
  for (float x = -250.0f; x <= 250.0f; x += 20.0f)
    for (float z = -250.0f; z <= 250.0f; z += 20.0f) {
      V3 o = { x, 300.0f, z }, d = { 0.0f, -1.0f, 0.0f };
      if (!rc(o, d, hit, 700.0f, 1, 0)) continue;
      if (*(float*)(hit + 16) < 0.6f) continue;
      ch++;
      float hx = *(float*)hit, hz = *(float*)(hit + 8);
      if (hx < minX) minX = hx; if (hx > maxX) maxX = hx;
      if (hz < minZ) minZ = hz; if (hz > maxZ) maxZ = hz;
    }
  nlog("coarse hits=%d bounds x[%.1f,%.1f] z[%.1f,%.1f]", ch, minX, maxX, minZ, maxZ);
  if (ch < 8) { nlog("too few ground hits, retry later"); hold_bots(0); return; }

  ctor_str_t ctor = (ctor_str_t)RVA(0x331EA0);
  get_tr_t gtr = (get_tr_t)RVA(0x332010);
  set_pos_t sp = (set_pos_t)RVA(0x3F4840);
  set_parent_t sparent = (set_parent_t)RVA(0x3F3AB0);

  P root = i_object_new(g_goCls);
  ctor(root, i_string_new("UCF_WayPoints"), 0);
  P rootTr = gtr(root, 0);
  V3 zero = { 0, 0, 0 };
  sp(rootTr, zero, 0);

  P childName = i_string_new("wp");
  int made = 0;
  g_nspots = 0;
  /* Multi-layer sampling: a single downward ray from y=300 hits the roof first,
   * which put most nodes on rooftops and left interiors (the ghost spawn cave)
   * without any node. Cast again just below each surface, up to 5 layers. */
  for (float x = minX - 4.0f; x <= maxX + 4.0f; x += 4.0f)
    for (float z = minZ - 4.0f; z <= maxZ + 4.0f; z += 4.0f) {
      V3 d = { 0.0f, -1.0f, 0.0f };
      float y = 300.0f;
      for (int layer = 0; layer < 5; layer++) {
        V3 o = { x, y, z };
        P c, t;
        V3 pos;
        if (!rc(o, d, hit, 700.0f, 1, 0)) break;
        if (*(float*)(hit + 16) < 0.65f) break;
        c = i_object_new(g_goCls);
        ctor(c, childName, 0);
        t = gtr(c, 0);
        pos.x = *(float*)hit;
        pos.y = *(float*)(hit + 4) + 0.2f;
        pos.z = *(float*)(hit + 8);
        /* y=39..57 surfaces are skybox/ceiling colliders, not walkable map area */
        if (pos.y < -30.0f || pos.y > 15.0f) {
          y = *(float*)(hit + 4) - 1.5f;
          if (y < -80.0f) break;
          continue;
        }
        sp(t, pos, 0);
        sparent(t, rootTr, 0, 0);
        /* guard areas only on real ground: high spots made ghosts try to fly */
        if ((made % 11) == 0 && g_nspots < 64 && pos.y > -3.0f && pos.y < 9.0f) g_spots[g_nspots++] = pos;
        made++;
        y = *(float*)(hit + 4) - 1.5f;
        if (y < -80.0f) break;
      }
    }
  nlog("waypoint objects created=%d", made);
  if (made < 8) { nlog("waypoints too few, abort"); hold_bots(0); return; }

  /* nodes on the map's own spawn points: guarantees Bot.Update's start node is non-null */
  add_spawn_nodes(rootTr);

  if (i_wbarrier) i_wbarrier(pg, (char*)pg + 0xB8, rootTr);
  *(P*)((char*)pg + 0xB8) = rootTr;

  /* ---- AI 行为点位：蹲守点 (Bot_CrouchPos) ---- */
  if (g_crouchCls && i_class_get_type && i_type_get_object) {
    P spareField = i_class_get_field_from_name(g_crouchCls, "SpareList_BL");
    P spareList = 0;
    if (spareField) i_field_static_get_value(spareField, &spareList);
    int existing = spareList ? *(int*)((char*)spareList + 0xC) : -1;
    {
      extern int editor_crouch_made(void);
      int own = editor_crouch_made();
      nlog("crouch: existing SpareList_BL count=%d (editor-made=%d)", existing, own);
      if (existing > 0 && own > 0) existing -= own;
    }
    if (existing <= 0) {
      P typeObj = i_type_get_object(i_class_get_type(g_crouchCls));
      addcomp_t addComp = (addcomp_t)RVA(0x331A90);
      P nameStr = i_string_new("CrouchPos");
      int made2 = 0;
      for (float cx = minX - 2.0f; cx <= maxX + 2.0f; cx += 9.0f)
        for (float cz = minZ - 2.0f; cz <= maxZ + 2.0f; cz += 9.0f) {
          V3 o = { cx, 300.0f, cz }, d = { 0.0f, -1.0f, 0.0f };
          if (!rc(o, d, hit, 700.0f, 1, 0)) continue;
          if (*(float*)(hit + 16) < 0.8f) continue;
          P co = i_object_new(g_goCls);
          ctor(co, nameStr, 0);
          P comp = addComp(co, typeObj, 0);
          if (!comp) continue;
          P ct = gtr(co, 0);
          V3 cpos = { *(float*)hit, *(float*)(hit + 4) + 0.05f, *(float*)(hit + 8) };
          sp(ct, cpos, 0);
          made2++;
        }
      P spareList2 = 0;
      if (spareField) i_field_static_get_value(spareField, &spareList2);
      int now = spareList2 ? *(int*)((char*)spareList2 + 0xC) : -1;
      nlog("crouch: created=%d registered=%d", made2, now);
    }
  }

  *(float*)((char*)pg + 0xC0) = 4.6f;   /* maxDistance: 4m grid connects, 5m+ floor gaps do not */
  /* Distance-only connections link nodes through walls/ceilings, so A* sends the
   * ghost straight into a wall. PointGraph.raycast makes ConnectNodes linecast
   * between nodes and drop blocked pairs. */
  *(unsigned char*)((char*)pg + 0xD0) = 1;   /* raycast */
  *(unsigned char*)((char*)pg + 0xD2) = 0;   /* thickRaycast */
  *(int*)((char*)pg + 0xDC) = -1;            /* mask: everything */

  scan_t scan = (scan_t)RVA(0x581640);
  scan(pg, 0);
  nlog("scan done: nodes=%d (was %d)", *(int*)((char*)pg + 0xEC), before);
  g_graphOurs = 1;

  {
    typedef void (*connect_t)(P, void*);
    connect_t connectNodes = (connect_t)RVA(0x5EE8E0);
    connectNodes(pg, 0);
    P nodes = *(P*)((char*)pg + 0xE8);
    int cnt2 = nodes ? *(int*)((char*)nodes + 0xC) : 0;
    int withLinks = 0, totalLinks = 0, sampleN = cnt2 < 300 ? cnt2 : 300;
    for (int i = 0; i < sampleN; i++) {
      P nd = *(P*)((char*)nodes + 0x10 + i*4);
      if (!nd) continue;
      P cc = *(P*)((char*)nd + 0x20);
      if (cc) { int L = *(int*)((char*)cc + 0xC); if (L > 0) withLinks++; totalLinks += L; }
    }
    nlog("connected: sampled=%d withLinks=%d totalLinks=%d", sampleN, withLinks, totalLinks);
  }

  /* ---- 幽灵守卫区: the hidden map has none at all, so every ghost just idles ---- */
  if (g_areaCls && g_posCls && g_vec3Cls && g_listCls && g_listCtor && g_listAdd) {
    int madeA = 0;
    g_madeAreas = 0;
    for (int i = 0; i < g_nspots && g_madeAreas < 64; i++) {
      P comp = make_guard_area(g_spots[i], 1 + (i % 2));
      if (comp) { g_areaComps[g_madeAreas++] = comp; madeA++; }
    }
    link_guard_areas();
    P f = i_class_get_field_from_name(g_areaCls, "SpareAreaList");
    P list = 0;
    if (f) i_field_static_get_value(f, &list);
    nlog("guard areas: created=%d spots=%d SpareAreaList=%d", madeA, g_nspots, list ? *(int*)((char*)list + 0xC) : -1);
  } else {
    nlog("guard areas: classes missing area=%p pos=%p vec3=%p list=%p", g_areaCls, g_posCls, g_vec3Cls, g_listCls);
  }
  hold_bots(0);
  { void editor_mark_dirty(void); editor_mark_dirty(); }
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
    nlog("scene astar=%p (purge start)", a);
    if (!g_collectOnly) purge_guard_areas();
    nlog("scene astar=%p (purge done, notify editor)", a);
    { void editor_on_scene(void*); editor_on_scene((void*)a); }
    nlog("scene astar=%p (editor notified)", a);
    {
      P pg0 = point_graph(a);
      if (!g_collectOnly && pg0 && *(int*)((char*)pg0 + 0xEC) == 0) { nlog("scene change: building immediately"); build_waypoints(); }
    }
  }
  pg = point_graph(a);
  nodes = pg ? *(int*)((char*)pg + 0xEC) : -1;
  if (pg && nodes == 0) {
    g_zeroStreak++;
    if (g_collectOnly) {
      if ((g_zeroStreak % 20) == 0) nlog("collect-only: graph still empty (~%.0f s)", g_zeroStreak * 0.25f);
    } else if (g_zeroStreak == 4 || (g_zeroStreak > 4 && (g_zeroStreak % 10) == 0)) {
      build_waypoints();
    }
  } else if (!pg) {
    g_zeroStreak++;
    if ((g_zeroStreak % 8) == 0) nlog("waiting for PointGraph (tick %d)", g_zeroStreak);
  } else {
    g_zeroStreak = 0;
  }
  { void editor_tick(void); editor_tick(); }
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
    build_waypoints();
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
