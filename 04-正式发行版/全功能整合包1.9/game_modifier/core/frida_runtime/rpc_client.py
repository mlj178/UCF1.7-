class RpcClient:
    """Whitelist RPC calls to plugin scripts."""

    ALLOWED_ACTIONS = {"enable", "disable", "setConfig", "status", "cleanup"}

    def __init__(self, script_manager):
        self.script_manager = script_manager

    def call(self, feature_id, action, payload=None):
        if action not in self.ALLOWED_ACTIONS:
            raise ValueError(f"unsupported plugin rpc action: {action}")
        return self.script_manager.call(feature_id, action, payload)

