# 游戏类定义 (Part 20/21)

共 200 个类 (总序号 3801 - 4000)

---

## VideoPlayer（Video玩家）

**继承**: Behaviour（行为）

### 字段 (8)

- `VideoPlayer.EventHandler prepareCompleted`（VideoPlayer.事件处理器 prepareCompleted）(偏移: 0xC)
- `VideoPlayer.EventHandler loopPointReached`（VideoPlayer.事件处理器 loopPointReached）(偏移: 0x10)
- `VideoPlayer.EventHandler started`（VideoPlayer.事件处理器 started）(偏移: 0x14)
- `VideoPlayer.EventHandler frameDropped`（VideoPlayer.事件处理器 frameDropped）(偏移: 0x18)
- `VideoPlayer.ErrorEventHandler errorReceived`（VideoPlayer.Error事件处理器 errorReceived）(偏移: 0x1C)
- `VideoPlayer.EventHandler seekCompleted`（VideoPlayer.事件处理器 seekCompleted）(偏移: 0x20)
- `VideoPlayer.TimeEventHandler clockResyncOccurred`（VideoPlayer.时间事件处理器 clockResyncOccurred）(偏移: 0x24)
- `VideoPlayer.FrameReadyEventHandler frameReady`（VideoPlayer.FrameReady事件处理器 frameReady）(偏移: 0x28)

### 方法 (8)

- `void InvokePrepareCompletedCallback_Internal(VideoPlayer source)`
  （void InvokePrepareCompletedCallback_内部的（Video玩家 source））
- `void InvokeFrameReadyCallback_Internal(VideoPlayer source, long frameIdx)`
  （void InvokeFrameReadyCallback_内部的（Video玩家 source, long frameIdx））
- `void InvokeLoopPointReachedCallback_Internal(VideoPlayer source)`
  （void InvokeLoopPointReachedCallback_内部的（Video玩家 source））
- `void InvokeStartedCallback_Internal(VideoPlayer source)`
  （void InvokeStartedCallback_内部的（Video玩家 source））
- `void InvokeFrameDroppedCallback_Internal(VideoPlayer source)`
  （void InvokeFrameDroppedCallback_内部的（Video玩家 source））
- `void InvokeErrorReceivedCallback_Internal(VideoPlayer source, string errorStr)`
  （void InvokeErrorReceivedCallback_内部的（Video玩家 source, string errorStr））
- `void InvokeSeekCompletedCallback_Internal(VideoPlayer source)`
  （void InvokeSeekCompletedCallback_内部的（Video玩家 source））
- `void InvokeClockResyncOccurredCallback_Internal(VideoPlayer source, double seconds)`
  （void Invoke时钟ResyncOccurredCallback_内部的（Video玩家 source, double seconds））

---

## VideoPlayer.ErrorEventHandler（VideoPlayer.Error事件处理器）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(VideoPlayer source, string message)`
  （void Invoke（Video玩家 source, string message））
- `IAsyncResult BeginInvoke(VideoPlayer source, string message, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Video玩家 source, string message, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## VideoPlayer.EventHandler（VideoPlayer.事件处理器）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(VideoPlayer source)`
  （void Invoke（Video玩家 source））
- `IAsyncResult BeginInvoke(VideoPlayer source, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Video玩家 source, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## VideoPlayer.FrameReadyEventHandler（VideoPlayer.FrameReady事件处理器）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(VideoPlayer source, long frameIdx)`
  （void Invoke（Video玩家 source, long frameIdx））
- `IAsyncResult BeginInvoke(VideoPlayer source, long frameIdx, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Video玩家 source, long frameIdx, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## VideoPlayer.TimeEventHandler（VideoPlayer.时间事件处理器）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(VideoPlayer source, double seconds)`
  （void Invoke（Video玩家 source, double seconds））
- `IAsyncResult BeginInvoke(VideoPlayer source, double seconds, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Video玩家 source, double seconds, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## VideoRenderMode（VideoRender模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## VideoSource（VideoSource）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## VideoTimeReference（Video时间引用）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## VideoTimeSource（Video时间Source）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Vignette（Vignette）

**继承**: VolumeComponent, IPostProcessComponent（体积组件, I后处理组件）

### 字段 (5)

- `ColorParameter color`（颜色Parameter color）(偏移: 0x1C)
- `Vector2Parameter center`（二维向量Parameter center）(偏移: 0x20)
- `ClampedFloatParameter intensity`（钳制浮点数参数 强度）(偏移: 0x24)
- `ClampedFloatParameter smoothness`（Clamped浮点数Parameter smoothness）(偏移: 0x28)
- `BoolParameter rounded`（布尔值Parameter rounded）(偏移: 0x2C)

### 方法 (2)

- `bool IsActive()`
  （布尔值 是否激活的（））
- `bool IsTileCompatible()`
  （布尔值 是否瓦片兼容（））

---

## VisibleLight（可见的光照）

**继承**: IEquatable<VisibleLight>（IEquatable<可见的Light>）

### 字段 (8)

- `LightType m_LightType`（光照类型 m_光照类型）(偏移: 0x0)
- `Color m_FinalColor`（颜色 m_Final颜色）(偏移: 0x4)
- `Rect m_ScreenRect`（Rect m_屏幕的Rect）(偏移: 0x14)
- `Matrix4x4 m_LocalToWorldMatrix`（Matrix4x4 m_本地的To世界的矩阵）(偏移: 0x24)
- `float m_Range`（float m_范围）(偏移: 0x64)
- `float m_SpotAngle`（float m_Spot角度）(偏移: 0x68)
- `int m_InstanceId`（int m_实例Id）(偏移: 0x6C)
- `VisibleLightFlags m_Flags`（可见的光照Flags m_Flags）(偏移: 0x70)

### 方法 (9)

- `Light get_light()`
  （光照 get_light（））
- `LightType get_lightType()`
  （光照类型 get_light类型（））
- `Color get_finalColor()`
  （颜色 get_final颜色（））
- `Matrix4x4 get_localToWorldMatrix()`
  （Matrix4x4 get_localTo世界的矩阵（））
- `float get_range()`
  （float get_range（））
- `float get_spotAngle()`
  （float get_spot角度（））
- `bool Equals(VisibleLight other)`
  （bool Equals（可见的光照 other））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## VisibleLightFlags（可见的光照Flags）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## VisibleReflectionProbe（可见的ReflectionProbe）

**继承**: IEquatable<VisibleReflectionProbe>（IEquatable<可见的ReflectionProbe>）

### 字段 (9)

- `Bounds m_Bounds`（Bounds m_Bounds）(偏移: 0x0)
- `Matrix4x4 m_LocalToWorldMatrix`（Matrix4x4 m_本地的To世界的矩阵）(偏移: 0x18)
- `Vector4 m_HdrData`（Vector4 m_Hdr数据）(偏移: 0x58)
- `Vector3 m_Center`（三维向量 m_中心）(偏移: 0x68)
- `float m_BlendDistance`（float m_Blend距离）(偏移: 0x74)
- `int m_Importance`（int m_Importance）(偏移: 0x78)
- `int m_BoxProjection`（int m_BoxProjection）(偏移: 0x7C)
- `int m_InstanceId`（int m_实例Id）(偏移: 0x80)
- `int m_TextureId`（int m_纹理Id）(偏移: 0x84)

### 方法 (3)

- `bool Equals(VisibleReflectionProbe other)`
  （bool Equals（可见的ReflectionProbe other））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## VisualEffect（Visual特效）

**继承**: Behaviour（行为）

### 字段 (2)

- `VFXEventAttribute m_cachedEventAttribute`（VFX事件Attribute m_cached事件Attribute）(偏移: 0xC)
- `Action<VFXOutputEventArgs> outputEventReceived`（Action<VFXOutput事件Args> output事件Received）(偏移: 0x10)

### 方法 (34)

- `VisualEffectAsset get_visualEffectAsset()`
  （Visual特效资产 get_visual特效资产（））
- `VFXEventAttribute CreateVFXEventAttribute()`
  （VFX事件Attribute 创建VFX事件Attribute（））
- `void CheckValidVFXEventAttribute(VFXEventAttribute eventAttribute)`
  （void 检查ValidVFX事件Attribute（VFX事件Attribute eventAttribute））
- `void SendEventFromScript(int eventNameID, VFXEventAttribute eventAttribute)`
  （void 发送事件FromScript（int eventNameID, VFX事件Attribute eventAttribute））
- `void SendEvent(int eventNameID, VFXEventAttribute eventAttribute)`
  （void 发送事件（int eventNameID, VFX事件Attribute eventAttribute））
- `void SendEvent(string eventName, VFXEventAttribute eventAttribute)`
  （void 发送事件（string eventName, VFX事件Attribute eventAttribute））
- `bool HasBool(int nameID)`
  （bool 是否有布尔值（int nameID））
- `bool HasInt(int nameID)`
  （bool 是否有整数（int nameID））
- `bool HasUInt(int nameID)`
  （bool 是否有U整数（int nameID））
- `bool HasFloat(int nameID)`
  （bool 是否有浮点数（int nameID））
- `bool HasVector3(int nameID)`
  （bool 是否有三维向量（int nameID））
- `bool HasVector4(int nameID)`
  （bool 是否有Vector4（int nameID））
- `bool HasTexture(int nameID)`
  （bool 是否有纹理（int nameID））
- `void SetBool(int nameID, bool b)`
  （void 集合布尔值（int nameID, bool b））
- `void SetInt(int nameID, int i)`
  （void 集合整数（int nameID, int i））
- `void SetUInt(int nameID, uint i)`
  （void 集合U整数（int nameID, uint i））
- `void SetFloat(int nameID, float f)`
  （void 集合浮点数（int nameID, float f））
- `void SetVector3(int nameID, Vector3 v)`
  （void 集合三维向量（int nameID, 三维向量 v））
- `void SetVector4(int nameID, Vector4 v)`
  （void 集合Vector4（int nameID, Vector4 v））
- `void SetTexture(int nameID, Texture t)`
  （void 集合纹理（int nameID, 纹理 t））
- `float GetFloat(int nameID)`
  （float 获取浮点数（int nameID））
- `bool HasUInt(string name)`
  （bool 是否有U整数（string name））
- `bool HasFloat(string name)`
  （bool 是否有浮点数（string name））
- `bool HasVector4(string name)`
  （bool 是否有Vector4（string name））
- `bool HasTexture(string name)`
  （bool 是否有纹理（string name））
- `void SetUInt(string name, uint i)`
  （void 集合U整数（string name, uint i））
- `void SetFloat(string name, float f)`
  （void 集合浮点数（string name, float f））
- `void SetVector4(string name, Vector4 v)`
  （void 集合Vector4（string name, Vector4 v））
- `void SetTexture(string name, Texture t)`
  （void 集合纹理（string name, 纹理 t））
- `void SetBool(string name, bool b)`
  （void 集合布尔值（string name, bool b））
- `VFXEventAttribute InvokeGetCachedEventAttributeForOutputEvent_Internal(VisualEffect source)`
  （VFX事件Attribute Invoke获取Cached事件AttributeForOutputEvent_内部的（Visual特效 source））
- `void InvokeOutputEventReceived_Internal(VisualEffect source, int eventNameId)`
  （void InvokeOutput事件Received_内部的（Visual特效 source, int eventNameId））
- `void SetVector3_Injected(int nameID, ref Vector3 v)`
  （void 集合Vector3_Injected（int nameID, ref Vector3 v））
- `void SetVector4_Injected(int nameID, ref Vector4 v)`
  （void 集合Vector4_Injected（int nameID, ref Vector4 v））

---

## VisualEffectActivationBehaviour（Visual特效ActivationBehaviour）

**继承**: PlayableBehaviour（可播放行为）

### 字段 (4)

- `ExposedProperty onClipEnter`（Exposed属性 on弹匣Enter）(偏移: 0x8)
- `ExposedProperty onClipExit`（Exposed属性 on弹匣Exit）(偏移: 0xC)
- `VisualEffectActivationBehaviour.EventState[] clipEnterEventAttributes`（Visual特效ActivationBehaviour.事件State[] clipEnter事件Attributes）(偏移: 0x10)
- `VisualEffectActivationBehaviour.EventState[] clipExitEventAttributes`（Visual特效ActivationBehaviour.事件State[] clipExit事件Attributes）(偏移: 0x14)

### 方法 (4)

- `void OnPlayableCreate(Playable playable)`
  （void OnPlayable创建（Playable playable））
- `void SendEventEnter(VisualEffect component)`
  （void 发送事件Enter（Visual特效 component））
- `void SendEventExit(VisualEffect component)`
  （void 发送事件Exit（Visual特效 component））
- `VFXEventAttribute BuildEventAttribute(VisualEffect component, VisualEffectActivationBehaviour.EventState[] states)`
  （VFX事件Attribute Build事件Attribute（Visual特效 component, Visual特效ActivationBehaviour.事件State[] states））

---

## VisualEffectActivationBehaviour.AttributeType（Visual特效ActivationBehaviour.Attribute类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## VisualEffectActivationBehaviour.EventState（Visual特效ActivationBehaviour.事件状态）

### 字段 (3)

- `ExposedProperty attribute`（Exposed属性 attribute）(偏移: 0x0)
- `VisualEffectActivationBehaviour.AttributeType type`（Visual特效ActivationBehaviour.Attribute类型 type）(偏移: 0x4)
- `float[] values`（float[] values）(偏移: 0x8)

---

## VisualEffectActivationClip（Visual特效Activation弹匣）

**继承**: PlayableAsset, ITimelineClipAsset（Playable资产, ITimeline弹匣资产）

### 字段 (1)

- `VisualEffectActivationBehaviour activationBehavior`（Visual特效ActivationBehaviour activationBehavior）(偏移: 0xC)

### 方法 (2)

- `ClipCaps get_clipCaps()`
  （弹匣Caps 获取_弹匣Caps（））
- `Playable CreatePlayable(PlayableGraph graph, GameObject owner)`
  （Playable 创建Playable（PlayableGraph graph, 游戏对象 owner））

---

## VisualEffectActivationMixerBehaviour（Visual特效ActivationMixerBehaviour）

**继承**: PlayableBehaviour（可播放行为）

### 字段 (1)

- `bool[] enabledStates`（bool[] enabledStates）(偏移: 0x8)

### 方法 (3)

- `void ProcessFrame(Playable playable, FrameData info, object playerData)`
  （void 处理Frame（Playable playable, Frame数据 info, object playerData））
- `void OnPlayableCreate(Playable playable)`
  （void OnPlayable创建（Playable playable））
- `void OnPlayableDestroy(Playable playable)`
  （void OnPlayable销毁（Playable playable））

---

## VisualEffectActivationTrack（Visual特效ActivationTrack）

**继承**: TrackAsset（轨道资产）

### 方法 (1)

- `Playable CreateTrackMixer(PlayableGraph graph, GameObject go, int inputCount)`
  （Playable 创建TrackMixer（PlayableGraph graph, 游戏对象 go, int inputCount））

---

## VisualEffectAsset（Visual特效资产）

**继承**: VisualEffectObject（Visual特效对象）

### 字段 (2)

- `int PlayEventID`（int 播放事件ID）(偏移: 0x0)
- `int StopEventID`（int 停止事件ID）(偏移: 0x4)

---

## VoiceFileRename（Voice文件Rename）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (1)

- `string voiceName`（string voice名称）(偏移: 0xC)

### 方法 (3)

- `void Update()`
  （void 更新（））
- `void Rename(string targetPath)`
  （void Rename（string targetPath））
- `void TryRename(FileInfo fileInfo)`
  （void TryRename（文件信息 fileInfo））

---

## Volatile（Volatile）

### 方法 (1)

- `bool Read(ref bool location)`
  （bool Read（ref bool location））

---

## Volume（Volume）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (8)

- `bool isGlobal`（bool is全局的）(偏移: 0xC)
- `float priority`（float priority）(偏移: 0x10)
- `float blendDistance`（float blend距离）(偏移: 0x14)
- `float weight`（浮点数 权重）(偏移: 0x18)
- `VolumeProfile sharedProfile`（VolumeProfile sharedProfile）(偏移: 0x1C)
- `int m_PreviousLayer`（int m_上一个层）(偏移: 0x20)
- `float m_PreviousPriority`（float m_上一个Priority）(偏移: 0x24)
- `VolumeProfile m_InternalProfile`（VolumeProfile m_内部的Profile）(偏移: 0x28)

### 方法 (8)

- `VolumeProfile get_profile()`
  （VolumeProfile get_profile（））
- `void set_profile(VolumeProfile value)`
  （void set_profile（VolumeProfile value））
- `VolumeProfile get_profileRef()`
  （VolumeProfile get_profileRef（））
- `bool HasInstantiatedProfile()`
  （bool 是否有InstantiatedProfile（））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `void Update()`
  （void 更新（））
- `void UpdateLayer()`
  （void 更新层（））

---

## VolumeComponent（Volume组件）

**继承**: ScriptableObject（脚本对象）

### 字段 (2)

- `bool active`（bool active）(偏移: 0xC)
- `bool m_AdvancedMode`（bool m_Advanced模式）(偏移: 0x18)

### 方法 (13)

- `string get_displayName()`
  （string get_display名称（））
- `void set_displayName(string value)`
  （void set_display名称（string value））
- `ReadOnlyCollection<VolumeParameter> get_parameters()`
  （ReadOnlyCollection<VolumeParameter> get_parameters（））
- `void set_parameters(ReadOnlyCollection<VolumeParameter> value)`
  （void set_parameters（ReadOnlyCollection<VolumeParameter> value））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `void Override(VolumeComponent state, float interpFactor)`
  （void 重写（Volume组件 state, float interpFactor））
- `void SetAllOverridesTo(bool state)`
  （void 集合所有OverridesTo（bool state））
- `void SetAllOverridesTo(IEnumerable<VolumeParameter> enumerable, bool state)`
  （void 集合所有OverridesTo（IEnumerable<VolumeParameter> enumerable, bool state））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `bool AnyPropertiesIsOverridden()`
  （bool 任意Properties是否Overridden（））
- `void OnDestroy()`
  （void 销毁时（））
- `void Release()`
  （void 释放（））

---

## VolumeComponentMenu（Volume组件菜单）

**继承**: Attribute（属性）

### 字段 (1)

- `string menu`（string menu）(偏移: 0x8)

---

## VolumeFrameworkUpdateMode（VolumeFramework更新模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## VolumeManager（Volume管理器）

### 字段 (5)

- `Lazy<VolumeManager> s_Instance`（Lazy<VolumeManager> s_实例）(偏移: 0x0)
- `List<Volume> m_Volumes`（List<Volume> m_Volumes）(偏移: 0x14)
- `List<VolumeComponent> m_ComponentsDefaultState`（List<VolumeComponent> m_Components默认的状态）(偏移: 0x1C)
- `List<Collider> m_TempColliders`（List<Collider> m_TempColliders）(偏移: 0x20)
- `VolumeStack m_DefaultStack`（Volume栈 m_默认的栈）(偏移: 0x24)

### 方法 (25)

- `VolumeManager get_instance()`
  （Volume管理器 get_instance（））
- `VolumeStack get_stack()`
  （Volume栈 get_stack（））
- `void set_stack(VolumeStack value)`
  （void set_stack（Volume栈 value））
- `IEnumerable<Type> get_baseComponentTypes()`
  （IEnumerable<Type> get_base组件Types（））
- `void set_baseComponentTypes(IEnumerable<Type> value)`
  （void set_base组件Types（IEnumerable<Type> value））
- `Type[] get_baseComponentTypeArray()`
  （Type[] get_base组件类型数组（））
- `void set_baseComponentTypeArray(Type[] value)`
  （void set_base组件类型数组（Type[] value））
- `VolumeStack CreateStack()`
  （Volume栈 创建栈（））
- `void ResetMainStack()`
  （void 重置主要的栈（））
- `void DestroyStack(VolumeStack stack)`
  （void 销毁栈（Volume栈 stack））
- `void ReloadBaseTypes()`
  （void 换弹基础Types（））
- `void Register(Volume volume, int layer)`
  （void Register（Volume volume, int layer））
- `void Unregister(Volume volume, int layer)`
  （void Unregister（Volume volume, int layer））
- `void SetLayerDirty(int layer)`
  （void 集合层Dirty（int layer））
- `void UpdateVolumeLayer(Volume volume, int prevLayer, int newLayer)`
  （void 更新Volume层（Volume volume, int prevLayer, int newLayer））
- `void OverrideData(VolumeStack stack, List<VolumeComponent> components, float interpFactor)`
  （void 重写数据（Volume栈 stack, List<VolumeComponent> components, float interpFactor））
- `void ReplaceData(VolumeStack stack, List<VolumeComponent> components)`
  （void Replace数据（Volume栈 stack, List<VolumeComponent> components））
- `void CheckBaseTypes()`
  （void 检查基础Types（））
- `void CheckStack(VolumeStack stack)`
  （void 检查栈（Volume栈 stack））
- `void Update(Transform trigger, LayerMask layerMask)`
  （void 更新（变换 trigger, 层掩码 layerMask））
- `void Update(VolumeStack stack, Transform trigger, LayerMask layerMask)`
  （void 更新（Volume栈 stack, 变换 trigger, 层掩码 layerMask））
- `Volume[] GetVolumes(LayerMask layerMask)`
  （Volume[] 获取Volumes（层掩码 layerMask））
- `List<Volume> GrabVolumes(LayerMask mask)`
  （List<Volume> GrabVolumes（层掩码 mask））
- `void SortByPriority(List<Volume> volumes)`
  （void SortByPriority（List<Volume> volumes））
- `bool IsVolumeRenderedByCamera(Volume volume, Camera camera)`
  （bool 是否VolumeRenderedBy摄像机（Volume volume, 摄像机 camera））

---

## VolumeParameter（VolumeParameter）

### 字段 (1)

- `bool m_OverrideState`（bool m_重写状态）(偏移: 0x8)

### 方法 (6)

- `bool get_overrideState()`
  （bool get_override状态（））
- `void set_overrideState(bool value)`
  （void set_override状态（bool value））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `bool IsObjectParameter(Type type)`
  （bool 是否对象Parameter（类型 type））
- `void Release()`
  （void 释放（））

---

## VolumeProfile（VolumeProfile）

**继承**: ScriptableObject（脚本对象）

### 字段 (2)

- `List<VolumeComponent> components`（List<VolumeComponent> components）(偏移: 0xC)
- `bool isDirty`（bool isDirty）(偏移: 0x10)

### 方法 (9)

- `void OnEnable()`
  （void 启用时（））
- `void Reset()`
  （void 重置（））
- `VolumeComponent Add(Type type, bool overrides = False)`
  （Volume组件 添加（类型 type, bool overrides = False））
- `void Remove(Type type)`
  （void 移除（类型 type））
- `bool Has(Type type)`
  （bool 是否有（类型 type））
- `bool HasSubclassOf(Type type)`
  （bool 是否有SubclassOf（类型 type））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `int GetComponentListHashCode()`
  （int 获取组件列表HashCode（））
- `void Sanitize()`
  （void Sanitize（））

---

## VolumeStack（Volume栈）

**继承**: IDisposable（可释放接口）

### 方法 (3)

- `void Reload(Type[] baseTypes)`
  （void 换弹（Type[] baseTypes））
- `VolumeComponent GetComponent(Type type)`
  （Volume组件 获取组件（类型 type））
- `void Dispose()`
  （void 释放（））

---

## VoxelArea（VoxelArea）

### 字段 (17)

- `int width`（整数 宽度）(偏移: 0x8)
- `int depth`（整数 深度）(偏移: 0xC)
- `CompactVoxelSpan[] compactSpans`（CompactVoxelSpan[] compactSpans）(偏移: 0x10)
- `CompactVoxelCell[] compactCells`（CompactVoxelCell[] compactCells）(偏移: 0x14)
- `int compactSpanCount`（int compactSpan数量）(偏移: 0x18)
- `ushort[] tmpUShortArr`（ushort[] tmpUShortArr）(偏移: 0x1C)
- `int[] areaTypes`（int[] areaTypes）(偏移: 0x20)
- `ushort[] dist`（ushort[] dist）(偏移: 0x24)
- `ushort maxDistance`（ushort max距离）(偏移: 0x28)
- `int maxRegions`（int maxRegions）(偏移: 0x2C)
- `int[] DirectionX`（int[] 方向X）(偏移: 0x30)
- `int[] DirectionZ`（int[] 方向Z）(偏移: 0x34)
- `Vector3[] VectorDirection`（Vector3[] 向量方向）(偏移: 0x38)
- `int linkedSpanCount`（int linkedSpan数量）(偏移: 0x3C)
- `LinkedVoxelSpan[] linkedSpans`（LinkedVoxelSpan[] linkedSpans）(偏移: 0x40)
- `int[] removedStack`（int[] removed栈）(偏移: 0x44)
- `int removedStackCount`（int removed栈数量）(偏移: 0x48)

### 方法 (6)

- `void Reset()`
  （void 重置（））
- `void ResetLinkedVoxelSpans()`
  （void 重置LinkedVoxelSpans（））
- `int GetSpanCountAll()`
  （int 获取Span数量所有（））
- `int GetSpanCount()`
  （int 获取Span数量（））
- `void PushToSpanRemovedStack(int index)`
  （void PushToSpanRemoved栈（int index））
- `void AddLinkedSpan(int index, uint bottom, uint top, int area, int voxelWalkableClimb)`
  （void 添加LinkedSpan（int index, uint bottom, uint top, int area, int voxelWalkableClimb））

---

## VoxelCell（VoxelCell）

### 字段 (1)

- `VoxelSpan firstSpan`（VoxelSpan firstSpan）(偏移: 0x0)

### 方法 (1)

- `void AddSpan(uint bottom, uint top, int area, int voxelWalkableClimb)`
  （void 添加Span（uint bottom, uint top, int area, int voxelWalkableClimb））

---

## VoxelContour（VoxelContour）

### 字段 (5)

- `int nverts`（int nverts）(偏移: 0x0)
- `int[] verts`（int[] verts）(偏移: 0x4)
- `int[] rverts`（int[] rverts）(偏移: 0x8)
- `int reg`（int reg）(偏移: 0xC)
- `int area`（整数 面积）(偏移: 0x10)

---

## VoxelContourSet（VoxelContour集合）

### 字段 (2)

- `List<VoxelContour> conts`（List<VoxelContour> conts）(偏移: 0x8)
- `Bounds bounds`（边界 bounds）(偏移: 0xC)

---

## VoxelMesh（Voxel网格）

### 字段 (3)

- `Int3[] verts`（Int3[] verts）(偏移: 0x0)
- `int[] tris`（整数[] 三角形）(偏移: 0x4)
- `int[] areas`（int[] areas）(偏移: 0x8)

---

## VoxelPolygonClipper（VoxelPolygonClipper）

### 字段 (4)

- `float[] x`（float[] x）(偏移: 0x0)
- `float[] y`（float[] y）(偏移: 0x4)
- `float[] z`（float[] z）(偏移: 0x8)
- `int n`（int n）(偏移: 0xC)

### 方法 (4)

- `void set_Item(int i, Vector3 value)`
  （void set_项目（int i, 三维向量 value））
- `void ClipPolygonAlongX(ref VoxelPolygonClipper result, float multi, float offset)`
  （void 弹匣PolygonAlongX（ref VoxelPolygonClipper result, float multi, float offset））
- `void ClipPolygonAlongZWithYZ(ref VoxelPolygonClipper result, float multi, float offset)`
  （void 弹匣PolygonAlongZWithYZ（ref VoxelPolygonClipper result, float multi, float offset））
- `void ClipPolygonAlongZWithY(ref VoxelPolygonClipper result, float multi, float offset)`
  （void 弹匣PolygonAlongZWithY（ref VoxelPolygonClipper result, float multi, float offset））

---

## VoxelSpan（VoxelSpan）

### 字段 (4)

- `uint bottom`（uint bottom）(偏移: 0x8)
- `uint top`（uint top）(偏移: 0xC)
- `VoxelSpan next`（VoxelSpan next）(偏移: 0x10)
- `int area`（整数 面积）(偏移: 0x14)

---

## Voxelize（Voxelize）

### 字段 (18)

- `List<RasterizationMesh> inputMeshes`（List<RasterizationMesh> inputMeshes）(偏移: 0x8)
- `int voxelWalkableClimb`（int voxelWalkable攀爬）(偏移: 0xC)
- `uint voxelWalkableHeight`（uint voxelWalkable高度）(偏移: 0x10)
- `float cellSize`（float cell大小）(偏移: 0x14)
- `float cellHeight`（float cell高度）(偏移: 0x18)
- `int minRegionSize`（int minRegion大小）(偏移: 0x1C)
- `int borderSize`（int border大小）(偏移: 0x20)
- `float maxEdgeLength`（float maxEdgeLength）(偏移: 0x24)
- `float maxSlope`（float maxSlope）(偏移: 0x28)
- `RecastGraph.RelevantGraphSurfaceMode relevantGraphSurfaceMode`（RecastGraph.RelevantGraphSurface模式 relevantGraphSurface模式）(偏移: 0x2C)
- `Bounds forcedBounds`（Bounds forcedBounds）(偏移: 0x30)
- `VoxelArea voxelArea`（VoxelArea voxelArea）(偏移: 0x48)
- `VoxelContourSet countourSet`（VoxelContour集合 countour集合）(偏移: 0x4C)
- `GraphTransform transform`（Graph变换 transform）(偏移: 0x50)
- `int width`（整数 宽度）(偏移: 0x58)
- `int depth`（整数 深度）(偏移: 0x5C)
- `Vector3 voxelOffset`（三维向量 voxelOffset）(偏移: 0x60)
- `Vector3 cellScale`（三维向量 cell缩放）(偏移: 0x6C)

### 方法 (53)

- `void BuildContours(float maxError, int maxEdgeLength, VoxelContourSet cset, int buildFlags)`
  （void BuildContours（float maxError, int maxEdgeLength, VoxelContour集合 cset, int buildFlags））
- `void GetClosestIndices(int[] vertsa, int nvertsa, int[] vertsb, int nvertsb, ref int ia, ref int ib)`
  （void 获取ClosestIndices（int[] vertsa, int nvertsa, int[] vertsb, int nvertsb, ref int ia, ref int ib））
- `void ReleaseContours(VoxelContourSet cset)`
  （void ReleaseContours（VoxelContour集合 cset））
- `bool MergeContours(ref VoxelContour ca, ref VoxelContour cb, int ia, int ib)`
  （bool MergeContours（ref VoxelContour ca, ref VoxelContour cb, int ia, int ib））
- `void SimplifyContour(List<int> verts, List<int> simplified, float maxError, int maxEdgeLenght, int buildFlags)`
  （void SimplifyContour（List<int> verts, List<int> simplified, float maxError, int maxEdgeLenght, int buildFlags））
- `void WalkContour(int x, int z, int i, ushort[] flags, List<int> verts)`
  （void WalkContour（int x, int z, int i, ushort[] flags, List<int> verts））
- `int GetCornerHeight(int x, int z, int i, int dir, ref bool isBorderVertex)`
  （int 获取Corner高度（int x, int z, int i, int dir, ref bool isBorderVertex））
- `void RemoveDegenerateSegments(List<int> simplified)`
  （void 移除DegenerateSegments（List<int> simplified））
- `int CalcAreaOfPolygon2D(int[] verts, int nverts)`
  （int CalcAreaOfPolygon2D（int[] verts, int nverts））
- `bool Ileft(int a, int b, int c, int[] va, int[] vb, int[] vc)`
  （bool Ileft（int a, int b, int c, int[] va, int[] vb, int[] vc））
- `bool Diagonal(int i, int j, int n, int[] verts, int[] indices)`
  （bool Diagonal（int i, int j, int n, int[] verts, int[] indices））
- `bool InCone(int i, int j, int n, int[] verts, int[] indices)`
  （bool InCone（int i, int j, int n, int[] verts, int[] indices））
- `bool Left(int a, int b, int c, int[] verts)`
  （bool 左（int a, int b, int c, int[] verts））
- `bool LeftOn(int a, int b, int c, int[] verts)`
  （bool 左On（int a, int b, int c, int[] verts））
- `bool Collinear(int a, int b, int c, int[] verts)`
  （bool Collinear（int a, int b, int c, int[] verts））
- `int Area2(int a, int b, int c, int[] verts)`
  （int Area2（int a, int b, int c, int[] verts））
- `bool Diagonalie(int i, int j, int n, int[] verts, int[] indices)`
  （bool Diagonalie（int i, int j, int n, int[] verts, int[] indices））
- `bool Xorb(bool x, bool y)`
  （bool Xorb（bool x, bool y））
- `bool IntersectProp(int a, int b, int c, int d, int[] verts)`
  （bool IntersectProp（int a, int b, int c, int d, int[] verts））
- `bool Between(int a, int b, int c, int[] verts)`
  （bool Between（int a, int b, int c, int[] verts））
- `bool Intersect(int a, int b, int c, int d, int[] verts)`
  （bool Intersect（int a, int b, int c, int d, int[] verts））
- `bool Vequal(int a, int b, int[] verts)`
  （bool Vequal（int a, int b, int[] verts））
- `int Prev(int i, int n)`
  （int Prev（int i, int n））
- `int Next(int i, int n)`
  （int 下一个（int i, int n））
- `void BuildPolyMesh(VoxelContourSet cset, int nvp, out VoxelMesh mesh)`
  （void BuildPoly网格（VoxelContour集合 cset, int nvp, out VoxelMesh mesh））
- `int Triangulate(int n, int[] verts, ref int[] indices, ref int[] tris)`
  （int Triangulate（int n, int[] verts, ref int[] indices, ref int[] tris））
- `GraphTransform get_transformVoxel2Graph()`
  （Graph变换 get_transformVoxel2Graph（））
- `void set_transformVoxel2Graph(GraphTransform value)`
  （void set_transformVoxel2Graph（Graph变换 value））
- `Vector3 CompactSpanToVector(int x, int z, int i)`
  （三维向量 CompactSpanTo向量（int x, int z, int i））
- `void VectorToIndex(Vector3 p, out int x, out int z)`
  （void 向量To索引（三维向量 p, out int x, out int z））
- `void Init()`
  （void 初始化（））
- `void VoxelizeInput(GraphTransform graphTransform, Bounds graphSpaceBounds)`
  （void Voxelize输入（Graph变换 graphTransform, Bounds graphSpaceBounds））
- `void DebugDrawSpans()`
  （void DebugDrawSpans（））
- `void BuildCompactField()`
  （void BuildCompactField（））
- `void BuildVoxelConnections()`
  （void BuildVoxelConnections（））
- `void DrawLine(int a, int b, int[] indices, int[] verts, Color color)`
  （void DrawLine（int a, int b, int[] indices, int[] verts, 颜色 color））
- `Vector3 VoxelToWorld(int x, int y, int z)`
  （三维向量 VoxelTo世界的（int x, int y, int z））
- `Int3 VoxelToWorldInt3(Int3 voxelPosition)`
  （Int3 VoxelTo世界的Int3（Int3 voxelPosition））
- `Vector3 ConvertPosWithoutOffset(int x, int y, int z)`
  （三维向量 转换PosWithoutOffset（int x, int y, int z））
- `Vector3 ConvertPosition(int x, int z, int i)`
  （三维向量 转换Position（int x, int z, int i））
- `void ErodeWalkableArea(int radius)`
  （void ErodeWalkableArea（int radius））
- `void BuildDistanceField()`
  （void Build距离Field（））
- `void ErodeVoxels(int radius)`
  （void ErodeVoxels（int radius））
- `void FilterLowHeightSpans(uint voxelWalkableHeight, float cs, float ch)`
  （void FilterLow高度Spans（uint voxelWalkableHeight, float cs, float ch））
- `void FilterLedges(uint voxelWalkableHeight, int voxelWalkableClimb, float cs, float ch)`
  （void FilterLedges（uint voxelWalkableHeight, int voxelWalkableClimb, float cs, float ch））
- `bool FloodRegion(int x, int z, int i, uint level, ushort r, ushort[] srcReg, ushort[] srcDist, Int3[] stack, int[] flags, bool[] closed)`
  （bool FloodRegion（int x, int z, int i, uint level, ushort r, ushort[] srcReg, ushort[] srcDist, Int3[] stack, int[] flags, bool[] closed））
- `void MarkRectWithRegion(int minx, int maxx, int minz, int maxz, ushort region, ushort[] srcReg)`
  （void MarkRectWithRegion（int minx, int maxx, int minz, int maxz, ushort region, ushort[] srcReg））
- `ushort CalculateDistanceField(ushort[] src)`
  （ushort 计算距离Field（ushort[] src））
- `ushort[] BoxBlur(ushort[] src, ushort[] dst)`
  （ushort[] BoxBlur（ushort[] src, ushort[] dst））
- `void BuildRegions()`
  （void BuildRegions（））
- `int union_find_find(int[] arr, int x)`
  （int union_find_find（int[] arr, int x））
- `void union_find_union(int[] arr, int a, int b)`
  （void union_find_union（int[] arr, int a, int b））
- `void FilterSmallRegions(ushort[] reg, int minRegionSize, int maxRegions)`
  （void FilterSmallRegions（ushort[] reg, int minRegionSize, int maxRegions））

---

## WD_AsceticHero（WD_Ascetic英雄）

**继承**: WD_SkillKnife（WD_技能近战武器）

### 字段 (6)

- `GameObject screenFX`（游戏对象 screenFX）(偏移: 0xF8)
- `GameObject FX_ShieldStart`（游戏对象 FX_Shield开始）(偏移: 0xFC)
- `GameObject FX_Shield1`（游戏对象 FX_Shield1）(偏移: 0x100)
- `GameObject FX_Shield2`（游戏对象 FX_Shield2）(偏移: 0x104)
- `GameObject FX_Explosion`（游戏对象 FX_Explosion）(偏移: 0x108)
- `AudioClip SND_ShieldStart`（音频弹匣 SND_Shield开始）(偏移: 0x10C)

---

## WD_EvilTerminator（WD_EvilTerminator）

**继承**: WD_SkillKnife, IMissileGetter（WD_技能近战武器, IMissileGetter）

### 字段 (4)

- `MissileData missileData`（Missile数据 missile数据）(偏移: 0xF8)
- `GameObject gauge`（游戏对象 gauge）(偏移: 0x124)
- `GameObject FX_Power_3rd`（游戏对象 FX_Power_3rd）(偏移: 0x128)
- `GameObject FX_Power_PV`（游戏对象 FX_Power_PV）(偏移: 0x12C)

### 方法 (1)

- `MissileData GetMissileData()`
  （Missile数据 获取Missile数据（））

---

## WD_GhostBlade（WD_幽灵刀锋）

**继承**: WeaponData_Knife（WeaponData_近战武器）

### 字段 (3)

- `string btlModeWpnName`（string btl模式武器名称）(偏移: 0xF4)
- `CharWpnAnimData btlModeCharAnimData`（Char武器动画数据 btl模式Char动画数据）(偏移: 0xF8)
- `GameObject skillBtn`（游戏对象 skillBtn）(偏移: 0x104)

### 方法 (1)

- `string GetWeaponName(int index)`
  （string 获取Weapon名称（int index））

---

## WD_GrenadeGun（WD_手雷枪械）

**继承**: WeaponData_Gun, IMissileGetter（WeaponData_枪械, IMissileGetter）

### 字段 (5)

- `string weaponName2`（string weaponName2）(偏移: 0x1C8)
- `WpnSpriteAsset spriteAsset2`（武器精灵资产 spriteAsset2）(偏移: 0x1CC)
- `CharWpnAnimData charWpnAnim2`（Char武器动画数据 char武器Anim2）(偏移: 0x1FC)
- `string shotSoundName2`（string shot音效Name2）(偏移: 0x208)
- `MissileData missileData`（Missile数据 missile数据）(偏移: 0x20C)

### 方法 (5)

- `bool get_haveGMcharAnim()`
  （bool get_haveGMchar动画（））
- `string GetWeaponName(int index)`
  （string 获取Weapon名称（int index））
- `Sprite GetKillMsgIcon(int index)`
  （精灵 获取击杀Msg图标（int index））
- `bool GetWeaponSelectImage(int index, out Texture img1, out Texture img2)`
  （bool 获取Weapon选择图像（int index, out Texture img1, out Texture img2））
- `MissileData GetMissileData()`
  （Missile数据 获取Missile数据（））

---

## WD_MasterHero（WD_Master英雄）

**继承**: WD_SkillKnife（WD_技能近战武器）

### 字段 (3)

- `string skillHitSndName`（string skill命中Snd名称）(偏移: 0xF8)
- `string skillHitEffectName`（string skill命中特效名称）(偏移: 0xFC)
- `GameObject debuffEffect`（游戏对象 debuff特效）(偏移: 0x100)

---

## WD_MasterHunter（WD_MasterHunter）

**继承**: WD_SkillKnife（WD_技能近战武器）

### 字段 (3)

- `GameObject FX_PV`（游戏对象 FX_PV）(偏移: 0xF8)
- `GameObject FX_Start`（游戏对象 FX_开始）(偏移: 0xFC)
- `GameObject FX_End`（游戏对象 FX_结束）(偏移: 0x100)

---

## WD_MechanicHero（WD_Mechanic英雄）

**继承**: WeaponData_Knife（WeaponData_近战武器）

### 字段 (2)

- `GameObject SkillBtn_Arcane`（游戏对象 技能Btn_Arcane）(偏移: 0xF4)
- `GameObject SkillBtn_SentryGun`（游戏对象 技能Btn_Sentry枪械）(偏移: 0xF8)

---

## WD_Missile（WD_Missile）

**继承**: WeaponData, IMissileGetter（武器数据, IMissileGetter）

### 字段 (1)

- `MissileData missileData`（Missile数据 missile数据）(偏移: 0xB8)

### 方法 (1)

- `MissileData GetMissileData()`
  （Missile数据 获取Missile数据（））

---

## WD_RPG（WD_RPG）

**继承**: WeaponData, IMissileGetter（武器数据, IMissileGetter）

### 字段 (5)

- `MissileData missileData`（Missile数据 missile数据）(偏移: 0xB8)
- `bool isGrenadeGun`（bool is手雷枪械）(偏移: 0xE4)
- `string shotSoundName`（string shot音效名称）(偏移: 0xE8)
- `float reloadAnimRate`（float reload动画Rate）(偏移: 0xEC)
- `float fireAnimRate`（float fire动画Rate）(偏移: 0xF0)

### 方法 (1)

- `MissileData GetMissileData()`
  （Missile数据 获取Missile数据（））

---

## WD_SentryGun（WD_Sentry枪械）

**继承**: WeaponData（武器数据）

### 字段 (8)

- `GameObject sentryGunPrefab`（游戏对象 sentry枪械预制体）(偏移: 0xB8)
- `AudioClip SND_Exp`（音频弹匣 SND_Exp）(偏移: 0xBC)
- `AudioClip SND_Fire`（音频弹匣 SND_开火）(偏移: 0xC0)
- `AudioClip SND_PostFire`（音频弹匣 SND_Post开火）(偏移: 0xC4)
- `AudioClip SND_Idle`（音频弹匣 SND_待机）(偏移: 0xC8)
- `AudioClip SND_Hit`（音频弹匣 SND_命中）(偏移: 0xCC)
- `string GVshotAnimName`（string GVshot动画名称）(偏移: 0xD0)
- `GameObject HealthBar`（游戏对象 HealthBar）(偏移: 0xD4)

---

## WD_SkillKnife（WD_技能近战武器）

**继承**: WeaponData_Knife, ISkillBtnGetter（WeaponData_近战武器, I技能BtnGetter）

### 字段 (1)

- `GameObject skillBtn`（游戏对象 skillBtn）(偏移: 0xF4)

### 方法 (2)

- `GameObject GetSkillBtn(int index)`
  （游戏对象 获取技能Btn（int index））
- `Sprite GetKillMsgIcon(int index)`
  （精灵 获取击杀Msg图标（int index））

---

## WD_VoidTerminator（WD_VoidTerminator）

**继承**: WeaponData_Knife（WeaponData_近战武器）

### 字段 (2)

- `GameObject skillBtn_Set`（游戏对象 skillBtn_集合）(偏移: 0xF4)
- `GameObject skillBtn_TP`（游戏对象 skillBtn_TP）(偏移: 0xF8)

---

## WPN_Arcane（WPN_Arcane）

**继承**: Weapon（武器）

### 方法 (6)

- `WD_Missile get_realData()`
  （WD_Missile get_real数据（））
- `void Init()`
  （void 初始化（））
- `void OnAnimationEnd(string animName, string animTag)`
  （void 动画结束时（字符串 animName, 字符串 animTag））
- `void UnDeploy(bool temporary = False)`
  （void 取消部署（布尔值 临时 = 假））
- `void Throw()`
  （void 投掷（））
- `bool GiveUp(bool death = True)`
  （布尔值 放弃（布尔值 死亡 = 真））

---

## WPN_ArmoredTerminator（WPN_ArmoredTerminator）

**继承**: WPN_Knife（WPN_近战武器）

### 字段 (5)

- `Skill_Common skill`（通用技能 skill）(偏移: 0xF0)
- `GameObject skillBtn`（游戏对象 skillBtn）(偏移: 0xF4)
- `GameObject effect`（游戏对象 特效）(偏移: 0xF8)
- `GameObject fearSign`（游戏对象 fear标志）(偏移: 0xFC)
- `float threatenRange`（float threaten范围）(偏移: 0x0)

### 方法 (9)

- `void SetValidOwner()`
  （void 设置有效所有者（））
- `void RemoveFromOldOwner()`
  （void 从旧所有者移除（））
- `void Deploy(bool noSelectAnim = False)`
  （void 部署（布尔值 无选择动画 = 假））
- `bool Cry(Player player)`
  （bool Cry（玩家 player））
- `void OnAnimationEnd(string animName, string animTag)`
  （void 动画结束时（字符串 animName, 字符串 animTag））
- `void CryTrigger()`
  （void Cry触发器（））
- `void Overlap(Action<Player> func)`
  （void Overlap（Action<Player> func））
- `void AddSlowDebuf(Player target)`
  （void 添加SlowDebuf（玩家 target））
- `void Threaten(Player target)`
  （void Threaten（玩家 target））

---

## WPN_AsceticHero（WPN_Ascetic英雄）

**继承**: WPN_Knife（WPN_近战武器）

### 字段 (5)

- `WD_AsceticHero realData2`（WD_Ascetic英雄 realData2）(偏移: 0xF0)
- `Skill_Common skill`（通用技能 skill）(偏移: 0xF4)
- `bool comboFinishTag`（bool comboFinish标签）(偏移: 0xF8)
- `int shieldHealth`（int shieldHealth）(偏移: 0xFC)
- `RecyclableObject shieldSound`（Recyclable对象 shield音效）(偏移: 0x100)

### 方法 (12)

- `void Init()`
  （void 初始化（））
- `void PostCalDamage(ref DamageEventData data)`
  （void PostCal伤害（ref DamageEventData data））
- `void Update()`
  （void 更新（））
- `void OnAnimationEnter(string animName, string animTag)`
  （void On动画Enter（string animName, string animTag））
- `void OnKnifeAttackAnimEnd(string animName)`
  （void On近战武器Attack动画结束（string animName））
- `void FinishCombo()`
  （void FinishCombo（））
- `void Deploy(bool noSelectAnim = False)`
  （void 部署（布尔值 无选择动画 = 假））
- `void UnDeploy(bool temporary = False)`
  （void 取消部署（布尔值 临时 = 假））
- `bool AsceticHeroSkill(Player player)`
  （bool Ascetic英雄技能（玩家 player））
- `void Shield2()`
  （void Shield2（））
- `void ShieldBlast()`
  （void ShieldBlast（））
- `BotSkillBase SkillAI_AsceticHero(Bot bot)`
  （机器人技能基础 技能AI_Ascetic英雄（机器人 bot））

---

## WPN_BoxingKing（WPN_BoxingKing）

**继承**: WPN_Knife（WPN_近战武器）

### 字段 (6)

- `float landCheckStartTime`（float land检查开始时间）(偏移: 0xF0)
- `Skill_Common kickSkill`（Skill_Common kick技能）(偏移: 0xF4)
- `Skill_Common rotateSkill`（Skill_Common rotate技能）(偏移: 0xF8)
- `Skill_Common flySkill`（Skill_Common fly技能）(偏移: 0xFC)
- `bool isRotating`（bool isRotating）(偏移: 0x100)
- `bool isFlying`（bool isFlying）(偏移: 0x101)

### 方法 (8)

- `void Init()`
  （void 初始化（））
- `void SetValidOwner()`
  （void 设置有效所有者（））
- `void RemoveFromOldOwner()`
  （void 从旧所有者移除（））
- `void Deploy(bool noSelectAnim = False)`
  （void 部署（布尔值 无选择动画 = 假））
- `void Update()`
  （void 更新（））
- `bool Kick(Player player)`
  （bool Kick（玩家 player））
- `bool Rotate(Player player)`
  （bool Rotate（玩家 player））
- `bool Fly(Player player)`
  （bool Fly（玩家 player））

---

## WPN_Disposable（WPN_Disposable）

**继承**: Weapon（武器）

### 方法 (7)

- `void Update()`
  （void 更新（））
- `void Deploy(bool noSelectAnim = False)`
  （void 部署（布尔值 无选择动画 = 假））
- `void UnDeploy(bool temporary = False)`
  （void 取消部署（布尔值 临时 = 假））
- `void AnimSpeedSetting()`
  （void 动画速度设置（））
- `void OnAnimExit()`
  （void On动画Exit（））
- `bool GiveUp(bool death = True)`
  （布尔值 放弃（布尔值 死亡 = 真））
- `void BotControl(Bot bot)`
  （void 机器人控制（机器人 bot））

---

## WPN_EvilTerminator（WPN_EvilTerminator）

**继承**: WPN_Knife（WPN_近战武器）

### 字段 (8)

- `WD_EvilTerminator realData2`（WD_EvilTerminator realData2）(偏移: 0xF0)
- `Skill_Common skill`（通用技能 skill）(偏移: 0xF4)
- `float startPowerTime`（float start力度时间）(偏移: 0xF8)
- `float powerProgress`（float powerProgress）(偏移: 0xFC)
- `RecyclableSound curPowerSnd`（Recyclable音效 cur力度Snd）(偏移: 0x100)
- `int sndState`（int snd状态）(偏移: 0x104)
- `EffectObj FX_3rd`（特效Obj FX_3rd）(偏移: 0x108)
- `EffectObj FX_PV`（特效Obj FX_PV）(偏移: 0x10C)

### 方法 (15)

- `bool get_isPowering()`
  （bool get_isPowering（））
- `void Update()`
  （void 更新（））
- `void Init()`
  （void 初始化（））
- `void Deploy(bool noSelectAnim = False)`
  （void 部署（布尔值 无选择动画 = 假））
- `void UnDeploy(bool temporary = False)`
  （void 取消部署（布尔值 临时 = 假））
- `bool EvilTerminatorSkill(Player player)`
  （bool EvilTerminator技能（玩家 player））
- `void OnAnimationEnd(string animName, string animTag)`
  （void 动画结束时（字符串 animName, 字符串 animTag））
- `void ThrowFireBall()`
  （void 投掷开火Ball（））
- `void FireBallSetting(WPN_Missile missile)`
  （void 开火Ball设置（WPN_Missile missile））
- `void EffectSndEvent()`
  （void 特效Snd事件（））
- `void ClearPowerSound()`
  （void 清除力度音效（））
- `void ClearPowerEffect()`
  （void 清除力度特效（））
- `void CreatePowerEffect()`
  （void 创建力度特效（））
- `void UpdateEffectSize(float progress)`
  （void 更新特效大小（float progress））
- `void BotControl(Bot bot)`
  （void 机器人控制（机器人 bot））

---

## WPN_GRENADE（WPN_GRENADE）

**继承**: WPN_Missile（WPN_Missile）

### 字段 (9)

- `float expRange`（float exp范围）(偏移: 0x5C)
- `float expDamage`（float exp伤害）(偏移: 0x60)
- `float expDmgFactorByDistance`（float expDmg系数By距离）(偏移: 0x64)
- `bool ignoreWall`（bool ignoreWall）(偏移: 0x68)
- `GameObject expEffectPrefab`（游戏对象 exp特效预制体）(偏移: 0x6C)
- `string expSoundName`（string exp音效名称）(偏移: 0x70)
- `bool expWhenTouchSth`（bool expWhen触摸Sth）(偏移: 0x74)
- `bool isExped`（bool isExped）(偏移: 0x75)
- `Action<Entity> CauseDamage_Listener`（Action<Entity> CauseDamage_监听器）(偏移: 0x78)

### 方法 (12)

- `void add_CauseDamage_Listener(Action<Entity> value)`
  （void add_CauseDamage_监听器（Action<Entity> value））
- `void remove_CauseDamage_Listener(Action<Entity> value)`
  （void remove_CauseDamage_监听器（Action<Entity> value））
- `void OnCollisionEnter(Collision collision)`
  （void 碰撞进入时（碰撞 collision））
- `void OnTriggerEnter(Collider other)`
  （void 触发器进入时（碰撞器 other））
- `void Work()`
  （void 工作（））
- `void OnLifeTimerEnd()`
  （void OnLife计时器结束（））
- `void TryExplosion()`
  （void TryExplosion（））
- `void PlayExpEffect()`
  （void 播放Exp特效（））
- `void Damage()`
  （void 伤害（））
- `DamageEventData GetBasicDamageEventData()`
  （伤害事件数据 获取Basic伤害事件数据（））
- `void SetMissileData(MissileData missileData)`
  （void 集合Missile数据（Missile数据 missileData））
- `void CreateExplosion(Vector3 worldPos, float damage, float range, float distanceDecay, bool ignoreWall, DamageEventData dmgEventData, Action<Entity> damageCallBack)`
  （void 创建Explosion（三维向量 worldPos, float damage, float range, float distanceDecay, bool ignoreWall, 伤害事件数据 dmgEventData, Action<Entity> damageCallBack））

---

## WPN_GhostBlade（WPN_幽灵刀锋）

**继承**: WPN_Knife（WPN_近战武器）

### 字段 (6)

- `WD_GhostBlade data2`（WD_幽灵刀锋 data2）(偏移: 0xF0)
- `string secKillhitTag`（string secKillhit标签）(偏移: 0x0)
- `List<Player> secKillTargets`（List<Player> sec击杀Targets）(偏移: 0xF4)
- `Player killTarget`（玩家 kill目标）(偏移: 0xF8)
- `ParticleSystem defenseFX`（粒子系统 defenseFX）(偏移: 0x100)
- `Skill_ModeChange skill`（Skill_模式Change skill）(偏移: 0x104)

### 方法 (22)

- `bool get_defense()`
  （bool get_defense（））
- `void set_defense(bool value)`
  （void set_defense（bool value））
- `void Init()`
  （void 初始化（））
- `void Deploy(bool noSelectAnim = False)`
  （void 部署（布尔值 无选择动画 = 假））
- `void UnDeploy(bool temporary = False)`
  （void 取消部署（布尔值 临时 = 假））
- `void ResetModeChange()`
  （void 重置模式Change（））
- `void SetValidOwner()`
  （void 设置有效所有者（））
- `void RemoveFromOldOwner()`
  （void 从旧所有者移除（））
- `void Update()`
  （void 更新（））
- `void UpdateDisabledSetting(PlayerWeapons wpns)`
  （void 更新禁用的设置（玩家武器 wpns））
- `bool CanSecKill(Player player)`
  （bool 能否Sec击杀（玩家 player））
- `void OnAnimationEnd(string animName, string animTag)`
  （void 动画结束时（字符串 animName, 字符串 animTag））
- `void OnSecKillAnimEnd()`
  （void OnSec击杀动画结束（））
- `CharWpnAnimData GetCharWpnAnimData()`
  （Char武器动画数据 获取Char武器动画数据（））
- `void PlayKnifeAttackAnim(WPN_Knife.KnifeAttackType type)`
  （void 播放近战武器Attack动画（WPN_Knife.近战武器Attack类型 type））
- `bool TryChangeMode()`
  （bool TryChange模式（））
- `void OnSpecialBtnDown()`
  （void 特殊按钮按下时（））
- `void OnSpecialBtnPressed()`
  （void On特殊Btn按下的（））
- `void OnSpecialBtnUnPressed()`
  （void On特殊BtnUn按下的（））
- `void OnJumpBtnDown()`
  （void On跳跃Btn下（））
- `void InvalidDmgCheck(ref DamageEventData eventData)`
  （void InvalidDmg检查（ref DamageEventData eventData））
- `string GetWpnName()`
  （string 获取武器名称（））

---

## WPN_GrenadeGun（WPN_手雷枪械）

**继承**: WPN_Gun（WPN_枪械）

### 字段 (3)

- `ParticleSystem grenadeFire`（粒子系统 grenade开火）(偏移: 0x130)
- `WPN_Gun.AmmoData gunAmmo`（WPN_Gun.弹药数据 gun弹药）(偏移: 0x134)
- `WPN_Gun.AmmoData grenadeAmmo`（WPN_Gun.弹药数据 grenade弹药）(偏移: 0x138)

### 方法 (21)

- `WD_GrenadeGun get_realData()`
  （WD_手雷枪械 get_real数据（））
- `bool get_grenadeMode()`
  （bool get_grenade模式（））
- `void set_grenadeMode(bool value)`
  （void set_grenade模式（bool value））
- `void Init()`
  （void 初始化（））
- `void WPN_GrenadeGun_AnimName_Modifier(ref string value)`
  （void WPN_手雷Gun_动画Name_修改器（ref string value））
- `void AmmoSetting()`
  （void 弹药设置（））
- `void FillAmmo()`
  （void Fill弹药（））
- `void AddAmmo(int count)`
  （void 添加弹药（int count））
- `void ResetModeChange()`
  （void 重置模式Change（））
- `void CrosshairSetting()`
  （void 准星设置（））
- `void AnimSpeedSetting()`
  （void 动画速度设置（））
- `bool GiveUp(bool death = True)`
  （布尔值 放弃（布尔值 死亡 = 真））
- `void OnSpecialBtnDown()`
  （void 特殊按钮按下时（））
- `string GetWpnName()`
  （string 获取武器名称（））
- `void GunShootFunction()`
  （void 枪械射击Function（））
- `void PlayGunShootSound()`
  （void 播放枪械射击音效（））
- `void PlayCharacterShootAnim()`
  （void 播放角色射击动画（））
- `void PlayGunFire()`
  （void 播放枪械开火（））
- `WpnSpriteAsset GetWpnSpriteAsset()`
  （武器精灵资产 获取武器精灵资产（））
- `CharWpnAnimData GetCharWpnAnimData()`
  （Char武器动画数据 获取Char武器动画数据（））
- `bool ShouldPlayBulletEffect()`
  （bool 应该播放子弹特效（））

---

## WPN_Gun（WPN_枪械）

**继承**: Weapon（武器）

### 字段 (13)

- `WeaponData_Gun realData`（WeaponData_枪械 real数据）(偏移: 0xEC)
- `bool shouldSetFireSpeed`（bool should集合开火Speed）(偏移: 0xF1)
- `Func<bool> ReloadCheck_Listener`（Func<bool> 换弹Check_监听器）(偏移: 0xF8)
- `float lastShootTime`（float last射击时间）(偏移: 0xFC)
- `int recoilDataID`（int recoil数据ID）(偏移: 0x100)
- `Func<bool> Getter_FireDisabled`（Func<bool> Getter_开火禁用的）(偏移: 0x104)
- `int fireAnim`（int fire动画）(偏移: 0x10C)
- `float nextAllowedShootTime`（float nextAllowed射击时间）(偏移: 0x110)
- `ParticleSystem gunFire`（粒子系统 gun开火）(偏移: 0x114)
- `int knifeAttackCount`（int knifeAttack数量）(偏移: 0x118)
- `int knifeAttackAnim`（int knifeAttack动画）(偏移: 0x11C)
- `int zoomActionCount`（int zoom动作数量）(偏移: 0x120)
- `int lastZoomIndex`（int last瞄准索引）(偏移: 0x128)

### 方法 (60)

- `bool get_isSemiGun()`
  （bool get_isSemi枪械（））
- `void set_isSemiGun(bool value)`
  （void set_isSemi枪械（bool value））
- `WPN_Gun.AmmoData get_ammoData()`
  （WPN_Gun.弹药数据 get_ammo数据（））
- `void set_ammoData(WPN_Gun.AmmoData value)`
  （void set_ammo数据（WPN_Gun.弹药数据 value））
- `WPN_Gun.SemiGunFireLinkState get_semiGunFireLinkState()`
  （WPN_Gun.Semi枪械开火Link状态 get_semi枪械开火Link状态（））
- `void set_semiGunFireLinkState(WPN_Gun.SemiGunFireLinkState value)`
  （void set_semi枪械开火Link状态（WPN_Gun.Semi枪械开火Link状态 value））
- `bool get_isSniper()`
  （bool get_is狙击（））
- `int get_zoomIndex()`
  （int get_zoom索引（））
- `void set_zoomIndex(int value)`
  （void set_zoom索引（int value））
- `bool get_nextZoomReady()`
  （bool get_next瞄准Ready（））
- `void set_nextZoomReady(bool value)`
  （void set_next瞄准Ready（bool value））
- `void Update()`
  （void 更新（））
- `void OnAnimationEnd(string animName, string animTag)`
  （void 动画结束时（字符串 animName, 字符串 animTag））
- `void OnAnimationExit(string animName, string animTag)`
  （void On动画Exit（string animName, string animTag））
- `void Init()`
  （void 初始化（））
- `void OnGenerateFromOwner()`
  （void 从所有者生成时（））
- `void AmmoSetting()`
  （void 弹药设置（））
- `void Deploy(bool noSelectAnim = False)`
  （void 部署（布尔值 无选择动画 = 假））
- `void AnimSpeedSetting()`
  （void 动画速度设置（））
- `void UpdateAnimSpeed_Reload()`
  （void 更新动画Speed_换弹（））
- `void UnDeploy(bool temporary = False)`
  （void 取消部署（布尔值 临时 = 假））
- `void SetBasicRecoilData()`
  （void 集合Basic后坐力数据（））
- `void SetRecoilData(int index = 0)`
  （void 集合后坐力数据（int index = 0））
- `void GunFireChecking()`
  （void 枪械开火Checking（））
- `void OnReloadBtnDown()`
  （void On换弹Btn下（））
- `void TryReload()`
  （void Try换弹（））
- `void OnSpecialBtnDown()`
  （void 特殊按钮按下时（））
- `bool CanReload()`
  （bool 能否换弹（））
- `void Reload()`
  （void 换弹（））
- `void ReloadOver()`
  （void 换弹Over（））
- `void PreReloadOver()`
  （void Pre换弹Over（））
- `void FillAmmo()`
  （void Fill弹药（））
- `void AddAmmo(int count)`
  （void 添加弹药（int count））
- `void Damage(Ray ray)`
  （void 伤害（Ray ray））
- `void PlayGunFire()`
  （void 播放枪械开火（））
- `void StopGunFire()`
  （void 停止枪械开火（））
- `void KnifeAttackEvent(int index)`
  （void 近战武器Attack事件（int index））
- `KnifeAttackData GetKnifeAttackData(int attackIndex)`
  （近战武器Attack数据 获取近战武器Attack数据（int attackIndex））
- `string GetKnifeHitSoundName(int attackIndex)`
  （string 获取近战武器命中音效名称（int attackIndex））
- `int GetKnifeAttackSprIndex(int attackIndex)`
  （int 获取近战武器AttackSpr索引（int attackIndex））
- `void StartKnifeAttack()`
  （void 开始近战武器Attack（））
- `void OnKnifeAttackExit()`
  （void On近战武器AttackExit（））
- `bool ShouldPlayBulletEffect()`
  （bool 应该播放子弹特效（））
- `void GenerateBullet()`
  （void Generate子弹（））
- `void UseZoom()`
  （void Use瞄准（））
- `void CloseZoom(bool rapidly = False)`
  （void 关闭瞄准（bool rapidly = False））
- `void OnFireAnimExit()`
  （void On开火动画Exit（））
- `void GunShoot()`
  （void 枪械射击（））
- `void GunShoot_NoCheck()`
  （void 枪械Shoot_No检查（））
- `void GunShoot_Logic()`
  （void 枪械Shoot_Logic（））
- `void GunShootFunction()`
  （void 枪械射击Function（））
- `bool ConsumeAmmo()`
  （bool Consume弹药（））
- `void TryReloadNextFrame()`
  （void Try换弹下一个Frame（））
- `void PlayGunShootSound()`
  （void 播放枪械射击音效（））
- `void BreakAutomaticGunFire()`
  （void BreakAutomatic枪械开火（））
- `void AutomaticGunStopFire()`
  （void Automatic枪械停止开火（））
- `void BotControl(Bot bot)`
  （void 机器人控制（机器人 bot））
- `void SniperBotControl(Bot bot)`
  （void 狙击机器人控制（机器人 bot））
- `bool CanGetInfinityAmmo()`
  （bool 能否获取无限弹药（））
- `bool GiveUp(bool death = True)`
  （布尔值 放弃（布尔值 死亡 = 真））

---

## WPN_Gun.AmmoData（WPN_Gun.弹药数据）

### 字段 (5)

- `ObscuredInt clip`（模糊整数 clip）(偏移: 0x8)
- `ObscuredInt ammo`（模糊整数 ammo）(偏移: 0x1C)
- `ObscuredInt maxClip`（模糊整数 max弹匣）(偏移: 0x30)
- `ObscuredInt maxAmmo`（模糊整数 max弹药）(偏移: 0x44)
- `bool isBuff`（bool is增益）(偏移: 0x58)

### 方法 (11)

- `bool get_isMaxClip()`
  （bool get_is最大弹匣（））
- `bool get_isEmptyClip()`
  （bool get_is空弹匣（））
- `bool get_isEmptyAmmo()`
  （bool get_is空弹药（））
- `bool get_canReload()`
  （bool get_can换弹（））
- `bool get_isAllEmpty()`
  （bool get_is所有空（））
- `void Reload()`
  （void 换弹（））
- `void Fill()`
  （void Fill（））
- `void AddAmmoByMultiplier(int count)`
  （void 添加弹药ByMultiplier（int count））
- `void AddClip(int count)`
  （void 添加弹匣（int count））
- `void Recover(float rate)`
  （void 恢复（float rate））
- `void BindHUD()`
  （void Bind抬头显示（））

---

## WPN_Gun.SemiGunFireLinkState（WPN_Gun.Semi枪械开火Link状态）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## WPN_Knife（WPN_近战武器）

**继承**: Weapon（武器）

### 字段 (2)

- `float combo1_AnimSpeed`（float combo1_动画Speed）(偏移: 0xEC)
- `string AnimTag_KnifeAttack`（string 动画Tag_近战武器Attack）(偏移: 0x0)

### 方法 (13)

- `WeaponData_Knife get_realData()`
  （WeaponData_近战武器 get_real数据（））
- `void Init()`
  （void 初始化（））
- `void Update()`
  （void 更新（））
- `void OnSpecialBtnDown()`
  （void 特殊按钮按下时（））
- `void PlayKnifeAttackAnim(WPN_Knife.KnifeAttackType type)`
  （void 播放近战武器Attack动画（WPN_Knife.近战武器Attack类型 type））
- `void AnimSpeedSetting()`
  （void 动画速度设置（））
- `void OnAnimationEnd(string animName, string animTag)`
  （void 动画结束时（字符串 animName, 字符串 animTag））
- `void OnKnifeAttackAnimEnd(string animName)`
  （void On近战武器Attack动画结束（string animName））
- `void KnifeAttackEvent(int index)`
  （void 近战武器Attack事件（int index））
- `KnifeAttackData GetKnifeAttackData(int attackIndex)`
  （近战武器Attack数据 获取近战武器Attack数据（int attackIndex））
- `string GetKnifeHitSoundName(int attackIndex)`
  （string 获取近战武器命中音效名称（int attackIndex））
- `bool GiveUp(bool death = True)`
  （布尔值 放弃（布尔值 死亡 = 真））
- `void BotControl(Bot bot)`
  （void 机器人控制（机器人 bot））

---

## WPN_Knife.KnifeAttackType（WPN_Knife.近战武器Attack类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## WPN_MasterHero（WPN_Master英雄）

**继承**: WPN_Knife（WPN_近战武器）

### 字段 (2)

- `WD_MasterHero realData2`（WD_Master英雄 realData2）(偏移: 0xF0)
- `Skill_Common skill`（通用技能 skill）(偏移: 0xF4)

### 方法 (9)

- `void Init()`
  （void 初始化（））
- `void WPN_MasterHero_KnifeAttackHit_Listener(int attackIndex, Entity victim)`
  （void WPN_MasterHero_近战武器AttackHit_监听器（int attackIndex, 实体 victim））
- `void Deploy(bool noSelectAnim = False)`
  （void 部署（布尔值 无选择动画 = 假））
- `void UnDeploy(bool temporary = False)`
  （void 取消部署（布尔值 临时 = 假））
- `bool MasterHeroSkill(Player player)`
  （bool Master英雄技能（玩家 player））
- `int GetKnifeAttackSprIndex(int attackIndex)`
  （int 获取近战武器AttackSpr索引（int attackIndex））
- `string GetKnifeHitSoundName(int attackIndex)`
  （string 获取近战武器命中音效名称（int attackIndex））
- `string GetKnifeHitEffectName(int attackIndex)`
  （string 获取近战武器命中特效名称（int attackIndex））
- `void BotControl(Bot bot)`
  （void 机器人控制（机器人 bot））

---

## WPN_MasterHunter（WPN_MasterHunter）

**继承**: WPN_Knife（WPN_近战武器）

### 字段 (2)

- `WD_MasterHunter realData2`（WD_MasterHunter realData2）(偏移: 0xF0)
- `Skill_Common skill`（通用技能 skill）(偏移: 0xF4)

### 方法 (5)

- `void Init()`
  （void 初始化（））
- `void Deploy(bool noSelectAnim = False)`
  （void 部署（布尔值 无选择动画 = 假））
- `void UnDeploy(bool temporary = False)`
  （void 取消部署（布尔值 临时 = 假））
- `BotSkillBase SkillAI_MasterHunter(Bot bot)`
  （机器人技能基础 技能AI_MasterHunter（机器人 bot））
- `bool MasterHunterSkill(Player player)`
  （bool MasterHunter技能（玩家 player））

---

## WPN_MechanicHero（WPN_Mechanic英雄）

**继承**: WPN_Knife（WPN_近战武器）

### 字段 (3)

- `WD_MechanicHero realData2`（WD_Mechanic英雄 realData2）(偏移: 0xF0)
- `Skill_Common skill_Arcane`（Skill_Common skill_Arcane）(偏移: 0xF4)
- `Skill_SentryGun skill_SentryGun`（Skill_Sentry枪械 skill_Sentry枪械）(偏移: 0xF8)

### 方法 (7)

- `void Init()`
  （void 初始化（））
- `void SetValidOwner()`
  （void 设置有效所有者（））
- `void RemoveFromOldOwner()`
  （void 从旧所有者移除（））
- `bool SkillArcane(Player player)`
  （bool 技能Arcane（玩家 player））
- `bool SkillSentryGun(Player player)`
  （bool 技能Sentry枪械（玩家 player））
- `BotSkillBase SkillAI_Arcane(Bot bot)`
  （机器人技能基础 技能AI_Arcane（机器人 bot））
- `BotSkillBase SkillAI_SentryGun(Bot bot)`
  （机器人技能基础 技能AI_Sentry枪械（机器人 bot））

---

## WPN_MiniGunAnim（WPN_Mini枪械动画）

**继承**: WpnComponent（武器组件）

### 字段 (1)

- `List<string> ModifyAnimList`（List<string> Modify动画列表）(偏移: 0x33B63397)

### 方法 (4)

- `void Init(Weapon wpn)`
  （void 初始化（武器 wpn））
- `void Wpn_AnimName_Modifier(ref string animName)`
  （void Wpn_动画Name_修改器（ref string animName））
- `void Update()`
  （void 更新（））
- `void JumpListener()`
  （void 跳跃监听器（））

---

## WPN_Missile（WPN_Missile）

**继承**: RecyclableObject（可回收对象）

### 字段 (9)

- `Entity owner`（实体 owner）(偏移: 0x30)
- `Team ownerInitalTeam`（队伍 ownerInital队伍）(偏移: 0x34)
- `WeaponData weaponData`（武器数据 weapon数据）(偏移: 0x38)
- `int sprIndex`（int spr索引）(偏移: 0x3C)
- `string dropSoundName`（string drop音效名称）(偏移: 0x40)
- `Rigidbody rigidBody`（刚体 rigid身体）(偏移: 0x44)
- `TrailRenderer trailRenderer`（Trail渲染器 trail渲染器）(偏移: 0x48)
- `float shootSpeed`（float shootSpeed）(偏移: 0x4C)
- `Vector3 extraGravity`（三维向量 extra重力）(偏移: 0x50)

### 方法 (8)

- `bool get_isLegal()`
  （bool get_isLegal（））
- `void OnCollisionEnter(Collision collision)`
  （void 碰撞进入时（碰撞 collision））
- `void Recycle(bool roundRecycle)`
  （void 回收（布尔值 循环回收））
- `void Work()`
  （void 工作（））
- `void SetOwner(Entity newOwner)`
  （void 集合Owner（实体 newOwner））
- `void FixedUpdate()`
  （void 固定更新（））
- `void SetWeaponData(WeaponData wpnData, int sprIndex)`
  （void 集合Weapon数据（武器数据 wpnData, int sprIndex））
- `void SetMissileData(MissileData missileData)`
  （void 集合Missile数据（Missile数据 missileData））

---

## WPN_Prefire（WPN_Prefire）

**继承**: WpnComponent（武器组件）

### 字段 (4)

- `float penalty`（float penalty）(偏移: 0x10)
- `float prefireAnimTime`（float prefire动画时间）(偏移: 0x14)
- `float needDelayTime`（float need延迟时间）(偏移: 0x18)
- `WPN_Gun gun`（WPN_枪械 gun）(偏移: 0x1C)

### 方法 (5)

- `void Init(Weapon wpn)`
  （void 初始化（武器 wpn））
- `void OnEnable()`
  （void 启用时（））
- `void Update()`
  （void 更新（））
- `void GetPrefireAnimTime()`
  （void 获取Prefire动画时间（））
- `bool Prefire()`
  （bool Prefire（））

---

## WPN_RPG（WPN_RPG）

**继承**: Weapon（武器）

### 字段 (4)

- `WPN_Gun.AmmoData ammo`（WPN_Gun.弹药数据 ammo）(偏移: 0xEC)
- `WD_RPG realData`（WD_RPG real数据）(偏移: 0xF0)
- `ParticleSystem gunfire`（粒子系统 gunfire）(偏移: 0xF4)
- `WPN_Gun.SemiGunFireLinkState fireState`（WPN_Gun.Semi枪械开火Link状态 fire状态）(偏移: 0xF8)

### 方法 (17)

- `void Init()`
  （void 初始化（））
- `void Deploy(bool noSelectAnim = False)`
  （void 部署（布尔值 无选择动画 = 假））
- `void OnGenerateFromOwner()`
  （void 从所有者生成时（））
- `void CrosshairSetting()`
  （void 准星设置（））
- `void AnimSpeedSetting()`
  （void 动画速度设置（））
- `void OnFireBtnPressed()`
  （void On开火Btn按下的（））
- `void Update()`
  （void 更新（））
- `void OnFireBtnUnPressed()`
  （void On开火BtnUn按下的（））
- `void Fire()`
  （void 开火（））
- `void OnReloadBtnDown()`
  （void On换弹Btn下（））
- `bool CanReload()`
  （bool 能否换弹（））
- `void Reload()`
  （void 换弹（））
- `void ReloadOver()`
  （void 换弹Over（））
- `void OnAnimationEnd(string animName, string animTag)`
  （void 动画结束时（字符串 animName, 字符串 animTag））
- `void BotControl(Bot bot)`
  （void 机器人控制（机器人 bot））
- `bool GiveUp(bool death = True)`
  （布尔值 放弃（布尔值 死亡 = 真））
- `void FillAmmo()`
  （void Fill弹药（））

---

## WPN_RandomBigshotAnim（WPN_随机爆头动画）

**继承**: WpnComponent（武器组件）

### 方法 (2)

- `void Init(Weapon wpn)`
  （void 初始化（武器 wpn））
- `void GetBigshotAnimName(ref string animName)`
  （void 获取爆头动画名称（ref string animName））

---

## WPN_RandomSelectAnim（WPN_随机选择动画）

**继承**: WpnComponent（武器组件）

### 方法 (2)

- `void Init(Weapon wpn)`
  （void 初始化（武器 wpn））
- `void GetSelectAnimName(ref string animName)`
  （void 获取选择动画名称（ref string animName））

---

## WPN_RecoverAmmo（WPN_恢复弹药）

**继承**: WpnComponent（武器组件）

### 字段 (2)

- `WPN_Gun gun`（WPN_枪械 gun）(偏移: 0x10)
- `float lastRecoverTime`（float last恢复时间）(偏移: 0x14)

### 方法 (2)

- `void Init(Weapon wpn)`
  （void 初始化（武器 wpn））
- `void Update()`
  （void 更新（））

---

## WPN_ReloadDisable（WPN_换弹禁用）

**继承**: WpnComponent（武器组件）

### 方法 (1)

- `void Init(Weapon wpn)`
  （void 初始化（武器 wpn））

---

## WPN_RepeatFire（WPN_Repeat开火）

**继承**: WpnComponent（武器组件）

### 字段 (4)

- `RepeatFireData data`（Repeat开火数据 data）(偏移: 0x10)
- `bool isOpen`（bool is打开）(偏移: 0x14)
- `float nextAvailableTime`（float nextAvailable时间）(偏移: 0x18)
- `Coroutine coroutine`（协程 coroutine）(偏移: 0x1C)

### 方法 (6)

- `WPN_Gun get_gun()`
  （WPN_枪械 get_gun（））
- `void Init(Weapon wpn)`
  （void 初始化（武器 wpn））
- `void Update()`
  （void 更新（））
- `void AmmoBGSetting()`
  （void 弹药BG设置（））
- `bool FireDisabledCheck()`
  （bool 开火禁用的检查（））
- `IEnumerator RepeatFireCoroutine()`
  （IEnumerator Repeat开火协程（））

---

## WPN_Rope（WPN_Rope）

**继承**: Weapon（武器）

### 字段 (10)

- `GameObject scrFX`（游戏对象 scrFX）(偏移: 0xEC)
- `float deltaY`（float deltaY）(偏移: 0xF0)
- `Vector3 startPoint`（三维向量 起点）(偏移: 0xF4)
- `Vector3 endPoint`（三维向量 终点）(偏移: 0x100)
- `float readyNeedTime`（float ready需要时间）(偏移: 0x10C)
- `float readyDuration`（float ready持续时间）(偏移: 0x110)
- `float slideStartTime`（float slide开始时间）(偏移: 0x114)
- `float slideNeedTime`（float slide需要时间）(偏移: 0x118)
- `float slideEndTime`（float slide结束时间）(偏移: 0x11C)
- `float slideSpeed`（float slideSpeed）(偏移: 0x120)

### 方法 (11)

- `bool get_slideStarted()`
  （bool get_slideStarted（））
- `void Deploy(bool noSelectAnim = False)`
  （void 部署（布尔值 无选择动画 = 假））
- `void OnAnimationEnd(string animName, string animTag)`
  （void 动画结束时（字符串 animName, 字符串 animTag））
- `void CalculateReadyData()`
  （void 计算Ready数据（））
- `void Update()`
  （void 更新（））
- `void UnDeploy(bool temporary = False)`
  （void 取消部署（布尔值 临时 = 假））
- `void RemoveFromOldOwner()`
  （void 从旧所有者移除（））
- `void RopeStart()`
  （void Rope开始（））
- `void RopeEnd()`
  （void Rope结束（））
- `void SetPoint(Vector3 start, Vector3 end)`
  （void 集合Point（三维向量 start, 三维向量 end））
- `bool GetNextPos(out Vector3 nextPos)`
  （bool 获取下一个Pos（out Vector3 nextPos））

---

## WPN_SentryGun（WPN_Sentry枪械）

**继承**: Weapon（武器）

### 字段 (4)

- `WD_SentryGun realData`（WD_Sentry枪械 real数据）(偏移: 0xEC)
- `WPN_Gun.AmmoData ammo`（WPN_Gun.弹药数据 ammo）(偏移: 0xF0)
- `Action<SentryGun> SetSuccess_Listener`（Action<SentryGun> 集合Success_监听器）(偏移: 0xF4)
- `Func<bool> SetCheck_Listener`（Func<bool> 集合Check_监听器）(偏移: 0xF8)

### 方法 (10)

- `void Init()`
  （void 初始化（））
- `void OnGenerateFromOwner()`
  （void 从所有者生成时（））
- `void OnAnimationEnd(string animName, string animTag)`
  （void 动画结束时（字符串 animName, 字符串 animTag））
- `void Update()`
  （void 更新（））
- `void Deploy(bool noSelectAnim = False)`
  （void 部署（布尔值 无选择动画 = 假））
- `void UnDeploy(bool temporary = False)`
  （void 取消部署（布尔值 临时 = 假））
- `void TrySet()`
  （void Try集合（））
- `void SetSentryGun()`
  （void 集合Sentry枪械（））
- `bool GiveUp(bool death = True)`
  （布尔值 放弃（布尔值 死亡 = 真））
- `void BotControl(Bot bot)`
  （void 机器人控制（机器人 bot））

---

## WPN_StunGrenade（WPN_眩晕手雷）

**继承**: WPN_GRENADE（WPN_GRENADE）

### 方法 (1)

- `void TryExplosion()`
  （void TryExplosion（））

---

## WPN_StunGrenade2（WPN_眩晕Grenade2）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (2)

- `GameObject stunBuffEffect`（游戏对象 stun增益特效）(偏移: 0xC)
- `GameObject screenFX`（游戏对象 screenFX）(偏移: 0x10)

### 方法 (2)

- `void Awake()`
  （void 唤醒（））
- `void OnCauseDamage(Entity victim)`
  （void OnCause伤害（实体 victim））

---

## WPN_Throw（WPN_投掷）

**继承**: Weapon（武器）

### 字段 (4)

- `Vector3 throwOffset`（三维向量 throwOffset）(偏移: 0x0)
- `WD_Missile realData`（WD_Missile real数据）(偏移: 0xEC)
- `WPN_Gun.AmmoData ammoData`（WPN_Gun.弹药数据 ammo数据）(偏移: 0xF0)
- `bool throwReady`（bool throwReady）(偏移: 0xF4)

### 方法 (11)

- `void Init()`
  （void 初始化（））
- `void OnAnimationEnd(string animName, string animTag)`
  （void 动画结束时（字符串 animName, 字符串 animTag））
- `void Update()`
  （void 更新（））
- `void UnDeploy(bool temporary = False)`
  （void 取消部署（布尔值 临时 = 假））
- `void Deploy(bool noSelectAnim = False)`
  （void 部署（布尔值 无选择动画 = 假））
- `void OnGenerateFromOwner()`
  （void 从所有者生成时（））
- `void Throw()`
  （void 投掷（））
- `void OnFireAnimEnd()`
  （void On开火动画结束（））
- `void Reload()`
  （void 换弹（））
- `bool GiveUp(bool death = True)`
  （布尔值 放弃（布尔值 死亡 = 真））
- `void Set5Times()`
  （void Set5Times（））

---

## WWWForm（WWWForm）

### 方法 (1)

- `Encoding get_DefaultEncoding()`
  （Encoding get_默认的Encoding（））

---

## WWWTranscoder（WWWTranscoder）

### 字段 (9)

- `byte[] ucHexChars`（byte[] ucHexChars）(偏移: 0x0)
- `byte[] lcHexChars`（byte[] lcHexChars）(偏移: 0x4)
- `byte urlEscapeChar`（byte urlEscapeChar）(偏移: 0x8)
- `byte[] urlSpace`（byte[] urlSpace）(偏移: 0xC)
- `byte[] dataSpace`（byte[] dataSpace）(偏移: 0x10)
- `byte[] urlForbidden`（byte[] urlForbidden）(偏移: 0x14)
- `byte qpEscapeChar`（byte qpEscapeChar）(偏移: 0x18)
- `byte[] qpSpace`（byte[] qpSpace）(偏移: 0x1C)
- `byte[] qpForbidden`（byte[] qpForbidden）(偏移: 0x20)

### 方法 (4)

- `byte Hex2Byte(byte[] b, int offset)`
  （byte Hex2Byte（byte[] b, int offset））
- `byte[] URLDecode(byte[] toEncode)`
  （byte[] URLDecode（byte[] toEncode））
- `bool ByteSubArrayEquals(byte[] array, int index, byte[] comperand)`
  （bool Byte子数组Equals（byte[] array, int index, byte[] comperand））
- `byte[] Decode(byte[] input, byte escapeChar, byte[] space)`
  （byte[] Decode（byte[] input, byte escapeChar, byte[] space））

---

## WaitCallback（Wait回调）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(object state)`
  （void 调用（对象 state））
- `IAsyncResult BeginInvoke(object state, AsyncCallback callback, object object)`
  （I异步结果 开始调用（对象 state, 异步回调 callback, 对象 object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## WaitForSeconds（WaitForSeconds）

**继承**: YieldInstruction（YieldInstruction）

### 字段 (1)

- `float m_Seconds`（float m_Seconds）(偏移: 0x8)

---

## WaitForSecondsRealtime（WaitForSecondsRealtime）

**继承**: CustomYieldInstruction（自定义Yield指令）

### 字段 (1)

- `float m_WaitUntilTime`（float m_WaitUntil时间）(偏移: 0xC)

### 方法 (4)

- `float get_waitTime()`
  （float get_wait时间（））
- `void set_waitTime(float value)`
  （void set_wait时间（float value））
- `bool get_keepWaiting()`
  （布尔值 获取_保持等待（））
- `void Reset()`
  （void 重置（））

---

## WaitHandle（Wait句柄）

**继承**: MarshalByRefObject, IDisposable（MarshalByRef对象, 可释放接口）

### 字段 (4)

- `IntPtr waitHandle`（整数Ptr wait句柄）(偏移: 0xC)
- `SafeWaitHandle safeWaitHandle`（SafeWait句柄 safeWait句柄）(偏移: 0x10)
- `bool hasThreadAffinity`（bool hasThreadAffinity）(偏移: 0x14)
- `IntPtr InvalidHandle`（整数Ptr Invalid句柄）(偏移: 0x0)

### 方法 (22)

- `void Init()`
  （void 初始化（））
- `void set_Handle(IntPtr value)`
  （void set_句柄（整数Ptr value））
- `SafeWaitHandle get_SafeWaitHandle()`
  （SafeWait句柄 get_SafeWait句柄（））
- `void SetHandleInternal(SafeWaitHandle handle)`
  （void 集合句柄内部的（SafeWait句柄 handle））
- `bool WaitOne(int millisecondsTimeout, bool exitContext)`
  （bool WaitOne（int millisecondsTimeout, bool exitContext））
- `bool WaitOne()`
  （bool WaitOne（））
- `bool WaitOne(int millisecondsTimeout)`
  （bool WaitOne（int millisecondsTimeout））
- `bool WaitOne(long timeout, bool exitContext)`
  （bool WaitOne（long timeout, bool exitContext））
- `bool InternalWaitOne(SafeHandle waitableSafeHandle, long millisecondsTimeout, bool hasThreadAffinity, bool exitContext)`
  （bool 内部的WaitOne（Safe句柄 waitableSafeHandle, long millisecondsTimeout, bool hasThreadAffinity, bool exitContext））
- `bool WaitAll(WaitHandle[] waitHandles, int millisecondsTimeout, bool exitContext)`
  （bool Wait所有（WaitHandle[] waitHandles, int millisecondsTimeout, bool exitContext））
- `bool WaitAll(WaitHandle[] waitHandles, int millisecondsTimeout)`
  （bool Wait所有（WaitHandle[] waitHandles, int millisecondsTimeout））
- `int WaitAny(WaitHandle[] waitHandles, int millisecondsTimeout, bool exitContext)`
  （int Wait任意（WaitHandle[] waitHandles, int millisecondsTimeout, bool exitContext））
- `int WaitAny(WaitHandle[] waitHandles, TimeSpan timeout, bool exitContext)`
  （int Wait任意（WaitHandle[] waitHandles, 时间Span timeout, bool exitContext））
- `int WaitAny(WaitHandle[] waitHandles)`
  （int Wait任意（WaitHandle[] waitHandles））
- `void ThrowAbandonedMutexException()`
  （void 投掷AbandonedMutexException（））
- `void ThrowAbandonedMutexException(int location, WaitHandle handle)`
  （void 投掷AbandonedMutexException（int location, Wait句柄 handle））
- `void Close()`
  （void 关闭（））
- `void Dispose(bool explicitDisposing)`
  （void 释放（bool explicitDisposing））
- `void Dispose()`
  （void 释放（））
- `int WaitMultiple(WaitHandle[] waitHandles, int millisecondsTimeout, bool exitContext, bool WaitAll)`
  （int WaitMultiple（WaitHandle[] waitHandles, int millisecondsTimeout, bool exitContext, bool WaitAll））
- `int WaitOneNative(SafeHandle waitableSafeHandle, uint millisecondsTimeout, bool hasThreadAffinity, bool exitContext)`
  （int WaitOneNative（Safe句柄 waitableSafeHandle, uint millisecondsTimeout, bool hasThreadAffinity, bool exitContext））
- `int Wait_internal(IntPtr* handles, int numHandles, bool waitAll, int ms)`
  （int Wait_internal（整数Ptr* handles, int numHandles, bool waitAll, int ms））

---

## WaitOrTimerCallback（WaitOr计时器回调）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(object state, bool timedOut)`
  （void Invoke（object state, bool timedOut））
- `IAsyncResult BeginInvoke(object state, bool timedOut, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（object state, bool timedOut, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## WallHackDetector（WallHackDetector）

**继承**: ACTkDetectorBase（反作弊检测器基类）

### 字段 (35)

- `Vector3 rigidPlayerVelocity`（三维向量 rigid玩家速度）(偏移: 0x1C)
- `int instancesInScene`（int instancesIn场景）(偏移: 0x0)
- `WaitForEndOfFrame waitForEndOfFrame`（WaitFor结束OfFrame waitFor结束OfFrame）(偏移: 0x28)
- `bool checkRigidbody`（bool check刚体）(偏移: 0x2C)
- `bool checkController`（bool check控制器）(偏移: 0x0)
- `bool checkWireframe`（bool checkWireframe）(偏移: 0x0)
- `bool checkRaycast`（bool checkRaycast）(偏移: 0x0)
- `int wireframeDelay`（int wireframe延迟）(偏移: 0x0)
- `int raycastDelay`（int raycast延迟）(偏移: 0x34)
- `Vector3 spawnPosition`（三维向量 spawnPosition）(偏移: 0x38)
- `byte maxFalsePositives`（byte maxFalsePositives）(偏移: 0x44)
- `GameObject serviceContainer`（游戏对象 service容器）(偏移: 0x48)
- `GameObject solidWall`（游戏对象 solidWall）(偏移: 0x4C)
- `GameObject thinWall`（游戏对象 thinWall）(偏移: 0x50)
- `Camera wfCamera`（摄像机 wf摄像机）(偏移: 0x54)
- `MeshRenderer foregroundRenderer`（网格渲染器 foreground渲染器）(偏移: 0x58)
- `MeshRenderer backgroundRenderer`（网格渲染器 background渲染器）(偏移: 0x5C)
- `Color wfColor1`（颜色 wfColor1）(偏移: 0x60)
- `Color wfColor2`（颜色 wfColor2）(偏移: 0x70)
- `Shader wfShader`（着色器 wf着色器）(偏移: 0x80)
- `Material wfMaterial`（材质 wf材质）(偏移: 0x84)
- `Texture2D shaderTexture`（Texture2D shader纹理）(偏移: 0x88)
- `Texture2D targetTexture`（Texture2D target纹理）(偏移: 0x8C)
- `RenderTexture renderTexture`（Render纹理 render纹理）(偏移: 0x90)
- `int whLayer`（int wh层）(偏移: 0x94)
- `int raycastMask`（int raycast掩码）(偏移: 0x98)
- `Rigidbody rigidPlayer`（刚体 rigid玩家）(偏移: 0x9C)
- `CharacterController charControllerPlayer`（角色控制器 char控制器玩家）(偏移: 0xA0)
- `float charControllerVelocity`（float char控制器速度）(偏移: 0xA4)
- `byte rigidbodyDetections`（byte rigidbodyDetections）(偏移: 0xA8)
- `byte controllerDetections`（byte controllerDetections）(偏移: 0x0)
- `byte wireframeDetections`（byte wireframeDetections）(偏移: 0x0)
- `byte raycastDetections`（byte raycastDetections）(偏移: 0x0)
- `bool wireframeDetected`（bool wireframeDetected）(偏移: 0x0)
- `RaycastHit[] rayHits`（RaycastHit[] rayHits）(偏移: 0xB0)

### 方法 (49)

- `bool get_CheckRigidbody()`
  （bool get_检查刚体（））
- `void set_CheckRigidbody(bool value)`
  （void set_检查刚体（bool value））
- `bool get_CheckController()`
  （bool get_检查控制器（））
- `void set_CheckController(bool value)`
  （void set_检查控制器（bool value））
- `bool get_CheckWireframe()`
  （bool get_检查Wireframe（））
- `void set_CheckWireframe(bool value)`
  （void set_检查Wireframe（bool value））
- `bool get_CheckRaycast()`
  （bool get_检查Raycast（））
- `void set_CheckRaycast(bool value)`
  （void set_检查Raycast（bool value））
- `WallHackDetector AddToSceneOrGetExisting()`
  （WallHackDetector 添加To场景Or获取Existing（））
- `void StartDetection()`
  （void 开始Detection（））
- `void StartDetection(Action callback)`
  （void 开始Detection（动作 callback））
- `void StartDetection(Action callback, Vector3 spawnPosition)`
  （void 开始Detection（动作 callback, 三维向量 spawnPosition））
- `void StartDetection(Action callback, Vector3 spawnPosition, byte maxFalsePositives)`
  （void 开始Detection（动作 callback, 三维向量 spawnPosition, byte maxFalsePositives））
- `void StopDetection()`
  （void 停止检测（））
- `void Dispose()`
  （void 释放（））
- `WallHackDetector get_Instance()`
  （WallHackDetector get_实例（））
- `void set_Instance(WallHackDetector value)`
  （void set_实例（WallHackDetector value））
- `WallHackDetector get_GetOrCreateInstance()`
  （WallHackDetector get_获取Or创建实例（））
- `void Awake()`
  （void 唤醒（））
- `void OnDestroy()`
  （void 销毁时（））
- `void OnLevelWasLoadedNew(Scene scene, LoadSceneMode mode)`
  （void On等级WasLoaded新的（场景 scene, 加载场景模式 mode））
- `void FixedUpdate()`
  （void 固定更新（））
- `void Update()`
  （void 更新（））
- `void StartDetectionInternal(Action callback, Vector3 servicePosition, byte falsePositivesInRow)`
  （void 开始Detection内部的（动作 callback, 三维向量 servicePosition, byte falsePositivesInRow））
- `void StartDetectionAutomatically()`
  （void 自动开始检测（））
- `void PauseDetector()`
  （void 暂停Detector（））
- `bool ResumeDetector()`
  （bool 恢复Detector（））
- `void StopDetectionInternal()`
  （void 停止Detection内部的（））
- `void DisposeInternal()`
  （void 释放内部（））
- `void UpdateServiceContainer()`
  （void 更新服务容器（））
- `IEnumerator InitDetector()`
  （IEnumerator 初始化Detector（））
- `void StartRigidModule()`
  （void 开始Rigid模块（））
- `void StartControllerModule()`
  （void 开始控制器模块（））
- `void StartWireframeModule()`
  （void 开始Wireframe模块（））
- `void ShootWireframeModule()`
  （void 射击Wireframe模块（））
- `IEnumerator CaptureFrame()`
  （IEnumerator CaptureFrame（））
- `void StartRaycastModule()`
  （void 开始Raycast模块（））
- `void ShootRaycastModule()`
  （void 射击Raycast模块（））
- `void StopRigidModule()`
  （void 停止Rigid模块（））
- `void StopControllerModule()`
  （void 停止控制器模块（））
- `void StopWireframeModule()`
  （void 停止Wireframe模块（））
- `void StopRaycastModule()`
  （void 停止Raycast模块（））
- `void InitRigidModule()`
  （void 初始化Rigid模块（））
- `void InitControllerModule()`
  （void 初始化控制器模块（））
- `void UninitRigidModule()`
  （void UninitRigid模块（））
- `void UninitControllerModule()`
  （void Uninit控制器模块（））
- `bool Detect()`
  （bool Detect（））
- `Color32 GenerateColor()`
  （Color32 Generate颜色（））
- `bool ColorsSimilar(Color32 c1, Color32 c2, int tolerance)`
  （bool ColorsSimilar（Color32 c1, Color32 c2, int tolerance））

---

## Warning（Warning）

### 字段 (1)

- `bool logged`（bool logged）(偏移: 0x3B673B45)

### 方法 (2)

- `void Log(string message, Warning.Logger logger, bool logInEditMode = False)`
  （void Log（string message, Warning.Logger logger, bool logInEditMode = False））
- `void Log(string message, Transform context, bool logInEditMode = False)`
  （void Log（string message, 变换 context, bool logInEditMode = False））

---

## Warning.Logger（Warning.Logger）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(string message)`
  （void Invoke（string message））
- `IAsyncResult BeginInvoke(string message, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（string message, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## WeakHashtable（WeakHashtable）

**继承**: Hashtable（Hashtable）

### 字段 (3)

- `IEqualityComparer _comparer`（IEqualityComparer _comparer）(偏移: 0x0)
- `long _lastGlobalMem`（long _last全局的Mem）(偏移: 0x38)
- `int _lastHashCount`（int _lastHash数量）(偏移: 0x40)

### 方法 (4)

- `void Clear()`
  （void 清除（））
- `void Remove(object key)`
  （void 移除（对象 key））
- `void SetWeak(object key, object value)`
  （void 集合Weak（object key, object value））
- `void ScavengeKeys()`
  （void ScavengeKeys（））

---

## WeakHashtable.EqualityWeakReference（WeakHashtable.EqualityWeak引用）

**继承**: WeakReference（Weak引用）

### 字段 (1)

- `int _hashCode`（int _hashCode）(偏移: 0x10)

### 方法 (2)

- `bool Equals(object o)`
  （布尔值 等于（对象 o））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## WeakReference（Weak引用）

**继承**: ISerializable（可序列化接口）

### 字段 (2)

- `bool isLongReference`（bool isLong引用）(偏移: 0x8)
- `GCHandle gcHandle`（GC句柄 gc句柄）(偏移: 0xC)

### 方法 (7)

- `void AllocateHandle(object target)`
  （void Allocate句柄（object target））
- `bool get_IsAlive()`
  （bool get_是否Alive（））
- `object get_Target()`
  （object get_目标（））
- `void set_Target(object value)`
  （void set_目标（object value））
- `bool get_TrackResurrection()`
  （bool get_TrackResurrection（））
- `void Finalize()`
  （void 终结（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））

---

## Weapon（武器）

**继承**: CFAnimator（CF动画器）

### 字段 (18)

- `WeaponData data`（武器数据 data）(偏移: 0x68)
- `List<RaycastHit> shootHitTemp`（List<RaycastHit> shoot命中Temp）(偏移: 0x6C)
- `List<DamageEventData> damageEventTemp`（List<伤害事件Data> damage事件Temp）(偏移: 0x70)
- `List<Weapon.KnifeHitData> knifeHitTemp`（List<Weapon.近战武器命中Data> knife命中Temp）(偏移: 0x74)
- `float knifeRangeMultiplier`（float knife范围Multiplier）(偏移: 0x0)
- `ObscuredBool moveDisabled`（模糊的布尔值 move禁用的）(偏移: 0x7C)
- `ObscuredBool jumpDisabled`（模糊的布尔值 jump禁用的）(偏移: 0x88)
- `ObscuredBool crouchDisabled`（模糊的布尔值 crouch禁用的）(偏移: 0x94)
- `ObscuredBool changeWpnDisabled`（模糊的布尔值 change武器禁用的）(偏移: 0xA0)
- `ObscuredBool forceWalk`（模糊的布尔值 forceWalk）(偏移: 0xAC)
- `ObscuredBool cameraRotDisabled`（模糊的布尔值 cameraRot禁用的）(偏移: 0xB8)
- `Vector3 charOffset`（三维向量 charOffset）(偏移: 0xC4)
- `MapGun bindMapTrigger`（地图枪械 bind映射触发器）(偏移: 0xD0)
- `bool newWpnTag`（bool new武器标签）(偏移: 0xD4)
- `Action<bool> Deploy_Listener`（Action<bool> Deploy_监听器）(偏移: 0xDC)
- `Action Setter_AmmoBG`（动作 Setter_弹药BG）(偏移: 0xE0)
- `Action<Player> NewValidOwner_Listener`（Action<Player> 新的ValidOwner_监听器）(偏移: 0xE4)
- `Action<Player> RemoveFromOwner_Listener`（Action<Player> 移除FromOwner_监听器）(偏移: 0xE8)

### 方法 (58)

- `bool get_isUsing()`
  （bool get_isUsing（））
- `bool get_isMyWeapon()`
  （bool get_isMyWeapon（））
- `bool get_isDead()`
  （布尔值 获取_是否死亡（））
- `bool get_fireBtnPressed()`
  （bool get_fireBtn按下的（））
- `void set_fireBtnPressed(bool value)`
  （void set_fireBtn按下的（bool value））
- `bool get_isMapGun()`
  （bool get_is映射枪械（））
- `void add_KnifeAttackHit_Listener(Action<int, Entity> value)`
  （void add_近战武器AttackHit_监听器（Action<int, Entity> value））
- `void remove_KnifeAttackHit_Listener(Action<int, Entity> value)`
  （void remove_近战武器AttackHit_监听器（Action<int, Entity> value））
- `void add_Deploy_Listener(Action<bool> value)`
  （void add_Deploy_监听器（Action<bool> value））
- `void remove_Deploy_Listener(Action<bool> value)`
  （void remove_Deploy_监听器（Action<bool> value））
- `void Update()`
  （void 更新（））
- `void UpdateDisabledSetting(PlayerWeapons wpns)`
  （void 更新禁用的设置（玩家武器 wpns））
- `void Init()`
  （void 初始化（））
- `void OnGenerateFromOwner()`
  （void 从所有者生成时（））
- `void Recycle(bool roundRecycle)`
  （void 回收（布尔值 循环回收））
- `void Deploy(bool noSelectAnim = False)`
  （void 部署（布尔值 无选择动画 = 假））
- `void UnDeploy(bool temporary = False)`
  （void 取消部署（布尔值 临时 = 假））
- `void ResetModeChange()`
  （void 重置模式Change（））
- `void PlayerViewSetting()`
  （void 玩家视图设置（））
- `void SynchronizeHand()`
  （void Synchronize手部（））
- `void AnimSpeedSetting()`
  （void 动画速度设置（））
- `void CrosshairSetting()`
  （void 准星设置（））
- `void SetMoveSpeedPenalty(float penalty)`
  （void 集合移动Speed惩罚（float penalty））
- `void SetCharacterAnim()`
  （void 集合角色动画（））
- `void RemoveFromOldOwner()`
  （void 从旧所有者移除（））
- `void OnSelectedFromWeaponPool()`
  （void On选中的FromWeapon池（））
- `void SetValidOwner()`
  （void 设置有效所有者（））
- `void OnFireBtnDown()`
  （void On开火Btn下（））
- `void OnFireBtnPressed()`
  （void On开火Btn按下的（））
- `void OnFireBtnUnPressed()`
  （void On开火BtnUn按下的（））
- `void OnSpecialBtnDown()`
  （void 特殊按钮按下时（））
- `void OnSpecialBtnPressed()`
  （void On特殊Btn按下的（））
- `void OnSpecialBtnUnPressed()`
  （void On特殊BtnUn按下的（））
- `void OnReloadBtnDown()`
  （void On换弹Btn下（））
- `void OnJumpBtnDown()`
  （void On跳跃Btn下（））
- `void SetTrigger(string name)`
  （void 集合触发器（string name））
- `void ResetTrigger(string name)`
  （void 重置触发器（string name））
- `void SetBool(string name, bool value)`
  （void 集合布尔值（string name, bool value））
- `void SetInteger(string name, int value)`
  （void 集合Integer（string name, int value））
- `void CrossFadeInFixedTime(string name, float time)`
  （void CrossFadeIn固定时间（string name, float time））
- `void Play(string animName, float normalizedTime)`
  （void 播放（string animName, float normalizedTime））
- `KnifeAttackData GetKnifeAttackData(int attackIndex)`
  （近战武器Attack数据 获取近战武器Attack数据（int attackIndex））
- `string GetKnifeHitSoundName(int attackIndex)`
  （string 获取近战武器命中音效名称（int attackIndex））
- `string GetKnifeHitEffectName(int attackIndex)`
  （string 获取近战武器命中特效名称（int attackIndex））
- `void CallKnifeAttack(int attackIndex, DamageBodyRatio damageBodyRatio)`
  （void Call近战武器Attack（int attackIndex, 伤害身体比率 damageBodyRatio））
- `int GetKnifeAttackSprIndex(int attackIndex)`
  （int 获取近战武器AttackSpr索引（int attackIndex））
- `void TriggerDmgEventAndClear()`
  （void 触发器Dmg事件And清除（））
- `bool ShouldDamage(Entity target)`
  （bool 应该伤害（实体 target））
- `void ProjectMissile(GameObject missilePrefab, Vector3 offset, Vector3 euler, Action<WPN_Missile> settingFunc)`
  （void ProjectMissile（游戏对象 missilePrefab, 三维向量 offset, 三维向量 euler, Action<WPN_Missile> settingFunc））
- `bool GiveUp(bool death = True)`
  （布尔值 放弃（布尔值 死亡 = 真））
- `void BotControl(Bot bot)`
  （void 机器人控制（机器人 bot））
- `void PlayCharacterShootAnim()`
  （void 播放角色射击动画（））
- `string GetWpnName()`
  （string 获取武器名称（））
- `WpnSpriteAsset GetWpnSpriteAsset()`
  （武器精灵资产 获取武器精灵资产（））
- `CharWpnAnimData GetCharWpnAnimData()`
  （Char武器动画数据 获取Char武器动画数据（））
- `bool CanGetInfinityAmmo()`
  （bool 能否获取无限弹药（））
- `void RemoveThisWeapon()`
  （void 移除ThisWeapon（））
- `bool ConsumeAmmo()`
  （bool Consume弹药（））

---

## Weapon.KnifeHitData（Weapon.近战武器命中数据）

### 字段 (3)

- `Transform bone`（变换 骨骼）(偏移: 0x0)
- `float distance`（浮点数 距离）(偏移: 0x4)
- `float angle`（float angle）(偏移: 0x8)

---

## Weapon.SlotType（Weapon.槽位类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## WeaponAsset（武器资产）

**继承**: ScriptableObject（脚本对象）

### 字段 (2)

- `bool loaded`（bool loaded）(偏移: 0xC)
- `List<GameObject> weaponList`（List<游戏Object> weapon列表）(偏移: 0x10)

### 方法 (1)

- `GameObject GetWeaponPrefab(int index)`
  （游戏对象 获取Weapon预制体（int index））

---

## WeaponBag（武器背包）

### 字段 (5)

- `ObscuredBool disabled`（模糊的布尔值 disabled）(偏移: 0x8)
- `ObscuredBool tooFarFromSpawnPos`（模糊的布尔值 tooFarFrom出生Pos）(偏移: 0x14)
- `bool[] available`（bool[] available）(偏移: 0x20)
- `int[][] weaponID`（int[][] weaponID）(偏移: 0x24)
- `int currentBagID`（int current背包ID）(偏移: 0x28)

### 方法 (3)

- `void LoadData(ClientData clientData)`
  （void 加载数据（客户端数据 clientData））
- `int GetRandomBagID()`
  （int 获取随机背包ID（））
- `bool EquipAnyVVIPWeapon()`
  （bool Equip任意VVIPWeapon（））

---

## WeaponClass（武器类别）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## WeaponData（武器数据）

**继承**: ScriptableObject（脚本对象）

### 字段 (18)

- `int wpnIndex`（int 武器索引）(偏移: 0xC)
- `WeaponClass wpnClass`（武器类别 武器类）(偏移: 0x10)
- `string weaponName`（string weapon名称）(偏移: 0x14)
- `PlayerViewData viewData`（玩家视图数据 view数据）(偏移: 0x18)
- `WpnSpriteAsset spriteAsset`（武器精灵资产 sprite资产）(偏移: 0x4C)
- `bool isVVIP`（bool isVVIP）(偏移: 0x7C)
- `float changeWeaponAnimRatio`（float changeWeapon动画比率）(偏移: 0x80)
- `string selectAnimName_C`（string select动画Name_C）(偏移: 0x84)
- `bool rapidChange`（bool rapidChange）(偏移: 0x88)
- `int targetSlot`（int target槽位）(偏移: 0x8C)
- `Weapon.SlotType slotType`（Weapon.槽位类型 slot类型）(偏移: 0x90)
- `CharWpnAnimData charWpnAnim`（Char武器动画数据 char武器动画）(偏移: 0x94)
- `float moveSpeedPenalty`（float moveSpeed惩罚）(偏移: 0xA0)
- `bool nanoModeLimited`（bool nano模式限制）(偏移: 0xA4)
- `string hitEffectName`（string hit特效名称）(偏移: 0xA8)
- `GameObject qvMdlPrefab`（游戏对象 qv模型预制体）(偏移: 0xAC)
- `BotControlData botControlData`（机器人控制数据 bot控制数据）(偏移: 0xB0)
- `ComponentData components`（组件数据 components）(偏移: 0xB4)

### 方法 (3)

- `Sprite GetKillMsgIcon(int index)`
  （精灵 获取击杀Msg图标（int index））
- `string GetWeaponName(int index)`
  （string 获取Weapon名称（int index））
- `bool GetWeaponSelectImage(int index, out Texture img1, out Texture img2)`
  （bool 获取Weapon选择图像（int index, out Texture img1, out Texture img2））

---

## WeaponData_Gun（WeaponData_枪械）

**继承**: WeaponData（武器数据）

### 字段 (39)

- `int clip`（int clip）(偏移: 0xB8)
- `int ammo`（整数 弹药）(偏移: 0xBC)
- `int clip_Nano`（int clip_纳米）(偏移: 0xC0)
- `int ammo_Nano`（int ammo_纳米）(偏移: 0xC4)
- `string shotSoundName`（string shot音效名称）(偏移: 0xC8)
- `float shotsPerMinute`（float shotsPerMinute）(偏移: 0xCC)
- `float fireAnimMultiplier`（float fire动画Multiplier）(偏移: 0xD0)
- `float reloadAnimRatio`（float reload动画比率）(偏移: 0xD4)
- `string reloadAnimName_C`（string reload动画Name_C）(偏移: 0xD8)
- `bool shootBullet`（bool shoot子弹）(偏移: 0xDC)
- `Vector3 bulletFxPos_L`（三维向量 bullet特效Pos_L）(偏移: 0xE0)
- `Vector3 bulletFxPos_R`（三维向量 bullet特效Pos_R）(偏移: 0xEC)
- `PostureFloat[] perturbMin`（姿态Float[] perturb最小）(偏移: 0xF8)
- `PostureFloat[] perturbMax`（姿态Float[] perturb最大）(偏移: 0xFC)
- `ChangeMovingRealSize changeMovingRealSize`（ChangeMovingReal大小 changeMovingReal大小）(偏移: 0x100)
- `DelayOneShootData delayOneShootTime`（延迟One射击数据 delayOne射击时间）(偏移: 0x114)
- `AmmoRecoverAndDecay[] shotReactYaw`（弹药恢复AndDecay[] shotReact偏航角）(偏移: 0x120)
- `AmmoRecoverAndDecay[] shotReactPitch`（弹药恢复AndDecay[] shotReact俯仰角）(偏移: 0x124)
- `PostureFloat[] detailPerturbShot`（姿态Float[] detail扰动射击）(偏移: 0x128)
- `PostureFloat[] detailReactPitchShot`（姿态Float[] detailReact俯仰角射击）(偏移: 0x12C)
- `PostureFloat[] detailReactYawShot`（姿态Float[] detailReact偏航角射击）(偏移: 0x130)
- `PostureFloat[] fullReactYaw`（姿态Float[] fullReact偏航角）(偏移: 0x134)
- `PostureFloat[] fullReactPitch`（姿态Float[] fullReact俯仰角）(偏移: 0x138)
- `SideReactDirect sideReactDirect`（侧面反应方向 sideReactDirect）(偏移: 0x13C)
- `AmmoRecoverAndDecay[] cameraYawAndPitch`（弹药恢复AndDecay[] camera偏航角And俯仰角）(偏移: 0x144)
- `float range`（浮点数 范围）(偏移: 0x148)
- `float ammoDamage`（float ammo伤害）(偏移: 0x14C)
- `float damageVariantionFactor`（float damage变化系数）(偏移: 0x150)
- `float damageFactorByDistance`（float damage系数By距离）(偏移: 0x154)
- `float wallShotDamageRatio`（float wall射击伤害比率）(偏移: 0x158)
- `DamageBodyRatio damageBodyRatio`（伤害身体比率 damage身体比率）(偏移: 0x15C)
- `KnifeAttackData[] knifeAttacks`（近战武器AttackData[] knifeAttacks）(偏移: 0x180)
- `string knifeAnimName`（string knife动画名称）(偏移: 0x184)
- `string knifeHitSoundName`（string knife命中音效名称）(偏移: 0x188)
- `DamageBodyRatio knifeDamageBodyRatio`（伤害身体比率 knife伤害身体比率）(偏移: 0x18C)
- `ZoomAction zoomAcion`（瞄准动作 zoomAcion）(偏移: 0x1B0)
- `float zoomInMoveSpeedPenalty`（float zoomIn移动Speed惩罚）(偏移: 0x1C0)
- `bool giveUpDisable`（bool give上禁用）(偏移: 0x1C4)
- `bool deathDropDisable`（bool deathDrop禁用）(偏移: 0x1C5)

### 方法 (3)

- `float get_shootIntervalTime()`
  （float get_shoot间隔时间（））
- `Sprite GetKillMsgIcon(int index)`
  （精灵 获取击杀Msg图标（int index））
- `bool GetWeaponSelectImage(int index, out Texture img1, out Texture img2)`
  （bool 获取Weapon选择图像（int index, out Texture img1, out Texture img2））

---

## WeaponData_Knife（WeaponData_近战武器）

**继承**: WeaponData（武器数据）

### 字段 (5)

- `string knifeAttackAnimName`（string knifeAttack动画名称）(偏移: 0xB8)
- `string knifeHitSoundName`（string knife命中音效名称）(偏移: 0xBC)
- `KnifeAttackData[] knifeAttacks`（近战武器AttackData[] knifeAttacks）(偏移: 0xC0)
- `DamageBodyRatio damageBodyRatio`（伤害身体比率 damage身体比率）(偏移: 0xC4)
- `Vector3 attackSpeed`（三维向量 attackSpeed）(偏移: 0xE8)

---

## WeaponLimited（Weapon限制）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## WeaponLogic（武器逻辑）

### 方法 (2)

- `bool CheckWall(Vector3 p1, Vector3 p2)`
  （bool 检查Wall（三维向量 p1, 三维向量 p2））
- `float RayPointDot(Ray ray, Vector3 point)`
  （float RayPointDot（Ray ray, 三维向量 point））

---

## WebProxyScriptElement（Web代理Script元素）

**继承**: ConfigurationElement（配置元素）

### 方法 (1)

- `ConfigurationPropertyCollection get_Properties()`
  （配置属性集合 获取_属性（））

---

## WebRequestModulesSection（Web请求ModulesSection）

**继承**: ConfigurationSection（配置节）

### 方法 (1)

- `ConfigurationPropertyCollection get_Properties()`
  （配置属性集合 获取_属性（））

---

## WebRequestUtils（Web请求Utils）

### 字段 (1)

- `Regex domainRegex`（Regex domainRegex）(偏移: 0x310330E6)

### 方法 (3)

- `string RedirectTo(string baseUri, string redirectUri)`
  （string RedirectTo（string baseUri, string redirectUri））
- `string MakeUriString(Uri targetUri, string targetUrl, bool prependProtocol)`
  （string MakeUri字符串（Uri targetUri, string targetUrl, bool prependProtocol））
- `string URLDecode(string encoded)`
  （string URLDecode（string encoded））

---

## WeightUtility（Weight工具）

### 方法 (1)

- `float NormalizeMixer(Playable mixer)`
  （float NormalizeMixer（Playable mixer））

---

## WellKnownClientTypeEntry（WellKnown客户端类型Entry）

**继承**: TypeEntry（类型项）

### 字段 (3)

- `Type obj_type`（类型 obj_type）(偏移: 0x10)
- `string obj_url`（string obj_url）(偏移: 0x14)
- `string app_url`（string app_url）(偏移: 0x18)

### 方法 (4)

- `string get_ApplicationUrl()`
  （string get_ApplicationUrl（））
- `Type get_ObjectType()`
  （类型 get_对象类型（））
- `string get_ObjectUrl()`
  （string get_对象Url（））
- `string ToString()`
  （字符串 转字符串（））

---

## WellKnownObjectMode（WellKnown对象模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## WellKnownServiceTypeEntry（WellKnown服务类型Entry）

**继承**: TypeEntry（类型项）

### 字段 (3)

- `Type obj_type`（类型 obj_type）(偏移: 0x10)
- `string obj_uri`（string obj_uri）(偏移: 0x14)
- `WellKnownObjectMode obj_mode`（WellKnown对象模式 obj_mode）(偏移: 0x18)

### 方法 (4)

- `WellKnownObjectMode get_Mode()`
  （WellKnown对象模式 get_模式（））
- `Type get_ObjectType()`
  （类型 get_对象类型（））
- `string get_ObjectUri()`
  （string get_对象Uri（））
- `string ToString()`
  （字符串 转字符串（））

---

## WhiteBalance（WhiteBalance）

**继承**: VolumeComponent, IPostProcessComponent（体积组件, I后处理组件）

### 字段 (2)

- `ClampedFloatParameter temperature`（Clamped浮点数Parameter temperature）(偏移: 0x1C)
- `ClampedFloatParameter tint`（Clamped浮点数Parameter tint）(偏移: 0x20)

### 方法 (2)

- `bool IsActive()`
  （布尔值 是否激活的（））
- `bool IsTileCompatible()`
  （布尔值 是否瓦片兼容（））

---

## Win32Exception（Win32Exception）

**继承**: ExternalException, ISerializable（外部的Exception, ISerializable）

### 字段 (2)

- `int nativeErrorCode`（int nativeErrorCode）(偏移: 0x44)
- `bool s_ErrorMessagesInitialized`（bool s_ErrorMessagesInitialized）(偏移: 0x0)

### 方法 (4)

- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））
- `string GetErrorMessage(int error)`
  （string 获取ErrorMessage（int error））
- `void InitializeErrorMessages()`
  （void 初始化ErrorMessages（））
- `void InitializeErrorMessages1()`
  （void 初始化ErrorMessages1（））

---

## Win32Native（Win32Native）

### 方法 (3)

- `string GetMessage(int hr)`
  （string 获取Message（int hr））
- `int MakeHRFromErrorCode(int errorCode)`
  （int MakeHRFromErrorCode（int errorCode））
- `uint GetCurrentProcessId()`
  （uint 获取当前处理Id（））

---

## Win32Native.WIN32_FIND_DATA（Win32Native.WIN32_FIND_DATA）

### 字段 (2)

- `int dwFileAttributes`（int dw文件Attributes）(偏移: 0x8)
- `string cFileName`（string c文件名称）(偏移: 0xC)

---

## Win32RegistryApi（Win32RegistryApi）

**继承**: IRegistryApi（IRegistryApi）

### 字段 (1)

- `int NativeBytesPerCharacter`（int NativeBytesPer角色）(偏移: 0x8)

### 方法 (21)

- `int RegCloseKey(IntPtr keyHandle)`
  （int Reg关闭键（整数Ptr keyHandle））
- `int RegFlushKey(IntPtr keyHandle)`
  （int RegFlush键（整数Ptr keyHandle））
- `int RegOpenKeyEx(IntPtr keyBase, string keyName, IntPtr reserved, int access, out IntPtr keyHandle)`
  （int Reg打开键Ex（整数Ptr keyBase, string keyName, 整数Ptr reserved, int access, out IntPtr keyHandle））
- `int RegEnumKeyEx(IntPtr keyHandle, int dwIndex, char* lpName, ref int lpcbName, int[] lpReserved, [Out] StringBuilder lpClass, int[] lpcbClass, long[] lpftLastWriteTime)`
  （int RegEnum键Ex（整数Ptr keyHandle, int dwIndex, char* lpName, ref int lpcbName, int[] lpReserved, [Out] StringBuilder lpClass, int[] lpcbClass, long[] lpftLastWriteTime））
- `int RegQueryValueEx(IntPtr keyBase, string valueName, IntPtr reserved, ref RegistryValueKind type, IntPtr zero, ref int dataSize)`
  （int RegQuery值Ex（整数Ptr keyBase, string valueName, 整数Ptr reserved, ref RegistryValueKind type, 整数Ptr zero, ref int dataSize））
- `int RegQueryValueEx(IntPtr keyBase, string valueName, IntPtr reserved, ref RegistryValueKind type, [Out] byte[] data, ref int dataSize)`
  （int RegQuery值Ex（整数Ptr keyBase, string valueName, 整数Ptr reserved, ref RegistryValueKind type, [Out] byte[] data, ref int dataSize））
- `int RegQueryValueEx(IntPtr keyBase, string valueName, IntPtr reserved, ref RegistryValueKind type, ref int data, ref int dataSize)`
  （int RegQuery值Ex（整数Ptr keyBase, string valueName, 整数Ptr reserved, ref RegistryValueKind type, ref int data, ref int dataSize））
- `int RegQueryValueEx(IntPtr keyBase, string valueName, IntPtr reserved, ref RegistryValueKind type, ref long data, ref int dataSize)`
  （int RegQuery值Ex（整数Ptr keyBase, string valueName, 整数Ptr reserved, ref RegistryValueKind type, ref long data, ref int dataSize））
- `int RegQueryInfoKey(IntPtr hKey, [Out] StringBuilder lpClass, int[] lpcbClass, IntPtr lpReserved_MustBeZero, ref int lpcSubKeys, int[] lpcbMaxSubKeyLen, int[] lpcbMaxClassLen, ref int lpcValues, int[] lpcbMaxValueNameLen, int[] lpcbMaxValueLen, int[] lpcbSecurityDescriptor, int[] lpftLastWriteTime)`
  （int RegQuery信息键（整数Ptr hKey, [Out] StringBuilder lpClass, int[] lpcbClass, 整数Ptr lpReserved_MustBeZero, ref int lpcSubKeys, int[] lpcbMaxSubKeyLen, int[] lpcbMaxClassLen, ref int lpcValues, int[] lpcbMaxValueNameLen, int[] lpcbMaxValueLen, int[] lpcbSecurityDescriptor, int[] lpftLastWriteTime））
- `IntPtr GetHandle(RegistryKey key)`
  （整数Ptr 获取句柄（Registry键 key））
- `bool IsHandleValid(RegistryKey key)`
  （bool 是否句柄Valid（Registry键 key））
- `object GetValue(RegistryKey rkey, string name, object defaultValue, RegistryValueOptions options)`
  （object 获取值（Registry键 rkey, string name, object defaultValue, Registry值Options options））
- `int GetBinaryValue(RegistryKey rkey, string name, RegistryValueKind type, out byte[] data, int size)`
  （int 获取Binary值（Registry键 rkey, string name, Registry值Kind type, out byte[] data, int size））
- `int SubKeyCount(RegistryKey rkey)`
  （int 子键数量（Registry键 rkey））
- `RegistryKey OpenSubKey(RegistryKey rkey, string keyName, bool writable)`
  （Registry键 打开子键（Registry键 rkey, string keyName, bool writable））
- `void Flush(RegistryKey rkey)`
  （void Flush（Registry键 rkey））
- `void Close(RegistryKey rkey)`
  （void 关闭（Registry键 rkey））
- `string[] GetSubKeyNames(RegistryKey rkey)`
  （string[] 获取子键Names（Registry键 rkey））
- `void GenerateException(int errorCode)`
  （void GenerateException（int errorCode））
- `string ToString(RegistryKey rkey)`
  （string To字符串（Registry键 rkey））
- `string CombineName(RegistryKey rkey, string localName)`
  （string Combine名称（Registry键 rkey, string localName））

---

## WindingRule（WindingRule）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## WindowsConsoleDriver（WindowsConsoleDriver）

**继承**: IConsoleDriver（IConsoleDriver）

### 字段 (3)

- `IntPtr inputHandle`（整数Ptr input句柄）(偏移: 0x8)
- `IntPtr outputHandle`（整数Ptr output句柄）(偏移: 0xC)
- `short defaultAttribute`（short defaultAttribute）(偏移: 0x10)

### 方法 (5)

- `ConsoleKeyInfo ReadKey(bool intercept)`
  （控制台键信息 读取键（布尔值 拦截））
- `bool IsModifierKey(short virtualKeyCode)`
  （bool 是否修改器键（short virtualKeyCode））
- `IntPtr GetStdHandle(Handles handle)`
  （整数Ptr 获取Std句柄（Handles handle））
- `bool GetConsoleScreenBufferInfo(IntPtr handle, out ConsoleScreenBufferInfo info)`
  （bool 获取Console屏幕的缓冲区信息（整数Ptr handle, out ConsoleScreenBufferInfo info））
- `bool ReadConsoleInput(IntPtr handle, out InputRecord record, int length, out int nread)`
  （bool ReadConsole输入（整数Ptr handle, out InputRecord record, int length, out int nread））

---

## WindowsStoreCompatibility（Windows商店Compatibility）

### 方法 (2)

- `Type GetTypeFromInfo(Type type)`
  （类型 获取类型From信息（类型 type））
- `Type GetTypeInfo(Type type)`
  （类型 获取类型信息（类型 type））

---

## WorkItem（Work项目）

### 字段 (8)

- `byte[] buffer`（byte[] buffer）(偏移: 0x8)
- `byte[] compressed`（byte[] compressed）(偏移: 0xC)
- `int crc`（int crc）(偏移: 0x10)
- `int index`（整数 索引）(偏移: 0x14)
- `int ordinal`（int ordinal）(偏移: 0x18)
- `int inputBytesAvailable`（int inputBytesAvailable）(偏移: 0x1C)
- `int compressedBytesAvailable`（int compressedBytesAvailable）(偏移: 0x20)
- `ZlibCodec compressor`（ZlibCodec compressor）(偏移: 0x24)

---

## WorkItemProcessor（Work项目Processor）

**继承**: IWorkItemContext（IWork项目Context）

### 字段 (4)

- `AstarPath astar`（Astar路径 astar）(偏移: 0xC)
- `WorkItemProcessor.IndexedQueue<AstarWorkItem> workItems`（Work项目Processor.IndexedQueue<AstarWorkItem> workItems）(偏移: 0x10)
- `bool queuedWorkItemFloodFill`（bool queuedWork项目FloodFill）(偏移: 0x14)
- `bool anyGraphsDirty`（bool anyGraphsDirty）(偏移: 0x15)

### 方法 (9)

- `bool get_workItemsInProgressRightNow()`
  （bool get_workItemsInProgress右Now（））
- `void set_workItemsInProgressRightNow(bool value)`
  （void set_workItemsInProgress右Now（bool value））
- `bool get_anyQueued()`
  （bool get_anyQueued（））
- `bool get_workItemsInProgress()`
  （bool get_workItemsInProgress（））
- `void set_workItemsInProgress(bool value)`
  （void set_workItemsInProgress（bool value））
- `void EnsureValidFloodFill()`
  （void EnsureValidFloodFill（））
- `void OnFloodFill()`
  （void OnFloodFill（））
- `void AddWorkItem(AstarWorkItem item)`
  （void 添加Work项目（AstarWork项目 item））
- `bool ProcessWorkItems(bool force)`
  （bool 处理WorkItems（bool force））

---

## WpnComponent（武器组件）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (1)

- `Weapon wpn`（Weapon 武器）(偏移: 0xC)

### 方法 (2)

- `Player get_owner()`
  （玩家 get_owner（））
- `void Init(Weapon wpn)`
  （void 初始化（武器 wpn））

---

## WpnDataExpand（武器数据Expand）

### 方法 (3)

- `bool IsMainWeapon(WeaponClass wpnClass)`
  （bool 是否主要的Weapon（武器类别 wpnClass））
- `bool IsThrowWeapon(WeaponClass wpnClass)`
  （bool 是否投掷Weapon（武器类别 wpnClass））
- `int GetSlotID(WeaponClass wpnClass)`
  （int 获取槽位ID（武器类别 wpnClass））

---

## WpnSpriteAsset（武器精灵资产）

### 字段 (10)

- `Texture background`（纹理 background）(偏移: 0x0)
- `Color backgroundColor`（颜色 background颜色）(偏移: 0x4)
- `Texture effect`（纹理 effect）(偏移: 0x14)
- `Texture line`（纹理 line）(偏移: 0x18)
- `Texture select`（纹理 select）(偏移: 0x1C)
- `Texture select2`（纹理 select2）(偏移: 0x20)
- `Texture bagIcon`（纹理 bag图标）(偏移: 0x24)
- `Sprite killMsgIcon`（精灵 killMsg图标）(偏移: 0x28)
- `Sprite killMsgIcon2`（精灵 killMsgIcon2）(偏移: 0x2C)
- `WpnSpriteAsset Null`（武器精灵资产 Null）(偏移: 0x0)

### 方法 (1)

- `void GetBigIcon(out Texture icon1, out Texture icon2)`
  （void 获取Big图标（out Texture icon1, out Texture icon2））

---

## WriteDelegate（Write委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(string entryName, Stream stream)`
  （void Invoke（string entryName, 流 stream））
- `IAsyncResult BeginInvoke(string entryName, Stream stream, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（string entryName, 流 stream, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## WriteObjectInfo（Write对象信息）

### 字段 (17)

- `int objectInfoId`（int object信息Id）(偏移: 0x8)
- `object obj`（object obj）(偏移: 0xC)
- `Type objectType`（类型 object类型）(偏移: 0x10)
- `bool isSi`（bool isSi）(偏移: 0x14)
- `bool isNamed`（bool isNamed）(偏移: 0x0)
- `bool isTyped`（bool isTyped）(偏移: 0x0)
- `bool isArray`（bool is数组）(偏移: 0x0)
- `SerializationInfo si`（Serialization信息 si）(偏移: 0x0)
- `SerObjectInfoCache cache`（Ser对象信息缓存 cache）(偏移: 0x1C)
- `object[] memberData`（object[] member数据）(偏移: 0x20)
- `ISerializationSurrogate serializationSurrogate`（ISerializationSurrogate serializationSurrogate）(偏移: 0x24)
- `StreamingContext context`（StreamingContext context）(偏移: 0x28)
- `SerObjectInfoInit serObjectInfoInit`（Ser对象信息初始化 ser对象信息初始化）(偏移: 0x30)
- `long objectId`（long objectId）(偏移: 0x38)
- `long assemId`（long assemId）(偏移: 0x40)
- `string binderTypeName`（string binder类型名称）(偏移: 0x48)
- `string binderAssemblyString`（string binderAssembly字符串）(偏移: 0x4C)

### 方法 (17)

- `void ObjectEnd()`
  （void 对象结束（））
- `void InternalInit()`
  （void 内部的初始化（））
- `WriteObjectInfo Serialize(object obj, ISurrogateSelector surrogateSelector, StreamingContext context, SerObjectInfoInit serObjectInfoInit, IFormatterConverter converter, ObjectWriter objectWriter, SerializationBinder binder)`
  （Write对象信息 Serialize（object obj, ISurrogateSelector surrogateSelector, StreamingContext context, Ser对象信息初始化 serObjectInfoInit, IFormatterConverter converter, 对象写入器 objectWriter, SerializationBinder binder））
- `void InitSerialize(object obj, ISurrogateSelector surrogateSelector, StreamingContext context, SerObjectInfoInit serObjectInfoInit, IFormatterConverter converter, ObjectWriter objectWriter, SerializationBinder binder)`
  （void 初始化Serialize（object obj, ISurrogateSelector surrogateSelector, StreamingContext context, Ser对象信息初始化 serObjectInfoInit, IFormatterConverter converter, 对象写入器 objectWriter, SerializationBinder binder））
- `WriteObjectInfo Serialize(Type objectType, ISurrogateSelector surrogateSelector, StreamingContext context, SerObjectInfoInit serObjectInfoInit, IFormatterConverter converter, SerializationBinder binder)`
  （Write对象信息 Serialize（类型 objectType, ISurrogateSelector surrogateSelector, StreamingContext context, Ser对象信息初始化 serObjectInfoInit, IFormatterConverter converter, SerializationBinder binder））
- `void InitSerialize(Type objectType, ISurrogateSelector surrogateSelector, StreamingContext context, SerObjectInfoInit serObjectInfoInit, IFormatterConverter converter, SerializationBinder binder)`
  （void 初始化Serialize（类型 objectType, ISurrogateSelector surrogateSelector, StreamingContext context, Ser对象信息初始化 serObjectInfoInit, IFormatterConverter converter, SerializationBinder binder））
- `void InitSiWrite()`
  （void 初始化SiWrite（））
- `void CheckTypeForwardedFrom(SerObjectInfoCache cache, Type objectType, string binderAssemblyString)`
  （void 检查类型ForwardedFrom（Ser对象信息缓存 cache, 类型 objectType, string binderAssemblyString））
- `void InitNoMembers()`
  （void 初始化NoMembers（））
- `void InitMemberInfo()`
  （void 初始化Member信息（））
- `string GetTypeFullName()`
  （string 获取类型满名称（））
- `string GetAssemblyString()`
  （string 获取Assembly字符串（））
- `void InvokeSerializationBinder(SerializationBinder binder)`
  （void InvokeSerializationBinder（SerializationBinder binder））
- `Type GetMemberType(MemberInfo objMember)`
  （类型 获取Member类型（Member信息 objMember））
- `void GetMemberInfo(out string[] outMemberNames, out Type[] outMemberTypes, out object[] outMemberData)`
  （void 获取Member信息（out string[] outMemberNames, out Type[] outMemberTypes, out object[] outMemberData））
- `WriteObjectInfo GetObjectInfo(SerObjectInfoInit serObjectInfoInit)`
  （Write对象信息 获取对象信息（Ser对象信息初始化 serObjectInfoInit））
- `void PutObjectInfo(SerObjectInfoInit serObjectInfoInit, WriteObjectInfo objectInfo)`
  （void Put对象信息（Ser对象信息初始化 serObjectInfoInit, Write对象信息 objectInfo））

---

## X509BasicConstraintsExtension（X509BasicConstraints扩展）

**继承**: X509Extension（X509扩展）

### 字段 (4)

- `bool _certificateAuthority`（bool _certificateAuthority）(偏移: 0x14)
- `bool _hasPathLengthConstraint`（bool _has路径LengthConstraint）(偏移: 0x15)
- `int _pathLengthConstraint`（int _pathLengthConstraint）(偏移: 0x18)
- `AsnDecodeStatus _status`（AsnDecodeStatus _status）(偏移: 0x1C)

### 方法 (7)

- `bool get_CertificateAuthority()`
  （bool get_CertificateAuthority（））
- `bool get_HasPathLengthConstraint()`
  （bool get_是否有路径LengthConstraint（））
- `int get_PathLengthConstraint()`
  （int get_路径LengthConstraint（））
- `void CopyFrom(AsnEncodedData asnEncodedData)`
  （void 复制自（Asn编码数据 asnEncodedData））
- `AsnDecodeStatus Decode(byte[] extension)`
  （AsnDecodeStatus Decode（byte[] extension））
- `byte[] Encode()`
  （byte[] Encode（））
- `string ToString(bool multiLine)`
  （字符串 转字符串（布尔值 多行））

---

## X509EnhancedKeyUsageExtension（X509Enhanced键Usage扩展）

**继承**: X509Extension（X509扩展）

### 字段 (2)

- `OidCollection _enhKeyUsage`（OidCollection _enh键Usage）(偏移: 0x14)
- `AsnDecodeStatus _status`（AsnDecodeStatus _status）(偏移: 0x18)

### 方法 (3)

- `void CopyFrom(AsnEncodedData asnEncodedData)`
  （void 复制自（Asn编码数据 asnEncodedData））
- `AsnDecodeStatus Decode(byte[] extension)`
  （AsnDecodeStatus Decode（byte[] extension））
- `string ToString(bool multiLine)`
  （字符串 转字符串（布尔值 多行））

---

## X509Extension（X509扩展）

**继承**: AsnEncodedData（AsnEncoded数据）

### 字段 (1)

- `bool _critical`（bool _critical）(偏移: 0x10)

### 方法 (4)

- `bool get_Critical()`
  （bool get_Critical（））
- `void set_Critical(bool value)`
  （void set_Critical（bool value））
- `void CopyFrom(AsnEncodedData asnEncodedData)`
  （void 复制自（Asn编码数据 asnEncodedData））
- `string FormatUnkownData(byte[] data)`
  （string 格式化Unkown数据（byte[] data））

---

## X509KeyUsageExtension（X509键Usage扩展）

**继承**: X509Extension（X509扩展）

### 字段 (2)

- `X509KeyUsageFlags _keyUsages`（X509键UsageFlags _keyUsages）(偏移: 0x14)
- `AsnDecodeStatus _status`（AsnDecodeStatus _status）(偏移: 0x18)

### 方法 (6)

- `X509KeyUsageFlags get_KeyUsages()`
  （X509键UsageFlags get_键Usages（））
- `void CopyFrom(AsnEncodedData asnEncodedData)`
  （void 复制自（Asn编码数据 asnEncodedData））
- `X509KeyUsageFlags GetValidFlags(X509KeyUsageFlags flags)`
  （X509键UsageFlags 获取ValidFlags（X509键UsageFlags flags））
- `AsnDecodeStatus Decode(byte[] extension)`
  （AsnDecodeStatus Decode（byte[] extension））
- `byte[] Encode()`
  （byte[] Encode（））
- `string ToString(bool multiLine)`
  （字符串 转字符串（布尔值 多行））

---

## X509KeyUsageFlags（X509键UsageFlags）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## X509SubjectKeyIdentifierExtension（X509Subject键Identifier扩展）

**继承**: X509Extension（X509扩展）

### 字段 (3)

- `byte[] _subjectKeyIdentifier`（byte[] _subject键Identifier）(偏移: 0x14)
- `string _ski`（string _ski）(偏移: 0x18)
- `AsnDecodeStatus _status`（AsnDecodeStatus _status）(偏移: 0x1C)

### 方法 (8)

- `string get_SubjectKeyIdentifier()`
  （string get_Subject键Identifier（））
- `void CopyFrom(AsnEncodedData asnEncodedData)`
  （void 复制自（Asn编码数据 asnEncodedData））
- `byte FromHexChar(char c)`
  （byte FromHexChar（char c））
- `byte FromHexChars(char c1, char c2)`
  （byte FromHexChars（char c1, char c2））
- `byte[] FromHex(string hex)`
  （byte[] FromHex（string hex））
- `AsnDecodeStatus Decode(byte[] extension)`
  （AsnDecodeStatus Decode（byte[] extension））
- `byte[] Encode()`
  （byte[] Encode（））
- `string ToString(bool multiLine)`
  （字符串 转字符串（布尔值 多行））

---

## X509SubjectKeyIdentifierHashAlgorithm（X509Subject键IdentifierHashAlgorithm）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## X509Utils（X509Utils）

### 方法 (2)

- `string FindOidInfo(uint keyType, string keyValue, OidGroup oidGroup)`
  （string 查找Oid信息（uint keyType, string keyValue, Oid组 oidGroup））
- `string FindOidInfoWithFallback(uint key, string value, OidGroup group)`
  （string 查找Oid信息WithFallback（uint key, string value, Oid组 group））

---

## XPath（X路径）

**继承**: ABPath（AB路径）

### 字段 (1)

- `PathEndingCondition endingCondition`（路径EndingCondition endingCondition）(偏移: 0xCC)

### 方法 (6)

- `XPath Construct(Vector3 start, Vector3 end, OnPathDelegate callback)`
  （X路径 Construct（三维向量 start, 三维向量 end, On路径委托 callback））
- `void Reset()`
  （void 重置（））
- `bool EndPointGridGraphSpecialCase(GraphNode endNode)`
  （bool 结束Point网格Graph特殊Case（Graph节点 endNode））
- `void CompletePathIfStartIsValidTarget()`
  （void Complete路径If开始是否Valid目标（））
- `void ChangeEndNode(GraphNode target)`
  （void Change结束节点（Graph节点 target））
- `void CalculateStep(long targetTick)`
  （void 计算步骤（长整数 targetTick））

---

## XRDevice（XRDevice）

### 字段 (1)

- `Action<string> deviceLoaded`（Action<string> deviceLoaded）(偏移: 0x22C)

### 方法 (1)

- `void InvokeDeviceLoaded(string loadedDeviceName)`
  （void InvokeDeviceLoaded（string loadedDeviceName））

---

## XRDisplaySubsystem（XRDisplaySubsystem）

**继承**: IntegratedSubsystem<XRDisplaySubsystemDescriptor>（IntegratedSubsystem<XRDisplaySubsystemDescriptor>）

### 字段 (1)

- `Action<bool> displayFocusChanged`（Action<bool> display聚焦Changed）(偏移: 0x10)

### 方法 (20)

- `void InvokeDisplayFocusChanged(bool focus)`
  （void InvokeDisplay聚焦Changed（bool focus））
- `void set_scaleOfAllRenderTargets(float value)`
  （void set_scaleOf所有RenderTargets（float value））
- `void set_zNear(float value)`
  （void set_zNear（float value））
- `void set_zFar(float value)`
  （void set_zFar（float value））
- `void set_sRGB(bool value)`
  （void set_sRGB颜色（bool value））
- `void set_textureLayout(XRDisplaySubsystem.TextureLayout value)`
  （void set_textureLayout（XRDisplaySubsystem.纹理Layout value））
- `void SetMSAALevel(int level)`
  （void 集合MSAA等级（int level））
- `void set_disableLegacyRenderer(bool value)`
  （void set_disableLegacy渲染器（bool value））
- `int GetRenderPassCount()`
  （int 获取RenderPass数量（））
- `void GetRenderPass(int renderPassIndex, out XRDisplaySubsystem.XRRenderPass renderPass)`
  （void 获取RenderPass（int renderPassIndex, out XRDisplaySubsystem.XRRenderPass renderPass））
- `bool Internal_TryGetRenderPass(int renderPassIndex, out XRDisplaySubsystem.XRRenderPass renderPass)`
  （bool Internal_Try获取RenderPass（int renderPassIndex, out XRDisplaySubsystem.XRRenderPass renderPass））
- `void EndRecordingIfLateLatched(Camera camera)`
  （void 结束RecordingIf延迟Latched（摄像机 camera））
- `bool Internal_TryEndRecordingIfLateLatched(Camera camera)`
  （bool Internal_Try结束RecordingIf延迟Latched（摄像机 camera））
- `void BeginRecordingIfLateLatched(Camera camera)`
  （void BeginRecordingIf延迟Latched（摄像机 camera））
- `bool Internal_TryBeginRecordingIfLateLatched(Camera camera)`
  （bool Internal_TryBeginRecordingIf延迟Latched（摄像机 camera））
- `void GetCullingParameters(Camera camera, int cullingPassIndex, out ScriptableCullingParameters scriptableCullingParameters)`
  （void 获取CullingParameters（摄像机 camera, int cullingPassIndex, out ScriptableCullingParameters scriptableCullingParameters））
- `bool Internal_TryGetCullingParams(Camera camera, int cullingPassIndex, out ScriptableCullingParameters scriptableCullingParameters)`
  （bool Internal_Try获取CullingParams（摄像机 camera, int cullingPassIndex, out ScriptableCullingParameters scriptableCullingParameters））
- `int GetPreferredMirrorBlitMode()`
  （int 获取PreferredMirrorBlit模式（））
- `bool GetMirrorViewBlitDesc(RenderTexture mirrorRt, out XRDisplaySubsystem.XRMirrorViewBlitDesc outDesc, int mode)`
  （bool 获取Mirror视图BlitDesc（Render纹理 mirrorRt, out XRDisplaySubsystem.XRMirrorViewBlitDesc outDesc, int mode））
- `bool AddGraphicsThreadMirrorViewBlit(CommandBuffer cmd, bool allowGraphicsStateInvalidate, int mode)`
  （bool 添加GraphicsThreadMirror视图Blit（Command缓冲区 cmd, bool allowGraphicsStateInvalidate, int mode））

---

## XRDisplaySubsystem.TextureLayout（XRDisplaySubsystem.纹理Layout）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## XRDisplaySubsystem.XRBlitParams（XRDisplaySubsystem.XRBlitParams）

### 字段 (4)

- `RenderTexture srcTex`（Render纹理 srcTex）(偏移: 0x0)
- `int srcTexArraySlice`（int srcTex数组Slice）(偏移: 0x4)
- `Rect srcRect`（Rect srcRect）(偏移: 0x8)
- `Rect destRect`（Rect destRect）(偏移: 0x18)

---

## XRDisplaySubsystem.XRMirrorViewBlitDesc（XRDisplaySubsystem.XRMirror视图BlitDesc）

### 字段 (4)

- `IntPtr displaySubsystemInstance`（整数Ptr displaySubsystem实例）(偏移: 0x0)
- `bool nativeBlitAvailable`（bool nativeBlitAvailable）(偏移: 0x4)
- `bool nativeBlitInvalidStates`（bool nativeBlitInvalidStates）(偏移: 0x5)
- `int blitParamsCount`（int blitParams数量）(偏移: 0x8)

### 方法 (2)

- `void GetBlitParameter(int blitParameterIndex, out XRDisplaySubsystem.XRBlitParams blitParameter)`
  （void 获取BlitParameter（int blitParameterIndex, out XRDisplaySubsystem.XRBlitParams blitParameter））
- `void GetBlitParameter_Injected(ref XRDisplaySubsystem.XRMirrorViewBlitDesc _unity_self, int blitParameterIndex, out XRDisplaySubsystem.XRBlitParams blitParameter)`
  （void 获取BlitParameter_Injected（ref XRDisplaySubsystem.XRMirrorViewBlitDesc _unity_self, int blitParameterIndex, out XRDisplaySubsystem.XRBlitParams blitParameter））

---

## XRDisplaySubsystem.XRRenderParameter（XRDisplaySubsystem.XRRenderParameter）

### 字段 (7)

- `Matrix4x4 view`（Matrix4x4 view）(偏移: 0x0)
- `Matrix4x4 projection`（Matrix4x4 projection）(偏移: 0x40)
- `Rect viewport`（Rect viewport）(偏移: 0x80)
- `Mesh occlusionMesh`（网格 occlusion网格）(偏移: 0x90)
- `int textureArraySlice`（int texture数组Slice）(偏移: 0x94)
- `Matrix4x4 previousView`（Matrix4x4 previous视图）(偏移: 0x98)
- `bool isPreviousViewValid`（bool is上一个视图Valid）(偏移: 0xD8)

---

## XRDisplaySubsystem.XRRenderPass（XRDisplaySubsystem.XRRenderPass）

### 字段 (9)

- `IntPtr displaySubsystemInstance`（整数Ptr displaySubsystem实例）(偏移: 0x0)
- `int renderPassIndex`（int renderPass索引）(偏移: 0x4)
- `RenderTargetIdentifier renderTarget`（Render目标Identifier render目标）(偏移: 0x8)
- `RenderTextureDescriptor renderTargetDesc`（Render纹理Descriptor render目标Desc）(偏移: 0x24)
- `bool hasMotionVectorPass`（bool hasMotion向量Pass）(偏移: 0x58)
- `RenderTargetIdentifier motionVectorRenderTarget`（Render目标Identifier motion向量Render目标）(偏移: 0x5C)
- `RenderTextureDescriptor motionVectorRenderTargetDesc`（Render纹理Descriptor motion向量Render目标Desc）(偏移: 0x78)
- `bool shouldFillOutDepth`（bool shouldFillOut深度）(偏移: 0xAC)
- `int cullingPassIndex`（int cullingPass索引）(偏移: 0xB0)

### 方法 (4)

- `void GetRenderParameter(Camera camera, int renderParameterIndex, out XRDisplaySubsystem.XRRenderParameter renderParameter)`
  （void 获取RenderParameter（摄像机 camera, int renderParameterIndex, out XRDisplaySubsystem.XRRenderParameter renderParameter））
- `int GetRenderParameterCount()`
  （int 获取RenderParameter数量（））
- `void GetRenderParameter_Injected(ref XRDisplaySubsystem.XRRenderPass _unity_self, Camera camera, int renderParameterIndex, out XRDisplaySubsystem.XRRenderParameter renderParameter)`
  （void 获取RenderParameter_Injected（ref XRDisplaySubsystem.XRRenderPass _unity_self, 摄像机 camera, int renderParameterIndex, out XRDisplaySubsystem.XRRenderParameter renderParameter））
- `int GetRenderParameterCount_Injected(ref XRDisplaySubsystem.XRRenderPass _unity_self)`
  （int 获取RenderParameterCount_Injected（ref XRDisplaySubsystem.XRRenderPass _unity_self））

---

## XRGraphics（XRGraphics）

### 方法 (11)

- `float get_eyeTextureResolutionScale()`
  （float get_eye纹理Resolution缩放（））
- `void set_eyeTextureResolutionScale(float value)`
  （void set_eye纹理Resolution缩放（float value））
- `float get_renderViewportScale()`
  （float get_renderViewport缩放（））
- `bool get_enabled()`
  （布尔值 获取_已启用（））
- `bool get_isDeviceActive()`
  （bool get_isDevice激活的（））
- `string get_loadedDeviceName()`
  （string get_loadedDevice名称（））
- `string[] get_supportedDevices()`
  （string[] get_supportedDevices（））
- `XRGraphics.StereoRenderingMode get_stereoRenderingMode()`
  （XRGraphics.StereoRendering模式 get_stereoRendering模式（））
- `RenderTextureDescriptor get_eyeTextureDesc()`
  （Render纹理Descriptor get_eye纹理Desc（））
- `int get_eyeTextureWidth()`
  （int get_eye纹理宽度（））
- `int get_eyeTextureHeight()`
  （int get_eye纹理高度（））

---

## XRGraphics.StereoRenderingMode（XRGraphics.StereoRendering模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## XRGraphicsAutomatedTests（XRGraphicsAutomatedTests）

### 字段 (1)

- `bool running`（bool running）(偏移: 0x1)

### 方法 (2)

- `bool get_activatedFromCommandLine()`
  （bool get_activatedFromCommandLine（））
- `bool get_enabled()`
  （布尔值 获取_已启用（））

---

## XRInputSubsystem（XR输入Subsystem）

**继承**: IntegratedSubsystem<XRInputSubsystemDescriptor>（IntegratedSubsystem<XR输入SubsystemDescriptor>）

### 字段 (2)

- `Action<XRInputSubsystem> trackingOriginUpdated`（Action<XR输入Subsystem> trackingOriginUpdated）(偏移: 0x10)
- `Action<XRInputSubsystem> boundaryChanged`（Action<XR输入Subsystem> boundaryChanged）(偏移: 0x14)

### 方法 (2)

- `void InvokeTrackingOriginUpdatedEvent(IntPtr internalPtr)`
  （void InvokeTrackingOriginUpdated事件（整数Ptr internalPtr））
- `void InvokeBoundaryChangedEvent(IntPtr internalPtr)`
  （void InvokeBoundaryChanged事件（整数Ptr internalPtr））

---

## XRLayout（XRLayout）

### 字段 (2)

- `Camera camera`（摄像机 camera）(偏移: 0x0)
- `XRSystem xrSystem`（XR系统 xr系统）(偏移: 0x4)

### 方法 (2)

- `XRPass CreatePass(XRPassCreateInfo passCreateInfo)`
  （XRPass 创建Pass（XRPass创建信息 passCreateInfo））
- `void AddViewToPass(XRViewCreateInfo viewCreateInfo, XRPass pass)`
  （void 添加视图ToPass（XR视图创建信息 viewCreateInfo, XRPass pass））

---

## XRMeshSubsystem（XR网格Subsystem）

**继承**: IntegratedSubsystem<XRMeshSubsystemDescriptor>（IntegratedSubsystem<XR网格SubsystemDescriptor>）

### 方法 (1)

- `void InvokeMeshReadyDelegate(MeshGenerationResult result, Action<MeshGenerationResult> onMeshGenerationComplete)`
  （void Invoke网格Ready委托（网格GenerationResult result, Action<网格GenerationResult> onMeshGenerationComplete））

---

## XRNode（XR节点）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## XRNodeState（XR节点状态）

### 字段 (10)

- `XRNode m_Type`（XR节点 m_类型）(偏移: 0x0)
- `AvailableTrackingData m_AvailableFields`（AvailableTracking数据 m_AvailableFields）(偏移: 0x4)
- `Vector3 m_Position`（三维向量 m_位置）(偏移: 0x8)
- `Quaternion m_Rotation`（四元数 m_旋转）(偏移: 0x14)
- `Vector3 m_Velocity`（三维向量 m_速度）(偏移: 0x24)
- `Vector3 m_AngularVelocity`（三维向量 m_Angular速度）(偏移: 0x30)
- `Vector3 m_Acceleration`（三维向量 m_加速度）(偏移: 0x3C)
- `Vector3 m_AngularAcceleration`（三维向量 m_Angular加速度）(偏移: 0x48)
- `int m_Tracked`（int m_Tracked）(偏移: 0x54)
- `ulong m_UniqueID`（ulong m_UniqueID）(偏移: 0x58)

### 方法 (3)

- `void set_uniqueID(ulong value)`
  （void set_uniqueID（ulong value））
- `void set_nodeType(XRNode value)`
  （void set_node类型（XR节点 value））
- `void set_tracked(bool value)`
  （void set_tracked（bool value））

---

## XROcclusionMeshPass（XROcclusion网格Pass）

**继承**: ScriptableRenderPass（可脚本化渲染通道）

### 方法 (1)

- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（可脚本化渲染上下文 context, 引用 渲染数据 renderingData））

---

## XRPass（XRPass）

### 字段 (16)

- `List<XRView> views`（List<XRView> views）(偏移: 0x8)
- `RenderTargetIdentifier invalidRT`（Render目标Identifier invalidRT）(偏移: 0x0)
- `Material occlusionMeshMaterial`（材质 occlusion网格材质）(偏移: 0x690)
- `Mesh occlusionMeshCombined`（网格 occlusion网格Combined）(偏移: 0x694)
- `int occlusionMeshCombinedHashCode`（int occlusion网格CombinedHashCode）(偏移: 0x698)
- `XRPass.CustomMirrorView customMirrorView`（XRPass.自定义的Mirror视图 customMirror视图）(偏移: 0x69C)
- `ProfilingSampler _XRCustomMirrorProfilingSampler`（ProfilingSampler _XR自定义的MirrorProfilingSampler）(偏移: 0x1C)
- `ProfilingSampler _XROcclusionProfilingSampler`（ProfilingSampler _XROcclusionProfilingSampler）(偏移: 0x20)
- `Vector4[] stereoEyeIndices`（Vector4[] stereoEyeIndices）(偏移: 0x6A0)
- `Matrix4x4[] stereoProjectionMatrix`（Matrix4x4[] stereoProjection矩阵）(偏移: 0x6A4)
- `Matrix4x4[] stereoViewMatrix`（Matrix4x4[] stereo视图矩阵）(偏移: 0x6A8)
- `Matrix4x4[] stereoCameraProjectionMatrix`（Matrix4x4[] stereo摄像机Projection矩阵）(偏移: 0x6AC)
- `int UNITY_STEREO_MATRIX_V`（int UNITY_STEREO_MATRIX_V）(偏移: 0x24)
- `int UNITY_STEREO_MATRIX_IV`（int UNITY_STEREO_MATRIX_IV）(偏移: 0x28)
- `int UNITY_STEREO_MATRIX_VP`（int UNITY_STEREO_MATRIX_VP）(偏移: 0x2C)
- `int UNITY_STEREO_MATRIX_IVP`（int UNITY_STEREO_MATRIX_IVP）(偏移: 0x30)

### 方法 (52)

- `bool get_enabled()`
  （布尔值 获取_已启用（））
- `bool get_xrSdkEnabled()`
  （bool get_xrSdk启用的（））
- `void set_xrSdkEnabled(bool value)`
  （void set_xrSdk启用的（bool value））
- `bool get_copyDepth()`
  （bool get_copy深度（））
- `void set_copyDepth(bool value)`
  （void set_copy深度（bool value））
- `int get_multipassId()`
  （int get_multipassId（））
- `void set_multipassId(int value)`
  （void set_multipassId（int value））
- `int get_cullingPassId()`
  （int get_cullingPassId（））
- `void set_cullingPassId(int value)`
  （void set_cullingPassId（int value））
- `RenderTargetIdentifier get_renderTarget()`
  （Render目标Identifier get_render目标（））
- `void set_renderTarget(RenderTargetIdentifier value)`
  （void set_render目标（Render目标Identifier value））
- `RenderTextureDescriptor get_renderTargetDesc()`
  （Render纹理Descriptor get_render目标Desc（））
- `void set_renderTargetDesc(RenderTextureDescriptor value)`
  （void set_render目标Desc（Render纹理Descriptor value））
- `bool get_renderTargetValid()`
  （bool get_render目标Valid（））
- `bool get_renderTargetIsRenderTexture()`
  （bool get_render目标是否Render纹理（））
- `void set_renderTargetIsRenderTexture(bool value)`
  （void set_render目标是否Render纹理（bool value））
- `bool get_isLateLatchEnabled()`
  （bool get_is延迟Latch启用的（））
- `void set_isLateLatchEnabled(bool value)`
  （void set_is延迟Latch启用的（bool value））
- `bool get_canMarkLateLatch()`
  （bool get_canMark延迟Latch（））
- `void set_canMarkLateLatch(bool value)`
  （void set_canMark延迟Latch（bool value））
- `bool get_hasMarkedLateLatch()`
  （bool get_hasMarked延迟Latch（））
- `void set_hasMarkedLateLatch(bool value)`
  （void set_hasMarked延迟Latch（bool value））
- `Matrix4x4 GetProjMatrix(int viewIndex = 0)`
  （Matrix4x4 获取Proj矩阵（int viewIndex = 0））
- `Matrix4x4 GetViewMatrix(int viewIndex = 0)`
  （Matrix4x4 获取视图矩阵（int viewIndex = 0））
- `int GetTextureArraySlice(int viewIndex = 0)`
  （int 获取纹理数组Slice（int viewIndex = 0））
- `Rect GetViewport(int viewIndex = 0)`
  （Rect 获取Viewport（int viewIndex = 0））
- `ScriptableCullingParameters get_cullingParams()`
  （ScriptableCullingParameters get_cullingParams（））
- `void set_cullingParams(ScriptableCullingParameters value)`
  （void set_cullingParams（ScriptableCullingParameters value））
- `int get_viewCount()`
  （int get_view数量（））
- `bool get_singlePassEnabled()`
  （bool get_singlePass启用的（））
- `bool get_isOcclusionMeshSupported()`
  （bool get_isOcclusion网格Supported（））
- `bool get_hasValidOcclusionMesh()`
  （bool get_hasValidOcclusion网格（））
- `void SetCustomMirrorView(XRPass.CustomMirrorView callback)`
  （void 集合自定义的Mirror视图（XRPass.自定义的Mirror视图 callback））
- `XRPass Create(XRPassCreateInfo createInfo)`
  （XRPass 创建（XRPass创建信息 createInfo））
- `void UpdateView(int viewId, XRDisplaySubsystem.XRRenderPass xrSdkRenderPass, XRDisplaySubsystem.XRRenderParameter xrSdkRenderParameter)`
  （void 更新视图（int viewId, XRDisplaySubsystem.XRRenderPass xrSdkRenderPass, XRDisplaySubsystem.XRRenderParameter xrSdkRenderParameter））
- `void UpdateView(int viewId, Matrix4x4 proj, Matrix4x4 view, Rect vp, int textureArraySlice = -1)`
  （void 更新视图（int viewId, Matrix4x4 proj, Matrix4x4 view, Rect vp, int textureArraySlice = -1））
- `void UpdateCullingParams(int cullingPassId, ScriptableCullingParameters cullingParams)`
  （void 更新CullingParams（int cullingPassId, ScriptableCullingParameters cullingParams））
- `void AddView(Matrix4x4 proj, Matrix4x4 view, Rect vp, int textureArraySlice = -1)`
  （void 添加视图（Matrix4x4 proj, Matrix4x4 view, Rect vp, int textureArraySlice = -1））
- `XRPass Create(XRDisplaySubsystem.XRRenderPass xrRenderPass, int multipassId, ScriptableCullingParameters cullingParameters, Material occlusionMeshMaterial)`
  （XRPass 创建（XRDisplaySubsystem.XRRenderPass xrRenderPass, int multipassId, ScriptableCullingParameters cullingParameters, 材质 occlusionMeshMaterial））
- `void AddView(XRDisplaySubsystem.XRRenderPass xrSdkRenderPass, XRDisplaySubsystem.XRRenderParameter xrSdkRenderParameter)`
  （void 添加视图（XRDisplaySubsystem.XRRenderPass xrSdkRenderPass, XRDisplaySubsystem.XRRenderParameter xrSdkRenderParameter））
- `void Release(XRPass xrPass)`
  （void Release（XRPass xrPass））
- `void AddViewInternal(XRView xrView)`
  （void 添加视图内部的（XR视图 xrView））
- `void UpdateOcclusionMesh()`
  （void 更新Occlusion网格（））
- `bool TryGetOcclusionMeshCombinedHashCode(out int hashCode)`
  （bool Try获取Occlusion网格CombinedHashCode（out int hashCode））
- `void CreateOcclusionMeshCombined()`
  （void 创建Occlusion网格Combined（））
- `void StartSinglePass(CommandBuffer cmd)`
  （void 开始单个Pass（Command缓冲区 cmd））
- `void StopSinglePass(CommandBuffer cmd)`
  （void 停止单个Pass（Command缓冲区 cmd））
- `void EndCamera(CommandBuffer cmd, CameraData cameraData)`
  （void 结束摄像机（Command缓冲区 cmd, 摄像机数据 cameraData））
- `void RenderOcclusionMesh(CommandBuffer cmd)`
  （void RenderOcclusion网格（Command缓冲区 cmd））
- `void UpdateGPUViewAndProjectionMatrices(CommandBuffer cmd, ref CameraData cameraData, bool isRenderToTexture)`
  （void 更新GPU视图AndProjectionMatrices（Command缓冲区 cmd, ref CameraData cameraData, bool isRenderToTexture））
- `void MarkLateLatchShaderProperties(CommandBuffer cmd, ref CameraData cameraData)`
  （void Mark延迟Latch着色器Properties（Command缓冲区 cmd, ref CameraData cameraData））
- `void UnmarkLateLatchShaderProperties(CommandBuffer cmd, ref CameraData cameraData)`
  （void Unmark延迟Latch着色器Properties（Command缓冲区 cmd, ref CameraData cameraData））

---

## XRPass.CustomMirrorView（XRPass.自定义的Mirror视图）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(XRPass pass, CommandBuffer cmd, RenderTexture rt, Rect viewport)`
  （void Invoke（XRPass pass, Command缓冲区 cmd, Render纹理 rt, Rect viewport））
- `IAsyncResult BeginInvoke(XRPass pass, CommandBuffer cmd, RenderTexture rt, Rect viewport, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（XRPass pass, Command缓冲区 cmd, Render纹理 rt, Rect viewport, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## XRPassCreateInfo（XRPass创建信息）

### 字段 (7)

- `int multipassId`（int multipassId）(偏移: 0x0)
- `int cullingPassId`（int cullingPassId）(偏移: 0x4)
- `RenderTexture renderTarget`（Render纹理 render目标）(偏移: 0x8)
- `RenderTextureDescriptor renderTargetDesc`（Render纹理Descriptor render目标Desc）(偏移: 0xC)
- `bool renderTargetIsRenderTexture`（bool render目标是否Render纹理）(偏移: 0x40)
- `ScriptableCullingParameters cullingParameters`（ScriptableCullingParameters cullingParameters）(偏移: 0x48)
- `XRPass.CustomMirrorView customMirrorView`（XRPass.自定义的Mirror视图 customMirror视图）(偏移: 0x668)

---

## XRSettings（XRSettings）

### 方法 (13)

- `bool get_enabled()`
  （布尔值 获取_已启用（））
- `bool get_isDeviceActive()`
  （bool get_isDevice激活的（））
- `float get_eyeTextureResolutionScale()`
  （float get_eye纹理Resolution缩放（））
- `void set_eyeTextureResolutionScale(float value)`
  （void set_eye纹理Resolution缩放（float value））
- `int get_eyeTextureWidth()`
  （int get_eye纹理宽度（））
- `int get_eyeTextureHeight()`
  （int get_eye纹理高度（））
- `RenderTextureDescriptor get_eyeTextureDesc()`
  （Render纹理Descriptor get_eye纹理Desc（））
- `float get_renderViewportScale()`
  （float get_renderViewport缩放（））
- `float get_renderViewportScaleInternal()`
  （float get_renderViewport缩放内部的（））
- `string get_loadedDeviceName()`
  （string get_loadedDevice名称（））
- `string[] get_supportedDevices()`
  （string[] get_supportedDevices（））
- `XRSettings.StereoRenderingMode get_stereoRenderingMode()`
  （XRSettings.StereoRendering模式 get_stereoRendering模式（））
- `void get_eyeTextureDesc_Injected(out RenderTextureDescriptor ret)`
  （void get_eye纹理Desc_Injected（out RenderTextureDescriptor ret））

---

## XRSettings.StereoRenderingMode（XRSettings.StereoRendering模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## XRSystem（XR系统）

### 字段 (10)

- `XRPass emptyPass`（XRPass emptyPass）(偏移: 0x8)
- `List<XRPass> framePasses`（List<XRPass> framePasses）(偏移: 0xC)
- `List<XRDisplaySubsystem> displayList`（List<XRDisplaySubsystem> display列表）(偏移: 0x0)
- `XRDisplaySubsystem display`（XRDisplaySubsystem display）(偏移: 0x10)
- `int msaaLevel`（int msaa等级）(偏移: 0x4)
- `Material occlusionMeshMaterial`（材质 occlusion网格材质）(偏移: 0x14)
- `Material mirrorViewMaterial`（材质 mirror视图材质）(偏移: 0x18)
- `MaterialPropertyBlock mirrorViewMaterialProperty`（材质属性Block mirror视图材质属性）(偏移: 0x1C)
- `RenderTexture testRenderTexture`（Render纹理 testRender纹理）(偏移: 0x20)
- `ProfilingSampler _XRMirrorProfilingSampler`（ProfilingSampler _XRMirrorProfilingSampler）(偏移: 0x8)

### 方法 (18)

- `void InitializeXRSystemData(XRSystemData data)`
  （void 初始化XR系统数据（XR系统数据 data））
- `void GetDisplaySubsystem()`
  （void 获取DisplaySubsystem（））
- `void XRSystemInit()`
  （void XR系统初始化（））
- `void UpdateMSAALevel(int level)`
  （void 更新MSAA等级（int level））
- `int GetMSAALevel()`
  （int 获取MSAA等级（））
- `void UpdateRenderScale(float renderScale)`
  （void 更新Render缩放（float renderScale））
- `int GetMaxViews()`
  （int 获取最大Views（））
- `void BeginLateLatching(Camera camera, XRPass xrPass)`
  （void Begin延迟Latching（摄像机 camera, XRPass xrPass））
- `void EndLateLatching(Camera camera, XRPass xrPass)`
  （void 结束延迟Latching（摄像机 camera, XRPass xrPass））
- `List<XRPass> SetupFrame(CameraData cameraData)`
  （List<XRPass> SetupFrame（摄像机数据 cameraData））
- `void ReleaseFrame()`
  （void ReleaseFrame（））
- `bool RefreshXrSdk()`
  （bool 刷新XrSdk（））
- `void UpdateCameraData(ref CameraData baseCameraData, in XRPass xr)`
  （void 更新摄像机数据（ref CameraData baseCameraData, in XRPass xr））
- `void UpdateFromCamera(ref XRPass xrPass, CameraData cameraData)`
  （void 更新From摄像机（ref XRPass xrPass, 摄像机数据 cameraData））
- `void CreateLayoutFromXrSdk(Camera camera, bool singlePassAllowed)`
  （void 创建LayoutFromXrSdk（摄像机 camera, bool singlePassAllowed））
- `void Dispose()`
  （void 释放（））
- `void AddPassToFrame(XRPass xrPass)`
  （void 添加PassToFrame（XRPass xrPass））
- `void RenderMirrorView(CommandBuffer cmd, Camera camera)`
  （void RenderMirror视图（Command缓冲区 cmd, 摄像机 camera））

---

## XRSystem.XRShaderIDs（XRSystem.XR着色器IDs）

### 字段 (3)

- `int _SourceTexArraySlice`（int _SourceTex数组Slice）(偏移: 0x0)
- `int _SRGBRead`（int _SRGBRead）(偏移: 0x4)
- `int _SRGBWrite`（int _SRGBWrite）(偏移: 0x8)

---

## XRSystemData（XR系统数据）

**继承**: ScriptableObject（脚本对象）

### 字段 (1)

- `XRSystemData.ShaderResources shaders`（XR系统Data.着色器Resources shaders）(偏移: 0xC)

---

## XRSystemData.ShaderResources（XR系统Data.着色器Resources）

### 字段 (2)

- `Shader xrOcclusionMeshPS`（着色器 xrOcclusion网格PS）(偏移: 0x8)
- `Shader xrMirrorViewPS`（着色器 xrMirror视图PS）(偏移: 0xC)

---

## XRUtils（XRUtils）

### 方法 (1)

- `void DrawOcclusionMesh(CommandBuffer cmd, Camera camera, bool stereoEnabled = True)`
  （void DrawOcclusion网格（Command缓冲区 cmd, 摄像机 camera, bool stereoEnabled = True））

---

## XRView（XR视图）

### 字段 (5)

- `Matrix4x4 projMatrix`（Matrix4x4 proj矩阵）(偏移: 0x0)
- `Matrix4x4 viewMatrix`（Matrix4x4 view矩阵）(偏移: 0x40)
- `Rect viewport`（Rect viewport）(偏移: 0x80)
- `Mesh occlusionMesh`（网格 occlusion网格）(偏移: 0x90)
- `int textureArraySlice`（int texture数组Slice）(偏移: 0x94)

---

## XRViewCreateInfo（XR视图创建信息）

### 字段 (4)

- `Matrix4x4 projMatrix`（Matrix4x4 proj矩阵）(偏移: 0x0)
- `Matrix4x4 viewMatrix`（Matrix4x4 view矩阵）(偏移: 0x40)
- `Rect viewport`（Rect viewport）(偏移: 0x80)
- `int textureArraySlice`（int texture数组Slice）(偏移: 0x90)

---

## XmlCharType（XmlChar类型）

### 字段 (3)

- `object s_Lock`（object s_Lock）(偏移: 0x0)
- `byte[] s_CharProperties`（byte[] s_CharProperties）(偏移: 0x4)
- `byte[] charProperties`（byte[] charProperties）(偏移: 0x0)

### 方法 (4)

- `object get_StaticLock()`
  （object get_静态的Lock（））
- `void InitInstance()`
  （void 初始化实例（））
- `void SetProperties(string ranges, byte value)`
  （void 集合Properties（string ranges, byte value））
- `XmlCharType get_Instance()`
  （XmlChar类型 get_实例（））

---

## XmlConvert（Xml转换）

### 字段 (4)

- `XmlCharType xmlCharType`（XmlChar类型 xmlChar类型）(偏移: 0x0)
- `char[] crt`（char[] crt）(偏移: 0x4)
- `int c_EncodedCharLength`（int c_EncodedCharLength）(偏移: 0x8)
- `char[] WhitespaceChars`（char[] WhitespaceChars）(偏移: 0xC)

### 方法 (1)

- `string EscapeValueForDebuggerDisplay(string value)`
  （string Escape值ForDebuggerDisplay（string value））

---

## XmlDocumentType（XmlDocument类型）

**继承**: XmlLinkedNode（XmlLinked节点）

### 字段 (4)

- `string name`（字符串 名称）(偏移: 0x8)
- `string publicId`（string publicId）(偏移: 0xC)
- `string systemId`（string systemId）(偏移: 0x10)
- `string internalSubset`（string internalSubset）(偏移: 0x14)

### 方法 (5)

- `string get_Name()`
  （字符串 获取_名称（））
- `XmlNodeType get_NodeType()`
  （Xml节点类型 get_节点类型（））
- `string get_PublicId()`
  （string get_公开的Id（））
- `string get_SystemId()`
  （string get_系统Id（））
- `string get_InternalSubset()`
  （string get_内部的Subset（））

---

## XmlNode（Xml节点）

### 方法 (2)

- `string get_Value()`
  （字符串 获取_值（））
- `object get_debuggerDisplayProxy()`
  （object get_debuggerDisplay代理（））

---

## XmlNodeType（Xml节点类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## XmlReader（Xml读取器）

### 字段 (3)

- `uint IsTextualNodeBitmap`（uint 是否Textual节点Bitmap）(偏移: 0x0)
- `uint CanReadContentAsBitmap`（uint 能否ReadContentAsBitmap）(偏移: 0x4)
- `uint HasValueBitmap`（uint 是否有值Bitmap）(偏移: 0x8)

### 方法 (2)

- `string get_Name()`
  （字符串 获取_名称（））
- `object get_debuggerDisplayProxy()`
  （object get_debuggerDisplay代理（））

---

## XmlReader.XmlReaderDebuggerDisplayProxy（XmlReader.Xml读取器DebuggerDisplay代理）

### 字段 (1)

- `XmlReader reader`（Xml读取器 reader）(偏移: 0x0)

### 方法 (1)

- `string ToString()`
  （字符串 转字符串（））

---

## YieldAwaitable（YieldAwaitable）

### 方法 (1)

- `YieldAwaitable.YieldAwaiter GetAwaiter()`
  （YieldAwaitable.YieldAwaiter 获取Awaiter（））

---

## YieldAwaitable.YieldAwaiter（YieldAwaitable.YieldAwaiter）

**继承**: ICriticalNotifyCompletion（ICriticalNotifyCompletion）

### 字段 (2)

- `WaitCallback s_waitCallbackRunAction`（Wait回调 s_wait回调运行动作）(偏移: 0x0)
- `SendOrPostCallback s_sendOrPostCallbackRunAction`（发送OrPost回调 s_sendOrPost回调运行动作）(偏移: 0x4)

### 方法 (5)

- `bool get_IsCompleted()`
  （布尔值 获取_是否完成（））
- `void UnsafeOnCompleted(Action continuation)`
  （void UnsafeOnCompleted（动作 continuation））
- `void QueueContinuation(Action continuation, bool flowContext)`
  （void 队列Continuation（动作 continuation, bool flowContext））
- `void RunAction(object state)`
  （void 运行动作（object state））
- `void GetResult()`
  （void 获取Result（））

---

## YogaMeasureMode（YogaMeasure模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## YogaNode（Yoga节点）

### 字段 (3)

- `IntPtr _ygNode`（整数Ptr _yg节点）(偏移: 0x8)
- `MeasureFunction _measureFunction`（MeasureFunction _measureFunction）(偏移: 0xC)
- `BaselineFunction _baselineFunction`（BaselineFunction _baselineFunction）(偏移: 0x10)

### 方法 (2)

- `YogaSize MeasureInternal(YogaNode node, float width, YogaMeasureMode widthMode, float height, YogaMeasureMode heightMode)`
  （Yoga大小 Measure内部的（Yoga节点 node, float width, YogaMeasure模式 widthMode, float height, YogaMeasure模式 heightMode））
- `float BaselineInternal(YogaNode node, float width, float height)`
  （float Baseline内部的（Yoga节点 node, float width, float height））

---

## YogaSize（Yoga大小）

### 字段 (2)

- `float width`（浮点数 宽度）(偏移: 0x0)
- `float height`（浮点数 高度）(偏移: 0x4)

---

## Zip64Option（Zip64Option）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ZipCipherStream（ZipCipher流）

**继承**: Stream（流）

### 字段 (3)

- `ZipCrypto _cipher`（ZipCrypto _cipher）(偏移: 0x14)
- `Stream _s`（流 _s）(偏移: 0x18)
- `CryptoMode _mode`（Crypto模式 _mode）(偏移: 0x1C)

### 方法 (11)

- `int Read(byte[] buffer, int offset, int count)`
  （整数 读取（字节[] buffer, 整数 offset, 整数 count））
- `void Write(byte[] buffer, int offset, int count)`
  （void 写入（字节[] buffer, 整数 offset, 整数 count））
- `bool get_CanRead()`
  （布尔值 获取_能否读取（））
- `bool get_CanSeek()`
  （布尔值 获取_能否查找（））
- `bool get_CanWrite()`
  （布尔值 获取_能否写入（））
- `void Flush()`
  （void 刷新（））
- `long get_Length()`
  （长整数 获取_长度（））
- `long get_Position()`
  （长整数 获取_位置（））
- `void set_Position(long value)`
  （void 设置_位置（长整数 value））
- `long Seek(long offset, SeekOrigin origin)`
  （长整数 查找（长整数 offset, 查找起点 origin））
- `void SetLength(long value)`
  （void 设置_长度（长整数 value））

---

## ZipContainer（Zip容器）

### 字段 (3)

- `ZipFile _zf`（Zip文件 _zf）(偏移: 0x8)
- `ZipOutputStream _zos`（ZipOutput流 _zos）(偏移: 0xC)
- `ZipInputStream _zis`（Zip输入流 _zis）(偏移: 0x10)

### 方法 (16)

- `ZipFile get_ZipFile()`
  （Zip文件 get_Zip文件（））
- `ZipOutputStream get_ZipOutputStream()`
  （ZipOutput流 get_ZipOutput流（））
- `string get_Password()`
  （string get_Password（））
- `Zip64Option get_Zip64()`
  （Zip64Option get_Zip64（））
- `int get_BufferSize()`
  （int get_缓冲区大小（））
- `ParallelDeflateOutputStream get_ParallelDeflater()`
  （ParallelDeflateOutput流 get_ParallelDeflater（））
- `void set_ParallelDeflater(ParallelDeflateOutputStream value)`
  （void set_ParallelDeflater（ParallelDeflateOutput流 value））
- `long get_ParallelDeflateThreshold()`
  （long get_ParallelDeflateThreshold（））
- `int get_ParallelDeflateMaxBufferPairs()`
  （int get_ParallelDeflate最大缓冲区Pairs（））
- `int get_CodecBufferSize()`
  （int get_Codec缓冲区大小（））
- `CompressionStrategy get_Strategy()`
  （CompressionStrategy get_Strategy（））
- `Zip64Option get_UseZip64WhenSaving()`
  （Zip64Option get_UseZip64WhenSaving（））
- `Encoding get_AlternateEncoding()`
  （Encoding get_AlternateEncoding（））
- `Encoding get_DefaultEncoding()`
  （Encoding get_默认的Encoding（））
- `ZipOption get_AlternateEncodingUsage()`
  （ZipOption get_AlternateEncodingUsage（））
- `Stream get_ReadStream()`
  （流 get_Read流（））

---

## ZipCrypto（ZipCrypto）

### 字段 (2)

- `uint[] _Keys`（uint[] _Keys）(偏移: 0x8)
- `CRC32 crc32`（CRC32 crc32）(偏移: 0xC)

### 方法 (7)

- `ZipCrypto ForWrite(string password)`
  （ZipCrypto ForWrite（string password））
- `ZipCrypto ForRead(string password, ZipEntry e)`
  （ZipCrypto ForRead（string password, ZipEntry e））
- `byte get_MagicByte()`
  （byte get_MagicByte（））
- `byte[] DecryptMessage(byte[] cipherText, int length)`
  （byte[] DecryptMessage（byte[] cipherText, int length））
- `byte[] EncryptMessage(byte[] plainText, int length)`
  （byte[] EncryptMessage（byte[] plainText, int length））
- `void InitCipher(string passphrase)`
  （void 初始化Cipher（string passphrase））
- `void UpdateKeys(byte byteValue)`
  （void 更新Keys（byte byteValue））

---

## ZipEntry（ZipEntry）

### 字段 (72)

- `short _VersionMadeBy`（short _VersionMadeBy）(偏移: 0x8)
- `short _InternalFileAttrs`（short _内部的文件Attrs）(偏移: 0xA)
- `int _ExternalFileAttrs`（int _外部的文件Attrs）(偏移: 0xC)
- `short _filenameLength`（short _filenameLength）(偏移: 0x10)
- `short _extraFieldLength`（short _extraFieldLength）(偏移: 0x12)
- `short _commentLength`（short _commentLength）(偏移: 0x14)
- `Stream _inputDecryptorStream`（流 _inputDecryptor流）(偏移: 0x18)
- `object _outputLock`（object _outputLock）(偏移: 0x1C)
- `ZipCrypto _zipCrypto_forExtract`（ZipCrypto _zipCrypto_forExtract）(偏移: 0x20)
- `ZipCrypto _zipCrypto_forWrite`（ZipCrypto _zipCrypto_forWrite）(偏移: 0x24)
- `DateTime _LastModified`（Date时间 _最后一个Modified）(偏移: 0x28)
- `DateTime _Mtime`（Date时间 _Mtime）(偏移: 0x30)
- `DateTime _Atime`（Date时间 _Atime）(偏移: 0x38)
- `DateTime _Ctime`（Date时间 _Ctime）(偏移: 0x40)
- `bool _ntfsTimesAreSet`（bool _ntfsTimesAre集合）(偏移: 0x48)
- `bool _emitNtfsTimes`（bool _emitNtfsTimes）(偏移: 0x0)
- `bool _emitUnixTimes`（bool _emitUnixTimes）(偏移: 0x0)
- `bool _TrimVolumeFromFullyQualifiedPaths`（bool _TrimVolumeFromFullyQualifiedPaths）(偏移: 0x0)
- `string _LocalFileName`（string _本地的文件名称）(偏移: 0x0)
- `string _FileNameInArchive`（string _文件名称InArchive）(偏移: 0x50)
- `short _VersionNeeded`（short _VersionNeeded）(偏移: 0x54)
- `short _BitField`（short _BitField）(偏移: 0x56)
- `short _CompressionMethod`（short _CompressionMethod）(偏移: 0x58)
- `short _CompressionMethod_FromZipFile`（short _CompressionMethod_FromZip文件）(偏移: 0x5A)
- `CompressionLevel _CompressionLevel`（Compression等级 _Compression等级）(偏移: 0x5C)
- `string _Comment`（string _Comment）(偏移: 0x60)
- `bool _IsDirectory`（bool _是否Directory）(偏移: 0x64)
- `byte[] _CommentBytes`（byte[] _CommentBytes）(偏移: 0x68)
- `long _CompressedSize`（long _Compressed大小）(偏移: 0x70)
- `long _CompressedFileDataSize`（long _Compressed文件数据大小）(偏移: 0x78)
- `long _UncompressedSize`（long _Uncompressed大小）(偏移: 0x80)
- `int _TimeBlob`（int _时间Blob）(偏移: 0x88)
- `bool _crcCalculated`（bool _crcCalculated）(偏移: 0x8C)
- `int _Crc32`（int _Crc32）(偏移: 0x90)
- `byte[] _Extra`（byte[] _额外的）(偏移: 0x94)
- `bool _metadataChanged`（bool _metadataChanged）(偏移: 0x98)
- `bool _restreamRequiredOnSave`（bool _restreamRequiredOn保存）(偏移: 0x0)
- `bool _sourceIsEncrypted`（bool _source是否Encrypted）(偏移: 0x0)
- `bool _skippedDuringSave`（bool _skippedDuring保存）(偏移: 0x0)
- `uint _diskNumber`（uint _diskNumber）(偏移: 0x0)
- `Encoding ibm437`（Encoding ibm437）(偏移: 0x0)
- `Encoding _actualEncoding`（Encoding _actualEncoding）(偏移: 0xA0)
- `ZipContainer _container`（Zip容器 _container）(偏移: 0xA4)
- `long __FileDataPosition`（long __文件数据Position）(偏移: 0xA8)
- `byte[] _EntryHeader`（byte[] _Entry标题）(偏移: 0xB0)
- `long _RelativeOffsetOfLocalHeader`（long _RelativeOffsetOf本地的标题）(偏移: 0xB8)
- `long _future_ROLH`（long _future_ROLH）(偏移: 0xC0)
- `long _TotalEntrySize`（long _TotalEntry大小）(偏移: 0xC8)
- `int _LengthOfHeader`（int _LengthOf标题）(偏移: 0xD0)
- `int _LengthOfTrailer`（int _LengthOfTrailer）(偏移: 0xD4)
- `bool _InputUsesZip64`（bool _输入UsesZip64）(偏移: 0xD8)
- `uint _UnsupportedAlgorithmId`（uint _UnsupportedAlgorithmId）(偏移: 0xDC)
- `string _Password`（string _Password）(偏移: 0xE0)
- `ZipEntrySource _Source`（ZipEntrySource _Source）(偏移: 0xE4)
- `EncryptionAlgorithm _Encryption`（EncryptionAlgorithm _Encryption）(偏移: 0xE8)
- `EncryptionAlgorithm _Encryption_FromZipFile`（EncryptionAlgorithm _Encryption_FromZip文件）(偏移: 0xEC)
- `byte[] _WeakEncryptionHeader`（byte[] _WeakEncryption标题）(偏移: 0xF0)
- `Stream _archiveStream`（流 _archive流）(偏移: 0xF4)
- `Stream _sourceStream`（流 _source流）(偏移: 0xF8)
- `Nullable<long> _sourceStreamOriginalPosition`（Nullable<long> _source流OriginalPosition）(偏移: 0x100)
- `bool _ioOperationCanceled`（bool _ioOperationCanceled）(偏移: 0x110)
- `bool _presumeZip64`（bool _presumeZip64）(偏移: 0x111)
- `Nullable<bool> _entryRequiresZip64`（Nullable<bool> _entryRequiresZip64）(偏移: 0x112)
- `Nullable<bool> _OutputUsesZip64`（Nullable<bool> _OutputUsesZip64）(偏移: 0x114)
- `bool _IsText`（bool _是否文本）(偏移: 0x116)
- `ZipEntryTimestamp _timestamp`（ZipEntry时间戳 _timestamp）(偏移: 0x118)
- `DateTime _unixEpoch`（Date时间 _unixEpoch）(偏移: 0x8)
- `DateTime _win32Epoch`（Date时间 _win32Epoch）(偏移: 0x10)
- `DateTime _zeroHour`（Date时间 _zeroHour）(偏移: 0x18)
- `WriteDelegate _WriteDelegate`（Write委托 _Write委托）(偏移: 0x11C)
- `OpenDelegate _OpenDelegate`（打开委托 _打开委托）(偏移: 0x120)
- `CloseDelegate _CloseDelegate`（关闭委托 _关闭委托）(偏移: 0x124)

### 方法 (110)

- `bool get_AttributesIndicateDirectory()`
  （bool get_AttributesIndicateDirectory（））
- `void ResetDirEntry()`
  （void 重置DirEntry（））
- `ZipEntry ReadDirEntry(ZipFile zf, Dictionary<string, object> previouslySeen)`
  （ZipEntry ReadDirEntry（Zip文件 zf, Dictionary<string, object> previouslySeen））
- `bool IsNotValidZipDirEntrySig(int signature)`
  （bool 是否NotValidZipDirEntrySig（int signature））
- `void Extract(Stream stream)`
  （void Extract（流 stream））
- `CrcCalculatorStream InternalOpenReader(string password)`
  （CrcCalculator流 内部的打开读取器（string password））
- `void OnExtractProgress(long bytesWritten, long totalBytesToWrite)`
  （void OnExtractProgress（long bytesWritten, long totalBytesToWrite））
- `void OnBeforeExtract(string path)`
  （void OnBeforeExtract（string path））
- `void OnAfterExtract(string path)`
  （void OnAfterExtract（string path））
- `void OnExtractExisting(string path)`
  （void OnExtractExisting（string path））
- `void ReallyDelete(string fileName)`
  （void ReallyDelete（string fileName））
- `void WriteStatus(string format, object[] args)`
  （void WriteStatus（string format, object[] args））
- `void InternalExtract(string baseDir, Stream outstream, string password)`
  （void 内部的Extract（string baseDir, 流 outstream, string password））
- `void VerifyCrcAfterExtract(int actualCrc32)`
  （void VerifyCrcAfterExtract（int actualCrc32））
- `int CheckExtractExistingFile(string baseDir, string targetFileName)`
  （int 检查ExtractExisting文件（string baseDir, string targetFileName））
- `void _CheckRead(int nbytes)`
  （void _检查Read（int nbytes））
- `int ExtractOne(Stream output)`
  （int ExtractOne（流 output））
- `Stream GetExtractDecompressor(Stream input2)`
  （流 获取ExtractDecompressor（流 input2））
- `Stream GetExtractDecryptor(Stream input)`
  （流 获取ExtractDecryptor（流 input））
- `void _SetTimes(string fileOrDirectory, bool isFile)`
  （void _集合Times（string fileOrDirectory, bool isFile））
- `string get_UnsupportedAlgorithm()`
  （string get_UnsupportedAlgorithm（））
- `string get_UnsupportedCompressionMethod()`
  （string get_UnsupportedCompressionMethod（））
- `void ValidateEncryption()`
  （void 验证Encryption（））
- `void ValidateCompression()`
  （void 验证Compression（））
- `void SetupCryptoForExtract(string password)`
  （void SetupCryptoForExtract（string password））
- `bool ValidateOutput(string basedir, Stream outstream, out string outFileName)`
  （bool 验证Output（string basedir, 流 outstream, out string outFileName））
- `bool ReadHeader(ZipEntry ze, Encoding defaultEncoding)`
  （bool Read标题（ZipEntry ze, Encoding defaultEncoding））
- `int ReadWeakEncryptionHeader(Stream s, byte[] buffer)`
  （int ReadWeakEncryption标题（流 s, byte[] buffer））
- `bool IsNotValidSig(int signature)`
  （bool 是否NotValidSig（int signature））
- `ZipEntry ReadEntry(ZipContainer zc, bool first)`
  （ZipEntry ReadEntry（Zip容器 zc, bool first））
- `void HandlePK00Prefix(Stream s)`
  （void 句柄PK00Prefix（流 s））
- `void HandleUnexpectedDataDescriptor(ZipEntry entry)`
  （void 句柄Unexpected数据Descriptor（ZipEntry entry））
- `int ProcessExtraField(Stream s, short extraFieldLength)`
  （int 处理额外的Field（流 s, short extraFieldLength））
- `int ProcessExtraFieldPkwareStrongEncryption(byte[] Buffer, int j)`
  （int 处理额外的FieldPkwareStrongEncryption（byte[] Buffer, int j））
- `int ProcessExtraFieldZip64(byte[] buffer, int j, short dataSize, long posn)`
  （int 处理额外的FieldZip64（byte[] buffer, int j, short dataSize, long posn））
- `int ProcessExtraFieldInfoZipTimes(byte[] buffer, int j, short dataSize, long posn)`
  （int 处理额外的Field信息ZipTimes（byte[] buffer, int j, short dataSize, long posn））
- `int ProcessExtraFieldUnixTimes(byte[] buffer, int j, short dataSize, long posn)`
  （int 处理额外的FieldUnixTimes（byte[] buffer, int j, short dataSize, long posn））
- `int ProcessExtraFieldWindowsTimes(byte[] buffer, int j, short dataSize, long posn)`
  （int 处理额外的FieldWindowsTimes（byte[] buffer, int j, short dataSize, long posn））
- `void WriteCentralDirectoryEntry(Stream s)`
  （void WriteCentralDirectoryEntry（流 s））
- `byte[] ConstructExtraField(bool forCentralDirectory)`
  （byte[] Construct额外的Field（bool forCentralDirectory））
- `string NormalizeFileName()`
  （string Normalize文件名称（））
- `byte[] GetEncodedFileNameBytes()`
  （byte[] 获取Encoded文件名称Bytes（））
- `bool WantReadAgain()`
  （bool 想要ReadAgain（））
- `void MaybeUnsetCompressionMethodForWriting(int cycle)`
  （void MaybeUnsetCompressionMethodForWriting（int cycle））
- `void WriteHeader(Stream s, int cycle)`
  （void Write标题（流 s, int cycle））
- `int FigureCrc32()`
  （int FigureCrc32（））
- `void PrepSourceStream()`
  （void PrepSource流（））
- `void CopyMetaData(ZipEntry source)`
  （void 复制Meta数据（ZipEntry source））
- `void OnWriteBlock(long bytesXferred, long totalBytesToXfer)`
  （void OnWriteBlock（long bytesXferred, long totalBytesToXfer））
- `void _WriteEntryData(Stream s)`
  （void _WriteEntry数据（流 s））
- `long SetInputAndFigureFileLength(ref Stream input)`
  （long 集合输入AndFigure文件Length（ref Stream input））
- `void FinishOutputStream(Stream s, CountingStream entryCounter, Stream encryptor, Stream compressor, CrcCalculatorStream output)`
  （void FinishOutput流（流 s, Counting流 entryCounter, 流 encryptor, 流 compressor, CrcCalculator流 output））
- `void PostProcessOutput(Stream s)`
  （void Post处理Output（流 s））
- `void SetZip64Flags()`
  （void 集合Zip64Flags（））
- `void PrepOutputStream(Stream s, long streamLength, out CountingStream outputCounter, out Stream encryptor, out Stream compressor, out CrcCalculatorStream output)`
  （void PrepOutput流（流 s, long streamLength, out CountingStream outputCounter, out Stream encryptor, out Stream compressor, out CrcCalculatorStream output））
- `Stream MaybeApplyCompression(Stream s, long streamLength)`
  （流 Maybe应用Compression（流 s, long streamLength））
- `Stream MaybeApplyEncryption(Stream s)`
  （流 Maybe应用Encryption（流 s））
- `void OnZipErrorWhileSaving(Exception e)`
  （void OnZipErrorWhileSaving（Exception e））
- `void Write(Stream s)`
  （void Write（流 s））
- `void StoreRelativeOffset()`
  （void 商店RelativeOffset（））
- `void NotifySaveComplete()`
  （void Notify保存Complete（））
- `void WriteSecurityMetadata(Stream outstream)`
  （void WriteSecurityMetadata（流 outstream））
- `void CopyThroughOneEntry(Stream outStream)`
  （void 复制ThroughOneEntry（流 outStream））
- `void CopyThroughWithRecompute(Stream outstream)`
  （void 复制ThroughWithRecompute（流 outstream））
- `void CopyThroughWithNoChange(Stream outstream)`
  （void 复制ThroughWithNoChange（流 outstream））
- `DateTime get_LastModified()`
  （Date时间 get_最后一个Modified（））
- `void set_LastModified(DateTime value)`
  （void set_最后一个Modified（Date时间 value））
- `int get_BufferSize()`
  （int get_缓冲区大小（））
- `void set_ModifiedTime(DateTime value)`
  （void set_Modified时间（Date时间 value））
- `void set_AccessedTime(DateTime value)`
  （void set_Accessed时间（Date时间 value））
- `void set_CreationTime(DateTime value)`
  （void set_Creation时间（Date时间 value））
- `void SetEntryTimes(DateTime created, DateTime accessed, DateTime modified)`
  （void 集合EntryTimes（Date时间 created, Date时间 accessed, Date时间 modified））
- `void set_EmitTimesInWindowsFormatWhenSaving(bool value)`
  （void set_EmitTimesInWindows格式化WhenSaving（bool value））
- `void set_EmitTimesInUnixFormatWhenSaving(bool value)`
  （void set_EmitTimesInUnix格式化WhenSaving（bool value））
- `string get_LocalFileName()`
  （string get_本地的文件名称（））
- `string get_FileName()`
  （string get_文件名称（））
- `short get_VersionNeeded()`
  （short get_VersionNeeded（））
- `string get_Comment()`
  （string get_Comment（））
- `Nullable<bool> get_OutputUsedZip64()`
  （Nullable<bool> get_OutputUsedZip64（））
- `CompressionMethod get_CompressionMethod()`
  （CompressionMethod get_CompressionMethod（））
- `void set_CompressionMethod(CompressionMethod value)`
  （void set_CompressionMethod（CompressionMethod value））
- `CompressionLevel get_CompressionLevel()`
  （Compression等级 get_Compression等级（））
- `void set_CompressionLevel(CompressionLevel value)`
  （void set_Compression等级（Compression等级 value））
- `long get_CompressedSize()`
  （long get_Compressed大小（））
- `long get_UncompressedSize()`
  （long get_Uncompressed大小（））
- `bool get_IsDirectory()`
  （bool get_是否Directory（））
- `EncryptionAlgorithm get_Encryption()`
  （EncryptionAlgorithm get_Encryption（））
- `void set_Encryption(EncryptionAlgorithm value)`
  （void set_Encryption（EncryptionAlgorithm value））
- `void set_Password(string value)`
  （void set_Password（string value））
- `ExtractExistingFileAction get_ExtractExistingFile()`
  （ExtractExisting文件动作 get_ExtractExisting文件（））
- `void set_ExtractExistingFile(ExtractExistingFileAction value)`
  （void set_ExtractExisting文件（ExtractExisting文件动作 value））
- `ZipErrorAction get_ZipErrorAction()`
  （ZipError动作 get_ZipError动作（））
- `void set_ZipErrorAction(ZipErrorAction value)`
  （void set_ZipError动作（ZipError动作 value））
- `bool get_IncludedInMostRecentSave()`
  （bool get_IncludedInMostRecent保存（））
- `SetCompressionCallback get_SetCompression()`
  （集合Compression回调 get_集合Compression（））
- `void set_SetCompression(SetCompressionCallback value)`
  （void set_集合Compression（集合Compression回调 value））
- `Encoding get_AlternateEncoding()`
  （Encoding get_AlternateEncoding（））
- `void set_AlternateEncoding(Encoding value)`
  （void set_AlternateEncoding（Encoding value））
- `ZipOption get_AlternateEncodingUsage()`
  （ZipOption get_AlternateEncodingUsage（））
- `void set_AlternateEncodingUsage(ZipOption value)`
  （void set_AlternateEncodingUsage（ZipOption value））
- `ZipEntry CreateForStream(string entryName, Stream s)`
  （ZipEntry 创建For流（string entryName, 流 s））
- `ZipEntry Create(string nameInArchive, ZipEntrySource source, object arg1, object arg2)`
  （ZipEntry 创建（string nameInArchive, ZipEntrySource source, object arg1, object arg2））
- `void MarkAsDirectory()`
  （void MarkAsDirectory（））
- `void set_IsText(bool value)`
  （void set_是否文本（bool value））
- `string ToString()`
  （字符串 转字符串（））
- `Stream get_ArchiveStream()`
  （流 get_Archive流（））
- `void SetFdpLoh()`
  （void 集合FdpLoh（））
- `int GetLengthOfCryptoHeaderBytes(EncryptionAlgorithm a)`
  （int 获取LengthOfCrypto标题Bytes（EncryptionAlgorithm a））
- `long get_FileDataPosition()`
  （long get_文件数据Position（））
- `int get_LengthOfHeader()`
  （int get_LengthOf标题（））

---

## ZipEntry.CopyHelper（ZipEntry.复制辅助器）

### 字段 (2)

- `Regex re`（Regex re）(偏移: 0x0)
- `int callCount`（int call数量）(偏移: 0x4)

### 方法 (1)

- `string AppendCopyToFileName(string f)`
  （string Append复制To文件名称（string f））

---

## ZipEntrySource（ZipEntrySource）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ZipEntryTimestamp（ZipEntry时间戳）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ZipErrorAction（ZipError动作）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ZipErrorEventArgs（ZipError事件Args）

**继承**: ZipProgressEventArgs（Zip进度事件参数）

### 字段 (1)

- `Exception _exc`（Exception _exc）(偏移: 0x30)

### 方法 (1)

- `ZipErrorEventArgs Saving(string archiveName, ZipEntry entry, Exception exception)`
  （ZipError事件Args Saving（string archiveName, ZipEntry entry, Exception exception））

---

## ZipFile（Zip文件）

**继承**: IEnumerable<ZipEntry>, IDisposable, IEnumerable（IEnumerable<ZipEntry>, IDisposable, IEnumerable）

### 字段 (53)

- `long _lengthOfReadStream`（long _lengthOfRead流）(偏移: 0x8)
- `TextWriter _StatusMessageTextWriter`（文本写入器 _StatusMessage文本写入器）(偏移: 0x10)
- `bool _CaseSensitiveRetrieval`（bool _CaseSensitiveRetrieval）(偏移: 0x14)
- `Stream _readstream`（流 _readstream）(偏移: 0x18)
- `Stream _writestream`（流 _writestream）(偏移: 0x1C)
- `ushort _versionMadeBy`（ushort _versionMadeBy）(偏移: 0x20)
- `ushort _versionNeededToExtract`（ushort _versionNeededToExtract）(偏移: 0x22)
- `uint _diskNumberWithCd`（uint _diskNumberWithCd）(偏移: 0x24)
- `int _maxOutputSegmentSize`（int _maxOutputSegment大小）(偏移: 0x28)
- `uint _numberOfSegmentsForMostRecentSave`（uint _numberOfSegmentsForMostRecent保存）(偏移: 0x2C)
- `ZipErrorAction _zipErrorAction`（ZipError动作 _zipError动作）(偏移: 0x30)
- `bool _disposed`（布尔值 _已释放）(偏移: 0x34)
- `List<ZipEntry> _zipEntriesAsList`（List<ZipEntry> _zipEntriesAs列表）(偏移: 0x3C)
- `string _name`（string _name）(偏移: 0x40)
- `string _readName`（string _read名称）(偏移: 0x44)
- `string _Comment`（string _Comment）(偏移: 0x48)
- `string _Password`（string _Password）(偏移: 0x4C)
- `bool _emitNtfsTimes`（bool _emitNtfsTimes）(偏移: 0x50)
- `bool _emitUnixTimes`（bool _emitUnixTimes）(偏移: 0x51)
- `CompressionStrategy _Strategy`（CompressionStrategy _Strategy）(偏移: 0x54)
- `CompressionMethod _compressionMethod`（CompressionMethod _compressionMethod）(偏移: 0x58)
- `bool _fileAlreadyExists`（bool _fileAlreadyExists）(偏移: 0x5C)
- `string _temporaryFileName`（string _temporary文件名称）(偏移: 0x60)
- `bool _contentsChanged`（bool _contentsChanged）(偏移: 0x64)
- `bool _hasBeenSaved`（bool _hasBeenSaved）(偏移: 0x65)
- `string _TempFileFolder`（string _Temp文件Folder）(偏移: 0x68)
- `bool _ReadStreamIsOurs`（bool _Read流是否Ours）(偏移: 0x6C)
- `object LOCK`（object LOCK）(偏移: 0x70)
- `bool _saveOperationCanceled`（bool _saveOperationCanceled）(偏移: 0x74)
- `bool _extractOperationCanceled`（bool _extractOperationCanceled）(偏移: 0x75)
- `bool _addOperationCanceled`（bool _addOperationCanceled）(偏移: 0x76)
- `EncryptionAlgorithm _Encryption`（EncryptionAlgorithm _Encryption）(偏移: 0x78)
- `bool _JustSaved`（bool _JustSaved）(偏移: 0x7C)
- `long _locEndOfCDS`（long _loc结束OfCDS）(偏移: 0x80)
- `uint _OffsetOfCentralDirectory`（uint _OffsetOfCentralDirectory）(偏移: 0x88)
- `long _OffsetOfCentralDirectory64`（long _OffsetOfCentralDirectory64）(偏移: 0x90)
- `Nullable<bool> _OutputUsesZip64`（Nullable<bool> _OutputUsesZip64）(偏移: 0x98)
- `bool _inExtractAll`（bool _inExtract所有）(偏移: 0x9A)
- `Encoding _defaultEncoding`（Encoding _defaultEncoding）(偏移: 0x0)
- `Encoding _alternateEncoding`（Encoding _alternateEncoding）(偏移: 0x9C)
- `ZipOption _alternateEncodingUsage`（ZipOption _alternateEncodingUsage）(偏移: 0xA0)
- `int _BufferSize`（int _缓冲区大小）(偏移: 0xA4)
- `ParallelDeflateOutputStream ParallelDeflater`（ParallelDeflateOutput流 ParallelDeflater）(偏移: 0xA8)
- `long _ParallelDeflateThreshold`（long _ParallelDeflateThreshold）(偏移: 0xB0)
- `int _maxBufferPairs`（int _max缓冲区Pairs）(偏移: 0xB8)
- `Zip64Option _zip64`（Zip64Option _zip64）(偏移: 0xBC)
- `bool _SavingSfx`（bool _SavingSfx）(偏移: 0xC0)
- `int BufferSizeDefault`（int 缓冲区大小默认的）(偏移: 0x4)
- `EventHandler<SaveProgressEventArgs> SaveProgress`（事件Handler<保存Progress事件Args> 保存Progress）(偏移: 0xC4)
- `EventHandler<ReadProgressEventArgs> ReadProgress`（事件Handler<ReadProgress事件Args> ReadProgress）(偏移: 0xC8)
- `EventHandler<ExtractProgressEventArgs> ExtractProgress`（事件Handler<ExtractProgress事件Args> ExtractProgress）(偏移: 0xCC)
- `EventHandler<AddProgressEventArgs> AddProgress`（事件Handler<添加Progress事件Args> 添加Progress）(偏移: 0xD0)
- `EventHandler<ZipErrorEventArgs> ZipError`（事件Handler<ZipError事件Args> ZipError）(偏移: 0xD4)

### 方法 (83)

- `void add_ReadProgress(EventHandler<ReadProgressEventArgs> value)`
  （void add_ReadProgress（事件Handler<ReadProgress事件Args> value））
- `void remove_ReadProgress(EventHandler<ReadProgressEventArgs> value)`
  （void remove_ReadProgress（事件Handler<ReadProgress事件Args> value））
- `ZipEntry AddEntry(string entryName, Stream stream)`
  （ZipEntry 添加Entry（string entryName, 流 stream））
- `ZipEntry _InternalAddEntry(ZipEntry ze)`
  （ZipEntry _内部的添加Entry（ZipEntry ze））
- `ZipEntry AddEntry(string entryName, byte[] byteContent)`
  （ZipEntry 添加Entry（string entryName, byte[] byteContent））
- `void InternalAddEntry(string name, ZipEntry entry)`
  （void 内部的添加Entry（string name, ZipEntry entry））
- `string get_ArchiveNameForEvent()`
  （string get_Archive名称For事件（））
- `bool OnSaveBlock(ZipEntry entry, long bytesXferred, long totalBytesToXfer)`
  （bool On保存Block（ZipEntry entry, long bytesXferred, long totalBytesToXfer））
- `void OnSaveEntry(int current, ZipEntry entry, bool before)`
  （void On保存Entry（int current, ZipEntry entry, bool before））
- `void OnSaveEvent(ZipProgressEventType eventFlavor)`
  （void On保存事件（ZipProgress事件类型 eventFlavor））
- `void OnSaveStarted()`
  （void On保存Started（））
- `void OnSaveCompleted()`
  （void On保存Completed（））
- `void OnReadStarted()`
  （void OnReadStarted（））
- `void OnReadCompleted()`
  （void OnReadCompleted（））
- `void OnReadBytes(ZipEntry entry)`
  （void OnReadBytes（ZipEntry entry））
- `void OnReadEntry(bool before, ZipEntry entry)`
  （void OnReadEntry（bool before, ZipEntry entry））
- `long get_LengthOfReadStream()`
  （long get_LengthOfRead流（））
- `bool OnExtractBlock(ZipEntry entry, long bytesWritten, long totalBytesToWrite)`
  （bool OnExtractBlock（ZipEntry entry, long bytesWritten, long totalBytesToWrite））
- `bool OnSingleEntryExtract(ZipEntry entry, string path, bool before)`
  （bool On单个EntryExtract（ZipEntry entry, string path, bool before））
- `bool OnExtractExisting(ZipEntry entry, string path)`
  （bool OnExtractExisting（ZipEntry entry, string path））
- `void AfterAddEntry(ZipEntry entry)`
  （void After添加Entry（ZipEntry entry））
- `bool OnZipErrorSaving(ZipEntry entry, Exception exc)`
  （bool OnZipErrorSaving（ZipEntry entry, Exception exc））
- `ZipFile Read(Stream zipStream)`
  （Zip文件 Read（流 zipStream））
- `ZipFile Read(Stream zipStream, TextWriter statusMessageWriter, Encoding encoding, EventHandler<ReadProgressEventArgs> readProgress)`
  （Zip文件 Read（流 zipStream, 文本写入器 statusMessageWriter, Encoding encoding, 事件Handler<ReadProgress事件Args> readProgress））
- `void ReadIntoInstance(ZipFile zf)`
  （void ReadInto实例（Zip文件 zf））
- `void Zip64SeekToCentralDirectory(ZipFile zf)`
  （void Zip64SeekToCentralDirectory（Zip文件 zf））
- `uint ReadFirstFourBytes(Stream s)`
  （uint Read第一个FourBytes（流 s））
- `void ReadCentralDirectory(ZipFile zf)`
  （void ReadCentralDirectory（Zip文件 zf））
- `void ReadIntoInstance_Orig(ZipFile zf)`
  （void ReadIntoInstance_Orig（Zip文件 zf））
- `void ReadCentralDirectoryFooter(ZipFile zf)`
  （void ReadCentralDirectoryFooter（Zip文件 zf））
- `void ReadZipFileComment(ZipFile zf)`
  （void ReadZip文件Comment（Zip文件 zf））
- `void DeleteFileWithRetry(string filename)`
  （void Delete文件WithRetry（string filename））
- `void Save()`
  （void 保存（））
- `void NotifyEntriesSaveComplete(ICollection<ZipEntry> c)`
  （void NotifyEntries保存Complete（ICollection<ZipEntry> c））
- `void RemoveTempFile()`
  （void 移除Temp文件（））
- `void CleanupAfterSaveOperation()`
  （void 清理After保存Operation（））
- `void Save(Stream outputStream)`
  （void 保存（流 outputStream））
- `bool get_FullScan()`
  （bool get_满Scan（））
- `bool get_SortEntriesBeforeSaving()`
  （bool get_SortEntriesBeforeSaving（））
- `void set_AddDirectoryWillTraverseReparsePoints(bool value)`
  （void set_添加DirectoryWillTraverseReparsePoints（bool value））
- `int get_BufferSize()`
  （int get_缓冲区大小（））
- `int get_CodecBufferSize()`
  （int get_Codec缓冲区大小（））
- `bool get_FlattenFoldersOnExtract()`
  （bool get_FlattenFoldersOnExtract（））
- `CompressionStrategy get_Strategy()`
  （CompressionStrategy get_Strategy（））
- `string get_Name()`
  （字符串 获取_名称（））
- `CompressionLevel get_CompressionLevel()`
  （Compression等级 get_Compression等级（））
- `void set_CompressionLevel(CompressionLevel value)`
  （void set_Compression等级（Compression等级 value））
- `CompressionMethod get_CompressionMethod()`
  （CompressionMethod get_CompressionMethod（））
- `string get_Comment()`
  （string get_Comment（））
- `void set_Comment(string value)`
  （void set_Comment（string value））
- `bool get_Verbose()`
  （bool get_Verbose（））
- `bool get_CaseSensitiveRetrieval()`
  （bool get_CaseSensitiveRetrieval（））
- `Zip64Option get_UseZip64WhenSaving()`
  （Zip64Option get_UseZip64WhenSaving（））
- `void set_UseZip64WhenSaving(Zip64Option value)`
  （void set_UseZip64WhenSaving（Zip64Option value））
- `Encoding get_AlternateEncoding()`
  （Encoding get_AlternateEncoding（））
- `void set_AlternateEncoding(Encoding value)`
  （void set_AlternateEncoding（Encoding value））
- `ZipOption get_AlternateEncodingUsage()`
  （ZipOption get_AlternateEncodingUsage（））
- `void set_AlternateEncodingUsage(ZipOption value)`
  （void set_AlternateEncodingUsage（ZipOption value））
- `Encoding get_DefaultEncoding()`
  （Encoding get_默认的Encoding（））
- `TextWriter get_StatusMessageTextWriter()`
  （文本写入器 get_StatusMessage文本写入器（））
- `string get_TempFileFolder()`
  （string get_Temp文件Folder（））
- `ExtractExistingFileAction get_ExtractExistingFile()`
  （ExtractExisting文件动作 get_ExtractExisting文件（））
- `ZipErrorAction get_ZipErrorAction()`
  （ZipError动作 get_ZipError动作（））
- `EncryptionAlgorithm get_Encryption()`
  （EncryptionAlgorithm get_Encryption（））
- `SetCompressionCallback get_SetCompression()`
  （集合Compression回调 get_集合Compression（））
- `int get_MaxOutputSegmentSize()`
  （int get_最大OutputSegment大小（））
- `void set_ParallelDeflateThreshold(long value)`
  （void set_ParallelDeflateThreshold（long value））
- `long get_ParallelDeflateThreshold()`
  （long get_ParallelDeflateThreshold（））
- `int get_ParallelDeflateMaxBufferPairs()`
  （int get_ParallelDeflate最大缓冲区Pairs（））
- `string ToString()`
  （字符串 转字符串（））
- `void NotifyEntryChanged()`
  （void NotifyEntryChanged（））
- `Stream StreamForDiskNumber(uint diskNumber)`
  （流 流ForDiskNumber（uint diskNumber））
- `void Reset(bool whileSaving)`
  （void 重置（bool whileSaving））
- `void _initEntriesDictionary()`
  （void _initEntries字典（））
- `void _InitInstance(string zipFileName, TextWriter statusMessageWriter)`
  （void _初始化实例（string zipFileName, 文本写入器 statusMessageWriter））
- `ZipEntry get_Item(string fileName)`
  （ZipEntry get_项目（string fileName））
- `ICollection<ZipEntry> get_Entries()`
  （ICollection<ZipEntry> get_Entries（））
- `ICollection<ZipEntry> get_EntriesSorted()`
  （ICollection<ZipEntry> get_EntriesSorted（））
- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposeManagedResources)`
  （void 释放（bool disposeManagedResources））
- `Stream get_ReadStream()`
  （流 get_Read流（））
- `Stream get_WriteStream()`
  （流 get_Write流（））
- `IEnumerator<ZipEntry> GetEnumerator()`
  （IEnumerator<ZipEntry> 获取Enumerator（））

---

## ZipInputStream（Zip输入流）

**继承**: Stream（流）

### 字段 (10)

- `Stream _inputStream`（流 _input流）(偏移: 0x14)
- `ZipEntry _currentEntry`（ZipEntry _currentEntry）(偏移: 0x18)
- `bool _needSetup`（bool _needSetup）(偏移: 0x1C)
- `CrcCalculatorStream _crcStream`（CrcCalculator流 _crc流）(偏移: 0x20)
- `long _LeftToRead`（long _左ToRead）(偏移: 0x28)
- `string _Password`（string _Password）(偏移: 0x30)
- `long _endOfEntry`（long _endOfEntry）(偏移: 0x38)
- `bool _closed`（bool _closed）(偏移: 0x40)
- `bool _findRequired`（bool _findRequired）(偏移: 0x41)
- `bool _exceptionPending`（bool _exceptionPending）(偏移: 0x42)

### 方法 (14)

- `int get_CodecBufferSize()`
  （int get_Codec缓冲区大小（））
- `void SetupStream()`
  （void Setup流（））
- `Stream get_ReadStream()`
  （流 get_Read流（））
- `int Read(byte[] buffer, int offset, int count)`
  （整数 读取（字节[] buffer, 整数 offset, 整数 count））
- `bool get_CanRead()`
  （布尔值 获取_能否读取（））
- `bool get_CanSeek()`
  （布尔值 获取_能否查找（））
- `bool get_CanWrite()`
  （布尔值 获取_能否写入（））
- `long get_Length()`
  （长整数 获取_长度（））
- `long get_Position()`
  （长整数 获取_位置（））
- `void set_Position(long value)`
  （void 设置_位置（长整数 value））
- `void Flush()`
  （void 刷新（））
- `void Write(byte[] buffer, int offset, int count)`
  （void 写入（字节[] buffer, 整数 offset, 整数 count））
- `long Seek(long offset, SeekOrigin origin)`
  （长整数 查找（长整数 offset, 查找起点 origin））
- `void SetLength(long value)`
  （void 设置_长度（长整数 value））

---

## ZipOption（ZipOption）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ZipOutput（ZipOutput）

### 方法 (5)

- `bool WriteCentralDirectoryStructure(Stream s, ICollection<ZipEntry> entries, uint numSegments, Zip64Option zip64, string comment, ZipContainer container)`
  （bool WriteCentralDirectoryStructure（流 s, ICollection<ZipEntry> entries, uint numSegments, Zip64Option zip64, string comment, Zip容器 container））
- `Encoding GetEncoding(ZipContainer container, string t)`
  （Encoding 获取Encoding（Zip容器 container, string t））
- `byte[] GenCentralDirectoryFooter(long StartOfCentralDirectory, long EndOfCentralDirectory, Zip64Option zip64, int entryCount, string comment, ZipContainer container)`
  （byte[] GenCentralDirectoryFooter（long StartOfCentralDirectory, long EndOfCentralDirectory, Zip64Option zip64, int entryCount, string comment, Zip容器 container））
- `byte[] GenZip64EndOfCentralDirectory(long StartOfCentralDirectory, long EndOfCentralDirectory, int entryCount, uint numSegments)`
  （byte[] GenZip64结束OfCentralDirectory（long StartOfCentralDirectory, long EndOfCentralDirectory, int entryCount, uint numSegments））
- `int CountEntries(ICollection<ZipEntry> _entries)`
  （int 数量Entries（ICollection<ZipEntry> _entries））

---

## ZipOutputStream（ZipOutput流）

**继承**: Stream（流）

### 字段 (17)

- `string _password`（string _password）(偏移: 0x14)
- `Stream _outputStream`（流 _output流）(偏移: 0x18)
- `ZipEntry _currentEntry`（ZipEntry _currentEntry）(偏移: 0x1C)
- `Zip64Option _zip64`（Zip64Option _zip64）(偏移: 0x20)
- `int _entryCount`（int _entry数量）(偏移: 0x28)
- `ZipOption _alternateEncodingUsage`（ZipOption _alternateEncodingUsage）(偏移: 0x2C)
- `Encoding _alternateEncoding`（Encoding _alternateEncoding）(偏移: 0x30)
- `bool _disposed`（布尔值 _已释放）(偏移: 0x34)
- `bool _exceptionPending`（bool _exceptionPending）(偏移: 0x35)
- `CountingStream _outputCounter`（Counting流 _outputCounter）(偏移: 0x38)
- `Stream _encryptor`（流 _encryptor）(偏移: 0x3C)
- `Stream _deflater`（流 _deflater）(偏移: 0x40)
- `CrcCalculatorStream _entryOutputStream`（CrcCalculator流 _entryOutput流）(偏移: 0x44)
- `bool _needToWriteEntryHeader`（bool _needToWriteEntry标题）(偏移: 0x48)
- `ParallelDeflateOutputStream ParallelDeflater`（ParallelDeflateOutput流 ParallelDeflater）(偏移: 0x4C)
- `long _ParallelDeflateThreshold`（long _ParallelDeflateThreshold）(偏移: 0x50)
- `int _maxBufferPairs`（int _max缓冲区Pairs）(偏移: 0x58)

### 方法 (21)

- `int get_CodecBufferSize()`
  （int get_Codec缓冲区大小（））
- `CompressionStrategy get_Strategy()`
  （CompressionStrategy get_Strategy（））
- `Zip64Option get_EnableZip64()`
  （Zip64Option get_启用Zip64（））
- `Encoding get_AlternateEncoding()`
  （Encoding get_AlternateEncoding（））
- `ZipOption get_AlternateEncodingUsage()`
  （ZipOption get_AlternateEncodingUsage（））
- `Encoding get_DefaultEncoding()`
  （Encoding get_默认的Encoding（））
- `long get_ParallelDeflateThreshold()`
  （long get_ParallelDeflateThreshold（））
- `int get_ParallelDeflateMaxBufferPairs()`
  （int get_ParallelDeflate最大缓冲区Pairs（））
- `Stream get_OutputStream()`
  （流 get_Output流（））
- `void Write(byte[] buffer, int offset, int count)`
  （void 写入（字节[] buffer, 整数 offset, 整数 count））
- `void _InitiateCurrentEntry(bool finishing)`
  （void _Initiate当前Entry（bool finishing））
- `bool get_CanRead()`
  （布尔值 获取_能否读取（））
- `bool get_CanSeek()`
  （布尔值 获取_能否查找（））
- `bool get_CanWrite()`
  （布尔值 获取_能否写入（））
- `long get_Length()`
  （长整数 获取_长度（））
- `long get_Position()`
  （长整数 获取_位置（））
- `void set_Position(long value)`
  （void 设置_位置（长整数 value））
- `void Flush()`
  （void 刷新（））
- `int Read(byte[] buffer, int offset, int count)`
  （整数 读取（字节[] buffer, 整数 offset, 整数 count））
- `long Seek(long offset, SeekOrigin origin)`
  （长整数 查找（长整数 offset, 查找起点 origin））
- `void SetLength(long value)`
  （void 设置_长度（长整数 value））

---

## ZipProgressEventArgs（Zip进度事件参数）

**继承**: EventArgs（事件参数）

### 字段 (7)

- `int _entriesTotal`（int _entriesTotal）(偏移: 0x8)
- `bool _cancel`（bool _cancel）(偏移: 0xC)
- `ZipEntry _latestEntry`（ZipEntry _latestEntry）(偏移: 0x10)
- `ZipProgressEventType _flavor`（ZipProgress事件类型 _flavor）(偏移: 0x14)
- `string _archiveName`（string _archive名称）(偏移: 0x18)
- `long _bytesTransferred`（long _bytesTransferred）(偏移: 0x20)
- `long _totalBytesToTransfer`（long _totalBytesToTransfer）(偏移: 0x28)

### 方法 (7)

- `void set_EntriesTotal(int value)`
  （void set_EntriesTotal（int value））
- `void set_CurrentEntry(ZipEntry value)`
  （void set_当前Entry（ZipEntry value））
- `bool get_Cancel()`
  （bool get_取消（））
- `void set_EventType(ZipProgressEventType value)`
  （void set_事件类型（ZipProgress事件类型 value））
- `void set_ArchiveName(string value)`
  （void set_Archive名称（string value））
- `void set_BytesTransferred(long value)`
  （void set_BytesTransferred（long value））
- `void set_TotalBytesToTransfer(long value)`
  （void set_TotalBytesToTransfer（long value））

---

## ZipProgressEventType（ZipProgress事件类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ZipSegmentedStream（ZipSegmented流）

**继承**: Stream（流）

### 字段 (10)

- `ZipSegmentedStream.RwMode rwMode`（ZipSegmentedStream.Rw模式 rw模式）(偏移: 0x14)
- `bool _exceptionPending`（bool _exceptionPending）(偏移: 0x18)
- `string _baseName`（string _base名称）(偏移: 0x1C)
- `string _baseDir`（string _baseDir）(偏移: 0x20)
- `string _currentName`（string _current名称）(偏移: 0x24)
- `string _currentTempName`（string _currentTemp名称）(偏移: 0x28)
- `uint _currentDiskNumber`（uint _currentDiskNumber）(偏移: 0x2C)
- `uint _maxDiskNumber`（uint _maxDiskNumber）(偏移: 0x30)
- `int _maxSegmentSize`（int _maxSegment大小）(偏移: 0x34)
- `Stream _innerStream`（流 _内部流）(偏移: 0x38)

### 方法 (27)

- `ZipSegmentedStream ForReading(string name, uint initialDiskNumber, uint maxDiskNumber)`
  （ZipSegmented流 ForReading（string name, uint initialDiskNumber, uint maxDiskNumber））
- `ZipSegmentedStream ForWriting(string name, int maxSegmentSize)`
  （ZipSegmented流 ForWriting（string name, int maxSegmentSize））
- `Stream ForUpdate(string name, uint diskNumber)`
  （流 For更新（string name, uint diskNumber））
- `bool get_ContiguousWrite()`
  （bool get_ContiguousWrite（））
- `void set_ContiguousWrite(bool value)`
  （void set_ContiguousWrite（bool value））
- `uint get_CurrentSegment()`
  （uint get_当前Segment（））
- `void set_CurrentSegment(uint value)`
  （void set_当前Segment（uint value））
- `string get_CurrentName()`
  （string get_当前名称（））
- `string get_CurrentTempName()`
  （string get_当前Temp名称（））
- `string _NameForSegment(uint diskNumber)`
  （string _名称ForSegment（uint diskNumber））
- `uint ComputeSegment(int length)`
  （uint ComputeSegment（int length））
- `string ToString()`
  （字符串 转字符串（））
- `void _SetReadStream()`
  （void _集合Read流（））
- `int Read(byte[] buffer, int offset, int count)`
  （整数 读取（字节[] buffer, 整数 offset, 整数 count））
- `void _SetWriteStream(uint increment)`
  （void _集合Write流（uint increment））
- `void Write(byte[] buffer, int offset, int count)`
  （void 写入（字节[] buffer, 整数 offset, 整数 count））
- `long TruncateBackward(uint diskNumber, long offset)`
  （long Truncate后退（uint diskNumber, long offset））
- `bool get_CanRead()`
  （布尔值 获取_能否读取（））
- `bool get_CanSeek()`
  （布尔值 获取_能否查找（））
- `bool get_CanWrite()`
  （布尔值 获取_能否写入（））
- `void Flush()`
  （void 刷新（））
- `long get_Length()`
  （长整数 获取_长度（））
- `long get_Position()`
  （长整数 获取_位置（））
- `void set_Position(long value)`
  （void 设置_位置（长整数 value））
- `long Seek(long offset, SeekOrigin origin)`
  （长整数 查找（长整数 offset, 查找起点 origin））
- `void SetLength(long value)`
  （void 设置_长度（长整数 value））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））

---

## ZipSegmentedStream.RwMode（ZipSegmentedStream.Rw模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ZlibBaseStream（Zlib基础流）

**继承**: Stream（流）

### 字段 (18)

- `ZlibCodec _z`（ZlibCodec _z）(偏移: 0x14)
- `ZlibBaseStream.StreamMode _streamMode`（Zlib基础Stream.流模式 _stream模式）(偏移: 0x18)
- `FlushType _flushMode`（Flush类型 _flush模式）(偏移: 0x1C)
- `ZlibStreamFlavor _flavor`（Zlib流Flavor _flavor）(偏移: 0x20)
- `CompressionMode _compressionMode`（Compression模式 _compression模式）(偏移: 0x24)
- `CompressionLevel _level`（Compression等级 _level）(偏移: 0x28)
- `bool _leaveOpen`（布尔值 _保持打开）(偏移: 0x2C)
- `byte[] _workingBuffer`（byte[] _working缓冲区）(偏移: 0x30)
- `int _bufferSize`（int _buffer大小）(偏移: 0x34)
- `byte[] _buf1`（byte[] _buf1）(偏移: 0x38)
- `Stream _stream`（流 _stream）(偏移: 0x3C)
- `CompressionStrategy Strategy`（CompressionStrategy Strategy）(偏移: 0x40)
- `CRC32 crc`（CRC32 crc）(偏移: 0x44)
- `string _GzipFileName`（string _Gzip文件名称）(偏移: 0x48)
- `string _GzipComment`（string _GzipComment）(偏移: 0x4C)
- `DateTime _GzipMtime`（Date时间 _GzipMtime）(偏移: 0x50)
- `int _gzipHeaderByteCount`（int _gzip标题Byte数量）(偏移: 0x58)
- `bool nomoreinput`（bool nomoreinput）(偏移: 0x5C)

### 方法 (19)

- `bool get__wantCompress()`
  （bool get__wantCompress（））
- `ZlibCodec get_z()`
  （ZlibCodec get_z（））
- `byte[] get_workingBuffer()`
  （byte[] get_working缓冲区（））
- `void Write(byte[] buffer, int offset, int count)`
  （void 写入（字节[] buffer, 整数 offset, 整数 count））
- `void finish()`
  （void finish（））
- `void end()`
  （void end（））
- `void Close()`
  （void 关闭（））
- `void Flush()`
  （void 刷新（））
- `long Seek(long offset, SeekOrigin origin)`
  （长整数 查找（长整数 offset, 查找起点 origin））
- `void SetLength(long value)`
  （void 设置_长度（长整数 value））
- `string ReadZeroTerminatedString()`
  （string ReadZeroTerminated字符串（））
- `int _ReadAndValidateGzipHeader()`
  （int _ReadAnd验证Gzip标题（））
- `int Read(byte[] buffer, int offset, int count)`
  （整数 读取（字节[] buffer, 整数 offset, 整数 count））
- `bool get_CanRead()`
  （布尔值 获取_能否读取（））
- `bool get_CanSeek()`
  （布尔值 获取_能否查找（））
- `bool get_CanWrite()`
  （布尔值 获取_能否写入（））
- `long get_Length()`
  （长整数 获取_长度（））
- `long get_Position()`
  （长整数 获取_位置（））
- `void set_Position(long value)`
  （void 设置_位置（长整数 value））

---

## ZlibBaseStream.StreamMode（Zlib基础Stream.流模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ZlibCodec（ZlibCodec）

### 字段 (15)

- `byte[] InputBuffer`（byte[] 输入缓冲区）(偏移: 0x8)
- `int NextIn`（int 下一个In）(偏移: 0xC)
- `int AvailableBytesIn`（int AvailableBytesIn）(偏移: 0x10)
- `long TotalBytesIn`（long TotalBytesIn）(偏移: 0x18)
- `byte[] OutputBuffer`（byte[] Output缓冲区）(偏移: 0x20)
- `int NextOut`（int 下一个Out）(偏移: 0x24)
- `int AvailableBytesOut`（int AvailableBytesOut）(偏移: 0x28)
- `long TotalBytesOut`（long TotalBytesOut）(偏移: 0x30)
- `string Message`（string Message）(偏移: 0x38)
- `DeflateManager dstate`（Deflate管理器 dstate）(偏移: 0x3C)
- `InflateManager istate`（Inflate管理器 istate）(偏移: 0x40)
- `uint _Adler32`（uint _Adler32）(偏移: 0x44)
- `CompressionLevel CompressLevel`（Compression等级 Compress等级）(偏移: 0x48)
- `int WindowBits`（int WindowBits）(偏移: 0x4C)
- `CompressionStrategy Strategy`（CompressionStrategy Strategy）(偏移: 0x50)

### 方法 (11)

- `int InitializeInflate(bool expectRfc1950Header)`
  （int 初始化Inflate（bool expectRfc1950Header））
- `int InitializeInflate(int windowBits, bool expectRfc1950Header)`
  （int 初始化Inflate（int windowBits, bool expectRfc1950Header））
- `int Inflate(FlushType flush)`
  （int Inflate（Flush类型 flush））
- `int EndInflate()`
  （int 结束Inflate（））
- `int InitializeDeflate(CompressionLevel level, bool wantRfc1950Header)`
  （int 初始化Deflate（Compression等级 level, bool wantRfc1950Header））
- `int _InternalInitializeDeflate(bool wantRfc1950Header)`
  （int _内部的初始化Deflate（bool wantRfc1950Header））
- `int Deflate(FlushType flush)`
  （int Deflate（Flush类型 flush））
- `int EndDeflate()`
  （int 结束Deflate（））
- `void ResetDeflate()`
  （void 重置Deflate（））
- `void flush_pending()`
  （void flush_pending（））
- `int read_buf(byte[] buf, int start, int size)`
  （int read_buf（byte[] buf, int start, int size））

---

## ZlibStreamFlavor（Zlib流Flavor）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

