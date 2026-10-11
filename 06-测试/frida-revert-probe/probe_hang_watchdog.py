# -*- coding: utf-8 -*-
"""探针：端到端验证「卡死看门狗」在真实卡死进程里能不能工作。

24_bot_pause 的看门狗做法（只用 Interceptor + Frida JS 线程）：
  1. 游戏主线程每帧调用的函数当心跳（ModeBase.Update）；
  2. 在一批可疑函数上留面包屑（环形缓冲，最近 64 条：时间/名字/线程号）；
  3. JS 线程 setInterval 每秒巡检，超过阈值没心跳 => 判定卡死，把面包屑倒进日志。

本探针在 32 位进程里造一个"永不停止的线程"（纯机器码死循环：Sleep(1) + GetTickCount），
并**刻意不调用心跳函数**（模拟主线程卡死），验证：
  a) 别的线程死循环时，JS 线程的 setInterval 是否还能按时触发；
  b) 面包屑是否被正确记录，且**名字不会全变成最后一个**（闭包陷阱）；
  c) 判定卡死后能否把缓冲完整倒出来。
"""

import sys
import time

import frida

TARGET = r"C:\Windows\SysWOW64\cmd.exe"
TARGET_ARGS = ["/k", "echo hang-watchdog-probe-ready"]

AGENT = r"""
var HANG_IDLE_MS = 2500;          // 探针里缩短，省时间
var report = { logs: [], hangDetected: false, ticks: 0 };
var started = Date.now();

function log(msg) { report.logs.push('+' + (Date.now() - started) + 'ms ' + msg); }

var watch = { lastPulseAt: 0, pulses: 0, dumped: false, busy: false, buf: [], seq: 0, hooks: [] };

function noteBreadcrumb(name) {
  try {
    watch.buf.push({ t: Date.now(), n: name, tid: Process.getCurrentThreadId(), s: ++watch.seq });
    if (watch.buf.length > 64) watch.buf.shift();
  } catch (_) {}
}

function flushBreadcrumbs(idleMs) {
  var first = watch.buf[0].t;
  var last = watch.buf[watch.buf.length - 1];
  var lines = [];
  for (var i = 0; i < watch.buf.length; i++) {
    var e = watch.buf[i];
    lines.push('#' + e.s + ' +' + (e.t - first) + 'ms ' + e.n + ' tid' + e.tid);
  }
  for (var j = 0; j < lines.length; j += 4) {
    log('面包屑[' + (Math.floor(j / 4) + 1) + ']: ' + lines.slice(j, j + 4).join(' | '));
  }
  log('最后一次面包屑 = ' + last.n + '，距今 ' + (Date.now() - last.t) + 'ms；主线程已静默 ' + idleMs + 'ms');
}

log('step1: 开始');

var k32 = Process.findModuleByName('kernel32.dll');
// 32 位 Windows API 是 stdcall —— 显式声明 ABI，别让它按默认（sysv/cdecl）去调
var Sleep = new NativeFunction(k32.findExportByName('Sleep'), 'void', ['uint'], 'stdcall');
var GetTickCount = new NativeFunction(k32.findExportByName('GetTickCount'), 'uint', [], 'stdcall');
var CreateThread = new NativeFunction(k32.findExportByName('CreateThread'), 'pointer',
  ['pointer', 'uint', 'pointer', 'pointer', 'uint', 'pointer'], 'stdcall');
log('step2: WinAPI 已解析 Sleep/tick/thread');

// 纯机器码死循环线程：
//   6A 01              push 1
//   FF 15 <Sleep>      call [Sleep]
//   FF 15 <Tick>       call [GetTickCount]      <- 面包屑观测点
//   EB F0              jmp 到第 0 字节
var sleepMs = 50;                 // 20 次/秒 —— 贴近真实看门狗的观测点调用频率
var page = Memory.alloc(Process.pageSize);
Memory.protect(page, Process.pageSize, 'rwx');
var code = [0x6A, 0x32, 0xFF, 0x15];
function abs32(p) { var a = p.toInt32(); return [a & 0xff, (a >> 8) & 0xff, (a >> 16) & 0xff, (a >> 24) & 0xff]; }
// 注意：`FF 15 <abs>` 是「间接调用」—— abs 处必须放**函数指针**，不能直接放函数地址。
// 上一版把函数地址直接写在操作数里，线程一起来就 call 到垃圾地址 -> 线程立即死掉（所以面包屑一条都没有）。
var slotSleep = page.add(0x10);
var slotTick = page.add(0x14);
code = code.concat(abs32(slotSleep));
code.push(0xFF, 0x15);
code = code.concat(abs32(slotTick));
code.push(0xEB, 0xF0);
page.writeByteArray(code);
page.add(0x10).writePointer(Sleep);
page.add(0x14).writePointer(GetTickCount);
log('step2b: stub=' + page + ' 机器码=' + JSON.stringify(code) + ' Sleep@' + Sleep + ' Tick@' + GetTickCount);

// 面包屑钩子：用工厂函数包一层，验证不会出现"名字全是最后一个"的闭包陷阱
(function (label, target) {
  watch.hooks.push(Interceptor.attach(target, {
    onEnter: function () {
      if (watch.seq === 0) send({ t: 'stage', msg: 'hook-first（死循环线程确实在跑，Hook 确实在触发）' });
      noteBreadcrumb(label);
    }
  }));
})('GetTickCount', GetTickCount);

var h = CreateThread(ptr(0), 0, page, ptr(0), 0, ptr(0));
log('step3: 死循环线程已创建 handle=' + h + ' stub=' + page);

// 短定时器：用来判断"JS 线程还活着吗"（如果它到了、而最终报告没到，就是被热点 Hook 卡住了）
setTimeout(function () { send({ t: 'stage', msg: 'timer-500 到了（JS 线程正常）' }); }, 500);
setTimeout(function () { send({ t: 'stage', msg: 'timer-2000 到了，此时面包屑条数=' + watch.buf.length + ' 总次数=' + watch.seq }); }, 2000);

// 心跳函数刻意不调用（watchPulse 不实现）=> 主线程静默

var timer = setInterval(function () {
  try {
    report.ticks++;
    if (watch.busy || watch.dumped) return;
    if (!watch.lastPulseAt) watch.lastPulseAt = 0;
    var since = watch.lastPulseAt ? (Date.now() - watch.lastPulseAt) : (Date.now() - started);
    if (since < HANG_IDLE_MS) return;
    watch.busy = true;
    watch.dumped = true;
    report.hangDetected = true;
    log('!!! 判定卡死：主线程超过 ' + since + 'ms 没有心跳，倒出面包屑');
    flushBreadcrumbs(since);
    watch.busy = false;
  } catch (e) { log('巡检异常: ' + e.message); }
}, 500);

setTimeout(function () {
  try { clearInterval(timer); } catch (_) {}
  report.bufLen = watch.buf.length;
  report.distinctNames = watch.buf.map(function (e) { return e.n; })
    .filter(function (v, i, a) { return a.indexOf(v) === i; }).join(',');
  report.bufTail = watch.buf.slice(-3).map(function (e) { return '#' + e.s + ' ' + e.n + ' tid' + e.tid; }).join(' | ');
  send({ t: 'report', data: report });
}, 6000);
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
        elif m.get("type") == "send" and m["payload"].get("t") == "stage":
            print("[stage]", m["payload"]["msg"])
        elif m.get("type") == "send":
            print("[agent]", m["payload"])
        else:
            print("[agent]", m)

    script.on("message", on_message)
    script.load()

    waited = 0.0
    while "logs" not in box and waited < 30:
        time.sleep(0.5)
        waited += 0.5

    for line in box.get("logs", []):
        print("   ", line)
    print("[=] 巡检次数:", box.get("ticks"), "| 缓冲条数:", box.get("bufLen"))
    print("[=] 面包屑里出现过的函数名:", box.get("distinctNames"))
    print("[=] 环形缓冲最后 3 条:", box.get("bufTail"))

    ok = box.get("hangDetected") is True and (box.get("bufLen") or 0) > 0 and "GetTickCount" in str(box.get("distinctNames"))
    print("[=] VERDICT:", "看门狗可用（别的线程死循环时仍能判定卡死并倒出面包屑）"
          if ok else "看门狗不可用，需要换方案")

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
