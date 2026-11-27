#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""自检：成品档「按指纹找图」的 C 实现（2026-11-27 一图一夹）。

跑法：python app/tests/test_navsearch_c.py

做的事：
  1) 从 src/editor.c 里**原样**抽出 nav_find_fp_file()（不复制、不手抄，改代码这里自动跟上）
  2) 造一份临时夹具：<root>/<图>/final/<指纹>.txt、<图>/markers.txt、<图>/<指纹>.txt
  3) 用 mingw gcc 编一个小程序跑四种情况：命中 / 缺文件 / 不带子目录 / 空参数
  4) 顺带验证中文图文件夹名在 ANSI 世界（FindFirstFileA / fopen）里能来回搬

找不到 gcc 时跳过（不判失败）：这台机器没装编译器不代表布局有问题。
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记，本文件搬到哪都对

EDITOR_C = os.path.join(UCF_ROOT, "src", "editor.c")
GCC_CANDIDATES = (r"D:\Program Files\mingw32\bin\gcc.exe", "gcc")

MAIN = r"""
#include <windows.h>
#include <stdio.h>
#include <string.h>

%s

static int failures = 0;
static void expect(int cond, const char* what) {
  if (cond) printf("  OK   %%s\n", what);
  else { printf("  !!   %%s\n", what); failures++; }
}
static int file_exists(const char* p) {
  DWORD a = GetFileAttributesA(p);
  return a != INVALID_FILE_ATTRIBUTES && !(a & FILE_ATTRIBUTE_DIRECTORY);
}
static int ends_with(const char* s, const char* tail) {
  size_t n = strlen(s), m = strlen(tail);
  return n >= m && strcmp(s + n - m, tail) == 0;
}

int main(int argc, char** argv) {
  char root[MAX_PATH], path[MAX_PATH], folder[160], mk[MAX_PATH];
  snprintf(root, sizeof root, "%%s", argc > 1 ? argv[1] : ".");
  path[0] = 0; folder[0] = 0;
  expect(nav_find_fp_file(root, "final", "n786-57a46e3465c847cb",
                          path, sizeof path, folder, sizeof folder) == 1,
         "final/ 里按指纹命中");
  expect(file_exists(path), "返回的路径真的存在（中文文件夹名没坏）");
  expect(ends_with(path, "\\final\\n786-57a46e3465c847cb.txt"), "路径尾巴 = final/<指纹>.txt");
  expect(folder[0] != 0, "带回了图文件夹名");
  snprintf(mk, sizeof mk, "%%s\\%%s\\markers.txt", root, folder);
  expect(file_exists(mk), "<图>/markers.txt 拼得出来（成品档蹲守点靠这句）");
  path[0] = 0; folder[0] = 0;
  expect(nav_find_fp_file(root, "", "n180-03b43b7ee737fcdc",
                          path, sizeof path, folder, sizeof folder) == 1,
         "不带子目录时找 <图>/<指纹>.txt");
  expect(file_exists(path), "草稿路径也存在");
  path[0] = 0; folder[0] = 0;
  expect(nav_find_fp_file(root, "final", "n0-0000000000000000",
                          path, sizeof path, folder, sizeof folder) == 0,
         "没有这张图的成品时返回 0（不瞎套）");
  expect(nav_find_fp_file("", "final", "n1-x", path, sizeof path, folder, sizeof folder) == 0,
         "空 root 返回 0");
  expect(nav_find_fp_file(root, "final", "", path, sizeof path, folder, sizeof folder) == 0,
         "空指纹返回 0");
  printf("\n%%s\n", failures ? "FAIL" : "PASS");
  return failures ? 1 : 0;
}
"""


def extract_fn():
    r"""从 editor.c 抽出 nav_find_fp_file() 的完整定义（到 pack_init 之前）。"""
    with open(EDITOR_C, "r", encoding="utf-8", errors="replace") as f:
        src = f.read()
    a = src.find("static int nav_find_fp_file(")
    b = src.find("static void pack_init(void) {")
    if a < 0 or b < 0 or b <= a:
        raise SystemExit("editor.c 里找不到 nav_find_fp_file() / pack_init()")
    return src[a:b].rstrip()


def find_gcc():
    for c in GCC_CANDIDATES:
        if os.path.isabs(c):
            if os.path.isfile(c):
                return c
        else:
            p = shutil.which(c)
            if p:
                return p
    return ""


def main():
    gcc = find_gcc()
    if not gcc:
        print("SKIP: 没找到 gcc（这台机器没装编译器），跳过 C 侧自检")
        return 0
    fn = extract_fn()
    tmp = tempfile.mkdtemp(prefix="ucf_navsearch_")
    try:
        old = os.getcwd()
        os.chdir(tmp)
        try:
            with open("t.c", "w", encoding="utf-8", newline="\n") as f:
                f.write(MAIN % fn)
            r = subprocess.run([gcc, "-O1", "-o", "t.exe", "t.c"], capture_output=True)
            if r.returncode != 0:
                print("!! 编译失败：")
                print((r.stderr or b"").decode("utf-8", "replace"))
                return 1
            # 夹具：两张图，一张有成品，一张只有草稿
            for d in ("01_TransportShip运输船/final", "11_Nano_DawnVillage新寂静村"):
                os.makedirs(os.path.join(tmp, "fx", *d.split("/")), exist_ok=True)
            for p in ("01_TransportShip运输船/final/n786-57a46e3465c847cb.txt",
                      "01_TransportShip运输船/markers.txt",
                      "11_Nano_DawnVillage新寂静村/n180-03b43b7ee737fcdc.txt"):
                with open(os.path.join(tmp, "fx", *p.split("/")), "w", encoding="utf-8") as f:
                    f.write("")
            r = subprocess.run(["t.exe", os.path.join(tmp, "fx")], capture_output=True)
            out = (r.stdout or b"").decode("utf-8", "replace")
            print(out.rstrip())
            return 0 if r.returncode == 0 else 1
        finally:
            os.chdir(old)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
