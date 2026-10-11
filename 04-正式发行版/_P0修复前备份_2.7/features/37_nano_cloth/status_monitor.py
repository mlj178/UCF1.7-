import queue
import threading


class NanoClothStatusMonitor:
    """Poll nano_cloth runtime status and render current cloth count.

    模式来源：features/10_roundskip/monitor.py（RoundSkipMonitor）。

    线程模型（关键修复）：
      - 所有 UI 操作（渲染标签）和 after 排程都在主线程执行；
      - 后台线程只做 status RPC，结果放入线程安全队列；
      - 主线程轮询循环每次先取队列渲染，再排程下一次。

    原因：真实 App 的 _safe_after 在非主线程调用 self.after() 时会抛
    RuntimeError "main thread is not in main loop"，被捕获后塞进只冲刷
    一次的 pending 队列，导致渲染回调永不执行、轮询循环中断。
    """

    def __init__(self, context, feature_id, interval_ms=1000):
        self._context = context
        self._feature_id = feature_id
        self._interval_ms = interval_ms
        self._timer = None
        self._running = False
        self._polling = False
        self._result_queue = queue.Queue()
        self._diag_logged = False
        self._diag_queue_empty_logged = False

    # ---- 调试探针（仅打印，不改渲染逻辑）----
    # 真实 App 在游戏房间内运行时，这些日志标题为 "[nano_cloth/probe]"，
    # 用于判定"当前防化服 --"断点到底在哪一段：
    #   a) monitor.start() 是否被调用、此时 renderer 是否已注册
    #   b) status RPC 是否返回、是否 dict
    #   c) 首条回执里 current_cloth_count / player_cached 的真实值
    def _log_diag(self, message):
        try:
            self._context.log("[nano_cloth/probe] " + message)
        except Exception:
            pass

    def start(self):
        if self._running:
            return
        self._running = True
        self._log_diag(
            "monitor.start() 已调用 (game_connected)，renderer=%s"
            % ("registered" if _renderer is not None else "NONE")
        )
        # 主线程启动第一条轮询
        self._schedule_poll(0)

    def stop(self):
        self._running = False
        if self._timer is not None:
            self._timer = None

    def _schedule_poll(self, delay_ms):
        if not self._running:
            return
        # 仅在主线程调用（start 在 game_connected 主线程回调里，
        # 后续排程也在主线程的 _poll_once 里）。
        self._timer = self._context.after(delay_ms, self._poll_once)

    def _poll_once(self):
        self._timer = None
        if not self._running:
            return

        # 主线程：先渲染队列里后台线程放好的结果
        rendered_any = False
        while True:
            try:
                result = self._result_queue.get_nowait()
            except queue.Empty:
                break
            rendered_any = True
            try:
                self._render_and_diag(result)
            except Exception:
                pass

        if not rendered_any and not self._diag_queue_empty_logged:
            self._diag_queue_empty_logged = True
            self._log_diag("首轮队列为空：status RPC 未回传结果（异常/未注入）")

        if not self._should_poll():
            self.stop()
            return

        if not self._polling:
            self._polling = True
            threading.Thread(target=self._poll_status, daemon=True).start()

        # 主线程排程下一次
        self._schedule_poll(self._interval_ms)

    def _render_and_diag(self, result):
        if isinstance(result, dict) and not self._diag_logged:
            self._diag_logged = True
            self._log_diag(
                "首条 status 回执: player_cached=%r current=%r last_known=%r "
                "connected=%r renderer=%s"
                % (
                    result.get("player_cached"),
                    result.get("current_cloth_count"),
                    result.get("last_known_cloth_count"),
                    self._context.is_connected(),
                    "registered" if _renderer is not None else "NONE",
                )
            )
        _render(result)

    def _poll_status(self):
        # 后台线程：只做 RPC，结果放队列，绝不碰 UI / after
        try:
            result = self._context.feature_service.status(self._feature_id)
            if result is None:
                self._log_diag("status RPC 返回 None（feature_service.status / plugin_call 无结果）")
            elif not isinstance(result, dict):
                self._log_diag("status RPC 返回非 dict: %r" % (result,))
            self._result_queue.put(result)
        except Exception as exc:
            self._log_diag("status RPC 异常: %r" % (exc,))
        finally:
            self._polling = False

    def _should_poll(self):
        return bool(self._running and self._context.is_connected())


_monitor = None
_renderer = None


def set_renderer(renderer):
    """panel.py 在构建卡片时注册标签刷新函数（在主线程调用）。"""
    global _renderer
    _renderer = renderer


def _render(result):
    if _renderer is None:
        return
    try:
        _renderer(result)
    except Exception:
        pass


def get_monitor(context):
    """events.py 生命周期钩子获取/创建监视器单例。"""
    global _monitor
    if _monitor is None:
        _monitor = NanoClothStatusMonitor(context, context.feature_id)
    return _monitor
