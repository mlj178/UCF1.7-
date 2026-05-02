# 游戏类定义 (Part 4/21)

共 200 个类 (总序号 601 - 800)

---

## CinemachineVirtualCameraBase.TransitionParams（Cinemachine虚拟的摄像机Base.TransitionParams）

### 字段 (3)

- `CinemachineVirtualCameraBase.BlendHint m_BlendHint`（Cinemachine虚拟的摄像机Base.BlendHint m_BlendHint）(偏移: 0x0)
- `bool m_InheritPosition`（bool m_InheritPosition）(偏移: 0x4)
- `CinemachineBrain.VcamActivatedEvent m_OnCameraLive`（CinemachineBrain.VcamActivated事件 m_On摄像机Live）(偏移: 0x8)

---

## CinemachineVolumeSettings（CinemachineVolumeSettings）

**继承**: CinemachineExtension（Cinemachine扩展）

### 字段 (8)

- `float s_VolumePriority`（float s_VolumePriority）(偏移: 0x0)
- `bool m_FocusTracksTarget`（bool m_聚焦Tracks目标）(偏移: 0x14)
- `CinemachineVolumeSettings.FocusTrackingMode m_FocusTracking`（CinemachineVolumeSettings.聚焦Tracking模式 m_聚焦Tracking）(偏移: 0x18)
- `Transform m_FocusTarget`（变换 m_聚焦目标）(偏移: 0x1C)
- `float m_FocusOffset`（float m_聚焦Offset）(偏移: 0x20)
- `VolumeProfile m_Profile`（VolumeProfile m_Profile）(偏移: 0x24)
- `string sVolumeOwnerName`（string sVolumeOwner名称）(偏移: 0x4)
- `List<Volume> sVolumes`（List<Volume> sVolumes）(偏移: 0x8)

### 方法 (9)

- `bool get_IsValid()`
  （bool get_是否Valid（））
- `void InvalidateCachedProfile()`
  （void InvalidateCachedProfile（））
- `void OnEnable()`
  （void On启用（））
- `void OnDestroy()`
  （void On销毁（））
- `void PostPipelineStageCallback(CinemachineVirtualCameraBase vcam, CinemachineCore.Stage stage, ref CameraState state, float deltaTime)`
  （void PostPipelineStage回调（Cinemachine虚拟的摄像机基础 vcam, CinemachineCore.Stage stage, ref CameraState state, float deltaTime））
- `void OnCameraCut(CinemachineBrain brain)`
  （void On摄像机Cut（Cinemachine爆头 brain））
- `void ApplyPostFX(CinemachineBrain brain)`
  （void 应用PostFX（Cinemachine爆头 brain））
- `List<Volume> GetDynamicBrainVolumes(CinemachineBrain brain, int minVolumes)`
  （List<Volume> 获取动态的爆头Volumes（Cinemachine爆头 brain, int minVolumes））
- `void InitializeModule()`
  （void 初始化模块（））

---

## CinemachineVolumeSettings.FocusTrackingMode（CinemachineVolumeSettings.聚焦Tracking模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## CinemachineVolumeSettings.VcamExtraState（CinemachineVolumeSettings.Vcam额外的状态）

### 字段 (1)

- `VolumeProfile mProfileCopy`（VolumeProfile mProfile复制）(偏移: 0x8)

### 方法 (2)

- `void CreateProfileCopy(VolumeProfile source)`
  （void 创建Profile复制（VolumeProfile source））
- `void DestroyProfileCopy()`
  （void 销毁Profile复制（））

---

## CipherMode（Cipher模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## CircleOptions（CircleOptions）

**继承**: IPlugOptions（IPlugOptions）

### 字段 (7)

- `float endValueDegrees`（float end值Degrees）(偏移: 0x0)
- `bool relativeCenter`（bool relative中心）(偏移: 0x4)
- `bool snapping`（bool snapping）(偏移: 0x5)
- `Vector2 center`（二维向量 center）(偏移: 0x8)
- `float radius`（float radius）(偏移: 0x10)
- `float startValueDegrees`（float start值Degrees）(偏移: 0x14)
- `bool initialized`（bool initialized）(偏移: 0x18)

### 方法 (2)

- `void Reset()`
  （void 重置（））
- `void Initialize(Vector2 startValue, Vector2 endValue)`
  （void 初始化（二维向量 startValue, 二维向量 endValue））

---

## CirclePlugin（Circle插件）

**继承**: ABSTweenPlugin<Vector2, Vector2, CircleOptions>（ABSTweenPlugin<二维向量, 二维向量, CircleOptions>）

### 方法 (9)

- `void Reset(TweenerCore<Vector2, Vector2, CircleOptions> t)`
  （void 重置（TweenerCore<二维向量, 二维向量, CircleOptions> t））
- `void SetFrom(TweenerCore<Vector2, Vector2, CircleOptions> t, bool isRelative)`
  （void 集合From（TweenerCore<二维向量, 二维向量, CircleOptions> t, bool isRelative））
- `void SetFrom(TweenerCore<Vector2, Vector2, CircleOptions> t, Vector2 fromValue, bool setImmediately, bool isRelative)`
  （void 集合From（TweenerCore<二维向量, 二维向量, CircleOptions> t, 二维向量 fromValue, bool setImmediately, bool isRelative））
- `Vector2 ConvertToStartValue(TweenerCore<Vector2, Vector2, CircleOptions> t, Vector2 value)`
  （二维向量 转换To开始值（TweenerCore<二维向量, 二维向量, CircleOptions> t, 二维向量 value））
- `void SetRelativeEndValue(TweenerCore<Vector2, Vector2, CircleOptions> t)`
  （void 集合Relative结束值（TweenerCore<二维向量, 二维向量, CircleOptions> t））
- `void SetChangeValue(TweenerCore<Vector2, Vector2, CircleOptions> t)`
  （void 集合Change值（TweenerCore<二维向量, 二维向量, CircleOptions> t））
- `float GetSpeedBasedDuration(CircleOptions options, float unitsXSecond, Vector2 changeValue)`
  （float 获取SpeedBased持续时间（CircleOptions options, float unitsXSecond, 二维向量 changeValue））
- `void EvaluateAndApply(CircleOptions options, Tween t, bool isRelative, DOGetter<Vector2> getter, DOSetter<Vector2> setter, float elapsed, Vector2 startValue, Vector2 changeValue, float duration, bool usingInversePosition, UpdateNotice updateNotice)`
  （void EvaluateAnd应用（CircleOptions options, Tween t, bool isRelative, DOGetter<Vector2> getter, DOSetter<Vector2> setter, float elapsed, 二维向量 startValue, 二维向量 changeValue, float duration, bool usingInversePosition, 更新Notice updateNotice））
- `Vector2 GetPositionOnCircle(CircleOptions options, float degrees)`
  （二维向量 获取PositionOnCircle（CircleOptions options, float degrees））

---

## ClampedFloatParameter（Clamped浮点数Parameter）

**继承**: FloatParameter（浮点数Parameter）

### 字段 (2)

- `float min`（float min）(偏移: 0x10)
- `float max`（float max）(偏移: 0x14)

### 方法 (2)

- `float get_value()`
  （float get_value（））
- `void set_value(float value)`
  （void set_value（float value））

---

## ClampedIntParameter（Clamped整数Parameter）

**继承**: IntParameter（整数Parameter）

### 字段 (2)

- `int min`（int min）(偏移: 0x10)
- `int max`（int max）(偏移: 0x14)

### 方法 (2)

- `int get_value()`
  （int get_value（））
- `void set_value(int value)`
  （void set_value（int value））

---

## ClassInterfaceAttribute（类InterfaceAttribute）

**继承**: Attribute（Attribute）

### 字段 (1)

- `ClassInterfaceType _val`（类Interface类型 _val）(偏移: 0x8)

---

## ClassInterfaceType（类Interface类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ClassLibraryInitializer（类LibraryInitializer）

### 方法 (1)

- `void Init()`
  （void 初始化（））

---

## ClearFlag（清除标志）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ClientActivatedIdentity（客户端ActivatedIdentity）

**继承**: ServerIdentity（服务器Identity）

### 字段 (1)

- `MarshalByRefObject _targetThis`（MarshalByRef对象 _targetThis）(偏移: 0x38)

### 方法 (5)

- `MarshalByRefObject GetServerObject()`
  （MarshalByRef对象 获取服务器对象（））
- `void SetClientProxy(MarshalByRefObject obj)`
  （void 集合客户端代理（MarshalByRef对象 obj））
- `void OnLifetimeExpired()`
  （void OnLifetimeExpired（））
- `IMessage SyncObjectProcessMessage(IMessage msg)`
  （IMessage 同步对象处理Message（IMessage msg））
- `IMessageCtrl AsyncObjectProcessMessage(IMessage msg, IMessageSink replySink)`
  （IMessageCtrl 异步对象处理Message（IMessage msg, IMessageSink replySink））

---

## ClientContextReplySink（客户端ContextReplySink）

**继承**: IMessageSink（IMessageSink）

### 字段 (2)

- `IMessageSink _replySink`（IMessageSink _replySink）(偏移: 0x8)
- `Context _context`（Context _context）(偏移: 0xC)

### 方法 (2)

- `IMessage SyncProcessMessage(IMessage msg)`
  （IMessage 同步处理Message（IMessage msg））
- `IMessageCtrl AsyncProcessMessage(IMessage msg, IMessageSink replySink)`
  （IMessageCtrl 异步处理Message（IMessage msg, IMessageSink replySink））

---

## ClientContextTerminatorSink（客户端ContextTerminatorSink）

**继承**: IMessageSink（IMessageSink）

### 字段 (1)

- `Context _context`（Context _context）(偏移: 0x8)

### 方法 (2)

- `IMessage SyncProcessMessage(IMessage msg)`
  （IMessage 同步处理Message（IMessage msg））
- `IMessageCtrl AsyncProcessMessage(IMessage msg, IMessageSink replySink)`
  （IMessageCtrl 异步处理Message（IMessage msg, IMessageSink replySink））

---

## ClientData（客户端数据）

### 字段 (11)

- `ClientData mine`（客户端数据 mine）(偏移: 0x0)
- `int defaultWpnBagID`（int default武器背包ID）(偏移: 0x8)
- `int[][] wpnBags`（int[][] 武器Bags）(偏移: 0xC)
- `string nickName`（string nick名称）(偏移: 0x10)
- `int level`（int level）(偏移: 0x14)
- `Team joinTeam`（队伍 join队伍）(偏移: 0x18)
- `bool isBot`（bool is机器人）(偏移: 0x1C)
- `int vipLevel`（int vip等级）(偏移: 0x20)
- `int character`（int character）(偏移: 0x24)
- `List<int> itemList`（List<int> item列表）(偏移: 0x28)
- `ClientData.ClipBuffInfo clipBuffInfo`（客户端Data.弹匣增益信息 clip增益信息）(偏移: 0x0)

### 方法 (30)

- `bool get_haveNanoCloth()`
  （bool get_have纳米服装（））
- `void set_haveNanoCloth(bool value)`
  （void set_have纳米服装（bool value））
- `bool get_haveNanoAmmo()`
  （bool get_have纳米弹药（））
- `void set_haveNanoAmmo(bool value)`
  （void set_have纳米弹药（bool value））
- `bool get_haveRifleAmmo()`
  （bool get_have步枪弹药（））
- `void set_haveRifleAmmo(bool value)`
  （void set_have步枪弹药（bool value））
- `bool get_haveShotGunAmmo()`
  （bool get_have射击枪械弹药（））
- `void set_haveShotGunAmmo(bool value)`
  （void set_have射击枪械弹药（bool value））
- `bool get_haveMgAmmo()`
  （bool get_haveMg弹药（））
- `void set_haveMgAmmo(bool value)`
  （void set_haveMg弹药（bool value））
- `bool get_haveSmgAmmo()`
  （bool get_haveSmg弹药（））
- `void set_haveSmgAmmo(bool value)`
  （void set_haveSmg弹药（bool value））
- `bool get_haveSniperAmmo()`
  （bool get_have狙击弹药（））
- `void set_haveSniperAmmo(bool value)`
  （void set_have狙击弹药（bool value））
- `bool get_havePistolAmmo()`
  （bool get_have手枪弹药（））
- `void set_havePistolAmmo(bool value)`
  （void set_have手枪弹药（bool value））
- `bool get_haveHulk()`
  （bool get_haveHulk（））
- `void set_haveHulk(bool value)`
  （void set_haveHulk（bool value））
- `bool get_haveNurse()`
  （bool get_haveNurse（））
- `void set_haveNurse(bool value)`
  （void set_haveNurse（bool value））
- `bool get_havePsycho()`
  （bool get_havePsycho（））
- `void set_havePsycho(bool value)`
  （void set_havePsycho（bool value））
- `bool get_haveNanoRole()`
  （bool get_have纳米Role（））
- `void set_haveNanoRole(bool value)`
  （void set_have纳米Role（bool value））
- `bool get_haveNanoHook()`
  （bool get_have纳米Hook（））
- `void set_haveNanoHook(bool value)`
  （void set_have纳米Hook（bool value））
- `void AddOrRemoveItem(int itemID)`
  （void 添加Or移除项目（int itemID））
- `void Update()`
  （void 更新（））
- `void BotRandom()`
  （void 机器人随机（））
- `void CalculateClipBuff()`
  （void 计算弹匣增益（））

---

## ClientData.ClipBuffInfo（客户端Data.弹匣增益信息）

### 字段 (5)

- `int rifle`（int rifle）(偏移: 0x0)
- `int sniper`（int sniper）(偏移: 0x4)
- `int smg`（int smg）(偏移: 0x8)
- `int machineGun`（int machine枪械）(偏移: 0xC)
- `int pistol`（int pistol）(偏移: 0x10)

### 方法 (4)

- `void Clear()`
  （void 清除（））
- `void Print()`
  （void Print（））
- `int GetCount(WeaponClass wpnClass)`
  （int 获取数量（武器类别 wpnClass））
- `void AddMaxClip(WPN_Gun.AmmoData ammoData, WeaponClass wpnClass)`
  （void 添加最大弹匣（WPN_Gun.弹药数据 ammoData, 武器类别 wpnClass））

---

## ClientIdentity（客户端Identity）

**继承**: Identity（Identity）

### 字段 (1)

- `WeakReference _proxyReference`（Weak引用 _proxy引用）(偏移: 0x24)

### 方法 (4)

- `MarshalByRefObject get_ClientProxy()`
  （MarshalByRef对象 get_客户端代理（））
- `void set_ClientProxy(MarshalByRefObject value)`
  （void set_客户端代理（MarshalByRef对象 value））
- `ObjRef CreateObjRef(Type requestedType)`
  （ObjRef 创建ObjRef（类型 requestedType））
- `string get_TargetUri()`
  （string get_目标Uri（））

---

## ClipBuff（弹匣增益）

**继承**: ItemAttributeBase（项目Attribute基础）

### 字段 (2)

- `WeaponClass wpnClass`（武器类别 武器类）(偏移: 0xC)
- `int count`（int count）(偏移: 0x10)

### 方法 (1)

- `void Calculate(ClientData client, bool add)`
  （void 计算（客户端数据 client, bool add））

---

## ClipCaps（弹匣Caps）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ClipType（弹匣类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Clipper（Clipper）

**继承**: ClipperBase（Clipper基础）

### 字段 (12)

- `List<OutRec> m_PolyOuts`（List<OutRec> m_PolyOuts）(偏移: 0x18)
- `ClipType m_ClipType`（弹匣类型 m_弹匣类型）(偏移: 0x1C)
- `Scanbeam m_Scanbeam`（Scanbeam m_Scanbeam）(偏移: 0x20)
- `TEdge m_ActiveEdges`（TEdge m_激活的Edges）(偏移: 0x24)
- `TEdge m_SortedEdges`（TEdge m_SortedEdges）(偏移: 0x28)
- `IntersectNode m_IntersectNodes`（Intersect节点 m_IntersectNodes）(偏移: 0x2C)
- `bool m_ExecuteLocked`（bool m_执行锁定的）(偏移: 0x30)
- `PolyFillType m_ClipFillType`（PolyFill类型 m_弹匣Fill类型）(偏移: 0x34)
- `PolyFillType m_SubjFillType`（PolyFill类型 m_SubjFill类型）(偏移: 0x38)
- `List<Join> m_Joins`（List<Join> m_Joins）(偏移: 0x3C)
- `List<Join> m_GhostJoins`（List<Join> m_幽灵Joins）(偏移: 0x40)
- `bool m_UsingPolyTree`（bool m_UsingPolyTree）(偏移: 0x44)

### 方法 (86)

- `void Clear()`
  （void 清除（））
- `void Reset()`
  （void 重置（））
- `bool get_ReverseSolution()`
  （bool get_ReverseSolution（））
- `void set_ReverseSolution(bool value)`
  （void set_ReverseSolution（bool value））
- `bool get_StrictlySimple()`
  （bool get_StrictlySimple（））
- `void set_StrictlySimple(bool value)`
  （void set_StrictlySimple（bool value））
- `void InsertScanbeam(long Y)`
  （void InsertScanbeam（long Y））
- `bool Execute(ClipType clipType, List<List<IntPoint>> solution, PolyFillType subjFillType, PolyFillType clipFillType)`
  （bool 执行（弹匣类型 clipType, List<List<整数Point>> solution, PolyFill类型 subjFillType, PolyFill类型 clipFillType））
- `bool Execute(ClipType clipType, PolyTree polytree, PolyFillType subjFillType, PolyFillType clipFillType)`
  （bool 执行（弹匣类型 clipType, PolyTree polytree, PolyFill类型 subjFillType, PolyFill类型 clipFillType））
- `void FixHoleLinkage(OutRec outRec)`
  （void FixHoleLinkage（OutRec outRec））
- `bool ExecuteInternal()`
  （bool 执行内部的（））
- `long PopScanbeam()`
  （long PopScanbeam（））
- `void DisposeAllPolyPts()`
  （void 释放所有PolyPts（））
- `void DisposeOutRec(int index)`
  （void 释放OutRec（int index））
- `void DisposeOutPts(OutPt pp)`
  （void 释放OutPts（OutPt pp））
- `void AddJoin(OutPt Op1, OutPt Op2, IntPoint OffPt)`
  （void 添加Join（OutPt Op1, OutPt Op2, 整数Point OffPt））
- `void AddGhostJoin(OutPt Op, IntPoint OffPt)`
  （void 添加幽灵Join（OutPt Op, 整数Point OffPt））
- `void InsertLocalMinimaIntoAEL(long botY)`
  （void Insert本地的MinimaIntoAEL（long botY））
- `void InsertEdgeIntoAEL(TEdge edge, TEdge startEdge)`
  （void InsertEdgeIntoAEL（TEdge edge, TEdge startEdge））
- `bool E2InsertsBeforeE1(TEdge e1, TEdge e2)`
  （bool E2InsertsBeforeE1（TEdge e1, TEdge e2））
- `bool IsEvenOddFillType(TEdge edge)`
  （bool 是否EvenOddFill类型（TEdge edge））
- `bool IsEvenOddAltFillType(TEdge edge)`
  （bool 是否EvenOddAltFill类型（TEdge edge））
- `bool IsContributing(TEdge edge)`
  （bool 是否Contributing（TEdge edge））
- `void SetWindingCount(TEdge edge)`
  （void 集合Winding数量（TEdge edge））
- `void AddEdgeToSEL(TEdge edge)`
  （void 添加EdgeToSEL（TEdge edge））
- `void CopyAELToSEL()`
  （void 复制AELToSEL（））
- `void SwapPositionsInAEL(TEdge edge1, TEdge edge2)`
  （void SwapPositionsInAEL（TEdge edge1, TEdge edge2））
- `void SwapPositionsInSEL(TEdge edge1, TEdge edge2)`
  （void SwapPositionsInSEL（TEdge edge1, TEdge edge2））
- `void AddLocalMaxPoly(TEdge e1, TEdge e2, IntPoint pt)`
  （void 添加本地的最大Poly（TEdge e1, TEdge e2, 整数Point pt））
- `OutPt AddLocalMinPoly(TEdge e1, TEdge e2, IntPoint pt)`
  （OutPt 添加本地的最小Poly（TEdge e1, TEdge e2, 整数Point pt））
- `OutRec CreateOutRec()`
  （OutRec 创建OutRec（））
- `OutPt AddOutPt(TEdge e, IntPoint pt)`
  （OutPt 添加OutPt（TEdge e, 整数Point pt））
- `bool HorzSegmentsOverlap(IntPoint Pt1a, IntPoint Pt1b, IntPoint Pt2a, IntPoint Pt2b)`
  （bool HorzSegmentsOverlap（整数Point Pt1a, 整数Point Pt1b, 整数Point Pt2a, 整数Point Pt2b））
- `void SetHoleState(TEdge e, OutRec outRec)`
  （void 集合Hole状态（TEdge e, OutRec outRec））
- `double GetDx(IntPoint pt1, IntPoint pt2)`
  （double 获取Dx（整数Point pt1, 整数Point pt2））
- `bool FirstIsBottomPt(OutPt btmPt1, OutPt btmPt2)`
  （bool 第一个是否底部Pt（OutPt btmPt1, OutPt btmPt2））
- `OutPt GetBottomPt(OutPt pp)`
  （OutPt 获取底部Pt（OutPt pp））
- `OutRec GetLowermostRec(OutRec outRec1, OutRec outRec2)`
  （OutRec 获取LowermostRec（OutRec outRec1, OutRec outRec2））
- `bool Param1RightOfParam2(OutRec outRec1, OutRec outRec2)`
  （bool Param1右OfParam2（OutRec outRec1, OutRec outRec2））
- `OutRec GetOutRec(int idx)`
  （OutRec 获取OutRec（int idx））
- `void AppendPolygon(TEdge e1, TEdge e2)`
  （void AppendPolygon（TEdge e1, TEdge e2））
- `void ReversePolyPtLinks(OutPt pp)`
  （void ReversePolyPtLinks（OutPt pp））
- `void SwapSides(TEdge edge1, TEdge edge2)`
  （void SwapSides（TEdge edge1, TEdge edge2））
- `void SwapPolyIndexes(TEdge edge1, TEdge edge2)`
  （void SwapPolyIndexes（TEdge edge1, TEdge edge2））
- `void IntersectEdges(TEdge e1, TEdge e2, IntPoint pt, bool protect = False)`
  （void IntersectEdges（TEdge e1, TEdge e2, 整数Point pt, bool protect = False））
- `void DeleteFromAEL(TEdge e)`
  （void DeleteFromAEL（TEdge e））
- `void DeleteFromSEL(TEdge e)`
  （void DeleteFromSEL（TEdge e））
- `void UpdateEdgeIntoAEL(ref TEdge e)`
  （void 更新EdgeIntoAEL（ref TEdge e））
- `void ProcessHorizontals(bool isTopOfScanbeam)`
  （void 处理Horizontals（bool isTopOfScanbeam））
- `void GetHorzDirection(TEdge HorzEdge, out Direction Dir, out long Left, out long Right)`
  （void 获取Horz方向（TEdge HorzEdge, out Direction Dir, out long Left, out long Right））
- `void PrepareHorzJoins(TEdge horzEdge, bool isTopOfScanbeam)`
  （void PrepareHorzJoins（TEdge horzEdge, bool isTopOfScanbeam））
- `void ProcessHorizontal(TEdge horzEdge, bool isTopOfScanbeam)`
  （void 处理水平（TEdge horzEdge, bool isTopOfScanbeam））
- `TEdge GetNextInAEL(TEdge e, Direction Direction)`
  （TEdge 获取下一个InAEL（TEdge e, 方向 Direction））
- `bool IsMaxima(TEdge e, double Y)`
  （bool 是否Maxima（TEdge e, double Y））
- `bool IsIntermediate(TEdge e, double Y)`
  （bool 是否Intermediate（TEdge e, double Y））
- `TEdge GetMaximaPair(TEdge e)`
  （TEdge 获取MaximaPair（TEdge e））
- `bool ProcessIntersections(long botY, long topY)`
  （bool 处理Intersections（long botY, long topY））
- `void BuildIntersectList(long botY, long topY)`
  （void BuildIntersect列表（long botY, long topY））
- `bool EdgesAdjacent(IntersectNode inode)`
  （bool EdgesAdjacent（Intersect节点 inode））
- `bool FixupIntersectionOrder()`
  （bool FixupIntersectionOrder（））
- `void ProcessIntersectList()`
  （void 处理Intersect列表（））
- `long Round(double value)`
  （long 回合（double value））
- `long TopX(TEdge edge, long currentY)`
  （long 顶部X（TEdge edge, long currentY））
- `void InsertIntersectNode(TEdge e1, TEdge e2, IntPoint pt)`
  （void InsertIntersect节点（TEdge e1, TEdge e2, 整数Point pt））
- `void SwapIntersectNodes(IntersectNode int1, IntersectNode int2)`
  （void SwapIntersectNodes（Intersect节点 int1, Intersect节点 int2））
- `bool IntersectPoint(TEdge edge1, TEdge edge2, out IntPoint ip)`
  （bool IntersectPoint（TEdge edge1, TEdge edge2, out IntPoint ip））
- `void DisposeIntersectNodes()`
  （void 释放IntersectNodes（））
- `void ProcessEdgesAtTopOfScanbeam(long topY)`
  （void 处理EdgesAt顶部OfScanbeam（long topY））
- `void DoMaxima(TEdge e)`
  （void DoMaxima（TEdge e））
- `bool Orientation(List<IntPoint> poly)`
  （bool Orientation（List<整数Point> poly））
- `int PointCount(OutPt pts)`
  （int Point数量（OutPt pts））
- `void BuildResult(List<List<IntPoint>> polyg)`
  （void BuildResult（List<List<整数Point>> polyg））
- `void BuildResult2(PolyTree polytree)`
  （void BuildResult2（PolyTree polytree））
- `void FixupOutPolygon(OutRec outRec)`
  （void FixupOutPolygon（OutRec outRec））
- `OutPt DupOutPt(OutPt outPt, bool InsertAfter)`
  （OutPt DupOutPt（OutPt outPt, bool InsertAfter））
- `bool GetOverlap(long a1, long a2, long b1, long b2, out long Left, out long Right)`
  （bool 获取Overlap（long a1, long a2, long b1, long b2, out long Left, out long Right））
- `bool JoinHorz(OutPt op1, OutPt op1b, OutPt op2, OutPt op2b, IntPoint Pt, bool DiscardLeft)`
  （bool JoinHorz（OutPt op1, OutPt op1b, OutPt op2, OutPt op2b, 整数Point Pt, bool DiscardLeft））
- `bool JoinPoints(Join j, out OutPt p1, out OutPt p2)`
  （bool JoinPoints（Join j, out OutPt p1, out OutPt p2））
- `bool Poly2ContainsPoly1(OutPt outPt1, OutPt outPt2, bool UseFullRange)`
  （bool Poly2ContainsPoly1（OutPt outPt1, OutPt outPt2, bool UseFullRange））
- `void FixupFirstLefts1(OutRec OldOutRec, OutRec NewOutRec)`
  （void Fixup第一个Lefts1（OutRec OldOutRec, OutRec NewOutRec））
- `void FixupFirstLefts2(OutRec OldOutRec, OutRec NewOutRec)`
  （void Fixup第一个Lefts2（OutRec OldOutRec, OutRec NewOutRec））
- `void JoinCommonEdges()`
  （void JoinCommonEdges（））
- `void UpdateOutPtIdxs(OutRec outrec)`
  （void 更新OutPtIdxs（OutRec outrec））
- `void DoSimplePolygons()`
  （void DoSimplePolygons（））
- `double Area(List<IntPoint> poly)`
  （double Area（List<整数Point> poly））
- `double Area(OutRec outRec)`
  （double Area（OutRec outRec））

---

## ClipperBase（Clipper基础）

### 字段 (5)

- `LocalMinima m_MinimaList`（本地的Minima m_Minima列表）(偏移: 0x8)
- `LocalMinima m_CurrentLM`（本地的Minima m_当前LM）(偏移: 0xC)
- `List<List<TEdge>> m_edges`（List<List<TEdge>> m_edges）(偏移: 0x10)
- `bool m_UseFullRange`（bool m_Use满范围）(偏移: 0x14)
- `bool m_HasOpenPaths`（bool m_是否有打开Paths）(偏移: 0x15)

### 方法 (33)

- `bool get_PreserveCollinear()`
  （bool get_PreserveCollinear（））
- `void set_PreserveCollinear(bool value)`
  （void set_PreserveCollinear（bool value））
- `bool IsHorizontal(TEdge e)`
  （bool 是否水平（TEdge e））
- `bool PointOnLineSegment(IntPoint pt, IntPoint linePt1, IntPoint linePt2, bool UseFullRange)`
  （bool PointOnLineSegment（整数Point pt, 整数Point linePt1, 整数Point linePt2, bool UseFullRange））
- `bool PointOnPolygon(IntPoint pt, OutPt pp, bool UseFullRange)`
  （bool PointOnPolygon（整数Point pt, OutPt pp, bool UseFullRange））
- `bool PointInPolygon(IntPoint pt, OutPt pp, bool UseFullRange)`
  （bool PointInPolygon（整数Point pt, OutPt pp, bool UseFullRange））
- `bool SlopesEqual(TEdge e1, TEdge e2, bool UseFullRange)`
  （bool SlopesEqual（TEdge e1, TEdge e2, bool UseFullRange））
- `bool SlopesEqual(IntPoint pt1, IntPoint pt2, IntPoint pt3, bool UseFullRange)`
  （bool SlopesEqual（整数Point pt1, 整数Point pt2, 整数Point pt3, bool UseFullRange））
- `void Clear()`
  （void 清除（））
- `void DisposeLocalMinimaList()`
  （void 释放本地的Minima列表（））
- `void RangeTest(IntPoint Pt, ref bool useFullRange)`
  （void 范围Test（整数Point Pt, ref bool useFullRange））
- `void InitEdge(TEdge e, TEdge eNext, TEdge ePrev, IntPoint pt)`
  （void 初始化Edge（TEdge e, TEdge eNext, TEdge ePrev, 整数Point pt））
- `void InitEdge2(TEdge e, PolyType polyType)`
  （void 初始化Edge2（TEdge e, Poly类型 polyType））
- `bool AddPath(List<IntPoint> pg, PolyType polyType, bool Closed)`
  （bool 添加路径（List<整数Point> pg, Poly类型 polyType, bool Closed））
- `bool AddPolygon(List<IntPoint> pg, PolyType polyType)`
  （bool 添加Polygon（List<整数Point> pg, Poly类型 polyType））
- `bool Pt2IsBetweenPt1AndPt3(IntPoint pt1, IntPoint pt2, IntPoint pt3)`
  （bool Pt2是否BetweenPt1AndPt3（整数Point pt1, 整数Point pt2, 整数Point pt3））
- `TEdge RemoveEdge(TEdge e)`
  （TEdge 移除Edge（TEdge e））
- `TEdge GetLastHorz(TEdge Edge)`
  （TEdge 获取最后一个Horz（TEdge Edge））
- `bool SharedVertWithPrevAtTop(TEdge Edge)`
  （bool SharedVertWithPrevAt顶部（TEdge Edge））
- `bool SharedVertWithNextIsBot(TEdge Edge)`
  （bool SharedVertWith下一个是否机器人（TEdge Edge））
- `bool MoreBelow(TEdge Edge)`
  （bool MoreBelow（TEdge Edge））
- `bool JustBeforeLocMin(TEdge Edge)`
  （bool JustBeforeLoc最小（TEdge Edge））
- `bool MoreAbove(TEdge Edge)`
  （bool MoreAbove（TEdge Edge））
- `bool AllHorizontal(TEdge Edge)`
  （bool 所有水平（TEdge Edge））
- `void SetDx(TEdge e)`
  （void 集合Dx（TEdge e））
- `void DoMinimaLML(TEdge E1, TEdge E2, bool IsClosed)`
  （void DoMinimaLML（TEdge E1, TEdge E2, bool IsClosed））
- `TEdge DescendToMin(ref TEdge E)`
  （TEdge DescendTo最小（ref TEdge E））
- `void AscendToMax(ref TEdge E, bool Appending, bool IsClosed)`
  （void AscendTo最大（ref TEdge E, bool Appending, bool IsClosed））
- `TEdge AddBoundsToLML(TEdge E, bool Closed)`
  （TEdge 添加BoundsToLML（TEdge E, bool Closed））
- `void InsertLocalMinima(LocalMinima newLm)`
  （void Insert本地的Minima（本地的Minima newLm））
- `void PopLocalMinima()`
  （void Pop本地的Minima（））
- `void ReverseHorizontal(TEdge e)`
  （void Reverse水平（TEdge e））
- `void Reset()`
  （void 重置（））

---

## ClipperRegistry（ClipperRegistry）

### 字段 (2)

- `ClipperRegistry s_Instance`（ClipperRegistry s_实例）(偏移: 0x0)
- `IndexedSet<IClipper> m_Clippers`（IndexedSet<IClipper> m_Clippers）(偏移: 0x8)

### 方法 (4)

- `ClipperRegistry get_instance()`
  （ClipperRegistry get_instance（））
- `void Cull()`
  （void Cull（））
- `void Register(IClipper c)`
  （void Register（IClipper c））
- `void Unregister(IClipper c)`
  （void Unregister（IClipper c））

---

## Clipping（Clipping）

### 方法 (1)

- `Rect FindCullAndClipWorldRect(List<RectMask2D> rectMaskParents, out bool validRect)`
  （Rect 查找CullAnd弹匣世界的Rect（List<RectMask2D> rectMaskParents, out bool validRect））

---

## CloseDelegate（关闭委托）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(string entryName, Stream stream)`
  （void Invoke（string entryName, 流 stream））
- `IAsyncResult BeginInvoke(string entryName, Stream stream, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（string entryName, 流 stream, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## CloseToDestinationMode（关闭ToDestination模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## CodePageDataItem（CodePage数据项目）

### 字段 (5)

- `int m_dataIndex`（int m_data索引）(偏移: 0x8)
- `int m_uiFamilyCodePage`（int m_uiFamilyCodePage）(偏移: 0xC)
- `string m_webName`（string m_web名称）(偏移: 0x10)
- `uint m_flags`（uint m_flags）(偏移: 0x14)
- `char[] sep`（char[] sep）(偏移: 0x0)

### 方法 (2)

- `string CreateString(string pStrings, uint index)`
  （string 创建字符串（string pStrings, uint index））
- `string get_WebName()`
  （string get_Web名称（））

---

## CodePointIndexer（CodePointIndexer）

### 字段 (4)

- `CodePointIndexer.TableRange[] ranges`（CodePointIndexer.TableRange[] ranges）(偏移: 0x8)
- `int TotalCount`（int Total数量）(偏移: 0xC)
- `int defaultIndex`（int default索引）(偏移: 0x10)
- `int defaultCP`（int defaultCP）(偏移: 0x14)

### 方法 (1)

- `int ToIndex(int cp)`
  （int To索引（int cp））

---

## CodePointIndexer.TableRange（CodePointIndexer.Table范围）

### 字段 (5)

- `int Start`（int 开始）(偏移: 0x0)
- `int End`（int 结束）(偏移: 0x4)
- `int Count`（int 数量）(偏移: 0x8)
- `int IndexStart`（int 索引开始）(偏移: 0xC)
- `int IndexEnd`（int 索引结束）(偏移: 0x10)

---

## CodegenOptions（CodegenOptions）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## CollectionConverter（CollectionConverter）

**继承**: TypeConverter（类型Converter）

### 方法 (3)

- `object ConvertTo(ITypeDescriptorContext context, CultureInfo culture, object value, Type destinationType)`
  （object 转换To（I类型DescriptorContext context, Culture信息 culture, object value, 类型 destinationType））
- `PropertyDescriptorCollection GetProperties(ITypeDescriptorContext context, object value, Attribute[] attributes)`
  （属性DescriptorCollection 获取Properties（I类型DescriptorContext context, object value, Attribute[] attributes））
- `bool GetPropertiesSupported(ITypeDescriptorContext context)`
  （bool 获取PropertiesSupported（I类型DescriptorContext context））

---

## Collider（碰撞器）

**继承**: Component（组件）

### 方法 (12)

- `bool get_enabled()`
  （bool get_enabled（））
- `void set_enabled(bool value)`
  （void set_enabled（bool value））
- `Rigidbody get_attachedRigidbody()`
  （刚体 get_attached刚体（））
- `bool get_isTrigger()`
  （bool get_is触发器（））
- `void set_isTrigger(bool value)`
  （void set_is触发器（bool value））
- `Vector3 ClosestPoint(Vector3 position)`
  （三维向量 ClosestPoint（三维向量 position））
- `Bounds get_bounds()`
  （Bounds get_bounds（））
- `RaycastHit Raycast(Ray ray, float maxDistance, ref bool hasHit)`
  （Raycast命中 Raycast（Ray ray, float maxDistance, ref bool hasHit））
- `bool Raycast(Ray ray, out RaycastHit hitInfo, float maxDistance)`
  （bool Raycast（Ray ray, out RaycastHit hitInfo, float maxDistance））
- `void ClosestPoint_Injected(ref Vector3 position, out Vector3 ret)`
  （void ClosestPoint_Injected（ref Vector3 position, out Vector3 ret））
- `void get_bounds_Injected(out Bounds ret)`
  （void get_bounds_Injected（out Bounds ret））
- `void Raycast_Injected(ref Ray ray, float maxDistance, ref bool hasHit, out RaycastHit ret)`
  （void Raycast_Injected（ref Ray ray, float maxDistance, ref bool hasHit, out RaycastHit ret））

---

## Collider2D（Collider2D）

**继承**: Behaviour（Behaviour）

### 方法 (7)

- `Vector2 get_offset()`
  （二维向量 get_offset（））
- `Rigidbody2D get_attachedRigidbody()`
  （Rigidbody2D get_attached刚体（））
- `Bounds get_bounds()`
  （Bounds get_bounds（））
- `bool OverlapPoint(Vector2 point)`
  （bool OverlapPoint（二维向量 point））
- `void get_offset_Injected(out Vector2 ret)`
  （void get_offset_Injected（out Vector2 ret））
- `void get_bounds_Injected(out Bounds ret)`
  （void get_bounds_Injected（out Bounds ret））
- `bool OverlapPoint_Injected(ref Vector2 point)`
  （bool OverlapPoint_Injected（ref Vector2 point））

---

## ColliderType（碰撞器类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Collision（Collision）

### 字段 (7)

- `Vector3 m_Impulse`（三维向量 m_Impulse）(偏移: 0x8)
- `Vector3 m_RelativeVelocity`（三维向量 m_Relative速度）(偏移: 0x14)
- `Component m_Body`（组件 m_身体）(偏移: 0x20)
- `Collider m_Collider`（碰撞器 m_碰撞器）(偏移: 0x24)
- `int m_ContactCount`（int m_Contact数量）(偏移: 0x28)
- `ContactPoint[] m_ReusedContacts`（ContactPoint[] m_ReusedContacts）(偏移: 0x2C)
- `ContactPoint[] m_LegacyContacts`（ContactPoint[] m_LegacyContacts）(偏移: 0x30)

### 方法 (4)

- `Vector3 get_relativeVelocity()`
  （三维向量 get_relative速度（））
- `Collider get_collider()`
  （碰撞器 get_collider（））
- `GameObject get_gameObject()`
  （游戏对象 get_game对象（））
- `ContactPoint[] get_contacts()`
  （ContactPoint[] get_contacts（））

---

## Collision2D（Collision2D）

### 字段 (9)

- `int m_Collider`（int m_碰撞器）(偏移: 0x8)
- `int m_OtherCollider`（int m_Other碰撞器）(偏移: 0xC)
- `int m_Rigidbody`（int m_刚体）(偏移: 0x10)
- `int m_OtherRigidbody`（int m_Other刚体）(偏移: 0x14)
- `Vector2 m_RelativeVelocity`（二维向量 m_Relative速度）(偏移: 0x18)
- `int m_Enabled`（int m_启用的）(偏移: 0x20)
- `int m_ContactCount`（int m_Contact数量）(偏移: 0x24)
- `ContactPoint2D[] m_ReusedContacts`（ContactPoint2D[] m_ReusedContacts）(偏移: 0x28)
- `ContactPoint2D[] m_LegacyContacts`（ContactPoint2D[] m_LegacyContacts）(偏移: 0x2C)

### 方法 (4)

- `Collider2D get_collider()`
  （Collider2D get_collider（））
- `Rigidbody2D get_rigidbody()`
  （Rigidbody2D get_rigidbody（））
- `GameObject get_gameObject()`
  （游戏对象 get_game对象（））
- `Vector2 get_relativeVelocity()`
  （二维向量 get_relative速度（））

---

## CollisionFlags（CollisionFlags）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Color（颜色）

**继承**: IEquatable<Color>, IFormattable（IEquatable<Color>, IFormattable）

### 字段 (4)

- `float r`（float r）(偏移: 0x0)
- `float g`（float g）(偏移: 0x4)
- `float b`（float b）(偏移: 0x8)
- `float a`（float a）(偏移: 0xC)

### 方法 (30)

- `string ToString()`
  （string To字符串（））
- `string ToString(string format, IFormatProvider formatProvider)`
  （string To字符串（string format, I格式化提供者 formatProvider））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool Equals(object other)`
  （bool Equals（object other））
- `bool Equals(Color other)`
  （bool Equals（颜色 other））
- `Color op_Addition(Color a, Color b)`
  （颜色 op_Addition（颜色 a, 颜色 b））
- `Color op_Subtraction(Color a, Color b)`
  （颜色 op_Subtraction（颜色 a, 颜色 b））
- `Color op_Multiply(Color a, Color b)`
  （颜色 op_Multiply（颜色 a, 颜色 b））
- `Color op_Multiply(Color a, float b)`
  （颜色 op_Multiply（颜色 a, float b））
- `Color op_Multiply(float b, Color a)`
  （颜色 op_Multiply（float b, 颜色 a））
- `bool op_Equality(Color lhs, Color rhs)`
  （bool op_Equality（颜色 lhs, 颜色 rhs））
- `bool op_Inequality(Color lhs, Color rhs)`
  （bool op_Inequality（颜色 lhs, 颜色 rhs））
- `Color Lerp(Color a, Color b, float t)`
  （颜色 Lerp（颜色 a, 颜色 b, float t））
- `Color RGBMultiplied(float multiplier)`
  （颜色 RGB颜色Multiplied（float multiplier））
- `Color get_red()`
  （颜色 get_red（））
- `Color get_green()`
  （颜色 get_green（））
- `Color get_blue()`
  （颜色 get_blue（））
- `Color get_white()`
  （颜色 get_white（））
- `Color get_black()`
  （颜色 get_black（））
- `Color get_yellow()`
  （颜色 get_yellow（））
- `Color get_cyan()`
  （颜色 get_cyan（））
- `Color get_magenta()`
  （颜色 get_magenta（））
- `Color get_gray()`
  （颜色 get_gray（））
- `Color get_grey()`
  （颜色 get_grey（））
- `Color get_clear()`
  （颜色 get_clear（））
- `Color get_linear()`
  （颜色 get_linear（））
- `Color get_gamma()`
  （颜色 get_gamma（））
- `float get_maxColorComponent()`
  （float get_max颜色组件（））
- `Vector4 op_Implicit(Color c)`
  （Vector4 op_Implicit（颜色 c））
- `Color op_Implicit(Vector4 v)`
  （颜色 op_Implicit（Vector4 v））

---

## Color2（Color2）

### 字段 (2)

- `Color ca`（颜色 ca）(偏移: 0x0)
- `Color cb`（颜色 cb）(偏移: 0x10)

### 方法 (3)

- `Color2 op_Addition(Color2 c1, Color2 c2)`
  （Color2 op_Addition（Color2 c1, Color2 c2））
- `Color2 op_Subtraction(Color2 c1, Color2 c2)`
  （Color2 op_Subtraction（Color2 c1, Color2 c2））
- `Color2 op_Multiply(Color2 c1, float f)`
  （Color2 op_Multiply（Color2 c1, float f））

---

## Color2Plugin（Color2插件）

**继承**: ABSTweenPlugin<Color2, Color2, ColorOptions>（ABSTweenPlugin<Color2, Color2, 颜色Options>）

### 方法 (8)

- `void Reset(TweenerCore<Color2, Color2, ColorOptions> t)`
  （void 重置（TweenerCore<Color2, Color2, 颜色Options> t））
- `void SetFrom(TweenerCore<Color2, Color2, ColorOptions> t, bool isRelative)`
  （void 集合From（TweenerCore<Color2, Color2, 颜色Options> t, bool isRelative））
- `void SetFrom(TweenerCore<Color2, Color2, ColorOptions> t, Color2 fromValue, bool setImmediately, bool isRelative)`
  （void 集合From（TweenerCore<Color2, Color2, 颜色Options> t, Color2 fromValue, bool setImmediately, bool isRelative））
- `Color2 ConvertToStartValue(TweenerCore<Color2, Color2, ColorOptions> t, Color2 value)`
  （Color2 转换To开始值（TweenerCore<Color2, Color2, 颜色Options> t, Color2 value））
- `void SetRelativeEndValue(TweenerCore<Color2, Color2, ColorOptions> t)`
  （void 集合Relative结束值（TweenerCore<Color2, Color2, 颜色Options> t））
- `void SetChangeValue(TweenerCore<Color2, Color2, ColorOptions> t)`
  （void 集合Change值（TweenerCore<Color2, Color2, 颜色Options> t））
- `float GetSpeedBasedDuration(ColorOptions options, float unitsXSecond, Color2 changeValue)`
  （float 获取SpeedBased持续时间（颜色Options options, float unitsXSecond, Color2 changeValue））
- `void EvaluateAndApply(ColorOptions options, Tween t, bool isRelative, DOGetter<Color2> getter, DOSetter<Color2> setter, float elapsed, Color2 startValue, Color2 changeValue, float duration, bool usingInversePosition, UpdateNotice updateNotice)`
  （void EvaluateAnd应用（颜色Options options, Tween t, bool isRelative, DOGetter<Color2> getter, DOSetter<Color2> setter, float elapsed, Color2 startValue, Color2 changeValue, float duration, bool usingInversePosition, 更新Notice updateNotice））

---

## Color32（Color32）

**继承**: IFormattable（IFormattable）

### 字段 (5)

- `int rgba`（int rgba）(偏移: 0x0)
- `byte r`（byte r）(偏移: 0x0)
- `byte g`（byte g）(偏移: 0x1)
- `byte b`（byte b）(偏移: 0x2)
- `byte a`（byte a）(偏移: 0x3)

### 方法 (4)

- `Color32 op_Implicit(Color c)`
  （Color32 op_Implicit（颜色 c））
- `Color op_Implicit(Color32 c)`
  （颜色 op_Implicit（Color32 c））
- `string ToString()`
  （string To字符串（））
- `string ToString(string format, IFormatProvider formatProvider)`
  （string To字符串（string format, I格式化提供者 formatProvider））

---

## ColorAdjustments（颜色Adjustments）

**继承**: VolumeComponent, IPostProcessComponent（Volume组件, IPost处理组件）

### 字段 (5)

- `FloatParameter postExposure`（浮点数Parameter postExposure）(偏移: 0x1C)
- `ClampedFloatParameter contrast`（Clamped浮点数Parameter contrast）(偏移: 0x20)
- `ColorParameter colorFilter`（颜色Parameter colorFilter）(偏移: 0x24)
- `ClampedFloatParameter hueShift`（Clamped浮点数Parameter hueShift）(偏移: 0x28)
- `ClampedFloatParameter saturation`（Clamped浮点数Parameter saturation）(偏移: 0x2C)

### 方法 (2)

- `bool IsActive()`
  （bool 是否激活的（））
- `bool IsTileCompatible()`
  （bool 是否TileCompatible（））

---

## ColorBlock（颜色Block）

**继承**: IEquatable<ColorBlock>（IEquatable<颜色Block>）

### 字段 (8)

- `Color m_NormalColor`（颜色 m_法线颜色）(偏移: 0x0)
- `Color m_HighlightedColor`（颜色 m_Highlighted颜色）(偏移: 0x10)
- `Color m_PressedColor`（颜色 m_按下的颜色）(偏移: 0x20)
- `Color m_SelectedColor`（颜色 m_选中的颜色）(偏移: 0x30)
- `Color m_DisabledColor`（颜色 m_禁用的颜色）(偏移: 0x40)
- `float m_ColorMultiplier`（float m_颜色Multiplier）(偏移: 0x50)
- `float m_FadeDuration`（float m_Fade持续时间）(偏移: 0x54)
- `ColorBlock defaultColorBlock`（颜色Block default颜色Block）(偏移: 0x0)

### 方法 (19)

- `Color get_normalColor()`
  （颜色 get_normal颜色（））
- `void set_normalColor(Color value)`
  （void set_normal颜色（颜色 value））
- `Color get_highlightedColor()`
  （颜色 get_highlighted颜色（））
- `void set_highlightedColor(Color value)`
  （void set_highlighted颜色（颜色 value））
- `Color get_pressedColor()`
  （颜色 get_pressed颜色（））
- `void set_pressedColor(Color value)`
  （void set_pressed颜色（颜色 value））
- `Color get_selectedColor()`
  （颜色 get_selected颜色（））
- `void set_selectedColor(Color value)`
  （void set_selected颜色（颜色 value））
- `Color get_disabledColor()`
  （颜色 get_disabled颜色（））
- `void set_disabledColor(Color value)`
  （void set_disabled颜色（颜色 value））
- `float get_colorMultiplier()`
  （float get_colorMultiplier（））
- `void set_colorMultiplier(float value)`
  （void set_colorMultiplier（float value））
- `float get_fadeDuration()`
  （float get_fade持续时间（））
- `void set_fadeDuration(float value)`
  （void set_fade持续时间（float value））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `bool Equals(ColorBlock other)`
  （bool Equals（颜色Block other））
- `bool op_Equality(ColorBlock point1, ColorBlock point2)`
  （bool op_Equality（颜色Block point1, 颜色Block point2））
- `bool op_Inequality(ColorBlock point1, ColorBlock point2)`
  （bool op_Inequality（颜色Block point1, 颜色Block point2））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## ColorCurves（颜色Curves）

**继承**: VolumeComponent, IPostProcessComponent（Volume组件, IPost处理组件）

### 字段 (8)

- `TextureCurveParameter master`（纹理CurveParameter master）(偏移: 0x1C)
- `TextureCurveParameter red`（纹理CurveParameter red）(偏移: 0x20)
- `TextureCurveParameter green`（纹理CurveParameter green）(偏移: 0x24)
- `TextureCurveParameter blue`（纹理CurveParameter blue）(偏移: 0x28)
- `TextureCurveParameter hueVsHue`（纹理CurveParameter hueVsHue）(偏移: 0x2C)
- `TextureCurveParameter hueVsSat`（纹理CurveParameter hueVsSat）(偏移: 0x30)
- `TextureCurveParameter satVsSat`（纹理CurveParameter satVsSat）(偏移: 0x34)
- `TextureCurveParameter lumVsSat`（纹理CurveParameter lumVsSat）(偏移: 0x38)

### 方法 (2)

- `bool IsActive()`
  （bool 是否激活的（））
- `bool IsTileCompatible()`
  （bool 是否TileCompatible（））

---

## ColorGradingLutPass（颜色GradingLutPass）

**继承**: ScriptableRenderPass（ScriptableRenderPass）

### 字段 (5)

- `Material m_LutBuilderLdr`（材质 m_Lut构建器Ldr）(偏移: 0x54)
- `Material m_LutBuilderHdr`（材质 m_Lut构建器Hdr）(偏移: 0x58)
- `GraphicsFormat m_HdrLutFormat`（Graphics格式化 m_HdrLut格式化）(偏移: 0x5C)
- `GraphicsFormat m_LdrLutFormat`（Graphics格式化 m_LdrLut格式化）(偏移: 0x60)
- `RenderTargetHandle m_InternalLut`（Render目标句柄 m_内部的Lut）(偏移: 0x64)

### 方法 (4)

- `void Setup(in RenderTargetHandle internalLut)`
  （void Setup（in RenderTargetHandle internalLut））
- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（ScriptableRenderContext context, ref RenderingData renderingData））
- `void OnFinishCameraStackRendering(CommandBuffer cmd)`
  （void OnFinish摄像机栈Rendering（Command缓冲区 cmd））
- `void Cleanup()`
  （void 清理（））

---

## ColorGradingLutPass.ShaderConstants（颜色GradingLutPass.着色器Constants）

### 字段 (24)

- `int _Lut_Params`（int _Lut_Params）(偏移: 0x0)
- `int _ColorBalance`（int _颜色Balance）(偏移: 0x4)
- `int _ColorFilter`（int _颜色Filter）(偏移: 0x8)
- `int _ChannelMixerRed`（int _ChannelMixer红色）(偏移: 0xC)
- `int _ChannelMixerGreen`（int _ChannelMixer绿色）(偏移: 0x10)
- `int _ChannelMixerBlue`（int _ChannelMixer蓝色）(偏移: 0x14)
- `int _HueSatCon`（int _HueSatCon）(偏移: 0x18)
- `int _Lift`（int _Lift）(偏移: 0x1C)
- `int _Gamma`（int _Gamma）(偏移: 0x20)
- `int _Gain`（int _Gain）(偏移: 0x24)
- `int _Shadows`（int _Shadows）(偏移: 0x28)
- `int _Midtones`（int _Midtones）(偏移: 0x2C)
- `int _Highlights`（int _Highlights）(偏移: 0x30)
- `int _ShaHiLimits`（int _ShaHiLimits）(偏移: 0x34)
- `int _SplitShadows`（int _SplitShadows）(偏移: 0x38)
- `int _SplitHighlights`（int _SplitHighlights）(偏移: 0x3C)
- `int _CurveMaster`（int _CurveMaster）(偏移: 0x40)
- `int _CurveRed`（int _Curve红色）(偏移: 0x44)
- `int _CurveGreen`（int _Curve绿色）(偏移: 0x48)
- `int _CurveBlue`（int _Curve蓝色）(偏移: 0x4C)
- `int _CurveHueVsHue`（int _CurveHueVsHue）(偏移: 0x50)
- `int _CurveHueVsSat`（int _CurveHueVsSat）(偏移: 0x54)
- `int _CurveLumVsSat`（int _CurveLumVsSat）(偏移: 0x58)
- `int _CurveSatVsSat`（int _CurveSatVsSat）(偏移: 0x5C)

---

## ColorGradingMode（颜色Grading模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ColorLookup（颜色Lookup）

**继承**: VolumeComponent, IPostProcessComponent（Volume组件, IPost处理组件）

### 字段 (2)

- `TextureParameter texture`（纹理Parameter texture）(偏移: 0x1C)
- `ClampedFloatParameter contribution`（Clamped浮点数Parameter contribution）(偏移: 0x20)

### 方法 (3)

- `bool IsActive()`
  （bool 是否激活的（））
- `bool IsTileCompatible()`
  （bool 是否TileCompatible（））
- `bool ValidateLUT()`
  （bool 验证LUT（））

---

## ColorOptions（颜色Options）

**继承**: IPlugOptions（IPlugOptions）

### 字段 (1)

- `bool alphaOnly`（bool alphaOnly）(偏移: 0x0)

### 方法 (1)

- `void Reset()`
  （void 重置（））

---

## ColorParameter（颜色Parameter）

**继承**: VolumeParameter<Color>（VolumeParameter<Color>）

### 字段 (3)

- `bool hdr`（bool hdr）(偏移: 0x1C)
- `bool showAlpha`（bool show透明度）(偏移: 0x1D)
- `bool showEyeDropper`（bool showEyeDropper）(偏移: 0x1E)

### 方法 (1)

- `void Interp(Color from, Color to, float t)`
  （void Interp（颜色 from, 颜色 to, float t））

---

## ColorPlugin（颜色插件）

**继承**: ABSTweenPlugin<Color, Color, ColorOptions>（ABSTweenPlugin<颜色, 颜色, 颜色Options>）

### 方法 (8)

- `void Reset(TweenerCore<Color, Color, ColorOptions> t)`
  （void 重置（TweenerCore<颜色, 颜色, 颜色Options> t））
- `void SetFrom(TweenerCore<Color, Color, ColorOptions> t, bool isRelative)`
  （void 集合From（TweenerCore<颜色, 颜色, 颜色Options> t, bool isRelative））
- `void SetFrom(TweenerCore<Color, Color, ColorOptions> t, Color fromValue, bool setImmediately, bool isRelative)`
  （void 集合From（TweenerCore<颜色, 颜色, 颜色Options> t, 颜色 fromValue, bool setImmediately, bool isRelative））
- `Color ConvertToStartValue(TweenerCore<Color, Color, ColorOptions> t, Color value)`
  （颜色 转换To开始值（TweenerCore<颜色, 颜色, 颜色Options> t, 颜色 value））
- `void SetRelativeEndValue(TweenerCore<Color, Color, ColorOptions> t)`
  （void 集合Relative结束值（TweenerCore<颜色, 颜色, 颜色Options> t））
- `void SetChangeValue(TweenerCore<Color, Color, ColorOptions> t)`
  （void 集合Change值（TweenerCore<颜色, 颜色, 颜色Options> t））
- `float GetSpeedBasedDuration(ColorOptions options, float unitsXSecond, Color changeValue)`
  （float 获取SpeedBased持续时间（颜色Options options, float unitsXSecond, 颜色 changeValue））
- `void EvaluateAndApply(ColorOptions options, Tween t, bool isRelative, DOGetter<Color> getter, DOSetter<Color> setter, float elapsed, Color startValue, Color changeValue, float duration, bool usingInversePosition, UpdateNotice updateNotice)`
  （void EvaluateAnd应用（颜色Options options, Tween t, bool isRelative, DOGetter<Color> getter, DOSetter<Color> setter, float elapsed, 颜色 startValue, 颜色 changeValue, float duration, bool usingInversePosition, 更新Notice updateNotice））

---

## ColorSpace（颜色Space）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ColorTween（颜色Tween）

**继承**: ITweenValue（ITween值）

### 字段 (6)

- `ColorTween.ColorTweenCallback m_Target`（颜色Tween.颜色Tween回调 m_目标）(偏移: 0x0)
- `Color m_StartColor`（颜色 m_开始颜色）(偏移: 0x4)
- `Color m_TargetColor`（颜色 m_目标颜色）(偏移: 0x14)
- `ColorTween.ColorTweenMode m_TweenMode`（颜色Tween.颜色Tween模式 m_Tween模式）(偏移: 0x24)
- `float m_Duration`（float m_持续时间）(偏移: 0x28)
- `bool m_IgnoreTimeScale`（bool m_Ignore时间缩放）(偏移: 0x2C)

### 方法 (15)

- `Color get_startColor()`
  （颜色 get_start颜色（））
- `void set_startColor(Color value)`
  （void set_start颜色（颜色 value））
- `Color get_targetColor()`
  （颜色 get_target颜色（））
- `void set_targetColor(Color value)`
  （void set_target颜色（颜色 value））
- `ColorTween.ColorTweenMode get_tweenMode()`
  （颜色Tween.颜色Tween模式 get_tween模式（））
- `void set_tweenMode(ColorTween.ColorTweenMode value)`
  （void set_tween模式（颜色Tween.颜色Tween模式 value））
- `float get_duration()`
  （float get_duration（））
- `void set_duration(float value)`
  （void set_duration（float value））
- `bool get_ignoreTimeScale()`
  （bool get_ignore时间缩放（））
- `void set_ignoreTimeScale(bool value)`
  （void set_ignore时间缩放（bool value））
- `void TweenValue(float floatPercentage)`
  （void Tween值（float floatPercentage））
- `void AddOnChangedCallback(UnityAction<Color> callback)`
  （void 添加OnChanged回调（Unity引擎Action<Color> callback））
- `bool GetIgnoreTimescale()`
  （bool 获取IgnoreTimescale（））
- `float GetDuration()`
  （float 获取持续时间（））
- `bool ValidTarget()`
  （bool Valid目标（））

---

## ColorTween.ColorTweenMode（颜色Tween.颜色Tween模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ColorUsageAttribute（颜色UsageAttribute）

**继承**: PropertyAttribute（属性Attribute）

### 字段 (6)

- `bool showAlpha`（bool show透明度）(偏移: 0x8)
- `bool hdr`（bool hdr）(偏移: 0x9)
- `float minBrightness`（float minBrightness）(偏移: 0xC)
- `float maxBrightness`（float maxBrightness）(偏移: 0x10)
- `float minExposureValue`（float minExposure值）(偏移: 0x14)
- `float maxExposureValue`（float maxExposure值）(偏移: 0x18)

---

## ColorUtility（颜色工具）

### 方法 (1)

- `string ToHtmlStringRGB(Color color)`
  （string ToHtml字符串RGB颜色（颜色 color））

---

## ColorUtils（颜色Utils）

### 字段 (2)

- `float s_LightMeterCalibrationConstant`（float s_光照MeterCalibrationConstant）(偏移: 0x0)
- `float s_LensAttenuation`（float s_LensAttenuation）(偏移: 0x4)

### 方法 (12)

- `float get_lensImperfectionExposureScale()`
  （float get_lensImperfectionExposure缩放（））
- `float StandardIlluminantY(float x)`
  （float StandardIlluminantY（float x））
- `Vector3 CIExyToLMS(float x, float y)`
  （三维向量 CIExyToLMS（float x, float y））
- `Vector3 ColorBalanceToLMSCoeffs(float temperature, float tint)`
  （三维向量 颜色BalanceToLMSCoeffs（float temperature, float tint））
- `float Luminance(in Color color)`
  （float Luminance（in Color color））
- `float ComputeEV100(float aperture, float shutterSpeed, float ISO)`
  （float ComputeEV100（float aperture, float shutterSpeed, float ISO））
- `float ConvertEV100ToExposure(float EV100)`
  （float 转换EV100ToExposure（float EV100））
- `float ConvertExposureToEV100(float exposure)`
  （float 转换ExposureToEV100（float exposure））
- `float ComputeEV100FromAvgLuminance(float avgLuminance)`
  （float ComputeEV100FromAvgLuminance（float avgLuminance））
- `float ComputeISO(float aperture, float shutterSpeed, float targetEV100)`
  （float ComputeISO（float aperture, float shutterSpeed, float targetEV100））
- `uint ToHex(Color c)`
  （uint ToHex（颜色 c））
- `Color ToRGBA(uint hex)`
  （颜色 ToRGBA（uint hex））

---

## ColorWriteMask（颜色Write掩码）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ComCompatibleVersionAttribute（ComCompatibleVersionAttribute）

**继承**: Attribute（Attribute）

### 字段 (4)

- `int _major`（int _major）(偏移: 0x8)
- `int _minor`（int _minor）(偏移: 0xC)
- `int _build`（int _build）(偏移: 0x10)
- `int _revision`（int _revision）(偏移: 0x14)

---

## ComDefaultInterfaceAttribute（Com默认的InterfaceAttribute）

**继承**: Attribute（Attribute）

### 字段 (1)

- `Type _val`（类型 _val）(偏移: 0x8)

---

## ComInterfaceType（ComInterface类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ComVisibleAttribute（Com可见的Attribute）

**继承**: Attribute（Attribute）

### 字段 (1)

- `bool _val`（bool _val）(偏移: 0x8)

---

## CombineCallback（Combine回调）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `object Invoke(Vec3 position, object[] data, float[] weights)`
  （object Invoke（Vec3 position, object[] data, float[] weights））
- `IAsyncResult BeginInvoke(Vec3 position, object[] data, float[] weights, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Vec3 position, object[] data, float[] weights, 异步回调 callback, object object））
- `object EndInvoke(IAsyncResult result)`
  （object 结束Invoke（I异步Result result））

---

## CombineInstance（Combine实例）

### 字段 (5)

- `int m_MeshInstanceID`（int m_网格实例ID）(偏移: 0x0)
- `int m_SubMeshIndex`（int m_子网格索引）(偏移: 0x4)
- `Matrix4x4 m_Transform`（Matrix4x4 m_变换）(偏移: 0x8)
- `Vector4 m_LightmapScaleOffset`（Vector4 m_Lightmap缩放Offset）(偏移: 0x48)
- `Vector4 m_RealtimeLightmapScaleOffset`（Vector4 m_RealtimeLightmap缩放Offset）(偏移: 0x58)

### 方法 (2)

- `void set_mesh(Mesh value)`
  （void set_mesh（网格 value））
- `void set_transform(Matrix4x4 value)`
  （void set_transform（Matrix4x4 value））

---

## CommandBuffer（Command缓冲区）

**继承**: IDisposable（IDisposable）

### 字段 (1)

- `IntPtr m_Ptr`（整数Ptr m_Ptr）(偏移: 0x8)

### 方法 (116)

- `void Internal_SetSinglePassStereo(SinglePassStereoMode mode)`
  （void Internal_集合单个PassStereo（单个PassStereo模式 mode））
- `IntPtr InitBuffer()`
  （整数Ptr 初始化缓冲区（））
- `IntPtr CreateGPUFence_Internal(GraphicsFenceType fenceType, SynchronisationStageFlags stage)`
  （整数Ptr 创建GPUFence_内部的（GraphicsFence类型 fenceType, SynchronisationStageFlags stage））
- `void WaitOnGPUFence_Internal(IntPtr fencePtr, SynchronisationStageFlags stage)`
  （void WaitOnGPUFence_内部的（整数Ptr fencePtr, SynchronisationStageFlags stage））
- `void ReleaseBuffer()`
  （void Release缓冲区（））
- `void Internal_SetComputeTextureParam(ComputeShader computeShader, int kernelIndex, int nameID, ref RenderTargetIdentifier rt, int mipLevel, RenderTextureSubElement element)`
  （void Internal_集合Compute纹理Param（Compute着色器 computeShader, int kernelIndex, int nameID, ref RenderTargetIdentifier rt, int mipLevel, Render纹理子元素 element））
- `void Internal_SetComputeConstantComputeBufferParam(ComputeShader computeShader, int nameID, ComputeBuffer buffer, int offset, int size)`
  （void Internal_集合ComputeConstantCompute缓冲区Param（Compute着色器 computeShader, int nameID, Compute缓冲区 buffer, int offset, int size））
- `void Internal_DispatchCompute(ComputeShader computeShader, int kernelIndex, int threadGroupsX, int threadGroupsY, int threadGroupsZ)`
  （void Internal_DispatchCompute（Compute着色器 computeShader, int kernelIndex, int threadGroupsX, int threadGroupsY, int threadGroupsZ））
- `void set_name(string value)`
  （void set_name（string value））
- `void Clear()`
  （void 清除（））
- `void Internal_DrawMesh(Mesh mesh, Matrix4x4 matrix, Material material, int submeshIndex, int shaderPass, MaterialPropertyBlock properties)`
  （void Internal_Draw网格（网格 mesh, Matrix4x4 matrix, 材质 material, int submeshIndex, int shaderPass, 材质属性Block properties））
- `void Internal_DrawRenderer(Renderer renderer, Material material, int submeshIndex, int shaderPass)`
  （void Internal_Draw渲染器（渲染器 renderer, 材质 material, int submeshIndex, int shaderPass））
- `void Internal_DrawProcedural(Matrix4x4 matrix, Material material, int shaderPass, MeshTopology topology, int vertexCount, int instanceCount, MaterialPropertyBlock properties)`
  （void Internal_DrawProcedural（Matrix4x4 matrix, 材质 material, int shaderPass, 网格Topology topology, int vertexCount, int instanceCount, 材质属性Block properties））
- `void Internal_DrawOcclusionMesh(RectInt normalizedCamViewport)`
  （void Internal_DrawOcclusion网格（Rect整数 normalizedCamViewport））
- `void SetViewport(Rect pixelRect)`
  （void 集合Viewport（Rect pixelRect））
- `void EnableScissorRect(Rect scissor)`
  （void 启用ScissorRect（Rect scissor））
- `void DisableScissorRect()`
  （void 禁用ScissorRect（））
- `void Blit_Identifier(ref RenderTargetIdentifier source, ref RenderTargetIdentifier dest, Material mat, int pass, Vector2 scale, Vector2 offset, int sourceDepthSlice, int destDepthSlice)`
  （void Blit_Identifier（ref RenderTargetIdentifier source, ref RenderTargetIdentifier dest, 材质 mat, int pass, 二维向量 scale, 二维向量 offset, int sourceDepthSlice, int destDepthSlice））
- `void GetTemporaryRT(int nameID, int width, int height, int depthBuffer, FilterMode filter, GraphicsFormat format, int antiAliasing, bool enableRandomWrite, RenderTextureMemoryless memorylessMode, bool useDynamicScale)`
  （void 获取临时的RT（int nameID, int width, int height, int depthBuffer, Filter模式 filter, Graphics格式化 format, int antiAliasing, bool enableRandomWrite, Render纹理Memoryless memorylessMode, bool useDynamicScale））
- `void GetTemporaryRT(int nameID, int width, int height, int depthBuffer, FilterMode filter, GraphicsFormat format, int antiAliasing, bool enableRandomWrite, RenderTextureMemoryless memorylessMode)`
  （void 获取临时的RT（int nameID, int width, int height, int depthBuffer, Filter模式 filter, Graphics格式化 format, int antiAliasing, bool enableRandomWrite, Render纹理Memoryless memorylessMode））
- `void GetTemporaryRT(int nameID, int width, int height, int depthBuffer, FilterMode filter, GraphicsFormat format, int antiAliasing)`
  （void 获取临时的RT（int nameID, int width, int height, int depthBuffer, Filter模式 filter, Graphics格式化 format, int antiAliasing））
- `void GetTemporaryRT(int nameID, int width, int height, int depthBuffer, FilterMode filter, GraphicsFormat format)`
  （void 获取临时的RT（int nameID, int width, int height, int depthBuffer, Filter模式 filter, Graphics格式化 format））
- `void GetTemporaryRT(int nameID, int width, int height, int depthBuffer, FilterMode filter, RenderTextureFormat format)`
  （void 获取临时的RT（int nameID, int width, int height, int depthBuffer, Filter模式 filter, Render纹理格式化 format））
- `void GetTemporaryRTWithDescriptor(int nameID, RenderTextureDescriptor desc, FilterMode filter)`
  （void 获取临时的RTWithDescriptor（int nameID, Render纹理Descriptor desc, Filter模式 filter））
- `void GetTemporaryRT(int nameID, RenderTextureDescriptor desc, FilterMode filter)`
  （void 获取临时的RT（int nameID, Render纹理Descriptor desc, Filter模式 filter））
- `void GetTemporaryRT(int nameID, RenderTextureDescriptor desc)`
  （void 获取临时的RT（int nameID, Render纹理Descriptor desc））
- `void ReleaseTemporaryRT(int nameID)`
  （void Release临时的RT（int nameID））
- `void ClearRenderTarget(bool clearDepth, bool clearColor, Color backgroundColor, float depth)`
  （void 清除Render目标（bool clearDepth, bool clearColor, 颜色 backgroundColor, float depth））
- `void ClearRenderTarget(bool clearDepth, bool clearColor, Color backgroundColor)`
  （void 清除Render目标（bool clearDepth, bool clearColor, 颜色 backgroundColor））
- `void SetGlobalFloat(int nameID, float value)`
  （void 集合全局的浮点数（int nameID, float value））
- `void SetGlobalInt(int nameID, int value)`
  （void 集合全局的整数（int nameID, int value））
- `void SetGlobalVector(int nameID, Vector4 value)`
  （void 集合全局的向量（int nameID, Vector4 value））
- `void SetGlobalColor(int nameID, Color value)`
  （void 集合全局的颜色（int nameID, 颜色 value））
- `void SetGlobalMatrix(int nameID, Matrix4x4 value)`
  （void 集合全局的矩阵（int nameID, Matrix4x4 value））
- `void EnableShaderKeyword(string keyword)`
  （void 启用着色器Keyword（string keyword））
- `void DisableShaderKeyword(string keyword)`
  （void 禁用着色器Keyword（string keyword））
- `void SetViewProjectionMatrices(Matrix4x4 view, Matrix4x4 proj)`
  （void 集合视图ProjectionMatrices（Matrix4x4 view, Matrix4x4 proj））
- `void SetExecutionFlags(CommandBufferExecutionFlags flags)`
  （void 集合ExecutionFlags（Command缓冲区ExecutionFlags flags））
- `bool ValidateAgainstExecutionFlags(CommandBufferExecutionFlags requiredFlags, CommandBufferExecutionFlags invalidFlags)`
  （bool 验证AgainstExecutionFlags（Command缓冲区ExecutionFlags requiredFlags, Command缓冲区ExecutionFlags invalidFlags））
- `void SetGlobalVectorArray(int nameID, Vector4[] values)`
  （void 集合全局的向量数组（int nameID, Vector4[] values））
- `void SetGlobalMatrixArray(int nameID, Matrix4x4[] values)`
  （void 集合全局的矩阵数组（int nameID, Matrix4x4[] values））
- `void SetLateLatchProjectionMatrices(Matrix4x4[] projectionMat)`
  （void 集合延迟LatchProjectionMatrices（Matrix4x4[] projectionMat））
- `void MarkLateLatchMatrixShaderPropertyID(CameraLateLatchMatrixType matrixPropertyType, int shaderPropertyID)`
  （void Mark延迟Latch矩阵着色器属性ID（摄像机延迟Latch矩阵类型 matrixPropertyType, int shaderPropertyID））
- `void UnmarkLateLatchMatrix(CameraLateLatchMatrixType matrixPropertyType)`
  （void Unmark延迟Latch矩阵（摄像机延迟Latch矩阵类型 matrixPropertyType））
- `void SetGlobalTexture_Impl(int nameID, ref RenderTargetIdentifier rt, RenderTextureSubElement element)`
  （void 集合全局的Texture_Impl（int nameID, ref RenderTargetIdentifier rt, Render纹理子元素 element））
- `void SetGlobalBufferInternal(int nameID, ComputeBuffer value)`
  （void 集合全局的缓冲区内部的（int nameID, Compute缓冲区 value））
- `void BeginSample(string name)`
  （void BeginSample（string name））
- `void EndSample(string name)`
  （void 结束Sample（string name））
- `void BeginSample(CustomSampler sampler)`
  （void BeginSample（自定义的Sampler sampler））
- `void EndSample(CustomSampler sampler)`
  （void 结束Sample（自定义的Sampler sampler））
- `void BeginSample_CustomSampler(CustomSampler sampler)`
  （void BeginSample_自定义的Sampler（自定义的Sampler sampler））
- `void EndSample_CustomSampler(CustomSampler sampler)`
  （void 结束Sample_自定义的Sampler（自定义的Sampler sampler））
- `void SetGlobalConstantBufferInternal(ComputeBuffer buffer, int nameID, int offset, int size)`
  （void 集合全局的Constant缓冲区内部的（Compute缓冲区 buffer, int nameID, int offset, int size））
- `void SetInstanceMultiplier(uint multiplier)`
  （void 集合实例Multiplier（uint multiplier））
- `void SetRenderTarget(RenderTargetIdentifier rt)`
  （void 集合Render目标（Render目标Identifier rt））
- `void SetRenderTarget(RenderTargetIdentifier rt, RenderBufferLoadAction loadAction, RenderBufferStoreAction storeAction)`
  （void 集合Render目标（Render目标Identifier rt, Render缓冲区加载动作 loadAction, Render缓冲区商店动作 storeAction））
- `void SetRenderTarget(RenderTargetIdentifier rt, RenderBufferLoadAction colorLoadAction, RenderBufferStoreAction colorStoreAction, RenderBufferLoadAction depthLoadAction, RenderBufferStoreAction depthStoreAction)`
  （void 集合Render目标（Render目标Identifier rt, Render缓冲区加载动作 colorLoadAction, Render缓冲区商店动作 colorStoreAction, Render缓冲区加载动作 depthLoadAction, Render缓冲区商店动作 depthStoreAction））
- `void SetRenderTarget(RenderTargetIdentifier rt, int mipLevel, CubemapFace cubemapFace, int depthSlice)`
  （void 集合Render目标（Render目标Identifier rt, int mipLevel, CubemapFace cubemapFace, int depthSlice））
- `void SetRenderTarget(RenderTargetIdentifier color, RenderTargetIdentifier depth)`
  （void 集合Render目标（Render目标Identifier color, Render目标Identifier depth））
- `void SetRenderTarget(RenderTargetIdentifier color, RenderTargetIdentifier depth, int mipLevel, CubemapFace cubemapFace, int depthSlice)`
  （void 集合Render目标（Render目标Identifier color, Render目标Identifier depth, int mipLevel, CubemapFace cubemapFace, int depthSlice））
- `void SetRenderTarget(RenderTargetIdentifier color, RenderBufferLoadAction colorLoadAction, RenderBufferStoreAction colorStoreAction, RenderTargetIdentifier depth, RenderBufferLoadAction depthLoadAction, RenderBufferStoreAction depthStoreAction)`
  （void 集合Render目标（Render目标Identifier color, Render缓冲区加载动作 colorLoadAction, Render缓冲区商店动作 colorStoreAction, Render目标Identifier depth, Render缓冲区加载动作 depthLoadAction, Render缓冲区商店动作 depthStoreAction））
- `void SetRenderTarget(RenderTargetIdentifier[] colors, RenderTargetIdentifier depth, int mipLevel, CubemapFace cubemapFace, int depthSlice)`
  （void 集合Render目标（Render目标Identifier[] colors, Render目标Identifier depth, int mipLevel, CubemapFace cubemapFace, int depthSlice））
- `void SetRenderTargetSingle_Internal(RenderTargetIdentifier rt, RenderBufferLoadAction colorLoadAction, RenderBufferStoreAction colorStoreAction, RenderBufferLoadAction depthLoadAction, RenderBufferStoreAction depthStoreAction)`
  （void 集合Render目标Single_内部的（Render目标Identifier rt, Render缓冲区加载动作 colorLoadAction, Render缓冲区商店动作 colorStoreAction, Render缓冲区加载动作 depthLoadAction, Render缓冲区商店动作 depthStoreAction））
- `void SetRenderTargetColorDepth_Internal(RenderTargetIdentifier color, RenderTargetIdentifier depth, RenderBufferLoadAction colorLoadAction, RenderBufferStoreAction colorStoreAction, RenderBufferLoadAction depthLoadAction, RenderBufferStoreAction depthStoreAction, RenderTargetFlags flags)`
  （void 集合Render目标颜色Depth_内部的（Render目标Identifier color, Render目标Identifier depth, Render缓冲区加载动作 colorLoadAction, Render缓冲区商店动作 colorStoreAction, Render缓冲区加载动作 depthLoadAction, Render缓冲区商店动作 depthStoreAction, Render目标Flags flags））
- `void SetRenderTargetMultiSubtarget(RenderTargetIdentifier[] colors, RenderTargetIdentifier depth, RenderBufferLoadAction[] colorLoadActions, RenderBufferStoreAction[] colorStoreActions, RenderBufferLoadAction depthLoadAction, RenderBufferStoreAction depthStoreAction, int mipLevel, CubemapFace cubemapFace, int depthSlice)`
  （void 集合Render目标多个Subtarget（Render目标Identifier[] colors, Render目标Identifier depth, Render缓冲区加载Action[] colorLoadActions, Render缓冲区商店Action[] colorStoreActions, Render缓冲区加载动作 depthLoadAction, Render缓冲区商店动作 depthStoreAction, int mipLevel, CubemapFace cubemapFace, int depthSlice））
- `void SetComputeBufferData(ComputeBuffer buffer, Array data)`
  （void 集合Compute缓冲区数据（Compute缓冲区 buffer, 数组 data））
- `void InternalSetComputeBufferData(ComputeBuffer buffer, Array data, int managedBufferStartIndex, int graphicsBufferStartIndex, int count, int elemSize)`
  （void 内部的集合Compute缓冲区数据（Compute缓冲区 buffer, 数组 data, int managedBufferStartIndex, int graphicsBufferStartIndex, int count, int elemSize））
- `void Finalize()`
  （void Finalize（））
- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））
- `void Release()`
  （void Release（））
- `GraphicsFence CreateAsyncGraphicsFence()`
  （GraphicsFence 创建异步GraphicsFence（））
- `GraphicsFence CreateGraphicsFence(GraphicsFenceType fenceType, SynchronisationStageFlags stage)`
  （GraphicsFence 创建GraphicsFence（GraphicsFence类型 fenceType, SynchronisationStageFlags stage））
- `void WaitOnAsyncGraphicsFence(GraphicsFence fence)`
  （void WaitOn异步GraphicsFence（GraphicsFence fence））
- `void WaitOnAsyncGraphicsFence(GraphicsFence fence, SynchronisationStage stage)`
  （void WaitOn异步GraphicsFence（GraphicsFence fence, SynchronisationStage stage））
- `void WaitOnAsyncGraphicsFence(GraphicsFence fence, SynchronisationStageFlags stage)`
  （void WaitOn异步GraphicsFence（GraphicsFence fence, SynchronisationStageFlags stage））
- `void SetComputeTextureParam(ComputeShader computeShader, int kernelIndex, string name, RenderTargetIdentifier rt)`
  （void 集合Compute纹理Param（Compute着色器 computeShader, int kernelIndex, string name, Render目标Identifier rt））
- `void SetComputeConstantBufferParam(ComputeShader computeShader, int nameID, ComputeBuffer buffer, int offset, int size)`
  （void 集合ComputeConstant缓冲区Param（Compute着色器 computeShader, int nameID, Compute缓冲区 buffer, int offset, int size））
- `void DispatchCompute(ComputeShader computeShader, int kernelIndex, int threadGroupsX, int threadGroupsY, int threadGroupsZ)`
  （void DispatchCompute（Compute着色器 computeShader, int kernelIndex, int threadGroupsX, int threadGroupsY, int threadGroupsZ））
- `void DrawMesh(Mesh mesh, Matrix4x4 matrix, Material material, int submeshIndex, int shaderPass, MaterialPropertyBlock properties)`
  （void Draw网格（网格 mesh, Matrix4x4 matrix, 材质 material, int submeshIndex, int shaderPass, 材质属性Block properties））
- `void DrawMesh(Mesh mesh, Matrix4x4 matrix, Material material, int submeshIndex, int shaderPass)`
  （void Draw网格（网格 mesh, Matrix4x4 matrix, 材质 material, int submeshIndex, int shaderPass））
- `void DrawMesh(Mesh mesh, Matrix4x4 matrix, Material material, int submeshIndex)`
  （void Draw网格（网格 mesh, Matrix4x4 matrix, 材质 material, int submeshIndex））
- `void DrawMesh(Mesh mesh, Matrix4x4 matrix, Material material)`
  （void Draw网格（网格 mesh, Matrix4x4 matrix, 材质 material））
- `void DrawRenderer(Renderer renderer, Material material, int submeshIndex, int shaderPass)`
  （void Draw渲染器（渲染器 renderer, 材质 material, int submeshIndex, int shaderPass））
- `void DrawRenderer(Renderer renderer, Material material, int submeshIndex)`
  （void Draw渲染器（渲染器 renderer, 材质 material, int submeshIndex））
- `void DrawRenderer(Renderer renderer, Material material)`
  （void Draw渲染器（渲染器 renderer, 材质 material））
- `void DrawProcedural(Matrix4x4 matrix, Material material, int shaderPass, MeshTopology topology, int vertexCount, int instanceCount, MaterialPropertyBlock properties)`
  （void DrawProcedural（Matrix4x4 matrix, 材质 material, int shaderPass, 网格Topology topology, int vertexCount, int instanceCount, 材质属性Block properties））
- `void DrawProcedural(Matrix4x4 matrix, Material material, int shaderPass, MeshTopology topology, int vertexCount, int instanceCount)`
  （void DrawProcedural（Matrix4x4 matrix, 材质 material, int shaderPass, 网格Topology topology, int vertexCount, int instanceCount））
- `void DrawProcedural(Matrix4x4 matrix, Material material, int shaderPass, MeshTopology topology, int vertexCount)`
  （void DrawProcedural（Matrix4x4 matrix, 材质 material, int shaderPass, 网格Topology topology, int vertexCount））
- `void DrawOcclusionMesh(RectInt normalizedCamViewport)`
  （void DrawOcclusion网格（Rect整数 normalizedCamViewport））
- `void Blit(RenderTargetIdentifier source, RenderTargetIdentifier dest)`
  （void Blit（Render目标Identifier source, Render目标Identifier dest））
- `void Blit(RenderTargetIdentifier source, RenderTargetIdentifier dest, Material mat)`
  （void Blit（Render目标Identifier source, Render目标Identifier dest, 材质 mat））
- `void Blit(RenderTargetIdentifier source, RenderTargetIdentifier dest, Material mat, int pass)`
  （void Blit（Render目标Identifier source, Render目标Identifier dest, 材质 mat, int pass））
- `void SetGlobalVector(string name, Vector4 value)`
  （void 集合全局的向量（string name, Vector4 value））
- `void SetGlobalVectorArray(string propertyName, Vector4[] values)`
  （void 集合全局的向量数组（string propertyName, Vector4[] values））
- `void SetGlobalTexture(string name, RenderTargetIdentifier value)`
  （void 集合全局的纹理（string name, Render目标Identifier value））
- `void SetGlobalTexture(int nameID, RenderTargetIdentifier value)`
  （void 集合全局的纹理（int nameID, Render目标Identifier value））
- `void SetGlobalTexture(int nameID, RenderTargetIdentifier value, RenderTextureSubElement element)`
  （void 集合全局的纹理（int nameID, Render目标Identifier value, Render纹理子元素 element））
- `void SetGlobalBuffer(int nameID, ComputeBuffer value)`
  （void 集合全局的缓冲区（int nameID, Compute缓冲区 value））
- `void SetGlobalConstantBuffer(ComputeBuffer buffer, int nameID, int offset, int size)`
  （void 集合全局的Constant缓冲区（Compute缓冲区 buffer, int nameID, int offset, int size））
- `void SetSinglePassStereo(SinglePassStereoMode mode)`
  （void 集合单个PassStereo（单个PassStereo模式 mode））
- `void Internal_DrawMesh_Injected(Mesh mesh, ref Matrix4x4 matrix, Material material, int submeshIndex, int shaderPass, MaterialPropertyBlock properties)`
  （void Internal_DrawMesh_Injected（网格 mesh, ref Matrix4x4 matrix, 材质 material, int submeshIndex, int shaderPass, 材质属性Block properties））
- `void Internal_DrawProcedural_Injected(ref Matrix4x4 matrix, Material material, int shaderPass, MeshTopology topology, int vertexCount, int instanceCount, MaterialPropertyBlock properties)`
  （void Internal_DrawProcedural_Injected（ref Matrix4x4 matrix, 材质 material, int shaderPass, 网格Topology topology, int vertexCount, int instanceCount, 材质属性Block properties））
- `void Internal_DrawOcclusionMesh_Injected(ref RectInt normalizedCamViewport)`
  （void Internal_DrawOcclusionMesh_Injected（ref RectInt normalizedCamViewport））
- `void SetViewport_Injected(ref Rect pixelRect)`
  （void 集合Viewport_Injected（ref Rect pixelRect））
- `void EnableScissorRect_Injected(ref Rect scissor)`
  （void 启用ScissorRect_Injected（ref Rect scissor））
- `void Blit_Identifier_Injected(ref RenderTargetIdentifier source, ref RenderTargetIdentifier dest, Material mat, int pass, ref Vector2 scale, ref Vector2 offset, int sourceDepthSlice, int destDepthSlice)`
  （void Blit_Identifier_Injected（ref RenderTargetIdentifier source, ref RenderTargetIdentifier dest, 材质 mat, int pass, ref Vector2 scale, ref Vector2 offset, int sourceDepthSlice, int destDepthSlice））
- `void GetTemporaryRTWithDescriptor_Injected(int nameID, ref RenderTextureDescriptor desc, FilterMode filter)`
  （void 获取临时的RTWithDescriptor_Injected（int nameID, ref RenderTextureDescriptor desc, Filter模式 filter））
- `void ClearRenderTarget_Injected(bool clearDepth, bool clearColor, ref Color backgroundColor, float depth)`
  （void 清除RenderTarget_Injected（bool clearDepth, bool clearColor, ref Color backgroundColor, float depth））
- `void SetGlobalVector_Injected(int nameID, ref Vector4 value)`
  （void 集合全局的Vector_Injected（int nameID, ref Vector4 value））
- `void SetGlobalColor_Injected(int nameID, ref Color value)`
  （void 集合全局的Color_Injected（int nameID, ref Color value））
- `void SetGlobalMatrix_Injected(int nameID, ref Matrix4x4 value)`
  （void 集合全局的Matrix_Injected（int nameID, ref Matrix4x4 value））
- `void SetViewProjectionMatrices_Injected(ref Matrix4x4 view, ref Matrix4x4 proj)`
  （void 集合视图ProjectionMatrices_Injected（ref Matrix4x4 view, ref Matrix4x4 proj））
- `void SetRenderTargetSingle_Internal_Injected(ref RenderTargetIdentifier rt, RenderBufferLoadAction colorLoadAction, RenderBufferStoreAction colorStoreAction, RenderBufferLoadAction depthLoadAction, RenderBufferStoreAction depthStoreAction)`
  （void 集合Render目标Single_Internal_Injected（ref RenderTargetIdentifier rt, Render缓冲区加载动作 colorLoadAction, Render缓冲区商店动作 colorStoreAction, Render缓冲区加载动作 depthLoadAction, Render缓冲区商店动作 depthStoreAction））
- `void SetRenderTargetColorDepth_Internal_Injected(ref RenderTargetIdentifier color, ref RenderTargetIdentifier depth, RenderBufferLoadAction colorLoadAction, RenderBufferStoreAction colorStoreAction, RenderBufferLoadAction depthLoadAction, RenderBufferStoreAction depthStoreAction, RenderTargetFlags flags)`
  （void 集合Render目标颜色Depth_Internal_Injected（ref RenderTargetIdentifier color, ref RenderTargetIdentifier depth, Render缓冲区加载动作 colorLoadAction, Render缓冲区商店动作 colorStoreAction, Render缓冲区加载动作 depthLoadAction, Render缓冲区商店动作 depthStoreAction, Render目标Flags flags））
- `void SetRenderTargetMultiSubtarget_Injected(RenderTargetIdentifier[] colors, ref RenderTargetIdentifier depth, RenderBufferLoadAction[] colorLoadActions, RenderBufferStoreAction[] colorStoreActions, RenderBufferLoadAction depthLoadAction, RenderBufferStoreAction depthStoreAction, int mipLevel, CubemapFace cubemapFace, int depthSlice)`
  （void 集合Render目标多个Subtarget_Injected（Render目标Identifier[] colors, ref RenderTargetIdentifier depth, Render缓冲区加载Action[] colorLoadActions, Render缓冲区商店Action[] colorStoreActions, Render缓冲区加载动作 depthLoadAction, Render缓冲区商店动作 depthStoreAction, int mipLevel, CubemapFace cubemapFace, int depthSlice））

---

## CommandBufferExecutionFlags（Command缓冲区ExecutionFlags）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## CommandBufferExtensions（Command缓冲区Extensions）

### 方法 (4)

- `void Internal_SwitchIntoFastMemory(CommandBuffer cmd, ref RenderTargetIdentifier rt, FastMemoryFlags fastMemoryFlags, float residency, bool copyContents)`
  （void Internal_SwitchIntoFastMemory（Command缓冲区 cmd, ref RenderTargetIdentifier rt, FastMemoryFlags fastMemoryFlags, float residency, bool copyContents））
- `void Internal_SwitchOutOfFastMemory(CommandBuffer cmd, ref RenderTargetIdentifier rt, bool copyContents)`
  （void Internal_SwitchOutOfFastMemory（Command缓冲区 cmd, ref RenderTargetIdentifier rt, bool copyContents））
- `void SwitchIntoFastMemory(CommandBuffer cmd, RenderTargetIdentifier rid, FastMemoryFlags fastMemoryFlags, float residency, bool copyContents)`
  （void SwitchIntoFastMemory（Command缓冲区 cmd, Render目标Identifier rid, FastMemoryFlags fastMemoryFlags, float residency, bool copyContents））
- `void SwitchOutOfFastMemory(CommandBuffer cmd, RenderTargetIdentifier rid, bool copyContents)`
  （void SwitchOutOfFastMemory（Command缓冲区 cmd, Render目标Identifier rid, bool copyContents））

---

## CommandBufferPool（Command缓冲区池）

### 字段 (1)

- `ObjectPool<CommandBuffer> s_BufferPool`（对象Pool<CommandBuffer> s_缓冲区池）(偏移: 0x301A3013)

### 方法 (3)

- `CommandBuffer Get()`
  （Command缓冲区 获取（））
- `CommandBuffer Get(string name)`
  （Command缓冲区 获取（string name））
- `void Release(CommandBuffer buffer)`
  （void Release（Command缓冲区 buffer））

---

## Comments（Comments）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (1)

- `string text`（string text）(偏移: 0xC)

---

## CommonHud_1（CommonHud_1）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (9)

- `CommonHud_1.Type graphicType`（CommonHud_1.类型 graphic类型）(偏移: 0xC)
- `Image image`（图像 image）(偏移: 0x10)
- `RawImage rawImage`（Raw图像 raw图像）(偏移: 0x14)
- `Text text`（文本 text）(偏移: 0x18)
- `float fadeInTime`（float fadeIn时间）(偏移: 0x1C)
- `float normalTime`（float normal时间）(偏移: 0x20)
- `float fadeOutTime`（float fadeOut时间）(偏移: 0x24)
- `Color defaultColor`（颜色 default颜色）(偏移: 0x28)
- `Color zeroAlphaColor`（颜色 zero透明度颜色）(偏移: 0x38)

### 方法 (15)

- `void Awake()`
  （void Awake（））
- `void Show(float inTime, float normalTime, float outTime)`
  （void 显示（float inTime, float normalTime, float outTime））
- `void Show()`
  （void 显示（））
- `void EnterNormalState()`
  （void Enter法线状态（））
- `void EnterFadeOutState()`
  （void EnterFadeOut状态（））
- `void SetGraphColor(Color color)`
  （void 集合Graph颜色（颜色 color））
- `void SetSprite(Sprite spr)`
  （void 集合精灵（精灵 spr））
- `void SetTexture(Texture tex)`
  （void 集合纹理（纹理 tex））
- `void SetText(string msg)`
  （void 集合文本（string msg））
- `void SetFontSize(int size)`
  （void 集合Font大小（int size））
- `void SetPos(Vector2 pos)`
  （void 集合Pos（二维向量 pos））
- `void SetTime(float inTime, float normalTime, float outTime)`
  （void 集合时间（float inTime, float normalTime, float outTime））
- `void Shake(float duration)`
  （void 震动（float duration））
- `void Shake(float duration, Vector2 originPos)`
  （void 震动（float duration, 二维向量 originPos））
- `void Stop()`
  （void 停止（））

---

## CommonHud_1.Type（CommonHud_1.类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## CommonKillMark（Common击杀Mark）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (3)

- `RectTransform rect`（Rect变换 rect）(偏移: 0xC)
- `RawImage image`（Raw图像 image）(偏移: 0x10)
- `Vector2 startPos`（二维向量 startPos）(偏移: 0x14)

### 方法 (3)

- `void Start()`
  （void 开始（））
- `void Play(Texture tex)`
  （void 播放（纹理 tex））
- `void Stop()`
  （void 停止（））

---

## CompactVoxelCell（CompactVoxelCell）

### 字段 (2)

- `uint index`（uint index）(偏移: 0x0)
- `uint count`（uint count）(偏移: 0x4)

---

## CompactVoxelSpan（CompactVoxelSpan）

### 字段 (4)

- `ushort y`（ushort y）(偏移: 0x0)
- `uint con`（uint con）(偏移: 0x4)
- `uint h`（uint h）(偏移: 0x8)
- `int reg`（int reg）(偏移: 0xC)

### 方法 (2)

- `void SetConnection(int dir, uint value)`
  （void 集合连接（int dir, uint value））
- `int GetConnection(int dir)`
  （int 获取连接（int dir））

---

## CompareFunction（CompareFunction）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## CompareInfo（Compare信息）

**继承**: IDeserializationCallback（IDeserialization回调）

### 字段 (8)

- `string m_name`（string m_name）(偏移: 0x8)
- `string m_sortName`（string m_sort名称）(偏移: 0xC)
- `int win32LCID`（int win32LCID）(偏移: 0x10)
- `int culture`（int culture）(偏移: 0x14)
- `SortVersion m_SortVersion`（SortVersion m_SortVersion）(偏移: 0x18)
- `SimpleCollator collator`（SimpleCollator collator）(偏移: 0x1C)
- `bool managedCollation`（bool managedCollation）(偏移: 0x4)
- `bool managedCollationChecked`（bool managedCollationChecked）(偏移: 0x5)

### 方法 (31)

- `CompareInfo GetCompareInfo(string name)`
  （Compare信息 获取Compare信息（string name））
- `void OnDeserializing(StreamingContext ctx)`
  （void OnDeserializing（StreamingContext ctx））
- `void OnDeserialized()`
  （void OnDeserialized（））
- `void OnDeserialized(StreamingContext ctx)`
  （void OnDeserialized（StreamingContext ctx））
- `void OnSerializing(StreamingContext ctx)`
  （void OnSerializing（StreamingContext ctx））
- `string get_Name()`
  （string get_名称（））
- `int Compare(string string1, string string2)`
  （int Compare（string string1, string string2））
- `int Compare(string string1, string string2, CompareOptions options)`
  （int Compare（string string1, string string2, CompareOptions options））
- `int Compare(string string1, int offset1, int length1, string string2, int offset2, int length2, CompareOptions options)`
  （int Compare（string string1, int offset1, int length1, string string2, int offset2, int length2, CompareOptions options））
- `int CompareOrdinal(string string1, int offset1, int length1, string string2, int offset2, int length2)`
  （int CompareOrdinal（string string1, int offset1, int length1, string string2, int offset2, int length2））
- `bool IsPrefix(string source, string prefix, CompareOptions options)`
  （bool 是否Prefix（string source, string prefix, CompareOptions options））
- `bool IsSuffix(string source, string suffix, CompareOptions options)`
  （bool 是否Suffix（string source, string suffix, CompareOptions options））
- `int IndexOf(string source, string value, int startIndex, int count, CompareOptions options)`
  （int 索引Of（string source, string value, int startIndex, int count, CompareOptions options））
- `int LastIndexOf(string source, string value, int startIndex, int count, CompareOptions options)`
  （int 最后一个索引Of（string source, string value, int startIndex, int count, CompareOptions options））
- `SortKey GetSortKey(string source, CompareOptions options)`
  （Sort键 获取Sort键（string source, CompareOptions options））
- `SortKey CreateSortKey(string source, CompareOptions options)`
  （Sort键 创建Sort键（string source, CompareOptions options））
- `bool Equals(object value)`
  （bool Equals（object value））
- `int GetHashCode()`
  （int 获取HashCode（））
- `int GetHashCodeOfString(string source, CompareOptions options)`
  （int 获取HashCodeOf字符串（string source, CompareOptions options））
- `int GetHashCodeOfString(string source, CompareOptions options, bool forceRandomizedHashing, long additionalEntropy)`
  （int 获取HashCodeOf字符串（string source, CompareOptions options, bool forceRandomizedHashing, long additionalEntropy））
- `string ToString()`
  （string To字符串（））
- `bool get_UseManagedCollation()`
  （bool get_UseManagedCollation（））
- `SimpleCollator GetCollator()`
  （SimpleCollator 获取Collator（））
- `SortKey CreateSortKeyCore(string source, CompareOptions options)`
  （Sort键 创建Sort键Core（string source, CompareOptions options））
- `int internal_index_switch(string s1, int sindex, int count, string s2, CompareOptions opt, bool first)`
  （int internal_index_switch（string s1, int sindex, int count, string s2, CompareOptions opt, bool first））
- `int internal_compare_switch(string str1, int offset1, int length1, string str2, int offset2, int length2, CompareOptions options)`
  （int internal_compare_switch（string str1, int offset1, int length1, string str2, int offset2, int length2, CompareOptions options））
- `int internal_compare_managed(string str1, int offset1, int length1, string str2, int offset2, int length2, CompareOptions options)`
  （int internal_compare_managed（string str1, int offset1, int length1, string str2, int offset2, int length2, CompareOptions options））
- `int internal_index_managed(string s1, int sindex, int count, string s2, CompareOptions opt, bool first)`
  （int internal_index_managed（string s1, int sindex, int count, string s2, CompareOptions opt, bool first））
- `void assign_sortkey(object key, string source, CompareOptions options)`
  （void assign_sortkey（object key, string source, CompareOptions options））
- `int internal_compare(string str1, int offset1, int length1, string str2, int offset2, int length2, CompareOptions options)`
  （int internal_compare（string str1, int offset1, int length1, string str2, int offset2, int length2, CompareOptions options））
- `int internal_index(string source, int sindex, int count, string value, CompareOptions options, bool first)`
  （int internal_index（string source, int sindex, int count, string value, CompareOptions options, bool first））

---

## CompareOptions（CompareOptions）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Comparer（Comparer）

**继承**: IComparer, ISerializable（IComparer, ISerializable）

### 字段 (3)

- `CompareInfo m_compareInfo`（Compare信息 m_compare信息）(偏移: 0x8)
- `Comparer Default`（Comparer 默认的）(偏移: 0x0)
- `Comparer DefaultInvariant`（Comparer 默认的Invariant）(偏移: 0x4)

### 方法 (2)

- `int Compare(object a, object b)`
  （int Compare（object a, object b））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））

---

## CompatibilitySwitches（CompatibilitySwitches）

### 字段 (2)

- `bool IsAppEarlierThanSilverlight4`（bool 是否AppEarlierThanSilverlight4）(偏移: 0x0)
- `bool IsAppEarlierThanWindowsPhone8`（bool 是否AppEarlierThanWindowsPhone8）(偏移: 0x1)

---

## CompatibleComparer（CompatibleComparer）

**继承**: IEqualityComparer（IEqualityComparer）

### 字段 (2)

- `IComparer _comparer`（IComparer _comparer）(偏移: 0x8)
- `IHashCodeProvider _hcp`（IHashCode提供者 _hcp）(偏移: 0xC)

### 方法 (5)

- `int Compare(object a, object b)`
  （int Compare（object a, object b））
- `bool Equals(object a, object b)`
  （bool Equals（object a, object b））
- `int GetHashCode(object obj)`
  （int 获取HashCode（object obj））
- `IComparer get_Comparer()`
  （IComparer get_Comparer（））
- `IHashCodeProvider get_HashCodeProvider()`
  （IHashCode提供者 get_HashCode提供者（））

---

## CompilationRelaxations（CompilationRelaxations）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## CompilationRelaxationsAttribute（CompilationRelaxationsAttribute）

**继承**: Attribute（Attribute）

### 字段 (1)

- `int m_relaxations`（int m_relaxations）(偏移: 0x8)

### 方法 (1)

- `int get_CompilationRelaxations()`
  （int get_CompilationRelaxations（））

---

## CompletionActionInvoker（Completion动作Invoker）

**继承**: IThreadPoolWorkItem（IThread池Work项目）

### 字段 (2)

- `ITaskCompletionAction m_action`（ITaskCompletion动作 m_action）(偏移: 0x8)
- `Task m_completingTask`（Task m_completingTask）(偏移: 0xC)

### 方法 (2)

- `void ExecuteWorkItem()`
  （void 执行Work项目（））
- `void MarkAborted(ThreadAbortException tae)`
  （void MarkAborted（ThreadAbortException tae））

---

## Component（组件）

**继承**: Object（对象）

### 方法 (14)

- `Transform get_transform()`
  （变换 get_transform（））
- `GameObject get_gameObject()`
  （游戏对象 get_game对象（））
- `Component GetComponent(Type type)`
  （组件 获取组件（类型 type））
- `void GetComponentFastPath(Type type, IntPtr oneFurtherThanResultValue)`
  （void 获取组件Fast路径（类型 type, 整数Ptr oneFurtherThanResultValue））
- `Component GetComponentInChildren(Type t, bool includeInactive)`
  （组件 获取组件InChildren（类型 t, bool includeInactive））
- `Component GetComponentInParent(Type t)`
  （组件 获取组件In父级（类型 t））
- `void GetComponentsForListInternal(Type searchType, object resultList)`
  （void 获取ComponentsFor列表内部的（类型 searchType, object resultList））
- `void GetComponents(Type type, List<Component> results)`
  （void 获取Components（类型 type, List<Component> results））
- `string get_tag()`
  （string get_tag（））
- `bool CompareTag(string tag)`
  （bool Compare标签（string tag））
- `void SendMessage(string methodName, object value)`
  （void 发送Message（string methodName, object value））
- `void SendMessage(string methodName)`
  （void 发送Message（string methodName））
- `void SendMessage(string methodName, object value, SendMessageOptions options)`
  （void 发送Message（string methodName, object value, 发送MessageOptions options））
- `void SendMessage(string methodName, SendMessageOptions options)`
  （void 发送Message（string methodName, 发送MessageOptions options））

---

## ComponentCollection（组件Collection）

**继承**: ReadOnlyCollectionBase（ReadOnlyCollection基础）

### 方法 (1)

- `IComponent get_Item(string name)`
  （I组件 get_项目（string name））

---

## ComponentConverter（组件Converter）

**继承**: ReferenceConverter（引用Converter）

### 方法 (2)

- `PropertyDescriptorCollection GetProperties(ITypeDescriptorContext context, object value, Attribute[] attributes)`
  （属性DescriptorCollection 获取Properties（I类型DescriptorContext context, object value, Attribute[] attributes））
- `bool GetPropertiesSupported(ITypeDescriptorContext context)`
  （bool 获取PropertiesSupported（I类型DescriptorContext context））

---

## ComponentData（组件数据）

### 字段 (1)

- `List<ComponentDataBase> list`（List<组件数据Base> list）(偏移: 0x8)

### 方法 (2)

- `void AddComponent_Float()`
  （void 添加Component_浮点数（））
- `void AddComponent_RepeatFire()`
  （void 添加Component_Repeat开火（））

---

## ComponentDataBase（组件数据基础）

### 字段 (1)

- `string name`（string name）(偏移: 0x8)

---

## ComponentUtility（组件工具）

### 方法 (2)

- `bool IsUniversalCamera(Camera camera)`
  （bool 是否Universal摄像机（摄像机 camera））
- `bool IsUniversalLight(Light light)`
  （bool 是否Universal光照（光照 light））

---

## CompositeCollider2D（CompositeCollider2D）

**继承**: Collider2D（Collider2D）

### 方法 (4)

- `int get_pathCount()`
  （int get_path数量（））
- `int get_pointCount()`
  （int get_point数量（））
- `int GetPath(int index, Vector2[] points)`
  （int 获取路径（int index, Vector2[] points））
- `int GetPathArray_Internal(int index, Vector2[] points)`
  （int 获取路径Array_内部的（int index, Vector2[] points））

---

## CompositeShadowCaster2D（CompositeShadowCaster2D）

**继承**: ShadowCasterGroup2D（ShadowCasterGroup2D）

### 方法 (2)

- `void OnEnable()`
  （void On启用（））
- `void OnDisable()`
  （void On禁用（））

---

## CompressionLevel（Compression等级）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## CompressionMethod（CompressionMethod）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## CompressionMode（Compression模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## CompressionStrategy（CompressionStrategy）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ComputeBuffer（Compute缓冲区）

**继承**: IDisposable（IDisposable）

### 字段 (1)

- `IntPtr m_Ptr`（整数Ptr m_Ptr）(偏移: 0x8)

### 方法 (12)

- `void Finalize()`
  （void Finalize（））
- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））
- `IntPtr InitBuffer(int count, int stride, ComputeBufferType type, ComputeBufferMode usage)`
  （整数Ptr 初始化缓冲区（int count, int stride, Compute缓冲区类型 type, Compute缓冲区模式 usage））
- `void DestroyBuffer(ComputeBuffer buf)`
  （void 销毁缓冲区（Compute缓冲区 buf））
- `void Release()`
  （void Release（））
- `int get_count()`
  （int get_count（））
- `int get_stride()`
  （int get_stride（））
- `void InternalSetNativeData(IntPtr data, int nativeBufferStartIndex, int computeBufferStartIndex, int count, int elemSize)`
  （void 内部的集合Native数据（整数Ptr data, int nativeBufferStartIndex, int computeBufferStartIndex, int count, int elemSize））
- `void InternalSetData(Array data, int managedBufferStartIndex, int computeBufferStartIndex, int count, int elemSize)`
  （void 内部的集合数据（数组 data, int managedBufferStartIndex, int computeBufferStartIndex, int count, int elemSize））
- `void set_name(string value)`
  （void set_name（string value））
- `void SetName(string name)`
  （void 集合名称（string name））

---

## ComputeBufferDesc（Compute缓冲区Desc）

### 字段 (4)

- `int count`（int count）(偏移: 0x0)
- `int stride`（int stride）(偏移: 0x4)
- `ComputeBufferType type`（Compute缓冲区类型 type）(偏移: 0x8)
- `string name`（string name）(偏移: 0xC)

### 方法 (1)

- `int GetHashCode()`
  （int 获取HashCode（））

---

## ComputeBufferHandle（Compute缓冲区句柄）

### 字段 (2)

- `ComputeBufferHandle s_NullHandle`（Compute缓冲区句柄 s_Null句柄）(偏移: 0x0)
- `ResourceHandle handle`（资源句柄 handle）(偏移: 0x0)

### 方法 (3)

- `ComputeBufferHandle get_nullHandle()`
  （Compute缓冲区句柄 get_null句柄（））
- `ComputeBuffer op_Implicit(ComputeBufferHandle buffer)`
  （Compute缓冲区 op_Implicit（Compute缓冲区句柄 buffer））
- `bool IsValid()`
  （bool 是否Valid（））

---

## ComputeBufferMode（Compute缓冲区模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ComputeBufferPool（Compute缓冲区池）

**继承**: RenderGraphResourcePool<ComputeBuffer>（RenderGraph资源Pool<ComputeBuffer>）

### 方法 (5)

- `void ReleaseInternalResource(ComputeBuffer res)`
  （void Release内部的资源（Compute缓冲区 res））
- `string GetResourceName(ComputeBuffer res)`
  （string 获取资源名称（Compute缓冲区 res））
- `long GetResourceSize(ComputeBuffer res)`
  （long 获取资源大小（Compute缓冲区 res））
- `string GetResourceTypeName()`
  （string 获取资源类型名称（））
- `void PurgeUnusedResources(int currentFrameIndex)`
  （void PurgeUnusedResources（int currentFrameIndex））

---

## ComputeBufferType（Compute缓冲区类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ComputeQueueType（Compute队列类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ComputeShader（Compute着色器）

**继承**: Object（对象）

### 方法 (3)

- `int FindKernel(string name)`
  （int 查找Kernel（string name））
- `void EnableKeyword(string keyword)`
  （void 启用Keyword（string keyword））
- `void DisableKeyword(string keyword)`
  （void 禁用Keyword（string keyword））

---

## ConditionalAttribute（ConditionalAttribute）

**继承**: Attribute（Attribute）

### 字段 (1)

- `string m_conditionString`（string m_condition字符串）(偏移: 0x8)

---

## ConfidenceFactor（Confidence系数）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ConfidenceLevel（Confidence等级）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ConfigHandler（配置处理器）

**继承**: SmallXmlParser.IContentHandler（SmallXmlParser.IContent处理器）

### 字段 (8)

- `ArrayList typeEntries`（数组列表 typeEntries）(偏移: 0x8)
- `ArrayList channelInstances`（数组列表 channelInstances）(偏移: 0xC)
- `ChannelData currentChannel`（Channel数据 currentChannel）(偏移: 0x10)
- `Stack currentProviderData`（栈 current提供者数据）(偏移: 0x14)
- `string currentClientUrl`（string current客户端Url）(偏移: 0x18)
- `string appName`（string app名称）(偏移: 0x1C)
- `string currentXmlPath`（string currentXml路径）(偏移: 0x20)
- `bool onlyDelayedChannels`（bool onlyDelayedChannels）(偏移: 0x24)

### 方法 (23)

- `void ValidatePath(string element, string[] paths)`
  （void 验证路径（string element, string[] paths））
- `bool CheckPath(string path)`
  （bool 检查路径（string path））
- `void OnStartParsing(SmallXmlParser parser)`
  （void On开始Parsing（SmallXmlParser parser））
- `void OnProcessingInstruction(string name, string text)`
  （void OnProcessingInstruction（string name, string text））
- `void OnIgnorableWhitespace(string s)`
  （void OnIgnorableWhitespace（string s））
- `void OnStartElement(string name, SmallXmlParser.IAttrList attrs)`
  （void On开始元素（string name, SmallXmlParser.IAttr列表 attrs））
- `void ParseElement(string name, SmallXmlParser.IAttrList attrs)`
  （void 解析元素（string name, SmallXmlParser.IAttr列表 attrs））
- `void OnEndElement(string name)`
  （void On结束元素（string name））
- `void ReadCustomProviderData(string name, SmallXmlParser.IAttrList attrs)`
  （void Read自定义的提供者数据（string name, SmallXmlParser.IAttr列表 attrs））
- `void ReadLifetine(SmallXmlParser.IAttrList attrs)`
  （void ReadLifetine（SmallXmlParser.IAttr列表 attrs））
- `TimeSpan ParseTime(string s)`
  （时间Span 解析时间（string s））
- `void ReadChannel(SmallXmlParser.IAttrList attrs, bool isTemplate)`
  （void ReadChannel（SmallXmlParser.IAttr列表 attrs, bool isTemplate））
- `ProviderData ReadProvider(string name, SmallXmlParser.IAttrList attrs, bool isTemplate)`
  （提供者数据 Read提供者（string name, SmallXmlParser.IAttr列表 attrs, bool isTemplate））
- `void ReadClientActivated(SmallXmlParser.IAttrList attrs)`
  （void Read客户端Activated（SmallXmlParser.IAttr列表 attrs））
- `void ReadServiceActivated(SmallXmlParser.IAttrList attrs)`
  （void Read服务Activated（SmallXmlParser.IAttr列表 attrs））
- `void ReadClientWellKnown(SmallXmlParser.IAttrList attrs)`
  （void Read客户端WellKnown（SmallXmlParser.IAttr列表 attrs））
- `void ReadServiceWellKnown(SmallXmlParser.IAttrList attrs)`
  （void Read服务WellKnown（SmallXmlParser.IAttr列表 attrs））
- `void ReadInteropXml(SmallXmlParser.IAttrList attrs, bool isElement)`
  （void ReadInteropXml（SmallXmlParser.IAttr列表 attrs, bool isElement））
- `void ReadPreload(SmallXmlParser.IAttrList attrs)`
  （void ReadPreload（SmallXmlParser.IAttr列表 attrs））
- `string GetNotNull(SmallXmlParser.IAttrList attrs, string name)`
  （string 获取NotNull（SmallXmlParser.IAttr列表 attrs, string name））
- `string ExtractAssembly(ref string type)`
  （string ExtractAssembly（ref string type））
- `void OnChars(string ch)`
  （void OnChars（string ch））
- `void OnEndParsing(SmallXmlParser parser)`
  （void On结束Parsing（SmallXmlParser parser））

---

## ConfigurationElement（Configuration元素）

### 方法 (4)

- `ConfigurationPropertyCollection get_Properties()`
  （Configuration属性Collection get_Properties（））
- `bool IsModified()`
  （bool 是否Modified（））
- `void Reset(ConfigurationElement parentElement)`
  （void 重置（Configuration元素 parentElement））
- `void ResetModified()`
  （void 重置Modified（））

---

## ConfigurationElementCollection（Configuration元素Collection）

**继承**: ConfigurationElement（Configuration元素）

### 方法 (1)

- `int get_Count()`
  （int get_数量（））

---

## ConfigurationSaveMode（Configuration保存模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ConfigurationSection（ConfigurationSection）

**继承**: ConfigurationElement（Configuration元素）

### 方法 (4)

- `void DeserializeSection(XmlReader reader)`
  （void DeserializeSection（Xml读取器 reader））
- `bool IsModified()`
  （bool 是否Modified（））
- `void ResetModified()`
  （void 重置Modified（））
- `string SerializeSection(ConfigurationElement parentElement, string name, ConfigurationSaveMode saveMode)`
  （string SerializeSection（Configuration元素 parentElement, string name, Configuration保存模式 saveMode））

---

## Connection（连接）

### 字段 (3)

- `GraphNode node`（Graph节点 node）(偏移: 0x0)
- `uint cost`（uint cost）(偏移: 0x4)
- `byte shapeEdge`（byte shapeEdge）(偏移: 0x8)

### 方法 (2)

- `int GetHashCode()`
  （int 获取HashCode（））
- `bool Equals(object obj)`
  （bool Equals（object obj））

---

## ConnectionChangeType（连接Change类型）

### 字段 (1)

- `uint value__`（uint value__）(偏移: 0x0)

---

## ConnectionManagementSection（连接ManagementSection）

**继承**: ConfigurationSection（ConfigurationSection）

### 方法 (1)

- `ConfigurationPropertyCollection get_Properties()`
  （Configuration属性Collection get_Properties（））

---

## Consistency（Consistency）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Console（Console）

### 字段 (7)

- `TextWriter stdout`（文本写入器 stdout）(偏移: 0x0)
- `TextWriter stderr`（文本写入器 stderr）(偏移: 0x4)
- `TextReader stdin`（文本读取器 stdin）(偏移: 0x8)
- `Encoding inputEncoding`（Encoding inputEncoding）(偏移: 0xC)
- `Encoding outputEncoding`（Encoding outputEncoding）(偏移: 0x10)
- `ConsoleCancelEventHandler cancel_event`（Console取消事件处理器 cancel_event）(偏移: 0x14)
- `Console.InternalCancelHandler cancel_handler`（Console.内部的取消处理器 cancel_handler）(偏移: 0x18)

### 方法 (13)

- `void SetupStreams(Encoding inputEncoding, Encoding outputEncoding)`
  （void SetupStreams（Encoding inputEncoding, Encoding outputEncoding））
- `TextWriter get_Error()`
  （文本写入器 get_Error（））
- `Stream Open(IntPtr handle, FileAccess access, int bufferSize)`
  （流 打开（整数Ptr handle, 文件Access access, int bufferSize））
- `Stream OpenStandardError(int bufferSize)`
  （流 打开StandardError（int bufferSize））
- `Stream OpenStandardInput(int bufferSize)`
  （流 打开Standard输入（int bufferSize））
- `Stream OpenStandardOutput(int bufferSize)`
  （流 打开StandardOutput（int bufferSize））
- `void SetOut(TextWriter newOut)`
  （void 集合Out（文本写入器 newOut））
- `void WriteLine(string value)`
  （void WriteLine（string value））
- `Encoding get_InputEncoding()`
  （Encoding get_输入Encoding（））
- `Encoding get_OutputEncoding()`
  （Encoding get_OutputEncoding（））
- `ConsoleKeyInfo ReadKey()`
  （Console键信息 Read键（））
- `ConsoleKeyInfo ReadKey(bool intercept)`
  （Console键信息 Read键（bool intercept））
- `void DoConsoleCancelEvent()`
  （void DoConsole取消事件（））

---

## Console.InternalCancelHandler（Console.内部的取消处理器）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke()`
  （void Invoke（））
- `IAsyncResult BeginInvoke(AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## Console.WindowsConsole（Console.WindowsConsole）

### 字段 (2)

- `bool ctrlHandlerAdded`（bool ctrl处理器Added）(偏移: 0x0)
- `Console.WindowsConsole.WindowsCancelHandler cancelHandler`（Console.WindowsConsole.Windows取消处理器 cancel处理器）(偏移: 0x4)

### 方法 (5)

- `int GetConsoleCP()`
  （int 获取ConsoleCP（））
- `int GetConsoleOutputCP()`
  （int 获取ConsoleOutputCP（））
- `bool DoWindowsConsoleCancelEvent(int keyCode)`
  （bool DoWindowsConsole取消事件（int keyCode））
- `int GetInputCodePage()`
  （int 获取输入CodePage（））
- `int GetOutputCodePage()`
  （int 获取OutputCodePage（））

---

## Console.WindowsConsole.WindowsCancelHandler（Console.WindowsConsole.Windows取消处理器）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `bool Invoke(int keyCode)`
  （bool Invoke（int keyCode））
- `IAsyncResult BeginInvoke(int keyCode, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（int keyCode, 异步回调 callback, object object））
- `bool EndInvoke(IAsyncResult result)`
  （bool 结束Invoke（I异步Result result））

---

## ConsoleCancelEventArgs（Console取消事件Args）

**继承**: EventArgs（事件Args）

### 字段 (2)

- `ConsoleSpecialKey _type`（Console特殊键 _type）(偏移: 0x8)
- `bool _cancel`（bool _cancel）(偏移: 0xC)

### 方法 (1)

- `bool get_Cancel()`
  （bool get_取消（））

---

## ConsoleCancelEventHandler（Console取消事件处理器）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(object sender, ConsoleCancelEventArgs e)`
  （void Invoke（object sender, Console取消事件Args e））
- `IAsyncResult BeginInvoke(object sender, ConsoleCancelEventArgs e, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（object sender, Console取消事件Args e, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## ConsoleColor（Console颜色）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ConsoleDriver（ConsoleDriver）

### 字段 (3)

- `IConsoleDriver driver`（IConsoleDriver driver）(偏移: 0x0)
- `bool is_console`（bool is_console）(偏移: 0x4)
- `bool called_isatty`（bool called_isatty）(偏移: 0x5)

### 方法 (9)

- `IConsoleDriver CreateNullConsoleDriver()`
  （IConsoleDriver 创建NullConsoleDriver（））
- `IConsoleDriver CreateWindowsConsoleDriver()`
  （IConsoleDriver 创建WindowsConsoleDriver（））
- `IConsoleDriver CreateTermInfoDriver(string term)`
  （IConsoleDriver 创建Term信息Driver（string term））
- `ConsoleKeyInfo ReadKey(bool intercept)`
  （Console键信息 Read键（bool intercept））
- `bool get_IsConsole()`
  （bool get_是否Console（））
- `bool Isatty(IntPtr handle)`
  （bool Isatty（整数Ptr handle））
- `int InternalKeyAvailable(int ms_timeout)`
  （int 内部的键Available（int ms_timeout））
- `bool TtySetup(string keypadXmit, string teardown, out byte[] control_characters, out int* address)`
  （bool TtySetup（string keypadXmit, string teardown, out byte[] control_characters, out int* address））
- `bool SetEcho(bool wantEcho)`
  （bool 集合Echo（bool wantEcho））

---

## ConsoleKey（Console键）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ConsoleKeyInfo（Console键信息）

### 字段 (3)

- `char _keyChar`（char _keyChar）(偏移: 0x0)
- `ConsoleKey _key`（Console键 _key）(偏移: 0x4)
- `ConsoleModifiers _mods`（ConsoleModifiers _mods）(偏移: 0x8)

### 方法 (5)

- `char get_KeyChar()`
  （char get_键Char（））
- `ConsoleKey get_Key()`
  （Console键 get_键（））
- `bool Equals(object value)`
  （bool Equals（object value））
- `bool Equals(ConsoleKeyInfo obj)`
  （bool Equals（Console键信息 obj））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## ConsoleModifiers（ConsoleModifiers）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ConsoleScreenBufferInfo（Console屏幕的缓冲区信息）

### 字段 (5)

- `Coord Size`（Coord 大小）(偏移: 0x0)
- `Coord CursorPosition`（Coord CursorPosition）(偏移: 0x4)
- `short Attribute`（short Attribute）(偏移: 0x8)
- `SmallRect Window`（SmallRect Window）(偏移: 0xA)
- `Coord MaxWindowSize`（Coord 最大Window大小）(偏移: 0x12)

---

## ConsoleSpecialKey（Console特殊键）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ConstantBuffer（Constant缓冲区）

### 字段 (1)

- `List<ConstantBufferBase> m_RegisteredConstantBuffers`（List<Constant缓冲区Base> m_RegisteredConstantBuffers）(偏移: 0x30903050)

### 方法 (2)

- `void ReleaseAll()`
  （void Release所有（））
- `void Register(ConstantBufferBase cb)`
  （void Register（Constant缓冲区基础 cb））

---

## ConstantPath（Constant路径）

**继承**: Path（路径）

### 字段 (5)

- `GraphNode startNode`（Graph节点 start节点）(偏移: 0x78)
- `Vector3 startPoint`（三维向量 startPoint）(偏移: 0x7C)
- `Vector3 originalStartPoint`（三维向量 original开始Point）(偏移: 0x88)
- `List<GraphNode> allNodes`（List<GraphNode> allNodes）(偏移: 0x94)
- `PathEndingCondition endingCondition`（路径EndingCondition endingCondition）(偏移: 0x98)

### 方法 (9)

- `bool get_FloodingPath()`
  （bool get_Flooding路径（））
- `ConstantPath Construct(Vector3 start, int maxGScore, OnPathDelegate callback)`
  （Constant路径 Construct（三维向量 start, int maxGScore, On路径委托 callback））
- `void Setup(Vector3 start, int maxGScore, OnPathDelegate callback)`
  （void Setup（三维向量 start, int maxGScore, On路径委托 callback））
- `void OnEnterPool()`
  （void OnEnter池（））
- `void Reset()`
  （void 重置（））
- `void Prepare()`
  （void Prepare（））
- `void Initialize()`
  （void 初始化（））
- `void Cleanup()`
  （void 清理（））
- `void CalculateStep(long targetTick)`
  （void 计算Step（long targetTick））

---

## Constraint（Constraint）

### 字段 (2)

- `Transform transform`（变换 transform）(偏移: 0x8)
- `float weight`（float weight）(偏移: 0xC)

### 方法 (1)

- `bool get_isValid()`
  （bool get_isValid（））

---

## ConstraintPosition（ConstraintPosition）

**继承**: Constraint（Constraint）

### 字段 (1)

- `Vector3 position`（三维向量 position）(偏移: 0x10)

### 方法 (1)

- `void UpdateConstraint()`
  （void 更新Constraint（））

---

## ConstraintPositionOffset（ConstraintPositionOffset）

**继承**: Constraint（Constraint）

### 字段 (4)

- `Vector3 offset`（三维向量 offset）(偏移: 0x10)
- `Vector3 defaultLocalPosition`（三维向量 default本地的Position）(偏移: 0x1C)
- `Vector3 lastLocalPosition`（三维向量 last本地的Position）(偏移: 0x28)
- `bool initiated`（bool initiated）(偏移: 0x34)

### 方法 (2)

- `void UpdateConstraint()`
  （void 更新Constraint（））
- `bool get_positionChanged()`
  （bool get_positionChanged（））

---

## ConstraintRotation（ConstraintRotation）

**继承**: Constraint（Constraint）

### 字段 (1)

- `Quaternion rotation`（Quaternion rotation）(偏移: 0x10)

### 方法 (1)

- `void UpdateConstraint()`
  （void 更新Constraint（））

---

## ConstraintRotationOffset（ConstraintRotationOffset）

**继承**: Constraint（Constraint）

### 字段 (6)

- `Quaternion offset`（Quaternion offset）(偏移: 0x10)
- `Quaternion defaultRotation`（Quaternion defaultRotation）(偏移: 0x20)
- `Quaternion defaultLocalRotation`（Quaternion default本地的Rotation）(偏移: 0x30)
- `Quaternion lastLocalRotation`（Quaternion last本地的Rotation）(偏移: 0x40)
- `Quaternion defaultTargetLocalRotation`（Quaternion default目标本地的Rotation）(偏移: 0x50)
- `bool initiated`（bool initiated）(偏移: 0x60)

### 方法 (2)

- `void UpdateConstraint()`
  （void 更新Constraint（））
- `bool get_rotationChanged()`
  （bool get_rotationChanged（））

---

## Constraints（Constraints）

### 字段 (8)

- `Transform transform`（变换 transform）(偏移: 0x8)
- `Transform target`（变换 target）(偏移: 0xC)
- `Vector3 positionOffset`（三维向量 positionOffset）(偏移: 0x10)
- `Vector3 position`（三维向量 position）(偏移: 0x1C)
- `float positionWeight`（float positionWeight）(偏移: 0x28)
- `Vector3 rotationOffset`（三维向量 rotationOffset）(偏移: 0x2C)
- `Vector3 rotation`（三维向量 rotation）(偏移: 0x38)
- `float rotationWeight`（float rotationWeight）(偏移: 0x44)

### 方法 (3)

- `bool IsValid()`
  （bool 是否Valid（））
- `void Initiate(Transform transform)`
  （void Initiate（变换 transform））
- `void Update()`
  （void 更新（））

---

## ConstructionCall（ConstructionCall）

**继承**: MethodCall, IConstructionCallMessage, IMessage, IMethodCallMessage, IMethodMessage（MethodCall, IConstructionCallMessage, IMessage, IMethodCallMessage, IMethodMessage）

### 字段 (7)

- `IActivator _activator`（IActivator _activator）(偏移: 0x34)
- `object[] _activationAttributes`（object[] _activationAttributes）(偏移: 0x38)
- `IList _contextProperties`（I列表 _contextProperties）(偏移: 0x3C)
- `Type _activationType`（类型 _activation类型）(偏移: 0x40)
- `string _activationTypeName`（string _activation类型名称）(偏移: 0x44)
- `bool _isContextOk`（bool _isContextOk）(偏移: 0x48)
- `RemotingProxy _sourceProxy`（Remoting代理 _source代理）(偏移: 0x4C)

### 方法 (15)

- `void InitDictionary()`
  （void 初始化字典（））
- `bool get_IsContextOk()`
  （bool get_是否ContextOk（））
- `void set_IsContextOk(bool value)`
  （void set_是否ContextOk（bool value））
- `Type get_ActivationType()`
  （类型 get_Activation类型（））
- `string get_ActivationTypeName()`
  （string get_Activation类型名称（））
- `IActivator get_Activator()`
  （IActivator get_Activator（））
- `void set_Activator(IActivator value)`
  （void set_Activator（IActivator value））
- `object[] get_CallSiteActivationAttributes()`
  （object[] get_CallSiteActivationAttributes（））
- `void SetActivationAttributes(object[] attributes)`
  （void 集合ActivationAttributes（object[] attributes））
- `IList get_ContextProperties()`
  （I列表 get_ContextProperties（））
- `void InitMethodProperty(string key, object value)`
  （void 初始化Method属性（string key, object value））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））
- `IDictionary get_Properties()`
  （I字典 get_Properties（））
- `RemotingProxy get_SourceProxy()`
  （Remoting代理 get_Source代理（））
- `void set_SourceProxy(RemotingProxy value)`
  （void set_Source代理（Remoting代理 value））

---

## ConstructionCallDictionary（ConstructionCall字典）

**继承**: MessageDictionary（Message字典）

### 字段 (1)

- `string[] InternalKeys`（string[] 内部的Keys）(偏移: 0x0)

### 方法 (2)

- `object GetMethodProperty(string key)`
  （object 获取Method属性（string key））
- `void SetMethodProperty(string key, object value)`
  （void 集合Method属性（string key, object value））

---

## ConstructionLevelActivator（Construction等级Activator）

**继承**: IActivator（IActivator）

### 方法 (2)

- `IActivator get_NextActivator()`
  （IActivator get_下一个Activator（））
- `IConstructionReturnMessage Activate(IConstructionCallMessage msg)`
  （IConstructionReturnMessage 激活（IConstructionCallMessage msg））

---

## ConstructionResponse（Construction响应）

**继承**: MethodResponse, IConstructionReturnMessage, IMethodReturnMessage, IMethodMessage, IMessage（Method响应, IConstructionReturnMessage, IMethodReturnMessage, IMethodMessage, IMessage）

### 方法 (1)

- `IDictionary get_Properties()`
  （I字典 get_Properties（））

---

## ConstructorBuilder（Constructor构建器）

**继承**: ConstructorInfo（Constructor信息）

### 方法 (12)

- `MethodAttributes get_Attributes()`
  （MethodAttributes get_Attributes（））
- `Type get_DeclaringType()`
  （类型 get_Declaring类型（））
- `string get_Name()`
  （string get_名称（））
- `ParameterInfo[] GetParameters()`
  （ParameterInfo[] 获取Parameters（））
- `RuntimeMethodHandle get_MethodHandle()`
  （RuntimeMethod句柄 get_Method句柄（））
- `Type get_ReflectedType()`
  （类型 get_Reflected类型（））
- `object[] GetCustomAttributes(bool inherit)`
  （object[] 获取自定义的Attributes（bool inherit））
- `object[] GetCustomAttributes(Type attributeType, bool inherit)`
  （object[] 获取自定义的Attributes（类型 attributeType, bool inherit））
- `MethodImplAttributes GetMethodImplementationFlags()`
  （MethodImplAttributes 获取MethodImplementationFlags（））
- `object Invoke(object obj, BindingFlags invokeAttr, Binder binder, object[] parameters, CultureInfo culture)`
  （object Invoke（object obj, BindingFlags invokeAttr, Binder binder, object[] parameters, Culture信息 culture））
- `object Invoke(BindingFlags invokeAttr, Binder binder, object[] parameters, CultureInfo culture)`
  （object Invoke（BindingFlags invokeAttr, Binder binder, object[] parameters, Culture信息 culture））
- `bool IsDefined(Type attributeType, bool inherit)`
  （bool 是否Defined（类型 attributeType, bool inherit））

---

## ConstructorInfo（Constructor信息）

**继承**: MethodBase, _ConstructorInfo（Method基础, _Constructor信息）

### 字段 (2)

- `string ConstructorName`（string Constructor名称）(偏移: 0x0)
- `string TypeConstructorName`（string 类型Constructor名称）(偏移: 0x4)

### 方法 (6)

- `MemberTypes get_MemberType()`
  （MemberTypes get_Member类型（））
- `object Invoke(object[] parameters)`
  （object Invoke（object[] parameters））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool op_Equality(ConstructorInfo left, ConstructorInfo right)`
  （bool op_Equality（Constructor信息 left, Constructor信息 right））
- `bool op_Inequality(ConstructorInfo left, ConstructorInfo right)`
  （bool op_Inequality（Constructor信息 left, Constructor信息 right））

---

## ContactFilter2D（ContactFilter2D）

### 字段 (11)

- `bool useTriggers`（bool useTriggers）(偏移: 0x0)
- `bool useLayerMask`（bool use层掩码）(偏移: 0x1)
- `bool useDepth`（bool use深度）(偏移: 0x2)
- `bool useOutsideDepth`（bool useOutside深度）(偏移: 0x3)
- `bool useNormalAngle`（bool use法线角度）(偏移: 0x4)
- `bool useOutsideNormalAngle`（bool useOutside法线角度）(偏移: 0x5)
- `LayerMask layerMask`（层掩码 layer掩码）(偏移: 0x8)
- `float minDepth`（float min深度）(偏移: 0xC)
- `float maxDepth`（float max深度）(偏移: 0x10)
- `float minNormalAngle`（float min法线角度）(偏移: 0x14)
- `float maxNormalAngle`（float max法线角度）(偏移: 0x18)

### 方法 (5)

- `void CheckConsistency()`
  （void 检查Consistency（））
- `void SetLayerMask(LayerMask layerMask)`
  （void 集合层掩码（层掩码 layerMask））
- `void SetDepth(float minDepth, float maxDepth)`
  （void 集合深度（float minDepth, float maxDepth））
- `ContactFilter2D CreateLegacyFilter(int layerMask, float minDepth, float maxDepth)`
  （ContactFilter2D 创建LegacyFilter（int layerMask, float minDepth, float maxDepth））
- `void CheckConsistency_Injected(ref ContactFilter2D _unity_self)`
  （void 检查Consistency_Injected（ref ContactFilter2D _unity_self））

---

## ContactPoint（ContactPoint）

### 字段 (5)

- `Vector3 m_Point`（三维向量 m_Point）(偏移: 0x0)
- `Vector3 m_Normal`（三维向量 m_法线）(偏移: 0xC)
- `int m_ThisColliderInstanceID`（int m_This碰撞器实例ID）(偏移: 0x18)
- `int m_OtherColliderInstanceID`（int m_Other碰撞器实例ID）(偏移: 0x1C)
- `float m_Separation`（float m_Separation）(偏移: 0x20)

### 方法 (2)

- `Vector3 get_point()`
  （三维向量 get_point（））
- `Vector3 get_normal()`
  （三维向量 get_normal（））

---

## ContactPoint2D（ContactPoint2D）

### 字段 (11)

- `Vector2 m_Point`（二维向量 m_Point）(偏移: 0x0)
- `Vector2 m_Normal`（二维向量 m_法线）(偏移: 0x8)
- `Vector2 m_RelativeVelocity`（二维向量 m_Relative速度）(偏移: 0x10)
- `float m_Separation`（float m_Separation）(偏移: 0x18)
- `float m_NormalImpulse`（float m_法线Impulse）(偏移: 0x1C)
- `float m_TangentImpulse`（float m_TangentImpulse）(偏移: 0x20)
- `int m_Collider`（int m_碰撞器）(偏移: 0x24)
- `int m_OtherCollider`（int m_Other碰撞器）(偏移: 0x28)
- `int m_Rigidbody`（int m_刚体）(偏移: 0x2C)
- `int m_OtherRigidbody`（int m_Other刚体）(偏移: 0x30)
- `int m_Enabled`（int m_启用的）(偏移: 0x34)

---

## ContentSizeFitter（Content大小Fitter）

**继承**: UIBehaviour, ILayoutSelfController, ILayoutController（界面Behaviour, ILayoutSelf控制器, ILayout控制器）

### 字段 (4)

- `ContentSizeFitter.FitMode m_HorizontalFit`（Content大小Fitter.Fit模式 m_水平Fit）(偏移: 0xC)
- `ContentSizeFitter.FitMode m_VerticalFit`（Content大小Fitter.Fit模式 m_垂直Fit）(偏移: 0x10)
- `RectTransform m_Rect`（Rect变换 m_Rect）(偏移: 0x14)
- `DrivenRectTransformTracker m_Tracker`（DrivenRect变换Tracker m_Tracker）(偏移: 0x18)

### 方法 (12)

- `ContentSizeFitter.FitMode get_horizontalFit()`
  （Content大小Fitter.Fit模式 get_horizontalFit（））
- `void set_horizontalFit(ContentSizeFitter.FitMode value)`
  （void set_horizontalFit（Content大小Fitter.Fit模式 value））
- `ContentSizeFitter.FitMode get_verticalFit()`
  （Content大小Fitter.Fit模式 get_verticalFit（））
- `void set_verticalFit(ContentSizeFitter.FitMode value)`
  （void set_verticalFit（Content大小Fitter.Fit模式 value））
- `RectTransform get_rectTransform()`
  （Rect变换 get_rect变换（））
- `void OnEnable()`
  （void On启用（））
- `void OnDisable()`
  （void On禁用（））
- `void OnRectTransformDimensionsChange()`
  （void OnRect变换DimensionsChange（））
- `void HandleSelfFittingAlongAxis(int axis)`
  （void 句柄SelfFittingAlong轴（int axis））
- `void SetLayoutHorizontal()`
  （void 集合Layout水平（））
- `void SetLayoutVertical()`
  （void 集合Layout垂直（））
- `void SetDirty()`
  （void 集合Dirty（））

---

## ContentSizeFitter.FitMode（Content大小Fitter.Fit模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Context（Context）

### 字段 (15)

- `int domain_id`（int domain_id）(偏移: 0x8)
- `int context_id`（int context_id）(偏移: 0xC)
- `UIntPtr static_data`（U整数Ptr static_data）(偏移: 0x10)
- `UIntPtr data`（U整数Ptr data）(偏移: 0x14)
- `object[] local_slots`（object[] local_slots）(偏移: 0x0)
- `IMessageSink default_server_context_sink`（IMessageSink default_server_context_sink）(偏移: 0x4)
- `IMessageSink server_context_sink_chain`（IMessageSink server_context_sink_chain）(偏移: 0x18)
- `IMessageSink client_context_sink_chain`（IMessageSink client_context_sink_chain）(偏移: 0x1C)
- `List<IContextProperty> context_properties`（List<IContextProperty> context_properties）(偏移: 0x20)
- `int global_count`（int global_count）(偏移: 0x8)
- `LocalDataStoreHolder _localDataStore`（本地的数据商店Holder _local数据商店）(偏移: 0x24)
- `LocalDataStoreMgr _localDataStoreMgr`（本地的数据商店Mgr _local数据商店Mgr）(偏移: 0xC)
- `DynamicPropertyCollection global_dynamic_properties`（动态的属性Collection global_dynamic_properties）(偏移: 0x10)
- `DynamicPropertyCollection context_dynamic_properties`（动态的属性Collection context_dynamic_properties）(偏移: 0x28)
- `ContextCallbackObject callback_object`（Context回调对象 callback_object）(偏移: 0x2C)

### 方法 (34)

- `void RegisterContext(Context ctx)`
  （void RegisterContext（Context ctx））
- `void ReleaseContext(Context ctx)`
  （void ReleaseContext（Context ctx））
- `void Finalize()`
  （void Finalize（））
- `Context get_DefaultContext()`
  （Context get_默认的Context（））
- `int get_ContextID()`
  （int get_ContextID（））
- `IContextProperty[] get_ContextProperties()`
  （IContextProperty[] get_ContextProperties（））
- `bool get_IsDefaultContext()`
  （bool get_是否默认的Context（））
- `bool get_NeedsContextSink()`
  （bool get_NeedsContextSink（））
- `bool RegisterDynamicProperty(IDynamicProperty prop, ContextBoundObject obj, Context ctx)`
  （bool Register动态的属性（I动态的属性 prop, ContextBound对象 obj, Context ctx））
- `bool UnregisterDynamicProperty(string name, ContextBoundObject obj, Context ctx)`
  （bool Unregister动态的属性（string name, ContextBound对象 obj, Context ctx））
- `DynamicPropertyCollection GetDynamicPropertyCollection(ContextBoundObject obj, Context ctx)`
  （动态的属性Collection 获取动态的属性Collection（ContextBound对象 obj, Context ctx））
- `void NotifyGlobalDynamicSinks(bool start, IMessage req_msg, bool client_site, bool async)`
  （void Notify全局的动态的Sinks（bool start, IMessage req_msg, bool client_site, bool async））
- `bool get_HasGlobalDynamicSinks()`
  （bool get_是否有全局的动态的Sinks（））
- `void NotifyDynamicSinks(bool start, IMessage req_msg, bool client_site, bool async)`
  （void Notify动态的Sinks（bool start, IMessage req_msg, bool client_site, bool async））
- `bool get_HasDynamicSinks()`
  （bool get_是否有动态的Sinks（））
- `bool get_HasExitSinks()`
  （bool get_是否有ExitSinks（））
- `IContextProperty GetProperty(string name)`
  （IContext属性 获取属性（string name））
- `void SetProperty(IContextProperty prop)`
  （void 集合属性（IContext属性 prop））
- `void Freeze()`
  （void Freeze（））
- `string ToString()`
  （string To字符串（））
- `IMessageSink GetServerContextSinkChain()`
  （IMessageSink 获取服务器ContextSinkChain（））
- `IMessageSink GetClientContextSinkChain()`
  （IMessageSink 获取客户端ContextSinkChain（））
- `IMessageSink CreateServerObjectSinkChain(MarshalByRefObject obj, bool forceInternalExecute)`
  （IMessageSink 创建服务器对象SinkChain（MarshalByRef对象 obj, bool forceInternalExecute））
- `IMessageSink CreateEnvoySink(MarshalByRefObject serverObject)`
  （IMessageSink 创建EnvoySink（MarshalByRef对象 serverObject））
- `Context SwitchToContext(Context newContext)`
  （Context SwitchToContext（Context newContext））
- `Context CreateNewContext(IConstructionCallMessage msg)`
  （Context 创建新的Context（IConstructionCallMessage msg））
- `void DoCallBack(CrossContextDelegate deleg)`
  （void DoCall后（CrossContext委托 deleg））
- `LocalDataStore get_MyLocalStore()`
  （本地的数据商店 get_My本地的商店（））
- `LocalDataStoreSlot AllocateDataSlot()`
  （本地的数据商店槽位 Allocate数据槽位（））
- `LocalDataStoreSlot AllocateNamedDataSlot(string name)`
  （本地的数据商店槽位 AllocateNamed数据槽位（string name））
- `void FreeNamedDataSlot(string name)`
  （void FreeNamed数据槽位（string name））
- `LocalDataStoreSlot GetNamedDataSlot(string name)`
  （本地的数据商店槽位 获取Named数据槽位（string name））
- `object GetData(LocalDataStoreSlot slot)`
  （object 获取数据（本地的数据商店槽位 slot））
- `void SetData(LocalDataStoreSlot slot, object data)`
  （void 集合数据（本地的数据商店槽位 slot, object data））

---

## ContextCallback（Context回调）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(object state)`
  （void Invoke（object state））
- `IAsyncResult BeginInvoke(object state, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（object state, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## ContextCallbackObject（Context回调对象）

**继承**: ContextBoundObject（ContextBound对象）

### 方法 (1)

- `void DoCallBack(CrossContextDelegate deleg)`
  （void DoCall后（CrossContext委托 deleg））

---

## ContextLevelActivator（Context等级Activator）

**继承**: IActivator（IActivator）

### 字段 (1)

- `IActivator m_NextActivator`（IActivator m_下一个Activator）(偏移: 0x8)

### 方法 (2)

- `IActivator get_NextActivator()`
  （IActivator get_下一个Activator（））
- `IConstructionReturnMessage Activate(IConstructionCallMessage ctorCall)`
  （IConstructionReturnMessage 激活（IConstructionCallMessage ctorCall））

---

## ContextMenu（Context菜单）

**继承**: Attribute（Attribute）

### 字段 (3)

- `string menuItem`（string menu项目）(偏移: 0x8)
- `bool validate`（bool validate）(偏移: 0xC)
- `int priority`（int priority）(偏移: 0x10)

---

## ContextMenuItemAttribute（Context菜单项目Attribute）

**继承**: PropertyAttribute（属性Attribute）

### 字段 (2)

- `string name`（string name）(偏移: 0x8)
- `string function`（string function）(偏移: 0xC)

---

## ContinuationTaskFromTask（ContinuationTaskFromTask）

**继承**: Task（Task）

### 字段 (1)

- `Task m_antecedent`（Task m_antecedent）(偏移: 0x28)

### 方法 (1)

- `void InnerInvoke()`
  （void InnerInvoke（））

---

## ContourOrientation（ContourOrientation）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ContourVertex（ContourVertex）

### 字段 (2)

- `Vec3 Position`（Vec3 Position）(偏移: 0x0)
- `object Data`（object 数据）(偏移: 0xC)

### 方法 (1)

- `string ToString()`
  （string To字符串（））

---

## Contraction（Contraction）

### 字段 (4)

- `int Index`（int 索引）(偏移: 0x8)
- `char[] Source`（char[] Source）(偏移: 0xC)
- `string Replacement`（string Replacement）(偏移: 0x10)
- `byte[] SortKey`（byte[] Sort键）(偏移: 0x14)

---

## ContractionComparer（ContractionComparer）

**继承**: IComparer<Contraction>（IComparer<Contraction>）

### 字段 (1)

- `ContractionComparer Instance`（ContractionComparer 实例）(偏移: 0x0)

### 方法 (1)

- `int Compare(Contraction c1, Contraction c2)`
  （int Compare（Contraction c1, Contraction c2））

---

## ControlPoint（控制Point）

### 字段 (2)

- `Vector3 a`（三维向量 a）(偏移: 0x0)
- `Vector3 b`（三维向量 b）(偏移: 0xC)

### 方法 (2)

- `ControlPoint op_Addition(ControlPoint cp, Vector3 v)`
  （控制Point op_Addition（控制Point cp, 三维向量 v））
- `string ToString()`
  （string To字符串（））

---

## ControllerColliderHit（控制器碰撞器命中）

### 字段 (7)

- `CharacterController m_Controller`（角色控制器 m_控制器）(偏移: 0x8)
- `Collider m_Collider`（碰撞器 m_碰撞器）(偏移: 0xC)
- `Vector3 m_Point`（三维向量 m_Point）(偏移: 0x10)
- `Vector3 m_Normal`（三维向量 m_法线）(偏移: 0x1C)
- `Vector3 m_MoveDirection`（三维向量 m_移动方向）(偏移: 0x28)
- `float m_MoveLength`（float m_移动Length）(偏移: 0x34)
- `int m_Push`（int m_Push）(偏移: 0x38)

---

## ControllerCommand（控制器Command）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Convert（转换）

### 字段 (4)

- `RuntimeType[] ConvertTypes`（RuntimeType[] 转换Types）(偏移: 0x0)
- `RuntimeType EnumType`（Runtime类型 Enum类型）(偏移: 0x4)
- `char[] base64Table`（char[] base64Table）(偏移: 0x8)
- `object DBNull`（object DBNull）(偏移: 0xC)

### 方法 (206)

- `TypeCode GetTypeCode(object value)`
  （类型Code 获取类型Code（object value））
- `object ChangeType(object value, TypeCode typeCode, IFormatProvider provider)`
  （object Change类型（object value, 类型Code typeCode, I格式化提供者 provider））
- `object DefaultToType(IConvertible value, Type targetType, IFormatProvider provider)`
  （object 默认的To类型（IConvertible value, 类型 targetType, I格式化提供者 provider））
- `object ChangeType(object value, Type conversionType, IFormatProvider provider)`
  （object Change类型（object value, 类型 conversionType, I格式化提供者 provider））
- `bool ToBoolean(object value, IFormatProvider provider)`
  （bool ToBoolean（object value, I格式化提供者 provider））
- `bool ToBoolean(sbyte value)`
  （bool ToBoolean（sbyte value））
- `bool ToBoolean(byte value)`
  （bool ToBoolean（byte value））
- `bool ToBoolean(short value)`
  （bool ToBoolean（short value））
- `bool ToBoolean(ushort value)`
  （bool ToBoolean（ushort value））
- `bool ToBoolean(int value)`
  （bool ToBoolean（int value））
- `bool ToBoolean(uint value)`
  （bool ToBoolean（uint value））
- `bool ToBoolean(long value)`
  （bool ToBoolean（long value））
- `bool ToBoolean(ulong value)`
  （bool ToBoolean（ulong value））
- `bool ToBoolean(string value, IFormatProvider provider)`
  （bool ToBoolean（string value, I格式化提供者 provider））
- `bool ToBoolean(float value)`
  （bool ToBoolean（float value））
- `bool ToBoolean(double value)`
  （bool ToBoolean（double value））
- `bool ToBoolean(Decimal value)`
  （bool ToBoolean（Decimal value））
- `char ToChar(object value, IFormatProvider provider)`
  （char ToChar（object value, I格式化提供者 provider））
- `char ToChar(sbyte value)`
  （char ToChar（sbyte value））
- `char ToChar(byte value)`
  （char ToChar（byte value））
- `char ToChar(short value)`
  （char ToChar（short value））
- `char ToChar(ushort value)`
  （char ToChar（ushort value））
- `char ToChar(int value)`
  （char ToChar（int value））
- `char ToChar(uint value)`
  （char ToChar（uint value））
- `char ToChar(long value)`
  （char ToChar（long value））
- `char ToChar(ulong value)`
  （char ToChar（ulong value））
- `char ToChar(string value, IFormatProvider provider)`
  （char ToChar（string value, I格式化提供者 provider））
- `sbyte ToSByte(object value, IFormatProvider provider)`
  （sbyte ToSByte（object value, I格式化提供者 provider））
- `sbyte ToSByte(bool value)`
  （sbyte ToSByte（bool value））
- `sbyte ToSByte(char value)`
  （sbyte ToSByte（char value））
- `sbyte ToSByte(byte value)`
  （sbyte ToSByte（byte value））
- `sbyte ToSByte(short value)`
  （sbyte ToSByte（short value））
- `sbyte ToSByte(ushort value)`
  （sbyte ToSByte（ushort value））
- `sbyte ToSByte(int value)`
  （sbyte ToSByte（int value））
- `sbyte ToSByte(uint value)`
  （sbyte ToSByte（uint value））
- `sbyte ToSByte(long value)`
  （sbyte ToSByte（long value））
- `sbyte ToSByte(ulong value)`
  （sbyte ToSByte（ulong value））
- `sbyte ToSByte(float value)`
  （sbyte ToSByte（float value））
- `sbyte ToSByte(double value)`
  （sbyte ToSByte（double value））
- `sbyte ToSByte(Decimal value)`
  （sbyte ToSByte（Decimal value））
- `sbyte ToSByte(string value, IFormatProvider provider)`
  （sbyte ToSByte（string value, I格式化提供者 provider））
- `byte ToByte(object value, IFormatProvider provider)`
  （byte ToByte（object value, I格式化提供者 provider））
- `byte ToByte(bool value)`
  （byte ToByte（bool value））
- `byte ToByte(char value)`
  （byte ToByte（char value））
- `byte ToByte(sbyte value)`
  （byte ToByte（sbyte value））
- `byte ToByte(short value)`
  （byte ToByte（short value））
- `byte ToByte(ushort value)`
  （byte ToByte（ushort value））
- `byte ToByte(int value)`
  （byte ToByte（int value））
- `byte ToByte(uint value)`
  （byte ToByte（uint value））
- `byte ToByte(long value)`
  （byte ToByte（long value））
- `byte ToByte(ulong value)`
  （byte ToByte（ulong value））
- `byte ToByte(float value)`
  （byte ToByte（float value））
- `byte ToByte(double value)`
  （byte ToByte（double value））
- `byte ToByte(Decimal value)`
  （byte ToByte（Decimal value））
- `byte ToByte(string value)`
  （byte ToByte（string value））
- `byte ToByte(string value, IFormatProvider provider)`
  （byte ToByte（string value, I格式化提供者 provider））
- `short ToInt16(object value, IFormatProvider provider)`
  （short ToInt16（object value, I格式化提供者 provider））
- `short ToInt16(bool value)`
  （short ToInt16（bool value））
- `short ToInt16(char value)`
  （short ToInt16（char value））
- `short ToInt16(sbyte value)`
  （short ToInt16（sbyte value））
- `short ToInt16(byte value)`
  （short ToInt16（byte value））
- `short ToInt16(ushort value)`
  （short ToInt16（ushort value））
- `short ToInt16(int value)`
  （short ToInt16（int value））
- `short ToInt16(uint value)`
  （short ToInt16（uint value））
- `short ToInt16(long value)`
  （short ToInt16（long value））
- `short ToInt16(ulong value)`
  （short ToInt16（ulong value））
- `short ToInt16(float value)`
  （short ToInt16（float value））
- `short ToInt16(double value)`
  （short ToInt16（double value））
- `short ToInt16(Decimal value)`
  （short ToInt16（Decimal value））
- `short ToInt16(string value, IFormatProvider provider)`
  （short ToInt16（string value, I格式化提供者 provider））
- `ushort ToUInt16(object value, IFormatProvider provider)`
  （ushort ToUInt16（object value, I格式化提供者 provider））
- `ushort ToUInt16(bool value)`
  （ushort ToUInt16（bool value））
- `ushort ToUInt16(char value)`
  （ushort ToUInt16（char value））
- `ushort ToUInt16(sbyte value)`
  （ushort ToUInt16（sbyte value））
- `ushort ToUInt16(byte value)`
  （ushort ToUInt16（byte value））
- `ushort ToUInt16(short value)`
  （ushort ToUInt16（short value））
- `ushort ToUInt16(int value)`
  （ushort ToUInt16（int value））
- `ushort ToUInt16(uint value)`
  （ushort ToUInt16（uint value））
- `ushort ToUInt16(long value)`
  （ushort ToUInt16（long value））
- `ushort ToUInt16(ulong value)`
  （ushort ToUInt16（ulong value））
- `ushort ToUInt16(float value)`
  （ushort ToUInt16（float value））
- `ushort ToUInt16(double value)`
  （ushort ToUInt16（double value））
- `ushort ToUInt16(Decimal value)`
  （ushort ToUInt16（Decimal value））
- `ushort ToUInt16(string value, IFormatProvider provider)`
  （ushort ToUInt16（string value, I格式化提供者 provider））
- `int ToInt32(object value)`
  （int ToInt32（object value））
- `int ToInt32(object value, IFormatProvider provider)`
  （int ToInt32（object value, I格式化提供者 provider））
- `int ToInt32(bool value)`
  （int ToInt32（bool value））
- `int ToInt32(char value)`
  （int ToInt32（char value））
- `int ToInt32(byte value)`
  （int ToInt32（byte value））
- `int ToInt32(short value)`
  （int ToInt32（short value））
- `int ToInt32(ushort value)`
  （int ToInt32（ushort value））
- `int ToInt32(uint value)`
  （int ToInt32（uint value））
- `int ToInt32(long value)`
  （int ToInt32（long value））
- `int ToInt32(ulong value)`
  （int ToInt32（ulong value））
- `int ToInt32(float value)`
  （int ToInt32（float value））
- `int ToInt32(double value)`
  （int ToInt32（double value））
- `int ToInt32(Decimal value)`
  （int ToInt32（Decimal value））
- `int ToInt32(string value)`
  （int ToInt32（string value））
- `int ToInt32(string value, IFormatProvider provider)`
  （int ToInt32（string value, I格式化提供者 provider））
- `uint ToUInt32(object value)`
  （uint ToUInt32（object value））
- `uint ToUInt32(object value, IFormatProvider provider)`
  （uint ToUInt32（object value, I格式化提供者 provider））
- `uint ToUInt32(bool value)`
  （uint ToUInt32（bool value））
- `uint ToUInt32(char value)`
  （uint ToUInt32（char value））
- `uint ToUInt32(sbyte value)`
  （uint ToUInt32（sbyte value））
- `uint ToUInt32(byte value)`
  （uint ToUInt32（byte value））
- `uint ToUInt32(short value)`
  （uint ToUInt32（short value））
- `uint ToUInt32(ushort value)`
  （uint ToUInt32（ushort value））
- `uint ToUInt32(int value)`
  （uint ToUInt32（int value））
- `uint ToUInt32(long value)`
  （uint ToUInt32（long value））
- `uint ToUInt32(ulong value)`
  （uint ToUInt32（ulong value））
- `uint ToUInt32(float value)`
  （uint ToUInt32（float value））
- `uint ToUInt32(double value)`
  （uint ToUInt32（double value））
- `uint ToUInt32(Decimal value)`
  （uint ToUInt32（Decimal value））
- `uint ToUInt32(string value, IFormatProvider provider)`
  （uint ToUInt32（string value, I格式化提供者 provider））
- `long ToInt64(object value, IFormatProvider provider)`
  （long ToInt64（object value, I格式化提供者 provider））
- `long ToInt64(bool value)`
  （long ToInt64（bool value））
- `long ToInt64(char value)`
  （long ToInt64（char value））
- `long ToInt64(sbyte value)`
  （long ToInt64（sbyte value））
- `long ToInt64(byte value)`
  （long ToInt64（byte value））
- `long ToInt64(short value)`
  （long ToInt64（short value））
- `long ToInt64(ushort value)`
  （long ToInt64（ushort value））
- `long ToInt64(int value)`
  （long ToInt64（int value））
- `long ToInt64(uint value)`
  （long ToInt64（uint value））
- `long ToInt64(ulong value)`
  （long ToInt64（ulong value））
- `long ToInt64(float value)`
  （long ToInt64（float value））
- `long ToInt64(double value)`
  （long ToInt64（double value））
- `long ToInt64(Decimal value)`
  （long ToInt64（Decimal value））
- `long ToInt64(string value)`
  （long ToInt64（string value））
- `long ToInt64(string value, IFormatProvider provider)`
  （long ToInt64（string value, I格式化提供者 provider））
- `ulong ToUInt64(object value, IFormatProvider provider)`
  （ulong ToUInt64（object value, I格式化提供者 provider））
- `ulong ToUInt64(bool value)`
  （ulong ToUInt64（bool value））
- `ulong ToUInt64(char value)`
  （ulong ToUInt64（char value））
- `ulong ToUInt64(sbyte value)`
  （ulong ToUInt64（sbyte value））
- `ulong ToUInt64(byte value)`
  （ulong ToUInt64（byte value））
- `ulong ToUInt64(short value)`
  （ulong ToUInt64（short value））
- `ulong ToUInt64(ushort value)`
  （ulong ToUInt64（ushort value））
- `ulong ToUInt64(int value)`
  （ulong ToUInt64（int value））
- `ulong ToUInt64(uint value)`
  （ulong ToUInt64（uint value））
- `ulong ToUInt64(long value)`
  （ulong ToUInt64（long value））
- `ulong ToUInt64(float value)`
  （ulong ToUInt64（float value））
- `ulong ToUInt64(double value)`
  （ulong ToUInt64（double value））
- `ulong ToUInt64(Decimal value)`
  （ulong ToUInt64（Decimal value））
- `ulong ToUInt64(string value, IFormatProvider provider)`
  （ulong ToUInt64（string value, I格式化提供者 provider））
- `float ToSingle(object value, IFormatProvider provider)`
  （float To单个（object value, I格式化提供者 provider））
- `float ToSingle(sbyte value)`
  （float To单个（sbyte value））
- `float ToSingle(byte value)`
  （float To单个（byte value））
- `float ToSingle(short value)`
  （float To单个（short value））
- `float ToSingle(ushort value)`
  （float To单个（ushort value））
- `float ToSingle(int value)`
  （float To单个（int value））
- `float ToSingle(uint value)`
  （float To单个（uint value））
- `float ToSingle(long value)`
  （float To单个（long value））
- `float ToSingle(ulong value)`
  （float To单个（ulong value））
- `float ToSingle(double value)`
  （float To单个（double value））
- `float ToSingle(Decimal value)`
  （float To单个（Decimal value））
- `float ToSingle(string value)`
  （float To单个（string value））
- `float ToSingle(string value, IFormatProvider provider)`
  （float To单个（string value, I格式化提供者 provider））
- `float ToSingle(bool value)`
  （float To单个（bool value））
- `double ToDouble(object value, IFormatProvider provider)`
  （double ToDouble（object value, I格式化提供者 provider））
- `double ToDouble(sbyte value)`
  （double ToDouble（sbyte value））
- `double ToDouble(byte value)`
  （double ToDouble（byte value））
- `double ToDouble(short value)`
  （double ToDouble（short value））
- `double ToDouble(ushort value)`
  （double ToDouble（ushort value））
- `double ToDouble(int value)`
  （double ToDouble（int value））
- `double ToDouble(uint value)`
  （double ToDouble（uint value））
- `double ToDouble(long value)`
  （double ToDouble（long value））
- `double ToDouble(ulong value)`
  （double ToDouble（ulong value））
- `double ToDouble(float value)`
  （double ToDouble（float value））
- `double ToDouble(Decimal value)`
  （double ToDouble（Decimal value））
- `double ToDouble(string value, IFormatProvider provider)`
  （double ToDouble（string value, I格式化提供者 provider））
- `double ToDouble(bool value)`
  （double ToDouble（bool value））
- `Decimal ToDecimal(object value, IFormatProvider provider)`
  （Decimal ToDecimal（object value, I格式化提供者 provider））
- `Decimal ToDecimal(sbyte value)`
  （Decimal ToDecimal（sbyte value））
- `Decimal ToDecimal(byte value)`
  （Decimal ToDecimal（byte value））
- `Decimal ToDecimal(short value)`
  （Decimal ToDecimal（short value））
- `Decimal ToDecimal(ushort value)`
  （Decimal ToDecimal（ushort value））
- `Decimal ToDecimal(int value)`
  （Decimal ToDecimal（int value））
- `Decimal ToDecimal(uint value)`
  （Decimal ToDecimal（uint value））
- `Decimal ToDecimal(long value)`
  （Decimal ToDecimal（long value））
- `Decimal ToDecimal(ulong value)`
  （Decimal ToDecimal（ulong value））
- `Decimal ToDecimal(float value)`
  （Decimal ToDecimal（float value））
- `Decimal ToDecimal(double value)`
  （Decimal ToDecimal（double value））
- `Decimal ToDecimal(string value, IFormatProvider provider)`
  （Decimal ToDecimal（string value, I格式化提供者 provider））
- `Decimal ToDecimal(bool value)`
  （Decimal ToDecimal（bool value））
- `DateTime ToDateTime(string value, IFormatProvider provider)`
  （Date时间 ToDate时间（string value, I格式化提供者 provider））
- `string ToString(object value, IFormatProvider provider)`
  （string To字符串（object value, I格式化提供者 provider））
- `string ToString(char value, IFormatProvider provider)`
  （string To字符串（char value, I格式化提供者 provider））
- `string ToString(int value, IFormatProvider provider)`
  （string To字符串（int value, I格式化提供者 provider））
- `byte ToByte(string value, int fromBase)`
  （byte ToByte（string value, int fromBase））
- `sbyte ToSByte(string value, int fromBase)`
  （sbyte ToSByte（string value, int fromBase））
- `short ToInt16(string value, int fromBase)`
  （short ToInt16（string value, int fromBase））
- `ushort ToUInt16(string value, int fromBase)`
  （ushort ToUInt16（string value, int fromBase））
- `int ToInt32(string value, int fromBase)`
  （int ToInt32（string value, int fromBase））
- `uint ToUInt32(string value, int fromBase)`
  （uint ToUInt32（string value, int fromBase））
- `long ToInt64(string value, int fromBase)`
  （long ToInt64（string value, int fromBase））
- `ulong ToUInt64(string value, int fromBase)`
  （ulong ToUInt64（string value, int fromBase））
- `string ToString(byte value, int toBase)`
  （string To字符串（byte value, int toBase））
- `string ToString(int value, int toBase)`
  （string To字符串（int value, int toBase））
- `string ToString(long value, int toBase)`
  （string To字符串（long value, int toBase））
- `string ToBase64String(byte[] inArray)`
  （string ToBase64字符串（byte[] inArray））
- `string ToBase64String(byte[] inArray, int offset, int length, Base64FormattingOptions options)`
  （string ToBase64字符串（byte[] inArray, int offset, int length, Base64FormattingOptions options））
- `int ConvertToBase64Array(char* outChars, byte* inData, int offset, int length, bool insertLineBreaks)`
  （int 转换ToBase64数组（char* outChars, byte* inData, int offset, int length, bool insertLineBreaks））
- `int ToBase64_CalculateAndValidateOutputLength(int inputLength, bool insertLineBreaks)`
  （int ToBase64_计算And验证OutputLength（int inputLength, bool insertLineBreaks））
- `byte[] FromBase64String(string s)`
  （byte[] FromBase64字符串（string s））
- `byte[] FromBase64CharPtr(char* inputPtr, int inputLength)`
  （byte[] FromBase64CharPtr（char* inputPtr, int inputLength））
- `int FromBase64_Decode(char* startInputPtr, int inputLength, byte* startDestPtr, int destLength)`
  （int FromBase64_Decode（char* startInputPtr, int inputLength, byte* startDestPtr, int destLength））
- `int FromBase64_ComputeResultLength(char* inputPtr, int inputLength)`
  （int FromBase64_ComputeResultLength（char* inputPtr, int inputLength））

---

## Converter（Converter）

### 字段 (47)

- `int primitiveTypeEnumLength`（int primitive类型EnumLength）(偏移: 0x0)
- `Type[] typeA`（Type[] typeA）(偏移: 0x4)
- `Type[] arrayTypeA`（Type[] array类型A）(偏移: 0x8)
- `string[] valueA`（string[] valueA）(偏移: 0xC)
- `TypeCode[] typeCodeA`（类型Code[] typeCodeA）(偏移: 0x10)
- `InternalPrimitiveTypeE[] codeA`（内部的Primitive类型E[] codeA）(偏移: 0x14)
- `Type typeofISerializable`（类型 typeofISerializable）(偏移: 0x18)
- `Type typeofString`（类型 typeof字符串）(偏移: 0x1C)
- `Type typeofConverter`（类型 typeofConverter）(偏移: 0x20)
- `Type typeofBoolean`（类型 typeofBoolean）(偏移: 0x24)
- `Type typeofByte`（类型 typeofByte）(偏移: 0x28)
- `Type typeofChar`（类型 typeofChar）(偏移: 0x2C)
- `Type typeofDecimal`（类型 typeofDecimal）(偏移: 0x30)
- `Type typeofDouble`（类型 typeofDouble）(偏移: 0x34)
- `Type typeofInt16`（类型 typeofInt16）(偏移: 0x38)
- `Type typeofInt32`（类型 typeofInt32）(偏移: 0x3C)
- `Type typeofInt64`（类型 typeofInt64）(偏移: 0x40)
- `Type typeofSByte`（类型 typeofSByte）(偏移: 0x44)
- `Type typeofSingle`（类型 typeof单个）(偏移: 0x48)
- `Type typeofTimeSpan`（类型 typeof时间Span）(偏移: 0x4C)
- `Type typeofDateTime`（类型 typeofDate时间）(偏移: 0x50)
- `Type typeofUInt16`（类型 typeofUInt16）(偏移: 0x54)
- `Type typeofUInt32`（类型 typeofUInt32）(偏移: 0x58)
- `Type typeofUInt64`（类型 typeofUInt64）(偏移: 0x5C)
- `Type typeofObject`（类型 typeof对象）(偏移: 0x60)
- `Type typeofSystemVoid`（类型 typeof系统Void）(偏移: 0x64)
- `Assembly urtAssembly`（Assembly urtAssembly）(偏移: 0x68)
- `string urtAssemblyString`（string urtAssembly字符串）(偏移: 0x6C)
- `Type typeofTypeArray`（类型 typeof类型数组）(偏移: 0x70)
- `Type typeofObjectArray`（类型 typeof对象数组）(偏移: 0x74)
- `Type typeofStringArray`（类型 typeof字符串数组）(偏移: 0x78)
- `Type typeofBooleanArray`（类型 typeofBoolean数组）(偏移: 0x7C)
- `Type typeofByteArray`（类型 typeofByte数组）(偏移: 0x80)
- `Type typeofCharArray`（类型 typeofChar数组）(偏移: 0x84)
- `Type typeofDecimalArray`（类型 typeofDecimal数组）(偏移: 0x88)
- `Type typeofDoubleArray`（类型 typeofDouble数组）(偏移: 0x8C)
- `Type typeofInt16Array`（类型 typeofInt16数组）(偏移: 0x90)
- `Type typeofInt32Array`（类型 typeofInt32数组）(偏移: 0x94)
- `Type typeofInt64Array`（类型 typeofInt64数组）(偏移: 0x98)
- `Type typeofSByteArray`（类型 typeofSByte数组）(偏移: 0x9C)
- `Type typeofSingleArray`（类型 typeof单个数组）(偏移: 0xA0)
- `Type typeofTimeSpanArray`（类型 typeof时间Span数组）(偏移: 0xA4)
- `Type typeofDateTimeArray`（类型 typeofDate时间数组）(偏移: 0xA8)
- `Type typeofUInt16Array`（类型 typeofUInt16数组）(偏移: 0xAC)
- `Type typeofUInt32Array`（类型 typeofUInt32数组）(偏移: 0xB0)
- `Type typeofUInt64Array`（类型 typeofUInt64数组）(偏移: 0xB4)
- `Type typeofMarshalByRefObject`（类型 typeofMarshalByRef对象）(偏移: 0xB8)

### 方法 (16)

- `InternalPrimitiveTypeE ToCode(Type type)`
  （内部的Primitive类型E ToCode（类型 type））
- `bool IsWriteAsByteArray(InternalPrimitiveTypeE code)`
  （bool 是否WriteAsByte数组（内部的Primitive类型E code））
- `int TypeLength(InternalPrimitiveTypeE code)`
  （int 类型Length（内部的Primitive类型E code））
- `Type ToArrayType(InternalPrimitiveTypeE code)`
  （类型 To数组类型（内部的Primitive类型E code））
- `void InitTypeA()`
  （void 初始化类型A（））
- `void InitArrayTypeA()`
  （void 初始化数组类型A（））
- `Type ToType(InternalPrimitiveTypeE code)`
  （类型 To类型（内部的Primitive类型E code））
- `Array CreatePrimitiveArray(InternalPrimitiveTypeE code, int length)`
  （数组 创建Primitive数组（内部的Primitive类型E code, int length））
- `bool IsPrimitiveArray(Type type, out object typeInformation)`
  （bool 是否Primitive数组（类型 type, out object typeInformation））
- `void InitValueA()`
  （void 初始化值A（））
- `string ToComType(InternalPrimitiveTypeE code)`
  （string ToCom类型（内部的Primitive类型E code））
- `void InitTypeCodeA()`
  （void 初始化类型CodeA（））
- `TypeCode ToTypeCode(InternalPrimitiveTypeE code)`
  （类型Code To类型Code（内部的Primitive类型E code））
- `void InitCodeA()`
  （void 初始化CodeA（））
- `InternalPrimitiveTypeE ToPrimitiveTypeEnum(TypeCode typeCode)`
  （内部的Primitive类型E ToPrimitive类型Enum（类型Code typeCode））
- `object FromString(string value, InternalPrimitiveTypeE code)`
  （object From字符串（string value, 内部的Primitive类型E code））

---

## Cookie（Cookie）

### 字段 (3)

- `int instanceID`（int instanceID）(偏移: 0x0)
- `float scale`（float scale）(偏移: 0x4)
- `Vector2 sizes`（二维向量 sizes）(偏移: 0x8)

---

## Coord（Coord）

### 字段 (2)

- `short X`（short X）(偏移: 0x0)
- `short Y`（short Y）(偏移: 0x2)

---

## CopyColorPass（复制颜色Pass）

**继承**: ScriptableRenderPass（ScriptableRenderPass）

### 字段 (4)

- `int m_SampleOffsetShaderHandle`（int m_SampleOffset着色器句柄）(偏移: 0x54)
- `Material m_SamplingMaterial`（材质 m_Sampling材质）(偏移: 0x58)
- `Downsampling m_DownsamplingMethod`（Downsampling m_DownsamplingMethod）(偏移: 0x5C)
- `Material m_CopyColorMaterial`（材质 m_复制颜色材质）(偏移: 0x60)

### 方法 (8)

- `RenderTargetIdentifier get_source()`
  （Render目标Identifier get_source（））
- `void set_source(RenderTargetIdentifier value)`
  （void set_source（Render目标Identifier value））
- `RenderTargetHandle get_destination()`
  （Render目标句柄 get_destination（））
- `void set_destination(RenderTargetHandle value)`
  （void set_destination（Render目标句柄 value））
- `void Setup(RenderTargetIdentifier source, RenderTargetHandle destination, Downsampling downsampling)`
  （void Setup（Render目标Identifier source, Render目标句柄 destination, Downsampling downsampling））
- `void OnCameraSetup(CommandBuffer cmd, ref RenderingData renderingData)`
  （void On摄像机Setup（Command缓冲区 cmd, ref RenderingData renderingData））
- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（ScriptableRenderContext context, ref RenderingData renderingData））
- `void OnCameraCleanup(CommandBuffer cmd)`
  （void On摄像机清理（Command缓冲区 cmd））

---

## CopyDepthPass（复制深度Pass）

**继承**: ScriptableRenderPass（ScriptableRenderPass）

### 字段 (1)

- `Material m_CopyDepthMaterial`（材质 m_复制深度材质）(偏移: 0x98)

### 方法 (10)

- `RenderTargetHandle get_source()`
  （Render目标句柄 get_source（））
- `void set_source(RenderTargetHandle value)`
  （void set_source（Render目标句柄 value））
- `RenderTargetHandle get_destination()`
  （Render目标句柄 get_destination（））
- `void set_destination(RenderTargetHandle value)`
  （void set_destination（Render目标句柄 value））
- `bool get_AllocateRT()`
  （bool get_AllocateRT（））
- `void set_AllocateRT(bool value)`
  （void set_AllocateRT（bool value））
- `void Setup(RenderTargetHandle source, RenderTargetHandle destination)`
  （void Setup（Render目标句柄 source, Render目标句柄 destination））
- `void OnCameraSetup(CommandBuffer cmd, ref RenderingData renderingData)`
  （void On摄像机Setup（Command缓冲区 cmd, ref RenderingData renderingData））
- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（ScriptableRenderContext context, ref RenderingData renderingData））
- `void OnCameraCleanup(CommandBuffer cmd)`
  （void On摄像机清理（Command缓冲区 cmd））

---

## CopyTextureSupport（复制纹理Support）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Core（Core）

### 字段 (2)

- `Color halfAlpha`（颜色 half透明度）(偏移: 0x0)
- `Color zeroAlpha`（颜色 zero透明度）(偏移: 0x10)

---

## CoreCameraValues（Core摄像机Values）

**继承**: IEquatable<CoreCameraValues>（IEquatable<Core摄像机Values>）

### 字段 (3)

- `int filterMode`（int filter模式）(偏移: 0x0)
- `uint cullingMask`（uint culling掩码）(偏移: 0x4)
- `int instanceID`（int instanceID）(偏移: 0x8)

### 方法 (3)

- `bool Equals(CoreCameraValues other)`
  （bool Equals（Core摄像机Values other））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## CoreMatrixUtils（Core矩阵Utils）

### 方法 (7)

- `void MatrixTimesTranslation(ref Matrix4x4 inOutMatrix, Vector3 translation)`
  （void 矩阵TimesTranslation（ref Matrix4x4 inOutMatrix, 三维向量 translation））
- `void TranslationTimesMatrix(ref Matrix4x4 inOutMatrix, Vector3 translation)`
  （void TranslationTimes矩阵（ref Matrix4x4 inOutMatrix, 三维向量 translation））
- `Matrix4x4 MultiplyPerspectiveMatrix(Matrix4x4 perspective, Matrix4x4 rhs)`
  （Matrix4x4 MultiplyPerspective矩阵（Matrix4x4 perspective, Matrix4x4 rhs））
- `Matrix4x4 MultiplyOrthoMatrixCentered(Matrix4x4 ortho, Matrix4x4 rhs)`
  （Matrix4x4 MultiplyOrtho矩阵Centered（Matrix4x4 ortho, Matrix4x4 rhs））
- `Matrix4x4 MultiplyGenericOrthoMatrix(Matrix4x4 ortho, Matrix4x4 rhs)`
  （Matrix4x4 MultiplyGenericOrtho矩阵（Matrix4x4 ortho, Matrix4x4 rhs））
- `Matrix4x4 MultiplyOrthoMatrix(Matrix4x4 ortho, Matrix4x4 rhs, bool centered)`
  （Matrix4x4 MultiplyOrtho矩阵（Matrix4x4 ortho, Matrix4x4 rhs, bool centered））
- `Matrix4x4 MultiplyProjectionMatrix(Matrix4x4 projMatrix, Matrix4x4 rhs, bool orthoCentered)`
  （Matrix4x4 MultiplyProjection矩阵（Matrix4x4 projMatrix, Matrix4x4 rhs, bool orthoCentered））

---

## CoreUnsafeUtils（CoreUnsafeUtils）

### 方法 (4)

- `void QuickSort(uint[] arr, int left, int right)`
  （void QuickSort（uint[] arr, int left, int right））
- `int CompareHashes(int oldHashCount, Hash128* oldHashes, int newHashCount, Hash128* newHashes, int* addIndices, int* removeIndices, out int addCount, out int remCount)`
  （int CompareHashes（int oldHashCount, Hash128* oldHashes, int newHashCount, Hash128* newHashes, int* addIndices, int* removeIndices, out int addCount, out int remCount））
- `void CombineHashes(int count, Hash128* hashes, Hash128* outHash)`
  （void CombineHashes（int count, Hash128* hashes, Hash128* outHash））
- `bool HaveDuplicates(int[] arr)`
  （bool HaveDuplicates（int[] arr））

---

## CoreUnsafeUtils.FixedBufferStringQueue（CoreUnsafeUtils.固定缓冲区字符串队列）

### 字段 (5)

- `byte* m_ReadCursor`（byte* m_ReadCursor）(偏移: 0x0)
- `byte* m_WriteCursor`（byte* m_WriteCursor）(偏移: 0x4)
- `byte* m_BufferEnd`（byte* m_缓冲区结束）(偏移: 0x8)
- `byte* m_BufferStart`（byte* m_缓冲区开始）(偏移: 0xC)
- `int m_BufferLength`（int m_缓冲区Length）(偏移: 0x10)

### 方法 (5)

- `int get_Count()`
  （int get_数量（））
- `void set_Count(int value)`
  （void set_数量（int value））
- `bool TryPush(string v)`
  （bool TryPush（string v））
- `bool TryPop(out string v)`
  （bool TryPop（out string v））
- `void Clear()`
  （void 清除（））

---

## CoreUnsafeUtils.UintKeyGetter（CoreUnsafeUtils.Uint键Getter）

**继承**: CoreUnsafeUtils.IKeyGetter<uint, uint>（CoreUnsafeUtils.I键Getter<uint, uint>）

### 方法 (1)

- `uint Get(ref uint v)`
  （uint 获取（ref uint v））

---

## CoreUtils（CoreUtils）

### 字段 (9)

- `Vector3[] lookAtList`（Vector3[] lookAt列表）(偏移: 0x0)
- `Vector3[] upVectorList`（Vector3[] up向量列表）(偏移: 0x4)
- `Cubemap m_BlackCubeTexture`（Cubemap m_BlackCube纹理）(偏移: 0x8)
- `Cubemap m_MagentaCubeTexture`（Cubemap m_MagentaCube纹理）(偏移: 0xC)
- `CubemapArray m_MagentaCubeTextureArray`（Cubemap数组 m_MagentaCube纹理数组）(偏移: 0x10)
- `Cubemap m_WhiteCubeTexture`（Cubemap m_WhiteCube纹理）(偏移: 0x14)
- `RenderTexture m_EmptyUAV`（Render纹理 m_空UAV）(偏移: 0x18)
- `Texture3D m_BlackVolumeTexture`（Texture3D m_BlackVolume纹理）(偏移: 0x1C)
- `IEnumerable<Type> m_AssemblyTypes`（IEnumerable<Type> m_AssemblyTypes）(偏移: 0x20)

### 方法 (61)

- `Cubemap get_blackCubeTexture()`
  （Cubemap get_blackCube纹理（））
- `Cubemap get_magentaCubeTexture()`
  （Cubemap get_magentaCube纹理（））
- `CubemapArray get_magentaCubeTextureArray()`
  （Cubemap数组 get_magentaCube纹理数组（））
- `Cubemap get_whiteCubeTexture()`
  （Cubemap get_whiteCube纹理（））
- `RenderTexture get_emptyUAV()`
  （Render纹理 get_emptyUAV（））
- `Texture3D get_blackVolumeTexture()`
  （Texture3D get_blackVolume纹理（））
- `void ClearRenderTarget(CommandBuffer cmd, ClearFlag clearFlag, Color clearColor)`
  （void 清除Render目标（Command缓冲区 cmd, 清除标志 clearFlag, 颜色 clearColor））
- `int FixupDepthSlice(int depthSlice, RTHandle buffer)`
  （int Fixup深度Slice（int depthSlice, RT句柄 buffer））
- `int FixupDepthSlice(int depthSlice, CubemapFace cubemapFace)`
  （int Fixup深度Slice（int depthSlice, CubemapFace cubemapFace））
- `void SetRenderTarget(CommandBuffer cmd, RenderTargetIdentifier buffer, ClearFlag clearFlag, Color clearColor, int miplevel = 0, CubemapFace cubemapFace = -1, int depthSlice = -1)`
  （void 集合Render目标（Command缓冲区 cmd, Render目标Identifier buffer, 清除标志 clearFlag, 颜色 clearColor, int miplevel = 0, CubemapFace cubemapFace = -1, int depthSlice = -1））
- `void SetRenderTarget(CommandBuffer cmd, RenderTargetIdentifier buffer, ClearFlag clearFlag = 0, int miplevel = 0, CubemapFace cubemapFace = -1, int depthSlice = -1)`
  （void 集合Render目标（Command缓冲区 cmd, Render目标Identifier buffer, 清除标志 clearFlag = 0, int miplevel = 0, CubemapFace cubemapFace = -1, int depthSlice = -1））
- `void SetRenderTarget(CommandBuffer cmd, RenderTargetIdentifier colorBuffer, RenderTargetIdentifier depthBuffer, int miplevel = 0, CubemapFace cubemapFace = -1, int depthSlice = -1)`
  （void 集合Render目标（Command缓冲区 cmd, Render目标Identifier colorBuffer, Render目标Identifier depthBuffer, int miplevel = 0, CubemapFace cubemapFace = -1, int depthSlice = -1））
- `void SetRenderTarget(CommandBuffer cmd, RenderTargetIdentifier colorBuffer, RenderTargetIdentifier depthBuffer, ClearFlag clearFlag, int miplevel = 0, CubemapFace cubemapFace = -1, int depthSlice = -1)`
  （void 集合Render目标（Command缓冲区 cmd, Render目标Identifier colorBuffer, Render目标Identifier depthBuffer, 清除标志 clearFlag, int miplevel = 0, CubemapFace cubemapFace = -1, int depthSlice = -1））
- `void SetRenderTarget(CommandBuffer cmd, RenderTargetIdentifier colorBuffer, RenderTargetIdentifier depthBuffer, ClearFlag clearFlag, Color clearColor, int miplevel = 0, CubemapFace cubemapFace = -1, int depthSlice = -1)`
  （void 集合Render目标（Command缓冲区 cmd, Render目标Identifier colorBuffer, Render目标Identifier depthBuffer, 清除标志 clearFlag, 颜色 clearColor, int miplevel = 0, CubemapFace cubemapFace = -1, int depthSlice = -1））
- `void SetRenderTarget(CommandBuffer cmd, RenderTargetIdentifier[] colorBuffers, RenderTargetIdentifier depthBuffer)`
  （void 集合Render目标（Command缓冲区 cmd, Render目标Identifier[] colorBuffers, Render目标Identifier depthBuffer））
- `void SetRenderTarget(CommandBuffer cmd, RenderTargetIdentifier[] colorBuffers, RenderTargetIdentifier depthBuffer, ClearFlag clearFlag = 0)`
  （void 集合Render目标（Command缓冲区 cmd, Render目标Identifier[] colorBuffers, Render目标Identifier depthBuffer, 清除标志 clearFlag = 0））
- `void SetRenderTarget(CommandBuffer cmd, RenderTargetIdentifier[] colorBuffers, RenderTargetIdentifier depthBuffer, ClearFlag clearFlag, Color clearColor)`
  （void 集合Render目标（Command缓冲区 cmd, Render目标Identifier[] colorBuffers, Render目标Identifier depthBuffer, 清除标志 clearFlag, 颜色 clearColor））
- `void SetRenderTarget(CommandBuffer cmd, RenderTargetIdentifier buffer, RenderBufferLoadAction loadAction, RenderBufferStoreAction storeAction, ClearFlag clearFlag, Color clearColor)`
  （void 集合Render目标（Command缓冲区 cmd, Render目标Identifier buffer, Render缓冲区加载动作 loadAction, Render缓冲区商店动作 storeAction, 清除标志 clearFlag, 颜色 clearColor））
- `void SetRenderTarget(CommandBuffer cmd, RenderTargetIdentifier buffer, RenderBufferLoadAction loadAction, RenderBufferStoreAction storeAction, ClearFlag clearFlag)`
  （void 集合Render目标（Command缓冲区 cmd, Render目标Identifier buffer, Render缓冲区加载动作 loadAction, Render缓冲区商店动作 storeAction, 清除标志 clearFlag））
- `void SetRenderTarget(CommandBuffer cmd, RenderTargetIdentifier colorBuffer, RenderBufferLoadAction colorLoadAction, RenderBufferStoreAction colorStoreAction, RenderTargetIdentifier depthBuffer, RenderBufferLoadAction depthLoadAction, RenderBufferStoreAction depthStoreAction, ClearFlag clearFlag, Color clearColor)`
  （void 集合Render目标（Command缓冲区 cmd, Render目标Identifier colorBuffer, Render缓冲区加载动作 colorLoadAction, Render缓冲区商店动作 colorStoreAction, Render目标Identifier depthBuffer, Render缓冲区加载动作 depthLoadAction, Render缓冲区商店动作 depthStoreAction, 清除标志 clearFlag, 颜色 clearColor））
- `void SetRenderTarget(CommandBuffer cmd, RenderTargetIdentifier colorBuffer, RenderBufferLoadAction colorLoadAction, RenderBufferStoreAction colorStoreAction, RenderTargetIdentifier depthBuffer, RenderBufferLoadAction depthLoadAction, RenderBufferStoreAction depthStoreAction, ClearFlag clearFlag)`
  （void 集合Render目标（Command缓冲区 cmd, Render目标Identifier colorBuffer, Render缓冲区加载动作 colorLoadAction, Render缓冲区商店动作 colorStoreAction, Render目标Identifier depthBuffer, Render缓冲区加载动作 depthLoadAction, Render缓冲区商店动作 depthStoreAction, 清除标志 clearFlag））
- `void SetViewportAndClear(CommandBuffer cmd, RTHandle buffer, ClearFlag clearFlag, Color clearColor)`
  （void 集合ViewportAnd清除（Command缓冲区 cmd, RT句柄 buffer, 清除标志 clearFlag, 颜色 clearColor））
- `void SetRenderTarget(CommandBuffer cmd, RTHandle buffer, ClearFlag clearFlag, Color clearColor, int miplevel = 0, CubemapFace cubemapFace = -1, int depthSlice = -1)`
  （void 集合Render目标（Command缓冲区 cmd, RT句柄 buffer, 清除标志 clearFlag, 颜色 clearColor, int miplevel = 0, CubemapFace cubemapFace = -1, int depthSlice = -1））
- `void SetRenderTarget(CommandBuffer cmd, RTHandle buffer, ClearFlag clearFlag = 0, int miplevel = 0, CubemapFace cubemapFace = -1, int depthSlice = -1)`
  （void 集合Render目标（Command缓冲区 cmd, RT句柄 buffer, 清除标志 clearFlag = 0, int miplevel = 0, CubemapFace cubemapFace = -1, int depthSlice = -1））
- `void SetRenderTarget(CommandBuffer cmd, RTHandle colorBuffer, RTHandle depthBuffer, int miplevel = 0, CubemapFace cubemapFace = -1, int depthSlice = -1)`
  （void 集合Render目标（Command缓冲区 cmd, RT句柄 colorBuffer, RT句柄 depthBuffer, int miplevel = 0, CubemapFace cubemapFace = -1, int depthSlice = -1））
- `void SetRenderTarget(CommandBuffer cmd, RTHandle colorBuffer, RTHandle depthBuffer, ClearFlag clearFlag, int miplevel = 0, CubemapFace cubemapFace = -1, int depthSlice = -1)`
  （void 集合Render目标（Command缓冲区 cmd, RT句柄 colorBuffer, RT句柄 depthBuffer, 清除标志 clearFlag, int miplevel = 0, CubemapFace cubemapFace = -1, int depthSlice = -1））
- `void SetRenderTarget(CommandBuffer cmd, RTHandle colorBuffer, RTHandle depthBuffer, ClearFlag clearFlag, Color clearColor, int miplevel = 0, CubemapFace cubemapFace = -1, int depthSlice = -1)`
  （void 集合Render目标（Command缓冲区 cmd, RT句柄 colorBuffer, RT句柄 depthBuffer, 清除标志 clearFlag, 颜色 clearColor, int miplevel = 0, CubemapFace cubemapFace = -1, int depthSlice = -1））
- `void SetRenderTarget(CommandBuffer cmd, RenderTargetIdentifier[] colorBuffers, RTHandle depthBuffer)`
  （void 集合Render目标（Command缓冲区 cmd, Render目标Identifier[] colorBuffers, RT句柄 depthBuffer））
- `void SetRenderTarget(CommandBuffer cmd, RenderTargetIdentifier[] colorBuffers, RTHandle depthBuffer, ClearFlag clearFlag = 0)`
  （void 集合Render目标（Command缓冲区 cmd, Render目标Identifier[] colorBuffers, RT句柄 depthBuffer, 清除标志 clearFlag = 0））
- `void SetRenderTarget(CommandBuffer cmd, RenderTargetIdentifier[] colorBuffers, RTHandle depthBuffer, ClearFlag clearFlag, Color clearColor)`
  （void 集合Render目标（Command缓冲区 cmd, Render目标Identifier[] colorBuffers, RT句柄 depthBuffer, 清除标志 clearFlag, 颜色 clearColor））
- `void SetViewport(CommandBuffer cmd, RTHandle target)`
  （void 集合Viewport（Command缓冲区 cmd, RT句柄 target））
- `string GetRenderTargetAutoName(int width, int height, int depth, RenderTextureFormat format, string name, bool mips = False, bool enableMSAA = False, MSAASamples msaaSamples = 1)`
  （string 获取Render目标自动名称（int width, int height, int depth, Render纹理格式化 format, string name, bool mips = False, bool enableMSAA = False, MSAASamples msaaSamples = 1））
- `string GetRenderTargetAutoName(int width, int height, int depth, GraphicsFormat format, string name, bool mips = False, bool enableMSAA = False, MSAASamples msaaSamples = 1)`
  （string 获取Render目标自动名称（int width, int height, int depth, Graphics格式化 format, string name, bool mips = False, bool enableMSAA = False, MSAASamples msaaSamples = 1））
- `string GetRenderTargetAutoName(int width, int height, int depth, GraphicsFormat format, TextureDimension dim, string name, bool mips = False, bool enableMSAA = False, MSAASamples msaaSamples = 1, bool dynamicRes = False)`
  （string 获取Render目标自动名称（int width, int height, int depth, Graphics格式化 format, 纹理Dimension dim, string name, bool mips = False, bool enableMSAA = False, MSAASamples msaaSamples = 1, bool dynamicRes = False））
- `string GetRenderTargetAutoName(int width, int height, int depth, string format, TextureDimension dim, string name, bool mips, bool enableMSAA, MSAASamples msaaSamples, bool dynamicRes)`
  （string 获取Render目标自动名称（int width, int height, int depth, string format, 纹理Dimension dim, string name, bool mips, bool enableMSAA, MSAASamples msaaSamples, bool dynamicRes））
- `string GetTextureAutoName(int width, int height, TextureFormat format, TextureDimension dim = 0, string name = "", bool mips = False, int depth = 0)`
  （string 获取纹理自动名称（int width, int height, 纹理格式化 format, 纹理Dimension dim = 0, string name = "", bool mips = False, int depth = 0））
- `string GetTextureAutoName(int width, int height, GraphicsFormat format, TextureDimension dim = 0, string name = "", bool mips = False, int depth = 0)`
  （string 获取纹理自动名称（int width, int height, Graphics格式化 format, 纹理Dimension dim = 0, string name = "", bool mips = False, int depth = 0））
- `string GetTextureAutoName(int width, int height, string format, TextureDimension dim = 0, string name = "", bool mips = False, int depth = 0)`
  （string 获取纹理自动名称（int width, int height, string format, 纹理Dimension dim = 0, string name = "", bool mips = False, int depth = 0））
- `void ClearCubemap(CommandBuffer cmd, RenderTexture renderTexture, Color clearColor, bool clearMips = False)`
  （void 清除Cubemap（Command缓冲区 cmd, Render纹理 renderTexture, 颜色 clearColor, bool clearMips = False））
- `void DrawFullScreen(CommandBuffer commandBuffer, Material material, MaterialPropertyBlock properties, int shaderPassId = 0)`
  （void Draw满屏幕的（Command缓冲区 commandBuffer, 材质 material, 材质属性Block properties, int shaderPassId = 0））
- `void DrawFullScreen(CommandBuffer commandBuffer, Material material, RenderTargetIdentifier colorBuffer, MaterialPropertyBlock properties, int shaderPassId = 0)`
  （void Draw满屏幕的（Command缓冲区 commandBuffer, 材质 material, Render目标Identifier colorBuffer, 材质属性Block properties, int shaderPassId = 0））
- `void DrawFullScreen(CommandBuffer commandBuffer, Material material, RenderTargetIdentifier colorBuffer, RenderTargetIdentifier depthStencilBuffer, MaterialPropertyBlock properties, int shaderPassId = 0)`
  （void Draw满屏幕的（Command缓冲区 commandBuffer, 材质 material, Render目标Identifier colorBuffer, Render目标Identifier depthStencilBuffer, 材质属性Block properties, int shaderPassId = 0））
- `void DrawFullScreen(CommandBuffer commandBuffer, Material material, RenderTargetIdentifier[] colorBuffers, RenderTargetIdentifier depthStencilBuffer, MaterialPropertyBlock properties, int shaderPassId = 0)`
  （void Draw满屏幕的（Command缓冲区 commandBuffer, 材质 material, Render目标Identifier[] colorBuffers, Render目标Identifier depthStencilBuffer, 材质属性Block properties, int shaderPassId = 0））
- `void DrawFullScreen(CommandBuffer commandBuffer, Material material, RenderTargetIdentifier[] colorBuffers, MaterialPropertyBlock properties, int shaderPassId = 0)`
  （void Draw满屏幕的（Command缓冲区 commandBuffer, 材质 material, Render目标Identifier[] colorBuffers, 材质属性Block properties, int shaderPassId = 0））
- `Color ConvertSRGBToActiveColorSpace(Color color)`
  （颜色 转换SRGBTo激活的颜色Space（颜色 color））
- `Color ConvertLinearToActiveColorSpace(Color color)`
  （颜色 转换LinearTo激活的颜色Space（颜色 color））
- `Material CreateEngineMaterial(string shaderPath)`
  （材质 创建引擎材质（string shaderPath））
- `Material CreateEngineMaterial(Shader shader)`
  （材质 创建引擎材质（着色器 shader））
- `void SetKeyword(CommandBuffer cmd, string keyword, bool state)`
  （void 集合Keyword（Command缓冲区 cmd, string keyword, bool state））
- `void SetKeyword(Material material, string keyword, bool state)`
  （void 集合Keyword（材质 material, string keyword, bool state））
- `void SetKeyword(ComputeShader cs, string keyword, bool state)`
  （void 集合Keyword（Compute着色器 cs, string keyword, bool state））
- `void Destroy(Object obj)`
  （void 销毁（对象 obj））
- `IEnumerable<Type> GetAllAssemblyTypes()`
  （IEnumerable<Type> 获取所有AssemblyTypes（））
- `void SafeRelease(ComputeBuffer buffer)`
  （void SafeRelease（Compute缓冲区 buffer））
- `Mesh CreateCubeMesh(Vector3 min, Vector3 max)`
  （网格 创建Cube网格（三维向量 min, 三维向量 max））
- `bool ArePostProcessesEnabled(Camera camera)`
  （bool ArePostProcesses启用的（摄像机 camera））
- `bool AreAnimatedMaterialsEnabled(Camera camera)`
  （bool AreAnimatedMaterials启用的（摄像机 camera））
- `bool IsSceneLightingDisabled(Camera camera)`
  （bool 是否场景Lighting禁用的（摄像机 camera））
- `bool IsLightOverlapDebugEnabled(Camera camera)`
  （bool 是否光照OverlapDebug启用的（摄像机 camera））
- `bool IsSceneViewFogEnabled(Camera camera)`
  （bool 是否场景视图Fog启用的（摄像机 camera））
- `void DrawRendererList(ScriptableRenderContext renderContext, CommandBuffer cmd, RendererList rendererList)`
  （void Draw渲染器列表（ScriptableRenderContext renderContext, Command缓冲区 cmd, 渲染器列表 rendererList））

---

## Coroutine（协程）

**继承**: YieldInstruction（YieldInstruction）

### 字段 (1)

- `IntPtr m_Ptr`（整数Ptr m_Ptr）(偏移: 0x8)

### 方法 (2)

- `void Finalize()`
  （void Finalize（））
- `void ReleaseCoroutine(IntPtr ptr)`
  （void Release协程（整数Ptr ptr））

---

## CountingStream（Counting流）

**继承**: Stream（流）

### 字段 (4)

- `Stream _s`（流 _s）(偏移: 0x14)
- `long _bytesWritten`（long _bytesWritten）(偏移: 0x18)
- `long _bytesRead`（long _bytesRead）(偏移: 0x20)
- `long _initialOffset`（long _initialOffset）(偏移: 0x28)

### 方法 (15)

- `long get_BytesWritten()`
  （long get_BytesWritten（））
- `long get_BytesRead()`
  （long get_BytesRead（））
- `void Adjust(long delta)`
  （void Adjust（long delta））
- `int Read(byte[] buffer, int offset, int count)`
  （int Read（byte[] buffer, int offset, int count））
- `void Write(byte[] buffer, int offset, int count)`
  （void Write（byte[] buffer, int offset, int count））
- `bool get_CanRead()`
  （bool get_能否Read（））
- `bool get_CanSeek()`
  （bool get_能否Seek（））
- `bool get_CanWrite()`
  （bool get_能否Write（））
- `void Flush()`
  （void Flush（））
- `long get_Length()`
  （long get_Length（））
- `long get_ComputedPosition()`
  （long get_ComputedPosition（））
- `long get_Position()`
  （long get_Position（））
- `void set_Position(long value)`
  （void set_Position（long value））
- `long Seek(long offset, SeekOrigin origin)`
  （long Seek（long offset, SeekOrigin origin））
- `void SetLength(long value)`
  （void 集合Length（long value））

---

## CrabStep（CrabStep）

### 字段 (2)

- `float nextChangeTime`（float nextChange时间）(偏移: 0x8)
- `int curStep`（int curStep）(偏移: 0xC)

### 方法 (1)

- `void TrySet(ref Vector2Int moveState)`
  （void Try集合（ref Vector2Int moveState））

---

## CrcCalculatorStream（CrcCalculator流）

**继承**: Stream, IDisposable（流, IDisposable）

### 字段 (5)

- `long UnsetLengthLimit`（long UnsetLengthLimit）(偏移: 0x0)
- `Stream _innerStream`（流 _inner流）(偏移: 0x14)
- `CRC32 _Crc32`（CRC32 _Crc32）(偏移: 0x18)
- `long _lengthLimit`（long _lengthLimit）(偏移: 0x20)
- `bool _leaveOpen`（bool _leave打开）(偏移: 0x28)

### 方法 (14)

- `long get_TotalBytesSlurped()`
  （long get_TotalBytesSlurped（））
- `int get_Crc()`
  （int get_Crc（））
- `int Read(byte[] buffer, int offset, int count)`
  （int Read（byte[] buffer, int offset, int count））
- `void Write(byte[] buffer, int offset, int count)`
  （void Write（byte[] buffer, int offset, int count））
- `bool get_CanRead()`
  （bool get_能否Read（））
- `bool get_CanSeek()`
  （bool get_能否Seek（））
- `bool get_CanWrite()`
  （bool get_能否Write（））
- `void Flush()`
  （void Flush（））
- `long get_Length()`
  （long get_Length（））
- `long get_Position()`
  （long get_Position（））
- `void set_Position(long value)`
  （void set_Position（long value））
- `long Seek(long offset, SeekOrigin origin)`
  （long Seek（long offset, SeekOrigin origin））
- `void SetLength(long value)`
  （void 集合Length（long value））
- `void Close()`
  （void 关闭（））

---

## CreateAssetMenuAttribute（创建资产菜单Attribute）

**继承**: Attribute（Attribute）

### 方法 (2)

- `void set_menuName(string value)`
  （void set_menu名称（string value））
- `void set_fileName(string value)`
  （void set_file名称（string value））

---

## CriticalDamageText（Critical伤害文本）

**继承**: RecyclableObject（Recyclable对象）

### 字段 (1)

- `Text dmgText`（文本 dmg文本）(偏移: 0x30)

### 方法 (2)

- `void Active(int damage)`
  （void 激活的（int damage））
- `void Work()`
  （void Work（））

---

## CriticalFinalizerObject（CriticalFinalizer对象）

### 方法 (1)

- `void Finalize()`
  （void Finalize（））

---

## CrossAppDomainChannel（CrossAppDomainChannel）

**继承**: IChannel, IChannelSender, IChannelReceiver（IChannel, IChannelSender, IChannelReceiver）

### 字段 (1)

- `object s_lock`（object s_lock）(偏移: 0x0)

### 方法 (6)

- `void RegisterCrossAppDomainChannel()`
  （void RegisterCrossAppDomainChannel（））
- `string get_ChannelName()`
  （string get_Channel名称（））
- `int get_ChannelPriority()`
  （int get_ChannelPriority（））
- `object get_ChannelData()`
  （object get_Channel数据（））
- `void StartListening(object data)`
  （void 开始Listening（object data））
- `IMessageSink CreateMessageSink(string url, object data, out string uri)`
  （IMessageSink 创建MessageSink（string url, object data, out string uri））

---

## CrossAppDomainData（CrossAppDomain数据）

### 字段 (3)

- `object _ContextID`（object _ContextID）(偏移: 0x8)
- `int _DomainID`（int _DomainID）(偏移: 0xC)
- `string _processGuid`（string _processGuid）(偏移: 0x10)

### 方法 (2)

- `int get_DomainID()`
  （int get_DomainID（））
- `string get_ProcessID()`
  （string get_处理ID（））

---

## CrossAppDomainSink（CrossAppDomainSink）

**继承**: IMessageSink（IMessageSink）

### 字段 (3)

- `Hashtable s_sinks`（Hashtable s_sinks）(偏移: 0x0)
- `MethodInfo processMessageMethod`（Method信息 processMessageMethod）(偏移: 0x4)
- `int _domainID`（int _domainID）(偏移: 0x8)

### 方法 (6)

- `CrossAppDomainSink GetSink(int domainID)`
  （CrossAppDomainSink 获取Sink（int domainID））
- `int get_TargetDomainId()`
  （int get_目标DomainId（））
- `CrossAppDomainSink.ProcessMessageRes ProcessMessageInDomain(byte[] arrRequest, CADMethodCallMessage cadMsg)`
  （CrossAppDomainSink.处理MessageRes 处理MessageInDomain（byte[] arrRequest, CADMethodCallMessage cadMsg））
- `IMessage SyncProcessMessage(IMessage msgRequest)`
  （IMessage 同步处理Message（IMessage msgRequest））
- `IMessageCtrl AsyncProcessMessage(IMessage reqMsg, IMessageSink replySink)`
  （IMessageCtrl 异步处理Message（IMessage reqMsg, IMessageSink replySink））
- `void SendAsyncMessage(object data)`
  （void 发送异步Message（object data））

---

## CrossAppDomainSink.ProcessMessageRes（CrossAppDomainSink.处理MessageRes）

### 字段 (2)

- `byte[] arrResponse`（byte[] arr响应）(偏移: 0x0)
- `CADMethodReturnMessage cadMrm`（CADMethodReturnMessage cadMrm）(偏移: 0x4)

---

## CrossContextChannel（CrossContextChannel）

**继承**: IMessageSink（IMessageSink）

### 方法 (2)

- `IMessage SyncProcessMessage(IMessage msg)`
  （IMessage 同步处理Message（IMessage msg））
- `IMessageCtrl AsyncProcessMessage(IMessage msg, IMessageSink replySink)`
  （IMessageCtrl 异步处理Message（IMessage msg, IMessageSink replySink））

---

## CrossContextChannel.ContextRestoreSink（CrossContextChannel.ContextRestoreSink）

**继承**: IMessageSink（IMessageSink）

### 字段 (3)

- `IMessageSink _next`（IMessageSink _next）(偏移: 0x8)
- `Context _context`（Context _context）(偏移: 0xC)
- `IMessage _call`（IMessage _call）(偏移: 0x10)

### 方法 (2)

- `IMessage SyncProcessMessage(IMessage msg)`
  （IMessage 同步处理Message（IMessage msg））
- `IMessageCtrl AsyncProcessMessage(IMessage msg, IMessageSink replySink)`
  （IMessageCtrl 异步处理Message（IMessage msg, IMessageSink replySink））

---

## CrossContextDelegate（CrossContext委托）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke()`
  （void Invoke（））
- `IAsyncResult BeginInvoke(AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## CryptoConfig（Crypto配置）

### 方法 (7)

- `byte[] EncodeOID(string str)`
  （byte[] EncodeOID（string str））
- `byte[] EncodeLongNumber(long x)`
  （byte[] EncodeLongNumber（long x））
- `bool get_AllowOnlyFipsAlgorithms()`
  （bool get_允许OnlyFipsAlgorithms（））
- `object CreateFromName(string name)`
  （object 创建From名称（string name））
- `object CreateFromName(string name, object[] args)`
  （object 创建From名称（string name, object[] args））
- `string MapNameToOID(string name, object arg)`
  （string 映射名称ToOID（string name, object arg））
- `string MapNameToOID(string name)`
  （string 映射名称ToOID（string name））

---

## CryptoConvert（Crypto转换）

### 方法 (1)

- `string ToHex(byte[] input)`
  （string ToHex（byte[] input））

---

## CryptoMode（Crypto模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## CryptoStream（Crypto流）

**继承**: Stream, IDisposable（流, IDisposable）

### 字段 (12)

- `Stream _stream`（流 _stream）(偏移: 0x14)
- `ICryptoTransform _Transform`（ICrypto变换 _变换）(偏移: 0x18)
- `byte[] _InputBuffer`（byte[] _输入缓冲区）(偏移: 0x1C)
- `int _InputBufferIndex`（int _输入缓冲区索引）(偏移: 0x20)
- `int _InputBlockSize`（int _输入Block大小）(偏移: 0x24)
- `byte[] _OutputBuffer`（byte[] _Output缓冲区）(偏移: 0x28)
- `int _OutputBufferIndex`（int _Output缓冲区索引）(偏移: 0x2C)
- `int _OutputBlockSize`（int _OutputBlock大小）(偏移: 0x30)
- `CryptoStreamMode _transformMode`（Crypto流模式 _transform模式）(偏移: 0x34)
- `bool _canRead`（bool _canRead）(偏移: 0x38)
- `bool _canWrite`（bool _canWrite）(偏移: 0x39)
- `bool _finalBlockTransformed`（bool _finalBlockTransformed）(偏移: 0x3A)

### 方法 (16)

- `bool get_CanRead()`
  （bool get_能否Read（））
- `bool get_CanSeek()`
  （bool get_能否Seek（））
- `bool get_CanWrite()`
  （bool get_能否Write（））
- `long get_Length()`
  （long get_Length（））
- `long get_Position()`
  （long get_Position（））
- `void set_Position(long value)`
  （void set_Position（long value））
- `bool get_HasFlushedFinalBlock()`
  （bool get_是否有FlushedFinalBlock（））
- `void FlushFinalBlock()`
  （void FlushFinalBlock（））
- `void Flush()`
  （void Flush（））
- `long Seek(long offset, SeekOrigin origin)`
  （long Seek（long offset, SeekOrigin origin））
- `void SetLength(long value)`
  （void 集合Length（long value））
- `int Read([In] [Out] byte[] buffer, int offset, int count)`
  （int Read（[In] [Out] byte[] buffer, int offset, int count））
- `void Write(byte[] buffer, int offset, int count)`
  （void Write（byte[] buffer, int offset, int count））
- `void Clear()`
  （void 清除（））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））
- `void InitializeBuffer()`
  （void 初始化缓冲区（））

---

## CryptoStreamMode（Crypto流模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## CspParameters（CspParameters）

### 字段 (5)

- `int ProviderType`（int 提供者类型）(偏移: 0x8)
- `string ProviderName`（string 提供者名称）(偏移: 0xC)
- `string KeyContainerName`（string 键容器名称）(偏移: 0x10)
- `int KeyNumber`（int 键Number）(偏移: 0x14)
- `int m_flags`（int m_flags）(偏移: 0x18)

### 方法 (2)

- `CspProviderFlags get_Flags()`
  （Csp提供者Flags get_Flags（））
- `void set_Flags(CspProviderFlags value)`
  （void set_Flags（Csp提供者Flags value））

---

## CspProviderFlags（Csp提供者Flags）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Cubemap（Cubemap）

**继承**: Texture（纹理）

### 方法 (10)

- `bool Internal_CreateImpl(Cubemap mono, int ext, int mipCount, GraphicsFormat format, TextureCreationFlags flags, IntPtr nativeTex)`
  （bool Internal_创建Impl（Cubemap mono, int ext, int mipCount, Graphics格式化 format, 纹理CreationFlags flags, 整数Ptr nativeTex））
- `void Internal_Create(Cubemap mono, int ext, int mipCount, GraphicsFormat format, TextureCreationFlags flags, IntPtr nativeTex)`
  （void Internal_创建（Cubemap mono, int ext, int mipCount, Graphics格式化 format, 纹理CreationFlags flags, 整数Ptr nativeTex））
- `void ApplyImpl(bool updateMipmaps, bool makeNoLongerReadable)`
  （void 应用Impl（bool updateMipmaps, bool makeNoLongerReadable））
- `bool get_isReadable()`
  （bool get_isReadable（））
- `void SetPixelImpl(int image, int x, int y, Color color)`
  （void 集合PixelImpl（int image, int x, int y, 颜色 color））
- `void SetPixel(CubemapFace face, int x, int y, Color color)`
  （void 集合Pixel（CubemapFace face, int x, int y, 颜色 color））
- `void Apply(bool updateMipmaps, bool makeNoLongerReadable)`
  （void 应用（bool updateMipmaps, bool makeNoLongerReadable））
- `void Apply()`
  （void 应用（））
- `void ValidateIsNotCrunched(TextureCreationFlags flags)`
  （void 验证是否NotCrunched（纹理CreationFlags flags））
- `void SetPixelImpl_Injected(int image, int x, int y, ref Color color)`
  （void 集合PixelImpl_Injected（int image, int x, int y, ref Color color））

---

## CubemapArray（Cubemap数组）

**继承**: Texture（纹理）

### 方法 (9)

- `bool get_isReadable()`
  （bool get_isReadable（））
- `bool Internal_CreateImpl(CubemapArray mono, int ext, int count, int mipCount, GraphicsFormat format, TextureCreationFlags flags)`
  （bool Internal_创建Impl（Cubemap数组 mono, int ext, int count, int mipCount, Graphics格式化 format, 纹理CreationFlags flags））
- `void Internal_Create(CubemapArray mono, int ext, int count, int mipCount, GraphicsFormat format, TextureCreationFlags flags)`
  （void Internal_创建（Cubemap数组 mono, int ext, int count, int mipCount, Graphics格式化 format, 纹理CreationFlags flags））
- `void ApplyImpl(bool updateMipmaps, bool makeNoLongerReadable)`
  （void 应用Impl（bool updateMipmaps, bool makeNoLongerReadable））
- `void SetPixels(Color[] colors, CubemapFace face, int arrayElement, int miplevel)`
  （void 集合Pixels（Color[] colors, CubemapFace face, int arrayElement, int miplevel））
- `void SetPixels(Color[] colors, CubemapFace face, int arrayElement)`
  （void 集合Pixels（Color[] colors, CubemapFace face, int arrayElement））
- `void Apply(bool updateMipmaps, bool makeNoLongerReadable)`
  （void 应用（bool updateMipmaps, bool makeNoLongerReadable））
- `void Apply()`
  （void 应用（））
- `void ValidateIsNotCrunched(TextureCreationFlags flags)`
  （void 验证是否NotCrunched（纹理CreationFlags flags））

---

