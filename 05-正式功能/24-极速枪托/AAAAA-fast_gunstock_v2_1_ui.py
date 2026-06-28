# AAAAA-fast_gunstock_v2_1_ui.py
# 极速枪托 v2.1 防打断保护版 UI
# 用户可见文本全部使用中文。

import os
import time
import threading
from datetime import datetime

import customtkinter as ctk
import frida
import psutil


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JS_FILE = os.path.join(BASE_DIR, "AAAAA-fast_gunstock_v2_1_guard.js")
游戏进程名 = "UnityCrossFire.exe"

颜色_绿 = "#2ecc71"
颜色_红 = "#e74c3c"
颜色_橙 = "#f39c12"
颜色_暗 = "#1a1a2e"
颜色_更暗 = "#16213e"


class 极速枪托窗口(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("极速枪托 v2.1 防打断保护版")
        self.geometry("720x760")
        self.minsize(660, 680)

        self.session = None
        self.script = None
        self.已连接 = False
        self.正在连接 = False
        self.正在轮询 = False
        self.已清理 = False

        self.状态 = {
            "已开启": False,
            "已安装": False,
            "提前伤害延迟ms": 120,
            "伤害后解锁延迟ms": 40,
            "保护超时ms": 650,
            "attackIndex": 0,
            "右键进入次数": 0,
            "右键放行次数": 0,
            "右键吞掉次数": 0,
            "提前伤害次数": 0,
            "自然伤害次数": 0,
            "重复自然伤害吞掉次数": 0,
            "解锁次数": 0,
            "正在保护": False,
            "当前已出伤害": False,
            "最后错误": None,
        }
        self.状态锁 = threading.Lock()

        self.创建界面()
        self.after(600, self.自动连接线程)

    # ==================== 界面 ====================

    def 创建界面(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)

        ctk.CTkLabel(
            self,
            text="极速枪托 v2.1 防打断保护版",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).grid(row=0, column=0, padx=18, pady=(16, 2), sticky="ew")

        ctk.CTkLabel(
            self,
            text="目标：第一次伤害必出，再允许第二次枪托；不再修改手部/角色动画倍率",
            font=ctk.CTkFont(size=12),
            text_color="#aaa",
        ).grid(row=1, column=0, padx=18, pady=(0, 8), sticky="ew")

        状态框 = ctk.CTkFrame(self, corner_radius=8, fg_color=颜色_暗)
        状态框.grid(row=2, column=0, padx=16, pady=4, sticky="ew")
        状态框.grid_columnconfigure(1, weight=1)

        self.连接点 = ctk.CTkLabel(状态框, text="●", font=ctk.CTkFont(size=18), text_color="#888")
        self.连接点.grid(row=0, column=0, padx=(12, 4), pady=8)

        self.连接文本 = ctk.CTkLabel(状态框, text="等待游戏启动...", font=ctk.CTkFont(size=14))
        self.连接文本.grid(row=0, column=1, padx=4, pady=8, sticky="w")

        self.pid文本 = ctk.CTkLabel(状态框, text="", font=ctk.CTkFont(size=11), text_color="#888")
        self.pid文本.grid(row=0, column=2, padx=12, pady=8, sticky="e")

        控制框 = ctk.CTkFrame(self, corner_radius=8, fg_color=颜色_更暗)
        控制框.grid(row=3, column=0, padx=16, pady=4, sticky="ew")
        控制框.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            控制框,
            text="功能开关",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=0, column=0, padx=(12, 6), pady=(12, 8), sticky="w")

        self.功能开关 = ctk.CTkSwitch(
            控制框,
            text="关闭",
            font=ctk.CTkFont(size=13),
            command=self.切换功能,
            progress_color=颜色_绿,
            switch_width=50,
            switch_height=24,
        )
        self.功能开关.grid(row=0, column=1, padx=4, pady=(12, 8), sticky="w")
        self.功能开关.configure(state="disabled")

        self.提前伤害滑块, self.提前伤害数值 = self.添加滑块(
            控制框, 1, "提前伤害延迟", 30, 300, 27, 120, "ms", self.提前伤害变化
        )
        self.解锁滑块, self.解锁数值 = self.添加滑块(
            控制框, 2, "伤害后解锁延迟", 0, 200, 40, 40, "ms", self.解锁变化
        )
        self.超时滑块, self.超时数值 = self.添加滑块(
            控制框, 3, "保护超时", 300, 1500, 24, 650, "ms", self.超时变化
        )
        self.攻击序号滑块, self.攻击序号数值 = self.添加滑块(
            控制框, 4, "attackIndex", 0, 5, 5, 0, "", self.攻击序号变化
        )

        提示框 = ctk.CTkFrame(self, corner_radius=8, fg_color=颜色_暗)
        提示框.grid(row=4, column=0, padx=16, pady=4, sticky="ew")
        提示框.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            提示框,
            text=(
                "推荐起步：提前伤害 120ms，伤害后解锁 40ms。"
                "如果稳定，再把提前伤害降到 100 / 90 / 80ms。"
                "不要一开始低于 60ms。"
            ),
            font=ctk.CTkFont(size=12),
            text_color="#ddd",
            wraplength=650,
            justify="left",
        ).grid(row=0, column=0, padx=12, pady=10, sticky="w")

        信息框 = ctk.CTkFrame(self, corner_radius=8, fg_color=颜色_暗)
        信息框.grid(row=5, column=0, padx=16, pady=4, sticky="ew")
        信息框.grid_columnconfigure((0, 1, 2), weight=1)

        self.开启状态文本 = self.添加信息格(信息框, 0, 0, "功能状态", "关闭")
        self.Hook状态文本 = self.添加信息格(信息框, 0, 1, "Hook 状态", "未安装")
        self.保护状态文本 = self.添加信息格(信息框, 0, 2, "保护窗口", "未保护")

        self.计数文本 = ctk.CTkLabel(
            信息框,
            text="右键: 0 / 放行: 0 / 吞掉: 0 / 提前伤害: 0 / 自然伤害: 0 / 解锁: 0",
            font=ctk.CTkFont(size=11),
            text_color="#aaa",
        )
        self.计数文本.grid(row=2, column=0, columnspan=3, padx=8, pady=(4, 8), sticky="ew")

        日志框 = ctk.CTkFrame(self, corner_radius=8)
        日志框.grid(row=6, column=0, padx=16, pady=(8, 12), sticky="nsew")
        日志框.grid_columnconfigure(0, weight=1)
        日志框.grid_rowconfigure(1, weight=1)

        日志头 = ctk.CTkFrame(日志框, fg_color="transparent")
        日志头.grid(row=0, column=0, padx=8, pady=(6, 2), sticky="ew")

        ctk.CTkLabel(日志头, text="运行日志", font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")
        ctk.CTkButton(
            日志头,
            text="清空",
            width=50,
            height=22,
            font=ctk.CTkFont(size=10),
            fg_color="#444",
            hover_color="#555",
            command=self.清空日志,
        ).pack(side="right")

        self.日志文本框 = ctk.CTkTextbox(日志框, font=ctk.CTkFont(size=11))
        self.日志文本框.grid(row=1, column=0, padx=8, pady=(2, 8), sticky="nsew")

        self.protocol("WM_DELETE_WINDOW", self.关闭窗口)

    def 添加滑块(self, 父级, 行, 名称, 最小, 最大, 步数, 默认, 单位, 回调):
        ctk.CTkLabel(父级, text=名称, font=ctk.CTkFont(size=13)).grid(
            row=行, column=0, padx=(12, 6), pady=6, sticky="w"
        )
        滑块 = ctk.CTkSlider(父级, from_=最小, to=最大, number_of_steps=步数, command=回调)
        滑块.set(默认)
        滑块.grid(row=行, column=1, padx=4, pady=6, sticky="ew")
        滑块.configure(state="disabled")
        文本 = ctk.CTkLabel(
            父级,
            text=str(int(默认)) + 单位,
            width=70,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#aaa",
        )
        文本.grid(row=行, column=2, padx=(6, 12), pady=6)
        return 滑块, 文本

    def 添加信息格(self, 父级, 行, 列, 标题, 默认值):
        格子 = ctk.CTkFrame(父级, corner_radius=6, fg_color=颜色_更暗)
        格子.grid(row=行, column=列, padx=6, pady=8, sticky="ew")
        ctk.CTkLabel(格子, text=标题, font=ctk.CTkFont(size=11), text_color="#888").pack(pady=(6, 0))
        值 = ctk.CTkLabel(格子, text=默认值, font=ctk.CTkFont(size=13, weight="bold"))
        值.pack(pady=(0, 6))
        return 值

    # ==================== 连接 ====================

    def 自动连接线程(self):
        if not self.已连接 and not self.正在连接:
            threading.Thread(target=self.查找并连接, daemon=True).start()
        if not self.已连接:
            self.after(1500, self.自动连接线程)

    def 查找游戏进程(self):
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if proc.info["name"] == 游戏进程名:
                    return proc.info["pid"]
            except Exception:
                pass
        return None

    def 查找并连接(self):
        pid = self.查找游戏进程()
        if not pid:
            self.安全设置(self.连接文本, text="等待游戏启动...")
            self.安全设置(self.连接点, text_color="#888")
            return
        self.执行连接(pid)

    def 执行连接(self, pid):
        if self.正在连接:
            return
        self.正在连接 = True
        self.安全日志("检测到游戏 PID: " + str(pid) + "，正在连接...")

        try:
            self.session = frida.attach(pid)
            self.安全日志("Frida 已附加，正在加载脚本...")

            if not os.path.exists(JS_FILE):
                self.安全日志("JS 文件不存在: " + JS_FILE)
                self.正在连接 = False
                return

            with open(JS_FILE, "r", encoding="utf-8") as f:
                js_code = f.read()

            self.script = self.session.create_script(js_code)
            self.script.on("message", self.接收JS消息)
            self.script.load()

            self.已连接 = True
            self.正在连接 = False
            self.安全设置(self.连接点, text_color=颜色_绿)
            self.安全设置(self.连接文本, text="已连接 - " + 游戏进程名)
            self.安全设置(self.pid文本, text="PID: " + str(pid))
            self.after(0, self.启用控件)
            self.安全日志("脚本已加载，打开开关即可启用防打断极速枪托")
            self.应用所有参数()
            self.开始轮询()

        except frida.ProcessNotFoundError:
            self.安全日志("游戏进程已退出")
            self.正在连接 = False
        except frida.ServerNotStartedError:
            self.安全日志("Frida Server 未运行，请先启动 frida-server")
            self.正在连接 = False
        except Exception as exc:
            self.安全日志("连接异常: " + str(exc))
            self.正在连接 = False

    # ==================== 控件回调 ====================

    def 启用控件(self):
        self.功能开关.configure(state="normal")
        self.提前伤害滑块.configure(state="normal")
        self.解锁滑块.configure(state="normal")
        self.超时滑块.configure(state="normal")
        self.攻击序号滑块.configure(state="normal")

    def 禁用控件(self):
        self.功能开关.configure(state="disabled")
        self.功能开关.deselect()
        self.功能开关.configure(text="关闭")
        self.提前伤害滑块.configure(state="disabled")
        self.解锁滑块.configure(state="disabled")
        self.超时滑块.configure(state="disabled")
        self.攻击序号滑块.configure(state="disabled")

    def 切换功能(self):
        if not self.已连接 or not self.script:
            self.功能开关.deselect()
            return

        if self.功能开关.get():
            self.功能开关.configure(text="开启")
            threading.Thread(target=self.执行开启, daemon=True).start()
        else:
            self.功能开关.configure(text="关闭")
            threading.Thread(target=self.执行关闭, daemon=True).start()

    def 提前伤害变化(self, value):
        v = int(round(float(value) / 10.0) * 10)
        self.提前伤害数值.configure(text=str(v) + "ms")
        self.异步设置参数("setearlydelay", v)

    def 解锁变化(self, value):
        v = int(round(float(value) / 5.0) * 5)
        self.解锁数值.configure(text=str(v) + "ms")
        self.异步设置参数("setunlockdelay", v)

    def 超时变化(self, value):
        v = int(round(float(value) / 50.0) * 50)
        self.超时数值.configure(text=str(v) + "ms")
        self.异步设置参数("setguardtimeout", v)

    def 攻击序号变化(self, value):
        v = int(round(float(value)))
        self.攻击序号数值.configure(text=str(v))
        self.异步设置参数("setattackindex", v)

    def 异步设置参数(self, 名称, 值):
        if self.已连接 and self.script:
            threading.Thread(target=self.执行设置参数, args=(名称, 值), daemon=True).start()

    def 执行设置参数(self, 名称, 值):
        try:
            fn = getattr(self.script.exports_sync, 名称)
            ok = fn(值)
            if ok:
                self.安全日志("参数已设置：" + 名称 + " = " + str(值))
        except Exception as exc:
            self.安全日志("设置参数失败: " + str(exc))

    def 应用所有参数(self):
        self.异步设置参数("setearlydelay", int(round(float(self.提前伤害滑块.get()) / 10.0) * 10))
        self.异步设置参数("setunlockdelay", int(round(float(self.解锁滑块.get()) / 5.0) * 5))
        self.异步设置参数("setguardtimeout", int(round(float(self.超时滑块.get()) / 50.0) * 50))
        self.异步设置参数("setattackindex", int(round(float(self.攻击序号滑块.get()))))

    def 执行开启(self):
        try:
            self.应用所有参数()
            ok = self.script.exports_sync.enable()
            self.安全日志("开启返回: " + str(ok))
        except Exception as exc:
            self.安全日志("开启失败: " + str(exc))
            self.after(0, self.功能开关.deselect)

    def 执行关闭(self):
        try:
            ok = self.script.exports_sync.disable()
            self.安全日志("关闭返回: " + str(ok))
        except Exception as exc:
            self.安全日志("关闭失败: " + str(exc))

    # ==================== 状态轮询 ====================

    def 开始轮询(self):
        self.正在轮询 = True
        threading.Thread(target=self.轮询循环, daemon=True).start()

    def 停止轮询(self):
        self.正在轮询 = False

    def 轮询循环(self):
        while self.正在轮询 and self.已连接 and self.script:
            try:
                status = self.script.exports_sync.status()
                if isinstance(status, dict):
                    with self.状态锁:
                        self.状态.update(status)
                    self.after(0, self.更新状态显示)
            except frida.InvalidOperationError:
                self.安全日志("脚本已失效")
                self.断开连接()
                return
            except Exception:
                pass
            time.sleep(0.35)

    def 更新状态显示(self):
        with self.状态锁:
            已开启 = self.状态.get("已开启", False)
            已安装 = self.状态.get("已安装", False)
            正在保护 = self.状态.get("正在保护", False)
            已出伤害 = self.状态.get("当前已出伤害", False)

            右键 = self.状态.get("右键进入次数", 0)
            放行 = self.状态.get("右键放行次数", 0)
            吞掉 = self.状态.get("右键吞掉次数", 0)
            提前 = self.状态.get("提前伤害次数", 0)
            自然 = self.状态.get("自然伤害次数", 0)
            重复 = self.状态.get("重复自然伤害吞掉次数", 0)
            解锁 = self.状态.get("解锁次数", 0)

        self.开启状态文本.configure(
            text="开启" if 已开启 else "关闭",
            text_color=颜色_绿 if 已开启 else 颜色_红,
        )
        self.Hook状态文本.configure(
            text="已安装" if 已安装 else "未安装",
            text_color=颜色_绿 if 已安装 else 颜色_橙,
        )

        if 正在保护 and not 已出伤害:
            self.保护状态文本.configure(text="等待伤害", text_color=颜色_橙)
        elif 正在保护 and 已出伤害:
            self.保护状态文本.configure(text="等待解锁", text_color=颜色_橙)
        else:
            self.保护状态文本.configure(text="可攻击", text_color=颜色_绿)

        self.计数文本.configure(
            text=(
                "右键: " + str(右键)
                + " / 放行: " + str(放行)
                + " / 吞掉: " + str(吞掉)
                + " / 提前伤害: " + str(提前)
                + " / 自然伤害: " + str(自然)
                + " / 去重: " + str(重复)
                + " / 解锁: " + str(解锁)
            )
        )

    # ==================== 断开与日志 ====================

    def 断开连接(self):
        self.停止轮询()
        if self.script:
            try:
                self.script.exports_sync.cleanup()
            except Exception:
                pass
            try:
                self.script.unload()
            except Exception:
                pass
            self.script = None

        if self.session:
            try:
                self.session.detach()
            except Exception:
                pass
            self.session = None

        self.已连接 = False
        self.安全设置(self.连接点, text_color="#888")
        self.安全设置(self.连接文本, text="已断开")
        self.安全设置(self.pid文本, text="")
        self.after(0, self.禁用控件)
        self.安全日志("已断开连接")

    def 接收JS消息(self, message, data):
        if message.get("type") == "send":
            payload = message.get("payload")
            if isinstance(payload, dict) and payload.get("type") == "日志":
                level = payload.get("level", "信息")
                module = payload.get("module", "")
                msg = payload.get("message", "")
                self.安全日志("[" + level + "][" + module + "] " + msg)
            else:
                self.安全日志("[JS] " + str(payload))
        elif message.get("type") == "error":
            self.安全日志("[JS错误] " + message.get("description", str(message)))

    def 安全设置(self, widget, **kwargs):
        try:
            self.after(0, lambda: widget.configure(**kwargs))
        except Exception:
            pass

    def 安全日志(self, text):
        try:
            self.after(0, lambda: self.添加日志(text))
        except Exception:
            pass

    def 添加日志(self, text):
        时间 = datetime.now().strftime("%H:%M:%S")
        self.日志文本框.insert("end", "[" + 时间 + "] " + text + "\n")
        self.日志文本框.see("end")

    def 清空日志(self):
        self.日志文本框.delete("1.0", "end")

    def 关闭窗口(self):
        if self.已清理:
            return
        self.已清理 = True
        self.断开连接()
        self.destroy()


if __name__ == "__main__":
    app = 极速枪托窗口()
    app.mainloop()
