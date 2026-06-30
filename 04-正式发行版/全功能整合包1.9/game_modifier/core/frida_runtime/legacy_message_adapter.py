class LegacyMessageAdapter:
    """Convert pre-plugin JS messages into generic plugin_event payloads."""

    @staticmethod
    def adapt(payload):
        msg_type = payload.get("type", "")
        if msg_type == "gather_result":
            return {
                "feature": "gather",
                "event": "result",
                "payload": payload.get("data", {}),
            }
        if msg_type == "round_skipped":
            return {
                "feature": "roundskip",
                "event": "skipped",
                "payload": payload,
            }
        if msg_type in {"giveWeaponResult", "playerRespawned", "playerRespawnedWithWeapon"}:
            return {
                "feature": "weapon_giver",
                "event": msg_type,
                "payload": payload,
            }
        if msg_type.startswith("nano4t_"):
            return {
                "feature": "nano4t",
                "event": msg_type,
                "payload": payload,
            }
        if msg_type.startswith("battle_round_"):
            return {
                "feature": "battle_round",
                "event": msg_type,
                "payload": payload,
            }
        if msg_type == "isbot_state":
            return {
                "feature": "isbot",
                "event": "state",
                "payload": payload,
            }
        return None
