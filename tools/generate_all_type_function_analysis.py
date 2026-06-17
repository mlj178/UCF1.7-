from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_field_relation_graphs as graphs
from generate_missing_type_value_analysis import priority_for


def format_names(mapping: dict[str, list[dict[str, str]]], limit: int = 10) -> str:
    if not mapping:
        return "-"
    names = sorted(mapping)
    shown = names[:limit]
    suffix = "" if len(names) <= limit else f" 等 {len(names)} 个"
    return "、".join(f"`{name}`" for name in shown) + suffix


def format_evidence(mapping: dict[str, list[dict[str, str]]], limit: int = 4) -> str:
    if not mapping:
        return "-"
    rows: list[str] = []
    for owner, fields in sorted(mapping.items(), key=lambda item: item[0].lower())[:limit]:
        field_text = "；".join(f"`{field['name']}`: `{field['type']}`" for field in fields[:3])
        rows.append(f"`{owner}` -> {field_text}")
    if len(mapping) > limit:
        rows.append(f"另有 {len(mapping) - limit} 个来源")
    return "；".join(rows)


def definition_kind(name: str, blocks: dict[str, str], enums: set[str]) -> str:
    if name in blocks:
        return "class/struct"
    if name in enums:
        return "enum"
    return "Unity/外部/嵌套显示名"


def main() -> None:
    text = graphs.DUMP.read_text(encoding="utf-8", errors="ignore")
    graphs.DELEGATE_TYPES = graphs.discover_delegate_types(text)
    blocks = graphs.class_blocks(text)
    enums = set(re.findall(r"\b(?:public|private|protected|internal)?\s*enum\s+([A-Za-z_][\w.<>]*)\b", text))
    all_fields = {name: graphs.fields_from_body(body) for name, body in blocks.items()}

    render_targets = graphs.collect_render_targets(all_fields)
    generated = set(render_targets)
    all_nodes = set(render_targets)
    relations: dict[str, tuple[dict[str, list[dict[str, str]]], dict[str, list[dict[str, str]]]]] = {}

    for target in render_targets:
        own, external = graphs.field_relation_summary(target, all_fields)
        relations[target] = (own, external)
        all_nodes.update(own)
        all_nodes.update(external)

    for target in sorted(all_nodes):
        if target not in relations:
            relations[target] = graphs.field_relation_summary(target, all_fields) if target in blocks else ({}, {})

    generated_nodes = sorted(generated, key=str.lower)
    missing_nodes = sorted(all_nodes - generated, key=str.lower)

    lines: list[str] = []
    lines.append("# 全部关系图类功能分析\n\n")
    lines.append(
        "范围：当前已生成 HTML 的类，以及这些 HTML 图中出现但还没有生成独立 HTML 的类/类型。"
        "功能判断来自 `dump.cs` 的字段声明、类名/字段名，以及 Unity/CF 对局语义。\n\n"
    )
    lines.append(f"- 已生成 HTML：{len(generated_nodes)} 个\n")
    lines.append(f"- 未生成 HTML：{len(missing_nodes)} 个\n")
    lines.append(f"- 合计分析：{len(all_nodes)} 个类/类型\n")
    lines.append("- 统计口径：字段关系；不包含方法参数、返回值、属性内部逻辑、IDA 运行时调用链。\n\n")

    lines.append("## 快速索引\n\n")
    lines.append("### 已生成 HTML\n\n")
    lines.append("、".join(f"`{name}`" for name in generated_nodes) + "\n\n")
    lines.append("### 未生成 HTML\n\n")
    lines.append("、".join(f"`{name}`" for name in missing_nodes) + "\n\n")

    for title, nodes, generated_flag in (
        ("已生成 HTML 的类", generated_nodes, True),
        ("未生成 HTML 的类/类型", missing_nodes, False),
    ):
        lines.append(f"## {title}\n\n")
        for name in nodes:
            own, external = relations[name]
            priority, reason = priority_for(name)
            html_name = f"HTML/{name}字段关系图.html" if generated_flag else "未生成"
            lines.append(f"### {name}\n\n")
            lines.append(f"- HTML：`{html_name}`\n")
            lines.append(f"- 定义类型：{definition_kind(name, blocks, enums)}\n")
            lines.append(f"- 功能分析：{graphs.analysis_for_type(name)}\n")
            lines.append(f"- 建议价值：{priority}。{reason}\n")
            lines.append(f"- 谁保存了这个类：{len(external)} 个，{format_names(external)}\n")
            lines.append(f"- 它保存了哪些类型：{len(own)} 个，{format_names(own)}\n")
            lines.append(f"- 字段依据示例：{format_evidence(external)}\n\n")

    output = graphs.DOC_OUT / "全部关系图类功能分析.md"
    output.write_text("".join(lines), encoding="utf-8")
    print(output)
    print(f"generated={len(generated_nodes)} missing={len(missing_nodes)} total={len(all_nodes)}")


if __name__ == "__main__":
    main()
