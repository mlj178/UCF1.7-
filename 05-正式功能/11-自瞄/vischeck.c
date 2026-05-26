// vischeck.c — Physics.Linecast 可见性检测辅助 DLL
// 编译: gcc -shared -o vischeck.dll vischeck.c -m32 -O2 -s
// 原因: Frida NativeFunction 不能传 Vector3 结构体(12字节按值),
//       由 C 编译器自动处理 __cdecl 栈帧和 struct 压栈

#include <stdbool.h>
#include <stdint.h>

typedef struct { float x, y, z; } Vector3;

// Frida 注入后写入 GameAssembly.dll + 0xAB9B80
static bool (*Linecast)(Vector3 start, Vector3 end, int32_t layerMask, void* method) = 0;

__declspec(dllexport) void SetLinecast(void* fn) {
    Linecast = (bool(*)(Vector3, Vector3, int32_t, void*))fn;
}

// from/to: 各指向3个float的指针; mask: layerMask (墙体=1)
// 返回: true=可见(中间无障碍), false=被遮挡
__declspec(dllexport) bool CheckVisible(float* from, float* to, int32_t mask) {
    Vector3 f = { from[0], from[1], from[2] };
    Vector3 t = { to[0], to[1], to[2] };
    return !Linecast(f, t, mask, 0);  // Linecast hit → 有障碍 → 不可见
}
