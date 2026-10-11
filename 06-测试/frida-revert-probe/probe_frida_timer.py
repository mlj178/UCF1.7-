# -*- coding: utf-8 -*-
"""探针：Frida 的 setTimeout/setInterval 在 spawn（挂起态）目标里到底会不会触发？

上一版看门狗探针里脚本体同步执行正常，但 `setTimeout`/`setInterval` 的回调一次都没跑
（报告始终没到），需要先把这条前提查清楚：是"没 resume 进程"导致，还是别的。

判据：同一段脚本，在 resume 前 / resume 后 各挂一个 1s 定时器，看哪个会 send 回来。
"""

import sys
import time

import frida

TARGET = r"C:\Windows\SysWOW64\cmd.exe"
TARGET_ARGS = ["/k", "echo frida-timer-probe-ready"]

AGENT = r"""
var n = 0;
send({ t: 'sync', msg: 'script body executed', hasSetTimeout: (typeof setTimeout), hasSetInterval: (typeof setInterval) });

rpc.exports = {
  arm: function (tag) {
    setTimeout(function () {
      n++;
      send({ t: 'timer', msg: 'fired: ' + tag, n: n, at: Date.now() });
    }, 1000);
    var iv = setInterval(function () {
      send({ t: 'interval', msg: 'tick: ' + tag });
      clearInterval(iv);
    }, 1000);
    return { ok: true, tag: tag };
  }
};
"""


def main():
    msgs = []
    pid = frida.spawn([TARGET] + TARGET_ARGS)
    device = frida.get_local_device()
    session = device.attach(pid)
    script = session.create_script(AGENT)
    script.on("message", lambda m, d: msgs.append(m.get("payload", m)))
    script.load()

    script.exports_sync.arm("before-resume")
    print("[i] 挂起态等待 2.5s ...")
    time.sleep(2.5)
    before = [m for m in msgs if isinstance(m, dict) and m.get("t") in ("timer", "interval")]
    print("[=] resume 前收到的定时器回调:", before)

    device.resume(pid)
    print("[i] 已 resume，等待 2.5s ...")
    time.sleep(2.5)
    after = [m for m in msgs if isinstance(m, dict) and m.get("t") in ("timer", "interval")]
    print("[=] resume 后累计定时器回调:", after)

    script.exports_sync.arm("after-resume")
    time.sleep(2.0)
    final = [m for m in msgs if isinstance(m, dict) and m.get("t") in ("timer", "interval")]
    print("[=] 最终累计定时器回调:", final)
    print("[=] sync 消息:", [m for m in msgs if isinstance(m, dict) and m.get("t") == "sync"])

    ok = len(before) == 0 and len(final) >= 3
    print("[=] VERDICT:", "定时器需要先 resume 进程（挂起态下不触发）" if ok else "结论与预期不同，见上面数据")

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
