from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_field_relation_graphs as graphs


def format_fields(fields: list[dict[str, str]]) -> str:
    if not fields:
        return "-"
    return "；".join(f"`{field['name']}`: `{field['type']}`" for field in fields)


def format_relation_map(
    mapping: dict[str, list[dict[str, str]]],
    blocks: dict[str, str],
) -> str:
    if not mapping:
        return "-"

    lines: list[str] = []
    for name, fields in sorted(mapping.items(), key=lambda item: item[0].lower()):
        source = "dump.cs 中有定义" if name in blocks else "dump.cs 中未发现定义/Unity或外部类型"
        lines.append(f"  - `{name}`（{source}）：{format_fields(fields)}")
    return "\n".join(lines)


def main() -> None:
    text = graphs.DUMP.read_text(encoding="utf-8", errors="ignore")
    graphs.DELEGATE_TYPES = graphs.discover_delegate_types(text)
    blocks = graphs.class_blocks(text)
    all_fields = {name: graphs.fields_from_body(body) for name, body in blocks.items()}

    generated = graphs.collect_render_targets(all_fields)
    generated_set = set(generated)
    seen_nodes: set[str] = set()
    generated_relations: dict[str, tuple[dict[str, list[dict[str, str]]], dict[str, list[dict[str, str]]]]] = {}

    for target in generated:
        own, external = graphs.field_relation_summary(target, all_fields)
        generated_relations[target] = (own, external)
        seen_nodes.update(own)
        seen_nodes.update(external)

    ungenerated = sorted(seen_nodes - generated_set, key=str.lower)

    lines: list[str] = []
    lines.append("# 字段关系图生成统计\n\n")
    lines.append(
        "统计口径：只统计 `dump.cs` 的字段声明关系；包含静态字段、泛型字段、嵌套类型字段；"
        "排除基础值、委托/事件、编译器生成类。方法参数、返回值、属性内部逻辑和 IDA 运行时调用链不在本表内。\n\n"
    )
    lines.append(f"- 已生成 HTML 的类：{len(generated)} 个\n")
    lines.append(f"- 未生成 HTML 但已出现在这些图里的类/类型：{len(ungenerated)} 个\n")
    lines.append(f"- 统计文件来源：`{graphs.DUMP.relative_to(graphs.ROOT)}`\n")
    lines.append(f"- HTML 输出目录：`{graphs.OUT.relative_to(graphs.ROOT)}`\n\n")

    lines.append("## 已生成 HTML 的类\n\n")
    for target in generated:
        own, external = generated_relations[target]
        lines.append(f"### {target}\n\n")
        lines.append(f"- HTML：`{target}字段关系图.html`\n")
        lines.append(f"- 谁保存了这个类：{len(external)} 个\n")
        lines.append(format_relation_map(external, blocks) + "\n")
        lines.append(f"- 它保存了哪些类型：{len(own)} 个\n")
        lines.append(format_relation_map(own, blocks) + "\n\n")

    lines.append("## 未生成 HTML 但已出现在图里的类/类型\n\n")
    for target in ungenerated:
        if target in blocks:
            own, external = graphs.field_relation_summary(target, all_fields)
            source = "dump.cs 中有定义，可继续生成独立关系图"
        else:
            own, external = {}, {}
            source = "dump.cs 中未发现同名 class/struct 定义，多数是 Unity/外部类型、枚举或嵌套类型显示名"

        lines.append(f"### {target}\n\n")
        lines.append("- HTML：未生成\n")
        lines.append(f"- 类型来源：{source}\n")
        lines.append(f"- 谁保存了这个类：{len(external)} 个\n")
        lines.append(format_relation_map(external, blocks) + "\n")
        lines.append(f"- 它保存了哪些类型：{len(own)} 个\n")
        lines.append(format_relation_map(own, blocks) + "\n\n")

    output = graphs.DOC_OUT / "字段关系图-已生成与未生成类统计.md"
    output.write_text("".join(lines), encoding="utf-8")
    print(output)
    print(f"generated={len(generated)} ungenerated={len(ungenerated)}")


if __name__ == "__main__":
    main()
