# 游戏类定义 (Part 16/21)

共 200 个类 (总序号 3001 - 3200)

---

## SerializationException（SerializationException）

**继承**: SystemException（系统Exception）

### 字段 (1)

- `string _nullMessage`（string _nullMessage）(偏移: 0x0)

---

## SerializationFieldInfo（SerializationField信息）

**继承**: FieldInfo（Field信息）

### 字段 (2)

- `RuntimeFieldInfo m_field`（RuntimeField信息 m_field）(偏移: 0x8)
- `string m_serializationName`（string m_serialization名称）(偏移: 0xC)

### 方法 (16)

- `Module get_Module()`
  （模块 get_模块（））
- `int get_MetadataToken()`
  （int get_Metadata令牌（））
- `string get_Name()`
  （string get_名称（））
- `Type get_DeclaringType()`
  （类型 get_Declaring类型（））
- `Type get_ReflectedType()`
  （类型 get_Reflected类型（））
- `object[] GetCustomAttributes(bool inherit)`
  （object[] 获取自定义的Attributes（bool inherit））
- `object[] GetCustomAttributes(Type attributeType, bool inherit)`
  （object[] 获取自定义的Attributes（类型 attributeType, bool inherit））
- `bool IsDefined(Type attributeType, bool inherit)`
  （bool 是否Defined（类型 attributeType, bool inherit））
- `Type get_FieldType()`
  （类型 get_Field类型（））
- `object GetValue(object obj)`
  （object 获取值（object obj））
- `object InternalGetValue(object obj)`
  （object 内部的获取值（object obj））
- `void SetValue(object obj, object value, BindingFlags invokeAttr, Binder binder, CultureInfo culture)`
  （void 集合值（object obj, object value, BindingFlags invokeAttr, Binder binder, Culture信息 culture））
- `void InternalSetValue(object obj, object value, BindingFlags invokeAttr, Binder binder, CultureInfo culture)`
  （void 内部的集合值（object obj, object value, BindingFlags invokeAttr, Binder binder, Culture信息 culture））
- `RuntimeFieldInfo get_FieldInfo()`
  （RuntimeField信息 get_Field信息（））
- `RuntimeFieldHandle get_FieldHandle()`
  （RuntimeField句柄 get_Field句柄（））
- `FieldAttributes get_Attributes()`
  （FieldAttributes get_Attributes（））

---

## SerializationHeaderRecord（Serialization标题Record）

### 字段 (7)

- `int binaryFormatterMajorVersion`（int binaryFormatterMajorVersion）(偏移: 0x8)
- `int binaryFormatterMinorVersion`（int binaryFormatterMinorVersion）(偏移: 0xC)
- `BinaryHeaderEnum binaryHeaderEnum`（Binary标题Enum binary标题Enum）(偏移: 0x10)
- `int topId`（int topId）(偏移: 0x14)
- `int headerId`（int headerId）(偏移: 0x18)
- `int majorVersion`（int majorVersion）(偏移: 0x1C)
- `int minorVersion`（int minorVersion）(偏移: 0x20)

### 方法 (4)

- `void Write(__BinaryWriter sout)`
  （void Write（__Binary写入器 sout））
- `int GetInt32(byte[] buffer, int index)`
  （int 获取Int32（byte[] buffer, int index））
- `void Read(__BinaryParser input)`
  （void Read（__BinaryParser input））
- `void Dump()`
  （void Dump（））

---

## SerializationInfo（Serialization信息）

### 字段 (11)

- `string[] m_members`（string[] m_members）(偏移: 0x8)
- `object[] m_data`（object[] m_data）(偏移: 0xC)
- `Type[] m_types`（Type[] m_types）(偏移: 0x10)
- `int m_currMember`（int m_currMember）(偏移: 0x18)
- `IFormatterConverter m_converter`（IFormatterConverter m_converter）(偏移: 0x1C)
- `string m_fullTypeName`（string m_full类型名称）(偏移: 0x20)
- `string m_assemName`（string m_assem名称）(偏移: 0x24)
- `Type objectType`（类型 object类型）(偏移: 0x28)
- `bool isFullTypeNameSetExplicit`（bool is满类型名称集合Explicit）(偏移: 0x2C)
- `bool isAssemblyNameSetExplicit`（bool isAssembly名称集合Explicit）(偏移: 0x2D)
- `bool requireSameTokenInPartialTrust`（bool requireSame令牌InPartialTrust）(偏移: 0x2E)

### 方法 (35)

- `string get_FullTypeName()`
  （string get_满类型名称（））
- `string get_AssemblyName()`
  （string get_Assembly名称（））
- `void SetType(Type type)`
  （void 集合类型（类型 type））
- `bool Compare(byte[] a, byte[] b)`
  （bool Compare（byte[] a, byte[] b））
- `void DemandForUnsafeAssemblyNameAssignments(string originalAssemblyName, string newAssemblyName)`
  （void DemandForUnsafeAssembly名称Assignments（string originalAssemblyName, string newAssemblyName））
- `bool IsAssemblyNameAssignmentSafe(string originalAssemblyName, string newAssemblyName)`
  （bool 是否Assembly名称AssignmentSafe（string originalAssemblyName, string newAssemblyName））
- `int get_MemberCount()`
  （int get_Member数量（））
- `Type get_ObjectType()`
  （类型 get_对象类型（））
- `bool get_IsFullTypeNameSetExplicit()`
  （bool get_是否满类型名称集合Explicit（））
- `bool get_IsAssemblyNameSetExplicit()`
  （bool get_是否Assembly名称集合Explicit（））
- `SerializationInfoEnumerator GetEnumerator()`
  （Serialization信息Enumerator 获取Enumerator（））
- `void ExpandArrays()`
  （void ExpandArrays（））
- `void AddValue(string name, object value, Type type)`
  （void 添加值（string name, object value, 类型 type））
- `void AddValue(string name, object value)`
  （void 添加值（string name, object value））
- `void AddValue(string name, bool value)`
  （void 添加值（string name, bool value））
- `void AddValue(string name, char value)`
  （void 添加值（string name, char value））
- `void AddValue(string name, byte value)`
  （void 添加值（string name, byte value））
- `void AddValue(string name, short value)`
  （void 添加值（string name, short value））
- `void AddValue(string name, int value)`
  （void 添加值（string name, int value））
- `void AddValue(string name, long value)`
  （void 添加值（string name, long value））
- `void AddValue(string name, ulong value)`
  （void 添加值（string name, ulong value））
- `void AddValue(string name, float value)`
  （void 添加值（string name, float value））
- `void AddValue(string name, DateTime value)`
  （void 添加值（string name, Date时间 value））
- `void AddValueInternal(string name, object value, Type type)`
  （void 添加值内部的（string name, object value, 类型 type））
- `void UpdateValue(string name, object value, Type type)`
  （void 更新值（string name, object value, 类型 type））
- `int FindElement(string name)`
  （int 查找元素（string name））
- `object GetElement(string name, out Type foundType)`
  （object 获取元素（string name, out Type foundType））
- `object GetElementNoThrow(string name, out Type foundType)`
  （object 获取元素No投掷（string name, out Type foundType））
- `object GetValue(string name, Type type)`
  （object 获取值（string name, 类型 type））
- `object GetValueNoThrow(string name, Type type)`
  （object 获取值No投掷（string name, 类型 type））
- `bool GetBoolean(string name)`
  （bool 获取Boolean（string name））
- `int GetInt32(string name)`
  （int 获取Int32（string name））
- `long GetInt64(string name)`
  （long 获取Int64（string name））
- `float GetSingle(string name)`
  （float 获取单个（string name））
- `string GetString(string name)`
  （string 获取字符串（string name））

---

## SerializationInfoEnumerator（Serialization信息Enumerator）

**继承**: IEnumerator（IEnumerator）

### 字段 (6)

- `string[] m_members`（string[] m_members）(偏移: 0x8)
- `object[] m_data`（object[] m_data）(偏移: 0xC)
- `Type[] m_types`（Type[] m_types）(偏移: 0x10)
- `int m_numItems`（int m_numItems）(偏移: 0x14)
- `int m_currItem`（int m_curr项目）(偏移: 0x18)
- `bool m_current`（bool m_current）(偏移: 0x1C)

### 方法 (6)

- `bool MoveNext()`
  （bool 移动下一个（））
- `SerializationEntry get_Current()`
  （SerializationEntry get_当前（））
- `void Reset()`
  （void 重置（））
- `string get_Name()`
  （string get_名称（））
- `object get_Value()`
  （object get_值（））
- `Type get_ObjectType()`
  （类型 get_对象类型（））

---

## SerializationObjectManager（Serialization对象管理器）

### 字段 (3)

- `Hashtable m_objectSeenTable`（Hashtable m_objectSeenTable）(偏移: 0x8)
- `SerializationEventHandler m_onSerializedHandler`（Serialization事件处理器 m_onSerialized处理器）(偏移: 0xC)
- `StreamingContext m_context`（StreamingContext m_context）(偏移: 0x10)

### 方法 (3)

- `void RegisterObject(object obj)`
  （void Register对象（object obj））
- `void RaiseOnSerializedEvent()`
  （void RaiseOnSerialized事件（））
- `void AddOnSerialized(object obj)`
  （void 添加OnSerialized（object obj））

---

## SerializeSettings（SerializeSettings）

### 字段 (3)

- `bool nodes`（bool nodes）(偏移: 0x8)
- `bool prettyPrint`（bool prettyPrint）(偏移: 0x9)
- `bool editorSettings`（bool editorSettings）(偏移: 0xA)

### 方法 (1)

- `SerializeSettings get_Settings()`
  （SerializeSettings get_Settings（））

---

## ServerContextTerminatorSink（服务器ContextTerminatorSink）

**继承**: IMessageSink（IMessageSink）

### 方法 (2)

- `IMessage SyncProcessMessage(IMessage msg)`
  （IMessage 同步处理Message（IMessage msg））
- `IMessageCtrl AsyncProcessMessage(IMessage msg, IMessageSink replySink)`
  （IMessageCtrl 异步处理Message（IMessage msg, IMessageSink replySink））

---

## ServerIdentity（服务器Identity）

**继承**: Identity（Identity）

### 字段 (5)

- `Type _objectType`（类型 _object类型）(偏移: 0x24)
- `MarshalByRefObject _serverObject`（MarshalByRef对象 _server对象）(偏移: 0x28)
- `IMessageSink _serverSink`（IMessageSink _serverSink）(偏移: 0x2C)
- `Context _context`（Context _context）(偏移: 0x30)
- `Lease _lease`（Lease _lease）(偏移: 0x34)

### 方法 (9)

- `Type get_ObjectType()`
  （类型 get_对象类型（））
- `void StartTrackingLifetime(ILease lease)`
  （void 开始TrackingLifetime（ILease lease））
- `void OnLifetimeExpired()`
  （void OnLifetimeExpired（））
- `ObjRef CreateObjRef(Type requestedType)`
  （ObjRef 创建ObjRef（类型 requestedType））
- `void AttachServerObject(MarshalByRefObject serverObject, Context context)`
  （void Attach服务器对象（MarshalByRef对象 serverObject, Context context））
- `Lease get_Lease()`
  （Lease get_Lease（））
- `Context get_Context()`
  （Context get_Context（））
- `void set_Context(Context value)`
  （void set_Context（Context value））
- `void DisposeServerObject()`
  （void 释放服务器对象（））

---

## ServerObjectReplySink（服务器对象ReplySink）

**继承**: IMessageSink（IMessageSink）

### 字段 (2)

- `IMessageSink _replySink`（IMessageSink _replySink）(偏移: 0x8)
- `ServerIdentity _identity`（服务器Identity _identity）(偏移: 0xC)

### 方法 (2)

- `IMessage SyncProcessMessage(IMessage msg)`
  （IMessage 同步处理Message（IMessage msg））
- `IMessageCtrl AsyncProcessMessage(IMessage msg, IMessageSink replySink)`
  （IMessageCtrl 异步处理Message（IMessage msg, IMessageSink replySink））

---

## ServerObjectTerminatorSink（服务器对象TerminatorSink）

**继承**: IMessageSink（IMessageSink）

### 字段 (1)

- `IMessageSink _nextSink`（IMessageSink _nextSink）(偏移: 0x8)

### 方法 (2)

- `IMessage SyncProcessMessage(IMessage msg)`
  （IMessage 同步处理Message（IMessage msg））
- `IMessageCtrl AsyncProcessMessage(IMessage msg, IMessageSink replySink)`
  （IMessageCtrl 异步处理Message（IMessage msg, IMessageSink replySink））

---

## ServicePointManagerElement（服务Point管理器元素）

**继承**: ConfigurationElement（Configuration元素）

### 方法 (1)

- `ConfigurationPropertyCollection get_Properties()`
  （Configuration属性Collection get_Properties（））

---

## SessionMask（Session掩码）

### 字段 (1)

- `uint m_mask`（uint m_mask）(偏移: 0x0)

### 方法 (9)

- `bool IsEqualOrSupersetOf(SessionMask m)`
  （bool 是否EqualOrSupersetOf（Session掩码 m））
- `SessionMask get_All()`
  （Session掩码 get_所有（））
- `SessionMask FromId(int perEventSourceSessionId)`
  （Session掩码 FromId（int perEventSourceSessionId））
- `ulong ToEventKeywords()`
  （ulong To事件Keywords（））
- `SessionMask FromEventKeywords(ulong m)`
  （Session掩码 From事件Keywords（ulong m））
- `bool get_Item(int perEventSourceSessionId)`
  （bool get_项目（int perEventSourceSessionId））
- `void set_Item(int perEventSourceSessionId, bool value)`
  （void set_项目（int perEventSourceSessionId, bool value））
- `ulong op_Explicit(SessionMask m)`
  （ulong op_Explicit（Session掩码 m））
- `uint op_Explicit(SessionMask m)`
  （uint op_Explicit（Session掩码 m））

---

## SetCompressionCallback（集合Compression回调）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `CompressionLevel Invoke(string localFileName, string fileNameInArchive)`
  （Compression等级 Invoke（string localFileName, string fileNameInArchive））
- `IAsyncResult BeginInvoke(string localFileName, string fileNameInArchive, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（string localFileName, string fileNameInArchive, 异步回调 callback, object object））
- `CompressionLevel EndInvoke(IAsyncResult result)`
  （Compression等级 结束Invoke（I异步Result result））

---

## SetPropertyUtility（集合属性工具）

### 方法 (1)

- `bool SetColor(ref Color currentValue, Color newValue)`
  （bool 集合颜色（ref Color currentValue, 颜色 newValue））

---

## SetSpawnTime（集合出生时间）

**继承**: VFXSpawnerCallbacks（VFXSpawnerCallbacks）

### 字段 (1)

- `int spawnTimeID`（int spawn时间ID）(偏移: 0x3B233B01)

---

## SettingsSection（SettingsSection）

**继承**: ConfigurationSection（ConfigurationSection）

### 方法 (1)

- `ConfigurationPropertyCollection get_Properties()`
  （Configuration属性Collection get_Properties（））

---

## SetupCoroutine（Setup协程）

### 方法 (2)

- `void InvokeMoveNext(IEnumerator enumerator, IntPtr returnValueAddress)`
  （void Invoke移动下一个（IEnumerator enumerator, 整数Ptr returnValueAddress））
- `object InvokeMember(object behaviour, string name, object variable)`
  （object InvokeMember（object behaviour, string name, object variable））

---

## Shader（着色器）

**继承**: Object（对象）

### 方法 (16)

- `Shader Find(string name)`
  （着色器 查找（string name））
- `bool get_isSupported()`
  （bool get_isSupported（））
- `void set_globalRenderPipeline(string value)`
  （void set_globalRenderPipeline（string value））
- `void EnableKeyword(string keyword)`
  （void 启用Keyword（string keyword））
- `void DisableKeyword(string keyword)`
  （void 禁用Keyword（string keyword））
- `DisableBatchingType get_disableBatching()`
  （禁用Batching类型 get_disableBatching（））
- `int TagToID(string name)`
  （int 标签ToID（string name））
- `int PropertyToID(string name)`
  （int 属性ToID（string name））
- `void SetGlobalVectorImpl(int name, Vector4 value)`
  （void 集合全局的向量Impl（int name, Vector4 value））
- `void SetGlobalTextureImpl(int name, Texture value)`
  （void 集合全局的纹理Impl（int name, 纹理 value））
- `void SetGlobalConstantBufferImpl(int name, ComputeBuffer value, int offset, int size)`
  （void 集合全局的Constant缓冲区Impl（int name, Compute缓冲区 value, int offset, int size））
- `void SetGlobalVector(int nameID, Vector4 value)`
  （void 集合全局的向量（int nameID, Vector4 value））
- `void SetGlobalColor(int nameID, Color value)`
  （void 集合全局的颜色（int nameID, 颜色 value））
- `void SetGlobalTexture(int nameID, Texture value)`
  （void 集合全局的纹理（int nameID, 纹理 value））
- `void SetGlobalConstantBuffer(int nameID, ComputeBuffer value, int offset, int size)`
  （void 集合全局的Constant缓冲区（int nameID, Compute缓冲区 value, int offset, int size））
- `void SetGlobalVectorImpl_Injected(int name, ref Vector4 value)`
  （void 集合全局的向量Impl_Injected（int name, ref Vector4 value））

---

## ShaderData（着色器数据）

**继承**: IDisposable（IDisposable）

### 字段 (5)

- `ShaderData m_Instance`（着色器数据 m_实例）(偏移: 0x0)
- `ComputeBuffer m_LightDataBuffer`（Compute缓冲区 m_光照数据缓冲区）(偏移: 0x8)
- `ComputeBuffer m_LightIndicesBuffer`（Compute缓冲区 m_光照Indices缓冲区）(偏移: 0xC)
- `ComputeBuffer m_ShadowDataBuffer`（Compute缓冲区 m_Shadow数据缓冲区）(偏移: 0x10)
- `ComputeBuffer m_ShadowIndicesBuffer`（Compute缓冲区 m_ShadowIndices缓冲区）(偏移: 0x14)

### 方法 (7)

- `ShaderData get_instance()`
  （着色器数据 get_instance（））
- `void Dispose()`
  （void 释放（））
- `ComputeBuffer GetLightDataBuffer(int size)`
  （Compute缓冲区 获取光照数据缓冲区（int size））
- `ComputeBuffer GetLightIndicesBuffer(int size)`
  （Compute缓冲区 获取光照Indices缓冲区（int size））
- `ComputeBuffer GetShadowDataBuffer(int size)`
  （Compute缓冲区 获取Shadow数据缓冲区（int size））
- `ComputeBuffer GetShadowIndicesBuffer(int size)`
  （Compute缓冲区 获取ShadowIndices缓冲区（int size））
- `void DisposeBuffer(ref ComputeBuffer buffer)`
  （void 释放缓冲区（ref ComputeBuffer buffer））

---

## ShaderInput.LightData（着色器Input.光照数据）

### 字段 (5)

- `Vector4 position`（Vector4 position）(偏移: 0x0)
- `Vector4 color`（Vector4 color）(偏移: 0x10)
- `Vector4 attenuation`（Vector4 attenuation）(偏移: 0x20)
- `Vector4 spotDirection`（Vector4 spot方向）(偏移: 0x30)
- `Vector4 occlusionProbeChannels`（Vector4 occlusionProbeChannels）(偏移: 0x40)

---

## ShaderInput.ShadowData（着色器Input.Shadow数据）

### 字段 (2)

- `Matrix4x4 worldToShadowMatrix`（Matrix4x4 worldToShadow矩阵）(偏移: 0x0)
- `Vector4 shadowParams`（Vector4 shadowParams）(偏移: 0x40)

---

## ShaderKeyword（着色器Keyword）

### 字段 (1)

- `int m_KeywordIndex`（int m_Keyword索引）(偏移: 0x0)

### 方法 (1)

- `int GetGlobalKeywordIndex(string keyword)`
  （int 获取全局的Keyword索引（string keyword））

---

## ShaderKeywordStrings（着色器KeywordStrings）

### 字段 (52)

- `string MainLightShadows`（string 主要的光照Shadows）(偏移: 0x0)
- `string MainLightShadowCascades`（string 主要的光照ShadowCascades）(偏移: 0x4)
- `string AdditionalLightsVertex`（string AdditionalLightsVertex）(偏移: 0x8)
- `string AdditionalLightsPixel`（string AdditionalLightsPixel）(偏移: 0xC)
- `string AdditionalLightShadows`（string Additional光照Shadows）(偏移: 0x10)
- `string SoftShadows`（string SoftShadows）(偏移: 0x14)
- `string MixedLightingSubtractive`（string MixedLightingSubtractive）(偏移: 0x18)
- `string LightmapShadowMixing`（string LightmapShadowMixing）(偏移: 0x1C)
- `string ShadowsShadowMask`（string ShadowsShadow掩码）(偏移: 0x20)
- `string DepthNoMsaa`（string 深度NoMsaa）(偏移: 0x24)
- `string DepthMsaa2`（string 深度Msaa2）(偏移: 0x28)
- `string DepthMsaa4`（string 深度Msaa4）(偏移: 0x2C)
- `string DepthMsaa8`（string 深度Msaa8）(偏移: 0x30)
- `string LinearToSRGBConversion`（string LinearToSRGBConversion）(偏移: 0x34)
- `string SmaaLow`（string SmaaLow）(偏移: 0x38)
- `string SmaaMedium`（string SmaaMedium）(偏移: 0x3C)
- `string SmaaHigh`（string SmaaHigh）(偏移: 0x40)
- `string PaniniGeneric`（string PaniniGeneric）(偏移: 0x44)
- `string PaniniUnitDistance`（string PaniniUnit距离）(偏移: 0x48)
- `string BloomLQ`（string BloomLQ）(偏移: 0x4C)
- `string BloomHQ`（string BloomHQ）(偏移: 0x50)
- `string BloomLQDirt`（string BloomLQDirt）(偏移: 0x54)
- `string BloomHQDirt`（string BloomHQDirt）(偏移: 0x58)
- `string UseRGBM`（string UseRGBM）(偏移: 0x5C)
- `string Distortion`（string Distortion）(偏移: 0x60)
- `string ChromaticAberration`（string ChromaticAberration）(偏移: 0x64)
- `string HDRGrading`（string HDRGrading）(偏移: 0x68)
- `string TonemapACES`（string TonemapACES）(偏移: 0x6C)
- `string TonemapNeutral`（string TonemapNeutral）(偏移: 0x70)
- `string FilmGrain`（string FilmGrain）(偏移: 0x74)
- `string Fxaa`（string Fxaa）(偏移: 0x78)
- `string Dithering`（string Dithering）(偏移: 0x7C)
- `string ScreenSpaceOcclusion`（string 屏幕的SpaceOcclusion）(偏移: 0x80)
- `string HighQualitySampling`（string HighQualitySampling）(偏移: 0x84)
- `string DOWNSAMPLING_SIZE_2`（string DOWNSAMPLING_SIZE_2）(偏移: 0x88)
- `string DOWNSAMPLING_SIZE_4`（string DOWNSAMPLING_SIZE_4）(偏移: 0x8C)
- `string DOWNSAMPLING_SIZE_8`（string DOWNSAMPLING_SIZE_8）(偏移: 0x90)
- `string DOWNSAMPLING_SIZE_16`（string DOWNSAMPLING_SIZE_16）(偏移: 0x94)
- `string _SPOT`（string _SPOT）(偏移: 0x98)
- `string _DIRECTIONAL`（string _DIRECTIONAL）(偏移: 0x9C)
- `string _POINT`（string _POINT）(偏移: 0xA0)
- `string _DEFERRED_ADDITIONAL_LIGHT_SHADOWS`（string _DEFERRED_ADDITIONAL_LIGHT_SHADOWS）(偏移: 0xA4)
- `string _GBUFFER_NORMALS_OCT`（string _GBUFFER_NORMALS_OCT）(偏移: 0xA8)
- `string _DEFERRED_SUBTRACTIVE_LIGHTING`（string _DEFERRED_SUBTRACTIVE_LIGHTING）(偏移: 0xAC)
- `string LIGHTMAP_ON`（string LIGHTMAP_ON）(偏移: 0xB0)
- `string _ALPHATEST_ON`（string _ALPHATEST_ON）(偏移: 0xB4)
- `string DIRLIGHTMAP_COMBINED`（string DIRLIGHTMAP_COMBINED）(偏移: 0xB8)
- `string _DETAIL_MULX2`（string _DETAIL_MULX2）(偏移: 0xBC)
- `string _DETAIL_SCALED`（string _DETAIL_SCALED）(偏移: 0xC0)
- `string _CLEARCOAT`（string _CLEARCOAT）(偏移: 0xC4)
- `string _CLEARCOATMAP`（string _CLEARCOATMAP）(偏移: 0xC8)
- `string UseDrawProcedural`（string UseDrawProcedural）(偏移: 0xCC)

---

## ShaderPathID（着色器路径ID）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ShaderPropertyFlags（着色器属性Flags）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ShaderPropertyId（着色器属性Id）

### 字段 (30)

- `int glossyEnvironmentColor`（int glossyEnvironment颜色）(偏移: 0x0)
- `int subtractiveShadowColor`（int subtractiveShadow颜色）(偏移: 0x4)
- `int ambientSkyColor`（int ambientSky颜色）(偏移: 0x8)
- `int ambientEquatorColor`（int ambientEquator颜色）(偏移: 0xC)
- `int ambientGroundColor`（int ambient地面颜色）(偏移: 0x10)
- `int time`（int time）(偏移: 0x14)
- `int sinTime`（int sin时间）(偏移: 0x18)
- `int cosTime`（int cos时间）(偏移: 0x1C)
- `int deltaTime`（int delta时间）(偏移: 0x20)
- `int timeParameters`（int timeParameters）(偏移: 0x24)
- `int scaledScreenParams`（int scaled屏幕的Params）(偏移: 0x28)
- `int worldSpaceCameraPos`（int worldSpace摄像机Pos）(偏移: 0x2C)
- `int screenParams`（int screenParams）(偏移: 0x30)
- `int projectionParams`（int projectionParams）(偏移: 0x34)
- `int zBufferParams`（int z缓冲区Params）(偏移: 0x38)
- `int orthoParams`（int orthoParams）(偏移: 0x3C)
- `int viewMatrix`（int view矩阵）(偏移: 0x40)
- `int projectionMatrix`（int projection矩阵）(偏移: 0x44)
- `int viewAndProjectionMatrix`（int viewAndProjection矩阵）(偏移: 0x48)
- `int inverseViewMatrix`（int inverse视图矩阵）(偏移: 0x4C)
- `int inverseProjectionMatrix`（int inverseProjection矩阵）(偏移: 0x50)
- `int inverseViewAndProjectionMatrix`（int inverse视图AndProjection矩阵）(偏移: 0x54)
- `int cameraProjectionMatrix`（int cameraProjection矩阵）(偏移: 0x58)
- `int inverseCameraProjectionMatrix`（int inverse摄像机Projection矩阵）(偏移: 0x5C)
- `int worldToCameraMatrix`（int worldTo摄像机矩阵）(偏移: 0x60)
- `int cameraToWorldMatrix`（int cameraTo世界的矩阵）(偏移: 0x64)
- `int sourceTex`（int sourceTex）(偏移: 0x68)
- `int scaleBias`（int scaleBias）(偏移: 0x6C)
- `int scaleBiasRt`（int scaleBiasRt）(偏移: 0x70)
- `int rendererColor`（int renderer颜色）(偏移: 0x74)

---

## ShaderTagId（着色器标签Id）

**继承**: IEquatable<ShaderTagId>（IEquatable<着色器标签Id>）

### 字段 (2)

- `ShaderTagId none`（着色器标签Id none）(偏移: 0x0)
- `int m_Id`（int m_Id）(偏移: 0x0)

### 方法 (7)

- `int get_id()`
  （int get_id（））
- `void set_id(int value)`
  （void set_id（int value））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `bool Equals(ShaderTagId other)`
  （bool Equals（着色器标签Id other））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool op_Equality(ShaderTagId tag1, ShaderTagId tag2)`
  （bool op_Equality（着色器标签Id tag1, 着色器标签Id tag2））
- `bool op_Inequality(ShaderTagId tag1, ShaderTagId tag2)`
  （bool op_Inequality（着色器标签Id tag1, 着色器标签Id tag2））

---

## ShaderUtils（着色器Utils）

### 字段 (1)

- `string[] s_ShaderPaths`（string[] s_着色器Paths）(偏移: 0x33BB3399)

### 方法 (3)

- `string GetShaderPath(ShaderPathID id)`
  （string 获取着色器路径（着色器路径ID id））
- `ShaderPathID GetEnumFromPath(string path)`
  （着色器路径ID 获取EnumFrom路径（string path））
- `bool IsLWShader(Shader shader)`
  （bool 是否LW着色器（着色器 shader））

---

## ShaderVariantLogLevel（着色器变异体Log等级）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Shadow（Shadow）

**继承**: BaseMeshEffect（基础网格特效）

### 字段 (3)

- `Color m_EffectColor`（颜色 m_特效颜色）(偏移: 0x10)
- `Vector2 m_EffectDistance`（二维向量 m_特效距离）(偏移: 0x20)
- `bool m_UseGraphicAlpha`（bool m_UseGraphic透明度）(偏移: 0x28)

### 方法 (9)

- `Color get_effectColor()`
  （颜色 get_effect颜色（））
- `void set_effectColor(Color value)`
  （void set_effect颜色（颜色 value））
- `Vector2 get_effectDistance()`
  （二维向量 get_effect距离（））
- `void set_effectDistance(Vector2 value)`
  （void set_effect距离（二维向量 value））
- `bool get_useGraphicAlpha()`
  （bool get_useGraphic透明度（））
- `void set_useGraphicAlpha(bool value)`
  （void set_useGraphic透明度（bool value））
- `void ApplyShadowZeroAlloc(List<UIVertex> verts, Color32 color, int start, int end, float x, float y)`
  （void 应用ShadowZeroAlloc（List<UIVertex> verts, Color32 color, int start, int end, float x, float y））
- `void ApplyShadow(List<UIVertex> verts, Color32 color, int start, int end, float x, float y)`
  （void 应用Shadow（List<UIVertex> verts, Color32 color, int start, int end, float x, float y））
- `void ModifyMesh(VertexHelper vh)`
  （void Modify网格（Vertex辅助器 vh））

---

## ShadowCascadesOption（ShadowCascadesOption）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ShadowCaster2D（ShadowCaster2D）

**继承**: ShadowCasterGroup2D（ShadowCasterGroup2D）

### 字段 (14)

- `bool m_HasRenderer`（bool m_是否有渲染器）(偏移: 0x14)
- `bool m_UseRendererSilhouette`（bool m_Use渲染器Silhouette）(偏移: 0x15)
- `bool m_CastsShadows`（bool m_CastsShadows）(偏移: 0x16)
- `bool m_SelfShadows`（bool m_SelfShadows）(偏移: 0x17)
- `int[] m_ApplyToSortingLayers`（int[] m_应用ToSortingLayers）(偏移: 0x18)
- `Vector3[] m_ShapePath`（Vector3[] m_Shape路径）(偏移: 0x1C)
- `int m_ShapePathHash`（int m_Shape路径Hash）(偏移: 0x20)
- `Mesh m_Mesh`（网格 m_网格）(偏移: 0x24)
- `int m_InstanceId`（int m_实例Id）(偏移: 0x28)
- `ShadowCasterGroup2D m_ShadowCasterGroup`（ShadowCasterGroup2D m_ShadowCaster组）(偏移: 0x2C)
- `ShadowCasterGroup2D m_PreviousShadowCasterGroup`（ShadowCasterGroup2D m_上一个ShadowCaster组）(偏移: 0x30)
- `int m_PreviousShadowGroup`（int m_上一个Shadow组）(偏移: 0x34)
- `bool m_PreviousCastsShadows`（bool m_上一个CastsShadows）(偏移: 0x38)
- `int m_PreviousPathHash`（int m_上一个路径Hash）(偏移: 0x3C)

### 方法 (16)

- `Mesh get_mesh()`
  （网格 get_mesh（））
- `Vector3[] get_shapePath()`
  （Vector3[] get_shape路径（））
- `int get_shapePathHash()`
  （int get_shape路径Hash（））
- `void set_shapePathHash(int value)`
  （void set_shape路径Hash（int value））
- `void set_useRendererSilhouette(bool value)`
  （void set_use渲染器Silhouette（bool value））
- `bool get_useRendererSilhouette()`
  （bool get_use渲染器Silhouette（））
- `void set_selfShadows(bool value)`
  （void set_selfShadows（bool value））
- `bool get_selfShadows()`
  （bool get_selfShadows（））
- `void set_castsShadows(bool value)`
  （void set_castsShadows（bool value））
- `bool get_castsShadows()`
  （bool get_castsShadows（））
- `int[] SetDefaultSortingLayers()`
  （int[] 集合默认的SortingLayers（））
- `bool IsShadowedLayer(int layer)`
  （bool 是否Shadowed层（int layer））
- `void Awake()`
  （void Awake（））
- `void OnEnable()`
  （void On启用（））
- `void OnDisable()`
  （void On禁用（））
- `void Update()`
  （void 更新（））

---

## ShadowCasterGroup2D（ShadowCasterGroup2D）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (2)

- `int m_ShadowGroup`（int m_Shadow组）(偏移: 0xC)
- `List<ShadowCaster2D> m_ShadowCasters`（List<ShadowCaster2D> m_ShadowCasters）(偏移: 0x10)

### 方法 (4)

- `List<ShadowCaster2D> GetShadowCasters()`
  （List<ShadowCaster2D> 获取ShadowCasters（））
- `int GetShadowGroup()`
  （int 获取Shadow组（））
- `void RegisterShadowCaster2D(ShadowCaster2D shadowCaster2D)`
  （void RegisterShadowCaster2D（ShadowCaster2D shadowCaster2D））
- `void UnregisterShadowCaster2D(ShadowCaster2D shadowCaster2D)`
  （void UnregisterShadowCaster2D（ShadowCaster2D shadowCaster2D））

---

## ShadowCasterGroup2DManager（ShadowCasterGroup2D管理器）

### 字段 (1)

- `List<ShadowCasterGroup2D> s_ShadowCasterGroups`（List<ShadowCasterGroup2D> s_ShadowCasterGroups）(偏移: 0x37FB37D9)

### 方法 (8)

- `List<ShadowCasterGroup2D> get_shadowCasterGroups()`
  （List<ShadowCasterGroup2D> get_shadowCasterGroups（））
- `void AddShadowCasterGroupToList(ShadowCasterGroup2D shadowCaster, List<ShadowCasterGroup2D> list)`
  （void 添加ShadowCaster组To列表（ShadowCasterGroup2D shadowCaster, List<ShadowCasterGroup2D> list））
- `void RemoveShadowCasterGroupFromList(ShadowCasterGroup2D shadowCaster, List<ShadowCasterGroup2D> list)`
  （void 移除ShadowCaster组From列表（ShadowCasterGroup2D shadowCaster, List<ShadowCasterGroup2D> list））
- `CompositeShadowCaster2D FindTopMostCompositeShadowCaster(ShadowCaster2D shadowCaster)`
  （CompositeShadowCaster2D 查找顶部MostCompositeShadowCaster（ShadowCaster2D shadowCaster））
- `bool AddToShadowCasterGroup(ShadowCaster2D shadowCaster, ref ShadowCasterGroup2D shadowCasterGroup)`
  （bool 添加ToShadowCaster组（ShadowCaster2D shadowCaster, ref ShadowCasterGroup2D shadowCasterGroup））
- `void RemoveFromShadowCasterGroup(ShadowCaster2D shadowCaster, ShadowCasterGroup2D shadowCasterGroup)`
  （void 移除FromShadowCaster组（ShadowCaster2D shadowCaster, ShadowCasterGroup2D shadowCasterGroup））
- `void AddGroup(ShadowCasterGroup2D group)`
  （void 添加组（ShadowCasterGroup2D group））
- `void RemoveGroup(ShadowCasterGroup2D group)`
  （void 移除组（ShadowCasterGroup2D group））

---

## ShadowCastingMode（ShadowCasting模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ShadowData（Shadow数据）

### 字段 (12)

- `bool supportsMainLightShadows`（bool supports主要的光照Shadows）(偏移: 0x0)
- `bool requiresScreenSpaceShadowResolve`（bool requires屏幕的SpaceShadowResolve）(偏移: 0x1)
- `int mainLightShadowmapWidth`（int main光照Shadowmap宽度）(偏移: 0x4)
- `int mainLightShadowmapHeight`（int main光照Shadowmap高度）(偏移: 0x8)
- `int mainLightShadowCascadesCount`（int main光照ShadowCascades数量）(偏移: 0xC)
- `Vector3 mainLightShadowCascadesSplit`（三维向量 main光照ShadowCascadesSplit）(偏移: 0x10)
- `bool supportsAdditionalLightShadows`（bool supportsAdditional光照Shadows）(偏移: 0x1C)
- `int additionalLightsShadowmapWidth`（int additionalLightsShadowmap宽度）(偏移: 0x20)
- `int additionalLightsShadowmapHeight`（int additionalLightsShadowmap高度）(偏移: 0x24)
- `bool supportsSoftShadows`（bool supportsSoftShadows）(偏移: 0x28)
- `int shadowmapDepthBufferBits`（int shadowmap深度缓冲区Bits）(偏移: 0x2C)
- `List<Vector4> bias`（List<Vector4> bias）(偏移: 0x30)

---

## ShadowDrawingSettings（ShadowDrawingSettings）

**继承**: IEquatable<ShadowDrawingSettings>（IEquatable<ShadowDrawingSettings>）

### 字段 (4)

- `CullingResults m_CullingResults`（CullingResults m_CullingResults）(偏移: 0x0)
- `int m_LightIndex`（int m_光照索引）(偏移: 0x8)
- `int m_UseRenderingLayerMaskTest`（int m_UseRendering层掩码Test）(偏移: 0xC)
- `ShadowSplitData m_SplitData`（ShadowSplit数据 m_Split数据）(偏移: 0x10)

### 方法 (5)

- `ShadowSplitData get_splitData()`
  （ShadowSplit数据 get_split数据（））
- `void set_splitData(ShadowSplitData value)`
  （void set_split数据（ShadowSplit数据 value））
- `bool Equals(ShadowDrawingSettings other)`
  （bool Equals（ShadowDrawingSettings other））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## ShadowQuality（ShadowQuality）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ShadowRendering（ShadowRendering）

### 字段 (5)

- `int k_LightPosID`（int k_光照PosID）(偏移: 0x0)
- `int k_ShadowStencilGroupID`（int k_ShadowStencil组ID）(偏移: 0x4)
- `int k_ShadowIntensityID`（int k_ShadowIntensityID）(偏移: 0x8)
- `int k_ShadowVolumeIntensityID`（int k_ShadowVolumeIntensityID）(偏移: 0xC)
- `int k_ShadowRadiusID`（int k_ShadowRadiusID）(偏移: 0x10)

### 方法 (4)

- `Material GetShadowMaterial(Renderer2DData rendererData, int index)`
  （材质 获取Shadow材质（Renderer2D数据 rendererData, int index））
- `Material GetRemoveSelfShadowMaterial(Renderer2DData rendererData, int index)`
  （材质 获取移除SelfShadow材质（Renderer2D数据 rendererData, int index））
- `void CreateShadowRenderTexture(IRenderPass2D pass, RenderingData renderingData, CommandBuffer cmd, int blendStyleIndex)`
  （void 创建ShadowRender纹理（IRenderPass2D pass, Rendering数据 renderingData, Command缓冲区 cmd, int blendStyleIndex））
- `void RenderShadows(IRenderPass2D pass, RenderingData renderingData, CommandBuffer cmdBuffer, int layerToRender, Light2D light, float shadowIntensity, RenderTargetIdentifier renderTexture, RenderTargetIdentifier depthTexture)`
  （void RenderShadows（IRenderPass2D pass, Rendering数据 renderingData, Command缓冲区 cmdBuffer, int layerToRender, Light2D light, float shadowIntensity, Render目标Identifier renderTexture, Render目标Identifier depthTexture））

---

## ShadowResolution（ShadowResolution）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ShadowSamplingMode（ShadowSampling模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ShadowSliceData（ShadowSlice数据）

### 字段 (6)

- `Matrix4x4 viewMatrix`（Matrix4x4 view矩阵）(偏移: 0x0)
- `Matrix4x4 projectionMatrix`（Matrix4x4 projection矩阵）(偏移: 0x40)
- `Matrix4x4 shadowTransform`（Matrix4x4 shadow变换）(偏移: 0x80)
- `int offsetX`（int offsetX）(偏移: 0xC0)
- `int offsetY`（int offsetY）(偏移: 0xC4)
- `int resolution`（int resolution）(偏移: 0xC8)

### 方法 (1)

- `void Clear()`
  （void 清除（））

---

## ShadowSplitData（ShadowSplit数据）

**继承**: IEquatable<ShadowSplitData>（IEquatable<ShadowSplitData>）

### 字段 (6)

- `int maximumCullingPlaneCount`（int maximumCullingPlane数量）(偏移: 0x0)
- `int m_CullingPlaneCount`（int m_CullingPlane数量）(偏移: 0x0)
- `ShadowSplitData.<m_CullingPlanes>e__FixedBuffer m_CullingPlanes`（ShadowSplitData.<m_CullingPlanes>e__固定缓冲区 m_CullingPlanes）(偏移: 0x4)
- `Vector4 m_CullingSphere`（Vector4 m_CullingSphere）(偏移: 0xA4)
- `float m_ShadowCascadeBlendCullingFactor`（float m_ShadowCascadeBlendCulling系数）(偏移: 0xB4)
- `float m_CullingNearPlane`（float m_CullingNearPlane）(偏移: 0xB8)

### 方法 (8)

- `int get_cullingPlaneCount()`
  （int get_cullingPlane数量（））
- `Vector4 get_cullingSphere()`
  （Vector4 get_cullingSphere（））
- `void set_cullingSphere(Vector4 value)`
  （void set_cullingSphere（Vector4 value））
- `void set_shadowCascadeBlendCullingFactor(float value)`
  （void set_shadowCascadeBlendCulling系数（float value））
- `Plane GetCullingPlane(int index)`
  （Plane 获取CullingPlane（int index））
- `bool Equals(ShadowSplitData other)`
  （bool Equals（ShadowSplit数据 other））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## ShadowUtility（Shadow工具）

### 方法 (8)

- `ShadowUtility.Edge CreateEdge(int triangleIndexA, int triangleIndexB, List<Vector3> vertices, List<int> triangles)`
  （ShadowUtility.Edge 创建Edge（int triangleIndexA, int triangleIndexB, List<Vector3> vertices, List<int> triangles））
- `void PopulateEdgeArray(List<Vector3> vertices, List<int> triangles, List<ShadowUtility.Edge> edges)`
  （void PopulateEdge数组（List<Vector3> vertices, List<int> triangles, List<ShadowUtility.Edge> edges））
- `bool IsOutsideEdge(int edgeIndex, List<ShadowUtility.Edge> edgesToProcess)`
  （bool 是否OutsideEdge（int edgeIndex, List<ShadowUtility.Edge> edgesToProcess））
- `void SortEdges(List<ShadowUtility.Edge> edgesToProcess)`
  （void SortEdges（List<ShadowUtility.Edge> edgesToProcess））
- `void CreateShadowTriangles(List<Vector3> vertices, List<Color> colors, List<int> triangles, List<Vector4> tangents, List<ShadowUtility.Edge> edges)`
  （void 创建ShadowTriangles（List<Vector3> vertices, List<Color> colors, List<int> triangles, List<Vector4> tangents, List<ShadowUtility.Edge> edges））
- `object InterpCustomVertexData(Vec3 position, object[] data, float[] weights)`
  （object Interp自定义的Vertex数据（Vec3 position, object[] data, float[] weights））
- `void InitializeTangents(int tangentsToAdd, List<Vector4> tangents)`
  （void 初始化Tangents（int tangentsToAdd, List<Vector4> tangents））
- `void GenerateShadowMesh(Mesh mesh, Vector3[] shapePath)`
  （void GenerateShadow网格（网格 mesh, Vector3[] shapePath））

---

## ShadowUtility.Edge（ShadowUtility.Edge）

**继承**: IComparable<ShadowUtility.Edge>（IComparable<ShadowUtility.Edge>）

### 字段 (4)

- `int vertexIndex0`（int vertexIndex0）(偏移: 0x0)
- `int vertexIndex1`（int vertexIndex1）(偏移: 0x4)
- `Vector4 tangent`（Vector4 tangent）(偏移: 0x8)
- `bool compareReversed`（bool compareReversed）(偏移: 0x18)

### 方法 (3)

- `void AssignVertexIndices(int vi0, int vi1)`
  （void AssignVertexIndices（int vi0, int vi1））
- `int Compare(ShadowUtility.Edge a, ShadowUtility.Edge b)`
  （int Compare（ShadowUtility.Edge a, ShadowUtility.Edge b））
- `int CompareTo(ShadowUtility.Edge edgeToCompare)`
  （int CompareTo（ShadowUtility.Edge edgeToCompare））

---

## ShadowUtils（ShadowUtils）

### 字段 (2)

- `RenderTextureFormat m_ShadowmapFormat`（Render纹理格式化 m_Shadowmap格式化）(偏移: 0x0)
- `bool m_ForceShadowPointSampling`（bool m_强制ShadowPointSampling）(偏移: 0x4)

### 方法 (10)

- `bool ExtractDirectionalLightMatrix(ref CullingResults cullResults, ref ShadowData shadowData, int shadowLightIndex, int cascadeIndex, int shadowmapWidth, int shadowmapHeight, int shadowResolution, float shadowNearPlane, out Vector4 cascadeSplitDistance, out ShadowSliceData shadowSliceData, out Matrix4x4 viewMatrix, out Matrix4x4 projMatrix)`
  （bool ExtractDirectional光照矩阵（ref CullingResults cullResults, ref ShadowData shadowData, int shadowLightIndex, int cascadeIndex, int shadowmapWidth, int shadowmapHeight, int shadowResolution, float shadowNearPlane, out Vector4 cascadeSplitDistance, out ShadowSliceData shadowSliceData, out Matrix4x4 viewMatrix, out Matrix4x4 projMatrix））
- `bool ExtractSpotLightMatrix(ref CullingResults cullResults, ref ShadowData shadowData, int shadowLightIndex, out Matrix4x4 shadowMatrix, out Matrix4x4 viewMatrix, out Matrix4x4 projMatrix)`
  （bool ExtractSpot光照矩阵（ref CullingResults cullResults, ref ShadowData shadowData, int shadowLightIndex, out Matrix4x4 shadowMatrix, out Matrix4x4 viewMatrix, out Matrix4x4 projMatrix））
- `void RenderShadowSlice(CommandBuffer cmd, ref ScriptableRenderContext context, ref ShadowSliceData shadowSliceData, ref ShadowDrawingSettings settings, Matrix4x4 proj, Matrix4x4 view)`
  （void RenderShadowSlice（Command缓冲区 cmd, ref ScriptableRenderContext context, ref ShadowSliceData shadowSliceData, ref ShadowDrawingSettings settings, Matrix4x4 proj, Matrix4x4 view））
- `void RenderShadowSlice(CommandBuffer cmd, ref ScriptableRenderContext context, ref ShadowSliceData shadowSliceData, ref ShadowDrawingSettings settings)`
  （void RenderShadowSlice（Command缓冲区 cmd, ref ScriptableRenderContext context, ref ShadowSliceData shadowSliceData, ref ShadowDrawingSettings settings））
- `int GetMaxTileResolutionInAtlas(int atlasWidth, int atlasHeight, int tileCount)`
  （int 获取最大TileResolutionInAtlas（int atlasWidth, int atlasHeight, int tileCount））
- `void ApplySliceTransform(ref ShadowSliceData shadowSliceData, int atlasWidth, int atlasHeight)`
  （void 应用Slice变换（ref ShadowSliceData shadowSliceData, int atlasWidth, int atlasHeight））
- `Vector4 GetShadowBias(ref VisibleLight shadowLight, int shadowLightIndex, ref ShadowData shadowData, Matrix4x4 lightProjectionMatrix, float shadowResolution)`
  （Vector4 获取ShadowBias（ref VisibleLight shadowLight, int shadowLightIndex, ref ShadowData shadowData, Matrix4x4 lightProjectionMatrix, float shadowResolution））
- `void SetupShadowCasterConstantBuffer(CommandBuffer cmd, ref VisibleLight shadowLight, Vector4 shadowBias)`
  （void SetupShadowCasterConstant缓冲区（Command缓冲区 cmd, ref VisibleLight shadowLight, Vector4 shadowBias））
- `RenderTexture GetTemporaryShadowTexture(int width, int height, int bits)`
  （Render纹理 获取临时的Shadow纹理（int width, int height, int bits））
- `Matrix4x4 GetShadowTransform(Matrix4x4 proj, Matrix4x4 view)`
  （Matrix4x4 获取Shadow变换（Matrix4x4 proj, Matrix4x4 view））

---

## ShadowmaskMode（Shadowmask模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ShadowsMidtonesHighlights（ShadowsMidtonesHighlights）

**继承**: VolumeComponent, IPostProcessComponent（Volume组件, IPost处理组件）

### 字段 (7)

- `Vector4Parameter shadows`（Vector4Parameter shadows）(偏移: 0x1C)
- `Vector4Parameter midtones`（Vector4Parameter midtones）(偏移: 0x20)
- `Vector4Parameter highlights`（Vector4Parameter highlights）(偏移: 0x24)
- `MinFloatParameter shadowsStart`（最小浮点数Parameter shadows开始）(偏移: 0x28)
- `MinFloatParameter shadowsEnd`（最小浮点数Parameter shadows结束）(偏移: 0x2C)
- `MinFloatParameter highlightsStart`（最小浮点数Parameter highlights开始）(偏移: 0x30)
- `MinFloatParameter highlightsEnd`（最小浮点数Parameter highlights结束）(偏移: 0x34)

### 方法 (2)

- `bool IsActive()`
  （bool 是否激活的（））
- `bool IsTileCompatible()`
  （bool 是否TileCompatible（））

---

## SharedReference（Shared引用）

### 字段 (2)

- `WeakReference _ref`（Weak引用 _ref）(偏移: 0x8)
- `int _locked`（int _locked）(偏移: 0xC)

### 方法 (2)

- `object Get()`
  （object 获取（））
- `void Cache(object obj)`
  （void 缓存（object obj））

---

## SharedUtilities（SharedUtilities）

### 字段 (3)

- `Regex doubleDotRegex1`（Regex doubleDotRegex1）(偏移: 0x0)
- `Encoding ibm437`（Encoding ibm437）(偏移: 0x4)
- `Encoding utf8`（Encoding utf8）(偏移: 0x8)

### 方法 (19)

- `long GetFileLength(string fileName)`
  （long 获取文件Length（string fileName））
- `string SimplifyFwdSlashPath(string path)`
  （string SimplifyFwdSlash路径（string path））
- `string NormalizePathForUseInZipFile(string pathName)`
  （string Normalize路径ForUseInZip文件（string pathName））
- `byte[] StringToByteArray(string value, Encoding encoding)`
  （byte[] 字符串ToByte数组（string value, Encoding encoding））
- `byte[] StringToByteArray(string value)`
  （byte[] 字符串ToByte数组（string value））
- `string Utf8StringFromBuffer(byte[] buf)`
  （string Utf8字符串From缓冲区（byte[] buf））
- `string StringFromBuffer(byte[] buf, Encoding encoding)`
  （string 字符串From缓冲区（byte[] buf, Encoding encoding））
- `int ReadSignature(Stream s)`
  （int ReadSignature（流 s））
- `int ReadEntrySignature(Stream s)`
  （int ReadEntrySignature（流 s））
- `int ReadInt(Stream s)`
  （int Read整数（流 s））
- `int _ReadFourBytes(Stream s, string message)`
  （int _ReadFourBytes（流 s, string message））
- `long FindSignature(Stream stream, int SignatureToFind)`
  （long 查找Signature（流 stream, int SignatureToFind））
- `DateTime AdjustTime_Reverse(DateTime time)`
  （Date时间 AdjustTime_Reverse（Date时间 time））
- `DateTime PackedToDateTime(int packedDateTime)`
  （Date时间 PackedToDate时间（int packedDateTime））
- `int DateTimeToPacked(DateTime time)`
  （int Date时间ToPacked（Date时间 time））
- `void CreateAndOpenUniqueTempFile(string dir, out Stream fs, out string filename)`
  （void 创建And打开UniqueTemp文件（string dir, out Stream fs, out string filename））
- `string InternalGetTempFileName()`
  （string 内部的获取Temp文件名称（））
- `string GenerateRandomStringImpl(int length, int delta)`
  （string Generate随机字符串Impl（int length, int delta））
- `int ReadWithRetry(Stream s, byte[] buffer, int offset, int count, string FileName)`
  （int ReadWithRetry（流 s, byte[] buffer, int offset, int count, string FileName））

---

## SharedUtils（SharedUtils）

### 方法 (1)

- `int URShift(int number, int bits)`
  （int URShift（int number, int bits））

---

## ShootPosture（射击姿态）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ShortcutExtensions（ShortcutExtensions）

### 方法 (54)

- `Tweener DOShakePosition(Camera target, float duration, float strength = 3, int vibrato = 10, float randomness = 90, bool fadeOut = True)`
  （Tweener DO震动Position（摄像机 target, float duration, float strength = 3, int vibrato = 10, float randomness = 90, bool fadeOut = True））
- `Tweener DOShakePosition(Camera target, float duration, Vector3 strength, int vibrato = 10, float randomness = 90, bool fadeOut = True)`
  （Tweener DO震动Position（摄像机 target, float duration, 三维向量 strength, int vibrato = 10, float randomness = 90, bool fadeOut = True））
- `Tweener DOShakeRotation(Camera target, float duration, float strength = 90, int vibrato = 10, float randomness = 90, bool fadeOut = True)`
  （Tweener DO震动Rotation（摄像机 target, float duration, float strength = 90, int vibrato = 10, float randomness = 90, bool fadeOut = True））
- `Tweener DOShakeRotation(Camera target, float duration, Vector3 strength, int vibrato = 10, float randomness = 90, bool fadeOut = True)`
  （Tweener DO震动Rotation（摄像机 target, float duration, 三维向量 strength, int vibrato = 10, float randomness = 90, bool fadeOut = True））
- `Tweener DOColor(LineRenderer target, Color2 startValue, Color2 endValue, float duration)`
  （Tweener DO颜色（Line渲染器 target, Color2 startValue, Color2 endValue, float duration））
- `Tweener DOResize(TrailRenderer target, float toStartWidth, float toEndWidth, float duration)`
  （Tweener DOResize（Trail渲染器 target, float toStartWidth, float toEndWidth, float duration））
- `Tweener DOLookAt(Transform target, Vector3 towards, float duration, AxisConstraint axisConstraint = 0, Nullable<Vector3> up)`
  （Tweener DOLookAt（变换 target, 三维向量 towards, float duration, 轴Constraint axisConstraint = 0, Nullable<Vector3> up））
- `Tweener DODynamicLookAt(Transform target, Vector3 towards, float duration, AxisConstraint axisConstraint = 0, Nullable<Vector3> up)`
  （Tweener DO动态的LookAt（变换 target, 三维向量 towards, float duration, 轴Constraint axisConstraint = 0, Nullable<Vector3> up））
- `Tweener LookAt(Transform target, Vector3 towards, float duration, AxisConstraint axisConstraint, Nullable<Vector3> up, bool dynamic)`
  （Tweener LookAt（变换 target, 三维向量 towards, float duration, 轴Constraint axisConstraint, Nullable<Vector3> up, bool dynamic））
- `Tweener DOPunchPosition(Transform target, Vector3 punch, float duration, int vibrato = 10, float elasticity = 1, bool snapping = False)`
  （Tweener DOPunchPosition（变换 target, 三维向量 punch, float duration, int vibrato = 10, float elasticity = 1, bool snapping = False））
- `Tweener DOPunchScale(Transform target, Vector3 punch, float duration, int vibrato = 10, float elasticity = 1)`
  （Tweener DOPunch缩放（变换 target, 三维向量 punch, float duration, int vibrato = 10, float elasticity = 1））
- `Tweener DOPunchRotation(Transform target, Vector3 punch, float duration, int vibrato = 10, float elasticity = 1)`
  （Tweener DOPunchRotation（变换 target, 三维向量 punch, float duration, int vibrato = 10, float elasticity = 1））
- `Tweener DOShakePosition(Transform target, float duration, float strength = 1, int vibrato = 10, float randomness = 90, bool snapping = False, bool fadeOut = True)`
  （Tweener DO震动Position（变换 target, float duration, float strength = 1, int vibrato = 10, float randomness = 90, bool snapping = False, bool fadeOut = True））
- `Tweener DOShakePosition(Transform target, float duration, Vector3 strength, int vibrato = 10, float randomness = 90, bool snapping = False, bool fadeOut = True)`
  （Tweener DO震动Position（变换 target, float duration, 三维向量 strength, int vibrato = 10, float randomness = 90, bool snapping = False, bool fadeOut = True））
- `Tweener DOShakeRotation(Transform target, float duration, float strength = 90, int vibrato = 10, float randomness = 90, bool fadeOut = True)`
  （Tweener DO震动Rotation（变换 target, float duration, float strength = 90, int vibrato = 10, float randomness = 90, bool fadeOut = True））
- `Tweener DOShakeRotation(Transform target, float duration, Vector3 strength, int vibrato = 10, float randomness = 90, bool fadeOut = True)`
  （Tweener DO震动Rotation（变换 target, float duration, 三维向量 strength, int vibrato = 10, float randomness = 90, bool fadeOut = True））
- `Tweener DOShakeScale(Transform target, float duration, float strength = 1, int vibrato = 10, float randomness = 90, bool fadeOut = True)`
  （Tweener DO震动缩放（变换 target, float duration, float strength = 1, int vibrato = 10, float randomness = 90, bool fadeOut = True））
- `Tweener DOShakeScale(Transform target, float duration, Vector3 strength, int vibrato = 10, float randomness = 90, bool fadeOut = True)`
  （Tweener DO震动缩放（变换 target, float duration, 三维向量 strength, int vibrato = 10, float randomness = 90, bool fadeOut = True））
- `Sequence DOJump(Transform target, Vector3 endValue, float jumpPower, int numJumps, float duration, bool snapping = False)`
  （Sequence DO跳跃（变换 target, 三维向量 endValue, float jumpPower, int numJumps, float duration, bool snapping = False））
- `Sequence DOLocalJump(Transform target, Vector3 endValue, float jumpPower, int numJumps, float duration, bool snapping = False)`
  （Sequence DO本地的跳跃（变换 target, 三维向量 endValue, float jumpPower, int numJumps, float duration, bool snapping = False））
- `Tweener DOBlendableColor(Light target, Color endValue, float duration)`
  （Tweener DOBlendable颜色（光照 target, 颜色 endValue, float duration））
- `Tweener DOBlendableColor(Material target, Color endValue, float duration)`
  （Tweener DOBlendable颜色（材质 target, 颜色 endValue, float duration））
- `Tweener DOBlendableColor(Material target, Color endValue, string property, float duration)`
  （Tweener DOBlendable颜色（材质 target, 颜色 endValue, string property, float duration））
- `Tweener DOBlendableColor(Material target, Color endValue, int propertyID, float duration)`
  （Tweener DOBlendable颜色（材质 target, 颜色 endValue, int propertyID, float duration））
- `Tweener DOBlendableMoveBy(Transform target, Vector3 byValue, float duration, bool snapping = False)`
  （Tweener DOBlendable移动By（变换 target, 三维向量 byValue, float duration, bool snapping = False））
- `Tweener DOBlendableLocalMoveBy(Transform target, Vector3 byValue, float duration, bool snapping = False)`
  （Tweener DOBlendable本地的移动By（变换 target, 三维向量 byValue, float duration, bool snapping = False））
- `Tweener DOBlendableRotateBy(Transform target, Vector3 byValue, float duration, RotateMode mode = 0)`
  （Tweener DOBlendableRotateBy（变换 target, 三维向量 byValue, float duration, Rotate模式 mode = 0））
- `Tweener DOBlendableLocalRotateBy(Transform target, Vector3 byValue, float duration, RotateMode mode = 0)`
  （Tweener DOBlendable本地的RotateBy（变换 target, 三维向量 byValue, float duration, Rotate模式 mode = 0））
- `Tweener DOBlendablePunchRotation(Transform target, Vector3 punch, float duration, int vibrato = 10, float elasticity = 1)`
  （Tweener DOBlendablePunchRotation（变换 target, 三维向量 punch, float duration, int vibrato = 10, float elasticity = 1））
- `Tweener DOBlendableScaleBy(Transform target, Vector3 byValue, float duration)`
  （Tweener DOBlendable缩放By（变换 target, 三维向量 byValue, float duration））
- `int DOComplete(Component target, bool withCallbacks = False)`
  （int DOComplete（组件 target, bool withCallbacks = False））
- `int DOComplete(Material target, bool withCallbacks = False)`
  （int DOComplete（材质 target, bool withCallbacks = False））
- `int DOKill(Component target, bool complete = False)`
  （int DO击杀（组件 target, bool complete = False））
- `int DOKill(Material target, bool complete = False)`
  （int DO击杀（材质 target, bool complete = False））
- `int DOFlip(Component target)`
  （int DOFlip（组件 target））
- `int DOFlip(Material target)`
  （int DOFlip（材质 target））
- `int DOGoto(Component target, float to, bool andPlay = False)`
  （int DOGoto（组件 target, float to, bool andPlay = False））
- `int DOGoto(Material target, float to, bool andPlay = False)`
  （int DOGoto（材质 target, float to, bool andPlay = False））
- `int DOPause(Component target)`
  （int DO暂停（组件 target））
- `int DOPause(Material target)`
  （int DO暂停（材质 target））
- `int DOPlay(Component target)`
  （int DO播放（组件 target））
- `int DOPlay(Material target)`
  （int DO播放（材质 target））
- `int DOPlayBackwards(Component target)`
  （int DO播放Backwards（组件 target））
- `int DOPlayBackwards(Material target)`
  （int DO播放Backwards（材质 target））
- `int DOPlayForward(Component target)`
  （int DO播放前进（组件 target））
- `int DOPlayForward(Material target)`
  （int DO播放前进（材质 target））
- `int DORestart(Component target, bool includeDelay = True)`
  （int DORestart（组件 target, bool includeDelay = True））
- `int DORestart(Material target, bool includeDelay = True)`
  （int DORestart（材质 target, bool includeDelay = True））
- `int DORewind(Component target, bool includeDelay = True)`
  （int DORewind（组件 target, bool includeDelay = True））
- `int DORewind(Material target, bool includeDelay = True)`
  （int DORewind（材质 target, bool includeDelay = True））
- `int DOSmoothRewind(Component target)`
  （int DOSmoothRewind（组件 target））
- `int DOSmoothRewind(Material target)`
  （int DOSmoothRewind（材质 target））
- `int DOTogglePause(Component target)`
  （int DO开关暂停（组件 target））
- `int DOTogglePause(Material target)`
  （int DO开关暂停（材质 target））

---

## ShoulderRotator（ShoulderRotator）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (4)

- `float weight`（float weight）(偏移: 0xC)
- `float offset`（float offset）(偏移: 0x10)
- `FullBodyBipedIK ik`（满身体BipedIK ik）(偏移: 0x14)
- `bool skip`（bool skip）(偏移: 0x18)

### 方法 (5)

- `void Start()`
  （void 开始（））
- `void RotateShoulders()`
  （void RotateShoulders（））
- `void RotateShoulder(FullBodyBipedChain chain, float weight, float offset)`
  （void RotateShoulder（满身体BipedChain chain, float weight, float offset））
- `IKMapping.BoneMap GetParentBoneMap(FullBodyBipedChain chain)`
  （IKMapping.Bone映射 获取父级Bone映射（满身体BipedChain chain））
- `void OnDestroy()`
  （void On销毁（））

---

## Side（侧面）

### 字段 (1)

- `byte value__`（byte value__）(偏移: 0x0)

---

## SideReactDirect（侧面反应方向）

### 字段 (2)

- `float mirrorProbability`（float mirrorProbability）(偏移: 0x0)
- `SideReactDirect.Data[] datas`（侧面ReactDirect.Data[] datas）(偏移: 0x4)

### 方法 (2)

- `bool GetMirror()`
  （bool 获取Mirror（））
- `int GetDirection(int ammo, bool mirror)`
  （int 获取方向（int ammo, bool mirror））

---

## SideReactDirect.Data（侧面ReactDirect.数据）

### 字段 (4)

- `int ammo`（int ammo）(偏移: 0x0)
- `float left`（float left）(偏移: 0x4)
- `float center`（float center）(偏移: 0x8)
- `float right`（float right）(偏移: 0xC)

---

## SignatureDescription（SignatureDescription）

### 字段 (4)

- `string _strKey`（string _str键）(偏移: 0x8)
- `string _strDigest`（string _strDigest）(偏移: 0xC)
- `string _strFormatter`（string _strFormatter）(偏移: 0x10)
- `string _strDeformatter`（string _strDeformatter）(偏移: 0x14)

### 方法 (4)

- `void set_KeyAlgorithm(string value)`
  （void set_键Algorithm（string value））
- `void set_DigestAlgorithm(string value)`
  （void set_DigestAlgorithm（string value））
- `void set_FormatterAlgorithm(string value)`
  （void set_FormatterAlgorithm（string value））
- `void set_DeformatterAlgorithm(string value)`
  （void set_DeformatterAlgorithm（string value））

---

## SimpleAnimStateAction（Simple动画状态动作）

**继承**: StateMachineBehaviour（状态MachineBehaviour）

### 字段 (4)

- `string Enter_ActionName`（string Enter_动作名称）(偏移: 0xC)
- `string Enter_Data`（string Enter_数据）(偏移: 0x10)
- `string Exit_ActionName`（string Exit_动作名称）(偏移: 0x14)
- `string Exit_Data`（string Exit_数据）(偏移: 0x18)

### 方法 (2)

- `void OnStateEnter(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)`
  （void On状态Enter（动画器 animator, 动画器状态信息 stateInfo, int layerIndex））
- `void OnStateExit(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)`
  （void On状态Exit（动画器 animator, 动画器状态信息 stateInfo, int layerIndex））

---

## SimpleCollator（SimpleCollator）

### 字段 (13)

- `bool QuickCheckDisabled`（bool Quick检查禁用的）(偏移: 0x0)
- `SimpleCollator invariant`（SimpleCollator invariant）(偏移: 0x4)
- `TextInfo textInfo`（文本信息 text信息）(偏移: 0x8)
- `CodePointIndexer cjkIndexer`（CodePointIndexer cjkIndexer）(偏移: 0xC)
- `Contraction[] contractions`（Contraction[] contractions）(偏移: 0x10)
- `Level2Map[] level2Maps`（Level2Map[] level2Maps）(偏移: 0x14)
- `byte[] unsafeFlags`（byte[] unsafeFlags）(偏移: 0x18)
- `byte* cjkCatTable`（byte* cjkCatTable）(偏移: 0x1C)
- `byte* cjkLv1Table`（byte* cjkLv1Table）(偏移: 0x20)
- `byte* cjkLv2Table`（byte* cjkLv2Table）(偏移: 0x24)
- `CodePointIndexer cjkLv2Indexer`（CodePointIndexer cjkLv2Indexer）(偏移: 0x28)
- `int lcid`（int lcid）(偏移: 0x2C)
- `bool frenchSort`（bool frenchSort）(偏移: 0x30)

### 方法 (45)

- `void SetCJKTable(CultureInfo culture, ref CodePointIndexer cjkIndexer, ref byte* catTable, ref byte* lv1Table, ref CodePointIndexer lv2Indexer, ref byte* lv2Table)`
  （void 集合CJKTable（Culture信息 culture, ref CodePointIndexer cjkIndexer, ref byte* catTable, ref byte* lv1Table, ref CodePointIndexer lv2Indexer, ref byte* lv2Table））
- `CultureInfo GetNeutralCulture(CultureInfo info)`
  （Culture信息 获取NeutralCulture（Culture信息 info））
- `byte Category(int cp)`
  （byte 类别（int cp））
- `byte Level1(int cp)`
  （byte Level1（int cp））
- `byte Level2(int cp, SimpleCollator.ExtenderType ext)`
  （byte Level2（int cp, SimpleCollator.Extender类型 ext））
- `bool IsHalfKana(int cp, CompareOptions opt)`
  （bool 是否HalfKana（int cp, CompareOptions opt））
- `Contraction GetContraction(string s, int start, int end)`
  （Contraction 获取Contraction（string s, int start, int end））
- `Contraction GetContraction(string s, int start, int end, Contraction[] clist)`
  （Contraction 获取Contraction（string s, int start, int end, Contraction[] clist））
- `Contraction GetTailContraction(string s, int start, int end)`
  （Contraction 获取TailContraction（string s, int start, int end））
- `Contraction GetTailContraction(string s, int start, int end, Contraction[] clist)`
  （Contraction 获取TailContraction（string s, int start, int end, Contraction[] clist））
- `int FilterOptions(int i, CompareOptions opt)`
  （int FilterOptions（int i, CompareOptions opt））
- `SimpleCollator.ExtenderType GetExtenderType(int i)`
  （SimpleCollator.Extender类型 获取Extender类型（int i））
- `byte ToDashTypeValue(SimpleCollator.ExtenderType ext, CompareOptions opt)`
  （byte ToDash类型值（SimpleCollator.Extender类型 ext, CompareOptions opt））
- `int FilterExtender(int i, SimpleCollator.ExtenderType ext, CompareOptions opt)`
  （int FilterExtender（int i, SimpleCollator.Extender类型 ext, CompareOptions opt））
- `bool IsIgnorable(int i, CompareOptions opt)`
  （bool 是否Ignorable（int i, CompareOptions opt））
- `bool IsSafe(int i)`
  （bool 是否Safe（int i））
- `SortKey GetSortKey(string s, CompareOptions options)`
  （Sort键 获取Sort键（string s, CompareOptions options））
- `SortKey GetSortKey(string s, int start, int length, CompareOptions options)`
  （Sort键 获取Sort键（string s, int start, int length, CompareOptions options））
- `void GetSortKey(string s, int start, int end, SortKeyBuffer buf, CompareOptions opt)`
  （void 获取Sort键（string s, int start, int end, Sort键缓冲区 buf, CompareOptions opt））
- `void FillSortKeyRaw(int i, SimpleCollator.ExtenderType ext, SortKeyBuffer buf, CompareOptions opt)`
  （void FillSort键Raw（int i, SimpleCollator.Extender类型 ext, Sort键缓冲区 buf, CompareOptions opt））
- `void FillSurrogateSortKeyRaw(int i, SortKeyBuffer buf)`
  （void FillSurrogateSort键Raw（int i, Sort键缓冲区 buf））
- `int Compare(string s1, int idx1, int len1, string s2, int idx2, int len2, CompareOptions options)`
  （int Compare（string s1, int idx1, int len1, string s2, int idx2, int len2, CompareOptions options））
- `void ClearBuffer(byte* buffer, int size)`
  （void 清除缓冲区（byte* buffer, int size））
- `int CompareInternal(string s1, int idx1, int len1, string s2, int idx2, int len2, out bool targetConsumed, out bool sourceConsumed, bool skipHeadingExtenders, bool immediateBreakup, ref SimpleCollator.Context ctx)`
  （int Compare内部的（string s1, int idx1, int len1, string s2, int idx2, int len2, out bool targetConsumed, out bool sourceConsumed, bool skipHeadingExtenders, bool immediateBreakup, ref SimpleCollator.Context ctx））
- `int CompareFlagPair(bool b1, bool b2)`
  （int Compare标志Pair（bool b1, bool b2））
- `bool IsPrefix(string src, string target, CompareOptions opt)`
  （bool 是否Prefix（string src, string target, CompareOptions opt））
- `bool IsPrefix(string s, string target, int start, int length, CompareOptions opt)`
  （bool 是否Prefix（string s, string target, int start, int length, CompareOptions opt））
- `bool IsPrefix(string s, string target, int start, int length, bool skipHeadingExtenders, ref SimpleCollator.Context ctx)`
  （bool 是否Prefix（string s, string target, int start, int length, bool skipHeadingExtenders, ref SimpleCollator.Context ctx））
- `bool IsSuffix(string src, string target, CompareOptions opt)`
  （bool 是否Suffix（string src, string target, CompareOptions opt））
- `bool IsSuffix(string s, string target, int start, int length, CompareOptions opt)`
  （bool 是否Suffix（string s, string target, int start, int length, CompareOptions opt））
- `int QuickIndexOf(string s, string target, int start, int length, out bool testWasUnable)`
  （int Quick索引Of（string s, string target, int start, int length, out bool testWasUnable））
- `int IndexOf(string s, string target, int start, int length, CompareOptions opt)`
  （int 索引Of（string s, string target, int start, int length, CompareOptions opt））
- `int IndexOfOrdinal(string s, string target, int start, int length)`
  （int 索引OfOrdinal（string s, string target, int start, int length））
- `int IndexOfOrdinal(string s, char target, int start, int length)`
  （int 索引OfOrdinal（string s, char target, int start, int length））
- `int IndexOfSortKey(string s, int start, int length, byte* sortkey, char target, int ti, bool noLv4, ref SimpleCollator.Context ctx)`
  （int 索引OfSort键（string s, int start, int length, byte* sortkey, char target, int ti, bool noLv4, ref SimpleCollator.Context ctx））
- `int IndexOf(string s, string target, int start, int length, byte* targetSortKey, ref SimpleCollator.Context ctx)`
  （int 索引Of（string s, string target, int start, int length, byte* targetSortKey, ref SimpleCollator.Context ctx））
- `int LastIndexOf(string s, string target, int start, int length, CompareOptions opt)`
  （int 最后一个索引Of（string s, string target, int start, int length, CompareOptions opt））
- `int LastIndexOfOrdinal(string s, string target, int start, int length)`
  （int 最后一个索引OfOrdinal（string s, string target, int start, int length））
- `int LastIndexOfSortKey(string s, int start, int orgStart, int length, byte* sortkey, int ti, bool noLv4, ref SimpleCollator.Context ctx)`
  （int 最后一个索引OfSort键（string s, int start, int orgStart, int length, byte* sortkey, int ti, bool noLv4, ref SimpleCollator.Context ctx））
- `int LastIndexOf(string s, string target, int start, int length, byte* targetSortKey, ref SimpleCollator.Context ctx)`
  （int 最后一个索引Of（string s, string target, int start, int length, byte* targetSortKey, ref SimpleCollator.Context ctx））
- `bool MatchesForward(string s, ref int idx, int end, int ti, byte* sortkey, bool noLv4, ref SimpleCollator.Context ctx)`
  （bool Matches前进（string s, ref int idx, int end, int ti, byte* sortkey, bool noLv4, ref SimpleCollator.Context ctx））
- `bool MatchesForwardCore(string s, ref int idx, int end, int ti, byte* sortkey, bool noLv4, SimpleCollator.ExtenderType ext, ref Contraction ct, ref SimpleCollator.Context ctx)`
  （bool Matches前进Core（string s, ref int idx, int end, int ti, byte* sortkey, bool noLv4, SimpleCollator.Extender类型 ext, ref Contraction ct, ref SimpleCollator.Context ctx））
- `bool MatchesPrimitive(CompareOptions opt, byte* source, int si, SimpleCollator.ExtenderType ext, byte* target, int ti, bool noLv4)`
  （bool MatchesPrimitive（CompareOptions opt, byte* source, int si, SimpleCollator.Extender类型 ext, byte* target, int ti, bool noLv4））
- `bool MatchesBackward(string s, ref int idx, int end, int orgStart, int ti, byte* sortkey, bool noLv4, ref SimpleCollator.Context ctx)`
  （bool Matches后退（string s, ref int idx, int end, int orgStart, int ti, byte* sortkey, bool noLv4, ref SimpleCollator.Context ctx））
- `bool MatchesBackwardCore(string s, ref int idx, int end, int orgStart, int ti, byte* sortkey, bool noLv4, SimpleCollator.ExtenderType ext, ref Contraction ct, ref SimpleCollator.Context ctx)`
  （bool Matches后退Core（string s, ref int idx, int end, int orgStart, int ti, byte* sortkey, bool noLv4, SimpleCollator.Extender类型 ext, ref Contraction ct, ref SimpleCollator.Context ctx））

---

## SimpleCollator.Context（SimpleCollator.Context）

### 字段 (7)

- `CompareOptions Option`（CompareOptions Option）(偏移: 0x0)
- `byte* NeverMatchFlags`（byte* Never比赛Flags）(偏移: 0x4)
- `byte* AlwaysMatchFlags`（byte* Always比赛Flags）(偏移: 0x8)
- `byte* Buffer1`（byte* Buffer1）(偏移: 0xC)
- `byte* Buffer2`（byte* Buffer2）(偏移: 0x10)
- `int PrevCode`（int PrevCode）(偏移: 0x14)
- `byte* PrevSortKey`（byte* PrevSort键）(偏移: 0x18)

---

## SimpleCollator.Escape（SimpleCollator.Escape）

### 字段 (5)

- `string Source`（string Source）(偏移: 0x0)
- `int Index`（int 索引）(偏移: 0x4)
- `int Start`（int 开始）(偏移: 0x8)
- `int End`（int 结束）(偏移: 0xC)
- `int Optional`（int Optional）(偏移: 0x10)

---

## SimpleCollator.ExtenderType（SimpleCollator.Extender类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SimpleCollator.PreviousInfo（SimpleCollator.上一个信息）

### 字段 (2)

- `int Code`（int Code）(偏移: 0x0)
- `byte* SortKey`（byte* Sort键）(偏移: 0x4)

---

## SimpleHudBase（SimpleHud基础）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (1)

- `GameObject all`（游戏对象 all）(偏移: 0xC)

### 方法 (3)

- `void Awake()`
  （void Awake（））
- `void MyPlayerInit(Player myPlayer)`
  （void My玩家初始化（玩家 myPlayer））
- `void SetVisible(bool value)`
  （void 集合可见的（bool value））

---

## SimpleObjectPool（Simple对象池）

**继承**: ObjectPool（对象池）

### 字段 (2)

- `GameObject prefab`（游戏对象 prefab）(偏移: 0xC)
- `Queue<RecyclableObject> pool`（Queue<RecyclableObject> pool）(偏移: 0x10)

### 方法 (2)

- `void Recycle(RecyclableObject obj)`
  （void Recycle（Recyclable对象 obj））
- `RecyclableObject Get()`
  （Recyclable对象 获取（））

---

## SimpleSmoothModifier（SimpleSmooth修改器）

**继承**: MonoModifier（Mono修改器）

### 字段 (9)

- `SimpleSmoothModifier.SmoothType smoothType`（SimpleSmoothModifier.Smooth类型 smooth类型）(偏移: 0x14)
- `int subdivisions`（int subdivisions）(偏移: 0x18)
- `int iterations`（int iterations）(偏移: 0x1C)
- `float strength`（float strength）(偏移: 0x20)
- `bool uniformLength`（bool uniformLength）(偏移: 0x24)
- `float maxSegmentLength`（float maxSegmentLength）(偏移: 0x28)
- `float bezierTangentLength`（float bezierTangentLength）(偏移: 0x2C)
- `float offset`（float offset）(偏移: 0x30)
- `float factor`（float factor）(偏移: 0x34)

### 方法 (7)

- `int get_Order()`
  （int get_Order（））
- `void Apply(Path p)`
  （void 应用（路径 p））
- `List<Vector3> CurvedNonuniform(List<Vector3> path)`
  （List<Vector3> CurvedNonuniform（List<Vector3> path））
- `Vector3 GetPointOnCubic(Vector3 a, Vector3 b, Vector3 tan1, Vector3 tan2, float t)`
  （三维向量 获取PointOnCubic（三维向量 a, 三维向量 b, 三维向量 tan1, 三维向量 tan2, float t））
- `List<Vector3> SmoothOffsetSimple(List<Vector3> path)`
  （List<Vector3> SmoothOffsetSimple（List<Vector3> path））
- `List<Vector3> SmoothSimple(List<Vector3> path)`
  （List<Vector3> SmoothSimple（List<Vector3> path））
- `List<Vector3> SmoothBezier(List<Vector3> path)`
  （List<Vector3> SmoothBezier（List<Vector3> path））

---

## SimpleSmoothModifier.SmoothType（SimpleSmoothModifier.Smooth类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Simulator（Simulator）

### 字段 (12)

- `bool doubleBuffering`（bool doubleBuffering）(偏移: 0x8)
- `float desiredDeltaTime`（float desiredDelta时间）(偏移: 0xC)
- `Simulator.Worker[] workers`（Simulator.Worker[] workers）(偏移: 0x10)
- `List<Agent> agents`（List<Agent> agents）(偏移: 0x14)
- `List<ObstacleVertex> obstacles`（List<ObstacleVertex> obstacles）(偏移: 0x18)
- `float deltaTime`（float delta时间）(偏移: 0x20)
- `float lastStep`（float lastStep）(偏移: 0x24)
- `bool doUpdateObstacles`（bool do更新Obstacles）(偏移: 0x28)
- `bool doCleanObstacles`（bool doCleanObstacles）(偏移: 0x29)
- `float symmetryBreakingBias`（float symmetryBreakingBias）(偏移: 0x2C)
- `MovementPlane movementPlane`（MovementPlane movementPlane）(偏移: 0x30)
- `Simulator.WorkerContext coroutineWorkerContext`（Simulator.WorkerContext coroutineWorkerContext）(偏移: 0x34)

### 方法 (28)

- `RVOQuadtree get_Quadtree()`
  （RVOQuadtree get_Quadtree（））
- `void set_Quadtree(RVOQuadtree value)`
  （void set_Quadtree（RVOQuadtree value））
- `float get_DeltaTime()`
  （float get_Delta时间（））
- `bool get_Multithreading()`
  （bool get_Multithreading（））
- `float get_DesiredDeltaTime()`
  （float get_DesiredDelta时间（））
- `void set_DesiredDeltaTime(float value)`
  （void set_DesiredDelta时间（float value））
- `List<Agent> GetAgents()`
  （List<Agent> 获取Agents（））
- `List<ObstacleVertex> GetObstacles()`
  （List<ObstacleVertex> 获取Obstacles（））
- `void ClearAgents()`
  （void 清除Agents（））
- `void OnDestroy()`
  （void On销毁（））
- `IAgent AddAgent(IAgent agent)`
  （IAgent 添加Agent（IAgent agent））
- `IAgent AddAgent(Vector3 position)`
  （IAgent 添加Agent（三维向量 position））
- `IAgent AddAgent(Vector2 position, float elevationCoordinate)`
  （IAgent 添加Agent（二维向量 position, float elevationCoordinate））
- `void RemoveAgent(IAgent agent)`
  （void 移除Agent（IAgent agent））
- `ObstacleVertex AddObstacle(ObstacleVertex v)`
  （ObstacleVertex 添加Obstacle（ObstacleVertex v））
- `ObstacleVertex AddObstacle(Vector3[] vertices, float height, bool cycle = True)`
  （ObstacleVertex 添加Obstacle（Vector3[] vertices, float height, bool cycle = True））
- `ObstacleVertex AddObstacle(Vector3[] vertices, float height, Matrix4x4 matrix, RVOLayer layer = 2, bool cycle = True)`
  （ObstacleVertex 添加Obstacle（Vector3[] vertices, float height, Matrix4x4 matrix, RVO层 layer = 2, bool cycle = True））
- `ObstacleVertex AddObstacle(Vector3 a, Vector3 b, float height)`
  （ObstacleVertex 添加Obstacle（三维向量 a, 三维向量 b, float height））
- `void UpdateObstacle(ObstacleVertex obstacle, Vector3[] vertices, Matrix4x4 matrix)`
  （void 更新Obstacle（ObstacleVertex obstacle, Vector3[] vertices, Matrix4x4 matrix））
- `void ScheduleCleanObstacles()`
  （void ScheduleCleanObstacles（））
- `void CleanObstacles()`
  （void CleanObstacles（））
- `void RemoveObstacle(ObstacleVertex v)`
  （void 移除Obstacle（ObstacleVertex v））
- `void UpdateObstacles()`
  （void 更新Obstacles（））
- `void BuildQuadtree()`
  （void BuildQuadtree（））
- `void BlockUntilSimulationStepIsDone()`
  （void BlockUntilSimulationStep是否Done（））
- `void PreCalculation()`
  （void PreCalculation（））
- `void CleanAndUpdateObstaclesIfNecessary()`
  （void CleanAnd更新ObstaclesIfNecessary（））
- `void Update()`
  （void 更新（））

---

## Simulator.Worker（Simulator.Worker）

### 字段 (8)

- `int start`（int start）(偏移: 0x8)
- `int end`（int end）(偏移: 0xC)
- `AutoResetEvent runFlag`（自动重置事件 run标志）(偏移: 0x10)
- `ManualResetEvent waitFlag`（手动重置事件 wait标志）(偏移: 0x14)
- `Simulator simulator`（Simulator simulator）(偏移: 0x18)
- `int task`（int task）(偏移: 0x1C)
- `bool terminate`（bool terminate）(偏移: 0x20)
- `Simulator.WorkerContext context`（Simulator.WorkerContext context）(偏移: 0x24)

### 方法 (4)

- `void Execute(int task)`
  （void 执行（int task））
- `void WaitOne()`
  （void WaitOne（））
- `void Terminate()`
  （void Terminate（））
- `void Run()`
  （void 运行（））

---

## Simulator.WorkerContext（Simulator.WorkerContext）

### 字段 (6)

- `Agent.VOBuffer vos`（Agent.VO缓冲区 vos）(偏移: 0x8)
- `Vector2[] bestPos`（Vector2[] bestPos）(偏移: 0xC)
- `float[] bestSizes`（float[] bestSizes）(偏移: 0x10)
- `float[] bestScores`（float[] bestScores）(偏移: 0x14)
- `Vector2[] samplePos`（Vector2[] samplePos）(偏移: 0x18)
- `float[] sampleSize`（float[] sample大小）(偏移: 0x1C)

---

## Single（单个）

**继承**: IComparable, IFormattable, IConvertible, IComparable<float>, IEquatable<float>（IComparable, IFormattable, IConvertible, IComparable<float>, IEquatable<float>）

### 字段 (1)

- `float m_value`（float m_value）(偏移: 0x0)

### 方法 (18)

- `bool IsInfinity(float f)`
  （bool 是否无限（float f））
- `bool IsPositiveInfinity(float f)`
  （bool 是否Positive无限（float f））
- `bool IsNaN(float f)`
  （bool 是否NaN（float f））
- `int CompareTo(object value)`
  （int CompareTo（object value））
- `int CompareTo(float value)`
  （int CompareTo（float value））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `bool Equals(float obj)`
  （bool Equals（float obj））
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
- `float Parse(string s, IFormatProvider provider)`
  （float 解析（string s, I格式化提供者 provider））
- `float Parse(string s, NumberStyles style, IFormatProvider provider)`
  （float 解析（string s, NumberStyles style, I格式化提供者 provider））
- `float Parse(string s, NumberStyles style, NumberFormatInfo info)`
  （float 解析（string s, NumberStyles style, Number格式化信息 info））
- `bool TryParse(string s, out float result)`
  （bool Try解析（string s, out float result））
- `bool TryParse(string s, NumberStyles style, NumberFormatInfo info, out float result)`
  （bool Try解析（string s, NumberStyles style, Number格式化信息 info, out float result））
- `TypeCode GetTypeCode()`
  （类型Code 获取类型Code（））

---

## SingleArrayTypeInfo（单个数组类型信息）

**继承**: TraceLoggingTypeInfo<float[]>（TraceLogging类型Info<float[]>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void WriteMetadata（TraceLoggingMetadataCollector collector, string name, 事件Field格式化 format））
- `void WriteData(TraceLoggingDataCollector collector, ref float[] value)`
  （void Write数据（TraceLogging数据Collector collector, ref float[] value））

---

## SingleCallIdentity（单个CallIdentity）

**继承**: ServerIdentity（服务器Identity）

### 方法 (2)

- `IMessage SyncObjectProcessMessage(IMessage msg)`
  （IMessage 同步对象处理Message（IMessage msg））
- `IMessageCtrl AsyncObjectProcessMessage(IMessage msg, IMessageSink replySink)`
  （IMessageCtrl 异步对象处理Message（IMessage msg, IMessageSink replySink））

---

## SingleConverter（单个Converter）

**继承**: BaseNumberConverter（基础NumberConverter）

### 方法 (6)

- `bool get_AllowHex()`
  （bool get_允许Hex（））
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

## SingleNodeBlocker（单个节点Blocker）

**继承**: VersionedMonoBehaviour（VersionedMonoBehaviour）

### 字段 (1)

- `BlockManager manager`（Block管理器 manager）(偏移: 0x14)

### 方法 (6)

- `GraphNode get_lastBlocked()`
  （Graph节点 get_lastBlocked（））
- `void set_lastBlocked(GraphNode value)`
  （void set_lastBlocked（Graph节点 value））
- `void BlockAtCurrentPosition()`
  （void BlockAt当前Position（））
- `void BlockAt(Vector3 position)`
  （void BlockAt（三维向量 position））
- `void Block(GraphNode node)`
  （void Block（Graph节点 node））
- `void Unblock()`
  （void Unblock（））

---

## SinglePassStereoMode（单个PassStereo模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SingleTypeInfo（单个类型信息）

**继承**: TraceLoggingTypeInfo<float>（TraceLogging类型Info<float>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void WriteMetadata（TraceLoggingMetadataCollector collector, string name, 事件Field格式化 format））
- `void WriteData(TraceLoggingDataCollector collector, ref float value)`
  （void Write数据（TraceLogging数据Collector collector, ref float value））

---

## SingletonIdentity（单例Identity）

**继承**: ServerIdentity（服务器Identity）

### 方法 (3)

- `MarshalByRefObject GetServerObject()`
  （MarshalByRef对象 获取服务器对象（））
- `IMessage SyncObjectProcessMessage(IMessage msg)`
  （IMessage 同步对象处理Message（IMessage msg））
- `IMessageCtrl AsyncObjectProcessMessage(IMessage msg, IMessageSink replySink)`
  （IMessageCtrl 异步对象处理Message（IMessage msg, IMessageSink replySink））

---

## SinkProviderData（Sink提供者数据）

### 字段 (3)

- `string sinkName`（string sink名称）(偏移: 0x8)
- `ArrayList children`（数组列表 children）(偏移: 0xC)
- `Hashtable properties`（Hashtable properties）(偏移: 0x10)

### 方法 (2)

- `IList get_Children()`
  （I列表 get_Children（））
- `IDictionary get_Properties()`
  （I字典 get_Properties（））

---

## SizedArray（Sized数组）

**继承**: ICloneable（ICloneable）

### 字段 (2)

- `object[] objects`（object[] objects）(偏移: 0x8)
- `object[] negObjects`（object[] negObjects）(偏移: 0xC)

### 方法 (4)

- `object Clone()`
  （object 克隆（））
- `object get_Item(int index)`
  （object get_项目（int index））
- `void set_Item(int index, object value)`
  （void set_项目（int index, object value））
- `void IncreaseCapacity(int index)`
  （void IncreaseCapacity（int index））

---

## SkeletonBone（SkeletonBone）

### 字段 (5)

- `string name`（string name）(偏移: 0x0)
- `string parentName`（string parent名称）(偏移: 0x4)
- `Vector3 position`（三维向量 position）(偏移: 0x8)
- `Quaternion rotation`（Quaternion rotation）(偏移: 0x14)
- `Vector3 scale`（三维向量 scale）(偏移: 0x24)

---

## Skill（技能）

### 字段 (4)

- `string name`（string name）(偏移: 0x8)
- `HUD_SkillBtn skillBtn`（HUD_技能Btn skillBtn）(偏移: 0xC)
- `bool disabled`（bool disabled）(偏移: 0x10)
- `Action Remove_Listener`（动作 Remove_监听器）(偏移: 0x18)

### 方法 (2)

- `void OnRemoveFromPlayer(Player player)`
  （void On移除From玩家（玩家 player））
- `bool TryGetSkillAI(Bot bot, out BotSkillBase skillAI)`
  （bool Try获取技能AI（机器人 bot, out BotSkillBase skillAI））

---

## SkillKey（技能键）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Skill_Common（Skill_Common）

**继承**: Skill（技能）

### 字段 (2)

- `float coldFinishTime`（float coldFinish时间）(偏移: 0x1C)
- `float coldTime`（float cold时间）(偏移: 0x24)

### 方法 (9)

- `bool get_isColdFinish()`
  （bool get_isColdFinish（））
- `bool get_isCanUse()`
  （bool get_is能否Use（））
- `int GetSpriteIndex()`
  （int 获取精灵索引（））
- `bool TryUse(Player player)`
  （bool TryUse（玩家 player））
- `bool BasicCheck()`
  （bool Basic检查（））
- `void OnPlayerReSpawn()`
  （void On玩家Re出生（））
- `void OnSetOnPlayer(Player player)`
  （void On集合On玩家（玩家 player））
- `void StartCold()`
  （void 开始Cold（））
- `void EndCold()`
  （void 结束Cold（））

---

## Skill_ModeChange（Skill_模式Change）

**继承**: Skill（技能）

### 字段 (2)

- `Func<bool> getModeState`（Func<bool> get模式状态）(偏移: 0x1C)
- `Func<bool> changeModeFunc`（Func<bool> change模式Func）(偏移: 0x20)

### 方法 (4)

- `int GetSpriteIndex()`
  （int 获取精灵索引（））
- `bool TryUse(Player player)`
  （bool TryUse（玩家 player））
- `void OnPlayerReSpawn()`
  （void On玩家Re出生（））
- `void OnSetOnPlayer(Player player)`
  （void On集合On玩家（玩家 player））

---

## Skill_SentryGun（Skill_Sentry枪械）

**继承**: Skill_Common（Skill_Common）

### 字段 (1)

- `SentryGun bindSentry`（Sentry枪械 bindSentry）(偏移: 0x28)

### 方法 (2)

- `void BindSentry(SentryGun sentry)`
  （void BindSentry（Sentry枪械 sentry））
- `bool IsNoneSentryGun()`
  （bool 是否无Sentry枪械（））

---

## Sky（Sky）

### 字段 (3)

- `Cubemap cubemap`（Cubemap cubemap）(偏移: 0x0)
- `float longitudeOffset`（float longitudeOffset）(偏移: 0x4)
- `float exposure`（float exposure）(偏移: 0x8)

---

## Skybox（Skybox）

**继承**: Behaviour（Behaviour）

### 方法 (1)

- `Material get_material()`
  （材质 get_material（））

---

## Slider（滑块）

**继承**: Selectable, IDragHandler, IEventSystemHandler, IInitializePotentialDragHandler, ICanvasElement（Selectable, IDrag处理器, I事件系统处理器, I初始化PotentialDrag处理器, I画布元素）

### 字段 (16)

- `RectTransform m_FillRect`（Rect变换 m_FillRect）(偏移: 0xB0)
- `RectTransform m_HandleRect`（Rect变换 m_句柄Rect）(偏移: 0xB4)
- `Slider.Direction m_Direction`（Slider.方向 m_方向）(偏移: 0xB8)
- `float m_MinValue`（float m_最小值）(偏移: 0xBC)
- `float m_MaxValue`（float m_最大值）(偏移: 0xC0)
- `bool m_WholeNumbers`（bool m_WholeNumbers）(偏移: 0xC4)
- `float m_Value`（float m_值）(偏移: 0xC8)
- `Slider.SliderEvent m_OnValueChanged`（Slider.滑块事件 m_On值Changed）(偏移: 0xCC)
- `Image m_FillImage`（图像 m_Fill图像）(偏移: 0xD0)
- `Transform m_FillTransform`（变换 m_Fill变换）(偏移: 0xD4)
- `RectTransform m_FillContainerRect`（Rect变换 m_Fill容器Rect）(偏移: 0xD8)
- `Transform m_HandleTransform`（变换 m_句柄变换）(偏移: 0xDC)
- `RectTransform m_HandleContainerRect`（Rect变换 m_句柄容器Rect）(偏移: 0xE0)
- `Vector2 m_Offset`（二维向量 m_Offset）(偏移: 0xE4)
- `DrivenRectTransformTracker m_Tracker`（DrivenRect变换Tracker m_Tracker）(偏移: 0xEC)
- `bool m_DelayedUpdateVisuals`（bool m_Delayed更新Visuals）(偏移: 0xED)

### 方法 (45)

- `RectTransform get_fillRect()`
  （Rect变换 get_fillRect（））
- `void set_fillRect(RectTransform value)`
  （void set_fillRect（Rect变换 value））
- `RectTransform get_handleRect()`
  （Rect变换 get_handleRect（））
- `void set_handleRect(RectTransform value)`
  （void set_handleRect（Rect变换 value））
- `Slider.Direction get_direction()`
  （Slider.方向 get_direction（））
- `void set_direction(Slider.Direction value)`
  （void set_direction（Slider.方向 value））
- `float get_minValue()`
  （float get_min值（））
- `void set_minValue(float value)`
  （void set_min值（float value））
- `float get_maxValue()`
  （float get_max值（））
- `void set_maxValue(float value)`
  （void set_max值（float value））
- `bool get_wholeNumbers()`
  （bool get_wholeNumbers（））
- `void set_wholeNumbers(bool value)`
  （void set_wholeNumbers（bool value））
- `float get_value()`
  （float get_value（））
- `void set_value(float value)`
  （void set_value（float value））
- `void SetValueWithoutNotify(float input)`
  （void 集合值WithoutNotify（float input））
- `float get_normalizedValue()`
  （float get_normalized值（））
- `void set_normalizedValue(float value)`
  （void set_normalized值（float value））
- `Slider.SliderEvent get_onValueChanged()`
  （Slider.滑块事件 get_on值Changed（））
- `void set_onValueChanged(Slider.SliderEvent value)`
  （void set_on值Changed（Slider.滑块事件 value））
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
- `void OnDidApplyAnimationProperties()`
  （void OnDid应用动画Properties（））
- `void UpdateCachedReferences()`
  （void 更新CachedReferences（））
- `float ClampValue(float input)`
  （float Clamp值（float input））
- `void Set(float input, bool sendCallback = True)`
  （void 集合（float input, bool sendCallback = True））
- `void OnRectTransformDimensionsChange()`
  （void OnRect变换DimensionsChange（））
- `Slider.Axis get_axis()`
  （Slider.轴 get_axis（））
- `bool get_reverseValue()`
  （bool get_reverse值（））
- `void UpdateVisuals()`
  （void 更新Visuals（））
- `void UpdateDrag(PointerEventData eventData, Camera cam)`
  （void 更新Drag（指针事件数据 eventData, 摄像机 cam））
- `bool MayDrag(PointerEventData eventData)`
  （bool MayDrag（指针事件数据 eventData））
- `void OnPointerDown(PointerEventData eventData)`
  （void On指针下（指针事件数据 eventData））
- `void OnDrag(PointerEventData eventData)`
  （void OnDrag（指针事件数据 eventData））
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
- `void SetDirection(Slider.Direction direction, bool includeRectLayouts)`
  （void 集合方向（Slider.方向 direction, bool includeRectLayouts））

---

## Slider.Axis（Slider.轴）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Slider.Direction（Slider.方向）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SmallRect（SmallRect）

### 字段 (4)

- `short Left`（short 左）(偏移: 0x0)
- `short Top`（short 顶部）(偏移: 0x2)
- `short Right`（short 右）(偏移: 0x4)
- `short Bottom`（short 底部）(偏移: 0x6)

---

## SmallXmlParser（SmallXmlParser）

### 字段 (12)

- `SmallXmlParser.IContentHandler handler`（SmallXmlParser.IContent处理器 handler）(偏移: 0x8)
- `TextReader reader`（文本读取器 reader）(偏移: 0xC)
- `Stack elementNames`（栈 elementNames）(偏移: 0x10)
- `Stack xmlSpaces`（栈 xmlSpaces）(偏移: 0x14)
- `string xmlSpace`（string xmlSpace）(偏移: 0x18)
- `StringBuilder buffer`（字符串构建器 buffer）(偏移: 0x1C)
- `char[] nameBuffer`（char[] name缓冲区）(偏移: 0x20)
- `bool isWhitespace`（bool isWhitespace）(偏移: 0x24)
- `SmallXmlParser.AttrListImpl attributes`（SmallXmlParser.Attr列表Impl attributes）(偏移: 0x28)
- `int line`（int line）(偏移: 0x2C)
- `int column`（int column）(偏移: 0x30)
- `bool resetColumn`（bool resetColumn）(偏移: 0x34)

### 方法 (22)

- `Exception Error(string msg)`
  （Exception Error（string msg））
- `Exception UnexpectedEndError()`
  （Exception Unexpected结束Error（））
- `bool IsNameChar(char c, bool start)`
  （bool 是否名称Char（char c, bool start））
- `bool IsWhitespace(int c)`
  （bool 是否Whitespace（int c））
- `void SkipWhitespaces()`
  （void SkipWhitespaces（））
- `void HandleWhitespaces()`
  （void 句柄Whitespaces（））
- `void SkipWhitespaces(bool expected)`
  （void SkipWhitespaces（bool expected））
- `int Peek()`
  （int Peek（））
- `int Read()`
  （int Read（））
- `void Expect(int c)`
  （void Expect（int c））
- `string ReadUntil(char until, bool handleReferences)`
  （string ReadUntil（char until, bool handleReferences））
- `string ReadName()`
  （string Read名称（））
- `void Parse(TextReader input, SmallXmlParser.IContentHandler handler)`
  （void 解析（文本读取器 input, SmallXmlParser.IContent处理器 handler））
- `void Cleanup()`
  （void 清理（））
- `void ReadContent()`
  （void ReadContent（））
- `void HandleBufferedContent()`
  （void 句柄BufferedContent（））
- `void ReadCharacters()`
  （void ReadCharacters（））
- `void ReadReference()`
  （void Read引用（））
- `int ReadCharacterReference()`
  （int Read角色引用（））
- `void ReadAttribute(SmallXmlParser.AttrListImpl a)`
  （void ReadAttribute（SmallXmlParser.Attr列表Impl a））
- `void ReadCDATASection()`
  （void ReadCDATASection（））
- `void ReadComment()`
  （void ReadComment（））

---

## SmallXmlParser.AttrListImpl（SmallXmlParser.Attr列表Impl）

**继承**: SmallXmlParser.IAttrList（SmallXmlParser.IAttr列表）

### 字段 (2)

- `List<string> attrNames`（List<string> attrNames）(偏移: 0x8)
- `List<string> attrValues`（List<string> attrValues）(偏移: 0xC)

### 方法 (8)

- `int get_Length()`
  （int get_Length（））
- `string GetName(int i)`
  （string 获取名称（int i））
- `string GetValue(int i)`
  （string 获取值（int i））
- `string GetValue(string name)`
  （string 获取值（string name））
- `string[] get_Names()`
  （string[] get_Names（））
- `string[] get_Values()`
  （string[] get_Values（））
- `void Clear()`
  （void 清除（））
- `void Add(string name, string value)`
  （void 添加（string name, string value））

---

## SmallXmlParserException（SmallXmlParserException）

**继承**: SystemException（系统Exception）

### 字段 (2)

- `int line`（int line）(偏移: 0x44)
- `int column`（int column）(偏移: 0x48)

---

## SnapToNode（SnapTo节点）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 方法 (1)

- `void Update()`
  （void 更新（））

---

## SoapAttribute（SoapAttribute）

**继承**: Attribute（Attribute）

### 字段 (3)

- `bool _useAttribute`（bool _useAttribute）(偏移: 0x8)
- `string ProtXmlNamespace`（string ProtXmlNamespace）(偏移: 0xC)
- `object ReflectInfo`（object Reflect信息）(偏移: 0x10)

### 方法 (3)

- `bool get_UseAttribute()`
  （bool get_UseAttribute（））
- `string get_XmlNamespace()`
  （string get_XmlNamespace（））
- `void SetReflectionObject(object reflectionObject)`
  （void 集合Reflection对象（object reflectionObject））

---

## SoapFieldAttribute（SoapFieldAttribute）

**继承**: SoapAttribute（SoapAttribute）

### 字段 (2)

- `string _elementName`（string _element名称）(偏移: 0x14)
- `bool _isElement`（bool _is元素）(偏移: 0x18)

### 方法 (3)

- `string get_XmlElementName()`
  （string get_Xml元素名称（））
- `bool IsInteropXmlElement()`
  （bool 是否InteropXml元素（））
- `void SetReflectionObject(object reflectionObject)`
  （void 集合Reflection对象（object reflectionObject））

---

## SoapMethodAttribute（SoapMethodAttribute）

**继承**: SoapAttribute（SoapAttribute）

### 字段 (6)

- `string _responseElement`（string _response元素）(偏移: 0x14)
- `string _responseNamespace`（string _responseNamespace）(偏移: 0x18)
- `string _returnElement`（string _return元素）(偏移: 0x1C)
- `string _soapAction`（string _soap动作）(偏移: 0x20)
- `bool _useAttribute`（bool _useAttribute）(偏移: 0x24)
- `string _namespace`（string _namespace）(偏移: 0x28)

### 方法 (3)

- `bool get_UseAttribute()`
  （bool get_UseAttribute（））
- `string get_XmlNamespace()`
  （string get_XmlNamespace（））
- `void SetReflectionObject(object reflectionObject)`
  （void 集合Reflection对象（object reflectionObject））

---

## SoapServices（SoapServices）

### 字段 (5)

- `Hashtable _xmlTypes`（Hashtable _xmlTypes）(偏移: 0x0)
- `Hashtable _xmlElements`（Hashtable _xmlElements）(偏移: 0x4)
- `Hashtable _soapActions`（Hashtable _soapActions）(偏移: 0x8)
- `Hashtable _soapActionsMethods`（Hashtable _soapActionsMethods）(偏移: 0xC)
- `Hashtable _typeInfos`（Hashtable _typeInfos）(偏移: 0x10)

### 方法 (15)

- `string get_XmlNsForClrTypeWithAssembly()`
  （string get_XmlNsForClr类型WithAssembly（））
- `string get_XmlNsForClrTypeWithNs()`
  （string get_XmlNsForClr类型WithNs（））
- `string get_XmlNsForClrTypeWithNsAndAssembly()`
  （string get_XmlNsForClr类型WithNsAndAssembly（））
- `string CodeXmlNamespaceForClrTypeNamespace(string typeNamespace, string assemblyName)`
  （string CodeXmlNamespaceForClr类型Namespace（string typeNamespace, string assemblyName））
- `string GetNameKey(string name, string namspace)`
  （string 获取名称键（string name, string namspace））
- `string GetAssemblyName(MethodBase mb)`
  （string 获取Assembly名称（Method基础 mb））
- `bool GetXmlElementForInteropType(Type type, out string xmlElement, out string xmlNamespace)`
  （bool 获取Xml元素ForInterop类型（类型 type, out string xmlElement, out string xmlNamespace））
- `string GetXmlNamespaceForMethodCall(MethodBase mb)`
  （string 获取XmlNamespaceForMethodCall（Method基础 mb））
- `string GetXmlNamespaceForMethodResponse(MethodBase mb)`
  （string 获取XmlNamespaceForMethod响应（Method基础 mb））
- `bool GetXmlTypeForInteropType(Type type, out string xmlType, out string xmlTypeNamespace)`
  （bool 获取Xml类型ForInterop类型（类型 type, out string xmlType, out string xmlTypeNamespace））
- `void PreLoad(Assembly assembly)`
  （void Pre加载（Assembly assembly））
- `void PreLoad(Type type)`
  （void Pre加载（类型 type））
- `void RegisterInteropXmlElement(string xmlElement, string xmlNamespace, Type type)`
  （void RegisterInteropXml元素（string xmlElement, string xmlNamespace, 类型 type））
- `void RegisterInteropXmlType(string xmlType, string xmlTypeNamespace, Type type)`
  （void RegisterInteropXml类型（string xmlType, string xmlTypeNamespace, 类型 type））
- `string EncodeNs(string ns)`
  （string EncodeNs（string ns））

---

## SoapServices.TypeInfo（SoapServices.类型信息）

### 字段 (2)

- `Hashtable Attributes`（Hashtable Attributes）(偏移: 0x8)
- `Hashtable Elements`（Hashtable Elements）(偏移: 0xC)

---

## SoapTypeAttribute（Soap类型Attribute）

**继承**: SoapAttribute（SoapAttribute）

### 字段 (7)

- `bool _useAttribute`（bool _useAttribute）(偏移: 0x14)
- `string _xmlElementName`（string _xml元素名称）(偏移: 0x18)
- `string _xmlNamespace`（string _xmlNamespace）(偏移: 0x1C)
- `string _xmlTypeName`（string _xml类型名称）(偏移: 0x20)
- `string _xmlTypeNamespace`（string _xml类型Namespace）(偏移: 0x24)
- `bool _isType`（bool _is类型）(偏移: 0x28)
- `bool _isElement`（bool _is元素）(偏移: 0x29)

### 方法 (8)

- `bool get_UseAttribute()`
  （bool get_UseAttribute（））
- `string get_XmlElementName()`
  （string get_Xml元素名称（））
- `string get_XmlNamespace()`
  （string get_XmlNamespace（））
- `string get_XmlTypeName()`
  （string get_Xml类型名称（））
- `string get_XmlTypeNamespace()`
  （string get_Xml类型Namespace（））
- `bool get_IsInteropXmlElement()`
  （bool get_是否InteropXml元素（））
- `bool get_IsInteropXmlType()`
  （bool get_是否InteropXml类型（））
- `void SetReflectionObject(object reflectionObject)`
  （void 集合Reflection对象（object reflectionObject））

---

## SocketElement（套接字元素）

**继承**: ConfigurationElement（Configuration元素）

### 方法 (1)

- `ConfigurationPropertyCollection get_Properties()`
  （Configuration属性Collection get_Properties（））

---

## SocketError（套接字Error）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SocketException（套接字Exception）

**继承**: Win32Exception（Win32Exception）

### 字段 (1)

- `EndPoint m_EndPoint`（结束Point m_结束Point）(偏移: 0x48)

### 方法 (2)

- `int WSAGetLastError_internal()`
  （int WSA获取最后一个Error_internal（））
- `string get_Message()`
  （string get_Message（））

---

## SocketItem（套接字项目）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (2)

- `SocketItem.ItemType itemType`（套接字Item.项目类型 item类型）(偏移: 0xC)
- `Vector3 itemEuler`（三维向量 itemEuler）(偏移: 0x0)

### 方法 (1)

- `void BindOnCharacter(CharacterModel characterModel)`
  （void BindOn角色（角色模型 characterModel））

---

## SocketItem.ItemType（套接字Item.项目类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SoftMask（Soft掩码）

**继承**: Mask, IMeshModifier（掩码, I网格修改器）

### 字段 (32)

- `List<SoftMask>[] s_TmpSoftMasks`（List<SoftMask>[] s_TmpSoftMasks）(偏移: 0x0)
- `Color[] s_ClearColors`（Color[] s_清除Colors）(偏移: 0x4)
- `bool s_UVStartsAtTop`（bool s_UVStartsAt顶部）(偏移: 0x8)
- `bool s_IsMetal`（bool s_是否Metal）(偏移: 0x9)
- `Shader s_SoftMaskShader`（着色器 s_Soft掩码着色器）(偏移: 0xC)
- `Texture2D s_ReadTexture`（Texture2D s_Read纹理）(偏移: 0x10)
- `List<SoftMask> s_ActiveSoftMasks`（List<SoftMask> s_激活的SoftMasks）(偏移: 0x14)
- `List<SoftMask> s_TempRelatables`（List<SoftMask> s_TempRelatables）(偏移: 0x18)
- `int s_StencilCompId`（int s_StencilCompId）(偏移: 0x24)
- `int s_ColorMaskId`（int s_颜色掩码Id）(偏移: 0x28)
- `int s_MainTexId`（int s_主要的TexId）(偏移: 0x2C)
- `int s_SoftnessId`（int s_SoftnessId）(偏移: 0x30)
- `int s_Alpha`（int s_透明度）(偏移: 0x34)
- `int s_PreviousWidth`（int s_上一个宽度）(偏移: 0x38)
- `int s_PreviousHeight`（int s_上一个高度）(偏移: 0x3C)
- `MaterialPropertyBlock _mpb`（材质属性Block _mpb）(偏移: 0x20)
- `CommandBuffer _cb`（Command缓冲区 _cb）(偏移: 0x24)
- `Material _material`（材质 _material）(偏移: 0x28)
- `RenderTexture _softMaskBuffer`（Render纹理 _soft掩码缓冲区）(偏移: 0x2C)
- `int _stencilDepth`（int _stencil深度）(偏移: 0x30)
- `Mesh _mesh`（网格 _mesh）(偏移: 0x34)
- `SoftMask _parent`（Soft掩码 _parent）(偏移: 0x38)
- `List<SoftMask> _children`（List<SoftMask> _children）(偏移: 0x3C)
- `bool _hasChanged`（bool _hasChanged）(偏移: 0x40)
- `bool _hasStencilStateChanged`（bool _hasStencil状态Changed）(偏移: 0x41)
- `SoftMask.DownSamplingRate m_DownSamplingRate`（SoftMask.下SamplingRate m_下SamplingRate）(偏移: 0x44)
- `float m_Softness`（float m_Softness）(偏移: 0x48)
- `float m_Alpha`（float m_透明度）(偏移: 0x4C)
- `bool m_IgnoreParent`（bool m_Ignore父级）(偏移: 0x50)
- `bool m_PartOfParent`（bool m_PartOf父级）(偏移: 0x51)
- `bool m_IgnoreSelfGraphic`（bool m_IgnoreSelfGraphic）(偏移: 0x52)
- `bool m_IgnoreSelfStencil`（bool m_IgnoreSelfStencil）(偏移: 0x53)

### 方法 (34)

- `SoftMask.DownSamplingRate get_downSamplingRate()`
  （SoftMask.下SamplingRate get_downSamplingRate（））
- `void set_downSamplingRate(SoftMask.DownSamplingRate value)`
  （void set_downSamplingRate（SoftMask.下SamplingRate value））
- `float get_softness()`
  （float get_softness（））
- `void set_softness(float value)`
  （void set_softness（float value））
- `float get_alpha()`
  （float get_alpha（））
- `void set_alpha(float value)`
  （void set_alpha（float value））
- `bool get_ignoreParent()`
  （bool get_ignore父级（））
- `void set_ignoreParent(bool value)`
  （void set_ignore父级（bool value））
- `bool get_partOfParent()`
  （bool get_partOf父级（））
- `void set_partOfParent(bool value)`
  （void set_partOf父级（bool value））
- `RenderTexture get_softMaskBuffer()`
  （Render纹理 get_soft掩码缓冲区（））
- `bool get_hasChanged()`
  （bool get_hasChanged（））
- `void set_hasChanged(bool value)`
  （void set_hasChanged（bool value））
- `SoftMask get_parent()`
  （Soft掩码 get_parent（））
- `bool get_ignoreSelfGraphic()`
  （bool get_ignoreSelfGraphic（））
- `void set_ignoreSelfGraphic(bool value)`
  （void set_ignoreSelfGraphic（bool value））
- `bool get_ignoreSelfStencil()`
  （bool get_ignoreSelfStencil（））
- `void set_ignoreSelfStencil(bool value)`
  （void set_ignoreSelfStencil（bool value））
- `Material get_material()`
  （材质 get_material（））
- `Mesh get_mesh()`
  （网格 get_mesh（））
- `Material GetModifiedMaterial(Material baseMaterial)`
  （材质 获取Modified材质（材质 baseMaterial））
- `bool IsRaycastLocationValid(Vector2 sp, Camera eventCamera, Graphic g, int[] interactions)`
  （bool 是否RaycastLocationValid（二维向量 sp, 摄像机 eventCamera, Graphic g, int[] interactions））
- `bool IsRaycastLocationValid(Vector2 sp, Camera eventCamera)`
  （bool 是否RaycastLocationValid（二维向量 sp, 摄像机 eventCamera））
- `void OnEnable()`
  （void On启用（））
- `void OnDisable()`
  （void On禁用（））
- `void OnTransformParentChanged()`
  （void On变换父级Changed（））
- `void OnRectTransformDimensionsChange()`
  （void OnRect变换DimensionsChange（））
- `void UpdateMaskTextures()`
  （void 更新掩码Textures（））
- `void UpdateMaskTexture()`
  （void 更新掩码纹理（））
- `void GetDownSamplingSize(SoftMask.DownSamplingRate rate, out int w, out int h)`
  （void 获取下Sampling大小（SoftMask.下SamplingRate rate, out int w, out int h））
- `void ReleaseRt(ref RenderTexture tmpRT)`
  （void ReleaseRt（ref RenderTexture tmpRT））
- `void ReleaseObject(Object obj)`
  （void Release对象（对象 obj））
- `void SetParent(SoftMask newParent)`
  （void 集合父级（Soft掩码 newParent））
- `float GetPixelValue(int x, int y, int[] interactions)`
  （float 获取Pixel值（int x, int y, int[] interactions））

---

## SoftMask.DownSamplingRate（SoftMask.下SamplingRate）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SoftMaskable（SoftMaskable）

**继承**: MonoBehaviour, IMaterialModifier, ICanvasRaycastFilter（MonoBehaviour行为, I材质修改器, I画布RaycastFilter）

### 字段 (15)

- `Hash128 k_InvalidHash`（Hash128 k_InvalidHash）(偏移: 0x0)
- `int s_SoftMaskTexId`（int s_Soft掩码TexId）(偏移: 0x10)
- `int s_StencilCompId`（int s_StencilCompId）(偏移: 0x14)
- `int s_MaskInteractionId`（int s_掩码InteractionId）(偏移: 0x18)
- `int s_GameVPId`（int s_游戏VPId）(偏移: 0x1C)
- `int s_GameTVPId`（int s_游戏TVPId）(偏移: 0x20)
- `List<SoftMaskable> s_ActiveSoftMaskables`（List<SoftMaskable> s_激活的SoftMaskables）(偏移: 0x24)
- `int[] s_Interactions`（int[] s_Interactions）(偏移: 0x28)
- `bool m_Inverse`（bool m_Inverse）(偏移: 0xC)
- `int m_MaskInteraction`（int m_掩码Interaction）(偏移: 0x10)
- `bool m_UseStencil`（bool m_UseStencil）(偏移: 0x14)
- `bool m_RaycastFilter`（bool m_RaycastFilter）(偏移: 0x15)
- `Graphic _graphic`（Graphic _graphic）(偏移: 0x18)
- `SoftMask _softMask`（Soft掩码 _soft掩码）(偏移: 0x1C)
- `Hash128 _effectMaterialHash`（Hash128 _effect材质Hash）(偏移: 0x20)

### 方法 (14)

- `bool get_inverse()`
  （bool get_inverse（））
- `void set_inverse(bool value)`
  （void set_inverse（bool value））
- `bool get_raycastFilter()`
  （bool get_raycastFilter（））
- `void set_raycastFilter(bool value)`
  （void set_raycastFilter（bool value））
- `bool get_useStencil()`
  （bool get_useStencil（））
- `void set_useStencil(bool value)`
  （void set_useStencil（bool value））
- `Graphic get_graphic()`
  （Graphic get_graphic（））
- `SoftMask get_softMask()`
  （Soft掩码 get_soft掩码（））
- `Material get_modifiedMaterial()`
  （材质 get_modified材质（））
- `void set_modifiedMaterial(Material value)`
  （void set_modified材质（材质 value））
- `void SetMaskInteraction(SpriteMaskInteraction intr)`
  （void 集合掩码Interaction（精灵掩码Interaction intr））
- `void SetMaskInteraction(SpriteMaskInteraction layer0, SpriteMaskInteraction layer1, SpriteMaskInteraction layer2, SpriteMaskInteraction layer3)`
  （void 集合掩码Interaction（精灵掩码Interaction layer0, 精灵掩码Interaction layer1, 精灵掩码Interaction layer2, 精灵掩码Interaction layer3））
- `void OnEnable()`
  （void On启用（））
- `void OnDisable()`
  （void On禁用（））

---

## SolverManager（Solver管理器）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (6)

- `bool fixTransforms`（bool fixTransforms）(偏移: 0xC)
- `Animator animator`（动画器 animator）(偏移: 0x10)
- `Animation legacy`（动画 legacy）(偏移: 0x14)
- `bool updateFrame`（bool updateFrame）(偏移: 0x18)
- `bool componentInitiated`（bool componentInitiated）(偏移: 0x19)
- `bool skipSolverUpdate`（bool skipSolver更新）(偏移: 0x1A)

### 方法 (14)

- `void Disable()`
  （void 禁用（））
- `void InitiateSolver()`
  （void InitiateSolver（））
- `void UpdateSolver()`
  （void 更新Solver（））
- `void FixTransforms()`
  （void FixTransforms（））
- `void OnDisable()`
  （void On禁用（））
- `void Start()`
  （void 开始（））
- `bool get_animatePhysics()`
  （bool get_animate物理（））
- `void Initiate()`
  （void Initiate（））
- `void Update()`
  （void 更新（））
- `void FindAnimatorRecursive(Transform t, bool findInChildren)`
  （void 查找动画器Recursive（变换 t, bool findInChildren））
- `bool get_isAnimated()`
  （bool get_isAnimated（））
- `void FixedUpdate()`
  （void 固定更新（））
- `void LateUpdate()`
  （void 延迟更新（））
- `void UpdateSolverExternal()`
  （void 更新Solver外部的（））

---

## SortKey（Sort键）

### 字段 (4)

- `string source`（string source）(偏移: 0x8)
- `byte[] key`（byte[] key）(偏移: 0xC)
- `CompareOptions options`（CompareOptions options）(偏移: 0x10)
- `int lcid`（int lcid）(偏移: 0x14)

### 方法 (6)

- `int Compare(SortKey sortkey1, SortKey sortkey2)`
  （int Compare（Sort键 sortkey1, Sort键 sortkey2））
- `string get_OriginalString()`
  （string get_Original字符串（））
- `byte[] get_KeyData()`
  （byte[] get_键数据（））
- `bool Equals(object value)`
  （bool Equals（object value））
- `int GetHashCode()`
  （int 获取HashCode（））
- `string ToString()`
  （string To字符串（））

---

## SortKeyBuffer（Sort键缓冲区）

### 字段 (22)

- `byte[] l1b`（byte[] l1b）(偏移: 0x8)
- `byte[] l2b`（byte[] l2b）(偏移: 0xC)
- `byte[] l3b`（byte[] l3b）(偏移: 0x10)
- `byte[] l4sb`（byte[] l4sb）(偏移: 0x14)
- `byte[] l4tb`（byte[] l4tb）(偏移: 0x18)
- `byte[] l4kb`（byte[] l4kb）(偏移: 0x1C)
- `byte[] l4wb`（byte[] l4wb）(偏移: 0x20)
- `byte[] l5b`（byte[] l5b）(偏移: 0x24)
- `string source`（string source）(偏移: 0x28)
- `int l1`（int l1）(偏移: 0x2C)
- `int l2`（int l2）(偏移: 0x30)
- `int l3`（int l3）(偏移: 0x34)
- `int l4s`（int l4s）(偏移: 0x38)
- `int l4t`（int l4t）(偏移: 0x3C)
- `int l4k`（int l4k）(偏移: 0x40)
- `int l4w`（int l4w）(偏移: 0x44)
- `int l5`（int l5）(偏移: 0x48)
- `int lcid`（int lcid）(偏移: 0x4C)
- `CompareOptions options`（CompareOptions options）(偏移: 0x50)
- `bool processLevel2`（bool processLevel2）(偏移: 0x54)
- `bool frenchSort`（bool frenchSort）(偏移: 0x55)
- `bool frenchSorted`（bool frenchSorted）(偏移: 0x56)

### 方法 (10)

- `void Reset()`
  （void 重置（））
- `void Initialize(CompareOptions options, int lcid, string s, bool frenchSort)`
  （void 初始化（CompareOptions options, int lcid, string s, bool frenchSort））
- `void AppendCJKExtension(byte lv1msb, byte lv1lsb)`
  （void AppendCJK扩展（byte lv1msb, byte lv1lsb））
- `void AppendKana(byte category, byte lv1, byte lv2, byte lv3, bool isSmallKana, byte markType, bool isKatakana, bool isHalfWidth)`
  （void AppendKana（byte category, byte lv1, byte lv2, byte lv3, bool isSmallKana, byte markType, bool isKatakana, bool isHalfWidth））
- `void AppendNormal(byte category, byte lv1, byte lv2, byte lv3)`
  （void Append法线（byte category, byte lv1, byte lv2, byte lv3））
- `void AppendLevel5(byte category, byte lv1)`
  （void AppendLevel5（byte category, byte lv1））
- `void AppendBufferPrimitive(byte value, ref byte[] buf, ref int bidx)`
  （void Append缓冲区Primitive（byte value, ref byte[] buf, ref int bidx））
- `SortKey GetResultAndReset()`
  （Sort键 获取ResultAnd重置（））
- `int GetOptimizedLength(byte[] data, int len, byte defaultValue)`
  （int 获取OptimizedLength（byte[] data, int len, byte defaultValue））
- `SortKey GetResult()`
  （Sort键 获取Result（））

---

## SortPrePunctualLight（SortPrePunctual光照）

**继承**: IComparer<DeferredTiler.PrePunctualLight>（IComparer<DeferredTiler.PrePunctualLight>）

### 方法 (1)

- `int Compare(DeferredTiler.PrePunctualLight a, DeferredTiler.PrePunctualLight b)`
  （int Compare（DeferredTiler.PrePunctual光照 a, DeferredTiler.PrePunctual光照 b））

---

## SortVersion（SortVersion）

### 字段 (2)

- `int m_NlsVersion`（int m_NlsVersion）(偏移: 0x8)
- `Guid m_SortId`（Guid m_SortId）(偏移: 0xC)

---

## SortedList（Sorted列表）

**继承**: IDictionary, ICollection, IEnumerable, ICloneable（I字典, ICollection, IEnumerable, ICloneable）

### 字段 (7)

- `object[] keys`（object[] keys）(偏移: 0x8)
- `object[] values`（object[] values）(偏移: 0xC)
- `int _size`（int _size）(偏移: 0x10)
- `int version`（int version）(偏移: 0x14)
- `IComparer comparer`（IComparer comparer）(偏移: 0x18)
- `object _syncRoot`（object _sync根）(偏移: 0x1C)
- `object[] emptyArray`（object[] empty数组）(偏移: 0x0)

### 方法 (20)

- `void Init()`
  （void 初始化（））
- `void Add(object key, object value)`
  （void 添加（object key, object value））
- `int get_Capacity()`
  （int get_Capacity（））
- `void set_Capacity(int value)`
  （void set_Capacity（int value））
- `int get_Count()`
  （int get_数量（））
- `object get_SyncRoot()`
  （object get_同步根（））
- `object Clone()`
  （object 克隆（））
- `bool Contains(object key)`
  （bool Contains（object key））
- `void CopyTo(Array array, int arrayIndex)`
  （void 复制To（数组 array, int arrayIndex））
- `KeyValuePairs[] ToKeyValuePairsArray()`
  （键值Pairs[] To键值Pairs数组（））
- `void EnsureCapacity(int min)`
  （void EnsureCapacity（int min））
- `object GetByIndex(int index)`
  （object 获取By索引（int index））
- `IDictionaryEnumerator GetEnumerator()`
  （I字典Enumerator 获取Enumerator（））
- `object GetKey(int index)`
  （object 获取键（int index））
- `object get_Item(object key)`
  （object get_项目（object key））
- `void set_Item(object key, object value)`
  （void set_项目（object key, object value））
- `int IndexOfKey(object key)`
  （int 索引Of键（object key））
- `void Insert(int index, object key, object value)`
  （void Insert（int index, object key, object value））
- `void RemoveAt(int index)`
  （void 移除At（int index））
- `void Remove(object key)`
  （void 移除（object key））

---

## SortedList.SortedListDebugView（SortedList.Sorted列表Debug视图）

### 字段 (1)

- `SortedList sortedList`（Sorted列表 sorted列表）(偏移: 0x8)

### 方法 (1)

- `KeyValuePairs[] get_Items()`
  （键值Pairs[] get_Items（））

---

## SortedList.SortedListEnumerator（SortedList.Sorted列表Enumerator）

**继承**: IDictionaryEnumerator, IEnumerator, ICloneable（I字典Enumerator, IEnumerator, ICloneable）

### 字段 (9)

- `SortedList sortedList`（Sorted列表 sorted列表）(偏移: 0x8)
- `object key`（object key）(偏移: 0xC)
- `object value`（object value）(偏移: 0x10)
- `int index`（int index）(偏移: 0x14)
- `int startIndex`（int start索引）(偏移: 0x18)
- `int endIndex`（int end索引）(偏移: 0x1C)
- `int version`（int version）(偏移: 0x20)
- `bool current`（bool current）(偏移: 0x24)
- `int getObjectRetType`（int get对象Ret类型）(偏移: 0x28)

### 方法 (7)

- `object Clone()`
  （object 克隆（））
- `object get_Key()`
  （object get_键（））
- `bool MoveNext()`
  （bool 移动下一个（））
- `DictionaryEntry get_Entry()`
  （字典Entry get_Entry（））
- `object get_Current()`
  （object get_当前（））
- `object get_Value()`
  （object get_值（））
- `void Reset()`
  （void 重置（））

---

## SortingCriteria（SortingCriteria）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SortingLayer（Sorting层）

### 字段 (1)

- `int m_Id`（int m_Id）(偏移: 0x0)

### 方法 (6)

- `int get_id()`
  （int get_id（））
- `int get_value()`
  （int get_value（））
- `SortingLayer[] get_layers()`
  （SortingLayer[] get_layers（））
- `int[] GetSortingLayerIDsInternal()`
  （int[] 获取Sorting层IDs内部的（））
- `int GetLayerValueFromID(int id)`
  （int 获取层值FromID（int id））
- `string IDToName(int id)`
  （string IDTo名称（int id））

---

## SortingLayerRange（Sorting层范围）

**继承**: IEquatable<SortingLayerRange>（IEquatable<Sorting层Range>）

### 字段 (2)

- `short m_LowerBound`（short m_下半身Bound）(偏移: 0x0)
- `short m_UpperBound`（short m_上半身Bound）(偏移: 0x2)

### 方法 (4)

- `SortingLayerRange get_all()`
  （Sorting层范围 get_all（））
- `bool Equals(SortingLayerRange other)`
  （bool Equals（Sorting层范围 other））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## SortingSettings（SortingSettings）

**继承**: IEquatable<SortingSettings>（IEquatable<SortingSettings>）

### 字段 (7)

- `Matrix4x4 m_WorldToCameraMatrix`（Matrix4x4 m_世界的To摄像机矩阵）(偏移: 0x0)
- `Vector3 m_CameraPosition`（三维向量 m_摄像机Position）(偏移: 0x40)
- `Vector3 m_CustomAxis`（三维向量 m_自定义的轴）(偏移: 0x4C)
- `SortingCriteria m_Criteria`（SortingCriteria m_Criteria）(偏移: 0x58)
- `DistanceMetric m_DistanceMetric`（距离Metric m_距离Metric）(偏移: 0x5C)
- `Matrix4x4 m_PreviousVPMatrix`（Matrix4x4 m_上一个VP矩阵）(偏移: 0x60)
- `Matrix4x4 m_NonJitteredVPMatrix`（Matrix4x4 m_NonJitteredVP矩阵）(偏移: 0xA0)

### 方法 (7)

- `void set_customAxis(Vector3 value)`
  （void set_custom轴（三维向量 value））
- `SortingCriteria get_criteria()`
  （SortingCriteria get_criteria（））
- `void set_criteria(SortingCriteria value)`
  （void set_criteria（SortingCriteria value））
- `void set_distanceMetric(DistanceMetric value)`
  （void set_distanceMetric（距离Metric value））
- `bool Equals(SortingSettings other)`
  （bool Equals（SortingSettings other））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## SoundManager（音效管理器）

**继承**: Singleton<SoundManager>（Singleton<音效Manager>）

### 字段 (4)

- `GameObject soundObj`（游戏对象 soundObj）(偏移: 0xC)
- `SimpleObjectPool soundPool`（Simple对象池 sound池）(偏移: 0x10)
- `GameObject channelSoundPrefab`（游戏对象 channel音效预制体）(偏移: 0x14)
- `Vector2 CommonSndDistance`（二维向量 CommonSnd距离）(偏移: 0x8)

### 方法 (13)

- `void Awake()`
  （void Awake（））
- `void Play2DSound(string name, int index = -1, bool temp = False)`
  （void Play2D音效（string name, int index = -1, bool temp = False））
- `RecyclableSound Play2DSound(AudioClip audioClip, int priority = 75)`
  （Recyclable音效 Play2D音效（音频弹匣 audioClip, int priority = 75））
- `void PlayNotifySound()`
  （void 播放Notify音效（））
- `void PlayMarkSound()`
  （void 播放Mark音效（））
- `bool TryCreateChannel(string channelName, out ChannelSound sound)`
  （bool Try创建Channel（string channelName, out ChannelSound sound））
- `void Play3DSound(string name, Vector3 worldPos, int index = -1)`
  （void Play3D音效（string name, 三维向量 worldPos, int index = -1））
- `RecyclableSound Play3DSound(string name, Transform parent, int index = -1, int priorityOffset = 0)`
  （Recyclable音效 Play3D音效（string name, 变换 parent, int index = -1, int priorityOffset = 0））
- `void Play3DSound(AudioClip clip, Vector2 distance, Transform parent, int priority = 128)`
  （void Play3D音效（音频弹匣 clip, 二维向量 distance, 变换 parent, int priority = 128））
- `void Play3DSound(AudioClip clip, Vector3 worldPos, int priority = 128)`
  （void Play3D音效（音频弹匣 clip, 三维向量 worldPos, int priority = 128））
- `RecyclableSound GetSound()`
  （Recyclable音效 获取音效（））
- `bool TrySet2dData(RecyclableSound sound, string name, int index = -1)`
  （bool TrySet2d数据（Recyclable音效 sound, string name, int index = -1））
- `bool TrySet3dData(RecyclableSound sound, string name, int index = -1)`
  （bool TrySet3d数据（Recyclable音效 sound, string name, int index = -1））

---

## Space（Space）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SpaceAttribute（SpaceAttribute）

**继承**: PropertyAttribute（属性Attribute）

### 字段 (1)

- `float height`（float height）(偏移: 0x8)

---

## SpawnOverDistance（出生Over距离）

**继承**: VFXSpawnerCallbacks（VFXSpawnerCallbacks）

### 字段 (7)

- `Vector3 m_OldPosition`（三维向量 m_旧的Position）(偏移: 0xC)
- `int positionPropertyId`（int position属性Id）(偏移: 0x0)
- `int ratePerUnitPropertyId`（int ratePerUnit属性Id）(偏移: 0x4)
- `int velocityThresholdPropertyId`（int velocityThreshold属性Id）(偏移: 0x8)
- `int clampToOnePropertyId`（int clampToOne属性Id）(偏移: 0xC)
- `int positionAttributeId`（int positionAttributeId）(偏移: 0x10)
- `int oldPositionAttributeId`（int oldPositionAttributeId）(偏移: 0x14)

---

## SpawnOverDistance.InputProperties（出生OverDistance.输入Properties）

### 字段 (4)

- `Vector3 Position`（三维向量 Position）(偏移: 0x8)
- `float RatePerUnit`（float RatePerUnit）(偏移: 0x14)
- `float VelocityThreshold`（float 速度Threshold）(偏移: 0x18)
- `bool ClampToOne`（bool ClampToOne）(偏移: 0x1C)

---

## SpawnPoint（出生Point）

### 字段 (2)

- `Vector3 position`（三维向量 position）(偏移: 0x0)
- `float rotaion`（float rotaion）(偏移: 0xC)

---

## SpawnPointArray（出生Point数组）

### 字段 (1)

- `SpawnPoint[] points`（出生Point[] points）(偏移: 0x8)

---

## SpecialKillType（特殊击杀类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SpecialPluginsUtils（特殊PluginsUtils）

### 方法 (4)

- `bool SetLookAt(TweenerCore<Quaternion, Vector3, QuaternionOptions> t)`
  （bool 集合LookAt（TweenerCore<Quaternion, 三维向量, QuaternionOptions> t））
- `bool SetPunch(TweenerCore<Vector3, Vector3[], Vector3ArrayOptions> t)`
  （bool 集合Punch（TweenerCore<三维向量, Vector3[], 三维向量数组Options> t））
- `bool SetShake(TweenerCore<Vector3, Vector3[], Vector3ArrayOptions> t)`
  （bool 集合震动（TweenerCore<三维向量, Vector3[], 三维向量数组Options> t））
- `bool SetCameraShakePosition(TweenerCore<Vector3, Vector3[], Vector3ArrayOptions> t)`
  （bool 集合摄像机震动Position（TweenerCore<三维向量, Vector3[], 三维向量数组Options> t））

---

## SpecialStartupMode（特殊Startup模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SpeechError（SpeechError）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SpeechSystemStatus（Speech系统Status）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SpeedBuff（Speed增益）

**继承**: Buff（增益）

### 字段 (1)

- `float moveSpeedPenalty`（float moveSpeed惩罚）(偏移: 0x24)

### 方法 (2)

- `void SpeedPenaltyBuffUpdate(ref float speedUp, ref float speedDown)`
  （void Speed惩罚增益更新（ref float speedUp, ref float speedDown））
- `void OnLifeEnd()`
  （void OnLife结束（））

---

## SpeedHackDetector（SpeedHackDetector）

**继承**: ACTkDetectorBase（ACTkDetector基础）

### 字段 (11)

- `int instancesInScene`（int instancesIn场景）(偏移: 0x0)
- `float interval`（float interval）(偏移: 0x1C)
- `byte maxFalsePositives`（byte maxFalsePositives）(偏移: 0x20)
- `int coolDown`（int cool下）(偏移: 0x24)
- `byte currentFalsePositives`（byte currentFalsePositives）(偏移: 0x28)
- `int currentCooldownShots`（int currentCooldownShots）(偏移: 0x2C)
- `long ticksOnStart`（long ticksOn开始）(偏移: 0x30)
- `long vulnerableTicksOnStart`（long vulnerableTicksOn开始）(偏移: 0x38)
- `long previousTicks`（long previousTicks）(偏移: 0x40)
- `long previousIntervalTicks`（long previous间隔Ticks）(偏移: 0x48)
- `float vulnerableTimeOnStart`（float vulnerable时间On开始）(偏移: 0x50)

### 方法 (21)

- `SpeedHackDetector AddToSceneOrGetExisting()`
  （SpeedHackDetector 添加To场景Or获取Existing（））
- `void StartDetection()`
  （void 开始Detection（））
- `void StartDetection(Action callback)`
  （void 开始Detection（动作 callback））
- `void StartDetection(Action callback, float interval)`
  （void 开始Detection（动作 callback, float interval））
- `void StartDetection(Action callback, float interval, byte maxFalsePositives)`
  （void 开始Detection（动作 callback, float interval, byte maxFalsePositives））
- `void StartDetection(Action callback, float interval, byte maxFalsePositives, int coolDown)`
  （void 开始Detection（动作 callback, float interval, byte maxFalsePositives, int coolDown））
- `void StopDetection()`
  （void 停止Detection（））
- `void Dispose()`
  （void 释放（））
- `SpeedHackDetector get_Instance()`
  （SpeedHackDetector get_实例（））
- `void set_Instance(SpeedHackDetector value)`
  （void set_实例（SpeedHackDetector value））
- `SpeedHackDetector get_GetOrCreateInstance()`
  （SpeedHackDetector get_获取Or创建实例（））
- `void Awake()`
  （void Awake（））
- `void OnDestroy()`
  （void On销毁（））
- `void OnLevelWasLoadedNew(Scene scene, LoadSceneMode mode)`
  （void On等级WasLoaded新的（场景 scene, 加载场景模式 mode））
- `void OnApplicationPause(bool pause)`
  （void OnApplication暂停（bool pause））
- `void Update()`
  （void 更新（））
- `void StartDetectionInternal(Action callback, float checkInterval, byte falsePositives, int shotsTillCooldown)`
  （void 开始Detection内部的（动作 callback, float checkInterval, byte falsePositives, int shotsTillCooldown））
- `void StartDetectionAutomatically()`
  （void 开始DetectionAutomatically（））
- `void DisposeInternal()`
  （void 释放内部的（））
- `void ResetStartTicks()`
  （void 重置开始Ticks（））
- `long GetReliableTicks()`
  （long 获取ReliableTicks（））

---

## SpeedUp（Speed上）

**继承**: BotSkillBase（机器人技能基础）

### 方法 (1)

- `bool CanDo()`
  （bool 能否Do（））

---

## SphereCollider（Sphere碰撞器）

**继承**: Collider（碰撞器）

### 方法 (4)

- `Vector3 get_center()`
  （三维向量 get_center（））
- `float get_radius()`
  （float get_radius（））
- `void set_radius(float value)`
  （void set_radius（float value））
- `void get_center_Injected(out Vector3 ret)`
  （void get_center_Injected（out Vector3 ret））

---

## SphericalHarmonicsL2（SphericalHarmonicsL2）

**继承**: IEquatable<SphericalHarmonicsL2>（IEquatable<SphericalHarmonicsL2>）

### 字段 (27)

- `float shr0`（float shr0）(偏移: 0x0)
- `float shr1`（float shr1）(偏移: 0x4)
- `float shr2`（float shr2）(偏移: 0x8)
- `float shr3`（float shr3）(偏移: 0xC)
- `float shr4`（float shr4）(偏移: 0x10)
- `float shr5`（float shr5）(偏移: 0x14)
- `float shr6`（float shr6）(偏移: 0x18)
- `float shr7`（float shr7）(偏移: 0x1C)
- `float shr8`（float shr8）(偏移: 0x20)
- `float shg0`（float shg0）(偏移: 0x24)
- `float shg1`（float shg1）(偏移: 0x28)
- `float shg2`（float shg2）(偏移: 0x2C)
- `float shg3`（float shg3）(偏移: 0x30)
- `float shg4`（float shg4）(偏移: 0x34)
- `float shg5`（float shg5）(偏移: 0x38)
- `float shg6`（float shg6）(偏移: 0x3C)
- `float shg7`（float shg7）(偏移: 0x40)
- `float shg8`（float shg8）(偏移: 0x44)
- `float shb0`（float shb0）(偏移: 0x48)
- `float shb1`（float shb1）(偏移: 0x4C)
- `float shb2`（float shb2）(偏移: 0x50)
- `float shb3`（float shb3）(偏移: 0x54)
- `float shb4`（float shb4）(偏移: 0x58)
- `float shb5`（float shb5）(偏移: 0x5C)
- `float shb6`（float shb6）(偏移: 0x60)
- `float shb7`（float shb7）(偏移: 0x64)
- `float shb8`（float shb8）(偏移: 0x68)

### 方法 (5)

- `float get_Item(int rgb, int coefficient)`
  （float get_项目（int rgb, int coefficient））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool Equals(object other)`
  （bool Equals（object other））
- `bool Equals(SphericalHarmonicsL2 other)`
  （bool Equals（SphericalHarmonicsL2 other））
- `bool op_Equality(SphericalHarmonicsL2 lhs, SphericalHarmonicsL2 rhs)`
  （bool op_Equality（SphericalHarmonicsL2 lhs, SphericalHarmonicsL2 rhs））

---

## SpinLock（SpinLock）

### 字段 (2)

- `int m_owner`（int m_owner）(偏移: 0x0)
- `int MAXIMUM_WAITERS`（int MAXIMUM_WAITERS）(偏移: 0x0)

### 方法 (10)

- `void Enter(ref bool lockTaken)`
  （void Enter（ref bool lockTaken））
- `void TryEnter(int millisecondsTimeout, ref bool lockTaken)`
  （void TryEnter（int millisecondsTimeout, ref bool lockTaken））
- `void ContinueTryEnter(int millisecondsTimeout, ref bool lockTaken)`
  （void ContinueTryEnter（int millisecondsTimeout, ref bool lockTaken））
- `void DecrementWaiters()`
  （void DecrementWaiters（））
- `void ContinueTryEnterWithThreadTracking(int millisecondsTimeout, uint startTime, ref bool lockTaken)`
  （void ContinueTryEnterWithThreadTracking（int millisecondsTimeout, uint startTime, ref bool lockTaken））
- `void Exit(bool useMemoryBarrier)`
  （void Exit（bool useMemoryBarrier））
- `void ExitSlowPath(bool useMemoryBarrier)`
  （void ExitSlow路径（bool useMemoryBarrier））
- `bool get_IsHeld()`
  （bool get_是否Held（））
- `bool get_IsHeldByCurrentThread()`
  （bool get_是否HeldBy当前Thread（））
- `bool get_IsThreadOwnerTrackingEnabled()`
  （bool get_是否ThreadOwnerTracking启用的（））

---

## SpinLock.SystemThreading_SpinLockDebugView（SpinLock.系统Threading_SpinLockDebug视图）

### 字段 (1)

- `SpinLock m_spinLock`（SpinLock m_spinLock）(偏移: 0x8)

### 方法 (3)

- `Nullable<bool> get_IsHeldByCurrentThread()`
  （Nullable<bool> get_是否HeldBy当前Thread（））
- `Nullable<int> get_OwnerThreadID()`
  （Nullable<int> get_OwnerThreadID（））
- `bool get_IsHeld()`
  （bool get_是否Held（））

---

## SpinWait（SpinWait）

### 字段 (1)

- `int m_count`（int m_count）(偏移: 0x0)

### 方法 (2)

- `bool get_NextSpinWillYield()`
  （bool get_下一个SpinWillYield（））
- `void SpinOnce()`
  （void SpinOnce（））

---

## SplineHelpers（SplineHelpers）

### 方法 (6)

- `Vector3 Bezier3(float t, Vector3 p0, Vector3 p1, Vector3 p2, Vector3 p3)`
  （三维向量 Bezier3（float t, 三维向量 p0, 三维向量 p1, 三维向量 p2, 三维向量 p3））
- `Vector3 BezierTangent3(float t, Vector3 p0, Vector3 p1, Vector3 p2, Vector3 p3)`
  （三维向量 BezierTangent3（float t, 三维向量 p0, 三维向量 p1, 三维向量 p2, 三维向量 p3））
- `float Bezier1(float t, float p0, float p1, float p2, float p3)`
  （float Bezier1（float t, float p0, float p1, float p2, float p3））
- `float BezierTangent1(float t, float p0, float p1, float p2, float p3)`
  （float BezierTangent1（float t, float p0, float p1, float p2, float p3））
- `void ComputeSmoothControlPoints(ref Vector4[] knot, ref Vector4[] ctrl1, ref Vector4[] ctrl2)`
  （void ComputeSmooth控制Points（ref Vector4[] knot, ref Vector4[] ctrl1, ref Vector4[] ctrl2））
- `void ComputeSmoothControlPointsLooped(ref Vector4[] knot, ref Vector4[] ctrl1, ref Vector4[] ctrl2)`
  （void ComputeSmooth控制PointsLooped（ref Vector4[] knot, ref Vector4[] ctrl1, ref Vector4[] ctrl2））

---

## SplitToning（SplitToning）

**继承**: VolumeComponent, IPostProcessComponent（Volume组件, IPost处理组件）

### 字段 (3)

- `ColorParameter shadows`（颜色Parameter shadows）(偏移: 0x1C)
- `ColorParameter highlights`（颜色Parameter highlights）(偏移: 0x20)
- `ClampedFloatParameter balance`（Clamped浮点数Parameter balance）(偏移: 0x24)

### 方法 (2)

- `bool IsActive()`
  （bool 是否激活的（））
- `bool IsTileCompatible()`
  （bool 是否TileCompatible（））

---

## SpookyHash（SpookyHash）

### 字段 (1)

- `bool AllowUnalignedRead`（bool 允许UnalignedRead）(偏移: 0x0)

### 方法 (10)

- `bool AttemptDetectAllowUnalignedRead()`
  （bool AttemptDetect允许UnalignedRead（））
- `void Hash(void* message, ulong length, ulong* hash1, ulong* hash2)`
  （void Hash（void* message, ulong length, ulong* hash1, ulong* hash2））
- `void End(ulong* data, ref ulong h0, ref ulong h1, ref ulong h2, ref ulong h3, ref ulong h4, ref ulong h5, ref ulong h6, ref ulong h7, ref ulong h8, ref ulong h9, ref ulong h10, ref ulong h11)`
  （void 结束（ulong* data, ref ulong h0, ref ulong h1, ref ulong h2, ref ulong h3, ref ulong h4, ref ulong h5, ref ulong h6, ref ulong h7, ref ulong h8, ref ulong h9, ref ulong h10, ref ulong h11））
- `void EndPartial(ref ulong h0, ref ulong h1, ref ulong h2, ref ulong h3, ref ulong h4, ref ulong h5, ref ulong h6, ref ulong h7, ref ulong h8, ref ulong h9, ref ulong h10, ref ulong h11)`
  （void 结束Partial（ref ulong h0, ref ulong h1, ref ulong h2, ref ulong h3, ref ulong h4, ref ulong h5, ref ulong h6, ref ulong h7, ref ulong h8, ref ulong h9, ref ulong h10, ref ulong h11））
- `void Rot64(ref ulong x, int k)`
  （void Rot64（ref ulong x, int k））
- `void Short(void* message, ulong length, ulong* hash1, ulong* hash2)`
  （void Short（void* message, ulong length, ulong* hash1, ulong* hash2））
- `void ShortMix(ref ulong h0, ref ulong h1, ref ulong h2, ref ulong h3)`
  （void ShortMix（ref ulong h0, ref ulong h1, ref ulong h2, ref ulong h3））
- `void ShortEnd(ref ulong h0, ref ulong h1, ref ulong h2, ref ulong h3)`
  （void Short结束（ref ulong h0, ref ulong h1, ref ulong h2, ref ulong h3））
- `void Mix(ulong* data, ref ulong s0, ref ulong s1, ref ulong s2, ref ulong s3, ref ulong s4, ref ulong s5, ref ulong s6, ref ulong s7, ref ulong s8, ref ulong s9, ref ulong s10, ref ulong s11)`
  （void Mix（ulong* data, ref ulong s0, ref ulong s1, ref ulong s2, ref ulong s3, ref ulong s4, ref ulong s5, ref ulong s6, ref ulong s7, ref ulong s8, ref ulong s9, ref ulong s10, ref ulong s11））
- `void memset(void* dst, int value, ulong numberOfBytes)`
  （void memset（void* dst, int value, ulong numberOfBytes））

---

## SpookyHash.U（SpookyHash.U）

### 字段 (4)

- `byte* p8`（byte* p8）(偏移: 0x0)
- `uint* p32`（uint* p32）(偏移: 0x0)
- `ulong* p64`（ulong* p64）(偏移: 0x0)
- `ulong i`（ulong i）(偏移: 0x0)

---

## SpotLight（Spot光照）

### 字段 (13)

- `int instanceID`（int instanceID）(偏移: 0x0)
- `bool shadow`（bool shadow）(偏移: 0x4)
- `LightMode mode`（光照模式 mode）(偏移: 0x5)
- `Vector3 position`（三维向量 position）(偏移: 0x8)
- `Quaternion orientation`（Quaternion orientation）(偏移: 0x14)
- `LinearColor color`（Linear颜色 color）(偏移: 0x24)
- `LinearColor indirectColor`（Linear颜色 indirect颜色）(偏移: 0x34)
- `float range`（float range）(偏移: 0x44)
- `float sphereRadius`（float sphereRadius）(偏移: 0x48)
- `float coneAngle`（float cone角度）(偏移: 0x4C)
- `float innerConeAngle`（float innerCone角度）(偏移: 0x50)
- `FalloffType falloff`（Falloff类型 falloff）(偏移: 0x54)
- `AngularFalloffType angularFalloff`（AngularFalloff类型 angularFalloff）(偏移: 0x55)

---

## Sprite（精灵）

**继承**: Object（对象）

### 方法 (36)

- `int GetPackingMode()`
  （int 获取Packing模式（））
- `int GetPacked()`
  （int 获取Packed（））
- `Rect GetTextureRect()`
  （Rect 获取纹理Rect（））
- `Vector4 GetInnerUVs()`
  （Vector4 获取InnerUVs（））
- `Vector4 GetOuterUVs()`
  （Vector4 获取OuterUVs（））
- `Vector4 GetPadding()`
  （Vector4 获取Padding（））
- `Sprite CreateSprite(Texture2D texture, Rect rect, Vector2 pivot, float pixelsPerUnit, uint extrude, SpriteMeshType meshType, Vector4 border, bool generateFallbackPhysicsShape)`
  （精灵 创建精灵（Texture2D texture, Rect rect, 二维向量 pivot, float pixelsPerUnit, uint extrude, 精灵网格类型 meshType, Vector4 border, bool generateFallbackPhysicsShape））
- `Bounds get_bounds()`
  （Bounds get_bounds（））
- `Rect get_rect()`
  （Rect get_rect（））
- `Vector4 get_border()`
  （Vector4 get_border（））
- `Texture2D get_texture()`
  （Texture2D get_texture（））
- `float get_pixelsPerUnit()`
  （float get_pixelsPerUnit（））
- `Texture2D get_associatedAlphaSplitTexture()`
  （Texture2D get_associated透明度Split纹理（））
- `Vector2 get_pivot()`
  （二维向量 get_pivot（））
- `bool get_isUsingPlaceholder()`
  （bool get_isUsingPlaceholder（））
- `bool get_packed()`
  （bool get_packed（））
- `SpritePackingMode get_packingMode()`
  （精灵Packing模式 get_packing模式（））
- `Rect get_textureRect()`
  （Rect get_textureRect（））
- `Vector2[] get_vertices()`
  （Vector2[] get_vertices（））
- `ushort[] get_triangles()`
  （ushort[] get_triangles（））
- `Vector2[] get_uv()`
  （Vector2[] get_uv（））
- `Sprite Create(Texture2D texture, Rect rect, Vector2 pivot, float pixelsPerUnit, uint extrude, SpriteMeshType meshType, Vector4 border, bool generateFallbackPhysicsShape)`
  （精灵 创建（Texture2D texture, Rect rect, 二维向量 pivot, float pixelsPerUnit, uint extrude, 精灵网格类型 meshType, Vector4 border, bool generateFallbackPhysicsShape））
- `Sprite Create(Texture2D texture, Rect rect, Vector2 pivot, float pixelsPerUnit, uint extrude, SpriteMeshType meshType, Vector4 border)`
  （精灵 创建（Texture2D texture, Rect rect, 二维向量 pivot, float pixelsPerUnit, uint extrude, 精灵网格类型 meshType, Vector4 border））
- `Sprite Create(Texture2D texture, Rect rect, Vector2 pivot, float pixelsPerUnit, uint extrude, SpriteMeshType meshType)`
  （精灵 创建（Texture2D texture, Rect rect, 二维向量 pivot, float pixelsPerUnit, uint extrude, 精灵网格类型 meshType））
- `Sprite Create(Texture2D texture, Rect rect, Vector2 pivot, float pixelsPerUnit, uint extrude)`
  （精灵 创建（Texture2D texture, Rect rect, 二维向量 pivot, float pixelsPerUnit, uint extrude））
- `Sprite Create(Texture2D texture, Rect rect, Vector2 pivot, float pixelsPerUnit)`
  （精灵 创建（Texture2D texture, Rect rect, 二维向量 pivot, float pixelsPerUnit））
- `Sprite Create(Texture2D texture, Rect rect, Vector2 pivot)`
  （精灵 创建（Texture2D texture, Rect rect, 二维向量 pivot））
- `void GetTextureRect_Injected(out Rect ret)`
  （void 获取纹理Rect_Injected（out Rect ret））
- `void GetInnerUVs_Injected(out Vector4 ret)`
  （void 获取InnerUVs_Injected（out Vector4 ret））
- `void GetOuterUVs_Injected(out Vector4 ret)`
  （void 获取OuterUVs_Injected（out Vector4 ret））
- `void GetPadding_Injected(out Vector4 ret)`
  （void 获取Padding_Injected（out Vector4 ret））
- `Sprite CreateSprite_Injected(Texture2D texture, ref Rect rect, ref Vector2 pivot, float pixelsPerUnit, uint extrude, SpriteMeshType meshType, ref Vector4 border, bool generateFallbackPhysicsShape)`
  （精灵 创建Sprite_Injected（Texture2D texture, ref Rect rect, ref Vector2 pivot, float pixelsPerUnit, uint extrude, 精灵网格类型 meshType, ref Vector4 border, bool generateFallbackPhysicsShape））
- `void get_bounds_Injected(out Bounds ret)`
  （void get_bounds_Injected（out Bounds ret））
- `void get_rect_Injected(out Rect ret)`
  （void get_rect_Injected（out Rect ret））
- `void get_border_Injected(out Vector4 ret)`
  （void get_border_Injected（out Vector4 ret））
- `void get_pivot_Injected(out Vector2 ret)`
  （void get_pivot_Injected（out Vector2 ret））

---

## SpriteAtlas（精灵Atlas）

**继承**: Object（对象）

### 方法 (2)

- `bool CanBindTo(Sprite sprite)`
  （bool 能否BindTo（精灵 sprite））
- `bool IsPlaceholder()`
  （bool 是否Placeholder（））

---

## SpriteAtlasManager（精灵Atlas管理器）

### 字段 (1)

- `Action<SpriteAtlas> atlasRegistered`（Action<精灵Atlas> atlasRegistered）(偏移: 0x4)

### 方法 (5)

- `bool RequestAtlas(string tag)`
  （bool 请求Atlas（string tag））
- `void add_atlasRegistered(Action<SpriteAtlas> value)`
  （void add_atlasRegistered（Action<精灵Atlas> value））
- `void remove_atlasRegistered(Action<SpriteAtlas> value)`
  （void remove_atlasRegistered（Action<精灵Atlas> value））
- `void PostRegisteredAtlas(SpriteAtlas spriteAtlas)`
  （void PostRegisteredAtlas（精灵Atlas spriteAtlas））
- `void Register(SpriteAtlas spriteAtlas)`
  （void Register（精灵Atlas spriteAtlas））

---

## SpriteBone（精灵Bone）

### 字段 (5)

- `string m_Name`（string m_名称）(偏移: 0x0)
- `Vector3 m_Position`（三维向量 m_Position）(偏移: 0x4)
- `Quaternion m_Rotation`（Quaternion m_Rotation）(偏移: 0x10)
- `float m_Length`（float m_Length）(偏移: 0x20)
- `int m_ParentId`（int m_父级Id）(偏移: 0x24)

---

## SpriteChannelInfo（精灵Channel信息）

### 字段 (4)

- `IntPtr m_Buffer`（整数Ptr m_缓冲区）(偏移: 0x0)
- `int m_Count`（int m_数量）(偏移: 0x4)
- `int m_Offset`（int m_Offset）(偏移: 0x8)
- `int m_Stride`（int m_Stride）(偏移: 0xC)

### 方法 (4)

- `void* get_buffer()`
  （void* get_buffer（））
- `int get_count()`
  （int get_count（））
- `int get_offset()`
  （int get_offset（））
- `int get_stride()`
  （int get_stride（））

---

## SpriteDataAccessExtensions（精灵数据AccessExtensions）

### 方法 (5)

- `NativeArray<ushort> GetIndices(Sprite sprite)`
  （NativeArray<ushort> 获取Indices（精灵 sprite））
- `SpriteChannelInfo GetIndicesInfo(Sprite sprite)`
  （精灵Channel信息 获取Indices信息（精灵 sprite））
- `SpriteChannelInfo GetChannelInfo(Sprite sprite, VertexAttribute channel)`
  （精灵Channel信息 获取Channel信息（精灵 sprite, VertexAttribute channel））
- `void GetIndicesInfo_Injected(Sprite sprite, out SpriteChannelInfo ret)`
  （void 获取IndicesInfo_Injected（精灵 sprite, out SpriteChannelInfo ret））
- `void GetChannelInfo_Injected(Sprite sprite, VertexAttribute channel, out SpriteChannelInfo ret)`
  （void 获取ChannelInfo_Injected（精灵 sprite, VertexAttribute channel, out SpriteChannelInfo ret））

---

## SpriteIntermediateRendererInfo（精灵Intermediate渲染器信息）

### 字段 (15)

- `int SpriteID`（int 精灵ID）(偏移: 0x0)
- `int TextureID`（int 纹理ID）(偏移: 0x4)
- `int MaterialID`（int 材质ID）(偏移: 0x8)
- `Color Color`（颜色 颜色）(偏移: 0xC)
- `Matrix4x4 Transform`（Matrix4x4 变换）(偏移: 0x1C)
- `Bounds Bounds`（Bounds Bounds）(偏移: 0x5C)
- `int Layer`（int 层）(偏移: 0x74)
- `int SortingLayer`（int Sorting层）(偏移: 0x78)
- `int SortingOrder`（int SortingOrder）(偏移: 0x7C)
- `ulong SceneCullingMask`（ulong 场景Culling掩码）(偏移: 0x80)
- `IntPtr IndexData`（整数Ptr 索引数据）(偏移: 0x88)
- `IntPtr VertexData`（整数Ptr Vertex数据）(偏移: 0x8C)
- `int IndexCount`（int 索引数量）(偏移: 0x90)
- `int VertexCount`（int Vertex数量）(偏移: 0x94)
- `int ShaderChannelMask`（int 着色器Channel掩码）(偏移: 0x98)

---

## SpriteMaskInteraction（精灵掩码Interaction）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SpriteMeshType（精灵网格类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SpritePackingMode（精灵Packing模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## SpriteRenderer（精灵渲染器）

**继承**: Renderer（渲染器）

### 方法 (4)

- `Color get_color()`
  （颜色 get_color（））
- `void set_color(Color value)`
  （void set_color（颜色 value））
- `void get_color_Injected(out Color ret)`
  （void get_color_Injected（out Color ret））
- `void set_color_Injected(ref Color value)`
  （void set_color_Injected（ref Color value））

---

## SpriteState（精灵状态）

**继承**: IEquatable<SpriteState>（IEquatable<精灵State>）

### 字段 (4)

- `Sprite m_HighlightedSprite`（精灵 m_Highlighted精灵）(偏移: 0x0)
- `Sprite m_PressedSprite`（精灵 m_按下的精灵）(偏移: 0x4)
- `Sprite m_SelectedSprite`（精灵 m_选中的精灵）(偏移: 0x8)
- `Sprite m_DisabledSprite`（精灵 m_禁用的精灵）(偏移: 0xC)

### 方法 (9)

- `Sprite get_highlightedSprite()`
  （精灵 get_highlighted精灵（））
- `void set_highlightedSprite(Sprite value)`
  （void set_highlighted精灵（精灵 value））
- `Sprite get_pressedSprite()`
  （精灵 get_pressed精灵（））
- `void set_pressedSprite(Sprite value)`
  （void set_pressed精灵（精灵 value））
- `Sprite get_selectedSprite()`
  （精灵 get_selected精灵（））
- `void set_selectedSprite(Sprite value)`
  （void set_selected精灵（精灵 value））
- `Sprite get_disabledSprite()`
  （精灵 get_disabled精灵（））
- `void set_disabledSprite(Sprite value)`
  （void set_disabled精灵（精灵 value））
- `bool Equals(SpriteState other)`
  （bool Equals（精灵状态 other））

---

## Stack（栈）

**继承**: ICollection, IEnumerable, ICloneable（ICollection, IEnumerable, ICloneable）

### 字段 (4)

- `object[] _array`（object[] _array）(偏移: 0x8)
- `int _size`（int _size）(偏移: 0xC)
- `int _version`（int _version）(偏移: 0x10)
- `object _syncRoot`（object _sync根）(偏移: 0x14)

### 方法 (10)

- `int get_Count()`
  （int get_数量（））
- `object get_SyncRoot()`
  （object get_同步根（））
- `void Clear()`
  （void 清除（））
- `object Clone()`
  （object 克隆（））
- `void CopyTo(Array array, int index)`
  （void 复制To（数组 array, int index））
- `IEnumerator GetEnumerator()`
  （IEnumerator 获取Enumerator（））
- `object Peek()`
  （object Peek（））
- `object Pop()`
  （object Pop（））
- `void Push(object obj)`
  （void Push（object obj））
- `object[] ToArray()`
  （object[] To数组（））

---

## Stack.StackDebugView（Stack.栈Debug视图）

### 字段 (1)

- `Stack stack`（栈 stack）(偏移: 0x8)

### 方法 (1)

- `object[] get_Items()`
  （object[] get_Items（））

---

## Stack.StackEnumerator（Stack.栈Enumerator）

**继承**: IEnumerator, ICloneable（IEnumerator, ICloneable）

### 字段 (4)

- `Stack _stack`（栈 _stack）(偏移: 0x8)
- `int _index`（int _index）(偏移: 0xC)
- `int _version`（int _version）(偏移: 0x10)
- `object currentElement`（object current元素）(偏移: 0x14)

### 方法 (4)

- `object Clone()`
  （object 克隆（））
- `bool MoveNext()`
  （bool 移动下一个（））
- `object get_Current()`
  （object get_当前（））
- `void Reset()`
  （void 重置（））

---

## StackBuilderSink（栈构建器Sink）

**继承**: IMessageSink（IMessageSink）

### 字段 (2)

- `MarshalByRefObject _target`（MarshalByRef对象 _target）(偏移: 0x8)
- `RealProxy _rp`（Real代理 _rp）(偏移: 0xC)

### 方法 (4)

- `IMessage SyncProcessMessage(IMessage msg)`
  （IMessage 同步处理Message（IMessage msg））
- `IMessageCtrl AsyncProcessMessage(IMessage msg, IMessageSink replySink)`
  （IMessageCtrl 异步处理Message（IMessage msg, IMessageSink replySink））
- `void ExecuteAsyncMessage(object ob)`
  （void 执行异步Message（object ob））
- `void CheckParameters(IMessage msg)`
  （void 检查Parameters（IMessage msg））

---

## StackCrawlMark（栈CrawlMark）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## StackFrame（栈Frame）

### 字段 (9)

- `int ilOffset`（int ilOffset）(偏移: 0x8)
- `int nativeOffset`（int nativeOffset）(偏移: 0xC)
- `long methodAddress`（long methodAddress）(偏移: 0x10)
- `uint methodIndex`（uint method索引）(偏移: 0x18)
- `MethodBase methodBase`（Method基础 method基础）(偏移: 0x1C)
- `string fileName`（string file名称）(偏移: 0x20)
- `int lineNumber`（int lineNumber）(偏移: 0x24)
- `int columnNumber`（int columnNumber）(偏移: 0x28)
- `string internalMethodName`（string internalMethod名称）(偏移: 0x2C)

### 方法 (11)

- `bool get_frame_info(int skip, bool needFileInfo, out MethodBase method, out int iloffset, out int native_offset, out string file, out int line, out int column)`
  （bool get_frame_info（int skip, bool needFileInfo, out MethodBase method, out int iloffset, out int native_offset, out string file, out int line, out int column））
- `int GetFileLineNumber()`
  （int 获取文件LineNumber（））
- `string GetFileName()`
  （string 获取文件名称（））
- `string GetSecureFileName()`
  （string 获取Secure文件名称（））
- `int GetILOffset()`
  （int 获取ILOffset（））
- `MethodBase GetMethod()`
  （Method基础 获取Method（））
- `int GetNativeOffset()`
  （int 获取NativeOffset（））
- `long GetMethodAddress()`
  （long 获取MethodAddress（））
- `uint GetMethodIndex()`
  （uint 获取Method索引（））
- `string GetInternalMethodName()`
  （string 获取内部的Method名称（））
- `string ToString()`
  （string To字符串（））

---

## StackGuard（栈Guard）

### 字段 (1)

- `int m_inliningDepth`（int m_inlining深度）(偏移: 0x8)

### 方法 (3)

- `bool TryBeginInliningScope()`
  （bool TryBeginInlining瞄准镜（））
- `void EndInliningScope()`
  （void 结束Inlining瞄准镜（））
- `bool CheckForSufficientStack()`
  （bool 检查ForSufficient栈（））

---

## StackTrace（栈Trace）

### 字段 (5)

- `StackFrame[] frames`（栈Frame[] frames）(偏移: 0x8)
- `StackTrace[] captured_traces`（栈Trace[] captured_traces）(偏移: 0xC)
- `bool debug_info`（bool debug_info）(偏移: 0x10)
- `bool isAotidSet`（bool isAotid集合）(偏移: 0x0)
- `string aotid`（string aotid）(偏移: 0x4)

### 方法 (9)

- `void init_frames(int skipFrames, bool fNeedFileInfo)`
  （void init_frames（int skipFrames, bool fNeedFileInfo））
- `StackFrame[] get_trace(Exception e, int skipFrames, bool fNeedFileInfo)`
  （栈Frame[] get_trace（Exception e, int skipFrames, bool fNeedFileInfo））
- `int get_FrameCount()`
  （int get_Frame数量（））
- `StackFrame GetFrame(int index)`
  （栈Frame 获取Frame（int index））
- `string GetAotId()`
  （string 获取AotId（））
- `bool AddFrames(StringBuilder sb)`
  （bool 添加Frames（字符串构建器 sb））
- `void GetFullNameForStackTrace(StringBuilder sb, MethodBase mi)`
  （void 获取满名称For栈Trace（字符串构建器 sb, Method基础 mi））
- `string ToString()`
  （string To字符串（））
- `string ToString(StackTrace.TraceFormat traceFormat)`
  （string To字符串（栈Trace.Trace格式化 traceFormat））

---

## StackTrace.TraceFormat（栈Trace.Trace格式化）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## StackTraceUtility（栈Trace工具）

### 字段 (1)

- `string projectFolder`（string projectFolder）(偏移: 0x0)

### 方法 (4)

- `void SetProjectFolder(string folder)`
  （void 集合ProjectFolder（string folder））
- `string ExtractStackTrace()`
  （string Extract栈Trace（））
- `void ExtractStringFromExceptionInternal(object exceptiono, out string message, out string stackTrace)`
  （void Extract字符串FromException内部的（object exceptiono, out string message, out string stackTrace））
- `string ExtractFormattedStackTrace(StackTrace stackTrace)`
  （string ExtractFormatted栈Trace（栈Trace stackTrace））

---

## StageRuntimeInterface（StageRuntimeInterface）

### 字段 (3)

- `Func<Camera> m_GetCamera`（Func<Camera> m_获取摄像机）(偏移: 0xC)
- `Func<Light> m_GetSunLight`（Func<Light> m_获取Sun光照）(偏移: 0x10)
- `object SRPData`（object SRP数据）(偏移: 0x14)

### 方法 (3)

- `GameObject AddGameObject(bool persistent = False)`
  （游戏对象 添加游戏对象（bool persistent = False））
- `Camera get_camera()`
  （摄像机 get_camera（））
- `Light get_sunLight()`
  （光照 get_sun光照（））

---

## StandaloneInputModule（Standalone输入模块）

**继承**: PointerInputModule（指针输入模块）

### 字段 (14)

- `float m_PrevActionTime`（float m_Prev动作时间）(偏移: 0x2C)
- `Vector2 m_LastMoveVector`（二维向量 m_最后一个移动向量）(偏移: 0x30)
- `int m_ConsecutiveMoveCount`（int m_Consecutive移动数量）(偏移: 0x38)
- `Vector2 m_LastMousePosition`（二维向量 m_最后一个鼠标Position）(偏移: 0x3C)
- `Vector2 m_MousePosition`（二维向量 m_鼠标Position）(偏移: 0x44)
- `GameObject m_CurrentFocusedGameObject`（游戏对象 m_当前聚焦的游戏对象）(偏移: 0x4C)
- `PointerEventData m_InputPointerEvent`（指针事件数据 m_输入指针事件）(偏移: 0x50)
- `string m_HorizontalAxis`（string m_水平轴）(偏移: 0x54)
- `string m_VerticalAxis`（string m_垂直轴）(偏移: 0x58)
- `string m_SubmitButton`（string m_Submit按钮）(偏移: 0x5C)
- `string m_CancelButton`（string m_取消按钮）(偏移: 0x60)
- `float m_InputActionsPerSecond`（float m_输入ActionsPerSecond）(偏移: 0x64)
- `float m_RepeatDelay`（float m_Repeat延迟）(偏移: 0x68)
- `bool m_ForceModuleActive`（bool m_强制模块激活的）(偏移: 0x6C)

### 方法 (36)

- `StandaloneInputModule.InputMode get_inputMode()`
  （Standalone输入Module.输入模式 get_input模式（））
- `bool get_allowActivationOnMobileDevice()`
  （bool get_allowActivationOnMobileDevice（））
- `void set_allowActivationOnMobileDevice(bool value)`
  （void set_allowActivationOnMobileDevice（bool value））
- `bool get_forceModuleActive()`
  （bool get_force模块激活的（））
- `void set_forceModuleActive(bool value)`
  （void set_force模块激活的（bool value））
- `float get_inputActionsPerSecond()`
  （float get_inputActionsPerSecond（））
- `void set_inputActionsPerSecond(float value)`
  （void set_inputActionsPerSecond（float value））
- `float get_repeatDelay()`
  （float get_repeat延迟（））
- `void set_repeatDelay(float value)`
  （void set_repeat延迟（float value））
- `string get_horizontalAxis()`
  （string get_horizontal轴（））
- `void set_horizontalAxis(string value)`
  （void set_horizontal轴（string value））
- `string get_verticalAxis()`
  （string get_vertical轴（））
- `void set_verticalAxis(string value)`
  （void set_vertical轴（string value））
- `string get_submitButton()`
  （string get_submit按钮（））
- `void set_submitButton(string value)`
  （void set_submit按钮（string value））
- `string get_cancelButton()`
  （string get_cancel按钮（））
- `void set_cancelButton(string value)`
  （void set_cancel按钮（string value））
- `bool ShouldIgnoreEventsOnNoFocus()`
  （bool 应该IgnoreEventsOnNo聚焦（））
- `void UpdateModule()`
  （void 更新模块（））
- `void ReleaseMouse(PointerEventData pointerEvent, GameObject currentOverGo)`
  （void Release鼠标（指针事件数据 pointerEvent, 游戏对象 currentOverGo））
- `bool IsModuleSupported()`
  （bool 是否模块Supported（））
- `bool ShouldActivateModule()`
  （bool 应该激活模块（））
- `void ActivateModule()`
  （void 激活模块（））
- `void DeactivateModule()`
  （void 停用模块（））
- `void Process()`
  （void 处理（））
- `bool ProcessTouchEvents()`
  （bool 处理触摸Events（））
- `void ProcessTouchPress(PointerEventData pointerEvent, bool pressed, bool released)`
  （void 处理触摸Press（指针事件数据 pointerEvent, bool pressed, bool released））
- `bool SendSubmitEventToSelectedObject()`
  （bool 发送Submit事件To选中的对象（））
- `Vector2 GetRawMoveVector()`
  （二维向量 获取Raw移动向量（））
- `bool SendMoveEventToSelectedObject()`
  （bool 发送移动事件To选中的对象（））
- `void ProcessMouseEvent()`
  （void 处理鼠标事件（））
- `bool ForceAutoSelect()`
  （bool 强制自动选择（））
- `void ProcessMouseEvent(int id)`
  （void 处理鼠标事件（int id））
- `bool SendUpdateEventToSelectedObject()`
  （bool 发送更新事件To选中的对象（））
- `void ProcessMousePress(PointerInputModule.MouseButtonEventData data)`
  （void 处理鼠标Press（指针输入Module.鼠标按钮事件数据 data））
- `GameObject GetCurrentFocusedGameObject()`
  （游戏对象 获取当前聚焦的游戏对象（））

---

## StandaloneInputModule.InputMode（Standalone输入Module.输入模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## StandardTaskContinuation（StandardTaskContinuation）

**继承**: TaskContinuation（TaskContinuation）

### 字段 (3)

- `Task m_task`（Task m_task）(偏移: 0x8)
- `TaskContinuationOptions m_options`（TaskContinuationOptions m_options）(偏移: 0xC)
- `TaskScheduler m_taskScheduler`（TaskScheduler m_taskScheduler）(偏移: 0x10)

### 方法 (1)

- `void Run(Task completedTask, bool bCanInlineContinuationTask)`
  （void 运行（Task completedTask, bool bCanInlineContinuationTask））

---

## StartEndModifier（开始结束修改器）

**继承**: PathModifier（路径修改器）

### 字段 (9)

- `bool addPoints`（bool addPoints）(偏移: 0xC)
- `StartEndModifier.Exactness exactStartPoint`（开始结束Modifier.Exactness exact开始Point）(偏移: 0x10)
- `StartEndModifier.Exactness exactEndPoint`（开始结束Modifier.Exactness exact结束Point）(偏移: 0x14)
- `Func<Vector3> adjustStartPoint`（Func<Vector3> adjust开始Point）(偏移: 0x18)
- `bool useRaycasting`（bool useRaycasting）(偏移: 0x1C)
- `LayerMask mask`（层掩码 mask）(偏移: 0x20)
- `bool useGraphRaycasting`（bool useGraphRaycasting）(偏移: 0x24)
- `List<GraphNode> connectionBuffer`（List<GraphNode> connection缓冲区）(偏移: 0x28)
- `Action<GraphNode> connectionBufferAddDelegate`（Action<GraphNode> connection缓冲区添加委托）(偏移: 0x2C)

### 方法 (4)

- `int get_Order()`
  （int get_Order（））
- `void Apply(Path _p)`
  （void 应用（路径 _p））
- `Vector3 Snap(ABPath path, StartEndModifier.Exactness mode, bool start, out bool forceAddPoint)`
  （三维向量 Snap（AB路径 path, 开始结束Modifier.Exactness mode, bool start, out bool forceAddPoint））
- `Vector3 GetClampedPoint(Vector3 from, Vector3 to, GraphNode hint)`
  （三维向量 获取ClampedPoint（三维向量 from, 三维向量 to, Graph节点 hint））

---

## StartEndModifier.Exactness（开始结束Modifier.Exactness）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## StateInfoIndex（状态信息索引）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## StateMachineAttribute（状态MachineAttribute）

**继承**: Attribute（Attribute）

### 方法 (1)

- `void set_StateMachineType(Type value)`
  （void set_状态Machine类型（类型 value））

---

## StateMachineBehaviour（状态MachineBehaviour）

**继承**: ScriptableObject（脚本对象）

### 方法 (14)

- `void OnStateEnter(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)`
  （void On状态Enter（动画器 animator, 动画器状态信息 stateInfo, int layerIndex））
- `void OnStateUpdate(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)`
  （void On状态更新（动画器 animator, 动画器状态信息 stateInfo, int layerIndex））
- `void OnStateExit(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)`
  （void On状态Exit（动画器 animator, 动画器状态信息 stateInfo, int layerIndex））
- `void OnStateMove(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)`
  （void On状态移动（动画器 animator, 动画器状态信息 stateInfo, int layerIndex））
- `void OnStateIK(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)`
  （void On状态IK（动画器 animator, 动画器状态信息 stateInfo, int layerIndex））
- `void OnStateMachineEnter(Animator animator, int stateMachinePathHash)`
  （void On状态MachineEnter（动画器 animator, int stateMachinePathHash））
- `void OnStateMachineExit(Animator animator, int stateMachinePathHash)`
  （void On状态MachineExit（动画器 animator, int stateMachinePathHash））
- `void OnStateEnter(Animator animator, AnimatorStateInfo stateInfo, int layerIndex, AnimatorControllerPlayable controller)`
  （void On状态Enter（动画器 animator, 动画器状态信息 stateInfo, int layerIndex, 动画器控制器Playable controller））
- `void OnStateUpdate(Animator animator, AnimatorStateInfo stateInfo, int layerIndex, AnimatorControllerPlayable controller)`
  （void On状态更新（动画器 animator, 动画器状态信息 stateInfo, int layerIndex, 动画器控制器Playable controller））
- `void OnStateExit(Animator animator, AnimatorStateInfo stateInfo, int layerIndex, AnimatorControllerPlayable controller)`
  （void On状态Exit（动画器 animator, 动画器状态信息 stateInfo, int layerIndex, 动画器控制器Playable controller））
- `void OnStateMove(Animator animator, AnimatorStateInfo stateInfo, int layerIndex, AnimatorControllerPlayable controller)`
  （void On状态移动（动画器 animator, 动画器状态信息 stateInfo, int layerIndex, 动画器控制器Playable controller））
- `void OnStateIK(Animator animator, AnimatorStateInfo stateInfo, int layerIndex, AnimatorControllerPlayable controller)`
  （void On状态IK（动画器 animator, 动画器状态信息 stateInfo, int layerIndex, 动画器控制器Playable controller））
- `void OnStateMachineEnter(Animator animator, int stateMachinePathHash, AnimatorControllerPlayable controller)`
  （void On状态MachineEnter（动画器 animator, int stateMachinePathHash, 动画器控制器Playable controller））
- `void OnStateMachineExit(Animator animator, int stateMachinePathHash, AnimatorControllerPlayable controller)`
  （void On状态MachineExit（动画器 animator, int stateMachinePathHash, 动画器控制器Playable controller））

---

## StaticAccessorAttribute（静态的AccessorAttribute）

**继承**: Attribute（Attribute）

### 方法 (2)

- `void set_Name(string value)`
  （void set_名称（string value））
- `void set_Type(StaticAccessorType value)`
  （void set_类型（静态的Accessor类型 value））

---

## StaticAccessorType（静态的Accessor类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## StaticBatchingHelper（静态的Batching辅助器）

### 方法 (3)

- `Mesh InternalCombineVertices(MeshSubsetCombineUtility.MeshInstance[] meshes, string meshName)`
  （网格 内部的CombineVertices（网格SubsetCombineUtility.网格Instance[] meshes, string meshName））
- `void InternalCombineIndices(MeshSubsetCombineUtility.SubMeshInstance[] submeshes, Mesh combinedMesh)`
  （void 内部的CombineIndices（网格SubsetCombineUtility.子网格Instance[] submeshes, 网格 combinedMesh））
- `bool IsMeshBatchable(Mesh mesh)`
  （bool 是否网格Batchable（网格 mesh））

---

## StaticBatchingUtility（静态的Batching工具）

### 字段 (3)

- `ProfilerMarker s_CombineMarker`（ProfilerMarker s_CombineMarker）(偏移: 0x0)
- `ProfilerMarker s_SortMarker`（ProfilerMarker s_SortMarker）(偏移: 0x4)
- `ProfilerMarker s_MakeBatchMarker`（ProfilerMarker s_MakeBatchMarker）(偏移: 0x8)

### 方法 (1)

- `void Combine(GameObject staticBatchRoot)`
  （void Combine（游戏对象 staticBatchRoot））

---

## StaticPointVirtualCamera（静态的Point虚拟的摄像机）

**继承**: ICinemachineCamera（ICinemachine摄像机）

### 方法 (20)

- `void SetState(CameraState state)`
  （void 集合状态（摄像机状态 state））
- `string get_Name()`
  （string get_名称（））
- `void set_Name(string value)`
  （void set_名称（string value））
- `string get_Description()`
  （string get_Description（））
- `int get_Priority()`
  （int get_Priority（））
- `void set_Priority(int value)`
  （void set_Priority（int value））
- `Transform get_LookAt()`
  （变换 get_LookAt（））
- `void set_LookAt(Transform value)`
  （void set_LookAt（变换 value））
- `Transform get_Follow()`
  （变换 get_Follow（））
- `void set_Follow(Transform value)`
  （void set_Follow（变换 value））
- `CameraState get_State()`
  （摄像机状态 get_状态（））
- `void set_State(CameraState value)`
  （void set_状态（摄像机状态 value））
- `GameObject get_VirtualCameraGameObject()`
  （游戏对象 get_虚拟的摄像机游戏对象（））
- `bool get_IsValid()`
  （bool get_是否Valid（））
- `ICinemachineCamera get_ParentCamera()`
  （ICinemachine摄像机 get_父级摄像机（））
- `bool IsLiveChild(ICinemachineCamera vcam, bool dominantChildOnly = False)`
  （bool 是否Live子级（ICinemachine摄像机 vcam, bool dominantChildOnly = False））
- `void UpdateCameraState(Vector3 worldUp, float deltaTime)`
  （void 更新摄像机状态（三维向量 worldUp, float deltaTime））
- `void InternalUpdateCameraState(Vector3 worldUp, float deltaTime)`
  （void 内部的更新摄像机状态（三维向量 worldUp, float deltaTime））
- `void OnTransitionFromCamera(ICinemachineCamera fromCam, Vector3 worldUp, float deltaTime)`
  （void OnTransitionFrom摄像机（ICinemachine摄像机 fromCam, 三维向量 worldUp, float deltaTime））
- `void OnTargetObjectWarped(Transform target, Vector3 positionDelta)`
  （void On目标对象Warped（变换 target, 三维向量 positionDelta））

---

## StaticTree（静态的Tree）

### 字段 (10)

- `short[] lengthAndLiteralsTreeCodes`（short[] lengthAndLiteralsTreeCodes）(偏移: 0x0)
- `short[] distTreeCodes`（short[] distTreeCodes）(偏移: 0x4)
- `StaticTree Literals`（静态的Tree Literals）(偏移: 0x8)
- `StaticTree Distances`（静态的Tree Distances）(偏移: 0xC)
- `StaticTree BitLengths`（静态的Tree BitLengths）(偏移: 0x10)
- `short[] treeCodes`（short[] treeCodes）(偏移: 0x8)
- `int[] extraBits`（int[] extraBits）(偏移: 0xC)
- `int extraBase`（int extra基础）(偏移: 0x10)
- `int elems`（int elems）(偏移: 0x14)
- `int maxLength`（int maxLength）(偏移: 0x18)

---

## Statics（Statics）

### 字段 (3)

- `TraceLoggingDataType IntPtrType`（TraceLogging数据类型 整数Ptr类型）(偏移: 0x0)
- `TraceLoggingDataType UIntPtrType`（TraceLogging数据类型 U整数Ptr类型）(偏移: 0x4)
- `TraceLoggingDataType HexIntPtrType`（TraceLogging数据类型 Hex整数Ptr类型）(偏移: 0x8)

### 方法 (24)

- `byte[] MetadataForString(string name, int prefixSize, int suffixSize, int additionalSize)`
  （byte[] MetadataFor字符串（string name, int prefixSize, int suffixSize, int additionalSize））
- `void EncodeTags(int tags, ref int pos, byte[] metadata)`
  （void EncodeTags（int tags, ref int pos, byte[] metadata））
- `byte Combine(int settingValue, byte defaultValue)`
  （byte Combine（int settingValue, byte defaultValue））
- `int Combine(int settingValue1, int settingValue2)`
  （int Combine（int settingValue1, int settingValue2））
- `void CheckName(string name)`
  （void 检查名称（string name））
- `bool ShouldOverrideFieldName(string fieldName)`
  （bool 应该重写Field名称（string fieldName））
- `TraceLoggingDataType MakeDataType(TraceLoggingDataType baseType, EventFieldFormat format)`
  （TraceLogging数据类型 Make数据类型（TraceLogging数据类型 baseType, 事件Field格式化 format））
- `TraceLoggingDataType Format8(EventFieldFormat format, TraceLoggingDataType native)`
  （TraceLogging数据类型 Format8（事件Field格式化 format, TraceLogging数据类型 native））
- `TraceLoggingDataType Format16(EventFieldFormat format, TraceLoggingDataType native)`
  （TraceLogging数据类型 Format16（事件Field格式化 format, TraceLogging数据类型 native））
- `TraceLoggingDataType Format32(EventFieldFormat format, TraceLoggingDataType native)`
  （TraceLogging数据类型 Format32（事件Field格式化 format, TraceLogging数据类型 native））
- `TraceLoggingDataType Format64(EventFieldFormat format, TraceLoggingDataType native)`
  （TraceLogging数据类型 Format64（事件Field格式化 format, TraceLogging数据类型 native））
- `TraceLoggingDataType FormatPtr(EventFieldFormat format, TraceLoggingDataType native)`
  （TraceLogging数据类型 格式化Ptr（事件Field格式化 format, TraceLogging数据类型 native））
- `object CreateInstance(Type type, object[] parameters)`
  （object 创建实例（类型 type, object[] parameters））
- `bool IsValueType(Type type)`
  （bool 是否值类型（类型 type））
- `bool IsEnum(Type type)`
  （bool 是否Enum（类型 type））
- `IEnumerable<PropertyInfo> GetProperties(Type type)`
  （IEnumerable<属性Info> 获取Properties（类型 type））
- `MethodInfo GetGetMethod(PropertyInfo propInfo)`
  （Method信息 获取获取Method（属性信息 propInfo））
- `MethodInfo GetDeclaredStaticMethod(Type declaringType, string name)`
  （Method信息 获取Declared静态的Method（类型 declaringType, string name））
- `bool HasCustomAttribute(PropertyInfo propInfo, Type attributeType)`
  （bool 是否有自定义的Attribute（属性信息 propInfo, 类型 attributeType））
- `Type[] GetGenericArguments(Type type)`
  （Type[] 获取GenericArguments（类型 type））
- `Type FindEnumerableElementType(Type type)`
  （类型 查找Enumerable元素类型（类型 type））
- `bool IsGenericMatch(Type type, object openType)`
  （bool 是否Generic比赛（类型 type, object openType））
- `Delegate CreateDelegate(Type delegateType, MethodInfo methodInfo)`
  （委托 创建委托（类型 delegateType, Method信息 methodInfo））
- `TraceLoggingTypeInfo GetTypeInfoInstance(Type dataType, List<Type> recursionCheck)`
  （TraceLogging类型信息 获取类型信息实例（类型 dataType, List<Type> recursionCheck））

---

## StencilMaterial（Stencil材质）

### 字段 (1)

- `List<StencilMaterial.MatEntry> m_List`（List<StencilMaterial.材质Entry> m_列表）(偏移: 0x0)

### 方法 (6)

- `Material Add(Material baseMat, int stencilID)`
  （材质 添加（材质 baseMat, int stencilID））
- `Material Add(Material baseMat, int stencilID, StencilOp operation, CompareFunction compareFunction, ColorWriteMask colorWriteMask)`
  （材质 添加（材质 baseMat, int stencilID, StencilOp operation, CompareFunction compareFunction, 颜色Write掩码 colorWriteMask））
- `void LogWarningWhenNotInBatchmode(string warning, Object context)`
  （void LogWarningWhenNotInBatchmode（string warning, 对象 context））
- `Material Add(Material baseMat, int stencilID, StencilOp operation, CompareFunction compareFunction, ColorWriteMask colorWriteMask, int readMask, int writeMask)`
  （材质 添加（材质 baseMat, int stencilID, StencilOp operation, CompareFunction compareFunction, 颜色Write掩码 colorWriteMask, int readMask, int writeMask））
- `void Remove(Material customMat)`
  （void 移除（材质 customMat））
- `void ClearAll()`
  （void 清除所有（））

---

## StencilMaterial.MatEntry（StencilMaterial.材质Entry）

### 字段 (10)

- `Material baseMat`（材质 base材质）(偏移: 0x8)
- `Material customMat`（材质 custom材质）(偏移: 0xC)
- `int count`（int count）(偏移: 0x10)
- `int stencilId`（int stencilId）(偏移: 0x14)
- `StencilOp operation`（StencilOp operation）(偏移: 0x18)
- `CompareFunction compareFunction`（CompareFunction compareFunction）(偏移: 0x1C)
- `int readMask`（int read掩码）(偏移: 0x20)
- `int writeMask`（int write掩码）(偏移: 0x24)
- `bool useAlphaClip`（bool use透明度弹匣）(偏移: 0x28)
- `ColorWriteMask colorMask`（颜色Write掩码 color掩码）(偏移: 0x2C)

---

## StencilOp（StencilOp）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## StencilState（Stencil状态）

**继承**: IEquatable<StencilState>（IEquatable<StencilState>）

### 字段 (12)

- `byte m_Enabled`（byte m_启用的）(偏移: 0x0)
- `byte m_ReadMask`（byte m_Read掩码）(偏移: 0x0)
- `byte m_WriteMask`（byte m_Write掩码）(偏移: 0x0)
- `byte m_Padding`（byte m_Padding）(偏移: 0x0)
- `byte m_CompareFunctionFront`（byte m_CompareFunction前）(偏移: 0x0)
- `byte m_PassOperationFront`（byte m_PassOperation前）(偏移: 0x0)
- `byte m_FailOperationFront`（byte m_FailOperation前）(偏移: 0x0)
- `byte m_ZFailOperationFront`（byte m_ZFailOperation前）(偏移: 0x0)
- `byte m_CompareFunctionBack`（byte m_CompareFunction后）(偏移: 0x0)
- `byte m_PassOperationBack`（byte m_PassOperation后）(偏移: 0x0)
- `byte m_FailOperationBack`（byte m_FailOperation后）(偏移: 0x0)
- `byte m_ZFailOperationBack`（byte m_ZFailOperation后）(偏移: 0x0)

### 方法 (28)

- `StencilState get_defaultValue()`
  （Stencil状态 get_default值（））
- `bool get_enabled()`
  （bool get_enabled（））
- `void set_enabled(bool value)`
  （void set_enabled（bool value））
- `byte get_readMask()`
  （byte get_read掩码（））
- `byte get_writeMask()`
  （byte get_write掩码（））
- `void SetCompareFunction(CompareFunction value)`
  （void 集合CompareFunction（CompareFunction value））
- `void SetPassOperation(StencilOp value)`
  （void 集合PassOperation（StencilOp value））
- `void SetFailOperation(StencilOp value)`
  （void 集合FailOperation（StencilOp value））
- `void SetZFailOperation(StencilOp value)`
  （void 集合ZFailOperation（StencilOp value））
- `CompareFunction get_compareFunctionFront()`
  （CompareFunction get_compareFunction前（））
- `void set_compareFunctionFront(CompareFunction value)`
  （void set_compareFunction前（CompareFunction value））
- `StencilOp get_passOperationFront()`
  （StencilOp get_passOperation前（））
- `void set_passOperationFront(StencilOp value)`
  （void set_passOperation前（StencilOp value））
- `StencilOp get_failOperationFront()`
  （StencilOp get_failOperation前（））
- `void set_failOperationFront(StencilOp value)`
  （void set_failOperation前（StencilOp value））
- `StencilOp get_zFailOperationFront()`
  （StencilOp get_zFailOperation前（））
- `void set_zFailOperationFront(StencilOp value)`
  （void set_zFailOperation前（StencilOp value））
- `CompareFunction get_compareFunctionBack()`
  （CompareFunction get_compareFunction后（））
- `void set_compareFunctionBack(CompareFunction value)`
  （void set_compareFunction后（CompareFunction value））
- `StencilOp get_passOperationBack()`
  （StencilOp get_passOperation后（））
- `void set_passOperationBack(StencilOp value)`
  （void set_passOperation后（StencilOp value））
- `StencilOp get_failOperationBack()`
  （StencilOp get_failOperation后（））
- `void set_failOperationBack(StencilOp value)`
  （void set_failOperation后（StencilOp value））
- `StencilOp get_zFailOperationBack()`
  （StencilOp get_zFailOperation后（））
- `void set_zFailOperationBack(StencilOp value)`
  （void set_zFailOperation后（StencilOp value））
- `bool Equals(StencilState other)`
  （bool Equals（Stencil状态 other））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## StencilStateData（Stencil状态数据）

### 字段 (6)

- `bool overrideStencilState`（bool overrideStencil状态）(偏移: 0x8)
- `int stencilReference`（int stencil引用）(偏移: 0xC)
- `CompareFunction stencilCompareFunction`（CompareFunction stencilCompareFunction）(偏移: 0x10)
- `StencilOp passOperation`（StencilOp passOperation）(偏移: 0x14)
- `StencilOp failOperation`（StencilOp failOperation）(偏移: 0x18)
- `StencilOp zFailOperation`（StencilOp zFailOperation）(偏移: 0x1C)

---

## StencilUsage（StencilUsage）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## StereoTargetEyeMask（Stereo目标Eye掩码）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Stopwatch（Stopwatch）

### 字段 (5)

- `long Frequency`（long Frequency）(偏移: 0x0)
- `bool IsHighResolution`（bool 是否HighResolution）(偏移: 0x8)
- `long elapsed`（long elapsed）(偏移: 0x8)
- `long started`（long started）(偏移: 0x10)
- `bool is_running`（bool is_running）(偏移: 0x18)

### 方法 (8)

- `long GetTimestamp()`
  （long 获取时间戳（））
- `Stopwatch StartNew()`
  （Stopwatch 开始新的（））
- `TimeSpan get_Elapsed()`
  （时间Span get_Elapsed（））
- `long get_ElapsedMilliseconds()`
  （long get_ElapsedMilliseconds（））
- `long get_ElapsedTicks()`
  （long get_ElapsedTicks（））
- `void Reset()`
  （void 重置（））
- `void Start()`
  （void 开始（））
- `void Stop()`
  （void 停止（））

---

## StoreActionsOptimization（商店ActionsOptimization）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Stream（流）

**继承**: MarshalByRefObject, IDisposable（MarshalByRef对象, IDisposable）

### 字段 (3)

- `Stream Null`（流 Null）(偏移: 0x0)
- `Stream.ReadWriteTask _activeReadWriteTask`（Stream.ReadWriteTask _activeReadWriteTask）(偏移: 0xC)
- `SemaphoreSlim _asyncActiveSemaphore`（SemaphoreSlim _async激活的Semaphore）(偏移: 0x10)

### 方法 (18)

- `SemaphoreSlim EnsureAsyncActiveSemaphoreInitialized()`
  （SemaphoreSlim Ensure异步激活的SemaphoreInitialized（））
- `void Close()`
  （void 关闭（））
- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））
- `IAsyncResult BeginRead(byte[] buffer, int offset, int count, AsyncCallback callback, object state)`
  （I异步Result BeginRead（byte[] buffer, int offset, int count, 异步回调 callback, object state））
- `IAsyncResult BeginReadInternal(byte[] buffer, int offset, int count, AsyncCallback callback, object state, bool serializeAsynchronously)`
  （I异步Result BeginRead内部的（byte[] buffer, int offset, int count, 异步回调 callback, object state, bool serializeAsynchronously））
- `int EndRead(IAsyncResult asyncResult)`
  （int 结束Read（I异步Result asyncResult））
- `IAsyncResult BeginWrite(byte[] buffer, int offset, int count, AsyncCallback callback, object state)`
  （I异步Result BeginWrite（byte[] buffer, int offset, int count, 异步回调 callback, object state））
- `IAsyncResult BeginWriteInternal(byte[] buffer, int offset, int count, AsyncCallback callback, object state, bool serializeAsynchronously)`
  （I异步Result BeginWrite内部的（byte[] buffer, int offset, int count, 异步回调 callback, object state, bool serializeAsynchronously））
- `void RunReadWriteTaskWhenReady(Task asyncWaiter, Stream.ReadWriteTask readWriteTask)`
  （void 运行ReadWriteTaskWhenReady（Task asyncWaiter, Stream.ReadWriteTask readWriteTask））
- `void RunReadWriteTask(Stream.ReadWriteTask readWriteTask)`
  （void 运行ReadWriteTask（Stream.ReadWriteTask readWriteTask））
- `void EndWrite(IAsyncResult asyncResult)`
  （void 结束Write（I异步Result asyncResult））
- `int ReadByte()`
  （int ReadByte（））
- `void WriteByte(byte value)`
  （void WriteByte（byte value））
- `IAsyncResult BlockingBeginRead(byte[] buffer, int offset, int count, AsyncCallback callback, object state)`
  （I异步Result BlockingBeginRead（byte[] buffer, int offset, int count, 异步回调 callback, object state））
- `int BlockingEndRead(IAsyncResult asyncResult)`
  （int Blocking结束Read（I异步Result asyncResult））
- `IAsyncResult BlockingBeginWrite(byte[] buffer, int offset, int count, AsyncCallback callback, object state)`
  （I异步Result BlockingBeginWrite（byte[] buffer, int offset, int count, 异步回调 callback, object state））
- `void BlockingEndWrite(IAsyncResult asyncResult)`
  （void Blocking结束Write（I异步Result asyncResult））

---

## Stream.NullStream（Stream.Null流）

**继承**: Stream（流）

### 方法 (18)

- `bool get_CanRead()`
  （bool get_能否Read（））
- `bool get_CanWrite()`
  （bool get_能否Write（））
- `bool get_CanSeek()`
  （bool get_能否Seek（））
- `long get_Length()`
  （long get_Length（））
- `long get_Position()`
  （long get_Position（））
- `void set_Position(long value)`
  （void set_Position（long value））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））
- `void Flush()`
  （void Flush（））
- `IAsyncResult BeginRead(byte[] buffer, int offset, int count, AsyncCallback callback, object state)`
  （I异步Result BeginRead（byte[] buffer, int offset, int count, 异步回调 callback, object state））
- `int EndRead(IAsyncResult asyncResult)`
  （int 结束Read（I异步Result asyncResult））
- `IAsyncResult BeginWrite(byte[] buffer, int offset, int count, AsyncCallback callback, object state)`
  （I异步Result BeginWrite（byte[] buffer, int offset, int count, 异步回调 callback, object state））
- `void EndWrite(IAsyncResult asyncResult)`
  （void 结束Write（I异步Result asyncResult））
- `int Read([In] [Out] byte[] buffer, int offset, int count)`
  （int Read（[In] [Out] byte[] buffer, int offset, int count））
- `int ReadByte()`
  （int ReadByte（））
- `void Write(byte[] buffer, int offset, int count)`
  （void Write（byte[] buffer, int offset, int count））
- `void WriteByte(byte value)`
  （void WriteByte（byte value））
- `long Seek(long offset, SeekOrigin origin)`
  （long Seek（long offset, SeekOrigin origin））
- `void SetLength(long length)`
  （void 集合Length（long length））

---

## Stream.ReadWriteTask（Stream.ReadWriteTask）

**继承**: Task<int>, ITaskCompletionAction（Task<int>, ITaskCompletion动作）

### 字段 (8)

- `bool _isRead`（bool _isRead）(偏移: 0x2C)
- `Stream _stream`（流 _stream）(偏移: 0x30)
- `byte[] _buffer`（byte[] _buffer）(偏移: 0x34)
- `int _offset`（int _offset）(偏移: 0x38)
- `int _count`（int _count）(偏移: 0x3C)
- `AsyncCallback _callback`（异步回调 _callback）(偏移: 0x40)
- `ExecutionContext _context`（ExecutionContext _context）(偏移: 0x44)
- `ContextCallback s_invokeAsyncCallback`（Context回调 s_invoke异步回调）(偏移: 0x0)

### 方法 (2)

- `void ClearBeginState()`
  （void 清除Begin状态（））
- `void InvokeAsyncCallback(object completedTask)`
  （void Invoke异步回调（object completedTask））

---

## Stream.SynchronousAsyncResult（Stream.Synchronous异步Result）

**继承**: IAsyncResult（I异步Result）

### 字段 (6)

- `object _stateObject`（object _state对象）(偏移: 0x8)
- `bool _isWrite`（bool _isWrite）(偏移: 0xC)
- `ManualResetEvent _waitHandle`（手动重置事件 _wait句柄）(偏移: 0x10)
- `ExceptionDispatchInfo _exceptionInfo`（ExceptionDispatch信息 _exception信息）(偏移: 0x14)
- `bool _endXxxCalled`（bool _endXxxCalled）(偏移: 0x18)
- `int _bytesRead`（int _bytesRead）(偏移: 0x1C)

### 方法 (4)

- `WaitHandle get_AsyncWaitHandle()`
  （Wait句柄 get_异步Wait句柄（））
- `void ThrowIfError()`
  （void 投掷IfError（））
- `int EndRead(IAsyncResult asyncResult)`
  （int 结束Read（I异步Result asyncResult））
- `void EndWrite(IAsyncResult asyncResult)`
  （void 结束Write（I异步Result asyncResult））

---

