"""自动检查 become_ghostblade 持久化日志。

用法：
  python check_logs.py                 # 检查 logs/ 下最新日志
  python check_logs.py path/to.log     # 检查指定日志
  python check_logs.py --all           # 检查 logs/ 下全部日志

退出码：0=通过/仅环境类提示；1=发现功能问题；2=无日志。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
FEATURE_ID = "become_ghostblade"
SUCCESS_MARKERS = (
    "local became ghostblade",
    "local_ghostblade applied",
)


def find_logs(all_logs: bool) -> list[Path]:
    if not LOG_DIR.exists():
        return []
    files = sorted(LOG_DIR.glob("become_ghostblade_ui_*.log"))
    if all_logs:
        return files
    return files[-1:]


def parse_rpc_statuses(text: str) -> list[dict]:
    statuses = []
    for line in text.splitlines():
        if "RPC_STATUS " not in line:
            continue
        payload = line.split("RPC_STATUS ", 1)[1].strip()
        try:
            obj = json.loads(payload)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            statuses.append(obj)
    return statuses


def evaluate(statuses: list[dict], raw: str) -> tuple[str, list[str], list[str]]:
    problems: list[str] = []
    notes: list[str] = []

    if not statuses:
        if "session_start" in raw:
            notes.append("日志已创建，但没有 RPC_STATUS（可能只是打开 UI 未操作）")
            return "INCOMPLETE", problems, notes
        problems.append("日志中没有可解析的 RPC_STATUS")
        return "FAIL", problems, notes

    last = statuses[-1]
    enabled = bool(last.get("enabled"))
    local_applied = int(last.get("local_ghostblade_applied") or 0)
    bot_applied = int(last.get("bot_ghostblade_applied") or 0)
    error_count = int(last.get("error_count") or 0)
    last_result = str(last.get("last_result") or "")
    last_error = str(last.get("last_error") or "")
    last_action = str(last.get("last_action") or "")
    total_applied = local_applied + bot_applied

    notes.append(
        f"最后一次状态: enabled={enabled}, action={last_action or '-'}, "
        f"local={local_applied}, bot={bot_applied}, errors={error_count}, "
        f"result={last_result or '-'}, error={last_error or '-'}"
    )

    if error_count > 0:
        problems.append(f"累计错误 error_count={error_count}: {last_error or last_result}")

    if last_result.startswith("rejected"):
        problems.append(f"最近一次被拒绝: {last_error or last_result}")
        if last_action:
            return "FAIL", problems, notes

    if last_result.startswith("skipped"):
        notes.append(f"最近一次跳过（常见于非佣兵/已死亡）: {last_result}")
        if last_action and total_applied == 0:
            return "WARN", problems, notes

    if last_error and "not in Nano6" in last_error:
        problems.append("当前不在生化6/剑客模式，功能按设计拒绝执行")
    if last_error and "Mode_Nano6.instance3 is unavailable" in last_error:
        problems.append("Mode_Nano6 实例不可用，可能是剑客模式未就绪")
    if last_error and "feature is disabled" in last_error:
        problems.append("功能开关未打开就点了变身按钮")
    if last_error and "local player is unavailable" in last_error:
        problems.append("本地玩家指针不可用（可能未进房）")

    has_text_success = any(marker in raw for marker in SUCCESS_MARKERS)
    if total_applied > 0 or has_text_success:
        if not enabled:
            problems.append("日志显示已成功变身，但最终 enabled=False（可能随后关闭了开关）")
            return "WARN", problems, notes
        return "PASS", problems, notes

    if any(s.get("pending") for s in statuses):
        notes.append("存在 pending 且未消费的动作，可能等待 ModeBase.Update 主线程")
        return "INCOMPLETE", problems, notes

    if any(s.get("last_result") == "queued" for s in statuses[-3:]):
        notes.append("最近动作仍在 queued，主线程可能未消费（未进对局/未 Update）")
        return "INCOMPLETE", problems, notes

    actions = [s for s in statuses if s.get("last_action")]
    if actions and total_applied == 0 and not problems:
        problems.append("执行过变身动作，但 local/bot applied 均为 0")
        problems.append(
            "可能原因：模式不对 / 角色不是佣兵 / 实例不可用 / Bot 列表为空；"
            f"请对照 last_result={last_result or '-'} last_error={last_error or '-'}"
        )
        return "FAIL", problems, notes

    notes.append("只有开关/状态轮询，尚未触发变身动作")
    return "INCOMPLETE", problems, notes


def report(path: Path, verdict: str, problems: list[str], notes: list[str]) -> int:
    print(f"LOG: {path}")
    print(f"VERDICT: {verdict}")
    for note in notes:
        print(f"  NOTE  {note}")
    for problem in problems:
        print(f"  PROB  {problem}")
    if verdict in {"PASS", "WARN", "INCOMPLETE"}:
        print("RESULT: " + ("OK" if verdict == "PASS" else verdict))
        return 0
    print("RESULT: FAIL")
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=f"检查 {FEATURE_ID} 持久化日志")
    parser.add_argument("path", nargs="?", help="日志文件路径；省略则用 logs/ 最新文件")
    parser.add_argument("--all", action="store_true", help="检查 logs/ 下全部日志")
    args = parser.parse_args(argv)

    if args.path:
        paths = [Path(args.path)]
        if not paths[0].is_file():
            print("RESULT: FAIL")
            print(f"  PROB  日志不存在: {paths[0]}")
            return 2
    else:
        paths = find_logs(args.all)
        if not paths:
            print("RESULT: FAIL")
            print(f"  PROB  未找到日志目录/文件: {LOG_DIR}")
            print("  NOTE  请先运行 AAAAA-become_ghostblade_ui.py 并完成游戏内测试")
            return 2

    exit_code = 0
    for path in paths:
        raw = path.read_text(encoding="utf-8", errors="replace")
        statuses = parse_rpc_statuses(raw)
        verdict, problems, notes = evaluate(statuses, raw)
        exit_code = max(exit_code, report(path, verdict, problems, notes))
        if path != paths[-1]:
            print("-" * 40)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
