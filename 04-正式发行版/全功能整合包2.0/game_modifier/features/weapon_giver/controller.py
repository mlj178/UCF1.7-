import threading

import customtkinter as ctk

from core.config import WEAPON_HOTKEY_DISPLAY_NAMES
from core.weapon_catalog import get_weapon_name
from features.weapon_giver.hotkeys import get_manager
from features.weapon_giver.service import WeaponGiverService
from features.weapon_giver.state import state


class WeaponInteractionController:
    def __init__(self, context, dialog_parent):
        self._context = context
        self._dialog_parent = dialog_parent
        self._service = WeaponGiverService(context.feature_service)

    def quick_give_weapon(self, weapon_id):
        if not self._context.is_connected():
            self._context.log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            return

        self._context.log(f"🔫 快速赋予武器 ID={weapon_id}...")

        def do_give_weapon():
            try:
                if not self._context.is_connected():
                    return
                result = self._service.give_weapon(weapon_id, True, True)
                if result and result.get("ok"):
                    if result.get("result", "").startswith("pending:"):
                        self._context.log("✅ 武器赋予任务已提交，等待主线程执行...")
                    else:
                        self._context.log("✅ 武器赋予成功！")
                else:
                    self._context.log(f"❌ 武器赋予失败: {result.get('msg', '未知错误')}")
            except Exception as e:
                self._context.log(f"❌ 武器赋予异常: {e}")

        threading.Thread(target=do_give_weapon, daemon=True).start()

    def give_weapon_by_id(self, weapon_id, weapon_name=""):
        if not self._context.is_connected():
            self._context.log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            return

        if state.current_weapon_label:
            state.current_weapon_label.configure(text=f"当前武器: {weapon_name} (ID: {weapon_id})")
        self._context.log(f"🔫 正在赋予武器: {weapon_name} (ID: {weapon_id})...")

        respawn_enabled = bool(
            state.respawn_weapon_var.get()
            if state.respawn_weapon_var is not None
            else state.respawn_enabled
        )
        if respawn_enabled:
            self.set_respawn_weapon(weapon_id, weapon_name)

        def do_give_weapon():
            try:
                if not self._context.is_connected():
                    return
                result = self._service.give_weapon(weapon_id, True, True)
                if result and result.get("ok"):
                    if result.get("result", "").startswith("pending:"):
                        self._context.log("✅ 武器赋予任务已提交，等待主线程执行...")
                    else:
                        self._context.log(f"✅ 武器赋予成功: {weapon_name}")
                else:
                    self._context.log(f"❌ 武器赋予失败: {weapon_name} - {result.get('msg', '未知错误')}")
            except Exception as e:
                self._context.log(f"❌ 武器赋予异常: {e}")

        threading.Thread(target=do_give_weapon, daemon=True).start()

    def set_respawn_weapon(self, weapon_id, weapon_name):
        if not self._context.is_connected():
            return

        def do_set():
            try:
                result = self._service.set_respawn_weapon(weapon_id, weapon_name)
                if result and result.get("ok"):
                    self._context.log(f"✅ 已设置复活自动装备: {weapon_name} (ID: {weapon_id})")
                else:
                    self._context.log("❌ 设置复活武器失败")
            except Exception as e:
                self._context.log(f"❌ 设置复活武器失败: {e}")

        threading.Thread(target=do_set, daemon=True).start()

    def on_respawn_weapon_toggle(self, enabled=None):
        if enabled is None:
            enabled = state.respawn_weapon_var.get() if state.respawn_weapon_var else state.respawn_enabled
        state.respawn_enabled = bool(enabled)
        self._context.config_manager.set("weapon_giver", {"respawn_weapon": state.respawn_enabled})
        if not self._context.is_connected():
            self._context.log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            return

        if state.respawn_enabled:
            self._context.log("✅ 复活自动装备已启用，点击武器卡片赋予时会自动设置")
        else:
            self.clear_respawn_weapon()

    def create_hotkey_badge(self, parent, weapon_id, weapon_name):
        hotkey = get_manager().get_weapon_hotkey(weapon_id)
        if not hotkey:
            return None

        badge_frame = ctk.CTkFrame(parent, fg_color="#3498db", corner_radius=3)
        display_name = WEAPON_HOTKEY_DISPLAY_NAMES.get(hotkey, hotkey)
        ctk.CTkLabel(
            badge_frame,
            text=f"⌨ {display_name}",
            font=("Microsoft YaHei", 8),
            text_color="white",
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            badge_frame,
            text="✕",
            width=15,
            height=15,
            font=("Microsoft YaHei", 7),
            command=lambda: self.unbind_weapon_hotkey(weapon_id, weapon_name),
            fg_color="transparent",
            hover_color="#e74c3c",
            text_color="white",
        ).pack(side="left", padx=1)
        return badge_frame

    def unbind_weapon_hotkey(self, weapon_id, _weapon_name):
        success = get_manager().unbind_weapon_hotkey(weapon_id)
        if success and weapon_id in state.weapon_hotkey_badges:
            badge = state.weapon_hotkey_badges[weapon_id]
            badge.destroy()
            del state.weapon_hotkey_badges[weapon_id]

    def bind_weapon_hotkey_dialog(self, weapon_id, weapon_name):
        dialog = ctk.CTkToplevel(self._dialog_parent)
        dialog.title(f"绑定快捷键 - {weapon_name}")
        dialog.geometry("300x200")
        dialog.transient(self._dialog_parent)
        dialog.grab_set()

        dialog.update_idletasks()
        x = self._dialog_parent.winfo_x() + (self._dialog_parent.winfo_width() - dialog.winfo_width()) // 2
        y = self._dialog_parent.winfo_y() + (self._dialog_parent.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        ctk.CTkLabel(dialog, text=f"为 {weapon_name} 绑定快捷键", font=("Microsoft YaHei", 12, "bold")).pack(pady=15)

        whm = get_manager()
        available_hotkeys = whm.get_available_hotkeys()
        current_hotkey = whm.get_weapon_hotkey(weapon_id)
        if current_hotkey and current_hotkey not in available_hotkeys:
            available_hotkeys.insert(0, current_hotkey)

        available_display = [WEAPON_HOTKEY_DISPLAY_NAMES.get(h, h) for h in available_hotkeys]
        has_available_hotkey = bool(available_hotkeys)
        hotkey_var = ctk.StringVar(value=available_display[0] if has_available_hotkey else "无可用快捷键")
        ctk.CTkOptionMenu(
            dialog,
            variable=hotkey_var,
            values=available_display if has_available_hotkey else ["无可用快捷键"],
            width=200,
            state="normal" if has_available_hotkey else "disabled",
        ).pack(pady=10)

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=15)

        def on_confirm():
            if not has_available_hotkey:
                self._context.log("⚠ 没有可用的武器快捷键，请先解绑其他武器")
                return
            display_name = hotkey_var.get()
            hotkey = None
            for key in available_hotkeys:
                display = WEAPON_HOTKEY_DISPLAY_NAMES.get(key, key)
                if display == display_name:
                    hotkey = key
                    break

            if hotkey:
                success, error_msg = whm.bind_weapon_hotkey(hotkey, weapon_id, weapon_name)
                if success:
                    self.update_weapon_badge(weapon_id, weapon_name)
                    dialog.destroy()
                else:
                    self._context.log(f"❌ {error_msg}")

        ctk.CTkButton(
            btn_frame,
            text="确定",
            width=80,
            command=on_confirm,
            state="normal" if has_available_hotkey else "disabled",
        ).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="取消", width=80, command=dialog.destroy).pack(side="left", padx=10)

    def update_weapon_badge(self, weapon_id, weapon_name):
        if weapon_id in state.weapon_hotkey_badges:
            old_badge = state.weapon_hotkey_badges[weapon_id]
            old_badge.destroy()
            del state.weapon_hotkey_badges[weapon_id]

        if weapon_id in state.weapon_top_frames:
            top_frame = state.weapon_top_frames[weapon_id]
            new_badge = self.create_hotkey_badge(top_frame, weapon_id, weapon_name)
            if new_badge:
                new_badge.pack(side="right", padx=3)
                state.weapon_hotkey_badges[weapon_id] = new_badge

    def init_hotkey_manager(self):
        whm = get_manager()
        whm.setup_hotkeys(self.give_weapon_by_id_from_hotkey, app=self._dialog_parent)
        bindings = whm.get_all_bindings()
        if bindings:
            self._context.log(f"✅ 武器快捷键已加载: {len(bindings)} 个绑定")

    def give_weapon_by_id_from_hotkey(self, weapon_id):
        weapon_name = self.get_weapon_name_by_id(weapon_id)
        self.give_weapon_by_id(weapon_id, weapon_name)

    def get_weapon_name_by_id(self, weapon_id):
        weapon_name = get_weapon_name(weapon_id)
        if weapon_name == f"weapon{weapon_id}":
            return f"武器{weapon_id}"
        return weapon_name

    def clear_respawn_weapon(self):
        if not self._context.is_connected():
            return

        self._context.log("🔫 清除复活自动装备武器")

        def do_clear():
            try:
                result = self._service.clear_respawn_weapon()
                if result and result.get("ok"):
                    self._context.log("✅ 已清除复活自动装备")
                else:
                    self._context.log("❌ 清除失败")
            except Exception as e:
                self._context.log(f"❌ 清除异常: {e}")

        threading.Thread(target=do_clear, daemon=True).start()

    def pause_hotkeys(self):
        try:
            get_manager().pause_hotkeys()
        except Exception:
            pass

    def cleanup(self):
        try:
            get_manager().cleanup()
        except Exception:
            pass
