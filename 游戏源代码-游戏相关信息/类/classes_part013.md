# 游戏类定义 (Part 13/21)

共 200 个类 (总序号 2401 - 2600)

---

## PhotoCapture.OnCapturedToMemoryCallback（PhotoCapture.OnCapturedToMemory回调）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(PhotoCapture.PhotoCaptureResult result, PhotoCaptureFrame photoCaptureFrame)`
  （void Invoke（PhotoCapture.PhotoCaptureResult result, PhotoCaptureFrame photoCaptureFrame））
- `IAsyncResult BeginInvoke(PhotoCapture.PhotoCaptureResult result, PhotoCaptureFrame photoCaptureFrame, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（PhotoCapture.PhotoCaptureResult result, PhotoCaptureFrame photoCaptureFrame, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## PhotoCapture.OnPhotoModeStartedCallback（PhotoCapture.OnPhoto模式Started回调）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(PhotoCapture.PhotoCaptureResult result)`
  （void Invoke（PhotoCapture.PhotoCaptureResult result））
- `IAsyncResult BeginInvoke(PhotoCapture.PhotoCaptureResult result, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（PhotoCapture.PhotoCaptureResult result, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## PhotoCapture.OnPhotoModeStoppedCallback（PhotoCapture.OnPhoto模式Stopped回调）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(PhotoCapture.PhotoCaptureResult result)`
  （void Invoke（PhotoCapture.PhotoCaptureResult result））
- `IAsyncResult BeginInvoke(PhotoCapture.PhotoCaptureResult result, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（PhotoCapture.PhotoCaptureResult result, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## PhotoCapture.PhotoCaptureResult（PhotoCapture.PhotoCaptureResult）

### 字段 (2)

- `PhotoCapture.CaptureResultType resultType`（PhotoCapture.CaptureResult类型 result类型）(偏移: 0x0)
- `long hResult`（long hResult）(偏移: 0x8)

---

## PhotoCaptureFrame（PhotoCaptureFrame）

**继承**: IDisposable（IDisposable）

### 字段 (1)

- `IntPtr m_NativePtr`（整数Ptr m_NativePtr）(偏移: 0x8)

### 方法 (11)

- `int get_dataLength()`
  （int get_dataLength（））
- `void set_dataLength(int value)`
  （void set_dataLength（int value））
- `void set_hasLocationData(bool value)`
  （void set_hasLocation数据（bool value））
- `void set_pixelFormat(CapturePixelFormat value)`
  （void set_pixel格式化（CapturePixel格式化 value））
- `int GetDataLength()`
  （int 获取数据Length（））
- `bool GetHasLocationData()`
  （bool 获取是否有Location数据（））
- `CapturePixelFormat GetCapturePixelFormat()`
  （CapturePixel格式化 获取CapturePixel格式化（））
- `void Cleanup()`
  （void 清理（））
- `void Dispose_Internal()`
  （void Dispose_内部的（））
- `void Dispose()`
  （void 释放（））
- `void Finalize()`
  （void Finalize（））

---

## PhraseRecognitionSystem（PhraseRecognition系统）

### 字段 (2)

- `PhraseRecognitionSystem.ErrorDelegate OnError`（PhraseRecognitionSystem.Error委托 OnError）(偏移: 0x0)
- `PhraseRecognitionSystem.StatusDelegate OnStatusChanged`（PhraseRecognitionSystem.Status委托 OnStatusChanged）(偏移: 0x4)

### 方法 (2)

- `void PhraseRecognitionSystem_InvokeErrorEvent(SpeechError errorCode)`
  （void PhraseRecognitionSystem_InvokeError事件（SpeechError errorCode））
- `void PhraseRecognitionSystem_InvokeStatusChangedEvent(SpeechSystemStatus status)`
  （void PhraseRecognitionSystem_InvokeStatusChanged事件（Speech系统Status status））

---

## PhraseRecognitionSystem.ErrorDelegate（PhraseRecognitionSystem.Error委托）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(SpeechError errorCode)`
  （void Invoke（SpeechError errorCode））
- `IAsyncResult BeginInvoke(SpeechError errorCode, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（SpeechError errorCode, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## PhraseRecognitionSystem.StatusDelegate（PhraseRecognitionSystem.Status委托）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(SpeechSystemStatus status)`
  （void Invoke（Speech系统Status status））
- `IAsyncResult BeginInvoke(SpeechSystemStatus status, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Speech系统Status status, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## PhraseRecognizedEventArgs（PhraseRecognized事件Args）

### 字段 (5)

- `ConfidenceLevel confidence`（Confidence等级 confidence）(偏移: 0x0)
- `SemanticMeaning[] semanticMeanings`（SemanticMeaning[] semanticMeanings）(偏移: 0x4)
- `string text`（string text）(偏移: 0x8)
- `DateTime phraseStartTime`（Date时间 phrase开始时间）(偏移: 0x10)
- `TimeSpan phraseDuration`（时间Span phrase持续时间）(偏移: 0x18)

---

## PhraseRecognizer（PhraseRecognizer）

### 字段 (2)

- `IntPtr m_Recognizer`（整数Ptr m_Recognizer）(偏移: 0x8)
- `PhraseRecognizer.PhraseRecognizedDelegate OnPhraseRecognized`（PhraseRecognizer.PhraseRecognized委托 OnPhraseRecognized）(偏移: 0xC)

### 方法 (2)

- `void InvokePhraseRecognizedEvent(string text, ConfidenceLevel confidence, SemanticMeaning[] semanticMeanings, long phraseStartFileTime, long phraseDurationTicks)`
  （void InvokePhraseRecognized事件（string text, Confidence等级 confidence, SemanticMeaning[] semanticMeanings, long phraseStartFileTime, long phraseDurationTicks））
- `SemanticMeaning[] MarshalSemanticMeaning(IntPtr keys, IntPtr values, IntPtr valueSizes, int valueCount)`
  （SemanticMeaning[] MarshalSemanticMeaning（整数Ptr keys, 整数Ptr values, 整数Ptr valueSizes, int valueCount））

---

## PhraseRecognizer.PhraseRecognizedDelegate（PhraseRecognizer.PhraseRecognized委托）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(PhraseRecognizedEventArgs args)`
  （void Invoke（PhraseRecognized事件Args args））
- `IAsyncResult BeginInvoke(PhraseRecognizedEventArgs args, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（PhraseRecognized事件Args args, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## Physics（物理）

### 方法 (66)

- `Vector3 get_gravity()`
  （三维向量 get_gravity（））
- `PhysicsScene get_defaultPhysicsScene()`
  （物理场景 get_default物理场景（））
- `void IgnoreCollision(Collider collider1, Collider collider2, bool ignore)`
  （void IgnoreCollision（碰撞器 collider1, 碰撞器 collider2, bool ignore））
- `void IgnoreCollision(Collider collider1, Collider collider2)`
  （void IgnoreCollision（碰撞器 collider1, 碰撞器 collider2））
- `bool Raycast(Vector3 origin, Vector3 direction, float maxDistance, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool Raycast（三维向量 origin, 三维向量 direction, float maxDistance, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool Raycast(Vector3 origin, Vector3 direction, float maxDistance, int layerMask)`
  （bool Raycast（三维向量 origin, 三维向量 direction, float maxDistance, int layerMask））
- `bool Raycast(Vector3 origin, Vector3 direction, float maxDistance)`
  （bool Raycast（三维向量 origin, 三维向量 direction, float maxDistance））
- `bool Raycast(Vector3 origin, Vector3 direction)`
  （bool Raycast（三维向量 origin, 三维向量 direction））
- `bool Raycast(Vector3 origin, Vector3 direction, out RaycastHit hitInfo, float maxDistance, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool Raycast（三维向量 origin, 三维向量 direction, out RaycastHit hitInfo, float maxDistance, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool Raycast(Vector3 origin, Vector3 direction, out RaycastHit hitInfo, float maxDistance, int layerMask)`
  （bool Raycast（三维向量 origin, 三维向量 direction, out RaycastHit hitInfo, float maxDistance, int layerMask））
- `bool Raycast(Vector3 origin, Vector3 direction, out RaycastHit hitInfo, float maxDistance)`
  （bool Raycast（三维向量 origin, 三维向量 direction, out RaycastHit hitInfo, float maxDistance））
- `bool Raycast(Vector3 origin, Vector3 direction, out RaycastHit hitInfo)`
  （bool Raycast（三维向量 origin, 三维向量 direction, out RaycastHit hitInfo））
- `bool Raycast(Ray ray, float maxDistance, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool Raycast（Ray ray, float maxDistance, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool Raycast(Ray ray, float maxDistance, int layerMask)`
  （bool Raycast（Ray ray, float maxDistance, int layerMask））
- `bool Raycast(Ray ray, float maxDistance)`
  （bool Raycast（Ray ray, float maxDistance））
- `bool Raycast(Ray ray)`
  （bool Raycast（Ray ray））
- `bool Raycast(Ray ray, out RaycastHit hitInfo, float maxDistance, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool Raycast（Ray ray, out RaycastHit hitInfo, float maxDistance, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool Raycast(Ray ray, out RaycastHit hitInfo, float maxDistance, int layerMask)`
  （bool Raycast（Ray ray, out RaycastHit hitInfo, float maxDistance, int layerMask））
- `bool Raycast(Ray ray, out RaycastHit hitInfo, float maxDistance)`
  （bool Raycast（Ray ray, out RaycastHit hitInfo, float maxDistance））
- `bool Raycast(Ray ray, out RaycastHit hitInfo)`
  （bool Raycast（Ray ray, out RaycastHit hitInfo））
- `bool Linecast(Vector3 start, Vector3 end, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool Linecast（三维向量 start, 三维向量 end, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool Linecast(Vector3 start, Vector3 end, int layerMask)`
  （bool Linecast（三维向量 start, 三维向量 end, int layerMask））
- `bool Linecast(Vector3 start, Vector3 end, out RaycastHit hitInfo, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool Linecast（三维向量 start, 三维向量 end, out RaycastHit hitInfo, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool Linecast(Vector3 start, Vector3 end, out RaycastHit hitInfo, int layerMask)`
  （bool Linecast（三维向量 start, 三维向量 end, out RaycastHit hitInfo, int layerMask））
- `bool CapsuleCast(Vector3 point1, Vector3 point2, float radius, Vector3 direction, out RaycastHit hitInfo, float maxDistance, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool CapsuleCast（三维向量 point1, 三维向量 point2, float radius, 三维向量 direction, out RaycastHit hitInfo, float maxDistance, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool CapsuleCast(Vector3 point1, Vector3 point2, float radius, Vector3 direction, out RaycastHit hitInfo, float maxDistance, int layerMask)`
  （bool CapsuleCast（三维向量 point1, 三维向量 point2, float radius, 三维向量 direction, out RaycastHit hitInfo, float maxDistance, int layerMask））
- `bool SphereCast(Vector3 origin, float radius, Vector3 direction, out RaycastHit hitInfo, float maxDistance, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool SphereCast（三维向量 origin, float radius, 三维向量 direction, out RaycastHit hitInfo, float maxDistance, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool SphereCast(Vector3 origin, float radius, Vector3 direction, out RaycastHit hitInfo, float maxDistance, int layerMask)`
  （bool SphereCast（三维向量 origin, float radius, 三维向量 direction, out RaycastHit hitInfo, float maxDistance, int layerMask））
- `bool SphereCast(Ray ray, float radius, float maxDistance, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool SphereCast（Ray ray, float radius, float maxDistance, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool SphereCast(Ray ray, float radius, float maxDistance, int layerMask)`
  （bool SphereCast（Ray ray, float radius, float maxDistance, int layerMask））
- `bool SphereCast(Ray ray, float radius, out RaycastHit hitInfo, float maxDistance, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool SphereCast（Ray ray, float radius, out RaycastHit hitInfo, float maxDistance, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `RaycastHit[] Internal_RaycastAll(PhysicsScene physicsScene, Ray ray, float maxDistance, int mask, QueryTriggerInteraction queryTriggerInteraction)`
  （RaycastHit[] Internal_Raycast所有（物理场景 physicsScene, Ray ray, float maxDistance, int mask, Query触发器Interaction queryTriggerInteraction））
- `RaycastHit[] RaycastAll(Vector3 origin, Vector3 direction, float maxDistance, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （RaycastHit[] Raycast所有（三维向量 origin, 三维向量 direction, float maxDistance, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `RaycastHit[] RaycastAll(Vector3 origin, Vector3 direction, float maxDistance, int layerMask)`
  （RaycastHit[] Raycast所有（三维向量 origin, 三维向量 direction, float maxDistance, int layerMask））
- `RaycastHit[] RaycastAll(Vector3 origin, Vector3 direction, float maxDistance)`
  （RaycastHit[] Raycast所有（三维向量 origin, 三维向量 direction, float maxDistance））
- `RaycastHit[] RaycastAll(Vector3 origin, Vector3 direction)`
  （RaycastHit[] Raycast所有（三维向量 origin, 三维向量 direction））
- `RaycastHit[] RaycastAll(Ray ray, float maxDistance, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （RaycastHit[] Raycast所有（Ray ray, float maxDistance, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `RaycastHit[] RaycastAll(Ray ray, float maxDistance, int layerMask)`
  （RaycastHit[] Raycast所有（Ray ray, float maxDistance, int layerMask））
- `RaycastHit[] RaycastAll(Ray ray, float maxDistance)`
  （RaycastHit[] Raycast所有（Ray ray, float maxDistance））
- `RaycastHit[] RaycastAll(Ray ray)`
  （RaycastHit[] Raycast所有（Ray ray））
- `int RaycastNonAlloc(Ray ray, RaycastHit[] results, float maxDistance, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （int RaycastNonAlloc（Ray ray, RaycastHit[] results, float maxDistance, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `int RaycastNonAlloc(Ray ray, RaycastHit[] results, float maxDistance, int layerMask)`
  （int RaycastNonAlloc（Ray ray, RaycastHit[] results, float maxDistance, int layerMask））
- `int RaycastNonAlloc(Ray ray, RaycastHit[] results, float maxDistance)`
  （int RaycastNonAlloc（Ray ray, RaycastHit[] results, float maxDistance））
- `int RaycastNonAlloc(Ray ray, RaycastHit[] results)`
  （int RaycastNonAlloc（Ray ray, RaycastHit[] results））
- `int RaycastNonAlloc(Vector3 origin, Vector3 direction, RaycastHit[] results, float maxDistance, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （int RaycastNonAlloc（三维向量 origin, 三维向量 direction, RaycastHit[] results, float maxDistance, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `int RaycastNonAlloc(Vector3 origin, Vector3 direction, RaycastHit[] results, float maxDistance, int layerMask)`
  （int RaycastNonAlloc（三维向量 origin, 三维向量 direction, RaycastHit[] results, float maxDistance, int layerMask））
- `int RaycastNonAlloc(Vector3 origin, Vector3 direction, RaycastHit[] results, float maxDistance)`
  （int RaycastNonAlloc（三维向量 origin, 三维向量 direction, RaycastHit[] results, float maxDistance））
- `int RaycastNonAlloc(Vector3 origin, Vector3 direction, RaycastHit[] results)`
  （int RaycastNonAlloc（三维向量 origin, 三维向量 direction, RaycastHit[] results））
- `Collider[] OverlapSphere_Internal(PhysicsScene physicsScene, Vector3 position, float radius, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （Collider[] OverlapSphere_内部的（物理场景 physicsScene, 三维向量 position, float radius, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `Collider[] OverlapSphere(Vector3 position, float radius, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （Collider[] OverlapSphere（三维向量 position, float radius, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `Collider[] OverlapSphere(Vector3 position, float radius, int layerMask)`
  （Collider[] OverlapSphere（三维向量 position, float radius, int layerMask））
- `bool Query_ComputePenetration(Collider colliderA, Vector3 positionA, Quaternion rotationA, Collider colliderB, Vector3 positionB, Quaternion rotationB, ref Vector3 direction, ref float distance)`
  （bool Query_ComputePenetration（碰撞器 colliderA, 三维向量 positionA, Quaternion rotationA, 碰撞器 colliderB, 三维向量 positionB, Quaternion rotationB, ref Vector3 direction, ref float distance））
- `bool ComputePenetration(Collider colliderA, Vector3 positionA, Quaternion rotationA, Collider colliderB, Vector3 positionB, Quaternion rotationB, out Vector3 direction, out float distance)`
  （bool ComputePenetration（碰撞器 colliderA, 三维向量 positionA, Quaternion rotationA, 碰撞器 colliderB, 三维向量 positionB, Quaternion rotationB, out Vector3 direction, out float distance））
- `int OverlapSphereNonAlloc(Vector3 position, float radius, Collider[] results, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （int OverlapSphereNonAlloc（三维向量 position, float radius, Collider[] results, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool CheckSphere_Internal(PhysicsScene physicsScene, Vector3 position, float radius, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool 检查Sphere_内部的（物理场景 physicsScene, 三维向量 position, float radius, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool CheckSphere(Vector3 position, float radius, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool 检查Sphere（三维向量 position, float radius, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `int SphereCastNonAlloc(Vector3 origin, float radius, Vector3 direction, RaycastHit[] results, float maxDistance, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （int SphereCastNonAlloc（三维向量 origin, float radius, 三维向量 direction, RaycastHit[] results, float maxDistance, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool CheckCapsule_Internal(PhysicsScene physicsScene, Vector3 start, Vector3 end, float radius, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool 检查Capsule_内部的（物理场景 physicsScene, 三维向量 start, 三维向量 end, float radius, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool CheckCapsule(Vector3 start, Vector3 end, float radius, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool 检查Capsule（三维向量 start, 三维向量 end, float radius, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `void get_gravity_Injected(out Vector3 ret)`
  （void get_gravity_Injected（out Vector3 ret））
- `void get_defaultPhysicsScene_Injected(out PhysicsScene ret)`
  （void get_default物理Scene_Injected（out PhysicsScene ret））
- `RaycastHit[] Internal_RaycastAll_Injected(ref PhysicsScene physicsScene, ref Ray ray, float maxDistance, int mask, QueryTriggerInteraction queryTriggerInteraction)`
  （RaycastHit[] Internal_RaycastAll_Injected（ref PhysicsScene physicsScene, ref Ray ray, float maxDistance, int mask, Query触发器Interaction queryTriggerInteraction））
- `Collider[] OverlapSphere_Internal_Injected(ref PhysicsScene physicsScene, ref Vector3 position, float radius, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （Collider[] OverlapSphere_Internal_Injected（ref PhysicsScene physicsScene, ref Vector3 position, float radius, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool Query_ComputePenetration_Injected(Collider colliderA, ref Vector3 positionA, ref Quaternion rotationA, Collider colliderB, ref Vector3 positionB, ref Quaternion rotationB, ref Vector3 direction, ref float distance)`
  （bool Query_ComputePenetration_Injected（碰撞器 colliderA, ref Vector3 positionA, ref Quaternion rotationA, 碰撞器 colliderB, ref Vector3 positionB, ref Quaternion rotationB, ref Vector3 direction, ref float distance））
- `bool CheckSphere_Internal_Injected(ref PhysicsScene physicsScene, ref Vector3 position, float radius, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool 检查Sphere_Internal_Injected（ref PhysicsScene physicsScene, ref Vector3 position, float radius, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool CheckCapsule_Internal_Injected(ref PhysicsScene physicsScene, ref Vector3 start, ref Vector3 end, float radius, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool 检查Capsule_Internal_Injected（ref PhysicsScene physicsScene, ref Vector3 start, ref Vector3 end, float radius, int layerMask, Query触发器Interaction queryTriggerInteraction））

---

## Physics2D（Physics2D）

### 字段 (1)

- `List<Rigidbody2D> m_LastDisabledRigidbody2D`（List<Rigidbody2D> m_最后一个禁用的Rigidbody2D）(偏移: 0x0)

### 方法 (22)

- `PhysicsScene2D get_defaultPhysicsScene()`
  （物理Scene2D get_default物理场景（））
- `bool get_queriesHitTriggers()`
  （bool get_queries命中Triggers（））
- `RaycastHit2D Linecast(Vector2 start, Vector2 end, int layerMask)`
  （RaycastHit2D Linecast（二维向量 start, 二维向量 end, int layerMask））
- `RaycastHit2D Raycast(Vector2 origin, Vector2 direction)`
  （RaycastHit2D Raycast（二维向量 origin, 二维向量 direction））
- `RaycastHit2D Raycast(Vector2 origin, Vector2 direction, float distance)`
  （RaycastHit2D Raycast（二维向量 origin, 二维向量 direction, float distance））
- `RaycastHit2D Raycast(Vector2 origin, Vector2 direction, float distance, int layerMask)`
  （RaycastHit2D Raycast（二维向量 origin, 二维向量 direction, float distance, int layerMask））
- `RaycastHit2D Raycast(Vector2 origin, Vector2 direction, float distance, int layerMask, float minDepth)`
  （RaycastHit2D Raycast（二维向量 origin, 二维向量 direction, float distance, int layerMask, float minDepth））
- `RaycastHit2D Raycast(Vector2 origin, Vector2 direction, float distance, int layerMask, float minDepth, float maxDepth)`
  （RaycastHit2D Raycast（二维向量 origin, 二维向量 direction, float distance, int layerMask, float minDepth, float maxDepth））
- `int Raycast(Vector2 origin, Vector2 direction, ContactFilter2D contactFilter, RaycastHit2D[] results)`
  （int Raycast（二维向量 origin, 二维向量 direction, ContactFilter2D contactFilter, RaycastHit2D[] results））
- `int Raycast(Vector2 origin, Vector2 direction, ContactFilter2D contactFilter, RaycastHit2D[] results, float distance)`
  （int Raycast（二维向量 origin, 二维向量 direction, ContactFilter2D contactFilter, RaycastHit2D[] results, float distance））
- `int Raycast(Vector2 origin, Vector2 direction, ContactFilter2D contactFilter, List<RaycastHit2D> results, float distance = ∞)`
  （int Raycast（二维向量 origin, 二维向量 direction, ContactFilter2D contactFilter, List<RaycastHit2D> results, float distance = ∞））
- `RaycastHit2D CircleCast(Vector2 origin, float radius, Vector2 direction, float distance, int layerMask)`
  （RaycastHit2D CircleCast（二维向量 origin, float radius, 二维向量 direction, float distance, int layerMask））
- `RaycastHit2D[] GetRayIntersectionAll(Ray ray)`
  （RaycastHit2D[] 获取RayIntersection所有（Ray ray））
- `RaycastHit2D[] GetRayIntersectionAll(Ray ray, float distance)`
  （RaycastHit2D[] 获取RayIntersection所有（Ray ray, float distance））
- `RaycastHit2D[] GetRayIntersectionAll(Ray ray, float distance, int layerMask)`
  （RaycastHit2D[] 获取RayIntersection所有（Ray ray, float distance, int layerMask））
- `RaycastHit2D[] GetRayIntersectionAll_Internal(PhysicsScene2D physicsScene, Vector3 origin, Vector3 direction, float distance, int layerMask)`
  （RaycastHit2D[] 获取RayIntersectionAll_内部的（物理Scene2D physicsScene, 三维向量 origin, 三维向量 direction, float distance, int layerMask））
- `int GetRayIntersectionNonAlloc(Ray ray, RaycastHit2D[] results)`
  （int 获取RayIntersectionNonAlloc（Ray ray, RaycastHit2D[] results））
- `int GetRayIntersectionNonAlloc(Ray ray, RaycastHit2D[] results, float distance)`
  （int 获取RayIntersectionNonAlloc（Ray ray, RaycastHit2D[] results, float distance））
- `int GetRayIntersectionNonAlloc(Ray ray, RaycastHit2D[] results, float distance, int layerMask)`
  （int 获取RayIntersectionNonAlloc（Ray ray, RaycastHit2D[] results, float distance, int layerMask））
- `Collider2D OverlapPoint(Vector2 point, int layerMask)`
  （Collider2D OverlapPoint（二维向量 point, int layerMask））
- `Collider2D OverlapCircle(Vector2 point, float radius, int layerMask)`
  （Collider2D OverlapCircle（二维向量 point, float radius, int layerMask））
- `RaycastHit2D[] GetRayIntersectionAll_Internal_Injected(ref PhysicsScene2D physicsScene, ref Vector3 origin, ref Vector3 direction, float distance, int layerMask)`
  （RaycastHit2D[] 获取RayIntersectionAll_Internal_Injected（ref PhysicsScene2D physicsScene, ref Vector3 origin, ref Vector3 direction, float distance, int layerMask））

---

## Physics2DRaycaster（Physics2DRaycaster）

**继承**: PhysicsRaycaster（物理Raycaster）

### 字段 (1)

- `RaycastHit2D[] m_Hits`（RaycastHit2D[] m_Hits）(偏移: 0x24)

### 方法 (1)

- `void Raycast(PointerEventData eventData, List<RaycastResult> resultAppendList)`
  （void Raycast（指针事件数据 eventData, List<RaycastResult> resultAppendList））

---

## PhysicsRaycaster（物理Raycaster）

**继承**: BaseRaycaster（基础Raycaster）

### 字段 (5)

- `Camera m_EventCamera`（摄像机 m_事件摄像机）(偏移: 0x10)
- `LayerMask m_EventMask`（层掩码 m_事件掩码）(偏移: 0x14)
- `int m_MaxRayIntersections`（int m_最大RayIntersections）(偏移: 0x18)
- `int m_LastMaxRayIntersections`（int m_最后一个最大RayIntersections）(偏移: 0x1C)
- `RaycastHit[] m_Hits`（RaycastHit[] m_Hits）(偏移: 0x20)

### 方法 (9)

- `Camera get_eventCamera()`
  （摄像机 get_event摄像机（））
- `int get_depth()`
  （int get_depth（））
- `int get_finalEventMask()`
  （int get_final事件掩码（））
- `LayerMask get_eventMask()`
  （层掩码 get_event掩码（））
- `void set_eventMask(LayerMask value)`
  （void set_event掩码（层掩码 value））
- `int get_maxRayIntersections()`
  （int get_maxRayIntersections（））
- `void set_maxRayIntersections(int value)`
  （void set_maxRayIntersections（int value））
- `bool ComputeRayAndDistance(PointerEventData eventData, ref Ray ray, ref int eventDisplayIndex, ref float distanceToClipPlane)`
  （bool ComputeRayAnd距离（指针事件数据 eventData, ref Ray ray, ref int eventDisplayIndex, ref float distanceToClipPlane））
- `void Raycast(PointerEventData eventData, List<RaycastResult> resultAppendList)`
  （void Raycast（指针事件数据 eventData, List<RaycastResult> resultAppendList））

---

## PhysicsRaycaster.RaycastHitComparer（物理Raycaster.Raycast命中Comparer）

**继承**: IComparer<RaycastHit>（IComparer<RaycastHit>）

### 字段 (1)

- `PhysicsRaycaster.RaycastHitComparer instance`（物理Raycaster.Raycast命中Comparer instance）(偏移: 0x0)

### 方法 (1)

- `int Compare(RaycastHit x, RaycastHit y)`
  （int Compare（Raycast命中 x, Raycast命中 y））

---

## PhysicsScene（物理场景）

**继承**: IEquatable<PhysicsScene>（IEquatable<物理Scene>）

### 字段 (1)

- `int m_Handle`（int m_句柄）(偏移: 0x0)

### 方法 (27)

- `string ToString()`
  （string To字符串（））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool Equals(object other)`
  （bool Equals（object other））
- `bool Equals(PhysicsScene other)`
  （bool Equals（物理场景 other））
- `bool Raycast(Vector3 origin, Vector3 direction, float maxDistance = ∞, int layerMask = -5, QueryTriggerInteraction queryTriggerInteraction = 0)`
  （bool Raycast（三维向量 origin, 三维向量 direction, float maxDistance = ∞, int layerMask = -5, Query触发器Interaction queryTriggerInteraction = 0））
- `bool Internal_RaycastTest(PhysicsScene physicsScene, Ray ray, float maxDistance, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool Internal_RaycastTest（物理场景 physicsScene, Ray ray, float maxDistance, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool Raycast(Vector3 origin, Vector3 direction, out RaycastHit hitInfo, float maxDistance = ∞, int layerMask = -5, QueryTriggerInteraction queryTriggerInteraction = 0)`
  （bool Raycast（三维向量 origin, 三维向量 direction, out RaycastHit hitInfo, float maxDistance = ∞, int layerMask = -5, Query触发器Interaction queryTriggerInteraction = 0））
- `bool Internal_Raycast(PhysicsScene physicsScene, Ray ray, float maxDistance, ref RaycastHit hit, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool Internal_Raycast（物理场景 physicsScene, Ray ray, float maxDistance, ref RaycastHit hit, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `int Raycast(Vector3 origin, Vector3 direction, RaycastHit[] raycastHits, float maxDistance = ∞, int layerMask = -5, QueryTriggerInteraction queryTriggerInteraction = 0)`
  （int Raycast（三维向量 origin, 三维向量 direction, RaycastHit[] raycastHits, float maxDistance = ∞, int layerMask = -5, Query触发器Interaction queryTriggerInteraction = 0））
- `int Internal_RaycastNonAlloc(PhysicsScene physicsScene, Ray ray, RaycastHit[] raycastHits, float maxDistance, int mask, QueryTriggerInteraction queryTriggerInteraction)`
  （int Internal_RaycastNonAlloc（物理场景 physicsScene, Ray ray, RaycastHit[] raycastHits, float maxDistance, int mask, Query触发器Interaction queryTriggerInteraction））
- `bool Query_CapsuleCast(PhysicsScene physicsScene, Vector3 point1, Vector3 point2, float radius, Vector3 direction, float maxDistance, ref RaycastHit hitInfo, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool Query_CapsuleCast（物理场景 physicsScene, 三维向量 point1, 三维向量 point2, float radius, 三维向量 direction, float maxDistance, ref RaycastHit hitInfo, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool Internal_CapsuleCast(PhysicsScene physicsScene, Vector3 point1, Vector3 point2, float radius, Vector3 direction, out RaycastHit hitInfo, float maxDistance, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool Internal_CapsuleCast（物理场景 physicsScene, 三维向量 point1, 三维向量 point2, float radius, 三维向量 direction, out RaycastHit hitInfo, float maxDistance, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool CapsuleCast(Vector3 point1, Vector3 point2, float radius, Vector3 direction, out RaycastHit hitInfo, float maxDistance = ∞, int layerMask = -5, QueryTriggerInteraction queryTriggerInteraction = 0)`
  （bool CapsuleCast（三维向量 point1, 三维向量 point2, float radius, 三维向量 direction, out RaycastHit hitInfo, float maxDistance = ∞, int layerMask = -5, Query触发器Interaction queryTriggerInteraction = 0））
- `bool Query_SphereCast(PhysicsScene physicsScene, Vector3 origin, float radius, Vector3 direction, float maxDistance, ref RaycastHit hitInfo, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool Query_SphereCast（物理场景 physicsScene, 三维向量 origin, float radius, 三维向量 direction, float maxDistance, ref RaycastHit hitInfo, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool Internal_SphereCast(PhysicsScene physicsScene, Vector3 origin, float radius, Vector3 direction, out RaycastHit hitInfo, float maxDistance, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool Internal_SphereCast（物理场景 physicsScene, 三维向量 origin, float radius, 三维向量 direction, out RaycastHit hitInfo, float maxDistance, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool SphereCast(Vector3 origin, float radius, Vector3 direction, out RaycastHit hitInfo, float maxDistance = ∞, int layerMask = -5, QueryTriggerInteraction queryTriggerInteraction = 0)`
  （bool SphereCast（三维向量 origin, float radius, 三维向量 direction, out RaycastHit hitInfo, float maxDistance = ∞, int layerMask = -5, Query触发器Interaction queryTriggerInteraction = 0））
- `int Internal_SphereCastNonAlloc(PhysicsScene physicsScene, Vector3 origin, float radius, Vector3 direction, RaycastHit[] raycastHits, float maxDistance, int mask, QueryTriggerInteraction queryTriggerInteraction)`
  （int Internal_SphereCastNonAlloc（物理场景 physicsScene, 三维向量 origin, float radius, 三维向量 direction, RaycastHit[] raycastHits, float maxDistance, int mask, Query触发器Interaction queryTriggerInteraction））
- `int SphereCast(Vector3 origin, float radius, Vector3 direction, RaycastHit[] results, float maxDistance = ∞, int layerMask = -5, QueryTriggerInteraction queryTriggerInteraction = 0)`
  （int SphereCast（三维向量 origin, float radius, 三维向量 direction, RaycastHit[] results, float maxDistance = ∞, int layerMask = -5, Query触发器Interaction queryTriggerInteraction = 0））
- `int OverlapSphereNonAlloc_Internal(PhysicsScene physicsScene, Vector3 position, float radius, Collider[] results, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （int OverlapSphereNonAlloc_内部的（物理场景 physicsScene, 三维向量 position, float radius, Collider[] results, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `int OverlapSphere(Vector3 position, float radius, Collider[] results, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （int OverlapSphere（三维向量 position, float radius, Collider[] results, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool Internal_RaycastTest_Injected(ref PhysicsScene physicsScene, ref Ray ray, float maxDistance, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool Internal_RaycastTest_Injected（ref PhysicsScene physicsScene, ref Ray ray, float maxDistance, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool Internal_Raycast_Injected(ref PhysicsScene physicsScene, ref Ray ray, float maxDistance, ref RaycastHit hit, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool Internal_Raycast_Injected（ref PhysicsScene physicsScene, ref Ray ray, float maxDistance, ref RaycastHit hit, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `int Internal_RaycastNonAlloc_Injected(ref PhysicsScene physicsScene, ref Ray ray, RaycastHit[] raycastHits, float maxDistance, int mask, QueryTriggerInteraction queryTriggerInteraction)`
  （int Internal_RaycastNonAlloc_Injected（ref PhysicsScene physicsScene, ref Ray ray, RaycastHit[] raycastHits, float maxDistance, int mask, Query触发器Interaction queryTriggerInteraction））
- `bool Query_CapsuleCast_Injected(ref PhysicsScene physicsScene, ref Vector3 point1, ref Vector3 point2, float radius, ref Vector3 direction, float maxDistance, ref RaycastHit hitInfo, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool Query_CapsuleCast_Injected（ref PhysicsScene physicsScene, ref Vector3 point1, ref Vector3 point2, float radius, ref Vector3 direction, float maxDistance, ref RaycastHit hitInfo, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `bool Query_SphereCast_Injected(ref PhysicsScene physicsScene, ref Vector3 origin, float radius, ref Vector3 direction, float maxDistance, ref RaycastHit hitInfo, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （bool Query_SphereCast_Injected（ref PhysicsScene physicsScene, ref Vector3 origin, float radius, ref Vector3 direction, float maxDistance, ref RaycastHit hitInfo, int layerMask, Query触发器Interaction queryTriggerInteraction））
- `int Internal_SphereCastNonAlloc_Injected(ref PhysicsScene physicsScene, ref Vector3 origin, float radius, ref Vector3 direction, RaycastHit[] raycastHits, float maxDistance, int mask, QueryTriggerInteraction queryTriggerInteraction)`
  （int Internal_SphereCastNonAlloc_Injected（ref PhysicsScene physicsScene, ref Vector3 origin, float radius, ref Vector3 direction, RaycastHit[] raycastHits, float maxDistance, int mask, Query触发器Interaction queryTriggerInteraction））
- `int OverlapSphereNonAlloc_Internal_Injected(ref PhysicsScene physicsScene, ref Vector3 position, float radius, Collider[] results, int layerMask, QueryTriggerInteraction queryTriggerInteraction)`
  （int OverlapSphereNonAlloc_Internal_Injected（ref PhysicsScene physicsScene, ref Vector3 position, float radius, Collider[] results, int layerMask, Query触发器Interaction queryTriggerInteraction））

---

## PhysicsScene2D（物理Scene2D）

**继承**: IEquatable<PhysicsScene2D>（IEquatable<物理Scene2D>）

### 字段 (1)

- `int m_Handle`（int m_句柄）(偏移: 0x0)

### 方法 (29)

- `string ToString()`
  （string To字符串（））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool Equals(object other)`
  （bool Equals（object other））
- `bool Equals(PhysicsScene2D other)`
  （bool Equals（物理Scene2D other））
- `RaycastHit2D Linecast(Vector2 start, Vector2 end, ContactFilter2D contactFilter)`
  （RaycastHit2D Linecast（二维向量 start, 二维向量 end, ContactFilter2D contactFilter））
- `RaycastHit2D Linecast_Internal(PhysicsScene2D physicsScene, Vector2 start, Vector2 end, ContactFilter2D contactFilter)`
  （RaycastHit2D Linecast_内部的（物理Scene2D physicsScene, 二维向量 start, 二维向量 end, ContactFilter2D contactFilter））
- `RaycastHit2D Raycast(Vector2 origin, Vector2 direction, float distance, int layerMask = -5)`
  （RaycastHit2D Raycast（二维向量 origin, 二维向量 direction, float distance, int layerMask = -5））
- `RaycastHit2D Raycast(Vector2 origin, Vector2 direction, float distance, ContactFilter2D contactFilter)`
  （RaycastHit2D Raycast（二维向量 origin, 二维向量 direction, float distance, ContactFilter2D contactFilter））
- `RaycastHit2D Raycast_Internal(PhysicsScene2D physicsScene, Vector2 origin, Vector2 direction, float distance, ContactFilter2D contactFilter)`
  （RaycastHit2D Raycast_内部的（物理Scene2D physicsScene, 二维向量 origin, 二维向量 direction, float distance, ContactFilter2D contactFilter））
- `int Raycast(Vector2 origin, Vector2 direction, float distance, ContactFilter2D contactFilter, RaycastHit2D[] results)`
  （int Raycast（二维向量 origin, 二维向量 direction, float distance, ContactFilter2D contactFilter, RaycastHit2D[] results））
- `int RaycastArray_Internal(PhysicsScene2D physicsScene, Vector2 origin, Vector2 direction, float distance, ContactFilter2D contactFilter, RaycastHit2D[] results)`
  （int RaycastArray_内部的（物理Scene2D physicsScene, 二维向量 origin, 二维向量 direction, float distance, ContactFilter2D contactFilter, RaycastHit2D[] results））
- `int Raycast(Vector2 origin, Vector2 direction, float distance, ContactFilter2D contactFilter, List<RaycastHit2D> results)`
  （int Raycast（二维向量 origin, 二维向量 direction, float distance, ContactFilter2D contactFilter, List<RaycastHit2D> results））
- `int RaycastList_Internal(PhysicsScene2D physicsScene, Vector2 origin, Vector2 direction, float distance, ContactFilter2D contactFilter, List<RaycastHit2D> results)`
  （int RaycastList_内部的（物理Scene2D physicsScene, 二维向量 origin, 二维向量 direction, float distance, ContactFilter2D contactFilter, List<RaycastHit2D> results））
- `RaycastHit2D CircleCast(Vector2 origin, float radius, Vector2 direction, float distance, ContactFilter2D contactFilter)`
  （RaycastHit2D CircleCast（二维向量 origin, float radius, 二维向量 direction, float distance, ContactFilter2D contactFilter））
- `RaycastHit2D CircleCast_Internal(PhysicsScene2D physicsScene, Vector2 origin, float radius, Vector2 direction, float distance, ContactFilter2D contactFilter)`
  （RaycastHit2D CircleCast_内部的（物理Scene2D physicsScene, 二维向量 origin, float radius, 二维向量 direction, float distance, ContactFilter2D contactFilter））
- `int GetRayIntersection(Ray ray, float distance, RaycastHit2D[] results, int layerMask = -5)`
  （int 获取RayIntersection（Ray ray, float distance, RaycastHit2D[] results, int layerMask = -5））
- `int GetRayIntersectionArray_Internal(PhysicsScene2D physicsScene, Vector3 origin, Vector3 direction, float distance, int layerMask, RaycastHit2D[] results)`
  （int 获取RayIntersectionArray_内部的（物理Scene2D physicsScene, 三维向量 origin, 三维向量 direction, float distance, int layerMask, RaycastHit2D[] results））
- `Collider2D OverlapPoint(Vector2 point, ContactFilter2D contactFilter)`
  （Collider2D OverlapPoint（二维向量 point, ContactFilter2D contactFilter））
- `Collider2D OverlapPoint_Internal(PhysicsScene2D physicsScene, Vector2 point, ContactFilter2D contactFilter)`
  （Collider2D OverlapPoint_内部的（物理Scene2D physicsScene, 二维向量 point, ContactFilter2D contactFilter））
- `Collider2D OverlapCircle(Vector2 point, float radius, ContactFilter2D contactFilter)`
  （Collider2D OverlapCircle（二维向量 point, float radius, ContactFilter2D contactFilter））
- `Collider2D OverlapCircle_Internal(PhysicsScene2D physicsScene, Vector2 point, float radius, ContactFilter2D contactFilter)`
  （Collider2D OverlapCircle_内部的（物理Scene2D physicsScene, 二维向量 point, float radius, ContactFilter2D contactFilter））
- `void Linecast_Internal_Injected(ref PhysicsScene2D physicsScene, ref Vector2 start, ref Vector2 end, ref ContactFilter2D contactFilter, out RaycastHit2D ret)`
  （void Linecast_Internal_Injected（ref PhysicsScene2D physicsScene, ref Vector2 start, ref Vector2 end, ref ContactFilter2D contactFilter, out RaycastHit2D ret））
- `void Raycast_Internal_Injected(ref PhysicsScene2D physicsScene, ref Vector2 origin, ref Vector2 direction, float distance, ref ContactFilter2D contactFilter, out RaycastHit2D ret)`
  （void Raycast_Internal_Injected（ref PhysicsScene2D physicsScene, ref Vector2 origin, ref Vector2 direction, float distance, ref ContactFilter2D contactFilter, out RaycastHit2D ret））
- `int RaycastArray_Internal_Injected(ref PhysicsScene2D physicsScene, ref Vector2 origin, ref Vector2 direction, float distance, ref ContactFilter2D contactFilter, RaycastHit2D[] results)`
  （int RaycastArray_Internal_Injected（ref PhysicsScene2D physicsScene, ref Vector2 origin, ref Vector2 direction, float distance, ref ContactFilter2D contactFilter, RaycastHit2D[] results））
- `int RaycastList_Internal_Injected(ref PhysicsScene2D physicsScene, ref Vector2 origin, ref Vector2 direction, float distance, ref ContactFilter2D contactFilter, List<RaycastHit2D> results)`
  （int RaycastList_Internal_Injected（ref PhysicsScene2D physicsScene, ref Vector2 origin, ref Vector2 direction, float distance, ref ContactFilter2D contactFilter, List<RaycastHit2D> results））
- `void CircleCast_Internal_Injected(ref PhysicsScene2D physicsScene, ref Vector2 origin, float radius, ref Vector2 direction, float distance, ref ContactFilter2D contactFilter, out RaycastHit2D ret)`
  （void CircleCast_Internal_Injected（ref PhysicsScene2D physicsScene, ref Vector2 origin, float radius, ref Vector2 direction, float distance, ref ContactFilter2D contactFilter, out RaycastHit2D ret））
- `int GetRayIntersectionArray_Internal_Injected(ref PhysicsScene2D physicsScene, ref Vector3 origin, ref Vector3 direction, float distance, int layerMask, RaycastHit2D[] results)`
  （int 获取RayIntersectionArray_Internal_Injected（ref PhysicsScene2D physicsScene, ref Vector3 origin, ref Vector3 direction, float distance, int layerMask, RaycastHit2D[] results））
- `Collider2D OverlapPoint_Internal_Injected(ref PhysicsScene2D physicsScene, ref Vector2 point, ref ContactFilter2D contactFilter)`
  （Collider2D OverlapPoint_Internal_Injected（ref PhysicsScene2D physicsScene, ref Vector2 point, ref ContactFilter2D contactFilter））
- `Collider2D OverlapCircle_Internal_Injected(ref PhysicsScene2D physicsScene, ref Vector2 point, float radius, ref ContactFilter2D contactFilter)`
  （Collider2D OverlapCircle_Internal_Injected（ref PhysicsScene2D physicsScene, ref Vector2 point, float radius, ref ContactFilter2D contactFilter））

---

## PinnedBufferMemoryStream（Pinned缓冲区Memory流）

**继承**: UnmanagedMemoryStream（UnmanagedMemory流）

### 字段 (2)

- `byte[] _array`（byte[] _array）(偏移: 0x48)
- `GCHandle _pinningHandle`（GC句柄 _pinning句柄）(偏移: 0x4C)

### 方法 (2)

- `void Finalize()`
  （void Finalize（））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））

---

## PipelineDebugLevel（PipelineDebug等级）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## PixelPerfectBackgroundPass（PixelPerfectBackgroundPass）

**继承**: ScriptableRenderPass（ScriptableRenderPass）

### 字段 (1)

- `ProfilingSampler m_ProfilingScope`（ProfilingSampler m_Profiling瞄准镜）(偏移: 0x37B73795)

### 方法 (1)

- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（ScriptableRenderContext context, ref RenderingData renderingData））

---

## PixelPerfectCamera（PixelPerfect摄像机）

**继承**: MonoBehaviour, IPixelPerfectCamera（MonoBehaviour行为, IPixelPerfect摄像机）

### 字段 (11)

- `int m_AssetsPPU`（int m_AssetsPPU）(偏移: 0xC)
- `int m_RefResolutionX`（int m_RefResolutionX）(偏移: 0x10)
- `int m_RefResolutionY`（int m_RefResolutionY）(偏移: 0x14)
- `bool m_UpscaleRT`（bool m_UpscaleRT）(偏移: 0x18)
- `bool m_PixelSnapping`（bool m_PixelSnapping）(偏移: 0x0)
- `bool m_CropFrameX`（bool m_CropFrameX）(偏移: 0x0)
- `bool m_CropFrameY`（bool m_CropFrameY）(偏移: 0x0)
- `bool m_StretchFill`（bool m_StretchFill）(偏移: 0x0)
- `Camera m_Camera`（摄像机 m_摄像机）(偏移: 0x20)
- `PixelPerfectCameraInternal m_Internal`（PixelPerfect摄像机内部的 m_内部的）(偏移: 0x24)
- `bool m_CinemachineCompatibilityMode`（bool m_CinemachineCompatibility模式）(偏移: 0x28)

### 方法 (30)

- `int get_assetsPPU()`
  （int get_assetsPPU（））
- `void set_assetsPPU(int value)`
  （void set_assetsPPU（int value））
- `int get_refResolutionX()`
  （int get_refResolutionX（））
- `void set_refResolutionX(int value)`
  （void set_refResolutionX（int value））
- `int get_refResolutionY()`
  （int get_refResolutionY（））
- `void set_refResolutionY(int value)`
  （void set_refResolutionY（int value））
- `bool get_upscaleRT()`
  （bool get_upscaleRT（））
- `void set_upscaleRT(bool value)`
  （void set_upscaleRT（bool value））
- `bool get_pixelSnapping()`
  （bool get_pixelSnapping（））
- `void set_pixelSnapping(bool value)`
  （void set_pixelSnapping（bool value））
- `bool get_cropFrameX()`
  （bool get_cropFrameX（））
- `void set_cropFrameX(bool value)`
  （void set_cropFrameX（bool value））
- `bool get_cropFrameY()`
  （bool get_cropFrameY（））
- `void set_cropFrameY(bool value)`
  （void set_cropFrameY（bool value））
- `bool get_stretchFill()`
  （bool get_stretchFill（））
- `void set_stretchFill(bool value)`
  （void set_stretchFill（bool value））
- `int get_pixelRatio()`
  （int get_pixel比率（））
- `Vector3 RoundToPixel(Vector3 position)`
  （三维向量 回合ToPixel（三维向量 position））
- `float CorrectCinemachineOrthoSize(float targetOrthoSize)`
  （float CorrectCinemachineOrtho大小（float targetOrthoSize））
- `bool get_isRunning()`
  （bool get_isRunning（））
- `FilterMode get_finalBlitFilterMode()`
  （Filter模式 get_finalBlitFilter模式（））
- `Vector2Int get_offscreenRTSize()`
  （二维向量整数 get_offscreenRT大小（））
- `Vector2Int get_cameraRTSize()`
  （二维向量整数 get_cameraRT大小（））
- `void PixelSnap()`
  （void PixelSnap（））
- `void Awake()`
  （void Awake（））
- `void OnBeginFrameRendering(ScriptableRenderContext context, Camera[] cameras)`
  （void OnBeginFrameRendering（ScriptableRenderContext context, Camera[] cameras））
- `void OnBeginCameraRendering(ScriptableRenderContext context, Camera camera)`
  （void OnBegin摄像机Rendering（ScriptableRenderContext context, 摄像机 camera））
- `void OnEndCameraRendering(ScriptableRenderContext context, Camera camera)`
  （void On结束摄像机Rendering（ScriptableRenderContext context, 摄像机 camera））
- `void OnEnable()`
  （void On启用（））
- `void OnDisable()`
  （void On禁用（））

---

## PixelPerfectCameraInternal（PixelPerfect摄像机内部的）

**继承**: ISerializationCallbackReceiver（ISerialization回调Receiver）

### 字段 (15)

- `IPixelPerfectCamera m_Component`（IPixelPerfect摄像机 m_组件）(偏移: 0x8)
- `PixelPerfectCamera m_SerializableComponent`（PixelPerfect摄像机 m_Serializable组件）(偏移: 0xC)
- `float originalOrthoSize`（float originalOrtho大小）(偏移: 0x10)
- `bool hasPostProcessLayer`（bool hasPost处理层）(偏移: 0x14)
- `bool cropFrameXAndY`（bool cropFrameXAndY）(偏移: 0x0)
- `bool cropFrameXOrY`（bool cropFrameXOrY）(偏移: 0x0)
- `bool useStretchFill`（bool useStretchFill）(偏移: 0x0)
- `int zoom`（int zoom）(偏移: 0x0)
- `bool useOffscreenRT`（bool useOffscreenRT）(偏移: 0x1C)
- `int offscreenRTWidth`（int offscreenRT宽度）(偏移: 0x20)
- `int offscreenRTHeight`（int offscreenRT高度）(偏移: 0x24)
- `Rect pixelRect`（Rect pixelRect）(偏移: 0x28)
- `float orthoSize`（float ortho大小）(偏移: 0x38)
- `float unitsPerPixel`（float unitsPerPixel）(偏移: 0x3C)
- `int cinemachineVCamZoom`（int cinemachineVCam瞄准）(偏移: 0x40)

### 方法 (5)

- `void OnBeforeSerialize()`
  （void OnBeforeSerialize（））
- `void OnAfterDeserialize()`
  （void OnAfterDeserialize（））
- `void CalculateCameraProperties(int screenWidth, int screenHeight)`
  （void 计算摄像机Properties（int screenWidth, int screenHeight））
- `Rect CalculateFinalBlitPixelRect(int screenWidth, int screenHeight)`
  （Rect 计算FinalBlitPixelRect（int screenWidth, int screenHeight））
- `float CorrectCinemachineOrthoSize(float targetOrthoSize)`
  （float CorrectCinemachineOrtho大小（float targetOrthoSize））

---

## PixelPerfectRendering（PixelPerfectRendering）

### 方法 (1)

- `void set_pixelSnapSpacing(float value)`
  （void set_pixelSnapSpacing（float value））

---

## Plane（Plane）

**继承**: IFormattable（IFormattable）

### 字段 (2)

- `Vector3 m_Normal`（三维向量 m_法线）(偏移: 0x0)
- `float m_Distance`（float m_距离）(偏移: 0xC)

### 方法 (5)

- `Vector3 get_normal()`
  （三维向量 get_normal（））
- `float get_distance()`
  （float get_distance（））
- `bool Raycast(Ray ray, out float enter)`
  （bool Raycast（Ray ray, out float enter））
- `string ToString()`
  （string To字符串（））
- `string ToString(string format, IFormatProvider formatProvider)`
  （string To字符串（string format, I格式化提供者 formatProvider））

---

## PlatformHelper（Platform辅助器）

### 字段 (2)

- `int s_processorCount`（int s_processor数量）(偏移: 0x0)
- `int s_lastProcessorCountRefreshTicks`（int s_lastProcessor数量刷新Ticks）(偏移: 0x4)

### 方法 (2)

- `int get_ProcessorCount()`
  （int get_Processor数量（））
- `bool get_IsSingleProcessor()`
  （bool get_是否单个Processor（））

---

## PlatformID（PlatformID）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## PlayMode（播放模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## PlayState（播放状态）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Playable（Playable）

**继承**: IPlayable, IEquatable<Playable>（IPlayable, IEquatable<Playable>）

### 字段 (2)

- `PlayableHandle m_Handle`（Playable句柄 m_句柄）(偏移: 0x0)
- `Playable m_NullPlayable`（Playable m_NullPlayable）(偏移: 0x0)

### 方法 (5)

- `Playable get_Null()`
  （Playable get_Null（））
- `Playable Create(PlayableGraph graph, int inputCount = 0)`
  （Playable 创建（PlayableGraph graph, int inputCount = 0））
- `PlayableHandle GetHandle()`
  （Playable句柄 获取句柄（））
- `Type GetPlayableType()`
  （类型 获取Playable类型（））
- `bool Equals(Playable other)`
  （bool Equals（Playable other））

---

## PlayableAsset（Playable资产）

**继承**: ScriptableObject, IPlayableAsset（脚本对象, IPlayable资产）

### 方法 (4)

- `double get_duration()`
  （double get_duration（））
- `IEnumerable<PlayableBinding> get_outputs()`
  （IEnumerable<PlayableBinding> get_outputs（））
- `void Internal_CreatePlayable(PlayableAsset asset, PlayableGraph graph, GameObject go, IntPtr ptr)`
  （void Internal_创建Playable（Playable资产 asset, PlayableGraph graph, 游戏对象 go, 整数Ptr ptr））
- `void Internal_GetPlayableAssetDuration(PlayableAsset asset, IntPtr ptrToDouble)`
  （void Internal_获取Playable资产持续时间（Playable资产 asset, 整数Ptr ptrToDouble））

---

## PlayableBehaviour（PlayableBehaviour）

**继承**: IPlayableBehaviour, ICloneable（IPlayableBehaviour, ICloneable）

### 方法 (9)

- `void OnGraphStart(Playable playable)`
  （void OnGraph开始（Playable playable））
- `void OnGraphStop(Playable playable)`
  （void OnGraph停止（Playable playable））
- `void OnPlayableCreate(Playable playable)`
  （void OnPlayable创建（Playable playable））
- `void OnPlayableDestroy(Playable playable)`
  （void OnPlayable销毁（Playable playable））
- `void OnBehaviourPlay(Playable playable, FrameData info)`
  （void OnBehaviour播放（Playable playable, Frame数据 info））
- `void OnBehaviourPause(Playable playable, FrameData info)`
  （void OnBehaviour暂停（Playable playable, Frame数据 info））
- `void PrepareFrame(Playable playable, FrameData info)`
  （void PrepareFrame（Playable playable, Frame数据 info））
- `void ProcessFrame(Playable playable, FrameData info, object playerData)`
  （void 处理Frame（Playable playable, Frame数据 info, object playerData））
- `object Clone()`
  （object 克隆（））

---

## PlayableBinding（PlayableBinding）

### 字段 (6)

- `string m_StreamName`（string m_流名称）(偏移: 0x0)
- `Object m_SourceObject`（对象 m_Source对象）(偏移: 0x4)
- `Type m_SourceBindingType`（类型 m_SourceBinding类型）(偏移: 0x8)
- `PlayableBinding.CreateOutputMethod m_CreateOutputMethod`（PlayableBinding.创建OutputMethod m_创建OutputMethod）(偏移: 0xC)
- `PlayableBinding[] None`（PlayableBinding[] 无）(偏移: 0x0)
- `double DefaultDuration`（double 默认的持续时间）(偏移: 0x8)

### 方法 (3)

- `Object get_sourceObject()`
  （对象 get_source对象（））
- `PlayableOutput CreateOutput(PlayableGraph graph)`
  （PlayableOutput 创建Output（PlayableGraph graph））
- `PlayableBinding CreateInternal(string name, Object sourceObject, Type sourceType, PlayableBinding.CreateOutputMethod createFunction)`
  （PlayableBinding 创建内部的（string name, 对象 sourceObject, 类型 sourceType, PlayableBinding.创建OutputMethod createFunction））

---

## PlayableBinding.CreateOutputMethod（PlayableBinding.创建OutputMethod）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `PlayableOutput Invoke(PlayableGraph graph, string name)`
  （PlayableOutput Invoke（PlayableGraph graph, string name））
- `IAsyncResult BeginInvoke(PlayableGraph graph, string name, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（PlayableGraph graph, string name, 异步回调 callback, object object））
- `PlayableOutput EndInvoke(IAsyncResult result)`
  （PlayableOutput 结束Invoke（I异步Result result））

---

## PlayableDirector（PlayableDirector）

**继承**: Behaviour, IExposedPropertyTable（Behaviour, IExposed属性Table）

### 字段 (3)

- `Action<PlayableDirector> played`（Action<PlayableDirector> played）(偏移: 0xC)
- `Action<PlayableDirector> paused`（Action<PlayableDirector> paused）(偏移: 0x10)
- `Action<PlayableDirector> stopped`（Action<PlayableDirector> stopped）(偏移: 0x14)

### 方法 (15)

- `DirectorWrapMode get_extrapolationMode()`
  （DirectorWrap模式 get_extrapolation模式（））
- `PlayableAsset get_playableAsset()`
  （Playable资产 get_playable资产（））
- `void set_time(double value)`
  （void set_time（double value））
- `double get_time()`
  （double get_time（））
- `double get_duration()`
  （double get_duration（））
- `void Play()`
  （void 播放（））
- `void Stop()`
  （void 停止（））
- `Object GetReferenceValue(PropertyName id, out bool idValid)`
  （对象 获取引用值（属性名称 id, out bool idValid））
- `Object GetGenericBinding(Object key)`
  （对象 获取GenericBinding（对象 key））
- `DirectorWrapMode GetWrapMode()`
  （DirectorWrap模式 获取Wrap模式（））
- `ScriptableObject Internal_GetPlayableAsset()`
  （脚本对象 Internal_获取Playable资产（））
- `void SendOnPlayableDirectorPlay()`
  （void 发送OnPlayableDirector播放（））
- `void SendOnPlayableDirectorPause()`
  （void 发送OnPlayableDirector暂停（））
- `void SendOnPlayableDirectorStop()`
  （void 发送OnPlayableDirector停止（））
- `Object GetReferenceValue_Injected(ref PropertyName id, out bool idValid)`
  （对象 获取引用Value_Injected（ref PropertyName id, out bool idValid））

---

## PlayableGraph（PlayableGraph）

### 字段 (2)

- `IntPtr m_Handle`（整数Ptr m_句柄）(偏移: 0x0)
- `uint m_Version`（uint m_Version）(偏移: 0x4)

### 方法 (12)

- `bool IsValid()`
  （bool 是否Valid（））
- `IExposedPropertyTable GetResolver()`
  （IExposed属性Table 获取Resolver（））
- `int GetPlayableCount()`
  （int 获取Playable数量（））
- `PlayableHandle CreatePlayableHandle()`
  （Playable句柄 创建Playable句柄（））
- `bool CreateScriptOutputInternal(string name, out PlayableOutputHandle handle)`
  （bool 创建ScriptOutput内部的（string name, out PlayableOutputHandle handle））
- `bool ConnectInternal(PlayableHandle source, int sourceOutputPort, PlayableHandle destination, int destinationInputPort)`
  （bool Connect内部的（Playable句柄 source, int sourceOutputPort, Playable句柄 destination, int destinationInputPort））
- `bool IsValid_Injected(ref PlayableGraph _unity_self)`
  （bool 是否Valid_Injected（ref PlayableGraph _unity_self））
- `IExposedPropertyTable GetResolver_Injected(ref PlayableGraph _unity_self)`
  （IExposed属性Table 获取Resolver_Injected（ref PlayableGraph _unity_self））
- `int GetPlayableCount_Injected(ref PlayableGraph _unity_self)`
  （int 获取PlayableCount_Injected（ref PlayableGraph _unity_self））
- `void CreatePlayableHandle_Injected(ref PlayableGraph _unity_self, out PlayableHandle ret)`
  （void 创建PlayableHandle_Injected（ref PlayableGraph _unity_self, out PlayableHandle ret））
- `bool CreateScriptOutputInternal_Injected(ref PlayableGraph _unity_self, string name, out PlayableOutputHandle handle)`
  （bool 创建ScriptOutputInternal_Injected（ref PlayableGraph _unity_self, string name, out PlayableOutputHandle handle））
- `bool ConnectInternal_Injected(ref PlayableGraph _unity_self, ref PlayableHandle source, int sourceOutputPort, ref PlayableHandle destination, int destinationInputPort)`
  （bool ConnectInternal_Injected（ref PlayableGraph _unity_self, ref PlayableHandle source, int sourceOutputPort, ref PlayableHandle destination, int destinationInputPort））

---

## PlayableHandle（Playable句柄）

**继承**: IEquatable<PlayableHandle>（IEquatable<PlayableHandle>）

### 字段 (3)

- `IntPtr m_Handle`（整数Ptr m_句柄）(偏移: 0x0)
- `uint m_Version`（uint m_Version）(偏移: 0x4)
- `PlayableHandle m_Null`（Playable句柄 m_Null）(偏移: 0x0)

### 方法 (57)

- `PlayableHandle get_Null()`
  （Playable句柄 get_Null（））
- `Playable GetInput(int inputPort)`
  （Playable 获取输入（int inputPort））
- `bool SetInputWeight(int inputIndex, float weight)`
  （bool 集合输入Weight（int inputIndex, float weight））
- `float GetInputWeight(int inputIndex)`
  （float 获取输入Weight（int inputIndex））
- `bool op_Equality(PlayableHandle x, PlayableHandle y)`
  （bool op_Equality（Playable句柄 x, Playable句柄 y））
- `bool Equals(object p)`
  （bool Equals（object p））
- `bool Equals(PlayableHandle other)`
  （bool Equals（Playable句柄 other））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool CompareVersion(PlayableHandle lhs, PlayableHandle rhs)`
  （bool CompareVersion（Playable句柄 lhs, Playable句柄 rhs））
- `bool CheckInputBounds(int inputIndex)`
  （bool 检查输入Bounds（int inputIndex））
- `bool CheckInputBounds(int inputIndex, bool acceptAny)`
  （bool 检查输入Bounds（int inputIndex, bool acceptAny））
- `bool IsValid()`
  （bool 是否Valid（））
- `Type GetPlayableType()`
  （类型 获取Playable类型（））
- `void SetScriptInstance(object scriptInstance)`
  （void 集合Script实例（object scriptInstance））
- `PlayState GetPlayState()`
  （播放状态 获取播放状态（））
- `void Play()`
  （void 播放（））
- `void Pause()`
  （void 暂停（））
- `void SetSpeed(double value)`
  （void 集合Speed（double value））
- `double GetTime()`
  （double 获取时间（））
- `void SetTime(double value)`
  （void 集合时间（double value））
- `bool IsDone()`
  （bool 是否Done（））
- `double GetDuration()`
  （double 获取持续时间（））
- `void SetDuration(double value)`
  （void 集合持续时间（double value））
- `void SetPropagateSetTime(bool value)`
  （void 集合Propagate集合时间（bool value））
- `int GetInputCount()`
  （int 获取输入数量（））
- `void SetInputCount(int value)`
  （void 集合输入数量（int value））
- `void SetInputWeight(PlayableHandle input, float weight)`
  （void 集合输入Weight（Playable句柄 input, float weight））
- `void SetTraversalMode(PlayableTraversalMode mode)`
  （void 集合Traversal模式（PlayableTraversal模式 mode））
- `DirectorWrapMode GetTimeWrapMode()`
  （DirectorWrap模式 获取时间Wrap模式（））
- `void SetTimeWrapMode(DirectorWrapMode mode)`
  （void 集合时间Wrap模式（DirectorWrap模式 mode））
- `object GetScriptInstance()`
  （object 获取Script实例（））
- `PlayableHandle GetInputHandle(int index)`
  （Playable句柄 获取输入句柄（int index））
- `void SetInputWeightFromIndex(int index, float weight)`
  （void 集合输入WeightFrom索引（int index, float weight））
- `float GetInputWeightFromIndex(int index)`
  （float 获取输入WeightFrom索引（int index））
- `bool IsValid_Injected(ref PlayableHandle _unity_self)`
  （bool 是否Valid_Injected（ref PlayableHandle _unity_self））
- `Type GetPlayableType_Injected(ref PlayableHandle _unity_self)`
  （类型 获取PlayableType_Injected（ref PlayableHandle _unity_self））
- `void SetScriptInstance_Injected(ref PlayableHandle _unity_self, object scriptInstance)`
  （void 集合ScriptInstance_Injected（ref PlayableHandle _unity_self, object scriptInstance））
- `PlayState GetPlayState_Injected(ref PlayableHandle _unity_self)`
  （播放状态 获取播放State_Injected（ref PlayableHandle _unity_self））
- `void Play_Injected(ref PlayableHandle _unity_self)`
  （void Play_Injected（ref PlayableHandle _unity_self））
- `void Pause_Injected(ref PlayableHandle _unity_self)`
  （void Pause_Injected（ref PlayableHandle _unity_self））
- `void SetSpeed_Injected(ref PlayableHandle _unity_self, double value)`
  （void 集合Speed_Injected（ref PlayableHandle _unity_self, double value））
- `double GetTime_Injected(ref PlayableHandle _unity_self)`
  （double 获取Time_Injected（ref PlayableHandle _unity_self））
- `void SetTime_Injected(ref PlayableHandle _unity_self, double value)`
  （void 集合Time_Injected（ref PlayableHandle _unity_self, double value））
- `bool IsDone_Injected(ref PlayableHandle _unity_self)`
  （bool 是否Done_Injected（ref PlayableHandle _unity_self））
- `double GetDuration_Injected(ref PlayableHandle _unity_self)`
  （double 获取Duration_Injected（ref PlayableHandle _unity_self））
- `void SetDuration_Injected(ref PlayableHandle _unity_self, double value)`
  （void 集合Duration_Injected（ref PlayableHandle _unity_self, double value））
- `void SetPropagateSetTime_Injected(ref PlayableHandle _unity_self, bool value)`
  （void 集合Propagate集合Time_Injected（ref PlayableHandle _unity_self, bool value））
- `int GetInputCount_Injected(ref PlayableHandle _unity_self)`
  （int 获取输入Count_Injected（ref PlayableHandle _unity_self））
- `void SetInputCount_Injected(ref PlayableHandle _unity_self, int value)`
  （void 集合输入Count_Injected（ref PlayableHandle _unity_self, int value））
- `void SetInputWeight_Injected(ref PlayableHandle _unity_self, ref PlayableHandle input, float weight)`
  （void 集合输入Weight_Injected（ref PlayableHandle _unity_self, ref PlayableHandle input, float weight））
- `void SetTraversalMode_Injected(ref PlayableHandle _unity_self, PlayableTraversalMode mode)`
  （void 集合TraversalMode_Injected（ref PlayableHandle _unity_self, PlayableTraversal模式 mode））
- `DirectorWrapMode GetTimeWrapMode_Injected(ref PlayableHandle _unity_self)`
  （DirectorWrap模式 获取时间WrapMode_Injected（ref PlayableHandle _unity_self））
- `void SetTimeWrapMode_Injected(ref PlayableHandle _unity_self, DirectorWrapMode mode)`
  （void 集合时间WrapMode_Injected（ref PlayableHandle _unity_self, DirectorWrap模式 mode））
- `object GetScriptInstance_Injected(ref PlayableHandle _unity_self)`
  （object 获取ScriptInstance_Injected（ref PlayableHandle _unity_self））
- `void GetInputHandle_Injected(ref PlayableHandle _unity_self, int index, out PlayableHandle ret)`
  （void 获取输入Handle_Injected（ref PlayableHandle _unity_self, int index, out PlayableHandle ret））
- `void SetInputWeightFromIndex_Injected(ref PlayableHandle _unity_self, int index, float weight)`
  （void 集合输入WeightFromIndex_Injected（ref PlayableHandle _unity_self, int index, float weight））
- `float GetInputWeightFromIndex_Injected(ref PlayableHandle _unity_self, int index)`
  （float 获取输入WeightFromIndex_Injected（ref PlayableHandle _unity_self, int index））

---

## PlayableOutput（PlayableOutput）

**继承**: IPlayableOutput, IEquatable<PlayableOutput>（IPlayableOutput, IEquatable<PlayableOutput>）

### 字段 (2)

- `PlayableOutputHandle m_Handle`（PlayableOutput句柄 m_句柄）(偏移: 0x0)
- `PlayableOutput m_NullPlayableOutput`（PlayableOutput m_NullPlayableOutput）(偏移: 0x0)

### 方法 (3)

- `PlayableOutput get_Null()`
  （PlayableOutput get_Null（））
- `PlayableOutputHandle GetHandle()`
  （PlayableOutput句柄 获取句柄（））
- `bool Equals(PlayableOutput other)`
  （bool Equals（PlayableOutput other））

---

## PlayableOutputHandle（PlayableOutput句柄）

**继承**: IEquatable<PlayableOutputHandle>（IEquatable<PlayableOutputHandle>）

### 字段 (3)

- `IntPtr m_Handle`（整数Ptr m_句柄）(偏移: 0x0)
- `uint m_Version`（uint m_Version）(偏移: 0x4)
- `PlayableOutputHandle m_Null`（PlayableOutput句柄 m_Null）(偏移: 0x0)

### 方法 (26)

- `PlayableOutputHandle get_Null()`
  （PlayableOutput句柄 get_Null（））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool op_Equality(PlayableOutputHandle lhs, PlayableOutputHandle rhs)`
  （bool op_Equality（PlayableOutput句柄 lhs, PlayableOutput句柄 rhs））
- `bool Equals(object p)`
  （bool Equals（object p））
- `bool Equals(PlayableOutputHandle other)`
  （bool Equals（PlayableOutput句柄 other））
- `bool CompareVersion(PlayableOutputHandle lhs, PlayableOutputHandle rhs)`
  （bool CompareVersion（PlayableOutput句柄 lhs, PlayableOutput句柄 rhs））
- `bool IsValid()`
  （bool 是否Valid（））
- `Type GetPlayableOutputType()`
  （类型 获取PlayableOutput类型（））
- `void SetReferenceObject(Object target)`
  （void 集合引用对象（对象 target））
- `void SetUserData(Object target)`
  （void 集合User数据（对象 target））
- `PlayableHandle GetSourcePlayable()`
  （Playable句柄 获取SourcePlayable（））
- `void SetSourcePlayable(PlayableHandle target, int port)`
  （void 集合SourcePlayable（Playable句柄 target, int port））
- `int GetSourceOutputPort()`
  （int 获取SourceOutputPort（））
- `void SetWeight(float weight)`
  （void 集合Weight（float weight））
- `void PushNotification(PlayableHandle origin, INotification notification, object context)`
  （void PushNotification（Playable句柄 origin, INotification notification, object context））
- `void AddNotificationReceiver(INotificationReceiver receiver)`
  （void 添加NotificationReceiver（INotificationReceiver receiver））
- `bool IsValid_Injected(ref PlayableOutputHandle _unity_self)`
  （bool 是否Valid_Injected（ref PlayableOutputHandle _unity_self））
- `Type GetPlayableOutputType_Injected(ref PlayableOutputHandle _unity_self)`
  （类型 获取PlayableOutputType_Injected（ref PlayableOutputHandle _unity_self））
- `void SetReferenceObject_Injected(ref PlayableOutputHandle _unity_self, Object target)`
  （void 集合引用Object_Injected（ref PlayableOutputHandle _unity_self, 对象 target））
- `void SetUserData_Injected(ref PlayableOutputHandle _unity_self, Object target)`
  （void 集合UserData_Injected（ref PlayableOutputHandle _unity_self, 对象 target））
- `void GetSourcePlayable_Injected(ref PlayableOutputHandle _unity_self, out PlayableHandle ret)`
  （void 获取SourcePlayable_Injected（ref PlayableOutputHandle _unity_self, out PlayableHandle ret））
- `void SetSourcePlayable_Injected(ref PlayableOutputHandle _unity_self, ref PlayableHandle target, int port)`
  （void 集合SourcePlayable_Injected（ref PlayableOutputHandle _unity_self, ref PlayableHandle target, int port））
- `int GetSourceOutputPort_Injected(ref PlayableOutputHandle _unity_self)`
  （int 获取SourceOutputPort_Injected（ref PlayableOutputHandle _unity_self））
- `void SetWeight_Injected(ref PlayableOutputHandle _unity_self, float weight)`
  （void 集合Weight_Injected（ref PlayableOutputHandle _unity_self, float weight））
- `void PushNotification_Injected(ref PlayableOutputHandle _unity_self, ref PlayableHandle origin, INotification notification, object context)`
  （void PushNotification_Injected（ref PlayableOutputHandle _unity_self, ref PlayableHandle origin, INotification notification, object context））
- `void AddNotificationReceiver_Injected(ref PlayableOutputHandle _unity_self, INotificationReceiver receiver)`
  （void 添加NotificationReceiver_Injected（ref PlayableOutputHandle _unity_self, INotificationReceiver receiver））

---

## PlayableTrack（PlayableTrack）

**继承**: TrackAsset（Track资产）

### 方法 (1)

- `void OnCreateClip(TimelineClip clip)`
  （void On创建弹匣（Timeline弹匣 clip））

---

## PlayableTraversalMode（PlayableTraversal模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Player（玩家）

**继承**: Entity（实体）

### 字段 (33)

- `float defaultMoveSpeed`（float default移动Speed）(偏移: 0x0)
- `float playerHeight`（float player高度）(偏移: 0x4)
- `float crouchSubHeight`（float crouch子高度）(偏移: 0x8)
- `float mapCmrHeight`（float map摄像机高度）(偏移: 0xC)
- `float mapCmrCrouchSubHeight`（float map摄像机蹲下子高度）(偏移: 0x10)
- `Vector3 playerGravity`（三维向量 player重力）(偏移: 0x14)
- `PlayerCameraManager cameraManager`（玩家摄像机管理器 camera管理器）(偏移: 0x48)
- `Vector2 cameraRotation`（二维向量 cameraRotation）(偏移: 0x4C)
- `Recoil recoil`（后坐力 recoil）(偏移: 0x54)
- `List<CharacterModel> characters`（List<角色Model> characters）(偏移: 0x60)
- `EffectObj bulletEffect`（特效Obj bullet特效）(偏移: 0x64)
- `Action JumpPost_Listener`（动作 跳跃Post_监听器）(偏移: 0x6C)
- `float jumpDropSndNextPlayTime`（float jumpDropSnd下一个播放时间）(偏移: 0x78)
- `float lastFallTime`（float last坠落时间）(偏移: 0x7C)
- `float heightBeforeFloat`（float heightBefore浮点数）(偏移: 0x80)
- `float startMoveTime`（float start移动时间）(偏移: 0x84)
- `float airVelControlEndTime`（float airVel控制结束时间）(偏移: 0x88)
- `PropertyModifier Modifier_MoveSpeedRatio`（属性修改器 Modifier_移动Speed比率）(偏移: 0x8C)
- `ClientData clientData`（客户端数据 client数据）(偏移: 0x94)
- `NanoRoleSelect nanoRoleSelect`（纳米Role选择 nanoRole选择）(偏移: 0xA8)
- `Nano4T_Data nano4TData`（Nano4T_数据 nano4T数据）(偏移: 0xAC)
- `PlayerSkills skills`（玩家技能 skills）(偏移: 0xB0)
- `Coroutine respawn_Coroutine`（协程 respawn_协程）(偏移: 0xC8)
- `Action<Player> StartRespawn_Listener`（Action<Player> 开始Respawn_监听器）(偏移: 0xCC)
- `Player.RespawnType respawnType`（Player.重生类型 respawn类型）(偏移: 0xD0)
- `Action<Player> NextRespawnInRound_Listener`（Action<Player> 下一个重生InRound_监听器）(偏移: 0xD4)
- `float nextRegenTime`（float nextRegen时间）(偏移: 0xFC)
- `MapTrigger mapTrigger`（地图触发器 map触发器）(偏移: 0x108)
- `bool Buff_CameraRotDisabled`（bool 增益_摄像机旋转禁用）(偏移: 0x118)
- `RefBool CameraRotDisabled_BuffUpdater`（引用布尔值 摄像机RotDisabled_增益Updater）(偏移: 0x11C)
- `RefBool JumpDisabled_BuffUpdater`（引用布尔值 跳跃Disabled_增益Updater）(偏移: 0x124)
- `bool Buff_InfinityAmmo`（bool 增益_无限弹药）(偏移: 0x128)
- `RefBool InfinityAmmo_BuffUpdater`（引用布尔值 无限Ammo_增益Updater）(偏移: 0x12C)

### 方法 (147)

- `Vector3 get_mapCameraPos()`
  （三维向量 get_map摄像机Pos（））
- `Vector3 get_mapCameraForward()`
  （三维向量 get_map摄像机前进（））
- `Transform get_characterContainer()`
  （变换 get_character容器（））
- `void set_characterContainer(Transform value)`
  （void set_character容器（变换 value））
- `CharacterModel get_currentCharacter()`
  （角色模型 get_current角色（））
- `void set_currentCharacter(CharacterModel value)`
  （void set_current角色（角色模型 value））
- `Vector3 get_footPos()`
  （三维向量 get_footPos（））
- `bool get_autonomousJump()`
  （bool get_autonomous跳跃（））
- `void set_autonomousJump(bool value)`
  （void set_autonomous跳跃（bool value））
- `void add_JumpPost_Listener(Action value)`
  （void add_跳跃Post_监听器（动作 value））
- `void remove_JumpPost_Listener(Action value)`
  （void remove_跳跃Post_监听器（动作 value））
- `bool get_isGrounded()`
  （bool get_is着地（））
- `void set_isGrounded(bool value)`
  （void set_is着地（bool value））
- `string get_groundMatName()`
  （string get_ground材质名称（））
- `void set_groundMatName(string value)`
  （void set_ground材质名称（string value））
- `float get_fallTime()`
  （float get_fall时间（））
- `bool get_canControlVelInAir()`
  （bool get_can控制VelIn空中（））
- `Vector3 get_velocity()`
  （三维向量 get_velocity（））
- `float get_MoveSpeedRatio()`
  （float get_移动Speed比率（））
- `PlayerVelocity get_velData()`
  （玩家速度 get_vel数据（））
- `void set_velData(PlayerVelocity value)`
  （void set_vel数据（玩家速度 value））
- `PlayerData get_playerData()`
  （玩家数据 get_player数据（））
- `void set_playerData(PlayerData value)`
  （void set_player数据（玩家数据 value））
- `PlayerInput get_input()`
  （玩家输入 get_input（））
- `void set_input(PlayerInput value)`
  （void set_input（玩家输入 value））
- `PlayerWeapons get_wpns()`
  （玩家武器 get_wpns（））
- `void set_wpns(PlayerWeapons value)`
  （void set_wpns（玩家武器 value））
- `WeaponBag get_weaponBag()`
  （武器背包 get_weapon背包（））
- `void set_weaponBag(WeaponBag value)`
  （void set_weapon背包（武器背包 value））
- `PlayerMdlInfo get_modelInfo()`
  （玩家模型信息 get_model信息（））
- `void set_modelInfo(PlayerMdlInfo value)`
  （void set_model信息（玩家模型信息 value））
- `bool get_isSniper()`
  （bool get_is狙击（））
- `void set_isSniper(bool value)`
  （void set_is狙击（bool value））
- `Vector3 get_spawnPos()`
  （三维向量 get_spawnPos（））
- `void set_spawnPos(Vector3 value)`
  （void set_spawnPos（三维向量 value））
- `void add_StartRespawn_Listener(Action<Player> value)`
  （void add_开始Respawn_监听器（Action<Player> value））
- `void remove_StartRespawn_Listener(Action<Player> value)`
  （void remove_开始Respawn_监听器（Action<Player> value））
- `void add_NextRespawnInRound_Listener(Action<Player> value)`
  （void add_下一个重生InRound_监听器（Action<Player> value））
- `void remove_NextRespawnInRound_Listener(Action<Player> value)`
  （void remove_下一个重生InRound_监听器（Action<Player> value））
- `bool get_isRespawning()`
  （bool get_isRespawning（））
- `void set_isRespawning(bool value)`
  （void set_isRespawning（bool value））
- `bool get_isMyPlayer()`
  （bool get_isMy玩家（））
- `bool get_isFocusPlayer()`
  （bool get_is聚焦玩家（））
- `bool get_isFocusPlayerInPV()`
  （bool get_is聚焦玩家In第三人称视角（））
- `bool get_isNanoGhost()`
  （bool get_is纳米幽灵（））
- `float get_crouchDuration()`
  （float get_crouch持续时间（））
- `void set_crouchDuration(float value)`
  （void set_crouch持续时间（float value））
- `bool get_isCrouching()`
  （bool get_isCrouching（））
- `bool get_walking()`
  （bool get_walking（））
- `void set_walking(bool value)`
  （void set_walking（bool value））
- `ObscuredInt get_nanoClothCount()`
  （模糊整数 get_nano服装数量（））
- `void set_nanoClothCount(ObscuredInt value)`
  （void set_nano服装数量（模糊整数 value））
- `float get_lastStopStartTime()`
  （float get_last停止开始时间（））
- `void set_lastStopStartTime(float value)`
  （void set_last停止开始时间（float value））
- `KeyInputState get_input_Interact()`
  （按键输入状态 get_input_交互（））
- `void set_input_Interact(KeyInputState value)`
  （void set_input_交互（按键输入状态 value））
- `void add_Interact_Listener(Action<Player, KeyInputState> value)`
  （void add_Interact_监听器（Action<玩家, 键输入State> value））
- `void remove_Interact_Listener(Action<Player, KeyInputState> value)`
  （void remove_Interact_监听器（Action<玩家, 键输入State> value））
- `WPN_Gun.AmmoData get_mapGunAmmo1()`
  （WPN_Gun.弹药数据 get_map枪械Ammo1（））
- `void set_mapGunAmmo1(WPN_Gun.AmmoData value)`
  （void set_map枪械Ammo1（WPN_Gun.弹药数据 value））
- `WPN_Gun.AmmoData get_mapGunAmmo2()`
  （WPN_Gun.弹药数据 get_map枪械Ammo2（））
- `void set_mapGunAmmo2(WPN_Gun.AmmoData value)`
  （void set_map枪械Ammo2（WPN_Gun.弹药数据 value））
- `Transform get_climbStair()`
  （变换 get_climb楼梯（））
- `void set_climbStair(Transform value)`
  （void set_climb楼梯（变换 value））
- `bool get_isClimbing()`
  （bool get_isClimbing（））
- `void add_CameraRotDisabled_BuffUpdater(RefBool value)`
  （void add_摄像机RotDisabled_增益Updater（引用布尔值 value））
- `void remove_CameraRotDisabled_BuffUpdater(RefBool value)`
  （void remove_摄像机RotDisabled_增益Updater（引用布尔值 value））
- `bool get_Buff_JumpDisabled()`
  （bool get_Buff_跳跃禁用的（））
- `void set_Buff_JumpDisabled(bool value)`
  （void set_Buff_跳跃禁用的（bool value））
- `void add_JumpDisabled_BuffUpdater(RefBool value)`
  （void add_跳跃Disabled_增益Updater（引用布尔值 value））
- `void remove_JumpDisabled_BuffUpdater(RefBool value)`
  （void remove_跳跃Disabled_增益Updater（引用布尔值 value））
- `void add_InfinityAmmo_BuffUpdater(RefBool value)`
  （void add_无限Ammo_增益Updater（引用布尔值 value））
- `void remove_InfinityAmmo_BuffUpdater(RefBool value)`
  （void remove_无限Ammo_增益Updater（引用布尔值 value））
- `string get_nickName()`
  （string get_nick名称（））
- `int get_level()`
  （int get_level（））
- `int get_vipLevel()`
  （int get_vip等级（））
- `int get_kill()`
  （int get_kill（））
- `void set_kill(int value)`
  （void set_kill（int value））
- `int get_death()`
  （int get_death（））
- `void set_death(int value)`
  （void set_death（int value））
- `int get_survival()`
  （int get_survival（））
- `void set_survival(int value)`
  （void set_survival（int value））
- `int get_score()`
  （int get_score（））
- `void set_score(int value)`
  （void set_score（int value））
- `HUD_Role.AceSign get_aceSign()`
  （HUD_Role.王牌标志 get_ace标志（））
- `void set_aceSign(HUD_Role.AceSign value)`
  （void set_ace标志（HUD_Role.王牌标志 value））
- `NanoRole get_nanoRole()`
  （纳米角色 get_nanoRole（））
- `void set_nanoRole(NanoRole value)`
  （void set_nanoRole（纳米角色 value））
- `void Awake()`
  （void Awake（））
- `void Update()`
  （void 更新（））
- `void FixedUpdate()`
  （void 固定更新（））
- `void UpdateGroundMatName()`
  （void 更新地面材质名称（））
- `void CharacterModelSetting()`
  （void 角色模型设置（））
- `void OnDestroy()`
  （void On销毁（））
- `bool SetExistentCharacter(string name)`
  （bool 集合Existent角色（string name））
- `void SetCharacter(CharacterModel character)`
  （void 集合角色（角色模型 character））
- `void UpdateModelColor()`
  （void 更新模型颜色（））
- `void PhysicalUpdate()`
  （void Physical更新（））
- `void SetGroundState(bool newState)`
  （void 集合地面状态（bool newState））
- `void OnJumpBtnDown()`
  （void On跳跃Btn下（））
- `float GetMoveSpeed()`
  （float 获取移动Speed（））
- `void MoveByLocalDirection(int x, int z)`
  （void 移动By本地的方向（int x, int z））
- `Vector2 GetCameraRotation()`
  （二维向量 获取摄像机Rotation（））
- `void AddCameraRotation(float x, float y)`
  （void 添加摄像机Rotation（float x, float y））
- `void UpdateCameraRotaion()`
  （void 更新摄像机Rotaion（））
- `void LookAt(Vector3 dir)`
  （void LookAt（三维向量 dir））
- `void SetWeapon(Weapon weapon)`
  （void 集合Weapon（Weapon weapon））
- `void RecoilShootPostureCheck()`
  （void 后坐力射击姿态检查（））
- `void OnEntityHurt(DamageEventData eventData)`
  （void On实体Hurt（伤害事件数据 eventData））
- `void OnEntityDeath(DeathEventData eventData)`
  （void On实体死亡（死亡事件数据 eventData））
- `void ClearMapObject()`
  （void 清除映射对象（））
- `void DropWeaponAfterDeath()`
  （void DropWeaponAfter死亡（））
- `void SendFireInTheHoleRadio(WeaponClass wpnClass)`
  （void 发送开火InTheHoleRadio（武器类别 wpnClass））
- `void RemoveFromTeamList(bool onlyAliveList)`
  （void 移除From队伍列表（bool onlyAliveList））
- `void AddToTeamList(bool isAliveList)`
  （void 添加To队伍列表（bool isAliveList））
- `void Respawn(float respawnTime, float invisibleTime = 1)`
  （void 重生（float respawnTime, float invisibleTime = 1））
- `void BreakRespawnCoroutine()`
  （void Break重生协程（））
- `void Spawn()`
  （void 出生（））
- `void OnGameRoundEnd()`
  （void On游戏回合结束（））
- `void SetPos(Vector3 pos)`
  （void 集合Pos（三维向量 pos））
- `bool SelectWeaponBag(int index = -1)`
  （bool 选择Weapon背包（int index = -1））
- `bool TryPickUpWeapon(Weapon wpn)`
  （bool TryPick上Weapon（Weapon wpn））
- `void SetCrouchState(bool crouch)`
  （void 集合蹲下状态（bool crouch））
- `void SetWalkState(bool walk)`
  （void 集合Walk状态（bool walk））
- `bool TrySubSkillHPCost(int cost)`
  （bool Try子技能HPCost（int cost））
- `void BreakStopTime()`
  （void Break停止时间（））
- `void NanoGhostHPRegen()`
  （void 纳米幽灵HPRegen（））
- `void SetNanoClothCount(int count)`
  （void 集合纳米服装数量（int count））
- `void AddNanoClothCount(int count)`
  （void 添加纳米服装数量（int count））
- `void SetInteractInput(KeyInputState state)`
  （void 集合交互输入（按键输入状态 state））
- `void FillMapGunAmmo()`
  （void Fill映射枪械弹药（））
- `RecyclableSound Play3dSound(string sndName, int index = -1)`
  （Recyclable音效 Play3d音效（string sndName, int index = -1））
- `void PlayBulletEffect(Vector3 position, bool left = False)`
  （void 播放子弹特效（三维向量 position, bool left = False））
- `void OnTriggerEnter(Collider other)`
  （void On触发器Enter（碰撞器 other））
- `void OnTriggerExit(Collider other)`
  （void On触发器Exit（碰撞器 other））
- `void Speak(string msg, HUD_ChatBox.Channel channel = 0)`
  （void Speak（string msg, HUD_ChatBox.Channel channel = 0））
- `void UpdateAce()`
  （void 更新王牌（））
- `void PlayFootStepSound(bool isRightFoot)`
  （void 播放脚部Step音效（bool isRightFoot））
- `void PlayJumpSound(bool isDrop)`
  （void 播放跳跃音效（bool isDrop））
- `void ResetDropSndTime()`
  （void 重置DropSnd时间（））
- `void UpdateFallTime()`
  （void 更新坠落时间（））
- `void UpdateRunState()`
  （void 更新运行状态（））
- `EffectObj AddPlayerViewEffect(GameObject fxPrefab)`
  （特效Obj 添加玩家视图特效（游戏对象 fxPrefab））
- `void UpdateBuffProperty()`
  （void 更新增益属性（））
- `void AddNextRespawnInvincible(float time)`
  （void 添加下一个重生Invincible（float time））
- `string GetName()`
  （string 获取名称（））
- `Transform GetVisibleHitBox(Ray viewRay)`
  （变换 获取可见的命中Box（Ray viewRay））

---

## Player.MoveType（Player.移动类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Player.RespawnType（Player.重生类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## PlayerCameraManager（玩家摄像机管理器）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (15)

- `CinemachineVirtualCamera mapCamera`（Cinemachine虚拟的摄像机 map摄像机）(偏移: 0xC)
- `Camera modelCamera`（摄像机 model摄像机）(偏移: 0x10)
- `int activeCullingMask`（int activeCulling掩码）(偏移: 0x14)
- `Transform modelContainer`（变换 model容器）(偏移: 0x18)
- `Vector3 modelDelayPos`（三维向量 model延迟Pos）(偏移: 0x1C)
- `float zoomFovScale`（float zoomFov缩放）(偏移: 0x28)
- `string zoomAnimId`（string zoom动画Id）(偏移: 0x2C)
- `string skillZoomId`（string skill瞄准Id）(偏移: 0x30)
- `float knifeHit_Value`（float knifeHit_值）(偏移: 0x34)
- `Coroutine knifeHit_Coroutine`（协程 knifeHit_协程）(偏移: 0x38)
- `Vector3 modelRightHandScale`（三维向量 model右手部缩放）(偏移: 0x0)
- `float modelDefaultFOV`（float model默认的视野）(偏移: 0x3C)
- `float extraMapFov`（float extra映射Fov）(偏移: 0x40)
- `float extraPvFov`（float extraPvFov）(偏移: 0x44)
- `PlayerCameraManager.FovZoomInfo fovZoomInfo`（玩家摄像机Manager.Fov瞄准信息 fov瞄准信息）(偏移: 0x48)

### 方法 (17)

- `Transform get_modelCameraTransform()`
  （变换 get_model摄像机变换（））
- `void set_mapFOV(float value)`
  （void set_map视野（float value））
- `void set_modelFOV(float value)`
  （void set_model视野（float value））
- `void set_modelVisible(bool value)`
  （void set_model可见的（bool value））
- `void set_focus(bool value)`
  （void set_focus（bool value））
- `void Awake()`
  （void Awake（））
- `void Update()`
  （void 更新（））
- `void OnDestroy()`
  （void On销毁（））
- `void SetModelDelayPos()`
  （void 集合模型延迟Pos（））
- `void AddModelDelayPos(float delay)`
  （void 添加模型延迟Pos（float delay））
- `void PlaySniperZoom(float fovScale, float duration, Action endCallBack)`
  （void 播放狙击瞄准（float fovScale, float duration, 动作 endCallBack））
- `void CameraFovSetting()`
  （void 摄像机Fov设置（））
- `void SetRotation(float angle)`
  （void 集合Rotation（float angle））
- `void LookAt(Vector3 dir)`
  （void LookAt（三维向量 dir））
- `void PlayKnifeHitStunShake(bool isBigshot)`
  （void 播放刀命中眩晕震动（bool isBigshot））
- `void SetFovBuffInfo(PlayerCameraManager.FovZoomInfo info)`
  （void 集合Fov增益信息（玩家摄像机Manager.Fov瞄准信息 info））
- `void FovZommBuffEndEvent()`
  （void FovZomm增益结束事件（））

---

## PlayerCameraManager.FovZoomInfo（玩家摄像机Manager.Fov瞄准信息）

### 字段 (5)

- `Buff bindBuff`（增益 bind增益）(偏移: 0x0)
- `float extraMapFov`（float extra映射Fov）(偏移: 0x4)
- `float extraPvFov`（float extraPvFov）(偏移: 0x8)
- `float inTime`（float in时间）(偏移: 0xC)
- `float outTime`（float out时间）(偏移: 0x10)

---

## PlayerConnection（玩家连接）

**继承**: ScriptableObject（脚本对象）

### 字段 (5)

- `IPlayerEditorConnectionNative connectionNative`（I玩家Editor连接Native connectionNative）(偏移: 0x0)
- `PlayerEditorConnectionEvents m_PlayerEditorConnectionEvents`（玩家Editor连接Events m_玩家Editor连接Events）(偏移: 0xC)
- `List<int> m_connectedPlayers`（List<int> m_connectedPlayers）(偏移: 0x10)
- `bool m_IsInitilized`（bool m_是否Initilized）(偏移: 0x14)
- `PlayerConnection s_Instance`（玩家连接 s_实例）(偏移: 0x4)

### 方法 (18)

- `PlayerConnection get_instance()`
  （玩家连接 get_instance（））
- `bool get_isConnected()`
  （bool get_isConnected（））
- `PlayerConnection CreateInstance()`
  （玩家连接 创建实例（））
- `void OnEnable()`
  （void On启用（））
- `IPlayerEditorConnectionNative GetConnectionNativeApi()`
  （I玩家Editor连接Native 获取连接NativeApi（））
- `void Register(Guid messageId, UnityAction<MessageEventArgs> callback)`
  （void Register（Guid messageId, Unity引擎Action<Message事件Args> callback））
- `void Unregister(Guid messageId, UnityAction<MessageEventArgs> callback)`
  （void Unregister（Guid messageId, Unity引擎Action<Message事件Args> callback））
- `void RegisterConnection(UnityAction<int> callback)`
  （void Register连接（Unity引擎Action<int> callback））
- `void RegisterDisconnection(UnityAction<int> callback)`
  （void RegisterDisconnection（Unity引擎Action<int> callback））
- `void UnregisterConnection(UnityAction<int> callback)`
  （void Unregister连接（Unity引擎Action<int> callback））
- `void UnregisterDisconnection(UnityAction<int> callback)`
  （void UnregisterDisconnection（Unity引擎Action<int> callback））
- `void Send(Guid messageId, byte[] data)`
  （void 发送（Guid messageId, byte[] data））
- `bool TrySend(Guid messageId, byte[] data)`
  （bool Try发送（Guid messageId, byte[] data））
- `bool BlockUntilRecvMsg(Guid messageId, int timeout)`
  （bool BlockUntilRecvMsg（Guid messageId, int timeout））
- `void DisconnectAll()`
  （void Disconnect所有（））
- `void MessageCallbackInternal(IntPtr data, ulong size, ulong guid, string messageId)`
  （void Message回调内部的（整数Ptr data, ulong size, ulong guid, string messageId））
- `void ConnectedCallbackInternal(int playerId)`
  （void Connected回调内部的（int playerId））
- `void DisconnectedCallback(int playerId)`
  （void Disconnected回调（int playerId））

---

## PlayerConnectionInternal（玩家连接内部的）

**继承**: IPlayerEditorConnectionNative（I玩家Editor连接Native）

### 方法 (8)

- `bool IsConnected()`
  （bool 是否Connected（））
- `void Initialize()`
  （void 初始化（））
- `void RegisterInternal(string messageId)`
  （void Register内部的（string messageId））
- `void UnregisterInternal(string messageId)`
  （void Unregister内部的（string messageId））
- `void SendMessage(string messageId, byte[] data, int playerId)`
  （void 发送Message（string messageId, byte[] data, int playerId））
- `bool TrySendMessage(string messageId, byte[] data, int playerId)`
  （bool Try发送Message（string messageId, byte[] data, int playerId））
- `void PollInternal()`
  （void Poll内部的（））
- `void DisconnectAll()`
  （void Disconnect所有（））

---

## PlayerController（玩家控制器）

**继承**: Singleton<PlayerController>（Singleton<玩家Controller>）

### 字段 (6)

- `string focusHUD`（string focus抬头显示）(偏移: 0xC)
- `float activeTime`（float active时间）(偏移: 0x0)
- `float mouseSpeed`（float mouseSpeed）(偏移: 0x4)
- `float zoomSpeed`（float zoomSpeed）(偏移: 0x8)
- `RefString FocusHUD_Listenner`（Ref字符串 聚焦HUD_Listenner）(偏移: 0xC)
- `float lastPressWTime`（float lastPressW时间）(偏移: 0x10)

### 方法 (15)

- `string get_FocusHUD()`
  （string get_聚焦抬头显示（））
- `Player get_player()`
  （玩家 get_player（））
- `void add_FocusHUD_Listenner(RefString value)`
  （void add_聚焦HUD_Listenner（Ref字符串 value））
- `void remove_FocusHUD_Listenner(RefString value)`
  （void remove_聚焦HUD_Listenner（Ref字符串 value））
- `void Awake()`
  （void Awake（））
- `void Start()`
  （void 开始（））
- `void OnDestroy()`
  （void On销毁（））
- `void Update()`
  （void 更新（））
- `void SkillButton()`
  （void 技能按钮（））
- `void CrouchAndWalkButton()`
  （void 蹲下AndWalk按钮（））
- `void CameraRotation()`
  （void 摄像机Rotation（））
- `void MoveButton()`
  （void 移动按钮（））
- `void JumpButton()`
  （void 跳跃按钮（））
- `void SelectWeapon()`
  （void 选择Weapon（））
- `void UseWeapon()`
  （void UseWeapon（））

---

## PlayerData（玩家数据）

### 字段 (23)

- `Action<Model.Type> ObserveMode_Listener`（Action<Model.Type> 观察模式监听器）(偏移: 0xC)
- `int playerID`（int playerID）(偏移: 0x14)
- `string orignalCharacterName`（string orignal角色名称）(偏移: 0x18)
- `int rank`（int rank）(偏移: 0x1C)
- `int spawnCount`（int spawn数量）(偏移: 0x20)
- `bool playerViewModelVisible`（bool player视图模型可见的）(偏移: 0x24)
- `int zoomType`（int zoom类型）(偏移: 0x28)
- `Sprite zoomSprite`（精灵 zoom精灵）(偏移: 0x2C)
- `float zoomCameraSpeedMultiplier`（float zoom摄像机SpeedMultiplier）(偏移: 0x30)
- `bool isAbsorbed`（bool is被吸收）(偏移: 0x34)
- `bool isBornNanoGhost`（bool is出生纳米幽灵）(偏移: 0x35)
- `int nanoDamage`（int nano伤害）(偏移: 0x38)
- `int nanoGhostLevel`（int nano幽灵等级）(偏移: 0x3C)
- `bool canPickUpWeapon`（bool canPick上Weapon）(偏移: 0x48)
- `bool ghostBladeSecKillTag`（bool ghost刀锋Sec击杀标签）(偏移: 0x49)
- `SubscribeableProperty<int> kill`（可订阅的Property<int> kill）(偏移: 0x4C)
- `SubscribeableProperty<int> death`（可订阅的Property<int> death）(偏移: 0x50)
- `SubscribeableProperty<int> survival`（可订阅的Property<int> survival）(偏移: 0x54)
- `SubscribeableProperty<int> score`（可订阅的Property<int> score）(偏移: 0x58)
- `SubscribeableProperty<HUD_Role.AceSign> aceSign`（可订阅的Property<HUD_Role.王牌Sign> ace标志）(偏移: 0x5C)
- `SubscribeableProperty<NanoRole> nanoRole`（可订阅的Property<纳米Role> nanoRole）(偏移: 0x60)
- `SubscribeableProperty<float> nanoRoleTableCloseTime`（可订阅的Property<float> nanoRoleTable关闭时间）(偏移: 0x64)
- `Action<Player> revengeTarget_Listener`（Action<Player> revengeTarget_监听器）(偏移: 0x6C)

### 方法 (13)

- `Model.Type get_observeMode()`
  （Model.类型 get_observe模式（））
- `void set_observeMode(Model.Type value)`
  （void set_observe模式（Model.类型 value））
- `MultiKillTimer get_multiKillTimer()`
  （多杀计时器 get_multi击杀计时器（））
- `void set_multiKillTimer(MultiKillTimer value)`
  （void set_multi击杀计时器（多杀计时器 value））
- `int get_nanoExp()`
  （int get_nanoExp（））
- `void set_nanoExp(int value)`
  （void set_nanoExp（int value））
- `Player get_revengeTarget()`
  （玩家 get_revenge目标（））
- `void set_revengeTarget(Player value)`
  （void set_revenge目标（玩家 value））
- `void SetObserveMode(Model.Type newMode)`
  （void 集合观察模式（Model.类型 newMode））
- `void SetZoom(int type, Sprite sprite)`
  （void 集合瞄准（int type, 精灵 sprite））
- `void SetNanoExp(int value)`
  （void 集合纳米Exp（int value））
- `void AddNanoExp(int value)`
  （void 添加纳米Exp（int value））
- `void SetRevengeTarget(Player killer)`
  （void 集合复仇目标（玩家 killer））

---

## PlayerEditorConnectionEvents（玩家Editor连接Events）

### 字段 (3)

- `List<PlayerEditorConnectionEvents.MessageTypeSubscribers> messageTypeSubscribers`（List<玩家Editor连接Events.Message类型Subscribers> message类型Subscribers）(偏移: 0x8)
- `PlayerEditorConnectionEvents.ConnectionChangeEvent connectionEvent`（玩家Editor连接Events.连接Change事件 connection事件）(偏移: 0xC)
- `PlayerEditorConnectionEvents.ConnectionChangeEvent disconnectionEvent`（玩家Editor连接Events.连接Change事件 disconnection事件）(偏移: 0x10)

### 方法 (3)

- `void InvokeMessageIdSubscribers(Guid messageId, byte[] data, int playerId)`
  （void InvokeMessageIdSubscribers（Guid messageId, byte[] data, int playerId））
- `UnityEvent<MessageEventArgs> AddAndCreate(Guid messageId)`
  （Unity引擎Event<Message事件Args> 添加And创建（Guid messageId））
- `void UnregisterManagedCallback(Guid messageId, UnityAction<MessageEventArgs> callback)`
  （void UnregisterManaged回调（Guid messageId, Unity引擎Action<Message事件Args> callback））

---

## PlayerEditorConnectionEvents.MessageTypeSubscribers（玩家Editor连接Events.Message类型Subscribers）

### 字段 (3)

- `string m_messageTypeId`（string m_message类型Id）(偏移: 0x8)
- `int subscriberCount`（int subscriber数量）(偏移: 0xC)
- `PlayerEditorConnectionEvents.MessageEvent messageCallback`（玩家Editor连接Events.Message事件 message回调）(偏移: 0x10)

### 方法 (2)

- `Guid get_MessageTypeId()`
  （Guid get_Message类型Id（））
- `void set_MessageTypeId(Guid value)`
  （void set_Message类型Id（Guid value））

---

## PlayerInput（玩家输入）

### 字段 (2)

- `KeyInputState RightMouse`（按键输入状态 鼠标右键）(偏移: 0x8)
- `KeyInputState JumpButton`（按键输入状态 跳跃按钮）(偏移: 0xC)

---

## PlayerLoopSystem（玩家循环系统）

### 字段 (5)

- `Type type`（类型 type）(偏移: 0x0)
- `PlayerLoopSystem[] subSystemList`（玩家LoopSystem[] sub系统列表）(偏移: 0x4)
- `PlayerLoopSystem.UpdateFunction updateDelegate`（玩家LoopSystem.更新Function update委托）(偏移: 0x8)
- `IntPtr updateFunction`（整数Ptr updateFunction）(偏移: 0xC)
- `IntPtr loopConditionFunction`（整数Ptr loopConditionFunction）(偏移: 0x10)

### 方法 (1)

- `string ToString()`
  （string To字符串（））

---

## PlayerLoopSystem.UpdateFunction（玩家LoopSystem.更新Function）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke()`
  （void Invoke（））
- `IAsyncResult BeginInvoke(AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## PlayerLoopSystemInternal（玩家Loop系统内部的）

### 字段 (5)

- `Type type`（类型 type）(偏移: 0x0)
- `PlayerLoopSystem.UpdateFunction updateDelegate`（玩家LoopSystem.更新Function update委托）(偏移: 0x4)
- `IntPtr updateFunction`（整数Ptr updateFunction）(偏移: 0x8)
- `IntPtr loopConditionFunction`（整数Ptr loopConditionFunction）(偏移: 0xC)
- `int numSubSystems`（int num子Systems）(偏移: 0x10)

---

## PlayerMdlInfo（玩家模型信息）

### 字段 (8)

- `SubscribeableProperty<Color> pvColor`（可订阅的Property<Color> pv颜色）(偏移: 0x8)
- `SubscribeableProperty<Color> cvColor`（可订阅的Property<Color> cv颜色）(偏移: 0xC)
- `List<PlayerMdlInfo.MatData> pvMatList`（List<玩家模型Info.材质Data> pv材质列表）(偏移: 0x10)
- `List<PlayerMdlInfo.MatData> cvMatList`（List<玩家模型Info.材质Data> cv材质列表）(偏移: 0x14)
- `Color AbsorbedColor`（颜色 被吸收颜色）(偏移: 0x0)
- `PlayerMdlInfo.FxType fxType`（玩家模型Info.特效类型 fx类型）(偏移: 0x18)
- `Ref2Float Getter_Alpha`（双引用浮点数 获取_透明度）(偏移: 0x20)
- `List<Renderer> cvRenderers`（List<Renderer> cvRenderers）(偏移: 0x24)

### 方法 (12)

- `float get_cvAlpha()`
  （float get_cv透明度（））
- `void set_cvAlpha(float value)`
  （void set_cv透明度（float value））
- `void add_Getter_Alpha(Ref2Float value)`
  （void add_Getter_透明度（双引用浮点数 value））
- `void remove_Getter_Alpha(Ref2Float value)`
  （void remove_Getter_透明度（双引用浮点数 value））
- `void AddModel(Model mdl)`
  （void 添加模型（模型 mdl））
- `void RemoveModel(Model mdl)`
  （void 移除模型（模型 mdl））
- `void AddMat(Material mat, List<PlayerMdlInfo.MatData> list, Color color)`
  （void 添加材质（材质 mat, List<玩家模型Info.材质Data> list, 颜色 color））
- `void RemoveMat(Material mat, List<PlayerMdlInfo.MatData> list)`
  （void 移除材质（材质 mat, List<玩家模型Info.材质Data> list））
- `void UpdateListColor(List<PlayerMdlInfo.MatData> list, Color oldColor, Color newColor)`
  （void 更新列表颜色（List<玩家模型Info.材质Data> list, 颜色 oldColor, 颜色 newColor））
- `void Update()`
  （void 更新（））
- `ShadowCastingMode GetShadowCastingMode()`
  （ShadowCasting模式 获取ShadowCasting模式（））
- `void UpdateShadowCaster()`
  （void 更新ShadowCaster（））

---

## PlayerMdlInfo.FxType（玩家模型Info.特效类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## PlayerMdlInfo.MatData（玩家模型Info.材质数据）

### 字段 (2)

- `Material mat`（材质 mat）(偏移: 0x0)
- `bool isTransparent`（bool is透明的）(偏移: 0x4)

---

## PlayerPrefs（玩家偏好）

### 方法 (14)

- `bool TrySetInt(string key, int value)`
  （bool Try集合整数（string key, int value））
- `bool TrySetFloat(string key, float value)`
  （bool Try集合浮点数（string key, float value））
- `bool TrySetSetString(string key, string value)`
  （bool Try集合集合字符串（string key, string value））
- `void SetInt(string key, int value)`
  （void 集合整数（string key, int value））
- `int GetInt(string key, int defaultValue)`
  （int 获取整数（string key, int defaultValue））
- `void SetFloat(string key, float value)`
  （void 集合浮点数（string key, float value））
- `float GetFloat(string key, float defaultValue)`
  （float 获取浮点数（string key, float defaultValue））
- `void SetString(string key, string value)`
  （void 集合字符串（string key, string value））
- `string GetString(string key, string defaultValue)`
  （string 获取字符串（string key, string defaultValue））
- `string GetString(string key)`
  （string 获取字符串（string key））
- `bool HasKey(string key)`
  （bool 是否有键（string key））
- `void DeleteKey(string key)`
  （void Delete键（string key））
- `void DeleteAll()`
  （void Delete所有（））
- `void Save()`
  （void 保存（））

---

## PlayerRefFloat（玩家Ref浮点数）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(Player player, ref float value)`
  （void Invoke（玩家 player, ref float value））
- `IAsyncResult BeginInvoke(Player player, ref float value, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（玩家 player, ref float value, 异步回调 callback, object object））
- `void EndInvoke(ref float value, IAsyncResult result)`
  （void 结束Invoke（ref float value, I异步Result result））

---

## PlayerSkills（玩家技能）

### 字段 (2)

- `Skill[] all`（Skill[] all）(偏移: 0x8)
- `Player owner`（玩家 owner）(偏移: 0xC)

### 方法 (5)

- `void Owner_LifeState_Listenner(bool isSpawn)`
  （void Owner_LifeState_Listenner（bool isSpawn））
- `void TryUse(SkillKey slot)`
  （void TryUse（技能键 slot））
- `void Set(SkillKey key, Skill skill, GameObject skillBtnPrefab)`
  （void 集合（技能键 key, 技能 skill, 游戏对象 skillBtnPrefab））
- `void Remove(string skillName)`
  （void 移除（string skillName））
- `void Remove(SkillKey key)`
  （void 移除（技能键 key））

---

## PlayerVelocity（玩家速度）

### 字段 (4)

- `Player owner`（玩家 owner）(偏移: 0x8)
- `Vector3 velocity`（三维向量 velocity）(偏移: 0xC)
- `PlayerVelocity.VelLockType lockType`（玩家Velocity.VelLock类型 lock类型）(偏移: 0x18)
- `float velUnlockTime`（float velUnlock时间）(偏移: 0x1C)

### 方法 (21)

- `float get_x()`
  （float get_x（））
- `float get_y()`
  （float get_y（））
- `void set_y(float value)`
  （void set_y（float value））
- `float get_z()`
  （float get_z（））
- `Vector3 get_direction()`
  （三维向量 get_direction（））
- `Vector3 get_horizontalDir()`
  （三维向量 get_horizontalDir（））
- `bool get_isVelUnlock()`
  （bool get_isVelUnlock（））
- `Vector3Int get_tryMoveDir()`
  （三维向量整数 get_try移动Dir（））
- `void set_tryMoveDir(Vector3Int value)`
  （void set_try移动Dir（三维向量整数 value））
- `bool get_isTryMoving()`
  （bool get_isTryMoving（））
- `bool get_dashOnGround()`
  （bool get_dashOn地面（））
- `void set_dashOnGround(bool value)`
  （void set_dashOn地面（bool value））
- `void Limit(float speed)`
  （void Limit（float speed））
- `void ClearGravity()`
  （void 清除重力（））
- `void ClearVelocity()`
  （void 清除速度（））
- `void SetMapDash(Vector3 vel, float duration, bool isHorizontal)`
  （void 集合映射Dash（三维向量 vel, float duration, bool isHorizontal））
- `void SetDash(float speed, float duration, bool dashOnGround)`
  （void 集合Dash（float speed, float duration, bool dashOnGround））
- `void LockVelocity(float lockTime)`
  （void Lock速度（float lockTime））
- `Vector3Int GetDashDirection()`
  （三维向量整数 获取Dash方向（））
- `void Update(int x, int z)`
  （void 更新（int x, int z））
- `bool ShouldMoveOnGround()`
  （bool 应该移动On地面（））

---

## PlayerVelocity.VelLockType（玩家Velocity.VelLock类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## PlayerViewData（玩家视图数据）

### 字段 (5)

- `Vector3 position`（三维向量 position）(偏移: 0x0)
- `Vector3 eulerAngle`（三维向量 euler角度）(偏移: 0xC)
- `Vector3 position_W`（三维向量 position_W）(偏移: 0x18)
- `Vector3 eulerAngle_W`（三维向量 eulerAngle_W）(偏移: 0x24)
- `float FOV`（float 视野）(偏移: 0x30)

---

## PlayerWeapons（玩家武器）

### 字段 (16)

- `Player owner`（玩家 owner）(偏移: 0x8)
- `List<Weapon> all`（List<Weapon> all）(偏移: 0xC)
- `Weapon inUse`（Weapon inUse）(偏移: 0x18)
- `Weapon[] current`（Weapon[] current）(偏移: 0x1C)
- `Weapon[] normal`（Weapon[] normal）(偏移: 0x20)
- `Weapon[] special`（Weapon[] special）(偏移: 0x24)
- `Weapon temporaryWpn`（Weapon temporary武器）(偏移: 0x28)
- `Weapon F_KeyWpn`（Weapon F_键武器）(偏移: 0x2C)
- `Weapon mapWpn`（Weapon map武器）(偏移: 0x30)
- `bool rapidChange`（bool rapidChange）(偏移: 0x34)
- `bool runState`（bool run状态）(偏移: 0x35)
- `bool interactDisabled`（bool interact禁用的）(偏移: 0x36)
- `float movePenalty`（float move惩罚）(偏移: 0x38)
- `PropertyModifier Modifier_ReloadSpeed`（属性修改器 Modifier_换弹Speed）(偏移: 0x3C)
- `PropertyModifier Modifier_KnifeRange`（属性修改器 Modifier_近战武器范围）(偏移: 0x40)
- `PropertyModifier Modifier_KnifeSpeed`（属性修改器 Modifier_近战武器Speed）(偏移: 0x44)

### 方法 (23)

- `int get_curSlot()`
  （int get_cur槽位（））
- `void set_curSlot(int value)`
  （void set_cur槽位（int value））
- `int get_lastSlot()`
  （int get_last槽位（））
- `void set_lastSlot(int value)`
  （void set_last槽位（int value））
- `float get_ReloadSpeed()`
  （float get_换弹Speed（））
- `float get_KnifeRange()`
  （float get_近战武器范围（））
- `float get_KnifeSpeed()`
  （float get_近战武器Speed（））
- `bool get_isInfinityAmmo()`
  （bool get_is无限弹药（））
- `void AutoSelect()`
  （void 自动选择（））
- `int GetValidSlot()`
  （int 获取Valid槽位（））
- `bool SelectLast()`
  （bool 选择最后一个（））
- `void SelectLastOrAutoSelect()`
  （void 选择最后一个Or自动选择（））
- `bool Select(int slot)`
  （bool 选择（int slot））
- `bool SelectByMouseRoll(bool forward)`
  （bool 选择By鼠标Roll（bool forward））
- `void SetWeapon(Weapon weapon)`
  （void 集合Weapon（Weapon weapon））
- `void SelectFKeyWeapon()`
  （void 选择F键Weapon（））
- `void RemoveAll()`
  （void 移除所有（））
- `void Remove(Weapon weapon, bool recycle = True)`
  （void 移除（Weapon weapon, bool recycle = True））
- `void SetCurrentWeapon(int slot, Weapon wpn)`
  （void 集合当前Weapon（int slot, Weapon wpn））
- `void FillMainWeaponAmmo()`
  （void Fill主要的Weapon弹药（））
- `void FillAllGunAmmo()`
  （void Fill所有枪械弹药（））
- `void GiveUpWeapon()`
  （void Give上Weapon（））
- `void GiveUpWeapon(int slot, bool death)`
  （void Give上Weapon（int slot, bool death））

---

## PluginsManager（Plugins管理器）

### 字段 (16)

- `ITweenPlugin _floatPlugin`（ITween插件 _float插件）(偏移: 0x0)
- `ITweenPlugin _doublePlugin`（ITween插件 _double插件）(偏移: 0x4)
- `ITweenPlugin _intPlugin`（ITween插件 _int插件）(偏移: 0x8)
- `ITweenPlugin _uintPlugin`（ITween插件 _uint插件）(偏移: 0xC)
- `ITweenPlugin _longPlugin`（ITween插件 _long插件）(偏移: 0x10)
- `ITweenPlugin _ulongPlugin`（ITween插件 _ulong插件）(偏移: 0x14)
- `ITweenPlugin _vector2Plugin`（ITween插件 _vector2插件）(偏移: 0x18)
- `ITweenPlugin _vector3Plugin`（ITween插件 _vector3插件）(偏移: 0x1C)
- `ITweenPlugin _vector4Plugin`（ITween插件 _vector4插件）(偏移: 0x20)
- `ITweenPlugin _quaternionPlugin`（ITween插件 _quaternion插件）(偏移: 0x24)
- `ITweenPlugin _colorPlugin`（ITween插件 _color插件）(偏移: 0x28)
- `ITweenPlugin _rectPlugin`（ITween插件 _rect插件）(偏移: 0x2C)
- `ITweenPlugin _rectOffsetPlugin`（ITween插件 _rectOffset插件）(偏移: 0x30)
- `ITweenPlugin _stringPlugin`（ITween插件 _string插件）(偏移: 0x34)
- `ITweenPlugin _vector3ArrayPlugin`（ITween插件 _vector3数组插件）(偏移: 0x38)
- `ITweenPlugin _color2Plugin`（ITween插件 _color2插件）(偏移: 0x3C)

### 方法 (1)

- `void PurgeAll()`
  （void Purge所有（））

---

## PointGraph（PointGraph）

**继承**: NavGraph, IUpdatableGraph（NavGraph, IUpdatableGraph）

### 字段 (13)

- `Transform root`（变换 root）(偏移: 0xB8)
- `string searchTag`（string search标签）(偏移: 0xBC)
- `float maxDistance`（float max距离）(偏移: 0xC0)
- `Vector3 limits`（三维向量 limits）(偏移: 0xC4)
- `bool raycast`（bool raycast）(偏移: 0xD0)
- `bool use2DPhysics`（bool use2D物理）(偏移: 0xD1)
- `bool thickRaycast`（bool thickRaycast）(偏移: 0xD2)
- `float thickRaycastRadius`（float thickRaycastRadius）(偏移: 0xD4)
- `bool recursive`（bool recursive）(偏移: 0xD8)
- `LayerMask mask`（层掩码 mask）(偏移: 0xDC)
- `bool optimizeForSparseGraph`（bool optimizeForSparseGraph）(偏移: 0xE0)
- `PointKDTree lookupTree`（PointKDTree lookupTree）(偏移: 0xE4)
- `PointNode[] nodes`（PointNode[] nodes）(偏移: 0xE8)

### 方法 (22)

- `int get_nodeCount()`
  （int get_node数量（））
- `void set_nodeCount(int value)`
  （void set_node数量（int value））
- `int CountNodes()`
  （int 数量Nodes（））
- `void GetNodes(Action<GraphNode> action)`
  （void 获取Nodes（Action<GraphNode> action））
- `NNInfoInternal GetNearest(Vector3 position, NNConstraint constraint, GraphNode hint)`
  （NN信息内部的 获取Nearest（三维向量 position, NNConstraint constraint, Graph节点 hint））
- `NNInfoInternal GetNearestForce(Vector3 position, NNConstraint constraint)`
  （NN信息内部的 获取Nearest强制（三维向量 position, NNConstraint constraint））
- `NNInfoInternal GetNearestInternal(Vector3 position, NNConstraint constraint, bool fastCheck)`
  （NN信息内部的 获取Nearest内部的（三维向量 position, NNConstraint constraint, bool fastCheck））
- `PointNode AddNode(Int3 position)`
  （Point节点 添加节点（Int3 position））
- `int CountChildren(Transform tr)`
  （int 数量Children（变换 tr））
- `void AddChildren(ref int c, Transform tr)`
  （void 添加Children（ref int c, 变换 tr））
- `void RebuildNodeLookup()`
  （void Rebuild节点Lookup（））
- `void AddToLookup(PointNode node)`
  （void 添加ToLookup（Point节点 node））
- `PointNode[] CreateNodes(int count)`
  （PointNode[] 创建Nodes（int count））
- `IEnumerable<Progress> ScanInternal()`
  （IEnumerable<Progress> Scan内部的（））
- `void ConnectNodes()`
  （void ConnectNodes（））
- `IEnumerable<Progress> ConnectNodesAsync()`
  （IEnumerable<Progress> ConnectNodes异步（））
- `bool IsValidConnection(GraphNode a, GraphNode b, out float dist)`
  （bool 是否Valid连接（Graph节点 a, Graph节点 b, out float dist））
- `void PostDeserialization(GraphSerializationContext ctx)`
  （void PostDeserialization（GraphSerializationContext ctx））
- `void RelocateNodes(Matrix4x4 deltaMatrix)`
  （void RelocateNodes（Matrix4x4 deltaMatrix））
- `void DeserializeSettingsCompatibility(GraphSerializationContext ctx)`
  （void DeserializeSettingsCompatibility（GraphSerializationContext ctx））
- `void SerializeExtraInfo(GraphSerializationContext ctx)`
  （void Serialize额外的信息（GraphSerializationContext ctx））
- `void DeserializeExtraInfo(GraphSerializationContext ctx)`
  （void Deserialize额外的信息（GraphSerializationContext ctx））

---

## PointKDTree（PointKDTree）

### 字段 (5)

- `PointKDTree.Node[] tree`（PointKDTree.Node[] tree）(偏移: 0x8)
- `int numNodes`（int numNodes）(偏移: 0xC)
- `List<GraphNode> largeList`（List<GraphNode> large列表）(偏移: 0x10)
- `Stack<GraphNode[]> arrayCache`（Stack<GraphNode[]> array缓存）(偏移: 0x14)
- `IComparer<GraphNode>[] comparers`（IComparer<GraphNode>[] comparers）(偏移: 0x0)

### 方法 (14)

- `void Add(GraphNode node)`
  （void 添加（Graph节点 node））
- `void Rebuild(GraphNode[] nodes, int start, int end)`
  （void Rebuild（GraphNode[] nodes, int start, int end））
- `GraphNode[] GetOrCreateList()`
  （GraphNode[] 获取Or创建列表（））
- `int Size(int index)`
  （int 大小（int index））
- `void CollectAndClear(int index, List<GraphNode> buffer)`
  （void CollectAnd清除（int index, List<GraphNode> buffer））
- `int MaxAllowedSize(int numNodes, int depth)`
  （int 最大Allowed大小（int numNodes, int depth））
- `void Rebalance(int index)`
  （void Rebalance（int index））
- `void EnsureSize(int index)`
  （void Ensure大小（int index））
- `void Build(int index, List<GraphNode> nodes, int start, int end)`
  （void Build（int index, List<GraphNode> nodes, int start, int end））
- `void Add(GraphNode point, int index, int depth = 0)`
  （void 添加（Graph节点 point, int index, int depth = 0））
- `GraphNode GetNearest(Int3 point, NNConstraint constraint)`
  （Graph节点 获取Nearest（Int3 point, NNConstraint constraint））
- `void GetNearestInternal(int index, Int3 point, NNConstraint constraint, ref GraphNode best, ref long bestSqrDist)`
  （void 获取Nearest内部的（int index, Int3 point, NNConstraint constraint, ref GraphNode best, ref long bestSqrDist））
- `void GetInRange(Int3 point, long sqrRadius, List<GraphNode> buffer)`
  （void 获取In范围（Int3 point, long sqrRadius, List<GraphNode> buffer））
- `void GetInRangeInternal(int index, Int3 point, long sqrRadius, List<GraphNode> buffer)`
  （void 获取In范围内部的（int index, Int3 point, long sqrRadius, List<GraphNode> buffer））

---

## PointKDTree.CompareX（PointKDTree.CompareX）

**继承**: IComparer<GraphNode>（IComparer<GraphNode>）

### 方法 (1)

- `int Compare(GraphNode lhs, GraphNode rhs)`
  （int Compare（Graph节点 lhs, Graph节点 rhs））

---

## PointKDTree.CompareY（PointKDTree.CompareY）

**继承**: IComparer<GraphNode>（IComparer<GraphNode>）

### 方法 (1)

- `int Compare(GraphNode lhs, GraphNode rhs)`
  （int Compare（Graph节点 lhs, Graph节点 rhs））

---

## PointKDTree.CompareZ（PointKDTree.CompareZ）

**继承**: IComparer<GraphNode>（IComparer<GraphNode>）

### 方法 (1)

- `int Compare(GraphNode lhs, GraphNode rhs)`
  （int Compare（Graph节点 lhs, Graph节点 rhs））

---

## PointKDTree.Node（PointKDTree.节点）

### 字段 (4)

- `GraphNode[] data`（GraphNode[] data）(偏移: 0x0)
- `int split`（int split）(偏移: 0x4)
- `ushort count`（ushort count）(偏移: 0x8)
- `byte splitAxis`（byte split轴）(偏移: 0xA)

---

## PointLight（Point光照）

### 字段 (10)

- `int instanceID`（int instanceID）(偏移: 0x0)
- `bool shadow`（bool shadow）(偏移: 0x4)
- `LightMode mode`（光照模式 mode）(偏移: 0x5)
- `Vector3 position`（三维向量 position）(偏移: 0x8)
- `Quaternion orientation`（Quaternion orientation）(偏移: 0x14)
- `LinearColor color`（Linear颜色 color）(偏移: 0x24)
- `LinearColor indirectColor`（Linear颜色 indirect颜色）(偏移: 0x34)
- `float range`（float range）(偏移: 0x44)
- `float sphereRadius`（float sphereRadius）(偏移: 0x48)
- `FalloffType falloff`（Falloff类型 falloff）(偏移: 0x4C)

---

## PointNode（Point节点）

**继承**: GraphNode（Graph节点）

### 字段 (2)

- `Connection[] connections`（Connection[] connections）(偏移: 0x20)
- `GameObject gameObject`（游戏对象 game对象）(偏移: 0x24)

### 方法 (13)

- `void SetPosition(Int3 value)`
  （void 集合Position（Int3 value））
- `void GetConnections(Action<GraphNode> action)`
  （void 获取Connections（Action<GraphNode> action））
- `void ClearConnections(bool alsoReverse)`
  （void 清除Connections（bool alsoReverse））
- `void UpdateRecursiveG(Path path, PathNode pathNode, PathHandler handler)`
  （void 更新RecursiveG（路径 path, 路径节点 pathNode, 路径处理器 handler））
- `bool ContainsConnection(GraphNode node)`
  （bool Contains连接（Graph节点 node））
- `void AddConnection(GraphNode node, uint cost)`
  （void 添加连接（Graph节点 node, uint cost））
- `void RemoveConnection(GraphNode node)`
  （void 移除连接（Graph节点 node））
- `void Open(Path path, PathNode pathNode, PathHandler handler)`
  （void 打开（路径 path, 路径节点 pathNode, 路径处理器 handler））
- `int GetGizmoHashCode()`
  （int 获取GizmoHashCode（））
- `void SerializeNode(GraphSerializationContext ctx)`
  （void Serialize节点（GraphSerializationContext ctx））
- `void DeserializeNode(GraphSerializationContext ctx)`
  （void Deserialize节点（GraphSerializationContext ctx））
- `void SerializeReferences(GraphSerializationContext ctx)`
  （void SerializeReferences（GraphSerializationContext ctx））
- `void DeserializeReferences(GraphSerializationContext ctx)`
  （void DeserializeReferences（GraphSerializationContext ctx））

---

## PointNodeTagModifier（Point节点标签修改器）

**继承**: GraphModifier（Graph修改器）

### 字段 (2)

- `Vector3[] points`（Vector3[] points）(偏移: 0x20)
- `uint pathTag`（uint path标签）(偏移: 0x24)

### 方法 (2)

- `void OnLatePostScan()`
  （void On延迟PostScan（））
- `void OnDrawGizmosSelected()`
  （void OnDrawGizmos选中的（））

---

## PointOnEdgeException（PointOnEdgeException）

**继承**: NotImplementedException（NotImplementedException）

### 字段 (3)

- `TriangulationPoint A`（TriangulationPoint A）(偏移: 0x44)
- `TriangulationPoint B`（TriangulationPoint B）(偏移: 0x48)
- `TriangulationPoint C`（TriangulationPoint C）(偏移: 0x4C)

---

## Pointer（指针）

**继承**: ISerializable（ISerializable）

### 字段 (2)

- `void* _ptr`（void* _ptr）(偏移: 0x8)
- `RuntimeType _ptrType`（Runtime类型 _ptr类型）(偏移: 0xC)

### 方法 (1)

- `object Box(void* ptr, Type type)`
  （object Box（void* ptr, 类型 type））

---

## PointerEventData（指针事件数据）

**继承**: BaseEventData（基础事件数据）

### 字段 (2)

- `GameObject m_PointerPress`（游戏对象 m_指针Press）(偏移: 0x14)
- `List<GameObject> hovered`（List<游戏Object> hovered）(偏移: 0xA8)

### 方法 (47)

- `GameObject get_pointerEnter()`
  （游戏对象 get_pointerEnter（））
- `void set_pointerEnter(GameObject value)`
  （void set_pointerEnter（游戏对象 value））
- `GameObject get_lastPress()`
  （游戏对象 get_lastPress（））
- `void set_lastPress(GameObject value)`
  （void set_lastPress（游戏对象 value））
- `GameObject get_rawPointerPress()`
  （游戏对象 get_raw指针Press（））
- `void set_rawPointerPress(GameObject value)`
  （void set_raw指针Press（游戏对象 value））
- `GameObject get_pointerDrag()`
  （游戏对象 get_pointerDrag（））
- `void set_pointerDrag(GameObject value)`
  （void set_pointerDrag（游戏对象 value））
- `GameObject get_pointerClick()`
  （游戏对象 get_pointerClick（））
- `void set_pointerClick(GameObject value)`
  （void set_pointerClick（游戏对象 value））
- `RaycastResult get_pointerCurrentRaycast()`
  （RaycastResult get_pointer当前Raycast（））
- `void set_pointerCurrentRaycast(RaycastResult value)`
  （void set_pointer当前Raycast（RaycastResult value））
- `RaycastResult get_pointerPressRaycast()`
  （RaycastResult get_pointerPressRaycast（））
- `void set_pointerPressRaycast(RaycastResult value)`
  （void set_pointerPressRaycast（RaycastResult value））
- `bool get_eligibleForClick()`
  （bool get_eligibleForClick（））
- `void set_eligibleForClick(bool value)`
  （void set_eligibleForClick（bool value））
- `int get_pointerId()`
  （int get_pointerId（））
- `void set_pointerId(int value)`
  （void set_pointerId（int value））
- `Vector2 get_position()`
  （二维向量 get_position（））
- `void set_position(Vector2 value)`
  （void set_position（二维向量 value））
- `Vector2 get_delta()`
  （二维向量 get_delta（））
- `void set_delta(Vector2 value)`
  （void set_delta（二维向量 value））
- `Vector2 get_pressPosition()`
  （二维向量 get_pressPosition（））
- `void set_pressPosition(Vector2 value)`
  （void set_pressPosition（二维向量 value））
- `Vector3 get_worldPosition()`
  （三维向量 get_worldPosition（））
- `void set_worldPosition(Vector3 value)`
  （void set_worldPosition（三维向量 value））
- `Vector3 get_worldNormal()`
  （三维向量 get_world法线（））
- `void set_worldNormal(Vector3 value)`
  （void set_world法线（三维向量 value））
- `float get_clickTime()`
  （float get_click时间（））
- `void set_clickTime(float value)`
  （void set_click时间（float value））
- `int get_clickCount()`
  （int get_click数量（））
- `void set_clickCount(int value)`
  （void set_click数量（int value））
- `Vector2 get_scrollDelta()`
  （二维向量 get_scrollDelta（））
- `void set_scrollDelta(Vector2 value)`
  （void set_scrollDelta（二维向量 value））
- `bool get_useDragThreshold()`
  （bool get_useDragThreshold（））
- `void set_useDragThreshold(bool value)`
  （void set_useDragThreshold（bool value））
- `bool get_dragging()`
  （bool get_dragging（））
- `void set_dragging(bool value)`
  （void set_dragging（bool value））
- `PointerEventData.InputButton get_button()`
  （指针事件Data.输入按钮 get_button（））
- `void set_button(PointerEventData.InputButton value)`
  （void set_button（指针事件Data.输入按钮 value））
- `bool IsPointerMoving()`
  （bool 是否指针Moving（））
- `bool IsScrolling()`
  （bool 是否Scrolling（））
- `Camera get_enterEventCamera()`
  （摄像机 get_enter事件摄像机（））
- `Camera get_pressEventCamera()`
  （摄像机 get_press事件摄像机（））
- `GameObject get_pointerPress()`
  （游戏对象 get_pointerPress（））
- `void set_pointerPress(GameObject value)`
  （void set_pointerPress（游戏对象 value））
- `string ToString()`
  （string To字符串（））

---

## PointerEventData.FramePressState（指针事件Data.FramePress状态）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## PointerEventData.InputButton（指针事件Data.输入按钮）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## PointerInputModule（指针输入模块）

**继承**: BaseInputModule（基础输入模块）

### 字段 (1)

- `PointerInputModule.MouseState m_MouseState`（指针输入Module.鼠标状态 m_鼠标状态）(偏移: 0x28)

### 方法 (15)

- `bool GetPointerData(int id, out PointerEventData data, bool create)`
  （bool 获取指针数据（int id, out PointerEventData data, bool create））
- `void RemovePointerData(PointerEventData data)`
  （void 移除指针数据（指针事件数据 data））
- `PointerEventData GetTouchPointerEventData(Touch input, out bool pressed, out bool released)`
  （指针事件数据 获取触摸指针事件数据（触摸 input, out bool pressed, out bool released））
- `void CopyFromTo(PointerEventData from, PointerEventData to)`
  （void 复制FromTo（指针事件数据 from, 指针事件数据 to））
- `PointerEventData.FramePressState StateForMouseButton(int buttonId)`
  （指针事件Data.FramePress状态 状态For鼠标按钮（int buttonId））
- `PointerInputModule.MouseState GetMousePointerEventData()`
  （指针输入Module.鼠标状态 获取鼠标指针事件数据（））
- `PointerInputModule.MouseState GetMousePointerEventData(int id)`
  （指针输入Module.鼠标状态 获取鼠标指针事件数据（int id））
- `PointerEventData GetLastPointerEventData(int id)`
  （指针事件数据 获取最后一个指针事件数据（int id））
- `bool ShouldStartDrag(Vector2 pressPos, Vector2 currentPos, float threshold, bool useDragThreshold)`
  （bool 应该开始Drag（二维向量 pressPos, 二维向量 currentPos, float threshold, bool useDragThreshold））
- `void ProcessMove(PointerEventData pointerEvent)`
  （void 处理移动（指针事件数据 pointerEvent））
- `void ProcessDrag(PointerEventData pointerEvent)`
  （void 处理Drag（指针事件数据 pointerEvent））
- `bool IsPointerOverGameObject(int pointerId)`
  （bool 是否指针Over游戏对象（int pointerId））
- `void ClearSelection()`
  （void 清除Selection（））
- `string ToString()`
  （string To字符串（））
- `void DeselectIfSelectionChanged(GameObject currentOverGo, BaseEventData pointerEvent)`
  （void 取消选择IfSelectionChanged（游戏对象 currentOverGo, 基础事件数据 pointerEvent））

---

## PointerInputModule.ButtonState（指针输入Module.按钮状态）

### 字段 (2)

- `PointerEventData.InputButton m_Button`（指针事件Data.输入按钮 m_按钮）(偏移: 0x8)
- `PointerInputModule.MouseButtonEventData m_EventData`（指针输入Module.鼠标按钮事件数据 m_事件数据）(偏移: 0xC)

### 方法 (4)

- `PointerInputModule.MouseButtonEventData get_eventData()`
  （指针输入Module.鼠标按钮事件数据 get_event数据（））
- `void set_eventData(PointerInputModule.MouseButtonEventData value)`
  （void set_event数据（指针输入Module.鼠标按钮事件数据 value））
- `PointerEventData.InputButton get_button()`
  （指针事件Data.输入按钮 get_button（））
- `void set_button(PointerEventData.InputButton value)`
  （void set_button（指针事件Data.输入按钮 value））

---

## PointerInputModule.MouseButtonEventData（指针输入Module.鼠标按钮事件数据）

### 字段 (2)

- `PointerEventData.FramePressState buttonState`（指针事件Data.FramePress状态 button状态）(偏移: 0x8)
- `PointerEventData buttonData`（指针事件数据 button数据）(偏移: 0xC)

### 方法 (2)

- `bool PressedThisFrame()`
  （bool 按下的ThisFrame（））
- `bool ReleasedThisFrame()`
  （bool ReleasedThisFrame（））

---

## PointerInputModule.MouseState（指针输入Module.鼠标状态）

### 字段 (1)

- `List<PointerInputModule.ButtonState> m_TrackedButtons`（List<指针输入Module.按钮State> m_TrackedButtons）(偏移: 0x8)

### 方法 (4)

- `bool AnyPressesThisFrame()`
  （bool 任意PressesThisFrame（））
- `bool AnyReleasesThisFrame()`
  （bool 任意ReleasesThisFrame（））
- `PointerInputModule.ButtonState GetButtonState(PointerEventData.InputButton button)`
  （指针输入Module.按钮状态 获取按钮状态（指针事件Data.输入按钮 button））
- `void SetButtonState(PointerEventData.InputButton button, PointerEventData.FramePressState stateForMouseButton, PointerEventData data)`
  （void 集合按钮状态（指针事件Data.输入按钮 button, 指针事件Data.FramePress状态 stateForMouseButton, 指针事件数据 data））

---

## PointerSpec（指针Spec）

**继承**: ModifierSpec（修改器Spec）

### 字段 (1)

- `int pointer_level`（int pointer_level）(偏移: 0x8)

### 方法 (3)

- `Type Resolve(Type type)`
  （类型 Resolve（类型 type））
- `StringBuilder Append(StringBuilder sb)`
  （字符串构建器 Append（字符串构建器 sb））
- `string ToString()`
  （string To字符串（））

---

## PointerType（指针类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## PolyFillType（PolyFill类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## PolyNode（Poly节点）

### 字段 (4)

- `PolyNode m_Parent`（Poly节点 m_父级）(偏移: 0x8)
- `List<IntPoint> m_polygon`（List<整数Point> m_polygon）(偏移: 0xC)
- `int m_Index`（int m_索引）(偏移: 0x10)
- `List<PolyNode> m_Childs`（List<PolyNode> m_Childs）(偏移: 0x14)

### 方法 (5)

- `int get_ChildCount()`
  （int get_子级数量（））
- `List<IntPoint> get_Contour()`
  （List<整数Point> get_Contour（））
- `void AddChild(PolyNode Child)`
  （void 添加子级（Poly节点 Child））
- `List<PolyNode> get_Childs()`
  （List<PolyNode> get_Childs（））
- `void set_IsOpen(bool value)`
  （void set_是否打开（bool value））

---

## PolyTree（PolyTree）

**继承**: PolyNode（Poly节点）

### 字段 (1)

- `List<PolyNode> m_AllPolys`（List<PolyNode> m_所有Polys）(偏移: 0x1C)

### 方法 (2)

- `void Finalize()`
  （void Finalize（））
- `void Clear()`
  （void 清除（））

---

## PolyType（Poly类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Polygon（Polygon）

**继承**: Triangulatable（Triangulatable）

### 字段 (5)

- `List<TriangulationPoint> _points`（List<TriangulationPoint> _points）(偏移: 0x8)
- `List<TriangulationPoint> _steinerPoints`（List<TriangulationPoint> _steinerPoints）(偏移: 0xC)
- `List<Polygon> _holes`（List<Polygon> _holes）(偏移: 0x10)
- `List<DelaunayTriangle> _triangles`（List<DelaunayTriangle> _triangles）(偏移: 0x14)
- `PolygonPoint _last`（PolygonPoint _last）(偏移: 0x18)

### 方法 (10)

- `TriangulationMode get_TriangulationMode()`
  （Triangulation模式 get_Triangulation模式（））
- `void AddHole(Polygon poly)`
  （void 添加Hole（Polygon poly））
- `void AddPoints(IEnumerable<PolygonPoint> list)`
  （void 添加Points（IEnumerable<PolygonPoint> list））
- `IList<TriangulationPoint> get_Points()`
  （IList<TriangulationPoint> get_Points（））
- `IList<DelaunayTriangle> get_Triangles()`
  （IList<DelaunayTriangle> get_Triangles（））
- `IList<Polygon> get_Holes()`
  （IList<Polygon> get_Holes（））
- `void AddTriangle(DelaunayTriangle t)`
  （void 添加Triangle（DelaunayTriangle t））
- `void AddTriangles(IEnumerable<DelaunayTriangle> list)`
  （void 添加Triangles（IEnumerable<DelaunayTriangle> list））
- `void ClearTriangles()`
  （void 清除Triangles（））
- `void Prepare(TriangulationContext tcx)`
  （void Prepare（TriangulationContext tcx））

---

## Polygon（Polygon）

### 方法 (13)

- `bool ContainsPointXZ(Vector3 a, Vector3 b, Vector3 c, Vector3 p)`
  （bool ContainsPointXZ（三维向量 a, 三维向量 b, 三维向量 c, 三维向量 p））
- `bool ContainsPointXZ(Int3 a, Int3 b, Int3 c, Int3 p)`
  （bool ContainsPointXZ（Int3 a, Int3 b, Int3 c, Int3 p））
- `bool ContainsPoint(Int2 a, Int2 b, Int2 c, Int2 p)`
  （bool ContainsPoint（Int2 a, Int2 b, Int2 c, Int2 p））
- `bool ContainsPoint(Vector2[] polyPoints, Vector2 p)`
  （bool ContainsPoint（Vector2[] polyPoints, 二维向量 p））
- `bool ContainsPointXZ(Vector3[] polyPoints, Vector3 p)`
  （bool ContainsPointXZ（Vector3[] polyPoints, 三维向量 p））
- `int SampleYCoordinateInTriangle(Int3 p1, Int3 p2, Int3 p3, Int3 p)`
  （int SampleYCoordinateInTriangle（Int3 p1, Int3 p2, Int3 p3, Int3 p））
- `Vector3[] ConvexHullXZ(Vector3[] points)`
  （Vector3[] ConvexHullXZ（Vector3[] points））
- `Vector2 ClosestPointOnTriangle(Vector2 a, Vector2 b, Vector2 c, Vector2 p)`
  （二维向量 ClosestPointOnTriangle（二维向量 a, 二维向量 b, 二维向量 c, 二维向量 p））
- `Vector3 ClosestPointOnTriangleXZ(Vector3 a, Vector3 b, Vector3 c, Vector3 p)`
  （三维向量 ClosestPointOnTriangleXZ（三维向量 a, 三维向量 b, 三维向量 c, 三维向量 p））
- `Vector3 ClosestPointOnTriangle(Vector3 a, Vector3 b, Vector3 c, Vector3 p)`
  （三维向量 ClosestPointOnTriangle（三维向量 a, 三维向量 b, 三维向量 c, 三维向量 p））
- `void CompressMesh(List<Int3> vertices, List<int> triangles, out Int3[] outVertices, out int[] outTriangles)`
  （void Compress网格（List<Int3> vertices, List<int> triangles, out Int3[] outVertices, out int[] outTriangles））
- `void TraceContours(Dictionary<int, int> outline, HashSet<int> hasInEdge, Action<List<int>, bool> results)`
  （void TraceContours（Dictionary<int, int> outline, HashSet<int> hasInEdge, Action<List<int>, bool> results））
- `void Subdivide(List<Vector3> points, List<Vector3> result, int subSegments)`
  （void Subdivide（List<Vector3> points, List<Vector3> result, int subSegments））

---

## PolygonCollider2D（PolygonCollider2D）

**继承**: Collider2D（Collider2D）

### 方法 (5)

- `int GetTotalPointCount()`
  （int 获取TotalPoint数量（））
- `Vector2[] get_points()`
  （Vector2[] get_points（））
- `int get_pathCount()`
  （int get_path数量（））
- `Vector2[] GetPath(int index)`
  （Vector2[] 获取路径（int index））
- `Vector2[] GetPath_Internal(int index)`
  （Vector2[] 获取Path_内部的（int index））

---

## PolygonPoint（PolygonPoint）

**继承**: TriangulationPoint（TriangulationPoint）

### 方法 (3)

- `PolygonPoint get_Next()`
  （PolygonPoint get_下一个（））
- `void set_Next(PolygonPoint value)`
  （void set_下一个（PolygonPoint value））
- `void set_Previous(PolygonPoint value)`
  （void set_上一个（PolygonPoint value））

---

## Poser（Poser）

**继承**: SolverManager（Solver管理器）

### 字段 (5)

- `Transform poseRoot`（变换 pose根）(偏移: 0x1C)
- `float weight`（float weight）(偏移: 0x20)
- `float localRotationWeight`（float localRotationWeight）(偏移: 0x24)
- `float localPositionWeight`（float localPositionWeight）(偏移: 0x28)
- `bool initiated`（bool initiated）(偏移: 0x2C)

### 方法 (4)

- `void UpdateManual()`
  （void 更新手动（））
- `void UpdateSolver()`
  （void 更新Solver（））
- `void InitiateSolver()`
  （void InitiateSolver（））
- `void FixTransforms()`
  （void FixTransforms（））

---

## PositionAsUV1（PositionAsUV1）

**继承**: BaseMeshEffect（基础网格特效）

### 方法 (1)

- `void ModifyMesh(VertexHelper vh)`
  （void Modify网格（Vertex辅助器 vh））

---

## PositionPredictor（PositionPredictor）

### 字段 (4)

- `Vector3 m_Velocity`（三维向量 m_速度）(偏移: 0x8)
- `Vector3 m_SmoothDampVelocity`（三维向量 m_SmoothDamp速度）(偏移: 0x14)
- `Vector3 m_Pos`（三维向量 m_Pos）(偏移: 0x20)
- `bool m_HavePos`（bool m_HavePos）(偏移: 0x2C)

### 方法 (8)

- `float get_Smoothing()`
  （float get_Smoothing（））
- `void set_Smoothing(float value)`
  （void set_Smoothing（float value））
- `bool IsEmpty()`
  （bool 是否空（））
- `void ApplyTransformDelta(Vector3 positionDelta)`
  （void 应用变换Delta（三维向量 positionDelta））
- `void Reset()`
  （void 重置（））
- `void AddPosition(Vector3 pos, float deltaTime, float lookaheadTime)`
  （void 添加Position（三维向量 pos, float deltaTime, float lookaheadTime））
- `Vector3 PredictPositionDelta(float lookaheadTime)`
  （三维向量 PredictPositionDelta（float lookaheadTime））
- `Vector3 PredictPosition(float lookaheadTime)`
  （三维向量 PredictPosition（float lookaheadTime））

---

## PostProcessData（Post处理数据）

**继承**: ScriptableObject（脚本对象）

### 字段 (2)

- `PostProcessData.ShaderResources shaders`（Post处理Data.着色器Resources shaders）(偏移: 0xC)
- `PostProcessData.TextureResources textures`（Post处理Data.纹理Resources textures）(偏移: 0x10)

---

## PostProcessData.ShaderResources（Post处理Data.着色器Resources）

### 字段 (11)

- `Shader stopNanPS`（着色器 stopNanPS）(偏移: 0x8)
- `Shader subpixelMorphologicalAntialiasingPS`（着色器 subpixelMorphologicalAntialiasingPS）(偏移: 0xC)
- `Shader gaussianDepthOfFieldPS`（着色器 gaussian深度OfFieldPS）(偏移: 0x10)
- `Shader bokehDepthOfFieldPS`（着色器 bokeh深度OfFieldPS）(偏移: 0x14)
- `Shader cameraMotionBlurPS`（着色器 cameraMotionBlurPS）(偏移: 0x18)
- `Shader paniniProjectionPS`（着色器 paniniProjectionPS）(偏移: 0x1C)
- `Shader lutBuilderLdrPS`（着色器 lut构建器LdrPS）(偏移: 0x20)
- `Shader lutBuilderHdrPS`（着色器 lut构建器HdrPS）(偏移: 0x24)
- `Shader bloomPS`（着色器 bloomPS）(偏移: 0x28)
- `Shader uberPostPS`（着色器 uberPostPS）(偏移: 0x2C)
- `Shader finalPostPassPS`（着色器 finalPostPassPS）(偏移: 0x30)

---

## PostProcessData.TextureResources（Post处理Data.纹理Resources）

### 字段 (4)

- `Texture2D[] blueNoise16LTex`（Texture2D[] blueNoise16LTex）(偏移: 0x8)
- `Texture2D[] filmGrainTex`（Texture2D[] filmGrainTex）(偏移: 0xC)
- `Texture2D smaaAreaTex`（Texture2D smaaAreaTex）(偏移: 0x10)
- `Texture2D smaaSearchTex`（Texture2D smaa搜索Tex）(偏移: 0x14)

---

## PostProcessPass（Post处理Pass）

**继承**: ScriptableRenderPass（ScriptableRenderPass）

### 字段 (36)

- `RenderTextureDescriptor m_Descriptor`（Render纹理Descriptor m_Descriptor）(偏移: 0x54)
- `RenderTargetHandle m_Source`（Render目标句柄 m_Source）(偏移: 0x88)
- `RenderTargetHandle m_Destination`（Render目标句柄 m_Destination）(偏移: 0xA8)
- `RenderTargetHandle m_Depth`（Render目标句柄 m_深度）(偏移: 0xC8)
- `RenderTargetHandle m_InternalLut`（Render目标句柄 m_内部的Lut）(偏移: 0xE8)
- `ProfilingSampler m_ProfilingRenderPostProcessing`（ProfilingSampler m_ProfilingRenderPostProcessing）(偏移: 0x0)
- `ProfilingSampler m_ProfilingRenderFinalPostProcessing`（ProfilingSampler m_ProfilingRenderFinalPostProcessing）(偏移: 0x4)
- `PostProcessPass.MaterialLibrary m_Materials`（Post处理Pass.材质Library m_Materials）(偏移: 0x108)
- `PostProcessData m_Data`（Post处理数据 m_数据）(偏移: 0x10C)
- `DepthOfField m_DepthOfField`（深度OfField m_深度OfField）(偏移: 0x110)
- `MotionBlur m_MotionBlur`（MotionBlur m_MotionBlur）(偏移: 0x114)
- `PaniniProjection m_PaniniProjection`（PaniniProjection m_PaniniProjection）(偏移: 0x118)
- `Bloom m_Bloom`（Bloom m_Bloom）(偏移: 0x11C)
- `LensDistortion m_LensDistortion`（LensDistortion m_LensDistortion）(偏移: 0x120)
- `ChromaticAberration m_ChromaticAberration`（ChromaticAberration m_ChromaticAberration）(偏移: 0x124)
- `Vignette m_Vignette`（Vignette m_Vignette）(偏移: 0x128)
- `ColorLookup m_ColorLookup`（颜色Lookup m_颜色Lookup）(偏移: 0x12C)
- `ColorAdjustments m_ColorAdjustments`（颜色Adjustments m_颜色Adjustments）(偏移: 0x130)
- `Tonemapping m_Tonemapping`（Tonemapping m_Tonemapping）(偏移: 0x134)
- `FilmGrain m_FilmGrain`（FilmGrain m_FilmGrain）(偏移: 0x138)
- `GraphicsFormat m_DefaultHDRFormat`（Graphics格式化 m_默认的HDR格式化）(偏移: 0x13C)
- `bool m_UseRGBM`（bool m_UseRGBM）(偏移: 0x140)
- `GraphicsFormat m_SMAAEdgeFormat`（Graphics格式化 m_SMAAEdge格式化）(偏移: 0x144)
- `GraphicsFormat m_GaussianCoCFormat`（Graphics格式化 m_GaussianCoC格式化）(偏移: 0x148)
- `Matrix4x4[] m_PrevViewProjM`（Matrix4x4[] m_Prev视图ProjM）(偏移: 0x14C)
- `bool m_ResetHistory`（bool m_重置History）(偏移: 0x150)
- `int m_DitheringTextureIndex`（int m_Dithering纹理索引）(偏移: 0x154)
- `RenderTargetIdentifier[] m_MRT2`（Render目标Identifier[] m_MRT2）(偏移: 0x158)
- `Vector4[] m_BokehKernel`（Vector4[] m_BokehKernel）(偏移: 0x15C)
- `int m_BokehHash`（int m_BokehHash）(偏移: 0x160)
- `bool m_IsFinalPass`（bool m_是否FinalPass）(偏移: 0x164)
- `bool m_HasFinalPass`（bool m_是否有FinalPass）(偏移: 0x0)
- `bool m_EnableSRGBConversionIfNeeded`（bool m_启用SRGBConversionIfNeeded）(偏移: 0x0)
- `bool m_UseDrawProcedural`（bool m_UseDrawProcedural）(偏移: 0x0)
- `Material m_BlitMaterial`（材质 m_Blit材质）(偏移: 0x0)
- `Matrix4x4[] viewProjMatrixStereo`（Matrix4x4[] viewProj矩阵Stereo）(偏移: 0x8)

### 方法 (33)

- `void Cleanup()`
  （void 清理（））
- `void Setup(in RenderTextureDescriptor baseDescriptor, in RenderTargetHandle source, in RenderTargetHandle destination, in RenderTargetHandle depth, in RenderTargetHandle internalLut, bool hasFinalPass, bool enableSRGBConversion)`
  （void Setup（in RenderTextureDescriptor baseDescriptor, in RenderTargetHandle source, in RenderTargetHandle destination, in RenderTargetHandle depth, in RenderTargetHandle internalLut, bool hasFinalPass, bool enableSRGBConversion））
- `void SetupFinalPass(in RenderTargetHandle source)`
  （void SetupFinalPass（in RenderTargetHandle source））
- `void OnCameraSetup(CommandBuffer cmd, ref RenderingData renderingData)`
  （void On摄像机Setup（Command缓冲区 cmd, ref RenderingData renderingData））
- `void OnCameraCleanup(CommandBuffer cmd)`
  （void On摄像机清理（Command缓冲区 cmd））
- `void ResetHistory()`
  （void 重置History（））
- `bool CanRunOnTile()`
  （bool 能否运行OnTile（））
- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（ScriptableRenderContext context, ref RenderingData renderingData））
- `RenderTextureDescriptor GetCompatibleDescriptor()`
  （Render纹理Descriptor 获取CompatibleDescriptor（））
- `RenderTextureDescriptor GetCompatibleDescriptor(int width, int height, GraphicsFormat format, int depthBufferBits = 0)`
  （Render纹理Descriptor 获取CompatibleDescriptor（int width, int height, Graphics格式化 format, int depthBufferBits = 0））
- `bool RequireSRGBConversionBlitToBackBuffer(CameraData cameraData)`
  （bool RequireSRGBConversionBlitTo后缓冲区（摄像机数据 cameraData））
- `void Blit(CommandBuffer cmd, RenderTargetIdentifier source, RenderTargetIdentifier destination, Material material, int passIndex = 0)`
  （void Blit（Command缓冲区 cmd, Render目标Identifier source, Render目标Identifier destination, 材质 material, int passIndex = 0））
- `void DrawFullscreenMesh(CommandBuffer cmd, Material material, int passIndex)`
  （void DrawFullscreen网格（Command缓冲区 cmd, 材质 material, int passIndex））
- `void Render(CommandBuffer cmd, ref RenderingData renderingData)`
  （void Render（Command缓冲区 cmd, ref RenderingData renderingData））
- `BuiltinRenderTextureType BlitDstDiscardContent(CommandBuffer cmd, RenderTargetIdentifier rt)`
  （BuiltinRender纹理类型 BlitDstDiscardContent（Command缓冲区 cmd, Render目标Identifier rt））
- `void DoSubpixelMorphologicalAntialiasing(ref CameraData cameraData, CommandBuffer cmd, int source, int destination)`
  （void DoSubpixelMorphologicalAntialiasing（ref CameraData cameraData, Command缓冲区 cmd, int source, int destination））
- `void DoDepthOfField(Camera camera, CommandBuffer cmd, int source, int destination, Rect pixelRect)`
  （void Do深度OfField（摄像机 camera, Command缓冲区 cmd, int source, int destination, Rect pixelRect））
- `void DoGaussianDepthOfField(Camera camera, CommandBuffer cmd, int source, int destination, Rect pixelRect)`
  （void DoGaussian深度OfField（摄像机 camera, Command缓冲区 cmd, int source, int destination, Rect pixelRect））
- `void PrepareBokehKernel()`
  （void PrepareBokehKernel（））
- `float GetMaxBokehRadiusInPixels(float viewportHeight)`
  （float 获取最大BokehRadiusInPixels（float viewportHeight））
- `void DoBokehDepthOfField(CommandBuffer cmd, int source, int destination, Rect pixelRect)`
  （void DoBokeh深度OfField（Command缓冲区 cmd, int source, int destination, Rect pixelRect））
- `void DoMotionBlur(CameraData cameraData, CommandBuffer cmd, int source, int destination)`
  （void DoMotionBlur（摄像机数据 cameraData, Command缓冲区 cmd, int source, int destination））
- `void DoPaniniProjection(Camera camera, CommandBuffer cmd, int source, int destination)`
  （void DoPaniniProjection（摄像机 camera, Command缓冲区 cmd, int source, int destination））
- `Vector2 CalcViewExtents(Camera camera)`
  （二维向量 Calc视图Extents（摄像机 camera））
- `Vector2 CalcCropExtents(Camera camera, float d)`
  （二维向量 CalcCropExtents（摄像机 camera, float d））
- `void SetupBloom(CommandBuffer cmd, int source, Material uberMaterial)`
  （void SetupBloom（Command缓冲区 cmd, int source, 材质 uberMaterial））
- `void SetupLensDistortion(Material material, bool isSceneView)`
  （void SetupLensDistortion（材质 material, bool isSceneView））
- `void SetupChromaticAberration(Material material)`
  （void SetupChromaticAberration（材质 material））
- `void SetupVignette(Material material)`
  （void SetupVignette（材质 material））
- `void SetupColorGrading(CommandBuffer cmd, ref RenderingData renderingData, Material material)`
  （void Setup颜色Grading（Command缓冲区 cmd, ref RenderingData renderingData, 材质 material））
- `void SetupGrain(in CameraData cameraData, Material material)`
  （void SetupGrain（in CameraData cameraData, 材质 material））
- `void SetupDithering(in CameraData cameraData, Material material)`
  （void SetupDithering（in CameraData cameraData, 材质 material））
- `void RenderFinalPass(CommandBuffer cmd, ref RenderingData renderingData)`
  （void RenderFinalPass（Command缓冲区 cmd, ref RenderingData renderingData））

---

## PostProcessPass.MaterialLibrary（Post处理Pass.材质Library）

### 字段 (9)

- `Material stopNaN`（材质 stopNaN）(偏移: 0x8)
- `Material subpixelMorphologicalAntialiasing`（材质 subpixelMorphologicalAntialiasing）(偏移: 0xC)
- `Material gaussianDepthOfField`（材质 gaussian深度OfField）(偏移: 0x10)
- `Material bokehDepthOfField`（材质 bokeh深度OfField）(偏移: 0x14)
- `Material cameraMotionBlur`（材质 cameraMotionBlur）(偏移: 0x18)
- `Material paniniProjection`（材质 paniniProjection）(偏移: 0x1C)
- `Material bloom`（材质 bloom）(偏移: 0x20)
- `Material uber`（材质 uber）(偏移: 0x24)
- `Material finalPass`（材质 finalPass）(偏移: 0x28)

### 方法 (2)

- `Material Load(Shader shader)`
  （材质 加载（着色器 shader））
- `void Cleanup()`
  （void 清理（））

---

## PostProcessPass.ShaderConstants（Post处理Pass.着色器Constants）

### 字段 (38)

- `int _TempTarget`（int _Temp目标）(偏移: 0x0)
- `int _TempTarget2`（int _TempTarget2）(偏移: 0x4)
- `int _StencilRef`（int _StencilRef）(偏移: 0x8)
- `int _StencilMask`（int _Stencil掩码）(偏移: 0xC)
- `int _FullCoCTexture`（int _满CoC纹理）(偏移: 0x10)
- `int _HalfCoCTexture`（int _HalfCoC纹理）(偏移: 0x14)
- `int _DofTexture`（int _Dof纹理）(偏移: 0x18)
- `int _CoCParams`（int _CoCParams）(偏移: 0x1C)
- `int _BokehKernel`（int _BokehKernel）(偏移: 0x20)
- `int _PongTexture`（int _Pong纹理）(偏移: 0x24)
- `int _PingTexture`（int _Ping纹理）(偏移: 0x28)
- `int _Metrics`（int _Metrics）(偏移: 0x2C)
- `int _AreaTexture`（int _Area纹理）(偏移: 0x30)
- `int _SearchTexture`（int _搜索纹理）(偏移: 0x34)
- `int _EdgeTexture`（int _Edge纹理）(偏移: 0x38)
- `int _BlendTexture`（int _Blend纹理）(偏移: 0x3C)
- `int _ColorTexture`（int _颜色纹理）(偏移: 0x40)
- `int _Params`（int _Params）(偏移: 0x44)
- `int _SourceTexLowMip`（int _SourceTexLowMip）(偏移: 0x48)
- `int _Bloom_Params`（int _Bloom_Params）(偏移: 0x4C)
- `int _Bloom_RGBM`（int _Bloom_RGBM）(偏移: 0x50)
- `int _Bloom_Texture`（int _Bloom_纹理）(偏移: 0x54)
- `int _LensDirt_Texture`（int _LensDirt_纹理）(偏移: 0x58)
- `int _LensDirt_Params`（int _LensDirt_Params）(偏移: 0x5C)
- `int _LensDirt_Intensity`（int _LensDirt_Intensity）(偏移: 0x60)
- `int _Distortion_Params1`（int _Distortion_Params1）(偏移: 0x64)
- `int _Distortion_Params2`（int _Distortion_Params2）(偏移: 0x68)
- `int _Chroma_Params`（int _Chroma_Params）(偏移: 0x6C)
- `int _Vignette_Params1`（int _Vignette_Params1）(偏移: 0x70)
- `int _Vignette_Params2`（int _Vignette_Params2）(偏移: 0x74)
- `int _Lut_Params`（int _Lut_Params）(偏移: 0x78)
- `int _UserLut_Params`（int _UserLut_Params）(偏移: 0x7C)
- `int _InternalLut`（int _内部的Lut）(偏移: 0x80)
- `int _UserLut`（int _UserLut）(偏移: 0x84)
- `int _DownSampleScaleFactor`（int _下Sample缩放系数）(偏移: 0x88)
- `int _FullscreenProjMat`（int _FullscreenProj材质）(偏移: 0x8C)
- `int[] _BloomMipUp`（int[] _BloomMip上）(偏移: 0x90)
- `int[] _BloomMipDown`（int[] _BloomMip下）(偏移: 0x94)

---

## PostProcessUtils（Post处理Utils）

### 方法 (5)

- `int ConfigureDithering(PostProcessData data, int index, Camera camera, Material material)`
  （int ConfigureDithering（Post处理数据 data, int index, 摄像机 camera, 材质 material））
- `int ConfigureDithering(PostProcessData data, int index, int cameraPixelWidth, int cameraPixelHeight, Material material)`
  （int ConfigureDithering（Post处理数据 data, int index, int cameraPixelWidth, int cameraPixelHeight, 材质 material））
- `void ConfigureFilmGrain(PostProcessData data, FilmGrain settings, Camera camera, Material material)`
  （void ConfigureFilmGrain（Post处理数据 data, FilmGrain settings, 摄像机 camera, 材质 material））
- `void ConfigureFilmGrain(PostProcessData data, FilmGrain settings, int cameraPixelWidth, int cameraPixelHeight, Material material)`
  （void ConfigureFilmGrain（Post处理数据 data, FilmGrain settings, int cameraPixelWidth, int cameraPixelHeight, 材质 material））
- `void SetSourceSize(CommandBuffer cmd, RenderTextureDescriptor desc)`
  （void 集合Source大小（Command缓冲区 cmd, Render纹理Descriptor desc））

---

## PostProcessUtils.ShaderConstants（Post处理Utils.着色器Constants）

### 字段 (6)

- `int _Grain_Texture`（int _Grain_纹理）(偏移: 0x0)
- `int _Grain_Params`（int _Grain_Params）(偏移: 0x4)
- `int _Grain_TilingParams`（int _Grain_TilingParams）(偏移: 0x8)
- `int _BlueNoise_Texture`（int _蓝色Noise_纹理）(偏移: 0xC)
- `int _Dithering_Params`（int _Dithering_Params）(偏移: 0x10)
- `int _SourceSize`（int _Source大小）(偏移: 0x14)

---

## PostProcessingData（PostProcessing数据）

### 字段 (2)

- `ColorGradingMode gradingMode`（颜色Grading模式 grading模式）(偏移: 0x0)
- `int lutSize`（int lut大小）(偏移: 0x4)

---

## PostureFloat（姿态浮点数）

### 字段 (5)

- `float standIdle`（float stand待机）(偏移: 0x0)
- `float crouchIdle`（float crouch待机）(偏移: 0x4)
- `float standRun`（float stand运行）(偏移: 0x8)
- `float crouchRun`（float crouch运行）(偏移: 0xC)
- `float floating`（float floating）(偏移: 0x10)

### 方法 (2)

- `float Get(ShootPosture posture)`
  （float 获取（射击姿态 posture））
- `float GetMultiplier(ShootPosture posture)`
  （float 获取Multiplier（射击姿态 posture））

---

## PreTile（PreTile）

### 字段 (4)

- `float4 planeLeft`（float4 plane左）(偏移: 0x0)
- `float4 planeRight`（float4 plane右）(偏移: 0x10)
- `float4 planeBottom`（float4 plane底部）(偏移: 0x20)
- `float4 planeTop`（float4 plane顶部）(偏移: 0x30)

---

## PreloadData（Preload数据）

**继承**: Object（对象）

### 方法 (1)

- `void PreloadDataDontStripMe()`
  （void Preload数据DontStripMe（））

---

## PrimalityTest（PrimalityTest）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `bool Invoke(BigInteger bi, ConfidenceFactor confidence)`
  （bool Invoke（BigInteger bi, Confidence系数 confidence））
- `IAsyncResult BeginInvoke(BigInteger bi, ConfidenceFactor confidence, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（BigInteger bi, Confidence系数 confidence, 异步回调 callback, object object））
- `bool EndInvoke(IAsyncResult result)`
  （bool 结束Invoke（I异步Result result））

---

## PrimalityTests（PrimalityTests）

### 方法 (4)

- `int GetSPPRounds(BigInteger bi, ConfidenceFactor confidence)`
  （int 获取SPPRounds（BigInteger bi, Confidence系数 confidence））
- `bool Test(BigInteger n, ConfidenceFactor confidence)`
  （bool Test（BigInteger n, Confidence系数 confidence））
- `bool RabinMillerTest(BigInteger n, ConfidenceFactor confidence)`
  （bool RabinMillerTest（BigInteger n, Confidence系数 confidence））
- `bool SmallPrimeSppTest(BigInteger bi, ConfidenceFactor confidence)`
  （bool SmallPrimeSppTest（BigInteger bi, Confidence系数 confidence））

---

## PrimeGeneratorBase（PrimeGenerator基础）

### 方法 (3)

- `ConfidenceFactor get_Confidence()`
  （Confidence系数 get_Confidence（））
- `PrimalityTest get_PrimalityTest()`
  （PrimalityTest get_PrimalityTest（））
- `int get_TrialDivisionBounds()`
  （int get_TrialDivisionBounds（））

---

## PrimitiveArray（Primitive数组）

### 字段 (12)

- `InternalPrimitiveTypeE code`（内部的Primitive类型E code）(偏移: 0x8)
- `bool[] booleanA`（bool[] booleanA）(偏移: 0xC)
- `char[] charA`（char[] charA）(偏移: 0x10)
- `double[] doubleA`（double[] doubleA）(偏移: 0x14)
- `short[] int16A`（short[] int16A）(偏移: 0x18)
- `int[] int32A`（int[] int32A）(偏移: 0x1C)
- `long[] int64A`（long[] int64A）(偏移: 0x20)
- `sbyte[] sbyteA`（sbyte[] sbyteA）(偏移: 0x24)
- `float[] singleA`（float[] singleA）(偏移: 0x28)
- `ushort[] uint16A`（ushort[] uint16A）(偏移: 0x2C)
- `uint[] uint32A`（uint[] uint32A）(偏移: 0x30)
- `ulong[] uint64A`（ulong[] uint64A）(偏移: 0x34)

### 方法 (2)

- `void Init(InternalPrimitiveTypeE code, Array array)`
  （void 初始化（内部的Primitive类型E code, 数组 array））
- `void SetValue(string value, int index)`
  （void 集合值（string value, int index））

---

## PrimitiveType（Primitive类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Priority（Priority）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ProceduralGridMover（Procedural网格Mover）

**继承**: VersionedMonoBehaviour（VersionedMonoBehaviour）

### 字段 (4)

- `float updateDistance`（float update距离）(偏移: 0x10)
- `Transform target`（变换 target）(偏移: 0x14)
- `GridGraph graph`（网格Graph graph）(偏移: 0x18)
- `GridNodeBase[] buffer`（网格节点Base[] buffer）(偏移: 0x1C)

### 方法 (7)

- `bool get_updatingGraph()`
  （bool get_updatingGraph（））
- `void set_updatingGraph(bool value)`
  （void set_updatingGraph（bool value））
- `void Start()`
  （void 开始（））
- `void Update()`
  （void 更新（））
- `Vector3 PointToGraphSpace(Vector3 p)`
  （三维向量 PointToGraphSpace（三维向量 p））
- `void UpdateGraph()`
  （void 更新Graph（））
- `IEnumerator UpdateGraphCoroutine()`
  （IEnumerator 更新Graph协程（））

---

## ProceduralWorld（Procedural世界的）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (8)

- `Transform target`（变换 target）(偏移: 0xC)
- `ProceduralWorld.ProceduralPrefab[] prefabs`（ProceduralWorld.ProceduralPrefab[] prefabs）(偏移: 0x10)
- `int range`（int range）(偏移: 0x14)
- `int disableAsyncLoadWithinRange`（int disable异步加载Within范围）(偏移: 0x18)
- `float tileSize`（float tile大小）(偏移: 0x1C)
- `int subTiles`（int subTiles）(偏移: 0x20)
- `bool staticBatching`（bool staticBatching）(偏移: 0x24)
- `Queue<IEnumerator> tileGenerationQueue`（Queue<IEnumerator> tileGeneration队列）(偏移: 0x28)

### 方法 (3)

- `void Start()`
  （void 开始（））
- `void Update()`
  （void 更新（））
- `IEnumerator GenerateTiles()`
  （IEnumerator GenerateTiles（））

---

## ProceduralWorld.ProceduralPrefab（ProceduralWorld.Procedural预制体）

### 字段 (9)

- `GameObject prefab`（游戏对象 prefab）(偏移: 0x8)
- `float density`（float density）(偏移: 0xC)
- `float perlin`（float perlin）(偏移: 0x10)
- `float perlinPower`（float perlin力度）(偏移: 0x14)
- `Vector2 perlinOffset`（二维向量 perlinOffset）(偏移: 0x18)
- `float perlinScale`（float perlin缩放）(偏移: 0x20)
- `float random`（float random）(偏移: 0x24)
- `ProceduralWorld.RotationRandomness randomRotation`（ProceduralWorld.RotationRandomness randomRotation）(偏移: 0x28)
- `bool singleFixed`（bool single固定）(偏移: 0x2C)

---

## ProceduralWorld.ProceduralTile（ProceduralWorld.ProceduralTile）

### 字段 (6)

- `int x`（int x）(偏移: 0x8)
- `int z`（int z）(偏移: 0xC)
- `Random rnd`（随机 rnd）(偏移: 0x10)
- `ProceduralWorld world`（Procedural世界的 world）(偏移: 0x14)
- `Transform root`（变换 root）(偏移: 0x1C)
- `IEnumerator ie`（IEnumerator ie）(偏移: 0x20)

### 方法 (9)

- `bool get_destroyed()`
  （bool get_destroyed（））
- `void set_destroyed(bool value)`
  （void set_destroyed（bool value））
- `IEnumerator Generate()`
  （IEnumerator Generate（））
- `void ForceFinish()`
  （void 强制Finish（））
- `Vector3 RandomInside()`
  （三维向量 随机Inside（））
- `Vector3 RandomInside(float px, float pz)`
  （三维向量 随机Inside（float px, float pz））
- `Quaternion RandomYRot(ProceduralWorld.ProceduralPrefab prefab)`
  （Quaternion 随机YRot（ProceduralWorld.Procedural预制体 prefab））
- `IEnumerator InternalGenerate()`
  （IEnumerator 内部的Generate（））
- `void Destroy()`
  （void 销毁（））

---

## ProceduralWorld.RotationRandomness（ProceduralWorld.RotationRandomness）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ProcessingState（Processing状态）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ProcessorArchitecture（ProcessorArchitecture）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Profile（Profile）

### 字段 (6)

- `string name`（string name）(偏移: 0x8)
- `Stopwatch watch`（Stopwatch watch）(偏移: 0xC)
- `int counter`（int counter）(偏移: 0x10)
- `long mem`（long mem）(偏移: 0x18)
- `long smem`（long smem）(偏移: 0x20)
- `int control`（int control）(偏移: 0x28)

### 方法 (10)

- `int ControlValue()`
  （int 控制值（））
- `void WriteCSV(string path, Profile[] profiles)`
  （void WriteCSV（string path, Profile[] profiles））
- `void Run(Action action)`
  （void 运行（动作 action））
- `void Start()`
  （void 开始（））
- `void Stop()`
  （void 停止（））
- `void Log()`
  （void Log（））
- `void ConsoleLog()`
  （void ConsoleLog（））
- `void Stop(int control)`
  （void 停止（int control））
- `void Control(Profile other)`
  （void 控制（Profile other））
- `string ToString()`
  （string To字符串（））

---

## Profiler（Profiler）

### 方法 (2)

- `void EndThreadProfiling()`
  （void 结束ThreadProfiling（））
- `long GetRuntimeMemorySizeLong(Object o)`
  （long 获取RuntimeMemory大小Long（对象 o））

---

## ProfilerMarker（ProfilerMarker）

### 字段 (1)

- `IntPtr m_Ptr`（整数Ptr m_Ptr）(偏移: 0x0)

### 方法 (1)

- `ProfilerMarker.AutoScope Auto()`
  （ProfilerMarker.自动瞄准镜 自动（））

---

## ProfilerMarker.AutoScope（ProfilerMarker.自动瞄准镜）

**继承**: IDisposable（IDisposable）

### 字段 (1)

- `IntPtr m_Ptr`（整数Ptr m_Ptr）(偏移: 0x0)

### 方法 (1)

- `void Dispose()`
  （void 释放（））

---

## ProfilerUnsafeUtility（ProfilerUnsafe工具）

### 方法 (3)

- `IntPtr CreateMarker(string name, ushort categoryId, MarkerFlags flags, int metadataCount)`
  （整数Ptr 创建Marker（string name, ushort categoryId, MarkerFlags flags, int metadataCount））
- `void BeginSample(IntPtr markerPtr)`
  （void BeginSample（整数Ptr markerPtr））
- `void EndSample(IntPtr markerPtr)`
  （void 结束Sample（整数Ptr markerPtr））

---

## ProfilingSample（ProfilingSample）

**继承**: IDisposable（IDisposable）

### 字段 (4)

- `CommandBuffer m_Cmd`（Command缓冲区 m_Cmd）(偏移: 0x0)
- `string m_Name`（string m_名称）(偏移: 0x4)
- `bool m_Disposed`（bool m_Disposed）(偏移: 0x8)
- `CustomSampler m_Sampler`（自定义的Sampler m_Sampler）(偏移: 0xC)

### 方法 (2)

- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））

---

## ProfilingSampler（ProfilingSampler）

### 字段 (2)

- `Recorder m_Recorder`（Recorder m_Recorder）(偏移: 0x14)
- `Recorder m_InlineRecorder`（Recorder m_InlineRecorder）(偏移: 0x18)

### 方法 (16)

- `void Begin(CommandBuffer cmd)`
  （void Begin（Command缓冲区 cmd））
- `void End(CommandBuffer cmd)`
  （void 结束（Command缓冲区 cmd））
- `bool IsValid()`
  （bool 是否Valid（））
- `CustomSampler get_sampler()`
  （自定义的Sampler get_sampler（））
- `void set_sampler(CustomSampler value)`
  （void set_sampler（自定义的Sampler value））
- `CustomSampler get_inlineSampler()`
  （自定义的Sampler get_inlineSampler（））
- `void set_inlineSampler(CustomSampler value)`
  （void set_inlineSampler（自定义的Sampler value））
- `string get_name()`
  （string get_name（））
- `void set_name(string value)`
  （void set_name（string value））
- `void set_enableRecording(bool value)`
  （void set_enableRecording（bool value））
- `float get_gpuElapsedTime()`
  （float get_gpuElapsed时间（））
- `int get_gpuSampleCount()`
  （int get_gpuSample数量（））
- `float get_cpuElapsedTime()`
  （float get_cpuElapsed时间（））
- `int get_cpuSampleCount()`
  （int get_cpuSample数量（））
- `float get_inlineCpuElapsedTime()`
  （float get_inlineCpuElapsed时间（））
- `int get_inlineCpuSampleCount()`
  （int get_inlineCpuSample数量（））

---

## ProfilingScope（Profiling瞄准镜）

**继承**: IDisposable（IDisposable）

### 方法 (1)

- `void Dispose()`
  （void 释放（））

---

## Progress（Progress）

### 字段 (2)

- `float progress`（float progress）(偏移: 0x0)
- `string description`（string description）(偏移: 0x4)

### 方法 (2)

- `Progress MapTo(float min, float max, string prefix)`
  （Progress 映射To（float min, float max, string prefix））
- `string ToString()`
  （string To字符串（））

---

## PropertyAnalysis（属性Analysis）

### 字段 (4)

- `string name`（string name）(偏移: 0x8)
- `MethodInfo getterInfo`（Method信息 getter信息）(偏移: 0xC)
- `TraceLoggingTypeInfo typeInfo`（TraceLogging类型信息 type信息）(偏移: 0x10)
- `EventFieldAttribute fieldAttribute`（事件FieldAttribute fieldAttribute）(偏移: 0x14)

---

## PropertyAttributes（属性Attributes）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## PropertyBuilder（属性构建器）

**继承**: PropertyInfo（属性信息）

### 方法 (16)

- `PropertyAttributes get_Attributes()`
  （属性Attributes get_Attributes（））
- `bool get_CanRead()`
  （bool get_能否Read（））
- `bool get_CanWrite()`
  （bool get_能否Write（））
- `Type get_DeclaringType()`
  （类型 get_Declaring类型（））
- `string get_Name()`
  （string get_名称（））
- `Type get_PropertyType()`
  （类型 get_属性类型（））
- `ParameterInfo[] GetIndexParameters()`
  （ParameterInfo[] 获取索引Parameters（））
- `Type get_ReflectedType()`
  （类型 get_Reflected类型（））
- `MethodInfo[] GetAccessors(bool nonPublic)`
  （MethodInfo[] 获取Accessors（bool nonPublic））
- `object[] GetCustomAttributes(bool inherit)`
  （object[] 获取自定义的Attributes（bool inherit））
- `object[] GetCustomAttributes(Type attributeType, bool inherit)`
  （object[] 获取自定义的Attributes（类型 attributeType, bool inherit））
- `MethodInfo GetGetMethod(bool nonPublic)`
  （Method信息 获取获取Method（bool nonPublic））
- `MethodInfo GetSetMethod(bool nonPublic)`
  （Method信息 获取集合Method（bool nonPublic））
- `object GetValue(object obj, BindingFlags invokeAttr, Binder binder, object[] index, CultureInfo culture)`
  （object 获取值（object obj, BindingFlags invokeAttr, Binder binder, object[] index, Culture信息 culture））
- `bool IsDefined(Type attributeType, bool inherit)`
  （bool 是否Defined（类型 attributeType, bool inherit））
- `void SetValue(object obj, object value, BindingFlags invokeAttr, Binder binder, object[] index, CultureInfo culture)`
  （void 集合值（object obj, object value, BindingFlags invokeAttr, Binder binder, object[] index, Culture信息 culture））

---

## PropertyDescriptor（属性Descriptor）

**继承**: MemberDescriptor（MemberDescriptor）

### 字段 (4)

- `TypeConverter converter`（类型Converter converter）(偏移: 0x34)
- `object[] editors`（object[] editors）(偏移: 0x38)
- `Type[] editorTypes`（Type[] editorTypes）(偏移: 0x3C)
- `int editorCount`（int editor数量）(偏移: 0x40)

### 方法 (3)

- `bool Equals(object obj)`
  （bool Equals（object obj））
- `void FillAttributes(IList attributeList)`
  （void FillAttributes（I列表 attributeList））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## PropertyDescriptorCollection（属性DescriptorCollection）

**继承**: ICollection, IEnumerable, IList, IDictionary（ICollection, IEnumerable, I列表, I字典）

### 字段 (10)

- `PropertyDescriptorCollection Empty`（属性DescriptorCollection 空）(偏移: 0x0)
- `IDictionary cachedFoundProperties`（I字典 cachedFoundProperties）(偏移: 0x8)
- `bool cachedIgnoreCase`（bool cachedIgnoreCase）(偏移: 0xC)
- `PropertyDescriptor[] properties`（属性Descriptor[] properties）(偏移: 0x10)
- `int propCount`（int prop数量）(偏移: 0x14)
- `string[] namedSort`（string[] namedSort）(偏移: 0x18)
- `IComparer comparer`（IComparer comparer）(偏移: 0x1C)
- `bool propsOwned`（bool propsOwned）(偏移: 0x20)
- `bool needSort`（bool needSort）(偏移: 0x21)
- `bool readOnly`（bool readOnly）(偏移: 0x22)

### 方法 (18)

- `int get_Count()`
  （int get_数量（））
- `PropertyDescriptor get_Item(int index)`
  （属性Descriptor get_项目（int index））
- `PropertyDescriptor get_Item(string name)`
  （属性Descriptor get_项目（string name））
- `int Add(PropertyDescriptor value)`
  （int 添加（属性Descriptor value））
- `void Clear()`
  （void 清除（））
- `bool Contains(PropertyDescriptor value)`
  （bool Contains（属性Descriptor value））
- `void CopyTo(Array array, int index)`
  （void 复制To（数组 array, int index））
- `void EnsurePropsOwned()`
  （void EnsurePropsOwned（））
- `void EnsureSize(int sizeNeeded)`
  （void Ensure大小（int sizeNeeded））
- `PropertyDescriptor Find(string name, bool ignoreCase)`
  （属性Descriptor 查找（string name, bool ignoreCase））
- `int IndexOf(PropertyDescriptor value)`
  （int 索引Of（属性Descriptor value））
- `void Insert(int index, PropertyDescriptor value)`
  （void Insert（int index, 属性Descriptor value））
- `void Remove(PropertyDescriptor value)`
  （void 移除（属性Descriptor value））
- `void RemoveAt(int index)`
  （void 移除At（int index））
- `PropertyDescriptorCollection Sort(string[] names)`
  （属性DescriptorCollection Sort（string[] names））
- `void InternalSort(string[] names)`
  （void 内部的Sort（string[] names））
- `void InternalSort(IComparer sorter)`
  （void 内部的Sort（IComparer sorter））
- `IEnumerator GetEnumerator()`
  （IEnumerator 获取Enumerator（））

---

## PropertyDescriptorCollection.PropertyDescriptorEnumerator（属性DescriptorCollection.属性DescriptorEnumerator）

**继承**: IDictionaryEnumerator, IEnumerator（I字典Enumerator, IEnumerator）

### 字段 (2)

- `PropertyDescriptorCollection owner`（属性DescriptorCollection owner）(偏移: 0x8)
- `int index`（int index）(偏移: 0xC)

### 方法 (6)

- `object get_Current()`
  （object get_当前（））
- `DictionaryEntry get_Entry()`
  （字典Entry get_Entry（））
- `object get_Key()`
  （object get_键（））
- `object get_Value()`
  （object get_值（））
- `bool MoveNext()`
  （bool 移动下一个（））
- `void Reset()`
  （void 重置（））

---

## PropertyInfo（属性信息）

**继承**: MemberInfo, _PropertyInfo（Member信息, _属性信息）

### 方法 (16)

- `MemberTypes get_MemberType()`
  （MemberTypes get_Member类型（））
- `MethodInfo GetGetMethod()`
  （Method信息 获取获取Method（））
- `MethodInfo GetSetMethod()`
  （Method信息 获取集合Method（））
- `object GetValue(object obj, object[] index)`
  （object 获取值（object obj, object[] index））
- `void SetValue(object obj, object value, object[] index)`
  （void 集合值（object obj, object value, object[] index））
- `Type[] GetOptionalCustomModifiers()`
  （Type[] 获取Optional自定义的Modifiers（））
- `Type[] GetRequiredCustomModifiers()`
  （Type[] 获取Required自定义的Modifiers（））
- `NotImplementedException CreateNIE()`
  （NotImplementedException 创建NIE（））
- `object GetConstantValue()`
  （object 获取Constant值（））
- `object GetRawConstantValue()`
  （object 获取RawConstant值（））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool op_Equality(PropertyInfo left, PropertyInfo right)`
  （bool op_Equality（属性信息 left, 属性信息 right））
- `bool op_Inequality(PropertyInfo left, PropertyInfo right)`
  （bool op_Inequality（属性信息 left, 属性信息 right））
- `PropertyInfo internal_from_handle_type(IntPtr event_handle, IntPtr type_handle)`
  （属性信息 internal_from_handle_type（整数Ptr event_handle, 整数Ptr type_handle））
- `PropertyInfo GetPropertyFromHandle(RuntimePropertyHandle handle, RuntimeTypeHandle reflectedType)`
  （属性信息 获取属性From句柄（Runtime属性句柄 handle, Runtime类型句柄 reflectedType））

---

## PropertyModifier（属性修改器）

### 字段 (1)

- `PlayerRefFloat modifier`（玩家Ref浮点数 modifier）(偏移: 0x8)

### 方法 (1)

- `float Get(Player player)`
  （float 获取（玩家 player））

---

## PropertyName（属性名称）

**继承**: IEquatable<PropertyName>（IEquatable<属性Name>）

### 字段 (1)

- `int id`（int id）(偏移: 0x0)

### 方法 (5)

- `bool op_Equality(PropertyName lhs, PropertyName rhs)`
  （bool op_Equality（属性名称 lhs, 属性名称 rhs））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool Equals(object other)`
  （bool Equals（object other））
- `bool Equals(PropertyName other)`
  （bool Equals（属性名称 other））
- `string ToString()`
  （string To字符串（））

---

## ProvidePropertyAttribute（Provide属性Attribute）

**继承**: Attribute（Attribute）

### 字段 (2)

- `string propertyName`（string property名称）(偏移: 0x8)
- `string receiverTypeName`（string receiver类型名称）(偏移: 0xC)

### 方法 (2)

- `string get_PropertyName()`
  （string get_属性名称（））
- `string get_ReceiverTypeName()`
  （string get_Receiver类型名称（））

---

## ProviderData（提供者数据）

### 字段 (5)

- `string Ref`（string Ref）(偏移: 0x8)
- `string Type`（string 类型）(偏移: 0xC)
- `string Id`（string Id）(偏移: 0x10)
- `Hashtable CustomProperties`（Hashtable 自定义的Properties）(偏移: 0x14)
- `IList CustomData`（I列表 自定义的数据）(偏移: 0x18)

### 方法 (1)

- `void CopyFrom(ProviderData other)`
  （void 复制From（提供者数据 other））

---

## ProxyAttribute（代理Attribute）

**继承**: Attribute（Attribute）

### 方法 (2)

- `MarshalByRefObject CreateInstance(Type serverType)`
  （MarshalByRef对象 创建实例（类型 serverType））
- `RealProxy CreateProxy(ObjRef objRef, Type serverType, object serverObject, Context serverContext)`
  （Real代理 创建代理（ObjRef objRef, 类型 serverType, object serverObject, Context serverContext））

---

## ProxyElement（代理元素）

**继承**: ConfigurationElement（Configuration元素）

### 方法 (1)

- `ConfigurationPropertyCollection get_Properties()`
  （Configuration属性Collection get_Properties（））

---

## PublicKey（公开的键）

### 字段 (4)

- `AsnEncodedData _keyValue`（AsnEncoded数据 _key值）(偏移: 0x8)
- `AsnEncodedData _params`（AsnEncoded数据 _params）(偏移: 0xC)
- `Oid _oid`（Oid _oid）(偏移: 0x10)
- `byte[] Empty`（byte[] 空）(偏移: 0x0)

### 方法 (3)

- `AsnEncodedData get_EncodedKeyValue()`
  （AsnEncoded数据 get_Encoded键值（））
- `AsnEncodedData get_EncodedParameters()`
  （AsnEncoded数据 get_EncodedParameters（））
- `Oid get_Oid()`
  （Oid get_Oid（））

---

## PunctualLightData（Punctual光照数据）

### 字段 (7)

- `Vector3 wsPos`（三维向量 wsPos）(偏移: 0x0)
- `float radius`（float radius）(偏移: 0xC)
- `Vector4 color`（Vector4 color）(偏移: 0x10)
- `Vector4 attenuation`（Vector4 attenuation）(偏移: 0x20)
- `Vector3 spotDirection`（三维向量 spot方向）(偏移: 0x30)
- `int lightIndex`（int light索引）(偏移: 0x3C)
- `Vector4 occlusionProbeInfo`（Vector4 occlusionProbe信息）(偏移: 0x40)

---

## PureQuaternionPlugin（PureQuaternion插件）

**继承**: ABSTweenPlugin<Quaternion, Quaternion, NoOptions>（ABSTweenPlugin<Quaternion, Quaternion, NoOptions>）

### 字段 (1)

- `PureQuaternionPlugin _plug`（PureQuaternion插件 _plug）(偏移: 0x3123311A)

### 方法 (9)

- `PureQuaternionPlugin Plug()`
  （PureQuaternion插件 Plug（））
- `void Reset(TweenerCore<Quaternion, Quaternion, NoOptions> t)`
  （void 重置（TweenerCore<Quaternion, Quaternion, NoOptions> t））
- `void SetFrom(TweenerCore<Quaternion, Quaternion, NoOptions> t, bool isRelative)`
  （void 集合From（TweenerCore<Quaternion, Quaternion, NoOptions> t, bool isRelative））
- `void SetFrom(TweenerCore<Quaternion, Quaternion, NoOptions> t, Quaternion fromValue, bool setImmediately, bool isRelative)`
  （void 集合From（TweenerCore<Quaternion, Quaternion, NoOptions> t, Quaternion fromValue, bool setImmediately, bool isRelative））
- `Quaternion ConvertToStartValue(TweenerCore<Quaternion, Quaternion, NoOptions> t, Quaternion value)`
  （Quaternion 转换To开始值（TweenerCore<Quaternion, Quaternion, NoOptions> t, Quaternion value））
- `void SetRelativeEndValue(TweenerCore<Quaternion, Quaternion, NoOptions> t)`
  （void 集合Relative结束值（TweenerCore<Quaternion, Quaternion, NoOptions> t））
- `void SetChangeValue(TweenerCore<Quaternion, Quaternion, NoOptions> t)`
  （void 集合Change值（TweenerCore<Quaternion, Quaternion, NoOptions> t））
- `float GetSpeedBasedDuration(NoOptions options, float unitsXSecond, Quaternion changeValue)`
  （float 获取SpeedBased持续时间（NoOptions options, float unitsXSecond, Quaternion changeValue））
- `void EvaluateAndApply(NoOptions options, Tween t, bool isRelative, DOGetter<Quaternion> getter, DOSetter<Quaternion> setter, float elapsed, Quaternion startValue, Quaternion changeValue, float duration, bool usingInversePosition, UpdateNotice updateNotice)`
  （void EvaluateAnd应用（NoOptions options, Tween t, bool isRelative, DOGetter<Quaternion> getter, DOSetter<Quaternion> setter, float elapsed, Quaternion startValue, Quaternion changeValue, float duration, bool usingInversePosition, 更新Notice updateNotice））

---

## QVModel（QV模型）

**继承**: Model（模型）

### 字段 (8)

- `Rigidbody rigidBody`（刚体 rigid身体）(偏移: 0x40)
- `QVModel.Data left`（QVModel.数据 left）(偏移: 0x44)
- `QVModel.Data right`（QVModel.数据 right）(偏移: 0x7C)
- `float giveUpScale`（float give上缩放）(偏移: 0xB4)
- `Weapon bindWpn`（Weapon bind武器）(偏移: 0xB8)
- `Transform pickUpArea`（变换 pick上Area）(偏移: 0xC0)
- `float startCheckPickUpTime`（float start检查Pick上时间）(偏移: 0xC4)
- `Vector3 giveUpScale_3rd`（三维向量 give上Scale_3rd）(偏移: 0x0)

### 方法 (13)

- `bool get_isDropState()`
  （bool get_isDrop状态（））
- `bool get_isMapGun()`
  （bool get_is映射枪械（））
- `void set_isMapGun(bool value)`
  （void set_is映射枪械（bool value））
- `void SetOnCharacter(CharacterModel character)`
  （void 集合On角色（角色模型 character））
- `void GiveUp(Weapon weapon, Vector3 pos, Quaternion rotation, float speed)`
  （void 放弃（Weapon weapon, 三维向量 pos, Quaternion rotation, float speed））
- `void TryRecycle(bool roundRecycle)`
  （void TryRecycle（bool roundRecycle））
- `void Recycle(bool roundRecycle)`
  （void Recycle（bool roundRecycle））
- `void RecycleModel()`
  （void Recycle模型（））
- `void SetVisible(bool visible)`
  （void 集合可见的（bool visible））
- `void SetGunFireState(bool leftHand, bool state)`
  （void 集合枪械开火状态（bool leftHand, bool state））
- `void StopGunFire()`
  （void 停止枪械开火（））
- `void SetOnMap(Transform setPos, Vector3 localPos, Vector3 localEuler)`
  （void 集合On映射（变换 setPos, 三维向量 localPos, 三维向量 localEuler））
- `void OnTriggerStay(Collider other)`
  （void On触发器Stay（碰撞器 other））

---

## QVModel.Data（QVModel.数据）

### 字段 (6)

- `Transform Model`（变换 模型）(偏移: 0x0)
- `Vector3 Pos_OnHand`（三维向量 Pos_On手部）(偏移: 0x4)
- `Vector3 Euler_OnHand`（三维向量 Euler_On手部）(偏移: 0x10)
- `Vector3 Pos_GiveUp`（三维向量 Pos_Give上）(偏移: 0x1C)
- `Vector3 Euler_GiveUp`（三维向量 Euler_Give上）(偏移: 0x28)
- `ParticleSystem GunFire`（粒子系统 枪械开火）(偏移: 0x34)

---

## QuaTools（QuaTools）

### 方法 (13)

- `Quaternion Lerp(Quaternion fromRotation, Quaternion toRotation, float weight)`
  （Quaternion Lerp（Quaternion fromRotation, Quaternion toRotation, float weight））
- `Quaternion Slerp(Quaternion fromRotation, Quaternion toRotation, float weight)`
  （Quaternion Slerp（Quaternion fromRotation, Quaternion toRotation, float weight））
- `Quaternion LinearBlend(Quaternion q, float weight)`
  （Quaternion LinearBlend（Quaternion q, float weight））
- `Quaternion SphericalBlend(Quaternion q, float weight)`
  （Quaternion SphericalBlend（Quaternion q, float weight））
- `Quaternion FromToAroundAxis(Vector3 fromDirection, Vector3 toDirection, Vector3 axis)`
  （Quaternion FromToAround轴（三维向量 fromDirection, 三维向量 toDirection, 三维向量 axis））
- `Quaternion RotationToLocalSpace(Quaternion space, Quaternion rotation)`
  （Quaternion RotationTo本地的Space（Quaternion space, Quaternion rotation））
- `Quaternion FromToRotation(Quaternion from, Quaternion to)`
  （Quaternion FromToRotation（Quaternion from, Quaternion to））
- `Vector3 GetAxis(Vector3 v)`
  （三维向量 获取轴（三维向量 v））
- `Quaternion ClampRotation(Quaternion rotation, float clampWeight, int clampSmoothing)`
  （Quaternion ClampRotation（Quaternion rotation, float clampWeight, int clampSmoothing））
- `float ClampAngle(float angle, float clampWeight, int clampSmoothing)`
  （float Clamp角度（float angle, float clampWeight, int clampSmoothing））
- `Quaternion MatchRotation(Quaternion targetRotation, Vector3 targetforwardAxis, Vector3 targetUpAxis, Vector3 forwardAxis, Vector3 upAxis)`
  （Quaternion 比赛Rotation（Quaternion targetRotation, 三维向量 targetforwardAxis, 三维向量 targetUpAxis, 三维向量 forwardAxis, 三维向量 upAxis））
- `Vector3 ToBiPolar(Vector3 euler)`
  （三维向量 ToBiPolar（三维向量 euler））
- `float ToBiPolar(float angle)`
  （float ToBiPolar（float angle））

---

## QualitySettings（QualitySettings）

**继承**: Object（对象）

### 方法 (6)

- `ShadowmaskMode get_shadowmaskMode()`
  （Shadowmask模式 get_shadowmask模式（））
- `void set_vSyncCount(int value)`
  （void set_v同步数量（int value））
- `int get_antiAliasing()`
  （int get_antiAliasing（））
- `void set_antiAliasing(int value)`
  （void set_antiAliasing（int value））
- `int get_maxQueuedFrames()`
  （int get_maxQueuedFrames（））
- `ColorSpace get_activeColorSpace()`
  （颜色Space get_active颜色Space（））

---

## Quaternion（Quaternion）

**继承**: IEquatable<Quaternion>, IFormattable（IEquatable<Quaternion>, IFormattable）

### 字段 (5)

- `float x`（float x）(偏移: 0x0)
- `float y`（float y）(偏移: 0x4)
- `float z`（float z）(偏移: 0x8)
- `float w`（float w）(偏移: 0xC)
- `Quaternion identityQuaternion`（Quaternion identityQuaternion）(偏移: 0x0)

### 方法 (43)

- `Quaternion FromToRotation(Vector3 fromDirection, Vector3 toDirection)`
  （Quaternion FromToRotation（三维向量 fromDirection, 三维向量 toDirection））
- `Quaternion Inverse(Quaternion rotation)`
  （Quaternion Inverse（Quaternion rotation））
- `Quaternion Slerp(Quaternion a, Quaternion b, float t)`
  （Quaternion Slerp（Quaternion a, Quaternion b, float t））
- `Quaternion SlerpUnclamped(Quaternion a, Quaternion b, float t)`
  （Quaternion SlerpUnclamped（Quaternion a, Quaternion b, float t））
- `Quaternion Lerp(Quaternion a, Quaternion b, float t)`
  （Quaternion Lerp（Quaternion a, Quaternion b, float t））
- `Quaternion Internal_FromEulerRad(Vector3 euler)`
  （Quaternion Internal_FromEulerRad（三维向量 euler））
- `Vector3 Internal_ToEulerRad(Quaternion rotation)`
  （三维向量 Internal_ToEulerRad（Quaternion rotation））
- `void Internal_ToAxisAngleRad(Quaternion q, out Vector3 axis, out float angle)`
  （void Internal_To轴角度Rad（Quaternion q, out Vector3 axis, out float angle））
- `Quaternion AngleAxis(float angle, Vector3 axis)`
  （Quaternion 角度轴（float angle, 三维向量 axis））
- `Quaternion LookRotation(Vector3 forward, Vector3 upwards)`
  （Quaternion LookRotation（三维向量 forward, 三维向量 upwards））
- `Quaternion LookRotation(Vector3 forward)`
  （Quaternion LookRotation（三维向量 forward））
- `Quaternion get_identity()`
  （Quaternion get_identity（））
- `Quaternion op_Multiply(Quaternion lhs, Quaternion rhs)`
  （Quaternion op_Multiply（Quaternion lhs, Quaternion rhs））
- `Vector3 op_Multiply(Quaternion rotation, Vector3 point)`
  （三维向量 op_Multiply（Quaternion rotation, 三维向量 point））
- `bool IsEqualUsingDot(float dot)`
  （bool 是否EqualUsingDot（float dot））
- `bool op_Equality(Quaternion lhs, Quaternion rhs)`
  （bool op_Equality（Quaternion lhs, Quaternion rhs））
- `bool op_Inequality(Quaternion lhs, Quaternion rhs)`
  （bool op_Inequality（Quaternion lhs, Quaternion rhs））
- `float Dot(Quaternion a, Quaternion b)`
  （float Dot（Quaternion a, Quaternion b））
- `float Angle(Quaternion a, Quaternion b)`
  （float 角度（Quaternion a, Quaternion b））
- `Vector3 Internal_MakePositive(Vector3 euler)`
  （三维向量 Internal_MakePositive（三维向量 euler））
- `Vector3 get_eulerAngles()`
  （三维向量 get_eulerAngles（））
- `Quaternion Euler(float x, float y, float z)`
  （Quaternion Euler（float x, float y, float z））
- `Quaternion Euler(Vector3 euler)`
  （Quaternion Euler（三维向量 euler））
- `void ToAngleAxis(out float angle, out Vector3 axis)`
  （void To角度轴（out float angle, out Vector3 axis））
- `Quaternion RotateTowards(Quaternion from, Quaternion to, float maxDegreesDelta)`
  （Quaternion RotateTowards（Quaternion from, Quaternion to, float maxDegreesDelta））
- `Quaternion Normalize(Quaternion q)`
  （Quaternion Normalize（Quaternion q））
- `Quaternion get_normalized()`
  （Quaternion get_normalized（））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool Equals(object other)`
  （bool Equals（object other））
- `bool Equals(Quaternion other)`
  （bool Equals（Quaternion other））
- `string ToString()`
  （string To字符串（））
- `string ToString(string format)`
  （string To字符串（string format））
- `string ToString(string format, IFormatProvider formatProvider)`
  （string To字符串（string format, I格式化提供者 formatProvider））
- `void FromToRotation_Injected(ref Vector3 fromDirection, ref Vector3 toDirection, out Quaternion ret)`
  （void FromToRotation_Injected（ref Vector3 fromDirection, ref Vector3 toDirection, out Quaternion ret））
- `void Inverse_Injected(ref Quaternion rotation, out Quaternion ret)`
  （void Inverse_Injected（ref Quaternion rotation, out Quaternion ret））
- `void Slerp_Injected(ref Quaternion a, ref Quaternion b, float t, out Quaternion ret)`
  （void Slerp_Injected（ref Quaternion a, ref Quaternion b, float t, out Quaternion ret））
- `void SlerpUnclamped_Injected(ref Quaternion a, ref Quaternion b, float t, out Quaternion ret)`
  （void SlerpUnclamped_Injected（ref Quaternion a, ref Quaternion b, float t, out Quaternion ret））
- `void Lerp_Injected(ref Quaternion a, ref Quaternion b, float t, out Quaternion ret)`
  （void Lerp_Injected（ref Quaternion a, ref Quaternion b, float t, out Quaternion ret））
- `void Internal_FromEulerRad_Injected(ref Vector3 euler, out Quaternion ret)`
  （void Internal_FromEulerRad_Injected（ref Vector3 euler, out Quaternion ret））
- `void Internal_ToEulerRad_Injected(ref Quaternion rotation, out Vector3 ret)`
  （void Internal_ToEulerRad_Injected（ref Quaternion rotation, out Vector3 ret））
- `void Internal_ToAxisAngleRad_Injected(ref Quaternion q, out Vector3 axis, out float angle)`
  （void Internal_To轴角度Rad_Injected（ref Quaternion q, out Vector3 axis, out float angle））
- `void AngleAxis_Injected(float angle, ref Vector3 axis, out Quaternion ret)`
  （void 角度Axis_Injected（float angle, ref Vector3 axis, out Quaternion ret））
- `void LookRotation_Injected(ref Vector3 forward, ref Vector3 upwards, out Quaternion ret)`
  （void LookRotation_Injected（ref Vector3 forward, ref Vector3 upwards, out Quaternion ret））

---

## QuaternionOptions（QuaternionOptions）

**继承**: IPlugOptions（IPlugOptions）

### 字段 (5)

- `RotateMode rotateMode`（Rotate模式 rotate模式）(偏移: 0x0)
- `AxisConstraint axisConstraint`（轴Constraint axisConstraint）(偏移: 0x4)
- `Vector3 up`（三维向量 up）(偏移: 0x8)
- `bool dynamicLookAt`（bool dynamicLookAt）(偏移: 0x14)
- `Vector3 dynamicLookAtWorldPosition`（三维向量 dynamicLookAt世界的Position）(偏移: 0x18)

### 方法 (1)

- `void Reset()`
  （void 重置（））

---

## QuaternionPlugin（Quaternion插件）

**继承**: ABSTweenPlugin<Quaternion, Vector3, QuaternionOptions>（ABSTweenPlugin<Quaternion, 三维向量, QuaternionOptions>）

### 方法 (8)

- `void Reset(TweenerCore<Quaternion, Vector3, QuaternionOptions> t)`
  （void 重置（TweenerCore<Quaternion, 三维向量, QuaternionOptions> t））
- `void SetFrom(TweenerCore<Quaternion, Vector3, QuaternionOptions> t, bool isRelative)`
  （void 集合From（TweenerCore<Quaternion, 三维向量, QuaternionOptions> t, bool isRelative））
- `void SetFrom(TweenerCore<Quaternion, Vector3, QuaternionOptions> t, Vector3 fromValue, bool setImmediately, bool isRelative)`
  （void 集合From（TweenerCore<Quaternion, 三维向量, QuaternionOptions> t, 三维向量 fromValue, bool setImmediately, bool isRelative））
- `Vector3 ConvertToStartValue(TweenerCore<Quaternion, Vector3, QuaternionOptions> t, Quaternion value)`
  （三维向量 转换To开始值（TweenerCore<Quaternion, 三维向量, QuaternionOptions> t, Quaternion value））
- `void SetRelativeEndValue(TweenerCore<Quaternion, Vector3, QuaternionOptions> t)`
  （void 集合Relative结束值（TweenerCore<Quaternion, 三维向量, QuaternionOptions> t））
- `void SetChangeValue(TweenerCore<Quaternion, Vector3, QuaternionOptions> t)`
  （void 集合Change值（TweenerCore<Quaternion, 三维向量, QuaternionOptions> t））
- `float GetSpeedBasedDuration(QuaternionOptions options, float unitsXSecond, Vector3 changeValue)`
  （float 获取SpeedBased持续时间（QuaternionOptions options, float unitsXSecond, 三维向量 changeValue））
- `void EvaluateAndApply(QuaternionOptions options, Tween t, bool isRelative, DOGetter<Quaternion> getter, DOSetter<Quaternion> setter, float elapsed, Vector3 startValue, Vector3 changeValue, float duration, bool usingInversePosition, UpdateNotice updateNotice)`
  （void EvaluateAnd应用（QuaternionOptions options, Tween t, bool isRelative, DOGetter<Quaternion> getter, DOSetter<Quaternion> setter, float elapsed, 三维向量 startValue, 三维向量 changeValue, float duration, bool usingInversePosition, 更新Notice updateNotice））

---

## QueryTriggerInteraction（Query触发器Interaction）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Queue（队列）

**继承**: ICollection, IEnumerable, ICloneable（ICollection, IEnumerable, ICloneable）

### 字段 (7)

- `object[] _array`（object[] _array）(偏移: 0x8)
- `int _head`（int _head）(偏移: 0xC)
- `int _tail`（int _tail）(偏移: 0x10)
- `int _size`（int _size）(偏移: 0x14)
- `int _growFactor`（int _grow系数）(偏移: 0x18)
- `int _version`（int _version）(偏移: 0x1C)
- `object _syncRoot`（object _sync根）(偏移: 0x20)

### 方法 (11)

- `int get_Count()`
  （int get_数量（））
- `object Clone()`
  （object 克隆（））
- `object get_SyncRoot()`
  （object get_同步根（））
- `void CopyTo(Array array, int index)`
  （void 复制To（数组 array, int index））
- `void Enqueue(object obj)`
  （void Enqueue（object obj））
- `IEnumerator GetEnumerator()`
  （IEnumerator 获取Enumerator（））
- `object Dequeue()`
  （object Dequeue（））
- `object Peek()`
  （object Peek（））
- `object GetElement(int i)`
  （object 获取元素（int i））
- `object[] ToArray()`
  （object[] To数组（））
- `void SetCapacity(int capacity)`
  （void 集合Capacity（int capacity））

---

## Queue.QueueDebugView（Queue.队列Debug视图）

### 字段 (1)

- `Queue queue`（队列 queue）(偏移: 0x8)

### 方法 (1)

- `object[] get_Items()`
  （object[] get_Items（））

---

## Queue.QueueEnumerator（Queue.队列Enumerator）

**继承**: IEnumerator, ICloneable（IEnumerator, ICloneable）

### 字段 (4)

- `Queue _q`（队列 _q）(偏移: 0x8)
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

## QueueUserWorkItemCallback（队列UserWork项目回调）

**继承**: IThreadPoolWorkItem（IThread池Work项目）

### 字段 (4)

- `WaitCallback callback`（Wait回调 callback）(偏移: 0x8)
- `ExecutionContext context`（ExecutionContext context）(偏移: 0xC)
- `object state`（object state）(偏移: 0x10)
- `ContextCallback ccb`（Context回调 ccb）(偏移: 0x0)

### 方法 (1)

- `void WaitCallback_Context(object state)`
  （void WaitCallback_Context（object state））

---

## RC2（RC2）

**继承**: SymmetricAlgorithm（SymmetricAlgorithm）

### 字段 (3)

- `int EffectiveKeySizeValue`（int Effective键大小值）(偏移: 0x2C)
- `KeySizes[] s_legalBlockSizes`（键Sizes[] s_legalBlockSizes）(偏移: 0x0)
- `KeySizes[] s_legalKeySizes`（键Sizes[] s_legal键Sizes）(偏移: 0x4)

### 方法 (3)

- `int get_EffectiveKeySize()`
  （int get_Effective键大小（））
- `int get_KeySize()`
  （int get_键大小（））
- `void set_KeySize(int value)`
  （void set_键大小（int value））

---

## RC2CryptoServiceProvider（RC2Crypto服务提供者）

**继承**: RC2（RC2）

### 字段 (2)

- `bool m_use40bitSalt`（bool m_use40bitSalt）(偏移: 0x30)
- `KeySizes[] s_legalKeySizes`（键Sizes[] s_legal键Sizes）(偏移: 0x0)

### 方法 (5)

- `int get_EffectiveKeySize()`
  （int get_Effective键大小（））
- `ICryptoTransform CreateEncryptor(byte[] rgbKey, byte[] rgbIV)`
  （ICrypto变换 创建Encryptor（byte[] rgbKey, byte[] rgbIV））
- `ICryptoTransform CreateDecryptor(byte[] rgbKey, byte[] rgbIV)`
  （ICrypto变换 创建Decryptor（byte[] rgbKey, byte[] rgbIV））
- `void GenerateKey()`
  （void Generate键（））
- `void GenerateIV()`
  （void GenerateIV（））

---

## RC2Transform（RC2变换）

**继承**: SymmetricTransform（Symmetric变换）

### 字段 (7)

- `ushort R0`（ushort R0）(偏移: 0x34)
- `ushort R1`（ushort R1）(偏移: 0x36)
- `ushort R2`（ushort R2）(偏移: 0x38)
- `ushort R3`（ushort R3）(偏移: 0x3A)
- `ushort[] K`（ushort[] K）(偏移: 0x3C)
- `int j`（int j）(偏移: 0x40)
- `byte[] pitable`（byte[] pitable）(偏移: 0x0)

### 方法 (1)

- `void ECB(byte[] input, byte[] output)`
  （void ECB（byte[] input, byte[] output））

---

## RIPEMD160Managed（RIPEMD160Managed）

**继承**: RIPEMD160（RIPEMD160）

### 字段 (4)

- `byte[] _buffer`（byte[] _buffer）(偏移: 0x18)
- `long _count`（long _count）(偏移: 0x20)
- `uint[] _stateMD160`（uint[] _stateMD160）(偏移: 0x28)
- `uint[] _blockDWords`（uint[] _blockDWords）(偏移: 0x2C)

### 方法 (12)

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
- `void MDTransform(uint* blockDWords, uint* state, byte* block)`
  （void MD变换（uint* blockDWords, uint* state, byte* block））
- `uint F(uint x, uint y, uint z)`
  （uint F（uint x, uint y, uint z））
- `uint G(uint x, uint y, uint z)`
  （uint G（uint x, uint y, uint z））
- `uint H(uint x, uint y, uint z)`
  （uint H（uint x, uint y, uint z））
- `uint I(uint x, uint y, uint z)`
  （uint I（uint x, uint y, uint z））
- `uint J(uint x, uint y, uint z)`
  （uint J（uint x, uint y, uint z））

---

## RNGCryptoServiceProvider（RNGCrypto服务提供者）

**继承**: RandomNumberGenerator（随机NumberGenerator）

### 字段 (2)

- `object _lock`（object _lock）(偏移: 0x0)
- `IntPtr _handle`（整数Ptr _handle）(偏移: 0x8)

### 方法 (8)

- `void Check()`
  （void 检查（））
- `bool RngOpen()`
  （bool Rng打开（））
- `IntPtr RngInitialize(byte[] seed)`
  （整数Ptr Rng初始化（byte[] seed））
- `IntPtr RngGetBytes(IntPtr handle, byte[] data)`
  （整数Ptr Rng获取Bytes（整数Ptr handle, byte[] data））
- `void RngClose(IntPtr handle)`
  （void Rng关闭（整数Ptr handle））
- `void GetBytes(byte[] data)`
  （void 获取Bytes（byte[] data））
- `void Finalize()`
  （void Finalize（））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））

---

## RO_WorkListener（RO_Work监听器）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 方法 (2)

- `void Awake()`
  （void Awake（））
- `void Work()`
  （void Work（））

---

## RSA（RSA）

**继承**: AsymmetricAlgorithm（AsymmetricAlgorithm）

### 方法 (1)

- `string ToXmlString(bool includePrivateParameters)`
  （string ToXml字符串（bool includePrivateParameters））

---

## RSACryptoServiceProvider（RSACrypto服务提供者）

**继承**: RSA（RSA）

### 字段 (7)

- `CspProviderFlags s_UseMachineKeyStore`（Csp提供者Flags s_UseMachine键商店）(偏移: 0x0)
- `KeyPairPersistence store`（键PairPersistence store）(偏移: 0x10)
- `bool persistKey`（bool persist键）(偏移: 0x14)
- `bool persisted`（bool persisted）(偏移: 0x15)
- `bool privateKeyExportable`（bool private键Exportable）(偏移: 0x16)
- `bool m_disposed`（bool m_disposed）(偏移: 0x17)
- `RSAManaged rsa`（RSAManaged rsa）(偏移: 0x18)

### 方法 (7)

- `bool get_UseMachineKeyStore()`
  （bool get_UseMachine键商店（））
- `void Common(int dwKeySize, bool parameters)`
  （void Common（int dwKeySize, bool parameters））
- `void Finalize()`
  （void Finalize（））
- `int get_KeySize()`
  （int get_键大小（））
- `RSAParameters ExportParameters(bool includePrivateParameters)`
  （RSAParameters ExportParameters（bool includePrivateParameters））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））
- `void OnKeyGenerated(object sender, EventArgs e)`
  （void On键Generated（object sender, 事件Args e））

---

## RSAManaged（RSAManaged）

**继承**: RSA（RSA）

### 字段 (13)

- `bool isCRTpossible`（bool isCRTpossible）(偏移: 0x10)
- `bool keyBlinding`（bool keyBlinding）(偏移: 0x11)
- `bool keypairGenerated`（bool keypairGenerated）(偏移: 0x12)
- `bool m_disposed`（bool m_disposed）(偏移: 0x13)
- `BigInteger d`（BigInteger d）(偏移: 0x14)
- `BigInteger p`（BigInteger p）(偏移: 0x18)
- `BigInteger q`（BigInteger q）(偏移: 0x1C)
- `BigInteger dp`（BigInteger dp）(偏移: 0x20)
- `BigInteger dq`（BigInteger dq）(偏移: 0x24)
- `BigInteger qInv`（BigInteger qInv）(偏移: 0x28)
- `BigInteger n`（BigInteger n）(偏移: 0x2C)
- `BigInteger e`（BigInteger e）(偏移: 0x30)
- `RSAManaged.KeyGeneratedEventHandler KeyGenerated`（RSAManaged.键Generated事件处理器 键Generated）(偏移: 0x34)

### 方法 (10)

- `void Finalize()`
  （void Finalize（））
- `void GenerateKeyPair()`
  （void Generate键Pair（））
- `int get_KeySize()`
  （int get_键大小（））
- `bool get_PublicOnly()`
  （bool get_公开的Only（））
- `RSAParameters ExportParameters(bool includePrivateParameters)`
  （RSAParameters ExportParameters（bool includePrivateParameters））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））
- `void add_KeyGenerated(RSAManaged.KeyGeneratedEventHandler value)`
  （void add_键Generated（RSAManaged.键Generated事件处理器 value））
- `void remove_KeyGenerated(RSAManaged.KeyGeneratedEventHandler value)`
  （void remove_键Generated（RSAManaged.键Generated事件处理器 value））
- `string ToXmlString(bool includePrivateParameters)`
  （string ToXml字符串（bool includePrivateParameters））
- `byte[] GetPaddedValue(BigInteger value, int length)`
  （byte[] 获取Padded值（BigInteger value, int length））

---

## RSAManaged.KeyGeneratedEventHandler（RSAManaged.键Generated事件处理器）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(object sender, EventArgs e)`
  （void Invoke（object sender, 事件Args e））
- `IAsyncResult BeginInvoke(object sender, EventArgs e, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（object sender, 事件Args e, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## RSAPKCS1SignatureDescription（RSAPKCS1SignatureDescription）

**继承**: SignatureDescription（SignatureDescription）

### 字段 (1)

- `string _hashAlgorithm`（string _hashAlgorithm）(偏移: 0x18)

---

## RSAParameters（RSAParameters）

### 字段 (8)

- `byte[] Exponent`（byte[] Exponent）(偏移: 0x0)
- `byte[] Modulus`（byte[] Modulus）(偏移: 0x4)
- `byte[] P`（byte[] P）(偏移: 0x8)
- `byte[] Q`（byte[] Q）(偏移: 0xC)
- `byte[] DP`（byte[] DP）(偏移: 0x10)
- `byte[] DQ`（byte[] DQ）(偏移: 0x14)
- `byte[] InverseQ`（byte[] InverseQ）(偏移: 0x18)
- `byte[] D`（byte[] D）(偏移: 0x1C)

---

## RTHandle（RT句柄）

### 字段 (9)

- `RTHandleSystem m_Owner`（RT句柄系统 m_Owner）(偏移: 0x8)
- `RenderTexture m_RT`（Render纹理 m_RT）(偏移: 0xC)
- `Texture m_ExternalTexture`（纹理 m_外部的纹理）(偏移: 0x10)
- `RenderTargetIdentifier m_NameID`（Render目标Identifier m_名称ID）(偏移: 0x14)
- `bool m_EnableMSAA`（bool m_启用MSAA）(偏移: 0x30)
- `bool m_EnableRandomWrite`（bool m_启用随机Write）(偏移: 0x31)
- `bool m_EnableHWDynamicScale`（bool m_启用HW动态的缩放）(偏移: 0x32)
- `string m_Name`（string m_名称）(偏移: 0x34)
- `ScaleFunc scaleFunc`（缩放Func scaleFunc）(偏移: 0x40)

### 方法 (22)

- `Vector2 get_scaleFactor()`
  （二维向量 get_scale系数（））
- `void set_scaleFactor(Vector2 value)`
  （void set_scale系数（二维向量 value））
- `bool get_useScaling()`
  （bool get_useScaling（））
- `void set_useScaling(bool value)`
  （void set_useScaling（bool value））
- `Vector2Int get_referenceSize()`
  （二维向量整数 get_reference大小（））
- `void set_referenceSize(Vector2Int value)`
  （void set_reference大小（二维向量整数 value））
- `RTHandleProperties get_rtHandleProperties()`
  （RT句柄Properties get_rt句柄Properties（））
- `RenderTexture get_rt()`
  （Render纹理 get_rt（））
- `RenderTargetIdentifier get_nameID()`
  （Render目标Identifier get_nameID（））
- `string get_name()`
  （string get_name（））
- `bool get_isMSAAEnabled()`
  （bool get_isMSAA启用的（））
- `RenderTexture op_Implicit(RTHandle handle)`
  （Render纹理 op_Implicit（RT句柄 handle））
- `Texture op_Implicit(RTHandle handle)`
  （纹理 op_Implicit（RT句柄 handle））
- `RenderTargetIdentifier op_Implicit(RTHandle handle)`
  （Render目标Identifier op_Implicit（RT句柄 handle））
- `void SetRenderTexture(RenderTexture rt)`
  （void 集合Render纹理（Render纹理 rt））
- `void SetTexture(Texture tex)`
  （void 集合纹理（纹理 tex））
- `void SetTexture(RenderTargetIdentifier tex)`
  （void 集合纹理（Render目标Identifier tex））
- `void Release()`
  （void Release（））
- `Vector2Int GetScaledSize(Vector2Int refSize)`
  （二维向量整数 获取Scaled大小（二维向量整数 refSize））
- `void SwitchToFastMemory(CommandBuffer cmd, float residencyFraction = 1, FastMemoryFlags flags = 1, bool copyContents = False)`
  （void SwitchToFastMemory（Command缓冲区 cmd, float residencyFraction = 1, FastMemoryFlags flags = 1, bool copyContents = False））
- `void CopyToFastMemory(CommandBuffer cmd, float residencyFraction = 1, FastMemoryFlags flags = 1)`
  （void 复制ToFastMemory（Command缓冲区 cmd, float residencyFraction = 1, FastMemoryFlags flags = 1））
- `void SwitchOutFastMemory(CommandBuffer cmd, bool copyContents = True)`
  （void SwitchOutFastMemory（Command缓冲区 cmd, bool copyContents = True））

---

## RTHandleProperties（RT句柄Properties）

### 字段 (5)

- `Vector2Int previousViewportSize`（二维向量整数 previousViewport大小）(偏移: 0x0)
- `Vector2Int previousRenderTargetSize`（二维向量整数 previousRender目标大小）(偏移: 0x8)
- `Vector2Int currentViewportSize`（二维向量整数 currentViewport大小）(偏移: 0x10)
- `Vector2Int currentRenderTargetSize`（二维向量整数 currentRender目标大小）(偏移: 0x18)
- `Vector4 rtHandleScale`（Vector4 rt句柄缩放）(偏移: 0x20)

---

## RTHandleSystem（RT句柄系统）

**继承**: IDisposable（IDisposable）

### 字段 (9)

- `bool m_HardwareDynamicResRequested`（bool m_Hardware动态的ResRequested）(偏移: 0x8)
- `bool m_ScaledRTSupportsMSAA`（bool m_ScaledRTSupportsMSAA）(偏移: 0x9)
- `MSAASamples m_ScaledRTCurrentMSAASamples`（MSAASamples m_ScaledRT当前MSAASamples）(偏移: 0xC)
- `HashSet<RTHandle> m_AutoSizedRTs`（HashSet<RTHandle> m_自动SizedRTs）(偏移: 0x10)
- `RTHandle[] m_AutoSizedRTsArray`（RTHandle[] m_自动SizedRTs数组）(偏移: 0x14)
- `HashSet<RTHandle> m_ResizeOnDemandRTs`（HashSet<RTHandle> m_ResizeOnDemandRTs）(偏移: 0x18)
- `RTHandleProperties m_RTHandleProperties`（RT句柄Properties m_RT句柄Properties）(偏移: 0x1C)
- `int m_MaxWidths`（int m_最大Widths）(偏移: 0x4C)
- `int m_MaxHeights`（int m_最大Heights）(偏移: 0x50)

### 方法 (25)

- `RTHandleProperties get_rtHandleProperties()`
  （RT句柄Properties get_rt句柄Properties（））
- `void Dispose()`
  （void 释放（））
- `void Initialize(int width, int height, bool scaledRTsupportsMSAA, MSAASamples scaledRTMSAASamples)`
  （void 初始化（int width, int height, bool scaledRTsupportsMSAA, MSAASamples scaledRTMSAASamples））
- `void Release(RTHandle rth)`
  （void Release（RT句柄 rth））
- `void Remove(RTHandle rth)`
  （void 移除（RT句柄 rth））
- `void ResetReferenceSize(int width, int height)`
  （void 重置引用大小（int width, int height））
- `void SetReferenceSize(int width, int height, MSAASamples msaaSamples)`
  （void 集合引用大小（int width, int height, MSAASamples msaaSamples））
- `void SetReferenceSize(int width, int height, MSAASamples msaaSamples, bool reset)`
  （void 集合引用大小（int width, int height, MSAASamples msaaSamples, bool reset））
- `void SetHardwareDynamicResolutionState(bool enableHWDynamicRes)`
  （void 集合Hardware动态的Resolution状态（bool enableHWDynamicRes））
- `void SwitchResizeMode(RTHandle rth, RTHandleSystem.ResizeMode mode)`
  （void SwitchResize模式（RT句柄 rth, RT句柄System.Resize模式 mode））
- `void DemandResize(RTHandle rth)`
  （void DemandResize（RT句柄 rth））
- `int GetMaxWidth()`
  （int 获取最大宽度（））
- `int GetMaxHeight()`
  （int 获取最大高度（））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））
- `void Resize(int width, int height, MSAASamples msaaSamples, bool sizeChanged, bool msaaSampleChanged)`
  （void Resize（int width, int height, MSAASamples msaaSamples, bool sizeChanged, bool msaaSampleChanged））
- `RTHandle Alloc(int width, int height, int slices = 1, DepthBits depthBufferBits = 0, GraphicsFormat colorFormat = 4, FilterMode filterMode = 0, TextureWrapMode wrapMode = 0, TextureDimension dimension = 2, bool enableRandomWrite = False, bool useMipMap = False, bool autoGenerateMips = True, bool isShadowMap = False, int anisoLevel = 1, float mipMapBias = 0, MSAASamples msaaSamples = 1, bool bindTextureMS = False, bool useDynamicScale = False, RenderTextureMemoryless memoryless = 0, string name = "")`
  （RT句柄 Alloc（int width, int height, int slices = 1, 深度Bits depthBufferBits = 0, Graphics格式化 colorFormat = 4, Filter模式 filterMode = 0, 纹理Wrap模式 wrapMode = 0, 纹理Dimension dimension = 2, bool enableRandomWrite = False, bool useMipMap = False, bool autoGenerateMips = True, bool isShadowMap = False, int anisoLevel = 1, float mipMapBias = 0, MSAASamples msaaSamples = 1, bool bindTextureMS = False, bool useDynamicScale = False, Render纹理Memoryless memoryless = 0, string name = ""））
- `RTHandle Alloc(Vector2 scaleFactor, int slices = 1, DepthBits depthBufferBits = 0, GraphicsFormat colorFormat = 4, FilterMode filterMode = 0, TextureWrapMode wrapMode = 0, TextureDimension dimension = 2, bool enableRandomWrite = False, bool useMipMap = False, bool autoGenerateMips = True, bool isShadowMap = False, int anisoLevel = 1, float mipMapBias = 0, bool enableMSAA = False, bool bindTextureMS = False, bool useDynamicScale = False, RenderTextureMemoryless memoryless = 0, string name = "")`
  （RT句柄 Alloc（二维向量 scaleFactor, int slices = 1, 深度Bits depthBufferBits = 0, Graphics格式化 colorFormat = 4, Filter模式 filterMode = 0, 纹理Wrap模式 wrapMode = 0, 纹理Dimension dimension = 2, bool enableRandomWrite = False, bool useMipMap = False, bool autoGenerateMips = True, bool isShadowMap = False, int anisoLevel = 1, float mipMapBias = 0, bool enableMSAA = False, bool bindTextureMS = False, bool useDynamicScale = False, Render纹理Memoryless memoryless = 0, string name = ""））
- `RTHandle Alloc(ScaleFunc scaleFunc, int slices = 1, DepthBits depthBufferBits = 0, GraphicsFormat colorFormat = 4, FilterMode filterMode = 0, TextureWrapMode wrapMode = 0, TextureDimension dimension = 2, bool enableRandomWrite = False, bool useMipMap = False, bool autoGenerateMips = True, bool isShadowMap = False, int anisoLevel = 1, float mipMapBias = 0, bool enableMSAA = False, bool bindTextureMS = False, bool useDynamicScale = False, RenderTextureMemoryless memoryless = 0, string name = "")`
  （RT句柄 Alloc（缩放Func scaleFunc, int slices = 1, 深度Bits depthBufferBits = 0, Graphics格式化 colorFormat = 4, Filter模式 filterMode = 0, 纹理Wrap模式 wrapMode = 0, 纹理Dimension dimension = 2, bool enableRandomWrite = False, bool useMipMap = False, bool autoGenerateMips = True, bool isShadowMap = False, int anisoLevel = 1, float mipMapBias = 0, bool enableMSAA = False, bool bindTextureMS = False, bool useDynamicScale = False, Render纹理Memoryless memoryless = 0, string name = ""））
- `RTHandle AllocAutoSizedRenderTexture(int width, int height, int slices, DepthBits depthBufferBits, GraphicsFormat colorFormat, FilterMode filterMode, TextureWrapMode wrapMode, TextureDimension dimension, bool enableRandomWrite, bool useMipMap, bool autoGenerateMips, bool isShadowMap, int anisoLevel, float mipMapBias, bool enableMSAA, bool bindTextureMS, bool useDynamicScale, RenderTextureMemoryless memoryless, string name)`
  （RT句柄 Alloc自动SizedRender纹理（int width, int height, int slices, 深度Bits depthBufferBits, Graphics格式化 colorFormat, Filter模式 filterMode, 纹理Wrap模式 wrapMode, 纹理Dimension dimension, bool enableRandomWrite, bool useMipMap, bool autoGenerateMips, bool isShadowMap, int anisoLevel, float mipMapBias, bool enableMSAA, bool bindTextureMS, bool useDynamicScale, Render纹理Memoryless memoryless, string name））
- `RTHandle Alloc(RenderTexture texture)`
  （RT句柄 Alloc（Render纹理 texture））
- `RTHandle Alloc(Texture texture)`
  （RT句柄 Alloc（纹理 texture））
- `RTHandle Alloc(RenderTargetIdentifier texture)`
  （RT句柄 Alloc（Render目标Identifier texture））
- `RTHandle Alloc(RenderTargetIdentifier texture, string name)`
  （RT句柄 Alloc（Render目标Identifier texture, string name））
- `RTHandle Alloc(RTHandle tex)`
  （RT句柄 Alloc（RT句柄 tex））
- `string DumpRTInfo()`
  （string DumpRT信息（））

---

## RTHandleSystem.ResizeMode（RT句柄System.Resize模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## RTHandles（RTHandles）

### 字段 (1)

- `RTHandleSystem s_DefaultInstance`（RT句柄系统 s_默认的实例）(偏移: 0x30BD30B6)

### 方法 (16)

- `int get_maxWidth()`
  （int get_max宽度（））
- `int get_maxHeight()`
  （int get_max高度（））
- `RTHandleProperties get_rtHandleProperties()`
  （RT句柄Properties get_rt句柄Properties（））
- `RTHandle Alloc(int width, int height, int slices = 1, DepthBits depthBufferBits = 0, GraphicsFormat colorFormat = 4, FilterMode filterMode = 0, TextureWrapMode wrapMode = 0, TextureDimension dimension = 2, bool enableRandomWrite = False, bool useMipMap = False, bool autoGenerateMips = True, bool isShadowMap = False, int anisoLevel = 1, float mipMapBias = 0, MSAASamples msaaSamples = 1, bool bindTextureMS = False, bool useDynamicScale = False, RenderTextureMemoryless memoryless = 0, string name = "")`
  （RT句柄 Alloc（int width, int height, int slices = 1, 深度Bits depthBufferBits = 0, Graphics格式化 colorFormat = 4, Filter模式 filterMode = 0, 纹理Wrap模式 wrapMode = 0, 纹理Dimension dimension = 2, bool enableRandomWrite = False, bool useMipMap = False, bool autoGenerateMips = True, bool isShadowMap = False, int anisoLevel = 1, float mipMapBias = 0, MSAASamples msaaSamples = 1, bool bindTextureMS = False, bool useDynamicScale = False, Render纹理Memoryless memoryless = 0, string name = ""））
- `RTHandle Alloc(Vector2 scaleFactor, int slices = 1, DepthBits depthBufferBits = 0, GraphicsFormat colorFormat = 4, FilterMode filterMode = 0, TextureWrapMode wrapMode = 0, TextureDimension dimension = 2, bool enableRandomWrite = False, bool useMipMap = False, bool autoGenerateMips = True, bool isShadowMap = False, int anisoLevel = 1, float mipMapBias = 0, bool enableMSAA = False, bool bindTextureMS = False, bool useDynamicScale = False, RenderTextureMemoryless memoryless = 0, string name = "")`
  （RT句柄 Alloc（二维向量 scaleFactor, int slices = 1, 深度Bits depthBufferBits = 0, Graphics格式化 colorFormat = 4, Filter模式 filterMode = 0, 纹理Wrap模式 wrapMode = 0, 纹理Dimension dimension = 2, bool enableRandomWrite = False, bool useMipMap = False, bool autoGenerateMips = True, bool isShadowMap = False, int anisoLevel = 1, float mipMapBias = 0, bool enableMSAA = False, bool bindTextureMS = False, bool useDynamicScale = False, Render纹理Memoryless memoryless = 0, string name = ""））
- `RTHandle Alloc(ScaleFunc scaleFunc, int slices = 1, DepthBits depthBufferBits = 0, GraphicsFormat colorFormat = 4, FilterMode filterMode = 0, TextureWrapMode wrapMode = 0, TextureDimension dimension = 2, bool enableRandomWrite = False, bool useMipMap = False, bool autoGenerateMips = True, bool isShadowMap = False, int anisoLevel = 1, float mipMapBias = 0, bool enableMSAA = False, bool bindTextureMS = False, bool useDynamicScale = False, RenderTextureMemoryless memoryless = 0, string name = "")`
  （RT句柄 Alloc（缩放Func scaleFunc, int slices = 1, 深度Bits depthBufferBits = 0, Graphics格式化 colorFormat = 4, Filter模式 filterMode = 0, 纹理Wrap模式 wrapMode = 0, 纹理Dimension dimension = 2, bool enableRandomWrite = False, bool useMipMap = False, bool autoGenerateMips = True, bool isShadowMap = False, int anisoLevel = 1, float mipMapBias = 0, bool enableMSAA = False, bool bindTextureMS = False, bool useDynamicScale = False, Render纹理Memoryless memoryless = 0, string name = ""））
- `RTHandle Alloc(Texture tex)`
  （RT句柄 Alloc（纹理 tex））
- `RTHandle Alloc(RenderTexture tex)`
  （RT句柄 Alloc（Render纹理 tex））
- `RTHandle Alloc(RenderTargetIdentifier tex)`
  （RT句柄 Alloc（Render目标Identifier tex））
- `RTHandle Alloc(RenderTargetIdentifier tex, string name)`
  （RT句柄 Alloc（Render目标Identifier tex, string name））
- `RTHandle Alloc(RTHandle tex)`
  （RT句柄 Alloc（RT句柄 tex））
- `void Initialize(int width, int height, bool scaledRTsupportsMSAA, MSAASamples scaledRTMSAASamples)`
  （void 初始化（int width, int height, bool scaledRTsupportsMSAA, MSAASamples scaledRTMSAASamples））
- `void Release(RTHandle rth)`
  （void Release（RT句柄 rth））
- `void SetHardwareDynamicResolutionState(bool hwDynamicResRequested)`
  （void 集合Hardware动态的Resolution状态（bool hwDynamicResRequested））
- `void SetReferenceSize(int width, int height, MSAASamples msaaSamples)`
  （void 集合引用大小（int width, int height, MSAASamples msaaSamples））
- `void ResetReferenceSize(int width, int height)`
  （void 重置引用大小（int width, int height））

---

## RVOController（RVO控制器）

**继承**: VersionedMonoBehaviour（VersionedMonoBehaviour）

### 字段 (16)

- `float radiusBackingField`（float radiusBackingField）(偏移: 0x10)
- `float heightBackingField`（float heightBackingField）(偏移: 0x14)
- `float centerBackingField`（float centerBackingField）(偏移: 0x18)
- `bool locked`（bool locked）(偏移: 0x1C)
- `bool lockWhenNotMoving`（bool lockWhenNotMoving）(偏移: 0x1D)
- `float agentTimeHorizon`（float agent时间Horizon）(偏移: 0x20)
- `float obstacleTimeHorizon`（float obstacle时间Horizon）(偏移: 0x24)
- `int maxNeighbours`（int maxNeighbours）(偏移: 0x28)
- `RVOLayer layer`（RVO层 layer）(偏移: 0x2C)
- `RVOLayer collidesWith`（RVO层 collidesWith）(偏移: 0x30)
- `float wallAvoidForce`（float wallAvoid强制）(偏移: 0x34)
- `float wallAvoidFalloff`（float wallAvoidFalloff）(偏移: 0x38)
- `float priority`（float priority）(偏移: 0x3C)
- `Transform tr`（变换 tr）(偏移: 0x48)
- `IAstarAI aiBackingField`（IAstarAI aiBackingField）(偏移: 0x4C)
- `bool debug`（bool debug）(偏移: 0x50)

### 方法 (39)

- `float get_radius()`
  （float get_radius（））
- `void set_radius(float value)`
  （void set_radius（float value））
- `float get_height()`
  （float get_height（））
- `void set_height(float value)`
  （void set_height（float value））
- `float get_center()`
  （float get_center（））
- `void set_center(float value)`
  （void set_center（float value））
- `LayerMask get_mask()`
  （层掩码 get_mask（））
- `void set_mask(LayerMask value)`
  （void set_mask（层掩码 value））
- `bool get_enableRotation()`
  （bool get_enableRotation（））
- `void set_enableRotation(bool value)`
  （void set_enableRotation（bool value））
- `float get_rotationSpeed()`
  （float get_rotationSpeed（））
- `void set_rotationSpeed(float value)`
  （void set_rotationSpeed（float value））
- `float get_maxSpeed()`
  （float get_maxSpeed（））
- `void set_maxSpeed(float value)`
  （void set_maxSpeed（float value））
- `MovementPlane get_movementPlane()`
  （MovementPlane get_movementPlane（））
- `IAgent get_rvoAgent()`
  （IAgent get_rvoAgent（））
- `void set_rvoAgent(IAgent value)`
  （void set_rvoAgent（IAgent value））
- `Simulator get_simulator()`
  （Simulator get_simulator（））
- `void set_simulator(Simulator value)`
  （void set_simulator（Simulator value））
- `IAstarAI get_ai()`
  （IAstarAI get_ai（））
- `void set_ai(IAstarAI value)`
  （void set_ai（IAstarAI value））
- `Vector3 get_position()`
  （三维向量 get_position（））
- `Vector3 get_velocity()`
  （三维向量 get_velocity（））
- `void set_velocity(Vector3 value)`
  （void set_velocity（三维向量 value））
- `Vector3 CalculateMovementDelta(float deltaTime)`
  （三维向量 计算MovementDelta（float deltaTime））
- `Vector3 CalculateMovementDelta(Vector3 position, float deltaTime)`
  （三维向量 计算MovementDelta（三维向量 position, float deltaTime））
- `void SetCollisionNormal(Vector3 normal)`
  （void 集合Collision法线（三维向量 normal））
- `void ForceSetVelocity(Vector3 velocity)`
  （void 强制集合速度（三维向量 velocity））
- `Vector2 To2D(Vector3 p)`
  （二维向量 To2D（三维向量 p））
- `Vector2 To2D(Vector3 p, out float elevation)`
  （二维向量 To2D（三维向量 p, out float elevation））
- `Vector3 To3D(Vector2 p, float elevationCoordinate)`
  （三维向量 To3D（二维向量 p, float elevationCoordinate））
- `void OnDisable()`
  （void On禁用（））
- `void OnEnable()`
  （void On启用（））
- `void UpdateAgentProperties()`
  （void 更新AgentProperties（））
- `void SetTarget(Vector3 pos, float speed, float maxSpeed)`
  （void 集合目标（三维向量 pos, float speed, float maxSpeed））
- `void Move(Vector3 vel)`
  （void 移动（三维向量 vel））
- `void Teleport(Vector3 pos)`
  （void Teleport（三维向量 pos））
- `void OnDrawGizmos()`
  （void OnDrawGizmos（））
- `int OnUpgradeSerializedData(int version, bool unityThread)`
  （int OnUpgradeSerialized数据（int version, bool unityThread））

---

## RVOLayer（RVO层）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## RVONavmesh（RVONavmesh）

**继承**: GraphModifier（Graph修改器）

### 字段 (3)

- `float wallHeight`（float wall高度）(偏移: 0x20)
- `List<ObstacleVertex> obstacles`（List<ObstacleVertex> obstacles）(偏移: 0x24)
- `Simulator lastSim`（Simulator lastSim）(偏移: 0x28)

### 方法 (7)

- `void OnPostCacheLoad()`
  （void OnPost缓存加载（））
- `void OnGraphsPostUpdate()`
  （void OnGraphsPost更新（））
- `void OnLatePostScan()`
  （void On延迟PostScan（））
- `void OnDisable()`
  （void On禁用（））
- `void RemoveObstacles()`
  （void 移除Obstacles（））
- `void AddGraphObstacles(Simulator sim, GridGraph grid)`
  （void 添加GraphObstacles（Simulator sim, 网格Graph grid））
- `void AddGraphObstacles(Simulator simulator, INavmesh navmesh)`
  （void 添加GraphObstacles（Simulator simulator, INavmesh navmesh））

---

## RVOObstacle（RVOObstacle）

**继承**: VersionedMonoBehaviour（VersionedMonoBehaviour）

### 字段 (9)

- `RVOObstacle.ObstacleVertexWinding obstacleMode`（RVOObstacle.ObstacleVertexWinding obstacle模式）(偏移: 0x10)
- `RVOLayer layer`（RVO层 layer）(偏移: 0x14)
- `Simulator sim`（Simulator sim）(偏移: 0x18)
- `List<ObstacleVertex> addedObstacles`（List<ObstacleVertex> addedObstacles）(偏移: 0x1C)
- `List<Vector3[]> sourceObstacles`（List<Vector3[]> sourceObstacles）(偏移: 0x20)
- `bool gizmoDrawing`（bool gizmoDrawing）(偏移: 0x24)
- `List<Vector3[]> gizmoVerts`（List<Vector3[]> gizmoVerts）(偏移: 0x28)
- `RVOObstacle.ObstacleVertexWinding _obstacleMode`（RVOObstacle.ObstacleVertexWinding _obstacle模式）(偏移: 0x2C)
- `Matrix4x4 prevUpdateMatrix`（Matrix4x4 prev更新矩阵）(偏移: 0x30)

### 方法 (12)

- `void OnDrawGizmos()`
  （void OnDrawGizmos（））
- `void OnDrawGizmosSelected()`
  （void OnDrawGizmos选中的（））
- `void OnDrawGizmos(bool selected)`
  （void OnDrawGizmos（bool selected））
- `Matrix4x4 GetMatrix()`
  （Matrix4x4 获取矩阵（））
- `void OnDisable()`
  （void On禁用（））
- `void OnEnable()`
  （void On启用（））
- `void Start()`
  （void 开始（））
- `void Update()`
  （void 更新（））
- `void FindSimulator()`
  （void 查找Simulator（））
- `void AddObstacle(Vector3[] vertices, float height)`
  （void 添加Obstacle（Vector3[] vertices, float height））
- `void AddObstacleInternal(Vector3[] vertices, float height)`
  （void 添加Obstacle内部的（Vector3[] vertices, float height））
- `void WindCorrectly(Vector3[] vertices)`
  （void WindCorrectly（Vector3[] vertices））

---

## RVOObstacle.ObstacleVertexWinding（RVOObstacle.ObstacleVertexWinding）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## RVOQuadtree（RVOQuadtree）

### 字段 (4)

- `float maxRadius`（float maxRadius）(偏移: 0x8)
- `RVOQuadtree.Node[] nodes`（RVOQuadtree.Node[] nodes）(偏移: 0xC)
- `int filledNodes`（int filledNodes）(偏移: 0x10)
- `Rect bounds`（Rect bounds）(偏移: 0x14)

### 方法 (8)

- `void Clear()`
  （void 清除（））
- `void SetBounds(Rect r)`
  （void 集合Bounds（Rect r））
- `int GetNodeIndex()`
  （int 获取节点索引（））
- `void Insert(Agent agent)`
  （void Insert（Agent agent））
- `void CalculateSpeeds()`
  （void 计算Speeds（））
- `void Query(Vector2 p, float speed, float timeHorizon, float agentRadius, Agent agent)`
  （void Query（二维向量 p, float speed, float timeHorizon, float agentRadius, Agent agent））
- `void DebugDraw()`
  （void DebugDraw（））
- `void DebugDrawRec(int i, Rect r)`
  （void DebugDrawRec（int i, Rect r））

---

## RVOQuadtree.Node（RVOQuadtree.节点）

### 字段 (4)

- `int child00`（int child00）(偏移: 0x0)
- `Agent linkedList`（Agent linked列表）(偏移: 0x4)
- `byte count`（byte count）(偏移: 0x8)
- `float maxSpeed`（float maxSpeed）(偏移: 0xC)

### 方法 (3)

- `void Add(Agent agent)`
  （void 添加（Agent agent））
- `void Distribute(RVOQuadtree.Node[] nodes, Rect r)`
  （void Distribute（RVOQuadtree.Node[] nodes, Rect r））
- `float CalculateMaxSpeed(RVOQuadtree.Node[] nodes, int index)`
  （float 计算最大Speed（RVOQuadtree.Node[] nodes, int index））

---

## RVOQuadtree.QuadtreeQuery（RVOQuadtree.QuadtreeQuery）

### 字段 (7)

- `Vector2 p`（二维向量 p）(偏移: 0x0)
- `float speed`（float speed）(偏移: 0x8)
- `float timeHorizon`（float timeHorizon）(偏移: 0xC)
- `float agentRadius`（float agentRadius）(偏移: 0x10)
- `float maxRadius`（float maxRadius）(偏移: 0x14)
- `Agent agent`（Agent agent）(偏移: 0x18)
- `RVOQuadtree.Node[] nodes`（RVOQuadtree.Node[] nodes）(偏移: 0x1C)

### 方法 (1)

- `void QueryRec(int i, Rect r)`
  （void QueryRec（int i, Rect r））

---

## RVOSimulator（RVOSimulator）

**继承**: VersionedMonoBehaviour（VersionedMonoBehaviour）

### 字段 (7)

- `int desiredSimulationFPS`（int desiredSimulationFPS）(偏移: 0x10)
- `ThreadCount workerThreads`（Thread数量 workerThreads）(偏移: 0x14)
- `bool doubleBuffering`（bool doubleBuffering）(偏移: 0x18)
- `float symmetryBreakingBias`（float symmetryBreakingBias）(偏移: 0x1C)
- `MovementPlane movementPlane`（MovementPlane movementPlane）(偏移: 0x20)
- `bool drawObstacles`（bool drawObstacles）(偏移: 0x24)
- `Simulator simulator`（Simulator simulator）(偏移: 0x28)

### 方法 (7)

- `RVOSimulator get_active()`
  （RVOSimulator get_active（））
- `void set_active(RVOSimulator value)`
  （void set_active（RVOSimulator value））
- `Simulator GetSimulator()`
  （Simulator 获取Simulator（））
- `void OnEnable()`
  （void On启用（））
- `void Awake()`
  （void Awake（））
- `void Update()`
  （void 更新（））
- `void OnDestroy()`
  （void On销毁（））

---

## RVOSquareObstacle（RVOSquareObstacle）

**继承**: RVOObstacle（RVOObstacle）

### 字段 (3)

- `float height`（float height）(偏移: 0x70)
- `Vector2 size`（二维向量 size）(偏移: 0x74)
- `Vector2 center`（二维向量 center）(偏移: 0x7C)

### 方法 (6)

- `bool get_StaticObstacle()`
  （bool get_静态的Obstacle（））
- `bool get_ExecuteInEditor()`
  （bool get_执行InEditor（））
- `bool get_LocalCoordinates()`
  （bool get_本地的Coordinates（））
- `float get_Height()`
  （float get_高度（））
- `bool AreGizmosDirty()`
  （bool AreGizmosDirty（））
- `void CreateObstacles()`
  （void 创建Obstacles（））

---

## Radio（Radio）

**继承**: Parent（父级）

### 字段 (1)

- `int selection`（int selection）(偏移: 0x18)

---

## RadioChild（Radio子级）

**继承**: ChoiceBase（Choice基础）

### 方法 (2)

- `bool OnSelect()`
  （bool On选择（））
- `bool GetFocus()`
  （bool 获取聚焦（））

---

## RadiusModifier（Radius修改器）

**继承**: MonoModifier（Mono修改器）

### 字段 (6)

- `float radius`（float radius）(偏移: 0x14)
- `float detail`（float detail）(偏移: 0x18)
- `float[] radi`（float[] radi）(偏移: 0x1C)
- `float[] a1`（float[] a1）(偏移: 0x20)
- `float[] a2`（float[] a2）(偏移: 0x24)
- `bool[] dir`（bool[] dir）(偏移: 0x28)

### 方法 (7)

- `int get_Order()`
  （int get_Order（））
- `bool CalculateCircleInner(Vector3 p1, Vector3 p2, float r1, float r2, out float a, out float sigma)`
  （bool 计算CircleInner（三维向量 p1, 三维向量 p2, float r1, float r2, out float a, out float sigma））
- `bool CalculateCircleOuter(Vector3 p1, Vector3 p2, float r1, float r2, out float a, out float sigma)`
  （bool 计算CircleOuter（三维向量 p1, 三维向量 p2, float r1, float r2, out float a, out float sigma））
- `RadiusModifier.TangentType CalculateTangentType(Vector3 p1, Vector3 p2, Vector3 p3, Vector3 p4)`
  （RadiusModifier.Tangent类型 计算Tangent类型（三维向量 p1, 三维向量 p2, 三维向量 p3, 三维向量 p4））
- `RadiusModifier.TangentType CalculateTangentTypeSimple(Vector3 p1, Vector3 p2, Vector3 p3)`
  （RadiusModifier.Tangent类型 计算Tangent类型Simple（三维向量 p1, 三维向量 p2, 三维向量 p3））
- `void Apply(Path p)`
  （void 应用（路径 p））
- `List<Vector3> Apply(List<Vector3> vs)`
  （List<Vector3> 应用（List<Vector3> vs））

---

## RadiusModifier.TangentType（RadiusModifier.Tangent类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## RagdollUtility（Ragdoll工具）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (16)

- `IK ik`（IK ik）(偏移: 0xC)
- `float ragdollToAnimationTime`（float ragdollTo动画时间）(偏移: 0x10)
- `bool applyIkOnRagdoll`（bool applyIkOnRagdoll）(偏移: 0x14)
- `float applyVelocity`（float apply速度）(偏移: 0x18)
- `float applyAngularVelocity`（float applyAngular速度）(偏移: 0x1C)
- `Animator animator`（动画器 animator）(偏移: 0x20)
- `RagdollUtility.Rigidbone[] rigidbones`（RagdollUtility.Rigidbone[] rigidbones）(偏移: 0x24)
- `RagdollUtility.Child[] children`（RagdollUtility.Child[] children）(偏移: 0x28)
- `bool enableRagdollFlag`（bool enableRagdoll标志）(偏移: 0x2C)
- `AnimatorUpdateMode animatorUpdateMode`（动画器更新模式 animator更新模式）(偏移: 0x30)
- `IK[] allIKComponents`（IK[] allIKComponents）(偏移: 0x34)
- `bool[] fixTransforms`（bool[] fixTransforms）(偏移: 0x38)
- `float ragdollWeight`（float ragdollWeight）(偏移: 0x3C)
- `float ragdollWeightV`（float ragdollWeightV）(偏移: 0x40)
- `bool fixedFrame`（bool fixedFrame）(偏移: 0x44)
- `bool[] disabledIKComponents`（bool[] disabledIKComponents）(偏移: 0x48)

### 方法 (17)

- `void EnableRagdoll()`
  （void 启用Ragdoll（））
- `void DisableRagdoll()`
  （void 禁用Ragdoll（））
- `void Start()`
  （void 开始（））
- `IEnumerator DisableRagdollSmooth()`
  （IEnumerator 禁用RagdollSmooth（））
- `void Update()`
  （void 更新（））
- `void FixedUpdate()`
  （void 固定更新（））
- `void LateUpdate()`
  （void 延迟更新（））
- `void AfterLastIK()`
  （void After最后一个IK（））
- `void AfterAnimation()`
  （void After动画（））
- `void OnFinalPose()`
  （void OnFinalPose（））
- `void RagdollEnabler()`
  （void RagdollEnabler（））
- `bool get_isRagdoll()`
  （bool get_isRagdoll（））
- `void RecordVelocities()`
  （void RecordVelocities（））
- `bool get_ikUsed()`
  （bool get_ikUsed（））
- `void StoreLocalState()`
  （void 商店本地的状态（））
- `void FixTransforms(float weight)`
  （void FixTransforms（float weight））
- `void OnDestroy()`
  （void On销毁（））

---

## RagdollUtility.Child（RagdollUtility.子级）

### 字段 (3)

- `Transform t`（变换 t）(偏移: 0x8)
- `Vector3 localPosition`（三维向量 localPosition）(偏移: 0xC)
- `Quaternion localRotation`（Quaternion localRotation）(偏移: 0x18)

### 方法 (2)

- `void FixTransform(float weight)`
  （void Fix变换（float weight））
- `void StoreLocalState()`
  （void 商店本地的状态（））

---

## RagdollUtility.Rigidbone（RagdollUtility.Rigidbone）

### 字段 (11)

- `Rigidbody r`（刚体 r）(偏移: 0x8)
- `Transform t`（变换 t）(偏移: 0xC)
- `Collider collider`（碰撞器 collider）(偏移: 0x10)
- `Joint joint`（Joint joint）(偏移: 0x14)
- `Rigidbody c`（刚体 c）(偏移: 0x18)
- `bool updateAnchor`（bool updateAnchor）(偏移: 0x1C)
- `Vector3 deltaPosition`（三维向量 deltaPosition）(偏移: 0x20)
- `Quaternion deltaRotation`（Quaternion deltaRotation）(偏移: 0x2C)
- `float deltaTime`（float delta时间）(偏移: 0x3C)
- `Vector3 lastPosition`（三维向量 lastPosition）(偏移: 0x40)
- `Quaternion lastRotation`（Quaternion lastRotation）(偏移: 0x4C)

### 方法 (2)

- `void RecordVelocity()`
  （void Record速度（））
- `void WakeUp(float velocityWeight, float angularVelocityWeight)`
  （void Wake上（float velocityWeight, float angularVelocityWeight））

---

## Random（随机）

### 字段 (3)

- `int inext`（int inext）(偏移: 0x8)
- `int inextp`（int inextp）(偏移: 0xC)
- `int[] SeedArray`（int[] Seed数组）(偏移: 0x10)

### 方法 (8)

- `double Sample()`
  （double Sample（））
- `int InternalSample()`
  （int 内部的Sample（））
- `int Next()`
  （int 下一个（））
- `double GetSampleForLargeRange()`
  （double 获取SampleForLarge范围（））
- `int Next(int minValue, int maxValue)`
  （int 下一个（int minValue, int maxValue））
- `int Next(int maxValue)`
  （int 下一个（int maxValue））
- `double NextDouble()`
  （double 下一个Double（））
- `void NextBytes(byte[] buffer)`
  （void 下一个Bytes（byte[] buffer））

---

## Random（随机）

### 方法 (10)

- `float Range(float minInclusive, float maxInclusive)`
  （float 范围（float minInclusive, float maxInclusive））
- `int Range(int minInclusive, int maxExclusive)`
  （int 范围（int minInclusive, int maxExclusive））
- `int RandomRangeInt(int minInclusive, int maxExclusive)`
  （int 随机范围整数（int minInclusive, int maxExclusive））
- `float get_value()`
  （float get_value（））
- `Vector3 get_insideUnitSphere()`
  （三维向量 get_insideUnitSphere（））
- `void GetRandomUnitCircle(out Vector2 output)`
  （void 获取随机UnitCircle（out Vector2 output））
- `Vector2 get_insideUnitCircle()`
  （二维向量 get_insideUnitCircle（））
- `Vector3 get_onUnitSphere()`
  （三维向量 get_onUnitSphere（））
- `void get_insideUnitSphere_Injected(out Vector3 ret)`
  （void get_insideUnitSphere_Injected（out Vector3 ret））
- `void get_onUnitSphere_Injected(out Vector3 ret)`
  （void get_onUnitSphere_Injected（out Vector3 ret））

---

## RandomItem（随机项目）

### 字段 (2)

- `RandomItem.Item[] items`（随机Item.Item[] items）(偏移: 0x8)
- `List<int> idList`（List<int> id列表）(偏移: 0xC)

### 方法 (2)

- `void Init()`
  （void 初始化（））
- `string Get()`
  （string 获取（））

---

## RandomItem.Item（随机Item.项目）

### 字段 (2)

- `string name`（string name）(偏移: 0x0)
- `int count`（int count）(偏移: 0x4)

---

## RandomNumberGenerator（随机NumberGenerator）

**继承**: IDisposable（IDisposable）

### 方法 (3)

- `RandomNumberGenerator Create()`
  （随机NumberGenerator 创建（））
- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））

---

## RandomPath（随机路径）

**继承**: ABPath（AB路径）

### 字段 (9)

- `int searchLength`（int searchLength）(偏移: 0xCC)
- `int spread`（int spread）(偏移: 0xD0)
- `float aimStrength`（float aimStrength）(偏移: 0xD4)
- `PathNode chosenNodeR`（路径节点 chosen节点R）(偏移: 0xD8)
- `PathNode maxGScoreNodeR`（路径节点 maxG分数节点R）(偏移: 0xDC)
- `int maxGScore`（int maxG分数）(偏移: 0xE0)
- `Vector3 aim`（三维向量 aim）(偏移: 0xE4)
- `int nodesEvaluatedRep`（int nodesEvaluatedRep）(偏移: 0xF0)
- `Random rnd`（随机 rnd）(偏移: 0xF4)

### 方法 (9)

- `bool get_FloodingPath()`
  （bool get_Flooding路径（））
- `bool get_hasEndPoint()`
  （bool get_has结束Point（））
- `void Reset()`
  （void 重置（））
- `RandomPath Construct(Vector3 start, int length, OnPathDelegate callback)`
  （随机路径 Construct（三维向量 start, int length, On路径委托 callback））
- `RandomPath Setup(Vector3 start, int length, OnPathDelegate callback)`
  （随机路径 Setup（三维向量 start, int length, On路径委托 callback））
- `void ReturnPath()`
  （void Return路径（））
- `void Prepare()`
  （void Prepare（））
- `void Initialize()`
  （void 初始化（））
- `void CalculateStep(long targetTick)`
  （void 计算Step（long targetTick））

---

