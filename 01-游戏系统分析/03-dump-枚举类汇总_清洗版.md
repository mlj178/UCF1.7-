# 游戏核心枚举分类对照表（CF专业术语翻译）

## 1. ForceMode 物理作用力模式

| 字段英文名     | 字段中文翻译 | 数值 |
| -------------- | ------------ | ---- |
| Force          | 普通作用力   | 0    |
| Acceleration   | 加速度模式   | 5    |
| Impulse        | 冲量模式     | 1    |
| VelocityChange | 速度变更模式 | 2    |

## 2. CollisionFlags 碰撞方位标识

| 字段英文名    | 字段中文翻译 | 数值 |
| ------------- | ------------ | ---- |
| None          | 无碰撞       | 0    |
| Sides         | 左右侧面     | 1    |
| Above         | 上方         | 2    |
| Below         | 下方         | 4    |
| CollidedSides | 侧面碰撞     | 1    |
| CollidedAbove | 顶部碰撞     | 2    |
| CollidedBelow | 底部碰撞     | 4    |

## 3. QueryTriggerInteraction 触发器检测规则

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| UseGlobal  | 沿用全局设置 | 0    |
| Ignore     | 忽略碰撞体   | 1    |
| Collide    | 检测碰撞体   | 2    |

## 4. BotEnemyInfo.DistanceControl 人机距离行为

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| None       | 无行为       | 0    |
| Close      | 近身作战     | 1    |
| Escape     | 后撤远离     | 2    |

## 5. SocketItem.ItemType 饰品穿戴槽位

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| HeadSet    | 头盔槽       | 0    |
| EyeWear    | 眼镜槽       | 1    |
| Backpack   | 背包槽       | 2    |
| Thigh      | 腿饰槽       | 3    |
| Waist      | 腰饰槽       | 4    |
| Shoulder   | 肩饰槽       | 5    |

## 6. DamageType 伤害类型

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| Invalid    | 无效伤害     | 0    |
| Gun        | 枪械伤害     | 1    |
| Knife      | 近战刀伤     | 2    |
| Grenade    | 手雷伤害     | 3    |
| Infect     | 生化感染伤害 | 4    |
| Other      | 其他伤害     | 5    |

## 7. NanoRoleSelect.Type 生化角色选择类型

| 字段英文名  | 字段中文翻译 | 数值 |
| ----------- | ------------ | ---- |
| None        | 无类型       | 0    |
| Normal      | 普通人类     | 1    |
| Hero        | 人类英雄     | 2    |
| Terminataor | 终结者       | 3    |

## 8. PlayerMdlInfo.FxType 玩家模型特效类型

| 字段英文名   | 字段中文翻译   | 数值 |
| ------------ | -------------- | ---- |
| None         | 无特效         | 0    |
| HumanRespawn | 人类复活特效   | 1    |
| NanoInLowHp  | 生化低血量特效 | 2    |
| Absorbed     | 吸收变身特效   | 3    |

## 9. SkillKey 技能快捷键

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| F          | F键技能      | 0    |
| G          | G键技能      | 1    |
| H          | H键技能      | 2    |
| WW         | 二段位移技能 | 3    |

## 10. PlayerVelocity.VelLockType 玩家速度锁定类型

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| None       | 无锁定       | 0    |
| Map        | 地图区域限速 | 1    |
| Dash       | 冲刺速度锁定 | 2    |

## 11. Player.RespawnType 玩家复活类型

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| Team       | 队内复活     | 0    |
| Stay       | 原地复活     | 1    |
| EnemyTeam  | 敌营复活     | 2    |

## 12. Team 阵营类型

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| BlackList  | 潜伏者       | 0    |
| GlobalRisk | 保卫者       | 1    |
| Neutral    | 中立阵营     | 2    |

## 13. GameMode 游戏模式

| 字段英文名       | 字段中文翻译    | 数值 |
| ---------------- | --------------- | ---- |
| TeamDeath        | 团队竞技        | 0    |
| DeathMatch       | 个人竞技        | 1    |
| Special          | 特殊模式        | 2    |
| Nano3            | 生化3模式       | 3    |
| Nano4            | 生化4模式       | 4    |
| Nano6            | 生化6模式       | 5    |
| Nano4_Terminator | 生化4终结者模式 | 6    |

## 14. HUD_PlayerRect.Type 界面玩家标识类型

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| BL         | 潜伏者标识   | 0    |
| GR         | 保卫者标识   | 1    |
| Dead       | 阵亡标识     | 2    |

## 15. NanoRole 生化角色枚举

| 字段英文名          | 字段中文翻译 | 数值 |
| ------------------- | ------------ | ---- |
| Soldier             | 普通人类     | 0    |
| NanoGhost           | 幽灵生化     | 1    |
| Hulk                | 绿巨人       | 2    |
| Nurse               | 治愈天使     | 3    |
| Assassin            | 暗影刺客     | 4    |
| Ink                 | 迷雾幽灵     | 5    |
| Jiangshi            | 僵尸幽灵     | 6    |
| Psycho              | 疯狂宝贝     | 7    |
| Terminator          | 普通终结者   | 8    |
| GrandTerminator     | 高阶终结者   | 9    |
| ArmoredTerminator   | 装甲终结者   | 10   |
| DevilTerminator     | 恶魔终结者   | 11   |
| ArchDevilTerminator | 炼狱终结者   | 12   |
| EvilTerminator      | 邪恶终结者   | 13   |
| DemonTerminator     | 魔尊终结者   | 14   |
| VoidTerminator      | 虚空终结者   | 15   |
| QueenTerminator     | 女皇终结者   | 16   |
| OutlawTerminator    | 亡命终结者   | 17   |
| Savior              | 救世主       | 18   |
| HumanBoss           | 人类BOSS     | 19   |
| WomanHumanBoss      | 女人类BOSS   | 20   |
| GhostBlade          | 幽灵猎手     | 21   |
| DevilHunter         | 复仇女神     | 22   |
| MasterHumanHero     | 传奇人类英雄 | 23   |
| MasterHunter        | 传奇猎手     | 24   |
| AsceticHero         | 苦修英雄     | 25   |
| MysticHero          | 秘术英雄     | 26   |
| MechanicHero        | 机械英雄     | 27   |

## 16. CommonHud_1.Type 通用UI组件类型

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| Image      | 普通图片     | 0    |
| RawImage   | 原生贴图     | 1    |
| Text       | 文字文本     | 2    |

## 17. HUD_KillMarkUnder.Type 击杀底部标识类型

| 字段英文名    | 字段中文翻译 | 数值 |
| ------------- | ------------ | ---- |
| Common        | 普通击杀     | 0    |
| Melee         | 近战击杀     | 1    |
| Headshot      | 普通爆头     | 2    |
| Headshot_Gold | 黄金爆头     | 3    |

## 18. HUD_ChatBox.Channel 聊天频道

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| All        | 全体频道     | 0    |
| Teammate   | 队伍频道     | 1    |
| Clan       | 战队频道     | 2    |

## 19. HUD_Crosshair.Type 准星类型

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| Common     | 默认准星     | 0    |
| FalCamo    | 迷彩专属准星 | 1    |

## 20. HUD_KillMark.ShowType 击杀提示显示类型

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| Normal     | 图文提示     | 0    |
| OnlyVoice  | 仅语音提示   | 1    |
| None       | 关闭提示     | 2    |

## 21. HUD_Weapon.AmmoBGType 弹药背景样式

| 字段英文名    | 字段中文翻译 | 数值 |
| ------------- | ------------ | ---- |
| None          | 无背景       | 0    |
| Gun           | 枪械弹药背景 | 1    |
| RepeatFireOFF | 连射关闭背景 | 2    |
| RepeatFireOn  | 连射开启背景 | 3    |
| Energy        | 能量弹药背景 | 4    |

## 22. HUD_Role.AceSign ACE标识类型

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| None       | 无标识       | 0    |
| Gray       | 灰色ACE      | 1    |
| Gold       | 金色ACE      | 2    |

## 23. KeyInputState 按键输入状态

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| Unpressed  | 未按下       | 0    |
| Down       | 按下瞬间     | 1    |
| Pressed    | 持续按住     | 2    |
| Up         | 松开按键     | 3    |

## 24. HeadShotType 爆头类型

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| None       | 未爆头       | 0    |
| White      | 普通爆头     | 1    |
| Gold       | 黄金爆头     | 2    |

## 25. SpecialKillType 特殊击杀类型

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| None       | 普通击杀     | 0    |
| FirstKill  | 首杀         | 1    |
| LastKill   | 终结击杀     | 2    |

## 26. NanoKillType 生化特殊击杀

| 字段英文名             | 字段中文翻译 | 数值 |
| ---------------------- | ------------ | ---- |
| None                   | 常规击杀     | 0    |
| NanoKillHero           | 猎手击杀生化 | 1    |
| SoldierKillNanoByKnife | 人类刀杀生化 | 2    |

## 27. WeaponLimited 武器限制类型

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| None       | 无限制       | 0    |
| Knife      | 仅限近战     | 1    |
| HandGun    | 仅限手枪     | 2    |
| Sniper     | 仅限狙击枪   | 3    |

## 28. CharacterModel.MoveDirection 人物移动方向

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| Idle       | 原地静止     | 0    |
| Left       | 向左移动     | 1    |
| Right      | 向右移动     | 2    |
| Forawrd    | 向前移动     | 3    |
| Backward   | 向后移动     | 4    |

## 29. CharacterModel.Sex 人物性别

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| Man        | 男性角色     | 0    |
| Woman      | 女性角色     | 1    |

## 30. Model.Type 模型类型

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| Character  | 人物模型     | 0    |
| PlayerView | 第一人称模型 | 1    |

## 31. SupplyBox.Type 补给箱类型

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| Yellow     | 黄色补给箱   | 0    |
| Red        | 红色补给箱   | 1    |
| Blue       | 蓝色补给箱   | 2    |

## 32. Nano6ModeAsset.UpgradeAsset.TargetPos 生化6升级属性位置

| 字段英文名    | 字段中文翻译 | 数值 |
| ------------- | ------------ | ---- |
| Ammo          | 弹药扩容     | 0    |
| Character     | 人物属性强化 | 1    |
| Radar         | 雷达探测     | 2    |
| HPRegen       | 血量回复     | 3    |
| ThermalVision | 热成像视野   | 4    |

## 33. SO_FxGroup.AttachType 特效挂载类型

| 字段英文名  | 字段中文翻译 | 数值 |
| ----------- | ------------ | ---- |
| NodeAttach  | 骨骼节点挂载 | 0    |
| PlayerView  | 第一人称挂载 | 1    |
| PlayerSpace | 人物空间挂载 | 2    |

## 34. WeaponClass 武器品类

| 字段英文名    | 字段中文翻译 | 数值 |
| ------------- | ------------ | ---- |
| Rifle         | 步枪         | 0    |
| Sniper        | 狙击枪       | 1    |
| MachineGun    | 机枪         | 2    |
| SubmachineGun | 冲锋枪       | 3    |
| ShotGun       | 散弹枪       | 4    |
| Pistol        | 手枪         | 5    |
| Knife         | 近战武器     | 6    |
| Grenade       | 手雷         | 7    |
| FlashBang     | 闪光弹       | 8    |
| SmokeGrenade  | 烟雾弹       | 9    |

## 35. SO_Item.Level 道具品质等级

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| Normal     | 普通道具     | 0    |
| VVIP       | 英雄级道具   | 1    |

## 36. UI_TopMenu.Frame 顶部菜单界面

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| GameRoom   | 游戏房间界面 | 0    |
| Inven      | 仓库背包界面 | 1    |

## 37. ShootPosture 射击姿态

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| StandIdle  | 站立静止     | 0    |
| CrouchIdle | 蹲伏静止     | 1    |
| StandRun   | 站立移动     | 2    |
| CrouchRun  | 蹲伏移动     | 3    |
| Floating   | 悬空姿态     | 4    |

## 38. WPN_Gun.SemiGunFireLinkState 半自动枪械连射状态

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| None       | 无连射       | 0    |
| Try        | 触发连射     | 1    |
| Finish     | 连射结束     | 2    |

## 39. WPN_Knife.KnifeAttackType 近战攻击招式

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| None       | 无攻击       | 0    |
| Combo1     | 轻击第一式   | 1    |
| Combo2     | 轻击第二式   | 2    |
| Bigshot    | 重击招式     | 3    |
| Other      | 特殊招式     | 4    |

## 40. Weapon.SlotType 武器槽位类型

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| Normal     | 常规武器槽   | 0    |
| Special    | 特殊武器槽   | 1    |
| Temporary  | 临时拾取槽   | 2    |
| FKey       | 技能武器槽   | 3    |

## 41. ItemAttribute.Type 道具属性类型

| 字段英文名 | 字段中文翻译 | 数值 |
| ---------- | ------------ | ---- |
| ClipBuff   | 弹容量加成   | 0    |

