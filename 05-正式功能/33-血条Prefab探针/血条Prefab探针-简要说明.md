# 血条 Prefab 探针简要说明

## 目标

验证一局游戏尚未出现墓碑时，`HUD_Tombstone.otherBarPrefab` 是否已经有效，以及其中的 `HUD_HealthBar.bar`、Image、Sprite、OverrideSprite 和 Material 是否完整。

探针默认只读。只有用户点击“主动生成测试血条”后，才会在下一次 `HUD_Tombstone.Update` 主线程显式执行一次原游戏的 `GetSign → Bind → Active` 链路；RPC 线程不会直接调用 Unity 方法。

## 关键依据

- `HUD_Tombstone.AddHealthBar`：`0xAE1210`
- `HUD_Tombstone.Update`：`0xAE18C0`
- `HUD_ProjectionID.GetSign`：`0xAD9980`
- `SentryGun.AddHealthBar`：`0xB1C8C0`
- `HUD_Tombstone.otherBarPrefab`：`+0x0C`
- `HUD_HealthBar.bar`：`+0x54`
- `HUD_HealthBar.Bind`：`0xB07290`
- `RecyclableObject.Active`：`0xB1A500`
- `HUD_ProjectionSign.Recycle`：`0xAD9AD0`
- `Image.m_Sprite`：`+0x80`
- `Image.m_OverrideSprite`：`+0x84`

## 运行方式

1. 启动 `UnityCrossFire.exe`。
2. 运行 `AAAAA-healthbar_prefab_probe_ui.py`。
3. UI 会自动连接游戏并启用只读采样。
4. 从一局全新的无墓碑对局开始保留日志，不要等墓碑出现后才启动探针。
5. 必要时点击“请求主线程快照”。按钮只设置请求，实际检查会在下一次 `HUD_Tombstone.Update` 主线程执行。

## 主动生成验证

1. 进入一局没有墓碑的对局，并保证场上至少有一个存活的其他玩家或人机。
2. 等待 Prefab、HealthBar、Image、Sprite 四项均显示“有效”。
3. 点击“主动生成测试血条”。探针会选择 `GameManager.allPlayers` 中第一个存活的非本地玩家；按钮只排队动作，实际调用在下一帧 HUD 主线程执行。
4. 成功时日志出现：

```text
[ACTIVE_TEST_REQUESTED] queued=create
[ACTIVE_TEST_CREATED] ...
```

5. 测试结束后点击“回收测试血条”，成功时日志出现：

```text
[ACTIVE_TEST_REQUESTED] queued=recycle
[ACTIVE_TEST_RECYCLED] ...
```

请先回收测试血条再关闭探针。若切换场景，探针不会对上一局的旧地址执行回收调用，原对象交由游戏的回合回收机制处理。

### 预期画面

- 日志中 `playerIndex`/`target` 对应的第一个存活非本地玩家头顶出现游戏原生风格的名称和血条；它不一定是准星所指玩家。
- 血条应跟随该玩家移动，受遮挡/距离等显示规则仍由原 `HUD_ProjectionSign` 控制。
- 目标掉血时，血条长度应跟随变化。
- 点击“回收测试血条”后，该血条应立即消失。
- 如果所有其他玩家均死亡、尚未生成或数组不可用，不会创建血条，日志会出现 `ACTIVE_TEST_REJECTED`。

## 必测时间线

### 阶段 A：无墓碑对局

进入对局后等待 10 秒，确认日志中是否出现：

```text
[PREFAB_SNAPSHOT]
```

不要主动触发墓碑。这个阶段用于判断 Prefab 和 Sprite 是否开局即有效。

### 阶段 B：出现墓碑前

在准备触发墓碑前点击一次“请求主线程快照”，等待新的 `PREFAB_SNAPSHOT`。

### 阶段 C：出现墓碑后

触发墓碑后继续等待 5 秒。日志应出现相关 `TIMELINE`：

```text
HUD_Tombstone.AddHealthBar
HUD_ProjectionID.GetSign
```

随后探针会自动请求一次新的 `PREFAB_SNAPSHOT`，用于对比出现墓碑前和出现墓碑后的引用链。

主动验证不要求出现墓碑；阶段 A 中即可执行。

## 字段解释

`conclusion` 中重点看：

- `prefabReady`：`otherBarPrefab` 是有效 Unity 对象。
- `componentReady`：Prefab 根上能取得 `HUD_HealthBar`。
- `imageReady`：`HUD_HealthBar.bar` 是有效 Image。
- `spriteReady`：`m_Sprite` 或 `m_OverrideSprite` 有效。
- `materialReady`：序列化 Material 有效；为空不一定代表不能渲染，因为 UI Image 可以使用默认材质。
- `completeOriginalBar`：Prefab、HealthBar、Image 和 Sprite 链路均有效。

## 日志回传

点击“保存日志”，把完整 `.log` 文件发回。不要只截取最后几行；需要保留：

- 脚本初始化和 Hook 安装日志。
- 无墓碑阶段的首个 `PREFAB_SNAPSHOT`。
- 出现墓碑前的手动快照。
- 出现墓碑后的全部 `TIMELINE` 和快照。
- 任何 `ERROR` 行。

如果无墓碑阶段一直没有 `HUD_Tombstone.Update` 命中，也请保存并回传日志。这将说明该 HUD 组件本身可能只在特定模式或 UI 场景中激活，需要改用另一个主线程入口读取单例或遍历已加载对象。
