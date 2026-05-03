# 游戏类定义 (Part 7/21)

共 200 个类 (总序号 1201 - 1400)

---

## EventSourceSettings（事件SourceSettings）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## EventSystem（事件系统）

**继承**: UIBehaviour（UI行为）

### 字段 (11)

- `List<BaseInputModule> m_SystemInputModules`（List<基础输入Module> m_系统输入Modules）(偏移: 0xC)
- `BaseInputModule m_CurrentInputModule`（基础输入模块 m_当前输入模块）(偏移: 0x10)
- `List<EventSystem> m_EventSystems`（List<事件System> m_事件Systems）(偏移: 0x0)
- `GameObject m_FirstSelected`（游戏对象 m_第一个选中的）(偏移: 0x14)
- `bool m_sendNavigationEvents`（bool m_sendNavigationEvents）(偏移: 0x18)
- `int m_DragThreshold`（int m_DragThreshold）(偏移: 0x1C)
- `GameObject m_CurrentSelected`（游戏对象 m_当前选中的）(偏移: 0x20)
- `bool m_HasFocus`（bool m_是否有聚焦）(偏移: 0x24)
- `bool m_SelectionGuard`（bool m_SelectionGuard）(偏移: 0x25)
- `BaseEventData m_DummyData`（基础事件数据 m_Dummy数据）(偏移: 0x28)
- `Comparison<RaycastResult> s_RaycastComparer`（Comparison<RaycastResult> s_RaycastComparer）(偏移: 0x4)

### 方法 (28)

- `EventSystem get_current()`
  （事件系统 get_current（））
- `void set_current(EventSystem value)`
  （void set_current（事件系统 value））
- `bool get_sendNavigationEvents()`
  （bool get_sendNavigationEvents（））
- `void set_sendNavigationEvents(bool value)`
  （void set_sendNavigationEvents（bool value））
- `int get_pixelDragThreshold()`
  （int get_pixelDragThreshold（））
- `void set_pixelDragThreshold(int value)`
  （void set_pixelDragThreshold（int value））
- `BaseInputModule get_currentInputModule()`
  （基础输入模块 get_current输入模块（））
- `GameObject get_firstSelectedGameObject()`
  （游戏对象 get_first选中的游戏对象（））
- `void set_firstSelectedGameObject(GameObject value)`
  （void set_first选中的游戏对象（游戏对象 value））
- `GameObject get_currentSelectedGameObject()`
  （游戏对象 get_current选中的游戏对象（））
- `GameObject get_lastSelectedGameObject()`
  （游戏对象 get_last选中的游戏对象（））
- `bool get_isFocused()`
  （bool get_is聚焦的（））
- `void UpdateModules()`
  （void 更新Modules（））
- `bool get_alreadySelecting()`
  （bool get_alreadySelecting（））
- `void SetSelectedGameObject(GameObject selected, BaseEventData pointer)`
  （void 集合选中的游戏对象（游戏对象 selected, 基础事件数据 pointer））
- `BaseEventData get_baseEventDataCache()`
  （基础事件数据 get_base事件数据缓存（））
- `void SetSelectedGameObject(GameObject selected)`
  （void 集合选中的游戏对象（游戏对象 selected））
- `int RaycastComparer(RaycastResult lhs, RaycastResult rhs)`
  （int RaycastComparer（RaycastResult lhs, RaycastResult rhs））
- `void RaycastAll(PointerEventData eventData, List<RaycastResult> raycastResults)`
  （void Raycast所有（指针事件数据 eventData, List<RaycastResult> raycastResults））
- `bool IsPointerOverGameObject()`
  （bool 是否指针Over游戏对象（））
- `bool IsPointerOverGameObject(int pointerId)`
  （bool 是否指针Over游戏对象（int pointerId））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `void TickModules()`
  （void TickModules（））
- `void OnApplicationFocus(bool hasFocus)`
  （void OnApplication聚焦（bool hasFocus））
- `void Update()`
  （void 更新（））
- `void ChangeEventModule(BaseInputModule module)`
  （void Change事件模块（基础输入模块 module））
- `string ToString()`
  （字符串 转字符串（））

---

## EventTags（事件Tags）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## EventTask（事件Task）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## EventTrigger（事件触发器）

**继承**: MonoBehaviour, IPointerEnterHandler, IEventSystemHandler, IPointerExitHandler, IPointerDownHandler, IPointerUpHandler, IPointerClickHandler, IInitializePotentialDragHandler, IBeginDragHandler, IDragHandler, IEndDragHandler, IDropHandler, IScrollHandler, IUpdateSelectedHandler, ISelectHandler, IDeselectHandler, IMoveHandler, ISubmitHandler, ICancelHandler（MonoBehaviour行为, I指针Enter处理器, I事件系统处理器, I指针Exit处理器, I指针下处理器, I指针上处理器, I指针Click处理器, I初始化PotentialDrag处理器, IBeginDrag处理器, IDrag处理器, I结束Drag处理器, IDrop处理器, I滚动处理器, I更新选中的处理器, I选择处理器, I取消选择处理器, I移动处理器, ISubmit处理器, I取消处理器）

### 字段 (1)

- `List<EventTrigger.Entry> m_Delegates`（List<事件Trigger.Entry> m_Delegates）(偏移: 0xC)

### 方法 (22)

- `List<EventTrigger.Entry> get_delegates()`
  （List<事件Trigger.Entry> get_delegates（））
- `void set_delegates(List<EventTrigger.Entry> value)`
  （void set_delegates（List<事件Trigger.Entry> value））
- `List<EventTrigger.Entry> get_triggers()`
  （List<事件Trigger.Entry> get_triggers（））
- `void set_triggers(List<EventTrigger.Entry> value)`
  （void set_triggers（List<事件Trigger.Entry> value））
- `void Execute(EventTriggerType id, BaseEventData eventData)`
  （void 执行（事件触发器类型 id, 基础事件数据 eventData））
- `void OnPointerEnter(PointerEventData eventData)`
  （void On指针Enter（指针事件数据 eventData））
- `void OnPointerExit(PointerEventData eventData)`
  （void On指针Exit（指针事件数据 eventData））
- `void OnDrag(PointerEventData eventData)`
  （void 拖拽时（指针事件数据 eventData））
- `void OnDrop(PointerEventData eventData)`
  （void OnDrop（指针事件数据 eventData））
- `void OnPointerDown(PointerEventData eventData)`
  （void 指针按下时（指针事件数据 eventData））
- `void OnPointerUp(PointerEventData eventData)`
  （void On指针上（指针事件数据 eventData））
- `void OnPointerClick(PointerEventData eventData)`
  （void 指针点击时（指针事件数据 eventData））
- `void OnSelect(BaseEventData eventData)`
  （void On选择（基础事件数据 eventData））
- `void OnDeselect(BaseEventData eventData)`
  （void On取消选择（基础事件数据 eventData））
- `void OnScroll(PointerEventData eventData)`
  （void On滚动（指针事件数据 eventData））
- `void OnMove(AxisEventData eventData)`
  （void On移动（轴事件数据 eventData））
- `void OnUpdateSelected(BaseEventData eventData)`
  （void On更新选中的（基础事件数据 eventData））
- `void OnInitializePotentialDrag(PointerEventData eventData)`
  （void On初始化PotentialDrag（指针事件数据 eventData））
- `void OnBeginDrag(PointerEventData eventData)`
  （void OnBeginDrag（指针事件数据 eventData））
- `void OnEndDrag(PointerEventData eventData)`
  （void On结束Drag（指针事件数据 eventData））
- `void OnSubmit(BaseEventData eventData)`
  （void 提交时（基础事件数据 eventData））
- `void OnCancel(BaseEventData eventData)`
  （void On取消（基础事件数据 eventData））

---

## EventTrigger.Entry（事件Trigger.Entry）

### 字段 (2)

- `EventTriggerType eventID`（事件触发器类型 eventID）(偏移: 0x8)
- `EventTrigger.TriggerEvent callback`（事件Trigger.触发器事件 callback）(偏移: 0xC)

---

## EventTriggerType（事件触发器类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## EventType（事件类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## EventWaitHandle（事件Wait句柄）

**继承**: WaitHandle（Wait句柄）

### 方法 (2)

- `bool Reset()`
  （bool 重置（））
- `bool Set()`
  （bool 集合（））

---

## EventWrittenEventArgs（事件Written事件Args）

**继承**: EventArgs（事件参数）

### 字段 (4)

- `string m_message`（string m_message）(偏移: 0x20)
- `string m_eventName`（string m_event名称）(偏移: 0x24)
- `EventSource m_eventSource`（事件Source m_eventSource）(偏移: 0x28)
- `ReadOnlyCollection<string> m_payloadNames`（ReadOnlyCollection<string> m_payloadNames）(偏移: 0x2C)

### 方法 (6)

- `void set_EventName(string value)`
  （void set_事件名称（string value））
- `void set_EventId(int value)`
  （void set_事件Id（int value））
- `void set_RelatedActivityId(Guid value)`
  （void set_RelatedActivityId（Guid value））
- `void set_Payload(ReadOnlyCollection<object> value)`
  （void set_Payload（ReadOnlyCollection<object> value））
- `void set_PayloadNames(ReadOnlyCollection<string> value)`
  （void set_PayloadNames（ReadOnlyCollection<string> value））
- `void set_Message(string value)`
  （void set_Message（string value））

---

## Evidence（Evidence）

**继承**: ICollection, IEnumerable（ICollection, IEnumerable）

### 字段 (3)

- `bool _locked`（bool _locked）(偏移: 0x8)
- `ArrayList hostEvidenceList`（数组列表 hostEvidence列表）(偏移: 0xC)
- `ArrayList assemblyEvidenceList`（数组列表 assemblyEvidence列表）(偏移: 0x10)

### 方法 (4)

- `int get_Count()`
  （整数 获取_数量（））
- `object get_SyncRoot()`
  （对象 获取_同步根（））
- `void CopyTo(Array array, int index)`
  （void 复制到（数组 array, 整数 index））
- `IEnumerator GetEnumerator()`
  （IEnumerator 获取枚举器（））

---

## Evidence.EvidenceEnumerator（Evidence.EvidenceEnumerator）

**继承**: IEnumerator（IEnumerator枚举器）

### 字段 (3)

- `IEnumerator currentEnum`（IEnumerator currentEnum）(偏移: 0x8)
- `IEnumerator hostEnum`（IEnumerator hostEnum）(偏移: 0xC)
- `IEnumerator assemblyEnum`（IEnumerator assemblyEnum）(偏移: 0x10)

### 方法 (3)

- `bool MoveNext()`
  （布尔值 移动下一个（））
- `void Reset()`
  （void 重置（））
- `object get_Current()`
  （对象 获取_当前（））

---

## Example（Example）

### 字段 (3)

- `string id`（string id）(偏移: 0x8)
- `QueryTriggerInteraction enumVal`（Query触发器Interaction enumVal）(偏移: 0xC)
- `NestedDict nestedData`（NestedDict nested数据）(偏移: 0x10)

---

## ExamplesGUI（ExamplesGUI）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (8)

- `ObscuredTypesExamples obscuredTypesExamples`（模糊的TypesExamples obscuredTypesExamples）(偏移: 0xC)
- `ObscuredPrefsExamples obscuredPrefsExamples`（模糊的PrefsExamples obscuredPrefsExamples）(偏移: 0x10)
- `DetectorsExamples detectorsExamples`（DetectorsExamples detectorsExamples）(偏移: 0x14)
- `string[] tabs`（string[] tabs）(偏移: 0x18)
- `ExamplesGUI.ExamplePage currentPage`（ExamplesGUI.ExamplePage currentPage）(偏移: 0x1C)
- `string allSimpleObscuredTypes`（string allSimple模糊的Types）(偏移: 0x20)
- `ObscuredPrefs.DeviceLockLevel savesLock`（模糊的Prefs.DeviceLock等级 savesLock）(偏移: 0x24)
- `GUIStyle centeredStyle`（GUIStyle centeredStyle）(偏移: 0x28)

### 方法 (6)

- `void OnGUI()`
  （void GUI时（））
- `void DrawObscuredTypesPage()`
  （void Draw模糊的TypesPage（））
- `void DrawObscuredPrefsPage()`
  （void Draw模糊的PrefsPage（））
- `void DrawDetectorsPage()`
  （void DrawDetectorsPage（））
- `string GetAllSimpleObscuredTypes()`
  （string 获取所有Simple模糊的Types（））
- `string GetAllObscuredPrefsDataTypes()`
  （string 获取所有模糊的Prefs数据Types（））

---

## ExamplesGUI.ExamplePage（ExamplesGUI.ExamplePage）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Exception（异常）

**继承**: ISerializable, _Exception（ISerializable, _Exception）

### 字段 (16)

- `object s_EDILock`（object s_EDILock）(偏移: 0x0)
- `string _className`（string _class名称）(偏移: 0x8)
- `string _message`（string _message）(偏移: 0xC)
- `IDictionary _data`（I字典 _data）(偏移: 0x10)
- `Exception _innerException`（Exception _innerException）(偏移: 0x14)
- `string _helpURL`（string _helpURL）(偏移: 0x18)
- `object _stackTrace`（object _stackTrace）(偏移: 0x1C)
- `string _stackTraceString`（string _stackTrace字符串）(偏移: 0x20)
- `string _remoteStackTraceString`（string _remote栈Trace字符串）(偏移: 0x24)
- `int _remoteStackIndex`（int _remote栈索引）(偏移: 0x28)
- `object _dynamicMethods`（object _dynamicMethods）(偏移: 0x2C)
- `int _HResult`（int _HResult）(偏移: 0x30)
- `string _source`（string _source）(偏移: 0x34)
- `SafeSerializationManager _safeSerializationManager`（SafeSerialization管理器 _safeSerialization管理器）(偏移: 0x38)
- `StackTrace[] captured_traces`（栈Trace[] captured_traces）(偏移: 0x3C)
- `IntPtr[] native_trace_ips`（整数Ptr[] native_trace_ips）(偏移: 0x40)

### 方法 (23)

- `void Init()`
  （void 初始化（））
- `string get_Message()`
  （字符串 获取_消息（））
- `IDictionary get_Data()`
  （I字典 get_数据（））
- `bool IsImmutableAgileException(Exception e)`
  （bool 是否ImmutableAgileException（Exception e））
- `string GetClassName()`
  （string 获取类名称（））
- `Exception get_InnerException()`
  （Exception get_InnerException（））
- `MethodBase get_TargetSite()`
  （Method基础 get_目标Site（））
- `string get_StackTrace()`
  （string get_栈Trace（））
- `string GetStackTrace(bool needFileInfo)`
  （string 获取栈Trace（bool needFileInfo））
- `void SetErrorCode(int hr)`
  （void 集合ErrorCode（int hr））
- `string get_Source()`
  （string get_Source（））
- `string ToString()`
  （字符串 转字符串（））
- `string ToString(bool needFileLineInfo, bool needMessage)`
  （string To字符串（bool needFileLineInfo, bool needMessage））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））
- `void OnDeserialized(StreamingContext context)`
  （void OnDeserialized（StreamingContext context））
- `string StripFileInfo(string stackTrace, bool isRemoteStackTrace)`
  （string Strip文件信息（string stackTrace, bool isRemoteStackTrace））
- `void RestoreExceptionDispatchInfo(ExceptionDispatchInfo exceptionDispatchInfo)`
  （void RestoreExceptionDispatch信息（ExceptionDispatch信息 exceptionDispatchInfo））
- `int get_HResult()`
  （int get_HResult（））
- `void set_HResult(int value)`
  （void set_HResult（int value））
- `Type GetType()`
  （类型 获取类型（））
- `string GetMessageFromNativeResources(Exception.ExceptionMessageKind kind)`
  （string 获取MessageFromNativeResources（Exception.ExceptionMessageKind kind））
- `Exception FixRemotingException()`
  （Exception FixRemotingException（））
- `void ReportUnhandledException(Exception exception)`
  （void ReportUnhandledException（Exception exception））

---

## Exception.ExceptionMessageKind（Exception.ExceptionMessageKind）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ExceptionArgument（ExceptionArgument）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ExceptionDispatchInfo（ExceptionDispatch信息）

### 字段 (2)

- `Exception m_Exception`（Exception m_Exception）(偏移: 0x8)
- `object m_stackTrace`（object m_stackTrace）(偏移: 0xC)

### 方法 (4)

- `object get_BinaryStackTraceArray()`
  （object get_Binary栈Trace数组（））
- `ExceptionDispatchInfo Capture(Exception source)`
  （ExceptionDispatch信息 Capture（Exception source））
- `Exception get_SourceException()`
  （Exception get_SourceException（））
- `void Throw()`
  （void 投掷（））

---

## ExceptionHandlingClause（ExceptionHandlingClause）

### 字段 (7)

- `Type catch_type`（类型 catch_type）(偏移: 0x8)
- `int filter_offset`（int filter_offset）(偏移: 0xC)
- `ExceptionHandlingClauseOptions flags`（ExceptionHandlingClauseOptions flags）(偏移: 0x10)
- `int try_offset`（int try_offset）(偏移: 0x14)
- `int try_length`（int try_length）(偏移: 0x18)
- `int handler_offset`（int handler_offset）(偏移: 0x1C)
- `int handler_length`（int handler_length）(偏移: 0x20)

### 方法 (1)

- `string ToString()`
  （字符串 转字符串（））

---

## ExceptionHandlingClauseOptions（ExceptionHandlingClauseOptions）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ExceptionResource（Exception资源）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ExclusiveReference（Exclusive引用）

### 字段 (3)

- `RegexRunner _ref`（RegexRunner _ref）(偏移: 0x8)
- `object _obj`（object _obj）(偏移: 0xC)
- `int _locked`（int _locked）(偏移: 0x10)

### 方法 (2)

- `object Get()`
  （object 获取（））
- `void Release(object obj)`
  （void Release（object obj））

---

## ExecuteEvents（执行Events）

### 字段 (19)

- `ExecuteEvents.EventFunction<IPointerEnterHandler> s_PointerEnterHandler`（执行Events.事件Function<I指针EnterHandler> s_指针Enter处理器）(偏移: 0x0)
- `ExecuteEvents.EventFunction<IPointerExitHandler> s_PointerExitHandler`（执行Events.事件Function<I指针ExitHandler> s_指针Exit处理器）(偏移: 0x4)
- `ExecuteEvents.EventFunction<IPointerDownHandler> s_PointerDownHandler`（执行Events.事件Function<I指针下Handler> s_指针下处理器）(偏移: 0x8)
- `ExecuteEvents.EventFunction<IPointerUpHandler> s_PointerUpHandler`（执行Events.事件Function<I指针上Handler> s_指针上处理器）(偏移: 0xC)
- `ExecuteEvents.EventFunction<IPointerClickHandler> s_PointerClickHandler`（执行Events.事件Function<I指针ClickHandler> s_指针Click处理器）(偏移: 0x10)
- `ExecuteEvents.EventFunction<IInitializePotentialDragHandler> s_InitializePotentialDragHandler`（执行Events.事件Function<I初始化PotentialDragHandler> s_初始化PotentialDrag处理器）(偏移: 0x14)
- `ExecuteEvents.EventFunction<IBeginDragHandler> s_BeginDragHandler`（执行Events.事件Function<IBeginDragHandler> s_BeginDrag处理器）(偏移: 0x18)
- `ExecuteEvents.EventFunction<IDragHandler> s_DragHandler`（执行Events.事件Function<IDragHandler> s_Drag处理器）(偏移: 0x1C)
- `ExecuteEvents.EventFunction<IEndDragHandler> s_EndDragHandler`（执行Events.事件Function<I结束DragHandler> s_结束Drag处理器）(偏移: 0x20)
- `ExecuteEvents.EventFunction<IDropHandler> s_DropHandler`（执行Events.事件Function<IDropHandler> s_Drop处理器）(偏移: 0x24)
- `ExecuteEvents.EventFunction<IScrollHandler> s_ScrollHandler`（执行Events.事件Function<I滚动Handler> s_滚动处理器）(偏移: 0x28)
- `ExecuteEvents.EventFunction<IUpdateSelectedHandler> s_UpdateSelectedHandler`（执行Events.事件Function<I更新选中的Handler> s_更新选中的处理器）(偏移: 0x2C)
- `ExecuteEvents.EventFunction<ISelectHandler> s_SelectHandler`（执行Events.事件Function<I选择Handler> s_选择处理器）(偏移: 0x30)
- `ExecuteEvents.EventFunction<IDeselectHandler> s_DeselectHandler`（执行Events.事件Function<I取消选择Handler> s_取消选择处理器）(偏移: 0x34)
- `ExecuteEvents.EventFunction<IMoveHandler> s_MoveHandler`（执行Events.事件Function<I移动Handler> s_移动处理器）(偏移: 0x38)
- `ExecuteEvents.EventFunction<ISubmitHandler> s_SubmitHandler`（执行Events.事件Function<ISubmitHandler> s_Submit处理器）(偏移: 0x3C)
- `ExecuteEvents.EventFunction<ICancelHandler> s_CancelHandler`（执行Events.事件Function<I取消Handler> s_取消处理器）(偏移: 0x40)
- `ObjectPool<List<IEventSystemHandler>> s_HandlerListPool`（对象Pool<List<I事件系统Handler>> s_处理器列表池）(偏移: 0x44)
- `List<Transform> s_InternalTransformList`（List<Transform> s_内部的变换列表）(偏移: 0x48)

### 方法 (35)

- `void Execute(IPointerEnterHandler handler, BaseEventData eventData)`
  （void 执行（I指针Enter处理器 handler, 基础事件数据 eventData））
- `void Execute(IPointerExitHandler handler, BaseEventData eventData)`
  （void 执行（I指针Exit处理器 handler, 基础事件数据 eventData））
- `void Execute(IPointerDownHandler handler, BaseEventData eventData)`
  （void 执行（I指针下处理器 handler, 基础事件数据 eventData））
- `void Execute(IPointerUpHandler handler, BaseEventData eventData)`
  （void 执行（I指针上处理器 handler, 基础事件数据 eventData））
- `void Execute(IPointerClickHandler handler, BaseEventData eventData)`
  （void 执行（I指针Click处理器 handler, 基础事件数据 eventData））
- `void Execute(IInitializePotentialDragHandler handler, BaseEventData eventData)`
  （void 执行（I初始化PotentialDrag处理器 handler, 基础事件数据 eventData））
- `void Execute(IBeginDragHandler handler, BaseEventData eventData)`
  （void 执行（IBeginDrag处理器 handler, 基础事件数据 eventData））
- `void Execute(IDragHandler handler, BaseEventData eventData)`
  （void 执行（IDrag处理器 handler, 基础事件数据 eventData））
- `void Execute(IEndDragHandler handler, BaseEventData eventData)`
  （void 执行（I结束Drag处理器 handler, 基础事件数据 eventData））
- `void Execute(IDropHandler handler, BaseEventData eventData)`
  （void 执行（IDrop处理器 handler, 基础事件数据 eventData））
- `void Execute(IScrollHandler handler, BaseEventData eventData)`
  （void 执行（I滚动处理器 handler, 基础事件数据 eventData））
- `void Execute(IUpdateSelectedHandler handler, BaseEventData eventData)`
  （void 执行（I更新选中的处理器 handler, 基础事件数据 eventData））
- `void Execute(ISelectHandler handler, BaseEventData eventData)`
  （void 执行（I选择处理器 handler, 基础事件数据 eventData））
- `void Execute(IDeselectHandler handler, BaseEventData eventData)`
  （void 执行（I取消选择处理器 handler, 基础事件数据 eventData））
- `void Execute(IMoveHandler handler, BaseEventData eventData)`
  （void 执行（I移动处理器 handler, 基础事件数据 eventData））
- `void Execute(ISubmitHandler handler, BaseEventData eventData)`
  （void 执行（ISubmit处理器 handler, 基础事件数据 eventData））
- `void Execute(ICancelHandler handler, BaseEventData eventData)`
  （void 执行（I取消处理器 handler, 基础事件数据 eventData））
- `ExecuteEvents.EventFunction<IPointerEnterHandler> get_pointerEnterHandler()`
  （执行Events.事件Function<I指针EnterHandler> get_pointerEnter处理器（））
- `ExecuteEvents.EventFunction<IPointerExitHandler> get_pointerExitHandler()`
  （执行Events.事件Function<I指针ExitHandler> get_pointerExit处理器（））
- `ExecuteEvents.EventFunction<IPointerDownHandler> get_pointerDownHandler()`
  （执行Events.事件Function<I指针下Handler> get_pointer下处理器（））
- `ExecuteEvents.EventFunction<IPointerUpHandler> get_pointerUpHandler()`
  （执行Events.事件Function<I指针上Handler> get_pointer上处理器（））
- `ExecuteEvents.EventFunction<IPointerClickHandler> get_pointerClickHandler()`
  （执行Events.事件Function<I指针ClickHandler> get_pointerClick处理器（））
- `ExecuteEvents.EventFunction<IInitializePotentialDragHandler> get_initializePotentialDrag()`
  （执行Events.事件Function<I初始化PotentialDragHandler> get_initializePotentialDrag（））
- `ExecuteEvents.EventFunction<IBeginDragHandler> get_beginDragHandler()`
  （执行Events.事件Function<IBeginDragHandler> get_beginDrag处理器（））
- `ExecuteEvents.EventFunction<IDragHandler> get_dragHandler()`
  （执行Events.事件Function<IDragHandler> get_drag处理器（））
- `ExecuteEvents.EventFunction<IEndDragHandler> get_endDragHandler()`
  （执行Events.事件Function<I结束DragHandler> get_endDrag处理器（））
- `ExecuteEvents.EventFunction<IDropHandler> get_dropHandler()`
  （执行Events.事件Function<IDropHandler> get_drop处理器（））
- `ExecuteEvents.EventFunction<IScrollHandler> get_scrollHandler()`
  （执行Events.事件Function<I滚动Handler> get_scroll处理器（））
- `ExecuteEvents.EventFunction<IUpdateSelectedHandler> get_updateSelectedHandler()`
  （执行Events.事件Function<I更新选中的Handler> get_update选中的处理器（））
- `ExecuteEvents.EventFunction<ISelectHandler> get_selectHandler()`
  （执行Events.事件Function<I选择Handler> get_select处理器（））
- `ExecuteEvents.EventFunction<IDeselectHandler> get_deselectHandler()`
  （执行Events.事件Function<I取消选择Handler> get_deselect处理器（））
- `ExecuteEvents.EventFunction<IMoveHandler> get_moveHandler()`
  （执行Events.事件Function<I移动Handler> get_move处理器（））
- `ExecuteEvents.EventFunction<ISubmitHandler> get_submitHandler()`
  （执行Events.事件Function<ISubmitHandler> get_submit处理器（））
- `ExecuteEvents.EventFunction<ICancelHandler> get_cancelHandler()`
  （执行Events.事件Function<I取消Handler> get_cancel处理器（））
- `void GetEventChain(GameObject root, IList<Transform> eventChain)`
  （void 获取事件Chain（游戏对象 root, IList<Transform> eventChain））

---

## ExecutionContext（ExecutionContext）

**继承**: IDisposable, ISerializable（IDisposable, ISerializable）

### 字段 (7)

- `SynchronizationContext _syncContext`（SynchronizationContext _syncContext）(偏移: 0x8)
- `SynchronizationContext _syncContextNoFlow`（SynchronizationContext _syncContextNoFlow）(偏移: 0xC)
- `LogicalCallContext _logicalCallContext`（LogicalCallContext _logicalCallContext）(偏移: 0x10)
- `IllogicalCallContext _illogicalCallContext`（IllogicalCallContext _illogicalCallContext）(偏移: 0x14)
- `ExecutionContext.Flags _flags`（ExecutionContext.Flags _flags）(偏移: 0x18)
- `List<IAsyncLocal> _localChangeNotifications`（List<I异步Local> _localChangeNotifications）(偏移: 0x20)
- `ExecutionContext s_dummyDefaultEC`（ExecutionContext s_dummy默认的EC）(偏移: 0x0)

### 方法 (32)

- `bool get_isNewCapture()`
  （bool get_is新的Capture（））
- `void set_isNewCapture(bool value)`
  （void set_is新的Capture（bool value））
- `bool get_isFlowSuppressed()`
  （bool get_isFlowSuppressed（））
- `void set_isFlowSuppressed(bool value)`
  （void set_isFlowSuppressed（bool value））
- `ExecutionContext get_PreAllocatedDefault()`
  （ExecutionContext get_PreAllocated默认的（））
- `bool get_IsPreAllocatedDefault()`
  （bool get_是否PreAllocated默认的（））
- `object GetLocalValue(IAsyncLocal local)`
  （object 获取本地的值（I异步本地的 local））
- `void SetLocalValue(IAsyncLocal local, object newValue, bool needChangeNotifications)`
  （void 集合本地的值（I异步本地的 local, object newValue, bool needChangeNotifications））
- `void OnAsyncLocalContextChanged(ExecutionContext previous, ExecutionContext current)`
  （void On异步本地的ContextChanged（ExecutionContext previous, ExecutionContext current））
- `LogicalCallContext get_LogicalCallContext()`
  （逻辑调用上下文 获取_逻辑调用上下文（））
- `void set_LogicalCallContext(LogicalCallContext value)`
  （void set_LogicalCallContext（LogicalCallContext value））
- `IllogicalCallContext get_IllogicalCallContext()`
  （IllogicalCallContext get_IllogicalCallContext（））
- `void set_IllogicalCallContext(IllogicalCallContext value)`
  （void set_IllogicalCallContext（IllogicalCallContext value））
- `SynchronizationContext get_SynchronizationContext()`
  （SynchronizationContext get_SynchronizationContext（））
- `void set_SynchronizationContext(SynchronizationContext value)`
  （void set_SynchronizationContext（SynchronizationContext value））
- `SynchronizationContext get_SynchronizationContextNoFlow()`
  （SynchronizationContext get_SynchronizationContextNoFlow（））
- `void set_SynchronizationContextNoFlow(SynchronizationContext value)`
  （void set_SynchronizationContextNoFlow（SynchronizationContext value））
- `void Dispose()`
  （void 释放（））
- `void Run(ExecutionContext executionContext, ContextCallback callback, object state)`
  （void 运行（ExecutionContext executionContext, Context回调 callback, object state））
- `void Run(ExecutionContext executionContext, ContextCallback callback, object state, bool preserveSyncCtx)`
  （void 运行（ExecutionContext executionContext, Context回调 callback, object state, bool preserveSyncCtx））
- `void RunInternal(ExecutionContext executionContext, ContextCallback callback, object state, bool preserveSyncCtx)`
  （void 运行内部的（ExecutionContext executionContext, Context回调 callback, object state, bool preserveSyncCtx））
- `void EstablishCopyOnWriteScope(ref ExecutionContextSwitcher ecsw)`
  （void Establish复制OnWrite瞄准镜（ref ExecutionContextSwitcher ecsw））
- `void EstablishCopyOnWriteScope(Thread currentThread, bool knownNullWindowsIdentity, ref ExecutionContextSwitcher ecsw)`
  （void Establish复制OnWrite瞄准镜（Thread currentThread, bool knownNullWindowsIdentity, ref ExecutionContextSwitcher ecsw））
- `ExecutionContextSwitcher SetExecutionContext(ExecutionContext executionContext, bool preserveSyncCtx)`
  （ExecutionContextSwitcher 集合ExecutionContext（ExecutionContext executionContext, bool preserveSyncCtx））
- `ExecutionContext CreateCopy()`
  （ExecutionContext 创建复制（））
- `ExecutionContext CreateMutableCopy()`
  （ExecutionContext 创建Mutable复制（））
- `bool IsFlowSuppressed()`
  （bool 是否FlowSuppressed（））
- `ExecutionContext Capture()`
  （ExecutionContext Capture（））
- `ExecutionContext FastCapture()`
  （ExecutionContext FastCapture（））
- `ExecutionContext Capture(ref StackCrawlMark stackMark, ExecutionContext.CaptureOptions options)`
  （ExecutionContext Capture（ref StackCrawlMark stackMark, ExecutionContext.CaptureOptions options））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））
- `bool IsDefaultFTContext(bool ignoreSyncCtx)`
  （bool 是否默认的FTContext（bool ignoreSyncCtx））

---

## ExecutionContext.CaptureOptions（ExecutionContext.CaptureOptions）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ExecutionContext.Flags（ExecutionContext.Flags）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ExecutionContext.Reader（ExecutionContext.读取器）

### 字段 (1)

- `ExecutionContext m_ec`（ExecutionContext m_ec）(偏移: 0x0)

### 方法 (9)

- `ExecutionContext DangerousGetRawExecutionContext()`
  （ExecutionContext Dangerous获取RawExecutionContext（））
- `bool get_IsNull()`
  （bool get_是否Null（））
- `bool IsDefaultFTContext(bool ignoreSyncCtx)`
  （bool 是否默认的FTContext（bool ignoreSyncCtx））
- `bool get_IsFlowSuppressed()`
  （bool get_是否FlowSuppressed（））
- `SynchronizationContext get_SynchronizationContext()`
  （SynchronizationContext get_SynchronizationContext（））
- `SynchronizationContext get_SynchronizationContextNoFlow()`
  （SynchronizationContext get_SynchronizationContextNoFlow（））
- `LogicalCallContext.Reader get_LogicalCallContext()`
  （LogicalCallContext.读取器 get_LogicalCallContext（））
- `object GetLocalValue(IAsyncLocal local)`
  （object 获取本地的值（I异步本地的 local））
- `bool HasSameLocalValues(ExecutionContext other)`
  （bool 是否有Same本地的Values（ExecutionContext other））

---

## ExecutionContextSwitcher（ExecutionContextSwitcher）

### 字段 (4)

- `ExecutionContext.Reader outerEC`（ExecutionContext.读取器 outerEC）(偏移: 0x0)
- `bool outerECBelongsToScope`（bool outerECBelongsTo瞄准镜）(偏移: 0x4)
- `object hecsw`（object hecsw）(偏移: 0x8)
- `Thread thread`（Thread thread）(偏移: 0xC)

### 方法 (2)

- `bool UndoNoThrow()`
  （bool UndoNo投掷（））
- `void Undo()`
  （void Undo（））

---

## ExpandString（Expand字符串）

### 字段 (1)

- `string value`（string value）(偏移: 0x8)

### 方法 (2)

- `string ToString()`
  （字符串 转字符串（））
- `string Expand()`
  （string Expand（））

---

## ExpandUtil（ExpandUtil）

### 字段 (2)

- `byte[] keyBytes`（byte[] keyBytes）(偏移: 0x0)
- `byte[] ivBytes`（byte[] ivBytes）(偏移: 0x4)

### 方法 (29)

- `bool IsTimeValidAndEnd(float time)`
  （bool 是否时间ValidAnd结束（float time））
- `int GetSign(float value)`
  （int 获取标志（float value））
- `Vector3 ClearDirY(Vector3 dir)`
  （三维向量 清除DirY（三维向量 dir））
- `float DistanceToRay(Vector3 point, Ray ray)`
  （float 距离ToRay（三维向量 point, Ray ray））
- `bool KnifeAtkCheck(Collider collider, Ray ray, float rad)`
  （bool 近战武器Atk检查（碰撞器 collider, Ray ray, float rad））
- `bool IsInRayRad(Vector3 point, Ray ray, float rad)`
  （bool 是否InRayRad（三维向量 point, Ray ray, float rad））
- `bool IsSphereInRayRad(Vector3 center, float radius, Ray ray, float rad)`
  （bool 是否SphereInRayRad（三维向量 center, float radius, Ray ray, float rad））
- `bool IsInRayRad(BoxCollider boxCollider, Ray ray, float rad)`
  （bool 是否InRayRad（Box碰撞器 boxCollider, Ray ray, float rad））
- `bool IsInRayRad(CapsuleCollider capsuleCollider, Ray ray, float rad)`
  （bool 是否InRayRad（Capsule碰撞器 capsuleCollider, Ray ray, float rad））
- `bool IsInRayRad(SphereCollider sphereCollider, Ray ray, float rad)`
  （bool 是否InRayRad（Sphere碰撞器 sphereCollider, Ray ray, float rad））
- `bool IsEnemy(Entity entity, Entity other)`
  （bool 是否Enemy（实体 entity, 实体 other））
- `bool IsSameTeam(Team team, Team otherTeam)`
  （bool 是否Same队伍（队伍 team, 队伍 otherTeam））
- `Vector3 DirToRot(Vector3 dir)`
  （三维向量 DirToRot（三维向量 dir））
- `float ClampIn180Degrees(float angle)`
  （float ClampIn180Degrees（float angle））
- `float GetDeltaXAngle(Vector3 fromDir, Vector3 toDir)`
  （float 获取DeltaX角度（三维向量 fromDir, 三维向量 toDir））
- `float GetDeltaYAngle(Vector3 fromDir, Vector3 toDir)`
  （float 获取DeltaY角度（三维向量 fromDir, 三维向量 toDir））
- `string GetSuffix(Team team)`
  （string 获取Suffix（队伍 team））
- `string GetSingleChar(CharacterModel.MoveDirection dir)`
  （string 获取单个Char（角色Model.移动方向 dir））
- `string AddSuffix(CharacterModel.MoveDirection dir, string head)`
  （string 添加Suffix（角色Model.移动方向 dir, string head））
- `void Synchronize(Animator thisAnimator, Animator otherAnimator)`
  （void Synchronize（动画器 thisAnimator, 动画器 otherAnimator））
- `void ApplySpriteSize(RectTransform rect, Sprite sprite)`
  （void 应用精灵大小（Rect变换 rect, 精灵 sprite））
- `string Load(string source, int head)`
  （string 加载（string source, int head））
- `string StringPack(string input)`
  （string 字符串Pack（string input））
- `string StringUnpack(string cipherStr)`
  （string 字符串Unpack（string cipherStr））
- `bool IsMouseInArea(Vector4 area)`
  （bool 是否鼠标InArea（Vector4 area））
- `int GetLevel(int exp, int[] expPerLevel)`
  （int 获取等级（int exp, int[] expPerLevel））
- `void SetSpriteSize(RectTransform rect, Sprite spr)`
  （void 集合精灵大小（Rect变换 rect, 精灵 spr））
- `void RefreshValue(Dropdown dropdown, int newValue)`
  （void 刷新值（Dropdown dropdown, int newValue））
- `void SetAllTransformScale(Transform transform, Vector3 scale)`
  （void 集合所有变换缩放（变换 transform, 三维向量 scale））

---

## ExposedProperty（Exposed属性）

### 字段 (2)

- `string m_Name`（字符串 m_名称）(偏移: 0x8)
- `int m_Id`（int m_Id）(偏移: 0xC)

### 方法 (5)

- `ExposedProperty op_Implicit(string name)`
  （Exposed属性 op_Implicit（string name））
- `string op_Explicit(ExposedProperty parameter)`
  （string op_Explicit（Exposed属性 parameter））
- `int op_Implicit(ExposedProperty parameter)`
  （int op_Implicit（Exposed属性 parameter））
- `ExposedProperty op_Addition(ExposedProperty self, ExposedProperty other)`
  （Exposed属性 op_Addition（Exposed属性 self, Exposed属性 other））
- `string ToString()`
  （字符串 转字符串（））

---

## ExtendedPropertyDescriptor（Extended属性Descriptor）

**继承**: PropertyDescriptor（属性Descriptor）

### 字段 (2)

- `ReflectPropertyDescriptor extenderInfo`（Reflect属性Descriptor extender信息）(偏移: 0x44)
- `IExtenderProvider provider`（IExtender提供者 provider）(偏移: 0x48)

### 方法 (4)

- `Type get_ComponentType()`
  （类型 get_组件类型（））
- `bool get_IsReadOnly()`
  （布尔值 获取_是否只读（））
- `Type get_PropertyType()`
  （类型 get_属性类型（））
- `string get_DisplayName()`
  （字符串 获取_显示名称（））

---

## ExtenderProvidedPropertyAttribute（ExtenderProvided属性Attribute）

**继承**: Attribute（属性）

### 字段 (3)

- `PropertyDescriptor extenderProperty`（属性Descriptor extender属性）(偏移: 0x8)
- `IExtenderProvider provider`（IExtender提供者 provider）(偏移: 0xC)
- `Type receiverType`（类型 receiver类型）(偏移: 0x10)

### 方法 (7)

- `ExtenderProvidedPropertyAttribute Create(PropertyDescriptor extenderProperty, Type receiverType, IExtenderProvider provider)`
  （ExtenderProvided属性Attribute 创建（属性Descriptor extenderProperty, 类型 receiverType, IExtender提供者 provider））
- `PropertyDescriptor get_ExtenderProperty()`
  （属性Descriptor get_Extender属性（））
- `IExtenderProvider get_Provider()`
  （IExtender提供者 get_提供者（））
- `Type get_ReceiverType()`
  （类型 get_Receiver类型（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `bool IsDefaultAttribute()`
  （布尔值 是否默认属性（））

---

## ExternalException（外部的Exception）

**继承**: SystemException（系统异常）

### 方法 (1)

- `string ToString()`
  （字符串 转字符串（））

---

## ExtractExistingFileAction（ExtractExisting文件动作）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ExtractProgressEventArgs（ExtractProgress事件Args）

**继承**: ZipProgressEventArgs（Zip进度事件参数）

### 字段 (1)

- `string _target`（string _target）(偏移: 0x30)

### 方法 (4)

- `ExtractProgressEventArgs BeforeExtractEntry(string archiveName, ZipEntry entry, string extractLocation)`
  （ExtractProgress事件Args BeforeExtractEntry（string archiveName, ZipEntry entry, string extractLocation））
- `ExtractProgressEventArgs ExtractExisting(string archiveName, ZipEntry entry, string extractLocation)`
  （ExtractProgress事件Args ExtractExisting（string archiveName, ZipEntry entry, string extractLocation））
- `ExtractProgressEventArgs AfterExtractEntry(string archiveName, ZipEntry entry, string extractLocation)`
  （ExtractProgress事件Args AfterExtractEntry（string archiveName, ZipEntry entry, string extractLocation））
- `ExtractProgressEventArgs ByteUpdate(string archiveName, ZipEntry entry, long bytesWritten, long totalBytes)`
  （ExtractProgress事件Args Byte更新（string archiveName, ZipEntry entry, long bytesWritten, long totalBytes））

---

## Extrapolation（Extrapolation）

### 字段 (1)

- `double kMinExtrapolationTime`（double k最小Extrapolation时间）(偏移: 0x383F381D)

### 方法 (2)

- `void CalculateExtrapolationTimes(TrackAsset asset)`
  （void 计算ExtrapolationTimes（Track资产 asset））
- `TimelineClip[] SortClipsByStartTime(TimelineClip[] clips)`
  （TimelineClip[] SortClipsBy开始时间（TimelineClip[] clips））

---

## Eyes（Eyes）

**继承**: IEquatable<Eyes>（IEquatable<Eyes>）

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
- `bool Equals(Eyes other)`
  （bool Equals（Eyes other））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## FABRIK（FABRIK）

**继承**: IK（IK反向运动学）

### 字段 (1)

- `IKSolverFABRIK solver`（IKSolverFABRIK solver）(偏移: 0x1C)

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

## FABRIKChain（FABRIKChain）

### 字段 (4)

- `FABRIK ik`（FABRIK ik）(偏移: 0x8)
- `float pull`（float pull）(偏移: 0xC)
- `float pin`（float pin）(偏移: 0x10)
- `int[] children`（int[] children）(偏移: 0x14)

### 方法 (5)

- `bool IsValid(ref string message)`
  （布尔值 是否有效（引用 字符串 message））
- `void Initiate()`
  （void 启动（））
- `void Stage1(FABRIKChain[] chain)`
  （void Stage1（FABRIKChain[] chain））
- `void Stage2(Vector3 rootPosition, FABRIKChain[] chain)`
  （void Stage2（三维向量 rootPosition, FABRIKChain[] chain））
- `Vector3 GetCentroid(FABRIKChain[] chain)`
  （三维向量 获取Centroid（FABRIKChain[] chain））

---

## FABRIKRoot（FABRIK根）

**继承**: IK（IK反向运动学）

### 字段 (1)

- `IKSolverFABRIKRoot solver`（IKSolverFABRIK根 solver）(偏移: 0x1C)

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

## FBBIKArmBending（FBBIK手臂Bending）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (8)

- `FullBodyBipedIK ik`（全身双足IK ik）(偏移: 0xC)
- `Vector3 bendDirectionOffsetLeft`（三维向量 bend方向Offset左）(偏移: 0x10)
- `Vector3 bendDirectionOffsetRight`（三维向量 bend方向Offset右）(偏移: 0x1C)
- `Vector3 characterSpaceBendOffsetLeft`（三维向量 characterSpaceBendOffset左）(偏移: 0x28)
- `Vector3 characterSpaceBendOffsetRight`（三维向量 characterSpaceBendOffset右）(偏移: 0x34)
- `Quaternion leftHandTargetRotation`（Quaternion left手部目标Rotation）(偏移: 0x40)
- `Quaternion rightHandTargetRotation`（Quaternion right手部目标Rotation）(偏移: 0x50)
- `bool initiated`（布尔值 已启动）(偏移: 0x60)

### 方法 (3)

- `void LateUpdate()`
  （void 延迟更新（））
- `void OnPostFBBIK()`
  （void OnPostFBBIK（））
- `void OnDestroy()`
  （void 销毁时（））

---

## FBBIKHeadEffector（FBBIK头部Effector）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (46)

- `FullBodyBipedIK ik`（全身双足IK ik）(偏移: 0xC)
- `float positionWeight`（浮点数 位置权重）(偏移: 0x10)
- `float bodyWeight`（float bodyWeight）(偏移: 0x14)
- `float thighWeight`（float thighWeight）(偏移: 0x18)
- `bool handsPullBody`（bool handsPull身体）(偏移: 0x1C)
- `float rotationWeight`（浮点数 旋转权重）(偏移: 0x20)
- `float bodyClampWeight`（float bodyClampWeight）(偏移: 0x24)
- `float headClampWeight`（float headClampWeight）(偏移: 0x28)
- `float bendWeight`（float bendWeight）(偏移: 0x2C)
- `FBBIKHeadEffector.BendBone[] bendBones`（FBBIK头部Effector.BendBone[] bendBones）(偏移: 0x30)
- `float CCDWeight`（float CCDWeight）(偏移: 0x34)
- `float roll`（float roll）(偏移: 0x38)
- `float damper`（float damper）(偏移: 0x3C)
- `Transform[] CCDBones`（Transform[] CCDBones）(偏移: 0x40)
- `float postStretchWeight`（float postStretchWeight）(偏移: 0x44)
- `float maxStretch`（float maxStretch）(偏移: 0x48)
- `float stretchDamper`（float stretchDamper）(偏移: 0x4C)
- `bool fixHead`（bool fix头部）(偏移: 0x50)
- `Transform[] stretchBones`（Transform[] stretchBones）(偏移: 0x54)
- `Vector3 chestDirection`（三维向量 chest方向）(偏移: 0x58)
- `float chestDirectionWeight`（float chest方向Weight）(偏移: 0x64)
- `Transform[] chestBones`（Transform[] chestBones）(偏移: 0x68)
- `IKSolver.UpdateDelegate OnPostHeadEffectorFK`（IKSolver.更新委托 OnPost头部EffectorFK）(偏移: 0x6C)
- `Vector3 offset`（三维向量 偏移）(偏移: 0x70)
- `Vector3 headToBody`（三维向量 headTo身体）(偏移: 0x7C)
- `Vector3 shoulderCenterToHead`（三维向量 shoulder中心To头部）(偏移: 0x88)
- `Vector3 headToLeftThigh`（三维向量 headTo左Thigh）(偏移: 0x94)
- `Vector3 headToRightThigh`（三维向量 headTo右Thigh）(偏移: 0xA0)
- `Vector3 leftShoulderPos`（三维向量 leftShoulderPos）(偏移: 0xAC)
- `Vector3 rightShoulderPos`（三维向量 rightShoulderPos）(偏移: 0xB8)
- `float shoulderDist`（float shoulderDist）(偏移: 0xC4)
- `float leftShoulderDist`（float leftShoulderDist）(偏移: 0xC8)
- `float rightShoulderDist`（float rightShoulderDist）(偏移: 0xCC)
- `Quaternion chestRotation`（Quaternion chestRotation）(偏移: 0xD0)
- `Quaternion headRotationRelativeToRoot`（Quaternion headRotationRelativeTo根）(偏移: 0xE0)
- `Quaternion[] ccdDefaultLocalRotations`（Quaternion[] ccd默认的本地的Rotations）(偏移: 0xF0)
- `Vector3 headLocalPosition`（三维向量 head本地的Position）(偏移: 0xF4)
- `Quaternion headLocalRotation`（Quaternion head本地的Rotation）(偏移: 0x100)
- `Vector3[] stretchLocalPositions`（Vector3[] stretch本地的Positions）(偏移: 0x110)
- `Quaternion[] stretchLocalRotations`（Quaternion[] stretch本地的Rotations）(偏移: 0x114)
- `Vector3[] chestLocalPositions`（Vector3[] chest本地的Positions）(偏移: 0x118)
- `Quaternion[] chestLocalRotations`（Quaternion[] chest本地的Rotations）(偏移: 0x11C)
- `int bendBonesCount`（int bendBones数量）(偏移: 0x120)
- `int ccdBonesCount`（int ccdBones数量）(偏移: 0x124)
- `int stretchBonesCount`（int stretchBones数量）(偏移: 0x128)
- `int chestBonesCount`（int chestBones数量）(偏移: 0x12C)

### 方法 (13)

- `void Start()`
  （void 开始（））
- `void OnStoreDefaultLocalState()`
  （void On商店默认的本地的状态（））
- `void OnFixTransforms()`
  （void OnFixTransforms（））
- `void OnPreRead()`
  （void OnPreRead（））
- `void SpineBend()`
  （void SpineBend（））
- `void CCDPass()`
  （void CCDPass（））
- `void Iterate(int iteration)`
  （void Iterate（int iteration））
- `void OnPostUpdate()`
  （void OnPost更新（））
- `void ChestDirection()`
  （void 胸部方向（））
- `void PostStretching()`
  （void PostStretching（））
- `void LerpSolverPosition(IKEffector effector, Vector3 position, float weight, Vector3 offset)`
  （void LerpSolverPosition（IKEffector effector, 三维向量 position, float weight, 三维向量 offset））
- `void Solve(ref Vector3 pos1, ref Vector3 pos2, float nominalDistance)`
  （void Solve（ref Vector3 pos1, ref Vector3 pos2, float nominalDistance））
- `void OnDestroy()`
  （void 销毁时（））

---

## FBBIKHeadEffector.BendBone（FBBIK头部Effector.BendBone）

### 字段 (3)

- `Transform transform`（变换 transform）(偏移: 0x8)
- `float weight`（浮点数 权重）(偏移: 0xC)
- `Quaternion defaultLocalRotation`（四元数 默认本地旋转）(偏移: 0x10)

### 方法 (2)

- `void StoreDefaultLocalState()`
  （void 商店默认的本地的状态（））
- `void FixTransforms()`
  （void 修复变换（））

---

## FBIKChain（FBIKChain）

### 字段 (22)

- `float pin`（float pin）(偏移: 0x8)
- `float pull`（float pull）(偏移: 0xC)
- `float push`（float push）(偏移: 0x10)
- `float pushParent`（float push父级）(偏移: 0x14)
- `float reach`（float reach）(偏移: 0x18)
- `FBIKChain.Smoothing reachSmoothing`（FBIKChain.Smoothing reachSmoothing）(偏移: 0x1C)
- `FBIKChain.Smoothing pushSmoothing`（FBIKChain.Smoothing pushSmoothing）(偏移: 0x20)
- `IKSolver.Node[] nodes`（IKSolver.Node[] nodes）(偏移: 0x24)
- `int[] children`（int[] children）(偏移: 0x28)
- `FBIKChain.ChildConstraint[] childConstraints`（FBIKChain.子级Constraint[] childConstraints）(偏移: 0x2C)
- `IKConstraintBend bendConstraint`（IKConstraintBend bendConstraint）(偏移: 0x30)
- `float rootLength`（float rootLength）(偏移: 0x34)
- `bool initiated`（布尔值 已启动）(偏移: 0x38)
- `float length`（浮点数 长度）(偏移: 0x3C)
- `float distance`（浮点数 距离）(偏移: 0x40)
- `IKSolver.Point p`（IKSolver.Point p）(偏移: 0x44)
- `float reachForce`（float reach强制）(偏移: 0x48)
- `float pullParentSum`（float pull父级Sum）(偏移: 0x4C)
- `float[] crossFades`（float[] crossFades）(偏移: 0x50)
- `float sqrMag1`（float sqrMag1）(偏移: 0x54)
- `float sqrMag2`（float sqrMag2）(偏移: 0x58)
- `float sqrMagDif`（float sqrMagDif）(偏移: 0x5C)

### 方法 (18)

- `void SetNodes(Transform[] boneTransforms)`
  （void 集合Nodes（Transform[] boneTransforms））
- `int GetNodeIndex(Transform boneTransform)`
  （int 获取节点索引（变换 boneTransform））
- `bool IsValid(ref string message)`
  （布尔值 是否有效（引用 字符串 message））
- `void Initiate(IKSolverFullBody solver)`
  （void 启动（IK求解器全身 solver））
- `void ReadPose(IKSolverFullBody solver, bool fullBody)`
  （void ReadPose（IKSolver满身体 solver, bool fullBody））
- `void CalculateBoneLengths(IKSolverFullBody solver)`
  （void 计算BoneLengths（IKSolver满身体 solver））
- `void Reach(IKSolverFullBody solver)`
  （void Reach（IKSolver满身体 solver））
- `Vector3 Push(IKSolverFullBody solver)`
  （三维向量 Push（IKSolver满身体 solver））
- `void SolveTrigonometric(IKSolverFullBody solver, bool calculateBendDirection = False)`
  （void SolveTrigonometric（IKSolver满身体 solver, bool calculateBendDirection = False））
- `void Stage1(IKSolverFullBody solver)`
  （void Stage1（IKSolver满身体 solver））
- `void Stage2(IKSolverFullBody solver, Vector3 position)`
  （void Stage2（IKSolver满身体 solver, 三维向量 position））
- `void SolveConstraintSystems(IKSolverFullBody solver)`
  （void SolveConstraintSystems（IKSolver满身体 solver））
- `Vector3 SolveFABRIKJoint(Vector3 pos1, Vector3 pos2, float length)`
  （三维向量 SolveFABRIKJoint（三维向量 pos1, 三维向量 pos2, float length））
- `Vector3 GetDirToBendPoint(Vector3 direction, Vector3 bendDirection, float directionMagnitude)`
  （三维向量 获取DirToBendPoint（三维向量 direction, 三维向量 bendDirection, float directionMagnitude））
- `void SolveChildConstraints(IKSolverFullBody solver)`
  （void Solve子级Constraints（IKSolver满身体 solver））
- `void SolveLinearConstraint(IKSolver.Node node1, IKSolver.Node node2, float crossFade, float distance)`
  （void SolveLinearConstraint（IKSolver.节点 node1, IKSolver.节点 node2, float crossFade, float distance））
- `void ForwardReach(Vector3 position)`
  （void 前进Reach（三维向量 position））
- `void BackwardReach(Vector3 position)`
  （void 后退Reach（三维向量 position））

---

## FBIKChain.ChildConstraint（FBIKChain.子级Constraint）

### 字段 (8)

- `float pushElasticity`（float pushElasticity）(偏移: 0x8)
- `float pullElasticity`（float pullElasticity）(偏移: 0xC)
- `Transform bone1`（变换 bone1）(偏移: 0x10)
- `Transform bone2`（变换 bone2）(偏移: 0x14)
- `float crossFade`（float crossFade）(偏移: 0x20)
- `float inverseCrossFade`（float inverseCrossFade）(偏移: 0x24)
- `int chain1Index`（int chain1索引）(偏移: 0x28)
- `int chain2Index`（int chain2索引）(偏移: 0x2C)

### 方法 (7)

- `float get_nominalDistance()`
  （float get_nominal距离（））
- `void set_nominalDistance(float value)`
  （void set_nominal距离（float value））
- `bool get_isRigid()`
  （bool get_isRigid（））
- `void set_isRigid(bool value)`
  （void set_isRigid（bool value））
- `void Initiate(IKSolverFullBody solver)`
  （void 启动（IK求解器全身 solver））
- `void OnPreSolve(IKSolverFullBody solver)`
  （void OnPreSolve（IKSolver满身体 solver））
- `void Solve(IKSolverFullBody solver)`
  （void Solve（IKSolver满身体 solver））

---

## FBIKChain.Smoothing（FBIKChain.Smoothing）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FFTWindow（FFTWindow）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FKOffset（FKOffset）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (2)

- `FKOffset.Offset[] offsets`（FKOffset.Offset[] offsets）(偏移: 0xC)
- `Animator animator`（动画器 animator）(偏移: 0x10)

### 方法 (3)

- `void Start()`
  （void 开始（））
- `void LateUpdate()`
  （void 延迟更新（））
- `void OnDrawGizmosSelected()`
  （void 绘制选中辅助线时（））

---

## FKOffset.Offset（FKOffset.Offset）

### 字段 (4)

- `string name`（字符串 名称）(偏移: 0x8)
- `HumanBodyBones bone`（人类身体Bones bone）(偏移: 0xC)
- `Vector3 rotationOffset`（三维向量 rotationOffset）(偏移: 0x10)
- `Transform t`（变换 t）(偏移: 0x1C)

### 方法 (1)

- `void Apply(Animator animator)`
  （void 应用（动画器 animator））

---

## FORMATFLAGS（FORMATFLAGS）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FalloffType（Falloff类型）

### 字段 (1)

- `byte value__`（字节 值__）(偏移: 0x0)

---

## FastMemoryDesc（FastMemoryDesc）

### 字段 (3)

- `bool inFastMemory`（bool inFastMemory）(偏移: 0x0)
- `FastMemoryFlags flags`（FastMemoryFlags flags）(偏移: 0x4)
- `float residencyFraction`（float residencyFraction）(偏移: 0x8)

---

## FastMemoryFlags（FastMemoryFlags）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FastResourceComparer（Fast资源Comparer）

**继承**: IComparer, IEqualityComparer, IComparer<string>, IEqualityComparer<string>（IComparer, IEqualityComparer, IComparer<string>, IEqualityComparer<string>）

### 字段 (1)

- `FastResourceComparer Default`（Fast资源Comparer 默认的）(偏移: 0x0)

### 方法 (10)

- `int GetHashCode(object key)`
  （int 获取HashCode（object key））
- `int GetHashCode(string key)`
  （int 获取HashCode（string key））
- `int HashFunction(string key)`
  （int HashFunction（string key））
- `int Compare(object a, object b)`
  （整数 比较（对象 a, 对象 b））
- `int Compare(string a, string b)`
  （int Compare（string a, string b））
- `bool Equals(string a, string b)`
  （bool Equals（string a, string b））
- `bool Equals(object a, object b)`
  （bool Equals（object a, object b））
- `int CompareOrdinal(string a, byte[] bytes, int bCharLength)`
  （int CompareOrdinal（string a, byte[] bytes, int bCharLength））
- `int CompareOrdinal(byte[] bytes, int aCharLength, string b)`
  （int CompareOrdinal（byte[] bytes, int aCharLength, string b））
- `int CompareOrdinal(byte* a, int byteLen, string b)`
  （int CompareOrdinal（byte* a, int byteLen, string b））

---

## FieldAttributes（FieldAttributes）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FieldBuilder（Field构建器）

**继承**: FieldInfo（Field信息）

### 方法 (11)

- `FieldAttributes get_Attributes()`
  （FieldAttributes get_Attributes（））
- `Type get_DeclaringType()`
  （类型 获取_声明类型（））
- `Type get_FieldType()`
  （类型 get_Field类型（））
- `string get_Name()`
  （字符串 获取_名称（））
- `object GetValue(object obj)`
  （object 获取值（object obj））
- `RuntimeFieldHandle get_FieldHandle()`
  （RuntimeField句柄 get_Field句柄（））
- `Type get_ReflectedType()`
  （类型 获取_反射类型（））
- `object[] GetCustomAttributes(bool inherit)`
  （对象[] 获取自定义属性（布尔值 继承））
- `object[] GetCustomAttributes(Type attributeType, bool inherit)`
  （对象[] 获取自定义属性（类型 attributeType, 布尔值 继承））
- `bool IsDefined(Type attributeType, bool inherit)`
  （布尔值 是否已定义（类型 attributeType, 布尔值 继承））
- `void SetValue(object obj, object val, BindingFlags invokeAttr, Binder binder, CultureInfo culture)`
  （void 集合值（object obj, object val, BindingFlags invokeAttr, Binder binder, Culture信息 culture））

---

## FieldInfo（Field信息）

**继承**: MemberInfo, _FieldInfo（Member信息, _Field信息）

### 方法 (18)

- `MemberTypes get_MemberType()`
  （成员类型 获取_成员类型（））
- `bool get_IsLiteral()`
  （bool get_是否Literal（））
- `bool get_IsStatic()`
  （bool get_是否静态的（））
- `bool get_IsPublic()`
  （bool get_是否公开的（））
- `bool get_IsNotSerialized()`
  （bool get_是否NotSerialized（））
- `void SetValue(object obj, object value)`
  （void 集合值（object obj, object value））
- `FieldInfo internal_from_handle_type(IntPtr field_handle, IntPtr type_handle)`
  （Field信息 internal_from_handle_type（整数Ptr field_handle, 整数Ptr type_handle））
- `FieldInfo GetFieldFromHandle(RuntimeFieldHandle handle)`
  （Field信息 获取FieldFrom句柄（RuntimeField句柄 handle））
- `FieldInfo GetFieldFromHandle(RuntimeFieldHandle handle, RuntimeTypeHandle declaringType)`
  （Field信息 获取FieldFrom句柄（RuntimeField句柄 handle, Runtime类型句柄 declaringType））
- `int GetFieldOffset()`
  （int 获取FieldOffset（））
- `void SetValueDirect(TypedReference obj, object value)`
  （void 集合值Direct（Typed引用 obj, object value））
- `MarshalAsAttribute get_marshal_info()`
  （MarshalAsAttribute get_marshal_info（））
- `object[] GetPseudoCustomAttributes()`
  （object[] 获取Pseudo自定义的Attributes（））
- `object GetRawConstantValue()`
  （object 获取RawConstant值（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `bool op_Equality(FieldInfo left, FieldInfo right)`
  （bool op_Equality（Field信息 left, Field信息 right））
- `bool op_Inequality(FieldInfo left, FieldInfo right)`
  （bool op_Inequality（Field信息 left, Field信息 right））

---

## FieldMetadata（FieldMetadata）

### 字段 (7)

- `string name`（字符串 名称）(偏移: 0x8)
- `int nameSize`（int name大小）(偏移: 0xC)
- `EventFieldTags tags`（事件FieldTags tags）(偏移: 0x10)
- `byte[] custom`（byte[] custom）(偏移: 0x14)
- `ushort fixedCount`（ushort fixed数量）(偏移: 0x18)
- `byte inType`（byte in类型）(偏移: 0x1A)
- `byte outType`（byte out类型）(偏移: 0x1B)

### 方法 (2)

- `void IncrementStructFieldCount()`
  （void IncrementStructField数量（））
- `void Encode(ref int pos, byte[] metadata)`
  （void Encode（ref int pos, byte[] metadata））

---

## FieldOffsetAttribute（FieldOffsetAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `int _val`（int _val）(偏移: 0x8)

---

## FieldPacking（FieldPacking）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FieldPrecision（FieldPrecision）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## File（文件）

### 方法 (14)

- `FileStream Create(string path)`
  （文件流 创建（string path））
- `FileStream Create(string path, int bufferSize)`
  （文件流 创建（string path, int bufferSize））
- `void Delete(string path)`
  （void Delete（string path））
- `bool Exists(string path)`
  （bool Exists（string path））
- `void Move(string sourceFileName, string destFileName)`
  （void 移动（string sourceFileName, string destFileName））
- `FileStream Open(string path, FileMode mode)`
  （文件流 打开（string path, 文件模式 mode））
- `FileStream Open(string path, FileMode mode, FileAccess access, FileShare share)`
  （文件流 打开（string path, 文件模式 mode, 文件Access access, 文件Share share））
- `FileStream OpenRead(string path)`
  （文件流 打开Read（string path））
- `StreamReader OpenText(string path)`
  （流读取器 打开文本（string path））
- `void SetAttributes(string path, FileAttributes fileAttributes)`
  （void 集合Attributes（string path, 文件Attributes fileAttributes））
- `string ReadAllText(string path)`
  （string Read所有文本（string path））
- `void WriteAllText(string path, string contents)`
  （void Write所有文本（string path, string contents））
- `void WriteAllText(string path, string contents, Encoding encoding)`
  （void Write所有文本（string path, string contents, Encoding encoding））
- `int FillAttributeInfo(string path, ref MonoIOStat data, bool tryagain, bool returnErrorOnNotFound)`
  （int FillAttribute信息（string path, ref MonoIOStat data, bool tryagain, bool returnErrorOnNotFound））

---

## FileAccess（文件Access）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FileAttributes（文件Attributes）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FileBasedResourceGroveler（文件Based资源Groveler）

**继承**: IResourceGroveler（I资源Groveler）

### 字段 (1)

- `ResourceManager.ResourceManagerMediator _mediator`（资源Manager.资源管理器Mediator _mediator）(偏移: 0x8)

### 方法 (3)

- `ResourceSet GrovelForResourceSet(CultureInfo culture, Dictionary<string, ResourceSet> localResourceSets, bool tryParents, bool createIfNotExists, ref StackCrawlMark stackMark)`
  （资源集合 GrovelFor资源集合（Culture信息 culture, Dictionary<string, 资源Set> localResourceSets, bool tryParents, bool createIfNotExists, ref StackCrawlMark stackMark））
- `string FindResourceFile(CultureInfo culture, string fileName)`
  （string 查找资源文件（Culture信息 culture, string fileName））
- `ResourceSet CreateResourceSet(string file)`
  （资源集合 创建资源集合（string file））

---

## FileInfo（文件信息）

**继承**: FileSystemInfo（文件系统信息）

### 字段 (1)

- `string _name`（string _name）(偏移: 0x48)

### 方法 (8)

- `void Init(string fileName, bool checkHost)`
  （void 初始化（string fileName, bool checkHost））
- `string GetDisplayPath(string originalPath)`
  （string 获取Display路径（string originalPath））
- `string get_Name()`
  （字符串 获取_名称（））
- `string get_DirectoryName()`
  （string get_Directory名称（））
- `DirectoryInfo get_Directory()`
  （Directory信息 get_Directory（））
- `bool get_Exists()`
  （bool get_Exists（））
- `void MoveTo(string destFileName)`
  （void 移动To（string destFileName））
- `string ToString()`
  （字符串 转字符串（））

---

## FileLoadException（文件加载Exception）

**继承**: IOException（IOException）

### 字段 (2)

- `string _fileName`（string _file名称）(偏移: 0x48)
- `string _fusionLog`（string _fusionLog）(偏移: 0x4C)

### 方法 (6)

- `string get_Message()`
  （字符串 获取_消息（））
- `void SetMessageField()`
  （void 设置消息字段（））
- `string ToString()`
  （字符串 转字符串（））
- `string get_FusionLog()`
  （string get_FusionLog（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））
- `string FormatFileLoadExceptionMessage(string fileName, int hResult)`
  （string 格式化文件加载ExceptionMessage（string fileName, int hResult））

---

## FileMode（文件模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FileNotFoundException（文件NotFoundException）

**继承**: IOException（IOException）

### 字段 (2)

- `string _fileName`（string _file名称）(偏移: 0x48)
- `string _fusionLog`（string _fusionLog）(偏移: 0x4C)

### 方法 (5)

- `string get_Message()`
  （字符串 获取_消息（））
- `void SetMessageField()`
  （void 设置消息字段（））
- `string ToString()`
  （字符串 转字符串（））
- `string get_FusionLog()`
  （string get_FusionLog（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））

---

## FileOptions（文件Options）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FileReadType（文件Read类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FileShare（文件Share）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FileState（文件状态）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FileStream（文件流）

**继承**: Stream（流）

### 字段 (17)

- `byte[] buf_recycle`（byte[] buf_recycle）(偏移: 0x0)
- `object buf_recycle_lock`（object buf_recycle_lock）(偏移: 0x4)
- `byte[] buf`（byte[] buf）(偏移: 0x14)
- `string name`（字符串 名称）(偏移: 0x18)
- `SafeFileHandle safeHandle`（Safe文件句柄 safe句柄）(偏移: 0x1C)
- `bool isExposed`（bool isExposed）(偏移: 0x20)
- `long append_startpos`（long append_startpos）(偏移: 0x28)
- `FileAccess access`（文件Access access）(偏移: 0x30)
- `bool owner`（bool owner）(偏移: 0x34)
- `bool async`（bool async）(偏移: 0x35)
- `bool canseek`（bool canseek）(偏移: 0x36)
- `bool anonymous`（bool anonymous）(偏移: 0x37)
- `bool buf_dirty`（bool buf_dirty）(偏移: 0x38)
- `int buf_size`（int buf_size）(偏移: 0x3C)
- `int buf_length`（int buf_length）(偏移: 0x40)
- `int buf_offset`（int buf_offset）(偏移: 0x44)
- `long buf_start`（long buf_start）(偏移: 0x48)

### 方法 (32)

- `void Init(SafeFileHandle safeHandle, FileAccess access, bool ownsHandle, int bufferSize, bool isAsync, bool isConsoleWrapper)`
  （void 初始化（Safe文件句柄 safeHandle, 文件Access access, bool ownsHandle, int bufferSize, bool isAsync, bool isConsoleWrapper））
- `bool get_CanRead()`
  （布尔值 获取_能否读取（））
- `bool get_CanWrite()`
  （布尔值 获取_能否写入（））
- `bool get_CanSeek()`
  （布尔值 获取_能否查找（））
- `long get_Length()`
  （长整数 获取_长度（））
- `long get_Position()`
  （长整数 获取_位置（））
- `void set_Position(long value)`
  （void 设置_位置（长整数 value））
- `void ExposeHandle()`
  （void Expose句柄（））
- `int ReadByte()`
  （整数 读取字节（））
- `void WriteByte(byte value)`
  （void 写字节（字节 value））
- `int Read([In] [Out] byte[] array, int offset, int count)`
  （int Read（[In] [Out] byte[] array, int offset, int count））
- `int ReadInternal(byte[] dest, int offset, int count)`
  （int Read内部的（byte[] dest, int offset, int count））
- `IAsyncResult BeginRead(byte[] array, int offset, int numBytes, AsyncCallback userCallback, object stateObject)`
  （I异步Result BeginRead（byte[] array, int offset, int numBytes, 异步回调 userCallback, object stateObject））
- `int EndRead(IAsyncResult asyncResult)`
  （int 结束Read（I异步Result asyncResult））
- `void Write(byte[] array, int offset, int count)`
  （void Write（byte[] array, int offset, int count））
- `void WriteInternal(byte[] src, int offset, int count)`
  （void Write内部的（byte[] src, int offset, int count））
- `IAsyncResult BeginWrite(byte[] array, int offset, int numBytes, AsyncCallback userCallback, object stateObject)`
  （I异步Result BeginWrite（byte[] array, int offset, int numBytes, 异步回调 userCallback, object stateObject））
- `void EndWrite(IAsyncResult asyncResult)`
  （void 结束Write（I异步Result asyncResult））
- `long Seek(long offset, SeekOrigin origin)`
  （长整数 查找（长整数 offset, 查找起点 origin））
- `void SetLength(long value)`
  （void 设置_长度（长整数 value））
- `void Flush()`
  （void 刷新（））
- `void Finalize()`
  （void 终结（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `int ReadSegment(byte[] dest, int dest_offset, int count)`
  （int ReadSegment（byte[] dest, int dest_offset, int count））
- `int WriteSegment(byte[] src, int src_offset, int count)`
  （int WriteSegment（byte[] src, int src_offset, int count））
- `void FlushBuffer()`
  （void Flush缓冲区（））
- `void FlushBufferIfDirty()`
  （void Flush缓冲区IfDirty（））
- `void RefillBuffer()`
  （void Refill缓冲区（））
- `int ReadData(SafeHandle safeHandle, byte[] buf, int offset, int count)`
  （int Read数据（Safe句柄 safeHandle, byte[] buf, int offset, int count））
- `void InitBuffer(int size, bool isZeroSize)`
  （void 初始化缓冲区（int size, bool isZeroSize））
- `string GetSecureFileName(string filename)`
  （string 获取Secure文件名称（string filename））
- `string GetSecureFileName(string filename, bool full)`
  （string 获取Secure文件名称（string filename, bool full））

---

## FileStream.ReadDelegate（文件Stream.Read委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `int Invoke(byte[] buffer, int offset, int count)`
  （int Invoke（byte[] buffer, int offset, int count））
- `IAsyncResult BeginInvoke(byte[] buffer, int offset, int count, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（byte[] buffer, int offset, int count, 异步回调 callback, object object））
- `int EndInvoke(IAsyncResult result)`
  （int 结束Invoke（I异步Result result））

---

## FileStream.WriteDelegate（文件Stream.Write委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(byte[] buffer, int offset, int count)`
  （void Invoke（byte[] buffer, int offset, int count））
- `IAsyncResult BeginInvoke(byte[] buffer, int offset, int count, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（byte[] buffer, int offset, int count, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## FileStreamAsyncResult（文件流异步Result）

**继承**: IAsyncResult（I异步Result）

### 字段 (7)

- `object state`（object state）(偏移: 0x8)
- `ManualResetEvent wh`（手动重置事件 wh）(偏移: 0xC)
- `AsyncCallback cb`（异步回调 cb）(偏移: 0x10)
- `int Count`（int 数量）(偏移: 0x14)
- `int OriginalCount`（int Original数量）(偏移: 0x18)
- `int BytesRead`（int BytesRead）(偏移: 0x1C)
- `AsyncCallback realcb`（异步回调 realcb）(偏移: 0x20)

### 方法 (2)

- `void CBWrapper(IAsyncResult ares)`
  （void CB包装器（I异步Result ares））
- `WaitHandle get_AsyncWaitHandle()`
  （Wait句柄 get_异步Wait句柄（））

---

## FileSystemEnumerableFactory（文件系统Enumerable工厂）

### 方法 (1)

- `IEnumerable<string> CreateFileNameIterator(string path, string originalUserPath, string searchPattern, bool includeFiles, bool includeDirs, SearchOption searchOption, bool checkHost)`
  （IEnumerable<string> 创建文件名称Iterator（string path, string originalUserPath, string searchPattern, bool includeFiles, bool includeDirs, 搜索Option searchOption, bool checkHost））

---

## FileSystemEnumerableHelpers（文件系统EnumerableHelpers）

### 方法 (2)

- `bool IsDir(Win32Native.WIN32_FIND_DATA data)`
  （bool 是否Dir（Win32Native.WIN32_FIND_DATA data））
- `bool IsFile(Win32Native.WIN32_FIND_DATA data)`
  （bool 是否文件（Win32Native.WIN32_FIND_DATA data））

---

## FileSystemInfo（文件系统信息）

**继承**: MarshalByRefObject, ISerializable（MarshalByRef对象, ISerializable）

### 字段 (5)

- `MonoIOStat _data`（MonoIOStat _data）(偏移: 0x10)
- `int _dataInitialised`（int _dataInitialised）(偏移: 0x38)
- `string FullPath`（string 满路径）(偏移: 0x3C)
- `string OriginalPath`（string Original路径）(偏移: 0x40)
- `string _displayPath`（string _display路径）(偏移: 0x44)

### 方法 (5)

- `string get_FullName()`
  （字符串 获取_全名称（））
- `void Refresh()`
  （void 刷新（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））
- `string get_DisplayPath()`
  （string get_Display路径（））
- `void set_DisplayPath(string value)`
  （void set_Display路径（string value））

---

## FilmGrain（FilmGrain）

**继承**: VolumeComponent, IPostProcessComponent（体积组件, I后处理组件）

### 字段 (4)

- `FilmGrainLookupParameter type`（FilmGrainLookupParameter type）(偏移: 0x1C)
- `ClampedFloatParameter intensity`（钳制浮点数参数 强度）(偏移: 0x20)
- `ClampedFloatParameter response`（Clamped浮点数Parameter response）(偏移: 0x24)
- `NoInterpTextureParameter texture`（NoInterp纹理Parameter texture）(偏移: 0x28)

### 方法 (2)

- `bool IsActive()`
  （布尔值 是否激活的（））
- `bool IsTileCompatible()`
  （布尔值 是否瓦片兼容（））

---

## FilmGrainLookup（FilmGrainLookup）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FilterMode（Filter模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FilterType（Filter类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FilteringSettings（FilteringSettings）

**继承**: IEquatable<FilteringSettings>（IEquatable<FilteringSettings>）

### 字段 (5)

- `RenderQueueRange m_RenderQueueRange`（Render队列范围 m_Render队列范围）(偏移: 0x0)
- `int m_LayerMask`（int m_层掩码）(偏移: 0x8)
- `uint m_RenderingLayerMask`（uint m_Rendering层掩码）(偏移: 0xC)
- `int m_ExcludeMotionVectorObjects`（int m_ExcludeMotion向量Objects）(偏移: 0x10)
- `SortingLayerRange m_SortingLayerRange`（Sorting层范围 m_Sorting层范围）(偏移: 0x14)

### 方法 (8)

- `void set_renderQueueRange(RenderQueueRange value)`
  （void set_render队列范围（Render队列范围 value））
- `void set_layerMask(int value)`
  （void set_layer掩码（int value））
- `void set_renderingLayerMask(uint value)`
  （void set_rendering层掩码（uint value））
- `void set_excludeMotionVectorObjects(bool value)`
  （void set_excludeMotion向量Objects（bool value））
- `void set_sortingLayerRange(SortingLayerRange value)`
  （void set_sorting层范围（Sorting层范围 value））
- `bool Equals(FilteringSettings other)`
  （bool Equals（FilteringSettings other））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## FinalBlitPass（FinalBlitPass）

**继承**: ScriptableRenderPass（可脚本化渲染通道）

### 字段 (2)

- `RenderTargetHandle m_Source`（Render目标句柄 m_Source）(偏移: 0x54)
- `Material m_BlitMaterial`（材质 m_Blit材质）(偏移: 0x74)

### 方法 (2)

- `void Setup(RenderTextureDescriptor baseDescriptor, RenderTargetHandle colorHandle)`
  （void Setup（Render纹理Descriptor baseDescriptor, Render目标句柄 colorHandle））
- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（可脚本化渲染上下文 context, 引用 渲染数据 renderingData））

---

## Finger（Finger）

### 字段 (16)

- `float weight`（浮点数 权重）(偏移: 0x8)
- `float rotationWeight`（浮点数 旋转权重）(偏移: 0xC)
- `Finger.DOF rotationDOF`（Finger.DOF rotationDOF）(偏移: 0x10)
- `bool fixBone1Twist`（bool fixBone1Twist）(偏移: 0x14)
- `Transform bone1`（变换 bone1）(偏移: 0x18)
- `Transform bone2`（变换 bone2）(偏移: 0x1C)
- `Transform bone3`（变换 bone3）(偏移: 0x20)
- `Transform tip`（变换 tip）(偏移: 0x24)
- `Transform target`（变换 目标）(偏移: 0x28)
- `IKSolverLimb solver`（IKSolverLimb solver）(偏移: 0x30)
- `Quaternion bone3RelativeToTarget`（Quaternion bone3RelativeTo目标）(偏移: 0x34)
- `Vector3 bone3DefaultLocalPosition`（三维向量 bone3默认的本地的Position）(偏移: 0x44)
- `Quaternion bone3DefaultLocalRotation`（Quaternion bone3默认的本地的Rotation）(偏移: 0x50)
- `Vector3 bone1Axis`（三维向量 bone1轴）(偏移: 0x60)
- `Vector3 tipAxis`（三维向量 tip轴）(偏移: 0x6C)
- `Vector3 bone1TwistAxis`（三维向量 bone1Twist轴）(偏移: 0x78)

### 方法 (11)

- `bool get_initiated()`
  （布尔值 获取_已启动（））
- `void set_initiated(bool value)`
  （void 设置_已启动（布尔值 value））
- `Vector3 get_IKPosition()`
  （三维向量 get_IKPosition（））
- `void set_IKPosition(Vector3 value)`
  （void set_IKPosition（三维向量 value））
- `Quaternion get_IKRotation()`
  （Quaternion get_IKRotation（））
- `void set_IKRotation(Quaternion value)`
  （void set_IKRotation（Quaternion value））
- `bool IsValid(ref string errorMessage)`
  （bool 是否Valid（ref string errorMessage））
- `void Initiate(Transform hand, int index)`
  （void Initiate（变换 hand, int index））
- `void FixTransforms()`
  （void 修复变换（））
- `void StoreDefaultLocalState()`
  （void 商店默认的本地的状态（））
- `void Update(float masterWeight)`
  （void 更新（float masterWeight））

---

## Finger.DOF（Finger.DOF）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FingerRig（FingerRig）

**继承**: SolverManager（求解器管理器）

### 字段 (2)

- `float weight`（浮点数 权重）(偏移: 0x1C)
- `Finger[] fingers`（Finger[] fingers）(偏移: 0x20)

### 方法 (13)

- `bool get_initiated()`
  （布尔值 获取_已启动（））
- `void set_initiated(bool value)`
  （void 设置_已启动（布尔值 value））
- `bool IsValid(ref string errorMessage)`
  （bool 是否Valid（ref string errorMessage））
- `void AutoDetect()`
  （void 自动Detect（））
- `void AddFinger(Transform bone1, Transform bone2, Transform bone3, Transform tip, Transform target)`
  （void 添加Finger（变换 bone1, 变换 bone2, 变换 bone3, 变换 tip, 变换 target））
- `void RemoveFinger(int index)`
  （void 移除Finger（int index））
- `void AddChildrenRecursive(Transform parent, ref Transform[] array)`
  （void 添加ChildrenRecursive（变换 parent, ref Transform[] array））
- `void InitiateSolver()`
  （void 启动求解器（））
- `void UpdateFingerSolvers()`
  （void 更新FingerSolvers（））
- `void FixFingerTransforms()`
  （void FixFingerTransforms（））
- `void StoreDefaultLocalState()`
  （void 商店默认的本地的状态（））
- `void UpdateSolver()`
  （void 更新求解器（））
- `void FixTransforms()`
  （void 修复变换（））

---

## FixedBitArray3（固定BitArray3）

**继承**: IEnumerable, IEnumerable<bool>（IEnumerable, IEnumerable<bool>）

### 字段 (3)

- `bool _0`（bool _0）(偏移: 0x0)
- `bool _1`（bool _1）(偏移: 0x1)
- `bool _2`（bool _2）(偏移: 0x2)

### 方法 (5)

- `bool get_Item(int index)`
  （bool get_项目（int index））
- `void set_Item(int index, bool value)`
  （void set_项目（int index, bool value））
- `void Clear()`
  （void 清除（））
- `IEnumerable<bool> Enumerate()`
  （IEnumerable<bool> Enumerate（））
- `IEnumerator<bool> GetEnumerator()`
  （IEnumerator<bool> 获取Enumerator（））

---

## FixedBufferAttribute（固定缓冲区Attribute）

**继承**: Attribute（属性）

### 字段 (2)

- `Type elementType`（类型 element类型）(偏移: 0x8)
- `int length`（整数 长度）(偏移: 0xC)

### 方法 (2)

- `Type get_ElementType()`
  （类型 get_元素类型（））
- `int get_Length()`
  （整数 获取_长度（））

---

## FixupHolder（FixupHolder）

### 字段 (3)

- `long m_id`（long m_id）(偏移: 0x8)
- `object m_fixupInfo`（object m_fixup信息）(偏移: 0x10)
- `int m_fixupType`（int m_fixup类型）(偏移: 0x14)

---

## FixupHolderList（FixupHolder列表）

### 字段 (2)

- `FixupHolder[] m_values`（FixupHolder[] m_values）(偏移: 0x8)
- `int m_count`（int m_count）(偏移: 0xC)

### 方法 (2)

- `void Add(FixupHolder fixup)`
  （void 添加（FixupHolder fixup））
- `void EnlargeArray()`
  （void Enlarge数组（））

---

## Flash（Flash）

### 方法 (5)

- `float Ease(float time, float duration, float overshootOrAmplitude, float period)`
  （float Ease（float time, float duration, float overshootOrAmplitude, float period））
- `float EaseIn(float time, float duration, float overshootOrAmplitude, float period)`
  （float EaseIn（float time, float duration, float overshootOrAmplitude, float period））
- `float EaseOut(float time, float duration, float overshootOrAmplitude, float period)`
  （float EaseOut（float time, float duration, float overshootOrAmplitude, float period））
- `float EaseInOut(float time, float duration, float overshootOrAmplitude, float period)`
  （float EaseInOut（float time, float duration, float overshootOrAmplitude, float period））
- `float WeightedEase(float overshootOrAmplitude, float period, int stepIndex, float stepDuration, float dir, float res)`
  （float WeightedEase（float overshootOrAmplitude, float period, int stepIndex, float stepDuration, float dir, float res））

---

## FleePath（Flee路径）

**继承**: RandomPath（随机路径）

### 方法 (2)

- `FleePath Construct(Vector3 start, Vector3 avoid, int searchLength, OnPathDelegate callback)`
  （Flee路径 Construct（三维向量 start, 三维向量 avoid, int searchLength, On路径委托 callback））
- `void Setup(Vector3 start, Vector3 avoid, int searchLength, OnPathDelegate callback)`
  （void Setup（三维向量 start, 三维向量 avoid, int searchLength, On路径委托 callback））

---

## FloatData（浮点数数据）

**继承**: ComponentDataBase（组件数据基础）

### 字段 (1)

- `float value`（float value）(偏移: 0xC)

---

## FloatOptions（浮点数Options）

**继承**: IPlugOptions（I插件选项）

### 字段 (1)

- `bool snapping`（布尔值 吸附）(偏移: 0x0)

### 方法 (1)

- `void Reset()`
  （void 重置（））

---

## FloatPlugin（浮点数插件）

**继承**: ABSTweenPlugin<float, float, FloatOptions>（ABSTweenPlugin<float, float, 浮点数Options>）

### 方法 (8)

- `void Reset(TweenerCore<float, float, FloatOptions> t)`
  （void 重置（TweenerCore<float, float, 浮点数Options> t））
- `void SetFrom(TweenerCore<float, float, FloatOptions> t, bool isRelative)`
  （void 集合From（TweenerCore<float, float, 浮点数Options> t, bool isRelative））
- `void SetFrom(TweenerCore<float, float, FloatOptions> t, float fromValue, bool setImmediately, bool isRelative)`
  （void 集合From（TweenerCore<float, float, 浮点数Options> t, float fromValue, bool setImmediately, bool isRelative））
- `float ConvertToStartValue(TweenerCore<float, float, FloatOptions> t, float value)`
  （float 转换To开始值（TweenerCore<float, float, 浮点数Options> t, float value））
- `void SetRelativeEndValue(TweenerCore<float, float, FloatOptions> t)`
  （void 集合Relative结束值（TweenerCore<float, float, 浮点数Options> t））
- `void SetChangeValue(TweenerCore<float, float, FloatOptions> t)`
  （void 集合Change值（TweenerCore<float, float, 浮点数Options> t））
- `float GetSpeedBasedDuration(FloatOptions options, float unitsXSecond, float changeValue)`
  （float 获取SpeedBased持续时间（浮点数Options options, float unitsXSecond, float changeValue））
- `void EvaluateAndApply(FloatOptions options, Tween t, bool isRelative, DOGetter<float> getter, DOSetter<float> setter, float elapsed, float startValue, float changeValue, float duration, bool usingInversePosition, UpdateNotice updateNotice)`
  （void EvaluateAnd应用（浮点数Options options, Tween t, bool isRelative, DOGetter<float> getter, DOSetter<float> setter, float elapsed, float startValue, float changeValue, float duration, bool usingInversePosition, 更新Notice updateNotice））

---

## FloatRangeParameter（浮点数范围Parameter）

**继承**: VolumeParameter<Vector2>（VolumeParameter<Vector2>）

### 字段 (2)

- `float min`（浮点数 最小值）(偏移: 0x14)
- `float max`（浮点数 最大值）(偏移: 0x18)

### 方法 (3)

- `Vector2 get_value()`
  （二维向量 get_value（））
- `void set_value(Vector2 value)`
  （void set_value（二维向量 value））
- `void Interp(Vector2 from, Vector2 to, float t)`
  （void Interp（二维向量 from, 二维向量 to, float t））

---

## FloatTween（浮点数Tween）

**继承**: ITweenValue（ITween值）

### 字段 (5)

- `FloatTween.FloatTweenCallback m_Target`（浮点数Tween.浮点数Tween回调 m_目标）(偏移: 0x0)
- `float m_StartValue`（float m_开始值）(偏移: 0x4)
- `float m_TargetValue`（float m_目标值）(偏移: 0x8)
- `float m_Duration`（float m_持续时间）(偏移: 0xC)
- `bool m_IgnoreTimeScale`（bool m_Ignore时间缩放）(偏移: 0x10)

### 方法 (13)

- `float get_startValue()`
  （float get_start值（））
- `void set_startValue(float value)`
  （void set_start值（float value））
- `float get_targetValue()`
  （float get_target值（））
- `void set_targetValue(float value)`
  （void set_target值（float value））
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
- `void AddOnChangedCallback(UnityAction<float> callback)`
  （void 添加OnChanged回调（Unity引擎Action<float> callback））
- `bool GetIgnoreTimescale()`
  （bool 获取IgnoreTimescale（））
- `float GetDuration()`
  （float 获取持续时间（））
- `bool ValidTarget()`
  （bool Valid目标（））

---

## FloodPath（Flood路径）

**继承**: Path（路径）

### 字段 (4)

- `Vector3 originalStartPoint`（三维向量 original开始Point）(偏移: 0x78)
- `Vector3 startPoint`（三维向量 起点）(偏移: 0x84)
- `GraphNode startNode`（Graph节点 start节点）(偏移: 0x90)
- `bool saveParents`（bool saveParents）(偏移: 0x94)

### 方法 (11)

- `bool get_FloodingPath()`
  （布尔值 获取_泛洪路径（））
- `bool HasPathTo(GraphNode node)`
  （bool 是否有路径To（Graph节点 node））
- `GraphNode GetParent(GraphNode node)`
  （Graph节点 获取父级（Graph节点 node））
- `FloodPath Construct(Vector3 start, OnPathDelegate callback)`
  （Flood路径 Construct（三维向量 start, On路径委托 callback））
- `FloodPath Construct(GraphNode start, OnPathDelegate callback)`
  （Flood路径 Construct（Graph节点 start, On路径委托 callback））
- `void Setup(Vector3 start, OnPathDelegate callback)`
  （void Setup（三维向量 start, On路径委托 callback））
- `void Setup(GraphNode start, OnPathDelegate callback)`
  （void Setup（Graph节点 start, On路径委托 callback））
- `void Reset()`
  （void 重置（））
- `void Prepare()`
  （void 准备（））
- `void Initialize()`
  （void 初始化（））
- `void CalculateStep(long targetTick)`
  （void 计算步骤（长整数 targetTick））

---

## FloodPathConstraint（Flood路径Constraint）

**继承**: NNConstraint（NNConstraint）

### 字段 (1)

- `FloodPath path`（Flood路径 path）(偏移: 0x20)

### 方法 (1)

- `bool Suitable(GraphNode node)`
  （bool Suitable（Graph节点 node））

---

## FloodPathTracer（Flood路径Tracer）

**继承**: ABPath（AB路径）

### 字段 (1)

- `FloodPath flood`（Flood路径 flood）(偏移: 0xCC)

### 方法 (7)

- `bool get_hasEndPoint()`
  （bool get_has结束Point（））
- `FloodPathTracer Construct(Vector3 start, FloodPath flood, OnPathDelegate callback)`
  （Flood路径Tracer Construct（三维向量 start, Flood路径 flood, On路径委托 callback））
- `void Setup(Vector3 start, FloodPath flood, OnPathDelegate callback)`
  （void Setup（三维向量 start, Flood路径 flood, On路径委托 callback））
- `void Reset()`
  （void 重置（））
- `void Initialize()`
  （void 初始化（））
- `void CalculateStep(long targetTick)`
  （void 计算步骤（长整数 targetTick））
- `void Trace(GraphNode from)`
  （void Trace（Graph节点 from））

---

## FlushType（Flush类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FocusType（聚焦类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Font（Font）

**继承**: Object（对象）

### 字段 (2)

- `Action<Font> textureRebuilt`（Action<Font> textureRebuilt）(偏移: 0x0)
- `Font.FontTextureRebuildCallback m_FontTextureRebuildCallback`（Font.Font纹理Rebuild回调 m_Font纹理Rebuild回调）(偏移: 0xC)

### 方法 (8)

- `void add_textureRebuilt(Action<Font> value)`
  （void add_textureRebuilt（Action<Font> value））
- `void remove_textureRebuilt(Action<Font> value)`
  （void remove_textureRebuilt（Action<Font> value））
- `Material get_material()`
  （材质 获取_材质（））
- `bool get_dynamic()`
  （bool get_dynamic（））
- `int get_fontSize()`
  （int get_font大小（））
- `void InvokeTextureRebuilt_Internal(Font font)`
  （void Invoke纹理Rebuilt_内部的（Font font））
- `bool HasCharacter(char c)`
  （bool 是否有角色（char c））
- `bool HasCharacter(int c)`
  （bool 是否有角色（int c））

---

## Font.FontTextureRebuildCallback（Font.Font纹理Rebuild回调）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke()`
  （void 调用（））
- `IAsyncResult BeginInvoke(AsyncCallback callback, object object)`
  （I异步结果 开始调用（异步回调 callback, 对象 object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## FontData（Font数据）

**继承**: ISerializationCallbackReceiver（ISerialization回调接收器）

### 字段 (12)

- `Font m_Font`（Font m_Font）(偏移: 0x8)
- `int m_FontSize`（int m_Font大小）(偏移: 0xC)
- `FontStyle m_FontStyle`（FontStyle m_FontStyle）(偏移: 0x10)
- `bool m_BestFit`（bool m_BestFit）(偏移: 0x14)
- `int m_MinSize`（int m_最小大小）(偏移: 0x18)
- `int m_MaxSize`（int m_最大大小）(偏移: 0x1C)
- `TextAnchor m_Alignment`（文本Anchor m_Alignment）(偏移: 0x20)
- `bool m_AlignByGeometry`（bool m_AlignByGeometry）(偏移: 0x24)
- `bool m_RichText`（bool m_Rich文本）(偏移: 0x25)
- `HorizontalWrapMode m_HorizontalOverflow`（水平Wrap模式 m_水平Overflow）(偏移: 0x28)
- `VerticalWrapMode m_VerticalOverflow`（垂直Wrap模式 m_垂直Overflow）(偏移: 0x2C)
- `float m_LineSpacing`（float m_LineSpacing）(偏移: 0x30)

### 方法 (25)

- `FontData get_defaultFontData()`
  （Font数据 get_defaultFont数据（））
- `Font get_font()`
  （Font get_font（））
- `void set_font(Font value)`
  （void set_font（Font value））
- `int get_fontSize()`
  （int get_font大小（））
- `void set_fontSize(int value)`
  （void set_font大小（int value））
- `FontStyle get_fontStyle()`
  （FontStyle get_fontStyle（））
- `void set_fontStyle(FontStyle value)`
  （void set_fontStyle（FontStyle value））
- `bool get_bestFit()`
  （bool get_bestFit（））
- `void set_bestFit(bool value)`
  （void set_bestFit（bool value））
- `int get_minSize()`
  （int get_min大小（））
- `void set_minSize(int value)`
  （void set_min大小（int value））
- `int get_maxSize()`
  （int get_max大小（））
- `void set_maxSize(int value)`
  （void set_max大小（int value））
- `TextAnchor get_alignment()`
  （文本Anchor get_alignment（））
- `void set_alignment(TextAnchor value)`
  （void set_alignment（文本Anchor value））
- `bool get_alignByGeometry()`
  （bool get_alignByGeometry（））
- `void set_alignByGeometry(bool value)`
  （void set_alignByGeometry（bool value））
- `bool get_richText()`
  （bool get_rich文本（））
- `void set_richText(bool value)`
  （void set_rich文本（bool value））
- `HorizontalWrapMode get_horizontalOverflow()`
  （水平Wrap模式 get_horizontalOverflow（））
- `void set_horizontalOverflow(HorizontalWrapMode value)`
  （void set_horizontalOverflow（水平Wrap模式 value））
- `VerticalWrapMode get_verticalOverflow()`
  （垂直Wrap模式 get_verticalOverflow（））
- `void set_verticalOverflow(VerticalWrapMode value)`
  （void set_verticalOverflow（垂直Wrap模式 value））
- `float get_lineSpacing()`
  （float get_lineSpacing（））
- `void set_lineSpacing(float value)`
  （void set_lineSpacing（float value））

---

## FontStyle（FontStyle）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FontUpdateTracker（Font更新Tracker）

### 方法 (3)

- `void TrackText(Text t)`
  （void Track文本（文本 t））
- `void RebuildForFont(Font f)`
  （void RebuildForFont（Font f））
- `void UntrackText(Text t)`
  （void Untrack文本（文本 t））

---

## FootPosBaseEffect（脚部Pos基础特效）

**继承**: EffectObj（特效Obj）

### 方法 (2)

- `void LateUpdate()`
  （void 延迟更新（））
- `void UpdatePosition()`
  （void 更新Position（））

---

## ForceMode（强制模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FormatUsage（格式化Usage）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FormatterAssemblyStyle（FormatterAssemblyStyle）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FormatterConverter（FormatterConverter）

**继承**: IFormatterConverter（IFormatterConverter）

### 方法 (6)

- `object Convert(object value, Type type)`
  （object 转换（object value, 类型 type））
- `bool ToBoolean(object value)`
  （bool ToBoolean（object value））
- `int ToInt32(object value)`
  （int ToInt32（object value））
- `long ToInt64(object value)`
  （long ToInt64（object value））
- `float ToSingle(object value)`
  （float To单个（object value））
- `string ToString(object value)`
  （string To字符串（object value））

---

## FormatterServices（FormatterServices）

### 字段 (4)

- `bool unsafeTypeForwardersIsEnabled`（bool unsafe类型Forwarders是否启用的）(偏移: 0x4)
- `bool unsafeTypeForwardersIsEnabledInitialized`（bool unsafe类型Forwarders是否启用的Initialized）(偏移: 0x5)
- `Type[] advancedTypes`（Type[] advancedTypes）(偏移: 0x8)
- `Binder s_binder`（Binder s_binder）(偏移: 0xC)

### 方法 (19)

- `MemberInfo[] GetSerializableMembers(RuntimeType type)`
  （MemberInfo[] 获取SerializableMembers（Runtime类型 type））
- `bool CheckSerializable(RuntimeType type)`
  （bool 检查Serializable（Runtime类型 type））
- `MemberInfo[] InternalGetSerializableMembers(RuntimeType type)`
  （MemberInfo[] 内部的获取SerializableMembers（Runtime类型 type））
- `bool GetParentTypes(RuntimeType parentType, out RuntimeType[] parentTypes, out int parentTypeCount)`
  （bool 获取父级Types（Runtime类型 parentType, out RuntimeType[] parentTypes, out int parentTypeCount））
- `MemberInfo[] GetSerializableMembers(Type type, StreamingContext context)`
  （MemberInfo[] 获取SerializableMembers（类型 type, StreamingContext context））
- `object GetUninitializedObject(Type type)`
  （object 获取Uninitialized对象（类型 type））
- `object nativeGetUninitializedObject(RuntimeType type)`
  （object native获取Uninitialized对象（Runtime类型 type））
- `bool GetEnableUnsafeTypeForwarders()`
  （bool 获取启用Unsafe类型Forwarders（））
- `bool UnsafeTypeForwardersIsEnabled()`
  （bool Unsafe类型Forwarders是否启用的（））
- `void SerializationSetValue(MemberInfo fi, object target, object value)`
  （void Serialization集合值（Member信息 fi, object target, object value））
- `object PopulateObjectMembers(object obj, MemberInfo[] members, object[] data)`
  （object Populate对象Members（object obj, MemberInfo[] members, object[] data））
- `object[] GetObjectData(object obj, MemberInfo[] members)`
  （object[] 获取对象数据（object obj, MemberInfo[] members））
- `Type GetTypeFromAssembly(Assembly assem, string name)`
  （类型 获取类型FromAssembly（Assembly assem, string name））
- `Assembly LoadAssemblyFromString(string assemblyName)`
  （Assembly 加载AssemblyFrom字符串（string assemblyName））
- `Assembly LoadAssemblyFromStringNoThrow(string assemblyName)`
  （Assembly 加载AssemblyFrom字符串No投掷（string assemblyName））
- `string GetClrAssemblyName(Type type, out bool hasTypeForwardedFrom)`
  （string 获取ClrAssembly名称（类型 type, out bool hasTypeForwardedFrom））
- `string GetClrTypeFullName(Type type)`
  （string 获取Clr类型满名称（类型 type））
- `string GetClrTypeFullNameForArray(Type type)`
  （string 获取Clr类型满名称For数组（类型 type））
- `string GetClrTypeFullNameForNonArrayTypes(Type type)`
  （string 获取Clr类型满名称ForNon数组Types（类型 type））

---

## FormatterTypeStyle（Formatter类型Style）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FormerlySerializedAsAttribute（FormerlySerializedAsAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `string m_oldName`（string m_old名称）(偏移: 0x8)

---

## ForwardLights（前进Lights）

### 字段 (10)

- `int m_AdditionalLightsBufferId`（int m_AdditionalLights缓冲区Id）(偏移: 0x8)
- `int m_AdditionalLightsIndicesId`（int m_AdditionalLightsIndicesId）(偏移: 0xC)
- `ProfilingSampler m_ProfilingSampler`（性能分析采样器 m_性能分析采样器）(偏移: 0x0)
- `MixedLightingSetup m_MixedLightingSetup`（MixedLightingSetup m_MixedLightingSetup）(偏移: 0x10)
- `Vector4[] m_AdditionalLightPositions`（Vector4[] m_Additional光照Positions）(偏移: 0x14)
- `Vector4[] m_AdditionalLightColors`（Vector4[] m_Additional光照Colors）(偏移: 0x18)
- `Vector4[] m_AdditionalLightAttenuations`（Vector4[] m_Additional光照Attenuations）(偏移: 0x1C)
- `Vector4[] m_AdditionalLightSpotDirections`（Vector4[] m_Additional光照SpotDirections）(偏移: 0x20)
- `Vector4[] m_AdditionalLightOcclusionProbeChannels`（Vector4[] m_Additional光照OcclusionProbeChannels）(偏移: 0x24)
- `bool m_UseStructuredBuffer`（bool m_UseStructured缓冲区）(偏移: 0x28)

### 方法 (6)

- `void Setup(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void Setup（ScriptableRenderContext context, ref RenderingData renderingData））
- `void InitializeLightConstants(NativeArray<VisibleLight> lights, int lightIndex, out Vector4 lightPos, out Vector4 lightColor, out Vector4 lightAttenuation, out Vector4 lightSpotDir, out Vector4 lightOcclusionProbeChannel)`
  （void 初始化光照Constants（NativeArray<可见的Light> lights, int lightIndex, out Vector4 lightPos, out Vector4 lightColor, out Vector4 lightAttenuation, out Vector4 lightSpotDir, out Vector4 lightOcclusionProbeChannel））
- `void SetupShaderLightConstants(CommandBuffer cmd, ref RenderingData renderingData)`
  （void Setup着色器光照Constants（Command缓冲区 cmd, ref RenderingData renderingData））
- `void SetupMainLightConstants(CommandBuffer cmd, ref LightData lightData)`
  （void Setup主要的光照Constants（Command缓冲区 cmd, ref LightData lightData））
- `void SetupAdditionalLightConstants(CommandBuffer cmd, ref RenderingData renderingData)`
  （void SetupAdditional光照Constants（Command缓冲区 cmd, ref RenderingData renderingData））
- `int SetupPerObjectLightIndices(CullingResults cullResults, ref LightData lightData)`
  （int SetupPer对象光照Indices（CullingResults cullResults, ref LightData lightData））

---

## ForwardLights.LightConstantBuffer（前进Lights.光照Constant缓冲区）

### 字段 (9)

- `int _MainLightPosition`（int _主要的光照Position）(偏移: 0x0)
- `int _MainLightColor`（int _主要的光照颜色）(偏移: 0x4)
- `int _MainLightOcclusionProbesChannel`（int _主要的光照OcclusionProbesChannel）(偏移: 0x8)
- `int _AdditionalLightsCount`（int _AdditionalLights数量）(偏移: 0xC)
- `int _AdditionalLightsPosition`（int _AdditionalLightsPosition）(偏移: 0x10)
- `int _AdditionalLightsColor`（int _AdditionalLights颜色）(偏移: 0x14)
- `int _AdditionalLightsAttenuation`（int _AdditionalLightsAttenuation）(偏移: 0x18)
- `int _AdditionalLightsSpotDir`（int _AdditionalLightsSpotDir）(偏移: 0x1C)
- `int _AdditionalLightOcclusionProbeChannel`（int _Additional光照OcclusionProbeChannel）(偏移: 0x20)

---

## ForwardRenderer（前进渲染器）

**继承**: ScriptableRenderer（Scriptable渲染器）

### 字段 (47)

- `ColorGradingLutPass m_ColorGradingLutPass`（颜色GradingLutPass m_颜色GradingLutPass）(偏移: 0x5C)
- `DepthOnlyPass m_DepthPrepass`（深度OnlyPass m_深度Prepass）(偏移: 0x60)
- `DepthNormalOnlyPass m_DepthNormalPrepass`（深度法线OnlyPass m_深度法线Prepass）(偏移: 0x64)
- `MainLightShadowCasterPass m_MainLightShadowCasterPass`（主要的光照ShadowCasterPass m_主要的光照ShadowCasterPass）(偏移: 0x68)
- `AdditionalLightsShadowCasterPass m_AdditionalLightsShadowCasterPass`（AdditionalLightsShadowCasterPass m_AdditionalLightsShadowCasterPass）(偏移: 0x6C)
- `GBufferPass m_GBufferPass`（G缓冲区Pass m_G缓冲区Pass）(偏移: 0x70)
- `CopyDepthPass m_GBufferCopyDepthPass`（复制深度Pass m_G缓冲区复制深度Pass）(偏移: 0x74)
- `TileDepthRangePass m_TileDepthRangePass`（Tile深度范围Pass m_Tile深度范围Pass）(偏移: 0x78)
- `TileDepthRangePass m_TileDepthRangeExtraPass`（Tile深度范围Pass m_Tile深度范围额外的Pass）(偏移: 0x7C)
- `DeferredPass m_DeferredPass`（DeferredPass m_DeferredPass）(偏移: 0x80)
- `DrawObjectsPass m_RenderOpaqueForwardOnlyPass`（DrawObjectsPass m_Render不透明的前进OnlyPass）(偏移: 0x84)
- `DrawObjectsPass m_RenderOpaqueForwardPass`（DrawObjectsPass m_Render不透明的前进Pass）(偏移: 0x88)
- `DrawSkyboxPass m_DrawSkyboxPass`（DrawSkyboxPass m_DrawSkyboxPass）(偏移: 0x8C)
- `CopyDepthPass m_CopyDepthPass`（复制深度Pass m_复制深度Pass）(偏移: 0x90)
- `CopyColorPass m_CopyColorPass`（复制颜色Pass m_复制颜色Pass）(偏移: 0x94)
- `TransparentSettingsPass m_TransparentSettingsPass`（透明的SettingsPass m_透明的SettingsPass）(偏移: 0x98)
- `DrawObjectsPass m_RenderTransparentForwardPass`（DrawObjectsPass m_Render透明的前进Pass）(偏移: 0x9C)
- `InvokeOnRenderObjectCallbackPass m_OnRenderObjectCallbackPass`（InvokeOnRender对象回调Pass m_OnRender对象回调Pass）(偏移: 0xA0)
- `PostProcessPass m_PostProcessPass`（Post处理Pass m_Post处理Pass）(偏移: 0xA4)
- `PostProcessPass m_FinalPostProcessPass`（Post处理Pass m_FinalPost处理Pass）(偏移: 0xA8)
- `FinalBlitPass m_FinalBlitPass`（FinalBlitPass m_FinalBlitPass）(偏移: 0xAC)
- `CapturePass m_CapturePass`（CapturePass m_CapturePass）(偏移: 0xB0)
- `XROcclusionMeshPass m_XROcclusionMeshPass`（XROcclusion网格Pass m_XROcclusion网格Pass）(偏移: 0xB4)
- `CopyDepthPass m_XRCopyDepthPass`（复制深度Pass m_XR复制深度Pass）(偏移: 0xB8)
- `RenderTargetHandle m_ActiveCameraColorAttachment`（Render目标句柄 m_激活的摄像机颜色Attachment）(偏移: 0xBC)
- `RenderTargetHandle m_ActiveCameraDepthAttachment`（Render目标句柄 m_激活的摄像机深度Attachment）(偏移: 0xDC)
- `RenderTargetHandle m_CameraColorAttachment`（Render目标句柄 m_摄像机颜色Attachment）(偏移: 0xFC)
- `RenderTargetHandle m_CameraDepthAttachment`（Render目标句柄 m_摄像机深度Attachment）(偏移: 0x11C)
- `RenderTargetHandle m_DepthTexture`（Render目标句柄 m_深度纹理）(偏移: 0x13C)
- `RenderTargetHandle m_NormalsTexture`（Render目标句柄 m_Normals纹理）(偏移: 0x15C)
- `RenderTargetHandle[] m_GBufferHandles`（Render目标Handle[] m_G缓冲区Handles）(偏移: 0x17C)
- `RenderTargetHandle m_OpaqueColor`（Render目标句柄 m_不透明的颜色）(偏移: 0x180)
- `RenderTargetHandle m_AfterPostProcessColor`（Render目标句柄 m_AfterPost处理颜色）(偏移: 0x1A0)
- `RenderTargetHandle m_ColorGradingLut`（Render目标句柄 m_颜色GradingLut）(偏移: 0x1C0)
- `RenderTargetHandle m_DepthInfoTexture`（Render目标句柄 m_深度信息纹理）(偏移: 0x1E0)
- `RenderTargetHandle m_TileDepthInfoTexture`（Render目标句柄 m_Tile深度信息纹理）(偏移: 0x200)
- `ForwardLights m_ForwardLights`（前进Lights m_前进Lights）(偏移: 0x220)
- `DeferredLights m_DeferredLights`（DeferredLights m_DeferredLights）(偏移: 0x224)
- `RenderingMode m_RenderingMode`（Rendering模式 m_Rendering模式）(偏移: 0x228)
- `StencilState m_DefaultStencilState`（Stencil状态 m_默认的Stencil状态）(偏移: 0x22C)
- `Material m_BlitMaterial`（材质 m_Blit材质）(偏移: 0x238)
- `Material m_CopyDepthMaterial`（材质 m_复制深度材质）(偏移: 0x23C)
- `Material m_SamplingMaterial`（材质 m_Sampling材质）(偏移: 0x240)
- `Material m_ScreenspaceShadowsMaterial`（材质 m_ScreenspaceShadows材质）(偏移: 0x244)
- `Material m_TileDepthInfoMaterial`（材质 m_Tile深度信息材质）(偏移: 0x248)
- `Material m_TileDeferredMaterial`（材质 m_TileDeferred材质）(偏移: 0x24C)
- `Material m_StencilDeferredMaterial`（材质 m_StencilDeferred材质）(偏移: 0x250)

### 方法 (14)

- `RenderingMode get_renderingMode()`
  （Rendering模式 get_rendering模式（））
- `RenderingMode get_actualRenderingMode()`
  （Rendering模式 get_actualRendering模式（））
- `bool get_accurateGbufferNormals()`
  （bool get_accurateGbufferNormals（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `void Setup(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void Setup（ScriptableRenderContext context, ref RenderingData renderingData））
- `void SetupLights(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void SetupLights（ScriptableRenderContext context, ref RenderingData renderingData））
- `void SetupCullingParameters(ref ScriptableCullingParameters cullingParameters, ref CameraData cameraData)`
  （void SetupCullingParameters（ref ScriptableCullingParameters cullingParameters, ref CameraData cameraData））
- `void FinishRendering(CommandBuffer cmd)`
  （void FinishRendering（Command缓冲区 cmd））
- `void EnqueueDeferred(ref RenderingData renderingData, bool hasDepthPrepass, bool applyMainShadow, bool applyAdditionalShadow)`
  （void EnqueueDeferred（ref RenderingData renderingData, bool hasDepthPrepass, bool applyMainShadow, bool applyAdditionalShadow））
- `ForwardRenderer.RenderPassInputSummary GetRenderPassInputs(ref RenderingData renderingData)`
  （前进Renderer.RenderPass输入Summary 获取RenderPassInputs（ref RenderingData renderingData））
- `void CreateCameraRenderTarget(ScriptableRenderContext context, ref RenderTextureDescriptor descriptor, bool createColor, bool createDepth)`
  （void 创建摄像机Render目标（ScriptableRenderContext context, ref RenderTextureDescriptor descriptor, bool createColor, bool createDepth））
- `bool PlatformRequiresExplicitMsaaResolve()`
  （bool PlatformRequiresExplicitMsaaResolve（））
- `bool RequiresIntermediateColorTexture(ref CameraData cameraData)`
  （bool RequiresIntermediate颜色纹理（ref CameraData cameraData））
- `bool CanCopyDepth(ref CameraData cameraData)`
  （bool 能否复制深度（ref CameraData cameraData））

---

## ForwardRenderer.Profiling（前进Renderer.Profiling）

### 字段 (1)

- `ProfilingSampler createCameraRenderTarget`（ProfilingSampler create摄像机Render目标）(偏移: 0x32573235)

---

## ForwardRenderer.RenderPassInputSummary（前进Renderer.RenderPass输入Summary）

### 字段 (4)

- `bool requiresDepthTexture`（bool requires深度纹理）(偏移: 0x329B3271)
- `bool requiresDepthPrepass`（bool requires深度Prepass）(偏移: 0x32DF32B5)
- `bool requiresNormalsTexture`（bool requiresNormals纹理）(偏移: 0x332332F9)
- `bool requiresColorTexture`（bool requires颜色纹理）(偏移: 0x3367333D)

---

## ForwardRendererData（前进渲染器数据）

**继承**: ScriptableRendererData（Scriptable渲染器数据）

### 字段 (9)

- `PostProcessData postProcessData`（Post处理数据 post处理数据）(偏移: 0x18)
- `XRSystemData xrSystemData`（XR系统数据 xr系统数据）(偏移: 0x1C)
- `ForwardRendererData.ShaderResources shaders`（前进渲染器Data.着色器Resources shaders）(偏移: 0x20)
- `LayerMask m_OpaqueLayerMask`（层掩码 m_不透明的层掩码）(偏移: 0x24)
- `LayerMask m_TransparentLayerMask`（层掩码 m_透明的层掩码）(偏移: 0x28)
- `StencilStateData m_DefaultStencilState`（Stencil状态数据 m_默认的Stencil状态）(偏移: 0x2C)
- `bool m_ShadowTransparentReceive`（bool m_Shadow透明的接收）(偏移: 0x30)
- `RenderingMode m_RenderingMode`（Rendering模式 m_Rendering模式）(偏移: 0x34)
- `bool m_AccurateGbufferNormals`（bool m_AccurateGbufferNormals）(偏移: 0x38)

### 方法 (14)

- `ScriptableRenderer Create()`
  （Scriptable渲染器 创建（））
- `LayerMask get_opaqueLayerMask()`
  （层掩码 get_opaque层掩码（））
- `void set_opaqueLayerMask(LayerMask value)`
  （void set_opaque层掩码（层掩码 value））
- `LayerMask get_transparentLayerMask()`
  （层掩码 get_transparent层掩码（））
- `void set_transparentLayerMask(LayerMask value)`
  （void set_transparent层掩码（层掩码 value））
- `StencilStateData get_defaultStencilState()`
  （Stencil状态数据 get_defaultStencil状态（））
- `void set_defaultStencilState(StencilStateData value)`
  （void set_defaultStencil状态（Stencil状态数据 value））
- `bool get_shadowTransparentReceive()`
  （bool get_shadow透明的接收（））
- `void set_shadowTransparentReceive(bool value)`
  （void set_shadow透明的接收（bool value））
- `RenderingMode get_renderingMode()`
  （Rendering模式 get_rendering模式（））
- `void set_renderingMode(RenderingMode value)`
  （void set_rendering模式（Rendering模式 value））
- `bool get_accurateGbufferNormals()`
  （bool get_accurateGbufferNormals（））
- `void set_accurateGbufferNormals(bool value)`
  （void set_accurateGbufferNormals（bool value））
- `void OnEnable()`
  （void 启用时（））

---

## ForwardRendererData.ShaderResources（前进渲染器Data.着色器Resources）

### 字段 (9)

- `Shader blitPS`（着色器 blitPS）(偏移: 0x8)
- `Shader copyDepthPS`（着色器 copy深度PS）(偏移: 0xC)
- `Shader screenSpaceShadowPS`（着色器 screenSpaceShadowPS）(偏移: 0x10)
- `Shader samplingPS`（着色器 samplingPS）(偏移: 0x14)
- `Shader tileDepthInfoPS`（着色器 tile深度信息PS）(偏移: 0x18)
- `Shader tileDeferredPS`（着色器 tileDeferredPS）(偏移: 0x1C)
- `Shader stencilDeferredPS`（着色器 stencilDeferredPS）(偏移: 0x20)
- `Shader fallbackErrorPS`（着色器 fallbackErrorPS）(偏移: 0x24)
- `Shader materialErrorPS`（着色器 materialErrorPS）(偏移: 0x28)

---

## FrameData（Frame数据）

### 字段 (9)

- `ulong m_FrameID`（ulong m_FrameID）(偏移: 0x0)
- `double m_DeltaTime`（double m_Delta时间）(偏移: 0x8)
- `float m_Weight`（float m_Weight）(偏移: 0x10)
- `float m_EffectiveWeight`（float m_EffectiveWeight）(偏移: 0x14)
- `double m_EffectiveParentDelay`（double m_Effective父级延迟）(偏移: 0x18)
- `float m_EffectiveParentSpeed`（float m_Effective父级Speed）(偏移: 0x20)
- `float m_EffectiveSpeed`（float m_EffectiveSpeed）(偏移: 0x24)
- `FrameData.Flags m_Flags`（FrameData.Flags m_Flags）(偏移: 0x28)
- `PlayableOutput m_Output`（PlayableOutput m_Output）(偏移: 0x2C)

### 方法 (6)

- `bool HasFlags(FrameData.Flags flag)`
  （bool 是否有Flags（FrameData.Flags flag））
- `float get_deltaTime()`
  （浮点数 获取_增量时间（））
- `float get_effectiveSpeed()`
  （float get_effectiveSpeed（））
- `FrameData.EvaluationType get_evaluationType()`
  （FrameData.Evaluation类型 get_evaluation类型（））
- `bool get_timeLooped()`
  （bool get_timeLooped（））
- `PlayableOutput get_output()`
  （PlayableOutput get_output（））

---

## FrameData.EvaluationType（FrameData.Evaluation类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FrameData.Flags（FrameData.Flags）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FreeCamera（Free摄像机）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (22)

- `float m_LookSpeedController`（float m_LookSpeed控制器）(偏移: 0xC)
- `float m_LookSpeedMouse`（float m_LookSpeed鼠标）(偏移: 0x10)
- `float m_MoveSpeed`（float m_移动Speed）(偏移: 0x14)
- `float m_MoveSpeedIncrement`（float m_移动SpeedIncrement）(偏移: 0x18)
- `float m_Turbo`（float m_Turbo）(偏移: 0x1C)
- `string kMouseX`（string k鼠标X）(偏移: 0x0)
- `string kMouseY`（string k鼠标Y）(偏移: 0x4)
- `string kRightStickX`（string k右StickX）(偏移: 0x8)
- `string kRightStickY`（string k右StickY）(偏移: 0xC)
- `string kVertical`（string k垂直）(偏移: 0x10)
- `string kHorizontal`（string k水平）(偏移: 0x14)
- `string kYAxis`（string kY轴）(偏移: 0x18)
- `string kSpeedAxis`（string kSpeed轴）(偏移: 0x1C)
- `float inputRotateAxisX`（float inputRotate轴X）(偏移: 0x20)
- `float inputRotateAxisY`（float inputRotate轴Y）(偏移: 0x24)
- `float inputChangeSpeed`（float inputChangeSpeed）(偏移: 0x28)
- `float inputVertical`（float input垂直）(偏移: 0x2C)
- `float inputHorizontal`（float input水平）(偏移: 0x30)
- `float inputYAxis`（float inputY轴）(偏移: 0x34)
- `bool leftShiftBoost`（bool leftShiftBoost）(偏移: 0x38)
- `bool leftShift`（bool leftShift）(偏移: 0x39)
- `bool fire1`（bool fire1）(偏移: 0x3A)

### 方法 (4)

- `void OnEnable()`
  （void 启用时（））
- `void RegisterInputs()`
  （void RegisterInputs（））
- `void UpdateInputs()`
  （void 更新Inputs（））
- `void Update()`
  （void 更新（））

---

## FrustumPlanes（FrustumPlanes）

### 字段 (6)

- `float left`（float left）(偏移: 0x0)
- `float right`（float right）(偏移: 0x4)
- `float bottom`（float bottom）(偏移: 0x8)
- `float top`（float top）(偏移: 0xC)
- `float zNear`（float zNear）(偏移: 0x10)
- `float zFar`（float zFar）(偏移: 0x14)

---

## FullBodyBipedChain（满身体BipedChain）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FullBodyBipedEffector（满身体BipedEffector）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## FullBodyBipedIK（满身体BipedIK）

**继承**: IK（IK反向运动学）

### 字段 (2)

- `BipedReferences references`（BipedReferences references）(偏移: 0x1C)
- `IKSolverFullBodyBiped solver`（IKSolver满身体Biped solver）(偏移: 0x20)

### 方法 (12)

- `void OpenUserManual()`
  （void 打开用户手动（））
- `void OpenScriptReference()`
  （void 打开脚本引用（））
- `void OpenSetupTutorial()`
  （void 打开SetupTutorial（））
- `void OpenInspectorTutorial()`
  （void 打开InspectorTutorial（））
- `void SupportGroup()`
  （void 支持组（））
- `void ASThread()`
  （void 异步线程（））
- `void SetReferences(BipedReferences references, Transform rootNode)`
  （void 集合References（BipedReferences references, 变换 rootNode））
- `IKSolver GetIKSolver()`
  （IK求解器 获取IK求解器（））
- `bool ReferencesError(ref string errorMessage)`
  （bool ReferencesError（ref string errorMessage））
- `bool ReferencesWarning(ref string warningMessage)`
  （bool ReferencesWarning（ref string warningMessage））
- `void Reinitiate()`
  （void Reinitiate（））
- `void AutoDetectReferences()`
  （void 自动DetectReferences（））

---

## FullScreenMode（满屏幕的模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Function（Function）

**继承**: ChoiceBase（选择基类）

### 字段 (1)

- `Action action`（动作 action）(偏移: 0x14)

### 方法 (1)

- `bool OnSelect()`
  （bool On选择（））

---

## Funnel（Funnel）

### 方法 (12)

- `List<Funnel.PathPart> SplitIntoParts(Path path)`
  （List<Funnel.路径Part> SplitIntoParts（路径 path））
- `Funnel.FunnelPortals ConstructFunnelPortals(List<GraphNode> nodes, Funnel.PathPart part)`
  （Funnel.FunnelPortals ConstructFunnelPortals（List<GraphNode> nodes, Funnel.路径Part part））
- `void ShrinkPortals(Funnel.FunnelPortals portals, float shrink)`
  （void ShrinkPortals（Funnel.FunnelPortals portals, float shrink））
- `bool UnwrapHelper(Vector3 portalStart, Vector3 portalEnd, Vector3 prevPoint, Vector3 nextPoint, ref Quaternion mRot, ref Vector3 mOffset)`
  （bool Unwrap辅助器（三维向量 portalStart, 三维向量 portalEnd, 三维向量 prevPoint, 三维向量 nextPoint, ref Quaternion mRot, ref Vector3 mOffset））
- `void Unwrap(Funnel.FunnelPortals funnel, Vector2[] left, Vector2[] right)`
  （void Unwrap（Funnel.FunnelPortals funnel, Vector2[] left, Vector2[] right））
- `int FixFunnel(Vector2[] left, Vector2[] right, int numPortals)`
  （int FixFunnel（Vector2[] left, Vector2[] right, int numPortals））
- `Vector2 ToXZ(Vector3 p)`
  （二维向量 ToXZ（三维向量 p））
- `Vector3 FromXZ(Vector2 p)`
  （三维向量 FromXZ（二维向量 p））
- `bool RightOrColinear(Vector2 a, Vector2 b)`
  （bool 右OrColinear（二维向量 a, 二维向量 b））
- `bool LeftOrColinear(Vector2 a, Vector2 b)`
  （bool 左OrColinear（二维向量 a, 二维向量 b））
- `List<Vector3> Calculate(Funnel.FunnelPortals funnel, bool unwrap, bool splitAtEveryPortal)`
  （List<Vector3> 计算（Funnel.FunnelPortals funnel, bool unwrap, bool splitAtEveryPortal））
- `void Calculate(Vector2[] left, Vector2[] right, int numPortals, int startIndex, List<int> funnelPath, int maxCorners, out bool lastCorner)`
  （void 计算（Vector2[] left, Vector2[] right, int numPortals, int startIndex, List<int> funnelPath, int maxCorners, out bool lastCorner））

---

## Funnel.FunnelPortals（Funnel.FunnelPortals）

### 字段 (2)

- `List<Vector3> left`（List<Vector3> left）(偏移: 0x0)
- `List<Vector3> right`（List<Vector3> right）(偏移: 0x4)

---

## Funnel.PathPart（Funnel.路径Part）

### 字段 (5)

- `int startIndex`（int start索引）(偏移: 0x0)
- `int endIndex`（int end索引）(偏移: 0x4)
- `Vector3 startPoint`（三维向量 起点）(偏移: 0x8)
- `Vector3 endPoint`（三维向量 终点）(偏移: 0x14)
- `bool isLink`（bool isLink）(偏移: 0x20)

---

## FunnelModifier（Funnel修改器）

**继承**: MonoModifier（Mono修改器）

### 字段 (2)

- `bool unwrap`（bool unwrap）(偏移: 0x14)
- `bool splitAtEveryPortal`（bool splitAtEveryPortal）(偏移: 0x15)

### 方法 (2)

- `int get_Order()`
  （整数 获取_顺序（））
- `void Apply(Path p)`
  （void 应用（路径 p））

---

## GBufferPass（G缓冲区Pass）

**继承**: ScriptableRenderPass（可脚本化渲染通道）

### 字段 (11)

- `ShaderTagId s_ShaderTagLit`（着色器标签Id s_着色器标签Lit）(偏移: 0x0)
- `ShaderTagId s_ShaderTagSimpleLit`（着色器标签Id s_着色器标签SimpleLit）(偏移: 0x4)
- `ShaderTagId s_ShaderTagUnlit`（着色器标签Id s_着色器标签Unlit）(偏移: 0x8)
- `ShaderTagId s_ShaderTagUniversalGBuffer`（着色器标签Id s_着色器标签UniversalG缓冲区）(偏移: 0xC)
- `ShaderTagId s_ShaderTagUniversalMaterialType`（着色器标签Id s_着色器标签Universal材质类型）(偏移: 0x10)
- `ProfilingSampler m_ProfilingSampler`（性能分析采样器 m_性能分析采样器）(偏移: 0x54)
- `DeferredLights m_DeferredLights`（DeferredLights m_DeferredLights）(偏移: 0x58)
- `ShaderTagId[] m_ShaderTagValues`（着色器标签Id[] m_着色器标签Values）(偏移: 0x5C)
- `RenderStateBlock[] m_RenderStateBlocks`（Render状态Block[] m_Render状态Blocks）(偏移: 0x60)
- `FilteringSettings m_FilteringSettings`（过滤设置 m_过滤设置）(偏移: 0x64)
- `RenderStateBlock m_RenderStateBlock`（Render状态Block m_Render状态Block）(偏移: 0x7C)

### 方法 (3)

- `void Configure(CommandBuffer cmd, RenderTextureDescriptor cameraTextureDescriptor)`
  （void 配置（命令缓冲区 cmd, 渲染纹理描述符 cameraTextureDescriptor））
- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（可脚本化渲染上下文 context, 引用 渲染数据 renderingData））
- `void OnCameraCleanup(CommandBuffer cmd)`
  （void 摄像机清理时（命令缓冲区 cmd））

---

## GC（GC）

### 字段 (1)

- `object EPHEMERON_TOMBSTONE`（object EPHEMERON_TOMBSTONE）(偏移: 0x0)

### 方法 (17)

- `int GetCollectionCount(int generation)`
  （int 获取Collection数量（int generation））
- `int GetMaxGeneration()`
  （int 获取最大Generation（））
- `void InternalCollect(int generation)`
  （void 内部的Collect（int generation））
- `void RecordPressure(long bytesAllocated)`
  （void RecordPressure（long bytesAllocated））
- `void register_ephemeron_array(Ephemeron[] array)`
  （void register_ephemeron_array（Ephemeron[] array））
- `object get_ephemeron_tombstone()`
  （object get_ephemeron_tombstone（））
- `void AddMemoryPressure(long bytesAllocated)`
  （void 添加MemoryPressure（long bytesAllocated））
- `void RemoveMemoryPressure(long bytesAllocated)`
  （void 移除MemoryPressure（long bytesAllocated））
- `void Collect()`
  （void Collect（））
- `int CollectionCount(int generation)`
  （int Collection数量（int generation））
- `void KeepAlive(object obj)`
  （void KeepAlive（object obj））
- `int get_MaxGeneration()`
  （int get_最大Generation（））
- `void _SuppressFinalize(object o)`
  （void _SuppressFinalize（object o））
- `void SuppressFinalize(object obj)`
  （void SuppressFinalize（object obj））
- `void _ReRegisterForFinalize(object o)`
  （void _ReRegisterForFinalize（object o））
- `void ReRegisterForFinalize(object obj)`
  （void ReRegisterForFinalize（object obj））
- `long GetTotalMemory(bool forceFullCollection)`
  （long 获取TotalMemory（bool forceFullCollection））

---

## GCHandle（GC句柄）

### 字段 (1)

- `int handle`（int handle）(偏移: 0x0)

### 方法 (19)

- `bool get_IsAllocated()`
  （bool get_是否Allocated（））
- `object get_Target()`
  （object get_目标（））
- `void set_Target(object value)`
  （void set_目标（object value））
- `IntPtr AddrOfPinnedObject()`
  （整数Ptr AddrOfPinned对象（））
- `GCHandle Alloc(object value)`
  （GC句柄 Alloc（object value））
- `GCHandle Alloc(object value, GCHandleType type)`
  （GC句柄 Alloc（object value, GC句柄类型 type））
- `void Free()`
  （void Free（））
- `IntPtr op_Explicit(GCHandle value)`
  （整数Ptr op_Explicit（GC句柄 value））
- `GCHandle op_Explicit(IntPtr value)`
  （GC句柄 op_Explicit（整数Ptr value））
- `bool CheckCurrentDomain(int handle)`
  （bool 检查当前Domain（int handle））
- `object GetTarget(int handle)`
  （object 获取目标（int handle））
- `int GetTargetHandle(object obj, int handle, GCHandleType type)`
  （int 获取目标句柄（object obj, int handle, GC句柄类型 type））
- `void FreeHandle(int handle)`
  （void Free句柄（int handle））
- `IntPtr GetAddrOfPinnedObject(int handle)`
  （整数Ptr 获取AddrOfPinned对象（int handle））
- `bool op_Equality(GCHandle a, GCHandle b)`
  （bool op_Equality（GC句柄 a, GC句柄 b））
- `bool Equals(object o)`
  （布尔值 等于（对象 o））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `GCHandle FromIntPtr(IntPtr value)`
  （GC句柄 From整数Ptr（整数Ptr value））
- `IntPtr ToIntPtr(GCHandle value)`
  （整数Ptr To整数Ptr（GC句柄 value））

---

## GCHandleType（GC句柄类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## GL（GL）

### 方法 (3)

- `bool get_wireframe()`
  （bool get_wireframe（））
- `Matrix4x4 GetGPUProjectionMatrix(Matrix4x4 proj, bool renderIntoTexture)`
  （Matrix4x4 获取GPUProjection矩阵（Matrix4x4 proj, bool renderIntoTexture））
- `void GetGPUProjectionMatrix_Injected(ref Matrix4x4 proj, bool renderIntoTexture, out Matrix4x4 ret)`
  （void 获取GPUProjectionMatrix_Injected（ref Matrix4x4 proj, bool renderIntoTexture, out Matrix4x4 ret））

---

## GUI（GUI）

### 字段 (11)

- `int s_HotTextField`（int s_Hot文本Field）(偏移: 0x0)
- `int s_BoxHash`（int s_BoxHash）(偏移: 0x4)
- `int s_ButonHash`（int s_ButonHash）(偏移: 0x8)
- `int s_RepeatButtonHash`（int s_Repeat按钮Hash）(偏移: 0xC)
- `int s_ToggleHash`（int s_开关Hash）(偏移: 0x10)
- `int s_ButtonGridHash`（int s_按钮网格Hash）(偏移: 0x14)
- `int s_SliderHash`（int s_滑块Hash）(偏移: 0x18)
- `int s_BeginGroupHash`（int s_Begin组Hash）(偏移: 0x1C)
- `int s_ScrollviewHash`（int s_ScrollviewHash）(偏移: 0x20)
- `GUISkin s_Skin`（GUISkin s_Skin）(偏移: 0x30)
- `Rect s_ToolTipRect`（Rect s_ToolTipRect）(偏移: 0x34)

### 方法 (39)

- `Color get_color()`
  （颜色 获取_颜色（））
- `void set_color(Color value)`
  （void 设置_颜色（颜色 value））
- `void set_changed(bool value)`
  （void set_changed（bool value））
- `bool get_enabled()`
  （布尔值 获取_已启用（））
- `void set_enabled(bool value)`
  （void 设置_已启用（布尔值 value））
- `void GrabMouseControl(int id)`
  （void Grab鼠标控制（int id））
- `bool HasMouseControl(int id)`
  （bool 是否有鼠标控制（int id））
- `void ReleaseMouseControl()`
  （void Release鼠标控制（））
- `void SetNextControlName(string name)`
  （void 集合下一个控制名称（string name））
- `void set_nextScrollStepTime(DateTime value)`
  （void set_next滚动Step时间（Date时间 value））
- `void set_skin(GUISkin value)`
  （void set_skin（GUISkin value））
- `GUISkin get_skin()`
  （GUISkin get_skin（））
- `void DoSetSkin(GUISkin newSkin)`
  （void Do集合Skin（GUISkin newSkin））
- `void Label(Rect position, string text)`
  （void 标签（Rect position, string text））
- `void Label(Rect position, string text, GUIStyle style)`
  （void 标签（Rect position, string text, GUIStyle style））
- `void Label(Rect position, GUIContent content, GUIStyle style)`
  （void 标签（Rect position, GUIContent content, GUIStyle style））
- `void Box(Rect position, string text)`
  （void Box（Rect position, string text））
- `void Box(Rect position, GUIContent content, GUIStyle style)`
  （void Box（Rect position, GUIContent content, GUIStyle style））
- `bool Button(Rect position, string text)`
  （bool 按钮（Rect position, string text））
- `bool Button(Rect position, GUIContent content, GUIStyle style)`
  （bool 按钮（Rect position, GUIContent content, GUIStyle style））
- `bool Button(Rect position, int id, GUIContent content, GUIStyle style)`
  （bool 按钮（Rect position, int id, GUIContent content, GUIStyle style））
- `bool Toggle(Rect position, bool value, GUIContent content, GUIStyle style)`
  （bool 开关（Rect position, bool value, GUIContent content, GUIStyle style））
- `int Toolbar(Rect position, int selected, GUIContent[] contents, string[] controlNames, GUIStyle style, GUI.ToolbarButtonSize buttonSize, bool[] contentsEnabled)`
  （int Toolbar（Rect position, int selected, GUIContent[] contents, string[] controlNames, GUIStyle style, GUI.Toolbar按钮大小 buttonSize, bool[] contentsEnabled））
- `int SelectionGrid(Rect position, int selected, GUIContent[] contents, int xCount, GUIStyle style)`
  （int Selection网格（Rect position, int selected, GUIContent[] contents, int xCount, GUIStyle style））
- `void FindStyles(ref GUIStyle style, out GUIStyle firstStyle, out GUIStyle midStyle, out GUIStyle lastStyle, string first, string mid, string last)`
  （void 查找Styles（ref GUIStyle style, out GUIStyle firstStyle, out GUIStyle midStyle, out GUIStyle lastStyle, string first, string mid, string last））
- `int CalcTotalHorizSpacing(int xCount, GUIStyle style, GUIStyle firstStyle, GUIStyle midStyle, GUIStyle lastStyle)`
  （int CalcTotalHorizSpacing（int xCount, GUIStyle style, GUIStyle firstStyle, GUIStyle midStyle, GUIStyle lastStyle））
- `bool DoControl(Rect position, int id, bool on, bool hover, GUIContent content, GUIStyle style)`
  （bool Do控制（Rect position, int id, bool on, bool hover, GUIContent content, GUIStyle style））
- `void DoLabel(Rect position, GUIContent content, GUIStyle style)`
  （void Do标签（Rect position, GUIContent content, GUIStyle style））
- `bool DoToggle(Rect position, int id, bool value, GUIContent content, GUIStyle style)`
  （bool Do开关（Rect position, int id, bool value, GUIContent content, GUIStyle style））
- `bool DoButton(Rect position, int id, GUIContent content, GUIStyle style)`
  （bool Do按钮（Rect position, int id, GUIContent content, GUIStyle style））
- `int DoButtonGrid(Rect position, int selected, GUIContent[] contents, string[] controlNames, int xCount, GUIStyle style, GUIStyle firstStyle, GUIStyle midStyle, GUIStyle lastStyle, GUI.ToolbarButtonSize buttonSize, bool[] contentsEnabled)`
  （int Do按钮网格（Rect position, int selected, GUIContent[] contents, string[] controlNames, int xCount, GUIStyle style, GUIStyle firstStyle, GUIStyle midStyle, GUIStyle lastStyle, GUI.Toolbar按钮大小 buttonSize, bool[] contentsEnabled））
- `Rect[] CalcMouseRects(Rect position, GUIContent[] contents, int xCount, float elemWidth, float elemHeight, GUIStyle style, GUIStyle firstStyle, GUIStyle midStyle, GUIStyle lastStyle, bool addBorders, GUI.ToolbarButtonSize buttonSize)`
  （Rect[] Calc鼠标Rects（Rect position, GUIContent[] contents, int xCount, float elemWidth, float elemHeight, GUIStyle style, GUIStyle firstStyle, GUIStyle midStyle, GUIStyle lastStyle, bool addBorders, GUI.Toolbar按钮大小 buttonSize））
- `void BeginGroup(Rect position, GUIContent content, GUIStyle style)`
  （void Begin组（Rect position, GUIContent content, GUIStyle style））
- `void BeginGroup(Rect position, GUIContent content, GUIStyle style, Vector2 scrollOffset)`
  （void Begin组（Rect position, GUIContent content, GUIStyle style, 二维向量 scrollOffset））
- `void EndGroup()`
  （void 结束组（））
- `GenericStack get_scrollViewStates()`
  （Generic栈 get_scroll视图States（））
- `void CallWindowDelegate(GUI.WindowFunction func, int id, int instanceID, GUISkin _skin, int forceRect, float width, float height, GUIStyle style)`
  （void CallWindow委托（GUI.WindowFunction func, int id, int instanceID, GUISkin _skin, int forceRect, float width, float height, GUIStyle style））
- `void get_color_Injected(out Color ret)`
  （void get_color_Injected（out Color ret））
- `void set_color_Injected(ref Color value)`
  （void set_color_Injected（ref Color value））

---

## GUI.Scope（GUI.瞄准镜）

**继承**: IDisposable（可释放接口）

### 字段 (1)

- `bool m_Disposed`（布尔值 m_已释放）(偏移: 0x8)

### 方法 (3)

- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `void Finalize()`
  （void 终结（））
- `void Dispose()`
  （void 释放（））

---

## GUI.ToolbarButtonSize（GUI.Toolbar按钮大小）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## GUI.WindowFunction（GUI.WindowFunction）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(int id)`
  （void Invoke（int id））
- `IAsyncResult BeginInvoke(int id, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（int id, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## GUIClip（GUI弹匣）

### 方法 (6)

- `Rect get_visibleRect()`
  （Rect get_visibleRect（））
- `void Internal_Push(Rect screenRect, Vector2 scrollOffset, Vector2 renderOffset, bool resetOffset)`
  （void Internal_Push（Rect screenRect, 二维向量 scrollOffset, 二维向量 renderOffset, bool resetOffset））
- `void Internal_Pop()`
  （void Internal_Pop（））
- `void Push(Rect screenRect, Vector2 scrollOffset, Vector2 renderOffset, bool resetOffset)`
  （void Push（Rect screenRect, 二维向量 scrollOffset, 二维向量 renderOffset, bool resetOffset））
- `void get_visibleRect_Injected(out Rect ret)`
  （void get_visibleRect_Injected（out Rect ret））
- `void Internal_Push_Injected(ref Rect screenRect, ref Vector2 scrollOffset, ref Vector2 renderOffset, bool resetOffset)`
  （void Internal_Push_Injected（ref Rect screenRect, ref Vector2 scrollOffset, ref Vector2 renderOffset, bool resetOffset））

---

## GUIContent（GUIContent）

### 字段 (7)

- `string m_Text`（string m_文本）(偏移: 0x8)
- `Texture m_Image`（纹理 m_图像）(偏移: 0xC)
- `string m_Tooltip`（string m_Tooltip）(偏移: 0x10)
- `GUIContent s_Text`（GUIContent s_文本）(偏移: 0x0)
- `GUIContent s_Image`（GUIContent s_图像）(偏移: 0x4)
- `GUIContent s_TextImage`（GUIContent s_文本图像）(偏移: 0x8)
- `GUIContent none`（GUIContent none）(偏移: 0xC)

### 方法 (8)

- `string get_text()`
  （字符串 获取_文本（））
- `void set_text(string value)`
  （void 设置_文本（字符串 value））
- `void set_image(Texture value)`
  （void set_image（纹理 value））
- `string get_tooltip()`
  （string get_tooltip（））
- `void set_tooltip(string value)`
  （void set_tooltip（string value））
- `GUIContent Temp(string t)`
  （GUIContent Temp（string t））
- `void ClearStaticCache()`
  （void 清除静态的缓存（））
- `GUIContent[] Temp(string[] texts)`
  （GUIContent[] Temp（string[] texts））

---

## GUIGridSizer（GUI网格Sizer）

**继承**: GUILayoutEntry（GUILayoutEntry）

### 字段 (6)

- `int m_Count`（int m_数量）(偏移: 0x38)
- `int m_XCount`（int m_X数量）(偏移: 0x3C)
- `float m_MinButtonWidth`（float m_最小按钮宽度）(偏移: 0x40)
- `float m_MaxButtonWidth`（float m_最大按钮宽度）(偏移: 0x44)
- `float m_MinButtonHeight`（float m_最小按钮高度）(偏移: 0x48)
- `float m_MaxButtonHeight`（float m_最大按钮高度）(偏移: 0x4C)

### 方法 (2)

- `Rect GetRect(GUIContent[] contents, int xCount, GUIStyle style, GUILayoutOption[] options)`
  （Rect 获取Rect（GUIContent[] contents, int xCount, GUIStyle style, GUILayoutOption[] options））
- `int get_rows()`
  （int get_rows（））

---

## GUILayout（GUILayout）

### 方法 (27)

- `void Label(string text, GUILayoutOption[] options)`
  （void 标签（string text, GUILayoutOption[] options））
- `void Label(string text, GUIStyle style, GUILayoutOption[] options)`
  （void 标签（string text, GUIStyle style, GUILayoutOption[] options））
- `void DoLabel(GUIContent content, GUIStyle style, GUILayoutOption[] options)`
  （void Do标签（GUIContent content, GUIStyle style, GUILayoutOption[] options））
- `bool Button(string text, GUILayoutOption[] options)`
  （bool 按钮（string text, GUILayoutOption[] options））
- `bool DoButton(GUIContent content, GUIStyle style, GUILayoutOption[] options)`
  （bool Do按钮（GUIContent content, GUIStyle style, GUILayoutOption[] options））
- `bool Toggle(bool value, string text, GUILayoutOption[] options)`
  （bool 开关（bool value, string text, GUILayoutOption[] options））
- `bool DoToggle(bool value, GUIContent content, GUIStyle style, GUILayoutOption[] options)`
  （bool Do开关（bool value, GUIContent content, GUIStyle style, GUILayoutOption[] options））
- `int Toolbar(int selected, string[] texts, GUILayoutOption[] options)`
  （int Toolbar（int selected, string[] texts, GUILayoutOption[] options））
- `int Toolbar(int selected, GUIContent[] contents, GUIStyle style, GUILayoutOption[] options)`
  （int Toolbar（int selected, GUIContent[] contents, GUIStyle style, GUILayoutOption[] options））
- `int Toolbar(int selected, GUIContent[] contents, GUIStyle style, GUI.ToolbarButtonSize buttonSize, GUILayoutOption[] options)`
  （int Toolbar（int selected, GUIContent[] contents, GUIStyle style, GUI.Toolbar按钮大小 buttonSize, GUILayoutOption[] options））
- `int Toolbar(int selected, GUIContent[] contents, bool[] enabled, GUIStyle style, GUI.ToolbarButtonSize buttonSize, GUILayoutOption[] options)`
  （int Toolbar（int selected, GUIContent[] contents, bool[] enabled, GUIStyle style, GUI.Toolbar按钮大小 buttonSize, GUILayoutOption[] options））
- `int SelectionGrid(int selected, string[] texts, int xCount, GUILayoutOption[] options)`
  （int Selection网格（int selected, string[] texts, int xCount, GUILayoutOption[] options））
- `int SelectionGrid(int selected, GUIContent[] contents, int xCount, GUIStyle style, GUILayoutOption[] options)`
  （int Selection网格（int selected, GUIContent[] contents, int xCount, GUIStyle style, GUILayoutOption[] options））
- `void Space(float pixels)`
  （void Space（float pixels））
- `void BeginHorizontal(GUILayoutOption[] options)`
  （void Begin水平（GUILayoutOption[] options））
- `void BeginHorizontal(GUIContent content, GUIStyle style, GUILayoutOption[] options)`
  （void Begin水平（GUIContent content, GUIStyle style, GUILayoutOption[] options））
- `void EndHorizontal()`
  （void 结束水平（））
- `void BeginVertical(GUILayoutOption[] options)`
  （void Begin垂直（GUILayoutOption[] options））
- `void BeginVertical(GUIStyle style, GUILayoutOption[] options)`
  （void Begin垂直（GUIStyle style, GUILayoutOption[] options））
- `void BeginVertical(GUIContent content, GUIStyle style, GUILayoutOption[] options)`
  （void Begin垂直（GUIContent content, GUIStyle style, GUILayoutOption[] options））
- `void EndVertical()`
  （void 结束垂直（））
- `void BeginArea(Rect screenRect)`
  （void BeginArea（Rect screenRect））
- `void BeginArea(Rect screenRect, GUIContent content, GUIStyle style)`
  （void BeginArea（Rect screenRect, GUIContent content, GUIStyle style））
- `void EndArea()`
  （void 结束Area（））
- `GUILayoutOption Width(float width)`
  （GUILayoutOption 宽度（float width））
- `GUILayoutOption MinWidth(float minWidth)`
  （GUILayoutOption 最小宽度（float minWidth））
- `GUILayoutOption Height(float height)`
  （GUILayoutOption 高度（float height））

---

## GUILayout.HorizontalScope（GUILayout.水平瞄准镜）

**继承**: GUI.Scope（GUI.瞄准镜）

### 方法 (1)

- `void CloseScope()`
  （void 关闭瞄准镜（））

---

## GUILayout.VerticalScope（GUILayout.垂直瞄准镜）

**继承**: GUI.Scope（GUI.瞄准镜）

### 方法 (1)

- `void CloseScope()`
  （void 关闭瞄准镜（））

---

## GUILayoutEntry（GUILayoutEntry）

### 字段 (11)

- `float minWidth`（float min宽度）(偏移: 0x8)
- `float maxWidth`（float max宽度）(偏移: 0xC)
- `float minHeight`（float min高度）(偏移: 0x10)
- `float maxHeight`（float max高度）(偏移: 0x14)
- `Rect rect`（Rect rect）(偏移: 0x18)
- `int stretchWidth`（int stretch宽度）(偏移: 0x28)
- `int stretchHeight`（int stretch高度）(偏移: 0x2C)
- `bool consideredForMargin`（bool consideredForMargin）(偏移: 0x30)
- `GUIStyle m_Style`（GUIStyle m_Style）(偏移: 0x34)
- `Rect kDummyRect`（Rect kDummyRect）(偏移: 0x0)
- `int indent`（int indent）(偏移: 0x10)

### 方法 (15)

- `GUIStyle get_style()`
  （GUIStyle get_style（））
- `void set_style(GUIStyle value)`
  （void set_style（GUIStyle value））
- `int get_marginLeft()`
  （int get_margin左（））
- `int get_marginRight()`
  （int get_margin右（））
- `int get_marginTop()`
  （int get_margin顶部（））
- `int get_marginBottom()`
  （int get_margin底部（））
- `int get_marginHorizontal()`
  （int get_margin水平（））
- `int get_marginVertical()`
  （int get_margin垂直（））
- `void CalcWidth()`
  （void Calc宽度（））
- `void CalcHeight()`
  （void Calc高度（））
- `void SetHorizontal(float x, float width)`
  （void 集合水平（float x, float width））
- `void SetVertical(float y, float height)`
  （void 集合垂直（float y, float height））
- `void ApplyStyleSettings(GUIStyle style)`
  （void 应用StyleSettings（GUIStyle style））
- `void ApplyOptions(GUILayoutOption[] options)`
  （void 应用Options（GUILayoutOption[] options））
- `string ToString()`
  （字符串 转字符串（））

---

## GUILayoutGroup（GUILayout组）

**继承**: GUILayoutEntry（GUILayoutEntry）

### 字段 (21)

- `List<GUILayoutEntry> entries`（List<GUILayoutEntry> entries）(偏移: 0x38)
- `bool isVertical`（bool is垂直）(偏移: 0x3C)
- `bool resetCoords`（bool resetCoords）(偏移: 0x3D)
- `float spacing`（float spacing）(偏移: 0x40)
- `bool sameSize`（bool same大小）(偏移: 0x44)
- `bool isWindow`（bool isWindow）(偏移: 0x45)
- `int windowID`（int windowID）(偏移: 0x48)
- `int m_Cursor`（int m_Cursor）(偏移: 0x4C)
- `int m_StretchableCountX`（int m_Stretchable数量X）(偏移: 0x50)
- `int m_StretchableCountY`（int m_Stretchable数量Y）(偏移: 0x54)
- `bool m_UserSpecifiedWidth`（bool m_UserSpecified宽度）(偏移: 0x58)
- `bool m_UserSpecifiedHeight`（bool m_UserSpecified高度）(偏移: 0x59)
- `float m_ChildMinWidth`（float m_子级最小宽度）(偏移: 0x5C)
- `float m_ChildMaxWidth`（float m_子级最大宽度）(偏移: 0x60)
- `float m_ChildMinHeight`（float m_子级最小高度）(偏移: 0x64)
- `float m_ChildMaxHeight`（float m_子级最大高度）(偏移: 0x68)
- `int m_MarginLeft`（int m_Margin左）(偏移: 0x6C)
- `int m_MarginRight`（int m_Margin右）(偏移: 0x70)
- `int m_MarginTop`（int m_Margin顶部）(偏移: 0x74)
- `int m_MarginBottom`（int m_Margin底部）(偏移: 0x78)
- `GUILayoutEntry none`（GUILayoutEntry none）(偏移: 0x0)

### 方法 (14)

- `int get_marginLeft()`
  （int get_margin左（））
- `int get_marginRight()`
  （int get_margin右（））
- `int get_marginTop()`
  （int get_margin顶部（））
- `int get_marginBottom()`
  （int get_margin底部（））
- `void ApplyOptions(GUILayoutOption[] options)`
  （void 应用Options（GUILayoutOption[] options））
- `void ApplyStyleSettings(GUIStyle style)`
  （void 应用StyleSettings（GUIStyle style））
- `void ResetCursor()`
  （void 重置Cursor（））
- `GUILayoutEntry GetNext()`
  （GUILayoutEntry 获取下一个（））
- `void Add(GUILayoutEntry e)`
  （void 添加（GUILayoutEntry e））
- `void CalcWidth()`
  （void Calc宽度（））
- `void SetHorizontal(float x, float width)`
  （void 集合水平（float x, float width））
- `void CalcHeight()`
  （void Calc高度（））
- `void SetVertical(float y, float height)`
  （void 集合垂直（float y, float height））
- `string ToString()`
  （字符串 转字符串（））

---

## GUILayoutOption（GUILayoutOption）

### 字段 (2)

- `GUILayoutOption.Type type`（GUILayoutOption.类型 type）(偏移: 0x8)
- `object value`（对象 value）(偏移: 0xC)

---

## GUILayoutOption.Type（GUILayoutOption.类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## GUILayoutUtility（GUILayout工具）

### 字段 (3)

- `GUILayoutUtility.LayoutCache current`（GUILayoutUtility.Layout缓存 current）(偏移: 0x8)
- `Rect kDummyRect`（Rect kDummyRect）(偏移: 0xC)
- `GUIStyle s_SpaceStyle`（GUIStyle s_SpaceStyle）(偏移: 0x1C)

### 方法 (20)

- `Rect Internal_GetWindowRect(int windowID)`
  （Rect Internal_获取WindowRect（int windowID））
- `void Internal_MoveWindow(int windowID, Rect r)`
  （void Internal_移动Window（int windowID, Rect r））
- `GUILayoutUtility.LayoutCache SelectIDList(int instanceID, bool isWindow)`
  （GUILayoutUtility.Layout缓存 选择ID列表（int instanceID, bool isWindow））
- `void Begin(int instanceID)`
  （void Begin（int instanceID））
- `void BeginWindow(int windowID, GUIStyle style, GUILayoutOption[] options)`
  （void BeginWindow（int windowID, GUIStyle style, GUILayoutOption[] options））
- `void Layout()`
  （void Layout（））
- `void LayoutFromEditorWindow()`
  （void LayoutFromEditorWindow（））
- `void LayoutFreeGroup(GUILayoutGroup toplevel)`
  （void LayoutFree组（GUILayout组 toplevel））
- `void LayoutSingleGroup(GUILayoutGroup i)`
  （void Layout单个组（GUILayout组 i））
- `GUILayoutGroup CreateGUILayoutGroupInstanceOfType(Type LayoutType)`
  （GUILayout组 创建GUILayout组实例Of类型（类型 LayoutType））
- `GUILayoutGroup BeginLayoutGroup(GUIStyle style, GUILayoutOption[] options, Type layoutType)`
  （GUILayout组 BeginLayout组（GUIStyle style, GUILayoutOption[] options, 类型 layoutType））
- `void EndLayoutGroup()`
  （void 结束Layout组（））
- `GUILayoutGroup BeginLayoutArea(GUIStyle style, Type layoutType)`
  （GUILayout组 BeginLayoutArea（GUIStyle style, 类型 layoutType））
- `Rect GetRect(GUIContent content, GUIStyle style, GUILayoutOption[] options)`
  （Rect 获取Rect（GUIContent content, GUIStyle style, GUILayoutOption[] options））
- `Rect DoGetRect(GUIContent content, GUIStyle style, GUILayoutOption[] options)`
  （Rect Do获取Rect（GUIContent content, GUIStyle style, GUILayoutOption[] options））
- `Rect GetRect(float width, float height, GUIStyle style, GUILayoutOption[] options)`
  （Rect 获取Rect（float width, float height, GUIStyle style, GUILayoutOption[] options））
- `Rect DoGetRect(float minWidth, float maxWidth, float minHeight, float maxHeight, GUIStyle style, GUILayoutOption[] options)`
  （Rect Do获取Rect（float minWidth, float maxWidth, float minHeight, float maxHeight, GUIStyle style, GUILayoutOption[] options））
- `GUIStyle get_spaceStyle()`
  （GUIStyle get_spaceStyle（））
- `void Internal_GetWindowRect_Injected(int windowID, out Rect ret)`
  （void Internal_获取WindowRect_Injected（int windowID, out Rect ret））
- `void Internal_MoveWindow_Injected(int windowID, ref Rect r)`
  （void Internal_移动Window_Injected（int windowID, ref Rect r））

---

## GUILayoutUtility.LayoutCache（GUILayoutUtility.Layout缓存）

### 字段 (3)

- `GUILayoutGroup topLevel`（GUILayout组 top等级）(偏移: 0xC)
- `GenericStack layoutGroups`（Generic栈 layoutGroups）(偏移: 0x10)
- `GUILayoutGroup windows`（GUILayout组 windows）(偏移: 0x14)

### 方法 (5)

- `int get_id()`
  （int get_id（））
- `void set_id(int value)`
  （void set_id（int value））
- `GUILayoutUtility.LayoutCacheState get_State()`
  （GUILayoutUtility.Layout缓存状态 get_状态（））
- `void CopyState(GUILayoutUtility.LayoutCacheState other)`
  （void 复制状态（GUILayoutUtility.Layout缓存状态 other））
- `void ResetCursor()`
  （void 重置Cursor（））

---

## GUILayoutUtility.LayoutCacheState（GUILayoutUtility.Layout缓存状态）

### 字段 (4)

- `int id`（整数 id）(偏移: 0x0)
- `GUILayoutGroup topLevel`（GUILayout组 top等级）(偏移: 0x4)
- `GenericStack layoutGroups`（Generic栈 layoutGroups）(偏移: 0x8)
- `GUILayoutGroup windows`（GUILayout组 windows）(偏移: 0xC)

---

## GUIScrollGroup（GUI滚动组）

**继承**: GUILayoutGroup（GUILayout组）

### 字段 (12)

- `float calcMinWidth`（float calc最小宽度）(偏移: 0x7C)
- `float calcMaxWidth`（float calc最大宽度）(偏移: 0x80)
- `float calcMinHeight`（float calc最小高度）(偏移: 0x84)
- `float calcMaxHeight`（float calc最大高度）(偏移: 0x88)
- `float clientWidth`（float client宽度）(偏移: 0x8C)
- `float clientHeight`（float client高度）(偏移: 0x90)
- `bool allowHorizontalScroll`（bool allow水平滚动）(偏移: 0x94)
- `bool allowVerticalScroll`（bool allow垂直滚动）(偏移: 0x0)
- `bool needsHorizontalScrollbar`（bool needs水平Scrollbar）(偏移: 0x0)
- `bool needsVerticalScrollbar`（bool needs垂直Scrollbar）(偏移: 0x0)
- `GUIStyle horizontalScrollbar`（GUIStyle horizontalScrollbar）(偏移: 0x0)
- `GUIStyle verticalScrollbar`（GUIStyle verticalScrollbar）(偏移: 0x9C)

### 方法 (4)

- `void CalcWidth()`
  （void Calc宽度（））
- `void SetHorizontal(float x, float width)`
  （void 集合水平（float x, float width））
- `void CalcHeight()`
  （void Calc高度（））
- `void SetVertical(float y, float height)`
  （void 集合垂直（float y, float height））

---

## GUISettings（GUISettings）

### 字段 (5)

- `bool m_DoubleClickSelectsWord`（bool m_DoubleClickSelectsWord）(偏移: 0x8)
- `bool m_TripleClickSelectsLine`（bool m_TripleClickSelectsLine）(偏移: 0x9)
- `Color m_CursorColor`（颜色 m_Cursor颜色）(偏移: 0xC)
- `float m_CursorFlashSpeed`（float m_CursorFlashSpeed）(偏移: 0x1C)
- `Color m_SelectionColor`（颜色 m_Selection颜色）(偏移: 0x20)

---

## GUISkin（GUISkin）

**继承**: ScriptableObject（脚本对象）

### 字段 (29)

- `Font m_Font`（Font m_Font）(偏移: 0xC)
- `GUIStyle m_box`（GUIStyle m_box）(偏移: 0x10)
- `GUIStyle m_button`（GUIStyle m_button）(偏移: 0x14)
- `GUIStyle m_toggle`（GUIStyle m_toggle）(偏移: 0x18)
- `GUIStyle m_label`（GUIStyle m_label）(偏移: 0x1C)
- `GUIStyle m_textField`（GUIStyle m_textField）(偏移: 0x20)
- `GUIStyle m_textArea`（GUIStyle m_textArea）(偏移: 0x24)
- `GUIStyle m_window`（GUIStyle m_window）(偏移: 0x28)
- `GUIStyle m_horizontalSlider`（GUIStyle m_horizontal滑块）(偏移: 0x2C)
- `GUIStyle m_horizontalSliderThumb`（GUIStyle m_horizontal滑块Thumb）(偏移: 0x30)
- `GUIStyle m_horizontalSliderThumbExtent`（GUIStyle m_horizontal滑块ThumbExtent）(偏移: 0x34)
- `GUIStyle m_verticalSlider`（GUIStyle m_vertical滑块）(偏移: 0x38)
- `GUIStyle m_verticalSliderThumb`（GUIStyle m_vertical滑块Thumb）(偏移: 0x3C)
- `GUIStyle m_verticalSliderThumbExtent`（GUIStyle m_vertical滑块ThumbExtent）(偏移: 0x40)
- `GUIStyle m_SliderMixed`（GUIStyle m_滑块Mixed）(偏移: 0x44)
- `GUIStyle m_horizontalScrollbar`（GUIStyle m_horizontalScrollbar）(偏移: 0x48)
- `GUIStyle m_horizontalScrollbarThumb`（GUIStyle m_horizontalScrollbarThumb）(偏移: 0x4C)
- `GUIStyle m_horizontalScrollbarLeftButton`（GUIStyle m_horizontalScrollbar左按钮）(偏移: 0x50)
- `GUIStyle m_horizontalScrollbarRightButton`（GUIStyle m_horizontalScrollbar右按钮）(偏移: 0x54)
- `GUIStyle m_verticalScrollbar`（GUIStyle m_verticalScrollbar）(偏移: 0x58)
- `GUIStyle m_verticalScrollbarThumb`（GUIStyle m_verticalScrollbarThumb）(偏移: 0x5C)
- `GUIStyle m_verticalScrollbarUpButton`（GUIStyle m_verticalScrollbar上按钮）(偏移: 0x60)
- `GUIStyle m_verticalScrollbarDownButton`（GUIStyle m_verticalScrollbar下按钮）(偏移: 0x64)
- `GUIStyle m_ScrollView`（GUIStyle m_滚动视图）(偏移: 0x68)
- `GUIStyle[] m_CustomStyles`（GUIStyle[] m_自定义的Styles）(偏移: 0x6C)
- `GUISettings m_Settings`（GUISettings m_Settings）(偏移: 0x70)
- `GUIStyle ms_Error`（GUIStyle ms_Error）(偏移: 0x0)
- `GUISkin.SkinChangedDelegate m_SkinChanged`（GUISkin.SkinChanged委托 m_SkinChanged）(偏移: 0x4)
- `GUISkin current`（GUISkin current）(偏移: 0x8)

### 方法 (60)

- `void OnEnable()`
  （void 启用时（））
- `void CleanupRoots()`
  （void 清理Roots（））
- `Font get_font()`
  （Font get_font（））
- `void set_font(Font value)`
  （void set_font（Font value））
- `GUIStyle get_box()`
  （GUIStyle get_box（））
- `void set_box(GUIStyle value)`
  （void set_box（GUIStyle value））
- `GUIStyle get_label()`
  （GUIStyle get_label（））
- `void set_label(GUIStyle value)`
  （void set_label（GUIStyle value））
- `GUIStyle get_textField()`
  （GUIStyle get_textField（））
- `void set_textField(GUIStyle value)`
  （void set_textField（GUIStyle value））
- `GUIStyle get_textArea()`
  （GUIStyle get_textArea（））
- `void set_textArea(GUIStyle value)`
  （void set_textArea（GUIStyle value））
- `GUIStyle get_button()`
  （GUIStyle get_button（））
- `void set_button(GUIStyle value)`
  （void set_button（GUIStyle value））
- `GUIStyle get_toggle()`
  （GUIStyle get_toggle（））
- `void set_toggle(GUIStyle value)`
  （void set_toggle（GUIStyle value））
- `GUIStyle get_window()`
  （GUIStyle get_window（））
- `void set_window(GUIStyle value)`
  （void set_window（GUIStyle value））
- `GUIStyle get_horizontalSlider()`
  （GUIStyle get_horizontal滑块（））
- `void set_horizontalSlider(GUIStyle value)`
  （void set_horizontal滑块（GUIStyle value））
- `GUIStyle get_horizontalSliderThumb()`
  （GUIStyle get_horizontal滑块Thumb（））
- `void set_horizontalSliderThumb(GUIStyle value)`
  （void set_horizontal滑块Thumb（GUIStyle value））
- `GUIStyle get_horizontalSliderThumbExtent()`
  （GUIStyle get_horizontal滑块ThumbExtent（））
- `void set_horizontalSliderThumbExtent(GUIStyle value)`
  （void set_horizontal滑块ThumbExtent（GUIStyle value））
- `GUIStyle get_sliderMixed()`
  （GUIStyle get_sliderMixed（））
- `void set_sliderMixed(GUIStyle value)`
  （void set_sliderMixed（GUIStyle value））
- `GUIStyle get_verticalSlider()`
  （GUIStyle get_vertical滑块（））
- `void set_verticalSlider(GUIStyle value)`
  （void set_vertical滑块（GUIStyle value））
- `GUIStyle get_verticalSliderThumb()`
  （GUIStyle get_vertical滑块Thumb（））
- `void set_verticalSliderThumb(GUIStyle value)`
  （void set_vertical滑块Thumb（GUIStyle value））
- `GUIStyle get_verticalSliderThumbExtent()`
  （GUIStyle get_vertical滑块ThumbExtent（））
- `void set_verticalSliderThumbExtent(GUIStyle value)`
  （void set_vertical滑块ThumbExtent（GUIStyle value））
- `GUIStyle get_horizontalScrollbar()`
  （GUIStyle get_horizontalScrollbar（））
- `void set_horizontalScrollbar(GUIStyle value)`
  （void set_horizontalScrollbar（GUIStyle value））
- `GUIStyle get_horizontalScrollbarThumb()`
  （GUIStyle get_horizontalScrollbarThumb（））
- `void set_horizontalScrollbarThumb(GUIStyle value)`
  （void set_horizontalScrollbarThumb（GUIStyle value））
- `GUIStyle get_horizontalScrollbarLeftButton()`
  （GUIStyle get_horizontalScrollbar左按钮（））
- `void set_horizontalScrollbarLeftButton(GUIStyle value)`
  （void set_horizontalScrollbar左按钮（GUIStyle value））
- `GUIStyle get_horizontalScrollbarRightButton()`
  （GUIStyle get_horizontalScrollbar右按钮（））
- `void set_horizontalScrollbarRightButton(GUIStyle value)`
  （void set_horizontalScrollbar右按钮（GUIStyle value））
- `GUIStyle get_verticalScrollbar()`
  （GUIStyle get_verticalScrollbar（））
- `void set_verticalScrollbar(GUIStyle value)`
  （void set_verticalScrollbar（GUIStyle value））
- `GUIStyle get_verticalScrollbarThumb()`
  （GUIStyle get_verticalScrollbarThumb（））
- `void set_verticalScrollbarThumb(GUIStyle value)`
  （void set_verticalScrollbarThumb（GUIStyle value））
- `GUIStyle get_verticalScrollbarUpButton()`
  （GUIStyle get_verticalScrollbar上按钮（））
- `void set_verticalScrollbarUpButton(GUIStyle value)`
  （void set_verticalScrollbar上按钮（GUIStyle value））
- `GUIStyle get_verticalScrollbarDownButton()`
  （GUIStyle get_verticalScrollbar下按钮（））
- `void set_verticalScrollbarDownButton(GUIStyle value)`
  （void set_verticalScrollbar下按钮（GUIStyle value））
- `GUIStyle get_scrollView()`
  （GUIStyle get_scroll视图（））
- `void set_scrollView(GUIStyle value)`
  （void set_scroll视图（GUIStyle value））
- `GUIStyle[] get_customStyles()`
  （GUIStyle[] get_customStyles（））
- `void set_customStyles(GUIStyle[] value)`
  （void set_customStyles（GUIStyle[] value））
- `GUISettings get_settings()`
  （GUISettings get_settings（））
- `GUIStyle get_error()`
  （GUIStyle get_error（））
- `void Apply()`
  （void 应用（））
- `void BuildStyleCache()`
  （void BuildStyle缓存（））
- `GUIStyle GetStyle(string styleName)`
  （GUIStyle 获取Style（string styleName））
- `GUIStyle FindStyle(string styleName)`
  （GUIStyle 查找Style（string styleName））
- `void MakeCurrent()`
  （void Make当前（））
- `IEnumerator GetEnumerator()`
  （IEnumerator 获取枚举器（））

---

## GUISkin.SkinChangedDelegate（GUISkin.SkinChanged委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke()`
  （void 调用（））
- `IAsyncResult BeginInvoke(AsyncCallback callback, object object)`
  （I异步结果 开始调用（异步回调 callback, 对象 object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## GUIStyle（GUIStyle）

### 字段 (16)

- `IntPtr m_Ptr`（整数指针 m_指针）(偏移: 0x8)
- `GUIStyleState m_Normal`（GUIStyle状态 m_法线）(偏移: 0xC)
- `GUIStyleState m_Hover`（GUIStyle状态 m_悬停）(偏移: 0x10)
- `GUIStyleState m_Active`（GUIStyle状态 m_激活的）(偏移: 0x14)
- `GUIStyleState m_Focused`（GUIStyle状态 m_聚焦的）(偏移: 0x18)
- `GUIStyleState m_OnNormal`（GUIStyle状态 m_On法线）(偏移: 0x1C)
- `GUIStyleState m_OnHover`（GUIStyle状态 m_On悬停）(偏移: 0x20)
- `GUIStyleState m_OnActive`（GUIStyle状态 m_On激活的）(偏移: 0x24)
- `GUIStyleState m_OnFocused`（GUIStyle状态 m_On聚焦的）(偏移: 0x28)
- `RectOffset m_Border`（RectOffset m_Border）(偏移: 0x2C)
- `RectOffset m_Padding`（RectOffset m_Padding）(偏移: 0x30)
- `RectOffset m_Margin`（RectOffset m_Margin）(偏移: 0x34)
- `RectOffset m_Overflow`（RectOffset m_Overflow）(偏移: 0x38)
- `string m_Name`（字符串 m_名称）(偏移: 0x3C)
- `bool showKeyboardFocus`（bool show键盘聚焦）(偏移: 0x0)
- `GUIStyle s_None`（GUIStyle s_无）(偏移: 0x4)

### 方法 (52)

- `string get_rawName()`
  （string get_raw名称（））
- `void set_rawName(string value)`
  （void set_raw名称（string value））
- `void set_font(Font value)`
  （void set_font（Font value））
- `ImagePosition get_imagePosition()`
  （图像Position get_imagePosition（））
- `void set_alignment(TextAnchor value)`
  （void set_alignment（文本Anchor value））
- `bool get_wordWrap()`
  （bool get_wordWrap（））
- `float get_fixedWidth()`
  （float get_fixed宽度（））
- `float get_fixedHeight()`
  （float get_fixed高度（））
- `bool get_stretchWidth()`
  （bool get_stretch宽度（））
- `void set_stretchWidth(bool value)`
  （void set_stretch宽度（bool value））
- `bool get_stretchHeight()`
  （bool get_stretch高度（））
- `void set_stretchHeight(bool value)`
  （void set_stretch高度（bool value））
- `void set_fontSize(int value)`
  （void set_font大小（int value））
- `IntPtr Internal_Create(GUIStyle self)`
  （整数Ptr Internal_创建（GUIStyle self））
- `IntPtr Internal_Copy(GUIStyle self, GUIStyle other)`
  （整数Ptr Internal_复制（GUIStyle self, GUIStyle other））
- `void Internal_Destroy(IntPtr self)`
  （void Internal_销毁（整数Ptr self））
- `IntPtr GetStyleStatePtr(int idx)`
  （整数Ptr 获取Style状态Ptr（int idx））
- `IntPtr GetRectOffsetPtr(int idx)`
  （整数Ptr 获取RectOffsetPtr（int idx））
- `void AssignRectOffset(int idx, IntPtr srcRectOffset)`
  （void AssignRectOffset（int idx, 整数Ptr srcRectOffset））
- `void Internal_Draw(Rect screenRect, GUIContent content, bool isHover, bool isActive, bool on, bool hasKeyboardFocus)`
  （void Internal_Draw（Rect screenRect, GUIContent content, bool isHover, bool isActive, bool on, bool hasKeyboardFocus））
- `void Internal_Draw2(Rect position, GUIContent content, int controlID, bool on)`
  （void Internal_Draw2（Rect position, GUIContent content, int controlID, bool on））
- `Vector2 Internal_CalcSize(GUIContent content)`
  （二维向量 Internal_Calc大小（GUIContent content））
- `Vector2 Internal_CalcSizeWithConstraints(GUIContent content, Vector2 maxSize)`
  （二维向量 Internal_Calc大小WithConstraints（GUIContent content, 二维向量 maxSize））
- `float Internal_CalcHeight(GUIContent content, float width)`
  （float Internal_Calc高度（GUIContent content, float width））
- `Vector2 Internal_CalcMinMaxWidth(GUIContent content)`
  （二维向量 Internal_Calc最小最大宽度（GUIContent content））
- `void SetMouseTooltip(string tooltip, Rect screenRect)`
  （void 集合鼠标Tooltip（string tooltip, Rect screenRect））
- `bool IsTooltipActive(string tooltip)`
  （bool 是否Tooltip激活的（string tooltip））
- `void SetDefaultFont(Font font)`
  （void 集合默认的Font（Font font））
- `void Finalize()`
  （void 终结（））
- `string get_name()`
  （字符串 获取_名称（））
- `void set_name(string value)`
  （void 设置_名称（字符串 value））
- `GUIStyleState get_normal()`
  （GUIStyle状态 get_normal（））
- `RectOffset get_margin()`
  （RectOffset get_margin（））
- `RectOffset get_padding()`
  （RectOffset get_padding（））
- `void set_padding(RectOffset value)`
  （void set_padding（RectOffset value））
- `void Draw(Rect position, GUIContent content, bool isHover, bool isActive, bool on, bool hasKeyboardFocus)`
  （void Draw（Rect position, GUIContent content, bool isHover, bool isActive, bool on, bool hasKeyboardFocus））
- `void Draw(Rect position, GUIContent content, int controlID)`
  （void Draw（Rect position, GUIContent content, int controlID））
- `void Draw(Rect position, GUIContent content, int controlID, bool on, bool hover)`
  （void Draw（Rect position, GUIContent content, int controlID, bool on, bool hover））
- `void Draw(Rect position, GUIContent content, int controlId, bool isHover, bool isActive, bool on, bool hasKeyboardFocus)`
  （void Draw（Rect position, GUIContent content, int controlId, bool isHover, bool isActive, bool on, bool hasKeyboardFocus））
- `GUIStyle get_none()`
  （GUIStyle get_none（））
- `Vector2 CalcSize(GUIContent content)`
  （二维向量 Calc大小（GUIContent content））
- `Vector2 CalcSizeWithConstraints(GUIContent content, Vector2 constraints)`
  （二维向量 Calc大小WithConstraints（GUIContent content, 二维向量 constraints））
- `float CalcHeight(GUIContent content, float width)`
  （float Calc高度（GUIContent content, float width））
- `bool get_isHeightDependantOnWidth()`
  （bool get_is高度DependantOn宽度（））
- `void CalcMinMaxWidth(GUIContent content, out float minWidth, out float maxWidth)`
  （void Calc最小最大宽度（GUIContent content, out float minWidth, out float maxWidth））
- `string ToString()`
  （字符串 转字符串（））
- `void Internal_Draw_Injected(ref Rect screenRect, GUIContent content, bool isHover, bool isActive, bool on, bool hasKeyboardFocus)`
  （void Internal_Draw_Injected（ref Rect screenRect, GUIContent content, bool isHover, bool isActive, bool on, bool hasKeyboardFocus））
- `void Internal_Draw2_Injected(ref Rect position, GUIContent content, int controlID, bool on)`
  （void Internal_Draw2_Injected（ref Rect position, GUIContent content, int controlID, bool on））
- `void Internal_CalcSize_Injected(GUIContent content, out Vector2 ret)`
  （void Internal_CalcSize_Injected（GUIContent content, out Vector2 ret））
- `void Internal_CalcSizeWithConstraints_Injected(GUIContent content, ref Vector2 maxSize, out Vector2 ret)`
  （void Internal_Calc大小WithConstraints_Injected（GUIContent content, ref Vector2 maxSize, out Vector2 ret））
- `void Internal_CalcMinMaxWidth_Injected(GUIContent content, out Vector2 ret)`
  （void Internal_Calc最小最大Width_Injected（GUIContent content, out Vector2 ret））
- `void SetMouseTooltip_Injected(string tooltip, ref Rect screenRect)`
  （void 集合鼠标Tooltip_Injected（string tooltip, ref Rect screenRect））

---

## GUIStyleState（GUIStyle状态）

### 字段 (2)

- `IntPtr m_Ptr`（整数指针 m_指针）(偏移: 0x8)
- `GUIStyle m_SourceStyle`（GUIStyle m_SourceStyle）(偏移: 0xC)

### 方法 (6)

- `void set_textColor(Color value)`
  （void set_text颜色（颜色 value））
- `IntPtr Init()`
  （整数Ptr 初始化（））
- `void Cleanup()`
  （void 清理（））
- `GUIStyleState GetGUIStyleState(GUIStyle sourceStyle, IntPtr source)`
  （GUIStyle状态 获取GUIStyle状态（GUIStyle sourceStyle, 整数Ptr source））
- `void Finalize()`
  （void 终结（））
- `void set_textColor_Injected(ref Color value)`
  （void set_textColor_Injected（ref Color value））

---

## GUITargetAttribute（GUI目标Attribute）

**继承**: Attribute（属性）

### 字段 (1)

- `int displayMask`（int display掩码）(偏移: 0x8)

### 方法 (1)

- `int GetGUITargetAttrValue(Type klass, string methodName)`
  （int 获取GUI目标Attr值（类型 klass, string methodName））

---

## GUIUtility（GUI工具）

### 字段 (6)

- `int s_SkinMode`（int s_Skin模式）(偏移: 0x0)
- `int s_OriginalID`（int s_OriginalID）(偏移: 0x4)
- `Action takeCapture`（动作 takeCapture）(偏移: 0x8)
- `Action releaseCapture`（动作 releaseCapture）(偏移: 0xC)
- `Action guiChanged`（动作 guiChanged）(偏移: 0x18)
- `Func<bool> s_HasCurrentWindowKeyFocusFunc`（Func<bool> s_是否有当前Window键聚焦Func）(偏移: 0x20)

### 方法 (38)

- `float get_pixelsPerPoint()`
  （float get_pixelsPerPoint（））
- `int get_guiDepth()`
  （int get_gui深度（））
- `void set_mouseUsed(bool value)`
  （void set_mouseUsed（bool value））
- `string get_systemCopyBuffer()`
  （string get_system复制缓冲区（））
- `void set_systemCopyBuffer(string value)`
  （void set_system复制缓冲区（string value））
- `int GetControlID(int hint, FocusType focusType, Rect rect)`
  （int 获取控制ID（int hint, 聚焦类型 focusType, Rect rect））
- `Rect AlignRectToDevice(Rect rect, out int widthInPixels, out int heightInPixels)`
  （Rect AlignRectToDevice（Rect rect, out int widthInPixels, out int heightInPixels））
- `int Internal_GetHotControl()`
  （int Internal_获取Hot控制（））
- `int Internal_GetKeyboardControl()`
  （int Internal_获取键盘控制（））
- `void Internal_SetHotControl(int value)`
  （void Internal_集合Hot控制（int value））
- `object Internal_GetDefaultSkin(int skinMode)`
  （object Internal_获取默认的Skin（int skinMode））
- `void Internal_ExitGUI()`
  （void Internal_ExitGUI（））
- `void MarkGUIChanged()`
  （void MarkGUIChanged（））
- `int GetControlID(int hint, FocusType focus)`
  （int 获取控制ID（int hint, 聚焦类型 focus））
- `bool get_guiIsExiting()`
  （bool get_gui是否Exiting（））
- `void set_guiIsExiting(bool value)`
  （void set_gui是否Exiting（bool value））
- `int get_hotControl()`
  （int get_hot控制（））
- `void set_hotControl(int value)`
  （void set_hot控制（int value））
- `void TakeCapture()`
  （void TakeCapture（））
- `void RemoveCapture()`
  （void 移除Capture（））
- `int get_keyboardControl()`
  （int get_keyboard控制（））
- `bool HasKeyFocus(int controlID)`
  （bool 是否有键聚焦（int controlID））
- `GUISkin GetDefaultSkin()`
  （GUISkin 获取默认的Skin（））
- `void ProcessEvent(int instanceID, IntPtr nativeEventPtr, out bool result)`
  （void 处理事件（int instanceID, 整数Ptr nativeEventPtr, out bool result））
- `void BeginGUI(int skinMode, int instanceID, int useGUILayout)`
  （void BeginGUI（int skinMode, int instanceID, int useGUILayout））
- `void EndGUI(int layoutType)`
  （void 结束GUI（int layoutType））
- `bool EndGUIFromException(Exception exception)`
  （bool 结束GUIFromException（Exception exception））
- `bool EndContainerGUIFromException(Exception exception)`
  （bool 结束容器GUIFromException（Exception exception））
- `void ResetGlobalState()`
  （void 重置全局的状态（））
- `bool IsExitGUIException(Exception exception)`
  （bool 是否ExitGUIException（Exception exception））
- `bool ShouldRethrowException(Exception exception)`
  （bool 应该RethrowException（Exception exception））
- `void CheckOnGUI()`
  （void 检查OnGUI（））
- `Rect AlignRectToDevice(Rect rect)`
  （Rect AlignRectToDevice（Rect rect））
- `bool HitTest(Rect rect, Vector2 point, int offset)`
  （bool 命中Test（Rect rect, 二维向量 point, int offset））
- `bool HitTest(Rect rect, Vector2 point, bool isDirectManipulationDevice)`
  （bool 命中Test（Rect rect, 二维向量 point, bool isDirectManipulationDevice））
- `bool HitTest(Rect rect, Event evt)`
  （bool 命中Test（Rect rect, 事件 evt））
- `int GetControlID_Injected(int hint, FocusType focusType, ref Rect rect)`
  （int 获取控制ID_Injected（int hint, 聚焦类型 focusType, ref Rect rect））
- `void AlignRectToDevice_Injected(ref Rect rect, out int widthInPixels, out int heightInPixels, out Rect ret)`
  （void AlignRectToDevice_Injected（ref Rect rect, out int widthInPixels, out int heightInPixels, out Rect ret））

---

## GUIWordWrapSizer（GUIWordWrapSizer）

**继承**: GUILayoutEntry（GUILayoutEntry）

### 字段 (3)

- `GUIContent m_Content`（GUIContent m_Content）(偏移: 0x38)
- `float m_ForcedMinHeight`（float m_Forced最小高度）(偏移: 0x3C)
- `float m_ForcedMaxHeight`（float m_Forced最大高度）(偏移: 0x40)

### 方法 (2)

- `void CalcWidth()`
  （void Calc宽度（））
- `void CalcHeight()`
  （void Calc高度（））

---

## GZipStream（GZip流）

**继承**: Stream（流）

### 字段 (9)

- `Nullable<DateTime> LastModified`（Nullable<DateTime> 最后一个Modified）(偏移: 0x18)
- `int _headerByteCount`（int _headerByte数量）(偏移: 0x28)
- `ZlibBaseStream _baseStream`（Zlib基础流 _base流）(偏移: 0x2C)
- `bool _disposed`（布尔值 _已释放）(偏移: 0x30)
- `bool _firstReadDone`（bool _firstReadDone）(偏移: 0x31)
- `string _FileName`（string _文件名称）(偏移: 0x34)
- `string _Comment`（string _Comment）(偏移: 0x38)
- `DateTime _unixEpoch`（Date时间 _unixEpoch）(偏移: 0x0)
- `Encoding iso8859dash1`（Encoding iso8859dash1）(偏移: 0x8)

### 方法 (16)

- `string get_Comment()`
  （string get_Comment（））
- `void set_Comment(string value)`
  （void set_Comment（string value））
- `string get_FileName()`
  （string get_文件名称（））
- `void set_FileName(string value)`
  （void set_文件名称（string value））
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
- `int EmitHeader()`
  （int Emit标题（））

---

## GameAsset（游戏资产）

**继承**: ScriptableObject（脚本对象）

### 字段 (3)

- `Texture2D[] levelIcon_Small`（Texture2D[] levelIcon_Small）(偏移: 0xC)
- `Texture2D[] vipIcon`（Texture2D[] vip图标）(偏移: 0x10)
- `Vector2[] animSpeedData`（Vector2[] animSpeed数据）(偏移: 0x14)

### 方法 (1)

- `float GetAnimSpeed(float input)`
  （float 获取动画Speed（float input））

---

## GameManager（游戏管理器）

**继承**: Singleton<GameManager>（Singleton<游戏Manager>）

### 字段 (38)

- `GameObject playerPrefab`（游戏对象 player预制体）(偏移: 0xC)
- `GameObject botPrefab`（游戏对象 bot预制体）(偏移: 0x10)
- `Player myPlayer`（玩家 my玩家）(偏移: 0x0)
- `GameMode gameMode`（游戏模式 game模式）(偏移: 0x4)
- `WeaponLimited weaponLimited`（Weapon限制 weapon限制）(偏移: 0x8)
- `bool revengeEnable`（bool revenge启用）(偏移: 0xC)
- `GameObject gameModePrefab`（游戏对象 game模式预制体）(偏移: 0x10)
- `List<Entity> entityBL_Alive`（List<Entity> entityBL_Alive）(偏移: 0x14)
- `List<Entity> entityGR_Alive`（List<Entity> entityGR_Alive）(偏移: 0x18)
- `Player[] allPlayers`（Player[] allPlayers）(偏移: 0x1C)
- `List<Player> playersBL`（List<Player> playersBL）(偏移: 0x20)
- `List<Player> playersBL_Alive`（List<Player> playersBL_Alive）(偏移: 0x24)
- `List<Player> playersGR`（List<Player> playersGR）(偏移: 0x28)
- `List<Player> playersGR_Alive`（List<Player> playersGR_Alive）(偏移: 0x2C)
- `WeaponAsset weaponAsset`（武器资产 weapon资产）(偏移: 0x30)
- `CharacterAsset characterAsset`（角色资产 character资产）(偏移: 0x34)
- `NameKeyPool characterPool`（名称键池 character池）(偏移: 0x38)
- `NameKeyPool weaponPool`（名称键池 weapon池）(偏移: 0x3C)
- `GameManager.DamageEvent DamageEvent_InvalidCheck_Observers`（游戏Manager.伤害事件 伤害Event_InvalidCheck_Observers）(偏移: 0x24)
- `GameManager.DamageEvent DamageEvent_PreCal_Observers`（游戏Manager.伤害事件 伤害Event_PreCal_Observers）(偏移: 0x28)
- `GameManager.DamageEvent DamageEvent_PostCal_Observers`（游戏Manager.伤害事件 伤害Event_PostCal_Observers）(偏移: 0x2C)
- `GameManager.DamageEvent DamageEvent_Post_Observers`（游戏Manager.伤害事件 伤害Event_Post_Observers）(偏移: 0x30)
- `GameManager.DeathEvent DeathEvent_Observers`（游戏Manager.死亡事件 死亡Event_Observers）(偏移: 0x34)
- `GameManager.DeathEvent DeathEvent_ForGameRule`（游戏Manager.死亡事件 死亡Event_For游戏Rule）(偏移: 0x38)
- `GameManager.SpecialKillChecker firstAndLastKillChecker`（游戏Manager.特殊击杀Checker firstAnd最后一个击杀Checker）(偏移: 0x3C)
- `Action<Player> NewPlayerJoinEvent_Observers`（Action<Player> 新的玩家JoinEvent_Observers）(偏移: 0x40)
- `Action<Player> PlayerSpawnEvent_Observers`（Action<Player> 玩家出生Event_Observers）(偏移: 0x44)
- `Action<Player> MyPlayerJoinEvent_Observers`（Action<Player> My玩家JoinEvent_Observers）(偏移: 0x48)
- `Action<Player> MyPlayerSpawnEvent_Observers`（Action<Player> My玩家出生Event_Observers）(偏移: 0x4C)
- `GameManager.DamageEvent MyPlayerCasueDamageEvent_Observers`（游戏Manager.伤害事件 My玩家Casue伤害Event_Observers）(偏移: 0x50)
- `GameManager.DamageEvent MyPlayerGetDamageEvent_Observers`（游戏Manager.伤害事件 My玩家获取伤害Event_Observers）(偏移: 0x54)
- `GameManager.DeathEvent MyPlayerKillEvent_Observers`（游戏Manager.死亡事件 My玩家击杀Event_Observers）(偏移: 0x58)
- `GameManager.DeathEvent MyPlayerDeathEvent_Observers`（游戏Manager.死亡事件 My玩家死亡Event_Observers）(偏移: 0x5C)
- `Action NewGameRoundStart_Observer`（动作 新的游戏回合Start_观察者）(偏移: 0x60)
- `Action<Weapon> GetGrenadeFromBag_Observer`（Action<Weapon> 获取手雷FromBag_观察者）(偏移: 0x64)
- `List<RecyclableObject> recyclableObjects`（List<RecyclableObject> recyclableObjects）(偏移: 0x40)
- `float dropWpnRecycleTime`（float drop武器Recycle时间）(偏移: 0x68)
- `int playerCameraChanger`（int player摄像机Changer）(偏移: 0x44)

### 方法 (56)

- `Team get_myJoinTeam()`
  （队伍 get_myJoin队伍（））
- `bool get_isNanoMode()`
  （bool get_is纳米模式（））
- `int get_playerCount_BL()`
  （int get_playerCount_BL（））
- `int get_alivePlayerCount_BL()`
  （int get_alive玩家Count_BL（））
- `int get_playerCount_GR()`
  （int get_playerCount_GR（））
- `int get_alivePlayerCount_GR()`
  （int get_alive玩家Count_GR（））
- `Player get_ace()`
  （玩家 get_ace（））
- `void set_ace(Player value)`
  （void set_ace（玩家 value））
- `bool get_gameRoundOver()`
  （bool get_game回合Over（））
- `void set_gameRoundOver(bool value)`
  （void set_game回合Over（bool value））
- `void add_DamageEvent_InvalidCheck_Observers(GameManager.DamageEvent value)`
  （void add_伤害Event_InvalidCheck_Observers（游戏Manager.伤害事件 value））
- `void remove_DamageEvent_InvalidCheck_Observers(GameManager.DamageEvent value)`
  （void remove_伤害Event_InvalidCheck_Observers（游戏Manager.伤害事件 value））
- `void add_DamageEvent_PreCal_Observers(GameManager.DamageEvent value)`
  （void add_伤害Event_PreCal_Observers（游戏Manager.伤害事件 value））
- `void remove_DamageEvent_PreCal_Observers(GameManager.DamageEvent value)`
  （void remove_伤害Event_PreCal_Observers（游戏Manager.伤害事件 value））
- `void add_DamageEvent_PostCal_Observers(GameManager.DamageEvent value)`
  （void add_伤害Event_PostCal_Observers（游戏Manager.伤害事件 value））
- `void remove_DamageEvent_PostCal_Observers(GameManager.DamageEvent value)`
  （void remove_伤害Event_PostCal_Observers（游戏Manager.伤害事件 value））
- `void add_NewPlayerJoinEvent_Observers(Action<Player> value)`
  （void add_新的玩家JoinEvent_Observers（Action<Player> value））
- `void remove_NewPlayerJoinEvent_Observers(Action<Player> value)`
  （void remove_新的玩家JoinEvent_Observers（Action<Player> value））
- `void add_MyPlayerJoinEvent_Observers(Action<Player> value)`
  （void add_My玩家JoinEvent_Observers（Action<Player> value））
- `void remove_MyPlayerJoinEvent_Observers(Action<Player> value)`
  （void remove_My玩家JoinEvent_Observers（Action<Player> value））
- `void add_MyPlayerCasueDamageEvent_Observers(GameManager.DamageEvent value)`
  （void add_My玩家Casue伤害Event_Observers（游戏Manager.伤害事件 value））
- `void remove_MyPlayerCasueDamageEvent_Observers(GameManager.DamageEvent value)`
  （void remove_My玩家Casue伤害Event_Observers（游戏Manager.伤害事件 value））
- `void add_MyPlayerGetDamageEvent_Observers(GameManager.DamageEvent value)`
  （void add_My玩家获取伤害Event_Observers（游戏Manager.伤害事件 value））
- `void remove_MyPlayerGetDamageEvent_Observers(GameManager.DamageEvent value)`
  （void remove_My玩家获取伤害Event_Observers（游戏Manager.伤害事件 value））
- `void add_MyPlayerKillEvent_Observers(GameManager.DeathEvent value)`
  （void add_My玩家击杀Event_Observers（游戏Manager.死亡事件 value））
- `void remove_MyPlayerKillEvent_Observers(GameManager.DeathEvent value)`
  （void remove_My玩家击杀Event_Observers（游戏Manager.死亡事件 value））
- `void add_MyPlayerDeathEvent_Observers(GameManager.DeathEvent value)`
  （void add_My玩家死亡Event_Observers（游戏Manager.死亡事件 value））
- `void remove_MyPlayerDeathEvent_Observers(GameManager.DeathEvent value)`
  （void remove_My玩家死亡Event_Observers（游戏Manager.死亡事件 value））
- `void add_GetGrenadeFromBag_Observer(Action<Weapon> value)`
  （void add_获取手雷FromBag_观察者（Action<Weapon> value））
- `void remove_GetGrenadeFromBag_Observer(Action<Weapon> value)`
  （void remove_获取手雷FromBag_观察者（Action<Weapon> value））
- `void Awake()`
  （void 唤醒（））
- `void Start()`
  （void 开始（））
- `void OnDestroy()`
  （void 销毁时（））
- `bool TryGetAce(Player player)`
  （bool Try获取王牌（玩家 player））
- `void ResetRound(float delay = 0)`
  （void 重置回合（float delay = 0））
- `IEnumerator RestRoundCoroutine(float delay)`
  （IEnumerator Rest回合协程（float delay））
- `void AddPlayers()`
  （void 添加Players（））
- `void Test()`
  （void Test（））
- `Player AddPlayer(bool isBot, Team team)`
  （玩家 添加玩家（bool isBot, 队伍 team））
- `int GetSparePlayerIndex()`
  （int 获取Spare玩家索引（））
- `void LoadWeapon(WeaponAsset asset)`
  （void 加载Weapon（武器资产 asset））
- `Weapon GiveWeapon(Player player, int weaponIndex, bool autoGiveUp, bool autoSelect)`
  （Weapon GiveWeapon（玩家 player, int weaponIndex, bool autoGiveUp, bool autoSelect））
- `Weapon GiveWeaponByBag(Player player, int weaponIndex)`
  （Weapon GiveWeaponBy背包（玩家 player, int weaponIndex））
- `Weapon GetWeapon(int weaponIndex)`
  （Weapon 获取Weapon（int weaponIndex））
- `bool GetWpnData(int weaponIndex, out WeaponData data)`
  （bool 获取武器数据（int weaponIndex, out WeaponData data））
- `string GetWpnName(int weaponIndex)`
  （string 获取武器名称（int weaponIndex））
- `void SetCharacter(Player player, string characterName)`
  （void 集合角色（玩家 player, string characterName））
- `CharacterModel GetCharacter(string characterName)`
  （角色模型 获取角色（string characterName））
- `void TakeDamage(DamageEventData data)`
  （void Take伤害（伤害事件数据 data））
- `void PlayHitFxAndSnd(Entity victim, Vector3 hitPos, DamageType dmgType, string hitSndName, string hitTag, string hitFX)`
  （void 播放命中特效AndSnd（实体 victim, 三维向量 hitPos, 伤害类型 dmgType, string hitSndName, string hitTag, string hitFX））
- `void DeathEventBroadcast(DeathEventData eventData)`
  （void 死亡事件Broadcast（死亡事件数据 eventData））
- `void ReturnLobby()`
  （void Return大厅（））
- `void GameRoundEnd()`
  （void 游戏回合结束（））
- `void AddRecyclableObject(RecyclableObject obj)`
  （void 添加Recyclable对象（Recyclable对象 obj））
- `void RemoveRecyclableObject(RecyclableObject obj)`
  （void 移除Recyclable对象（Recyclable对象 obj））
- `void ClearRecyclableObject()`
  （void 清除Recyclable对象（））

---

## GameManager.DamageEvent（游戏Manager.伤害事件）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(ref DamageEventData data)`
  （void Invoke（ref DamageEventData data））
- `IAsyncResult BeginInvoke(ref DamageEventData data, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（ref DamageEventData data, 异步回调 callback, object object））
- `void EndInvoke(ref DamageEventData data, IAsyncResult result)`
  （void 结束Invoke（ref DamageEventData data, I异步Result result））

---

## GameManager.DeathEvent（游戏Manager.死亡事件）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(DeathEventData data)`
  （void Invoke（死亡事件数据 data））
- `IAsyncResult BeginInvoke(DeathEventData data, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（死亡事件数据 data, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## GameManager.SpecialKillChecker（游戏Manager.特殊击杀Checker）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `SpecialKillType Invoke(Entity killer, Entity dead)`
  （特殊击杀类型 Invoke（实体 killer, 实体 dead））
- `IAsyncResult BeginInvoke(Entity killer, Entity dead, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（实体 killer, 实体 dead, 异步回调 callback, object object））
- `SpecialKillType EndInvoke(IAsyncResult result)`
  （特殊击杀类型 结束Invoke（I异步Result result））

---

## GameMode（游戏模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## GameModeExpand（游戏模式扩展）

### 方法 (4)

- `bool IsNanoMode(GameMode gameMode)`
  （bool 是否纳米模式（游戏模式 gameMode））
- `string ToChinese(GameMode gamemode)`
  （string ToChinese（游戏模式 gamemode））
- `bool IsMultiPlayerMode(GameMode gameMode)`
  （bool 是否多个玩家模式（游戏模式 gameMode））
- `bool IsTerminatorMode(GameMode gameMode)`
  （bool 是否Terminator模式（游戏模式 gameMode））

---

## GameObject（游戏对象）

**继承**: Object（对象）

### 方法 (23)

- `GameObject CreatePrimitive(PrimitiveType type)`
  （游戏对象 创建Primitive（Primitive类型 type））
- `Component GetComponent(Type type)`
  （组件 获取组件（类型 type））
- `void GetComponentFastPath(Type type, IntPtr oneFurtherThanResultValue)`
  （void 获取组件Fast路径（类型 type, 整数Ptr oneFurtherThanResultValue））
- `Component GetComponentInChildren(Type type, bool includeInactive)`
  （组件 获取组件InChildren（类型 type, bool includeInactive））
- `Component GetComponentInParent(Type type, bool includeInactive)`
  （组件 获取组件In父级（类型 type, bool includeInactive））
- `Component GetComponentInParent(Type type)`
  （组件 获取组件In父级（类型 type））
- `Array GetComponentsInternal(Type type, bool useSearchTypeAsArrayReturnType, bool recursive, bool includeInactive, bool reverse, object resultList)`
  （数组 获取Components内部的（类型 type, bool useSearchTypeAsArrayReturnType, bool recursive, bool includeInactive, bool reverse, object resultList））
- `void TryGetComponentFastPath(Type type, IntPtr oneFurtherThanResultValue)`
  （void Try获取组件Fast路径（类型 type, 整数Ptr oneFurtherThanResultValue））
- `Component Internal_AddComponentWithType(Type componentType)`
  （组件 Internal_添加组件With类型（类型 componentType））
- `Component AddComponent(Type componentType)`
  （组件 添加组件（类型 componentType））
- `Transform get_transform()`
  （变换 获取_transform（））
- `int get_layer()`
  （int get_layer（））
- `void set_layer(int value)`
  （void set_layer（int value））
- `void SetActive(bool value)`
  （void 集合激活的（bool value））
- `bool get_activeSelf()`
  （布尔值 获取_自身激活（））
- `bool get_activeInHierarchy()`
  （布尔值 获取_层级激活（））
- `bool get_isStaticBatchable()`
  （bool get_is静态的Batchable（））
- `string get_tag()`
  （string get_tag（））
- `bool CompareTag(string tag)`
  （bool Compare标签（string tag））
- `GameObject[] FindGameObjectsWithTag(string tag)`
  （游戏Object[] 查找游戏ObjectsWith标签（string tag））
- `void SendMessage(string methodName, object value, SendMessageOptions options)`
  （void 发送Message（string methodName, object value, 发送MessageOptions options））
- `void Internal_CreateGameObject(GameObject self, string name)`
  （void Internal_创建游戏对象（游戏对象 self, string name））
- `GameObject get_gameObject()`
  （游戏对象 获取_游戏对象（））

---

## GaussianWindow1D_CameraRotation（GaussianWindow1D_摄像机Rotation）

**继承**: GaussianWindow1d<Vector2>（GaussianWindow1d<Vector2>）

### 方法 (1)

- `Vector2 Compute(int windowPos)`
  （二维向量 Compute（int windowPos））

---

## GaussianWindow1D_Quaternion（GaussianWindow1D_Quaternion）

**继承**: GaussianWindow1d<Quaternion>（GaussianWindow1d<Quaternion>）

### 方法 (1)

- `Quaternion Compute(int windowPos)`
  （Quaternion Compute（int windowPos））

---

## GaussianWindow1D_Vector3（GaussianWindow1D_三维向量）

**继承**: GaussianWindow1d<Vector3>（GaussianWindow1d<Vector3>）

### 方法 (1)

- `Vector3 Compute(int windowPos)`
  （三维向量 Compute（int windowPos））

---

## GenerateHLSL（GenerateHLSL）

**继承**: Attribute（属性）

### 字段 (9)

- `PackingRules packingRules`（PackingRules packingRules）(偏移: 0x8)
- `bool containsPackedFields`（bool containsPackedFields）(偏移: 0xC)
- `bool needAccessors`（bool needAccessors）(偏移: 0x0)
- `bool needSetters`（bool needSetters）(偏移: 0x0)
- `bool needParamDebug`（bool needParamDebug）(偏移: 0x0)
- `int paramDefinesStart`（int paramDefines开始）(偏移: 0x0)
- `bool omitStructDeclaration`（bool omitStructDeclaration）(偏移: 0x14)
- `bool generateCBuffer`（bool generateC缓冲区）(偏移: 0x15)
- `int constantRegister`（int constantRegister）(偏移: 0x18)

---

## GenericBaker（GenericBaker）

**继承**: Baker（Baker）

### 字段 (8)

- `bool markAsLegacy`（bool markAsLegacy）(偏移: 0x44)
- `Transform root`（变换 根节点）(偏移: 0x48)
- `Transform rootNode`（变换 root节点）(偏移: 0x4C)
- `Transform[] ignoreList`（Transform[] ignore列表）(偏移: 0x50)
- `Transform[] bakePositionList`（Transform[] bakePosition列表）(偏移: 0x54)
- `BakerTransform[] children`（BakerTransform[] children）(偏移: 0x58)
- `BakerTransform rootChild`（Baker变换 root子级）(偏移: 0x5C)
- `int rootChildIndex`（int root子级索引）(偏移: 0x60)

### 方法 (8)

- `void Awake()`
  （void 唤醒（））
- `Transform GetCharacterRoot()`
  （变换 获取角色根（））
- `void OnStartBaking()`
  （void On开始Baking（））
- `void OnSetLoopFrame(float time)`
  （void On集合LoopFrame（float time））
- `void OnSetCurves(ref AnimationClip clip)`
  （void On集合Curves（ref AnimationClip clip））
- `void OnSetKeyframes(float time, bool lastFrame)`
  （void On集合Keyframes（float time, bool lastFrame））
- `bool IsIgnored(Transform t)`
  （bool 是否Ignored（变换 t））
- `bool BakePosition(Transform t)`
  （bool BakePosition（变换 t））

---

## GenericParameterAttributes（GenericParameterAttributes）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## GenericPoser（GenericPoser）

**继承**: Poser（Poser）

### 字段 (1)

- `GenericPoser.Map[] maps`（GenericPoser.Map[] maps）(偏移: 0x30)

### 方法 (6)

- `void AutoMapping()`
  （void 自动Mapping（））
- `void InitiatePoser()`
  （void InitiatePoser（））
- `void UpdatePoser()`
  （void 更新Poser（））
- `void FixPoserTransforms()`
  （void FixPoserTransforms（））
- `void StoreDefaultState()`
  （void 商店默认的状态（））
- `Transform GetTargetNamed(string tName, Transform[] array)`
  （变换 获取目标Named（string tName, Transform[] array））

---

## GenericPoser.Map（GenericPoser.映射）

### 字段 (4)

- `Transform bone`（变换 骨骼）(偏移: 0x8)
- `Transform target`（变换 目标）(偏移: 0xC)
- `Vector3 defaultLocalPosition`（三维向量 默认本地位置）(偏移: 0x10)
- `Quaternion defaultLocalRotation`（四元数 默认本地旋转）(偏移: 0x1C)

### 方法 (3)

- `void StoreDefaultState()`
  （void 商店默认的状态（））
- `void FixTransform()`
  （void Fix变换（））
- `void Update(float localRotationWeight, float localPositionWeight)`
  （void 更新（float localRotationWeight, float localPositionWeight））

---

## GenericTypeParameterBuilder（Generic类型Parameter构建器）

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

## Geom（Geom）

### 方法 (16)

- `bool IsWindingInside(WindingRule rule, int n)`
  （bool 是否WindingInside（WindingRule rule, int n））
- `bool VertCCW(MeshUtils.Vertex u, MeshUtils.Vertex v, MeshUtils.Vertex w)`
  （bool VertCCW（网格Utils.Vertex u, 网格Utils.Vertex v, 网格Utils.Vertex w））
- `bool VertEq(MeshUtils.Vertex lhs, MeshUtils.Vertex rhs)`
  （bool VertEq（网格Utils.Vertex lhs, 网格Utils.Vertex rhs））
- `bool VertLeq(MeshUtils.Vertex lhs, MeshUtils.Vertex rhs)`
  （bool VertLeq（网格Utils.Vertex lhs, 网格Utils.Vertex rhs））
- `float EdgeEval(MeshUtils.Vertex u, MeshUtils.Vertex v, MeshUtils.Vertex w)`
  （float EdgeEval（网格Utils.Vertex u, 网格Utils.Vertex v, 网格Utils.Vertex w））
- `float EdgeSign(MeshUtils.Vertex u, MeshUtils.Vertex v, MeshUtils.Vertex w)`
  （float Edge标志（网格Utils.Vertex u, 网格Utils.Vertex v, 网格Utils.Vertex w））
- `bool TransLeq(MeshUtils.Vertex lhs, MeshUtils.Vertex rhs)`
  （bool TransLeq（网格Utils.Vertex lhs, 网格Utils.Vertex rhs））
- `float TransEval(MeshUtils.Vertex u, MeshUtils.Vertex v, MeshUtils.Vertex w)`
  （float TransEval（网格Utils.Vertex u, 网格Utils.Vertex v, 网格Utils.Vertex w））
- `float TransSign(MeshUtils.Vertex u, MeshUtils.Vertex v, MeshUtils.Vertex w)`
  （float Trans标志（网格Utils.Vertex u, 网格Utils.Vertex v, 网格Utils.Vertex w））
- `bool EdgeGoesLeft(MeshUtils.Edge e)`
  （bool EdgeGoes左（网格Utils.Edge e））
- `bool EdgeGoesRight(MeshUtils.Edge e)`
  （bool EdgeGoes右（网格Utils.Edge e））
- `float VertL1dist(MeshUtils.Vertex u, MeshUtils.Vertex v)`
  （float VertL1dist（网格Utils.Vertex u, 网格Utils.Vertex v））
- `void AddWinding(MeshUtils.Edge eDst, MeshUtils.Edge eSrc)`
  （void 添加Winding（网格Utils.Edge eDst, 网格Utils.Edge eSrc））
- `float Interpolate(float a, float x, float b, float y)`
  （float Interpolate（float a, float x, float b, float y））
- `void Swap(ref MeshUtils.Vertex a, ref MeshUtils.Vertex b)`
  （void Swap（ref MeshUtils.Vertex a, ref MeshUtils.Vertex b））
- `void EdgeIntersect(MeshUtils.Vertex o1, MeshUtils.Vertex d1, MeshUtils.Vertex o2, MeshUtils.Vertex d2, MeshUtils.Vertex v)`
  （void EdgeIntersect（网格Utils.Vertex o1, 网格Utils.Vertex d1, 网格Utils.Vertex o2, 网格Utils.Vertex d2, 网格Utils.Vertex v））

---

## GeometryUtility（Geometry工具）

### 方法 (7)

- `Plane[] CalculateFrustumPlanes(Camera camera)`
  （Plane[] 计算FrustumPlanes（摄像机 camera））
- `void CalculateFrustumPlanes(Camera camera, Plane[] planes)`
  （void 计算FrustumPlanes（摄像机 camera, Plane[] planes））
- `void CalculateFrustumPlanes(Matrix4x4 worldToProjectionMatrix, Plane[] planes)`
  （void 计算FrustumPlanes（Matrix4x4 worldToProjectionMatrix, Plane[] planes））
- `bool TestPlanesAABB(Plane[] planes, Bounds bounds)`
  （bool TestPlanesAABB（Plane[] planes, Bounds bounds））
- `void Internal_ExtractPlanes([Out] Plane[] planes, Matrix4x4 worldToProjectionMatrix)`
  （void Internal_ExtractPlanes（[Out] Plane[] planes, Matrix4x4 worldToProjectionMatrix））
- `bool TestPlanesAABB_Injected(Plane[] planes, ref Bounds bounds)`
  （bool TestPlanesAABB_Injected（Plane[] planes, ref Bounds bounds））
- `void Internal_ExtractPlanes_Injected([Out] Plane[] planes, ref Matrix4x4 worldToProjectionMatrix)`
  （void Internal_ExtractPlanes_Injected（[Out] Plane[] planes, ref Matrix4x4 worldToProjectionMatrix））

---

## GhostBladeOneShine（幽灵刀锋OneShine）

**继承**: VolumeComponent, IPostProcessComponent（体积组件, I后处理组件）

### 字段 (3)

- `FloatParameter RedDuration`（浮点数Parameter 红色持续时间）(偏移: 0x1C)
- `FloatParameter WhiteDuration`（浮点数Parameter White持续时间）(偏移: 0x20)
- `FloatParameter PosterizePower`（浮点数Parameter Posterize力度）(偏移: 0x24)

### 方法 (2)

- `bool IsActive()`
  （布尔值 是否激活的（））
- `bool IsTileCompatible()`
  （布尔值 是否瓦片兼容（））

---

## GhostBladeOneShinePass（幽灵刀锋OneShinePass）

**继承**: ScriptableRenderPass（可脚本化渲染通道）

### 字段 (9)

- `string k_RenderTag`（string k_Render标签）(偏移: 0x0)
- `int MainTexID`（int 主要的TexID）(偏移: 0x4)
- `int TempID`（int TempID）(偏移: 0x8)
- `int RedDurationID`（int 红色持续时间ID）(偏移: 0xC)
- `int WhiteDurationID`（int White持续时间ID）(偏移: 0x10)
- `int PosterizePowerID`（int Posterize力度ID）(偏移: 0x14)
- `GhostBladeOneShine oneShine`（幽灵刀锋OneShine oneShine）(偏移: 0x54)
- `Material mat`（材质 mat）(偏移: 0x58)
- `RenderTargetIdentifier curTarget`（Render目标Identifier cur目标）(偏移: 0x5C)

### 方法 (3)

- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（可脚本化渲染上下文 context, 引用 渲染数据 renderingData））
- `void Render(CommandBuffer cmd, ref RenderingData renderingData)`
  （void Render（Command缓冲区 cmd, ref RenderingData renderingData））
- `void Setup(in RenderTargetIdentifier curTarget)`
  （void Setup（in RenderTargetIdentifier curTarget））

---

## GizmoSubset（GizmoSubset）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Gizmos（Gizmos）

### 方法 (16)

- `void DrawLine(Vector3 from, Vector3 to)`
  （void DrawLine（三维向量 from, 三维向量 to））
- `void DrawWireSphere(Vector3 center, float radius)`
  （void DrawWireSphere（三维向量 center, float radius））
- `void DrawSphere(Vector3 center, float radius)`
  （void DrawSphere（三维向量 center, float radius））
- `void DrawWireCube(Vector3 center, Vector3 size)`
  （void DrawWireCube（三维向量 center, 三维向量 size））
- `void DrawCube(Vector3 center, Vector3 size)`
  （void DrawCube（三维向量 center, 三维向量 size））
- `void DrawIcon(Vector3 center, string name, bool allowScaling, Color tint)`
  （void Draw图标（三维向量 center, string name, bool allowScaling, 颜色 tint））
- `Color get_color()`
  （颜色 获取_颜色（））
- `void set_color(Color value)`
  （void 设置_颜色（颜色 value））
- `void DrawLine_Injected(ref Vector3 from, ref Vector3 to)`
  （void DrawLine_Injected（ref Vector3 from, ref Vector3 to））
- `void DrawWireSphere_Injected(ref Vector3 center, float radius)`
  （void DrawWireSphere_Injected（ref Vector3 center, float radius））
- `void DrawSphere_Injected(ref Vector3 center, float radius)`
  （void DrawSphere_Injected（ref Vector3 center, float radius））
- `void DrawWireCube_Injected(ref Vector3 center, ref Vector3 size)`
  （void DrawWireCube_Injected（ref Vector3 center, ref Vector3 size））
- `void DrawCube_Injected(ref Vector3 center, ref Vector3 size)`
  （void DrawCube_Injected（ref Vector3 center, ref Vector3 size））
- `void DrawIcon_Injected(ref Vector3 center, string name, bool allowScaling, ref Color tint)`
  （void DrawIcon_Injected（ref Vector3 center, string name, bool allowScaling, ref Color tint））
- `void get_color_Injected(out Color ret)`
  （void get_color_Injected（out Color ret））
- `void set_color_Injected(ref Color value)`
  （void set_color_Injected（ref Color value））

---

## GlobalDynamicResolutionSettings（全局的动态的ResolutionSettings）

### 字段 (7)

- `bool enabled`（bool enabled）(偏移: 0x0)
- `float maxPercentage`（float maxPercentage）(偏移: 0x4)
- `float minPercentage`（float minPercentage）(偏移: 0x8)
- `DynamicResolutionType dynResType`（动态的Resolution类型 dynRes类型）(偏移: 0xC)
- `DynamicResUpscaleFilter upsampleFilter`（动态的ResUpscaleFilter upsampleFilter）(偏移: 0xD)
- `bool forceResolution`（bool forceResolution）(偏移: 0xE)
- `float forcedPercentage`（float forcedPercentage）(偏移: 0x10)

### 方法 (1)

- `GlobalDynamicResolutionSettings NewDefault()`
  （全局的动态的ResolutionSettings 新的默认的（））

---

## GlobalJavaObjectRef（全局的Java对象Ref）

### 字段 (2)

- `bool m_disposed`（布尔值 m_已释放）(偏移: 0x8)
- `IntPtr m_jobject`（整数Ptr m_jobject）(偏移: 0xC)

### 方法 (3)

- `void Finalize()`
  （void 终结（））
- `IntPtr op_Implicit(GlobalJavaObjectRef obj)`
  （整数Ptr op_Implicit（全局的Java对象Ref obj））
- `void Dispose()`
  （void 释放（））

---

## GoCrouchPos（Go蹲下Pos）

**继承**: BotActionBase（机器人动作基础）

### 字段 (2)

- `Bot_CrouchPos target`（Bot_蹲下Pos target）(偏移: 0x10)
- `float giveUpTime`（float give上时间）(偏移: 0x14)

### 方法 (7)

- `void Bot_Getter_ZoomDirection(ref Vector3 zoomDir, ref int priority)`
  （void Bot_Getter_瞄准方向（ref Vector3 zoomDir, ref int priority））
- `void Bot_Destination_Listener(ref Vector3 pos, ref int priority)`
  （void Bot_目的地_监听器（引用 Vector3 pos, 引用 整数 priority））
- `void Update()`
  （void 更新（））
- `bool CanDo()`
  （布尔值 能否执行（））
- `void DoAction()`
  （void 执行动作（））
- `void OnActionFinish()`
  （void 动作完成时（））
- `void GiveUp()`
  （void 放弃（））

---

## GoDestination（GoDestination）

**继承**: BotActionBase（机器人动作基础）

### 方法 (2)

- `bool CanDo()`
  （布尔值 能否执行（））
- `void DoAction()`
  （void 执行动作（））

---

