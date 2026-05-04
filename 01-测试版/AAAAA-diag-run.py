# 诊断工具: 对比 GameManager 所有数组
# 功能: 找出 allPlayers 中为 null 的 BOT 藏在哪个数组里

import frida
import psutil
import os
import time

DIAG_JS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AAAAA-diag-v8.js")

def find_game_pid():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if 'CrossFire' in proc.info['name'] or 'game' in proc.info['name'].lower():
                return proc.info['pid']
        except:
            pass
    return None

def main():
    print("="*60)
    print("诊断工具: GameManager 数组对比")
    print("="*60)
    
    pid = find_game_pid()
    if not pid:
        print("❌ 未找到游戏进程，请先启动游戏")
        return
    
    print(f"✅ 找到游戏进程 PID: {pid}")
    
    with open(DIAG_JS_PATH, 'r', encoding='utf-8') as f:
        script_content = f.read()
    
    try:
        device = frida.get_local_device()
        session = device.attach(pid)
        print("✅ 已附加到游戏进程")
        
        script = session.create_script(script_content)
        script.load()
        print("✅ 诊断脚本已加载")
        
        time.sleep(3)
        
        print("🔍 调用诊断函数...")
        script.exports_sync.trigger()
        
        time.sleep(5)
        
        print("\n" + "="*60)
        print("✅ 诊断完成，请查看上方日志")
        print("="*60)
        
    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    main()
