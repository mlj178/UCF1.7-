import importlib
import sys
from pathlib import Path


def load_plugin_module(plugin_dir, module_stem):
    """Import a feature-local module from its on-disk plugin directory."""
    plugin_dir = Path(plugin_dir)
    features_dir = plugin_dir.parent
    project_dir = plugin_dir.parent.parent
    project_dir_text = str(project_dir)
    if project_dir_text not in sys.path:
        sys.path.insert(0, project_dir_text)
    features_package = sys.modules.get("features")
    if features_package is not None and hasattr(features_package, "__path__"):
        features_dir_text = str(features_dir)
        if features_dir_text not in features_package.__path__:
            features_package.__path__.append(features_dir_text)
    return importlib.import_module(f"features.{plugin_dir.name}.{module_stem}")
