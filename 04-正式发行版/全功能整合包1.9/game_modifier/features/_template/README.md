# 功能插件模板

新增功能时，只新增 `features/功能ID/` 目录，并复制本模板中的文件。

必须保持：

- 不改 `ui/app.py` 堆新功能逻辑。
- 不改 `core/frida_manager.py` 堆新功能逻辑。
- 不改 `FeatureCommandService` 堆新功能逻辑。
- JS 入口使用 `rpc.exports.enable/disable/setConfig/status/cleanup`。
- 功能配置写入 `data/default_config.json` 和 `data/user_config.json` 的对应 `feature_id` 分区。

本模板只作为新功能起点，不会被 `ManifestLoader` 加载。
