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
  { "auto_export",    1, "进图稳定后自动导出路点 JSON" },
  { "hud",            1, "进图显示状态面板" },
  { "hud_states",     0, "HUD 第一行：可视化/五层/标签的开关状态（默认不显示）" },
  { "hud_keys",       0, "HUD 快捷键帮助块（默认不显示；Ctrl+H 可临时叫出）" },
  { "hud_log",        1, "HUD 显示导出结果与最近 3 行日志（Ctrl+M）" },
  { "visualizer",     0, "进图就画导航网格" },
  { "vis_layer_a",    1, "可视化 A 层：路点/连线（Ctrl+Shift+1）" },
  { "vis_layer_b",    1, "可视化 B 层：人类蹲守（Ctrl+Shift+2）" },
  { "vis_layer_c",    1, "可视化 C 层：幽灵守区（Ctrl+Shift+3）" },
  { "vis_layer_d",    1, "可视化 D 层：出生点/补给箱（Ctrl+Shift+4）" },
  { "vis_layer_e",    1, "可视化 E 层：模式（Ctrl+Shift+5）" },
  { "vis_labels",     0, "可视化文字标签：0 关 / 1 近距 35m / 2 全部（Ctrl+Shift+L）" },
  { "navmesh_show",   1, "画 A* 可走面（NavMeshGraph 三角网线框）" },
  { "vis_lists",      1, "读游戏自己的组件表（守区/蹲守/出生点）：崩溃时可关" },
  { "editor",         1, "允许游戏内编辑（Ctrl+1）" },
  { "collect_only",   0, "只读采集：只导出，不改游戏" },
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
  cflog("======== ucf_mod.json %s ========", g_ok ? "loaded" : "MISSING (defaults)");
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
