import customtkinter as ctk

from .player_profile_service import get_default_player_data_path


def build_card(parent, manifest, row, col, colspan, callbacks, card_builder):
    feature_id = manifest["feature_id"]
    frame = ctk.CTkFrame(parent, corner_radius=6, fg_color="#3a3a3a", border_width=1, border_color="#555555")
    frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)
    frame.grid_columnconfigure(1, weight=1)
    ctk.CTkLabel(frame, text=manifest.get("display_name", ""), font=("Microsoft YaHei", 15, "bold"), text_color=manifest.get("layout", {}).get("title_color", "#60a5fa")).grid(row=0, column=0, columnspan=3, sticky="w", padx=12, pady=(8, 2))
    ctk.CTkLabel(frame, text=manifest.get("desc", ""), text_color="#cbd5e1", font=("Microsoft YaHei", 12), anchor="w", justify="left", wraplength=560).grid(row=1, column=0, columnspan=3, sticky="ew", padx=12, pady=(0, 6))

    path_text = str(get_default_player_data_path())
    ctk.CTkLabel(frame, text="文件", width=55, anchor="w").grid(row=2, column=0, padx=(12, 6), pady=4)
    ctk.CTkLabel(frame, text=path_text, anchor="w", justify="left", wraplength=430).grid(row=2, column=1, columnspan=2, sticky="ew", padx=(0, 12), pady=4)

    nickname_var = ctk.StringVar(value="内個")
    level_var = ctk.StringVar(value="30")
    vip_var = ctk.StringVar(value="2")
    for row_index, label, variable in ((3, "昵称", nickname_var), (4, "等级", level_var), (5, "VIP等级", vip_var)):
        ctk.CTkLabel(frame, text=label, width=75, anchor="w").grid(row=row_index, column=0, padx=(12, 6), pady=3)
        ctk.CTkEntry(frame, textvariable=variable).grid(row=row_index, column=1, columnspan=2, sticky="ew", padx=(0, 12), pady=3)

    status = ctk.CTkLabel(frame, text="未读取", text_color="#facc15", anchor="w")
    status.grid(row=6, column=0, columnspan=3, sticky="ew", padx=12, pady=(5, 2))
    buttons = ctk.CTkFrame(frame, fg_color="transparent")
    buttons.grid(row=7, column=0, columnspan=3, sticky="ew", padx=12, pady=(2, 8))
    buttons.grid_columnconfigure((0, 1), weight=1, uniform="profile_actions")

    def read():
        result = callbacks["action"](feature_id, "load_profile", {"path": path_text})
        if not result or result is False:
            status.configure(text="读取失败", text_color="#f87171")
            return
        profile = result.get("profile")
        if profile:
            nickname_var.set(profile["nickname"])
            level_var.set(str(profile["level"]))
            vip_var.set(str(profile["vip_level"]))
            status.configure(text="已读取现有 [Player]", text_color="#4ade80")
        else:
            status.configure(text="未找到 [Player]，保存时会自动添加", text_color="#facc15")

    def save():
        try:
            payload = {"path": path_text, "nickname": nickname_var.get(), "level": int(level_var.get()), "vip_level": int(vip_var.get())}
            result = callbacks["action"](feature_id, "save_profile", payload)
        except ValueError:
            status.configure(text="等级和 VIP 等级必须是数字", text_color="#f87171")
            return
        if result and result is not False and result.get("ok", True):
            status.configure(text=result.get("message", "保存成功"), text_color="#4ade80")
        else:
            status.configure(text=(result or {}).get("message", "保存失败"), text_color="#f87171")

    ctk.CTkButton(buttons, text="读取", command=read, fg_color="#2563eb", hover_color="#1d4ed8").grid(row=0, column=0, sticky="ew", padx=(0, 4))
    ctk.CTkButton(buttons, text="保存到 PlayerData.dat", command=save, fg_color="#16a34a", hover_color="#15803d").grid(row=0, column=1, sticky="ew", padx=(4, 0))
    read()
    return {}
