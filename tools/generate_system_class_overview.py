from __future__ import annotations

import html
import re
import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_field_relation_graphs as graphs
from generate_missing_type_value_analysis import priority_for


SYSTEMS = [
    ("对局总控与玩法规则", "回合流程、模式规则、阵营、复活、胜负和全局管理。"),
    ("玩家与战斗实体", "玩家、实体生命状态、移动输入、技能、速度和玩家数据。"),
    ("武器与伤害结算", "武器实例、武器数据、弹药、伤害事件、死亡事件和特殊击杀。"),
    ("Bot / AI / 寻路", "电脑玩家行为、索敌、寻路、跳跃连接、防守点和 AI 决策数据。"),
    ("地图与出生点", "地图枪、地图触发器、出生点、补给点和地图选择标识。"),
    ("纳米与特殊模式", "纳米/终结者模式角色、守卫、模式 HUD 和特殊玩法数据。"),
    ("HUD / UI / 计分板", "准星、小地图、记分板、击杀提示、房间界面和 UI 资源。"),
    ("角色模型与表现资源", "角色模型、皮肤、动画、语音、特效、材质和表现层资源。"),
    ("相机 / 视角 / 渲染", "相机管理、Cinemachine、热成像、后处理、渲染特性和视角缩放。"),
    ("数据结构 / 工具 / 对象池", "对象池、可订阅属性、加密数值、引用值、可序列化字典等支撑类型。"),
    ("Unity 基础组件 / 外部类型", "Transform、Vector、GameObject、Text、Sprite、Collider 等 Unity 基础类型。"),
]

UNITY_NAMES = {
    "Animation",
    "Animator",
    "AudioClip",
    "AudioSource",
    "BoxCollider",
    "Camera",
    "CharacterController",
    "Color",
    "Coroutine",
    "GameObject",
    "Image",
    "Material",
    "ParticleSystem",
    "RawImage",
    "RaycastHit",
    "RectTransform",
    "Renderer",
    "Rigidbody",
    "Sprite",
    "Text",
    "Texture",
    "Texture2D",
    "Transform",
    "TrailRenderer",
    "Vector2",
    "Vector2Int",
    "Vector3",
    "Vector3Int",
}


def system_for(name: str, analysis: str) -> str:
    value = f"{name} {analysis}"
    if name in UNITY_NAMES:
        return "Unity 基础组件 / 外部类型"
    if any(key in value for key in ("GameManager", "ModeBase", "GameMode", "WeaponLimited", "Team", "RespawnType")):
        return "对局总控与玩法规则"
    if any(key in value for key in ("Player", "Entity", "HealthData", "Skill", "Velocity", "Input", "Buff")):
        return "玩家与战斗实体"
    if any(key in value for key in ("Weapon", "WPN_", "Ammo", "Damage", "Death", "HeadShot", "SpecialKill", "Missile", "GhostBlade", "Wpn")):
        return "武器与伤害结算"
    if any(key in value for key in ("Bot", "AI", "Path", "Seeker", "GraphNode", "CrabStep", "Saunter")):
        return "Bot / AI / 寻路"
    if any(key in value for key in ("Map", "SpawnPoint", "地图", "出生", "补给", "Trigger")):
        return "地图与出生点"
    if any(key in value for key in ("Nano", "Terminator", "终结者", "纳米")):
        return "纳米与特殊模式"
    if any(key in value for key in ("HUD", "UI_", "TabScoreBoard", "Text", "Image", "RawImage", "KillMark", "Radar", "ScoreBoard", "RectTransform")):
        return "HUD / UI / 计分板"
    if any(key in value for key in ("Character", "Model", "Asset", "Voice", "Anim", "Effect", "Helmet", "Material", "Renderer", "GhostBladeOneShine")):
        return "角色模型与表现资源"
    if any(key in value for key in ("Camera", "Cinemachine", "ThermalVision", "VolumeProfile", "RendererFeature", "ForwardRendererData", "Fov")):
        return "相机 / 视角 / 渲染"
    if any(key in value for key in ("Pool", "Obscured", "Ref", "Subscribeable", "SerializableDictionary", "PropertyModifier", "Data", "Dictionary", "Test")):
        return "数据结构 / 工具 / 对象池"
    return "数据结构 / 工具 / 对象池"


def definition_kind(name: str, blocks: dict[str, str], enums: set[str]) -> str:
    if name in blocks:
        return "class/struct"
    if name in enums:
        return "enum"
    return "Unity/外部/嵌套类型"


def field_names(mapping: dict[str, list[dict[str, str]]], limit: int = 5) -> str:
    if not mapping:
        return "无"
    names = sorted(mapping)
    shown = "、".join(names[:limit])
    return shown if len(names) <= limit else f"{shown} 等 {len(names)} 个"


def evidence(mapping: dict[str, list[dict[str, str]]], limit: int = 2) -> str:
    if not mapping:
        return "无直接字段来源"
    rows: list[str] = []
    for owner, fields in sorted(mapping.items(), key=lambda item: item[0].lower())[:limit]:
        field_text = "；".join(f"{field['name']}: {field['type']}" for field in fields[:2])
        rows.append(f"{owner} -> {field_text}")
    if len(mapping) > limit:
        rows.append(f"另有 {len(mapping) - limit} 个来源")
    return "；".join(rows)


def collect_data():
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

    grouped: dict[str, list[dict[str, object]]] = {name: [] for name, _ in SYSTEMS}
    for name in sorted(all_nodes, key=str.lower):
        own, external = relations[name]
        analysis = graphs.analysis_for_type(name)
        priority, reason = priority_for(name)
        system = system_for(name, analysis)
        grouped[system].append(
            {
                "name": name,
                "analysis": analysis,
                "generated": name in generated,
                "priority": priority,
                "reason": reason,
                "kind": definition_kind(name, blocks, enums),
                "who_count": len(external),
                "save_count": len(own),
                "who": field_names(external),
                "saves": field_names(own),
                "evidence": evidence(external),
            }
        )
    return grouped, len(generated), len(all_nodes - generated), len(all_nodes)


def badge(text: str, cls: str) -> str:
    return f'<span class="badge {cls}">{html.escape(text)}</span>'


def render(link_prefix: str = "./HTML/") -> str:
    grouped, generated_count, missing_count, total_count = collect_data()
    nav = "\n".join(
        (
            f'<a href="#{html.escape(system)}" title="已生成/总数">'
            f'<span>{html.escape(system)}</span>'
            f'<strong>{sum(1 for item in grouped[system] if item["generated"])}/'
            f'{len(grouped[system])}</strong></a>'
        )
        for system, _ in SYSTEMS
    )
    sections: list[str] = []
    for system, desc in SYSTEMS:
        items = grouped[system]
        high = sum(1 for item in items if item["priority"] == "高")
        generated = sum(1 for item in items if item["generated"])
        missing = len(items) - generated
        rows: list[str] = []
        for item in items:
            name = str(item["name"])
            link = link_prefix + quote(f"{name}字段关系图.html")
            title = (
                f'<a class="class-name" href="{html.escape(link)}">{html.escape(name)}</a>'
                if item["generated"]
                else f'<span class="class-name">{html.escape(name)}</span>'
            )
            rows.append(
                f"""
        <article class="item">
          <div class="item-head">
            {title}
            <div class="badges">
              {badge("已生成HTML" if item["generated"] else "未生成HTML", "done" if item["generated"] else "todo")}
              {badge(str(item["priority"]) + "价值", "p-" + str(item["priority"]))}
              {badge(str(item["kind"]), "kind")}
            </div>
          </div>
          <p class="analysis">{html.escape(str(item["analysis"]))}</p>
          <dl>
            <div><dt>字段关系</dt><dd>被 {item["who_count"]} 个类保存；自身保存 {item["save_count"]} 种类型</dd></div>
            <div><dt>谁保存它</dt><dd>{html.escape(str(item["who"]))}</dd></div>
            <div><dt>它保存</dt><dd>{html.escape(str(item["saves"]))}</dd></div>
            <div><dt>依据示例</dt><dd>{html.escape(str(item["evidence"]))}</dd></div>
          </dl>
        </article>"""
            )
        sections.append(
            f"""
    <section id="{html.escape(system)}">
      <div class="section-head">
        <div>
          <h2>{html.escape(system)}</h2>
          <p>{html.escape(desc)}</p>
        </div>
        <div class="section-stats">
          <span>{len(items)} 个类型</span>
          <span>{generated}/{len(items)} 已/总</span>
          <span>{generated} 已生成</span>
          <span>{high} 高价值</span>
        </div>
      </div>
      <div class="items">
        {''.join(rows)}
      </div>
    </section>"""
        )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>类功能系统分类总览</title>
  <style>
    :root {{
      --bg:#f4f6f9; --panel:#ffffff; --ink:#1e2530; --muted:#667085; --line:#d7deea;
      --blue:#2463b8; --green:#24724c; --amber:#9a5b00; --red:#b42318; --soft:#f8fafc;
    }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:var(--bg); color:var(--ink); font-family:"Microsoft YaHei","Segoe UI",Arial,sans-serif; }}
    header {{ padding:28px 34px 18px; background:#fff; border-bottom:1px solid var(--line); position:sticky; top:0; z-index:3; }}
    h1 {{ margin:0 0 10px; font-size:28px; letter-spacing:0; }}
    .summary {{ display:flex; flex-wrap:wrap; gap:10px; color:var(--muted); font-size:14px; }}
    .summary span {{ padding:7px 10px; background:var(--soft); border:1px solid #e4e9f2; border-radius:6px; }}
    .layout {{ display:grid; grid-template-columns:280px minmax(0,1fr); gap:20px; padding:22px; }}
    nav {{ position:sticky; top:112px; align-self:start; display:flex; flex-direction:column; gap:8px; }}
    nav a {{ display:flex; justify-content:space-between; gap:10px; padding:10px 12px; color:var(--ink); text-decoration:none; background:#fff; border:1px solid var(--line); border-radius:6px; font-size:13px; }}
    nav strong {{ color:var(--blue); }}
    main {{ display:flex; flex-direction:column; gap:22px; min-width:0; }}
    section {{ background:#fff; border:1px solid var(--line); border-radius:8px; overflow:hidden; }}
    .section-head {{ display:flex; justify-content:space-between; gap:16px; padding:18px 20px; border-bottom:1px solid var(--line); background:#fbfcfe; }}
    h2 {{ margin:0 0 6px; font-size:21px; }}
    .section-head p {{ margin:0; color:var(--muted); font-size:13px; }}
    .section-stats {{ display:flex; flex-wrap:wrap; gap:8px; align-content:flex-start; justify-content:flex-end; min-width:220px; }}
    .section-stats span {{ padding:6px 9px; border:1px solid #dce3ee; border-radius:6px; color:#344054; background:#fff; font-size:12px; }}
    .items {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(360px,1fr)); gap:12px; padding:14px; }}
    .item {{ border:1px solid #e0e6ef; border-radius:8px; background:#fff; padding:14px; min-width:0; }}
    .item-head {{ display:flex; align-items:flex-start; justify-content:space-between; gap:12px; }}
    .class-name {{ font-weight:700; font-size:16px; color:#163b70; text-decoration:none; word-break:break-word; }}
    a.class-name:hover {{ text-decoration:underline; }}
    .badges {{ display:flex; flex-wrap:wrap; justify-content:flex-end; gap:5px; min-width:150px; }}
    .badge {{ display:inline-flex; align-items:center; height:24px; padding:0 7px; border-radius:5px; font-size:12px; white-space:nowrap; border:1px solid transparent; }}
    .done {{ color:#175c38; background:#ecfdf3; border-color:#b7e4c7; }}
    .todo {{ color:#6941c6; background:#f4f0ff; border-color:#d9d0ff; }}
    .p-高 {{ color:#9f1c16; background:#fff1f0; border-color:#ffc9c5; }}
    .p-中 {{ color:#875000; background:#fff7e6; border-color:#ffd591; }}
    .p-低 {{ color:#475467; background:#f2f4f7; border-color:#d0d5dd; }}
    .kind {{ color:#344054; background:#f8fafc; border-color:#d0d5dd; }}
    .analysis {{ margin:10px 0 12px; color:#334155; font-size:14px; line-height:1.55; }}
    dl {{ margin:0; display:grid; gap:7px; }}
    dl div {{ display:grid; grid-template-columns:72px minmax(0,1fr); gap:8px; font-size:12px; line-height:1.45; }}
    dt {{ color:#667085; }}
    dd {{ margin:0; color:#344054; word-break:break-word; }}
    @media (max-width: 900px) {{
      header {{ position:static; }}
      .layout {{ grid-template-columns:1fr; padding:14px; }}
      nav {{ position:static; }}
      .section-head {{ flex-direction:column; }}
      .section-stats {{ justify-content:flex-start; min-width:0; }}
      .items {{ grid-template-columns:1fr; }}
      .item-head {{ flex-direction:column; }}
      .badges {{ justify-content:flex-start; min-width:0; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>类功能系统分类总览</h1>
    <div class="summary">
      <span>已生成 HTML：{generated_count} 个</span>
      <span>未生成 HTML：{missing_count} 个</span>
      <span>合计：{total_count} 个类/类型</span>
      <span>依据：dump.cs 字段声明 + 当前字段关系图</span>
    </div>
  </header>
  <div class="layout">
    <nav>{nav}</nav>
    <main>{''.join(sections)}</main>
  </div>
</body>
</html>
"""


def main() -> None:
    output = graphs.DOC_OUT / "类功能系统分类总览.html"
    output.write_text(render("./HTML/"), encoding="utf-8")
    legacy_output = graphs.OUT / "类功能系统分类总览.html"
    legacy_output.write_text(render("./文档汇总/HTML/"), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
