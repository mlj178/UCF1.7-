# -*- coding: utf-8 -*-
import re

# FPS射击游戏高频单词翻译表
word_translations = {
    'map': '地图', 'camera': '摄像机', 'pos': '位置', 'forward': '前方', 'character': '角色',
    'container': '容器', 'current': '当前', 'foot': '脚', 'autonomous': '自动', 'jump': '跳跃',
    'grounded': '着地', 'ground': '地面', 'mat': '材质', 'name': '名称', 'fall': '下落',
    'time': '时间', 'can': '能否', 'control': '控制', 'vel': '速度', 'air': '空中',
    'velocity': '速度', 'move': '移动', 'speed': '速度', 'ratio': '比率', 'data': '数据',
    'player': '玩家', 'input': '输入', 'wpns': '武器', 'weapon': '武器', 'bag': '背包',
    'model': '模型', 'info': '信息', 'sniper': '狙击手', 'spawn': '出生', 'respawning': '重生中',
    'my': '我的', 'focus': '焦点', 'pv': 'PV', 'nano': '纳米', 'ghost': '幽灵',
    'crouch': '蹲下', 'duration': '持续时间', 'crouching': '蹲下中', 'walking': '行走中',
    'cloth': '服装', 'count': '数量', 'interact': '交互', 'key': '键', 'state': '状态',
    'interactable': '可交互', 'set': '设置', 'value': '值', 'exist': '存在',
    'existent': '已存在', 'color': '颜色', 'physical': '物理', 'update': '更新',
    'btn': '按钮', 'down': '按下', 'get': '获取', 'by': '通过', 'local': '本地',
    'direction': '方向', 'add': '添加', 'rotation': '旋转', 'look': '看', 'at': '朝向',
    'recoil': '后坐力', 'shoot': '射击', 'posture': '姿态', 'check': '检查', 'entity': '实体',
    'hurt': '受伤', 'death': '死亡', 'clear': '清除', 'mapObject': '地图物体', 'drop': '掉落',
    'after': '后', 'send': '发送', 'fire': '开火', 'in': '在', 'hole': '洞', 'radio': '语音',
    'remove': '移除', 'from': '从', 'team': '队伍', 'list': '列表', 'to': '到',
    'break': '中断', 'coroutine': '协程', 'on': '当', 'game': '游戏', 'round': '回合',
    'end': '结束', 'select': '选择', 'try': '尝试', 'pick': '拾取', 'up': '上',
    'walk': '行走', 'sub': '减去', 'skill': '技能', 'hp': 'HP', 'cost': '消耗',
    'stop': '停止', 'regen': '回复', 'fill': '填充', 'ammo': '弹药', 'trigger': '触发器',
    'enter': '进入', 'exit': '退出', 'ace': '王牌', 'reset': '重置', 'dropSnd': '掉落音效',
    'run': '奔跑', 'buff': '增益', 'property': '属性', 'next': '下次', 'invincible': '无敌',
    'visible': '可见', 'hit': '命中', 'box': '框', 'base': '基础', 'is': '是否',
    'no': '无', 'feedback': '反馈', 'penalty': '惩罚', 'rate': '比率', 'health': '生命',
    'dead': '死亡', 'black': '黑名单', 'global': '全局', 'risk': '风险', 'animator': '动画器',
    'controller': '控制器', 'inverse': '反向', 'only': '仅', 'alive': '存活', 'clean': '清除',
    'all': '全部', 'find': '查找', 'soldier': '士兵', 'savior': '救世主', 'like': '类似',
    'guard': '守卫', 'human': '人类', 'hero': '英雄', 'normal': '普通', 'master': '大师',
    'terminator': '终结者', 'use': '使用', 'anim': '动画', 'generate': '生成', 'owner': '所有者',
    'recycle': '回收', 'deploy': '部署', 'un': '取消', 'mode': '模式', 'view': '视角',
    'setting': '设置', 'sync': '同步', 'hand': '手', 'crosshair': '准星', 'char': '角色',
    'pool': '池', 'fireBtn': '开火按钮', 'pressed': '按下', 'unPressed': '松开',
    'special': '特殊', 'reload': '换弹', 'bool': '布尔', 'integer': '整数', 'cross': '交叉',
    'fade': '淡入', 'fixed': '固定', 'knife': '刀', 'call': '调用', 'spr': '精灵',
    'idx': '索引', 'dmg': '伤害', 'event': '事件', 'should': '应该', 'give': '给予',
    'bot': '机器人', 'charShoot': '角色射击', 'wpn': '武器', 'sprite': '精灵',
    'infinity': '无限', 'this': '这个', 'consume': '消耗', 'basic': '基础', 'gun': '枪',
    'over': '结束', 'pre': '预', 'effect': '特效', 'stopFire': '停火', 'start': '开始',
    'gen': '生成', 'bullet': '子弹', 'zoom': '瞄准', 'close': '关闭', 'func': '函数',
    'frame': '帧', 'auto': '自动', 'stopFire': '停火', 'collision': '碰撞', 'throw': '投掷',
    'explode': '爆炸', 'exp': '爆炸', 'snd': '音效', 'cause': '造成', 'missile': '导弹',
    'target': '目标', 'fly': '飞行', 'take': '承受', 'place': '生效', 'print': '打印',
    'rot': '旋转', 'modify': '修改', 'offset': '偏移', 'fbik': 'FBBIK', 'aim': '瞄准',
    'ik': 'IK', 'life': '生命', 'refresh': '刷新', 'timeout': '超时', 'cold': '冷却',
    'finish': '完成', 'basicCheck': '基础检查', 'playerSpawn': '玩家出生', 'setPlayer': '设置玩家',
    'startCold': '开始冷却', 'endCold': '结束冷却', 'speedUpdate': '速度更新',
    'dmgRate': '伤害比率', 'alpha': '透明度', 'hangout': '聚集', 'gizmos': 'Gizmos',
    'nearest': '最近', 'node': '节点', 'path': '路径', 'reach': '到达', 'dist': '距离',
    'complete': '完成', 'jumpCheck': '跳跃检查', 'tryCrouch': '尝试蹲下', 'moveState': '移动状态',
    'camRot': '摄像机旋转', 'lifeChange': '生命改变', 'takeDmg': '承受伤害', 'delay': '延迟',
    'guard': '守卫', 'area': '区域', 'attack': '攻击', 'checkTarget': '检查目标',
    'useWpn': '使用武器', 'selectWpn': '选择武器', 'wpnAction': '武器动作', 'useSkill': '使用技能',
    'role': '角色', 'change': '改变', 'updateAction': '更新动作', 'table': '表', 'type': '类型',
    'playerSkill': '玩家技能', 'pathLength': '路径长度', 'ghostEntity': '幽灵实体', 'zoomDir': '缩放方向',
    'setAbility': '设置能力', 'gunDist': '枪械距离', 'knifeDist': '刀具距离', 'waitKnife': '等待刀击',
    'doAction': '执行动作', 'nextCheck': '下次检查', 'tryGetAce': '尝试获取王牌', 'resetRound': '重置回合',
    'restRound': '休息回合', 'addPlayers': '添加玩家', 'test': '测试', 'addPlayer': '添加玩家',
    'spareIdx': '备用索引', 'loadWpn': '加载武器', 'giveWpn': '给予武器', 'byBag': '通过背包',
    'getWpn': '获取武器', 'wpnData': '武器数据', 'getChar': '获取角色', 'deathEvent': '死亡事件',
    'returnLobby': '返回大厅', 'roundEnd': '回合结束', 'recycleObj': '可回收物体', 'clearRecycle': '清除可回收',
    'mapGunInit': '地图枪械初始化', 'newRound': '新回合', 'spawnPoint': '出生点', 'supplyBox': '补给箱',
    'releaseBox': '释放箱子', 'active': '激活', 'playerExit': '玩家退出', 'mapWpnRecycle': '地图武器回收',
    'resetEuler': '重置欧拉角', 'canInteract': '能否交互', 'tipSprite': '提示精灵', 'canPickUp': '能否拾取',
    'redBox': '红盒', 'work': '工作', 'boxList': '箱子列表', 'randomBox': '随机箱子', 'nearestBox': '最近箱子',
    'clearBox': '清除箱子', 'boxType': '箱子类型', 'pixel': '像素', 'radar': '雷达', 'originPos': '原点位置',
    'perDistance': '每距离', 'weaponMdl': '武器模型', 'onPlayerExit': '玩家退出', 'mapWpn': '地图武器',
    'cameraPos': '摄像机位置', 'cameraForward': '摄像机前方向', 'characterContainer': '角色容器',
    'currentCharacter': '当前角色', 'footPos': '脚部位置', 'autonomousJump': '自动跳跃',
    'isGrounded': '是否着地', 'groundMatName': '地面材质名称', 'fallTime': '下落时间',
    'canControlVelInAir': '能否在空中控制速度', 'moveSpeedRatio': '移动速度比率',
    'velData': '速度数据', 'playerData': '玩家数据', 'weaponBag': '武器背包', 'modelInfo': '模型信息',
    'isSniper': '是否狙击手', 'spawnPos': '出生位置', 'isRespawning': '是否重生中',
    'isMyPlayer': '是否我的玩家', 'isFocusPlayer': '是否焦点玩家', 'isFocusPlayerInPV': '是否PV中焦点玩家',
    'isNanoGhost': '是否纳米幽灵', 'crouchDuration': '蹲下持续时间', 'isCrouching': '是否蹲下中',
    'isWalking': '是否行走中', 'nanoClothCount': '纳米服装数量', 'inputInteract': '交互输入',
    'isInteractable': '是否可交互', 'existCharacter': '已存在角色', 'characterModelSetting': '角色模型设置',
    'modelColor': '模型颜色', 'groundState': '地面状态', 'jumpBtn': '跳跃按钮', 'moveSpeed': '移动速度',
    'cameraRotation': '摄像机旋转', 'weapon': '武器', 'recoilShootPostureCheck': '后坐力射击姿态检查',
    'entityHurt': '实体受伤', 'entityDeath': '实体死亡', 'mapObject': '地图物体', 'weaponAfterDeath': '死亡后武器',
    'fireInTheHoleRadio': '投掷物语音', 'teamList': '队伍列表', 'respawn': '重生', 'respawnCoroutine': '重生协程',
    'weaponBag': '武器背包', 'weapon': '武器', 'crouchState': '蹲下状态', 'walkState': '行走状态',
    'subSkillHPCost': '技能HP消耗', 'stopTime': '停止时间', 'nanoGhostHPRegen': '纳米幽灵HP回复',
    'nanoClothCount': '纳米服装数量', 'interactInput': '交互输入', 'mapGunAmmo': '地图枪械弹药',
    'triggerEnter': '触发器进入', 'triggerExit': '触发器退出', 'updateAce': '更新王牌',
    'dropSndTime': '掉落音效时间', 'fallTime': '下落时间', 'runState': '奔跑状态',
    'buffProperty': '增益属性', 'nextRespawnInvincible': '下次重生无敌', 'visibleHitBox': '可见命中框',
    'baseMoveSpeed': '基础移动速度', 'isGhostEntity': '是否幽灵实体', 'isNoHitFeedback': '是否无命中反馈',
    'speedPenaltyUpdater': '速度惩罚更新器', 'damageRateUpdater': '伤害比率更新器', 'invincibleUpdater': '无敌更新器',
    'speedPenalty': '速度惩罚', 'damageRate': '伤害比率', 'isInvincible': '是否无敌', 'healthData': '生命数据',
    'isDead': '是否死亡', 'isBlackList': '是否黑名单', 'isGlobalRisk': '是否全局风险',
    'characterAnimator': '角色动画器', 'characterController': '角色控制器', 'localDirection': '本地方向',
    'removeBuff': '移除增益', 'cleanAllBuff': '清除所有增益', 'findBuff': '查找增益', 'addBuff': '添加增益',
    'tryAddBuff': '尝试添加增益', 'updateBuff': '更新增益', 'updateBuffProperty': '更新增益属性',
    'setGhostEntityState': '设置幽灵实体状态', 'getVisibleHitBox': '获取可见命中框',
    'ownerLifeStateListener': '所有者生命状态监听', 'tryUse': '尝试使用', 'remove': '移除',
    'isSoldier': '是否士兵', 'isSavior': '是否救世主', 'isLikeGuard': '是否类似守卫', 'isHuman': '是否人类',
    'isHero': '是否英雄', 'isNormalHero': '是否普通英雄', 'isMasterHero': '是否大师英雄', 'isNormalNano': '是否普通纳米',
    'isTerminator': '是否终结者', 'isNormalTerminator': '是否普通终结者', 'isMasterTerminator': '是否大师终结者',
    'removeAll': '移除全部', 'canUse': '能否使用', 'animEnd': '动画结束', 'animExit': '动画退出', 'generate': '生成',
    'fromOwner': '从所有者', 'recycle': '回收', 'deploy': '部署', 'unDeploy': '取消部署', 'resetMode': '重置模式',
    'viewSetting': '视图设置', 'syncHand': '同步手部', 'animSpeed': '动画速度', 'crosshair': '准星',
    'charAnim': '角色动画', 'fromPool': '从武器池', 'fireBtn': '开火按钮', 'pressed': '按住', 'unPressed': '松开',
    'specialBtn': '特殊按钮', 'reloadBtn': '换弹按钮', 'bool': '布尔值', 'integer': '整数', 'crossFade': '交叉淡入',
    'fixedTime': '固定时间', 'knifeData': '刀击数据', 'callKnife': '调用刀击', 'sprIndex': '精灵索引',
    'dmgEvent': '伤害事件', 'shouldDmg': '是否应伤害', 'giveUp': '丢弃', 'botControl': '机器人控制',
    'charShoot': '角色射击', 'wpnName': '武器名称', 'wpnSprite': '武器精灵', 'charWpn': '角色武器',
    'animData': '动画数据', 'infinityAmmo': '无限弹药', 'thisWpn': '此武器', 'consume': '消耗',
    'animReload': '换弹动画', 'basicRecoil': '基础后坐力', 'recoilData': '后坐力数据', 'gunFire': '枪械开火',
    'tryReload': '尝试换弹', 'canReload': '能否换弹', 'reloadOver': '换弹结束', 'preReload': '预换弹',
    'fillAmmo': '填充弹药', 'addAmmo': '添加弹药', 'gunFireEffect': '枪口火焰', 'stopFire': '停止开火',
    'knifeEvent': '刀击事件', 'startKnife': '开始刀击', 'knifeExit': '刀击退出', 'genBullet': '生成子弹',
    'useZoom': '使用缩放', 'closeZoom': '关闭缩放', 'fireAnim': '开火动画', 'gunShoot': '枪械射击',
    'noCheck': '无检查', 'shootLogic': '射击逻辑', 'shootFunc': '射击函数', 'nextFrame': '下一帧',
    'autoFire': '自动开火', 'autoStop': '自动停火', 'sniperBot': '狙击机器人', 'collision': '碰撞',
    'throwAnim': '投掷动画', 'throw': '投掷', 'explode': '爆炸', 'expEffect': '爆炸特效', 'expSound': '爆炸音效',
    'causeDmg': '造成伤害', 'missile': '导弹', 'target': '目标', 'flyAnim': '飞行动画', 'updateMissile': '更新导弹',
    'knifeAnim': '刀击动画', 'takePlace': '生效', 'print': '打印', 'handRot': '手部旋转', 'modifyOffset': '修改偏移',
    'afterFBBIK': 'FBBIK后', 'afterAimIK': 'AimIK后', 'lifeEnd': '生命结束', 'endTime': '结束时间',
    'refreshTime': '刷新时间', 'timeout': '超时', 'coldFinish': '冷却完成', 'spriteIdx': '精灵索引',
    'basicCheck': '基础检查', 'onPlayerSpawn': '玩家重生', 'onSetPlayer': '设置到玩家', 'startCold': '开始冷却',
    'endCold': '结束冷却', 'speedUpdate': '速度更新', 'dmgRateUpdate': '伤害比率更新', 'modelAlpha': '模型透明度',
    'hangoutCount': '聚集数量', 'gizmos': 'Gizmos', 'nearestNode': '最近节点', 'pathSetting': '路径设置',
    'reachDist': '可达距离', 'pathComplete': '路径完成', 'jumpCheck': '跳跃检查', 'tryCrouch': '尝试蹲下',
    'moveState': '移动状态', 'camRot': '摄像机旋转', 'lifeChange': '生命改变', 'takeDmg': '承受伤害',
    'spawnDelay': '生成延迟', 'nanoGuard': '纳米守卫', 'guardArea': '守卫区域', 'attackTarget': '攻击目标',
    'checkTarget': '检查目标', 'useWpn': '使用武器', 'selectWpn': '选择武器', 'wpnAction': '武器动作',
    'useSkill': '使用技能', 'roleChange': '角色改变', 'updateAction': '更新动作', 'tableType': '表类型',
    'playerSkill': '玩家技能', 'pathLength': '路径长度', 'ghostEntity': '幽灵实体', 'zoomDir': '缩放方向',
    'setAbility': '设置能力', 'gunDist': '枪械距离', 'knifeDist': '刀具距离', 'waitKnife': '等待刀击',
    'doAction': '执行动作', 'nextCheck': '下次检查', 'tryGetAce': '尝试获取王牌', 'resetRound': '重置回合',
    'restRound': '休息回合', 'addPlayers': '添加玩家', 'test': '测试', 'addPlayer': '添加玩家',
    'spareIdx': '备用索引', 'loadWpn': '加载武器', 'giveWpn': '给予武器', 'byBag': '通过背包',
    'getWpn': '获取武器', 'wpnData': '武器数据', 'getChar': '获取角色', 'deathEvent': '死亡事件',
    'returnLobby': '返回大厅', 'roundEnd': '回合结束', 'recycleObj': '可回收物体', 'clearRecycle': '清除可回收',
    'mapGunInit': '地图枪械初始化', 'newRound': '新回合', 'spawnPoint': '出生点', 'supplyBox': '补给箱',
    'releaseBox': '释放箱子', 'active': '激活', 'playerExit': '玩家退出', 'mapWpnRecycle': '地图武器回收',
    'resetEuler': '重置欧拉角', 'canInteract': '能否交互', 'tipSprite': '提示精灵', 'canPickUp': '能否拾取',
    'redBox': '红盒', 'work': '工作', 'boxList': '箱子列表', 'randomBox': '随机箱子', 'nearestBox': '最近箱子',
    'clearBox': '清除箱子', 'boxType': '箱子类型', 'pixel': '像素', 'radar': '雷达', 'originPos': '原点位置',
    'perDistance': '每距离', 'weaponMdl': '武器模型', 'onPlayerExit': '玩家退出', 'mapWpn': '地图武器',
    'gravity': '重力', 'manager': '管理器', 'characters': '角色列表', 'obj': '物体', 'play': '播放',
    'before': '之前', 'client': '客户端', 'skills': '技能', 'nextRegen': '下次回复', 'cameraRot': '摄像机旋转',
    'cameraRotDisabled': '摄像机旋转禁用', 'jumpDisabled': '跳跃禁用', 'mapCamera': '地图摄像机',
    'mapCameraPos': '地图摄像机位置', 'mapCameraForward': '地图摄像机前方向', 'characterContainer': '角色容器',
    'currentCharacter': '当前角色模型', 'footPos': '脚部位置', 'autonomousJump': '自动跳跃',
    'isGrounded': '是否着地', 'groundMatName': '地面材质名称', 'fallTime': '下落时间',
    'canControlVelInAir': '能否在空中控制速度', 'velocity': '速度', 'moveSpeedRatio': '移动速度比率',
    'velData': '速度数据', 'playerData': '玩家数据', 'input': '输入', 'wpns': '武器',
    'weaponBag': '武器背包', 'modelInfo': '模型信息', 'isSniper': '是否狙击手', 'spawnPos': '出生位置',
    'isRespawning': '是否正在重生', 'isMyPlayer': '是否我的玩家', 'isFocusPlayer': '是否焦点玩家',
    'isFocusPlayerInPV': '是否在PV中的焦点玩家', 'isNanoGhost': '是否纳米幽灵', 'crouchDuration': '蹲下持续时间',
    'isCrouching': '是否蹲下中', 'walking': '是否行走中', 'nanoClothCount': '纳米服装数量',
    'inputInteract': '交互输入', 'mapGunAmmo': '地图枪械弹药', 'climbStair': '爬楼梯',
    'isClimbing': '是否攀爬中', 'buffJumpDisabled': '跳跃禁用增益', 'nickName': '昵称', 'vipLevel': 'VIP等级',
    'survival': '生存', 'score': '分数', 'aceSign': '王牌标志', 'nanoRole': '纳米角色',
    'fixedUpdate': '固定帧更新', 'updateGroundMatName': '更新地面材质名称', 'characterModelSetting': '角色模型设置',
    'setExistentCharacter': '设置已存在角色', 'setCharacter': '设置角色', 'updateModelColor': '更新模型颜色',
    'physicalUpdate': '物理更新', 'setGroundState': '设置地面状态', 'onJumpBtnDown': '跳跃按钮按下',
    'getMoveSpeed': '获取移动速度', 'moveByLocalDirection': '按本地方向移动', 'getCameraRotation': '获取摄像机旋转',
    'addCameraRotation': '添加摄像机旋转', 'updateCameraRotation': '更新摄像机旋转', 'lookAt': '看向',
    'setWeapon': '设置武器', 'recoilShootPostureCheck': '后坐力射击姿态检查', 'onEntityHurt': '实体受伤',
    'onEntityDeath': '实体死亡', 'clearMapObject': '清除地图物体', 'dropWeaponAfterDeath': '死亡后丢弃武器',
    'sendFireInTheHoleRadio': '发送投掷物语音', 'removeFromTeamList': '从队伍列表移除', 'addToTeamList': '添加到队伍列表',
    'respawn': '重生', 'breakRespawnCoroutine': '中断重生协程', 'spawn': '生成', 'onGameRoundEnd': '回合结束',
    'setPos': '设置位置', 'selectWeaponBag': '选择武器包', 'tryPickUpWeapon': '尝试拾取武器', 'setCrouchState': '设置蹲下状态',
    'setWalkState': '设置行走状态', 'trySubSkillHPCost': '尝试扣除技能HP消耗', 'breakStopTime': '中断停止时间',
    'nanoGhostHPRegen': '纳米幽灵HP回复', 'setNanoClothCount': '设置纳米服装数量', 'addNanoClothCount': '增加纳米服装数量',
    'setInteractInput': '设置交互输入', 'fillMapGunAmmo': '填充地图枪械弹药', 'onTriggerEnter': '进入触发器',
    'onTriggerExit': '退出触发器', 'updateAce': '更新王牌', 'resetDropSndTime': '重置掉落音效时间',
    'updateFallTime': '更新下落时间', 'updateRunState': '更新奔跑状态', 'updateBuffProperty': '更新增益属性',
    'addNextRespawnInvincible': '添加下次重生无敌', 'getVisibleHitBox': '获取可见命中框',
    'baseMoveSpeed': '基础移动速度', 'isGhostEntity': '是否幽灵实体', 'isNoHitFeedback': '是否无命中反馈',
    'speedPenaltyUpdater': '速度惩罚更新器', 'damageRateUpdater': '伤害比率更新器', 'invincibleUpdater': '无敌更新器',
    'speedPenalty': '速度惩罚', 'damageRate': '伤害比率', 'isInvincible': '是否无敌', 'healthData': '生命数据',
    'isDead': '是否死亡', 'isBlackList': '是否黑名单', 'isGlobalRisk': '是否全局风险', 'team': '队伍',
    'characterAnimator': '角色动画器', 'characterController': '角色控制器', 'setTeam': '设置队伍',
    'removeFromTeamList': '从队伍列表移除', 'addToTeamList': '添加到队伍列表', 'getLocalDirection': '获取本地方向',
    'spawn': '生成', 'onEntityHurt': '实体受伤', 'onEntityDeath': '实体死亡', 'addSpeedPenalty': '添加速度惩罚',
    'setDamageRate': '设置伤害比率', 'removeBuff': '移除增益', 'cleanAllBuff': '清除所有增益', 'findBuff': '查找增益',
    'addBuff': '添加增益', 'tryAddBuff': '尝试添加增益', 'updateBuff': '更新增益', 'updateBuffProperty': '更新增益属性',
    'setGhostEntityState': '设置幽灵实体状态', 'getVisibleHitBox': '获取可见命中框',
}

def translate_by_words(name):
    """根据单词翻译名称"""
    if name in word_translations:
        return word_translations[name]
    parts = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|[0-9]|\b)|\d+', name)
    translations = []
    for part in parts:
        if part.lower() in word_translations:
            translations.append(word_translations[part.lower()])
        else:
            translations.append(part)
    return ''.join(translations) if translations else name

def translate_method_name(method_name):
    """翻译方法名"""
    if method_name.startswith('get_'):
        prop = method_name[4:]
        return f'获取{translate_by_words(prop)}'
    elif method_name.startswith('set_'):
        prop = method_name[4:]
        return f'设置{translate_by_words(prop)}'
    elif method_name.startswith('On'):
        return translate_by_words(method_name)
    elif method_name.startswith('Try'):
        return translate_by_words(method_name)
    elif method_name.startswith('Add'):
        return translate_by_words(method_name)
    elif method_name.startswith('Update'):
        return translate_by_words(method_name)
    elif method_name.startswith('Set'):
        return translate_by_words(method_name)
    elif method_name.startswith('Remove'):
        return translate_by_words(method_name)
    elif method_name.startswith('Clear'):
        return translate_by_words(method_name)
    elif method_name.startswith('Find'):
        return translate_by_words(method_name)
    elif method_name.startswith('Select'):
        return translate_by_words(method_name)
    elif method_name.startswith('Spawn'):
        return translate_by_words(method_name)
    elif method_name.startswith('Break'):
        return translate_by_words(method_name)
    elif method_name.startswith('Reset'):
        return translate_by_words(method_name)
    elif method_name.startswith('Fill'):
        return translate_by_words(method_name)
    elif method_name.startswith('Drop'):
        return translate_by_words(method_name)
    elif method_name.startswith('Send'):
        return translate_by_words(method_name)
    elif method_name.startswith('Speak'):
        return translate_by_words(method_name)
    elif method_name.startswith('Return'):
        return translate_by_words(method_name)
    elif method_name.startswith('Load'):
        return translate_by_words(method_name)
    elif method_name.startswith('Give'):
        return translate_by_words(method_name)
    elif method_name.startswith('Take'):
        return translate_by_words(method_name)
    elif method_name.startswith('Get'):
        return translate_by_words(method_name)
    else:
        return translate_by_words(method_name)

def process_file1(input_path):
    """处理文件1 - 完整版可视化.html - 只添加方法翻译"""
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配methods数组中的方法定义
    # 格式: "ReturnType methodName(params)"
    def replace_method(match):
        full = match.group(0)
        # 如果已经有翻译了（包含中文括号），跳过
        if re.search(r'\([^)]*[\u4e00-\u9fff]', full):
            return full
        
        # 提取方法签名（不含引号）
        method_sig = match.group(1)
        
        # 提取方法名
        name_match = re.search(r'(\w+)\s*\(', method_sig)
        if not name_match:
            return full
        method_name = name_match.group(1)
        
        # 生成翻译
        translation = translate_method_name(method_name)
        
        # 返回带翻译的方法定义
        return f'"{method_sig} ({translation})"'
    
    # 匹配methods数组中的方法定义
    content = re.sub(
        r'"([^"]+\([^)]*\))"',
        replace_method,
        content
    )
    
    with open(input_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'文件1处理完成')

if __name__ == '__main__':
    base_path = r'd:\trae_project\UCF1.7修改大全\游戏逆向分析-相关信息\02-部分系统'
    
    process_file1(f'{base_path}\\02-完整版可视化.html')
    
    print('所有文件处理完成!')
