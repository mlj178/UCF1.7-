import customtkinter as ctk
import os
import webbrowser

from core.config import FEATURES_INFO, DATA_DIR, RESOURCE_DIR, HOTKEY_POSITIONS, HOTKEY_DISPLAY_NAMES, HOTKEY_EXCLUDED
from core.hotkey_manager import HotkeyManager
from core.sound_manager import SoundManager


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("设置")
        self.geometry("500x650")
        self.resizable(False, False)
        self.attributes('-topmost', True)
        self.transient(parent)
        self.grab_set()

        self._parent = parent
        self._hotkey = HotkeyManager.get_instance()
        self._sound = SoundManager.get_instance()

        self._setup_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_save)

    def _setup_ui(self):
        self._tabview = ctk.CTkTabview(self, corner_radius=8)
        self._tabview.pack(fill="both", expand=True, padx=12, pady=12)

        self._setup_hotkey_tab()
        self._setup_about_tab()

    def _setup_hotkey_tab(self):
        tab = self._tabview.add("快捷键")
        hotkey_frame = ctk.CTkScrollableFrame(tab, corner_radius=0)
        hotkey_frame.pack(fill="both", expand=True, padx=4, pady=4)

        ctk.CTkLabel(hotkey_frame, text="快捷键绑定 - 功能互斥绑定",
                     font=("Microsoft YaHei", 14, "bold")).pack(pady=(12, 6))

        feature_display_names = {v['icon'] + ' ' + v['name']: k for k, v in FEATURES_INFO.items()
                                 if k not in HOTKEY_EXCLUDED}
        self._feature_display_names = feature_display_names

        self._combo_widgets = {}

        hotkey_data = self._hotkey.get_hotkey_config()

        for pos, fid in hotkey_data.items():
            if fid in HOTKEY_EXCLUDED:
                self._hotkey.remove_hotkey(pos)
                hotkey_data[pos] = None

        def get_available_features(exclude_pos=None):
            available = ["未绑定"]
            for display_name, feature_id in feature_display_names.items():
                is_bound = False
                for pos, feat in hotkey_data.items():
                    if pos != exclude_pos and feat == feature_id:
                        is_bound = True
                        break
                if not is_bound:
                    available.append(display_name)
            return available

        def update_combo_options():
            for pos, combo in self._combo_widgets.items():
                current_value = combo.get()
                available = get_available_features(exclude_pos=pos)
                combo.configure(values=available)
                if current_value not in available:
                    combo.set("未绑定")
                    self._hotkey.remove_hotkey(pos)
                    hotkey_data[pos] = None

        for pos in HOTKEY_POSITIONS:
            row_frame = ctk.CTkFrame(hotkey_frame, fg_color="#2a2a2a")
            row_frame.pack(fill="x", padx=8, pady=3)

            display_name = HOTKEY_DISPLAY_NAMES.get(pos, pos)
            ctk.CTkLabel(row_frame, text=display_name, font=("Microsoft YaHei", 12),
                         text_color="#aaa", width=60).pack(side="left", padx=8)

            feature_id = hotkey_data.get(pos)
            feature_info = FEATURES_INFO.get(feature_id)
            feature_name = feature_info['icon'] + ' ' + feature_info['name'] if feature_info else "未绑定"

            available_features = get_available_features(exclude_pos=pos)
            combo = ctk.CTkComboBox(row_frame, values=available_features,
                                     state="readonly", width=150)
            combo.pack(side="left", padx=8)
            combo.set(feature_name)

            self._combo_widgets[pos] = combo

            def on_combo_change(selected, position=pos):
                if selected and selected != "未绑定":
                    fid = feature_display_names[selected]
                    self._hotkey.set_hotkey(position, fid)
                    hotkey_data[position] = fid
                else:
                    self._hotkey.remove_hotkey(position)
                    hotkey_data[position] = None
                update_combo_options()

            combo.configure(command=on_combo_change)

        save_btn = ctk.CTkButton(self, text="保存并应用", width=100,
                                  command=self._on_save,
                                  fg_color="#007acc", hover_color="#005a99")
        save_btn.pack(pady=(0, 12))

    def _setup_about_tab(self):
        tab = self._tabview.add("关于")
        about_frame = ctk.CTkScrollableFrame(tab, corner_radius=0)
        about_frame.pack(fill="both", expand=True, padx=4, pady=4)

        ctk.CTkLabel(about_frame, text="游戏修改器控制台 - 全功能整合包 v1.6",
                     font=("Microsoft YaHei", 18, "bold")).pack(pady=(12, 4))
        ctk.CTkLabel(about_frame, text="版本: v1.6 (模块化架构)",
                     font=("Microsoft YaHei", 12)).pack(pady=2)
        ctk.CTkLabel(about_frame, text="作者: 挂呱呱呱",
                     font=("Microsoft YaHei", 12)).pack(pady=2)

        ctk.CTkLabel(about_frame, text="\nQQ群: 1095388251",
                     font=("Microsoft YaHei", 12)).pack(pady=4)

        bili_frame = ctk.CTkFrame(about_frame, fg_color="transparent")
        bili_frame.pack(pady=(12, 4))
        ctk.CTkLabel(bili_frame, text="B站: ", font=("Microsoft YaHei", 12)).pack(side="left")
        bili_btn = ctk.CTkButton(bili_frame, text="🔗 BiliBili", font=("Microsoft YaHei", 11),
                                   width=100, command=self._open_bilibili)
        bili_btn.pack(side="left")

        ctk.CTkLabel(about_frame, text="\n微信赞赏码:",
                     font=("Microsoft YaHei", 12)).pack(pady=4)
        donate_image_path = os.path.join(RESOURCE_DIR, "微信赞赏码.png")
        if os.path.exists(donate_image_path):
            try:
                from PIL import Image
                donate_image = Image.open(donate_image_path)
                donate_image = donate_image.resize((225, 225), Image.LANCZOS)
                donate_photo = ctk.CTkImage(light_image=donate_image, dark_image=donate_image,
                                             size=(225, 225))
                donate_label = ctk.CTkLabel(about_frame, image=donate_photo, text="")
                donate_label.pack(pady=4)
            except Exception as e:
                ctk.CTkLabel(about_frame, text=f"加载图片失败: {e}",
                             font=("Microsoft YaHei", 11), text_color="#888").pack(pady=4)
        else:
            ctk.CTkLabel(about_frame, text="赞赏码图片未找到",
                         font=("Microsoft YaHei", 11), text_color="#888").pack(pady=4)

    def _open_bilibili(self):
        webbrowser.open("https://space.bilibili.com/481324794")

    def _on_save(self):
        self._hotkey.save_and_apply(
            self._parent._on_hotkey_toggle if hasattr(self._parent, '_on_hotkey_toggle') else lambda fid: None
        )
        self.destroy()
