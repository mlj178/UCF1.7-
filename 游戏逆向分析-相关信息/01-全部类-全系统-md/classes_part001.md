# 游戏类定义 (Part 1/21)

共 200 个类 (总序号 1 - 200)

---

## ABPath（AB路径）

**继承**: Path（路径）

### 字段 (12)

- `GraphNode startNode`（Graph节点 start节点）(偏移: 0x78)
- `GraphNode endNode`（Graph节点 end节点）(偏移: 0x7C)
- `Vector3 originalStartPoint`（三维向量 original开始Point）(偏移: 0x80)
- `Vector3 originalEndPoint`（三维向量 original结束Point）(偏移: 0x8C)
- `Vector3 startPoint`（三维向量 起点）(偏移: 0x98)
- `Vector3 endPoint`（三维向量 终点）(偏移: 0xA4)
- `Int3 startIntPoint`（Int3 start整数Point）(偏移: 0xB0)
- `bool calculatePartial`（bool calculatePartial）(偏移: 0xBC)
- `PathNode partialBestTarget`（路径节点 partialBest目标）(偏移: 0xC0)
- `int[] endNodeCosts`（int[] end节点Costs）(偏移: 0xC4)
- `GridNode gridSpecialCaseNode`（网格节点 grid特殊Case节点）(偏移: 0xC8)
- `NNConstraint NNConstraintNone`（NNConstraint NNConstraint无）(偏移: 0x0)

### 方法 (16)

- `bool get_hasEndPoint()`
  （bool get_has结束Point（））
- `ABPath Construct(Vector3 start, Vector3 end, OnPathDelegate callback)`
  （AB路径 Construct（三维向量 start, 三维向量 end, On路径委托 callback））
- `void Setup(Vector3 start, Vector3 end, OnPathDelegate callbackDelegate)`
  （void Setup（三维向量 start, 三维向量 end, On路径委托 callbackDelegate））
- `void UpdateStartEnd(Vector3 start, Vector3 end)`
  （void 更新开始结束（三维向量 start, 三维向量 end））
- `uint GetConnectionSpecialCost(GraphNode a, GraphNode b, uint currentCost)`
  （uint 获取连接特殊Cost（Graph节点 a, Graph节点 b, uint currentCost））
- `void Reset()`
  （void 重置（））
- `bool EndPointGridGraphSpecialCase(GraphNode closestWalkableEndNode)`
  （bool 结束Point网格Graph特殊Case（Graph节点 closestWalkableEndNode））
- `void SetFlagOnSurroundingGridNodes(GridNode gridNode, int flag, bool flagState)`
  （void 集合标志OnSurrounding网格Nodes（网格节点 gridNode, int flag, bool flagState））
- `void Prepare()`
  （void 准备（））
- `void CompletePathIfStartIsValidTarget()`
  （void Complete路径If开始是否Valid目标（））
- `void Initialize()`
  （void 初始化（））
- `void Cleanup()`
  （void 清理（））
- `void CompleteWith(GraphNode node)`
  （void CompleteWith（Graph节点 node））
- `void CalculateStep(long targetTick)`
  （void 计算步骤（长整数 targetTick））
- `string DebugString(PathLog logMode)`
  （string Debug字符串（路径Log logMode））
- `Vector3 GetMovementVector(Vector3 point)`
  （三维向量 获取Movement向量（三维向量 point））

---

## ABPathEndingCondition（AB路径EndingCondition）

**继承**: PathEndingCondition（路径EndingCondition）

### 字段 (1)

- `ABPath abPath`（AB路径 ab路径）(偏移: 0xC)

### 方法 (1)

- `bool TargetFound(PathNode node)`
  （bool 目标Found（路径节点 node））

---

## ABSSequentiable（ABSSequentiable）

### 字段 (4)

- `TweenType tweenType`（Tween类型 tween类型）(偏移: 0x8)
- `float sequencedPosition`（float sequencedPosition）(偏移: 0xC)
- `float sequencedEndPosition`（float sequenced结束Position）(偏移: 0x10)
- `TweenCallback onStart`（Tween回调 on开始）(偏移: 0x14)

---

## ACTkByte16（ACTk字节16）

### 字段 (16)

- `byte b1`（byte b1）(偏移: 0x3C333C09)
- `byte b2`（byte b2）(偏移: 0x3C773C4D)
- `byte b3`（byte b3）(偏移: 0x3CBB3C91)
- `byte b4`（byte b4）(偏移: 0x3CFF3CD5)
- `byte b5`（byte b5）(偏移: 0x3D433D19)
- `byte b6`（byte b6）(偏移: 0x3D873D5D)
- `byte b7`（byte b7）(偏移: 0x3DCB3DA1)
- `byte b8`（byte b8）(偏移: 0x3E0F3DE5)
- `byte b9`（byte b9）(偏移: 0x3E533E29)
- `byte b10`（byte b10）(偏移: 0x3E973E6D)
- `byte b11`（byte b11）(偏移: 0x3EDB3EB1)
- `byte b12`（byte b12）(偏移: 0x3F1F3EF5)
- `byte b13`（byte b13）(偏移: 0x3F633F39)
- `byte b14`（byte b14）(偏移: 0x3FA73F7D)
- `byte b15`（byte b15）(偏移: 0x3FEB3FC1)
- `byte b16`（byte b16）(偏移: 0xECFF8)

---

## ACTkByte4（ACTkByte4）

### 字段 (4)

- `byte b1`（byte b1）(偏移: 0xF4)
- `byte b2`（byte b2）(偏移: 0x302F3005)
- `byte b3`（byte b3）(偏移: 0x30733049)
- `byte b4`（byte b4）(偏移: 0x30B7308D)

### 方法 (2)

- `void Shuffle()`
  （void Shuffle（））
- `void UnShuffle()`
  （void UnShuffle（））

---

## ACTkByte8（ACTkByte8）

### 字段 (8)

- `byte b1`（byte b1）(偏移: 0x30FB30D1)
- `byte b2`（byte b2）(偏移: 0x313F3115)
- `byte b3`（byte b3）(偏移: 0x31833159)
- `byte b4`（byte b4）(偏移: 0x31EB31B7)
- `byte b5`（byte b5）(偏移: 0x32303209)
- `byte b6`（byte b6）(偏移: 0x327B3247)
- `byte b7`（byte b7）(偏移: 0x32BE3297)
- `byte b8`（byte b8）(偏移: 0x32FC32D5)

### 方法 (2)

- `void Shuffle()`
  （void Shuffle（））
- `void UnShuffle()`
  （void UnShuffle（））

---

## ACTkDetectorBase（反作弊检测器基类）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (9)

- `GameObject detectorsContainer`（游戏对象 detectors容器）(偏移: 0x0)
- `bool autoStart`（bool auto开始）(偏移: 0xC)
- `bool keepAlive`（bool keepAlive）(偏移: 0xD)
- `bool autoDispose`（bool auto释放）(偏移: 0xE)
- `Action CheatDetected`（动作 CheatDetected）(偏移: 0x10)
- `UnityEvent detectionEvent`（Unity引擎事件 detection事件）(偏移: 0x14)
- `bool detectionEventHasListener`（bool detection事件是否有监听器）(偏移: 0x18)
- `bool started`（bool started）(偏移: 0x19)
- `bool isRunning`（bool isRunning）(偏移: 0x1A)

### 方法 (15)

- `void add_CheatDetected(Action value)`
  （void add_CheatDetected（动作 value））
- `void remove_CheatDetected(Action value)`
  （void remove_CheatDetected（动作 value））
- `bool get_IsRunning()`
  （bool get_是否Running（））
- `void Start()`
  （void 开始（））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `void OnApplicationQuit()`
  （void 应用退出时（））
- `void OnDestroy()`
  （void 销毁时（））
- `void OnCheatingDetected()`
  （void OnCheatingDetected（））
- `bool Init(ACTkDetectorBase instance, string detectorName)`
  （bool 初始化（ACTkDetector基础 instance, string detectorName））
- `void DisposeInternal()`
  （void 释放内部（））
- `bool DetectorHasCallbacks()`
  （bool Detector是否有Callbacks（））
- `void StopDetectionInternal()`
  （void 停止Detection内部的（））
- `void PauseDetector()`
  （void 暂停Detector（））
- `bool ResumeDetector()`
  （bool 恢复Detector（））

---

## AIBase（AI基础）

**继承**: VersionedMonoBehaviour（版本化MonoBehaviour）

### 字段 (35)

- `float radius`（浮点数 半径）(偏移: 0x10)
- `float height`（浮点数 高度）(偏移: 0x14)
- `float repathRate`（浮点数 重新寻路频率）(偏移: 0x18)
- `bool canSearch`（bool can搜索）(偏移: 0x1C)
- `bool canMove`（bool can移动）(偏移: 0x1D)
- `float maxSpeed`（float maxSpeed）(偏移: 0x20)
- `Vector3 gravity`（三维向量 gravity）(偏移: 0x24)
- `LayerMask groundMask`（层掩码 ground掩码）(偏移: 0x30)
- `float centerOffsetCompatibility`（float centerOffsetCompatibility）(偏移: 0x34)
- `OrientationMode orientation`（Orientation模式 orientation）(偏移: 0x38)
- `bool enableRotation`（布尔值 启用旋转）(偏移: 0x3C)
- `Vector3 simulatedPosition`（三维向量 simulatedPosition）(偏移: 0x40)
- `Quaternion simulatedRotation`（四元数 模拟旋转）(偏移: 0x4C)
- `Vector3 accumulatedMovementDelta`（三维向量 accumulatedMovementDelta）(偏移: 0x5C)
- `Vector2 velocity2D`（二维向量 velocity2D）(偏移: 0x68)
- `float verticalVelocity`（float vertical速度）(偏移: 0x70)
- `Seeker seeker`（寻路器 seeker）(偏移: 0x74)
- `Transform tr`（变换 tr）(偏移: 0x78)
- `Rigidbody rigid`（刚体 rigid）(偏移: 0x7C)
- `Rigidbody2D rigid2D`（Rigidbody2D rigid2D）(偏移: 0x80)
- `CharacterController controller`（角色控制器 controller）(偏移: 0x84)
- `RVOController rvoController`（RVO控制器 rvo控制器）(偏移: 0x88)
- `IMovementPlane movementPlane`（IMovementPlane movementPlane）(偏移: 0x8C)
- `bool updatePosition`（布尔值 更新位置）(偏移: 0x90)
- `bool updateRotation`（布尔值 更新旋转）(偏移: 0x91)
- `float lastDeltaTime`（float lastDelta时间）(偏移: 0x94)
- `int prevFrame`（整数 上一帧）(偏移: 0x98)
- `Vector3 prevPosition1`（三维向量 prevPosition1）(偏移: 0x9C)
- `Vector3 prevPosition2`（三维向量 prevPosition2）(偏移: 0xA8)
- `Vector2 lastDeltaPosition`（二维向量 lastDeltaPosition）(偏移: 0xB4)
- `bool waitingForPathCalculation`（bool waitingFor路径Calculation）(偏移: 0xBC)
- `float lastRepath`（浮点数 上次重新寻路）(偏移: 0xC0)
- `Transform targetCompatibility`（变换 targetCompatibility）(偏移: 0xC4)
- `bool startHasRun`（bool start是否有运行）(偏移: 0xC8)
- `Color ShapeGizmoColor`（颜色 ShapeGizmo颜色）(偏移: 0x0)

### 方法 (49)

- `float get_centerOffset()`
  （浮点数 获取_中心偏移（））
- `void set_centerOffset(float value)`
  （void 设置_中心偏移（浮点数 value））
- `bool get_rotationIn2D()`
  （布尔值 获取_2D旋转（））
- `void set_rotationIn2D(bool value)`
  （void 设置_2D旋转（布尔值 value））
- `Vector3 get_position()`
  （三维向量 获取_位置（））
- `Quaternion get_rotation()`
  （四元数 获取_旋转（））
- `bool get_usingGravity()`
  （bool get_using重力（））
- `void set_usingGravity(bool value)`
  （void set_using重力（bool value））
- `Transform get_target()`
  （变换 get_target（））
- `void set_target(Transform value)`
  （void set_target（变换 value））
- `Vector3 get_destination()`
  （三维向量 get_destination（））
- `void set_destination(Vector3 value)`
  （void set_destination（三维向量 value））
- `Vector3 get_velocity()`
  （三维向量 获取_速度（））
- `Vector3 get_desiredVelocity()`
  （三维向量 get_desired速度（））
- `bool get_isStopped()`
  （布尔值 获取_已停止（））
- `void set_isStopped(bool value)`
  （void 设置_已停止（布尔值 value））
- `Action get_onSearchPath()`
  （动作 get_on搜索路径（））
- `void set_onSearchPath(Action value)`
  （void set_on搜索路径（动作 value））
- `bool get_shouldRecalculatePath()`
  （bool get_shouldRecalculate路径（））
- `void FindComponents()`
  （void 查找Components（））
- `void OnEnable()`
  （void 启用时（））
- `void Start()`
  （void 开始（））
- `void Init()`
  （void 初始化（））
- `void Teleport(Vector3 newPosition, bool clearPath = True)`
  （void Teleport（三维向量 newPosition, bool clearPath = True））
- `void CancelCurrentPathRequest()`
  （void 取消当前路径请求（））
- `void OnDisable()`
  （void 禁用时（））
- `void Update()`
  （void 更新（））
- `void FixedUpdate()`
  （void 固定更新（））
- `void MovementUpdate(float deltaTime, out Vector3 nextPosition, out Quaternion nextRotation)`
  （void Movement更新（float deltaTime, out Vector3 nextPosition, out Quaternion nextRotation））
- `void CalculatePathRequestEndpoints(out Vector3 start, out Vector3 end)`
  （void 计算路径请求Endpoints（out Vector3 start, out Vector3 end））
- `void SearchPath()`
  （void 搜索路径（））
- `Vector3 GetFeetPosition()`
  （三维向量 获取FeetPosition（））
- `void SetPath(Path path)`
  （void 集合路径（路径 path））
- `void ApplyGravity(float deltaTime)`
  （void 应用重力（float deltaTime））
- `Vector2 CalculateDeltaToMoveThisFrame(Vector2 position, float distanceToEndOfPath, float deltaTime)`
  （二维向量 计算DeltaTo移动ThisFrame（二维向量 position, float distanceToEndOfPath, float deltaTime））
- `Quaternion SimulateRotationTowards(Vector3 direction, float maxDegrees)`
  （Quaternion SimulateRotationTowards（三维向量 direction, float maxDegrees））
- `Quaternion SimulateRotationTowards(Vector2 direction, float maxDegrees)`
  （Quaternion SimulateRotationTowards（二维向量 direction, float maxDegrees））
- `void Move(Vector3 deltaPosition)`
  （void 移动（三维向量 deltaPosition））
- `void FinalizeMovement(Vector3 nextPosition, Quaternion nextRotation)`
  （void FinalizeMovement（三维向量 nextPosition, Quaternion nextRotation））
- `void FinalizeRotation(Quaternion nextRotation)`
  （void 完成旋转（四元数 nextRotation））
- `void FinalizePosition(Vector3 nextPosition)`
  （void FinalizePosition（三维向量 nextPosition））
- `void UpdateVelocity()`
  （void 更新速度（））
- `Vector3 ClampToNavmesh(Vector3 position, out bool positionChanged)`
  （三维向量 ClampToNavmesh（三维向量 position, out bool positionChanged））
- `Vector3 RaycastPosition(Vector3 position, float lastElevation)`
  （三维向量 RaycastPosition（三维向量 position, float lastElevation））
- `void OnDrawGizmosSelected()`
  （void 绘制选中辅助线时（））
- `void OnDrawGizmos()`
  （void 绘制辅助线时（））
- `void Reset()`
  （void 重置（））
- `void ResetShape()`
  （void 重置Shape（））
- `int OnUpgradeSerializedData(int version, bool unityThread)`
  （整数 升级序列化数据（整数 version, 布尔值 unityThread））

---

## AIDestinationSetter（AIDestinationSetter）

**继承**: VersionedMonoBehaviour（版本化MonoBehaviour）

### 字段 (2)

- `Transform target`（变换 目标）(偏移: 0x10)
- `IAstarAI ai`（IAstarAI ai）(偏移: 0x14)

### 方法 (3)

- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `void Update()`
  （void 更新（））

---

## AILerp（AILerp）

**继承**: VersionedMonoBehaviour, IAstarAI（VersionedMonoBehaviour, IAstarAI）

### 字段 (26)

- `float repathRate`（浮点数 重新寻路频率）(偏移: 0x10)
- `bool canSearch`（bool can搜索）(偏移: 0x14)
- `bool canMove`（bool can移动）(偏移: 0x15)
- `float speed`（浮点数 速度）(偏移: 0x18)
- `OrientationMode orientation`（Orientation模式 orientation）(偏移: 0x1C)
- `bool enableRotation`（布尔值 启用旋转）(偏移: 0x20)
- `float rotationSpeed`（浮点数 旋转速度）(偏移: 0x24)
- `bool interpolatePathSwitches`（bool interpolate路径Switches）(偏移: 0x28)
- `float switchPathInterpolationSpeed`（float switch路径InterpolationSpeed）(偏移: 0x2C)
- `bool updatePosition`（布尔值 更新位置）(偏移: 0x40)
- `bool updateRotation`（布尔值 更新旋转）(偏移: 0x41)
- `Seeker seeker`（寻路器 seeker）(偏移: 0x48)
- `Transform tr`（变换 tr）(偏移: 0x4C)
- `float lastRepath`（浮点数 上次重新寻路）(偏移: 0x50)
- `ABPath path`（AB路径 path）(偏移: 0x54)
- `bool canSearchAgain`（bool can搜索Again）(偏移: 0x58)
- `Vector3 previousMovementOrigin`（三维向量 previousMovementOrigin）(偏移: 0x5C)
- `Vector3 previousMovementDirection`（三维向量 previousMovement方向）(偏移: 0x68)
- `float pathSwitchInterpolationTime`（float pathSwitchInterpolation时间）(偏移: 0x74)
- `PathInterpolator interpolator`（路径Interpolator interpolator）(偏移: 0x78)
- `bool startHasRun`（bool start是否有运行）(偏移: 0x7C)
- `Vector3 previousPosition1`（三维向量 previousPosition1）(偏移: 0x80)
- `Vector3 previousPosition2`（三维向量 previousPosition2）(偏移: 0x8C)
- `Vector3 simulatedPosition`（三维向量 simulatedPosition）(偏移: 0x98)
- `Quaternion simulatedRotation`（四元数 模拟旋转）(偏移: 0xA4)
- `Transform targetCompatibility`（变换 targetCompatibility）(偏移: 0xB4)

### 方法 (40)

- `bool get_rotationIn2D()`
  （布尔值 获取_2D旋转（））
- `void set_rotationIn2D(bool value)`
  （void 设置_2D旋转（布尔值 value））
- `bool get_reachedEndOfPath()`
  （bool get_reached结束Of路径（））
- `void set_reachedEndOfPath(bool value)`
  （void set_reached结束Of路径（bool value））
- `bool get_reachedDestination()`
  （布尔值 获取_到达目的地（））
- `Vector3 get_destination()`
  （三维向量 get_destination（））
- `void set_destination(Vector3 value)`
  （void set_destination（三维向量 value））
- `Transform get_target()`
  （变换 get_target（））
- `void set_target(Transform value)`
  （void set_target（变换 value））
- `Vector3 get_position()`
  （三维向量 获取_位置（））
- `Quaternion get_rotation()`
  （四元数 获取_旋转（））
- `float get_remainingDistance()`
  （浮点数 获取_剩余距离（））
- `void set_remainingDistance(float value)`
  （void set_remaining距离（float value））
- `bool get_hasPath()`
  （bool get_has路径（））
- `bool get_pathPending()`
  （布尔值 获取_路径待处理（））
- `bool get_isStopped()`
  （布尔值 获取_已停止（））
- `void set_isStopped(bool value)`
  （void 设置_已停止（布尔值 value））
- `Action get_onSearchPath()`
  （动作 get_on搜索路径（））
- `void set_onSearchPath(Action value)`
  （void set_on搜索路径（动作 value））
- `void Awake()`
  （void 唤醒（））
- `void Start()`
  （void 开始（））
- `void OnEnable()`
  （void 启用时（））
- `void Init()`
  （void 初始化（））
- `void OnDisable()`
  （void 禁用时（））
- `void Teleport(Vector3 position, bool clearPath = True)`
  （void Teleport（三维向量 position, bool clearPath = True））
- `bool get_shouldRecalculatePath()`
  （bool get_shouldRecalculate路径（））
- `void ForceSearchPath()`
  （void 强制搜索路径（））
- `void SearchPath()`
  （void 搜索路径（））
- `void OnTargetReached()`
  （void 到达目标时（））
- `void OnPathComplete(Path _p)`
  （void On路径Complete（路径 _p））
- `void SetPath(Path path)`
  （void 集合路径（路径 path））
- `void ConfigurePathSwitchInterpolation()`
  （void Configure路径SwitchInterpolation（））
- `Vector3 GetFeetPosition()`
  （三维向量 获取FeetPosition（））
- `void ConfigureNewPath()`
  （void Configure新的路径（））
- `void Update()`
  （void 更新（））
- `void MovementUpdate(float deltaTime, out Vector3 nextPosition, out Quaternion nextRotation)`
  （void Movement更新（float deltaTime, out Vector3 nextPosition, out Quaternion nextRotation））
- `void FinalizeMovement(Vector3 nextPosition, Quaternion nextRotation)`
  （void FinalizeMovement（三维向量 nextPosition, Quaternion nextRotation））
- `Quaternion SimulateRotationTowards(Vector3 direction, float deltaTime)`
  （Quaternion SimulateRotationTowards（三维向量 direction, float deltaTime））
- `Vector3 CalculateNextPosition(out Vector3 direction, float deltaTime)`
  （三维向量 计算下一个Position（out Vector3 direction, float deltaTime））
- `int OnUpgradeSerializedData(int version, bool unityThread)`
  （整数 升级序列化数据（整数 version, 布尔值 unityThread））

---

## AIPath（AI路径）

**继承**: AIBase, IAstarAI（AI基础, IAstarAI）

### 字段 (12)

- `float maxAcceleration`（float max加速度）(偏移: 0xE0)
- `float rotationSpeed`（浮点数 旋转速度）(偏移: 0xE4)
- `float slowdownDistance`（float slowdown距离）(偏移: 0xE8)
- `float pickNextWaypointDist`（float pick下一个WaypointDist）(偏移: 0xEC)
- `float endReachedDistance`（float endReached距离）(偏移: 0xF0)
- `bool alwaysDrawGizmos`（布尔值 始终绘制辅助线）(偏移: 0xF4)
- `bool slowWhenNotFacingTarget`（bool slowWhenNotFacing目标）(偏移: 0xF5)
- `CloseToDestinationMode whenCloseToDestination`（关闭ToDestination模式 when关闭ToDestination）(偏移: 0xF8)
- `bool constrainInsideGraph`（布尔值 限制在图内）(偏移: 0xFC)
- `Path path`（路径 path）(偏移: 0x100)
- `PathInterpolator interpolator`（路径Interpolator interpolator）(偏移: 0x104)
- `NNConstraint cachedNNConstraint`（NN约束 cachedNN约束）(偏移: 0x0)

### 方法 (22)

- `void Teleport(Vector3 newPosition, bool clearPath = True)`
  （void Teleport（三维向量 newPosition, bool clearPath = True））
- `float get_remainingDistance()`
  （浮点数 获取_剩余距离（））
- `bool get_reachedDestination()`
  （布尔值 获取_到达目的地（））
- `bool get_reachedEndOfPath()`
  （bool get_reached结束Of路径（））
- `void set_reachedEndOfPath(bool value)`
  （void set_reached结束Of路径（bool value））
- `bool get_hasPath()`
  （bool get_has路径（））
- `bool get_pathPending()`
  （布尔值 获取_路径待处理（））
- `Vector3 get_steeringTarget()`
  （三维向量 get_steering目标（））
- `void OnDisable()`
  （void 禁用时（））
- `void OnTargetReached()`
  （void 到达目标时（））
- `void OnPathComplete(Path newPath)`
  （void 路径完成时（路径 newPath））
- `void MovementUpdateInternal(float deltaTime, out Vector3 nextPosition, out Quaternion nextRotation)`
  （void Movement更新内部的（float deltaTime, out Vector3 nextPosition, out Quaternion nextRotation））
- `void CalculateNextRotation(float slowdown, out Quaternion nextRotation)`
  （void 计算下一个Rotation（float slowdown, out Quaternion nextRotation））
- `Vector3 ClampToNavmesh(Vector3 position, out bool positionChanged)`
  （三维向量 ClampToNavmesh（三维向量 position, out bool positionChanged））
- `int OnUpgradeSerializedData(int version, bool unityThread)`
  （整数 升级序列化数据（整数 version, 布尔值 unityThread））
- `bool get_TargetReached()`
  （bool get_目标Reached（））
- `float get_turningSpeed()`
  （float get_turningSpeed（））
- `void set_turningSpeed(float value)`
  （void set_turningSpeed（float value））
- `float get_speed()`
  （float get_speed（））
- `void set_speed(float value)`
  （void set_speed（float value））
- `Vector3 get_targetDirection()`
  （三维向量 get_target方向（））
- `Vector3 CalculateVelocity(Vector3 position)`
  （三维向量 计算速度（三维向量 position））

---

## APIUpdaterRuntimeHelpers（APIUpdaterRuntimeHelpers）

### 方法 (2)

- `bool GetMovedFromAttributeDataForType(Type sourceType, out string assembly, out string nsp, out string klass)`
  （bool 获取MovedFromAttribute数据For类型（类型 sourceType, out string assembly, out string nsp, out string klass））
- `bool GetObsoleteTypeRedirection(Type sourceType, out string assemblyName, out string nsp, out string className)`
  （bool 获取Obsolete类型Redirection（类型 sourceType, out string assemblyName, out string nsp, out string className））

---

## ASCIIEncoding（ASCIIEncoding）

**继承**: Encoding（编码）

### 方法 (20)

- `void SetDefaultFallbacks()`
  （void 设置默认回退（））
- `int GetByteCount(char[] chars, int index, int count)`
  （整数 获取字节数量（字符[] chars, 整数 index, 整数 count））
- `int GetByteCount(string chars)`
  （int 获取Byte数量（string chars））
- `int GetByteCount(char* chars, int count)`
  （整数 获取字节数量（字符* chars, 整数 count））
- `int GetBytes(string chars, int charIndex, int charCount, byte[] bytes, int byteIndex)`
  （int 获取Bytes（string chars, int charIndex, int charCount, byte[] bytes, int byteIndex））
- `int GetBytes(char[] chars, int charIndex, int charCount, byte[] bytes, int byteIndex)`
  （整数 获取字节（字符[] chars, 整数 charIndex, 整数 charCount, 字节[] bytes, 整数 byteIndex））
- `int GetBytes(char* chars, int charCount, byte* bytes, int byteCount)`
  （整数 获取字节（字符* chars, 整数 charCount, 字节* bytes, 整数 byteCount））
- `int GetCharCount(byte[] bytes, int index, int count)`
  （整数 获取字符数量（字节[] bytes, 整数 index, 整数 count））
- `int GetCharCount(byte* bytes, int count)`
  （整数 获取字符数量（字节* bytes, 整数 count））
- `int GetChars(byte[] bytes, int byteIndex, int byteCount, char[] chars, int charIndex)`
  （整数 获取字符（字节[] bytes, 整数 byteIndex, 整数 byteCount, 字符[] chars, 整数 charIndex））
- `int GetChars(byte* bytes, int byteCount, char* chars, int charCount)`
  （整数 获取字符（字节* bytes, 整数 byteCount, 字符* chars, 整数 charCount））
- `string GetString(byte[] bytes, int byteIndex, int byteCount)`
  （string 获取字符串（byte[] bytes, int byteIndex, int byteCount））
- `int GetByteCount(char* chars, int charCount, EncoderNLS encoder)`
  （int 获取Byte数量（char* chars, int charCount, EncoderNLS encoder））
- `int GetBytes(char* chars, int charCount, byte* bytes, int byteCount, EncoderNLS encoder)`
  （整数 获取字节（字符* chars, 整数 charCount, 字节* bytes, 整数 byteCount, 编码器NLS encoder））
- `int GetCharCount(byte* bytes, int count, DecoderNLS decoder)`
  （int 获取Char数量（byte* bytes, int count, DecoderNLS decoder））
- `int GetChars(byte* bytes, int byteCount, char* chars, int charCount, DecoderNLS decoder)`
  （int 获取Chars（byte* bytes, int byteCount, char* chars, int charCount, DecoderNLS decoder））
- `int GetMaxByteCount(int charCount)`
  （整数 获取_最大字节数量（整数 charCount））
- `int GetMaxCharCount(int byteCount)`
  （整数 获取_最大字符数量（整数 byteCount））
- `Decoder GetDecoder()`
  （解码器 获取解码器（））
- `Encoder GetEncoder()`
  （编码器 获取编码器（））

---

## ASN1（ASN1）

### 字段 (3)

- `byte m_nTag`（byte m_n标签）(偏移: 0x8)
- `byte[] m_aValue`（byte[] m_a值）(偏移: 0xC)
- `ArrayList elist`（数组列表 elist）(偏移: 0x10)

### 方法 (10)

- `int get_Count()`
  （整数 获取_数量（））
- `byte get_Tag()`
  （byte get_标签（））
- `byte[] get_Value()`
  （byte[] get_值（））
- `void set_Value(byte[] value)`
  （void set_值（byte[] value））
- `ASN1 Add(ASN1 asn1)`
  （ASN1 添加（ASN1 asn1））
- `byte[] GetBytes()`
  （byte[] 获取Bytes（））
- `void Decode(byte[] asn1, ref int anPos, int anLength)`
  （void Decode（byte[] asn1, ref int anPos, int anLength））
- `void DecodeTLV(byte[] asn1, ref int pos, out byte tag, out int length, out byte[] content)`
  （void DecodeTLV（byte[] asn1, ref int pos, out byte tag, out int length, out byte[] content））
- `ASN1 get_Item(int index)`
  （ASN1 get_项目（int index））
- `string ToString()`
  （字符串 转字符串（））

---

## ASN1Convert（ASN1转换）

### 方法 (3)

- `ASN1 FromInt32(int value)`
  （ASN1 FromInt32（int value））
- `int ToInt32(ASN1 asn1)`
  （int ToInt32（ASN1 asn1））
- `string ToOid(ASN1 asn1)`
  （string ToOid（ASN1 asn1））

---

## AS_AnimEndAction（AS_动画结束动作）

**继承**: StateMachineBehaviour（状态MachineBehaviour）

### 字段 (1)

- `bool isEnd`（bool is结束）(偏移: 0xC)

### 方法 (1)

- `void OnStateUpdate(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)`
  （void On状态更新（动画器 animator, 动画器状态信息 stateInfo, int layerIndex））

---

## AbandonedMutexException（AbandonedMutexException）

**继承**: SystemException（系统异常）

### 字段 (2)

- `int m_MutexIndex`（int m_Mutex索引）(偏移: 0x44)
- `Mutex m_Mutex`（Mutex m_Mutex）(偏移: 0x48)

### 方法 (1)

- `void SetupException(int location, WaitHandle handle)`
  （void SetupException（int location, Wait句柄 handle））

---

## AbstractEventData（抽象的事件数据）

### 字段 (1)

- `bool m_Used`（bool m_Used）(偏移: 0x8)

### 方法 (3)

- `void Reset()`
  （void 重置（））
- `void Use()`
  （void Use（））
- `bool get_used()`
  （bool get_used（））

---

## Action（动作）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke()`
  （void 调用（））
- `IAsyncResult BeginInvoke(AsyncCallback callback, object object)`
  （I异步结果 开始调用（异步回调 callback, 对象 object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## ActivatedClientTypeEntry（Activated客户端类型Entry）

**继承**: TypeEntry（类型项）

### 字段 (2)

- `string applicationUrl`（string applicationUrl）(偏移: 0x10)
- `Type obj_type`（类型 obj_type）(偏移: 0x14)

### 方法 (4)

- `string get_ApplicationUrl()`
  （string get_ApplicationUrl（））
- `IContextAttribute[] get_ContextAttributes()`
  （IContextAttribute[] get_ContextAttributes（））
- `Type get_ObjectType()`
  （类型 get_对象类型（））
- `string ToString()`
  （字符串 转字符串（））

---

## ActivatedServiceTypeEntry（Activated服务类型Entry）

**继承**: TypeEntry（类型项）

### 字段 (1)

- `Type obj_type`（类型 obj_type）(偏移: 0x10)

### 方法 (2)

- `Type get_ObjectType()`
  （类型 get_对象类型（））
- `string ToString()`
  （字符串 转字符串（））

---

## ActivationServices（ActivationServices）

### 字段 (1)

- `IActivator _constructionActivator`（IActivator _constructionActivator）(偏移: 0x0)

### 方法 (8)

- `IActivator get_ConstructionActivator()`
  （IActivator get_ConstructionActivator（））
- `IMessage Activate(RemotingProxy proxy, ConstructionCall ctorCall)`
  （IMessage 激活（Remoting代理 proxy, ConstructionCall ctorCall））
- `IMessage RemoteActivate(IConstructionCallMessage ctorCall)`
  （IMessage Remote激活（IConstructionCallMessage ctorCall））
- `ConstructionCall CreateConstructionCall(Type type, string activationUrl, object[] activationAttributes)`
  （ConstructionCall 创建ConstructionCall（类型 type, string activationUrl, object[] activationAttributes））
- `IMessage CreateInstanceFromMessage(IConstructionCallMessage ctorCall)`
  （IMessage 创建实例FromMessage（IConstructionCallMessage ctorCall））
- `object CreateProxyForType(Type type)`
  （object 创建代理For类型（类型 type））
- `object AllocateUninitializedClassInstance(Type type)`
  （object AllocateUninitialized类实例（类型 type））
- `void EnableProxyActivation(Type type, bool enable)`
  （void 启用代理Activation（类型 type, bool enable））

---

## Activator（Activator）

### 方法 (5)

- `object CreateInstance(Type type, BindingFlags bindingAttr, Binder binder, object[] args, CultureInfo culture)`
  （object 创建实例（类型 type, BindingFlags bindingAttr, Binder binder, object[] args, Culture信息 culture））
- `object CreateInstance(Type type, BindingFlags bindingAttr, Binder binder, object[] args, CultureInfo culture, object[] activationAttributes)`
  （object 创建实例（类型 type, BindingFlags bindingAttr, Binder binder, object[] args, Culture信息 culture, object[] activationAttributes））
- `object CreateInstance(Type type, object[] args)`
  （object 创建实例（类型 type, object[] args））
- `object CreateInstance(Type type)`
  （object 创建实例（类型 type））
- `object CreateInstance(Type type, bool nonPublic)`
  （object 创建实例（类型 type, bool nonPublic））

---

## ActivityFilter（ActivityFilter）

**继承**: IDisposable（可释放接口）

### 字段 (7)

- `Guid m_providerGuid`（Guid m_providerGuid）(偏移: 0x10)
- `int m_eventId`（int m_eventId）(偏移: 0x20)
- `int m_samplingFreq`（int m_samplingFreq）(偏移: 0x24)
- `int m_curSampleCount`（int m_curSample数量）(偏移: 0x28)
- `int m_perEventSourceSessionId`（int m_per事件SourceSessionId）(偏移: 0x2C)
- `ActivityFilter m_next`（ActivityFilter m_next）(偏移: 0x30)
- `Action<Guid> m_myActivityDelegate`（Action<Guid> m_myActivity委托）(偏移: 0x34)

### 方法 (10)

- `void DisableFilter(ref ActivityFilter filterList, EventSource source)`
  （void 禁用Filter（ref ActivityFilter filterList, 事件Source source））
- `void UpdateFilter(ref ActivityFilter filterList, EventSource source, int perEventSourceSessionId, string startEvents)`
  （void 更新Filter（ref ActivityFilter filterList, 事件Source source, int perEventSourceSessionId, string startEvents））
- `bool PassesActivityFilter(ActivityFilter filterList, Guid* childActivityID, bool triggeringEvent, EventSource source, int eventId)`
  （bool PassesActivityFilter（ActivityFilter filterList, Guid* childActivityID, bool triggeringEvent, 事件Source source, int eventId））
- `void FlowActivityIfNeeded(ActivityFilter filterList, Guid* currentActivityId, Guid* childActivityID)`
  （void FlowActivityIfNeeded（ActivityFilter filterList, Guid* currentActivityId, Guid* childActivityID））
- `void UpdateKwdTriggers(ActivityFilter activityFilter, Guid sourceGuid, EventSource source, EventKeywords sessKeywords)`
  （void 更新KwdTriggers（ActivityFilter activityFilter, Guid sourceGuid, 事件Source source, 事件Keywords sessKeywords））
- `void Dispose()`
  （void 释放（））
- `void EnsureActivityCleanupDelegate(ActivityFilter filterList)`
  （void EnsureActivity清理委托（ActivityFilter filterList））
- `Action<Guid> GetActivityDyingDelegate(ActivityFilter filterList)`
  （Action<Guid> 获取ActivityDying委托（ActivityFilter filterList））
- `bool EnableFilter(ref ActivityFilter filterList, EventSource source, int perEventSourceSessionId, int eventId, int samplingFreq)`
  （bool 启用Filter（ref ActivityFilter filterList, 事件Source source, int perEventSourceSessionId, int eventId, int samplingFreq））
- `void TrimActiveActivityStore(ConcurrentDictionary<Guid, int> activities)`
  （void Trim激活的Activity商店（ConcurrentDictionary<Guid, int> activities））

---

## ActivityTracker（ActivityTracker）

### 字段 (4)

- `AsyncLocal<ActivityTracker.ActivityInfo> m_current`（异步Local<ActivityTracker.ActivityInfo> m_current）(偏移: 0x8)
- `bool m_checkedForEnable`（bool m_checkedFor启用）(偏移: 0xC)
- `ActivityTracker s_activityTrackerInstance`（ActivityTracker s_activityTracker实例）(偏移: 0x0)
- `long m_nextId`（long m_nextId）(偏移: 0x8)

### 方法 (7)

- `void OnStart(string providerName, string activityName, int task, ref Guid activityId, ref Guid relatedActivityId, EventActivityOptions options)`
  （void On开始（string providerName, string activityName, int task, ref Guid activityId, ref Guid relatedActivityId, 事件ActivityOptions options））
- `void OnStop(string providerName, string activityName, int task, ref Guid activityId)`
  （void On停止（string providerName, string activityName, int task, ref Guid activityId））
- `void Enable()`
  （void 启用（））
- `ActivityTracker get_Instance()`
  （ActivityTracker get_实例（））
- `ActivityTracker.ActivityInfo FindActiveActivity(string name, ActivityTracker.ActivityInfo startLocation)`
  （ActivityTracker.Activity信息 查找激活的Activity（string name, ActivityTracker.Activity信息 startLocation））
- `string NormalizeActivityName(string providerName, string activityName, int task)`
  （string NormalizeActivity名称（string providerName, string activityName, int task））
- `void ActivityChanging(AsyncLocalValueChangedArgs<ActivityTracker.ActivityInfo> args)`
  （void ActivityChanging（异步本地的值ChangedArgs<ActivityTracker.ActivityInfo> args））

---

## ActivityTracker.ActivityInfo（ActivityTracker.Activity信息）

### 字段 (10)

- `string m_name`（字符串 m_名称）(偏移: 0x8)
- `long m_uniqueId`（long m_uniqueId）(偏移: 0x10)
- `Guid m_guid`（Guid m_guid）(偏移: 0x18)
- `int m_activityPathGuidOffset`（int m_activity路径GuidOffset）(偏移: 0x28)
- `int m_level`（int m_level）(偏移: 0x2C)
- `EventActivityOptions m_eventOptions`（事件ActivityOptions m_eventOptions）(偏移: 0x30)
- `long m_lastChildID`（long m_last子级ID）(偏移: 0x38)
- `int m_stopped`（int m_stopped）(偏移: 0x40)
- `ActivityTracker.ActivityInfo m_creator`（ActivityTracker.Activity信息 m_creator）(偏移: 0x44)
- `Guid m_activityIdToRestore`（Guid m_activityIdToRestore）(偏移: 0x48)

### 方法 (9)

- `Guid get_ActivityId()`
  （Guid get_ActivityId（））
- `string Path(ActivityTracker.ActivityInfo activityInfo)`
  （string 路径（ActivityTracker.Activity信息 activityInfo））
- `string ToString()`
  （字符串 转字符串（））
- `string LiveActivities(ActivityTracker.ActivityInfo list)`
  （string LiveActivities（ActivityTracker.Activity信息 list））
- `bool CanBeOrphan()`
  （bool 能否BeOrphan（））
- `void CreateActivityPathGuid(out Guid idRet, out int activityPathGuidOffset)`
  （void 创建Activity路径Guid（out Guid idRet, out int activityPathGuidOffset））
- `void CreateOverflowGuid(Guid* outPtr)`
  （void 创建OverflowGuid（Guid* outPtr））
- `int AddIdToGuid(Guid* outPtr, int whereToAddId, uint id, bool overflow = False)`
  （int 添加IdToGuid（Guid* outPtr, int whereToAddId, uint id, bool overflow = False））
- `void WriteNibble(ref byte* ptr, byte* endPtr, uint value)`
  （void WriteNibble（ref byte* ptr, byte* endPtr, uint value））

---

## AddComponentMenu（添加组件菜单）

**继承**: Attribute（属性）

### 字段 (2)

- `string m_AddComponentMenu`（string m_添加组件菜单）(偏移: 0x8)
- `int m_Ordering`（int m_Ordering）(偏移: 0xC)

---

## AddProgressEventArgs（添加Progress事件Args）

**继承**: ZipProgressEventArgs（Zip进度事件参数）

### 方法 (1)

- `AddProgressEventArgs AfterEntry(string archiveName, ZipEntry entry, int entriesTotal)`
  （添加Progress事件Args AfterEntry（string archiveName, ZipEntry entry, int entriesTotal））

---

## AddSimpleRadarIcon（添加SimpleRadar图标）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (3)

- `Sprite iconSprite`（精灵 icon精灵）(偏移: 0xC)
- `bool addInMapMask`（bool addIn映射掩码）(偏移: 0x10)
- `bool maskable`（bool maskable）(偏移: 0x11)

### 方法 (1)

- `void Start()`
  （void 开始（））

---

## AdditionalLightsShadowCasterPass（AdditionalLightsShadowCasterPass）

**继承**: ScriptableRenderPass（可脚本化渲染通道）

### 字段 (16)

- `int m_AdditionalShadowsBufferId`（int m_AdditionalShadows缓冲区Id）(偏移: 0x0)
- `int m_AdditionalShadowsIndicesId`（int m_AdditionalShadowsIndicesId）(偏移: 0x4)
- `bool m_UseStructuredBuffer`（bool m_UseStructured缓冲区）(偏移: 0x54)
- `RenderTargetHandle m_AdditionalLightsShadowmap`（Render目标句柄 m_AdditionalLightsShadowmap）(偏移: 0x58)
- `RenderTexture m_AdditionalLightsShadowmapTexture`（Render纹理 m_AdditionalLightsShadowmap纹理）(偏移: 0x78)
- `int m_ShadowmapWidth`（int m_Shadowmap宽度）(偏移: 0x7C)
- `int m_ShadowmapHeight`（int m_Shadowmap高度）(偏移: 0x80)
- `ShadowSliceData[] m_AdditionalLightSlices`（ShadowSliceData[] m_Additional光照Slices）(偏移: 0x84)
- `Matrix4x4[] m_AdditionalLightsWorldToShadow`（Matrix4x4[] m_AdditionalLights世界的ToShadow）(偏移: 0x88)
- `Vector4[] m_AdditionalLightsShadowParams`（Vector4[] m_AdditionalLightsShadowParams）(偏移: 0x8C)
- `ShaderInput.ShadowData[] m_AdditionalLightsShadowData`（着色器Input.ShadowData[] m_AdditionalLightsShadow数据）(偏移: 0x90)
- `List<int> m_AdditionalShadowCastingLightIndices`（List<int> m_AdditionalShadowCasting光照Indices）(偏移: 0x94)
- `List<int> m_AdditionalShadowCastingLightIndicesMap`（List<int> m_AdditionalShadowCasting光照Indices映射）(偏移: 0x98)
- `List<int> m_ShadowCastingLightIndicesMap`（List<int> m_ShadowCasting光照Indices映射）(偏移: 0x9C)
- `bool m_SupportsBoxFilterForShadows`（bool m_SupportsBoxFilterForShadows）(偏移: 0xA0)
- `ProfilingSampler m_ProfilingSetupSampler`（ProfilingSampler m_ProfilingSetupSampler）(偏移: 0xA4)

### 方法 (9)

- `bool Setup(ref RenderingData renderingData)`
  （bool Setup（ref RenderingData renderingData））
- `void Configure(CommandBuffer cmd, RenderTextureDescriptor cameraTextureDescriptor)`
  （void 配置（命令缓冲区 cmd, 渲染纹理描述符 cameraTextureDescriptor））
- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（可脚本化渲染上下文 context, 引用 渲染数据 renderingData））
- `void OnCameraCleanup(CommandBuffer cmd)`
  （void 摄像机清理时（命令缓冲区 cmd））
- `int GetShadowLightIndexFromLightIndex(int visibleLightIndex)`
  （int 获取Shadow光照索引From光照索引（int visibleLightIndex））
- `void Clear()`
  （void 清除（））
- `void RenderAdditionalShadowmapAtlas(ref ScriptableRenderContext context, ref CullingResults cullResults, ref LightData lightData, ref ShadowData shadowData)`
  （void RenderAdditionalShadowmapAtlas（ref ScriptableRenderContext context, ref CullingResults cullResults, ref LightData lightData, ref ShadowData shadowData））
- `void SetupAdditionalLightsShadowReceiverConstants(CommandBuffer cmd, ref ShadowData shadowData, bool softShadows)`
  （void SetupAdditionalLightsShadowReceiverConstants（Command缓冲区 cmd, ref ShadowData shadowData, bool softShadows））
- `bool IsValidShadowCastingLight(ref LightData lightData, int i)`
  （bool 是否ValidShadowCasting光照（ref LightData lightData, int i））

---

## AdditionalLightsShadowCasterPass.AdditionalShadowsConstantBuffer（AdditionalLightsShadowCasterPass.AdditionalShadowsConstant缓冲区）

### 字段 (7)

- `int _AdditionalLightsWorldToShadow`（int _AdditionalLights世界的ToShadow）(偏移: 0x0)
- `int _AdditionalShadowParams`（int _AdditionalShadowParams）(偏移: 0x4)
- `int _AdditionalShadowOffset0`（int _AdditionalShadowOffset0）(偏移: 0x8)
- `int _AdditionalShadowOffset1`（int _AdditionalShadowOffset1）(偏移: 0xC)
- `int _AdditionalShadowOffset2`（int _AdditionalShadowOffset2）(偏移: 0x10)
- `int _AdditionalShadowOffset3`（int _AdditionalShadowOffset3）(偏移: 0x14)
- `int _AdditionalShadowmapSize`（int _AdditionalShadowmap大小）(偏移: 0x18)

---

## AddressFamily（AddressFamily）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Adler（Adler）

### 字段 (2)

- `uint BASE`（uint BASE）(偏移: 0x0)
- `int NMAX`（int NMAX）(偏移: 0x4)

### 方法 (1)

- `uint Adler32(uint adler, byte[] buf, int index, int len)`
  （uint Adler32（uint adler, byte[] buf, int index, int len））

---

## AdvancedSmooth（AdvancedSmooth）

**继承**: MonoModifier（Mono修改器）

### 字段 (3)

- `float turningRadius`（float turningRadius）(偏移: 0x14)
- `AdvancedSmooth.MaxTurn turnConstruct1`（AdvancedSmooth.最大Turn turnConstruct1）(偏移: 0x18)
- `AdvancedSmooth.ConstantTurn turnConstruct2`（AdvancedSmooth.ConstantTurn turnConstruct2）(偏移: 0x1C)

### 方法 (3)

- `int get_Order()`
  （整数 获取_顺序（））
- `void Apply(Path p)`
  （void 应用（路径 p））
- `void EvaluatePaths(List<AdvancedSmooth.Turn> turnList, List<Vector3> output)`
  （void EvaluatePaths（List<AdvancedSmooth.Turn> turnList, List<Vector3> output））

---

## AdvancedSmooth.ConstantTurn（AdvancedSmooth.ConstantTurn）

**继承**: AdvancedSmooth.TurnConstructor（AdvancedSmooth.TurnConstructor）

### 字段 (4)

- `Vector3 circleCenter`（三维向量 circle中心）(偏移: 0x10)
- `double gamma1`（double gamma1）(偏移: 0x20)
- `double gamma2`（double gamma2）(偏移: 0x28)
- `bool clockwise`（bool clockwise）(偏移: 0x30)

### 方法 (3)

- `void Prepare(int i, Vector3[] vectorPath)`
  （void Prepare（int i, Vector3[] vectorPath））
- `void TangentToTangent(List<AdvancedSmooth.Turn> turnList)`
  （void TangentToTangent（List<AdvancedSmooth.Turn> turnList））
- `void GetPath(AdvancedSmooth.Turn turn, List<Vector3> output)`
  （void 获取路径（AdvancedSmooth.Turn turn, List<Vector3> output））

---

## AdvancedSmooth.MaxTurn（AdvancedSmooth.最大Turn）

**继承**: AdvancedSmooth.TurnConstructor（AdvancedSmooth.TurnConstructor）

### 字段 (20)

- `Vector3 preRightCircleCenter`（三维向量 pre右Circle中心）(偏移: 0x10)
- `Vector3 preLeftCircleCenter`（三维向量 pre左Circle中心）(偏移: 0x1C)
- `Vector3 rightCircleCenter`（三维向量 rightCircle中心）(偏移: 0x28)
- `Vector3 leftCircleCenter`（三维向量 leftCircle中心）(偏移: 0x34)
- `double vaRight`（double va右）(偏移: 0x40)
- `double vaLeft`（double va左）(偏移: 0x48)
- `double preVaLeft`（double preVa左）(偏移: 0x50)
- `double preVaRight`（double preVa右）(偏移: 0x58)
- `double gammaLeft`（double gamma左）(偏移: 0x60)
- `double gammaRight`（double gamma右）(偏移: 0x68)
- `double betaRightRight`（double beta右右）(偏移: 0x70)
- `double betaRightLeft`（double beta右左）(偏移: 0x78)
- `double betaLeftRight`（double beta左右）(偏移: 0x80)
- `double betaLeftLeft`（double beta左左）(偏移: 0x88)
- `double deltaRightLeft`（double delta右左）(偏移: 0x90)
- `double deltaLeftRight`（double delta左右）(偏移: 0x98)
- `double alfaRightRight`（double alfa右右）(偏移: 0xA0)
- `double alfaLeftLeft`（double alfa左左）(偏移: 0xA8)
- `double alfaRightLeft`（double alfa右左）(偏移: 0xB0)
- `double alfaLeftRight`（double alfa左右）(偏移: 0xB8)

### 方法 (6)

- `void OnTangentUpdate()`
  （void OnTangent更新（））
- `void Prepare(int i, Vector3[] vectorPath)`
  （void Prepare（int i, Vector3[] vectorPath））
- `void TangentToTangent(List<AdvancedSmooth.Turn> turnList)`
  （void TangentToTangent（List<AdvancedSmooth.Turn> turnList））
- `void PointToTangent(List<AdvancedSmooth.Turn> turnList)`
  （void PointToTangent（List<AdvancedSmooth.Turn> turnList））
- `void TangentToPoint(List<AdvancedSmooth.Turn> turnList)`
  （void TangentToPoint（List<AdvancedSmooth.Turn> turnList））
- `void GetPath(AdvancedSmooth.Turn turn, List<Vector3> output)`
  （void 获取路径（AdvancedSmooth.Turn turn, List<Vector3> output））

---

## AdvancedSmooth.Turn（AdvancedSmooth.Turn）

**继承**: IComparable<AdvancedSmooth.Turn>（IComparable<AdvancedSmooth.Turn>）

### 字段 (3)

- `float length`（浮点数 长度）(偏移: 0x0)
- `int id`（整数 id）(偏移: 0x4)
- `AdvancedSmooth.TurnConstructor constructor`（AdvancedSmooth.TurnConstructor constructor）(偏移: 0x8)

### 方法 (5)

- `float get_score()`
  （float get_score（））
- `void GetPath(List<Vector3> output)`
  （void 获取路径（List<Vector3> output））
- `int CompareTo(AdvancedSmooth.Turn t)`
  （int CompareTo（AdvancedSmooth.Turn t））
- `bool op_LessThan(AdvancedSmooth.Turn lhs, AdvancedSmooth.Turn rhs)`
  （bool op_LessThan（AdvancedSmooth.Turn lhs, AdvancedSmooth.Turn rhs））
- `bool op_GreaterThan(AdvancedSmooth.Turn lhs, AdvancedSmooth.Turn rhs)`
  （bool op_GreaterThan（AdvancedSmooth.Turn lhs, AdvancedSmooth.Turn rhs））

---

## AdvancedSmooth.TurnConstructor（AdvancedSmooth.TurnConstructor）

### 字段 (11)

- `float constantBias`（float constantBias）(偏移: 0x8)
- `float factorBias`（float factorBias）(偏移: 0xC)
- `float turningRadius`（float turningRadius）(偏移: 0x0)
- `Vector3 prev`（三维向量 prev）(偏移: 0x4)
- `Vector3 current`（三维向量 current）(偏移: 0x10)
- `Vector3 next`（三维向量 next）(偏移: 0x1C)
- `Vector3 t1`（三维向量 t1）(偏移: 0x28)
- `Vector3 t2`（三维向量 t2）(偏移: 0x34)
- `Vector3 normal`（三维向量 normal）(偏移: 0x40)
- `Vector3 prevNormal`（三维向量 prev法线）(偏移: 0x4C)
- `bool changedPreviousTangent`（bool changed上一个Tangent）(偏移: 0x58)

### 方法 (16)

- `void OnTangentUpdate()`
  （void OnTangent更新（））
- `void PointToTangent(List<AdvancedSmooth.Turn> turnList)`
  （void PointToTangent（List<AdvancedSmooth.Turn> turnList））
- `void TangentToPoint(List<AdvancedSmooth.Turn> turnList)`
  （void TangentToPoint（List<AdvancedSmooth.Turn> turnList））
- `void TangentToTangent(List<AdvancedSmooth.Turn> turnList)`
  （void TangentToTangent（List<AdvancedSmooth.Turn> turnList））
- `void Setup(int i, Vector3[] vectorPath)`
  （void Setup（int i, Vector3[] vectorPath））
- `void PostPrepare()`
  （void PostPrepare（））
- `void AddCircleSegment(double startAngle, double endAngle, bool clockwise, Vector3 center, List<Vector3> output, float radius)`
  （void 添加CircleSegment（double startAngle, double endAngle, bool clockwise, 三维向量 center, List<Vector3> output, float radius））
- `void DebugCircleSegment(Vector3 center, double startAngle, double endAngle, double radius, Color color)`
  （void DebugCircleSegment（三维向量 center, double startAngle, double endAngle, double radius, 颜色 color））
- `void DebugCircle(Vector3 center, double radius, Color color)`
  （void DebugCircle（三维向量 center, double radius, 颜色 color））
- `double GetLengthFromAngle(double angle, double radius)`
  （double 获取LengthFrom角度（double angle, double radius））
- `double ClockwiseAngle(double from, double to)`
  （double Clockwise角度（double from, double to））
- `double CounterClockwiseAngle(double from, double to)`
  （double CounterClockwise角度（double from, double to））
- `Vector3 AngleToVector(double a)`
  （三维向量 角度To向量（double a））
- `double ToDegrees(double rad)`
  （double ToDegrees（double rad））
- `double ClampAngle(double a)`
  （double Clamp角度（double a））
- `double Atan2(Vector3 v)`
  （double Atan2（三维向量 v））

---

## AdvancingFront（Advancing前）

### 字段 (3)

- `AdvancingFrontNode Head`（Advancing前节点 头部）(偏移: 0x8)
- `AdvancingFrontNode Tail`（Advancing前节点 Tail）(偏移: 0xC)
- `AdvancingFrontNode Search`（Advancing前节点 搜索）(偏移: 0x10)

### 方法 (7)

- `void AddNode(AdvancingFrontNode node)`
  （void 添加节点（Advancing前节点 node））
- `void RemoveNode(AdvancingFrontNode node)`
  （void 移除节点（Advancing前节点 node））
- `string ToString()`
  （字符串 转字符串（））
- `AdvancingFrontNode FindSearchNode(double x)`
  （Advancing前节点 查找搜索节点（double x））
- `AdvancingFrontNode LocateNode(TriangulationPoint point)`
  （Advancing前节点 Locate节点（TriangulationPoint point））
- `AdvancingFrontNode LocateNode(double x)`
  （Advancing前节点 Locate节点（double x））
- `AdvancingFrontNode LocatePoint(TriangulationPoint point)`
  （Advancing前节点 LocatePoint（TriangulationPoint point））

---

## AdvancingFrontNode（Advancing前节点）

### 字段 (5)

- `AdvancingFrontNode Next`（Advancing前节点 下一个）(偏移: 0x8)
- `AdvancingFrontNode Prev`（Advancing前节点 Prev）(偏移: 0xC)
- `double Value`（double 值）(偏移: 0x10)
- `TriangulationPoint Point`（TriangulationPoint Point）(偏移: 0x18)
- `DelaunayTriangle Triangle`（DelaunayTriangle Triangle）(偏移: 0x1C)

### 方法 (2)

- `bool get_HasNext()`
  （bool get_是否有下一个（））
- `bool get_HasPrev()`
  （bool get_是否有Prev（））

---

## Aes（Aes）

**继承**: SymmetricAlgorithm（对称算法）

### 字段 (2)

- `KeySizes[] s_legalBlockSizes`（密钥大小[] s_合法块大小）(偏移: 0x0)
- `KeySizes[] s_legalKeySizes`（密钥大小[] s_合法密钥大小）(偏移: 0x4)

### 方法 (2)

- `Aes Create()`
  （Aes 创建（））
- `Aes Create(string algorithmName)`
  （Aes 创建（string algorithmName））

---

## AesCryptoServiceProvider（AesCrypto服务提供者）

**继承**: Aes（Aes）

### 方法 (16)

- `void GenerateIV()`
  （void 生成IV（））
- `void GenerateKey()`
  （void 生成密钥（））
- `ICryptoTransform CreateDecryptor(byte[] key, byte[] iv)`
  （ICrypto变换 创建Decryptor（byte[] key, byte[] iv））
- `ICryptoTransform CreateEncryptor(byte[] key, byte[] iv)`
  （ICrypto变换 创建Encryptor（byte[] key, byte[] iv））
- `byte[] get_IV()`
  （byte[] get_IV（））
- `void set_IV(byte[] value)`
  （void set_IV（byte[] value））
- `byte[] get_Key()`
  （字节[] 获取_键（））
- `void set_Key(byte[] value)`
  （void 设置_键（字节[] value））
- `int get_KeySize()`
  （整数 获取_键大小（））
- `void set_KeySize(int value)`
  （void 设置_键大小（整数 value））
- `int get_FeedbackSize()`
  （int get_Feedback大小（））
- `CipherMode get_Mode()`
  （Cipher模式 get_模式（））
- `PaddingMode get_Padding()`
  （Padding模式 get_Padding（））
- `void set_Padding(PaddingMode value)`
  （void set_Padding（Padding模式 value））
- `ICryptoTransform CreateEncryptor()`
  （ICrypto变换 创建Encryptor（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））

---

## AesManaged（AesManaged）

**继承**: Aes（Aes）

### 字段 (1)

- `RijndaelManaged m_rijndael`（RijndaelManaged m_rijndael）(偏移: 0x2C)

### 方法 (16)

- `int get_FeedbackSize()`
  （int get_Feedback大小（））
- `byte[] get_IV()`
  （byte[] get_IV（））
- `void set_IV(byte[] value)`
  （void set_IV（byte[] value））
- `byte[] get_Key()`
  （字节[] 获取_键（））
- `void set_Key(byte[] value)`
  （void 设置_键（字节[] value））
- `int get_KeySize()`
  （整数 获取_键大小（））
- `void set_KeySize(int value)`
  （void 设置_键大小（整数 value））
- `CipherMode get_Mode()`
  （Cipher模式 get_模式（））
- `PaddingMode get_Padding()`
  （Padding模式 get_Padding（））
- `void set_Padding(PaddingMode value)`
  （void set_Padding（Padding模式 value））
- `ICryptoTransform CreateDecryptor(byte[] key, byte[] iv)`
  （ICrypto变换 创建Decryptor（byte[] key, byte[] iv））
- `ICryptoTransform CreateEncryptor()`
  （ICrypto变换 创建Encryptor（））
- `ICryptoTransform CreateEncryptor(byte[] key, byte[] iv)`
  （ICrypto变换 创建Encryptor（byte[] key, byte[] iv））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `void GenerateIV()`
  （void 生成IV（））
- `void GenerateKey()`
  （void 生成密钥（））

---

## AesTransform（Aes变换）

**继承**: SymmetricTransform（对称变换）

### 字段 (14)

- `uint[] expandedKey`（uint[] expanded键）(偏移: 0x34)
- `int Nk`（int Nk）(偏移: 0x38)
- `int Nr`（int Nr）(偏移: 0x3C)
- `uint[] Rcon`（uint[] Rcon）(偏移: 0x0)
- `byte[] SBox`（byte[] SBox）(偏移: 0x4)
- `byte[] iSBox`（byte[] iSBox）(偏移: 0x8)
- `uint[] T0`（uint[] T0）(偏移: 0xC)
- `uint[] T1`（uint[] T1）(偏移: 0x10)
- `uint[] T2`（uint[] T2）(偏移: 0x14)
- `uint[] T3`（uint[] T3）(偏移: 0x18)
- `uint[] iT0`（uint[] iT0）(偏移: 0x1C)
- `uint[] iT1`（uint[] iT1）(偏移: 0x20)
- `uint[] iT2`（uint[] iT2）(偏移: 0x24)
- `uint[] iT3`（uint[] iT3）(偏移: 0x28)

### 方法 (4)

- `void ECB(byte[] input, byte[] output)`
  （void ECB（字节[] input, 字节[] output））
- `uint SubByte(uint a)`
  （uint 子Byte（uint a））
- `void Encrypt128(byte[] indata, byte[] outdata, uint[] ekey)`
  （void Encrypt128（byte[] indata, byte[] outdata, uint[] ekey））
- `void Decrypt128(byte[] indata, byte[] outdata, uint[] ekey)`
  （void Decrypt128（byte[] indata, byte[] outdata, uint[] ekey））

---

## Agent（Agent）

**继承**: IAgent（IAgent）

### 字段 (29)

- `float radius`（浮点数 半径）(偏移: 0x8)
- `float height`（浮点数 高度）(偏移: 0xC)
- `float desiredSpeed`（float desiredSpeed）(偏移: 0x10)
- `float maxSpeed`（float maxSpeed）(偏移: 0x14)
- `float agentTimeHorizon`（float agent时间Horizon）(偏移: 0x18)
- `float obstacleTimeHorizon`（float obstacle时间Horizon）(偏移: 0x1C)
- `bool locked`（bool locked）(偏移: 0x20)
- `RVOLayer layer`（RVO层 layer）(偏移: 0x24)
- `RVOLayer collidesWith`（RVO层 collidesWith）(偏移: 0x28)
- `int maxNeighbours`（int maxNeighbours）(偏移: 0x2C)
- `Vector2 position`（二维向量 position）(偏移: 0x30)
- `float elevationCoordinate`（float elevationCoordinate）(偏移: 0x38)
- `Vector2 currentVelocity`（二维向量 current速度）(偏移: 0x3C)
- `Vector2 desiredTargetPointInVelocitySpace`（二维向量 desired目标PointIn速度Space）(偏移: 0x44)
- `Vector2 desiredVelocity`（二维向量 desired速度）(偏移: 0x4C)
- `Vector2 nextTargetPoint`（二维向量 next目标Point）(偏移: 0x54)
- `float nextDesiredSpeed`（float nextDesiredSpeed）(偏移: 0x5C)
- `float nextMaxSpeed`（float next最大Speed）(偏移: 0x60)
- `Vector2 collisionNormal`（二维向量 collision法线）(偏移: 0x64)
- `bool manuallyControlled`（bool manuallyControlled）(偏移: 0x6C)
- `bool debugDraw`（bool debugDraw）(偏移: 0x6D)
- `Agent next`（Agent next）(偏移: 0xB4)
- `float calculatedSpeed`（float calculatedSpeed）(偏移: 0xB8)
- `Vector2 calculatedTargetPoint`（二维向量 calculated目标Point）(偏移: 0xBC)
- `Simulator simulator`（Simulator simulator）(偏移: 0xC4)
- `List<Agent> neighbours`（List<Agent> neighbours）(偏移: 0xC8)
- `List<float> neighbourDists`（List<float> neighbourDists）(偏移: 0xCC)
- `List<ObstacleVertex> obstaclesBuffered`（List<ObstacleVertex> obstaclesBuffered）(偏移: 0xD0)
- `List<ObstacleVertex> obstacles`（List<ObstacleVertex> obstacles）(偏移: 0xD4)

### 方法 (54)

- `Vector2 get_Position()`
  （二维向量 get_Position（））
- `void set_Position(Vector2 value)`
  （void set_Position（二维向量 value））
- `float get_ElevationCoordinate()`
  （float get_ElevationCoordinate（））
- `void set_ElevationCoordinate(float value)`
  （void set_ElevationCoordinate（float value））
- `Vector2 get_CalculatedTargetPoint()`
  （二维向量 get_Calculated目标Point（））
- `void set_CalculatedTargetPoint(Vector2 value)`
  （void set_Calculated目标Point（二维向量 value））
- `float get_CalculatedSpeed()`
  （float get_CalculatedSpeed（））
- `void set_CalculatedSpeed(float value)`
  （void set_CalculatedSpeed（float value））
- `bool get_Locked()`
  （bool get_锁定的（））
- `void set_Locked(bool value)`
  （void set_锁定的（bool value））
- `float get_Radius()`
  （float get_Radius（））
- `void set_Radius(float value)`
  （void set_Radius（float value））
- `float get_Height()`
  （float get_高度（））
- `void set_Height(float value)`
  （void set_高度（float value））
- `float get_AgentTimeHorizon()`
  （float get_Agent时间Horizon（））
- `void set_AgentTimeHorizon(float value)`
  （void set_Agent时间Horizon（float value））
- `float get_ObstacleTimeHorizon()`
  （float get_Obstacle时间Horizon（））
- `void set_ObstacleTimeHorizon(float value)`
  （void set_Obstacle时间Horizon（float value））
- `int get_MaxNeighbours()`
  （int get_最大Neighbours（））
- `void set_MaxNeighbours(int value)`
  （void set_最大Neighbours（int value））
- `int get_NeighbourCount()`
  （int get_Neighbour数量（））
- `void set_NeighbourCount(int value)`
  （void set_Neighbour数量（int value））
- `RVOLayer get_Layer()`
  （RVO层 get_层（））
- `void set_Layer(RVOLayer value)`
  （void set_层（RVO层 value））
- `RVOLayer get_CollidesWith()`
  （RVO层 get_CollidesWith（））
- `void set_CollidesWith(RVOLayer value)`
  （void set_CollidesWith（RVO层 value））
- `bool get_DebugDraw()`
  （bool get_DebugDraw（））
- `void set_DebugDraw(bool value)`
  （void set_DebugDraw（bool value））
- `float get_Priority()`
  （float get_Priority（））
- `void set_Priority(float value)`
  （void set_Priority（float value））
- `Action get_PreCalculationCallback()`
  （动作 get_PreCalculation回调（））
- `void set_PreCalculationCallback(Action value)`
  （void set_PreCalculation回调（动作 value））
- `void SetTarget(Vector2 targetPoint, float desiredSpeed, float maxSpeed)`
  （void 集合目标（二维向量 targetPoint, float desiredSpeed, float maxSpeed））
- `void SetCollisionNormal(Vector2 normal)`
  （void 集合Collision法线（二维向量 normal））
- `void ForceSetVelocity(Vector2 velocity)`
  （void 强制集合速度（二维向量 velocity））
- `List<ObstacleVertex> get_NeighbourObstacles()`
  （List<ObstacleVertex> get_NeighbourObstacles（））
- `void BufferSwitch()`
  （void 缓冲区Switch（））
- `void PreCalculation()`
  （void PreCalculation（））
- `void PostCalculation()`
  （void PostCalculation（））
- `void CalculateNeighbours()`
  （void 计算Neighbours（））
- `float Sqr(float x)`
  （float Sqr（float x））
- `float InsertAgentNeighbour(Agent agent, float rangeSq)`
  （float InsertAgentNeighbour（Agent agent, float rangeSq））
- `Vector3 FromXZ(Vector2 p)`
  （三维向量 FromXZ（二维向量 p））
- `Vector2 ToXZ(Vector3 p)`
  （二维向量 ToXZ（三维向量 p））
- `Vector2 To2D(Vector3 p, out float elevation)`
  （二维向量 To2D（三维向量 p, out float elevation））
- `void DrawVO(Vector2 circleCenter, float radius, Vector2 origin)`
  （void DrawVO（二维向量 circleCenter, float radius, 二维向量 origin））
- `void CalculateVelocity(Simulator.WorkerContext context)`
  （void 计算速度（Simulator.WorkerContext context））
- `Color Rainbow(float v)`
  （颜色 Rainbow（float v））
- `void GenerateObstacleVOs(Agent.VOBuffer vos)`
  （void GenerateObstacleVOs（Agent.VO缓冲区 vos））
- `void GenerateNeighbourAgentVOs(Agent.VOBuffer vos)`
  （void GenerateNeighbourAgentVOs（Agent.VO缓冲区 vos））
- `Vector2 GradientDescent(Agent.VOBuffer vos, Vector2 sampleAround1, Vector2 sampleAround2)`
  （二维向量 GradientDescent（Agent.VO缓冲区 vos, 二维向量 sampleAround1, 二维向量 sampleAround2））
- `bool BiasDesiredVelocity(Agent.VOBuffer vos, ref Vector2 desiredVelocity, ref Vector2 targetPointInVelocitySpace, float maxBiasRadians)`
  （bool BiasDesired速度（Agent.VO缓冲区 vos, ref Vector2 desiredVelocity, ref Vector2 targetPointInVelocitySpace, float maxBiasRadians））
- `Vector2 EvaluateGradient(Agent.VOBuffer vos, Vector2 p, out float value)`
  （二维向量 EvaluateGradient（Agent.VO缓冲区 vos, 二维向量 p, out float value））
- `Vector2 Trace(Agent.VOBuffer vos, Vector2 p, out float score)`
  （二维向量 Trace（Agent.VO缓冲区 vos, 二维向量 p, out float score））

---

## Agent.VO（Agent.VO）

### 字段 (14)

- `Vector2 line1`（二维向量 line1）(偏移: 0x0)
- `Vector2 line2`（二维向量 line2）(偏移: 0x8)
- `Vector2 dir1`（二维向量 dir1）(偏移: 0x10)
- `Vector2 dir2`（二维向量 dir2）(偏移: 0x18)
- `Vector2 cutoffLine`（二维向量 cutoffLine）(偏移: 0x20)
- `Vector2 cutoffDir`（二维向量 cutoffDir）(偏移: 0x28)
- `Vector2 circleCenter`（二维向量 circle中心）(偏移: 0x30)
- `bool colliding`（bool colliding）(偏移: 0x38)
- `float radius`（浮点数 半径）(偏移: 0x3C)
- `float weightFactor`（float weight系数）(偏移: 0x40)
- `float weightBonus`（float weight奖励的）(偏移: 0x44)
- `Vector2 segmentStart`（二维向量 segment开始）(偏移: 0x48)
- `Vector2 segmentEnd`（二维向量 segment结束）(偏移: 0x50)
- `bool segment`（bool segment）(偏移: 0x58)

### 方法 (4)

- `Agent.VO SegmentObstacle(Vector2 segmentStart, Vector2 segmentEnd, Vector2 offset, float radius, float inverseDt, float inverseDeltaTime)`
  （Agent.VO SegmentObstacle（二维向量 segmentStart, 二维向量 segmentEnd, 二维向量 offset, float radius, float inverseDt, float inverseDeltaTime））
- `float SignedDistanceFromLine(Vector2 a, Vector2 dir, Vector2 p)`
  （float Signed距离FromLine（二维向量 a, 二维向量 dir, 二维向量 p））
- `Vector2 ScaledGradient(Vector2 p, out float weight)`
  （二维向量 ScaledGradient（二维向量 p, out float weight））
- `Vector2 Gradient(Vector2 p, out float weight)`
  （二维向量 Gradient（二维向量 p, out float weight））

---

## Agent.VOBuffer（Agent.VO缓冲区）

### 字段 (2)

- `Agent.VO[] buffer`（Agent.VO[] buffer）(偏移: 0x8)
- `int length`（整数 长度）(偏移: 0xC)

### 方法 (2)

- `void Clear()`
  （void 清除（））
- `void Add(Agent.VO vo)`
  （void 添加（Agent.VO vo））

---

## AggregateException（AggregateException）

**继承**: Exception（异常）

### 字段 (1)

- `ReadOnlyCollection<Exception> m_innerExceptions`（ReadOnlyCollection<Exception> m_innerExceptions）(偏移: 0x44)

### 方法 (5)

- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））
- `ReadOnlyCollection<Exception> get_InnerExceptions()`
  （ReadOnlyCollection<Exception> get_InnerExceptions（））
- `AggregateException Flatten()`
  （AggregateException Flatten（））
- `string ToString()`
  （字符串 转字符串（））
- `int get_InnerExceptionCount()`
  （int get_InnerException数量（））

---

## AimController（Aim控制器）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (27)

- `AimIK ik`（AimIK ik）(偏移: 0xC)
- `float weight`（浮点数 权重）(偏移: 0x10)
- `Transform target`（变换 目标）(偏移: 0x14)
- `float targetSwitchSmoothTime`（float targetSwitchSmooth时间）(偏移: 0x18)
- `float weightSmoothTime`（float weightSmooth时间）(偏移: 0x1C)
- `bool smoothTurnTowardsTarget`（bool smoothTurnTowards目标）(偏移: 0x20)
- `float maxRadiansDelta`（float maxRadiansDelta）(偏移: 0x24)
- `float maxMagnitudeDelta`（float maxMagnitudeDelta）(偏移: 0x28)
- `float slerpSpeed`（float slerpSpeed）(偏移: 0x2C)
- `Vector3 pivotOffsetFromRoot`（三维向量 pivotOffsetFrom根）(偏移: 0x30)
- `float minDistance`（float min距离）(偏移: 0x3C)
- `Vector3 offset`（三维向量 偏移）(偏移: 0x40)
- `float maxRootAngle`（float max根角度）(偏移: 0x4C)
- `bool turnToTarget`（bool turnTo目标）(偏移: 0x50)
- `float turnToTargetTime`（float turnTo目标时间）(偏移: 0x54)
- `bool useAnimatedAimDirection`（bool useAnimatedAim方向）(偏移: 0x58)
- `Vector3 animatedAimDirection`（三维向量 animatedAim方向）(偏移: 0x5C)
- `Transform lastTarget`（变换 last目标）(偏移: 0x68)
- `float switchWeight`（float switchWeight）(偏移: 0x6C)
- `float switchWeightV`（float switchWeightV）(偏移: 0x70)
- `float weightV`（float weightV）(偏移: 0x74)
- `Vector3 lastPosition`（三维向量 最后位置）(偏移: 0x78)
- `Vector3 dir`（三维向量 dir）(偏移: 0x84)
- `bool lastSmoothTowardsTarget`（bool lastSmoothTowards目标）(偏移: 0x90)
- `bool turningToTarget`（bool turningTo目标）(偏移: 0x91)
- `float turnToTargetMlp`（float turnTo目标Mlp）(偏移: 0x94)
- `float turnToTargetMlpV`（float turnTo目标MlpV）(偏移: 0x98)

### 方法 (6)

- `void Start()`
  （void 开始（））
- `void LateUpdate()`
  （void 延迟更新（））
- `Vector3 get_pivot()`
  （三维向量 get_pivot（））
- `void ApplyMinDistance()`
  （void 应用最小距离（））
- `void RootRotation()`
  （void 根Rotation（））
- `IEnumerator TurnToTarget()`
  （IEnumerator TurnTo目标（））

---

## AimIK（AimIK）

**继承**: IK（IK反向运动学）

### 字段 (1)

- `IKSolverAim solver`（IKSolverAim solver）(偏移: 0x1C)

### 方法 (6)

- `void OpenUserManual()`
  （void 打开用户手动（））
- `void OpenScriptReference()`
  （void 打开脚本引用（））
- `void OpenSetupTutorial()`
  （void 打开SetupTutorial（））
- `void SupportGroup()`
  （void 支持组（））
- `void ASThread()`
  （void 异步线程（））
- `IKSolver GetIKSolver()`
  （IK求解器 获取IK求解器（））

---

## AimPoser（AimPoser）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (2)

- `float angleBuffer`（float angle缓冲区）(偏移: 0xC)
- `AimPoser.Pose[] poses`（AimPoser.Pose[] poses）(偏移: 0x10)

### 方法 (2)

- `AimPoser.Pose GetPose(Vector3 localDirection)`
  （AimPoser.Pose 获取Pose（三维向量 localDirection））
- `void SetPoseActive(AimPoser.Pose pose)`
  （void 集合Pose激活的（AimPoser.Pose pose））

---

## AimPoser.Pose（AimPoser.Pose）

### 字段 (6)

- `bool visualize`（bool visualize）(偏移: 0x8)
- `string name`（字符串 名称）(偏移: 0xC)
- `Vector3 direction`（三维向量 方向）(偏移: 0x10)
- `float yaw`（float yaw）(偏移: 0x1C)
- `float pitch`（float pitch）(偏移: 0x20)
- `float angleBuffer`（float angle缓冲区）(偏移: 0x24)

### 方法 (2)

- `bool IsInDirection(Vector3 d)`
  （bool 是否In方向（三维向量 d））
- `void SetAngleBuffer(float value)`
  （void 集合角度缓冲区（float value））

---

## Allocator（Allocator）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AlternativePath（Alternative路径）

**继承**: MonoModifier（Mono修改器）

### 字段 (6)

- `int penalty`（int penalty）(偏移: 0x14)
- `int randomStep`（int randomStep）(偏移: 0x18)
- `List<GraphNode> prevNodes`（List<GraphNode> prevNodes）(偏移: 0x1C)
- `int prevPenalty`（int prev惩罚）(偏移: 0x20)
- `Random rnd`（随机 rnd）(偏移: 0x24)
- `bool destroyed`（bool destroyed）(偏移: 0x28)

### 方法 (6)

- `int get_Order()`
  （整数 获取_顺序（））
- `void Apply(Path p)`
  （void 应用（路径 p））
- `void OnDestroy()`
  （void 销毁时（））
- `void ClearOnDestroy()`
  （void 清除On销毁（））
- `void InversePrevious()`
  （void Inverse上一个（））
- `void ApplyNow(List<GraphNode> nodes)`
  （void 应用Now（List<GraphNode> nodes））

---

## AmbientValueAttribute（Ambient值Attribute）

**继承**: Attribute（属性）

### 字段 (1)

- `object value`（对象 value）(偏移: 0x8)

### 方法 (1)

- `object get_Value()`
  （对象 获取_值（））

---

## AmmoRecoverAndDecay（弹药恢复And衰减）

### 字段 (1)

- `AmmoRecoverAndDecay.Data[] datas`（弹药恢复AndDecay.Data[] datas）(偏移: 0x0)

### 方法 (2)

- `float GetRecover(int ammo)`
  （float 获取恢复（int ammo））
- `float GetDecay(int ammo)`
  （float 获取衰减（int ammo））

---

## AmmoRecoverAndDecay.Data（弹药恢复AndDecay.数据）

### 字段 (3)

- `int ammo`（整数 弹药）(偏移: 0x0)
- `float recover`（float recover）(偏移: 0x4)
- `float decay`（float decay）(偏移: 0x8)

---

## Amplifier（Amplifier）

**继承**: OffsetModifier（偏移修改器）

### 字段 (1)

- `Amplifier.Body[] bodies`（Amplifier.Body[] bodies）(偏移: 0x18)

### 方法 (1)

- `void OnModifyOffset()`
  （void 修改偏移时（））

---

## Amplifier.Body（Amplifier.身体）

### 字段 (9)

- `Transform transform`（变换 transform）(偏移: 0x8)
- `Transform relativeTo`（变换 relativeTo）(偏移: 0xC)
- `Amplifier.Body.EffectorLink[] effectorLinks`（Amplifier.Body.EffectorLink[] effectorLinks）(偏移: 0x10)
- `float verticalWeight`（float verticalWeight）(偏移: 0x14)
- `float horizontalWeight`（float horizontalWeight）(偏移: 0x18)
- `float speed`（浮点数 速度）(偏移: 0x1C)
- `Vector3 lastRelativePos`（三维向量 lastRelativePos）(偏移: 0x20)
- `Vector3 smoothDelta`（三维向量 smoothDelta）(偏移: 0x2C)
- `bool firstUpdate`（bool first更新）(偏移: 0x38)

### 方法 (2)

- `void Update(IKSolverFullBodyBiped solver, float w, float deltaTime)`
  （void 更新（IKSolver满身体Biped solver, float w, float deltaTime））
- `Vector3 Multiply(Vector3 v1, Vector3 v2)`
  （三维向量 Multiply（三维向量 v1, 三维向量 v2））

---

## Amplifier.Body.EffectorLink（Amplifier.Body.EffectorLink）

### 字段 (2)

- `FullBodyBipedEffector effector`（全身双足效应器 effector）(偏移: 0x8)
- `float weight`（浮点数 权重）(偏移: 0xC)

---

## AnalyticsSessionInfo（AnalyticsSession信息）

### 字段 (2)

- `AnalyticsSessionInfo.SessionStateChanged sessionStateChanged`（AnalyticsSessionInfo.Session状态Changed session状态Changed）(偏移: 0x0)
- `AnalyticsSessionInfo.IdentityTokenChanged identityTokenChanged`（AnalyticsSessionInfo.Identity令牌Changed identity令牌Changed）(偏移: 0x4)

### 方法 (2)

- `void CallSessionStateChanged(AnalyticsSessionState sessionState, long sessionId, long sessionElapsedTime, bool sessionChanged)`
  （void CallSession状态Changed（AnalyticsSession状态 sessionState, long sessionId, long sessionElapsedTime, bool sessionChanged））
- `void CallIdentityTokenChanged(string token)`
  （void CallIdentity令牌Changed（string token））

---

## AnalyticsSessionInfo.IdentityTokenChanged（AnalyticsSessionInfo.Identity令牌Changed）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(string token)`
  （void Invoke（string token））
- `IAsyncResult BeginInvoke(string token, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（string token, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## AnalyticsSessionInfo.SessionStateChanged（AnalyticsSessionInfo.Session状态Changed）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(AnalyticsSessionState sessionState, long sessionId, long sessionElapsedTime, bool sessionChanged)`
  （void Invoke（AnalyticsSession状态 sessionState, long sessionId, long sessionElapsedTime, bool sessionChanged））
- `IAsyncResult BeginInvoke(AnalyticsSessionState sessionState, long sessionId, long sessionElapsedTime, bool sessionChanged, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（AnalyticsSession状态 sessionState, long sessionId, long sessionElapsedTime, bool sessionChanged, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## AnalyticsSessionState（AnalyticsSession状态）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AndroidJNI（AndroidJNI）

### 方法 (61)

- `IntPtr FindClass(string name)`
  （整数Ptr 查找类（string name））
- `IntPtr FromReflectedMethod(IntPtr refMethod)`
  （整数Ptr FromReflectedMethod（整数Ptr refMethod））
- `IntPtr ExceptionOccurred()`
  （整数Ptr ExceptionOccurred（））
- `void ExceptionClear()`
  （void Exception清除（））
- `IntPtr NewGlobalRef(IntPtr obj)`
  （整数Ptr 新的全局的Ref（整数Ptr obj））
- `void DeleteGlobalRef(IntPtr obj)`
  （void Delete全局的Ref（整数Ptr obj））
- `IntPtr NewWeakGlobalRef(IntPtr obj)`
  （整数Ptr 新的Weak全局的Ref（整数Ptr obj））
- `void DeleteWeakGlobalRef(IntPtr obj)`
  （void DeleteWeak全局的Ref（整数Ptr obj））
- `IntPtr NewLocalRef(IntPtr obj)`
  （整数Ptr 新的本地的Ref（整数Ptr obj））
- `void DeleteLocalRef(IntPtr obj)`
  （void Delete本地的Ref（整数Ptr obj））
- `IntPtr NewObject(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （整数Ptr 新的对象（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `IntPtr GetObjectClass(IntPtr obj)`
  （整数Ptr 获取对象类（整数Ptr obj））
- `IntPtr GetMethodID(IntPtr clazz, string name, string sig)`
  （整数Ptr 获取MethodID（整数Ptr clazz, string name, string sig））
- `IntPtr GetStaticMethodID(IntPtr clazz, string name, string sig)`
  （整数Ptr 获取静态的MethodID（整数Ptr clazz, string name, string sig））
- `IntPtr NewString(string chars)`
  （整数Ptr 新的字符串（string chars））
- `IntPtr NewStringFromStr(string chars)`
  （整数Ptr 新的字符串FromStr（string chars））
- `string GetStringChars(IntPtr str)`
  （string 获取字符串Chars（整数Ptr str））
- `string CallStringMethod(IntPtr obj, IntPtr methodID, jvalue[] args)`
  （string Call字符串Method（整数Ptr obj, 整数Ptr methodID, jvalue[] args））
- `IntPtr CallObjectMethod(IntPtr obj, IntPtr methodID, jvalue[] args)`
  （整数Ptr Call对象Method（整数Ptr obj, 整数Ptr methodID, jvalue[] args））
- `int CallIntMethod(IntPtr obj, IntPtr methodID, jvalue[] args)`
  （int Call整数Method（整数Ptr obj, 整数Ptr methodID, jvalue[] args））
- `bool CallBooleanMethod(IntPtr obj, IntPtr methodID, jvalue[] args)`
  （bool CallBooleanMethod（整数Ptr obj, 整数Ptr methodID, jvalue[] args））
- `short CallShortMethod(IntPtr obj, IntPtr methodID, jvalue[] args)`
  （short CallShortMethod（整数Ptr obj, 整数Ptr methodID, jvalue[] args））
- `sbyte CallSByteMethod(IntPtr obj, IntPtr methodID, jvalue[] args)`
  （sbyte CallSByteMethod（整数Ptr obj, 整数Ptr methodID, jvalue[] args））
- `char CallCharMethod(IntPtr obj, IntPtr methodID, jvalue[] args)`
  （char CallCharMethod（整数Ptr obj, 整数Ptr methodID, jvalue[] args））
- `float CallFloatMethod(IntPtr obj, IntPtr methodID, jvalue[] args)`
  （float Call浮点数Method（整数Ptr obj, 整数Ptr methodID, jvalue[] args））
- `double CallDoubleMethod(IntPtr obj, IntPtr methodID, jvalue[] args)`
  （double CallDoubleMethod（整数Ptr obj, 整数Ptr methodID, jvalue[] args））
- `long CallLongMethod(IntPtr obj, IntPtr methodID, jvalue[] args)`
  （long CallLongMethod（整数Ptr obj, 整数Ptr methodID, jvalue[] args））
- `string CallStaticStringMethod(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （string Call静态的字符串Method（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `IntPtr CallStaticObjectMethod(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （整数Ptr Call静态的对象Method（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `int CallStaticIntMethod(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （int Call静态的整数Method（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `bool CallStaticBooleanMethod(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （bool Call静态的BooleanMethod（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `short CallStaticShortMethod(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （short Call静态的ShortMethod（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `sbyte CallStaticSByteMethod(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （sbyte Call静态的SByteMethod（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `char CallStaticCharMethod(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （char Call静态的CharMethod（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `float CallStaticFloatMethod(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （float Call静态的浮点数Method（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `double CallStaticDoubleMethod(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （double Call静态的DoubleMethod（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `long CallStaticLongMethod(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （long Call静态的LongMethod（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `void CallStaticVoidMethod(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （void Call静态的VoidMethod（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `IntPtr ToBooleanArray(bool[] array)`
  （整数Ptr ToBoolean数组（bool[] array））
- `IntPtr ToByteArray(byte[] array)`
  （整数Ptr ToByte数组（byte[] array））
- `IntPtr ToSByteArray(sbyte[] array)`
  （整数Ptr ToSByte数组（sbyte[] array））
- `IntPtr ToCharArray(char[] array)`
  （整数Ptr ToChar数组（char[] array））
- `IntPtr ToShortArray(short[] array)`
  （整数Ptr ToShort数组（short[] array））
- `IntPtr ToIntArray(int[] array)`
  （整数Ptr To整数数组（int[] array））
- `IntPtr ToLongArray(long[] array)`
  （整数Ptr ToLong数组（long[] array））
- `IntPtr ToFloatArray(float[] array)`
  （整数Ptr To浮点数数组（float[] array））
- `IntPtr ToDoubleArray(double[] array)`
  （整数Ptr ToDouble数组（double[] array））
- `IntPtr ToObjectArray(IntPtr[] array, IntPtr arrayClass)`
  （整数Ptr To对象数组（整数Ptr[] array, 整数Ptr arrayClass））
- `bool[] FromBooleanArray(IntPtr array)`
  （bool[] FromBoolean数组（整数Ptr array））
- `byte[] FromByteArray(IntPtr array)`
  （byte[] FromByte数组（整数Ptr array））
- `sbyte[] FromSByteArray(IntPtr array)`
  （sbyte[] FromSByte数组（整数Ptr array））
- `char[] FromCharArray(IntPtr array)`
  （char[] FromChar数组（整数Ptr array））
- `short[] FromShortArray(IntPtr array)`
  （short[] FromShort数组（整数Ptr array））
- `int[] FromIntArray(IntPtr array)`
  （int[] From整数数组（整数Ptr array））
- `long[] FromLongArray(IntPtr array)`
  （long[] FromLong数组（整数Ptr array））
- `float[] FromFloatArray(IntPtr array)`
  （float[] From浮点数数组（整数Ptr array））
- `double[] FromDoubleArray(IntPtr array)`
  （double[] FromDouble数组（整数Ptr array））
- `int GetArrayLength(IntPtr array)`
  （int 获取数组Length（整数Ptr array））
- `IntPtr NewObjectArray(int size, IntPtr clazz, IntPtr obj)`
  （整数Ptr 新的对象数组（int size, 整数Ptr clazz, 整数Ptr obj））
- `IntPtr GetObjectArrayElement(IntPtr array, int index)`
  （整数Ptr 获取对象数组元素（整数Ptr array, int index））
- `void SetObjectArrayElement(IntPtr array, int index, IntPtr obj)`
  （void 集合对象数组元素（整数Ptr array, int index, 整数Ptr obj））

---

## AndroidJNIHelper（AndroidJNI辅助器）

### 方法 (7)

- `IntPtr GetConstructorID(IntPtr javaClass, string signature)`
  （整数Ptr 获取ConstructorID（整数Ptr javaClass, string signature））
- `IntPtr GetMethodID(IntPtr javaClass, string methodName, string signature, bool isStatic)`
  （整数Ptr 获取MethodID（整数Ptr javaClass, string methodName, string signature, bool isStatic））
- `IntPtr CreateJavaRunnable(AndroidJavaRunnable jrunnable)`
  （整数Ptr 创建JavaRunnable（AndroidJavaRunnable jrunnable））
- `IntPtr CreateJavaProxy(AndroidJavaProxy proxy)`
  （整数Ptr 创建Java代理（AndroidJava代理 proxy））
- `jvalue[] CreateJNIArgArray(object[] args)`
  （jvalue[] 创建JNIArg数组（object[] args））
- `void DeleteJNIArgArray(object[] args, jvalue[] jniArgs)`
  （void DeleteJNIArg数组（object[] args, jvalue[] jniArgs））
- `IntPtr GetConstructorID(IntPtr jclass, object[] args)`
  （整数Ptr 获取ConstructorID（整数Ptr jclass, object[] args））

---

## AndroidJNISafe（AndroidJNISafe）

### 方法 (54)

- `void CheckException()`
  （void 检查Exception（））
- `void DeleteGlobalRef(IntPtr globalref)`
  （void Delete全局的Ref（整数Ptr globalref））
- `void DeleteWeakGlobalRef(IntPtr globalref)`
  （void DeleteWeak全局的Ref（整数Ptr globalref））
- `void DeleteLocalRef(IntPtr localref)`
  （void Delete本地的Ref（整数Ptr localref））
- `IntPtr NewString(string chars)`
  （整数Ptr 新的字符串（string chars））
- `string GetStringChars(IntPtr str)`
  （string 获取字符串Chars（整数Ptr str））
- `IntPtr GetObjectClass(IntPtr ptr)`
  （整数Ptr 获取对象类（整数Ptr ptr））
- `IntPtr GetStaticMethodID(IntPtr clazz, string name, string sig)`
  （整数Ptr 获取静态的MethodID（整数Ptr clazz, string name, string sig））
- `IntPtr GetMethodID(IntPtr obj, string name, string sig)`
  （整数Ptr 获取MethodID（整数Ptr obj, string name, string sig））
- `IntPtr FromReflectedMethod(IntPtr refMethod)`
  （整数Ptr FromReflectedMethod（整数Ptr refMethod））
- `IntPtr FindClass(string name)`
  （整数Ptr 查找类（string name））
- `IntPtr NewObject(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （整数Ptr 新的对象（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `void CallStaticVoidMethod(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （void Call静态的VoidMethod（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `IntPtr CallStaticObjectMethod(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （整数Ptr Call静态的对象Method（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `string CallStaticStringMethod(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （string Call静态的字符串Method（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `char CallStaticCharMethod(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （char Call静态的CharMethod（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `double CallStaticDoubleMethod(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （double Call静态的DoubleMethod（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `float CallStaticFloatMethod(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （float Call静态的浮点数Method（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `long CallStaticLongMethod(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （long Call静态的LongMethod（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `short CallStaticShortMethod(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （short Call静态的ShortMethod（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `sbyte CallStaticSByteMethod(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （sbyte Call静态的SByteMethod（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `bool CallStaticBooleanMethod(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （bool Call静态的BooleanMethod（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `int CallStaticIntMethod(IntPtr clazz, IntPtr methodID, jvalue[] args)`
  （int Call静态的整数Method（整数Ptr clazz, 整数Ptr methodID, jvalue[] args））
- `IntPtr CallObjectMethod(IntPtr obj, IntPtr methodID, jvalue[] args)`
  （整数Ptr Call对象Method（整数Ptr obj, 整数Ptr methodID, jvalue[] args））
- `string CallStringMethod(IntPtr obj, IntPtr methodID, jvalue[] args)`
  （string Call字符串Method（整数Ptr obj, 整数Ptr methodID, jvalue[] args））
- `char CallCharMethod(IntPtr obj, IntPtr methodID, jvalue[] args)`
  （char CallCharMethod（整数Ptr obj, 整数Ptr methodID, jvalue[] args））
- `double CallDoubleMethod(IntPtr obj, IntPtr methodID, jvalue[] args)`
  （double CallDoubleMethod（整数Ptr obj, 整数Ptr methodID, jvalue[] args））
- `float CallFloatMethod(IntPtr obj, IntPtr methodID, jvalue[] args)`
  （float Call浮点数Method（整数Ptr obj, 整数Ptr methodID, jvalue[] args））
- `long CallLongMethod(IntPtr obj, IntPtr methodID, jvalue[] args)`
  （long CallLongMethod（整数Ptr obj, 整数Ptr methodID, jvalue[] args））
- `short CallShortMethod(IntPtr obj, IntPtr methodID, jvalue[] args)`
  （short CallShortMethod（整数Ptr obj, 整数Ptr methodID, jvalue[] args））
- `sbyte CallSByteMethod(IntPtr obj, IntPtr methodID, jvalue[] args)`
  （sbyte CallSByteMethod（整数Ptr obj, 整数Ptr methodID, jvalue[] args））
- `bool CallBooleanMethod(IntPtr obj, IntPtr methodID, jvalue[] args)`
  （bool CallBooleanMethod（整数Ptr obj, 整数Ptr methodID, jvalue[] args））
- `int CallIntMethod(IntPtr obj, IntPtr methodID, jvalue[] args)`
  （int Call整数Method（整数Ptr obj, 整数Ptr methodID, jvalue[] args））
- `char[] FromCharArray(IntPtr array)`
  （char[] FromChar数组（整数Ptr array））
- `double[] FromDoubleArray(IntPtr array)`
  （double[] FromDouble数组（整数Ptr array））
- `float[] FromFloatArray(IntPtr array)`
  （float[] From浮点数数组（整数Ptr array））
- `long[] FromLongArray(IntPtr array)`
  （long[] FromLong数组（整数Ptr array））
- `short[] FromShortArray(IntPtr array)`
  （short[] FromShort数组（整数Ptr array））
- `byte[] FromByteArray(IntPtr array)`
  （byte[] FromByte数组（整数Ptr array））
- `sbyte[] FromSByteArray(IntPtr array)`
  （sbyte[] FromSByte数组（整数Ptr array））
- `bool[] FromBooleanArray(IntPtr array)`
  （bool[] FromBoolean数组（整数Ptr array））
- `int[] FromIntArray(IntPtr array)`
  （int[] From整数数组（整数Ptr array））
- `IntPtr ToObjectArray(IntPtr[] array, IntPtr type)`
  （整数Ptr To对象数组（整数Ptr[] array, 整数Ptr type））
- `IntPtr ToCharArray(char[] array)`
  （整数Ptr ToChar数组（char[] array））
- `IntPtr ToDoubleArray(double[] array)`
  （整数Ptr ToDouble数组（double[] array））
- `IntPtr ToFloatArray(float[] array)`
  （整数Ptr To浮点数数组（float[] array））
- `IntPtr ToLongArray(long[] array)`
  （整数Ptr ToLong数组（long[] array））
- `IntPtr ToShortArray(short[] array)`
  （整数Ptr ToShort数组（short[] array））
- `IntPtr ToByteArray(byte[] array)`
  （整数Ptr ToByte数组（byte[] array））
- `IntPtr ToSByteArray(sbyte[] array)`
  （整数Ptr ToSByte数组（sbyte[] array））
- `IntPtr ToBooleanArray(bool[] array)`
  （整数Ptr ToBoolean数组（bool[] array））
- `IntPtr ToIntArray(int[] array)`
  （整数Ptr To整数数组（int[] array））
- `IntPtr GetObjectArrayElement(IntPtr array, int index)`
  （整数Ptr 获取对象数组元素（整数Ptr array, int index））
- `int GetArrayLength(IntPtr array)`
  （int 获取数组Length（整数Ptr array））

---

## AndroidJavaClass（AndroidJava类）

**继承**: AndroidJavaObject（AndroidJava对象）

### 方法 (1)

- `void _AndroidJavaClass(string className)`
  （void _AndroidJava类（string className））

---

## AndroidJavaException（AndroidJavaException）

**继承**: Exception（异常）

### 字段 (1)

- `string mJavaStackTrace`（string mJava栈Trace）(偏移: 0x44)

### 方法 (1)

- `string get_StackTrace()`
  （string get_栈Trace（））

---

## AndroidJavaObject（AndroidJava对象）

**继承**: IDisposable（可释放接口）

### 字段 (3)

- `bool enableDebugPrints`（bool enableDebugPrints）(偏移: 0x0)
- `GlobalJavaObjectRef m_jobject`（全局的Java对象Ref m_jobject）(偏移: 0x8)
- `GlobalJavaObjectRef m_jclass`（全局的Java对象Ref m_jclass）(偏移: 0xC)

### 方法 (11)

- `void Dispose()`
  （void 释放（））
- `IntPtr GetRawObject()`
  （整数Ptr 获取Raw对象（））
- `IntPtr GetRawClass()`
  （整数Ptr 获取Raw类（））
- `void DebugPrint(string msg)`
  （void DebugPrint（string msg））
- `void _AndroidJavaObject(string className, object[] args)`
  （void _AndroidJava对象（string className, object[] args））
- `void Finalize()`
  （void 终结（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `AndroidJavaObject AndroidJavaObjectDeleteLocalRef(IntPtr jobject)`
  （AndroidJava对象 AndroidJava对象Delete本地的Ref（整数Ptr jobject））
- `AndroidJavaClass AndroidJavaClassDeleteLocalRef(IntPtr jclass)`
  （AndroidJava类 AndroidJava类Delete本地的Ref（整数Ptr jclass））
- `IntPtr _GetRawObject()`
  （整数Ptr _获取Raw对象（））
- `IntPtr _GetRawClass()`
  （整数Ptr _获取Raw类（））

---

## AndroidJavaProxy（AndroidJava代理）

### 字段 (4)

- `AndroidJavaClass javaInterface`（AndroidJava类 javaInterface）(偏移: 0x8)
- `IntPtr proxyObject`（整数Ptr proxy对象）(偏移: 0xC)
- `GlobalJavaObjectRef s_JavaLangSystemClass`（全局的Java对象Ref s_JavaLang系统类）(偏移: 0x0)
- `IntPtr s_HashCodeMethodID`（整数Ptr s_HashCodeMethodID）(偏移: 0x4)

### 方法 (5)

- `void Finalize()`
  （void 终结（））
- `AndroidJavaObject Invoke(string methodName, object[] args)`
  （AndroidJava对象 Invoke（string methodName, object[] args））
- `AndroidJavaObject Invoke(string methodName, AndroidJavaObject[] javaArgs)`
  （AndroidJava对象 Invoke（string methodName, AndroidJavaObject[] javaArgs））
- `AndroidJavaObject GetProxyObject()`
  （AndroidJava对象 获取代理对象（））
- `IntPtr GetRawProxy()`
  （整数Ptr 获取Raw代理（））

---

## AndroidJavaRunnable（AndroidJavaRunnable）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke()`
  （void 调用（））
- `IAsyncResult BeginInvoke(AsyncCallback callback, object object)`
  （I异步结果 开始调用（异步回调 callback, 对象 object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## AndroidJavaRunnableProxy（AndroidJavaRunnable代理）

**继承**: AndroidJavaProxy（AndroidJava代理）

### 字段 (1)

- `AndroidJavaRunnable mRunnable`（AndroidJavaRunnable mRunnable）(偏移: 0x10)

---

## AndroidReflection（AndroidReflection）

### 字段 (8)

- `GlobalJavaObjectRef s_ReflectionHelperClass`（全局的Java对象Ref s_Reflection辅助器类）(偏移: 0x0)
- `IntPtr s_ReflectionHelperGetConstructorID`（整数Ptr s_Reflection辅助器获取ConstructorID）(偏移: 0x4)
- `IntPtr s_ReflectionHelperGetMethodID`（整数Ptr s_Reflection辅助器获取MethodID）(偏移: 0x8)
- `IntPtr s_ReflectionHelperGetFieldID`（整数Ptr s_Reflection辅助器获取FieldID）(偏移: 0xC)
- `IntPtr s_ReflectionHelperGetFieldSignature`（整数Ptr s_Reflection辅助器获取FieldSignature）(偏移: 0x10)
- `IntPtr s_ReflectionHelperNewProxyInstance`（整数Ptr s_Reflection辅助器新的代理实例）(偏移: 0x14)
- `IntPtr s_ReflectionHelperSetNativeExceptionOnProxy`（整数Ptr s_Reflection辅助器集合NativeExceptionOn代理）(偏移: 0x18)
- `IntPtr s_FieldGetDeclaringClass`（整数Ptr s_Field获取Declaring类）(偏移: 0x1C)

### 方法 (8)

- `bool IsPrimitive(Type t)`
  （bool 是否Primitive（类型 t））
- `bool IsAssignableFrom(Type t, Type from)`
  （bool 是否AssignableFrom（类型 t, 类型 from））
- `IntPtr GetStaticMethodID(string clazz, string methodName, string signature)`
  （整数Ptr 获取静态的MethodID（string clazz, string methodName, string signature））
- `IntPtr GetMethodID(string clazz, string methodName, string signature)`
  （整数Ptr 获取MethodID（string clazz, string methodName, string signature））
- `IntPtr GetConstructorMember(IntPtr jclass, string signature)`
  （整数Ptr 获取ConstructorMember（整数Ptr jclass, string signature））
- `IntPtr GetMethodMember(IntPtr jclass, string methodName, string signature, bool isStatic)`
  （整数Ptr 获取MethodMember（整数Ptr jclass, string methodName, string signature, bool isStatic））
- `IntPtr NewProxyInstance(IntPtr delegateHandle, IntPtr interfaze)`
  （整数Ptr 新的代理实例（整数Ptr delegateHandle, 整数Ptr interfaze））
- `void SetNativeExceptionOnProxy(IntPtr proxy, Exception e, bool methodNotFound)`
  （void 集合NativeExceptionOn代理（整数Ptr proxy, Exception e, bool methodNotFound））

---

## AngularFalloffType（AngularFalloff类型）

### 字段 (1)

- `byte value__`（字节 值__）(偏移: 0x0)

---

## AnimSFX（动画SFX）

**继承**: RecyclableObject（可回收对象）

### 字段 (3)

- `RawImage img`（Raw图像 img）(偏移: 0x30)
- `float animTime`（float anim时间）(偏移: 0x34)
- `bool isTargetFull`（bool is目标满）(偏移: 0x38)

### 方法 (3)

- `void Recycle(bool roundRecycle)`
  （void 回收（布尔值 循环回收））
- `void Work()`
  （void 工作（））
- `void Animation()`
  （void 动画（））

---

## Animation（动画）

**继承**: Behaviour, IEnumerable（Behaviour, IEnumerable）

### 方法 (20)

- `void Stop()`
  （void 停止（））
- `void Rewind(string name)`
  （void Rewind（string name））
- `void RewindNamed(string name)`
  （void RewindNamed（string name））
- `void Sample()`
  （void Sample（））
- `AnimationState get_Item(string name)`
  （动画状态 get_项目（string name））
- `bool Play()`
  （bool 播放（））
- `bool Play(PlayMode mode)`
  （bool 播放（播放模式 mode））
- `bool PlayDefaultAnimation(PlayMode mode)`
  （bool 播放默认的动画（播放模式 mode））
- `bool Play(string animation)`
  （bool 播放（string animation））
- `bool Play(string animation, PlayMode mode)`
  （bool 播放（string animation, 播放模式 mode））
- `void CrossFade(string animation, float fadeLength)`
  （void CrossFade（string animation, float fadeLength））
- `void CrossFade(string animation, float fadeLength, PlayMode mode)`
  （void CrossFade（string animation, float fadeLength, 播放模式 mode））
- `void AddClip(AnimationClip clip, string newName)`
  （void 添加弹匣（动画弹匣 clip, string newName））
- `void AddClip(AnimationClip clip, string newName, int firstFrame, int lastFrame)`
  （void 添加弹匣（动画弹匣 clip, string newName, int firstFrame, int lastFrame））
- `void AddClip(AnimationClip clip, string newName, int firstFrame, int lastFrame, bool addLoopFrame)`
  （void 添加弹匣（动画弹匣 clip, string newName, int firstFrame, int lastFrame, bool addLoopFrame））
- `IEnumerator GetEnumerator()`
  （IEnumerator 获取枚举器（））
- `AnimationState GetState(string name)`
  （动画状态 获取状态（string name））
- `AnimationState GetStateAtIndex(int index)`
  （动画状态 获取状态At索引（int index））
- `int GetStateCount()`
  （int 获取状态数量（））
- `bool get_animatePhysics()`
  （bool get_animate物理（））

---

## Animation.Enumerator（Animation.Enumerator）

**继承**: IEnumerator（IEnumerator枚举器）

### 字段 (2)

- `Animation m_Outer`（动画 m_Outer）(偏移: 0x8)
- `int m_CurrentIndex`（int m_当前索引）(偏移: 0xC)

### 方法 (3)

- `object get_Current()`
  （对象 获取_当前（））
- `bool MoveNext()`
  （布尔值 移动下一个（））
- `void Reset()`
  （void 重置（））

---

## AnimationClip（动画弹匣）

**继承**: Motion（Motion）

### 方法 (13)

- `void Internal_CreateAnimationClip(AnimationClip self)`
  （void Internal_创建动画弹匣（动画弹匣 self））
- `float get_length()`
  （浮点数 获取_长度（））
- `float get_frameRate()`
  （float get_frameRate（））
- `void set_frameRate(float value)`
  （void set_frameRate（float value））
- `void SetCurve(string relativePath, Type type, string propertyName, AnimationCurve curve)`
  （void 集合Curve（string relativePath, 类型 type, string propertyName, 动画Curve curve））
- `void EnsureQuaternionContinuity()`
  （void EnsureQuaternionContinuity（））
- `bool get_legacy()`
  （bool get_legacy（））
- `void set_legacy(bool value)`
  （void set_legacy（bool value））
- `bool get_empty()`
  （bool get_empty（））
- `bool get_hasGenericRootTransform()`
  （bool get_hasGeneric根变换（））
- `bool get_hasMotionCurves()`
  （bool get_hasMotionCurves（））
- `bool get_hasRootCurves()`
  （bool get_has根Curves（））
- `bool get_hasRootMotion()`
  （bool get_has根Motion（））

---

## AnimationClipPlayable（动画弹匣Playable）

**继承**: IPlayable, IEquatable<AnimationClipPlayable>（IPlayable, IEquatable<动画弹匣Playable>）

### 字段 (1)

- `PlayableHandle m_Handle`（可播放句柄 m_句柄）(偏移: 0x0)

### 方法 (15)

- `AnimationClipPlayable Create(PlayableGraph graph, AnimationClip clip)`
  （动画弹匣Playable 创建（PlayableGraph graph, 动画弹匣 clip））
- `PlayableHandle CreateHandle(PlayableGraph graph, AnimationClip clip)`
  （Playable句柄 创建句柄（PlayableGraph graph, 动画弹匣 clip））
- `PlayableHandle GetHandle()`
  （可播放句柄 获取句柄（））
- `Playable op_Implicit(AnimationClipPlayable playable)`
  （Playable op_Implicit（动画弹匣Playable playable））
- `bool Equals(AnimationClipPlayable other)`
  （bool Equals（动画弹匣Playable other））
- `void SetApplyFootIK(bool value)`
  （void 集合应用脚部IK（bool value））
- `void SetRemoveStartOffset(bool value)`
  （void 集合移除开始Offset（bool value））
- `void SetOverrideLoopTime(bool value)`
  （void 集合重写Loop时间（bool value））
- `void SetLoopTime(bool value)`
  （void 集合Loop时间（bool value））
- `bool CreateHandleInternal(PlayableGraph graph, AnimationClip clip, ref PlayableHandle handle)`
  （bool 创建句柄内部的（PlayableGraph graph, 动画弹匣 clip, ref PlayableHandle handle））
- `void SetApplyFootIKInternal(ref PlayableHandle handle, bool value)`
  （void 集合应用脚部IK内部的（ref PlayableHandle handle, bool value））
- `void SetRemoveStartOffsetInternal(ref PlayableHandle handle, bool value)`
  （void 集合移除开始Offset内部的（ref PlayableHandle handle, bool value））
- `void SetOverrideLoopTimeInternal(ref PlayableHandle handle, bool value)`
  （void 集合重写Loop时间内部的（ref PlayableHandle handle, bool value））
- `void SetLoopTimeInternal(ref PlayableHandle handle, bool value)`
  （void 集合Loop时间内部的（ref PlayableHandle handle, bool value））
- `bool CreateHandleInternal_Injected(ref PlayableGraph graph, AnimationClip clip, ref PlayableHandle handle)`
  （bool 创建句柄Internal_Injected（ref PlayableGraph graph, 动画弹匣 clip, ref PlayableHandle handle））

---

## AnimationCurve（动画Curve）

**继承**: IEquatable<AnimationCurve>（IEquatable<动画Curve>）

### 字段 (1)

- `IntPtr m_Ptr`（整数指针 m_指针）(偏移: 0x8)

### 方法 (26)

- `void Internal_Destroy(IntPtr ptr)`
  （void 内部_销毁（整数指针 ptr））
- `IntPtr Internal_Create(Keyframe[] keys)`
  （整数Ptr Internal_创建（Keyframe[] keys））
- `bool Internal_Equals(IntPtr other)`
  （bool Internal_Equals（整数Ptr other））
- `void Finalize()`
  （void 终结（））
- `float Evaluate(float time)`
  （float Evaluate（float time））
- `Keyframe[] get_keys()`
  （Keyframe[] get_keys（））
- `void set_keys(Keyframe[] value)`
  （void set_keys（Keyframe[] value））
- `int AddKey(float time, float value)`
  （int 添加键（float time, float value））
- `int AddKey(Keyframe key)`
  （int 添加键（Keyframe key））
- `int AddKey_Internal(Keyframe key)`
  （int 添加Key_内部的（Keyframe key））
- `int MoveKey(int index, Keyframe key)`
  （int 移动键（int index, Keyframe key））
- `void RemoveKey(int index)`
  （void 移除键（int index））
- `Keyframe get_Item(int index)`
  （Keyframe get_项目（int index））
- `int get_length()`
  （int get_length（））
- `void SetKeys(Keyframe[] keys)`
  （void 集合Keys（Keyframe[] keys））
- `Keyframe GetKey(int index)`
  （Keyframe 获取键（int index））
- `Keyframe[] GetKeys()`
  （Keyframe[] 获取Keys（））
- `void SmoothTangents(int index, float weight)`
  （void SmoothTangents（int index, float weight））
- `AnimationCurve Linear(float timeStart, float valueStart, float timeEnd, float valueEnd)`
  （动画Curve Linear（float timeStart, float valueStart, float timeEnd, float valueEnd））
- `AnimationCurve EaseInOut(float timeStart, float valueStart, float timeEnd, float valueEnd)`
  （动画Curve EaseInOut（float timeStart, float valueStart, float timeEnd, float valueEnd））
- `bool Equals(object o)`
  （布尔值 等于（对象 o））
- `bool Equals(AnimationCurve other)`
  （bool Equals（动画Curve other））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `int AddKey_Internal_Injected(ref Keyframe key)`
  （int 添加Key_Internal_Injected（ref Keyframe key））
- `int MoveKey_Injected(int index, ref Keyframe key)`
  （int 移动Key_Injected（int index, ref Keyframe key））
- `void GetKey_Injected(int index, out Keyframe ret)`
  （void 获取Key_Injected（int index, out Keyframe ret））

---

## AnimationEvent（动画事件）

### 字段 (11)

- `float m_Time`（float m_时间）(偏移: 0x8)
- `string m_FunctionName`（string m_Function名称）(偏移: 0xC)
- `string m_StringParameter`（string m_字符串Parameter）(偏移: 0x10)
- `Object m_ObjectReferenceParameter`（对象 m_对象引用Parameter）(偏移: 0x14)
- `float m_FloatParameter`（float m_浮点数Parameter）(偏移: 0x18)
- `int m_IntParameter`（int m_整数Parameter）(偏移: 0x1C)
- `int m_MessageOptions`（int m_MessageOptions）(偏移: 0x20)
- `AnimationEventSource m_Source`（动画事件Source m_Source）(偏移: 0x24)
- `AnimationState m_StateSender`（动画状态 m_状态Sender）(偏移: 0x28)
- `AnimatorStateInfo m_AnimatorStateInfo`（动画器状态信息 m_动画器状态信息）(偏移: 0x2C)
- `AnimatorClipInfo m_AnimatorClipInfo`（动画器弹匣信息 m_动画器弹匣信息）(偏移: 0x50)

---

## AnimationEventReceiver（动画事件Receiver）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (4)

- `byte handTag`（byte hand标签）(偏移: 0xC)
- `SO_FxGroup[] effects`（SO_特效Group[] effects）(偏移: 0x10)
- `ParticleSystem[] ptcSystems`（粒子System[] ptcSystems）(偏移: 0x14)
- `Model mdl`（模型 mdl）(偏移: 0x18)

### 方法 (11)

- `bool get_isHand()`
  （bool get_is手部（））
- `void Awake()`
  （void 唤醒（））
- `void PlaySound(string input)`
  （void 播放音效（string input））
- `void AE_ReloadOver()`
  （void AE_换弹Over（））
- `void KnifeAttack(int index)`
  （void 近战武器Attack（int index））
- `void BulletRelease()`
  （void 子弹Release（））
- `void PlayEffect(int index)`
  （void 播放特效（int index））
- `void WeaponSpecialEvent(string msg)`
  （void Weapon特殊事件（string msg））
- `void EffectSwitchEvent(string eventName)`
  （void 特效Switch事件（string eventName））
- `void FootStep(int isRightFoot)`
  （void 脚部Step（int isRightFoot））
- `void JumpEvent(int isDrop)`
  （void 跳跃事件（int isDrop））

---

## AnimationEventSource（动画事件Source）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AnimationHud（动画Hud）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (3)

- `AnimationHud.Anim[] animations`（动画Hud.Anim[] animations）(偏移: 0xC)
- `Image image`（图像 image）(偏移: 0x10)
- `RawImage rawImage`（Raw图像 raw图像）(偏移: 0x14)

### 方法 (7)

- `SubscribeableProperty<bool> get_isPlaying()`
  （可订阅的Property<bool> get_isPlaying（））
- `void set_isPlaying(SubscribeableProperty<bool> value)`
  （void set_isPlaying（可订阅的Property<bool> value））
- `void Play(int index)`
  （void 播放（int index））
- `void OnDisable()`
  （void 禁用时（））
- `void Play(string animName)`
  （void 播放（string animName））
- `IEnumerator AnimationCoroutine(int animID)`
  （IEnumerator 动画协程（int animID））
- `void Stop()`
  （void 停止（））

---

## AnimationHud.Anim（动画Hud.动画）

### 字段 (5)

- `string name`（字符串 名称）(偏移: 0x0)
- `Sprite[] sprites`（Sprite[] sprites）(偏移: 0x4)
- `Texture[] textures`（Texture[] textures）(偏移: 0x8)
- `float[] interval`（float[] interval）(偏移: 0xC)
- `bool loop`（bool loop）(偏移: 0x10)

---

## AnimationHumanStream（动画人类流）

### 字段 (1)

- `IntPtr stream`（整数Ptr stream）(偏移: 0x0)

---

## AnimationLayerMixerPlayable（动画层MixerPlayable）

**继承**: IPlayable, IEquatable<AnimationLayerMixerPlayable>（IPlayable, IEquatable<动画层MixerPlayable>）

### 字段 (2)

- `PlayableHandle m_Handle`（可播放句柄 m_句柄）(偏移: 0x0)
- `AnimationLayerMixerPlayable m_NullPlayable`（动画层MixerPlayable m_NullPlayable）(偏移: 0x0)

### 方法 (9)

- `AnimationLayerMixerPlayable Create(PlayableGraph graph, int inputCount = 0)`
  （动画层MixerPlayable 创建（PlayableGraph graph, int inputCount = 0））
- `PlayableHandle CreateHandle(PlayableGraph graph, int inputCount = 0)`
  （Playable句柄 创建句柄（PlayableGraph graph, int inputCount = 0））
- `PlayableHandle GetHandle()`
  （可播放句柄 获取句柄（））
- `Playable op_Implicit(AnimationLayerMixerPlayable playable)`
  （Playable op_Implicit（动画层MixerPlayable playable））
- `bool Equals(AnimationLayerMixerPlayable other)`
  （bool Equals（动画层MixerPlayable other））
- `void SetLayerMaskFromAvatarMask(uint layerIndex, AvatarMask mask)`
  （void 集合层掩码FromAvatar掩码（uint layerIndex, Avatar掩码 mask））
- `bool CreateHandleInternal(PlayableGraph graph, ref PlayableHandle handle)`
  （bool 创建句柄内部的（PlayableGraph graph, ref PlayableHandle handle））
- `void SetLayerMaskFromAvatarMaskInternal(ref PlayableHandle handle, uint layerIndex, AvatarMask mask)`
  （void 集合层掩码FromAvatar掩码内部的（ref PlayableHandle handle, uint layerIndex, Avatar掩码 mask））
- `bool CreateHandleInternal_Injected(ref PlayableGraph graph, ref PlayableHandle handle)`
  （bool 创建句柄Internal_Injected（ref PlayableGraph graph, ref PlayableHandle handle））

---

## AnimationLink（动画Link）

**继承**: NodeLink2（节点Link2）

### 字段 (6)

- `string clip`（string clip）(偏移: 0x58)
- `float animSpeed`（float animSpeed）(偏移: 0x5C)
- `bool reverseAnim`（bool reverse动画）(偏移: 0x60)
- `GameObject referenceMesh`（游戏对象 reference网格）(偏移: 0x64)
- `AnimationLink.LinkClip[] sequence`（动画Link.LinkClip[] sequence）(偏移: 0x68)
- `string boneRoot`（string bone根）(偏移: 0x6C)

### 方法 (3)

- `Transform SearchRec(Transform tr, string name)`
  （变换 搜索Rec（变换 tr, string name））
- `void CalculateOffsets(List<Vector3> trace, out Vector3 endPosition)`
  （void 计算Offsets（List<Vector3> trace, out Vector3 endPosition））
- `void OnDrawGizmosSelected()`
  （void 绘制选中辅助线时（））

---

## AnimationLink.LinkClip（动画Link.Link弹匣）

### 字段 (3)

- `AnimationClip clip`（动画弹匣 clip）(偏移: 0x8)
- `Vector3 velocity`（三维向量 速度）(偏移: 0xC)
- `int loopCount`（int loop数量）(偏移: 0x18)

### 方法 (1)

- `string get_name()`
  （字符串 获取_名称（））

---

## AnimationLinkTraverser（动画LinkTraverser）

**继承**: VersionedMonoBehaviour（版本化MonoBehaviour）

### 字段 (2)

- `Animation anim`（动画 anim）(偏移: 0x10)
- `RichAI ai`（RichAI ai）(偏移: 0x14)

### 方法 (3)

- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `IEnumerator TraverseOffMeshLink(RichSpecial rs)`
  （IEnumerator TraverseOff网格Link（Rich特殊 rs））

---

## AnimationMixerPlayable（动画MixerPlayable）

**继承**: IPlayable, IEquatable<AnimationMixerPlayable>（IPlayable, IEquatable<动画MixerPlayable>）

### 字段 (2)

- `PlayableHandle m_Handle`（可播放句柄 m_句柄）(偏移: 0x0)
- `AnimationMixerPlayable m_NullPlayable`（动画MixerPlayable m_NullPlayable）(偏移: 0x0)

### 方法 (7)

- `AnimationMixerPlayable Create(PlayableGraph graph, int inputCount = 0, bool normalizeWeights = False)`
  （动画MixerPlayable 创建（PlayableGraph graph, int inputCount = 0, bool normalizeWeights = False））
- `PlayableHandle CreateHandle(PlayableGraph graph, int inputCount = 0, bool normalizeWeights = False)`
  （Playable句柄 创建句柄（PlayableGraph graph, int inputCount = 0, bool normalizeWeights = False））
- `PlayableHandle GetHandle()`
  （可播放句柄 获取句柄（））
- `Playable op_Implicit(AnimationMixerPlayable playable)`
  （Playable op_Implicit（动画MixerPlayable playable））
- `bool Equals(AnimationMixerPlayable other)`
  （bool Equals（动画MixerPlayable other））
- `bool CreateHandleInternal(PlayableGraph graph, bool normalizeWeights, ref PlayableHandle handle)`
  （bool 创建句柄内部的（PlayableGraph graph, bool normalizeWeights, ref PlayableHandle handle））
- `bool CreateHandleInternal_Injected(ref PlayableGraph graph, bool normalizeWeights, ref PlayableHandle handle)`
  （bool 创建句柄Internal_Injected（ref PlayableGraph graph, bool normalizeWeights, ref PlayableHandle handle））

---

## AnimationMotionXToDeltaPlayable（动画MotionXToDeltaPlayable）

**继承**: IPlayable, IEquatable<AnimationMotionXToDeltaPlayable>（IPlayable, IEquatable<动画MotionXToDeltaPlayable>）

### 字段 (2)

- `PlayableHandle m_Handle`（可播放句柄 m_句柄）(偏移: 0x0)
- `AnimationMotionXToDeltaPlayable m_NullPlayable`（动画MotionXToDeltaPlayable m_NullPlayable）(偏移: 0x0)

### 方法 (9)

- `AnimationMotionXToDeltaPlayable Create(PlayableGraph graph)`
  （动画MotionXToDeltaPlayable 创建（PlayableGraph graph））
- `PlayableHandle CreateHandle(PlayableGraph graph)`
  （Playable句柄 创建句柄（PlayableGraph graph））
- `PlayableHandle GetHandle()`
  （可播放句柄 获取句柄（））
- `Playable op_Implicit(AnimationMotionXToDeltaPlayable playable)`
  （Playable op_Implicit（动画MotionXToDeltaPlayable playable））
- `bool Equals(AnimationMotionXToDeltaPlayable other)`
  （bool Equals（动画MotionXToDeltaPlayable other））
- `void SetAbsoluteMotion(bool value)`
  （void 集合AbsoluteMotion（bool value））
- `bool CreateHandleInternal(PlayableGraph graph, ref PlayableHandle handle)`
  （bool 创建句柄内部的（PlayableGraph graph, ref PlayableHandle handle））
- `void SetAbsoluteMotionInternal(ref PlayableHandle handle, bool value)`
  （void 集合AbsoluteMotion内部的（ref PlayableHandle handle, bool value））
- `bool CreateHandleInternal_Injected(ref PlayableGraph graph, ref PlayableHandle handle)`
  （bool 创建句柄Internal_Injected（ref PlayableGraph graph, ref PlayableHandle handle））

---

## AnimationOffsetPlayable（动画OffsetPlayable）

**继承**: IPlayable, IEquatable<AnimationOffsetPlayable>（IPlayable, IEquatable<动画OffsetPlayable>）

### 字段 (2)

- `PlayableHandle m_Handle`（可播放句柄 m_句柄）(偏移: 0x0)
- `AnimationOffsetPlayable m_NullPlayable`（动画OffsetPlayable m_NullPlayable）(偏移: 0x0)

### 方法 (7)

- `AnimationOffsetPlayable Create(PlayableGraph graph, Vector3 position, Quaternion rotation, int inputCount)`
  （动画OffsetPlayable 创建（PlayableGraph graph, 三维向量 position, Quaternion rotation, int inputCount））
- `PlayableHandle CreateHandle(PlayableGraph graph, Vector3 position, Quaternion rotation, int inputCount)`
  （Playable句柄 创建句柄（PlayableGraph graph, 三维向量 position, Quaternion rotation, int inputCount））
- `PlayableHandle GetHandle()`
  （可播放句柄 获取句柄（））
- `Playable op_Implicit(AnimationOffsetPlayable playable)`
  （Playable op_Implicit（动画OffsetPlayable playable））
- `bool Equals(AnimationOffsetPlayable other)`
  （bool Equals（动画OffsetPlayable other））
- `bool CreateHandleInternal(PlayableGraph graph, Vector3 position, Quaternion rotation, ref PlayableHandle handle)`
  （bool 创建句柄内部的（PlayableGraph graph, 三维向量 position, Quaternion rotation, ref PlayableHandle handle））
- `bool CreateHandleInternal_Injected(ref PlayableGraph graph, ref Vector3 position, ref Quaternion rotation, ref PlayableHandle handle)`
  （bool 创建句柄Internal_Injected（ref PlayableGraph graph, ref Vector3 position, ref Quaternion rotation, ref PlayableHandle handle））

---

## AnimationOutputWeightProcessor（动画OutputWeightProcessor）

**继承**: ITimelineEvaluateCallback（ITimelineEvaluate回调）

### 字段 (2)

- `AnimationPlayableOutput m_Output`（动画PlayableOutput m_Output）(偏移: 0x8)
- `List<AnimationOutputWeightProcessor.WeightInfo> m_Mixers`（List<动画OutputWeightProcessor.WeightInfo> m_Mixers）(偏移: 0x10)

### 方法 (3)

- `void FindMixers()`
  （void 查找Mixers（））
- `void FindMixers(Playable parent, int port, Playable node)`
  （void 查找Mixers（Playable parent, int port, Playable node））
- `void Evaluate()`
  （void Evaluate（））

---

## AnimationOutputWeightProcessor.WeightInfo（动画OutputWeightProcessor.Weight信息）

### 字段 (3)

- `Playable mixer`（Playable mixer）(偏移: 0x0)
- `Playable parentMixer`（Playable parentMixer）(偏移: 0x8)
- `int port`（int port）(偏移: 0x10)

---

## AnimationPlayableAsset（动画Playable资产）

**继承**: PlayableAsset, ITimelineClipAsset, IPropertyPreview, ISerializationCallbackReceiver（Playable资产, ITimeline弹匣资产, I属性Preview, ISerialization回调Receiver）

### 字段 (11)

- `AnimationClip m_Clip`（动画弹匣 m_弹匣）(偏移: 0xC)
- `Vector3 m_Position`（三维向量 m_位置）(偏移: 0x10)
- `Vector3 m_EulerAngles`（三维向量 m_EulerAngles）(偏移: 0x1C)
- `bool m_UseTrackMatchFields`（bool m_UseTrack比赛Fields）(偏移: 0x28)
- `MatchTargetFields m_MatchTargetFields`（比赛目标Fields m_比赛目标Fields）(偏移: 0x2C)
- `bool m_RemoveStartOffset`（bool m_移除开始Offset）(偏移: 0x30)
- `bool m_ApplyFootIK`（bool m_应用脚部IK）(偏移: 0x31)
- `AnimationPlayableAsset.LoopMode m_Loop`（动画PlayableAsset.Loop模式 m_Loop）(偏移: 0x34)
- `int k_LatestVersion`（int k_LatestVersion）(偏移: 0x0)
- `int m_Version`（整数 m_版本）(偏移: 0x3C)
- `Quaternion m_Rotation`（四元数 m_旋转）(偏移: 0x40)

### 方法 (32)

- `Vector3 get_position()`
  （三维向量 获取_位置（））
- `void set_position(Vector3 value)`
  （void 设置_位置（三维向量 value））
- `Quaternion get_rotation()`
  （四元数 获取_旋转（））
- `void set_rotation(Quaternion value)`
  （void 设置_旋转（四元数 value））
- `Vector3 get_eulerAngles()`
  （三维向量 获取_欧拉角（））
- `void set_eulerAngles(Vector3 value)`
  （void set_eulerAngles（三维向量 value））
- `bool get_useTrackMatchFields()`
  （bool get_useTrack比赛Fields（））
- `void set_useTrackMatchFields(bool value)`
  （void set_useTrack比赛Fields（bool value））
- `MatchTargetFields get_matchTargetFields()`
  （比赛目标Fields get_match目标Fields（））
- `void set_matchTargetFields(MatchTargetFields value)`
  （void set_match目标Fields（比赛目标Fields value））
- `bool get_removeStartOffset()`
  （bool get_remove开始Offset（））
- `void set_removeStartOffset(bool value)`
  （void set_remove开始Offset（bool value））
- `bool get_applyFootIK()`
  （bool get_apply脚部IK（））
- `void set_applyFootIK(bool value)`
  （void set_apply脚部IK（bool value））
- `AnimationPlayableAsset.LoopMode get_loop()`
  （动画PlayableAsset.Loop模式 get_loop（））
- `void set_loop(AnimationPlayableAsset.LoopMode value)`
  （void set_loop（动画PlayableAsset.Loop模式 value））
- `bool get_hasRootTransforms()`
  （bool get_has根Transforms（））
- `AppliedOffsetMode get_appliedOffsetMode()`
  （AppliedOffset模式 get_appliedOffset模式（））
- `void set_appliedOffsetMode(AppliedOffsetMode value)`
  （void set_appliedOffset模式（AppliedOffset模式 value））
- `AnimationClip get_clip()`
  （动画弹匣 get_clip（））
- `void set_clip(AnimationClip value)`
  （void set_clip（动画弹匣 value））
- `double get_duration()`
  （双精度 获取_持续时间（））
- `IEnumerable<PlayableBinding> get_outputs()`
  （IEnumerable<可播放绑定> 获取_输出（））
- `Playable CreatePlayable(PlayableGraph graph, GameObject go)`
  （Playable 创建Playable（PlayableGraph graph, 游戏对象 go））
- `Playable CreatePlayable(PlayableGraph graph, AnimationClip clip, Vector3 positionOffset, Vector3 eulerOffset, bool removeStartOffset, AppliedOffsetMode mode, bool applyFootIK, AnimationPlayableAsset.LoopMode loop)`
  （Playable 创建Playable（PlayableGraph graph, 动画弹匣 clip, 三维向量 positionOffset, 三维向量 eulerOffset, bool removeStartOffset, AppliedOffset模式 mode, bool applyFootIK, 动画PlayableAsset.Loop模式 loop））
- `bool ShouldApplyOffset(AppliedOffsetMode mode, AnimationClip clip)`
  （bool 应该应用Offset（AppliedOffset模式 mode, 动画弹匣 clip））
- `bool ShouldApplyScaleRemove(AppliedOffsetMode mode)`
  （bool 应该应用缩放移除（AppliedOffset模式 mode））
- `ClipCaps get_clipCaps()`
  （弹匣Caps 获取_弹匣Caps（））
- `void ResetOffsets()`
  （void 重置偏移（））
- `void GatherProperties(PlayableDirector director, IPropertyCollector driver)`
  （void 收集属性（可播放导演 director, I属性收集器 driver））
- `bool HasRootTransforms(AnimationClip clip)`
  （bool 是否有根Transforms（动画弹匣 clip））
- `void OnUpgradeFromVersion(int oldVersion)`
  （void OnUpgradeFromVersion（int oldVersion））

---

## AnimationPlayableAsset.AnimationPlayableAssetUpgrade（动画PlayableAsset.动画Playable资产Upgrade）

### 方法 (1)

- `void ConvertRotationToEuler(AnimationPlayableAsset asset)`
  （void 转换RotationToEuler（动画Playable资产 asset））

---

## AnimationPlayableAsset.LoopMode（动画PlayableAsset.Loop模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AnimationPlayableBinding（动画PlayableBinding）

### 方法 (2)

- `PlayableBinding Create(string name, Object key)`
  （PlayableBinding 创建（string name, 对象 key））
- `PlayableOutput CreateAnimationOutput(PlayableGraph graph, string name)`
  （PlayableOutput 创建动画Output（PlayableGraph graph, string name））

---

## AnimationPlayableExtensions（动画PlayableExtensions）

### 方法 (1)

- `void SetAnimatedPropertiesInternal(ref PlayableHandle playable, AnimationClip animatedProperties)`
  （void 集合AnimatedProperties内部的（ref PlayableHandle playable, 动画弹匣 animatedProperties））

---

## AnimationPlayableGraphExtensions（动画PlayableGraphExtensions）

### 方法 (1)

- `bool InternalCreateAnimationOutput(ref PlayableGraph graph, string name, out PlayableOutputHandle handle)`
  （bool 内部的创建动画Output（ref PlayableGraph graph, string name, out PlayableOutputHandle handle））

---

## AnimationPlayableOutput（动画PlayableOutput）

**继承**: IPlayableOutput（I可播放输出）

### 字段 (1)

- `PlayableOutputHandle m_Handle`（可播放输出句柄 m_句柄）(偏移: 0x0)

### 方法 (7)

- `AnimationPlayableOutput Create(PlayableGraph graph, string name, Animator target)`
  （动画PlayableOutput 创建（PlayableGraph graph, string name, 动画器 target））
- `AnimationPlayableOutput get_Null()`
  （动画PlayableOutput get_Null（））
- `PlayableOutputHandle GetHandle()`
  （可播放输出句柄 获取句柄（））
- `PlayableOutput op_Implicit(AnimationPlayableOutput output)`
  （PlayableOutput op_Implicit（动画PlayableOutput output））
- `AnimationPlayableOutput op_Explicit(PlayableOutput output)`
  （动画PlayableOutput op_Explicit（PlayableOutput output））
- `void SetTarget(Animator value)`
  （void 集合目标（动画器 value））
- `void InternalSetTarget(ref PlayableOutputHandle handle, Animator target)`
  （void 内部的集合目标（ref PlayableOutputHandle handle, 动画器 target））

---

## AnimationPosePlayable（动画PosePlayable）

**继承**: IPlayable, IEquatable<AnimationPosePlayable>（IPlayable, IEquatable<动画PosePlayable>）

### 字段 (2)

- `PlayableHandle m_Handle`（可播放句柄 m_句柄）(偏移: 0x0)
- `AnimationPosePlayable m_NullPlayable`（动画PosePlayable m_NullPlayable）(偏移: 0x0)

### 方法 (2)

- `PlayableHandle GetHandle()`
  （可播放句柄 获取句柄（））
- `bool Equals(AnimationPosePlayable other)`
  （bool Equals（动画PosePlayable other））

---

## AnimationRemoveScalePlayable（动画移除缩放Playable）

**继承**: IPlayable, IEquatable<AnimationRemoveScalePlayable>（IPlayable, IEquatable<动画移除缩放Playable>）

### 字段 (2)

- `PlayableHandle m_Handle`（可播放句柄 m_句柄）(偏移: 0x0)
- `AnimationRemoveScalePlayable m_NullPlayable`（动画移除缩放Playable m_NullPlayable）(偏移: 0x0)

### 方法 (7)

- `AnimationRemoveScalePlayable Create(PlayableGraph graph, int inputCount)`
  （动画移除缩放Playable 创建（PlayableGraph graph, int inputCount））
- `PlayableHandle CreateHandle(PlayableGraph graph, int inputCount)`
  （Playable句柄 创建句柄（PlayableGraph graph, int inputCount））
- `PlayableHandle GetHandle()`
  （可播放句柄 获取句柄（））
- `Playable op_Implicit(AnimationRemoveScalePlayable playable)`
  （Playable op_Implicit（动画移除缩放Playable playable））
- `bool Equals(AnimationRemoveScalePlayable other)`
  （bool Equals（动画移除缩放Playable other））
- `bool CreateHandleInternal(PlayableGraph graph, ref PlayableHandle handle)`
  （bool 创建句柄内部的（PlayableGraph graph, ref PlayableHandle handle））
- `bool CreateHandleInternal_Injected(ref PlayableGraph graph, ref PlayableHandle handle)`
  （bool 创建句柄Internal_Injected（ref PlayableGraph graph, ref PlayableHandle handle））

---

## AnimationScriptPlayable（动画ScriptPlayable）

**继承**: IPlayable, IEquatable<AnimationScriptPlayable>（IPlayable, IEquatable<动画ScriptPlayable>）

### 字段 (2)

- `PlayableHandle m_Handle`（可播放句柄 m_句柄）(偏移: 0x0)
- `AnimationScriptPlayable m_NullPlayable`（动画ScriptPlayable m_NullPlayable）(偏移: 0x0)

### 方法 (2)

- `PlayableHandle GetHandle()`
  （可播放句柄 获取句柄（））
- `bool Equals(AnimationScriptPlayable other)`
  （bool Equals（动画ScriptPlayable other））

---

## AnimationState（动画状态）

**继承**: TrackedReference（Tracked引用）

### 方法 (6)

- `void set_enabled(bool value)`
  （void 设置_已启用（布尔值 value））
- `void set_weight(float value)`
  （void set_weight（float value））
- `void set_normalizedTime(float value)`
  （void set_normalized时间（float value））
- `void set_speed(float value)`
  （void set_speed（float value））
- `float get_length()`
  （浮点数 获取_长度（））
- `void set_layer(int value)`
  （void set_layer（int value））

---

## AnimationStream（动画流）

### 字段 (7)

- `uint m_AnimatorBindingsVersion`（uint m_动画器BindingsVersion）(偏移: 0x0)
- `IntPtr constant`（整数Ptr constant）(偏移: 0x4)
- `IntPtr input`（整数Ptr input）(偏移: 0x8)
- `IntPtr output`（整数Ptr output）(偏移: 0xC)
- `IntPtr workspace`（整数Ptr workspace）(偏移: 0x10)
- `IntPtr inputStreamAccessor`（整数Ptr input流Accessor）(偏移: 0x14)
- `IntPtr animationHandleBinder`（整数Ptr animation句柄Binder）(偏移: 0x18)

---

## AnimationTrack（动画Track）

**继承**: TrackAsset, ILayerable（Track资产, ILayerable）

### 字段 (19)

- `TimelineClip.ClipExtrapolation m_InfiniteClipPreExtrapolation`（TimelineClip.弹匣Extrapolation m_Infinite弹匣PreExtrapolation）(偏移: 0x58)
- `TimelineClip.ClipExtrapolation m_InfiniteClipPostExtrapolation`（TimelineClip.弹匣Extrapolation m_Infinite弹匣PostExtrapolation）(偏移: 0x5C)
- `Vector3 m_InfiniteClipOffsetPosition`（三维向量 m_Infinite弹匣OffsetPosition）(偏移: 0x60)
- `Vector3 m_InfiniteClipOffsetEulerAngles`（三维向量 m_Infinite弹匣OffsetEulerAngles）(偏移: 0x6C)
- `double m_InfiniteClipTimeOffset`（double m_Infinite弹匣时间Offset）(偏移: 0x78)
- `bool m_InfiniteClipRemoveOffset`（bool m_Infinite弹匣移除Offset）(偏移: 0x80)
- `bool m_InfiniteClipApplyFootIK`（bool m_Infinite弹匣应用脚部IK）(偏移: 0x81)
- `AnimationPlayableAsset.LoopMode mInfiniteClipLoop`（动画PlayableAsset.Loop模式 mInfinite弹匣Loop）(偏移: 0x84)
- `MatchTargetFields m_MatchTargetFields`（比赛目标Fields m_比赛目标Fields）(偏移: 0x88)
- `Vector3 m_Position`（三维向量 m_位置）(偏移: 0x8C)
- `Vector3 m_EulerAngles`（三维向量 m_EulerAngles）(偏移: 0x98)
- `AvatarMask m_AvatarMask`（Avatar掩码 m_Avatar掩码）(偏移: 0xA4)
- `bool m_ApplyAvatarMask`（bool m_应用Avatar掩码）(偏移: 0xA8)
- `TrackOffset m_TrackOffset`（TrackOffset m_TrackOffset）(偏移: 0xAC)
- `AnimationClip m_InfiniteClip`（动画弹匣 m_Infinite弹匣）(偏移: 0xB0)
- `Queue<Transform> s_CachedQueue`（Queue<Transform> s_Cached队列）(偏移: 0x0)
- `Quaternion m_OpenClipOffsetRotation`（Quaternion m_打开弹匣OffsetRotation）(偏移: 0xB4)
- `Quaternion m_Rotation`（四元数 m_旋转）(偏移: 0xC4)
- `bool m_ApplyOffsets`（bool m_应用Offsets）(偏移: 0xD4)

### 方法 (79)

- `Vector3 get_position()`
  （三维向量 获取_位置（））
- `void set_position(Vector3 value)`
  （void 设置_位置（三维向量 value））
- `Quaternion get_rotation()`
  （四元数 获取_旋转（））
- `void set_rotation(Quaternion value)`
  （void 设置_旋转（四元数 value））
- `Vector3 get_eulerAngles()`
  （三维向量 获取_欧拉角（））
- `void set_eulerAngles(Vector3 value)`
  （void set_eulerAngles（三维向量 value））
- `bool get_applyOffsets()`
  （bool get_applyOffsets（））
- `void set_applyOffsets(bool value)`
  （void set_applyOffsets（bool value））
- `TrackOffset get_trackOffset()`
  （TrackOffset get_trackOffset（））
- `void set_trackOffset(TrackOffset value)`
  （void set_trackOffset（TrackOffset value））
- `MatchTargetFields get_matchTargetFields()`
  （比赛目标Fields get_match目标Fields（））
- `void set_matchTargetFields(MatchTargetFields value)`
  （void set_match目标Fields（比赛目标Fields value））
- `AnimationClip get_infiniteClip()`
  （动画弹匣 get_infinite弹匣（））
- `void set_infiniteClip(AnimationClip value)`
  （void set_infinite弹匣（动画弹匣 value））
- `bool get_infiniteClipRemoveOffset()`
  （bool get_infinite弹匣移除Offset（））
- `void set_infiniteClipRemoveOffset(bool value)`
  （void set_infinite弹匣移除Offset（bool value））
- `AvatarMask get_avatarMask()`
  （Avatar掩码 get_avatar掩码（））
- `void set_avatarMask(AvatarMask value)`
  （void set_avatar掩码（Avatar掩码 value））
- `bool get_applyAvatarMask()`
  （bool get_applyAvatar掩码（））
- `void set_applyAvatarMask(bool value)`
  （void set_applyAvatar掩码（bool value））
- `bool CanCompileClips()`
  （bool 能否CompileClips（））
- `IEnumerable<PlayableBinding> get_outputs()`
  （IEnumerable<可播放绑定> 获取_输出（））
- `bool get_inClipMode()`
  （bool get_in弹匣模式（））
- `Vector3 get_infiniteClipOffsetPosition()`
  （三维向量 get_infinite弹匣OffsetPosition（））
- `void set_infiniteClipOffsetPosition(Vector3 value)`
  （void set_infinite弹匣OffsetPosition（三维向量 value））
- `Quaternion get_infiniteClipOffsetRotation()`
  （Quaternion get_infinite弹匣OffsetRotation（））
- `void set_infiniteClipOffsetRotation(Quaternion value)`
  （void set_infinite弹匣OffsetRotation（Quaternion value））
- `Vector3 get_infiniteClipOffsetEulerAngles()`
  （三维向量 get_infinite弹匣OffsetEulerAngles（））
- `void set_infiniteClipOffsetEulerAngles(Vector3 value)`
  （void set_infinite弹匣OffsetEulerAngles（三维向量 value））
- `bool get_infiniteClipApplyFootIK()`
  （bool get_infinite弹匣应用脚部IK（））
- `void set_infiniteClipApplyFootIK(bool value)`
  （void set_infinite弹匣应用脚部IK（bool value））
- `double get_infiniteClipTimeOffset()`
  （double get_infinite弹匣时间Offset（））
- `void set_infiniteClipTimeOffset(double value)`
  （void set_infinite弹匣时间Offset（double value））
- `TimelineClip.ClipExtrapolation get_infiniteClipPreExtrapolation()`
  （TimelineClip.弹匣Extrapolation get_infinite弹匣PreExtrapolation（））
- `void set_infiniteClipPreExtrapolation(TimelineClip.ClipExtrapolation value)`
  （void set_infinite弹匣PreExtrapolation（TimelineClip.弹匣Extrapolation value））
- `TimelineClip.ClipExtrapolation get_infiniteClipPostExtrapolation()`
  （TimelineClip.弹匣Extrapolation get_infinite弹匣PostExtrapolation（））
- `void set_infiniteClipPostExtrapolation(TimelineClip.ClipExtrapolation value)`
  （void set_infinite弹匣PostExtrapolation（TimelineClip.弹匣Extrapolation value））
- `AnimationPlayableAsset.LoopMode get_infiniteClipLoop()`
  （动画PlayableAsset.Loop模式 get_infinite弹匣Loop（））
- `void set_infiniteClipLoop(AnimationPlayableAsset.LoopMode value)`
  （void set_infinite弹匣Loop（动画PlayableAsset.Loop模式 value））
- `void ResetOffsets()`
  （void 重置偏移（））
- `TimelineClip CreateClip(AnimationClip clip)`
  （Timeline弹匣 创建弹匣（动画弹匣 clip））
- `void CreateInfiniteClip(string infiniteClipName)`
  （void 创建Infinite弹匣（string infiniteClipName））
- `TimelineClip CreateRecordableClip(string animClipName)`
  （Timeline弹匣 创建Recordable弹匣（string animClipName））
- `void OnCreateClip(TimelineClip clip)`
  （void On创建弹匣（Timeline弹匣 clip））
- `int CalculateItemsHash()`
  （int 计算ItemsHash（））
- `void UpdateClipOffsets()`
  （void 更新弹匣Offsets（））
- `Playable CompileTrackPlayable(PlayableGraph graph, AnimationTrack track, GameObject go, IntervalTree<RuntimeElement> tree, AppliedOffsetMode mode)`
  （Playable CompileTrackPlayable（PlayableGraph graph, 动画Track track, 游戏对象 go, 间隔Tree<RuntimeElement> tree, AppliedOffset模式 mode））
- `Playable OnCreateClipPlayableGraph(PlayableGraph graph, GameObject go, IntervalTree<RuntimeElement> tree)`
  （Playable On创建弹匣PlayableGraph（PlayableGraph graph, 游戏对象 go, 间隔Tree<RuntimeElement> tree））
- `int GetDefaultBlendCount()`
  （int 获取默认的Blend数量（））
- `void AttachDefaultBlend(PlayableGraph graph, AnimationLayerMixerPlayable mixer, bool requireOffset)`
  （void Attach默认的Blend（PlayableGraph graph, 动画层MixerPlayable mixer, bool requireOffset））
- `Playable AttachOffsetPlayable(PlayableGraph graph, Playable playable, Vector3 pos, Quaternion rot)`
  （Playable AttachOffsetPlayable（PlayableGraph graph, Playable playable, 三维向量 pos, Quaternion rot））
- `bool RequiresMotionXPlayable(AppliedOffsetMode mode, GameObject gameObject)`
  （bool RequiresMotionXPlayable（AppliedOffset模式 mode, 游戏对象 gameObject））
- `bool UsesAbsoluteMotion(AppliedOffsetMode mode)`
  （bool UsesAbsoluteMotion（AppliedOffset模式 mode））
- `bool HasController(GameObject gameObject)`
  （bool 是否有控制器（游戏对象 gameObject））
- `Animator GetBinding(PlayableDirector director)`
  （动画器 获取Binding（PlayableDirector director））
- `AnimationLayerMixerPlayable CreateGroupMixer(PlayableGraph graph, GameObject go, int inputCount)`
  （动画层MixerPlayable 创建组Mixer（PlayableGraph graph, 游戏对象 go, int inputCount））
- `Playable CreateInfiniteTrackPlayable(PlayableGraph graph, GameObject go, IntervalTree<RuntimeElement> tree, AppliedOffsetMode mode)`
  （Playable 创建InfiniteTrackPlayable（PlayableGraph graph, 游戏对象 go, 间隔Tree<RuntimeElement> tree, AppliedOffset模式 mode））
- `Playable ApplyTrackOffset(PlayableGraph graph, Playable root, GameObject go, AppliedOffsetMode mode)`
  （Playable 应用TrackOffset（PlayableGraph graph, Playable root, 游戏对象 go, AppliedOffset模式 mode））
- `void GetEvaluationTime(out double outStart, out double outDuration)`
  （void 获取Evaluation时间（out double outStart, out double outDuration））
- `void GetSequenceTime(out double outStart, out double outDuration)`
  （void 获取Sequence时间（out double outStart, out double outDuration））
- `void AssignAnimationClip(TimelineClip clip, AnimationClip animClip)`
  （void Assign动画弹匣（Timeline弹匣 clip, 动画弹匣 animClip））
- `void GatherProperties(PlayableDirector director, IPropertyCollector driver)`
  （void 收集属性（可播放导演 director, I属性收集器 driver））
- `void GetAnimationClips(List<AnimationClip> animClips)`
  （void 获取动画Clips（List<动画Clip> animClips））
- `AppliedOffsetMode GetOffsetMode(GameObject go, bool animatesRootTransform)`
  （AppliedOffset模式 获取Offset模式（游戏对象 go, bool animatesRootTransform））
- `bool IsRootTransformDisabledByMask(GameObject gameObject, Transform genericRootNode)`
  （bool 是否根变换禁用的By掩码（游戏对象 gameObject, 变换 genericRootNode））
- `Transform GetGenericRootNode(GameObject gameObject)`
  （变换 获取Generic根节点（游戏对象 gameObject））
- `bool AnimatesRootTransform()`
  （bool Animates根变换（））
- `Transform FindInHierarchyBreadthFirst(Transform t, string name)`
  （变换 查找InHierarchyBreadth第一个（变换 t, string name））
- `Vector3 get_openClipOffsetPosition()`
  （三维向量 get_open弹匣OffsetPosition（））
- `void set_openClipOffsetPosition(Vector3 value)`
  （void set_open弹匣OffsetPosition（三维向量 value））
- `Quaternion get_openClipOffsetRotation()`
  （Quaternion get_open弹匣OffsetRotation（））
- `void set_openClipOffsetRotation(Quaternion value)`
  （void set_open弹匣OffsetRotation（Quaternion value））
- `Vector3 get_openClipOffsetEulerAngles()`
  （三维向量 get_open弹匣OffsetEulerAngles（））
- `void set_openClipOffsetEulerAngles(Vector3 value)`
  （void set_open弹匣OffsetEulerAngles（三维向量 value））
- `TimelineClip.ClipExtrapolation get_openClipPreExtrapolation()`
  （TimelineClip.弹匣Extrapolation get_open弹匣PreExtrapolation（））
- `void set_openClipPreExtrapolation(TimelineClip.ClipExtrapolation value)`
  （void set_open弹匣PreExtrapolation（TimelineClip.弹匣Extrapolation value））
- `TimelineClip.ClipExtrapolation get_openClipPostExtrapolation()`
  （TimelineClip.弹匣Extrapolation get_open弹匣PostExtrapolation（））
- `void set_openClipPostExtrapolation(TimelineClip.ClipExtrapolation value)`
  （void set_open弹匣PostExtrapolation（TimelineClip.弹匣Extrapolation value））
- `void OnUpgradeFromVersion(int oldVersion)`
  （void OnUpgradeFromVersion（int oldVersion））

---

## AnimationTrack.AnimationTrackUpgrade（动画Track.动画TrackUpgrade）

### 方法 (3)

- `void ConvertRotationsToEuler(AnimationTrack track)`
  （void 转换RotationsToEuler（动画Track track））
- `void ConvertRootMotion(AnimationTrack track)`
  （void 转换根Motion（动画Track track））
- `void ConvertInfiniteTrack(AnimationTrack track)`
  （void 转换InfiniteTrack（动画Track track））

---

## AnimationTriggers（动画Triggers）

### 字段 (5)

- `string m_NormalTrigger`（string m_法线触发器）(偏移: 0x8)
- `string m_HighlightedTrigger`（string m_Highlighted触发器）(偏移: 0xC)
- `string m_PressedTrigger`（string m_按下的触发器）(偏移: 0x10)
- `string m_SelectedTrigger`（string m_选中的触发器）(偏移: 0x14)
- `string m_DisabledTrigger`（string m_禁用的触发器）(偏移: 0x18)

### 方法 (10)

- `string get_normalTrigger()`
  （string get_normal触发器（））
- `void set_normalTrigger(string value)`
  （void set_normal触发器（string value））
- `string get_highlightedTrigger()`
  （string get_highlighted触发器（））
- `void set_highlightedTrigger(string value)`
  （void set_highlighted触发器（string value））
- `string get_pressedTrigger()`
  （string get_pressed触发器（））
- `void set_pressedTrigger(string value)`
  （void set_pressed触发器（string value））
- `string get_selectedTrigger()`
  （string get_selected触发器（））
- `void set_selectedTrigger(string value)`
  （void set_selected触发器（string value））
- `string get_disabledTrigger()`
  （string get_disabled触发器（））
- `void set_disabledTrigger(string value)`
  （void set_disabled触发器（string value））

---

## Animator（动画器）

**继承**: Behaviour（行为）

### 方法 (52)

- `bool get_isHuman()`
  （bool get_is人类（））
- `bool get_hasRootMotion()`
  （bool get_has根Motion（））
- `float get_humanScale()`
  （float get_human缩放（））
- `void SetFloat(string name, float value)`
  （void 集合浮点数（string name, float value））
- `void SetBool(string name, bool value)`
  （void 集合布尔值（string name, bool value））
- `void SetInteger(string name, int value)`
  （void 集合Integer（string name, int value））
- `void SetTrigger(string name)`
  （void 集合触发器（string name））
- `void ResetTrigger(string name)`
  （void 重置触发器（string name））
- `Vector3 get_deltaPosition()`
  （三维向量 get_deltaPosition（））
- `Quaternion get_deltaRotation()`
  （Quaternion get_deltaRotation（））
- `void set_applyRootMotion(bool value)`
  （void set_apply根Motion（bool value））
- `AnimatorUpdateMode get_updateMode()`
  （动画器更新模式 get_update模式（））
- `void set_updateMode(AnimatorUpdateMode value)`
  （void set_update模式（动画器更新模式 value））
- `int get_layerCount()`
  （int get_layer数量（））
- `void GetAnimatorStateInfo(int layerIndex, StateInfoIndex stateInfoIndex, out AnimatorStateInfo info)`
  （void 获取动画器状态信息（int layerIndex, 状态信息索引 stateInfoIndex, out AnimatorStateInfo info））
- `AnimatorStateInfo GetCurrentAnimatorStateInfo(int layerIndex)`
  （动画器状态信息 获取当前动画器状态信息（int layerIndex））
- `AnimatorStateInfo GetNextAnimatorStateInfo(int layerIndex)`
  （动画器状态信息 获取下一个动画器状态信息（int layerIndex））
- `void GetCurrentAnimatorClipInfo(int layerIndex, List<AnimatorClipInfo> clips)`
  （void 获取当前动画器弹匣信息（int layerIndex, List<动画器弹匣Info> clips））
- `void GetAnimatorClipInfoInternal(int layerIndex, bool isCurrent, object clips)`
  （void 获取动画器弹匣信息内部的（int layerIndex, bool isCurrent, object clips））
- `void GetNextAnimatorClipInfo(int layerIndex, List<AnimatorClipInfo> clips)`
  （void 获取下一个动画器弹匣信息（int layerIndex, List<动画器弹匣Info> clips））
- `bool IsInTransition(int layerIndex)`
  （bool 是否InTransition（int layerIndex））
- `void set_speed(float value)`
  （void set_speed（float value））
- `void CrossFadeInFixedTime(string stateName, float fixedTransitionDuration)`
  （void CrossFadeIn固定时间（string stateName, float fixedTransitionDuration））
- `void CrossFadeInFixedTime(string stateName, float fixedTransitionDuration, int layer)`
  （void CrossFadeIn固定时间（string stateName, float fixedTransitionDuration, int layer））
- `void CrossFadeInFixedTime(string stateName, float fixedTransitionDuration, int layer, float fixedTimeOffset)`
  （void CrossFadeIn固定时间（string stateName, float fixedTransitionDuration, int layer, float fixedTimeOffset））
- `void CrossFadeInFixedTime(int stateHashName, float fixedTransitionDuration, int layer, float fixedTimeOffset, float normalizedTransitionTime)`
  （void CrossFadeIn固定时间（int stateHashName, float fixedTransitionDuration, int layer, float fixedTimeOffset, float normalizedTransitionTime））
- `void CrossFade(string stateName, float normalizedTransitionDuration, int layer, float normalizedTimeOffset)`
  （void CrossFade（string stateName, float normalizedTransitionDuration, int layer, float normalizedTimeOffset））
- `void CrossFade(string stateName, float normalizedTransitionDuration, int layer)`
  （void CrossFade（string stateName, float normalizedTransitionDuration, int layer））
- `void CrossFade(string stateName, float normalizedTransitionDuration, int layer, float normalizedTimeOffset, float normalizedTransitionTime)`
  （void CrossFade（string stateName, float normalizedTransitionDuration, int layer, float normalizedTimeOffset, float normalizedTransitionTime））
- `void CrossFade(int stateHashName, float normalizedTransitionDuration, int layer, float normalizedTimeOffset, float normalizedTransitionTime)`
  （void CrossFade（int stateHashName, float normalizedTransitionDuration, int layer, float normalizedTimeOffset, float normalizedTransitionTime））
- `void PlayInFixedTime(string stateName, int layer)`
  （void 播放In固定时间（string stateName, int layer））
- `void PlayInFixedTime(string stateName, int layer, float fixedTime)`
  （void 播放In固定时间（string stateName, int layer, float fixedTime））
- `void PlayInFixedTime(int stateNameHash, int layer, float fixedTime)`
  （void 播放In固定时间（int stateNameHash, int layer, float fixedTime））
- `void Play(string stateName, int layer)`
  （void 播放（string stateName, int layer））
- `void Play(string stateName, int layer, float normalizedTime)`
  （void 播放（string stateName, int layer, float normalizedTime））
- `void Play(int stateNameHash, int layer, float normalizedTime)`
  （void 播放（int stateNameHash, int layer, float normalizedTime））
- `Transform GetBoneTransform(HumanBodyBones humanBoneId)`
  （变换 获取Bone变换（人类身体Bones humanBoneId））
- `Transform GetBoneTransformInternal(int humanBoneId)`
  （变换 获取Bone变换内部的（int humanBoneId））
- `void set_cullingMode(AnimatorCullingMode value)`
  （void set_culling模式（动画器Culling模式 value））
- `RuntimeAnimatorController get_runtimeAnimatorController()`
  （Runtime动画器控制器 get_runtime动画器控制器（））
- `void set_runtimeAnimatorController(RuntimeAnimatorController value)`
  （void set_runtime动画器控制器（Runtime动画器控制器 value））
- `bool get_hasBoundPlayables()`
  （bool get_hasBoundPlayables（））
- `int StringToHash(string name)`
  （int 字符串ToHash（string name））
- `Avatar get_avatar()`
  （Avatar get_avatar（））
- `void SetFloatString(string name, float value)`
  （void 集合浮点数字符串（string name, float value））
- `void SetBoolString(string name, bool value)`
  （void 集合布尔值字符串（string name, bool value））
- `void SetIntegerString(string name, int value)`
  （void 集合Integer字符串（string name, int value））
- `void SetTriggerString(string name)`
  （void 集合触发器字符串（string name））
- `void ResetTriggerString(string name)`
  （void 重置触发器字符串（string name））
- `void Update(float deltaTime)`
  （void 更新（float deltaTime））
- `void get_deltaPosition_Injected(out Vector3 ret)`
  （void get_deltaPosition_Injected（out Vector3 ret））
- `void get_deltaRotation_Injected(out Quaternion ret)`
  （void get_deltaRotation_Injected（out Quaternion ret））

---

## AnimatorClipInfo（动画器弹匣信息）

### 字段 (2)

- `int m_ClipInstanceID`（int m_弹匣实例ID）(偏移: 0x0)
- `float m_Weight`（float m_Weight）(偏移: 0x4)

### 方法 (3)

- `AnimationClip get_clip()`
  （动画弹匣 get_clip（））
- `float get_weight()`
  （float get_weight（））
- `AnimationClip InstanceIDToAnimationClipPPtr(int instanceID)`
  （动画弹匣 实例IDTo动画弹匣PPtr（int instanceID））

---

## AnimatorControllerPlayable（动画器控制器Playable）

**继承**: IPlayable, IEquatable<AnimatorControllerPlayable>（IPlayable, IEquatable<动画器控制器Playable>）

### 字段 (2)

- `PlayableHandle m_Handle`（可播放句柄 m_句柄）(偏移: 0x0)
- `AnimatorControllerPlayable m_NullPlayable`（动画器控制器Playable m_NullPlayable）(偏移: 0x0)

### 方法 (3)

- `PlayableHandle GetHandle()`
  （可播放句柄 获取句柄（））
- `void SetHandle(PlayableHandle handle)`
  （void 集合句柄（Playable句柄 handle））
- `bool Equals(AnimatorControllerPlayable other)`
  （bool Equals（动画器控制器Playable other））

---

## AnimatorCullingMode（动画器Culling模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AnimatorOverrideController（动画器重写控制器）

**继承**: RuntimeAnimatorController（Runtime动画器控制器）

### 字段 (1)

- `AnimatorOverrideController.OnOverrideControllerDirtyCallback OnOverrideControllerDirty`（动画器重写Controller.On重写控制器Dirty回调 On重写控制器Dirty）(偏移: 0xC)

### 方法 (1)

- `void OnInvalidateOverrideController(AnimatorOverrideController controller)`
  （void OnInvalidate重写控制器（动画器重写控制器 controller））

---

## AnimatorOverrideController.OnOverrideControllerDirtyCallback（动画器重写Controller.On重写控制器Dirty回调）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke()`
  （void 调用（））
- `IAsyncResult BeginInvoke(AsyncCallback callback, object object)`
  （I异步结果 开始调用（异步回调 callback, 对象 object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## AnimatorStateInfo（动画器状态信息）

### 字段 (9)

- `int m_Name`（int m_名称）(偏移: 0x0)
- `int m_Path`（int m_路径）(偏移: 0x4)
- `int m_FullPath`（int m_满路径）(偏移: 0x8)
- `float m_NormalizedTime`（float m_Normalized时间）(偏移: 0xC)
- `float m_Length`（float m_Length）(偏移: 0x10)
- `float m_Speed`（float m_Speed）(偏移: 0x14)
- `float m_SpeedMultiplier`（float m_SpeedMultiplier）(偏移: 0x18)
- `int m_Tag`（int m_标签）(偏移: 0x1C)
- `int m_Loop`（int m_Loop）(偏移: 0x20)

### 方法 (4)

- `bool IsName(string name)`
  （bool 是否名称（string name））
- `int get_fullPathHash()`
  （int get_full路径Hash（））
- `int get_shortNameHash()`
  （int get_short名称Hash（））
- `float get_normalizedTime()`
  （float get_normalized时间（））

---

## AnimatorTransitionInfo（动画器Transition信息）

### 字段 (8)

- `int m_FullPath`（int m_满路径）(偏移: 0x0)
- `int m_UserName`（int m_User名称）(偏移: 0x4)
- `int m_Name`（int m_名称）(偏移: 0x8)
- `bool m_HasFixedDuration`（bool m_是否有固定持续时间）(偏移: 0xC)
- `float m_Duration`（float m_持续时间）(偏移: 0x10)
- `float m_NormalizedTime`（float m_Normalized时间）(偏移: 0x14)
- `bool m_AnyState`（bool m_任意状态）(偏移: 0x18)
- `int m_TransitionType`（int m_Transition类型）(偏移: 0x1C)

---

## AnimatorUpdateMode（动画器更新模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AntialiasingMode（Antialiasing模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AntialiasingQuality（AntialiasingQuality）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AppContextSwitches（AppContextSwitches）

### 字段 (2)

- `bool ThrowExceptionIfDisposedCancellationTokenSource`（bool 投掷ExceptionIfDisposedCancellation令牌Source）(偏移: 0x0)
- `bool PreserveEventListnerObjectIdentity`（bool Preserve事件Listner对象Identity）(偏移: 0x1)

---

## AppDomain（AppDomain）

**继承**: MarshalByRefObject（MarshalByRef对象）

### 字段 (20)

- `IntPtr _mono_app_domain`（整数Ptr _mono_app_domain）(偏移: 0xC)
- `string _process_guid`（string _process_guid）(偏移: 0x0)
- `object _evidence`（object _evidence）(偏移: 0x10)
- `object _granted`（object _granted）(偏移: 0x14)
- `int _principalPolicy`（int _principalPolicy）(偏移: 0x18)
- `object _principal`（object _principal）(偏移: 0x8000000C)
- `AppDomain default_domain`（AppDomain default_domain）(偏移: 0x4)
- `AssemblyLoadEventHandler AssemblyLoad`（Assembly加载事件处理器 Assembly加载）(偏移: 0x1C)
- `ResolveEventHandler AssemblyResolve`（Resolve事件处理器 AssemblyResolve）(偏移: 0x20)
- `EventHandler DomainUnload`（事件处理器 DomainUnload）(偏移: 0x24)
- `EventHandler ProcessExit`（事件处理器 处理Exit）(偏移: 0x28)
- `ResolveEventHandler ResourceResolve`（Resolve事件处理器 资源Resolve）(偏移: 0x2C)
- `ResolveEventHandler TypeResolve`（Resolve事件处理器 类型Resolve）(偏移: 0x30)
- `UnhandledExceptionEventHandler UnhandledException`（UnhandledException事件处理器 UnhandledException）(偏移: 0x34)
- `EventHandler<FirstChanceExceptionEventArgs> FirstChanceException`（事件Handler<第一个ChanceException事件Args> 第一个ChanceException）(偏移: 0x38)
- `object _domain_manager`（object _domain_manager）(偏移: 0x3C)
- `ResolveEventHandler ReflectionOnlyAssemblyResolve`（Resolve事件处理器 ReflectionOnlyAssemblyResolve）(偏移: 0x40)
- `object _activation`（object _activation）(偏移: 0x44)
- `object _applicationIdentity`（object _applicationIdentity）(偏移: 0x48)
- `List<string> compatibility_switch`（List<string> compatibility_switch）(偏移: 0x4C)

### 方法 (39)

- `string getFriendlyName()`
  （string getFriendly名称（））
- `AppDomain getCurDomain()`
  （AppDomain getCurDomain（））
- `AppDomain get_CurrentDomain()`
  （AppDomain get_当前Domain（））
- `Assembly[] GetAssemblies(bool refOnly)`
  （Assembly[] 获取Assemblies（bool refOnly））
- `Assembly[] GetAssemblies()`
  （Assembly[] 获取Assemblies（））
- `object GetData(string name)`
  （object 获取数据（string name））
- `object InitializeLifetimeService()`
  （object 初始化Lifetime服务（））
- `Assembly LoadAssembly(string assemblyRef, Evidence securityEvidence, bool refOnly)`
  （Assembly 加载Assembly（string assemblyRef, Evidence securityEvidence, bool refOnly））
- `Assembly LoadSatellite(AssemblyName assemblyRef, bool throwOnError)`
  （Assembly 加载Satellite（Assembly名称 assemblyRef, bool throwOnError））
- `Assembly Load(string assemblyString)`
  （Assembly 加载（string assemblyString））
- `Assembly Load(string assemblyString, Evidence assemblySecurity, bool refonly)`
  （Assembly 加载（string assemblyString, Evidence assemblySecurity, bool refonly））
- `AppDomain InternalSetDomainByID(int domain_id)`
  （AppDomain 内部的集合DomainByID（int domain_id））
- `AppDomain InternalSetDomain(AppDomain context)`
  （AppDomain 内部的集合Domain（AppDomain context））
- `void InternalPushDomainRefByID(int domain_id)`
  （void 内部的PushDomainRefByID（int domain_id））
- `void InternalPopDomainRef()`
  （void 内部的PopDomainRef（））
- `Context InternalSetContext(Context context)`
  （Context 内部的集合Context（Context context））
- `Context InternalGetContext()`
  （Context 内部的获取Context（））
- `Context InternalGetDefaultContext()`
  （Context 内部的获取默认的Context（））
- `string InternalGetProcessGuid(string newguid)`
  （string 内部的获取处理Guid（string newguid））
- `object InvokeInDomainByID(int domain_id, MethodInfo method, object obj, object[] args)`
  （object InvokeInDomainByID（int domain_id, Method信息 method, object obj, object[] args））
- `string GetProcessGuid()`
  （string 获取处理Guid（））
- `bool InternalIsFinalizingForUnload(int domain_id)`
  （bool 内部的是否FinalizingForUnload（int domain_id））
- `bool IsFinalizingForUnload()`
  （bool 是否FinalizingForUnload（））
- `int getDomainID()`
  （int getDomainID（））
- `int GetCurrentThreadId()`
  （int 获取当前ThreadId（））
- `string ToString()`
  （字符串 转字符串（））
- `void DoAssemblyLoad(Assembly assembly)`
  （void DoAssembly加载（Assembly assembly））
- `Assembly DoAssemblyResolve(string name, Assembly requestingAssembly, bool refonly)`
  （Assembly DoAssemblyResolve（string name, Assembly requestingAssembly, bool refonly））
- `Assembly DoTypeResolve(object name_or_tb)`
  （Assembly Do类型Resolve（object name_or_tb））
- `Assembly DoResourceResolve(string name, Assembly requesting)`
  （Assembly Do资源Resolve（string name, Assembly requesting））
- `void DoDomainUnload()`
  （void DoDomainUnload（））
- `byte[] GetMarshalledDomainObjRef()`
  （byte[] 获取MarshalledDomainObjRef（））
- `void ProcessMessageInDomain(byte[] arrRequest, CADMethodCallMessage cadMsg, out byte[] arrResponse, out CADMethodReturnMessage cadMrm)`
  （void 处理MessageInDomain（byte[] arrRequest, CADMethodCallMessage cadMsg, out byte[] arrResponse, out CADMethodReturnMessage cadMrm））
- `void add_DomainUnload(EventHandler value)`
  （void add_DomainUnload（事件处理器 value））
- `void remove_DomainUnload(EventHandler value)`
  （void remove_DomainUnload（事件处理器 value））
- `void add_ProcessExit(EventHandler value)`
  （void add_处理Exit（事件处理器 value））
- `void remove_ProcessExit(EventHandler value)`
  （void remove_处理Exit（事件处理器 value））
- `void add_UnhandledException(UnhandledExceptionEventHandler value)`
  （void add_UnhandledException（UnhandledException事件处理器 value））
- `void remove_UnhandledException(UnhandledExceptionEventHandler value)`
  （void remove_UnhandledException（UnhandledException事件处理器 value））

---

## AppDomainLevelActivator（AppDomain等级Activator）

**继承**: IActivator（IActivator）

### 字段 (2)

- `string _activationUrl`（string _activationUrl）(偏移: 0x8)
- `IActivator _next`（IActivator _next）(偏移: 0xC)

### 方法 (2)

- `IActivator get_NextActivator()`
  （IActivator get_下一个Activator（））
- `IConstructionReturnMessage Activate(IConstructionCallMessage ctorCall)`
  （IConstructionReturnMessage 激活（IConstructionCallMessage ctorCall））

---

## AppDomainSetup（AppDomainSetup）

### 字段 (22)

- `string application_base`（string application_base）(偏移: 0x8)
- `string application_name`（string application_name）(偏移: 0xC)
- `string cache_path`（string cache_path）(偏移: 0x10)
- `string configuration_file`（string configuration_file）(偏移: 0x14)
- `string dynamic_base`（string dynamic_base）(偏移: 0x18)
- `string license_file`（string license_file）(偏移: 0x1C)
- `string private_bin_path`（string private_bin_path）(偏移: 0x20)
- `string private_bin_path_probe`（string private_bin_path_probe）(偏移: 0x24)
- `string shadow_copy_directories`（string shadow_copy_directories）(偏移: 0x28)
- `string shadow_copy_files`（string shadow_copy_files）(偏移: 0x2C)
- `bool publisher_policy`（bool publisher_policy）(偏移: 0x30)
- `bool path_changed`（bool path_changed）(偏移: 0x31)
- `int loader_optimization`（int loader_optimization）(偏移: 0x34)
- `bool disallow_binding_redirects`（bool disallow_binding_redirects）(偏移: 0x38)
- `bool disallow_code_downloads`（bool disallow_code_downloads）(偏移: 0x39)
- `object _activationArguments`（object _activationArguments）(偏移: 0x3C)
- `object domain_initializer`（object domain_initializer）(偏移: 0x40)
- `object application_trust`（object application_trust）(偏移: 0x44)
- `string[] domain_initializer_args`（string[] domain_initializer_args）(偏移: 0x48)
- `bool disallow_appbase_probe`（bool disallow_appbase_probe）(偏移: 0x4C)
- `byte[] configuration_bytes`（byte[] configuration_bytes）(偏移: 0x50)
- `byte[] serialized_non_primitives`（byte[] serialized_non_primitives）(偏移: 0x54)

---

## Application（Application）

### 字段 (8)

- `Application.LowMemoryCallback lowMemory`（Application.LowMemory回调 lowMemory）(偏移: 0x0)
- `Application.LogCallback s_LogCallbackHandler`（Application.Log回调 s_Log回调处理器）(偏移: 0x4)
- `Application.LogCallback s_LogCallbackHandlerThreaded`（Application.Log回调 s_Log回调处理器Threaded）(偏移: 0x8)
- `Action<bool> focusChanged`（Action<bool> focusChanged）(偏移: 0xC)
- `Action<string> deepLinkActivated`（Action<string> deepLinkActivated）(偏移: 0x10)
- `Func<bool> wantsToQuit`（Func<bool> wantsToQuit）(偏移: 0x14)
- `Action quitting`（动作 quitting）(偏移: 0x18)
- `Action unloading`（动作 unloading）(偏移: 0x1C)

### 方法 (19)

- `void Quit(int exitCode)`
  （void Quit（int exitCode））
- `void Quit()`
  （void Quit（））
- `bool get_isPlaying()`
  （bool get_isPlaying（））
- `bool HasProLicense()`
  （bool 是否有ProLicense（））
- `bool get_isBatchMode()`
  （bool get_isBatch模式（））
- `string get_dataPath()`
  （string get_data路径（））
- `string get_persistentDataPath()`
  （string get_persistent数据路径（））
- `void OpenURL(string url)`
  （void 打开URL（string url））
- `RuntimePlatform get_platform()`
  （RuntimePlatform get_platform（））
- `bool get_isMobilePlatform()`
  （bool get_isMobilePlatform（））
- `void CallLowMemory()`
  （void CallLowMemory（））
- `void CallLogCallback(string logString, string stackTrace, LogType type, bool invokedOnMainThread)`
  （void CallLog回调（string logString, string stackTrace, Log类型 type, bool invokedOnMainThread））
- `bool Internal_ApplicationWantsToQuit()`
  （bool Internal_ApplicationWantsToQuit（））
- `void Internal_ApplicationQuit()`
  （void Internal_ApplicationQuit（））
- `void Internal_ApplicationUnload()`
  （void Internal_ApplicationUnload（））
- `void InvokeOnBeforeRender()`
  （void InvokeOnBeforeRender（））
- `void InvokeFocusChanged(bool focus)`
  （void Invoke聚焦Changed（bool focus））
- `void InvokeDeepLinkActivated(string url)`
  （void InvokeDeepLinkActivated（string url））
- `bool get_isEditor()`
  （bool get_isEditor（））

---

## Application.LogCallback（Application.Log回调）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(string condition, string stackTrace, LogType type)`
  （void Invoke（string condition, string stackTrace, Log类型 type））
- `IAsyncResult BeginInvoke(string condition, string stackTrace, LogType type, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（string condition, string stackTrace, Log类型 type, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## Application.LowMemoryCallback（Application.LowMemory回调）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke()`
  （void 调用（））
- `IAsyncResult BeginInvoke(AsyncCallback callback, object object)`
  （I异步结果 开始调用（异步回调 callback, 对象 object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## AppliedOffsetMode（AppliedOffset模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ArgInfo（Arg信息）

### 字段 (3)

- `int[] _paramMap`（int[] _param映射）(偏移: 0x8)
- `int _inoutArgCount`（int _inoutArg数量）(偏移: 0xC)
- `MethodBase _method`（Method基础 _method）(偏移: 0x10)

### 方法 (1)

- `object[] GetInOutArgs(object[] args)`
  （object[] 获取InOutArgs（object[] args））

---

## ArgInfoType（Arg信息类型）

### 字段 (1)

- `byte value__`（字节 值__）(偏移: 0x0)

---

## ArgIterator（ArgIterator）

### 字段 (4)

- `IntPtr sig`（整数Ptr sig）(偏移: 0x0)
- `IntPtr args`（整数Ptr args）(偏移: 0x4)
- `int next_arg`（int next_arg）(偏移: 0x8)
- `int num_args`（int num_args）(偏移: 0xC)

### 方法 (2)

- `bool Equals(object o)`
  （布尔值 等于（对象 o））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## ArgumentCache（Argument缓存）

**继承**: ISerializationCallbackReceiver（ISerialization回调接收器）

### 字段 (6)

- `Object m_ObjectArgument`（对象 m_对象Argument）(偏移: 0x8)
- `string m_ObjectArgumentAssemblyTypeName`（string m_对象ArgumentAssembly类型名称）(偏移: 0xC)
- `int m_IntArgument`（int m_整数Argument）(偏移: 0x10)
- `float m_FloatArgument`（float m_浮点数Argument）(偏移: 0x14)
- `string m_StringArgument`（string m_字符串Argument）(偏移: 0x18)
- `bool m_BoolArgument`（bool m_布尔值Argument）(偏移: 0x1C)

### 方法 (8)

- `Object get_unityObjectArgument()`
  （对象 get_unity对象Argument（））
- `string get_unityObjectArgumentAssemblyTypeName()`
  （string get_unity对象ArgumentAssembly类型名称（））
- `int get_intArgument()`
  （int get_intArgument（））
- `float get_floatArgument()`
  （float get_floatArgument（））
- `string get_stringArgument()`
  （string get_stringArgument（））
- `bool get_boolArgument()`
  （bool get_boolArgument（））
- `void OnBeforeSerialize()`
  （void 序列化前（））
- `void OnAfterDeserialize()`
  （void 反序列化后（））

---

## ArgumentException（ArgumentException）

**继承**: SystemException, ISerializable（系统Exception, ISerializable）

### 字段 (1)

- `string m_paramName`（string m_param名称）(偏移: 0x44)

### 方法 (2)

- `string get_Message()`
  （字符串 获取_消息（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））

---

## ArgumentOutOfRangeException（ArgumentOutOf范围Exception）

**继承**: ArgumentException, ISerializable（ArgumentException, ISerializable）

### 字段 (2)

- `string _rangeMessage`（string _rangeMessage）(偏移: 0x0)
- `object m_actualValue`（object m_actual值）(偏移: 0x48)

### 方法 (3)

- `string get_RangeMessage()`
  （string get_范围Message（））
- `string get_Message()`
  （字符串 获取_消息（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））

---

## ArmIK（手臂IK）

**继承**: IK（IK反向运动学）

### 字段 (1)

- `IKSolverArm solver`（IKSolver手臂 solver）(偏移: 0x1C)

### 方法 (5)

- `void OpenUserManual()`
  （void 打开用户手动（））
- `void OpenScriptReference()`
  （void 打开脚本引用（））
- `void SupportGroup()`
  （void 支持组（））
- `void ASThread()`
  （void 异步线程（））
- `IKSolver GetIKSolver()`
  （IK求解器 获取IK求解器（））

---

## ArmorRatio（护甲比率）

### 字段 (3)

- `float helmetRatio`（float helmet比率）(偏移: 0x0)
- `float armorRatio`（float armor比率）(偏移: 0x4)
- `float nanoClothRatio`（float nano服装比率）(偏移: 0x8)

---

## Array（数组）

**继承**: ICollection, IEnumerable, IList, IStructuralComparable, IStructuralEquatable, ICloneable（ICollection, IEnumerable, I列表, IStructuralComparable, IStructuralEquatable, ICloneable）

### 方法 (83)

- `Array CreateInstance(Type elementType, long[] lengths)`
  （数组 创建实例（类型 elementType, long[] lengths））
- `void CopyTo(Array array, int index)`
  （void 复制到（数组 array, 整数 index））
- `object Clone()`
  （对象 克隆（））
- `int CombineHashCodes(int h1, int h2)`
  （int CombineHashCodes（int h1, int h2））
- `int BinarySearch(Array array, object value)`
  （int Binary搜索（数组 array, object value））
- `void Copy(Array sourceArray, Array destinationArray, long length)`
  （void 复制（数组 sourceArray, 数组 destinationArray, long length））
- `void Copy(Array sourceArray, long sourceIndex, Array destinationArray, long destinationIndex, long length)`
  （void 复制（数组 sourceArray, long sourceIndex, 数组 destinationArray, long destinationIndex, long length））
- `void CopyTo(Array array, long index)`
  （void 复制To（数组 array, long index））
- `long get_LongLength()`
  （long get_LongLength（））
- `long GetLongLength(int dimension)`
  （long 获取LongLength（int dimension））
- `object GetValue(long index)`
  （object 获取值（long index））
- `object GetValue(long index1, long index2)`
  （object 获取值（long index1, long index2））
- `object GetValue(long index1, long index2, long index3)`
  （object 获取值（long index1, long index2, long index3））
- `object GetValue(long[] indices)`
  （object 获取值（long[] indices））
- `bool get_IsFixedSize()`
  （bool get_是否固定大小（））
- `bool get_IsReadOnly()`
  （布尔值 获取_是否只读（））
- `bool get_IsSynchronized()`
  （bool get_是否Synchronized（））
- `object get_SyncRoot()`
  （对象 获取_同步根（））
- `int BinarySearch(Array array, int index, int length, object value)`
  （int Binary搜索（数组 array, int index, int length, object value））
- `int BinarySearch(Array array, object value, IComparer comparer)`
  （int Binary搜索（数组 array, object value, IComparer comparer））
- `int BinarySearch(Array array, int index, int length, object value, IComparer comparer)`
  （int Binary搜索（数组 array, int index, int length, object value, IComparer comparer））
- `int GetMedian(int low, int hi)`
  （int 获取Median（int low, int hi））
- `int IndexOf(Array array, object value)`
  （int 索引Of（数组 array, object value））
- `int IndexOf(Array array, object value, int startIndex)`
  （int 索引Of（数组 array, object value, int startIndex））
- `int IndexOf(Array array, object value, int startIndex, int count)`
  （int 索引Of（数组 array, object value, int startIndex, int count））
- `int LastIndexOf(Array array, object value)`
  （int 最后一个索引Of（数组 array, object value））
- `int LastIndexOf(Array array, object value, int startIndex)`
  （int 最后一个索引Of（数组 array, object value, int startIndex））
- `int LastIndexOf(Array array, object value, int startIndex, int count)`
  （int 最后一个索引Of（数组 array, object value, int startIndex, int count））
- `void Reverse(Array array)`
  （void Reverse（数组 array））
- `void Reverse(Array array, int index, int length)`
  （void Reverse（数组 array, int index, int length））
- `void SetValue(object value, long index)`
  （void 集合值（object value, long index））
- `void SetValue(object value, long index1, long index2)`
  （void 集合值（object value, long index1, long index2））
- `void SetValue(object value, long index1, long index2, long index3)`
  （void 集合值（object value, long index1, long index2, long index3））
- `void SetValue(object value, long[] indices)`
  （void 集合值（object value, long[] indices））
- `void Sort(Array array)`
  （void Sort（数组 array））
- `void Sort(Array array, int index, int length)`
  （void Sort（数组 array, int index, int length））
- `void Sort(Array array, IComparer comparer)`
  （void Sort（数组 array, IComparer comparer））
- `void Sort(Array array, int index, int length, IComparer comparer)`
  （void Sort（数组 array, int index, int length, IComparer comparer））
- `void Sort(Array keys, Array items)`
  （void Sort（数组 keys, 数组 items））
- `void Sort(Array keys, Array items, IComparer comparer)`
  （void Sort（数组 keys, 数组 items, IComparer comparer））
- `void Sort(Array keys, Array items, int index, int length)`
  （void Sort（数组 keys, 数组 items, int index, int length））
- `void Sort(Array keys, Array items, int index, int length, IComparer comparer)`
  （void Sort（数组 keys, 数组 items, int index, int length, IComparer comparer））
- `IEnumerator GetEnumerator()`
  （IEnumerator 获取枚举器（））
- `int InternalArray__ICollection_get_Count()`
  （int 内部的Array__ICollection_get_数量（））
- `bool InternalArray__ICollection_get_IsReadOnly()`
  （bool 内部的Array__ICollection_get_是否ReadOnly（））
- `void InternalArray__ICollection_Clear()`
  （void 内部的Array__ICollection_清除（））
- `int InternalArray__IReadOnlyCollection_get_Count()`
  （int 内部的Array__IReadOnlyCollection_get_数量（））
- `void InternalArray__RemoveAt(int index)`
  （void 内部的Array__移除At（int index））
- `int get_Length()`
  （整数 获取_长度（））
- `int get_Rank()`
  （int get_排名（））
- `int GetRank()`
  （int 获取排名（））
- `int GetLength(int dimension)`
  （int 获取Length（int dimension））
- `int GetLowerBound(int dimension)`
  （int 获取下半身Bound（int dimension））
- `object GetValue(int[] indices)`
  （object 获取值（int[] indices））
- `void SetValue(object value, int[] indices)`
  （void 集合值（object value, int[] indices））
- `object GetValueImpl(int pos)`
  （object 获取值Impl（int pos））
- `void SetValueImpl(object value, int pos)`
  （void 集合值Impl（object value, int pos））
- `bool FastCopy(Array source, int source_idx, Array dest, int dest_idx, int length)`
  （bool Fast复制（数组 source, int source_idx, 数组 dest, int dest_idx, int length））
- `Array CreateInstanceImpl(Type elementType, int[] lengths, int[] bounds)`
  （数组 创建实例Impl（类型 elementType, int[] lengths, int[] bounds））
- `int GetUpperBound(int dimension)`
  （int 获取上半身Bound（int dimension））
- `object GetValue(int index)`
  （object 获取值（int index））
- `object GetValue(int index1, int index2)`
  （object 获取值（int index1, int index2））
- `object GetValue(int index1, int index2, int index3)`
  （object 获取值（int index1, int index2, int index3））
- `void SetValue(object value, int index)`
  （void 集合值（object value, int index））
- `void SetValue(object value, int index1, int index2)`
  （void 集合值（object value, int index1, int index2））
- `void SetValue(object value, int index1, int index2, int index3)`
  （void 集合值（object value, int index1, int index2, int index3））
- `Array UnsafeCreateInstance(Type elementType, int[] lengths, int[] lowerBounds)`
  （数组 Unsafe创建实例（类型 elementType, int[] lengths, int[] lowerBounds））
- `Array UnsafeCreateInstance(Type elementType, int length1, int length2)`
  （数组 Unsafe创建实例（类型 elementType, int length1, int length2））
- `Array UnsafeCreateInstance(Type elementType, int[] lengths)`
  （数组 Unsafe创建实例（类型 elementType, int[] lengths））
- `Array CreateInstance(Type elementType, int length)`
  （数组 创建实例（类型 elementType, int length））
- `Array CreateInstance(Type elementType, int length1, int length2)`
  （数组 创建实例（类型 elementType, int length1, int length2））
- `Array CreateInstance(Type elementType, int length1, int length2, int length3)`
  （数组 创建实例（类型 elementType, int length1, int length2, int length3））
- `Array CreateInstance(Type elementType, int[] lengths)`
  （数组 创建实例（类型 elementType, int[] lengths））
- `Array CreateInstance(Type elementType, int[] lengths, int[] lowerBounds)`
  （数组 创建实例（类型 elementType, int[] lengths, int[] lowerBounds））
- `void Clear(Array array, int index, int length)`
  （void 清除（数组 array, int index, int length））
- `void ClearInternal(Array a, int index, int count)`
  （void 清除内部的（数组 a, int index, int count））
- `void Copy(Array sourceArray, Array destinationArray, int length)`
  （void 复制（数组 sourceArray, 数组 destinationArray, int length））
- `void Copy(Array sourceArray, int sourceIndex, Array destinationArray, int destinationIndex, int length)`
  （void 复制（数组 sourceArray, int sourceIndex, 数组 destinationArray, int destinationIndex, int length））
- `Exception CreateArrayTypeMismatchException()`
  （Exception 创建数组类型MismatchException（））
- `bool CanAssignArrayElement(Type source, Type target)`
  （bool 能否Assign数组元素（类型 source, 类型 target））
- `void ConstrainedCopy(Array sourceArray, int sourceIndex, Array destinationArray, int destinationIndex, int length)`
  （void Constrained复制（数组 sourceArray, int sourceIndex, 数组 destinationArray, int destinationIndex, int length））
- `void Initialize()`
  （void 初始化（））
- `void SortImpl(Array keys, Array items, int index, int length, IComparer comparer)`
  （void SortImpl（数组 keys, 数组 items, int index, int length, IComparer comparer））

---

## Array.ArrayEnumerator（Array.数组Enumerator）

**继承**: IEnumerator, ICloneable（IEnumerator, ICloneable可克隆）

### 字段 (3)

- `Array _array`（数组 _array）(偏移: 0x8)
- `int _index`（整数 _索引）(偏移: 0xC)
- `int _endIndex`（int _end索引）(偏移: 0x10)

### 方法 (4)

- `bool MoveNext()`
  （布尔值 移动下一个（））
- `void Reset()`
  （void 重置（））
- `object Clone()`
  （对象 克隆（））
- `object get_Current()`
  （对象 获取_当前（））

---

## Array.SorterGenericArray（Array.SorterGeneric数组）

### 字段 (3)

- `Array keys`（数组 keys）(偏移: 0x0)
- `Array items`（数组 items）(偏移: 0x4)
- `IComparer comparer`（I比较器 comparer）(偏移: 0x8)

### 方法 (9)

- `void SwapIfGreaterWithItems(int a, int b)`
  （void SwapIfGreaterWithItems（int a, int b））
- `void Swap(int i, int j)`
  （void Swap（int i, int j））
- `void Sort(int left, int length)`
  （void Sort（int left, int length））
- `void IntrospectiveSort(int left, int length)`
  （void IntrospectiveSort（int left, int length））
- `void IntroSort(int lo, int hi, int depthLimit)`
  （void IntroSort（int lo, int hi, int depthLimit））
- `int PickPivotAndPartition(int lo, int hi)`
  （int PickPivotAndPartition（int lo, int hi））
- `void Heapsort(int lo, int hi)`
  （void Heapsort（int lo, int hi））
- `void DownHeap(int i, int n, int lo)`
  （void 下Heap（int i, int n, int lo））
- `void InsertionSort(int lo, int hi)`
  （void InsertionSort（int lo, int hi））

---

## Array.SorterObjectArray（Array.Sorter对象数组）

### 字段 (3)

- `object[] keys`（object[] keys）(偏移: 0x0)
- `object[] items`（object[] items）(偏移: 0x4)
- `IComparer comparer`（I比较器 comparer）(偏移: 0x8)

### 方法 (9)

- `void SwapIfGreaterWithItems(int a, int b)`
  （void SwapIfGreaterWithItems（int a, int b））
- `void Swap(int i, int j)`
  （void Swap（int i, int j））
- `void Sort(int left, int length)`
  （void Sort（int left, int length））
- `void IntrospectiveSort(int left, int length)`
  （void IntrospectiveSort（int left, int length））
- `void IntroSort(int lo, int hi, int depthLimit)`
  （void IntroSort（int lo, int hi, int depthLimit））
- `int PickPivotAndPartition(int lo, int hi)`
  （int PickPivotAndPartition（int lo, int hi））
- `void Heapsort(int lo, int hi)`
  （void Heapsort（int lo, int hi））
- `void DownHeap(int i, int n, int lo)`
  （void 下Heap（int i, int n, int lo））
- `void InsertionSort(int lo, int hi)`
  （void InsertionSort（int lo, int hi））

---

## ArrayConverter（数组Converter）

**继承**: CollectionConverter（CollectionConverter）

### 方法 (3)

- `object ConvertTo(ITypeDescriptorContext context, CultureInfo culture, object value, Type destinationType)`
  （对象 转换到（I类型描述符上下文 context, 区域性信息 culture, 对象 value, 类型 destinationType））
- `PropertyDescriptorCollection GetProperties(ITypeDescriptorContext context, object value, Attribute[] attributes)`
  （属性描述符集合 获取属性（I类型描述符上下文 context, 对象 value, 属性[] attributes））
- `bool GetPropertiesSupported(ITypeDescriptorContext context)`
  （布尔值 获取属性支持（I类型描述符上下文 context））

---

## ArrayConverter.ArrayPropertyDescriptor（数组Converter.数组属性Descriptor）

**继承**: TypeConverter.SimplePropertyDescriptor（类型Converter.Simple属性Descriptor）

### 字段 (1)

- `int index`（整数 索引）(偏移: 0x4C)

---

## ArrayList（数组列表）

**继承**: IList, ICollection, IEnumerable, ICloneable（I列表, ICollection, IEnumerable, ICloneable）

### 字段 (5)

- `object[] _items`（object[] _items）(偏移: 0x8)
- `int _size`（整数 _大小）(偏移: 0xC)
- `int _version`（整数 _版本）(偏移: 0x10)
- `object _syncRoot`（对象 _同步根）(偏移: 0x14)
- `object[] emptyArray`（object[] empty数组）(偏移: 0x0)

### 方法 (27)

- `void set_Capacity(int value)`
  （void 设置_容量（整数 value））
- `int get_Count()`
  （整数 获取_数量（））
- `bool get_IsFixedSize()`
  （bool get_是否固定大小（））
- `bool get_IsReadOnly()`
  （布尔值 获取_是否只读（））
- `object get_SyncRoot()`
  （对象 获取_同步根（））
- `object get_Item(int index)`
  （对象 获取_项（整数 index））
- `void set_Item(int index, object value)`
  （void set_项目（int index, object value））
- `ArrayList Adapter(IList list)`
  （数组列表 适配器（I列表 list））
- `int Add(object value)`
  （int 添加（object value））
- `void AddRange(ICollection c)`
  （void 添加范围（ICollection c））
- `void Clear()`
  （void 清除（））
- `object Clone()`
  （对象 克隆（））
- `bool Contains(object item)`
  （bool Contains（object item））
- `void CopyTo(Array array)`
  （void 复制To（数组 array））
- `void CopyTo(Array array, int arrayIndex)`
  （void 复制到（数组 array, 整数 arrayIndex））
- `void CopyTo(int index, Array array, int arrayIndex, int count)`
  （void 复制To（int index, 数组 array, int arrayIndex, int count））
- `void EnsureCapacity(int min)`
  （void EnsureCapacity（int min））
- `IEnumerator GetEnumerator()`
  （IEnumerator 获取枚举器（））
- `int IndexOf(object value)`
  （int 索引Of（object value））
- `void Insert(int index, object value)`
  （void 插入（整数 index, 对象 value））
- `void InsertRange(int index, ICollection c)`
  （void Insert范围（int index, ICollection c））
- `void Remove(object obj)`
  （void 移除（object obj））
- `void RemoveAt(int index)`
  （void 移除在（整数 index））
- `void Sort(IComparer comparer)`
  （void Sort（IComparer comparer））
- `void Sort(int index, int count, IComparer comparer)`
  （void Sort（int index, int count, IComparer comparer））
- `object[] ToArray()`
  （对象[] 转数组（））
- `Array ToArray(Type type)`
  （数组 To数组（类型 type））

---

## ArrayList.ArrayListDebugView（数组List.数组列表Debug视图）

### 字段 (1)

- `ArrayList arrayList`（数组列表 array列表）(偏移: 0x8)

### 方法 (1)

- `object[] get_Items()`
  （object[] get_Items（））

---

## ArrayList.ArrayListEnumeratorSimple（数组List.数组列表EnumeratorSimple）

**继承**: IEnumerator, ICloneable（IEnumerator, ICloneable可克隆）

### 字段 (6)

- `ArrayList list`（数组列表 list）(偏移: 0x8)
- `int index`（整数 索引）(偏移: 0xC)
- `int version`（整数 版本）(偏移: 0x10)
- `object currentElement`（object current元素）(偏移: 0x14)
- `bool isArrayList`（bool is数组列表）(偏移: 0x18)
- `object dummyObject`（object dummy对象）(偏移: 0x0)

### 方法 (4)

- `object Clone()`
  （对象 克隆（））
- `bool MoveNext()`
  （布尔值 移动下一个（））
- `object get_Current()`
  （对象 获取_当前（））
- `void Reset()`
  （void 重置（））

---

## ArrayList.IListWrapper（数组List.I列表包装器）

**继承**: ArrayList（数组列表）

### 字段 (1)

- `IList _list`（I列表 _list）(偏移: 0x18)

### 方法 (23)

- `void set_Capacity(int value)`
  （void 设置_容量（整数 value））
- `int get_Count()`
  （整数 获取_数量（））
- `bool get_IsReadOnly()`
  （布尔值 获取_是否只读（））
- `bool get_IsFixedSize()`
  （bool get_是否固定大小（））
- `object get_Item(int index)`
  （对象 获取_项（整数 index））
- `void set_Item(int index, object value)`
  （void set_项目（int index, object value））
- `object get_SyncRoot()`
  （对象 获取_同步根（））
- `int Add(object obj)`
  （int 添加（object obj））
- `void AddRange(ICollection c)`
  （void 添加范围（ICollection c））
- `void Clear()`
  （void 清除（））
- `object Clone()`
  （对象 克隆（））
- `bool Contains(object obj)`
  （bool Contains（object obj））
- `void CopyTo(Array array, int index)`
  （void 复制到（数组 array, 整数 index））
- `void CopyTo(int index, Array array, int arrayIndex, int count)`
  （void 复制To（int index, 数组 array, int arrayIndex, int count））
- `IEnumerator GetEnumerator()`
  （IEnumerator 获取枚举器（））
- `int IndexOf(object value)`
  （int 索引Of（object value））
- `void Insert(int index, object obj)`
  （void Insert（int index, object obj））
- `void InsertRange(int index, ICollection c)`
  （void Insert范围（int index, ICollection c））
- `void Remove(object value)`
  （void 移除（object value））
- `void RemoveAt(int index)`
  （void 移除在（整数 index））
- `void Sort(int index, int count, IComparer comparer)`
  （void Sort（int index, int count, IComparer comparer））
- `object[] ToArray()`
  （对象[] 转数组（））
- `Array ToArray(Type type)`
  （数组 To数组（类型 type））

---

## ArraySpec（数组Spec）

**继承**: ModifierSpec（修改器Spec）

### 字段 (2)

- `int dimensions`（int dimensions）(偏移: 0x8)
- `bool bound`（bool bound）(偏移: 0xC)

### 方法 (3)

- `Type Resolve(Type type)`
  （类型 Resolve（类型 type））
- `StringBuilder Append(StringBuilder sb)`
  （字符串构建器 Append（字符串构建器 sb））
- `string ToString()`
  （字符串 转字符串（））

---

## ArraySubsetEnumerator（数组SubsetEnumerator）

**继承**: IEnumerator（IEnumerator枚举器）

### 字段 (3)

- `Array array`（数组 array）(偏移: 0x8)
- `int total`（int total）(偏移: 0xC)
- `int current`（int current）(偏移: 0x10)

### 方法 (3)

- `bool MoveNext()`
  （布尔值 移动下一个（））
- `void Reset()`
  （void 重置（））
- `object get_Current()`
  （对象 获取_当前（））

---

## AsceticHeroSFX（Ascetic英雄SFX）

**继承**: AnimSFX（动画SFX）

### 字段 (2)

- `Texture baseTex`（纹理 baseTex）(偏移: 0x3C)
- `Texture blastTex`（纹理 blastTex）(偏移: 0x40)

### 方法 (1)

- `void set_isBlast(bool value)`
  （void set_isBlast（bool value））

---

## AsnDecodeStatus（AsnDecodeStatus）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AsnEncodedData（AsnEncoded数据）

### 字段 (2)

- `Oid _oid`（Oid _oid）(偏移: 0x8)
- `byte[] _raw`（byte[] _raw）(偏移: 0xC)

### 方法 (12)

- `void set_Oid(Oid value)`
  （void set_Oid（Oid value））
- `byte[] get_RawData()`
  （byte[] get_Raw数据（））
- `void set_RawData(byte[] value)`
  （void set_Raw数据（byte[] value））
- `void CopyFrom(AsnEncodedData asnEncodedData)`
  （void 复制自（Asn编码数据 asnEncodedData））
- `string ToString(bool multiLine)`
  （字符串 转字符串（布尔值 多行））
- `string Default(bool multiLine)`
  （string 默认的（bool multiLine））
- `string BasicConstraintsExtension(bool multiLine)`
  （string BasicConstraints扩展（bool multiLine））
- `string EnhancedKeyUsageExtension(bool multiLine)`
  （string Enhanced键Usage扩展（bool multiLine））
- `string KeyUsageExtension(bool multiLine)`
  （string 键Usage扩展（bool multiLine））
- `string SubjectKeyIdentifierExtension(bool multiLine)`
  （string Subject键Identifier扩展（bool multiLine））
- `string SubjectAltName(bool multiLine)`
  （string SubjectAlt名称（bool multiLine））
- `string NetscapeCertType(bool multiLine)`
  （string NetscapeCert类型（bool multiLine））

---

## AspectRatioFitter（Aspect比率Fitter）

**继承**: UIBehaviour, ILayoutSelfController, ILayoutController（界面Behaviour, ILayoutSelf控制器, ILayout控制器）

### 字段 (6)

- `AspectRatioFitter.AspectMode m_AspectMode`（Aspect比率Fitter.Aspect模式 m_Aspect模式）(偏移: 0xC)
- `float m_AspectRatio`（float m_Aspect比率）(偏移: 0x10)
- `RectTransform m_Rect`（矩形变换 m_Rect）(偏移: 0x14)
- `bool m_DelayedSetDirty`（bool m_Delayed集合Dirty）(偏移: 0x18)
- `bool m_DoesParentExist`（bool m_Does父级Exist）(偏移: 0x19)
- `DrivenRectTransformTracker m_Tracker`（驱动矩形变换跟踪器 m_跟踪器）(偏移: 0x1A)

### 方法 (20)

- `AspectRatioFitter.AspectMode get_aspectMode()`
  （Aspect比率Fitter.Aspect模式 get_aspect模式（））
- `void set_aspectMode(AspectRatioFitter.AspectMode value)`
  （void set_aspect模式（Aspect比率Fitter.Aspect模式 value））
- `float get_aspectRatio()`
  （float get_aspect比率（））
- `void set_aspectRatio(float value)`
  （void set_aspect比率（float value））
- `RectTransform get_rectTransform()`
  （矩形变换 获取_矩形变换（））
- `void OnEnable()`
  （void 启用时（））
- `void Start()`
  （void 开始（））
- `void OnDisable()`
  （void 禁用时（））
- `void OnTransformParentChanged()`
  （void 变换父级改变时（））
- `void Update()`
  （void 更新（））
- `void OnRectTransformDimensionsChange()`
  （void 矩形变换尺寸改变时（））
- `void UpdateRect()`
  （void 更新Rect（））
- `float GetSizeDeltaToProduceSize(float size, int axis)`
  （float 获取大小DeltaToProduce大小（float size, int axis））
- `Vector2 GetParentSize()`
  （二维向量 获取父级大小（））
- `void SetLayoutHorizontal()`
  （void 设置布局水平（））
- `void SetLayoutVertical()`
  （void 设置布局垂直（））
- `void SetDirty()`
  （void 设置_脏（））
- `bool IsComponentValidOnObject()`
  （bool 是否组件ValidOn对象（））
- `bool IsAspectModeValid()`
  （bool 是否Aspect模式Valid（））
- `bool DoesParentExists()`
  （bool Does父级Exists（））

---

## AspectRatioFitter.AspectMode（Aspect比率Fitter.Aspect模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Assembly（Assembly）

**继承**: ICustomAttributeProvider, ISerializable, _Assembly（I自定义的Attribute提供者, ISerializable, _Assembly）

### 字段 (10)

- `IntPtr _mono_assembly`（整数Ptr _mono_assembly）(偏移: 0x8)
- `Assembly.ResolveEventHolder resolve_event_holder`（Assembly.Resolve事件Holder resolve_event_holder）(偏移: 0xC)
- `object _evidence`（object _evidence）(偏移: 0x10)
- `object _minimum`（object _minimum）(偏移: 0x14)
- `object _optional`（object _optional）(偏移: 0x18)
- `object _refuse`（object _refuse）(偏移: 0x1C)
- `object _granted`（object _granted）(偏移: 0x20)
- `object _denied`（object _denied）(偏移: 0x24)
- `bool fromByteArray`（bool fromByte数组）(偏移: 0x28)
- `string assemblyName`（string assembly名称）(偏移: 0x2C)

### 方法 (51)

- `string get_code_base(bool escaped)`
  （string get_code_base（bool escaped））
- `string get_fullname()`
  （string get_fullname（））
- `string get_location()`
  （string get_location（））
- `string GetAotId()`
  （string 获取AotId（））
- `string GetCodeBase(bool escaped)`
  （string 获取Code基础（bool escaped））
- `string get_CodeBase()`
  （string get_Code基础（））
- `string get_FullName()`
  （字符串 获取_全名称（））
- `string get_Location()`
  （string get_Location（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））
- `bool IsDefined(Type attributeType, bool inherit)`
  （布尔值 是否已定义（类型 attributeType, 布尔值 继承））
- `object[] GetCustomAttributes(Type attributeType, bool inherit)`
  （对象[] 获取自定义属性（类型 attributeType, 布尔值 继承））
- `IntPtr GetManifestResourceInternal(string name, out int size, out Module module)`
  （整数Ptr 获取Manifest资源内部的（string name, out int size, out Module module））
- `Stream GetManifestResourceStream(string name)`
  （流 获取Manifest资源流（string name））
- `Stream GetManifestResourceStream(Type type, string name, bool skipSecurityCheck, ref StackCrawlMark stackMark)`
  （流 获取Manifest资源流（类型 type, string name, bool skipSecurityCheck, ref StackCrawlMark stackMark））
- `Stream GetManifestResourceStream(string name, ref StackCrawlMark stackMark, bool skipSecurityCheck)`
  （流 获取Manifest资源流（string name, ref StackCrawlMark stackMark, bool skipSecurityCheck））
- `string GetSimpleName()`
  （string 获取Simple名称（））
- `byte[] GetPublicKey()`
  （byte[] 获取公开的键（））
- `Version GetVersion()`
  （Version 获取Version（））
- `AssemblyNameFlags GetFlags()`
  （Assembly名称Flags 获取Flags（））
- `Type[] GetTypes(bool exportedOnly)`
  （Type[] 获取Types（bool exportedOnly））
- `Type[] GetTypes()`
  （Type[] 获取Types（））
- `Type GetType(string name)`
  （类型 获取类型（string name））
- `Type InternalGetType(Module module, string name, bool throwOnError, bool ignoreCase)`
  （类型 内部的获取类型（模块 module, string name, bool throwOnError, bool ignoreCase））
- `AssemblyName GetName(bool copiedName)`
  （Assembly名称 获取名称（bool copiedName））
- `AssemblyName GetName()`
  （Assembly名称 获取名称（））
- `string ToString()`
  （字符串 转字符串（））
- `Assembly GetAssembly(Type type)`
  （Assembly 获取Assembly（类型 type））
- `RuntimeAssembly InternalGetSatelliteAssembly(string name, CultureInfo culture, Version version, bool throwOnFileNotFound, ref StackCrawlMark stackMark)`
  （RuntimeAssembly 内部的获取SatelliteAssembly（string name, Culture信息 culture, Version version, bool throwOnFileNotFound, ref StackCrawlMark stackMark））
- `Assembly LoadFrom(string assemblyFile, bool refonly)`
  （Assembly 加载From（string assemblyFile, bool refonly））
- `Assembly LoadFrom(string assemblyFile)`
  （Assembly 加载From（string assemblyFile））
- `Assembly Load(string assemblyString)`
  （Assembly 加载（string assemblyString））
- `Assembly load_with_partial_name(string name, Evidence e)`
  （Assembly load_with_partial_name（string name, Evidence e））
- `Assembly LoadWithPartialName(string partialName, Evidence securityEvidence)`
  （Assembly 加载WithPartial名称（string partialName, Evidence securityEvidence））
- `Assembly LoadWithPartialName(string partialName, Evidence securityEvidence, bool oldBehavior)`
  （Assembly 加载WithPartial名称（string partialName, Evidence securityEvidence, bool oldBehavior））
- `Module[] GetModules()`
  （Module[] 获取Modules（））
- `Module[] GetModulesInternal()`
  （Module[] 获取Modules内部的（））
- `string[] GetManifestResourceNames()`
  （string[] 获取Manifest资源Names（））
- `Assembly GetExecutingAssembly()`
  （Assembly 获取ExecutingAssembly（））
- `Assembly GetCallingAssembly()`
  （Assembly 获取CallingAssembly（））
- `bool GetManifestResourceInfoInternal(string name, ManifestResourceInfo info)`
  （bool 获取Manifest资源信息内部的（string name, Manifest资源信息 info））
- `ManifestResourceInfo GetManifestResourceInfo(string resourceName)`
  （Manifest资源信息 获取Manifest资源信息（string resourceName））
- `bool get_ReflectionOnly()`
  （bool get_ReflectionOnly（））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `bool Equals(object o)`
  （布尔值 等于（对象 o））
- `Exception CreateNIE()`
  （Exception 创建NIE（））
- `bool get_IsFullyTrusted()`
  （bool get_是否FullyTrusted（））
- `Type GetType(string name, bool throwOnError, bool ignoreCase)`
  （类型 获取类型（string name, bool throwOnError, bool ignoreCase））
- `Module GetModule(string name)`
  （模块 获取模块（string name））
- `Module[] GetModules(bool getResourceModules)`
  （Module[] 获取Modules（bool getResourceModules））
- `bool op_Equality(Assembly left, Assembly right)`
  （bool op_Equality（Assembly left, Assembly right））
- `bool op_Inequality(Assembly left, Assembly right)`
  （bool op_Inequality（Assembly left, Assembly right））

---

## Assembly.UnmanagedMemoryStreamForModule（Assembly.UnmanagedMemory流For模块）

**继承**: UnmanagedMemoryStream（UnmanagedMemory流）

### 字段 (1)

- `Module module`（模块 module）(偏移: 0x48)

### 方法 (1)

- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））

---

## AssemblyCompanyAttribute（AssemblyCompanyAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `string m_company`（string m_company）(偏移: 0x8)

---

## AssemblyConfigurationAttribute（AssemblyConfigurationAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `string m_configuration`（string m_configuration）(偏移: 0x8)

---

## AssemblyContentType（AssemblyContent类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AssemblyCopyrightAttribute（AssemblyCopyrightAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `string m_copyright`（string m_copyright）(偏移: 0x8)

---

## AssemblyDefaultAliasAttribute（Assembly默认的AliasAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `string m_defaultAlias`（string m_defaultAlias）(偏移: 0x8)

---

## AssemblyDelaySignAttribute（Assembly延迟标志Attribute）

**继承**: Attribute（属性）

### 字段 (1)

- `bool m_delaySign`（bool m_delay标志）(偏移: 0x8)

---

## AssemblyDescriptionAttribute（AssemblyDescriptionAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `string m_description`（string m_description）(偏移: 0x8)

---

## AssemblyFileVersionAttribute（Assembly文件VersionAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `string _version`（string _version）(偏移: 0x8)

---

## AssemblyHashAlgorithm（AssemblyHashAlgorithm）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AssemblyInformationalVersionAttribute（AssemblyInformationalVersionAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `string m_informationalVersion`（string m_informationalVersion）(偏移: 0x8)

---

## AssemblyKeyFileAttribute（Assembly键文件Attribute）

**继承**: Attribute（属性）

### 字段 (1)

- `string m_keyFile`（string m_key文件）(偏移: 0x8)

---

## AssemblyLoadEventArgs（Assembly加载事件Args）

**继承**: EventArgs（事件参数）

### 字段 (1)

- `Assembly m_loadedAssembly`（Assembly m_loadedAssembly）(偏移: 0x8)

---

## AssemblyLoadEventHandler（Assembly加载事件处理器）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(object sender, AssemblyLoadEventArgs args)`
  （void Invoke（object sender, Assembly加载事件Args args））
- `IAsyncResult BeginInvoke(object sender, AssemblyLoadEventArgs args, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（object sender, Assembly加载事件Args args, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## AssemblyName（Assembly名称）

**继承**: ICloneable, ISerializable, IDeserializationCallback, _AssemblyName（ICloneable, ISerializable, IDeserialization回调, _Assembly名称）

### 字段 (16)

- `string name`（字符串 名称）(偏移: 0x8)
- `string codebase`（string codebase）(偏移: 0xC)
- `int major`（int major）(偏移: 0x10)
- `int minor`（int minor）(偏移: 0x14)
- `int build`（int build）(偏移: 0x18)
- `int revision`（int revision）(偏移: 0x1C)
- `CultureInfo cultureinfo`（Culture信息 cultureinfo）(偏移: 0x20)
- `AssemblyNameFlags flags`（Assembly名称Flags flags）(偏移: 0x24)
- `AssemblyHashAlgorithm hashalg`（AssemblyHashAlgorithm hashalg）(偏移: 0x28)
- `StrongNameKeyPair keypair`（Strong名称键Pair keypair）(偏移: 0x2C)
- `byte[] publicKey`（byte[] public键）(偏移: 0x30)
- `byte[] keyToken`（byte[] key令牌）(偏移: 0x34)
- `AssemblyVersionCompatibility versioncompat`（AssemblyVersionCompatibility versioncompat）(偏移: 0x38)
- `Version version`（Version version）(偏移: 0x3C)
- `ProcessorArchitecture processor_architecture`（ProcessorArchitecture processor_architecture）(偏移: 0x40)
- `AssemblyContentType contentType`（AssemblyContent类型 content类型）(偏移: 0x44)

### 方法 (24)

- `bool ParseAssemblyName(IntPtr name, out MonoAssemblyName aname, out bool is_version_definited, out bool is_token_defined)`
  （bool 解析Assembly名称（整数Ptr name, out MonoAssemblyName aname, out bool is_version_definited, out bool is_token_defined））
- `string get_Name()`
  （字符串 获取_名称（））
- `void set_Name(string value)`
  （void 设置_名称（字符串 value））
- `CultureInfo get_CultureInfo()`
  （Culture信息 get_Culture信息（））
- `void set_CultureInfo(CultureInfo value)`
  （void set_Culture信息（Culture信息 value））
- `AssemblyNameFlags get_Flags()`
  （Assembly名称Flags get_Flags（））
- `void set_Flags(AssemblyNameFlags value)`
  （void set_Flags（Assembly名称Flags value））
- `string get_FullName()`
  （字符串 获取_全名称（））
- `Version get_Version()`
  （Version get_Version（））
- `void set_Version(Version value)`
  （void set_Version（Version value））
- `string ToString()`
  （字符串 转字符串（））
- `byte[] GetPublicKey()`
  （byte[] 获取公开的键（））
- `byte[] GetPublicKeyToken()`
  （byte[] 获取公开的键令牌（））
- `bool get_IsPublicKeyValid()`
  （bool get_是否公开的键Valid（））
- `byte[] InternalGetPublicKeyToken()`
  （byte[] 内部的获取公开的键令牌（））
- `void get_public_token(byte* token, byte* pubkey, int len)`
  （void get_public_token（byte* token, byte* pubkey, int len））
- `byte[] ComputePublicKeyToken()`
  （byte[] Compute公开的键令牌（））
- `void SetPublicKey(byte[] publicKey)`
  （void 集合公开的键（byte[] publicKey））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））
- `object Clone()`
  （对象 克隆（））
- `void OnDeserialization(object sender)`
  （void 反序列化时（对象 sender））
- `MonoAssemblyName* GetNativeName(IntPtr assembly_ptr)`
  （MonoAssemblyName* 获取Native名称（整数Ptr assembly_ptr））
- `void FillName(MonoAssemblyName* native, string codeBase, bool addVersion, bool addPublickey, bool defaultToken, bool assemblyRef)`
  （void Fill名称（MonoAssemblyName* native, string codeBase, bool addVersion, bool addPublickey, bool defaultToken, bool assemblyRef））
- `AssemblyName Create(Assembly assembly, bool fillCodebase)`
  （Assembly名称 创建（Assembly assembly, bool fillCodebase））

---

## AssemblyNameFlags（Assembly名称Flags）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AssemblyProductAttribute（AssemblyProductAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `string m_product`（string m_product）(偏移: 0x8)

---

## AssemblyTitleAttribute（AssemblyTitleAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `string m_title`（string m_title）(偏移: 0x8)

---

## AssemblyTrademarkAttribute（AssemblyTrademarkAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `string m_trademark`（string m_trademark）(偏移: 0x8)

---

## AssemblyVersionCompatibility（AssemblyVersionCompatibility）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AssetLoadingSubsystem（资产LoadingSubsystem）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AssetManager（资产管理器）

**继承**: Singleton<AssetManager>（Singleton<资产Manager>）

### 字段 (1)

- `GameAsset asset`（游戏资产 asset）(偏移: 0xC)

### 方法 (3)

- `float GetAnimSpeed(float input)`
  （float 获取动画Speed（float input））
- `Texture2D GetVipLevelIcon(int level)`
  （Texture2D 获取Vip等级图标（int level））
- `Texture2D GetSmallLevelIcon(int level)`
  （Texture2D 获取Small等级图标（int level））

---

## AstarColor（Astar颜色）

### 字段 (14)

- `Color _SolidColor`（颜色 _Solid颜色）(偏移: 0x8)
- `Color _UnwalkableNode`（颜色 _Unwalkable节点）(偏移: 0x18)
- `Color _BoundsHandles`（颜色 _BoundsHandles）(偏移: 0x28)
- `Color _ConnectionLowLerp`（颜色 _连接LowLerp）(偏移: 0x38)
- `Color _ConnectionHighLerp`（颜色 _连接HighLerp）(偏移: 0x48)
- `Color _MeshEdgeColor`（颜色 _网格Edge颜色）(偏移: 0x58)
- `Color[] _AreaColors`（Color[] _AreaColors）(偏移: 0x68)
- `Color SolidColor`（颜色 Solid颜色）(偏移: 0x0)
- `Color UnwalkableNode`（颜色 Unwalkable节点）(偏移: 0x10)
- `Color BoundsHandles`（颜色 BoundsHandles）(偏移: 0x20)
- `Color ConnectionLowLerp`（颜色 连接LowLerp）(偏移: 0x30)
- `Color ConnectionHighLerp`（颜色 连接HighLerp）(偏移: 0x40)
- `Color MeshEdgeColor`（颜色 网格Edge颜色）(偏移: 0x50)
- `Color[] AreaColors`（Color[] AreaColors）(偏移: 0x60)

### 方法 (4)

- `int ColorHash()`
  （int 颜色Hash（））
- `Color GetAreaColor(uint area)`
  （颜色 获取Area颜色（uint area））
- `Color GetTagColor(uint tag)`
  （颜色 获取标签颜色（uint tag））
- `void PushToStatic(AstarPath astar)`
  （void PushTo静态的（Astar路径 astar））

---

## AstarData（Astar数据）

### 字段 (7)

- `NavGraph[] graphs`（NavGraph[] graphs）(偏移: 0x20)
- `string dataString`（string data字符串）(偏移: 0x24)
- `byte[] upgradeData`（byte[] upgrade数据）(偏移: 0x28)
- `TextAsset file_cachedStartup`（文本资产 file_cachedStartup）(偏移: 0x2C)
- `byte[] data_cachedStartup`（byte[] data_cachedStartup）(偏移: 0x30)
- `bool cacheStartup`（bool cacheStartup）(偏移: 0x34)
- `List<bool> graphStructureLocked`（List<bool> graphStructure锁定的）(偏移: 0x38)

### 方法 (49)

- `AstarPath get_active()`
  （Astar路径 get_active（））
- `NavMeshGraph get_navmesh()`
  （Nav网格Graph get_navmesh（））
- `void set_navmesh(NavMeshGraph value)`
  （void set_navmesh（Nav网格Graph value））
- `GridGraph get_gridGraph()`
  （网格Graph get_gridGraph（））
- `void set_gridGraph(GridGraph value)`
  （void set_gridGraph（网格Graph value））
- `LayerGridGraph get_layerGridGraph()`
  （层网格Graph get_layer网格Graph（））
- `void set_layerGridGraph(LayerGridGraph value)`
  （void set_layer网格Graph（层网格Graph value））
- `PointGraph get_pointGraph()`
  （PointGraph get_pointGraph（））
- `void set_pointGraph(PointGraph value)`
  （void set_pointGraph（PointGraph value））
- `RecastGraph get_recastGraph()`
  （RecastGraph get_recastGraph（））
- `void set_recastGraph(RecastGraph value)`
  （void set_recastGraph（RecastGraph value））
- `Type[] get_graphTypes()`
  （Type[] get_graphTypes（））
- `void set_graphTypes(Type[] value)`
  （void set_graphTypes（Type[] value））
- `byte[] get_data()`
  （byte[] get_data（））
- `void set_data(byte[] value)`
  （void set_data（byte[] value））
- `byte[] GetData()`
  （byte[] 获取数据（））
- `void SetData(byte[] data)`
  （void 集合数据（byte[] data））
- `void Awake()`
  （void 唤醒（））
- `void LockGraphStructure(bool allowAddingGraphs = False)`
  （void LockGraphStructure（bool allowAddingGraphs = False））
- `void UnlockGraphStructure()`
  （void UnlockGraphStructure（））
- `PathProcessor.GraphUpdateLock AssertSafe(bool onlyAddingGraph = False)`
  （路径Processor.Graph更新Lock AssertSafe（bool onlyAddingGraph = False））
- `void GetNodes(Action<GraphNode> callback)`
  （void 获取Nodes（Action<GraphNode> callback））
- `void UpdateShortcuts()`
  （void 更新Shortcuts（））
- `void LoadFromCache()`
  （void 加载From缓存（））
- `byte[] SerializeGraphs()`
  （byte[] SerializeGraphs（））
- `byte[] SerializeGraphs(SerializeSettings settings)`
  （byte[] SerializeGraphs（SerializeSettings settings））
- `byte[] SerializeGraphs(SerializeSettings settings, out uint checksum)`
  （byte[] SerializeGraphs（SerializeSettings settings, out uint checksum））
- `void DeserializeGraphs()`
  （void DeserializeGraphs（））
- `void ClearGraphs()`
  （void 清除Graphs（））
- `void OnDestroy()`
  （void 销毁时（））
- `void DeserializeGraphs(byte[] bytes)`
  （void DeserializeGraphs（byte[] bytes））
- `void DeserializeGraphsAdditive(byte[] bytes)`
  （void DeserializeGraphsAdditive（byte[] bytes））
- `void DeserializeGraphsPartAdditive(AstarSerializer sr)`
  （void DeserializeGraphsPartAdditive（AstarSerializer sr））
- `void FindGraphTypes()`
  （void 查找GraphTypes（））
- `Type GetGraphType(string type)`
  （类型 获取Graph类型（string type））
- `NavGraph CreateGraph(string type)`
  （NavGraph 创建Graph（string type））
- `NavGraph CreateGraph(Type type)`
  （NavGraph 创建Graph（类型 type））
- `NavGraph AddGraph(string type)`
  （NavGraph 添加Graph（string type））
- `NavGraph AddGraph(Type type)`
  （NavGraph 添加Graph（类型 type））
- `void AddGraph(NavGraph graph)`
  （void 添加Graph（NavGraph graph））
- `bool RemoveGraph(NavGraph graph)`
  （bool 移除Graph（NavGraph graph））
- `NavGraph GetGraph(GraphNode node)`
  （NavGraph 获取Graph（Graph节点 node））
- `NavGraph FindGraph(Func<NavGraph, bool> predicate)`
  （NavGraph 查找Graph（Func<NavGraph, bool> predicate））
- `NavGraph FindGraphOfType(Type type)`
  （NavGraph 查找GraphOf类型（类型 type））
- `NavGraph FindGraphWhichInheritsFrom(Type type)`
  （NavGraph 查找GraphWhichInheritsFrom（类型 type））
- `IEnumerable FindGraphsOfType(Type type)`
  （IEnumerable 查找GraphsOf类型（类型 type））
- `IEnumerable GetUpdateableGraphs()`
  （IEnumerable 获取UpdateableGraphs（））
- `IEnumerable GetRaycastableGraphs()`
  （IEnumerable 获取RaycastableGraphs（））
- `int GetGraphIndex(NavGraph graph)`
  （int 获取Graph索引（NavGraph graph））

---

## AstarDebugger（AstarDebugger）

**继承**: VersionedMonoBehaviour（版本化MonoBehaviour）

### 字段 (36)

- `int yOffset`（int yOffset）(偏移: 0x10)
- `bool show`（bool show）(偏移: 0x14)
- `bool showInEditor`（bool showInEditor）(偏移: 0x15)
- `bool showFPS`（bool showFPS）(偏移: 0x16)
- `bool showPathProfile`（bool show路径Profile）(偏移: 0x17)
- `bool showMemProfile`（bool showMemProfile）(偏移: 0x18)
- `bool showGraph`（bool showGraph）(偏移: 0x19)
- `int graphBufferSize`（int graph缓冲区大小）(偏移: 0x1C)
- `Font font`（Font font）(偏移: 0x20)
- `int fontSize`（int font大小）(偏移: 0x24)
- `StringBuilder text`（字符串构建器 text）(偏移: 0x28)
- `string cachedText`（string cached文本）(偏移: 0x2C)
- `float lastUpdate`（float last更新）(偏移: 0x30)
- `AstarDebugger.GraphPoint[] graph`（AstarDebugger.GraphPoint[] graph）(偏移: 0x34)
- `float delayedDeltaTime`（float delayedDelta时间）(偏移: 0x38)
- `float lastCollect`（float lastCollect）(偏移: 0x3C)
- `float lastCollectNum`（float lastCollectNum）(偏移: 0x40)
- `float delta`（float delta）(偏移: 0x44)
- `float lastDeltaTime`（float lastDelta时间）(偏移: 0x48)
- `int allocRate`（int allocRate）(偏移: 0x4C)
- `int lastAllocMemory`（int lastAllocMemory）(偏移: 0x50)
- `float lastAllocSet`（float lastAlloc集合）(偏移: 0x54)
- `int allocMem`（int allocMem）(偏移: 0x58)
- `int collectAlloc`（int collectAlloc）(偏移: 0x5C)
- `int peakAlloc`（int peakAlloc）(偏移: 0x60)
- `int fpsDropCounterSize`（int fpsDropCounter大小）(偏移: 0x64)
- `float[] fpsDrops`（float[] fpsDrops）(偏移: 0x68)
- `Rect boxRect`（Rect boxRect）(偏移: 0x6C)
- `GUIStyle style`（GUIStyle style）(偏移: 0x7C)
- `Camera cam`（摄像机 cam）(偏移: 0x80)
- `float graphWidth`（float graph宽度）(偏移: 0x84)
- `float graphHeight`（float graph高度）(偏移: 0x88)
- `float graphOffset`（float graphOffset）(偏移: 0x8C)
- `int maxVecPool`（int maxVec池）(偏移: 0x90)
- `int maxNodePool`（int max节点池）(偏移: 0x94)
- `AstarDebugger.PathTypeDebug[] debugTypes`（AstarDebugger.路径类型Debug[] debugTypes）(偏移: 0x98)

### 方法 (4)

- `void Start()`
  （void 开始（））
- `void LateUpdate()`
  （void 延迟更新（））
- `void DrawGraphLine(int index, Matrix4x4 m, float x1, float x2, float y1, float y2, Color color)`
  （void DrawGraphLine（int index, Matrix4x4 m, float x1, float x2, float y1, float y2, 颜色 color））
- `void OnGUI()`
  （void GUI时（））

---

## AstarDebugger.GraphPoint（AstarDebugger.GraphPoint）

### 字段 (3)

- `float fps`（float fps）(偏移: 0x0)
- `float memory`（float memory）(偏移: 0x4)
- `bool collectEvent`（bool collect事件）(偏移: 0x8)

---

## AstarDebugger.PathTypeDebug（AstarDebugger.路径类型Debug）

### 字段 (3)

- `string name`（字符串 名称）(偏移: 0x0)
- `Func<int> getSize`（Func<int> get大小）(偏移: 0x4)
- `Func<int> getTotalCreated`（Func<int> getTotalCreated）(偏移: 0x8)

### 方法 (1)

- `void Print(StringBuilder text)`
  （void Print（字符串构建器 text））

---

## AstarMath（Astar数学）

### 方法 (5)

- `float MapTo(float startMin, float startMax, float targetMin, float targetMax, float value)`
  （float 映射To（float startMin, float startMax, float targetMin, float targetMax, float value））
- `string FormatBytesBinary(int bytes)`
  （string 格式化BytesBinary（int bytes））
- `int Bit(int a, int b)`
  （int Bit（int a, int b））
- `Color IntToColor(int i, float a)`
  （颜色 整数To颜色（int i, float a））
- `Color HSVToRGB(float h, float s, float v)`
  （颜色 HSV颜色ToRGB颜色（float h, float s, float v））

---

## AstarPath（Astar路径）

**继承**: VersionedMonoBehaviour（版本化MonoBehaviour）

### 字段 (60)

- `Version Version`（Version Version）(偏移: 0x0)
- `AstarPath.AstarDistribution Distribution`（AstarPath.AstarDistribution Distribution）(偏移: 0x4)
- `string Branch`（string Branch）(偏移: 0x8)
- `AstarData data`（Astar数据 data）(偏移: 0x10)
- `AstarPath active`（Astar路径 active）(偏移: 0xC)
- `bool showNavGraphs`（bool showNavGraphs）(偏移: 0x14)
- `bool showUnwalkableNodes`（bool showUnwalkableNodes）(偏移: 0x15)
- `GraphDebugMode debugMode`（GraphDebug模式 debug模式）(偏移: 0x18)
- `float debugFloor`（float debugFloor）(偏移: 0x1C)
- `float debugRoof`（float debugRoof）(偏移: 0x20)
- `bool manualDebugFloorRoof`（bool manualDebugFloorRoof）(偏移: 0x24)
- `bool showSearchTree`（bool show搜索Tree）(偏移: 0x25)
- `float unwalkableNodeDebugSize`（float unwalkable节点Debug大小）(偏移: 0x28)
- `PathLog logPathResults`（路径Log log路径Results）(偏移: 0x2C)
- `float maxNearestNodeDistance`（float maxNearest节点距离）(偏移: 0x30)
- `bool scanOnStartup`（bool scanOnStartup）(偏移: 0x34)
- `bool fullGetNearestSearch`（bool full获取Nearest搜索）(偏移: 0x35)
- `bool prioritizeGraphs`（bool prioritizeGraphs）(偏移: 0x36)
- `float prioritizeGraphsLimit`（float prioritizeGraphsLimit）(偏移: 0x38)
- `AstarColor colorSettings`（Astar颜色 colorSettings）(偏移: 0x3C)
- `string[] tagNames`（string[] tagNames）(偏移: 0x40)
- `Heuristic heuristic`（Heuristic heuristic）(偏移: 0x44)
- `float heuristicScale`（float heuristic缩放）(偏移: 0x48)
- `ThreadCount threadCount`（Thread数量 thread数量）(偏移: 0x4C)
- `float maxFrameTime`（float maxFrame时间）(偏移: 0x50)
- `bool batchGraphUpdates`（bool batchGraphUpdates）(偏移: 0x54)
- `float graphUpdateBatchingInterval`（float graph更新Batching间隔）(偏移: 0x58)
- `PathHandler debugPathData`（路径处理器 debug路径数据）(偏移: 0x60)
- `ushort debugPathID`（ushort debug路径ID）(偏移: 0x64)
- `string inGameDebugPath`（string in游戏Debug路径）(偏移: 0x68)
- `bool isScanningBacking`（bool isScanningBacking）(偏移: 0x6C)
- `Action OnAwakeSettings`（动作 OnAwakeSettings）(偏移: 0x10)
- `OnGraphDelegate OnGraphPreScan`（OnGraph委托 OnGraphPreScan）(偏移: 0x14)
- `OnGraphDelegate OnGraphPostScan`（OnGraph委托 OnGraphPostScan）(偏移: 0x18)
- `OnPathDelegate OnPathPreSearch`（On路径委托 On路径Pre搜索）(偏移: 0x1C)
- `OnPathDelegate OnPathPostSearch`（On路径委托 On路径Post搜索）(偏移: 0x20)
- `OnScanDelegate OnPreScan`（OnScan委托 OnPreScan）(偏移: 0x24)
- `OnScanDelegate OnPostScan`（OnScan委托 OnPostScan）(偏移: 0x28)
- `OnScanDelegate OnLatePostScan`（OnScan委托 On延迟PostScan）(偏移: 0x2C)
- `OnScanDelegate OnGraphsUpdated`（OnScan委托 OnGraphsUpdated）(偏移: 0x30)
- `Action On65KOverflow`（动作 On65KOverflow）(偏移: 0x34)
- `Action OnGraphsWillBeUpdated`（动作 OnGraphsWillBeUpdated）(偏移: 0x70)
- `Action OnGraphsWillBeUpdated2`（动作 OnGraphsWillBeUpdated2）(偏移: 0x74)
- `GraphUpdateProcessor graphUpdates`（Graph更新Processor graphUpdates）(偏移: 0x78)
- `HierarchicalGraph hierarchicalGraph`（HierarchicalGraph hierarchicalGraph）(偏移: 0x7C)
- `NavmeshUpdates navmeshUpdates`（NavmeshUpdates navmeshUpdates）(偏移: 0x80)
- `WorkItemProcessor workItems`（Work项目Processor workItems）(偏移: 0x84)
- `PathProcessor pathProcessor`（路径Processor pathProcessor）(偏移: 0x88)
- `bool graphUpdateRoutineRunning`（bool graph更新RoutineRunning）(偏移: 0x8C)
- `bool graphUpdatesWorkItemAdded`（bool graphUpdatesWork项目Added）(偏移: 0x8D)
- `float lastGraphUpdate`（float lastGraph更新）(偏移: 0x90)
- `PathProcessor.GraphUpdateLock workItemLock`（路径Processor.Graph更新Lock work项目Lock）(偏移: 0x94)
- `PathReturnQueue pathReturnQueue`（路径Return队列 pathReturn队列）(偏移: 0x9C)
- `EuclideanEmbedding euclideanEmbedding`（EuclideanEmbedding euclideanEmbedding）(偏移: 0xA0)
- `bool showGraphs`（bool showGraphs）(偏移: 0xA4)
- `ushort nextFreePathID`（ushort nextFree路径ID）(偏移: 0xA6)
- `RetainedGizmos gizmos`（RetainedGizmos gizmos）(偏移: 0xA8)
- `int lastRenderedFrame`（int lastRenderedFrame）(偏移: 0xAC)
- `int waitForPathDepth`（int waitFor路径深度）(偏移: 0x38)
- `NNConstraint NNConstraintNone`（NNConstraint NNConstraint无）(偏移: 0x3C)

### 方法 (77)

- `Type[] get_graphTypes()`
  （Type[] get_graphTypes（））
- `AstarData get_astarData()`
  （Astar数据 get_astar数据（））
- `NavGraph[] get_graphs()`
  （NavGraph[] get_graphs（））
- `float get_maxNearestNodeDistanceSqr()`
  （float get_maxNearest节点距离Sqr（））
- `bool get_limitGraphUpdates()`
  （bool get_limitGraphUpdates（））
- `void set_limitGraphUpdates(bool value)`
  （void set_limitGraphUpdates（bool value））
- `float get_maxGraphUpdateFreq()`
  （float get_maxGraph更新Freq（））
- `void set_maxGraphUpdateFreq(float value)`
  （void set_maxGraph更新Freq（float value））
- `float get_lastScanTime()`
  （float get_lastScan时间（））
- `void set_lastScanTime(float value)`
  （void set_lastScan时间（float value））
- `bool get_isScanning()`
  （bool get_isScanning（））
- `void set_isScanning(bool value)`
  （void set_isScanning（bool value））
- `int get_NumParallelThreads()`
  （int get_NumParallelThreads（））
- `bool get_IsUsingMultithreading()`
  （bool get_是否UsingMultithreading（））
- `bool get_IsAnyGraphUpdatesQueued()`
  （bool get_是否任意GraphUpdatesQueued（））
- `bool get_IsAnyGraphUpdateQueued()`
  （bool get_是否任意Graph更新Queued（））
- `bool get_IsAnyGraphUpdateInProgress()`
  （bool get_是否任意Graph更新InProgress（））
- `bool get_IsAnyWorkItemInProgress()`
  （bool get_是否任意Work项目InProgress（））
- `bool get_IsInsideWorkItem()`
  （bool get_是否InsideWork项目（））
- `string[] GetTagNames()`
  （string[] 获取标签Names（））
- `void FindAstarPath()`
  （void 查找Astar路径（））
- `string[] FindTagNames()`
  （string[] 查找标签Names（））
- `ushort GetNextPathID()`
  （ushort 获取下一个路径ID（））
- `void RecalculateDebugLimits()`
  （void RecalculateDebugLimits（））
- `void OnDrawGizmos()`
  （void 绘制辅助线时（））
- `void OnGUI()`
  （void GUI时（））
- `void LogPathResults(Path path)`
  （void Log路径Results（路径 path））
- `void Update()`
  （void 更新（））
- `void PerformBlockingActions(bool force = False)`
  （void 执行BlockingActions（bool force = False））
- `void QueueWorkItemFloodFill()`
  （void 队列Work项目FloodFill（））
- `void EnsureValidFloodFill()`
  （void EnsureValidFloodFill（））
- `void AddWorkItem(Action callback)`
  （void 添加Work项目（动作 callback））
- `void AddWorkItem(Action<IWorkItemContext> callback)`
  （void 添加Work项目（Action<IWork项目Context> callback））
- `void AddWorkItem(AstarWorkItem item)`
  （void 添加Work项目（AstarWork项目 item））
- `void QueueGraphUpdates()`
  （void 队列GraphUpdates（））
- `IEnumerator DelayedGraphUpdate()`
  （IEnumerator DelayedGraph更新（））
- `void UpdateGraphs(Bounds bounds, float delay)`
  （void 更新Graphs（Bounds bounds, float delay））
- `void UpdateGraphs(GraphUpdateObject ob, float delay)`
  （void 更新Graphs（Graph更新对象 ob, float delay））
- `IEnumerator UpdateGraphsInternal(GraphUpdateObject ob, float delay)`
  （IEnumerator 更新Graphs内部的（Graph更新对象 ob, float delay））
- `void UpdateGraphs(Bounds bounds)`
  （void 更新Graphs（Bounds bounds））
- `void UpdateGraphs(GraphUpdateObject ob)`
  （void 更新Graphs（Graph更新对象 ob））
- `void FlushGraphUpdates()`
  （void FlushGraphUpdates（））
- `void FlushWorkItems()`
  （void FlushWorkItems（））
- `void FlushWorkItems(bool unblockOnComplete, bool block)`
  （void FlushWorkItems（bool unblockOnComplete, bool block））
- `void FlushThreadSafeCallbacks()`
  （void FlushThreadSafeCallbacks（））
- `int CalculateThreadCount(ThreadCount count)`
  （int 计算Thread数量（Thread数量 count））
- `void Awake()`
  （void 唤醒（））
- `void InitializePathProcessor()`
  （void 初始化路径Processor（））
- `void VerifyIntegrity()`
  （void VerifyIntegrity（））
- `void ConfigureReferencesInternal()`
  （void ConfigureReferences内部的（））
- `void InitializeProfiler()`
  （void 初始化Profiler（））
- `void InitializeAstarData()`
  （void 初始化Astar数据（））
- `void OnDisable()`
  （void 禁用时（））
- `void OnDestroy()`
  （void 销毁时（））
- `void FloodFill(GraphNode seed)`
  （void FloodFill（Graph节点 seed））
- `void FloodFill(GraphNode seed, uint area)`
  （void FloodFill（Graph节点 seed, uint area））
- `void FloodFill()`
  （void FloodFill（））
- `int GetNewNodeIndex()`
  （int 获取新的节点索引（））
- `void InitializeNode(GraphNode node)`
  （void 初始化节点（Graph节点 node））
- `void DestroyNode(GraphNode node)`
  （void 销毁节点（Graph节点 node））
- `void BlockUntilPathQueueBlocked()`
  （void BlockUntil路径队列Blocked（））
- `PathProcessor.GraphUpdateLock PausePathfinding()`
  （路径Processor.Graph更新Lock 暂停Pathfinding（））
- `PathProcessor.GraphUpdateLock PausePathfindingSoon()`
  （路径Processor.Graph更新Lock 暂停PathfindingSoon（））
- `void Scan(NavGraph graphToScan)`
  （void Scan（NavGraph graphToScan））
- `void Scan(NavGraph[] graphsToScan)`
  （void Scan（NavGraph[] graphsToScan））
- `IEnumerable<Progress> ScanAsync(NavGraph graphToScan)`
  （IEnumerable<Progress> Scan异步（NavGraph graphToScan））
- `IEnumerable<Progress> ScanAsync(NavGraph[] graphsToScan)`
  （IEnumerable<Progress> Scan异步（NavGraph[] graphsToScan））
- `IEnumerable<Progress> ScanGraph(NavGraph graph)`
  （IEnumerable<Progress> ScanGraph（NavGraph graph））
- `void WaitForPath(Path path)`
  （void WaitFor路径（路径 path））
- `void BlockUntilCalculated(Path path)`
  （void BlockUntilCalculated（路径 path））
- `void RegisterSafeUpdate(Action callback)`
  （void RegisterSafe更新（动作 callback））
- `void StartPath(Path path, bool pushToFront = False)`
  （void 开始路径（路径 path, bool pushToFront = False））
- `void OnApplicationQuit()`
  （void 应用退出时（））
- `NNInfo GetNearest(Vector3 position)`
  （NN信息 获取Nearest（三维向量 position））
- `NNInfo GetNearest(Vector3 position, NNConstraint constraint)`
  （NN信息 获取Nearest（三维向量 position, NNConstraint constraint））
- `NNInfo GetNearest(Vector3 position, NNConstraint constraint, GraphNode hint)`
  （NN信息 获取Nearest（三维向量 position, NNConstraint constraint, Graph节点 hint））
- `GraphNode GetNearest(Ray ray)`
  （Graph节点 获取Nearest（Ray ray））

---

## AstarPath.AstarDistribution（AstarPath.AstarDistribution）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AstarProfiler（AstarProfiler）

### 字段 (3)

- `DateTime startTime`（Date时间 start时间）(偏移: 0x8)
- `AstarProfiler.ProfilePoint[] fastProfiles`（AstarProfiler.ProfilePoint[] fastProfiles）(偏移: 0x10)
- `string[] fastProfileNames`（string[] fastProfileNames）(偏移: 0x14)

### 方法 (9)

- `void InitializeFastProfile(string[] profileNames)`
  （void 初始化FastProfile（string[] profileNames））
- `void StartFastProfile(int tag)`
  （void 开始FastProfile（int tag））
- `void EndFastProfile(int tag)`
  （void 结束FastProfile（int tag））
- `void EndProfile()`
  （void 结束Profile（））
- `void StartProfile(string tag)`
  （void 开始Profile（string tag））
- `void EndProfile(string tag)`
  （void 结束Profile（string tag））
- `void Reset()`
  （void 重置（））
- `void PrintFastResults()`
  （void PrintFastResults（））
- `void PrintResults()`
  （void PrintResults（））

---

## AstarProfiler.ProfilePoint（AstarProfiler.ProfilePoint）

### 字段 (4)

- `Stopwatch watch`（Stopwatch watch）(偏移: 0x8)
- `int totalCalls`（int totalCalls）(偏移: 0xC)
- `long tmpBytes`（long tmpBytes）(偏移: 0x10)
- `long totalBytes`（long totalBytes）(偏移: 0x18)

---

## AstarSerializer（AstarSerializer）

### 字段 (13)

- `AstarData data`（Astar数据 data）(偏移: 0x8)
- `ZipFile zip`（Zip文件 zip）(偏移: 0xC)
- `MemoryStream zipStream`（Memory流 zip流）(偏移: 0x10)
- `GraphMeta meta`（GraphMeta meta）(偏移: 0x14)
- `SerializeSettings settings`（SerializeSettings settings）(偏移: 0x18)
- `NavGraph[] graphs`（NavGraph[] graphs）(偏移: 0x1C)
- `int graphIndexOffset`（int graph索引Offset）(偏移: 0x24)
- `uint checksum`（uint checksum）(偏移: 0x28)
- `UTF8Encoding encoding`（UTF8Encoding encoding）(偏移: 0x2C)
- `StringBuilder _stringBuilder`（字符串构建器 _string构建器）(偏移: 0x0)
- `Version V3_8_3`（Version V3_8_3）(偏移: 0x4)
- `Version V3_9_0`（Version V3_9_0）(偏移: 0x8)
- `Version V4_1_0`（Version V4_1_0）(偏移: 0xC)

### 方法 (38)

- `StringBuilder GetStringBuilder()`
  （字符串构建器 获取字符串构建器（））
- `void SetGraphIndexOffset(int offset)`
  （void 集合Graph索引Offset（int offset））
- `void AddChecksum(byte[] bytes)`
  （void 添加Checksum（byte[] bytes））
- `void AddEntry(string name, byte[] bytes)`
  （void 添加Entry（string name, byte[] bytes））
- `uint GetChecksum()`
  （uint 获取Checksum（））
- `void OpenSerialize()`
  （void 打开Serialize（））
- `byte[] CloseSerialize()`
  （byte[] 关闭Serialize（））
- `void SerializeGraphs(NavGraph[] _graphs)`
  （void SerializeGraphs（NavGraph[] _graphs））
- `byte[] SerializeMeta()`
  （byte[] SerializeMeta（））
- `byte[] Serialize(NavGraph graph)`
  （byte[] Serialize（NavGraph graph））
- `void SerializeNodes()`
  （void SerializeNodes（））
- `int GetMaxNodeIndexInAllGraphs(NavGraph[] graphs)`
  （int 获取最大节点索引In所有Graphs（NavGraph[] graphs））
- `byte[] SerializeNodeIndices(NavGraph[] graphs)`
  （byte[] Serialize节点Indices（NavGraph[] graphs））
- `byte[] SerializeGraphExtraInfo(NavGraph graph)`
  （byte[] SerializeGraph额外的信息（NavGraph graph））
- `byte[] SerializeGraphNodeReferences(NavGraph graph)`
  （byte[] SerializeGraph节点References（NavGraph graph））
- `void SerializeExtraInfo()`
  （void Serialize额外的信息（））
- `byte[] SerializeNodeLinks()`
  （byte[] Serialize节点Links（））
- `ZipEntry GetEntry(string name)`
  （ZipEntry 获取Entry（string name））
- `bool ContainsEntry(string name)`
  （bool ContainsEntry（string name））
- `bool OpenDeserialize(byte[] bytes)`
  （bool 打开Deserialize（byte[] bytes））
- `Version FullyDefinedVersion(Version v)`
  （Version FullyDefinedVersion（Version v））
- `void CloseDeserialize()`
  （void 关闭Deserialize（））
- `NavGraph DeserializeGraph(int zipIndex, int graphIndex)`
  （NavGraph DeserializeGraph（int zipIndex, int graphIndex））
- `NavGraph[] DeserializeGraphs()`
  （NavGraph[] DeserializeGraphs（））
- `bool DeserializeExtraInfo(NavGraph graph)`
  （bool Deserialize额外的信息（NavGraph graph））
- `bool AnyDestroyedNodesInGraphs()`
  （bool 任意DestroyedNodesInGraphs（））
- `GraphNode[] DeserializeNodeReferenceMap()`
  （GraphNode[] Deserialize节点引用映射（））
- `void DeserializeNodeReferences(NavGraph graph, GraphNode[] int2Node)`
  （void Deserialize节点References（NavGraph graph, GraphNode[] int2Node））
- `void DeserializeExtraInfo()`
  （void Deserialize额外的信息（））
- `void DeserializeNodeLinks(GraphNode[] int2Node)`
  （void Deserialize节点Links（GraphNode[] int2Node））
- `void PostDeserialization()`
  （void PostDeserialization（））
- `void DeserializeEditorSettingsCompatibility()`
  （void DeserializeEditorSettingsCompatibility（））
- `BinaryReader GetBinaryReader(ZipEntry entry)`
  （Binary读取器 获取Binary读取器（ZipEntry entry））
- `string GetString(ZipEntry entry)`
  （string 获取字符串（ZipEntry entry））
- `GraphMeta DeserializeMeta(ZipEntry entry)`
  （GraphMeta DeserializeMeta（ZipEntry entry））
- `GraphMeta DeserializeBinaryMeta(ZipEntry entry)`
  （GraphMeta DeserializeBinaryMeta（ZipEntry entry））
- `void SaveToFile(string path, byte[] data)`
  （void 保存To文件（string path, byte[] data））
- `byte[] LoadFromFile(string path)`
  （byte[] 加载From文件（string path））

---

## AstarSmoothFollow2（AstarSmoothFollow2）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (8)

- `Transform target`（变换 目标）(偏移: 0xC)
- `float distance`（浮点数 距离）(偏移: 0x10)
- `float height`（浮点数 高度）(偏移: 0x14)
- `float damping`（float damping）(偏移: 0x18)
- `bool smoothRotation`（bool smoothRotation）(偏移: 0x1C)
- `bool followBehind`（bool followBehind）(偏移: 0x1D)
- `float rotationDamping`（float rotationDamping）(偏移: 0x20)
- `bool staticOffset`（bool staticOffset）(偏移: 0x24)

### 方法 (1)

- `void LateUpdate()`
  （void 延迟更新（））

---

## AstarSplines（AstarSplines）

### 方法 (4)

- `Vector3 CatmullRom(Vector3 previous, Vector3 start, Vector3 end, Vector3 next, float elapsedTime)`
  （三维向量 CatmullRom（三维向量 previous, 三维向量 start, 三维向量 end, 三维向量 next, float elapsedTime））
- `Vector3 CubicBezier(Vector3 p0, Vector3 p1, Vector3 p2, Vector3 p3, float t)`
  （三维向量 CubicBezier（三维向量 p0, 三维向量 p1, 三维向量 p2, 三维向量 p3, float t））
- `Vector3 CubicBezierDerivative(Vector3 p0, Vector3 p1, Vector3 p2, Vector3 p3, float t)`
  （三维向量 CubicBezierDerivative（三维向量 p0, 三维向量 p1, 三维向量 p2, 三维向量 p3, float t））
- `Vector3 CubicBezierSecondDerivative(Vector3 p0, Vector3 p1, Vector3 p2, Vector3 p3, float t)`
  （三维向量 CubicBezierSecondDerivative（三维向量 p0, 三维向量 p1, 三维向量 p2, 三维向量 p3, float t））

---

## AstarWorkItem（AstarWork项目）

### 字段 (2)

- `Action init`（动作 init）(偏移: 0x0)
- `Action<IWorkItemContext> initWithContext`（Action<IWork项目Context> initWithContext）(偏移: 0x4)

---

## AsymmetricAlgorithm（AsymmetricAlgorithm）

**继承**: IDisposable（可释放接口）

### 字段 (2)

- `int KeySizeValue`（int 键大小值）(偏移: 0x8)
- `KeySizes[] LegalKeySizesValue`（键Sizes[] Legal键Sizes值）(偏移: 0xC)

### 方法 (6)

- `void Dispose()`
  （void 释放（））
- `void Clear()`
  （void 清除（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `int get_KeySize()`
  （整数 获取_键大小（））
- `void set_KeySize(int value)`
  （void 设置_键大小（整数 value））
- `string ToXmlString(bool includePrivateParameters)`
  （字符串 转XML字符串（布尔值 包含私有参数））

---

## AsyncCallback（异步回调）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(IAsyncResult ar)`
  （void Invoke（I异步Result ar））
- `IAsyncResult BeginInvoke(IAsyncResult ar, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（I异步Result ar, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## AsyncCausalityStatus（异步CausalityStatus）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AsyncCausalityTracer（异步CausalityTracer）

### 方法 (6)

- `bool get_LoggingOn()`
  （bool get_LoggingOn（））
- `void TraceOperationCreation(CausalityTraceLevel traceLevel, int taskId, string operationName, ulong relatedContext)`
  （void TraceOperationCreation（CausalityTrace等级 traceLevel, int taskId, string operationName, ulong relatedContext））
- `void TraceOperationCompletion(CausalityTraceLevel traceLevel, int taskId, AsyncCausalityStatus status)`
  （void TraceOperationCompletion（CausalityTrace等级 traceLevel, int taskId, 异步CausalityStatus status））
- `void TraceOperationRelation(CausalityTraceLevel traceLevel, int taskId, CausalityRelation relation)`
  （void TraceOperationRelation（CausalityTrace等级 traceLevel, int taskId, CausalityRelation relation））
- `void TraceSynchronousWorkStart(CausalityTraceLevel traceLevel, int taskId, CausalitySynchronousWork work)`
  （void TraceSynchronousWork开始（CausalityTrace等级 traceLevel, int taskId, CausalitySynchronousWork work））
- `void TraceSynchronousWorkCompletion(CausalityTraceLevel traceLevel, CausalitySynchronousWork work)`
  （void TraceSynchronousWorkCompletion（CausalityTrace等级 traceLevel, CausalitySynchronousWork work））

---

## AsyncMethodBuilderCore（异步Method构建器Core）

### 字段 (2)

- `IAsyncStateMachine m_stateMachine`（I异步状态Machine m_stateMachine）(偏移: 0x0)
- `Action m_defaultContextAction`（动作 m_defaultContext动作）(偏移: 0x4)

### 方法 (7)

- `void SetStateMachine(IAsyncStateMachine stateMachine)`
  （void 集合状态Machine（I异步状态Machine stateMachine））
- `Action GetCompletionAction(Task taskForTracing, ref AsyncMethodBuilderCore.MoveNextRunner runnerToInitialize)`
  （动作 获取Completion动作（Task taskForTracing, ref AsyncMethodBuilderCore.MoveNextRunner runnerToInitialize））
- `Action OutputAsyncCausalityEvents(Task innerTask, Action continuation)`
  （动作 Output异步CausalityEvents（Task innerTask, 动作 continuation））
- `void PostBoxInitialization(IAsyncStateMachine stateMachine, AsyncMethodBuilderCore.MoveNextRunner runner, Task builtTask)`
  （void PostBoxInitialization（I异步状态Machine stateMachine, 异步Method构建器Core.移动下一个Runner runner, Task builtTask））
- `void ThrowAsync(Exception exception, SynchronizationContext targetContext)`
  （void 投掷异步（Exception exception, SynchronizationContext targetContext））
- `Action CreateContinuationWrapper(Action continuation, Action invokeAction, Task innerTask)`
  （动作 创建Continuation包装器（动作 continuation, 动作 invokeAction, Task innerTask））
- `Task TryGetContinuationTask(Action action)`
  （Task Try获取ContinuationTask（动作 action））

---

## AsyncMethodBuilderCore.ContinuationWrapper（异步Method构建器Core.Continuation包装器）

### 字段 (3)

- `Action m_continuation`（动作 m_continuation）(偏移: 0x8)
- `Action m_invokeAction`（动作 m_invoke动作）(偏移: 0xC)
- `Task m_innerTask`（Task m_innerTask）(偏移: 0x10)

### 方法 (1)

- `void Invoke()`
  （void 调用（））

---

## AsyncMethodBuilderCore.MoveNextRunner（异步Method构建器Core.移动下一个Runner）

### 字段 (3)

- `ExecutionContext m_context`（ExecutionContext m_context）(偏移: 0x8)
- `IAsyncStateMachine m_stateMachine`（I异步状态Machine m_stateMachine）(偏移: 0xC)
- `ContextCallback s_invokeMoveNext`（Context回调 s_invoke移动下一个）(偏移: 0x0)

### 方法 (2)

- `void Run()`
  （void 运行（））
- `void InvokeMoveNext(object stateMachine)`
  （void Invoke移动下一个（object stateMachine））

---

## AsyncOperation（异步Operation）

**继承**: YieldInstruction（YieldInstruction）

### 字段 (2)

- `IntPtr m_Ptr`（整数指针 m_指针）(偏移: 0x8)
- `Action<AsyncOperation> m_completeCallback`（Action<异步Operation> m_complete回调）(偏移: 0xC)

### 方法 (5)

- `void InternalDestroy(IntPtr ptr)`
  （void 内部的销毁（整数Ptr ptr））
- `bool get_isDone()`
  （bool get_isDone（））
- `float get_progress()`
  （float get_progress（））
- `void Finalize()`
  （void 终结（））
- `void InvokeCompletionEvent()`
  （void InvokeCompletion事件（））

---

