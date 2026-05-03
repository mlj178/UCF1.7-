# 游戏类定义 (Part 14/21)

共 200 个类 (总序号 2601 - 2800)

---

## RandomUse（随机Use）

**继承**: BotSkillBase（机器人技能基础）

### 字段 (2)

- `float minCheckTime`（float min检查时间）(偏移: 0x18)
- `float maxCheckTime`（float max检查时间）(偏移: 0x1C)

### 方法 (1)

- `bool CanDo()`
  （布尔值 能否执行（））

---

## RangeAttribute（范围Attribute）

**继承**: PropertyAttribute（属性特性）

### 字段 (2)

- `float min`（浮点数 最小值）(偏移: 0x8)
- `float max`（浮点数 最大值）(偏移: 0xC)

---

## RangeInt（范围整数）

### 字段 (2)

- `int start`（int start）(偏移: 0x0)
- `int length`（整数 长度）(偏移: 0x4)

### 方法 (1)

- `int get_end()`
  （int get_end（））

---

## RankField（排名Field）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (3)

- `GameObject prefab`（游戏对象 预制体）(偏移: 0xC)
- `SimpleObjectPool pool`（Simple对象池 pool）(偏移: 0x10)
- `List<TabScoreBoard_PlayerData> list`（List<Tab分数Board_玩家Data> list）(偏移: 0x14)

### 方法 (4)

- `TabScoreBoard_PlayerData AddPlayer(Player player)`
  （Tab分数Board_玩家数据 添加玩家（玩家 player））
- `void TryRerank(TabScoreBoard_PlayerData target)`
  （void TryRerank（Tab分数Board_玩家数据 target））
- `TabScoreBoard_PlayerData FindDataByPlayer(Player player)`
  （Tab分数Board_玩家数据 查找数据By玩家（玩家 player））
- `TabScoreBoard_PlayerData FindPlayerByRank(int rank)`
  （Tab分数Board_玩家数据 查找玩家By排名（int rank））

---

## RasterState（Raster状态）

**继承**: IEquatable<RasterState>（IEquatable<RasterState>）

### 字段 (8)

- `RasterState defaultValue`（Raster状态 default值）(偏移: 0x0)
- `CullMode m_CullingMode`（Cull模式 m_Culling模式）(偏移: 0x0)
- `int m_OffsetUnits`（int m_OffsetUnits）(偏移: 0x4)
- `float m_OffsetFactor`（float m_Offset系数）(偏移: 0x8)
- `byte m_DepthClip`（byte m_深度弹匣）(偏移: 0xC)
- `byte m_Conservative`（byte m_Conservative）(偏移: 0xD)
- `byte m_Padding1`（byte m_Padding1）(偏移: 0xE)
- `byte m_Padding2`（byte m_Padding2）(偏移: 0xF)

### 方法 (3)

- `bool Equals(RasterState other)`
  （bool Equals（Raster状态 other））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## RasterizationMesh（Rasterization网格）

### 字段 (9)

- `MeshFilter original`（网格Filter original）(偏移: 0x8)
- `int area`（整数 面积）(偏移: 0xC)
- `Vector3[] vertices`（Vector3[] vertices）(偏移: 0x10)
- `int[] triangles`（int[] triangles）(偏移: 0x14)
- `int numVertices`（int numVertices）(偏移: 0x18)
- `int numTriangles`（int numTriangles）(偏移: 0x1C)
- `Bounds bounds`（边界 bounds）(偏移: 0x20)
- `Matrix4x4 matrix`（Matrix4x4 matrix）(偏移: 0x38)
- `bool pool`（bool pool）(偏移: 0x78)

### 方法 (2)

- `void RecalculateBounds()`
  （void RecalculateBounds（））
- `void Pool()`
  （void 池（））

---

## RawImage（Raw图像）

**继承**: MaskableGraphic（MaskableGraphic）

### 字段 (2)

- `Texture m_Texture`（纹理 m_纹理）(偏移: 0x80)
- `Rect m_UVRect`（Rect m_UVRect）(偏移: 0x84)

### 方法 (8)

- `Texture get_mainTexture()`
  （纹理 获取_主纹理（））
- `Texture get_texture()`
  （纹理 get_texture（））
- `void set_texture(Texture value)`
  （void set_texture（纹理 value））
- `Rect get_uvRect()`
  （Rect get_uvRect（））
- `void set_uvRect(Rect value)`
  （void set_uvRect（Rect value））
- `void SetNativeSize()`
  （void 集合Native大小（））
- `void OnPopulateMesh(VertexHelper vh)`
  （void OnPopulate网格（Vertex辅助器 vh））
- `void OnDidApplyAnimationProperties()`
  （void 已应用动画属性时（））

---

## Ray（Ray）

**继承**: IFormattable（I可格式化）

### 字段 (2)

- `Vector3 m_Origin`（三维向量 m_Origin）(偏移: 0x0)
- `Vector3 m_Direction`（三维向量 m_方向）(偏移: 0xC)

### 方法 (6)

- `Vector3 get_origin()`
  （三维向量 get_origin（））
- `Vector3 get_direction()`
  （三维向量 get_direction（））
- `void set_direction(Vector3 value)`
  （void set_direction（三维向量 value））
- `Vector3 GetPoint(float distance)`
  （三维向量 获取Point（float distance））
- `string ToString()`
  （字符串 转字符串（））
- `string ToString(string format, IFormatProvider formatProvider)`
  （字符串 转字符串（字符串 格式, I格式化提供者 formatProvider））

---

## RayDirection（Ray方向）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RaycastHit（Raycast命中）

### 字段 (6)

- `Vector3 m_Point`（三维向量 m_Point）(偏移: 0x0)
- `Vector3 m_Normal`（三维向量 m_法线）(偏移: 0xC)
- `uint m_FaceID`（uint m_FaceID）(偏移: 0x18)
- `float m_Distance`（float m_距离）(偏移: 0x1C)
- `Vector2 m_UV`（二维向量 m_UV）(偏移: 0x20)
- `int m_Collider`（整数 m_碰撞器）(偏移: 0x28)

### 方法 (9)

- `Collider get_collider()`
  （碰撞器 get_collider（））
- `Vector3 get_point()`
  （三维向量 获取_点（））
- `void set_point(Vector3 value)`
  （void set_point（三维向量 value））
- `Vector3 get_normal()`
  （三维向量 get_normal（））
- `void set_normal(Vector3 value)`
  （void set_normal（三维向量 value））
- `float get_distance()`
  （浮点数 获取_距离（））
- `void set_distance(float value)`
  （void set_distance（float value））
- `Transform get_transform()`
  （变换 获取_transform（））
- `Rigidbody get_rigidbody()`
  （刚体 get_rigidbody（））

---

## RaycastHit2D（RaycastHit2D）

### 字段 (6)

- `Vector2 m_Centroid`（二维向量 m_Centroid）(偏移: 0x0)
- `Vector2 m_Point`（二维向量 m_Point）(偏移: 0x8)
- `Vector2 m_Normal`（二维向量 m_法线）(偏移: 0x10)
- `float m_Distance`（float m_距离）(偏移: 0x18)
- `float m_Fraction`（float m_Fraction）(偏移: 0x1C)
- `int m_Collider`（整数 m_碰撞器）(偏移: 0x20)

### 方法 (5)

- `Vector2 get_point()`
  （二维向量 get_point（））
- `Vector2 get_normal()`
  （二维向量 get_normal（））
- `float get_distance()`
  （浮点数 获取_距离（））
- `Collider2D get_collider()`
  （Collider2D get_collider（））
- `bool op_Implicit(RaycastHit2D hit)`
  （bool op_Implicit（RaycastHit2D hit））

---

## RaycastModifier（Raycast修改器）

**继承**: MonoModifier（Mono修改器）

### 字段 (12)

- `bool useRaycasting`（bool useRaycasting）(偏移: 0x14)
- `LayerMask mask`（层掩码 mask）(偏移: 0x18)
- `bool thickRaycast`（bool thickRaycast）(偏移: 0x1C)
- `float thickRaycastRadius`（float thickRaycastRadius）(偏移: 0x20)
- `bool use2DPhysics`（bool use2D物理）(偏移: 0x24)
- `Vector3 raycastOffset`（三维向量 raycastOffset）(偏移: 0x28)
- `bool useGraphRaycasting`（bool useGraphRaycasting）(偏移: 0x34)
- `RaycastModifier.Quality quality`（RaycastModifier.Quality quality）(偏移: 0x38)
- `int[] iterationsByQuality`（int[] iterationsByQuality）(偏移: 0x0)
- `List<Vector3> buffer`（List<Vector3> buffer）(偏移: 0x4)
- `float[] DPCosts`（float[] DPCosts）(偏移: 0x8)
- `int[] DPParents`（int[] DPParents）(偏移: 0xC)

### 方法 (5)

- `int get_Order()`
  （整数 获取_顺序（））
- `void Apply(Path p)`
  （void 应用（路径 p））
- `List<Vector3> ApplyGreedy(Path p, List<Vector3> points)`
  （List<Vector3> 应用Greedy（路径 p, List<Vector3> points））
- `List<Vector3> ApplyDP(Path p, List<Vector3> points)`
  （List<Vector3> 应用DP（路径 p, List<Vector3> points））
- `bool ValidateLine(GraphNode n1, GraphNode n2, Vector3 v1, Vector3 v2)`
  （bool 验证Line（Graph节点 n1, Graph节点 n2, 三维向量 v1, 三维向量 v2））

---

## RaycastModifier.Quality（RaycastModifier.Quality）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RaycastResult（RaycastResult）

### 字段 (11)

- `GameObject m_GameObject`（游戏对象 m_游戏对象）(偏移: 0x0)
- `BaseRaycaster module`（基础Raycaster module）(偏移: 0x4)
- `float distance`（浮点数 距离）(偏移: 0x8)
- `float index`（float index）(偏移: 0xC)
- `int depth`（整数 深度）(偏移: 0x10)
- `int sortingLayer`（int sorting层）(偏移: 0x14)
- `int sortingOrder`（int sortingOrder）(偏移: 0x18)
- `Vector3 worldPosition`（三维向量 worldPosition）(偏移: 0x1C)
- `Vector3 worldNormal`（三维向量 world法线）(偏移: 0x28)
- `Vector2 screenPosition`（二维向量 screenPosition）(偏移: 0x34)
- `int displayIndex`（int display索引）(偏移: 0x3C)

### 方法 (5)

- `GameObject get_gameObject()`
  （游戏对象 获取_游戏对象（））
- `void set_gameObject(GameObject value)`
  （void set_game对象（游戏对象 value））
- `bool get_isValid()`
  （布尔值 获取_是否有效（））
- `void Clear()`
  （void 清除（））
- `string ToString()`
  （字符串 转字符串（））

---

## RaycasterManager（Raycaster管理器）

### 字段 (1)

- `List<BaseRaycaster> s_Raycasters`（List<基础Raycaster> s_Raycasters）(偏移: 0x0)

### 方法 (3)

- `void AddRaycaster(BaseRaycaster baseRaycaster)`
  （void 添加Raycaster（基础Raycaster baseRaycaster））
- `List<BaseRaycaster> GetRaycasters()`
  （List<基础Raycaster> 获取Raycasters（））
- `void RemoveRaycasters(BaseRaycaster baseRaycaster)`
  （void 移除Raycasters（基础Raycaster baseRaycaster））

---

## ReadObjectInfo（Read对象信息）

### 字段 (18)

- `int objectInfoId`（int object信息Id）(偏移: 0x8)
- `int readObjectInfoCounter`（int read对象信息Counter）(偏移: 0x0)
- `Type objectType`（类型 object类型）(偏移: 0xC)
- `ObjectManager objectManager`（对象管理器 object管理器）(偏移: 0x10)
- `int count`（整数 数量）(偏移: 0x14)
- `bool isSi`（bool isSi）(偏移: 0x18)
- `bool isNamed`（bool isNamed）(偏移: 0x0)
- `bool isTyped`（bool isTyped）(偏移: 0x0)
- `bool bSimpleAssembly`（bool bSimpleAssembly）(偏移: 0x0)
- `SerObjectInfoCache cache`（Ser对象信息缓存 cache）(偏移: 0x0)
- `string[] wireMemberNames`（string[] wireMemberNames）(偏移: 0x20)
- `Type[] wireMemberTypes`（Type[] wireMemberTypes）(偏移: 0x24)
- `int lastPosition`（int lastPosition）(偏移: 0x28)
- `ISerializationSurrogate serializationSurrogate`（ISerializationSurrogate serializationSurrogate）(偏移: 0x2C)
- `StreamingContext context`（StreamingContext context）(偏移: 0x30)
- `List<Type> memberTypesList`（List<Type> memberTypes列表）(偏移: 0x38)
- `SerObjectInfoInit serObjectInfoInit`（Ser对象信息初始化 ser对象信息初始化）(偏移: 0x3C)
- `IFormatterConverter formatterConverter`（IFormatterConverter formatterConverter）(偏移: 0x40)

### 方法 (20)

- `void ObjectEnd()`
  （void 对象结束（））
- `void PrepareForReuse()`
  （void PrepareForReuse（））
- `ReadObjectInfo Create(Type objectType, ISurrogateSelector surrogateSelector, StreamingContext context, ObjectManager objectManager, SerObjectInfoInit serObjectInfoInit, IFormatterConverter converter, bool bSimpleAssembly)`
  （Read对象信息 创建（类型 objectType, ISurrogateSelector surrogateSelector, StreamingContext context, 对象管理器 objectManager, Ser对象信息初始化 serObjectInfoInit, IFormatterConverter converter, bool bSimpleAssembly））
- `void Init(Type objectType, ISurrogateSelector surrogateSelector, StreamingContext context, ObjectManager objectManager, SerObjectInfoInit serObjectInfoInit, IFormatterConverter converter, bool bSimpleAssembly)`
  （void 初始化（类型 objectType, ISurrogateSelector surrogateSelector, StreamingContext context, 对象管理器 objectManager, Ser对象信息初始化 serObjectInfoInit, IFormatterConverter converter, bool bSimpleAssembly））
- `ReadObjectInfo Create(Type objectType, string[] memberNames, Type[] memberTypes, ISurrogateSelector surrogateSelector, StreamingContext context, ObjectManager objectManager, SerObjectInfoInit serObjectInfoInit, IFormatterConverter converter, bool bSimpleAssembly)`
  （Read对象信息 创建（类型 objectType, string[] memberNames, Type[] memberTypes, ISurrogateSelector surrogateSelector, StreamingContext context, 对象管理器 objectManager, Ser对象信息初始化 serObjectInfoInit, IFormatterConverter converter, bool bSimpleAssembly））
- `void Init(Type objectType, string[] memberNames, Type[] memberTypes, ISurrogateSelector surrogateSelector, StreamingContext context, ObjectManager objectManager, SerObjectInfoInit serObjectInfoInit, IFormatterConverter converter, bool bSimpleAssembly)`
  （void 初始化（类型 objectType, string[] memberNames, Type[] memberTypes, ISurrogateSelector surrogateSelector, StreamingContext context, 对象管理器 objectManager, Ser对象信息初始化 serObjectInfoInit, IFormatterConverter converter, bool bSimpleAssembly））
- `void InitReadConstructor(Type objectType, ISurrogateSelector surrogateSelector, StreamingContext context)`
  （void 初始化ReadConstructor（类型 objectType, ISurrogateSelector surrogateSelector, StreamingContext context））
- `void InitSiRead()`
  （void 初始化SiRead（））
- `void InitNoMembers()`
  （void 初始化NoMembers（））
- `void InitMemberInfo()`
  （void 初始化Member信息（））
- `MemberInfo GetMemberInfo(string name)`
  （Member信息 获取Member信息（string name））
- `Type GetType(string name)`
  （类型 获取类型（string name））
- `void AddValue(string name, object value, ref SerializationInfo si, ref object[] memberData)`
  （void 添加值（string name, object value, ref SerializationInfo si, ref object[] memberData））
- `void InitDataStore(ref SerializationInfo si, ref object[] memberData)`
  （void 初始化数据商店（ref SerializationInfo si, ref object[] memberData））
- `void RecordFixup(long objectId, string name, long idRef)`
  （void RecordFixup（long objectId, string name, long idRef））
- `void PopulateObjectMembers(object obj, object[] memberData)`
  （void Populate对象Members（object obj, object[] memberData））
- `int Position(string name)`
  （int Position（string name））
- `Type[] GetMemberTypes(string[] inMemberNames, Type objectType)`
  （Type[] 获取MemberTypes（string[] inMemberNames, 类型 objectType））
- `Type GetMemberType(MemberInfo objMember)`
  （类型 获取Member类型（Member信息 objMember））
- `ReadObjectInfo GetObjectInfo(SerObjectInfoInit serObjectInfoInit)`
  （Read对象信息 获取对象信息（Ser对象信息初始化 serObjectInfoInit））

---

## ReadOnlyAttribute（ReadOnlyAttribute）

**继承**: Attribute（属性）

### 字段 (4)

- `bool isReadOnly`（bool isReadOnly）(偏移: 0x8)
- `ReadOnlyAttribute Yes`（ReadOnlyAttribute Yes）(偏移: 0x0)
- `ReadOnlyAttribute No`（ReadOnlyAttribute No）(偏移: 0x4)
- `ReadOnlyAttribute Default`（ReadOnlyAttribute 默认的）(偏移: 0x8)

### 方法 (4)

- `bool get_IsReadOnly()`
  （布尔值 获取_是否只读（））
- `bool Equals(object value)`
  （布尔值 等于（对象 value））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `bool IsDefaultAttribute()`
  （布尔值 是否默认属性（））

---

## ReadOnlyCollectionBase（ReadOnlyCollection基础）

**继承**: ICollection, IEnumerable（ICollection, IEnumerable）

### 字段 (1)

- `ArrayList list`（数组列表 list）(偏移: 0x8)

### 方法 (3)

- `ArrayList get_InnerList()`
  （数组列表 get_Inner列表（））
- `int get_Count()`
  （整数 获取_数量（））
- `IEnumerator GetEnumerator()`
  （IEnumerator 获取枚举器（））

---

## ReadProgressEventArgs（ReadProgress事件Args）

**继承**: ZipProgressEventArgs（Zip进度事件参数）

### 方法 (5)

- `ReadProgressEventArgs Before(string archiveName, int entriesTotal)`
  （ReadProgress事件Args Before（string archiveName, int entriesTotal））
- `ReadProgressEventArgs After(string archiveName, ZipEntry entry, int entriesTotal)`
  （ReadProgress事件Args After（string archiveName, ZipEntry entry, int entriesTotal））
- `ReadProgressEventArgs Started(string archiveName)`
  （ReadProgress事件Args Started（string archiveName））
- `ReadProgressEventArgs ByteUpdate(string archiveName, ZipEntry entry, long bytesXferred, long totalBytes)`
  （ReadProgress事件Args Byte更新（string archiveName, ZipEntry entry, long bytesXferred, long totalBytes））
- `ReadProgressEventArgs Completed(string archiveName)`
  （ReadProgress事件Args Completed（string archiveName））

---

## RealProxy（Real代理）

### 字段 (8)

- `Type class_to_proxy`（类型 class_to_proxy）(偏移: 0x8)
- `Context _targetContext`（Context _targetContext）(偏移: 0xC)
- `MarshalByRefObject _server`（MarshalByRef对象 _server）(偏移: 0x10)
- `int _targetDomainId`（int _targetDomainId）(偏移: 0x14)
- `string _targetUri`（string _targetUri）(偏移: 0x18)
- `Identity _objectIdentity`（Identity _objectIdentity）(偏移: 0x1C)
- `object _objTP`（object _objTP）(偏移: 0x20)
- `object _stubData`（object _stub数据）(偏移: 0x24)

### 方法 (12)

- `Type InternalGetProxyType(object transparentProxy)`
  （类型 内部的获取代理类型（object transparentProxy））
- `Type GetProxiedType()`
  （类型 获取Proxied类型（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））
- `Identity get_ObjectIdentity()`
  （Identity get_对象Identity（））
- `void set_ObjectIdentity(Identity value)`
  （void set_对象Identity（Identity value））
- `object PrivateInvoke(RealProxy rp, IMessage msg, out Exception exc, out object[] out_args)`
  （object 私有的Invoke（Real代理 rp, IMessage msg, out Exception exc, out object[] out_args））
- `object InternalGetTransparentProxy(string className)`
  （object 内部的获取透明的代理（string className））
- `object GetTransparentProxy()`
  （object 获取透明的代理（））
- `void AttachServer(MarshalByRefObject s)`
  （void Attach服务器（MarshalByRef对象 s））
- `void SetTargetDomain(int domainId)`
  （void 集合目标Domain（int domainId））
- `object GetAppDomainTarget()`
  （object 获取AppDomain目标（））
- `object[] ProcessResponse(IMethodReturnMessage mrm, MonoMethodMessage call)`
  （object[] 处理响应（IMethodReturnMessage mrm, MonoMethodMessage call））

---

## RecastBBTree（RecastBBTree）

### 字段 (1)

- `RecastBBTreeBox root`（RecastBBTreeBox root）(偏移: 0x8)

### 方法 (9)

- `void QueryInBounds(Rect bounds, List<RecastMeshObj> buffer)`
  （void QueryInBounds（Rect bounds, List<Recast网格Obj> buffer））
- `void QueryBoxInBounds(RecastBBTreeBox box, Rect bounds, List<RecastMeshObj> boxes)`
  （void QueryBoxInBounds（RecastBBTreeBox box, Rect bounds, List<Recast网格Obj> boxes））
- `bool Remove(RecastMeshObj mesh)`
  （bool 移除（Recast网格Obj mesh））
- `RecastBBTreeBox RemoveBox(RecastBBTreeBox c, RecastMeshObj mesh, Rect bounds, ref bool found)`
  （RecastBBTreeBox 移除Box（RecastBBTreeBox c, Recast网格Obj mesh, Rect bounds, ref bool found））
- `void Insert(RecastMeshObj mesh)`
  （void Insert（Recast网格Obj mesh））
- `bool RectIntersectsRect(Rect r, Rect r2)`
  （bool RectIntersectsRect（Rect r, Rect r2））
- `float ExpansionRequired(Rect r, Rect r2)`
  （float ExpansionRequired（Rect r, Rect r2））
- `Rect ExpandToContain(Rect r, Rect r2)`
  （Rect ExpandToContain（Rect r, Rect r2））
- `float RectArea(Rect r)`
  （float RectArea（Rect r））

---

## RecastBBTreeBox（RecastBBTreeBox）

### 字段 (4)

- `Rect rect`（Rect rect）(偏移: 0x8)
- `RecastMeshObj mesh`（Recast网格Obj mesh）(偏移: 0x18)
- `RecastBBTreeBox c1`（RecastBBTreeBox c1）(偏移: 0x1C)
- `RecastBBTreeBox c2`（RecastBBTreeBox c2）(偏移: 0x20)

### 方法 (1)

- `bool Contains(Vector3 p)`
  （bool Contains（三维向量 p））

---

## RecastGraph（RecastGraph）

**继承**: NavmeshBase, IUpdatableGraph（Navmesh基础, IUpdatableGraph）

### 字段 (26)

- `float characterRadius`（float characterRadius）(偏移: 0xF8)
- `float contourMaxError`（float contour最大Error）(偏移: 0xFC)
- `float cellSize`（float cell大小）(偏移: 0x100)
- `float walkableHeight`（float walkable高度）(偏移: 0x104)
- `float walkableClimb`（float walkable攀爬）(偏移: 0x108)
- `float maxSlope`（float maxSlope）(偏移: 0x10C)
- `float maxEdgeLength`（float maxEdgeLength）(偏移: 0x110)
- `float minRegionSize`（float minRegion大小）(偏移: 0x114)
- `int editorTileSize`（int editorTile大小）(偏移: 0x118)
- `int tileSizeX`（int tile大小X）(偏移: 0x11C)
- `int tileSizeZ`（int tile大小Z）(偏移: 0x120)
- `bool useTiles`（bool useTiles）(偏移: 0x124)
- `bool scanEmptyGraph`（bool scan空Graph）(偏移: 0x125)
- `RecastGraph.RelevantGraphSurfaceMode relevantGraphSurfaceMode`（RecastGraph.RelevantGraphSurface模式 relevantGraphSurface模式）(偏移: 0x128)
- `bool rasterizeColliders`（bool rasterizeColliders）(偏移: 0x12C)
- `bool rasterizeMeshes`（bool rasterizeMeshes）(偏移: 0x0)
- `bool rasterizeTerrain`（bool rasterizeTerrain）(偏移: 0x0)
- `bool rasterizeTrees`（bool rasterizeTrees）(偏移: 0x0)
- `float colliderRasterizeDetail`（float colliderRasterizeDetail）(偏移: 0x0)
- `LayerMask mask`（层掩码 mask）(偏移: 0x134)
- `List<string> tagMask`（List<string> tag掩码）(偏移: 0x138)
- `int terrainSampleSize`（int terrainSample大小）(偏移: 0x13C)
- `Vector3 rotation`（三维向量 旋转）(偏移: 0x140)
- `Vector3 forcedBoundsCenter`（三维向量 forcedBounds中心）(偏移: 0x14C)
- `Voxelize globalVox`（Voxelize globalVox）(偏移: 0x158)
- `List<NavmeshTile> stagingTiles`（List<NavmeshTile> stagingTiles）(偏移: 0x15C)

### 方法 (22)

- `bool get_RecalculateNormals()`
  （bool get_RecalculateNormals（））
- `float get_TileWorldSizeX()`
  （float get_Tile世界的大小X（））
- `float get_TileWorldSizeZ()`
  （float get_Tile世界的大小Z（））
- `float get_MaxTileConnectionEdgeDistance()`
  （float get_最大Tile连接Edge距离（））
- `Bounds get_forcedBounds()`
  （Bounds get_forcedBounds（））
- `Vector3 ClosestPointOnNode(TriangleMeshNode node, Vector3 pos)`
  （三维向量 ClosestPointOn节点（Triangle网格节点 node, 三维向量 pos））
- `bool ContainsPoint(TriangleMeshNode node, Vector3 pos)`
  （bool ContainsPoint（Triangle网格节点 node, 三维向量 pos））
- `void SnapForceBoundsToScene()`
  （void Snap强制BoundsTo场景（））
- `IEnumerable<Progress> ScanInternal()`
  （IEnumerable<进度> 扫描内部（））
- `GraphTransform CalculateTransform()`
  （Graph变换 计算变换（））
- `void InitializeTileInfo()`
  （void 初始化Tile信息（））
- `List<RasterizationMesh>[] PutMeshesIntoTileBuckets(List<RasterizationMesh> meshes)`
  （List<RasterizationMesh>[] PutMeshesIntoTileBuckets（List<RasterizationMesh> meshes））
- `IEnumerable<Progress> ScanAllTiles()`
  （IEnumerable<Progress> Scan所有Tiles（））
- `List<RasterizationMesh> CollectMeshes(Bounds bounds)`
  （List<RasterizationMesh> CollectMeshes（Bounds bounds））
- `float get_CellHeight()`
  （float get_Cell高度（））
- `int get_CharacterRadiusInVoxels()`
  （int get_角色RadiusInVoxels（））
- `int get_TileBorderSizeInVoxels()`
  （int get_TileBorder大小InVoxels（））
- `float get_TileBorderSizeInWorldUnits()`
  （float get_TileBorder大小In世界的Units（））
- `Bounds CalculateTileBoundsWithBorder(int x, int z)`
  （Bounds 计算TileBoundsWithBorder（int x, int z））
- `NavmeshTile BuildTileMesh(Voxelize vox, int x, int z, int threadIndex = 0)`
  （NavmeshTile BuildTile网格（Voxelize vox, int x, int z, int threadIndex = 0））
- `NavmeshTile CreateTile(Voxelize vox, VoxelMesh mesh, int x, int z, int threadIndex)`
  （NavmeshTile 创建Tile（Voxelize vox, Voxel网格 mesh, int x, int z, int threadIndex））
- `void DeserializeSettingsCompatibility(GraphSerializationContext ctx)`
  （void 反序列化设置兼容性（图序列化上下文 ctx））

---

## RecastGraph.RelevantGraphSurfaceMode（RecastGraph.RelevantGraphSurface模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RecastMeshGatherer（Recast网格Gatherer）

### 字段 (8)

- `int terrainSampleSize`（int terrainSample大小）(偏移: 0x8)
- `LayerMask mask`（层掩码 mask）(偏移: 0xC)
- `List<string> tagMask`（List<string> tag掩码）(偏移: 0x10)
- `float colliderRasterizeDetail`（float colliderRasterizeDetail）(偏移: 0x14)
- `Bounds bounds`（边界 bounds）(偏移: 0x18)
- `int[] BoxColliderTris`（int[] Box碰撞器Tris）(偏移: 0x0)
- `Vector3[] BoxColliderVerts`（Vector3[] Box碰撞器Verts）(偏移: 0x4)
- `List<RecastMeshGatherer.CapsuleCache> capsuleCache`（List<Recast网格Gatherer.CapsuleCache> capsule缓存）(偏移: 0x30)

### 方法 (13)

- `List<MeshFilter> FilterMeshes(MeshFilter[] meshFilters, List<string> tagMask, LayerMask layerMask)`
  （List<网格Filter> FilterMeshes（网格Filter[] meshFilters, List<string> tagMask, 层掩码 layerMask））
- `void CollectSceneMeshes(List<RasterizationMesh> meshes)`
  （void Collect场景Meshes（List<RasterizationMesh> meshes））
- `void CollectRecastMeshObjs(List<RasterizationMesh> buffer)`
  （void CollectRecast网格Objs（List<RasterizationMesh> buffer））
- `void CollectTerrainMeshes(bool rasterizeTrees, float desiredChunkSize, List<RasterizationMesh> result)`
  （void CollectTerrainMeshes（bool rasterizeTrees, float desiredChunkSize, List<RasterizationMesh> result））
- `void GenerateTerrainChunks(Terrain terrain, Bounds bounds, float desiredChunkSize, List<RasterizationMesh> result)`
  （void GenerateTerrainChunks（Terrain terrain, Bounds bounds, float desiredChunkSize, List<RasterizationMesh> result））
- `int CeilDivision(int lhs, int rhs)`
  （int CeilDivision（int lhs, int rhs））
- `RasterizationMesh GenerateHeightmapChunk(float[,] heights, Vector3 sampleSize, Vector3 offset, int x0, int z0, int width, int depth, int stride)`
  （Rasterization网格 GenerateHeightmapChunk（float[, ] heights, 三维向量 sampleSize, 三维向量 offset, int x0, int z0, int width, int depth, int stride））
- `void CollectTreeMeshes(Terrain terrain, List<RasterizationMesh> result)`
  （void CollectTreeMeshes（Terrain terrain, List<RasterizationMesh> result））
- `void CollectColliderMeshes(List<RasterizationMesh> result)`
  （void Collect碰撞器Meshes（List<RasterizationMesh> result））
- `RasterizationMesh RasterizeCollider(Collider col)`
  （Rasterization网格 Rasterize碰撞器（碰撞器 col））
- `RasterizationMesh RasterizeCollider(Collider col, Matrix4x4 localToWorldMatrix)`
  （Rasterization网格 Rasterize碰撞器（碰撞器 col, Matrix4x4 localToWorldMatrix））
- `RasterizationMesh RasterizeBoxCollider(BoxCollider collider, Matrix4x4 localToWorldMatrix)`
  （Rasterization网格 RasterizeBox碰撞器（Box碰撞器 collider, Matrix4x4 localToWorldMatrix））
- `RasterizationMesh RasterizeCapsuleCollider(float radius, float height, Bounds bounds, Matrix4x4 localToWorldMatrix)`
  （Rasterization网格 RasterizeCapsule碰撞器（float radius, float height, Bounds bounds, Matrix4x4 localToWorldMatrix））

---

## RecastMeshGatherer.CapsuleCache（Recast网格Gatherer.Capsule缓存）

### 字段 (4)

- `int rows`（int rows）(偏移: 0x8)
- `float height`（浮点数 高度）(偏移: 0xC)
- `Vector3[] verts`（Vector3[] verts）(偏移: 0x10)
- `int[] tris`（整数[] 三角形）(偏移: 0x14)

---

## RecastMeshObj（Recast网格Obj）

**继承**: VersionedMonoBehaviour（版本化MonoBehaviour）

### 字段 (7)

- `RecastBBTree tree`（RecastBBTree tree）(偏移: 0x0)
- `List<RecastMeshObj> dynamicMeshObjs`（List<Recast网格Obj> dynamic网格Objs）(偏移: 0x4)
- `Bounds bounds`（边界 bounds）(偏移: 0x10)
- `bool dynamic`（bool dynamic）(偏移: 0x28)
- `int area`（整数 面积）(偏移: 0x2C)
- `bool _dynamic`（bool _dynamic）(偏移: 0x30)
- `bool registered`（bool registered）(偏移: 0x31)

### 方法 (8)

- `void GetAllInBounds(List<RecastMeshObj> buffer, Bounds bounds)`
  （void 获取所有InBounds（List<Recast网格Obj> buffer, Bounds bounds））
- `void OnEnable()`
  （void 启用时（））
- `void Register()`
  （void Register（））
- `void RecalculateBounds()`
  （void RecalculateBounds（））
- `Bounds GetBounds()`
  （Bounds 获取Bounds（））
- `MeshFilter GetMeshFilter()`
  （网格Filter 获取网格Filter（））
- `Collider GetCollider()`
  （碰撞器 获取碰撞器（））
- `void OnDisable()`
  （void 禁用时（））

---

## Recoil（后坐力）

**继承**: OffsetModifier（偏移修改器）

### 字段 (23)

- `AimIK aimIK`（AimIK aimIK）(偏移: 0x18)
- `bool aimIKSolvedLast`（bool aimIKSolved最后一个）(偏移: 0x1C)
- `Recoil.Handedness handedness`（Recoil.Handedness handedness）(偏移: 0x20)
- `bool twoHanded`（bool twoHanded）(偏移: 0x24)
- `AnimationCurve recoilWeight`（动画Curve recoilWeight）(偏移: 0x28)
- `float magnitudeRandom`（float magnitude随机）(偏移: 0x2C)
- `Vector3 rotationRandom`（三维向量 rotation随机）(偏移: 0x30)
- `Vector3 handRotationOffset`（三维向量 handRotationOffset）(偏移: 0x3C)
- `float blendTime`（float blend时间）(偏移: 0x48)
- `Recoil.RecoilOffset[] offsets`（Recoil.后坐力Offset[] offsets）(偏移: 0x4C)
- `Quaternion rotationOffset`（Quaternion rotationOffset）(偏移: 0x50)
- `float magnitudeMlp`（float magnitudeMlp）(偏移: 0x60)
- `float endTime`（float end时间）(偏移: 0x64)
- `Quaternion handRotation`（Quaternion handRotation）(偏移: 0x68)
- `Quaternion secondaryHandRelativeRotation`（Quaternion secondary手部RelativeRotation）(偏移: 0x78)
- `Quaternion randomRotation`（Quaternion randomRotation）(偏移: 0x88)
- `float length`（浮点数 长度）(偏移: 0x98)
- `bool initiated`（布尔值 已启动）(偏移: 0x9C)
- `float blendWeight`（float blendWeight）(偏移: 0xA0)
- `float w`（浮点数 w）(偏移: 0xA4)
- `Quaternion primaryHandRotation`（Quaternion primary手部Rotation）(偏移: 0xA8)
- `bool handRotationsSet`（bool handRotations集合）(偏移: 0xB8)
- `Vector3 aimIKAxis`（三维向量 aimIK轴）(偏移: 0xBC)

### 方法 (11)

- `bool get_isFinished()`
  （bool get_isFinished（））
- `void SetHandRotations(Quaternion leftHandRotation, Quaternion rightHandRotation)`
  （void 集合手部Rotations（Quaternion leftHandRotation, Quaternion rightHandRotation））
- `void Fire(float magnitude)`
  （void 开火（float magnitude））
- `void OnModifyOffset()`
  （void 修改偏移时（））
- `void AfterFBBIK()`
  （void AfterFBBIK（））
- `void AfterAimIK()`
  （void AfterAimIK（））
- `IKEffector get_primaryHandEffector()`
  （IKEffector get_primary手部Effector（））
- `IKEffector get_secondaryHandEffector()`
  （IKEffector get_secondary手部Effector（））
- `Transform get_primaryHand()`
  （变换 get_primary手部（））
- `Transform get_secondaryHand()`
  （变换 get_secondary手部（））
- `void OnDestroy()`
  （void 销毁时（））

---

## Recoil（后坐力）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (32)

- `ShootPosture shootPosture`（射击姿态 shoot姿态）(偏移: 0xC)
- `PostureFloat perturbMin`（姿态浮点数 perturb最小）(偏移: 0x10)
- `PostureFloat perturbMax`（姿态浮点数 perturb最大）(偏移: 0x24)
- `Vector2 perturbChangeSpeed`（二维向量 perturbChangeSpeed）(偏移: 0x38)
- `PostureFloat detailedReactYawShot`（姿态浮点数 detailedReact偏航角射击）(偏移: 0x40)
- `PostureFloat detailedReactPitchShot`（姿态浮点数 detailedReact俯仰角射击）(偏移: 0x54)
- `float addYaw_Target`（float addYaw_目标）(偏移: 0x70)
- `float addPitch_Target`（float addPitch_目标）(偏移: 0x74)
- `PostureFloat fullReactYaw`（姿态浮点数 fullReact偏航角）(偏移: 0x78)
- `PostureFloat fullReactPitch`（姿态浮点数 fullReact俯仰角）(偏移: 0x8C)
- `SideReactDirect sideReactDirect`（侧面反应方向 sideReactDirect）(偏移: 0xA0)
- `int shotRepeatCount`（int shotRepeat数量）(偏移: 0xA8)
- `int oneShotRepeatCount`（int one射击Repeat数量）(偏移: 0xAC)
- `int longOneShotRepeatCount`（int longOne射击Repeat数量）(偏移: 0xB0)
- `int longOneShotRepeatCount_CrossHair`（int longOne射击RepeatCount_CrossHair）(偏移: 0xB4)
- `PostureFloat detailPerturbShot`（姿态浮点数 detail扰动射击）(偏移: 0xB8)
- `AmmoRecoverAndDecay shotReactYaw`（弹药恢复And衰减 shotReact偏航角）(偏移: 0xCC)
- `AmmoRecoverAndDecay shotReactPitch`（弹药恢复And衰减 shotReact俯仰角）(偏移: 0xD0)
- `bool mirror`（bool mirror）(偏移: 0xD4)
- `bool shoot`（bool shoot）(偏移: 0xD5)
- `float oneShotTime`（float one射击时间）(偏移: 0xD8)
- `float previousOneShotTime`（float previousOne射击时间）(偏移: 0xDC)
- `float previousShotTime`（float previous射击时间）(偏移: 0xE0)
- `int shotCount_CrossHair`（int shotCount_CrossHair）(偏移: 0xE4)
- `float nextCircleRealSize`（float nextCircleReal大小）(偏移: 0xE8)
- `float circleMinSize`（float circle最小大小）(偏移: 0xEC)
- `float nextCircleShotSize`（float nextCircle射击大小）(偏移: 0xF0)
- `float lastTargetSize`（float last目标大小）(偏移: 0xF4)
- `ChangeMovingRealSize changeMovingRealSize`（ChangeMovingReal大小 changeMovingReal大小）(偏移: 0xF8)
- `DelayOneShootData delayOneShootTime`（延迟One射击数据 delayOne射击时间）(偏移: 0x10C)
- `bool isKnife`（bool is近战武器）(偏移: 0x118)
- `int byGunRotateDirection`（int by枪械Rotate方向）(偏移: 0x11C)

### 方法 (32)

- `float get_addYaw()`
  （float get_add偏航角（））
- `void set_addYaw(float value)`
  （void set_add偏航角（float value））
- `float get_addPitch()`
  （float get_add俯仰角（））
- `void set_addPitch(float value)`
  （void set_add俯仰角（float value））
- `float get_reactRate()`
  （float get_reactRate（））
- `void SetPerturb(PostureFloat min, PostureFloat max)`
  （void 集合扰动（姿态浮点数 min, 姿态浮点数 max））
- `void SetDetailedReactShot(PostureFloat yaw, PostureFloat pitch)`
  （void 集合DetailedReact射击（姿态浮点数 yaw, 姿态浮点数 pitch））
- `void SetDetailPerturbShot(PostureFloat detailPerturb)`
  （void 集合Detail扰动射击（姿态浮点数 detailPerturb））
- `void SetSideReactDirect(SideReactDirect sideReactDirect)`
  （void 集合侧面ReactDirect（侧面反应方向 sideReactDirect））
- `void SetShotReact(AmmoRecoverAndDecay yaw, AmmoRecoverAndDecay pitch)`
  （void 集合射击React（弹药恢复And衰减 yaw, 弹药恢复And衰减 pitch））
- `void SetChangeMovingRealSize(ChangeMovingRealSize changeMovingRealSize)`
  （void 集合ChangeMovingReal大小（ChangeMovingReal大小 changeMovingRealSize））
- `void SetFullReact(PostureFloat yaw, PostureFloat pitch)`
  （void 集合满React（姿态浮点数 yaw, 姿态浮点数 pitch））
- `void SetDelayOneShoot(DelayOneShootData data)`
  （void 集合延迟One射击（延迟One射击数据 data））
- `float GetCurrentPerturb()`
  （float 获取当前扰动（））
- `void Update()`
  （void 更新（））
- `void LateUpdate()`
  （void 延迟更新（））
- `void TransformUpdate()`
  （void 变换更新（））
- `void UpdateAddYaw()`
  （void 更新添加偏航角（））
- `void UpdateAddPitch()`
  （void 更新添加俯仰角（））
- `void OnGunShot()`
  （void On枪械射击（））
- `void ShotRepeatCountAdd()`
  （void 射击Repeat数量添加（））
- `int ShotRepeatCountClamp(int input, int maxClip)`
  （int 射击Repeat数量Clamp（int input, int maxClip））
- `Vector3 SetDirect(Vector3 direct)`
  （三维向量 集合Direct（三维向量 direct））
- `Ray GetShootRay()`
  （Ray 获取射击Ray（））
- `Ray GetKnifeAttackRay()`
  （Ray 获取近战武器AttackRay（））
- `Vector2 GetCurrentRecoil()`
  （二维向量 获取当前后坐力（））
- `void ResetShotRepeatCount(bool allResetSwitch = False)`
  （void 重置射击Repeat数量（bool allResetSwitch = False））
- `void CalcCircleSizeForNextFrame()`
  （void CalcCircle大小For下一个Frame（））
- `Vector3 CalculateWeaponPath(Quaternion rGunDir)`
  （三维向量 计算Weapon路径（Quaternion rGunDir））
- `void ResetCrossHairValue()`
  （void 重置CrossHair值（））
- `void UpdateCrossHair()`
  （void 更新CrossHair（））
- `void SendTargetSizeInfo(float minSize, float realSize)`
  （void 发送目标大小信息（float minSize, float realSize））

---

## Recoil.Handedness（Recoil.Handedness）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Recoil.RecoilOffset（Recoil.后坐力Offset）

### 字段 (6)

- `Vector3 offset`（三维向量 偏移）(偏移: 0x8)
- `float additivity`（float additivity）(偏移: 0x14)
- `float maxAdditiveOffsetMag`（float maxAdditiveOffsetMag）(偏移: 0x18)
- `Recoil.RecoilOffset.EffectorLink[] effectorLinks`（Recoil.后坐力Offset.EffectorLink[] effectorLinks）(偏移: 0x1C)
- `Vector3 additiveOffset`（三维向量 additiveOffset）(偏移: 0x20)
- `Vector3 lastOffset`（三维向量 lastOffset）(偏移: 0x2C)

### 方法 (2)

- `void Start()`
  （void 开始（））
- `void Apply(IKSolverFullBodyBiped solver, Quaternion rotation, float masterWeight, float length, float timeLeft)`
  （void 应用（IKSolver满身体Biped solver, Quaternion rotation, float masterWeight, float length, float timeLeft））

---

## Recoil.RecoilOffset.EffectorLink（Recoil.后坐力Offset.EffectorLink）

### 字段 (2)

- `FullBodyBipedEffector effector`（全身双足效应器 effector）(偏移: 0x8)
- `float weight`（浮点数 权重）(偏移: 0xC)

---

## Recorder（Recorder）

### 字段 (2)

- `IntPtr m_Ptr`（整数指针 m_指针）(偏移: 0x8)
- `Recorder s_InvalidRecorder`（Recorder s_InvalidRecorder）(偏移: 0x0)

### 方法 (15)

- `void Finalize()`
  （void 终结（））
- `bool get_isValid()`
  （布尔值 获取_是否有效（））
- `void DisposeNative(IntPtr ptr)`
  （void 释放Native（整数Ptr ptr））
- `bool get_enabled()`
  （布尔值 获取_已启用（））
- `void set_enabled(bool value)`
  （void 设置_已启用（布尔值 value））
- `bool IsEnabled()`
  （bool 是否启用的（））
- `void SetEnabled(bool enabled)`
  （void 集合启用的（bool enabled））
- `long get_elapsedNanoseconds()`
  （long get_elapsedNanoseconds（））
- `long get_gpuElapsedNanoseconds()`
  （long get_gpuElapsedNanoseconds（））
- `long GetElapsedNanoseconds()`
  （long 获取ElapsedNanoseconds（））
- `long GetGpuElapsedNanoseconds()`
  （long 获取GpuElapsedNanoseconds（））
- `int get_sampleBlockCount()`
  （int get_sampleBlock数量（））
- `int get_gpuSampleBlockCount()`
  （int get_gpuSampleBlock数量（））
- `int GetSampleBlockCount()`
  （int 获取SampleBlock数量（））
- `int GetGpuSampleBlockCount()`
  （int 获取GpuSampleBlock数量（））

---

## Rect（Rect）

**继承**: IEquatable<Rect>, IFormattable（IEquatable<Rect>, IFormattable）

### 字段 (4)

- `float m_XMin`（float m_X最小）(偏移: 0x0)
- `float m_YMin`（float m_Y最小）(偏移: 0x4)
- `float m_Width`（float m_宽度）(偏移: 0x8)
- `float m_Height`（float m_高度）(偏移: 0xC)

### 方法 (36)

- `Rect get_zero()`
  （Rect get_zero（））
- `Rect MinMaxRect(float xmin, float ymin, float xmax, float ymax)`
  （Rect 最小最大Rect（float xmin, float ymin, float xmax, float ymax））
- `float get_x()`
  （float get_x（））
- `void set_x(float value)`
  （void set_x（float value））
- `float get_y()`
  （float get_y（））
- `void set_y(float value)`
  （void set_y（float value））
- `Vector2 get_position()`
  （二维向量 get_position（））
- `void set_position(Vector2 value)`
  （void set_position（二维向量 value））
- `Vector2 get_center()`
  （二维向量 get_center（））
- `Vector2 get_min()`
  （二维向量 get_min（））
- `Vector2 get_max()`
  （二维向量 get_max（））
- `float get_width()`
  （float get_width（））
- `void set_width(float value)`
  （void set_width（float value））
- `float get_height()`
  （浮点数 获取_高度（））
- `void set_height(float value)`
  （void 设置_高度（浮点数 value））
- `Vector2 get_size()`
  （二维向量 get_size（））
- `float get_xMin()`
  （float get_x最小（））
- `void set_xMin(float value)`
  （void set_x最小（float value））
- `float get_yMin()`
  （float get_y最小（））
- `void set_yMin(float value)`
  （void set_y最小（float value））
- `float get_xMax()`
  （float get_x最大（））
- `void set_xMax(float value)`
  （void set_x最大（float value））
- `float get_yMax()`
  （float get_y最大（））
- `void set_yMax(float value)`
  （void set_y最大（float value））
- `bool Contains(Vector2 point)`
  （bool Contains（二维向量 point））
- `bool Contains(Vector3 point)`
  （布尔值 包含（三维向量 point））
- `Rect OrderMinMax(Rect rect)`
  （Rect Order最小最大（Rect rect））
- `bool Overlaps(Rect other)`
  （bool Overlaps（Rect other））
- `bool Overlaps(Rect other, bool allowInverse)`
  （bool Overlaps（Rect other, bool allowInverse））
- `bool op_Inequality(Rect lhs, Rect rhs)`
  （bool op_Inequality（Rect lhs, Rect rhs））
- `bool op_Equality(Rect lhs, Rect rhs)`
  （bool op_Equality（Rect lhs, Rect rhs））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `bool Equals(object other)`
  （布尔值 等于（对象 other））
- `bool Equals(Rect other)`
  （bool Equals（Rect other））
- `string ToString()`
  （字符串 转字符串（））
- `string ToString(string format, IFormatProvider formatProvider)`
  （字符串 转字符串（字符串 格式, I格式化提供者 formatProvider））

---

## RectInt（Rect整数）

**继承**: IEquatable<RectInt>, IFormattable（IEquatable<RectInt>, IFormattable）

### 字段 (4)

- `int m_XMin`（int m_X最小）(偏移: 0x0)
- `int m_YMin`（int m_Y最小）(偏移: 0x4)
- `int m_Width`（int m_宽度）(偏移: 0x8)
- `int m_Height`（int m_高度）(偏移: 0xC)

### 方法 (11)

- `int get_x()`
  （整数 获取_x（））
- `void set_x(int value)`
  （void 设置_x（整数 value））
- `int get_y()`
  （整数 获取_y（））
- `void set_y(int value)`
  （void 设置_y（整数 value））
- `int get_width()`
  （整数 获取_宽度（））
- `void set_width(int value)`
  （void 设置_宽度（整数 value））
- `int get_height()`
  （整数 获取_高度（））
- `void set_height(int value)`
  （void 设置_高度（整数 value））
- `string ToString()`
  （字符串 转字符串（））
- `string ToString(string format, IFormatProvider formatProvider)`
  （字符串 转字符串（字符串 格式, I格式化提供者 formatProvider））
- `bool Equals(RectInt other)`
  （bool Equals（Rect整数 other））

---

## RectMask2D（RectMask2D）

**继承**: UIBehaviour, IClipper, ICanvasRaycastFilter（界面Behaviour, IClipper, I画布RaycastFilter）

### 字段 (12)

- `RectangularVertexClipper m_VertexClipper`（RectangularVertexClipper m_VertexClipper）(偏移: 0xC)
- `RectTransform m_RectTransform`（Rect变换 m_Rect变换）(偏移: 0x10)
- `HashSet<MaskableGraphic> m_MaskableTargets`（HashSet<MaskableGraphic> m_MaskableTargets）(偏移: 0x14)
- `HashSet<IClippable> m_ClipTargets`（HashSet<IClippable> m_弹匣Targets）(偏移: 0x18)
- `bool m_ShouldRecalculateClipRects`（bool m_应该Recalculate弹匣Rects）(偏移: 0x1C)
- `List<RectMask2D> m_Clippers`（List<RectMask2D> m_Clippers）(偏移: 0x20)
- `Rect m_LastClipRectCanvasSpace`（Rect m_最后一个弹匣Rect画布Space）(偏移: 0x24)
- `bool m_ForceClip`（bool m_强制弹匣）(偏移: 0x34)
- `Vector4 m_Padding`（Vector4 m_Padding）(偏移: 0x38)
- `Vector2Int m_Softness`（二维向量整数 m_Softness）(偏移: 0x48)
- `Canvas m_Canvas`（画布 m_画布）(偏移: 0x50)
- `Vector3[] m_Corners`（Vector3[] m_Corners）(偏移: 0x54)

### 方法 (17)

- `Vector4 get_padding()`
  （Vector4 get_padding（））
- `void set_padding(Vector4 value)`
  （void set_padding（Vector4 value））
- `Vector2Int get_softness()`
  （二维向量整数 get_softness（））
- `void set_softness(Vector2Int value)`
  （void set_softness（二维向量整数 value））
- `Canvas get_Canvas()`
  （画布 get_画布（））
- `Rect get_canvasRect()`
  （Rect get_canvasRect（））
- `RectTransform get_rectTransform()`
  （矩形变换 获取_矩形变换（））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `bool IsRaycastLocationValid(Vector2 sp, Camera eventCamera)`
  （布尔值 射线检测位置是否有效（二维向量 sp, 摄像机 eventCamera））
- `Rect get_rootCanvasRect()`
  （Rect get_root画布Rect（））
- `void PerformClipping()`
  （void 执行Clipping（））
- `void UpdateClipSoftness()`
  （void 更新弹匣Softness（））
- `void AddClippable(IClippable clippable)`
  （void 添加Clippable（IClippable clippable））
- `void RemoveClippable(IClippable clippable)`
  （void 移除Clippable（IClippable clippable））
- `void OnTransformParentChanged()`
  （void 变换父级改变时（））
- `void OnCanvasHierarchyChanged()`
  （void 画布层级改变时（））

---

## RectOffset（RectOffset）

**继承**: IFormattable（I可格式化）

### 字段 (2)

- `IntPtr m_Ptr`（整数指针 m_指针）(偏移: 0x8)
- `object m_SourceStyle`（object m_SourceStyle）(偏移: 0xC)

### 方法 (18)

- `void Finalize()`
  （void 终结（））
- `string ToString()`
  （字符串 转字符串（））
- `string ToString(string format, IFormatProvider formatProvider)`
  （字符串 转字符串（字符串 格式, I格式化提供者 formatProvider））
- `void Destroy()`
  （void 销毁（））
- `IntPtr InternalCreate()`
  （整数Ptr 内部的创建（））
- `void InternalDestroy(IntPtr ptr)`
  （void 内部的销毁（整数Ptr ptr））
- `int get_left()`
  （int get_left（））
- `void set_left(int value)`
  （void set_left（int value））
- `int get_right()`
  （int get_right（））
- `void set_right(int value)`
  （void set_right（int value））
- `int get_top()`
  （int get_top（））
- `void set_top(int value)`
  （void set_top（int value））
- `int get_bottom()`
  （int get_bottom（））
- `void set_bottom(int value)`
  （void set_bottom（int value））
- `int get_horizontal()`
  （int get_horizontal（））
- `int get_vertical()`
  （int get_vertical（））
- `Rect Add(Rect rect)`
  （Rect 添加（Rect rect））
- `void Add_Injected(ref Rect rect, out Rect ret)`
  （void Add_Injected（ref Rect rect, out Rect ret））

---

## RectOffsetPlugin（RectOffset插件）

**继承**: ABSTweenPlugin<RectOffset, RectOffset, NoOptions>（ABSTweenPlugin<RectOffset, RectOffset, NoOptions>）

### 字段 (1)

- `RectOffset _r`（RectOffset _r）(偏移: 0x3113310A)

### 方法 (8)

- `void Reset(TweenerCore<RectOffset, RectOffset, NoOptions> t)`
  （void 重置（TweenerCore<RectOffset, RectOffset, NoOptions> t））
- `void SetFrom(TweenerCore<RectOffset, RectOffset, NoOptions> t, bool isRelative)`
  （void 集合From（TweenerCore<RectOffset, RectOffset, NoOptions> t, bool isRelative））
- `void SetFrom(TweenerCore<RectOffset, RectOffset, NoOptions> t, RectOffset fromValue, bool setImmediately, bool isRelative)`
  （void 集合From（TweenerCore<RectOffset, RectOffset, NoOptions> t, RectOffset fromValue, bool setImmediately, bool isRelative））
- `RectOffset ConvertToStartValue(TweenerCore<RectOffset, RectOffset, NoOptions> t, RectOffset value)`
  （RectOffset 转换To开始值（TweenerCore<RectOffset, RectOffset, NoOptions> t, RectOffset value））
- `void SetRelativeEndValue(TweenerCore<RectOffset, RectOffset, NoOptions> t)`
  （void 集合Relative结束值（TweenerCore<RectOffset, RectOffset, NoOptions> t））
- `void SetChangeValue(TweenerCore<RectOffset, RectOffset, NoOptions> t)`
  （void 集合Change值（TweenerCore<RectOffset, RectOffset, NoOptions> t））
- `float GetSpeedBasedDuration(NoOptions options, float unitsXSecond, RectOffset changeValue)`
  （float 获取SpeedBased持续时间（NoOptions options, float unitsXSecond, RectOffset changeValue））
- `void EvaluateAndApply(NoOptions options, Tween t, bool isRelative, DOGetter<RectOffset> getter, DOSetter<RectOffset> setter, float elapsed, RectOffset startValue, RectOffset changeValue, float duration, bool usingInversePosition, UpdateNotice updateNotice)`
  （void EvaluateAnd应用（NoOptions options, Tween t, bool isRelative, DOGetter<RectOffset> getter, DOSetter<RectOffset> setter, float elapsed, RectOffset startValue, RectOffset changeValue, float duration, bool usingInversePosition, 更新Notice updateNotice））

---

## RectOptions（RectOptions）

**继承**: IPlugOptions（I插件选项）

### 字段 (1)

- `bool snapping`（布尔值 吸附）(偏移: 0x0)

### 方法 (1)

- `void Reset()`
  （void 重置（））

---

## RectPlugin（Rect插件）

**继承**: ABSTweenPlugin<Rect, Rect, RectOptions>（ABSTweenPlugin<Rect, Rect, RectOptions>）

### 方法 (8)

- `void Reset(TweenerCore<Rect, Rect, RectOptions> t)`
  （void 重置（TweenerCore<Rect, Rect, RectOptions> t））
- `void SetFrom(TweenerCore<Rect, Rect, RectOptions> t, bool isRelative)`
  （void 集合From（TweenerCore<Rect, Rect, RectOptions> t, bool isRelative））
- `void SetFrom(TweenerCore<Rect, Rect, RectOptions> t, Rect fromValue, bool setImmediately, bool isRelative)`
  （void 集合From（TweenerCore<Rect, Rect, RectOptions> t, Rect fromValue, bool setImmediately, bool isRelative））
- `Rect ConvertToStartValue(TweenerCore<Rect, Rect, RectOptions> t, Rect value)`
  （Rect 转换To开始值（TweenerCore<Rect, Rect, RectOptions> t, Rect value））
- `void SetRelativeEndValue(TweenerCore<Rect, Rect, RectOptions> t)`
  （void 集合Relative结束值（TweenerCore<Rect, Rect, RectOptions> t））
- `void SetChangeValue(TweenerCore<Rect, Rect, RectOptions> t)`
  （void 集合Change值（TweenerCore<Rect, Rect, RectOptions> t））
- `float GetSpeedBasedDuration(RectOptions options, float unitsXSecond, Rect changeValue)`
  （float 获取SpeedBased持续时间（RectOptions options, float unitsXSecond, Rect changeValue））
- `void EvaluateAndApply(RectOptions options, Tween t, bool isRelative, DOGetter<Rect> getter, DOSetter<Rect> setter, float elapsed, Rect startValue, Rect changeValue, float duration, bool usingInversePosition, UpdateNotice updateNotice)`
  （void EvaluateAnd应用（RectOptions options, Tween t, bool isRelative, DOGetter<Rect> getter, DOSetter<Rect> setter, float elapsed, Rect startValue, Rect changeValue, float duration, bool usingInversePosition, 更新Notice updateNotice））

---

## RectTransform（Rect变换）

**继承**: Transform（变换）

### 字段 (1)

- `RectTransform.ReapplyDrivenProperties reapplyDrivenProperties`（RectTransform.ReapplyDrivenProperties reapplyDrivenProperties）(偏移: 0x0)

### 方法 (34)

- `void add_reapplyDrivenProperties(RectTransform.ReapplyDrivenProperties value)`
  （void add_reapplyDrivenProperties（RectTransform.ReapplyDrivenProperties value））
- `void remove_reapplyDrivenProperties(RectTransform.ReapplyDrivenProperties value)`
  （void remove_reapplyDrivenProperties（RectTransform.ReapplyDrivenProperties value））
- `Rect get_rect()`
  （Rect get_rect（））
- `Vector2 get_anchorMin()`
  （二维向量 get_anchor最小（））
- `void set_anchorMin(Vector2 value)`
  （void set_anchor最小（二维向量 value））
- `Vector2 get_anchorMax()`
  （二维向量 get_anchor最大（））
- `void set_anchorMax(Vector2 value)`
  （void set_anchor最大（二维向量 value））
- `Vector2 get_anchoredPosition()`
  （二维向量 get_anchoredPosition（））
- `void set_anchoredPosition(Vector2 value)`
  （void set_anchoredPosition（二维向量 value））
- `Vector2 get_sizeDelta()`
  （二维向量 get_sizeDelta（））
- `void set_sizeDelta(Vector2 value)`
  （void set_sizeDelta（二维向量 value））
- `Vector2 get_pivot()`
  （二维向量 get_pivot（））
- `void set_pivot(Vector2 value)`
  （void set_pivot（二维向量 value））
- `Vector3 get_anchoredPosition3D()`
  （三维向量 get_anchoredPosition3D（））
- `void set_anchoredPosition3D(Vector3 value)`
  （void set_anchoredPosition3D（三维向量 value））
- `void set_offsetMin(Vector2 value)`
  （void set_offset最小（二维向量 value））
- `void set_offsetMax(Vector2 value)`
  （void set_offset最大（二维向量 value））
- `void ForceUpdateRectTransforms()`
  （void 强制更新RectTransforms（））
- `void GetLocalCorners(Vector3[] fourCornersArray)`
  （void 获取本地的Corners（Vector3[] fourCornersArray））
- `void GetWorldCorners(Vector3[] fourCornersArray)`
  （void 获取世界的Corners（Vector3[] fourCornersArray））
- `void SetSizeWithCurrentAnchors(RectTransform.Axis axis, float size)`
  （void 集合大小With当前Anchors（RectTransform.轴 axis, float size））
- `void SendReapplyDrivenProperties(RectTransform driven)`
  （void 发送ReapplyDrivenProperties（Rect变换 driven））
- `Vector2 GetParentSize()`
  （二维向量 获取父级大小（））
- `void get_rect_Injected(out Rect ret)`
  （void get_rect_Injected（out Rect ret））
- `void get_anchorMin_Injected(out Vector2 ret)`
  （void get_anchorMin_Injected（out Vector2 ret））
- `void set_anchorMin_Injected(ref Vector2 value)`
  （void set_anchorMin_Injected（ref Vector2 value））
- `void get_anchorMax_Injected(out Vector2 ret)`
  （void get_anchorMax_Injected（out Vector2 ret））
- `void set_anchorMax_Injected(ref Vector2 value)`
  （void set_anchorMax_Injected（ref Vector2 value））
- `void get_anchoredPosition_Injected(out Vector2 ret)`
  （void get_anchoredPosition_Injected（out Vector2 ret））
- `void set_anchoredPosition_Injected(ref Vector2 value)`
  （void set_anchoredPosition_Injected（ref Vector2 value））
- `void get_sizeDelta_Injected(out Vector2 ret)`
  （void get_sizeDelta_Injected（out Vector2 ret））
- `void set_sizeDelta_Injected(ref Vector2 value)`
  （void set_sizeDelta_Injected（ref Vector2 value））
- `void get_pivot_Injected(out Vector2 ret)`
  （void get_pivot_Injected（out Vector2 ret））
- `void set_pivot_Injected(ref Vector2 value)`
  （void set_pivot_Injected（ref Vector2 value））

---

## RectTransform.Axis（RectTransform.轴）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RectTransform.ReapplyDrivenProperties（RectTransform.ReapplyDrivenProperties）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(RectTransform driven)`
  （void Invoke（Rect变换 driven））
- `IAsyncResult BeginInvoke(RectTransform driven, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Rect变换 driven, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## RectTransformUtility（Rect变换工具）

### 字段 (1)

- `Vector3[] s_Corners`（Vector3[] s_Corners）(偏移: 0x0)

### 方法 (15)

- `Vector2 PixelAdjustPoint(Vector2 point, Transform elementTransform, Canvas canvas)`
  （二维向量 PixelAdjustPoint（二维向量 point, 变换 elementTransform, 画布 canvas））
- `Rect PixelAdjustRect(RectTransform rectTransform, Canvas canvas)`
  （Rect PixelAdjustRect（Rect变换 rectTransform, 画布 canvas））
- `bool PointInRectangle(Vector2 screenPoint, RectTransform rect, Camera cam, Vector4 offset)`
  （bool PointInRectangle（二维向量 screenPoint, Rect变换 rect, 摄像机 cam, Vector4 offset））
- `bool RectangleContainsScreenPoint(RectTransform rect, Vector2 screenPoint, Camera cam)`
  （bool RectangleContains屏幕的Point（Rect变换 rect, 二维向量 screenPoint, 摄像机 cam））
- `bool RectangleContainsScreenPoint(RectTransform rect, Vector2 screenPoint, Camera cam, Vector4 offset)`
  （bool RectangleContains屏幕的Point（Rect变换 rect, 二维向量 screenPoint, 摄像机 cam, Vector4 offset））
- `bool ScreenPointToWorldPointInRectangle(RectTransform rect, Vector2 screenPoint, Camera cam, out Vector3 worldPoint)`
  （bool 屏幕的PointTo世界的PointInRectangle（Rect变换 rect, 二维向量 screenPoint, 摄像机 cam, out Vector3 worldPoint））
- `bool ScreenPointToLocalPointInRectangle(RectTransform rect, Vector2 screenPoint, Camera cam, out Vector2 localPoint)`
  （bool 屏幕的PointTo本地的PointInRectangle（Rect变换 rect, 二维向量 screenPoint, 摄像机 cam, out Vector2 localPoint））
- `Ray ScreenPointToRay(Camera cam, Vector2 screenPos)`
  （Ray 屏幕的PointToRay（摄像机 cam, 二维向量 screenPos））
- `Vector2 WorldToScreenPoint(Camera cam, Vector3 worldPoint)`
  （二维向量 世界的To屏幕的Point（摄像机 cam, 三维向量 worldPoint））
- `void FlipLayoutOnAxis(RectTransform rect, int axis, bool keepPositioning, bool recursive)`
  （void FlipLayoutOn轴（Rect变换 rect, int axis, bool keepPositioning, bool recursive））
- `void FlipLayoutAxes(RectTransform rect, bool keepPositioning, bool recursive)`
  （void FlipLayoutAxes（Rect变换 rect, bool keepPositioning, bool recursive））
- `Vector2 GetTransposed(Vector2 input)`
  （二维向量 获取Transposed（二维向量 input））
- `void PixelAdjustPoint_Injected(ref Vector2 point, Transform elementTransform, Canvas canvas, out Vector2 ret)`
  （void PixelAdjustPoint_Injected（ref Vector2 point, 变换 elementTransform, 画布 canvas, out Vector2 ret））
- `void PixelAdjustRect_Injected(RectTransform rectTransform, Canvas canvas, out Rect ret)`
  （void PixelAdjustRect_Injected（Rect变换 rectTransform, 画布 canvas, out Rect ret））
- `bool PointInRectangle_Injected(ref Vector2 screenPoint, RectTransform rect, Camera cam, ref Vector4 offset)`
  （bool PointInRectangle_Injected（ref Vector2 screenPoint, Rect变换 rect, 摄像机 cam, ref Vector4 offset））

---

## RectangleLight（Rectangle光照）

### 字段 (11)

- `int instanceID`（整数 实例ID）(偏移: 0x0)
- `bool shadow`（布尔值 阴影）(偏移: 0x4)
- `LightMode mode`（光照模式 mode）(偏移: 0x5)
- `Vector3 position`（三维向量 位置）(偏移: 0x8)
- `Quaternion orientation`（四元数 朝向）(偏移: 0x14)
- `LinearColor color`（线性颜色 color）(偏移: 0x24)
- `LinearColor indirectColor`（线性颜色 间接颜色）(偏移: 0x34)
- `float range`（浮点数 范围）(偏移: 0x44)
- `float width`（浮点数 宽度）(偏移: 0x48)
- `float height`（浮点数 高度）(偏移: 0x4C)
- `FalloffType falloff`（衰减类型 falloff）(偏移: 0x50)

---

## RectangularVertexClipper（RectangularVertexClipper）

### 字段 (2)

- `Vector3[] m_WorldCorners`（Vector3[] m_世界的Corners）(偏移: 0x8)
- `Vector3[] m_CanvasCorners`（Vector3[] m_画布Corners）(偏移: 0xC)

### 方法 (1)

- `Rect GetCanvasRect(RectTransform t, Canvas c)`
  （Rect 获取画布Rect（Rect变换 t, 画布 c））

---

## RecyclableImpulse（RecyclableImpulse）

**继承**: RecyclableObject（可回收对象）

### 字段 (1)

- `CinemachineImpulseSource impulse`（CinemachineImpulseSource impulse）(偏移: 0x30)

### 方法 (5)

- `void set_power(float value)`
  （void set_power（float value））
- `void set_minRadius(float value)`
  （void set_minRadius（float value））
- `void set_maxRadius(float value)`
  （void set_maxRadius（float value））
- `void set_duration(float value)`
  （void set_duration（float value））
- `void Work()`
  （void 工作（））

---

## RecyclableObject（可回收对象）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (7)

- `bool disabledAfterLife`（bool disabledAfterLife）(偏移: 0xC)
- `ObjectPool pool`（对象池 pool）(偏移: 0x10)
- `float lifeTime`（float life时间）(偏移: 0x14)
- `bool roundEndRecycle`（bool round结束Recycle）(偏移: 0x18)
- `Action WorkEvent_Listener`（动作 WorkEvent_监听器）(偏移: 0x24)
- `Action RecycleEvent_Listener`（动作 RecycleEvent_监听器）(偏移: 0x28)
- `Action NoRoundRecycleEvent_Listener`（动作 No回合RecycleEvent_监听器）(偏移: 0x2C)

### 方法 (18)

- `float get_activeTime()`
  （float get_active时间（））
- `void set_activeTime(float value)`
  （void set_active时间（float value））
- `bool get_isRecycled()`
  （bool get_isRecycled（））
- `void set_isRecycled(bool value)`
  （void set_isRecycled（bool value））
- `void add_WorkEvent_Listener(Action value)`
  （void add_WorkEvent_监听器（动作 value））
- `void remove_WorkEvent_Listener(Action value)`
  （void remove_WorkEvent_监听器（动作 value））
- `void add_RecycleEvent_Listener(Action value)`
  （void add_RecycleEvent_监听器（动作 value））
- `void remove_RecycleEvent_Listener(Action value)`
  （void remove_RecycleEvent_监听器（动作 value））
- `void add_NoRoundRecycleEvent_Listener(Action value)`
  （void add_No回合RecycleEvent_监听器（动作 value））
- `void remove_NoRoundRecycleEvent_Listener(Action value)`
  （void remove_No回合RecycleEvent_监听器（动作 value））
- `void OnEnable()`
  （void 启用时（））
- `void TryRecycle()`
  （void TryRecycle（））
- `void TryRecycle(bool roundRecycle)`
  （void TryRecycle（bool roundRecycle））
- `void Recycle(bool roundRecycle)`
  （void 回收（布尔值 循环回收））
- `void StartLifeTimer(float time)`
  （void 开始Life计时器（float time））
- `void OnLifeTimerEnd()`
  （void OnLife计时器结束（））
- `void Active()`
  （void 激活的（））
- `void Work()`
  （void 工作（））

---

## RecyclableSound（Recyclable音效）

**继承**: RecyclableObject（可回收对象）

### 字段 (1)

- `AudioSource audioSource`（音频Source audioSource）(偏移: 0x30)

### 方法 (6)

- `void Recycle(bool roundRecycle)`
  （void 回收（布尔值 循环回收））
- `void Set3dData(AudioClip clip, Vector2 distance)`
  （void Set3d数据（音频弹匣 clip, 二维向量 distance））
- `void Set3dDistance(Vector2 distance)`
  （void Set3d距离（二维向量 distance））
- `void Set3dDistance(float min, float max)`
  （void Set3d距离（float min, float max））
- `void SetClip(AudioClip clip)`
  （void 集合弹匣（音频弹匣 clip））
- `void Set2dData(AudioClip clip)`
  （void Set2d数据（音频弹匣 clip））

---

## Ref2Float（双引用浮点数）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(ref float float1, ref float float2)`
  （void Invoke（ref float float1, ref float float2））
- `IAsyncResult BeginInvoke(ref float float1, ref float float2, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（ref float float1, ref float float2, 异步回调 callback, object object））
- `void EndInvoke(ref float float1, ref float float2, IAsyncResult result)`
  （void 结束Invoke（ref float float1, ref float float2, I异步Result result））

---

## RefBool（引用布尔值）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(ref bool value)`
  （void Invoke（ref bool value））
- `IAsyncResult BeginInvoke(ref bool value, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（ref bool value, 异步回调 callback, object object））
- `void EndInvoke(ref bool value, IAsyncResult result)`
  （void 结束Invoke（ref bool value, I异步Result result））

---

## RefFloat（引用浮点数）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(ref float value)`
  （void Invoke（ref float value））
- `IAsyncResult BeginInvoke(ref float value, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（ref float value, 异步回调 callback, object object））
- `void EndInvoke(ref float value, IAsyncResult result)`
  （void 结束Invoke（ref float value, I异步Result result））

---

## RefInt（Ref整数）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(ref int value)`
  （void Invoke（ref int value））
- `IAsyncResult BeginInvoke(ref int value, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（ref int value, 异步回调 callback, object object））
- `void EndInvoke(ref int value, IAsyncResult result)`
  （void 结束Invoke（ref int value, I异步Result result））

---

## RefInt（Ref整数）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(ref int intValue, ref int priority)`
  （void Invoke（ref int intValue, ref int priority））
- `IAsyncResult BeginInvoke(ref int intValue, ref int priority, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（ref int intValue, ref int priority, 异步回调 callback, object object））
- `void EndInvoke(ref int intValue, ref int priority, IAsyncResult result)`
  （void 结束Invoke（ref int intValue, ref int priority, I异步Result result））

---

## RefPosition（RefPosition）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(ref Vector3 pos, ref int priority)`
  （void Invoke（ref Vector3 pos, ref int priority））
- `IAsyncResult BeginInvoke(ref Vector3 pos, ref int priority, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（ref Vector3 pos, ref int priority, 异步回调 callback, object object））
- `void EndInvoke(ref Vector3 pos, ref int priority, IAsyncResult result)`
  （void 结束Invoke（ref Vector3 pos, ref int priority, I异步Result result））

---

## RefString（Ref字符串）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(ref string value)`
  （void Invoke（ref string value））
- `IAsyncResult BeginInvoke(ref string value, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（ref string value, 异步回调 callback, object object））
- `void EndInvoke(ref string value, IAsyncResult result)`
  （void 结束Invoke（ref string value, I异步Result result））

---

## ReferenceConverter（引用Converter）

**继承**: TypeConverter（类型转换器）

### 字段 (2)

- `string none`（string none）(偏移: 0x0)
- `Type type`（类型 type）(偏移: 0x8)

### 方法 (7)

- `bool CanConvertFrom(ITypeDescriptorContext context, Type sourceType)`
  （布尔值 能否转换自（I类型描述符上下文 context, 类型 sourceType））
- `object ConvertFrom(ITypeDescriptorContext context, CultureInfo culture, object value)`
  （对象 转换自（I类型描述符上下文 context, 区域性信息 culture, 对象 value））
- `object ConvertTo(ITypeDescriptorContext context, CultureInfo culture, object value, Type destinationType)`
  （对象 转换到（I类型描述符上下文 context, 区域性信息 culture, 对象 value, 类型 destinationType））
- `TypeConverter.StandardValuesCollection GetStandardValues(ITypeDescriptorContext context)`
  （类型转换器.标准值集合 获取标准值（I类型描述符上下文 context））
- `bool GetStandardValuesExclusive(ITypeDescriptorContext context)`
  （布尔值 获取标准值独占（I类型描述符上下文 context））
- `bool GetStandardValuesSupported(ITypeDescriptorContext context)`
  （布尔值 获取标准值支持（I类型描述符上下文 context））
- `bool IsValueAllowed(ITypeDescriptorContext context, object value)`
  （bool 是否值Allowed（I类型DescriptorContext context, object value））

---

## ReferenceConverter.ReferenceComparer（引用Converter.引用Comparer）

**继承**: IComparer（I比较器）

### 字段 (1)

- `ReferenceConverter converter`（引用Converter converter）(偏移: 0x8)

### 方法 (1)

- `int Compare(object item1, object item2)`
  （int Compare（object item1, object item2））

---

## ReflectEventDescriptor（Reflect事件Descriptor）

**继承**: EventDescriptor（事件Descriptor）

### 字段 (6)

- `Type type`（类型 type）(偏移: 0x34)
- `Type componentClass`（类型 component类）(偏移: 0x38)
- `MethodInfo addMethod`（Method信息 addMethod）(偏移: 0x3C)
- `MethodInfo removeMethod`（Method信息 removeMethod）(偏移: 0x40)
- `EventInfo realEvent`（事件信息 real事件）(偏移: 0x44)
- `bool filledMethods`（bool filledMethods）(偏移: 0x48)

### 方法 (5)

- `Type get_EventType()`
  （类型 get_事件类型（））
- `void FillAttributes(IList attributes)`
  （void FillAttributes（I列表 attributes））
- `void FillEventInfoAttribute(EventInfo realEventInfo, IList attributes)`
  （void Fill事件信息Attribute（事件信息 realEventInfo, I列表 attributes））
- `void FillMethods()`
  （void FillMethods（））
- `void FillSingleMethodAttribute(MethodInfo realMethodInfo, IList attributes)`
  （void Fill单个MethodAttribute（Method信息 realMethodInfo, I列表 attributes））

---

## ReflectPropertyDescriptor（Reflect属性Descriptor）

**继承**: PropertyDescriptor（属性Descriptor）

### 字段 (25)

- `Type[] argsNone`（Type[] args无）(偏移: 0x0)
- `object noValue`（object no值）(偏移: 0x4)
- `TraceSwitch PropDescCreateSwitch`（TraceSwitch PropDesc创建Switch）(偏移: 0x8)
- `TraceSwitch PropDescUsageSwitch`（TraceSwitch PropDescUsageSwitch）(偏移: 0xC)
- `int BitDefaultValueQueried`（int Bit默认的值Queried）(偏移: 0x10)
- `int BitGetQueried`（int Bit获取Queried）(偏移: 0x14)
- `int BitSetQueried`（int Bit集合Queried）(偏移: 0x18)
- `int BitShouldSerializeQueried`（int Bit应该SerializeQueried）(偏移: 0x1C)
- `int BitResetQueried`（int Bit重置Queried）(偏移: 0x20)
- `int BitChangedQueried`（int BitChangedQueried）(偏移: 0x24)
- `int BitIPropChangedQueried`（int BitIPropChangedQueried）(偏移: 0x28)
- `int BitReadOnlyChecked`（int BitReadOnlyChecked）(偏移: 0x2C)
- `int BitAmbientValueQueried`（int BitAmbient值Queried）(偏移: 0x30)
- `int BitSetOnDemand`（int Bit集合OnDemand）(偏移: 0x34)
- `BitVector32 state`（BitVector32 state）(偏移: 0x44)
- `Type componentClass`（类型 component类）(偏移: 0x48)
- `Type type`（类型 type）(偏移: 0x4C)
- `object defaultValue`（object default值）(偏移: 0x50)
- `object ambientValue`（object ambient值）(偏移: 0x54)
- `PropertyInfo propInfo`（属性信息 prop信息）(偏移: 0x58)
- `MethodInfo getMethod`（Method信息 getMethod）(偏移: 0x5C)
- `MethodInfo setMethod`（Method信息 setMethod）(偏移: 0x60)
- `MethodInfo shouldSerializeMethod`（Method信息 shouldSerializeMethod）(偏移: 0x64)
- `MethodInfo resetMethod`（Method信息 resetMethod）(偏移: 0x68)
- `Type receiverType`（类型 receiver类型）(偏移: 0x6C)

### 方法 (8)

- `Type get_ComponentType()`
  （类型 get_组件类型（））
- `bool get_IsExtender()`
  （bool get_是否Extender（））
- `bool get_IsReadOnly()`
  （布尔值 获取_是否只读（））
- `Type get_PropertyType()`
  （类型 get_属性类型（））
- `MethodInfo get_SetMethodValue()`
  （Method信息 get_集合Method值（））
- `Type ExtenderGetReceiverType()`
  （类型 Extender获取Receiver类型（））
- `Type ExtenderGetType(IExtenderProvider provider)`
  （类型 Extender获取类型（IExtender提供者 provider））
- `void FillAttributes(IList attributes)`
  （void FillAttributes（I列表 attributes））

---

## ReflectTypeDescriptionProvider（Reflect类型Description提供者）

**继承**: TypeDescriptionProvider（类型描述提供者）

### 字段 (16)

- `Hashtable _typeData`（Hashtable _type数据）(偏移: 0x10)
- `Type[] _typeConstructor`（Type[] _typeConstructor）(偏移: 0x0)
- `Hashtable _editorTables`（Hashtable _editorTables）(偏移: 0x4)
- `Hashtable _intrinsicTypeConverters`（Hashtable _intrinsic类型Converters）(偏移: 0x8)
- `object _intrinsicReferenceKey`（object _intrinsic引用键）(偏移: 0xC)
- `object _intrinsicNullableKey`（object _intrinsicNullable键）(偏移: 0x10)
- `object _dictionaryKey`（object _dictionary键）(偏移: 0x14)
- `Hashtable _propertyCache`（Hashtable _property缓存）(偏移: 0x18)
- `Hashtable _eventCache`（Hashtable _event缓存）(偏移: 0x1C)
- `Hashtable _attributeCache`（Hashtable _attribute缓存）(偏移: 0x20)
- `Hashtable _extendedPropertyCache`（Hashtable _extended属性缓存）(偏移: 0x24)
- `Guid _extenderProviderKey`（Guid _extender提供者键）(偏移: 0x28)
- `Guid _extenderPropertiesKey`（Guid _extenderProperties键）(偏移: 0x38)
- `Guid _extenderProviderPropertiesKey`（Guid _extender提供者Properties键）(偏移: 0x48)
- `Type[] _skipInterfaceAttributeList`（Type[] _skipInterfaceAttribute列表）(偏移: 0x58)
- `object _internalSyncObject`（object _internal同步对象）(偏移: 0x5C)

### 方法 (41)

- `Hashtable get_IntrinsicTypeConverters()`
  （Hashtable get_Intrinsic类型Converters（））
- `void AddEditorTable(Type editorBaseType, Hashtable table)`
  （void 添加EditorTable（类型 editorBaseType, Hashtable table））
- `object CreateInstance(IServiceProvider provider, Type objectType, Type[] argTypes, object[] args)`
  （对象 创建实例（I服务提供者 provider, 类型 objectType, 类型[] argTypes, 对象[] args））
- `object CreateInstance(Type objectType, Type callingType)`
  （object 创建实例（类型 objectType, 类型 callingType））
- `AttributeCollection GetAttributes(Type type)`
  （AttributeCollection 获取Attributes（类型 type））
- `IDictionary GetCache(object instance)`
  （I字典 获取缓存（对象 instance））
- `string GetClassName(Type type)`
  （string 获取类名称（类型 type））
- `string GetComponentName(Type type, object instance)`
  （string 获取组件名称（类型 type, object instance））
- `TypeConverter GetConverter(Type type, object instance)`
  （类型Converter 获取Converter（类型 type, object instance））
- `EventDescriptor GetDefaultEvent(Type type, object instance)`
  （事件Descriptor 获取默认的事件（类型 type, object instance））
- `PropertyDescriptor GetDefaultProperty(Type type, object instance)`
  （属性Descriptor 获取默认的属性（类型 type, object instance））
- `object GetEditor(Type type, object instance, Type editorBaseType)`
  （object 获取Editor（类型 type, object instance, 类型 editorBaseType））
- `Hashtable GetEditorTable(Type editorBaseType)`
  （Hashtable 获取EditorTable（类型 editorBaseType））
- `EventDescriptorCollection GetEvents(Type type)`
  （事件DescriptorCollection 获取Events（类型 type））
- `AttributeCollection GetExtendedAttributes(object instance)`
  （AttributeCollection 获取ExtendedAttributes（object instance））
- `string GetExtendedClassName(object instance)`
  （string 获取Extended类名称（object instance））
- `string GetExtendedComponentName(object instance)`
  （string 获取Extended组件名称（object instance））
- `TypeConverter GetExtendedConverter(object instance)`
  （类型Converter 获取ExtendedConverter（object instance））
- `EventDescriptor GetExtendedDefaultEvent(object instance)`
  （事件Descriptor 获取Extended默认的事件（object instance））
- `PropertyDescriptor GetExtendedDefaultProperty(object instance)`
  （属性Descriptor 获取Extended默认的属性（object instance））
- `object GetExtendedEditor(object instance, Type editorBaseType)`
  （object 获取ExtendedEditor（object instance, 类型 editorBaseType））
- `EventDescriptorCollection GetExtendedEvents(object instance)`
  （事件DescriptorCollection 获取ExtendedEvents（object instance））
- `PropertyDescriptorCollection GetExtendedProperties(object instance)`
  （属性DescriptorCollection 获取ExtendedProperties（object instance））
- `IExtenderProvider[] GetExtenderProviders(object instance)`
  （IExtenderProvider[] 获取ExtenderProviders（object instance））
- `IExtenderProvider[] GetExtenders(ICollection components, object instance, IDictionary cache)`
  （IExtenderProvider[] 获取Extenders（ICollection components, object instance, I字典 cache））
- `ICustomTypeDescriptor GetExtendedTypeDescriptor(object instance)`
  （I自定义的类型Descriptor 获取Extended类型Descriptor（object instance））
- `string GetFullComponentName(object component)`
  （字符串 获取完整组件名称（对象 component））
- `Type[] GetPopulatedTypes(Module module)`
  （Type[] 获取PopulatedTypes（模块 module））
- `PropertyDescriptorCollection GetProperties(Type type)`
  （属性DescriptorCollection 获取Properties（类型 type））
- `Type GetReflectionType(Type objectType, object instance)`
  （类型 获取Reflection类型（类型 objectType, object instance））
- `ReflectTypeDescriptionProvider.ReflectedTypeData GetTypeData(Type type, bool createIfNeeded)`
  （Reflect类型DescriptionProvider.Reflected类型数据 获取类型数据（类型 type, bool createIfNeeded））
- `ICustomTypeDescriptor GetTypeDescriptor(Type objectType, object instance)`
  （I自定义类型描述符 获取类型描述符（类型 objectType, 对象 instance））
- `Type GetTypeFromName(string typeName)`
  （类型 获取类型From名称（string typeName））
- `bool IsPopulated(Type type)`
  （bool 是否Populated（类型 type））
- `Attribute[] ReflectGetAttributes(Type type)`
  （Attribute[] Reflect获取Attributes（类型 type））
- `Attribute[] ReflectGetAttributes(MemberInfo member)`
  （Attribute[] Reflect获取Attributes（Member信息 member））
- `EventDescriptor[] ReflectGetEvents(Type type)`
  （事件Descriptor[] Reflect获取Events（类型 type））
- `PropertyDescriptor[] ReflectGetExtendedProperties(IExtenderProvider provider)`
  （属性Descriptor[] Reflect获取ExtendedProperties（IExtender提供者 provider））
- `PropertyDescriptor[] ReflectGetProperties(Type type)`
  （属性Descriptor[] Reflect获取Properties（类型 type））
- `void Refresh(Type type)`
  （void 刷新（类型 type））
- `object SearchIntrinsicTable(Hashtable table, Type callingType)`
  （object 搜索IntrinsicTable（Hashtable table, 类型 callingType））

---

## ReflectTypeDescriptionProvider.ReflectedTypeData（Reflect类型DescriptionProvider.Reflected类型数据）

### 字段 (8)

- `Type _type`（类型 _type）(偏移: 0x8)
- `AttributeCollection _attributes`（AttributeCollection _attributes）(偏移: 0xC)
- `EventDescriptorCollection _events`（事件DescriptorCollection _events）(偏移: 0x10)
- `PropertyDescriptorCollection _properties`（属性DescriptorCollection _properties）(偏移: 0x14)
- `TypeConverter _converter`（类型Converter _converter）(偏移: 0x18)
- `object[] _editors`（object[] _editors）(偏移: 0x1C)
- `Type[] _editorTypes`（Type[] _editorTypes）(偏移: 0x20)
- `int _editorCount`（int _editor数量）(偏移: 0x24)

### 方法 (13)

- `bool get_IsPopulated()`
  （bool get_是否Populated（））
- `AttributeCollection GetAttributes()`
  （AttributeCollection 获取Attributes（））
- `string GetClassName(object instance)`
  （string 获取类名称（object instance））
- `string GetComponentName(object instance)`
  （string 获取组件名称（object instance））
- `TypeConverter GetConverter(object instance)`
  （类型Converter 获取Converter（object instance））
- `EventDescriptor GetDefaultEvent(object instance)`
  （事件Descriptor 获取默认的事件（object instance））
- `PropertyDescriptor GetDefaultProperty(object instance)`
  （属性Descriptor 获取默认的属性（object instance））
- `object GetEditor(object instance, Type editorBaseType)`
  （object 获取Editor（object instance, 类型 editorBaseType））
- `EditorAttribute GetEditorAttribute(AttributeCollection attributes, Type editorBaseType)`
  （EditorAttribute 获取EditorAttribute（AttributeCollection attributes, 类型 editorBaseType））
- `EventDescriptorCollection GetEvents()`
  （事件DescriptorCollection 获取Events（））
- `PropertyDescriptorCollection GetProperties()`
  （属性DescriptorCollection 获取Properties（））
- `Type GetTypeFromName(string typeName)`
  （类型 获取类型From名称（string typeName））
- `void Refresh()`
  （void 刷新（））

---

## ReflectionExtensions（ReflectionExtensions）

### 方法 (7)

- `bool IsEnum(Type type)`
  （bool 是否Enum（类型 type））
- `bool IsAbstract(Type type)`
  （bool 是否抽象的（类型 type））
- `bool IsSealed(Type type)`
  （bool 是否Sealed（类型 type））
- `Type BaseType(Type type)`
  （类型 基础类型（类型 type））
- `Assembly Assembly(Type type)`
  （Assembly Assembly（类型 type））
- `TypeCode GetTypeCode(Type type)`
  （类型Code 获取类型Code（类型 type））
- `bool ReflectionOnly(Assembly assm)`
  （bool ReflectionOnly（Assembly assm））

---

## ReflectionMethodsCache（ReflectionMethods缓存）

### 字段 (7)

- `ReflectionMethodsCache.Raycast3DCallback raycast3D`（ReflectionMethodsCache.Raycast3D回调 raycast3D）(偏移: 0x8)
- `ReflectionMethodsCache.RaycastAllCallback raycast3DAll`（ReflectionMethodsCache.Raycast所有回调 raycast3D所有）(偏移: 0xC)
- `ReflectionMethodsCache.GetRaycastNonAllocCallback getRaycastNonAlloc`（ReflectionMethodsCache.获取RaycastNonAlloc回调 getRaycastNonAlloc）(偏移: 0x10)
- `ReflectionMethodsCache.Raycast2DCallback raycast2D`（ReflectionMethodsCache.Raycast2D回调 raycast2D）(偏移: 0x14)
- `ReflectionMethodsCache.GetRayIntersectionAllCallback getRayIntersectionAll`（ReflectionMethodsCache.获取RayIntersection所有回调 getRayIntersection所有）(偏移: 0x18)
- `ReflectionMethodsCache.GetRayIntersectionAllNonAllocCallback getRayIntersectionAllNonAlloc`（ReflectionMethodsCache.获取RayIntersection所有NonAlloc回调 getRayIntersection所有NonAlloc）(偏移: 0x1C)
- `ReflectionMethodsCache s_ReflectionMethodsCache`（ReflectionMethods缓存 s_ReflectionMethods缓存）(偏移: 0x0)

### 方法 (1)

- `ReflectionMethodsCache get_Singleton()`
  （ReflectionMethods缓存 get_单例（））

---

## ReflectionMethodsCache.GetRayIntersectionAllCallback（ReflectionMethodsCache.获取RayIntersection所有回调）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `RaycastHit2D[] Invoke(Ray r, float f, int i)`
  （RaycastHit2D[] Invoke（Ray r, float f, int i））
- `IAsyncResult BeginInvoke(Ray r, float f, int i, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Ray r, float f, int i, 异步回调 callback, object object））
- `RaycastHit2D[] EndInvoke(IAsyncResult result)`
  （RaycastHit2D[] 结束Invoke（I异步Result result））

---

## ReflectionMethodsCache.GetRayIntersectionAllNonAllocCallback（ReflectionMethodsCache.获取RayIntersection所有NonAlloc回调）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `int Invoke(Ray r, RaycastHit2D[] results, float f, int i)`
  （int Invoke（Ray r, RaycastHit2D[] results, float f, int i））
- `IAsyncResult BeginInvoke(Ray r, RaycastHit2D[] results, float f, int i, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Ray r, RaycastHit2D[] results, float f, int i, 异步回调 callback, object object））
- `int EndInvoke(IAsyncResult result)`
  （int 结束Invoke（I异步Result result））

---

## ReflectionMethodsCache.GetRaycastNonAllocCallback（ReflectionMethodsCache.获取RaycastNonAlloc回调）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `int Invoke(Ray r, RaycastHit[] results, float f, int i)`
  （int Invoke（Ray r, RaycastHit[] results, float f, int i））
- `IAsyncResult BeginInvoke(Ray r, RaycastHit[] results, float f, int i, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Ray r, RaycastHit[] results, float f, int i, 异步回调 callback, object object））
- `int EndInvoke(IAsyncResult result)`
  （int 结束Invoke（I异步Result result））

---

## ReflectionMethodsCache.Raycast2DCallback（ReflectionMethodsCache.Raycast2D回调）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `RaycastHit2D Invoke(Vector2 p1, Vector2 p2, float f, int i)`
  （RaycastHit2D Invoke（二维向量 p1, 二维向量 p2, float f, int i））
- `IAsyncResult BeginInvoke(Vector2 p1, Vector2 p2, float f, int i, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（二维向量 p1, 二维向量 p2, float f, int i, 异步回调 callback, object object））
- `RaycastHit2D EndInvoke(IAsyncResult result)`
  （RaycastHit2D 结束Invoke（I异步Result result））

---

## ReflectionMethodsCache.Raycast3DCallback（ReflectionMethodsCache.Raycast3D回调）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `bool Invoke(Ray r, out RaycastHit hit, float f, int i)`
  （bool Invoke（Ray r, out RaycastHit hit, float f, int i））
- `IAsyncResult BeginInvoke(Ray r, out RaycastHit hit, float f, int i, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Ray r, out RaycastHit hit, float f, int i, 异步回调 callback, object object））
- `bool EndInvoke(out RaycastHit hit, IAsyncResult result)`
  （bool 结束Invoke（out RaycastHit hit, I异步Result result））

---

## ReflectionMethodsCache.RaycastAllCallback（ReflectionMethodsCache.Raycast所有回调）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `RaycastHit[] Invoke(Ray r, float f, int i)`
  （RaycastHit[] Invoke（Ray r, float f, int i））
- `IAsyncResult BeginInvoke(Ray r, float f, int i, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Ray r, float f, int i, 异步回调 callback, object object））
- `RaycastHit[] EndInvoke(IAsyncResult result)`
  （RaycastHit[] 结束Invoke（I异步Result result））

---

## ReflectionOnlyType（ReflectionOnly类型）

**继承**: RuntimeType（Runtime类型）

### 方法 (1)

- `RuntimeTypeHandle get_TypeHandle()`
  （Runtime类型句柄 get_类型句柄（））

---

## ReflectionProbe（ReflectionProbe）

**继承**: Behaviour（行为）

### 字段 (1)

- `Action<Cubemap> defaultReflectionSet`（Action<Cubemap> defaultReflection集合）(偏移: 0x4)

### 方法 (2)

- `void CallReflectionProbeEvent(ReflectionProbe probe, ReflectionProbe.ReflectionProbeEvent probeEvent)`
  （void CallReflectionProbe事件（ReflectionProbe probe, ReflectionProbe.ReflectionProbe事件 probeEvent））
- `void CallSetDefaultReflection(Cubemap defaultReflectionCubemap)`
  （void Call集合默认的Reflection（Cubemap defaultReflectionCubemap））

---

## ReflectionProbe.ReflectionProbeEvent（ReflectionProbe.ReflectionProbe事件）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ReflectionProbeSortingCriteria（ReflectionProbeSortingCriteria）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ReflectionTypeLoadException（Reflection类型加载Exception）

**继承**: SystemException, ISerializable（系统Exception, ISerializable）

### 字段 (2)

- `Type[] _classes`（Type[] _classes）(偏移: 0x44)
- `Exception[] _exceptions`（Exception[] _exceptions）(偏移: 0x48)

### 方法 (1)

- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））

---

## RefreshEventArgs（刷新事件Args）

**继承**: EventArgs（事件参数）

### 字段 (2)

- `object componentChanged`（object componentChanged）(偏移: 0x8)
- `Type typeChanged`（类型 typeChanged）(偏移: 0xC)

---

## RefreshEventHandler（刷新事件处理器）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(RefreshEventArgs e)`
  （void Invoke（刷新事件Args e））
- `IAsyncResult BeginInvoke(RefreshEventArgs e, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（刷新事件Args e, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## Regex（Regex）

**继承**: ISerializable（可序列化接口）

### 字段 (18)

- `string pattern`（string pattern）(偏移: 0x8)
- `RegexRunnerFactory factory`（RegexRunner工厂 factory）(偏移: 0xC)
- `RegexOptions roptions`（RegexOptions roptions）(偏移: 0x10)
- `TimeSpan MaximumMatchTimeout`（时间Span Maximum比赛超时）(偏移: 0x0)
- `TimeSpan InfiniteMatchTimeout`（时间Span Infinite比赛超时）(偏移: 0x8)
- `TimeSpan internalMatchTimeout`（时间Span internal比赛超时）(偏移: 0x18)
- `TimeSpan FallbackDefaultMatchTimeout`（时间Span Fallback默认的比赛超时）(偏移: 0x10)
- `TimeSpan DefaultMatchTimeout`（时间Span 默认的比赛超时）(偏移: 0x18)
- `Hashtable caps`（Hashtable caps）(偏移: 0x20)
- `Hashtable capnames`（Hashtable capnames）(偏移: 0x24)
- `string[] capslist`（string[] capslist）(偏移: 0x28)
- `int capsize`（int capsize）(偏移: 0x2C)
- `ExclusiveReference runnerref`（Exclusive引用 runnerref）(偏移: 0x30)
- `SharedReference replref`（Shared引用 replref）(偏移: 0x34)
- `RegexCode code`（RegexCode code）(偏移: 0x38)
- `bool refsInitialized`（bool refsInitialized）(偏移: 0x3C)
- `LinkedList<CachedCodeEntry> livecode`（LinkedList<CachedCodeEntry> livecode）(偏移: 0x20)
- `int cacheSize`（int cache大小）(偏移: 0x24)

### 方法 (21)

- `void ValidateMatchTimeout(TimeSpan matchTimeout)`
  （void 验证比赛超时（时间Span matchTimeout））
- `TimeSpan InitDefaultMatchTimeout()`
  （时间Span 初始化默认的比赛超时（））
- `RegexOptions get_Options()`
  （RegexOptions get_Options（））
- `TimeSpan get_MatchTimeout()`
  （时间Span get_比赛超时（））
- `bool get_RightToLeft()`
  （bool get_右To左（））
- `string ToString()`
  （字符串 转字符串（））
- `string GroupNameFromNumber(int i)`
  （string 组名称FromNumber（int i））
- `Match Match(string input, string pattern)`
  （比赛 比赛（string input, string pattern））
- `Match Match(string input, string pattern, RegexOptions options, TimeSpan matchTimeout)`
  （比赛 比赛（string input, string pattern, RegexOptions options, 时间Span matchTimeout））
- `Match Match(string input)`
  （比赛 比赛（string input））
- `Match Match(string input, int startat)`
  （比赛 比赛（string input, int startat））
- `string Replace(string input, string pattern, string replacement)`
  （string Replace（string input, string pattern, string replacement））
- `string Replace(string input, string pattern, string replacement, RegexOptions options, TimeSpan matchTimeout)`
  （string Replace（string input, string pattern, string replacement, RegexOptions options, 时间Span matchTimeout））
- `string Replace(string input, string replacement)`
  （string Replace（string input, string replacement））
- `string Replace(string input, string replacement, int count, int startat)`
  （string Replace（string input, string replacement, int count, int startat））
- `void InitializeReferences()`
  （void 初始化References（））
- `Match Run(bool quick, int prevlen, string input, int beginning, int length, int startat)`
  （比赛 运行（bool quick, int prevlen, string input, int beginning, int length, int startat））
- `CachedCodeEntry LookupCachedAndUpdate(string key)`
  （CachedCodeEntry LookupCachedAnd更新（string key））
- `CachedCodeEntry CacheCode(string key)`
  （CachedCodeEntry 缓存Code（string key））
- `bool UseOptionR()`
  （bool UseOptionR（））
- `bool UseOptionInvariant()`
  （bool UseOptionInvariant（））

---

## RegexBoyerMoore（RegexBoyerMoore）

### 字段 (9)

- `int[] _positive`（int[] _positive）(偏移: 0x8)
- `int[] _negativeASCII`（int[] _negativeASCII）(偏移: 0xC)
- `int[][] _negativeUnicode`（int[][] _negativeUnicode）(偏移: 0x10)
- `string _pattern`（string _pattern）(偏移: 0x14)
- `int _lowASCII`（int _lowASCII）(偏移: 0x18)
- `int _highASCII`（int _highASCII）(偏移: 0x1C)
- `bool _rightToLeft`（bool _rightTo左）(偏移: 0x20)
- `bool _caseInsensitive`（bool _caseInsensitive）(偏移: 0x21)
- `CultureInfo _culture`（Culture信息 _culture）(偏移: 0x24)

### 方法 (4)

- `bool MatchPattern(string text, int index)`
  （bool 比赛Pattern（string text, int index））
- `bool IsMatch(string text, int index, int beglimit, int endlimit)`
  （bool 是否比赛（string text, int index, int beglimit, int endlimit））
- `int Scan(string text, int index, int beglimit, int endlimit)`
  （int Scan（string text, int index, int beglimit, int endlimit））
- `string ToString()`
  （字符串 转字符串（））

---

## RegexCharClass（RegexChar类）

### 字段 (17)

- `List<RegexCharClass.SingleRange> _rangelist`（List<RegexCharClass.单个Range> _rangelist）(偏移: 0x8)
- `StringBuilder _categories`（字符串构建器 _categories）(偏移: 0xC)
- `bool _canonical`（bool _canonical）(偏移: 0x10)
- `bool _negate`（bool _negate）(偏移: 0x11)
- `RegexCharClass _subtractor`（RegexChar类 _subtractor）(偏移: 0x14)
- `string InternalRegexIgnoreCase`（string 内部的RegexIgnoreCase）(偏移: 0x0)
- `string Space`（string Space）(偏移: 0x4)
- `string NotSpace`（string NotSpace）(偏移: 0x8)
- `string Word`（string Word）(偏移: 0xC)
- `string NotWord`（string NotWord）(偏移: 0x10)
- `string SpaceClass`（string Space类）(偏移: 0x14)
- `string NotSpaceClass`（string NotSpace类）(偏移: 0x18)
- `string WordClass`（string Word类）(偏移: 0x1C)
- `string NotWordClass`（string NotWord类）(偏移: 0x20)
- `string DigitClass`（string Digit类）(偏移: 0x24)
- `string NotDigitClass`（string NotDigit类）(偏移: 0x28)
- `RegexCharClass.LowerCaseMapping[] _lcTable`（RegexCharClass.下半身CaseMapping[] _lcTable）(偏移: 0x34)

### 方法 (36)

- `bool get_CanMerge()`
  （bool get_能否Merge（））
- `void set_Negate(bool value)`
  （void set_Negate（bool value））
- `void AddChar(char c)`
  （void 添加Char（char c））
- `void AddCharClass(RegexCharClass cc)`
  （void 添加Char类（RegexChar类 cc））
- `void AddSet(string set)`
  （void 添加集合（string set））
- `void AddSubtraction(RegexCharClass sub)`
  （void 添加Subtraction（RegexChar类 sub））
- `void AddRange(char first, char last)`
  （void 添加范围（char first, char last））
- `void AddCategoryFromName(string categoryName, bool invert, bool caseInsensitive, string pattern)`
  （void 添加类别From名称（string categoryName, bool invert, bool caseInsensitive, string pattern））
- `void AddCategory(string category)`
  （void 添加类别（string category））
- `void AddLowercase(CultureInfo culture)`
  （void 添加Lowercase（Culture信息 culture））
- `void AddLowercaseRange(char chMin, char chMax, CultureInfo culture)`
  （void 添加Lowercase范围（char chMin, char chMax, Culture信息 culture））
- `void AddWord(bool ecma, bool negate)`
  （void 添加Word（bool ecma, bool negate））
- `void AddSpace(bool ecma, bool negate)`
  （void 添加Space（bool ecma, bool negate））
- `void AddDigit(bool ecma, bool negate, string pattern)`
  （void 添加Digit（bool ecma, bool negate, string pattern））
- `char SingletonChar(string set)`
  （char 单例Char（string set））
- `bool IsMergeable(string charClass)`
  （bool 是否Mergeable（string charClass））
- `bool IsEmpty(string charClass)`
  （bool 是否空（string charClass））
- `bool IsSingleton(string set)`
  （bool 是否单例（string set））
- `bool IsSingletonInverse(string set)`
  （bool 是否单例Inverse（string set））
- `bool IsSubtraction(string charClass)`
  （bool 是否Subtraction（string charClass））
- `bool IsNegated(string set)`
  （bool 是否Negated（string set））
- `bool IsECMAWordChar(char ch)`
  （bool 是否ECMAWordChar（char ch））
- `bool IsWordChar(char ch)`
  （bool 是否WordChar（char ch））
- `bool CharInClass(char ch, string set)`
  （bool CharIn类（char ch, string set））
- `bool CharInClassRecursive(char ch, string set, int start)`
  （bool CharIn类Recursive（char ch, string set, int start））
- `bool CharInClassInternal(char ch, string set, int start, int mySetLength, int myCategoryLength)`
  （bool CharIn类内部的（char ch, string set, int start, int mySetLength, int myCategoryLength））
- `bool CharInCategory(char ch, string set, int start, int mySetLength, int myCategoryLength)`
  （bool CharIn类别（char ch, string set, int start, int mySetLength, int myCategoryLength））
- `bool CharInCategoryGroup(char ch, UnicodeCategory chcategory, string category, ref int i)`
  （bool CharIn类别组（char ch, Unicode类别 chcategory, string category, ref int i））
- `string NegateCategory(string category)`
  （string Negate类别（string category））
- `RegexCharClass Parse(string charClass)`
  （RegexChar类 解析（string charClass））
- `RegexCharClass ParseRecursive(string charClass, int start)`
  （RegexChar类 解析Recursive（string charClass, int start））
- `int RangeCount()`
  （int 范围数量（））
- `string ToStringClass()`
  （string To字符串类（））
- `RegexCharClass.SingleRange GetRangeAt(int i)`
  （RegexCharClass.单个范围 获取范围At（int i））
- `void Canonicalize()`
  （void Canonicalize（））
- `string SetFromProperty(string capname, bool invert, string pattern)`
  （string 集合From属性（string capname, bool invert, string pattern））

---

## RegexCharClass.LowerCaseMapping（RegexCharClass.下半身CaseMapping）

### 字段 (4)

- `char _chMin`（char _ch最小）(偏移: 0x0)
- `char _chMax`（char _ch最大）(偏移: 0x2)
- `int _lcOp`（int _lcOp）(偏移: 0x4)
- `int _data`（int _data）(偏移: 0x8)

---

## RegexCharClass.SingleRange（RegexCharClass.单个范围）

### 字段 (2)

- `char _first`（char _first）(偏移: 0x8)
- `char _last`（char _last）(偏移: 0xA)

---

## RegexCharClass.SingleRangeComparer（RegexCharClass.单个范围Comparer）

**继承**: IComparer<RegexCharClass.SingleRange>（IComparer<RegexCharClass.单个Range>）

### 方法 (1)

- `int Compare(RegexCharClass.SingleRange x, RegexCharClass.SingleRange y)`
  （int Compare（RegexCharClass.单个范围 x, RegexCharClass.单个范围 y））

---

## RegexCode（RegexCode）

### 字段 (9)

- `int[] _codes`（int[] _codes）(偏移: 0x8)
- `string[] _strings`（string[] _strings）(偏移: 0xC)
- `int _trackcount`（int _trackcount）(偏移: 0x10)
- `Hashtable _caps`（哈希表 _caps）(偏移: 0x14)
- `int _capsize`（int _capsize）(偏移: 0x18)
- `RegexPrefix _fcPrefix`（RegexPrefix _fcPrefix）(偏移: 0x1C)
- `RegexBoyerMoore _bmPrefix`（RegexBoyerMoore _bmPrefix）(偏移: 0x20)
- `int _anchors`（int _anchors）(偏移: 0x24)
- `bool _rightToLeft`（bool _rightTo左）(偏移: 0x28)

### 方法 (1)

- `bool OpcodeBacktracks(int Op)`
  （bool OpcodeBacktracks（int Op））

---

## RegexFC（RegexFC）

### 字段 (3)

- `RegexCharClass _cc`（RegexChar类 _cc）(偏移: 0x8)
- `bool _nullable`（bool _nullable）(偏移: 0xC)
- `bool _caseInsensitive`（bool _caseInsensitive）(偏移: 0xD)

### 方法 (3)

- `bool AddFC(RegexFC fc, bool concatenate)`
  （bool 添加FC（RegexFC fc, bool concatenate））
- `string GetFirstChars(CultureInfo culture)`
  （string 获取第一个Chars（Culture信息 culture））
- `bool IsCaseInsensitive()`
  （bool 是否CaseInsensitive（））

---

## RegexFCD（RegexFCD）

### 字段 (7)

- `int[] _intStack`（int[] _int栈）(偏移: 0x8)
- `int _intDepth`（int _int深度）(偏移: 0xC)
- `RegexFC[] _fcStack`（RegexFC[] _fc栈）(偏移: 0x10)
- `int _fcDepth`（int _fc深度）(偏移: 0x14)
- `bool _skipAllChildren`（bool _skip所有Children）(偏移: 0x18)
- `bool _skipchild`（bool _skipchild）(偏移: 0x19)
- `bool _failed`（bool _failed）(偏移: 0x1A)

### 方法 (14)

- `RegexPrefix FirstChars(RegexTree t)`
  （RegexPrefix 第一个Chars（RegexTree t））
- `RegexPrefix Prefix(RegexTree tree)`
  （RegexPrefix Prefix（RegexTree tree））
- `int Anchors(RegexTree tree)`
  （int Anchors（RegexTree tree））
- `int AnchorFromType(int type)`
  （int AnchorFrom类型（int type））
- `void PushInt(int I)`
  （void Push整数（int I））
- `bool IntIsEmpty()`
  （bool 整数是否空（））
- `int PopInt()`
  （int Pop整数（））
- `void PushFC(RegexFC fc)`
  （void PushFC（RegexFC fc））
- `bool FCIsEmpty()`
  （bool FC是否空（））
- `RegexFC PopFC()`
  （RegexFC PopFC（））
- `RegexFC TopFC()`
  （RegexFC 顶部FC（））
- `RegexFC RegexFCFromRegexTree(RegexTree tree)`
  （RegexFC RegexFCFromRegexTree（RegexTree tree））
- `void SkipChild()`
  （void Skip子级（））
- `void CalculateFC(int NodeType, RegexNode node, int CurIndex)`
  （void 计算FC（int NodeType, Regex节点 node, int CurIndex））

---

## RegexInterpreter（RegexInterpreter）

**继承**: RegexRunner（RegexRunner）

### 字段 (11)

- `int runoperator`（int runoperator）(偏移: 0x50)
- `int[] runcodes`（int[] runcodes）(偏移: 0x54)
- `int runcodepos`（int runcodepos）(偏移: 0x58)
- `string[] runstrings`（string[] runstrings）(偏移: 0x5C)
- `RegexCode runcode`（RegexCode runcode）(偏移: 0x60)
- `RegexPrefix runfcPrefix`（RegexPrefix runfcPrefix）(偏移: 0x64)
- `RegexBoyerMoore runbmPrefix`（RegexBoyerMoore runbmPrefix）(偏移: 0x68)
- `int runanchors`（int runanchors）(偏移: 0x6C)
- `bool runrtl`（bool runrtl）(偏移: 0x70)
- `bool runci`（bool runci）(偏移: 0x71)
- `CultureInfo runculture`（Culture信息 runculture）(偏移: 0x74)

### 方法 (40)

- `void InitTrackCount()`
  （void 初始化Track数量（））
- `void Advance()`
  （void Advance（））
- `void Advance(int i)`
  （void Advance（int i））
- `void Goto(int newpos)`
  （void Goto（int newpos））
- `void Textto(int newpos)`
  （void Textto（int newpos））
- `void Trackto(int newpos)`
  （void Trackto（int newpos））
- `int Textstart()`
  （int Textstart（））
- `int Textpos()`
  （int Textpos（））
- `int Trackpos()`
  （int Trackpos（））
- `void TrackPush()`
  （void TrackPush（））
- `void TrackPush(int I1)`
  （void TrackPush（int I1））
- `void TrackPush(int I1, int I2)`
  （void TrackPush（int I1, int I2））
- `void TrackPush(int I1, int I2, int I3)`
  （void TrackPush（int I1, int I2, int I3））
- `void TrackPush2(int I1)`
  （void TrackPush2（int I1））
- `void TrackPush2(int I1, int I2)`
  （void TrackPush2（int I1, int I2））
- `void Backtrack()`
  （void Backtrack（））
- `void SetOperator(int op)`
  （void 集合Operator（int op））
- `void TrackPop()`
  （void TrackPop（））
- `void TrackPop(int framesize)`
  （void TrackPop（int framesize））
- `int TrackPeek()`
  （int TrackPeek（））
- `int TrackPeek(int i)`
  （int TrackPeek（int i））
- `void StackPush(int I1)`
  （void 栈Push（int I1））
- `void StackPush(int I1, int I2)`
  （void 栈Push（int I1, int I2））
- `void StackPop()`
  （void 栈Pop（））
- `void StackPop(int framesize)`
  （void 栈Pop（int framesize））
- `int StackPeek()`
  （int 栈Peek（））
- `int StackPeek(int i)`
  （int 栈Peek（int i））
- `int Operator()`
  （int Operator（））
- `int Operand(int i)`
  （int Operand（int i））
- `int Leftchars()`
  （int Leftchars（））
- `int Rightchars()`
  （int Rightchars（））
- `int Bump()`
  （int Bump（））
- `int Forwardchars()`
  （int Forwardchars（））
- `char Forwardcharnext()`
  （char Forwardcharnext（））
- `bool Stringmatch(string str)`
  （bool Stringmatch（string str））
- `bool Refmatch(int index, int len)`
  （bool Refmatch（int index, int len））
- `void Backwardnext()`
  （void Backwardnext（））
- `char CharAt(int j)`
  （char CharAt（int j））
- `bool FindFirstChar()`
  （bool 查找第一个Char（））
- `void Go()`
  （void Go（））

---

## RegexMatchTimeoutException（Regex比赛超时Exception）

**继承**: TimeoutException, ISerializable（超时Exception, ISerializable）

### 字段 (3)

- `string regexInput`（string regex输入）(偏移: 0x44)
- `string regexPattern`（string regexPattern）(偏移: 0x48)
- `TimeSpan matchTimeout`（时间Span match超时）(偏移: 0x50)

### 方法 (2)

- `void Init()`
  （void 初始化（））
- `void Init(string input, string pattern, TimeSpan timeout)`
  （void 初始化（string input, string pattern, 时间Span timeout））

---

## RegexNode（Regex节点）

### 字段 (8)

- `int _type`（int _type）(偏移: 0x8)
- `List<RegexNode> _children`（List<RegexNode> _children）(偏移: 0xC)
- `string _str`（string _str）(偏移: 0x10)
- `char _ch`（char _ch）(偏移: 0x14)
- `int _m`（int _m）(偏移: 0x18)
- `int _n`（int _n）(偏移: 0x1C)
- `RegexOptions _options`（RegexOptions _options）(偏移: 0x20)
- `RegexNode _next`（Regex节点 _next）(偏移: 0x24)

### 方法 (15)

- `bool UseOptionR()`
  （bool UseOptionR（））
- `RegexNode ReverseLeft()`
  （Regex节点 Reverse左（））
- `void MakeRep(int type, int min, int max)`
  （void MakeRep（int type, int min, int max））
- `RegexNode Reduce()`
  （Regex节点 Reduce（））
- `RegexNode StripEnation(int emptyType)`
  （Regex节点 StripEnation（int emptyType））
- `RegexNode ReduceGroup()`
  （Regex节点 Reduce组（））
- `RegexNode ReduceRep()`
  （Regex节点 ReduceRep（））
- `RegexNode ReduceSet()`
  （Regex节点 Reduce集合（））
- `RegexNode ReduceAlternation()`
  （Regex节点 ReduceAlternation（））
- `RegexNode ReduceConcatenation()`
  （Regex节点 ReduceConcatenation（））
- `RegexNode MakeQuantifier(bool lazy, int min, int max)`
  （Regex节点 MakeQuantifier（bool lazy, int min, int max））
- `void AddChild(RegexNode newChild)`
  （void 添加子级（Regex节点 newChild））
- `RegexNode Child(int i)`
  （Regex节点 子级（int i））
- `int ChildCount()`
  （int 子级数量（））
- `int Type()`
  （int 类型（））

---

## RegexOptions（RegexOptions）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RegexParser（RegexParser）

### 字段 (20)

- `RegexNode _stack`（Regex节点 _stack）(偏移: 0x8)
- `RegexNode _group`（Regex节点 _group）(偏移: 0xC)
- `RegexNode _alternation`（Regex节点 _alternation）(偏移: 0x10)
- `RegexNode _concatenation`（Regex节点 _concatenation）(偏移: 0x14)
- `RegexNode _unit`（Regex节点 _unit）(偏移: 0x18)
- `string _pattern`（string _pattern）(偏移: 0x1C)
- `int _currentPos`（int _currentPos）(偏移: 0x20)
- `CultureInfo _culture`（Culture信息 _culture）(偏移: 0x24)
- `int _autocap`（int _autocap）(偏移: 0x28)
- `int _capcount`（int _capcount）(偏移: 0x2C)
- `int _captop`（int _captop）(偏移: 0x30)
- `int _capsize`（int _capsize）(偏移: 0x34)
- `Hashtable _caps`（哈希表 _caps）(偏移: 0x38)
- `Hashtable _capnames`（Hashtable _capnames）(偏移: 0x3C)
- `int[] _capnumlist`（int[] _capnumlist）(偏移: 0x40)
- `List<string> _capnamelist`（List<string> _capnamelist）(偏移: 0x44)
- `RegexOptions _options`（RegexOptions _options）(偏移: 0x48)
- `List<RegexOptions> _optionsStack`（List<RegexOptions> _options栈）(偏移: 0x4C)
- `bool _ignoreNextParen`（bool _ignore下一个Paren）(偏移: 0x50)
- `byte[] _category`（byte[] _category）(偏移: 0x0)

### 方法 (74)

- `RegexTree Parse(string re, RegexOptions op)`
  （RegexTree 解析（string re, RegexOptions op））
- `RegexReplacement ParseReplacement(string rep, Hashtable caps, int capsize, Hashtable capnames, RegexOptions op)`
  （RegexReplacement 解析Replacement（string rep, Hashtable caps, int capsize, Hashtable capnames, RegexOptions op））
- `void SetPattern(string Re)`
  （void 集合Pattern（string Re））
- `void Reset(RegexOptions topopts)`
  （void 重置（RegexOptions topopts））
- `RegexNode ScanRegex()`
  （Regex节点 ScanRegex（））
- `RegexNode ScanReplacement()`
  （Regex节点 ScanReplacement（））
- `RegexCharClass ScanCharClass(bool caseInsensitive)`
  （RegexChar类 ScanChar类（bool caseInsensitive））
- `RegexCharClass ScanCharClass(bool caseInsensitive, bool scanOnly)`
  （RegexChar类 ScanChar类（bool caseInsensitive, bool scanOnly））
- `RegexNode ScanGroupOpen()`
  （Regex节点 Scan组打开（））
- `void ScanBlank()`
  （void ScanBlank（））
- `RegexNode ScanBackslash()`
  （Regex节点 ScanBackslash（））
- `RegexNode ScanBasicBackslash()`
  （Regex节点 ScanBasicBackslash（））
- `RegexNode ScanDollar()`
  （Regex节点 ScanDollar（））
- `string ScanCapname()`
  （string ScanCapname（））
- `char ScanOctal()`
  （char ScanOctal（））
- `int ScanDecimal()`
  （int ScanDecimal（））
- `char ScanHex(int c)`
  （char ScanHex（int c））
- `int HexDigit(char ch)`
  （int HexDigit（char ch））
- `char ScanControl()`
  （char Scan控制（））
- `bool IsOnlyTopOption(RegexOptions option)`
  （bool 是否Only顶部Option（RegexOptions option））
- `void ScanOptions()`
  （void ScanOptions（））
- `char ScanCharEscape()`
  （char ScanCharEscape（））
- `string ParseProperty()`
  （string 解析属性（））
- `int TypeFromCode(char ch)`
  （int 类型FromCode（char ch））
- `RegexOptions OptionFromCode(char ch)`
  （RegexOptions OptionFromCode（char ch））
- `void CountCaptures()`
  （void 数量Captures（））
- `void NoteCaptureSlot(int i, int pos)`
  （void NoteCapture槽位（int i, int pos））
- `void NoteCaptureName(string name, int pos)`
  （void NoteCapture名称（string name, int pos））
- `void NoteCaptures(Hashtable caps, int capsize, Hashtable capnames)`
  （void NoteCaptures（Hashtable caps, int capsize, Hashtable capnames））
- `void AssignNameSlots()`
  （void Assign名称Slots（））
- `int CaptureSlotFromName(string capname)`
  （int Capture槽位From名称（string capname））
- `bool IsCaptureSlot(int i)`
  （bool 是否Capture槽位（int i））
- `bool IsCaptureName(string capname)`
  （bool 是否Capture名称（string capname））
- `bool UseOptionN()`
  （bool UseOptionN（））
- `bool UseOptionI()`
  （bool UseOptionI（））
- `bool UseOptionM()`
  （bool UseOptionM（））
- `bool UseOptionS()`
  （bool UseOptionS（））
- `bool UseOptionX()`
  （bool UseOptionX（））
- `bool UseOptionE()`
  （bool UseOptionE（））
- `bool IsSpecial(char ch)`
  （bool 是否特殊（char ch））
- `bool IsStopperX(char ch)`
  （bool 是否StopperX（char ch））
- `bool IsQuantifier(char ch)`
  （bool 是否Quantifier（char ch））
- `bool IsTrueQuantifier()`
  （bool 是否TrueQuantifier（））
- `bool IsSpace(char ch)`
  （bool 是否Space（char ch））
- `void AddConcatenate(int pos, int cch, bool isReplacement)`
  （void 添加Concatenate（int pos, int cch, bool isReplacement））
- `void PushGroup()`
  （void Push组（））
- `void PopGroup()`
  （void Pop组（））
- `bool EmptyStack()`
  （bool 空栈（））
- `void StartGroup(RegexNode openGroup)`
  （void 开始组（Regex节点 openGroup））
- `void AddAlternate()`
  （void 添加Alternate（））
- `void AddConcatenate()`
  （void 添加Concatenate（））
- `void AddConcatenate(bool lazy, int min, int max)`
  （void 添加Concatenate（bool lazy, int min, int max））
- `RegexNode Unit()`
  （Regex节点 Unit（））
- `void AddUnitOne(char ch)`
  （void 添加UnitOne（char ch））
- `void AddUnitNotone(char ch)`
  （void 添加UnitNotone（char ch））
- `void AddUnitSet(string cc)`
  （void 添加Unit集合（string cc））
- `void AddUnitNode(RegexNode node)`
  （void 添加Unit节点（Regex节点 node））
- `void AddUnitType(int type)`
  （void 添加Unit类型（int type））
- `void AddGroup()`
  （void 添加组（））
- `void PushOptions()`
  （void PushOptions（））
- `void PopOptions()`
  （void PopOptions（））
- `bool EmptyOptionsStack()`
  （bool 空Options栈（））
- `void PopKeepOptions()`
  （void PopKeepOptions（））
- `ArgumentException MakeException(string message)`
  （ArgumentException MakeException（string message））
- `int Textpos()`
  （int Textpos（））
- `void Textto(int pos)`
  （void Textto（int pos））
- `char MoveRightGetChar()`
  （char 移动右获取Char（））
- `void MoveRight()`
  （void 移动右（））
- `void MoveRight(int i)`
  （void 移动右（int i））
- `void MoveLeft()`
  （void 移动左（））
- `char CharAt(int i)`
  （char CharAt（int i））
- `char RightChar()`
  （char 右Char（））
- `char RightChar(int i)`
  （char 右Char（int i））
- `int CharsRight()`
  （int Chars右（））

---

## RegexPrefix（RegexPrefix）

### 字段 (3)

- `string _prefix`（string _prefix）(偏移: 0x8)
- `bool _caseInsensitive`（bool _caseInsensitive）(偏移: 0xC)
- `RegexPrefix _empty`（RegexPrefix _empty）(偏移: 0x0)

### 方法 (3)

- `string get_Prefix()`
  （string get_Prefix（））
- `bool get_CaseInsensitive()`
  （bool get_CaseInsensitive（））
- `RegexPrefix get_Empty()`
  （RegexPrefix get_空（））

---

## RegexReplacement（RegexReplacement）

### 字段 (3)

- `string _rep`（string _rep）(偏移: 0x8)
- `List<string> _strings`（List<string> _strings）(偏移: 0xC)
- `List<int> _rules`（List<int> _rules）(偏移: 0x10)

### 方法 (4)

- `void ReplacementImpl(StringBuilder sb, Match match)`
  （void ReplacementImpl（字符串构建器 sb, 比赛 match））
- `void ReplacementImplRTL(List<string> al, Match match)`
  （void ReplacementImplRTL（List<string> al, 比赛 match））
- `string get_Pattern()`
  （string get_Pattern（））
- `string Replace(Regex regex, string input, int count, int startat)`
  （string Replace（Regex regex, string input, int count, int startat））

---

## RegexRunner（RegexRunner）

### 字段 (18)

- `int runtextbeg`（int runtextbeg）(偏移: 0x8)
- `int runtextend`（int runtextend）(偏移: 0xC)
- `int runtextstart`（int runtextstart）(偏移: 0x10)
- `string runtext`（string runtext）(偏移: 0x14)
- `int runtextpos`（int runtextpos）(偏移: 0x18)
- `int[] runtrack`（int[] runtrack）(偏移: 0x1C)
- `int runtrackpos`（int runtrackpos）(偏移: 0x20)
- `int[] runstack`（int[] runstack）(偏移: 0x24)
- `int runstackpos`（int runstackpos）(偏移: 0x28)
- `int[] runcrawl`（int[] runcrawl）(偏移: 0x2C)
- `int runcrawlpos`（int runcrawlpos）(偏移: 0x30)
- `int runtrackcount`（int runtrackcount）(偏移: 0x34)
- `Match runmatch`（比赛 runmatch）(偏移: 0x38)
- `Regex runregex`（Regex runregex）(偏移: 0x3C)
- `int timeout`（int timeout）(偏移: 0x40)
- `bool ignoreTimeout`（bool ignore超时）(偏移: 0x44)
- `int timeoutOccursAt`（int timeoutOccursAt）(偏移: 0x48)
- `int timeoutChecksToSkip`（int timeoutChecksToSkip）(偏移: 0x4C)

### 方法 (21)

- `Match Scan(Regex regex, string text, int textbeg, int textend, int textstart, int prevlen, bool quick, TimeSpan timeout)`
  （比赛 Scan（Regex regex, string text, int textbeg, int textend, int textstart, int prevlen, bool quick, 时间Span timeout））
- `void StartTimeoutWatch()`
  （void 开始超时Watch（））
- `void CheckTimeout()`
  （void 检查超时（））
- `void DoCheckTimeout()`
  （void Do检查超时（））
- `void InitMatch()`
  （void 初始化比赛（））
- `Match TidyMatch(bool quick)`
  （比赛 Tidy比赛（bool quick））
- `void EnsureStorage()`
  （void EnsureStorage（））
- `bool IsBoundary(int index, int startpos, int endpos)`
  （bool 是否Boundary（int index, int startpos, int endpos））
- `bool IsECMABoundary(int index, int startpos, int endpos)`
  （bool 是否ECMABoundary（int index, int startpos, int endpos））
- `void DoubleTrack()`
  （void DoubleTrack（））
- `void DoubleStack()`
  （void Double栈（））
- `void DoubleCrawl()`
  （void DoubleCrawl（））
- `void Crawl(int i)`
  （void Crawl（int i））
- `int Popcrawl()`
  （int Popcrawl（））
- `int Crawlpos()`
  （int Crawlpos（））
- `void Capture(int capnum, int start, int end)`
  （void Capture（int capnum, int start, int end））
- `void TransferCapture(int capnum, int uncapnum, int start, int end)`
  （void TransferCapture（int capnum, int uncapnum, int start, int end））
- `void Uncapture()`
  （void Uncapture（））
- `bool IsMatched(int cap)`
  （bool 是否Matched（int cap））
- `int MatchIndex(int cap)`
  （int 比赛索引（int cap））
- `int MatchLength(int cap)`
  （int 比赛Length（int cap））

---

## RegexTree（RegexTree）

### 字段 (7)

- `RegexNode _root`（Regex节点 _root）(偏移: 0x8)
- `Hashtable _caps`（哈希表 _caps）(偏移: 0xC)
- `int[] _capnumlist`（int[] _capnumlist）(偏移: 0x10)
- `Hashtable _capnames`（Hashtable _capnames）(偏移: 0x14)
- `string[] _capslist`（string[] _capslist）(偏移: 0x18)
- `RegexOptions _options`（RegexOptions _options）(偏移: 0x1C)
- `int _captop`（int _captop）(偏移: 0x20)

---

## RegexWriter（Regex写入器）

### 字段 (9)

- `int[] _intStack`（int[] _int栈）(偏移: 0x8)
- `int _depth`（int _depth）(偏移: 0xC)
- `int[] _emitted`（int[] _emitted）(偏移: 0x10)
- `int _curpos`（int _curpos）(偏移: 0x14)
- `List<string> _stringtable`（List<string> _stringtable）(偏移: 0x1C)
- `bool _counting`（bool _counting）(偏移: 0x20)
- `int _count`（int _count）(偏移: 0x24)
- `int _trackcount`（int _trackcount）(偏移: 0x28)
- `Hashtable _caps`（哈希表 _caps）(偏移: 0x2C)

### 方法 (14)

- `RegexCode Write(RegexTree t)`
  （RegexCode Write（RegexTree t））
- `void PushInt(int I)`
  （void Push整数（int I））
- `bool EmptyStack()`
  （bool 空栈（））
- `int PopInt()`
  （int Pop整数（））
- `int CurPos()`
  （int CurPos（））
- `void PatchJump(int Offset, int jumpDest)`
  （void Patch跳跃（int Offset, int jumpDest））
- `void Emit(int op)`
  （void Emit（int op））
- `void Emit(int op, int opd1)`
  （void Emit（int op, int opd1））
- `void Emit(int op, int opd1, int opd2)`
  （void Emit（int op, int opd1, int opd2））
- `int StringCode(string str)`
  （int 字符串Code（string str））
- `ArgumentException MakeException(string message)`
  （ArgumentException MakeException（string message））
- `int MapCapnum(int capnum)`
  （int 映射Capnum（int capnum））
- `RegexCode RegexCodeFromRegexTree(RegexTree tree)`
  （RegexCode RegexCodeFromRegexTree（RegexTree tree））
- `void EmitFragment(int nodetype, RegexNode node, int CurIndex)`
  （void EmitFragment（int nodetype, Regex节点 node, int CurIndex））

---

## RegionInfo（Region信息）

### 字段 (11)

- `RegionInfo currentRegion`（Region信息 currentRegion）(偏移: 0x0)
- `int regionId`（int regionId）(偏移: 0x8)
- `string iso2Name`（string iso2名称）(偏移: 0xC)
- `string iso3Name`（string iso3名称）(偏移: 0x10)
- `string win3Name`（string win3名称）(偏移: 0x14)
- `string englishName`（string english名称）(偏移: 0x18)
- `string nativeName`（string native名称）(偏移: 0x1C)
- `string currencySymbol`（string currencySymbol）(偏移: 0x20)
- `string isoCurrencySymbol`（string iso货币Symbol）(偏移: 0x24)
- `string currencyEnglishName`（string currencyEnglish名称）(偏移: 0x28)
- `string currencyNativeName`（string currencyNative名称）(偏移: 0x2C)

### 方法 (20)

- `RegionInfo get_CurrentRegion()`
  （Region信息 get_当前Region（））
- `bool GetByTerritory(CultureInfo ci)`
  （bool 获取ByTerritory（Culture信息 ci））
- `bool construct_internal_region_from_name(string name)`
  （bool construct_internal_region_from_name（string name））
- `string get_CurrencyEnglishName()`
  （string get_货币English名称（））
- `string get_CurrencySymbol()`
  （string get_货币Symbol（））
- `string get_DisplayName()`
  （字符串 获取_显示名称（））
- `string get_EnglishName()`
  （string get_English名称（））
- `int get_GeoId()`
  （int get_GeoId（））
- `bool get_IsMetric()`
  （bool get_是否Metric（））
- `string get_ISOCurrencySymbol()`
  （string get_ISO货币Symbol（））
- `string get_NativeName()`
  （string get_Native名称（））
- `string get_CurrencyNativeName()`
  （string get_货币Native名称（））
- `string get_Name()`
  （字符串 获取_名称（））
- `string get_ThreeLetterISORegionName()`
  （string get_ThreeLetterISORegion名称（））
- `string get_ThreeLetterWindowsRegionName()`
  （string get_ThreeLetterWindowsRegion名称（））
- `string get_TwoLetterISORegionName()`
  （string get_TwoLetterISORegion名称（））
- `bool Equals(object value)`
  （布尔值 等于（对象 value））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `string ToString()`
  （字符串 转字符串（））
- `void ClearCachedData()`
  （void 清除Cached数据（））

---

## RegisteredWaitHandle（RegisteredWait句柄）

**继承**: MarshalByRefObject（MarshalByRef对象）

### 字段 (9)

- `WaitHandle _waitObject`（Wait句柄 _wait对象）(偏移: 0xC)
- `WaitOrTimerCallback _callback`（WaitOr计时器回调 _callback）(偏移: 0x10)
- `object _state`（object _state）(偏移: 0x14)
- `WaitHandle _finalEvent`（Wait句柄 _final事件）(偏移: 0x18)
- `ManualResetEvent _cancelEvent`（手动重置事件 _cancel事件）(偏移: 0x1C)
- `TimeSpan _timeout`（时间Span _timeout）(偏移: 0x20)
- `int _callsInProcess`（int _callsIn处理）(偏移: 0x28)
- `bool _executeOnlyOnce`（bool _executeOnlyOnce）(偏移: 0x2C)
- `bool _unregistered`（bool _unregistered）(偏移: 0x2D)

### 方法 (2)

- `void Wait(object state)`
  （void Wait（object state））
- `void DoCallBack(object timedOut)`
  （void DoCall后（object timedOut））

---

## Registry（Registry）

### 字段 (7)

- `RegistryKey ClassesRoot`（Registry键 Classes根）(偏移: 0x0)
- `RegistryKey CurrentConfig`（Registry键 当前配置）(偏移: 0x4)
- `RegistryKey CurrentUser`（Registry键 当前User）(偏移: 0x8)
- `RegistryKey DynData`（Registry键 Dyn数据）(偏移: 0xC)
- `RegistryKey LocalMachine`（Registry键 本地的Machine）(偏移: 0x10)
- `RegistryKey PerformanceData`（Registry键 Performance数据）(偏移: 0x14)
- `RegistryKey Users`（Registry键 Users）(偏移: 0x18)

---

## RegistryHive（RegistryHive）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RegistryKey（Registry键）

**继承**: MarshalByRefObject, IDisposable（MarshalByRef对象, 可释放接口）

### 字段 (7)

- `object handle`（object handle）(偏移: 0xC)
- `SafeRegistryHandle safe_handle`（SafeRegistry句柄 safe_handle）(偏移: 0x10)
- `object hive`（object hive）(偏移: 0x14)
- `string qname`（string qname）(偏移: 0x18)
- `bool isRemoteRoot`（bool isRemote根）(偏移: 0x1C)
- `bool isWritable`（bool isWritable）(偏移: 0x1D)
- `IRegistryApi RegistryApi`（IRegistryApi RegistryApi）(偏移: 0x0)

### 方法 (20)

- `bool IsEquals(RegistryKey a, RegistryKey b)`
  （bool 是否Equals（Registry键 a, Registry键 b））
- `void Dispose()`
  （void 释放（））
- `string get_Name()`
  （字符串 获取_名称（））
- `void Flush()`
  （void 刷新（））
- `void Close()`
  （void 关闭（））
- `SafeRegistryHandle get_Handle()`
  （SafeRegistry句柄 get_句柄（））
- `RegistryKey OpenSubKey(string name)`
  （Registry键 打开子键（string name））
- `RegistryKey OpenSubKey(string name, bool writable)`
  （Registry键 打开子键（string name, bool writable））
- `object GetValue(string name)`
  （object 获取值（string name））
- `object GetValue(string name, object defaultValue)`
  （object 获取值（string name, object defaultValue））
- `string[] GetSubKeyNames()`
  （string[] 获取子键Names（））
- `string ToString()`
  （字符串 转字符串（））
- `bool get_IsRoot()`
  （bool get_是否根（））
- `RegistryHive get_Hive()`
  （RegistryHive get_Hive（））
- `object get_InternalHandle()`
  （object get_内部的句柄（））
- `void AssertKeyStillValid()`
  （void Assert键StillValid（））
- `void AssertKeyNameLength(string name)`
  （void Assert键名称Length（string name））
- `string DecodeString(byte[] data)`
  （string Decode字符串（byte[] data））
- `IOException CreateMarkedForDeletionException()`
  （IOException 创建MarkedForDeletionException（））
- `string GetHiveName(RegistryHive hive)`
  （string 获取Hive名称（RegistryHive hive））

---

## RegistryKeyComparer（Registry键Comparer）

**继承**: IEqualityComparer（IEqualityComparer）

### 方法 (2)

- `bool Equals(object x, object y)`
  （bool Equals（object x, object y））
- `int GetHashCode(object obj)`
  （整数 获取哈希码（对象 obj））

---

## RegistryValueKind（Registry值Kind）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RegistryValueOptions（Registry值Options）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RelevantGraphSurface（RelevantGraphSurface）

**继承**: VersionedMonoBehaviour（版本化MonoBehaviour）

### 字段 (5)

- `RelevantGraphSurface root`（RelevantGraphSurface root）(偏移: 0x0)
- `float maxRange`（float max范围）(偏移: 0x10)
- `RelevantGraphSurface prev`（RelevantGraphSurface prev）(偏移: 0x14)
- `RelevantGraphSurface next`（RelevantGraphSurface next）(偏移: 0x18)
- `Vector3 position`（三维向量 位置）(偏移: 0x1C)

### 方法 (11)

- `Vector3 get_Position()`
  （三维向量 get_Position（））
- `RelevantGraphSurface get_Next()`
  （RelevantGraphSurface get_下一个（））
- `RelevantGraphSurface get_Prev()`
  （RelevantGraphSurface get_Prev（））
- `RelevantGraphSurface get_Root()`
  （RelevantGraphSurface get_根（））
- `void UpdatePosition()`
  （void 更新Position（））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `void UpdateAllPositions()`
  （void 更新所有Positions（））
- `void FindAllGraphSurfaces()`
  （void 查找所有GraphSurfaces（））
- `void OnDrawGizmos()`
  （void 绘制辅助线时（））
- `void OnDrawGizmosSelected()`
  （void 绘制选中辅助线时（））

---

## ReliabilityContractAttribute（ReliabilityContractAttribute）

**继承**: Attribute（属性）

### 字段 (2)

- `Consistency _consistency`（Consistency _consistency）(偏移: 0x8)
- `Cer _cer`（Cer _cer）(偏移: 0xC)

---

## ReloadAttribute.Package（换弹Attribute.Package）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RemoteConfigSettings（Remote配置Settings）

### 字段 (2)

- `IntPtr m_Ptr`（整数指针 m_指针）(偏移: 0x8)
- `Action<bool> Updated`（Action<bool> Updated）(偏移: 0xC)

### 方法 (1)

- `void RemoteConfigSettingsUpdated(RemoteConfigSettings rcs, bool wasLastUpdatedFromServer)`
  （void Remote配置SettingsUpdated（Remote配置Settings rcs, bool wasLastUpdatedFromServer））

---

## RemoteConfigSettingsHelper.Tag（Remote配置SettingsHelper.标签）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RemoteSettings（RemoteSettings）

### 字段 (2)

- `RemoteSettings.UpdatedEventHandler Updated`（RemoteSettings.Updated事件处理器 Updated）(偏移: 0x0)
- `Action BeforeFetchFromServer`（动作 BeforeFetchFrom服务器）(偏移: 0x4)

### 方法 (3)

- `void RemoteSettingsUpdated(bool wasLastUpdatedFromServer)`
  （void RemoteSettingsUpdated（bool wasLastUpdatedFromServer））
- `void RemoteSettingsBeforeFetchFromServer()`
  （void RemoteSettingsBeforeFetchFrom服务器（））
- `void RemoteSettingsUpdateCompleted(bool wasLastUpdatedFromServer, bool settingsChanged, int response)`
  （void RemoteSettings更新Completed（bool wasLastUpdatedFromServer, bool settingsChanged, int response））

---

## RemoteSettings.UpdatedEventHandler（RemoteSettings.Updated事件处理器）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke()`
  （void 调用（））
- `IAsyncResult BeginInvoke(AsyncCallback callback, object object)`
  （I异步结果 开始调用（异步回调 callback, 对象 object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## RemotingConfiguration（RemotingConfiguration）

### 字段 (13)

- `string applicationID`（string applicationID）(偏移: 0x0)
- `string applicationName`（string application名称）(偏移: 0x4)
- `string processGuid`（string processGuid）(偏移: 0x8)
- `bool defaultConfigRead`（bool default配置Read）(偏移: 0xC)
- `bool defaultDelayedConfigRead`（bool defaultDelayed配置Read）(偏移: 0xD)
- `string _errorMode`（string _error模式）(偏移: 0x10)
- `Hashtable wellKnownClientEntries`（Hashtable wellKnown客户端Entries）(偏移: 0x14)
- `Hashtable activatedClientEntries`（Hashtable activated客户端Entries）(偏移: 0x18)
- `Hashtable wellKnownServiceEntries`（Hashtable wellKnown服务Entries）(偏移: 0x1C)
- `Hashtable activatedServiceEntries`（Hashtable activated服务Entries）(偏移: 0x20)
- `Hashtable channelTemplates`（Hashtable channelTemplates）(偏移: 0x24)
- `Hashtable clientProviderTemplates`（Hashtable client提供者Templates）(偏移: 0x28)
- `Hashtable serverProviderTemplates`（Hashtable server提供者Templates）(偏移: 0x2C)

### 方法 (17)

- `string get_ApplicationName()`
  （string get_Application名称（））
- `void set_ApplicationName(string value)`
  （void set_Application名称（string value））
- `string get_ProcessId()`
  （string get_处理Id（））
- `void LoadDefaultDelayedChannels()`
  （void 加载默认的DelayedChannels（））
- `ActivatedClientTypeEntry IsRemotelyActivatedClientType(Type svrType)`
  （Activated客户端类型Entry 是否RemotelyActivated客户端类型（类型 svrType））
- `WellKnownClientTypeEntry IsWellKnownClientType(Type svrType)`
  （WellKnown客户端类型Entry 是否WellKnown客户端类型（类型 svrType））
- `void RegisterActivatedClientType(ActivatedClientTypeEntry entry)`
  （void RegisterActivated客户端类型（Activated客户端类型Entry entry））
- `void RegisterActivatedServiceType(ActivatedServiceTypeEntry entry)`
  （void RegisterActivated服务类型（Activated服务类型Entry entry））
- `void RegisterWellKnownClientType(WellKnownClientTypeEntry entry)`
  （void RegisterWellKnown客户端类型（WellKnown客户端类型Entry entry））
- `void RegisterWellKnownServiceType(WellKnownServiceTypeEntry entry)`
  （void RegisterWellKnown服务类型（WellKnown服务类型Entry entry））
- `void RegisterChannelTemplate(ChannelData channel)`
  （void RegisterChannelTemplate（Channel数据 channel））
- `void RegisterClientProviderTemplate(ProviderData prov)`
  （void Register客户端提供者Template（提供者数据 prov））
- `void RegisterServerProviderTemplate(ProviderData prov)`
  （void Register服务器提供者Template（提供者数据 prov））
- `void RegisterChannels(ArrayList channels, bool onlyDelayed)`
  （void RegisterChannels（数组列表 channels, bool onlyDelayed））
- `void RegisterTypes(ArrayList types)`
  （void RegisterTypes（数组列表 types））
- `bool CustomErrorsEnabled(bool isLocalRequest)`
  （bool 自定义的Errors启用的（bool isLocalRequest））
- `void SetCustomErrorsMode(string mode)`
  （void 集合自定义的Errors模式（string mode））

---

## RemotingProxy（Remoting代理）

**继承**: RealProxy, IRemotingTypeInfo（Real代理, IRemoting类型信息）

### 字段 (5)

- `MethodInfo _cache_GetTypeMethod`（Method信息 _cache_获取类型Method）(偏移: 0x0)
- `MethodInfo _cache_GetHashCodeMethod`（Method信息 _cache_获取HashCodeMethod）(偏移: 0x4)
- `IMessageSink _sink`（IMessageSink _sink）(偏移: 0x28)
- `bool _hasEnvoySink`（bool _hasEnvoySink）(偏移: 0x2C)
- `ConstructionCall _ctorCall`（ConstructionCall _ctorCall）(偏移: 0x30)

### 方法 (6)

- `IMessage Invoke(IMessage request)`
  （IMessage Invoke（IMessage request））
- `void AttachIdentity(Identity identity)`
  （void AttachIdentity（Identity identity））
- `IMessage ActivateRemoteObject(IMethodMessage request)`
  （IMessage 激活Remote对象（IMethodMessage request））
- `string get_TypeName()`
  （字符串 获取_类型名称（））
- `bool CanCastTo(Type fromType, object o)`
  （bool 能否CastTo（类型 fromType, object o））
- `void Finalize()`
  （void 终结（））

---

## RemotingServices（RemotingServices）

### 字段 (8)

- `Hashtable uri_hash`（Hashtable uri_hash）(偏移: 0x0)
- `BinaryFormatter _serializationFormatter`（BinaryFormatter _serializationFormatter）(偏移: 0x4)
- `BinaryFormatter _deserializationFormatter`（BinaryFormatter _deserializationFormatter）(偏移: 0x8)
- `string app_id`（string app_id）(偏移: 0xC)
- `object app_id_lock`（object app_id_lock）(偏移: 0x10)
- `int next_id`（int next_id）(偏移: 0x14)
- `MethodInfo FieldSetterMethod`（Method信息 FieldSetterMethod）(偏移: 0x18)
- `MethodInfo FieldGetterMethod`（Method信息 FieldGetterMethod）(偏移: 0x1C)

### 方法 (41)

- `object InternalExecute(MethodBase method, object obj, object[] parameters, out object[] out_args)`
  （object 内部的执行（Method基础 method, object obj, object[] parameters, out object[] out_args））
- `MethodBase GetVirtualMethod(Type type, MethodBase method)`
  （Method基础 获取虚拟的Method（类型 type, Method基础 method））
- `bool IsTransparentProxy(object proxy)`
  （bool 是否透明的代理（object proxy））
- `IMethodReturnMessage InternalExecuteMessage(MarshalByRefObject target, IMethodCallMessage reqMsg)`
  （IMethodReturnMessage 内部的执行Message（MarshalByRef对象 target, IMethodCallMessage reqMsg））
- `object Connect(Type classToProxy, string url)`
  （object Connect（类型 classToProxy, string url））
- `object Connect(Type classToProxy, string url, object data)`
  （object Connect（类型 classToProxy, string url, object data））
- `Type GetServerTypeForUri(string URI)`
  （类型 获取服务器类型ForUri（string URI））
- `object Unmarshal(ObjRef objectRef)`
  （object Unmarshal（ObjRef objectRef））
- `object Unmarshal(ObjRef objectRef, bool fRefine)`
  （object Unmarshal（ObjRef objectRef, bool fRefine））
- `ObjRef Marshal(MarshalByRefObject Obj)`
  （ObjRef Marshal（MarshalByRef对象 Obj））
- `ObjRef Marshal(MarshalByRefObject Obj, string ObjURI, Type RequestedType)`
  （ObjRef Marshal（MarshalByRef对象 Obj, string ObjURI, 类型 RequestedType））
- `string NewUri()`
  （string 新的Uri（））
- `RealProxy GetRealProxy(object proxy)`
  （Real代理 获取Real代理（object proxy））
- `MethodBase GetMethodBaseFromMethodMessage(IMethodMessage msg)`
  （Method基础 获取Method基础FromMethodMessage（IMethodMessage msg））
- `MethodBase GetMethodBaseFromName(Type type, string methodName, Type[] signature)`
  （Method基础 获取Method基础From名称（类型 type, string methodName, Type[] signature））
- `MethodBase FindInterfaceMethod(Type type, string methodName, Type[] signature)`
  （Method基础 查找InterfaceMethod（类型 type, string methodName, Type[] signature））
- `void GetObjectData(object obj, SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（object obj, Serialization信息 info, StreamingContext context））
- `bool IsOneWay(MethodBase method)`
  （bool 是否OneWay（Method基础 method））
- `object CreateClientProxy(ActivatedClientTypeEntry entry, object[] activationAttributes)`
  （object 创建客户端代理（Activated客户端类型Entry entry, object[] activationAttributes））
- `object CreateClientProxy(Type objectType, string url, object[] activationAttributes)`
  （object 创建客户端代理（类型 objectType, string url, object[] activationAttributes））
- `object CreateClientProxy(WellKnownClientTypeEntry entry)`
  （object 创建客户端代理（WellKnown客户端类型Entry entry））
- `object CreateClientProxyForContextBound(Type type, object[] activationAttributes)`
  （object 创建客户端代理ForContextBound（类型 type, object[] activationAttributes））
- `Identity GetIdentityForUri(string uri)`
  （Identity 获取IdentityForUri（string uri））
- `string RemoveAppNameFromUri(string uri)`
  （string 移除App名称FromUri（string uri））
- `ClientIdentity GetOrCreateClientIdentity(ObjRef objRef, Type proxyType, out object clientProxy)`
  （客户端Identity 获取Or创建客户端Identity（ObjRef objRef, 类型 proxyType, out object clientProxy））
- `IMessageSink GetClientChannelSinkChain(string url, object channelData, out string objectUri)`
  （IMessageSink 获取客户端ChannelSinkChain（string url, object channelData, out string objectUri））
- `ClientActivatedIdentity CreateContextBoundObjectIdentity(Type objectType)`
  （客户端ActivatedIdentity 创建ContextBound对象Identity（类型 objectType））
- `ClientActivatedIdentity CreateClientActivatedServerIdentity(MarshalByRefObject realObject, Type objectType, string objectUri)`
  （客户端ActivatedIdentity 创建客户端Activated服务器Identity（MarshalByRef对象 realObject, 类型 objectType, string objectUri））
- `ServerIdentity CreateWellKnownServerIdentity(Type objectType, string objectUri, WellKnownObjectMode mode)`
  （服务器Identity 创建WellKnown服务器Identity（类型 objectType, string objectUri, WellKnown对象模式 mode））
- `void RegisterServerIdentity(ServerIdentity identity)`
  （void Register服务器Identity（服务器Identity identity））
- `object GetProxyForRemoteObject(ObjRef objref, Type classToProxy)`
  （object 获取代理ForRemote对象（ObjRef objref, 类型 classToProxy））
- `object GetRemoteObject(ObjRef objRef, Type proxyType)`
  （object 获取Remote对象（ObjRef objRef, 类型 proxyType））
- `byte[] SerializeCallData(object obj)`
  （byte[] SerializeCall数据（object obj））
- `object DeserializeCallData(byte[] array)`
  （object DeserializeCall数据（byte[] array））
- `byte[] SerializeExceptionData(Exception ex)`
  （byte[] SerializeException数据（Exception ex））
- `void RegisterInternalChannels()`
  （void Register内部的Channels（））
- `void DisposeIdentity(Identity ident)`
  （void 释放Identity（Identity ident））
- `Identity GetMessageTargetIdentity(IMessage msg)`
  （Identity 获取Message目标Identity（IMessage msg））
- `void SetMessageTargetIdentity(IMessage msg, Identity ident)`
  （void 集合Message目标Identity（IMessage msg, Identity ident））
- `bool UpdateOutArgObject(ParameterInfo pi, object local, object remote)`
  （bool 更新OutArg对象（Parameter信息 pi, object local, object remote））
- `string GetNormalizedUri(string uri)`
  （string 获取NormalizedUri（string uri））

---

## RemotingServices.CACD（RemotingServices.CACD）

### 字段 (2)

- `object d`（object d）(偏移: 0x8)
- `object c`（object c）(偏移: 0xC)

---

## RemotingSurrogate（RemotingSurrogate）

**继承**: ISerializationSurrogate（ISerializationSurrogate）

### 方法 (2)

- `void GetObjectData(object obj, SerializationInfo si, StreamingContext sc)`
  （void 获取对象数据（object obj, Serialization信息 si, StreamingContext sc））
- `object SetObjectData(object obj, SerializationInfo si, StreamingContext sc, ISurrogateSelector selector)`
  （object 集合对象数据（object obj, Serialization信息 si, StreamingContext sc, ISurrogateSelector selector））

---

## RemotingSurrogateSelector（RemotingSurrogateSelector）

**继承**: ISurrogateSelector（ISurrogateSelector）

### 字段 (4)

- `Type s_cachedTypeObjRef`（类型 s_cached类型ObjRef）(偏移: 0x0)
- `ObjRefSurrogate _objRefSurrogate`（ObjRefSurrogate _objRefSurrogate）(偏移: 0x4)
- `RemotingSurrogate _objRemotingSurrogate`（RemotingSurrogate _objRemotingSurrogate）(偏移: 0x8)
- `ISurrogateSelector _next`（ISurrogateSelector _next）(偏移: 0x8)

### 方法 (1)

- `ISerializationSurrogate GetSurrogate(Type type, StreamingContext context, out ISurrogateSelector ssout)`
  （ISerializationSurrogate 获取Surrogate（类型 type, StreamingContext context, out ISurrogateSelector ssout））

---

## Render2DLightingPass（Render2DLightingPass）

**继承**: ScriptableRenderPass, IRenderPass2D（ScriptableRenderPass, IRenderPass2D）

### 字段 (16)

- `int k_HDREmulationScaleID`（int k_HDREmulation缩放ID）(偏移: 0x0)
- `int k_InverseHDREmulationScaleID`（int k_InverseHDREmulation缩放ID）(偏移: 0x4)
- `int k_UseSceneLightingID`（int k_Use场景LightingID）(偏移: 0x8)
- `int k_RendererColorID`（int k_渲染器颜色ID）(偏移: 0xC)
- `int k_ShapeLightTexture0ID`（int k_Shape光照Texture0ID）(偏移: 0x10)
- `int k_ShapeLightTexture1ID`（int k_Shape光照Texture1ID）(偏移: 0x14)
- `int k_ShapeLightTexture2ID`（int k_Shape光照Texture2ID）(偏移: 0x18)
- `int k_ShapeLightTexture3ID`（int k_Shape光照Texture3ID）(偏移: 0x1C)
- `ShaderTagId k_CombinedRenderingPassNameOld`（着色器标签Id k_CombinedRenderingPass名称旧的）(偏移: 0x20)
- `ShaderTagId k_CombinedRenderingPassName`（着色器标签Id k_CombinedRenderingPass名称）(偏移: 0x24)
- `ShaderTagId k_NormalsRenderingPassName`（着色器标签Id k_NormalsRenderingPass名称）(偏移: 0x28)
- `ShaderTagId k_LegacyPassName`（着色器标签Id k_LegacyPass名称）(偏移: 0x2C)
- `List<ShaderTagId> k_ShaderTags`（List<着色器标签Id> k_着色器Tags）(偏移: 0x30)
- `ProfilingSampler m_ProfilingSampler`（性能分析采样器 m_性能分析采样器）(偏移: 0x34)
- `ProfilingSampler m_ProfilingSamplerUnlit`（ProfilingSampler m_ProfilingSamplerUnlit）(偏移: 0x38)
- `Renderer2DData m_Renderer2DData`（Renderer2D数据 m_Renderer2D数据）(偏移: 0x54)

### 方法 (4)

- `void GetTransparencySortingMode(Camera camera, ref SortingSettings sortingSettings)`
  （void 获取TransparencySorting模式（摄像机 camera, ref SortingSettings sortingSettings））
- `bool CompareLightsInLayer(int layerIndex1, int layerIndex2, SortingLayer[] sortingLayers)`
  （bool CompareLightsIn层（int layerIndex1, int layerIndex2, SortingLayer[] sortingLayers））
- `int FindUpperBoundInBatch(int startLayerIndex, SortingLayer[] sortingLayers)`
  （int 查找上半身BoundInBatch（int startLayerIndex, SortingLayer[] sortingLayers））
- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（可脚本化渲染上下文 context, 引用 渲染数据 renderingData））

---

## RenderBufferLoadAction（Render缓冲区加载动作）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RenderBufferStoreAction（Render缓冲区商店动作）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RenderGraph（RenderGraph）

### 字段 (21)

- `int kMaxMRTCount`（int k最大MRT数量）(偏移: 0x0)
- `RenderGraphResourceRegistry m_Resources`（RenderGraph资源Registry m_Resources）(偏移: 0x8)
- `RenderGraphObjectPool m_RenderGraphPool`（RenderGraph对象池 m_RenderGraph池）(偏移: 0xC)
- `List<RenderGraphPass> m_RenderPasses`（List<RenderGraphPass> m_RenderPasses）(偏移: 0x10)
- `List<RendererListHandle> m_RendererLists`（List<渲染器列表Handle> m_渲染器Lists）(偏移: 0x14)
- `RenderGraphDebugParams m_DebugParameters`（RenderGraphDebugParams m_DebugParameters）(偏移: 0x18)
- `RenderGraphLogger m_Logger`（RenderGraphLogger m_Logger）(偏移: 0x1C)
- `RenderGraphDefaultResources m_DefaultResources`（RenderGraph默认的Resources m_默认的Resources）(偏移: 0x20)
- `bool m_ExecutionExceptionWasRaised`（bool m_ExecutionExceptionWasRaised）(偏移: 0x28)
- `RenderGraphContext m_RenderGraphContext`（RenderGraphContext m_RenderGraphContext）(偏移: 0x2C)
- `CommandBuffer m_PreviousCommandBuffer`（Command缓冲区 m_上一个Command缓冲区）(偏移: 0x30)
- `int m_CurrentImmediatePassIndex`（int m_当前ImmediatePass索引）(偏移: 0x34)
- `List<int>[] m_ImmediateModeResourceList`（List<int>[] m_Immediate模式资源列表）(偏移: 0x38)
- `DynamicArray<RenderGraph.CompiledResourceInfo>[] m_CompiledResourcesInfos`（动态的Array<RenderGraph.Compiled资源Info>[] m_CompiledResourcesInfos）(偏移: 0x3C)
- `DynamicArray<RenderGraph.CompiledPassInfo> m_CompiledPassInfos`（动态的Array<RenderGraph.CompiledPassInfo> m_CompiledPassInfos）(偏移: 0x40)
- `Stack<int> m_CullingStack`（Stack<int> m_Culling栈）(偏移: 0x44)
- `int m_ExecutionCount`（int m_Execution数量）(偏移: 0x48)
- `RenderGraphDebugData m_RenderGraphDebugData`（RenderGraphDebug数据 m_RenderGraphDebug数据）(偏移: 0x4C)
- `List<RenderGraph> s_RegisteredGraphs`（List<RenderGraph> s_RegisteredGraphs）(偏移: 0x4)
- `RenderGraph.OnGraphRegisteredDelegate onGraphRegistered`（RenderGraph.OnGraphRegistered委托 onGraphRegistered）(偏移: 0xC)
- `RenderGraph.OnGraphRegisteredDelegate onGraphUnregistered`（RenderGraph.OnGraphRegistered委托 onGraphUnregistered）(偏移: 0x10)

### 方法 (60)

- `string get_name()`
  （字符串 获取_名称（））
- `void set_name(string value)`
  （void 设置_名称（字符串 value））
- `bool get_requireDebugData()`
  （bool get_requireDebug数据（））
- `void set_requireDebugData(bool value)`
  （void set_requireDebug数据（bool value））
- `RenderGraphDefaultResources get_defaultResources()`
  （RenderGraph默认的Resources get_defaultResources（））
- `void Cleanup()`
  （void 清理（））
- `RenderGraphDebugData GetDebugData()`
  （RenderGraphDebug数据 获取Debug数据（））
- `void EndFrame()`
  （void 结束Frame（））
- `TextureHandle ImportTexture(RTHandle rt)`
  （纹理句柄 Import纹理（RT句柄 rt））
- `TextureHandle ImportBackbuffer(RenderTargetIdentifier rt)`
  （纹理句柄 ImportBackbuffer（Render目标Identifier rt））
- `TextureHandle CreateTexture(in TextureDesc desc)`
  （纹理句柄 创建纹理（in TextureDesc desc））
- `TextureHandle CreateTexture(TextureHandle texture)`
  （纹理句柄 创建纹理（纹理句柄 texture））
- `void CreateTextureIfInvalid(in TextureDesc desc, ref TextureHandle texture)`
  （void 创建纹理IfInvalid（in TextureDesc desc, ref TextureHandle texture））
- `TextureDesc GetTextureDesc(TextureHandle texture)`
  （纹理Desc 获取纹理Desc（纹理句柄 texture））
- `RendererListHandle CreateRendererList(in RendererListDesc desc)`
  （渲染器列表句柄 创建渲染器列表（in RendererListDesc desc））
- `ComputeBufferHandle ImportComputeBuffer(ComputeBuffer computeBuffer)`
  （Compute缓冲区句柄 ImportCompute缓冲区（Compute缓冲区 computeBuffer））
- `ComputeBufferHandle CreateComputeBuffer(in ComputeBufferDesc desc)`
  （Compute缓冲区句柄 创建Compute缓冲区（in ComputeBufferDesc desc））
- `ComputeBufferHandle CreateComputeBuffer(in ComputeBufferHandle computeBuffer)`
  （Compute缓冲区句柄 创建Compute缓冲区（in ComputeBufferHandle computeBuffer））
- `ComputeBufferDesc GetComputeBufferDesc(in ComputeBufferHandle computeBuffer)`
  （Compute缓冲区Desc 获取Compute缓冲区Desc（in ComputeBufferHandle computeBuffer））
- `void Begin(in RenderGraphParameters parameters)`
  （void Begin（in RenderGraphParameters parameters））
- `void Execute()`
  （void 执行（））
- `void BeginProfilingSampler(ProfilingSampler sampler)`
  （void BeginProfilingSampler（ProfilingSampler sampler））
- `void EndProfilingSampler(ProfilingSampler sampler)`
  （void 结束ProfilingSampler（ProfilingSampler sampler））
- `List<RenderGraph> GetRegisteredRenderGraphs()`
  （List<RenderGraph> 获取RegisteredRenderGraphs（））
- `DynamicArray<RenderGraph.CompiledPassInfo> GetCompiledPassInfos()`
  （动态的Array<RenderGraph.CompiledPassInfo> 获取CompiledPassInfos（））
- `void ClearCompiledGraph()`
  （void 清除CompiledGraph（））
- `void InvalidateContext()`
  （void InvalidateContext（））
- `void OnPassAdded(RenderGraphPass pass)`
  （void OnPassAdded（RenderGraphPass pass））
- `void add_onGraphRegistered(RenderGraph.OnGraphRegisteredDelegate value)`
  （void add_onGraphRegistered（RenderGraph.OnGraphRegistered委托 value））
- `void remove_onGraphRegistered(RenderGraph.OnGraphRegisteredDelegate value)`
  （void remove_onGraphRegistered（RenderGraph.OnGraphRegistered委托 value））
- `void add_onGraphUnregistered(RenderGraph.OnGraphRegisteredDelegate value)`
  （void add_onGraphUnregistered（RenderGraph.OnGraphRegistered委托 value））
- `void remove_onGraphUnregistered(RenderGraph.OnGraphRegisteredDelegate value)`
  （void remove_onGraphUnregistered（RenderGraph.OnGraphRegistered委托 value））
- `void InitResourceInfosData(DynamicArray<RenderGraph.CompiledResourceInfo> resourceInfos, int count)`
  （void 初始化资源Infos数据（动态的Array<RenderGraph.Compiled资源Info> resourceInfos, int count））
- `void InitializeCompilationData()`
  （void 初始化Compilation数据（））
- `void CountReferences()`
  （void 数量References（））
- `void CullOutputlessPasses()`
  （void CullOutputlessPasses（））
- `void CullUnusedPasses()`
  （void CullUnusedPasses（））
- `void UpdatePassSynchronization(ref RenderGraph.CompiledPassInfo currentPassInfo, ref RenderGraph.CompiledPassInfo producerPassInfo, int currentPassIndex, int lastProducer, ref int intLastSyncIndex)`
  （void 更新PassSynchronization（ref RenderGraph.CompiledPassInfo currentPassInfo, ref RenderGraph.CompiledPassInfo producerPassInfo, int currentPassIndex, int lastProducer, ref int intLastSyncIndex））
- `void UpdateResourceSynchronization(ref int lastGraphicsPipeSync, ref int lastComputePipeSync, int currentPassIndex, in RenderGraph.CompiledResourceInfo resource)`
  （void 更新资源Synchronization（ref int lastGraphicsPipeSync, ref int lastComputePipeSync, int currentPassIndex, in RenderGraph.CompiledResourceInfo resource））
- `int GetLatestProducerIndex(int passIndex, in RenderGraph.CompiledResourceInfo info)`
  （int 获取LatestProducer索引（int passIndex, in RenderGraph.CompiledResourceInfo info））
- `int GetLatestValidReadIndex(in RenderGraph.CompiledResourceInfo info)`
  （int 获取LatestValidRead索引（in RenderGraph.CompiledResourceInfo info））
- `int GetFirstValidWriteIndex(in RenderGraph.CompiledResourceInfo info)`
  （int 获取第一个ValidWrite索引（in RenderGraph.CompiledResourceInfo info））
- `int GetLatestValidWriteIndex(in RenderGraph.CompiledResourceInfo info)`
  （int 获取LatestValidWrite索引（in RenderGraph.CompiledResourceInfo info））
- `void UpdateResourceAllocationAndSynchronization()`
  （void 更新资源AllocationAndSynchronization（））
- `void CompileRenderGraph()`
  （void CompileRenderGraph（））
- `void ExecutePassImmediatly(RenderGraphPass pass)`
  （void 执行PassImmediatly（RenderGraphPass pass））
- `void ExecuteCompiledPass(ref RenderGraph.CompiledPassInfo passInfo, int passIndex)`
  （void 执行CompiledPass（ref RenderGraph.CompiledPassInfo passInfo, int passIndex））
- `void ExecuteRenderGraph()`
  （void 执行RenderGraph（））
- `void PreRenderPassSetRenderTargets(in RenderGraph.CompiledPassInfo passInfo, RenderGraphContext rgContext)`
  （void PreRenderPass集合RenderTargets（in RenderGraph.CompiledPassInfo passInfo, RenderGraphContext rgContext））
- `void PreRenderPassExecute(in RenderGraph.CompiledPassInfo passInfo, RenderGraphContext rgContext)`
  （void PreRenderPass执行（in RenderGraph.CompiledPassInfo passInfo, RenderGraphContext rgContext））
- `void PostRenderPassExecute(ref RenderGraph.CompiledPassInfo passInfo, RenderGraphContext rgContext)`
  （void PostRenderPass执行（ref RenderGraph.CompiledPassInfo passInfo, RenderGraphContext rgContext））
- `void ClearRenderPasses()`
  （void 清除RenderPasses（））
- `void ReleaseImmediateModeResources()`
  （void ReleaseImmediate模式Resources（））
- `void LogFrameInformation()`
  （void LogFrameInformation（））
- `void LogRendererListsCreation()`
  （void Log渲染器ListsCreation（））
- `void LogRenderPassBegin(in RenderGraph.CompiledPassInfo passInfo)`
  （void LogRenderPassBegin（in RenderGraph.CompiledPassInfo passInfo））
- `void LogCulledPasses()`
  （void LogCulledPasses（））
- `ProfilingSampler GetDefaultProfilingSampler(string name)`
  （ProfilingSampler 获取默认的ProfilingSampler（string name））
- `void UpdateImportedResourceLifeTime(ref RenderGraphDebugData.ResourceDebugData data, List<int> passList)`
  （void 更新Imported资源Life时间（ref RenderGraphDebugData.ResourceDebugData data, List<int> passList））
- `void GenerateDebugData()`
  （void GenerateDebug数据（））

---

## RenderGraph.CompiledPassInfo（RenderGraph.CompiledPass信息）

### 字段 (11)

- `RenderGraphPass pass`（RenderGraphPass pass）(偏移: 0x0)
- `List<int>[] resourceCreateList`（List<int>[] resource创建列表）(偏移: 0x4)
- `List<int>[] resourceReleaseList`（List<int>[] resourceRelease列表）(偏移: 0x8)
- `int refCount`（int ref数量）(偏移: 0xC)
- `bool culled`（bool culled）(偏移: 0x10)
- `bool hasSideEffect`（bool has侧面特效）(偏移: 0x11)
- `int syncToPassIndex`（int syncToPass索引）(偏移: 0x14)
- `int syncFromPassIndex`（int syncFromPass索引）(偏移: 0x18)
- `bool needGraphicsFence`（bool needGraphicsFence）(偏移: 0x1C)
- `GraphicsFence fence`（GraphicsFence fence）(偏移: 0x20)
- `bool enableAsyncCompute`（bool enable异步Compute）(偏移: 0x2C)

### 方法 (2)

- `bool get_allowPassCulling()`
  （bool get_allowPassCulling（））
- `void Reset(RenderGraphPass pass)`
  （void 重置（RenderGraphPass pass））

---

## RenderGraph.CompiledResourceInfo（RenderGraph.Compiled资源信息）

### 字段 (4)

- `List<int> producers`（List<int> producers）(偏移: 0x0)
- `List<int> consumers`（List<int> consumers）(偏移: 0x4)
- `bool resourceCreated`（bool resourceCreated）(偏移: 0x8)
- `int refCount`（int ref数量）(偏移: 0xC)

### 方法 (1)

- `void Reset()`
  （void 重置（））

---

## RenderGraph.OnGraphRegisteredDelegate（RenderGraph.OnGraphRegistered委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(RenderGraph graph)`
  （void Invoke（RenderGraph graph））
- `IAsyncResult BeginInvoke(RenderGraph graph, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（RenderGraph graph, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## RenderGraph.ProfilingScopePassData（RenderGraph.Profiling瞄准镜Pass数据）

### 字段 (1)

- `ProfilingSampler sampler`（ProfilingSampler sampler）(偏移: 0x8)

---

## RenderGraphBuilder（RenderGraph构建器）

**继承**: IDisposable（可释放接口）

### 字段 (4)

- `RenderGraphPass m_RenderPass`（RenderGraphPass m_RenderPass）(偏移: 0x0)
- `RenderGraphResourceRegistry m_Resources`（RenderGraph资源Registry m_Resources）(偏移: 0x4)
- `RenderGraph m_RenderGraph`（RenderGraph m_RenderGraph）(偏移: 0x8)
- `bool m_Disposed`（布尔值 m_已释放）(偏移: 0xC)

### 方法 (18)

- `TextureHandle UseColorBuffer(in TextureHandle input, int index)`
  （纹理句柄 Use颜色缓冲区（in TextureHandle input, int index））
- `TextureHandle UseDepthBuffer(in TextureHandle input, DepthAccess flags)`
  （纹理句柄 Use深度缓冲区（in TextureHandle input, 深度Access flags））
- `TextureHandle ReadTexture(in TextureHandle input)`
  （纹理句柄 Read纹理（in TextureHandle input））
- `TextureHandle WriteTexture(in TextureHandle input)`
  （纹理句柄 Write纹理（in TextureHandle input））
- `TextureHandle ReadWriteTexture(in TextureHandle input)`
  （纹理句柄 ReadWrite纹理（in TextureHandle input））
- `TextureHandle CreateTransientTexture(in TextureDesc desc)`
  （纹理句柄 创建Transient纹理（in TextureDesc desc））
- `TextureHandle CreateTransientTexture(in TextureHandle texture)`
  （纹理句柄 创建Transient纹理（in TextureHandle texture））
- `RendererListHandle UseRendererList(in RendererListHandle input)`
  （渲染器列表句柄 Use渲染器列表（in RendererListHandle input））
- `ComputeBufferHandle ReadComputeBuffer(in ComputeBufferHandle input)`
  （Compute缓冲区句柄 ReadCompute缓冲区（in ComputeBufferHandle input））
- `ComputeBufferHandle WriteComputeBuffer(in ComputeBufferHandle input)`
  （Compute缓冲区句柄 WriteCompute缓冲区（in ComputeBufferHandle input））
- `ComputeBufferHandle CreateTransientComputeBuffer(in ComputeBufferDesc desc)`
  （Compute缓冲区句柄 创建TransientCompute缓冲区（in ComputeBufferDesc desc））
- `ComputeBufferHandle CreateTransientComputeBuffer(in ComputeBufferHandle computebuffer)`
  （Compute缓冲区句柄 创建TransientCompute缓冲区（in ComputeBufferHandle computebuffer））
- `void EnableAsyncCompute(bool value)`
  （void 启用异步Compute（bool value））
- `void AllowPassCulling(bool value)`
  （void 允许PassCulling（bool value））
- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `void CheckResource(in ResourceHandle res)`
  （void 检查资源（in ResourceHandle res））
- `void GenerateDebugData(bool value)`
  （void GenerateDebug数据（bool value））

---

## RenderGraphContext（RenderGraphContext）

### 字段 (4)

- `ScriptableRenderContext renderContext`（ScriptableRenderContext renderContext）(偏移: 0x8)
- `CommandBuffer cmd`（Command缓冲区 cmd）(偏移: 0xC)
- `RenderGraphObjectPool renderGraphPool`（RenderGraph对象池 renderGraph池）(偏移: 0x10)
- `RenderGraphDefaultResources defaultResources`（RenderGraph默认的Resources defaultResources）(偏移: 0x14)

---

## RenderGraphDebugData（RenderGraphDebug数据）

### 字段 (2)

- `List<RenderGraphDebugData.PassDebugData> passList`（List<RenderGraphDebugData.PassDebugData> pass列表）(偏移: 0x8)
- `List<RenderGraphDebugData.ResourceDebugData>[] resourceLists`（List<RenderGraphDebugData.资源DebugData>[] resourceLists）(偏移: 0xC)

### 方法 (1)

- `void Clear()`
  （void 清除（））

---

## RenderGraphDebugData.PassDebugData（RenderGraphDebugData.PassDebug数据）

### 字段 (5)

- `string name`（字符串 名称）(偏移: 0x0)
- `List<int>[] resourceReadLists`（List<int>[] resourceReadLists）(偏移: 0x4)
- `List<int>[] resourceWriteLists`（List<int>[] resourceWriteLists）(偏移: 0x8)
- `bool culled`（bool culled）(偏移: 0xC)
- `bool generateDebugData`（bool generateDebug数据）(偏移: 0xD)

---

## RenderGraphDebugData.ResourceDebugData（RenderGraphDebugData.资源Debug数据）

### 字段 (6)

- `string name`（字符串 名称）(偏移: 0x0)
- `bool imported`（bool imported）(偏移: 0x4)
- `int creationPassIndex`（int creationPass索引）(偏移: 0x8)
- `int releasePassIndex`（int releasePass索引）(偏移: 0xC)
- `List<int> consumerList`（List<int> consumer列表）(偏移: 0x10)
- `List<int> producerList`（List<int> producer列表）(偏移: 0x14)

---

## RenderGraphDebugParams（RenderGraphDebugParams）

### 字段 (6)

- `bool clearRenderTargetsAtCreation`（bool clearRenderTargetsAtCreation）(偏移: 0x8)
- `bool clearRenderTargetsAtRelease`（bool clearRenderTargetsAtRelease）(偏移: 0x9)
- `bool disablePassCulling`（bool disablePassCulling）(偏移: 0xA)
- `bool immediateMode`（bool immediate模式）(偏移: 0xB)
- `bool logFrameInformation`（bool logFrameInformation）(偏移: 0xC)
- `bool logResources`（bool logResources）(偏移: 0xD)

### 方法 (2)

- `void RegisterDebug(string name)`
  （void RegisterDebug（string name））
- `void UnRegisterDebug(string name)`
  （void UnRegisterDebug（string name））

---

## RenderGraphDefaultResources（RenderGraph默认的Resources）

### 字段 (4)

- `bool m_IsValid`（bool m_是否Valid）(偏移: 0x8)
- `RTHandle m_BlackTexture2D`（RT句柄 m_BlackTexture2D）(偏移: 0xC)
- `RTHandle m_WhiteTexture2D`（RT句柄 m_WhiteTexture2D）(偏移: 0x10)
- `RTHandle m_ShadowTexture2D`（RT句柄 m_ShadowTexture2D）(偏移: 0x14)

### 方法 (22)

- `TextureHandle get_blackTexture()`
  （纹理句柄 get_black纹理（））
- `void set_blackTexture(TextureHandle value)`
  （void set_black纹理（纹理句柄 value））
- `TextureHandle get_whiteTexture()`
  （纹理句柄 get_white纹理（））
- `void set_whiteTexture(TextureHandle value)`
  （void set_white纹理（纹理句柄 value））
- `TextureHandle get_clearTextureXR()`
  （纹理句柄 get_clear纹理XR（））
- `void set_clearTextureXR(TextureHandle value)`
  （void set_clear纹理XR（纹理句柄 value））
- `TextureHandle get_magentaTextureXR()`
  （纹理句柄 get_magenta纹理XR（））
- `void set_magentaTextureXR(TextureHandle value)`
  （void set_magenta纹理XR（纹理句柄 value））
- `TextureHandle get_blackTextureXR()`
  （纹理句柄 get_black纹理XR（））
- `void set_blackTextureXR(TextureHandle value)`
  （void set_black纹理XR（纹理句柄 value））
- `TextureHandle get_blackTextureArrayXR()`
  （纹理句柄 get_black纹理数组XR（））
- `void set_blackTextureArrayXR(TextureHandle value)`
  （void set_black纹理数组XR（纹理句柄 value））
- `TextureHandle get_blackUIntTextureXR()`
  （纹理句柄 get_blackU整数纹理XR（））
- `void set_blackUIntTextureXR(TextureHandle value)`
  （void set_blackU整数纹理XR（纹理句柄 value））
- `TextureHandle get_blackTexture3DXR()`
  （纹理句柄 get_blackTexture3DXR（））
- `void set_blackTexture3DXR(TextureHandle value)`
  （void set_blackTexture3DXR（纹理句柄 value））
- `TextureHandle get_whiteTextureXR()`
  （纹理句柄 get_white纹理XR（））
- `void set_whiteTextureXR(TextureHandle value)`
  （void set_white纹理XR（纹理句柄 value））
- `TextureHandle get_defaultShadowTexture()`
  （纹理句柄 get_defaultShadow纹理（））
- `void set_defaultShadowTexture(TextureHandle value)`
  （void set_defaultShadow纹理（纹理句柄 value））
- `void Cleanup()`
  （void 清理（））
- `void InitializeForRendering(RenderGraph renderGraph)`
  （void 初始化ForRendering（RenderGraph renderGraph））

---

## RenderGraphLogIndent（RenderGraphLogIndent）

**继承**: IDisposable（可释放接口）

### 字段 (3)

- `int m_Indentation`（int m_Indentation）(偏移: 0x0)
- `RenderGraphLogger m_Logger`（RenderGraphLogger m_Logger）(偏移: 0x4)
- `bool m_Disposed`（布尔值 m_已释放）(偏移: 0x8)

### 方法 (2)

- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））

---

## RenderGraphLogger（RenderGraphLogger）

### 字段 (2)

- `StringBuilder m_Builder`（字符串构建器 m_构建器）(偏移: 0x8)
- `int m_CurrentIndentation`（int m_当前Indentation）(偏移: 0xC)

### 方法 (5)

- `void Initialize()`
  （void 初始化（））
- `void IncrementIndentation(int value)`
  （void IncrementIndentation（int value））
- `void DecrementIndentation(int value)`
  （void DecrementIndentation（int value））
- `void LogLine(string format, object[] args)`
  （void LogLine（string format, object[] args））
- `string GetLog()`
  （string 获取Log（））

---

## RenderGraphObjectPool（RenderGraph对象池）

### 字段 (1)

- `List<MaterialPropertyBlock> m_AllocatedMaterialPropertyBlocks`（List<材质属性Block> m_Allocated材质属性Blocks）(偏移: 0x10)

### 方法 (2)

- `MaterialPropertyBlock GetTempMaterialPropertyBlock()`
  （材质属性Block 获取Temp材质属性Block（））
- `void ReleaseAllTempAlloc()`
  （void Release所有TempAlloc（））

---

## RenderGraphParameters（RenderGraphParameters）

### 字段 (3)

- `int currentFrameIndex`（int currentFrame索引）(偏移: 0x0)
- `ScriptableRenderContext scriptableRenderContext`（ScriptableRenderContext scriptableRenderContext）(偏移: 0x4)
- `CommandBuffer commandBuffer`（Command缓冲区 command缓冲区）(偏移: 0x8)

---

## RenderGraphPass（RenderGraphPass）

### 字段 (4)

- `List<ResourceHandle>[] resourceReadLists`（List<资源Handle>[] resourceReadLists）(偏移: 0x30)
- `List<ResourceHandle>[] resourceWriteLists`（List<资源Handle>[] resourceWriteLists）(偏移: 0x34)
- `List<ResourceHandle>[] transientResourceList`（List<资源Handle>[] transient资源列表）(偏移: 0x38)
- `List<RendererListHandle> usedRendererListList`（List<渲染器列表Handle> used渲染器列表列表）(偏移: 0x3C)

### 方法 (30)

- `string get_name()`
  （字符串 获取_名称（））
- `void set_name(string value)`
  （void 设置_名称（字符串 value））
- `int get_index()`
  （int get_index（））
- `void set_index(int value)`
  （void set_index（int value））
- `ProfilingSampler get_customSampler()`
  （ProfilingSampler get_customSampler（））
- `void set_customSampler(ProfilingSampler value)`
  （void set_customSampler（ProfilingSampler value））
- `bool get_enableAsyncCompute()`
  （bool get_enable异步Compute（））
- `void set_enableAsyncCompute(bool value)`
  （void set_enable异步Compute（bool value））
- `bool get_allowPassCulling()`
  （bool get_allowPassCulling（））
- `void set_allowPassCulling(bool value)`
  （void set_allowPassCulling（bool value））
- `TextureHandle get_depthBuffer()`
  （纹理句柄 get_depth缓冲区（））
- `void set_depthBuffer(TextureHandle value)`
  （void set_depth缓冲区（纹理句柄 value））
- `TextureHandle[] get_colorBuffers()`
  （纹理Handle[] get_colorBuffers（））
- `void set_colorBuffers(TextureHandle[] value)`
  （void set_colorBuffers（纹理Handle[] value））
- `int get_colorBufferMaxIndex()`
  （int get_color缓冲区最大索引（））
- `void set_colorBufferMaxIndex(int value)`
  （void set_color缓冲区最大索引（int value））
- `int get_refCount()`
  （int get_ref数量（））
- `void set_refCount(int value)`
  （void set_ref数量（int value））
- `bool get_generateDebugData()`
  （bool get_generateDebug数据（））
- `void set_generateDebugData(bool value)`
  （void set_generateDebug数据（bool value））
- `void Clear()`
  （void 清除（））
- `void AddResourceWrite(in ResourceHandle res)`
  （void 添加资源Write（in ResourceHandle res））
- `void AddResourceRead(in ResourceHandle res)`
  （void 添加资源Read（in ResourceHandle res））
- `void AddTransientResource(in ResourceHandle res)`
  （void 添加Transient资源（in ResourceHandle res））
- `void UseRendererList(RendererListHandle rendererList)`
  （void Use渲染器列表（渲染器列表句柄 rendererList））
- `void EnableAsyncCompute(bool value)`
  （void 启用异步Compute（bool value））
- `void AllowPassCulling(bool value)`
  （void 允许PassCulling（bool value））
- `void GenerateDebugData(bool value)`
  （void GenerateDebug数据（bool value））
- `void SetColorBuffer(TextureHandle resource, int index)`
  （void 集合颜色缓冲区（纹理句柄 resource, int index））
- `void SetDepthBuffer(TextureHandle resource, DepthAccess flags)`
  （void 集合深度缓冲区（纹理句柄 resource, 深度Access flags））

---

## RenderGraphProfileId（RenderGraphProfileId）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RenderGraphProfilingScope（RenderGraphProfiling瞄准镜）

**继承**: IDisposable（可释放接口）

### 字段 (3)

- `bool m_Disposed`（布尔值 m_已释放）(偏移: 0x0)
- `ProfilingSampler m_Sampler`（ProfilingSampler m_Sampler）(偏移: 0x4)
- `RenderGraph m_RenderGraph`（RenderGraph m_RenderGraph）(偏移: 0x8)

### 方法 (2)

- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））

---

## RenderGraphResourceRegistry（RenderGraph资源Registry）

### 字段 (11)

- `ShaderTagId s_EmptyName`（着色器标签Id s_空名称）(偏移: 0x0)
- `RenderGraphResourceRegistry m_CurrentRegistry`（RenderGraph资源Registry m_当前Registry）(偏移: 0x4)
- `DynamicArray<RenderGraphResourceRegistry.IRenderGraphResource>[] m_Resources`（动态的Array<RenderGraph资源Registry.IRenderGraphResource>[] m_Resources）(偏移: 0x8)
- `TexturePool m_TexturePool`（纹理池 m_纹理池）(偏移: 0xC)
- `int m_TextureCreationIndex`（int m_纹理Creation索引）(偏移: 0x10)
- `ComputeBufferPool m_ComputeBufferPool`（Compute缓冲区池 m_Compute缓冲区池）(偏移: 0x14)
- `DynamicArray<RenderGraphResourceRegistry.RendererListResource> m_RendererListResources`（动态的Array<RenderGraph资源Registry.渲染器列表Resource> m_渲染器列表Resources）(偏移: 0x18)
- `RenderGraphDebugParams m_RenderGraphDebug`（RenderGraphDebugParams m_RenderGraphDebug）(偏移: 0x1C)
- `RenderGraphLogger m_Logger`（RenderGraphLogger m_Logger）(偏移: 0x20)
- `int m_CurrentFrameIndex`（int m_当前Frame索引）(偏移: 0x24)
- `RTHandle m_CurrentBackbuffer`（RT句柄 m_当前Backbuffer）(偏移: 0x28)

### 方法 (47)

- `RenderGraphResourceRegistry get_current()`
  （RenderGraph资源Registry get_current（））
- `void set_current(RenderGraphResourceRegistry value)`
  （void set_current（RenderGraph资源Registry value））
- `RTHandle GetTexture(in TextureHandle handle)`
  （RT句柄 获取纹理（in TextureHandle handle））
- `bool TextureNeedsFallback(in TextureHandle handle)`
  （bool 纹理NeedsFallback（in TextureHandle handle））
- `RendererList GetRendererList(in RendererListHandle handle)`
  （渲染器列表 获取渲染器列表（in RendererListHandle handle））
- `ComputeBuffer GetComputeBuffer(in ComputeBufferHandle handle)`
  （Compute缓冲区 获取Compute缓冲区（in ComputeBufferHandle handle））
- `void BeginRender(int currentFrameIndex, int executionCount)`
  （void BeginRender（int currentFrameIndex, int executionCount））
- `void EndRender()`
  （void 结束Render（））
- `void CheckHandleValidity(in ResourceHandle res)`
  （void 检查句柄Validity（in ResourceHandle res））
- `void CheckHandleValidity(RenderGraphResourceType type, int index)`
  （void 检查句柄Validity（RenderGraph资源类型 type, int index））
- `void IncrementWriteCount(in ResourceHandle res)`
  （void IncrementWrite数量（in ResourceHandle res））
- `string GetResourceName(in ResourceHandle res)`
  （string 获取资源名称（in ResourceHandle res））
- `string GetResourceName(RenderGraphResourceType type, int index)`
  （string 获取资源名称（RenderGraph资源类型 type, int index））
- `bool IsResourceImported(in ResourceHandle res)`
  （bool 是否资源Imported（in ResourceHandle res））
- `bool IsResourceCreated(in ResourceHandle res)`
  （bool 是否资源Created（in ResourceHandle res））
- `bool IsRendererListCreated(in RendererListHandle res)`
  （bool 是否渲染器列表Created（in RendererListHandle res））
- `bool IsResourceImported(RenderGraphResourceType type, int index)`
  （bool 是否资源Imported（RenderGraph资源类型 type, int index））
- `int GetResourceTransientIndex(in ResourceHandle res)`
  （int 获取资源Transient索引（in ResourceHandle res））
- `TextureHandle ImportTexture(RTHandle rt)`
  （纹理句柄 Import纹理（RT句柄 rt））
- `TextureHandle ImportBackbuffer(RenderTargetIdentifier rt)`
  （纹理句柄 ImportBackbuffer（Render目标Identifier rt））
- `TextureHandle CreateTexture(in TextureDesc desc, int transientPassIndex = -1)`
  （纹理句柄 创建纹理（in TextureDesc desc, int transientPassIndex = -1））
- `int GetTextureResourceCount()`
  （int 获取纹理资源数量（））
- `RenderGraphResourceRegistry.TextureResource GetTextureResource(in ResourceHandle handle)`
  （RenderGraph资源Registry.纹理资源 获取纹理资源（in ResourceHandle handle））
- `TextureDesc GetTextureResourceDesc(in ResourceHandle handle)`
  （纹理Desc 获取纹理资源Desc（in ResourceHandle handle））
- `void ForceTextureClear(in ResourceHandle handle, Color clearColor)`
  （void 强制纹理清除（in ResourceHandle handle, 颜色 clearColor））
- `RendererListHandle CreateRendererList(in RendererListDesc desc)`
  （渲染器列表句柄 创建渲染器列表（in RendererListDesc desc））
- `ComputeBufferHandle ImportComputeBuffer(ComputeBuffer computeBuffer)`
  （Compute缓冲区句柄 ImportCompute缓冲区（Compute缓冲区 computeBuffer））
- `ComputeBufferHandle CreateComputeBuffer(in ComputeBufferDesc desc, int transientPassIndex = -1)`
  （Compute缓冲区句柄 创建Compute缓冲区（in ComputeBufferDesc desc, int transientPassIndex = -1））
- `ComputeBufferDesc GetComputeBufferResourceDesc(in ResourceHandle handle)`
  （Compute缓冲区Desc 获取Compute缓冲区资源Desc（in ResourceHandle handle））
- `int GetComputeBufferResourceCount()`
  （int 获取Compute缓冲区资源数量（））
- `RenderGraphResourceRegistry.ComputeBufferResource GetComputeBufferResource(in ResourceHandle handle)`
  （RenderGraph资源Registry.Compute缓冲区资源 获取Compute缓冲区资源（in ResourceHandle handle））
- `void CreateAndClearTexture(RenderGraphContext rgContext, int index)`
  （void 创建And清除纹理（RenderGraphContext rgContext, int index））
- `void CreateComputeBuffer(RenderGraphContext rgContext, int index)`
  （void 创建Compute缓冲区（RenderGraphContext rgContext, int index））
- `void ReleaseTexture(RenderGraphContext rgContext, int index)`
  （void Release纹理（RenderGraphContext rgContext, int index））
- `void ReleaseComputeBuffer(RenderGraphContext rgContext, int index)`
  （void ReleaseCompute缓冲区（RenderGraphContext rgContext, int index））
- `void ValidateTextureDesc(in TextureDesc desc)`
  （void 验证纹理Desc（in TextureDesc desc））
- `void ValidateRendererListDesc(in RendererListDesc desc)`
  （void 验证渲染器列表Desc（in RendererListDesc desc））
- `void ValidateComputeBufferDesc(in ComputeBufferDesc desc)`
  （void 验证Compute缓冲区Desc（in ComputeBufferDesc desc））
- `void CreateRendererLists(List<RendererListHandle> rendererLists)`
  （void 创建渲染器Lists（List<渲染器列表Handle> rendererLists））
- `void Clear(bool onException)`
  （void 清除（bool onException））
- `void PurgeUnusedResources()`
  （void PurgeUnusedResources（））
- `void Cleanup()`
  （void 清理（））
- `void LogTextureCreation(RenderGraphResourceRegistry.TextureResource rt)`
  （void Log纹理Creation（RenderGraph资源Registry.纹理资源 rt））
- `void LogTextureRelease(RenderGraphResourceRegistry.TextureResource rt)`
  （void Log纹理Release（RenderGraph资源Registry.纹理资源 rt））
- `void LogComputeBufferCreation(RenderGraphResourceRegistry.ComputeBufferResource buffer)`
  （void LogCompute缓冲区Creation（RenderGraph资源Registry.Compute缓冲区资源 buffer））
- `void LogComputeBufferRelease(RenderGraphResourceRegistry.ComputeBufferResource buffer)`
  （void LogCompute缓冲区Release（RenderGraph资源Registry.Compute缓冲区资源 buffer））
- `void LogResources()`
  （void LogResources（））

---

## RenderGraphResourceRegistry.ComputeBufferResource（RenderGraph资源Registry.Compute缓冲区资源）

**继承**: RenderGraphResourceRegistry.RenderGraphResource<ComputeBufferDesc, ComputeBuffer>（RenderGraph资源Registry.RenderGraphResource<Compute缓冲区Desc, ComputeBuffer>）

### 方法 (1)

- `string GetName()`
  （字符串 获取名称（））

---

## RenderGraphResourceRegistry.IRenderGraphResource（RenderGraph资源Registry.IRenderGraph资源）

### 字段 (6)

- `bool imported`（bool imported）(偏移: 0x8)
- `int cachedHash`（int cachedHash）(偏移: 0xC)
- `int transientPassIndex`（int transientPass索引）(偏移: 0x10)
- `uint writeCount`（uint write数量）(偏移: 0x14)
- `bool wasReleased`（bool wasReleased）(偏移: 0x18)
- `bool requestFallBack`（bool request坠落后）(偏移: 0x19)

### 方法 (5)

- `void Reset()`
  （void 重置（））
- `string GetName()`
  （字符串 获取名称（））
- `bool IsCreated()`
  （bool 是否Created（））
- `void IncrementWriteCount()`
  （void IncrementWrite数量（））
- `bool NeedsFallBack()`
  （bool Needs坠落后（））

---

## RenderGraphResourceRegistry.RendererListResource（RenderGraph资源Registry.渲染器列表资源）

### 字段 (2)

- `RendererListDesc desc`（渲染器列表Desc desc）(偏移: 0x0)
- `RendererList rendererList`（渲染器列表 renderer列表）(偏移: 0xA4)

---

## RenderGraphResourceRegistry.TextureResource（RenderGraph资源Registry.纹理资源）

**继承**: RenderGraphResourceRegistry.RenderGraphResource<TextureDesc, RTHandle>（RenderGraph资源Registry.RenderGraphResource<纹理Desc, RTHandle>）

### 方法 (1)

- `string GetName()`
  （字符串 获取名称（））

---

## RenderGraphResourceType（RenderGraph资源类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RenderMode（Render模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RenderObjects（RenderObjects）

**继承**: ScriptableRendererFeature（可脚本化渲染器特性）

### 字段 (2)

- `RenderObjects.RenderObjectsSettings settings`（RenderObjects.RenderObjectsSettings settings）(偏移: 0x10)
- `RenderObjectsPass renderObjectsPass`（RenderObjectsPass renderObjectsPass）(偏移: 0x14)

### 方法 (2)

- `void Create()`
  （void 创建（））
- `void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)`
  （void 添加渲染通道（可脚本化渲染器 renderer, 引用 渲染数据 renderingData））

---

## RenderObjects.CustomCameraSettings（RenderObjects.自定义的摄像机Settings）

### 字段 (4)

- `bool overrideCamera`（bool override摄像机）(偏移: 0x8)
- `bool restoreCamera`（bool restore摄像机）(偏移: 0x9)
- `Vector4 offset`（Vector4 offset）(偏移: 0xC)
- `float cameraFieldOfView`（float cameraFieldOf视图）(偏移: 0x1C)

---

## RenderObjects.FilterSettings（RenderObjects.FilterSettings）

### 字段 (3)

- `RenderQueueType RenderQueueType`（Render队列类型 Render队列类型）(偏移: 0x8)
- `LayerMask LayerMask`（层掩码 层掩码）(偏移: 0xC)
- `string[] PassNames`（string[] PassNames）(偏移: 0x10)

---

## RenderObjects.RenderObjectsSettings（RenderObjects.RenderObjectsSettings）

### 字段 (10)

- `string passTag`（string pass标签）(偏移: 0x8)
- `RenderPassEvent Event`（RenderPass事件 事件）(偏移: 0xC)
- `RenderObjects.FilterSettings filterSettings`（RenderObjects.FilterSettings filterSettings）(偏移: 0x10)
- `Material overrideMaterial`（材质 override材质）(偏移: 0x14)
- `int overrideMaterialPassIndex`（int override材质Pass索引）(偏移: 0x18)
- `bool overrideDepthState`（bool override深度状态）(偏移: 0x1C)
- `CompareFunction depthCompareFunction`（CompareFunction depthCompareFunction）(偏移: 0x20)
- `bool enableWrite`（bool enableWrite）(偏移: 0x24)
- `StencilStateData stencilSettings`（Stencil状态数据 stencilSettings）(偏移: 0x28)
- `RenderObjects.CustomCameraSettings cameraSettings`（RenderObjects.自定义的摄像机Settings cameraSettings）(偏移: 0x2C)

---

## RenderObjectsPass（RenderObjectsPass）

**继承**: ScriptableRenderPass（可脚本化渲染通道）

### 字段 (7)

- `RenderQueueType renderQueueType`（Render队列类型 render队列类型）(偏移: 0x54)
- `FilteringSettings m_FilteringSettings`（过滤设置 m_过滤设置）(偏移: 0x58)
- `RenderObjects.CustomCameraSettings m_CameraSettings`（RenderObjects.自定义的摄像机Settings m_摄像机Settings）(偏移: 0x70)
- `string m_ProfilerTag`（string m_Profiler标签）(偏移: 0x74)
- `ProfilingSampler m_ProfilingSampler`（性能分析采样器 m_性能分析采样器）(偏移: 0x78)
- `List<ShaderTagId> m_ShaderTagIdList`（List<着色器标签Id> m_着色器标签Id列表）(偏移: 0x84)
- `RenderStateBlock m_RenderStateBlock`（Render状态Block m_Render状态Block）(偏移: 0x88)

### 方法 (7)

- `Material get_overrideMaterial()`
  （材质 get_override材质（））
- `void set_overrideMaterial(Material value)`
  （void set_override材质（材质 value））
- `int get_overrideMaterialPassIndex()`
  （int get_override材质Pass索引（））
- `void set_overrideMaterialPassIndex(int value)`
  （void set_override材质Pass索引（int value））
- `void SetDetphState(bool writeEnabled, CompareFunction function = 2)`
  （void 集合Detph状态（bool writeEnabled, CompareFunction function = 2））
- `void SetStencilState(int reference, CompareFunction compareFunction, StencilOp passOp, StencilOp failOp, StencilOp zFailOp)`
  （void 集合Stencil状态（int reference, CompareFunction compareFunction, StencilOp passOp, StencilOp failOp, StencilOp zFailOp））
- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（可脚本化渲染上下文 context, 引用 渲染数据 renderingData））

---

## RenderPassEvent（RenderPass事件）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RenderPipeline（RenderPipeline）

### 方法 (11)

- `void ProcessRenderRequests(ScriptableRenderContext context, Camera camera, List<Camera.RenderRequest> renderRequests)`
  （void 处理RenderRequests（ScriptableRenderContext context, 摄像机 camera, List<Camera.RenderRequest> renderRequests））
- `void BeginFrameRendering(ScriptableRenderContext context, Camera[] cameras)`
  （void BeginFrameRendering（ScriptableRenderContext context, Camera[] cameras））
- `void BeginCameraRendering(ScriptableRenderContext context, Camera camera)`
  （void Begin摄像机Rendering（ScriptableRenderContext context, 摄像机 camera））
- `void EndFrameRendering(ScriptableRenderContext context, Camera[] cameras)`
  （void 结束FrameRendering（ScriptableRenderContext context, Camera[] cameras））
- `void EndCameraRendering(ScriptableRenderContext context, Camera camera)`
  （void 结束摄像机Rendering（ScriptableRenderContext context, 摄像机 camera））
- `void InternalRender(ScriptableRenderContext context, Camera[] cameras)`
  （void 内部的Render（ScriptableRenderContext context, Camera[] cameras））
- `void InternalRenderWithRequests(ScriptableRenderContext context, Camera[] cameras, List<Camera.RenderRequest> renderRequests)`
  （void 内部的RenderWithRequests（ScriptableRenderContext context, Camera[] cameras, List<Camera.RenderRequest> renderRequests））
- `bool get_disposed()`
  （bool get_disposed（））
- `void set_disposed(bool value)`
  （void set_disposed（bool value））
- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））

---

## RenderPipelineAsset（RenderPipeline资产）

**继承**: ScriptableObject（脚本对象）

### 方法 (21)

- `RenderPipeline InternalCreatePipeline()`
  （RenderPipeline 内部的创建Pipeline（））
- `string[] get_renderingLayerMaskNames()`
  （string[] get_rendering层掩码Names（））
- `Material get_defaultMaterial()`
  （材质 get_default材质（））
- `Shader get_autodeskInteractiveShader()`
  （着色器 get_autodeskInteractive着色器（））
- `Shader get_autodeskInteractiveTransparentShader()`
  （着色器 get_autodeskInteractive透明的着色器（））
- `Shader get_autodeskInteractiveMaskedShader()`
  （着色器 get_autodeskInteractiveMasked着色器（））
- `Shader get_terrainDetailLitShader()`
  （着色器 get_terrainDetailLit着色器（））
- `Shader get_terrainDetailGrassShader()`
  （着色器 get_terrainDetailGrass着色器（））
- `Shader get_terrainDetailGrassBillboardShader()`
  （着色器 get_terrainDetailGrassBillboard着色器（））
- `Material get_defaultParticleMaterial()`
  （材质 get_default粒子材质（））
- `Material get_defaultLineMaterial()`
  （材质 get_defaultLine材质（））
- `Material get_defaultTerrainMaterial()`
  （材质 get_defaultTerrain材质（））
- `Material get_defaultUIMaterial()`
  （材质 get_default界面材质（））
- `Material get_defaultUIOverdrawMaterial()`
  （材质 get_default界面Overdraw材质（））
- `Material get_defaultUIETC1SupportedMaterial()`
  （材质 get_defaultUIETC1Supported材质（））
- `Material get_default2DMaterial()`
  （材质 get_default2D材质（））
- `Shader get_defaultShader()`
  （着色器 get_default着色器（））
- `Shader get_defaultSpeedTree7Shader()`
  （着色器 get_defaultSpeedTree7着色器（））
- `Shader get_defaultSpeedTree8Shader()`
  （着色器 get_defaultSpeedTree8着色器（））
- `void OnValidate()`
  （void 验证时（））
- `void OnDisable()`
  （void 禁用时（））

---

## RenderPipelineManager（RenderPipeline管理器）

### 字段 (3)

- `RenderPipelineAsset s_CurrentPipelineAsset`（RenderPipeline资产 s_当前Pipeline资产）(偏移: 0x0)
- `Camera[] s_Cameras`（Camera[] s_Cameras）(偏移: 0x4)
- `int s_CameraCapacity`（int s_摄像机Capacity）(偏移: 0x8)

### 方法 (16)

- `RenderPipeline get_currentPipeline()`
  （RenderPipeline get_currentPipeline（））
- `void set_currentPipeline(RenderPipeline value)`
  （void set_currentPipeline（RenderPipeline value））
- `void add_beginFrameRendering(Action<ScriptableRenderContext, Camera[]> value)`
  （void add_beginFrameRendering（Action<ScriptableRenderContext, Camera[]> value））
- `void remove_beginFrameRendering(Action<ScriptableRenderContext, Camera[]> value)`
  （void remove_beginFrameRendering（Action<ScriptableRenderContext, Camera[]> value））
- `void add_beginCameraRendering(Action<ScriptableRenderContext, Camera> value)`
  （void add_begin摄像机Rendering（Action<ScriptableRenderContext, Camera> value））
- `void remove_beginCameraRendering(Action<ScriptableRenderContext, Camera> value)`
  （void remove_begin摄像机Rendering（Action<ScriptableRenderContext, Camera> value））
- `void add_endCameraRendering(Action<ScriptableRenderContext, Camera> value)`
  （void add_end摄像机Rendering（Action<ScriptableRenderContext, Camera> value））
- `void remove_endCameraRendering(Action<ScriptableRenderContext, Camera> value)`
  （void remove_end摄像机Rendering（Action<ScriptableRenderContext, Camera> value））
- `void BeginFrameRendering(ScriptableRenderContext context, Camera[] cameras)`
  （void BeginFrameRendering（ScriptableRenderContext context, Camera[] cameras））
- `void BeginCameraRendering(ScriptableRenderContext context, Camera camera)`
  （void Begin摄像机Rendering（ScriptableRenderContext context, 摄像机 camera））
- `void EndFrameRendering(ScriptableRenderContext context, Camera[] cameras)`
  （void 结束FrameRendering（ScriptableRenderContext context, Camera[] cameras））
- `void EndCameraRendering(ScriptableRenderContext context, Camera camera)`
  （void 结束摄像机Rendering（ScriptableRenderContext context, 摄像机 camera））
- `void CleanupRenderPipeline()`
  （void 清理RenderPipeline（））
- `void GetCameras(ScriptableRenderContext context)`
  （void 获取Cameras（ScriptableRenderContext context））
- `void DoRenderLoop_Internal(RenderPipelineAsset pipe, IntPtr loopPtr, List<Camera.RenderRequest> renderRequests)`
  （void DoRenderLoop_内部的（RenderPipeline资产 pipe, 整数Ptr loopPtr, List<Camera.RenderRequest> renderRequests））
- `void PrepareRenderPipeline(RenderPipelineAsset pipelineAsset)`
  （void PrepareRenderPipeline（RenderPipeline资产 pipelineAsset））

---

## RenderQueueRange（Render队列范围）

**继承**: IEquatable<RenderQueueRange>（IEquatable<Render队列Range>）

### 字段 (4)

- `int m_LowerBound`（int m_下半身Bound）(偏移: 0x0)
- `int m_UpperBound`（int m_上半身Bound）(偏移: 0x4)
- `int minimumBound`（int minimumBound）(偏移: 0x0)
- `int maximumBound`（int maximumBound）(偏移: 0x4)

### 方法 (6)

- `RenderQueueRange get_all()`
  （Render队列范围 get_all（））
- `RenderQueueRange get_opaque()`
  （Render队列范围 get_opaque（））
- `RenderQueueRange get_transparent()`
  （Render队列范围 get_transparent（））
- `bool Equals(RenderQueueRange other)`
  （bool Equals（Render队列范围 other））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## RenderQueueType（Render队列类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RenderSettings（RenderSettings）

**继承**: Object（对象）

### 方法 (14)

- `bool get_fog()`
  （bool get_fog（））
- `Color get_ambientSkyColor()`
  （颜色 get_ambientSky颜色（））
- `Color get_ambientEquatorColor()`
  （颜色 get_ambientEquator颜色（））
- `Color get_ambientGroundColor()`
  （颜色 get_ambient地面颜色（））
- `Color get_subtractiveShadowColor()`
  （颜色 get_subtractiveShadow颜色（））
- `Material get_skybox()`
  （材质 get_skybox（））
- `Light get_sun()`
  （光照 get_sun（））
- `SphericalHarmonicsL2 get_ambientProbe()`
  （SphericalHarmonicsL2 get_ambientProbe（））
- `float get_reflectionIntensity()`
  （float get_reflectionIntensity（））
- `void get_ambientSkyColor_Injected(out Color ret)`
  （void get_ambientSkyColor_Injected（out Color ret））
- `void get_ambientEquatorColor_Injected(out Color ret)`
  （void get_ambientEquatorColor_Injected（out Color ret））
- `void get_ambientGroundColor_Injected(out Color ret)`
  （void get_ambient地面Color_Injected（out Color ret））
- `void get_subtractiveShadowColor_Injected(out Color ret)`
  （void get_subtractiveShadowColor_Injected（out Color ret））
- `void get_ambientProbe_Injected(out SphericalHarmonicsL2 ret)`
  （void get_ambientProbe_Injected（out SphericalHarmonicsL2 ret））

---

## RenderStateBlock（Render状态Block）

**继承**: IEquatable<RenderStateBlock>（IEquatable<Render状态Block>）

### 字段 (6)

- `BlendState m_BlendState`（Blend状态 m_Blend状态）(偏移: 0x0)
- `RasterState m_RasterState`（Raster状态 m_Raster状态）(偏移: 0x44)
- `DepthState m_DepthState`（深度状态 m_深度状态）(偏移: 0x54)
- `StencilState m_StencilState`（Stencil状态 m_Stencil状态）(偏移: 0x56)
- `int m_StencilReference`（int m_Stencil引用）(偏移: 0x64)
- `RenderStateMask m_Mask`（Render状态掩码 m_掩码）(偏移: 0x68)

### 方法 (10)

- `void set_depthState(DepthState value)`
  （void set_depth状态（深度状态 value））
- `StencilState get_stencilState()`
  （Stencil状态 get_stencil状态（））
- `void set_stencilState(StencilState value)`
  （void set_stencil状态（Stencil状态 value））
- `int get_stencilReference()`
  （int get_stencil引用（））
- `void set_stencilReference(int value)`
  （void set_stencil引用（int value））
- `RenderStateMask get_mask()`
  （Render状态掩码 get_mask（））
- `void set_mask(RenderStateMask value)`
  （void set_mask（Render状态掩码 value））
- `bool Equals(RenderStateBlock other)`
  （bool Equals（Render状态Block other））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## RenderStateMask（Render状态掩码）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RenderTargetBlendState（Render目标Blend状态）

**继承**: IEquatable<RenderTargetBlendState>（IEquatable<Render目标BlendState>）

### 字段 (8)

- `byte m_WriteMask`（byte m_Write掩码）(偏移: 0x0)
- `byte m_SourceColorBlendMode`（byte m_Source颜色Blend模式）(偏移: 0x0)
- `byte m_DestinationColorBlendMode`（byte m_Destination颜色Blend模式）(偏移: 0x0)
- `byte m_SourceAlphaBlendMode`（byte m_Source透明度Blend模式）(偏移: 0x0)
- `byte m_DestinationAlphaBlendMode`（byte m_Destination透明度Blend模式）(偏移: 0x0)
- `byte m_ColorBlendOperation`（byte m_颜色BlendOperation）(偏移: 0x0)
- `byte m_AlphaBlendOperation`（byte m_透明度BlendOperation）(偏移: 0x0)
- `byte m_Padding`（byte m_Padding）(偏移: 0x0)

### 方法 (4)

- `RenderTargetBlendState get_defaultValue()`
  （Render目标Blend状态 get_default值（））
- `bool Equals(RenderTargetBlendState other)`
  （bool Equals（Render目标Blend状态 other））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## RenderTargetFlags（Render目标Flags）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RenderTargetHandle（Render目标句柄）

### 字段 (1)

- `RenderTargetHandle CameraTarget`（Render目标句柄 摄像机目标）(偏移: 0x0)

### 方法 (14)

- `void set_id(int value)`
  （void set_id（int value））
- `int get_id()`
  （int get_id（））
- `void set_rtid(RenderTargetIdentifier value)`
  （void set_rtid（Render目标Identifier value））
- `RenderTargetIdentifier get_rtid()`
  （Render目标Identifier get_rtid（））
- `RenderTargetHandle GetCameraTarget(XRPass xr)`
  （Render目标句柄 获取摄像机目标（XRPass xr））
- `void Init(string shaderProperty)`
  （void 初始化（string shaderProperty））
- `void Init(RenderTargetIdentifier renderTargetIdentifier)`
  （void 初始化（Render目标Identifier renderTargetIdentifier））
- `RenderTargetIdentifier Identifier()`
  （Render目标Identifier Identifier（））
- `bool HasInternalRenderTargetId()`
  （bool 是否有内部的Render目标Id（））
- `bool Equals(RenderTargetHandle other)`
  （bool Equals（Render目标句柄 other））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `bool op_Equality(RenderTargetHandle c1, RenderTargetHandle c2)`
  （bool op_Equality（Render目标句柄 c1, Render目标句柄 c2））
- `bool op_Inequality(RenderTargetHandle c1, RenderTargetHandle c2)`
  （bool op_Inequality（Render目标句柄 c1, Render目标句柄 c2））

---

## RenderTargetIdentifier（Render目标Identifier）

**继承**: IEquatable<RenderTargetIdentifier>（IEquatable<Render目标Identifier>）

### 字段 (7)

- `BuiltinRenderTextureType m_Type`（BuiltinRender纹理类型 m_类型）(偏移: 0x0)
- `int m_NameID`（int m_名称ID）(偏移: 0x4)
- `int m_InstanceID`（int m_实例ID）(偏移: 0x8)
- `IntPtr m_BufferPointer`（整数Ptr m_缓冲区指针）(偏移: 0xC)
- `int m_MipLevel`（int m_Mip等级）(偏移: 0x10)
- `CubemapFace m_CubeFace`（CubemapFace m_CubeFace）(偏移: 0x14)
- `int m_DepthSlice`（int m_深度Slice）(偏移: 0x18)

### 方法 (9)

- `RenderTargetIdentifier op_Implicit(BuiltinRenderTextureType type)`
  （Render目标Identifier op_Implicit（BuiltinRender纹理类型 type））
- `RenderTargetIdentifier op_Implicit(int nameID)`
  （Render目标Identifier op_Implicit（int nameID））
- `RenderTargetIdentifier op_Implicit(Texture tex)`
  （Render目标Identifier op_Implicit（纹理 tex））
- `string ToString()`
  （字符串 转字符串（））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `bool Equals(RenderTargetIdentifier rhs)`
  （bool Equals（Render目标Identifier rhs））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool op_Equality(RenderTargetIdentifier lhs, RenderTargetIdentifier rhs)`
  （bool op_Equality（Render目标Identifier lhs, Render目标Identifier rhs））
- `bool op_Inequality(RenderTargetIdentifier lhs, RenderTargetIdentifier rhs)`
  （bool op_Inequality（Render目标Identifier lhs, Render目标Identifier rhs））

---

## RenderTexture（Render纹理）

**继承**: Texture（纹理）

### 方法 (50)

- `int get_width()`
  （整数 获取_宽度（））
- `void set_width(int value)`
  （void 设置_宽度（整数 value））
- `int get_height()`
  （整数 获取_高度（））
- `void set_height(int value)`
  （void 设置_高度（整数 value））
- `TextureDimension get_dimension()`
  （纹理Dimension get_dimension（））
- `void set_dimension(TextureDimension value)`
  （void set_dimension（纹理Dimension value））
- `GraphicsFormat get_graphicsFormat()`
  （Graphics格式化 get_graphics格式化（））
- `void set_graphicsFormat(GraphicsFormat value)`
  （void set_graphics格式化（Graphics格式化 value））
- `bool get_useMipMap()`
  （bool get_useMip映射（））
- `void set_useMipMap(bool value)`
  （void set_useMip映射（bool value））
- `bool get_sRGB()`
  （bool get_sRGB颜色（））
- `void set_memorylessMode(RenderTextureMemoryless value)`
  （void set_memoryless模式（Render纹理Memoryless value））
- `RenderTextureFormat get_format()`
  （Render纹理格式化 get_format（））
- `void set_stencilFormat(GraphicsFormat value)`
  （void set_stencil格式化（Graphics格式化 value））
- `void set_autoGenerateMips(bool value)`
  （void set_autoGenerateMips（bool value））
- `int get_volumeDepth()`
  （int get_volume深度（））
- `void set_volumeDepth(int value)`
  （void set_volume深度（int value））
- `int get_antiAliasing()`
  （int get_antiAliasing（））
- `void set_antiAliasing(int value)`
  （void set_antiAliasing（int value））
- `void set_bindTextureMS(bool value)`
  （void set_bind纹理MS（bool value））
- `void set_enableRandomWrite(bool value)`
  （void set_enable随机Write（bool value））
- `bool get_useDynamicScale()`
  （bool get_use动态的缩放（））
- `void set_useDynamicScale(bool value)`
  （void set_use动态的缩放（bool value））
- `RenderTexture GetActive()`
  （Render纹理 获取激活的（））
- `void SetActive(RenderTexture rt)`
  （void 集合激活的（Render纹理 rt））
- `RenderTexture get_active()`
  （Render纹理 get_active（））
- `void set_active(RenderTexture value)`
  （void set_active（Render纹理 value））
- `void DiscardContents(bool discardColor, bool discardDepth)`
  （void DiscardContents（bool discardColor, bool discardDepth））
- `void DiscardContents()`
  （void DiscardContents（））
- `bool Create()`
  （bool 创建（））
- `void Release()`
  （void 释放（））
- `bool IsCreated()`
  （bool 是否Created（））
- `void SetSRGBReadWrite(bool srgb)`
  （void 集合SRGBReadWrite（bool srgb））
- `void Internal_Create(RenderTexture rt)`
  （void Internal_创建（Render纹理 rt））
- `void SetRenderTextureDescriptor(RenderTextureDescriptor desc)`
  （void 集合Render纹理Descriptor（Render纹理Descriptor desc））
- `RenderTextureDescriptor GetDescriptor()`
  （Render纹理Descriptor 获取Descriptor（））
- `RenderTexture GetTemporary_Internal(RenderTextureDescriptor desc)`
  （Render纹理 获取Temporary_内部的（Render纹理Descriptor desc））
- `void ReleaseTemporary(RenderTexture temp)`
  （void Release临时的（Render纹理 temp））
- `void set_depth(int value)`
  （void set_depth（int value））
- `RenderTextureDescriptor get_descriptor()`
  （Render纹理Descriptor get_descriptor（））
- `void set_descriptor(RenderTextureDescriptor value)`
  （void set_descriptor（Render纹理Descriptor value））
- `void ValidateRenderTextureDesc(RenderTextureDescriptor desc)`
  （void 验证Render纹理Desc（Render纹理Descriptor desc））
- `GraphicsFormat GetCompatibleFormat(RenderTextureFormat renderTextureFormat, RenderTextureReadWrite readWrite)`
  （Graphics格式化 获取Compatible格式化（Render纹理格式化 renderTextureFormat, Render纹理ReadWrite readWrite））
- `RenderTexture GetTemporary(RenderTextureDescriptor desc)`
  （Render纹理 获取临时的（Render纹理Descriptor desc））
- `RenderTexture GetTemporaryImpl(int width, int height, int depthBuffer, GraphicsFormat format, int antiAliasing = 1, RenderTextureMemoryless memorylessMode = 0, VRTextureUsage vrUsage = 0, bool useDynamicScale = False)`
  （Render纹理 获取临时的Impl（int width, int height, int depthBuffer, Graphics格式化 format, int antiAliasing = 1, Render纹理Memoryless memorylessMode = 0, VR纹理Usage vrUsage = 0, bool useDynamicScale = False））
- `RenderTexture GetTemporary(int width, int height, int depthBuffer, RenderTextureFormat format, RenderTextureReadWrite readWrite, int antiAliasing, RenderTextureMemoryless memorylessMode)`
  （Render纹理 获取临时的（int width, int height, int depthBuffer, Render纹理格式化 format, Render纹理ReadWrite readWrite, int antiAliasing, Render纹理Memoryless memorylessMode））
- `RenderTexture GetTemporary(int width, int height, int depthBuffer, RenderTextureFormat format)`
  （Render纹理 获取临时的（int width, int height, int depthBuffer, Render纹理格式化 format））
- `void SetRenderTextureDescriptor_Injected(ref RenderTextureDescriptor desc)`
  （void 集合Render纹理Descriptor_Injected（ref RenderTextureDescriptor desc））
- `void GetDescriptor_Injected(out RenderTextureDescriptor ret)`
  （void 获取Descriptor_Injected（out RenderTextureDescriptor ret））
- `RenderTexture GetTemporary_Internal_Injected(ref RenderTextureDescriptor desc)`
  （Render纹理 获取Temporary_Internal_Injected（ref RenderTextureDescriptor desc））

---

## RenderTextureCreationFlags（Render纹理CreationFlags）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RenderTextureDescriptor（Render纹理Descriptor）

### 字段 (4)

- `GraphicsFormat _graphicsFormat`（Graphics格式化 _graphics格式化）(偏移: 0x14)
- `int _depthBufferBits`（int _depth缓冲区Bits）(偏移: 0x1C)
- `int[] depthFormatBits`（int[] depth格式化Bits）(偏移: 0x0)
- `RenderTextureCreationFlags _flags`（Render纹理CreationFlags _flags）(偏移: 0x2C)

### 方法 (33)

- `int get_width()`
  （整数 获取_宽度（））
- `void set_width(int value)`
  （void 设置_宽度（整数 value））
- `int get_height()`
  （整数 获取_高度（））
- `void set_height(int value)`
  （void 设置_高度（整数 value））
- `int get_msaaSamples()`
  （int get_msaaSamples（））
- `void set_msaaSamples(int value)`
  （void set_msaaSamples（int value））
- `int get_volumeDepth()`
  （int get_volume深度（））
- `void set_volumeDepth(int value)`
  （void set_volume深度（int value））
- `int get_mipCount()`
  （int get_mip数量（））
- `void set_mipCount(int value)`
  （void set_mip数量（int value））
- `GraphicsFormat get_graphicsFormat()`
  （Graphics格式化 get_graphics格式化（））
- `void set_graphicsFormat(GraphicsFormat value)`
  （void set_graphics格式化（Graphics格式化 value））
- `void set_stencilFormat(GraphicsFormat value)`
  （void set_stencil格式化（Graphics格式化 value））
- `RenderTextureFormat get_colorFormat()`
  （Render纹理格式化 get_color格式化（））
- `void set_colorFormat(RenderTextureFormat value)`
  （void set_color格式化（Render纹理格式化 value））
- `bool get_sRGB()`
  （bool get_sRGB颜色（））
- `void set_sRGB(bool value)`
  （void set_sRGB颜色（bool value））
- `int get_depthBufferBits()`
  （int get_depth缓冲区Bits（））
- `void set_depthBufferBits(int value)`
  （void set_depth缓冲区Bits（int value））
- `TextureDimension get_dimension()`
  （纹理Dimension get_dimension（））
- `void set_dimension(TextureDimension value)`
  （void set_dimension（纹理Dimension value））
- `void set_shadowSamplingMode(ShadowSamplingMode value)`
  （void set_shadowSampling模式（ShadowSampling模式 value））
- `VRTextureUsage get_vrUsage()`
  （VR纹理Usage get_vrUsage（））
- `void set_vrUsage(VRTextureUsage value)`
  （void set_vrUsage（VR纹理Usage value））
- `void set_memoryless(RenderTextureMemoryless value)`
  （void set_memoryless（Render纹理Memoryless value））
- `void SetOrClearRenderTextureCreationFlag(bool value, RenderTextureCreationFlags flag)`
  （void 集合Or清除Render纹理Creation标志（bool value, Render纹理CreationFlags flag））
- `void set_useMipMap(bool value)`
  （void set_useMip映射（bool value））
- `void set_autoGenerateMips(bool value)`
  （void set_autoGenerateMips（bool value））
- `void set_enableRandomWrite(bool value)`
  （void set_enable随机Write（bool value））
- `void set_bindMS(bool value)`
  （void set_bindMS（bool value））
- `void set_createdFromScript(bool value)`
  （void set_createdFromScript（bool value））
- `bool get_useDynamicScale()`
  （bool get_use动态的缩放（））
- `void set_useDynamicScale(bool value)`
  （void set_use动态的缩放（bool value））

---

## RenderTextureFormat（Render纹理格式化）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RenderTextureMemoryless（Render纹理Memoryless）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RenderTextureReadWrite（Render纹理ReadWrite）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RenderTextureSubElement（Render纹理子元素）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Renderer（渲染器）

**继承**: Component（组件）

### 方法 (34)

- `Bounds get_bounds()`
  （边界 获取_边界（））
- `Material GetMaterial()`
  （材质 获取材质（））
- `Material GetSharedMaterial()`
  （材质 获取Shared材质（））
- `void SetMaterial(Material m)`
  （void 集合材质（材质 m））
- `void SetMaterialArray(Material[] m)`
  （void 集合材质数组（Material[] m））
- `bool get_enabled()`
  （布尔值 获取_已启用（））
- `void set_enabled(bool value)`
  （void 设置_已启用（布尔值 value））
- `bool get_isVisible()`
  （bool get_is可见的（））
- `ShadowCastingMode get_shadowCastingMode()`
  （ShadowCasting模式 get_shadowCasting模式（））
- `void set_shadowCastingMode(ShadowCastingMode value)`
  （void set_shadowCasting模式（ShadowCasting模式 value））
- `void set_receiveShadows(bool value)`
  （void set_receiveShadows（bool value））
- `uint get_renderingLayerMask()`
  （uint get_rendering层掩码（））
- `void set_renderingLayerMask(uint value)`
  （void set_rendering层掩码（uint value））
- `int get_sortingLayerID()`
  （int get_sorting层ID（））
- `int get_sortingOrder()`
  （int get_sortingOrder（））
- `void set_staticBatchRootTransform(Transform value)`
  （void set_staticBatch根变换（变换 value））
- `int get_staticBatchIndex()`
  （int get_staticBatch索引（））
- `void SetStaticBatchInfo(int firstSubMesh, int subMeshCount)`
  （void 集合静态的Batch信息（int firstSubMesh, int subMeshCount））
- `bool get_isPartOfStaticBatch()`
  （bool get_isPartOf静态的Batch（））
- `Matrix4x4 get_localToWorldMatrix()`
  （Matrix4x4 get_localTo世界的矩阵（））
- `int GetLightmapIndex(LightmapType lt)`
  （int 获取Lightmap索引（Lightmap类型 lt））
- `Vector4 GetLightmapST(LightmapType lt)`
  （Vector4 获取LightmapST（Lightmap类型 lt））
- `int get_lightmapIndex()`
  （int get_lightmap索引（））
- `Vector4 get_lightmapScaleOffset()`
  （Vector4 get_lightmap缩放Offset（））
- `Vector4 get_realtimeLightmapScaleOffset()`
  （Vector4 get_realtimeLightmap缩放Offset（））
- `Material[] GetSharedMaterialArray()`
  （Material[] 获取Shared材质数组（））
- `Material get_material()`
  （材质 获取_材质（））
- `Material get_sharedMaterial()`
  （材质 get_shared材质（））
- `void set_sharedMaterial(Material value)`
  （void set_shared材质（材质 value））
- `Material[] get_sharedMaterials()`
  （Material[] get_sharedMaterials（））
- `void set_sharedMaterials(Material[] value)`
  （void set_sharedMaterials（Material[] value））
- `void get_bounds_Injected(out Bounds ret)`
  （void 获取_边界_注入（输出 Bounds ret））
- `void get_localToWorldMatrix_Injected(out Matrix4x4 ret)`
  （void get_localTo世界的Matrix_Injected（out Matrix4x4 ret））
- `void GetLightmapST_Injected(LightmapType lt, out Vector4 ret)`
  （void 获取LightmapST_Injected（Lightmap类型 lt, out Vector4 ret））

---

## Renderer2D（Renderer2D）

**继承**: ScriptableRenderer（Scriptable渲染器）

### 字段 (17)

- `ColorGradingLutPass m_ColorGradingLutPass`（颜色GradingLutPass m_颜色GradingLutPass）(偏移: 0x5C)
- `Render2DLightingPass m_Render2DLightingPass`（Render2DLightingPass m_Render2DLightingPass）(偏移: 0x60)
- `PostProcessPass m_PostProcessPass`（Post处理Pass m_Post处理Pass）(偏移: 0x64)
- `PixelPerfectBackgroundPass m_PixelPerfectBackgroundPass`（PixelPerfectBackgroundPass m_PixelPerfectBackgroundPass）(偏移: 0x68)
- `FinalBlitPass m_FinalBlitPass`（FinalBlitPass m_FinalBlitPass）(偏移: 0x6C)
- `PostProcessPass m_FinalPostProcessPass`（Post处理Pass m_FinalPost处理Pass）(偏移: 0x70)
- `Light2DCullResult m_LightCullResult`（Light2DCullResult m_光照CullResult）(偏移: 0x74)
- `ProfilingSampler m_ProfilingSampler`（性能分析采样器 m_性能分析采样器）(偏移: 0x0)
- `bool m_UseDepthStencilBuffer`（bool m_Use深度Stencil缓冲区）(偏移: 0x78)
- `bool m_CreateColorTexture`（bool m_创建颜色纹理）(偏移: 0x79)
- `bool m_CreateDepthTexture`（bool m_创建深度纹理）(偏移: 0x7A)
- `RenderTargetHandle k_ColorTextureHandle`（Render目标句柄 k_颜色纹理句柄）(偏移: 0x7C)
- `RenderTargetHandle k_DepthTextureHandle`（Render目标句柄 k_深度纹理句柄）(偏移: 0x9C)
- `RenderTargetHandle k_AfterPostProcessColorHandle`（Render目标句柄 k_AfterPost处理颜色句柄）(偏移: 0xBC)
- `RenderTargetHandle k_ColorGradingLutHandle`（Render目标句柄 k_颜色GradingLut句柄）(偏移: 0xDC)
- `Material m_BlitMaterial`（材质 m_Blit材质）(偏移: 0xFC)
- `Renderer2DData m_Renderer2DData`（Renderer2D数据 m_Renderer2D数据）(偏移: 0x100)

### 方法 (8)

- `bool get_createColorTexture()`
  （bool get_create颜色纹理（））
- `bool get_createDepthTexture()`
  （bool get_create深度纹理（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `Renderer2DData GetRenderer2DData()`
  （Renderer2D数据 获取Renderer2D数据（））
- `void CreateRenderTextures(ref CameraData cameraData, bool forceCreateColorTexture, FilterMode colorTextureFilterMode, CommandBuffer cmd, out RenderTargetHandle colorTargetHandle, out RenderTargetHandle depthTargetHandle)`
  （void 创建RenderTextures（ref CameraData cameraData, bool forceCreateColorTexture, Filter模式 colorTextureFilterMode, Command缓冲区 cmd, out RenderTargetHandle colorTargetHandle, out RenderTargetHandle depthTargetHandle））
- `void Setup(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void Setup（ScriptableRenderContext context, ref RenderingData renderingData））
- `void SetupCullingParameters(ref ScriptableCullingParameters cullingParameters, ref CameraData cameraData)`
  （void SetupCullingParameters（ref ScriptableCullingParameters cullingParameters, ref CameraData cameraData））
- `void FinishRendering(CommandBuffer cmd)`
  （void FinishRendering（Command缓冲区 cmd））

---

## Renderer2DData（Renderer2D数据）

**继承**: ScriptableRendererData（Scriptable渲染器数据）

### 字段 (15)

- `TransparencySortMode m_TransparencySortMode`（TransparencySort模式 m_TransparencySort模式）(偏移: 0x18)
- `Vector3 m_TransparencySortAxis`（三维向量 m_TransparencySort轴）(偏移: 0x1C)
- `float m_HDREmulationScale`（float m_HDREmulation缩放）(偏移: 0x28)
- `Light2DBlendStyle[] m_LightBlendStyles`（Light2DBlendStyle[] m_光照BlendStyles）(偏移: 0x2C)
- `bool m_UseDepthStencilBuffer`（bool m_Use深度Stencil缓冲区）(偏移: 0x30)
- `Shader m_ShapeLightShader`（着色器 m_Shape光照着色器）(偏移: 0x34)
- `Shader m_ShapeLightVolumeShader`（着色器 m_Shape光照Volume着色器）(偏移: 0x38)
- `Shader m_PointLightShader`（着色器 m_Point光照着色器）(偏移: 0x3C)
- `Shader m_PointLightVolumeShader`（着色器 m_Point光照Volume着色器）(偏移: 0x40)
- `Shader m_BlitShader`（着色器 m_Blit着色器）(偏移: 0x44)
- `Shader m_ShadowGroupShader`（着色器 m_Shadow组着色器）(偏移: 0x48)
- `Shader m_RemoveSelfShadowShader`（着色器 m_移除SelfShadow着色器）(偏移: 0x4C)
- `PostProcessData m_PostProcessData`（Post处理数据 m_Post处理数据）(偏移: 0x50)
- `RenderTargetHandle normalsRenderTarget`（Render目标句柄 normalsRender目标）(偏移: 0x60)
- `RenderTargetHandle shadowsRenderTarget`（Render目标句柄 shadowsRender目标）(偏移: 0x80)

### 方法 (21)

- `float get_hdrEmulationScale()`
  （float get_hdrEmulation缩放（））
- `Light2DBlendStyle[] get_lightBlendStyles()`
  （Light2DBlendStyle[] get_lightBlendStyles（））
- `bool get_useDepthStencilBuffer()`
  （bool get_use深度Stencil缓冲区（））
- `Shader get_shapeLightShader()`
  （着色器 get_shape光照着色器（））
- `Shader get_shapeLightVolumeShader()`
  （着色器 get_shape光照Volume着色器（））
- `Shader get_pointLightShader()`
  （着色器 get_point光照着色器（））
- `Shader get_pointLightVolumeShader()`
  （着色器 get_point光照Volume着色器（））
- `Shader get_blitShader()`
  （着色器 get_blit着色器（））
- `Shader get_shadowGroupShader()`
  （着色器 get_shadow组着色器（））
- `Shader get_removeSelfShadowShader()`
  （着色器 get_removeSelfShadow着色器（））
- `PostProcessData get_postProcessData()`
  （Post处理数据 get_post处理数据（））
- `TransparencySortMode get_transparencySortMode()`
  （TransparencySort模式 get_transparencySort模式（））
- `Vector3 get_transparencySortAxis()`
  （三维向量 get_transparencySort轴（））
- `ScriptableRenderer Create()`
  （Scriptable渲染器 创建（））
- `void OnEnable()`
  （void 启用时（））
- `Material[] get_shadowMaterials()`
  （Material[] get_shadowMaterials（））
- `void set_shadowMaterials(Material[] value)`
  （void set_shadowMaterials（Material[] value））
- `Material[] get_removeSelfShadowMaterials()`
  （Material[] get_removeSelfShadowMaterials（））
- `void set_removeSelfShadowMaterials(Material[] value)`
  （void set_removeSelfShadowMaterials（Material[] value））
- `ILight2DCullResult get_lightCullResult()`
  （ILight2DCullResult get_lightCullResult（））
- `void set_lightCullResult(ILight2DCullResult value)`
  （void set_lightCullResult（ILight2DCullResult value））

---

## Renderer2DData.Renderer2DDefaultMaterialType（Renderer2DData.Renderer2D默认的材质类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RendererLighting（渲染器Lighting）

### 字段 (33)

- `ProfilingSampler m_ProfilingSampler`（性能分析采样器 m_性能分析采样器）(偏移: 0x0)
- `ShaderTagId k_NormalsRenderingPassName`（着色器标签Id k_NormalsRenderingPass名称）(偏移: 0x4)
- `Color k_NormalClearColor`（颜色 k_法线清除颜色）(偏移: 0x8)
- `string k_SpriteLightKeyword`（string k_精灵光照Keyword）(偏移: 0x18)
- `string k_UsePointLightCookiesKeyword`（string k_UsePoint光照CookiesKeyword）(偏移: 0x1C)
- `string k_LightQualityFastKeyword`（string k_光照QualityFastKeyword）(偏移: 0x20)
- `string k_UseNormalMap`（string k_Use法线映射）(偏移: 0x24)
- `string k_UseAdditiveBlendingKeyword`（string k_UseAdditiveBlendingKeyword）(偏移: 0x28)
- `string[] k_UseBlendStyleKeywords`（string[] k_UseBlendStyleKeywords）(偏移: 0x2C)
- `int[] k_BlendFactorsPropIDs`（int[] k_BlendFactorsPropIDs）(偏移: 0x30)
- `int[] k_MaskFilterPropIDs`（int[] k_掩码FilterPropIDs）(偏移: 0x34)
- `int[] k_InvertedFilterPropIDs`（int[] k_InvertedFilterPropIDs）(偏移: 0x38)
- `GraphicsFormat s_RenderTextureFormatToUse`（Graphics格式化 s_Render纹理格式化ToUse）(偏移: 0x3C)
- `bool s_HasSetupRenderTextureFormatToUse`（bool s_是否有SetupRender纹理格式化ToUse）(偏移: 0x40)
- `int k_SrcBlendID`（int k_SrcBlendID）(偏移: 0x44)
- `int k_DstBlendID`（int k_DstBlendID）(偏移: 0x48)
- `int k_FalloffIntensityID`（int k_FalloffIntensityID）(偏移: 0x4C)
- `int k_FalloffDistanceID`（int k_Falloff距离ID）(偏移: 0x50)
- `int k_FalloffOffsetID`（int k_FalloffOffsetID）(偏移: 0x54)
- `int k_LightColorID`（int k_光照颜色ID）(偏移: 0x58)
- `int k_VolumeOpacityID`（int k_VolumeOpacityID）(偏移: 0x5C)
- `int k_CookieTexID`（int k_CookieTexID）(偏移: 0x60)
- `int k_FalloffLookupID`（int k_FalloffLookupID）(偏移: 0x64)
- `int k_LightPositionID`（int k_光照PositionID）(偏移: 0x68)
- `int k_LightInvMatrixID`（int k_光照Inv矩阵ID）(偏移: 0x6C)
- `int k_LightNoRotInvMatrixID`（int k_光照NoRotInv矩阵ID）(偏移: 0x70)
- `int k_InnerRadiusMultID`（int k_InnerRadiusMultID）(偏移: 0x74)
- `int k_OuterAngleID`（int k_Outer角度ID）(偏移: 0x78)
- `int k_InnerAngleMultID`（int k_Inner角度MultID）(偏移: 0x7C)
- `int k_LightLookupID`（int k_光照LookupID）(偏移: 0x80)
- `int k_IsFullSpotlightID`（int k_是否满SpotlightID）(偏移: 0x84)
- `int k_LightZDistanceID`（int k_光照Z距离ID）(偏移: 0x88)
- `int k_PointLightCookieTexID`（int k_Point光照CookieTexID）(偏移: 0x8C)

### 方法 (20)

- `GraphicsFormat GetRenderTextureFormat()`
  （Graphics格式化 获取Render纹理格式化（））
- `void CreateNormalMapRenderTexture(IRenderPass2D pass, RenderingData renderingData, CommandBuffer cmd)`
  （void 创建法线映射Render纹理（IRenderPass2D pass, Rendering数据 renderingData, Command缓冲区 cmd））
- `void CreateBlendStyleRenderTexture(IRenderPass2D pass, RenderingData renderingData, CommandBuffer cmd, int blendStyleIndex)`
  （void 创建BlendStyleRender纹理（IRenderPass2D pass, Rendering数据 renderingData, Command缓冲区 cmd, int blendStyleIndex））
- `void EnableBlendStyle(CommandBuffer cmd, int blendStyleIndex, bool enabled)`
  （void 启用BlendStyle（Command缓冲区 cmd, int blendStyleIndex, bool enabled））
- `void ReleaseRenderTextures(IRenderPass2D pass, CommandBuffer cmd)`
  （void ReleaseRenderTextures（IRenderPass2D pass, Command缓冲区 cmd））
- `bool RenderLightSet(IRenderPass2D pass, RenderingData renderingData, int blendStyleIndex, CommandBuffer cmd, int layerToRender, RenderTargetIdentifier renderTexture, bool rtNeedsClear, Color clearColor, List<Light2D> lights)`
  （bool Render光照集合（IRenderPass2D pass, Rendering数据 renderingData, int blendStyleIndex, Command缓冲区 cmd, int layerToRender, Render目标Identifier renderTexture, bool rtNeedsClear, 颜色 clearColor, List<Light2D> lights））
- `void RenderLightVolumeSet(IRenderPass2D pass, RenderingData renderingData, int blendStyleIndex, CommandBuffer cmd, int layerToRender, RenderTargetIdentifier renderTexture, RenderTargetIdentifier depthTexture, List<Light2D> lights)`
  （void Render光照Volume集合（IRenderPass2D pass, Rendering数据 renderingData, int blendStyleIndex, Command缓冲区 cmd, int layerToRender, Render目标Identifier renderTexture, Render目标Identifier depthTexture, List<Light2D> lights））
- `void SetShapeLightShaderGlobals(IRenderPass2D pass, CommandBuffer cmd)`
  （void 集合Shape光照着色器Globals（IRenderPass2D pass, Command缓冲区 cmd））
- `float GetNormalizedInnerRadius(Light2D light)`
  （float 获取NormalizedInnerRadius（Light2D light））
- `float GetNormalizedAngle(float angle)`
  （float 获取Normalized角度（float angle））
- `void GetScaledLightInvMatrix(Light2D light, out Matrix4x4 retMatrix, bool includeRotation)`
  （void 获取Scaled光照Inv矩阵（Light2D light, out Matrix4x4 retMatrix, bool includeRotation））
- `void SetPointLightShaderGlobals(CommandBuffer cmd, Light2D light)`
  （void 集合Point光照着色器Globals（Command缓冲区 cmd, Light2D light））
- `void ClearDirtyLighting(IRenderPass2D pass, CommandBuffer cmd, uint blendStylesUsed)`
  （void 清除DirtyLighting（IRenderPass2D pass, Command缓冲区 cmd, uint blendStylesUsed））
- `void RenderNormals(IRenderPass2D pass, ScriptableRenderContext context, CullingResults cullResults, DrawingSettings drawSettings, FilteringSettings filterSettings, RenderTargetIdentifier depthTarget)`
  （void RenderNormals（IRenderPass2D pass, ScriptableRenderContext context, CullingResults cullResults, DrawingSettings drawSettings, FilteringSettings filterSettings, Render目标Identifier depthTarget））
- `void RenderLights(IRenderPass2D pass, RenderingData renderingData, CommandBuffer cmd, int layerToRender, uint blendStylesUsed)`
  （void RenderLights（IRenderPass2D pass, Rendering数据 renderingData, Command缓冲区 cmd, int layerToRender, uint blendStylesUsed））
- `void RenderLightVolumes(IRenderPass2D pass, RenderingData renderingData, CommandBuffer cmd, int layerToRender, RenderTargetIdentifier renderTarget, RenderTargetIdentifier depthTarget, uint blendStylesUsed)`
  （void Render光照Volumes（IRenderPass2D pass, Rendering数据 renderingData, Command缓冲区 cmd, int layerToRender, Render目标Identifier renderTarget, Render目标Identifier depthTarget, uint blendStylesUsed））
- `void SetBlendModes(Material material, BlendMode src, BlendMode dst)`
  （void 集合BlendModes（材质 material, Blend模式 src, Blend模式 dst））
- `uint GetLightMaterialIndex(Light2D light, bool isVolume)`
  （uint 获取光照材质索引（Light2D light, bool isVolume））
- `Material CreateLightMaterial(Renderer2DData rendererData, Light2D light, bool isVolume)`
  （材质 创建光照材质（Renderer2D数据 rendererData, Light2D light, bool isVolume））
- `Material GetLightMaterial(Renderer2DData rendererData, Light2D light, bool isVolume)`
  （材质 获取光照材质（Renderer2D数据 rendererData, Light2D light, bool isVolume））

---

## RendererList（渲染器列表）

### 字段 (6)

- `ShaderTagId s_EmptyName`（着色器标签Id s_空名称）(偏移: 0x0)
- `RendererList nullRendererList`（渲染器列表 null渲染器列表）(偏移: 0x4)
- `CullingResults cullingResult`（CullingResults cullingResult）(偏移: 0x4)
- `DrawingSettings drawSettings`（DrawingSettings drawSettings）(偏移: 0xC)
- `FilteringSettings filteringSettings`（FilteringSettings filteringSettings）(偏移: 0x144)
- `Nullable<RenderStateBlock> stateBlock`（Nullable<Render状态Block> stateBlock）(偏移: 0x15C)

### 方法 (3)

- `bool get_isValid()`
  （布尔值 获取_是否有效（））
- `void set_isValid(bool value)`
  （void set_isValid（bool value））
- `RendererList Create(in RendererListDesc desc)`
  （渲染器列表 创建（in RendererListDesc desc））

---

## RendererListDesc（渲染器列表Desc）

### 字段 (8)

- `SortingCriteria sortingCriteria`（SortingCriteria sortingCriteria）(偏移: 0x0)
- `PerObjectData rendererConfiguration`（Per对象数据 rendererConfiguration）(偏移: 0x4)
- `RenderQueueRange renderQueueRange`（Render队列范围 render队列范围）(偏移: 0x8)
- `Nullable<RenderStateBlock> stateBlock`（Nullable<Render状态Block> stateBlock）(偏移: 0x10)
- `Material overrideMaterial`（材质 override材质）(偏移: 0x80)
- `bool excludeObjectMotionVectors`（bool exclude对象MotionVectors）(偏移: 0x84)
- `int layerMask`（int layer掩码）(偏移: 0x88)
- `int overrideMaterialPassIndex`（int override材质Pass索引）(偏移: 0x8C)

### 方法 (9)

- `CullingResults get_cullingResult()`
  （CullingResults get_cullingResult（））
- `void set_cullingResult(CullingResults value)`
  （void set_cullingResult（CullingResults value））
- `Camera get_camera()`
  （摄像机 get_camera（））
- `void set_camera(Camera value)`
  （void set_camera（摄像机 value））
- `ShaderTagId get_passName()`
  （着色器标签Id get_pass名称（））
- `void set_passName(ShaderTagId value)`
  （void set_pass名称（着色器标签Id value））
- `ShaderTagId[] get_passNames()`
  （着色器标签Id[] get_passNames（））
- `void set_passNames(ShaderTagId[] value)`
  （void set_passNames（着色器标签Id[] value））
- `bool IsValid()`
  （布尔值 是否有效（））

---

## RendererListHandle（渲染器列表句柄）

### 字段 (1)

- `bool m_IsValid`（bool m_是否Valid）(偏移: 0x0)

### 方法 (5)

- `int get_handle()`
  （int get_handle（））
- `void set_handle(int value)`
  （void set_handle（int value））
- `int op_Implicit(RendererListHandle handle)`
  （int op_Implicit（渲染器列表句柄 handle））
- `RendererList op_Implicit(RendererListHandle rendererList)`
  （渲染器列表 op_Implicit（渲染器列表句柄 rendererList））
- `bool IsValid()`
  （布尔值 是否有效（））

---

## RendererOverrideOption（渲染器重写Option）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RendererType（渲染器类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RenderingData（Rendering数据）

### 字段 (8)

- `CullingResults cullResults`（CullingResults cullResults）(偏移: 0x0)
- `CameraData cameraData`（摄像机数据 camera数据）(偏移: 0x8)
- `LightData lightData`（光照数据 light数据）(偏移: 0x12C)
- `ShadowData shadowData`（Shadow数据 shadow数据）(偏移: 0x148)
- `PostProcessingData postProcessingData`（PostProcessing数据 postProcessing数据）(偏移: 0x17C)
- `bool supportsDynamicBatching`（bool supports动态的Batching）(偏移: 0x184)
- `PerObjectData perObjectData`（Per对象数据 per对象数据）(偏移: 0x188)
- `bool postProcessingEnabled`（bool postProcessing启用的）(偏移: 0x18C)

---

## RenderingMode（Rendering模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RenderingPath（Rendering路径）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## RenderingUtils（RenderingUtils）

### 字段 (13)

- `List<ShaderTagId> m_LegacyShaderPassNames`（List<着色器标签Id> m_Legacy着色器PassNames）(偏移: 0x0)
- `Mesh s_FullscreenMesh`（网格 s_Fullscreen网格）(偏移: 0x4)
- `Material s_ErrorMaterial`（材质 s_Error材质）(偏移: 0x8)
- `int UNITY_STEREO_MATRIX_V`（int UNITY_STEREO_MATRIX_V）(偏移: 0xC)
- `int UNITY_STEREO_MATRIX_IV`（int UNITY_STEREO_MATRIX_IV）(偏移: 0x10)
- `int UNITY_STEREO_MATRIX_P`（int UNITY_STEREO_MATRIX_P）(偏移: 0x14)
- `int UNITY_STEREO_MATRIX_IP`（int UNITY_STEREO_MATRIX_IP）(偏移: 0x18)
- `int UNITY_STEREO_MATRIX_VP`（int UNITY_STEREO_MATRIX_VP）(偏移: 0x1C)
- `int UNITY_STEREO_MATRIX_IVP`（int UNITY_STEREO_MATRIX_IVP）(偏移: 0x20)
- `int UNITY_STEREO_CAMERA_PROJECTION`（int UNITY_STEREO_CAMERA_PROJECTION）(偏移: 0x24)
- `int UNITY_STEREO_CAMERA_INV_PROJECTION`（int UNITY_STEREO_CAMERA_INV_PROJECTION）(偏移: 0x28)
- `int UNITY_STEREO_VECTOR_CAMPOS`（int UNITY_STEREO_VECTOR_CAMPOS）(偏移: 0x2C)
- `RenderingUtils.StereoConstants stereoConstants`（RenderingUtils.StereoConstants stereoConstants）(偏移: 0x30)

### 方法 (19)

- `Mesh get_fullscreenMesh()`
  （网格 get_fullscreen网格（））
- `bool get_useStructuredBuffer()`
  （bool get_useStructured缓冲区（））
- `Material get_errorMaterial()`
  （材质 get_error材质（））
- `void SetViewAndProjectionMatrices(CommandBuffer cmd, Matrix4x4 viewMatrix, Matrix4x4 projectionMatrix, bool setInverseMatrices)`
  （void 集合视图AndProjectionMatrices（Command缓冲区 cmd, Matrix4x4 viewMatrix, Matrix4x4 projectionMatrix, bool setInverseMatrices））
- `void SetStereoViewAndProjectionMatrices(CommandBuffer cmd, Matrix4x4[] viewMatrix, Matrix4x4[] projMatrix, Matrix4x4[] cameraProjMatrix, bool setInverseMatrices)`
  （void 集合Stereo视图AndProjectionMatrices（Command缓冲区 cmd, Matrix4x4[] viewMatrix, Matrix4x4[] projMatrix, Matrix4x4[] cameraProjMatrix, bool setInverseMatrices））
- `void Blit(CommandBuffer cmd, RenderTargetIdentifier source, RenderTargetIdentifier destination, Material material, int passIndex = 0, bool useDrawProcedural = False, RenderBufferLoadAction colorLoadAction = 0, RenderBufferStoreAction colorStoreAction = 0, RenderBufferLoadAction depthLoadAction = 0, RenderBufferStoreAction depthStoreAction = 0)`
  （void Blit（Command缓冲区 cmd, Render目标Identifier source, Render目标Identifier destination, 材质 material, int passIndex = 0, bool useDrawProcedural = False, Render缓冲区加载动作 colorLoadAction = 0, Render缓冲区商店动作 colorStoreAction = 0, Render缓冲区加载动作 depthLoadAction = 0, Render缓冲区商店动作 depthStoreAction = 0））
- `void RenderObjectsWithError(ScriptableRenderContext context, ref CullingResults cullResults, Camera camera, FilteringSettings filterSettings, SortingCriteria sortFlags)`
  （void RenderObjectsWithError（ScriptableRenderContext context, ref CullingResults cullResults, 摄像机 camera, FilteringSettings filterSettings, SortingCriteria sortFlags））
- `void ClearSystemInfoCache()`
  （void 清除系统信息缓存（））
- `bool SupportsRenderTextureFormat(RenderTextureFormat format)`
  （bool SupportsRender纹理格式化（Render纹理格式化 format））
- `bool SupportsGraphicsFormat(GraphicsFormat format, FormatUsage usage)`
  （bool SupportsGraphics格式化（Graphics格式化 format, 格式化Usage usage））
- `int GetLastValidColorBufferIndex(RenderTargetIdentifier[] colorBuffers)`
  （int 获取最后一个Valid颜色缓冲区索引（Render目标Identifier[] colorBuffers））
- `uint GetValidColorBufferCount(RenderTargetIdentifier[] colorBuffers)`
  （uint 获取Valid颜色缓冲区数量（Render目标Identifier[] colorBuffers））
- `bool IsMRT(RenderTargetIdentifier[] colorBuffers)`
  （bool 是否MRT（Render目标Identifier[] colorBuffers））
- `bool Contains(RenderTargetIdentifier[] source, RenderTargetIdentifier value)`
  （bool Contains（Render目标Identifier[] source, Render目标Identifier value））
- `int IndexOf(RenderTargetIdentifier[] source, RenderTargetIdentifier value)`
  （int 索引Of（Render目标Identifier[] source, Render目标Identifier value））
- `uint CountDistinct(RenderTargetIdentifier[] source, RenderTargetIdentifier value)`
  （uint 数量Distinct（Render目标Identifier[] source, Render目标Identifier value））
- `int LastValid(RenderTargetIdentifier[] source)`
  （int 最后一个Valid（Render目标Identifier[] source））
- `bool Contains(ClearFlag a, ClearFlag b)`
  （bool Contains（清除标志 a, 清除标志 b））
- `bool SequenceEqual(RenderTargetIdentifier[] left, RenderTargetIdentifier[] right)`
  （bool SequenceEqual（Render目标Identifier[] left, Render目标Identifier[] right））

---

## RenderingUtils.StereoConstants（RenderingUtils.StereoConstants）

### 字段 (6)

- `Matrix4x4[] viewProjMatrix`（Matrix4x4[] viewProj矩阵）(偏移: 0x8)
- `Matrix4x4[] invViewMatrix`（Matrix4x4[] inv视图矩阵）(偏移: 0xC)
- `Matrix4x4[] invProjMatrix`（Matrix4x4[] invProj矩阵）(偏移: 0x10)
- `Matrix4x4[] invViewProjMatrix`（Matrix4x4[] inv视图Proj矩阵）(偏移: 0x14)
- `Matrix4x4[] invCameraProjMatrix`（Matrix4x4[] inv摄像机Proj矩阵）(偏移: 0x18)
- `Vector4[] worldSpaceCameraPos`（Vector4[] worldSpace摄像机Pos）(偏移: 0x1C)

---

## RepeatFireData（Repeat开火数据）

**继承**: ComponentDataBase（组件数据基础）

### 字段 (3)

- `bool triggerMode`（bool trigger模式）(偏移: 0xC)
- `float coldTime`（float cold时间）(偏移: 0x10)
- `float shootInterval`（float shoot间隔）(偏移: 0x14)

---

## RequireComponent（Require组件）

**继承**: Attribute（属性）

### 字段 (3)

- `Type m_Type0`（类型 m_Type0）(偏移: 0x8)
- `Type m_Type1`（类型 m_Type1）(偏移: 0xC)
- `Type m_Type2`（类型 m_Type2）(偏移: 0x10)

---

## RequiredByNativeCodeAttribute（RequiredByNativeCodeAttribute）

**继承**: Attribute（属性）

### 方法 (3)

- `void set_Name(string value)`
  （void 设置_名称（字符串 value））
- `void set_Optional(bool value)`
  （void set_Optional（bool value））
- `void set_GenerateProxy(bool value)`
  （void set_Generate代理（bool value））

---

## RequiredReferences（RequiredReferences）

**继承**: ScriptableObject（脚本对象）

### 字段 (3)

- `GameObject _gameObject`（游戏对象 _game对象）(偏移: 0xC)
- `Material _material`（材质 _material）(偏移: 0x10)
- `AudioClip _audioClip`（音频弹匣 _audio弹匣）(偏移: 0x14)

---

## Resolution（Resolution）

### 字段 (3)

- `int m_Width`（int m_宽度）(偏移: 0x0)
- `int m_Height`（int m_高度）(偏移: 0x4)
- `int m_RefreshRate`（int m_刷新Rate）(偏移: 0x8)

### 方法 (3)

- `int get_width()`
  （整数 获取_宽度（））
- `int get_height()`
  （整数 获取_高度（））
- `string ToString()`
  （字符串 转字符串（））

---

## ResolveEventArgs（Resolve事件Args）

**继承**: EventArgs（事件参数）

### 字段 (2)

- `string m_Name`（字符串 m_名称）(偏移: 0x8)
- `Assembly m_Requesting`（Assembly m_Requesting）(偏移: 0xC)

---

## ResolveEventHandler（Resolve事件处理器）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `Assembly Invoke(object sender, ResolveEventArgs args)`
  （Assembly Invoke（object sender, Resolve事件Args args））
- `IAsyncResult BeginInvoke(object sender, ResolveEventArgs args, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（object sender, Resolve事件Args args, 异步回调 callback, object object））
- `Assembly EndInvoke(IAsyncResult result)`
  （Assembly 结束Invoke（I异步Result result））

---

## ResourceFallbackManager（资源Fallback管理器）

**继承**: IEnumerable<CultureInfo>, IEnumerable（IEnumerable<CultureInfo>, IEnumerable）

### 字段 (3)

- `CultureInfo m_startingCulture`（Culture信息 m_startingCulture）(偏移: 0x8)
- `CultureInfo m_neutralResourcesCulture`（Culture信息 m_neutralResourcesCulture）(偏移: 0xC)
- `bool m_useParents`（bool m_useParents）(偏移: 0x10)

### 方法 (1)

- `IEnumerator<CultureInfo> GetEnumerator()`
  （IEnumerator<CultureInfo> 获取Enumerator（））

---

## ResourceHandle（资源句柄）

### 字段 (2)

- `uint m_Value`（uint m_值）(偏移: 0x0)
- `uint s_CurrentValidBit`（uint s_当前ValidBit）(偏移: 0x0)

### 方法 (7)

- `int get_index()`
  （int get_index（））
- `RenderGraphResourceType get_type()`
  （RenderGraph资源类型 get_type（））
- `void set_type(RenderGraphResourceType value)`
  （void set_type（RenderGraph资源类型 value））
- `int get_iType()`
  （int get_i类型（））
- `int op_Implicit(ResourceHandle handle)`
  （int op_Implicit（资源句柄 handle））
- `bool IsValid()`
  （布尔值 是否有效（））
- `void NewFrame(int executionIndex)`
  （void 新的Frame（int executionIndex））

---

## ResourceLocation（资源Location）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ResourceLocator（资源Locator）

### 字段 (2)

- `object _value`（object _value）(偏移: 0x0)
- `int _dataPos`（int _dataPos）(偏移: 0x4)

### 方法 (4)

- `int get_DataPosition()`
  （int get_数据Position（））
- `object get_Value()`
  （对象 获取_值（））
- `void set_Value(object value)`
  （void set_值（object value））
- `bool CanCache(ResourceTypeCode value)`
  （bool 能否缓存（资源类型Code value））

---

## ResourceManager（资源管理器）

### 字段 (24)

- `string BaseNameField`（string 基础名称Field）(偏移: 0x8)
- `Hashtable ResourceSets`（Hashtable 资源Sets）(偏移: 0xC)
- `string moduleDir`（string moduleDir）(偏移: 0x14)
- `Assembly MainAssembly`（Assembly 主要的Assembly）(偏移: 0x18)
- `Type _locationInfo`（类型 _location信息）(偏移: 0x1C)
- `Type _userResourceSet`（类型 _user资源集合）(偏移: 0x20)
- `CultureInfo _neutralResourcesCulture`（Culture信息 _neutralResourcesCulture）(偏移: 0x24)
- `ResourceManager.CultureNameResourceSetPair _lastUsedResourceCache`（资源Manager.Culture名称资源集合Pair _lastUsed资源缓存）(偏移: 0x28)
- `bool _ignoreCase`（bool _ignoreCase）(偏移: 0x2C)
- `bool UseManifest`（bool UseManifest）(偏移: 0x2D)
- `bool UseSatelliteAssem`（bool UseSatelliteAssem）(偏移: 0x2E)
- `UltimateResourceFallbackLocation _fallbackLoc`（Ultimate资源FallbackLocation _fallbackLoc）(偏移: 0x30)
- `Version _satelliteContractVersion`（Version _satelliteContractVersion）(偏移: 0x34)
- `bool _lookedForSatelliteContractVersion`（bool _lookedForSatelliteContractVersion）(偏移: 0x38)
- `Assembly _callingAssembly`（Assembly _callingAssembly）(偏移: 0x3C)
- `RuntimeAssembly m_callingAssembly`（RuntimeAssembly m_callingAssembly）(偏移: 0x40)
- `IResourceGroveler resourceGroveler`（I资源Groveler resourceGroveler）(偏移: 0x44)
- `int MagicNumber`（int MagicNumber）(偏移: 0x0)
- `int HeaderVersionNumber`（int 标题VersionNumber）(偏移: 0x4)
- `Type _minResourceSet`（类型 _min资源集合）(偏移: 0x8)
- `string ResReaderTypeName`（string Res读取器类型名称）(偏移: 0xC)
- `string ResSetTypeName`（string Res集合类型名称）(偏移: 0x10)
- `string MscorlibName`（string Mscorlib名称）(偏移: 0x14)
- `int DEBUG`（int DEBUG）(偏移: 0x18)

### 方法 (17)

- `void Init()`
  （void 初始化（））
- `void OnDeserializing(StreamingContext ctx)`
  （void 反序列化中（流上下文 ctx））
- `void OnDeserialized(StreamingContext ctx)`
  （void 反序列化后（流上下文 ctx））
- `void OnSerializing(StreamingContext ctx)`
  （void 序列化中（流上下文 ctx））
- `void CommonAssemblyInit()`
  （void CommonAssembly初始化（））
- `string get_BaseName()`
  （string get_基础名称（））
- `UltimateResourceFallbackLocation get_FallbackLocation()`
  （Ultimate资源FallbackLocation get_FallbackLocation（））
- `string GetResourceFileName(CultureInfo culture)`
  （string 获取资源文件名称（Culture信息 culture））
- `ResourceSet GetFirstResourceSet(CultureInfo culture)`
  （资源集合 获取第一个资源集合（Culture信息 culture））
- `ResourceSet GetResourceSet(CultureInfo culture, bool createIfNotExists, bool tryParents)`
  （资源集合 获取资源集合（Culture信息 culture, bool createIfNotExists, bool tryParents））
- `ResourceSet InternalGetResourceSet(CultureInfo culture, bool createIfNotExists, bool tryParents)`
  （资源集合 内部的获取资源集合（Culture信息 culture, bool createIfNotExists, bool tryParents））
- `ResourceSet InternalGetResourceSet(CultureInfo requestedCulture, bool createIfNotExists, bool tryParents, ref StackCrawlMark stackMark)`
  （资源集合 内部的获取资源集合（Culture信息 requestedCulture, bool createIfNotExists, bool tryParents, ref StackCrawlMark stackMark））
- `void AddResourceSet(Dictionary<string, ResourceSet> localResourceSets, string cultureName, ref ResourceSet rs)`
  （void 添加资源集合（Dictionary<string, 资源Set> localResourceSets, string cultureName, ref ResourceSet rs））
- `Version GetSatelliteContractVersion(Assembly a)`
  （Version 获取SatelliteContractVersion（Assembly a））
- `bool CompareNames(string asmTypeName1, string typeName2, AssemblyName asmName2)`
  （bool CompareNames（string asmTypeName1, string typeName2, Assembly名称 asmName2））
- `void SetAppXConfiguration()`
  （void 集合AppXConfiguration（））
- `string GetString(string name, CultureInfo culture)`
  （string 获取字符串（string name, Culture信息 culture））

---

## ResourceManager.CultureNameResourceSetPair（资源Manager.Culture名称资源集合Pair）

### 字段 (2)

- `string lastCultureName`（string lastCulture名称）(偏移: 0x8)
- `ResourceSet lastResourceSet`（资源集合 last资源集合）(偏移: 0xC)

---

## ResourceManager.ResourceManagerMediator（资源Manager.资源管理器Mediator）

### 字段 (1)

- `ResourceManager _rm`（资源管理器 _rm）(偏移: 0x8)

### 方法 (15)

- `string get_ModuleDir()`
  （string get_模块Dir（））
- `Type get_LocationInfo()`
  （类型 get_Location信息（））
- `Type get_UserResourceSet()`
  （类型 get_User资源集合（））
- `string get_BaseNameField()`
  （string get_基础名称Field（））
- `CultureInfo get_NeutralResourcesCulture()`
  （Culture信息 get_NeutralResourcesCulture（））
- `string GetResourceFileName(CultureInfo culture)`
  （string 获取资源文件名称（Culture信息 culture））
- `bool get_LookedForSatelliteContractVersion()`
  （bool get_LookedForSatelliteContractVersion（））
- `void set_LookedForSatelliteContractVersion(bool value)`
  （void set_LookedForSatelliteContractVersion（bool value））
- `Version get_SatelliteContractVersion()`
  （Version get_SatelliteContractVersion（））
- `void set_SatelliteContractVersion(Version value)`
  （void set_SatelliteContractVersion（Version value））
- `Version ObtainSatelliteContractVersion(Assembly a)`
  （Version ObtainSatelliteContractVersion（Assembly a））
- `UltimateResourceFallbackLocation get_FallbackLoc()`
  （Ultimate资源FallbackLocation get_FallbackLoc（））
- `RuntimeAssembly get_CallingAssembly()`
  （RuntimeAssembly get_CallingAssembly（））
- `RuntimeAssembly get_MainAssembly()`
  （RuntimeAssembly get_主要的Assembly（））
- `string get_BaseName()`
  （string get_基础名称（））

---

