import inspect
from pathlib import Path

from core.config import FEATURES_DIR
from core.log_manager import get_logger
from core.plugin.manifest_loader import ManifestLoader
from core.plugin.module_loader import load_plugin_module
from core.plugin.plugin_base import PluginFeatureBase
from core.plugin.plugin_contract import PluginContract


def _accepts_binding_args(feature_cls):
    """判断插件类的 __init__ 是否接受 (manifest, rpc_client, config_manager)。"""
    try:
        signature = inspect.signature(feature_cls.__init__)
    except (TypeError, ValueError):
        return True
    positional = 0
    for name, parameter in signature.parameters.items():
        if name == "self":
            continue
        if parameter.kind is inspect.Parameter.VAR_POSITIONAL:
            return True
        if parameter.kind in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        ):
            positional += 1
    return positional >= 3


def _manifest_order(feature):
    """order 字段缺失或不是数字时退化为 0，避免 sorted() 抛 TypeError 中断启动。"""
    try:
        return float(feature.manifest.get("order", 0))
    except (TypeError, ValueError):
        return 0.0


class PluginRegistry:
    """Registry for manifest-backed feature plugin instances."""

    def __init__(
        self,
        features_dir=None,
        manifest_loader=None,
        contract=None,
        rpc_client=None,
        config_manager=None,
        logger=None,
    ):
        self.features_dir = Path(features_dir or FEATURES_DIR)
        self.manifest_loader = manifest_loader or ManifestLoader(self.features_dir)
        self.contract = contract or PluginContract()
        self.rpc_client = rpc_client
        self.config_manager = config_manager
        self._logger = logger or get_logger("PluginRegistry")
        self._features = {}

    def _warning(self, message):
        if callable(self._logger):
            self._logger(message)
            return
        self._logger.warning(message)

    def load(self):
        self._features = {}
        for manifest in self.manifest_loader.load():
            self.contract.validate(manifest)
            feature_id = manifest.get("feature_id")
            if not feature_id:
                continue
            try:
                feature = self._load_feature(manifest)
                self._features[feature_id] = feature
            except Exception as exc:
                self._warning(f"failed to load plugin {feature_id}: {exc}")
        return self.all()

    def _load_feature(self, manifest):
        feature_id = manifest["feature_id"]
        plugin_dir = Path(manifest.get("_plugin_dir") or self.features_dir / feature_id)
        feature_path = plugin_dir / "feature.py"
        if not feature_path.exists():
            return PluginFeatureBase(manifest, self.rpc_client, self.config_manager)

        module = load_plugin_module(plugin_dir, "feature")
        feature_cls = getattr(module, "PluginFeature", None)
        if feature_cls is None:
            feature_cls = next(
                (
                    value
                    for value in module.__dict__.values()
                    if isinstance(value, type)
                    and issubclass(value, PluginFeatureBase)
                    and value is not PluginFeatureBase
                ),
                PluginFeatureBase,
            )
        if _accepts_binding_args(feature_cls):
            return feature_cls(manifest, self.rpc_client, self.config_manager)
        # 少数插件类只写 __init__(self)（内部再调 super().__init__()）。
        # 这里补跑一次基类初始化，让 manifest / _config / rpc_client /
        # config_manager 都被正确填上（原先只赋 manifest 等三个属性，
        # 基类的 _config 与 feature_id 仍然是空的）。
        feature = feature_cls()
        PluginFeatureBase.__init__(feature, manifest, self.rpc_client, self.config_manager)
        return feature

    def get(self, feature_id):
        return self._features.get(feature_id)

    def all(self):
        return sorted(self._features.values(), key=_manifest_order)

    def by_tab(self, tab_id):
        features = [
            feature
            for feature in self._features.values()
            if feature.manifest.get("tab") == tab_id
        ]
        return sorted(features, key=_manifest_order)

    def enabled_features(self):
        return [feature for feature in self._features.values() if feature.enabled]
