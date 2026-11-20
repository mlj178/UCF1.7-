/* cfg.c - ucf_mod.json 的唯一读取器（见 cfg.h）
 *
 * 设计取舍：不引进 JSON 库。配置结构固定、字段极少，用一次线性扫描找
 * "key" : true/false 就够了，也不会因为嵌套层级变化而失效。
 */
#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>
#include "cfg.h"

#define CFG_MAX 65536

static char g_path[MAX_PATH];
static char g_log[MAX_PATH];
static char g_buf[CFG_MAX];
static int  g_ok;          /* 文件读进来了 */

/* 顺序 = 日志里的打印顺序。doc 只给 UI 用，C 侧不打。 */
static const CFG_DEF g_defs[] = {
  { "enabled",        1, "总开关：关掉等于插件不动作" },
  { "hidden_map",     1, "往房间地图列表塞隐藏地图" },
  { "auto_waypoints", 1, "没路点的图自动铺路点 + 连线" },
  { "auto_crouch",    1, "没有蹲守点时自动补" },
  { "ghost_areas",    1, "凭空造幽灵守卫区" },
  { "visualizer",     0, "进图就画导航网格" },
  { "vis_nodes",      1, "可视化：路点 / 连线（PointNode / Connection）" },
  { "navmesh_show",   1, "画 A* 可走面（NavMeshGraph 三角网线框）" },
  { "vis_nano",       1, "名单 SpareAreaList：幽灵守区 + 幽灵守点" },
  { "vis_crouch",     1, "名单 SpareList_BL/GR：人类蹲守点（蓝/红）" },
  { "vis_guard",      1, "Bot_GuardArea / Bot_GuardPos：守卫区 + 守卫点" },
  { "vis_born",       1, "MapManager：幽灵出生 / 保卫者出生 / 中立点" },
  { "vis_supply",     1, "MapManager：补给箱 / 红箱 / 蓝箱" },
  { "vis_jump",       1, "Bot_JumpLink：跳点（不走名单）" },
  { "vis_tag",        1, "PointNodeTagModifier：标签区（不走名单）" },
  { "vis_player_marks", 1, "玩家坐标记录：本次进图手动记录的位置（金色方块 + 顺序折线）" },
  { "vis_compass",    1, "方向罗盘：屏幕下方汉字东南西北（独立于可视化总开关）" },
  { "export_enabled", 1, "Ctrl+E 导出总开关" },
  { "export_nodes",   1, "Ctrl+E 导出：路点 / 连线" },
  { "export_crouch",  1, "Ctrl+E 导出：人类蹲守点" },
  { "export_area",    1, "Ctrl+E 导出：幽灵守区 / 幽灵守点" },
  { "export_guard",   1, "Ctrl+E 导出：守卫区 / 守卫点" },
  { "export_spawn",   1, "Ctrl+E 导出：出生点 / 补给箱" },
  { "export_tags",    1, "Ctrl+E 导出：跳点 / 标签区" },
  { "editor",         1, "允许游戏内编辑（Ctrl+1）" },
  { "collect_only",   0, "只读采集：只导出，不改游戏" },
  { "wp_menu",        1, "游戏内路点菜单（F2 / 长按 E）" },
  { "wp_autoground",  1, "加点自动贴地（菜单加普通路点）" },
  { 0, 0, 0 }
};

const CFG_DEF* cfg_table(void) { return g_defs; }

static void cflog(const char* fmt, ...) {
  FILE* f;
  va_list ap;
  SYSTEMTIME st;
  if (!g_log[0]) return;
  f = fopen(g_log, "a");
  if (!f) return;
  GetLocalTime(&st);
  fprintf(f, "%04d-%02d-%02d %02d:%02d:%02d [cfg] ",
          st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond);
  va_start(ap, fmt);
  vfprintf(f, fmt, ap);
  va_end(ap);
  fprintf(f, "\n");
  fclose(f);
}

void cfg_init(const char* modDir) {
  FILE* f;
  size_t n;
  if (!modDir || !modDir[0]) return;
  sprintf(g_path, "%s\\ucf_mod.json", modDir);
  sprintf(g_log,  "%s\\ucf_mod.log",  modDir);
  g_ok = 0;
  g_buf[0] = 0;
  f = fopen(g_path, "rb");
  if (!f) { cflog("no config file (%s) - every switch falls back to its default", g_path); return; }
  n = fread(g_buf, 1, CFG_MAX - 1, f);
  fclose(f);
  g_buf[n] = 0;
  g_ok = 1;
}

/* 找到 "key" 后面的值起点；找不到返回 0。 */
static const char* find_value(const char* key) {
  char pat[96];
  const char* p;
  if (!g_ok || !key || !key[0]) return 0;
  sprintf(pat, "\"%s\"", key);
  p = g_buf;
  for (;;) {
    p = strstr(p, pat);
    if (!p) return 0;
    p += strlen(pat);
    while (*p == ' ' || *p == '\t' || *p == '\r' || *p == '\n') p++;
    if (*p != ':') continue;          /* 是别的字符串的一部分，继续找 */
    p++;
    while (*p == ' ' || *p == '\t' || *p == '\r' || *p == '\n') p++;
    return p;
  }
}

int cfg_bool(const char* key, int def) {
  const char* v = find_value(key);
  if (!v) return def;
  if (!strncmp(v, "true", 4))  return 1;
  if (!strncmp(v, "false", 5)) return 0;
  return def;
}

int cfg_int(const char* key, int def) {
  const char* v = find_value(key);
  if (!v) return def;
  if (*v != '-' && (*v < '0' || *v > '9')) return def;
  return atoi(v);
}

void cfg_str(const char* key, const char* def, char* out, int n) {
  const char* v = find_value(key);
  int i = 0;
  if (!out || n <= 0) return;
  if (!v || *v != '"') { if (def) { strncpy(out, def, n - 1); } out[n - 1] = 0; return; }
  v++;
  while (*v && *v != '"' && i < n - 1) out[i++] = *v++;
  out[i] = 0;
  if (!out[0] && def) { strncpy(out, def, n - 1); out[n - 1] = 0; }
}

void cfg_dump(void) {
  int i;
  char dirbuf[MAX_PATH];
  cflog("======== ucf_mod.json %s ========", g_ok ? "loaded" : "MISSING (defaults)");
  /* 字符串项（2026-11-18 四版分离）：空 = 用插件目录下的默认位置。
   * 控制台启动游戏时用环境变量覆盖，手改 ucf_mod.json 也能生效。 */
  cfg_str("export_dir", "", dirbuf, sizeof dirbuf);
  cflog("  %-14s = %s%s", "export_dir", dirbuf[0] ? dirbuf : "(plugin dir \\vis)",
        dirbuf[0] ? "" : "  (default)");
  cfg_str("pack_dir", "", dirbuf, sizeof dirbuf);
  cflog("  %-14s = %s%s", "pack_dir", dirbuf[0] ? dirbuf : "(plugin dir \\packs)",
        dirbuf[0] ? "" : "  (default)");
  for (i = 0; g_defs[i].key; i++) {
    const char* v = find_value(g_defs[i].key);
    int on;
    if (!strcmp(g_defs[i].key, "vis_labels")) {   /* 三态：0/1/2，别按 bool 打印 */
      cflog("  %-14s = %d%s", g_defs[i].key, cfg_int(g_defs[i].key, g_defs[i].def),
            v ? "" : "  (default)");
      continue;
    }
    on = cfg_bool(g_defs[i].key, g_defs[i].def);
    cflog("  %-14s = %-5s%s", g_defs[i].key, on ? "ON" : "off",
          v ? "" : (on == g_defs[i].def ? "  (default)" : ""));
  }
  cflog("=================================");
}
