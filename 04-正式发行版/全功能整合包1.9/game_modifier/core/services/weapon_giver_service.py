class WeaponGiverService:
    def __init__(self, frida_manager):
        self._frida = frida_manager

    def give_weapon(self, weapon_id, auto_give_up=True, auto_select=True):
        return self._frida.call_export("giveweapon", weapon_id, auto_give_up, auto_select)

    def set_respawn_weapon(self, weapon_id, weapon_name):
        return self._frida.call_export("setrespawnweapon", weapon_id, weapon_name)

    def clear_respawn_weapon(self):
        return self._frida.call_export("clearrespawnweapon")
