# 高跳空中移动只读探针

这个工具用于比较整合包 2.4 与 2.5 的“高跳后空中 WSAD 移动”运行时表现。

它是**只读**探针：不会写入游戏内存、不会替换游戏函数、不会调用修改器开关，也不会修改整合包源码。它仅自动等待并附加 `UnityCrossFire` 进程，记录已知移动入口调用和高跳脚本涉及的字段快照。

## 运行前准备

1. 关闭会改动角色位置的其他功能，特别是穿墙、瞬移和自由视角。
2. 启动对应版本的修改器，并连接游戏；探针不负责启用轻重力。
3. 在本目录打开 PowerShell。若修改器或游戏以管理员身份运行，探针也需要以管理员身份运行。

## 测试整合包 2.4

```powershell
python .\gravity_airmove_probe.py --label 2.4
```

探针会显示等待状态。随后启动或进入 `UnityCrossFire`，它会自动附加。

## 测试整合包 2.5

```powershell
python .\gravity_airmove_probe.py --label 2.5
```

每次只比较一个版本；完成 2.4 测试后关闭探针，再启动 2.5 测试。

## 两个版本必须采用相同复现步骤

1. 只开启轻重力 / 高跳，并使用相同的重力、跳跃倍率和生效范围。
2. 先在地面分别按 W、A、S、D，确认正常移动。
3. 起跳后依次按住 W、A、S、D，各持续约两秒。
4. 落地后停止探针：在 PowerShell 中按 `Ctrl+C`。

## 日志文件

所有文件在 `logs` 子目录中：

- `gravity_airmove_2.4_<时间>.jsonl` 或 `gravity_airmove_2.5_<时间>.jsonl`：逐事件日志。
- 相同前缀的 `_summary.json`：会话摘要，包括附加状态、Hook 命中、离地样本、可解析的水平移动样本和错误数。

空中没有出现 `controller_move` 事件本身也是有效证据：它表示水平移动调用可能在进入角色控制器之前就被阻断。请保留 2.4 和 2.5 的两份日志，再交给我进行逐项比较。

## 自检

```powershell
python -m unittest .\test_gravity_airmove_probe.py -v
Select-String -LiteralPath .\gravity_airmove_probe.js -Pattern 'write|replace|NativeCallback|rpc' -CaseSensitive:$false
```

第二条命令不应输出任何匹配行；这是确认游戏内脚本未包含内存写入、替换或修改器调用标记的静态检查。
