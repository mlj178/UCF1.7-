from pathlib import Path

from core.plugin.plugin_base import PluginFeatureBase

from .player_profile_service import (
    PlayerProfile,
    get_default_player_data_path,
    load_profile,
    save_profile,
)


class PluginFeature(PluginFeatureBase):
    feature_id = "player_profile_editor"
    name = "玩家信息修改"
    category = "other"
    desc = "读取和修改本地 PlayerData.dat 的玩家信息。"

    def load_profile(self, payload=None):
        payload = payload or {}
        path = Path(payload.get("path") or get_default_player_data_path())
        profile = load_profile(path)
        if profile is None:
            return {"ok": True, "path": str(path), "profile": None, "message": "没有读取到 [Player]"}
        return {
            "ok": True,
            "path": str(path),
            "profile": {
                "nickname": profile.nickname,
                "level": profile.level,
                "vip_level": profile.vip_level,
            },
            "message": "已读取现有 [Player] 信息",
        }

    def save_profile(self, payload=None):
        payload = payload or {}
        path = Path(payload.get("path") or get_default_player_data_path())
        try:
            profile = PlayerProfile(
                nickname=payload.get("nickname", ""),
                level=int(payload.get("level", 0)),
                vip_level=int(payload.get("vip_level", 0)),
            )
            result = save_profile(path, profile)
        except (TypeError, ValueError, OSError) as exc:
            return {"ok": False, "path": str(path), "message": str(exc)}
        return {
            "ok": True,
            "path": str(result.path),
            "created_file": result.created_file,
            "message": "已新建并保存，重启游戏后生效" if result.created_file else "保存成功，重启游戏后生效",
        }
