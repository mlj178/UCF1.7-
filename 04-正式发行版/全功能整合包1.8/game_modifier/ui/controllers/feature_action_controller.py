import threading


class FeatureActionController:
    def __init__(self, app):
        self._app = app

    def toggle_feature(self, feature_id):
        app = self._app
        if feature_id != "esp_box" and not app._ready:
            app._log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            return

        new_state = not app._features.get(feature_id, False)

        if feature_id == "esp_box":
            switch = getattr(app, "esp_box_switch", None)
            if switch:
                switch.configure(state="disabled")

            def run_in_background():
                try:
                    feature = app._registry.get("esp_box")
                    ok = feature.enable() if new_state else feature.disable()
                    app._features[feature_id] = bool(ok and new_state)
                    app.after(0, lambda: self.on_esp_box_complete(feature_id, ok))
                except Exception as e:
                    app.after(0, lambda: self.on_esp_box_error(feature_id, str(e)))

            threading.Thread(target=run_in_background, daemon=True).start()
            return

        app._features[feature_id] = new_state
        if feature_id == "isbot":
            app._set_isbot_state("awaiting_room" if new_state else "off")

        app._feature_service.toggle_feature(
            feature_id,
            new_state,
            knife_speed=app._knife_speed,
            move_speed=app._movespeed,
            range_mult=app._range_mult,
            gravity_config={"g": app._gravity, "j": app._jump, "m": app._gravity_mode},
            timescale=app._timescale,
        )

        app._sound.play_toggle_sound()
        app._update_switch(feature_id)
        app._schedule_save_state()

    def on_esp_box_complete(self, feature_id, ok):
        app = self._app
        app._update_switch(feature_id)
        app._schedule_save_state()
        switch = getattr(app, "esp_box_switch", None)
        if switch:
            switch.configure(state="normal")
        if ok:
            app._sound.play_toggle_sound()

    def on_esp_box_error(self, feature_id, error_msg):
        app = self._app
        app._log(f"⚠ 方框透视操作失败: {error_msg}")
        app._features[feature_id] = False
        app._update_switch(feature_id)
        switch = getattr(app, "esp_box_switch", None)
        if switch:
            switch.configure(state="normal")

    def on_knife_speed_change(self, value):
        app = self._app
        app._knife_speed = round(float(value), 1)
        if app._features.get("knife"):
            app._feature_service.set_knife_speed(app._knife_speed)
        app._schedule_save_state()

    def on_move_speed_change(self, value):
        app = self._app
        app._movespeed = round(float(value), 1)
        if app._features.get("movespeed"):
            app._feature_service.set_move_speed(app._movespeed)
        app._schedule_save_state()

    def on_range_change(self, value):
        app = self._app
        app._range_mult = round(float(value), 1)
        if app._features.get("range"):
            app._feature_service.set_range(app._range_mult)
        app._schedule_save_state()

    def on_timescale_change(self, value):
        app = self._app
        app._timescale = round(float(value), 1)
        app.timescale_label.configure(text=f"{app._timescale:.1f}x")
        if app._features.get("timescale"):
            app._feature_service.set_timescale_speed(app._timescale)
        app._schedule_save_state()

    def on_gravity_change(self, value):
        app = self._app
        app._gravity = round(float(value), 1)
        app.gravity_label.configure(text=f"{app._gravity:.1f}")
        self.debounce_gravity_config()
        app._schedule_save_state()

    def on_jump_change(self, value):
        app = self._app
        app._jump = round(float(value), 1)
        app.jump_label.configure(text=f"{app._jump:.1f}")
        self.debounce_gravity_config()
        app._schedule_save_state()

    def on_gravity_mode_change(self, value):
        app = self._app
        app._gravity_mode = "player_only" if value == "仅自己" else "all"
        self.debounce_gravity_config()
        app._schedule_save_state()

    def debounce_gravity_config(self):
        app = self._app
        if app._gravity_debounce_timer:
            app.after_cancel(app._gravity_debounce_timer)
        app._gravity_debounce_timer = app.after(300, self.send_gravity_config)

    def send_gravity_config(self):
        app = self._app
        if app._features.get("gravity"):
            app._feature_service.send_gravity_config(app._gravity, app._jump, app._gravity_mode)

    def gather(self):
        app = self._app
        if not app._ready:
            app._log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            return
        if not app._features.get("gather"):
            app._log("⚠ 聚怪功能未启用，请先打开「启用追踪」开关")
            return

        app._log("📍 正在聚怪（传送所有 Bot 到佣兵出生点）...")
        app.gather_btn.configure(state="disabled", text="⏳ 聚怪中...")

        def do_gather():
            try:
                result = app._game_action_service.gather()
                if result:
                    ok = result.get("ok", False)
                    if ok:
                        bots = result.get("bots", 0)
                        fail = result.get("fail", 0)
                        app._log(f"✅ 聚怪完成! 成功{bots} 失败{fail}")
                    else:
                        app._log(f"❌ 聚怪失败: {result.get('msg', '未知错误')}")
            except Exception as e:
                app._log(f"❌ 聚怪异常: {e}")
            finally:
                app.after(0, lambda: app.gather_btn.configure(state="normal", text="📍 一键聚怪"))

        threading.Thread(target=do_gather, daemon=True).start()

    def skip_round(self):
        app = self._app
        if not app._ready:
            app._log("⚠ 尚未连接到游戏，请先点击「连接游戏」")
            return

        app._log("⏭️ 正在跳过当前回合...")
        app.skip_round_btn.configure(state="disabled", text="⏳ 跳转中...")

        def do_skip():
            try:
                result = app._game_action_service.skip_round()
                if result:
                    ok = result.get("ok", False)
                    if ok:
                        app._log("✅ 回合跳过成功！")
                    else:
                        reason = result.get("reason", "未知错误")
                        if reason == "no_instance":
                            app._log("⚠ 未能获取到游戏回合实例，请确保已进入游戏模式")
                        elif reason == "already_zero":
                            app._log("⚠ 回合时间已为 0:00，无需跳过")
                        else:
                            app._log(f"❌ 跳过失败: {reason}")
            except Exception as e:
                app._log(f"❌ 跳过异常: {e}")
            finally:
                app.after(0, lambda: app.skip_round_btn.configure(state="normal", text="▶ 跳过当前回合"))

        threading.Thread(target=do_skip, daemon=True).start()

    def restore_features(self):
        app = self._app
        for feature_id in list(app._features.keys()):
            if app._features[feature_id]:
                self.restore_single_feature(feature_id)
        for feature_id in app._features:
            app._update_switch(feature_id)

    def restore_single_feature(self, feature_id):
        app = self._app
        if feature_id in ("nano4t", "roundskip", "esp_box"):
            return
        app._feature_service.restore_feature(
            feature_id,
            knife_speed=app._knife_speed,
            move_speed=app._movespeed,
            range_mult=app._range_mult,
            gravity_config={"g": app._gravity, "j": app._jump, "m": app._gravity_mode},
            timescale=app._timescale,
        )
