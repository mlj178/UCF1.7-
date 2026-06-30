class WeaponGiverService:
    def __init__(self, frida_manager):
        self._frida = frida_manager

    def give_weapon(self, weapon_id, auto_give_up=True, auto_select=True):
        return self._frida.plugin_call(
            "weapon_giver",
            "giveWeapon",
            {
                "weaponId": weapon_id,
                "autoGiveUp": bool(auto_give_up),
                "autoSelect": bool(auto_select),
            },
        )

    def set_respawn_weapon(self, weapon_id, weapon_name):
        return self._frida.plugin_call(
            "weapon_giver",
            "setRespawnWeapon",
            {
                "weaponId": weapon_id,
                "weaponName": weapon_name,
            },
        )

    def clear_respawn_weapon(self):
        return self._frida.plugin_call("weapon_giver", "clearRespawnWeapon", {})
