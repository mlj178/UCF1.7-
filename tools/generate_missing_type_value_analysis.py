from __future__ import annotations

import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_field_relation_graphs as graphs


HIGH_KEYWORDS = (
    "GameMode",
    "WeaponLimited",
    "Weapon",
    "WPN_",
    "Bot",
    "ModeBase_Nano",
    "Nano",
    "DamageEventData",
    "DeathEventData",
    "HealthData",
    "Player",
    "MapGun",
    "MapTrigger",
    "SpawnPoint",
    "Team",
)

MID_KEYWORDS = (
    "HUD_",
    "UI_",
    "Camera",
    "Character",
    "Recoil",
    "Buff",
    "EffectObj",
    "ThermalVision",
    "TombStone",
    "NameKeyPool",
    "SimpleObjectPool",
)

LOW_NAMES = {
    "Transform",
    "Vector2",
    "Vector2Int",
    "Vector3",
    "GameObject",
    "Text",
    "RawImage",
    "Texture",
    "Texture2D",
    "Material",
    "Renderer",
    "Animator",
    "AudioClip",
    "Camera",
    "Coroutine",
    "ParticleSystem",
}


def priority_for(name: str) -> tuple[str, str]:
    if name in LOW_NAMES:
        return "低", "Unity/表现层基础类型，本身不是业务入口，通常作为字段证据或资源挂点参考。"
    if any(key in name for key in HIGH_KEYWORDS):
        return "高", "和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。"
    if any(key in name for key in MID_KEYWORDS):
        return "中", "偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。"
    return "中", "在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。"


def format_names(mapping: dict[str, list[dict[str, str]]], limit: int = 8) -> str:
    if not mapping:
        return "-"
    names = sorted(mapping)
    shown = names[:limit]
    suffix = "" if len(names) <= limit else f" 等 {len(names)} 个"
    return "、".join(f"`{name}`" for name in shown) + suffix


def field_evidence(mapping: dict[str, list[dict[str, str]]], limit: int = 5) -> str:
    if not mapping:
        return "-"
    rows: list[str] = []
    for owner, fields in sorted(mapping.items(), key=lambda item: item[0].lower())[:limit]:
        field_text = "；".join(f"`{field['name']}`: `{field['type']}`" for field in fields[:3])
        rows.append(f"`{owner}` -> {field_text}")
    if len(mapping) > limit:
        rows.append(f"另有 {len(mapping) - limit} 个来源")
    return "；".join(rows)


def main() -> None:
    text = graphs.DUMP.read_text(encoding="utf-8", errors="ignore")
    graphs.DELEGATE_TYPES = graphs.discover_delegate_types(text)
    blocks = graphs.class_blocks(text)
    enums = set(re.findall(r"\b(?:public|private|protected|internal)?\s*enum\s+([A-Za-z_][\w.<>]*)\b", text))
    all_fields = {name: graphs.fields_from_body(body) for name, body in blocks.items()}

    render_targets = graphs.collect_render_targets(all_fields)
    generated = set(render_targets)
    seen_nodes: set[str] = set()
    for target in render_targets:
        own, external = graphs.field_relation_summary(target, all_fields)
        seen_nodes.update(own)
        seen_nodes.update(external)

    missing = sorted(seen_nodes - generated, key=str.lower)

    grouped: dict[str, list[str]] = {"高": [], "中": [], "低": []}
    details: dict[str, dict[str, str | int | bool]] = {}
    for name in missing:
        own, external = graphs.field_relation_summary(name, all_fields) if name in blocks else ({}, {})
        priority, reason = priority_for(name)
        grouped[priority].append(name)
        details[name] = {
            "defined": name in blocks,
            "enum": name in enums,
            "analysis": graphs.analysis_for_type(name),
            "priority": priority,
            "reason": reason,
            "who_count": len(external),
            "save_count": len(own),
            "who": format_names(external),
            "saves": format_names(own),
            "evidence": field_evidence(external),
        }

    lines: list[str] = []
    lines.append("# 未生成 HTML 类/类型功能分析\n\n")
    lines.append(
        "范围：这里只分析“已经出现在当前 10 张字段关系图里，但还没有生成独立 HTML”的类/类型。"
        "功能判断来自 `dump.cs` 的类名、字段名、字段类型，以及 Unity/CF 对局语义。\n\n"
    )
    lines.append(f"- 未生成项总数：{len(missing)} 个\n")
    lines.append(f"- 建议优先生成：{len(grouped['高'])} 个\n")
    lines.append(f"- 可按需求生成：{len(grouped['中'])} 个\n")
    lines.append(f"- 暂时可不生成：{len(grouped['低'])} 个\n\n")

    lines.append("## 优先级总览\n\n")
    for priority in ("高", "中", "低"):
        lines.append(f"### {priority}优先级（{len(grouped[priority])} 个）\n\n")
        lines.append("、".join(f"`{name}`" for name in grouped[priority]) + "\n\n")

    lines.append("## 详细分析\n\n")
    for priority in ("高", "中", "低"):
        lines.append(f"### {priority}优先级\n\n")
        for name in grouped[priority]:
            item = details[name]
            lines.append(f"#### {name}\n\n")
            if item["defined"]:
                definition = "有 class/struct 定义"
            elif item["enum"]:
                definition = "有 enum 定义"
            else:
                definition = "未发现同名 class/struct/enum，可能是 Unity 类型或外部类型"
            lines.append(f"- 功能分析：{item['analysis']}\n")
            lines.append(f"- 建议价值：{item['priority']}。{item['reason']}\n")
            lines.append(f"- dump.cs 定义：{definition}\n")
            lines.append(f"- 谁保存了这个类：{item['who_count']} 个，{item['who']}\n")
            lines.append(f"- 它保存了哪些类型：{item['save_count']} 个，{item['saves']}\n")
            lines.append(f"- 字段依据示例：{item['evidence']}\n\n")

    output = graphs.DOC_OUT / "未生成HTML类功能分析.md"
    output.write_text("".join(lines), encoding="utf-8")
    print(output)
    print(f"missing={len(missing)} high={len(grouped['高'])} mid={len(grouped['中'])} low={len(grouped['低'])}")


if __name__ == "__main__":
    main()
