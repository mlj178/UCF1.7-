class GameConnectionService:
    def __init__(self, frida, session_manager=None):
        self._frida = frida
        if session_manager is None:
            from core.game_session_manager import GameSessionManager
            session_manager = GameSessionManager.get_instance()
        self._session_manager = session_manager

    @property
    def is_connected(self):
        return self._frida.is_connected

    @property
    def pid(self):
        return self._frida.pid

    def find_pid(self):
        return self._frida.find_pid()

    def connect(self, pid):
        self._session_manager.reconnect()
        return True, "requested"

    def disconnect(self):
        self._session_manager.disconnect()
