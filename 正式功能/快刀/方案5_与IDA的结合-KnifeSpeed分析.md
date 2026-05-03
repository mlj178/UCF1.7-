# 快刀方案5：修改 PlayerWeapons.KnifeSpeed

## 为什么之前没发现，现在 IDA 分析才发现？

### 原因分析

```
┌─────────────────────────────────────────────────────────────┐
│  dump.cs 文件中其实有这个字段！                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ public PropertyModifier Modifier_KnifeSpeed; // 0x44  │   │
│  │ public float get_KnifeSpeed() { }                     │   │
│  │                                                       │   │
│  │ 但是 dump.cs 只告诉我们：                               │
│  │ - 有这个字段                                           │   │
│  │ - 偏移是 0x44                                          │   │
│  │ - 有个 get_KnifeSpeed() 方法                           │   │
│  │                                                       │   │
│  │ 但是 dump.cs 没有告诉我们：                             │
│  │ ✗ KnifeSpeed 是如何参与速度计算的                       │   │
│  │ ✗ 最终速度 = KnifeSpeed × 其他字段                     │   │
│  │ ✗ 这个修饰符是玩家专属的                                │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  IDA 反编译 PlayKnifeAttackAnim 后才发现：                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ v31 = sub_10B170A0(v22);  // PlayerWeapons.get_KnifeSpeed() │
│  │ sub_10B34E40(a1, ..., v31 * v28, ...);  // 相乘！      │   │
│  │                                                       │   │
│  │ 原来 KnifeSpeed 是作为一个乘数参与最终速度计算的！        │   │
│  │ 这才是关键！                                            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 关键区别

```
dump.cs 能看到的：
┌─────────────────────────────────────────────────────────────┐
│  class PlayerWeapons {                                       │
│      public PropertyModifier Modifier_KnifeSpeed; // 0x44    │
│      public float get_KnifeSpeed() { }                       │
│  }                                                           │
│                                                             │
│  只知道"有这个属性"，但不知道"怎么用"                          │
└─────────────────────────────────────────────────────────────┘

IDA 反编译能看到的：
┌─────────────────────────────────────────────────────────────┐
│  PlayKnifeAttackAnim 函数内部：                               │
│                                                             │
│  float knifeSpeed = PlayerWeapons.get_KnifeSpeed();          │
│  float animSpeed = combo1_AnimSpeed;  // 或其他字段           │
│  float finalSpeed = knifeSpeed * animSpeed;  ← 关键！         │
│  Animator.SetSpeed(finalSpeed);                              │
│                                                             │
│  看到了"实际计算逻辑"！                                       │
└─────────────────────────────────────────────────────────────┘
```

### 我之前为什么没发现？

```
┌─────────────────────────────────────────────────────────────┐
│  1. 分析方向错误                                              │
│     - 我一直关注 Weapon 类的字段                              │
│     - 关注 combo1_AnimSpeed、attackSpeed                     │
│     - 没有追踪到 PlayerWeapons.KnifeSpeed                    │
│                                                             │
│  2. 没有分析速度计算的完整链路                                 │
│     - 只看了字段定义                                         │
│     - 没有看 PlayKnifeAttackAnim 函数内部逻辑                 │
│     - 不知道 KnifeSpeed 是乘数                               │
│                                                             │
│  3. dump.cs 的局限性                                         │
│     - 只有类定义，没有函数实现                                │
│     - 看不到字段是如何被使用的                                │
│     - 需要 IDA 反编译才能看到实际逻辑                         │
└─────────────────────────────────────────────────────────────┘
```

### 总结

```
dump.cs → 静态结构（有什么）
IDA     → 动态逻辑（怎么用）

两者结合才能完整理解：
1. dump.cs 找到 PlayerWeapons.Modifier_KnifeSpeed (0x44)
2. IDA 发现 KnifeSpeed 是速度计算的乘数
3. 结论：修改 KnifeSpeed 可以加速所有攻击段，且只影响玩家
```

---

## IDA 反编译分析结果

### PlayKnifeAttackAnim 函数逻辑

```c
// sub_10B642B0 = WPN_Knife.PlayKnifeAttackAnim(KnifeAttackType type)
// a1 = WPN_Knife 实例
// a2 = KnifeAttackType (1=Combo1, 2=Combo2, 3=Bigshot)

if (a2 == 1)  // Combo1 轻击第一段
{
    v28 = *(float *)(a1 + 236);  // 0xEC = combo1_AnimSpeed (实例字段!)
    v31 = sub_10B170A0(v22);     // PlayerWeapons.get_KnifeSpeed()
    sub_10B34E40(a1, ..., v31 * v28, ...);  // 最终速度 = KnifeSpeed × combo1_AnimSpeed
}
else if (a2 == 2)  // Combo2 轻击第二段
{
    v15 = sub_10B2A7F0(*(v14 + 236));  // 读取 data->attackSpeed.y
    v30 = sub_10B170A0(v17);           // PlayerWeapons.get_KnifeSpeed()
    sub_10B34E40(a1, ..., v30 * v28, ...);  // 最终速度 = KnifeSpeed × attackSpeed.y
}
else if (a2 == 3)  // Bigshot 重击
{
    v5 = sub_10B2A7F0(*(v4 + 240));  // 读取 data->attackSpeed.z
    v29 = sub_10B170A0(v7);          // PlayerWeapons.get_KnifeSpeed()
    sub_10B34E40(a1, ..., v29 * v28, ...);  // 最终速度 = KnifeSpeed × attackSpeed.z
}
```

### 最终速度公式

```
┌─────────────────────────────────────────────────────────────┐
│  最终动画速度 = PlayerWeapons.KnifeSpeed × 实例/共享字段      │
│                                                             │
│  Combo1:  KnifeSpeed × combo1_AnimSpeed (0xEC, 实例)         │
│  Combo2:  KnifeSpeed × attackSpeed.y (共享)                  │
│  Bigshot: KnifeSpeed × attackSpeed.z (共享)                  │
│                                                             │
│  PlayerWeapons.KnifeSpeed 是玩家专属的属性修饰符！             │
│  它不会影响机器人！                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 方案5：修改 PlayerWeapons.KnifeSpeed（最佳方案）

### 原理

```
┌─────────────────────────────────────────────────────────────┐
│  PlayerWeapons 类 (0x44 偏移)                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ public PropertyModifier Modifier_KnifeSpeed; // 0x44  │   │
│  │                                                       │   │
│  │ public float get_KnifeSpeed() {                       │   │
│  │     // 返回基础速度 × 修饰符                           │   │
│  │ }                                                     │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  每个 Player 有自己的 PlayerWeapons 实例！                    │
│  修改玩家的 KnifeSpeed → 只影响玩家的武器！                   │
│  机器人的 KnifeSpeed 不受影响！                               │
│                                                             │
│  效果：                                                       │
│  ✓ 轻击第一段加速 (KnifeSpeed × combo1_AnimSpeed)            │
│  ✓ 轻击第二段加速 (KnifeSpeed × attackSpeed.y)               │
│  ✓ 重击加速 (KnifeSpeed × attackSpeed.z)                     │
│  ✓ 只影响玩家                                                 │
│  ✓ 不影响机器人                                               │
│  ✓ 切换背包自动生效（同一个 PlayerWeapons 实例）               │
│  ✓ 退出房间自动失效（PlayerWeapons 实例销毁）                  │
└─────────────────────────────────────────────────────────────┘
```

### 验证 PlayerWeapons 实例独立性

```
内存布局：
┌─────────────────────────────────────────────────────────────┐
│  本地玩家的 PlayerWeapons: 0xAAAA0000                         │
│  ├─ 0x8: owner → 本地玩家                                     │
│  ├─ 0x44: Modifier_KnifeSpeed → 可修改                        │
│  └─ KnifeSpeed 返回值 = 1.0 (默认)                            │
│                                                             │
│  机器人的 PlayerWeapons: 0xBBBB0000                           │
│  ├─ 0x8: owner → 机器人                                       │
│  ├─ 0x44: Modifier_KnifeSpeed → 不修改                        │
│  └─ KnifeSpeed 返回值 = 1.0 (默认)                            │
│                                                             │
│  修改 0xAAAA0000+0x44 → 只影响本地玩家！                       │
└─────────────────────────────────────────────────────────────┘
```

### 生命周期管理

```
┌─────────────────────────────────────────────────────────────┐
│  进入房间：                                                   │
│  - 找到本地玩家的 Player 实例                                 │
│  - 读取 player + 0xA0 得到 PlayerWeapons 指针                │
│  - 修改 PlayerWeapons + 0x44 的 Modifier_KnifeSpeed          │
│                                                             │
│  切换背包：                                                   │
│  - 无需处理！                                                 │
│  - 同一个 PlayerWeapons 实例管理所有背包                      │
│  - KnifeSpeed 修改持续有效                                    │
│                                                             │
│  退出房间：                                                   │
│  - PlayerWeapons 实例被销毁                                   │
│  - 修改自动失效                                               │
│  - 不影响下次游戏                                             │
└─────────────────────────────────────────────────────────────┘
```
