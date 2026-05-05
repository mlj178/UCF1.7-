# -*- coding: utf-8 -*-
import re

# FPS射击游戏术语翻译字典
translations = {
    # 字段翻译
    'defaultMoveSpeed': '默认移动速度',
    'playerHeight': '玩家高度',
    'crouchSubHeight': '蹲下子高度',
    'mapCmrHeight': '地图摄像机高度',
    'mapCmrCrouchSubHeight': '地图摄像机蹲下子高度',
    'playerGravity': '玩家重力',
    'cameraManager': '玩家摄像机管理器',
    'cameraRotation': '摄像机旋转',
    'recoil': '后坐力',
    'characters': '角色模型列表',
    'bulletEffect': '子弹特效',
    'JumpPost_Listener': '跳跃后监听器',
    'jumpDropSndNextPlayTime': '跳跃下落音效下次播放时间',
    'lastFallTime': '上次下落时间',
    'heightBeforeFloat': '浮空前高度',
    'startMoveTime': '开始移动时间',
    'airVelControlEndTime': '空中速度控制结束时间',
    'Modifier_MoveSpeedRatio': '移动速度比率修改器',
    'clientData': '客户端数据',
    'nanoRoleSelect': '纳米角色选择',
    'nano4TData': '纳米4T数据',
    'skills': '玩家技能',
    'respawn_Coroutine': '重生协程',
    'StartRespawn_Listener': '开始重生监听器',
    'respawnType': '重生类型',
    'NextRespawnInRound_Listener': '回合内下次重生监听器',
    'nextRegenTime': '下次回复时间',
    'mapTrigger': '地图触发器',
    'Buff_CameraRotDisabled': '摄像机旋转禁用增益',
    'CameraRotDisabled_BuffUpdater': '摄像机旋转禁用增益更新器',
    'JumpDisabled_BuffUpdater': '跳跃禁用增益更新器',
    'Buff_InfinityAmmo': '无限弹药增益',
    'InfinityAmmo_BuffUpdater': '无限弹药增益更新器',
    
    # 方法翻译 - getter/setter
    'get_mapCameraPos': '获取地图摄像机位置',
    'set_mapCameraPos': '设置地图摄像机位置',
    'get_mapCameraForward': '获取地图摄像机前方向',
    'set_mapCameraForward': '设置地图摄像机前方向',
    'get_characterContainer': '获取角色容器',
    'set_characterContainer': '设置角色容器',
    'get_currentCharacter': '获取当前角色模型',
    'set_currentCharacter': '设置当前角色模型',
    'get_footPos': '获取脚部位置',
    'set_footPos': '设置脚部位置',
    'get_autonomousJump': '获取自动跳跃',
    'set_autonomousJump': '设置自动跳跃',
    'get_isGrounded': '获取是否着地',
    'set_isGrounded': '设置是否着地',
    'get_groundMatName': '获取地面材质名称',
    'set_groundMatName': '设置地面材质名称',
    'get_fallTime': '获取下落时间',
    'set_fallTime': '设置下落时间',
    'get_canControlVelInAir': '获取能否在空中控制速度',
    'set_canControlVelInAir': '设置能否在空中控制速度',
    'get_velocity': '获取速度',
    'set_velocity': '设置速度',
    'get_MoveSpeedRatio': '获取移动速度比率',
    'set_MoveSpeedRatio': '设置移动速度比率',
    'get_velData': '获取速度数据',
    'set_velData': '设置速度数据',
    'get_playerData': '获取玩家数据',
    'set_playerData': '设置玩家数据',
    'get_input': '获取输入',
    'set_input': '设置输入',
    'get_wpns': '获取武器',
    'set_wpns': '设置武器',
    'get_weaponBag': '获取武器背包',
    'set_weaponBag': '设置武器背包',
    'get_modelInfo': '获取模型信息',
    'set_modelInfo': '设置模型信息',
    'get_isSniper': '获取是否狙击手',
    'set_isSniper': '设置是否狙击手',
    'get_spawnPos': '获取出生位置',
    'set_spawnPos': '设置出生位置',
    'get_isRespawning': '获取是否正在重生',
    'set_isRespawning': '设置是否正在重生',
    'get_isMyPlayer': '获取是否我的玩家',
    'set_isMyPlayer': '设置是否我的玩家',
    'get_isFocusPlayer': '获取是否焦点玩家',
    'set_isFocusPlayer': '设置是否焦点玩家',
    'get_isFocusPlayerInPV': '获取是否在PV中的焦点玩家',
    'set_isFocusPlayerInPV': '设置是否在PV中的焦点玩家',
    'get_isNanoGhost': '获取是否纳米幽灵',
    'set_isNanoGhost': '设置是否纳米幽灵',
    'get_crouchDuration': '获取蹲下持续时间',
    'set_crouchDuration': '设置蹲下持续时间',
    'get_isCrouching': '获取是否蹲下中',
    'set_isCrouching': '设置是否蹲下中',
    'get_walking': '获取是否行走中',
    'set_walking': '设置是否行走中',
    'get_nanoClothCount': '获取纳米服装数量',
    'set_nanoClothCount': '设置纳米服装数量',
    'get_input_Interact': '获取交互输入',
    'set_input_Interact': '设置交互输入',
    'get_mapGunAmmo1': '获取地图枪械弹药1',
    'set_mapGunAmmo1': '设置地图枪械弹药1',
    'get_mapGunAmmo2': '获取地图枪械弹药2',
    'set_mapGunAmmo2': '设置地图枪械弹药2',
    'get_climbStair': '获取爬楼梯',
    'set_climbStair': '设置爬楼梯',
    
    # 其他方法翻译
    'FixedUpdate': '固定帧更新',
    'UpdateGroundMatName': '更新地面材质名称',
    'CharacterModelSetting': '角色模型设置',
    'SetExistentCharacter': '设置已存在角色',
    'SetCharacter': '设置角色',
    'UpdateModelColor': '更新模型颜色',
    'PhysicalUpdate': '物理更新',
    'SetGroundState': '设置地面状态',
    'OnJumpBtnDown': '跳跃按钮按下',
    'GetMoveSpeed': '获取移动速度',
    'MoveByLocalDirection': '按本地方向移动',
    'GetCameraRotation': '获取摄像机旋转',
    'AddCameraRotation': '添加摄像机旋转',
    'UpdateCameraRotaion': '更新摄像机旋转',
    'LookAt': '看向',
    'SetWeapon': '设置武器',
    'RecoilShootPostureCheck': '后坐力射击姿态检查',
    'OnEntityHurt': '实体受伤',
    'OnEntityDeath': '实体死亡',
    'ClearMapObject': '清除地图物体',
    'DropWeaponAfterDeath': '死亡后丢弃武器',
    'SendFireInTheHoleRadio': '发送投掷物语音',
    'RemoveFromTeamList': '从队伍列表移除',
    'AddToTeamList': '添加到队伍列表',
    'Respawn': '重生',
    'BreakRespawnCoroutine': '中断重生协程',
    'Spawn': '生成',
    'OnGameRoundEnd': '回合结束',
    'SetPos': '设置位置',
    'SelectWeaponBag': '选择武器包',
    'TryPickUpWeapon': '尝试拾取武器',
    'SetCrouchState': '设置蹲下状态',
    'SetWalkState': '设置行走状态',
    'TrySubSkillHPCost': '尝试扣除技能HP消耗',
    'BreakStopTime': '中断停止时间',
    'NanoGhostHPRegen': '纳米幽灵HP回复',
    'SetNanoClothCount': '设置纳米服装数量',
    'AddNanoClothCount': '增加纳米服装数量',
    'SetInteractInput': '设置交互输入',
    'FillMapGunAmmo': '填充地图枪械弹药',
    'OnTriggerEnter': '进入触发器',
    'OnTriggerExit': '退出触发器',
    'Speak': '说话',
    'UpdateAce': '更新王牌',
    'ResetDropSndTime': '重置掉落音效时间',
    'UpdateFallTime': '更新下落时间',
    'UpdateRunState': '更新奔跑状态',
    'UpdateBuffProperty': '更新增益属性',
    'AddNextRespawnInvincible': '添加下次重生无敌',
    'GetVisibleHitBox': '获取可见命中框',
    'Owner_LifeState_Listenner': '所有者生命状态监听',
    'TryUse': '尝试使用',
    'Remove': '移除',
    'AutoSelect': '自动选择',
    'GetValidSlot': '获取有效槽位',
    'SelectLast': '选择上一个',
    'SelectLastOrAutoSelect': '选择上一个或自动选择',
    'Select': '选择',
    'SelectByMouseRoll': '鼠标滚轮选择',
    'SelectFKeyWeapon': '选择F键武器',
    'RemoveAll': '移除全部',
    'SetCurrentWeapon': '设置当前武器',
    'FillMainWeaponAmmo': '填充主武器弹药',
    'FillAllGunAmmo': '填充所有枪械弹药',
    'GiveUpWeapon': '丢弃武器',
    'Limit': '限制',
    'ClearGravity': '清除重力',
    'ClearVelocity': '清除速度',
    'SetMapDash': '设置地图冲刺',
    'SetDash': '设置冲刺',
    'LockVelocity': '锁定速度',
    'GetDashDirection': '获取冲刺方向',
    'Update': '更新',
    'ShouldMoveOnGround': '是否应在地面移动',
    'SetModelDelayPos': '设置模型延迟位置',
    'AddModelDelayPos': '添加模型延迟位置',
    'CameraFovSetting': '摄像机视野设置',
    'SetRotation': '设置旋转',
    'PlayKnifeHitStunShake': '播放刀击眩晕震动',
    'SetFovBuffInfo': '设置视野增益信息',
    'FovZommBuffEndEvent': '视野缩放增益结束事件',
    'GetName': '获取名称',
    'IsSoldierOrSavior': '是否士兵或救世主',
    'LikeGuard': '类似守卫',
    'IsHuman': '是否人类',
    'IsHero': '是否英雄',
    'IsNormalHero': '是否普通英雄',
    'IsMasterHero': '是否大师英雄',
    'IsNanoGhost': '是否纳米幽灵',
    'IsNormalNanoGhost': '是否普通纳米幽灵',
    'IsTerminator': '是否终结者',
    'IsNormalTerminator': '是否普通终结者',
    'IsMasterTerminator': '是否大师终结者',
    'GetTeam': '获取队伍',
    'ShouldRemoveAllWpn': '是否应移除所有武器',
    'CanUseGun': '能否使用枪械',
    'OnAnimationEnd': '动画结束',
    'OnAnimationExit': '动画退出',
    'Init': '初始化',
    'OnGenerateFromOwner': '从所有者生成',
    'Recycle': '回收',
    'Deploy': '部署',
    'UnDeploy': '取消部署',
    'ResetModeChange': '重置模式切换',
    'PlayerViewSetting': '玩家视图设置',
    'SynchronizeHand': '同步手部',
    'AnimSpeedSetting': '动画速度设置',
    'CrosshairSetting': '准星设置',
    'SetMoveSpeedPenalty': '设置移动速度惩罚',
    'SetCharacterAnim': '设置角色动画',
    'OnSelectedFromWeaponPool': '从武器池选中',
    'OnFireBtnDown': '开火按钮按下',
    'OnFireBtnPressed': '开火按钮按住',
    'OnFireBtnUnPressed': '开火按钮松开',
    'OnSpecialBtnDown': '特殊按钮按下',
    'OnSpecialBtnPressed': '特殊按钮按住',
    'OnSpecialBtnUnPressed': '特殊按钮松开',
    'OnReloadBtnDown': '换弹按钮按下',
    'SetTrigger': '设置触发器',
    'ResetTrigger': '重置触发器',
    'SetBool': '设置布尔值',
    'SetInteger': '设置整数值',
    'CrossFadeInFixedTime': '固定时间交叉淡入',
    'Play': '播放',
    'GetKnifeAttackData': '获取刀击数据',
    'CallKnifeAttack': '调用刀击',
    'GetKnifeAttackSprIndex': '获取刀击精灵索引',
    'TriggerDmgEventAndClear': '触发伤害事件并清除',
    'ShouldDamage': '是否应造成伤害',
    'GiveUp': '丢弃',
    'BotControl': '机器人控制',
    'PlayCharacterShootAnim': '播放角色射击动画',
    'GetWpnName': '获取武器名称',
    'GetWpnSpriteAsset': '获取武器精灵资源',
    'GetCharWpnAnimData': '获取角色武器动画数据',
    'CanGetInfinityAmmo': '能否获取无限弹药',
    'RemoveThisWeapon': '移除此武器',
    'ConsumeAmmo': '消耗弹药',
    'AmmoSetting': '弹药设置',
    'UpdateAnimSpeed_Reload': '更新动画速度_换弹',
    'SetBasicRecoilData': '设置基础后坐力数据',
    'SetRecoilData': '设置后坐力数据',
    'GunFireChecking': '枪械开火检查',
    'TryReload': '尝试换弹',
    'CanReload': '能否换弹',
    'Reload': '换弹',
    'ReloadOver': '换弹结束',
    'PreReloadOver': '换弹结束前',
    'FillAmmo': '填充弹药',
    'AddAmmo': '添加弹药',
    'Damage': '伤害',
    'PlayGunFire': '播放枪口火焰',
    'StopGunFire': '停止枪口火焰',
    'KnifeAttackEvent': '刀击事件',
    'StartKnifeAttack': '开始刀击',
    'OnKnifeAttackExit': '刀击退出',
    'GenerateBullet': '生成子弹',
    'UseZoom': '使用缩放',
    'CloseZoom': '关闭缩放',
    'OnFireAnimExit': '开火动画退出',
    'GunShoot': '枪械射击',
    'GunShoot_NoCheck': '枪械射击_无检查',
    'GunShoot_Logic': '枪械射击_逻辑',
    'GunShootFunction': '枪械射击函数',
    'TryReloadNextFrame': '尝试下一帧换弹',
    'BreakAutomaticGunFire': '中断自动开火',
    'AutomaticGunStopFire': '自动停火',
    'SniperBotControl': '狙击机器人控制',
    'OnCollisionEnter': '进入碰撞',
    'PlayThrowAnim': '播放投掷动画',
    'Throw': '投掷',
    'Explode': '爆炸',
    'PlayExpEffect': '播放爆炸特效',
    'PlayExpSound': '播放爆炸音效',
    'CauseDamage': '造成伤害',
    'OnCollisionStay': '停留碰撞',
    'OnCollisionExit': '退出碰撞',
    'SetMissileTarget': '设置导弹目标',
    'PlayFlyAnim': '播放飞行动画',
    'UpdateMissile': '更新导弹',
    'PlayKnifeAttackAnim': '播放刀击动画',
    'OnKnifeAttackAnimEnd': '刀击动画结束',
    'TakePlace': '生效',
    'Print': '打印',
    'Get': '获取',
    'SetHandRotations': '设置手部旋转',
    'Fire': '开火',
    'OnModifyOffset': '修改偏移',
    'AfterFBBIK': 'FBBIK之后',
    'AfterAimIK': 'AimIK之后',
    'BuffUpdater': '增益更新器',
    'OnLifeEnd': '生命周期结束',
    'get_name': '获取名称',
    'set_name': '设置名称',
    'get_owner': '获取所有者',
    'set_owner': '设置所有者',
    'get_endTime': '获取结束时间',
    'set_endTime': '设置结束时间',
    'Refreshime': '刷新时间',
    'TimeOut': '超时',
    'get_isColdFinish': '获取是否冷却完成',
    'get_isCanUse': '获取是否可用',
    'GetSpriteIndex': '获取精灵索引',
    'BasicCheck': '基础检查',
    'OnPlayerReSpawn': '玩家重生',
    'OnSetOnPlayer': '设置到玩家身上',
    'StartCold': '开始冷却',
    'EndCold': '结束冷却',
    'SpeedPenaltyBuffUpdate': '速度惩罚增益更新',
    'DamageRateBuffUpdate': '伤害比率增益更新',
    'Owner_Invincible_BuffUpdater': '所有者无敌增益更新器',
    'ModelInfo_Getter_Alpha': '模型信息获取透明度',
    'InitHangOutCount': '初始化聚集数量',
    'OnDrawGizmosSelected': '绘制选中Gizmos',
    'UpdateNearestGraphNode': '更新最近图节点',
    'PathSetting': '路径设置',
    'IsPosInReachDistance': '位置是否在可达距离',
    'OnPathComplete': '路径完成',
    'Move': '移动',
    'JumpCheck': '跳跃检查',
    'Jump': '跳跃',
    'TryCrouch': '尝试蹲下',
    'GetMoveStateByDir': '根据方向获取移动状态',
    'CameraRotation': '摄像机旋转',
    'OnLifeStateChange': '生命状态改变',
    'TakeDamageEvent': '承受伤害事件',
    'SpawnDelayEvent': '生成延迟事件',
    'OnEnterNanoGuardArea': '进入纳米守卫区域',
    'OnExitNanoGuardArea': '退出纳米守卫区域',
    'IEnumerator': 'IEnumerator',
    'FindAttackTarget': '查找攻击目标',
    'TrySetAttackTarget': '尝试设置攻击目标',
    'CheckHitBox': '检查命中框',
    'CheckAttackTarget': '检查攻击目标',
    'UseWeapon': '使用武器',
    'SelectWeapon': '选择武器',
    'AddSelectWpnAction': '添加选择武器动作',
    'UseSkill': '使用技能',
    'OnNanoRoleChange': '纳米角色改变',
    'UpdateAction': '更新动作',
    'OnNanoRoleTableTypeChange': '纳米角色表类型改变',
    'OnPlayerSetSkill': '玩家设置技能',
    'IsPathLengthToEnemyLess': '到敌人路径长度是否小于',
    'UpdateGhostEntityState': '更新幽灵实体状态',
    'GetZoomDirectionByPos': '根据位置获取缩放方向',
    'SetAbility': '设置能力',
    'CalGunDistanceControl': '计算枪械距离控制',
    'CalKnifeDistanceControl': '计算刀具距离控制',
    'ShouldWaitKnifeAttack': '是否应等待刀击',
    'DoAction': '执行动作',
    'AddNextCheckTime': '添加下次检查时间',
    'TryGetAce': '尝试获取王牌',
    'ResetRound': '重置回合',
    'RestRoundCoroutine': '休息回合协程',
    'AddPlayers': '添加玩家',
    'Test': '测试',
    'AddPlayer': '添加玩家',
    'GetSparePlayerIndex': '获取备用玩家索引',
    'LoadWeapon': '加载武器',
    'GiveWeapon': '给予武器',
    'GiveWeaponByBag': '通过背包给予武器',
    'GetWeapon': '获取武器',
    'GetWpnData': '获取武器数据',
    'GetCharacter': '获取角色',
    'TakeDamage': '承受伤害',
    'DeathEventBroadcast': '死亡事件广播',
    'ReturnLobby': '返回大厅',
    'GameRoundEnd': '回合结束',
    'AddRecyclableObject': '添加可回收物体',
    'RemoveRecyclableObject': '移除可回收物体',
    'ClearRecyclableObject': '清除可回收物体',
    'MapGunInit': '地图枪械初始化',
    'NewGameRoundStart': '新回合开始',
    'GetSpawnPoint': '获取出生点',
    'OnDrawGizmos': '绘制Gizmos',
    'GetSupplyBoxPoint': '获取补给箱点',
    'ReleaseSupplyBoxPoint': '释放补给箱点',
    'Active': '激活',
    'OnPlayerExit': '玩家退出',
    'OnMapWpnRecycle': '地图武器回收',
    'ResetEuler': '重置欧拉角',
    'CanInteract': '能否交互',
    'GetTipSprite': '获取提示精灵',
    'CanPickUp': '能否拾取',
    'CanPickUpRedBox': '能否拾取红盒',
    'Work': '工作',
    'GetBoxList': '获取箱子列表',
    'GetRandomBox': '获取随机箱子',
    'GetNearestBox': '获取最近箱子',
    'ClearBoxList': '清除箱子列表',
    'GetBoxType': '获取箱子类型',
}

def translate_method(method_str):
    """为方法字符串添加中文翻译"""
    # 如果已经有翻译了，跳过
    if ' (' in method_str and method_str.endswith(')'):
        if re.search(r'\([^)]*[\u4e00-\u9fff]', method_str):
            return method_str
    
    # 提取方法签名
    match = re.match(r'^(\S+\s+\w+\([^)]*\))(.*)$', method_str)
    if not match:
        return method_str
    
    signature = match.group(1)
    
    # 提取方法名
    method_name_match = re.search(r'\b(\w+)\s*\(', signature)
    if not method_name_match:
        return method_str
    
    method_name = method_name_match.group(1)
    
    # 查找翻译
    translation = translations.get(method_name)
    if translation:
        return f'{signature} ({translation})'
    
    # 尝试生成翻译
    if method_name.startswith('get_'):
        prop = method_name[4:]
        return f'{signature} (获取{prop})'
    elif method_name.startswith('set_'):
        prop = method_name[4:]
        return f'{signature} (设置{prop})'
    elif method_name.startswith('Is'):
        return f'{signature} (是否{method_name[2:]})'
    elif method_name.startswith('Can'):
        return f'{signature} (能否{method_name[3:]})'
    elif method_name.startswith('Should'):
        return f'{signature} (是否应该{method_name[6:]})'
    elif method_name.startswith('Has'):
        return f'{signature} (是否有{method_name[3:]})'
    elif method_name.startswith('Have'):
        return f'{signature} (是否有{method_name[4:]})'
    
    return method_str

def translate_field(field_str):
    """为字段字符串添加中文翻译"""
    # 如果已经有翻译了，跳过
    if ' (' in field_str and ')' in field_str:
        parts = field_str.split(' (')
        if len(parts) >= 2:
            cn_part = parts[1].split(')')[0]
            if re.search(r'[\u4e00-\u9fff]', cn_part):
                return field_str
    
    # 提取字段名和类型
    match = re.match(r'^(\w+)\s*:\s*(.+)$', field_str)
    if not match:
        return field_str
    
    field_name = match.group(1)
    field_type = match.group(2)
    
    # 查找翻译
    translation = translations.get(field_name)
    if translation:
        return f'{field_name} ({translation}) : {field_type}'
    
    # 尝试生成翻译
    if field_name.startswith('is') and len(field_name) > 2 and field_name[2].isupper():
        return f'{field_name} (是否{field_name[2:]}) : {field_type}'
    elif field_name.startswith('is'):
        return f'{field_name} (是否{field_name[2:]}) : {field_type}'
    elif field_name.startswith('has') and len(field_name) > 3 and field_name[3].isupper():
        return f'{field_name} (是否有{field_name[3:]}) : {field_type}'
    elif field_name.startswith('has'):
        return f'{field_name} (是否有{field_name[3:]}) : {field_type}'
    
    return field_str

def process_file1(input_path, output_path):
    """处理文件1 - 完整版可视化.html"""
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 处理字段 - 替换已有的半中文半英文翻译为正确的中文翻译
    def replace_field(match):
        field_str = match.group(0)
        # 提取字段名
        field_name_match = re.match(r'"(\w+)\s*\(', field_str)
        if not field_name_match:
            return field_str
        field_name = field_name_match.group(1)
        translation = translations.get(field_name)
        if translation:
            # 提取类型部分
            type_match = re.search(r':\s*(.+)"$', field_str)
            if type_match:
                field_type = type_match.group(1)
                return f'"{field_name} ({translation}) : {field_type}"'
        return field_str
    
    # 匹配有翻译的字段 "fieldName (xxx) : type"
    content = re.sub(
        r'"(\w+\s*\([^)]+\)\s*:\s*[^"]+)"',
        replace_field,
        content
    )
    
    # 处理没有翻译的字段 "fieldName : type"
    def replace_field_no_translation(match):
        field_str = match.group(0)
        # 提取字段名和类型
        field_match = re.match(r'"(\w+)\s*:\s*(.+)"$', field_str)
        if not field_match:
            return field_str
        field_name = field_match.group(1)
        field_type = field_match.group(2)
        translation = translations.get(field_name)
        if translation:
            return f'"{field_name} ({translation}) : {field_type}"'
        return field_str
    
    # 匹配没有翻译的字段
    content = re.sub(
        r'"(\w+\s*:\s*[^"]+)"',
        replace_field_no_translation,
        content
    )
    
    # 处理methods部分
    content = re.sub(
        r'"((?:void|bool|int|float|string|Vector[23]|Transform|CharacterModel|PlayerData|PlayerInput|PlayerWeapons|WeaponBag|PlayerMdlInfo|ObscuredInt|KeyInputState|WPN_Gun\.AmmoData|HUD_Role\.AceSign|NanoRole|Buff|Sprite|HealthData|Animator|CharacterController|Team|Weapon|KnifeAttackData|WpnSpriteAsset|CharWpnAnimData|IEnumerator|PlayerVelocity|PlayerCameraManager\.FovZoomInfo|WPN_Knife\.KnifeAttackType|SupplyBox\.Type|QVModel|DamageEventData|DeathEventData|Ray|Collider|GameObject|Coroutine|ParticleSystem|Texture2D|CinemachineVirtualCamera|Camera|BoxCollider|Seeker|Quaternion|Action|Func|RefBool|RefInt|Ref2Float|PropertyModifier|ObscuredBool|ObscuredInt|Vector2Int|Vector3Int|List<[^>]+>|[A-Z][a-zA-Z0-9_<>\[\]\.]*\[\])\s+\w+\([^)]*\))"',
        lambda m: '"' + translate_method(m.group(1)) + '"',
        content
    )
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'文件1处理完成: {output_path}')

def process_file2(input_path, output_path):
    """处理文件2 - 核心类详细定义.html"""
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 处理字段 - <div class="field-item">...</div>
    def replace_field_div(match):
        div_content = match.group(0)
        # 提取字段名 - 在</span>之后，</div>之前
        field_match = re.search(r'</span>\s*(\w+)\s*</div>', div_content)
        if field_match:
            field_name = field_match.group(1)
            translation = translations.get(field_name)
            if translation:
                # 在字段名后添加中文翻译
                new_div = div_content.replace(f'{field_name}</div>', f'{field_name} <span class="field-cn">({translation})</span></div>')
                return new_div
        return div_content
    
    # 处理方法 - <div class="method-item">...</div>
    def replace_method_div(match):
        div_content = match.group(0)
        # 提取方法名
        method_match = re.search(r'<span class="method-name">(\w+)</span>', div_content)
        if method_match:
            method_name = method_match.group(1)
            translation = translations.get(method_name)
            if translation:
                # 在方法名后添加中文翻译
                new_div = div_content.replace(f'>{method_name}</span>', f'>{method_name}</span><span class="method-cn"> ({translation})</span>')
                return new_div
            # 尝试生成翻译
            if method_name.startswith('get_'):
                prop = method_name[4:]
                new_div = div_content.replace(f'>{method_name}</span>', f'>{method_name}</span><span class="method-cn"> (获取{prop})</span>')
                return new_div
            elif method_name.startswith('set_'):
                prop = method_name[4:]
                new_div = div_content.replace(f'>{method_name}</span>', f'>{method_name}</span><span class="method-cn"> (设置{prop})</span>')
                return new_div
        return div_content
    
    content = re.sub(r'<div class="field-item">.*?</div>', replace_field_div, content, flags=re.DOTALL)
    content = re.sub(r'<div class="method-item">.*?</div>', replace_method_div, content, flags=re.DOTALL)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'文件2处理完成: {output_path}')

if __name__ == '__main__':
    base_path = r'd:\trae_project\UCF1.7修改大全\游戏逆向分析-相关信息\02-部分系统'
    
    # 处理文件1
    process_file1(
        f'{base_path}\\02-完整版可视化.html',
        f'{base_path}\\02-完整版可视化.html'
    )
    
    # 处理文件2
    process_file2(
        f'{base_path}\\03--核心类详细定义.html',
        f'{base_path}\\03--核心类详细定义.html'
    )
    
    print('所有文件处理完成!')
