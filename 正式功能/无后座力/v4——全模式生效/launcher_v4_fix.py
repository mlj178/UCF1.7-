import frida
import sys
import os
import time
import threading

# 1. 读取嵌入的 JS 脚本（和 launcher.py 放在同一目录）
def get_js_code():
    # PyInstaller 打包时，资源文件路径会变为 sys._MEIPASS
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    js_file = os.path.join(base_path, 'no_recoil_v4_fix.js')  # 使用 V4 修复版
    with open(js_file, 'r', encoding='utf-8') as f:
        return f.read()

# 2. JS 脚本回传消息的处理函数
def on_message(message, data):
    if message['type'] == 'send':
        print(f"[+] {message['payload']}")
    elif message['type'] == 'error':
        print(f"[-] {message['stack']}")
    else:
        print(message)

# 3. 主逻辑
def main():
    TARGET_PROCESS = "UnityCrossFire.exe"  # 目标游戏进程名
    
    print("=" * 50)
    print("  No Recoil V4 Fix")
    print("  (All Modes Support)")
    print("=" * 50)
    print()
    print("[*] 功能：")
    print("  - 自动检测游戏进程")
    print("  - 自动注入无后坐力脚本")
    print("  - 支持所有游戏模式")
    print("  - 换房间自动生效")
    print("  - 零性能影响")
    print()
    print("[*] 提示：")
    print("  - 按 Ctrl+C 退出")
    print("  - 关闭此窗口会自动停止注入")
    print()
    print("=" * 50)
    
    script_code = get_js_code()
    current_session = None
    current_script = None
    
    def inject_script():
        nonlocal current_session, current_script
        
        try:
            # 附加到正在运行的进程
            print(f"\n[*] 正在查找进程：{TARGET_PROCESS}...")
            current_session = frida.attach(TARGET_PROCESS)
            print(f"[+] 成功附加到进程：{TARGET_PROCESS}")
            
            current_script = current_session.create_script(script_code)
            current_script.on('message', on_message)
            current_script.load()
            print("[+] 无后坐力 V4 修复版已激活！")
            print("[*] 返回游戏测试射击效果...")
            print("[*] 监控中：换房间自动生效...")
            print("=" * 50)
            
            # 等待会话结束
            current_session.on('detached', lambda reason: print(f"\n[*] 会话已断开：{reason}"))
            
        except frida.ProcessNotFoundError:
            print(f"[-] 找不到进程 {TARGET_PROCESS}，等待游戏启动...")
            return False
        except Exception as e:
            print(f"[-] 错误：{e}")
            return False
        
        return True
    
    def monitor_process():
        """监控进程，如果断开则重新注入"""
        nonlocal current_session, current_script
        
        while True:
            try:
                time.sleep(5)  # 每 5 秒检查一次
                
                # 检查会话是否还有效
                if current_session is None:
                    print("\n[*] 检测到会话断开，尝试重新注入...")
                    if inject_script():
                        print("[+] 重新注入成功！")
                    else:
                        print("[-] 重新注入失败，继续等待...")
                        
            except KeyboardInterrupt:
                print("\n[*] 用户中断，退出...")
                break
            except Exception as e:
                print(f"[-] 监控错误：{e}")
                time.sleep(5)
    
    # 首次注入
    while not inject_script():
        time.sleep(3)  # 等待 3 秒后重试
    
    # 启动监控线程
    monitor_thread = threading.Thread(target=monitor_process, daemon=True)
    monitor_thread.start()
    
    # 保持主线程运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] 退出中...")
        if current_script:
            current_script.unload()
        if current_session:
            current_session.detach()
        print("[*] 已退出")

if __name__ == '__main__':
    main()
