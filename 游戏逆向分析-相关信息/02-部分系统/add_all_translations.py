# -*- coding: utf-8 -*-
import re

# FPS射击游戏高频单词翻译表
word_translations = {
    'time': '时间', 'damage': '伤害', 'next': '下次', 'knife': '刀', 'ratio': '比率',
    'wpn': '武器', 'event': '事件', 'player': '玩家', 'hit': '命中', 'observers': '观察者列表',
    'speed': '速度', 'buff': '增益', 'pos': '位置', 'disabled': '禁用', 'map': '地图',
    'camera': '摄像机', 'ammo': '弹药', 'zoom': '瞄准', 'anim': '动画', 'move': '移动',
    'rotation': '旋转', 'jump': '跳跃', 'last': '上次', 'hand': '手', 'attack': '攻击',
    'action': '动作', 'index': '索引', 'name': '名称', 'shot': '射击', 'react': '反应',
    'box': '箱子', 'check': '检查', 'end': '结束', 'type': '类型', 'updater': '更新器',
    'tag': '标签', 'exp': '爆炸', 'listener': '监听器', 'height': '高度', 'data': '数据',
    'nano': '纳米', 'model': '模型', 'fov': '视野', 'distance': '距离', 'weapon': '武器',
    'start': '开始', 'shoot': '射击', 'fire': '开火', 'list': '列表', 'crouch': '蹲下',
    'bullet': '子弹', 'modifier': '修改器', 'penalty': '惩罚', 'owner': '所有者',
    'change': '改变', 'range': '范围', 'clip': '弹夹', 'max': '最大', 'wall': '墙壁',
    'prefab': '预制体', 'yaw': '偏航角', 'pitch': '俯仰角', 'death': '死亡', 'kill': '击杀',
    'enemy': '敌人', 'path': '路径', 'node': '节点', 'game': '游戏', 'all': '全部',
    'reload': '换弹', 'background': '后台', 'default': '默认', 'effect': '特效',
    'post': '后', 'drop': '掉落', 'control': '控制', 'respawn': '重生', 'rot': '旋转',
    'rate': '比率', 'skill': '技能', 'offset': '偏移', 'new': '新', 'set': '设置',
    'gun': '枪械', 'count': '数量', 'factor': '系数', 'ignore': '忽略', 'sound': '音效',
    'perturb': '扰动', 'detail': '详情', 'origin': '原点', 'leg': '腿', 'aim': '瞄准',
    'random': '随机', 'out': '输出', 'cos': '余弦', 'bot': '机器人', 'players': '玩家列表',
    'select': '选择', 'getter': '获取器', 'hangout': '聚集', 'sub': '子', 'cmr': '摄像机',
    'recoil': '后坐力', 'snd': '音效', 'vel': '速度', 'coroutine': '协程', 'trigger': '触发器',
    'infinity': '无限', 'entity': '实体', 'use': '使用', 'special': '特殊', 'key': '键',
    'delay': '延迟', 'scale': '缩放', 'extra': '额外', 'info': '信息', 'multiplier': '乘数',
    'real': '实际', 'dmg': '伤害', 'per': '每', 'full': '完整', 'and': '和', 'body': '身体',
    'disable': '禁用', 'through': '穿透', 'spr': '精灵', 'revenge': '复仇', 'magnitude': '大小',
    'blend': '混合', 'cold': '冷却', 'alpha': '透明度', 'watch': '监视', 'point': '点',
    'find': '查找', 'mode': '模式', 'alive': '存活', 'asset': '资源', 'character': '角色',
    'pool': '池', 'cal': '计算', 'netural': '中立', 'red': '红色', 'blue': '蓝色',
    'occupied': '占用', 'euler': '欧拉角', 'round': '回合', 'temp': '临时', 'remove': '移除',
    'get': '获取', 'observer': '观察者', 'supply': '补给', 'ground': '地面', 'foot': '脚',
    'air': '空中', 'float': '浮空', 'state': '状态', 'current': '当前', 'sniper': '狙击手',
    'spawn': '出生', 'focus': '焦点', 'ghost': '幽灵', 'walking': '行走', 'cloth': '服装',
    'interact': '交互', 'input': '输入', 'climb': '攀爬', 'stair': '楼梯', 'nick': '昵称',
    'level': '等级', 'vip': 'VIP', 'survival': '生存', 'score': '分数', 'sign': '标志',
    'role': '角色', 'fixed': '固定', 'update': '更新', 'setting': '设置', 'existent': '已存在',
    'color': '颜色', 'physical': '物理', 'btn': '按钮', 'down': '按下', 'local': '本地',
    'direction': '方向', 'add': '添加', 'posture': '姿态', 'hurt': '受伤', 'clear': '清除',
    'object': '物体', 'radio': '语音', 'only': '仅', 'invisible': '隐身', 'pick': '拾取',
    'up': '上', 'cost': '消耗', 'break': '中断', 'regen': '回复', 'fill': '填充',
    'enter': '进入', 'exit': '退出', 'speak': '说话', 'msg': '消息', 'channel': '频道',
    'ace': '王牌', 'run': '奔跑', 'property': '属性', 'visible': '可见', 'ray': '射线',
    'view': '视角', 'base': '基础', 'feedback': '反馈', 'buffs': '增益列表', 'health': '生命',
    'dead': '死亡', 'black': '黑名单', 'global': '全局', 'risk': '风险', 'team': '队伍',
    'animator': '动画器', 'controller': '控制器', 'slot': '槽位', 'forward': '前方',
    'container': '容器', 'autonomous': '自动', 'grounded': '着地', 'mat': '材质', 'fall': '下落',
    'can': '能否', 'my': '我的', 'duration': '持续时间', 'crouching': '蹲下中', 'climbing': '攀爬中',
    'nickName': '昵称', 'isSniper': '是否狙击手', 'isRespawning': '是否正在重生',
    'isMyPlayer': '是否我的玩家', 'isFocusPlayer': '是否焦点玩家', 'isNanoGhost': '是否纳米幽灵',
    'crouchDuration': '蹲下持续时间', 'isCrouching': '是否蹲下中', 'nanoCloth': '纳米服装',
    'clothCount': '服装数量', 'mapGun': '地图枪械', 'isClimbing': '是否攀爬中',
    'isBlackList': '是否黑名单', 'isGlobalRisk': '是否全局风险', 'characterAnimator': '角色动画器',
    'characterController': '角色控制器', 'speedPenalty': '速度惩罚', 'damageRate': '伤害比率',
    'isInvincible': '是否无敌', 'healthData': '生命数据', 'isDead': '是否死亡',
    'isGhostEntity': '是否幽灵实体', 'noHitFeedback': '无命中反馈', 'invincibleUpdater': '无敌更新器',
    'localDirection': '本地方向', 'inverse': '反向', 'onlyAlive': '仅存活', 'isAlive': '是否存活',
    'penaltyBuff': '惩罚增益', 'damageRateBuff': '伤害比率增益', 'cleanAll': '清除全部',
    'priority': '优先级', 'findBuff': '查找增益', 'newBuff': '新增益', 'tryAdd': '尝试添加',
    'creater': '创建器', 'updateBuff': '更新增益', 'ghostState': '幽灵状态', 'hitBox': '命中框',
    'viewRay': '视角射线', 'allSkills': '全部技能', 'lifeState': '生命状态', 'tryUse': '尝试使用',
    'skillName': '技能名称', 'skillKey': '技能键', 'isSoldier': '是否士兵', 'savior': '救世主',
    'likeGuard': '类似守卫', 'isHuman': '是否人类', 'isHero': '是否英雄', 'normalHero': '普通英雄',
    'masterHero': '大师英雄', 'normalNano': '普通纳米', 'terminator': '终结者',
    'normalTerminator': '普通终结者', 'masterTerminator': '大师终结者', 'removeAll': '移除全部',
    'canUse': '能否使用', 'animEnd': '动画结束', 'animExit': '动画退出', 'generate': '生成',
    'fromOwner': '从所有者', 'recycle': '回收', 'deploy': '部署', 'unDeploy': '取消部署',
    'resetMode': '重置模式', 'viewSetting': '视图设置', 'syncHand': '同步手部', 'animSpeed': '动画速度',
    'crosshair': '准星', 'charAnim': '角色动画', 'fromPool': '从武器池', 'fireBtn': '开火按钮',
    'pressed': '按住', 'unPressed': '松开', 'specialBtn': '特殊按钮', 'reloadBtn': '换弹按钮',
    'bool': '布尔值', 'integer': '整数', 'crossFade': '交叉淡入', 'fixedTime': '固定时间',
    'knifeData': '刀击数据', 'callKnife': '调用刀击', 'sprIndex': '精灵索引', 'dmgEvent': '伤害事件',
    'shouldDmg': '是否应伤害', 'giveUp': '丢弃', 'botControl': '机器人控制', 'charShoot': '角色射击',
    'wpnName': '武器名称', 'wpnSprite': '武器精灵', 'charWpn': '角色武器', 'animData': '动画数据',
    'infinityAmmo': '无限弹药', 'thisWpn': '此武器', 'consume': '消耗', 'animReload': '换弹动画',
    'basicRecoil': '基础后坐力', 'recoilData': '后坐力数据', 'gunFire': '枪械开火',
    'tryReload': '尝试换弹', 'canReload': '能否换弹', 'reloadOver': '换弹结束', 'preReload': '预换弹',
    'fillAmmo': '填充弹药', 'addAmmo': '添加弹药', 'gunFireEffect': '枪口火焰', 'stopFire': '停止开火',
    'knifeEvent': '刀击事件', 'startKnife': '开始刀击', 'knifeExit': '刀击退出', 'genBullet': '生成子弹',
    'useZoom': '使用缩放', 'closeZoom': '关闭缩放', 'fireAnim': '开火动画', 'gunShoot': '枪械射击',
    'noCheck': '无检查', 'shootLogic': '射击逻辑', 'shootFunc': '射击函数', 'nextFrame': '下一帧',
    'autoFire': '自动开火', 'autoStop': '自动停火', 'sniperBot': '狙击机器人', 'collision': '碰撞',
    'throwAnim': '投掷动画', 'throw': '投掷', 'explode': '爆炸', 'expEffect': '爆炸特效',
    'expSound': '爆炸音效', 'causeDmg': '造成伤害', 'missile': '导弹', 'target': '目标',
    'flyAnim': '飞行动画', 'updateMissile': '更新导弹', 'knifeAnim': '刀击动画', 'takePlace': '生效',
    'print': '打印', 'handRot': '手部旋转', 'modifyOffset': '修改偏移', 'afterFBBIK': 'FBBIK后',
    'afterAimIK': 'AimIK后', 'lifeEnd': '生命结束', 'endTime': '结束时间', 'refreshTime': '刷新时间',
    'timeout': '超时', 'coldFinish': '冷却完成', 'spriteIdx': '精灵索引', 'basicCheck': '基础检查',
    'onPlayerSpawn': '玩家重生', 'onSetPlayer': '设置到玩家', 'startCold': '开始冷却',
    'endCold': '结束冷却', 'speedUpdate': '速度更新', 'dmgRateUpdate': '伤害比率更新',
    'modelAlpha': '模型透明度', 'hangoutCount': '聚集数量', 'gizmos': 'Gizmos',
    'nearestNode': '最近节点', 'pathSetting': '路径设置', 'reachDist': '可达距离',
    'pathComplete': '路径完成', 'jumpCheck': '跳跃检查', 'tryCrouch': '尝试蹲下', 'moveState': '移动状态',
    'camRot': '摄像机旋转', 'lifeChange': '生命改变', 'takeDmg': '承受伤害', 'spawnDelay': '生成延迟',
    'nanoGuard': '纳米守卫', 'guardArea': '守卫区域', 'attackTarget': '攻击目标', 'checkTarget': '检查目标',
    'useWpn': '使用武器', 'selectWpn': '选择武器', 'wpnAction': '武器动作', 'useSkill': '使用技能',
    'roleChange': '角色改变', 'updateAction': '更新动作', 'tableType': '表类型', 'playerSkill': '玩家技能',
    'pathLength': '路径长度', 'ghostEntity': '幽灵实体', 'zoomDir': '缩放方向', 'setAbility': '设置能力',
    'gunDist': '枪械距离', 'knifeDist': '刀具距离', 'waitKnife': '等待刀击', 'doAction': '执行动作',
    'nextCheck': '下次检查', 'tryGetAce': '尝试获取王牌', 'resetRound': '重置回合', 'restRound': '休息回合',
    'addPlayers': '添加玩家', 'test': '测试', 'addPlayer': '添加玩家', 'spareIdx': '备用索引',
    'loadWpn': '加载武器', 'giveWpn': '给予武器', 'byBag': '通过背包', 'getWpn': '获取武器',
    'wpnData': '武器数据', 'getChar': '获取角色', 'deathEvent': '死亡事件', 'returnLobby': '返回大厅',
    'roundEnd': '回合结束', 'recycleObj': '可回收物体', 'clearRecycle': '清除可回收',
    'mapGunInit': '地图枪械初始化', 'newRound': '新回合', 'spawnPoint': '出生点', 'supplyBox': '补给箱',
    'releaseBox': '释放箱子', 'active': '激活', 'playerExit': '玩家退出', 'mapWpnRecycle': '地图武器回收',
    'resetEuler': '重置欧拉角', 'canInteract': '能否交互', 'tipSprite': '提示精灵', 'canPickUp': '能否拾取',
    'redBox': '红盒', 'work': '工作', 'boxList': '箱子列表', 'randomBox': '随机箱子',
    'nearestBox': '最近箱子', 'clearBox': '清除箱子', 'boxType': '箱子类型', 'pixel': '像素',
    'radar': '雷达', 'originPos': '原点位置', 'perDistance': '每距离', 'weaponMdl': '武器模型',
    'onPlayerExit': '玩家退出', 'mapWpn': '地图武器', 'gravity': '重力', 'manager': '管理器',
    'characters': '角色列表', 'obj': '物体', 'play': '播放', 'before': '之前', 'vel': '速度',
    'client': '客户端', 'skills': '技能', 'nextRegen': '下次回复', 'cameraRot': '摄像机旋转',
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
    'setGhostEntityState': '设置幽灵实体状态', 'getVisibleHitBox': '获取可见命中框', 'all': '全部', 'owner': '所有者',
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

def process_file1(input_path):
    """处理文件1 - 完整版可视化.html"""
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 处理方法 - 添加翻译
    def replace_method(match):
        full = match.group(0)
        # 如果已经有翻译了，跳过
        if full.count('(') > 1:  # 方法签名本身有括号，如果还有额外括号说明有翻译
            # 检查是否有中文翻译（在最后的括号内）
            if re.search(r'\)\s*\([^)]*[\u4e00-\u9fff]', full):
                return full
        # 提取方法签名
        method_match = re.match(r'"([^"]+)"', full)
        if not method_match:
            return full
        method_sig = method_match.group(1)
        # 提取方法名
        name_match = re.search(r'(\w+)\s*\(', method_sig)
        if not name_match:
            return full
        method_name = name_match.group(1)
        # 生成翻译
        if method_name.startswith('get_'):
            prop = method_name[4:]
            translation = f'获取{translate_by_words(prop)}'
        elif method_name.startswith('set_'):
            prop = method_name[4:]
            translation = f'设置{translate_by_words(prop)}'
        elif method_name.startswith('On'):
            translation = translate_by_words(method_name)
        elif method_name.startswith('Try'):
            translation = translate_by_words(method_name)
        elif method_name.startswith('Add'):
            translation = translate_by_words(method_name)
        elif method_name.startswith('Update'):
            translation = translate_by_words(method_name)
        elif method_name.startswith('Set'):
            translation = translate_by_words(method_name)
        elif method_name.startswith('Remove'):
            translation = translate_by_words(method_name)
        elif method_name.startswith('Clear'):
            translation = translate_by_words(method_name)
        elif method_name.startswith('Find'):
            translation = translate_by_words(method_name)
        elif method_name.startswith('Select'):
            translation = translate_by_words(method_name)
        elif method_name.startswith('Spawn'):
            translation = translate_by_words(method_name)
        elif method_name.startswith('Break'):
            translation = translate_by_words(method_name)
        elif method_name.startswith('Reset'):
            translation = translate_by_words(method_name)
        elif method_name.startswith('Fill'):
            translation = translate_by_words(method_name)
        elif method_name.startswith('Drop'):
            translation = translate_by_words(method_name)
        elif method_name.startswith('Send'):
            translation = translate_by_words(method_name)
        elif method_name.startswith('Speak'):
            translation = translate_by_words(method_name)
        elif method_name.startswith('Return'):
            translation = translate_by_words(method_name)
        elif method_name.startswith('Load'):
            translation = translate_by_words(method_name)
        elif method_name.startswith('Give'):
            translation = translate_by_words(method_name)
        elif method_name.startswith('Take'):
            translation = translate_by_words(method_name)
        elif method_name.startswith('Get'):
            translation = translate_by_words(method_name)
        else:
            translation = translate_by_words(method_name)
        return f'"{method_sig} ({translation})"'
    
    # 匹配methods数组中的方法定义
    content = re.sub(
        r'^(\s*)"([^"]+\([^)]*\))"\s*$',
        replace_method,
        content,
        flags=re.MULTILINE
    )
    
    with open(input_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'文件1处理完成')

def process_file2(input_path):
    """处理文件2 - 核心类详细定义.html"""
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 处理方法 - <div class="method-item">...</div>
    def replace_method_div(match):
        div_content = match.group(0)
        # 如果已经有翻译了，跳过
        if 'method-cn' in div_content:
            return div_content
        # 提取方法名
        method_match = re.search(r'<span class="method-name">(\w+)</span>', div_content)
        if method_match:
            method_name = method_match.group(1)
            # 生成翻译
            if method_name.startswith('get_'):
                prop = method_name[4:]
                translation = f'获取{translate_by_words(prop)}'
            elif method_name.startswith('set_'):
                prop = method_name[4:]
                translation = f'设置{translate_by_words(prop)}'
            else:
                translation = translate_by_words(method_name)
            # 在方法名后添加中文翻译
            new_div = div_content.replace(f'>{method_name}</span>', f'>{method_name}</span><span class="method-cn"> ({translation})</span>')
            return new_div
        return div_content
    
    content = re.sub(r'<div class="method-item">.*?</div>', replace_method_div, content, flags=re.DOTALL)
    
    with open(input_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'文件2处理完成')

if __name__ == '__main__':
    base_path = r'd:\trae_project\UCF1.7修改大全\游戏逆向分析-相关信息\02-部分系统'
    
    process_file1(f'{base_path}\\02-完整版可视化.html')
    process_file2(f'{base_path}\\03--核心类详细定义.html')
    
    print('所有文件处理完成!')
