# Connection And Battle Round UX Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让决战回合可随时预约但只在多人生化回合写字段，并缩短程序启动到普通功能可用的等待时间。

**Architecture:** 使用低频房间生命周期Hook代替Python定时轮询；连接管理器先完成Frida核心连接，再按ESP意愿后台处理Universal DLL。状态机仅在无进展时等待，成功转换立即继续。

**Tech Stack:** Python、CustomTkinter、Frida JavaScript、Universal DLL命名管道。

---

### Task 1: 决战回合事件化

**Files:**
- Modify: `04-正式发行版/全功能整合包1.7-修复版/game_modifier/scripts/19-battle_round.js`
- Modify: `04-正式发行版/全功能整合包1.7-修复版/game_modifier/core/frida_manager.py`
- Modify: `04-正式发行版/全功能整合包1.7-修复版/game_modifier/ui/app.py`

- [ ] 删除启用和禁用时对 `isBattleRound` 的立即写入。
- [ ] 始终安装低频新回合/退出房间Hook，精确验证 `Mode_Nano4_Terminator` 后才允许写字段。
- [ ] 发送模式进入、回合状态、模式退出事件，并在UI显示关闭、等待连接、已预约、已生效。
- [ ] 允许用户在未连接或未进入模式时操作开关，连接后恢复用户意愿。

### Task 2: 删除持续轮询

**Files:**
- Modify: `04-正式发行版/全功能整合包1.7-修复版/game_modifier/scripts/15-buff_selector.js`
- Modify: `04-正式发行版/全功能整合包1.7-修复版/game_modifier/ui/app.py`

- [ ] 删除1秒决战状态RPC和2秒多人生化健康轮询。
- [ ] 删除5秒当前Buff轮询，改为新回合事件触发一次读取。
- [ ] 将 `ModeBase.Update` 调度Hook改为有请求时临时安装、处理后立即解除。
- [ ] Frida连接后仅执行一次当前房间状态检查，避免漏掉已进入的房间。

### Task 3: 连接状态机提速与ESP按需加载

**Files:**
- Modify: `04-正式发行版/全功能整合包1.7-修复版/game_modifier/core/game_session_manager.py`

- [ ] 将进程检测等待改为0.8秒，READY健康检查改为3秒。
- [ ] 成功状态转换后立即执行下一步，不再每一步固定等待2秒。
- [ ] 检测进程稳定0.5秒后优先连接Frida并发布普通功能就绪事件。
- [ ] 仅当ESP期望状态为开启时连接或注入DLL；开启ESP时唤醒后台工作线程。
- [ ] 保留1、2、4、8秒失败退避和手动立即重试。

### Task 4: UI启动和快捷键延后

**Files:**
- Modify: `04-正式发行版/全功能整合包1.7-修复版/game_modifier/ui/app.py`

- [ ] 基础状态区域建立后立即订阅事件并启动进程检测，再继续构建完整页面。
- [ ] 将全局快捷键注册延后到Tk主循环启动后执行。
- [ ] 保持JSON配置同步读取，不增加Frida脚本缓存文件。

### Task 5: 文档与静态验证

**Files:**
- Modify: `04-正式发行版/全功能整合包1.7-修复版/程序文档.md`

- [ ] 在原文末尾追加本次连接与交互改造记录。
- [ ] 对修改后的Python执行 `py_compile`，对JavaScript执行 `node --check`。
- [ ] 搜索确认不存在立即写入、1秒/2秒/5秒轮询和永久空闲Update调度路径。
