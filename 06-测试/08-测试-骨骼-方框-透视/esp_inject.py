#=============================================================================
# esp_inject.py - ESP DLL Injector
# 注入 m.dll 到游戏进程
# 运行: python esp_inject.py
#=============================================================================

import sys
import os
import frida
import psutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DLL_PATH = os.path.join(SCRIPT_DIR, "m", "m.dll")
LOG_PATH = os.path.join(SCRIPT_DIR, "m", "esp_log.txt")

if not os.path.isfile(DLL_PATH):
    print("[X] m.dll not found at:", DLL_PATH)
    print("[!] Run m\\build.bat first to compile the DLL.")
    sys.exit(1)

DLL_PATH_JS = DLL_PATH.replace("\\", "\\\\")

JS_CODE = f"""
var DLL_PATH = "{DLL_PATH_JS}";
console.log("[ESP] Loading DLL: " + DLL_PATH);

try {{
    Module.load(DLL_PATH);
    console.log("[ESP] DLL loaded successfully!");
    console.log("[ESP] Check esp_log.txt for debug output.");
    console.log("[ESP] Path: " + DLL_PATH.replace("m.dll", "esp_log.txt"));
}} catch (e) {{
    console.log("[ESP] FAILED to load DLL: " + e.message);
    console.log("[ESP] Error name: " + e.name);
    var errCode = e.message.match(/0x[0-9a-fA-F]+/);
    if (errCode) {{
        console.log("[ESP] Error code: " + errCode[0]);
        if (errCode[0] === "0x0000007e") {{
            console.log("[ESP] -> Missing dependency. Make sure m.dll was built with /MT (static CRT).");
        }}
    }}
}}
"""

def find_game_pid():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and 'unitycrossfire' in proc.info['name'].lower():
                return proc.info['pid']
        except Exception:
            pass
    return None

def main():
    pid = find_game_pid()
    if not pid:
        print("[X] UnityCrossFire.exe not found! Start the game first.")
        sys.exit(1)

    print(f"[*] DLL path: {DLL_PATH}")
    print(f"[*] Log path: {LOG_PATH}")
    print(f"[*] Attaching to UnityCrossFire.exe (PID={pid})...")

    try:
        session = frida.attach(pid)
    except Exception as e:
        print(f"[X] Frida attach failed: {e}")
        sys.exit(1)

    script = session.create_script(JS_CODE)
    script.on('message', lambda msg, data: print(f"[Frida] {msg}"))
    print("[*] Loading script...")
    script.load()

    print(f"\n[+] ESP injected successfully!")
    print(f"    Log: {LOG_PATH}")
    print(f"    Hotkeys:")
    print(f"      - INSERT: Open/Close menu")
    print(f"      - F1: Toggle ESP")
    print(f"      - END: Uninject")
    print(f"    Monitor log: Get-Content '{LOG_PATH}' -Wait")
    print(f"[*] Press Ctrl+C to stop.\n")

    try:
        sys.stdin.read()
    except KeyboardInterrupt:
        print("\n[*] Stopping...")
    finally:
        session.detach()
        print("[*] Detached.")

if __name__ == "__main__":
    main()
