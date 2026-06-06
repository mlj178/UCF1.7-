import sys
import os
import atexit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import features

from ui.app import App


def main():
    app = App()

    # Register cleanup handler
    def on_exit():
        """Stop workers and unload the injected DLL."""
        try:
            from core.game_session_manager import GameSessionManager

            GameSessionManager.get_instance().stop()
        except Exception:
            pass

    atexit.register(on_exit)

    app.mainloop()


if __name__ == '__main__':
    main()
