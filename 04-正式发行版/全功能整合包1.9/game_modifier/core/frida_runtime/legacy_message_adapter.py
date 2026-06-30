"""LEGACY_COMPAT_ONLY.

Do not add new feature branches here. New plugins must send plugin_event
directly from their script.js:

send({
  type: "plugin_event",
  feature: "<feature_id>",
  event: "<event_name>",
  payload: {},
  audience: "dev"
});
"""


LEGACY_FEATURE_IDS = frozenset({
    "gather",
    "roundskip",
    "weapon_giver",
    "nano4t",
    "battle_round",
    "isbot",
})

LEGACY_MESSAGE_TYPES = frozenset({
    "gather_result",
    "round_skipped",
    "giveWeaponResult",
    "playerRespawned",
    "playerRespawnedWithWeapon",
    "isbot_state",
})

LEGACY_MESSAGE_PREFIXES = frozenset({
    "nano4t_",
    "battle_round_",
})


class LegacyMessageAdapter:
    """Convert declared pre-plugin JS messages into plugin_event payloads."""

    @staticmethod
    def adapt(payload):
        msg_type = payload.get("type", "")
        if not _is_declared_legacy_type(msg_type):
            return None

        if msg_type == "gather_result":
            return _plugin_event(
                "gather",
                "result",
                payload.get("data", {}),
                "user",
            )
        if msg_type == "round_skipped":
            return _plugin_event("roundskip", "skipped", payload, "user")
        if msg_type in {"giveWeaponResult", "playerRespawned", "playerRespawnedWithWeapon"}:
            return _plugin_event("weapon_giver", msg_type, payload, "both")
        if msg_type.startswith("nano4t_"):
            return _plugin_event("nano4t", msg_type, payload, "dev")
        if msg_type.startswith("battle_round_"):
            return _plugin_event("battle_round", msg_type, payload, "dev")
        if msg_type == "isbot_state":
            return _plugin_event("isbot", "state", payload, "user")
        return None


def _is_declared_legacy_type(msg_type):
    return msg_type in LEGACY_MESSAGE_TYPES or any(
        msg_type.startswith(prefix) for prefix in LEGACY_MESSAGE_PREFIXES
    )


def _plugin_event(feature_id, event, payload, audience):
    if feature_id not in LEGACY_FEATURE_IDS:
        return None
    return {
        "feature": feature_id,
        "event": event,
        "payload": payload,
        "audience": audience,
    }
