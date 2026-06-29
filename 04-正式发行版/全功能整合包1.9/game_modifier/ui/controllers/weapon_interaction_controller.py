import threading

import customtkinter as ctk

from core.config import WEAPON_HOTKEY_DISPLAY_NAMES
from core.weapon_catalog import get_weapon_name
from core.weapon_hotkey_manager import WeaponHotkeyManager


class WeaponInteractionController:
    def __init__(self, app):
        self._app = app

    def quick_give_weapon(self, weapon_id):
        app = self._app
        if not app._ready:
            app._log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            return

        app._log(f"🔫 快速赋予武器 ID={weapon_id}...")
        request_pid = app._pid

        def do_give_weapon():
            try:
                if not app._ready or app._pid != request_pid:
                    return
                result = app._weapon_giver_service.give_weapon(weapon_id, True, True)
                if result and result.get("ok"):
                    if result.get("result", "").startswith("pending:"):
                        app._log("✅ 武器赋予任务已提交，等待主线程执行...")
                    else:
                        app._log("✅ 武器赋予成功！")
                else:
                    app._log(f"❌ 武器赋予失败: {result.get('msg', '未知错误')}")
            except Exception as e:
                app._log(f"❌ 武器赋予异常: {e}")

        threading.Thread(target=do_give_weapon, daemon=True).start()

    def give_weapon_by_id(self, weapon_id, weapon_name=""):
        app = self._app
        if not app._ready:
            app._log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            return

        if hasattr(app, "current_weapon_label"):
            app.current_weapon_label.configure(text=f"当前武器: {weapon_name} (ID: {weapon_id})")
        app._log(f"🔫 正在赋予武器: {weapon_name} (ID: {weapon_id})...")
        request_pid = app._pid

        respawn_enabled = app.respawn_weapon_var.get() if hasattr(app, "respawn_weapon_var") else app._weapon_giver_respawn_enabled
        if respawn_enabled:
            self.set_respawn_weapon(weapon_id, weapon_name)

        def do_give_weapon():
            try:
                if not app._ready or app._pid != request_pid:
                    return
                result = app._weapon_giver_service.give_weapon(weapon_id, True, True)
                if result and result.get("ok"):
                    if result.get("result", "").startswith("pending:"):
                        app._log("✅ 武器赋予任务已提交，等待主线程执行...")
                    else:
                        app._log(f"✅ 武器赋予成功: {weapon_name}")
                else:
                    app._log(f"❌ 武器赋予失败: {weapon_name} - {result.get('msg', '未知错误')}")
            except Exception as e:
                app._log(f"❌ 武器赋予异常: {e}")

        threading.Thread(target=do_give_weapon, daemon=True).start()

    def set_respawn_weapon(self, weapon_id, weapon_name):
        app = self._app
        if not app._ready:
            return

        def do_set():
            try:
                result = app._weapon_giver_service.set_respawn_weapon(weapon_id, weapon_name)
                if result and result.get("ok"):
                    app._log(f"✅ 已设置复活自动装备: {weapon_name} (ID: {weapon_id})")
                else:
                    app._log("❌ 设置复活武器失败")
            except Exception as e:
                app._log(f"❌ 设置复活武器失败: {e}")

        threading.Thread(target=do_set, daemon=True).start()

    def on_respawn_weapon_toggle(self, enabled=None):
        app = self._app
        if enabled is None:
            enabled = app.respawn_weapon_var.get() if hasattr(app, "respawn_weapon_var") else app._weapon_giver_respawn_enabled
        app._weapon_giver_respawn_enabled = bool(enabled)
        app._schedule_save_state()
        if not app._ready:
            app._log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            return

        if app._weapon_giver_respawn_enabled:
            app._log("✅ 复活自动装备已启用，点击武器卡片赋予时会自动设置")
        else:
            self.clear_respawn_weapon()

    def create_hotkey_badge(self, parent, weapon_id, weapon_name):
        hotkey = WeaponHotkeyManager.get_instance().get_weapon_hotkey(weapon_id)
        if not hotkey:
            return None

        badge_frame = ctk.CTkFrame(parent, fg_color="#3498db", corner_radius=3)
        display_name = WEAPON_HOTKEY_DISPLAY_NAMES.get(hotkey, hotkey)
        hotkey_label = ctk.CTkLabel(
            badge_frame,
            text=f"⌨ {display_name}",
            font=("Microsoft YaHei", 8),
            text_color="white",
        )
        hotkey_label.pack(side="left", padx=2)

        remove_btn = ctk.CTkButton(
            badge_frame,
            text="✕",
            width=15,
            height=15,
            font=("Microsoft YaHei", 7),
            command=lambda: self.unbind_weapon_hotkey(weapon_id, weapon_name),
            fg_color="transparent",
            hover_color="#e74c3c",
            text_color="white",
        )
        remove_btn.pack(side="left", padx=1)
        return badge_frame

    def unbind_weapon_hotkey(self, weapon_id, _weapon_name):
        app = self._app
        success = WeaponHotkeyManager.get_instance().unbind_weapon_hotkey(weapon_id)
        if success and weapon_id in app._weapon_hotkey_badges:
            badge = app._weapon_hotkey_badges[weapon_id]
            badge.destroy()
            del app._weapon_hotkey_badges[weapon_id]

    def bind_weapon_hotkey_dialog(self, weapon_id, weapon_name):
        app = self._app

        dialog = ctk.CTkToplevel(app)
        dialog.title(f"绑定快捷键 - {weapon_name}")
        dialog.geometry("300x200")
        dialog.transient(app)
        dialog.grab_set()

        dialog.update_idletasks()
        x = app.winfo_x() + (app.winfo_width() - dialog.winfo_width()) // 2
        y = app.winfo_y() + (app.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        title_label = ctk.CTkLabel(dialog, text=f"为 {weapon_name} 绑定快捷键", font=("Microsoft YaHei", 12, "bold"))
        title_label.pack(pady=15)

        whm = WeaponHotkeyManager.get_instance()
        available_hotkeys = whm.get_available_hotkeys()
        current_hotkey = whm.get_weapon_hotkey(weapon_id)
        if current_hotkey and current_hotkey not in available_hotkeys:
            available_hotkeys.insert(0, current_hotkey)

        available_display = [WEAPON_HOTKEY_DISPLAY_NAMES.get(h, h) for h in available_hotkeys]
        has_available_hotkey = bool(available_hotkeys)
        hotkey_var = ctk.StringVar(value=available_display[0] if has_available_hotkey else "无可用快捷键")
        hotkey_menu = ctk.CTkOptionMenu(
            dialog,
            variable=hotkey_var,
            values=available_display if has_available_hotkey else ["无可用快捷键"],
            width=200,
            state="normal" if has_available_hotkey else "disabled",
        )
        hotkey_menu.pack(pady=10)

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=15)

        def on_confirm():
            if not has_available_hotkey:
                app._log("⚠ 没有可用的武器快捷键，请先解绑其他武器")
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
                    app._log(f"❌ {error_msg}")

        confirm_btn = ctk.CTkButton(
            btn_frame,
            text="确定",
            width=80,
            command=on_confirm,
            state="normal" if has_available_hotkey else "disabled",
        )
        confirm_btn.pack(side="left", padx=10)
        cancel_btn = ctk.CTkButton(btn_frame, text="取消", width=80, command=dialog.destroy)
        cancel_btn.pack(side="left", padx=10)

    def update_weapon_badge(self, weapon_id, weapon_name):
        app = self._app
        if weapon_id in app._weapon_hotkey_badges:
            old_badge = app._weapon_hotkey_badges[weapon_id]
            old_badge.destroy()
            del app._weapon_hotkey_badges[weapon_id]

        if weapon_id in app._weapon_top_frames:
            top_frame = app._weapon_top_frames[weapon_id]
            new_badge = self.create_hotkey_badge(top_frame, weapon_id, weapon_name)
            if new_badge:
                new_badge.pack(side="right", padx=3)
                app._weapon_hotkey_badges[weapon_id] = new_badge

    def init_hotkey_manager(self):
        app = self._app
        whm = WeaponHotkeyManager.get_instance()
        whm.setup_hotkeys(self.give_weapon_by_id_from_hotkey, app=app)
        bindings = whm.get_all_bindings()
        if bindings:
            app._log(f"✅ 武器快捷键已加载: {len(bindings)} 个绑定")

    def give_weapon_by_id_from_hotkey(self, weapon_id):
        weapon_name = self.get_weapon_name_by_id(weapon_id)
        self.give_weapon_by_id(weapon_id, weapon_name)

    def get_weapon_name_by_id(self, weapon_id):
        weapon_name = get_weapon_name(weapon_id)
        if weapon_name == f"weapon{weapon_id}":
            return f"武器{weapon_id}"
        return weapon_name

    def clear_respawn_weapon(self):
        app = self._app
        if not app._ready:
            return

        app._log("🔫 清除复活自动装备武器")

        def do_clear():
            try:
                result = app._weapon_giver_service.clear_respawn_weapon()
                if result and result.get("ok"):
                    app._log("✅ 已清除复活自动装备")
                else:
                    app._log("❌ 清除失败")
            except Exception as e:
                app._log(f"❌ 清除异常: {e}")

        threading.Thread(target=do_clear, daemon=True).start()

    def pause_hotkeys(self):
        try:
            WeaponHotkeyManager.get_instance().pause_hotkeys()
        except Exception:
            pass

    def cleanup(self):
        try:
            WeaponHotkeyManager.get_instance().cleanup()
        except Exception:
            pass
