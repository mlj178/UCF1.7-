# ============================================================
# weapon_hero_ui_v2.py - 武器赋予与英雄变身UI（修正版）
#
# 功能：
#   - 武器和英雄统一通过武器ID赋予
#   - 可视化武器列表
#   - 搜索和筛选功能
#   - 参考AAAAA-ui_template.py模板
#
# 游戏进程：UnityCrossFire.exe
# ============================================================

import customtkinter as ctk
import frida
import psutil
import threading
import time
import os
import sys
from datetime import datetime

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
    ("5", "KNIFE", "刀", "近战"),
    ("6", "GRENADE", "手雷", "投掷"),
    ("11", "M4A1", "M4A1", "步枪"),
    ("12", "AK-47", "AK-47", "步枪"),
    ("17", "M60", "M60", "机枪"),
    ("20", "Desert Eagle", "沙漠之鹰", "手枪"),
    ("35", "轻型军用手斧", "轻型军用手斧", "近战"),
    ("45", "M4A1-A", "M4A1-A", "步枪"),
    ("53", "Desert Eagle-A", "沙漠之鹰-A", "手枪"),
    ("56", "黄金AK-47", "黄金AK-47", "步枪"),
    ("57", "M4A1-S", "M4A1-S", "步枪"),
    ("60", "黄金沙漠之鹰", "黄金沙漠之鹰", "手枪"),
    ("61", "RPK机关枪", "RPK机关枪", "机枪"),
    ("69", "Barrett M82A1", "Barrett M82A1", "狙击"),
    ("76", "M4A1-小鸡", "M4A1-小鸡", "步枪"),
    ("120", "NANOKNIFE", "NANOKNIFE", "近战"),
    ("124", "M60-A", "M60-A", "机枪"),
    ("125", "黄金M4A1", "黄金M4A1", "步枪"),
    ("126", "生化手雷", "生化手雷", "投掷"),
    ("176", "HULKFIST", "绿巨人拳头", "英雄"),
    ("177", "HOSTHULKFIST", "主机绿巨人拳头", "英雄"),
    ("178", "MASTERHULKFIST", "大师绿巨人拳头", "英雄"),
    ("182", "MASTERNANOKNIFE", "大师NANOKNIFE", "近战"),
    ("183", "汤姆逊冲锋枪", "汤姆逊冲锋枪", "冲锋"),
    ("195", "幽灵之刃", "幽灵之刃", "英雄"),
    ("197", "幽灵之刃", "幽灵之刃", "英雄"),
    ("210", "诅咒娃娃手雷", "诅咒娃娃手雷", "投掷"),
    ("223", "CRAZYKNIFE", "疯狂之刃", "近战"),
    ("226", "幽灵之刃", "幽灵之刃", "英雄"),
    ("237", "圣诞M4A1", "圣诞M4A1", "步枪"),
    ("244", "尼泊尔军刀", "尼泊尔军刀", "近战"),
    ("255", "M4A1-T", "M4A1-T", "步枪"),
    ("266", "M4A1-Red", "M4A1-Red", "步枪"),
    ("289", "M4A1-樱", "M4A1-樱", "步枪"),
    ("317", "M4A1-黑虎", "M4A1-黑虎", "步枪"),
    ("334", "毛瑟军用手枪", "毛瑟军用手枪", "手枪"),
    ("341", "AK47-茉莉", "AK47-茉莉", "步枪"),
    ("355", "M4A1-PINK", "M4A1-PINK", "步枪"),
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
    ("660", "M4A1-狼牙", "M4A1-狼牙", "步枪"),
    ("672", "GrandTerminator", "大终结者", "英雄"),
    ("730", "AK47-火麒麟", "AK47-火麒麟", "步枪"),
    ("758", "Barrett-翔龙", "Barrett-翔龙", "狙击"),
    ("761", "MG3-翔龙", "MG3-翔龙", "机枪"),
    ("764", "拳击手套", "拳击手套", "近战"),
    ("780", "M4A1-紫罗兰", "M4A1-紫罗兰", "步枪"),
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
    ("4270", "FAL CAMO", "FAL CAMO", "步枪"),
    ("4850", "机械英雄", "机械英雄", "英雄"),
    ("4851", "XM214重机枪", "XM214重机枪", "机枪"),
    ("4852", "奥术手榴弹", "奥术手榴弹", "投掷"),
    ("4853", "机枪守卫", "机枪守卫", "特殊"),
    ("4854", "不法终结者", "不法终结者", "英雄"),
    ("5359", "蝴蝶刀", "蝴蝶刀", "近战"),
    ("5361", "蝴蝶刀-枪王排位", "蝴蝶刀-枪王排位", "近战"),
    ("5384", "斯泰尔-枪娘暗刃", "斯泰尔-枪娘暗刃", "冲锋"),
]


class WeaponHeroUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("武器赋予与英雄变身工具 v2.0")
        self.geometry("1100x750")
        self.configure(fg_color=COLOR_DARK)

        self.session = None
        self.script = None
        self.is_connected = False
        self.log_count = 0
        self.max_logs = 500
        self.filtered_weapons = WEAPON_LIST.copy()
        self._initialized = False

        self.setup_ui()
        self.after(100, self._mark_initialized)
        self.start_auto_connect()

    def _mark_initialized(self):
        self._initialized = True

    def setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.setup_sidebar()
        self.setup_main_area()

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color=COLOR_DARKER)
        self.sidebar.grid(row=0, column=0, rowspan=3, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)

        self.title_label = ctk.CTkLabel(
            self.sidebar, 
            text="🎮 武器赋予与英雄变身",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLOR_BLUE
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        self.status_label = ctk.CTkLabel(
            self.sidebar,
            text="⏳ 等待连接...",
            font=ctk.CTkFont(size=12),
            text_color=COLOR_ORANGE
        )
        self.status_label.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        self.quick_section = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.quick_section.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(
            self.quick_section,
            text="⚡ 快速赋予",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLOR_GREEN
        ).grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")

        ctk.CTkLabel(self.quick_section, text="武器ID:").grid(row=1, column=0, pady=5, sticky="w")
        self.weapon_id_entry = ctk.CTkEntry(self.quick_section, width=100, placeholder_text="输入武器ID")
        self.weapon_id_entry.grid(row=1, column=1, padx=5, pady=5)

        self.give_weapon_btn = ctk.CTkButton(
            self.quick_section,
            text="赋予武器",
            command=self.give_weapon,
            fg_color=COLOR_GREEN,
            hover_color="#27ae60"
        )
        self.give_weapon_btn.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        self.options_frame = ctk.CTkFrame(self.quick_section, fg_color="transparent")
        self.options_frame.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

        self.auto_giveup_var = ctk.BooleanVar(value=True)
        self.auto_giveup_cb = ctk.CTkCheckBox(
            self.options_frame,
            text="自动放弃当前武器",
            variable=self.auto_giveup_var
        )
        self.auto_giveup_cb.pack(side="left", padx=5)

        self.auto_select_var = ctk.BooleanVar(value=True)
        self.auto_select_cb = ctk.CTkCheckBox(
            self.options_frame,
            text="自动选择新武器",
            variable=self.auto_select_var
        )
        self.auto_select_cb.pack(side="left", padx=5)

        self.tools_section = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.tools_section.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(
            self.tools_section,
            text="🔧 工具",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLOR_ORANGE
        ).grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")

        self.refresh_btn = ctk.CTkButton(
            self.tools_section,
            text="刷新武器列表",
            command=self.refresh_weapon_list,
            fg_color=COLOR_ORANGE,
            hover_color="#e67e22"
        )
        self.refresh_btn.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")

        self.clear_log_btn = ctk.CTkButton(
            self.tools_section,
            text="清空日志",
            command=self.clear_log,
            fg_color=COLOR_ORANGE,
            hover_color="#e67e22"
        )
        self.clear_log_btn.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")

        self.disconnect_btn = ctk.CTkButton(
            self.sidebar,
            text="断开连接",
            command=self.disconnect,
            fg_color=COLOR_RED,
            hover_color="#c0392b"
        )
        self.disconnect_btn.grid(row=7, column=0, padx=20, pady=20, sticky="ew")

    def setup_main_area(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=COLOR_DARK)
        self.main_frame.grid(row=0, column=1, rowspan=3, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.search_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.search_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(
            self.search_frame,
            text="🔍 搜索:",
            font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=5)

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            width=200,
            placeholder_text="输入武器名称或ID"
        )
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.on_search)

        self.filter_var = ctk.StringVar(value="全部")
        self.filter_menu = ctk.CTkOptionMenu(
            self.search_frame,
            values=["全部", "步枪", "手枪", "狙击", "机枪", "冲锋", "近战", "投掷", "英雄", "特殊"],
            command=self.on_filter,
            width=100
        )
        self.filter_menu.pack(side="left", padx=5)

        self.weapon_list_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color=COLOR_DARKER
        )
        self.weapon_list_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.log_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.log_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.log_frame.grid_columnconfigure(0, weight=1)

        self.log_title = ctk.CTkLabel(
            self.log_frame,
            text="📋 运行日志",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLOR_BLUE
        )
        self.log_title.grid(row=0, column=0, pady=5, sticky="w")

        self.log_text = ctk.CTkTextbox(
            self.log_frame,
            height=120,
            font=ctk.CTkFont(family="Consolas", size=10),
            fg_color=COLOR_DARKER,
            text_color="#ecf0f1"
        )
        self.log_text.grid(row=1, column=0, sticky="ew")

        self.refresh_weapon_list()

    def refresh_weapon_list(self):
        for widget in self.weapon_list_frame.winfo_children():
            widget.destroy()

        for weapon_id, en_name, cn_name, weapon_type in self.filtered_weapons:
            weapon_frame = ctk.CTkFrame(
                self.weapon_list_frame,
                fg_color=COLOR_DARK if weapon_type != "英雄" else "#2c3e50",
                corner_radius=5
            )
            weapon_frame.pack(fill="x", padx=5, pady=3)

            id_label = ctk.CTkLabel(
                weapon_frame,
                text=f"ID: {weapon_id}",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=COLOR_GREEN if weapon_type != "英雄" else COLOR_RED,
                width=70
            )
            id_label.pack(side="left", padx=10, pady=8)

            name_label = ctk.CTkLabel(
                weapon_frame,
                text=f"{cn_name} ({en_name})",
                font=ctk.CTkFont(size=11),
                text_color="#ecf0f1",
                anchor="w"
            )
            name_label.pack(side="left", padx=5, pady=8, fill="x", expand=True)

            type_label = ctk.CTkLabel(
                weapon_frame,
                text=weapon_type,
                font=ctk.CTkFont(size=10),
                text_color=COLOR_ORANGE,
                width=50
            )
            type_label.pack(side="left", padx=5, pady=8)

            give_btn = ctk.CTkButton(
                weapon_frame,
                text="赋予",
                width=60,
                command=lambda id=weapon_id: self.give_weapon_by_id(id),
                fg_color=COLOR_BLUE if weapon_type != "英雄" else COLOR_RED,
                hover_color="#2980b9" if weapon_type != "英雄" else "#c0392b"
            )
            give_btn.pack(side="right", padx=10, pady=8)

    def on_search(self, event=None):
        search_text = self.search_entry.get().lower()
        self.apply_filters(search_text, self.filter_var.get())

    def on_filter(self, choice):
        search_text = self.search_entry.get().lower()
        self.apply_filters(search_text, choice)

    def apply_filters(self, search_text, filter_type):
        self.filtered_weapons = []
        for weapon in WEAPON_LIST:
            weapon_id, en_name, cn_name, weapon_type = weapon
            
            if filter_type != "全部" and weapon_type != filter_type:
                continue
            
            if search_text:
                if (search_text not in weapon_id.lower() and 
                    search_text not in en_name.lower() and 
                    search_text not in cn_name.lower()):
                    continue
            
            self.filtered_weapons.append(weapon)
        
        self.refresh_weapon_list()

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
                self._safe_call(lambda: self.log(f"[{level}][{module}] {msg}"))
            elif payload['type'] == 'giveWeaponResult':
                task_id = payload.get('taskId', '?')
                success = payload.get('success', False)
                if success:
                    self._safe_call(lambda tid=task_id: self.log(f"[SUCCESS] ✅ 武器赋予成功! (taskId={tid})"))
                else:
                    self._safe_call(lambda tid=task_id: self.log(f"[ERROR] ❌ 武器赋予失败 (taskId={tid})"))

    def give_weapon(self):
        if not self.is_connected:
            self.log("[ERROR] 未连接到游戏")
            return

        weapon_id_str = self.weapon_id_entry.get()
        if not weapon_id_str:
            self.log("[ERROR] 请输入武器ID")
            return

        try:
            weapon_id = int(weapon_id_str)
            self.give_weapon_by_id(weapon_id)
        except ValueError:
            self.log("[ERROR] 武器ID必须是数字")

    def give_weapon_by_id(self, weapon_id):
        if not self.is_connected or not self.script:
            self.log("[ERROR] 未连接到游戏")
            return

        auto_giveup = self.auto_giveup_var.get()
        auto_select = self.auto_select_var.get()

        self.log(f"[INFO] 尝试赋予武器 ID={weapon_id} (autoGiveUp={auto_giveup}, autoSelect={auto_select})")

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
