import re
import os
import json
import time
import urllib.request
import urllib.parse
import sys

INPUT_DIR = r"d:\trae_project\UCF1.7修改大全\游戏源代码-游戏相关信息\类"
CACHE_FILE = r"d:\trae_project\UCF1.7修改大全\游戏源代码-游戏相关信息\translation_cache.json"

# 加载缓存
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        cache = json.load(f)
else:
    cache = {}

# CF射击游戏专业术语词典
CF_DICT = {
    # Unity/引擎
    'Vector3': '三维向量', 'Vector2': '二维向量', 'Vector4': '四维向量',
    'Quaternion': '四元数', 'GameObject': '游戏对象', 'Transform': '变换',
    'MonoBehaviour': 'MonoBehaviour', 'Rigidbody': '刚体', 'Collider': '碰撞器',
    'Renderer': '渲染器', 'Camera': '摄像机', 'Light': '光照',
    'Audio': '音频', 'Animation': '动画', 'Animator': '动画器',
    'ParticleSystem': '粒子系统', 'Sprite': '精灵', 'Texture': '纹理',
    'Material': '材质', 'Shader': '着色器', 'Mesh': '网格',
    'Scene': '场景', 'Prefab': '预制体', 'Coroutine': '协程',
    'SerializeField': '序列化字段', 'HideInInspector': '隐藏检查器',
    'Header': '标题', 'Range': '范围', 'Tooltip': '提示',
    
    # AI寻路
    'GraphNode': '图节点', 'PathNode': '路径节点', 'GridNode': '网格节点',
    'ABPath': 'AB路径', 'Path': '路径', 'Seeker': '寻路器',
    'NNConstraint': '最近节点约束', 'PathInterpolator': '路径插值器',
    'RVOController': 'RVO控制器', 'IMovementPlane': '移动平面接口',
    'Navmesh': '导航网格', 'Waypoint': '路点',
    'repathRate': '重新寻路频率', 'canSearch': '可搜索路径',
    'canMove': '可移动', 'maxSpeed': '最大速度',
    'gravity': '重力', 'groundMask': '地面层掩码',
    'orientation': '朝向模式', 'enableRotation': '启用旋转',
    'simulatedPosition': '模拟位置', 'simulatedRotation': '模拟旋转',
    'accumulatedMovementDelta': '累积移动增量',
    'velocity2D': '二维速度', 'verticalVelocity': '垂直速度',
    'updatePosition': '更新位置', 'updateRotation': '更新旋转',
    'lastDeltaTime': '上次增量时间', 'prevPosition': '上一位置',
    'lastDeltaPosition': '上次增量位置',
    'waitingForPathCalculation': '等待路径计算',
    'lastRepath': '上次重新寻路',
    'targetCompatibility': '目标兼容性',
    'startHasRun': '启动已运行',
    'ShapeGizmoColor': '辅助线颜色',
    'centerOffset': '中心偏移',
    'rotationIn2D': '2D旋转',
    'usingGravity': '使用重力',
    'destination': '目的地',
    'velocity': '速度',
    'desiredVelocity': '期望速度',
    'isStopped': '已停止',
    'onSearchPath': '搜索路径时',
    'shouldRecalculatePath': '应重新计算路径',
    'FindComponents': '查找组件',
    'Teleport': '瞬移',
    'CancelCurrentPathRequest': '取消当前路径请求',
    'MovementUpdate': '移动更新',
    'CalculatePathRequestEndpoints': '计算路径请求端点',
    'SearchPath': '搜索路径',
    'GetFeetPosition': '获取脚部位置',
    'SetPath': '设置路径',
    'ApplyGravity': '应用重力',
    'CalculateDeltaToMoveThisFrame': '计算本帧移动增量',
    'SimulateRotationTowards': '模拟朝方向旋转',
    'Move': '移动',
    'FinalizeMovement': '完成移动',
    'FinalizeRotation': '完成旋转',
    'FinalizePosition': '完成位置',
    'UpdateVelocity': '更新速度',
    'ClampToNavmesh': '限制到导航网格',
    'RaycastPosition': '射线检测位置',
    'OnDrawGizmosSelected': '绘制选中辅助线',
    'OnDrawGizmos': '绘制辅助线',
    'Reset': '重置',
    'ResetShape': '重置形状',
    'OnUpgradeSerializedData': '升级序列化数据',
    
    # 通用
    'startNode': '起始节点', 'endNode': '结束节点',
    'originalStartPoint': '原始起点', 'originalEndPoint': '原始终点',
    'startPoint': '起点', 'endPoint': '终点',
    'startIntPoint': '起始整数点',
    'calculatePartial': '计算部分路径',
    'partialBestTarget': '部分最佳目标',
    'endNodeCosts': '终点代价',
    'gridSpecialCaseNode': '网格特殊节点',
    'NNConstraintNone': '无最近节点约束',
    'hasEndPoint': '有终点',
    'Construct': '构造', 'Setup': '设置',
    'UpdateStartEnd': '更新起点终点',
    'GetConnectionSpecialCost': '获取连接特殊代价',
    'EndPointGridGraphSpecialCase': '终点网格图特殊情况',
    'SetFlagOnSurroundingGridNodes': '设置周围网格节点标志',
    'Prepare': '准备',
    'CompletePathIfStartIsValidTarget': '如果起点是有效目标则完成路径',
    'Initialize': '初始化', 'Cleanup': '清理',
    'CompleteWith': '完成于',
    'CalculateStep': '计算步骤',
    'DebugString': '调试字符串',
    'GetMovementVector': '获取移动向量',
    'TargetFound': '找到目标',
    
    # Tween动画
    'TweenType': '补间类型', 'tweenType': '补间类型',
    'sequencedPosition': '序列位置',
    'sequencedEndPosition': '序列结束位置',
    'TweenCallback': '补间回调',
    'onStart': '开始时',
    
    # 反作弊
    'ACTkDetectorBase': '反作弊检测器基类',
    'detectorsContainer': '检测器容器',
    'autoStart': '自动启动', 'keepAlive': '保持存活',
    'autoDispose': '自动释放',
    'CheatDetected': '检测到作弊',
    'detectionEvent': '检测事件',
    'detectionEventHasListener': '检测事件有监听器',
    'started': '已启动', 'isRunning': '运行中',
    'add_CheatDetected': '添加_检测到作弊',
    'remove_CheatDetected': '移除_检测到作弊',
    'get_IsRunning': '获取_是否运行中',
    'Start': '启动', 'OnEnable': '启用时',
    'OnDisable': '禁用时', 'OnApplicationQuit': '应用退出时',
    'OnDestroy': '销毁时',
    'OnCheatingDetected': '检测到作弊时',
    'Init': '初始化', 'DisposeInternal': '内部释放',
    'DetectorHasCallbacks': '检测器有回调',
    'StopDetectionInternal': '停止检测内部',
    'PauseDetector': '暂停检测器',
    'ResumeDetector': '恢复检测器',
    
    # 通用编程
    'Shuffle': '打乱', 'UnShuffle': '恢复打乱',
    'OnTargetReached': '到达目标时',
    'OnPathComplete': '路径完成时',
    'ConfigurePathSwitchInterpolation': '配置路径切换插值',
    'ConfigureNewPath': '配置新路径',
    'CalculateNextPosition': '计算下一个位置',
    'ForceSearchPath': '强制搜索路径',
    'reachedEndOfPath': '到达路径终点',
    'reachedDestination': '到达目的地',
    'remainingDistance': '剩余距离',
    'hasPath': '有路径', 'pathPending': '路径待处理',
    'Awake': '唤醒',
    'interpolatePathSwitches': '插值路径切换',
    'switchPathInterpolationSpeed': '切换路径插值速度',
    'previousMovementOrigin': '上次移动起点',
    'previousMovementDirection': '上次移动方向',
    'pathSwitchInterpolationTime': '路径切换插值时间',
    'previousPosition1': '上一位置1', 'previousPosition2': '上一位置2',
    'maxAcceleration': '最大加速度',
    'slowdownDistance': '减速距离',
    'pickNextWaypointDist': '选取下一个路点距离',
    'endReachedDistance': '到达终点距离',
    'alwaysDrawGizmos': '始终绘制辅助线',
    'slowWhenNotFacingTarget': '未面向目标时减速',
    'whenCloseToDestination': '接近目的地时',
    'constrainInsideGraph': '限制在图内',
    'cachedNNConstraint': '缓存的最近节点约束',
}

def translate_with_cf_dict(text):
    """使用CF词典翻译"""
    if text in CF_DICT:
        return CF_DICT[text]
    if text in cache:
        return cache[text]
    return None

def process_file(filepath):
    """处理一个MD文件"""
    fname = os.path.basename(filepath)
    print(f"处理 {fname}...", flush=True)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找出所有需要翻译的术语
    terms_to_translate = []
    for match in re.finditer(r'（([^）]+)）', content):
        inner = match.group(1)
        # 跳过已经是中文的
        chinese_count = len(re.findall(r'[\u4e00-\u9fff]', inner))
        if chinese_count < len(inner) * 0.5:
            if translate_with_cf_dict(inner) is None:
                terms_to_translate.append(inner)
    
    # 去重
    seen = set()
    unique_terms = []
    for t in terms_to_translate:
        if t not in seen:
            seen.add(t)
            unique_terms.append(t)
    
    print(f"  找到 {len(unique_terms)} 个需要翻译的术语", flush=True)
    
    # 用CF词典替换
    def replace_term(match):
        inner = match.group(1)
        translated = translate_with_cf_dict(inner)
        if translated:
            return f"（{translated}）"
        return match.group(0)
    
    new_content = re.sub(r'（([^）]+)）', replace_term, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  完成: {fname}", flush=True)

# 处理前3个文件
for i in range(1, 4):
    fpath = os.path.join(INPUT_DIR, f"classes_part{i:03d}.md")
    if os.path.exists(fpath):
        process_file(fpath)

print(f"\n批次完成", flush=True)
