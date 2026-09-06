"""Attach the read-only fast-stock probe to an already-running game process."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import argparse
import json
import sys
import time

import frida


PROCESS_NAME = "UnityCrossFire.exe"
ROOT = Path(__file__).resolve().parent
SCRIPTS = {
    "probe": ROOT / "AAAAA-fast_stock_hit_probe_min.js",
    "bypass": ROOT / "AAAAA-fast_stock_hit_stun_bypass_min.js",
    "precise": ROOT / "AAAAA-fast_stock_hit_stun_precise_min.js",
    "wait": ROOT / "AAAAA-fast_stock_hit_stun_wait_min.js",
    "anim": ROOT / "AAAAA-fast_stock_anim_boost_min.js",
    "gate": ROOT / "AAAAA-fast_stock_gate_probe_min.js",
    "unlock": ROOT / "AAAAA-fast_stock_damage_unlock_min.js",
    "hurt": ROOT / "AAAAA-fast_stock_natural_unlock_hurt_probe_min.js",
}


def write_log(handle, record: dict) -> None:
    line = json.dumps(record, ensure_ascii=False, sort_keys=True)
    handle.write(line + "\n")
    handle.flush()
    print(line, flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="极速枪托测试运行程序")
    parser.add_argument("--mode", choices=("probe", "bypass", "precise", "wait", "anim", "gate", "unlock", "hurt"), default="probe")
    args = parser.parse_args()
    script_path = SCRIPTS[args.mode]
    log_path = ROOT / ("fast_stock_hit_" + args.mode + "_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".log")

    if not script_path.is_file():
        print(f"测试脚本不存在：{script_path}", file=sys.stderr)
        return 2

    try:
        session = frida.attach(PROCESS_NAME)
    except frida.ProcessNotFoundError:
        print("未找到 UnityCrossFire.exe。请先启动游戏并进入可测试房间，再运行本程序。", file=sys.stderr)
        return 3

    with log_path.open("a", encoding="utf-8") as handle:
        def on_message(message: dict, data: bytes | None) -> None:
            record = {"host_at": datetime.now().isoformat(timespec="milliseconds"), "message": message}
            if data is not None:
                record["binary_size"] = len(data)
            write_log(handle, record)

        script = session.create_script(script_path.read_text(encoding="utf-8"))
        script.on("message", on_message)
        script.load()

        try:
            result = script.exports_sync.enable()
            write_log(handle, {"host_at": datetime.now().isoformat(timespec="milliseconds"), "event": "feature_enable_result", "mode": args.mode, "result": result})
            if args.mode == "probe":
                print("只读探测已启用。依次做 5 次空枪托、5 次命中枪托；按 Ctrl+C 结束。", flush=True)
            elif args.mode == "bypass":
                print("命中硬直旁路已启用。测试空枪托和命中枪托是否同速；按 Ctrl+C 恢复原函数。", flush=True)
            elif args.mode == "precise":
                print("精确验证已启用。命中镜头反馈会保留，仅恢复本地枪托动画速度；按 Ctrl+C 结束。", flush=True)
            elif args.mode == "wait":
                print("命中等待缩短验证已启用。镜头反馈会保留，本地命中等待改为 0 秒；按 Ctrl+C 结束。", flush=True)
            elif args.mode == "anim":
                print("枪托动画加速验证已启用。伤害仍由原动画事件触发；按 Ctrl+C 结束。", flush=True)
            elif args.mode == "gate":
                print("枪托解锁时序探测已启用。交替测试空枪托和命中枪托；按 Ctrl+C 结束。", flush=True)
            else:
                print("伤害后提前解锁验证已启用。伤害仍走原事件；按 Ctrl+C 结束。", flush=True)
            while True:
                time.sleep(0.25)
        except KeyboardInterrupt:
            print("正在清理探测 Hook…", flush=True)
        finally:
            try:
                result = script.exports_sync.cleanup()
                write_log(handle, {"host_at": datetime.now().isoformat(timespec="milliseconds"), "event": "feature_cleanup_result", "mode": args.mode, "result": result})
            finally:
                script.unload()
                session.detach()

    print(f"日志已保存：{log_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
