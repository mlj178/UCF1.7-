# 自瞄-Physics可见性打空气问题复盘

记录时间：2026-07-26

对应版本：全功能整合包 2.3

对应功能：`features/11_aim`

## 现象

开启自瞄后，准星会锁到敌人附近，但部分敌人明明在眼前，子弹打过去像打空气。

用户视角的表现是：

- 关闭 Physics 可见性筛选后，打人有正常打击效果。
- 恢复 Physics 可见性筛选后，曾经出现“能锁到、能射过去、但敌人不掉血”的情况。
- 日志里不一定能看到全部问题，因为日志只记录被自瞄捕捉到的目标；没被捕捉进来的敌人，游戏里表现就是打不到。

## 根因判断

问题核心不在胸部坐标，也不在准星角度计算。

更可信的根因是：Physics 可见性检测跑得太激进，并且和开枪射线 Hook 共用了同一批 native 缓冲区，导致 Unity Physics 查询之间互相污染。

具体说人话就是：

1. 目标扫描以前用 `setInterval` 每 30ms 调一次。
2. 扫描里会调用 Unity 的 Physics Raycast。
3. 开枪时 `Recoil.GetShootRay` Hook 里也会调用 Physics Raycast。
4. 两边以前共用 `physicsSceneBuffer`、`visibilityRayBuffer`、`visibilityHitBuffer`。
5. Frida 的 `NativeFunction` 默认调度可能释放 JS 锁，两个 Physics 调用有机会交叉执行。
6. 一旦缓冲区被覆盖，筛选结果和射击修正就可能拿到错误 hit 信息。

所以表面看是“射线可见性筛掉了目标”，实际更像是“扫描线程、射击线程、Physics 缓冲区混在一起了”。

## 证据

- 关闭 `visibilityCheck` 后，用户实测打击效果恢复，说明问题和 Physics 可见性链路强相关。
- 日志曾出现较多 `no_shootable_hitbox`，说明 HitBox/可见性判断把一部分目标排除了。
- 日志里原始射击方向和修正方向曾经接近 `0` 度偏差，说明角度计算本身不是主要问题。
- 2.2 老方案没有默认开启可见性，也没有这么重的 Physics 射线筛选，因此没有这个“打空气”表现。

## 修复方案

本次采用“保留可见性，但降低副作用”的方案：

1. 恢复 `visibilityCheck: true`。
2. 目标扫描不再用独立 `setInterval` 硬扫，改为挂在相机更新 Hook 后面跑。
3. 扫描频率保留 30ms 节流，但执行时机靠近 Unity 相机主流程。
4. Physics `NativeFunction` 改成 `scheduling: 'exclusive'`，减少重入交叉。
5. 每次扫描、每次开枪都创建自己的 Physics scratch buffer，不再共用全局缓冲区。
6. 目标选择可见性只检测环境阻挡，使用 `QueryTriggerInteraction.Ignore`，不让触发器误挡目标。
7. 开枪射线命中验证仍允许 `HitBox` 触发器，使用 `QueryTriggerInteraction.Collide`，因为游戏 hitbox 很可能就是 trigger collider。

## 当前逻辑

目标选择阶段：

- 从相机位置往敌人胸部点打一条可见性射线。
- 只看环境/水面这类阻挡。
- 忽略 trigger，避免空气墙、检测区、hitbox 触发器误判成遮挡。

开枪修正阶段：

- Hook `Recoil.GetShootRay`。
- 根据当前目标胸部点修正射击 Ray。
- 再做一次命中验证，确认射线能打到目标身上的 HitBox/Entity。

## 以后注意

- 自瞄只应该改“准星/射击方向”，尽量不要改原版伤害流程。
- 可见性筛选可以做，但不要过度依赖 Physics 结果一票否决。
- Unity Physics 查询尽量放在游戏主流程附近执行，不要用高频独立定时器乱扫。
- Native 调用涉及返回结构体、RaycastHit、Ray 这种 buffer 时，不要多个流程共用同一个内存块。
- 目标筛选阶段和开枪命中阶段要分开配置：筛选看墙，开枪看 hitbox。

## 涉及文件

- `04-正式发行版/全功能整合包2.3/game_modifier/features/11_aim/script.js`
- `04-正式发行版/全功能整合包2.3/game_modifier/features/11_aim/test_aim_static.py`
- `04-正式发行版/全功能整合包2.3/game_modifier/features/11_aim/test_aim_runtime.js`

## 验证命令

```powershell
node --check features\11_aim\script.js
node features\11_aim\test_aim_runtime.js
python -m unittest discover -p 'test_*.py' -v
```

验证结果：语法检查通过，运行时测试通过，单元测试通过。
