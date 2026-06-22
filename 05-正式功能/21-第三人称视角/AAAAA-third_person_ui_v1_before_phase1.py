# 第三人称视角修改器 v4 — Python UI 启动器
# 修复：日志重复写入、状态同步、Frida 断线重连、按钮并发、完整恢复
# 依赖: pip install customtkinter frida-tools psutil

import customtkinter as ctk
import frida
import threading
import time
from datetime import datetime
import psutil
import os
import sys
import logging

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AAAAA-third_person_v1.js")
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")


# ============================================================
# 文件日志管理器 (独立，不与 UI 日志耦合)
# ============================================================
class FileLogger:
    def __init__(self, log_dir):
        os.makedirs(log_dir, exist_ok=True)
        date_str = datetime.now().strftime("%Y%m%d")
        self.log_path = os.path.join(log_dir, f"third_person_{date_str}.txt")

        self.logger = logging.getLogger("third_person_v4")
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers.clear()

        fh = logging.FileHandler(self.log_path, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%H:%M:%S')
        fh.setFormatter(fmt)
        self.logger.addHandler(fh)

        self.logger.info("=" * 60)
        self.logger.info("第三人称视角修改器 v4 日志")
        self.logger.info(f"JS 脚本: {SCRIPT_PATH}")
        self.logger.info("=" * 60)

    def info(self, msg): self.logger.info(msg)
    def warn(self, msg): self.logger.warning(msg)
    def error(self, msg): self.logger.error(msg)
    def debug(self, msg): self.logger.debug(msg)


file_log = FileLogger(LOG_DIR)


class ThirdPersonApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("第三人称视角修改器 v4")
        self.geometry("480x580+200+100")
        self.resizable(False, False)

        # 连接状态
        self.session = None
        self.script = None
        self.is_connected = False
        self.is_enabled = False
        self.attached_pid = None
        self._stop = False
        self._aim_diag_lines = []  # 瞄准诊断日志缓冲

        # 操作并发控制
        self.operation_in_progress = False

        # 参数
        self.camera_distance = 3.0
        self.camera_sensitivity = 1.0

        # UI 日志行数限制
        self._log_lines = 0
        self._max_log_lines = 500

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._build_ui()

        # 后台线程：连接 + 状态同步
        threading.Thread(target=self._connect_loop, daemon=True).start()
        threading.Thread(target=self._status_sync_loop, daemon=True).start()

    def _build_ui(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=15, padx=15, fill="both", expand=True)

        # === 标题 + 状态 ===
        self.title_label = ctk.CTkLabel(
            self.main_frame, text="第三人称视角修改器",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.title_label.pack(pady=8)

        self.status_label = ctk.CTkLabel(
            self.main_frame, text="等待游戏启动...",
            font=ctk.CTkFont(size=13)
        )
        self.status_label.pack(pady=2)

        # === 开关 ===
        self.toggle_frame = ctk.CTkFrame(self.main_frame)
        self.toggle_frame.pack(pady=8, padx=15, fill="x")

        self.toggle_btn = ctk.CTkButton(
            self.toggle_frame, text="开启第三人称",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45, fg_color="#28a745", hover_color="#218838",
            command=self._toggle
        )
        self.toggle_btn.pack(pady=8, padx=10, fill="x")

        self.toggle_status = ctk.CTkLabel(
            self.toggle_frame, text="当前: 第一人称",
            font=ctk.CTkFont(size=13)
        )
        self.toggle_status.pack(pady=2)

        # === 相机距离 ===
        self.distance_frame = ctk.CTkFrame(self.main_frame)
        self.distance_frame.pack(pady=6, padx=15, fill="x")

        ctk.CTkLabel(self.distance_frame, text="相机距离",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=4)

        self.distance_slider = ctk.CTkSlider(
            self.distance_frame, from_=1.0, to=8.0,
            number_of_steps=28,
            command=self._on_distance_change
        )
        self.distance_slider.set(3.0)
        self.distance_slider.pack(pady=2, padx=10, fill="x")

        self.distance_label = ctk.CTkLabel(
            self.distance_frame, text="3.0",
            font=ctk.CTkFont(size=12)
        )
        self.distance_label.pack(pady=2)

        # === 灵敏度 (暂未生效，标注) ===
        self.sens_frame = ctk.CTkFrame(self.main_frame)
        self.sens_frame.pack(pady=6, padx=15, fill="x")

        ctk.CTkLabel(self.sens_frame, text="鼠标灵敏度 (暂未生效)",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=4)

        self.sens_slider = ctk.CTkSlider(
            self.sens_frame, from_=0.2, to=3.0,
            number_of_steps=28,
            command=self._on_sens_change
        )
        self.sens_slider.set(1.0)
        self.sens_slider.pack(pady=2, padx=10, fill="x")

        self.sens_label = ctk.CTkLabel(
            self.sens_frame, text="1.0x",
            font=ctk.CTkFont(size=12)
        )
        self.sens_label.pack(pady=2)

        # === 诊断按钮 ===
        self.diag_frame = ctk.CTkFrame(self.main_frame)
        self.diag_frame.pack(pady=4, padx=15, fill="x")

        self.diag_btn = ctk.CTkButton(
            self.diag_frame, text="模型诊断",
            font=ctk.CTkFont(size=13), height=32,
            fg_color="#6c757d", hover_color="#5a6268",
            command=self._run_diagnostic
        )
        self.diag_btn.pack(pady=4, padx=10, fill="x")

        # === 瞄准诊断按钮 ===
        self.aim_diag_frame = ctk.CTkFrame(self.main_frame)
        self.aim_diag_frame.pack(pady=4, padx=15, fill="x")

        aim_btn_row = ctk.CTkFrame(self.aim_diag_frame, fg_color="transparent")
        aim_btn_row.pack(pady=4, padx=5, fill="x")

        self.aim_start_btn = ctk.CTkButton(
            aim_btn_row, text="开始瞄准诊断",
            font=ctk.CTkFont(size=13), height=32, width=160,
            fg_color="#17a2b8", hover_color="#138496",
            command=self._start_aim_diagnostic
        )
        self.aim_start_btn.pack(side="left", padx=5, expand=True, fill="x")

        self.aim_stop_btn = ctk.CTkButton(
            aim_btn_row, text="停止瞄准诊断",
            font=ctk.CTkFont(size=13), height=32, width=160,
            fg_color="#fd7e14", hover_color="#e06b0a",
            command=self._stop_aim_diagnostic,
            state="disabled"
        )
        self.aim_stop_btn.pack(side="left", padx=5, expand=True, fill="x")

        self.aim_diag_label = ctk.CTkLabel(
            self.aim_diag_frame, text="采集15秒 | 射击时自动记录",
            font=ctk.CTkFont(size=11), text_color="gray"
        )
        self.aim_diag_label.pack(pady=2)

        # v9: 瞄准诊断状态显示
        self.aim_diag_status = ctk.CTkLabel(
            self.aim_diag_frame, text="",
            font=ctk.CTkFont(size=10), text_color="#aaaaaa",
            wraplength=380, justify="left"
        )
        self.aim_diag_status.pack(pady=1, padx=5)

        # 测试步骤提示
        aim_test_tip = ctk.CTkLabel(
            self.aim_diag_frame,
            text="测试步骤: A.空旷转视角 B.2m墙单发3次 C.10m墙单发3次 D.30m墙单发3次 E.贴墙单发3次 F.待机/开火/换弹快照 G.换枪后射击",
            font=ctk.CTkFont(size=10), text_color="#888888",
            wraplength=380, justify="left"
        )
        aim_test_tip.pack(pady=1, padx=5)

        # === 日志 ===
        self.log_frame = ctk.CTkFrame(self.main_frame)
        self.log_frame.pack(pady=6, padx=15, fill="both", expand=True)

        log_header = ctk.CTkFrame(self.log_frame, fg_color="transparent")
        log_header.pack(fill="x", padx=5)

        ctk.CTkLabel(log_header, text="日志",
                     font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")

        self.log_path_label = ctk.CTkLabel(
            log_header, text=f"日志: {file_log.log_path}",
            font=ctk.CTkFont(size=10), text_color="gray"
        )
        self.log_path_label.pack(side="right")

        self.log_text = ctk.CTkTextbox(
            self.log_frame, height=80, font=ctk.CTkFont(size=11)
        )
        self.log_text.pack(pady=2, padx=5, fill="both", expand=True)

    # ============================================================
    # 线程安全 UI 更新
    # ============================================================
    def _log_ui(self, msg):
        """UI 日志 (仅主线程调用) — 不再写文件日志"""
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] {msg}"
        self.log_text.insert("end", line + "\n")
        self.log_text.see("end")
        self._log_lines += 1

        # 超过 500 行时删除旧日志
        if self._log_lines > self._max_log_lines:
            self.log_text.delete("1.0", "100.end")
            self._log_lines -= 100

    def _safe_log(self, msg):
        """线程安全的 UI 日志"""
        self.after(0, lambda: self._log_ui(msg))

    def _safe_config(self, widget, **kw):
        """线程安全的控件配置"""
        self.after(0, lambda: widget.configure(**kw))

    # ============================================================
    # 带超时的 RPC 调用 (防止卡死)
    # ============================================================
    def _rpc_call(self, func_name, *args, timeout=5.0):
        """带超时的 RPC 调用，防止 Frida 阻塞导致程序卡死"""
        if not self.script:
            return None

        result = [None]
        exception = [None]
        completed = [False]

        def call():
            try:
                func = getattr(self.script.exports_sync, func_name)
                result[0] = func(*args)
                completed[0] = True
            except frida.InvalidOperationError as e:
                exception[0] = e
                # 会话已失效，需要清理
                self.after(0, self._cleanup_session)
            except frida.TransportError as e:
                exception[0] = e
            except Exception as e:
                exception[0] = e

        thread = threading.Thread(target=call, daemon=True)
        thread.start()
        thread.join(timeout=timeout)

        if thread.is_alive():
            # 超时，线程仍在运行
            file_log.error(f"RPC 调用超时: {func_name}({args})")
            # v10: 超时后标记会话可能失效
            self.after(0, lambda: self._safe_log(f"RPC 调用超时: {func_name}"))
            return None

        if exception[0]:
            # 有异常
            if isinstance(exception[0], frida.InvalidOperationError):
                file_log.error(f"RPC 调用失败 (InvalidOperation): {func_name}")
                self.after(0, self._cleanup_session)
            elif isinstance(exception[0], frida.TransportError):
                file_log.error(f"RPC 调用失败 (Transport): {exception[0]}")
            else:
                file_log.error(f"RPC 调用失败: {exception[0]}")
            return None

        return result[0]

    # ============================================================
    # 进程查找
    # ============================================================
    def _find_pid(self):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                name = (proc.info['name'] or '').lower()
                if 'unitycrossfire' in name:
                    return proc.info['pid']
            except Exception:
                pass
        return None

    # ============================================================
    # 连接循环 (后台线程)
    # ============================================================
    def _connect_loop(self):
        while not self._stop:
            if self.is_connected:
                time.sleep(5)
                continue

            pid = self._find_pid()
            if not pid:
                self._safe_config(self.status_label, text="等待游戏启动...")
                time.sleep(3)
                continue

            # 防止同一 PID 重复 attach
            if self.attached_pid == pid and self.session:
                time.sleep(5)
                continue

            self._safe_config(self.status_label, text=f"连接中 PID={pid}...")
            file_log.info(f"尝试连接 PID={pid}")

            try:
                self._cleanup_session()

                self.session = frida.attach(pid)
                self.attached_pid = pid
                file_log.info(f"Frida 已附加到 PID={pid}")

                # 注册断线回调
                self.session.on('detached', self._on_detached)

                if not os.path.exists(SCRIPT_PATH):
                    file_log.error(f"JS 文件不存在: {SCRIPT_PATH}")
                    self._safe_log(f"JS 文件不存在: {SCRIPT_PATH}")
                    self._cleanup_session()
                    time.sleep(10)
                    continue

                with open(SCRIPT_PATH, 'r', encoding='utf-8') as f:
                    js_code = f.read()

                file_log.info(f"JS 脚本大小: {len(js_code)} 字节")

                self.script = self.session.create_script(js_code)
                self.script.on('message', self._on_message)
                self.script.load()

                file_log.info("JS 脚本已加载，调用 installhook...")

                result = self._rpc_call('installhook', timeout=10.0)
                if result is None:
                    file_log.error("installhook 超时")
                    self._safe_log("Hook 安装超时")
                    self._cleanup_session()
                    time.sleep(5)
                    continue

                file_log.info(f"installhook 返回: {result}")

                if result.get('ok'):
                    self.is_connected = True
                    self._safe_config(self.status_label, text="已连接")
                    self._safe_log("连接成功，Hook 已安装")
                else:
                    file_log.error(f"Hook 安装失败: {result}")
                    self._safe_log("Hook 安装失败")
                    # JS 加载失败时主动清理
                    self._cleanup_session()

            except frida.ProcessNotFoundError:
                self._safe_config(self.status_label, text="进程未找到")
                file_log.error(f"进程 PID={pid} 未找到")
            except frida.PermissionDeniedError:
                self._safe_config(self.status_label, text="权限不足，请以管理员运行")
                file_log.error("Frida 附加权限不足")
            except frida.TransportError as e:
                self._safe_config(self.status_label, text="连接断开")
                file_log.error(f"Transport 错误: {e}")
                self._cleanup_session()
            except Exception as e:
                self._safe_config(self.status_label, text="连接失败")
                file_log.error(f"连接错误: {e}")
                self._cleanup_session()

            time.sleep(5)

    def _on_detached(self, reason, crash):
        """Frida 断线回调"""
        file_log.error(f"Frida 断开: reason={reason}, crash={crash}")
        self.is_connected = False
        self.is_enabled = False
        self.attached_pid = None
        self.session = None
        self.script = None

        self.after(0, self._update_ui_disconnected)

    def _update_ui_disconnected(self):
        """断线后更新 UI (主线程)"""
        self.status_label.configure(text="连接已断开")
        self.toggle_btn.configure(text="开启第三人称", fg_color="#28a745", hover_color="#218838")
        self.toggle_status.configure(text="当前: 第一人称")
        self._log_ui("连接已断开，等待重新连接...")

    def _cleanup_session(self):
        """清理 Frida 会话"""
        try:
            if self.script:
                self.script.unload()
        except Exception:
            pass
        try:
            if self.session:
                self.session.detach()
        except Exception:
            pass
        self.script = None
        self.session = None
        self.is_connected = False
        self.is_enabled = False
        self.attached_pid = None

    # ============================================================
    # 状态同步循环 (后台线程，每 2 秒查询一次)
    # ============================================================
    def _status_sync_loop(self):
        while not self._stop:
            if self.is_connected and self.script:
                try:
                    status = self._rpc_call('getstatus', timeout=3.0)
                    if status is None:
                        # 超时，但不立即断开，可能是临时阻塞
                        continue
                    self.after(0, lambda s=status: self._sync_ui_from_status(s))
                except frida.InvalidOperationError:
                    file_log.error("状态同步: 脚本已断开")
                    self._cleanup_session()
                    self.after(0, self._update_ui_disconnected)
                except frida.TransportError as e:
                    file_log.error(f"状态同步 Transport 错误: {e}")
                    self._cleanup_session()
                    self.after(0, self._update_ui_disconnected)
                except Exception as e:
                    # 静默忽略偶尔的同步失败
                    pass
            time.sleep(2)  # v10: 1秒 -> 2秒，减少同步频率

    def _sync_ui_from_status(self, status):
        """根据 JS 状态同步 UI (主线程)"""
        js_enabled = status.get('enabled', False)
        js_state = status.get('state', '')

        # 同步启用状态
        if self.is_enabled != js_enabled:
            self.is_enabled = js_enabled
            if js_enabled:
                self.toggle_btn.configure(text="关闭第三人称", fg_color="#dc3545", hover_color="#c82333")
                self.toggle_status.configure(text="当前: 第三人称")
            else:
                self.toggle_btn.configure(text="开启第三人称", fg_color="#28a745", hover_color="#218838")
                self.toggle_status.configure(text="当前: 第一人称")

        # 更新状态标签
        if self.is_connected:
            state_text = {
                'NO_GAME': '未检测到游戏',
                'WAITING_ROOM': '等待进入房间',
                'ROOM_READY': '房间就绪',
                'TP_ENABLED': '第三人称已启用',
                'DISCONNECTED': '已断开',
            }.get(js_state, js_state)
            self.status_label.configure(text=f"已连接 | {state_text}")

        # 显示最后错误
        last_err = status.get('lastError', '')
        if last_err:
            self._log_ui(f"[JS错误] {last_err}")

    # ============================================================
    # Frida 消息处理 (修复：不再重复写文件日志)
    # ============================================================
    def _on_message(self, message, data):
        if message['type'] == 'send':
            payload = message['payload']

            if isinstance(payload, dict) and payload.get('type') == 'log':
                level = payload.get('level', 'info')
                module = payload.get('module', '')
                msg = payload.get('message', '')
                full_msg = f"[{module}] {msg}" if module else msg

                # 只写文件日志一次
                if level == 'error':
                    file_log.error(full_msg)
                elif level == 'warn':
                    file_log.warn(full_msg)
                else:
                    file_log.info(full_msg)

                # UI 日志通过主线程更新 (不重复写文件)
                self._safe_log(full_msg)

            elif isinstance(payload, dict) and payload.get('type') == 'state_changed':
                # 状态变化事件，只写文件日志，不刷 UI 日志
                old_state = payload.get('oldState', '')
                new_state = payload.get('newState', '')
                file_log.info(f"状态变化: {old_state} -> {new_state}")

            elif isinstance(payload, dict) and payload.get('type') == 'aim_diag':
                # 瞄准诊断日志行
                line = payload.get('line', '')
                if line:
                    self._aim_diag_lines.append(line)
                    # 写入文件日志
                    file_log.debug(f"[AimDiag] {line}")
                    # v9: 检测射击事件更新状态
                    if 'SHOT' in line and 'BEGIN' in line:
                        try:
                            # 尝试获取当前诊断状态
                            if self.script:
                                status = self._rpc_call('getaimdiagstatus', timeout=2.0)
                                if status:
                                    sid = status.get('sessionId', '?')
                                    shots = status.get('shotId', 0)
                                    self._safe_config(self.aim_diag_status,
                                        text=f"sessionId={sid} | 射击={shots}次 | 采集中...")
                        except Exception:
                            pass

            elif isinstance(payload, dict) and payload.get('type') == 'aim_diag_complete':
                # 瞄准诊断完成
                session_id = payload.get('sessionId', 'unknown')
                shot_count = payload.get('shotCount', 0)
                lines = list(self._aim_diag_lines)
                self._aim_diag_lines.clear()
                self._write_aim_diag_file(session_id, lines, shot_count)

            else:
                # 简单字符串消息
                msg_str = str(payload)
                file_log.info(f"[JS] {msg_str}")
                self._safe_log(f"[JS] {msg_str}")

        elif message.get('type') == 'error':
            desc = message.get('description', '未知错误')
            stack = message.get('stack', '')
            file_log.error(f"Frida 错误: {desc}\n{stack[:500]}")
            self._safe_log(f"Frida 错误: {desc[:200]}")

    # ============================================================
    # 开关切换 (后台线程 + 并发控制)
    # ============================================================
    def _toggle(self):
        if not self.is_connected:
            self._log_ui("未连接，请先启动游戏")
            return

        if self.operation_in_progress:
            self._log_ui("操作进行中，请稍候...")
            return

        # 禁用按钮防止并发
        self.toggle_btn.configure(state="disabled")
        self.operation_in_progress = True

        threading.Thread(target=self._toggle_bg, daemon=True).start()

    def _toggle_bg(self):
        try:
            if self.is_enabled:
                result = self._rpc_call('disable', timeout=8.0)
                if result is None:
                    self._safe_log("关闭操作超时")
                    return
                if result.get('ok'):
                    self.is_enabled = False
                    self.after(0, lambda: self.toggle_btn.configure(
                        text="开启第三人称", fg_color="#28a745", hover_color="#218838"))
                    self.after(0, lambda: self.toggle_status.configure(text="当前: 第一人称"))
                    self._safe_log("已切换回第一人称")
                else:
                    self._safe_log(f"关闭失败: {result.get('error', '未知')}")
            else:
                result = self._rpc_call('enable', timeout=8.0)
                if result is None:
                    self._safe_log("开启操作超时")
                    return
                if result.get('ok') and result.get('enabled'):
                    self.is_enabled = True
                    self.after(0, lambda: self.toggle_btn.configure(
                        text="关闭第三人称", fg_color="#dc3545", hover_color="#c82333"))
                    self.after(0, lambda: self.toggle_status.configure(text="当前: 第三人称"))
                    self._safe_log("已切换到第三人称")
                else:
                    err = result.get('error', '未知错误')
                    self.is_enabled = False
                    self._safe_log(f"切换失败: {err}")
                    file_log.warn(f"enable() 失败: {result}")
        except frida.InvalidOperationError:
            self._safe_log("脚本已断开，请等待重新连接")
            self._cleanup_session()
            self.after(0, self._update_ui_disconnected)
        except frida.TransportError as e:
            self._safe_log(f"通信错误: {e}")
            self._cleanup_session()
            self.after(0, self._update_ui_disconnected)
        except Exception as e:
            self._safe_log(f"操作失败: {e}")
            file_log.error(f"操作失败: {e}")
            # 重新查询真实状态
            try:
                status = self._rpc_call('getstatus', timeout=3.0)
                if status:
                    self.after(0, lambda s=status: self._sync_ui_from_status(s))
            except Exception:
                pass
        finally:
            self.operation_in_progress = False
            self.after(0, lambda: self.toggle_btn.configure(state="normal"))

    # ============================================================
    # 模型诊断 (后台线程)
    # ============================================================
    def _run_diagnostic(self):
        if not self.is_connected or not self.script:
            self._log_ui("未连接，无法运行诊断")
            return
        self.diag_btn.configure(state="disabled", text="诊断中...")
        threading.Thread(target=self._diagnostic_bg, daemon=True).start()

    def _diagnostic_bg(self):
        try:
            result = self._rpc_call('debugmodel', timeout=10.0)
            if result is None:
                self._safe_log("诊断操作超时")
                return
            if result.get('ok'):
                r = result.get('result', {})
                self._safe_log("=== 模型诊断结果 ===")
                self._safe_log(f"Player: {r.get('player', 'null')}")
                self._safe_log(f"Character: {r.get('character', 'null')}")
                self._safe_log(f"PlayerData: {r.get('playerData', 'null')}")
                self._safe_log(f"observeMode: {r.get('observeMode', '?')}")
                self._safe_log(f"playerViewModelVisible: {r.get('playerViewModelVisible', '?')}")
                self._safe_log(f"PlayerCameraManager: {r.get('playerCameraManager', 'null')}")
                self._safe_log(f"PV 对象数: {r.get('pvCount', 0)} | CV 对象数: {r.get('cvCount', 0)}")

                # PV 对象详情
                pv_items = r.get('pvItems', [])
                for i, item in enumerate(pv_items[:10]):
                    self._safe_log(f"  PV[{i}] {item.get('name','?')} active={item.get('active','?')} layer={item.get('layer','?')}")

                # CV 对象详情
                cv_items = r.get('cvItems', [])
                for i, item in enumerate(cv_items[:10]):
                    self._safe_log(f"  CV[{i}] {item.get('name','?')} active={item.get('active','?')} layer={item.get('layer','?')}")

                # 武器
                self._safe_log(f"当前武器: {r.get('weapon', 'null')}")

                # Sockets
                sockets = r.get('sockets', [])
                for s in sockets[:10]:
                    self._safe_log(f"  Socket: {s.get('name','?')} node={s.get('node','?')}")

                # FreeLook Rigs
                rigs = r.get('freeLookRigs', [])
                for rig in rigs:
                    comps = rig.get('components', [])
                    for c in comps:
                        ctype = c.get('type', 'Unknown')
                        if ctype == 'Composer':
                            self._safe_log(f"  Rig{rig.get('index','?')} Composer: SX={c.get('screenX','?'):.2f} SY={c.get('screenY','?'):.2f} "
                                         f"Offset={c.get('trackedOffset','?')} DZ={c.get('deadZone','?')}")
                        elif ctype == 'Transposer':
                            self._safe_log(f"  Rig{rig.get('index','?')} Transposer: FollowOffset={c.get('followOffset','?')}")

                self._safe_log("=== 诊断完成 ===")
                file_log.info(f"模型诊断完成: PV={r.get('pvCount',0)} CV={r.get('cvCount',0)} weapon={r.get('weapon','null')}")
            else:
                err = result.get('error', '未知错误')
                self._safe_log(f"诊断失败: {err}")
                file_log.error(f"模型诊断失败: {err}")
        except frida.InvalidOperationError:
            self._safe_log("脚本已断开，无法诊断")
            self._cleanup_session()
            self.after(0, self._update_ui_disconnected)
        except frida.TransportError as e:
            self._safe_log(f"诊断通信错误: {e}")
        except Exception as e:
            self._safe_log(f"诊断异常: {e}")
            file_log.error(f"诊断异常: {e}")
        finally:
            self.after(0, lambda: self.diag_btn.configure(state="normal", text="模型诊断"))

    # ============================================================
    # 瞄准诊断
    # ============================================================
    def _start_aim_diagnostic(self):
        if not self.is_connected or not self.script:
            self._log_ui("未连接，无法启动瞄准诊断")
            return
        self.aim_start_btn.configure(state="disabled")
        threading.Thread(target=self._start_aim_diag_bg, daemon=True).start()

    def _start_aim_diag_bg(self):
        try:
            result = self._rpc_call('startaimdiagnostic', 15, timeout=5.0)
            if result is None:
                self._safe_log("启动瞄准诊断超时")
                self._safe_config(self.aim_start_btn, state="normal")
                return
            if result.get('ok'):
                sid = result.get('sessionId', '?')
                dur = result.get('duration', 15)
                self._safe_log(f"瞄准诊断已启动: {sid} ({dur}s)")
                self._safe_config(self.aim_start_btn, state="disabled")
                self._safe_config(self.aim_stop_btn, state="normal")
                self._safe_config(self.aim_diag_label, text=f"诊断中... {sid}")
                self._safe_config(self.aim_diag_status, text=f"sessionId={sid} | 等待射击数据...")
                file_log.info(f"瞄准诊断启动: sessionId={sid} duration={dur}s")
            else:
                err = result.get('error', '未知错误')
                self._safe_log(f"启动失败: {err}")
                self._safe_config(self.aim_start_btn, state="normal")
                self._safe_config(self.aim_diag_status, text=f"启动失败: {err}")
        except frida.InvalidOperationError:
            self._safe_log("脚本已断开")
            self._cleanup_session()
            self.after(0, self._update_ui_disconnected)
        except Exception as e:
            self._safe_log(f"启动异常: {e}")
            self._safe_config(self.aim_start_btn, state="normal")

    def _stop_aim_diagnostic(self):
        if not self.is_connected or not self.script:
            self._log_ui("未连接")
            return
        self.aim_stop_btn.configure(state="disabled")
        threading.Thread(target=self._stop_aim_diag_bg, daemon=True).start()

    def _stop_aim_diag_bg(self):
        try:
            result = self._rpc_call('stopaimdiagnostic', timeout=5.0)
            if result is None:
                self._safe_log("停止瞄准诊断超时")
                return
            if result.get('ok'):
                shots = result.get('shotCount', 0)
                lines = result.get('lineCount', 0)
                self._safe_log(f"瞄准诊断已停止: {shots}次射击, {lines}行日志")
                file_log.info(f"瞄准诊断停止: shots={shots} lines={lines}")
            else:
                err = result.get('error', '未知')
                self._safe_log(f"停止失败: {err}")
        except frida.InvalidOperationError:
            self._safe_log("脚本已断开")
            self._cleanup_session()
            self.after(0, self._update_ui_disconnected)
        except Exception as e:
            self._safe_log(f"停止异常: {e}")
        finally:
            self._safe_config(self.aim_start_btn, state="normal")
            self._safe_config(self.aim_stop_btn, state="disabled")
            self._safe_config(self.aim_diag_label, text="采集15秒 | 射击时自动记录")
            self._safe_config(self.aim_diag_status, text="")

    def _write_aim_diag_file(self, session_id, lines, shot_count):
        """将瞄准诊断日志写入独立文件"""
        try:
            os.makedirs(LOG_DIR, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"aim_diagnostic_{ts}_{session_id}.txt"
            filepath = os.path.join(LOG_DIR, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"UCF1.7 瞄准诊断日志\n")
                f.write(f"sessionId: {session_id}\n")
                f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"射击次数: {shot_count}\n")
                f.write(f"日志行数: {len(lines)}\n")
                f.write("=" * 60 + "\n\n")
                for line in lines:
                    f.write(line + "\n")

            self._safe_log(f"诊断日志已保存: {filename}")
            self._safe_config(self.aim_diag_label, text=f"已保存: {filename}")
            self._safe_config(self.aim_diag_status, text=f"射击={shot_count}次 | 日志={len(lines)}行 | {filename}")
            file_log.info(f"瞄准诊断日志已保存: {filepath} ({len(lines)} 行, {shot_count} 次射击)")
        except Exception as e:
            self._safe_log(f"保存诊断日志失败: {e}")
            file_log.error(f"保存瞄准诊断日志失败: {e}")

    # ============================================================
    # 滑块回调
    # ============================================================
    def _on_distance_change(self, value):
        self.camera_distance = round(value, 1)
        self.distance_label.configure(text=str(self.camera_distance))
        if self.is_connected and self.is_enabled:
            try:
                self.script.exports_sync.setdistance(self.camera_distance)
            except Exception:
                pass

    def _on_sens_change(self, value):
        self.camera_sensitivity = round(value, 1)
        self.sens_label.configure(text=f"{self.camera_sensitivity}x")
        if self.is_connected:
            try:
                self.script.exports_sync.setsensitivity(self.camera_sensitivity)
            except Exception:
                pass

    # ============================================================
    # 关闭 (完整清理)
    # ============================================================
    def _on_close(self):
        self._stop = True
        file_log.info("修改器关闭")

        # 先关闭第三人称
        if self.is_enabled and self.script:
            try:
                self.script.exports_sync.disable()
                file_log.info("关闭时已恢复游戏状态")
            except Exception as e:
                file_log.error(f"关闭时恢复失败: {e}")

        # 清理 Frida
        self._cleanup_session()
        self.destroy()


if __name__ == "__main__":
    app = ThirdPersonApp()
    app.mainloop()
