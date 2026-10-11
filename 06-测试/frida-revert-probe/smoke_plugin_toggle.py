# -*- coding: utf-8 -*-
"""临时冒烟：在没连游戏的情况下装载插件注册表，验证开关/参数下发路径不再走死代码。"""

import sys
from pathlib import Path

ROOT = Path(r"D:\trae_project\ucf1.7-modifier\04-正式发行版\全功能整合包2.7\game_modifier")
sys.path.insert(0, str(ROOT))

from core.plugin.plugin_base import PluginFeatureBase  # noqa: E402
from core.plugin.plugin_registry import PluginRegistry  # noqa: E402

registry = PluginRegistry(config_manager=None, rpc_client=None)
features = registry.load()
print(f"[i] 插件装载: {len(features)} 个")

TARGETS = ["knife", "movespeed", "range", "gravity", "timescale", "fast_gunstock"]
for feature_id in TARGETS:
    feature = registry.get(feature_id)
    assert feature is not None, feature_id
    enabled = feature.enable()
    disabled = feature.disable()
    configured = feature.set_config({"probe": 1})
    uses_base = type(feature).enable is PluginFeatureBase.enable
    print(
        f"[=] {feature_id:<14} {type(feature).__name__:<20} base.enable={uses_base} "
        f"enable={enabled} disable={disabled} set_config_keys={sorted(configured['config'])}"
    )
    assert uses_base, f"{feature_id} 仍覆写 enable"
    assert type(feature).disable is PluginFeatureBase.disable, f"{feature_id} 仍覆写 disable"

print("\n[=] gravity 三个 setter：")
gravity = registry.get("gravity")
print("   set_gravity(0.5) ->", gravity.set_gravity(0.5))
print("   set_jump(2.5)    ->", gravity.set_jump(2.5))
print("   set_mode('all')  ->", gravity.set_mode("all"))

print("\n[=] 清单 rpc 与 controls 一致性抽查 (enable/disable/setConfig)：")
missing = []
for feature in registry.all():
    manifest = feature.manifest
    rpc = set(manifest.get("rpc") or [])
    fid = manifest.get("feature_id")
    for needed in ("enable", "disable", "status"):
        if needed not in rpc:
            missing.append((fid, needed))
    if any(c.get("action") == "setConfig" for c in manifest.get("controls") or []):
        if "setConfig" not in rpc:
            missing.append((fid, "setConfig"))
print("   缺失项:", missing if missing else "无")
