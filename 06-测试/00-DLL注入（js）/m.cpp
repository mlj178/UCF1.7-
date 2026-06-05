// m.cpp - MSVC DLL, Frida loads, shared memory trigger, IL2CPP attach
#include <windows.h>
#include <stdint.h>

#define RVA_SingletonGet   0x4A8170
#define RVA_IsMyPlayer     0xB55FD0
#define RVA_Linecast       0xAB9B80

typedef struct { float x,y,z; } Vec3;
typedef void*(__cdecl*fSG)(void*);
typedef int (__cdecl*fIMP)(void*,void*);
typedef int (__cdecl*fLC)(Vec3,Vec3,int,void*);

static uint32_t g_base = 0;
static fSG  gSG=NULL; static fIMP gIMP=NULL; static fLC gLC=NULL;
static int  g_ready=0;

// Frida writes to these:
__declspec(dllexport) volatile int  g_cmd = 0;  // 1=start, 2=done
__declspec(dllexport) volatile int  g_ok = 0;

static void Init() {
    HMODULE ga = GetModuleHandleA("GameAssembly.dll");
    if (!ga) return;
    g_base = (uint32_t)ga;
    gSG  = (fSG)(g_base + RVA_SingletonGet);
    gIMP = (fIMP)(g_base + RVA_IsMyPlayer);
    gLC  = (fLC)(g_base + RVA_Linecast);

    // attach IL2CPP
    auto dg = (void*(__cdecl*)())GetProcAddress(ga,"il2cpp_domain_get");
    auto ta = (void*(__cdecl*)(void*))GetProcAddress(ga,"il2cpp_thread_attach");
    auto td = (void(__cdecl*)(void*))GetProcAddress(ga,"il2cpp_thread_detach");
    if (dg && ta && td) {
        void* t = ta(dg());
        g_ready = 1;
        // write sentinel file
        HANDLE hf = CreateFileA("D:\\BaiduNetdiskDownload\\UnityCrossFire1.7.1\\UnityCrossFire1.7.1\\m_ready.txt", GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
        if (hf != INVALID_HANDLE_VALUE) { DWORD bw; WriteFile(hf, "1", 1, &bw, NULL); CloseHandle(hf); }
        OutputDebugStringA("[m] IL2CPP attached\n");
        td(t);
    }
}

static DWORD WINAPI Th(LPVOID) { Init(); return 0; }

BOOL WINAPI DllMain(HINSTANCE h, DWORD r, LPVOID) {
    if (r == DLL_PROCESS_ATTACH) {
        DisableThreadLibraryCalls(h);
        CreateThread(0,0,Th,0,0,0);
    }
    return TRUE;
}
