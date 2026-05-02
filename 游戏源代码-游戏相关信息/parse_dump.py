import re
import os
import json
import time
import urllib.request
import urllib.parse

INPUT_FILE = r"d:\trae_project\UCF1.7修改大全\游戏源代码-游戏相关信息\Il2CppDumper\dump.cs"
OUTPUT_DIR = r"d:\trae_project\UCF1.7修改大全\游戏源代码-游戏相关信息\类"

# Common programming/game terms dictionary
TERM_DICT = {
    # Unity/Engine
    'Unity': 'Unity引擎', 'Engine': '引擎', 'Component': '组件', 'GameObject': '游戏对象',
    'Transform': '变换', 'Renderer': '渲染器', 'Camera': '摄像机', 'Light': '光照',
    'Audio': '音频', 'Physics': '物理', 'Animation': '动画', 'Particle': '粒子',
    'Sprite': '精灵', 'Texture': '纹理', 'Material': '材质', 'Shader': '着色器',
    'Collider': '碰撞器', 'Rigidbody': '刚体', 'Mesh': '网格', 'Scene': '场景',
    'MonoBehaviour': 'MonoBehaviour行为', 'ScriptableObject': '脚本对象',
    'Animator': '动画器', 'Prefab': '预制体', 'Coroutine': '协程',
    'SerializeField': '序列化字段', 'Header': '标题', 'Range': '范围',
    'Effect': '特效', 'Fx': '特效', 'Mdl': '模型', 'Cmr': '摄像机',
    'CF': '穿越火线', 'CFAnimator': 'CF动画器',
    
    # CF射击游戏专用
    'WPN': '武器', 'Wpn': '武器', 'wpn': '武器',
    'Gun': '枪械', 'Rifle': '步枪', 'Sniper': '狙击枪', 'MachineGun': '机枪',
    'SubmachineGun': '冲锋枪', 'ShotGun': '霰弹枪', 'Pistol': '手枪',
    'Knife': '近战武器', 'Grenade': '手雷', 'FlashBang': '闪光弹',
    'SmokeGrenade': '烟雾弹', 'Throw': '投掷',
    'Clip': '弹匣', 'Ammo': '弹药', 'Bullet': '子弹',
    'Shoot': '射击', 'Shot': '射击', 'Fire': '开火',
    'Reload': '换弹', 'Perturb': '扰动', 'Recoil': '后坐力',
    'Damage': '伤害', 'Brain': '爆头', 'Head': '头部', 'Neck': '颈部',
    'Chest': '胸部', 'Abdomen': '腹部', 'Arm': '手臂', 'Hand': '手部',
    'Leg': '腿部', 'Foot': '脚部', 'Body': '身体',
    'Helmet': '头盔', 'Armor': '护甲', 'Cloth': '服装',
    'WallShot': '穿射', 'Variantion': '变化', 'Factor': '系数',
    'Ratio': '比率', 'Penalty': '惩罚', 'Limited': '限制',
    'Hit': '命中', 'HitEffect': '命中特效', 'HitSound': '命中音效',
    'Sound': '音效', 'Kill': '击杀', 'Death': '死亡', 'KillMsg': '击杀信息',
    'Icon': '图标', 'Select': '选择', 'Bag': '背包', 'Slot': '槽位',
    'ChangeWeapon': '切换武器', 'Rapid': '快速', 'Anim': '动画',
    'Upper': '上半身', 'Lower': '下半身', 'Side': '侧面',
    'Posture': '姿态', 'Stand': '站立', 'Crouch': '蹲下',
    'Idle': '待机', 'Floating': '浮空', 'Air': '空中',
    'Ground': '地面', 'Grounded': '着地', 'Fall': '坠落',
    'Jump': '跳跃', 'Climb': '攀爬', 'Stair': '楼梯',
    'MoveSpeed': '移动速度', 'Acceleration': '加速度',
    'Velocity': '速度', 'Gravity': '重力', 'Power': '力度',
    'Yaw': '偏航角', 'Pitch': '俯仰角', 'EulerAngle': '欧拉角',
    'FOV': '视野', 'Zoom': '瞄准', 'Sniper': '狙击',
    'Crosshair': '准星', 'Sight': '瞄准镜', 'Scope': '瞄准镜',
    'Nano': '纳米', 'NanoGhost': '纳米幽灵', 'NanoRole': '纳米角色',
    'NanoExp': '纳米经验', 'NanoMode': '纳米模式', 'NanoCloth': '纳米服装',
    'NanoInLowHp': '纳米低血量', 'Absorbed': '被吸收',
    'Ghost': '幽灵', 'Blade': '刀锋', 'SecKill': '秒杀',
    'Hero': '英雄', 'Human': '人类', 'Zombie': '僵尸',
    'Mutation': '变异', 'Biochemical': '生化', 'Variant': '变异体',
    'Infection': '感染', 'Survival': '生存',
    'MultiKill': '多杀', 'Ace': '王牌', 'Sign': '标志',
    'Revenge': '复仇', 'Target': '目标', 'Killer': '击杀者',
    'Respawn': '重生', 'Spawn': '出生', 'Born': '出生',
    'Round': '回合', 'Next': '下一个', 'InRound': '回合内',
    'Observe': '观察', 'Observer': '观察者', 'ViewModel': '第一人称模型',
    'Visible': '可见', 'Focus': '聚焦', 'PV': '第一人称',
    'NickName': '昵称', 'VIP': 'VIP', 'Rank': '排名',
    'PlayerID': '玩家ID', 'Client': '客户端', 'ClientData': '客户端数据',
    'Interact': '交互', 'Trigger': '触发器', 'Map': '地图',
    'MapGun': '地图枪械', 'MapTrigger': '地图触发器',
    'MapShadow': '地图阴影', 'Combiner': '组合器',
    'MapAsset': '地图资产', 'DeathMatch': '团队竞技',
    'TeamDeath': '团队歼灭', 'Special': '特殊', 'Nano': '纳米',
    'GameMode': '游戏模式', 'Mode': '模式',
    'Entity': '实体', 'Player': '玩家', 'Character': '角色',
    'CharacterModel': '角色模型', 'CharacterEffect': '角色特效',
    'CharacterVoice': '角色语音', 'CharacterAsset': '角色资产',
    'CharacterContainer': '角色容器', 'CurrentCharacter': '当前角色',
    'PlayerData': '玩家数据', 'PlayerInput': '玩家输入',
    'PlayerWeapons': '玩家武器', 'PlayerController': '玩家控制器',
    'PlayerCamera': '玩家摄像机', 'PlayerMdl': '玩家模型',
    'PlayerSkills': '玩家技能', 'PlayerVelocity': '玩家速度',
    'PlayerRef': '玩家引用', 'PlayerLoop': '玩家循环',
    'PlayerConnection': '玩家连接', 'PlayerEditor': '玩家编辑器',
    'PlayerPrefs': '玩家偏好', 'PlayerLoopSystem': '玩家循环系统',
    'WeaponData': '武器数据', 'WeaponBag': '武器背包',
    'WeaponAsset': '武器资产', 'WeaponLogic': '武器逻辑',
    'WeaponSlot': '武器槽位', 'WeaponSlotPriority': '武器槽位优先级',
    'WeaponClass': '武器类别', 'WpnData': '武器数据',
    'WpnSprite': '武器精灵', 'WpnMdl': '武器模型',
    'Bot': '机器人', 'BotControl': '机器人控制',
    'Bigshot': '爆头', 'BigshotRate': '爆头率',
    'DamageRate': '伤害率', 'DamageBody': '身体伤害',
    'DamageFactor': '伤害系数', 'DamageByDistance': '距离伤害',
    'DamageVariation': '伤害变化', 'DamageRatio': '伤害比率',
    'ArmorRatio': '护甲比率', 'HelmetRatio': '头盔比率',
    'BrainRatio': '爆头比率', 'HeadRatio': '头部比率',
    'NeckRatio': '颈部比率', 'ChestRatio': '胸部比率',
    'AbdomenRatio': '腹部比率', 'ArmRatio': '手臂比率',
    'HandRatio': '手部比率', 'LegRatio': '腿部比率',
    'FootRatio': '脚部比率',
    'ShootPosture': '射击姿态', 'ShootInterval': '射击间隔',
    'ShootBullet': '射出子弹', 'ShotCount': '射击次数',
    'ShotReact': '射击反应', 'ShotSound': '射击音效',
    'ShotReactYaw': '射击反应偏航', 'ShotReactPitch': '射击反应俯仰',
    'ShotPerMinute': '每分钟射击数', 'FireAnim': '开火动画',
    'ReloadAnim': '换弹动画', 'ChangeMoving': '切换移动',
    'RealSize': '实际大小', 'DelayOneShoot': '延迟单发',
    'TimeMin': '最小时间', 'TimeMax': '最大时间',
    'Recover': '恢复', 'Decay': '衰减',
    'DetailPerturb': '详细扰动', 'DetailReact': '详细反应',
    'DetailReactPitch': '详细反应俯仰', 'DetailReactYaw': '详细反应偏航',
    'FullReact': '完全反应', 'FullReactYaw': '完全反应偏航',
    'FullReactPitch': '完全反应俯仰', 'SideReact': '侧面反应',
    'SideReactDirect': '侧面反应方向', 'CameraYaw': '摄像机偏航',
    'CameraPitch': '摄像机俯仰', 'CameraYawAndPitch': '摄像机偏航和俯仰',
    'ZoomAction': '瞄准动作', 'ZoomIn': '瞄准进入',
    'ZoomCamera': '瞄准摄像机', 'ZoomType': '瞄准类型',
    'ZoomSprite': '瞄准精灵', 'GiveUp': '放弃',
    'DeathDrop': '死亡掉落', 'Disable': '禁用',
    'InfinityAmmo': '无限弹药', 'Infinity': '无限',
    'Buff': '增益效果', 'BuffUpdater': '增益更新器',
    'JumpDisabled': '跳跃禁用', 'CameraRot': '摄像机旋转',
    'CameraRotDisabled': '摄像机旋转禁用',
    'Buff_CameraRotDisabled': '增益_摄像机旋转禁用',
    'Buff_JumpDisabled': '增益_跳跃禁用',
    'Buff_InfinityAmmo': '增益_无限弹药',
    'Stun': '眩晕', 'HitStun': '命中眩晕', 'HitAnim': '命中动画',
    'Shake': '震动', 'KnifeHitStun': '刀命中眩晕',
    'KnifeHitStunShake': '刀命中眩晕震动',
    'PlayKnifeHitStunShake': '播放刀命中眩晕震动',
    'LoopShoot': '循环射击', 'MapEffect': '地图特效',
    'MapEffectShooter': '地图特效射击器',
    'DamageType': '伤害类型', 'DamageTypeExpand': '伤害类型扩展',
    'GameModeExpand': '游戏模式扩展',
    'KillMark': '击杀标记', 'KillMarkAsset': '击杀标记资产',
    'Subscribeable': '可订阅的', 'SubscribeableProperty': '可订阅属性',
    'Listener': '监听器', 'Action': '动作',
    'PropertyModifier': '属性修改器', 'Modifier': '修改器',
    'MoveSpeedRatio': '移动速度比率', 'MoveSpeedPenalty': '移动速度惩罚',
    'RefBool': '引用布尔值', 'RefFloat': '引用浮点数',
    'Ref2Float': '双引用浮点数', 'ObscuredInt': '模糊整数',
    'Obscured': '模糊的', 'Property': '属性',
    'KeyInput': '按键输入', 'KeyInputState': '按键输入状态',
    'RightMouse': '鼠标右键', 'JumpButton': '跳跃按钮',
    'InputInteract': '输入交互', 'Input_Interact': '输入_交互',
    'Autonomous': '自主的', 'AutonomousJump': '自主跳跃',
    'JumpPost': '跳跃后', 'JumpDrop': '跳跃掉落',
    'JumpDropSnd': '跳跃掉落音效', 'NextPlayTime': '下次播放时间',
    'LastFallTime': '上次坠落时间', 'HeightBeforeFloat': '浮起前高度',
    'StartMoveTime': '开始移动时间', 'AirVelControl': '空中速度控制',
    'EndTime': '结束时间', 'AirVelControlEndTime': '空中速度控制结束时间',
    'VelData': '速度数据', 'CanControlVel': '能否控制速度',
    'InAir': '在空中', 'CanControlVelInAir': '空中能否控制速度',
    'FallTime': '坠落时间', 'FootPos': '脚部位置',
    'MapCamera': '地图摄像机', 'MapCameraPos': '地图摄像机位置',
    'MapCameraForward': '地图摄像机前方', 'MapCameraHeight': '地图摄像机高度',
    'MapCmr': '地图摄像机', 'MapCmrHeight': '地图摄像机高度',
    'MapCmrCrouchSub': '地图摄像机蹲下减去',
    'CrouchSubHeight': '蹲下减去高度', 'CrouchDuration': '蹲下持续时间',
    'IsCrouching': '是否蹲下', 'Walking': '行走',
    'IsSniper': '是否狙击', 'SpawnPos': '出生位置',
    'IsRespawning': '是否重生中', 'IsMyPlayer': '是否我的玩家',
    'IsFocusPlayer': '是否聚焦玩家', 'IsFocusPlayerInPV': '是否第一人称聚焦玩家',
    'IsNanoGhost': '是否纳米幽灵', 'IsClimbing': '是否攀爬',
    'IsBornNanoGhost': '是否出生为纳米幽灵', 'IsAbsorbed': '是否被吸收',
    'CanPickUpWeapon': '能否拾取武器', 'GhostBladeSecKillTag': '刀锋秒杀标记',
    'NanoDamage': '纳米伤害', 'NanoGhostLevel': '纳米幽灵等级',
    'NanoClothCount': '纳米服装数量', 'LastStopStart': '上次停止开始',
    'LastStopStartTime': '上次停止开始时间', 'NextRegen': '下次再生',
    'NextRegenTime': '下次再生时间', 'RespawnType': '重生类型',
    'Respawn_Coroutine': '重生_协程', 'StartRespawn': '开始重生',
    'NextRespawnInRound': '回合内下次重生',
    'WaitForRespawn': '等待重生', 'g__WaitForRespawn': '等待重生',
    'OrignalCharacterName': '原始角色名称', 'SpawnCount': '出生次数',
    'PlayerViewModelVisible': '玩家第一人称模型可见',
    'MultiKillTimer': '多杀计时器', 'AceSign': '王牌标志',
    'NanoRoleTable': '纳米角色表', 'NanoRoleTableCloseTime': '纳米角色表关闭时间',
    'RevengeTarget': '复仇目标', 'RevengeTarget_Listener': '复仇目标监听器',
    'ObserveMode': '观察模式', 'ObserveMode_Listener': '观察模式监听器',
    'NanoExp_Listener': '纳米经验监听器',
    'CV': '第一人称视角', 'PV': '第三人称视角',
    'CvColor': '第一人称颜色', 'PvColor': '第三人称颜色',
    'CvMatList': '第一人称材质列表', 'PvMatList': '第三人称材质列表',
    'CvRenderers': '第一人称渲染器', 'CvAlpha': '第一人称透明度',
    'Getter_Alpha': '获取_透明度', 'AddMat': '添加材质',
    'RemoveMat': '移除材质', 'UpdateListColor': '更新列表颜色',
    'AddModel': '添加模型', 'RemoveModel': '移除模型',
    'MatData': '材质数据', 'IsTransparent': '是否透明',
    'FxType': '特效类型', 'HumanRespawn': '人类重生',
    'Mat': '材质', 'List': '列表',
    'Singleton': '单例', 'Model': '模型',
    'Type': '类型', 'Color': '颜色',
    'Vector3': '三维向量', 'Vector2': '二维向量',
    'String': '字符串', 'Int': '整数', 'Float': '浮点数',
    'Bool': '布尔值', 'Object': '对象',
    
    # 通用编程
    'Get': '获取', 'Set': '设置', 'Add': '添加', 'Remove': '移除',
    'Create': '创建', 'Destroy': '销毁', 'Enable': '启用', 'Disable': '禁用',
    'Show': '显示', 'Hide': '隐藏', 'Open': '打开', 'Close': '关闭',
    'Play': '播放', 'Stop': '停止', 'Reset': '重置', 'Clear': '清除',
    'Apply': '应用', 'Cancel': '取消', 'Confirm': '确认', 'Check': '检查',
    'Validate': '验证', 'Parse': '解析', 'Format': '格式化',
    'Convert': '转换', 'Clone': '克隆', 'Copy': '复制', 'Move': '移动',
    'Find': '查找', 'Search': '搜索', 'Select': '选择', 'Deselect': '取消选择',
    'Activate': '激活', 'Deactivate': '停用', 'Initialize': '初始化',
    'Dispose': '释放', 'Cleanup': '清理', 'Process': '处理',
    'Execute': '执行', 'Run': '运行', 'Perform': '执行',
    'Handle': '处理', 'Manage': '管理', 'Control': '控制',
    'Update': '更新', 'Refresh': '刷新', 'Sync': '同步',
    'Manager': '管理器', 'Controller': '控制器', 'Handler': '处理器',
    'Provider': '提供者', 'Factory': '工厂', 'Builder': '构建器',
    'Helper': '辅助器', 'Utility': '工具', 'Service': '服务',
    'Module': '模块', 'Plugin': '插件', 'Extension': '扩展',
    'Wrapper': '包装器', 'Adapter': '适配器', 'Proxy': '代理',
    'Buffer': '缓冲区', 'Pool': '池', 'Container': '容器',
    'Node': '节点', 'Element': '元素', 'Item': '项目',
    'Entity': '实体', 'Instance': '实例', 'Reference': '引用',
    'Pointer': '指针', 'Handle': '句柄', 'Token': '令牌',
    'ID': 'ID', 'Name': '名称', 'Value': '值', 'Count': '数量',
    'Index': '索引', 'Key': '键', 'Flag': '标志', 'Mask': '掩码',
    'Layer': '层', 'Group': '组', 'Category': '类别', 'Tag': '标签',
    'Is': '是否', 'Has': '是否有', 'Can': '能否', 'Should': '应该',
    'Need': '需要', 'Want': '想要', 'Allow': '允许', 'Prevent': '阻止',
    'Force': '强制', 'Auto': '自动', 'Manual': '手动',
    'Single': '单个', 'Multi': '多个', 'All': '所有', 'Any': '任意',
    'None': '无', 'Empty': '空', 'Full': '满', 'Max': '最大', 'Min': '最小',
    'First': '第一个', 'Last': '最后一个', 'Next': '下一个', 'Previous': '上一个',
    'Current': '当前', 'Old': '旧的', 'New': '新的', 'Main': '主要的',
    'Sub': '子', 'Extra': '额外的', 'Bonus': '奖励的',
    'Base': '基础', 'Derived': '派生的', 'Abstract': '抽象的',
    'Concrete': '具体的', 'Virtual': '虚拟的', 'Override': '重写',
    'Private': '私有的', 'Public': '公开的', 'Protected': '受保护的',
    'Internal': '内部的', 'External': '外部的',
    'Data': '数据', 'Info': '信息', 'Config': '配置', 'Setting': '设置',
    'State': '状态', 'Mode': '模式', 'Level': '等级', 'Score': '分数',
    'Start': '开始', 'End': '结束', 'Pause': '暂停', 'Resume': '恢复',
    'Init': '初始化', 'Fixed': '固定', 'Late': '延迟',
    'Time': '时间', 'Timer': '计时器', 'Clock': '时钟', 'Duration': '持续时间',
    'Delay': '延迟', 'Interval': '间隔', 'Timeout': '超时', 'Timestamp': '时间戳',
    'Math': '数学', 'Calculate': '计算', 'Random': '随机', 'Angle': '角度',
    'Distance': '距离', 'Direction': '方向', 'Normal': '法线', 'Scale': '缩放',
    'Size': '大小', 'Width': '宽度', 'Height': '高度', 'Depth': '深度',
    'Red': '红色', 'Green': '绿色', 'Blue': '蓝色',
    'Alpha': '透明度', 'RGB': 'RGB颜色', 'HSV': 'HSV颜色',
    'File': '文件', 'Path': '路径', 'Load': '加载', 'Save': '保存',
    'Resource': '资源', 'Asset': '资产', 'Bundle': '捆绑包', 'Cache': '缓存',
    'Stream': '流', 'Reader': '读取器', 'Writer': '写入器',
    'Event': '事件', 'Trigger': '触发器', 'Callback': '回调',
    'Signal': '信号', 'Delegate': '委托',
    'Network': '网络', 'Server': '服务器', 'Connection': '连接',
    'Socket': '套接字', 'Request': '请求', 'Response': '响应', 'Packet': '数据包',
    'Async': '异步', 'Send': '发送', 'Receive': '接收',
    'Input': '输入', 'Mouse': '鼠标', 'Touch': '触摸',
    'Keyboard': '键盘', 'Joystick': '摇杆', 'Button': '按钮', 'Axis': '轴',
    'UI': '界面', 'Text': '文本', 'Image': '图像',
    'Panel': '面板', 'Menu': '菜单', 'Dialog': '对话框', 'Popup': '弹窗',
    'Label': '标签', 'Slider': '滑块', 'Toggle': '开关',
    'Grid': '网格', 'Scroll': '滚动', 'View': '视图',
    'Screen': '屏幕', 'Canvas': '画布', 'HUD': '抬头显示',
    'Array': '数组', 'Dictionary': '字典', 'Map': '映射', 'Set': '集合',
    'Queue': '队列', 'Stack': '栈', 'Class': '类', 'Type': '类型',
    'Matrix': '矩阵', 'Vector': '向量',
    'Active': '激活的', 'Visible': '可见的', 'Enabled': '启用的',
    'Locked': '锁定的', 'Selected': '选中的', 'Focused': '聚焦的',
    'Hover': '悬停', 'Pressed': '按下的', 'Disabled': '禁用的',
    'Hidden': '隐藏的', 'Transparent': '透明的', 'Opaque': '不透明的',
    'Static': '静态的', 'Dynamic': '动态的', 'Persistent': '持久的',
    'Temporary': '临时的', 'Default': '默认的', 'Custom': '自定义的',
    'Global': '全局的', 'Local': '局部的', 'World': '世界的',
    'Screen': '屏幕的', 'Local': '本地的', 'Parent': '父级',
    'Child': '子级', 'Root': '根', 'Top': '顶部', 'Bottom': '底部',
    'Left': '左', 'Right': '右', 'Center': '中心', 'Middle': '中间',
    'Front': '前', 'Back': '后', 'Forward': '前进', 'Backward': '后退',
    'Up': '上', 'Down': '下', 'Vertical': '垂直', 'Horizontal': '水平',
    'Buff': '增益', 'Debuff': '减益', 'Skill': '技能', 'Ability': '能力',
    'Equipment': '装备', 'Inventory': '背包',
    'Shop': '商店', 'Store': '商店', 'Purchase': '购买', 'Sell': '出售',
    'Quest': '任务', 'Mission': '任务', 'Achievement': '成就',
    'Reward': '奖励', 'Prize': '奖品', 'Coin': '金币', 'Currency': '货币',
    'Experience': '经验', 'EXP': '经验', 'Level': '等级', 'Rank': '排名',
    'Star': '星', 'Medal': '奖牌', 'Trophy': '奖杯',
    'Team': '队伍', 'Room': '房间', 'Lobby': '大厅',
    'Match': '比赛', 'Game': '游戏', 'System': '系统',
}

def split_camel(name):
    """Split CamelCase into words"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1)

def translate_name(name):
    """Translate a name using dictionary + camelCase splitting"""
    if not name or name == '.ctor':
        return '构造函数'
    if name == '.cctor':
        return '静态构造函数'
    
    # Try exact match first
    if name in TERM_DICT:
        return TERM_DICT[name]
    
    # Split camelCase
    words = split_camel(name).split()
    
    translated_words = []
    for word in words:
        if word in TERM_DICT:
            translated_words.append(TERM_DICT[word])
        else:
            translated_words.append(word)
    
    return ''.join(translated_words)

def translate_params(params_str):
    """Translate parameter types in method signature"""
    if not params_str:
        return ''
    
    parts = []
    for param in params_str.split(','):
        param = param.strip()
        if not param:
            continue
        # Handle "Type paramName" format
        tokens = param.split()
        if len(tokens) >= 2:
            type_name = tokens[0]
            param_name = ' '.join(tokens[1:])
            translated_type = translate_name(type_name)
            parts.append(f'{translated_type} {param_name}')
        else:
            parts.append(translate_name(param))
    
    return ', '.join(parts)

# Parse dump.cs
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

class_decl_indices = []
for i, line in enumerate(lines):
    if '// TypeDefIndex:' in line and ('class ' in line or 'struct ' in line or 'interface ' in line or 'enum ' in line):
        class_decl_indices.append(i)

print(f"Found {len(class_decl_indices)} class declarations")

classes = []
for idx in class_decl_indices:
    decl_line = lines[idx]
    
    name_match = re.search(r'(?:class|struct|interface|enum)\s+(\S+)', decl_line)
    if not name_match:
        continue
    class_name = name_match.group(1)
    
    inherit_match = re.search(r':\s*([^/]+)//', decl_line)
    inheritance = inherit_match.group(1).strip() if inherit_match else ''
    
    brace_start = -1
    for j in range(idx, min(idx + 3, len(lines))):
        if '{' in lines[j]:
            brace_start = j
            break
    
    if brace_start == -1:
        continue
    
    depth = 0
    brace_end = -1
    for j in range(brace_start, len(lines)):
        depth += lines[j].count('{') - lines[j].count('}')
        if depth == 0:
            brace_end = j
            break
    
    if brace_end == -1:
        continue
    
    body_lines = lines[brace_start+1:brace_end]
    body_text = '\n'.join(body_lines)
    
    fields = []
    field_pattern = re.compile(
        r'(?:private|public|protected|internal)\s+(?:static\s+|readonly\s+)*(?:const\s+)?'
        r'([\w<>\[\]\*]+(?:\.[\w<>\[\]\*]+)*)\s+'
        r'(\w+)\s*;\s*//\s*0x([0-9A-Fa-f]+)'
    )
    for fm in field_pattern.finditer(body_text):
        fields.append({
            'type': fm.group(1),
            'name': fm.group(2),
            'offset': fm.group(3)
        })
    
    methods = []
    method_pattern = re.compile(
        r'(?:public|private|protected|internal)\s+'
        r'(?:static\s+|override\s+|virtual\s+|abstract\s+|sealed\s+extern\s+|extern\s+)*'
        r'([\w<>\[\]\*]+(?:\.[\w<>\[\]\*]+)*)\s+'
        r'(\w+)\s*\(([^)]*)\)\s*\{'
    )
    for mm in method_pattern.finditer(body_text):
        methods.append({
            'return_type': mm.group(1),
            'name': mm.group(2),
            'params': mm.group(3).strip()
        })
    
    if fields or methods:
        if '<' not in class_name and '>' not in class_name:
            classes.append({
                'name': class_name,
                'inheritance': inheritance,
                'fields': fields,
                'methods': methods
            })

classes.sort(key=lambda c: c['name'])

total = len(classes)
print(f"Parsed {total} classes, generating translations...")

# Split into chunks
CHUNK_SIZE = 200
num_files = (total + CHUNK_SIZE - 1) // CHUNK_SIZE

for i in range(0, total, CHUNK_SIZE):
    chunk = classes[i:i+CHUNK_SIZE]
    file_num = i // CHUNK_SIZE + 1
    filename = f"classes_part{file_num:03d}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# 游戏类定义 (Part {file_num}/{num_files})\n\n")
        f.write(f"共 {len(chunk)} 个类 (总序号 {i+1} - {min(i+CHUNK_SIZE, total)})\n\n")
        f.write("---\n\n")
        
        for cls in chunk:
            cls_trans = translate_name(cls['name'])
            f.write(f"## {cls['name']}（{cls_trans}）\n\n")
            
            if cls['inheritance']:
                inherit_parts = [p.strip() for p in cls['inheritance'].split(',')]
                inherit_trans = ', '.join([translate_name(p) for p in inherit_parts])
                f.write(f"**继承**: {cls['inheritance']}（{inherit_trans}）\n\n")
            
            if cls['fields']:
                f.write(f"### 字段 ({len(cls['fields'])})\n\n")
                for field in cls['fields']:
                    type_trans = translate_name(field['type'])
                    name_trans = translate_name(field['name'])
                    f.write(f"- `{field['type']} {field['name']}`（{type_trans} {name_trans}）(偏移: 0x{field['offset']})\n")
                f.write("\n")
            
            if cls['methods']:
                f.write(f"### 方法 ({len(cls['methods'])})\n\n")
                for method in cls['methods']:
                    rt_trans = translate_name(method['return_type'])
                    name_trans = translate_name(method['name'])
                    params_trans = translate_params(method['params'])
                    f.write(f"- `{method['return_type']} {method['name']}({method['params']})`\n  （{rt_trans} {name_trans}（{params_trans}））\n")
                f.write("\n")
            
            f.write("---\n\n")
    
    print(f"  Written: {filename} ({len(chunk)} classes)")

print(f"\nDone! Generated {num_files} files in {OUTPUT_DIR}")
