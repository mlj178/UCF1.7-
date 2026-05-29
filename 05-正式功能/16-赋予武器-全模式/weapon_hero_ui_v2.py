# ============================================================
# weapon_hero_ui_v2.py - 武器赋予与英雄变身UI（重构版）
#
# 功能:
#   - 武器和英雄统一通过武器ID赋予
#   - 按类型分区展示武器列表
#   - 网格卡片布局（每行6个）
#   - 类型差异化配色
#   - 复活自动恢复武器功能（使用Player.Spawn Hook）
#
# 游戏进程: UnityCrossFire.exe
# ============================================================

import customtkinter as ctk
import frida
import psutil
import threading
import time
import os
import sys
from datetime import datetime
from collections import defaultdict

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JS_FILE = os.path.join(BASE_DIR, "weapon-hero-giver-fixed-v2.js")

COLOR_GREEN = "#2ecc71"
COLOR_RED = "#e74c3c"
COLOR_ORANGE = "#f39c12"
COLOR_BLUE = "#3498db"
COLOR_DARK = "#1a1a2e"
COLOR_DARKER = "#16213e"

GAME_PROCESS_NAME = "UnityCrossFire.exe"

WEAPON_LIST = [
    ("120", "NANOKNIFE", "NANOKNIFE", "近战"),
    ("195", "幽灵之刃", "幽灵之刃", "英雄"),
    ("210", "诅咒娃娃手雷", "诅咒娃娃手雷", "投掷"),

    ("237", "圣诞M4A1", "圣诞M4A1", "步枪"),
    ("341", "AK47-茉莉", "AK47-茉莉", "步枪"),
    ("390", "FAL CAMO", "FAL CAMO", "步枪"),
    ("413", "AK47-万圣节", "AK47-万圣节", "步枪"),
    ("415", "M4A1-万圣节", "M4A1-万圣节", "步枪"),
    ("428", "圣诞AK47", "圣诞AK47", "步枪"),
    ("540", "Terminator", "终结者", "英雄"),
    ("585", "M4A1-战龙", "M4A1-战龙", "步枪"),
    ("586", "Barrett-战龙", "Barrett-战龙", "狙击"),
    ("588", "MG3-银色杀手", "MG3-银色杀手", "机枪"),
    ("606", "M4A1-轻骑兵", "M4A1-轻骑兵", "步枪"),
    ("615", "百城M4A1", "百城M4A1", "步枪"),
    ("617", "百城AK47", "百城AK47", "步枪"),
    ("622", "M4A1-蓝水晶", "M4A1-蓝水晶", "步枪"),

    ("672", "GrandTerminator", "大终结者", "英雄"),
    ("730", "AK47-火麒麟", "AK47-火麒麟", "步枪"),
    ("758", "Barrett-翔龙", "Barrett-翔龙", "狙击"),
    ("761", "MG3-翔龙", "MG3-翔龙", "机枪"),
    ("764", "拳击手套", "拳击手套", "近战"),

    ("855", "M4A1-黑龙", "M4A1-黑龙", "步枪"),
    ("856", "M4A1-雷神", "M4A1-雷神", "步枪"),
    ("880", "纯金AK-47", "纯金AK-47", "步枪"),
    ("938", "汤姆逊-烈龙", "汤姆逊-烈龙", "冲锋"),
    ("994", "尼泊尔-红水晶", "尼泊尔-红水晶", "近战"),
    ("1002", "M4A1-黑骑士", "M4A1-黑骑士", "步枪"),
    ("1003", "屠龙", "屠龙", "近战"),
    ("1004", "AK47-苍龙", "AK47-苍龙", "步枪"),
    ("1005", "Barrett-苍龙", "Barrett-苍龙", "狙击"),
    ("1061", "M4A1-玫瑰精灵", "M4A1-玫瑰精灵", "步枪"),
    ("1069", "Ghost Blade-Normal form", "幽灵之刃", "英雄"),
    ("1070", "Armored Terminator", "装甲终结者", "英雄"),
    ("1097", "Fear", "恐惧", "英雄"),
    ("1168", "沙鹰-修罗", "沙鹰-修罗", "手枪"),
    ("1508", "M4A1-死神", "M4A1-死神", "步枪"),
    ("1621", "惨叫鸡", "惨叫鸡", "近战"),
    ("2568", "M82A1-水枪", "M82A1-水枪", "狙击"),
    ("2759", "M4A1-水枪", "M4A1-水枪", "步枪"),
    ("2975", "地狱终结者", "地狱终结者", "英雄"),
    ("2976", "终极猎手", "终极猎手", "英雄"),
    ("2977", "震撼弹", "震撼弹", "投掷"),
    ("2978", "FN FAL榴弹版", "FN FAL榴弹版", "步枪"),
    ("3017", "生化手雷", "生化手雷", "投掷"),
    ("3494", "Nano AT4", "Nano AT4", "特殊"),
    ("3495", "时空猎手", "时空猎手", "英雄"),
    ("3496", "钢铁终结者", "钢铁终结者", "英雄"),
    ("3831", "圣拳猎手", "圣拳猎手", "英雄"),
    ("3832", "虚空之刃", "虚空之刃", "英雄"),
    ("3928", "M14EBR-能量核心", "M14EBR-能量核心", "步枪"),
    ("4850", "机械英雄", "机械英雄", "英雄"),
    ("4851", "XM214重机枪", "XM214重机枪", "机枪"),
    ("4852", "奥术手榴弹", "奥术手榴弹", "投掷"),
    ("4853", "机枪守卫", "机枪守卫", "特殊"),
    ("4854", "不法终结者", "不法终结者", "英雄"),

    ("5361", "蝴蝶刀-枪王排位", "蝴蝶刀-枪王排位", "近战"),
    ("5384", "斯泰尔-枪娘暗刃", "斯泰尔-枪娘暗刃", "冲锋"),
]

TYPE_COLORS = {
    "步枪": "#1e3a5f",
    "英雄": "#3a1e5f",
    "近战": "#1e5f3a",
    "投掷": "#5f4a1e",
    "狙击": "#1e5f5f",
    "机枪": "#5f3a1e",
    "冲锋": "#4a1e5f",
    "特殊": "#3a3a3a",
    "手枪": "#4a5f1e",
}


class WeaponHeroUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("武器赋予与英雄变身工具 v2.0")
        self.geometry("1400x900")
        self.configure(fg_color=COLOR_DARK)

        self.session = None
        self.script = None
        self.is_connected = False
        self.log_count = 0
        self.max_logs = 500
        self._initialized = False
        self.auto_restore_enabled = False
        self.current_weapon_id = None

        self.weapons_by_type = self._group_weapons_by_type()
        self.sorted_types = self._sort_types_by_count()

        self.setup_ui()
        self.after(100, self._mark_initialized)
        self.start_auto_connect()

    def _mark_initialized(self):
        self._initialized = True

    def _group_weapons_by_type(self):
        grouped = defaultdict(list)
        for weapon in WEAPON_LIST:
            weapon_id, en_name, cn_name, weapon_type = weapon
            grouped[weapon_type].append(weapon)
        return grouped

    def _sort_types_by_count(self):
        type_counts = [(t, len(self.weapons_by_type[t])) for t in self.weapons_by_type]
        type_counts.sort(key=lambda x: x[1], reverse=True)
        return [t for t, _ in type_counts]

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.setup_header()
        self.setup_weapon_list()
        self.setup_log()

    def setup_header(self):
        self.header_frame = ctk.CTkFrame(self, fg_color=COLOR_DARKER, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.header_frame.grid_columnconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="🎮 武器赋予与英雄变身工具 v2.0",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLOR_BLUE
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(15, 10), sticky="w")

        self.status_label = ctk.CTkLabel(
            self.header_frame,
            text="⏳ 等待连接...",
            font=ctk.CTkFont(size=12),
            text_color=COLOR_ORANGE
        )
        self.status_label.grid(row=0, column=1, padx=20, pady=(15, 10), sticky="e")

        self.tools_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.tools_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 15), sticky="ew")

        self.auto_restore_var = ctk.BooleanVar(value=False)
        self.auto_restore_switch = ctk.CTkSwitch(
            self.tools_frame,
            text="复活自动恢复武器",
            variable=self.auto_restore_var,
            command=self.toggle_auto_restore,
            onvalue=True,
            offvalue=False
        )
        self.auto_restore_switch.pack(side="left", padx=(0, 20))

        self.current_weapon_label = ctk.CTkLabel(
            self.tools_frame,
            text="当前武器: 无",
            font=ctk.CTkFont(size=12),
            text_color=COLOR_GREEN
        )
        self.current_weapon_label.pack(side="left", padx=(0, 20))

        self.refresh_btn = ctk.CTkButton(
            self.tools_frame,
            text="刷新武器列表",
            command=self.refresh_weapon_list,
            fg_color=COLOR_ORANGE,
            hover_color="#e67e22",
            width=120
        )
        self.refresh_btn.pack(side="left", padx=(0, 10))

        self.clear_log_btn = ctk.CTkButton(
            self.tools_frame,
            text="清空日志",
            command=self.clear_log,
            fg_color=COLOR_ORANGE,
            hover_color="#e67e22",
            width=100
        )
        self.clear_log_btn.pack(side="left", padx=(0, 10))

        self.disconnect_btn = ctk.CTkButton(
            self.tools_frame,
            text="断开连接",
            command=self.disconnect,
            fg_color=COLOR_RED,
            hover_color="#c0392b",
            width=100
        )
        self.disconnect_btn.pack(side="left")

    def setup_weapon_list(self):
        self.weapon_scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLOR_DARK
        )
        self.weapon_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.refresh_weapon_list()

    def setup_log(self):
        self.log_frame = ctk.CTkFrame(self, fg_color=COLOR_DARKER, corner_radius=0)
        self.log_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
        self.log_frame.grid_columnconfigure(0, weight=1)

        self.log_title = ctk.CTkLabel(
            self.log_frame,
            text="📋 运行日志",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLOR_BLUE
        )
        self.log_title.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="w")

        self.log_text = ctk.CTkTextbox(
            self.log_frame,
            height=100,
            font=ctk.CTkFont(family="Consolas", size=10),
            fg_color=COLOR_DARKER,
            text_color="#ecf0f1"
        )
        self.log_text.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

    def refresh_weapon_list(self):
        for widget in self.weapon_scroll_frame.winfo_children():
            widget.destroy()

        for weapon_type in self.sorted_types:
            weapons = self.weapons_by_type[weapon_type]
            if not weapons:
                continue

            type_color = TYPE_COLORS.get(weapon_type, COLOR_DARKER)

            type_section = ctk.CTkFrame(
                self.weapon_scroll_frame,
                fg_color=type_color,
                corner_radius=8
            )
            type_section.pack(fill="x", padx=5, pady=(10, 5))

            type_header = ctk.CTkLabel(
                type_section,
                text=f"【{weapon_type}】(共{len(weapons)}个)",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#ecf0f1",
                anchor="w"
            )
            type_header.pack(fill="x", padx=15, pady=(10, 5))

            cards_frame = ctk.CTkFrame(type_section, fg_color="transparent")
            cards_frame.pack(fill="x", padx=10, pady=(0, 10))

            for i, weapon in enumerate(weapons):
                weapon_id, en_name, cn_name, w_type = weapon
                is_hero = (w_type == "英雄")

                row = i // 6
                col = i % 6

                card = ctk.CTkFrame(
                    cards_frame,
                    fg_color=COLOR_DARK if not is_hero else "#2c3e50",
                    corner_radius=5
                )
                card.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

                cards_frame.grid_columnconfigure(col, weight=1)

                id_label = ctk.CTkLabel(
                    card,
                    text=f"ID: {weapon_id}",
                    font=ctk.CTkFont(size=10, weight="bold"),
                    text_color=COLOR_GREEN if not is_hero else COLOR_RED
                )
                id_label.pack(padx=5, pady=(5, 2))

                name_label = ctk.CTkLabel(
                    card,
                    text=cn_name,
                    font=ctk.CTkFont(size=10),
                    text_color="#ecf0f1"
                )
                name_label.pack(padx=5, pady=(0, 5))

                give_btn = ctk.CTkButton(
                    card,
                    text="赋予",
                    width=60,
                    height=25,
                    command=lambda wid=weapon_id, name=cn_name: self.give_weapon_by_id(wid, name),
                    fg_color=COLOR_BLUE if not is_hero else COLOR_RED,
                    hover_color="#2980b9" if not is_hero else "#c0392b"
                )
                give_btn.pack(padx=5, pady=(0, 5))

    def toggle_auto_restore(self):
        self.auto_restore_enabled = self.auto_restore_var.get()
        if self.auto_restore_enabled:
            self.log("[INFO] 复活自动恢复武器已启用")
            if self.current_weapon_id:
                self.set_respawn_weapon(self.current_weapon_id, "当前武器")
        else:
            self.log("[INFO] 复活自动恢复武器已禁用")
            self.clear_respawn_weapon()

    def set_respawn_weapon(self, weapon_id, weapon_name):
        if not self.is_connected or not self.script:
            return

        def call():
            try:
                if not self.script or not self.is_connected:
                    return
                self.script.exports_sync.setrespawnweapon(weapon_id, weapon_name)
            except:
                pass

        threading.Thread(target=call, daemon=True).start()

    def clear_respawn_weapon(self):
        if not self.is_connected or not self.script:
            return

        def call():
            try:
                if not self.script or not self.is_connected:
                    return
                self.script.exports_sync.clearrespawnweapon()
            except:
                pass

        threading.Thread(target=call, daemon=True).start()

    def _safe_call(self, func):
        try:
            if self._initialized:
                self.after(0, func)
            else:
                func()
        except RuntimeError:
            pass

    def start_auto_connect(self):
        def connect_thread():
            while not self.is_connected:
                try:
                    for proc in psutil.process_iter(['pid', 'name']):
                        if proc.info['name'] == GAME_PROCESS_NAME:
                            self.connect_to_game(proc.info['pid'])
                            return
                except:
                    pass
                time.sleep(2)

        threading.Thread(target=connect_thread, daemon=True).start()

    def connect_to_game(self, pid):
        try:
            self.session = frida.attach(pid)
            with open(JS_FILE, 'r', encoding='utf-8') as f:
                script_code = f.read()

            self.script = self.session.create_script(script_code)
            self.script.on('message', self.on_message)
            self.script.load()

            self.is_connected = True
            self._safe_call(lambda: self.update_status(f"✅ 已连接到 {GAME_PROCESS_NAME} (PID: {pid})", COLOR_GREEN))
            self._safe_call(lambda: self.log(f"[SUCCESS] 已连接到游戏进程: {GAME_PROCESS_NAME} (PID: {pid})"))

            if self.auto_restore_enabled and self.current_weapon_id:
                self.set_respawn_weapon(self.current_weapon_id, "当前武器")

        except Exception as e:
            self.is_connected = False
            self.script = None
            self.session = None
            self._safe_call(lambda: self.update_status(f"❌ 连接失败: {e}", COLOR_RED))
            self._safe_call(lambda: self.log(f"[ERROR] 连接失败: {e}"))

    def update_status(self, text, color):
        self.status_label.configure(text=text, text_color=color)

    def log(self, message):
        if self.log_count >= self.max_logs:
            self.log_text.delete("1.0", "end")
            self.log_count = 0

        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")
        self.log_count += 1

    def on_message(self, message, data):
        if message['type'] == 'send':
            payload = message['payload']
            if payload['type'] == 'log':
                level = payload.get('level', 'info').upper()
                module = payload.get('module', 'Unknown')
                msg = payload.get('message', '')
                self._safe_call(lambda: self.log(f'[{level}][{module}] {msg}'))
            elif payload['type'] == 'giveWeaponResult':
                task_id = payload.get('taskId', '?')
                success = payload.get('success', False)
                if success:
                    self._safe_call(lambda tid=task_id: self.log(f'[SUCCESS] ✅ 武器赋予成功! (taskId={tid})'))
                else:
                    self._safe_call(lambda tid=task_id: self.log(f'[ERROR] ❌ 武器赋予失败 (taskId={tid})'))
            elif payload['type'] == 'playerRespawned':
                self._safe_call(lambda: self.on_player_respawn())
            elif payload['type'] == 'playerRespawnedWithWeapon':
                weapon_id = payload.get('weaponId')
                weapon_name = payload.get('weaponName', '未知武器')
                self._safe_call(lambda wid=weapon_id, wname=weapon_name: self.on_player_respawn_with_weapon(wid, wname))

    def on_player_respawn(self):
        if self.auto_restore_enabled and self.current_weapon_id:
            self.log(f"[INFO] 检测到玩家复活，自动恢复武器 ID: {self.current_weapon_id}")
            self.give_weapon_by_id(self.current_weapon_id, "自动恢复")

    def on_player_respawn_with_weapon(self, weapon_id, weapon_name):
        self.log(f'[SUCCESS] 检测到玩家复活，自动赋予武器: {weapon_name} (ID: {weapon_id})')
        self.give_weapon_by_id(weapon_id, weapon_name)

    def give_weapon_by_id(self, weapon_id, weapon_name=""):
        if not self.is_connected or not self.script:
            self.log("[ERROR] 未连接到游戏")
            return

        self.current_weapon_id = weapon_id
        if weapon_name:
            self.current_weapon_label.configure(text=f"当前武器: {weapon_name} (ID: {weapon_id})")

        if self.auto_restore_enabled:
            self.set_respawn_weapon(weapon_id, weapon_name)

        auto_giveup = True
        auto_select = True

        self.log(f"[INFO] 尝试赋予武器 ID: {weapon_id}, 名称: {weapon_name}")

        def call():
            try:
                if not self.script or not self.is_connected:
                    self._safe_call(lambda: self.log("[ERROR] 脚本已断开，请重新连接"))
                    return
                result = self.script.exports_sync.giveweapon(weapon_id, auto_giveup, auto_select)
                if isinstance(result, str) and result.startswith('pending:'):
                    task_id = result.split(':')[1]
                    self._safe_call(lambda tid=task_id: self.log(f"[INFO] ⏳ 任务已入队 (taskId={tid})，等待主线程执行..."))
                else:
                    self._safe_call(lambda r=result: self.log(f"[SUCCESS] 武器赋予结果: {r}"))
            except frida.InvalidOperationError:
                self.is_connected = False
                self.script = None
                self.session = None
                self._safe_call(lambda: self.update_status("⏳ 连接已断开，等待重连...", COLOR_ORANGE))
                self._safe_call(lambda: self.log("[ERROR] Frida会话已失效，请重新连接"))
            except Exception as ex:
                error_msg = str(ex)
                if "script has been destroyed" in error_msg:
                    self.is_connected = False
                    self.script = None
                    self.session = None
                    self._safe_call(lambda: self.update_status("⏳ 连接已断开，等待重连...", COLOR_ORANGE))
                    self._safe_call(lambda: self.log("[ERROR] 脚本已销毁，请重新连接"))
                else:
                    self._safe_call(lambda msg=error_msg: self.log(f"[ERROR] 武器赋予失败: {msg}"))

        threading.Thread(target=call, daemon=True).start()

    def clear_log(self):
        self.log_text.delete("1.0", "end")
        self.log_count = 0
        self.log("[INFO] 日志已清空")

    def disconnect(self):
        try:
            if self.script:
                self.script.unload()
        except:
            pass
        try:
            if self.session:
                self.session.detach()
        except:
            pass

        self.is_connected = False
        self.script = None
        self.session = None
        self.update_status("⏳ 等待连接...", COLOR_ORANGE)
        self.log("[INFO] 已断开连接，将在2秒后自动重连...")
        self.after(2000, self.start_auto_connect)


if __name__ == "__main__":
    app = WeaponHeroUI()
    app.mainloop()
