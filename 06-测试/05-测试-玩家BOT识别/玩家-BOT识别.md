所有player的 ismyplayer() = 全部都是false
 ismyplayer()无法区分玩家和bot
 isbot在大多数模式下可以区分，但是在多人生化模式中，isbot没有数值。
 
 GameManager的静态字段myplayer = 玩家对象

 ┌─────────────────────────────────────────────────────────────┐
│  类继承关系                                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  MonoBehaviour                                              │
│       │                                                     │
│       ├── Entity (实体基类)                                  │
│       │       │                                             │
│       │       └── Player (玩家类) ← 玩家和BOT共用！          │
│       │                                                     │
│       └── Bot (BOT AI组件) ← 独立组件，附加到Player上        │
│                                                             │
└─────────────────────────────────────────────────────────────┘



# Player 遍历结果日志

```markdown
--- 遍历 Player (元素大小=8字节) ---
  #0: 真人 @0x4dd198a0 (isMyPlayer=false, isBot=0)
  #1: Bot(活) @0x4a633450 (isMyPlayer=false, isBot=1)
  #2: Bot(活) @0x4638e8a0 (isMyPlayer=false, isBot=1)
  #3: Bot(活) @0x23edf000 (isMyPlayer=false, isBot=1)
  #4: Bot(活) @0x4dd10e60 (isMyPlayer=false, isBot=1)
  #5: Bot(活) @0x4dd102e0 (isMyPlayer=false, isBot=1)
  #6: Bot(活) @0x4dd13730 (isMyPlayer=false, isBot=1)
  #7: Bot(活) @0x4dd17b80 (isMyPlayer=false, isBot=1)
  #8: Bot(活) @0x4dd17000 (isMyPlayer=false, isBot=1)
  #9: Bot(活) @0x4a463450 (isMyPlayer=false, isBot=1)
  #10: Bot(活) @0x4a5338a0 (isMyPlayer=false, isBot=1)
  #11: Bot(活) @0x4a663cf0 (isMyPlayer=false, isBot=1)
  #12: Bot(活) @0x4a663170 (isMyPlayer=false, isBot=1)
  #13: Bot(活) @0x372825c0 (isMyPlayer=false, isBot=1)
  #14: Bot(活) @0x4a4a7a10 (isMyPlayer=false, isBot=1)
  #15: [空或无效]
  #16: ?? @0x1188f1a8 (isMyPlayer=false, isBot=?)
  #17: [空或无效]
  #18: ?? @0x23f103d0 (isMyPlayer=false, isBot=?)
  #19: ?? @0x23f103b0 (isMyPlayer=false, isBot=?)
  #20: ?? @0x23f10390 (isMyPlayer=false, isBot=?)
  #21: ?? @0x23f10370 (isMyPlayer=false, isBot=?)
  #22: ?? @0x23f10350 (isMyPlayer=false, isBot=?)
  #23: ?? @0x23f10330 (isMyPlayer=false, isBot=?)
  #24: ?? @0x23f10310 (isMyPlayer=false, isBot=?)
  #25: ?? @0x23f102f0 (isMyPlayer=false, isBot=?)
  #26: ?? @0x23f102d0 (isMyPlayer=false, isBot=?)
  #27: ?? @0x23f102b0 (isMyPlayer=false, isBot=?)
  #28: ?? @0x23f10290 (isMyPlayer=false, isBot=?)
  #29: ?? @0x23f10270 (isMyPlayer=false, isBot=?)
```




# 最本质、最可靠的区分依据

**GameManager.myPlayer** 静态字段中存储的 **Player 实例地址**。

## 证据链

1.  **Player.get_isMyPlayer()** 的底层实现就是 `this == GameManager.myPlayer`，这是游戏引擎内置的官方判定方式，被 **60+ 处代码** 调用（从 IDA 汇编列表中可见大量 `call Player$$get_isMyPlayer`）。
2.  **Weapon.get_isMyWeapon()** 同样基于 `owner == GameManager.myPlayer` 的比较。
3.  **日志验证**：遍历所有 Player 时，`isMyPlayer` 对所有对象返回 `false` ——这不是方法失效，而是因为 Frida 脚本调用 `get_isMyPlayer()` 时传入的 `this` 参数可能有问题，或者 `GameManager.myPlayer` 在调用时还未初始化。**MD文档中记录的 GameManager的静态字段myplayer = 玩家对象** 证实了该字段确实指向真人玩家。
4.  **ClientData.isBot** 是辅助标记，但在多人生化模式下不可靠。
5.  **Bot 组件存在性** 是第三种独立方式，但需要额外调用 `GetComponent`，不如直接地址比较高效。

## 三种方式的可靠性排序

| 排名 | 方式 | 可靠性 | 说明 |
| :---: | :--- | :---: | :--- |
| 🥇 | **GameManager.myPlayer 地址比较** | 最可靠 | 全模式通用，游戏核心逻辑依赖此字段 |
| 🥈 | **Bot 组件存在性检测** | 可靠 | 全模式通用，但需额外 GetComponent 调用 |
| 🥉 | **ClientData.isBot 字段** | 部分可靠 | 多人生化模式下可能失效 |