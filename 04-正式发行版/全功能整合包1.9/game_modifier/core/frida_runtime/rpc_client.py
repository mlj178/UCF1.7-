class RpcClient:
    """Authorize RPC calls using each plugin manifest."""

    DEFAULT_ACTIONS = {"enable", "disable", "setConfig", "status", "cleanup"}

    def __init__(self, script_manager):
        self.script_manager = script_manager

    def call(self, feature_id, action, payload=None):
        manifest = self.script_manager.manifests.get(feature_id, {})
        allowed = set(manifest.get("rpc") or self.DEFAULT_ACTIONS)
        if action not in allowed:
            manifest_ref = manifest.get("_manifest_path") or manifest.get("display_name") or feature_id
            raise ValueError(
                f"unsupported plugin rpc action: feature_id={feature_id}, "
                f"action={action}, manifest={manifest_ref}"
            )
        return self.script_manager.call(feature_id, action, payload)
