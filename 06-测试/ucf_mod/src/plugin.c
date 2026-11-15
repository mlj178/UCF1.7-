#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>

typedef void* P;
static HMODULE GA;
static char gDir[MAX_PATH];
static char gLog[MAX_PATH];
static int gGameMode = 6;
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

static P g_field;   /* UI_GameRoom singleton instance field */

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

static void read_config(const char* path) {
  FILE* f = fopen(path, "rb");
  if (!f) { logf_("config not found, using defaults"); return; }
  static char buf[65536];
  size_t n = fread(buf, 1, sizeof(buf)-1, f); fclose(f); buf[n] = 0;
  char* p = strstr(buf, "\"game_mode\"");
  if (p) { p = strchr(p, ':'); if (p) gGameMode = atoi(p+1); }
  p = strstr(buf, "\"scene\"");
  if (p) { p = strchr(p, ':'); if (p) { p = strchr(p, '"'); if (p) { p++; char* q = strchr(p, '"'); if (q && (size_t)(q-p) < sizeof(gScene)) { memcpy(gScene, p, q-p); gScene[q-p] = 0; } } } }
  p = strstr(buf, "\"label\"");
  if (p) { p = strchr(p, ':'); if (p) { p = strchr(p, '"'); if (p) { p++; char* q = strchr(p, '"'); if (q && (size_t)(q-p) < sizeof(gLabel)) { memcpy(gLabel, p, q-p); gLabel[q-p] = 0; } } } }
  logf_("config: scene=%s label=%s game_mode=%d", gScene, gLabel, gGameMode);
}

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
  P arr = *(P*)((char*)ma + 0x14);
  if (!arr) return 0;
  int n = *(int*)((char*)arr + 0xC);
  char* data = (char*)arr + 0x10;
  for (int i = 0; i < n; i++) if (str_eq_il2cpp(*(P*)(data + i*0x1C), gScene)) return 0;
  P klass = *(P*)arr;
  P elem = p_class_get_element_class(klass);
  P na = p_array_new(elem, n+1);
  if (!na) return 0;
  memcpy((char*)na + 0x10, data, n*0x1C);
  memcpy((char*)na + 0x10 + n*0x1C, data, 0x1C);
  *(P*)((char*)na + 0x10 + n*0x1C) = p_string_new(gScene);
  *(P*)((char*)na + 0x10 + n*0x1C + 4) = p_string_new(gLabel);
  p_wbarrier(ma, (char*)ma + 0x14, na);
  *(P*)((char*)ma + 0x14) = na;
  return n + 1;
}

/* runs on the game's main thread (posted from the inject worker) */
void plugin_tick(void) {
  P inst = 0;
  if (InterlockedCompareExchange(&g_appQuit, 0, 0)) return;
  if (!g_field) return;
  p_field_static_get_value(g_field, &inst);
  if (!inst) return;
  {
    P mapDatas = *(P*)((char*)inst + 0x2C);
    if (mapDatas) {
      int n = *(int*)((char*)mapDatas + 0xC);
      for (int i = 0; i < n; i++) {
        P ma = *(P*)((char*)mapDatas + 0x10 + i*4);
        if (!ma) continue;
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
    char path[MAX_PATH]; GetModuleFileNameA(h, path, MAX_PATH);
    char* p = strrchr(path, '\\'); if (p) *p = 0;
    strcpy(gDir, path);
    sprintf(gLog, "%s\\ucf_mod.log", gDir);
    DisableThreadLibraryCalls(h);
    CreateThread(0, 0, worker, 0, 0, 0);
    { void navfix_start(const char*); navfix_start(gDir); }
    { void editor_start(const char*); editor_start(gDir); }
  } else if (reason == DLL_PROCESS_DETACH) {
    InterlockedExchange(&g_appQuit, 1);
  }
  return TRUE;
}
