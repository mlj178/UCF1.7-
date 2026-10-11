# -*- coding: utf-8 -*-
"""32 位目标探针：在真实 32 位（ia32 / 4 字节指针）进程里验证

1) Interceptor.replace 的替身回调里调用"替换前创建的 NativeFunction 原函数"是否会递归；
2) Interceptor.revert 之后，替身回调是否彻底不再被触发（= 关闭功能真的还原了原函数）；
3) replace -> revert -> replace 反复开关是否可重复。

触发器放在目标进程内部（Frida agent 自己调用同一地址），不依赖目标程序的行为。
被替换的是 kernel32!GetTickCount：只读、无副作用、返回值可校验。
"""

import sys

import frida

TARGET = r"C:\Windows\SysWOW64\cmd.exe"
TARGET_ARGS = ["/k", "echo probe-ready"]

AGENT = r"""
var k32 = Process.getModuleByName('kernel32.dll');
var addr = k32.getExportByName('GetTickCount');
var orig = new NativeFunction(addr, 'uint32', []);
var probe = new NativeFunction(addr, 'uint32', []);   // 替换前建立的"原函数"引用
var hits = 0;
var maxDepth = 0;
var depth = 0;

function replacement() {
  depth++;
  if (depth > maxDepth) maxDepth = depth;
  hits++;
  var v = orig();
  depth--;
  return v;
}

rpc.exports = {
  install: function () {
    depth = 0;
    Interceptor.replace(addr, new NativeCallback(replacement, 'uint32', []));
    return true;
  },
  revert: function () { Interceptor.revert(addr); return true; },
  calln: function (n) {
    var last = 0;
    for (var i = 0; i < n; i++) last = probe();
    return last;
  },
  stats: function () { return JSON.stringify({ hits: hits, maxDepth: maxDepth, depth: depth }); }
};

send({
  t: 'ready',
  arch: Process.arch,
  pointerSize: Process.pointerSize,
  addr: addr.toString()
});
"""


def main():
    print(f"[i] spawning 32-bit target: {TARGET}")
    pid = frida.spawn([TARGET] + TARGET_ARGS)
    session = frida.attach(pid)
    script = session.create_script(AGENT)
    script.on("message", lambda m, d: print("[agent]", m))
    script.load()

    def stats():
        import json
        return json.loads(script.exports_sync.stats())

    results = {}

    # 1) 未 hook：调用 200 次，命中数应保持 0
    v0 = script.exports_sync.calln(200)
    s0 = stats()
    results["hits_before_install"] = s0["hits"]
    results["value_before_install"] = v0

    # 2) replace 后调用 200 次
    script.exports_sync.install()
    v1 = script.exports_sync.calln(200)
    s1 = stats()
    results["hits_after_install"] = s1["hits"]
    results["max_depth_in_replacement"] = s1["maxDepth"]
    results["value_after_install"] = v1

    # 3) revert 后再调用 400 次
    script.exports_sync.revert()
    s2 = stats()
    v2 = script.exports_sync.calln(400)
    s3 = stats()
    results["hits_just_after_revert"] = s2["hits"]
    results["hits_after_revert_plus_400_calls"] = s3["hits"]
    results["callback_dead_after_revert"] = (s3["hits"] == s2["hits"])
    results["value_after_revert"] = v2

    # 4) 第二次 replace -> revert
    script.exports_sync.install()
    script.exports_sync.calln(200)
    s4 = stats()
    script.exports_sync.revert()
    s5 = stats()
    script.exports_sync.calln(400)
    s6 = stats()
    results["second_install_hits"] = s4["hits"]
    results["second_revert_hits"] = s5["hits"]
    results["second_revert_dead"] = (s6["hits"] == s5["hits"])

    print("[=] results:")
    for key, value in results.items():
        print(f"    {key} = {value}")

    ok = (
        results["hits_before_install"] == 0
        and results["hits_after_install"] >= 200
        and results["max_depth_in_replacement"] == 1
        and results["callback_dead_after_revert"]
        and results["second_install_hits"] > results["hits_after_revert_plus_400_calls"]
        and results["second_revert_dead"]
        and results["value_before_install"] > 0
        and results["value_after_revert"] > 0
    )
    print("[=] VERDICT:", "32 位：replace/revert 完全可逆，替身内可安全调用原函数" if ok else "32 位：存在异常")

    try:
        session.detach()
    except Exception:
        pass
    try:
        frida.kill(pid)
    except Exception:
        pass
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
