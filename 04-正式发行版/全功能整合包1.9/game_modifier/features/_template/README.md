# 功能插件模板

新增功能时，只复制本目录到 `features/<feature_id>/`，然后修改该目录内文件。

必须包含：

- `manifest.json`
- `feature.py`
- `script.js`
- `panel.py`
- `events.py`

## JS 标准

- `script.js` 必须自包含。
- 不使用 `common.js`。
- 不引用 `scripts/_common.js`。
- 不 import / require 共享 JS。
- 必须提供 `rpc.exports`。
- RPC action 必须写入 `manifest.rpc`。
- JS 事件统一发送 `{ type: "plugin_event", feature, event, payload }`。

## Python 标准

- `feature.py` 必须继承 `PluginFeatureBase`。
- 不使用 `FeatureBase`。
- 不使用 `register_feature`。
- 不 import `core.feature_registry`。

## UI 标准

`panel.py` 只能通过通用 callbacks 调用运行逻辑：

- `callbacks["toggle"](feature_id)`
- `callbacks["set_config"](feature_id, key, value)`
- `callbacks["action"](feature_id, action)`

`panel.py` 不允许直接 import `FridaManager`。
`panel.py` 不允许访问完整 App 或 `app._xxx` 私有字段。
`panel.py` 不允许使用 `context._app`、`context.legacy`、`get_state`、`set_state`、`get_handle`、`set_handle`、`controller`、`service`。
如果需要特殊事件处理，可在功能目录新增 `events.py`，只处理本功能事件。
如果需要完整页面，在 `manifest.json` 中声明 `ui.mode = "special_page"` 和 `ui.tab_title`，不要改 `ui/app.py`。

## 禁止改中心文件

新增功能不要修改：

- `ui/app.py`
- `core/frida_manager.py`
- `core/services/feature_command_service.py`
- `ui/controllers/feature_action_controller.py`
- `core/state/app_state.py`
- `scripts/`
