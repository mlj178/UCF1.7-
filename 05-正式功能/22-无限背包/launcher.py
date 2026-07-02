import os
import sys
import time

import frida


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JS_FILE = os.path.join(BASE_DIR, "AAAAA-unlimited_bag_min.js")
GAME_PROCESS_NAME = "UnityCrossFire.exe"


def log(message):
    print("[无限背包] " + message, flush=True)


def find_game_pid(device):
    for proc in device.enumerate_processes():
        if proc.name.lower() == GAME_PROCESS_NAME.lower():
            return proc.pid
    return None


def on_message(message, data):
    if message.get("type") == "send":
        payload = message.get("payload")
        if isinstance(payload, dict) and payload.get("type") == "log":
            level = payload.get("level", "info")
            module = payload.get("module", "")
            text = payload.get("message", "")
            log("[" + level + "][" + module + "] " + text)
        else:
            log("[JS] " + str(payload))
    elif message.get("type") == "error":
        log("[JS错误] " + message.get("description", str(message)))


def main():
    if not os.path.exists(JS_FILE):
        log("JS 文件不存在: " + JS_FILE)
        return 1

    log("等待游戏进程: " + GAME_PROCESS_NAME)
    device = frida.get_local_device()
    pid = None

    while pid is None:
        pid = find_game_pid(device)
        if pid is None:
            time.sleep(1.0)

    log("找到游戏 PID: " + str(pid))
    session = None
    script = None

    try:
        session = device.attach(pid)
        log("Frida 已附加")

        with open(JS_FILE, "r", encoding="utf-8") as f:
            js_code = f.read()

        script = session.create_script(js_code)
        script.on("message", on_message)
        script.load()

        result = script.exports_sync.enable()
        log("enable() 返回: " + str(result))
        log("保持运行中，按 Ctrl+C 退出")

        while True:
            time.sleep(1.0)

    except KeyboardInterrupt:
        log("收到退出请求")
    except frida.ProcessNotFoundError:
        log("游戏进程已退出")
        return 2
    except Exception as exc:
        log("异常: " + str(exc))
        return 3
    finally:
        if script is not None:
            try:
                script.exports_sync.cleanup()
            except Exception:
                pass
            try:
                script.unload()
            except Exception:
                pass

        if session is not None:
            try:
                session.detach()
            except Exception:
                pass

        log("已清理")

    return 0


if __name__ == "__main__":
    sys.exit(main())
