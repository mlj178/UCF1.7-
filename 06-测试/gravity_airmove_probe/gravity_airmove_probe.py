"""只读的高跳空中水平移动诊断探针。"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path
import threading
import time
from typing import Any


def build_log_paths(directory: str | Path, label: str, timestamp: str) -> tuple[Path, Path]:
    """返回指定版本标签和时间戳对应的事件、摘要日志路径。"""
    if label not in {"2.4", "2.5"}:
        raise ValueError("label 必须为 '2.4' 或 '2.5'")
    root = Path(directory)
    prefix = f"gravity_airmove_{label}_{timestamp}"
    return root / f"{prefix}.jsonl", root / f"{prefix}_summary.json"


@dataclass
class SessionSummary:
    """聚合来自只读 Frida 探针的结构化事件。"""

    label: str
    event_count: int = 0
    airborne_samples: int = 0
    readable_horizontal_moves: int = 0
    errors: int = 0
    hooks_installed: int = 0
    hook_hits: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def observe(self, event: dict[str, Any]) -> None:
        self.event_count += 1
        event_type = event.get("type")
        if event_type == "player_snapshot" and event.get("grounded") is False:
            self.airborne_samples += 1
        elif event_type == "controller_move" and event.get("vector_readable") is True:
            self.readable_horizontal_moves += 1
        elif event_type == "probe_error":
            self.errors += 1
        elif event_type == "hook_installed":
            self.hooks_installed += 1
        elif event_type == "hook_hit":
            self.hook_hits += 1
        elif event_type == "probe_metadata":
            self.metadata.update(event)

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "event_count": self.event_count,
            "airborne_samples": self.airborne_samples,
            "readable_horizontal_moves": self.readable_horizontal_moves,
            "errors": self.errors,
            "hooks_installed": self.hooks_installed,
            "hook_hits": self.hook_hits,
            "metadata": self.metadata,
        }


def choose_target(processes: list[dict[str, Any]]) -> dict[str, Any] | None:
    """仅当本机恰有一个 UnityCrossFire 进程时返回它。"""
    matches = [
        process
        for process in processes
        if "unitycrossfire" in str(process.get("name", "")).lower()
    ]
    return matches[0] if len(matches) == 1 else None


def _write_event(handle: Any, summary: SessionSummary, event: dict[str, Any]) -> None:
    event.setdefault("host_timestamp", datetime.now().astimezone().isoformat(timespec="milliseconds"))
    handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    handle.flush()
    summary.observe(event)


def run_probe(label: str, poll_seconds: float = 1.0) -> int:
    """等待唯一游戏进程，加载只读观察脚本，并持续写入会话日志。"""
    root = Path(__file__).resolve().parent
    logs_dir = root / "logs"
    logs_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    event_path, summary_path = build_log_paths(logs_dir, label, timestamp)
    summary = SessionSummary(label=label)
    session = None
    return_code = 0
    session_detached = threading.Event()

    with event_path.open("w", encoding="utf-8") as event_file:
        try:
            try:
                import frida
            except ImportError as error:
                raise RuntimeError("未找到 Frida Python 运行库") from error
            device = frida.get_local_device()
            while True:
                processes = [
                    {"pid": process.pid, "name": process.name}
                    for process in device.enumerate_processes()
                ]
                target = choose_target(processes)
                if target is not None:
                    break
                _write_event(event_file, summary, {"type": "waiting_for_game"})
                time.sleep(poll_seconds)

            _write_event(event_file, summary, {"type": "target_found", **target})
            session = device.attach(target["pid"])

            def on_detached(reason: Any, crash: Any) -> None:
                _write_event(event_file, summary, {
                    "type": "session_detached",
                    "reason": str(reason),
                    "crash": str(crash) if crash is not None else None,
                })
                session_detached.set()

            session.on("detached", on_detached)
            source = (root / "gravity_airmove_probe.js").read_text(encoding="utf-8")
            script = session.create_script(source)

            def on_message(message: dict[str, Any], _data: Any) -> None:
                if message.get("type") == "send" and isinstance(message.get("payload"), dict):
                    _write_event(event_file, summary, message["payload"])
                elif message.get("type") == "error":
                    _write_event(event_file, summary, {
                        "type": "probe_error",
                        "message": message.get("description", "Frida script error"),
                    })

            script.on("message", on_message)
            script.load()
            _write_event(event_file, summary, {"type": "probe_attached", **target})

            while not session_detached.wait(0.2):
                pass
        except KeyboardInterrupt:
            _write_event(event_file, summary, {"type": "probe_stopped", "reason": "keyboard_interrupt"})
            return_code = 0
        except Exception as error:
            _write_event(event_file, summary, {"type": "probe_error", "message": str(error)})
            return_code = 1
        else:
            return_code = 0
        finally:
            if session is not None:
                try:
                    session.detach()
                    _write_event(event_file, summary, {"type": "probe_detached"})
                except Exception as error:
                    _write_event(event_file, summary, {"type": "probe_error", "message": str(error)})
            summary_path.write_text(
                json.dumps(summary.to_dict(), ensure_ascii=False, indent=2, sort_keys=True),
                encoding="utf-8",
            )
    return return_code


def main() -> int:
    parser = argparse.ArgumentParser(description="高跳空中移动只读探针")
    parser.add_argument("--label", choices=("2.4", "2.5"), required=True, help="本次测试的整合包版本")
    parser.add_argument("--poll-seconds", type=float, default=1.0, help="等待游戏进程的轮询间隔")
    args = parser.parse_args()
    if args.poll_seconds <= 0:
        parser.error("--poll-seconds 必须大于 0")
    return run_probe(args.label, args.poll_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
