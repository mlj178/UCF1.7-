/* cfg.h - ucf_mod.json 的唯一读取器
 *
 * 2026-11-16: 之前 plugin.c 里有个 read_config() 但从来没被调用，
 * 于是整个 ucf_mod.json 是死的（enabled / scene / game_mode 全没生效）。
 * 现在所有开关都从这里出，并且 cfg_dump() 会在启动时把每一项打到日志，
 * 日志里看得见 "哪个开着、哪个关了"，不用猜。
 */
#pragma once

/* DllMain 里调用一次：定位 ucf_mod.json / ucf_mod.log，读进内存 */
void cfg_init(const char* modDir);

/* 开关查询。缺文件、缺字段、字段类型不对 -> 返回 def。 */
int  cfg_bool(const char* key, int def);
int  cfg_int(const char* key, int def);
void cfg_str(const char* key, const char* def, char* out, int n);

/* 把全部已知开关 + 当前值写进日志（启动时调用一次） */
void cfg_dump(void);

/* 已知开关表（cfg.c 定义），给 UI / 自检复用 */
typedef struct { const char* key; int def; const char* doc; } CFG_DEF;
const CFG_DEF* cfg_table(void);
