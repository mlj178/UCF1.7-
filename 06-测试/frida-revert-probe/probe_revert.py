# -*- coding: utf-8 -*-
"""只读探针：验证 Frida 17 在 32/64 位进程里

1) Interceptor.replace 的替身回调里调用"替换前创建的 NativeFunction 原始地址"是否会递归；
2) Interceptor.revert 之后，替身回调是否彻底不再被调用（= 关闭功能是否真的还原）；
3) replace -> revert -> replace 反复开关是否可重复（模拟用户反复开关功能）。

做法：把自己这个 Python 进程作为目标，替换 kernel32!GetCurrentProcessId，
用 ctypes 直接调用它，统计替身回调的命中次数。
替身回调原样返回原函数结果，因此不会改变进程行为。
"""

import ctypes
import os
import sys

import frida

AGENT = r"""
var addr = Process.getModuleByName('kernel32.dll').getExportByName('GetCurrentProcessId');
var orig = new NativeFunction(addr, 'uint32', []);
var hits = 0;
var recursed = 0;

function install() {
  Interceptor.replace(addr, new NativeCallback(function () {
    hits++;
    if (hits > 100000) { recursed++; return 0; }  // 递归保护：不该发生
    return orig();
  }, 'uint32', []));
}

rpc.exports = {
  install: function () { install(); return true; },
  revert: function () { Interceptor.revert(addr); return true; },
  hits: function () { return hits; },
  recursed: function () { return recursed; }
};
"""


def main():
    pid = os.getpid()
    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.GetCurrentProcessId.restype = ctypes.c_uint32
    k32.GetCurrentProcessId.argtypes = []

    print(f"[i] target pid = {pid}, python = {sys.version.split()[0]} ({8 * ctypes.sizeof(ctypes.c_void_p)}-bit)")

    session = frida.attach(pid)
    script = session.create_script(AGENT)
    messages = []
    script.on("message", lambda m, d: (messages.append(m), print("[agent]", m)))
    script.load()
    print("[i] frida attach(self) ok, agent loaded")

    results = {}

    def sample(n=200):
        return [k32.GetCurrentProcessId() for _ in range(n)]

    # --- 1) 未 hook 基线 ---
    sample()
    hits0 = script.exports_sync.hits()
    results["hits_before_install"] = hits0

    # --- 2) replace 「开」 ---
    script.exports_sync.install()
    values = sample()
    hits1 = script.exports_sync.hits()
    recursed1 = script.exports_sync.recursed()
    results["hits_after_install"] = hits1
    results["recursed_after_install"] = recursed1
    results["pid_values_ok_with_hook"] = all(v == pid for v in values)

    # --- 3) revert 「关」 ---
    script.exports_sync.revert()
    hits2 = script.exports_sync.hits()
    sample()
    hits3 = script.exports_sync.hits()
    results["hits_right_after_revert"] = hits2
    results["hits_after_revert_and_calls"] = hits3
    results["callback_dead_after_revert"] = (hits3 == hits2)

    # --- 4) 再开一次（replace -> revert -> replace）---
    script.exports_sync.install()
    hitsA = script.exports_sync.hits()
    sample()
    hitsB = script.exports_sync.hits()
    results["second_enable_works"] = (hitsB > hitsA)
    script.exports_sync.revert()
    hitsC = script.exports_sync.hits()
    sample()
    hitsD = script.exports_sync.hits()
    results["second_disable_works"] = (hitsD == hitsC)

    print("[=] results:")
    for key, value in results.items():
        print(f"    {key} = {value}")

    if messages:
        print("[=] agent messages:")
        for message in messages:
            print("   ", message)

    script.unload()
    session.detach()

    ok = (
        results["hits_after_install"] > results["hits_before_install"]
        and results["recursed_after_install"] == 0
        and results["pid_values_ok_with_hook"]
        and results["callback_dead_after_revert"]
        and results["second_enable_works"]
        and results["second_disable_works"]
    )
    print("[=] VERDICT:", "replace/revert 可逆、可在替身里安全调用原函数" if ok else "存在异常，见上方数据")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
