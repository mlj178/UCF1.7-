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

/* ---------------------------------------------------------------- 日志目录
 * 2026-11-23：日志的主位置在**工程端** <工程>\log\ —— 控制台启动游戏时用环境变量
 * UCF_LOG_DIR 指过去，所以游戏目录里不会生成日志。查找顺序：
 *   1) UCF_LOG_DIR      控制台注入（日常都走这条）
 *   2) <modDir>\log\    没走控制台：手动启动 / 别人机器 / 独立测试
 *   3) <modDir>\        连 log\ 都建不出来（权限 / 路径异常）
 * 任何一步都不许静默失败：最差也得落在 modDir —— 日志是排错唯一的证据。
 * fopen 在父目录不存在时是**静默失败**，所以这里负责逐级建目录。
 *   ucf_log_dir()  : 拿日志目录。返回 2 = UCF_LOG_DIR，1 = <modDir>\log，0 = 回退 <modDir>
 *   ucf_log_file() : 拼 <日志目录>\<name>（ucf_mod.log / autotest.txt / player_marks.txt）
 */
void ucf_mkdir_p(const char* path);          /* 逐级建目录（跨盘、多层都行） */

/* 日志里打路径用：ANSI 路径（Win32 A 接口给的）转成 UTF-8，
 * 否则工程端路径带中文时，按 UTF-8 读日志会看到乱码。 */
void ucf_path_to_utf8(const char* ansi, char* out, int n);
int  ucf_log_dir(char* out, int n, const char* modDir);
int  ucf_log_file(char* out, int n, const char* modDir, const char* name);

/* 日志超过 16 MB 就把 ...\ucf_mod.log 改名成 ...\ucf_mod.prev.log（只保 1 代）。
 * 改名失败就照常往原文件写，不丢日志。 */
void ucf_log_rotate(const char* logPath);
