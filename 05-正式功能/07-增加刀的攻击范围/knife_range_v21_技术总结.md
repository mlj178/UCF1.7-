# 近战距离修改器 技术总结

## 一、玩家识别方法

### 核心路径

```
WPN_Knife + 0x30 → owner (Player*)
                      ↓
              isMyPlayer(owner)
                      ↓
                 true = 本地玩家
```





## 四、全模式应用方法

### 为什么 v8 不是全模式生效

v8 有**两个致命问题**导致部分模式无效：

**问题1：Hook 点不对**

| | v8 | v12+/v21 |
|------|-----|-----|
| Hook 函数 | `WPN_Knife.PlayKnifeAttackAnim` (0xB642B0) | `WPN_Knife.GetKnifeAttackData` (0xB63EC0) |
| 函数类型 | **动画函数** | **数据函数** |

`PlayKnifeAttackAnim` 是播放攻击动画的函数。轻击（Combo1/2）走这条路，但**重击（Bigshot）走 `OnSpecialBtnDown`**（0xB64240），不经过 `PlayKnifeAttackAnim`。某些游戏模式（如生化模式、挑战模式）的攻击判定链路可能直接取数据做伤害计算，跳过动画函数。

`GetKnifeAttackData` 是底层数据获取函数——**只要游戏需要知道攻击距离，就必然调它**，无论什么模式、什么攻击类型。



### Hook 目标

| 函数 | RVA | 说明 |
|------|-----|------|
| `WPN_Knife.GetKnifeAttackData` | 0xB63EC0 | 所有近战武器的攻击数据获取入口 |
| `PlayerWeapons.get_KnifeSpeed` | 0xB170A0 | 每次挥刀必调，用于安全捕获 myPlayer |

### 为什么 v21 全模式生效

`WPN_Knife.GetKnifeAttackData` 是所有近战武器（刀、斧、铲等）获取攻击数据的统一底层函数。无论团队模式、生化模式、个人竞技、挑战模式，只要玩家挥刀，游戏必然调此函数获取 `KnifeAttackData` 结构体。

修改点在 `retval + 0x4`（range 字段），不涉及任何模式特定的配置或 ScriptableObject，因此全模式通用。

### 房间切换处理

Hook 以下三个函数检测房间切换并重置 `myPlayer`：

### 





# 近战距离修改器 v22 脚本分析


脚本采用 **Hook 获取攻击数据** 的方式，在游戏读取近战攻击属性（伤害、范围、角度）时，拦截并放大 `range` 值，从而达到超远刀距的效果。

- 将原有的 `Interceptor.replace` 改为 `Interceptor.attach`，以便与同时使用 `replace` 的 **快刀脚本（speed_knife_v16）** 兼容共存。  
- 通过监听 `get_KnifeSpeed` 的调用捕获本地玩家的 `Player` 指针，而非自行遍历查找。

### 

