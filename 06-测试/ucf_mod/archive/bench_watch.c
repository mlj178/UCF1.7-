#include <windows.h>
#include <stdio.h>
#include <string.h>

int main(void) {
  LARGE_INTEGER f, t0, t1;
  MEMORY_BASIC_INFORMATION mbi;
  char buf[256];
  int i, N = 1000000;
  volatile SIZE_T acc = 0;
  QueryPerformanceFrequency(&f);

  /* A: 旧实现 —— 每个槽位都重新扫一遍类名（Bot_NanoGuardArea = 17 字节）*/
  QueryPerformanceCounter(&t0);
  for (i = 0; i < N; i++) {
    int k;
    for (k = 0; k < 21; k++) { VirtualQuery(&buf[k], &mbi, sizeof mbi); memcpy(&buf[k], &i, 4); }
    acc += (unsigned char)buf[0];
  }
  QueryPerformanceCounter(&t1);
  printf("A slot check (name scan) : %8.2f us\n", (double)(t1.QuadPart - t0.QuadPart) * 1e6 / (double)f.QuadPart / N);

  /* B: 新实现 —— 类指针命中速查表后，每个槽位只剩「读槽位 + 读 klass」2 次 */
  QueryPerformanceCounter(&t0);
  for (i = 0; i < N; i++) {
    int k;
    for (k = 0; k < 2; k++) { VirtualQuery(&buf[k], &mbi, sizeof mbi); memcpy(&buf[k], &i, 4); }
    acc += (unsigned char)buf[0];
  }
  QueryPerformanceCounter(&t1);
  printf("B slot check (memo hit)  : %8.2f us\n", (double)(t1.QuadPart - t0.QuadPart) * 1e6 / (double)f.QuadPart / N);
  return 0;
}
