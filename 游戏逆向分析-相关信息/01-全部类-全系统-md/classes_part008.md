# 游戏类定义 (Part 8/21)

共 200 个类 (总序号 1401 - 1600)

---

## Gradient（Gradient）

**继承**: IEquatable<Gradient>（IEquatable<Gradient>）

### 字段 (1)

- `IntPtr m_Ptr`（整数指针 m_指针）(偏移: 0x8)

### 方法 (10)

- `IntPtr Init()`
  （整数Ptr 初始化（））
- `void Cleanup()`
  （void 清理（））
- `bool Internal_Equals(IntPtr other)`
  （bool Internal_Equals（整数Ptr other））
- `void Finalize()`
  （void 终结（））
- `Color Evaluate(float time)`
  （颜色 Evaluate（float time））
- `GradientColorKey[] get_colorKeys()`
  （Gradient颜色Key[] get_colorKeys（））
- `bool Equals(object o)`
  （布尔值 等于（对象 o））
- `bool Equals(Gradient other)`
  （bool Equals（Gradient other））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `void Evaluate_Injected(float time, out Color ret)`
  （void Evaluate_Injected（float time, out Color ret））

---

## GradientColorKey（Gradient颜色键）

### 字段 (2)

- `Color color`（颜色 color）(偏移: 0x0)
- `float time`（float time）(偏移: 0x10)

---

## GraphCollision（GraphCollision）

### 字段 (19)

- `ColliderType type`（碰撞器类型 type）(偏移: 0x8)
- `float diameter`（float diameter）(偏移: 0xC)
- `float height`（浮点数 高度）(偏移: 0x10)
- `float collisionOffset`（float collisionOffset）(偏移: 0x14)
- `RayDirection rayDirection`（Ray方向 ray方向）(偏移: 0x18)
- `LayerMask mask`（层掩码 mask）(偏移: 0x1C)
- `LayerMask heightMask`（层掩码 height掩码）(偏移: 0x20)
- `float fromHeight`（float from高度）(偏移: 0x24)
- `bool thickRaycast`（bool thickRaycast）(偏移: 0x28)
- `float thickRaycastDiameter`（float thickRaycastDiameter）(偏移: 0x2C)
- `bool unwalkableWhenNoGround`（bool unwalkableWhenNo地面）(偏移: 0x30)
- `bool use2D`（bool use2D）(偏移: 0x0)
- `bool collisionCheck`（bool collision检查）(偏移: 0x0)
- `bool heightCheck`（bool height检查）(偏移: 0x0)
- `Vector3 up`（三维向量 up）(偏移: 0x0)
- `Vector3 upheight`（三维向量 upheight）(偏移: 0x40)
- `float finalRadius`（float finalRadius）(偏移: 0x4C)
- `float finalRaycastRadius`（float finalRaycastRadius）(偏移: 0x50)
- `RaycastHit[] hitBuffer`（RaycastHit[] hit缓冲区）(偏移: 0x54)

### 方法 (6)

- `void Initialize(GraphTransform transform, float scale)`
  （void 初始化（Graph变换 transform, float scale））
- `bool Check(Vector3 position)`
  （bool 检查（三维向量 position））
- `Vector3 CheckHeight(Vector3 position)`
  （三维向量 检查高度（三维向量 position））
- `Vector3 CheckHeight(Vector3 position, out RaycastHit hit, out bool walkable)`
  （三维向量 检查高度（三维向量 position, out RaycastHit hit, out bool walkable））
- `RaycastHit[] CheckHeightAll(Vector3 position, out int numHits)`
  （RaycastHit[] 检查高度所有（三维向量 position, out int numHits））
- `void DeserializeSettingsCompatibility(GraphSerializationContext ctx)`
  （void 反序列化设置兼容性（图序列化上下文 ctx））

---

## GraphDebugMode（GraphDebug模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## GraphEditorBase（GraphEditor基础）

### 字段 (1)

- `NavGraph target`（NavGraph target）(偏移: 0x8)

---

## GraphGizmoHelper（GraphGizmo辅助器）

**继承**: IAstarPooledObject, IDisposable（IAstarPooled对象, IDisposable）

### 字段 (10)

- `RetainedGizmos gizmos`（RetainedGizmos gizmos）(偏移: 0x18)
- `PathHandler debugData`（路径处理器 debug数据）(偏移: 0x1C)
- `ushort debugPathID`（ushort debug路径ID）(偏移: 0x20)
- `GraphDebugMode debugMode`（GraphDebug模式 debug模式）(偏移: 0x24)
- `bool showSearchTree`（bool show搜索Tree）(偏移: 0x28)
- `float debugFloor`（float debugFloor）(偏移: 0x2C)
- `float debugRoof`（float debugRoof）(偏移: 0x30)
- `Vector3 drawConnectionStart`（三维向量 draw连接开始）(偏移: 0x38)
- `Color drawConnectionColor`（颜色 draw连接颜色）(偏移: 0x44)
- `Action<GraphNode> drawConnection`（Action<GraphNode> draw连接）(偏移: 0x54)

### 方法 (14)

- `RetainedGizmos.Hasher get_hasher()`
  （RetainedGizmos.Hasher get_hasher（））
- `void set_hasher(RetainedGizmos.Hasher value)`
  （void set_hasher（RetainedGizmos.Hasher value））
- `RetainedGizmos.Builder get_builder()`
  （RetainedGizmos.构建器 get_builder（））
- `void set_builder(RetainedGizmos.Builder value)`
  （void set_builder（RetainedGizmos.构建器 value））
- `void Init(AstarPath active, RetainedGizmos.Hasher hasher, RetainedGizmos gizmos)`
  （void 初始化（Astar路径 active, RetainedGizmos.Hasher hasher, RetainedGizmos gizmos））
- `void OnEnterPool()`
  （void 进入池时（））
- `void DrawConnections(GraphNode node)`
  （void DrawConnections（Graph节点 node））
- `void DrawConnection(GraphNode other)`
  （void Draw连接（Graph节点 other））
- `Color NodeColor(GraphNode node)`
  （颜色 节点颜色（Graph节点 node））
- `bool InSearchTree(GraphNode node, PathHandler handler, ushort pathID)`
  （bool In搜索Tree（Graph节点 node, 路径处理器 handler, ushort pathID））
- `void DrawWireTriangle(Vector3 a, Vector3 b, Vector3 c, Color color)`
  （void DrawWireTriangle（三维向量 a, 三维向量 b, 三维向量 c, 颜色 color））
- `void DrawTriangles(Vector3[] vertices, Color[] colors, int numTriangles)`
  （void DrawTriangles（Vector3[] vertices, Color[] colors, int numTriangles））
- `void DrawWireTriangles(Vector3[] vertices, Color[] colors, int numTriangles)`
  （void DrawWireTriangles（Vector3[] vertices, Color[] colors, int numTriangles））
- `void Submit()`
  （void Submit（））

---

## GraphHitInfo（Graph命中信息）

### 字段 (5)

- `Vector3 origin`（三维向量 origin）(偏移: 0x0)
- `Vector3 point`（三维向量 point）(偏移: 0xC)
- `GraphNode node`（图节点 node）(偏移: 0x18)
- `Vector3 tangentOrigin`（三维向量 tangentOrigin）(偏移: 0x1C)
- `Vector3 tangent`（三维向量 tangent）(偏移: 0x28)

### 方法 (1)

- `float get_distance()`
  （浮点数 获取_距离（））

---

## GraphMask（Graph掩码）

### 字段 (1)

- `int value`（整数 value）(偏移: 0x0)

### 方法 (10)

- `GraphMask get_everything()`
  （Graph掩码 get_everything（））
- `int op_Implicit(GraphMask mask)`
  （int op_Implicit（Graph掩码 mask））
- `GraphMask op_Implicit(int mask)`
  （Graph掩码 op_Implicit（int mask））
- `GraphMask op_BitwiseAnd(GraphMask lhs, GraphMask rhs)`
  （Graph掩码 op_BitwiseAnd（Graph掩码 lhs, Graph掩码 rhs））
- `GraphMask op_BitwiseOr(GraphMask lhs, GraphMask rhs)`
  （Graph掩码 op_BitwiseOr（Graph掩码 lhs, Graph掩码 rhs））
- `GraphMask op_OnesComplement(GraphMask lhs)`
  （Graph掩码 op_OnesComplement（Graph掩码 lhs））
- `bool Contains(int graphIndex)`
  （bool Contains（int graphIndex））
- `GraphMask FromGraph(NavGraph graph)`
  （Graph掩码 FromGraph（NavGraph graph））
- `string ToString()`
  （字符串 转字符串（））
- `GraphMask FromGraphName(string graphName)`
  （Graph掩码 FromGraph名称（string graphName））

---

## GraphMeta（GraphMeta）

### 字段 (4)

- `Version version`（Version version）(偏移: 0x8)
- `int graphs`（int graphs）(偏移: 0xC)
- `List<string> guids`（List<string> guids）(偏移: 0x10)
- `List<string> typeNames`（List<string> typeNames）(偏移: 0x14)

### 方法 (1)

- `Type GetGraphType(int index)`
  （类型 获取Graph类型（int index））

---

## GraphModifier（图修改器）

**继承**: VersionedMonoBehaviour（版本化MonoBehaviour）

### 字段 (4)

- `GraphModifier root`（Graph修改器 root）(偏移: 0x0)
- `GraphModifier prev`（Graph修改器 prev）(偏移: 0x10)
- `GraphModifier next`（Graph修改器 next）(偏移: 0x14)
- `ulong uniqueID`（ulong uniqueID）(偏移: 0x18)

### 方法 (16)

- `void FindAllModifiers()`
  （void 查找所有Modifiers（））
- `void TriggerEvent(GraphModifier.EventType type)`
  （void 触发器事件（GraphModifier.事件类型 type））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `void Awake()`
  （void 唤醒（））
- `void ConfigureUniqueID()`
  （void ConfigureUniqueID（））
- `void AddToLinkedList()`
  （void 添加ToLinked列表（））
- `void RemoveFromLinkedList()`
  （void 移除FromLinked列表（））
- `void OnDestroy()`
  （void 销毁时（））
- `void OnPostScan()`
  （void 扫描后（））
- `void OnPreScan()`
  （void OnPreScan（））
- `void OnLatePostScan()`
  （void 延迟后扫描时（））
- `void OnPostCacheLoad()`
  （void OnPost缓存加载（））
- `void OnGraphsPreUpdate()`
  （void OnGraphsPre更新（））
- `void OnGraphsPostUpdate()`
  （void 图后更新时（））
- `void Reset()`
  （void 重置（））

---

## GraphModifier.EventType（GraphModifier.事件类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## GraphNode（Graph节点）

### 字段 (4)

- `int nodeIndex`（int node索引）(偏移: 0x8)
- `uint flags`（uint flags）(偏移: 0xC)
- `uint penalty`（uint penalty）(偏移: 0x10)
- `Int3 position`（Int3 position）(偏移: 0x14)

### 方法 (35)

- `NavGraph get_Graph()`
  （NavGraph get_Graph（））
- `void Destroy()`
  （void 销毁（））
- `bool get_Destroyed()`
  （bool get_Destroyed（））
- `int get_NodeIndex()`
  （int get_节点索引（））
- `void set_NodeIndex(int value)`
  （void set_节点索引（int value））
- `bool get_TemporaryFlag1()`
  （bool get_临时的Flag1（））
- `void set_TemporaryFlag1(bool value)`
  （void set_临时的Flag1（bool value））
- `bool get_TemporaryFlag2()`
  （bool get_临时的Flag2（））
- `void set_TemporaryFlag2(bool value)`
  （void set_临时的Flag2（bool value））
- `uint get_Flags()`
  （uint get_Flags（））
- `void set_Flags(uint value)`
  （void set_Flags（uint value））
- `uint get_Penalty()`
  （uint get_惩罚（））
- `void set_Penalty(uint value)`
  （void set_惩罚（uint value））
- `bool get_Walkable()`
  （bool get_Walkable（））
- `void set_Walkable(bool value)`
  （void set_Walkable（bool value））
- `int get_HierarchicalNodeIndex()`
  （int get_Hierarchical节点索引（））
- `void set_HierarchicalNodeIndex(int value)`
  （void set_Hierarchical节点索引（int value））
- `bool get_IsHierarchicalNodeDirty()`
  （bool get_是否Hierarchical节点Dirty（））
- `void set_IsHierarchicalNodeDirty(bool value)`
  （void set_是否Hierarchical节点Dirty（bool value））
- `uint get_Area()`
  （uint get_Area（））
- `uint get_GraphIndex()`
  （uint get_Graph索引（））
- `void set_GraphIndex(uint value)`
  （void set_Graph索引（uint value））
- `uint get_Tag()`
  （uint get_标签（））
- `void set_Tag(uint value)`
  （void set_标签（uint value））
- `void SetConnectivityDirty()`
  （void 集合ConnectivityDirty（））
- `void UpdateRecursiveG(Path path, PathNode pathNode, PathHandler handler)`
  （void 更新递归G（路径 path, 路径节点 pathNode, 路径处理器 handler））
- `bool ContainsConnection(GraphNode node)`
  （bool Contains连接（Graph节点 node））
- `bool GetPortal(GraphNode other, List<Vector3> left, List<Vector3> right, bool backwards)`
  （bool 获取Portal（Graph节点 other, List<Vector3> left, List<Vector3> right, bool backwards））
- `float SurfaceArea()`
  （float SurfaceArea（））
- `Vector3 RandomPointOnSurface()`
  （三维向量 随机PointOnSurface（））
- `int GetGizmoHashCode()`
  （整数 获取辅助线哈希码（））
- `void SerializeNode(GraphSerializationContext ctx)`
  （void 序列化节点（图序列化上下文 ctx））
- `void DeserializeNode(GraphSerializationContext ctx)`
  （void 反序列化节点（图序列化上下文 ctx））
- `void SerializeReferences(GraphSerializationContext ctx)`
  （void 序列化引用（图序列化上下文 ctx））
- `void DeserializeReferences(GraphSerializationContext ctx)`
  （void 反序列化引用（图序列化上下文 ctx））

---

## GraphSerializationContext（GraphSerializationContext）

### 字段 (5)

- `GraphNode[] id2NodeMapping`（GraphNode[] id2节点Mapping）(偏移: 0x8)
- `BinaryReader reader`（Binary读取器 reader）(偏移: 0xC)
- `BinaryWriter writer`（Binary写入器 writer）(偏移: 0x10)
- `uint graphIndex`（uint graph索引）(偏移: 0x14)
- `GraphMeta meta`（GraphMeta meta）(偏移: 0x18)

### 方法 (9)

- `void SerializeNodeReference(GraphNode node)`
  （void Serialize节点引用（Graph节点 node））
- `GraphNode DeserializeNodeReference()`
  （Graph节点 Deserialize节点引用（））
- `void SerializeVector3(Vector3 v)`
  （void Serialize三维向量（三维向量 v））
- `Vector3 DeserializeVector3()`
  （三维向量 Deserialize三维向量（））
- `void SerializeInt3(Int3 v)`
  （void SerializeInt3（Int3 v））
- `Int3 DeserializeInt3()`
  （Int3 DeserializeInt3（））
- `int DeserializeInt(int defaultValue)`
  （int Deserialize整数（int defaultValue））
- `float DeserializeFloat(float defaultValue)`
  （float Deserialize浮点数（float defaultValue））
- `Object DeserializeUnityObject()`
  （对象 DeserializeUnity引擎对象（））

---

## GraphTransform（Graph变换）

**继承**: IMovementPlane, ITransform（IMovementPlane, I变换）

### 字段 (12)

- `bool identity`（bool identity）(偏移: 0x8)
- `bool onlyTranslational`（bool onlyTranslational）(偏移: 0x9)
- `bool isXY`（bool isXY）(偏移: 0xA)
- `bool isXZ`（bool isXZ）(偏移: 0xB)
- `Matrix4x4 matrix`（Matrix4x4 matrix）(偏移: 0xC)
- `Matrix4x4 inverseMatrix`（Matrix4x4 inverse矩阵）(偏移: 0x4C)
- `Vector3 up`（三维向量 up）(偏移: 0x8C)
- `Vector3 translation`（三维向量 translation）(偏移: 0x98)
- `Int3 i3translation`（Int3 i3translation）(偏移: 0xA4)
- `Quaternion rotation`（四元数 旋转）(偏移: 0xB0)
- `Quaternion inverseRotation`（Quaternion inverseRotation）(偏移: 0xC0)
- `GraphTransform identityTransform`（Graph变换 identity变换）(偏移: 0x0)

### 方法 (13)

- `Vector3 WorldUpAtGraphPosition(Vector3 point)`
  （三维向量 世界的上AtGraphPosition（三维向量 point））
- `bool MatrixIsTranslational(Matrix4x4 matrix)`
  （bool 矩阵是否Translational（Matrix4x4 matrix））
- `Vector3 Transform(Vector3 point)`
  （三维向量 变换（三维向量 point））
- `Vector3 TransformVector(Vector3 point)`
  （三维向量 变换向量（三维向量 point））
- `void Transform(Int3[] arr)`
  （void 变换（Int3[] arr））
- `void Transform(Vector3[] arr)`
  （void 变换（Vector3[] arr））
- `Vector3 InverseTransform(Vector3 point)`
  （三维向量 Inverse变换（三维向量 point））
- `Int3 InverseTransform(Int3 point)`
  （Int3 Inverse变换（Int3 point））
- `void InverseTransform(Int3[] arr)`
  （void Inverse变换（Int3[] arr））
- `GraphTransform op_Multiply(GraphTransform lhs, Matrix4x4 rhs)`
  （Graph变换 op_Multiply（Graph变换 lhs, Matrix4x4 rhs））
- `GraphTransform op_Multiply(Matrix4x4 lhs, GraphTransform rhs)`
  （Graph变换 op_Multiply（Matrix4x4 lhs, Graph变换 rhs））
- `Bounds Transform(Bounds bounds)`
  （Bounds 变换（Bounds bounds））
- `Bounds InverseTransform(Bounds bounds)`
  （Bounds Inverse变换（Bounds bounds））

---

## GraphUpdateObject（Graph更新对象）

### 字段 (15)

- `Bounds bounds`（边界 bounds）(偏移: 0x8)
- `bool updatePhysics`（bool update物理）(偏移: 0x20)
- `bool resetPenaltyOnPhysics`（bool reset惩罚On物理）(偏移: 0x21)
- `bool updateErosion`（bool updateErosion）(偏移: 0x22)
- `NNConstraint nnConstraint`（NNConstraint nnConstraint）(偏移: 0x24)
- `int addPenalty`（int add惩罚）(偏移: 0x28)
- `bool modifyWalkability`（bool modifyWalkability）(偏移: 0x2C)
- `bool setWalkability`（bool setWalkability）(偏移: 0x2D)
- `bool modifyTag`（bool modify标签）(偏移: 0x2E)
- `int setTag`（int set标签）(偏移: 0x30)
- `bool trackChangedNodes`（bool trackChangedNodes）(偏移: 0x34)
- `List<GraphNode> changedNodes`（List<GraphNode> changedNodes）(偏移: 0x38)
- `List<uint> backupData`（List<uint> backup数据）(偏移: 0x3C)
- `List<Int3> backupPositionData`（List<Int3> backupPosition数据）(偏移: 0x40)
- `GraphUpdateShape shape`（Graph更新Shape shape）(偏移: 0x44)

### 方法 (4)

- `void set_requiresFloodFill(bool value)`
  （void set_requiresFloodFill（bool value））
- `void WillUpdateNode(GraphNode node)`
  （void Will更新节点（Graph节点 node））
- `void RevertFromBackup()`
  （void RevertFromBackup（））
- `void Apply(GraphNode node)`
  （void 应用（Graph节点 node））

---

## GraphUpdateProcessor（Graph更新Processor）

### 字段 (12)

- `Action OnGraphsUpdated`（动作 OnGraphsUpdated）(偏移: 0x8)
- `AstarPath astar`（Astar路径 astar）(偏移: 0xC)
- `Thread graphUpdateThread`（Thread graph更新Thread）(偏移: 0x10)
- `bool anyGraphUpdateInProgress`（bool anyGraph更新InProgress）(偏移: 0x14)
- `CustomSampler asyncUpdateProfilingSampler`（自定义的Sampler async更新ProfilingSampler）(偏移: 0x18)
- `Queue<GraphUpdateObject> graphUpdateQueue`（Queue<Graph更新Object> graph更新队列）(偏移: 0x1C)
- `Queue<GraphUpdateProcessor.GUOSingle> graphUpdateQueueAsync`（Queue<Graph更新Processor.GUOSingle> graph更新队列异步）(偏移: 0x20)
- `Queue<GraphUpdateProcessor.GUOSingle> graphUpdateQueuePost`（Queue<Graph更新Processor.GUOSingle> graph更新队列Post）(偏移: 0x24)
- `Queue<GraphUpdateProcessor.GUOSingle> graphUpdateQueueRegular`（Queue<Graph更新Processor.GUOSingle> graph更新队列Regular）(偏移: 0x28)
- `ManualResetEvent asyncGraphUpdatesComplete`（手动重置事件 asyncGraphUpdatesComplete）(偏移: 0x2C)
- `AutoResetEvent graphUpdateAsyncEvent`（自动重置事件 graph更新异步事件）(偏移: 0x30)
- `AutoResetEvent exitAsyncThread`（自动重置事件 exit异步Thread）(偏移: 0x34)

### 方法 (14)

- `void add_OnGraphsUpdated(Action value)`
  （void add_OnGraphsUpdated（动作 value））
- `void remove_OnGraphsUpdated(Action value)`
  （void remove_OnGraphsUpdated（动作 value））
- `bool get_IsAnyGraphUpdateQueued()`
  （bool get_是否任意Graph更新Queued（））
- `bool get_IsAnyGraphUpdateInProgress()`
  （bool get_是否任意Graph更新InProgress（））
- `AstarWorkItem GetWorkItem()`
  （AstarWork项目 获取Work项目（））
- `void EnableMultithreading()`
  （void 启用Multithreading（））
- `void DisableMultithreading()`
  （void 禁用Multithreading（））
- `void AddToQueue(GraphUpdateObject ob)`
  （void 添加To队列（Graph更新对象 ob））
- `void QueueGraphUpdatesInternal()`
  （void 队列GraphUpdates内部的（））
- `bool ProcessGraphUpdates(bool force)`
  （bool 处理GraphUpdates（bool force））
- `bool ProcessRegularUpdates(bool force)`
  （bool 处理RegularUpdates（bool force））
- `bool StartAsyncUpdatesIfQueued()`
  （bool 开始异步UpdatesIfQueued（））
- `void ProcessPostUpdates()`
  （void 处理PostUpdates（））
- `void ProcessGraphUpdatesAsync()`
  （void 处理GraphUpdates异步（））

---

## GraphUpdateProcessor.GUOSingle（Graph更新Processor.GUO单个）

### 字段 (3)

- `GraphUpdateProcessor.GraphUpdateOrder order`（Graph更新Processor.Graph更新Order order）(偏移: 0x0)
- `IUpdatableGraph graph`（IUpdatableGraph graph）(偏移: 0x4)
- `GraphUpdateObject obj`（Graph更新对象 obj）(偏移: 0x8)

---

## GraphUpdateProcessor.GraphUpdateOrder（Graph更新Processor.Graph更新Order）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## GraphUpdateScene（Graph更新场景）

**继承**: GraphModifier（图修改器）

### 字段 (19)

- `Vector3[] points`（Vector3[] points）(偏移: 0x20)
- `Vector3[] convexPoints`（Vector3[] convexPoints）(偏移: 0x24)
- `bool convex`（bool convex）(偏移: 0x28)
- `float minBoundsHeight`（float minBounds高度）(偏移: 0x2C)
- `int penaltyDelta`（int penaltyDelta）(偏移: 0x30)
- `bool modifyWalkability`（bool modifyWalkability）(偏移: 0x34)
- `bool setWalkability`（bool setWalkability）(偏移: 0x0)
- `bool applyOnStart`（bool applyOn开始）(偏移: 0x0)
- `bool applyOnScan`（bool applyOnScan）(偏移: 0x0)
- `bool updatePhysics`（bool update物理）(偏移: 0x0)
- `bool resetPenaltyOnPhysics`（bool reset惩罚On物理）(偏移: 0x0)
- `bool updateErosion`（bool updateErosion）(偏移: 0x0)
- `bool modifyTag`（bool modify标签）(偏移: 0x0)
- `int setTag`（int set标签）(偏移: 0x0)
- `bool legacyMode`（bool legacy模式）(偏移: 0x0)
- `int setTagInvert`（int set标签Invert）(偏移: 0x0)
- `bool firstApplied`（bool firstApplied）(偏移: 0x0)
- `int serializedVersion`（int serializedVersion）(偏移: 0x0)
- `bool legacyUseWorldSpace`（bool legacyUse世界的Space）(偏移: 0x0)

### 方法 (13)

- `void Start()`
  （void 开始（））
- `void OnPostScan()`
  （void 扫描后（））
- `void InvertSettings()`
  （void InvertSettings（））
- `void RecalcConvex()`
  （void RecalcConvex（））
- `void ToggleUseWorldSpace()`
  （void 开关Use世界的Space（））
- `void LockToY()`
  （void LockToY（））
- `Bounds GetBounds()`
  （Bounds 获取Bounds（））
- `void Apply()`
  （void 应用（））
- `void OnDrawGizmos()`
  （void 绘制辅助线时（））
- `void OnDrawGizmosSelected()`
  （void 绘制选中辅助线时（））
- `void OnDrawGizmos(bool selected)`
  （void OnDrawGizmos（bool selected））
- `void DisableLegacyMode()`
  （void 禁用Legacy模式（））
- `void Awake()`
  （void 唤醒（））

---

## GraphUpdateShape（Graph更新Shape）

### 字段 (8)

- `Vector3[] _points`（Vector3[] _points）(偏移: 0x8)
- `Vector3[] _convexPoints`（Vector3[] _convexPoints）(偏移: 0xC)
- `bool _convex`（bool _convex）(偏移: 0x10)
- `Vector3 right`（三维向量 right）(偏移: 0x14)
- `Vector3 forward`（三维向量 forward）(偏移: 0x20)
- `Vector3 up`（三维向量 up）(偏移: 0x2C)
- `Vector3 origin`（三维向量 origin）(偏移: 0x38)
- `float minimumHeight`（float minimum高度）(偏移: 0x44)

### 方法 (10)

- `Vector3[] get_points()`
  （Vector3[] get_points（））
- `void set_points(Vector3[] value)`
  （void set_points（Vector3[] value））
- `bool get_convex()`
  （bool get_convex（））
- `void set_convex(bool value)`
  （void set_convex（bool value））
- `void CalculateConvexHull()`
  （void 计算ConvexHull（））
- `Bounds GetBounds()`
  （Bounds 获取Bounds（））
- `Bounds GetBounds(Vector3[] points, Matrix4x4 matrix, float minimumHeight)`
  （Bounds 获取Bounds（Vector3[] points, Matrix4x4 matrix, float minimumHeight））
- `Bounds GetBounds(Vector3[] points, Vector3 right, Vector3 up, Vector3 forward, Vector3 origin, float minimumHeight)`
  （Bounds 获取Bounds（Vector3[] points, 三维向量 right, 三维向量 up, 三维向量 forward, 三维向量 origin, float minimumHeight））
- `bool Contains(GraphNode node)`
  （bool Contains（Graph节点 node））
- `bool Contains(Vector3 point)`
  （布尔值 包含（三维向量 point））

---

## GraphUpdateThreading（Graph更新Threading）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## GraphUpdateUtilities（Graph更新Utilities）

### 方法 (2)

- `bool UpdateGraphsNoBlock(GraphUpdateObject guo, GraphNode node1, GraphNode node2, bool alwaysRevert = False)`
  （bool 更新GraphsNoBlock（Graph更新对象 guo, Graph节点 node1, Graph节点 node2, bool alwaysRevert = False））
- `bool UpdateGraphsNoBlock(GraphUpdateObject guo, List<GraphNode> nodes, bool alwaysRevert = False)`
  （bool 更新GraphsNoBlock（Graph更新对象 guo, List<GraphNode> nodes, bool alwaysRevert = False））

---

## GraphUtilities（GraphUtilities）

### 方法 (3)

- `List<Vector3> GetContours(NavGraph graph)`
  （List<Vector3> 获取Contours（NavGraph graph））
- `void GetContours(INavmesh navmesh, Action<List<Int3>, bool> results)`
  （void 获取Contours（INavmesh navmesh, Action<List<Int3>, bool> results））
- `void GetContours(GridGraph grid, Action<Vector3[]> callback, float yMergeThreshold, GridNodeBase[] nodes)`
  （void 获取Contours（网格Graph grid, Action<Vector3[]> callback, float yMergeThreshold, 网格节点Base[] nodes））

---

## Graphic（Graphic）

**继承**: UIBehaviour, ICanvasElement（界面Behaviour, I画布元素）

### 字段 (21)

- `Material s_DefaultUI`（材质 s_默认的界面）(偏移: 0x0)
- `Texture2D s_WhiteTexture`（Texture2D s_White纹理）(偏移: 0x4)
- `Material m_Material`（材质 m_材质）(偏移: 0xC)
- `Color m_Color`（颜色 m_颜色）(偏移: 0x10)
- `bool m_SkipLayoutUpdate`（bool m_SkipLayout更新）(偏移: 0x20)
- `bool m_SkipMaterialUpdate`（bool m_Skip材质更新）(偏移: 0x21)
- `bool m_RaycastTarget`（bool m_Raycast目标）(偏移: 0x22)
- `Vector4 m_RaycastPadding`（Vector4 m_RaycastPadding）(偏移: 0x24)
- `RectTransform m_RectTransform`（Rect变换 m_Rect变换）(偏移: 0x34)
- `CanvasRenderer m_CanvasRenderer`（画布渲染器 m_画布渲染器）(偏移: 0x38)
- `Canvas m_Canvas`（画布 m_画布）(偏移: 0x3C)
- `bool m_VertsDirty`（bool m_VertsDirty）(偏移: 0x40)
- `bool m_MaterialDirty`（bool m_材质Dirty）(偏移: 0x41)
- `UnityAction m_OnDirtyLayoutCallback`（Unity引擎动作 m_OnDirtyLayout回调）(偏移: 0x44)
- `UnityAction m_OnDirtyVertsCallback`（Unity引擎动作 m_OnDirtyVerts回调）(偏移: 0x48)
- `UnityAction m_OnDirtyMaterialCallback`（Unity引擎动作 m_OnDirty材质回调）(偏移: 0x4C)
- `Mesh s_Mesh`（网格 s_网格）(偏移: 0x8)
- `VertexHelper s_VertexHelper`（Vertex辅助器 s_Vertex辅助器）(偏移: 0xC)
- `Mesh m_CachedMesh`（网格 m_Cached网格）(偏移: 0x50)
- `Vector2[] m_CachedUvs`（Vector2[] m_CachedUvs）(偏移: 0x54)
- `TweenRunner<ColorTween> m_ColorTweenRunner`（TweenRunner<颜色Tween> m_颜色TweenRunner）(偏移: 0x58)

### 方法 (57)

- `Material get_defaultGraphicMaterial()`
  （材质 get_defaultGraphic材质（））
- `Color get_color()`
  （颜色 获取_颜色（））
- `void set_color(Color value)`
  （void 设置_颜色（颜色 value））
- `bool get_raycastTarget()`
  （bool get_raycast目标（））
- `void set_raycastTarget(bool value)`
  （void set_raycast目标（bool value））
- `Vector4 get_raycastPadding()`
  （Vector4 get_raycastPadding（））
- `void set_raycastPadding(Vector4 value)`
  （void set_raycastPadding（Vector4 value））
- `bool get_useLegacyMeshGeneration()`
  （bool get_useLegacy网格Generation（））
- `void set_useLegacyMeshGeneration(bool value)`
  （void set_useLegacy网格Generation（bool value））
- `void SetAllDirty()`
  （void 集合所有Dirty（））
- `void SetLayoutDirty()`
  （void 集合LayoutDirty（））
- `void SetVerticesDirty()`
  （void 集合VerticesDirty（））
- `void SetMaterialDirty()`
  （void 集合材质Dirty（））
- `void OnRectTransformDimensionsChange()`
  （void 矩形变换尺寸改变时（））
- `void OnBeforeTransformParentChanged()`
  （void OnBefore变换父级Changed（））
- `void OnTransformParentChanged()`
  （void 变换父级改变时（））
- `int get_depth()`
  （int get_depth（））
- `RectTransform get_rectTransform()`
  （矩形变换 获取_矩形变换（））
- `Canvas get_canvas()`
  （画布 get_canvas（））
- `void CacheCanvas()`
  （void 缓存画布（））
- `CanvasRenderer get_canvasRenderer()`
  （画布渲染器 get_canvas渲染器（））
- `Material get_defaultMaterial()`
  （材质 get_default材质（））
- `Material get_material()`
  （材质 获取_材质（））
- `void set_material(Material value)`
  （void set_material（材质 value））
- `Material get_materialForRendering()`
  （材质 get_materialForRendering（））
- `Texture get_mainTexture()`
  （纹理 获取_主纹理（））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `void OnDestroy()`
  （void 销毁时（））
- `void OnCanvasHierarchyChanged()`
  （void 画布层级改变时（））
- `void OnCullingChanged()`
  （void OnCullingChanged（））
- `void Rebuild(CanvasUpdate update)`
  （void Rebuild（画布更新 update））
- `void LayoutComplete()`
  （void 布局完成（））
- `void GraphicUpdateComplete()`
  （void 图形更新完成（））
- `void UpdateMaterial()`
  （void 更新材质（））
- `void UpdateGeometry()`
  （void 更新Geometry（））
- `void DoMeshGeneration()`
  （void Do网格Generation（））
- `void DoLegacyMeshGeneration()`
  （void DoLegacy网格Generation（））
- `Mesh get_workerMesh()`
  （网格 get_worker网格（））
- `void OnFillVBO(List<UIVertex> vbo)`
  （void OnFillVBO（List<UIVertex> vbo））
- `void OnPopulateMesh(Mesh m)`
  （void OnPopulate网格（网格 m））
- `void OnPopulateMesh(VertexHelper vh)`
  （void OnPopulate网格（Vertex辅助器 vh））
- `void OnDidApplyAnimationProperties()`
  （void 已应用动画属性时（））
- `void SetNativeSize()`
  （void 集合Native大小（））
- `bool Raycast(Vector2 sp, Camera eventCamera)`
  （bool Raycast（二维向量 sp, 摄像机 eventCamera））
- `Vector2 PixelAdjustPoint(Vector2 point)`
  （二维向量 PixelAdjustPoint（二维向量 point））
- `Rect GetPixelAdjustedRect()`
  （Rect 获取PixelAdjustedRect（））
- `void CrossFadeColor(Color targetColor, float duration, bool ignoreTimeScale, bool useAlpha)`
  （void CrossFade颜色（颜色 targetColor, float duration, bool ignoreTimeScale, bool useAlpha））
- `void CrossFadeColor(Color targetColor, float duration, bool ignoreTimeScale, bool useAlpha, bool useRGB)`
  （void CrossFade颜色（颜色 targetColor, float duration, bool ignoreTimeScale, bool useAlpha, bool useRGB））
- `Color CreateColorFromAlpha(float alpha)`
  （颜色 创建颜色From透明度（float alpha））
- `void CrossFadeAlpha(float alpha, float duration, bool ignoreTimeScale)`
  （void CrossFade透明度（float alpha, float duration, bool ignoreTimeScale））
- `void RegisterDirtyLayoutCallback(UnityAction action)`
  （void RegisterDirtyLayout回调（Unity引擎动作 action））
- `void UnregisterDirtyLayoutCallback(UnityAction action)`
  （void UnregisterDirtyLayout回调（Unity引擎动作 action））
- `void RegisterDirtyVerticesCallback(UnityAction action)`
  （void RegisterDirtyVertices回调（Unity引擎动作 action））
- `void UnregisterDirtyVerticesCallback(UnityAction action)`
  （void UnregisterDirtyVertices回调（Unity引擎动作 action））
- `void RegisterDirtyMaterialCallback(UnityAction action)`
  （void RegisterDirty材质回调（Unity引擎动作 action））
- `void UnregisterDirtyMaterialCallback(UnityAction action)`
  （void UnregisterDirty材质回调（Unity引擎动作 action））

---

## GraphicConnector（GraphicConnector）

### 字段 (2)

- `List<GraphicConnector> s_Connectors`（List<GraphicConnector> s_Connectors）(偏移: 0x0)
- `GraphicConnector s_EmptyConnector`（GraphicConnector s_空Connector）(偏移: 0x8)

### 方法 (7)

- `void Init()`
  （void 初始化（））
- `void AddConnector(GraphicConnector connector)`
  （void 添加Connector（GraphicConnector connector））
- `GraphicConnector FindConnector(Graphic graphic)`
  （GraphicConnector 查找Connector（Graphic graphic））
- `int get_priority()`
  （int get_priority（））
- `bool IsValid(Graphic graphic)`
  （bool 是否Valid（Graphic graphic））
- `void SetVerticesDirty(Graphic graphic)`
  （void 集合VerticesDirty（Graphic graphic））
- `void SetMaterialDirty(Graphic graphic)`
  （void 集合材质Dirty（Graphic graphic））

---

## GraphicConnectorExtension（GraphicConnector扩展）

### 方法 (2)

- `void SetVerticesDirtyEx(Graphic graphic)`
  （void 集合VerticesDirtyEx（Graphic graphic））
- `void SetMaterialDirtyEx(Graphic graphic)`
  （void 集合材质DirtyEx（Graphic graphic））

---

## GraphicRaycaster（GraphicRaycaster）

**继承**: BaseRaycaster（基础Raycaster）

### 字段 (6)

- `bool m_IgnoreReversedGraphics`（bool m_IgnoreReversedGraphics）(偏移: 0x10)
- `GraphicRaycaster.BlockingObjects m_BlockingObjects`（GraphicRaycaster.BlockingObjects m_BlockingObjects）(偏移: 0x14)
- `LayerMask m_BlockingMask`（层掩码 m_Blocking掩码）(偏移: 0x18)
- `Canvas m_Canvas`（画布 m_画布）(偏移: 0x1C)
- `List<Graphic> m_RaycastResults`（List<Graphic> m_RaycastResults）(偏移: 0x20)
- `List<Graphic> s_SortedGraphics`（List<Graphic> s_SortedGraphics）(偏移: 0x0)

### 方法 (12)

- `int get_sortOrderPriority()`
  （int get_sortOrderPriority（））
- `int get_renderOrderPriority()`
  （int get_renderOrderPriority（））
- `bool get_ignoreReversedGraphics()`
  （bool get_ignoreReversedGraphics（））
- `void set_ignoreReversedGraphics(bool value)`
  （void set_ignoreReversedGraphics（bool value））
- `GraphicRaycaster.BlockingObjects get_blockingObjects()`
  （GraphicRaycaster.BlockingObjects get_blockingObjects（））
- `void set_blockingObjects(GraphicRaycaster.BlockingObjects value)`
  （void set_blockingObjects（GraphicRaycaster.BlockingObjects value））
- `LayerMask get_blockingMask()`
  （层掩码 get_blocking掩码（））
- `void set_blockingMask(LayerMask value)`
  （void set_blocking掩码（层掩码 value））
- `Canvas get_canvas()`
  （画布 get_canvas（））
- `void Raycast(PointerEventData eventData, List<RaycastResult> resultAppendList)`
  （void Raycast（指针事件数据 eventData, List<RaycastResult> resultAppendList））
- `Camera get_eventCamera()`
  （摄像机 get_event摄像机（））
- `void Raycast(Canvas canvas, Camera eventCamera, Vector2 pointerPosition, IList<Graphic> foundGraphics, List<Graphic> results)`
  （void Raycast（画布 canvas, 摄像机 eventCamera, 二维向量 pointerPosition, IList<Graphic> foundGraphics, List<Graphic> results））

---

## GraphicRaycaster.BlockingObjects（GraphicRaycaster.BlockingObjects）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## GraphicRegistry（GraphicRegistry）

### 字段 (2)

- `GraphicRegistry s_Instance`（GraphicRegistry s_实例）(偏移: 0x0)
- `List<Graphic> s_EmptyList`（List<Graphic> s_空列表）(偏移: 0x4)

### 方法 (7)

- `GraphicRegistry get_instance()`
  （GraphicRegistry get_instance（））
- `void RegisterGraphicForCanvas(Canvas c, Graphic graphic)`
  （void RegisterGraphicFor画布（画布 c, Graphic graphic））
- `void RegisterRaycastGraphicForCanvas(Canvas c, Graphic graphic)`
  （void RegisterRaycastGraphicFor画布（画布 c, Graphic graphic））
- `void UnregisterGraphicForCanvas(Canvas c, Graphic graphic)`
  （void UnregisterGraphicFor画布（画布 c, Graphic graphic））
- `void UnregisterRaycastGraphicForCanvas(Canvas c, Graphic graphic)`
  （void UnregisterRaycastGraphicFor画布（画布 c, Graphic graphic））
- `IList<Graphic> GetGraphicsForCanvas(Canvas canvas)`
  （IList<Graphic> 获取GraphicsFor画布（画布 canvas））
- `IList<Graphic> GetRaycastableGraphicsForCanvas(Canvas canvas)`
  （IList<Graphic> 获取RaycastableGraphicsFor画布（画布 canvas））

---

## Graphics（Graphics）

### 字段 (1)

- `int kMaxDrawMeshInstanceCount`（int k最大Draw网格实例数量）(偏移: 0x0)

### 方法 (13)

- `int Internal_GetMaxDrawMeshInstanceCount()`
  （int Internal_获取最大Draw网格实例数量（））
- `GraphicsTier get_activeTier()`
  （GraphicsTier get_activeTier（））
- `bool GetPreserveFramebufferAlpha()`
  （bool 获取PreserveFramebuffer透明度（））
- `bool get_preserveFramebufferAlpha()`
  （bool get_preserveFramebuffer透明度（））
- `OpenGLESVersion GetMinOpenGLESVersion()`
  （打开GLESVersion 获取最小打开GLESVersion（））
- `OpenGLESVersion get_minOpenGLESVersion()`
  （打开GLESVersion get_min打开GLESVersion（））
- `void CopyTexture_Slice(Texture src, int srcElement, int srcMip, Texture dst, int dstElement, int dstMip)`
  （void 复制Texture_Slice（纹理 src, int srcElement, int srcMip, 纹理 dst, int dstElement, int dstMip））
- `void Internal_DrawMeshNow2(Mesh mesh, int subsetIndex, Matrix4x4 matrix)`
  （void Internal_Draw网格Now2（网格 mesh, int subsetIndex, Matrix4x4 matrix））
- `void ExecuteCommandBuffer(CommandBuffer buffer)`
  （void 执行Command缓冲区（Command缓冲区 buffer））
- `void CopyTexture(Texture src, int srcElement, int srcMip, Texture dst, int dstElement, int dstMip)`
  （void 复制纹理（纹理 src, int srcElement, int srcMip, 纹理 dst, int dstElement, int dstMip））
- `void DrawMeshNow(Mesh mesh, Matrix4x4 matrix, int materialIndex)`
  （void Draw网格Now（网格 mesh, Matrix4x4 matrix, int materialIndex））
- `void DrawMeshNow(Mesh mesh, Matrix4x4 matrix)`
  （void Draw网格Now（网格 mesh, Matrix4x4 matrix））
- `void Internal_DrawMeshNow2_Injected(Mesh mesh, int subsetIndex, ref Matrix4x4 matrix)`
  （void Internal_Draw网格Now2_Injected（网格 mesh, int subsetIndex, ref Matrix4x4 matrix））

---

## GraphicsDeviceType（GraphicsDevice类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## GraphicsFence（GraphicsFence）

### 字段 (3)

- `IntPtr m_Ptr`（整数指针 m_指针）(偏移: 0x0)
- `int m_Version`（整数 m_版本）(偏移: 0x4)
- `GraphicsFenceType m_FenceType`（GraphicsFence类型 m_Fence类型）(偏移: 0x8)

### 方法 (6)

- `SynchronisationStageFlags TranslateSynchronizationStageToFlags(SynchronisationStage s)`
  （SynchronisationStageFlags TranslateSynchronizationStageToFlags（SynchronisationStage s））
- `void InitPostAllocation()`
  （void 初始化PostAllocation（））
- `bool IsFencePending()`
  （bool 是否FencePending（））
- `void Validate()`
  （void 验证（））
- `int GetPlatformNotSupportedVersion()`
  （int 获取PlatformNotSupportedVersion（））
- `int GetVersionNumber(IntPtr fencePtr)`
  （int 获取VersionNumber（整数Ptr fencePtr））

---

## GraphicsFenceType（GraphicsFence类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## GraphicsFormat（Graphics格式化）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## GraphicsFormatUtility（Graphics格式化工具）

### 方法 (12)

- `GraphicsFormat GetFormat(Texture texture)`
  （Graphics格式化 获取格式化（纹理 texture））
- `GraphicsFormat GetGraphicsFormat(TextureFormat format, bool isSRGB)`
  （Graphics格式化 获取Graphics格式化（纹理格式化 format, bool isSRGB））
- `GraphicsFormat GetGraphicsFormat_Native_TextureFormat(TextureFormat format, bool isSRGB)`
  （Graphics格式化 获取GraphicsFormat_Native_纹理格式化（纹理格式化 format, bool isSRGB））
- `GraphicsFormat GetGraphicsFormat(RenderTextureFormat format, bool isSRGB)`
  （Graphics格式化 获取Graphics格式化（Render纹理格式化 format, bool isSRGB））
- `GraphicsFormat GetGraphicsFormat_Native_RenderTextureFormat(RenderTextureFormat format, bool isSRGB)`
  （Graphics格式化 获取GraphicsFormat_Native_Render纹理格式化（Render纹理格式化 format, bool isSRGB））
- `GraphicsFormat GetGraphicsFormat(RenderTextureFormat format, RenderTextureReadWrite readWrite)`
  （Graphics格式化 获取Graphics格式化（Render纹理格式化 format, Render纹理ReadWrite readWrite））
- `bool IsSRGBFormat(GraphicsFormat format)`
  （bool 是否SRGB格式化（Graphics格式化 format））
- `RenderTextureFormat GetRenderTextureFormat(GraphicsFormat format)`
  （Render纹理格式化 获取Render纹理格式化（Graphics格式化 format））
- `bool IsCompressedTextureFormat(TextureFormat format)`
  （bool 是否Compressed纹理格式化（纹理格式化 format））
- `bool CanDecompressFormat(GraphicsFormat format, bool wholeImage)`
  （bool 能否Decompress格式化（Graphics格式化 format, bool wholeImage））
- `bool CanDecompressFormat(GraphicsFormat format)`
  （bool 能否Decompress格式化（Graphics格式化 format））
- `bool IsCrunchFormat(TextureFormat format)`
  （bool 是否Crunch格式化（纹理格式化 format））

---

## GraphicsSettings（GraphicsSettings）

**继承**: Object（对象）

### 方法 (12)

- `bool get_lightsUseLinearIntensity()`
  （bool get_lightsUseLinearIntensity（））
- `void set_lightsUseLinearIntensity(bool value)`
  （void set_lightsUseLinearIntensity（bool value））
- `void set_useScriptableRenderPipelineBatching(bool value)`
  （void set_useScriptableRenderPipelineBatching（bool value））
- `bool HasShaderDefine(GraphicsTier tier, BuiltinShaderDefine defineHash)`
  （bool 是否有着色器Define（GraphicsTier tier, Builtin着色器Define defineHash））
- `ScriptableObject get_INTERNAL_currentRenderPipeline()`
  （脚本对象 get_INTERNAL_currentRenderPipeline（））
- `RenderPipelineAsset get_currentRenderPipeline()`
  （RenderPipeline资产 get_currentRenderPipeline（））
- `RenderPipelineAsset get_renderPipelineAsset()`
  （RenderPipeline资产 get_renderPipeline资产（））
- `void set_renderPipelineAsset(RenderPipelineAsset value)`
  （void set_renderPipeline资产（RenderPipeline资产 value））
- `ScriptableObject get_INTERNAL_defaultRenderPipeline()`
  （脚本对象 get_INTERNAL_defaultRenderPipeline（））
- `void set_INTERNAL_defaultRenderPipeline(ScriptableObject value)`
  （void set_INTERNAL_defaultRenderPipeline（脚本对象 value））
- `RenderPipelineAsset get_defaultRenderPipeline()`
  （RenderPipeline资产 get_defaultRenderPipeline（））
- `void set_defaultRenderPipeline(RenderPipelineAsset value)`
  （void set_defaultRenderPipeline（RenderPipeline资产 value））

---

## GraphicsTier（GraphicsTier）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## GregorianCalendar（GregorianCalendar）

**继承**: Calendar（日历）

### 字段 (4)

- `GregorianCalendarTypes m_type`（GregorianCalendarTypes m_type）(偏移: 0x14)
- `int[] DaysToMonth365`（int[] DaysToMonth365）(偏移: 0x0)
- `int[] DaysToMonth366`（int[] DaysToMonth366）(偏移: 0x4)
- `Calendar s_defaultInstance`（Calendar s_default实例）(偏移: 0x8)

### 方法 (21)

- `void OnDeserialized(StreamingContext ctx)`
  （void 反序列化后（流上下文 ctx））
- `DateTime get_MinSupportedDateTime()`
  （日期时间 获取_最小支持日期时间（））
- `DateTime get_MaxSupportedDateTime()`
  （日期时间 获取_最大支持日期时间（））
- `Calendar GetDefaultInstance()`
  （Calendar 获取默认的实例（））
- `int get_ID()`
  （整数 获取_ID（））
- `int GetDatePart(long ticks, int part)`
  （int 获取DatePart（long ticks, int part））
- `long GetAbsoluteDate(int year, int month, int day)`
  （long 获取AbsoluteDate（int year, int month, int day））
- `int GetDayOfMonth(DateTime time)`
  （整数 获取_月中的日（日期时间 time））
- `DayOfWeek GetDayOfWeek(DateTime time)`
  （星期几 获取星期几（日期时间 time））
- `int GetDaysInMonth(int year, int month, int era)`
  （整数 获取_月中的天数（整数 year, 整数 month, 整数 era））
- `int GetDaysInYear(int year, int era)`
  （整数 获取_年中的天数（整数 year, 整数 era））
- `int GetEra(DateTime time)`
  （整数 获取_纪元（日期时间 time））
- `int[] get_Eras()`
  （整数[] 获取_纪元（））
- `int GetMonth(DateTime time)`
  （整数 获取_月（日期时间 time））
- `int GetMonthsInYear(int year, int era)`
  （整数 获取_年中的月数（整数 year, 整数 era））
- `int GetYear(DateTime time)`
  （整数 获取_年（日期时间 time））
- `bool IsLeapYear(int year, int era)`
  （布尔值 是否闰年（整数 year, 整数 era））
- `DateTime ToDateTime(int year, int month, int day, int hour, int minute, int second, int millisecond, int era)`
  （日期时间 转日期时间（整数 year, 整数 month, 整数 day, 整数 hour, 整数 minute, 整数 second, 整数 millisecond, 整数 era））
- `bool TryToDateTime(int year, int month, int day, int hour, int minute, int second, int millisecond, int era, out DateTime result)`
  （bool TryToDate时间（int year, int month, int day, int hour, int minute, int second, int millisecond, int era, out DateTime result））
- `int get_TwoDigitYearMax()`
  （整数 获取_两位数年份最大（））
- `int ToFourDigitYear(int year)`
  （整数 转四位数年份（整数 year））

---

## GregorianCalendarHelper（GregorianCalendar辅助器）

### 字段 (8)

- `int[] DaysToMonth365`（int[] DaysToMonth365）(偏移: 0x0)
- `int[] DaysToMonth366`（int[] DaysToMonth366）(偏移: 0x4)
- `int m_maxYear`（int m_maxYear）(偏移: 0x8)
- `int m_minYear`（int m_minYear）(偏移: 0xC)
- `Calendar m_Cal`（Calendar m_Cal）(偏移: 0x10)
- `EraInfo[] m_EraInfo`（EraInfo[] m_Era信息）(偏移: 0x14)
- `int[] m_eras`（int[] m_eras）(偏移: 0x18)
- `DateTime m_minDate`（Date时间 m_minDate）(偏移: 0x20)

### 方法 (20)

- `int get_MaxYear()`
  （int get_最大Year（））
- `int GetGregorianYear(int year, int era)`
  （int 获取GregorianYear（int year, int era））
- `bool IsValidYear(int year, int era)`
  （bool 是否ValidYear（int year, int era））
- `int GetDatePart(long ticks, int part)`
  （int 获取DatePart（long ticks, int part））
- `long GetAbsoluteDate(int year, int month, int day)`
  （long 获取AbsoluteDate（int year, int month, int day））
- `long DateToTicks(int year, int month, int day)`
  （long DateToTicks（int year, int month, int day））
- `long TimeToTicks(int hour, int minute, int second, int millisecond)`
  （long 时间ToTicks（int hour, int minute, int second, int millisecond））
- `void CheckTicksRange(long ticks)`
  （void 检查Ticks范围（long ticks））
- `int GetDayOfMonth(DateTime time)`
  （整数 获取_月中的日（日期时间 time））
- `DayOfWeek GetDayOfWeek(DateTime time)`
  （星期几 获取星期几（日期时间 time））
- `int GetDaysInMonth(int year, int month, int era)`
  （整数 获取_月中的天数（整数 year, 整数 month, 整数 era））
- `int GetDaysInYear(int year, int era)`
  （整数 获取_年中的天数（整数 year, 整数 era））
- `int GetEra(DateTime time)`
  （整数 获取_纪元（日期时间 time））
- `int[] get_Eras()`
  （整数[] 获取_纪元（））
- `int GetMonth(DateTime time)`
  （整数 获取_月（日期时间 time））
- `int GetMonthsInYear(int year, int era)`
  （整数 获取_年中的月数（整数 year, 整数 era））
- `int GetYear(DateTime time)`
  （整数 获取_年（日期时间 time））
- `bool IsLeapYear(int year, int era)`
  （布尔值 是否闰年（整数 year, 整数 era））
- `DateTime ToDateTime(int year, int month, int day, int hour, int minute, int second, int millisecond, int era)`
  （日期时间 转日期时间（整数 year, 整数 month, 整数 day, 整数 hour, 整数 minute, 整数 second, 整数 millisecond, 整数 era））
- `int ToFourDigitYear(int year, int twoDigitYearMax)`
  （int ToFourDigitYear（int year, int twoDigitYearMax））

---

## GregorianCalendarTypes（GregorianCalendarTypes）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## GridGraph（网格Graph）

**继承**: NavGraph, IUpdatableGraph, ITransformedGraph, IRaycastableGraph（NavGraph, IUpdatableGraph, ITransformedGraph, IRaycastableGraph）

### 字段 (35)

- `InspectorGridMode inspectorGridMode`（Inspector网格模式 inspector网格模式）(偏移: 0xB8)
- `int width`（整数 宽度）(偏移: 0xBC)
- `int depth`（整数 深度）(偏移: 0xC0)
- `float aspectRatio`（float aspect比率）(偏移: 0xC4)
- `float isometricAngle`（float isometric角度）(偏移: 0xC8)
- `bool uniformEdgeCosts`（bool uniformEdgeCosts）(偏移: 0xCC)
- `Vector3 rotation`（三维向量 旋转）(偏移: 0xD0)
- `Vector3 center`（三维向量 center）(偏移: 0xDC)
- `Vector2 unclampedSize`（二维向量 unclamped大小）(偏移: 0xE8)
- `float nodeSize`（float node大小）(偏移: 0xF0)
- `GraphCollision collision`（GraphCollision collision）(偏移: 0xF4)
- `float maxClimb`（float max攀爬）(偏移: 0xF8)
- `float maxSlope`（float maxSlope）(偏移: 0xFC)
- `int erodeIterations`（int erodeIterations）(偏移: 0x100)
- `bool erosionUseTags`（bool erosionUseTags）(偏移: 0x104)
- `int erosionFirstTag`（int erosion第一个标签）(偏移: 0x108)
- `NumNeighbours neighbours`（NumNeighbours neighbours）(偏移: 0x10C)
- `bool cutCorners`（bool cutCorners）(偏移: 0x110)
- `float penaltyPositionOffset`（float penaltyPositionOffset）(偏移: 0x114)
- `bool penaltyPosition`（bool penaltyPosition）(偏移: 0x118)
- `float penaltyPositionFactor`（float penaltyPosition系数）(偏移: 0x11C)
- `bool penaltyAngle`（bool penalty角度）(偏移: 0x120)
- `float penaltyAngleFactor`（float penalty角度系数）(偏移: 0x124)
- `float penaltyAnglePower`（float penalty角度力度）(偏移: 0x128)
- `bool useJumpPointSearch`（bool use跳跃Point搜索）(偏移: 0x12C)
- `bool showMeshOutline`（bool show网格Outline）(偏移: 0x0)
- `bool showNodeConnections`（bool show节点Connections）(偏移: 0x0)
- `bool showMeshSurface`（bool show网格Surface）(偏移: 0x0)
- `GridGraph.TextureData textureData`（网格Graph.纹理数据 texture数据）(偏移: 0x0)
- `int[] neighbourOffsets`（int[] neighbourOffsets）(偏移: 0x13C)
- `uint[] neighbourCosts`（uint[] neighbourCosts）(偏移: 0x140)
- `int[] neighbourXOffsets`（int[] neighbourXOffsets）(偏移: 0x144)
- `int[] neighbourZOffsets`（int[] neighbourZOffsets）(偏移: 0x148)
- `int[] hexagonNeighbourIndices`（int[] hexagonNeighbourIndices）(偏移: 0x0)
- `GridNode[] nodes`（网格Node[] nodes）(偏移: 0x14C)

### 方法 (77)

- `void OnDestroy()`
  （void 销毁时（））
- `void DestroyAllNodes()`
  （void 销毁所有Nodes（））
- `void RemoveGridGraphFromStatic()`
  （void 移除网格GraphFrom静态的（））
- `bool get_uniformWidthDepthGrid()`
  （bool get_uniform宽度深度网格（））
- `int get_LayerCount()`
  （int get_层数量（））
- `int CountNodes()`
  （int 数量Nodes（））
- `void GetNodes(Action<GraphNode> action)`
  （void 获取节点（Action<GraphNode> action））
- `bool get_useRaycastNormal()`
  （bool get_useRaycast法线（））
- `Vector2 get_size()`
  （二维向量 get_size（））
- `void set_size(Vector2 value)`
  （void set_size（二维向量 value））
- `GraphTransform get_transform()`
  （Graph变换 get_transform（））
- `void set_transform(GraphTransform value)`
  （void set_transform（Graph变换 value））
- `void RelocateNodes(Matrix4x4 deltaMatrix)`
  （void RelocateNodes（Matrix4x4 deltaMatrix））
- `void RelocateNodes(Vector3 center, Quaternion rotation, float nodeSize, float aspectRatio = 1, float isometricAngle = 0)`
  （void RelocateNodes（三维向量 center, Quaternion rotation, float nodeSize, float aspectRatio = 1, float isometricAngle = 0））
- `Int3 GraphPointToWorld(int x, int z, float height)`
  （Int3 GraphPointTo世界的（int x, int z, float height））
- `int get_Width()`
  （int get_宽度（））
- `void set_Width(int value)`
  （void set_宽度（int value））
- `int get_Depth()`
  （int get_深度（））
- `void set_Depth(int value)`
  （void set_深度（int value））
- `uint GetConnectionCost(int dir)`
  （uint 获取连接Cost（int dir））
- `GridNode GetNodeConnection(GridNode node, int dir)`
  （网格节点 获取节点连接（网格节点 node, int dir））
- `bool HasNodeConnection(GridNode node, int dir)`
  （bool 是否有节点连接（网格节点 node, int dir））
- `void SetNodeConnection(GridNode node, int dir, bool value)`
  （void 集合节点连接（网格节点 node, int dir, bool value））
- `GridNode GetNodeConnection(int index, int x, int z, int dir)`
  （网格节点 获取节点连接（int index, int x, int z, int dir））
- `void SetNodeConnection(int index, int x, int z, int dir, bool value)`
  （void 集合节点连接（int index, int x, int z, int dir, bool value））
- `bool HasNodeConnection(int index, int x, int z, int dir)`
  （bool 是否有节点连接（int index, int x, int z, int dir））
- `void SetDimensions(int width, int depth, float nodeSize)`
  （void 集合Dimensions（int width, int depth, float nodeSize））
- `void UpdateSizeFromWidthDepth()`
  （void 更新大小From宽度深度（））
- `void GenerateMatrix()`
  （void Generate矩阵（））
- `void UpdateTransform()`
  （void 更新变换（））
- `GraphTransform CalculateTransform()`
  （Graph变换 计算变换（））
- `void CalculateDimensions(out int width, out int depth, out float nodeSize)`
  （void 计算Dimensions（out int width, out int depth, out float nodeSize））
- `NNInfoInternal GetNearest(Vector3 position, NNConstraint constraint, GraphNode hint)`
  （NN信息内部 获取最近（三维向量 position, NN约束 constraint, 图节点 hint））
- `NNInfoInternal GetNearestForce(Vector3 position, NNConstraint constraint)`
  （NN信息内部 获取最近强制（三维向量 position, NN约束 constraint））
- `void SetUpOffsetsAndCosts()`
  （void 集合上OffsetsAndCosts（））
- `IEnumerable<Progress> ScanInternal()`
  （IEnumerable<进度> 扫描内部（））
- `void UpdateNodePositionCollision(GridNode node, int x, int z, bool resetPenalty = True)`
  （void 更新节点PositionCollision（网格节点 node, int x, int z, bool resetPenalty = True））
- `void RecalculateCell(int x, int z, bool resetPenalties = True, bool resetTags = True)`
  （void RecalculateCell（int x, int z, bool resetPenalties = True, bool resetTags = True））
- `bool ErosionAnyFalseConnections(GraphNode baseNode)`
  （bool Erosion任意FalseConnections（Graph节点 baseNode））
- `void ErodeNode(GraphNode node)`
  （void Erode节点（Graph节点 node））
- `void ErodeNodeWithTagsInit(GraphNode node)`
  （void Erode节点WithTags初始化（Graph节点 node））
- `void ErodeNodeWithTags(GraphNode node, int iteration)`
  （void Erode节点WithTags（Graph节点 node, int iteration））
- `void ErodeWalkableArea()`
  （void ErodeWalkableArea（））
- `void ErodeWalkableArea(int xmin, int zmin, int xmax, int zmax)`
  （void ErodeWalkableArea（int xmin, int zmin, int xmax, int zmax））
- `bool IsValidConnection(GridNodeBase node1, GridNodeBase node2)`
  （bool 是否Valid连接（网格节点基础 node1, 网格节点基础 node2））
- `void CalculateConnectionsForCellAndNeighbours(int x, int z)`
  （void 计算ConnectionsForCellAndNeighbours（int x, int z））
- `void CalculateConnections(GridNode node)`
  （void 计算Connections（网格节点 node））
- `void CalculateConnections(GridNodeBase node)`
  （void 计算Connections（网格节点基础 node））
- `void CalculateConnections(int x, int z, GridNode node)`
  （void 计算Connections（int x, int z, 网格节点 node））
- `void CalculateConnections(int x, int z)`
  （void 计算Connections（int x, int z））
- `void OnDrawGizmos(RetainedGizmos gizmos, bool drawNodes)`
  （void OnDrawGizmos（RetainedGizmos gizmos, bool drawNodes））
- `void CreateNavmeshSurfaceVisualization(GridNodeBase[] nodes, int nodeCount, GraphGizmoHelper helper)`
  （void 创建NavmeshSurfaceVisualization（网格节点Base[] nodes, int nodeCount, GraphGizmo辅助器 helper））
- `IntRect GetRectFromBounds(Bounds bounds)`
  （整数Rect 获取RectFromBounds（Bounds bounds））
- `List<GraphNode> GetNodesInArea(Bounds bounds)`
  （List<GraphNode> 获取NodesInArea（Bounds bounds））
- `List<GraphNode> GetNodesInArea(GraphUpdateShape shape)`
  （List<GraphNode> 获取NodesInArea（Graph更新Shape shape））
- `List<GraphNode> GetNodesInArea(Bounds bounds, GraphUpdateShape shape)`
  （List<GraphNode> 获取NodesInArea（Bounds bounds, Graph更新Shape shape））
- `List<GraphNode> GetNodesInRegion(Bounds bounds)`
  （List<GraphNode> 获取NodesInRegion（Bounds bounds））
- `List<GraphNode> GetNodesInRegion(GraphUpdateShape shape)`
  （List<GraphNode> 获取NodesInRegion（Graph更新Shape shape））
- `List<GraphNode> GetNodesInRegion(Bounds bounds, GraphUpdateShape shape)`
  （List<GraphNode> 获取NodesInRegion（Bounds bounds, Graph更新Shape shape））
- `List<GraphNode> GetNodesInRegion(IntRect rect)`
  （List<GraphNode> 获取NodesInRegion（整数Rect rect））
- `int GetNodesInRegion(IntRect rect, GridNodeBase[] buffer)`
  （int 获取NodesInRegion（整数Rect rect, 网格节点Base[] buffer））
- `GridNodeBase GetNode(int x, int z)`
  （网格节点基础 获取节点（int x, int z））
- `void CalculateAffectedRegions(GraphUpdateObject o, out IntRect originalRect, out IntRect affectRect, out IntRect physicsRect, out bool willChangeWalkability, out int erosion)`
  （void 计算AffectedRegions（Graph更新对象 o, out IntRect originalRect, out IntRect affectRect, out IntRect physicsRect, out bool willChangeWalkability, out int erosion））
- `bool Linecast(Vector3 from, Vector3 to)`
  （bool Linecast（三维向量 from, 三维向量 to））
- `bool Linecast(Vector3 from, Vector3 to, GraphNode hint)`
  （bool Linecast（三维向量 from, 三维向量 to, Graph节点 hint））
- `bool Linecast(Vector3 from, Vector3 to, GraphNode hint, out GraphHitInfo hit)`
  （bool Linecast（三维向量 from, 三维向量 to, Graph节点 hint, out GraphHitInfo hit））
- `float CrossMagnitude(Vector2 a, Vector2 b)`
  （float CrossMagnitude（二维向量 a, 二维向量 b））
- `long CrossMagnitude(Int2 a, Int2 b)`
  （long CrossMagnitude（Int2 a, Int2 b））
- `bool ClipLineSegmentToBounds(Vector3 a, Vector3 b, out Vector3 outA, out Vector3 outB)`
  （bool 弹匣LineSegmentToBounds（三维向量 a, 三维向量 b, out Vector3 outA, out Vector3 outB））
- `bool Linecast(Vector3 from, Vector3 to, GraphNode hint, out GraphHitInfo hit, List<GraphNode> trace)`
  （bool Linecast（三维向量 from, 三维向量 to, Graph节点 hint, out GraphHitInfo hit, List<GraphNode> trace））
- `bool SnappedLinecast(Vector3 from, Vector3 to, GraphNode hint, out GraphHitInfo hit)`
  （bool SnappedLinecast（三维向量 from, 三维向量 to, Graph节点 hint, out GraphHitInfo hit））
- `bool Linecast(GridNodeBase fromNode, GridNodeBase toNode)`
  （bool Linecast（网格节点基础 fromNode, 网格节点基础 toNode））
- `bool CheckConnection(GridNode node, int dir)`
  （bool 检查连接（网格节点 node, int dir））
- `void SerializeExtraInfo(GraphSerializationContext ctx)`
  （void 序列化额外信息（图序列化上下文 ctx））
- `void DeserializeExtraInfo(GraphSerializationContext ctx)`
  （void 反序列化额外信息（图序列化上下文 ctx））
- `void DeserializeSettingsCompatibility(GraphSerializationContext ctx)`
  （void 反序列化设置兼容性（图序列化上下文 ctx））
- `void PostDeserialization(GraphSerializationContext ctx)`
  （void 反序列化后（图序列化上下文 ctx））

---

## GridGraph.TextureData（网格Graph.纹理数据）

### 字段 (5)

- `bool enabled`（bool enabled）(偏移: 0x8)
- `Texture2D source`（Texture2D source）(偏移: 0xC)
- `float[] factors`（float[] factors）(偏移: 0x10)
- `GridGraph.TextureData.ChannelUse[] channels`（网格Graph.纹理Data.ChannelUse[] channels）(偏移: 0x14)
- `Color32[] data`（Color32[] data）(偏移: 0x18)

### 方法 (3)

- `void Initialize()`
  （void 初始化（））
- `void Apply(GridNode node, int x, int z)`
  （void 应用（网格节点 node, int x, int z））
- `void ApplyChannel(GridNode node, int x, int z, int value, GridGraph.TextureData.ChannelUse channelUse, float factor)`
  （void 应用Channel（网格节点 node, int x, int z, int value, 网格Graph.纹理Data.ChannelUse channelUse, float factor））

---

## GridGraph.TextureData.ChannelUse（网格Graph.纹理Data.ChannelUse）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## GridLayout（网格Layout）

**继承**: Behaviour（行为）

### 方法 (1)

- `void DoNothing()`
  （void DoNothing（））

---

## GridLayoutGroup（网格Layout组）

**继承**: LayoutGroup（Layout组）

### 字段 (6)

- `GridLayoutGroup.Corner m_StartCorner`（网格LayoutGroup.Corner m_开始Corner）(偏移: 0x38)
- `GridLayoutGroup.Axis m_StartAxis`（网格LayoutGroup.轴 m_开始轴）(偏移: 0x3C)
- `Vector2 m_CellSize`（二维向量 m_Cell大小）(偏移: 0x40)
- `Vector2 m_Spacing`（二维向量 m_Spacing）(偏移: 0x48)
- `GridLayoutGroup.Constraint m_Constraint`（网格LayoutGroup.Constraint m_Constraint）(偏移: 0x50)
- `int m_ConstraintCount`（int m_Constraint数量）(偏移: 0x54)

### 方法 (17)

- `GridLayoutGroup.Corner get_startCorner()`
  （网格LayoutGroup.Corner get_startCorner（））
- `void set_startCorner(GridLayoutGroup.Corner value)`
  （void set_startCorner（网格LayoutGroup.Corner value））
- `GridLayoutGroup.Axis get_startAxis()`
  （网格LayoutGroup.轴 get_start轴（））
- `void set_startAxis(GridLayoutGroup.Axis value)`
  （void set_start轴（网格LayoutGroup.轴 value））
- `Vector2 get_cellSize()`
  （二维向量 get_cell大小（））
- `void set_cellSize(Vector2 value)`
  （void set_cell大小（二维向量 value））
- `Vector2 get_spacing()`
  （二维向量 get_spacing（））
- `void set_spacing(Vector2 value)`
  （void set_spacing（二维向量 value））
- `GridLayoutGroup.Constraint get_constraint()`
  （网格LayoutGroup.Constraint get_constraint（））
- `void set_constraint(GridLayoutGroup.Constraint value)`
  （void set_constraint（网格LayoutGroup.Constraint value））
- `int get_constraintCount()`
  （int get_constraint数量（））
- `void set_constraintCount(int value)`
  （void set_constraint数量（int value））
- `void CalculateLayoutInputHorizontal()`
  （void 计算布局输入水平（））
- `void CalculateLayoutInputVertical()`
  （void 计算布局输入垂直（））
- `void SetLayoutHorizontal()`
  （void 设置布局水平（））
- `void SetLayoutVertical()`
  （void 设置布局垂直（））
- `void SetCellsAlongAxis(int axis)`
  （void 集合CellsAlong轴（int axis））

---

## GridLayoutGroup.Axis（网格LayoutGroup.轴）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## GridLayoutGroup.Constraint（网格LayoutGroup.Constraint）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## GridLayoutGroup.Corner（网格LayoutGroup.Corner）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## GridNode（网格节点）

**继承**: GridNodeBase（网格节点基础）

### 字段 (1)

- `GridGraph[] _gridGraphs`（网格Graph[] _gridGraphs）(偏移: 0x390338E1)

### 方法 (21)

- `GridGraph GetGridGraph(uint graphIndex)`
  （网格Graph 获取网格Graph（uint graphIndex））
- `void SetGridGraph(int graphIndex, GridGraph graph)`
  （void 集合网格Graph（int graphIndex, 网格Graph graph））
- `ushort get_InternalGridFlags()`
  （ushort get_内部的网格Flags（））
- `void set_InternalGridFlags(ushort value)`
  （void set_内部的网格Flags（ushort value））
- `bool get_HasConnectionsToAllEightNeighbours()`
  （bool get_是否有ConnectionsTo所有EightNeighbours（））
- `bool HasConnectionInDirection(int dir)`
  （bool 是否有连接In方向（int dir））
- `bool GetConnectionInternal(int dir)`
  （bool 获取连接内部的（int dir））
- `void SetConnectionInternal(int dir, bool value)`
  （void 集合连接内部的（int dir, bool value））
- `void SetAllConnectionInternal(int connections)`
  （void 集合所有连接内部的（int connections））
- `void ResetConnectionsInternal()`
  （void 重置Connections内部的（））
- `bool get_EdgeNode()`
  （bool get_Edge节点（））
- `void set_EdgeNode(bool value)`
  （void set_Edge节点（bool value））
- `GridNodeBase GetNeighbourAlongDirection(int direction)`
  （网格节点基础 获取NeighbourAlong方向（int direction））
- `void ClearConnections(bool alsoReverse)`
  （void 清除连接（布尔值 也反向））
- `void GetConnections(Action<GraphNode> action)`
  （void 获取连接（Action<GraphNode> action））
- `Vector3 ClosestPointOnNode(Vector3 p)`
  （三维向量 ClosestPointOn节点（三维向量 p））
- `bool GetPortal(GraphNode other, List<Vector3> left, List<Vector3> right, bool backwards)`
  （bool 获取Portal（Graph节点 other, List<Vector3> left, List<Vector3> right, bool backwards））
- `void UpdateRecursiveG(Path path, PathNode pathNode, PathHandler handler)`
  （void 更新递归G（路径 path, 路径节点 pathNode, 路径处理器 handler））
- `void Open(Path path, PathNode pathNode, PathHandler handler)`
  （void 打开（路径 path, 路径节点 pathNode, 路径处理器 handler））
- `void SerializeNode(GraphSerializationContext ctx)`
  （void 序列化节点（图序列化上下文 ctx））
- `void DeserializeNode(GraphSerializationContext ctx)`
  （void 反序列化节点（图序列化上下文 ctx））

---

## GridNodeBase（网格节点基础）

**继承**: GraphNode（Graph节点）

### 字段 (3)

- `int nodeInGridIndex`（int nodeIn网格索引）(偏移: 0x20)
- `ushort gridFlags`（ushort gridFlags）(偏移: 0x24)
- `Connection[] connections`（Connection[] connections）(偏移: 0x28)

### 方法 (21)

- `int get_NodeInGridIndex()`
  （int get_节点In网格索引（））
- `void set_NodeInGridIndex(int value)`
  （void set_节点In网格索引（int value））
- `int get_XCoordinateInGrid()`
  （int get_XCoordinateIn网格（））
- `int get_ZCoordinateInGrid()`
  （int get_ZCoordinateIn网格（））
- `bool get_WalkableErosion()`
  （bool get_WalkableErosion（））
- `void set_WalkableErosion(bool value)`
  （void set_WalkableErosion（bool value））
- `bool get_TmpWalkable()`
  （bool get_TmpWalkable（））
- `void set_TmpWalkable(bool value)`
  （void set_TmpWalkable（bool value））
- `float SurfaceArea()`
  （float SurfaceArea（））
- `Vector3 RandomPointOnSurface()`
  （三维向量 随机PointOnSurface（））
- `int GetGizmoHashCode()`
  （整数 获取辅助线哈希码（））
- `bool ContainsConnection(GraphNode node)`
  （bool Contains连接（Graph节点 node））
- `void ClearCustomConnections(bool alsoReverse)`
  （void 清除自定义的Connections（bool alsoReverse））
- `void ClearConnections(bool alsoReverse)`
  （void 清除连接（布尔值 也反向））
- `void GetConnections(Action<GraphNode> action)`
  （void 获取连接（Action<GraphNode> action））
- `void UpdateRecursiveG(Path path, PathNode pathNode, PathHandler handler)`
  （void 更新递归G（路径 path, 路径节点 pathNode, 路径处理器 handler））
- `void Open(Path path, PathNode pathNode, PathHandler handler)`
  （void 打开（路径 path, 路径节点 pathNode, 路径处理器 handler））
- `void AddConnection(GraphNode node, uint cost)`
  （void 添加连接（Graph节点 node, uint cost））
- `void RemoveConnection(GraphNode node)`
  （void 移除连接（Graph节点 node））
- `void SerializeReferences(GraphSerializationContext ctx)`
  （void 序列化引用（图序列化上下文 ctx））
- `void DeserializeReferences(GraphSerializationContext ctx)`
  （void 反序列化引用（图序列化上下文 ctx））

---

## Grounder（接地器）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (4)

- `float weight`（浮点数 权重）(偏移: 0xC)
- `Grounding solver`（Grounding solver）(偏移: 0x10)
- `Grounder.GrounderDelegate OnPreGrounder`（Grounder.Grounder委托 OnPreGrounder）(偏移: 0x14)
- `Grounder.GrounderDelegate OnPostGrounder`（Grounder.Grounder委托 OnPostGrounder）(偏移: 0x18)

### 方法 (6)

- `bool get_initiated()`
  （布尔值 获取_已启动（））
- `void set_initiated(bool value)`
  （void 设置_已启动（布尔值 value））
- `Vector3 GetSpineOffsetTarget()`
  （三维向量 获取SpineOffset目标（））
- `void LogWarning(string message)`
  （void 记录警告（字符串 message））
- `Vector3 GetLegSpineBendVector(Grounding.Leg leg)`
  （三维向量 获取腿部SpineBend向量（Grounding.腿部 leg））
- `Vector3 GetLegSpineTangent(Grounding.Leg leg)`
  （三维向量 获取腿部SpineTangent（Grounding.腿部 leg））

---

## Grounder.GrounderDelegate（Grounder.Grounder委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke()`
  （void 调用（））
- `IAsyncResult BeginInvoke(AsyncCallback callback, object object)`
  （I异步结果 开始调用（异步回调 callback, 对象 object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## GrounderBipedIK（GrounderBipedIK）

**继承**: Grounder（接地器）

### 字段 (9)

- `BipedIK ik`（BipedIK ik）(偏移: 0x20)
- `float spineBend`（float spineBend）(偏移: 0x24)
- `float spineSpeed`（float spineSpeed）(偏移: 0x28)
- `Transform[] feet`（Transform[] feet）(偏移: 0x2C)
- `Quaternion[] footRotations`（Quaternion[] footRotations）(偏移: 0x30)
- `Vector3 animatedPelvisLocalPosition`（三维向量 animatedPelvis本地的Position）(偏移: 0x34)
- `Vector3 solvedPelvisLocalPosition`（三维向量 solvedPelvis本地的Position）(偏移: 0x40)
- `Vector3 spineOffset`（三维向量 spineOffset）(偏移: 0x4C)
- `float lastWeight`（float lastWeight）(偏移: 0x58)

### 方法 (11)

- `void OpenUserManual()`
  （void 打开用户手动（））
- `void OpenScriptReference()`
  （void 打开脚本引用（））
- `void ResetPosition()`
  （void 重置位置（））
- `bool IsReadyToInitiate()`
  （布尔值 是否准备启动（））
- `void Update()`
  （void 更新（））
- `void Initiate()`
  （void 启动（））
- `void OnDisable()`
  （void 禁用时（））
- `void OnSolverUpdate()`
  （void 求解器更新时（））
- `void SetLegIK(IKSolverLimb limb, int index)`
  （void 集合腿部IK（IKSolverLimb limb, int index））
- `void OnPostSolverUpdate()`
  （void OnPostSolver更新（））
- `void OnDestroy()`
  （void 销毁时（））

---

## GrounderFBBIK（GrounderFBBIK）

**继承**: Grounder（接地器）

### 字段 (7)

- `FullBodyBipedIK ik`（全身双足IK ik）(偏移: 0x20)
- `float spineBend`（float spineBend）(偏移: 0x24)
- `float spineSpeed`（float spineSpeed）(偏移: 0x28)
- `GrounderFBBIK.SpineEffector[] spine`（GrounderFBBIK.SpineEffector[] spine）(偏移: 0x2C)
- `Transform[] feet`（Transform[] feet）(偏移: 0x30)
- `Vector3 spineOffset`（三维向量 spineOffset）(偏移: 0x34)
- `bool firstSolve`（bool firstSolve）(偏移: 0x40)

### 方法 (13)

- `void OpenTutorial()`
  （void 打开Tutorial（））
- `void OpenUserManual()`
  （void 打开用户手动（））
- `void OpenScriptReference()`
  （void 打开脚本引用（））
- `void ResetPosition()`
  （void 重置位置（））
- `bool IsReadyToInitiate()`
  （布尔值 是否准备启动（））
- `void Update()`
  （void 更新（））
- `void FixedUpdate()`
  （void 固定更新（））
- `void LateUpdate()`
  （void 延迟更新（））
- `void Initiate()`
  （void 启动（））
- `void OnSolverUpdate()`
  （void 求解器更新时（））
- `void SetLegIK(IKEffector effector, Grounding.Leg leg)`
  （void 集合腿部IK（IKEffector effector, Grounding.腿部 leg））
- `void OnDrawGizmosSelected()`
  （void 绘制选中辅助线时（））
- `void OnDestroy()`
  （void 销毁时（））

---

## GrounderFBBIK.SpineEffector（GrounderFBBIK.SpineEffector）

### 字段 (3)

- `FullBodyBipedEffector effectorType`（满身体BipedEffector effector类型）(偏移: 0x8)
- `float horizontalWeight`（float horizontalWeight）(偏移: 0xC)
- `float verticalWeight`（float verticalWeight）(偏移: 0x10)

---

## GrounderIK（GrounderIK）

**继承**: Grounder（接地器）

### 字段 (14)

- `IK[] legs`（IK[] legs）(偏移: 0x20)
- `Transform pelvis`（变换 骨盆）(偏移: 0x24)
- `Transform characterRoot`（变换 character根）(偏移: 0x28)
- `float rootRotationWeight`（float rootRotationWeight）(偏移: 0x2C)
- `float rootRotationSpeed`（float rootRotationSpeed）(偏移: 0x30)
- `float maxRootRotationAngle`（float max根Rotation角度）(偏移: 0x34)
- `Transform[] feet`（Transform[] feet）(偏移: 0x38)
- `Quaternion[] footRotations`（Quaternion[] footRotations）(偏移: 0x3C)
- `Vector3 animatedPelvisLocalPosition`（三维向量 animatedPelvis本地的Position）(偏移: 0x40)
- `Vector3 solvedPelvisLocalPosition`（三维向量 solvedPelvis本地的Position）(偏移: 0x4C)
- `int solvedFeet`（int solvedFeet）(偏移: 0x58)
- `bool solved`（bool solved）(偏移: 0x5C)
- `float lastWeight`（float lastWeight）(偏移: 0x60)
- `Rigidbody characterRootRigidbody`（刚体 character根刚体）(偏移: 0x64)

### 方法 (11)

- `void OpenUserManual()`
  （void 打开用户手动（））
- `void OpenScriptReference()`
  （void 打开脚本引用（））
- `void ResetPosition()`
  （void 重置位置（））
- `bool IsReadyToInitiate()`
  （布尔值 是否准备启动（））
- `void OnDisable()`
  （void 禁用时（））
- `void Update()`
  （void 更新（））
- `void Initiate()`
  （void 启动（））
- `void OnSolverUpdate()`
  （void 求解器更新时（））
- `void SetLegIK(int index)`
  （void 集合腿部IK（int index））
- `void OnPostSolverUpdate()`
  （void OnPostSolver更新（））
- `void OnDestroy()`
  （void 销毁时（））

---

## GrounderQuadruped（GrounderQuadruped）

**继承**: Grounder（接地器）

### 字段 (29)

- `Grounding forelegSolver`（Grounding forelegSolver）(偏移: 0x20)
- `float rootRotationWeight`（float rootRotationWeight）(偏移: 0x24)
- `float minRootRotation`（float min根Rotation）(偏移: 0x28)
- `float maxRootRotation`（float max根Rotation）(偏移: 0x2C)
- `float rootRotationSpeed`（float rootRotationSpeed）(偏移: 0x30)
- `float maxLegOffset`（float max腿部Offset）(偏移: 0x34)
- `float maxForeLegOffset`（float maxFore腿部Offset）(偏移: 0x38)
- `float maintainHeadRotationWeight`（float maintain头部RotationWeight）(偏移: 0x3C)
- `Transform characterRoot`（变换 character根）(偏移: 0x40)
- `Transform pelvis`（变换 骨盆）(偏移: 0x44)
- `Transform lastSpineBone`（变换 lastSpineBone）(偏移: 0x48)
- `Transform head`（变换 头部）(偏移: 0x4C)
- `IK[] legs`（IK[] legs）(偏移: 0x50)
- `IK[] forelegs`（IK[] forelegs）(偏移: 0x54)
- `Vector3 gravity`（三维向量 gravity）(偏移: 0x58)
- `GrounderQuadruped.Foot[] feet`（GrounderQuadruped.Foot[] feet）(偏移: 0x64)
- `Vector3 animatedPelvisLocalPosition`（三维向量 animatedPelvis本地的Position）(偏移: 0x68)
- `Quaternion animatedPelvisLocalRotation`（Quaternion animatedPelvis本地的Rotation）(偏移: 0x74)
- `Quaternion animatedHeadLocalRotation`（Quaternion animated头部本地的Rotation）(偏移: 0x84)
- `Vector3 solvedPelvisLocalPosition`（三维向量 solvedPelvis本地的Position）(偏移: 0x94)
- `Quaternion solvedPelvisLocalRotation`（Quaternion solvedPelvis本地的Rotation）(偏移: 0xA0)
- `Quaternion solvedHeadLocalRotation`（Quaternion solved头部本地的Rotation）(偏移: 0xB0)
- `int solvedFeet`（int solvedFeet）(偏移: 0xC0)
- `bool solved`（bool solved）(偏移: 0xC4)
- `float angle`（float angle）(偏移: 0xC8)
- `Transform forefeetRoot`（变换 forefeet根）(偏移: 0xCC)
- `Quaternion headRotation`（Quaternion headRotation）(偏移: 0xD0)
- `float lastWeight`（float lastWeight）(偏移: 0xE0)
- `Rigidbody characterRootRigidbody`（刚体 character根刚体）(偏移: 0xE4)

### 方法 (17)

- `void OpenUserManual()`
  （void 打开用户手动（））
- `void OpenScriptReference()`
  （void 打开脚本引用（））
- `void ResetPosition()`
  （void 重置位置（））
- `bool IsReadyToInitiate()`
  （布尔值 是否准备启动（））
- `bool IsReadyToInitiateLegs(IK[] ikComponents)`
  （bool 是否ReadyToInitiateLegs（IK[] ikComponents））
- `void OnDisable()`
  （void 禁用时（））
- `void Update()`
  （void 更新（））
- `void Initiate()`
  （void 启动（））
- `Transform[] InitiateFeet(IK[] ikComponents, ref GrounderQuadruped.Foot[] f, int indexOffset)`
  （Transform[] InitiateFeet（IK[] ikComponents, ref GrounderQuadruped.Foot[] f, int indexOffset））
- `void LateUpdate()`
  （void 延迟更新（））
- `void RootRotation()`
  （void 根Rotation（））
- `void OnSolverUpdate()`
  （void 求解器更新时（））
- `void UpdateForefeetRoot()`
  （void 更新Forefeet根（））
- `void SetFootIK(GrounderQuadruped.Foot foot, float maxOffset)`
  （void 集合脚部IK（GrounderQuadruped.脚部 foot, float maxOffset））
- `void OnPostSolverUpdate()`
  （void OnPostSolver更新（））
- `void OnDestroy()`
  （void 销毁时（））
- `void DestroyLegs(IK[] ikComponents)`
  （void 销毁Legs（IK[] ikComponents））

---

## GrounderQuadruped.Foot（GrounderQuadruped.脚部）

### 字段 (4)

- `IKSolver solver`（IKSolver solver）(偏移: 0x0)
- `Transform transform`（变换 transform）(偏移: 0x4)
- `Quaternion rotation`（四元数 旋转）(偏移: 0x8)
- `Grounding.Leg leg`（Grounding.腿部 leg）(偏移: 0x18)

---

## GrounderVRIK（GrounderVRIK）

**继承**: Grounder（接地器）

### 字段 (2)

- `VRIK ik`（VRIK ik）(偏移: 0x20)
- `Transform[] feet`（Transform[] feet）(偏移: 0x24)

### 方法 (12)

- `void OpenTutorial()`
  （void 打开Tutorial（））
- `void OpenUserManual()`
  （void 打开用户手动（））
- `void OpenScriptReference()`
  （void 打开脚本引用（））
- `void ResetPosition()`
  （void 重置位置（））
- `bool IsReadyToInitiate()`
  （布尔值 是否准备启动（））
- `void Update()`
  （void 更新（））
- `void Initiate()`
  （void 启动（））
- `void OnSolverUpdate()`
  （void 求解器更新时（））
- `void SetLegIK(IKSolverVR.PositionOffset positionOffset, Transform bone, Grounding.Leg leg)`
  （void 集合腿部IK（IKSolverVR.PositionOffset positionOffset, 变换 bone, Grounding.腿部 leg））
- `void OnPostSolverUpdate()`
  （void OnPostSolver更新（））
- `void OnDrawGizmosSelected()`
  （void 绘制选中辅助线时（））
- `void OnDestroy()`
  （void 销毁时（））

---

## Grounding（Grounding）

### 字段 (19)

- `LayerMask layers`（层掩码 layers）(偏移: 0x8)
- `float maxStep`（float maxStep）(偏移: 0xC)
- `float heightOffset`（float heightOffset）(偏移: 0x10)
- `float footSpeed`（float footSpeed）(偏移: 0x14)
- `float footRadius`（float footRadius）(偏移: 0x18)
- `float footCenterOffset`（float foot中心Offset）(偏移: 0x1C)
- `float prediction`（float prediction）(偏移: 0x20)
- `float footRotationWeight`（float footRotationWeight）(偏移: 0x24)
- `float footRotationSpeed`（float footRotationSpeed）(偏移: 0x28)
- `float maxFootRotationAngle`（float max脚部Rotation角度）(偏移: 0x2C)
- `bool rotateSolver`（bool rotateSolver）(偏移: 0x30)
- `float pelvisSpeed`（float pelvisSpeed）(偏移: 0x34)
- `float pelvisDamper`（float pelvisDamper）(偏移: 0x38)
- `float lowerPelvisWeight`（float lowerPelvisWeight）(偏移: 0x3C)
- `float liftPelvisWeight`（float liftPelvisWeight）(偏移: 0x40)
- `float rootSphereCastRadius`（float rootSphereCastRadius）(偏移: 0x44)
- `bool overstepFallsDown`（bool overstepFalls下）(偏移: 0x48)
- `Grounding.Quality quality`（Grounding.Quality quality）(偏移: 0x4C)
- `bool initiated`（布尔值 已启动）(偏移: 0x8C)

### 方法 (23)

- `Grounding.Leg[] get_legs()`
  （Grounding.Leg[] get_legs（））
- `void set_legs(Grounding.Leg[] value)`
  （void set_legs（Grounding.Leg[] value））
- `Grounding.Pelvis get_pelvis()`
  （Grounding.Pelvis get_pelvis（））
- `void set_pelvis(Grounding.Pelvis value)`
  （void set_pelvis（Grounding.Pelvis value））
- `bool get_isGrounded()`
  （布尔值 获取_是否着地（））
- `void set_isGrounded(bool value)`
  （void set_is着地（bool value））
- `Transform get_root()`
  （变换 get_root（））
- `void set_root(Transform value)`
  （void set_root（变换 value））
- `RaycastHit get_rootHit()`
  （Raycast命中 get_root命中（））
- `void set_rootHit(RaycastHit value)`
  （void set_root命中（Raycast命中 value））
- `bool get_rootGrounded()`
  （bool get_root着地（））
- `RaycastHit GetRootHit(float maxDistanceMlp = 10)`
  （Raycast命中 获取根命中（float maxDistanceMlp = 10））
- `bool IsValid(ref string errorMessage)`
  （bool 是否Valid（ref string errorMessage））
- `void Initiate(Transform root, Transform[] feet)`
  （void Initiate（变换 root, Transform[] feet））
- `void Update()`
  （void 更新（））
- `Vector3 GetLegsPlaneNormal()`
  （三维向量 获取LegsPlane法线（））
- `void Reset()`
  （void 重置（））
- `void LogWarning(string message)`
  （void 记录警告（字符串 message））
- `Vector3 get_up()`
  （三维向量 get_up（））
- `float GetVerticalOffset(Vector3 p1, Vector3 p2)`
  （float 获取垂直Offset（三维向量 p1, 三维向量 p2））
- `Vector3 Flatten(Vector3 v)`
  （三维向量 Flatten（三维向量 v））
- `bool get_useRootRotation()`
  （bool get_use根Rotation（））
- `Vector3 GetFootCenterOffset()`
  （三维向量 获取脚部中心Offset（））

---

## Grounding.Leg（Grounding.腿部）

### 字段 (12)

- `Quaternion rotationOffset`（Quaternion rotationOffset）(偏移: 0x18)
- `bool invertFootCenter`（bool invert脚部中心）(偏移: 0x44)
- `Grounding grounding`（Grounding grounding）(偏移: 0xA0)
- `float lastTime`（浮点数 上次时间）(偏移: 0xA4)
- `float deltaTime`（float delta时间）(偏移: 0xA8)
- `Vector3 lastPosition`（三维向量 最后位置）(偏移: 0xAC)
- `Quaternion toHitNormal`（Quaternion to命中法线）(偏移: 0xB8)
- `Quaternion r`（Quaternion r）(偏移: 0xC8)
- `Vector3 up`（三维向量 up）(偏移: 0xD8)
- `bool doOverrideFootPosition`（bool do重写脚部Position）(偏移: 0xE4)
- `Vector3 overrideFootPosition`（三维向量 override脚部Position）(偏移: 0xE8)
- `Vector3 transformPosition`（三维向量 transformPosition）(偏移: 0xF4)

### 方法 (34)

- `bool get_isGrounded()`
  （布尔值 获取_是否着地（））
- `void set_isGrounded(bool value)`
  （void set_is着地（bool value））
- `Vector3 get_IKPosition()`
  （三维向量 get_IKPosition（））
- `void set_IKPosition(Vector3 value)`
  （void set_IKPosition（三维向量 value））
- `bool get_initiated()`
  （布尔值 获取_已启动（））
- `void set_initiated(bool value)`
  （void 设置_已启动（布尔值 value））
- `float get_heightFromGround()`
  （float get_heightFrom地面（））
- `void set_heightFromGround(float value)`
  （void set_heightFrom地面（float value））
- `Vector3 get_velocity()`
  （三维向量 获取_速度（））
- `void set_velocity(Vector3 value)`
  （void set_velocity（三维向量 value））
- `Transform get_transform()`
  （变换 获取_transform（））
- `void set_transform(Transform value)`
  （void set_transform（变换 value））
- `float get_IKOffset()`
  （float get_IKOffset（））
- `void set_IKOffset(float value)`
  （void set_IKOffset（float value））
- `RaycastHit get_heelHit()`
  （Raycast命中 get_heel命中（））
- `void set_heelHit(RaycastHit value)`
  （void set_heel命中（Raycast命中 value））
- `RaycastHit get_capsuleHit()`
  （Raycast命中 get_capsule命中（））
- `void set_capsuleHit(RaycastHit value)`
  （void set_capsule命中（Raycast命中 value））
- `RaycastHit get_GetHitPoint()`
  （Raycast命中 get_获取命中Point（））
- `void SetFootPosition(Vector3 position)`
  （void 集合脚部Position（三维向量 position））
- `void Initiate(Grounding grounding, Transform transform)`
  （void Initiate（Grounding grounding, 变换 transform））
- `void OnEnable()`
  （void 启用时（））
- `void Reset()`
  （void 重置（））
- `void Process()`
  （void 处理（））
- `float get_stepHeightFromGround()`
  （float get_step高度From地面（））
- `RaycastHit GetCapsuleHit(Vector3 offsetFromHeel)`
  （Raycast命中 获取Capsule命中（三维向量 offsetFromHeel））
- `RaycastHit GetRaycastHit(Vector3 offsetFromHeel)`
  （Raycast命中 获取Raycast命中（三维向量 offsetFromHeel））
- `Vector3 RotateNormal(Vector3 normal)`
  （三维向量 Rotate法线（三维向量 normal））
- `void SetFootToPoint(Vector3 normal, Vector3 point)`
  （void 集合脚部ToPoint（三维向量 normal, 三维向量 point））
- `void SetFootToPlane(Vector3 planeNormal, Vector3 planePoint, Vector3 heelHitPoint)`
  （void 集合脚部ToPlane（三维向量 planeNormal, 三维向量 planePoint, 三维向量 heelHitPoint））
- `float GetHeightFromGround(Vector3 hitPoint)`
  （float 获取高度From地面（三维向量 hitPoint））
- `void RotateFoot()`
  （void Rotate脚部（））
- `Quaternion GetRotationOffsetTarget()`
  （Quaternion 获取RotationOffset目标（））
- `float get_rootYOffset()`
  （float get_rootYOffset（））

---

## Grounding.Pelvis（Grounding.Pelvis）

### 字段 (5)

- `Grounding grounding`（Grounding grounding）(偏移: 0x18)
- `Vector3 lastRootPosition`（三维向量 last根Position）(偏移: 0x1C)
- `float damperF`（float damperF）(偏移: 0x28)
- `bool initiated`（布尔值 已启动）(偏移: 0x2C)
- `float lastTime`（浮点数 上次时间）(偏移: 0x30)

### 方法 (8)

- `Vector3 get_IKOffset()`
  （三维向量 get_IKOffset（））
- `void set_IKOffset(Vector3 value)`
  （void set_IKOffset（三维向量 value））
- `float get_heightOffset()`
  （float get_heightOffset（））
- `void set_heightOffset(float value)`
  （void set_heightOffset（float value））
- `void Initiate(Grounding grounding)`
  （void Initiate（Grounding grounding））
- `void Reset()`
  （void 重置（））
- `void OnEnable()`
  （void 启用时（））
- `void Process(float lowestOffset, float highestOffset, bool isGrounded)`
  （void 处理（float lowestOffset, float highestOffset, bool isGrounded））

---

## Grounding.Quality（Grounding.Quality）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Group（组）

**继承**: Capture（Capture）

### 字段 (4)

- `Group _emptygroup`（组 _emptygroup）(偏移: 0x0)
- `int[] _caps`（int[] _caps）(偏移: 0x14)
- `int _capcount`（int _capcount）(偏移: 0x18)
- `string _name`（string _name）(偏移: 0x1C)

### 方法 (1)

- `bool get_Success()`
  （bool get_Success（））

---

## GroupCollection（组Collection）

**继承**: ICollection, IEnumerable（ICollection, IEnumerable）

### 字段 (3)

- `Match _match`（比赛 _match）(偏移: 0x8)
- `Hashtable _captureMap`（Hashtable _capture映射）(偏移: 0xC)
- `Group[] _groups`（Group[] _groups）(偏移: 0x10)

### 方法 (7)

- `object get_SyncRoot()`
  （对象 获取_同步根（））
- `int get_Count()`
  （整数 获取_数量（））
- `Group get_Item(int groupnum)`
  （组 get_项目（int groupnum））
- `Group GetGroup(int groupnum)`
  （组 获取组（int groupnum））
- `Group GetGroupImpl(int groupnum)`
  （组 获取组Impl（int groupnum））
- `void CopyTo(Array array, int arrayIndex)`
  （void 复制到（数组 array, 整数 arrayIndex））
- `IEnumerator GetEnumerator()`
  （IEnumerator 获取枚举器（））

---

## GroupEnumerator（组Enumerator）

**继承**: IEnumerator（IEnumerator枚举器）

### 字段 (2)

- `GroupCollection _rgc`（组Collection _rgc）(偏移: 0x8)
- `int _curindex`（int _curindex）(偏移: 0xC)

### 方法 (4)

- `bool MoveNext()`
  （布尔值 移动下一个（））
- `object get_Current()`
  （对象 获取_当前（））
- `Capture get_Capture()`
  （Capture get_Capture（））
- `void Reset()`
  （void 重置（））

---

## GroupTrack（组Track）

**继承**: TrackAsset（轨道资产）

### 方法 (2)

- `bool CanCompileClips()`
  （bool 能否CompileClips（））
- `IEnumerable<PlayableBinding> get_outputs()`
  （IEnumerable<可播放绑定> 获取_输出（））

---

## GroupWeightManipulator（组WeightManipulator）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (9)

- `float m_Weight0`（float m_Weight0）(偏移: 0xC)
- `float m_Weight1`（float m_Weight1）(偏移: 0x10)
- `float m_Weight2`（float m_Weight2）(偏移: 0x14)
- `float m_Weight3`（float m_Weight3）(偏移: 0x18)
- `float m_Weight4`（float m_Weight4）(偏移: 0x1C)
- `float m_Weight5`（float m_Weight5）(偏移: 0x20)
- `float m_Weight6`（float m_Weight6）(偏移: 0x24)
- `float m_Weight7`（float m_Weight7）(偏移: 0x28)
- `CinemachineTargetGroup m_group`（Cinemachine目标组 m_group）(偏移: 0x2C)

### 方法 (4)

- `void Start()`
  （void 开始（））
- `void OnValidate()`
  （void 验证时（））
- `void Update()`
  （void 更新（））
- `void UpdateWeights()`
  （void 更新Weights（））

---

## Guid（Guid）

**继承**: IFormattable, IComparable, IComparable<Guid>, IEquatable<Guid>（IFormattable, IComparable, IComparable<Guid>, IEquatable<Guid>）

### 字段 (15)

- `Guid Empty`（Guid 空）(偏移: 0x0)
- `int _a`（int _a）(偏移: 0x0)
- `short _b`（short _b）(偏移: 0x4)
- `short _c`（short _c）(偏移: 0x6)
- `byte _d`（byte _d）(偏移: 0x8)
- `byte _e`（byte _e）(偏移: 0x9)
- `byte _f`（byte _f）(偏移: 0xA)
- `byte _g`（byte _g）(偏移: 0xB)
- `byte _h`（byte _h）(偏移: 0xC)
- `byte _i`（byte _i）(偏移: 0xD)
- `byte _j`（byte _j）(偏移: 0xE)
- `byte _k`（byte _k）(偏移: 0xF)
- `object _rngAccess`（object _rngAccess）(偏移: 0x10)
- `RandomNumberGenerator _rng`（随机NumberGenerator _rng）(偏移: 0x14)
- `RandomNumberGenerator _fastRng`（随机NumberGenerator _fastRng）(偏移: 0x18)

### 方法 (31)

- `Guid Parse(string input)`
  （Guid 解析（string input））
- `bool TryParse(string input, out Guid result)`
  （bool Try解析（string input, out Guid result））
- `bool TryParseGuid(string g, Guid.GuidStyles flags, ref Guid.GuidResult result)`
  （bool Try解析Guid（string g, Guid.GuidStyles flags, ref Guid.GuidResult result））
- `bool TryParseGuidWithHexPrefix(string guidString, ref Guid.GuidResult result)`
  （bool Try解析GuidWithHexPrefix（string guidString, ref Guid.GuidResult result））
- `bool TryParseGuidWithNoStyle(string guidString, ref Guid.GuidResult result)`
  （bool Try解析GuidWithNoStyle（string guidString, ref Guid.GuidResult result））
- `bool TryParseGuidWithDashes(string guidString, ref Guid.GuidResult result)`
  （bool Try解析GuidWithDashes（string guidString, ref Guid.GuidResult result））
- `bool StringToShort(string str, int requiredLength, int flags, out short result, ref Guid.GuidResult parseResult)`
  （bool 字符串ToShort（string str, int requiredLength, int flags, out short result, ref Guid.GuidResult parseResult））
- `bool StringToShort(string str, int* parsePos, int requiredLength, int flags, out short result, ref Guid.GuidResult parseResult)`
  （bool 字符串ToShort（string str, int* parsePos, int requiredLength, int flags, out short result, ref Guid.GuidResult parseResult））
- `bool StringToInt(string str, int requiredLength, int flags, out int result, ref Guid.GuidResult parseResult)`
  （bool 字符串To整数（string str, int requiredLength, int flags, out int result, ref Guid.GuidResult parseResult））
- `bool StringToInt(string str, ref int parsePos, int requiredLength, int flags, out int result, ref Guid.GuidResult parseResult)`
  （bool 字符串To整数（string str, ref int parsePos, int requiredLength, int flags, out int result, ref Guid.GuidResult parseResult））
- `bool StringToInt(string str, int* parsePos, int requiredLength, int flags, out int result, ref Guid.GuidResult parseResult)`
  （bool 字符串To整数（string str, int* parsePos, int requiredLength, int flags, out int result, ref Guid.GuidResult parseResult））
- `bool StringToLong(string str, ref int parsePos, int flags, out long result, ref Guid.GuidResult parseResult)`
  （bool 字符串ToLong（string str, ref int parsePos, int flags, out long result, ref Guid.GuidResult parseResult））
- `bool StringToLong(string str, int* parsePos, int flags, out long result, ref Guid.GuidResult parseResult)`
  （bool 字符串ToLong（string str, int* parsePos, int flags, out long result, ref Guid.GuidResult parseResult））
- `string EatAllWhitespace(string str)`
  （string Eat所有Whitespace（string str））
- `bool IsHexPrefix(string str, int i)`
  （bool 是否HexPrefix（string str, int i））
- `byte[] ToByteArray()`
  （byte[] ToByte数组（））
- `string ToString()`
  （字符串 转字符串（））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `bool Equals(object o)`
  （布尔值 等于（对象 o））
- `bool Equals(Guid g)`
  （bool Equals（Guid g））
- `int GetResult(uint me, uint them)`
  （int 获取Result（uint me, uint them））
- `int CompareTo(object value)`
  （整数 比较到（对象 value））
- `int CompareTo(Guid value)`
  （int CompareTo（Guid value））
- `bool op_Equality(Guid a, Guid b)`
  （bool op_Equality（Guid a, Guid b））
- `bool op_Inequality(Guid a, Guid b)`
  （bool op_Inequality（Guid a, Guid b））
- `string ToString(string format)`
  （字符串 转字符串（字符串 格式））
- `char HexToChar(int a)`
  （char HexToChar（int a））
- `int HexsToChars(char* guidChars, int offset, int a, int b)`
  （int HexsToChars（char* guidChars, int offset, int a, int b））
- `int HexsToChars(char* guidChars, int offset, int a, int b, bool hex)`
  （int HexsToChars（char* guidChars, int offset, int a, int b, bool hex））
- `string ToString(string format, IFormatProvider provider)`
  （字符串 转字符串（字符串 格式, I格式化提供者 provider））
- `Guid NewGuid()`
  （Guid 新的Guid（））

---

## Guid（Guid）

### 字段 (6)

- `Guid zero`（Guid zero）(偏移: 0x0)
- `string zeroString`（string zero字符串）(偏移: 0x10)
- `ulong _a`（ulong _a）(偏移: 0x0)
- `ulong _b`（ulong _b）(偏移: 0x8)
- `Random random`（随机 random）(偏移: 0x14)
- `StringBuilder text`（字符串构建器 text）(偏移: 0x18)

### 方法 (9)

- `Guid Parse(string input)`
  （Guid 解析（string input））
- `ulong SwapEndianness(ulong value)`
  （ulong SwapEndianness（ulong value））
- `byte[] ToByteArray()`
  （byte[] ToByte数组（））
- `Guid NewGuid()`
  （Guid 新的Guid（））
- `bool op_Equality(Guid lhs, Guid rhs)`
  （bool op_Equality（Guid lhs, Guid rhs））
- `bool op_Inequality(Guid lhs, Guid rhs)`
  （bool op_Inequality（Guid lhs, Guid rhs））
- `bool Equals(object _rhs)`
  （bool Equals（object _rhs））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `string ToString()`
  （字符串 转字符串（））

---

## Guid.GuidParseThrowStyle（Guid.Guid解析投掷Style）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Guid.GuidResult（Guid.GuidResult）

### 字段 (7)

- `Guid parsedGuid`（Guid parsedGuid）(偏移: 0x0)
- `Guid.GuidParseThrowStyle throwStyle`（Guid.Guid解析投掷Style throwStyle）(偏移: 0x10)
- `Guid.ParseFailureKind m_failure`（Guid.解析FailureKind m_failure）(偏移: 0x14)
- `string m_failureMessageID`（string m_failureMessageID）(偏移: 0x18)
- `object m_failureMessageFormatArgument`（object m_failureMessage格式化Argument）(偏移: 0x1C)
- `string m_failureArgumentName`（string m_failureArgument名称）(偏移: 0x20)
- `Exception m_innerException`（Exception m_innerException）(偏移: 0x24)

### 方法 (6)

- `void Init(Guid.GuidParseThrowStyle canThrow)`
  （void 初始化（Guid.Guid解析投掷Style canThrow））
- `void SetFailure(Exception nativeException)`
  （void 集合Failure（Exception nativeException））
- `void SetFailure(Guid.ParseFailureKind failure, string failureMessageID)`
  （void 集合Failure（Guid.解析FailureKind failure, string failureMessageID））
- `void SetFailure(Guid.ParseFailureKind failure, string failureMessageID, object failureMessageFormatArgument)`
  （void 集合Failure（Guid.解析FailureKind failure, string failureMessageID, object failureMessageFormatArgument））
- `void SetFailure(Guid.ParseFailureKind failure, string failureMessageID, object failureMessageFormatArgument, string failureArgumentName, Exception innerException)`
  （void 集合Failure（Guid.解析FailureKind failure, string failureMessageID, object failureMessageFormatArgument, string failureArgumentName, Exception innerException））
- `Exception GetGuidParseException()`
  （Exception 获取Guid解析Exception（））

---

## Guid.GuidStyles（Guid.GuidStyles）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Guid.ParseFailureKind（Guid.解析FailureKind）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## GuidArrayTypeInfo（Guid数组类型信息）

**继承**: TraceLoggingTypeInfo<Guid[]>（TraceLogging类型Info<Guid[]>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void 写入元数据（跟踪日志元数据收集器 collector, 字符串 name, 事件字段格式 format））
- `void WriteData(TraceLoggingDataCollector collector, ref Guid[] value)`
  （void Write数据（TraceLogging数据Collector collector, ref Guid[] value））

---

## GuidAttribute（GuidAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `string _val`（string _val）(偏移: 0x8)

---

## GuidTypeInfo（Guid类型信息）

**继承**: TraceLoggingTypeInfo<Guid>（TraceLogging类型Info<Guid>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void 写入元数据（跟踪日志元数据收集器 collector, 字符串 name, 事件字段格式 format））
- `void WriteData(TraceLoggingDataCollector collector, ref Guid value)`
  （void Write数据（TraceLogging数据Collector collector, ref Guid value））

---

## HLSLArray（HLSL数组）

**继承**: Attribute（属性）

### 字段 (2)

- `int arraySize`（int array大小）(偏移: 0x8)
- `Type elementType`（类型 element类型）(偏移: 0xC)

---

## HMAC（HMAC）

**继承**: KeyedHashAlgorithm（KeyedHashAlgorithm）

### 字段 (7)

- `int blockSizeValue`（int block大小值）(偏移: 0x1C)
- `string m_hashName`（string m_hash名称）(偏移: 0x20)
- `HashAlgorithm m_hash1`（HashAlgorithm m_hash1）(偏移: 0x24)
- `HashAlgorithm m_hash2`（HashAlgorithm m_hash2）(偏移: 0x28)
- `byte[] m_inner`（byte[] m_inner）(偏移: 0x2C)
- `byte[] m_outer`（byte[] m_outer）(偏移: 0x30)
- `bool m_hashing`（bool m_hashing）(偏移: 0x34)

### 方法 (9)

- `int get_BlockSizeValue()`
  （int get_Block大小值（））
- `void set_BlockSizeValue(int value)`
  （void set_Block大小值（int value））
- `void UpdateIOPadBuffers()`
  （void 更新IOPadBuffers（））
- `void InitializeKey(byte[] key)`
  （void 初始化键（byte[] key））
- `byte[] get_Key()`
  （字节[] 获取_键（））
- `void Initialize()`
  （void 初始化（））
- `void HashCore(byte[] rgb, int ib, int cb)`
  （void HashCore（byte[] rgb, int ib, int cb））
- `byte[] HashFinal()`
  （字节[] 哈希最终（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））

---

## HMACSHA384（HMACSHA384）

**继承**: HMAC（HMAC）

### 字段 (1)

- `bool m_useLegacyBlockSize`（bool m_useLegacyBlock大小）(偏移: 0x38)

### 方法 (1)

- `int get_BlockSize()`
  （int get_Block大小（））

---

## HMACSHA512（HMACSHA512）

**继承**: HMAC（HMAC）

### 字段 (1)

- `bool m_useLegacyBlockSize`（bool m_useLegacyBlock大小）(偏移: 0x38)

### 方法 (1)

- `int get_BlockSize()`
  （int get_Block大小（））

---

## HUD_Bag（HUD_背包）

**继承**: Singleton<HUD_Bag>（Singleton<HUD_Bag>）

### 字段 (9)

- `HUD_BagButton[] buttons`（HUD_背包Button[] buttons）(偏移: 0xC)
- `RawImage[] weaponIcons`（RawImage[] weaponIcons）(偏移: 0x10)
- `GameObject[] vvipBG`（游戏Object[] vvipBG）(偏移: 0x14)
- `Texture[][] iconTextures`（Texture[][] iconTextures）(偏移: 0x18)
- `bool[][] isVVIP`（bool[][] isVVIP）(偏移: 0x1C)
- `RectTransform bagIcon`（Rect变换 bag图标）(偏移: 0x20)
- `Text bagIndexText`（文本 bag索引文本）(偏移: 0x24)
- `int browseBagID`（int browse背包ID）(偏移: 0x28)
- `WeaponBag bag`（武器背包 bag）(偏移: 0x2C)

### 方法 (8)

- `void Awake()`
  （void 唤醒（））
- `void PlayerController_FocusHUD_Listenner(ref string hud)`
  （void 玩家控制器_聚焦HUD_监听器（引用 字符串 hud））
- `void Update()`
  （void 更新（））
- `void MyPlayerJoin(Player player)`
  （void My玩家Join（玩家 player））
- `void SetVisible(bool visible)`
  （void 设置可见（布尔值 visible））
- `void Initialize()`
  （void 初始化（））
- `void FocusBag(int bagID)`
  （void 聚焦背包（int bagID））
- `void SelectBag(int bagID)`
  （void 选择背包（int bagID））

---

## HUD_BagButton（HUD_背包按钮）

**继承**: MonoBehaviour, IPointerEnterHandler, IEventSystemHandler, IPointerDownHandler（MonoBehaviour行为, I指针Enter处理器, I事件系统处理器, I指针下处理器）

### 字段 (4)

- `int bagIndex`（int bag索引）(偏移: 0xC)
- `Sprite normalSprite`（精灵 normal精灵）(偏移: 0x10)
- `Sprite focusSprite`（精灵 focus精灵）(偏移: 0x14)
- `Image image`（图像 image）(偏移: 0x18)

### 方法 (4)

- `void ChangeNormalImage()`
  （void Change法线图像（））
- `void ChangeFocusImage()`
  （void Change聚焦图像（））
- `void OnPointerEnter(PointerEventData eventData)`
  （void On指针Enter（指针事件数据 eventData））
- `void OnPointerDown(PointerEventData eventData)`
  （void 指针按下时（指针事件数据 eventData））

---

## HUD_ChatBox（HUD_ChatBox）

**继承**: Singleton<HUD_ChatBox>（Singleton<HUD_ChatBox>）

### 字段 (15)

- `InputField inputField`（输入Field inputField）(偏移: 0xC)
- `RectTransform msgMask`（Rect变换 msg掩码）(偏移: 0x10)
- `float tempMsgMaskHeight`（float tempMsg掩码高度）(偏移: 0x14)
- `Text msgText`（文本 msg文本）(偏移: 0x18)
- `Text tempMsgText`（文本 tempMsg文本）(偏移: 0x1C)
- `bool firstMsg`（bool firstMsg）(偏移: 0x20)
- `Queue<HUD_ChatBox.MsgMaskRectData> maskDataQueue`（Queue<HUD_ChatBox.Msg掩码RectData> mask数据队列）(偏移: 0x24)
- `string color_JoinGame`（string color_Join游戏）(偏移: 0x0)
- `string color_ExitGame`（string color_Exit游戏）(偏移: 0x4)
- `string color_Radio`（string color_Radio）(偏移: 0x8)
- `string color_System`（string color_系统）(偏移: 0xC)
- `string color_Normal`（string color_法线）(偏移: 0x10)
- `string color_Teammate`（string color_Teammate）(偏移: 0x14)
- `string color_VIP`（string color_VIP）(偏移: 0x18)
- `string[] gameTip`（string[] gameTip）(偏移: 0x28)

### 方法 (14)

- `void Awake()`
  （void 唤醒（））
- `void PlayerController_FocusHUD_Listenner(ref string hud)`
  （void 玩家控制器_聚焦HUD_监听器（引用 字符串 hud））
- `void Update()`
  （void 更新（））
- `void AddSimpleMsg(string color, string msg)`
  （void 添加SimpleMsg（string color, string msg））
- `void MsgMaskHeightUpdate()`
  （void Msg掩码高度更新（））
- `void MsgMaskHeightSetting()`
  （void Msg掩码高度设置（））
- `void OnPlayerJoinGame(Player newPlayer)`
  （void On玩家Join游戏（玩家 newPlayer））
- `void OnPlayerInputText(string text)`
  （void On玩家输入文本（string text））
- `void SetVisible(bool visible)`
  （void 设置可见（布尔值 visible））
- `void TryGetWpnCommand(int wpnIndex)`
  （void Try获取武器Command（int wpnIndex））
- `void TryBecomeGhostBlade()`
  （void TryBecome幽灵刀锋（））
- `void TryBecomeArmoredTerminator()`
  （void TryBecomeArmoredTerminator（））
- `void TryBecomeMasterHero()`
  （void TryBecomeMaster英雄（））
- `void GameTip()`
  （void 游戏Tip（））

---

## HUD_ChatBox.Channel（HUD_ChatBox.Channel）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## HUD_ChatBox.MsgMaskRectData（HUD_ChatBox.Msg掩码Rect数据）

### 字段 (2)

- `float time`（float time）(偏移: 0x0)
- `float height`（浮点数 高度）(偏移: 0x4)

---

## HUD_Cheat（HUD_Cheat）

**继承**: Singleton<HUD_Cheat>（Singleton<HUD_Cheat>）

### 字段 (8)

- `RectTransform mainRect`（Rect变换 mainRect）(偏移: 0xC)
- `GameObject choicePrefab`（游戏对象 choice预制体）(偏移: 0x10)
- `SimpleObjectPool pool`（Simple对象池 pool）(偏移: 0x14)
- `List<HUD_CheatChoice> curChoiceList`（List<HUD_CheatChoice> curChoice列表）(偏移: 0x18)
- `Texture[] buttonTexs`（Texture[] buttonTexs）(偏移: 0x1C)
- `ChoiceBase[] originMenu`（ChoiceBase[] origin菜单）(偏移: 0x20)
- `ChoiceBase[] curMenu`（ChoiceBase[] cur菜单）(偏移: 0x24)
- `Radio nanoRoleMenu`（Radio nanoRole菜单）(偏移: 0x28)

### 方法 (13)

- `Player get_myPlayer()`
  （玩家 get_my玩家（））
- `int get_NanoRoleChoice()`
  （int get_纳米RoleChoice（））
- `void Awake()`
  （void 唤醒（））
- `void SetVisible(bool visible)`
  （void 设置可见（布尔值 visible））
- `void RefreshAnim()`
  （void 刷新动画（））
- `void InitChoice()`
  （void 初始化Choice（））
- `void PlayerController_FocusHUD_Listenner(ref string value)`
  （void 玩家Controller_聚焦HUD_Listenner（ref string value））
- `void ResetChoice(ChoiceBase[] choices)`
  （void 重置Choice（ChoiceBase[] choices））
- `void UpdateInvincible(bool value)`
  （void 更新Invincible（bool value））
- `void TryBecomeSavior()`
  （void TryBecomeSavior（））
- `void TryBecomeHero(NanoRole role)`
  （void TryBecome英雄（纳米角色 role））
- `void TryBecomeTerminator(NanoRole role)`
  （void TryBecomeTerminator（纳米角色 role））
- `void TryGiveWeapon(int wpnID)`
  （void TryGiveWeapon（int wpnID））

---

## HUD_CheatChoice（HUD_CheatChoice）

**继承**: RecyclableObject（可回收对象）

### 字段 (3)

- `RectTransform rect`（矩形变换 rect）(偏移: 0x30)
- `RawImage rawImg`（Raw图像 rawImg）(偏移: 0x34)
- `Text choiceText`（文本 choice文本）(偏移: 0x38)

### 方法 (3)

- `void set_isFocus(bool value)`
  （void set_is聚焦（bool value））
- `void SetText(string str)`
  （void 集合文本（string str））
- `void SetPos(int pos)`
  （void 集合Pos（int pos））

---

## HUD_CommonMsg（HUD_CommonMsg）

**继承**: Singleton<HUD_CommonMsg>（Singleton<HUD_CommonMsg>）

### 字段 (10)

- `GameObject msgBox`（游戏对象 msgBox）(偏移: 0xC)
- `Text msgText`（文本 msg文本）(偏移: 0x10)
- `float msgBoxHideTime`（float msgBox隐藏时间）(偏移: 0x14)
- `RectTransform triggerTipRect`（Rect变换 triggerTipRect）(偏移: 0x18)
- `Image triggerTip`（图像 triggerTip）(偏移: 0x1C)
- `CommonHud_1 modeTipText`（CommonHud_1 modeTip文本）(偏移: 0x20)
- `HUD_Gauge settingGauge`（HUD_Gauge settingGauge）(偏移: 0x24)
- `CommonHud_1 wpnModeTip_RepeatFire`（CommonHud_1 武器模式Tip_Repeat开火）(偏移: 0x28)
- `CommonHud_1 wpnModeTip_GrenadeGun`（CommonHud_1 武器模式Tip_手雷枪械）(偏移: 0x2C)
- `float mouseSpeedStartContinuousAdjustTime`（float mouseSpeed开始ContinuousAdjust时间）(偏移: 0x30)

### 方法 (9)

- `void Awake()`
  （void 唤醒（））
- `void Start()`
  （void 开始（））
- `void ShowModeTipText()`
  （void 显示模式Tip文本（））
- `void Update()`
  （void 更新（））
- `void ShowMsgBox(string msg, float showTime = 2, bool cancelSameMsgSnd = True)`
  （void 显示MsgBox（string msg, float showTime = 2, bool cancelSameMsgSnd = True））
- `void SetTriggerTip(Sprite sprite)`
  （void 集合触发器Tip（精灵 sprite））
- `bool MouseSpeedAdjust()`
  （bool 鼠标SpeedAdjust（））
- `void ShowTip_GrenadeGunMode(bool isOpen)`
  （void 显示Tip_手雷枪械模式（bool isOpen））
- `void ShowTip_RepeatFireMode(bool isOpen)`
  （void 显示Tip_Repeat开火模式（bool isOpen））

---

## HUD_Crosshair（HUD_准星）

**继承**: Singleton<HUD_Crosshair>（Singleton<HUD_Crosshair>）

### 字段 (14)

- `RectTransform sniperCross`（Rect变换 sniperCross）(偏移: 0xC)
- `Image sniperCrossBackGround`（图像 sniperCross后地面）(偏移: 0x10)
- `RectTransform hitRect`（Rect变换 hitRect）(偏移: 0x14)
- `float nextHitAnimAllowedTime`（float next命中动画Allowed时间）(偏移: 0x0)
- `bool hideCrosshair`（bool hide准星）(偏移: 0x4)
- `Player player`（玩家 player）(偏移: 0x18)
- `GameObject[] allCrosshair`（游戏Object[] all准星）(偏移: 0x1C)
- `RectTransform crosshair1_horizontal`（Rect变换 crosshair1_horizontal）(偏移: 0x20)
- `RectTransform crosshair1_vertical`（Rect变换 crosshair1_vertical）(偏移: 0x24)
- `HUD_Crosshair.Type curCrosshairType`（HUD_Crosshair.类型 cur准星类型）(偏移: 0x28)
- `Text[] zoomTargetTexts`（Text[] zoom目标Texts）(偏移: 0x2C)
- `List<RaycastHit> zoomRaycastTemp`（List<RaycastHit> zoomRaycastTemp）(偏移: 0x30)
- `Color color_ZoomTeammate`（颜色 color_瞄准Teammate）(偏移: 0x8)
- `Color color_ZoomEnemy`（颜色 color_瞄准Enemy）(偏移: 0x18)

### 方法 (10)

- `void Awake()`
  （void 唤醒（））
- `void Start()`
  （void 开始（））
- `void Update()`
  （void 更新（））
- `void ZoomTargetNameUpdate()`
  （void 瞄准目标名称更新（））
- `void OnDestroy()`
  （void 销毁时（））
- `void SetSniperCrossVisible(bool visible)`
  （void 集合狙击Cross可见的（bool visible））
- `void DamageEvent(ref DamageEventData eventData)`
  （void 伤害事件（ref DamageEventData eventData））
- `void FocusPlayerChangeEvent(Player oldPlayer, Player newPlayer)`
  （void 聚焦玩家Change事件（玩家 oldPlayer, 玩家 newPlayer））
- `void CheckSniperZoomImage()`
  （void 检查狙击瞄准图像（））
- `void SetType(HUD_Crosshair.Type crosshairType)`
  （void 集合类型（HUD_Crosshair.类型 crosshairType））

---

## HUD_Crosshair.Type（HUD_Crosshair.类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## HUD_DamageArrow（HUD_伤害Arrow）

**继承**: Singleton<HUD_DamageArrow>（Singleton<HUD_伤害Arrow>）

### 字段 (5)

- `Image image`（图像 image）(偏移: 0xC)
- `RectTransform rectTransform`（Rect变换 rect变换）(偏移: 0x10)
- `float hideTime`（float hide时间）(偏移: 0x14)
- `Color imageColor`（颜色 image颜色）(偏移: 0x18)
- `Vector3 damageOrigin`（三维向量 damageOrigin）(偏移: 0x28)

### 方法 (4)

- `void Awake()`
  （void 唤醒（））
- `void Update()`
  （void 更新（））
- `void Start()`
  （void 开始（））
- `void DamageEvent(ref DamageEventData eventData)`
  （void 伤害事件（ref DamageEventData eventData））

---

## HUD_EscMenu（HUD_Esc菜单）

**继承**: Singleton<HUD_EscMenu>（Singleton<HUD_EscMenu>）

### 字段 (1)

- `GameObject exitMsgWnd`（游戏对象 exitMsgWnd）(偏移: 0xC)

### 方法 (7)

- `void Awake()`
  （void 唤醒（））
- `void Update()`
  （void 更新（））
- `void PlayerController_FocusHUD_Listenner(ref string hud)`
  （void 玩家控制器_聚焦HUD_监听器（引用 字符串 hud））
- `void OnCloseMenuBtnDown()`
  （void On关闭菜单Btn下（））
- `void OnGameEndBtnDown()`
  （void On游戏结束Btn下（））
- `void SureGameEnd()`
  （void Sure游戏结束（））
- `void CancelGameEnd()`
  （void 取消游戏结束（））

---

## HUD_GameResult（HUD_游戏Result）

**继承**: Singleton<HUD_GameResult>（Singleton<HUD_游戏Result>）

### 字段 (2)

- `Image image`（图像 image）(偏移: 0xC)
- `Sprite[] sprites`（Sprite[] sprites）(偏移: 0x10)

### 方法 (3)

- `void Awake()`
  （void 唤醒（））
- `void Show(int index)`
  （void 显示（int index））
- `void Hide()`
  （void 隐藏（））

---

## HUD_Gauge（HUD_Gauge）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (9)

- `float startTime`（float start时间）(偏移: 0xC)
- `float totalTime`（float total时间）(偏移: 0x10)
- `float hideTime`（float hide时间）(偏移: 0x14)
- `float curProgress`（float curProgress）(偏移: 0x18)
- `RectTransform progressRect`（Rect变换 progressRect）(偏移: 0x1C)
- `float minLength`（float minLength）(偏移: 0x20)
- `float progressLength`（float progressLength）(偏移: 0x24)
- `Text progressText`（文本 progress文本）(偏移: 0x28)
- `Text introduction`（文本 introduction）(偏移: 0x2C)

### 方法 (6)

- `void OnDisable()`
  （void 禁用时（））
- `void Update()`
  （void 更新（））
- `void SetProgress(float progress)`
  （void 集合Progress（float progress））
- `void SetIntroduction(string text)`
  （void 集合Introduction（string text））
- `void Play(float totalTime)`
  （void 播放（float totalTime））
- `void Show(float showTime = 3)`
  （void 显示（float showTime = 3））

---

## HUD_GaugeSystem（HUD_Gauge系统）

**继承**: Singleton<HUD_GaugeSystem>（Singleton<HUD_GaugeSystem>）

### 方法 (2)

- `HUD_Gauge GetGauge(GameObject prefab)`
  （HUD_Gauge 获取Gauge（游戏对象 prefab））
- `bool BreakGauge(string gaugeName)`
  （bool BreakGauge（string gaugeName））

---

## HUD_Gauge_EvilFire（HUD_Gauge_Evil开火）

**继承**: HUD_Gauge（HUD_Gauge）

### 字段 (6)

- `Color color1`（颜色 color1）(偏移: 0x30)
- `Color color2`（颜色 color2）(偏移: 0x40)
- `RawImage gaugeImage`（Raw图像 gauge图像）(偏移: 0x50)
- `GameObject gaugeLight`（游戏对象 gauge光照）(偏移: 0x54)
- `bool useColor2`（bool useColor2）(偏移: 0x58)
- `float nextChangeColorTime`（float nextChange颜色时间）(偏移: 0x5C)

### 方法 (3)

- `void OnDisable()`
  （void 禁用时（））
- `void Update()`
  （void 更新（））
- `void Play(float maxPowerTime, float lastestShootTime)`
  （void 播放（float maxPowerTime, float lastestShootTime））

---

## HUD_HealthBar（HUD_HealthBar）

**继承**: HUD_ProjectionSign（HUD_投影标志）

### 字段 (3)

- `Text entityName`（文本 entity名称）(偏移: 0x50)
- `Image bar`（图像 bar）(偏移: 0x54)
- `HealthData health`（Health数据 health）(偏移: 0x58)

### 方法 (3)

- `void Update()`
  （void 更新（））
- `void SetGraphVisible(bool visible)`
  （void 集合Graph可见的（bool visible））
- `void Bind(Entity entity)`
  （void Bind（实体 entity））

---

## HUD_HeartBeatRadar（HUD_HeartBeatRadar）

**继承**: Singleton<HUD_HeartBeatRadar>（Singleton<HUD_HeartBeatRadar>）

### 字段 (10)

- `bool open`（bool open）(偏移: 0xC)
- `RectTransform heartBeatWave`（Rect变换 heartBeatWave）(偏移: 0x10)
- `List<Player> checkedEnemy`（List<Player> checkedEnemy）(偏移: 0x14)
- `bool scaleAnim`（bool scale动画）(偏移: 0x18)
- `float startScanTime`（float startScan时间）(偏移: 0x1C)
- `AudioClip heartBeatSnd`（音频弹匣 heartBeatSnd）(偏移: 0x20)
- `float nextSndTime`（float nextSnd时间）(偏移: 0x24)
- `GameObject hearBeatPrefab`（游戏对象 hearBeat预制体）(偏移: 0x28)
- `SimpleObjectPool pool`（Simple对象池 pool）(偏移: 0x2C)
- `CommonHud_1 radarEffect`（CommonHud_1 radar特效）(偏移: 0x30)

### 方法 (6)

- `void Start()`
  （void 开始（））
- `void Update()`
  （void 更新（））
- `void AddHeartBeatIcon(Player player)`
  （void 添加HeartBeat图标（玩家 player））
- `float GetScanDuration()`
  （float 获取Scan持续时间（））
- `IEnumerator ScaleAnimation()`
  （IEnumerator 缩放动画（））
- `void PlayRadarEffect()`
  （void 播放Radar特效（））

---

## HUD_KillMark（HUD_击杀Mark）

**继承**: Singleton<HUD_KillMark>（Singleton<HUD_击杀Mark>）

### 字段 (11)

- `KillMarkAsset asset`（击杀标记资产 asset）(偏移: 0xC)
- `CommonKillMark commonMark`（Common击杀Mark commonMark）(偏移: 0x10)
- `RectTransform multiKillEffect`（Rect变换 multi击杀特效）(偏移: 0x14)
- `RawImage multiKillEffectImage`（Raw图像 multi击杀特效图像）(偏移: 0x18)
- `CommonKillMark specialKill`（Common击杀Mark special击杀）(偏移: 0x1C)
- `AudioSource voiceAudioSource`（音频Source voice音频Source）(偏移: 0x20)
- `CharacterVoice voiceAsset`（角色语音 voice资产）(偏移: 0x24)
- `int FirstKill`（int 第一个击杀）(偏移: 0x0)
- `int LastKill`（int 最后一个击杀）(偏移: 0x4)
- `int Revenge`（int 复仇）(偏移: 0x8)
- `HUD_KillMark.KillMarkEvent KillMarkEvent_Listener`（HUD_击杀Mark.击杀Mark事件 击杀MarkEvent_监听器）(偏移: 0xC)

### 方法 (6)

- `void Start()`
  （void 开始（））
- `void OnDestroy()`
  （void 销毁时（））
- `void PlayCommonMark(HUD_KillMark.ShowType showType, int multiKill, HeadShotType headShot, bool wallThrough, DamageType damageType, bool isVVIP)`
  （void 播放CommonMark（HUD_击杀Mark.显示类型 showType, int multiKill, 头部射击类型 headShot, bool wallThrough, 伤害类型 damageType, bool isVVIP））
- `void PlayCommonMark(Texture tex)`
  （void 播放CommonMark（纹理 tex））
- `void PlayMultiKillEffect()`
  （void 播放多个击杀特效（））
- `void DeathEvent(DeathEventData eventData)`
  （void 死亡事件（死亡事件数据 eventData））

---

## HUD_KillMark.EventData（HUD_击杀Mark.事件数据）

### 字段 (5)

- `Player killer`（玩家 killer）(偏移: 0x0)
- `Player dead`（玩家 dead）(偏移: 0x4)
- `int multiKill`（int multi击杀）(偏移: 0x8)
- `HUD_KillMark.ShowType showType`（HUD_击杀Mark.显示类型 show类型）(偏移: 0xC)
- `DamageType dmgType`（伤害类型 dmg类型）(偏移: 0x10)

---

## HUD_KillMark.KillMarkEvent（HUD_击杀Mark.击杀Mark事件）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(ref HUD_KillMark.EventData killMarkEvtData)`
  （void Invoke（ref HUD_KillMark.EventData killMarkEvtData））
- `IAsyncResult BeginInvoke(ref HUD_KillMark.EventData killMarkEvtData, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（ref HUD_KillMark.EventData killMarkEvtData, 异步回调 callback, object object））
- `void EndInvoke(ref HUD_KillMark.EventData killMarkEvtData, IAsyncResult result)`
  （void 结束Invoke（ref HUD_KillMark.EventData killMarkEvtData, I异步Result result））

---

## HUD_KillMark.ShowType（HUD_击杀Mark.显示类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## HUD_KillMarkUnder（HUD_击杀MarkUnder）

**继承**: Singleton<HUD_KillMarkUnder>（Singleton<HUD_击杀MarkUnder>）

### 字段 (5)

- `GameObject prefab`（游戏对象 预制体）(偏移: 0xC)
- `Sprite[] sprites`（Sprite[] sprites）(偏移: 0x10)
- `List<Image> markList`（List<Image> mark列表）(偏移: 0x14)
- `int currentCount`（int current数量）(偏移: 0x0)
- `int tenCounter`（int tenCounter）(偏移: 0x4)

### 方法 (3)

- `void Awake()`
  （void 唤醒（））
- `void AddMark(HUD_KillMarkUnder.Type type)`
  （void 添加Mark（HUD_击杀MarkUnder.类型 type））
- `void Shrink()`
  （void Shrink（））

---

## HUD_KillMarkUnder.Type（HUD_击杀MarkUnder.类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## HUD_KillMsg（HUD_击杀Msg）

**继承**: Singleton<HUD_KillMsg>（Singleton<HUD_击杀Msg>）

### 字段 (17)

- `List<HUD_KillMsgIndividual> spareMsg`（List<HUD_击杀MsgIndividual> spareMsg）(偏移: 0xC)
- `List<HUD_KillMsgIndividual> busyMsg`（List<HUD_击杀MsgIndividual> busyMsg）(偏移: 0x10)
- `Queue<float> refreshTime`（Queue<float> refresh时间）(偏移: 0x14)
- `Sprite[] headshotIcon`（Sprite[] headshot图标）(偏移: 0x18)
- `Sprite[] wallThroughIcon`（Sprite[] wallThrough图标）(偏移: 0x1C)
- `Sprite[] mulltiKillIcon`（Sprite[] mullti击杀图标）(偏移: 0x20)
- `Sprite[] firstAndLastKillIcon`（Sprite[] firstAnd最后一个击杀图标）(偏移: 0x24)
- `Sprite nanoKillHeroIcon`（精灵 nano击杀英雄图标）(偏移: 0x28)
- `Sprite nanoMeleeDeathIcon`（精灵 nanoMelee死亡图标）(偏移: 0x2C)
- `Material additiveMaterial`（材质 additive材质）(偏移: 0x30)
- `Color vvipFlashColor`（颜色 vvipFlash颜色）(偏移: 0x0)
- `Color color_BL`（颜色 color_BL）(偏移: 0x10)
- `Color color_GR`（颜色 color_GR）(偏移: 0x20)
- `Color color_NanoGhost`（颜色 color_纳米幽灵）(偏移: 0x30)
- `Color color_Human`（颜色 color_人类）(偏移: 0x40)
- `Color color_DM_Me`（颜色 color_DM_Me）(偏移: 0x50)
- `Color color_DM_Other`（颜色 color_DM_Other）(偏移: 0x60)

### 方法 (7)

- `void Start()`
  （void 开始（））
- `void Update()`
  （void 更新（））
- `void DeathEvent(DeathEventData data)`
  （void 死亡事件（死亡事件数据 data））
- `void NanoInfect(string nanoName, string soldierName, Sprite icon)`
  （void 纳米Infect（string nanoName, string soldierName, 精灵 icon））
- `void AddMsg(string killerName, Color killerColor, string deadName, Color deadColor, Sprite icon, bool isVVIP, HeadShotType headShot, bool wallThrough, SpecialKillType specialKill, NanoKillType nanoKill, int multiKill)`
  （void 添加Msg（string killerName, 颜色 killerColor, string deadName, 颜色 deadColor, 精灵 icon, bool isVVIP, 头部射击类型 headShot, bool wallThrough, 特殊击杀类型 specialKill, 纳米击杀类型 nanoKill, int multiKill））
- `HUD_KillMsgIndividual GetMsg()`
  （HUD_击杀MsgIndividual 获取Msg（））
- `Color GetColor(Player player)`
  （颜色 获取颜色（玩家 player））

---

## HUD_KillMsgIndividual（HUD_击杀MsgIndividual）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (12)

- `RectTransform mainTransform`（Rect变换 main变换）(偏移: 0xC)
- `Text deathText`（文本 death文本）(偏移: 0x10)
- `RectTransform iconTransform`（Rect变换 icon变换）(偏移: 0x14)
- `Image iconImage`（图像 icon图像）(偏移: 0x18)
- `RectTransform killerTransform`（Rect变换 killer变换）(偏移: 0x1C)
- `Text killerText`（文本 killer文本）(偏移: 0x20)
- `Image nanoKillTypeImage`（图像 nano击杀类型图像）(偏移: 0x24)
- `RectTransform killTypeTransform1`（Rect变换 kill类型Transform1）(偏移: 0x28)
- `Image killType1`（图像 killType1）(偏移: 0x2C)
- `RectTransform killTypeTransform2`（Rect变换 kill类型Transform2）(偏移: 0x30)
- `Image killType2`（图像 killType2）(偏移: 0x34)
- `bool isVVIP`（bool isVVIP）(偏移: 0x38)

### 方法 (1)

- `void Update()`
  （void 更新（））

---

## HUD_KillerSign（HUD_击杀者标志）

**继承**: HUD_ProjectionSign（HUD_投影标志）

### 字段 (1)

- `float hideTime`（float hide时间）(偏移: 0x50)

### 方法 (2)

- `void Update()`
  （void 更新（））
- `void Bind(Transform killer)`
  （void Bind（变换 killer））

---

## HUD_MapGun（HUD_映射枪械）

**继承**: Singleton<HUD_MapGun>（Singleton<HUD_映射Gun>）

### 字段 (5)

- `GameObject exitTip`（游戏对象 exitTip）(偏移: 0xC)
- `RawImage backgroundImage`（Raw图像 background图像）(偏移: 0x10)
- `Text ammoText`（文本 ammo文本）(偏移: 0x14)
- `Text emptyAmmoText`（文本 empty弹药文本）(偏移: 0x18)
- `int emptyAmmoTextAnim`（int empty弹药文本动画）(偏移: 0x1C)

### 方法 (6)

- `void Awake()`
  （void 唤醒（））
- `void Start()`
  （void 开始（））
- `void OnMyPlayerJoin(Player myPlayer)`
  （void 我的玩家加入时（玩家 myPlayer））
- `void OnNanoRoleChange(NanoRole oldRole, NanoRole newRole)`
  （void On纳米RoleChange（纳米角色 oldRole, 纳米角色 newRole））
- `void OnLifeStateChange(bool isAlive)`
  （void 生命状态改变时（布尔值 isAlive））
- `void Update()`
  （void 更新（））

---

## HUD_Nano4T_Attribute（HUD_Nano4T_Attribute）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (17)

- `GameObject timerTipBG`（游戏对象 timerTipBG）(偏移: 0xC)
- `HUD_Nano4T_AttributeIcon nanoIcon`（HUD_Nano4T_Attribute图标 nano图标）(偏移: 0x10)
- `HUD_Nano4T_AttributeIcon humanIcon`（HUD_Nano4T_Attribute图标 human图标）(偏移: 0x14)
- `Image header`（图像 header）(偏移: 0x18)
- `Sprite[] headerSpr`（Sprite[] headerSpr）(偏移: 0x1C)
- `Text timer`（文本 timer）(偏移: 0x20)
- `Image nanoImg`（图像 nanoImg）(偏移: 0x24)
- `Text nanoLayer`（文本 nano层）(偏移: 0x28)
- `Image humanImg`（图像 humanImg）(偏移: 0x2C)
- `Text humanLayer`（文本 human层）(偏移: 0x30)
- `bool isNanoBuffMax10`（bool is纳米增益Max10）(偏移: 0x34)
- `Image battleIcon`（图像 battle图标）(偏移: 0x38)
- `Image battleAttributeImg`（图像 battleAttributeImg）(偏移: 0x3C)
- `Text battleAttributeText`（文本 battleAttribute文本）(偏移: 0x40)
- `Sprite[] battleAttributeSprs`（Sprite[] battleAttributeSprs）(偏移: 0x44)
- `GameObject battleCDBg`（游戏对象 battleCDBg）(偏移: 0x48)
- `Text battleCDText`（文本 battleCD文本）(偏移: 0x4C)

### 方法 (10)

- `void Awake()`
  （void 唤醒（））
- `void GameManager_MyPlayerJoinEvent_Observers(Player myPlayer)`
  （void 游戏Manager_My玩家JoinEvent_Observers（玩家 myPlayer））
- `void NanoRole_listener(NanoRole oldRole, NanoRole newRole)`
  （void 纳米Role_listener（纳米角色 oldRole, 纳米角色 newRole））
- `void NewRoundReset(Nano4T_Attribute nanoAtt, Nano4T_Attribute humanAtt)`
  （void 新的回合重置（Nano4T_Attribute nanoAtt, Nano4T_Attribute humanAtt））
- `void StartBattleCountDown()`
  （void 开始Battle数量下（））
- `void StartNanoTimerCountDown()`
  （void 开始纳米计时器数量下（））
- `void OnNanoGhostAppear()`
  （void On纳米幽灵Appear（））
- `void UpdateNanoLayer(int arg1, int newLayer)`
  （void 更新纳米层（int arg1, int newLayer））
- `void UpdateHumanLayer(int arg1, int newLayer)`
  （void 更新人类层（int arg1, int newLayer））
- `void UpdateLayer(Text text, int layer, bool max10)`
  （void 更新层（文本 text, int layer, bool max10））

---

## HUD_Nano4T_AttributeIcon（HUD_Nano4T_Attribute图标）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (7)

- `bool isNano`（bool is纳米）(偏移: 0x10)
- `RectTransform rect`（矩形变换 rect）(偏移: 0x14)
- `Image image`（图像 image）(偏移: 0x18)
- `Text description`（文本 description）(偏移: 0x1C)
- `Vector2 Pos_Nano`（二维向量 Pos_纳米）(偏移: 0x0)
- `Vector2 Pos_Center`（二维向量 Pos_中心）(偏移: 0x8)
- `Vector2 Pos_Soldier`（二维向量 Pos_Soldier）(偏移: 0x10)

### 方法 (8)

- `Nano4T_Attribute get_attribute()`
  （Nano4T_Attribute get_attribute（））
- `void set_attribute(Nano4T_Attribute value)`
  （void set_attribute（Nano4T_Attribute value））
- `bool get_isActive()`
  （bool get_is激活的（））
- `void Init()`
  （void 初始化（））
- `void UpdatePosition(bool isCenter)`
  （void 更新Position（bool isCenter））
- `void SetActive(bool active)`
  （void 设置激活（布尔值 active））
- `void BindAttribute(Nano4T_Attribute attribute)`
  （void BindAttribute（Nano4T_Attribute attribute））
- `void UpdateDescription(bool withName)`
  （void 更新Description（bool withName））

---

## HUD_Nano4T_BoxTimer（HUD_Nano4T_Box计时器）

**继承**: SimpleHudBase（SimpleHud基础）

### 字段 (1)

- `Text timerText`（文本 timer文本）(偏移: 0x10)

### 方法 (3)

- `void Awake()`
  （void 唤醒（））
- `void MyPlayerInit(Player myPlayer)`
  （void My玩家初始化（玩家 myPlayer））
- `void PickUpBoxCount_listener(int oldCount, int newCount)`
  （void Pick上BoxCount_listener（int oldCount, int newCount））

---

## HUD_Nano4T_Critical（HUD_Nano4T_Critical）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (2)

- `GameObject textPrefab`（游戏对象 text预制体）(偏移: 0xC)
- `SimpleObjectPool pool`（Simple对象池 pool）(偏移: 0x10)

### 方法 (3)

- `void Awake()`
  （void 唤醒（））
- `void GameManager_MyPlayerCasueDamageEvent_Observers(ref DamageEventData data)`
  （void 游戏Manager_My玩家Casue伤害Event_Observers（ref DamageEventData data））
- `void ShowDamage(int damage)`
  （void 显示伤害（int damage））

---

## HUD_Nano4_HumanGauge（HUD_Nano4_人类Gauge）

**继承**: SimpleHudBase（SimpleHud基础）

### 字段 (10)

- `GameObject background`（游戏对象 background）(偏移: 0x10)
- `GameObject slotPrefab`（游戏对象 slot预制体）(偏移: 0x14)
- `Image gauge`（图像 gauge）(偏移: 0x18)
- `RawImage[] slots`（RawImage[] slots）(偏移: 0x1C)
- `Texture[] slotTexs`（Texture[] slotTexs）(偏移: 0x20)
- `AnimationHud head`（动画Hud head）(偏移: 0x24)
- `Text atkPowerText`（文本 atk力度文本）(偏移: 0x28)
- `AudioClip heroReadySnd`（音频弹匣 heroReadySnd）(偏移: 0x2C)
- `int deadSoldierCount`（int deadSoldier数量）(偏移: 0x30)
- `int heroNeedCount`（int hero需要数量）(偏移: 0x34)

### 方法 (14)

- `bool get_isNoHero()`
  （bool get_isNo英雄（））
- `bool get_isHeroReady()`
  （bool get_is英雄Ready（））
- `bool get_isSlotType()`
  （bool get_is槽位类型（））
- `void Awake()`
  （void 唤醒（））
- `void MyPlayerInit(Player myPlayer)`
  （void My玩家初始化（玩家 myPlayer））
- `void OnTeamChange(Team team)`
  （void On队伍Change（队伍 team））
- `void OnMyPlayerLifeStateChange(bool isAlive)`
  （void OnMy玩家Life状态Change（bool isAlive））
- `void Update()`
  （void 更新（））
- `void SetTotalSlot(int count)`
  （void 集合Total槽位（int count））
- `void AddSlot()`
  （void 添加槽位（））
- `void ShowHeroReadyTip()`
  （void 显示英雄ReadyTip（））
- `void SetVisible(bool value)`
  （void 集合可见的（bool value））
- `void SetSlotVisible(bool visible)`
  （void 集合槽位可见的（bool visible））
- `void ResetHeroReady()`
  （void 重置英雄Ready（））

---

## HUD_Nano6Gauge（HUD_Nano6Gauge）

**继承**: SimpleHudBase（SimpleHud基础）

### 字段 (7)

- `bool humanType`（bool human类型）(偏移: 0x10)
- `Image headImage`（图像 head图像）(偏移: 0x14)
- `Image backgroundImage`（图像 background图像）(偏移: 0x18)
- `Image duration`（图像 duration）(偏移: 0x1C)
- `Sprite[] asset`（Sprite[] asset）(偏移: 0x20)
- `RectTransform delta`（Rect变换 delta）(偏移: 0x24)
- `float deltaHideTime`（float delta隐藏时间）(偏移: 0x28)

### 方法 (9)

- `void Awake()`
  （void 唤醒（））
- `void MyPlayerInit(Player myPlayer)`
  （void My玩家初始化（玩家 myPlayer））
- `void OnNanoExpChange(int arg1, int newExp)`
  （void On纳米ExpChange（int arg1, int newExp））
- `void OnSoldierExpChange(float oldExp, float newExp)`
  （void OnSoldierExpChange（float oldExp, float newExp））
- `void OnTeamChange(Team team)`
  （void On队伍Change（队伍 team））
- `void SetType(bool isHuman)`
  （void 集合类型（bool isHuman））
- `void Update()`
  （void 更新（））
- `void SetFillAmount(float currentExp, int[] needExp)`
  （void 集合FillAmount（float currentExp, int[] needExp））
- `void ShowDelta()`
  （void 显示Delta（））

---

## HUD_Nano6_BuffIcon（HUD_Nano6_增益图标）

**继承**: RecyclableObject（可回收对象）

### 字段 (3)

- `Image image`（图像 image）(偏移: 0x30)
- `Vector3 targetPos`（三维向量 targetPos）(偏移: 0x34)
- `bool isRadar`（bool isRadar）(偏移: 0x40)

### 方法 (4)

- `void SetSprite(Sprite sprite, bool isRadar)`
  （void 集合精灵（精灵 sprite, bool isRadar））
- `void SetBornPosAndTartgetPos(Vector3 born, Vector3 target)`
  （void 集合出生PosAndTartgetPos（三维向量 born, 三维向量 target））
- `void Work()`
  （void 工作（））
- `void Recycle(bool roundRecycle)`
  （void 回收（布尔值 循环回收））

---

## HUD_NanoDamageScore（HUD_纳米伤害分数）

**继承**: Singleton<HUD_NanoDamageScore>（Singleton<HUD_纳米伤害Score>）

### 字段 (19)

- `int maxDamage`（int max伤害）(偏移: 0xC)
- `RectTransform[] starRect`（RectTransform[] starRect）(偏移: 0x10)
- `RawImage[] starImage`（RawImage[] star图像）(偏移: 0x14)
- `GameObject damageStarPrefab`（游戏对象 damage星预制体）(偏移: 0x18)
- `RectTransform damageStarBornPos`（Rect变换 damage星出生Pos）(偏移: 0x1C)
- `SimpleObjectPool starPool`（Simple对象池 star池）(偏移: 0x20)
- `GameObject goalStarPrefab`（游戏对象 goal星预制体）(偏移: 0x24)
- `SimpleObjectPool goalStarPool`（Simple对象池 goal星池）(偏移: 0x28)
- `RectTransform[] forStarEffect`（RectTransform[] for星特效）(偏移: 0x2C)
- `float randomDistance`（float random距离）(偏移: 0x30)
- `float nextGoalFxTime`（float nextGoal特效时间）(偏移: 0x34)
- `int nextStarPos`（int next星Pos）(偏移: 0x38)
- `Queue<bool> starQueue`（Queue<bool> star队列）(偏移: 0x3C)
- `float shrinkAnimTime`（float shrink动画时间）(偏移: 0x0)
- `Action activeStarRecycyle`（动作 active星Recycyle）(偏移: 0x4)
- `Action goalStarRecycle`（动作 goal星Recycle）(偏移: 0x8)
- `CommonKillMark nanoScore`（Common击杀Mark nano分数）(偏移: 0x40)
- `Texture scoreMark`（纹理 scoreMark）(偏移: 0x44)
- `AnimationHud nanoKillMark`（动画Hud nano击杀Mark）(偏移: 0x48)

### 方法 (17)

- `void Awake()`
  （void 唤醒（））
- `void Start()`
  （void 开始（））
- `void OnMyPlayerJoin(Player myPlayer)`
  （void 我的玩家加入时（玩家 myPlayer））
- `void OnMyPlayerLifeStateChange(bool alive)`
  （void OnMy玩家Life状态Change（bool alive））
- `void OnMyPlayerTeamChange(Team newTeam)`
  （void OnMy玩家队伍Change（队伍 newTeam））
- `void SetVisible(bool newVisbile)`
  （void 集合可见的（bool newVisbile））
- `void OnDestroy()`
  （void 销毁时（））
- `void ResetStar()`
  （void 重置星（））
- `void DamageEvent(ref DamageEventData eventData)`
  （void 伤害事件（ref DamageEventData eventData））
- `void AddStartCount(int count, bool hide)`
  （void 添加开始数量（int count, bool hide））
- `bool SubStarCount(int count)`
  （bool 子星数量（int count））
- `IEnumerator StarGenerator()`
  （IEnumerator 星Generator（））
- `void GenerateGoalStarEffect()`
  （void GenerateGoal星特效（））
- `void StarArrive(int index, bool is500)`
  （void 星Arrive（int index, bool is500））
- `void PlayNanoScoreMark(Texture tex)`
  （void 播放纳米分数Mark（纹理 tex））
- `void PlayNanoScoreMark()`
  （void 播放纳米分数Mark（））
- `void OnPlayNanoKillMark(bool oldState, bool newState)`
  （void On播放纳米击杀Mark（bool oldState, bool newState））

---

## HUD_NanoDamageScore_Effect（HUD_纳米伤害Score_特效）

**继承**: RecyclableObject（可回收对象）

### 字段 (3)

- `RectTransform rectTransform`（Rect变换 rect变换）(偏移: 0x30)
- `RawImage image`（Raw图像 image）(偏移: 0x34)
- `Vector3 targetPos`（三维向量 targetPos）(偏移: 0x38)

### 方法 (3)

- `void Work()`
  （void 工作（））
- `void Recycle(bool roundRecycle)`
  （void 回收（布尔值 循环回收））
- `void SetPos(Vector3 bornPos, Vector3 targetPos)`
  （void 集合Pos（三维向量 bornPos, 三维向量 targetPos））

---

## HUD_NanoDamageScore_Star（HUD_纳米伤害Score_星）

**继承**: RecyclableObject（可回收对象）

### 字段 (7)

- `RectTransform rectTransform`（Rect变换 rect变换）(偏移: 0x30)
- `RawImage rawimage`（Raw图像 rawimage）(偏移: 0x34)
- `int index`（整数 索引）(偏移: 0x38)
- `bool is500`（bool is500）(偏移: 0x3C)
- `bool hide`（bool hide）(偏移: 0x3D)
- `Vector2 targetPos1`（二维向量 targetPos1）(偏移: 0x40)
- `Vector2 targetPos2`（二维向量 targetPos2）(偏移: 0x48)

### 方法 (5)

- `void OnDisable()`
  （void 禁用时（））
- `void OnEnable()`
  （void 启用时（））
- `void SetData(int index, bool is500, bool hide)`
  （void 集合数据（int index, bool is500, bool hide））
- `void Work()`
  （void 工作（））
- `void Recycle(bool roundRecycle)`
  （void 回收（布尔值 循环回收））

---

## HUD_NanoExpGauge（HUD_纳米ExpGauge）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (2)

- `GameObject bg`（游戏对象 bg）(偏移: 0xC)
- `GameObject[] expObjs`（游戏Object[] expObjs）(偏移: 0x10)

### 方法 (5)

- `void Awake()`
  （void 唤醒（））
- `void OnMyPlayerJoin(Player myPlayer)`
  （void 我的玩家加入时（玩家 myPlayer））
- `void OnNanoExpChange(int oldExp, int newExp)`
  （void On纳米ExpChange（int oldExp, int newExp））
- `void OnNanoRoleChange(NanoRole oldRole, NanoRole newRole)`
  （void On纳米RoleChange（纳米角色 oldRole, 纳米角色 newRole））
- `void OnLifeStateChange(bool isAlive)`
  （void 生命状态改变时（布尔值 isAlive））

---

## HUD_NanoRoleSign（HUD_纳米Role标志）

**继承**: HUD_ProjectionSign（HUD_投影标志）

### 字段 (3)

- `Player bindPlayer`（玩家 bind玩家）(偏移: 0x50)
- `bool globalView`（bool global视图）(偏移: 0x54)
- `bool soldierSign`（bool soldier标志）(偏移: 0x55)

### 方法 (3)

- `void Bind(Player player)`
  （void 绑定（玩家 player））
- `void OnRoleChange(NanoRole oldRole, NanoRole newRole)`
  （void OnRoleChange（纳米角色 oldRole, 纳米角色 newRole））
- `bool GetVisible()`
  （bool 获取可见的（））

---

## HUD_Nano_FinalBattle（HUD_Nano_FinalBattle）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (13)

- `bool shakeIcon`（bool shake图标）(偏移: 0xC)
- `RectTransform heroIconRect`（Rect变换 hero图标Rect）(偏移: 0x10)
- `RectTransform nanoIconRect`（Rect变换 nano图标Rect）(偏移: 0x14)
- `Text heroNumText`（文本 heroNum文本）(偏移: 0x18)
- `Text nanoNumText`（文本 nanoNum文本）(偏移: 0x1C)
- `Font normalFont`（Font normalFont）(偏移: 0x20)
- `Font flashFont`（Font flashFont）(偏移: 0x24)
- `Vector2Int curCount`（二维向量整数 cur数量）(偏移: 0x28)
- `Vector2 flashEndTime`（二维向量 flash结束时间）(偏移: 0x30)
- `AudioClip nanoCountDownSnd`（音频弹匣 nano数量下Snd）(偏移: 0x38)
- `float nextKillNanoSndTime`（float next击杀纳米Snd时间）(偏移: 0x3C)
- `Vector2 heroIconPos`（二维向量 hero图标Pos）(偏移: 0x0)
- `Vector2 nanoIconPos`（二维向量 nano图标Pos）(偏移: 0x8)

### 方法 (7)

- `void Awake()`
  （void 唤醒（））
- `void Update()`
  （void 更新（））
- `void SetActive(bool active)`
  （void 设置激活（布尔值 active））
- `void SetHeroCount(int count)`
  （void 集合英雄数量（int count））
- `void SetNanoCount(int count)`
  （void 集合纳米数量（int count））
- `void DeathEvent(DeathEventData evtData)`
  （void 死亡事件（死亡事件数据 evtData））
- `void ShakeIcon(RectTransform target, Vector2 originPos)`
  （void 震动图标（Rect变换 target, 二维向量 originPos））

---

## HUD_PlayerRect（HUD_玩家Rect）

**继承**: RecyclableObject（可回收对象）

### 字段 (3)

- `RectTransform rect`（矩形变换 rect）(偏移: 0x30)
- `Image image`（图像 image）(偏移: 0x34)
- `Sprite[] asset`（Sprite[] asset）(偏移: 0x38)

### 方法 (2)

- `void SetPos(int id, bool left)`
  （void 集合Pos（int id, bool left））
- `void SetImage(HUD_PlayerRect.Type type)`
  （void 集合图像（HUD_玩家Rect.类型 type））

---

## HUD_PlayerRect.Type（HUD_玩家Rect.类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## HUD_ProjectionID（HUD_ProjectionID）

**继承**: Singleton<HUD_ProjectionID>（Singleton<HUD_ProjectionID>）

### 字段 (4)

- `RectTransform canvasRect`（Rect变换 canvasRect）(偏移: 0xC)
- `HUD_KillerSign killerSign`（HUD_击杀者标志 killer标志）(偏移: 0x10)
- `GameObject supplyBoxPrefab`（游戏对象 supplyBox预制体）(偏移: 0x14)
- `NameKeyPool pool`（名称键池 pool）(偏移: 0x18)

### 方法 (4)

- `void Awake()`
  （void 唤醒（））
- `void SetKiller(Transform killer)`
  （void 集合击杀者（变换 killer））
- `void AddSupplyBox(SupplyBox supplyBox)`
  （void 添加SupplyBox（SupplyBox supplyBox））
- `RecyclableObject GetSign(GameObject prefab)`
  （Recyclable对象 获取标志（游戏对象 prefab））

---

## HUD_ProjectionSign（HUD_投影标志）

**继承**: RecyclableObject（可回收对象）

### 字段 (6)

- `Image image`（图像 image）(偏移: 0x30)
- `RectTransform rect`（矩形变换 rect）(偏移: 0x34)
- `Text distanceText`（文本 distance文本）(偏移: 0x38)
- `Transform bindTransform`（变换 bind变换）(偏移: 0x3C)
- `Vector3 offset`（三维向量 偏移）(偏移: 0x40)
- `float showRange`（float show范围）(偏移: 0x4C)

### 方法 (6)

- `void Update()`
  （void 更新（））
- `void SetGraphVisible(bool visible)`
  （void 集合Graph可见的（bool visible））
- `void Recycle(bool roundRecycle)`
  （void 回收（布尔值 循环回收））
- `bool GetVisible()`
  （bool 获取可见的（））
- `void Bind(Transform bind)`
  （void Bind（变换 bind））
- `void SetSprtie(Sprite spr)`
  （void 集合Sprtie（精灵 spr））

---

## HUD_Radar（HUD_Radar）

**继承**: Singleton<HUD_Radar>（Singleton<HUD_Radar>）

### 字段 (11)

- `RectTransform mask`（Rect变换 mask）(偏移: 0xC)
- `RectTransform minimap`（Rect变换 minimap）(偏移: 0x10)
- `RectTransform frame`（Rect变换 frame）(偏移: 0x14)
- `RectTransform iconsContainer`（Rect变换 icons容器）(偏移: 0x18)
- `GameObject simpleRadarIconPrefab`（游戏对象 simpleRadar图标预制体）(偏移: 0x1C)
- `GameObject entityRadarIconPrefab`（游戏对象 entityRadar图标预制体）(偏移: 0x20)
- `GameObject supplyBoxIconPrefab`（游戏对象 supplyBox图标预制体）(偏移: 0x24)
- `NameKeyPool radarIconPool1`（名称键池 radar图标Pool1）(偏移: 0x28)
- `NameKeyPool radarIconPool2`（名称键池 radar图标Pool2）(偏移: 0x2C)
- `bool hideEnemy`（bool hideEnemy）(偏移: 0x0)
- `float scale`（浮点数 缩放）(偏移: 0x4)

### 方法 (11)

- `float get_pixelPerDistance()`
  （float get_pixelPer距离（））
- `Vector3 get_originalPos()`
  （三维向量 get_originalPos（））
- `void Awake()`
  （void 唤醒（））
- `void Start()`
  （void 开始（））
- `void OnNewPlayerJoin(Player player)`
  （void On新的玩家Join（玩家 player））
- `void Update()`
  （void 更新（））
- `RectTransform GetIconContainer()`
  （Rect变换 获取图标容器（））
- `HUD_RadarIcon AddIcon(Transform bind, bool addInMask = False)`
  （HUD_Radar图标 添加图标（变换 bind, bool addInMask = False））
- `void AddEntity(Entity entity)`
  （void 添加实体（实体 entity））
- `void AddSupplyBox(SupplyBox supplyBox)`
  （void 添加SupplyBox（SupplyBox supplyBox））
- `HUD_RadarIcon GetIcon(GameObject prefab, bool addInMask)`
  （HUD_Radar图标 获取图标（游戏对象 prefab, bool addInMask））

---

## HUD_RadarIcon（HUD_雷达图标）

**继承**: RecyclableObject（可回收对象）

### 字段 (5)

- `RectTransform rectTransform`（Rect变换 rect变换）(偏移: 0x30)
- `Image image`（图像 image）(偏移: 0x34)
- `Transform bindTransform`（变换 bind变换）(偏移: 0x38)
- `Vector3 delta3dPos`（三维向量 delta3dPos）(偏移: 0x3C)
- `bool rotateAtEdge`（bool rotateAtEdge）(偏移: 0x49)

### 方法 (12)

- `bool get_atEdge()`
  （bool get_atEdge（））
- `void set_atEdge(bool value)`
  （void set_atEdge（bool value））
- `Player get_focusPlayer()`
  （玩家 get_focus玩家（））
- `bool get_maskable()`
  （bool get_maskable（））
- `void set_maskable(bool value)`
  （void set_maskable（bool value））
- `void Update()`
  （void 更新（））
- `void UpdateTransform()`
  （void 更新变换（））
- `bool IsVisible()`
  （布尔值 是否可见（））
- `void SetSprite(Sprite sprite)`
  （void 集合精灵（精灵 sprite））
- `void Bind(Transform bind)`
  （void Bind（变换 bind））
- `void Work()`
  （void 工作（））
- `void Recycle(bool roundRecycle)`
  （void 回收（布尔值 循环回收））

---

## HUD_RadarIcon_Alive（HUD_RadarIcon_Alive）

**继承**: HUD_RadarIcon（HUD_雷达图标）

### 字段 (1)

- `Entity entity`（实体 entity）(偏移: 0x4C)

### 方法 (3)

- `bool IsVisible()`
  （布尔值 是否可见（））
- `void Bind(Entity entity)`
  （void Bind（实体 entity））
- `void Recycle(bool roundRecycle)`
  （void 回收（布尔值 循环回收））

---

## HUD_RadarIcon_Entity（HUD_RadarIcon_实体）

**继承**: HUD_RadarIcon（HUD_雷达图标）

### 字段 (12)

- `Entity entity`（实体 entity）(偏移: 0x4C)
- `Sprite teammate`（精灵 teammate）(偏移: 0x50)
- `Sprite teammate_Far`（精灵 teammate_Far）(偏移: 0x54)
- `Sprite teammate_Top`（精灵 teammate_顶部）(偏移: 0x58)
- `Sprite teammate_Bottom`（精灵 teammate_底部）(偏移: 0x5C)
- `Sprite teammate_Dead`（精灵 teammate_Dead）(偏移: 0x60)
- `Sprite enemy`（精灵 enemy）(偏移: 0x64)
- `Sprite enemy_Far`（精灵 enemy_Far）(偏移: 0x68)
- `Sprite enemy_Top`（精灵 enemy_顶部）(偏移: 0x6C)
- `Sprite enemy_Bottom`（精灵 enemy_底部）(偏移: 0x70)
- `Vector2 normalPivot`（二维向量 normalPivot）(偏移: 0x0)
- `Vector2 farPivot`（二维向量 farPivot）(偏移: 0x8)

### 方法 (4)

- `void Update()`
  （void 更新（））
- `bool IsVisible()`
  （布尔值 是否可见（））
- `void Bind(Entity entity)`
  （void Bind（实体 entity））
- `void Recycle(bool roundRecycle)`
  （void 回收（布尔值 循环回收））

---

## HUD_RadarIcon_HearBeat（HUD_RadarIcon_HearBeat）

**继承**: HUD_RadarIcon（HUD_雷达图标）

### 字段 (2)

- `CommonHud_1 hud`（CommonHud_1 hud）(偏移: 0x4C)
- `Entity entity`（实体 entity）(偏移: 0x50)

### 方法 (4)

- `bool IsVisible()`
  （布尔值 是否可见（））
- `void Bind(Entity entity, float time)`
  （void Bind（实体 entity, float time））
- `void Recycle(bool roundRecycle)`
  （void 回收（布尔值 循环回收））
- `void Work()`
  （void 工作（））

---

## HUD_RadarIcon_SupplyBox（HUD_RadarIcon_SupplyBox）

**继承**: HUD_RadarIcon（HUD_雷达图标）

### 字段 (4)

- `SupplyBox.Type supplyBoxType`（SupplyBox.类型 supplyBox类型）(偏移: 0x4C)
- `Sprite yellow`（精灵 yellow）(偏移: 0x50)
- `Sprite red`（精灵 red）(偏移: 0x54)
- `Sprite blue`（精灵 blue）(偏移: 0x58)

### 方法 (3)

- `void Update()`
  （void 更新（））
- `bool IsVisible()`
  （布尔值 是否可见（））
- `void Bind(SupplyBox supplyBox)`
  （void Bind（SupplyBox supplyBox））

---

## HUD_Role（HUD_Role）

**继承**: Singleton<HUD_Role>（Singleton<HUD_Role>）

### 字段 (16)

- `Sprite[] aceSprites`（Sprite[] aceSprites）(偏移: 0xC)
- `AudioClip[] aceAudio`（音频Clip[] ace音频）(偏移: 0x10)
- `HealthData healthData`（Health数据 health数据）(偏移: 0x14)
- `RawImage backgroundImage`（Raw图像 background图像）(偏移: 0x18)
- `Image effectImage`（图像 effect图像）(偏移: 0x1C)
- `RawImage lineImage`（Raw图像 line图像）(偏移: 0x20)
- `Text healthNum`（文本 healthNum）(偏移: 0x24)
- `Text armorNum`（文本 armorNum）(偏移: 0x28)
- `Material redFlashMat`（材质 redFlash材质）(偏移: 0x2C)
- `float lerpAnimEndTime`（float lerp动画结束时间）(偏移: 0x30)
- `Image aceImage`（图像 ace图像）(偏移: 0x34)
- `Color green`（颜色 green）(偏移: 0x0)
- `Color orange`（颜色 orange）(偏移: 0x10)
- `Color red`（颜色 red）(偏移: 0x20)
- `NameKeyPool skillBtnPool`（名称键池 skillBtn池）(偏移: 0x38)
- `HUD_SkillBtn[] skillBtns`（HUD_技能Btn[] skillBtns）(偏移: 0x3C)

### 方法 (10)

- `void Awake()`
  （void 唤醒（））
- `void Update()`
  （void 更新（））
- `void SetColor(Color color, bool flash = False)`
  （void 集合颜色（颜色 color, bool flash = False））
- `void OnMyPlayerJoin(Player myPlayer)`
  （void 我的玩家加入时（玩家 myPlayer））
- `void SetAsset(HUD_RoleAsset roleAsset)`
  （void 集合资产（HUD_Role资产 roleAsset））
- `void UpdateAceSign(HUD_Role.AceSign oldSign, HUD_Role.AceSign newSign)`
  （void 更新王牌标志（HUD_Role.王牌标志 oldSign, HUD_Role.王牌标志 newSign））
- `HUD_SkillBtn AddSkillBtn(GameObject btnPrefab, Skill bindSkill)`
  （HUD_技能Btn 添加技能Btn（游戏对象 btnPrefab, 技能 bindSkill））
- `void RemoveSkillBtn(HUD_SkillBtn btn)`
  （void 移除技能Btn（HUD_技能Btn btn））
- `void TrySetPos(HUD_SkillBtn btn, int pos)`
  （void Try集合Pos（HUD_技能Btn btn, int pos））
- `void StartLerpAnim()`
  （void 开始Lerp动画（））

---

## HUD_Role.AceSign（HUD_Role.王牌标志）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## HUD_RoleAsset（HUD_Role资产）

**继承**: ScriptableObject（脚本对象）

### 字段 (3)

- `Texture background`（纹理 background）(偏移: 0xC)
- `Sprite effect`（精灵 effect）(偏移: 0x10)
- `Texture line`（纹理 line）(偏移: 0x14)

---

## HUD_ScreenFX（HUD_屏幕的FX）

**继承**: Singleton<HUD_ScreenFX>（Singleton<HUD_屏幕的FX>）

### 字段 (2)

- `RawImage nanoScreenImage`（Raw图像 nano屏幕的图像）(偏移: 0xC)
- `NameKeyPool pool`（名称键池 pool）(偏移: 0x10)

### 方法 (3)

- `void Awake()`
  （void 唤醒（））
- `void Update()`
  （void 更新（））
- `RecyclableObject AddEffect(GameObject pfb, bool autoActive)`
  （Recyclable对象 添加特效（游戏对象 pfb, bool autoActive））

---

## HUD_SelectMasterRole（HUD_选择MasterRole）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (3)

- `Image img`（图像 img）(偏移: 0xC)
- `Sprite[] sprs`（Sprite[] sprs）(偏移: 0x10)
- `NanoRoleSelect roleSelect`（纳米Role选择 role选择）(偏移: 0x14)

### 方法 (4)

- `void Awake()`
  （void 唤醒（））
- `void GameManager_MyPlayerJoinEvent_Observers(Player myPlayer)`
  （void 游戏Manager_My玩家JoinEvent_Observers（玩家 myPlayer））
- `void PlayerController_FocusHUD_Listenner(ref string hud)`
  （void 玩家控制器_聚焦HUD_监听器（引用 字符串 hud））
- `void NanoRoleSelect_Type_Listnner(NanoRoleSelect.Type obj)`
  （void 纳米RoleSelect_Type_Listnner（纳米RoleSelect.类型 obj））

---

## HUD_SelectNanoRole（HUD_选择纳米Role）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (4)

- `GameObject main`（游戏对象 main）(偏移: 0xC)
- `GameObject[] images`（游戏Object[] images）(偏移: 0x10)
- `Text timeText`（文本 time文本）(偏移: 0x14)
- `NanoRoleSelect roleSelect`（纳米Role选择 role选择）(偏移: 0x18)

### 方法 (6)

- `void Awake()`
  （void 唤醒（））
- `void PlayerController_FocusHUD_Listenner(ref string hud)`
  （void 玩家控制器_聚焦HUD_监听器（引用 字符串 hud））
- `void Update()`
  （void 更新（））
- `void GameManager_MyPlayerJoinEvent_Observers(Player myPlayer)`
  （void 游戏Manager_My玩家JoinEvent_Observers（玩家 myPlayer））
- `void NanoRoleSelect_Type_Listnner(NanoRoleSelect.Type obj)`
  （void 纳米RoleSelect_Type_Listnner（纳米RoleSelect.类型 obj））
- `void UpdateTimeText()`
  （void 更新时间文本（））

---

## HUD_SkillBtn（HUD_技能Btn）

**继承**: RecyclableObject（可回收对象）

### 字段 (4)

- `int curPos`（int curPos）(偏移: 0x30)
- `Image image`（图像 image）(偏移: 0x34)
- `Sprite[] btnSprs`（Sprite[] btnSprs）(偏移: 0x38)
- `Skill bindSkill`（技能 bind技能）(偏移: 0x3C)

### 方法 (3)

- `void Update()`
  （void 更新（））
- `void SetPos(int pos)`
  （void 集合Pos（int pos））
- `void Recycle(bool roundRecycle)`
  （void 回收（布尔值 循环回收））

---

## HUD_Spectate（HUD_Spectate）

**继承**: Singleton<HUD_Spectate>（Singleton<HUD_Spectate>）

### 字段 (21)

- `string hideString`（string hide字符串）(偏移: 0x0)
- `string showString`（string show字符串）(偏移: 0x4)
- `Vector2 originPos`（二维向量 originPos）(偏移: 0x8)
- `Vector2 offsetPos`（二维向量 offsetPos）(偏移: 0x10)
- `Vector3 hideScale`（三维向量 hide缩放）(偏移: 0x18)
- `RectTransform mainRect`（Rect变换 mainRect）(偏移: 0xC)
- `Text underText`（文本 under文本）(偏移: 0x10)
- `RawImage killerLevel`（Raw图像 killer等级）(偏移: 0x14)
- `Text killerNameText`（文本 killer名称文本）(偏移: 0x18)
- `Text weaponNameText`（文本 weapon名称文本）(偏移: 0x1C)
- `RectTransform weaponRect`（Rect变换 weaponRect）(偏移: 0x20)
- `RawImage weaponImage`（Raw图像 weapon图像）(偏移: 0x24)
- `RawImage weaponExtraImage`（Raw图像 weapon额外的图像）(偏移: 0x28)
- `GameObject skull`（游戏对象 skull）(偏移: 0x2C)
- `GameObject headShot`（游戏对象 head射击）(偏移: 0x30)
- `bool switchCooling`（bool switchCooling）(偏移: 0x34)
- `bool isOpen`（bool is打开）(偏移: 0x35)
- `Sprite[] hitNodeSprites`（Sprite[] hit节点Sprites）(偏移: 0x38)
- `List<HUD_SpectateMsg> spareMsg`（List<HUD_SpectateMsg> spareMsg）(偏移: 0x3C)
- `List<HUD_SpectateMsg> busyMsg`（List<HUD_SpectateMsg> busyMsg）(偏移: 0x40)
- `List<HUD_Spectate.Data> dataList`（List<HUD_Spectate.Data> data列表）(偏移: 0x44)

### 方法 (10)

- `void Awake()`
  （void 唤醒（））
- `void SpawnEvent(Player player)`
  （void 出生事件（玩家 player））
- `void DamageEvent(ref DamageEventData eventData)`
  （void 伤害事件（ref DamageEventData eventData））
- `void DeathEvent(DeathEventData eventData)`
  （void 死亡事件（死亡事件数据 eventData））
- `void KillEvent(DeathEventData eventData)`
  （void 击杀事件（死亡事件数据 eventData））
- `void Update()`
  （void 更新（））
- `void Clear()`
  （void 清除（））
- `void Open()`
  （void 打开（））
- `void Close()`
  （void 关闭（））
- `void TryCloseAandObserveTeammate()`
  （void Try关闭Aand观察Teammate（））

---

## HUD_Spectate.Data（HUD_Spectate.数据）

### 字段 (4)

- `int spawnCount`（int spawn数量）(偏移: 0x8)
- `string nickName`（string nick名称）(偏移: 0xC)
- `int damage`（int damage）(偏移: 0x10)
- `HUD_SpectateMsg bindMsg`（HUD_SpectateMsg bindMsg）(偏移: 0x14)

---

## HUD_SpectateMsg（HUD_SpectateMsg）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (7)

- `RawImage levelIcon`（Raw图像 level图标）(偏移: 0xC)
- `RectTransform rect`（矩形变换 rect）(偏移: 0x10)
- `Text nameText`（文本 name文本）(偏移: 0x14)
- `Image killTypeImage`（图像 kill类型图像）(偏移: 0x18)
- `Text damageText`（文本 damage文本）(偏移: 0x1C)
- `Color deadColor`（颜色 dead颜色）(偏移: 0x0)
- `Color aliveColor`（颜色 alive颜色）(偏移: 0x10)

### 方法 (5)

- `void set_damage(int value)`
  （void set_damage（int value））
- `void set_infect(bool value)`
  （void set_infect（bool value））
- `void Init(string nickName, int level)`
  （void 初始化（string nickName, int level））
- `void Kill(Sprite killTypeSprite)`
  （void 击杀（精灵 killTypeSprite））
- `void SetPos(int index)`
  （void 集合Pos（int index））

---

## HUD_SupplyBoxSign（HUD_SupplyBox标志）

**继承**: HUD_ProjectionSign（HUD_投影标志）

### 字段 (4)

- `SupplyBox.Type supplyBoxType`（SupplyBox.类型 supplyBox类型）(偏移: 0x50)
- `Sprite yellow`（精灵 yellow）(偏移: 0x54)
- `Sprite red`（精灵 red）(偏移: 0x58)
- `Sprite blue`（精灵 blue）(偏移: 0x5C)

### 方法 (3)

- `void Update()`
  （void 更新（））
- `bool GetVisible()`
  （bool 获取可见的（））
- `void Bind(SupplyBox supplyBox)`
  （void Bind（SupplyBox supplyBox））

---

## HUD_TabScoreBoard（HUD_Tab分数Board）

**继承**: Singleton<HUD_TabScoreBoard>（Singleton<HUD_Tab分数Board>）

### 字段 (15)

- `RectTransform rect`（矩形变换 rect）(偏移: 0xC)
- `Image[] images`（Image[] images）(偏移: 0x10)
- `Vector2 showStartPos`（二维向量 show开始Pos）(偏移: 0x14)
- `Vector2 showEndPos`（二维向量 show结束Pos）(偏移: 0x1C)
- `RankField rankField`（排名Field rankField）(偏移: 0x24)
- `RectTransform revengeSignRect`（Rect变换 revenge标志Rect）(偏移: 0x28)
- `Vector2 revengeSignLocalPos`（二维向量 revenge标志本地的Pos）(偏移: 0x0)
- `RectTransform myPlayerBG`（Rect变换 my玩家BG）(偏移: 0x2C)
- `TabScoreBoard_PlayerData myPlayerData`（Tab分数Board_玩家数据 my玩家数据）(偏移: 0x30)
- `Text fpsText`（文本 fps文本）(偏移: 0x34)
- `int passFrame`（int passFrame）(偏移: 0x38)
- `float passTime`（float pass时间）(偏移: 0x3C)
- `int dataInterval`（int data间隔）(偏移: 0x40)
- `Action AceUpdateAction`（动作 王牌更新动作）(偏移: 0x8)
- `Vector2 myPlayerBGlocalPos`（二维向量 my玩家BGlocalPos）(偏移: 0xC)

### 方法 (10)

- `void Awake()`
  （void 唤醒（））
- `void Update()`
  （void 更新（））
- `void OnDestroy()`
  （void 销毁时（））
- `void SetVisible(bool newVisible)`
  （void 集合可见的（bool newVisible））
- `void NewPlayerJoin(Player newPlayer)`
  （void 新的玩家Join（玩家 newPlayer））
- `void OnMyPlayerJoin(Player myPlayer)`
  （void 我的玩家加入时（玩家 myPlayer））
- `void UpdateRevengeTarget(Player target)`
  （void 更新复仇目标（玩家 target））
- `RankField GetEnemyRankField()`
  （排名Field 获取Enemy排名Field（））
- `TabScoreBoard_PlayerData AddPlayerToRankField(Player newPlayer)`
  （Tab分数Board_玩家数据 添加玩家To排名Field（玩家 newPlayer））
- `IEnumerator FPSCalculator()`
  （IEnumerator FPSCalculator（））

---

## HUD_TabScoreBoard_DM（HUD_Tab分数Board_DM）

**继承**: HUD_TabScoreBoard（HUD_Tab分数Board）

### 字段 (1)

- `GameObject aceSign`（游戏对象 ace标志）(偏移: 0x44)

### 方法 (1)

- `void Update()`
  （void 更新（））

---

## HUD_TabScoreBoard_Nano（HUD_Tab分数Board_纳米）

**继承**: HUD_TabScoreBoard（HUD_Tab分数Board）

### 字段 (1)

- `HUD_TabScoreBoard_Nano instance2`（HUD_Tab分数Board_纳米 instance2）(偏移: 0x0)

### 方法 (4)

- `void Awake()`
  （void 唤醒（））
- `void OnDestroy()`
  （void 销毁时（））
- `Texture GetRespawnIcon()`
  （纹理 获取重生图标（））
- `Texture GetRoleIcon(NanoRole nanoRole)`
  （纹理 获取Role图标（纳米角色 nanoRole））

---

## HUD_TabScoreBoard_TD（HUD_Tab分数Board_TD）

**继承**: HUD_TabScoreBoard（HUD_Tab分数Board）

### 字段 (5)

- `RankField enemyRankField`（排名Field enemy排名Field）(偏移: 0x44)
- `Image[] scoreboardImages`（Image[] scoreboardImages）(偏移: 0x48)
- `Sprite[] scoreboardSprs`（Sprite[] scoreboardSprs）(偏移: 0x4C)
- `Sprite[] aceSignSprs`（Sprite[] ace标志Sprs）(偏移: 0x50)
- `GameObject firstIcon`（游戏对象 first图标）(偏移: 0x54)

### 方法 (5)

- `void Update()`
  （void 更新（））
- `void OnMyPlayerJoin(Player myPlayer)`
  （void 我的玩家加入时（玩家 myPlayer））
- `TabScoreBoard_PlayerData AddPlayerToRankField(Player newPlayer)`
  （Tab分数Board_玩家数据 添加玩家To排名Field（玩家 newPlayer））
- `RankField GetEnemyRankField()`
  （排名Field 获取Enemy排名Field（））
- `Sprite GetAceSign(HUD_Role.AceSign sign)`
  （精灵 获取王牌标志（HUD_Role.王牌标志 sign））

---

## HUD_TerminatorSign（HUD_Terminator标志）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (5)

- `Button readBtn`（按钮 readBtn）(偏移: 0xC)
- `Text btnText`（文本 btn文本）(偏移: 0x10)
- `Text centerText`（文本 center文本）(偏移: 0x14)
- `int curText`（int cur文本）(偏移: 0x18)
- `string[] myTexts`（string[] myTexts）(偏移: 0x1C)

### 方法 (3)

- `void Awake()`
  （void 唤醒（））
- `void Start()`
  （void 开始（））
- `void NextRead()`
  （void 下一个Read（））

---

## HUD_Tombstone（HUD_Tombstone）

**继承**: Singleton<HUD_Tombstone>（Singleton<HUD_Tombstone>）

### 字段 (5)

- `GameObject otherBarPrefab`（游戏对象 otherBar预制体）(偏移: 0xC)
- `Text tip`（文本 tip）(偏移: 0x10)
- `Image bar`（图像 bar）(偏移: 0x14)
- `Text hpText`（文本 hp文本）(偏移: 0x18)
- `HealthData myTombHealth`（Health数据 myTombHealth）(偏移: 0x1C)

### 方法 (7)

- `void Update()`
  （void 更新（））
- `HUD_HealthBar AddHealthBar(TombStone tomb)`
  （HUD_HealthBar 添加HealthBar（TombStone tomb））
- `void BindMyTomb(RecyclableObject tombRO, HealthData health)`
  （void BindMyTomb（Recyclable对象 tombRO, Health数据 health））
- `void OnMyTombRecycle()`
  （void OnMyTombRecycle（））
- `void ShowRespawnTip()`
  （void 显示重生Tip（））
- `void StopRespawnCountDown()`
  （void 停止重生数量下（））
- `void OnMyPlayerRespawn(Player myPlayer)`
  （void OnMy玩家重生（玩家 myPlayer））

---

## HUD_UpgradeBoxTip（HUD_UpgradeBoxTip）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (5)

- `GameObject background`（游戏对象 background）(偏移: 0xC)
- `Text text`（文本 text）(偏移: 0x10)
- `Team tipTeam`（队伍 tip队伍）(偏移: 0x14)
- `float arriveTime`（float arrive时间）(偏移: 0x18)
- `float closeTime`（float close时间）(偏移: 0x1C)

### 方法 (7)

- `void Awake()`
  （void 唤醒（））
- `void GameManager_MyPlayerJoinEvent_Observers(Player myPlayer)`
  （void 游戏Manager_My玩家JoinEvent_Observers（玩家 myPlayer））
- `void MyPlayer_team_Listenner(Team team)`
  （void MyPlayer_team_Listenner（队伍 team））
- `void Update()`
  （void 更新（））
- `void Show(float arriveTime, Team tipTeam)`
  （void 显示（float arriveTime, 队伍 tipTeam））
- `void Close()`
  （void 关闭（））
- `void UpdateText()`
  （void 更新文本（））

---

## HUD_Weapon（HUD_Weapon）

**继承**: Singleton<HUD_Weapon>（Singleton<HUD_Weapon>）

### 字段 (23)

- `Recoil recoil`（后坐力 recoil）(偏移: 0xC)
- `float clipRedEndTime`（float clip红色结束时间）(偏移: 0x10)
- `RawImage ammo_BG`（Raw图像 ammo_BG）(偏移: 0x14)
- `Text clipText`（文本 clip文本）(偏移: 0x18)
- `Text ammoText`（文本 ammo文本）(偏移: 0x1C)
- `RectTransform weaponNameRect`（Rect变换 weapon名称Rect）(偏移: 0x20)
- `Text weaponNameText`（文本 weapon名称文本）(偏移: 0x24)
- `RawImage weaponBGImage`（Raw图像 weaponBG图像）(偏移: 0x28)
- `RawImage weaponEffectImage`（Raw图像 weapon特效图像）(偏移: 0x2C)
- `RawImage weaponLineImage`（Raw图像 weaponLine图像）(偏移: 0x30)
- `GameObject infinityAmmo`（游戏对象 infinity弹药）(偏移: 0x34)
- `Texture[] ammoBGTexs`（Texture[] ammoBGTexs）(偏移: 0x38)
- `GameObject ammoEnergyBG`（游戏对象 ammoEnergyBG）(偏移: 0x3C)
- `Image ammoEnergyGauge`（图像 ammoEnergyGauge）(偏移: 0x40)
- `Vector2 wpnNamePos_L`（二维向量 武器名称Pos_L）(偏移: 0x0)
- `Vector2 wpnNamePos_R`（二维向量 武器名称Pos_R）(偏移: 0x8)
- `Vector2 AmmoPos_below_1000`（二维向量 弹药Pos_below_1000）(偏移: 0x10)
- `Vector2 AmmoPos_above_1000`（二维向量 弹药Pos_above_1000）(偏移: 0x18)
- `Color Color_BuffClip`（颜色 Color_增益弹匣）(偏移: 0x20)
- `float effectAnimTime`（float effect动画时间）(偏移: 0x30)
- `float effectEndTime`（float effect结束时间）(偏移: 0x44)
- `WPN_Gun.AmmoData ammoData`（WPN_Gun.弹药数据 ammo数据）(偏移: 0x48)
- `float lerpAnimEndTime`（float lerp动画结束时间）(偏移: 0x4C)

### 方法 (9)

- `void Awake()`
  （void 唤醒（））
- `void Update()`
  （void 更新（））
- `void AmmoUpdate()`
  （void 弹药更新（））
- `void PlayClipNumFlashFX()`
  （void 播放弹匣NumFlashFX（））
- `void PlayAmmoLerpAnim()`
  （void 播放弹药Lerp动画（））
- `void SetIcon(WpnSpriteAsset asset)`
  （void 集合图标（武器精灵资产 asset））
- `void SetName(string name)`
  （void 集合名称（string name））
- `void SetAmmoBGType(HUD_Weapon.AmmoBGType bgType)`
  （void 集合弹药BG类型（HUD_Weapon.弹药BG类型 bgType））
- `void PlayEffect()`
  （void 播放特效（））

---

## HUD_Weapon.AmmoBGType（HUD_Weapon.弹药BG类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## HUD_WeaponSlot（HUD_Weapon槽位）

**继承**: Singleton<HUD_WeaponSlot>（Singleton<HUD_WeaponSlot>）

### 字段 (7)

- `HUD_WeaponSlotIndividual[] slots`（HUD_Weapon槽位Individual[] slots）(偏移: 0xC)
- `int rapidChangeSlot`（int rapidChange槽位）(偏移: 0x10)
- `RawImage rapidChangeImage`（Raw图像 rapidChange图像）(偏移: 0x14)
- `int specialWeaponSlot`（int specialWeapon槽位）(偏移: 0x18)
- `RawImage specialWeaponImage`（Raw图像 specialWeapon图像）(偏移: 0x1C)
- `Texture2D[] specialWeaponSprs`（Texture2D[] specialWeaponSprs）(偏移: 0x20)
- `Vector2 SpecialWeaponTipPos`（二维向量 特殊WeaponTipPos）(偏移: 0x0)

### 方法 (6)

- `void Update()`
  （void 更新（））
- `void SetImage(int slot, WpnSpriteAsset spriteAsset)`
  （void 集合图像（int slot, 武器精灵资产 spriteAsset））
- `void Clean(int slot)`
  （void Clean（int slot））
- `void Select(int slot, bool isRapidChange)`
  （void 选择（int slot, bool isRapidChange））
- `void SetSpecialWeaponState(bool isOn)`
  （void 集合特殊Weapon状态（bool isOn））
- `void SetSpecialWeaponSlot(int slot)`
  （void 集合特殊Weapon槽位（int slot））

---

## HUD_WeaponSlotIndividual（HUD_Weapon槽位Individual）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (6)

- `RawImage slotImage`（Raw图像 slot图像）(偏移: 0xC)
- `RectTransform slotRect`（Rect变换 slotRect）(偏移: 0x10)
- `RawImage weaponImage`（Raw图像 weapon图像）(偏移: 0x14)
- `RawImage extraImage`（Raw图像 extra图像）(偏移: 0x18)
- `Vector2 wpnOriginPos`（二维向量 武器OriginPos）(偏移: 0x0)
- `Vector2 wpnOffsetPos`（二维向量 武器OffsetPos）(偏移: 0x8)

### 方法 (8)

- `Color get_curColor()`
  （颜色 get_cur颜色（））
- `void set_curColor(Color value)`
  （void set_cur颜色（颜色 value））
- `void Awake()`
  （void 唤醒（））
- `void Update()`
  （void 更新（））
- `void SetSprite(WpnSpriteAsset spriteAsset)`
  （void 集合精灵（武器精灵资产 spriteAsset））
- `void Clean()`
  （void Clean（））
- `void ForwardAnim()`
  （void 前进动画（））
- `void BackAnim()`
  （void 后动画（））

---

## HableCurve（HableCurve）

### 字段 (2)

- `HableCurve.Segment[] segments`（HableCurve.Segment[] segments）(偏移: 0x18)
- `HableCurve.Uniforms uniforms`（HableCurve.Uniforms uniforms）(偏移: 0x1C)

### 方法 (14)

- `float get_whitePoint()`
  （float get_whitePoint（））
- `void set_whitePoint(float value)`
  （void set_whitePoint（float value））
- `float get_inverseWhitePoint()`
  （float get_inverseWhitePoint（））
- `void set_inverseWhitePoint(float value)`
  （void set_inverseWhitePoint（float value））
- `float get_x0()`
  （float get_x0（））
- `void set_x0(float value)`
  （void set_x0（float value））
- `float get_x1()`
  （float get_x1（））
- `void set_x1(float value)`
  （void set_x1（float value））
- `float Eval(float x)`
  （float Eval（float x））
- `void Init(float toeStrength, float toeLength, float shoulderStrength, float shoulderLength, float shoulderAngle, float gamma)`
  （void 初始化（float toeStrength, float toeLength, float shoulderStrength, float shoulderLength, float shoulderAngle, float gamma））
- `void InitSegments(HableCurve.DirectParams srcParams)`
  （void 初始化Segments（HableCurve.DirectParams srcParams））
- `void SolveAB(out float lnA, out float B, float x0, float y0, float m)`
  （void SolveAB（out float lnA, out float B, float x0, float y0, float m））
- `void AsSlopeIntercept(out float m, out float b, float x0, float x1, float y0, float y1)`
  （void AsSlopeIntercept（out float m, out float b, float x0, float x1, float y0, float y1））
- `float EvalDerivativeLinearGamma(float m, float b, float g, float x)`
  （float EvalDerivativeLinearGamma（float m, float b, float g, float x））

---

## HableCurve.DirectParams（HableCurve.DirectParams）

### 字段 (8)

- `float x0`（float x0）(偏移: 0x0)
- `float y0`（float y0）(偏移: 0x4)
- `float x1`（float x1）(偏移: 0x8)
- `float y1`（float y1）(偏移: 0xC)
- `float W`（float W）(偏移: 0x10)
- `float overshootX`（float overshootX）(偏移: 0x14)
- `float overshootY`（float overshootY）(偏移: 0x18)
- `float gamma`（float gamma）(偏移: 0x1C)

---

## HableCurve.Segment（HableCurve.Segment）

### 字段 (6)

- `float offsetX`（float offsetX）(偏移: 0x8)
- `float offsetY`（float offsetY）(偏移: 0xC)
- `float scaleX`（float scaleX）(偏移: 0x10)
- `float scaleY`（float scaleY）(偏移: 0x14)
- `float lnA`（float lnA）(偏移: 0x18)
- `float B`（float B）(偏移: 0x1C)

### 方法 (1)

- `float Eval(float x)`
  （float Eval（float x））

---

## HableCurve.Uniforms（HableCurve.Uniforms）

### 字段 (1)

- `HableCurve parent`（HableCurve parent）(偏移: 0x8)

### 方法 (7)

- `Vector4 get_curve()`
  （Vector4 get_curve（））
- `Vector4 get_toeSegmentA()`
  （Vector4 get_toeSegmentA（））
- `Vector4 get_toeSegmentB()`
  （Vector4 get_toeSegmentB（））
- `Vector4 get_midSegmentA()`
  （Vector4 get_midSegmentA（））
- `Vector4 get_midSegmentB()`
  （Vector4 get_midSegmentB（））
- `Vector4 get_shoSegmentA()`
  （Vector4 get_shoSegmentA（））
- `Vector4 get_shoSegmentB()`
  （Vector4 get_shoSegmentB（））

---

## HaltonSequence（HaltonSequence）

### 方法 (1)

- `float Get(int index, int radix)`
  （float 获取（int index, int radix））

---

## Hand（手部）

**继承**: IEquatable<Hand>（IEquatable<Hand>）

### 字段 (2)

- `ulong m_DeviceId`（无符号长整数 m_设备ID）(偏移: 0x0)
- `uint m_FeatureIndex`（uint m_Feature索引）(偏移: 0x8)

### 方法 (5)

- `ulong get_deviceId()`
  （无符号长整数 获取_设备ID（））
- `uint get_featureIndex()`
  （uint get_feature索引（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(Hand other)`
  （bool Equals（手部 other））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## HandPoser（手部Poser）

**继承**: Poser（Poser）

### 字段 (5)

- `Transform[] children`（Transform[] children）(偏移: 0x30)
- `Transform _poseRoot`（变换 _pose根）(偏移: 0x34)
- `Transform[] poseChildren`（Transform[] poseChildren）(偏移: 0x38)
- `Vector3[] defaultLocalPositions`（Vector3[] default本地的Positions）(偏移: 0x3C)
- `Quaternion[] defaultLocalRotations`（Quaternion[] default本地的Rotations）(偏移: 0x40)

### 方法 (5)

- `void AutoMapping()`
  （void 自动Mapping（））
- `void InitiatePoser()`
  （void InitiatePoser（））
- `void FixPoserTransforms()`
  （void FixPoserTransforms（））
- `void UpdatePoser()`
  （void 更新Poser（））
- `void StoreDefaultState()`
  （void 商店默认的状态（））

---

## Handles（Handles）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Hash128（Hash128）

**继承**: IComparable, IComparable<Hash128>, IEquatable<Hash128>（IComparable, IComparable<Hash128>, IEquatable<Hash128>）

### 字段 (4)

- `uint m_u32_0`（uint m_u32_0）(偏移: 0x0)
- `uint m_u32_1`（uint m_u32_1）(偏移: 0x4)
- `uint m_u32_2`（uint m_u32_2）(偏移: 0x8)
- `uint m_u32_3`（uint m_u32_3）(偏移: 0xC)

### 方法 (14)

- `ulong get_u64_0()`
  （ulong get_u64_0（））
- `ulong get_u64_1()`
  （ulong get_u64_1（））
- `bool get_isValid()`
  （布尔值 获取_是否有效（））
- `int CompareTo(Hash128 rhs)`
  （int CompareTo（Hash128 rhs））
- `string ToString()`
  （字符串 转字符串（））
- `string Hash128ToStringImpl(Hash128 hash)`
  （string Hash128To字符串Impl（Hash128 hash））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(Hash128 obj)`
  （bool Equals（Hash128 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `int CompareTo(object obj)`
  （整数 比较到（对象 obj））
- `bool op_Equality(Hash128 hash1, Hash128 hash2)`
  （bool op_Equality（Hash128 hash1, Hash128 hash2））
- `bool op_LessThan(Hash128 x, Hash128 y)`
  （bool op_LessThan（Hash128 x, Hash128 y））
- `bool op_GreaterThan(Hash128 x, Hash128 y)`
  （bool op_GreaterThan（Hash128 x, Hash128 y））
- `string Hash128ToStringImpl_Injected(ref Hash128 hash)`
  （string Hash128To字符串Impl_Injected（ref Hash128 hash））

---

## HashAlgorithm（HashAlgorithm）

**继承**: IDisposable, ICryptoTransform（IDisposable, ICrypto变换）

### 字段 (4)

- `int HashSizeValue`（int Hash大小值）(偏移: 0x8)
- `byte[] HashValue`（byte[] Hash值）(偏移: 0xC)
- `int State`（int 状态）(偏移: 0x10)
- `bool m_bDisposed`（bool m_bDisposed）(偏移: 0x14)

### 方法 (8)

- `byte[] ComputeHash(byte[] buffer)`
  （byte[] ComputeHash（byte[] buffer））
- `int get_InputBlockSize()`
  （int get_输入Block大小（））
- `int get_OutputBlockSize()`
  （int get_OutputBlock大小（））
- `bool get_CanTransformMultipleBlocks()`
  （bool get_能否变换MultipleBlocks（））
- `int TransformBlock(byte[] inputBuffer, int inputOffset, int inputCount, byte[] outputBuffer, int outputOffset)`
  （int 变换Block（byte[] inputBuffer, int inputOffset, int inputCount, byte[] outputBuffer, int outputOffset））
- `byte[] TransformFinalBlock(byte[] inputBuffer, int inputOffset, int inputCount)`
  （byte[] 变换FinalBlock（byte[] inputBuffer, int inputOffset, int inputCount））
- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））

---

## HashCodeHelper（HashCode辅助器）

### 方法 (1)

- `int Combine(int hash1, int hash2)`
  （int Combine（int hash1, int hash2））

---

## HashHelpers（HashHelpers）

### 字段 (1)

- `int RandomSeed`（int 随机Seed）(偏移: 0x0)

### 方法 (1)

- `int Combine(int h1, int h2)`
  （int Combine（int h1, int h2））

---

## HashHelpers（HashHelpers）

### 字段 (1)

- `int[] primes`（int[] primes）(偏移: 0x0)

### 方法 (3)

- `bool IsPrime(int candidate)`
  （bool 是否Prime（int candidate））
- `int GetPrime(int min)`
  （int 获取Prime（int min））
- `int ExpandPrime(int oldSize)`
  （int ExpandPrime（int oldSize））

---

## HashUnsafeUtilities（HashUnsafeUtilities）

### 方法 (2)

- `void ComputeHash128(void* data, ulong dataSize, ulong* hash1, ulong* hash2)`
  （void ComputeHash128（void* data, ulong dataSize, ulong* hash1, ulong* hash2））
- `void ComputeHash128(void* data, ulong dataSize, Hash128* hash)`
  （void ComputeHash128（void* data, ulong dataSize, Hash128* hash））

---

## HashUtilities（HashUtilities）

### 方法 (1)

- `void AppendHash(ref Hash128 inHash, ref Hash128 outHash)`
  （void AppendHash（ref Hash128 inHash, ref Hash128 outHash））

---

## HashUtility（Hash工具）

### 方法 (5)

- `int CombineHash(int h1, int h2)`
  （int CombineHash（int h1, int h2））
- `int CombineHash(int h1, int h2, int h3)`
  （int CombineHash（int h1, int h2, int h3））
- `int CombineHash(int h1, int h2, int h3, int h4)`
  （int CombineHash（int h1, int h2, int h3, int h4））
- `int CombineHash(int h1, int h2, int h3, int h4, int h5)`
  （int CombineHash（int h1, int h2, int h3, int h4, int h5））
- `int CombineHash(int h1, int h2, int h3, int h4, int h5, int h6)`
  （int CombineHash（int h1, int h2, int h3, int h4, int h5, int h6））

---

## Hashtable（Hashtable）

**继承**: IDictionary, ICollection, IEnumerable, ISerializable, IDeserializationCallback, ICloneable（I字典, ICollection, IEnumerable, ISerializable, IDeserialization回调, ICloneable）

### 字段 (11)

- `Hashtable.bucket[] buckets`（Hashtable.bucket[] buckets）(偏移: 0x8)
- `int count`（整数 数量）(偏移: 0xC)
- `int occupancy`（int occupancy）(偏移: 0x10)
- `int loadsize`（int loadsize）(偏移: 0x14)
- `float loadFactor`（float load系数）(偏移: 0x18)
- `int version`（整数 版本）(偏移: 0x1C)
- `bool isWriterInProgress`（bool is写入器InProgress）(偏移: 0x20)
- `ICollection keys`（ICollection keys）(偏移: 0x24)
- `ICollection values`（ICollection values）(偏移: 0x28)
- `IEqualityComparer _keycomparer`（IEqualityComparer _keycomparer）(偏移: 0x2C)
- `object _syncRoot`（对象 _同步根）(偏移: 0x30)

### 方法 (30)

- `uint InitHash(object key, int hashsize, out uint seed, out uint incr)`
  （uint 初始化Hash（object key, int hashsize, out uint seed, out uint incr））
- `void Add(object key, object value)`
  （void 添加（对象 key, 对象 value））
- `void Clear()`
  （void 清除（））
- `object Clone()`
  （对象 克隆（））
- `bool Contains(object key)`
  （布尔值 包含（对象 key））
- `bool ContainsKey(object key)`
  （bool Contains键（object key））
- `void CopyKeys(Array array, int arrayIndex)`
  （void 复制Keys（数组 array, int arrayIndex））
- `void CopyEntries(Array array, int arrayIndex)`
  （void 复制Entries（数组 array, int arrayIndex））
- `void CopyTo(Array array, int arrayIndex)`
  （void 复制到（数组 array, 整数 arrayIndex））
- `KeyValuePairs[] ToKeyValuePairsArray()`
  （键值Pairs[] To键值Pairs数组（））
- `void CopyValues(Array array, int arrayIndex)`
  （void 复制Values（数组 array, int arrayIndex））
- `object get_Item(object key)`
  （对象 获取_项（对象 key））
- `void set_Item(object key, object value)`
  （void 设置_项（对象 key, 对象 value））
- `void expand()`
  （void expand（））
- `void rehash()`
  （void rehash（））
- `void UpdateVersion()`
  （void 更新Version（））
- `void rehash(int newsize, bool forceNewHashCode)`
  （void rehash（int newsize, bool forceNewHashCode））
- `IDictionaryEnumerator GetEnumerator()`
  （I字典枚举器 获取枚举器（））
- `int GetHash(object key)`
  （int 获取Hash（object key））
- `bool KeyEquals(object item, object key)`
  （bool 键Equals（object item, object key））
- `ICollection get_Keys()`
  （ICollection get_Keys（））
- `ICollection get_Values()`
  （ICollection get_Values（））
- `void Insert(object key, object nvalue, bool add)`
  （void Insert（object key, object nvalue, bool add））
- `void putEntry(Hashtable.bucket[] newBuckets, object key, object nvalue, int hashcode)`
  （void putEntry（Hashtable.bucket[] newBuckets, object key, object nvalue, int hashcode））
- `void Remove(object key)`
  （void 移除（对象 key））
- `object get_SyncRoot()`
  （对象 获取_同步根（））
- `int get_Count()`
  （整数 获取_数量（））
- `Hashtable Synchronized(Hashtable table)`
  （Hashtable Synchronized（Hashtable table））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））
- `void OnDeserialization(object sender)`
  （void 反序列化时（对象 sender））

---

## Hashtable.HashtableDebugView（Hashtable.HashtableDebug视图）

### 字段 (1)

- `Hashtable hashtable`（Hashtable hashtable）(偏移: 0x8)

### 方法 (1)

- `KeyValuePairs[] get_Items()`
  （键值Pairs[] get_Items（））

---

## Hashtable.HashtableEnumerator（Hashtable.HashtableEnumerator）

**继承**: IDictionaryEnumerator, IEnumerator, ICloneable（I字典Enumerator, IEnumerator, ICloneable）

### 字段 (7)

- `Hashtable hashtable`（Hashtable hashtable）(偏移: 0x8)
- `int bucket`（int bucket）(偏移: 0xC)
- `int version`（整数 版本）(偏移: 0x10)
- `bool current`（bool current）(偏移: 0x14)
- `int getObjectRetType`（int get对象Ret类型）(偏移: 0x18)
- `object currentKey`（object current键）(偏移: 0x1C)
- `object currentValue`（object current值）(偏移: 0x20)

### 方法 (7)

- `object Clone()`
  （对象 克隆（））
- `object get_Key()`
  （对象 获取_键（））
- `bool MoveNext()`
  （布尔值 移动下一个（））
- `DictionaryEntry get_Entry()`
  （字典项 获取_项（））
- `object get_Current()`
  （对象 获取_当前（））
- `object get_Value()`
  （对象 获取_值（））
- `void Reset()`
  （void 重置（））

---

## Hashtable.KeyCollection（Hashtable.键Collection）

**继承**: ICollection, IEnumerable（ICollection, IEnumerable）

### 字段 (1)

- `Hashtable _hashtable`（Hashtable _hashtable）(偏移: 0x8)

### 方法 (4)

- `void CopyTo(Array array, int arrayIndex)`
  （void 复制到（数组 array, 整数 arrayIndex））
- `IEnumerator GetEnumerator()`
  （IEnumerator 获取枚举器（））
- `object get_SyncRoot()`
  （对象 获取_同步根（））
- `int get_Count()`
  （整数 获取_数量（））

---

## Hashtable.SyncHashtable（Hashtable.同步Hashtable）

**继承**: Hashtable, IEnumerable（Hashtable, IEnumerable）

### 字段 (1)

- `Hashtable _table`（Hashtable _table）(偏移: 0x34)

### 方法 (17)

- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））
- `int get_Count()`
  （整数 获取_数量（））
- `object get_Item(object key)`
  （对象 获取_项（对象 key））
- `void set_Item(object key, object value)`
  （void 设置_项（对象 key, 对象 value））
- `object get_SyncRoot()`
  （对象 获取_同步根（））
- `void Add(object key, object value)`
  （void 添加（对象 key, 对象 value））
- `void Clear()`
  （void 清除（））
- `bool Contains(object key)`
  （布尔值 包含（对象 key））
- `bool ContainsKey(object key)`
  （bool Contains键（object key））
- `void CopyTo(Array array, int arrayIndex)`
  （void 复制到（数组 array, 整数 arrayIndex））
- `object Clone()`
  （对象 克隆（））
- `IDictionaryEnumerator GetEnumerator()`
  （I字典枚举器 获取枚举器（））
- `ICollection get_Keys()`
  （ICollection get_Keys（））
- `ICollection get_Values()`
  （ICollection get_Values（））
- `void Remove(object key)`
  （void 移除（对象 key））
- `void OnDeserialization(object sender)`
  （void 反序列化时（对象 sender））
- `KeyValuePairs[] ToKeyValuePairsArray()`
  （键值Pairs[] To键值Pairs数组（））

---

## Hashtable.ValueCollection（Hashtable.值Collection）

**继承**: ICollection, IEnumerable（ICollection, IEnumerable）

### 字段 (1)

- `Hashtable _hashtable`（Hashtable _hashtable）(偏移: 0x8)

### 方法 (4)

- `void CopyTo(Array array, int arrayIndex)`
  （void 复制到（数组 array, 整数 arrayIndex））
- `IEnumerator GetEnumerator()`
  （IEnumerator 获取枚举器（））
- `object get_SyncRoot()`
  （对象 获取_同步根（））
- `int get_Count()`
  （整数 获取_数量（））

---

## Hashtable.bucket（Hashtable.bucket）

### 字段 (3)

- `object key`（对象 key）(偏移: 0x0)
- `object val`（object val）(偏移: 0x4)
- `int hash_coll`（int hash_coll）(偏移: 0x8)

---

## HeadShotType（头部射击类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Header（标题）

### 字段 (4)

- `string HeaderNamespace`（string 标题Namespace）(偏移: 0x8)
- `bool MustUnderstand`（bool MustUnderstand）(偏移: 0xC)
- `string Name`（string 名称）(偏移: 0x10)
- `object Value`（object 值）(偏移: 0x14)

---

## HeaderAttribute（标题Attribute）

**继承**: PropertyAttribute（属性特性）

### 字段 (1)

- `string header`（string header）(偏移: 0x8)

---

## HeaderHandler（标题处理器）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `object Invoke(Header[] headers)`
  （object Invoke（Header[] headers））
- `IAsyncResult BeginInvoke(Header[] headers, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Header[] headers, 异步回调 callback, object object））
- `object EndInvoke(IAsyncResult result)`
  （object 结束Invoke（I异步Result result））

---

## HeadingTracker（HeadingTracker）

### 字段 (9)

- `HeadingTracker.Item[] mHistory`（HeadingTracker.Item[] mHistory）(偏移: 0x8)
- `int mTop`（int m顶部）(偏移: 0xC)
- `int mBottom`（int m底部）(偏移: 0x10)
- `int mCount`（int m数量）(偏移: 0x14)
- `Vector3 mHeadingSum`（三维向量 mHeadingSum）(偏移: 0x18)
- `float mWeightSum`（float mWeightSum）(偏移: 0x24)
- `float mWeightTime`（float mWeight时间）(偏移: 0x28)
- `Vector3 mLastGoodHeading`（三维向量 m最后一个GoodHeading）(偏移: 0x2C)
- `float mDecayExponent`（float m衰减Exponent）(偏移: 0x0)

### 方法 (7)

- `int get_FilterSize()`
  （int get_Filter大小（））
- `void ClearHistory()`
  （void 清除History（））
- `float Decay(float time)`
  （float 衰减（float time））
- `void Add(Vector3 velocity)`
  （void 添加（三维向量 velocity））
- `void PopBottom()`
  （void Pop底部（））
- `void DecayHistory()`
  （void 衰减History（））
- `Vector3 GetReliableHeading()`
  （三维向量 获取ReliableHeading（））

---

## HeadingTracker.Item（HeadingTracker.项目）

### 字段 (3)

- `Vector3 velocity`（三维向量 速度）(偏移: 0x0)
- `float weight`（浮点数 权重）(偏移: 0xC)
- `float time`（float time）(偏移: 0x10)

---

## HealthData（Health数据）

### 字段 (4)

- `ObscuredInt currentHealth`（模糊整数 currentHealth）(偏移: 0x8)
- `ObscuredInt maxHealth`（模糊整数 maxHealth）(偏移: 0x1C)
- `ObscuredInt tempHealth`（模糊整数 tempHealth）(偏移: 0x30)
- `float invinsibleEndTime`（float invinsible结束时间）(偏移: 0x44)

### 方法 (11)

- `float get_rate()`
  （float get_rate（））
- `bool get_isDead()`
  （布尔值 获取_是否死亡（））
- `bool get_isMaxHP()`
  （bool get_is最大HP（））
- `void Heal(int value)`
  （void Heal（int value））
- `void Heal()`
  （void Heal（））
- `void Hurt(int value)`
  （void Hurt（int value））
- `void SetHealthMax(int value, bool heal = True)`
  （void 集合Health最大（int value, bool heal = True））
- `void AddHealthMax(int addHP, bool heal = True)`
  （void 添加Health最大（int addHP, bool heal = True））
- `void SetHealthMaxWithoutTempHealth(int value, bool heal = True)`
  （void 集合Health最大WithoutTempHealth（int value, bool heal = True））
- `void AddTempHealth(int addValue)`
  （void 添加TempHealth（int addValue））
- `void ClearTempHealth()`
  （void 清除TempHealth（））

---

## HebrewNumber（HebrewNumber）

### 字段 (3)

- `HebrewNumber.HebrewValue[] HebrewValues`（HebrewNumber.HebrewValue[] HebrewValues）(偏移: 0x0)
- `char maxHebrewNumberCh`（char maxHebrewNumberCh）(偏移: 0x4)
- `HebrewNumber.HS[][] NumberPasingState`（HebrewNumber.HS[][] NumberPasing状态）(偏移: 0x8)

### 方法 (3)

- `string ToString(int Number)`
  （string To字符串（int Number））
- `HebrewNumberParsingState ParseByChar(char ch, ref HebrewNumberParsingContext context)`
  （HebrewNumberParsing状态 解析ByChar（char ch, ref HebrewNumberParsingContext context））
- `bool IsDigit(char ch)`
  （bool 是否Digit（char ch））

---

## HebrewNumber.HS（HebrewNumber.HS）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## HebrewNumber.HebrewToken（HebrewNumber.Hebrew令牌）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## HebrewNumber.HebrewValue（HebrewNumber.Hebrew值）

### 字段 (2)

- `HebrewNumber.HebrewToken token`（HebrewNumber.Hebrew令牌 token）(偏移: 0x8)
- `int value`（整数 value）(偏移: 0xC)

---

## HebrewNumberParsingContext（HebrewNumberParsingContext）

### 字段 (2)

- `HebrewNumber.HS state`（HebrewNumber.HS state）(偏移: 0x0)
- `int result`（int result）(偏移: 0x4)

---

## HebrewNumberParsingState（HebrewNumberParsing状态）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Helmet（头盔）

**继承**: SocketItem（套接字项目）

### 字段 (2)

- `Collider helmetCollider`（碰撞器 helmet碰撞器）(偏移: 0x10)
- `Rigidbody rigidBody`（刚体 rigid身体）(偏移: 0x14)

### 方法 (3)

- `void Awake()`
  （void 唤醒（））
- `void BindOnCharacter(CharacterModel characterModel)`
  （void BindOn角色（角色模型 characterModel））
- `void Drop()`
  （void Drop（））

---

## HelpURLAttribute（HelpURLAttribute）

**继承**: Attribute（属性）

### 字段 (3)

- `string m_Url`（string m_Url）(偏移: 0x8)
- `bool m_Dispatcher`（bool m_Dispatcher）(偏移: 0xC)
- `string m_DispatchingFieldName`（string m_DispatchingField名称）(偏移: 0x10)

---

## HeroCharacterEffect（英雄角色特效）

**继承**: CharacterEffect（角色特效）

### 方法 (1)

- `void SetEffectState(bool active)`
  （void 集合特效状态（bool active））

---

## Heuristic（Heuristic）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## HeuristicOptimizationMode（HeuristicOptimization模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## HideFlags（隐藏Flags）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## HierarchicalGraph（HierarchicalGraph）

### 字段 (15)

- `List<GraphNode>[] children`（List<GraphNode>[] children）(偏移: 0x8)
- `List<int>[] connections`（List<int>[] connections）(偏移: 0xC)
- `int[] areas`（int[] areas）(偏移: 0x10)
- `byte[] dirty`（byte[] dirty）(偏移: 0x14)
- `Action onConnectedComponentsChanged`（动作 onConnectedComponentsChanged）(偏移: 0x1C)
- `Action<GraphNode> connectionCallback`（Action<GraphNode> connection回调）(偏移: 0x20)
- `Queue<GraphNode> temporaryQueue`（Queue<GraphNode> temporary队列）(偏移: 0x24)
- `List<GraphNode> currentChildren`（List<GraphNode> currentChildren）(偏移: 0x28)
- `List<int> currentConnections`（List<int> currentConnections）(偏移: 0x2C)
- `int currentHierarchicalNodeIndex`（int currentHierarchical节点索引）(偏移: 0x30)
- `Stack<int> temporaryStack`（Stack<int> temporary栈）(偏移: 0x34)
- `int numDirtyNodes`（int numDirtyNodes）(偏移: 0x38)
- `GraphNode[] dirtyNodes`（GraphNode[] dirtyNodes）(偏移: 0x3C)
- `Stack<int> freeNodeIndices`（Stack<int> free节点Indices）(偏移: 0x40)
- `int gizmoVersion`（int gizmoVersion）(偏移: 0x44)

### 方法 (15)

- `int get_version()`
  （int get_version（））
- `void set_version(int value)`
  （void set_version（int value））
- `void Grow()`
  （void Grow（））
- `int GetHierarchicalNodeIndex()`
  （int 获取Hierarchical节点索引（））
- `void OnCreatedNode(GraphNode node)`
  （void OnCreated节点（Graph节点 node））
- `void AddDirtyNode(GraphNode node)`
  （void 添加Dirty节点（Graph节点 node））
- `int get_NumConnectedComponents()`
  （int get_NumConnectedComponents（））
- `void set_NumConnectedComponents(int value)`
  （void set_NumConnectedComponents（int value））
- `uint GetConnectedComponent(int hierarchicalNodeIndex)`
  （uint 获取Connected组件（int hierarchicalNodeIndex））
- `void RemoveHierarchicalNode(int hierarchicalNode, bool removeAdjacentSmallNodes)`
  （void 移除Hierarchical节点（int hierarchicalNode, bool removeAdjacentSmallNodes））
- `void RecalculateIfNecessary()`
  （void RecalculateIfNecessary（））
- `void RecalculateAll()`
  （void Recalculate所有（））
- `void FloodFill()`
  （void FloodFill（））
- `void FindHierarchicalNodeChildren(int hierarchicalNode, GraphNode startNode)`
  （void 查找Hierarchical节点Children（int hierarchicalNode, Graph节点 startNode））
- `void OnDrawGizmos(RetainedGizmos gizmos)`
  （void OnDrawGizmos（RetainedGizmos gizmos））

---

## Hierarchy（Hierarchy）

### 方法 (10)

- `bool HierarchyIsValid(Transform[] bones)`
  （bool Hierarchy是否Valid（Transform[] bones））
- `Object ContainsDuplicate(Object[] objects)`
  （对象 ContainsDuplicate（Object[] objects））
- `bool IsAncestor(Transform transform, Transform ancestor)`
  （bool 是否Ancestor（变换 transform, 变换 ancestor））
- `bool ContainsChild(Transform transform, Transform child)`
  （bool Contains子级（变换 transform, 变换 child））
- `void AddAncestors(Transform transform, Transform blocker, ref Transform[] array)`
  （void 添加Ancestors（变换 transform, 变换 blocker, ref Transform[] array））
- `Transform GetAncestor(Transform transform, int minChildCount)`
  （变换 获取Ancestor（变换 transform, int minChildCount））
- `Transform GetFirstCommonAncestor(Transform t1, Transform t2)`
  （变换 获取第一个CommonAncestor（变换 t1, 变换 t2））
- `Transform GetFirstCommonAncestor(Transform[] transforms)`
  （变换 获取第一个CommonAncestor（Transform[] transforms））
- `Transform GetFirstCommonAncestorRecursive(Transform transform, Transform[] transforms)`
  （变换 获取第一个CommonAncestorRecursive（变换 transform, Transform[] transforms））
- `bool IsCommonAncestor(Transform transform, Transform[] transforms)`
  （bool 是否CommonAncestor（变换 transform, Transform[] transforms））

---

## HijriCalendar（HijriCalendar）

**继承**: Calendar（日历）

### 字段 (5)

- `int HijriEra`（int HijriEra）(偏移: 0x0)
- `int[] HijriMonthDays`（int[] HijriMonthDays）(偏移: 0x4)
- `int m_HijriAdvance`（int m_HijriAdvance）(偏移: 0x14)
- `DateTime calendarMinValue`（Date时间 calendar最小值）(偏移: 0x8)
- `DateTime calendarMaxValue`（Date时间 calendar最大值）(偏移: 0x10)

### 方法 (25)

- `DateTime get_MinSupportedDateTime()`
  （日期时间 获取_最小支持日期时间（））
- `DateTime get_MaxSupportedDateTime()`
  （日期时间 获取_最大支持日期时间（））
- `int get_ID()`
  （整数 获取_ID（））
- `long GetAbsoluteDateHijri(int y, int m, int d)`
  （long 获取AbsoluteDateHijri（int y, int m, int d））
- `long DaysUpToHijriYear(int HijriYear)`
  （long Days上ToHijriYear（int HijriYear））
- `int get_HijriAdjustment()`
  （int get_HijriAdjustment（））
- `int GetAdvanceHijriDate()`
  （int 获取AdvanceHijriDate（））
- `void CheckTicksRange(long ticks)`
  （void 检查Ticks范围（long ticks））
- `void CheckEraRange(int era)`
  （void 检查Era范围（int era））
- `void CheckYearRange(int year, int era)`
  （void 检查Year范围（int year, int era））
- `void CheckYearMonthRange(int year, int month, int era)`
  （void 检查YearMonth范围（int year, int month, int era））
- `int GetDatePart(long ticks, int part)`
  （int 获取DatePart（long ticks, int part））
- `int GetDayOfMonth(DateTime time)`
  （整数 获取_月中的日（日期时间 time））
- `DayOfWeek GetDayOfWeek(DateTime time)`
  （星期几 获取星期几（日期时间 time））
- `int GetDaysInMonth(int year, int month, int era)`
  （整数 获取_月中的天数（整数 year, 整数 month, 整数 era））
- `int GetDaysInYear(int year, int era)`
  （整数 获取_年中的天数（整数 year, 整数 era））
- `int GetEra(DateTime time)`
  （整数 获取_纪元（日期时间 time））
- `int[] get_Eras()`
  （整数[] 获取_纪元（））
- `int GetMonth(DateTime time)`
  （整数 获取_月（日期时间 time））
- `int GetMonthsInYear(int year, int era)`
  （整数 获取_年中的月数（整数 year, 整数 era））
- `int GetYear(DateTime time)`
  （整数 获取_年（日期时间 time））
- `bool IsLeapYear(int year, int era)`
  （布尔值 是否闰年（整数 year, 整数 era））
- `DateTime ToDateTime(int year, int month, int day, int hour, int minute, int second, int millisecond, int era)`
  （日期时间 转日期时间（整数 year, 整数 month, 整数 day, 整数 hour, 整数 minute, 整数 second, 整数 millisecond, 整数 era））
- `int get_TwoDigitYearMax()`
  （整数 获取_两位数年份最大（））
- `int ToFourDigitYear(int year)`
  （整数 转四位数年份（整数 year））

---

## HitReaction（命中Reaction）

**继承**: OffsetModifier（偏移修改器）

### 字段 (2)

- `HitReaction.HitPointEffector[] effectorHitPoints`（命中Reaction.命中PointEffector[] effector命中Points）(偏移: 0x18)
- `HitReaction.HitPointBone[] boneHitPoints`（命中Reaction.命中PointBone[] bone命中Points）(偏移: 0x1C)

### 方法 (3)

- `bool get_inProgress()`
  （bool get_inProgress（））
- `void OnModifyOffset()`
  （void 修改偏移时（））
- `void Hit(Collider collider, Vector3 force, Vector3 point)`
  （void 命中（碰撞器 collider, 三维向量 force, 三维向量 point））

---

