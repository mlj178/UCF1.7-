# 游戏类定义 (Part 15/21)

共 200 个类 (总序号 2801 - 3000)

---

## ResourceReader（资源读取器）

**继承**: IResourceReader, IEnumerable, IDisposable（I资源读取器, IEnumerable, IDisposable）

### 字段 (13)

- `BinaryReader _store`（Binary读取器 _store）(偏移: 0x8)
- `long _nameSectionOffset`（long _nameSectionOffset）(偏移: 0x10)
- `long _dataSectionOffset`（long _dataSectionOffset）(偏移: 0x18)
- `int[] _nameHashes`（int[] _nameHashes）(偏移: 0x20)
- `int* _nameHashesPtr`（int* _nameHashesPtr）(偏移: 0x24)
- `int[] _namePositions`（int[] _namePositions）(偏移: 0x28)
- `int* _namePositionsPtr`（int* _namePositionsPtr）(偏移: 0x2C)
- `RuntimeType[] _typeTable`（RuntimeType[] _typeTable）(偏移: 0x30)
- `int[] _typeNamePositions`（int[] _type名称Positions）(偏移: 0x34)
- `BinaryFormatter _objFormatter`（BinaryFormatter _objFormatter）(偏移: 0x38)
- `int _numResources`（int _numResources）(偏移: 0x3C)
- `UnmanagedMemoryStream _ums`（UnmanagedMemory流 _ums）(偏移: 0x40)
- `int _version`（int _version）(偏移: 0x44)

### 方法 (24)

- `void Close()`
  （void 关闭（））
- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））
- `int ReadUnalignedI4(int* p)`
  （int ReadUnalignedI4（int* p））
- `void SkipString()`
  （void Skip字符串（））
- `int GetNameHash(int index)`
  （int 获取名称Hash（int index））
- `int GetNamePosition(int index)`
  （int 获取名称Position（int index））
- `IDictionaryEnumerator GetEnumerator()`
  （I字典Enumerator 获取Enumerator（））
- `ResourceReader.ResourceEnumerator GetEnumeratorInternal()`
  （资源Reader.资源Enumerator 获取Enumerator内部的（））
- `int FindPosForResource(string name)`
  （int 查找PosFor资源（string name））
- `bool CompareStringEqualsName(string name)`
  （bool Compare字符串Equals名称（string name））
- `string AllocateStringForNameIndex(int index, out int dataOffset)`
  （string Allocate字符串For名称索引（int index, out int dataOffset））
- `object GetValueForNameIndex(int index)`
  （object 获取值For名称索引（int index））
- `string LoadString(int pos)`
  （string 加载字符串（int pos））
- `object LoadObject(int pos)`
  （object 加载对象（int pos））
- `object LoadObject(int pos, out ResourceTypeCode typeCode)`
  （object 加载对象（int pos, out ResourceTypeCode typeCode））
- `object LoadObjectV1(int pos)`
  （object 加载对象V1（int pos））
- `object _LoadObjectV1(int pos)`
  （object _加载对象V1（int pos））
- `object LoadObjectV2(int pos, out ResourceTypeCode typeCode)`
  （object 加载对象V2（int pos, out ResourceTypeCode typeCode））
- `object _LoadObjectV2(int pos, out ResourceTypeCode typeCode)`
  （object _加载对象V2（int pos, out ResourceTypeCode typeCode））
- `object DeserializeObject(int typeIndex)`
  （object Deserialize对象（int typeIndex））
- `void ReadResources()`
  （void ReadResources（））
- `void _ReadResources()`
  （void _ReadResources（））
- `RuntimeType FindType(int typeIndex)`
  （Runtime类型 查找类型（int typeIndex））

---

## ResourceReader.ResourceEnumerator（资源Reader.资源Enumerator）

**继承**: IDictionaryEnumerator, IEnumerator（I字典Enumerator, IEnumerator）

### 字段 (4)

- `ResourceReader _reader`（资源读取器 _reader）(偏移: 0x8)
- `bool _currentIsValid`（bool _current是否Valid）(偏移: 0xC)
- `int _currentName`（int _current名称）(偏移: 0x10)
- `int _dataPosition`（int _dataPosition）(偏移: 0x14)

### 方法 (7)

- `bool MoveNext()`
  （bool 移动下一个（））
- `object get_Key()`
  （object get_键（））
- `object get_Current()`
  （object get_当前（））
- `int get_DataPosition()`
  （int get_数据Position（））
- `DictionaryEntry get_Entry()`
  （字典Entry get_Entry（））
- `object get_Value()`
  （object get_值（））
- `void Reset()`
  （void 重置（））

---

## ResourceRequest（资源请求）

**继承**: AsyncOperation（异步Operation）

### 字段 (2)

- `string m_Path`（string m_路径）(偏移: 0x10)
- `Type m_Type`（类型 m_类型）(偏移: 0x14)

---

## ResourceSet（资源集合）

**继承**: IDisposable, IEnumerable（IDisposable, IEnumerable）

### 字段 (3)

- `IResourceReader Reader`（I资源读取器 读取器）(偏移: 0x8)
- `Hashtable Table`（Hashtable Table）(偏移: 0xC)
- `Hashtable _caseInsensitiveTable`（Hashtable _caseInsensitiveTable）(偏移: 0x10)

### 方法 (11)

- `void CommonInit()`
  （void Common初始化（））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））
- `void Dispose()`
  （void 释放（））
- `IDictionaryEnumerator GetEnumerator()`
  （I字典Enumerator 获取Enumerator（））
- `IDictionaryEnumerator GetEnumeratorHelper()`
  （I字典Enumerator 获取Enumerator辅助器（））
- `string GetString(string name)`
  （string 获取字符串（string name））
- `string GetString(string name, bool ignoreCase)`
  （string 获取字符串（string name, bool ignoreCase））
- `object GetObject(string name)`
  （object 获取对象（string name））
- `object GetObject(string name, bool ignoreCase)`
  （object 获取对象（string name, bool ignoreCase））
- `object GetObjectInternal(string name)`
  （object 获取对象内部的（string name））
- `object GetCaseInsensitiveObjectInternal(string name)`
  （object 获取CaseInsensitive对象内部的（string name））

---

## ResourceTypeCode（资源类型Code）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Resources（Resources）

### 方法 (4)

- `Object Load(string path)`
  （对象 加载（string path））
- `Object Load(string path, Type systemTypeInstance)`
  （对象 加载（string path, 类型 systemTypeInstance））
- `Object[] LoadAll(string path, Type systemTypeInstance)`
  （Object[] 加载所有（string path, 类型 systemTypeInstance））
- `Object GetBuiltinResource(Type type, string path)`
  （对象 获取Builtin资源（类型 type, string path））

---

## ResourcesAPI（ResourcesAPI）

### 字段 (1)

- `ResourcesAPI s_DefaultAPI`（ResourcesAPI s_默认的API）(偏移: 0x0)

### 方法 (5)

- `ResourcesAPI get_ActiveAPI()`
  （ResourcesAPI get_激活的API（））
- `ResourcesAPI get_overrideAPI()`
  （ResourcesAPI get_overrideAPI（））
- `Shader FindShaderByName(string name)`
  （着色器 查找着色器By名称（string name））
- `Object Load(string path, Type systemTypeInstance)`
  （对象 加载（string path, 类型 systemTypeInstance））
- `Object[] LoadAll(string path, Type systemTypeInstance)`
  （Object[] 加载所有（string path, 类型 systemTypeInstance））

---

## ResourcesAPIInternal（ResourcesAPI内部的）

### 方法 (3)

- `Shader FindShaderByName(string name)`
  （着色器 查找着色器By名称（string name））
- `Object Load(string path, Type systemTypeInstance)`
  （对象 加载（string path, 类型 systemTypeInstance））
- `Object[] LoadAll(string path, Type systemTypeInstance)`
  （Object[] 加载所有（string path, 类型 systemTypeInstance））

---

## RetainedGizmos（RetainedGizmos）

### 字段 (6)

- `List<RetainedGizmos.MeshWithHash> meshes`（List<RetainedGizmos.网格WithHash> meshes）(偏移: 0x8)
- `HashSet<ulong> usedHashes`（HashSet<ulong> usedHashes）(偏移: 0xC)
- `HashSet<ulong> existingHashes`（HashSet<ulong> existingHashes）(偏移: 0x10)
- `Stack<Mesh> cachedMeshes`（Stack<Mesh> cachedMeshes）(偏移: 0x14)
- `Material surfaceMaterial`（材质 surface材质）(偏移: 0x18)
- `Material lineMaterial`（材质 line材质）(偏移: 0x1C)

### 方法 (10)

- `GraphGizmoHelper GetSingleFrameGizmoHelper(AstarPath active)`
  （GraphGizmo辅助器 获取单个FrameGizmo辅助器（Astar路径 active））
- `GraphGizmoHelper GetGizmoHelper(AstarPath active, RetainedGizmos.Hasher hasher)`
  （GraphGizmo辅助器 获取Gizmo辅助器（Astar路径 active, RetainedGizmos.Hasher hasher））
- `void PoolMesh(Mesh mesh)`
  （void 池网格（网格 mesh））
- `Mesh GetMesh()`
  （网格 获取网格（））
- `bool HasCachedMesh(RetainedGizmos.Hasher hasher)`
  （bool 是否有Cached网格（RetainedGizmos.Hasher hasher））
- `bool Draw(RetainedGizmos.Hasher hasher)`
  （bool Draw（RetainedGizmos.Hasher hasher））
- `void DrawExisting()`
  （void DrawExisting（））
- `void FinalizeDraw()`
  （void FinalizeDraw（））
- `void ClearCache()`
  （void 清除缓存（））
- `void RemoveUnusedMeshes(List<RetainedGizmos.MeshWithHash> meshList)`
  （void 移除UnusedMeshes（List<RetainedGizmos.网格WithHash> meshList））

---

## RetainedGizmos.Builder（RetainedGizmos.构建器）

**继承**: IAstarPooledObject（IAstarPooled对象）

### 字段 (3)

- `List<Vector3> lines`（List<Vector3> lines）(偏移: 0x8)
- `List<Color32> lineColors`（List<Color32> lineColors）(偏移: 0xC)
- `List<Mesh> meshes`（List<Mesh> meshes）(偏移: 0x10)

### 方法 (6)

- `void DrawMesh(RetainedGizmos gizmos, Vector3[] vertices, List<int> triangles, Color[] colors)`
  （void Draw网格（RetainedGizmos gizmos, Vector3[] vertices, List<int> triangles, Color[] colors））
- `void DrawWireCube(GraphTransform tr, Bounds bounds, Color color)`
  （void DrawWireCube（Graph变换 tr, Bounds bounds, 颜色 color））
- `void DrawLine(Vector3 start, Vector3 end, Color color)`
  （void DrawLine（三维向量 start, 三维向量 end, 颜色 color））
- `void Submit(RetainedGizmos gizmos, RetainedGizmos.Hasher hasher)`
  （void Submit（RetainedGizmos gizmos, RetainedGizmos.Hasher hasher））
- `void SubmitMeshes(RetainedGizmos gizmos, ulong hash)`
  （void SubmitMeshes（RetainedGizmos gizmos, ulong hash））
- `void SubmitLines(RetainedGizmos gizmos, ulong hash)`
  （void SubmitLines（RetainedGizmos gizmos, ulong hash））

---

## RetainedGizmos.Hasher（RetainedGizmos.Hasher）

### 字段 (4)

- `ulong hash`（ulong hash）(偏移: 0x0)
- `bool includePathSearchInfo`（bool include路径搜索信息）(偏移: 0x8)
- `bool includeAreaInfo`（bool includeArea信息）(偏移: 0x9)
- `PathHandler debugData`（路径处理器 debug数据）(偏移: 0xC)

### 方法 (3)

- `void AddHash(int hash)`
  （void 添加Hash（int hash））
- `void HashNode(GraphNode node)`
  （void Hash节点（Graph节点 node））
- `ulong get_Hash()`
  （ulong get_Hash（））

---

## RetainedGizmos.MeshWithHash（RetainedGizmos.网格WithHash）

### 字段 (3)

- `ulong hash`（ulong hash）(偏移: 0x0)
- `Mesh mesh`（网格 mesh）(偏移: 0x8)
- `bool lines`（bool lines）(偏移: 0xC)

---

## ReturnMessage（ReturnMessage）

**继承**: IMethodReturnMessage, IMethodMessage, IMessage, IInternalMessage（IMethodReturnMessage, IMethodMessage, IMessage, I内部的Message）

### 字段 (13)

- `object[] _outArgs`（object[] _outArgs）(偏移: 0x8)
- `object[] _args`（object[] _args）(偏移: 0xC)
- `LogicalCallContext _callCtx`（LogicalCallContext _callCtx）(偏移: 0x10)
- `object _returnValue`（object _return值）(偏移: 0x14)
- `string _uri`（string _uri）(偏移: 0x18)
- `Exception _exception`（Exception _exception）(偏移: 0x1C)
- `MethodBase _methodBase`（Method基础 _method基础）(偏移: 0x20)
- `string _methodName`（string _method名称）(偏移: 0x24)
- `Type[] _methodSignature`（Type[] _methodSignature）(偏移: 0x28)
- `string _typeName`（string _type名称）(偏移: 0x2C)
- `MethodReturnDictionary _properties`（MethodReturn字典 _properties）(偏移: 0x30)
- `Identity _targetIdentity`（Identity _targetIdentity）(偏移: 0x34)
- `ArgInfo _inArgInfo`（Arg信息 _inArg信息）(偏移: 0x38)

### 方法 (14)

- `int get_ArgCount()`
  （int get_Arg数量（））
- `object[] get_Args()`
  （object[] get_Args（））
- `LogicalCallContext get_LogicalCallContext()`
  （LogicalCallContext get_LogicalCallContext（））
- `MethodBase get_MethodBase()`
  （Method基础 get_Method基础（））
- `string get_MethodName()`
  （string get_Method名称（））
- `object get_MethodSignature()`
  （object get_MethodSignature（））
- `IDictionary get_Properties()`
  （I字典 get_Properties（））
- `string get_TypeName()`
  （string get_类型名称（））
- `string get_Uri()`
  （string get_Uri（））
- `void set_Uri(string value)`
  （void set_Uri（string value））
- `object GetArg(int argNum)`
  （object 获取Arg（int argNum））
- `Exception get_Exception()`
  （Exception get_Exception（））
- `object[] get_OutArgs()`
  （object[] get_OutArgs（））
- `object get_ReturnValue()`
  （object get_Return值（））

---

## RewindCallbackMode（Rewind回调模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## RichAI（RichAI）

**继承**: AIBase, IAstarAI（AI基础, IAstarAI）

### 字段 (16)

- `float acceleration`（float acceleration）(偏移: 0xE0)
- `float rotationSpeed`（float rotationSpeed）(偏移: 0xE4)
- `float slowdownTime`（float slowdown时间）(偏移: 0xE8)
- `float endReachedDistance`（float endReached距离）(偏移: 0xEC)
- `float wallForce`（float wall强制）(偏移: 0xF0)
- `float wallDist`（float wallDist）(偏移: 0xF4)
- `bool funnelSimplification`（bool funnelSimplification）(偏移: 0xF8)
- `bool slowWhenNotFacingTarget`（bool slowWhenNotFacing目标）(偏移: 0xF9)
- `RichPath richPath`（Rich路径 rich路径）(偏移: 0x100)
- `bool delayUpdatePath`（bool delay更新路径）(偏移: 0x104)
- `bool lastCorner`（bool lastCorner）(偏移: 0x105)
- `float distanceToSteeringTarget`（float distanceToSteering目标）(偏移: 0x108)
- `List<Vector3> nextCorners`（List<Vector3> nextCorners）(偏移: 0x10C)
- `List<Vector3> wallBuffer`（List<Vector3> wall缓冲区）(偏移: 0x110)
- `Color GizmoColorPath`（颜色 Gizmo颜色路径）(偏移: 0x0)
- `Animation animCompatibility`（动画 animCompatibility）(偏移: 0x124)

### 方法 (42)

- `bool get_traversingOffMeshLink()`
  （bool get_traversingOff网格Link（））
- `void set_traversingOffMeshLink(bool value)`
  （void set_traversingOff网格Link（bool value））
- `float get_remainingDistance()`
  （float get_remaining距离（））
- `bool get_reachedEndOfPath()`
  （bool get_reached结束Of路径（））
- `bool get_reachedDestination()`
  （bool get_reachedDestination（））
- `bool get_hasPath()`
  （bool get_has路径（））
- `bool get_pathPending()`
  （bool get_pathPending（））
- `Vector3 get_steeringTarget()`
  （三维向量 get_steering目标（））
- `void set_steeringTarget(Vector3 value)`
  （void set_steering目标（三维向量 value））
- `bool get_approachingPartEndpoint()`
  （bool get_approachingPartEndpoint（））
- `bool get_approachingPathEndpoint()`
  （bool get_approaching路径Endpoint（））
- `void Teleport(Vector3 newPosition, bool clearPath = True)`
  （void Teleport（三维向量 newPosition, bool clearPath = True））
- `void OnDisable()`
  （void On禁用（））
- `bool get_shouldRecalculatePath()`
  （bool get_shouldRecalculate路径（））
- `void SearchPath()`
  （void 搜索路径（））
- `void OnPathComplete(Path p)`
  （void On路径Complete（路径 p））
- `void NextPart()`
  （void 下一个Part（））
- `void OnTargetReached()`
  （void On目标Reached（））
- `Vector3 UpdateTarget(RichFunnel fn)`
  （三维向量 更新目标（RichFunnel fn））
- `void MovementUpdateInternal(float deltaTime, out Vector3 nextPosition, out Quaternion nextRotation)`
  （void Movement更新内部的（float deltaTime, out Vector3 nextPosition, out Quaternion nextRotation））
- `void TraverseFunnel(RichFunnel fn, float deltaTime, out Vector3 nextPosition, out Quaternion nextRotation)`
  （void TraverseFunnel（RichFunnel fn, float deltaTime, out Vector3 nextPosition, out Quaternion nextRotation））
- `void FinalMovement(Vector3 position3D, float deltaTime, float distanceToEndOfPath, float slowdownFactor, out Vector3 nextPosition, out Quaternion nextRotation)`
  （void FinalMovement（三维向量 position3D, float deltaTime, float distanceToEndOfPath, float slowdownFactor, out Vector3 nextPosition, out Quaternion nextRotation））
- `Vector3 ClampToNavmesh(Vector3 position, out bool positionChanged)`
  （三维向量 ClampToNavmesh（三维向量 position, out bool positionChanged））
- `Vector2 CalculateWallForce(Vector2 position, float elevation, Vector2 directionToTarget)`
  （二维向量 计算Wall强制（二维向量 position, float elevation, 二维向量 directionToTarget））
- `IEnumerator TraverseSpecial(RichSpecial link)`
  （IEnumerator Traverse特殊（Rich特殊 link））
- `IEnumerator TraverseOffMeshLinkFallback(RichSpecial link)`
  （IEnumerator TraverseOff网格LinkFallback（Rich特殊 link））
- `void OnDrawGizmos()`
  （void OnDrawGizmos（））
- `int OnUpgradeSerializedData(int version, bool unityThread)`
  （int OnUpgradeSerialized数据（int version, bool unityThread））
- `void UpdatePath()`
  （void 更新路径（））
- `Vector3 get_Velocity()`
  （三维向量 get_速度（））
- `Vector3 get_NextWaypoint()`
  （三维向量 get_下一个Waypoint（））
- `float get_DistanceToNextWaypoint()`
  （float get_距离To下一个Waypoint（））
- `bool get_repeatedlySearchPaths()`
  （bool get_repeatedly搜索Paths（））
- `void set_repeatedlySearchPaths(bool value)`
  （void set_repeatedly搜索Paths（bool value））
- `bool get_TargetReached()`
  （bool get_目标Reached（））
- `bool get_PathPending()`
  （bool get_路径Pending（））
- `bool get_ApproachingPartEndpoint()`
  （bool get_ApproachingPartEndpoint（））
- `bool get_ApproachingPathEndpoint()`
  （bool get_Approaching路径Endpoint（））
- `bool get_TraversingSpecial()`
  （bool get_Traversing特殊（））
- `Vector3 get_TargetPoint()`
  （三维向量 get_目标Point（））
- `Animation get_anim()`
  （动画 get_anim（））
- `void set_anim(Animation value)`
  （void set_anim（动画 value））

---

## RichFunnel（RichFunnel）

**继承**: RichPathPart（Rich路径Part）

### 字段 (14)

- `List<Vector3> left`（List<Vector3> left）(偏移: 0x8)
- `List<Vector3> right`（List<Vector3> right）(偏移: 0xC)
- `List<TriangleMeshNode> nodes`（List<Triangle网格Node> nodes）(偏移: 0x10)
- `Vector3 exactStart`（三维向量 exact开始）(偏移: 0x14)
- `Vector3 exactEnd`（三维向量 exact结束）(偏移: 0x20)
- `NavmeshBase graph`（Navmesh基础 graph）(偏移: 0x2C)
- `int currentNode`（int current节点）(偏移: 0x30)
- `Vector3 currentPosition`（三维向量 currentPosition）(偏移: 0x34)
- `int checkForDestroyedNodesCounter`（int checkForDestroyedNodesCounter）(偏移: 0x40)
- `RichPath path`（Rich路径 path）(偏移: 0x44)
- `int[] triBuffer`（int[] tri缓冲区）(偏移: 0x48)
- `bool funnelSimplification`（bool funnelSimplification）(偏移: 0x4C)
- `Queue<TriangleMeshNode> navmeshClampQueue`（Queue<Triangle网格Node> navmeshClamp队列）(偏移: 0x0)
- `List<TriangleMeshNode> navmeshClampList`（List<Triangle网格Node> navmeshClamp列表）(偏移: 0x4)

### 方法 (14)

- `RichFunnel Initialize(RichPath path, NavmeshBase graph)`
  （RichFunnel 初始化（Rich路径 path, Navmesh基础 graph））
- `void OnEnterPool()`
  （void OnEnter池（））
- `TriangleMeshNode get_CurrentNode()`
  （Triangle网格节点 get_当前节点（））
- `void BuildFunnelCorridor(List<GraphNode> nodes, int start, int end)`
  （void BuildFunnelCorridor（List<GraphNode> nodes, int start, int end））
- `void SimplifyPath(IRaycastableGraph graph, List<GraphNode> nodes, int start, int end, List<GraphNode> result, Vector3 startPoint, Vector3 endPoint)`
  （void Simplify路径（IRaycastableGraph graph, List<GraphNode> nodes, int start, int end, List<GraphNode> result, 三维向量 startPoint, 三维向量 endPoint））
- `void UpdateFunnelCorridor(int splitIndex, List<TriangleMeshNode> prefix)`
  （void 更新FunnelCorridor（int splitIndex, List<Triangle网格Node> prefix））
- `bool CheckForDestroyedNodes()`
  （bool 检查ForDestroyedNodes（））
- `float get_DistanceToEndOfPath()`
  （float get_距离To结束Of路径（））
- `Vector3 ClampToNavmesh(Vector3 position)`
  （三维向量 ClampToNavmesh（三维向量 position））
- `Vector3 Update(Vector3 position, List<Vector3> buffer, int numCorners, out bool lastCorner, out bool requiresRepath)`
  （三维向量 更新（三维向量 position, List<Vector3> buffer, int numCorners, out bool lastCorner, out bool requiresRepath））
- `bool ClampToNavmeshInternal(ref Vector3 position)`
  （bool ClampToNavmesh内部的（ref Vector3 position））
- `void FindWalls(List<Vector3> wallBuffer, float range)`
  （void 查找Walls（List<Vector3> wallBuffer, float range））
- `void FindWalls(int nodeIndex, List<Vector3> wallBuffer, Vector3 position, float range)`
  （void 查找Walls（int nodeIndex, List<Vector3> wallBuffer, 三维向量 position, float range））
- `bool FindNextCorners(Vector3 origin, int startIndex, List<Vector3> funnelPath, int numCorners, out bool lastCorner)`
  （bool 查找下一个Corners（三维向量 origin, int startIndex, List<Vector3> funnelPath, int numCorners, out bool lastCorner））

---

## RichPath（Rich路径）

### 字段 (4)

- `int currentPart`（int currentPart）(偏移: 0x8)
- `List<RichPathPart> parts`（List<Rich路径Part> parts）(偏移: 0xC)
- `Seeker seeker`（Seeker seeker）(偏移: 0x10)
- `ITransform transform`（I变换 transform）(偏移: 0x14)

### 方法 (8)

- `void Clear()`
  （void 清除（））
- `void Initialize(Seeker seeker, Path path, bool mergePartEndpoints, bool simplificationMode)`
  （void 初始化（Seeker seeker, 路径 path, bool mergePartEndpoints, bool simplificationMode））
- `Vector3 get_Endpoint()`
  （三维向量 get_Endpoint（））
- `void set_Endpoint(Vector3 value)`
  （void set_Endpoint（三维向量 value））
- `bool get_CompletedAllParts()`
  （bool get_Completed所有Parts（））
- `bool get_IsLastPart()`
  （bool get_是否最后一个Part（））
- `void NextPart()`
  （void 下一个Part（））
- `RichPathPart GetCurrentPart()`
  （Rich路径Part 获取当前Part（））

---

## RichSpecial（Rich特殊）

**继承**: RichPathPart（Rich路径Part）

### 字段 (4)

- `NodeLink2 nodeLink`（节点Link2 nodeLink）(偏移: 0x8)
- `Transform first`（变换 first）(偏移: 0xC)
- `Transform second`（变换 second）(偏移: 0x10)
- `bool reverse`（bool reverse）(偏移: 0x14)

### 方法 (2)

- `void OnEnterPool()`
  （void OnEnter池（））
- `RichSpecial Initialize(NodeLink2 nodeLink, GraphNode first)`
  （Rich特殊 初始化（节点Link2 nodeLink, Graph节点 first））

---

## Rigidbody（刚体）

**继承**: Component（组件）

### 方法 (32)

- `Vector3 get_velocity()`
  （三维向量 get_velocity（））
- `void set_velocity(Vector3 value)`
  （void set_velocity（三维向量 value））
- `void set_angularVelocity(Vector3 value)`
  （void set_angular速度（三维向量 value））
- `float get_mass()`
  （float get_mass（））
- `void set_useGravity(bool value)`
  （void set_use重力（bool value））
- `bool get_isKinematic()`
  （bool get_isKinematic（））
- `void set_isKinematic(bool value)`
  （void set_isKinematic（bool value））
- `Vector3 get_worldCenterOfMass()`
  （三维向量 get_world中心OfMass（））
- `void set_detectCollisions(bool value)`
  （void set_detectCollisions（bool value））
- `Vector3 get_position()`
  （三维向量 get_position（））
- `Quaternion get_rotation()`
  （Quaternion get_rotation（））
- `void set_rotation(Quaternion value)`
  （void set_rotation（Quaternion value））
- `float get_maxAngularVelocity()`
  （float get_maxAngular速度（））
- `void set_maxAngularVelocity(float value)`
  （void set_maxAngular速度（float value））
- `void MovePosition(Vector3 position)`
  （void 移动Position（三维向量 position））
- `void MoveRotation(Quaternion rot)`
  （void 移动Rotation（Quaternion rot））
- `void WakeUp()`
  （void Wake上（））
- `void ResetCenterOfMass()`
  （void 重置中心OfMass（））
- `void AddForce(Vector3 force, ForceMode mode)`
  （void 添加强制（三维向量 force, 强制模式 mode））
- `void AddForce(Vector3 force)`
  （void 添加强制（三维向量 force））
- `void AddTorque(Vector3 torque, ForceMode mode)`
  （void 添加Torque（三维向量 torque, 强制模式 mode））
- `void get_velocity_Injected(out Vector3 ret)`
  （void get_velocity_Injected（out Vector3 ret））
- `void set_velocity_Injected(ref Vector3 value)`
  （void set_velocity_Injected（ref Vector3 value））
- `void set_angularVelocity_Injected(ref Vector3 value)`
  （void set_angularVelocity_Injected（ref Vector3 value））
- `void get_worldCenterOfMass_Injected(out Vector3 ret)`
  （void get_world中心OfMass_Injected（out Vector3 ret））
- `void get_position_Injected(out Vector3 ret)`
  （void get_position_Injected（out Vector3 ret））
- `void get_rotation_Injected(out Quaternion ret)`
  （void get_rotation_Injected（out Quaternion ret））
- `void set_rotation_Injected(ref Quaternion value)`
  （void set_rotation_Injected（ref Quaternion value））
- `void MovePosition_Injected(ref Vector3 position)`
  （void 移动Position_Injected（ref Vector3 position））
- `void MoveRotation_Injected(ref Quaternion rot)`
  （void 移动Rotation_Injected（ref Quaternion rot））
- `void AddForce_Injected(ref Vector3 force, ForceMode mode)`
  （void 添加Force_Injected（ref Vector3 force, 强制模式 mode））
- `void AddTorque_Injected(ref Vector3 torque, ForceMode mode)`
  （void 添加Torque_Injected（ref Vector3 torque, 强制模式 mode））

---

## Rigidbody2D（Rigidbody2D）

**继承**: Component（组件）

### 方法 (14)

- `Vector2 get_position()`
  （二维向量 get_position（））
- `void set_position(Vector2 value)`
  （void set_position（二维向量 value））
- `float get_rotation()`
  （float get_rotation（））
- `void MovePosition(Vector2 position)`
  （void 移动Position（二维向量 position））
- `void MoveRotation(float angle)`
  （void 移动Rotation（float angle））
- `void MoveRotation_Angle(float angle)`
  （void 移动Rotation_角度（float angle））
- `Vector2 get_velocity()`
  （二维向量 get_velocity（））
- `float get_mass()`
  （float get_mass（））
- `RigidbodyType2D get_bodyType()`
  （刚体Type2D get_body类型（））
- `bool get_isKinematic()`
  （bool get_isKinematic（））
- `void get_position_Injected(out Vector2 ret)`
  （void get_position_Injected（out Vector2 ret））
- `void set_position_Injected(ref Vector2 value)`
  （void set_position_Injected（ref Vector2 value））
- `void MovePosition_Injected(ref Vector2 position)`
  （void 移动Position_Injected（ref Vector2 position））
- `void get_velocity_Injected(out Vector2 ret)`
  （void get_velocity_Injected（out Vector2 ret））

---

## RigidbodyType2D（刚体Type2D）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Rijndael（Rijndael）

**继承**: SymmetricAlgorithm（SymmetricAlgorithm）

### 字段 (2)

- `KeySizes[] s_legalBlockSizes`（键Sizes[] s_legalBlockSizes）(偏移: 0x0)
- `KeySizes[] s_legalKeySizes`（键Sizes[] s_legal键Sizes）(偏移: 0x4)

---

## RijndaelManaged（RijndaelManaged）

**继承**: Rijndael（Rijndael）

### 方法 (5)

- `ICryptoTransform CreateEncryptor(byte[] rgbKey, byte[] rgbIV)`
  （ICrypto变换 创建Encryptor（byte[] rgbKey, byte[] rgbIV））
- `ICryptoTransform CreateDecryptor(byte[] rgbKey, byte[] rgbIV)`
  （ICrypto变换 创建Decryptor（byte[] rgbKey, byte[] rgbIV））
- `void GenerateKey()`
  （void Generate键（））
- `void GenerateIV()`
  （void GenerateIV（））
- `ICryptoTransform NewEncryptor(byte[] rgbKey, CipherMode mode, byte[] rgbIV, int feedbackSize, RijndaelManagedTransformMode encryptMode)`
  （ICrypto变换 新的Encryptor（byte[] rgbKey, Cipher模式 mode, byte[] rgbIV, int feedbackSize, RijndaelManaged变换模式 encryptMode））

---

## RijndaelManagedTransform（RijndaelManaged变换）

**继承**: ICryptoTransform, IDisposable（ICrypto变换, IDisposable）

### 字段 (24)

- `CipherMode m_cipherMode`（Cipher模式 m_cipher模式）(偏移: 0x8)
- `PaddingMode m_paddingValue`（Padding模式 m_padding值）(偏移: 0xC)
- `RijndaelManagedTransformMode m_transformMode`（RijndaelManaged变换模式 m_transform模式）(偏移: 0x10)
- `int m_blockSizeBits`（int m_block大小Bits）(偏移: 0x14)
- `int m_blockSizeBytes`（int m_block大小Bytes）(偏移: 0x18)
- `int m_inputBlockSize`（int m_inputBlock大小）(偏移: 0x1C)
- `int m_outputBlockSize`（int m_outputBlock大小）(偏移: 0x20)
- `int[] m_encryptKeyExpansion`（int[] m_encrypt键Expansion）(偏移: 0x24)
- `int[] m_decryptKeyExpansion`（int[] m_decrypt键Expansion）(偏移: 0x28)
- `int m_Nr`（int m_Nr）(偏移: 0x2C)
- `int m_Nb`（int m_Nb）(偏移: 0x30)
- `int m_Nk`（int m_Nk）(偏移: 0x34)
- `int[] m_encryptindex`（int[] m_encryptindex）(偏移: 0x38)
- `int[] m_decryptindex`（int[] m_decryptindex）(偏移: 0x3C)
- `int[] m_IV`（int[] m_IV）(偏移: 0x40)
- `int[] m_lastBlockBuffer`（int[] m_lastBlock缓冲区）(偏移: 0x44)
- `byte[] m_depadBuffer`（byte[] m_depad缓冲区）(偏移: 0x48)
- `byte[] m_shiftRegister`（byte[] m_shiftRegister）(偏移: 0x4C)
- `byte[] s_Sbox`（byte[] s_Sbox）(偏移: 0x0)
- `int[] s_Rcon`（int[] s_Rcon）(偏移: 0x4)
- `int[] s_T`（int[] s_T）(偏移: 0x8)
- `int[] s_TF`（int[] s_TF）(偏移: 0xC)
- `int[] s_iT`（int[] s_iT）(偏移: 0x10)
- `int[] s_iTF`（int[] s_iTF）(偏移: 0x14)

### 方法 (18)

- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））
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
- `void Reset()`
  （void 重置（））
- `int EncryptData(byte[] inputBuffer, int inputOffset, int inputCount, ref byte[] outputBuffer, int outputOffset, PaddingMode paddingMode, bool fLast)`
  （int Encrypt数据（byte[] inputBuffer, int inputOffset, int inputCount, ref byte[] outputBuffer, int outputOffset, Padding模式 paddingMode, bool fLast））
- `int DecryptData(byte[] inputBuffer, int inputOffset, int inputCount, ref byte[] outputBuffer, int outputOffset, PaddingMode paddingMode, bool fLast)`
  （int Decrypt数据（byte[] inputBuffer, int inputOffset, int inputCount, ref byte[] outputBuffer, int outputOffset, Padding模式 paddingMode, bool fLast））
- `void Enc(int* encryptindex, int* encryptKeyExpansion, int* T, int* TF, int* work, int* temp)`
  （void Enc（int* encryptindex, int* encryptKeyExpansion, int* T, int* TF, int* work, int* temp））
- `void Dec(int* decryptindex, int* decryptKeyExpansion, int* iT, int* iTF, int* work, int* temp)`
  （void Dec（int* decryptindex, int* decryptKeyExpansion, int* iT, int* iTF, int* work, int* temp））
- `void GenerateKeyExpansion(byte[] rgbKey)`
  （void Generate键Expansion（byte[] rgbKey））
- `int rot1(int val)`
  （int rot1（int val））
- `int rot2(int val)`
  （int rot2（int val））
- `int rot3(int val)`
  （int rot3（int val））
- `int SubWord(int a)`
  （int 子Word（int a））
- `int MulX(int x)`
  （int MulX（int x））

---

## RijndaelManagedTransformMode（RijndaelManaged变换模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## RootDesignerSerializerAttribute（根DesignerSerializerAttribute）

**继承**: Attribute（Attribute）

### 字段 (4)

- `bool reloadable`（bool reloadable）(偏移: 0x8)
- `string serializerTypeName`（string serializer类型名称）(偏移: 0xC)
- `string serializerBaseTypeName`（string serializer基础类型名称）(偏移: 0x10)
- `string typeId`（string typeId）(偏移: 0x14)

### 方法 (1)

- `object get_TypeId()`
  （object get_类型Id（））

---

## RopeTrigger（Rope触发器）

**继承**: MapTrigger（地图触发器）

### 字段 (2)

- `Vector3 startPoint`（三维向量 startPoint）(偏移: 0x1C)
- `Vector3 endPoint`（三维向量 endPoint）(偏移: 0x28)

### 方法 (3)

- `void StartInteract(Player player)`
  （void 开始交互（玩家 player））
- `void Active(Player player)`
  （void 激活的（玩家 player））
- `void OnDrawGizmosSelected()`
  （void OnDrawGizmos选中的（））

---

## RotateMode（Rotate模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## RotationLimit（RotationLimit）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (5)

- `Vector3 axis`（三维向量 axis）(偏移: 0xC)
- `Quaternion defaultLocalRotation`（Quaternion default本地的Rotation）(偏移: 0x18)
- `bool initiated`（bool initiated）(偏移: 0x29)
- `bool applicationQuit`（bool applicationQuit）(偏移: 0x2A)
- `bool defaultLocalRotationSet`（bool default本地的Rotation集合）(偏移: 0x2B)

### 方法 (15)

- `void SetDefaultLocalRotation()`
  （void 集合默认的本地的Rotation（））
- `void SetDefaultLocalRotation(Quaternion localRotation)`
  （void 集合默认的本地的Rotation（Quaternion localRotation））
- `Quaternion GetLimitedLocalRotation(Quaternion localRotation, out bool changed)`
  （Quaternion 获取限制本地的Rotation（Quaternion localRotation, out bool changed））
- `bool Apply()`
  （bool 应用（））
- `void Disable()`
  （void 禁用（））
- `Vector3 get_secondaryAxis()`
  （三维向量 get_secondary轴（））
- `Vector3 get_crossAxis()`
  （三维向量 get_cross轴（））
- `bool get_defaultLocalRotationOverride()`
  （bool get_default本地的Rotation重写（））
- `void set_defaultLocalRotationOverride(bool value)`
  （void set_default本地的Rotation重写（bool value））
- `void Awake()`
  （void Awake（））
- `void LateUpdate()`
  （void 延迟更新（））
- `void LogWarning(string message)`
  （void LogWarning（string message））
- `Quaternion Limit1DOF(Quaternion rotation, Vector3 axis)`
  （Quaternion Limit1DOF（Quaternion rotation, 三维向量 axis））
- `Quaternion LimitTwist(Quaternion rotation, Vector3 axis, Vector3 orthoAxis, float twistLimit)`
  （Quaternion LimitTwist（Quaternion rotation, 三维向量 axis, 三维向量 orthoAxis, float twistLimit））
- `float GetOrthogonalAngle(Vector3 v1, Vector3 v2, Vector3 normal)`
  （float 获取Orthogonal角度（三维向量 v1, 三维向量 v2, 三维向量 normal））

---

## RotationLimitAngle（RotationLimit角度）

**继承**: RotationLimit（RotationLimit）

### 字段 (2)

- `float limit`（float limit）(偏移: 0x2C)
- `float twistLimit`（float twistLimit）(偏移: 0x30)

### 方法 (6)

- `void OpenUserManual()`
  （void 打开User手动（））
- `void OpenScriptReference()`
  （void 打开Script引用（））
- `void SupportGroup()`
  （void Support组（））
- `void ASThread()`
  （void ASThread（））
- `Quaternion LimitRotation(Quaternion rotation)`
  （Quaternion LimitRotation（Quaternion rotation））
- `Quaternion LimitSwing(Quaternion rotation)`
  （Quaternion LimitSwing（Quaternion rotation））

---

## RotationLimitHinge（RotationLimitHinge）

**继承**: RotationLimit（RotationLimit）

### 字段 (6)

- `bool useLimits`（bool useLimits）(偏移: 0x2C)
- `float min`（float min）(偏移: 0x30)
- `float max`（float max）(偏移: 0x34)
- `float zeroAxisDisplayOffset`（float zero轴DisplayOffset）(偏移: 0x38)
- `Quaternion lastRotation`（Quaternion lastRotation）(偏移: 0x3C)
- `float lastAngle`（float last角度）(偏移: 0x4C)

### 方法 (6)

- `void OpenUserManual()`
  （void 打开User手动（））
- `void OpenScriptReference()`
  （void 打开Script引用（））
- `void SupportGroup()`
  （void Support组（））
- `void ASThread()`
  （void ASThread（））
- `Quaternion LimitRotation(Quaternion rotation)`
  （Quaternion LimitRotation（Quaternion rotation））
- `Quaternion LimitHinge(Quaternion rotation)`
  （Quaternion LimitHinge（Quaternion rotation））

---

## RotationLimitPolygonal（RotationLimitPolygonal）

**继承**: RotationLimit（RotationLimit）

### 字段 (5)

- `float twistLimit`（float twistLimit）(偏移: 0x2C)
- `int smoothIterations`（int smoothIterations）(偏移: 0x30)
- `RotationLimitPolygonal.LimitPoint[] points`（RotationLimitPolygonal.LimitPoint[] points）(偏移: 0x34)
- `Vector3[] P`（Vector3[] P）(偏移: 0x38)
- `RotationLimitPolygonal.ReachCone[] reachCones`（RotationLimitPolygonal.ReachCone[] reachCones）(偏移: 0x3C)

### 方法 (15)

- `void OpenUserManual()`
  （void 打开User手动（））
- `void OpenScriptReference()`
  （void 打开Script引用（））
- `void SupportGroup()`
  （void Support组（））
- `void ASThread()`
  （void ASThread（））
- `void SetLimitPoints(RotationLimitPolygonal.LimitPoint[] points)`
  （void 集合LimitPoints（RotationLimitPolygonal.LimitPoint[] points））
- `Quaternion LimitRotation(Quaternion rotation)`
  （Quaternion LimitRotation（Quaternion rotation））
- `void Start()`
  （void 开始（））
- `void ResetToDefault()`
  （void 重置To默认的（））
- `void BuildReachCones()`
  （void BuildReachCones（））
- `Vector3[] SmoothPoints()`
  （Vector3[] SmoothPoints（））
- `float GetScalar(int k)`
  （float 获取Scalar（int k））
- `Vector3 PointToTangentPlane(Vector3 p, float r)`
  （三维向量 PointToTangentPlane（三维向量 p, float r））
- `Vector3 TangentPointToSphere(Vector3 q, float r)`
  （三维向量 TangentPointToSphere（三维向量 q, float r））
- `Quaternion LimitSwing(Quaternion rotation)`
  （Quaternion LimitSwing（Quaternion rotation））
- `int GetReachCone(Vector3 L)`
  （int 获取ReachCone（三维向量 L））

---

## RotationLimitPolygonal.LimitPoint（RotationLimitPolygonal.LimitPoint）

### 字段 (2)

- `Vector3 point`（三维向量 point）(偏移: 0x8)
- `float tangentWeight`（float tangentWeight）(偏移: 0x14)

---

## RotationLimitPolygonal.ReachCone（RotationLimitPolygonal.ReachCone）

### 字段 (4)

- `Vector3[] tetrahedron`（Vector3[] tetrahedron）(偏移: 0x8)
- `float volume`（float volume）(偏移: 0xC)
- `Vector3 S`（三维向量 S）(偏移: 0x10)
- `Vector3 B`（三维向量 B）(偏移: 0x1C)

### 方法 (6)

- `Vector3 get_o()`
  （三维向量 get_o（））
- `Vector3 get_a()`
  （三维向量 get_a（））
- `Vector3 get_b()`
  （三维向量 get_b（））
- `Vector3 get_c()`
  （三维向量 get_c（））
- `bool get_isValid()`
  （bool get_isValid（））
- `void Calculate()`
  （void 计算（））

---

## RotationLimitSpline（RotationLimitSpline）

**继承**: RotationLimit（RotationLimit）

### 字段 (2)

- `float twistLimit`（float twistLimit）(偏移: 0x2C)
- `AnimationCurve spline`（动画Curve spline）(偏移: 0x30)

### 方法 (7)

- `void OpenUserManual()`
  （void 打开User手动（））
- `void OpenScriptReference()`
  （void 打开Script引用（））
- `void SupportGroup()`
  （void Support组（））
- `void ASThread()`
  （void ASThread（））
- `void SetSpline(Keyframe[] keyframes)`
  （void 集合Spline（Keyframe[] keyframes））
- `Quaternion LimitRotation(Quaternion rotation)`
  （Quaternion LimitRotation（Quaternion rotation））
- `Quaternion LimitSwing(Quaternion rotation)`
  （Quaternion LimitSwing（Quaternion rotation））

---

## RtFieldInfo（RtField信息）

**继承**: RuntimeFieldInfo（RuntimeField信息）

### 方法 (4)

- `object UnsafeGetValue(object obj)`
  （object Unsafe获取值（object obj））
- `void CheckConsistency(object target)`
  （void 检查Consistency（object target））
- `void UnsafeSetValue(object obj, object value, BindingFlags invokeAttr, Binder binder, CultureInfo culture)`
  （void Unsafe集合值（object obj, object value, BindingFlags invokeAttr, Binder binder, Culture信息 culture））
- `void SetValueDirect(TypedReference obj, object value)`
  （void 集合值Direct（Typed引用 obj, object value））

---

## Runtime（Runtime）

### 方法 (7)

- `void mono_runtime_install_handlers()`
  （void mono_runtime_install_handlers（））
- `void InstallSignalHandlers()`
  （void Install信号Handlers（））
- `void mono_runtime_cleanup_handlers()`
  （void mono_runtime_cleanup_handlers（））
- `void RemoveSignalHandlers()`
  （void 移除信号Handlers（））
- `string GetDisplayName()`
  （string 获取Display名称（））
- `string GetNativeStackTrace(Exception exception)`
  （string 获取Native栈Trace（Exception exception））
- `bool SetGCAllowSynchronousMajor(bool flag)`
  （bool 集合GC允许SynchronousMajor（bool flag））

---

## RuntimeAnimatorController（Runtime动画器控制器）

**继承**: Object（对象）

### 方法 (1)

- `AnimationClip[] get_animationClips()`
  （动画Clip[] get_animationClips（））

---

## RuntimeArgumentHandle（RuntimeArgument句柄）

### 字段 (1)

- `IntPtr args`（整数Ptr args）(偏移: 0x0)

---

## RuntimeAssembly（RuntimeAssembly）

**继承**: Assembly（Assembly）

### 方法 (4)

- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））
- `RuntimeAssembly LoadWithPartialNameInternal(string partialName, Evidence securityEvidence, ref StackCrawlMark stackMark)`
  （RuntimeAssembly 加载WithPartial名称内部的（string partialName, Evidence securityEvidence, ref StackCrawlMark stackMark））
- `RuntimeAssembly LoadWithPartialNameInternal(AssemblyName an, Evidence securityEvidence, ref StackCrawlMark stackMark)`
  （RuntimeAssembly 加载WithPartial名称内部的（Assembly名称 an, Evidence securityEvidence, ref StackCrawlMark stackMark））
- `AssemblyName GetName(bool copiedName)`
  （Assembly名称 获取名称（bool copiedName））

---

## RuntimeClassHandle（Runtime类句柄）

### 字段 (1)

- `RuntimeStructs.MonoClass* value`（RuntimeStructs.MonoClass* value）(偏移: 0x0)

### 方法 (5)

- `RuntimeStructs.MonoClass* get_Value()`
  （RuntimeStructs.MonoClass* get_值（））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））
- `IntPtr GetTypeFromClass(RuntimeStructs.MonoClass* klass)`
  （整数Ptr 获取类型From类（RuntimeStructs.MonoClass* klass））
- `RuntimeTypeHandle GetTypeHandle()`
  （Runtime类型句柄 获取类型句柄（））

---

## RuntimeClip（Runtime弹匣）

**继承**: RuntimeClipBase（Runtime弹匣基础）

### 字段 (3)

- `TimelineClip m_Clip`（Timeline弹匣 m_弹匣）(偏移: 0xC)
- `Playable m_Playable`（Playable m_Playable）(偏移: 0x10)
- `Playable m_ParentMixer`（Playable m_父级Mixer）(偏移: 0x18)

### 方法 (11)

- `double get_start()`
  （double get_start（））
- `double get_duration()`
  （double get_duration（））
- `void Create(TimelineClip clip, Playable clipPlayable, Playable parentMixer)`
  （void 创建（Timeline弹匣 clip, Playable clipPlayable, Playable parentMixer））
- `TimelineClip get_clip()`
  （Timeline弹匣 get_clip（））
- `Playable get_mixer()`
  （Playable get_mixer（））
- `Playable get_playable()`
  （Playable get_playable（））
- `void set_enable(bool value)`
  （void set_enable（bool value））
- `void SetTime(double time)`
  （void 集合时间（double time））
- `void SetDuration(double duration)`
  （void 集合持续时间（double duration））
- `void EvaluateAt(double localTime, FrameData frameData)`
  （void EvaluateAt（double localTime, Frame数据 frameData））
- `void Reset()`
  （void 重置（））

---

## RuntimeClipBase（Runtime弹匣基础）

**继承**: RuntimeElement（Runtime元素）

### 方法 (2)

- `long get_intervalStart()`
  （long get_interval开始（））
- `long get_intervalEnd()`
  （long get_interval结束（））

---

## RuntimeCompatibilityAttribute（RuntimeCompatibilityAttribute）

**继承**: Attribute（Attribute）

### 字段 (1)

- `bool m_wrapNonExceptionThrows`（bool m_wrapNonExceptionThrows）(偏移: 0x8)

### 方法 (1)

- `void set_WrapNonExceptionThrows(bool value)`
  （void set_WrapNonExceptionThrows（bool value））

---

## RuntimeConstructorInfo（RuntimeConstructor信息）

**继承**: ConstructorInfo, ISerializable（Constructor信息, ISerializable）

### 方法 (7)

- `Module get_Module()`
  （模块 get_模块（））
- `RuntimeModule GetRuntimeModule()`
  （Runtime模块 获取Runtime模块（））
- `BindingFlags get_BindingFlags()`
  （BindingFlags get_BindingFlags（））
- `RuntimeType get_ReflectedTypeInternal()`
  （Runtime类型 get_Reflected类型内部的（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））
- `string SerializationToString()`
  （string SerializationTo字符串（））
- `void SerializationInvoke(object target, SerializationInfo info, StreamingContext context)`
  （void SerializationInvoke（object target, Serialization信息 info, StreamingContext context））

---

## RuntimeElement（Runtime元素）

**继承**: IInterval（I间隔）

### 方法 (3)

- `int get_intervalBit()`
  （int get_intervalBit（））
- `void set_intervalBit(int value)`
  （void set_intervalBit（int value））
- `void Reset()`
  （void 重置（））

---

## RuntimeEventHandle（Runtime事件句柄）

### 字段 (1)

- `IntPtr value`（整数Ptr value）(偏移: 0x0)

### 方法 (3)

- `IntPtr get_Value()`
  （整数Ptr get_值（））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## RuntimeEventInfo（Runtime事件信息）

**继承**: EventInfo, ISerializable（事件信息, ISerializable）

### 方法 (6)

- `BindingFlags get_BindingFlags()`
  （BindingFlags get_BindingFlags（））
- `Module get_Module()`
  （模块 get_模块（））
- `RuntimeType GetDeclaringTypeInternal()`
  （Runtime类型 获取Declaring类型内部的（））
- `RuntimeType get_ReflectedTypeInternal()`
  （Runtime类型 get_Reflected类型内部的（））
- `RuntimeModule GetRuntimeModule()`
  （Runtime模块 获取Runtime模块（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））

---

## RuntimeFieldHandle（RuntimeField句柄）

**继承**: ISerializable（ISerializable）

### 字段 (1)

- `IntPtr value`（整数Ptr value）(偏移: 0x0)

### 方法 (7)

- `IntPtr get_Value()`
  （整数Ptr get_值（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））
- `void SetValueInternal(FieldInfo fi, object obj, object value)`
  （void 集合值内部的（Field信息 fi, object obj, object value））
- `void SetValue(RtFieldInfo field, object obj, object value, RuntimeType fieldType, FieldAttributes fieldAttr, RuntimeType declaringType, ref bool domainInitialized)`
  （void 集合值（RtField信息 field, object obj, object value, Runtime类型 fieldType, FieldAttributes fieldAttr, Runtime类型 declaringType, ref bool domainInitialized））
- `void SetValueDirect(RtFieldInfo field, RuntimeType fieldType, void* pTypedRef, object value, RuntimeType contextType)`
  （void 集合值Direct（RtField信息 field, Runtime类型 fieldType, void* pTypedRef, object value, Runtime类型 contextType））

---

## RuntimeFieldInfo（RuntimeField信息）

**继承**: FieldInfo, ISerializable（Field信息, ISerializable）

### 方法 (6)

- `BindingFlags get_BindingFlags()`
  （BindingFlags get_BindingFlags（））
- `Module get_Module()`
  （模块 get_模块（））
- `RuntimeType GetDeclaringTypeInternal()`
  （Runtime类型 获取Declaring类型内部的（））
- `RuntimeType get_ReflectedTypeInternal()`
  （Runtime类型 get_Reflected类型内部的（））
- `RuntimeModule GetRuntimeModule()`
  （Runtime模块 获取Runtime模块（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））

---

## RuntimeGPtrArrayHandle（RuntimeGPtr数组句柄）

### 字段 (1)

- `RuntimeStructs.GPtrArray* value`（RuntimeStructs.GPtrArray* value）(偏移: 0x0)

### 方法 (5)

- `int get_Length()`
  （int get_Length（））
- `IntPtr get_Item(int i)`
  （整数Ptr get_项目（int i））
- `IntPtr Lookup(int i)`
  （整数Ptr Lookup（int i））
- `void GPtrArrayFree(RuntimeStructs.GPtrArray* value)`
  （void GPtr数组Free（RuntimeStructs.GPtrArray* value））
- `void DestroyAndFree(ref RuntimeGPtrArrayHandle h)`
  （void 销毁AndFree（ref RuntimeGPtrArrayHandle h））

---

## RuntimeGenericParamInfoHandle（RuntimeGenericParam信息句柄）

### 字段 (1)

- `RuntimeStructs.GenericParamInfo* value`（RuntimeStructs.GenericParamInfo* value）(偏移: 0x0)

### 方法 (4)

- `Type[] get_Constraints()`
  （Type[] get_Constraints（））
- `GenericParameterAttributes get_Attributes()`
  （GenericParameterAttributes get_Attributes（））
- `Type[] GetConstraints()`
  （Type[] 获取Constraints（））
- `int GetConstraintsCount()`
  （int 获取Constraints数量（））

---

## RuntimeHelpers（RuntimeHelpers）

### 方法 (7)

- `void InitializeArray(Array array, IntPtr fldHandle)`
  （void 初始化数组（数组 array, 整数Ptr fldHandle））
- `void InitializeArray(Array array, RuntimeFieldHandle fldHandle)`
  （void 初始化数组（数组 array, RuntimeField句柄 fldHandle））
- `int get_OffsetToStringData()`
  （int get_OffsetTo字符串数据（））
- `int GetHashCode(object o)`
  （int 获取HashCode（object o））
- `void RunClassConstructor(IntPtr type)`
  （void 运行类Constructor（整数Ptr type））
- `void RunClassConstructor(RuntimeTypeHandle type)`
  （void 运行类Constructor（Runtime类型句柄 type））
- `void PrepareConstrainedRegions()`
  （void PrepareConstrainedRegions（））

---

## RuntimeInitializeLoadType（Runtime初始化加载类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## RuntimeInitializeOnLoadMethodAttribute（Runtime初始化On加载MethodAttribute）

**继承**: PreserveAttribute（PreserveAttribute）

### 字段 (1)

- `RuntimeInitializeLoadType m_LoadType`（Runtime初始化加载类型 m_加载类型）(偏移: 0x8)

### 方法 (1)

- `void set_loadType(RuntimeInitializeLoadType value)`
  （void set_load类型（Runtime初始化加载类型 value））

---

## RuntimeMarshal（RuntimeMarshal）

### 方法 (6)

- `string PtrToUtf8String(IntPtr ptr)`
  （string PtrToUtf8字符串（整数Ptr ptr））
- `SafeStringMarshal MarshalString(string str)`
  （Safe字符串Marshal Marshal字符串（string str））
- `int DecodeBlobSize(IntPtr in_ptr, out IntPtr out_ptr)`
  （int DecodeBlob大小（整数Ptr in_ptr, out IntPtr out_ptr））
- `byte[] DecodeBlobArray(IntPtr ptr)`
  （byte[] DecodeBlob数组（整数Ptr ptr））
- `int AsciHexDigitValue(int c)`
  （int AsciHexDigit值（int c））
- `void FreeAssemblyName(ref MonoAssemblyName name, bool freeStruct)`
  （void FreeAssembly名称（ref MonoAssemblyName name, bool freeStruct））

---

## RuntimeMethodHandle（RuntimeMethod句柄）

**继承**: ISerializable（ISerializable）

### 字段 (1)

- `IntPtr value`（整数Ptr value）(偏移: 0x0)

### 方法 (6)

- `IntPtr get_Value()`
  （整数Ptr get_值（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））
- `string ConstructInstantiation(RuntimeMethodInfo method, TypeNameFormatFlags format)`
  （string ConstructInstantiation（RuntimeMethod信息 method, 类型名称格式化Flags format））
- `bool IsNullHandle()`
  （bool 是否Null句柄（））

---

## RuntimeMethodInfo（RuntimeMethod信息）

**继承**: MethodInfo, ISerializable（Method信息, ISerializable）

### 方法 (8)

- `BindingFlags get_BindingFlags()`
  （BindingFlags get_BindingFlags（））
- `Module get_Module()`
  （模块 get_模块（））
- `RuntimeType get_ReflectedTypeInternal()`
  （Runtime类型 get_Reflected类型内部的（））
- `string FormatNameAndSig(bool serialization)`
  （string 格式化名称AndSig（bool serialization））
- `string ToString()`
  （string To字符串（））
- `RuntimeModule GetRuntimeModule()`
  （Runtime模块 获取Runtime模块（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））
- `string SerializationToString()`
  （string SerializationTo字符串（））

---

## RuntimePlatform（RuntimePlatform）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## RuntimePropertyHandle（Runtime属性句柄）

### 字段 (1)

- `IntPtr value`（整数Ptr value）(偏移: 0x0)

### 方法 (3)

- `IntPtr get_Value()`
  （整数Ptr get_值（））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## RuntimePropertyInfo（Runtime属性信息）

**继承**: PropertyInfo, ISerializable（属性信息, ISerializable）

### 方法 (9)

- `BindingFlags get_BindingFlags()`
  （BindingFlags get_BindingFlags（））
- `Module get_Module()`
  （模块 get_模块（））
- `RuntimeType GetDeclaringTypeInternal()`
  （Runtime类型 获取Declaring类型内部的（））
- `RuntimeType get_ReflectedTypeInternal()`
  （Runtime类型 get_Reflected类型内部的（））
- `RuntimeModule GetRuntimeModule()`
  （Runtime模块 获取Runtime模块（））
- `string ToString()`
  （string To字符串（））
- `string FormatNameAndSig(bool serialization)`
  （string 格式化名称AndSig（bool serialization））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））
- `string SerializationToString()`
  （string SerializationTo字符串（））

---

## RuntimeRemoteClassHandle（RuntimeRemote类句柄）

### 字段 (1)

- `RuntimeStructs.RemoteClass* value`（RuntimeStructs.RemoteClass* value）(偏移: 0x0)

### 方法 (1)

- `RuntimeClassHandle get_ProxyClass()`
  （Runtime类句柄 get_代理类（））

---

## RuntimeResourceSet（Runtime资源集合）

**继承**: ResourceSet, IEnumerable（资源集合, IEnumerable）

### 字段 (2)

- `ResourceReader _defaultReader`（资源读取器 _default读取器）(偏移: 0x18)
- `bool _haveReadFromReader`（bool _haveReadFrom读取器）(偏移: 0x20)

### 方法 (9)

- `void Dispose(bool disposing)`
  （void 释放（bool disposing））
- `IDictionaryEnumerator GetEnumerator()`
  （I字典Enumerator 获取Enumerator（））
- `IDictionaryEnumerator GetEnumeratorHelper()`
  （I字典Enumerator 获取Enumerator辅助器（））
- `string GetString(string key)`
  （string 获取字符串（string key））
- `string GetString(string key, bool ignoreCase)`
  （string 获取字符串（string key, bool ignoreCase））
- `object GetObject(string key)`
  （object 获取对象（string key））
- `object GetObject(string key, bool ignoreCase)`
  （object 获取对象（string key, bool ignoreCase））
- `object GetObject(string key, bool ignoreCase, bool isString)`
  （object 获取对象（string key, bool ignoreCase, bool isString））
- `object ResolveResourceLocator(ResourceLocator resLocation, string key, Dictionary<string, ResourceLocator> copyOfCache, bool keyInWrongCase)`
  （object Resolve资源Locator（资源Locator resLocation, string key, Dictionary<string, 资源Locator> copyOfCache, bool keyInWrongCase））

---

## RuntimeStructs.GPtrArray（RuntimeStructs.GPtr数组）

### 字段 (2)

- `IntPtr* data`（整数Ptr* data）(偏移: 0x0)
- `int len`（int len）(偏移: 0x4)

---

## RuntimeStructs.GenericParamInfo（RuntimeStructs.GenericParam信息）

### 字段 (5)

- `RuntimeStructs.MonoClass* pklass`（RuntimeStructs.MonoClass* pklass）(偏移: 0x0)
- `IntPtr name`（整数Ptr name）(偏移: 0x4)
- `ushort flags`（ushort flags）(偏移: 0x8)
- `uint token`（uint token）(偏移: 0xC)
- `RuntimeStructs.MonoClass** constraints`（RuntimeStructs.MonoClass** constraints）(偏移: 0x10)

---

## RuntimeStructs.HandleStackMark（RuntimeStructs.句柄栈Mark）

### 字段 (3)

- `int size`（int size）(偏移: 0x0)
- `int interior_size`（int interior_size）(偏移: 0x4)
- `IntPtr chunk`（整数Ptr chunk）(偏移: 0x8)

---

## RuntimeStructs.MonoError（RuntimeStructs.MonoError）

### 字段 (18)

- `ushort error_code`（ushort error_code）(偏移: 0x0)
- `ushort hidden_0`（ushort hidden_0）(偏移: 0x2)
- `IntPtr hidden_1`（整数Ptr hidden_1）(偏移: 0x4)
- `IntPtr hidden_2`（整数Ptr hidden_2）(偏移: 0x8)
- `IntPtr hidden_3`（整数Ptr hidden_3）(偏移: 0xC)
- `IntPtr hidden_4`（整数Ptr hidden_4）(偏移: 0x10)
- `IntPtr hidden_5`（整数Ptr hidden_5）(偏移: 0x14)
- `IntPtr hidden_6`（整数Ptr hidden_6）(偏移: 0x18)
- `IntPtr hidden_7`（整数Ptr hidden_7）(偏移: 0x1C)
- `IntPtr hidden_8`（整数Ptr hidden_8）(偏移: 0x20)
- `IntPtr hidden_11`（整数Ptr hidden_11）(偏移: 0x24)
- `IntPtr hidden_12`（整数Ptr hidden_12）(偏移: 0x28)
- `IntPtr hidden_13`（整数Ptr hidden_13）(偏移: 0x2C)
- `IntPtr hidden_14`（整数Ptr hidden_14）(偏移: 0x30)
- `IntPtr hidden_15`（整数Ptr hidden_15）(偏移: 0x34)
- `IntPtr hidden_16`（整数Ptr hidden_16）(偏移: 0x38)
- `IntPtr hidden_17`（整数Ptr hidden_17）(偏移: 0x3C)
- `IntPtr hidden_18`（整数Ptr hidden_18）(偏移: 0x40)

---

## RuntimeStructs.RemoteClass（RuntimeStructs.Remote类）

### 字段 (5)

- `IntPtr default_vtable`（整数Ptr default_vtable）(偏移: 0x0)
- `IntPtr xdomain_vtable`（整数Ptr xdomain_vtable）(偏移: 0x4)
- `RuntimeStructs.MonoClass* proxy_class`（RuntimeStructs.MonoClass* proxy_class）(偏移: 0x8)
- `IntPtr proxy_class_name`（整数Ptr proxy_class_name）(偏移: 0xC)
- `uint interface_count`（uint interface_count）(偏移: 0x10)

---

## RuntimeType（Runtime类型）

**继承**: TypeInfo, ISerializable, ICloneable（类型信息, ISerializable, ICloneable）

### 字段 (10)

- `RuntimeType ValueType`（Runtime类型 值类型）(偏移: 0x0)
- `RuntimeType EnumType`（Runtime类型 Enum类型）(偏移: 0x4)
- `RuntimeType ObjectType`（Runtime类型 对象类型）(偏移: 0x8)
- `RuntimeType StringType`（Runtime类型 字符串类型）(偏移: 0xC)
- `RuntimeType DelegateType`（Runtime类型 委托类型）(偏移: 0x10)
- `Type[] s_SICtorParamTypes`（Type[] s_SICtorParamTypes）(偏移: 0x14)
- `RuntimeType s_typedRef`（Runtime类型 s_typedRef）(偏移: 0x18)
- `MonoTypeInfo type_info`（Mono类型信息 type_info）(偏移: 0xC)
- `object GenericCache`（object Generic缓存）(偏移: 0x10)
- `RuntimeConstructorInfo m_serializationCtor`（RuntimeConstructor信息 m_serializationCtor）(偏移: 0x14)

### 方法 (135)

- `void ThrowIfTypeNeverValidGenericArgument(RuntimeType type)`
  （void 投掷If类型NeverValidGenericArgument（Runtime类型 type））
- `void SanityCheckGenericArguments(RuntimeType[] genericArguments, RuntimeType[] genericParamters)`
  （void Sanity检查GenericArguments（RuntimeType[] genericArguments, RuntimeType[] genericParamters））
- `void SplitName(string fullname, out string name, out string ns)`
  （void Split名称（string fullname, out string name, out string ns））
- `void FilterHelper(BindingFlags bindingFlags, ref string name, bool allowPrefixLookup, out bool prefixLookup, out bool ignoreCase, out RuntimeType.MemberListType listType)`
  （void Filter辅助器（BindingFlags bindingFlags, ref string name, bool allowPrefixLookup, out bool prefixLookup, out bool ignoreCase, out RuntimeType.MemberListType listType））
- `void FilterHelper(BindingFlags bindingFlags, ref string name, out bool ignoreCase, out RuntimeType.MemberListType listType)`
  （void Filter辅助器（BindingFlags bindingFlags, ref string name, out bool ignoreCase, out RuntimeType.MemberListType listType））
- `bool FilterApplyPrefixLookup(MemberInfo memberInfo, string name, bool ignoreCase)`
  （bool Filter应用PrefixLookup（Member信息 memberInfo, string name, bool ignoreCase））
- `bool FilterApplyBase(MemberInfo memberInfo, BindingFlags bindingFlags, bool isPublic, bool isNonProtectedInternal, bool isStatic, string name, bool prefixLookup)`
  （bool Filter应用基础（Member信息 memberInfo, BindingFlags bindingFlags, bool isPublic, bool isNonProtectedInternal, bool isStatic, string name, bool prefixLookup））
- `bool FilterApplyType(Type type, BindingFlags bindingFlags, string name, bool prefixLookup, string ns)`
  （bool Filter应用类型（类型 type, BindingFlags bindingFlags, string name, bool prefixLookup, string ns））
- `bool FilterApplyMethodInfo(RuntimeMethodInfo method, BindingFlags bindingFlags, CallingConventions callConv, Type[] argumentTypes)`
  （bool Filter应用Method信息（RuntimeMethod信息 method, BindingFlags bindingFlags, CallingConventions callConv, Type[] argumentTypes））
- `bool FilterApplyConstructorInfo(RuntimeConstructorInfo constructor, BindingFlags bindingFlags, CallingConventions callConv, Type[] argumentTypes)`
  （bool Filter应用Constructor信息（RuntimeConstructor信息 constructor, BindingFlags bindingFlags, CallingConventions callConv, Type[] argumentTypes））
- `bool FilterApplyMethodBase(MethodBase methodBase, BindingFlags methodFlags, BindingFlags bindingFlags, CallingConventions callConv, Type[] argumentTypes)`
  （bool Filter应用Method基础（Method基础 methodBase, BindingFlags methodFlags, BindingFlags bindingFlags, CallingConventions callConv, Type[] argumentTypes））
- `bool IsSpecialSerializableType()`
  （bool 是否特殊Serializable类型（））
- `RuntimeType.ListBuilder<MethodInfo> GetMethodCandidates(string name, BindingFlags bindingAttr, CallingConventions callConv, Type[] types, bool allowPrefixLookup)`
  （RuntimeType.列表Builder<MethodInfo> 获取MethodCandidates（string name, BindingFlags bindingAttr, CallingConventions callConv, Type[] types, bool allowPrefixLookup））
- `RuntimeType.ListBuilder<ConstructorInfo> GetConstructorCandidates(string name, BindingFlags bindingAttr, CallingConventions callConv, Type[] types, bool allowPrefixLookup)`
  （RuntimeType.列表Builder<ConstructorInfo> 获取ConstructorCandidates（string name, BindingFlags bindingAttr, CallingConventions callConv, Type[] types, bool allowPrefixLookup））
- `RuntimeType.ListBuilder<PropertyInfo> GetPropertyCandidates(string name, BindingFlags bindingAttr, Type[] types, bool allowPrefixLookup)`
  （RuntimeType.列表Builder<属性Info> 获取属性Candidates（string name, BindingFlags bindingAttr, Type[] types, bool allowPrefixLookup））
- `RuntimeType.ListBuilder<EventInfo> GetEventCandidates(string name, BindingFlags bindingAttr, bool allowPrefixLookup)`
  （RuntimeType.列表Builder<事件Info> 获取事件Candidates（string name, BindingFlags bindingAttr, bool allowPrefixLookup））
- `RuntimeType.ListBuilder<FieldInfo> GetFieldCandidates(string name, BindingFlags bindingAttr, bool allowPrefixLookup)`
  （RuntimeType.列表Builder<FieldInfo> 获取FieldCandidates（string name, BindingFlags bindingAttr, bool allowPrefixLookup））
- `RuntimeType.ListBuilder<Type> GetNestedTypeCandidates(string fullname, BindingFlags bindingAttr, bool allowPrefixLookup)`
  （RuntimeType.列表Builder<Type> 获取Nested类型Candidates（string fullname, BindingFlags bindingAttr, bool allowPrefixLookup））
- `MethodInfo[] GetMethods(BindingFlags bindingAttr)`
  （MethodInfo[] 获取Methods（BindingFlags bindingAttr））
- `ConstructorInfo[] GetConstructors(BindingFlags bindingAttr)`
  （ConstructorInfo[] 获取Constructors（BindingFlags bindingAttr））
- `PropertyInfo[] GetProperties(BindingFlags bindingAttr)`
  （属性Info[] 获取Properties（BindingFlags bindingAttr））
- `EventInfo[] GetEvents(BindingFlags bindingAttr)`
  （事件Info[] 获取Events（BindingFlags bindingAttr））
- `FieldInfo[] GetFields(BindingFlags bindingAttr)`
  （FieldInfo[] 获取Fields（BindingFlags bindingAttr））
- `MethodInfo GetMethodImpl(string name, BindingFlags bindingAttr, Binder binder, CallingConventions callConv, Type[] types, ParameterModifier[] modifiers)`
  （Method信息 获取MethodImpl（string name, BindingFlags bindingAttr, Binder binder, CallingConventions callConv, Type[] types, ParameterModifier[] modifiers））
- `ConstructorInfo GetConstructorImpl(BindingFlags bindingAttr, Binder binder, CallingConventions callConvention, Type[] types, ParameterModifier[] modifiers)`
  （Constructor信息 获取ConstructorImpl（BindingFlags bindingAttr, Binder binder, CallingConventions callConvention, Type[] types, ParameterModifier[] modifiers））
- `PropertyInfo GetPropertyImpl(string name, BindingFlags bindingAttr, Binder binder, Type returnType, Type[] types, ParameterModifier[] modifiers)`
  （属性信息 获取属性Impl（string name, BindingFlags bindingAttr, Binder binder, 类型 returnType, Type[] types, ParameterModifier[] modifiers））
- `EventInfo GetEvent(string name, BindingFlags bindingAttr)`
  （事件信息 获取事件（string name, BindingFlags bindingAttr））
- `FieldInfo GetField(string name, BindingFlags bindingAttr)`
  （Field信息 获取Field（string name, BindingFlags bindingAttr））
- `Type GetNestedType(string fullname, BindingFlags bindingAttr)`
  （类型 获取Nested类型（string fullname, BindingFlags bindingAttr））
- `MemberInfo[] GetMember(string name, MemberTypes type, BindingFlags bindingAttr)`
  （MemberInfo[] 获取Member（string name, MemberTypes type, BindingFlags bindingAttr））
- `Module get_Module()`
  （模块 get_模块（））
- `RuntimeModule GetRuntimeModule()`
  （Runtime模块 获取Runtime模块（））
- `Assembly get_Assembly()`
  （Assembly get_Assembly（））
- `RuntimeAssembly GetRuntimeAssembly()`
  （RuntimeAssembly 获取RuntimeAssembly（））
- `RuntimeTypeHandle get_TypeHandle()`
  （Runtime类型句柄 get_类型句柄（））
- `bool IsInstanceOfType(object o)`
  （bool 是否实例Of类型（object o））
- `bool IsSubclassOf(Type type)`
  （bool 是否SubclassOf（类型 type））
- `bool IsAssignableFrom(Type c)`
  （bool 是否AssignableFrom（类型 c））
- `bool IsEquivalentTo(Type other)`
  （bool 是否EquivalentTo（类型 other））
- `Type get_BaseType()`
  （类型 get_基础类型（））
- `RuntimeType GetBaseType()`
  （Runtime类型 获取基础类型（））
- `Type get_UnderlyingSystemType()`
  （类型 get_Underlying系统类型（））
- `TypeAttributes GetAttributeFlagsImpl()`
  （类型Attributes 获取AttributeFlagsImpl（））
- `bool IsContextfulImpl()`
  （bool 是否ContextfulImpl（））
- `bool IsByRefImpl()`
  （bool 是否ByRefImpl（））
- `bool IsPrimitiveImpl()`
  （bool 是否PrimitiveImpl（））
- `bool IsPointerImpl()`
  （bool 是否指针Impl（））
- `bool IsCOMObjectImpl()`
  （bool 是否COM对象Impl（））
- `bool IsValueTypeImpl()`
  （bool 是否值类型Impl（））
- `bool get_IsEnum()`
  （bool get_是否Enum（））
- `bool HasElementTypeImpl()`
  （bool 是否有元素类型Impl（））
- `GenericParameterAttributes get_GenericParameterAttributes()`
  （GenericParameterAttributes get_GenericParameterAttributes（））
- `bool get_IsSzArray()`
  （bool get_是否Sz数组（））
- `bool IsArrayImpl()`
  （bool 是否数组Impl（））
- `int GetArrayRank()`
  （int 获取数组排名（））
- `Type GetElementType()`
  （类型 获取元素类型（））
- `string[] GetEnumNames()`
  （string[] 获取EnumNames（））
- `Array GetEnumValues()`
  （数组 获取EnumValues（））
- `Type GetEnumUnderlyingType()`
  （类型 获取EnumUnderlying类型（））
- `bool IsEnumDefined(object value)`
  （bool 是否EnumDefined（object value））
- `string GetEnumName(object value)`
  （string 获取Enum名称（object value））
- `RuntimeType[] GetGenericArgumentsInternal()`
  （RuntimeType[] 获取GenericArguments内部的（））
- `Type[] GetGenericArguments()`
  （Type[] 获取GenericArguments（））
- `Type MakeGenericType(Type[] instantiation)`
  （类型 MakeGeneric类型（Type[] instantiation））
- `bool get_IsGenericTypeDefinition()`
  （bool get_是否Generic类型Definition（））
- `bool get_IsGenericParameter()`
  （bool get_是否GenericParameter（））
- `int get_GenericParameterPosition()`
  （int get_GenericParameterPosition（））
- `Type GetGenericTypeDefinition()`
  （类型 获取Generic类型Definition（））
- `bool get_IsGenericType()`
  （bool get_是否Generic类型（））
- `object InvokeMember(string name, BindingFlags bindingFlags, Binder binder, object target, object[] providedArgs, ParameterModifier[] modifiers, CultureInfo culture, string[] namedParams)`
  （object InvokeMember（string name, BindingFlags bindingFlags, Binder binder, object target, object[] providedArgs, ParameterModifier[] modifiers, Culture信息 culture, string[] namedParams））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `bool op_Equality(RuntimeType left, RuntimeType right)`
  （bool op_Equality（Runtime类型 left, Runtime类型 right））
- `bool op_Inequality(RuntimeType left, RuntimeType right)`
  （bool op_Inequality（Runtime类型 left, Runtime类型 right））
- `object Clone()`
  （object 克隆（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））
- `object[] GetCustomAttributes(bool inherit)`
  （object[] 获取自定义的Attributes（bool inherit））
- `object[] GetCustomAttributes(Type attributeType, bool inherit)`
  （object[] 获取自定义的Attributes（类型 attributeType, bool inherit））
- `bool IsDefined(Type attributeType, bool inherit)`
  （bool 是否Defined（类型 attributeType, bool inherit））
- `IList<CustomAttributeData> GetCustomAttributesData()`
  （IList<自定义的AttributeData> 获取自定义的Attributes数据（））
- `string FormatTypeName(bool serialization)`
  （string 格式化类型名称（bool serialization））
- `MemberTypes get_MemberType()`
  （MemberTypes get_Member类型（））
- `Type get_ReflectedType()`
  （类型 get_Reflected类型（））
- `int get_MetadataToken()`
  （int get_Metadata令牌（））
- `void CreateInstanceCheckThis()`
  （void 创建实例检查This（））
- `object CreateInstanceImpl(BindingFlags bindingAttr, Binder binder, object[] args, CultureInfo culture, object[] activationAttributes, ref StackCrawlMark stackMark)`
  （object 创建实例Impl（BindingFlags bindingAttr, Binder binder, object[] args, Culture信息 culture, object[] activationAttributes, ref StackCrawlMark stackMark））
- `object CreateInstanceDefaultCtor(bool publicOnly, bool skipCheckThis, bool fillCache, ref StackCrawlMark stackMark)`
  （object 创建实例默认的Ctor（bool publicOnly, bool skipCheckThis, bool fillCache, ref StackCrawlMark stackMark））
- `MonoCMethod GetDefaultConstructor()`
  （MonoCMethod 获取默认的Constructor（））
- `string GetDefaultMemberName()`
  （string 获取默认的Member名称（））
- `RuntimeConstructorInfo GetSerializationCtor()`
  （RuntimeConstructor信息 获取SerializationCtor（））
- `object CreateInstanceSlow(bool publicOnly, bool skipCheckThis, bool fillCache, ref StackCrawlMark stackMark)`
  （object 创建实例Slow（bool publicOnly, bool skipCheckThis, bool fillCache, ref StackCrawlMark stackMark））
- `object CreateInstanceMono(bool nonPublic)`
  （object 创建实例Mono（bool nonPublic））
- `object CheckValue(object value, Binder binder, CultureInfo culture, BindingFlags invokeAttr)`
  （object 检查值（object value, Binder binder, Culture信息 culture, BindingFlags invokeAttr））
- `object TryConvertToType(object value, ref bool failed)`
  （object Try转换To类型（object value, ref bool failed））
- `object IsConvertibleToPrimitiveType(object value, Type targetType)`
  （object 是否ConvertibleToPrimitive类型（object value, 类型 targetType））
- `string GetCachedName(TypeNameKind kind)`
  （string 获取Cached名称（类型名称Kind kind））
- `Type make_array_type(int rank)`
  （类型 make_array_type（int rank））
- `Type MakeArrayType()`
  （类型 Make数组类型（））
- `Type MakeArrayType(int rank)`
  （类型 Make数组类型（int rank））
- `Type make_byref_type()`
  （类型 make_byref_type（））
- `Type MakeByRefType()`
  （类型 MakeByRef类型（））
- `Type MakePointerType(Type type)`
  （类型 Make指针类型（类型 type））
- `Type MakePointerType()`
  （类型 Make指针类型（））
- `bool get_ContainsGenericParameters()`
  （bool get_ContainsGenericParameters（））
- `Type[] GetGenericParameterConstraints()`
  （Type[] 获取GenericParameterConstraints（））
- `object CreateInstanceForAnotherGenericParameter(Type genericType, RuntimeType genericArgument)`
  （object 创建实例ForAnotherGenericParameter（类型 genericType, Runtime类型 genericArgument））
- `Type MakeGenericType(Type gt, Type[] types)`
  （类型 MakeGeneric类型（类型 gt, Type[] types））
- `IntPtr GetMethodsByName_native(IntPtr namePtr, BindingFlags bindingAttr, bool ignoreCase)`
  （整数Ptr 获取MethodsByName_native（整数Ptr namePtr, BindingFlags bindingAttr, bool ignoreCase））
- `RuntimeMethodInfo[] GetMethodsByName(string name, BindingFlags bindingAttr, bool ignoreCase, RuntimeType reflectedType)`
  （RuntimeMethodInfo[] 获取MethodsBy名称（string name, BindingFlags bindingAttr, bool ignoreCase, Runtime类型 reflectedType））
- `IntPtr GetPropertiesByName_native(IntPtr name, BindingFlags bindingAttr, bool icase)`
  （整数Ptr 获取PropertiesByName_native（整数Ptr name, BindingFlags bindingAttr, bool icase））
- `IntPtr GetConstructors_native(BindingFlags bindingAttr)`
  （整数Ptr 获取Constructors_native（BindingFlags bindingAttr））
- `RuntimeConstructorInfo[] GetConstructors_internal(BindingFlags bindingAttr, RuntimeType reflectedType)`
  （RuntimeConstructorInfo[] 获取Constructors_internal（BindingFlags bindingAttr, Runtime类型 reflectedType））
- `RuntimePropertyInfo[] GetPropertiesByName(string name, BindingFlags bindingAttr, bool icase, RuntimeType reflectedType)`
  （Runtime属性Info[] 获取PropertiesBy名称（string name, BindingFlags bindingAttr, bool icase, Runtime类型 reflectedType））
- `TypeCode GetTypeCodeImpl()`
  （类型Code 获取类型CodeImpl（））
- `TypeCode GetTypeCodeImplInternal(Type type)`
  （类型Code 获取类型CodeImpl内部的（类型 type））
- `string ToString()`
  （string To字符串（））
- `bool IsGenericCOMObjectImpl()`
  （bool 是否GenericCOM对象Impl（））
- `object CreateInstanceInternal(Type type)`
  （object 创建实例内部的（类型 type））
- `MethodBase get_DeclaringMethod()`
  （Method基础 get_DeclaringMethod（））
- `string getFullName(bool full_name, bool assembly_qualified)`
  （string get满名称（bool full_name, bool assembly_qualified））
- `Type[] GetGenericArgumentsInternal(bool runtimeArray)`
  （Type[] 获取GenericArguments内部的（bool runtimeArray））
- `GenericParameterAttributes GetGenericParameterAttributes()`
  （GenericParameterAttributes 获取GenericParameterAttributes（））
- `int GetGenericParameterPosition()`
  （int 获取GenericParameterPosition（））
- `IntPtr GetEvents_native(IntPtr name, BindingFlags bindingAttr)`
  （整数Ptr 获取Events_native（整数Ptr name, BindingFlags bindingAttr））
- `IntPtr GetFields_native(IntPtr name, BindingFlags bindingAttr)`
  （整数Ptr 获取Fields_native（整数Ptr name, BindingFlags bindingAttr））
- `RuntimeFieldInfo[] GetFields_internal(string name, BindingFlags bindingAttr, RuntimeType reflectedType)`
  （RuntimeFieldInfo[] 获取Fields_internal（string name, BindingFlags bindingAttr, Runtime类型 reflectedType））
- `RuntimeEventInfo[] GetEvents_internal(string name, BindingFlags bindingAttr, RuntimeType reflectedType)`
  （Runtime事件Info[] 获取Events_internal（string name, BindingFlags bindingAttr, Runtime类型 reflectedType））
- `Type[] GetInterfaces()`
  （Type[] 获取Interfaces（））
- `IntPtr GetNestedTypes_native(IntPtr name, BindingFlags bindingAttr)`
  （整数Ptr 获取NestedTypes_native（整数Ptr name, BindingFlags bindingAttr））
- `RuntimeType[] GetNestedTypes_internal(string displayName, BindingFlags bindingAttr)`
  （RuntimeType[] 获取NestedTypes_internal（string displayName, BindingFlags bindingAttr））
- `string get_AssemblyQualifiedName()`
  （string get_AssemblyQualified名称（））
- `Type get_DeclaringType()`
  （类型 get_Declaring类型（））
- `string get_Name()`
  （string get_名称（））
- `string get_Namespace()`
  （string get_Namespace（））
- `int GetHashCode()`
  （int 获取HashCode（））
- `string get_FullName()`
  （string get_满名称（））

---

## RuntimeType.MemberListType（RuntimeType.Member列表类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## RuntimeTypeHandle（Runtime类型句柄）

**继承**: ISerializable（ISerializable）

### 字段 (1)

- `IntPtr value`（整数Ptr value）(偏移: 0x0)

### 方法 (33)

- `IntPtr get_Value()`
  （整数Ptr get_值（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））
- `TypeAttributes GetAttributes(RuntimeType type)`
  （类型Attributes 获取Attributes（Runtime类型 type））
- `int GetMetadataToken(RuntimeType type)`
  （int 获取Metadata令牌（Runtime类型 type））
- `int GetToken(RuntimeType type)`
  （int 获取令牌（Runtime类型 type））
- `Type GetGenericTypeDefinition_impl(RuntimeType type)`
  （类型 获取Generic类型Definition_impl（Runtime类型 type））
- `Type GetGenericTypeDefinition(RuntimeType type)`
  （类型 获取Generic类型Definition（Runtime类型 type））
- `bool HasElementType(RuntimeType type)`
  （bool 是否有元素类型（Runtime类型 type））
- `bool HasInstantiation(RuntimeType type)`
  （bool 是否有Instantiation（Runtime类型 type））
- `bool IsArray(RuntimeType type)`
  （bool 是否数组（Runtime类型 type））
- `bool IsByRef(RuntimeType type)`
  （bool 是否ByRef（Runtime类型 type））
- `bool IsComObject(RuntimeType type)`
  （bool 是否Com对象（Runtime类型 type））
- `bool IsInstanceOfType(RuntimeType type, object o)`
  （bool 是否实例Of类型（Runtime类型 type, object o））
- `bool IsPointer(RuntimeType type)`
  （bool 是否指针（Runtime类型 type））
- `bool IsPrimitive(RuntimeType type)`
  （bool 是否Primitive（Runtime类型 type））
- `bool HasReferences(RuntimeType type)`
  （bool 是否有References（Runtime类型 type））
- `bool IsComObject(RuntimeType type, bool isGenericCOM)`
  （bool 是否Com对象（Runtime类型 type, bool isGenericCOM））
- `bool IsContextful(RuntimeType type)`
  （bool 是否Contextful（Runtime类型 type））
- `bool IsEquivalentTo(RuntimeType rtType1, RuntimeType rtType2)`
  （bool 是否EquivalentTo（Runtime类型 rtType1, Runtime类型 rtType2））
- `bool IsSzArray(RuntimeType type)`
  （bool 是否Sz数组（Runtime类型 type））
- `bool IsInterface(RuntimeType type)`
  （bool 是否Interface（Runtime类型 type））
- `int GetArrayRank(RuntimeType type)`
  （int 获取数组排名（Runtime类型 type））
- `RuntimeAssembly GetAssembly(RuntimeType type)`
  （RuntimeAssembly 获取Assembly（Runtime类型 type））
- `RuntimeType GetElementType(RuntimeType type)`
  （Runtime类型 获取元素类型（Runtime类型 type））
- `RuntimeModule GetModule(RuntimeType type)`
  （Runtime模块 获取模块（Runtime类型 type））
- `bool IsGenericVariable(RuntimeType type)`
  （bool 是否GenericVariable（Runtime类型 type））
- `RuntimeType GetBaseType(RuntimeType type)`
  （Runtime类型 获取基础类型（Runtime类型 type））
- `bool CanCastTo(RuntimeType type, RuntimeType target)`
  （bool 能否CastTo（Runtime类型 type, Runtime类型 target））
- `bool type_is_assignable_from(Type a, Type b)`
  （bool type_is_assignable_from（类型 a, 类型 b））
- `bool IsGenericTypeDefinition(RuntimeType type)`
  （bool 是否Generic类型Definition（Runtime类型 type））
- `IntPtr GetGenericParameterInfo(RuntimeType type)`
  （整数Ptr 获取GenericParameter信息（Runtime类型 type））

---

## RuntimeUtility（Runtime工具）

### 字段 (4)

- `RaycastHit[] s_HitBuffer`（RaycastHit[] s_命中缓冲区）(偏移: 0x0)
- `int[] s_PenetrationIndexBuffer`（int[] s_Penetration索引缓冲区）(偏移: 0x4)
- `SphereCollider s_ScratchCollider`（Sphere碰撞器 s_Scratch碰撞器）(偏移: 0x8)
- `GameObject s_ScratchColliderGameObject`（游戏对象 s_Scratch碰撞器游戏对象）(偏移: 0xC)

### 方法 (6)

- `void DestroyObject(Object obj)`
  （void 销毁对象（对象 obj））
- `bool IsPrefab(GameObject gameObject)`
  （bool 是否预制体（游戏对象 gameObject））
- `bool RaycastIgnoreTag(Ray ray, out RaycastHit hitInfo, float rayLength, int layerMask, in string ignoreTag)`
  （bool RaycastIgnore标签（Ray ray, out RaycastHit hitInfo, float rayLength, int layerMask, in string ignoreTag））
- `bool SphereCastIgnoreTag(Vector3 rayStart, float radius, Vector3 dir, out RaycastHit hitInfo, float rayLength, int layerMask, in string ignoreTag)`
  （bool SphereCastIgnore标签（三维向量 rayStart, float radius, 三维向量 dir, out RaycastHit hitInfo, float rayLength, int layerMask, in string ignoreTag））
- `SphereCollider GetScratchCollider()`
  （Sphere碰撞器 获取Scratch碰撞器（））
- `void DestroyScratchCollider()`
  （void 销毁Scratch碰撞器（））

---

## RuntimeWrappedException（RuntimeWrappedException）

**继承**: Exception（Exception）

### 字段 (1)

- `object m_wrappedException`（object m_wrappedException）(偏移: 0x44)

### 方法 (1)

- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））

---

## SByte（SByte）

**继承**: IComparable, IFormattable, IConvertible, IComparable<sbyte>, IEquatable<sbyte>（IComparable, IFormattable, IConvertible, IComparable<sbyte>, IEquatable<sbyte>）

### 字段 (1)

- `sbyte m_value`（sbyte m_value）(偏移: 0x0)

### 方法 (14)

- `int CompareTo(object obj)`
  （int CompareTo（object obj））
- `int CompareTo(sbyte value)`
  （int CompareTo（sbyte value））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `bool Equals(sbyte obj)`
  （bool Equals（sbyte obj））
- `int GetHashCode()`
  （int 获取HashCode（））
- `string ToString()`
  （string To字符串（））
- `string ToString(IFormatProvider provider)`
  （string To字符串（I格式化提供者 provider））
- `string ToString(string format)`
  （string To字符串（string format））
- `string ToString(string format, IFormatProvider provider)`
  （string To字符串（string format, I格式化提供者 provider））
- `string ToString(string format, NumberFormatInfo info)`
  （string To字符串（string format, Number格式化信息 info））
- `sbyte Parse(string s, IFormatProvider provider)`
  （sbyte 解析（string s, I格式化提供者 provider））
- `sbyte Parse(string s, NumberStyles style, IFormatProvider provider)`
  （sbyte 解析（string s, NumberStyles style, I格式化提供者 provider））
- `sbyte Parse(string s, NumberStyles style, NumberFormatInfo info)`
  （sbyte 解析（string s, NumberStyles style, Number格式化信息 info））
- `TypeCode GetTypeCode()`
  （类型Code 获取类型Code（））

---

## SByteArrayTypeInfo（SByte数组类型信息）

**继承**: TraceLoggingTypeInfo<sbyte[]>（TraceLogging类型Info<sbyte[]>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void WriteMetadata（TraceLoggingMetadataCollector collector, string name, 事件Field格式化 format））
- `void WriteData(TraceLoggingDataCollector collector, ref sbyte[] value)`
  （void Write数据（TraceLogging数据Collector collector, ref sbyte[] value））

---

## SByteConverter（SByteConverter）

**继承**: BaseNumberConverter（基础NumberConverter）

### 方法 (5)

- `Type get_TargetType()`
  （类型 get_目标类型（））
- `object FromString(string value, int radix)`
  （object From字符串（string value, int radix））
- `object FromString(string value, NumberFormatInfo formatInfo)`
  （object From字符串（string value, Number格式化信息 formatInfo））
- `object FromString(string value, CultureInfo culture)`
  （object From字符串（string value, Culture信息 culture））
- `string ToString(object value, NumberFormatInfo formatInfo)`
  （string To字符串（object value, Number格式化信息 formatInfo））

---

## SByteEnum（SByteEnum）

### 字段 (1)

- `sbyte value__`（sbyte value__）(偏移: 0x0)

---

## SByteTypeInfo（SByte类型信息）

**继承**: TraceLoggingTypeInfo<sbyte>（TraceLogging类型Info<sbyte>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void WriteMetadata（TraceLoggingMetadataCollector collector, string name, 事件Field格式化 format））
- `void WriteData(TraceLoggingDataCollector collector, ref sbyte value)`
  （void Write数据（TraceLogging数据Collector collector, ref sbyte value））

---

## SHA1（SHA1）

**继承**: HashAlgorithm（HashAlgorithm）

### 方法 (1)

- `SHA1 Create()`
  （SHA1 创建（））

---

## SHA1CryptoServiceProvider（SHA1Crypto服务提供者）

**继承**: SHA1（SHA1）

### 字段 (1)

- `SHA1Internal sha`（SHA1内部的 sha）(偏移: 0x18)

### 方法 (5)

- `void Finalize()`
  （void Finalize（））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））
- `void HashCore(byte[] rgb, int ibStart, int cbSize)`
  （void HashCore（byte[] rgb, int ibStart, int cbSize））
- `byte[] HashFinal()`
  （byte[] HashFinal（））
- `void Initialize()`
  （void 初始化（））

---

## SHA1Internal（SHA1内部的）

### 字段 (5)

- `uint[] _H`（uint[] _H）(偏移: 0x8)
- `ulong count`（ulong count）(偏移: 0x10)
- `byte[] _ProcessingBuffer`（byte[] _Processing缓冲区）(偏移: 0x18)
- `int _ProcessingBufferCount`（int _Processing缓冲区数量）(偏移: 0x1C)
- `uint[] buff`（uint[] buff）(偏移: 0x20)

### 方法 (8)

- `void HashCore(byte[] rgb, int ibStart, int cbSize)`
  （void HashCore（byte[] rgb, int ibStart, int cbSize））
- `byte[] HashFinal()`
  （byte[] HashFinal（））
- `void Initialize()`
  （void 初始化（））
- `void ProcessBlock(byte[] inputBuffer, uint inputOffset)`
  （void 处理Block（byte[] inputBuffer, uint inputOffset））
- `void InitialiseBuff(uint[] buff, byte[] input, uint inputOffset)`
  （void Initialise增益（uint[] buff, byte[] input, uint inputOffset））
- `void FillBuff(uint[] buff)`
  （void Fill增益（uint[] buff））
- `void ProcessFinalBlock(byte[] inputBuffer, int inputOffset, int inputCount)`
  （void 处理FinalBlock（byte[] inputBuffer, int inputOffset, int inputCount））
- `void AddLength(ulong length, byte[] buffer, int position)`
  （void 添加Length（ulong length, byte[] buffer, int position））

---

## SHA1Managed（SHA1Managed）

**继承**: SHA1（SHA1）

### 字段 (4)

- `byte[] _buffer`（byte[] _buffer）(偏移: 0x18)
- `long _count`（long _count）(偏移: 0x20)
- `uint[] _stateSHA1`（uint[] _stateSHA1）(偏移: 0x28)
- `uint[] _expandedBuffer`（uint[] _expanded缓冲区）(偏移: 0x2C)

### 方法 (8)

- `void Initialize()`
  （void 初始化（））
- `void HashCore(byte[] rgb, int ibStart, int cbSize)`
  （void HashCore（byte[] rgb, int ibStart, int cbSize））
- `byte[] HashFinal()`
  （byte[] HashFinal（））
- `void InitializeState()`
  （void 初始化状态（））
- `void _HashData(byte[] partIn, int ibStart, int cbSize)`
  （void _Hash数据（byte[] partIn, int ibStart, int cbSize））
- `byte[] _EndHash()`
  （byte[] _结束Hash（））
- `void SHATransform(uint* expandedBuffer, uint* state, byte* block)`
  （void SHA变换（uint* expandedBuffer, uint* state, byte* block））
- `void SHAExpand(uint* x)`
  （void SHAExpand（uint* x））

---

## SHA256Managed（SHA256Managed）

**继承**: SHA256（SHA256）

### 字段 (5)

- `byte[] _buffer`（byte[] _buffer）(偏移: 0x18)
- `long _count`（long _count）(偏移: 0x20)
- `uint[] _stateSHA256`（uint[] _stateSHA256）(偏移: 0x28)
- `uint[] _W`（uint[] _W）(偏移: 0x2C)
- `uint[] _K`（uint[] _K）(偏移: 0x0)

### 方法 (15)

- `void Initialize()`
  （void 初始化（））
- `void HashCore(byte[] rgb, int ibStart, int cbSize)`
  （void HashCore（byte[] rgb, int ibStart, int cbSize））
- `byte[] HashFinal()`
  （byte[] HashFinal（））
- `void InitializeState()`
  （void 初始化状态（））
- `void _HashData(byte[] partIn, int ibStart, int cbSize)`
  （void _Hash数据（byte[] partIn, int ibStart, int cbSize））
- `byte[] _EndHash()`
  （byte[] _结束Hash（））
- `void SHATransform(uint* expandedBuffer, uint* state, byte* block)`
  （void SHA变换（uint* expandedBuffer, uint* state, byte* block））
- `uint RotateRight(uint x, int n)`
  （uint Rotate右（uint x, int n））
- `uint Ch(uint x, uint y, uint z)`
  （uint Ch（uint x, uint y, uint z））
- `uint Maj(uint x, uint y, uint z)`
  （uint Maj（uint x, uint y, uint z））
- `uint sigma_0(uint x)`
  （uint sigma_0（uint x））
- `uint sigma_1(uint x)`
  （uint sigma_1（uint x））
- `uint Sigma_0(uint x)`
  （uint Sigma_0（uint x））
- `uint Sigma_1(uint x)`
  （uint Sigma_1（uint x））
- `void SHA256Expand(uint* x)`
  （void SHA256Expand（uint* x））

---

## SHA384Managed（SHA384Managed）

**继承**: SHA384（SHA384）

### 字段 (5)

- `byte[] _buffer`（byte[] _buffer）(偏移: 0x18)
- `ulong _count`（ulong _count）(偏移: 0x20)
- `ulong[] _stateSHA384`（ulong[] _stateSHA384）(偏移: 0x28)
- `ulong[] _W`（ulong[] _W）(偏移: 0x2C)
- `ulong[] _K`（ulong[] _K）(偏移: 0x0)

### 方法 (15)

- `void Initialize()`
  （void 初始化（））
- `void HashCore(byte[] rgb, int ibStart, int cbSize)`
  （void HashCore（byte[] rgb, int ibStart, int cbSize））
- `byte[] HashFinal()`
  （byte[] HashFinal（））
- `void InitializeState()`
  （void 初始化状态（））
- `void _HashData(byte[] partIn, int ibStart, int cbSize)`
  （void _Hash数据（byte[] partIn, int ibStart, int cbSize））
- `byte[] _EndHash()`
  （byte[] _结束Hash（））
- `void SHATransform(ulong* expandedBuffer, ulong* state, byte* block)`
  （void SHA变换（ulong* expandedBuffer, ulong* state, byte* block））
- `ulong RotateRight(ulong x, int n)`
  （ulong Rotate右（ulong x, int n））
- `ulong Ch(ulong x, ulong y, ulong z)`
  （ulong Ch（ulong x, ulong y, ulong z））
- `ulong Maj(ulong x, ulong y, ulong z)`
  （ulong Maj（ulong x, ulong y, ulong z））
- `ulong Sigma_0(ulong x)`
  （ulong Sigma_0（ulong x））
- `ulong Sigma_1(ulong x)`
  （ulong Sigma_1（ulong x））
- `ulong sigma_0(ulong x)`
  （ulong sigma_0（ulong x））
- `ulong sigma_1(ulong x)`
  （ulong sigma_1（ulong x））
- `void SHA384Expand(ulong* x)`
  （void SHA384Expand（ulong* x））

---

## SHA512Managed（SHA512Managed）

**继承**: SHA512（SHA512）

### 字段 (5)

- `byte[] _buffer`（byte[] _buffer）(偏移: 0x18)
- `ulong _count`（ulong _count）(偏移: 0x20)
- `ulong[] _stateSHA512`（ulong[] _stateSHA512）(偏移: 0x28)
- `ulong[] _W`（ulong[] _W）(偏移: 0x2C)
- `ulong[] _K`（ulong[] _K）(偏移: 0x0)

### 方法 (15)

- `void Initialize()`
  （void 初始化（））
- `void HashCore(byte[] rgb, int ibStart, int cbSize)`
  （void HashCore（byte[] rgb, int ibStart, int cbSize））
- `byte[] HashFinal()`
  （byte[] HashFinal（））
- `void InitializeState()`
  （void 初始化状态（））
- `void _HashData(byte[] partIn, int ibStart, int cbSize)`
  （void _Hash数据（byte[] partIn, int ibStart, int cbSize））
- `byte[] _EndHash()`
  （byte[] _结束Hash（））
- `void SHATransform(ulong* expandedBuffer, ulong* state, byte* block)`
  （void SHA变换（ulong* expandedBuffer, ulong* state, byte* block））
- `ulong RotateRight(ulong x, int n)`
  （ulong Rotate右（ulong x, int n））
- `ulong Ch(ulong x, ulong y, ulong z)`
  （ulong Ch（ulong x, ulong y, ulong z））
- `ulong Maj(ulong x, ulong y, ulong z)`
  （ulong Maj（ulong x, ulong y, ulong z））
- `ulong Sigma_0(ulong x)`
  （ulong Sigma_0（ulong x））
- `ulong Sigma_1(ulong x)`
  （ulong Sigma_1（ulong x））
- `ulong sigma_0(ulong x)`
  （ulong sigma_0（ulong x））
- `ulong sigma_1(ulong x)`
  （ulong sigma_1（ulong x））
- `void SHA512Expand(ulong* x)`
  （void SHA512Expand（ulong* x））

---

## SO_2dSound（SO_2d音效）

**继承**: ScriptableObject（脚本对象）

### 字段 (2)

- `AudioClip[] clips`（音频Clip[] clips）(偏移: 0xC)
- `int priority`（int priority）(偏移: 0x10)

### 方法 (1)

- `void SetData(RecyclableSound sound, int clipID)`
  （void 集合数据（Recyclable音效 sound, int clipID））

---

## SO_3dSound（SO_3d音效）

**继承**: ScriptableObject（脚本对象）

### 字段 (4)

- `AudioClip[] clips`（音频Clip[] clips）(偏移: 0xC)
- `float minDistance`（float min距离）(偏移: 0x10)
- `float maxDistance`（float max距离）(偏移: 0x14)
- `int priority`（int priority）(偏移: 0x18)

### 方法 (1)

- `void SetData(RecyclableSound sound, int clipID)`
  （void 集合数据（Recyclable音效 sound, int clipID））

---

## SO_AnimationLerpData（SO_动画Lerp数据）

**继承**: ScriptableObject（脚本对象）

### 字段 (1)

- `SO_AnimationLerpData.Dic dictionary`（SO_动画LerpData.Dic dictionary）(偏移: 0xC)

### 方法 (1)

- `float GetLerpTime(string animName)`
  （float 获取Lerp时间（string animName））

---

## SO_FxGroup（SO_特效组）

**继承**: ScriptableObject（脚本对象）

### 字段 (3)

- `SO_FxGroup.AttachType attachType`（SO_特效Group.Attach类型 attach类型）(偏移: 0xC)
- `bool setNodeAsParent`（bool set节点As父级）(偏移: 0x10)
- `SO_FxGroup.FxData[] allFx`（SO_特效Group.特效Data[] all特效）(偏移: 0x14)

### 方法 (1)

- `void Play(Model mdl)`
  （void 播放（模型 mdl））

---

## SO_FxGroup.AttachType（SO_特效Group.Attach类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SO_FxGroup.FxData（SO_特效Group.特效数据）

### 字段 (5)

- `GameObject fxPrefab`（游戏对象 fx预制体）(偏移: 0x0)
- `float fxSize`（float fx大小）(偏移: 0x4)
- `string attachName`（string attach名称）(偏移: 0x8)
- `Vector3 offset`（三维向量 offset）(偏移: 0xC)
- `Vector3 euler`（三维向量 euler）(偏移: 0x18)

---

## SO_Item（SO_项目）

**继承**: ScriptableObject（脚本对象）

### 字段 (6)

- `int index`（int index）(偏移: 0xC)
- `Texture itemIcon`（纹理 item图标）(偏移: 0x10)
- `string itemName`（string item名称）(偏移: 0x14)
- `SO_Item.Level itemLevel`（SO_Item.等级 item等级）(偏移: 0x18)
- `bool unique`（bool unique）(偏移: 0x1C)
- `ItemAttribute attributes`（项目Attribute attributes）(偏移: 0x20)

### 方法 (2)

- `bool GetSelected()`
  （bool 获取选中的（））
- `bool TryCalClipBuff(ClientData client, bool add)`
  （bool TryCal弹匣增益（客户端数据 client, bool add））

---

## SO_Item.Level（SO_Item.等级）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SO_Item_Character（SO_Item_角色）

**继承**: SO_Item（SO_项目）

### 字段 (2)

- `string characterName`（string character名称）(偏移: 0x24)
- `bool nanoModeSpecial`（bool nano模式特殊）(偏移: 0x28)

### 方法 (2)

- `bool GetSelected()`
  （bool 获取选中的（））
- `string GetCharacterName(Team team)`
  （string 获取角色名称（队伍 team））

---

## SO_Item_Equip（SO_Item_Equip）

**继承**: SO_Item（SO_项目）

### 方法 (1)

- `bool GetSelected()`
  （bool 获取选中的（））

---

## SO_Item_Wpn（SO_Item_武器）

**继承**: SO_Item（SO_项目）

### 字段 (2)

- `int wpnIndex`（int 武器索引）(偏移: 0x24)
- `WeaponClass wpnClass`（武器类别 武器类）(偏移: 0x28)

---

## SO_Item_Wpn_Throw（SO_Item_Wpn_投掷）

**继承**: SO_Item_Wpn（SO_Item_武器）

### 字段 (1)

- `Texture smallIcon`（纹理 small图标）(偏移: 0x2C)

---

## SR（SR）

### 方法 (2)

- `string Format(string resourceFormat, object p1)`
  （string 格式化（string resourceFormat, object p1））
- `string Format(string resourceFormat, object p1, object p2)`
  （string 格式化（string resourceFormat, object p1, object p2））

---

## SR（SR）

### 方法 (3)

- `string GetString(string name, object[] args)`
  （string 获取字符串（string name, object[] args））
- `string GetString(CultureInfo culture, string name, object[] args)`
  （string 获取字符串（Culture信息 culture, string name, object[] args））
- `string GetString(string name)`
  （string 获取字符串（string name））

---

## SR（SR）

### 方法 (1)

- `string GetString(string name)`
  （string 获取字符串（string name））

---

## SafeBuffer（Safe缓冲区）

**继承**: SafeHandleZeroOrMinusOneIsInvalid（Safe句柄ZeroOrMinusOne是否Invalid）

### 字段 (1)

- `bool inited`（bool inited）(偏移: 0x14)

### 方法 (2)

- `void AcquirePointer(ref byte* pointer)`
  （void Acquire指针（ref byte* pointer））
- `void ReleasePointer()`
  （void Release指针（））

---

## SafeFileHandle（Safe文件句柄）

**继承**: SafeHandleZeroOrMinusOneIsInvalid（Safe句柄ZeroOrMinusOne是否Invalid）

### 方法 (1)

- `bool ReleaseHandle()`
  （bool Release句柄（））

---

## SafeFindHandle（Safe查找句柄）

**继承**: SafeHandleZeroOrMinusOneIsInvalid（Safe句柄ZeroOrMinusOne是否Invalid）

### 方法 (1)

- `bool ReleaseHandle()`
  （bool Release句柄（））

---

## SafeGPtrArrayHandle（SafeGPtr数组句柄）

**继承**: IDisposable（IDisposable）

### 字段 (1)

- `RuntimeGPtrArrayHandle handle`（RuntimeGPtr数组句柄 handle）(偏移: 0x0)

### 方法 (3)

- `void Dispose()`
  （void 释放（））
- `int get_Length()`
  （int get_Length（））
- `IntPtr get_Item(int i)`
  （整数Ptr get_项目（int i））

---

## SafeHandle（Safe句柄）

**继承**: CriticalFinalizerObject, IDisposable（CriticalFinalizer对象, IDisposable）

### 字段 (4)

- `IntPtr handle`（整数Ptr handle）(偏移: 0x8)
- `int _state`（int _state）(偏移: 0xC)
- `bool _ownsHandle`（bool _owns句柄）(偏移: 0x10)
- `bool _fullyInitialized`（bool _fullyInitialized）(偏移: 0x11)

### 方法 (13)

- `void Finalize()`
  （void Finalize（））
- `void SetHandle(IntPtr handle)`
  （void 集合句柄（整数Ptr handle））
- `IntPtr DangerousGetHandle()`
  （整数Ptr Dangerous获取句柄（））
- `bool get_IsClosed()`
  （bool get_是否Closed（））
- `void Close()`
  （void 关闭（））
- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））
- `void SetHandleAsInvalid()`
  （void 集合句柄AsInvalid（））
- `void DangerousAddRef(ref bool success)`
  （void Dangerous添加Ref（ref bool success））
- `void DangerousRelease()`
  （void DangerousRelease（））
- `void InternalDispose()`
  （void 内部的释放（））
- `void InternalFinalize()`
  （void 内部的Finalize（））
- `void DangerousReleaseInternal(bool dispose)`
  （void DangerousRelease内部的（bool dispose））

---

## SafeHandleZeroOrMinusOneIsInvalid（Safe句柄ZeroOrMinusOne是否Invalid）

**继承**: SafeHandle（Safe句柄）

### 方法 (1)

- `bool get_IsInvalid()`
  （bool get_是否Invalid（））

---

## SafeModeLogBehaviour（Safe模式LogBehaviour）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SafeModeReport（Safe模式Report）

### 方法 (10)

- `int get_totMissingTargetOrFieldErrors()`
  （int get_totMissing目标OrFieldErrors（））
- `void set_totMissingTargetOrFieldErrors(int value)`
  （void set_totMissing目标OrFieldErrors（int value））
- `int get_totCallbackErrors()`
  （int get_tot回调Errors（））
- `void set_totCallbackErrors(int value)`
  （void set_tot回调Errors（int value））
- `int get_totStartupErrors()`
  （int get_totStartupErrors（））
- `void set_totStartupErrors(int value)`
  （void set_totStartupErrors（int value））
- `int get_totUnsetErrors()`
  （int get_totUnsetErrors（））
- `void set_totUnsetErrors(int value)`
  （void set_totUnsetErrors（int value））
- `void Add(SafeModeReport.SafeModeReportType type)`
  （void 添加（Safe模式Report.Safe模式Report类型 type））
- `int GetTotErrors()`
  （int 获取TotErrors（））

---

## SafeModeReport.SafeModeReportType（Safe模式Report.Safe模式Report类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SafeRegistryHandle（SafeRegistry句柄）

**继承**: SafeHandleZeroOrMinusOneIsInvalid（Safe句柄ZeroOrMinusOne是否Invalid）

### 方法 (1)

- `bool ReleaseHandle()`
  （bool Release句柄（））

---

## SafeSerializationEventArgs（SafeSerialization事件Args）

**继承**: EventArgs（事件Args）

### 字段 (2)

- `StreamingContext m_streamingContext`（StreamingContext m_streamingContext）(偏移: 0x8)
- `List<object> m_serializedStates`（List<object> m_serializedStates）(偏移: 0x10)

### 方法 (1)

- `IList<object> get_SerializedStates()`
  （IList<object> get_SerializedStates（））

---

## SafeSerializationManager（SafeSerialization管理器）

**继承**: IObjectReference, ISerializable（I对象引用, ISerializable）

### 字段 (5)

- `IList<object> m_serializedStates`（IList<object> m_serializedStates）(偏移: 0x8)
- `SerializationInfo m_savedSerializationInfo`（Serialization信息 m_savedSerialization信息）(偏移: 0xC)
- `object m_realObject`（object m_real对象）(偏移: 0x10)
- `RuntimeType m_realType`（Runtime类型 m_real类型）(偏移: 0x14)
- `EventHandler<SafeSerializationEventArgs> SerializeObjectState`（事件Handler<SafeSerialization事件Args> Serialize对象状态）(偏移: 0x18)

### 方法 (4)

- `bool get_IsActive()`
  （bool get_是否激活的（））
- `void CompleteSerialization(object serializedObject, SerializationInfo info, StreamingContext context)`
  （void CompleteSerialization（object serializedObject, Serialization信息 info, StreamingContext context））
- `void CompleteDeserialization(object deserializedObject)`
  （void CompleteDeserialization（object deserializedObject））
- `void OnDeserialized(StreamingContext context)`
  （void OnDeserialized（StreamingContext context））

---

## SafeStringMarshal（Safe字符串Marshal）

**继承**: IDisposable（IDisposable）

### 字段 (2)

- `string str`（string str）(偏移: 0x0)
- `IntPtr marshaled_string`（整数Ptr marshaled_string）(偏移: 0x4)

### 方法 (4)

- `IntPtr StringToUtf8(string str)`
  （整数Ptr 字符串ToUtf8（string str））
- `void GFree(IntPtr ptr)`
  （void GFree（整数Ptr ptr））
- `IntPtr get_Value()`
  （整数Ptr get_值（））
- `void Dispose()`
  （void 释放（））

---

## SafeWaitHandle（SafeWait句柄）

**继承**: SafeHandleZeroOrMinusOneIsInvalid（Safe句柄ZeroOrMinusOne是否Invalid）

### 方法 (1)

- `bool ReleaseHandle()`
  （bool Release句柄（））

---

## SampleCount（Sample数量）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Sampler（Sampler）

### 字段 (2)

- `IntPtr m_Ptr`（整数Ptr m_Ptr）(偏移: 0x8)
- `Sampler s_InvalidSampler`（Sampler s_InvalidSampler）(偏移: 0x0)

### 方法 (3)

- `bool get_isValid()`
  （bool get_isValid（））
- `Recorder GetRecorder()`
  （Recorder 获取Recorder（））
- `IntPtr GetRecorderInternal(IntPtr ptr)`
  （整数Ptr 获取Recorder内部的（整数Ptr ptr））

---

## SatelliteContractVersionAttribute（SatelliteContractVersionAttribute）

**继承**: Attribute（Attribute）

### 字段 (1)

- `string _version`（string _version）(偏移: 0x8)

### 方法 (1)

- `string get_Version()`
  （string get_Version（））

---

## Saunter（Saunter）

**继承**: BotActionBase（机器人动作基础）

### 字段 (4)

- `Vector3 targetPos`（三维向量 targetPos）(偏移: 0x14)
- `bool pathOver`（bool pathOver）(偏移: 0x20)
- `float nanoEndTime`（float nano结束时间）(偏移: 0x24)
- `float nextCheckTime`（float next检查时间）(偏移: 0x28)

### 方法 (9)

- `bool get_isSaunter()`
  （bool get_isSaunter（））
- `void set_isSaunter(bool value)`
  （void set_isSaunter（bool value））
- `bool get_isReach()`
  （bool get_isReach（））
- `void set_isReach(bool value)`
  （void set_isReach（bool value））
- `bool get_isOccupyingPathfinder()`
  （bool get_isOccupyingPathfinder（））
- `void Bot_Destination_Listener(ref Vector3 pos, ref int priority)`
  （void Bot_Destination_监听器（ref Vector3 pos, ref int priority））
- `bool CanDo()`
  （bool 能否Do（））
- `void DoAction()`
  （void Do动作（））
- `void OnPathComplete(Path newPath)`
  （void On路径Complete（路径 newPath））

---

## SaveProgressEventArgs（保存Progress事件Args）

**继承**: ZipProgressEventArgs（ZipProgress事件Args）

### 字段 (1)

- `int _entriesSaved`（int _entriesSaved）(偏移: 0x30)

### 方法 (3)

- `SaveProgressEventArgs ByteUpdate(string archiveName, ZipEntry entry, long bytesXferred, long totalBytes)`
  （保存Progress事件Args Byte更新（string archiveName, ZipEntry entry, long bytesXferred, long totalBytes））
- `SaveProgressEventArgs Started(string archiveName)`
  （保存Progress事件Args Started（string archiveName））
- `SaveProgressEventArgs Completed(string archiveName)`
  （保存Progress事件Args Completed（string archiveName））

---

## ScalableBufferManager（Scalable缓冲区管理器）

### 方法 (3)

- `float get_widthScaleFactor()`
  （float get_width缩放系数（））
- `float get_heightScaleFactor()`
  （float get_height缩放系数（））
- `void ResizeBuffers(float widthScale, float heightScale)`
  （void ResizeBuffers（float widthScale, float heightScale））

---

## ScaleFunc（缩放Func）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `Vector2Int Invoke(Vector2Int size)`
  （二维向量整数 Invoke（二维向量整数 size））
- `IAsyncResult BeginInvoke(Vector2Int size, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（二维向量整数 size, 异步回调 callback, object object））
- `Vector2Int EndInvoke(IAsyncResult result)`
  （二维向量整数 结束Invoke（I异步Result result））

---

## Scanbeam（Scanbeam）

### 字段 (2)

- `long Y`（long Y）(偏移: 0x8)
- `Scanbeam Next`（Scanbeam 下一个）(偏移: 0x10)

---

## Scene（场景）

### 字段 (1)

- `int m_Handle`（int m_句柄）(偏移: 0x0)

### 方法 (3)

- `int get_handle()`
  （int get_handle（））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool Equals(object other)`
  （bool Equals（object other））

---

## SceneManager（场景管理器）

### 字段 (2)

- `bool s_AllowLoadScene`（bool s_允许加载场景）(偏移: 0x0)
- `UnityAction<Scene> sceneUnloaded`（Unity引擎Action<Scene> sceneUnloaded）(偏移: 0x8)

### 方法 (16)

- `int get_sceneCount()`
  （int get_scene数量（））
- `Scene GetSceneAt(int index)`
  （场景 获取场景At（int index））
- `AsyncOperation LoadSceneAsyncNameIndexInternal(string sceneName, int sceneBuildIndex, LoadSceneParameters parameters, bool mustCompleteNextFrame)`
  （异步Operation 加载场景异步名称索引内部的（string sceneName, int sceneBuildIndex, 加载场景Parameters parameters, bool mustCompleteNextFrame））
- `AsyncOperation LoadFirstScene_Internal(bool async)`
  （异步Operation 加载第一个Scene_内部的（bool async））
- `void add_sceneLoaded(UnityAction<Scene, LoadSceneMode> value)`
  （void add_sceneLoaded（Unity引擎Action<场景, 加载场景Mode> value））
- `void remove_sceneLoaded(UnityAction<Scene, LoadSceneMode> value)`
  （void remove_sceneLoaded（Unity引擎Action<场景, 加载场景Mode> value））
- `void add_sceneUnloaded(UnityAction<Scene> value)`
  （void add_sceneUnloaded（Unity引擎Action<Scene> value））
- `void remove_sceneUnloaded(UnityAction<Scene> value)`
  （void remove_sceneUnloaded（Unity引擎Action<Scene> value））
- `void LoadScene(int sceneBuildIndex, LoadSceneMode mode)`
  （void 加载场景（int sceneBuildIndex, 加载场景模式 mode））
- `Scene LoadScene(int sceneBuildIndex, LoadSceneParameters parameters)`
  （场景 加载场景（int sceneBuildIndex, 加载场景Parameters parameters））
- `AsyncOperation LoadSceneAsync(string sceneName, LoadSceneMode mode)`
  （异步Operation 加载场景异步（string sceneName, 加载场景模式 mode））
- `AsyncOperation LoadSceneAsync(string sceneName, LoadSceneParameters parameters)`
  （异步Operation 加载场景异步（string sceneName, 加载场景Parameters parameters））
- `void Internal_SceneLoaded(Scene scene, LoadSceneMode mode)`
  （void Internal_场景Loaded（场景 scene, 加载场景模式 mode））
- `void Internal_SceneUnloaded(Scene scene)`
  （void Internal_场景Unloaded（场景 scene））
- `void Internal_ActiveSceneChanged(Scene previousActiveScene, Scene newActiveScene)`
  （void Internal_激活的场景Changed（场景 previousActiveScene, 场景 newActiveScene））
- `void GetSceneAt_Injected(int index, out Scene ret)`
  （void 获取场景At_Injected（int index, out Scene ret））

---

## SceneManagerAPI（场景管理器API）

### 字段 (1)

- `SceneManagerAPI s_DefaultAPI`（场景管理器API s_默认的API）(偏移: 0x0)

### 方法 (4)

- `SceneManagerAPI get_ActiveAPI()`
  （场景管理器API get_激活的API（））
- `SceneManagerAPI get_overrideAPI()`
  （场景管理器API get_overrideAPI（））
- `AsyncOperation LoadSceneAsyncByNameOrIndex(string sceneName, int sceneBuildIndex, LoadSceneParameters parameters, bool mustCompleteNextFrame)`
  （异步Operation 加载场景异步By名称Or索引（string sceneName, int sceneBuildIndex, 加载场景Parameters parameters, bool mustCompleteNextFrame））
- `AsyncOperation LoadFirstScene(bool mustLoadAsync)`
  （异步Operation 加载第一个场景（bool mustLoadAsync））

---

## SceneManagerAPIInternal（场景管理器API内部的）

### 方法 (2)

- `AsyncOperation LoadSceneAsyncNameIndexInternal(string sceneName, int sceneBuildIndex, LoadSceneParameters parameters, bool mustCompleteNextFrame)`
  （异步Operation 加载场景异步名称索引内部的（string sceneName, int sceneBuildIndex, 加载场景Parameters parameters, bool mustCompleteNextFrame））
- `AsyncOperation LoadSceneAsyncNameIndexInternal_Injected(string sceneName, int sceneBuildIndex, ref LoadSceneParameters parameters, bool mustCompleteNextFrame)`
  （异步Operation 加载场景异步名称索引Internal_Injected（string sceneName, int sceneBuildIndex, ref LoadSceneParameters parameters, bool mustCompleteNextFrame））

---

## SceneRenderPipeline（场景RenderPipeline）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (1)

- `RenderPipelineAsset renderPipelineAsset`（RenderPipeline资产 renderPipeline资产）(偏移: 0xC)

### 方法 (2)

- `void OnEnable()`
  （void On启用（））
- `void OnValidate()`
  （void On验证（））

---

## SceneViewDepthCopyPass（场景视图深度复制Pass）

**继承**: ScriptableRenderPass（ScriptableRenderPass）

### 字段 (2)

- `Material m_CopyDepthMaterial`（材质 m_复制深度材质）(偏移: 0x74)
- `ProfilingSampler m_ProfilingSampler`（ProfilingSampler m_ProfilingSampler）(偏移: 0x0)

### 方法 (4)

- `RenderTargetHandle get_source()`
  （Render目标句柄 get_source（））
- `void set_source(RenderTargetHandle value)`
  （void set_source（Render目标句柄 value））
- `void Setup(RenderTargetHandle source)`
  （void Setup（Render目标句柄 source））
- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（ScriptableRenderContext context, ref RenderingData renderingData））

---

## ScheduleMode（Schedule模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ScrambleMode（Scramble模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Screen（屏幕的）

### 方法 (10)

- `int get_width()`
  （int get_width（））
- `int get_height()`
  （int get_height（））
- `float get_dpi()`
  （float get_dpi（））
- `Resolution get_currentResolution()`
  （Resolution get_currentResolution（））
- `bool get_fullScreen()`
  （bool get_full屏幕的（））
- `FullScreenMode get_fullScreenMode()`
  （满屏幕的模式 get_full屏幕的模式（））
- `void SetResolution(int width, int height, FullScreenMode fullscreenMode, int preferredRefreshRate)`
  （void 集合Resolution（int width, int height, 满屏幕的模式 fullscreenMode, int preferredRefreshRate））
- `void SetResolution(int width, int height, bool fullscreen, int preferredRefreshRate)`
  （void 集合Resolution（int width, int height, bool fullscreen, int preferredRefreshRate））
- `void SetResolution(int width, int height, bool fullscreen)`
  （void 集合Resolution（int width, int height, bool fullscreen））
- `void get_currentResolution_Injected(out Resolution ret)`
  （void get_currentResolution_Injected（out Resolution ret））

---

## ScreenSpaceAmbientOcclusion（屏幕的SpaceAmbientOcclusion）

**继承**: ScriptableRendererFeature（Scriptable渲染器Feature）

### 字段 (4)

- `Shader m_Shader`（着色器 m_着色器）(偏移: 0x10)
- `ScreenSpaceAmbientOcclusionSettings m_Settings`（屏幕的SpaceAmbientOcclusionSettings m_Settings）(偏移: 0x14)
- `Material m_Material`（材质 m_材质）(偏移: 0x18)
- `ScreenSpaceAmbientOcclusion.ScreenSpaceAmbientOcclusionPass m_SSAOPass`（屏幕的SpaceAmbientOcclusion.屏幕的SpaceAmbientOcclusionPass m_SSAOPass）(偏移: 0x1C)

### 方法 (4)

- `void Create()`
  （void 创建（））
- `void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)`
  （void 添加RenderPasses（Scriptable渲染器 renderer, ref RenderingData renderingData））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））
- `bool GetMaterial()`
  （bool 获取材质（））

---

## ScreenSpaceAmbientOcclusion.ScreenSpaceAmbientOcclusionPass（屏幕的SpaceAmbientOcclusion.屏幕的SpaceAmbientOcclusionPass）

**继承**: ScriptableRenderPass（ScriptableRenderPass）

### 字段 (13)

- `string profilerTag`（string profiler标签）(偏移: 0x54)
- `Material material`（材质 material）(偏移: 0x58)
- `ScreenSpaceAmbientOcclusionSettings m_CurrentSettings`（屏幕的SpaceAmbientOcclusionSettings m_当前Settings）(偏移: 0x5C)
- `ProfilingSampler m_ProfilingSampler`（ProfilingSampler m_ProfilingSampler）(偏移: 0x60)
- `RenderTargetIdentifier m_SSAOTexture1Target`（Render目标Identifier m_SSAOTexture1目标）(偏移: 0x64)
- `RenderTargetIdentifier m_SSAOTexture2Target`（Render目标Identifier m_SSAOTexture2目标）(偏移: 0x80)
- `RenderTargetIdentifier m_SSAOTexture3Target`（Render目标Identifier m_SSAOTexture3目标）(偏移: 0x9C)
- `RenderTextureDescriptor m_Descriptor`（Render纹理Descriptor m_Descriptor）(偏移: 0xB8)
- `int s_BaseMapID`（int s_基础映射ID）(偏移: 0x0)
- `int s_SSAOParamsID`（int s_SSAOParamsID）(偏移: 0x4)
- `int s_SSAOTexture1ID`（int s_SSAOTexture1ID）(偏移: 0x8)
- `int s_SSAOTexture2ID`（int s_SSAOTexture2ID）(偏移: 0xC)
- `int s_SSAOTexture3ID`（int s_SSAOTexture3ID）(偏移: 0x10)

### 方法 (6)

- `bool Setup(ScreenSpaceAmbientOcclusionSettings featureSettings)`
  （bool Setup（屏幕的SpaceAmbientOcclusionSettings featureSettings））
- `void OnCameraSetup(CommandBuffer cmd, ref RenderingData renderingData)`
  （void On摄像机Setup（Command缓冲区 cmd, ref RenderingData renderingData））
- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（ScriptableRenderContext context, ref RenderingData renderingData））
- `void Render(CommandBuffer cmd, RenderTargetIdentifier target, ScreenSpaceAmbientOcclusion.ScreenSpaceAmbientOcclusionPass.ShaderPasses pass)`
  （void Render（Command缓冲区 cmd, Render目标Identifier target, 屏幕的SpaceAmbientOcclusion.屏幕的SpaceAmbientOcclusionPass.着色器Passes pass））
- `void RenderAndSetBaseMap(CommandBuffer cmd, RenderTargetIdentifier baseMap, RenderTargetIdentifier target, ScreenSpaceAmbientOcclusion.ScreenSpaceAmbientOcclusionPass.ShaderPasses pass)`
  （void RenderAnd集合基础映射（Command缓冲区 cmd, Render目标Identifier baseMap, Render目标Identifier target, 屏幕的SpaceAmbientOcclusion.屏幕的SpaceAmbientOcclusionPass.着色器Passes pass））
- `void OnCameraCleanup(CommandBuffer cmd)`
  （void On摄像机清理（Command缓冲区 cmd））

---

## ScreenSpaceAmbientOcclusion.ScreenSpaceAmbientOcclusionPass.ShaderPasses（屏幕的SpaceAmbientOcclusion.屏幕的SpaceAmbientOcclusionPass.着色器Passes）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ScreenSpaceAmbientOcclusionSettings（屏幕的SpaceAmbientOcclusionSettings）

### 字段 (7)

- `bool Downsample`（bool Downsample）(偏移: 0x8)
- `ScreenSpaceAmbientOcclusionSettings.DepthSource Source`（屏幕的SpaceAmbientOcclusionSettings.深度Source Source）(偏移: 0xC)
- `ScreenSpaceAmbientOcclusionSettings.NormalQuality NormalSamples`（屏幕的SpaceAmbientOcclusionSettings.法线Quality 法线Samples）(偏移: 0x10)
- `float Intensity`（float Intensity）(偏移: 0x14)
- `float DirectLightingStrength`（float DirectLightingStrength）(偏移: 0x18)
- `float Radius`（float Radius）(偏移: 0x1C)
- `int SampleCount`（int Sample数量）(偏移: 0x20)

---

## ScreenSpaceAmbientOcclusionSettings.DepthSource（屏幕的SpaceAmbientOcclusionSettings.深度Source）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ScreenSpaceAmbientOcclusionSettings.NormalQuality（屏幕的SpaceAmbientOcclusionSettings.法线Quality）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ScreenSpaceShadowResolvePass（屏幕的SpaceShadowResolvePass）

**继承**: ScriptableRenderPass（ScriptableRenderPass）

### 字段 (3)

- `Material m_ScreenSpaceShadowsMaterial`（材质 m_屏幕的SpaceShadows材质）(偏移: 0x54)
- `RenderTargetHandle m_ScreenSpaceShadowmap`（Render目标句柄 m_屏幕的SpaceShadowmap）(偏移: 0x58)
- `RenderTextureDescriptor m_RenderTextureDescriptor`（Render纹理Descriptor m_Render纹理Descriptor）(偏移: 0x78)

### 方法 (4)

- `void Setup(RenderTextureDescriptor baseDescriptor)`
  （void Setup（Render纹理Descriptor baseDescriptor））
- `void Configure(CommandBuffer cmd, RenderTextureDescriptor cameraTextureDescriptor)`
  （void Configure（Command缓冲区 cmd, Render纹理Descriptor cameraTextureDescriptor））
- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（ScriptableRenderContext context, ref RenderingData renderingData））
- `void OnCameraCleanup(CommandBuffer cmd)`
  （void On摄像机清理（Command缓冲区 cmd））

---

## ScriptPlayableBinding（ScriptPlayableBinding）

### 方法 (2)

- `PlayableBinding Create(string name, Object key, Type type)`
  （PlayableBinding 创建（string name, 对象 key, 类型 type））
- `PlayableOutput CreateScriptOutput(PlayableGraph graph, string name)`
  （PlayableOutput 创建ScriptOutput（PlayableGraph graph, string name））

---

## ScriptPlayableOutput（ScriptPlayableOutput）

**继承**: IPlayableOutput（IPlayableOutput）

### 字段 (1)

- `PlayableOutputHandle m_Handle`（PlayableOutput句柄 m_句柄）(偏移: 0x0)

### 方法 (4)

- `ScriptPlayableOutput Create(PlayableGraph graph, string name)`
  （ScriptPlayableOutput 创建（PlayableGraph graph, string name））
- `ScriptPlayableOutput get_Null()`
  （ScriptPlayableOutput get_Null（））
- `PlayableOutputHandle GetHandle()`
  （PlayableOutput句柄 获取句柄（））
- `PlayableOutput op_Implicit(ScriptPlayableOutput output)`
  （PlayableOutput op_Implicit（ScriptPlayableOutput output））

---

## ScriptableCullingParameters（ScriptableCullingParameters）

**继承**: IEquatable<ScriptableCullingParameters>（IEquatable<ScriptableCullingParameters>）

### 字段 (22)

- `int m_IsOrthographic`（int m_是否Orthographic）(偏移: 0x0)
- `LODParameters m_LODParameters`（LODParameters m_LODParameters）(偏移: 0x4)
- `int maximumCullingPlaneCount`（int maximumCullingPlane数量）(偏移: 0x0)
- `ScriptableCullingParameters.<m_CullingPlanes>e__FixedBuffer m_CullingPlanes`（ScriptableCullingParameters.<m_CullingPlanes>e__固定缓冲区 m_CullingPlanes）(偏移: 0x20)
- `int m_CullingPlaneCount`（int m_CullingPlane数量）(偏移: 0xC0)
- `uint m_CullingMask`（uint m_Culling掩码）(偏移: 0xC4)
- `ulong m_SceneMask`（ulong m_场景掩码）(偏移: 0xC8)
- `int layerCount`（int layer数量）(偏移: 0x4)
- `ScriptableCullingParameters.<m_LayerFarCullDistances>e__FixedBuffer m_LayerFarCullDistances`（ScriptableCullingParameters.<m_层FarCullDistances>e__固定缓冲区 m_层FarCullDistances）(偏移: 0xD0)
- `int m_LayerCull`（int m_层Cull）(偏移: 0x150)
- `Matrix4x4 m_CullingMatrix`（Matrix4x4 m_Culling矩阵）(偏移: 0x154)
- `Vector3 m_Origin`（三维向量 m_Origin）(偏移: 0x194)
- `float m_ShadowDistance`（float m_Shadow距离）(偏移: 0x1A0)
- `CullingOptions m_CullingOptions`（CullingOptions m_CullingOptions）(偏移: 0x1A4)
- `ReflectionProbeSortingCriteria m_ReflectionProbeSortingCriteria`（ReflectionProbeSortingCriteria m_ReflectionProbeSortingCriteria）(偏移: 0x1A8)
- `CameraProperties m_CameraProperties`（摄像机Properties m_摄像机Properties）(偏移: 0x1AC)
- `float m_AccurateOcclusionThreshold`（float m_AccurateOcclusionThreshold）(偏移: 0x58C)
- `int m_MaximumPortalCullingJobs`（int m_MaximumPortalCullingJobs）(偏移: 0x590)
- `Matrix4x4 m_StereoViewMatrix`（Matrix4x4 m_Stereo视图矩阵）(偏移: 0x594)
- `Matrix4x4 m_StereoProjectionMatrix`（Matrix4x4 m_StereoProjection矩阵）(偏移: 0x5D4)
- `float m_StereoSeparationDistance`（float m_StereoSeparation距离）(偏移: 0x614)
- `int m_maximumVisibleLights`（int m_maximum可见的Lights）(偏移: 0x618)

### 方法 (14)

- `void set_maximumVisibleLights(int value)`
  （void set_maximum可见的Lights（int value））
- `int get_cullingPlaneCount()`
  （int get_cullingPlane数量（））
- `void set_isOrthographic(bool value)`
  （void set_isOrthographic（bool value））
- `void set_shadowDistance(float value)`
  （void set_shadow距离（float value））
- `CullingOptions get_cullingOptions()`
  （CullingOptions get_cullingOptions（））
- `void set_cullingOptions(CullingOptions value)`
  （void set_cullingOptions（CullingOptions value））
- `void set_stereoViewMatrix(Matrix4x4 value)`
  （void set_stereo视图矩阵（Matrix4x4 value））
- `Matrix4x4 get_stereoProjectionMatrix()`
  （Matrix4x4 get_stereoProjection矩阵（））
- `void set_stereoProjectionMatrix(Matrix4x4 value)`
  （void set_stereoProjection矩阵（Matrix4x4 value））
- `float GetLayerCullingDistance(int layerIndex)`
  （float 获取层Culling距离（int layerIndex））
- `Plane GetCullingPlane(int index)`
  （Plane 获取CullingPlane（int index））
- `bool Equals(ScriptableCullingParameters other)`
  （bool Equals（ScriptableCullingParameters other））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## ScriptableObject（脚本对象）

**继承**: Object（对象）

### 方法 (3)

- `ScriptableObject CreateInstance(Type type)`
  （脚本对象 创建实例（类型 type））
- `void CreateScriptableObject(ScriptableObject self)`
  （void 创建Scriptable对象（脚本对象 self））
- `ScriptableObject CreateScriptableObjectInstanceFromType(Type type, bool applyDefaultsAndReset)`
  （脚本对象 创建Scriptable对象实例From类型（类型 type, bool applyDefaultsAndReset））

---

## ScriptableRenderContext（ScriptableRenderContext）

**继承**: IEquatable<ScriptableRenderContext>（IEquatable<ScriptableRenderContext>）

### 字段 (2)

- `ShaderTagId kRenderTypeTag`（着色器标签Id kRender类型标签）(偏移: 0x0)
- `IntPtr m_Ptr`（整数Ptr m_Ptr）(偏移: 0x0)

### 方法 (43)

- `void Internal_Cull(ref ScriptableCullingParameters parameters, ScriptableRenderContext renderLoop, IntPtr results)`
  （void Internal_Cull（ref ScriptableCullingParameters parameters, ScriptableRenderContext renderLoop, 整数Ptr results））
- `void InitializeSortSettings(Camera camera, out SortingSettings sortingSettings)`
  （void 初始化SortSettings（摄像机 camera, out SortingSettings sortingSettings））
- `void Submit_Internal()`
  （void Submit_内部的（））
- `int GetNumberOfCameras_Internal()`
  （int 获取NumberOfCameras_内部的（））
- `Camera GetCamera_Internal(int index)`
  （摄像机 获取Camera_内部的（int index））
- `void DrawRenderers_Internal(IntPtr cullResults, ref DrawingSettings drawingSettings, ref FilteringSettings filteringSettings, ShaderTagId tagName, bool isPassTagName, IntPtr tagValues, IntPtr stateBlocks, int stateCount)`
  （void DrawRenderers_内部的（整数Ptr cullResults, ref DrawingSettings drawingSettings, ref FilteringSettings filteringSettings, 着色器标签Id tagName, bool isPassTagName, 整数Ptr tagValues, 整数Ptr stateBlocks, int stateCount））
- `void DrawShadows_Internal(IntPtr shadowDrawingSettings)`
  （void DrawShadows_内部的（整数Ptr shadowDrawingSettings））
- `void ExecuteCommandBuffer_Internal(CommandBuffer commandBuffer)`
  （void 执行CommandBuffer_内部的（Command缓冲区 commandBuffer））
- `void ExecuteCommandBufferAsync_Internal(CommandBuffer commandBuffer, ComputeQueueType queueType)`
  （void 执行Command缓冲区Async_内部的（Command缓冲区 commandBuffer, Compute队列类型 queueType））
- `void SetupCameraProperties_Internal(Camera camera, bool stereoSetup, int eye)`
  （void Setup摄像机Properties_内部的（摄像机 camera, bool stereoSetup, int eye））
- `void DrawSkybox_Internal(Camera camera)`
  （void DrawSkybox_内部的（摄像机 camera））
- `void InvokeOnRenderObjectCallback_Internal()`
  （void InvokeOnRender对象Callback_内部的（））
- `void DrawWireOverlay_Impl(Camera camera)`
  （void DrawWireOverlay_Impl（摄像机 camera））
- `void Submit()`
  （void Submit（））
- `int GetNumberOfCameras()`
  （int 获取NumberOfCameras（））
- `Camera GetCamera(int index)`
  （摄像机 获取摄像机（int index））
- `void DrawRenderers(CullingResults cullingResults, ref DrawingSettings drawingSettings, ref FilteringSettings filteringSettings)`
  （void DrawRenderers（CullingResults cullingResults, ref DrawingSettings drawingSettings, ref FilteringSettings filteringSettings））
- `void DrawRenderers(CullingResults cullingResults, ref DrawingSettings drawingSettings, ref FilteringSettings filteringSettings, ref RenderStateBlock stateBlock)`
  （void DrawRenderers（CullingResults cullingResults, ref DrawingSettings drawingSettings, ref FilteringSettings filteringSettings, ref RenderStateBlock stateBlock））
- `void DrawRenderers(CullingResults cullingResults, ref DrawingSettings drawingSettings, ref FilteringSettings filteringSettings, ShaderTagId tagName, bool isPassTagName, NativeArray<ShaderTagId> tagValues, NativeArray<RenderStateBlock> stateBlocks)`
  （void DrawRenderers（CullingResults cullingResults, ref DrawingSettings drawingSettings, ref FilteringSettings filteringSettings, 着色器标签Id tagName, bool isPassTagName, NativeArray<着色器标签Id> tagValues, NativeArray<Render状态Block> stateBlocks））
- `void DrawShadows(ref ShadowDrawingSettings settings)`
  （void DrawShadows（ref ShadowDrawingSettings settings））
- `void ExecuteCommandBuffer(CommandBuffer commandBuffer)`
  （void 执行Command缓冲区（Command缓冲区 commandBuffer））
- `void ExecuteCommandBufferAsync(CommandBuffer commandBuffer, ComputeQueueType queueType)`
  （void 执行Command缓冲区异步（Command缓冲区 commandBuffer, Compute队列类型 queueType））
- `void SetupCameraProperties(Camera camera, bool stereoSetup = False)`
  （void Setup摄像机Properties（摄像机 camera, bool stereoSetup = False））
- `void SetupCameraProperties(Camera camera, bool stereoSetup, int eye)`
  （void Setup摄像机Properties（摄像机 camera, bool stereoSetup, int eye））
- `void DrawSkybox(Camera camera)`
  （void DrawSkybox（摄像机 camera））
- `void InvokeOnRenderObjectCallback()`
  （void InvokeOnRender对象回调（））
- `void DrawWireOverlay(Camera camera)`
  （void DrawWireOverlay（摄像机 camera））
- `CullingResults Cull(ref ScriptableCullingParameters parameters)`
  （CullingResults Cull（ref ScriptableCullingParameters parameters））
- `bool Equals(ScriptableRenderContext other)`
  （bool Equals（ScriptableRenderContext other））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））
- `void Internal_Cull_Injected(ref ScriptableCullingParameters parameters, ref ScriptableRenderContext renderLoop, IntPtr results)`
  （void Internal_Cull_Injected（ref ScriptableCullingParameters parameters, ref ScriptableRenderContext renderLoop, 整数Ptr results））
- `void Submit_Internal_Injected(ref ScriptableRenderContext _unity_self)`
  （void Submit_Internal_Injected（ref ScriptableRenderContext _unity_self））
- `int GetNumberOfCameras_Internal_Injected(ref ScriptableRenderContext _unity_self)`
  （int 获取NumberOfCameras_Internal_Injected（ref ScriptableRenderContext _unity_self））
- `Camera GetCamera_Internal_Injected(ref ScriptableRenderContext _unity_self, int index)`
  （摄像机 获取Camera_Internal_Injected（ref ScriptableRenderContext _unity_self, int index））
- `void DrawRenderers_Internal_Injected(ref ScriptableRenderContext _unity_self, IntPtr cullResults, ref DrawingSettings drawingSettings, ref FilteringSettings filteringSettings, ref ShaderTagId tagName, bool isPassTagName, IntPtr tagValues, IntPtr stateBlocks, int stateCount)`
  （void DrawRenderers_Internal_Injected（ref ScriptableRenderContext _unity_self, 整数Ptr cullResults, ref DrawingSettings drawingSettings, ref FilteringSettings filteringSettings, ref ShaderTagId tagName, bool isPassTagName, 整数Ptr tagValues, 整数Ptr stateBlocks, int stateCount））
- `void DrawShadows_Internal_Injected(ref ScriptableRenderContext _unity_self, IntPtr shadowDrawingSettings)`
  （void DrawShadows_Internal_Injected（ref ScriptableRenderContext _unity_self, 整数Ptr shadowDrawingSettings））
- `void ExecuteCommandBuffer_Internal_Injected(ref ScriptableRenderContext _unity_self, CommandBuffer commandBuffer)`
  （void 执行CommandBuffer_Internal_Injected（ref ScriptableRenderContext _unity_self, Command缓冲区 commandBuffer））
- `void ExecuteCommandBufferAsync_Internal_Injected(ref ScriptableRenderContext _unity_self, CommandBuffer commandBuffer, ComputeQueueType queueType)`
  （void 执行Command缓冲区Async_Internal_Injected（ref ScriptableRenderContext _unity_self, Command缓冲区 commandBuffer, Compute队列类型 queueType））
- `void SetupCameraProperties_Internal_Injected(ref ScriptableRenderContext _unity_self, Camera camera, bool stereoSetup, int eye)`
  （void Setup摄像机Properties_Internal_Injected（ref ScriptableRenderContext _unity_self, 摄像机 camera, bool stereoSetup, int eye））
- `void DrawSkybox_Internal_Injected(ref ScriptableRenderContext _unity_self, Camera camera)`
  （void DrawSkybox_Internal_Injected（ref ScriptableRenderContext _unity_self, 摄像机 camera））
- `void InvokeOnRenderObjectCallback_Internal_Injected(ref ScriptableRenderContext _unity_self)`
  （void InvokeOnRender对象Callback_Internal_Injected（ref ScriptableRenderContext _unity_self））
- `void DrawWireOverlay_Impl_Injected(ref ScriptableRenderContext _unity_self, Camera camera)`
  （void DrawWireOverlay_Impl_Injected（ref ScriptableRenderContext _unity_self, 摄像机 camera））

---

## ScriptableRenderPass（ScriptableRenderPass）

### 字段 (7)

- `RenderBufferStoreAction[] m_ColorStoreActions`（Render缓冲区商店Action[] m_颜色商店Actions）(偏移: 0xC)
- `RenderBufferStoreAction m_DepthStoreAction`（Render缓冲区商店动作 m_深度商店动作）(偏移: 0x10)
- `RenderTargetIdentifier[] m_ColorAttachments`（Render目标Identifier[] m_颜色Attachments）(偏移: 0x1C)
- `RenderTargetIdentifier m_DepthAttachment`（Render目标Identifier m_深度Attachment）(偏移: 0x20)
- `ScriptableRenderPassInput m_Input`（ScriptableRenderPass输入 m_输入）(偏移: 0x3C)
- `ClearFlag m_ClearFlag`（清除标志 m_清除标志）(偏移: 0x40)
- `Color m_ClearColor`（颜色 m_清除颜色）(偏移: 0x44)

### 方法 (35)

- `void FrameCleanup(CommandBuffer cmd)`
  （void Frame清理（Command缓冲区 cmd））
- `RenderPassEvent get_renderPassEvent()`
  （RenderPass事件 get_renderPass事件（））
- `void set_renderPassEvent(RenderPassEvent value)`
  （void set_renderPass事件（RenderPass事件 value））
- `RenderTargetIdentifier[] get_colorAttachments()`
  （Render目标Identifier[] get_colorAttachments（））
- `RenderTargetIdentifier get_colorAttachment()`
  （Render目标Identifier get_colorAttachment（））
- `RenderTargetIdentifier get_depthAttachment()`
  （Render目标Identifier get_depthAttachment（））
- `RenderBufferStoreAction[] get_colorStoreActions()`
  （Render缓冲区商店Action[] get_color商店Actions（））
- `RenderBufferStoreAction get_depthStoreAction()`
  （Render缓冲区商店动作 get_depth商店动作（））
- `ScriptableRenderPassInput get_input()`
  （ScriptableRenderPass输入 get_input（））
- `ClearFlag get_clearFlag()`
  （清除标志 get_clear标志（））
- `Color get_clearColor()`
  （颜色 get_clear颜色（））
- `ProfilingSampler get_profilingSampler()`
  （ProfilingSampler get_profilingSampler（））
- `void set_profilingSampler(ProfilingSampler value)`
  （void set_profilingSampler（ProfilingSampler value））
- `bool get_overrideCameraTarget()`
  （bool get_override摄像机目标（））
- `void set_overrideCameraTarget(bool value)`
  （void set_override摄像机目标（bool value））
- `bool get_isBlitRenderPass()`
  （bool get_isBlitRenderPass（））
- `void set_isBlitRenderPass(bool value)`
  （void set_isBlitRenderPass（bool value））
- `void ConfigureInput(ScriptableRenderPassInput passInput)`
  （void Configure输入（ScriptableRenderPass输入 passInput））
- `void ConfigureColorStoreAction(RenderBufferStoreAction storeAction, uint attachmentIndex = 0)`
  （void Configure颜色商店动作（Render缓冲区商店动作 storeAction, uint attachmentIndex = 0））
- `void ConfigureColorStoreActions(RenderBufferStoreAction[] storeActions)`
  （void Configure颜色商店Actions（Render缓冲区商店Action[] storeActions））
- `void ConfigureDepthStoreAction(RenderBufferStoreAction storeAction)`
  （void Configure深度商店动作（Render缓冲区商店动作 storeAction））
- `void ConfigureTarget(RenderTargetIdentifier colorAttachment, RenderTargetIdentifier depthAttachment)`
  （void Configure目标（Render目标Identifier colorAttachment, Render目标Identifier depthAttachment））
- `void ConfigureTarget(RenderTargetIdentifier[] colorAttachments, RenderTargetIdentifier depthAttachment)`
  （void Configure目标（Render目标Identifier[] colorAttachments, Render目标Identifier depthAttachment））
- `void ConfigureTarget(RenderTargetIdentifier colorAttachment)`
  （void Configure目标（Render目标Identifier colorAttachment））
- `void ConfigureTarget(RenderTargetIdentifier[] colorAttachments)`
  （void Configure目标（Render目标Identifier[] colorAttachments））
- `void ConfigureClear(ClearFlag clearFlag, Color clearColor)`
  （void Configure清除（清除标志 clearFlag, 颜色 clearColor））
- `void OnCameraSetup(CommandBuffer cmd, ref RenderingData renderingData)`
  （void On摄像机Setup（Command缓冲区 cmd, ref RenderingData renderingData））
- `void Configure(CommandBuffer cmd, RenderTextureDescriptor cameraTextureDescriptor)`
  （void Configure（Command缓冲区 cmd, Render纹理Descriptor cameraTextureDescriptor））
- `void OnCameraCleanup(CommandBuffer cmd)`
  （void On摄像机清理（Command缓冲区 cmd））
- `void OnFinishCameraStackRendering(CommandBuffer cmd)`
  （void OnFinish摄像机栈Rendering（Command缓冲区 cmd））
- `void Blit(CommandBuffer cmd, RenderTargetIdentifier source, RenderTargetIdentifier destination, Material material, int passIndex = 0)`
  （void Blit（Command缓冲区 cmd, Render目标Identifier source, Render目标Identifier destination, 材质 material, int passIndex = 0））
- `DrawingSettings CreateDrawingSettings(ShaderTagId shaderTagId, ref RenderingData renderingData, SortingCriteria sortingCriteria)`
  （DrawingSettings 创建DrawingSettings（着色器标签Id shaderTagId, ref RenderingData renderingData, SortingCriteria sortingCriteria））
- `DrawingSettings CreateDrawingSettings(List<ShaderTagId> shaderTagIdList, ref RenderingData renderingData, SortingCriteria sortingCriteria)`
  （DrawingSettings 创建DrawingSettings（List<着色器标签Id> shaderTagIdList, ref RenderingData renderingData, SortingCriteria sortingCriteria））
- `bool op_LessThan(ScriptableRenderPass lhs, ScriptableRenderPass rhs)`
  （bool op_LessThan（ScriptableRenderPass lhs, ScriptableRenderPass rhs））
- `bool op_GreaterThan(ScriptableRenderPass lhs, ScriptableRenderPass rhs)`
  （bool op_GreaterThan（ScriptableRenderPass lhs, ScriptableRenderPass rhs））

---

## ScriptableRenderPassInput（ScriptableRenderPass输入）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ScriptableRenderer（Scriptable渲染器）

**继承**: IDisposable（IDisposable）

### 字段 (16)

- `ScriptableRenderer current`（Scriptable渲染器 current）(偏移: 0x0)
- `StoreActionsOptimization m_StoreActionsOptimizationSetting`（商店ActionsOptimization m_商店ActionsOptimization设置）(偏移: 0x14)
- `bool m_UseOptimizedStoreActions`（bool m_UseOptimized商店Actions）(偏移: 0x4)
- `List<ScriptableRenderPass> m_ActiveRenderPassQueue`（List<ScriptableRenderPass> m_激活的RenderPass队列）(偏移: 0x18)
- `List<ScriptableRendererFeature> m_RendererFeatures`（List<Scriptable渲染器Feature> m_渲染器Features）(偏移: 0x1C)
- `RenderTargetIdentifier m_CameraColorTarget`（Render目标Identifier m_摄像机颜色目标）(偏移: 0x20)
- `RenderTargetIdentifier m_CameraDepthTarget`（Render目标Identifier m_摄像机深度目标）(偏移: 0x3C)
- `bool m_FirstTimeCameraColorTargetIsBound`（bool m_第一个时间摄像机颜色目标是否Bound）(偏移: 0x0)
- `bool m_FirstTimeCameraDepthTargetIsBound`（bool m_第一个时间摄像机深度目标是否Bound）(偏移: 0x0)
- `bool m_IsPipelineExecuting`（bool m_是否PipelineExecuting）(偏移: 0x0)
- `bool isCameraColorTargetValid`（bool is摄像机颜色目标Valid）(偏移: 0x0)
- `RenderTargetIdentifier[] m_ActiveColorAttachments`（Render目标Identifier[] m_激活的颜色Attachments）(偏移: 0x8)
- `RenderTargetIdentifier m_ActiveDepthAttachment`（Render目标Identifier m_激活的深度Attachment）(偏移: 0xC)
- `RenderBufferStoreAction[] m_ActiveColorStoreActions`（Render缓冲区商店Action[] m_激活的颜色商店Actions）(偏移: 0x28)
- `RenderBufferStoreAction m_ActiveDepthStoreAction`（Render缓冲区商店动作 m_激活的深度商店动作）(偏移: 0x2C)
- `RenderTargetIdentifier[][] m_TrimmedColorAttachmentCopies`（Render目标Identifier[][] m_Trimmed颜色AttachmentCopies）(偏移: 0x30)

### 方法 (43)

- `RenderTargetIdentifier get_cameraDepth()`
  （Render目标Identifier get_camera深度（））
- `ProfilingSampler get_profilingExecute()`
  （ProfilingSampler get_profiling执行（））
- `void set_profilingExecute(ProfilingSampler value)`
  （void set_profiling执行（ProfilingSampler value））
- `void SetCameraMatrices(CommandBuffer cmd, ref CameraData cameraData, bool setInverseMatrices)`
  （void 集合摄像机Matrices（Command缓冲区 cmd, ref CameraData cameraData, bool setInverseMatrices））
- `void SetPerCameraShaderVariables(CommandBuffer cmd, ref CameraData cameraData)`
  （void 集合Per摄像机着色器Variables（Command缓冲区 cmd, ref CameraData cameraData））
- `void SetShaderTimeValues(CommandBuffer cmd, float time, float deltaTime, float smoothDeltaTime)`
  （void 集合着色器时间Values（Command缓冲区 cmd, float time, float deltaTime, float smoothDeltaTime））
- `RenderTargetIdentifier get_cameraColorTarget()`
  （Render目标Identifier get_camera颜色目标（））
- `RenderTargetIdentifier get_cameraDepthTarget()`
  （Render目标Identifier get_camera深度目标（））
- `List<ScriptableRendererFeature> get_rendererFeatures()`
  （List<Scriptable渲染器Feature> get_rendererFeatures（））
- `List<ScriptableRenderPass> get_activeRenderPassQueue()`
  （List<ScriptableRenderPass> get_activeRenderPass队列（））
- `ScriptableRenderer.RenderingFeatures get_supportedRenderingFeatures()`
  （ScriptableRenderer.RenderingFeatures get_supportedRenderingFeatures（））
- `void set_supportedRenderingFeatures(ScriptableRenderer.RenderingFeatures value)`
  （void set_supportedRenderingFeatures（ScriptableRenderer.RenderingFeatures value））
- `GraphicsDeviceType[] get_unsupportedGraphicsDeviceTypes()`
  （GraphicsDeviceType[] get_unsupportedGraphicsDeviceTypes（））
- `void set_unsupportedGraphicsDeviceTypes(GraphicsDeviceType[] value)`
  （void set_unsupportedGraphicsDeviceTypes（GraphicsDeviceType[] value））
- `void ConfigureActiveTarget(RenderTargetIdentifier colorAttachment, RenderTargetIdentifier depthAttachment)`
  （void Configure激活的目标（Render目标Identifier colorAttachment, Render目标Identifier depthAttachment））
- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））
- `void ConfigureCameraTarget(RenderTargetIdentifier colorTarget, RenderTargetIdentifier depthTarget)`
  （void Configure摄像机目标（Render目标Identifier colorTarget, Render目标Identifier depthTarget））
- `void ConfigureCameraColorTarget(RenderTargetIdentifier colorTarget)`
  （void Configure摄像机颜色目标（Render目标Identifier colorTarget））
- `void SetupLights(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void SetupLights（ScriptableRenderContext context, ref RenderingData renderingData））
- `void SetupCullingParameters(ref ScriptableCullingParameters cullingParameters, ref CameraData cameraData)`
  （void SetupCullingParameters（ref ScriptableCullingParameters cullingParameters, ref CameraData cameraData））
- `void FinishRendering(CommandBuffer cmd)`
  （void FinishRendering（Command缓冲区 cmd））
- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（ScriptableRenderContext context, ref RenderingData renderingData））
- `void EnqueuePass(ScriptableRenderPass pass)`
  （void EnqueuePass（ScriptableRenderPass pass））
- `ClearFlag GetCameraClearFlag(ref CameraData cameraData)`
  （清除标志 获取摄像机清除标志（ref CameraData cameraData））
- `void AddRenderPasses(ref RenderingData renderingData)`
  （void 添加RenderPasses（ref RenderingData renderingData））
- `void ClearRenderingState(CommandBuffer cmd)`
  （void 清除Rendering状态（Command缓冲区 cmd））
- `void Clear(CameraRenderType cameraType)`
  （void 清除（摄像机Render类型 cameraType））
- `void ExecuteBlock(int blockIndex, in ScriptableRenderer.RenderBlocks renderBlocks, ScriptableRenderContext context, ref RenderingData renderingData, bool submit = False)`
  （void 执行Block（int blockIndex, in ScriptableRenderer.RenderBlocks renderBlocks, ScriptableRenderContext context, ref RenderingData renderingData, bool submit = False））
- `void ExecuteRenderPass(ScriptableRenderContext context, ScriptableRenderPass renderPass, ref RenderingData renderingData)`
  （void 执行RenderPass（ScriptableRenderContext context, ScriptableRenderPass renderPass, ref RenderingData renderingData））
- `void SetRenderPassAttachments(CommandBuffer cmd, ScriptableRenderPass renderPass, ref CameraData cameraData)`
  （void 集合RenderPassAttachments（Command缓冲区 cmd, ScriptableRenderPass renderPass, ref CameraData cameraData））
- `void BeginXRRendering(CommandBuffer cmd, ScriptableRenderContext context, ref CameraData cameraData)`
  （void BeginXRRendering（Command缓冲区 cmd, ScriptableRenderContext context, ref CameraData cameraData））
- `void EndXRRendering(CommandBuffer cmd, ScriptableRenderContext context, ref CameraData cameraData)`
  （void 结束XRRendering（Command缓冲区 cmd, ScriptableRenderContext context, ref CameraData cameraData））
- `void SetRenderTarget(CommandBuffer cmd, RenderTargetIdentifier colorAttachment, RenderTargetIdentifier depthAttachment, ClearFlag clearFlag, Color clearColor)`
  （void 集合Render目标（Command缓冲区 cmd, Render目标Identifier colorAttachment, Render目标Identifier depthAttachment, 清除标志 clearFlag, 颜色 clearColor））
- `void SetRenderTarget(CommandBuffer cmd, RenderTargetIdentifier colorAttachment, RenderTargetIdentifier depthAttachment, ClearFlag clearFlag, Color clearColor, RenderBufferStoreAction colorStoreAction, RenderBufferStoreAction depthStoreAction)`
  （void 集合Render目标（Command缓冲区 cmd, Render目标Identifier colorAttachment, Render目标Identifier depthAttachment, 清除标志 clearFlag, 颜色 clearColor, Render缓冲区商店动作 colorStoreAction, Render缓冲区商店动作 depthStoreAction））
- `void SetRenderTarget(CommandBuffer cmd, RenderTargetIdentifier colorAttachment, RenderBufferLoadAction colorLoadAction, RenderBufferStoreAction colorStoreAction, ClearFlag clearFlags, Color clearColor)`
  （void 集合Render目标（Command缓冲区 cmd, Render目标Identifier colorAttachment, Render缓冲区加载动作 colorLoadAction, Render缓冲区商店动作 colorStoreAction, 清除标志 clearFlags, 颜色 clearColor））
- `void SetRenderTarget(CommandBuffer cmd, RenderTargetIdentifier colorAttachment, RenderBufferLoadAction colorLoadAction, RenderBufferStoreAction colorStoreAction, RenderTargetIdentifier depthAttachment, RenderBufferLoadAction depthLoadAction, RenderBufferStoreAction depthStoreAction, ClearFlag clearFlags, Color clearColor)`
  （void 集合Render目标（Command缓冲区 cmd, Render目标Identifier colorAttachment, Render缓冲区加载动作 colorLoadAction, Render缓冲区商店动作 colorStoreAction, Render目标Identifier depthAttachment, Render缓冲区加载动作 depthLoadAction, Render缓冲区商店动作 depthStoreAction, 清除标志 clearFlags, 颜色 clearColor））
- `void SetRenderTarget(CommandBuffer cmd, RenderTargetIdentifier[] colorAttachments, RenderTargetIdentifier depthAttachment, ClearFlag clearFlag, Color clearColor)`
  （void 集合Render目标（Command缓冲区 cmd, Render目标Identifier[] colorAttachments, Render目标Identifier depthAttachment, 清除标志 clearFlag, 颜色 clearColor））
- `void DrawGizmos(ScriptableRenderContext context, Camera camera, GizmoSubset gizmoSubset)`
  （void DrawGizmos（ScriptableRenderContext context, 摄像机 camera, GizmoSubset gizmoSubset））
- `void DrawWireOverlay(ScriptableRenderContext context, Camera camera)`
  （void DrawWireOverlay（ScriptableRenderContext context, 摄像机 camera））
- `void InternalStartRendering(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 内部的开始Rendering（ScriptableRenderContext context, ref RenderingData renderingData））
- `void InternalFinishRendering(ScriptableRenderContext context, bool resolveFinalTarget)`
  （void 内部的FinishRendering（ScriptableRenderContext context, bool resolveFinalTarget））
- `void SortStable(List<ScriptableRenderPass> list)`
  （void SortStable（List<ScriptableRenderPass> list））

---

## ScriptableRenderer.Profiling（ScriptableRenderer.Profiling）

### 字段 (8)

- `ProfilingSampler setPerCameraShaderVariables`（ProfilingSampler setPer摄像机着色器Variables）(偏移: 0x0)
- `ProfilingSampler sortRenderPasses`（ProfilingSampler sortRenderPasses）(偏移: 0x4)
- `ProfilingSampler setupLights`（ProfilingSampler setupLights）(偏移: 0x8)
- `ProfilingSampler setupCamera`（ProfilingSampler setup摄像机）(偏移: 0xC)
- `ProfilingSampler addRenderPasses`（ProfilingSampler addRenderPasses）(偏移: 0x10)
- `ProfilingSampler clearRenderingState`（ProfilingSampler clearRendering状态）(偏移: 0x14)
- `ProfilingSampler internalStartRendering`（ProfilingSampler internal开始Rendering）(偏移: 0x18)
- `ProfilingSampler internalFinishRendering`（ProfilingSampler internalFinishRendering）(偏移: 0x1C)

---

## ScriptableRenderer.Profiling.RenderBlock（ScriptableRenderer.Profiling.RenderBlock）

### 字段 (4)

- `ProfilingSampler beforeRendering`（ProfilingSampler beforeRendering）(偏移: 0x0)
- `ProfilingSampler mainRenderingOpaque`（ProfilingSampler mainRendering不透明的）(偏移: 0x4)
- `ProfilingSampler mainRenderingTransparent`（ProfilingSampler mainRendering透明的）(偏移: 0x8)
- `ProfilingSampler afterRendering`（ProfilingSampler afterRendering）(偏移: 0xC)

---

## ScriptableRenderer.Profiling.RenderPass（ScriptableRenderer.Profiling.RenderPass）

### 字段 (1)

- `ProfilingSampler configure`（ProfilingSampler configure）(偏移: 0x31D231B3)

---

## ScriptableRenderer.RenderBlocks（ScriptableRenderer.RenderBlocks）

**继承**: IDisposable（IDisposable）

### 字段 (3)

- `NativeArray<RenderPassEvent> m_BlockEventLimits`（NativeArray<RenderPassEvent> m_Block事件Limits）(偏移: 0x0)
- `NativeArray<int> m_BlockRanges`（NativeArray<int> m_BlockRanges）(偏移: 0xC)
- `NativeArray<int> m_BlockRangeLengths`（NativeArray<int> m_Block范围Lengths）(偏移: 0x18)

### 方法 (4)

- `void Dispose()`
  （void 释放（））
- `void FillBlockRanges(List<ScriptableRenderPass> activeRenderPassQueue)`
  （void FillBlockRanges（List<ScriptableRenderPass> activeRenderPassQueue））
- `int GetLength(int index)`
  （int 获取Length（int index））
- `ScriptableRenderer.RenderBlocks.BlockRange GetRange(int index)`
  （ScriptableRenderer.RenderBlocks.Block范围 获取范围（int index））

---

## ScriptableRenderer.RenderBlocks.BlockRange（ScriptableRenderer.RenderBlocks.Block范围）

**继承**: IDisposable（IDisposable）

### 字段 (2)

- `int m_Current`（int m_当前）(偏移: 0x0)
- `int m_End`（int m_结束）(偏移: 0x4)

### 方法 (4)

- `ScriptableRenderer.RenderBlocks.BlockRange GetEnumerator()`
  （ScriptableRenderer.RenderBlocks.Block范围 获取Enumerator（））
- `bool MoveNext()`
  （bool 移动下一个（））
- `int get_Current()`
  （int get_当前（））
- `void Dispose()`
  （void 释放（））

---

## ScriptableRenderer.RenderPassBlock（ScriptableRenderer.RenderPassBlock）

### 字段 (4)

- `int BeforeRendering`（int BeforeRendering）(偏移: 0x0)
- `int MainRenderingOpaque`（int 主要的Rendering不透明的）(偏移: 0x4)
- `int MainRenderingTransparent`（int 主要的Rendering透明的）(偏移: 0x8)
- `int AfterRendering`（int AfterRendering）(偏移: 0xC)

---

## ScriptableRenderer.RenderingFeatures（ScriptableRenderer.RenderingFeatures）

### 方法 (4)

- `bool get_cameraStacking()`
  （bool get_cameraStacking（））
- `void set_cameraStacking(bool value)`
  （void set_cameraStacking（bool value））
- `bool get_msaa()`
  （bool get_msaa（））
- `void set_msaa(bool value)`
  （void set_msaa（bool value））

---

## ScriptableRendererData（Scriptable渲染器数据）

**继承**: ScriptableObject（脚本对象）

### 字段 (2)

- `List<ScriptableRendererFeature> m_RendererFeatures`（List<Scriptable渲染器Feature> m_渲染器Features）(偏移: 0x10)
- `List<long> m_RendererFeatureMap`（List<long> m_渲染器Feature映射）(偏移: 0x14)

### 方法 (7)

- `bool get_isInvalidated()`
  （bool get_isInvalidated（））
- `void set_isInvalidated(bool value)`
  （void set_isInvalidated（bool value））
- `List<ScriptableRendererFeature> get_rendererFeatures()`
  （List<Scriptable渲染器Feature> get_rendererFeatures（））
- `void SetDirty()`
  （void 集合Dirty（））
- `ScriptableRenderer InternalCreateRenderer()`
  （Scriptable渲染器 内部的创建渲染器（））
- `void OnValidate()`
  （void On验证（））
- `void OnEnable()`
  （void On启用（））

---

## ScriptableRendererFeature（Scriptable渲染器Feature）

**继承**: ScriptableObject, IDisposable（脚本对象, IDisposable）

### 字段 (1)

- `bool m_Active`（bool m_激活的）(偏移: 0xC)

### 方法 (6)

- `bool get_isActive()`
  （bool get_is激活的（））
- `void OnEnable()`
  （void On启用（））
- `void OnValidate()`
  （void On验证（））
- `void SetActive(bool active)`
  （void 集合激活的（bool active））
- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））

---

## ScriptableRuntimeReflectionSystemSettings（ScriptableRuntimeReflection系统Settings）

### 字段 (1)

- `ScriptableRuntimeReflectionSystemWrapper s_Instance`（ScriptableRuntimeReflection系统包装器 s_实例）(偏移: 0x0)

### 方法 (3)

- `void set_Internal_ScriptableRuntimeReflectionSystemSettings_system(IScriptableRuntimeReflectionSystem value)`
  （void set_Internal_ScriptableRuntimeReflection系统Settings_system（IScriptableRuntimeReflection系统 value））
- `ScriptableRuntimeReflectionSystemWrapper get_Internal_ScriptableRuntimeReflectionSystemSettings_instance()`
  （ScriptableRuntimeReflection系统包装器 get_Internal_ScriptableRuntimeReflection系统Settings_instance（））
- `void ScriptingDirtyReflectionSystemInstance()`
  （void ScriptingDirtyReflection系统实例（））

---

## ScriptableRuntimeReflectionSystemWrapper（ScriptableRuntimeReflection系统包装器）

### 方法 (3)

- `IScriptableRuntimeReflectionSystem get_implementation()`
  （IScriptableRuntimeReflection系统 get_implementation（））
- `void set_implementation(IScriptableRuntimeReflectionSystem value)`
  （void set_implementation（IScriptableRuntimeReflection系统 value））
- `void Internal_ScriptableRuntimeReflectionSystemWrapper_TickRealtimeProbes(out bool result)`
  （void Internal_ScriptableRuntimeReflection系统Wrapper_TickRealtimeProbes（out bool result））

---

## ScriptingUtility（Scripting工具）

### 方法 (1)

- `bool IsManagedCodeWorking()`
  （bool 是否ManagedCodeWorking（））

---

## ScriptingUtility.TestClass（ScriptingUtility.Test类）

### 字段 (1)

- `int value`（int value）(偏移: 0x0)

---

## ScrollRect（滚动Rect）

**继承**: UIBehaviour, IInitializePotentialDragHandler, IEventSystemHandler, IBeginDragHandler, IEndDragHandler, IDragHandler, IScrollHandler, ICanvasElement, ILayoutElement, ILayoutGroup, ILayoutController（界面Behaviour, I初始化PotentialDrag处理器, I事件系统处理器, IBeginDrag处理器, I结束Drag处理器, IDrag处理器, I滚动处理器, I画布元素, ILayout元素, ILayout组, ILayout控制器）

### 字段 (37)

- `RectTransform m_Content`（Rect变换 m_Content）(偏移: 0xC)
- `bool m_Horizontal`（bool m_水平）(偏移: 0x10)
- `bool m_Vertical`（bool m_垂直）(偏移: 0x11)
- `ScrollRect.MovementType m_MovementType`（滚动Rect.Movement类型 m_Movement类型）(偏移: 0x14)
- `float m_Elasticity`（float m_Elasticity）(偏移: 0x18)
- `bool m_Inertia`（bool m_Inertia）(偏移: 0x1C)
- `float m_DecelerationRate`（float m_DecelerationRate）(偏移: 0x20)
- `float m_ScrollSensitivity`（float m_滚动Sensitivity）(偏移: 0x24)
- `RectTransform m_Viewport`（Rect变换 m_Viewport）(偏移: 0x28)
- `Scrollbar m_HorizontalScrollbar`（Scrollbar m_水平Scrollbar）(偏移: 0x2C)
- `Scrollbar m_VerticalScrollbar`（Scrollbar m_垂直Scrollbar）(偏移: 0x30)
- `ScrollRect.ScrollbarVisibility m_HorizontalScrollbarVisibility`（滚动Rect.ScrollbarVisibility m_水平ScrollbarVisibility）(偏移: 0x34)
- `ScrollRect.ScrollbarVisibility m_VerticalScrollbarVisibility`（滚动Rect.ScrollbarVisibility m_垂直ScrollbarVisibility）(偏移: 0x38)
- `float m_HorizontalScrollbarSpacing`（float m_水平ScrollbarSpacing）(偏移: 0x3C)
- `float m_VerticalScrollbarSpacing`（float m_垂直ScrollbarSpacing）(偏移: 0x40)
- `ScrollRect.ScrollRectEvent m_OnValueChanged`（滚动Rect.滚动Rect事件 m_On值Changed）(偏移: 0x44)
- `Vector2 m_PointerStartLocalCursor`（二维向量 m_指针开始本地的Cursor）(偏移: 0x48)
- `Vector2 m_ContentStartPosition`（二维向量 m_Content开始Position）(偏移: 0x50)
- `RectTransform m_ViewRect`（Rect变换 m_视图Rect）(偏移: 0x58)
- `Bounds m_ContentBounds`（Bounds m_ContentBounds）(偏移: 0x5C)
- `Bounds m_ViewBounds`（Bounds m_视图Bounds）(偏移: 0x74)
- `Vector2 m_Velocity`（二维向量 m_速度）(偏移: 0x8C)
- `bool m_Dragging`（bool m_Dragging）(偏移: 0x94)
- `bool m_Scrolling`（bool m_Scrolling）(偏移: 0x95)
- `Vector2 m_PrevPosition`（二维向量 m_PrevPosition）(偏移: 0x98)
- `Bounds m_PrevContentBounds`（Bounds m_PrevContentBounds）(偏移: 0xA0)
- `Bounds m_PrevViewBounds`（Bounds m_Prev视图Bounds）(偏移: 0xB8)
- `bool m_HasRebuiltLayout`（bool m_是否有RebuiltLayout）(偏移: 0xD0)
- `bool m_HSliderExpand`（bool m_H滑块Expand）(偏移: 0xD1)
- `bool m_VSliderExpand`（bool m_V滑块Expand）(偏移: 0xD2)
- `float m_HSliderHeight`（float m_H滑块高度）(偏移: 0xD4)
- `float m_VSliderWidth`（float m_V滑块宽度）(偏移: 0xD8)
- `RectTransform m_Rect`（Rect变换 m_Rect）(偏移: 0xDC)
- `RectTransform m_HorizontalScrollbarRect`（Rect变换 m_水平ScrollbarRect）(偏移: 0xE0)
- `RectTransform m_VerticalScrollbarRect`（Rect变换 m_垂直ScrollbarRect）(偏移: 0xE4)
- `DrivenRectTransformTracker m_Tracker`（DrivenRect变换Tracker m_Tracker）(偏移: 0xE8)
- `Vector3[] m_Corners`（Vector3[] m_Corners）(偏移: 0xEC)

### 方法 (89)

- `RectTransform get_content()`
  （Rect变换 get_content（））
- `void set_content(RectTransform value)`
  （void set_content（Rect变换 value））
- `bool get_horizontal()`
  （bool get_horizontal（））
- `void set_horizontal(bool value)`
  （void set_horizontal（bool value））
- `bool get_vertical()`
  （bool get_vertical（））
- `void set_vertical(bool value)`
  （void set_vertical（bool value））
- `ScrollRect.MovementType get_movementType()`
  （滚动Rect.Movement类型 get_movement类型（））
- `void set_movementType(ScrollRect.MovementType value)`
  （void set_movement类型（滚动Rect.Movement类型 value））
- `float get_elasticity()`
  （float get_elasticity（））
- `void set_elasticity(float value)`
  （void set_elasticity（float value））
- `bool get_inertia()`
  （bool get_inertia（））
- `void set_inertia(bool value)`
  （void set_inertia（bool value））
- `float get_decelerationRate()`
  （float get_decelerationRate（））
- `void set_decelerationRate(float value)`
  （void set_decelerationRate（float value））
- `float get_scrollSensitivity()`
  （float get_scrollSensitivity（））
- `void set_scrollSensitivity(float value)`
  （void set_scrollSensitivity（float value））
- `RectTransform get_viewport()`
  （Rect变换 get_viewport（））
- `void set_viewport(RectTransform value)`
  （void set_viewport（Rect变换 value））
- `Scrollbar get_horizontalScrollbar()`
  （Scrollbar get_horizontalScrollbar（））
- `void set_horizontalScrollbar(Scrollbar value)`
  （void set_horizontalScrollbar（Scrollbar value））
- `Scrollbar get_verticalScrollbar()`
  （Scrollbar get_verticalScrollbar（））
- `void set_verticalScrollbar(Scrollbar value)`
  （void set_verticalScrollbar（Scrollbar value））
- `ScrollRect.ScrollbarVisibility get_horizontalScrollbarVisibility()`
  （滚动Rect.ScrollbarVisibility get_horizontalScrollbarVisibility（））
- `void set_horizontalScrollbarVisibility(ScrollRect.ScrollbarVisibility value)`
  （void set_horizontalScrollbarVisibility（滚动Rect.ScrollbarVisibility value））
- `ScrollRect.ScrollbarVisibility get_verticalScrollbarVisibility()`
  （滚动Rect.ScrollbarVisibility get_verticalScrollbarVisibility（））
- `void set_verticalScrollbarVisibility(ScrollRect.ScrollbarVisibility value)`
  （void set_verticalScrollbarVisibility（滚动Rect.ScrollbarVisibility value））
- `float get_horizontalScrollbarSpacing()`
  （float get_horizontalScrollbarSpacing（））
- `void set_horizontalScrollbarSpacing(float value)`
  （void set_horizontalScrollbarSpacing（float value））
- `float get_verticalScrollbarSpacing()`
  （float get_verticalScrollbarSpacing（））
- `void set_verticalScrollbarSpacing(float value)`
  （void set_verticalScrollbarSpacing（float value））
- `ScrollRect.ScrollRectEvent get_onValueChanged()`
  （滚动Rect.滚动Rect事件 get_on值Changed（））
- `void set_onValueChanged(ScrollRect.ScrollRectEvent value)`
  （void set_on值Changed（滚动Rect.滚动Rect事件 value））
- `RectTransform get_viewRect()`
  （Rect变换 get_viewRect（））
- `Vector2 get_velocity()`
  （二维向量 get_velocity（））
- `void set_velocity(Vector2 value)`
  （void set_velocity（二维向量 value））
- `RectTransform get_rectTransform()`
  （Rect变换 get_rect变换（））
- `void Rebuild(CanvasUpdate executing)`
  （void Rebuild（画布更新 executing））
- `void LayoutComplete()`
  （void LayoutComplete（））
- `void GraphicUpdateComplete()`
  （void Graphic更新Complete（））
- `void UpdateCachedData()`
  （void 更新Cached数据（））
- `void OnEnable()`
  （void On启用（））
- `void OnDisable()`
  （void On禁用（））
- `bool IsActive()`
  （bool 是否激活的（））
- `void EnsureLayoutHasRebuilt()`
  （void EnsureLayout是否有Rebuilt（））
- `void StopMovement()`
  （void 停止Movement（））
- `void OnScroll(PointerEventData data)`
  （void On滚动（指针事件数据 data））
- `void OnInitializePotentialDrag(PointerEventData eventData)`
  （void On初始化PotentialDrag（指针事件数据 eventData））
- `void OnBeginDrag(PointerEventData eventData)`
  （void OnBeginDrag（指针事件数据 eventData））
- `void OnEndDrag(PointerEventData eventData)`
  （void On结束Drag（指针事件数据 eventData））
- `void OnDrag(PointerEventData eventData)`
  （void OnDrag（指针事件数据 eventData））
- `void SetContentAnchoredPosition(Vector2 position)`
  （void 集合ContentAnchoredPosition（二维向量 position））
- `void LateUpdate()`
  （void 延迟更新（））
- `void UpdatePrevData()`
  （void 更新Prev数据（））
- `void UpdateScrollbars(Vector2 offset)`
  （void 更新Scrollbars（二维向量 offset））
- `Vector2 get_normalizedPosition()`
  （二维向量 get_normalizedPosition（））
- `void set_normalizedPosition(Vector2 value)`
  （void set_normalizedPosition（二维向量 value））
- `float get_horizontalNormalizedPosition()`
  （float get_horizontalNormalizedPosition（））
- `void set_horizontalNormalizedPosition(float value)`
  （void set_horizontalNormalizedPosition（float value））
- `float get_verticalNormalizedPosition()`
  （float get_verticalNormalizedPosition（））
- `void set_verticalNormalizedPosition(float value)`
  （void set_verticalNormalizedPosition（float value））
- `void SetHorizontalNormalizedPosition(float value)`
  （void 集合水平NormalizedPosition（float value））
- `void SetVerticalNormalizedPosition(float value)`
  （void 集合垂直NormalizedPosition（float value））
- `void SetNormalizedPosition(float value, int axis)`
  （void 集合NormalizedPosition（float value, int axis））
- `float RubberDelta(float overStretching, float viewSize)`
  （float RubberDelta（float overStretching, float viewSize））
- `void OnRectTransformDimensionsChange()`
  （void OnRect变换DimensionsChange（））
- `bool get_hScrollingNeeded()`
  （bool get_hScrollingNeeded（））
- `bool get_vScrollingNeeded()`
  （bool get_vScrollingNeeded（））
- `void CalculateLayoutInputHorizontal()`
  （void 计算Layout输入水平（））
- `void CalculateLayoutInputVertical()`
  （void 计算Layout输入垂直（））
- `float get_minWidth()`
  （float get_min宽度（））
- `float get_preferredWidth()`
  （float get_preferred宽度（））
- `float get_flexibleWidth()`
  （float get_flexible宽度（））
- `float get_minHeight()`
  （float get_min高度（））
- `float get_preferredHeight()`
  （float get_preferred高度（））
- `float get_flexibleHeight()`
  （float get_flexible高度（））
- `int get_layoutPriority()`
  （int get_layoutPriority（））
- `void SetLayoutHorizontal()`
  （void 集合Layout水平（））
- `void SetLayoutVertical()`
  （void 集合Layout垂直（））
- `void UpdateScrollbarVisibility()`
  （void 更新ScrollbarVisibility（））
- `void UpdateOneScrollbarVisibility(bool xScrollingNeeded, bool xAxisEnabled, ScrollRect.ScrollbarVisibility scrollbarVisibility, Scrollbar scrollbar)`
  （void 更新OneScrollbarVisibility（bool xScrollingNeeded, bool xAxisEnabled, 滚动Rect.ScrollbarVisibility scrollbarVisibility, Scrollbar scrollbar））
- `void UpdateScrollbarLayout()`
  （void 更新ScrollbarLayout（））
- `void UpdateBounds()`
  （void 更新Bounds（））
- `void AdjustBounds(ref Bounds viewBounds, ref Vector2 contentPivot, ref Vector3 contentSize, ref Vector3 contentPos)`
  （void AdjustBounds（ref Bounds viewBounds, ref Vector2 contentPivot, ref Vector3 contentSize, ref Vector3 contentPos））
- `Bounds GetBounds()`
  （Bounds 获取Bounds（））
- `Bounds InternalGetBounds(Vector3[] corners, ref Matrix4x4 viewWorldToLocalMatrix)`
  （Bounds 内部的获取Bounds（Vector3[] corners, ref Matrix4x4 viewWorldToLocalMatrix））
- `Vector2 CalculateOffset(Vector2 delta)`
  （二维向量 计算Offset（二维向量 delta））
- `Vector2 InternalCalculateOffset(ref Bounds viewBounds, ref Bounds contentBounds, bool horizontal, bool vertical, ScrollRect.MovementType movementType, ref Vector2 delta)`
  （二维向量 内部的计算Offset（ref Bounds viewBounds, ref Bounds contentBounds, bool horizontal, bool vertical, 滚动Rect.Movement类型 movementType, ref Vector2 delta））
- `void SetDirty()`
  （void 集合Dirty（））
- `void SetDirtyCaching()`
  （void 集合DirtyCaching（））

---

## ScrollRect.MovementType（滚动Rect.Movement类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ScrollRect.ScrollbarVisibility（滚动Rect.ScrollbarVisibility）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Scrollbar（Scrollbar）

**继承**: Selectable, IBeginDragHandler, IEventSystemHandler, IDragHandler, IInitializePotentialDragHandler, ICanvasElement（Selectable, IBeginDrag处理器, I事件系统处理器, IDrag处理器, I初始化PotentialDrag处理器, I画布元素）

### 字段 (12)

- `RectTransform m_HandleRect`（Rect变换 m_句柄Rect）(偏移: 0xB0)
- `Scrollbar.Direction m_Direction`（Scrollbar.方向 m_方向）(偏移: 0xB4)
- `float m_Value`（float m_值）(偏移: 0xB8)
- `float m_Size`（float m_大小）(偏移: 0xBC)
- `int m_NumberOfSteps`（int m_NumberOfSteps）(偏移: 0xC0)
- `Scrollbar.ScrollEvent m_OnValueChanged`（Scrollbar.滚动事件 m_On值Changed）(偏移: 0xC4)
- `RectTransform m_ContainerRect`（Rect变换 m_容器Rect）(偏移: 0xC8)
- `Vector2 m_Offset`（二维向量 m_Offset）(偏移: 0xCC)
- `DrivenRectTransformTracker m_Tracker`（DrivenRect变换Tracker m_Tracker）(偏移: 0xD4)
- `Coroutine m_PointerDownRepeat`（协程 m_指针下Repeat）(偏移: 0xD8)
- `bool isPointerDownAndNotDragging`（bool is指针下AndNotDragging）(偏移: 0xDC)
- `bool m_DelayedUpdateVisuals`（bool m_Delayed更新Visuals）(偏移: 0xDD)

### 方法 (42)

- `RectTransform get_handleRect()`
  （Rect变换 get_handleRect（））
- `void set_handleRect(RectTransform value)`
  （void set_handleRect（Rect变换 value））
- `Scrollbar.Direction get_direction()`
  （Scrollbar.方向 get_direction（））
- `void set_direction(Scrollbar.Direction value)`
  （void set_direction（Scrollbar.方向 value））
- `float get_value()`
  （float get_value（））
- `void set_value(float value)`
  （void set_value（float value））
- `void SetValueWithoutNotify(float input)`
  （void 集合值WithoutNotify（float input））
- `float get_size()`
  （float get_size（））
- `void set_size(float value)`
  （void set_size（float value））
- `int get_numberOfSteps()`
  （int get_numberOfSteps（））
- `void set_numberOfSteps(int value)`
  （void set_numberOfSteps（int value））
- `Scrollbar.ScrollEvent get_onValueChanged()`
  （Scrollbar.滚动事件 get_on值Changed（））
- `void set_onValueChanged(Scrollbar.ScrollEvent value)`
  （void set_on值Changed（Scrollbar.滚动事件 value））
- `float get_stepSize()`
  （float get_step大小（））
- `void Rebuild(CanvasUpdate executing)`
  （void Rebuild（画布更新 executing））
- `void LayoutComplete()`
  （void LayoutComplete（））
- `void GraphicUpdateComplete()`
  （void Graphic更新Complete（））
- `void OnEnable()`
  （void On启用（））
- `void OnDisable()`
  （void On禁用（））
- `void Update()`
  （void 更新（））
- `void UpdateCachedReferences()`
  （void 更新CachedReferences（））
- `void Set(float input, bool sendCallback = True)`
  （void 集合（float input, bool sendCallback = True））
- `void OnRectTransformDimensionsChange()`
  （void OnRect变换DimensionsChange（））
- `Scrollbar.Axis get_axis()`
  （Scrollbar.轴 get_axis（））
- `bool get_reverseValue()`
  （bool get_reverse值（））
- `void UpdateVisuals()`
  （void 更新Visuals（））
- `void UpdateDrag(PointerEventData eventData)`
  （void 更新Drag（指针事件数据 eventData））
- `void DoUpdateDrag(Vector2 handleCorner, float remainingSize)`
  （void Do更新Drag（二维向量 handleCorner, float remainingSize））
- `bool MayDrag(PointerEventData eventData)`
  （bool MayDrag（指针事件数据 eventData））
- `void OnBeginDrag(PointerEventData eventData)`
  （void OnBeginDrag（指针事件数据 eventData））
- `void OnDrag(PointerEventData eventData)`
  （void OnDrag（指针事件数据 eventData））
- `void OnPointerDown(PointerEventData eventData)`
  （void On指针下（指针事件数据 eventData））
- `IEnumerator ClickRepeat(PointerEventData eventData)`
  （IEnumerator ClickRepeat（指针事件数据 eventData））
- `IEnumerator ClickRepeat(Vector2 screenPosition, Camera camera)`
  （IEnumerator ClickRepeat（二维向量 screenPosition, 摄像机 camera））
- `void OnPointerUp(PointerEventData eventData)`
  （void On指针上（指针事件数据 eventData））
- `void OnMove(AxisEventData eventData)`
  （void On移动（轴事件数据 eventData））
- `Selectable FindSelectableOnLeft()`
  （Selectable 查找SelectableOn左（））
- `Selectable FindSelectableOnRight()`
  （Selectable 查找SelectableOn右（））
- `Selectable FindSelectableOnUp()`
  （Selectable 查找SelectableOn上（））
- `Selectable FindSelectableOnDown()`
  （Selectable 查找SelectableOn下（））
- `void OnInitializePotentialDrag(PointerEventData eventData)`
  （void On初始化PotentialDrag（指针事件数据 eventData））
- `void SetDirection(Scrollbar.Direction direction, bool includeRectLayouts)`
  （void 集合方向（Scrollbar.方向 direction, bool includeRectLayouts））

---

## Scrollbar.Axis（Scrollbar.轴）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Scrollbar.Direction（Scrollbar.方向）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SearchOption（搜索Option）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SearchResult（搜索Result）

### 字段 (3)

- `string fullPath`（string full路径）(偏移: 0x8)
- `string userPath`（string user路径）(偏移: 0xC)
- `Win32Native.WIN32_FIND_DATA findData`（Win32Native.WIN32_FIND_DATA find数据）(偏移: 0x10)

### 方法 (2)

- `string get_UserPath()`
  （string get_User路径（））
- `Win32Native.WIN32_FIND_DATA get_FindData()`
  （Win32Native.WIN32_FIND_DATA get_查找数据（））

---

## SecurityElement（Security元素）

### 字段 (9)

- `string text`（string text）(偏移: 0x8)
- `string tag`（string tag）(偏移: 0xC)
- `ArrayList attributes`（数组列表 attributes）(偏移: 0x10)
- `ArrayList children`（数组列表 children）(偏移: 0x14)
- `char[] invalid_tag_chars`（char[] invalid_tag_chars）(偏移: 0x0)
- `char[] invalid_text_chars`（char[] invalid_text_chars）(偏移: 0x4)
- `char[] invalid_attr_name_chars`（char[] invalid_attr_name_chars）(偏移: 0x8)
- `char[] invalid_attr_value_chars`（char[] invalid_attr_value_chars）(偏移: 0xC)
- `char[] invalid_chars`（char[] invalid_chars）(偏移: 0x10)

### 方法 (17)

- `Hashtable get_Attributes()`
  （Hashtable get_Attributes（））
- `ArrayList get_Children()`
  （数组列表 get_Children（））
- `string get_Tag()`
  （string get_标签（））
- `string get_Text()`
  （string get_文本（））
- `void set_Text(string value)`
  （void set_文本（string value））
- `void AddAttribute(string name, string value)`
  （void 添加Attribute（string name, string value））
- `void AddChild(SecurityElement child)`
  （void 添加子级（Security元素 child））
- `string Escape(string str)`
  （string Escape（string str））
- `string Unescape(string str)`
  （string Unescape（string str））
- `SecurityElement FromString(string xml)`
  （Security元素 From字符串（string xml））
- `bool IsValidAttributeName(string name)`
  （bool 是否ValidAttribute名称（string name））
- `bool IsValidAttributeValue(string value)`
  （bool 是否ValidAttribute值（string value））
- `bool IsValidTag(string tag)`
  （bool 是否Valid标签（string tag））
- `bool IsValidText(string text)`
  （bool 是否Valid文本（string text））
- `string ToString()`
  （string To字符串（））
- `void ToXml(ref StringBuilder s, int level)`
  （void ToXml（ref StringBuilder s, int level））
- `SecurityElement.SecurityAttribute GetAttribute(string name)`
  （SecurityElement.SecurityAttribute 获取Attribute（string name））

---

## SecurityElement.SecurityAttribute（SecurityElement.SecurityAttribute）

### 字段 (2)

- `string _name`（string _name）(偏移: 0x8)
- `string _value`（string _value）(偏移: 0xC)

### 方法 (2)

- `string get_Name()`
  （string get_名称（））
- `string get_Value()`
  （string get_值（））

---

## SecurityException（SecurityException）

**继承**: SystemException（系统Exception）

### 字段 (1)

- `string permissionState`（string permission状态）(偏移: 0x44)

### 方法 (2)

- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））
- `string ToString()`
  （string To字符串（））

---

## SecurityManager（Security管理器）

### 方法 (2)

- `bool CheckElevatedPermissions()`
  （bool 检查ElevatedPermissions（））
- `void EnsureElevatedPermissions()`
  （void EnsureElevatedPermissions（））

---

## SecurityParser（SecurityParser）

**继承**: SmallXmlParser, SmallXmlParser.IContentHandler（SmallXmlParser, SmallXmlParser.IContent处理器）

### 字段 (3)

- `SecurityElement root`（Security元素 root）(偏移: 0x38)
- `SecurityElement current`（Security元素 current）(偏移: 0x3C)
- `Stack stack`（栈 stack）(偏移: 0x40)

### 方法 (9)

- `void LoadXml(string xml)`
  （void 加载Xml（string xml））
- `SecurityElement ToXml()`
  （Security元素 ToXml（））
- `void OnStartParsing(SmallXmlParser parser)`
  （void On开始Parsing（SmallXmlParser parser））
- `void OnProcessingInstruction(string name, string text)`
  （void OnProcessingInstruction（string name, string text））
- `void OnIgnorableWhitespace(string s)`
  （void OnIgnorableWhitespace（string s））
- `void OnStartElement(string name, SmallXmlParser.IAttrList attrs)`
  （void On开始元素（string name, SmallXmlParser.IAttr列表 attrs））
- `void OnEndElement(string name)`
  （void On结束元素（string name））
- `void OnChars(string ch)`
  （void OnChars（string ch））
- `void OnEndParsing(SmallXmlParser parser)`
  （void On结束Parsing（SmallXmlParser parser））

---

## SecurityUtils（SecurityUtils）

### 方法 (7)

- `void DemandReflectionAccess(Type type)`
  （void DemandReflectionAccess（类型 type））
- `bool HasReflectionPermission(Type type)`
  （bool 是否有ReflectionPermission（类型 type））
- `object SecureCreateInstance(Type type)`
  （object Secure创建实例（类型 type））
- `object SecureCreateInstance(Type type, object[] args, bool allowNonPublic)`
  （object Secure创建实例（类型 type, object[] args, bool allowNonPublic））
- `object SecureCreateInstance(Type type, object[] args)`
  （object Secure创建实例（类型 type, object[] args））
- `object SecureConstructorInvoke(Type type, Type[] argTypes, object[] args, bool allowNonPublic)`
  （object SecureConstructorInvoke（类型 type, Type[] argTypes, object[] args, bool allowNonPublic））
- `object SecureConstructorInvoke(Type type, Type[] argTypes, object[] args, bool allowNonPublic, BindingFlags extraFlags)`
  （object SecureConstructorInvoke（类型 type, Type[] argTypes, object[] args, bool allowNonPublic, BindingFlags extraFlags））

---

## SeekOrigin（SeekOrigin）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Seeker（Seeker）

**继承**: VersionedMonoBehaviour（VersionedMonoBehaviour）

### 字段 (19)

- `bool drawGizmos`（bool drawGizmos）(偏移: 0x10)
- `bool detailedGizmos`（bool detailedGizmos）(偏移: 0x11)
- `StartEndModifier startEndModifier`（开始结束修改器 start结束修改器）(偏移: 0x14)
- `int traversableTags`（int traversableTags）(偏移: 0x18)
- `int[] tagPenalties`（int[] tagPenalties）(偏移: 0x1C)
- `GraphMask graphMask`（Graph掩码 graph掩码）(偏移: 0x20)
- `int graphMaskCompatibility`（int graph掩码Compatibility）(偏移: 0x24)
- `OnPathDelegate pathCallback`（On路径委托 path回调）(偏移: 0x28)
- `OnPathDelegate preProcessPath`（On路径委托 pre处理路径）(偏移: 0x2C)
- `OnPathDelegate postProcessPath`（On路径委托 post处理路径）(偏移: 0x30)
- `List<Vector3> lastCompletedVectorPath`（List<Vector3> lastCompleted向量路径）(偏移: 0x34)
- `List<GraphNode> lastCompletedNodePath`（List<GraphNode> lastCompleted节点路径）(偏移: 0x38)
- `Path path`（路径 path）(偏移: 0x3C)
- `Path prevPath`（路径 prev路径）(偏移: 0x40)
- `OnPathDelegate onPathDelegate`（On路径委托 on路径委托）(偏移: 0x44)
- `OnPathDelegate onPartialPathDelegate`（On路径委托 onPartial路径委托）(偏移: 0x48)
- `OnPathDelegate tmpPathCallback`（On路径委托 tmp路径回调）(偏移: 0x4C)
- `uint lastPathID`（uint last路径ID）(偏移: 0x50)
- `List<IPathModifier> modifiers`（List<I路径Modifier> modifiers）(偏移: 0x54)

### 方法 (26)

- `void Awake()`
  （void Awake（））
- `Path GetCurrentPath()`
  （路径 获取当前路径（））
- `void CancelCurrentPathRequest(bool pool = True)`
  （void 取消当前路径请求（bool pool = True））
- `void OnDestroy()`
  （void On销毁（））
- `void ReleaseClaimedPath()`
  （void ReleaseClaimed路径（））
- `void RegisterModifier(IPathModifier modifier)`
  （void Register修改器（I路径修改器 modifier））
- `void DeregisterModifier(IPathModifier modifier)`
  （void Deregister修改器（I路径修改器 modifier））
- `void PostProcess(Path path)`
  （void Post处理（路径 path））
- `void RunModifiers(Seeker.ModifierPass pass, Path path)`
  （void 运行Modifiers（Seeker.修改器Pass pass, 路径 path））
- `bool IsDone()`
  （bool 是否Done（））
- `void OnPathComplete(Path path)`
  （void On路径Complete（路径 path））
- `void OnPathComplete(Path p, bool runModifiers, bool sendCallbacks)`
  （void On路径Complete（路径 p, bool runModifiers, bool sendCallbacks））
- `void OnPartialPathComplete(Path p)`
  （void OnPartial路径Complete（路径 p））
- `void OnMultiPathComplete(Path p)`
  （void On多个路径Complete（路径 p））
- `ABPath GetNewPath(Vector3 start, Vector3 end)`
  （AB路径 获取新的路径（三维向量 start, 三维向量 end））
- `Path StartPath(Vector3 start, Vector3 end)`
  （路径 开始路径（三维向量 start, 三维向量 end））
- `Path StartPath(Vector3 start, Vector3 end, OnPathDelegate callback)`
  （路径 开始路径（三维向量 start, 三维向量 end, On路径委托 callback））
- `Path StartPath(Vector3 start, Vector3 end, OnPathDelegate callback, GraphMask graphMask)`
  （路径 开始路径（三维向量 start, 三维向量 end, On路径委托 callback, Graph掩码 graphMask））
- `Path StartPath(Path p, OnPathDelegate callback)`
  （路径 开始路径（路径 p, On路径委托 callback））
- `Path StartPath(Path p, OnPathDelegate callback, GraphMask graphMask)`
  （路径 开始路径（路径 p, On路径委托 callback, Graph掩码 graphMask））
- `void StartPathInternal(Path p, OnPathDelegate callback)`
  （void 开始路径内部的（路径 p, On路径委托 callback））
- `MultiTargetPath StartMultiTargetPath(Vector3 start, Vector3[] endPoints, bool pathsForAll, OnPathDelegate callback, int graphMask = -1)`
  （多个目标路径 开始多个目标路径（三维向量 start, Vector3[] endPoints, bool pathsForAll, On路径委托 callback, int graphMask = -1））
- `MultiTargetPath StartMultiTargetPath(Vector3[] startPoints, Vector3 end, bool pathsForAll, OnPathDelegate callback, int graphMask = -1)`
  （多个目标路径 开始多个目标路径（Vector3[] startPoints, 三维向量 end, bool pathsForAll, On路径委托 callback, int graphMask = -1））
- `MultiTargetPath StartMultiTargetPath(MultiTargetPath p, OnPathDelegate callback, int graphMask = -1)`
  （多个目标路径 开始多个目标路径（多个目标路径 p, On路径委托 callback, int graphMask = -1））
- `void OnDrawGizmos()`
  （void OnDrawGizmos（））
- `int OnUpgradeSerializedData(int version, bool unityThread)`
  （int OnUpgradeSerialized数据（int version, bool unityThread））

---

## Seeker.ModifierPass（Seeker.修改器Pass）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Selectable（Selectable）

**继承**: UIBehaviour, IMoveHandler, IEventSystemHandler, IPointerDownHandler, IPointerUpHandler, IPointerEnterHandler, IPointerExitHandler, ISelectHandler, IDeselectHandler（界面Behaviour, I移动处理器, I事件系统处理器, I指针下处理器, I指针上处理器, I指针Enter处理器, I指针Exit处理器, I选择处理器, I取消选择处理器）

### 字段 (13)

- `Selectable[] s_Selectables`（Selectable[] s_Selectables）(偏移: 0x0)
- `int s_SelectableCount`（int s_Selectable数量）(偏移: 0x4)
- `bool m_EnableCalled`（bool m_启用Called）(偏移: 0xC)
- `Navigation m_Navigation`（Navigation m_Navigation）(偏移: 0x10)
- `Selectable.Transition m_Transition`（Selectable.Transition m_Transition）(偏移: 0x28)
- `ColorBlock m_Colors`（颜色Block m_Colors）(偏移: 0x2C)
- `SpriteState m_SpriteState`（精灵状态 m_精灵状态）(偏移: 0x84)
- `AnimationTriggers m_AnimationTriggers`（动画Triggers m_动画Triggers）(偏移: 0x94)
- `bool m_Interactable`（bool m_Interactable）(偏移: 0x98)
- `Graphic m_TargetGraphic`（Graphic m_目标Graphic）(偏移: 0x9C)
- `bool m_GroupsAllowInteraction`（bool m_Groups允许Interaction）(偏移: 0xA0)
- `int m_CurrentIndex`（int m_当前索引）(偏移: 0xA4)
- `List<CanvasGroup> m_CanvasGroupCache`（List<画布Group> m_画布组缓存）(偏移: 0xAC)

### 方法 (59)

- `Selectable[] get_allSelectablesArray()`
  （Selectable[] get_allSelectables数组（））
- `int get_allSelectableCount()`
  （int get_allSelectable数量（））
- `List<Selectable> get_allSelectables()`
  （List<Selectable> get_allSelectables（））
- `int AllSelectablesNoAlloc(Selectable[] selectables)`
  （int 所有SelectablesNoAlloc（Selectable[] selectables））
- `Navigation get_navigation()`
  （Navigation get_navigation（））
- `void set_navigation(Navigation value)`
  （void set_navigation（Navigation value））
- `Selectable.Transition get_transition()`
  （Selectable.Transition get_transition（））
- `void set_transition(Selectable.Transition value)`
  （void set_transition（Selectable.Transition value））
- `ColorBlock get_colors()`
  （颜色Block get_colors（））
- `void set_colors(ColorBlock value)`
  （void set_colors（颜色Block value））
- `SpriteState get_spriteState()`
  （精灵状态 get_sprite状态（））
- `void set_spriteState(SpriteState value)`
  （void set_sprite状态（精灵状态 value））
- `AnimationTriggers get_animationTriggers()`
  （动画Triggers get_animationTriggers（））
- `void set_animationTriggers(AnimationTriggers value)`
  （void set_animationTriggers（动画Triggers value））
- `Graphic get_targetGraphic()`
  （Graphic get_targetGraphic（））
- `void set_targetGraphic(Graphic value)`
  （void set_targetGraphic（Graphic value））
- `bool get_interactable()`
  （bool get_interactable（））
- `void set_interactable(bool value)`
  （void set_interactable（bool value））
- `bool get_isPointerInside()`
  （bool get_is指针Inside（））
- `void set_isPointerInside(bool value)`
  （void set_is指针Inside（bool value））
- `bool get_isPointerDown()`
  （bool get_is指针下（））
- `void set_isPointerDown(bool value)`
  （void set_is指针下（bool value））
- `bool get_hasSelection()`
  （bool get_hasSelection（））
- `void set_hasSelection(bool value)`
  （void set_hasSelection（bool value））
- `Image get_image()`
  （图像 get_image（））
- `void set_image(Image value)`
  （void set_image（图像 value））
- `Animator get_animator()`
  （动画器 get_animator（））
- `void Awake()`
  （void Awake（））
- `void OnCanvasGroupChanged()`
  （void On画布组Changed（））
- `bool IsInteractable()`
  （bool 是否Interactable（））
- `void OnDidApplyAnimationProperties()`
  （void OnDid应用动画Properties（））
- `void OnEnable()`
  （void On启用（））
- `void OnTransformParentChanged()`
  （void On变换父级Changed（））
- `void OnSetProperty()`
  （void On集合属性（））
- `void OnDisable()`
  （void On禁用（））
- `Selectable.SelectionState get_currentSelectionState()`
  （Selectable.Selection状态 get_currentSelection状态（））
- `void InstantClearState()`
  （void Instant清除状态（））
- `void DoStateTransition(Selectable.SelectionState state, bool instant)`
  （void Do状态Transition（Selectable.Selection状态 state, bool instant））
- `Selectable FindSelectable(Vector3 dir)`
  （Selectable 查找Selectable（三维向量 dir））
- `Vector3 GetPointOnRectEdge(RectTransform rect, Vector2 dir)`
  （三维向量 获取PointOnRectEdge（Rect变换 rect, 二维向量 dir））
- `void Navigate(AxisEventData eventData, Selectable sel)`
  （void Navigate（轴事件数据 eventData, Selectable sel））
- `Selectable FindSelectableOnLeft()`
  （Selectable 查找SelectableOn左（））
- `Selectable FindSelectableOnRight()`
  （Selectable 查找SelectableOn右（））
- `Selectable FindSelectableOnUp()`
  （Selectable 查找SelectableOn上（））
- `Selectable FindSelectableOnDown()`
  （Selectable 查找SelectableOn下（））
- `void OnMove(AxisEventData eventData)`
  （void On移动（轴事件数据 eventData））
- `void StartColorTween(Color targetColor, bool instant)`
  （void 开始颜色Tween（颜色 targetColor, bool instant））
- `void DoSpriteSwap(Sprite newSprite)`
  （void Do精灵Swap（精灵 newSprite））
- `void TriggerAnimation(string triggername)`
  （void 触发器动画（string triggername））
- `bool IsHighlighted()`
  （bool 是否Highlighted（））
- `bool IsPressed()`
  （bool 是否按下的（））
- `void EvaluateAndTransitionToSelectionState()`
  （void EvaluateAndTransitionToSelection状态（））
- `void OnPointerDown(PointerEventData eventData)`
  （void On指针下（指针事件数据 eventData））
- `void OnPointerUp(PointerEventData eventData)`
  （void On指针上（指针事件数据 eventData））
- `void OnPointerEnter(PointerEventData eventData)`
  （void On指针Enter（指针事件数据 eventData））
- `void OnPointerExit(PointerEventData eventData)`
  （void On指针Exit（指针事件数据 eventData））
- `void OnSelect(BaseEventData eventData)`
  （void On选择（基础事件数据 eventData））
- `void OnDeselect(BaseEventData eventData)`
  （void On取消选择（基础事件数据 eventData））
- `void Select()`
  （void 选择（））

---

## Selectable.SelectionState（Selectable.Selection状态）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Selectable.Transition（Selectable.Transition）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SemanticMeaning（SemanticMeaning）

### 字段 (2)

- `string key`（string key）(偏移: 0x0)
- `string[] values`（string[] values）(偏移: 0x4)

---

## SemaphoreSlim（SemaphoreSlim）

**继承**: IDisposable（IDisposable）

### 字段 (9)

- `int m_currentCount`（int m_current数量）(偏移: 0x8)
- `int m_maxCount`（int m_max数量）(偏移: 0xC)
- `int m_waitCount`（int m_wait数量）(偏移: 0x10)
- `object m_lockObj`（object m_lockObj）(偏移: 0x14)
- `ManualResetEvent m_waitHandle`（手动重置事件 m_wait句柄）(偏移: 0x18)
- `SemaphoreSlim.TaskNode m_asyncHead`（SemaphoreSlim.Task节点 m_async头部）(偏移: 0x1C)
- `SemaphoreSlim.TaskNode m_asyncTail`（SemaphoreSlim.Task节点 m_asyncTail）(偏移: 0x20)
- `Task<bool> s_trueTask`（Task<bool> s_trueTask）(偏移: 0x0)
- `Action<object> s_cancellationTokenCanceledEventHandler`（Action<object> s_cancellation令牌Canceled事件处理器）(偏移: 0x4)

### 方法 (16)

- `void Wait()`
  （void Wait（））
- `bool Wait(int millisecondsTimeout, CancellationToken cancellationToken)`
  （bool Wait（int millisecondsTimeout, Cancellation令牌 cancellationToken））
- `bool WaitUntilCountOrTimeout(int millisecondsTimeout, uint startTime, CancellationToken cancellationToken)`
  （bool WaitUntil数量Or超时（int millisecondsTimeout, uint startTime, Cancellation令牌 cancellationToken））
- `Task WaitAsync()`
  （Task Wait异步（））
- `Task<bool> WaitAsync(int millisecondsTimeout, CancellationToken cancellationToken)`
  （Task<bool> Wait异步（int millisecondsTimeout, Cancellation令牌 cancellationToken））
- `SemaphoreSlim.TaskNode CreateAndAddAsyncWaiter()`
  （SemaphoreSlim.Task节点 创建And添加异步Waiter（））
- `bool RemoveAsyncWaiter(SemaphoreSlim.TaskNode task)`
  （bool 移除异步Waiter（SemaphoreSlim.Task节点 task））
- `Task<bool> WaitUntilCountOrTimeoutAsync(SemaphoreSlim.TaskNode asyncWaiter, int millisecondsTimeout, CancellationToken cancellationToken)`
  （Task<bool> WaitUntil数量Or超时异步（SemaphoreSlim.Task节点 asyncWaiter, int millisecondsTimeout, Cancellation令牌 cancellationToken））
- `int Release()`
  （int Release（））
- `int Release(int releaseCount)`
  （int Release（int releaseCount））
- `void QueueWaiterTask(SemaphoreSlim.TaskNode waiterTask)`
  （void 队列WaiterTask（SemaphoreSlim.Task节点 waiterTask））
- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））
- `void CancellationTokenCanceledEventHandler(object obj)`
  （void Cancellation令牌Canceled事件处理器（object obj））
- `void CheckDispose()`
  （void 检查释放（））
- `string GetResourceString(string str)`
  （string 获取资源字符串（string str））

---

## SemaphoreSlim.TaskNode（SemaphoreSlim.Task节点）

**继承**: Task<bool>, IThreadPoolWorkItem（Task<bool>, IThread池Work项目）

### 字段 (2)

- `SemaphoreSlim.TaskNode Prev`（SemaphoreSlim.Task节点 Prev）(偏移: 0x2C)
- `SemaphoreSlim.TaskNode Next`（SemaphoreSlim.Task节点 下一个）(偏移: 0x30)

---

## SendMessageOptions（发送MessageOptions）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SendMouseEvents（发送鼠标Events）

### 字段 (5)

- `bool s_MouseUsed`（bool s_鼠标Used）(偏移: 0x0)
- `SendMouseEvents.HitInfo[] m_LastHit`（发送鼠标Events.命中Info[] m_最后一个命中）(偏移: 0x4)
- `SendMouseEvents.HitInfo[] m_MouseDownHit`（发送鼠标Events.命中Info[] m_鼠标下命中）(偏移: 0x8)
- `SendMouseEvents.HitInfo[] m_CurrentHit`（发送鼠标Events.命中Info[] m_当前命中）(偏移: 0xC)
- `Camera[] m_Cameras`（Camera[] m_Cameras）(偏移: 0x10)

### 方法 (3)

- `void SetMouseMoved()`
  （void 集合鼠标Moved（））
- `void DoSendMouseEvents(int skipRTCameras)`
  （void Do发送鼠标Events（int skipRTCameras））
- `void SendEvents(int i, SendMouseEvents.HitInfo hit)`
  （void 发送Events（int i, 发送鼠标Events.命中信息 hit））

---

## SendMouseEvents.HitInfo（发送鼠标Events.命中信息）

### 字段 (2)

- `GameObject target`（游戏对象 target）(偏移: 0x0)
- `Camera camera`（摄像机 camera）(偏移: 0x4)

### 方法 (3)

- `void SendMessage(string name)`
  （void 发送Message（string name））
- `bool op_Implicit(SendMouseEvents.HitInfo exists)`
  （bool op_Implicit（发送鼠标Events.命中信息 exists））
- `bool Compare(SendMouseEvents.HitInfo lhs, SendMouseEvents.HitInfo rhs)`
  （bool Compare（发送鼠标Events.命中信息 lhs, 发送鼠标Events.命中信息 rhs））

---

## SendOrPostCallback（发送OrPost回调）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(object state)`
  （void Invoke（object state））
- `IAsyncResult BeginInvoke(object state, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（object state, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## SentryGun（Sentry枪械）

**继承**: Entity（实体）

### 字段 (14)

- `Transform head`（变换 head）(偏移: 0x48)
- `ParticleSystem fireFX`（粒子系统 fireFX）(偏移: 0x4C)
- `GameObject expFX`（游戏对象 expFX）(偏移: 0x50)
- `Vector3 headLocalEuler`（三维向量 head本地的Euler）(偏移: 0x54)
- `RecyclableObject RO`（Recyclable对象 RO）(偏移: 0x60)
- `Player owner`（玩家 owner）(偏移: 0x64)
- `RecyclableSound sound`（Recyclable音效 sound）(偏移: 0x68)
- `SentryGun.State state`（SentryGun.状态 state）(偏移: 0x6C)
- `WD_SentryGun wpnData`（WD_Sentry枪械 武器数据）(偏移: 0x70)
- `DamageEventData dmgData`（伤害事件数据 dmg数据）(偏移: 0x74)
- `Entity enemy`（实体 enemy）(偏移: 0xBC)
- `int nextEnemyID`（int nextEnemyID）(偏移: 0xC0)
- `float nextAttackTime`（float nextAttack时间）(偏移: 0xC4)
- `HUD_HealthBar healthBar`（HUD_HealthBar healthBar）(偏移: 0xC8)

### 方法 (18)

- `void Awake()`
  （void Awake（））
- `void Update()`
  （void 更新（））
- `void OnEnable()`
  （void On启用（））
- `void EnterIdleState()`
  （void Enter待机状态（））
- `void Spawn()`
  （void 出生（））
- `void OnRecycle()`
  （void OnRecycle（））
- `void OnEntityHurt(DamageEventData eventData)`
  （void On实体Hurt（伤害事件数据 eventData））
- `void OnEntityDeath(DeathEventData eventData)`
  （void On实体死亡（死亡事件数据 eventData））
- `void FindEnemy()`
  （void 查找Enemy（））
- `bool CheckEnemy(Entity target)`
  （bool 检查Enemy（实体 target））
- `void AttackEnemy()`
  （void AttackEnemy（））
- `void HeadRotation()`
  （void 头部Rotation（））
- `void SetData(Player owner, WD_SentryGun wpnData, Vector3 position)`
  （void 集合数据（玩家 owner, WD_Sentry枪械 wpnData, 三维向量 position））
- `Transform GetVisibleHitBox(Ray viewRay)`
  （变换 获取可见的命中Box（Ray viewRay））
- `void CreateExplosion()`
  （void 创建Explosion（））
- `void SetState(SentryGun.State newState)`
  （void 集合状态（SentryGun.状态 newState））
- `string GetName()`
  （string 获取名称（））
- `void AddHealthBar()`
  （void 添加HealthBar（））

---

## SentryGun（Sentry枪械）

**继承**: BotSkillBase（机器人技能基础）

### 字段 (1)

- `Skill_SentryGun bindSkill`（Skill_Sentry枪械 bind技能）(偏移: 0x18)

### 方法 (2)

- `void OnActionFinish()`
  （void On动作Finish（））
- `bool CanDo()`
  （bool 能否Do（））

---

## SentryGun.State（SentryGun.状态）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SentryGunSystem（Sentry枪械系统）

**继承**: Singleton<SentryGunSystem>（Singleton<Sentry枪械System>）

### 字段 (1)

- `NameKeyPool pool`（名称键池 pool）(偏移: 0xC)

### 方法 (2)

- `void Awake()`
  （void Awake（））
- `RecyclableObject Get(GameObject prefab)`
  （Recyclable对象 获取（游戏对象 prefab））

---

## Sequence（Sequence）

**继承**: Tween（Tween）

### 字段 (3)

- `List<Tween> sequencedTweens`（List<Tween> sequencedTweens）(偏移: 0xC4)
- `List<ABSSequentiable> _sequencedObjs`（List<ABSSequentiable> _sequencedObjs）(偏移: 0xC8)
- `float lastTweenInsertTime`（float lastTweenInsert时间）(偏移: 0xCC)

### 方法 (16)

- `Sequence DoPrepend(Sequence inSequence, Tween t)`
  （Sequence DoPrepend（Sequence inSequence, Tween t））
- `Sequence DoInsert(Sequence inSequence, Tween t, float atPosition)`
  （Sequence DoInsert（Sequence inSequence, Tween t, float atPosition））
- `Sequence DoAppendInterval(Sequence inSequence, float interval)`
  （Sequence DoAppend间隔（Sequence inSequence, float interval））
- `Sequence DoPrependInterval(Sequence inSequence, float interval)`
  （Sequence DoPrepend间隔（Sequence inSequence, float interval））
- `Sequence DoInsertCallback(Sequence inSequence, TweenCallback callback, float atPosition)`
  （Sequence DoInsert回调（Sequence inSequence, Tween回调 callback, float atPosition））
- `float UpdateDelay(float elapsed)`
  （float 更新延迟（float elapsed））
- `void Reset()`
  （void 重置（））
- `bool Validate()`
  （bool 验证（））
- `bool Startup()`
  （bool Startup（））
- `bool ApplyTween(float prevPosition, int prevCompletedLoops, int newCompletedSteps, bool useInversePosition, UpdateMode updateMode, UpdateNotice updateNotice)`
  （bool 应用Tween（float prevPosition, int prevCompletedLoops, int newCompletedSteps, bool useInversePosition, 更新模式 updateMode, 更新Notice updateNotice））
- `void Setup(Sequence s)`
  （void Setup（Sequence s））
- `bool DoStartup(Sequence s)`
  （bool DoStartup（Sequence s））
- `bool DoApplyTween(Sequence s, float prevPosition, int prevCompletedLoops, int newCompletedSteps, bool useInversePosition, UpdateMode updateMode)`
  （bool Do应用Tween（Sequence s, float prevPosition, int prevCompletedLoops, int newCompletedSteps, bool useInversePosition, 更新模式 updateMode））
- `bool ApplyInternalCycle(Sequence s, float fromPos, float toPos, UpdateMode updateMode, bool useInverse, bool prevPosIsInverse, bool multiCycleStep = False)`
  （bool 应用内部的Cycle（Sequence s, float fromPos, float toPos, 更新模式 updateMode, bool useInverse, bool prevPosIsInverse, bool multiCycleStep = False））
- `void StableSortSequencedObjs(List<ABSSequentiable> list)`
  （void StableSortSequencedObjs（List<ABSSequentiable> list））
- `bool IsAnyCallbackSet(Sequence s)`
  （bool 是否任意回调集合（Sequence s））

---

## SequentialSearchPrimeGeneratorBase（Sequential搜索PrimeGenerator基础）

**继承**: PrimeGeneratorBase（PrimeGenerator基础）

### 方法 (4)

- `BigInteger GenerateSearchBase(int bits, object context)`
  （BigInteger Generate搜索基础（int bits, object context））
- `BigInteger GenerateNewPrime(int bits)`
  （BigInteger Generate新的Prime（int bits））
- `BigInteger GenerateNewPrime(int bits, object context)`
  （BigInteger Generate新的Prime（int bits, object context））
- `bool IsPrimeAcceptable(BigInteger bi, object context)`
  （bool 是否PrimeAcceptable（BigInteger bi, object context））

---

## SerObjectInfoCache（Ser对象信息缓存）

### 字段 (6)

- `string fullTypeName`（string full类型名称）(偏移: 0x8)
- `string assemblyString`（string assembly字符串）(偏移: 0xC)
- `bool hasTypeForwardedFrom`（bool has类型ForwardedFrom）(偏移: 0x10)
- `MemberInfo[] memberInfos`（MemberInfo[] memberInfos）(偏移: 0x14)
- `string[] memberNames`（string[] memberNames）(偏移: 0x18)
- `Type[] memberTypes`（Type[] memberTypes）(偏移: 0x1C)

---

## SerObjectInfoInit（Ser对象信息初始化）

### 字段 (3)

- `Hashtable seenBeforeTable`（Hashtable seenBeforeTable）(偏移: 0x8)
- `int objectInfoIdCount`（int object信息Id数量）(偏移: 0xC)
- `SerStack oiPool`（Ser栈 oi池）(偏移: 0x10)

---

## SerStack（Ser栈）

### 字段 (3)

- `object[] objects`（object[] objects）(偏移: 0x8)
- `string stackId`（string stackId）(偏移: 0xC)
- `int top`（int top）(偏移: 0x10)

### 方法 (6)

- `void Push(object obj)`
  （void Push（object obj））
- `object Pop()`
  （object Pop（））
- `void IncreaseCapacity()`
  （void IncreaseCapacity（））
- `object Peek()`
  （object Peek（））
- `object PeekPeek()`
  （object PeekPeek（））
- `bool IsEmpty()`
  （bool 是否空（））

---

## SerializationBinder（SerializationBinder）

### 方法 (1)

- `void BindToName(Type serializedType, out string assemblyName, out string typeName)`
  （void BindTo名称（类型 serializedType, out string assemblyName, out string typeName））

---

## SerializationEntry（SerializationEntry）

### 字段 (3)

- `Type m_type`（类型 m_type）(偏移: 0x0)
- `object m_value`（object m_value）(偏移: 0x4)
- `string m_name`（string m_name）(偏移: 0x8)

### 方法 (2)

- `object get_Value()`
  （object get_值（））
- `string get_Name()`
  （string get_名称（））

---

## SerializationEventHandler（Serialization事件处理器）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(StreamingContext context)`
  （void Invoke（StreamingContext context））
- `IAsyncResult BeginInvoke(StreamingContext context, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（StreamingContext context, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## SerializationEvents（SerializationEvents）

### 字段 (4)

- `List<MethodInfo> m_OnSerializingMethods`（List<MethodInfo> m_OnSerializingMethods）(偏移: 0x8)
- `List<MethodInfo> m_OnSerializedMethods`（List<MethodInfo> m_OnSerializedMethods）(偏移: 0xC)
- `List<MethodInfo> m_OnDeserializingMethods`（List<MethodInfo> m_OnDeserializingMethods）(偏移: 0x10)
- `List<MethodInfo> m_OnDeserializedMethods`（List<MethodInfo> m_OnDeserializedMethods）(偏移: 0x14)

### 方法 (7)

- `List<MethodInfo> GetMethodsWithAttribute(Type attribute, Type t)`
  （List<MethodInfo> 获取MethodsWithAttribute（类型 attribute, 类型 t））
- `bool get_HasOnSerializingEvents()`
  （bool get_是否有OnSerializingEvents（））
- `void InvokeOnSerializing(object obj, StreamingContext context)`
  （void InvokeOnSerializing（object obj, StreamingContext context））
- `void InvokeOnDeserializing(object obj, StreamingContext context)`
  （void InvokeOnDeserializing（object obj, StreamingContext context））
- `void InvokeOnDeserialized(object obj, StreamingContext context)`
  （void InvokeOnDeserialized（object obj, StreamingContext context））
- `SerializationEventHandler AddOnSerialized(object obj, SerializationEventHandler handler)`
  （Serialization事件处理器 添加OnSerialized（object obj, Serialization事件处理器 handler））
- `SerializationEventHandler AddOnDeserialized(object obj, SerializationEventHandler handler)`
  （Serialization事件处理器 添加OnDeserialized（object obj, Serialization事件处理器 handler））

---

## SerializationEventsCache（SerializationEvents缓存）

### 字段 (1)

- `Hashtable cache`（Hashtable cache）(偏移: 0x0)

### 方法 (1)

- `SerializationEvents GetSerializationEventsForType(Type t)`
  （SerializationEvents 获取SerializationEventsFor类型（类型 t））

---

