import frida
import sys
import json
import time

class WeaponIDFinder:
    def __init__(self):
        self.session = None
        self.script = None
        self.weapon_log = []
        
    def connect(self, process_name="UnityCrossFire.exe"):
        try:
            self.session = frida.attach(process_name)
            print(f"[+] 已连接到进程: {process_name}")
            return True
        except Exception as e:
            print(f"[-] 连接失败: {e}")
            return False
    
    def load_script(self, script_path="weapon-id-finder.js"):
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                script_code = f.read()
            
            self.script = self.session.create_script(script_code)
            self.script.on('message', self.on_message)
            self.script.load()
            print(f"[+] 脚本已加载: {script_path}")
            return True
        except Exception as e:
            print(f"[-] 加载脚本失败: {e}")
            return False
    
    def on_message(self, message, data):
        if message['type'] == 'send':
            payload = message['payload']
            if payload['type'] == 'log':
                level = payload.get('level', 'info')
                module = payload.get('module', 'Unknown')
                msg = payload.get('message', '')
                print(f"[{level.upper()}][{module}] {msg}")
        elif message['type'] == 'error':
            print(f"[ERROR] {message['description']}")
    
    def hook_give_weapon(self):
        try:
            result = self.script.exports.hook_give_weapon()
            return result
        except Exception as e:
            print(f"[-] Hook失败: {e}")
            return False
    
    def get_weapon_name(self, weapon_id):
        try:
            name = self.script.exports.get_weapon_name(weapon_id)
            return name
        except Exception as e:
            return None
    
    def test_weapon_range(self, start_id, end_id):
        try:
            results = self.script.exports.test_weapon_range(start_id, end_id)
            return results
        except Exception as e:
            print(f"[-] 测试失败: {e}")
            return []
    
    def get_weapon_log(self):
        try:
            log = self.script.exports.get_weapon_log()
            return log
        except Exception as e:
            print(f"[-] 获取日志失败: {e}")
            return []
    
    def clear_weapon_log(self):
        try:
            self.script.exports.clear_weapon_log()
            print("[+] 武器日志已清空")
        except Exception as e:
            print(f"[-] 清空日志失败: {e}")

def main():
    print("=" * 60)
    print("武器ID查找工具")
    print("=" * 60)
    
    finder = WeaponIDFinder()
    
    if not finder.connect():
        return
    
    if not finder.load_script():
        return
    
    print("\n使用说明:")
    print("1. 选择 'Hook GiveWeapon' 开始监听")
    print("2. 在游戏中正常选择武器")
    print("3. 返回查看记录的武器ID")
    print("4. 或使用批量测试功能")
    
    while True:
        print("\n" + "=" * 60)
        print("选项:")
        print("  1. Hook GiveWeapon 方法")
        print("  2. 查看武器日志")
        print("  3. 清空武器日志")
        print("  4. 批量测试武器ID (1-100)")
        print("  5. 自定义范围测试")
        print("  6. 查询单个武器名称")
        print("  7. 导出武器ID列表")
        print("  0. 退出")
        print("=" * 60)
        
        choice = input("请选择: ").strip()
        
        if choice == '1':
            result = finder.hook_give_weapon()
            if result:
                print("[+] Hook成功，现在可以在游戏中选择武器")
                print("[+] 返回此界面查看记录的武器ID")
            else:
                print("[-] Hook失败")
        
        elif choice == '2':
            log = finder.get_weapon_log()
            if log:
                print("\n武器日志:")
                for entry in log:
                    weapon_id = entry.get('weaponIndex', 'Unknown')
                    time_str = entry.get('time', 'Unknown')
                    print(f"  [{time_str}] 武器ID: {weapon_id}")
            else:
                print("[-] 武器日志为空")
        
        elif choice == '3':
            finder.clear_weapon_log()
        
        elif choice == '4':
            print("\n开始批量测试武器ID (1-100)...")
            results = finder.test_weapon_range(1, 100)
            if results:
                print(f"\n找到 {len(results)} 个有效武器:")
                for weapon in results:
                    print(f"  ID {weapon['id']:3d}: {weapon['name']}")
            else:
                print("[-] 未找到有效武器")
        
        elif choice == '5':
            try:
                start_id = int(input("输入起始ID: "))
                end_id = int(input("输入结束ID: "))
                print(f"\n开始测试武器ID ({start_id}-{end_id})...")
                results = finder.test_weapon_range(start_id, end_id)
                if results:
                    print(f"\n找到 {len(results)} 个有效武器:")
                    for weapon in results:
                        print(f"  ID {weapon['id']:3d}: {weapon['name']}")
                else:
                    print("[-] 未找到有效武器")
            except ValueError:
                print("[-] 请输入有效的数字")
        
        elif choice == '6':
            try:
                weapon_id = int(input("输入武器ID: "))
                name = finder.get_weapon_name(weapon_id)
                if name:
                    print(f"[+] 武器名称: {name}")
                else:
                    print(f"[-] 未找到武器 ID={weapon_id}")
            except ValueError:
                print("[-] 请输入有效的数字")
        
        elif choice == '7':
            log = finder.get_weapon_log()
            if log:
                filename = f"weapon_id_list_{int(time.time())}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(log, f, indent=2, ensure_ascii=False)
                print(f"[+] 武器ID列表已导出: {filename}")
            else:
                print("[-] 武器日志为空，无法导出")
        
        elif choice == '0':
            print("退出程序")
            break
        
        else:
            print("[-] 无效选项")

if __name__ == "__main__":
    main()
