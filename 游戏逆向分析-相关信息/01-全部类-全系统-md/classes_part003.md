# 游戏类定义 (Part 3/21)

共 200 个类 (总序号 401 - 600)

---

## CallContextSecurityData（CallContextSecurity数据）

**继承**: ICloneable（ICloneable可克隆）

### 字段 (1)

- `IPrincipal _principal`（IPrincipal _principal）(偏移: 0x8)

### 方法 (2)

- `bool get_HasInfo()`
  （布尔值 获取_是否有信息（））
- `object Clone()`
  （对象 克隆（））

---

## CallType（Call类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CallingConvention（CallingConvention）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CallingConventions（CallingConventions）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Camera（摄像机）

**继承**: Behaviour（行为）

### 字段 (3)

- `Camera.CameraCallback onPreCull`（Camera.摄像机回调 onPreCull）(偏移: 0x0)
- `Camera.CameraCallback onPreRender`（Camera.摄像机回调 onPreRender）(偏移: 0x4)
- `Camera.CameraCallback onPostRender`（Camera.摄像机回调 onPostRender）(偏移: 0x8)

### 方法 (97)

- `float get_nearClipPlane()`
  （float get_near弹匣Plane（））
- `void set_nearClipPlane(float value)`
  （void set_near弹匣Plane（float value））
- `float get_farClipPlane()`
  （float get_far弹匣Plane（））
- `void set_farClipPlane(float value)`
  （void set_far弹匣Plane（float value））
- `float get_fieldOfView()`
  （float get_fieldOf视图（））
- `void set_fieldOfView(float value)`
  （void set_fieldOf视图（float value））
- `void set_renderingPath(RenderingPath value)`
  （void set_rendering路径（Rendering路径 value））
- `bool get_allowHDR()`
  （bool get_allowHDR（））
- `void set_allowHDR(bool value)`
  （void set_allowHDR（bool value））
- `bool get_allowMSAA()`
  （bool get_allowMSAA（））
- `void set_allowMSAA(bool value)`
  （void set_allowMSAA（bool value））
- `bool get_allowDynamicResolution()`
  （bool get_allow动态的Resolution（））
- `float get_orthographicSize()`
  （float get_orthographic大小（））
- `void set_orthographicSize(float value)`
  （void set_orthographic大小（float value））
- `bool get_orthographic()`
  （bool get_orthographic（））
- `void set_orthographic(bool value)`
  （void set_orthographic（bool value））
- `OpaqueSortMode get_opaqueSortMode()`
  （不透明的Sort模式 get_opaqueSort模式（））
- `float get_depth()`
  （float get_depth（））
- `void set_depth(float value)`
  （void set_depth（float value））
- `float get_aspect()`
  （float get_aspect（））
- `void set_aspect(float value)`
  （void set_aspect（float value））
- `int get_cullingMask()`
  （int get_culling掩码（））
- `void set_cullingMask(int value)`
  （void set_culling掩码（int value））
- `int get_eventMask()`
  （int get_event掩码（））
- `CameraType get_cameraType()`
  （摄像机类型 get_camera类型（））
- `void set_useOcclusionCulling(bool value)`
  （void set_useOcclusionCulling（bool value））
- `Color get_backgroundColor()`
  （颜色 get_background颜色（））
- `void set_backgroundColor(Color value)`
  （void set_background颜色（颜色 value））
- `CameraClearFlags get_clearFlags()`
  （摄像机清除Flags get_clearFlags（））
- `void set_clearFlags(CameraClearFlags value)`
  （void set_clearFlags（摄像机清除Flags value））
- `bool get_usePhysicalProperties()`
  （bool get_usePhysicalProperties（））
- `void set_usePhysicalProperties(bool value)`
  （void set_usePhysicalProperties（bool value））
- `Vector2 get_sensorSize()`
  （二维向量 get_sensor大小（））
- `Vector2 get_lensShift()`
  （二维向量 get_lensShift（））
- `void set_lensShift(Vector2 value)`
  （void set_lensShift（二维向量 value））
- `Rect get_rect()`
  （Rect get_rect（））
- `void set_rect(Rect value)`
  （void set_rect（Rect value））
- `Rect get_pixelRect()`
  （Rect get_pixelRect（））
- `void set_pixelRect(Rect value)`
  （void set_pixelRect（Rect value））
- `int get_pixelWidth()`
  （int get_pixel宽度（））
- `int get_pixelHeight()`
  （int get_pixel高度（））
- `int get_scaledPixelWidth()`
  （int get_scaledPixel宽度（））
- `int get_scaledPixelHeight()`
  （int get_scaledPixel高度（））
- `RenderTexture get_targetTexture()`
  （Render纹理 get_target纹理（））
- `void set_targetTexture(RenderTexture value)`
  （void set_target纹理（Render纹理 value））
- `int get_targetDisplay()`
  （int get_targetDisplay（））
- `Matrix4x4 get_worldToCameraMatrix()`
  （Matrix4x4 get_worldTo摄像机矩阵（））
- `void set_worldToCameraMatrix(Matrix4x4 value)`
  （void set_worldTo摄像机矩阵（Matrix4x4 value））
- `Matrix4x4 get_projectionMatrix()`
  （Matrix4x4 get_projection矩阵（））
- `void set_projectionMatrix(Matrix4x4 value)`
  （void set_projection矩阵（Matrix4x4 value））
- `void ResetWorldToCameraMatrix()`
  （void 重置世界的To摄像机矩阵（））
- `void ResetProjectionMatrix()`
  （void 重置Projection矩阵（））
- `Vector3 WorldToScreenPoint(Vector3 position, Camera.MonoOrStereoscopicEye eye)`
  （三维向量 世界的To屏幕的Point（三维向量 position, Camera.MonoOrStereoscopicEye eye））
- `Vector3 ScreenToWorldPoint(Vector3 position, Camera.MonoOrStereoscopicEye eye)`
  （三维向量 屏幕的To世界的Point（三维向量 position, Camera.MonoOrStereoscopicEye eye））
- `Vector3 WorldToScreenPoint(Vector3 position)`
  （三维向量 世界的To屏幕的Point（三维向量 position））
- `Vector3 ScreenToWorldPoint(Vector3 position)`
  （三维向量 屏幕的To世界的Point（三维向量 position））
- `Vector3 ScreenToViewportPoint(Vector3 position)`
  （三维向量 屏幕的ToViewportPoint（三维向量 position））
- `Ray ScreenPointToRay(Vector2 pos, Camera.MonoOrStereoscopicEye eye)`
  （Ray 屏幕的PointToRay（二维向量 pos, Camera.MonoOrStereoscopicEye eye））
- `Ray ScreenPointToRay(Vector3 pos, Camera.MonoOrStereoscopicEye eye)`
  （Ray 屏幕的PointToRay（三维向量 pos, Camera.MonoOrStereoscopicEye eye））
- `Ray ScreenPointToRay(Vector3 pos)`
  （Ray 屏幕的PointToRay（三维向量 pos））
- `Camera get_main()`
  （摄像机 get_main（））
- `Camera get_current()`
  （摄像机 get_current（））
- `bool get_stereoEnabled()`
  （bool get_stereo启用的（））
- `StereoTargetEyeMask get_stereoTargetEye()`
  （Stereo目标Eye掩码 get_stereo目标Eye（））
- `void SetStereoProjectionMatrix(Camera.StereoscopicEye eye, Matrix4x4 matrix)`
  （void 集合StereoProjection矩阵（Camera.StereoscopicEye eye, Matrix4x4 matrix））
- `void ResetStereoProjectionMatrices()`
  （void 重置StereoProjectionMatrices（））
- `void SetStereoViewMatrix(Camera.StereoscopicEye eye, Matrix4x4 matrix)`
  （void 集合Stereo视图矩阵（Camera.StereoscopicEye eye, Matrix4x4 matrix））
- `void ResetStereoViewMatrices()`
  （void 重置Stereo视图Matrices（））
- `int GetAllCamerasCount()`
  （int 获取所有Cameras数量（））
- `int GetAllCamerasImpl([Out] Camera[] cam)`
  （int 获取所有CamerasImpl（[Out] Camera[] cam））
- `int get_allCamerasCount()`
  （int get_allCameras数量（））
- `int GetAllCameras(Camera[] cameras)`
  （int 获取所有Cameras（Camera[] cameras））
- `void Render()`
  （void Render（））
- `void FireOnPreCull(Camera cam)`
  （void 开火OnPreCull（摄像机 cam））
- `void FireOnPreRender(Camera cam)`
  （void 开火OnPreRender（摄像机 cam））
- `void FireOnPostRender(Camera cam)`
  （void 开火OnPostRender（摄像机 cam））
- `bool TryGetCullingParameters(bool stereoAware, out ScriptableCullingParameters cullingParameters)`
  （bool Try获取CullingParameters（bool stereoAware, out ScriptableCullingParameters cullingParameters））
- `bool GetCullingParameters_Internal(Camera camera, bool stereoAware, out ScriptableCullingParameters cullingParameters, int managedCullingParametersSize)`
  （bool 获取CullingParameters_内部的（摄像机 camera, bool stereoAware, out ScriptableCullingParameters cullingParameters, int managedCullingParametersSize））
- `void get_backgroundColor_Injected(out Color ret)`
  （void get_backgroundColor_Injected（out Color ret））
- `void set_backgroundColor_Injected(ref Color value)`
  （void set_backgroundColor_Injected（ref Color value））
- `void get_sensorSize_Injected(out Vector2 ret)`
  （void get_sensorSize_Injected（out Vector2 ret））
- `void get_lensShift_Injected(out Vector2 ret)`
  （void get_lensShift_Injected（out Vector2 ret））
- `void set_lensShift_Injected(ref Vector2 value)`
  （void set_lensShift_Injected（ref Vector2 value））
- `void get_rect_Injected(out Rect ret)`
  （void get_rect_Injected（out Rect ret））
- `void set_rect_Injected(ref Rect value)`
  （void set_rect_Injected（ref Rect value））
- `void get_pixelRect_Injected(out Rect ret)`
  （void get_pixelRect_Injected（out Rect ret））
- `void set_pixelRect_Injected(ref Rect value)`
  （void set_pixelRect_Injected（ref Rect value））
- `void get_worldToCameraMatrix_Injected(out Matrix4x4 ret)`
  （void get_worldTo摄像机Matrix_Injected（out Matrix4x4 ret））
- `void set_worldToCameraMatrix_Injected(ref Matrix4x4 value)`
  （void set_worldTo摄像机Matrix_Injected（ref Matrix4x4 value））
- `void get_projectionMatrix_Injected(out Matrix4x4 ret)`
  （void get_projectionMatrix_Injected（out Matrix4x4 ret））
- `void set_projectionMatrix_Injected(ref Matrix4x4 value)`
  （void set_projectionMatrix_Injected（ref Matrix4x4 value））
- `void WorldToScreenPoint_Injected(ref Vector3 position, Camera.MonoOrStereoscopicEye eye, out Vector3 ret)`
  （void 世界的To屏幕的Point_Injected（ref Vector3 position, Camera.MonoOrStereoscopicEye eye, out Vector3 ret））
- `void ScreenToWorldPoint_Injected(ref Vector3 position, Camera.MonoOrStereoscopicEye eye, out Vector3 ret)`
  （void 屏幕的To世界的Point_Injected（ref Vector3 position, Camera.MonoOrStereoscopicEye eye, out Vector3 ret））
- `void ScreenToViewportPoint_Injected(ref Vector3 position, out Vector3 ret)`
  （void 屏幕的ToViewportPoint_Injected（ref Vector3 position, out Vector3 ret））
- `void ScreenPointToRay_Injected(ref Vector2 pos, Camera.MonoOrStereoscopicEye eye, out Ray ret)`
  （void 屏幕的PointToRay_Injected（ref Vector2 pos, Camera.MonoOrStereoscopicEye eye, out Ray ret））
- `void SetStereoProjectionMatrix_Injected(Camera.StereoscopicEye eye, ref Matrix4x4 matrix)`
  （void 集合StereoProjectionMatrix_Injected（Camera.StereoscopicEye eye, ref Matrix4x4 matrix））
- `void SetStereoViewMatrix_Injected(Camera.StereoscopicEye eye, ref Matrix4x4 matrix)`
  （void 集合Stereo视图Matrix_Injected（Camera.StereoscopicEye eye, ref Matrix4x4 matrix））

---

## Camera.CameraCallback（Camera.摄像机回调）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(Camera cam)`
  （void Invoke（摄像机 cam））
- `IAsyncResult BeginInvoke(Camera cam, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（摄像机 cam, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## Camera.MonoOrStereoscopicEye（Camera.MonoOrStereoscopicEye）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Camera.RenderRequest（Camera.Render请求）

### 字段 (3)

- `Camera.RenderRequestMode m_CameraRenderMode`（Camera.Render请求模式 m_摄像机Render模式）(偏移: 0x0)
- `RenderTexture m_ResultRT`（Render纹理 m_ResultRT）(偏移: 0x4)
- `Camera.RenderRequestOutputSpace m_OutputSpace`（Camera.Render请求OutputSpace m_OutputSpace）(偏移: 0x8)

---

## Camera.RenderRequestMode（Camera.Render请求模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Camera.RenderRequestOutputSpace（Camera.Render请求OutputSpace）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Camera.StereoscopicEye（Camera.StereoscopicEye）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CameraCaptureBridge（摄像机CaptureBridge）

### 字段 (1)

- `bool _enabled`（bool _enabled）(偏移: 0x4)

### 方法 (4)

- `bool get_enabled()`
  （布尔值 获取_已启用（））
- `void set_enabled(bool value)`
  （void 设置_已启用（布尔值 value））
- `void AddCaptureAction(Camera camera, Action<RenderTargetIdentifier, CommandBuffer> action)`
  （void 添加Capture动作（摄像机 camera, Action<Render目标Identifier, CommandBuffer> action））
- `void RemoveCaptureAction(Camera camera, Action<RenderTargetIdentifier, CommandBuffer> action)`
  （void 移除Capture动作（摄像机 camera, Action<Render目标Identifier, CommandBuffer> action））

---

## CameraClearFlags（摄像机清除Flags）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CameraData（摄像机数据）

### 字段 (31)

- `Matrix4x4 m_ViewMatrix`（Matrix4x4 m_视图矩阵）(偏移: 0x0)
- `Matrix4x4 m_ProjectionMatrix`（Matrix4x4 m_Projection矩阵）(偏移: 0x40)
- `Camera camera`（摄像机 camera）(偏移: 0x80)
- `CameraRenderType renderType`（摄像机Render类型 render类型）(偏移: 0x84)
- `RenderTexture targetTexture`（Render纹理 target纹理）(偏移: 0x88)
- `RenderTextureDescriptor cameraTargetDescriptor`（Render纹理Descriptor camera目标Descriptor）(偏移: 0x8C)
- `Rect pixelRect`（Rect pixelRect）(偏移: 0xC0)
- `int pixelWidth`（int pixel宽度）(偏移: 0xD0)
- `int pixelHeight`（int pixel高度）(偏移: 0xD4)
- `float aspectRatio`（float aspect比率）(偏移: 0xD8)
- `float renderScale`（float render缩放）(偏移: 0xDC)
- `bool clearDepth`（bool clear深度）(偏移: 0xE0)
- `CameraType cameraType`（摄像机类型 camera类型）(偏移: 0xE4)
- `bool isDefaultViewport`（bool is默认的Viewport）(偏移: 0xE8)
- `bool isHdrEnabled`（bool isHdr启用的）(偏移: 0x0)
- `bool requiresDepthTexture`（bool requires深度纹理）(偏移: 0x0)
- `bool requiresOpaqueTexture`（bool requires不透明的纹理）(偏移: 0x0)
- `bool xrRendering`（bool xrRendering）(偏移: 0x0)
- `SortingCriteria defaultOpaqueSortFlags`（SortingCriteria default不透明的SortFlags）(偏移: 0xF0)
- `XRPass xr`（XRPass xr）(偏移: 0xF4)
- `bool isStereoEnabled`（bool isStereo启用的）(偏移: 0xF8)
- `float maxShadowDistance`（float maxShadow距离）(偏移: 0xFC)
- `bool postProcessEnabled`（bool post处理启用的）(偏移: 0x100)
- `LayerMask volumeLayerMask`（层掩码 volume层掩码）(偏移: 0x108)
- `Transform volumeTrigger`（变换 volume触发器）(偏移: 0x10C)
- `bool isStopNaNEnabled`（bool is停止NaN启用的）(偏移: 0x110)
- `bool isDitheringEnabled`（bool isDithering启用的）(偏移: 0x111)
- `AntialiasingMode antialiasing`（Antialiasing模式 antialiasing）(偏移: 0x114)
- `AntialiasingQuality antialiasingQuality`（AntialiasingQuality antialiasingQuality）(偏移: 0x118)
- `ScriptableRenderer renderer`（Scriptable渲染器 renderer）(偏移: 0x11C)
- `bool resolveFinalTarget`（bool resolveFinal目标）(偏移: 0x120)

### 方法 (8)

- `void SetViewAndProjectionMatrix(Matrix4x4 viewMatrix, Matrix4x4 projectionMatrix)`
  （void 集合视图AndProjection矩阵（Matrix4x4 viewMatrix, Matrix4x4 projectionMatrix））
- `Matrix4x4 GetViewMatrix(int viewIndex = 0)`
  （Matrix4x4 获取视图矩阵（int viewIndex = 0））
- `Matrix4x4 GetProjectionMatrix(int viewIndex = 0)`
  （Matrix4x4 获取Projection矩阵（int viewIndex = 0））
- `Matrix4x4 GetGPUProjectionMatrix(int viewIndex = 0)`
  （Matrix4x4 获取GPUProjection矩阵（int viewIndex = 0））
- `bool get_requireSrgbConversion()`
  （bool get_requireSrgbConversion（））
- `bool get_isSceneViewCamera()`
  （bool get_is场景视图摄像机（））
- `bool get_isPreviewCamera()`
  （bool get_isPreview摄像机（））
- `bool IsCameraProjectionMatrixFlipped()`
  （bool 是否摄像机Projection矩阵Flipped（））

---

## CameraExtensions（摄像机Extensions）

### 方法 (8)

- `UniversalAdditionalCameraData GetUniversalAdditionalCameraData(Camera camera)`
  （UniversalAdditional摄像机数据 获取UniversalAdditional摄像机数据（摄像机 camera））
- `VolumeFrameworkUpdateMode GetVolumeFrameworkUpdateMode(Camera camera)`
  （VolumeFramework更新模式 获取VolumeFramework更新模式（摄像机 camera））
- `void SetVolumeFrameworkUpdateMode(Camera camera, VolumeFrameworkUpdateMode mode)`
  （void 集合VolumeFramework更新模式（摄像机 camera, VolumeFramework更新模式 mode））
- `void UpdateVolumeStack(Camera camera)`
  （void 更新Volume栈（摄像机 camera））
- `void UpdateVolumeStack(Camera camera, UniversalAdditionalCameraData cameraData)`
  （void 更新Volume栈（摄像机 camera, UniversalAdditional摄像机数据 cameraData））
- `void DestroyVolumeStack(Camera camera)`
  （void 销毁Volume栈（摄像机 camera））
- `void DestroyVolumeStack(Camera camera, UniversalAdditionalCameraData cameraData)`
  （void 销毁Volume栈（摄像机 camera, UniversalAdditional摄像机数据 cameraData））
- `void GetVolumeLayerMaskAndTrigger(Camera camera, UniversalAdditionalCameraData cameraData, out LayerMask layerMask, out Transform trigger)`
  （void 获取Volume层掩码And触发器（摄像机 camera, UniversalAdditional摄像机数据 cameraData, out LayerMask layerMask, out Transform trigger））

---

## CameraLateLatchMatrixType（摄像机延迟Latch矩阵类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CameraManager（摄像机管理器）

**继承**: Singleton<CameraManager>（Singleton<摄像机Manager>）

### 字段 (10)

- `CinemachineFreeLook freeLookCamera`（CinemachineFreeLook freeLook摄像机）(偏移: 0x10)
- `CinemachineBrain brain`（Cinemachine爆头 brain）(偏移: 0x14)
- `ObscuredBool playerView`（模糊的布尔值 player视图）(偏移: 0x0)
- `List<Camera> cameraStack`（List<Camera> camera栈）(偏移: 0x18)
- `float changeViewUnlockTime`（float change视图Unlock时间）(偏移: 0x1C)
- `VolumeProfile volumeProfile`（VolumeProfile volumeProfile）(偏移: 0x10)
- `GhostBladeOneShine oneShine`（幽灵刀锋OneShine oneShine）(偏移: 0x14)
- `ThermalVision thermalVision`（ThermalVision thermalVision）(偏移: 0x18)
- `ForwardRendererData fwdRenderData`（前进渲染器数据 fwdRender数据）(偏移: 0x20)
- `ScriptableRendererFeature humanCatchFeature`（Scriptable渲染器Feature humanCatchFeature）(偏移: 0x24)

### 方法 (19)

- `Player get_focusPlayer()`
  （玩家 get_focus玩家（））
- `void set_focusPlayer(Player value)`
  （void set_focus玩家（玩家 value））
- `void add_FocusPlayerChangeEvent_Observers(Action<Player, Player> value)`
  （void add_聚焦玩家ChangeEvent_Observers（Action<玩家, Player> value））
- `void remove_FocusPlayerChangeEvent_Observers(Action<Player, Player> value)`
  （void remove_聚焦玩家ChangeEvent_Observers（Action<玩家, Player> value））
- `bool get_changeViewUnlock()`
  （bool get_change视图Unlock（））
- `void Awake()`
  （void 唤醒（））
- `void Update()`
  （void 更新（））
- `void OnDestroy()`
  （void 销毁时（））
- `void ChangePVandCV()`
  （void ChangePVand第一人称视角（））
- `void SetFocusPlayer(Player player)`
  （void 集合聚焦玩家（玩家 player））
- `void SpawnEvent(Player player)`
  （void 出生事件（玩家 player））
- `void DeathEvent(DeathEventData data)`
  （void 死亡事件（死亡事件数据 data））
- `void SetFreeLookCameraActive(bool active)`
  （void 集合FreeLook摄像机激活的（bool active））
- `void SetFreeLookCameraLookDir(Vector3 direction)`
  （void 集合FreeLook摄像机LookDir（三维向量 direction））
- `void TryChangeTeammateView(bool next)`
  （void TryChangeTeammate视图（bool next））
- `void PlayGhostBladeOneShineEffect()`
  （void 播放幽灵刀锋OneShine特效（））
- `void SetThermalVision(float duration, bool showHuman)`
  （void 集合ThermalVision（float duration, bool showHuman））
- `bool IsInThisPlayerPV(Entity entity)`
  （bool 是否InThis玩家第三人称视角（实体 entity））
- `void ManualUpdate()`
  （void 手动更新（））

---

## CameraOverrideOption（摄像机重写Option）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CameraPlayable（摄像机Playable）

**继承**: IPlayable, IEquatable<CameraPlayable>（IPlayable, IEquatable<摄像机Playable>）

### 字段 (1)

- `PlayableHandle m_Handle`（可播放句柄 m_句柄）(偏移: 0x0)

### 方法 (2)

- `PlayableHandle GetHandle()`
  （可播放句柄 获取句柄（））
- `bool Equals(CameraPlayable other)`
  （bool Equals（摄像机Playable other））

---

## CameraProperties（摄像机Properties）

**继承**: IEquatable<CameraProperties>（IEquatable<摄像机Properties>）

### 字段 (32)

- `Rect screenRect`（Rect screenRect）(偏移: 0x0)
- `Vector3 viewDir`（三维向量 viewDir）(偏移: 0x10)
- `float projectionNear`（float projectionNear）(偏移: 0x1C)
- `float projectionFar`（float projectionFar）(偏移: 0x20)
- `float cameraNear`（float cameraNear）(偏移: 0x24)
- `float cameraFar`（float cameraFar）(偏移: 0x28)
- `float cameraAspect`（float cameraAspect）(偏移: 0x2C)
- `Matrix4x4 cameraToWorld`（Matrix4x4 cameraTo世界的）(偏移: 0x30)
- `Matrix4x4 actualWorldToClip`（Matrix4x4 actual世界的To弹匣）(偏移: 0x70)
- `Matrix4x4 cameraClipToWorld`（Matrix4x4 camera弹匣To世界的）(偏移: 0xB0)
- `Matrix4x4 cameraWorldToClip`（Matrix4x4 camera世界的To弹匣）(偏移: 0xF0)
- `Matrix4x4 implicitProjection`（Matrix4x4 implicitProjection）(偏移: 0x130)
- `Matrix4x4 stereoWorldToClipLeft`（Matrix4x4 stereo世界的To弹匣左）(偏移: 0x170)
- `Matrix4x4 stereoWorldToClipRight`（Matrix4x4 stereo世界的To弹匣右）(偏移: 0x1B0)
- `Matrix4x4 worldToCamera`（Matrix4x4 worldTo摄像机）(偏移: 0x1F0)
- `Vector3 up`（三维向量 up）(偏移: 0x230)
- `Vector3 right`（三维向量 right）(偏移: 0x23C)
- `Vector3 transformDirection`（三维向量 transform方向）(偏移: 0x248)
- `Vector3 cameraEuler`（三维向量 cameraEuler）(偏移: 0x254)
- `Vector3 velocity`（三维向量 速度）(偏移: 0x260)
- `float farPlaneWorldSpaceLength`（float farPlane世界的SpaceLength）(偏移: 0x26C)
- `uint rendererCount`（uint renderer数量）(偏移: 0x270)
- `CameraProperties.<m_ShadowCullPlanes>e__FixedBuffer m_ShadowCullPlanes`（摄像机Properties.<m_ShadowCullPlanes>e__固定缓冲区 m_ShadowCullPlanes）(偏移: 0x274)
- `CameraProperties.<m_CameraCullPlanes>e__FixedBuffer m_CameraCullPlanes`（摄像机Properties.<m_摄像机CullPlanes>e__固定缓冲区 m_摄像机CullPlanes）(偏移: 0x2D4)
- `float baseFarDistance`（float baseFar距离）(偏移: 0x334)
- `Vector3 shadowCullCenter`（三维向量 shadowCull中心）(偏移: 0x338)
- `CameraProperties.<layerCullDistances>e__FixedBuffer layerCullDistances`（摄像机Properties.<layerCullDistances>e__固定缓冲区 layerCullDistances）(偏移: 0x344)
- `int layerCullSpherical`（int layerCullSpherical）(偏移: 0x3C4)
- `CoreCameraValues coreCameraValues`（Core摄像机Values core摄像机Values）(偏移: 0x3C8)
- `uint cameraType`（uint camera类型）(偏移: 0x3D4)
- `int projectionIsOblique`（int projection是否Oblique）(偏移: 0x3D8)
- `int isImplicitProjectionMatrix`（int isImplicitProjection矩阵）(偏移: 0x3DC)

### 方法 (5)

- `Plane GetShadowCullingPlane(int index)`
  （Plane 获取ShadowCullingPlane（int index））
- `Plane GetCameraCullingPlane(int index)`
  （Plane 获取摄像机CullingPlane（int index））
- `bool Equals(CameraProperties other)`
  （bool Equals（摄像机Properties other））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## CameraRaycastHelper（摄像机Raycast辅助器）

### 方法 (4)

- `GameObject RaycastTry(Camera cam, Ray ray, float distance, int layerMask)`
  （游戏对象 RaycastTry（摄像机 cam, Ray ray, float distance, int layerMask））
- `GameObject RaycastTry2D(Camera cam, Ray ray, float distance, int layerMask)`
  （游戏对象 RaycastTry2D（摄像机 cam, Ray ray, float distance, int layerMask））
- `GameObject RaycastTry_Injected(Camera cam, ref Ray ray, float distance, int layerMask)`
  （游戏对象 RaycastTry_Injected（摄像机 cam, ref Ray ray, float distance, int layerMask））
- `GameObject RaycastTry2D_Injected(Camera cam, ref Ray ray, float distance, int layerMask)`
  （游戏对象 RaycastTry2D_Injected（摄像机 cam, ref Ray ray, float distance, int layerMask））

---

## CameraRenderType（摄像机Render类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CameraState（摄像机状态）

### 字段 (6)

- `Vector3 kNoPoint`（三维向量 kNoPoint）(偏移: 0x0)
- `CameraState.CustomBlendable mCustom0`（摄像机State.自定义的Blendable mCustom0）(偏移: 0x90)
- `CameraState.CustomBlendable mCustom1`（摄像机State.自定义的Blendable mCustom1）(偏移: 0x98)
- `CameraState.CustomBlendable mCustom2`（摄像机State.自定义的Blendable mCustom2）(偏移: 0xA0)
- `CameraState.CustomBlendable mCustom3`（摄像机State.自定义的Blendable mCustom3）(偏移: 0xA8)
- `List<CameraState.CustomBlendable> m_CustomOverflow`（List<摄像机State.自定义的Blendable> m_自定义的Overflow）(偏移: 0xB0)

### 方法 (36)

- `LensSettings get_Lens()`
  （LensSettings get_Lens（））
- `void set_Lens(LensSettings value)`
  （void set_Lens（LensSettings value））
- `Vector3 get_ReferenceUp()`
  （三维向量 get_引用上（））
- `void set_ReferenceUp(Vector3 value)`
  （void set_引用上（三维向量 value））
- `Vector3 get_ReferenceLookAt()`
  （三维向量 get_引用LookAt（））
- `void set_ReferenceLookAt(Vector3 value)`
  （void set_引用LookAt（三维向量 value））
- `bool get_HasLookAt()`
  （bool get_是否有LookAt（））
- `Vector3 get_RawPosition()`
  （三维向量 get_RawPosition（））
- `void set_RawPosition(Vector3 value)`
  （void set_RawPosition（三维向量 value））
- `Quaternion get_RawOrientation()`
  （Quaternion get_RawOrientation（））
- `void set_RawOrientation(Quaternion value)`
  （void set_RawOrientation（Quaternion value））
- `Vector3 get_PositionDampingBypass()`
  （三维向量 get_PositionDampingBypass（））
- `void set_PositionDampingBypass(Vector3 value)`
  （void set_PositionDampingBypass（三维向量 value））
- `float get_ShotQuality()`
  （float get_射击Quality（））
- `void set_ShotQuality(float value)`
  （void set_射击Quality（float value））
- `Vector3 get_PositionCorrection()`
  （三维向量 get_PositionCorrection（））
- `void set_PositionCorrection(Vector3 value)`
  （void set_PositionCorrection（三维向量 value））
- `Quaternion get_OrientationCorrection()`
  （Quaternion get_OrientationCorrection（））
- `void set_OrientationCorrection(Quaternion value)`
  （void set_OrientationCorrection（Quaternion value））
- `Vector3 get_CorrectedPosition()`
  （三维向量 get_CorrectedPosition（））
- `Quaternion get_CorrectedOrientation()`
  （Quaternion get_CorrectedOrientation（））
- `Vector3 get_FinalPosition()`
  （三维向量 get_FinalPosition（））
- `Quaternion get_FinalOrientation()`
  （Quaternion get_FinalOrientation（））
- `CameraState.BlendHintValue get_BlendHint()`
  （摄像机State.BlendHint值 get_BlendHint（））
- `void set_BlendHint(CameraState.BlendHintValue value)`
  （void set_BlendHint（摄像机State.BlendHint值 value））
- `CameraState get_Default()`
  （摄像机状态 get_默认的（））
- `int get_NumCustomBlendables()`
  （int get_Num自定义的Blendables（））
- `void set_NumCustomBlendables(int value)`
  （void set_Num自定义的Blendables（int value））
- `CameraState.CustomBlendable GetCustomBlendable(int index)`
  （摄像机State.自定义的Blendable 获取自定义的Blendable（int index））
- `int FindCustomBlendable(Object custom)`
  （int 查找自定义的Blendable（对象 custom））
- `void AddCustomBlendable(CameraState.CustomBlendable b)`
  （void 添加自定义的Blendable（摄像机State.自定义的Blendable b））
- `CameraState Lerp(CameraState stateA, CameraState stateB, float t)`
  （摄像机状态 Lerp（摄像机状态 stateA, 摄像机状态 stateB, float t））
- `float InterpolateFOV(float fovA, float fovB, float dA, float dB, float t)`
  （float Interpolate视野（float fovA, float fovB, float dA, float dB, float t））
- `Vector3 ApplyPosBlendHint(Vector3 posA, CameraState.BlendHintValue hintA, Vector3 posB, CameraState.BlendHintValue hintB, Vector3 original, Vector3 blended)`
  （三维向量 应用PosBlendHint（三维向量 posA, 摄像机State.BlendHint值 hintA, 三维向量 posB, 摄像机State.BlendHint值 hintB, 三维向量 original, 三维向量 blended））
- `Quaternion ApplyRotBlendHint(Quaternion rotA, CameraState.BlendHintValue hintA, Quaternion rotB, CameraState.BlendHintValue hintB, Quaternion original, Quaternion blended)`
  （Quaternion 应用RotBlendHint（Quaternion rotA, 摄像机State.BlendHint值 hintA, Quaternion rotB, 摄像机State.BlendHint值 hintB, Quaternion original, Quaternion blended））
- `Vector3 InterpolatePosition(Vector3 posA, Vector3 pivotA, Vector3 posB, Vector3 pivotB, float t)`
  （三维向量 InterpolatePosition（三维向量 posA, 三维向量 pivotA, 三维向量 posB, 三维向量 pivotB, float t））

---

## CameraState.BlendHintValue（摄像机State.BlendHint值）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CameraState.CustomBlendable（摄像机State.自定义的Blendable）

### 字段 (2)

- `Object m_Custom`（对象 m_自定义的）(偏移: 0x0)
- `float m_Weight`（float m_Weight）(偏移: 0x4)

---

## CameraSwitcher（摄像机Switcher）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (10)

- `Camera[] m_Cameras`（Camera[] m_Cameras）(偏移: 0xC)
- `int m_CurrentCameraIndex`（int m_当前摄像机索引）(偏移: 0x10)
- `Camera m_OriginalCamera`（摄像机 m_Original摄像机）(偏移: 0x14)
- `Vector3 m_OriginalCameraPosition`（三维向量 m_Original摄像机Position）(偏移: 0x18)
- `Quaternion m_OriginalCameraRotation`（Quaternion m_Original摄像机Rotation）(偏移: 0x24)
- `Camera m_CurrentCamera`（摄像机 m_当前摄像机）(偏移: 0x34)
- `GUIContent[] m_CameraNames`（GUIContent[] m_摄像机Names）(偏移: 0x38)
- `int[] m_CameraIndices`（int[] m_摄像机Indices）(偏移: 0x3C)
- `DebugUI.EnumField m_DebugEntry`（DebugUI.EnumField m_DebugEntry）(偏移: 0x40)
- `int m_DebugEntryEnumIndex`（int m_DebugEntryEnum索引）(偏移: 0x44)

### 方法 (5)

- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `int GetCameraCount()`
  （int 获取摄像机数量（））
- `Camera GetNextCamera()`
  （摄像机 获取下一个摄像机（））
- `void SetCameraIndex(int index)`
  （void 集合摄像机索引（int index））

---

## CameraType（摄像机类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CameraTypeUtility（摄像机类型工具）

### 字段 (1)

- `string[] s_CameraTypeNames`（string[] s_摄像机类型Names）(偏移: 0x33FF33DD)

### 方法 (1)

- `string GetName(CameraRenderType type)`
  （string 获取名称（摄像机Render类型 type））

---

## CancellationCallbackCoreWorkArguments（Cancellation回调CoreWorkArguments）

### 字段 (2)

- `SparselyPopulatedArrayFragment<CancellationCallbackInfo> m_currArrayFragment`（SparselyPopulated数组Fragment<Cancellation回调Info> m_curr数组Fragment）(偏移: 0x0)
- `int m_currArrayIndex`（int m_curr数组索引）(偏移: 0x4)

---

## CancellationCallbackInfo（Cancellation回调信息）

### 字段 (6)

- `Action<object> Callback`（Action<object> 回调）(偏移: 0x8)
- `object StateForCallback`（object 状态For回调）(偏移: 0xC)
- `SynchronizationContext TargetSyncContext`（SynchronizationContext 目标同步Context）(偏移: 0x10)
- `ExecutionContext TargetExecutionContext`（ExecutionContext 目标ExecutionContext）(偏移: 0x14)
- `CancellationTokenSource CancellationTokenSource`（Cancellation令牌Source Cancellation令牌Source）(偏移: 0x18)
- `ContextCallback s_executionContextCallback`（Context回调 s_executionContext回调）(偏移: 0x0)

### 方法 (2)

- `void ExecuteCallback()`
  （void 执行回调（））
- `void ExecutionContextCallback(object obj)`
  （void ExecutionContext回调（object obj））

---

## CancellationToken（Cancellation令牌）

### 字段 (2)

- `CancellationTokenSource m_source`（Cancellation令牌Source m_source）(偏移: 0x0)
- `Action<object> s_ActionToActionObjShunt`（Action<object> s_动作To动作ObjShunt）(偏移: 0x0)

### 方法 (15)

- `CancellationToken get_None()`
  （Cancellation令牌 get_无（））
- `bool get_IsCancellationRequested()`
  （bool get_是否CancellationRequested（））
- `bool get_CanBeCanceled()`
  （bool get_能否BeCanceled（））
- `void ActionToActionObjShunt(object obj)`
  （void 动作To动作ObjShunt（object obj））
- `CancellationTokenRegistration InternalRegisterWithoutEC(Action<object> callback, object state)`
  （Cancellation令牌Registration 内部的RegisterWithoutEC（Action<object> callback, object state））
- `CancellationTokenRegistration Register(Action<object> callback, object state, bool useSynchronizationContext, bool useExecutionContext)`
  （Cancellation令牌Registration Register（Action<object> callback, object state, bool useSynchronizationContext, bool useExecutionContext））
- `bool Equals(CancellationToken other)`
  （bool Equals（Cancellation令牌 other））
- `bool Equals(object other)`
  （布尔值 等于（对象 other））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `bool op_Equality(CancellationToken left, CancellationToken right)`
  （bool op_Equality（Cancellation令牌 left, Cancellation令牌 right））
- `bool op_Inequality(CancellationToken left, CancellationToken right)`
  （bool op_Inequality（Cancellation令牌 left, Cancellation令牌 right））
- `void ThrowIfCancellationRequested()`
  （void 投掷IfCancellationRequested（））
- `void ThrowIfSourceDisposed()`
  （void 投掷IfSourceDisposed（））
- `void ThrowOperationCanceledException()`
  （void 投掷OperationCanceledException（））
- `void ThrowObjectDisposedException()`
  （void 投掷对象DisposedException（））

---

## CancellationTokenRegistration（Cancellation令牌Registration）

**继承**: IEquatable<CancellationTokenRegistration>, IDisposable（IEquatable<Cancellation令牌Registration>, IDisposable）

### 字段 (2)

- `CancellationCallbackInfo m_callbackInfo`（Cancellation回调信息 m_callback信息）(偏移: 0x0)
- `SparselyPopulatedArrayAddInfo<CancellationCallbackInfo> m_registrationInfo`（SparselyPopulated数组添加Info<Cancellation回调Info> m_registration信息）(偏移: 0x4)

### 方法 (5)

- `bool TryDeregister()`
  （bool TryDeregister（））
- `void Dispose()`
  （void 释放（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(CancellationTokenRegistration other)`
  （bool Equals（Cancellation令牌Registration other））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## CancellationTokenSource（Cancellation令牌Source）

**继承**: IDisposable（可释放接口）

### 字段 (13)

- `CancellationTokenSource _staticSource_Set`（Cancellation令牌Source _staticSource_集合）(偏移: 0x0)
- `CancellationTokenSource _staticSource_NotCancelable`（Cancellation令牌Source _staticSource_NotCancelable）(偏移: 0x4)
- `int s_nLists`（int s_nLists）(偏移: 0x8)
- `ManualResetEvent m_kernelEvent`（手动重置事件 m_kernel事件）(偏移: 0x8)
- `SparselyPopulatedArray<CancellationCallbackInfo>[] m_registeredCallbacksLists`（SparselyPopulatedArray<Cancellation回调Info>[] m_registeredCallbacksLists）(偏移: 0xC)
- `int m_state`（int m_state）(偏移: 0x10)
- `int m_threadIDExecutingCallbacks`（int m_threadIDExecutingCallbacks）(偏移: 0x14)
- `bool m_disposed`（布尔值 m_已释放）(偏移: 0x18)
- `CancellationTokenRegistration[] m_linkingRegistrations`（Cancellation令牌Registration[] m_linkingRegistrations）(偏移: 0x1C)
- `Action<object> s_LinkedTokenCancelDelegate`（Action<object> s_Linked令牌取消委托）(偏移: 0xC)
- `CancellationCallbackInfo m_executingCallback`（Cancellation回调信息 m_executing回调）(偏移: 0x20)
- `Timer m_timer`（计时器 m_timer）(偏移: 0x24)
- `TimerCallback s_timerCallback`（计时器回调 s_timer回调）(偏移: 0x10)

### 方法 (24)

- `void LinkedTokenCancelDelegate(object source)`
  （void Linked令牌取消委托（object source））
- `bool get_IsCancellationRequested()`
  （bool get_是否CancellationRequested（））
- `bool get_IsCancellationCompleted()`
  （bool get_是否CancellationCompleted（））
- `bool get_IsDisposed()`
  （bool get_是否Disposed（））
- `void set_ThreadIDExecutingCallbacks(int value)`
  （void set_ThreadIDExecutingCallbacks（int value））
- `int get_ThreadIDExecutingCallbacks()`
  （int get_ThreadIDExecutingCallbacks（））
- `CancellationToken get_Token()`
  （Cancellation令牌 get_令牌（））
- `bool get_CanBeCanceled()`
  （bool get_能否BeCanceled（））
- `CancellationCallbackInfo get_ExecutingCallback()`
  （Cancellation回调信息 get_Executing回调（））
- `void Cancel()`
  （void 取消（））
- `void Cancel(bool throwOnFirstException)`
  （void 取消（bool throwOnFirstException））
- `void TimerCallbackLogic(object obj)`
  （void 计时器回调Logic（object obj））
- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `void ThrowIfDisposed()`
  （void 投掷IfDisposed（））
- `void ThrowObjectDisposedException()`
  （void 投掷对象DisposedException（））
- `CancellationTokenSource InternalGetStaticSource(bool set)`
  （Cancellation令牌Source 内部的获取静态的Source（bool set））
- `CancellationTokenRegistration InternalRegister(Action<object> callback, object stateForCallback, SynchronizationContext targetSyncContext, ExecutionContext executionContext)`
  （Cancellation令牌Registration 内部的Register（Action<object> callback, object stateForCallback, SynchronizationContext targetSyncContext, ExecutionContext executionContext））
- `void NotifyCancellation(bool throwOnFirstException)`
  （void NotifyCancellation（bool throwOnFirstException））
- `void ExecuteCallbackHandlers(bool throwOnFirstException)`
  （void 执行回调Handlers（bool throwOnFirstException））
- `void CancellationCallbackCoreWork_OnSyncContext(object obj)`
  （void Cancellation回调CoreWork_On同步Context（object obj））
- `void CancellationCallbackCoreWork(CancellationCallbackCoreWorkArguments args)`
  （void Cancellation回调CoreWork（Cancellation回调CoreWorkArguments args））
- `CancellationTokenSource CreateLinkedTokenSource(CancellationToken token1, CancellationToken token2)`
  （Cancellation令牌Source 创建Linked令牌Source（Cancellation令牌 token1, Cancellation令牌 token2））
- `void WaitForCallbackToComplete(CancellationCallbackInfo callbackInfo)`
  （void WaitFor回调ToComplete（Cancellation回调信息 callbackInfo））

---

## Canvas（画布）

**继承**: Behaviour（行为）

### 字段 (2)

- `Canvas.WillRenderCanvases preWillRenderCanvases`（Canvas.WillRenderCanvases preWillRenderCanvases）(偏移: 0x0)
- `Canvas.WillRenderCanvases willRenderCanvases`（Canvas.WillRenderCanvases willRenderCanvases）(偏移: 0x4)

### 方法 (29)

- `void add_preWillRenderCanvases(Canvas.WillRenderCanvases value)`
  （void add_preWillRenderCanvases（Canvas.WillRenderCanvases value））
- `void remove_preWillRenderCanvases(Canvas.WillRenderCanvases value)`
  （void remove_preWillRenderCanvases（Canvas.WillRenderCanvases value））
- `void add_willRenderCanvases(Canvas.WillRenderCanvases value)`
  （void add_willRenderCanvases（Canvas.WillRenderCanvases value））
- `void remove_willRenderCanvases(Canvas.WillRenderCanvases value)`
  （void remove_willRenderCanvases（Canvas.WillRenderCanvases value））
- `RenderMode get_renderMode()`
  （Render模式 get_render模式（））
- `void set_renderMode(RenderMode value)`
  （void set_render模式（Render模式 value））
- `bool get_isRootCanvas()`
  （bool get_is根画布（））
- `float get_scaleFactor()`
  （float get_scale系数（））
- `void set_scaleFactor(float value)`
  （void set_scale系数（float value））
- `float get_referencePixelsPerUnit()`
  （float get_referencePixelsPerUnit（））
- `void set_referencePixelsPerUnit(float value)`
  （void set_referencePixelsPerUnit（float value））
- `bool get_pixelPerfect()`
  （bool get_pixelPerfect（））
- `int get_renderOrder()`
  （int get_renderOrder（））
- `bool get_overrideSorting()`
  （bool get_overrideSorting（））
- `void set_overrideSorting(bool value)`
  （void set_overrideSorting（bool value））
- `int get_sortingOrder()`
  （int get_sortingOrder（））
- `void set_sortingOrder(int value)`
  （void set_sortingOrder（int value））
- `int get_targetDisplay()`
  （int get_targetDisplay（））
- `int get_sortingLayerID()`
  （int get_sorting层ID（））
- `void set_sortingLayerID(int value)`
  （void set_sorting层ID（int value））
- `Canvas get_rootCanvas()`
  （画布 get_root画布（））
- `Vector2 get_renderingDisplaySize()`
  （二维向量 get_renderingDisplay大小（））
- `Camera get_worldCamera()`
  （摄像机 get_world摄像机（））
- `Material GetDefaultCanvasMaterial()`
  （材质 获取默认的画布材质（））
- `Material GetETC1SupportedCanvasMaterial()`
  （材质 获取ETC1Supported画布材质（））
- `void ForceUpdateCanvases()`
  （void 强制更新Canvases（））
- `void SendPreWillRenderCanvases()`
  （void 发送PreWillRenderCanvases（））
- `void SendWillRenderCanvases()`
  （void 发送WillRenderCanvases（））
- `void get_renderingDisplaySize_Injected(out Vector2 ret)`
  （void get_renderingDisplaySize_Injected（out Vector2 ret））

---

## Canvas.WillRenderCanvases（Canvas.WillRenderCanvases）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke()`
  （void 调用（））
- `IAsyncResult BeginInvoke(AsyncCallback callback, object object)`
  （I异步结果 开始调用（异步回调 callback, 对象 object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## CanvasGroup（画布组）

**继承**: Behaviour, ICanvasRaycastFilter（Behaviour, I画布RaycastFilter）

### 方法 (6)

- `float get_alpha()`
  （float get_alpha（））
- `void set_alpha(float value)`
  （void set_alpha（float value））
- `bool get_interactable()`
  （bool get_interactable（））
- `bool get_blocksRaycasts()`
  （bool get_blocksRaycasts（））
- `bool get_ignoreParentGroups()`
  （bool get_ignore父级Groups（））
- `bool IsRaycastLocationValid(Vector2 sp, Camera eventCamera)`
  （布尔值 射线检测位置是否有效（二维向量 sp, 摄像机 eventCamera））

---

## CanvasRenderer（画布渲染器）

**继承**: Component（组件）

### 方法 (30)

- `void set_hasPopInstruction(bool value)`
  （void set_hasPopInstruction（bool value））
- `int get_materialCount()`
  （int get_material数量（））
- `void set_materialCount(int value)`
  （void set_material数量（int value））
- `void set_popMaterialCount(int value)`
  （void set_pop材质数量（int value））
- `int get_absoluteDepth()`
  （int get_absolute深度（））
- `bool get_hasMoved()`
  （bool get_hasMoved（））
- `bool get_cull()`
  （bool get_cull（））
- `void set_cull(bool value)`
  （void set_cull（bool value））
- `void SetColor(Color color)`
  （void 集合颜色（颜色 color））
- `Color GetColor()`
  （颜色 获取颜色（））
- `void EnableRectClipping(Rect rect)`
  （void 启用RectClipping（Rect rect））
- `void set_clippingSoftness(Vector2 value)`
  （void set_clippingSoftness（二维向量 value））
- `void DisableRectClipping()`
  （void 禁用RectClipping（））
- `void SetMaterial(Material material, int index)`
  （void 集合材质（材质 material, int index））
- `void SetPopMaterial(Material material, int index)`
  （void 集合Pop材质（材质 material, int index））
- `void SetTexture(Texture texture)`
  （void 集合纹理（纹理 texture））
- `void SetAlphaTexture(Texture texture)`
  （void 集合透明度纹理（纹理 texture））
- `void SetMesh(Mesh mesh)`
  （void 集合网格（网格 mesh））
- `void Clear()`
  （void 清除（））
- `void SetMaterial(Material material, Texture texture)`
  （void 集合材质（材质 material, 纹理 texture））
- `void SplitUIVertexStreams(List<UIVertex> verts, List<Vector3> positions, List<Color32> colors, List<Vector4> uv0S, List<Vector4> uv1S, List<Vector4> uv2S, List<Vector4> uv3S, List<Vector3> normals, List<Vector4> tangents, List<int> indices)`
  （void Split界面VertexStreams（List<UIVertex> verts, List<Vector3> positions, List<Color32> colors, List<Vector4> uv0S, List<Vector4> uv1S, List<Vector4> uv2S, List<Vector4> uv3S, List<Vector3> normals, List<Vector4> tangents, List<int> indices））
- `void CreateUIVertexStream(List<UIVertex> verts, List<Vector3> positions, List<Color32> colors, List<Vector4> uv0S, List<Vector4> uv1S, List<Vector4> uv2S, List<Vector4> uv3S, List<Vector3> normals, List<Vector4> tangents, List<int> indices)`
  （void 创建界面Vertex流（List<UIVertex> verts, List<Vector3> positions, List<Color32> colors, List<Vector4> uv0S, List<Vector4> uv1S, List<Vector4> uv2S, List<Vector4> uv3S, List<Vector3> normals, List<Vector4> tangents, List<int> indices））
- `void AddUIVertexStream(List<UIVertex> verts, List<Vector3> positions, List<Color32> colors, List<Vector4> uv0S, List<Vector4> uv1S, List<Vector4> uv2S, List<Vector4> uv3S, List<Vector3> normals, List<Vector4> tangents)`
  （void 添加界面Vertex流（List<UIVertex> verts, List<Vector3> positions, List<Color32> colors, List<Vector4> uv0S, List<Vector4> uv1S, List<Vector4> uv2S, List<Vector4> uv3S, List<Vector3> normals, List<Vector4> tangents））
- `void SplitIndicesStreamsInternal(object verts, object indices)`
  （void SplitIndicesStreams内部的（object verts, object indices））
- `void SplitUIVertexStreamsInternal(object verts, object positions, object colors, object uv0S, object uv1S, object uv2S, object uv3S, object normals, object tangents)`
  （void Split界面VertexStreams内部的（object verts, object positions, object colors, object uv0S, object uv1S, object uv2S, object uv3S, object normals, object tangents））
- `void CreateUIVertexStreamInternal(object verts, object positions, object colors, object uv0S, object uv1S, object uv2S, object uv3S, object normals, object tangents, object indices)`
  （void 创建界面Vertex流内部的（object verts, object positions, object colors, object uv0S, object uv1S, object uv2S, object uv3S, object normals, object tangents, object indices））
- `void SetColor_Injected(ref Color color)`
  （void 集合Color_Injected（ref Color color））
- `void GetColor_Injected(out Color ret)`
  （void 获取Color_Injected（out Color ret））
- `void EnableRectClipping_Injected(ref Rect rect)`
  （void 启用RectClipping_Injected（ref Rect rect））
- `void set_clippingSoftness_Injected(ref Vector2 value)`
  （void set_clippingSoftness_Injected（ref Vector2 value））

---

## CanvasScaler（画布Scaler）

**继承**: UIBehaviour（UI行为）

### 字段 (14)

- `CanvasScaler.ScaleMode m_UiScaleMode`（画布Scaler.缩放模式 m_Ui缩放模式）(偏移: 0xC)
- `float m_ReferencePixelsPerUnit`（float m_引用PixelsPerUnit）(偏移: 0x10)
- `float m_ScaleFactor`（float m_缩放系数）(偏移: 0x14)
- `Vector2 m_ReferenceResolution`（二维向量 m_引用Resolution）(偏移: 0x18)
- `CanvasScaler.ScreenMatchMode m_ScreenMatchMode`（画布Scaler.屏幕的比赛模式 m_屏幕的比赛模式）(偏移: 0x20)
- `float m_MatchWidthOrHeight`（float m_比赛宽度Or高度）(偏移: 0x24)
- `CanvasScaler.Unit m_PhysicalUnit`（画布Scaler.Unit m_PhysicalUnit）(偏移: 0x28)
- `float m_FallbackScreenDPI`（float m_Fallback屏幕的DPI）(偏移: 0x2C)
- `float m_DefaultSpriteDPI`（float m_默认的精灵DPI）(偏移: 0x30)
- `float m_DynamicPixelsPerUnit`（float m_动态的PixelsPerUnit）(偏移: 0x34)
- `Canvas m_Canvas`（画布 m_画布）(偏移: 0x38)
- `float m_PrevScaleFactor`（float m_Prev缩放系数）(偏移: 0x3C)
- `float m_PrevReferencePixelsPerUnit`（float m_Prev引用PixelsPerUnit）(偏移: 0x40)
- `bool m_PresetInfoIsWorld`（bool m_Preset信息是否世界的）(偏移: 0x44)

### 方法 (30)

- `CanvasScaler.ScaleMode get_uiScaleMode()`
  （画布Scaler.缩放模式 get_ui缩放模式（））
- `void set_uiScaleMode(CanvasScaler.ScaleMode value)`
  （void set_ui缩放模式（画布Scaler.缩放模式 value））
- `float get_referencePixelsPerUnit()`
  （float get_referencePixelsPerUnit（））
- `void set_referencePixelsPerUnit(float value)`
  （void set_referencePixelsPerUnit（float value））
- `float get_scaleFactor()`
  （float get_scale系数（））
- `void set_scaleFactor(float value)`
  （void set_scale系数（float value））
- `Vector2 get_referenceResolution()`
  （二维向量 get_referenceResolution（））
- `void set_referenceResolution(Vector2 value)`
  （void set_referenceResolution（二维向量 value））
- `CanvasScaler.ScreenMatchMode get_screenMatchMode()`
  （画布Scaler.屏幕的比赛模式 get_screen比赛模式（））
- `void set_screenMatchMode(CanvasScaler.ScreenMatchMode value)`
  （void set_screen比赛模式（画布Scaler.屏幕的比赛模式 value））
- `float get_matchWidthOrHeight()`
  （float get_match宽度Or高度（））
- `void set_matchWidthOrHeight(float value)`
  （void set_match宽度Or高度（float value））
- `CanvasScaler.Unit get_physicalUnit()`
  （画布Scaler.Unit get_physicalUnit（））
- `void set_physicalUnit(CanvasScaler.Unit value)`
  （void set_physicalUnit（画布Scaler.Unit value））
- `float get_fallbackScreenDPI()`
  （float get_fallback屏幕的DPI（））
- `void set_fallbackScreenDPI(float value)`
  （void set_fallback屏幕的DPI（float value））
- `float get_defaultSpriteDPI()`
  （float get_default精灵DPI（））
- `void set_defaultSpriteDPI(float value)`
  （void set_default精灵DPI（float value））
- `float get_dynamicPixelsPerUnit()`
  （float get_dynamicPixelsPerUnit（））
- `void set_dynamicPixelsPerUnit(float value)`
  （void set_dynamicPixelsPerUnit（float value））
- `void OnEnable()`
  （void 启用时（））
- `void Canvas_preWillRenderCanvases()`
  （void Canvas_preWillRenderCanvases（））
- `void OnDisable()`
  （void 禁用时（））
- `void Handle()`
  （void 句柄（））
- `void HandleWorldCanvas()`
  （void 句柄世界的画布（））
- `void HandleConstantPixelSize()`
  （void 句柄ConstantPixel大小（））
- `void HandleScaleWithScreenSize()`
  （void 句柄缩放With屏幕的大小（））
- `void HandleConstantPhysicalSize()`
  （void 句柄ConstantPhysical大小（））
- `void SetScaleFactor(float scaleFactor)`
  （void 集合缩放系数（float scaleFactor））
- `void SetReferencePixelsPerUnit(float referencePixelsPerUnit)`
  （void 集合引用PixelsPerUnit（float referencePixelsPerUnit））

---

## CanvasScaler.ScaleMode（画布Scaler.缩放模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CanvasScaler.ScreenMatchMode（画布Scaler.屏幕的比赛模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CanvasScaler.Unit（画布Scaler.Unit）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CanvasUpdate（画布更新）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CanvasUpdateRegistry（画布更新Registry）

### 字段 (7)

- `CanvasUpdateRegistry s_Instance`（画布更新Registry s_实例）(偏移: 0x0)
- `bool m_PerformingLayoutUpdate`（bool m_PerformingLayout更新）(偏移: 0x8)
- `bool m_PerformingGraphicUpdate`（bool m_PerformingGraphic更新）(偏移: 0x9)
- `string[] m_CanvasUpdateProfilerStrings`（string[] m_画布更新ProfilerStrings）(偏移: 0xC)
- `IndexedSet<ICanvasElement> m_LayoutRebuildQueue`（IndexedSet<I画布Element> m_LayoutRebuild队列）(偏移: 0x10)
- `IndexedSet<ICanvasElement> m_GraphicRebuildQueue`（IndexedSet<I画布Element> m_GraphicRebuild队列）(偏移: 0x14)
- `Comparison<ICanvasElement> s_SortLayoutFunction`（Comparison<I画布Element> s_SortLayoutFunction）(偏移: 0x4)

### 方法 (17)

- `CanvasUpdateRegistry get_instance()`
  （画布更新Registry get_instance（））
- `bool ObjectValidForUpdate(ICanvasElement element)`
  （bool 对象ValidFor更新（I画布元素 element））
- `void CleanInvalidItems()`
  （void CleanInvalidItems（））
- `void PerformUpdate()`
  （void 执行更新（））
- `int ParentCount(Transform child)`
  （int 父级数量（变换 child））
- `int SortLayoutList(ICanvasElement x, ICanvasElement y)`
  （int SortLayout列表（I画布元素 x, I画布元素 y））
- `void RegisterCanvasElementForLayoutRebuild(ICanvasElement element)`
  （void Register画布元素ForLayoutRebuild（I画布元素 element））
- `bool TryRegisterCanvasElementForLayoutRebuild(ICanvasElement element)`
  （bool TryRegister画布元素ForLayoutRebuild（I画布元素 element））
- `bool InternalRegisterCanvasElementForLayoutRebuild(ICanvasElement element)`
  （bool 内部的Register画布元素ForLayoutRebuild（I画布元素 element））
- `void RegisterCanvasElementForGraphicRebuild(ICanvasElement element)`
  （void Register画布元素ForGraphicRebuild（I画布元素 element））
- `bool TryRegisterCanvasElementForGraphicRebuild(ICanvasElement element)`
  （bool TryRegister画布元素ForGraphicRebuild（I画布元素 element））
- `bool InternalRegisterCanvasElementForGraphicRebuild(ICanvasElement element)`
  （bool 内部的Register画布元素ForGraphicRebuild（I画布元素 element））
- `void UnRegisterCanvasElementForRebuild(ICanvasElement element)`
  （void UnRegister画布元素ForRebuild（I画布元素 element））
- `void InternalUnRegisterCanvasElementForLayoutRebuild(ICanvasElement element)`
  （void 内部的UnRegister画布元素ForLayoutRebuild（I画布元素 element））
- `void InternalUnRegisterCanvasElementForGraphicRebuild(ICanvasElement element)`
  （void 内部的UnRegister画布元素ForGraphicRebuild（I画布元素 element））
- `bool IsRebuildingLayout()`
  （bool 是否RebuildingLayout（））
- `bool IsRebuildingGraphics()`
  （bool 是否RebuildingGraphics（））

---

## CapsuleCollider（Capsule碰撞器）

**继承**: Collider（碰撞器）

### 方法 (6)

- `Vector3 get_center()`
  （三维向量 获取_中心（））
- `float get_radius()`
  （浮点数 获取_半径（））
- `float get_height()`
  （浮点数 获取_高度（））
- `void set_height(float value)`
  （void 设置_高度（浮点数 value））
- `int get_direction()`
  （int get_direction（））
- `void get_center_Injected(out Vector3 ret)`
  （void 获取_中心_注入（输出 Vector3 ret））

---

## Capture（Capture）

### 字段 (3)

- `string _text`（string _text）(偏移: 0x8)
- `int _index`（整数 _索引）(偏移: 0xC)
- `int _length`（int _length）(偏移: 0x10)

### 方法 (7)

- `int get_Index()`
  （int get_索引（））
- `int get_Length()`
  （整数 获取_长度（））
- `string get_Value()`
  （字符串 获取_值（））
- `string ToString()`
  （字符串 转字符串（））
- `string GetOriginalString()`
  （string 获取Original字符串（））
- `string GetLeftSubstring()`
  （string 获取左Substring（））
- `string GetRightSubstring()`
  （string 获取右Substring（））

---

## CapturePass（CapturePass）

**继承**: ScriptableRenderPass（可脚本化渲染通道）

### 字段 (2)

- `RenderTargetHandle m_CameraColorHandle`（Render目标句柄 m_摄像机颜色句柄）(偏移: 0x54)
- `ProfilingSampler m_ProfilingSampler`（性能分析采样器 m_性能分析采样器）(偏移: 0x0)

### 方法 (2)

- `void Setup(RenderTargetHandle colorHandle)`
  （void Setup（Render目标句柄 colorHandle））
- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（可脚本化渲染上下文 context, 引用 渲染数据 renderingData））

---

## CapturePixelFormat（CapturePixel格式化）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CaseInsensitiveComparer（CaseInsensitiveComparer）

**继承**: IComparer（I比较器）

### 字段 (1)

- `CompareInfo m_compareInfo`（比较信息 m_compare信息）(偏移: 0x8)

### 方法 (2)

- `CaseInsensitiveComparer get_Default()`
  （CaseInsensitiveComparer get_默认的（））
- `int Compare(object a, object b)`
  （整数 比较（对象 a, 对象 b））

---

## CaseInsensitiveHashCodeProvider（CaseInsensitiveHashCode提供者）

**继承**: IHashCodeProvider（IHashCode提供者）

### 字段 (1)

- `TextInfo m_text`（文本信息 m_text）(偏移: 0x8)

### 方法 (2)

- `CaseInsensitiveHashCodeProvider get_Default()`
  （CaseInsensitiveHashCode提供者 get_默认的（））
- `int GetHashCode(object obj)`
  （整数 获取哈希码（对象 obj））

---

## CatmullRomDecoder（CatmullRomDecoder）

**继承**: ABSPathDecoder（ABS路径Decoder）

### 字段 (2)

- `ControlPoint[] _PartialControlPs`（控制Point[] _Partial控制Ps）(偏移: 0x0)
- `Vector3[] _PartialWps`（Vector3[] _PartialWps）(偏移: 0x4)

### 方法 (5)

- `int get_minInputWaypoints()`
  （整数 获取_最小输入路点（））
- `void FinalizePath(Path p, Vector3[] wps, bool isClosedPath)`
  （void Finalize路径（路径 p, Vector3[] wps, bool isClosedPath））
- `Vector3 GetPoint(float perc, Vector3[] wps, Path p, ControlPoint[] controlPoints)`
  （三维向量 获取Point（float perc, Vector3[] wps, 路径 p, 控制Point[] controlPoints））
- `void SetTimeToLengthTables(Path p, int subdivisions)`
  （void 集合时间ToLengthTables（路径 p, int subdivisions））
- `void SetWaypointsLengths(Path p, int subdivisions)`
  （void 集合WaypointsLengths（路径 p, int subdivisions））

---

## CausalityRelation（CausalityRelation）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CausalitySynchronousWork（CausalitySynchronousWork）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CausalityTraceLevel（CausalityTrace等级）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Cer（Cer）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CertificateHandler（Certificate处理器）

### 字段 (1)

- `IntPtr m_Ptr`（整数指针 m_指针）(偏移: 0x8)

### 方法 (4)

- `void Release()`
  （void 释放（））
- `bool ValidateCertificate(byte[] certificateData)`
  （bool 验证Certificate（byte[] certificateData））
- `bool ValidateCertificateNative(byte[] certificateData)`
  （bool 验证CertificateNative（byte[] certificateData））
- `void Dispose()`
  （void 释放（））

---

## ChangeMovingRealSize（ChangeMovingReal大小）

### 字段 (5)

- `float DecreaseSpeed`（float DecreaseSpeed）(偏移: 0x0)
- `float Increase_Repeat`（float Increase_Repeat）(偏移: 0x4)
- `float Increase_Oneshot`（float Increase_Oneshot）(偏移: 0x8)
- `float Increase_OneshotOver`（float Increase_OneshotOver）(偏移: 0xC)
- `float Min`（float 最小）(偏移: 0x10)

---

## ChannelData（Channel数据）

### 字段 (7)

- `string Ref`（string Ref）(偏移: 0x8)
- `string Type`（string 类型）(偏移: 0xC)
- `string Id`（string Id）(偏移: 0x10)
- `string DelayLoadAsClientChannel`（string 延迟加载As客户端Channel）(偏移: 0x14)
- `ArrayList _serverProviders`（数组列表 _serverProviders）(偏移: 0x18)
- `ArrayList _clientProviders`（数组列表 _clientProviders）(偏移: 0x1C)
- `Hashtable _customProperties`（Hashtable _customProperties）(偏移: 0x20)

### 方法 (4)

- `ArrayList get_ServerProviders()`
  （数组列表 get_服务器Providers（））
- `ArrayList get_ClientProviders()`
  （数组列表 get_客户端Providers（））
- `Hashtable get_CustomProperties()`
  （Hashtable get_自定义的Properties（））
- `void CopyFrom(ChannelData other)`
  （void 复制From（Channel数据 other））

---

## ChannelInfo（Channel信息）

**继承**: IChannelInfo（IChannel信息）

### 字段 (1)

- `object[] channelData`（object[] channel数据）(偏移: 0x8)

### 方法 (1)

- `object[] get_ChannelData()`
  （object[] get_Channel数据（））

---

## ChannelMixer（ChannelMixer）

**继承**: VolumeComponent, IPostProcessComponent（体积组件, I后处理组件）

### 字段 (9)

- `ClampedFloatParameter redOutRedIn`（Clamped浮点数Parameter redOut红色In）(偏移: 0x1C)
- `ClampedFloatParameter redOutGreenIn`（Clamped浮点数Parameter redOut绿色In）(偏移: 0x20)
- `ClampedFloatParameter redOutBlueIn`（Clamped浮点数Parameter redOut蓝色In）(偏移: 0x24)
- `ClampedFloatParameter greenOutRedIn`（Clamped浮点数Parameter greenOut红色In）(偏移: 0x28)
- `ClampedFloatParameter greenOutGreenIn`（Clamped浮点数Parameter greenOut绿色In）(偏移: 0x2C)
- `ClampedFloatParameter greenOutBlueIn`（Clamped浮点数Parameter greenOut蓝色In）(偏移: 0x30)
- `ClampedFloatParameter blueOutRedIn`（Clamped浮点数Parameter blueOut红色In）(偏移: 0x34)
- `ClampedFloatParameter blueOutGreenIn`（Clamped浮点数Parameter blueOut绿色In）(偏移: 0x38)
- `ClampedFloatParameter blueOutBlueIn`（Clamped浮点数Parameter blueOut蓝色In）(偏移: 0x3C)

### 方法 (2)

- `bool IsActive()`
  （布尔值 是否激活的（））
- `bool IsTileCompatible()`
  （布尔值 是否瓦片兼容（））

---

## ChannelServices（ChannelServices）

### 字段 (5)

- `ArrayList registeredChannels`（数组列表 registeredChannels）(偏移: 0x0)
- `ArrayList delayedClientChannels`（数组列表 delayed客户端Channels）(偏移: 0x4)
- `CrossContextChannel _crossContextSink`（CrossContextChannel _crossContextSink）(偏移: 0x8)
- `string CrossContextUrl`（string CrossContextUrl）(偏移: 0xC)
- `IList oldStartModeTypes`（I列表 old开始模式Types）(偏移: 0x10)

### 方法 (12)

- `CrossContextChannel get_CrossContextChannel()`
  （CrossContextChannel get_CrossContextChannel（））
- `IMessageSink CreateClientChannelSinkChain(string url, object remoteChannelData, out string objectUri)`
  （IMessageSink 创建客户端ChannelSinkChain（string url, object remoteChannelData, out string objectUri））
- `IMessageSink CreateClientChannelSinkChain(IChannelSender sender, string url, object[] channelDataArray, out string objectUri)`
  （IMessageSink 创建客户端ChannelSinkChain（IChannelSender sender, string url, object[] channelDataArray, out string objectUri））
- `void RegisterChannel(IChannel chnl)`
  （void RegisterChannel（IChannel chnl））
- `void RegisterChannel(IChannel chnl, bool ensureSecurity)`
  （void RegisterChannel（IChannel chnl, bool ensureSecurity））
- `void RegisterChannelConfig(ChannelData channel)`
  （void RegisterChannel配置（Channel数据 channel））
- `object CreateProvider(ProviderData prov)`
  （object 创建提供者（提供者数据 prov））
- `IMessage SyncDispatchMessage(IMessage msg)`
  （IMessage 同步DispatchMessage（IMessage msg））
- `ReturnMessage CheckIncomingMessage(IMessage msg)`
  （ReturnMessage 检查IncomingMessage（IMessage msg））
- `IMessage CheckReturnMessage(IMessage callMsg, IMessage retMsg)`
  （IMessage 检查ReturnMessage（IMessage callMsg, IMessage retMsg））
- `bool IsLocalCall(IMessage callMsg)`
  （bool 是否本地的Call（IMessage callMsg））
- `object[] GetCurrentChannelInfo()`
  （object[] 获取当前Channel信息（））

---

## ChannelSound（Channel音效）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (5)

- `float inTime`（float in时间）(偏移: 0xC)
- `float outTime`（float out时间）(偏移: 0x10)
- `Func<bool> func`（Func<bool> func）(偏移: 0x14)
- `AudioSource source`（音频Source source）(偏移: 0x18)
- `bool shouldPlay`（bool should播放）(偏移: 0x1C)

### 方法 (4)

- `void Update()`
  （void 更新（））
- `void SetFadeDuration(float inTime, float outTime)`
  （void 集合Fade持续时间（float inTime, float outTime））
- `void SetJudgeFunction(Func<bool> func)`
  （void 集合JudgeFunction（Func<bool> func））
- `AudioSource GetSource()`
  （音频Source 获取Source（））

---

## Char（Char）

**继承**: IComparable, IConvertible, IComparable<char>, IEquatable<char>（IComparable, IConvertible, IComparable<char>, IEquatable<char>）

### 字段 (2)

- `char m_value`（char m_value）(偏移: 0x0)
- `byte[] categoryForLatin1`（byte[] categoryForLatin1）(偏移: 0x0)

### 方法 (39)

- `bool IsLatin1(char ch)`
  （bool 是否Latin1（char ch））
- `bool IsAscii(char ch)`
  （bool 是否Ascii（char ch））
- `UnicodeCategory GetLatin1UnicodeCategory(char ch)`
  （Unicode类别 获取Latin1Unicode类别（char ch））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(char obj)`
  （bool Equals（char obj））
- `int CompareTo(object value)`
  （整数 比较到（对象 value））
- `int CompareTo(char value)`
  （int CompareTo（char value））
- `string ToString()`
  （字符串 转字符串（））
- `string ToString(IFormatProvider provider)`
  （字符串 转字符串（I格式化提供者 provider））
- `string ToString(char c)`
  （string To字符串（char c））
- `char Parse(string s)`
  （char 解析（string s））
- `bool IsDigit(char c)`
  （bool 是否Digit（char c））
- `bool CheckLetter(UnicodeCategory uc)`
  （bool 检查Letter（Unicode类别 uc））
- `bool IsLetter(char c)`
  （bool 是否Letter（char c））
- `bool IsWhiteSpaceLatin1(char c)`
  （bool 是否WhiteSpaceLatin1（char c））
- `bool IsWhiteSpace(char c)`
  （bool 是否WhiteSpace（char c））
- `bool IsUpper(char c)`
  （bool 是否上半身（char c））
- `bool IsLower(char c)`
  （bool 是否下半身（char c））
- `bool CheckLetterOrDigit(UnicodeCategory uc)`
  （bool 检查LetterOrDigit（Unicode类别 uc））
- `bool IsLetterOrDigit(char c)`
  （bool 是否LetterOrDigit（char c））
- `char ToUpper(char c, CultureInfo culture)`
  （char To上半身（char c, Culture信息 culture））
- `char ToUpper(char c)`
  （char To上半身（char c））
- `char ToUpperInvariant(char c)`
  （char To上半身Invariant（char c））
- `char ToLower(char c, CultureInfo culture)`
  （char To下半身（char c, Culture信息 culture））
- `char ToLower(char c)`
  （char To下半身（char c））
- `char ToLowerInvariant(char c)`
  （char To下半身Invariant（char c））
- `TypeCode GetTypeCode()`
  （类型代码 获取类型代码（））
- `bool CheckNumber(UnicodeCategory uc)`
  （bool 检查Number（Unicode类别 uc））
- `bool IsNumber(char c)`
  （bool 是否Number（char c））
- `bool IsSurrogate(char c)`
  （bool 是否Surrogate（char c））
- `bool IsSurrogate(string s, int index)`
  （bool 是否Surrogate（string s, int index））
- `UnicodeCategory GetUnicodeCategory(char c)`
  （Unicode类别 获取Unicode类别（char c））
- `UnicodeCategory GetUnicodeCategory(string s, int index)`
  （Unicode类别 获取Unicode类别（string s, int index））
- `bool IsHighSurrogate(char c)`
  （bool 是否HighSurrogate（char c））
- `bool IsHighSurrogate(string s, int index)`
  （bool 是否HighSurrogate（string s, int index））
- `bool IsLowSurrogate(char c)`
  （bool 是否LowSurrogate（char c））
- `bool IsSurrogatePair(char highSurrogate, char lowSurrogate)`
  （bool 是否SurrogatePair（char highSurrogate, char lowSurrogate））
- `int ConvertToUtf32(char highSurrogate, char lowSurrogate)`
  （int 转换ToUtf32（char highSurrogate, char lowSurrogate））

---

## CharArrayTypeInfo（Char数组类型信息）

**继承**: TraceLoggingTypeInfo<char[]>（TraceLogging类型Info<char[]>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void 写入元数据（跟踪日志元数据收集器 collector, 字符串 name, 事件字段格式 format））
- `void WriteData(TraceLoggingDataCollector collector, ref char[] value)`
  （void Write数据（TraceLogging数据Collector collector, ref char[] value））

---

## CharEnumerator（CharEnumerator）

**继承**: IEnumerator, ICloneable, IEnumerator<char>, IDisposable（IEnumerator, ICloneable, IEnumerator<char>, IDisposable）

### 字段 (3)

- `string str`（string str）(偏移: 0x8)
- `int index`（整数 索引）(偏移: 0xC)
- `char currentElement`（char current元素）(偏移: 0x10)

### 方法 (5)

- `object Clone()`
  （对象 克隆（））
- `bool MoveNext()`
  （布尔值 移动下一个（））
- `void Dispose()`
  （void 释放（））
- `char get_Current()`
  （char get_当前（））
- `void Reset()`
  （void 重置（））

---

## CharSet（Char集合）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CharTypeInfo（Char类型信息）

**继承**: TraceLoggingTypeInfo<char>（TraceLogging类型Info<char>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void 写入元数据（跟踪日志元数据收集器 collector, 字符串 name, 事件字段格式 format））
- `void WriteData(TraceLoggingDataCollector collector, ref char value)`
  （void Write数据（TraceLogging数据Collector collector, ref char value））

---

## CharUnicodeInfo（CharUnicode信息）

### 字段 (5)

- `ushort[] s_pCategoryLevel1Index`（ushort[] s_p类别Level1索引）(偏移: 0x0)
- `byte[] s_pCategoriesValue`（byte[] s_pCategories值）(偏移: 0x4)
- `ushort[] s_pNumericLevel1Index`（ushort[] s_pNumericLevel1索引）(偏移: 0x8)
- `byte[] s_pNumericValues`（byte[] s_pNumericValues）(偏移: 0xC)
- `ushort[] s_pDigitValues`（ushort[] s_pDigitValues）(偏移: 0x10)

### 方法 (6)

- `int InternalConvertToUtf32(string s, int index)`
  （int 内部的转换ToUtf32（string s, int index））
- `bool IsWhiteSpace(char c)`
  （bool 是否WhiteSpace（char c））
- `UnicodeCategory GetUnicodeCategory(char ch)`
  （Unicode类别 获取Unicode类别（char ch））
- `UnicodeCategory InternalGetUnicodeCategory(int ch)`
  （Unicode类别 内部的获取Unicode类别（int ch））
- `byte InternalGetCategoryValue(int ch, int offset)`
  （byte 内部的获取类别值（int ch, int offset））
- `UnicodeCategory InternalGetUnicodeCategory(string value, int index)`
  （Unicode类别 内部的获取Unicode类别（string value, int index））

---

## CharUnicodeInfo.Debug（CharUnicodeInfo.Debug）

### 方法 (1)

- `void Assert(bool condition, string message)`
  （void Assert（bool condition, string message））

---

## CharWpnAnimData（Char武器动画数据）

### 字段 (3)

- `string upper`（string upper）(偏移: 0x0)
- `bool upper_4side`（bool upper_4side）(偏移: 0x4)
- `string lower`（string lower）(偏移: 0x8)

---

## CharacterAsset（角色资产）

**继承**: ScriptableObject（脚本对象）

### 字段 (2)

- `List<GameObject> characterList`（List<游戏Object> character列表）(偏移: 0xC)
- `List<GameObject> socketItems`（List<游戏Object> socketItems）(偏移: 0x10)

### 方法 (2)

- `GameObject GetCharacterPrefab(string name)`
  （游戏对象 获取角色预制体（string name））
- `GameObject GetSocketItemPrefab(string name)`
  （游戏对象 获取套接字项目预制体（string name））

---

## CharacterController（角色控制器）

**继承**: Collider（碰撞器）

### 方法 (11)

- `bool SimpleMove(Vector3 speed)`
  （bool Simple移动（三维向量 speed））
- `CollisionFlags Move(Vector3 motion)`
  （CollisionFlags 移动（三维向量 motion））
- `bool get_isGrounded()`
  （布尔值 获取_是否着地（））
- `float get_radius()`
  （浮点数 获取_半径（））
- `float get_height()`
  （浮点数 获取_高度（））
- `void set_height(float value)`
  （void 设置_高度（浮点数 value））
- `Vector3 get_center()`
  （三维向量 获取_中心（））
- `float get_skinWidth()`
  （float get_skin宽度（））
- `bool SimpleMove_Injected(ref Vector3 speed)`
  （bool SimpleMove_Injected（ref Vector3 speed））
- `CollisionFlags Move_Injected(ref Vector3 motion)`
  （CollisionFlags Move_Injected（ref Vector3 motion））
- `void get_center_Injected(out Vector3 ret)`
  （void 获取_中心_注入（输出 Vector3 ret））

---

## CharacterEffect（角色特效）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (3)

- `CharacterEffect.FxData[] datas`（角色Effect.特效Data[] datas）(偏移: 0xC)
- `Player owner`（玩家 所有者）(偏移: 0x10)
- `List<EffectObj> fxList`（List<特效Obj> fx列表）(偏移: 0x14)

### 方法 (5)

- `bool get_isFxEnable()`
  （bool get_is特效启用（））
- `void set_isFxEnable(bool value)`
  （void set_is特效启用（bool value））
- `void SetEffectState(bool active)`
  （void 集合特效状态（bool active））
- `EffectObj ApplyFxData(CharacterEffect.FxData data)`
  （特效Obj 应用特效数据（角色Effect.特效数据 data））
- `void RemoveEffect(EffectObj fx)`
  （void 移除特效（特效Obj fx））

---

## CharacterEffect.FxData（角色Effect.特效数据）

### 字段 (4)

- `Transform node`（变换 node）(偏移: 0x0)
- `Vector3 offset`（三维向量 偏移）(偏移: 0x4)
- `Vector3 euler`（三维向量 欧拉角）(偏移: 0x10)
- `GameObject fxPrefab`（游戏对象 fx预制体）(偏移: 0x1C)

---

## CharacterModel（角色模型）

**继承**: Model（模型）

### 字段 (26)

- `CharacterModel.Sex sex`（角色Model.Sex sex）(偏移: 0x40)
- `bool recycle`（bool recycle）(偏移: 0x44)
- `Animator characterAnimator`（动画器 character动画器）(偏移: 0x48)
- `Animator handAnimator`（动画器 hand动画器）(偏移: 0x4C)
- `CharacterEffect characterEffect`（角色特效 character特效）(偏移: 0x50)
- `Renderer[] cvRenderers`（Renderer[] cvRenderers）(偏移: 0x54)
- `AudioClip dieVoice`（音频弹匣 dieVoice）(偏移: 0x58)
- `Transform spine`（变换 spine）(偏移: 0x5C)
- `Transform spine1`（变换 spine1）(偏移: 0x60)
- `Transform neck`（变换 neck）(偏移: 0x64)
- `string[] socketItemsName`（string[] socketItems名称）(偏移: 0x68)
- `bool isInit`（bool is初始化）(偏移: 0x70)
- `Transform[] hitboxes`（Transform[] hitboxes）(偏移: 0x74)
- `float targetLowerAngle`（float target下半身角度）(偏移: 0x78)
- `float lowerAngle`（float lower角度）(偏移: 0x7C)
- `CharacterVoice voiceAsset`（角色语音 voice资产）(偏移: 0x80)
- `HUD_RoleAsset roleAsset`（HUD_Role资产 role资产）(偏移: 0x84)
- `CharacterModel.MoveDirection deathDir`（角色Model.移动方向 deathDir）(偏移: 0x88)
- `CharacterModel.MoveDirection lastMovDir`（角色Model.移动方向 lastMovDir）(偏移: 0x8C)
- `string lowerAnimName`（string lower动画名称）(偏移: 0x90)
- `string lowerAnimName_Temp`（string lower动画Name_Temp）(偏移: 0x94)
- `string lowerAnimTag`（string lower动画标签）(偏移: 0x98)
- `string upperAnimName`（string upper动画名称）(偏移: 0x9C)
- `CharWpnAnimData animSetting`（Char武器动画数据 anim设置）(偏移: 0xA0)
- `ParticleSystem aliveEffect`（粒子系统 alive特效）(偏移: 0xAC)
- `bool reverseSpineRotation`（bool reverseSpineRotation）(偏移: 0xB0)

### 方法 (39)

- `Helmet get_helmet()`
  （头盔 get_helmet（））
- `void set_helmet(Helmet value)`
  （void set_helmet（头盔 value））
- `QVModel get_bindQvMdl()`
  （QV模型 get_bindQv模型（））
- `void set_bindQvMdl(QVModel value)`
  （void set_bindQv模型（QV模型 value））
- `void OnEnable()`
  （void 启用时（））
- `void Update()`
  （void 更新（））
- `void LateUpdate()`
  （void 延迟更新（））
- `void BindQvModel(GameObject mdlPrefab)`
  （void BindQv模型（游戏对象 mdlPrefab））
- `void BindMapGunQvModel(QVModel qvMdl)`
  （void Bind映射枪械Qv模型（QV模型 qvMdl））
- `void RecycleCurQvModel()`
  （void RecycleCurQv模型（））
- `void SetOwner(Player newOwner)`
  （void 集合Owner（玩家 newOwner））
- `void SetValidOwner()`
  （void 设置有效所有者（））
- `void RemoveFromOldOwner()`
  （void 从旧所有者移除（））
- `void InitSocketItem()`
  （void 初始化套接字项目（））
- `void SetActive(bool active)`
  （void 设置激活（布尔值 active））
- `void PlayHitAnim(Vector3 dmgOrigin)`
  （void 播放命中动画（三维向量 dmgOrigin））
- `void OnPlayerRespawn()`
  （void On玩家重生（））
- `void OnPlayerDeath(bool explosion, bool headshot, bool isHitLower)`
  （void On玩家死亡（bool explosion, bool headshot, bool isHitLower））
- `void PlayJumpAnim(string animName = "M-jump")`
  （void 播放跳跃动画（string animName = "M-jump"））
- `void PlayGunReloadAnim(string gunName)`
  （void 播放枪械换弹动画（string gunName））
- `void PlayWpnAnim(string animName, float duration = 0.2)`
  （void 播放武器动画（string animName, float duration = 0.2））
- `void StopWeaponAnim(float duration = 0)`
  （void 停止Weapon动画（float duration = 0））
- `void SetLowerAnimRate(float run, float walk, float crouchWalk)`
  （void 集合下半身动画Rate（float run, float walk, float crouchWalk））
- `CharacterModel.MoveDirection GetMoveDirByNum(Vector3Int dir)`
  （角色Model.移动方向 获取移动DirByNum（三维向量整数 dir））
- `CharacterModel.MoveDirection GetMoveDirByNum(int x, int z)`
  （角色Model.移动方向 获取移动DirByNum（int x, int z））
- `CharacterModel.MoveDirection GetDeathDirection(float angle)`
  （角色Model.移动方向 获取死亡方向（float angle））
- `void SetWeaponAnim(CharWpnAnimData animData)`
  （void 集合Weapon动画（Char武器动画数据 animData））
- `void ResetAnimator()`
  （void 重置动画器（））
- `void UpdateLowerAngle()`
  （void 更新下半身角度（））
- `void UpdateAnim()`
  （void 更新动画（））
- `string CombineAnimName(CharacterModel.MoveDirection moveDir, bool walk, bool crouch)`
  （string Combine动画名称（角色Model.移动方向 moveDir, bool walk, bool crouch））
- `void PlayUpperAnim(string animName, float lerpTime = 0.2, bool cancelIfPlaying = True)`
  （void 播放上半身动画（string animName, float lerpTime = 0.2, bool cancelIfPlaying = True））
- `void PlayLowerAnim(string animName, string animTag, float lerpTime = 0.2, bool cancelIfPlaying = True)`
  （void 播放下半身动画（string animName, string animTag, float lerpTime = 0.2, bool cancelIfPlaying = True））
- `void PlayTempLowerAnim(string animName, string animTag, float lerpTime = 0.2, bool cancelIfPlaying = False)`
  （void 播放Temp下半身动画（string animName, string animTag, float lerpTime = 0.2, bool cancelIfPlaying = False））
- `void PlayDeathAnim(string animName, float lerpTime = 0)`
  （void 播放死亡动画（string animName, float lerpTime = 0））
- `void StopDeathAnim()`
  （void 停止死亡动画（））
- `void Nano6CharacterSetting(bool isAlive)`
  （void Nano6角色设置（bool isAlive））
- `Transform GetVisibleHitBox(Ray viewRay)`
  （变换 获取可见命中框（射线 viewRay））
- `bool CheckHitBox(Ray viewRay, Transform box)`
  （bool 检查命中Box（Ray viewRay, 变换 box））

---

## CharacterModel.MoveDirection（角色Model.移动方向）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CharacterModel.Sex（角色Model.Sex）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CharacterVoice（角色语音）

**继承**: ScriptableObject（脚本对象）

### 字段 (13)

- `AudioClip headShot`（音频弹匣 head射击）(偏移: 0xC)
- `AudioClip[] multilKill`（音频Clip[] multil击杀）(偏移: 0x10)
- `AudioClip grenade`（音频弹匣 grenade）(偏移: 0x14)
- `AudioClip knife`（音频弹匣 knife）(偏移: 0x18)
- `AudioClip die`（音频弹匣 die）(偏移: 0x1C)
- `AudioClip[] fireInTheHole`（音频Clip[] fireInTheHole）(偏移: 0x20)
- `AudioClip[] fireInTheHole_C`（音频Clip[] fireInTheHole_C）(偏移: 0x24)
- `AudioClip gameStart_TD`（音频弹匣 gameStart_TD）(偏移: 0x28)
- `AudioClip gameWin`（音频弹匣 gameWin）(偏移: 0x2C)
- `AudioClip gameDraw`（音频弹匣 gameDraw）(偏移: 0x30)
- `AudioClip gameLose`（音频弹匣 gameLose）(偏移: 0x34)
- `AudioClip gameStart_DM`（音频弹匣 gameStart_DM）(偏移: 0x38)
- `AudioClip gameOver_DM`（音频弹匣 gameOver_DM）(偏移: 0x3C)

---

## Checksum（Checksum）

### 方法 (1)

- `uint GetChecksum(byte[] arr, uint hash)`
  （uint 获取Checksum（byte[] arr, uint hash））

---

## ChoiceBase（选择基类）

### 字段 (3)

- `Parent parent`（父级 parent）(偏移: 0x8)
- `int index`（整数 索引）(偏移: 0xC)
- `string name`（字符串 名称）(偏移: 0x10)

### 方法 (2)

- `string GetText()`
  （string 获取文本（））
- `bool GetFocus()`
  （bool 获取聚焦（））

---

## ChromaticAberration（ChromaticAberration）

**继承**: VolumeComponent, IPostProcessComponent（体积组件, I后处理组件）

### 字段 (1)

- `ClampedFloatParameter intensity`（钳制浮点数参数 强度）(偏移: 0x1C)

### 方法 (2)

- `bool IsActive()`
  （布尔值 是否激活的（））
- `bool IsTileCompatible()`
  （布尔值 是否瓦片兼容（））

---

## Cinemachine3rdPersonAim（Cinemachine3rdPersonAim）

**继承**: CinemachineExtension（Cinemachine扩展）

### 字段 (4)

- `LayerMask AimCollisionFilter`（层掩码 AimCollisionFilter）(偏移: 0x14)
- `string IgnoreTag`（string Ignore标签）(偏移: 0x18)
- `float AimDistance`（float Aim距离）(偏移: 0x1C)
- `RectTransform AimTargetReticle`（Rect变换 Aim目标Reticle）(偏移: 0x20)

### 方法 (6)

- `void OnValidate()`
  （void 验证时（））
- `void Reset()`
  （void 重置（））
- `bool OnTransitionFromCamera(ICinemachineCamera fromCam, Vector3 worldUp, float deltaTime)`
  （bool OnTransitionFrom摄像机（ICinemachine摄像机 fromCam, 三维向量 worldUp, float deltaTime））
- `void DrawReticle(CinemachineBrain brain)`
  （void DrawReticle（Cinemachine爆头 brain））
- `Vector3 GetLookAtPoint(Vector3 camPos)`
  （三维向量 获取LookAtPoint（三维向量 camPos））
- `void PostPipelineStageCallback(CinemachineVirtualCameraBase vcam, CinemachineCore.Stage stage, ref CameraState state, float deltaTime)`
  （void 后管线阶段回调（Cinemachine虚拟摄像机基类 vcam, CinemachineCore.阶段 stage, 引用 CameraState state, 浮点数 deltaTime））

---

## Cinemachine3rdPersonFollow（Cinemachine3rdPersonFollow）

**继承**: CinemachineComponentBase（Cinemachine组件基类）

### 字段 (11)

- `Vector3 Damping`（三维向量 Damping）(偏移: 0x28)
- `Vector3 ShoulderOffset`（三维向量 ShoulderOffset）(偏移: 0x34)
- `float VerticalArmLength`（float 垂直手臂Length）(偏移: 0x40)
- `float CameraSide`（float 摄像机侧面）(偏移: 0x44)
- `float CameraDistance`（float 摄像机距离）(偏移: 0x48)
- `LayerMask CameraCollisionFilter`（层掩码 摄像机CollisionFilter）(偏移: 0x4C)
- `string IgnoreTag`（string Ignore标签）(偏移: 0x50)
- `float CameraRadius`（float 摄像机Radius）(偏移: 0x54)
- `Vector3 m_PreviousFollowTargetPosition`（三维向量 m_上一个Follow目标Position）(偏移: 0x58)
- `Vector3 m_DampingCorrection`（三维向量 m_DampingCorrection）(偏移: 0x64)
- `float m_CamPosCollisionCorrection`（float m_CamPosCollisionCorrection）(偏移: 0x70)

### 方法 (13)

- `void OnValidate()`
  （void 验证时（））
- `void Reset()`
  （void 重置（））
- `void OnDestroy()`
  （void 销毁时（））
- `bool get_IsValid()`
  （布尔值 获取_是否有效（））
- `CinemachineCore.Stage get_Stage()`
  （CinemachineCore.阶段 获取_阶段（））
- `float GetMaxDampTime()`
  （浮点数 获取最大阻尼时间（））
- `void MutateCameraState(ref CameraState curState, float deltaTime)`
  （void 变更摄像机状态（引用 CameraState curState, 浮点数 deltaTime））
- `void OnTargetObjectWarped(Transform target, Vector3 positionDelta)`
  （void 目标对象扭曲时（变换 target, 三维向量 位置增量））
- `void PositionCamera(ref CameraState curState, float deltaTime)`
  （void Position摄像机（ref CameraState curState, float deltaTime））
- `void GetRigPositions(out Vector3 root, out Vector3 shoulder, out Vector3 hand)`
  （void 获取RigPositions（out Vector3 root, out Vector3 shoulder, out Vector3 hand））
- `Quaternion GetHeading(Vector3 targetForward, Vector3 up)`
  （Quaternion 获取Heading（三维向量 targetForward, 三维向量 up））
- `void GetRawRigPositions(Vector3 root, Quaternion targetRot, Quaternion heading, out Vector3 shoulder, out Vector3 hand)`
  （void 获取RawRigPositions（三维向量 root, Quaternion targetRot, Quaternion heading, out Vector3 shoulder, out Vector3 hand））
- `Vector3 ResolveCollisions(Vector3 root, Vector3 tip, float cameraRadius)`
  （三维向量 ResolveCollisions（三维向量 root, 三维向量 tip, float cameraRadius））

---

## CinemachineBasicMultiChannelPerlin（CinemachineBasic多个ChannelPerlin）

**继承**: CinemachineComponentBase（Cinemachine组件基类）

### 字段 (7)

- `NoiseSettings m_NoiseProfile`（NoiseSettings m_NoiseProfile）(偏移: 0x28)
- `Vector3 m_PivotOffset`（三维向量 m_PivotOffset）(偏移: 0x2C)
- `float m_AmplitudeGain`（float m_AmplitudeGain）(偏移: 0x38)
- `float m_FrequencyGain`（float m_FrequencyGain）(偏移: 0x3C)
- `bool mInitialized`（bool mInitialized）(偏移: 0x40)
- `float mNoiseTime`（float mNoise时间）(偏移: 0x44)
- `Vector3 mNoiseOffsets`（三维向量 mNoiseOffsets）(偏移: 0x48)

### 方法 (5)

- `bool get_IsValid()`
  （布尔值 获取_是否有效（））
- `CinemachineCore.Stage get_Stage()`
  （CinemachineCore.阶段 获取_阶段（））
- `void MutateCameraState(ref CameraState curState, float deltaTime)`
  （void 变更摄像机状态（引用 CameraState curState, 浮点数 deltaTime））
- `void ReSeed()`
  （void ReSeed（））
- `void Initialize()`
  （void 初始化（））

---

## CinemachineBlend（CinemachineBlend）

### 方法 (17)

- `ICinemachineCamera get_CamA()`
  （ICinemachine摄像机 get_CamA（））
- `void set_CamA(ICinemachineCamera value)`
  （void set_CamA（ICinemachine摄像机 value））
- `ICinemachineCamera get_CamB()`
  （ICinemachine摄像机 get_CamB（））
- `void set_CamB(ICinemachineCamera value)`
  （void set_CamB（ICinemachine摄像机 value））
- `AnimationCurve get_BlendCurve()`
  （动画Curve get_BlendCurve（））
- `void set_BlendCurve(AnimationCurve value)`
  （void set_BlendCurve（动画Curve value））
- `float get_TimeInBlend()`
  （float get_时间InBlend（））
- `void set_TimeInBlend(float value)`
  （void set_时间InBlend（float value））
- `float get_BlendWeight()`
  （float get_BlendWeight（））
- `bool get_IsValid()`
  （布尔值 获取_是否有效（））
- `float get_Duration()`
  （float get_持续时间（））
- `void set_Duration(float value)`
  （void set_持续时间（float value））
- `bool get_IsComplete()`
  （bool get_是否Complete（））
- `string get_Description()`
  （字符串 获取_描述（））
- `bool Uses(ICinemachineCamera cam)`
  （bool Uses（ICinemachine摄像机 cam））
- `void UpdateCameraState(Vector3 worldUp, float deltaTime)`
  （void 更新摄像机状态（三维向量 worldUp, 浮点数 deltaTime））
- `CameraState get_State()`
  （摄像机状态 get_状态（））

---

## CinemachineBlendDefinition（CinemachineBlendDefinition）

### 字段 (4)

- `CinemachineBlendDefinition.Style m_Style`（CinemachineBlendDefinition.Style m_Style）(偏移: 0x0)
- `float m_Time`（float m_时间）(偏移: 0x4)
- `AnimationCurve m_CustomCurve`（动画Curve m_自定义的Curve）(偏移: 0x8)
- `AnimationCurve[] sStandardCurves`（动画Curve[] sStandardCurves）(偏移: 0x0)

### 方法 (3)

- `float get_BlendTime()`
  （float get_Blend时间（））
- `void CreateStandardCurves()`
  （void 创建StandardCurves（））
- `AnimationCurve get_BlendCurve()`
  （动画Curve get_BlendCurve（））

---

## CinemachineBlendDefinition.Style（CinemachineBlendDefinition.Style）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineBlendListCamera（CinemachineBlend列表摄像机）

**继承**: CinemachineVirtualCameraBase（Cinemachine虚拟摄像机基类）

### 字段 (10)

- `Transform m_LookAt`（变换 m_看向）(偏移: 0x40)
- `Transform m_Follow`（变换 m_跟随）(偏移: 0x44)
- `bool m_ShowDebugText`（布尔值 m_显示调试文本）(偏移: 0x48)
- `bool m_Loop`（bool m_Loop）(偏移: 0x49)
- `CinemachineVirtualCameraBase[] m_ChildCameras`（Cinemachine虚拟摄像机Base[] m_子摄像机）(偏移: 0x4C)
- `CinemachineBlendListCamera.Instruction[] m_Instructions`（CinemachineBlend列表Camera.Instruction[] m_Instructions）(偏移: 0x50)
- `CameraState m_State`（摄像机状态 m_状态）(偏移: 0x5C)
- `float mActivationTime`（float mActivation时间）(偏移: 0x114)
- `int mCurrentInstruction`（int m当前Instruction）(偏移: 0x118)
- `CinemachineBlend mActiveBlend`（CinemachineBlend m激活的Blend）(偏移: 0x11C)

### 方法 (26)

- `string get_Description()`
  （字符串 获取_描述（））
- `void Reset()`
  （void 重置（））
- `void set_LiveChild(ICinemachineCamera value)`
  （void 设置_活动子级（ICinemachine摄像机 value））
- `ICinemachineCamera get_LiveChild()`
  （ICinemachine摄像机 获取_活动子级（））
- `bool IsLiveChild(ICinemachineCamera vcam, bool dominantChildOnly = False)`
  （布尔值 是否活动子级（ICinemachine摄像机 vcam, 布尔值 仅主从子级 = 假））
- `CameraState get_State()`
  （摄像机状态 get_状态（））
- `Transform get_LookAt()`
  （变换 获取_看向（））
- `void set_LookAt(Transform value)`
  （void 设置_看向（变换 value））
- `Transform get_Follow()`
  （变换 获取_跟随（））
- `void set_Follow(Transform value)`
  （void 设置_跟随（变换 value））
- `void OnTargetObjectWarped(Transform target, Vector3 positionDelta)`
  （void 目标对象扭曲时（变换 target, 三维向量 位置增量））
- `void ForceCameraPosition(Vector3 pos, Quaternion rot)`
  （void 强制摄像机位置（三维向量 pos, 四元数 rot））
- `void OnTransitionFromCamera(ICinemachineCamera fromCam, Vector3 worldUp, float deltaTime)`
  （void 从摄像机过渡时（ICinemachine摄像机 fromCam, 三维向量 worldUp, 浮点数 deltaTime））
- `ICinemachineCamera get_TransitioningFrom()`
  （ICinemachine摄像机 get_TransitioningFrom（））
- `void set_TransitioningFrom(ICinemachineCamera value)`
  （void set_TransitioningFrom（ICinemachine摄像机 value））
- `void InternalUpdateCameraState(Vector3 worldUp, float deltaTime)`
  （void 内部更新摄像机状态（三维向量 worldUp, 浮点数 deltaTime））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `void OnTransformChildrenChanged()`
  （void 变换子级改变时（））
- `void OnGuiHandler()`
  （void GUI处理器（））
- `CinemachineVirtualCameraBase[] get_ChildCameras()`
  （Cinemachine虚拟摄像机Base[] 获取_子摄像机（））
- `bool get_IsBlending()`
  （布尔值 获取_是否混合（））
- `void InvalidateListOfChildren()`
  （void 使无效子级列表（））
- `void UpdateListOfChildren()`
  （void 更新列表OfChildren（））
- `void ValidateInstructions()`
  （void 验证Instructions（））
- `void AdvanceCurrentInstruction(float deltaTime)`
  （void Advance当前Instruction（float deltaTime））

---

## CinemachineBlendListCamera.Instruction（CinemachineBlend列表Camera.Instruction）

### 字段 (3)

- `CinemachineVirtualCameraBase m_VirtualCamera`（Cinemachine虚拟的摄像机基础 m_虚拟的摄像机）(偏移: 0x0)
- `float m_Hold`（float m_Hold）(偏移: 0x4)
- `CinemachineBlendDefinition m_Blend`（CinemachineBlendDefinition m_Blend）(偏移: 0x8)

---

## CinemachineBlenderSettings（CinemachineBlenderSettings）

**继承**: ScriptableObject（脚本对象）

### 字段 (1)

- `CinemachineBlenderSettings.CustomBlend[] m_CustomBlends`（CinemachineBlenderSettings.自定义的Blend[] m_自定义的Blends）(偏移: 0xC)

### 方法 (1)

- `CinemachineBlendDefinition GetBlendForVirtualCameras(string fromCameraName, string toCameraName, CinemachineBlendDefinition defaultBlend)`
  （CinemachineBlendDefinition 获取BlendFor虚拟的Cameras（string fromCameraName, string toCameraName, CinemachineBlendDefinition defaultBlend））

---

## CinemachineBlenderSettings.CustomBlend（CinemachineBlenderSettings.自定义的Blend）

### 字段 (3)

- `string m_From`（string m_From）(偏移: 0x0)
- `string m_To`（string m_To）(偏移: 0x4)
- `CinemachineBlendDefinition m_Blend`（CinemachineBlendDefinition m_Blend）(偏移: 0x8)

---

## CinemachineBrain（Cinemachine爆头）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (20)

- `bool m_ShowDebugText`（布尔值 m_显示调试文本）(偏移: 0xC)
- `bool m_ShowCameraFrustum`（bool m_显示摄像机Frustum）(偏移: 0xD)
- `bool m_IgnoreTimeScale`（bool m_Ignore时间缩放）(偏移: 0xE)
- `Transform m_WorldUpOverride`（变换 m_世界的上重写）(偏移: 0x10)
- `CinemachineBrain.UpdateMethod m_UpdateMethod`（CinemachineBrain.更新Method m_更新Method）(偏移: 0x14)
- `CinemachineBrain.BrainUpdateMethod m_BlendUpdateMethod`（CinemachineBrain.爆头更新Method m_Blend更新Method）(偏移: 0x18)
- `CinemachineBlendDefinition m_DefaultBlend`（CinemachineBlendDefinition m_默认的Blend）(偏移: 0x1C)
- `CinemachineBlenderSettings m_CustomBlends`（CinemachineBlenderSettings m_自定义的Blends）(偏移: 0x28)
- `Camera m_OutputCamera`（摄像机 m_Output摄像机）(偏移: 0x2C)
- `CinemachineBrain.BrainEvent m_CameraCutEvent`（CinemachineBrain.爆头事件 m_摄像机Cut事件）(偏移: 0x30)
- `CinemachineBrain.VcamActivatedEvent m_CameraActivatedEvent`（CinemachineBrain.VcamActivated事件 m_摄像机Activated事件）(偏移: 0x34)
- `ICinemachineCamera mSoloCamera`（ICinemachine摄像机 mSolo摄像机）(偏移: 0x0)
- `Coroutine mPhysicsCoroutine`（协程 m物理协程）(偏移: 0x38)
- `int m_LastFrameUpdated`（int m_最后一个FrameUpdated）(偏移: 0x3C)
- `WaitForFixedUpdate mWaitForFixedUpdate`（WaitFor固定更新 mWaitFor固定更新）(偏移: 0x40)
- `List<CinemachineBrain.BrainFrame> mFrameStack`（List<CinemachineBrain.爆头Frame> mFrame栈）(偏移: 0x44)
- `int mNextFrameId`（int m下一个FrameId）(偏移: 0x48)
- `CinemachineBlend mCurrentLiveCameras`（CinemachineBlend m当前LiveCameras）(偏移: 0x4C)
- `AnimationCurve mDefaultLinearAnimationCurve`（动画Curve m默认的Linear动画Curve）(偏移: 0x4)
- `ICinemachineCamera mActiveCameraPreviousFrame`（ICinemachine摄像机 m激活的摄像机上一个Frame）(偏移: 0x50)

### 方法 (32)

- `Camera get_OutputCamera()`
  （摄像机 get_Output摄像机（））
- `ICinemachineCamera get_SoloCamera()`
  （ICinemachine摄像机 get_Solo摄像机（））
- `void set_SoloCamera(ICinemachineCamera value)`
  （void set_Solo摄像机（ICinemachine摄像机 value））
- `Color GetSoloGUIColor()`
  （颜色 获取SoloGUI颜色（））
- `Vector3 get_DefaultWorldUp()`
  （三维向量 get_默认的世界的上（））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `void OnSceneLoaded(Scene scene, LoadSceneMode mode)`
  （void On场景Loaded（场景 scene, 加载场景模式 mode））
- `void OnSceneUnloaded(Scene scene)`
  （void On场景Unloaded（场景 scene））
- `void Start()`
  （void 开始（））
- `void OnGuiHandler()`
  （void GUI处理器（））
- `IEnumerator AfterPhysics()`
  （IEnumerator After物理（））
- `void LateUpdate()`
  （void 延迟更新（））
- `void ManualUpdate()`
  （void 手动更新（））
- `float GetEffectiveDeltaTime(bool fixedDelta)`
  （float 获取EffectiveDelta时间（bool fixedDelta））
- `void UpdateVirtualCameras(CinemachineCore.UpdateFilter updateFilter, float deltaTime)`
  （void 更新虚拟的Cameras（CinemachineCore.更新Filter updateFilter, float deltaTime））
- `ICinemachineCamera get_ActiveVirtualCamera()`
  （ICinemachine摄像机 get_激活的虚拟的摄像机（））
- `ICinemachineCamera DeepCamBFromBlend(CinemachineBlend blend)`
  （ICinemachine摄像机 DeepCamBFromBlend（CinemachineBlend blend））
- `bool get_IsBlending()`
  （布尔值 获取_是否混合（））
- `CinemachineBlend get_ActiveBlend()`
  （CinemachineBlend get_激活的Blend（））
- `int GetBrainFrame(int withId)`
  （int 获取爆头Frame（int withId））
- `int SetCameraOverride(int overrideId, ICinemachineCamera camA, ICinemachineCamera camB, float weightB, float deltaTime)`
  （int 集合摄像机重写（int overrideId, ICinemachine摄像机 camA, ICinemachine摄像机 camB, float weightB, float deltaTime））
- `void ReleaseCameraOverride(int overrideId)`
  （void Release摄像机重写（int overrideId））
- `void ProcessActiveCamera(float deltaTime)`
  （void 处理激活的摄像机（float deltaTime））
- `void UpdateFrame0(float deltaTime)`
  （void 更新Frame0（float deltaTime））
- `void ComputeCurrentBlend(ref CinemachineBlend outputBlend, int numTopLayersToExclude)`
  （void Compute当前Blend（ref CinemachineBlend outputBlend, int numTopLayersToExclude））
- `bool IsLive(ICinemachineCamera vcam, bool dominantChildOnly = False)`
  （bool 是否Live（ICinemachine摄像机 vcam, bool dominantChildOnly = False））
- `CameraState get_CurrentCameraState()`
  （摄像机状态 get_当前摄像机状态（））
- `void set_CurrentCameraState(CameraState value)`
  （void set_当前摄像机状态（摄像机状态 value））
- `ICinemachineCamera TopCameraFromPriorityQueue()`
  （ICinemachine摄像机 顶部摄像机FromPriority队列（））
- `CinemachineBlendDefinition LookupBlend(ICinemachineCamera fromKey, ICinemachineCamera toKey)`
  （CinemachineBlendDefinition LookupBlend（ICinemachine摄像机 fromKey, ICinemachine摄像机 toKey））
- `void PushStateToUnityCamera(CameraState state)`
  （void Push状态ToUnity引擎摄像机（摄像机状态 state））

---

## CinemachineBrain.BrainFrame（CinemachineBrain.爆头Frame）

### 字段 (5)

- `int id`（整数 id）(偏移: 0x8)
- `CinemachineBlend blend`（CinemachineBlend blend）(偏移: 0xC)
- `CinemachineBlend workingBlend`（CinemachineBlend workingBlend）(偏移: 0x10)
- `BlendSourceVirtualCamera workingBlendSource`（BlendSource虚拟的摄像机 workingBlendSource）(偏移: 0x14)
- `float deltaTimeOverride`（float delta时间重写）(偏移: 0x18)

### 方法 (1)

- `bool get_Active()`
  （bool get_激活的（））

---

## CinemachineBrain.BrainUpdateMethod（CinemachineBrain.爆头更新Method）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineBrain.UpdateMethod（CinemachineBrain.更新Method）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineCameraOffset（Cinemachine摄像机Offset）

**继承**: CinemachineExtension（Cinemachine扩展）

### 字段 (3)

- `Vector3 m_Offset`（三维向量 m_Offset）(偏移: 0x14)
- `CinemachineCore.Stage m_ApplyAfter`（CinemachineCore.Stage m_应用After）(偏移: 0x20)
- `bool m_PreserveComposition`（bool m_PreserveComposition）(偏移: 0x24)

### 方法 (1)

- `void PostPipelineStageCallback(CinemachineVirtualCameraBase vcam, CinemachineCore.Stage stage, ref CameraState state, float deltaTime)`
  （void 后管线阶段回调（Cinemachine虚拟摄像机基类 vcam, CinemachineCore.阶段 stage, 引用 CameraState state, 浮点数 deltaTime））

---

## CinemachineClearShot（Cinemachine清除射击）

**继承**: CinemachineVirtualCameraBase（Cinemachine虚拟摄像机基类）

### 字段 (16)

- `Transform m_LookAt`（变换 m_看向）(偏移: 0x40)
- `Transform m_Follow`（变换 m_跟随）(偏移: 0x44)
- `bool m_ShowDebugText`（布尔值 m_显示调试文本）(偏移: 0x48)
- `CinemachineVirtualCameraBase[] m_ChildCameras`（Cinemachine虚拟摄像机Base[] m_子摄像机）(偏移: 0x4C)
- `float m_ActivateAfter`（float m_激活After）(偏移: 0x50)
- `float m_MinDuration`（float m_最小持续时间）(偏移: 0x54)
- `bool m_RandomizeChoice`（bool m_RandomizeChoice）(偏移: 0x58)
- `CinemachineBlendDefinition m_DefaultBlend`（CinemachineBlendDefinition m_默认的Blend）(偏移: 0x5C)
- `CinemachineBlenderSettings m_CustomBlends`（CinemachineBlenderSettings m_自定义的Blends）(偏移: 0x68)
- `CameraState m_State`（摄像机状态 m_状态）(偏移: 0x70)
- `float mActivationTime`（float mActivation时间）(偏移: 0x128)
- `float mPendingActivationTime`（float mPendingActivation时间）(偏移: 0x12C)
- `ICinemachineCamera mPendingCamera`（ICinemachine摄像机 mPending摄像机）(偏移: 0x130)
- `CinemachineBlend mActiveBlend`（CinemachineBlend m激活的Blend）(偏移: 0x134)
- `bool mRandomizeNow`（bool mRandomizeNow）(偏移: 0x138)
- `CinemachineVirtualCameraBase[] m_RandomizedChilden`（Cinemachine虚拟的摄像机Base[] m_RandomizedChilden）(偏移: 0x13C)

### 方法 (27)

- `string get_Description()`
  （字符串 获取_描述（））
- `void set_LiveChild(ICinemachineCamera value)`
  （void 设置_活动子级（ICinemachine摄像机 value））
- `ICinemachineCamera get_LiveChild()`
  （ICinemachine摄像机 获取_活动子级（））
- `CameraState get_State()`
  （摄像机状态 get_状态（））
- `bool IsLiveChild(ICinemachineCamera vcam, bool dominantChildOnly = False)`
  （布尔值 是否活动子级（ICinemachine摄像机 vcam, 布尔值 仅主从子级 = 假））
- `Transform get_LookAt()`
  （变换 获取_看向（））
- `void set_LookAt(Transform value)`
  （void 设置_看向（变换 value））
- `Transform get_Follow()`
  （变换 获取_跟随（））
- `void set_Follow(Transform value)`
  （void 设置_跟随（变换 value））
- `void OnTargetObjectWarped(Transform target, Vector3 positionDelta)`
  （void 目标对象扭曲时（变换 target, 三维向量 位置增量））
- `void ForceCameraPosition(Vector3 pos, Quaternion rot)`
  （void 强制摄像机位置（三维向量 pos, 四元数 rot））
- `void InternalUpdateCameraState(Vector3 worldUp, float deltaTime)`
  （void 内部更新摄像机状态（三维向量 worldUp, 浮点数 deltaTime））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `void OnTransformChildrenChanged()`
  （void 变换子级改变时（））
- `void OnGuiHandler()`
  （void GUI处理器（））
- `bool get_IsBlending()`
  （布尔值 获取_是否混合（））
- `CinemachineVirtualCameraBase[] get_ChildCameras()`
  （Cinemachine虚拟摄像机Base[] 获取_子摄像机（））
- `void InvalidateListOfChildren()`
  （void 使无效子级列表（））
- `void ResetRandomization()`
  （void 重置Randomization（））
- `void UpdateListOfChildren()`
  （void 更新列表OfChildren（））
- `ICinemachineCamera ChooseCurrentCamera(Vector3 worldUp)`
  （ICinemachine摄像机 Choose当前摄像机（三维向量 worldUp））
- `CinemachineVirtualCameraBase[] Randomize(CinemachineVirtualCameraBase[] src)`
  （Cinemachine虚拟的摄像机Base[] Randomize（Cinemachine虚拟的摄像机Base[] src））
- `CinemachineBlendDefinition LookupBlend(ICinemachineCamera fromKey, ICinemachineCamera toKey)`
  （CinemachineBlendDefinition LookupBlend（ICinemachine摄像机 fromKey, ICinemachine摄像机 toKey））
- `void OnTransitionFromCamera(ICinemachineCamera fromCam, Vector3 worldUp, float deltaTime)`
  （void 从摄像机过渡时（ICinemachine摄像机 fromCam, 三维向量 worldUp, 浮点数 deltaTime））
- `ICinemachineCamera get_TransitioningFrom()`
  （ICinemachine摄像机 get_TransitioningFrom（））
- `void set_TransitioningFrom(ICinemachineCamera value)`
  （void set_TransitioningFrom（ICinemachine摄像机 value））

---

## CinemachineClearShot.Pair（Cinemachine清除Shot.Pair）

### 字段 (2)

- `int a`（int a）(偏移: 0x0)
- `float b`（float b）(偏移: 0x4)

---

## CinemachineCollider（Cinemachine碰撞器）

**继承**: CinemachineExtension（Cinemachine扩展）

### 字段 (18)

- `LayerMask m_CollideAgainst`（层掩码 m_CollideAgainst）(偏移: 0x14)
- `string m_IgnoreTag`（string m_Ignore标签）(偏移: 0x18)
- `LayerMask m_TransparentLayers`（层掩码 m_透明的Layers）(偏移: 0x1C)
- `float m_MinimumDistanceFromTarget`（float m_Minimum距离From目标）(偏移: 0x20)
- `bool m_AvoidObstacles`（bool m_AvoidObstacles）(偏移: 0x24)
- `float m_DistanceLimit`（float m_距离Limit）(偏移: 0x28)
- `float m_MinimumOcclusionTime`（float m_MinimumOcclusion时间）(偏移: 0x2C)
- `float m_CameraRadius`（float m_摄像机Radius）(偏移: 0x30)
- `CinemachineCollider.ResolutionStrategy m_Strategy`（CinemachineCollider.ResolutionStrategy m_Strategy）(偏移: 0x34)
- `int m_MaximumEffort`（int m_MaximumEffort）(偏移: 0x38)
- `float m_SmoothingTime`（float m_Smoothing时间）(偏移: 0x3C)
- `float m_Damping`（浮点数 m_阻尼）(偏移: 0x40)
- `float m_DampingWhenOccluded`（float m_DampingWhenOccluded）(偏移: 0x44)
- `float m_OptimalTargetDistance`（float m_Optimal目标距离）(偏移: 0x48)
- `RaycastHit[] m_CornerBuffer`（RaycastHit[] m_Corner缓冲区）(偏移: 0x4C)
- `Collider[] mColliderBuffer`（Collider[] m碰撞器缓冲区）(偏移: 0x50)
- `SphereCollider mCameraCollider`（Sphere碰撞器 m摄像机碰撞器）(偏移: 0x0)
- `GameObject mCameraColliderGameObject`（游戏对象 m摄像机碰撞器游戏对象）(偏移: 0x4)

### 方法 (18)

- `bool IsTargetObscured(ICinemachineCamera vcam)`
  （bool 是否目标模糊的（ICinemachine摄像机 vcam））
- `bool CameraWasDisplaced(ICinemachineCamera vcam)`
  （bool 摄像机WasDisplaced（ICinemachine摄像机 vcam））
- `float GetCameraDisplacementDistance(ICinemachineCamera vcam)`
  （float 获取摄像机Displacement距离（ICinemachine摄像机 vcam））
- `void OnValidate()`
  （void 验证时（））
- `void OnDestroy()`
  （void 销毁时（））
- `List<List<Vector3>> get_DebugPaths()`
  （List<List<Vector3>> get_DebugPaths（））
- `float GetMaxDampTime()`
  （浮点数 获取最大阻尼时间（））
- `void PostPipelineStageCallback(CinemachineVirtualCameraBase vcam, CinemachineCore.Stage stage, ref CameraState state, float deltaTime)`
  （void 后管线阶段回调（Cinemachine虚拟摄像机基类 vcam, CinemachineCore.阶段 stage, 引用 CameraState state, 浮点数 deltaTime））
- `Vector3 PreserveLineOfSight(ref CameraState state, ref CinemachineCollider.VcamExtraState extra)`
  （三维向量 PreserveLineOf瞄准镜（ref CameraState state, ref CinemachineCollider.VcamExtraState extra））
- `Vector3 PullCameraInFrontOfNearestObstacle(Vector3 cameraPos, Vector3 lookAtPos, int layerMask, ref RaycastHit hitInfo)`
  （三维向量 Pull摄像机In前OfNearestObstacle（三维向量 cameraPos, 三维向量 lookAtPos, int layerMask, ref RaycastHit hitInfo））
- `Vector3 PushCameraBack(Vector3 currentPos, Vector3 pushDir, RaycastHit obstacle, Vector3 lookAtPos, Plane startPlane, float targetDistance, int iterations, ref CinemachineCollider.VcamExtraState extra)`
  （三维向量 Push摄像机后（三维向量 currentPos, 三维向量 pushDir, Raycast命中 obstacle, 三维向量 lookAtPos, Plane startPlane, float targetDistance, int iterations, ref CinemachineCollider.VcamExtraState extra））
- `bool GetWalkingDirection(Vector3 pos, Vector3 pushDir, RaycastHit obstacle, ref Vector3 outDir)`
  （bool 获取行走方向（三维向量 pos, 三维向量 pushDir, Raycast命中 obstacle, ref Vector3 outDir））
- `float GetPushBackDistance(Ray ray, Plane startPlane, float targetDistance, Vector3 lookAtPos)`
  （float 获取Push后距离（Ray ray, Plane startPlane, float targetDistance, 三维向量 lookAtPos））
- `float ClampRayToBounds(Ray ray, float distance, Bounds bounds)`
  （float ClampRayToBounds（Ray ray, float distance, Bounds bounds））
- `void DestroyCollider()`
  （void 销毁碰撞器（））
- `Vector3 RespectCameraRadius(Vector3 cameraPos, ref CameraState state)`
  （三维向量 Respect摄像机Radius（三维向量 cameraPos, ref CameraState state））
- `bool CheckForTargetObstructions(CameraState state)`
  （bool 检查For目标Obstructions（摄像机状态 state））
- `bool IsTargetOffscreen(CameraState state)`
  （bool 是否目标Offscreen（摄像机状态 state））

---

## CinemachineCollider.ResolutionStrategy（CinemachineCollider.ResolutionStrategy）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineCollider.VcamExtraState（CinemachineCollider.Vcam额外的状态）

### 字段 (8)

- `Vector3 m_previousDisplacement`（三维向量 m_previousDisplacement）(偏移: 0x8)
- `Vector3 m_previousDisplacementCorrection`（三维向量 m_previousDisplacementCorrection）(偏移: 0x14)
- `float colliderDisplacement`（float colliderDisplacement）(偏移: 0x20)
- `bool targetObscured`（bool target模糊的）(偏移: 0x24)
- `float occlusionStartTime`（float occlusion开始时间）(偏移: 0x28)
- `List<Vector3> debugResolutionPath`（List<Vector3> debugResolution路径）(偏移: 0x2C)
- `float m_SmoothedDistance`（float m_Smoothed距离）(偏移: 0x30)
- `float m_SmoothedTime`（float m_Smoothed时间）(偏移: 0x34)

### 方法 (4)

- `void AddPointToDebugPath(Vector3 p)`
  （void 添加PointToDebug路径（三维向量 p））
- `float ApplyDistanceSmoothing(float distance, float smoothingTime)`
  （float 应用距离Smoothing（float distance, float smoothingTime））
- `void UpdateDistanceSmoothing(float distance, float smoothingTime)`
  （void 更新距离Smoothing（float distance, float smoothingTime））
- `void ResetDistanceSmoothing(float smoothingTime)`
  （void 重置距离Smoothing（float smoothingTime））

---

## CinemachineCollisionImpulseSource（CinemachineCollisionImpulseSource）

**继承**: CinemachineImpulseSource（CinemachineImpulseSource）

### 字段 (7)

- `LayerMask m_LayerMask`（层掩码 m_层掩码）(偏移: 0x10)
- `string m_IgnoreTag`（string m_Ignore标签）(偏移: 0x14)
- `bool m_UseImpactDirection`（bool m_UseImpact方向）(偏移: 0x18)
- `bool m_ScaleImpactWithMass`（bool m_缩放ImpactWithMass）(偏移: 0x19)
- `bool m_ScaleImpactWithSpeed`（bool m_缩放ImpactWithSpeed）(偏移: 0x1A)
- `Rigidbody mRigidBody`（刚体 mRigid身体）(偏移: 0x1C)
- `Rigidbody2D mRigidBody2D`（Rigidbody2D mRigidBody2D）(偏移: 0x20)

### 方法 (10)

- `void Start()`
  （void 开始（））
- `void OnEnable()`
  （void 启用时（））
- `void OnCollisionEnter(Collision c)`
  （void OnCollisionEnter（Collision c））
- `void OnTriggerEnter(Collider c)`
  （void On触发器Enter（碰撞器 c））
- `float GetMassAndVelocity(Collider other, ref Vector3 vel)`
  （float 获取MassAnd速度（碰撞器 other, ref Vector3 vel））
- `void GenerateImpactEvent(Collider other, Vector3 vel)`
  （void GenerateImpact事件（碰撞器 other, 三维向量 vel））
- `void OnCollisionEnter2D(Collision2D c)`
  （void OnCollisionEnter2D（Collision2D c））
- `void OnTriggerEnter2D(Collider2D c)`
  （void On触发器Enter2D（Collider2D c））
- `float GetMassAndVelocity2D(Collider2D other2d, ref Vector3 vel)`
  （float 获取MassAndVelocity2D（Collider2D other2d, ref Vector3 vel））
- `void GenerateImpactEvent2D(Collider2D other2d, Vector3 vel)`
  （void GenerateImpactEvent2D（Collider2D other2d, 三维向量 vel））

---

## CinemachineComponentBase（Cinemachine组件基类）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (7)

- `CinemachineVirtualCameraBase m_vcamOwner`（Cinemachine虚拟的摄像机基础 m_vcamOwner）(偏移: 0xC)
- `Transform mCachedFollowTarget`（变换 mCachedFollow目标）(偏移: 0x10)
- `CinemachineVirtualCameraBase mCachedFollowTargetVcam`（Cinemachine虚拟的摄像机基础 mCachedFollow目标Vcam）(偏移: 0x14)
- `ICinemachineTargetGroup mCachedFollowTargetGroup`（ICinemachine目标组 mCachedFollow目标组）(偏移: 0x18)
- `Transform mCachedLookAtTarget`（变换 mCachedLookAt目标）(偏移: 0x1C)
- `CinemachineVirtualCameraBase mCachedLookAtTargetVcam`（Cinemachine虚拟的摄像机基础 mCachedLookAt目标Vcam）(偏移: 0x20)
- `ICinemachineTargetGroup mCachedLookAtTargetGroup`（ICinemachine目标组 mCachedLookAt目标组）(偏移: 0x24)

### 方法 (20)

- `CinemachineVirtualCameraBase get_VirtualCamera()`
  （Cinemachine虚拟的摄像机基础 get_虚拟的摄像机（））
- `Transform get_FollowTarget()`
  （变换 get_Follow目标（））
- `Transform get_LookAtTarget()`
  （变换 get_LookAt目标（））
- `void UpdateFollowTargetCache()`
  （void 更新Follow目标缓存（））
- `ICinemachineTargetGroup get_AbstractFollowTargetGroup()`
  （ICinemachine目标组 get_抽象的Follow目标组（））
- `CinemachineTargetGroup get_FollowTargetGroup()`
  （Cinemachine目标组 get_Follow目标组（））
- `Vector3 get_FollowTargetPosition()`
  （三维向量 get_Follow目标Position（））
- `Quaternion get_FollowTargetRotation()`
  （Quaternion get_Follow目标Rotation（））
- `void UpdateLookAtTargetCache()`
  （void 更新LookAt目标缓存（））
- `ICinemachineTargetGroup get_AbstractLookAtTargetGroup()`
  （ICinemachine目标组 get_抽象的LookAt目标组（））
- `CinemachineTargetGroup get_LookAtTargetGroup()`
  （Cinemachine目标组 get_LookAt目标组（））
- `Vector3 get_LookAtTargetPosition()`
  （三维向量 get_LookAt目标Position（））
- `Quaternion get_LookAtTargetRotation()`
  （Quaternion get_LookAt目标Rotation（））
- `CameraState get_VcamState()`
  （摄像机状态 get_Vcam状态（））
- `void PrePipelineMutateCameraState(ref CameraState curState, float deltaTime)`
  （void PrePipelineMutate摄像机状态（ref CameraState curState, float deltaTime））
- `bool get_BodyAppliesAfterAim()`
  （bool get_身体AppliesAfterAim（））
- `bool OnTransitionFromCamera(ICinemachineCamera fromCam, Vector3 worldUp, float deltaTime, ref CinemachineVirtualCameraBase.TransitionParams transitionParams)`
  （布尔值 从摄像机过渡时（ICinemachine摄像机 fromCam, 三维向量 worldUp, 浮点数 deltaTime, 引用 CinemachineVirtualCameraBase.过渡参数 transitionParams））
- `void OnTargetObjectWarped(Transform target, Vector3 positionDelta)`
  （void 目标对象扭曲时（变换 target, 三维向量 位置增量））
- `void ForceCameraPosition(Vector3 pos, Quaternion rot)`
  （void 强制摄像机位置（三维向量 pos, 四元数 rot））
- `float GetMaxDampTime()`
  （浮点数 获取最大阻尼时间（））

---

## CinemachineComposer（CinemachineComposer）

**继承**: CinemachineComponentBase（Cinemachine组件基类）

### 字段 (21)

- `Vector3 m_TrackedObjectOffset`（三维向量 m_Tracked对象Offset）(偏移: 0x28)
- `float m_LookaheadTime`（float m_Lookahead时间）(偏移: 0x34)
- `float m_LookaheadSmoothing`（float m_LookaheadSmoothing）(偏移: 0x38)
- `bool m_LookaheadIgnoreY`（bool m_LookaheadIgnoreY）(偏移: 0x3C)
- `float m_HorizontalDamping`（float m_水平Damping）(偏移: 0x40)
- `float m_VerticalDamping`（float m_垂直Damping）(偏移: 0x44)
- `float m_ScreenX`（float m_屏幕的X）(偏移: 0x48)
- `float m_ScreenY`（float m_屏幕的Y）(偏移: 0x4C)
- `float m_DeadZoneWidth`（float m_DeadZone宽度）(偏移: 0x50)
- `float m_DeadZoneHeight`（float m_DeadZone高度）(偏移: 0x54)
- `float m_SoftZoneWidth`（float m_SoftZone宽度）(偏移: 0x58)
- `float m_SoftZoneHeight`（float m_SoftZone高度）(偏移: 0x5C)
- `float m_BiasX`（float m_BiasX）(偏移: 0x60)
- `float m_BiasY`（float m_BiasY）(偏移: 0x64)
- `bool m_CenterOnActivate`（bool m_中心On激活）(偏移: 0x68)
- `Vector3 m_CameraPosPrevFrame`（三维向量 m_摄像机PosPrevFrame）(偏移: 0x78)
- `Vector3 m_LookAtPrevFrame`（三维向量 m_LookAtPrevFrame）(偏移: 0x84)
- `Vector2 m_ScreenOffsetPrevFrame`（二维向量 m_屏幕的OffsetPrevFrame）(偏移: 0x90)
- `Quaternion m_CameraOrientationPrevFrame`（Quaternion m_摄像机OrientationPrevFrame）(偏移: 0x98)
- `PositionPredictor m_Predictor`（PositionPredictor m_Predictor）(偏移: 0xA8)
- `CinemachineComposer.FovCache mCache`（CinemachineComposer.Fov缓存 m缓存）(偏移: 0xAC)

### 方法 (16)

- `bool get_IsValid()`
  （布尔值 获取_是否有效（））
- `CinemachineCore.Stage get_Stage()`
  （CinemachineCore.阶段 获取_阶段（））
- `Vector3 get_TrackedPoint()`
  （三维向量 get_TrackedPoint（））
- `void set_TrackedPoint(Vector3 value)`
  （void set_TrackedPoint（三维向量 value））
- `Vector3 GetLookAtPointAndSetTrackedPoint(Vector3 lookAt, Vector3 up, float deltaTime)`
  （三维向量 获取LookAtPointAnd集合TrackedPoint（三维向量 lookAt, 三维向量 up, float deltaTime））
- `void OnTargetObjectWarped(Transform target, Vector3 positionDelta)`
  （void 目标对象扭曲时（变换 target, 三维向量 位置增量））
- `void ForceCameraPosition(Vector3 pos, Quaternion rot)`
  （void 强制摄像机位置（三维向量 pos, 四元数 rot））
- `float GetMaxDampTime()`
  （浮点数 获取最大阻尼时间（））
- `void PrePipelineMutateCameraState(ref CameraState curState, float deltaTime)`
  （void PrePipelineMutate摄像机状态（ref CameraState curState, float deltaTime））
- `void MutateCameraState(ref CameraState curState, float deltaTime)`
  （void 变更摄像机状态（引用 CameraState curState, 浮点数 deltaTime））
- `Rect get_SoftGuideRect()`
  （Rect get_SoftGuideRect（））
- `void set_SoftGuideRect(Rect value)`
  （void set_SoftGuideRect（Rect value））
- `Rect get_HardGuideRect()`
  （Rect get_HardGuideRect（））
- `void set_HardGuideRect(Rect value)`
  （void set_HardGuideRect（Rect value））
- `void RotateToScreenBounds(ref CameraState state, Rect screenRect, Vector3 trackedPoint, ref Quaternion rigOrientation, float fov, float fovH, float deltaTime)`
  （void RotateTo屏幕的Bounds（ref CameraState state, Rect screenRect, 三维向量 trackedPoint, ref Quaternion rigOrientation, float fov, float fovH, float deltaTime））
- `bool ClampVerticalBounds(ref Rect r, Vector3 dir, Vector3 up, float fov)`
  （bool Clamp垂直Bounds（ref Rect r, 三维向量 dir, 三维向量 up, float fov））

---

## CinemachineComposer.FovCache（CinemachineComposer.Fov缓存）

### 字段 (8)

- `Rect mFovSoftGuideRect`（Rect mFovSoftGuideRect）(偏移: 0x0)
- `Rect mFovHardGuideRect`（Rect mFovHardGuideRect）(偏移: 0x10)
- `float mFovH`（float mFovH）(偏移: 0x20)
- `float mFov`（float mFov）(偏移: 0x24)
- `float mOrthoSizeOverDistance`（float mOrtho大小Over距离）(偏移: 0x28)
- `float mAspect`（float mAspect）(偏移: 0x2C)
- `Rect mSoftGuideRect`（Rect mSoftGuideRect）(偏移: 0x30)
- `Rect mHardGuideRect`（Rect mHardGuideRect）(偏移: 0x40)

### 方法 (2)

- `void UpdateCache(LensSettings lens, Rect softGuide, Rect hardGuide, float targetDistance)`
  （void 更新缓存（LensSettings lens, Rect softGuide, Rect hardGuide, float targetDistance））
- `Rect ScreenToFOV(Rect rScreen, float fov, float fovH, float aspect)`
  （Rect 屏幕的To视野（Rect rScreen, float fov, float fovH, float aspect））

---

## CinemachineConfiner（CinemachineConfiner）

**继承**: CinemachineExtension（Cinemachine扩展）

### 字段 (8)

- `CinemachineConfiner.Mode m_ConfineMode`（CinemachineConfiner.模式 m_Confine模式）(偏移: 0x14)
- `Collider m_BoundingVolume`（碰撞器 m_BoundingVolume）(偏移: 0x18)
- `Collider2D m_BoundingShape2D`（Collider2D m_BoundingShape2D）(偏移: 0x1C)
- `Collider2D m_BoundingShape2DCache`（Collider2D m_BoundingShape2D缓存）(偏移: 0x20)
- `bool m_ConfineScreenEdges`（bool m_Confine屏幕的Edges）(偏移: 0x24)
- `float m_Damping`（浮点数 m_阻尼）(偏移: 0x28)
- `List<List<Vector2>> m_pathCache`（List<List<Vector2>> m_path缓存）(偏移: 0x2C)
- `int m_pathTotalPointCount`（int m_pathTotalPoint数量）(偏移: 0x30)

### 方法 (11)

- `bool CameraWasDisplaced(CinemachineVirtualCameraBase vcam)`
  （bool 摄像机WasDisplaced（Cinemachine虚拟的摄像机基础 vcam））
- `float GetCameraDisplacementDistance(CinemachineVirtualCameraBase vcam)`
  （float 获取摄像机Displacement距离（Cinemachine虚拟的摄像机基础 vcam））
- `void OnValidate()`
  （void 验证时（））
- `void ConnectToVcam(bool connect)`
  （void ConnectToVcam（bool connect））
- `bool get_IsValid()`
  （布尔值 获取_是否有效（））
- `float GetMaxDampTime()`
  （浮点数 获取最大阻尼时间（））
- `void PostPipelineStageCallback(CinemachineVirtualCameraBase vcam, CinemachineCore.Stage stage, ref CameraState state, float deltaTime)`
  （void 后管线阶段回调（Cinemachine虚拟摄像机基类 vcam, CinemachineCore.阶段 stage, 引用 CameraState state, 浮点数 deltaTime））
- `void InvalidatePathCache()`
  （void Invalidate路径缓存（））
- `bool ValidatePathCache()`
  （bool 验证路径缓存（））
- `Vector3 ConfinePoint(Vector3 camPos)`
  （三维向量 ConfinePoint（三维向量 camPos））
- `Vector3 ConfineScreenEdges(CinemachineVirtualCameraBase vcam, ref CameraState state)`
  （三维向量 Confine屏幕的Edges（Cinemachine虚拟的摄像机基础 vcam, ref CameraState state））

---

## CinemachineConfiner.Mode（CinemachineConfiner.模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineConfiner.VcamExtraState（CinemachineConfiner.Vcam额外的状态）

### 字段 (2)

- `Vector3 m_previousDisplacement`（三维向量 m_previousDisplacement）(偏移: 0x8)
- `float confinerDisplacement`（float confinerDisplacement）(偏移: 0x14)

---

## CinemachineCore（CinemachineCore）

### 字段 (15)

- `int kStreamingVersion`（int kStreamingVersion）(偏移: 0x0)
- `string kVersionString`（string kVersion字符串）(偏移: 0x4)
- `CinemachineCore sInstance`（CinemachineCore s实例）(偏移: 0x8)
- `bool sShowHiddenObjects`（bool s显示隐藏的Objects）(偏移: 0xC)
- `CinemachineCore.AxisInputDelegate GetInputAxis`（CinemachineCore.轴输入委托 获取输入轴）(偏移: 0x10)
- `float UniformDeltaTimeOverride`（float UniformDelta时间重写）(偏移: 0x14)
- `float CurrentTimeOverride`（float 当前时间重写）(偏移: 0x18)
- `CinemachineCore.GetBlendOverrideDelegate GetBlendOverride`（CinemachineCore.获取Blend重写委托 获取Blend重写）(偏移: 0x1C)
- `CinemachineBrain.BrainEvent CameraUpdatedEvent`（CinemachineBrain.爆头事件 摄像机Updated事件）(偏移: 0x20)
- `CinemachineBrain.BrainEvent CameraCutEvent`（CinemachineBrain.爆头事件 摄像机Cut事件）(偏移: 0x24)
- `List<CinemachineBrain> mActiveBrains`（List<CinemachineBrain> m激活的Brains）(偏移: 0x8)
- `List<CinemachineVirtualCameraBase> mActiveCameras`（List<Cinemachine虚拟的摄像机Base> m激活的Cameras）(偏移: 0xC)
- `List<List<CinemachineVirtualCameraBase>> mAllCameras`（List<List<Cinemachine虚拟的摄像机Base>> m所有Cameras）(偏移: 0x10)
- `CinemachineVirtualCameraBase mRoundRobinVcamLastFrame`（Cinemachine虚拟的摄像机基础 m回合RobinVcam最后一个Frame）(偏移: 0x14)
- `float mLastUpdateTime`（float m最后一个更新时间）(偏移: 0x28)

### 方法 (27)

- `CinemachineCore get_Instance()`
  （CinemachineCore get_实例（））
- `float get_DeltaTime()`
  （float get_Delta时间（））
- `float get_CurrentTime()`
  （float get_当前时间（））
- `int get_BrainCount()`
  （int get_爆头数量（））
- `CinemachineBrain GetActiveBrain(int index)`
  （Cinemachine爆头 获取激活的爆头（int index））
- `void AddActiveBrain(CinemachineBrain brain)`
  （void 添加激活的爆头（Cinemachine爆头 brain））
- `void RemoveActiveBrain(CinemachineBrain brain)`
  （void 移除激活的爆头（Cinemachine爆头 brain））
- `int get_VirtualCameraCount()`
  （int get_虚拟的摄像机数量（））
- `CinemachineVirtualCameraBase GetVirtualCamera(int index)`
  （Cinemachine虚拟的摄像机基础 获取虚拟的摄像机（int index））
- `void AddActiveCamera(CinemachineVirtualCameraBase vcam)`
  （void 添加激活的摄像机（Cinemachine虚拟的摄像机基础 vcam））
- `void RemoveActiveCamera(CinemachineVirtualCameraBase vcam)`
  （void 移除激活的摄像机（Cinemachine虚拟的摄像机基础 vcam））
- `void CameraDestroyed(CinemachineVirtualCameraBase vcam)`
  （void 摄像机Destroyed（Cinemachine虚拟的摄像机基础 vcam））
- `void CameraEnabled(CinemachineVirtualCameraBase vcam)`
  （void 摄像机启用的（Cinemachine虚拟的摄像机基础 vcam））
- `void CameraDisabled(CinemachineVirtualCameraBase vcam)`
  （void 摄像机禁用的（Cinemachine虚拟的摄像机基础 vcam））
- `int get_FixedFrameCount()`
  （int get_固定Frame数量（））
- `void set_FixedFrameCount(int value)`
  （void set_固定Frame数量（int value））
- `void UpdateAllActiveVirtualCameras(int layerMask, Vector3 worldUp, float deltaTime)`
  （void 更新所有激活的虚拟的Cameras（int layerMask, 三维向量 worldUp, float deltaTime））
- `void UpdateVirtualCamera(CinemachineVirtualCameraBase vcam, Vector3 worldUp, float deltaTime)`
  （void 更新虚拟的摄像机（Cinemachine虚拟的摄像机基础 vcam, 三维向量 worldUp, float deltaTime））
- `void InitializeModule()`
  （void 初始化模块（））
- `CinemachineCore.UpdateFilter get_CurrentUpdateFilter()`
  （CinemachineCore.更新Filter get_当前更新Filter（））
- `void set_CurrentUpdateFilter(CinemachineCore.UpdateFilter value)`
  （void set_当前更新Filter（CinemachineCore.更新Filter value））
- `Transform GetUpdateTarget(CinemachineVirtualCameraBase vcam)`
  （变换 获取更新目标（Cinemachine虚拟的摄像机基础 vcam））
- `UpdateTracker.UpdateClock GetVcamUpdateStatus(CinemachineVirtualCameraBase vcam)`
  （更新Tracker.更新时钟 获取Vcam更新Status（Cinemachine虚拟的摄像机基础 vcam））
- `bool IsLive(ICinemachineCamera vcam)`
  （bool 是否Live（ICinemachine摄像机 vcam））
- `void GenerateCameraActivationEvent(ICinemachineCamera vcam, ICinemachineCamera vcamFrom)`
  （void Generate摄像机Activation事件（ICinemachine摄像机 vcam, ICinemachine摄像机 vcamFrom））
- `void GenerateCameraCutEvent(ICinemachineCamera vcam)`
  （void Generate摄像机Cut事件（ICinemachine摄像机 vcam））
- `CinemachineBrain FindPotentialTargetBrain(CinemachineVirtualCameraBase vcam)`
  （Cinemachine爆头 查找Potential目标爆头（Cinemachine虚拟的摄像机基础 vcam））

---

## CinemachineCore.AxisInputDelegate（CinemachineCore.轴输入委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `float Invoke(string axisName)`
  （float Invoke（string axisName））
- `IAsyncResult BeginInvoke(string axisName, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（string axisName, 异步回调 callback, object object））
- `float EndInvoke(IAsyncResult result)`
  （浮点数 结束调用（I异步结果 result））

---

## CinemachineCore.GetBlendOverrideDelegate（CinemachineCore.获取Blend重写委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `CinemachineBlendDefinition Invoke(ICinemachineCamera fromVcam, ICinemachineCamera toVcam, CinemachineBlendDefinition defaultBlend, MonoBehaviour owner)`
  （CinemachineBlendDefinition Invoke（ICinemachine摄像机 fromVcam, ICinemachine摄像机 toVcam, CinemachineBlendDefinition defaultBlend, MonoBehaviour行为 owner））
- `IAsyncResult BeginInvoke(ICinemachineCamera fromVcam, ICinemachineCamera toVcam, CinemachineBlendDefinition defaultBlend, MonoBehaviour owner, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（ICinemachine摄像机 fromVcam, ICinemachine摄像机 toVcam, CinemachineBlendDefinition defaultBlend, MonoBehaviour行为 owner, 异步回调 callback, object object））
- `CinemachineBlendDefinition EndInvoke(IAsyncResult result)`
  （CinemachineBlendDefinition 结束Invoke（I异步Result result））

---

## CinemachineCore.Stage（CinemachineCore.Stage）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineCore.UpdateFilter（CinemachineCore.更新Filter）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineCore.UpdateStatus（CinemachineCore.更新Status）

### 字段 (4)

- `int lastUpdateFrame`（int last更新Frame）(偏移: 0x8)
- `int lastUpdateFixedFrame`（int last更新固定Frame）(偏移: 0xC)
- `UpdateTracker.UpdateClock lastUpdateMode`（更新Tracker.更新时钟 last更新模式）(偏移: 0x10)
- `float lastUpdateDeltaTime`（float last更新Delta时间）(偏移: 0x14)

---

## CinemachineDebug（CinemachineDebug）

### 字段 (3)

- `HashSet<Object> mClients`（HashSet<Object> mClients）(偏移: 0x0)
- `CinemachineDebug.OnGUIDelegate OnGUIHandlers`（CinemachineDebug.OnGUI委托 OnGUIHandlers）(偏移: 0x4)
- `List<StringBuilder> mAvailableStringBuilders`（List<字符串Builder> mAvailable字符串Builders）(偏移: 0x8)

### 方法 (4)

- `void ReleaseScreenPos(Object client)`
  （void Release屏幕的Pos（对象 client））
- `Rect GetScreenPos(Object client, string text, GUIStyle style)`
  （Rect 获取屏幕的Pos（对象 client, string text, GUIStyle style））
- `StringBuilder SBFromPool()`
  （字符串构建器 SBFrom池（））
- `void ReturnToPool(StringBuilder sb)`
  （void ReturnTo池（字符串构建器 sb））

---

## CinemachineDebug.OnGUIDelegate（CinemachineDebug.OnGUI委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke()`
  （void 调用（））
- `IAsyncResult BeginInvoke(AsyncCallback callback, object object)`
  （I异步结果 开始调用（异步回调 callback, 对象 object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## CinemachineDollyCart（CinemachineDollyCart）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (5)

- `CinemachinePathBase m_Path`（Cinemachine路径基础 m_路径）(偏移: 0xC)
- `CinemachineDollyCart.UpdateMethod m_UpdateMethod`（CinemachineDollyCart.更新Method m_更新Method）(偏移: 0x10)
- `CinemachinePathBase.PositionUnits m_PositionUnits`（Cinemachine路径Base.PositionUnits m_PositionUnits）(偏移: 0x14)
- `float m_Speed`（float m_Speed）(偏移: 0x18)
- `float m_Position`（float m_Position）(偏移: 0x1C)

### 方法 (4)

- `void FixedUpdate()`
  （void 固定更新（））
- `void Update()`
  （void 更新（））
- `void LateUpdate()`
  （void 延迟更新（））
- `void SetCartPosition(float distanceAlongPath)`
  （void 集合CartPosition（float distanceAlongPath））

---

## CinemachineDollyCart.UpdateMethod（CinemachineDollyCart.更新Method）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineEmbeddedAssetPropertyAttribute（CinemachineEmbedded资产属性Attribute）

**继承**: PropertyAttribute（属性特性）

### 字段 (1)

- `bool WarnIfNull`（bool WarnIfNull）(偏移: 0x8)

---

## CinemachineExtension（Cinemachine扩展）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (1)

- `CinemachineVirtualCameraBase m_vcamOwner`（Cinemachine虚拟的摄像机基础 m_vcamOwner）(偏移: 0xC)

### 方法 (12)

- `CinemachineVirtualCameraBase get_VirtualCamera()`
  （Cinemachine虚拟的摄像机基础 get_虚拟的摄像机（））
- `void Awake()`
  （void 唤醒（））
- `void OnEnable()`
  （void 启用时（））
- `void OnDestroy()`
  （void 销毁时（））
- `void EnsureStarted()`
  （void EnsureStarted（））
- `void ConnectToVcam(bool connect)`
  （void ConnectToVcam（bool connect））
- `void PrePipelineMutateCameraStateCallback(CinemachineVirtualCameraBase vcam, ref CameraState curState, float deltaTime)`
  （void PrePipelineMutate摄像机状态回调（Cinemachine虚拟的摄像机基础 vcam, ref CameraState curState, float deltaTime））
- `void InvokePostPipelineStageCallback(CinemachineVirtualCameraBase vcam, CinemachineCore.Stage stage, ref CameraState state, float deltaTime)`
  （void InvokePostPipelineStage回调（Cinemachine虚拟的摄像机基础 vcam, CinemachineCore.Stage stage, ref CameraState state, float deltaTime））
- `void OnTargetObjectWarped(Transform target, Vector3 positionDelta)`
  （void 目标对象扭曲时（变换 target, 三维向量 位置增量））
- `void ForceCameraPosition(Vector3 pos, Quaternion rot)`
  （void 强制摄像机位置（三维向量 pos, 四元数 rot））
- `bool OnTransitionFromCamera(ICinemachineCamera fromCam, Vector3 worldUp, float deltaTime)`
  （bool OnTransitionFrom摄像机（ICinemachine摄像机 fromCam, 三维向量 worldUp, float deltaTime））
- `float GetMaxDampTime()`
  （浮点数 获取最大阻尼时间（））

---

## CinemachineExternalCamera（Cinemachine外部的摄像机）

**继承**: CinemachineVirtualCameraBase（Cinemachine虚拟摄像机基类）

### 字段 (4)

- `Transform m_LookAt`（变换 m_看向）(偏移: 0x40)
- `Camera m_Camera`（摄像机 m_摄像机）(偏移: 0x44)
- `CameraState m_State`（摄像机状态 m_状态）(偏移: 0x48)
- `CinemachineVirtualCameraBase.BlendHint m_BlendHint`（Cinemachine虚拟的摄像机Base.BlendHint m_BlendHint）(偏移: 0x104)

### 方法 (6)

- `CameraState get_State()`
  （摄像机状态 get_状态（））
- `Transform get_LookAt()`
  （变换 获取_看向（））
- `void set_LookAt(Transform value)`
  （void 设置_看向（变换 value））
- `Transform get_Follow()`
  （变换 获取_跟随（））
- `void set_Follow(Transform value)`
  （void 设置_跟随（变换 value））
- `void InternalUpdateCameraState(Vector3 worldUp, float deltaTime)`
  （void 内部更新摄像机状态（三维向量 worldUp, 浮点数 deltaTime））

---

## CinemachineFixedSignal（Cinemachine固定信号）

**继承**: SignalSourceAsset（信号Source资产）

### 字段 (3)

- `AnimationCurve m_XCurve`（动画Curve m_XCurve）(偏移: 0xC)
- `AnimationCurve m_YCurve`（动画Curve m_YCurve）(偏移: 0x10)
- `AnimationCurve m_ZCurve`（动画Curve m_ZCurve）(偏移: 0x14)

### 方法 (4)

- `float get_SignalDuration()`
  （float get_信号持续时间（））
- `float AxisDuration(AnimationCurve axis)`
  （float 轴持续时间（动画Curve axis））
- `void GetSignal(float timeSinceSignalStart, out Vector3 pos, out Quaternion rot)`
  （void 获取信号（float timeSinceSignalStart, out Vector3 pos, out Quaternion rot））
- `float AxisValue(AnimationCurve axis, float time)`
  （float 轴值（动画Curve axis, float time））

---

## CinemachineFollowZoom（CinemachineFollow瞄准）

**继承**: CinemachineExtension（Cinemachine扩展）

### 字段 (4)

- `float m_Width`（float m_宽度）(偏移: 0x14)
- `float m_Damping`（浮点数 m_阻尼）(偏移: 0x18)
- `float m_MinFOV`（float m_最小视野）(偏移: 0x1C)
- `float m_MaxFOV`（float m_最大视野）(偏移: 0x20)

### 方法 (3)

- `void OnValidate()`
  （void 验证时（））
- `float GetMaxDampTime()`
  （浮点数 获取最大阻尼时间（））
- `void PostPipelineStageCallback(CinemachineVirtualCameraBase vcam, CinemachineCore.Stage stage, ref CameraState state, float deltaTime)`
  （void 后管线阶段回调（Cinemachine虚拟摄像机基类 vcam, CinemachineCore.阶段 stage, 引用 CameraState state, 浮点数 deltaTime））

---

## CinemachineFollowZoom.VcamExtraState（CinemachineFollowZoom.Vcam额外的状态）

### 字段 (1)

- `float m_previousFrameZoom`（float m_previousFrame瞄准）(偏移: 0x8)

---

## CinemachineFramingTransposer（CinemachineFramingTransposer）

**继承**: CinemachineComponentBase（Cinemachine组件基类）

### 字段 (35)

- `Vector3 m_TrackedObjectOffset`（三维向量 m_Tracked对象Offset）(偏移: 0x28)
- `float m_LookaheadTime`（float m_Lookahead时间）(偏移: 0x34)
- `float m_LookaheadSmoothing`（float m_LookaheadSmoothing）(偏移: 0x38)
- `bool m_LookaheadIgnoreY`（bool m_LookaheadIgnoreY）(偏移: 0x3C)
- `float m_XDamping`（float m_XDamping）(偏移: 0x40)
- `float m_YDamping`（float m_YDamping）(偏移: 0x44)
- `float m_ZDamping`（float m_ZDamping）(偏移: 0x48)
- `bool m_TargetMovementOnly`（bool m_目标MovementOnly）(偏移: 0x4C)
- `float m_ScreenX`（float m_屏幕的X）(偏移: 0x50)
- `float m_ScreenY`（float m_屏幕的Y）(偏移: 0x54)
- `float m_CameraDistance`（float m_摄像机距离）(偏移: 0x58)
- `float m_DeadZoneWidth`（float m_DeadZone宽度）(偏移: 0x5C)
- `float m_DeadZoneHeight`（float m_DeadZone高度）(偏移: 0x60)
- `float m_DeadZoneDepth`（float m_DeadZone深度）(偏移: 0x64)
- `bool m_UnlimitedSoftZone`（bool m_UnlimitedSoftZone）(偏移: 0x68)
- `float m_SoftZoneWidth`（float m_SoftZone宽度）(偏移: 0x6C)
- `float m_SoftZoneHeight`（float m_SoftZone高度）(偏移: 0x70)
- `float m_BiasX`（float m_BiasX）(偏移: 0x74)
- `float m_BiasY`（float m_BiasY）(偏移: 0x78)
- `bool m_CenterOnActivate`（bool m_中心On激活）(偏移: 0x7C)
- `CinemachineFramingTransposer.FramingMode m_GroupFramingMode`（CinemachineFramingTransposer.Framing模式 m_组Framing模式）(偏移: 0x80)
- `CinemachineFramingTransposer.AdjustmentMode m_AdjustmentMode`（CinemachineFramingTransposer.Adjustment模式 m_Adjustment模式）(偏移: 0x84)
- `float m_GroupFramingSize`（float m_组Framing大小）(偏移: 0x88)
- `float m_MaxDollyIn`（float m_最大DollyIn）(偏移: 0x8C)
- `float m_MaxDollyOut`（float m_最大DollyOut）(偏移: 0x90)
- `float m_MinimumDistance`（float m_Minimum距离）(偏移: 0x94)
- `float m_MaximumDistance`（float m_Maximum距离）(偏移: 0x98)
- `float m_MinimumFOV`（float m_Minimum视野）(偏移: 0x9C)
- `float m_MaximumFOV`（float m_Maximum视野）(偏移: 0xA0)
- `float m_MinimumOrthoSize`（float m_MinimumOrtho大小）(偏移: 0xA4)
- `float m_MaximumOrthoSize`（float m_MaximumOrtho大小）(偏移: 0xA8)
- `Vector3 m_PreviousCameraPosition`（三维向量 m_上一个摄像机Position）(偏移: 0xAC)
- `PositionPredictor m_Predictor`（PositionPredictor m_Predictor）(偏移: 0xB8)
- `float m_prevFOV`（float m_prev视野）(偏移: 0xCC)
- `Quaternion m_prevRotation`（Quaternion m_prevRotation）(偏移: 0xD0)

### 方法 (26)

- `Rect get_SoftGuideRect()`
  （Rect get_SoftGuideRect（））
- `void set_SoftGuideRect(Rect value)`
  （void set_SoftGuideRect（Rect value））
- `Rect get_HardGuideRect()`
  （Rect get_HardGuideRect（））
- `void set_HardGuideRect(Rect value)`
  （void set_HardGuideRect（Rect value））
- `void OnValidate()`
  （void 验证时（））
- `bool get_IsValid()`
  （布尔值 获取_是否有效（））
- `CinemachineCore.Stage get_Stage()`
  （CinemachineCore.阶段 获取_阶段（））
- `bool get_BodyAppliesAfterAim()`
  （bool get_身体AppliesAfterAim（））
- `Vector3 get_TrackedPoint()`
  （三维向量 get_TrackedPoint（））
- `void set_TrackedPoint(Vector3 value)`
  （void set_TrackedPoint（三维向量 value））
- `void OnTargetObjectWarped(Transform target, Vector3 positionDelta)`
  （void 目标对象扭曲时（变换 target, 三维向量 位置增量））
- `void ForceCameraPosition(Vector3 pos, Quaternion rot)`
  （void 强制摄像机位置（三维向量 pos, 四元数 rot））
- `float GetMaxDampTime()`
  （浮点数 获取最大阻尼时间（））
- `bool OnTransitionFromCamera(ICinemachineCamera fromCam, Vector3 worldUp, float deltaTime, ref CinemachineVirtualCameraBase.TransitionParams transitionParams)`
  （布尔值 从摄像机过渡时（ICinemachine摄像机 fromCam, 三维向量 worldUp, 浮点数 deltaTime, 引用 CinemachineVirtualCameraBase.过渡参数 transitionParams））
- `bool get_InheritingPosition()`
  （bool get_InheritingPosition（））
- `void set_InheritingPosition(bool value)`
  （void set_InheritingPosition（bool value））
- `Rect ScreenToOrtho(Rect rScreen, float orthoSize, float aspect)`
  （Rect 屏幕的ToOrtho（Rect rScreen, float orthoSize, float aspect））
- `Vector3 OrthoOffsetToScreenBounds(Vector3 targetPos2D, Rect screenRect)`
  （三维向量 OrthoOffsetTo屏幕的Bounds（三维向量 targetPos2D, Rect screenRect））
- `Bounds get_LastBounds()`
  （Bounds get_最后一个Bounds（））
- `void set_LastBounds(Bounds value)`
  （void set_最后一个Bounds（Bounds value））
- `Matrix4x4 get_LastBoundsMatrix()`
  （Matrix4x4 get_最后一个Bounds矩阵（））
- `void set_LastBoundsMatrix(Matrix4x4 value)`
  （void set_最后一个Bounds矩阵（Matrix4x4 value））
- `void MutateCameraState(ref CameraState curState, float deltaTime)`
  （void 变更摄像机状态（引用 CameraState curState, 浮点数 deltaTime））
- `float GetTargetHeight(Vector2 boundsSize)`
  （float 获取目标高度（二维向量 boundsSize））
- `Vector3 ComputeGroupBounds(ICinemachineTargetGroup group, ref CameraState curState)`
  （三维向量 Compute组Bounds（ICinemachine目标组 group, ref CameraState curState））
- `Bounds GetScreenSpaceGroupBoundingBox(ICinemachineTargetGroup group, ref Vector3 pos, Quaternion orientation)`
  （Bounds 获取屏幕的Space组BoundingBox（ICinemachine目标组 group, ref Vector3 pos, Quaternion orientation））

---

## CinemachineFramingTransposer.AdjustmentMode（CinemachineFramingTransposer.Adjustment模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineFramingTransposer.FramingMode（CinemachineFramingTransposer.Framing模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineFreeLook（CinemachineFreeLook）

**继承**: CinemachineVirtualCameraBase（Cinemachine虚拟摄像机基类）

### 字段 (29)

- `Transform m_LookAt`（变换 m_看向）(偏移: 0x40)
- `Transform m_Follow`（变换 m_跟随）(偏移: 0x44)
- `bool m_CommonLens`（bool m_CommonLens）(偏移: 0x48)
- `LensSettings m_Lens`（LensSettings m_Lens）(偏移: 0x4C)
- `CinemachineVirtualCameraBase.TransitionParams m_Transitions`（Cinemachine虚拟的摄像机Base.TransitionParams m_Transitions）(偏移: 0x78)
- `CinemachineVirtualCameraBase.BlendHint m_LegacyBlendHint`（Cinemachine虚拟的摄像机Base.BlendHint m_LegacyBlendHint）(偏移: 0x84)
- `AxisState m_YAxis`（轴状态 m_Y轴）(偏移: 0x88)
- `AxisState.Recentering m_YAxisRecentering`（轴State.Recentering m_Y轴Recentering）(偏移: 0xE8)
- `AxisState m_XAxis`（轴状态 m_X轴）(偏移: 0x104)
- `CinemachineOrbitalTransposer.Heading m_Heading`（CinemachineOrbitalTransposer.Heading m_Heading）(偏移: 0x164)
- `AxisState.Recentering m_RecenterToTargetHeading`（轴State.Recentering m_RecenterTo目标Heading）(偏移: 0x170)
- `CinemachineTransposer.BindingMode m_BindingMode`（CinemachineTransposer.Binding模式 m_Binding模式）(偏移: 0x18C)
- `float m_SplineCurvature`（float m_SplineCurvature）(偏移: 0x190)
- `CinemachineFreeLook.Orbit[] m_Orbits`（CinemachineFreeLook.Orbit[] m_Orbits）(偏移: 0x194)
- `float m_LegacyHeadingBias`（float m_LegacyHeadingBias）(偏移: 0x198)
- `bool mUseLegacyRigDefinitions`（bool mUseLegacyRigDefinitions）(偏移: 0x19C)
- `bool mIsDestroyed`（bool m是否Destroyed）(偏移: 0x19D)
- `CameraState m_State`（摄像机状态 m_状态）(偏移: 0x1A0)
- `CinemachineVirtualCamera[] m_Rigs`（Cinemachine虚拟的Camera[] m_Rigs）(偏移: 0x258)
- `CinemachineOrbitalTransposer[] mOrbitals`（CinemachineOrbitalTransposer[] mOrbitals）(偏移: 0x25C)
- `CinemachineBlend mBlendA`（CinemachineBlend mBlendA）(偏移: 0x260)
- `CinemachineBlend mBlendB`（CinemachineBlend mBlendB）(偏移: 0x264)
- `CinemachineFreeLook.CreateRigDelegate CreateRigOverride`（CinemachineFreeLook.创建Rig委托 创建Rig重写）(偏移: 0x0)
- `CinemachineFreeLook.DestroyRigDelegate DestroyRigOverride`（CinemachineFreeLook.销毁Rig委托 销毁Rig重写）(偏移: 0x4)
- `CinemachineFreeLook.Orbit[] m_CachedOrbits`（CinemachineFreeLook.Orbit[] m_CachedOrbits）(偏移: 0x26C)
- `float m_CachedTension`（float m_CachedTension）(偏移: 0x270)
- `Vector4[] m_CachedKnots`（Vector4[] m_CachedKnots）(偏移: 0x274)
- `Vector4[] m_CachedCtrl1`（Vector4[] m_CachedCtrl1）(偏移: 0x278)
- `Vector4[] m_CachedCtrl2`（Vector4[] m_CachedCtrl2）(偏移: 0x27C)

### 方法 (34)

- `void OnValidate()`
  （void 验证时（））
- `CinemachineVirtualCamera GetRig(int i)`
  （Cinemachine虚拟的摄像机 获取Rig（int i））
- `string[] get_RigNames()`
  （string[] get_RigNames（））
- `void OnEnable()`
  （void 启用时（））
- `void UpdateInputAxisProvider()`
  （void 更新输入轴提供者（））
- `void OnDestroy()`
  （void 销毁时（））
- `void OnTransformChildrenChanged()`
  （void 变换子级改变时（））
- `void Reset()`
  （void 重置（））
- `bool get_PreviousStateIsValid()`
  （bool get_上一个状态是否Valid（））
- `void set_PreviousStateIsValid(bool value)`
  （void set_上一个状态是否Valid（bool value））
- `CameraState get_State()`
  （摄像机状态 get_状态（））
- `Transform get_LookAt()`
  （变换 获取_看向（））
- `void set_LookAt(Transform value)`
  （void 设置_看向（变换 value））
- `Transform get_Follow()`
  （变换 获取_跟随（））
- `void set_Follow(Transform value)`
  （void 设置_跟随（变换 value））
- `bool IsLiveChild(ICinemachineCamera vcam, bool dominantChildOnly = False)`
  （布尔值 是否活动子级（ICinemachine摄像机 vcam, 布尔值 仅主从子级 = 假））
- `void OnTargetObjectWarped(Transform target, Vector3 positionDelta)`
  （void 目标对象扭曲时（变换 target, 三维向量 位置增量））
- `void ForceCameraPosition(Vector3 pos, Quaternion rot)`
  （void 强制摄像机位置（三维向量 pos, 四元数 rot））
- `void InternalUpdateCameraState(Vector3 worldUp, float deltaTime)`
  （void 内部更新摄像机状态（三维向量 worldUp, 浮点数 deltaTime））
- `void OnTransitionFromCamera(ICinemachineCamera fromCam, Vector3 worldUp, float deltaTime)`
  （void 从摄像机过渡时（ICinemachine摄像机 fromCam, 三维向量 worldUp, 浮点数 deltaTime））
- `float GetYAxisClosestValue(Vector3 cameraPos, Vector3 up)`
  （float 获取Y轴Closest值（三维向量 cameraPos, 三维向量 up））
- `void InvalidateRigCache()`
  （void InvalidateRig缓存（））
- `void DestroyRigs()`
  （void 销毁Rigs（））
- `CinemachineVirtualCamera[] CreateRigs(CinemachineVirtualCamera[] copyFrom)`
  （Cinemachine虚拟的Camera[] 创建Rigs（Cinemachine虚拟的Camera[] copyFrom））
- `void UpdateRigCache()`
  （void 更新Rig缓存（））
- `int LocateExistingRigs(string[] rigNames, bool forceOrbital)`
  （int LocateExistingRigs（string[] rigNames, bool forceOrbital））
- `float get_CachedXAxisHeading()`
  （float get_CachedX轴Heading（））
- `void set_CachedXAxisHeading(float value)`
  （void set_CachedX轴Heading（float value））
- `float UpdateXAxisHeading(CinemachineOrbitalTransposer orbital, float deltaTime, Vector3 up)`
  （float 更新X轴Heading（CinemachineOrbitalTransposer orbital, float deltaTime, 三维向量 up））
- `void PushSettingsToRigs()`
  （void PushSettingsToRigs（））
- `float GetYAxisValue()`
  （float 获取Y轴值（））
- `CameraState CalculateNewState(Vector3 worldUp, float deltaTime)`
  （摄像机状态 计算新的状态（三维向量 worldUp, float deltaTime））
- `Vector3 GetLocalPositionForCameraFromInput(float t)`
  （三维向量 获取本地的PositionFor摄像机From输入（float t））
- `void UpdateCachedSpline()`
  （void 更新CachedSpline（））

---

## CinemachineFreeLook.CreateRigDelegate（CinemachineFreeLook.创建Rig委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `CinemachineVirtualCamera Invoke(CinemachineFreeLook vcam, string name, CinemachineVirtualCamera copyFrom)`
  （Cinemachine虚拟的摄像机 Invoke（CinemachineFreeLook vcam, string name, Cinemachine虚拟的摄像机 copyFrom））
- `IAsyncResult BeginInvoke(CinemachineFreeLook vcam, string name, CinemachineVirtualCamera copyFrom, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（CinemachineFreeLook vcam, string name, Cinemachine虚拟的摄像机 copyFrom, 异步回调 callback, object object））
- `CinemachineVirtualCamera EndInvoke(IAsyncResult result)`
  （Cinemachine虚拟的摄像机 结束Invoke（I异步Result result））

---

## CinemachineFreeLook.DestroyRigDelegate（CinemachineFreeLook.销毁Rig委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(GameObject rig)`
  （void Invoke（游戏对象 rig））
- `IAsyncResult BeginInvoke(GameObject rig, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（游戏对象 rig, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## CinemachineFreeLook.Orbit（CinemachineFreeLook.Orbit）

### 字段 (2)

- `float m_Height`（float m_高度）(偏移: 0x0)
- `float m_Radius`（float m_Radius）(偏移: 0x4)

---

## CinemachineGroupComposer（Cinemachine组Composer）

**继承**: CinemachineComposer（CinemachineComposer）

### 字段 (14)

- `float m_GroupFramingSize`（float m_组Framing大小）(偏移: 0xFC)
- `CinemachineGroupComposer.FramingMode m_FramingMode`（Cinemachine组Composer.Framing模式 m_Framing模式）(偏移: 0x100)
- `float m_FrameDamping`（float m_FrameDamping）(偏移: 0x104)
- `CinemachineGroupComposer.AdjustmentMode m_AdjustmentMode`（Cinemachine组Composer.Adjustment模式 m_Adjustment模式）(偏移: 0x108)
- `float m_MaxDollyIn`（float m_最大DollyIn）(偏移: 0x10C)
- `float m_MaxDollyOut`（float m_最大DollyOut）(偏移: 0x110)
- `float m_MinimumDistance`（float m_Minimum距离）(偏移: 0x114)
- `float m_MaximumDistance`（float m_Maximum距离）(偏移: 0x118)
- `float m_MinimumFOV`（float m_Minimum视野）(偏移: 0x11C)
- `float m_MaximumFOV`（float m_Maximum视野）(偏移: 0x120)
- `float m_MinimumOrthoSize`（float m_MinimumOrtho大小）(偏移: 0x124)
- `float m_MaximumOrthoSize`（float m_MaximumOrtho大小）(偏移: 0x128)
- `float m_prevFramingDistance`（float m_prevFraming距离）(偏移: 0x12C)
- `float m_prevFOV`（float m_prev视野）(偏移: 0x130)

### 方法 (9)

- `void OnValidate()`
  （void 验证时（））
- `Bounds get_LastBounds()`
  （Bounds get_最后一个Bounds（））
- `void set_LastBounds(Bounds value)`
  （void set_最后一个Bounds（Bounds value））
- `Matrix4x4 get_LastBoundsMatrix()`
  （Matrix4x4 get_最后一个Bounds矩阵（））
- `void set_LastBoundsMatrix(Matrix4x4 value)`
  （void set_最后一个Bounds矩阵（Matrix4x4 value））
- `float GetMaxDampTime()`
  （浮点数 获取最大阻尼时间（））
- `void MutateCameraState(ref CameraState curState, float deltaTime)`
  （void 变更摄像机状态（引用 CameraState curState, 浮点数 deltaTime））
- `float GetTargetHeight(Vector2 boundsSize)`
  （float 获取目标高度（二维向量 boundsSize））
- `Bounds GetScreenSpaceGroupBoundingBox(ICinemachineTargetGroup group, Matrix4x4 observer, out Vector3 newFwd)`
  （Bounds 获取屏幕的Space组BoundingBox（ICinemachine目标组 group, Matrix4x4 observer, out Vector3 newFwd））

---

## CinemachineGroupComposer.AdjustmentMode（Cinemachine组Composer.Adjustment模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineGroupComposer.FramingMode（Cinemachine组Composer.Framing模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineHardLockToTarget（CinemachineHardLockTo目标）

**继承**: CinemachineComponentBase（Cinemachine组件基类）

### 字段 (2)

- `float m_Damping`（浮点数 m_阻尼）(偏移: 0x28)
- `Vector3 m_PreviousTargetPosition`（三维向量 m_上一个目标Position）(偏移: 0x2C)

### 方法 (4)

- `bool get_IsValid()`
  （布尔值 获取_是否有效（））
- `CinemachineCore.Stage get_Stage()`
  （CinemachineCore.阶段 获取_阶段（））
- `float GetMaxDampTime()`
  （浮点数 获取最大阻尼时间（））
- `void MutateCameraState(ref CameraState curState, float deltaTime)`
  （void 变更摄像机状态（引用 CameraState curState, 浮点数 deltaTime））

---

## CinemachineHardLookAt（CinemachineHardLookAt）

**继承**: CinemachineComponentBase（Cinemachine组件基类）

### 方法 (3)

- `bool get_IsValid()`
  （布尔值 获取_是否有效（））
- `CinemachineCore.Stage get_Stage()`
  （CinemachineCore.阶段 获取_阶段（））
- `void MutateCameraState(ref CameraState curState, float deltaTime)`
  （void 变更摄像机状态（引用 CameraState curState, 浮点数 deltaTime））

---

## CinemachineImpulseDefinition（CinemachineImpulseDefinition）

### 字段 (12)

- `int m_ImpulseChannel`（int m_ImpulseChannel）(偏移: 0x8)
- `SignalSourceAsset m_RawSignal`（信号Source资产 m_Raw信号）(偏移: 0xC)
- `float m_AmplitudeGain`（float m_AmplitudeGain）(偏移: 0x10)
- `float m_FrequencyGain`（float m_FrequencyGain）(偏移: 0x14)
- `CinemachineImpulseDefinition.RepeatMode m_RepeatMode`（CinemachineImpulseDefinition.Repeat模式 m_Repeat模式）(偏移: 0x18)
- `bool m_Randomize`（bool m_Randomize）(偏移: 0x1C)
- `CinemachineImpulseManager.EnvelopeDefinition m_TimeEnvelope`（CinemachineImpulseManager.EnvelopeDefinition m_时间Envelope）(偏移: 0x20)
- `float m_ImpactRadius`（float m_ImpactRadius）(偏移: 0x38)
- `CinemachineImpulseManager.ImpulseEvent.DirectionMode m_DirectionMode`（CinemachineImpulseManager.ImpulseEvent.方向模式 m_方向模式）(偏移: 0x3C)
- `CinemachineImpulseManager.ImpulseEvent.DissipationMode m_DissipationMode`（CinemachineImpulseManager.ImpulseEvent.Dissipation模式 m_Dissipation模式）(偏移: 0x40)
- `float m_DissipationDistance`（float m_Dissipation距离）(偏移: 0x44)
- `float m_PropagationSpeed`（float m_PropagationSpeed）(偏移: 0x48)

### 方法 (3)

- `void OnValidate()`
  （void 验证时（））
- `void CreateEvent(Vector3 position, Vector3 velocity)`
  （void 创建事件（三维向量 position, 三维向量 velocity））
- `CinemachineImpulseManager.ImpulseEvent CreateAndReturnEvent(Vector3 position, Vector3 velocity)`
  （CinemachineImpulseManager.Impulse事件 创建AndReturn事件（三维向量 position, 三维向量 velocity））

---

## CinemachineImpulseDefinition.RepeatMode（CinemachineImpulseDefinition.Repeat模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineImpulseDefinition.SignalSource（CinemachineImpulseDefinition.信号Source）

**继承**: ISignalSource6D（I信号Source6D）

### 字段 (3)

- `CinemachineImpulseDefinition m_Def`（CinemachineImpulseDefinition m_Def）(偏移: 0x8)
- `Vector3 m_Velocity`（三维向量 m_速度）(偏移: 0xC)
- `float m_StartTimeOffset`（float m_开始时间Offset）(偏移: 0x18)

### 方法 (2)

- `float get_SignalDuration()`
  （float get_信号持续时间（））
- `void GetSignal(float timeSinceSignalStart, out Vector3 pos, out Quaternion rot)`
  （void 获取信号（float timeSinceSignalStart, out Vector3 pos, out Quaternion rot））

---

## CinemachineImpulseListener（CinemachineImpulse监听器）

**继承**: CinemachineExtension（Cinemachine扩展）

### 字段 (3)

- `int m_ChannelMask`（int m_Channel掩码）(偏移: 0x14)
- `float m_Gain`（float m_Gain）(偏移: 0x18)
- `bool m_Use2DDistance`（bool m_Use2D距离）(偏移: 0x1C)

### 方法 (1)

- `void PostPipelineStageCallback(CinemachineVirtualCameraBase vcam, CinemachineCore.Stage stage, ref CameraState state, float deltaTime)`
  （void 后管线阶段回调（Cinemachine虚拟摄像机基类 vcam, CinemachineCore.阶段 stage, 引用 CameraState state, 浮点数 deltaTime））

---

## CinemachineImpulseManager（CinemachineImpulse管理器）

### 字段 (3)

- `CinemachineImpulseManager sInstance`（CinemachineImpulse管理器 s实例）(偏移: 0x0)
- `List<CinemachineImpulseManager.ImpulseEvent> m_ExpiredEvents`（List<CinemachineImpulseManager.ImpulseEvent> m_ExpiredEvents）(偏移: 0x8)
- `List<CinemachineImpulseManager.ImpulseEvent> m_ActiveEvents`（List<CinemachineImpulseManager.ImpulseEvent> m_激活的Events）(偏移: 0xC)

### 方法 (9)

- `CinemachineImpulseManager get_Instance()`
  （CinemachineImpulse管理器 get_实例（））
- `void InitializeModule()`
  （void 初始化模块（））
- `bool GetImpulseAt(Vector3 listenerLocation, bool distance2D, int channelMask, out Vector3 pos, out Quaternion rot)`
  （bool 获取ImpulseAt（三维向量 listenerLocation, bool distance2D, int channelMask, out Vector3 pos, out Quaternion rot））
- `bool get_IgnoreTimeScale()`
  （bool get_Ignore时间缩放（））
- `void set_IgnoreTimeScale(bool value)`
  （void set_Ignore时间缩放（bool value））
- `float get_CurrentTime()`
  （float get_当前时间（））
- `CinemachineImpulseManager.ImpulseEvent NewImpulseEvent()`
  （CinemachineImpulseManager.Impulse事件 新的Impulse事件（））
- `void AddImpulseEvent(CinemachineImpulseManager.ImpulseEvent e)`
  （void 添加Impulse事件（CinemachineImpulseManager.Impulse事件 e））
- `void Clear()`
  （void 清除（））

---

## CinemachineImpulseManager.EnvelopeDefinition（CinemachineImpulseManager.EnvelopeDefinition）

### 字段 (7)

- `AnimationCurve m_AttackShape`（动画Curve m_AttackShape）(偏移: 0x0)
- `AnimationCurve m_DecayShape`（动画Curve m_衰减Shape）(偏移: 0x4)
- `float m_AttackTime`（float m_Attack时间）(偏移: 0x8)
- `float m_SustainTime`（float m_Sustain时间）(偏移: 0xC)
- `float m_DecayTime`（float m_衰减时间）(偏移: 0x10)
- `bool m_ScaleWithImpact`（bool m_缩放WithImpact）(偏移: 0x14)
- `bool m_HoldForever`（bool m_HoldForever）(偏移: 0x15)

### 方法 (6)

- `CinemachineImpulseManager.EnvelopeDefinition Default()`
  （CinemachineImpulseManager.EnvelopeDefinition 默认的（））
- `float get_Duration()`
  （float get_持续时间（））
- `float GetValueAt(float offset)`
  （float 获取值At（float offset））
- `void ChangeStopTime(float offset, bool forceNoDecay)`
  （void Change停止时间（float offset, bool forceNoDecay））
- `void Clear()`
  （void 清除（））
- `void Validate()`
  （void 验证（））

---

## CinemachineImpulseManager.ImpulseEvent（CinemachineImpulseManager.Impulse事件）

### 字段 (10)

- `float m_StartTime`（float m_开始时间）(偏移: 0x8)
- `CinemachineImpulseManager.EnvelopeDefinition m_Envelope`（CinemachineImpulseManager.EnvelopeDefinition m_Envelope）(偏移: 0xC)
- `ISignalSource6D m_SignalSource`（I信号Source6D m_信号Source）(偏移: 0x24)
- `Vector3 m_Position`（三维向量 m_位置）(偏移: 0x28)
- `float m_Radius`（float m_Radius）(偏移: 0x34)
- `CinemachineImpulseManager.ImpulseEvent.DirectionMode m_DirectionMode`（CinemachineImpulseManager.ImpulseEvent.方向模式 m_方向模式）(偏移: 0x38)
- `int m_Channel`（int m_Channel）(偏移: 0x3C)
- `CinemachineImpulseManager.ImpulseEvent.DissipationMode m_DissipationMode`（CinemachineImpulseManager.ImpulseEvent.Dissipation模式 m_Dissipation模式）(偏移: 0x40)
- `float m_DissipationDistance`（float m_Dissipation距离）(偏移: 0x44)
- `float m_PropagationSpeed`（float m_PropagationSpeed）(偏移: 0x48)

### 方法 (5)

- `bool get_Expired()`
  （bool get_Expired（））
- `void Cancel(float time, bool forceNoDecay)`
  （void 取消（float time, bool forceNoDecay））
- `float DistanceDecay(float distance)`
  （float 距离衰减（float distance））
- `bool GetDecayedSignal(Vector3 listenerPosition, bool use2D, out Vector3 pos, out Quaternion rot)`
  （bool 获取Decayed信号（三维向量 listenerPosition, bool use2D, out Vector3 pos, out Quaternion rot））
- `void Clear()`
  （void 清除（））

---

## CinemachineImpulseManager.ImpulseEvent.DirectionMode（CinemachineImpulseManager.ImpulseEvent.方向模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineImpulseManager.ImpulseEvent.DissipationMode（CinemachineImpulseManager.ImpulseEvent.Dissipation模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineImpulseSource（CinemachineImpulseSource）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (1)

- `CinemachineImpulseDefinition m_ImpulseDefinition`（CinemachineImpulseDefinition m_ImpulseDefinition）(偏移: 0xC)

### 方法 (5)

- `void OnValidate()`
  （void 验证时（））
- `void GenerateImpulseAt(Vector3 position, Vector3 velocity)`
  （void GenerateImpulseAt（三维向量 position, 三维向量 velocity））
- `void GenerateImpulse(Vector3 velocity)`
  （void GenerateImpulse（三维向量 velocity））
- `void GenerateImpulse(float force)`
  （void GenerateImpulse（float force））
- `void GenerateImpulse()`
  （void GenerateImpulse（））

---

## CinemachineIndependentImpulseListener（CinemachineIndependentImpulse监听器）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (5)

- `Vector3 impulsePosLastFrame`（三维向量 impulsePos最后一个Frame）(偏移: 0xC)
- `Quaternion impulseRotLastFrame`（Quaternion impulseRot最后一个Frame）(偏移: 0x18)
- `int m_ChannelMask`（int m_Channel掩码）(偏移: 0x28)
- `float m_Gain`（float m_Gain）(偏移: 0x2C)
- `bool m_Use2DDistance`（bool m_Use2D距离）(偏移: 0x30)

### 方法 (4)

- `void Reset()`
  （void 重置（））
- `void OnEnable()`
  （void 启用时（））
- `void Update()`
  （void 更新（））
- `void LateUpdate()`
  （void 延迟更新（））

---

## CinemachineInputAxisDriver（Cinemachine输入轴Driver）

### 字段 (6)

- `float multiplier`（float multiplier）(偏移: 0x0)
- `float accelTime`（float accel时间）(偏移: 0x4)
- `float decelTime`（float decel时间）(偏移: 0x8)
- `string name`（字符串 名称）(偏移: 0xC)
- `float inputValue`（float input值）(偏移: 0x10)
- `float mCurrentSpeed`（float m当前Speed）(偏移: 0x14)

### 方法 (4)

- `void Validate()`
  （void 验证（））
- `bool Update(float deltaTime, ref AxisBase axis)`
  （bool 更新（float deltaTime, ref AxisBase axis））
- `float ClampValue(ref AxisBase axis, float v)`
  （float Clamp值（ref AxisBase axis, float v））
- `bool Update(float deltaTime, ref AxisState axis)`
  （bool 更新（float deltaTime, ref AxisState axis））

---

## CinemachineMixer（CinemachineMixer）

**继承**: PlayableBehaviour（可播放行为）

### 字段 (4)

- `CinemachineMixer.MasterDirectorDelegate GetMasterPlayableDirector`（CinemachineMixer.MasterDirector委托 获取MasterPlayableDirector）(偏移: 0x0)
- `CinemachineBrain mBrain`（Cinemachine爆头 m爆头）(偏移: 0x8)
- `int mBrainOverrideId`（int m爆头重写Id）(偏移: 0xC)
- `bool mPreviewPlay`（bool mPreview播放）(偏移: 0x10)

### 方法 (4)

- `void OnPlayableDestroy(Playable playable)`
  （void OnPlayable销毁（Playable playable））
- `void PrepareFrame(Playable playable, FrameData info)`
  （void 准备帧（可播放 playable, 帧数据 info））
- `void ProcessFrame(Playable playable, FrameData info, object playerData)`
  （void 处理Frame（Playable playable, Frame数据 info, object playerData））
- `float GetDeltaTime(float deltaTime)`
  （float 获取Delta时间（float deltaTime））

---

## CinemachineMixer.MasterDirectorDelegate（CinemachineMixer.MasterDirector委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `PlayableDirector Invoke()`
  （PlayableDirector Invoke（））
- `IAsyncResult BeginInvoke(AsyncCallback callback, object object)`
  （I异步结果 开始调用（异步回调 callback, 对象 object））
- `PlayableDirector EndInvoke(IAsyncResult result)`
  （PlayableDirector 结束Invoke（I异步Result result））

---

## CinemachineMixingCamera（CinemachineMixing摄像机）

**继承**: CinemachineVirtualCameraBase（Cinemachine虚拟摄像机基类）

### 字段 (10)

- `float m_Weight0`（float m_Weight0）(偏移: 0x40)
- `float m_Weight1`（float m_Weight1）(偏移: 0x44)
- `float m_Weight2`（float m_Weight2）(偏移: 0x48)
- `float m_Weight3`（float m_Weight3）(偏移: 0x4C)
- `float m_Weight4`（float m_Weight4）(偏移: 0x50)
- `float m_Weight5`（float m_Weight5）(偏移: 0x54)
- `float m_Weight6`（float m_Weight6）(偏移: 0x58)
- `float m_Weight7`（float m_Weight7）(偏移: 0x5C)
- `CameraState m_State`（摄像机状态 m_状态）(偏移: 0x60)
- `CinemachineVirtualCameraBase[] m_ChildCameras`（Cinemachine虚拟摄像机Base[] m_子摄像机）(偏移: 0x124)

### 方法 (22)

- `float GetWeight(int index)`
  （float 获取Weight（int index））
- `void SetWeight(int index, float w)`
  （void 集合Weight（int index, float w））
- `float GetWeight(CinemachineVirtualCameraBase vcam)`
  （float 获取Weight（Cinemachine虚拟的摄像机基础 vcam））
- `void SetWeight(CinemachineVirtualCameraBase vcam, float w)`
  （void 集合Weight（Cinemachine虚拟的摄像机基础 vcam, float w））
- `void set_LiveChild(ICinemachineCamera value)`
  （void 设置_活动子级（ICinemachine摄像机 value））
- `ICinemachineCamera get_LiveChild()`
  （ICinemachine摄像机 获取_活动子级（））
- `CameraState get_State()`
  （摄像机状态 get_状态（））
- `Transform get_LookAt()`
  （变换 获取_看向（））
- `void set_LookAt(Transform value)`
  （void 设置_看向（变换 value））
- `Transform get_Follow()`
  （变换 获取_跟随（））
- `void set_Follow(Transform value)`
  （void 设置_跟随（变换 value））
- `void OnTargetObjectWarped(Transform target, Vector3 positionDelta)`
  （void 目标对象扭曲时（变换 target, 三维向量 位置增量））
- `void ForceCameraPosition(Vector3 pos, Quaternion rot)`
  （void 强制摄像机位置（三维向量 pos, 四元数 rot））
- `void OnEnable()`
  （void 启用时（））
- `void OnTransformChildrenChanged()`
  （void 变换子级改变时（））
- `void OnValidate()`
  （void 验证时（））
- `bool IsLiveChild(ICinemachineCamera vcam, bool dominantChildOnly = False)`
  （布尔值 是否活动子级（ICinemachine摄像机 vcam, 布尔值 仅主从子级 = 假））
- `CinemachineVirtualCameraBase[] get_ChildCameras()`
  （Cinemachine虚拟摄像机Base[] 获取_子摄像机（））
- `void InvalidateListOfChildren()`
  （void 使无效子级列表（））
- `void ValidateListOfChildren()`
  （void 验证列表OfChildren（））
- `void OnTransitionFromCamera(ICinemachineCamera fromCam, Vector3 worldUp, float deltaTime)`
  （void 从摄像机过渡时（ICinemachine摄像机 fromCam, 三维向量 worldUp, 浮点数 deltaTime））
- `void InternalUpdateCameraState(Vector3 worldUp, float deltaTime)`
  （void 内部更新摄像机状态（三维向量 worldUp, 浮点数 deltaTime））

---

## CinemachineOrbitalTransposer（CinemachineOrbitalTransposer）

**继承**: CinemachineTransposer（CinemachineTransposer）

### 字段 (12)

- `CinemachineOrbitalTransposer.Heading m_Heading`（CinemachineOrbitalTransposer.Heading m_Heading）(偏移: 0x98)
- `AxisState.Recentering m_RecenterToTargetHeading`（轴State.Recentering m_RecenterTo目标Heading）(偏移: 0xA4)
- `AxisState m_XAxis`（轴状态 m_X轴）(偏移: 0xC0)
- `float m_LegacyRadius`（float m_LegacyRadius）(偏移: 0x120)
- `float m_LegacyHeightOffset`（float m_Legacy高度Offset）(偏移: 0x124)
- `float m_LegacyHeadingBias`（float m_LegacyHeadingBias）(偏移: 0x128)
- `bool m_HeadingIsSlave`（bool m_Heading是否Slave）(偏移: 0x12C)
- `CinemachineOrbitalTransposer.UpdateHeadingDelegate HeadingUpdater`（CinemachineOrbitalTransposer.更新Heading委托 HeadingUpdater）(偏移: 0x130)
- `Vector3 mLastTargetPosition`（三维向量 m最后一个目标Position）(偏移: 0x134)
- `HeadingTracker mHeadingTracker`（HeadingTracker mHeadingTracker）(偏移: 0x140)
- `Rigidbody mTargetRigidBody`（刚体 m目标Rigid身体）(偏移: 0x144)
- `Vector3 mLastCameraPosition`（三维向量 m最后一个摄像机Position）(偏移: 0x14C)

### 方法 (16)

- `void OnValidate()`
  （void 验证时（））
- `float UpdateHeading(float deltaTime, Vector3 up, ref AxisState axis)`
  （float 更新Heading（float deltaTime, 三维向量 up, ref AxisState axis））
- `float UpdateHeading(float deltaTime, Vector3 up, ref AxisState axis, ref AxisState.Recentering recentering, bool isLive)`
  （float 更新Heading（float deltaTime, 三维向量 up, ref AxisState axis, ref AxisState.Recentering recentering, bool isLive））
- `void OnEnable()`
  （void 启用时（））
- `void UpdateInputAxisProvider()`
  （void 更新输入轴提供者（））
- `Transform get_PreviousTarget()`
  （变换 get_上一个目标（））
- `void set_PreviousTarget(Transform value)`
  （void set_上一个目标（变换 value））
- `void OnTargetObjectWarped(Transform target, Vector3 positionDelta)`
  （void 目标对象扭曲时（变换 target, 三维向量 位置增量））
- `void ForceCameraPosition(Vector3 pos, Quaternion rot)`
  （void 强制摄像机位置（三维向量 pos, 四元数 rot））
- `bool OnTransitionFromCamera(ICinemachineCamera fromCam, Vector3 worldUp, float deltaTime, ref CinemachineVirtualCameraBase.TransitionParams transitionParams)`
  （布尔值 从摄像机过渡时（ICinemachine摄像机 fromCam, 三维向量 worldUp, 浮点数 deltaTime, 引用 CinemachineVirtualCameraBase.过渡参数 transitionParams））
- `float GetAxisClosestValue(Vector3 cameraPos, Vector3 up)`
  （float 获取轴Closest值（三维向量 cameraPos, 三维向量 up））
- `float get_LastHeading()`
  （float get_最后一个Heading（））
- `void set_LastHeading(float value)`
  （void set_最后一个Heading（float value））
- `void MutateCameraState(ref CameraState curState, float deltaTime)`
  （void 变更摄像机状态（引用 CameraState curState, 浮点数 deltaTime））
- `Vector3 GetTargetCameraPosition(Vector3 worldUp)`
  （三维向量 获取目标摄像机Position（三维向量 worldUp））
- `float GetTargetHeading(float currentHeading, Quaternion targetOrientation)`
  （float 获取目标Heading（float currentHeading, Quaternion targetOrientation））

---

## CinemachineOrbitalTransposer.Heading（CinemachineOrbitalTransposer.Heading）

### 字段 (3)

- `CinemachineOrbitalTransposer.Heading.HeadingDefinition m_Definition`（CinemachineOrbitalTransposer.Heading.HeadingDefinition m_Definition）(偏移: 0x0)
- `int m_VelocityFilterStrength`（int m_速度FilterStrength）(偏移: 0x4)
- `float m_Bias`（float m_Bias）(偏移: 0x8)

---

## CinemachineOrbitalTransposer.Heading.HeadingDefinition（CinemachineOrbitalTransposer.Heading.HeadingDefinition）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineOrbitalTransposer.UpdateHeadingDelegate（CinemachineOrbitalTransposer.更新Heading委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `float Invoke(CinemachineOrbitalTransposer orbital, float deltaTime, Vector3 up)`
  （float Invoke（CinemachineOrbitalTransposer orbital, float deltaTime, 三维向量 up））
- `IAsyncResult BeginInvoke(CinemachineOrbitalTransposer orbital, float deltaTime, Vector3 up, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（CinemachineOrbitalTransposer orbital, float deltaTime, 三维向量 up, 异步回调 callback, object object））
- `float EndInvoke(IAsyncResult result)`
  （浮点数 结束调用（I异步结果 result））

---

## CinemachinePOV（CinemachinePOV）

**继承**: CinemachineComponentBase（Cinemachine组件基类）

### 字段 (6)

- `CinemachinePOV.RecenterTargetMode m_RecenterTarget`（CinemachinePOV.Recenter目标模式 m_Recenter目标）(偏移: 0x28)
- `AxisState m_VerticalAxis`（轴状态 m_垂直轴）(偏移: 0x2C)
- `AxisState.Recentering m_VerticalRecentering`（轴State.Recentering m_垂直Recentering）(偏移: 0x8C)
- `AxisState m_HorizontalAxis`（轴状态 m_水平轴）(偏移: 0xA8)
- `AxisState.Recentering m_HorizontalRecentering`（轴State.Recentering m_水平Recentering）(偏移: 0x108)
- `bool m_ApplyBeforeBody`（bool m_应用Before身体）(偏移: 0x124)

### 方法 (12)

- `bool get_IsValid()`
  （布尔值 获取_是否有效（））
- `CinemachineCore.Stage get_Stage()`
  （CinemachineCore.阶段 获取_阶段（））
- `void OnValidate()`
  （void 验证时（））
- `void OnEnable()`
  （void 启用时（））
- `void UpdateInputAxisProvider()`
  （void 更新输入轴提供者（））
- `void PrePipelineMutateCameraState(ref CameraState state, float deltaTime)`
  （void PrePipelineMutate摄像机状态（ref CameraState state, float deltaTime））
- `void MutateCameraState(ref CameraState curState, float deltaTime)`
  （void 变更摄像机状态（引用 CameraState curState, 浮点数 deltaTime））
- `Vector2 GetRecenterTarget()`
  （二维向量 获取Recenter目标（））
- `float NormalizeAngle(float angle)`
  （float Normalize角度（float angle））
- `void ForceCameraPosition(Vector3 pos, Quaternion rot)`
  （void 强制摄像机位置（三维向量 pos, 四元数 rot））
- `bool OnTransitionFromCamera(ICinemachineCamera fromCam, Vector3 worldUp, float deltaTime, ref CinemachineVirtualCameraBase.TransitionParams transitionParams)`
  （布尔值 从摄像机过渡时（ICinemachine摄像机 fromCam, 三维向量 worldUp, 浮点数 deltaTime, 引用 CinemachineVirtualCameraBase.过渡参数 transitionParams））
- `void SetAxesForRotation(Quaternion targetRot)`
  （void 集合AxesForRotation（Quaternion targetRot））

---

## CinemachinePOV.RecenterTargetMode（CinemachinePOV.Recenter目标模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachinePath（Cinemachine路径）

**继承**: CinemachinePathBase（Cinemachine路径基础）

### 字段 (2)

- `bool m_Looped`（bool m_Looped）(偏移: 0x2C)
- `CinemachinePath.Waypoint[] m_Waypoints`（CinemachinePath.Waypoint[] m_Waypoints）(偏移: 0x30)

### 方法 (10)

- `float get_MinPos()`
  （float get_最小Pos（））
- `float get_MaxPos()`
  （float get_最大Pos（））
- `bool get_Looped()`
  （bool get_Looped（））
- `void Reset()`
  （void 重置（））
- `int get_DistanceCacheSampleStepsPerSegment()`
  （int get_距离缓存SampleStepsPerSegment（））
- `float GetBoundingIndices(float pos, out int indexA, out int indexB)`
  （float 获取BoundingIndices（float pos, out int indexA, out int indexB））
- `Vector3 EvaluatePosition(float pos)`
  （三维向量 EvaluatePosition（float pos））
- `Vector3 EvaluateTangent(float pos)`
  （三维向量 EvaluateTangent（float pos））
- `Quaternion EvaluateOrientation(float pos)`
  （Quaternion EvaluateOrientation（float pos））
- `void OnValidate()`
  （void 验证时（））

---

## CinemachinePath.Waypoint（CinemachinePath.Waypoint）

### 字段 (3)

- `Vector3 position`（三维向量 位置）(偏移: 0x0)
- `Vector3 tangent`（三维向量 tangent）(偏移: 0xC)
- `float roll`（float roll）(偏移: 0x18)

---

## CinemachinePathBase（Cinemachine路径基础）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (8)

- `int m_Resolution`（int m_Resolution）(偏移: 0xC)
- `CinemachinePathBase.Appearance m_Appearance`（Cinemachine路径Base.Appearance m_Appearance）(偏移: 0x10)
- `float[] m_DistanceToPos`（float[] m_距离ToPos）(偏移: 0x14)
- `float[] m_PosToDistance`（float[] m_PosTo距离）(偏移: 0x18)
- `int m_CachedSampleSteps`（int m_CachedSampleSteps）(偏移: 0x1C)
- `float m_PathLength`（float m_路径Length）(偏移: 0x20)
- `float m_cachedPosStepSize`（float m_cachedPosStep大小）(偏移: 0x24)
- `float m_cachedDistanceStepSize`（float m_cached距离Step大小）(偏移: 0x28)

### 方法 (15)

- `float StandardizePos(float pos)`
  （float StandardizePos（float pos））
- `float FindClosestPoint(Vector3 p, int startSegment, int searchRadius, int stepsPerSegment)`
  （float 查找ClosestPoint（三维向量 p, int startSegment, int searchRadius, int stepsPerSegment））
- `float MinUnit(CinemachinePathBase.PositionUnits units)`
  （float 最小Unit（Cinemachine路径Base.PositionUnits units））
- `float MaxUnit(CinemachinePathBase.PositionUnits units)`
  （float 最大Unit（Cinemachine路径Base.PositionUnits units））
- `float StandardizeUnit(float pos, CinemachinePathBase.PositionUnits units)`
  （float StandardizeUnit（float pos, Cinemachine路径Base.PositionUnits units））
- `Vector3 EvaluatePositionAtUnit(float pos, CinemachinePathBase.PositionUnits units)`
  （三维向量 EvaluatePositionAtUnit（float pos, Cinemachine路径Base.PositionUnits units））
- `Vector3 EvaluateTangentAtUnit(float pos, CinemachinePathBase.PositionUnits units)`
  （三维向量 EvaluateTangentAtUnit（float pos, Cinemachine路径Base.PositionUnits units））
- `Quaternion EvaluateOrientationAtUnit(float pos, CinemachinePathBase.PositionUnits units)`
  （Quaternion EvaluateOrientationAtUnit（float pos, Cinemachine路径Base.PositionUnits units））
- `void InvalidateDistanceCache()`
  （void Invalidate距离缓存（））
- `bool DistanceCacheIsValid()`
  （bool 距离缓存是否Valid（））
- `float get_PathLength()`
  （float get_路径Length（））
- `float StandardizePathDistance(float distance)`
  （float Standardize路径距离（float distance））
- `float ToNativePathUnits(float pos, CinemachinePathBase.PositionUnits units)`
  （float ToNative路径Units（float pos, Cinemachine路径Base.PositionUnits units））
- `float FromPathNativeUnits(float pos, CinemachinePathBase.PositionUnits units)`
  （float From路径NativeUnits（float pos, Cinemachine路径Base.PositionUnits units））
- `void ResamplePath(int stepsPerSegment)`
  （void Resample路径（int stepsPerSegment））

---

## CinemachinePathBase.Appearance（Cinemachine路径Base.Appearance）

### 字段 (3)

- `Color pathColor`（颜色 path颜色）(偏移: 0x8)
- `Color inactivePathColor`（颜色 inactive路径颜色）(偏移: 0x18)
- `float width`（浮点数 宽度）(偏移: 0x28)

---

## CinemachinePathBase.PositionUnits（Cinemachine路径Base.PositionUnits）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachinePixelPerfect（CinemachinePixelPerfect）

**继承**: CinemachineExtension（Cinemachine扩展）

### 方法 (1)

- `void PostPipelineStageCallback(CinemachineVirtualCameraBase vcam, CinemachineCore.Stage stage, ref CameraState state, float deltaTime)`
  （void 后管线阶段回调（Cinemachine虚拟摄像机基类 vcam, CinemachineCore.阶段 stage, 引用 CameraState state, 浮点数 deltaTime））

---

## CinemachinePostProcessing（CinemachinePostProcessing）

**继承**: CinemachineExtension（Cinemachine扩展）

### 方法 (1)

- `void PostPipelineStageCallback(CinemachineVirtualCameraBase vcam, CinemachineCore.Stage stage, ref CameraState state, float deltaTime)`
  （void 后管线阶段回调（Cinemachine虚拟摄像机基类 vcam, CinemachineCore.阶段 stage, 引用 CameraState state, 浮点数 deltaTime））

---

## CinemachineRecomposer（CinemachineRecomposer）

**继承**: CinemachineExtension（Cinemachine扩展）

### 字段 (7)

- `CinemachineCore.Stage m_ApplyAfter`（CinemachineCore.Stage m_应用After）(偏移: 0x14)
- `float m_Tilt`（float m_Tilt）(偏移: 0x18)
- `float m_Pan`（float m_Pan）(偏移: 0x1C)
- `float m_Dutch`（float m_Dutch）(偏移: 0x20)
- `float m_ZoomScale`（float m_瞄准缩放）(偏移: 0x24)
- `float m_FollowAttachment`（float m_FollowAttachment）(偏移: 0x28)
- `float m_LookAtAttachment`（float m_LookAtAttachment）(偏移: 0x2C)

### 方法 (4)

- `void Reset()`
  （void 重置（））
- `void OnValidate()`
  （void 验证时（））
- `void PrePipelineMutateCameraStateCallback(CinemachineVirtualCameraBase vcam, ref CameraState curState, float deltaTime)`
  （void PrePipelineMutate摄像机状态回调（Cinemachine虚拟的摄像机基础 vcam, ref CameraState curState, float deltaTime））
- `void PostPipelineStageCallback(CinemachineVirtualCameraBase vcam, CinemachineCore.Stage stage, ref CameraState state, float deltaTime)`
  （void 后管线阶段回调（Cinemachine虚拟摄像机基类 vcam, CinemachineCore.阶段 stage, 引用 CameraState state, 浮点数 deltaTime））

---

## CinemachineSameAsFollowTarget（CinemachineSameAsFollow目标）

**继承**: CinemachineComponentBase（Cinemachine组件基类）

### 字段 (2)

- `float m_Damping`（浮点数 m_阻尼）(偏移: 0x28)
- `Quaternion m_PreviousReferenceOrientation`（Quaternion m_上一个引用Orientation）(偏移: 0x2C)

### 方法 (4)

- `bool get_IsValid()`
  （布尔值 获取_是否有效（））
- `CinemachineCore.Stage get_Stage()`
  （CinemachineCore.阶段 获取_阶段（））
- `float GetMaxDampTime()`
  （浮点数 获取最大阻尼时间（））
- `void MutateCameraState(ref CameraState curState, float deltaTime)`
  （void 变更摄像机状态（引用 CameraState curState, 浮点数 deltaTime））

---

## CinemachineShot（Cinemachine射击）

**继承**: PlayableAsset, IPropertyPreview（Playable资产, I属性Preview）

### 字段 (2)

- `string DisplayName`（string Display名称）(偏移: 0xC)
- `ExposedReference<CinemachineVirtualCameraBase> VirtualCamera`（ExposedReference<Cinemachine虚拟的摄像机Base> 虚拟的摄像机）(偏移: 0x10)

### 方法 (2)

- `Playable CreatePlayable(PlayableGraph graph, GameObject owner)`
  （Playable 创建Playable（PlayableGraph graph, 游戏对象 owner））
- `void GatherProperties(PlayableDirector director, IPropertyCollector driver)`
  （void 收集属性（可播放导演 director, I属性收集器 driver））

---

## CinemachineShotPlayable（Cinemachine射击Playable）

**继承**: PlayableBehaviour（可播放行为）

### 字段 (1)

- `CinemachineVirtualCameraBase VirtualCamera`（Cinemachine虚拟的摄像机基础 虚拟的摄像机）(偏移: 0x8)

### 方法 (1)

- `bool get_IsValid()`
  （布尔值 获取_是否有效（））

---

## CinemachineSmoothPath（CinemachineSmooth路径）

**继承**: CinemachinePathBase（Cinemachine路径基础）

### 字段 (5)

- `bool m_Looped`（bool m_Looped）(偏移: 0x2C)
- `CinemachineSmoothPath.Waypoint[] m_Waypoints`（CinemachineSmoothPath.Waypoint[] m_Waypoints）(偏移: 0x30)
- `CinemachineSmoothPath.Waypoint[] m_ControlPoints1`（CinemachineSmoothPath.Waypoint[] m_控制Points1）(偏移: 0x34)
- `CinemachineSmoothPath.Waypoint[] m_ControlPoints2`（CinemachineSmoothPath.Waypoint[] m_控制Points2）(偏移: 0x38)
- `bool m_IsLoopedCache`（bool m_是否Looped缓存）(偏移: 0x3C)

### 方法 (13)

- `float get_MinPos()`
  （float get_最小Pos（））
- `float get_MaxPos()`
  （float get_最大Pos（））
- `bool get_Looped()`
  （bool get_Looped（））
- `int get_DistanceCacheSampleStepsPerSegment()`
  （int get_距离缓存SampleStepsPerSegment（））
- `void OnValidate()`
  （void 验证时（））
- `void Reset()`
  （void 重置（））
- `void InvalidateDistanceCache()`
  （void Invalidate距离缓存（））
- `void UpdateControlPoints()`
  （void 更新控制Points（））
- `float GetBoundingIndices(float pos, out int indexA, out int indexB)`
  （float 获取BoundingIndices（float pos, out int indexA, out int indexB））
- `Vector3 EvaluatePosition(float pos)`
  （三维向量 EvaluatePosition（float pos））
- `Vector3 EvaluateTangent(float pos)`
  （三维向量 EvaluateTangent（float pos））
- `Quaternion EvaluateOrientation(float pos)`
  （Quaternion EvaluateOrientation（float pos））
- `Quaternion RollAroundForward(float angle)`
  （Quaternion RollAround前进（float angle））

---

## CinemachineSmoothPath.Waypoint（CinemachineSmoothPath.Waypoint）

### 字段 (2)

- `Vector3 position`（三维向量 位置）(偏移: 0x0)
- `float roll`（float roll）(偏移: 0xC)

### 方法 (2)

- `Vector4 get_AsVector4()`
  （Vector4 get_AsVector4（））
- `CinemachineSmoothPath.Waypoint FromVector4(Vector4 v)`
  （CinemachineSmoothPath.Waypoint FromVector4（Vector4 v））

---

## CinemachineStateDrivenCamera（Cinemachine状态Driven摄像机）

**继承**: CinemachineVirtualCameraBase（Cinemachine虚拟摄像机基类）

### 字段 (17)

- `Transform m_LookAt`（变换 m_看向）(偏移: 0x40)
- `Transform m_Follow`（变换 m_跟随）(偏移: 0x44)
- `Animator m_AnimatedTarget`（动画器 m_Animated目标）(偏移: 0x48)
- `int m_LayerIndex`（int m_层索引）(偏移: 0x4C)
- `bool m_ShowDebugText`（布尔值 m_显示调试文本）(偏移: 0x50)
- `CinemachineVirtualCameraBase[] m_ChildCameras`（Cinemachine虚拟摄像机Base[] m_子摄像机）(偏移: 0x54)
- `CinemachineStateDrivenCamera.Instruction[] m_Instructions`（Cinemachine状态DrivenCamera.Instruction[] m_Instructions）(偏移: 0x58)
- `CinemachineBlendDefinition m_DefaultBlend`（CinemachineBlendDefinition m_默认的Blend）(偏移: 0x5C)
- `CinemachineBlenderSettings m_CustomBlends`（CinemachineBlenderSettings m_自定义的Blends）(偏移: 0x68)
- `CinemachineStateDrivenCamera.ParentHash[] m_ParentHash`（Cinemachine状态DrivenCamera.父级Hash[] m_父级Hash）(偏移: 0x6C)
- `CameraState m_State`（摄像机状态 m_状态）(偏移: 0x78)
- `float mActivationTime`（float mActivation时间）(偏移: 0x134)
- `CinemachineStateDrivenCamera.Instruction mActiveInstruction`（Cinemachine状态DrivenCamera.Instruction m激活的Instruction）(偏移: 0x138)
- `float mPendingActivationTime`（float mPendingActivation时间）(偏移: 0x148)
- `CinemachineStateDrivenCamera.Instruction mPendingInstruction`（Cinemachine状态DrivenCamera.Instruction mPendingInstruction）(偏移: 0x14C)
- `CinemachineBlend mActiveBlend`（CinemachineBlend m激活的Blend）(偏移: 0x15C)
- `List<AnimatorClipInfo> m_clipInfoList`（List<动画器弹匣Info> m_clip信息列表）(偏移: 0x168)

### 方法 (29)

- `string get_Description()`
  （字符串 获取_描述（））
- `void set_LiveChild(ICinemachineCamera value)`
  （void 设置_活动子级（ICinemachine摄像机 value））
- `ICinemachineCamera get_LiveChild()`
  （ICinemachine摄像机 获取_活动子级（））
- `bool IsLiveChild(ICinemachineCamera vcam, bool dominantChildOnly = False)`
  （布尔值 是否活动子级（ICinemachine摄像机 vcam, 布尔值 仅主从子级 = 假））
- `CameraState get_State()`
  （摄像机状态 get_状态（））
- `Transform get_LookAt()`
  （变换 获取_看向（））
- `void set_LookAt(Transform value)`
  （void 设置_看向（变换 value））
- `Transform get_Follow()`
  （变换 获取_跟随（））
- `void set_Follow(Transform value)`
  （void 设置_跟随（变换 value））
- `void OnTargetObjectWarped(Transform target, Vector3 positionDelta)`
  （void 目标对象扭曲时（变换 target, 三维向量 位置增量））
- `void ForceCameraPosition(Vector3 pos, Quaternion rot)`
  （void 强制摄像机位置（三维向量 pos, 四元数 rot））
- `void OnTransitionFromCamera(ICinemachineCamera fromCam, Vector3 worldUp, float deltaTime)`
  （void 从摄像机过渡时（ICinemachine摄像机 fromCam, 三维向量 worldUp, 浮点数 deltaTime））
- `ICinemachineCamera get_TransitioningFrom()`
  （ICinemachine摄像机 get_TransitioningFrom（））
- `void set_TransitioningFrom(ICinemachineCamera value)`
  （void set_TransitioningFrom（ICinemachine摄像机 value））
- `void InternalUpdateCameraState(Vector3 worldUp, float deltaTime)`
  （void 内部更新摄像机状态（三维向量 worldUp, 浮点数 deltaTime））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `void OnTransformChildrenChanged()`
  （void 变换子级改变时（））
- `void OnGuiHandler()`
  （void GUI处理器（））
- `CinemachineVirtualCameraBase[] get_ChildCameras()`
  （Cinemachine虚拟摄像机Base[] 获取_子摄像机（））
- `bool get_IsBlending()`
  （布尔值 获取_是否混合（））
- `int CreateFakeHash(int parentHash, AnimationClip clip)`
  （int 创建FakeHash（int parentHash, 动画弹匣 clip））
- `int LookupFakeHash(int parentHash, AnimationClip clip)`
  （int LookupFakeHash（int parentHash, 动画弹匣 clip））
- `void InvalidateListOfChildren()`
  （void 使无效子级列表（））
- `void UpdateListOfChildren()`
  （void 更新列表OfChildren（））
- `void ValidateInstructions()`
  （void 验证Instructions（））
- `CinemachineVirtualCameraBase ChooseCurrentCamera()`
  （Cinemachine虚拟的摄像机基础 Choose当前摄像机（））
- `int GetClipHash(int hash, List<AnimatorClipInfo> clips)`
  （int 获取弹匣Hash（int hash, List<动画器弹匣Info> clips））
- `CinemachineBlendDefinition LookupBlend(ICinemachineCamera fromKey, ICinemachineCamera toKey)`
  （CinemachineBlendDefinition LookupBlend（ICinemachine摄像机 fromKey, ICinemachine摄像机 toKey））

---

## CinemachineStateDrivenCamera.HashPair（Cinemachine状态DrivenCamera.HashPair）

### 字段 (2)

- `int parentHash`（int parentHash）(偏移: 0x0)
- `int hash`（int hash）(偏移: 0x4)

---

## CinemachineStateDrivenCamera.Instruction（Cinemachine状态DrivenCamera.Instruction）

### 字段 (4)

- `int m_FullHash`（int m_满Hash）(偏移: 0x0)
- `CinemachineVirtualCameraBase m_VirtualCamera`（Cinemachine虚拟的摄像机基础 m_虚拟的摄像机）(偏移: 0x4)
- `float m_ActivateAfter`（float m_激活After）(偏移: 0x8)
- `float m_MinDuration`（float m_最小持续时间）(偏移: 0xC)

---

## CinemachineStateDrivenCamera.ParentHash（Cinemachine状态DrivenCamera.父级Hash）

### 字段 (2)

- `int m_Hash`（int m_Hash）(偏移: 0x0)
- `int m_ParentHash`（int m_父级Hash）(偏移: 0x4)

---

## CinemachineStoryboard（CinemachineStoryboard）

**继承**: CinemachineExtension（Cinemachine扩展）

### 字段 (12)

- `bool s_StoryboardGlobalMute`（bool s_Storyboard全局的Mute）(偏移: 0x0)
- `bool m_ShowImage`（bool m_显示图像）(偏移: 0x14)
- `Texture m_Image`（纹理 m_图像）(偏移: 0x18)
- `CinemachineStoryboard.FillStrategy m_Aspect`（CinemachineStoryboard.FillStrategy m_Aspect）(偏移: 0x1C)
- `float m_Alpha`（float m_透明度）(偏移: 0x20)
- `Vector2 m_Center`（二维向量 m_中心）(偏移: 0x24)
- `Vector3 m_Rotation`（三维向量 m_Rotation）(偏移: 0x2C)
- `Vector2 m_Scale`（二维向量 m_缩放）(偏移: 0x38)
- `bool m_SyncScale`（bool m_同步缩放）(偏移: 0x40)
- `bool m_MuteCamera`（bool m_Mute摄像机）(偏移: 0x41)
- `float m_SplitView`（float m_Split视图）(偏移: 0x44)
- `List<CinemachineStoryboard.CanvasInfo> mCanvasInfo`（List<CinemachineStoryboard.画布Info> m画布信息）(偏移: 0x48)

### 方法 (10)

- `void PostPipelineStageCallback(CinemachineVirtualCameraBase vcam, CinemachineCore.Stage stage, ref CameraState state, float deltaTime)`
  （void 后管线阶段回调（Cinemachine虚拟摄像机基类 vcam, CinemachineCore.阶段 stage, 引用 CameraState state, 浮点数 deltaTime））
- `void ConnectToVcam(bool connect)`
  （void ConnectToVcam（bool connect））
- `string get_CanvasName()`
  （string get_画布名称（））
- `void CameraUpdatedCallback(CinemachineBrain brain)`
  （void 摄像机Updated回调（Cinemachine爆头 brain））
- `CinemachineStoryboard.CanvasInfo LocateMyCanvas(CinemachineBrain parent, bool createIfNotFound)`
  （CinemachineStoryboard.画布信息 LocateMy画布（Cinemachine爆头 parent, bool createIfNotFound））
- `void CreateCanvas(CinemachineStoryboard.CanvasInfo ci)`
  （void 创建画布（CinemachineStoryboard.画布信息 ci））
- `void DestroyCanvas()`
  （void 销毁画布（））
- `void PlaceImage(CinemachineStoryboard.CanvasInfo ci, float alpha)`
  （void Place图像（CinemachineStoryboard.画布信息 ci, float alpha））
- `void StaticBlendingHandler(CinemachineBrain brain)`
  （void 静态的Blending处理器（Cinemachine爆头 brain））
- `void InitializeModule()`
  （void 初始化模块（））

---

## CinemachineStoryboard.CanvasInfo（CinemachineStoryboard.画布信息）

### 字段 (4)

- `GameObject mCanvas`（游戏对象 m画布）(偏移: 0x8)
- `CinemachineBrain mCanvasParent`（Cinemachine爆头 m画布父级）(偏移: 0xC)
- `RectTransform mViewport`（Rect变换 mViewport）(偏移: 0x10)
- `RawImage mRawImage`（Raw图像 mRaw图像）(偏移: 0x14)

---

## CinemachineStoryboard.FillStrategy（CinemachineStoryboard.FillStrategy）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineTargetGroup（Cinemachine目标组）

**继承**: MonoBehaviour, ICinemachineTargetGroup（MonoBehaviour行为, ICinemachine目标组）

### 字段 (7)

- `CinemachineTargetGroup.PositionMode m_PositionMode`（Cinemachine目标Group.Position模式 m_Position模式）(偏移: 0xC)
- `CinemachineTargetGroup.RotationMode m_RotationMode`（Cinemachine目标Group.Rotation模式 m_Rotation模式）(偏移: 0x10)
- `CinemachineTargetGroup.UpdateMethod m_UpdateMethod`（Cinemachine目标Group.更新Method m_更新Method）(偏移: 0x14)
- `CinemachineTargetGroup.Target[] m_Targets`（Cinemachine目标Group.Target[] m_Targets）(偏移: 0x18)
- `float m_MaxWeight`（float m_最大Weight）(偏移: 0x34)
- `Vector3 m_AveragePos`（三维向量 m_AveragePos）(偏移: 0x38)
- `BoundingSphere m_BoundingSphere`（BoundingSphere m_BoundingSphere）(偏移: 0x44)

### 方法 (21)

- `Transform get_Transform()`
  （变换 get_变换（））
- `Bounds get_BoundingBox()`
  （Bounds get_BoundingBox（））
- `void set_BoundingBox(Bounds value)`
  （void set_BoundingBox（Bounds value））
- `BoundingSphere get_Sphere()`
  （BoundingSphere get_Sphere（））
- `bool get_IsEmpty()`
  （布尔值 获取_是否为空（））
- `void AddMember(Transform t, float weight, float radius)`
  （void 添加Member（变换 t, float weight, float radius））
- `void RemoveMember(Transform t)`
  （void 移除Member（变换 t））
- `int FindMember(Transform t)`
  （int 查找Member（变换 t））
- `BoundingSphere GetWeightedBoundsForMember(int index)`
  （BoundingSphere 获取WeightedBoundsForMember（int index））
- `Bounds GetViewSpaceBoundingBox(Matrix4x4 observer)`
  （Bounds 获取视图SpaceBoundingBox（Matrix4x4 observer））
- `BoundingSphere WeightedMemberBounds(CinemachineTargetGroup.Target t, Vector3 avgPos, float maxWeight)`
  （BoundingSphere WeightedMemberBounds（Cinemachine目标Group.目标 t, 三维向量 avgPos, float maxWeight））
- `void DoUpdate()`
  （void Do更新（））
- `BoundingSphere CalculateBoundingSphere(float maxWeight)`
  （BoundingSphere 计算BoundingSphere（float maxWeight））
- `Vector3 CalculateAveragePosition(out float maxWeight)`
  （三维向量 计算AveragePosition（out float maxWeight））
- `Quaternion CalculateAverageOrientation()`
  （Quaternion 计算AverageOrientation（））
- `Bounds CalculateBoundingBox(Vector3 avgPos, float maxWeight)`
  （Bounds 计算BoundingBox（三维向量 avgPos, float maxWeight））
- `void OnValidate()`
  （void 验证时（））
- `void FixedUpdate()`
  （void 固定更新（））
- `void Update()`
  （void 更新（））
- `void LateUpdate()`
  （void 延迟更新（））
- `void GetViewSpaceAngularBounds(Matrix4x4 observer, out Vector2 minAngles, out Vector2 maxAngles, out Vector2 zRange)`
  （void 获取视图SpaceAngularBounds（Matrix4x4 observer, out Vector2 minAngles, out Vector2 maxAngles, out Vector2 zRange））

---

## CinemachineTargetGroup.PositionMode（Cinemachine目标Group.Position模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineTargetGroup.RotationMode（Cinemachine目标Group.Rotation模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineTargetGroup.Target（Cinemachine目标Group.目标）

### 字段 (3)

- `Transform target`（变换 目标）(偏移: 0x0)
- `float weight`（浮点数 权重）(偏移: 0x4)
- `float radius`（浮点数 半径）(偏移: 0x8)

---

## CinemachineTargetGroup.UpdateMethod（Cinemachine目标Group.更新Method）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineTouchInputMapper（Cinemachine触摸输入Mapper）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (4)

- `float TouchSensitivityX`（float 触摸SensitivityX）(偏移: 0xC)
- `float TouchSensitivityY`（float 触摸SensitivityY）(偏移: 0x10)
- `string TouchXInputMapTo`（string 触摸X输入映射To）(偏移: 0x14)
- `string TouchYInputMapTo`（string 触摸Y输入映射To）(偏移: 0x18)

### 方法 (2)

- `void Start()`
  （void 开始（））
- `float GetInputAxis(string axisName)`
  （float 获取输入轴（string axisName））

---

## CinemachineTrack（CinemachineTrack）

**继承**: TrackAsset（轨道资产）

### 方法 (1)

- `Playable CreateTrackMixer(PlayableGraph graph, GameObject go, int inputCount)`
  （Playable 创建TrackMixer（PlayableGraph graph, 游戏对象 go, int inputCount））

---

## CinemachineTrackedDolly（CinemachineTrackedDolly）

**继承**: CinemachineComponentBase（Cinemachine组件基类）

### 字段 (15)

- `CinemachinePathBase m_Path`（Cinemachine路径基础 m_路径）(偏移: 0x28)
- `float m_PathPosition`（float m_路径Position）(偏移: 0x2C)
- `CinemachinePathBase.PositionUnits m_PositionUnits`（Cinemachine路径Base.PositionUnits m_PositionUnits）(偏移: 0x30)
- `Vector3 m_PathOffset`（三维向量 m_路径Offset）(偏移: 0x34)
- `float m_XDamping`（float m_XDamping）(偏移: 0x40)
- `float m_YDamping`（float m_YDamping）(偏移: 0x44)
- `float m_ZDamping`（float m_ZDamping）(偏移: 0x48)
- `CinemachineTrackedDolly.CameraUpMode m_CameraUp`（CinemachineTrackedDolly.摄像机上模式 m_摄像机上）(偏移: 0x4C)
- `float m_PitchDamping`（float m_俯仰角Damping）(偏移: 0x50)
- `float m_YawDamping`（float m_偏航角Damping）(偏移: 0x54)
- `float m_RollDamping`（float m_RollDamping）(偏移: 0x58)
- `CinemachineTrackedDolly.AutoDolly m_AutoDolly`（CinemachineTrackedDolly.自动Dolly m_自动Dolly）(偏移: 0x5C)
- `float m_PreviousPathPosition`（float m_上一个路径Position）(偏移: 0x6C)
- `Quaternion m_PreviousOrientation`（Quaternion m_上一个Orientation）(偏移: 0x70)
- `Vector3 m_PreviousCameraPosition`（三维向量 m_上一个摄像机Position）(偏移: 0x80)

### 方法 (6)

- `bool get_IsValid()`
  （布尔值 获取_是否有效（））
- `CinemachineCore.Stage get_Stage()`
  （CinemachineCore.阶段 获取_阶段（））
- `float GetMaxDampTime()`
  （浮点数 获取最大阻尼时间（））
- `void MutateCameraState(ref CameraState curState, float deltaTime)`
  （void 变更摄像机状态（引用 CameraState curState, 浮点数 deltaTime））
- `Quaternion GetCameraOrientationAtPathPoint(Quaternion pathOrientation, Vector3 up)`
  （Quaternion 获取摄像机OrientationAt路径Point（Quaternion pathOrientation, 三维向量 up））
- `Vector3 get_AngularDamping()`
  （三维向量 get_AngularDamping（））

---

## CinemachineTrackedDolly.AutoDolly（CinemachineTrackedDolly.自动Dolly）

### 字段 (4)

- `bool m_Enabled`（bool m_启用的）(偏移: 0x0)
- `float m_PositionOffset`（float m_PositionOffset）(偏移: 0x4)
- `int m_SearchRadius`（int m_搜索Radius）(偏移: 0x8)
- `int m_SearchResolution`（int m_搜索Resolution）(偏移: 0xC)

---

## CinemachineTrackedDolly.CameraUpMode（CinemachineTrackedDolly.摄像机上模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineTransposer（CinemachineTransposer）

**继承**: CinemachineComponentBase（Cinemachine组件基类）

### 字段 (15)

- `CinemachineTransposer.BindingMode m_BindingMode`（CinemachineTransposer.Binding模式 m_Binding模式）(偏移: 0x28)
- `Vector3 m_FollowOffset`（三维向量 m_FollowOffset）(偏移: 0x2C)
- `float m_XDamping`（float m_XDamping）(偏移: 0x38)
- `float m_YDamping`（float m_YDamping）(偏移: 0x3C)
- `float m_ZDamping`（float m_ZDamping）(偏移: 0x40)
- `CinemachineTransposer.AngularDampingMode m_AngularDampingMode`（CinemachineTransposer.AngularDamping模式 m_AngularDamping模式）(偏移: 0x44)
- `float m_PitchDamping`（float m_俯仰角Damping）(偏移: 0x48)
- `float m_YawDamping`（float m_偏航角Damping）(偏移: 0x4C)
- `float m_RollDamping`（float m_RollDamping）(偏移: 0x50)
- `float m_AngularDamping`（float m_AngularDamping）(偏移: 0x54)
- `Vector3 m_PreviousTargetPosition`（三维向量 m_上一个目标Position）(偏移: 0x5C)
- `Quaternion m_PreviousReferenceOrientation`（Quaternion m_上一个引用Orientation）(偏移: 0x68)
- `Quaternion m_targetOrientationOnAssign`（Quaternion m_targetOrientationOnAssign）(偏移: 0x78)
- `Vector3 m_PreviousOffset`（三维向量 m_上一个Offset）(偏移: 0x88)
- `Transform m_previousTarget`（变换 m_previous目标）(偏移: 0x94)

### 方法 (17)

- `void OnValidate()`
  （void 验证时（））
- `bool get_HideOffsetInInspector()`
  （bool get_隐藏OffsetInInspector（））
- `void set_HideOffsetInInspector(bool value)`
  （void set_隐藏OffsetInInspector（bool value））
- `Vector3 get_EffectiveOffset()`
  （三维向量 get_EffectiveOffset（））
- `bool get_IsValid()`
  （布尔值 获取_是否有效（））
- `CinemachineCore.Stage get_Stage()`
  （CinemachineCore.阶段 获取_阶段（））
- `float GetMaxDampTime()`
  （浮点数 获取最大阻尼时间（））
- `void MutateCameraState(ref CameraState curState, float deltaTime)`
  （void 变更摄像机状态（引用 CameraState curState, 浮点数 deltaTime））
- `void OnTargetObjectWarped(Transform target, Vector3 positionDelta)`
  （void 目标对象扭曲时（变换 target, 三维向量 位置增量））
- `void ForceCameraPosition(Vector3 pos, Quaternion rot)`
  （void 强制摄像机位置（三维向量 pos, 四元数 rot））
- `void InitPrevFrameStateInfo(ref CameraState curState, float deltaTime)`
  （void 初始化PrevFrame状态信息（ref CameraState curState, float deltaTime））
- `void TrackTarget(float deltaTime, Vector3 up, Vector3 desiredCameraOffset, out Vector3 outTargetPosition, out Quaternion outTargetOrient)`
  （void Track目标（float deltaTime, 三维向量 up, 三维向量 desiredCameraOffset, out Vector3 outTargetPosition, out Quaternion outTargetOrient））
- `Vector3 GetOffsetForMinimumTargetDistance(Vector3 dampedTargetPos, Vector3 cameraOffset, Vector3 cameraFwd, Vector3 up, Vector3 actualTargetPos)`
  （三维向量 获取OffsetForMinimum目标距离（三维向量 dampedTargetPos, 三维向量 cameraOffset, 三维向量 cameraFwd, 三维向量 up, 三维向量 actualTargetPos））
- `Vector3 get_Damping()`
  （三维向量 get_Damping（））
- `Vector3 get_AngularDamping()`
  （三维向量 get_AngularDamping（））
- `Vector3 GetTargetCameraPosition(Vector3 worldUp)`
  （三维向量 获取目标摄像机Position（三维向量 worldUp））
- `Quaternion GetReferenceOrientation(Vector3 worldUp)`
  （Quaternion 获取引用Orientation（三维向量 worldUp））

---

## CinemachineTransposer.AngularDampingMode（CinemachineTransposer.AngularDamping模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineTransposer.BindingMode（CinemachineTransposer.Binding模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineTriggerAction（Cinemachine触发器动作）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (8)

- `LayerMask m_LayerMask`（层掩码 m_层掩码）(偏移: 0xC)
- `string m_WithTag`（string m_With标签）(偏移: 0x10)
- `string m_WithoutTag`（string m_Without标签）(偏移: 0x14)
- `int m_SkipFirst`（int m_Skip第一个）(偏移: 0x18)
- `bool m_Repeating`（bool m_Repeating）(偏移: 0x1C)
- `CinemachineTriggerAction.ActionSettings m_OnObjectEnter`（Cinemachine触发器Action.动作Settings m_On对象Enter）(偏移: 0x20)
- `CinemachineTriggerAction.ActionSettings m_OnObjectExit`（Cinemachine触发器Action.动作Settings m_On对象Exit）(偏移: 0x38)
- `HashSet<GameObject> m_ActiveTriggerObjects`（HashSet<游戏Object> m_激活的触发器Objects）(偏移: 0x50)

### 方法 (12)

- `bool Filter(GameObject other)`
  （bool Filter（游戏对象 other））
- `void InternalDoTriggerEnter(GameObject other)`
  （void 内部的Do触发器Enter（游戏对象 other））
- `void InternalDoTriggerExit(GameObject other)`
  （void 内部的Do触发器Exit（游戏对象 other））
- `void OnTriggerEnter(Collider other)`
  （void 触发器进入时（碰撞器 other））
- `void OnTriggerExit(Collider other)`
  （void 触发器退出时（碰撞器 other））
- `void OnCollisionEnter(Collision other)`
  （void OnCollisionEnter（Collision other））
- `void OnCollisionExit(Collision other)`
  （void OnCollisionExit（Collision other））
- `void OnTriggerEnter2D(Collider2D other)`
  （void On触发器Enter2D（Collider2D other））
- `void OnTriggerExit2D(Collider2D other)`
  （void On触发器Exit2D（Collider2D other））
- `void OnCollisionEnter2D(Collision2D other)`
  （void OnCollisionEnter2D（Collision2D other））
- `void OnCollisionExit2D(Collision2D other)`
  （void OnCollisionExit2D（Collision2D other））
- `void OnEnable()`
  （void 启用时（））

---

## CinemachineTriggerAction.ActionSettings（Cinemachine触发器Action.动作Settings）

### 字段 (6)

- `CinemachineTriggerAction.ActionSettings.Mode m_Action`（Cinemachine触发器Action.动作Settings.模式 m_动作）(偏移: 0x0)
- `Object m_Target`（对象 m_目标）(偏移: 0x4)
- `int m_BoostAmount`（int m_BoostAmount）(偏移: 0x8)
- `float m_StartTime`（float m_开始时间）(偏移: 0xC)
- `CinemachineTriggerAction.ActionSettings.TimeMode m_Mode`（Cinemachine触发器Action.动作Settings.时间模式 m_模式）(偏移: 0x10)
- `CinemachineTriggerAction.ActionSettings.TriggerEvent m_Event`（Cinemachine触发器Action.动作Settings.触发器事件 m_事件）(偏移: 0x14)

### 方法 (1)

- `void Invoke()`
  （void 调用（））

---

## CinemachineTriggerAction.ActionSettings.Mode（Cinemachine触发器Action.动作Settings.模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineTriggerAction.ActionSettings.TimeMode（Cinemachine触发器Action.动作Settings.时间模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineUniversalPixelPerfect（CinemachineUniversalPixelPerfect）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 方法 (1)

- `void OnEnable()`
  （void 启用时（））

---

## CinemachineVirtualCamera（Cinemachine虚拟的摄像机）

**继承**: CinemachineVirtualCameraBase（Cinemachine虚拟摄像机基类）

### 字段 (12)

- `Transform m_LookAt`（变换 m_看向）(偏移: 0x40)
- `Transform m_Follow`（变换 m_跟随）(偏移: 0x44)
- `LensSettings m_Lens`（LensSettings m_Lens）(偏移: 0x48)
- `CinemachineVirtualCameraBase.TransitionParams m_Transitions`（Cinemachine虚拟的摄像机Base.TransitionParams m_Transitions）(偏移: 0x74)
- `CinemachineVirtualCameraBase.BlendHint m_LegacyBlendHint`（Cinemachine虚拟的摄像机Base.BlendHint m_LegacyBlendHint）(偏移: 0x80)
- `CinemachineVirtualCamera.CreatePipelineDelegate CreatePipelineOverride`（Cinemachine虚拟的Camera.创建Pipeline委托 创建Pipeline重写）(偏移: 0x0)
- `CinemachineVirtualCamera.DestroyPipelineDelegate DestroyPipelineOverride`（Cinemachine虚拟的Camera.销毁Pipeline委托 销毁Pipeline重写）(偏移: 0x4)
- `CameraState m_State`（摄像机状态 m_状态）(偏移: 0x88)
- `CinemachineComponentBase[] m_ComponentPipeline`（Cinemachine组件Base[] m_组件Pipeline）(偏移: 0x140)
- `Transform m_ComponentOwner`（变换 m_组件Owner）(偏移: 0x144)
- `Transform mCachedLookAtTarget`（变换 mCachedLookAt目标）(偏移: 0x148)
- `CinemachineVirtualCameraBase mCachedLookAtTargetVcam`（Cinemachine虚拟的摄像机基础 mCachedLookAt目标Vcam）(偏移: 0x14C)

### 方法 (27)

- `CameraState get_State()`
  （摄像机状态 get_状态（））
- `Transform get_LookAt()`
  （变换 获取_看向（））
- `void set_LookAt(Transform value)`
  （void 设置_看向（变换 value））
- `Transform get_Follow()`
  （变换 获取_跟随（））
- `void set_Follow(Transform value)`
  （void 设置_跟随（变换 value））
- `float GetMaxDampTime()`
  （浮点数 获取最大阻尼时间（））
- `void InternalUpdateCameraState(Vector3 worldUp, float deltaTime)`
  （void 内部更新摄像机状态（三维向量 worldUp, 浮点数 deltaTime））
- `void OnEnable()`
  （void 启用时（））
- `void OnDestroy()`
  （void 销毁时（））
- `void OnValidate()`
  （void 验证时（））
- `void OnTransformChildrenChanged()`
  （void 变换子级改变时（））
- `void Reset()`
  （void 重置（））
- `void DestroyPipeline()`
  （void 销毁Pipeline（））
- `Transform CreatePipeline(CinemachineVirtualCamera copyFrom)`
  （变换 创建Pipeline（Cinemachine虚拟的摄像机 copyFrom））
- `void InvalidateComponentPipeline()`
  （void Invalidate组件Pipeline（））
- `Transform GetComponentOwner()`
  （变换 获取组件Owner（））
- `CinemachineComponentBase[] GetComponentPipeline()`
  （Cinemachine组件Base[] 获取组件Pipeline（））
- `CinemachineComponentBase GetCinemachineComponent(CinemachineCore.Stage stage)`
  （Cinemachine组件基础 获取Cinemachine组件（CinemachineCore.Stage stage））
- `bool get_UserIsDragging()`
  （bool get_User是否Dragging（））
- `void set_UserIsDragging(bool value)`
  （void set_User是否Dragging（bool value））
- `void UpdateComponentPipeline()`
  （void 更新组件Pipeline（））
- `void SetFlagsForHiddenChild(GameObject child)`
  （void 集合FlagsFor隐藏的子级（游戏对象 child））
- `CameraState CalculateNewState(Vector3 worldUp, float deltaTime)`
  （摄像机状态 计算新的状态（三维向量 worldUp, float deltaTime））
- `void OnTargetObjectWarped(Transform target, Vector3 positionDelta)`
  （void 目标对象扭曲时（变换 target, 三维向量 位置增量））
- `void ForceCameraPosition(Vector3 pos, Quaternion rot)`
  （void 强制摄像机位置（三维向量 pos, 四元数 rot））
- `void SetStateRawPosition(Vector3 pos)`
  （void 集合状态RawPosition（三维向量 pos））
- `void OnTransitionFromCamera(ICinemachineCamera fromCam, Vector3 worldUp, float deltaTime)`
  （void 从摄像机过渡时（ICinemachine摄像机 fromCam, 三维向量 worldUp, 浮点数 deltaTime））

---

## CinemachineVirtualCamera.CreatePipelineDelegate（Cinemachine虚拟的Camera.创建Pipeline委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `Transform Invoke(CinemachineVirtualCamera vcam, string name, CinemachineComponentBase[] copyFrom)`
  （变换 Invoke（Cinemachine虚拟的摄像机 vcam, string name, Cinemachine组件Base[] copyFrom））
- `IAsyncResult BeginInvoke(CinemachineVirtualCamera vcam, string name, CinemachineComponentBase[] copyFrom, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Cinemachine虚拟的摄像机 vcam, string name, Cinemachine组件Base[] copyFrom, 异步回调 callback, object object））
- `Transform EndInvoke(IAsyncResult result)`
  （变换 结束Invoke（I异步Result result））

---

## CinemachineVirtualCamera.DestroyPipelineDelegate（Cinemachine虚拟的Camera.销毁Pipeline委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(GameObject pipeline)`
  （void Invoke（游戏对象 pipeline））
- `IAsyncResult BeginInvoke(GameObject pipeline, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（游戏对象 pipeline, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## CinemachineVirtualCameraBase（Cinemachine虚拟摄像机基类）

**继承**: MonoBehaviour, ICinemachineCamera（MonoBehaviour行为, ICinemachine摄像机）

### 字段 (12)

- `string[] m_ExcludedPropertiesInInspector`（string[] m_ExcludedPropertiesInInspector）(偏移: 0xC)
- `CinemachineCore.Stage[] m_LockStageInInspector`（CinemachineCore.Stage[] m_LockStageInInspector）(偏移: 0x10)
- `int m_ValidatingStreamVersion`（int m_Validating流Version）(偏移: 0x14)
- `bool m_OnValidateCalled`（bool m_On验证Called）(偏移: 0x18)
- `int m_StreamingVersion`（int m_StreamingVersion）(偏移: 0x1C)
- `int m_Priority`（int m_Priority）(偏移: 0x20)
- `CinemachineVirtualCameraBase.StandbyUpdateMode m_StandbyUpdate`（Cinemachine虚拟的摄像机Base.Standby更新模式 m_Standby更新）(偏移: 0x2C)
- `List<CinemachineExtension> mExtensions`（List<CinemachineExtension> mExtensions）(偏移: 0x30)
- `bool m_WasStarted`（bool m_WasStarted）(偏移: 0x35)
- `bool mSlaveStatusUpdated`（bool mSlaveStatusUpdated）(偏移: 0x36)
- `CinemachineVirtualCameraBase m_parentVcam`（Cinemachine虚拟的摄像机基础 m_parentVcam）(偏移: 0x38)
- `int m_QueuePriority`（int m_队列Priority）(偏移: 0x3C)

### 方法 (49)

- `int get_ValidatingStreamVersion()`
  （int get_Validating流Version（））
- `void set_ValidatingStreamVersion(int value)`
  （void set_Validating流Version（int value））
- `float get_FollowTargetAttachment()`
  （float get_Follow目标Attachment（））
- `void set_FollowTargetAttachment(float value)`
  （void set_Follow目标Attachment（float value））
- `float get_LookAtTargetAttachment()`
  （float get_LookAt目标Attachment（））
- `void set_LookAtTargetAttachment(float value)`
  （void set_LookAt目标Attachment（float value））
- `float GetMaxDampTime()`
  （浮点数 获取最大阻尼时间（））
- `float DetachedFollowTargetDamp(float initial, float dampTime, float deltaTime)`
  （float DetachedFollow目标Damp（float initial, float dampTime, float deltaTime））
- `Vector3 DetachedFollowTargetDamp(Vector3 initial, Vector3 dampTime, float deltaTime)`
  （三维向量 DetachedFollow目标Damp（三维向量 initial, 三维向量 dampTime, float deltaTime））
- `Vector3 DetachedFollowTargetDamp(Vector3 initial, float dampTime, float deltaTime)`
  （三维向量 DetachedFollow目标Damp（三维向量 initial, float dampTime, float deltaTime））
- `float DetachedLookAtTargetDamp(float initial, float dampTime, float deltaTime)`
  （float DetachedLookAt目标Damp（float initial, float dampTime, float deltaTime））
- `Vector3 DetachedLookAtTargetDamp(Vector3 initial, Vector3 dampTime, float deltaTime)`
  （三维向量 DetachedLookAt目标Damp（三维向量 initial, 三维向量 dampTime, float deltaTime））
- `Vector3 DetachedLookAtTargetDamp(Vector3 initial, float dampTime, float deltaTime)`
  （三维向量 DetachedLookAt目标Damp（三维向量 initial, float dampTime, float deltaTime））
- `void AddExtension(CinemachineExtension extension)`
  （void 添加扩展（Cinemachine扩展 extension））
- `void RemoveExtension(CinemachineExtension extension)`
  （void 移除扩展（Cinemachine扩展 extension））
- `void InvokePostPipelineStageCallback(CinemachineVirtualCameraBase vcam, CinemachineCore.Stage stage, ref CameraState newState, float deltaTime)`
  （void InvokePostPipelineStage回调（Cinemachine虚拟的摄像机基础 vcam, CinemachineCore.Stage stage, ref CameraState newState, float deltaTime））
- `void InvokePrePipelineMutateCameraStateCallback(CinemachineVirtualCameraBase vcam, ref CameraState newState, float deltaTime)`
  （void InvokePrePipelineMutate摄像机状态回调（Cinemachine虚拟的摄像机基础 vcam, ref CameraState newState, float deltaTime））
- `bool InvokeOnTransitionInExtensions(ICinemachineCamera fromCam, Vector3 worldUp, float deltaTime)`
  （bool InvokeOnTransitionInExtensions（ICinemachine摄像机 fromCam, 三维向量 worldUp, float deltaTime））
- `string get_Name()`
  （字符串 获取_名称（））
- `string get_Description()`
  （字符串 获取_描述（））
- `int get_Priority()`
  （int get_Priority（））
- `void set_Priority(int value)`
  （void set_Priority（int value））
- `void ApplyPositionBlendMethod(ref CameraState state, CinemachineVirtualCameraBase.BlendHint hint)`
  （void 应用PositionBlendMethod（ref CameraState state, Cinemachine虚拟的摄像机Base.BlendHint hint））
- `GameObject get_VirtualCameraGameObject()`
  （游戏对象 get_虚拟的摄像机游戏对象（））
- `bool get_IsValid()`
  （布尔值 获取_是否有效（））
- `ICinemachineCamera get_ParentCamera()`
  （ICinemachine摄像机 get_父级摄像机（））
- `bool IsLiveChild(ICinemachineCamera vcam, bool dominantChildOnly = False)`
  （布尔值 是否活动子级（ICinemachine摄像机 vcam, 布尔值 仅主从子级 = 假））
- `bool get_PreviousStateIsValid()`
  （bool get_上一个状态是否Valid（））
- `void set_PreviousStateIsValid(bool value)`
  （void set_上一个状态是否Valid（bool value））
- `void UpdateCameraState(Vector3 worldUp, float deltaTime)`
  （void 更新摄像机状态（三维向量 worldUp, 浮点数 deltaTime））
- `void OnTransitionFromCamera(ICinemachineCamera fromCam, Vector3 worldUp, float deltaTime)`
  （void 从摄像机过渡时（ICinemachine摄像机 fromCam, 三维向量 worldUp, 浮点数 deltaTime））
- `void OnDestroy()`
  （void 销毁时（））
- `void OnTransformParentChanged()`
  （void 变换父级改变时（））
- `void Start()`
  （void 开始（））
- `void EnsureStarted()`
  （void EnsureStarted（））
- `AxisState.IInputAxisProvider GetInputAxisProvider()`
  （轴State.I输入轴提供者 获取输入轴提供者（））
- `void OnValidate()`
  （void 验证时（））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `void Update()`
  （void 更新（））
- `void UpdateSlaveStatus()`
  （void 更新SlaveStatus（））
- `Transform ResolveLookAt(Transform localLookAt)`
  （变换 ResolveLookAt（变换 localLookAt））
- `Transform ResolveFollow(Transform localFollow)`
  （变换 ResolveFollow（变换 localFollow））
- `void UpdateVcamPoolStatus()`
  （void 更新Vcam池Status（））
- `void MoveToTopOfPrioritySubqueue()`
  （void 移动To顶部OfPrioritySubqueue（））
- `void OnTargetObjectWarped(Transform target, Vector3 positionDelta)`
  （void 目标对象扭曲时（变换 target, 三维向量 位置增量））
- `void ForceCameraPosition(Vector3 pos, Quaternion rot)`
  （void 强制摄像机位置（三维向量 pos, 四元数 rot））
- `CinemachineBlend CreateBlend(ICinemachineCamera camA, ICinemachineCamera camB, CinemachineBlendDefinition blendDef, CinemachineBlend activeBlend)`
  （CinemachineBlend 创建Blend（ICinemachine摄像机 camA, ICinemachine摄像机 camB, CinemachineBlendDefinition blendDef, CinemachineBlend activeBlend））
- `CameraState PullStateFromVirtualCamera(Vector3 worldUp, ref LensSettings lens)`
  （摄像机状态 Pull状态From虚拟的摄像机（三维向量 worldUp, ref LensSettings lens））

---

## CinemachineVirtualCameraBase.BlendHint（Cinemachine虚拟的摄像机Base.BlendHint）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CinemachineVirtualCameraBase.StandbyUpdateMode（Cinemachine虚拟的摄像机Base.Standby更新模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

