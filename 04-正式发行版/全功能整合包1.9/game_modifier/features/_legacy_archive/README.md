Legacy archive only.

Runtime entrypoints are now always under:

- `features/<feature_id>/manifest.json`
- `features/<feature_id>/feature.py`
- `features/<feature_id>/script.js`
- `features/<feature_id>/panel.py`

Historical JavaScript files, including `_common.js`, are archived in
`features/_legacy_archive/scripts/`. They are reference material only and must
not be loaded by runtime code.

Historical FeatureRegistry / FeatureBase Python files are archived in
`features/_legacy_archive/python_runtime/` and `core/_legacy_archive/`.
They are reference material only and must not be used for new features.
