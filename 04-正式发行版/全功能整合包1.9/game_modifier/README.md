# Game Modifier Plugin Architecture

## 功能统一目录

所有功能都放在独立插件目录：

```text
features/<feature_id>/
  manifest.json
  feature.py
  script.js
  panel.py
```

普通功能和特殊功能都使用同一标准。运行时通过
`PluginRegistry` 扫描 `manifest.json`，通过 `ScriptManager` 加载对应
`features/<feature_id>/script.js`。

## 方案 B：无共享 JS

本项目不使用 `common.js`。

每个 `script.js` 必须自包含所需 helper、Hook、RPC 边界。这样新增或维护功能时，只需要查看一个 `features/<feature_id>/` 目录，就能理解完整逻辑。

## 普通功能和特殊功能

普通功能通常显示为卡片：

- `panel.py` 较简单。
- `script.js` 只处理本功能 Hook。
- UI 控件由 manifest 的 `controls` 和 `layout` 描述。

特殊功能可以拥有完整页面：

- 也必须位于 `features/<feature_id>/`。
- 也必须包含 `manifest.json / feature.py / script.js / panel.py`。
- 也必须通过 `manifest.rpc` 声明可调用 RPC。
- 也必须通过 `FridaManager.plugin_call(feature_id, action, payload)` 调用。

## 新增功能禁止事项

禁止：

- 不要改 `FridaManager` 添加功能分支。
- 不要改 `App` 添加普通功能 UI 细节。
- 不要向 `scripts/` 添加正式 JS。
- 不要使用 `common.js`。
- 不要使用 `FeatureRegistry`。
- 不要使用 `register_feature`。
- 不要使用 `FeatureBase`。
- 不要让 `panel.py` 直接 import `FridaManager`。
- 不要把多个功能写进一个大 JS。
- 不要在中心文件写功能 ID 列表。

## 新增功能流程

1. 复制 `features/_template/` 到 `features/<feature_id>/`。
2. 修改 `feature_id`。
3. 编写 `manifest.json`。
4. 编写 `feature.py`，继承 `PluginFeatureBase`。
5. 编写自包含 `script.js`。
6. 编写 `panel.py`。
7. 在 `manifest.rpc` 声明 RPC。
8. 在 `manifest.runtime.type` 写 `plugin_script`。
9. 不改中心文件。
