from dataclasses import dataclass

import customtkinter as ctk

from ui.pages.plugin_feature_page import PluginFeaturePage


@dataclass
class FeatureTabsHandles:
    knife_speed_var: ctk.DoubleVar
    knife_switch: ctk.CTkSwitch
    knife_speed_label: ctk.CTkLabel
    recoil_switch: ctk.CTkSwitch
    ammo_switch: ctk.CTkSwitch
    ammoplus_switch: ctk.CTkSwitch
    range_var: ctk.DoubleVar
    range_switch: ctk.CTkSwitch
    range_label: ctk.CTkLabel
    aim_switch: ctk.CTkSwitch
    speedgun_switch: ctk.CTkSwitch
    move_speed_var: ctk.DoubleVar
    move_switch: ctk.CTkSwitch
    move_speed_label: ctk.CTkLabel
    time_switch: ctk.CTkSwitch
    gravity_switch: ctk.CTkSwitch
    gravity_var: ctk.DoubleVar
    gravity_slider: ctk.CTkSlider
    gravity_label: ctk.CTkLabel
    jump_var: ctk.DoubleVar
    jump_slider: ctk.CTkSlider
    jump_label: ctk.CTkLabel
    gravity_mode_var: ctk.StringVar
    gravity_mode_combo: ctk.CTkComboBox
    godmode_switch: ctk.CTkSwitch
    skillcd_switch: ctk.CTkSwitch
    gather_switch: ctk.CTkSwitch
    gather_btn: ctk.CTkButton
    isbot_switch: ctk.CTkSwitch
    isbot_status_label: ctk.CTkLabel
    skip_round_btn: ctk.CTkButton
    esp_box_switch: ctk.CTkSwitch
    timescale_switch: ctk.CTkSwitch
    timescale_var: ctk.DoubleVar
    timescale_slider: ctk.CTkSlider
    timescale_label: ctk.CTkLabel


class FeatureTabsView:
    def __init__(
        self,
        *,
        plugin_registry,
        on_toggle_feature,
        on_knife_speed_change,
        on_move_speed_change,
        on_range_change,
        on_timescale_change,
        on_gravity_change,
        on_jump_change,
        on_gravity_mode_change,
        on_gather,
        on_skip_round,
    ):
        callbacks = {
            "toggle": on_toggle_feature,
            "slider": {
                "knife": on_knife_speed_change,
                "movespeed": on_move_speed_change,
                "range": on_range_change,
                "timescale": on_timescale_change,
            },
            "gravity": on_gravity_change,
            "jump": on_jump_change,
            "gravity_mode": on_gravity_mode_change,
            "gather": on_gather,
            "skip_round": on_skip_round,
        }
        self._page = PluginFeaturePage(plugin_registry, callbacks)

    def build(self, *, weapon_scroll, player_scroll, other_scroll):
        handles = {}
        handles.update(self._page.build_tab(weapon_scroll, "weapon_tab"))
        handles.update(self._page.build_tab(player_scroll, "player_tab"))
        handles.update(self._page.build_tab(other_scroll, "other_tab"))
        return FeatureTabsHandles(**handles)
