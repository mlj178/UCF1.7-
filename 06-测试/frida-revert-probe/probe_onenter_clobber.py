# -*- coding: utf-8 -*-
"""根因验证探针：证明"在被 Hook 函数体的 onEnter 里写内存会被本体覆盖，onLeave 才站得住"。

与游戏同形状的模型（不依赖任何 Windows API 的内部实现）：
  在目标进程里生成一个自己的机器码函数：`void body(int* p) { *p = 0x11223344; }`
  —— 与游戏侧 `Weapon.OnFireBtnPressed(+0xB6CDA0)` 的函数体 `this->_fireBtnPressed = 1;`
     形状完全一致：函数体自己写一块内存。
  同一个 Hook 里 onEnter / onLeave 都实现，用 phase 决定谁去清零，避免反复 attach 干扰结论。

判据（目标进程为 32 位 ia32，与游戏 GameAssembly.dll 同架构）：
  phase none   只挂钩不清零 -> 0x11223344（确认函数体真的在写）
  phase enter  onEnter 清零 -> 仍 0x11223344 = 被本体覆盖（这正是线上那版保护的真实情况）
  phase leave  onLeave  清零 -> 0x0        = 撤销站得住
  phase skip   onLeave 但不撤销 -> 0x11223344 = 不该误伤时确实不动
"""

import sys

import frida

TARGET = r"C:\Windows\SysWOW64\cmd.exe"
TARGET_ARGS = ["/k", "echo onenter-probe-ready"]

AGENT = r"""
var page = Memory.alloc(Process.pageSize);
Memory.protect(page, Process.pageSize, 'rwx');

// void body(int* p) { *p = 0x11223344; }
if (Process.pointerSize === 4) {
  page.writeByteArray([0x8B, 0x44, 0x24, 0x04,                     // mov eax, [esp+4]
                       0xC7, 0x00, 0x44, 0x33, 0x22, 0x11,          // mov dword [eax], 0x11223344
                       0xC3]);                                     // ret
} else {
  page.writeByteArray([0x48, 0x89, 0xC8,                            // mov rax, rcx
                       0xC7, 0x00, 0x44, 0x33, 0x22, 0x11,
                       0xC3]);
}
var body = new NativeFunction(page, 'void', ['pointer']);
var buf = Memory.alloc(4);
var phase = 'none';
var hits = { enter: 0, leave: 0 };

Interceptor.attach(page, {
  onEnter: function (args) {
    hits.enter++;
    this.p = args[0];
    if (phase === 'enter' && args[0] && !args[0].isNull()) args[0].writeU32(0);
  },
  onLeave: function () {
    hits.leave++;
    if (phase === 'leave' && this.p && !this.p.isNull()) this.p.writeU32(0);
  }
});

rpc.exports = {
  setphase: function (p) { phase = p; return phase; },
  call: function () {
    buf.writeU32(0);
    body(buf);
    return { value: '0x' + buf.readU32().toString(16), hits: JSON.stringify(hits) };
  }
};

send({ t: 'ready', arch: Process.arch, pointerSize: Process.pointerSize, body: page.toString() });
"""


def main():
    print(f"[i] spawning 32-bit target: {TARGET}")
    pid = frida.spawn([TARGET] + TARGET_ARGS)
    session = frida.attach(pid)
    script = session.create_script(AGENT)
    script.on("message", lambda m, d: print("[agent]", m))
    script.load()

    results = {}
    for phase, key in (
        ("none", "phase_none_expected_0x11223344"),
        ("enter", "phase_enter_onEnter_zero_expected_clobbered"),
        ("leave", "phase_leave_onLeave_zero_expected_0x0"),
        ("skip", "phase_skip_no_write_expected_0x11223344"),
    ):
        script.exports_sync.setphase(phase)
        run = script.exports_sync.call()
        results[key] = run["value"]
        print(f"[phase {phase:5s}] value = {run['value']:12s} hits = {run['hits']}")

    print("[=] results:")
    for key, value in results.items():
        print(f"    {key} = {value}")

    ok = (
        results["phase_none_expected_0x11223344"] == "0x11223344"
        and results["phase_enter_onEnter_zero_expected_clobbered"] == "0x11223344"
        and results["phase_leave_onLeave_zero_expected_0x0"] == "0x0"
        and results["phase_skip_no_write_expected_0x11223344"] == "0x11223344"
    )
    print("[=] VERDICT:", "已复现：onEnter 写的值被本体覆盖，onLeave 才站得住" if ok else "结论与预期不符")

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
