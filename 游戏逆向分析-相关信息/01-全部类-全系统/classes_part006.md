# 游戏类定义 (Part 6/21)

共 200 个类 (总序号 1001 - 1200)

---

## DefaultMaterialType（默认的材质类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DefaultMemberAttribute（默认的MemberAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `string m_memberName`（string m_member名称）(偏移: 0x8)

### 方法 (1)

- `string get_MemberName()`
  （string get_Member名称（））

---

## DefaultPropertyAttribute（默认的属性Attribute）

**继承**: Attribute（属性）

### 字段 (2)

- `string name`（字符串 名称）(偏移: 0x8)
- `DefaultPropertyAttribute Default`（默认的属性Attribute 默认的）(偏移: 0x0)

### 方法 (3)

- `string get_Name()`
  （字符串 获取_名称（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## DefaultProxySection（默认的代理Section）

**继承**: ConfigurationSection（配置节）

### 方法 (2)

- `ConfigurationPropertyCollection get_Properties()`
  （配置属性集合 获取_属性（））
- `void Reset(ConfigurationElement parentElement)`
  （void 重置（Configuration元素 parentElement））

---

## DefaultValueAttribute（默认的值Attribute）

**继承**: Attribute（属性）

### 字段 (1)

- `object value`（对象 value）(偏移: 0x8)

### 方法 (1)

- `object get_Value()`
  （对象 获取_值（））

---

## DefaultValueAttribute（默认的值Attribute）

**继承**: Attribute（属性）

### 字段 (1)

- `object DefaultValue`（object 默认的值）(偏移: 0x8)

### 方法 (3)

- `object get_Value()`
  （对象 获取_值（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## DeferredConfig（Deferred配置）

### 方法 (6)

- `bool get_IsOpenGL()`
  （bool get_是否打开GL（））
- `void set_IsOpenGL(bool value)`
  （void set_是否打开GL（bool value））
- `bool get_UseCBufferForDepthRange()`
  （bool get_UseC缓冲区For深度范围（））
- `bool get_UseCBufferForTileList()`
  （bool get_UseC缓冲区ForTile列表（））
- `bool get_UseCBufferForLightData()`
  （bool get_UseC缓冲区For光照数据（））
- `bool get_UseCBufferForLightList()`
  （bool get_UseC缓冲区For光照列表（））

---

## DeferredLights（DeferredLights）

### 字段 (37)

- `string k_SetupLights`（string k_SetupLights）(偏移: 0x0)
- `string k_DeferredPass`（string k_DeferredPass）(偏移: 0x4)
- `string k_TileDepthInfo`（string k_Tile深度信息）(偏移: 0x8)
- `string k_DeferredTiledPass`（string k_DeferredTiledPass）(偏移: 0xC)
- `string k_DeferredStencilPass`（string k_DeferredStencilPass）(偏移: 0x10)
- `string k_DeferredFogPass`（string k_DeferredFogPass）(偏移: 0x14)
- `string k_ClearStencilPartial`（string k_清除StencilPartial）(偏移: 0x18)
- `string k_SetupLightConstants`（string k_Setup光照Constants）(偏移: 0x1C)
- `float kStencilShapeGuard`（float kStencilShapeGuard）(偏移: 0x20)
- `ProfilingSampler m_ProfilingSetupLights`（ProfilingSampler m_ProfilingSetupLights）(偏移: 0x24)
- `ProfilingSampler m_ProfilingDeferredPass`（ProfilingSampler m_ProfilingDeferredPass）(偏移: 0x28)
- `ProfilingSampler m_ProfilingTileDepthInfo`（ProfilingSampler m_ProfilingTile深度信息）(偏移: 0x2C)
- `ProfilingSampler m_ProfilingSetupLightConstants`（ProfilingSampler m_ProfilingSetup光照Constants）(偏移: 0x30)
- `int m_CachedRenderWidth`（int m_CachedRender宽度）(偏移: 0x118)
- `int m_CachedRenderHeight`（int m_CachedRender高度）(偏移: 0x11C)
- `Matrix4x4 m_CachedProjectionMatrix`（Matrix4x4 m_CachedProjection矩阵）(偏移: 0x120)
- `DeferredTiler[] m_Tilers`（DeferredTiler[] m_Tilers）(偏移: 0x160)
- `int[] m_TileDataCapacities`（int[] m_Tile数据Capacities）(偏移: 0x164)
- `bool m_HasTileVisLights`（bool m_是否有TileVisLights）(偏移: 0x168)
- `NativeArray<ushort> m_stencilVisLights`（NativeArray<ushort> m_stencilVisLights）(偏移: 0x16C)
- `NativeArray<ushort> m_stencilVisLightOffsets`（NativeArray<ushort> m_stencilVis光照Offsets）(偏移: 0x178)
- `AdditionalLightsShadowCasterPass m_AdditionalLightsShadowCasterPass`（AdditionalLightsShadowCasterPass m_AdditionalLightsShadowCasterPass）(偏移: 0x184)
- `Mesh m_SphereMesh`（网格 m_Sphere网格）(偏移: 0x188)
- `Mesh m_HemisphereMesh`（网格 m_Hemisphere网格）(偏移: 0x18C)
- `Mesh m_FullscreenMesh`（网格 m_Fullscreen网格）(偏移: 0x190)
- `int m_MaxDepthRangePerBatch`（int m_最大深度范围PerBatch）(偏移: 0x194)
- `int m_MaxTilesPerBatch`（int m_最大TilesPerBatch）(偏移: 0x198)
- `int m_MaxPunctualLightPerBatch`（int m_最大Punctual光照PerBatch）(偏移: 0x19C)
- `int m_MaxRelLightIndicesPerBatch`（int m_最大Rel光照IndicesPerBatch）(偏移: 0x1A0)
- `Material m_TileDepthInfoMaterial`（材质 m_Tile深度信息材质）(偏移: 0x1A4)
- `Material m_TileDeferredMaterial`（材质 m_TileDeferred材质）(偏移: 0x1A8)
- `Material m_StencilDeferredMaterial`（材质 m_StencilDeferred材质）(偏移: 0x1AC)
- `Matrix4x4[] m_ScreenToWorld`（Matrix4x4[] m_屏幕的To世界的）(偏移: 0x1B0)
- `ProfilingSampler m_ProfilingSamplerDeferredTiledPass`（ProfilingSampler m_ProfilingSamplerDeferredTiledPass）(偏移: 0x1B4)
- `ProfilingSampler m_ProfilingSamplerDeferredStencilPass`（ProfilingSampler m_ProfilingSamplerDeferredStencilPass）(偏移: 0x1B8)
- `ProfilingSampler m_ProfilingSamplerDeferredFogPass`（ProfilingSampler m_ProfilingSamplerDeferredFogPass）(偏移: 0x1BC)
- `ProfilingSampler m_ProfilingSamplerClearStencilPartialPass`（ProfilingSampler m_ProfilingSampler清除StencilPartialPass）(偏移: 0x1C0)

### 方法 (83)

- `int get_GbufferDepthIndex()`
  （int get_Gbuffer深度索引（））
- `int get_GBufferAlbedoIndex()`
  （int get_G缓冲区Albedo索引（））
- `int get_GBufferSpecularMetallicIndex()`
  （int get_G缓冲区SpecularMetallic索引（））
- `int get_GBufferNormalSmoothnessIndex()`
  （int get_G缓冲区法线Smoothness索引（））
- `int get_GBufferLightingIndex()`
  （int get_G缓冲区Lighting索引（））
- `int get_GBufferShadowMask()`
  （int get_G缓冲区Shadow掩码（））
- `int get_GBufferSliceCount()`
  （int get_G缓冲区Slice数量（））
- `GraphicsFormat GetGBufferFormat(int index)`
  （Graphics格式化 获取G缓冲区格式化（int index））
- `bool get_UseShadowMask()`
  （bool get_UseShadow掩码（））
- `bool get_UseRenderPass()`
  （bool get_UseRenderPass（））
- `void set_UseRenderPass(bool value)`
  （void set_UseRenderPass（bool value））
- `bool get_HasDepthPrepass()`
  （bool get_是否有深度Prepass（））
- `void set_HasDepthPrepass(bool value)`
  （void set_是否有深度Prepass（bool value））
- `bool get_IsOverlay()`
  （bool get_是否Overlay（））
- `void set_IsOverlay(bool value)`
  （void set_是否Overlay（bool value））
- `bool get_AccurateGbufferNormals()`
  （bool get_AccurateGbufferNormals（））
- `void set_AccurateGbufferNormals(bool value)`
  （void set_AccurateGbufferNormals（bool value））
- `bool get_TiledDeferredShading()`
  （bool get_TiledDeferredShading（））
- `void set_TiledDeferredShading(bool value)`
  （void set_TiledDeferredShading（bool value））
- `MixedLightingSetup get_MixedLightingSetup()`
  （MixedLightingSetup get_MixedLightingSetup（））
- `void set_MixedLightingSetup(MixedLightingSetup value)`
  （void set_MixedLightingSetup（MixedLightingSetup value））
- `bool get_UseJobSystem()`
  （bool get_UseJob系统（））
- `void set_UseJobSystem(bool value)`
  （void set_UseJob系统（bool value））
- `int get_RenderWidth()`
  （int get_Render宽度（））
- `void set_RenderWidth(int value)`
  （void set_Render宽度（int value））
- `int get_RenderHeight()`
  （int get_Render高度（））
- `void set_RenderHeight(int value)`
  （void set_Render高度（int value））
- `RenderTargetHandle[] get_GbufferAttachments()`
  （Render目标Handle[] get_GbufferAttachments（））
- `void set_GbufferAttachments(RenderTargetHandle[] value)`
  （void set_GbufferAttachments（Render目标Handle[] value））
- `RenderTargetHandle get_DepthAttachment()`
  （Render目标句柄 get_深度Attachment（））
- `void set_DepthAttachment(RenderTargetHandle value)`
  （void set_深度Attachment（Render目标句柄 value））
- `RenderTargetHandle get_DepthCopyTexture()`
  （Render目标句柄 get_深度复制纹理（））
- `void set_DepthCopyTexture(RenderTargetHandle value)`
  （void set_深度复制纹理（Render目标句柄 value））
- `RenderTargetHandle get_DepthInfoTexture()`
  （Render目标句柄 get_深度信息纹理（））
- `void set_DepthInfoTexture(RenderTargetHandle value)`
  （void set_深度信息纹理（Render目标句柄 value））
- `RenderTargetHandle get_TileDepthInfoTexture()`
  （Render目标句柄 get_Tile深度信息纹理（））
- `void set_TileDepthInfoTexture(RenderTargetHandle value)`
  （void set_Tile深度信息纹理（Render目标句柄 value））
- `RenderTargetIdentifier[] get_GbufferAttachmentIdentifiers()`
  （Render目标Identifier[] get_GbufferAttachmentIdentifiers（））
- `void set_GbufferAttachmentIdentifiers(RenderTargetIdentifier[] value)`
  （void set_GbufferAttachmentIdentifiers（Render目标Identifier[] value））
- `RenderTargetIdentifier get_DepthAttachmentIdentifier()`
  （Render目标Identifier get_深度AttachmentIdentifier（））
- `void set_DepthAttachmentIdentifier(RenderTargetIdentifier value)`
  （void set_深度AttachmentIdentifier（Render目标Identifier value））
- `RenderTargetIdentifier get_DepthCopyTextureIdentifier()`
  （Render目标Identifier get_深度复制纹理Identifier（））
- `void set_DepthCopyTextureIdentifier(RenderTargetIdentifier value)`
  （void set_深度复制纹理Identifier（Render目标Identifier value））
- `RenderTargetIdentifier get_DepthInfoTextureIdentifier()`
  （Render目标Identifier get_深度信息纹理Identifier（））
- `void set_DepthInfoTextureIdentifier(RenderTargetIdentifier value)`
  （void set_深度信息纹理Identifier（Render目标Identifier value））
- `RenderTargetIdentifier get_TileDepthInfoTextureIdentifier()`
  （Render目标Identifier get_Tile深度信息纹理Identifier（））
- `void set_TileDepthInfoTextureIdentifier(RenderTargetIdentifier value)`
  （void set_Tile深度信息纹理Identifier（Render目标Identifier value））
- `void SetupLights(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void SetupLights（ScriptableRenderContext context, ref RenderingData renderingData））
- `void ResolveMixedLightingMode(ref RenderingData renderingData)`
  （void ResolveMixedLighting模式（ref RenderingData renderingData））
- `bool IsRuntimeSupportedThisFrame()`
  （bool 是否RuntimeSupportedThisFrame（））
- `void Setup(ref RenderingData renderingData, AdditionalLightsShadowCasterPass additionalLightsShadowCasterPass, bool hasDepthPrepass, bool isOverlay, RenderTargetHandle depthCopyTexture, RenderTargetHandle depthInfoTexture, RenderTargetHandle tileDepthInfoTexture, RenderTargetHandle depthAttachment, RenderTargetHandle[] gbufferHandles)`
  （void Setup（ref RenderingData renderingData, AdditionalLightsShadowCasterPass additionalLightsShadowCasterPass, bool hasDepthPrepass, bool isOverlay, Render目标句柄 depthCopyTexture, Render目标句柄 depthInfoTexture, Render目标句柄 tileDepthInfoTexture, Render目标句柄 depthAttachment, Render目标Handle[] gbufferHandles））
- `void OnCameraCleanup(CommandBuffer cmd)`
  （void 摄像机清理时（命令缓冲区 cmd））
- `StencilState OverwriteStencil(StencilState s, int stencilWriteMask)`
  （Stencil状态 OverwriteStencil（Stencil状态 s, int stencilWriteMask））
- `RenderStateBlock OverwriteStencil(RenderStateBlock block, int stencilWriteMask, int stencilRef)`
  （Render状态Block OverwriteStencil（Render状态Block block, int stencilWriteMask, int stencilRef））
- `bool HasTileLights()`
  （bool 是否有TileLights（））
- `bool HasTileDepthRangeExtraPass()`
  （bool 是否有Tile深度范围额外的Pass（））
- `void ExecuteTileDepthInfoPass(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行Tile深度信息Pass（ScriptableRenderContext context, ref RenderingData renderingData））
- `void ExecuteDownsampleBitmaskPass(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行DownsampleBitmaskPass（ScriptableRenderContext context, ref RenderingData renderingData））
- `void ClearStencilPartial(CommandBuffer cmd)`
  （void 清除StencilPartial（Command缓冲区 cmd））
- `void ExecuteDeferredPass(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行DeferredPass（ScriptableRenderContext context, ref RenderingData renderingData））
- `void SetupShaderLightConstants(CommandBuffer cmd, ref RenderingData renderingData)`
  （void Setup着色器光照Constants（Command缓冲区 cmd, ref RenderingData renderingData））
- `void SetupMainLightConstants(CommandBuffer cmd, ref LightData lightData)`
  （void Setup主要的光照Constants（Command缓冲区 cmd, ref LightData lightData））
- `void SetupMatrixConstants(CommandBuffer cmd, ref RenderingData renderingData)`
  （void Setup矩阵Constants（Command缓冲区 cmd, ref RenderingData renderingData））
- `void SortLights(ref NativeArray<DeferredTiler.PrePunctualLight> prePunctualLights)`
  （void SortLights（ref NativeArray<DeferredTiler.PrePunctualLight> prePunctualLights））
- `bool CheckHasTileLights(ref NativeArray<VisibleLight> visibleLights)`
  （bool 检查是否有TileLights（ref NativeArray<VisibleLight> visibleLights））
- `void PrecomputeLights(out NativeArray<DeferredTiler.PrePunctualLight> prePunctualLights, out NativeArray<ushort> stencilVisLights, out NativeArray<ushort> stencilVisLightOffsets, ref NativeArray<VisibleLight> visibleLights, bool hasAdditionalLights, Matrix4x4 view, bool isOrthographic, float zNear)`
  （void PrecomputeLights（out NativeArray<DeferredTiler.PrePunctualLight> prePunctualLights, out NativeArray<ushort> stencilVisLights, out NativeArray<ushort> stencilVisLightOffsets, ref NativeArray<VisibleLight> visibleLights, bool hasAdditionalLights, Matrix4x4 view, bool isOrthographic, float zNear））
- `void RenderTileLights(ScriptableRenderContext context, CommandBuffer cmd, ref RenderingData renderingData)`
  （void RenderTileLights（ScriptableRenderContext context, Command缓冲区 cmd, ref RenderingData renderingData））
- `void RenderStencilLights(ScriptableRenderContext context, CommandBuffer cmd, ref RenderingData renderingData)`
  （void RenderStencilLights（ScriptableRenderContext context, Command缓冲区 cmd, ref RenderingData renderingData））
- `void RenderStencilDirectionalLights(CommandBuffer cmd, ref RenderingData renderingData, NativeArray<VisibleLight> visibleLights, int mainLightIndex)`
  （void RenderStencilDirectionalLights（Command缓冲区 cmd, ref RenderingData renderingData, NativeArray<可见的Light> visibleLights, int mainLightIndex））
- `void RenderStencilPointLights(CommandBuffer cmd, ref RenderingData renderingData, NativeArray<VisibleLight> visibleLights)`
  （void RenderStencilPointLights（Command缓冲区 cmd, ref RenderingData renderingData, NativeArray<可见的Light> visibleLights））
- `void RenderStencilSpotLights(CommandBuffer cmd, ref RenderingData renderingData, NativeArray<VisibleLight> visibleLights)`
  （void RenderStencilSpotLights（Command缓冲区 cmd, ref RenderingData renderingData, NativeArray<可见的Light> visibleLights））
- `void RenderFog(ScriptableRenderContext context, CommandBuffer cmd, ref RenderingData renderingData)`
  （void RenderFog（ScriptableRenderContext context, Command缓冲区 cmd, ref RenderingData renderingData））
- `int TrimLights(ref NativeArray<ushort> trimmedLights, ref NativeArray<ushort> tiles, int offset, int lightCount, ref BitArray usedLights)`
  （int TrimLights（ref NativeArray<ushort> trimmedLights, ref NativeArray<ushort> tiles, int offset, int lightCount, ref BitArray usedLights））
- `void StorePunctualLightData(ref NativeArray<uint4> punctualLightBuffer, int storeIndex, ref NativeArray<VisibleLight> visibleLights, int index)`
  （void 商店Punctual光照数据（ref NativeArray<uint4> punctualLightBuffer, int storeIndex, ref NativeArray<VisibleLight> visibleLights, int index））
- `void StoreTileData(ref NativeArray<uint4> tileList, int storeIndex, uint tileID, uint listBitMask, ushort relLightOffset, ushort lightCount)`
  （void 商店Tile数据（ref NativeArray<uint4> tileList, int storeIndex, uint tileID, uint listBitMask, ushort relLightOffset, ushort lightCount））
- `bool IsTileLight(VisibleLight visibleLight)`
  （bool 是否Tile光照（可见的光照 visibleLight））
- `Mesh CreateSphereMesh()`
  （网格 创建Sphere网格（））
- `Mesh CreateHemisphereMesh()`
  （网格 创建Hemisphere网格（））
- `Mesh CreateFullscreenMesh()`
  （网格 创建Fullscreen网格（））
- `int Align(int s, int alignment)`
  （int Align（int s, int alignment））
- `uint PackTileID(uint i, uint j)`
  （uint PackTileID（uint i, uint j））
- `uint FloatToUInt(float val)`
  （uint 浮点数ToU整数（float val））
- `uint Half2ToUInt(float x, float y)`
  （uint Half2ToU整数（float x, float y））

---

## DeferredLights.CullLightsJob（DeferredLights.CullLightsJob）

**继承**: IJob（IJob）

### 字段 (9)

- `DeferredTiler tiler`（DeferredTiler tiler）(偏移: 0x0)
- `NativeArray<DeferredTiler.PrePunctualLight> prePunctualLights`（NativeArray<DeferredTiler.PrePunctualLight> prePunctualLights）(偏移: 0x68)
- `NativeArray<ushort> coarseTiles`（NativeArray<ushort> coarseTiles）(偏移: 0x74)
- `NativeArray<uint> coarseTileHeaders`（NativeArray<uint> coarseTileHeaders）(偏移: 0x80)
- `int coarseHeaderOffset`（int coarse标题Offset）(偏移: 0x8C)
- `int istart`（int istart）(偏移: 0x90)
- `int iend`（int iend）(偏移: 0x94)
- `int jstart`（int jstart）(偏移: 0x98)
- `int jend`（int jend）(偏移: 0x9C)

### 方法 (1)

- `void Execute()`
  （void 执行（））

---

## DeferredLights.DrawCall（DeferredLights.DrawCall）

### 字段 (8)

- `ComputeBuffer tileList`（Compute缓冲区 tile列表）(偏移: 0x0)
- `ComputeBuffer punctualLightBuffer`（Compute缓冲区 punctual光照缓冲区）(偏移: 0x4)
- `ComputeBuffer relLightList`（Compute缓冲区 rel光照列表）(偏移: 0x8)
- `int tileListSize`（int tile列表大小）(偏移: 0xC)
- `int punctualLightBufferSize`（int punctual光照缓冲区大小）(偏移: 0x10)
- `int relLightListSize`（int rel光照列表大小）(偏移: 0x14)
- `int instanceOffset`（int instanceOffset）(偏移: 0x18)
- `int instanceCount`（int instance数量）(偏移: 0x1C)

---

## DeferredLights.GBufferHandles（DeferredLights.G缓冲区Handles）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DeferredLights.ShaderConstants（DeferredLights.着色器Constants）

### 字段 (62)

- `int _LitStencilRef`（int _LitStencilRef）(偏移: 0x0)
- `int _LitStencilReadMask`（int _LitStencilRead掩码）(偏移: 0x4)
- `int _LitStencilWriteMask`（int _LitStencilWrite掩码）(偏移: 0x8)
- `int _SimpleLitStencilRef`（int _SimpleLitStencilRef）(偏移: 0xC)
- `int _SimpleLitStencilReadMask`（int _SimpleLitStencilRead掩码）(偏移: 0x10)
- `int _SimpleLitStencilWriteMask`（int _SimpleLitStencilWrite掩码）(偏移: 0x14)
- `int _StencilRef`（int _StencilRef）(偏移: 0x18)
- `int _StencilReadMask`（int _StencilRead掩码）(偏移: 0x1C)
- `int _StencilWriteMask`（int _StencilWrite掩码）(偏移: 0x20)
- `int _LitPunctualStencilRef`（int _LitPunctualStencilRef）(偏移: 0x24)
- `int _LitPunctualStencilReadMask`（int _LitPunctualStencilRead掩码）(偏移: 0x28)
- `int _LitPunctualStencilWriteMask`（int _LitPunctualStencilWrite掩码）(偏移: 0x2C)
- `int _SimpleLitPunctualStencilRef`（int _SimpleLitPunctualStencilRef）(偏移: 0x30)
- `int _SimpleLitPunctualStencilReadMask`（int _SimpleLitPunctualStencilRead掩码）(偏移: 0x34)
- `int _SimpleLitPunctualStencilWriteMask`（int _SimpleLitPunctualStencilWrite掩码）(偏移: 0x38)
- `int _LitDirStencilRef`（int _LitDirStencilRef）(偏移: 0x3C)
- `int _LitDirStencilReadMask`（int _LitDirStencilRead掩码）(偏移: 0x40)
- `int _LitDirStencilWriteMask`（int _LitDirStencilWrite掩码）(偏移: 0x44)
- `int _SimpleLitDirStencilRef`（int _SimpleLitDirStencilRef）(偏移: 0x48)
- `int _SimpleLitDirStencilReadMask`（int _SimpleLitDirStencilRead掩码）(偏移: 0x4C)
- `int _SimpleLitDirStencilWriteMask`（int _SimpleLitDirStencilWrite掩码）(偏移: 0x50)
- `int _ClearStencilRef`（int _清除StencilRef）(偏移: 0x54)
- `int _ClearStencilReadMask`（int _清除StencilRead掩码）(偏移: 0x58)
- `int _ClearStencilWriteMask`（int _清除StencilWrite掩码）(偏移: 0x5C)
- `int UDepthRanges`（int U深度Ranges）(偏移: 0x60)
- `int _DepthRanges`（int _深度Ranges）(偏移: 0x64)
- `int _DownsamplingWidth`（int _Downsampling宽度）(偏移: 0x68)
- `int _DownsamplingHeight`（int _Downsampling高度）(偏移: 0x6C)
- `int _SourceShiftX`（int _SourceShiftX）(偏移: 0x70)
- `int _SourceShiftY`（int _SourceShiftY）(偏移: 0x74)
- `int _TileShiftX`（int _TileShiftX）(偏移: 0x78)
- `int _TileShiftY`（int _TileShiftY）(偏移: 0x7C)
- `int _tileXCount`（int _tileX数量）(偏移: 0x80)
- `int _DepthRangeOffset`（int _深度范围Offset）(偏移: 0x84)
- `int _BitmaskTex`（int _BitmaskTex）(偏移: 0x88)
- `int UTileList`（int UTile列表）(偏移: 0x8C)
- `int _TileList`（int _Tile列表）(偏移: 0x90)
- `int UPunctualLightBuffer`（int UPunctual光照缓冲区）(偏移: 0x94)
- `int _PunctualLightBuffer`（int _Punctual光照缓冲区）(偏移: 0x98)
- `int URelLightList`（int URel光照列表）(偏移: 0x9C)
- `int _RelLightList`（int _Rel光照列表）(偏移: 0xA0)
- `int _TilePixelWidth`（int _TilePixel宽度）(偏移: 0xA4)
- `int _TilePixelHeight`（int _TilePixel高度）(偏移: 0xA8)
- `int _InstanceOffset`（int _实例Offset）(偏移: 0xAC)
- `int _DepthTex`（int _深度Tex）(偏移: 0xB0)
- `int _DepthTexSize`（int _深度Tex大小）(偏移: 0xB4)
- `int _ScreenSize`（int _屏幕的大小）(偏移: 0xB8)
- `int _ScreenToWorld`（int _屏幕的To世界的）(偏移: 0xBC)
- `int _unproject0`（int _unproject0）(偏移: 0xC0)
- `int _unproject1`（int _unproject1）(偏移: 0xC4)
- `int _MainLightPosition`（int _主要的光照Position）(偏移: 0xC8)
- `int _MainLightColor`（int _主要的光照颜色）(偏移: 0xCC)
- `int _SpotLightScale`（int _Spot光照缩放）(偏移: 0xD0)
- `int _SpotLightBias`（int _Spot光照Bias）(偏移: 0xD4)
- `int _SpotLightGuard`（int _Spot光照Guard）(偏移: 0xD8)
- `int _LightPosWS`（int _光照PosWS）(偏移: 0xDC)
- `int _LightColor`（int _光照颜色）(偏移: 0xE0)
- `int _LightAttenuation`（int _光照Attenuation）(偏移: 0xE4)
- `int _LightOcclusionProbInfo`（int _光照OcclusionProb信息）(偏移: 0xE8)
- `int _LightDirection`（int _光照方向）(偏移: 0xEC)
- `int _LightFlags`（int _光照Flags）(偏移: 0xF0)
- `int _ShadowLightIndex`（int _Shadow光照索引）(偏移: 0xF4)

---

## DeferredPass（DeferredPass）

**继承**: ScriptableRenderPass（可脚本化渲染通道）

### 字段 (1)

- `DeferredLights m_DeferredLights`（DeferredLights m_DeferredLights）(偏移: 0x54)

### 方法 (3)

- `void Configure(CommandBuffer cmd, RenderTextureDescriptor cameraTextureDescripor)`
  （void Configure（Command缓冲区 cmd, Render纹理Descriptor cameraTextureDescripor））
- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（可脚本化渲染上下文 context, 引用 渲染数据 renderingData））
- `void OnCameraCleanup(CommandBuffer cmd)`
  （void 摄像机清理时（命令缓冲区 cmd））

---

## DeferredShaderData（Deferred着色器数据）

**继承**: IDisposable（可释放接口）

### 字段 (7)

- `DeferredShaderData m_Instance`（Deferred着色器数据 m_实例）(偏移: 0x0)
- `NativeArray<PreTile>[] m_PreTiles`（NativeArray<PreTile>[] m_PreTiles）(偏移: 0x8)
- `ComputeBuffer[] m_Buffers`（ComputeBuffer[] m_Buffers）(偏移: 0xC)
- `DeferredShaderData.ComputeBufferInfo[] m_BufferInfos`（Deferred着色器Data.Compute缓冲区Info[] m_缓冲区Infos）(偏移: 0x10)
- `int m_BufferCount`（int m_缓冲区数量）(偏移: 0x14)
- `int m_CachedBufferIndex`（int m_Cached缓冲区索引）(偏移: 0x18)
- `uint m_FrameIndex`（uint m_Frame索引）(偏移: 0x1C)

### 方法 (8)

- `DeferredShaderData get_instance()`
  （Deferred着色器数据 get_instance（））
- `void Dispose()`
  （void 释放（））
- `void ResetBuffers()`
  （void 重置Buffers（））
- `NativeArray<PreTile> GetPreTiles(int level, int count)`
  （NativeArray<PreTile> 获取PreTiles（int level, int count））
- `ComputeBuffer GetOrUpdateBuffer(int count, int stride, bool isConstantBuffer)`
  （Compute缓冲区 获取Or更新缓冲区（int count, int stride, bool isConstantBuffer））
- `void DisposeBuffers(ComputeBuffer[,] buffers)`
  （void 释放Buffers（ComputeBuffer[, ] buffers））
- `bool IsLessCircular(uint a, uint b)`
  （bool 是否LessCircular（uint a, uint b））
- `int Align(int s, int alignment)`
  （int Align（int s, int alignment））

---

## DeferredShaderData.ComputeBufferInfo（Deferred着色器Data.Compute缓冲区信息）

### 字段 (2)

- `uint frameUsed`（uint frameUsed）(偏移: 0x0)
- `ComputeBufferType type`（Compute缓冲区类型 type）(偏移: 0x4)

---

## DeferredTiler（DeferredTiler）

### 字段 (13)

- `int m_TilePixelWidth`（int m_TilePixel宽度）(偏移: 0x0)
- `int m_TilePixelHeight`（int m_TilePixel高度）(偏移: 0x4)
- `int m_TileXCount`（int m_TileX数量）(偏移: 0x8)
- `int m_TileYCount`（int m_TileY数量）(偏移: 0xC)
- `int m_TileHeaderSize`（int m_Tile标题大小）(偏移: 0x10)
- `int m_AvgLightPerTile`（int m_Avg光照PerTile）(偏移: 0x14)
- `int m_TilerLevel`（int m_Tiler等级）(偏移: 0x18)
- `FrustumPlanes m_FrustumPlanes`（FrustumPlanes m_FrustumPlanes）(偏移: 0x1C)
- `bool m_IsOrthographic`（bool m_是否Orthographic）(偏移: 0x34)
- `NativeArray<int> m_Counters`（NativeArray<int> m_Counters）(偏移: 0x38)
- `NativeArray<ushort> m_TileData`（NativeArray<ushort> m_Tile数据）(偏移: 0x44)
- `NativeArray<uint> m_TileHeaders`（NativeArray<uint> m_TileHeaders）(偏移: 0x50)
- `NativeArray<PreTile> m_PreTiles`（NativeArray<PreTile> m_PreTiles）(偏移: 0x5C)

### 方法 (30)

- `int get_TilerLevel()`
  （int get_Tiler等级（））
- `int get_TileXCount()`
  （int get_TileX数量（））
- `int get_TileYCount()`
  （int get_TileY数量（））
- `int get_TilePixelWidth()`
  （int get_TilePixel宽度（））
- `int get_TilePixelHeight()`
  （int get_TilePixel高度（））
- `int get_TileHeaderSize()`
  （int get_Tile标题大小（））
- `int get_MaxLightPerTile()`
  （int get_最大光照PerTile（））
- `int get_TileDataCapacity()`
  （int get_Tile数据Capacity（））
- `NativeArray<ushort> get_Tiles()`
  （NativeArray<ushort> get_Tiles（））
- `NativeArray<uint> get_TileHeaders()`
  （NativeArray<uint> get_TileHeaders（））
- `void GetTileOffsetAndCount(int i, int j, out int offset, out int count)`
  （void 获取TileOffsetAnd数量（int i, int j, out int offset, out int count））
- `int GetTileHeaderOffset(int i, int j)`
  （int 获取Tile标题Offset（int i, int j））
- `void Setup(int tileDataCapacity)`
  （void Setup（int tileDataCapacity））
- `void OnCameraCleanup()`
  （void On摄像机清理（））
- `void PrecomputeTiles(Matrix4x4 proj, bool isOrthographic, int renderWidth, int renderHeight)`
  （void PrecomputeTiles（Matrix4x4 proj, bool isOrthographic, int renderWidth, int renderHeight））
- `void CullFinalLights(ref NativeArray<DeferredTiler.PrePunctualLight> punctualLights, ref NativeArray<ushort> lightIndices, int lightStartIndex, int lightCount, int istart, int iend, int jstart, int jend)`
  （void CullFinalLights（ref NativeArray<DeferredTiler.PrePunctualLight> punctualLights, ref NativeArray<ushort> lightIndices, int lightStartIndex, int lightCount, int istart, int iend, int jstart, int jend））
- `void CullIntermediateLights(ref NativeArray<DeferredTiler.PrePunctualLight> punctualLights, ref NativeArray<ushort> lightIndices, int lightStartIndex, int lightCount, int istart, int iend, int jstart, int jend)`
  （void CullIntermediateLights（ref NativeArray<DeferredTiler.PrePunctualLight> punctualLights, ref NativeArray<ushort> lightIndices, int lightStartIndex, int lightCount, int istart, int iend, int jstart, int jend））
- `int AddTileData(ushort* lightData, ref int size)`
  （int 添加Tile数据（ushort* lightData, ref int size））
- `bool IntersectionLineSphere(float3 centre, float radius, float3 raySource, float3 rayDirection, out float t0, out float t1)`
  （bool IntersectionLineSphere（float3 centre, float radius, float3 raySource, float3 rayDirection, out float t0, out float t1））
- `bool Clip(ref PreTile tile, float3 posVS, float radius)`
  （bool 弹匣（ref PreTile tile, float3 posVS, float radius））
- `DeferredTiler.ClipResult ClipPartial(float4 plane, float4 sidePlaneA, float4 sidePlaneB, float3 posVS, float radius, float radiusSq, ref int insideCount)`
  （DeferredTiler.弹匣Result 弹匣Partial（float4 plane, float4 sidePlaneA, float4 sidePlaneB, float3 posVS, float radius, float radiusSq, ref int insideCount））
- `float4 MakePlane(float3 pb, float3 pc)`
  （float4 MakePlane（float3 pb, float3 pc））
- `float4 MakePlane(float3 pa, float3 pb, float3 pc)`
  （float4 MakePlane（float3 pa, float3 pb, float3 pc））
- `float DistanceToPlane(float4 plane, float3 p)`
  （float 距离ToPlane（float4 plane, float3 p））
- `float SignedSq(float f)`
  （float SignedSq（float f））
- `float min2(float a, float b)`
  （float min2（float a, float b））
- `float max2(float a, float b)`
  （float max2（float a, float b））
- `float max3(float a, float b, float c)`
  （float max3（float a, float b, float c））
- `uint _f32tof16(float x)`
  （uint _f32tof16（float x））
- `int Align(int s, int alignment)`
  （int Align（int s, int alignment））

---

## DeferredTiler.ClipResult（DeferredTiler.弹匣Result）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DeferredTiler.PrePunctualLight（DeferredTiler.PrePunctual光照）

### 字段 (5)

- `float3 posVS`（float3 posVS）(偏移: 0x0)
- `float radius`（浮点数 半径）(偏移: 0xC)
- `float minDist`（float minDist）(偏移: 0x10)
- `float2 screenPos`（float2 screenPos）(偏移: 0x14)
- `ushort visLightIndex`（ushort vis光照索引）(偏移: 0x1C)

---

## DeflateFlavor（DeflateFlavor）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DeflateManager（Deflate管理器）

### 字段 (74)

- `int MEM_LEVEL_MAX`（int MEM_LEVEL_MAX）(偏移: 0x0)
- `int MEM_LEVEL_DEFAULT`（int MEM_LEVEL_DEFAULT）(偏移: 0x4)
- `DeflateManager.CompressFunc DeflateFunction`（DeflateManager.CompressFunc DeflateFunction）(偏移: 0x8)
- `string[] _ErrorMessage`（string[] _ErrorMessage）(偏移: 0x8)
- `int PRESET_DICT`（int PRESET_DICT）(偏移: 0xC)
- `int INIT_STATE`（int INIT_STATE）(偏移: 0x10)
- `int BUSY_STATE`（int BUSY_STATE）(偏移: 0x14)
- `int FINISH_STATE`（int FINISH_STATE）(偏移: 0x18)
- `int Z_DEFLATED`（int Z_DEFLATED）(偏移: 0x1C)
- `int STORED_BLOCK`（int STORED_BLOCK）(偏移: 0x20)
- `int STATIC_TREES`（int STATIC_TREES）(偏移: 0x24)
- `int DYN_TREES`（int DYN_TREES）(偏移: 0x28)
- `int Z_BINARY`（int Z_BINARY）(偏移: 0x2C)
- `int Z_ASCII`（int Z_ASCII）(偏移: 0x30)
- `int Z_UNKNOWN`（int Z_UNKNOWN）(偏移: 0x34)
- `int Buf_size`（int Buf_size）(偏移: 0x38)
- `int MIN_MATCH`（int MIN_MATCH）(偏移: 0x3C)
- `int MAX_MATCH`（int MAX_MATCH）(偏移: 0x40)
- `int MIN_LOOKAHEAD`（int MIN_LOOKAHEAD）(偏移: 0x44)
- `int HEAP_SIZE`（int HEAP_SIZE）(偏移: 0x48)
- `int END_BLOCK`（int END_BLOCK）(偏移: 0x4C)
- `ZlibCodec _codec`（ZlibCodec _codec）(偏移: 0xC)
- `int status`（int status）(偏移: 0x10)
- `byte[] pending`（byte[] pending）(偏移: 0x14)
- `int nextPending`（int nextPending）(偏移: 0x18)
- `int pendingCount`（int pending数量）(偏移: 0x1C)
- `sbyte data_type`（sbyte data_type）(偏移: 0x20)
- `int last_flush`（int last_flush）(偏移: 0x24)
- `int w_size`（int w_size）(偏移: 0x28)
- `int w_bits`（int w_bits）(偏移: 0x2C)
- `int w_mask`（int w_mask）(偏移: 0x30)
- `byte[] window`（byte[] window）(偏移: 0x34)
- `int window_size`（int window_size）(偏移: 0x38)
- `short[] prev`（short[] prev）(偏移: 0x3C)
- `short[] head`（short[] head）(偏移: 0x40)
- `int ins_h`（int ins_h）(偏移: 0x44)
- `int hash_size`（int hash_size）(偏移: 0x48)
- `int hash_bits`（int hash_bits）(偏移: 0x4C)
- `int hash_mask`（int hash_mask）(偏移: 0x50)
- `int hash_shift`（int hash_shift）(偏移: 0x54)
- `int block_start`（int block_start）(偏移: 0x58)
- `DeflateManager.Config config`（DeflateManager.配置 config）(偏移: 0x5C)
- `int match_length`（int match_length）(偏移: 0x60)
- `int prev_match`（int prev_match）(偏移: 0x64)
- `int match_available`（int match_available）(偏移: 0x68)
- `int strstart`（int strstart）(偏移: 0x6C)
- `int match_start`（int match_start）(偏移: 0x70)
- `int lookahead`（int lookahead）(偏移: 0x74)
- `int prev_length`（int prev_length）(偏移: 0x78)
- `CompressionLevel compressionLevel`（Compression等级 compression等级）(偏移: 0x7C)
- `CompressionStrategy compressionStrategy`（CompressionStrategy compressionStrategy）(偏移: 0x80)
- `short[] dyn_ltree`（short[] dyn_ltree）(偏移: 0x84)
- `short[] dyn_dtree`（short[] dyn_dtree）(偏移: 0x88)
- `short[] bl_tree`（short[] bl_tree）(偏移: 0x8C)
- `Tree treeLiterals`（Tree treeLiterals）(偏移: 0x90)
- `Tree treeDistances`（Tree treeDistances）(偏移: 0x94)
- `Tree treeBitLengths`（Tree treeBitLengths）(偏移: 0x98)
- `short[] bl_count`（short[] bl_count）(偏移: 0x9C)
- `int[] heap`（int[] heap）(偏移: 0xA0)
- `int heap_len`（int heap_len）(偏移: 0xA4)
- `int heap_max`（int heap_max）(偏移: 0xA8)
- `sbyte[] depth`（sbyte[] depth）(偏移: 0xAC)
- `int _lengthOffset`（int _lengthOffset）(偏移: 0xB0)
- `int lit_bufsize`（int lit_bufsize）(偏移: 0xB4)
- `int last_lit`（int last_lit）(偏移: 0xB8)
- `int _distanceOffset`（int _distanceOffset）(偏移: 0xBC)
- `int opt_len`（int opt_len）(偏移: 0xC0)
- `int static_len`（int static_len）(偏移: 0xC4)
- `int matches`（int matches）(偏移: 0xC8)
- `int last_eob_len`（int last_eob_len）(偏移: 0xCC)
- `short bi_buf`（short bi_buf）(偏移: 0xD0)
- `int bi_valid`（int bi_valid）(偏移: 0xD4)
- `bool Rfc1950BytesEmitted`（bool Rfc1950BytesEmitted）(偏移: 0xD8)
- `bool _WantRfc1950HeaderBytes`（bool _想要Rfc1950标题Bytes）(偏移: 0xD9)

### 方法 (34)

- `void _InitializeLazyMatch()`
  （void _初始化Lazy比赛（））
- `void _InitializeTreeData()`
  （void _初始化Tree数据（））
- `void _InitializeBlocks()`
  （void _初始化Blocks（））
- `void pqdownheap(short[] tree, int k)`
  （void pqdownheap（short[] tree, int k））
- `bool _IsSmaller(short[] tree, int n, int m, sbyte[] depth)`
  （bool _是否Smaller（short[] tree, int n, int m, sbyte[] depth））
- `void scan_tree(short[] tree, int max_code)`
  （void scan_tree（short[] tree, int max_code））
- `int build_bl_tree()`
  （int build_bl_tree（））
- `void send_all_trees(int lcodes, int dcodes, int blcodes)`
  （void send_all_trees（int lcodes, int dcodes, int blcodes））
- `void send_tree(short[] tree, int max_code)`
  （void send_tree（short[] tree, int max_code））
- `void put_bytes(byte[] p, int start, int len)`
  （void put_bytes（byte[] p, int start, int len））
- `void send_code(int c, short[] tree)`
  （void send_code（int c, short[] tree））
- `void send_bits(int value, int length)`
  （void send_bits（int value, int length））
- `void _tr_align()`
  （void _tr_align（））
- `bool _tr_tally(int dist, int lc)`
  （bool _tr_tally（int dist, int lc））
- `void send_compressed_block(short[] ltree, short[] dtree)`
  （void send_compressed_block（short[] ltree, short[] dtree））
- `void set_data_type()`
  （void set_data_type（））
- `void bi_flush()`
  （void bi_flush（））
- `void bi_windup()`
  （void bi_windup（））
- `void copy_block(int buf, int len, bool header)`
  （void copy_block（int buf, int len, bool header））
- `void flush_block_only(bool eof)`
  （void flush_block_only（bool eof））
- `BlockState DeflateNone(FlushType flush)`
  （Block状态 Deflate无（Flush类型 flush））
- `void _tr_stored_block(int buf, int stored_len, bool eof)`
  （void _tr_stored_block（int buf, int stored_len, bool eof））
- `void _tr_flush_block(int buf, int stored_len, bool eof)`
  （void _tr_flush_block（int buf, int stored_len, bool eof））
- `void _fillWindow()`
  （void _fillWindow（））
- `BlockState DeflateFast(FlushType flush)`
  （Block状态 DeflateFast（Flush类型 flush））
- `BlockState DeflateSlow(FlushType flush)`
  （Block状态 DeflateSlow（Flush类型 flush））
- `int longest_match(int cur_match)`
  （int longest_match（int cur_match））
- `bool get_WantRfc1950HeaderBytes()`
  （bool get_想要Rfc1950标题Bytes（））
- `void set_WantRfc1950HeaderBytes(bool value)`
  （void set_想要Rfc1950标题Bytes（bool value））
- `int Initialize(ZlibCodec codec, CompressionLevel level, int bits, CompressionStrategy compressionStrategy)`
  （int 初始化（ZlibCodec codec, Compression等级 level, int bits, CompressionStrategy compressionStrategy））
- `int Initialize(ZlibCodec codec, CompressionLevel level, int windowBits, int memLevel, CompressionStrategy strategy)`
  （int 初始化（ZlibCodec codec, Compression等级 level, int windowBits, int memLevel, CompressionStrategy strategy））
- `void Reset()`
  （void 重置（））
- `void SetDeflater()`
  （void 集合Deflater（））
- `int Deflate(FlushType flush)`
  （int Deflate（Flush类型 flush））

---

## DeflateManager.CompressFunc（DeflateManager.CompressFunc）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `BlockState Invoke(FlushType flush)`
  （Block状态 Invoke（Flush类型 flush））
- `IAsyncResult BeginInvoke(FlushType flush, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Flush类型 flush, 异步回调 callback, object object））
- `BlockState EndInvoke(IAsyncResult result)`
  （Block状态 结束Invoke（I异步Result result））

---

## DeflateManager.Config（DeflateManager.配置）

### 字段 (6)

- `int GoodLength`（int GoodLength）(偏移: 0x8)
- `int MaxLazy`（int 最大Lazy）(偏移: 0xC)
- `int NiceLength`（int NiceLength）(偏移: 0x10)
- `int MaxChainLength`（int 最大ChainLength）(偏移: 0x14)
- `DeflateFlavor Flavor`（DeflateFlavor Flavor）(偏移: 0x18)
- `DeflateManager.Config[] Table`（DeflateManager.Config[] Table）(偏移: 0x0)

### 方法 (1)

- `DeflateManager.Config Lookup(CompressionLevel level)`
  （DeflateManager.配置 Lookup（Compression等级 level））

---

## DeflateStream（Deflate流）

**继承**: Stream（流）

### 字段 (3)

- `ZlibBaseStream _baseStream`（Zlib基础流 _base流）(偏移: 0x14)
- `Stream _innerStream`（流 _内部流）(偏移: 0x18)
- `bool _disposed`（布尔值 _已释放）(偏移: 0x1C)

### 方法 (14)

- `void set_BufferSize(int value)`
  （void set_缓冲区大小（int value））
- `void set_Strategy(CompressionStrategy value)`
  （void set_Strategy（CompressionStrategy value））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
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
- `int Read(byte[] buffer, int offset, int count)`
  （整数 读取（字节[] buffer, 整数 offset, 整数 count））
- `long Seek(long offset, SeekOrigin origin)`
  （长整数 查找（长整数 offset, 查找起点 origin））
- `void SetLength(long value)`
  （void 设置_长度（长整数 value））
- `void Write(byte[] buffer, int offset, int count)`
  （void 写入（字节[] buffer, 整数 offset, 整数 count））

---

## DelaunayTriangle（DelaunayTriangle）

### 字段 (4)

- `FixedArray3<TriangulationPoint> Points`（固定Array3<TriangulationPoint> Points）(偏移: 0x8)
- `FixedArray3<DelaunayTriangle> Neighbors`（固定Array3<DelaunayTriangle> Neighbors）(偏移: 0x14)
- `FixedBitArray3 EdgeIsConstrained`（固定BitArray3 Edge是否Constrained）(偏移: 0x20)
- `FixedBitArray3 EdgeIsDelaunay`（固定BitArray3 Edge是否Delaunay）(偏移: 0x23)

### 方法 (27)

- `bool get_IsInterior()`
  （bool get_是否Interior（））
- `void set_IsInterior(bool value)`
  （void set_是否Interior（bool value））
- `int IndexOf(TriangulationPoint p)`
  （int 索引Of（TriangulationPoint p））
- `int IndexCCWFrom(TriangulationPoint p)`
  （int 索引CCWFrom（TriangulationPoint p））
- `bool Contains(TriangulationPoint p)`
  （bool Contains（TriangulationPoint p））
- `void MarkNeighbor(TriangulationPoint p1, TriangulationPoint p2, DelaunayTriangle t)`
  （void MarkNeighbor（TriangulationPoint p1, TriangulationPoint p2, DelaunayTriangle t））
- `void MarkNeighbor(DelaunayTriangle t)`
  （void MarkNeighbor（DelaunayTriangle t））
- `TriangulationPoint OppositePoint(DelaunayTriangle t, TriangulationPoint p)`
  （TriangulationPoint OppositePoint（DelaunayTriangle t, TriangulationPoint p））
- `DelaunayTriangle NeighborCWFrom(TriangulationPoint point)`
  （DelaunayTriangle NeighborCWFrom（TriangulationPoint point））
- `DelaunayTriangle NeighborCCWFrom(TriangulationPoint point)`
  （DelaunayTriangle NeighborCCWFrom（TriangulationPoint point））
- `DelaunayTriangle NeighborAcrossFrom(TriangulationPoint point)`
  （DelaunayTriangle NeighborAcrossFrom（TriangulationPoint point））
- `TriangulationPoint PointCCWFrom(TriangulationPoint point)`
  （TriangulationPoint PointCCWFrom（TriangulationPoint point））
- `TriangulationPoint PointCWFrom(TriangulationPoint point)`
  （TriangulationPoint PointCWFrom（TriangulationPoint point））
- `void RotateCW()`
  （void RotateCW（））
- `void Legalize(TriangulationPoint oPoint, TriangulationPoint nPoint)`
  （void Legalize（TriangulationPoint oPoint, TriangulationPoint nPoint））
- `string ToString()`
  （字符串 转字符串（））
- `void MarkConstrainedEdge(int index)`
  （void MarkConstrainedEdge（int index））
- `void MarkConstrainedEdge(TriangulationPoint p, TriangulationPoint q)`
  （void MarkConstrainedEdge（TriangulationPoint p, TriangulationPoint q））
- `int EdgeIndex(TriangulationPoint p1, TriangulationPoint p2)`
  （int Edge索引（TriangulationPoint p1, TriangulationPoint p2））
- `bool GetConstrainedEdgeCCW(TriangulationPoint p)`
  （bool 获取ConstrainedEdgeCCW（TriangulationPoint p））
- `bool GetConstrainedEdgeCW(TriangulationPoint p)`
  （bool 获取ConstrainedEdgeCW（TriangulationPoint p））
- `void SetConstrainedEdgeCCW(TriangulationPoint p, bool ce)`
  （void 集合ConstrainedEdgeCCW（TriangulationPoint p, bool ce））
- `void SetConstrainedEdgeCW(TriangulationPoint p, bool ce)`
  （void 集合ConstrainedEdgeCW（TriangulationPoint p, bool ce））
- `bool GetDelaunayEdgeCCW(TriangulationPoint p)`
  （bool 获取DelaunayEdgeCCW（TriangulationPoint p））
- `bool GetDelaunayEdgeCW(TriangulationPoint p)`
  （bool 获取DelaunayEdgeCW（TriangulationPoint p））
- `void SetDelaunayEdgeCCW(TriangulationPoint p, bool ce)`
  （void 集合DelaunayEdgeCCW（TriangulationPoint p, bool ce））
- `void SetDelaunayEdgeCW(TriangulationPoint p, bool ce)`
  （void 集合DelaunayEdgeCW（TriangulationPoint p, bool ce））

---

## DelayOneShootData（延迟One射击数据）

### 字段 (3)

- `float timeMin`（float time最小）(偏移: 0x0)
- `float timeMax`（float time最大）(偏移: 0x4)
- `int shotCount`（int shot数量）(偏移: 0x8)

---

## Delegate（委托）

**继承**: ICloneable, ISerializable（ICloneable, ISerializable）

### 字段 (11)

- `IntPtr method_ptr`（整数Ptr method_ptr）(偏移: 0x8)
- `IntPtr invoke_impl`（整数Ptr invoke_impl）(偏移: 0xC)
- `object m_target`（object m_target）(偏移: 0x10)
- `IntPtr method`（整数Ptr method）(偏移: 0x14)
- `IntPtr delegate_trampoline`（整数Ptr delegate_trampoline）(偏移: 0x18)
- `IntPtr extra_arg`（整数Ptr extra_arg）(偏移: 0x1C)
- `IntPtr method_code`（整数Ptr method_code）(偏移: 0x20)
- `MethodInfo method_info`（Method信息 method_info）(偏移: 0x24)
- `MethodInfo original_method_info`（Method信息 original_method_info）(偏移: 0x28)
- `DelegateData data`（委托数据 data）(偏移: 0x2C)
- `bool method_is_virtual`（bool method_is_virtual）(偏移: 0x30)

### 方法 (33)

- `MethodInfo get_Method()`
  （Method信息 get_Method（））
- `MethodInfo GetVirtualMethod_internal()`
  （Method信息 获取虚拟的Method_internal（））
- `object get_Target()`
  （object get_目标（））
- `Delegate CreateDelegate_internal(Type type, object target, MethodInfo info, bool throwOnBindFailure)`
  （委托 创建Delegate_internal（类型 type, object target, Method信息 info, bool throwOnBindFailure））
- `bool arg_type_match(Type delArgType, Type argType)`
  （bool arg_type_match（类型 delArgType, 类型 argType））
- `bool arg_type_match_this(Type delArgType, Type argType, bool boxedThis)`
  （bool arg_type_match_this（类型 delArgType, 类型 argType, bool boxedThis））
- `bool return_type_match(Type delReturnType, Type returnType)`
  （bool return_type_match（类型 delReturnType, 类型 returnType））
- `Delegate CreateDelegate(Type type, object firstArgument, MethodInfo method, bool throwOnBindFailure)`
  （委托 创建委托（类型 type, object firstArgument, Method信息 method, bool throwOnBindFailure））
- `Delegate CreateDelegate(Type type, object firstArgument, MethodInfo method, bool throwOnBindFailure, bool allowClosed)`
  （委托 创建委托（类型 type, object firstArgument, Method信息 method, bool throwOnBindFailure, bool allowClosed））
- `Delegate CreateDelegate(Type type, object firstArgument, MethodInfo method)`
  （委托 创建委托（类型 type, object firstArgument, Method信息 method））
- `Delegate CreateDelegate(Type type, MethodInfo method, bool throwOnBindFailure)`
  （委托 创建委托（类型 type, Method信息 method, bool throwOnBindFailure））
- `Delegate CreateDelegate(Type type, MethodInfo method)`
  （委托 创建委托（类型 type, Method信息 method））
- `Delegate CreateDelegate(Type type, object target, string method)`
  （委托 创建委托（类型 type, object target, string method））
- `MethodInfo GetCandidateMethod(Type type, Type target, string method, BindingFlags bflags, bool ignoreCase, bool throwOnBindFailure)`
  （Method信息 获取CandidateMethod（类型 type, 类型 target, string method, BindingFlags bflags, bool ignoreCase, bool throwOnBindFailure））
- `Delegate CreateDelegate(Type type, Type target, string method, bool ignoreCase, bool throwOnBindFailure)`
  （委托 创建委托（类型 type, 类型 target, string method, bool ignoreCase, bool throwOnBindFailure））
- `Delegate CreateDelegate(Type type, Type target, string method)`
  （委托 创建委托（类型 type, 类型 target, string method））
- `Delegate CreateDelegate(Type type, object target, string method, bool ignoreCase, bool throwOnBindFailure)`
  （委托 创建委托（类型 type, object target, string method, bool ignoreCase, bool throwOnBindFailure））
- `Delegate CreateDelegate(Type type, object target, string method, bool ignoreCase)`
  （委托 创建委托（类型 type, object target, string method, bool ignoreCase））
- `object Clone()`
  （对象 克隆（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `MethodInfo GetMethodImpl()`
  （Method信息 获取MethodImpl（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））
- `Delegate[] GetInvocationList()`
  （Delegate[] 获取Invocation列表（））
- `Delegate Combine(Delegate a, Delegate b)`
  （委托 Combine（委托 a, 委托 b））
- `Delegate Combine(Delegate[] delegates)`
  （委托 Combine（Delegate[] delegates））
- `Delegate CombineImpl(Delegate d)`
  （委托 CombineImpl（委托 d））
- `Delegate Remove(Delegate source, Delegate value)`
  （委托 移除（委托 source, 委托 value））
- `Delegate RemoveImpl(Delegate d)`
  （委托 移除Impl（委托 d））
- `bool op_Equality(Delegate d1, Delegate d2)`
  （bool op_Equality（委托 d1, 委托 d2））
- `bool op_Inequality(Delegate d1, Delegate d2)`
  （bool op_Inequality（委托 d1, 委托 d2））
- `Delegate CreateDelegateNoSecurityCheck(RuntimeType type, object firstArgument, MethodInfo method)`
  （委托 创建委托NoSecurity检查（Runtime类型 type, object firstArgument, Method信息 method））
- `MulticastDelegate AllocDelegateLike_internal(Delegate d)`
  （Multicast委托 Alloc委托Like_internal（委托 d））

---

## DelegateData（委托数据）

### 字段 (3)

- `Type target_type`（类型 target_type）(偏移: 0x8)
- `string method_name`（string method_name）(偏移: 0xC)
- `bool curried_first_arg`（bool curried_first_arg）(偏移: 0x10)

---

## DelegateSerializationHolder（委托SerializationHolder）

**继承**: ISerializable, IObjectReference（ISerializable, I对象引用）

### 字段 (1)

- `Delegate _delegate`（委托 _delegate）(偏移: 0x8)

### 方法 (3)

- `void GetDelegateData(Delegate instance, SerializationInfo info, StreamingContext ctx)`
  （void 获取委托数据（委托 instance, Serialization信息 info, StreamingContext ctx））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））
- `object GetRealObject(StreamingContext context)`
  （对象 获取真实对象（流上下文 context））

---

## DelegateSerializationHolder.DelegateEntry（委托SerializationHolder.委托Entry）

### 字段 (7)

- `string type`（string type）(偏移: 0x8)
- `string assembly`（string assembly）(偏移: 0xC)
- `object target`（object target）(偏移: 0x10)
- `string targetTypeAssembly`（string target类型Assembly）(偏移: 0x14)
- `string targetTypeName`（string target类型名称）(偏移: 0x18)
- `string methodName`（string method名称）(偏移: 0x1C)
- `DelegateSerializationHolder.DelegateEntry delegateEntry`（委托SerializationHolder.委托Entry delegateEntry）(偏移: 0x20)

### 方法 (1)

- `Delegate DeserializeDelegate(SerializationInfo info, int index)`
  （委托 Deserialize委托（Serialization信息 info, int index））

---

## DelegateUtility（委托工具）

### 方法 (1)

- `Delegate Cast(Delegate source, Type type)`
  （委托 Cast（委托 source, 类型 type））

---

## DelegatingTypeDescriptionProvider（Delegating类型Description提供者）

**继承**: TypeDescriptionProvider（类型描述提供者）

### 字段 (1)

- `Type _type`（类型 _type）(偏移: 0x10)

### 方法 (8)

- `TypeDescriptionProvider get_Provider()`
  （类型Description提供者 get_提供者（））
- `object CreateInstance(IServiceProvider provider, Type objectType, Type[] argTypes, object[] args)`
  （对象 创建实例（I服务提供者 provider, 类型 objectType, 类型[] argTypes, 对象[] args））
- `IDictionary GetCache(object instance)`
  （I字典 获取缓存（对象 instance））
- `string GetFullComponentName(object component)`
  （字符串 获取完整组件名称（对象 component））
- `ICustomTypeDescriptor GetExtendedTypeDescriptor(object instance)`
  （I自定义的类型Descriptor 获取Extended类型Descriptor（object instance））
- `IExtenderProvider[] GetExtenderProviders(object instance)`
  （IExtenderProvider[] 获取ExtenderProviders（object instance））
- `Type GetReflectionType(Type objectType, object instance)`
  （类型 获取Reflection类型（类型 objectType, object instance））
- `ICustomTypeDescriptor GetTypeDescriptor(Type objectType, object instance)`
  （I自定义类型描述符 获取类型描述符（类型 objectType, 对象 instance））

---

## DemoGUIMessage（DemoGUIMessage）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (2)

- `string text`（字符串 文本）(偏移: 0xC)
- `Color color`（颜色 color）(偏移: 0x10)

### 方法 (1)

- `void OnGUI()`
  （void GUI时（））

---

## DepthAccess（深度Access）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DepthBits（深度Bits）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DepthNormalOnlyPass（深度法线OnlyPass）

**继承**: ScriptableRenderPass（可脚本化渲染通道）

### 字段 (2)

- `ShaderTagId m_ShaderTagId`（着色器标签Id m_着色器标签Id）(偏移: 0xFC)
- `FilteringSettings m_FilteringSettings`（过滤设置 m_过滤设置）(偏移: 0x100)

### 方法 (12)

- `RenderTextureDescriptor get_normalDescriptor()`
  （Render纹理Descriptor get_normalDescriptor（））
- `void set_normalDescriptor(RenderTextureDescriptor value)`
  （void set_normalDescriptor（Render纹理Descriptor value））
- `RenderTextureDescriptor get_depthDescriptor()`
  （Render纹理Descriptor get_depthDescriptor（））
- `void set_depthDescriptor(RenderTextureDescriptor value)`
  （void set_depthDescriptor（Render纹理Descriptor value））
- `RenderTargetHandle get_depthHandle()`
  （Render目标句柄 get_depth句柄（））
- `void set_depthHandle(RenderTargetHandle value)`
  （void set_depth句柄（Render目标句柄 value））
- `RenderTargetHandle get_normalHandle()`
  （Render目标句柄 get_normal句柄（））
- `void set_normalHandle(RenderTargetHandle value)`
  （void set_normal句柄（Render目标句柄 value））
- `void Setup(RenderTextureDescriptor baseDescriptor, RenderTargetHandle depthHandle, RenderTargetHandle normalHandle)`
  （void Setup（Render纹理Descriptor baseDescriptor, Render目标句柄 depthHandle, Render目标句柄 normalHandle））
- `void OnCameraSetup(CommandBuffer cmd, ref RenderingData renderingData)`
  （void 摄像机设置时（命令缓冲区 cmd, 引用 渲染数据 renderingData））
- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（可脚本化渲染上下文 context, 引用 渲染数据 renderingData））
- `void OnCameraCleanup(CommandBuffer cmd)`
  （void 摄像机清理时（命令缓冲区 cmd））

---

## DepthOfField（深度OfField）

**继承**: VolumeComponent, IPostProcessComponent（体积组件, I后处理组件）

### 字段 (11)

- `DepthOfFieldModeParameter mode`（深度OfField模式Parameter mode）(偏移: 0x1C)
- `MinFloatParameter gaussianStart`（最小浮点数Parameter gaussian开始）(偏移: 0x20)
- `MinFloatParameter gaussianEnd`（最小浮点数Parameter gaussian结束）(偏移: 0x24)
- `ClampedFloatParameter gaussianMaxRadius`（Clamped浮点数Parameter gaussian最大Radius）(偏移: 0x28)
- `BoolParameter highQualitySampling`（布尔值Parameter highQualitySampling）(偏移: 0x2C)
- `MinFloatParameter focusDistance`（最小浮点数Parameter focus距离）(偏移: 0x30)
- `ClampedFloatParameter aperture`（Clamped浮点数Parameter aperture）(偏移: 0x34)
- `ClampedFloatParameter focalLength`（Clamped浮点数Parameter focalLength）(偏移: 0x38)
- `ClampedIntParameter bladeCount`（Clamped整数Parameter blade数量）(偏移: 0x3C)
- `ClampedFloatParameter bladeCurvature`（Clamped浮点数Parameter bladeCurvature）(偏移: 0x40)
- `ClampedFloatParameter bladeRotation`（Clamped浮点数Parameter bladeRotation）(偏移: 0x44)

### 方法 (2)

- `bool IsActive()`
  （布尔值 是否激活的（））
- `bool IsTileCompatible()`
  （布尔值 是否瓦片兼容（））

---

## DepthOfFieldMode（深度OfField模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DepthOnlyPass（深度OnlyPass）

**继承**: ScriptableRenderPass（可脚本化渲染通道）

### 字段 (3)

- `int kDepthBufferBits`（int k深度缓冲区Bits）(偏移: 0x54)
- `FilteringSettings m_FilteringSettings`（过滤设置 m_过滤设置）(偏移: 0xAC)
- `ShaderTagId m_ShaderTagId`（着色器标签Id m_着色器标签Id）(偏移: 0xC4)

### 方法 (8)

- `RenderTargetHandle get_depthAttachmentHandle()`
  （Render目标句柄 get_depthAttachment句柄（））
- `void set_depthAttachmentHandle(RenderTargetHandle value)`
  （void set_depthAttachment句柄（Render目标句柄 value））
- `RenderTextureDescriptor get_descriptor()`
  （Render纹理Descriptor get_descriptor（））
- `void set_descriptor(RenderTextureDescriptor value)`
  （void set_descriptor（Render纹理Descriptor value））
- `void Setup(RenderTextureDescriptor baseDescriptor, RenderTargetHandle depthAttachmentHandle)`
  （void Setup（Render纹理Descriptor baseDescriptor, Render目标句柄 depthAttachmentHandle））
- `void OnCameraSetup(CommandBuffer cmd, ref RenderingData renderingData)`
  （void 摄像机设置时（命令缓冲区 cmd, 引用 渲染数据 renderingData））
- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（可脚本化渲染上下文 context, 引用 渲染数据 renderingData））
- `void OnCameraCleanup(CommandBuffer cmd)`
  （void 摄像机清理时（命令缓冲区 cmd））

---

## DepthState（深度状态）

**继承**: IEquatable<DepthState>（IEquatable<深度State>）

### 字段 (2)

- `byte m_WriteEnabled`（byte m_Write启用的）(偏移: 0x0)
- `sbyte m_CompareFunction`（sbyte m_CompareFunction）(偏移: 0x1)

### 方法 (4)

- `DepthState get_defaultValue()`
  （深度状态 get_default值（））
- `bool Equals(DepthState other)`
  （bool Equals（深度状态 other））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## DeserializationEventHandler（Deserialization事件处理器）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(object sender)`
  （void Invoke（object sender））
- `IAsyncResult BeginInvoke(object sender, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（object sender, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## DesignOnlyAttribute（DesignOnlyAttribute）

**继承**: Attribute（属性）

### 字段 (4)

- `bool isDesignOnly`（bool isDesignOnly）(偏移: 0x8)
- `DesignOnlyAttribute Yes`（DesignOnlyAttribute Yes）(偏移: 0x0)
- `DesignOnlyAttribute No`（DesignOnlyAttribute No）(偏移: 0x4)
- `DesignOnlyAttribute Default`（DesignOnlyAttribute 默认的）(偏移: 0x8)

### 方法 (4)

- `bool get_IsDesignOnly()`
  （bool get_是否DesignOnly（））
- `bool IsDefaultAttribute()`
  （布尔值 是否默认属性（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## DesignerAttribute（DesignerAttribute）

**继承**: Attribute（属性）

### 字段 (3)

- `string designerTypeName`（string designer类型名称）(偏移: 0x8)
- `string designerBaseTypeName`（string designer基础类型名称）(偏移: 0xC)
- `string typeId`（string typeId）(偏移: 0x10)

### 方法 (5)

- `string get_DesignerBaseTypeName()`
  （string get_Designer基础类型名称（））
- `string get_DesignerTypeName()`
  （string get_Designer类型名称（））
- `object get_TypeId()`
  （object get_类型Id（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## DetectorsExamples（DetectorsExamples）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (6)

- `bool injectionDetected`（bool injectionDetected）(偏移: 0xC)
- `bool speedHackDetected`（bool speedHackDetected）(偏移: 0xD)
- `bool wrongTimeDetected`（bool wrong时间Detected）(偏移: 0xE)
- `bool timeCheatingDetected`（bool timeCheatingDetected）(偏移: 0xF)
- `bool obscuredTypeCheatDetected`（bool obscured类型CheatDetected）(偏移: 0x10)
- `bool wallHackCheatDetected`（bool wallHackCheatDetected）(偏移: 0x11)

### 方法 (13)

- `void OnSpeedHackDetected()`
  （void OnSpeedHackDetected（））
- `void OnTimeCheatingDetected()`
  （void On时间CheatingDetected（））
- `void OnInjectionDetected()`
  （void OnInjectionDetected（））
- `void OnInjectionDetectedWithCause(string cause)`
  （void OnInjectionDetectedWithCause（string cause））
- `void OnObscuredTypeCheatingDetected()`
  （void On模糊的类型CheatingDetected（））
- `void OnWallHackDetected()`
  （void OnWallHackDetected（））
- `void OnTimeCheatChecked(TimeCheatingDetector.CheckResult checkResult, TimeCheatingDetector.ErrorKind errorKind)`
  （void On时间CheatChecked（时间CheatingDetector.检查Result checkResult, 时间CheatingDetector.ErrorKind errorKind））
- `void Start()`
  （void 开始（））
- `void SpeedHackDetectorExample()`
  （void SpeedHackDetectorExample（））
- `void InjectionDetectorExample()`
  （void InjectionDetectorExample（））
- `void ObscuredCheatingDetectorExample()`
  （void 模糊的CheatingDetectorExample（））
- `void TimeCheatingDetectorExample()`
  （void 时间CheatingDetectorExample（））
- `void ForceTimeCheatingDetectorCheck()`
  （void 强制时间CheatingDetector检查（））

---

## DeviceType（Device类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DiagnosticsConfigurationHandler（DiagnosticsConfiguration处理器）

**继承**: IConfigurationSectionHandler（IConfigurationSection处理器）

### 方法 (1)

- `object Create(object parent, object configContext, XmlNode section)`
  （object 创建（object parent, object configContext, Xml节点 section））

---

## DictationCompletionCause（DictationCompletionCause）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DictationRecognizer（DictationRecognizer）

### 字段 (5)

- `IntPtr m_Recognizer`（整数Ptr m_Recognizer）(偏移: 0x8)
- `DictationRecognizer.DictationHypothesisDelegate DictationHypothesis`（DictationRecognizer.DictationHypothesis委托 DictationHypothesis）(偏移: 0xC)
- `DictationRecognizer.DictationResultDelegate DictationResult`（DictationRecognizer.DictationResult委托 DictationResult）(偏移: 0x10)
- `DictationRecognizer.DictationCompletedDelegate DictationComplete`（DictationRecognizer.DictationCompleted委托 DictationComplete）(偏移: 0x14)
- `DictationRecognizer.DictationErrorHandler DictationError`（DictationRecognizer.DictationError处理器 DictationError）(偏移: 0x18)

### 方法 (4)

- `void DictationRecognizer_InvokeHypothesisGeneratedEvent(string keyword)`
  （void DictationRecognizer_InvokeHypothesisGenerated事件（string keyword））
- `void DictationRecognizer_InvokeResultGeneratedEvent(string keyword, ConfidenceLevel minimumConfidence)`
  （void DictationRecognizer_InvokeResultGenerated事件（string keyword, Confidence等级 minimumConfidence））
- `void DictationRecognizer_InvokeCompletedEvent(DictationCompletionCause cause)`
  （void DictationRecognizer_InvokeCompleted事件（DictationCompletionCause cause））
- `void DictationRecognizer_InvokeErrorEvent(string error, int hresult)`
  （void DictationRecognizer_InvokeError事件（string error, int hresult））

---

## DictationRecognizer.DictationCompletedDelegate（DictationRecognizer.DictationCompleted委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(DictationCompletionCause cause)`
  （void Invoke（DictationCompletionCause cause））
- `IAsyncResult BeginInvoke(DictationCompletionCause cause, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（DictationCompletionCause cause, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## DictationRecognizer.DictationErrorHandler（DictationRecognizer.DictationError处理器）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(string error, int hresult)`
  （void Invoke（string error, int hresult））
- `IAsyncResult BeginInvoke(string error, int hresult, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（string error, int hresult, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## DictationRecognizer.DictationHypothesisDelegate（DictationRecognizer.DictationHypothesis委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(string text)`
  （void Invoke（string text））
- `IAsyncResult BeginInvoke(string text, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（string text, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## DictationRecognizer.DictationResultDelegate（DictationRecognizer.DictationResult委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(string text, ConfidenceLevel confidence)`
  （void Invoke（string text, Confidence等级 confidence））
- `IAsyncResult BeginInvoke(string text, ConfidenceLevel confidence, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（string text, Confidence等级 confidence, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## DictionaryEntry（字典Entry）

### 字段 (2)

- `object _key`（object _key）(偏移: 0x0)
- `object _value`（object _value）(偏移: 0x4)

### 方法 (2)

- `object get_Key()`
  （对象 获取_键（））
- `object get_Value()`
  （对象 获取_值（））

---

## Direction（方向）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DirectionalLight（Directional光照）

### 字段 (9)

- `int instanceID`（整数 实例ID）(偏移: 0x0)
- `bool shadow`（布尔值 阴影）(偏移: 0x4)
- `LightMode mode`（光照模式 mode）(偏移: 0x5)
- `Vector3 position`（三维向量 位置）(偏移: 0x8)
- `Quaternion orientation`（四元数 朝向）(偏移: 0x14)
- `LinearColor color`（线性颜色 color）(偏移: 0x24)
- `LinearColor indirectColor`（线性颜色 间接颜色）(偏移: 0x34)
- `float penumbraWidthRadian`（float penumbra宽度Radian）(偏移: 0x44)
- `Vector3 direction`（三维向量 方向）(偏移: 0x48)

---

## DirectorWrapMode（DirectorWrap模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Directory（Directory）

### 方法 (16)

- `string[] GetFiles(string path)`
  （string[] 获取Files（string path））
- `string[] GetFiles(string path, string searchPattern)`
  （string[] 获取Files（string path, string searchPattern））
- `string[] InternalGetFiles(string path, string searchPattern, SearchOption searchOption)`
  （string[] 内部的获取Files（string path, string searchPattern, 搜索Option searchOption））
- `string[] GetDirectories(string path)`
  （string[] 获取Directories（string path））
- `string[] GetDirectories(string path, string searchPattern)`
  （string[] 获取Directories（string path, string searchPattern））
- `string[] InternalGetDirectories(string path, string searchPattern, SearchOption searchOption)`
  （string[] 内部的获取Directories（string path, string searchPattern, 搜索Option searchOption））
- `string[] InternalGetFileDirectoryNames(string path, string userPathOriginal, string searchPattern, bool includeFiles, bool includeDirs, SearchOption searchOption, bool checkHost)`
  （string[] 内部的获取文件DirectoryNames（string path, string userPathOriginal, string searchPattern, bool includeFiles, bool includeDirs, 搜索Option searchOption, bool checkHost））
- `DirectoryInfo CreateDirectory(string path)`
  （Directory信息 创建Directory（string path））
- `DirectoryInfo CreateDirectoriesInternal(string path)`
  （Directory信息 创建Directories内部的（string path））
- `void Delete(string path)`
  （void Delete（string path））
- `void RecursiveDelete(string path)`
  （void RecursiveDelete（string path））
- `void Delete(string path, bool recursive)`
  （void Delete（string path, bool recursive））
- `bool Exists(string path)`
  （bool Exists（string path））
- `string GetCurrentDirectory()`
  （string 获取当前Directory（））
- `string InsecureGetCurrentDirectory()`
  （string Insecure获取当前Directory（））
- `string GetDemandDir(string fullPath, bool thisDirOnly)`
  （string 获取DemandDir（string fullPath, bool thisDirOnly））

---

## Directory.SearchData（Directory.搜索数据）

### 字段 (3)

- `string fullPath`（string full路径）(偏移: 0x8)
- `string userPath`（string user路径）(偏移: 0xC)
- `SearchOption searchOption`（搜索Option searchOption）(偏移: 0x10)

---

## DirectoryInfo（Directory信息）

**继承**: FileSystemInfo（文件系统信息）

### 字段 (2)

- `string current`（string current）(偏移: 0x48)
- `string parent`（string parent）(偏移: 0x4C)

### 方法 (11)

- `void Initialize()`
  （void 初始化（））
- `bool get_Exists()`
  （bool get_Exists（））
- `string get_Name()`
  （字符串 获取_名称（））
- `DirectoryInfo get_Parent()`
  （Directory信息 get_父级（））
- `void Create()`
  （void 创建（））
- `FileInfo[] GetFiles()`
  （文件Info[] 获取Files（））
- `FileInfo[] GetFiles(string searchPattern)`
  （文件Info[] 获取Files（string searchPattern））
- `DirectoryInfo[] GetDirectories()`
  （DirectoryInfo[] 获取Directories（））
- `DirectoryInfo[] GetDirectories(string searchPattern)`
  （DirectoryInfo[] 获取Directories（string searchPattern））
- `string ToString()`
  （字符串 转字符串（））
- `void CheckPath(string path)`
  （void 检查路径（string path））

---

## DisableBatchingType（禁用Batching类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DiscLight（Disc光照）

### 字段 (10)

- `int instanceID`（整数 实例ID）(偏移: 0x0)
- `bool shadow`（布尔值 阴影）(偏移: 0x4)
- `LightMode mode`（光照模式 mode）(偏移: 0x5)
- `Vector3 position`（三维向量 位置）(偏移: 0x8)
- `Quaternion orientation`（四元数 朝向）(偏移: 0x14)
- `LinearColor color`（线性颜色 color）(偏移: 0x24)
- `LinearColor indirectColor`（线性颜色 间接颜色）(偏移: 0x34)
- `float range`（浮点数 范围）(偏移: 0x44)
- `float radius`（浮点数 半径）(偏移: 0x48)
- `FalloffType falloff`（衰减类型 falloff）(偏移: 0x4C)

---

## DiscreteTime（Discrete时间）

**继承**: IComparable（IComparable）

### 字段 (2)

- `DiscreteTime kMaxTime`（Discrete时间 k最大时间）(偏移: 0x0)
- `long m_DiscreteTime`（long m_Discrete时间）(偏移: 0x0)

### 方法 (22)

- `double get_tickValue()`
  （double get_tick值（））
- `DiscreteTime OneTickBefore()`
  （Discrete时间 OneTickBefore（））
- `DiscreteTime OneTickAfter()`
  （Discrete时间 OneTickAfter（））
- `DiscreteTime FromTicks(long ticks)`
  （Discrete时间 FromTicks（long ticks））
- `int CompareTo(object obj)`
  （整数 比较到（对象 obj））
- `bool Equals(DiscreteTime other)`
  （bool Equals（Discrete时间 other））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `long DoubleToDiscreteTime(double time)`
  （long DoubleToDiscrete时间（double time））
- `long IntToDiscreteTime(int time)`
  （long 整数ToDiscrete时间（int time））
- `double ToDouble(long time)`
  （double ToDouble（long time））
- `double op_Explicit(DiscreteTime b)`
  （double op_Explicit（Discrete时间 b））
- `DiscreteTime op_Explicit(double time)`
  （Discrete时间 op_Explicit（double time））
- `DiscreteTime op_Implicit(int time)`
  （Discrete时间 op_Implicit（int time））
- `bool op_Equality(DiscreteTime lhs, DiscreteTime rhs)`
  （bool op_Equality（Discrete时间 lhs, Discrete时间 rhs））
- `bool op_Inequality(DiscreteTime lhs, DiscreteTime rhs)`
  （bool op_Inequality（Discrete时间 lhs, Discrete时间 rhs））
- `bool op_LessThanOrEqual(DiscreteTime lhs, DiscreteTime rhs)`
  （bool op_LessThanOrEqual（Discrete时间 lhs, Discrete时间 rhs））
- `bool op_GreaterThanOrEqual(DiscreteTime lhs, DiscreteTime rhs)`
  （bool op_GreaterThanOrEqual（Discrete时间 lhs, Discrete时间 rhs））
- `DiscreteTime op_Subtraction(DiscreteTime lhs, DiscreteTime rhs)`
  （Discrete时间 op_Subtraction（Discrete时间 lhs, Discrete时间 rhs））
- `string ToString()`
  （字符串 转字符串（））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `DiscreteTime Max(DiscreteTime lhs, DiscreteTime rhs)`
  （Discrete时间 最大（Discrete时间 lhs, Discrete时间 rhs））
- `long GetNearestTick(double time)`
  （long 获取NearestTick（double time））

---

## DispIdAttribute（DispIdAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `int _val`（int _val）(偏移: 0x8)

---

## Display（Display）

### 字段 (5)

- `IntPtr nativeDisplay`（整数Ptr nativeDisplay）(偏移: 0x8)
- `Display[] displays`（Display[] displays）(偏移: 0x0)
- `Display _mainDisplay`（Display _mainDisplay）(偏移: 0x4)
- `int m_ActiveEditorGameViewTarget`（int m_激活的Editor游戏视图目标）(偏移: 0x8)
- `Display.DisplaysUpdatedDelegate onDisplaysUpdated`（Display.DisplaysUpdated委托 onDisplaysUpdated）(偏移: 0xC)

### 方法 (13)

- `int get_renderingWidth()`
  （int get_rendering宽度（））
- `int get_renderingHeight()`
  （int get_rendering高度（））
- `int get_systemWidth()`
  （int get_system宽度（））
- `int get_systemHeight()`
  （int get_system高度（））
- `bool get_requiresSrgbBlitToBackbuffer()`
  （bool get_requiresSrgbBlitToBackbuffer（））
- `Vector3 RelativeMouseAt(Vector3 inputMouseCoordinates)`
  （三维向量 Relative鼠标At（三维向量 inputMouseCoordinates））
- `Display get_main()`
  （Display get_main（））
- `void RecreateDisplayList(IntPtr[] nativeDisplay)`
  （void RecreateDisplay列表（整数Ptr[] nativeDisplay））
- `void FireDisplaysUpdated()`
  （void 开火DisplaysUpdated（））
- `void GetSystemExtImpl(IntPtr nativeDisplay, out int w, out int h)`
  （void 获取系统ExtImpl（整数Ptr nativeDisplay, out int w, out int h））
- `void GetRenderingExtImpl(IntPtr nativeDisplay, out int w, out int h)`
  （void 获取RenderingExtImpl（整数Ptr nativeDisplay, out int w, out int h））
- `int RelativeMouseAtImpl(int x, int y, out int rx, out int ry)`
  （int Relative鼠标AtImpl（int x, int y, out int rx, out int ry））
- `bool RequiresSrgbBlitToBackbufferImpl(IntPtr nativeDisplay)`
  （bool RequiresSrgbBlitToBackbufferImpl（整数Ptr nativeDisplay））

---

## Display.DisplaysUpdatedDelegate（Display.DisplaysUpdated委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke()`
  （void 调用（））
- `IAsyncResult BeginInvoke(AsyncCallback callback, object object)`
  （I异步结果 开始调用（异步回调 callback, 对象 object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## DisplayInfoAttribute（Display信息Attribute）

**继承**: Attribute（属性）

### 字段 (2)

- `string name`（字符串 名称）(偏移: 0x8)
- `int order`（int order）(偏移: 0xC)

---

## DisplayNameAttribute（Display名称Attribute）

**继承**: Attribute（属性）

### 字段 (2)

- `DisplayNameAttribute Default`（Display名称Attribute 默认的）(偏移: 0x0)
- `string _displayName`（string _display名称）(偏移: 0x8)

### 方法 (5)

- `string get_DisplayName()`
  （字符串 获取_显示名称（））
- `string get_DisplayNameValue()`
  （string get_Display名称值（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `bool IsDefaultAttribute()`
  （布尔值 是否默认属性（））

---

## DisposerReplySink（DisposerReplySink）

**继承**: IMessageSink（IMessage接收器）

### 字段 (2)

- `IMessageSink _next`（IMessageSink _next）(偏移: 0x8)
- `IDisposable _disposable`（IDisposable _disposable）(偏移: 0xC)

### 方法 (2)

- `IMessage SyncProcessMessage(IMessage msg)`
  （IMessage 同步处理消息（IMessage msg））
- `IMessageCtrl AsyncProcessMessage(IMessage msg, IMessageSink replySink)`
  （IMessageCtrl 异步处理消息（IMessage msg, IMessageSink replySink））

---

## DistanceMetric（距离Metric）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DistanceUse（距离Use）

**继承**: BotSkillBase（机器人技能基础）

### 字段 (2)

- `float minDis`（float minDis）(偏移: 0x18)
- `float maxDis`（float maxDis）(偏移: 0x1C)

### 方法 (1)

- `bool CanDo()`
  （布尔值 能否执行（））

---

## DllImportAttribute（DllImportAttribute）

**继承**: Attribute（属性）

### 字段 (9)

- `string _val`（string _val）(偏移: 0x8)
- `string EntryPoint`（string EntryPoint）(偏移: 0xC)
- `CharSet CharSet`（Char集合 Char集合）(偏移: 0x10)
- `bool SetLastError`（bool 集合最后一个Error）(偏移: 0x14)
- `bool ExactSpelling`（bool ExactSpelling）(偏移: 0x15)
- `bool PreserveSig`（bool PreserveSig）(偏移: 0x16)
- `CallingConvention CallingConvention`（CallingConvention CallingConvention）(偏移: 0x18)
- `bool BestFitMapping`（bool BestFitMapping）(偏移: 0x1C)
- `bool ThrowOnUnmappableChar`（bool 投掷OnUnmappableChar）(偏移: 0x1D)

### 方法 (3)

- `Attribute GetCustomAttribute(RuntimeMethodInfo method)`
  （Attribute 获取自定义的Attribute（RuntimeMethod信息 method））
- `bool IsDefined(RuntimeMethodInfo method)`
  （bool 是否Defined（RuntimeMethod信息 method））
- `string get_Value()`
  （字符串 获取_值（））

---

## DllImportSearchPath（DllImport搜索路径）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DocumentationSortingAttribute（DocumentationSortingAttribute）

**继承**: Attribute（属性）

### 方法 (2)

- `DocumentationSortingAttribute.Level get_Category()`
  （DocumentationSortingAttribute.等级 get_类别（））
- `void set_Category(DocumentationSortingAttribute.Level value)`
  （void set_类别（DocumentationSortingAttribute.等级 value））

---

## DocumentationSortingAttribute.Level（DocumentationSortingAttribute.等级）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DomainNameHelper（Domain名称辅助器）

### 方法 (11)

- `string ParseCanonicalName(string str, int start, int end, ref bool loopback)`
  （string 解析Canonical名称（string str, int start, int end, ref bool loopback））
- `bool IsValid(char* name, ushort pos, ref int returnedEnd, ref bool notCanonical, bool notImplicitFile)`
  （bool 是否Valid（char* name, ushort pos, ref int returnedEnd, ref bool notCanonical, bool notImplicitFile））
- `bool IsValidByIri(char* name, ushort pos, ref int returnedEnd, ref bool notCanonical, bool notImplicitFile)`
  （bool 是否ValidByIri（char* name, ushort pos, ref int returnedEnd, ref bool notCanonical, bool notImplicitFile））
- `string IdnEquivalent(char* hostname, int start, int end, ref bool allAscii, ref bool atLeastOneValidIdn)`
  （string IdnEquivalent（char* hostname, int start, int end, ref bool allAscii, ref bool atLeastOneValidIdn））
- `string IdnEquivalent(char* hostname, int start, int end, ref bool allAscii, ref string bidiStrippedHost)`
  （string IdnEquivalent（char* hostname, int start, int end, ref bool allAscii, ref string bidiStrippedHost））
- `bool IsIdnAce(string input, int index)`
  （bool 是否Idn王牌（string input, int index））
- `bool IsIdnAce(char* input, int index)`
  （bool 是否Idn王牌（char* input, int index））
- `string UnicodeEquivalent(string idnHost, char* hostname, int start, int end)`
  （string UnicodeEquivalent（string idnHost, char* hostname, int start, int end））
- `string UnicodeEquivalent(char* hostname, int start, int end, ref bool allAscii, ref bool atLeastOneValidIdn)`
  （string UnicodeEquivalent（char* hostname, int start, int end, ref bool allAscii, ref bool atLeastOneValidIdn））
- `bool IsASCIILetterOrDigit(char character, ref bool notCanonical)`
  （bool 是否ASCIILetterOrDigit（char character, ref bool notCanonical））
- `bool IsValidDomainLabelCharacter(char character, ref bool notCanonical)`
  （bool 是否ValidDomain标签角色（char character, ref bool notCanonical））

---

## DoorController（Door控制器）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (6)

- `bool open`（bool open）(偏移: 0xC)
- `int opentag`（int opentag）(偏移: 0x10)
- `int closedtag`（int closedtag）(偏移: 0x14)
- `bool updateGraphsWithGUO`（bool updateGraphsWithGUO）(偏移: 0x18)
- `float yOffset`（float yOffset）(偏移: 0x1C)
- `Bounds bounds`（边界 bounds）(偏移: 0x20)

### 方法 (3)

- `void Start()`
  （void 开始（））
- `void OnGUI()`
  （void GUI时（））
- `void SetState(bool open)`
  （void 集合状态（bool open））

---

## Double（Double）

**继承**: IComparable, IFormattable, IConvertible, IComparable<double>, IEquatable<double>（IComparable, IFormattable, IConvertible, IComparable<double>, IEquatable<double>）

### 字段 (2)

- `double m_value`（double m_value）(偏移: 0x0)
- `double NegativeZero`（double NegativeZero）(偏移: 0x0)

### 方法 (20)

- `bool IsInfinity(double d)`
  （bool 是否无限（double d））
- `bool IsPositiveInfinity(double d)`
  （bool 是否Positive无限（double d））
- `bool IsNaN(double d)`
  （bool 是否NaN（double d））
- `int CompareTo(object value)`
  （整数 比较到（对象 value））
- `int CompareTo(double value)`
  （int CompareTo（double value））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(double obj)`
  （bool Equals（double obj））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `string ToString()`
  （字符串 转字符串（））
- `string ToString(string format)`
  （字符串 转字符串（字符串 格式））
- `string ToString(IFormatProvider provider)`
  （字符串 转字符串（I格式化提供者 provider））
- `string ToString(string format, IFormatProvider provider)`
  （字符串 转字符串（字符串 格式, I格式化提供者 provider））
- `double Parse(string s)`
  （double 解析（string s））
- `double Parse(string s, IFormatProvider provider)`
  （double 解析（string s, I格式化提供者 provider））
- `double Parse(string s, NumberStyles style, IFormatProvider provider)`
  （double 解析（string s, NumberStyles style, I格式化提供者 provider））
- `double Parse(string s, NumberStyles style, NumberFormatInfo info)`
  （double 解析（string s, NumberStyles style, Number格式化信息 info））
- `bool TryParse(string s, out double result)`
  （bool Try解析（string s, out double result））
- `bool TryParse(string s, NumberStyles style, IFormatProvider provider, out double result)`
  （bool Try解析（string s, NumberStyles style, I格式化提供者 provider, out double result））
- `bool TryParse(string s, NumberStyles style, NumberFormatInfo info, out double result)`
  （bool Try解析（string s, NumberStyles style, Number格式化信息 info, out double result））
- `TypeCode GetTypeCode()`
  （类型代码 获取类型代码（））

---

## DoubleArrayTypeInfo（Double数组类型信息）

**继承**: TraceLoggingTypeInfo<double[]>（TraceLogging类型Info<double[]>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void 写入元数据（跟踪日志元数据收集器 collector, 字符串 name, 事件字段格式 format））
- `void WriteData(TraceLoggingDataCollector collector, ref double[] value)`
  （void Write数据（TraceLogging数据Collector collector, ref double[] value））

---

## DoubleConverter（DoubleConverter）

**继承**: BaseNumberConverter（基础数字转换器）

### 方法 (6)

- `bool get_AllowHex()`
  （布尔值 获取_允许十六进制（））
- `Type get_TargetType()`
  （类型 get_目标类型（））
- `object FromString(string value, int radix)`
  （对象 从字符串（字符串 value, 整数 radix））
- `object FromString(string value, NumberFormatInfo formatInfo)`
  （对象 从字符串（字符串 value, 数字格式信息 formatInfo））
- `object FromString(string value, CultureInfo culture)`
  （对象 从字符串（字符串 value, 区域性信息 culture））
- `string ToString(object value, NumberFormatInfo formatInfo)`
  （字符串 转字符串（对象 value, 数字格式信息 formatInfo））

---

## DoublePlugin（Double插件）

**继承**: ABSTweenPlugin<double, double, NoOptions>（ABSTweenPlugin<double, double, NoOptions>）

### 方法 (8)

- `void Reset(TweenerCore<double, double, NoOptions> t)`
  （void 重置（TweenerCore<double, double, NoOptions> t））
- `void SetFrom(TweenerCore<double, double, NoOptions> t, bool isRelative)`
  （void 集合From（TweenerCore<double, double, NoOptions> t, bool isRelative））
- `void SetFrom(TweenerCore<double, double, NoOptions> t, double fromValue, bool setImmediately, bool isRelative)`
  （void 集合From（TweenerCore<double, double, NoOptions> t, double fromValue, bool setImmediately, bool isRelative））
- `double ConvertToStartValue(TweenerCore<double, double, NoOptions> t, double value)`
  （double 转换To开始值（TweenerCore<double, double, NoOptions> t, double value））
- `void SetRelativeEndValue(TweenerCore<double, double, NoOptions> t)`
  （void 集合Relative结束值（TweenerCore<double, double, NoOptions> t））
- `void SetChangeValue(TweenerCore<double, double, NoOptions> t)`
  （void 集合Change值（TweenerCore<double, double, NoOptions> t））
- `float GetSpeedBasedDuration(NoOptions options, float unitsXSecond, double changeValue)`
  （float 获取SpeedBased持续时间（NoOptions options, float unitsXSecond, double changeValue））
- `void EvaluateAndApply(NoOptions options, Tween t, bool isRelative, DOGetter<double> getter, DOSetter<double> setter, float elapsed, double startValue, double changeValue, float duration, bool usingInversePosition, UpdateNotice updateNotice)`
  （void EvaluateAnd应用（NoOptions options, Tween t, bool isRelative, DOGetter<double> getter, DOSetter<double> setter, float elapsed, double startValue, double changeValue, float duration, bool usingInversePosition, 更新Notice updateNotice））

---

## DoubleTypeInfo（Double类型信息）

**继承**: TraceLoggingTypeInfo<double>（TraceLogging类型Info<double>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void 写入元数据（跟踪日志元数据收集器 collector, 字符串 name, 事件字段格式 format））
- `void WriteData(TraceLoggingDataCollector collector, ref double value)`
  （void Write数据（TraceLogging数据Collector collector, ref double value））

---

## DownloadHandler（Download处理器）

### 字段 (1)

- `IntPtr m_Ptr`（整数指针 m_指针）(偏移: 0x8)

### 方法 (4)

- `void Release()`
  （void 释放（））
- `void Dispose()`
  （void 释放（））
- `void ReceiveContentLengthHeader(ulong contentLength)`
  （void 接收ContentLength标题（ulong contentLength））
- `void ReceiveContentLength(int contentLength)`
  （void 接收ContentLength（int contentLength））

---

## Downsampling（Downsampling）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Draw（Draw）

### 字段 (4)

- `Draw Debug`（Draw Debug）(偏移: 0x0)
- `Draw Gizmos`（Draw Gizmos）(偏移: 0x4)
- `bool gizmos`（bool gizmos）(偏移: 0x8)
- `Matrix4x4 matrix`（Matrix4x4 matrix）(偏移: 0xC)

### 方法 (6)

- `void SetColor(Color color)`
  （void 集合颜色（颜色 color））
- `void Line(Vector3 a, Vector3 b, Color color)`
  （void Line（三维向量 a, 三维向量 b, 颜色 color））
- `void CircleXZ(Vector3 center, float radius, Color color, float startAngle = 0, float endAngle = 6.2831855)`
  （void CircleXZ（三维向量 center, float radius, 颜色 color, float startAngle = 0, float endAngle = 6.2831855））
- `void Cylinder(Vector3 position, Vector3 up, float height, float radius, Color color)`
  （void Cylinder（三维向量 position, 三维向量 up, float height, float radius, 颜色 color））
- `void CrossXZ(Vector3 position, Color color, float size = 1)`
  （void CrossXZ（三维向量 position, 颜色 color, float size = 1））
- `void Bezier(Vector3 a, Vector3 b, Color color)`
  （void Bezier（三维向量 a, 三维向量 b, 颜色 color））

---

## DrawObjectsPass（DrawObjectsPass）

**继承**: ScriptableRenderPass（可脚本化渲染通道）

### 字段 (7)

- `FilteringSettings m_FilteringSettings`（过滤设置 m_过滤设置）(偏移: 0x54)
- `RenderStateBlock m_RenderStateBlock`（Render状态Block m_Render状态Block）(偏移: 0x6C)
- `List<ShaderTagId> m_ShaderTagIdList`（List<着色器标签Id> m_着色器标签Id列表）(偏移: 0xD8)
- `string m_ProfilerTag`（string m_Profiler标签）(偏移: 0xDC)
- `ProfilingSampler m_ProfilingSampler`（性能分析采样器 m_性能分析采样器）(偏移: 0xE0)
- `bool m_IsOpaque`（bool m_是否不透明的）(偏移: 0xE4)
- `int s_DrawObjectPassDataPropID`（int s_Draw对象Pass数据PropID）(偏移: 0x0)

### 方法 (1)

- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（可脚本化渲染上下文 context, 引用 渲染数据 renderingData））

---

## DrawRendererFlags（Draw渲染器Flags）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DrawSkyboxPass（DrawSkyboxPass）

**继承**: ScriptableRenderPass（可脚本化渲染通道）

### 方法 (1)

- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（可脚本化渲染上下文 context, 引用 渲染数据 renderingData））

---

## DrawableDictionary（Drawable字典）

### 字段 (3)

- `ReorderableList reorderableList`（Reorderable列表 reorderable列表）(偏移: 0x8)
- `RequiredReferences reqReferences`（RequiredReferences reqReferences）(偏移: 0xC)
- `bool isExpanded`（bool isExpanded）(偏移: 0x10)

---

## DrawingSettings（DrawingSettings）

**继承**: IEquatable<DrawingSettings>（IEquatable<DrawingSettings>）

### 字段 (9)

- `int maxShaderPasses`（int max着色器Passes）(偏移: 0x0)
- `SortingSettings m_SortingSettings`（SortingSettings m_SortingSettings）(偏移: 0x0)
- `DrawingSettings.<shaderPassNames>e__FixedBuffer shaderPassNames`（DrawingSettings.<shaderPassNames>e__固定缓冲区 shaderPassNames）(偏移: 0xE0)
- `PerObjectData m_PerObjectData`（Per对象数据 m_Per对象数据）(偏移: 0x120)
- `DrawRendererFlags m_Flags`（Draw渲染器Flags m_Flags）(偏移: 0x124)
- `int m_OverrideMaterialInstanceId`（int m_重写材质实例Id）(偏移: 0x128)
- `int m_OverrideMaterialPassIndex`（int m_重写材质Pass索引）(偏移: 0x12C)
- `int m_MainLightIndex`（int m_主要的光照索引）(偏移: 0x130)
- `int m_UseSrpBatcher`（int m_UseSrpBatcher）(偏移: 0x134)

### 方法 (13)

- `SortingSettings get_sortingSettings()`
  （SortingSettings get_sortingSettings（））
- `void set_sortingSettings(SortingSettings value)`
  （void set_sortingSettings（SortingSettings value））
- `void set_perObjectData(PerObjectData value)`
  （void set_per对象数据（Per对象数据 value））
- `void set_enableDynamicBatching(bool value)`
  （void set_enable动态的Batching（bool value））
- `void set_enableInstancing(bool value)`
  （void set_enableInstancing（bool value））
- `void set_overrideMaterial(Material value)`
  （void set_override材质（材质 value））
- `void set_overrideMaterialPassIndex(int value)`
  （void set_override材质Pass索引（int value））
- `void set_mainLightIndex(int value)`
  （void set_main光照索引（int value））
- `ShaderTagId GetShaderPassName(int index)`
  （着色器标签Id 获取着色器Pass名称（int index））
- `void SetShaderPassName(int index, ShaderTagId shaderPassName)`
  （void 集合着色器Pass名称（int index, 着色器标签Id shaderPassName））
- `bool Equals(DrawingSettings other)`
  （bool Equals（DrawingSettings other））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## DrivenRectTransformTracker（DrivenRect变换Tracker）

### 方法 (2)

- `void Add(Object driver, RectTransform rectTransform, DrivenTransformProperties drivenProperties)`
  （void 添加（对象 driver, Rect变换 rectTransform, Driven变换Properties drivenProperties））
- `void Clear()`
  （void 清除（））

---

## DrivenTransformProperties（Driven变换Properties）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Dropdown（Dropdown）

**继承**: Selectable, IPointerClickHandler, IEventSystemHandler, ISubmitHandler, ICancelHandler（Selectable, I指针Click处理器, I事件系统处理器, ISubmit处理器, I取消处理器）

### 字段 (15)

- `RectTransform m_Template`（Rect变换 m_Template）(偏移: 0xB0)
- `Text m_CaptionText`（文本 m_Caption文本）(偏移: 0xB4)
- `Image m_CaptionImage`（图像 m_Caption图像）(偏移: 0xB8)
- `Text m_ItemText`（文本 m_项目文本）(偏移: 0xBC)
- `Image m_ItemImage`（图像 m_项目图像）(偏移: 0xC0)
- `int m_Value`（int m_值）(偏移: 0xC4)
- `Dropdown.OptionDataList m_Options`（Dropdown.Option数据列表 m_Options）(偏移: 0xC8)
- `Dropdown.DropdownEvent m_OnValueChanged`（Dropdown.Dropdown事件 m_On值Changed）(偏移: 0xCC)
- `float m_AlphaFadeSpeed`（float m_透明度FadeSpeed）(偏移: 0xD0)
- `GameObject m_Dropdown`（游戏对象 m_Dropdown）(偏移: 0xD4)
- `GameObject m_Blocker`（游戏对象 m_Blocker）(偏移: 0xD8)
- `List<Dropdown.DropdownItem> m_Items`（List<Dropdown.DropdownItem> m_Items）(偏移: 0xDC)
- `TweenRunner<FloatTween> m_AlphaTweenRunner`（TweenRunner<浮点数Tween> m_透明度TweenRunner）(偏移: 0xE0)
- `bool validTemplate`（bool validTemplate）(偏移: 0xE4)
- `Dropdown.OptionData s_NoOptionData`（Dropdown.Option数据 s_NoOption数据）(偏移: 0x0)

### 方法 (47)

- `RectTransform get_template()`
  （Rect变换 get_template（））
- `void set_template(RectTransform value)`
  （void set_template（Rect变换 value））
- `Text get_captionText()`
  （文本 get_caption文本（））
- `void set_captionText(Text value)`
  （void set_caption文本（文本 value））
- `Image get_captionImage()`
  （图像 get_caption图像（））
- `void set_captionImage(Image value)`
  （void set_caption图像（图像 value））
- `Text get_itemText()`
  （文本 get_item文本（））
- `void set_itemText(Text value)`
  （void set_item文本（文本 value））
- `Image get_itemImage()`
  （图像 get_item图像（））
- `void set_itemImage(Image value)`
  （void set_item图像（图像 value））
- `List<Dropdown.OptionData> get_options()`
  （List<Dropdown.OptionData> get_options（））
- `void set_options(List<Dropdown.OptionData> value)`
  （void set_options（List<Dropdown.OptionData> value））
- `Dropdown.DropdownEvent get_onValueChanged()`
  （Dropdown.Dropdown事件 get_on值Changed（））
- `void set_onValueChanged(Dropdown.DropdownEvent value)`
  （void set_on值Changed（Dropdown.Dropdown事件 value））
- `float get_alphaFadeSpeed()`
  （float get_alphaFadeSpeed（））
- `void set_alphaFadeSpeed(float value)`
  （void set_alphaFadeSpeed（float value））
- `int get_value()`
  （整数 获取_值（））
- `void set_value(int value)`
  （void 设置_值（整数 value））
- `void SetValueWithoutNotify(int input)`
  （void 集合值WithoutNotify（int input））
- `void Set(int value, bool sendCallback = True)`
  （void 集合（int value, bool sendCallback = True））
- `void Awake()`
  （void 唤醒（））
- `void Start()`
  （void 开始（））
- `void OnDisable()`
  （void 禁用时（））
- `void RefreshShownValue()`
  （void 刷新Shown值（））
- `void AddOptions(List<Dropdown.OptionData> options)`
  （void 添加Options（List<Dropdown.OptionData> options））
- `void AddOptions(List<string> options)`
  （void 添加Options（List<string> options））
- `void AddOptions(List<Sprite> options)`
  （void 添加Options（List<Sprite> options））
- `void ClearOptions()`
  （void 清除Options（））
- `void SetupTemplate(Canvas rootCanvas)`
  （void SetupTemplate（画布 rootCanvas））
- `void OnPointerClick(PointerEventData eventData)`
  （void 指针点击时（指针事件数据 eventData））
- `void OnSubmit(BaseEventData eventData)`
  （void 提交时（基础事件数据 eventData））
- `void OnCancel(BaseEventData eventData)`
  （void On取消（基础事件数据 eventData））
- `void Show()`
  （void 显示（））
- `GameObject CreateBlocker(Canvas rootCanvas)`
  （游戏对象 创建Blocker（画布 rootCanvas））
- `void DestroyBlocker(GameObject blocker)`
  （void 销毁Blocker（游戏对象 blocker））
- `GameObject CreateDropdownList(GameObject template)`
  （游戏对象 创建Dropdown列表（游戏对象 template））
- `void DestroyDropdownList(GameObject dropdownList)`
  （void 销毁Dropdown列表（游戏对象 dropdownList））
- `Dropdown.DropdownItem CreateItem(Dropdown.DropdownItem itemTemplate)`
  （Dropdown.Dropdown项目 创建项目（Dropdown.Dropdown项目 itemTemplate））
- `void DestroyItem(Dropdown.DropdownItem item)`
  （void 销毁项目（Dropdown.Dropdown项目 item））
- `Dropdown.DropdownItem AddItem(Dropdown.OptionData data, bool selected, Dropdown.DropdownItem itemTemplate, List<Dropdown.DropdownItem> items)`
  （Dropdown.Dropdown项目 添加项目（Dropdown.Option数据 data, bool selected, Dropdown.Dropdown项目 itemTemplate, List<Dropdown.DropdownItem> items））
- `void AlphaFadeList(float duration, float alpha)`
  （void 透明度Fade列表（float duration, float alpha））
- `void AlphaFadeList(float duration, float start, float end)`
  （void 透明度Fade列表（float duration, float start, float end））
- `void SetAlpha(float alpha)`
  （void 集合透明度（float alpha））
- `void Hide()`
  （void 隐藏（））
- `IEnumerator DelayedDestroyDropdownList(float delay)`
  （IEnumerator Delayed销毁Dropdown列表（float delay））
- `void ImmediateDestroyDropdownList()`
  （void Immediate销毁Dropdown列表（））
- `void OnSelectItem(Toggle toggle)`
  （void On选择项目（开关 toggle））

---

## Dropdown.DropdownItem（Dropdown.Dropdown项目）

**继承**: MonoBehaviour, IPointerEnterHandler, IEventSystemHandler, ICancelHandler（MonoBehaviour行为, I指针Enter处理器, I事件系统处理器, I取消处理器）

### 字段 (4)

- `Text m_Text`（文本 m_文本）(偏移: 0xC)
- `Image m_Image`（图像 m_图像）(偏移: 0x10)
- `RectTransform m_RectTransform`（Rect变换 m_Rect变换）(偏移: 0x14)
- `Toggle m_Toggle`（开关 m_开关）(偏移: 0x18)

### 方法 (10)

- `Text get_text()`
  （文本 get_text（））
- `void set_text(Text value)`
  （void set_text（文本 value））
- `Image get_image()`
  （图像 get_image（））
- `void set_image(Image value)`
  （void set_image（图像 value））
- `RectTransform get_rectTransform()`
  （矩形变换 获取_矩形变换（））
- `void set_rectTransform(RectTransform value)`
  （void set_rect变换（Rect变换 value））
- `Toggle get_toggle()`
  （开关 get_toggle（））
- `void set_toggle(Toggle value)`
  （void set_toggle（开关 value））
- `void OnPointerEnter(PointerEventData eventData)`
  （void On指针Enter（指针事件数据 eventData））
- `void OnCancel(BaseEventData eventData)`
  （void On取消（基础事件数据 eventData））

---

## Dropdown.OptionData（Dropdown.Option数据）

### 字段 (2)

- `string m_Text`（string m_文本）(偏移: 0x8)
- `Sprite m_Image`（精灵 m_图像）(偏移: 0xC)

### 方法 (4)

- `string get_text()`
  （字符串 获取_文本（））
- `void set_text(string value)`
  （void 设置_文本（字符串 value））
- `Sprite get_image()`
  （精灵 get_image（））
- `void set_image(Sprite value)`
  （void set_image（精灵 value））

---

## Dropdown.OptionDataList（Dropdown.Option数据列表）

### 字段 (1)

- `List<Dropdown.OptionData> m_Options`（List<Dropdown.OptionData> m_Options）(偏移: 0x8)

### 方法 (2)

- `List<Dropdown.OptionData> get_options()`
  （List<Dropdown.OptionData> get_options（））
- `void set_options(List<Dropdown.OptionData> value)`
  （void set_options（List<Dropdown.OptionData> value））

---

## DynamicGridObstacle（动态的网格Obstacle）

**继承**: GraphModifier（图修改器）

### 字段 (9)

- `Collider coll`（碰撞器 coll）(偏移: 0x20)
- `Collider2D coll2D`（Collider2D coll2D）(偏移: 0x24)
- `Transform tr`（变换 tr）(偏移: 0x28)
- `float updateError`（float updateError）(偏移: 0x2C)
- `float checkTime`（float check时间）(偏移: 0x30)
- `Bounds prevBounds`（Bounds prevBounds）(偏移: 0x34)
- `Quaternion prevRotation`（Quaternion prevRotation）(偏移: 0x4C)
- `bool prevEnabled`（bool prev启用的）(偏移: 0x5C)
- `float lastCheckTime`（float last检查时间）(偏移: 0x60)

### 方法 (8)

- `Bounds get_bounds()`
  （边界 获取_边界（））
- `bool get_colliderEnabled()`
  （bool get_collider启用的（））
- `void Awake()`
  （void 唤醒（））
- `void OnPostScan()`
  （void 扫描后（））
- `void Update()`
  （void 更新（））
- `void OnDisable()`
  （void 禁用时（））
- `void DoUpdateGraphs()`
  （void Do更新Graphs（））
- `float BoundsVolume(Bounds b)`
  （float BoundsVolume（Bounds b））

---

## DynamicMethod（动态的Method）

**继承**: MethodInfo（Method信息）

### 方法 (11)

- `MethodAttributes get_Attributes()`
  （方法属性 获取_属性（））
- `Type get_DeclaringType()`
  （类型 获取_声明类型（））
- `RuntimeMethodHandle get_MethodHandle()`
  （运行时方法句柄 获取_方法句柄（））
- `string get_Name()`
  （字符串 获取_名称（））
- `Type get_ReflectedType()`
  （类型 获取_反射类型（））
- `object[] GetCustomAttributes(bool inherit)`
  （对象[] 获取自定义属性（布尔值 继承））
- `object[] GetCustomAttributes(Type attributeType, bool inherit)`
  （对象[] 获取自定义属性（类型 attributeType, 布尔值 继承））
- `MethodImplAttributes GetMethodImplementationFlags()`
  （方法实现属性 获取方法实现标志（））
- `ParameterInfo[] GetParameters()`
  （参数信息[] 获取参数（））
- `object Invoke(object obj, BindingFlags invokeAttr, Binder binder, object[] parameters, CultureInfo culture)`
  （对象 调用（对象 obj, 绑定标志 invokeAttr, 绑定器 binder, 对象[] parameters, 区域性信息 culture））
- `bool IsDefined(Type attributeType, bool inherit)`
  （布尔值 是否已定义（类型 attributeType, 布尔值 继承））

---

## DynamicPropertyCollection（动态的属性Collection）

### 字段 (1)

- `ArrayList _properties`（数组列表 _properties）(偏移: 0x8)

### 方法 (5)

- `bool get_HasProperties()`
  （bool get_是否有Properties（））
- `bool RegisterDynamicProperty(IDynamicProperty prop)`
  （bool Register动态的属性（I动态的属性 prop））
- `bool UnregisterDynamicProperty(string name)`
  （bool Unregister动态的属性（string name））
- `void NotifyMessage(bool start, IMessage msg, bool client_site, bool async)`
  （void NotifyMessage（bool start, IMessage msg, bool client_site, bool async））
- `int FindProperty(string name)`
  （int 查找属性（string name））

---

## DynamicPropertyCollection.DynamicPropertyReg（动态的属性Collection.动态的属性Reg）

### 字段 (2)

- `IDynamicProperty Property`（I动态的属性 属性）(偏移: 0x8)
- `IDynamicMessageSink Sink`（I动态的MessageSink Sink）(偏移: 0xC)

---

## DynamicResScalePolicyType（动态的Res缩放Policy类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DynamicResUpscaleFilter（动态的ResUpscaleFilter）

### 字段 (1)

- `byte value__`（字节 值__）(偏移: 0x0)

---

## DynamicResolutionHandler（动态的Resolution处理器）

### 字段 (23)

- `bool m_Enabled`（bool m_启用的）(偏移: 0x8)
- `float m_MinScreenFraction`（float m_最小屏幕的Fraction）(偏移: 0xC)
- `float m_MaxScreenFraction`（float m_最大屏幕的Fraction）(偏移: 0x10)
- `float m_CurrentFraction`（float m_当前Fraction）(偏移: 0x14)
- `bool m_ForcingRes`（bool m_ForcingRes）(偏移: 0x18)
- `bool m_CurrentCameraRequest`（bool m_当前摄像机请求）(偏移: 0x19)
- `float m_PrevFraction`（float m_PrevFraction）(偏移: 0x1C)
- `bool m_ForceSoftwareFallback`（bool m_强制SoftwareFallback）(偏移: 0x20)
- `float m_PrevHWScaleWidth`（float m_PrevHW缩放宽度）(偏移: 0x24)
- `float m_PrevHWScaleHeight`（float m_PrevHW缩放高度）(偏移: 0x28)
- `Vector2Int m_LastScaledSize`（二维向量整数 m_最后一个Scaled大小）(偏移: 0x2C)
- `DynamicResScalePolicyType s_ScalerType`（动态的Res缩放Policy类型 s_Scaler类型）(偏移: 0x0)
- `PerformDynamicRes s_DynamicResMethod`（执行动态的Res s_动态的ResMethod）(偏移: 0x4)
- `Vector2Int cachedOriginalSize`（二维向量整数 cachedOriginal大小）(偏移: 0x34)
- `DynamicResolutionType type`（动态的Resolution类型 type）(偏移: 0x48)
- `GlobalDynamicResolutionSettings m_CachedSettings`（全局的动态的ResolutionSettings m_CachedSettings）(偏移: 0x4C)
- `WeakReference m_OwnerCameraWeakRef`（Weak引用 m_Owner摄像机WeakRef）(偏移: 0x60)
- `DynamicResolutionHandler s_DefaultInstance`（动态的Resolution处理器 s_默认的实例）(偏移: 0xC)
- `int s_ActiveCameraId`（int s_激活的摄像机Id）(偏移: 0x10)
- `DynamicResolutionHandler s_ActiveInstance`（动态的Resolution处理器 s_激活的实例）(偏移: 0x14)
- `bool s_ActiveInstanceDirty`（bool s_激活的实例Dirty）(偏移: 0x18)
- `float s_GlobalHwFraction`（float s_全局的HwFraction）(偏移: 0x1C)
- `bool s_GlobalHwUpresActive`（bool s_全局的HwUpres激活的）(偏移: 0x20)

### 方法 (25)

- `void Reset()`
  （void 重置（））
- `DynamicResUpscaleFilter get_filter()`
  （动态的ResUpscaleFilter get_filter（））
- `void set_filter(DynamicResUpscaleFilter value)`
  （void set_filter（动态的ResUpscaleFilter value））
- `Vector2Int get_finalViewport()`
  （二维向量整数 get_finalViewport（））
- `void set_finalViewport(Vector2Int value)`
  （void set_finalViewport（二维向量整数 value））
- `bool FlushScalableBufferManagerState()`
  （bool FlushScalable缓冲区管理器状态（））
- `DynamicResolutionHandler GetOrCreateDrsInstanceHandler(Camera camera)`
  （动态的Resolution处理器 获取Or创建Drs实例处理器（摄像机 camera））
- `DynamicResolutionHandler get_instance()`
  （动态的Resolution处理器 get_instance（））
- `float DefaultDynamicResMethod()`
  （float 默认的动态的ResMethod（））
- `void ProcessSettings(GlobalDynamicResolutionSettings settings)`
  （void 处理Settings（全局的动态的ResolutionSettings settings））
- `Vector2 GetResolvedScale()`
  （二维向量 获取Resolved缩放（））
- `void SetDynamicResScaler(PerformDynamicRes scaler, DynamicResScalePolicyType scalerType = 1)`
  （void 集合动态的ResScaler（执行动态的Res scaler, 动态的Res缩放Policy类型 scalerType = 1））
- `void ClearSelectedCamera()`
  （void 清除选中的摄像机（））
- `void SetCurrentCameraRequest(bool cameraRequest)`
  （void 集合当前摄像机请求（bool cameraRequest））
- `void UpdateAndUseCamera(Camera camera, Nullable<GlobalDynamicResolutionSettings> settings, Action OnResolutionChange)`
  （void 更新AndUse摄像机（摄像机 camera, Nullable<全局的动态的ResolutionSettings> settings, 动作 OnResolutionChange））
- `void Update(GlobalDynamicResolutionSettings settings, Action OnResolutionChange)`
  （void 更新（全局的动态的ResolutionSettings settings, 动作 OnResolutionChange））
- `bool SoftwareDynamicResIsEnabled()`
  （bool Software动态的Res是否启用的（））
- `bool HardwareDynamicResIsEnabled()`
  （bool Hardware动态的Res是否启用的（））
- `bool RequestsHardwareDynamicResolution()`
  （bool RequestsHardware动态的Resolution（））
- `bool DynamicResolutionEnabled()`
  （bool 动态的Resolution启用的（））
- `void ForceSoftwareFallback()`
  （void 强制SoftwareFallback（））
- `Vector2Int GetScaledSize(Vector2Int size)`
  （二维向量整数 获取Scaled大小（二维向量整数 size））
- `Vector2Int ApplyScalesOnSize(Vector2Int size)`
  （二维向量整数 应用ScalesOn大小（二维向量整数 size））
- `float GetCurrentScale()`
  （float 获取当前缩放（））
- `Vector2Int GetLastScaledSize()`
  （二维向量整数 获取最后一个Scaled大小（））

---

## DynamicResolutionType（动态的Resolution类型）

### 字段 (1)

- `byte value__`（字节 值__）(偏移: 0x0)

---

## Ease（Ease）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## EaseCurve（EaseCurve）

### 字段 (1)

- `AnimationCurve _animCurve`（动画Curve _animCurve）(偏移: 0x8)

### 方法 (1)

- `float Evaluate(float time, float duration, float unusedOvershoot, float unusedPeriod)`
  （float Evaluate（float time, float duration, float unusedOvershoot, float unusedPeriod））

---

## EaseFactory（Ease工厂）

### 方法 (3)

- `EaseFunction StopMotion(int motionFps, Nullable<Ease> ease)`
  （EaseFunction 停止Motion（int motionFps, Nullable<Ease> ease））
- `EaseFunction StopMotion(int motionFps, AnimationCurve animCurve)`
  （EaseFunction 停止Motion（int motionFps, 动画Curve animCurve））
- `EaseFunction StopMotion(int motionFps, EaseFunction customEase)`
  （EaseFunction 停止Motion（int motionFps, EaseFunction customEase））

---

## EaseFunction（EaseFunction）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `float Invoke(float time, float duration, float overshootOrAmplitude, float period)`
  （float Invoke（float time, float duration, float overshootOrAmplitude, float period））
- `IAsyncResult BeginInvoke(float time, float duration, float overshootOrAmplitude, float period, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（float time, float duration, float overshootOrAmplitude, float period, 异步回调 callback, object object））
- `float EndInvoke(IAsyncResult result)`
  （浮点数 结束调用（I异步结果 result））

---

## EaseManager（Ease管理器）

### 方法 (4)

- `float Evaluate(Tween t, float time, float duration, float overshootOrAmplitude, float period)`
  （float Evaluate（Tween t, float time, float duration, float overshootOrAmplitude, float period））
- `float Evaluate(Ease easeType, EaseFunction customEase, float time, float duration, float overshootOrAmplitude, float period)`
  （float Evaluate（Ease easeType, EaseFunction customEase, float time, float duration, float overshootOrAmplitude, float period））
- `EaseFunction ToEaseFunction(Ease ease)`
  （EaseFunction ToEaseFunction（Ease ease））
- `bool IsFlashEase(Ease ease)`
  （bool 是否FlashEase（Ease ease））

---

## EdgeSide（Edge侧面）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## EditorAttribute（EditorAttribute）

**继承**: Attribute（属性）

### 字段 (2)

- `string baseTypeName`（string base类型名称）(偏移: 0x8)
- `string typeName`（字符串 类型名称）(偏移: 0xC)

### 方法 (2)

- `string get_EditorBaseTypeName()`
  （string get_Editor基础类型名称（））
- `string get_EditorTypeName()`
  （string get_Editor类型名称（））

---

## EditorBrowsableAttribute（EditorBrowsableAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `EditorBrowsableState browsableState`（EditorBrowsable状态 browsable状态）(偏移: 0x8)

### 方法 (2)

- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## EditorBrowsableState（EditorBrowsable状态）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## EditorIK（EditorIK）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (1)

- `IK ik`（IK ik）(偏移: 0xC)

### 方法 (2)

- `void Start()`
  （void 开始（））
- `void Update()`
  （void 更新（））

---

## EffectAsset（特效资产）

**继承**: ScriptableObject（脚本对象）

### 字段 (1)

- `List<EffectAsset.EffectData> asset`（List<特效Asset.特效Data> asset）(偏移: 0xC)

### 方法 (1)

- `GameObject GetPrefab(string name, int index = -1)`
  （游戏对象 获取预制体（string name, int index = -1））

---

## EffectAsset.EffectData（特效Asset.特效数据）

### 字段 (2)

- `string name`（字符串 名称）(偏移: 0x0)
- `GameObject[] effects`（游戏Object[] effects）(偏移: 0x4)

---

## EffectManager（特效管理器）

**继承**: Singleton<EffectManager>（Singleton<特效Manager>）

### 字段 (4)

- `GameObject recyclableImpulse`（游戏对象 recyclableImpulse）(偏移: 0xC)
- `EffectAsset asset`（特效资产 asset）(偏移: 0x10)
- `NameKeyPool effectPool`（名称键池 effect池）(偏移: 0x14)
- `SimpleObjectPool impulsePool`（Simple对象池 impulse池）(偏移: 0x18)

### 方法 (9)

- `void Awake()`
  （void 唤醒（））
- `RecyclableObject PlayWorldEffect(string name, int index, Vector3 position, Quaternion rotation, bool autoActive = True)`
  （Recyclable对象 播放世界的特效（string name, int index, 三维向量 position, Quaternion rotation, bool autoActive = True））
- `RecyclableObject PlayWorldEffect(GameObject prefab, Vector3 position, Quaternion rotation, bool autoActive = True)`
  （Recyclable对象 播放世界的特效（游戏对象 prefab, 三维向量 position, Quaternion rotation, bool autoActive = True））
- `RecyclableObject PlayWorldEffect(GameObject prefab, Player player, bool autoActive = True)`
  （Recyclable对象 播放世界的特效（游戏对象 prefab, 玩家 player, bool autoActive = True））
- `RecyclableObject PlayAttachEffect(GameObject prefab, Transform parent, bool autoActive = True)`
  （Recyclable对象 播放Attach特效（游戏对象 prefab, 变换 parent, bool autoActive = True））
- `RecyclableObject GetEffect(GameObject prefab)`
  （Recyclable对象 获取特效（游戏对象 prefab））
- `GameObject GetEffectPrefab(string name, int index = -1)`
  （游戏对象 获取特效预制体（string name, int index = -1））
- `void CreateBulletHole(RaycastHit hitInfo)`
  （void 创建子弹Hole（Raycast命中 hitInfo））
- `void PlayImpulse(Vector3 worldPos, float power, float minRadius, float maxRadius, float duration)`
  （void 播放Impulse（三维向量 worldPos, float power, float minRadius, float maxRadius, float duration））

---

## EffectObj（特效Obj）

**继承**: Model（模型）

### 字段 (9)

- `ParticleSystem ptcSystem`（粒子系统 ptc系统）(偏移: 0x40)
- `Transform root`（变换 根节点）(偏移: 0x44)
- `bool isWorldSpace`（bool is世界的Space）(偏移: 0x48)
- `Vector3 bindOffset`（三维向量 bindOffset）(偏移: 0x4C)
- `Transform bindTransform`（变换 bind变换）(偏移: 0x58)
- `Func<bool> preRecycleFunc`（Func<bool> preRecycleFunc）(偏移: 0x5C)
- `float delayRecycleTime`（float delayRecycle时间）(偏移: 0x60)
- `float finalRecycleTime`（float finalRecycle时间）(偏移: 0x64)
- `bool fixBug`（bool fixBug）(偏移: 0x68)

### 方法 (9)

- `void Work()`
  （void 工作（））
- `void LateUpdate()`
  （void 延迟更新（））
- `void TryRecycle(bool roundRecycle)`
  （void TryRecycle（bool roundRecycle））
- `void Recycle(bool roundRecycle)`
  （void 回收（布尔值 循环回收））
- `void BindOnTransformInLocalSpace(Transform bind, Vector3 offset)`
  （void BindOn变换In本地的Space（变换 bind, 三维向量 offset））
- `void BindOnTransformInWorldSpace(Transform bind, Vector3 offset)`
  （void BindOn变换In世界的Space（变换 bind, 三维向量 offset））
- `void BindTransform(Transform bind, Vector3 offset)`
  （void Bind变换（变换 bind, 三维向量 offset））
- `void UpdatePosition()`
  （void 更新Position（））
- `void StopShootEffect(bool clear)`
  （void 停止射击特效（bool clear））

---

## EffectTester（特效Tester）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (3)

- `Vector3 offset`（三维向量 偏移）(偏移: 0xC)
- `Vector3 euler`（三维向量 欧拉角）(偏移: 0x18)
- `Quaternion orignalRot`（Quaternion orignalRot）(偏移: 0x24)

### 方法 (2)

- `void RecordRot()`
  （void RecordRot（））
- `void UpdateRot()`
  （void 更新Rot（））

---

## ElementType（元素类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Empty（空）

**继承**: ISerializable（可序列化接口）

### 字段 (1)

- `Empty Value`（空 值）(偏移: 0x0)

### 方法 (2)

- `string ToString()`
  （字符串 转字符串（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））

---

## EmptyReadOnlyDictionaryInternal（空ReadOnly字典内部的）

**继承**: IDictionary, ICollection, IEnumerable（I字典, ICollection, IEnumerable）

### 方法 (8)

- `void CopyTo(Array array, int index)`
  （void 复制到（数组 array, 整数 index））
- `int get_Count()`
  （整数 获取_数量（））
- `object get_SyncRoot()`
  （对象 获取_同步根（））
- `object get_Item(object key)`
  （对象 获取_项（对象 key））
- `void set_Item(object key, object value)`
  （void 设置_项（对象 key, 对象 value））
- `bool Contains(object key)`
  （布尔值 包含（对象 key））
- `IDictionaryEnumerator GetEnumerator()`
  （I字典枚举器 获取枚举器（））
- `void Remove(object key)`
  （void 移除（对象 key））

---

## EmptyReadOnlyDictionaryInternal.NodeEnumerator（空ReadOnly字典Internal.节点Enumerator）

**继承**: IDictionaryEnumerator, IEnumerator（I字典枚举器, IEnumerator）

### 方法 (6)

- `bool MoveNext()`
  （布尔值 移动下一个（））
- `object get_Current()`
  （对象 获取_当前（））
- `void Reset()`
  （void 重置（））
- `object get_Key()`
  （对象 获取_键（））
- `object get_Value()`
  （对象 获取_值（））
- `DictionaryEntry get_Entry()`
  （字典项 获取_项（））

---

## Encoder（Encoder）

### 字段 (2)

- `EncoderFallback m_fallback`（EncoderFallback m_fallback）(偏移: 0x8)
- `EncoderFallbackBuffer m_fallbackBuffer`（EncoderFallback缓冲区 m_fallback缓冲区）(偏移: 0xC)

### 方法 (7)

- `void SerializeEncoder(SerializationInfo info)`
  （void SerializeEncoder（Serialization信息 info））
- `EncoderFallback get_Fallback()`
  （EncoderFallback get_Fallback（））
- `EncoderFallbackBuffer get_FallbackBuffer()`
  （EncoderFallback缓冲区 get_Fallback缓冲区（））
- `bool get_InternalHasFallbackBuffer()`
  （bool get_内部的是否有Fallback缓冲区（））
- `void Reset()`
  （void 重置（））
- `int GetByteCount(char* chars, int count, bool flush)`
  （int 获取Byte数量（char* chars, int count, bool flush））
- `int GetBytes(char* chars, int charCount, byte* bytes, int byteCount, bool flush)`
  （int 获取Bytes（char* chars, int charCount, byte* bytes, int byteCount, bool flush））

---

## EncoderExceptionFallback（EncoderExceptionFallback）

**继承**: EncoderFallback（EncoderFallback）

### 方法 (4)

- `EncoderFallbackBuffer CreateFallbackBuffer()`
  （EncoderFallback缓冲区 创建Fallback缓冲区（））
- `int get_MaxCharCount()`
  （整数 获取_最大字符数量（））
- `bool Equals(object value)`
  （布尔值 等于（对象 value））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## EncoderExceptionFallbackBuffer（EncoderExceptionFallback缓冲区）

**继承**: EncoderFallbackBuffer（EncoderFallback缓冲区）

### 方法 (5)

- `bool Fallback(char charUnknown, int index)`
  （bool Fallback（char charUnknown, int index））
- `bool Fallback(char charUnknownHigh, char charUnknownLow, int index)`
  （bool Fallback（char charUnknownHigh, char charUnknownLow, int index））
- `char GetNextChar()`
  （字符 获取下一个字符（））
- `bool MovePrevious()`
  （bool 移动上一个（））
- `int get_Remaining()`
  （int get_Remaining（））

---

## EncoderFallback（EncoderFallback）

### 字段 (4)

- `bool bIsMicrosoftBestFitFallback`（bool b是否MicrosoftBestFitFallback）(偏移: 0x8)
- `EncoderFallback replacementFallback`（EncoderFallback replacementFallback）(偏移: 0x0)
- `EncoderFallback exceptionFallback`（EncoderFallback exceptionFallback）(偏移: 0x4)
- `object s_InternalSyncObject`（对象 s_内部同步对象）(偏移: 0x8)

### 方法 (3)

- `object get_InternalSyncObject()`
  （对象 获取_内部同步对象（））
- `EncoderFallback get_ReplacementFallback()`
  （EncoderFallback get_ReplacementFallback（））
- `EncoderFallback get_ExceptionFallback()`
  （EncoderFallback get_ExceptionFallback（））

---

## EncoderFallbackBuffer（EncoderFallback缓冲区）

### 字段 (7)

- `char* charStart`（char* char开始）(偏移: 0x8)
- `char* charEnd`（char* char结束）(偏移: 0xC)
- `EncoderNLS encoder`（EncoderNLS encoder）(偏移: 0x10)
- `bool setEncoder`（bool setEncoder）(偏移: 0x14)
- `bool bUsedEncoder`（bool bUsedEncoder）(偏移: 0x15)
- `bool bFallingBack`（bool bFalling后）(偏移: 0x16)
- `int iRecursionCount`（int iRecursion数量）(偏移: 0x18)

### 方法 (6)

- `void Reset()`
  （void 重置（））
- `void InternalReset()`
  （void 内部的重置（））
- `void InternalInitialize(char* charStart, char* charEnd, EncoderNLS encoder, bool setEncoder)`
  （void 内部的初始化（char* charStart, char* charEnd, EncoderNLS encoder, bool setEncoder））
- `char InternalGetNextChar()`
  （char 内部的获取下一个Char（））
- `bool InternalFallback(char ch, ref char* chars)`
  （bool 内部的Fallback（char ch, ref char* chars））
- `void ThrowLastCharRecursive(int charRecursive)`
  （void 投掷最后一个CharRecursive（int charRecursive））

---

## EncoderFallbackException（EncoderFallbackException）

**继承**: ArgumentException（ArgumentException）

### 字段 (4)

- `char charUnknown`（char charUnknown）(偏移: 0x48)
- `char charUnknownHigh`（char charUnknownHigh）(偏移: 0x4A)
- `char charUnknownLow`（char charUnknownLow）(偏移: 0x4C)
- `int index`（整数 索引）(偏移: 0x50)

---

## EncoderNLS（EncoderNLS）

**继承**: Encoder, ISerializable（Encoder, ISerializable）

### 字段 (5)

- `char charLeftOver`（char char左Over）(偏移: 0x10)
- `Encoding m_encoding`（Encoding m_encoding）(偏移: 0x14)
- `bool m_mustFlush`（bool m_mustFlush）(偏移: 0x18)
- `bool m_throwOnOverflow`（bool m_throwOnOverflow）(偏移: 0x19)
- `int m_charsUsed`（int m_charsUsed）(偏移: 0x1C)

### 方法 (8)

- `void Reset()`
  （void 重置（））
- `int GetByteCount(char[] chars, int index, int count, bool flush)`
  （int 获取Byte数量（char[] chars, int index, int count, bool flush））
- `int GetByteCount(char* chars, int count, bool flush)`
  （int 获取Byte数量（char* chars, int count, bool flush））
- `int GetBytes(char[] chars, int charIndex, int charCount, byte[] bytes, int byteIndex, bool flush)`
  （int 获取Bytes（char[] chars, int charIndex, int charCount, byte[] bytes, int byteIndex, bool flush））
- `int GetBytes(char* chars, int charCount, byte* bytes, int byteCount, bool flush)`
  （int 获取Bytes（char* chars, int charCount, byte* bytes, int byteCount, bool flush））
- `Encoding get_Encoding()`
  （Encoding get_Encoding（））
- `bool get_MustFlush()`
  （bool get_MustFlush（））
- `void ClearMustFlush()`
  （void 清除MustFlush（））

---

## EncoderReplacementFallback（EncoderReplacementFallback）

**继承**: EncoderFallback（EncoderFallback）

### 字段 (1)

- `string strDefault`（string str默认的）(偏移: 0xC)

### 方法 (5)

- `string get_DefaultString()`
  （string get_默认的字符串（））
- `EncoderFallbackBuffer CreateFallbackBuffer()`
  （EncoderFallback缓冲区 创建Fallback缓冲区（））
- `int get_MaxCharCount()`
  （整数 获取_最大字符数量（））
- `bool Equals(object value)`
  （布尔值 等于（对象 value））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## EncoderReplacementFallbackBuffer（EncoderReplacementFallback缓冲区）

**继承**: EncoderFallbackBuffer（EncoderFallback缓冲区）

### 字段 (3)

- `string strDefault`（string str默认的）(偏移: 0x1C)
- `int fallbackCount`（int fallback数量）(偏移: 0x20)
- `int fallbackIndex`（int fallback索引）(偏移: 0x24)

### 方法 (6)

- `bool Fallback(char charUnknown, int index)`
  （bool Fallback（char charUnknown, int index））
- `bool Fallback(char charUnknownHigh, char charUnknownLow, int index)`
  （bool Fallback（char charUnknownHigh, char charUnknownLow, int index））
- `char GetNextChar()`
  （字符 获取下一个字符（））
- `bool MovePrevious()`
  （bool 移动上一个（））
- `int get_Remaining()`
  （int get_Remaining（））
- `void Reset()`
  （void 重置（））

---

## Encoding（编码）

**继承**: ICloneable（ICloneable可克隆）

### 字段 (16)

- `Encoding defaultEncoding`（Encoding defaultEncoding）(偏移: 0x0)
- `Encoding unicodeEncoding`（Encoding unicodeEncoding）(偏移: 0x4)
- `Encoding bigEndianUnicode`（Encoding bigEndianUnicode）(偏移: 0x8)
- `Encoding utf7Encoding`（Encoding utf7Encoding）(偏移: 0xC)
- `Encoding utf8Encoding`（Encoding utf8Encoding）(偏移: 0x10)
- `Encoding utf32Encoding`（Encoding utf32Encoding）(偏移: 0x14)
- `Encoding asciiEncoding`（Encoding asciiEncoding）(偏移: 0x18)
- `Encoding latin1Encoding`（Encoding latin1Encoding）(偏移: 0x1C)
- `Hashtable encodings`（Hashtable encodings）(偏移: 0x20)
- `int m_codePage`（int m_codePage）(偏移: 0x8)
- `CodePageDataItem dataItem`（CodePage数据项目 data项目）(偏移: 0xC)
- `bool m_deserializedFromEverett`（bool m_deserializedFromEverett）(偏移: 0x10)
- `bool m_isReadOnly`（布尔值 m_是否只读）(偏移: 0x11)
- `EncoderFallback encoderFallback`（EncoderFallback encoderFallback）(偏移: 0x14)
- `DecoderFallback decoderFallback`（DecoderFallback decoderFallback）(偏移: 0x18)
- `object s_InternalSyncObject`（对象 s_内部同步对象）(偏移: 0x24)

### 方法 (58)

- `void SetDefaultFallbacks()`
  （void 设置默认回退（））
- `void OnDeserializing()`
  （void OnDeserializing（））
- `void OnDeserialized()`
  （void OnDeserialized（））
- `void OnDeserializing(StreamingContext ctx)`
  （void 反序列化中（流上下文 ctx））
- `void OnDeserialized(StreamingContext ctx)`
  （void 反序列化后（流上下文 ctx））
- `void OnSerializing(StreamingContext ctx)`
  （void 序列化中（流上下文 ctx））
- `void DeserializeEncoding(SerializationInfo info, StreamingContext context)`
  （void DeserializeEncoding（Serialization信息 info, StreamingContext context））
- `void SerializeEncoding(SerializationInfo info, StreamingContext context)`
  （void SerializeEncoding（Serialization信息 info, StreamingContext context））
- `object get_InternalSyncObject()`
  （对象 获取_内部同步对象（））
- `Encoding GetEncoding(int codepage)`
  （Encoding 获取Encoding（int codepage））
- `Encoding GetEncoding(int codepage, EncoderFallback encoderFallback, DecoderFallback decoderFallback)`
  （Encoding 获取Encoding（int codepage, EncoderFallback encoderFallback, DecoderFallback decoderFallback））
- `Encoding GetEncoding(string name)`
  （Encoding 获取Encoding（string name））
- `byte[] GetPreamble()`
  （byte[] 获取Preamble（））
- `void GetDataItem()`
  （void 获取数据项目（））
- `string get_EncodingName()`
  （string get_Encoding名称（））
- `string get_WebName()`
  （string get_Web名称（））
- `EncoderFallback get_EncoderFallback()`
  （EncoderFallback get_EncoderFallback（））
- `void set_EncoderFallback(EncoderFallback value)`
  （void set_EncoderFallback（EncoderFallback value））
- `DecoderFallback get_DecoderFallback()`
  （DecoderFallback get_DecoderFallback（））
- `void set_DecoderFallback(DecoderFallback value)`
  （void set_DecoderFallback（DecoderFallback value））
- `object Clone()`
  （对象 克隆（））
- `bool get_IsReadOnly()`
  （布尔值 获取_是否只读（））
- `Encoding get_ASCII()`
  （Encoding get_ASCII（））
- `Encoding get_Latin1()`
  （Encoding get_Latin1（））
- `int GetByteCount(string s)`
  （整数 获取字节数量（字符串 s））
- `int GetByteCount(char* chars, int count)`
  （整数 获取字节数量（字符* chars, 整数 count））
- `int GetByteCount(char* chars, int count, EncoderNLS encoder)`
  （int 获取Byte数量（char* chars, int count, EncoderNLS encoder））
- `byte[] GetBytes(char[] chars, int index, int count)`
  （byte[] 获取Bytes（char[] chars, int index, int count））
- `byte[] GetBytes(string s)`
  （byte[] 获取Bytes（string s））
- `int GetBytes(string s, int charIndex, int charCount, byte[] bytes, int byteIndex)`
  （整数 获取字节（字符串 s, 整数 charIndex, 整数 charCount, 字节[] bytes, 整数 byteIndex））
- `int GetBytes(char* chars, int charCount, byte* bytes, int byteCount, EncoderNLS encoder)`
  （整数 获取字节（字符* chars, 整数 charCount, 字节* bytes, 整数 byteCount, 编码器NLS encoder））
- `int GetBytes(char* chars, int charCount, byte* bytes, int byteCount)`
  （整数 获取字节（字符* chars, 整数 charCount, 字节* bytes, 整数 byteCount））
- `int GetCharCount(byte* bytes, int count)`
  （整数 获取字符数量（字节* bytes, 整数 count））
- `int GetCharCount(byte* bytes, int count, DecoderNLS decoder)`
  （int 获取Char数量（byte* bytes, int count, DecoderNLS decoder））
- `char[] GetChars(byte[] bytes, int index, int count)`
  （char[] 获取Chars（byte[] bytes, int index, int count））
- `int GetChars(byte* bytes, int byteCount, char* chars, int charCount)`
  （整数 获取字符（字节* bytes, 整数 byteCount, 字符* chars, 整数 charCount））
- `int GetChars(byte* bytes, int byteCount, char* chars, int charCount, DecoderNLS decoder)`
  （int 获取Chars（byte* bytes, int byteCount, char* chars, int charCount, DecoderNLS decoder））
- `int get_CodePage()`
  （int get_CodePage（））
- `Decoder GetDecoder()`
  （解码器 获取解码器（））
- `Encoding CreateDefaultEncoding()`
  （Encoding 创建默认的Encoding（））
- `void setReadOnly(bool value = True)`
  （void setReadOnly（bool value = True））
- `Encoding get_Default()`
  （Encoding get_默认的（））
- `Encoder GetEncoder()`
  （编码器 获取编码器（））
- `string GetString(byte[] bytes)`
  （string 获取字符串（byte[] bytes））
- `string GetString(byte[] bytes, int index, int count)`
  （字符串 获取字符串（字节[] bytes, 整数 index, 整数 count））
- `Encoding get_Unicode()`
  （Encoding get_Unicode（））
- `Encoding get_BigEndianUnicode()`
  （Encoding get_BigEndianUnicode（））
- `Encoding get_UTF7()`
  （Encoding get_UTF7（））
- `Encoding get_UTF8()`
  （Encoding get_UTF8（））
- `Encoding get_UTF32()`
  （Encoding get_UTF32（））
- `bool Equals(object value)`
  （布尔值 等于（对象 value））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `char[] GetBestFitUnicodeToBytesData()`
  （char[] 获取BestFitUnicodeToBytes数据（））
- `char[] GetBestFitBytesToUnicodeData()`
  （char[] 获取BestFitBytesToUnicode数据（））
- `void ThrowBytesOverflow()`
  （void 投掷BytesOverflow（））
- `void ThrowBytesOverflow(EncoderNLS encoder, bool nothingEncoded)`
  （void 投掷BytesOverflow（EncoderNLS encoder, bool nothingEncoded））
- `void ThrowCharsOverflow()`
  （void 投掷CharsOverflow（））
- `void ThrowCharsOverflow(DecoderNLS decoder, bool nothingDecoded)`
  （void 投掷CharsOverflow（DecoderNLS decoder, bool nothingDecoded））

---

## Encoding.DefaultDecoder（Encoding.默认的Decoder）

**继承**: Decoder, ISerializable, IObjectReference（Decoder, ISerializable, I对象引用）

### 字段 (2)

- `Encoding m_encoding`（Encoding m_encoding）(偏移: 0x10)
- `bool m_hasInitializedEncoding`（bool m_hasInitializedEncoding）(偏移: 0x14)

### 方法 (7)

- `object GetRealObject(StreamingContext context)`
  （对象 获取真实对象（流上下文 context））
- `int GetCharCount(byte[] bytes, int index, int count)`
  （整数 获取字符数量（字节[] bytes, 整数 index, 整数 count））
- `int GetCharCount(byte[] bytes, int index, int count, bool flush)`
  （int 获取Char数量（byte[] bytes, int index, int count, bool flush））
- `int GetCharCount(byte* bytes, int count, bool flush)`
  （int 获取Char数量（byte* bytes, int count, bool flush））
- `int GetChars(byte[] bytes, int byteIndex, int byteCount, char[] chars, int charIndex)`
  （整数 获取字符（字节[] bytes, 整数 byteIndex, 整数 byteCount, 字符[] chars, 整数 charIndex））
- `int GetChars(byte[] bytes, int byteIndex, int byteCount, char[] chars, int charIndex, bool flush)`
  （int 获取Chars（byte[] bytes, int byteIndex, int byteCount, char[] chars, int charIndex, bool flush））
- `int GetChars(byte* bytes, int byteCount, char* chars, int charCount, bool flush)`
  （int 获取Chars（byte* bytes, int byteCount, char* chars, int charCount, bool flush））

---

## Encoding.DefaultEncoder（Encoding.默认的Encoder）

**继承**: Encoder, ISerializable, IObjectReference（Encoder, ISerializable, I对象引用）

### 字段 (3)

- `Encoding m_encoding`（Encoding m_encoding）(偏移: 0x10)
- `bool m_hasInitializedEncoding`（bool m_hasInitializedEncoding）(偏移: 0x14)
- `char charLeftOver`（char char左Over）(偏移: 0x16)

### 方法 (5)

- `object GetRealObject(StreamingContext context)`
  （对象 获取真实对象（流上下文 context））
- `int GetByteCount(char[] chars, int index, int count, bool flush)`
  （int 获取Byte数量（char[] chars, int index, int count, bool flush））
- `int GetByteCount(char* chars, int count, bool flush)`
  （int 获取Byte数量（char* chars, int count, bool flush））
- `int GetBytes(char[] chars, int charIndex, int charCount, byte[] bytes, int byteIndex, bool flush)`
  （int 获取Bytes（char[] chars, int charIndex, int charCount, byte[] bytes, int byteIndex, bool flush））
- `int GetBytes(char* chars, int charCount, byte* bytes, int byteCount, bool flush)`
  （int 获取Bytes（char* chars, int charCount, byte* bytes, int byteCount, bool flush））

---

## Encoding.EncodingByteBuffer（Encoding.EncodingByte缓冲区）

### 字段 (10)

- `byte* bytes`（byte* bytes）(偏移: 0x8)
- `byte* byteStart`（byte* byte开始）(偏移: 0xC)
- `byte* byteEnd`（byte* byte结束）(偏移: 0x10)
- `char* chars`（char* chars）(偏移: 0x14)
- `char* charStart`（char* char开始）(偏移: 0x18)
- `char* charEnd`（char* char结束）(偏移: 0x1C)
- `int byteCountResult`（int byte数量Result）(偏移: 0x20)
- `Encoding enc`（Encoding enc）(偏移: 0x24)
- `EncoderNLS encoder`（EncoderNLS encoder）(偏移: 0x28)
- `EncoderFallbackBuffer fallbackBuffer`（EncoderFallback缓冲区 fallback缓冲区）(偏移: 0x2C)

### 方法 (9)

- `bool AddByte(byte b, int moreBytesExpected)`
  （bool 添加Byte（byte b, int moreBytesExpected））
- `bool AddByte(byte b1)`
  （bool 添加Byte（byte b1））
- `bool AddByte(byte b1, byte b2)`
  （bool 添加Byte（byte b1, byte b2））
- `bool AddByte(byte b1, byte b2, int moreBytesExpected)`
  （bool 添加Byte（byte b1, byte b2, int moreBytesExpected））
- `void MovePrevious(bool bThrow)`
  （void 移动上一个（bool bThrow））
- `bool get_MoreData()`
  （bool get_More数据（））
- `char GetNextChar()`
  （字符 获取下一个字符（））
- `int get_CharsUsed()`
  （int get_CharsUsed（））
- `int get_Count()`
  （整数 获取_数量（））

---

## Encoding.EncodingCharBuffer（Encoding.EncodingChar缓冲区）

### 字段 (10)

- `char* chars`（char* chars）(偏移: 0x8)
- `char* charStart`（char* char开始）(偏移: 0xC)
- `char* charEnd`（char* char结束）(偏移: 0x10)
- `int charCountResult`（int char数量Result）(偏移: 0x14)
- `Encoding enc`（Encoding enc）(偏移: 0x18)
- `DecoderNLS decoder`（DecoderNLS decoder）(偏移: 0x1C)
- `byte* byteStart`（byte* byte开始）(偏移: 0x20)
- `byte* byteEnd`（byte* byte结束）(偏移: 0x24)
- `byte* bytes`（byte* bytes）(偏移: 0x28)
- `DecoderFallbackBuffer fallbackBuffer`（DecoderFallback缓冲区 fallback缓冲区）(偏移: 0x2C)

### 方法 (9)

- `bool AddChar(char ch, int numBytes)`
  （bool 添加Char（char ch, int numBytes））
- `bool AddChar(char ch)`
  （bool 添加Char（char ch））
- `void AdjustBytes(int count)`
  （void AdjustBytes（int count））
- `bool get_MoreData()`
  （bool get_More数据（））
- `byte GetNextByte()`
  （byte 获取下一个Byte（））
- `int get_BytesUsed()`
  （int get_BytesUsed（））
- `bool Fallback(byte fallbackByte)`
  （bool Fallback（byte fallbackByte））
- `bool Fallback(byte[] byteBuffer)`
  （bool Fallback（byte[] byteBuffer））
- `int get_Count()`
  （整数 获取_数量（））

---

## EncodingHelper（Encoding辅助器）

### 字段 (4)

- `Encoding utf8EncodingWithoutMarkers`（Encoding utf8EncodingWithoutMarkers）(偏移: 0x0)
- `object lockobj`（object lockobj）(偏移: 0x4)
- `Assembly i18nAssembly`（Assembly i18nAssembly）(偏移: 0x8)
- `bool i18nDisabled`（bool i18n禁用的）(偏移: 0xC)

### 方法 (4)

- `Encoding get_UTF8Unmarked()`
  （Encoding get_UTF8Unmarked（））
- `string InternalCodePage(ref int code_page)`
  （string 内部的CodePage（ref int code_page））
- `Encoding GetDefaultEncoding()`
  （Encoding 获取默认的Encoding（））
- `object InvokeI18N(string name, object[] args)`
  （object InvokeI18N（string name, object[] args））

---

## EncodingNLS（EncodingNLS）

**继承**: Encoding（编码）

### 方法 (13)

- `int GetByteCount(char[] chars, int index, int count)`
  （整数 获取字节数量（字符[] chars, 整数 index, 整数 count））
- `int GetByteCount(string s)`
  （整数 获取字节数量（字符串 s））
- `int GetByteCount(char* chars, int count)`
  （整数 获取字节数量（字符* chars, 整数 count））
- `int GetBytes(string s, int charIndex, int charCount, byte[] bytes, int byteIndex)`
  （整数 获取字节（字符串 s, 整数 charIndex, 整数 charCount, 字节[] bytes, 整数 byteIndex））
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
- `string GetString(byte[] bytes, int index, int count)`
  （字符串 获取字符串（字节[] bytes, 整数 index, 整数 count））
- `Decoder GetDecoder()`
  （解码器 获取解码器（））
- `Encoder GetEncoder()`
  （编码器 获取编码器（））

---

## EncodingProvider（Encoding提供者）

### 字段 (2)

- `object s_InternalSyncObject`（对象 s_内部同步对象）(偏移: 0x0)
- `EncodingProvider[] s_providers`（EncodingProvider[] s_providers）(偏移: 0x4)

### 方法 (4)

- `Encoding GetEncoding(int codepage, EncoderFallback encoderFallback, DecoderFallback decoderFallback)`
  （Encoding 获取Encoding（int codepage, EncoderFallback encoderFallback, DecoderFallback decoderFallback））
- `Encoding GetEncodingFromProvider(int codepage)`
  （Encoding 获取EncodingFrom提供者（int codepage））
- `Encoding GetEncodingFromProvider(string encodingName)`
  （Encoding 获取EncodingFrom提供者（string encodingName））
- `Encoding GetEncodingFromProvider(int codepage, EncoderFallback enc, DecoderFallback dec)`
  （Encoding 获取EncodingFrom提供者（int codepage, EncoderFallback enc, DecoderFallback dec））

---

## EncodingTable（EncodingTable）

### 字段 (5)

- `InternalEncodingDataItem[] encodingDataPtr`（内部的Encoding数据Item[] encoding数据Ptr）(偏移: 0x0)
- `InternalCodePageDataItem[] codePageDataPtr`（内部的CodePage数据Item[] codePage数据Ptr）(偏移: 0x4)
- `int lastEncodingItem`（int lastEncoding项目）(偏移: 0x8)
- `Hashtable hashByName`（Hashtable hashBy名称）(偏移: 0xC)
- `Hashtable hashByCodePage`（Hashtable hashByCodePage）(偏移: 0x10)

### 方法 (6)

- `int GetNumEncodingItems()`
  （int 获取NumEncodingItems（））
- `InternalEncodingDataItem ENC(string name, ushort cp)`
  （内部的Encoding数据项目 ENC（string name, ushort cp））
- `InternalCodePageDataItem MapCodePageDataItem(ushort cp, ushort fcp, string names, uint flags)`
  （内部的CodePage数据项目 映射CodePage数据项目（ushort cp, ushort fcp, string names, uint flags））
- `int internalGetCodePageFromName(string name)`
  （int internal获取CodePageFrom名称（string name））
- `int GetCodePageFromName(string name)`
  （int 获取CodePageFrom名称（string name））
- `CodePageDataItem GetCodePageDataItem(int codepage)`
  （CodePage数据项目 获取CodePage数据项目（int codepage））

---

## EncryptionAlgorithm（EncryptionAlgorithm）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## EndingConditionDistance（EndingCondition距离）

**继承**: PathEndingCondition（路径EndingCondition）

### 字段 (1)

- `int maxGScore`（int maxG分数）(偏移: 0xC)

### 方法 (1)

- `bool TargetFound(PathNode node)`
  （bool 目标Found（路径节点 node））

---

## EndingConditionProximity（EndingConditionProximity）

**继承**: ABPathEndingCondition（AB路径EndingCondition）

### 字段 (1)

- `float maxDistance`（float max距离）(偏移: 0x10)

### 方法 (1)

- `bool TargetFound(PathNode node)`
  （bool 目标Found（路径节点 node））

---

## Entity（实体）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (9)

- `float baseMoveSpeed`（float base移动Speed）(偏移: 0xC)
- `Action<Team> team_Listenner`（Action<Team> team_Listenner）(偏移: 0x24)
- `bool isGhostEntity`（bool is幽灵实体）(偏移: 0x30)
- `bool isNoHitFeedback`（bool isNo命中Feedback）(偏移: 0x31)
- `List<Buff> buffs`（List<Buff> buffs）(偏移: 0x34)
- `Action<bool> LifeState_Listenner`（Action<bool> LifeState_Listenner）(偏移: 0x38)
- `Ref2Float SpeedPenalty_BuffUpdater`（双引用浮点数 SpeedPenalty_增益Updater）(偏移: 0x3C)
- `Ref2Float DamageRate_BuffUpdater`（双引用浮点数 伤害Rate_增益Updater）(偏移: 0x40)
- `RefBool Invincible_BuffUpdater`（引用布尔值 Invincible_增益Updater）(偏移: 0x44)

### 方法 (50)

- `float get_speedPenalty()`
  （float get_speed惩罚（））
- `void set_speedPenalty(float value)`
  （void set_speed惩罚（float value））
- `float get_damageRate()`
  （float get_damageRate（））
- `void set_damageRate(float value)`
  （void set_damageRate（float value））
- `bool get_isInvincible()`
  （bool get_isInvincible（））
- `void set_isInvincible(bool value)`
  （void set_isInvincible（bool value））
- `HealthData get_healthData()`
  （Health数据 get_health数据（））
- `void set_healthData(HealthData value)`
  （void set_health数据（Health数据 value））
- `bool get_isDead()`
  （布尔值 获取_是否死亡（））
- `bool get_isBlackList()`
  （bool get_isBlack列表（））
- `bool get_isGlobalRisk()`
  （bool get_is全局的Risk（））
- `Team get_team()`
  （队伍 get_team（））
- `void set_team(Team value)`
  （void set_team（队伍 value））
- `void add_team_Listenner(Action<Team> value)`
  （void add_team_Listenner（Action<Team> value））
- `void remove_team_Listenner(Action<Team> value)`
  （void remove_team_Listenner（Action<Team> value））
- `Animator get_characterAnimator()`
  （动画器 get_character动画器（））
- `void set_characterAnimator(Animator value)`
  （void set_character动画器（动画器 value））
- `CharacterController get_characterController()`
  （角色控制器 get_character控制器（））
- `void set_characterController(CharacterController value)`
  （void set_character控制器（角色控制器 value））
- `void add_LifeState_Listenner(Action<bool> value)`
  （void add_LifeState_Listenner（Action<bool> value））
- `void remove_LifeState_Listenner(Action<bool> value)`
  （void remove_LifeState_Listenner（Action<bool> value））
- `void add_SpeedPenalty_BuffUpdater(Ref2Float value)`
  （void add_SpeedPenalty_增益Updater（双引用浮点数 value））
- `void remove_SpeedPenalty_BuffUpdater(Ref2Float value)`
  （void remove_SpeedPenalty_增益Updater（双引用浮点数 value））
- `void add_DamageRate_BuffUpdater(Ref2Float value)`
  （void add_伤害Rate_增益Updater（双引用浮点数 value））
- `void remove_DamageRate_BuffUpdater(Ref2Float value)`
  （void remove_伤害Rate_增益Updater（双引用浮点数 value））
- `void add_Invincible_BuffUpdater(RefBool value)`
  （void add_Invincible_增益Updater（引用布尔值 value））
- `void remove_Invincible_BuffUpdater(RefBool value)`
  （void remove_Invincible_增益Updater（引用布尔值 value））
- `void Awake()`
  （void 唤醒（））
- `void Update()`
  （void 更新（））
- `void OnDestroy()`
  （void 销毁时（））
- `void SetTeam(Team newTeam)`
  （void 集合队伍（队伍 newTeam））
- `void RemoveFromTeamList(bool onlyAliveList)`
  （void 移除From队伍列表（bool onlyAliveList））
- `void AddToTeamList(bool isAliveList)`
  （void 添加To队伍列表（bool isAliveList））
- `int GetLocalDirection(Vector3 point, bool inverse = False)`
  （int 获取本地的方向（三维向量 point, bool inverse = False））
- `void Spawn()`
  （void 出生（））
- `void OnEntityHurt(DamageEventData eventData)`
  （void On实体Hurt（伤害事件数据 eventData））
- `void OnEntityDeath(DeathEventData eventData)`
  （void On实体死亡（死亡事件数据 eventData））
- `Buff AddSpeedPenalty(float penalty, float time, string buffName = "Simple")`
  （增益 添加Speed惩罚（float penalty, float time, string buffName = "Simple"））
- `Buff SetDamageRate(float subRate, float time)`
  （增益 集合伤害Rate（float subRate, float time））
- `void RemoveBuff(string buffName)`
  （void 移除增益（string buffName））
- `void CleanAllBuff(int priority = 0)`
  （void Clean所有增益（int priority = 0））
- `Buff FindBuff(string buffName)`
  （增益 查找增益（string buffName））
- `void AddBuff(Buff newBuff)`
  （void 添加增益（增益 newBuff））
- `Buff TryAddBuff(string buffName, float duration, Func<Buff> buffCreater)`
  （增益 Try添加增益（string buffName, float duration, Func<Buff> buffCreater））
- `void UpdateBuff()`
  （void 更新增益（））
- `void UpdateBuffProperty()`
  （void 更新增益属性（））
- `void SetGhostEntityState(bool isGhost)`
  （void 集合幽灵实体状态（bool isGhost））
- `void UpdateColliderLayer()`
  （void 更新碰撞器层（））
- `string GetName()`
  （字符串 获取名称（））
- `Transform GetVisibleHitBox(Ray viewRay)`
  （变换 获取可见命中框（射线 viewRay））

---

## Enum（Enum）

**继承**: ValueType, IComparable, IFormattable, IConvertible（值类型, IComparable, IFormattable, IConvertible）

### 字段 (1)

- `char[] enumSeperatorCharArray`（char[] enumSeperatorChar数组）(偏移: 0x0)

### 方法 (42)

- `Enum.ValuesAndNames GetCachedValuesAndNames(RuntimeType enumType, bool getNames)`
  （Enum.ValuesAndNames 获取CachedValuesAndNames（Runtime类型 enumType, bool getNames））
- `string InternalFormattedHexString(object value)`
  （string 内部的FormattedHex字符串（object value））
- `string InternalFormat(RuntimeType eT, object value)`
  （string 内部的格式化（Runtime类型 eT, object value））
- `string InternalFlagsFormat(RuntimeType eT, object value)`
  （string 内部的Flags格式化（Runtime类型 eT, object value））
- `ulong ToUInt64(object value)`
  （ulong ToUInt64（object value））
- `int InternalCompareTo(object o1, object o2)`
  （int 内部的CompareTo（object o1, object o2））
- `RuntimeType InternalGetUnderlyingType(RuntimeType enumType)`
  （Runtime类型 内部的获取Underlying类型（Runtime类型 enumType））
- `bool GetEnumValuesAndNames(RuntimeType enumType, out ulong[] values, out string[] names)`
  （bool 获取EnumValuesAndNames（Runtime类型 enumType, out ulong[] values, out string[] names））
- `object InternalBoxEnum(RuntimeType enumType, long value)`
  （object 内部的BoxEnum（Runtime类型 enumType, long value））
- `object Parse(Type enumType, string value)`
  （object 解析（类型 enumType, string value））
- `object Parse(Type enumType, string value, bool ignoreCase)`
  （object 解析（类型 enumType, string value, bool ignoreCase））
- `bool TryParseEnum(Type enumType, string value, bool ignoreCase, ref Enum.EnumResult parseResult)`
  （bool Try解析Enum（类型 enumType, string value, bool ignoreCase, ref Enum.EnumResult parseResult））
- `Type GetUnderlyingType(Type enumType)`
  （类型 获取Underlying类型（类型 enumType））
- `Array GetValues(Type enumType)`
  （数组 获取Values（类型 enumType））
- `ulong[] InternalGetValues(RuntimeType enumType)`
  （ulong[] 内部的获取Values（Runtime类型 enumType））
- `string GetName(Type enumType, object value)`
  （string 获取名称（类型 enumType, object value））
- `string[] GetNames(Type enumType)`
  （string[] 获取Names（类型 enumType））
- `string[] InternalGetNames(RuntimeType enumType)`
  （string[] 内部的获取Names（Runtime类型 enumType））
- `object ToObject(Type enumType, object value)`
  （object To对象（类型 enumType, object value））
- `bool IsDefined(Type enumType, object value)`
  （bool 是否Defined（类型 enumType, object value））
- `string Format(Type enumType, object value, string format)`
  （string 格式化（类型 enumType, object value, string format））
- `object get_value()`
  （object get_value（））
- `object GetValue()`
  （object 获取值（））
- `int get_hashcode()`
  （int get_hashcode（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `string ToString()`
  （字符串 转字符串（））
- `string ToString(string format, IFormatProvider provider)`
  （字符串 转字符串（字符串 格式, I格式化提供者 provider））
- `int CompareTo(object target)`
  （int CompareTo（object target））
- `string ToString(string format)`
  （字符串 转字符串（字符串 格式））
- `string ToString(IFormatProvider provider)`
  （字符串 转字符串（I格式化提供者 provider））
- `TypeCode GetTypeCode()`
  （类型代码 获取类型代码（））
- `object ToObject(Type enumType, sbyte value)`
  （object To对象（类型 enumType, sbyte value））
- `object ToObject(Type enumType, short value)`
  （object To对象（类型 enumType, short value））
- `object ToObject(Type enumType, int value)`
  （object To对象（类型 enumType, int value））
- `object ToObject(Type enumType, byte value)`
  （object To对象（类型 enumType, byte value））
- `object ToObject(Type enumType, ushort value)`
  （object To对象（类型 enumType, ushort value））
- `object ToObject(Type enumType, uint value)`
  （object To对象（类型 enumType, uint value））
- `object ToObject(Type enumType, long value)`
  （object To对象（类型 enumType, long value））
- `object ToObject(Type enumType, ulong value)`
  （object To对象（类型 enumType, ulong value））
- `object ToObject(Type enumType, char value)`
  （object To对象（类型 enumType, char value））
- `object ToObject(Type enumType, bool value)`
  （object To对象（类型 enumType, bool value））

---

## Enum.EnumResult（Enum.EnumResult）

### 字段 (7)

- `object parsedEnum`（object parsedEnum）(偏移: 0x0)
- `bool canThrow`（bool can投掷）(偏移: 0x4)
- `Enum.ParseFailureKind m_failure`（Enum.解析FailureKind m_failure）(偏移: 0x8)
- `string m_failureMessageID`（string m_failureMessageID）(偏移: 0xC)
- `string m_failureParameter`（string m_failureParameter）(偏移: 0x10)
- `object m_failureMessageFormatArgument`（object m_failureMessage格式化Argument）(偏移: 0x14)
- `Exception m_innerException`（Exception m_innerException）(偏移: 0x18)

### 方法 (5)

- `void Init(bool canMethodThrow)`
  （void 初始化（bool canMethodThrow））
- `void SetFailure(Exception unhandledException)`
  （void 集合Failure（Exception unhandledException））
- `void SetFailure(Enum.ParseFailureKind failure, string failureParameter)`
  （void 集合Failure（Enum.解析FailureKind failure, string failureParameter））
- `void SetFailure(Enum.ParseFailureKind failure, string failureMessageID, object failureMessageFormatArgument)`
  （void 集合Failure（Enum.解析FailureKind failure, string failureMessageID, object failureMessageFormatArgument））
- `Exception GetEnumParseException()`
  （Exception 获取Enum解析Exception（））

---

## Enum.ParseFailureKind（Enum.解析FailureKind）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Enum.ValuesAndNames（Enum.ValuesAndNames）

### 字段 (2)

- `ulong[] Values`（ulong[] Values）(偏移: 0x8)
- `string[] Names`（string[] Names）(偏移: 0xC)

---

## EnumBuilder（Enum构建器）

**继承**: TypeInfo（类型信息）

### 方法 (32)

- `Assembly get_Assembly()`
  （程序集 获取_程序集（））
- `string get_AssemblyQualifiedName()`
  （string get_AssemblyQualified名称（））
- `Type get_BaseType()`
  （类型 get_基础类型（））
- `string get_FullName()`
  （字符串 获取_全名称（））
- `Module get_Module()`
  （模块 获取_模块（））
- `string get_Name()`
  （字符串 获取_名称（））
- `string get_Namespace()`
  （string get_Namespace（））
- `Type GetElementType()`
  （类型 获取元素类型（））
- `Type get_UnderlyingSystemType()`
  （类型 get_Underlying系统类型（））
- `TypeAttributes GetAttributeFlagsImpl()`
  （类型Attributes 获取AttributeFlagsImpl（））
- `ConstructorInfo GetConstructorImpl(BindingFlags bindingAttr, Binder binder, CallingConventions callConvention, Type[] types, ParameterModifier[] modifiers)`
  （Constructor信息 获取ConstructorImpl（BindingFlags bindingAttr, Binder binder, CallingConventions callConvention, Type[] types, ParameterModifier[] modifiers））
- `ConstructorInfo[] GetConstructors(BindingFlags bindingAttr)`
  （ConstructorInfo[] 获取Constructors（BindingFlags bindingAttr））
- `object[] GetCustomAttributes(bool inherit)`
  （对象[] 获取自定义属性（布尔值 继承））
- `object[] GetCustomAttributes(Type attributeType, bool inherit)`
  （对象[] 获取自定义属性（类型 attributeType, 布尔值 继承））
- `EventInfo GetEvent(string name, BindingFlags bindingAttr)`
  （事件信息 获取事件（string name, BindingFlags bindingAttr））
- `EventInfo[] GetEvents(BindingFlags bindingAttr)`
  （事件Info[] 获取Events（BindingFlags bindingAttr））
- `FieldInfo GetField(string name, BindingFlags bindingAttr)`
  （Field信息 获取Field（string name, BindingFlags bindingAttr））
- `FieldInfo[] GetFields(BindingFlags bindingAttr)`
  （FieldInfo[] 获取Fields（BindingFlags bindingAttr））
- `Type[] GetInterfaces()`
  （Type[] 获取Interfaces（））
- `MethodInfo GetMethodImpl(string name, BindingFlags bindingAttr, Binder binder, CallingConventions callConvention, Type[] types, ParameterModifier[] modifiers)`
  （Method信息 获取MethodImpl（string name, BindingFlags bindingAttr, Binder binder, CallingConventions callConvention, Type[] types, ParameterModifier[] modifiers））
- `MethodInfo[] GetMethods(BindingFlags bindingAttr)`
  （MethodInfo[] 获取Methods（BindingFlags bindingAttr））
- `Type GetNestedType(string name, BindingFlags bindingAttr)`
  （类型 获取Nested类型（string name, BindingFlags bindingAttr））
- `PropertyInfo[] GetProperties(BindingFlags bindingAttr)`
  （属性Info[] 获取Properties（BindingFlags bindingAttr））
- `PropertyInfo GetPropertyImpl(string name, BindingFlags bindingAttr, Binder binder, Type returnType, Type[] types, ParameterModifier[] modifiers)`
  （属性信息 获取属性Impl（string name, BindingFlags bindingAttr, Binder binder, 类型 returnType, Type[] types, ParameterModifier[] modifiers））
- `bool HasElementTypeImpl()`
  （bool 是否有元素类型Impl（））
- `object InvokeMember(string name, BindingFlags invokeAttr, Binder binder, object target, object[] args, ParameterModifier[] modifiers, CultureInfo culture, string[] namedParameters)`
  （object InvokeMember（string name, BindingFlags invokeAttr, Binder binder, object target, object[] args, ParameterModifier[] modifiers, Culture信息 culture, string[] namedParameters））
- `bool IsArrayImpl()`
  （bool 是否数组Impl（））
- `bool IsByRefImpl()`
  （bool 是否ByRefImpl（））
- `bool IsCOMObjectImpl()`
  （bool 是否COM对象Impl（））
- `bool IsDefined(Type attributeType, bool inherit)`
  （布尔值 是否已定义（类型 attributeType, 布尔值 继承））
- `bool IsPointerImpl()`
  （bool 是否指针Impl（））
- `bool IsPrimitiveImpl()`
  （bool 是否PrimitiveImpl（））

---

## EnumConverter（EnumConverter）

**继承**: TypeConverter（类型转换器）

### 字段 (2)

- `TypeConverter.StandardValuesCollection values`（类型Converter.StandardValuesCollection values）(偏移: 0x8)
- `Type type`（类型 type）(偏移: 0xC)

### 方法 (12)

- `Type get_EnumType()`
  （类型 get_Enum类型（））
- `TypeConverter.StandardValuesCollection get_Values()`
  （类型Converter.StandardValuesCollection get_Values（））
- `void set_Values(TypeConverter.StandardValuesCollection value)`
  （void set_Values（类型Converter.StandardValuesCollection value））
- `bool CanConvertFrom(ITypeDescriptorContext context, Type sourceType)`
  （布尔值 能否转换自（I类型描述符上下文 context, 类型 sourceType））
- `bool CanConvertTo(ITypeDescriptorContext context, Type destinationType)`
  （布尔值 能否转换到（I类型描述符上下文 context, 类型 destinationType））
- `IComparer get_Comparer()`
  （IComparer get_Comparer（））
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
- `bool IsValid(ITypeDescriptorContext context, object value)`
  （bool 是否Valid（I类型DescriptorContext context, object value））

---

## Environment（Environment）

### 字段 (2)

- `string nl`（string nl）(偏移: 0x0)
- `OperatingSystem os`（Operating系统 os）(偏移: 0x4)

### 方法 (35)

- `string GetResourceString(string key)`
  （string 获取资源字符串（string key））
- `string GetResourceString(string key, object[] values)`
  （string 获取资源字符串（string key, object[] values））
- `string GetResourceStringEncodingName(int codePage)`
  （string 获取资源字符串Encoding名称（int codePage））
- `int get_CurrentManagedThreadId()`
  （int get_当前ManagedThreadId（））
- `bool get_HasShutdownStarted()`
  （bool get_是否有ShutdownStarted（））
- `string GetNewLine()`
  （string 获取新的Line（））
- `string get_NewLine()`
  （string get_新的Line（））
- `PlatformID get_Platform()`
  （PlatformID get_Platform（））
- `string GetOSVersionString()`
  （string 获取OSVersion字符串（））
- `OperatingSystem get_OSVersion()`
  （Operating系统 get_OSVersion（））
- `Version CreateVersionFromString(string info)`
  （Version 创建VersionFrom字符串（string info））
- `string get_StackTrace()`
  （string get_栈Trace（））
- `int get_TickCount()`
  （int get_Tick数量（））
- `void Exit(int exitCode)`
  （void Exit（int exitCode））
- `string ExpandEnvironmentVariables(string name)`
  （string ExpandEnvironmentVariables（string name））
- `string[] GetCommandLineArgs()`
  （string[] 获取CommandLineArgs（））
- `string internalGetEnvironmentVariable_native(IntPtr variable)`
  （string internal获取EnvironmentVariable_native（整数Ptr variable））
- `string internalGetEnvironmentVariable(string variable)`
  （string internal获取EnvironmentVariable（string variable））
- `string GetEnvironmentVariable(string variable)`
  （string 获取EnvironmentVariable（string variable））
- `Hashtable GetEnvironmentVariablesNoCase()`
  （Hashtable 获取EnvironmentVariablesNoCase（））
- `string GetFolderPath(Environment.SpecialFolder folder)`
  （string 获取Folder路径（Environment.特殊Folder folder））
- `string GetWindowsFolderPath(int folder)`
  （string 获取WindowsFolder路径（int folder））
- `string GetFolderPath(Environment.SpecialFolder folder, Environment.SpecialFolderOption option)`
  （string 获取Folder路径（Environment.特殊Folder folder, Environment.特殊FolderOption option））
- `string ReadXdgUserDir(string config_dir, string home_dir, string key, string fallback)`
  （string ReadXdgUserDir（string config_dir, string home_dir, string key, string fallback））
- `string UnixGetFolderPath(Environment.SpecialFolder folder, Environment.SpecialFolderOption option)`
  （string Unix获取Folder路径（Environment.特殊Folder folder, Environment.特殊FolderOption option））
- `void FailFast(string message)`
  （void FailFast（string message））
- `void FailFast(string message, Exception exception)`
  （void FailFast（string message, Exception exception））
- `bool get_Is64BitProcess()`
  （bool get_Is64Bit处理（））
- `int get_ProcessorCount()`
  （int get_Processor数量（））
- `bool get_IsRunningOnWindows()`
  （bool get_是否RunningOnWindows（））
- `string[] GetEnvironmentVariableNames()`
  （string[] 获取EnvironmentVariableNames（））
- `string GetMachineConfigPath()`
  （string 获取Machine配置路径（））
- `string internalGetHome()`
  （string internal获取Home（））
- `int GetPageSize()`
  （int 获取Page大小（））
- `string GetStackTrace(Exception e, bool needFileInfo)`
  （string 获取栈Trace（Exception e, bool needFileInfo））

---

## Environment.SpecialFolder（Environment.特殊Folder）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Environment.SpecialFolderOption（Environment.特殊FolderOption）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## EnvoyInfo（Envoy信息）

**继承**: IEnvoyInfo（IEnvoy信息）

### 字段 (1)

- `IMessageSink envoySinks`（IMessageSink envoySinks）(偏移: 0x8)

### 方法 (1)

- `IMessageSink get_EnvoySinks()`
  （IMessageSink get_EnvoySinks（））

---

## EnvoyTerminatorSink（EnvoyTerminatorSink）

**继承**: IMessageSink（IMessage接收器）

### 字段 (1)

- `EnvoyTerminatorSink Instance`（EnvoyTerminatorSink 实例）(偏移: 0x0)

### 方法 (2)

- `IMessage SyncProcessMessage(IMessage msg)`
  （IMessage 同步处理消息（IMessage msg））
- `IMessageCtrl AsyncProcessMessage(IMessage msg, IMessageSink replySink)`
  （IMessageCtrl 异步处理消息（IMessage msg, IMessageSink replySink））

---

## Ephemeron（Ephemeron）

### 字段 (2)

- `object key`（对象 key）(偏移: 0x0)
- `object value`（对象 value）(偏移: 0x4)

---

## EraInfo（Era信息）

### 字段 (8)

- `int era`（int era）(偏移: 0x8)
- `long ticks`（long ticks）(偏移: 0x10)
- `int yearOffset`（int yearOffset）(偏移: 0x18)
- `int minEraYear`（int minEraYear）(偏移: 0x1C)
- `int maxEraYear`（int maxEraYear）(偏移: 0x20)
- `string eraName`（string era名称）(偏移: 0x24)
- `string abbrevEraName`（string abbrevEra名称）(偏移: 0x28)
- `string englishEraName`（string englishEra名称）(偏移: 0x2C)

---

## Error（Error）

### 方法 (4)

- `Exception ArgumentNull(string s)`
  （Exception ArgumentNull（string s））
- `Exception ArgumentOutOfRange(string s)`
  （Exception ArgumentOutOf范围（string s））
- `Exception MoreThanOneMatch()`
  （Exception MoreThanOne比赛（））
- `Exception NoElements()`
  （Exception NoElements（））

---

## ErrorMessage（ErrorMessage）

**继承**: IMethodCallMessage, IMethodMessage, IMessage（IMethodCallMessage, IMethodMessage, IMessage）

### 字段 (1)

- `string _uri`（字符串 _uri）(偏移: 0x8)

### 方法 (10)

- `int get_ArgCount()`
  （整数 获取_参数数量（））
- `object[] get_Args()`
  （对象[] 获取_参数（））
- `MethodBase get_MethodBase()`
  （方法基类 获取_方法基类（））
- `string get_MethodName()`
  （字符串 获取_方法名称（））
- `object get_MethodSignature()`
  （对象 获取_方法签名（））
- `IDictionary get_Properties()`
  （I字典 获取_属性（））
- `string get_TypeName()`
  （字符串 获取_类型名称（））
- `string get_Uri()`
  （字符串 获取_Uri（））
- `object GetArg(int arg_num)`
  （object 获取Arg（int arg_num））
- `LogicalCallContext get_LogicalCallContext()`
  （逻辑调用上下文 获取_逻辑调用上下文（））

---

## ErrorWrapper（Error包装器）

### 字段 (1)

- `int m_ErrorCode`（int m_ErrorCode）(偏移: 0x8)

---

## EtwSession（EtwSession）

### 字段 (3)

- `int m_etwSessionId`（int m_etwSessionId）(偏移: 0x8)
- `ActivityFilter m_activityFilter`（ActivityFilter m_activityFilter）(偏移: 0xC)
- `List<WeakReference<EtwSession>> s_etwSessions`（List<WeakReference<EtwSession>> s_etwSessions）(偏移: 0x0)

### 方法 (3)

- `EtwSession GetEtwSession(int etwSessionId, bool bCreateIfNeeded = False)`
  （EtwSession 获取EtwSession（int etwSessionId, bool bCreateIfNeeded = False））
- `void RemoveEtwSession(EtwSession etwSession)`
  （void 移除EtwSession（EtwSession etwSession））
- `void TrimGlobalList()`
  （void Trim全局的列表（））

---

## EuclideanEmbedding（EuclideanEmbedding）

### 字段 (11)

- `HeuristicOptimizationMode mode`（HeuristicOptimization模式 mode）(偏移: 0x8)
- `int seed`（int seed）(偏移: 0xC)
- `Transform pivotPointRoot`（变换 pivotPoint根）(偏移: 0x10)
- `int spreadOutCount`（int spreadOut数量）(偏移: 0x14)
- `bool dirty`（bool dirty）(偏移: 0x18)
- `uint[] costs`（uint[] costs）(偏移: 0x1C)
- `int maxNodeIndex`（int max节点索引）(偏移: 0x20)
- `int pivotCount`（int pivot数量）(偏移: 0x24)
- `GraphNode[] pivots`（GraphNode[] pivots）(偏移: 0x28)
- `uint rval`（uint rval）(偏移: 0x2C)
- `object lockObj`（object lockObj）(偏移: 0x30)

### 方法 (10)

- `uint GetRandom()`
  （uint 获取随机（））
- `void EnsureCapacity(int index)`
  （void EnsureCapacity（int index））
- `uint GetHeuristic(int nodeIndex1, int nodeIndex2)`
  （uint 获取Heuristic（int nodeIndex1, int nodeIndex2））
- `void GetClosestWalkableNodesToChildrenRecursively(Transform tr, List<GraphNode> nodes)`
  （void 获取ClosestWalkableNodesToChildrenRecursively（变换 tr, List<GraphNode> nodes））
- `void PickNRandomNodes(int count, List<GraphNode> buffer)`
  （void PickN随机Nodes（int count, List<GraphNode> buffer））
- `GraphNode PickAnyWalkableNode()`
  （Graph节点 Pick任意Walkable节点（））
- `void RecalculatePivots()`
  （void RecalculatePivots（））
- `void RecalculateCosts()`
  （void RecalculateCosts（））
- `void ApplyGridGraphEndpointSpecialCase()`
  （void 应用网格GraphEndpoint特殊Case（））
- `void OnDrawGizmos()`
  （void 绘制辅助线时（））

---

## Event（事件）

### 字段 (3)

- `IntPtr m_Ptr`（整数指针 m_指针）(偏移: 0x8)
- `Event s_Current`（事件 s_当前）(偏移: 0x0)
- `Event s_MasterEvent`（事件 s_Master事件）(偏移: 0x4)

### 方法 (31)

- `EventType get_rawType()`
  （事件类型 get_raw类型（））
- `Vector2 get_mousePosition()`
  （二维向量 get_mousePosition（））
- `PointerType get_pointerType()`
  （指针类型 get_pointer类型（））
- `EventModifiers get_modifiers()`
  （事件Modifiers get_modifiers（））
- `int get_clickCount()`
  （int get_click数量（））
- `char get_character()`
  （char get_character（））
- `KeyCode get_keyCode()`
  （键Code get_keyCode（））
- `void set_displayIndex(int value)`
  （void set_display索引（int value））
- `EventType get_type()`
  （事件类型 get_type（））
- `string get_commandName()`
  （string get_command名称（））
- `void Internal_Use()`
  （void Internal_Use（））
- `IntPtr Internal_Create(int displayIndex)`
  （整数Ptr Internal_创建（int displayIndex））
- `void Internal_Destroy(IntPtr ptr)`
  （void 内部_销毁（整数指针 ptr））
- `EventType GetTypeForControl(int controlID)`
  （事件类型 获取类型For控制（int controlID））
- `bool PopEvent(Event outEvent)`
  （bool Pop事件（事件 outEvent））
- `void Internal_SetNativeEvent(IntPtr ptr)`
  （void Internal_集合Native事件（整数Ptr ptr））
- `void Internal_MakeMasterEventCurrent(int displayIndex)`
  （void Internal_MakeMaster事件当前（int displayIndex））
- `void Finalize()`
  （void 终结（））
- `bool get_shift()`
  （bool get_shift（））
- `bool get_control()`
  （bool get_control（））
- `bool get_alt()`
  （bool get_alt（））
- `bool get_command()`
  （bool get_command（））
- `Event get_current()`
  （事件 get_current（））
- `bool get_isKey()`
  （bool get_is键（））
- `bool get_isMouse()`
  （bool get_is鼠标（））
- `bool get_isDirectManipulationDevice()`
  （bool get_isDirectManipulationDevice（））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `string ToString()`
  （字符串 转字符串（））
- `void Use()`
  （void Use（））
- `void get_mousePosition_Injected(out Vector2 ret)`
  （void get_mousePosition_Injected（out Vector2 ret））

---

## EventActivityOptions（事件ActivityOptions）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## EventArgs（事件参数）

### 字段 (1)

- `EventArgs Empty`（事件Args 空）(偏移: 0x0)

---

## EventAttribute（事件Attribute）

**继承**: Attribute（属性）

### 字段 (2)

- `EventOpcode m_opcode`（事件Opcode m_opcode）(偏移: 0x2C)
- `bool m_opcodeSet`（bool m_opcode集合）(偏移: 0x30)

### 方法 (16)

- `int get_EventId()`
  （int get_事件Id（））
- `void set_EventId(int value)`
  （void set_事件Id（int value））
- `EventLevel get_Level()`
  （事件等级 get_等级（））
- `void set_Level(EventLevel value)`
  （void set_等级（事件等级 value））
- `EventKeywords get_Keywords()`
  （事件Keywords get_Keywords（））
- `EventOpcode get_Opcode()`
  （事件Opcode get_Opcode（））
- `void set_Opcode(EventOpcode value)`
  （void set_Opcode（事件Opcode value））
- `bool get_IsOpcodeSet()`
  （bool get_是否Opcode集合（））
- `EventTask get_Task()`
  （事件Task get_Task（））
- `void set_Task(EventTask value)`
  （void set_Task（事件Task value））
- `byte get_Version()`
  （byte get_Version（））
- `string get_Message()`
  （字符串 获取_消息（））
- `void set_Message(string value)`
  （void set_Message（string value））
- `EventTags get_Tags()`
  （事件Tags get_Tags（））
- `EventActivityOptions get_ActivityOptions()`
  （事件ActivityOptions get_ActivityOptions（））
- `void set_ActivityOptions(EventActivityOptions value)`
  （void set_ActivityOptions（事件ActivityOptions value））

---

## EventAttributes（事件Attributes）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## EventChannel（事件Channel）

### 字段 (1)

- `byte value__`（字节 值__）(偏移: 0x0)

---

## EventCommand（事件Command）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## EventCommandEventArgs（事件Command事件Args）

**继承**: EventArgs（事件参数）

### 字段 (9)

- `EventSource eventSource`（事件Source eventSource）(偏移: 0x10)
- `EventDispatcher dispatcher`（事件Dispatcher dispatcher）(偏移: 0x14)
- `EventListener listener`（事件监听器 listener）(偏移: 0x18)
- `int perEventSourceSessionId`（int per事件SourceSessionId）(偏移: 0x1C)
- `int etwSessionId`（int etwSessionId）(偏移: 0x20)
- `bool enable`（bool enable）(偏移: 0x24)
- `EventLevel level`（事件等级 level）(偏移: 0x28)
- `EventKeywords matchAnyKeyword`（事件Keywords match任意Keyword）(偏移: 0x30)
- `EventCommandEventArgs nextCommand`（事件Command事件Args nextCommand）(偏移: 0x38)

### 方法 (3)

- `EventCommand get_Command()`
  （事件Command get_Command（））
- `void set_Command(EventCommand value)`
  （void set_Command（事件Command value））
- `void set_Arguments(IDictionary<string, string> value)`
  （void set_Arguments（IDictionary<string, string> value））

---

## EventDataAttribute（事件数据Attribute）

**继承**: Attribute（属性）

### 字段 (2)

- `EventLevel level`（事件等级 level）(偏移: 0x8)
- `EventOpcode opcode`（事件Opcode opcode）(偏移: 0xC)

### 方法 (5)

- `string get_Name()`
  （字符串 获取_名称（））
- `EventLevel get_Level()`
  （事件等级 get_等级（））
- `EventOpcode get_Opcode()`
  （事件Opcode get_Opcode（））
- `EventKeywords get_Keywords()`
  （事件Keywords get_Keywords（））
- `EventTags get_Tags()`
  （事件Tags get_Tags（））

---

## EventDescriptor（事件Descriptor）

### 字段 (8)

- `int m_traceloggingId`（int m_traceloggingId）(偏移: 0x0)
- `ushort m_id`（ushort m_id）(偏移: 0x0)
- `byte m_version`（byte m_version）(偏移: 0x2)
- `byte m_channel`（byte m_channel）(偏移: 0x3)
- `byte m_level`（byte m_level）(偏移: 0x4)
- `byte m_opcode`（byte m_opcode）(偏移: 0x5)
- `ushort m_task`（ushort m_task）(偏移: 0x6)
- `long m_keywords`（long m_keywords）(偏移: 0x8)

### 方法 (10)

- `int get_EventId()`
  （int get_事件Id（））
- `byte get_Version()`
  （byte get_Version（））
- `byte get_Channel()`
  （byte get_Channel（））
- `byte get_Level()`
  （byte get_等级（））
- `byte get_Opcode()`
  （byte get_Opcode（））
- `int get_Task()`
  （int get_Task（））
- `long get_Keywords()`
  （long get_Keywords（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `bool Equals(EventDescriptor other)`
  （bool Equals（事件Descriptor other））

---

## EventDescriptorCollection（事件DescriptorCollection）

**继承**: ICollection, IEnumerable, IList（ICollection, IEnumerable, I列表）

### 字段 (8)

- `EventDescriptor[] events`（事件Descriptor[] events）(偏移: 0x8)
- `string[] namedSort`（string[] namedSort）(偏移: 0xC)
- `IComparer comparer`（I比较器 comparer）(偏移: 0x10)
- `bool eventsOwned`（bool eventsOwned）(偏移: 0x14)
- `bool needSort`（bool needSort）(偏移: 0x15)
- `int eventCount`（int event数量）(偏移: 0x18)
- `bool readOnly`（bool readOnly）(偏移: 0x1C)
- `EventDescriptorCollection Empty`（事件DescriptorCollection 空）(偏移: 0x0)

### 方法 (16)

- `int get_Count()`
  （整数 获取_数量（））
- `EventDescriptor get_Item(int index)`
  （事件Descriptor get_项目（int index））
- `EventDescriptor get_Item(string name)`
  （事件Descriptor get_项目（string name））
- `int Add(EventDescriptor value)`
  （int 添加（事件Descriptor value））
- `void Clear()`
  （void 清除（））
- `bool Contains(EventDescriptor value)`
  （bool Contains（事件Descriptor value））
- `void EnsureEventsOwned()`
  （void EnsureEventsOwned（））
- `void EnsureSize(int sizeNeeded)`
  （void Ensure大小（int sizeNeeded））
- `EventDescriptor Find(string name, bool ignoreCase)`
  （事件Descriptor 查找（string name, bool ignoreCase））
- `int IndexOf(EventDescriptor value)`
  （int 索引Of（事件Descriptor value））
- `void Insert(int index, EventDescriptor value)`
  （void Insert（int index, 事件Descriptor value））
- `void Remove(EventDescriptor value)`
  （void 移除（事件Descriptor value））
- `void RemoveAt(int index)`
  （void 移除在（整数 index））
- `IEnumerator GetEnumerator()`
  （IEnumerator 获取枚举器（））
- `void InternalSort(string[] names)`
  （void 内部的Sort（string[] names））
- `void InternalSort(IComparer sorter)`
  （void 内部的Sort（IComparer sorter））

---

## EventDispatcher（事件Dispatcher）

### 字段 (4)

- `EventListener m_Listener`（事件监听器 m_监听器）(偏移: 0x8)
- `bool[] m_EventEnabled`（bool[] m_事件启用的）(偏移: 0xC)
- `bool m_activityFilteringEnabled`（bool m_activityFiltering启用的）(偏移: 0x10)
- `EventDispatcher m_Next`（事件Dispatcher m_下一个）(偏移: 0x14)

---

## EventFieldAttribute（事件FieldAttribute）

**继承**: Attribute（属性）

### 方法 (3)

- `EventFieldTags get_Tags()`
  （事件FieldTags get_Tags（））
- `string get_Name()`
  （字符串 获取_名称（））
- `EventFieldFormat get_Format()`
  （事件Field格式化 get_格式化（））

---

## EventFieldFormat（事件Field格式化）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## EventFieldTags（事件FieldTags）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## EventHandle（事件句柄）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## EventHandler（事件处理器）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(object sender, EventArgs e)`
  （void Invoke（object sender, 事件Args e））
- `IAsyncResult BeginInvoke(object sender, EventArgs e, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（object sender, 事件Args e, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## EventInfo（事件信息）

**继承**: MemberInfo, _EventInfo（Member信息, _事件信息）

### 字段 (1)

- `EventInfo.AddEventAdapter cached_add_event`（事件Info.添加事件适配器 cached_add_event）(偏移: 0x8)

### 方法 (10)

- `Type get_EventHandlerType()`
  （类型 get_事件处理器类型（））
- `MemberTypes get_MemberType()`
  （成员类型 获取_成员类型（））
- `MethodInfo GetAddMethod()`
  （Method信息 获取添加Method（））
- `MethodInfo GetRemoveMethod()`
  （Method信息 获取移除Method（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `bool op_Equality(EventInfo left, EventInfo right)`
  （bool op_Equality（事件信息 left, 事件信息 right））
- `bool op_Inequality(EventInfo left, EventInfo right)`
  （bool op_Inequality（事件信息 left, 事件信息 right））
- `EventInfo internal_from_handle_type(IntPtr event_handle, IntPtr type_handle)`
  （事件信息 internal_from_handle_type（整数Ptr event_handle, 整数Ptr type_handle））
- `EventInfo GetEventFromHandle(RuntimeEventHandle handle, RuntimeTypeHandle reflectedType)`
  （事件信息 获取事件From句柄（Runtime事件句柄 handle, Runtime类型句柄 reflectedType））

---

## EventInfo.AddEventAdapter（事件Info.添加事件适配器）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(object _this, Delegate dele)`
  （void Invoke（object _this, 委托 dele））
- `IAsyncResult BeginInvoke(object _this, Delegate dele, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（object _this, 委托 dele, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## EventKeywords（事件Keywords）

### 字段 (1)

- `long value__`（long value__）(偏移: 0x0)

---

## EventLevel（事件等级）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## EventListener（事件监听器）

### 字段 (9)

- `object s_EventSourceCreatedLock`（object s_事件SourceCreatedLock）(偏移: 0x0)
- `EventHandler<EventSourceCreatedEventArgs> _EventSourceCreated`（事件Handler<事件SourceCreated事件Args> _事件SourceCreated）(偏移: 0x8)
- `EventHandler<EventWrittenEventArgs> EventWritten`（事件Handler<事件Written事件Args> 事件Written）(偏移: 0xC)
- `EventListener m_Next`（事件监听器 m_下一个）(偏移: 0x10)
- `ActivityFilter m_activityFilter`（ActivityFilter m_activityFilter）(偏移: 0x14)
- `EventListener s_Listeners`（事件监听器 s_Listeners）(偏移: 0x4)
- `List<WeakReference> s_EventSources`（List<WeakReference> s_事件Sources）(偏移: 0x8)
- `bool s_CreatingListener`（bool s_Creating监听器）(偏移: 0xC)
- `bool s_EventSourceShutdownRegistered`（bool s_事件SourceShutdownRegistered）(偏移: 0xD)

### 方法 (5)

- `void OnEventSourceCreated(EventSource eventSource)`
  （void On事件SourceCreated（事件Source eventSource））
- `void OnEventWritten(EventWrittenEventArgs eventData)`
  （void On事件Written（事件Written事件Args eventData））
- `void AddEventSource(EventSource newEventSource)`
  （void 添加事件Source（事件Source newEventSource））
- `void DisposeOnShutdown(object sender, EventArgs e)`
  （void 释放OnShutdown（object sender, 事件Args e））
- `object get_EventListenersLock()`
  （object get_事件ListenersLock（））

---

## EventManifestOptions（事件ManifestOptions）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## EventModifiers（事件Modifiers）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## EventOpcode（事件Opcode）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## EventPayload（事件Payload）

**继承**: IDictionary<string, object>, ICollection<KeyValuePair<string, object>>, IEnumerable<KeyValuePair<string, object>>, IEnumerable（IDictionary<string, object>, ICollection<键值Pair<string, object>>, IEnumerable<键值Pair<string, object>>, IEnumerable）

### 字段 (2)

- `List<string> m_names`（List<string> m_names）(偏移: 0x8)
- `List<object> m_values`（List<object> m_values）(偏移: 0xC)

### 方法 (12)

- `ICollection<string> get_Keys()`
  （ICollection<string> get_Keys（））
- `void set_Item(string key, object value)`
  （void set_项目（string key, object value））
- `void Add(string key, object value)`
  （void 添加（string key, object value））
- `void Add(KeyValuePair<string, object> payloadEntry)`
  （void 添加（键值Pair<string, object> payloadEntry））
- `void Clear()`
  （void 清除（））
- `bool Contains(KeyValuePair<string, object> entry)`
  （bool Contains（键值Pair<string, object> entry））
- `bool ContainsKey(string key)`
  （bool Contains键（string key））
- `int get_Count()`
  （整数 获取_数量（））
- `bool get_IsReadOnly()`
  （布尔值 获取_是否只读（））
- `void CopyTo(KeyValuePair<string, object>[] payloadEntries, int count)`
  （void 复制To（键值Pair<string, object>[] payloadEntries, int count））
- `bool Remove(KeyValuePair<string, object> entry)`
  （bool 移除（键值Pair<string, object> entry））
- `bool TryGetValue(string key, out object value)`
  （bool Try获取值（string key, out object value））

---

## EventProvider（事件提供者）

**继承**: IDisposable（可释放接口）

### 字段 (13)

- `bool m_setInformationMissing`（bool m_setInformationMissing）(偏移: 0x0)
- `UnsafeNativeMethods.ManifestEtw.EtwEnableCallback m_etwCallback`（UnsafeNativeMethods.ManifestEtw.Etw启用回调 m_etw回调）(偏移: 0x8)
- `GCHandle m_thisGCHandle`（GC句柄 m_thisGC句柄）(偏移: 0xC)
- `long m_regHandle`（long m_reg句柄）(偏移: 0x10)
- `byte m_level`（byte m_level）(偏移: 0x18)
- `long m_anyKeywordMask`（long m_anyKeyword掩码）(偏移: 0x20)
- `long m_allKeywordMask`（long m_allKeyword掩码）(偏移: 0x28)
- `List<EventProvider.SessionInfo> m_liveSessions`（List<事件Provider.SessionInfo> m_liveSessions）(偏移: 0x30)
- `bool m_enabled`（bool m_enabled）(偏移: 0x34)
- `Guid m_providerId`（Guid m_providerId）(偏移: 0x38)
- `bool m_disposed`（布尔值 m_已释放）(偏移: 0x48)
- `EventProvider.WriteEventErrorCode s_returnCode`（事件Provider.Write事件ErrorCode s_returnCode）(偏移: 0x80000000)
- `int[] nibblebits`（int[] nibblebits）(偏移: 0x4)

### 方法 (27)

- `void Register(Guid providerGuid)`
  （void Register（Guid providerGuid））
- `int SetInformation(UnsafeNativeMethods.ManifestEtw.EVENT_INFO_CLASS eventInfoClass, void* data, int dataSize)`
  （int 集合Information（UnsafeNativeMethods.ManifestEtw.EVENT_INFO_CLASS eventInfoClass, void* data, int dataSize））
- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `void Finalize()`
  （void 终结（））
- `void Deregister()`
  （void Deregister（））
- `void EtwEnableCallBack(in Guid sourceId, [In] int controlCode, [In] byte setLevel, [In] long anyKeyword, [In] long allKeyword, [In] UnsafeNativeMethods.ManifestEtw.EVENT_FILTER_DESCRIPTOR* filterData, [In] void* callbackContext)`
  （void Etw启用Call后（in Guid sourceId, [In] int controlCode, [In] byte setLevel, [In] long anyKeyword, [In] long allKeyword, [In] UnsafeNativeMethods.ManifestEtw.EVENT_FILTER_DESCRIPTOR* filterData, [In] void* callbackContext））
- `void EtwEnableCallBackImpl([In] int controlCode, [In] byte setLevel, [In] long anyKeyword, [In] long allKeyword, [In] UnsafeNativeMethods.ManifestEtw.EVENT_FILTER_DESCRIPTOR* filterData)`
  （void Etw启用Call后Impl（[In] int controlCode, [In] byte setLevel, [In] long anyKeyword, [In] long allKeyword, [In] UnsafeNativeMethods.ManifestEtw.EVENT_FILTER_DESCRIPTOR* filterData））
- `void OnControllerCommand(ControllerCommand command, IDictionary<string, string> arguments, int sessionId, int etwSessionId)`
  （void On控制器Command（控制器Command command, IDictionary<string, string> arguments, int sessionId, int etwSessionId））
- `EventLevel get_Level()`
  （事件等级 get_等级（））
- `EventKeywords get_MatchAnyKeyword()`
  （事件Keywords get_比赛任意Keyword（））
- `int FindNull(byte[] buffer, int idx)`
  （int 查找Null（byte[] buffer, int idx））
- `void GetSessionInfoCallback(int etwSessionId, long matchAllKeywords, ref List<EventProvider.SessionInfo> sessionList)`
  （void 获取Session信息回调（int etwSessionId, long matchAllKeywords, ref List<EventProvider.SessionInfo> sessionList））
- `void GetSessionInfo(Action<int, long> action)`
  （void 获取Session信息（Action<int, long> action））
- `int IndexOfSessionInList(List<EventProvider.SessionInfo> sessions, int etwSessionId)`
  （int 索引OfSessionIn列表（List<事件Provider.SessionInfo> sessions, int etwSessionId））
- `bool GetDataFromController(int etwSessionId, UnsafeNativeMethods.ManifestEtw.EVENT_FILTER_DESCRIPTOR* filterData, out ControllerCommand command, out byte[] data, out int dataStart)`
  （bool 获取数据From控制器（int etwSessionId, UnsafeNativeMethods.ManifestEtw.EVENT_FILTER_DESCRIPTOR* filterData, out ControllerCommand command, out byte[] data, out int dataStart））
- `bool IsEnabled()`
  （bool 是否启用的（））
- `bool IsEnabled(byte level, long keywords)`
  （bool 是否启用的（byte level, long keywords））
- `EventProvider.WriteEventErrorCode GetLastWriteEventError()`
  （事件Provider.Write事件ErrorCode 获取最后一个Write事件Error（））
- `void SetLastError(int error)`
  （void 集合最后一个Error（int error））
- `object EncodeObject(ref object data, ref EventProvider.EventData* dataDescriptor, ref byte* dataBuffer, ref uint totalEventSize)`
  （object Encode对象（ref object data, ref EventProvider.EventData* dataDescriptor, ref byte* dataBuffer, ref uint totalEventSize））
- `bool WriteEvent(ref EventDescriptor eventDescriptor, Guid* activityID, Guid* childActivityID, object[] eventPayload)`
  （bool Write事件（ref EventDescriptor eventDescriptor, Guid* activityID, Guid* childActivityID, object[] eventPayload））
- `bool WriteEvent(ref EventDescriptor eventDescriptor, Guid* activityID, Guid* childActivityID, int dataCount, IntPtr data)`
  （bool Write事件（ref EventDescriptor eventDescriptor, Guid* activityID, Guid* childActivityID, int dataCount, 整数Ptr data））
- `bool WriteEventRaw(ref EventDescriptor eventDescriptor, Guid* activityID, Guid* relatedActivityID, int dataCount, IntPtr data)`
  （bool Write事件Raw（ref EventDescriptor eventDescriptor, Guid* activityID, Guid* relatedActivityID, int dataCount, 整数Ptr data））
- `uint EventUnregister()`
  （uint 事件Unregister（））
- `int bitcount(uint n)`
  （int bitcount（uint n））
- `int bitindex(uint n)`
  （int bitindex（uint n））

---

## EventProvider.EventData（事件Provider.事件数据）

### 字段 (3)

- `ulong Ptr`（ulong Ptr）(偏移: 0x0)
- `uint Size`（uint 大小）(偏移: 0x8)
- `uint Reserved`（uint Reserved）(偏移: 0xC)

---

## EventProvider.SessionInfo（事件Provider.Session信息）

### 字段 (2)

- `int sessionIdBit`（int sessionIdBit）(偏移: 0x0)
- `int etwSessionId`（int etwSessionId）(偏移: 0x4)

---

## EventProvider.WriteEventErrorCode（事件Provider.Write事件ErrorCode）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## EventResetMode（事件重置模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## EventSource（事件Source）

**继承**: IDisposable（可释放接口）

### 字段 (29)

- `byte[] providerMetadata`（byte[] providerMetadata）(偏移: 0x8)
- `string m_name`（字符串 m_名称）(偏移: 0xC)
- `int m_id`（int m_id）(偏移: 0x10)
- `Guid m_guid`（Guid m_guid）(偏移: 0x14)
- `EventSource.EventMetadata[] m_eventData`（事件Source.事件Metadata[] m_event数据）(偏移: 0x24)
- `byte[] m_rawManifest`（byte[] m_rawManifest）(偏移: 0x28)
- `EventHandler<EventCommandEventArgs> m_eventCommandExecuted`（事件Handler<事件Command事件Args> m_eventCommandExecuted）(偏移: 0x2C)
- `EventSourceSettings m_config`（事件SourceSettings m_config）(偏移: 0x30)
- `bool m_eventSourceEnabled`（bool m_eventSource启用的）(偏移: 0x34)
- `EventLevel m_level`（事件等级 m_level）(偏移: 0x38)
- `EventKeywords m_matchAnyKeyword`（事件Keywords m_match任意Keyword）(偏移: 0x40)
- `EventDispatcher m_Dispatchers`（事件Dispatcher m_Dispatchers）(偏移: 0x48)
- `EventSource.OverideEventProvider m_provider`（事件Source.Overide事件提供者 m_provider）(偏移: 0x4C)
- `bool m_completelyInited`（bool m_completelyInited）(偏移: 0x50)
- `Exception m_constructionException`（Exception m_constructionException）(偏移: 0x54)
- `byte m_outOfBandMessageCount`（byte m_outOfBandMessage数量）(偏移: 0x58)
- `EventCommandEventArgs m_deferredCommands`（事件Command事件Args m_deferredCommands）(偏移: 0x5C)
- `string[] m_traits`（string[] m_traits）(偏移: 0x60)
- `uint s_currentPid`（uint s_currentPid）(偏移: 0x0)
- `byte m_EventSourceExceptionRecurenceCount`（byte m_事件SourceExceptionRecurence数量）(偏移: 0x80000000)
- `SessionMask m_curLiveSessions`（Session掩码 m_curLiveSessions）(偏移: 0x64)
- `EtwSession[] m_etwSessionIdMap`（EtwSession[] m_etwSessionId映射）(偏移: 0x68)
- `List<EtwSession> m_legacySessions`（List<EtwSession> m_legacySessions）(偏移: 0x6C)
- `long m_keywordTriggers`（long m_keywordTriggers）(偏移: 0x70)
- `SessionMask m_activityFilteringForETWEnabled`（Session掩码 m_activityFilteringForETW启用的）(偏移: 0x78)
- `Action<Guid> s_activityDying`（Action<Guid> s_activityDying）(偏移: 0x4)
- `ActivityTracker m_activityTracker`（ActivityTracker m_activityTracker）(偏移: 0x7C)
- `byte[] namespaceBytes`（byte[] namespaceBytes）(偏移: 0x8)
- `Guid AspNetEventSourceGuid`（Guid AspNet事件SourceGuid）(偏移: 0xC)

### 方法 (78)

- `void WriteMultiMerge(string eventName, ref EventSourceOptions options, TraceLoggingEventTypes eventTypes, Guid* activityID, Guid* childActivityID, object[] values)`
  （void Write多个Merge（string eventName, ref EventSourceOptions options, TraceLogging事件Types eventTypes, Guid* activityID, Guid* childActivityID, object[] values））
- `void WriteMultiMergeInner(string eventName, ref EventSourceOptions options, TraceLoggingEventTypes eventTypes, Guid* activityID, Guid* childActivityID, object[] values)`
  （void Write多个MergeInner（string eventName, ref EventSourceOptions options, TraceLogging事件Types eventTypes, Guid* activityID, Guid* childActivityID, object[] values））
- `void WriteMultiMerge(string eventName, ref EventSourceOptions options, TraceLoggingEventTypes eventTypes, Guid* activityID, Guid* childActivityID, EventSource.EventData* data)`
  （void Write多个Merge（string eventName, ref EventSourceOptions options, TraceLogging事件Types eventTypes, Guid* activityID, Guid* childActivityID, 事件Source.事件Data* data））
- `void WriteCleanup(GCHandle* pPins, int cPins)`
  （void Write清理（GCHandle* pPins, int cPins））
- `void InitializeProviderMetadata()`
  （void 初始化提供者Metadata（））
- `int AddValueToMetaData(List<byte> metaData, string value)`
  （int 添加值ToMeta数据（List<byte> metaData, string value））
- `int HexDigit(char c)`
  （int HexDigit（char c））
- `NameInfo UpdateDescriptor(string name, TraceLoggingEventTypes eventInfo, ref EventSourceOptions options, out EventDescriptor descriptor)`
  （名称信息 更新Descriptor（string name, TraceLogging事件Types eventInfo, ref EventSourceOptions options, out EventDescriptor descriptor））
- `string get_Name()`
  （字符串 获取_名称（））
- `Guid get_Guid()`
  （Guid get_Guid（））
- `bool IsEnabled()`
  （bool 是否启用的（））
- `bool IsEnabled(EventLevel level, EventKeywords keywords)`
  （bool 是否启用的（事件等级 level, 事件Keywords keywords））
- `bool IsEnabled(EventLevel level, EventKeywords keywords, EventChannel channel)`
  （bool 是否启用的（事件等级 level, 事件Keywords keywords, 事件Channel channel））
- `Guid GetGuid(Type eventSourceType)`
  （Guid 获取Guid（类型 eventSourceType））
- `string GetName(Type eventSourceType)`
  （string 获取名称（类型 eventSourceType））
- `void SetCurrentThreadActivityId(Guid activityId)`
  （void 集合当前ThreadActivityId（Guid activityId））
- `Guid get_CurrentThreadActivityId()`
  （Guid get_当前ThreadActivityId（））
- `Guid get_InternalCurrentThreadActivityId()`
  （Guid get_内部的当前ThreadActivityId（））
- `Guid get_FallbackActivityId()`
  （Guid get_FallbackActivityId（））
- `string ToString()`
  （字符串 转字符串（））
- `void OnEventCommand(EventCommandEventArgs command)`
  （void On事件Command（事件Command事件Args command））
- `void WriteEvent(int eventId, int arg1)`
  （void Write事件（int eventId, int arg1））
- `void WriteEvent(int eventId, string arg1, string arg2)`
  （void Write事件（int eventId, string arg1, string arg2））
- `void WriteEvent(int eventId, string arg1, string arg2, string arg3)`
  （void Write事件（int eventId, string arg1, string arg2, string arg3））
- `void WriteEventCore(int eventId, int eventDataCount, EventSource.EventData* data)`
  （void Write事件Core（int eventId, int eventDataCount, 事件Source.事件Data* data））
- `void WriteEventWithRelatedActivityIdCore(int eventId, Guid* relatedActivityId, int eventDataCount, EventSource.EventData* data)`
  （void Write事件WithRelatedActivityIdCore（int eventId, Guid* relatedActivityId, int eventDataCount, 事件Source.事件Data* data））
- `void WriteEvent(int eventId, object[] args)`
  （void Write事件（int eventId, object[] args））
- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `void Finalize()`
  （void 终结（））
- `void WriteStringToListener(EventListener listener, string msg, SessionMask m)`
  （void Write字符串To监听器（事件监听器 listener, string msg, Session掩码 m））
- `void WriteEventRaw(string eventName, ref EventDescriptor eventDescriptor, Guid* activityID, Guid* relatedActivityID, int dataCount, IntPtr data)`
  （void Write事件Raw（string eventName, ref EventDescriptor eventDescriptor, Guid* activityID, Guid* relatedActivityID, int dataCount, 整数Ptr data））
- `void Initialize(Guid eventSourceGuid, string eventSourceName, string[] traits)`
  （void 初始化（Guid eventSourceGuid, string eventSourceName, string[] traits））
- `string GetName(Type eventSourceType, EventManifestOptions flags)`
  （string 获取名称（类型 eventSourceType, 事件ManifestOptions flags））
- `Guid GenerateGuidFromName(string name)`
  （Guid GenerateGuidFrom名称（string name））
- `object DecodeObject(int eventId, int parameterId, ref EventSource.EventData* data)`
  （object Decode对象（int eventId, int parameterId, ref EventSource.EventData* data））
- `EventDispatcher GetDispatcher(EventListener listener)`
  （事件Dispatcher 获取Dispatcher（事件监听器 listener））
- `void WriteEventVarargs(int eventId, Guid* childActivityID, object[] args)`
  （void Write事件Varargs（int eventId, Guid* childActivityID, object[] args））
- `object[] SerializeEventArgs(int eventId, object[] args)`
  （object[] Serialize事件Args（int eventId, object[] args））
- `void LogEventArgsMismatches(ParameterInfo[] infos, object[] args)`
  （void Log事件ArgsMismatches（ParameterInfo[] infos, object[] args））
- `int GetParamLengthIncludingByteArray(ParameterInfo[] parameters)`
  （int 获取ParamLengthIncludingByte数组（ParameterInfo[] parameters））
- `void WriteToAllListeners(int eventId, Guid* childActivityID, int eventDataCount, EventSource.EventData* data)`
  （void WriteTo所有Listeners（int eventId, Guid* childActivityID, int eventDataCount, 事件Source.事件Data* data））
- `void WriteToAllListeners(int eventId, Guid* childActivityID, object[] args)`
  （void WriteTo所有Listeners（int eventId, Guid* childActivityID, object[] args））
- `void DispatchToAllListeners(int eventId, Guid* childActivityID, EventWrittenEventArgs eventCallbackArgs)`
  （void DispatchTo所有Listeners（int eventId, Guid* childActivityID, 事件Written事件Args eventCallbackArgs））
- `void WriteEventString(EventLevel level, long keywords, string msgString)`
  （void Write事件字符串（事件等级 level, long keywords, string msgString））
- `void WriteStringToAllListeners(string eventName, string msg)`
  （void Write字符串To所有Listeners（string eventName, string msg））
- `SessionMask GetEtwSessionMask(int eventId, Guid* childActivityID)`
  （Session掩码 获取EtwSession掩码（int eventId, Guid* childActivityID））
- `bool IsEnabledByDefault(int eventNum, bool enable, EventLevel currentLevel, EventKeywords currentMatchAnyKeyword)`
  （bool 是否启用的By默认的（int eventNum, bool enable, 事件等级 currentLevel, 事件Keywords currentMatchAnyKeyword））
- `bool IsEnabledCommon(bool enabled, EventLevel currentLevel, EventKeywords currentMatchAnyKeyword, EventLevel eventLevel, EventKeywords eventKeywords, EventChannel eventChannel)`
  （bool 是否启用的Common（bool enabled, 事件等级 currentLevel, 事件Keywords currentMatchAnyKeyword, 事件等级 eventLevel, 事件Keywords eventKeywords, 事件Channel eventChannel））
- `void ThrowEventSourceException(string eventName, Exception innerEx)`
  （void 投掷事件SourceException（string eventName, Exception innerEx））
- `void ValidateEventOpcodeForTransfer(ref EventSource.EventMetadata eventData, string eventName)`
  （void 验证事件OpcodeForTransfer（ref EventSource.EventMetadata eventData, string eventName））
- `EventOpcode GetOpcodeWithDefault(EventOpcode opcode, string eventName)`
  （事件Opcode 获取OpcodeWith默认的（事件Opcode opcode, string eventName））
- `void SendCommand(EventListener listener, int perEventSourceSessionId, int etwSessionId, EventCommand command, bool enable, EventLevel level, EventKeywords matchAnyKeyword, IDictionary<string, string> commandArguments)`
  （void 发送Command（事件监听器 listener, int perEventSourceSessionId, int etwSessionId, 事件Command command, bool enable, 事件等级 level, 事件Keywords matchAnyKeyword, IDictionary<string, string> commandArguments））
- `void DoCommand(EventCommandEventArgs commandArgs)`
  （void DoCommand（事件Command事件Args commandArgs））
- `void UpdateEtwSession(int sessionIdBit, int etwSessionId, bool bEnable, string activityFilters, bool participateInSampling)`
  （void 更新EtwSession（int sessionIdBit, int etwSessionId, bool bEnable, string activityFilters, bool participateInSampling））
- `bool ParseCommandArgs(IDictionary<string, string> commandArguments, out bool participateInSampling, out string activityFilters, out int sessionIdBit)`
  （bool 解析CommandArgs（IDictionary<string, string> commandArguments, out bool participateInSampling, out string activityFilters, out int sessionIdBit））
- `void UpdateKwdTriggers(bool enable)`
  （void 更新KwdTriggers（bool enable））
- `bool EnableEventForDispatcher(EventDispatcher dispatcher, int eventId, bool value)`
  （bool 启用事件ForDispatcher（事件Dispatcher dispatcher, int eventId, bool value））
- `bool AnyEventEnabled()`
  （bool 任意事件启用的（））
- `bool get_IsDisposed()`
  （bool get_是否Disposed（））
- `void EnsureDescriptorsInitialized()`
  （void EnsureDescriptorsInitialized（））
- `bool SendManifest(byte[] rawManifest)`
  （bool 发送Manifest（byte[] rawManifest））
- `Attribute GetCustomAttributeHelper(MemberInfo member, Type attributeType, EventManifestOptions flags = 0)`
  （Attribute 获取自定义的Attribute辅助器（Member信息 member, 类型 attributeType, 事件ManifestOptions flags = 0））
- `bool AttributeTypeNamesMatch(Type attributeType, Type reflectedAttributeType)`
  （bool Attribute类型Names比赛（类型 attributeType, 类型 reflectedAttributeType））
- `Type GetEventSourceBaseType(Type eventSourceType, bool allowEventSourceOverride, bool reflectionOnly)`
  （类型 获取事件Source基础类型（类型 eventSourceType, bool allowEventSourceOverride, bool reflectionOnly））
- `byte[] CreateManifestAndDescriptors(Type eventSourceType, string eventSourceDllName, EventSource source, EventManifestOptions flags = 0)`
  （byte[] 创建ManifestAndDescriptors（类型 eventSourceType, string eventSourceDllName, 事件Source source, 事件ManifestOptions flags = 0））
- `bool RemoveFirstArgIfRelatedActivityId(ref ParameterInfo[] args)`
  （bool 移除第一个ArgIfRelatedActivityId（ref ParameterInfo[] args））
- `void AddProviderEnumKind(ManifestBuilder manifest, FieldInfo staticField, string providerEnumKind)`
  （void 添加提供者EnumKind（Manifest构建器 manifest, Field信息 staticField, string providerEnumKind））
- `void AddEventDescriptor(ref EventSource.EventMetadata[] eventData, string eventName, EventAttribute eventAttribute, ParameterInfo[] eventParameters, bool hasRelatedActivityID)`
  （void 添加事件Descriptor（ref EventSource.EventMetadata[] eventData, string eventName, 事件Attribute eventAttribute, ParameterInfo[] eventParameters, bool hasRelatedActivityID））
- `void TrimEventDescriptors(ref EventSource.EventMetadata[] eventData)`
  （void Trim事件Descriptors（ref EventSource.EventMetadata[] eventData））
- `void AddListener(EventListener listener)`
  （void 添加监听器（事件监听器 listener））
- `void DebugCheckEvent(ref Dictionary<string, string> eventsByName, EventSource.EventMetadata[] eventData, MethodInfo method, EventAttribute eventAttribute, ManifestBuilder manifest, EventManifestOptions options)`
  （void Debug检查事件（ref Dictionary<string, string> eventsByName, 事件Source.事件Metadata[] eventData, Method信息 method, 事件Attribute eventAttribute, Manifest构建器 manifest, 事件ManifestOptions options））
- `int GetHelperCallFirstArg(MethodInfo method)`
  （int 获取辅助器Call第一个Arg（Method信息 method））
- `void ReportOutOfBandMessage(string msg, bool flush)`
  （void ReportOutOfBandMessage（string msg, bool flush））
- `EventSourceSettings ValidateSettings(EventSourceSettings settings)`
  （事件SourceSettings 验证Settings（事件SourceSettings settings））
- `bool get_ThrowOnEventWriteErrors()`
  （bool get_投掷On事件WriteErrors（））
- `bool get_SelfDescribingEvents()`
  （bool get_SelfDescribingEvents（））
- `void ReportActivitySamplingInfo(EventListener listener, SessionMask sessions)`
  （void ReportActivitySampling信息（事件监听器 listener, Session掩码 sessions））

---

## EventSource.EventData（事件Source.事件数据）

### 字段 (3)

- `long m_Ptr`（long m_Ptr）(偏移: 0x0)
- `int m_Size`（int m_大小）(偏移: 0x8)
- `int m_Reserved`（int m_Reserved）(偏移: 0xC)

### 方法 (4)

- `IntPtr get_DataPointer()`
  （整数Ptr get_数据指针（））
- `void set_DataPointer(IntPtr value)`
  （void set_数据指针（整数Ptr value））
- `void set_Size(int value)`
  （void set_大小（int value））
- `void SetMetadata(byte* pointer, int size, int reserved)`
  （void 集合Metadata（byte* pointer, int size, int reserved））

---

## EventSource.EventMetadata（事件Source.事件Metadata）

### 字段 (11)

- `EventDescriptor Descriptor`（事件Descriptor Descriptor）(偏移: 0x0)
- `EventTags Tags`（事件Tags Tags）(偏移: 0x10)
- `bool EnabledForAnyListener`（bool 启用的For任意监听器）(偏移: 0x14)
- `bool EnabledForETW`（bool 启用的ForETW）(偏移: 0x15)
- `bool HasRelatedActivityID`（bool 是否有RelatedActivityID）(偏移: 0x16)
- `byte TriggersActivityTracking`（byte TriggersActivityTracking）(偏移: 0x17)
- `string Name`（string 名称）(偏移: 0x18)
- `string Message`（string Message）(偏移: 0x1C)
- `ParameterInfo[] Parameters`（ParameterInfo[] Parameters）(偏移: 0x20)
- `TraceLoggingEventTypes TraceLoggingEventTypes`（TraceLogging事件Types TraceLogging事件Types）(偏移: 0x24)
- `EventActivityOptions ActivityOptions`（事件ActivityOptions ActivityOptions）(偏移: 0x28)

---

## EventSource.OverideEventProvider（事件Source.Overide事件提供者）

**继承**: EventProvider（事件提供者）

### 字段 (1)

- `EventSource m_eventSource`（事件Source m_eventSource）(偏移: 0x50)

### 方法 (1)

- `void OnControllerCommand(ControllerCommand command, IDictionary<string, string> arguments, int perEventSourceSessionId, int etwSessionId)`
  （void On控制器Command（控制器Command command, IDictionary<string, string> arguments, int perEventSourceSessionId, int etwSessionId））

---

## EventSource.Sha1ForNonSecretPurposes（事件Source.Sha1ForNonSecretPurposes）

### 字段 (3)

- `long length`（long length）(偏移: 0x0)
- `uint[] w`（uint[] w）(偏移: 0x8)
- `int pos`（int pos）(偏移: 0xC)

### 方法 (8)

- `void Start()`
  （void 开始（））
- `void Append(byte input)`
  （void Append（byte input））
- `void Append(byte[] input)`
  （void Append（byte[] input））
- `void Finish(byte[] output)`
  （void Finish（byte[] output））
- `void Drain()`
  （void Drain（））
- `uint Rol1(uint input)`
  （uint Rol1（uint input））
- `uint Rol5(uint input)`
  （uint Rol5（uint input））
- `uint Rol30(uint input)`
  （uint Rol30（uint input））

---

## EventSourceAttribute（事件SourceAttribute）

**继承**: Attribute（属性）

### 方法 (5)

- `string get_Name()`
  （字符串 获取_名称（））
- `void set_Name(string value)`
  （void 设置_名称（字符串 value））
- `string get_Guid()`
  （string get_Guid（））
- `void set_Guid(string value)`
  （void set_Guid（string value））
- `string get_LocalizationResources()`
  （string get_LocalizationResources（））

---

## EventSourceCreatedEventArgs（事件SourceCreated事件Args）

**继承**: EventArgs（事件参数）

### 方法 (1)

- `void set_EventSource(EventSource value)`
  （void set_事件Source（事件Source value））

---

## EventSourceOptions（事件SourceOptions）

### 字段 (6)

- `EventKeywords keywords`（事件Keywords keywords）(偏移: 0x0)
- `EventTags tags`（事件标签 tags）(偏移: 0x8)
- `EventActivityOptions activityOptions`（事件ActivityOptions activityOptions）(偏移: 0xC)
- `byte level`（byte level）(偏移: 0x10)
- `byte opcode`（byte opcode）(偏移: 0x11)
- `byte valuesSet`（byte values集合）(偏移: 0x12)

### 方法 (3)

- `void set_Level(EventLevel value)`
  （void set_等级（事件等级 value））
- `void set_Opcode(EventOpcode value)`
  （void set_Opcode（事件Opcode value））
- `void set_Keywords(EventKeywords value)`
  （void set_Keywords（事件Keywords value））

---

