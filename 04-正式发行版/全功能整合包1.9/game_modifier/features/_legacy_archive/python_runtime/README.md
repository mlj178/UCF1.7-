Legacy Python runtime archive only.

These files are historical references from the old FeatureRegistry /
FeatureBase architecture. They are not runtime entrypoints.

New features must not use:

- `FeatureRegistry`
- `register_feature`
- `FeatureBase`

New features must use:

- `PluginRegistry`
- `PluginFeatureBase`
- `features/<feature_id>/manifest.json`
- `features/<feature_id>/script.js`
- `features/<feature_id>/panel.py`
