/*
 * proxy.c —— winhttp.dll 代理外壳（UCF mod 的加载器）
 *
 * 为什么需要它：
 *   游戏（UnityPlayer）自己会 LoadLibrary("winhttp.dll")。我们把一个同名 DLL 放进
 *   游戏目录，Windows 的 DLL 搜索顺序会优先加载它；它再把 92 个导出原样转发给
 *   同目录的 winhttp_orig.dll（= 系统 winhttp 的副本），游戏完全察觉不到。
 *   在进程里"顺手"把 <游戏目录>\ucf_mod\ucf_mod.dll 载进来，插件就挂上了。
 *
 * 本文件来历（2026-11-22）：
 *   原件是 2026-11 中旬在仓库外编的，源码没进 git（06-测试/ucf_mod/.gitignore 有 *.dll），
 *   也没留 .c。2026-11-22 从游戏目录里的二进制反推复原：
 *     - 二进制未 strip，COFF 符号表 876 条，可见 _DllMain@12 / _loader@4 / 源文件名 proxy.c
 *     - 92 个导出在 PE Export Address Table 里全部是 "Forwarder RVA -- winhttp_orig.<同名>"
 *     - .text 仅 6144 字节，实质代码就是 DllMain + loader 两个函数
 *   复原后的源码文字不是原样（原始变量名/排版已不可知），但**行为与导出表等价**：
 *     导出 92/92 一致（见 winhttp.def）、加载路径一致、日志文字一致（从立即数逐字节还原）。
 *   逐一对应的证据见同目录 README.md。
 *
 * 编译：powershell -File build_proxy.ps1
 */
#include <windows.h>
#include <string.h>

#define MOD_DIR  "\\ucf_mod\\"
#define MOD_DLL  "ucf_mod.dll"
#define MOD_LOG  "ucf_mod.log"

/* 原始实现用的是一个 .bss 里的全局缓冲（地址 0x64546040），DllMain 只算一次。 */
static char g_dir[MAX_PATH];

static void join_path(char *out, unsigned cap, const char *dir_part, const char *tail) {
    unsigned n = 0;
    if (cap == 0) return;
    while (dir_part[n] && n + 1 < cap) { out[n] = dir_part[n]; n++; }
    while (*tail && n + 1 < cap) out[n++] = *tail++;
    out[n] = 0;
}

/* 原函数名就是 loader（stdcall，1 个参数），被 CreateThread 起来。
 * 失败时往 <游戏目录>\ucf_mod\ucf_mod.log 追加一行，成功则什么都不写。 */
static DWORD WINAPI loader(LPVOID unused) {
    char dll[MAX_PATH * 2];
    char log[MAX_PATH * 2];
    HANDLE h;
    DWORD written = 0;
    static const char msg[] = "proxy: failed to load plugin\r\n";

    (void)unused;

    Sleep(200);                     /* 原始值 0xc8：等游戏把目录结构准备好 */

    join_path(dll, sizeof dll, g_dir, MOD_DIR MOD_DLL);
    if (LoadLibraryA(dll)) return 0;   /* 载入成功：插件自己会打日志，这里不重复写 */

    join_path(log, sizeof log, g_dir, MOD_DIR MOD_LOG);
    h = CreateFileA(log, FILE_APPEND_DATA, FILE_SHARE_READ | FILE_SHARE_WRITE,
                    NULL, OPEN_ALWAYS, 0, NULL);
    if (h == INVALID_HANDLE_VALUE) return 0;

    SetFilePointer(h, 0, NULL, FILE_END);
    WriteFile(h, msg, sizeof msg - 1, &written, NULL);
    CloseHandle(h);
    return 0;
}

BOOL WINAPI DllMain(HINSTANCE inst, DWORD reason, LPVOID reserved) {
    char *slash;

    (void)reserved;

    /* 原始实现：非 DLL_PROCESS_ATTACH 直接返回 TRUE，不做任何清理。 */
    if (reason != DLL_PROCESS_ATTACH) return TRUE;

    /* 拿自身完整路径（本 DLL 就在游戏目录里），截掉文件名得到游戏目录。 */
    GetModuleFileNameA(inst, g_dir, MAX_PATH);
    slash = strrchr(g_dir, '\\');
    if (slash) *slash = 0;

    DisableThreadLibraryCalls(inst);
    CreateThread(NULL, 0, loader, NULL, 0, NULL);   /* 不在 DllMain 里做重活 */
    return TRUE;
}
