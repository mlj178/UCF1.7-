"""CustomTkinter UI for the brightness_probe single-feature probe."""

import os
import queue
import threading
import time

import customtkinter as ctk
import frida
import psutil


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JS_FILE = os.path.join(BASE_DIR, "AAAAA-brightness_probe_min.js")
GAME_PROCESS_NAME = "UnityCrossFire.exe"

GREEN = "#2ecc71"
ORANGE = "#f39c12"
RED = "#e74c3c"
PANEL = "#1d2430"
PANEL_DARK = "#151b24"

DEFAULT_CONFIG = {
    "exposure": 1.5,
    "contrast": 0.0,
    "saturation": 0.0,
    "gamma": 0.0,
    "gain": 0.0,
    "force_render_post_processing": False,
    "update_volume_stack": True,
}


class BrightnessProbeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("亮度调节探针")
        self.geometry("660x760")
        self.minsize(600, 700)

        self.session = None
        self.script = None
        self.connected = False
        self.connecting = False
        self.closing = False
        self.rpc_busy = False
        self.status_busy = False
        self.shutdown_done = False

        self.ui_queue = queue.Queue()
        self.rpc_lock = threading.Lock()

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(100, self._drain_ui_queue)
        self.after(600, self._schedule_connect)

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)

        ctk.CTkLabel(self, text="亮度调节探针", font=ctk.CTkFont(size=24, weight="bold")).grid(
            row=0, column=0, padx=18, pady=(18, 4), sticky="ew"
        )
        ctk.CTkLabel(
            self,
            text="验证 URP ColorAdjustments.postExposure 是否能真实影响游戏画面",
            text_color="#95a0af",
            font=ctk.CTkFont(size=12),
        ).grid(row=1, column=0, padx=18, pady=(0, 8), sticky="ew")

        status = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL)
        status.grid(row=2, column=0, padx=18, pady=5, sticky="ew")
        status.grid_columnconfigure(1, weight=1)
        self.status_dot = ctk.CTkLabel(status, text="●", text_color="#777")
        self.status_dot.grid(row=0, column=0, padx=(12, 5), pady=10)
        self.connection_label = ctk.CTkLabel(status, text="等待游戏启动...")
        self.connection_label.grid(row=0, column=1, padx=5, pady=10, sticky="w")
        self.pid_label = ctk.CTkLabel(status, text="", text_color="#999")
        self.pid_label.grid(row=0, column=2, padx=12, pady=10)

        controls = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL_DARK)
        controls.grid(row=3, column=0, padx=18, pady=5, sticky="ew")
        controls.grid_columnconfigure(1, weight=1)

        self.exposure_slider, self.exposure_value_label = self._add_slider_control(
            controls, 0, "曝光", "exposure", -2.0, 4.0, 60, "{:.2f}"
        )
        self.contrast_slider, self.contrast_value_label = self._add_slider_control(
            controls, 2, "对比度", "contrast", -50.0, 50.0, 100, "{:.0f}"
        )
        self.saturation_slider, self.saturation_value_label = self._add_slider_control(
            controls, 4, "饱和度", "saturation", -100.0, 100.0, 200, "{:.0f}"
        )
        self.gamma_slider, self.gamma_value_label = self._add_slider_control(
            controls, 6, "中间调 Gamma", "gamma", -1.0, 1.0, 100, "{:.2f}"
        )
        self.gain_slider, self.gain_value_label = self._add_slider_control(
            controls, 8, "亮部 Gain", "gain", -1.0, 1.0, 100, "{:.2f}"
        )

        self.force_post_switch = ctk.CTkSwitch(
            controls,
            text="强制开启相机后处理",
            command=self._on_config_changed,
            progress_color=ORANGE,
        )
        self.force_post_switch.grid(row=10, column=0, columnspan=3, padx=12, pady=(8, 12), sticky="w")

        actions = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL)
        actions.grid(row=4, column=0, padx=18, pady=5, sticky="ew")
        actions.grid_columnconfigure((0, 1), weight=1)

        self.apply_button = ctk.CTkButton(actions, text="应用参数", command=self._apply_brightness, height=34, fg_color=GREEN)
        self.apply_button.grid(row=0, column=0, padx=8, pady=12, sticky="ew")
        self.reset_button = ctk.CTkButton(actions, text="恢复游戏初始值", command=self._reset_brightness, height=34, fg_color=ORANGE)
        self.reset_button.grid(row=0, column=1, padx=8, pady=12, sticky="ew")

        metrics = ctk.CTkFrame(self, corner_radius=8, fg_color=PANEL_DARK)
        metrics.grid(row=5, column=0, padx=18, pady=5, sticky="ew")
        metrics.grid_columnconfigure((0, 1, 2), weight=1)
        self.locate_label = self._add_metric(metrics, 0, "ColorAdjustments", "未定位")
        self.post_label = self._add_metric(metrics, 1, "后处理", "未知")
        self.exposure_label = self._add_metric(metrics, 2, "读回曝光", "-")

        self.detail_label = ctk.CTkLabel(
            self,
            text="连接游戏后可直接应用参数；应用后需要在游戏内目测画面是否变化。",
            text_color="#9aa3b2",
            font=ctk.CTkFont(size=12),
        )
        self.detail_label.grid(row=6, column=0, padx=18, pady=(6, 4), sticky="ew")

        self.log_box = ctk.CTkTextbox(self, height=190, font=ctk.CTkFont(size=11))
        self.log_box.grid(row=7, column=0, padx=18, pady=(4, 16), sticky="nsew")
        self.log_box.configure(state="disabled")

        self._set_controls_enabled(False)

    def _add_metric(self, parent, column, title, value):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=column, padx=8, pady=10, sticky="ew")
        ctk.CTkLabel(frame, text=title, text_color="#8f98a8", font=ctk.CTkFont(size=11)).pack()
        label = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=15, weight="bold"))
        label.pack(pady=(2, 0))
        return label

    def _add_slider_control(self, parent, row, title, key, from_, to, steps, value_format):
        ctk.CTkLabel(parent, text=title, font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=row, column=0, padx=12, pady=(10 if row else 12, 4), sticky="w"
        )
        label = ctk.CTkLabel(parent, text=value_format.format(DEFAULT_CONFIG[key]))
        label.grid(row=row, column=2, padx=12, pady=(10 if row else 12, 4), sticky="e")
        slider = ctk.CTkSlider(
            parent,
            from_=from_,
            to=to,
            number_of_steps=steps,
            command=self._on_config_changed,
        )
        slider.grid(row=row + 1, column=0, columnspan=3, padx=12, pady=(0, 6), sticky="ew")
        slider.set(DEFAULT_CONFIG[key])
        return slider, label

    def _post(self, event, *args):
        if not self.closing:
            self.ui_queue.put((event, args))

    def _post_allow_closing(self, event, *args):
        self.ui_queue.put((event, args))
        try:
            self.after(0, self._drain_ui_queue)
        except Exception:
            pass

    def _drain_ui_queue(self):
        try:
            while True:
                event, args = self.ui_queue.get_nowait()
                self._handle_event(event, *args)
        except queue.Empty:
            pass
        if not self.closing:
            self.after(100, self._drain_ui_queue)

    def _handle_event(self, event, *args):
        if event == "log":
            self._log(args[0])
        elif event == "waiting":
            self._set_connection(False, args[0], args[1] if len(args) > 1 else "")
        elif event == "connected":
            self._on_connected(args[0])
        elif event == "detached":
            self._on_detached(args[0])
        elif event == "retry_connect":
            self.after(800, self._schedule_connect)
        elif event == "rpc_done":
            self.rpc_busy = False
            self._render_status(args[0])
            self._set_controls_enabled(self.connected)
        elif event == "rpc_error":
            self.rpc_busy = False
            self._log("操作失败：" + str(args[0]))
            self._set_controls_enabled(self.connected)
        elif event == "status":
            self._render_status(args[0])
        elif event == "destroy":
            self.destroy()

    def _log(self, text):
        stamp = time.strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{stamp}] {text}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _set_connection(self, connected, text, pid_text=""):
        self.status_dot.configure(text_color=GREEN if connected else "#777")
        self.connection_label.configure(text=text)
        self.pid_label.configure(text=pid_text)

    def _set_controls_enabled(self, enabled):
        state = "normal" if enabled and not self.rpc_busy else "disabled"
        for widget in (
            self.apply_button,
            self.reset_button,
            self.exposure_slider,
            self.contrast_slider,
            self.saturation_slider,
            self.gamma_slider,
            self.gain_slider,
            self.force_post_switch,
        ):
            widget.configure(state=state)

    def _find_game_pid(self):
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if proc.info["name"] == GAME_PROCESS_NAME:
                    return proc.info["pid"]
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None

    def _schedule_connect(self):
        if self.closing or self.connected or self.connecting:
            return
        threading.Thread(target=self._connect_worker, daemon=True).start()

    def _connect_worker(self):
        self.connecting = True
        try:
            pid = self._find_game_pid()
            if not pid:
                self._post("waiting", "等待游戏启动...", "")
                self._post("retry_connect")
                return

            self._post("waiting", "正在连接游戏...", f"PID {pid}")
            self.session = frida.attach(pid)
            with open(JS_FILE, "r", encoding="utf-8") as f:
                source = f.read()
            self.script = self.session.create_script(source)
            self.script.on("message", self._on_message)
            self.session.on("detached", self._on_detached_frida)
            self.script.load()
            self.connected = True
            self._post("connected", pid)
            self._call_rpc_sequence((("setconfig", self._current_config()), ("enable",)))
            self.after(1000, self._poll_status)
        except Exception as exc:
            self._post("log", "连接失败：" + str(exc))
            self._post("waiting", "连接失败，稍后重试...", "")
            self._post("retry_connect")
        finally:
            self.connecting = False

    def _on_connected(self, pid):
        self._set_connection(True, "已连接游戏", f"PID {pid}")
        self._set_controls_enabled(True)
        self._log("脚本已加载，可直接应用参数")

    def _on_detached_frida(self, reason, crash=None):
        detail = str(reason)
        if crash:
            detail += " " + str(crash)
        self._post("detached", detail)

    def _on_detached(self, detail):
        self.connected = False
        self.script = None
        self.session = None
        self._set_connection(False, "游戏已断开", "")
        self._set_controls_enabled(False)
        self._log("已断开：" + str(detail))
        if not self.closing:
            self.after(1000, self._schedule_connect)

    def _on_message(self, message, data):
        if message.get("type") == "send":
            payload = message.get("payload", {})
            if isinstance(payload, dict) and payload.get("type") == "log":
                self._post("log", payload.get("message", ""))
        elif message.get("type") == "error":
            self._post("log", message.get("stack", message.get("description", "Frida error")))
        else:
            self._post("log", str(message))

    def _current_config(self):
        return {
            "exposure": float(self.exposure_slider.get()),
            "contrast": float(self.contrast_slider.get()),
            "saturation": float(self.saturation_slider.get()),
            "gamma": float(self.gamma_slider.get()),
            "gain": float(self.gain_slider.get()),
            "force_render_post_processing": bool(self.force_post_switch.get()),
            "update_volume_stack": True,
        }

    def _on_config_changed(self, *_):
        required = (
            "exposure_slider",
            "contrast_slider",
            "saturation_slider",
            "gamma_slider",
            "gain_slider",
        )
        if not all(hasattr(self, name) for name in required):
            return
        exposure = float(self.exposure_slider.get())
        contrast = float(self.contrast_slider.get())
        saturation = float(self.saturation_slider.get())
        gamma = float(self.gamma_slider.get())
        gain = float(self.gain_slider.get())
        self.exposure_value_label.configure(text=f"{exposure:.2f}")
        self.contrast_value_label.configure(text=f"{contrast:.0f}")
        self.saturation_value_label.configure(text=f"{saturation:.0f}")
        self.gamma_value_label.configure(text=f"{gamma:.2f}")
        self.gain_value_label.configure(text=f"{gain:.2f}")
        if self.connected:
            self._call_rpc("setconfig", self._current_config())

    def _apply_brightness(self):
        self._call_rpc_sequence(
            (
                ("setconfig", self._current_config()),
                ("applybrightness", float(self.exposure_slider.get())),
            )
        )

    def _reset_brightness(self):
        self._call_rpc("resetbrightness")

    def _call_rpc(self, action, *args):
        if not self.script or self.rpc_busy:
            return
        self.rpc_busy = True
        self._set_controls_enabled(False)
        threading.Thread(target=self._rpc_worker, args=(action, args), daemon=True).start()

    def _call_rpc_sequence(self, steps):
        if not self.script or self.rpc_busy:
            return
        self.rpc_busy = True
        self._set_controls_enabled(False)
        threading.Thread(target=self._rpc_sequence_worker, args=(tuple(steps),), daemon=True).start()

    def _rpc_worker(self, action, args):
        try:
            with self.rpc_lock:
                export = getattr(self.script.exports_sync, action)
                result = export(*args)
            self._post("rpc_done", result)
        except Exception as exc:
            self._post("rpc_error", exc)

    def _rpc_sequence_worker(self, steps):
        try:
            result = None
            with self.rpc_lock:
                for step in steps:
                    action = step[0]
                    args = step[1:]
                    export = getattr(self.script.exports_sync, action)
                    result = export(*args)
            self._post("rpc_done", result)
        except Exception as exc:
            self._post("rpc_error", exc)

    def _poll_status(self):
        if self.closing or not self.connected or self.status_busy or self.rpc_busy:
            if not self.closing:
                self.after(1200, self._poll_status)
            return
        threading.Thread(target=self._status_worker, daemon=True).start()
        self.after(1200, self._poll_status)

    def _status_worker(self):
        self.status_busy = True
        try:
            result = self.script.exports_sync.status()
            self._post("status", result)
        except Exception as exc:
            self._post("log", "状态读取失败：" + str(exc))
            if self.connected:
                self._post("detached", "Frida RPC 状态读取失败，可能游戏已退出")
        finally:
            self.status_busy = False

    def _render_status(self, status):
        probe = (status or {}).get("probe", {})
        ok = bool(probe.get("ok"))
        self.locate_label.configure(text="已找到" if ok else "未找到", text_color=GREEN if ok else ORANGE)
        render_post = probe.get("renderPostProcessing")
        if render_post is True:
            self.post_label.configure(text="开启", text_color=GREEN)
        elif render_post is False:
            self.post_label.configure(text="关闭", text_color=ORANGE)
        else:
            self.post_label.configure(text="未知", text_color="#ddd")

        exposure = probe.get("postExposure") or {}
        value = exposure.get("value")
        if isinstance(value, (int, float)):
            self.exposure_label.configure(text=f"{value:.2f}", text_color=GREEN if ok else "#ddd")
        else:
            self.exposure_label.configure(text="-", text_color="#ddd")

        reason = probe.get("reason") or (status or {}).get("stats", {}).get("lastApplyResult") or "等待应用"
        profile = probe.get("cameraManagerVolumeProfile") or {}
        profile_ptr = profile.get("volumeProfile")
        components = profile.get("components") or {}
        component_size = components.get("size")
        if profile_ptr and profile_ptr != "0x0":
            reason = f"{reason} | CameraManager profile={profile_ptr}, components={component_size}"
        self.detail_label.configure(text=str(reason))

    def _on_close(self):
        if self.shutdown_done:
            return
        self.shutdown_done = True
        self.closing = True
        self._set_controls_enabled(False)
        threading.Thread(target=self._shutdown_worker, daemon=True).start()

    def _shutdown_worker(self):
        try:
            if self.script:
                try:
                    self.script.exports_sync.cleanup()
                except Exception:
                    pass
                try:
                    self.script.unload()
                except Exception:
                    pass
            if self.session:
                try:
                    self.session.detach()
                except Exception:
                    pass
        finally:
            self._post_allow_closing("destroy")


if __name__ == "__main__":
    app = BrightnessProbeApp()
    app.mainloop()
