# AGENTS.md · UCF 1.7 修改器 — Agent 读取与检索策略

> 本文件由 DSH 在会话首次请求时自动注入（项目根 → 当前工作目录），**不需要 agent 主动 read**。
> 目标：把"每次先把项目读一遍"换成"按任务取最小充分上下文"。
> 仓库现状：约 **2.0 GB / 3.9 万个文件**，其中对"写新功能"有用的不足 10%。

## 0. 版本事实（先记这里，别读错目录）

| 角色 | 路径 | 说明 |
| --- | --- | --- |
| 当前开发版 | `04-正式发行版/全功能整合包2.8/` | dev 分支正在改，新功能以它为准 |
| 最新正式版 | `04-正式发行版/全功能整合包2.7/` | 稳定对照，只读，不在这里加功能 |
| 历史版本 | `全功能整合包1.0` ~ `2.6`、`1.7-修复版` | 默认不读，见 §3 |

README 里写的"当前版本 2.7"是 2026-10-22 的快照，已落后于 2.8。

## 1. 会话启动只读这些

1. `02-开发规范/00-总览与导航.md` —— 入口索引、阅读顺序、主题权威表
2. `02-开发规范/01-项目背景与游戏信息.md` —— 游戏信息、逆向资料位置、技术红线
3. 只有确认要动手写代码时，才继续读 §2 中对应任务的规范

**不要**一上来 `glob "**/*"`、不要递归列根目录、不要"先把项目读一遍再开始"。

## 2. 按任务取最小阅读集

| 任务 | 必读 | 选读 | 不读 |
| --- | --- | --- | --- |
| 写新功能 | 00-总览、01-背景、`10-单功能开发/11`、`12`、`13`、`20-整合包接入/21`、`22`、`90-通用规范/91`、`2.8/game_modifier/features/` 下同类功能、`02-开发规范/各个功能/对应.md` | `23-快捷键`、`31-程序与UI`、`03-经验手册/01-IL2CPP逆向` | `05-正式功能/` 旧代码、1.0–2.6、`.lst`、AssetStudio |
| 改现有功能 | `2.8/game_modifier/features/<功能>/`（script.js + feature.py + panel.py + manifest.json）、`22-持久化总表`、`13-生命周期` | `02-开发规范/各个功能/对应.md` | 其他功能目录、历史版本 |
| 排查崩溃/失效 | `03-经验手册/` 相关篇、`06-测试/` 对应目录、`2.7/game_modifier/logs/` 里的具体日志（logs 被 .gitignore 排除，grep 看不到，直接 read 文件） | 对 dump.cs 做 grep | `.lst`、AssetStudio |
| 打包发布 | `32-打包发布须知`、`34-安装器`、`31-程序与UI`、`91-编码` | `2.7/game_modifier/release/` 的产物结构 | `dist_release/` 全量 |
| 逆向/找地址 | IDA MCP（已连 GameAssembly.dll）、`03-经验手册/01` | 对 dump.cs / script.json 做 grep | `.lst`、AssetStudio 遍历 |

## 3. 硬性排除清单（默认不读；要读先说明理由）

| 路径 / 模式 | 体量 | 替代做法 |
| --- | --- | --- |
| `00-游戏逆向分析-相关信息/IDA-汇编代码/切分输出/**/*.lst` | 42 个，384 MB | **用 IDA MCP 替代**（见 §5） |
| `00-游戏逆向分析-相关信息/AssetStudio/` | 21 682 个，161 MB | 需要素材名时按文件名 grep，不遍历 |
| `00-游戏逆向分析-相关信息/Il2CppDumper/dump.cs` | 9.1 MB | `grep` 类/方法名，再 `read` 命中附近行 |
| `00-游戏逆向分析-相关信息/Il2CppDumper/script.json` | 25.6 MB | 只查字符串字面量时用脚本/jq 过滤，不整读 |
| `00-游戏逆向分析-相关信息/Il2CppDumper/il2cpp.h` | 14 MB | 只在写 C 侧代码时按符号 grep |
| `04-正式发行版/.venv-build/` | 3 832 个，181 MB | 不读 |
| `04-正式发行版/全功能整合包1.0` ~ `2.6`、`1.7-修复版` | 2 424 个，38 MB | 默认不读；只在"旧版怎么实现/回归对比"时按单文件读 |
| `2.7/game_modifier/{build,build_release,dist_release,release,logs}/` | 约 304 MB | 看源码去 2.8；查发布产物结构只列一层 |
| `05-正式功能/18-Universal-ESP盒子/*.{obj,pdb,iobj,ipdb,tlog}` | 约 215 MB | 只读 `.cpp/.h/.sln` |
| `.git/` | 715 MB | 工具已排除；不要加 `--hidden` 硬扫 |
| `*.pyc`、`__pycache__`、`*.zip`、`*.exe`、`*.pyd`、`*.dll`、`*.log`、图片 | — | 不读；UI/素材任务除外 |
| `类关系分析/` | 182 个，5.6 MB | 作者自用整理，AI 不需要看 |
| `.dsh-tmp-dis/` | — | 临时反汇编输出，不读 |

## 4. 检索纪律（DSH 工具行为差异，重要）

- **glob 不认 `.gitignore`/`.ignore`**：它用 `rg --files --no-ignore --hidden`，只排除 `.git` 等 VCS 目录。所以必须用 `path` 收窄范围：
  `glob({ pattern: "**/*.py", path: "04-正式发行版/全功能整合包2.8/game_modifier" })`
- **grep 认忽略文件**：默认遵循 `.gitignore`/`.ignore` 并跳过隐藏文件；仓库根的 `.ignore` 已把 §3 的重目录排除。再加 `include: "*.py"` 更稳。
- **read 默认 2000 行**：读大文件必须带 `offset`/`limit`，先 grep 定位行号。
- 顺序固定：**grep 定位 → read 局部 → 需要结构再看目录**。
- 不要用 `pwsh Get-ChildItem -Recurse` 扫全仓。

## 5. 逆向资料替代规则（重点）

- 查函数汇编 / 地址 / 交叉引用 → **IDA MCP**。当前库：`GameAssembly.dll`，base `0x10000000`，md5 `fab04426db6a014c0129ef2001530908`。
  常用：`decompile_function`、`disassemble_function`、`get_xrefs_to`、`list_strings_filter`、`get_function_by_name`。
- 查类 / 字段 / 方法签名 → 对 `dump.cs` 做 grep（如 `grep({ pattern: "class .*Weapon", include: "dump.cs" })`），不要整文件 read。
- **只有** IDA MCP 不可用、且用户明确要求时，才允许读单个 `.lst` chunk：先 grep 该 chunk 定位函数，再 `read` 命中附近 ≤200 行。

## 6. 例外流程

用户点名某个被排除路径，或任务确实需要（例如"对比 2.5 与 2.8 的差异"）时可以读，但先说明三件事：
**为什么必须读 → 只读哪几个文件 → 预计多大**。

## 7. 收尾自检

- 本次是否读过 `.lst` / AssetStudio / 类关系分析 / 1.0–2.6 / build 产物？若非用户要求，即为违规。
- 每次 read 是否 ≤ 2000 行、且有明确目的？
- 是否用 IDA MCP 代替了 `.lst`？

## 更新记录

```text
更新日期：2026-11-08
更新说明：建立 Agent 读取策略：固定入口、按任务最小阅读集、硬性排除清单（.lst / AssetStudio / 历史版本 / 构建产物 / 类关系分析）、glob 与 grep 的忽略行为差异、IDA MCP 替代 .lst 的规则。
```
