import sys
import os
import atexit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.log_manager import log_to_file
from ui.app import App


def main():
    app = App()

    # Register cleanup handler
    def on_exit():
        """Stop workers and unload the injected DLL."""
        try:
            from core.game_session_manager import GameSessionManager

            GameSessionManager.get_instance().stop()
        except Exception as exc:
            # 退出清理失败不能再往外抛（atexit 中抛异常会中断后续清理），但需留痕
            log_to_file("warning", "系统", f"退出清理失败: {exc}")

    atexit.register(on_exit)

    app.mainloop()


if __name__ == '__main__':
    main()
