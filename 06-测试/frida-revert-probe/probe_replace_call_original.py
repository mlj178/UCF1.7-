# -*- coding: utf-8 -*-
"""探针：验证「Interceptor.replace 之后还能不能安全调用原函数」。

04_knife 新加的"重击防卡死"依赖这个模式：
    var orig = new NativeFunction(addr, ...);          // 必须在 replace 之前建好
    Interceptor.replace(addr, new NativeCallback(function(...) {
        if (该拦) return;                              // 不调原函数
        orig(...);                                     // ← 这里到底进原函数，还是又进 replacement？
    }, ...));

如果 `orig(...)` 又进 replacement，就是**无限递归**（用户那边就是直接崩）。
这里用一个自造的 8 字节函数 `int target(int x){ return x+1; }` 实测，并用递归深度计数器兜住，
无论哪种结果都不会把探针进程搞崩。
"""

import sys

import frida

TARGET = r"C:\Windows\SysWOW64\cmd.exe"
TARGET_ARGS = ["/k", "echo replace-orig-probe-ready"]

AGENT = r"""
var out = {};

// int target(int x) { return x + 1; }
var page = Memory.alloc(Process.pageSize);
Memory.protect(page, Process.pageSize, 'rwx');
page.writeByteArray([0x8B, 0x44, 0x24, 0x04,      // mov eax, [esp+4]
                     0x83, 0xC0, 0x01,             // add eax, 1
                     0xC3]);                       // ret

var orig = new NativeFunction(page, 'int', ['int']);
out.before_replace = orig(41);                     // 期望 42

var depth = 0;
var maxDepth = 0;
var calls = 0;

var replacement = new NativeCallback(function (x) {
  calls++;
  depth++;
  if (depth > maxDepth) maxDepth = depth;
  if (depth > 5) {                                  // 兜住递归，别把进程搞崩
    depth--;
    return -999;
  }
  var r = orig(x);                                  // ← 关键：这一句的去向
  depth--;
  return r + 100;
}, 'int', ['int']);

Interceptor.replace(page, replacement);

var after = -12345;
try { after = orig(41); } catch (e) { after = 'THROW:' + e.message; }

out.after_replace_value = after;
out.replacement_calls = calls;
out.max_recursion_depth = maxDepth;
out.verdict = (maxDepth <= 1) ? 'orig() 调用的是原函数（安全）'
  : ('orig() 又进了 replacement（递归！深度 ' + maxDepth + '）—— 该模式不能用');

send({ t: 'report', data: out });
"""


def main():
    print(f"[i] spawning 32-bit target: {TARGET}")
    pid = frida.spawn([TARGET] + TARGET_ARGS)
    session = frida.attach(pid)
    box = {}
    script = session.create_script(AGENT)

    def on_message(m, d):
        if m.get("type") == "send" and m["payload"].get("t") == "report":
            box.update(m["payload"]["data"])
        else:
            print("[agent]", m)

    script.on("message", on_message)
    script.load()

    print("[=] replace 前 orig(41) =", box.get("before_replace"), "（期望 42）")
    print("[=] replace 后 orig(41) =", box.get("after_replace_value"), "（期望 142 = 42+100）")
    print("[=] replacement 被调用次数 =", box.get("replacement_calls"))
    print("[=] 递归深度 =", box.get("max_recursion_depth"))
    print("[=] VERDICT:", box.get("verdict"))

    ok = box.get("before_replace") == 42 and box.get("after_replace_value") == 142 and box.get("max_recursion_depth") == 1
    print("[=] 结论:", "该模式可用（replace 后仍能调原函数）" if ok else "该模式不可用，需要换实现")

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
