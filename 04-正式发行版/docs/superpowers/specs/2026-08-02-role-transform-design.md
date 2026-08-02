# 角色变身最小实现设计

## 目标

在多人生化模式中，角色吃到变身补给箱后，按开关配置把实际拾取者变成英雄或幽灵。拾取者既可以是本地玩家，也可以是 Bot。

## 范围

本实现只包含四种结果：

| 拾取者 | 结果 |
| --- | --- |
| 本地玩家 | 英雄（`MasterHumanHero = 23`） |
| 本地玩家 | 幽灵（`Psycho = 7`） |
| Bot | 英雄（`MasterHumanHero = 23`） |
| Bot | 幽灵（`Psycho = 7`） |

每次成功拾取只会应用一个结果。若同一类型同时启用了英雄和幽灵，优先英雄，避免在同一次补给箱事件中连续覆盖角色。

不在本次范围内：角色选择 UI、多种英雄/幽灵的选择、非多人生化模式、生存或网络同步绕过、直接写入 `Player.nanoRole`。

## 已确认的原生链路

IDA Pro MCP 当前连接到同版本 `GameAssembly.dll`，已确认：

```text
英雄：Mode_Nano4.BecomeHero(modeNano4, player, 23, false)
      RVA 0xB412F0

幽灵：ModeBase_Nano.ChangeNanoGhostType(modeNano, player, 7)
      RVA 0xAEF790

统一角色状态更新：ModeBase_Nano.UpdateNanoRole
      RVA 0xAF4FF0
```

这两条原生函数接受目标 `Player*`，不依赖“本地玩家”身份。Bot 原生 AI 也通过相同角色更新链路完成变身；因此不能直接写 `Player.nanoRole`，以保留模型、队伍、导航和 Bot 回调更新。

## 设计

### 触发方式

在补给箱的“成功拾取并已确定拾取者”入口安装 `Interceptor.attach`。Hook 仅记录事件携带的 `Player*`，随后在同一游戏线程调用相应的原生变身函数。实现阶段会先用 IDA 交叉引用和日志验证该入口，再将已验证 RVA 写入脚本注释和常量。

### 目标判定

从补给箱事件取得的 `Player*` 读取玩家身份。仅在以下条件均满足时继续：

1. 当前模式是多人生化模式；
2. `Player*` 可读且存活；
3. 事件确实代表成功拾取；
4. 身份属于本地玩家或 Bot，且对应开关已启用。

本地玩家使用游戏原生 `Player.get_isMyPlayer` 判定；Bot 使用已验证的 Bot/ClientData 身份来源判定，不以“不是本地玩家”代替 Bot。

### 执行矩阵

```text
本地玩家 + 玩家英雄开关 -> BecomeHero(..., 23, false)
本地玩家 + 玩家幽灵开关 -> ChangeNanoGhostType(..., 7)
Bot      + Bot英雄开关   -> BecomeHero(..., 23, false)
Bot      + Bot幽灵开关   -> ChangeNanoGhostType(..., 7)
```

若目标已是对应角色，跳过调用。调用前重新取得模式单例，避免跨房间缓存 `Player*` 或模式对象。

### 生命周期与接口

核心 Frida 脚本维护单一 `Runtime`：启用状态、generation、Hook 句柄、限频日志、当前配置和统计。导出标准 RPC：`enable`、`disable`、`status`、`cleanup`、`setConfig`。关闭、卸载、切房间或失效时，`resetRuntime` 移除 Hook 并丢弃全部对象指针。

## 文件与交付位置

当前仓库的开发规范要求先在 `05-正式功能/34-角色变身/` 完成单功能验证，稳定后才进入 `04-正式发行版/全功能整合包2.4`。本次会先建立：

```text
05-正式功能/34-角色变身/
  AAAAA-role_transform_min.js
  AAAAA-role_transform_ui.py
  角色变身-简要说明.md
```

完成游戏内验证并达到 `release_ready` 后，才以正式插件壳迁移到 `04-正式发行版/全功能整合包2.4/game_modifier/features/`。

## 验证

自动检查：`node --check`、`python -m py_compile`、静态测试检查导出 RPC、角色 RVA、生命周期接口和 UI 调用方式。

游戏内检查：四种变身路径各测试一次；重复开关；连续拾取；死亡/重生；切房间；退出游戏。若 Hook 未命中，将记录补给箱候选调用参数，再用 IDA 继续收敛入口，不以猜测 RVA 写入正式脚本。
