# 方框透视「多人生化第 2 回合起失效、开关无效」复现手册

> 目标：用一次 5～10 分钟的对局，拿到能**区分三种原因**的日志证据。
> 不用改代码、不用重编 DLL，2.7 自带诊断（DLL 1.8.3 / 协议 6）。

---

## 0. 这次要排除的三个假设

| 假设 | 机理 | 日志指纹（关键） |
|---|---|---|
| **A. 回合结束闸门卡住**（当前最可疑） | `GameManager.gameRoundOver` 静态字段（static+0x20）在后几个回合仍为 1；`IsCandidateRenderable` 里 `if (!relaxed && snapshot.roundOver) return false;` 把整帧候选全拒，而且这种拒绝算在 `rejectedObject`，不触发兜底重扫 | `回合结束=1`、`候选>0`、`来源拒=0`、`对象拒=候选数`、`已画=0`，且 `epoch` 稳定不变 |
| **B. 会话 / 本地玩家丢了** | `GetLocalPlayer()` 返回空，或玩家容器读不到 → Render 在写诊断之前就 return | 诊断行的 `候选/已画/对象拒` **完全冻结不再变化**；`epoch` 每隔 10 秒涨 5～6（无本地玩家看门狗 90 帧一次在狂清缓存）；或 `候选=0` |
| **C. 开关命令被 DLL 丢弃** | 协议 revision 比 DLL 里的小，`set_state` 直接忽略 | 抓取日志出现 `[PipeServer] State update ignored: old revision X <= current Y`，而界面仍提示“方框透视已开启 … rev=X” |

A 和 B 都能解释“整局空白 + 开关无效”，只有日志能分开；C 是另一种“开关没用”，顺手一起排除。

---

## 1. 前置准备

1. **只开「18 方框透视」**。以下功能必须关掉，否则会污染现象（它们会写回合时间 / `gameRoundOver` / ModeBase 静态字段）：
   - 03 无限时间、10 回合跳过、19 强制决战、27 游戏模式切换、24 人机暂停
2. **修改器只开一个**：exe 版和 `python main.py` 版不能同时开（会抢同一个命名管道）。
3. **确认 DLL 是协议 6**：进房后抓取日志里应有
   `"dll_version":"1.8.3" ... "protocol":6`。若 protocol 不是 6，说明游戏里跑的是旧 DLL，需重启游戏后重新注入（此时任何结论都不可信）。
4. **起抓取脚本**（本目录，已验证可用）：

```powershell
cd "D:\trae_project\ucf1.7-modifier\06-测试\18-方框透视回合失效复现"
powershell -NoProfile -ExecutionPolicy Bypass -File .\capture-esp-debug.ps1 -Seconds 1800
```

   - 输出：同目录 `esp_debug_capture.log`（追加写），每行 `[时间] [PID 进程名] 内容`；
   - 抓的是 DLL 的 `OutputDebugStringA`（发布版 DLL 不写 esp_debug.log）；
   - **同一会话只能有一个监听者**：先关掉 DebugView / Visual Studio 调试器，否则会互相抢消息；
   - 不加 `-Filter` 全收；只想看关键行可加 `-Filter "ESP"` 或 `-Filter "PipeServer"`（一次只能一个关键字，跑两遍也行）。
5. 想让日志落盘成完整文本（exe 版**不写任何日志文件**，只有界面日志框）：
   ```powershell
   cd "D:\trae_project\ucf1.7-modifier\04-正式发行版\全功能整合包2.7\game_modifier"
   ..\..\.venv-build\Scripts\python.exe main.py
   ```
   日志 → `04-正式发行版\全功能整合包2.7\game_modifier\logs\game_modifier.log`（5MB 轮转）。
   > 注意：开发版与 exe 的 Frida 版本可能不同，若开发版连不上游戏（界面报连接失败），就以 exe 版为准，只用界面日志 + 抓取脚本的证据。

---

## 2. 复现流程（边做边记时间戳）

| 步骤 | 动作 | 记什么 |
|---|---|---|
| t0 | 进**多人生化**房（生化/终结者等），开局，打开方框透视 | 模式名、房间人数、**第 1 回合**有框（截图） |
| t1 | 第 1 回合结束，进入结算画面 | 结算时没框是正常现象 |
| t2 | 第 2 回合正式开始（能动了） | **有没有框** ← 关键 |
| t2+3s | 没框就别急着退，**先关开关、等 3 秒、再开** | 界面日志里两条 `方框透视已关闭/已开启 … rev=N`，以及有没有报错 |
| t2+20s | 原地站 20 秒（等 ≥2 条诊断行） | 复制/截图 `方框透视诊断:` 行 |
| t3 | 若第 2 回合还好，继续等第 3 回合 | 记录**从第几回合开始失效** |
| t4 | 失效后退出房间、重进新一局 | 是否立刻恢复 ← 区分“整局状态卡死”还是“全局坏了” |

**加速回合**（可选）：开「10 回合跳过」反复跳（先关「03 无限时间」，否则 0:00 会被钳回 99:59）。跳过走的就是 `GameManager.GameRoundEnd` → `gameRoundOver=1` 这条正常路径，正好是我们要观察的对象。

---

## 3. 判定（回到第 0 节的表）

在**失效的那一刻**找最近的一条诊断行：

```
方框透视诊断: mode=… epoch=… 回合结束=… 候选=… 来源拒=… 对象拒=… 敌我拒=… 已画=… (来源兜底=…)
```

- `回合结束=1` + `候选>0` + `来源拒=0` + `对象拒=候选数` + `已画=0` → **A 成立**（就是上一轮分析的闸门 + 兜底条件写窄）。
- `候选/已画/对象拒` 长时间**一模一样不动**，且 `epoch` 每 10 秒涨一截 → **B 成立**（Render 在写诊断前就 return 了，本地玩家取不到）。
- `候选=0` 且 `epoch` 不变 → 容器/会话层面读不到人（也属于 B 的变体，进一步看抓取日志里有没有 `[GameManager] Clearing session state` / `GameManager unavailable`）。
- 抓取日志里出现 `State update ignored: old revision` → **C 成立**。

> 小提醒：ESP 关掉时 DLL 不渲染，诊断数值会冻结在最后一次 —— 这是正常的，别当成 B。判断“冻结”要看**开着 ESP 的失效回合**里数值是否还在变。

---

## 4. 决定性验证（可选，有风险）

「27 游戏模式切换」在应用规则时会写 `GameManager_gameRoundOver = 0`（`features/27_game_mode_override/script.js:2280`）。

所以：**在方框已经消失的状态下**，用 27 应用一次模式规则 —— 如果方框立刻回来，A 就基本坐实了。

⚠️ 27 会同时改写 `targetRound / targetScore / gameTime / respawnTime`，**只在自建房 / 人机房里做**，别在真人局里玩。

---

## 5. 交回给分析的内容

1. `esp_debug_capture.log`（整段，或至少包含 t1～t4 的部分）；
2. 界面日志里的：所有 `方框透视诊断:` 行、`方框透视已开启/已关闭 … rev=` 行、`ESP DLL 已连接/已在后台就绪` 行；
3. 时间轴：t0/t1/t2/t4 + 每步是第几回合 + 模式名 + `mode=` 的数值；
4. `04-正式发行版\全功能整合包2.7\game_modifier\data\universal_revision.json` 的内容。

有这四样，就能把 A/B/C 锁死到其中一条，再决定改哪里。
