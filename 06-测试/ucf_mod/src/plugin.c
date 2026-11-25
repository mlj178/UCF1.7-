#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>
#include "cfg.h"

typedef void* P;
static HMODULE GA;
static char gDir[MAX_PATH];
static char gLog[MAX_PATH];
static int gGameMode = 6;
static int g_hiddenMap = 1;   /* cfg: features.hidden_map */
static char gScene[128] = "Nano30_Storm";
static char gLabel[256] = "隐藏地图 暴风";

extern volatile LONG g_appQuit;
extern HWND navfix_hwnd(void);

static P (*p_domain_get)(void);
static P (*p_domain_get_assemblies)(P, int*);
static P (*p_assembly_get_image)(P);
static const char* (*p_image_get_name)(P);
static P (*p_class_from_name)(P, const char*, const char*);
static P (*p_class_get_parent)(P);
static P (*p_class_get_field_from_name)(P, const char*);
static P (*p_field_static_get_value)(P, void*);
static P (*p_array_new)(P, unsigned int);
static P (*p_class_get_element_class)(P);
static P (*p_string_new)(const char*);
static void (*p_wbarrier)(P, P, P);
static P (*p_thread_attach)(P);
static void (*p_runtime_class_init)(P);
static P (*p_gchandle_new)(P, unsigned char);
static void (*p_gchandle_free)(P);

static P g_field;   /* UI_GameRoom singleton instance field */

/* UnityEngine.Object.m_CachedPtr; destroyed components leave a fake-null
 * managed wrapper.  Touching one from native code raises a managed
 * MissingReferenceException and aborts the process. */
static int p_live(P o) { return o && *(P*)((char*)o + 0x8) != 0; }

static void logf_(const char* fmt, ...) {
  FILE* f = fopen(gLog, "a");
  if (!f) return;
  SYSTEMTIME st; GetLocalTime(&st);
  fprintf(f, "%04d-%02d-%02d %02d:%02d:%02d ", st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond);
  va_list ap; va_start(ap, fmt); vfprintf(f, fmt, ap); va_end(ap);
  fprintf(f, "\n"); fclose(f);
}

static int str_eq_il2cpp(P s, const char* ascii) {
  if (!s) return 0;
  int len = *(int*)((char*)s + 8);
  unsigned short* ch = (unsigned short*)((char*)s + 12);
  int i = 0;
  for (; i < len && ascii[i]; i++) if (ch[i] != (unsigned char)ascii[i]) return 0;
  return (i == len && ascii[i] == 0);
}

/* 配置读取统一走 cfg.c（2026-11-16 之前这里的 read_config 从没被调用过，
 * 所以 ucf_mod.json 整个文件是死的）。 */

static P find_image(const char* name) {
  int n = 0;
  P arr = p_domain_get_assemblies(p_domain_get(), &n);
  for (int i = 0; i < n; i++) {
    P asm_ = *(P*)((char*)arr + 0x10 + i*4);
    P img;
    if (!asm_) break;
    img = p_assembly_get_image(asm_);
    if (img && strcmp(p_image_get_name(img), name) == 0) return img;
  }
  return 0;
}

static int inject_one(P ma) {
  P arr, klass, elem, na, sScene, sLabel;
  P hna = 0, hs = 0, hl = 0;
  int n, i;
  char* data;
  if (!p_live(ma)) return 0;
  arr = *(P*)((char*)ma + 0x14);
  if (!arr) return 0;
  n = *(int*)((char*)arr + 0xC);
  data = (char*)arr + 0x10;
  for (i = 0; i < n; i++) if (str_eq_il2cpp(*(P*)(data + i*0x1C), gScene)) return 0;

  /* Strings/arrays are managed objects held only in native locals here.  Root
   * them across the next allocations: a GC in p_array_new/p_string_new would
   * otherwise free them and the MapAsset field would point at dead memory,
   * which crashes the next GC (0xC0000005 in GameAssembly GC mark). */
  sScene = p_string_new(gScene);
  if (p_gchandle_new) hs = (P)p_gchandle_new(sScene, 0);
  sLabel = p_string_new(gLabel);
  if (p_gchandle_new) hl = (P)p_gchandle_new(sLabel, 0);

  klass = *(P*)arr;
  elem = p_class_get_element_class(klass);
  na = p_array_new(elem, n+1);
  if (!na) {
    if (hs && p_gchandle_free) p_gchandle_free(hs);
    if (hl && p_gchandle_free) p_gchandle_free(hl);
    return 0;
  }
  if (p_gchandle_new) hna = (P)p_gchandle_new(na, 0);
  /* 新数组必须真有 n+1 个 MapAsset.Map（每个 0x1C）槽位，否则下面的 memcpy
   * 会写出界，把托管堆写花。 */
  if (*(int*)((char*)na + 0xC) != n + 1) {
    logf_("!!! inject: array len mismatch %d != %d - skipped", *(int*)((char*)na + 0xC), n + 1);
    if (hna && p_gchandle_free) p_gchandle_free(hna);
    if (hl && p_gchandle_free) p_gchandle_free(hl);
    if (hs && p_gchandle_free) p_gchandle_free(hs);
    return 0;
  }

  memcpy((char*)na + 0x10, data, n*0x1C);
  memcpy((char*)na + 0x10 + n*0x1C, data, 0x1C);
  *(P*)((char*)na + 0x10 + n*0x1C) = sScene;
  *(P*)((char*)na + 0x10 + n*0x1C + 4) = sLabel;
  p_wbarrier(ma, (char*)ma + 0x14, na);
  *(P*)((char*)ma + 0x14) = na;

  if (hna && p_gchandle_free) p_gchandle_free(hna);
  if (hl && p_gchandle_free) p_gchandle_free(hl);
  if (hs && p_gchandle_free) p_gchandle_free(hs);
  return n + 1;
}

/* runs on the game's main thread (posted from the inject worker) */
void plugin_tick(void) {
  P inst = 0;
  if (InterlockedCompareExchange(&g_appQuit, 0, 0)) return;
  if (!g_field) return;
  if (!g_hiddenMap) return;          /* cfg: hidden_map = off */
  p_field_static_get_value(g_field, &inst);
  if (!p_live(inst)) return;
  {
    P mapDatas = *(P*)((char*)inst + 0x2C);
    if (mapDatas) {
      int n = *(int*)((char*)mapDatas + 0xC);
      for (int i = 0; i < n; i++) {
        P ma = *(P*)((char*)mapDatas + 0x10 + i*4);
        if (!p_live(ma)) continue;
        int gm = *(int*)((char*)ma + 0xC);
        if (gGameMode >= 0 && gm != gGameMode) continue;
        int r = inject_one(ma);
        if (r) logf_("injected into MapAsset %p (mode=%d) -> %d entries", ma, gm, r);
      }
    }
  }
}

static DWORD WINAPI worker(LPVOID x) {
  for (int i = 0; i < 600; i++) {
    GA = GetModuleHandleA("GameAssembly.dll");
    if (GA) break;
    Sleep(200);
  }
  if (!GA) { logf_("GameAssembly not found"); return 0; }
  logf_("GameAssembly=%p", GA);
#define RE(name) do { *(void**)&p_##name = GetProcAddress(GA, "il2cpp_" #name); if (!p_##name) logf_("missing " #name); } while(0)
  RE(domain_get); RE(domain_get_assemblies); RE(assembly_get_image); RE(image_get_name);
  RE(class_from_name); RE(class_get_parent); RE(class_get_field_from_name);
  RE(field_static_get_value); RE(array_new); RE(class_get_element_class);
  RE(string_new); RE(thread_attach);
  RE(gchandle_new); RE(gchandle_free);
  { FARPROC p = GetProcAddress(GA, "il2cpp_gc_wbarrier_set_field"); p_wbarrier = (void(*)(P,P,P))p; if (!p) logf_("missing wbarrier"); }
  { FARPROC p = GetProcAddress(GA, "il2cpp_runtime_class_init"); p_runtime_class_init = (void(*)(P))p; }
#undef RE
  for (int i = 0; i < 300; i++) { if (p_domain_get && p_domain_get()) break; Sleep(200); }
  if (!p_domain_get || !p_domain_get()) { logf_("domain not ready"); return 0; }
  p_thread_attach(p_domain_get());
  P img = 0;
  for (int k = 0; k < 300; k++) { img = find_image("Assembly-CSharp.dll"); if (img) break; Sleep(200); }
  if (!img) { logf_("Assembly-CSharp not found"); return 0; }
  P uiCls = 0;
  for (int k = 0; k < 300 && !uiCls; k++) { uiCls = p_class_from_name(img, "", "UI_GameRoom"); if (!uiCls) Sleep(200); }
  if (!uiCls) { logf_("UI_GameRoom not found"); return 0; }
  P base = p_class_get_parent(uiCls);
  logf_("UI_GameRoom=%p base=%p", uiCls, base);
  const char* names[] = {"<instance>k__BackingField", "instance", "_instance", "m_Instance"};
  for (int i = 0; i < 4 && !g_field; i++) g_field = p_class_get_field_from_name(base, names[i]);
  if (!g_field) { logf_("singleton instance field not found"); return 0; }
  if (p_runtime_class_init) p_runtime_class_init(base);
  logf_("inject: waiting for lobby (main-thread ticks)");

  for (;;) {
    HWND h;
    if (InterlockedCompareExchange(&g_appQuit, 0, 0)) { logf_("quit: inject worker stop"); break; }
    h = navfix_hwnd();
    if (h) PostMessageA(h, WM_APP + 0x54, 0, 0);
    Sleep(1000);
  }
  return 0;
}

BOOL APIENTRY DllMain(HMODULE h, DWORD reason, LPVOID reserved) {
  if (reason == DLL_PROCESS_ATTACH) {
    /* ---- 通行证 ----
     * 只有从「UCF 控制台」启动游戏时，父进程才会把这枚环境变量递进来。
     * 直接双击 UnityCrossFire.exe：这里立刻返回 —— 不起线程、不读配置、
     * 不写日志、不装窗口钩子。游戏行为和原版一致。
     * （加载器 winhttp.dll 仍然会被加载，它只做纯转发，不会碰 ucf_mod.dll 以外的东西） */
    {
      char gate[8];
      DWORD n = GetEnvironmentVariableA("UCF_MOD", gate, sizeof(gate));
      if (n == 0 || gate[0] != '1') return TRUE;   /* 原版模式：到此为止 */
    }
    char path[MAX_PATH]; GetModuleFileNameA(h, path, MAX_PATH);
    char* p = strrchr(path, '\\'); if (p) *p = 0;
    /* 2026-11-25：开发直读时 DLL 在工程 run\build，但配置/数据根仍应指向
     * 部署端 <游戏目录>\ucf_mod；控制台启动时注入 UCF_MOD_DIR。没注入才用 DLL 目录。 */
    {
      char over[MAX_PATH];
      DWORD n = GetEnvironmentVariableA("UCF_MOD_DIR", over, sizeof over);
      strcpy(gDir, (n > 0 && over[0]) ? over : path);
    }
    /* 2026-11-23：日志主位置在工程端（控制台注入 UCF_LOG_DIR）；没注入就落
     * <modDir>\log\；再不行退回 <modDir> —— 三步都不许静默丢日志。 */
    ucf_log_file(gLog, sizeof gLog, gDir, "ucf_mod.log");
    ucf_log_rotate(gLog);
    {
      /* 排查先看这一行：日志在哪、走的哪一级、这次是哪个部署 */
      char _ld[MAX_PATH];
      char _ldu[MAX_PATH * 4], _gdu[MAX_PATH * 4];
      int _kind = ucf_log_dir(_ld, sizeof _ld, gDir);
      ucf_path_to_utf8(_ld, _ldu, sizeof _ldu);
      ucf_path_to_utf8(gDir, _gdu, sizeof _gdu);
      logf_("log: dir=%s env=%d fallback=%d mod=%s", _ldu,
            _kind == 2 ? 1 : 0, _kind == 0 ? 1 : 0, _gdu);
    }
    DisableThreadLibraryCalls(h);

    /* 配置必须最先读：三个子系统启动时都要看开关 */
    cfg_init(gDir);
    cfg_dump();
    cfg_str("scene", "Nano30_Storm", gScene, sizeof(gScene));
    cfg_str("label", "隐藏地图 暴风", gLabel, sizeof(gLabel));
    gGameMode = cfg_int("game_mode", 6);
    g_hiddenMap = cfg_bool("hidden_map", 1);
    logf_("config: scene=%s label=%s game_mode=%d hidden_map=%d",
          gScene, gLabel, gGameMode, g_hiddenMap);

    if (!cfg_bool("enabled", 1)) {
      logf_("master switch OFF (enabled=false) - loaded but idle, nothing will run");
      return TRUE;
    }

    CreateThread(0, 0, worker, 0, 0, 0);
    { void navfix_start(const char*); navfix_start(gDir); }
    { void editor_start(const char*); editor_start(gDir); }
  } else if (reason == DLL_PROCESS_DETACH) {
    InterlockedExchange(&g_appQuit, 1);
  }
  return TRUE;
}
