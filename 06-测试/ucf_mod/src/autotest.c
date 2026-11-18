/* autotest.c -- 无人值守「进图」自测：不依赖鼠标键盘，把游戏自己切到指定关卡场景。
 *
 * 为什么需要它：2026-11-17 的闪退只在「进沙漠要塞 / 新寂静村」时出现，而 DSH 会话里
 * 抢不到游戏窗口前台（GetForegroundWindow 永远不是游戏窗口），合成点击会落到别的窗口上。
 * 所以改成在游戏进程内部直接调用 Unity 自己的接口换场景：
 *   1) SceneUtility.GetScenePathByBuildIndex(i) 先把 0..N 的场景名打进日志，确认序号；
 *   2) SceneManager.LoadScene(levelN) 逐个切图；
 *   3) 每张图等若干 tick，没崩就打 OK；全过之后写 autotest.txt 并 ExitProcess(0)。
 *
 * 只由环境变量打开，正常游戏不受影响：
 *   UCF_AUTOTEST=7,10   关卡序号（levelN 的 N，见 docs/地图对照表.md）
 *   UCF_AT_WARM=40      切图前等多少 tick（一 tick = 250 ms）
 *   UCF_AT_SETTLE=48    每张图等多少 tick
 *   UCF_AT_EXIT=1       全部通过后是否直接退出（1=退出，0=留在游戏里）
 */
#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdarg.h>

typedef void* P;

#define AT_MAX_TARGETS 8

static int g_on;
static int g_phase;          /* 0=查场景表 1=预热 2=逐图切换 3=结束 */
static int g_sub;            /* phase 2 的子状态：0=该切图了 1=等稳定 */
static int g_ticks;
static int g_iTarget;
static char g_dir[MAX_PATH];
static int g_targets[AT_MAX_TARGETS];
static int g_nTargets;
static int g_warmLen = 40;
static int g_settleLen = 48;
static int g_exitWhenDone = 1;

static P (*a_domain_get)(void);
static P (*a_domain_get_assemblies)(P, int*);
static P (*a_assembly_get_image)(P);
static const char* (*a_image_get_name)(P);
static P (*a_class_from_name)(P, const char*, const char*);
static P (*a_class_get_method_from_name)(P, const char*, int);
static P (*a_class_get_methods)(P, void**);
static const char* (*a_method_get_name)(P);
static int (*a_method_get_param_count)(P);
static P (*a_method_get_param)(P, int);
static P (*a_class_from_il2cpp_type)(P);
static const char* (*a_class_get_name)(P);
static P (*a_runtime_invoke)(P, P, void**, P*);
static void (*a_thread_attach)(P);
static P (*a_domain_assembly_open)(P, const char*);

static P g_scmCls, g_sutilCls, g_loadScene, g_scenePath;
static P g_appCls;
/* Resources.UnloadUnusedAssets：Unity 换图后会做一次「托管对象存活判定」
 * (il2cpp_unity_liveness_calculation_*)。2026-11-17 的五次闪退全崩在这条路径里
 * （GameAssembly+0x1290b1）。自测里在进图后主动调一次，用来判断不经过房间/对局
 * 能不能复现。UCF_AT_UNLOAD=0 可关。 */
static P g_resCls, g_unload;
static int g_unloadOn = 1, g_unloadDone;
static const char* g_loadName;
static int g_loadArgc = 1;
static int g_loadDumped2;

static void alog(const char* fmt, ...) {
  char line[512];
  char path[MAX_PATH];
  FILE* f;
  SYSTEMTIME st;
  va_list ap;
  if (!g_dir[0]) return;
  va_start(ap, fmt);
  vsnprintf(line, sizeof line, fmt, ap);
  va_end(ap);
  sprintf(path, "%s\\ucf_mod.log", g_dir);
  f = fopen(path, "a");
  if (!f) return;
  GetLocalTime(&st);
  fprintf(f, "%04d-%02d-%02d %02d:%02d:%02d [at] %s\n",
          st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond, line);
  fclose(f);
}

/* VEH 之外的第二道保险：只在确认可读时才解引用 */
static int at_readable(const void* p, unsigned n) {
  MEMORY_BASIC_INFORMATION mbi;
  if (!p) return 0;
  if (VirtualQuery(p, &mbi, sizeof mbi) != sizeof mbi) return 0;
  if (mbi.State != MEM_COMMIT) return 0;
  if (mbi.Protect & (PAGE_NOACCESS | PAGE_GUARD)) return 0;
  return ((const unsigned char*)p + n) <= ((const unsigned char*)mbi.BaseAddress + mbi.RegionSize);
}

static void at_str(P s, char* out, int cap) {
  int n, i;
  if (!out || cap <= 0) return;
  out[0] = 0;
  if (!s || !at_readable(s, 0x10)) return;
  n = *(int*)((char*)s + 8);
  if (n < 0) return;
  if (n > cap - 1) n = cap - 1;
  if (n > 300) n = 300;
  for (i = 0; i < n; i++) {
    unsigned short ch = *(unsigned short*)((char*)s + 12 + i * 2);
    out[i] = (ch > 0 && ch < 128) ? (char)ch : '?';
  }
  out[n] = 0;
}

static P at_find_image(const char* name) {
  int n = 0, i;
  P arr, dom;
  if (!a_domain_get || !a_domain_get_assemblies || !a_assembly_get_image || !a_image_get_name) return 0;
  dom = a_domain_get();
  if (!dom) return 0;
  if (a_domain_assembly_open) {
    P asm_ = a_domain_assembly_open(dom, name);
    if (asm_) {
      P img = a_assembly_get_image(asm_);
      if (img) return img;
    }
  }
  arr = a_domain_get_assemblies(dom, &n);
  if (!arr) return 0;
  for (i = 0; i < n; i++) {
    P asm_ = *(P*)((char*)arr + 0x10 + i * 4);
    P img;
    const char* in;
    if (!asm_) break;
    img = a_assembly_get_image(asm_);
    if (!img || !a_image_get_name) continue;
    in = a_image_get_name(img);
    if (in && !strcmp(in, name)) return img;
  }
  return 0;
}

static int g_probes;
static int g_loadDumped;

/* Il2CppType: data(0..3) | attrs:16, type:8, num_mods:6, byref:1, pinned:1
 * 也就是枚举类型落在偏移 6 的那个字节上。用它判断参数是 int32 还是 string，
 * 不依赖 il2cpp_class_from_il2cpp_type（那个导出不一定有）。 */
static int at_type_kind(P ty) {
  if (!ty || !at_readable(ty, 8)) return -1;
  return (int)((const unsigned char*)ty)[6];
}

/* 在一个镜像里找 SceneManager / SceneUtility，并记下 LoadScene 的重载情况 */
static void at_pick_scene(P img) {
  if (!img || !a_class_from_name) return;
  if (!g_scmCls) g_scmCls = a_class_from_name(img, "UnityEngine.SceneManagement", "SceneManager");
  if (!g_scmCls) g_scmCls = a_class_from_name(img, "", "SceneManager");
  if (!g_sutilCls) g_sutilCls = a_class_from_name(img, "UnityEngine.SceneManagement", "SceneUtility");
  if (!g_sutilCls) g_sutilCls = a_class_from_name(img, "", "SceneUtility");
  if (!g_appCls) g_appCls = a_class_from_name(img, "UnityEngine", "Application");
}

static int at_resolve(void) {
  HMODULE ga;
  if (g_loadScene && g_scenePath) return 1;
  ga = GetModuleHandleA("GameAssembly.dll");
  if (!ga) return 0;
  if (!a_domain_get) {
#define AR(n) *(void**)&a_##n = GetProcAddress(ga, "il2cpp_" #n)
    AR(domain_get); AR(domain_get_assemblies); AR(assembly_get_image); AR(image_get_name);
    AR(class_from_name); AR(class_get_method_from_name); AR(class_get_methods);
    AR(method_get_name); AR(method_get_param_count); AR(method_get_param);
    AR(class_from_il2cpp_type); AR(class_get_name); AR(runtime_invoke);
    AR(thread_attach); AR(domain_assembly_open);
#undef AR
    if (!a_domain_get || !a_domain_get()) return 0;
    if (a_thread_attach) a_thread_attach(a_domain_get());
  }
  if (!a_class_from_name || !a_runtime_invoke) {
    if ((g_probes++ % 16) == 0)
      alog("resolve: missing export class_from_name=%p runtime_invoke=%p", (void*)a_class_from_name, (void*)a_runtime_invoke);
    return 0;
  }
  if (!g_scmCls) {
    P img = at_find_image("UnityEngine.SceneManagement.dll");
    if ((g_probes++ % 16) == 0) alog("resolve: img(SceneManagement)=%p", img);
    if (img) at_pick_scene(img);
    if (!g_scmCls) {
      /* 兜底：不认镜像名，就把所有程序集挨个试一遍 */
      int n = 0, i;
      P arr = a_domain_get_assemblies(a_domain_get(), &n);
      if ((g_probes % 16) == 1) alog("resolve: fallback scan over %d assemblie(s)", n);
      for (i = 0; arr && i < n && !g_scmCls; i++) {
        P asm_ = *(P*)((char*)arr + 0x10 + i * 4);
        P im;
        if (!asm_) break;
        im = a_assembly_get_image(asm_);
        if (!im) continue;
        if ((g_probes % 16) == 1 && a_image_get_name) alog("resolve: asm[%d]='%s'", i, a_image_get_name(im));
        at_pick_scene(im);
      }
    }
  }
  if (!g_scmCls) return 0;
  /* LoadScene 有 (int) 和 (string) 两个单参数重载，必须挑 int 那个（传错了就是
   * 把整数当 string 引用用，必崩）。参数类型直接用 Il2CppType 的类型字节判断。 */
  if (!g_loadScene) {
    /* 先看导出到底缺哪个，再列出所有 argc=1 的候选（只打一次） */
    if (!g_loadDumped) {
      alog("resolve: exp methods=%p mname=%p mpc=%p mparam=%p fmtn=%p cft=%p cname=%p",
           (void*)a_class_get_methods, (void*)a_method_get_name, (void*)a_method_get_param_count,
           (void*)a_method_get_param, (void*)a_class_get_method_from_name,
           (void*)a_class_from_il2cpp_type, (void*)a_class_get_name);
      if (a_class_get_methods && a_method_get_name && a_method_get_param_count) {
        void* it = 0;
        P m;
        int total = 0, shown = 0;
        while ((m = a_class_get_methods(g_scmCls, &it)) != 0 && total < 400) {
          const char* nm = a_method_get_name(m);
          int argc = a_method_get_param_count(m);
          total++;
          if (nm && (strstr(nm, "Load") || strstr(nm, "Scene")) && shown < 30) {
            alog("resolve: SceneManager.%s argc=%d", nm, argc);
            shown++;
          }
        }
        alog("resolve: SceneManager method count=%d", total);
      }
      g_loadDumped = 1;
    }
    {
      /* il2cpp 裁剪（code stripping）把单参数的 LoadScene(int) / LoadScene(string)
       * 这两个便利重载删掉了，元数据里只剩 LoadScene(int, LoadSceneMode) 和
       * LoadScene(string, LoadSceneMode)。所以按参数个数 2 来找，并且必须确认
       * 第一个参数是 int32，不能拿 (string, mode) 那个。 */
      static const char* cand[] = { "LoadScene", "LoadSceneAsync" };
      int ci;
      for (ci = 0; ci < 2 && !g_loadScene; ci++) {
        int want;
        for (want = 1; want <= 2 && !g_loadScene; want++) {
          void* it = 0;
          P m;
          if (!a_class_get_methods) break;
          while ((m = a_class_get_methods(g_scmCls, &it)) != 0) {
            const char* nm = a_method_get_name ? a_method_get_name(m) : 0;
            int k0, k1 = -1;
            if (!nm || strcmp(nm, cand[ci])) continue;
            if (a_method_get_param_count(m) != want) continue;
            k0 = at_type_kind(a_method_get_param ? a_method_get_param(m, 0) : 0);
            if (want == 2) k1 = at_type_kind(a_method_get_param ? a_method_get_param(m, 1) : 0);
            if (!g_loadDumped2) alog("resolve: %s argc=%d kind0=0x%02x kind1=0x%02x", cand[ci], want, k0, k1);
            if (k0 == 8) { g_loadScene = m; g_loadName = cand[ci]; g_loadArgc = want; break; }
          }
        }
      }
      g_loadDumped2 = 1;
      /* 兜底：老 API Application.LoadLevel(int)，Unity 2020 还在（标了 obsolete） */
      if (!g_loadScene && g_appCls && a_class_get_method_from_name) {
        P m = a_class_get_method_from_name(g_appCls, "LoadLevel", 1);
        if (m && a_method_get_param) {
          int k = at_type_kind(a_method_get_param(m, 0));
          if (k == 8) { g_loadScene = m; g_loadName = "Application.LoadLevel"; }
        }
      }
    }
  }
  if (!g_scenePath && g_sutilCls && a_class_get_method_from_name)
    g_scenePath = a_class_get_method_from_name(g_sutilCls, "GetScenePathByBuildIndex", 1);
  if (!g_loadScene) {
    if ((g_probes++ % 16) == 3)
      alog("resolve: partial scm=%p sutil=%p load=%p path=%p", g_scmCls, g_sutilCls, g_loadScene, g_scenePath);
    return 0;
  }
  if (!g_resCls) {
    P img = at_find_image("UnityEngine.CoreModule.dll");
    if (img) g_resCls = a_class_from_name(img, "UnityEngine", "Resources");
    if (!g_resCls) {
      int n = 0, i;
      P arr = a_domain_get_assemblies(a_domain_get(), &n);
      for (i = 0; arr && i < n && !g_resCls; i++) {
        P asm_ = *(P*)((char*)arr + 0x10 + i * 4);
        P im;
        if (!asm_) break;
        im = a_assembly_get_image(asm_);
        if (!im) continue;
        g_resCls = a_class_from_name(im, "UnityEngine", "Resources");
      }
    }
    if (g_resCls && a_class_get_method_from_name)
      g_unload = a_class_get_method_from_name(g_resCls, "UnloadUnusedAssets", 0);
    alog("resolve: Resources=%p UnloadUnusedAssets=%p", (void*)g_resCls, (void*)g_unload);
  }
  alog("resolve: OK scm=%p load=%p(%s) path=%p (scene-path dump %s)",
       g_scmCls, g_loadScene, g_loadName ? g_loadName : "?", g_scenePath, g_scenePath ? "on" : "off");
  return 1;
}

static P at_invoke2(P m, void* a0, void* a1, int* excOut) {
  void* args[2];
  P exc = 0;
  P r;
  if (excOut) *excOut = 0;
  if (!m) return 0;
  args[0] = a0;
  args[1] = a1;
  r = a_runtime_invoke(m, 0, args, &exc);
  if (exc && excOut) *excOut = 1;
  return r;
}

static P at_invoke(P m, void* arg, int* excOut) { return at_invoke2(m, arg, 0, excOut); }

static void at_result(const char* text) {
  char path[MAX_PATH];
  FILE* f;
  if (!g_dir[0]) return;
  sprintf(path, "%s\\autotest.txt", g_dir);
  f = fopen(path, "a");
  if (!f) return;
  fprintf(f, "%s\n", text);
  fclose(f);
}

static void at_finish(int ok) {
  char line[256];
  sprintf(line, "RESULT %s targets=%d", ok ? "PASS" : "FAIL", g_nTargets);
  alog("=== %s ===", line);
  at_result(line);
  g_phase = 3;
  if (ok && g_exitWhenDone) {
    alog("exiting (UCF_AT_EXIT=1) so the harness can tell PASS from a crash");
    ExitProcess(0);
  }
}

void autotest_tick(void) {
  if (!g_on || g_phase >= 3) return;
  if (!at_resolve()) {
    if ((g_ticks++ % 16) == 0) alog("waiting for SceneManager/SceneUtility ...");
    return;
  }
  if (g_phase == 0) {
    int i;
    for (i = 0; g_scenePath && i < 16; i++) {
      int idx = i, exc = 0;
      P s = at_invoke(g_scenePath, &idx, &exc);
      char b[200];
      at_str(s, b, sizeof b);
      alog("scene[%d] = %s", i, b[0] ? b : "(null)");
      if (!b[0]) break;
    }
    alog("targets=%d warm=%d settle=%d (tick=250ms)", g_nTargets, g_warmLen, g_settleLen);
    g_phase = 1;
    g_ticks = 0;
    return;
  }
  if (g_phase == 1) {
    if (++g_ticks < g_warmLen) {
      if ((g_ticks % 8) == 0) alog("warm %d/%d", g_ticks, g_warmLen);
      return;
    }
    alog("warm done -> begin scene switching");
    g_phase = 2;
    g_sub = 0;
    g_iTarget = 0;
    g_ticks = 0;
    return;
  }
  if (g_phase == 2) {
    int idx = g_targets[g_iTarget];
    if (g_sub == 0) {
      int exc = 0;
      int mode = 0;   /* LoadSceneMode.Single */
      alog("LOAD level%d (build index %d, %s argc=%d)", idx, idx, g_loadName ? g_loadName : "?", g_loadArgc);
      if (g_loadArgc >= 2) at_invoke2(g_loadScene, &idx, &mode, &exc);
      else at_invoke(g_loadScene, &idx, &exc);
      if (exc) {
        alog("FAIL level%d: managed exception thrown by LoadScene", idx);
        at_finish(0);
        return;
      }
      g_sub = 1;
      g_ticks = 0;
      g_unloadDone = 0;
      return;
    }
    g_ticks++;
    if (g_unloadOn && g_unload && !g_unloadDone && g_ticks == 4) {
      int exc = 0;
      P op = at_invoke(g_unload, 0, &exc);
      g_unloadDone = 1;
      alog("unload: Resources.UnloadUnusedAssets -> %p exc=%d (level%d, +1s)", (void*)op, exc, idx);
    }
    if (g_ticks < g_settleLen) {
      if ((g_ticks % 8) == 0) alog("settle level%d %d/%d", idx, g_ticks, g_settleLen);
      return;
    }
    {
      char mn[80];
      extern void editor_map_name(char*, int);
      mn[0] = 0;
      editor_map_name(mn, sizeof mn);
      alog("OK level%d survived %d ticks (map='%s')", idx, g_settleLen, mn);
      {
        char okline[64];
        sprintf(okline, "OK level%d", idx);
        at_result(okline);
      }
    }
    g_ticks = 0;
    g_sub = 0;
    if (++g_iTarget >= g_nTargets) at_finish(1);
  }
}

/* editor.c 的自由视角用：车测已经进图（phase 2 = 正在切图）才允许接管相机，
 * 免得在大厅/热身阶段把相机摆到 0,0,0。 */
int autotest_in_map(void) { return g_on && g_phase >= 2; }

void autotest_start(const char* modDir) {
  char v[256];
  char* p;
  DWORD n;
  if (!modDir || !modDir[0]) return;
  strncpy(g_dir, modDir, sizeof(g_dir) - 1);
  g_dir[sizeof(g_dir) - 1] = 0;
  n = GetEnvironmentVariableA("UCF_AUTOTEST", v, sizeof v);
  if (n == 0 || !v[0]) return;
  {
    char u[16];
    DWORD un = GetEnvironmentVariableA("UCF_AT_UNLOAD", u, sizeof u);
    if (un > 0 && u[0] == '0') g_unloadOn = 0;
  }
  p = v;
  while (*p && g_nTargets < AT_MAX_TARGETS) {
    while (*p == ' ' || *p == ',') p++;
    if (!*p) break;
    g_targets[g_nTargets++] = atoi(p);
    while (*p && *p != ',') p++;
  }
  if (!g_nTargets) return;
  {
    char t[64];
    DWORD m = GetEnvironmentVariableA("UCF_AT_WARM", t, sizeof t);
    if (m && t[0]) g_warmLen = atoi(t);
    m = GetEnvironmentVariableA("UCF_AT_SETTLE", t, sizeof t);
    if (m && t[0]) g_settleLen = atoi(t);
    m = GetEnvironmentVariableA("UCF_AT_EXIT", t, sizeof t);
    if (m && t[0]) g_exitWhenDone = atoi(t);
  }
  if (g_warmLen < 0) g_warmLen = 0;
  if (g_settleLen < 4) g_settleLen = 4;
  {
    char path[MAX_PATH];
    FILE* f;
    sprintf(path, "%s\\autotest.txt", g_dir);
    f = fopen(path, "w");
    if (f) { fprintf(f, "autotest start targets=%d\n", g_nTargets); fclose(f); }
  }
  g_on = 1;
  alog("autotest armed: %d target(s), warm=%d settle=%d exit=%d", g_nTargets, g_warmLen, g_settleLen, g_exitWhenDone);
}