# -*- coding: utf-8 -*-
"""探针：验证"物理左键读取"这条兜底链在 Frida 17 下到底能不能用。

背景：04_knife / 23_fast_gunstock 的"左键防卡死"兜底里，第一道门是

    if (physicalLeftDown() !== false) return false;   // true=按着 / null=读不到 -> 不动

如果 `Module.getGlobalExportByName('GetAsyncKeyState')` 在 Frida 17 里不存在（Frida 17
移除了 Module 的静态方法），而 user32 回退又拿不到，physicalLeftDown() 会恒返回 null，
于是这个兜底就永远不生效——这正是"日志里从来没有出现过【已撤销 fireBtnPressed】"的一个候选解释。

本探针在真实进程（32 位 ia32，与游戏同架构）里逐条报告：
  1. typeof Module.getGlobalExportByName / findExportByName / getExportByName
  2. Process.findModuleByName('user32.dll') 是否拿得到
  3. module.findExportByName / module.getExportByName 是否拿得到 GetAsyncKeyState
  4. 真调用 GetAsyncKeyState(0x01) 的原始返回值（是否 throws）
"""

import sys

import frida

TARGET = r"C:\Windows\SysWOW64\cmd.exe"
TARGET_ARGS = ["/k", "echo async-keystate-probe-ready"]

AGENT = r"""
var report = {};

function safe(label, fn) {
  try { report[label] = fn(); } catch (e) { report[label] = 'THROW: ' + e.message; }
}

safe('arch', function () { return Process.arch + '/' + Process.pointerSize; });
safe('frida_version', function () { return Frida.version; });
safe('typeof_Module_getGlobalExportByName', function () { return typeof Module.getGlobalExportByName; });
safe('typeof_Module_findExportByName', function () { return typeof Module.findExportByName; });
safe('typeof_Module_getExportByName', function () { return typeof Module.getExportByName; });

safe('globalExport', function () {
  if (typeof Module.getGlobalExportByName !== 'function') return 'NOT_A_FUNCTION';
  var p = Module.getGlobalExportByName('GetAsyncKeyState');
  return p ? p.toString() : 'null';
});

safe('user32_found', function () {
  var u = Process.findModuleByName('user32.dll');
  return u ? (u.name + ' @ ' + u.base) : 'null';
});

safe('user32_findExportByName', function () {
  var u = Process.findModuleByName('user32.dll');
  if (!u) return 'no-user32';
  var p = u.findExportByName('GetAsyncKeyState');
  return p ? p.toString() : 'null';
});

safe('user32_getExportByName', function () {
  var u = Process.findModuleByName('user32.dll');
  if (!u) return 'no-user32';
  var p = u.getExportByName('GetAsyncKeyState');
  return p ? p.toString() : 'null';
});

// 逐个试用候选返回类型：`short` 是否合法？（脚本里用的就是 'short'）
safe('retType_matrix', function () {
  var u = Process.findModuleByName('user32.dll');
  if (!u) return 'no-user32';
  var p = u.findExportByName('GetAsyncKeyState');
  if (!p) return 'no-export';
  var types = ['short', 'int16', 'uint16', 'sshort', 'int', 'BOOL'];
  var out = [];
  for (var i = 0; i < types.length; i++) {
    var t = types[i];
    try {
      var fn = new NativeFunction(p, t, ['int']);
      var raw = fn(0x01);
      out.push(t + '=OK(raw=' + raw + ',down=' + ((raw & 0x8000) !== 0) + ')');
    } catch (e) {
      out.push(t + '=THROW(' + e.message + ')');
    }
  }
  return out.join(' | ');
});

// 真正调用一次，看原始返回值（脚本原样的 'short'）
safe('call_with_short_like_script', function () {
  var u = Process.findModuleByName('user32.dll');
  if (!u) return 'no-user32';
  var p = u.findExportByName('GetAsyncKeyState');
  if (!p) return 'no-export';
  var fn = new NativeFunction(p, 'short', ['int']);   // ← 与 04/23 脚本里完全一致的写法
  var raw = fn(0x01);
  return 'raw=' + raw;
});

// 把两个脚本里的 physicalLeftDown() 原样搬进来，旧写法 / 新写法各跑一次
function physicalLeftDown_old() {
  try {
    var fn = Module.getGlobalExportByName('GetAsyncKeyState');
    var f = new NativeFunction(fn, 'short', ['int']);     // ← 修复前的写法（04/23 原样）
    return ((f(0x01) & 0x8000) !== 0);
  } catch (e) { return null; }                            // ← 原样的 catch：异常被吞 -> 恒 null
}
function physicalLeftDown_new() {
  try {
    var fn = Module.getGlobalExportByName('GetAsyncKeyState');
    var f = new NativeFunction(fn, 'uint16', ['int']);    // ← 修复后的写法
    return ((f(0x01) & 0x8000) !== 0);
  } catch (e) { return null; }
}

safe('physicalLeftDown_old', function () { return String(physicalLeftDown_old()); });
safe('physicalLeftDown_new', function () { return String(physicalLeftDown_new()); });

// 模拟 clearStuckFireBtn 的第一道门：`if (physicalLeftDown() !== false) return false;`
safe('guard_first_gate', function () {
  var o = physicalLeftDown_old();
  var n = physicalLeftDown_new();
  return '旧: ' + (o !== false ? '拦住(永不撤销 fireBtnPressed)' : '放行(会撤销)')
    + ' | 新: ' + (n !== false ? '拦住' : '放行(会撤销)');
});

// 顺带确认 Frida 自己有没有 input/键盘 API 可用作替代
safe('typeof_Process_enumerateModules', function () { return typeof Process.enumerateModules; });
safe('typeof_SendInput', function () {
  var u = Process.findModuleByName('user32.dll');
  if (!u) return 'no-user32';
  var p = u.findExportByName('GetKeyState');
  return p ? 'GetKeyState@' + p : 'null';
});

send({ t: 'report', data: report });
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

    print("[=] report")
    for k, v in box.items():
        print(f"    {k} = {v}")

    ok = (
        box.get("typeof_Module_getGlobalExportByName") == "function"
        and str(box.get("globalExport", "")).startswith("0x")
        and "int16=OK" in str(box.get("retType_matrix", ""))
    )
    print("[=] VERDICT:", "物理按键读取链可用" if ok else "物理按键读取链有断点（见上表）")

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
