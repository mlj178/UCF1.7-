/* =====================================================================
 * 路点体检（waypoint probe）—— 05-正式功能/42-路点体检
 *
 * 没有热键：UI（AAAAA-waypoint_probe_ui.py）写命令文件，插件每 ~0.2 s 读一次，
 * 结果写成状态文件给 UI 显示；日志/报告落盘供事后分析。
 *
 *   ucf_mod\probe_cmd.ini      UI -> 插件（开关 / 参数 / 手动触发）
 *   ucf_mod\probe_status.txt   插件 -> UI（当前地图 / 统计 / 文件路径）
 *   ucf_mod\nav\probe_<fp>.txt        物理探针逐边结果
 *   ucf_mod\nav\botwalk_<fp>.log      人机位置/跨边样本
 *
 * 命令文件键（每行 key=value，# 开头是注释）：
 *   enabled=1          总开关
 *   pacify=1           停战（只关战斗，不动移动）
 *   walk=1             人机采样
 *   auto_probe=1       进图自动跑一次物理探针
 *   probe_once=<毫秒>  UI 点“跑一次”时写当前时间戳；插件发现变化就执行
 *   sample_ms=200      采样间隔
 * ===================================================================== */
#define PR_PASS  0
#define PR_BLOCK 1
#define PR_GAP   2
#define PR_STEP  3
#define PR_DROP  4
#define PR_STEEP 5
#define PR_MAXE  8000

typedef struct { int a, b; unsigned char v; } PREDGE;

static PREDGE g_pr[PR_MAXE];
static int g_prN;
static int g_prBots;
static P   g_prBotType;
static unsigned g_prTick;
static int g_prSeen[256];
static int g_prSeenN;
static int g_prInit;
static char g_prFp[48];
static char g_prFile[MAX_PATH];
static char g_prWalkFile[MAX_PATH];
static int g_prWalkReady;
static unsigned g_prSamples, g_prTraversals, g_prLinked0;
static char g_prAutoFp[48];

/* --- 配置（由 UI 写） -------------------------------------------------- */
typedef struct {
  int enabled, pacify, walk, auto_probe, sample_ms;
  unsigned long long probe_once;
} PRCFG;
static PRCFG g_prCfg = { 1, 1, 1, 1, 200, 0 };
static unsigned long long g_prOnceSeen;
static char g_prCfgPath[MAX_PATH];
static char g_prStatusPath[MAX_PATH];
static int g_prCfgReady;
static unsigned long long g_prCfgStamp;

static const char* pr_name(int v) {
  switch (v) {
  case PR_PASS:  return "PASS";
  case PR_BLOCK: return "BLOCK";
  case PR_GAP:   return "GAP";
  case PR_STEP:  return "STEP";
  case PR_DROP:  return "DROP";
  case PR_STEEP: return "STEEP";
  default:       return "?";
  }
}

static void pr_cfg_defaults(void) {
  sprintf(g_prCfgPath, "%s\\probe_cmd.ini", g_dir);
  sprintf(g_prStatusPath, "%s\\probe_status.txt", g_dir);
}

/* 读命令文件；文件不存在就写一份默认的，方便用户/UI 看有哪些开关 */
static void pr_cfg_read(void) {
  FILE* f;
  char line[256];
  PRCFG c = g_prCfg;
  if (!g_prCfgReady) pr_cfg_defaults();
  f = fopen(g_prCfgPath, "r");
  if (!f) {
    f = fopen(g_prCfgPath, "w");
    if (f) {
      fprintf(f, "# ucf 路点体检 开关（UI 会自动改这个文件）\n");
      fprintf(f, "enabled=1\npacify=1\nwalk=1\nauto_probe=1\nprobe_once=0\nsample_ms=200\n");
      fclose(f);
    }
    g_prCfgReady = 1;
    return;
  }
  while (fgets(line, sizeof(line), f)) {
    char* p = line;
    char k[32];
    int v;
    unsigned long long uv;
    while (*p == ' ' || *p == '\t') p++;
    if (*p == '#' || *p == '\n' || *p == '\r' || !*p) continue;
    if (sscanf(p, "%31[^=]=%d", k, &v) == 2) {
      if (!strcmp(k, "enabled")) c.enabled = v;
      else if (!strcmp(k, "pacify")) c.pacify = v;
      else if (!strcmp(k, "walk")) c.walk = v;
      else if (!strcmp(k, "auto_probe")) c.auto_probe = v;
      else if (!strcmp(k, "sample_ms")) { if (v >= 50 && v <= 5000) c.sample_ms = v; }
    } else if (sscanf(p, "%31[^=]=%llu", k, &uv) == 2) {
      if (!strcmp(k, "probe_once")) c.probe_once = uv;
    }
  }
  fclose(f);
  g_prCfg = c;
  g_prCfgReady = 1;
}

/* 状态文件：UI 每 1 s 读一次 */
static void pr_status_write(void) {
  FILE* f;
  int cnt[6], i;
  char mapname[80];
  P g;
  memset(cnt, 0, sizeof(cnt));
  for (i = 0; i < g_prN; i++) cnt[g_pr[i].v]++;
  map_name_from_minimap(mapname, sizeof(mapname));
  g = navfix_point_graph();
  f = fopen(g_prStatusPath, "w");
  if (!f) return;
  fprintf(f, "# ucf-probe-status v1\n");
  fprintf(f, "map=%s\n", mapname);
  fprintf(f, "fp=%s\n", g_prFp);
  fprintf(f, "nodes=%d\n", g ? nav_count(g) : 0);
  fprintf(f, "edges=%d\n", g_vnN ? g_veN : 0);
  fprintf(f, "probe_total=%d\n", g_prN);
  fprintf(f, "pass=%d\nblock=%d\ngap=%d\nstep=%d\ndrop=%d\nsteep=%d\n",
          cnt[PR_PASS], cnt[PR_BLOCK], cnt[PR_GAP], cnt[PR_STEP], cnt[PR_DROP], cnt[PR_STEEP]);
  fprintf(f, "enabled=%d\npacify=%d\nwalk=%d\nauto_probe=%d\n",
          g_prCfg.enabled, g_prCfg.pacify, g_prCfg.walk, g_prCfg.auto_probe);
  fprintf(f, "bots=%d\n", g_prBots);
  fprintf(f, "samples=%u\ntraversals=%u\nlinked0=%u\n", g_prSamples, g_prTraversals, g_prLinked0);
  fprintf(f, "probe_file=%s\n", g_prFile);
  fprintf(f, "walk_file=%s\n", g_prWalkFile);
  fprintf(f, "tick=%u\n", g_prTick);
  fclose(f);
}

/* 一次射线：命中返回 1，点写 hit、法线写 nrm */
static int pr_ray(V3 o, V3 d, float dist, V3* hit, V3* nrm) {
  char buf[128];
  raycast_t rc = (raycast_t)RVA(R_RAYCAST);
  if (!rc(o, d, buf, dist, 1, 0)) return 0;
  if (hit) *hit = *(V3*)buf;
  if (nrm) *nrm = *(V3*)(buf + 12);
  return 1;
}

/* 沿边：地面 + 体积（两档高度）判定 */
static int pr_check_edge(V3 A, V3 B, float* out_gmax, int* out_block, int* out_gap) {
  float dist, dx, dz, t, step;
  int ns, i, blocked = 0, gap = 0;
  float gmax = 0.0f;
  V3 hit, nrm, o, d;
  if (out_gmax) *out_gmax = 0.0f;
  if (out_block) *out_block = 0;
  if (out_gap) *out_gap = 0;
  dx = B.x - A.x; dz = B.z - A.z;
  dist = sqrtf(dx * dx + dz * dz);
  if (dist < 0.01f) return PR_PASS;
  ns = (int)(dist / 0.5f) + 2;
  if (ns > 16) ns = 16;
  step = dist / (float)(ns - 1);
  for (i = 0; i < ns; i++) {
    V3 p;
    t = (float)i / (float)(ns - 1);
    p.x = A.x + (B.x - A.x) * t;
    p.z = A.z + (B.z - A.z) * t;
    p.y = A.y + (B.y - A.y) * t;
    o.x = p.x; o.y = p.y + 1.6f; o.z = p.z;
    d.x = 0.0f; d.y = -1.0f; d.z = 0.0f;
    if (!pr_ray(o, d, 8.0f, &hit, &nrm)) { gap = 1; continue; }
    {
      float dh = hit.y - p.y;
      float adh = dh < 0 ? -dh : dh;
      if (adh > gmax) gmax = adh;
      if (nrm.y > 0.0f && nrm.y < 0.7071f && adh > 0.25f) blocked = 1;
    }
    if (i + 1 < ns) {
      V3 np, dir, rh, ro;
      float nd, len;
      int k;
      float hs[2];
      np.x = A.x + (B.x - A.x) * ((float)(i + 1) / (float)(ns - 1));
      np.z = A.z + (B.z - A.z) * ((float)(i + 1) / (float)(ns - 1));
      dir.x = np.x - p.x; dir.z = np.z - p.z; dir.y = 0.0f;
      nd = sqrtf(dir.x * dir.x + dir.z * dir.z);
      if (nd > 0.001f) {
        dir.x /= nd; dir.z /= nd;
        len = nd + 0.15f;
        hs[0] = 0.35f; hs[1] = 1.15f;
        for (k = 0; k < 2; k++) {
          ro.x = p.x; ro.y = hit.y + hs[k]; ro.z = p.z;
          if (pr_ray(ro, dir, len, &rh, 0)) {
            float dd = (rh.x - ro.x) * dir.x + (rh.z - ro.z) * dir.z;
            if (dd < nd - 0.20f) blocked = 1;
          }
        }
      }
    }
  }
  (void)step;
  if (out_gmax) *out_gmax = gmax;
  if (out_block) *out_block = blocked;
  if (out_gap) *out_gap = gap;
  if (blocked) return PR_BLOCK;
  if (gap) return PR_GAP;
  if (gmax > 0.75f) return PR_STEP;
  if (gmax > 0.35f) return PR_STEEP;
  return PR_PASS;
}

/* 画探针结果（4 个 Mesh） */
static void probe_draw(void) {
  int i, g;
  if (!g_prN) return;
  for (g = 0; g <= 3; g++) {
    int c = 0, slot = 5;
    bs_reset();
    for (i = 0; i < g_prN; i++) {
      int v = g_pr[i].v;
      int grp = (v == PR_PASS) ? 0 : (v == PR_BLOCK) ? 1 : (v == PR_GAP) ? 2 : 3;
      if (grp != g) continue;
      if (g_pr[i].a < 0 || g_pr[i].b < 0) continue;
      if (g_pr[i].a >= g_vnN || g_pr[i].b >= g_vnN) continue;
      bs_line(g_vn[g_pr[i].a].p, g_vn[g_pr[i].b].p, 0.07f);
      c++;
    }
    if (!c) continue;
    if (g == 0) slot = 5;
    else if (g == 1) slot = 1;
    else if (g == 2) slot = 14;
    else slot = 8;
    vis_flush_mesh(g == 0 ? "probe_pass" : (g == 1 ? "probe_block" : (g == 2 ? "probe_gap" : "probe_step")),
                   slot, c);
  }
}

/* 跑一次物理探针 */
static void probe_run(void) {
  int i, n, cnt[6];
  FILE* f;
  SYSTEMTIME st;
  char mapname[80];
  memset(cnt, 0, sizeof(cnt));
  g_prN = 0;
  if (!navfix_point_graph()) { elog("probe: no point graph (not in a match yet?)"); return; }
  if (!g_vnN || !g_veN) vis_rebuild();
  if (!g_veN) { elog("probe: 0 edges in graph, nothing to probe"); return; }
  GetLocalTime(&st);
  nav_fp(g_prFp, sizeof(g_prFp));
  {
    char nd[MAX_PATH];
    sprintf(nd, "%s\\nav", g_dir);
    CreateDirectoryA(nd, 0);
  }
  sprintf(g_prFile, "%s\\nav\\probe_%s.txt", g_dir, g_prFp);
  map_name_from_minimap(mapname, sizeof(mapname));
  f = fopen(g_prFile, "w");
  if (f) {
    fprintf(f, "# ucf-probe v1 fp=%s map=%s time=%04d-%02d-%02d %02d:%02d:%02d nodes=%d edges=%d\n",
            g_prFp, mapname, st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond,
            g_vnN, g_veN);
    fprintf(f, "# radius=0.35 height=1.70 sample=0.5m ground=down8m wall=0.35/1.15m\n");
  }
  n = g_veN;
  for (i = 0; i < n && g_prN < PR_MAXE; i++) {
    int a = g_ve[i].a, b = g_ve[i].b, v;
    float gmax = 0.0f;
    int blocked = 0, gap = 0;
    V3 A, B;
    if (a < 0 || b < 0 || a >= g_vnN || b >= g_vnN) continue;
    A = g_vn[a].p; B = g_vn[b].p;
    if (!g_vn[a].walk || !g_vn[b].walk) v = PR_BLOCK;
    else v = pr_check_edge(A, B, &gmax, &blocked, &gap);
    g_pr[g_prN].a = a; g_pr[g_prN].b = b; g_pr[g_prN].v = (unsigned char)v;
    g_prN++;
    cnt[v]++;
    if (f) {
      float ddx = B.x - A.x, ddz = B.z - A.z;
      fprintf(f, "E %d %d %.2f %.2f %.2f %.2f %.2f %.2f d=%.2f v=%s gmax=%.2f block=%d gap=%d\n",
              a, b, A.x, A.y, A.z, B.x, B.y, B.z,
              sqrtf(ddx * ddx + ddz * ddz), pr_name(v), gmax, blocked, gap);
    }
  }
  if (f) {
    fprintf(f, "# summary pass=%d block=%d gap=%d step=%d drop=%d steep=%d total=%d\n",
            cnt[PR_PASS], cnt[PR_BLOCK], cnt[PR_GAP], cnt[PR_STEP], cnt[PR_DROP], cnt[PR_STEEP], g_prN);
    fclose(f);
  }
  elog("probe: %d edges -> %s (pass=%d block=%d gap=%d step=%d drop=%d steep=%d)",
       g_prN, g_prFile, cnt[PR_PASS], cnt[PR_BLOCK], cnt[PR_GAP], cnt[PR_STEP], cnt[PR_DROP], cnt[PR_STEEP]);
  probe_draw();
  pr_status_write();
  hud_refresh();
}

static int probe_bots(P* out, int cap) {
  int n = 0, i, cnt;
  P arr;
  if (!g_prBotType) return 0;
  arr = ((find_objs_t)RVA(R_FINDOBJS))(g_prBotType, 1, 0);
  if (!arr) return 0;
  cnt = *(int*)((char*)arr + 0x0C);
  if (cnt > cap) cnt = cap;
  for (i = 0; i < cnt; i++) {
    P b = *(P*)((char*)arr + 0x10 + i * 4);
    if (b) out[n++] = b;
  }
  return n;
}

/* 停战：清目标 + 关转身 + 把重新搜索/攻击计时推到很远的将来 */
static void probe_pacify(void) {
  P bots[128];
  int n = probe_bots(bots, 128), i, cleared = 0;
  for (i = 0; i < n; i++) {
    P b = bots[i];
    if (*(P*)((char*)b + 0x2C)) { *(P*)((char*)b + 0x2C) = 0; cleared++; }
    *(unsigned char*)((char*)b + 0x30) = 0;
    *(float*)((char*)b + 0x38) = 1.0e9f;
    *(float*)((char*)b + 0x3C) = 1.0e9f;
  }
  g_prBots = n;
  if (cleared) elog("probe: pacify cleared %d bots (of %d)", cleared, n);
}

/* 人机采样 */
static void probe_walk_sample(void) {
  P bots[128];
  int n = probe_bots(bots, 128), i;
  P g = navfix_point_graph();
  FILE* f;
  if (!g) return;
  if (!g_prWalkReady) {
    SYSTEMTIME st;
    char mapname[80];
    GetLocalTime(&st);
    map_name_from_minimap(mapname, sizeof(mapname));
    sprintf(g_prWalkFile, "%s\\nav\\botwalk_%s.log", g_dir, g_prFp);
    f = fopen(g_prWalkFile, "w");
    if (f) {
      fprintf(f, "# ucf-botwalk v1 fp=%s map=%s time=%04d-%02d-%02d %02d:%02d:%02d nodes=%d\n",
              g_prFp, mapname, st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond,
              nav_count(g));
      fclose(f);
      g_prWalkReady = 1;
    }
  }
  f = fopen(g_prWalkFile, "a");
  if (!f) return;
  for (i = 0; i < n; i++) {
    V3 p;
    int nd = -1, k;
    if (!comp_pos(bots[i], &p)) continue;
    {
      float best = 1e18f;
      for (k = 0; k < nav_count(g); k++) {
        P node = nav_node(g, k);
        V3 q;
        float d;
        if (!node) continue;
        nav_pos(node, &q);
        d = nav_d2(&p, &q);
        if (d < best) { best = d; nd = k; }
      }
    }
    g_prSamples++;
    fprintf(f, "P t=%.3f bot=%d x=%.2f y=%.2f z=%.2f node=%d\n",
            (double)(GetTickCount() / 1000.0), i, p.x, p.y, p.z, nd);
    if (i < 256) {
      int prev = g_prSeen[i];
      if (prev >= 0 && prev != nd && prev < nav_count(g) && nd >= 0) {
        P pa = nav_node(g, prev), pb = nav_node(g, nd);
        int has = (pa && pb && nav_conn_has(pa, pb)) ? 1 : 0;
        g_prTraversals++;
        if (!has) g_prLinked0++;
        fprintf(f, "E t=%.3f bot=%d %d>%d linked=%d\n",
                (double)(GetTickCount() / 1000.0), i, prev, nd, has);
      }
      g_prSeen[i] = nd;
      if (i >= g_prSeenN) g_prSeenN = i + 1;
    }
  }
  fclose(f);
}

static void probe_summary(void) {
  int cnt[6], i;
  memset(cnt, 0, sizeof(cnt));
  for (i = 0; i < g_prN; i++) cnt[g_pr[i].v]++;
  elog("probe: summary edges=%d pass=%d block=%d gap=%d step=%d drop=%d steep=%d pacify=%d walk=%d bots=%d",
       g_prN, cnt[PR_PASS], cnt[PR_BLOCK], cnt[PR_GAP],
       cnt[PR_STEP], cnt[PR_DROP], cnt[PR_STEEP], g_prCfg.pacify, g_prCfg.walk, g_prBots);
}

static void probe_reset(void) {
  int i;
  g_prN = 0;
  g_prWalkReady = 0;
  g_prSamples = g_prTraversals = g_prLinked0 = 0;
  for (i = 0; i < 256; i++) g_prSeen[i] = -1;
  g_prSeenN = 0;
  g_prAutoFp[0] = 0;
}

/* 主线程 tick：读命令文件、停战、采样、状态落盘 */
static void probe_tick(void) {
  int i;
  g_prTick++;
  if (!g_prInit) { for (i = 0; i < 256; i++) g_prSeen[i] = -1; g_prInit = 1; }
  if (!g_prBotType) {
    P cls = find_cls("", "Bot");
    if (cls) g_prBotType = x_type_get_object(x_class_get_type(cls));
    if (g_prBotType) elog("probe: Bot type=%p", g_prBotType);
  }
  if ((g_prTick % 12) == 0) pr_cfg_read();
  if (g_prCfg.probe_once != g_prOnceSeen) {
    g_prOnceSeen = g_prCfg.probe_once;
    if (g_prCfg.enabled && g_prCfg.probe_once) probe_run();
  }
  if (!g_prCfg.enabled) {
    if ((g_prTick % 60) == 0) pr_status_write();
    return;
  }
  if (g_prCfg.pacify && !g_collectOnly && (g_prTick % 6) == 0) probe_pacify();
  if (g_prCfg.walk && (g_prTick % 12) == 0) probe_walk_sample();
  /* 进图自动跑一次（每张图一次） */
  if (g_prCfg.auto_probe && (g_prTick % 30) == 0) {
    P g = navfix_point_graph();
    if (g && !g_prN) {
      nav_fp(g_prFp, sizeof(g_prFp));
      if (strcmp(g_prFp, g_prAutoFp) != 0) {
        strcpy(g_prAutoFp, g_prFp);
        probe_run();
      }
    }
  }
  if ((g_prTick % 60) == 0) pr_status_write();
}
