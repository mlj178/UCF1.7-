from __future__ import annotations

from pathlib import Path
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk

sys.path.insert(0, str(Path(__file__).resolve().parent))

from player_profile_service import (  # noqa: E402
    PlayerProfile,
    get_default_player_data_path,
    load_profile,
    save_profile,
)


FEATURE_ID = "player_profile_editor"
WINDOW_TITLE = "玩家信息修改器"


class PlayerProfileEditorApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title(WINDOW_TITLE)
        self.geometry("760x520")
        self.minsize(720, 480)

        self.file_path_var = tk.StringVar(value=str(get_default_player_data_path()))
        self.nickname_var = tk.StringVar(value="内個")
        self.level_var = tk.StringVar(value="30")
        self.vip_level_var = tk.StringVar(value="2")
        self.status_var = tk.StringVar(value="未保存")

        self._build_ui()
        self._log("工具已启动")
        self._log(f"默认路径: {self.file_path_var.get()}")
        self.load_current_profile(show_missing=False)

    def _build_ui(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        path_frame = ctk.CTkFrame(self)
        path_frame.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        path_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(path_frame, text="文件").grid(row=0, column=0, padx=(12, 8), pady=12)
        ctk.CTkEntry(path_frame, textvariable=self.file_path_var).grid(row=0, column=1, sticky="ew", pady=12)
        ctk.CTkButton(path_frame, text="选择", width=72, command=self.choose_file).grid(
            row=0, column=2, padx=8, pady=12
        )
        ctk.CTkButton(path_frame, text="读取", width=72, command=self.load_current_profile).grid(
            row=0, column=3, padx=(0, 12), pady=12
        )

        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=0, sticky="ew", padx=16, pady=8)
        form_frame.grid_columnconfigure((1, 3, 5), weight=1)

        ctk.CTkLabel(form_frame, text="昵称").grid(row=0, column=0, padx=(12, 8), pady=16)
        ctk.CTkEntry(form_frame, textvariable=self.nickname_var).grid(row=0, column=1, sticky="ew", pady=16)

        ctk.CTkLabel(form_frame, text="等级").grid(row=0, column=2, padx=(16, 8), pady=16)
        ctk.CTkEntry(form_frame, textvariable=self.level_var, width=90).grid(row=0, column=3, sticky="ew", pady=16)

        ctk.CTkLabel(form_frame, text="VIP等级").grid(row=0, column=4, padx=(16, 8), pady=16)
        ctk.CTkEntry(form_frame, textvariable=self.vip_level_var, width=90).grid(
            row=0, column=5, sticky="ew", padx=(0, 12), pady=16
        )

        action_frame = ctk.CTkFrame(self)
        action_frame.grid(row=2, column=0, sticky="ew", padx=16, pady=8)
        action_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(action_frame, textvariable=self.status_var, anchor="w").grid(
            row=0, column=0, sticky="ew", padx=12, pady=12
        )
        ctk.CTkButton(action_frame, text="保存到 PlayerData.dat", command=self.save_current_profile).grid(
            row=0, column=1, padx=12, pady=12
        )

        self.log_box = ctk.CTkTextbox(self)
        self.log_box.grid(row=3, column=0, sticky="nsew", padx=16, pady=(8, 16))
        self.log_box.configure(state="disabled")

    def choose_file(self) -> None:
        initial_path = Path(self.file_path_var.get())
        chosen = filedialog.askopenfilename(
            title="选择 PlayerData.dat",
            initialdir=str(initial_path.parent if initial_path.parent.exists() else Path.home()),
            filetypes=[("PlayerData", "PlayerData.dat"), ("All files", "*.*")],
        )
        if chosen:
            self.file_path_var.set(chosen)
            self._log(f"已选择文件: {chosen}")
            self.load_current_profile(show_missing=False)

    def load_current_profile(self, show_missing: bool = True) -> None:
        path = Path(self.file_path_var.get())
        try:
            profile = load_profile(path)
        except Exception as exc:
            self.status_var.set("读取失败")
            self._log(f"读取失败: {exc}")
            messagebox.showerror(WINDOW_TITLE, str(exc))
            return

        if profile is None:
            if show_missing:
                self._log("没有读取到 [Player]，保存时会自动添加")
            return

        self.nickname_var.set(profile.nickname)
        self.level_var.set(str(profile.level))
        self.vip_level_var.set(str(profile.vip_level))
        self.status_var.set("已读取现有 [Player]")
        self._log("已读取现有 [Player] 信息")

    def save_current_profile(self) -> None:
        path = Path(self.file_path_var.get())
        try:
            profile = PlayerProfile(
                nickname=self.nickname_var.get(),
                level=int(self.level_var.get()),
                vip_level=int(self.vip_level_var.get()),
            )
            result = save_profile(path, profile)
        except ValueError as exc:
            self.status_var.set("输入不合法")
            self._log(f"输入不合法: {exc}")
            messagebox.showwarning(WINDOW_TITLE, str(exc))
            return
        except Exception as exc:
            self.status_var.set("保存失败")
            self._log(f"保存失败: {exc}")
            messagebox.showerror(WINDOW_TITLE, str(exc))
            return

        if result.created_file:
            self.status_var.set("已新建并保存")
            self._log(f"文件不存在，已新建: {result.path}")
        else:
            self.status_var.set("保存成功")
            self._log(f"保存成功: {result.path}")
            self._log(f"备份文件: {result.backup_path}")

    def _log(self, message: str) -> None:
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{FEATURE_ID}] {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")


def main() -> None:
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = PlayerProfileEditorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
