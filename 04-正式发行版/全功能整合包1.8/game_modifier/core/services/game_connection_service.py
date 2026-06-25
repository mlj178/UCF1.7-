class GameConnectionService:
    def __init__(self, frida):
        self._frida = frida

    @property
    def is_connected(self):
        return self._frida.is_connected

    @property
    def pid(self):
        return self._frida.pid

    def find_pid(self):
        return self._frida.find_pid()

    def connect(self, pid):
        return self._frida.connect(pid)

    def disconnect(self):
        return self._frida.disconnect()
