Legacy core archive only.

`feature_registry.py` was used by the old manual registration runtime. It is
kept only as historical reference.

New features must not use FeatureRegistry or `register_feature`. Use
manifest-backed plugins under `features/<feature_id>/` instead.
