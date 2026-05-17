import frida
import sys
import time

def on_message(message, data):
    if message['type'] == 'log':
        level = message.get('level', 'info')
        msg = message.get('message', '')
        
        if level == 'error':
            print(f"[错误] {msg}")
        elif level == 'success':
            print(f"[成功] {msg}")
        elif level == 'warning':
            print(f"[警告] {msg}")
        else:
            print(f"[信息] {msg}")
    elif message['type'] == 'send':
        print(f"[发送] {message}")
    else:
        print(f"[其他] {message}")

def main():
    print("=" * 60)
    print("玩家/BOT识别测试脚本")
    print("=" * 60)
    
    try:
        device = frida.get_local_device()
        print(f"[*] 本地设备: {device}")
    except Exception as e:
        print(f"[!] 获取设备失败: {e}")
        return

    processes = device.enumerate_processes()
    target = None
    for p in processes:
        if 'UnityCrossFire' in p.name:
            target = p
            break
    
    if not target:
        print("[!] 未找到 UnityCrossFire 进程")
        return
    
    print(f"[*] 找到进程: {target.name} (PID: {target.pid})")
    
    try:
        session = device.attach(target.pid)
        print(f"[*] 已附加到进程")
    except Exception as e:
        print(f"[!] 附加失败: {e}")
        return
    
    with open('check_player_bot.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
    
    try:
        script = session.create_script(js_code)
        script.on('message', on_message)
        script.load()
        print("[*] 脚本已加载")
        print("=" * 60)
        
        sys.stdin.read()
        
    except Exception as e:
        print(f"[!] 脚本执行错误: {e}")
    finally:
        session.detach()
        print("[*] 已断开连接")

if __name__ == '__main__':
    main()
