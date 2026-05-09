# 游戏类定义 (Part 10/21)

共 200 个类 (总序号 1801 - 2000)

---

## InternalSerializerTypeE（内部的Serializer类型E）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## InternalStaticBatchingUtility（内部的静态的Batching工具）

### 方法 (6)

- `void CombineRoot(GameObject staticBatchRoot, InternalStaticBatchingUtility.StaticBatcherGOSorter sorter)`
  （void Combine根（游戏对象 staticBatchRoot, 内部的静态的BatchingUtility.静态的BatcherGOSorter sorter））
- `void Combine(GameObject staticBatchRoot, bool combineOnlyStatic, bool isEditorPostprocessScene, InternalStaticBatchingUtility.StaticBatcherGOSorter sorter)`
  （void Combine（游戏对象 staticBatchRoot, bool combineOnlyStatic, bool isEditorPostprocessScene, 内部的静态的BatchingUtility.静态的BatcherGOSorter sorter））
- `uint GetMeshFormatHash(Mesh mesh)`
  （uint 获取网格格式化Hash（网格 mesh））
- `GameObject[] SortGameObjectsForStaticBatching(GameObject[] gos, InternalStaticBatchingUtility.StaticBatcherGOSorter sorter)`
  （游戏Object[] Sort游戏ObjectsFor静态的Batching（游戏Object[] gos, 内部的静态的BatchingUtility.静态的BatcherGOSorter sorter））
- `void CombineGameObjects(GameObject[] gos, GameObject staticBatchRoot, bool isEditorPostprocessScene, InternalStaticBatchingUtility.StaticBatcherGOSorter sorter)`
  （void Combine游戏Objects（游戏Object[] gos, 游戏对象 staticBatchRoot, bool isEditorPostprocessScene, 内部的静态的BatchingUtility.静态的BatcherGOSorter sorter））
- `void MakeBatch(List<MeshSubsetCombineUtility.MeshContainer> meshes, Transform staticBatchRootTransform, int batchIndex)`
  （void MakeBatch（List<网格SubsetCombineUtility.网格Container> meshes, 变换 staticBatchRootTransform, int batchIndex））

---

## InternalStaticBatchingUtility.StaticBatcherGOSorter（内部的静态的BatchingUtility.静态的BatcherGOSorter）

### 方法 (5)

- `long GetMaterialId(Renderer renderer)`
  （long 获取材质Id（渲染器 renderer））
- `int GetLightmapIndex(Renderer renderer)`
  （int 获取Lightmap索引（渲染器 renderer））
- `Renderer GetRenderer(GameObject go)`
  （渲染器 获取渲染器（游戏对象 go））
- `Mesh GetMesh(GameObject go)`
  （网格 获取网格（游戏对象 go））
- `long GetRendererId(Renderer renderer)`
  （long 获取渲染器Id（渲染器 renderer））

---

## InternalStringComparer（内部的字符串Comparer）

**继承**: EqualityComparer<string>（EqualityComparer<string>）

### 方法 (3)

- `int GetHashCode(string obj)`
  （int 获取HashCode（string obj））
- `bool Equals(string x, string y)`
  （bool Equals（string x, string y））
- `int IndexOf(string[] array, string value, int startIndex, int count)`
  （int 索引Of（string[] array, string value, int startIndex, int count））

---

## InternalTaskOptions（内部的TaskOptions）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## InternalThread（内部的Thread）

**继承**: CriticalFinalizerObject（CriticalFinalizer对象）

### 字段 (39)

- `int lock_thread_id`（int lock_thread_id）(偏移: 0x8)
- `IntPtr handle`（整数Ptr handle）(偏移: 0xC)
- `IntPtr native_handle`（整数Ptr native_handle）(偏移: 0x10)
- `IntPtr unused3`（整数Ptr unused3）(偏移: 0x14)
- `IntPtr name`（整数Ptr name）(偏移: 0x18)
- `int name_len`（int name_len）(偏移: 0x1C)
- `ThreadState state`（Thread状态 state）(偏移: 0x20)
- `object abort_exc`（object abort_exc）(偏移: 0x24)
- `int abort_state_handle`（int abort_state_handle）(偏移: 0x28)
- `long thread_id`（long thread_id）(偏移: 0x30)
- `IntPtr debugger_thread`（整数Ptr debugger_thread）(偏移: 0x38)
- `UIntPtr static_data`（U整数Ptr static_data）(偏移: 0x3C)
- `IntPtr runtime_thread_info`（整数Ptr runtime_thread_info）(偏移: 0x40)
- `object current_appcontext`（object current_appcontext）(偏移: 0x44)
- `object root_domain_thread`（object root_domain_thread）(偏移: 0x48)
- `byte[] _serialized_principal`（byte[] _serialized_principal）(偏移: 0x4C)
- `int _serialized_principal_version`（int _serialized_principal_version）(偏移: 0x50)
- `IntPtr appdomain_refs`（整数Ptr appdomain_refs）(偏移: 0x54)
- `int interruption_requested`（int interruption_requested）(偏移: 0x58)
- `IntPtr synch_cs`（整数Ptr synch_cs）(偏移: 0x5C)
- `bool threadpool_thread`（bool threadpool_thread）(偏移: 0x60)
- `bool thread_interrupt_requested`（bool thread_interrupt_requested）(偏移: 0x61)
- `int stack_size`（int stack_size）(偏移: 0x64)
- `byte apartment_state`（byte apartment_state）(偏移: 0x68)
- `int critical_region_level`（int critical_region_level）(偏移: 0x6C)
- `int managed_id`（int managed_id）(偏移: 0x70)
- `int small_id`（int small_id）(偏移: 0x74)
- `IntPtr manage_callback`（整数Ptr manage_callback）(偏移: 0x78)
- `IntPtr unused4`（整数Ptr unused4）(偏移: 0x7C)
- `IntPtr flags`（整数Ptr flags）(偏移: 0x80)
- `IntPtr thread_pinning_ref`（整数Ptr thread_pinning_ref）(偏移: 0x84)
- `IntPtr abort_protected_block_count`（整数Ptr abort_protected_block_count）(偏移: 0x88)
- `int priority`（整数 优先级）(偏移: 0x8C)
- `IntPtr owned_mutex`（整数Ptr owned_mutex）(偏移: 0x90)
- `IntPtr suspended_event`（整数Ptr suspended_event）(偏移: 0x94)
- `int self_suspended`（int self_suspended）(偏移: 0x98)
- `IntPtr unused1`（整数Ptr unused1）(偏移: 0x9C)
- `IntPtr unused2`（整数Ptr unused2）(偏移: 0xA0)
- `IntPtr last`（整数Ptr last）(偏移: 0xA4)

### 方法 (2)

- `void Thread_free_internal()`
  （void Thread_free_internal（））
- `void Finalize()`
  （void 终结（））

---

## Internal_SubsystemDescriptors（Internal_SubsystemDescriptors）

### 方法 (1)

- `void Internal_AddDescriptor(SubsystemDescriptor descriptor)`
  （void Internal_添加Descriptor（SubsystemDescriptor descriptor））

---

## InternalsVisibleToAttribute（Internals可见的ToAttribute）

**继承**: Attribute（属性）

### 字段 (2)

- `string _assemblyName`（string _assembly名称）(偏移: 0x8)
- `bool _allInternalsVisible`（bool _allInternals可见的）(偏移: 0xC)

### 方法 (3)

- `string get_AssemblyName()`
  （string get_Assembly名称（））
- `bool get_AllInternalsVisible()`
  （bool get_所有Internals可见的（））
- `void set_AllInternalsVisible(bool value)`
  （void set_所有Internals可见的（bool value））

---

## Interp（Interp）

### 方法 (30)

- `float Float(float t, InterpolationMode mode)`
  （float 浮点数（float t, Interpolation模式 mode））
- `Vector3 V3(Vector3 v1, Vector3 v2, float t, InterpolationMode mode)`
  （三维向量 V3（三维向量 v1, 三维向量 v2, float t, Interpolation模式 mode））
- `float LerpValue(float value, float target, float increaseSpeed, float decreaseSpeed)`
  （float Lerp值（float value, float target, float increaseSpeed, float decreaseSpeed））
- `float None(float t, float b, float c)`
  （float 无（float t, float b, float c））
- `float InOutCubic(float t, float b, float c)`
  （float InOutCubic（float t, float b, float c））
- `float InOutQuintic(float t, float b, float c)`
  （float InOutQuintic（float t, float b, float c））
- `float InQuintic(float t, float b, float c)`
  （float InQuintic（float t, float b, float c））
- `float InQuartic(float t, float b, float c)`
  （float InQuartic（float t, float b, float c））
- `float InCubic(float t, float b, float c)`
  （float InCubic（float t, float b, float c））
- `float InQuadratic(float t, float b, float c)`
  （float InQuadratic（float t, float b, float c））
- `float OutQuintic(float t, float b, float c)`
  （float OutQuintic（float t, float b, float c））
- `float OutQuartic(float t, float b, float c)`
  （float OutQuartic（float t, float b, float c））
- `float OutCubic(float t, float b, float c)`
  （float OutCubic（float t, float b, float c））
- `float OutInCubic(float t, float b, float c)`
  （float OutInCubic（float t, float b, float c））
- `float OutInQuartic(float t, float b, float c)`
  （float OutInQuartic（float t, float b, float c））
- `float BackInCubic(float t, float b, float c)`
  （float 后InCubic（float t, float b, float c））
- `float BackInQuartic(float t, float b, float c)`
  （float 后InQuartic（float t, float b, float c））
- `float OutBackCubic(float t, float b, float c)`
  （float Out后Cubic（float t, float b, float c））
- `float OutBackQuartic(float t, float b, float c)`
  （float Out后Quartic（float t, float b, float c））
- `float OutElasticSmall(float t, float b, float c)`
  （float OutElasticSmall（float t, float b, float c））
- `float OutElasticBig(float t, float b, float c)`
  （float OutElasticBig（float t, float b, float c））
- `float InElasticSmall(float t, float b, float c)`
  （float InElasticSmall（float t, float b, float c））
- `float InElasticBig(float t, float b, float c)`
  （float InElasticBig（float t, float b, float c））
- `float InSine(float t, float b, float c)`
  （float InSine（float t, float b, float c））
- `float OutSine(float t, float b, float c)`
  （float OutSine（float t, float b, float c））
- `float InOutSine(float t, float b, float c)`
  （float InOutSine（float t, float b, float c））
- `float InElastic(float t, float b, float c)`
  （float InElastic（float t, float b, float c））
- `float OutElastic(float t, float b, float c)`
  （float OutElastic（float t, float b, float c））
- `float InBack(float t, float b, float c)`
  （float In后（float t, float b, float c））
- `float OutBack(float t, float b, float c)`
  （float Out后（float t, float b, float c））

---

## InterpolationMode（Interpolation模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## IntersectNode（Intersect节点）

### 字段 (4)

- `TEdge Edge1`（TEdge Edge1）(偏移: 0x8)
- `TEdge Edge2`（TEdge Edge2）(偏移: 0xC)
- `IntPoint Pt`（整数Point Pt）(偏移: 0x10)
- `IntersectNode Next`（Intersect节点 下一个）(偏移: 0x20)

---

## IntervalTreeNode（间隔Tree节点）

### 字段 (5)

- `long center`（long center）(偏移: 0x0)
- `int first`（int first）(偏移: 0x8)
- `int last`（int last）(偏移: 0xC)
- `int left`（int left）(偏移: 0x10)
- `int right`（int right）(偏移: 0x14)

---

## IntrospectiveSortUtilities（IntrospectiveSortUtilities）

### 方法 (2)

- `int FloorLog2(int n)`
  （int FloorLog2（int n））
- `void ThrowOrIgnoreBadComparer(object comparer)`
  （void 投掷OrIgnoreBadComparer（object comparer））

---

## InvariantComparer（InvariantComparer）

**继承**: IComparer（I比较器）

### 字段 (2)

- `CompareInfo m_compareInfo`（比较信息 m_compare信息）(偏移: 0x8)
- `InvariantComparer Default`（InvariantComparer 默认的）(偏移: 0x0)

### 方法 (1)

- `int Compare(object a, object b)`
  （整数 比较（对象 a, 对象 b））

---

## Invincible（Invincible）

**继承**: BotSkillBase（机器人技能基础）

### 方法 (1)

- `bool CanDo()`
  （布尔值 能否执行（））

---

## InvincibleBuff（Invincible增益）

**继承**: Buff（增益）

### 字段 (1)

- `bool ignoreAttack`（bool ignoreAttack）(偏移: 0x24)

### 方法 (2)

- `void Owner_Invincible_BuffUpdater(ref bool value)`
  （void Owner_Invincible_增益Updater（ref bool value））
- `void OnLifeEnd()`
  （void 生命结束时（））

---

## InvokableCall（InvokableCall）

**继承**: BaseInvokableCall（基础InvokableCall）

### 字段 (1)

- `UnityAction Delegate`（Unity引擎动作 委托）(偏移: 0x8)

### 方法 (5)

- `void add_Delegate(UnityAction value)`
  （void add_委托（Unity引擎动作 value））
- `void remove_Delegate(UnityAction value)`
  （void remove_委托（Unity引擎动作 value））
- `void Invoke(object[] args)`
  （void Invoke（object[] args））
- `void Invoke()`
  （void 调用（））
- `bool Find(object targetObj, MethodInfo method)`
  （bool 查找（object targetObj, Method信息 method））

---

## InvokableCallList（InvokableCall列表）

### 字段 (4)

- `List<BaseInvokableCall> m_PersistentCalls`（List<基础InvokableCall> m_持久的Calls）(偏移: 0x8)
- `List<BaseInvokableCall> m_RuntimeCalls`（List<基础InvokableCall> m_RuntimeCalls）(偏移: 0xC)
- `List<BaseInvokableCall> m_ExecutingCalls`（List<基础InvokableCall> m_ExecutingCalls）(偏移: 0x10)
- `bool m_NeedsUpdate`（bool m_Needs更新）(偏移: 0x14)

### 方法 (5)

- `void AddPersistentInvokableCall(BaseInvokableCall call)`
  （void 添加持久的InvokableCall（基础InvokableCall call））
- `void AddListener(BaseInvokableCall call)`
  （void 添加监听器（基础InvokableCall call））
- `void RemoveListener(object targetObj, MethodInfo method)`
  （void 移除监听器（object targetObj, Method信息 method））
- `void ClearPersistent()`
  （void 清除持久的（））
- `List<BaseInvokableCall> PrepareInvoke()`
  （List<基础InvokableCall> PrepareInvoke（））

---

## InvokeOnRenderObjectCallbackPass（InvokeOnRender对象回调Pass）

**继承**: ScriptableRenderPass（可脚本化渲染通道）

### 方法 (1)

- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（可脚本化渲染上下文 context, 引用 渲染数据 renderingData））

---

## Ipv6Element（Ipv6元素）

**继承**: ConfigurationElement（配置元素）

### 方法 (1)

- `ConfigurationPropertyCollection get_Properties()`
  （配置属性集合 获取_属性（））

---

## IriHelper（Iri辅助器）

### 方法 (4)

- `bool CheckIriUnicodeRange(char unicode, bool isQuery)`
  （bool 检查IriUnicode范围（char unicode, bool isQuery））
- `bool CheckIriUnicodeRange(char highSurr, char lowSurr, ref bool surrogatePair, bool isQuery)`
  （bool 检查IriUnicode范围（char highSurr, char lowSurr, ref bool surrogatePair, bool isQuery））
- `bool CheckIsReserved(char ch, UriComponents component)`
  （bool 检查是否Reserved（char ch, UriComponents component））
- `string EscapeUnescapeIri(char* pInput, int start, int end, UriComponents component)`
  （string EscapeUnescapeIri（char* pInput, int start, int end, UriComponents component））

---

## ItemAttribute（项目Attribute）

### 字段 (1)

- `List<ItemAttributeBase> list`（List<项目AttributeBase> list）(偏移: 0x8)

### 方法 (1)

- `void AddClipBuff()`
  （void 添加弹匣增益（））

---

## ItemAttribute.Type（项目Attribute.类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ItemAttributeBase（项目Attribute基础）

### 字段 (1)

- `ItemAttribute.Type type`（项目Attribute.类型 type）(偏移: 0x8)

---

## ItemObject（项目对象）

### 方法 (2)

- `SO_Item get_data()`
  （SO_项目 get_data（））
- `void set_data(SO_Item value)`
  （void set_data（SO_项目 value））

---

## JapaneseCalendar（JapaneseCalendar）

**继承**: Calendar（日历）

### 字段 (4)

- `DateTime calendarMinValue`（Date时间 calendar最小值）(偏移: 0x0)
- `EraInfo[] japaneseEraInfo`（EraInfo[] japaneseEra信息）(偏移: 0x8)
- `Calendar s_defaultInstance`（Calendar s_default实例）(偏移: 0xC)
- `GregorianCalendarHelper helper`（GregorianCalendar辅助器 helper）(偏移: 0x14)

### 方法 (23)

- `DateTime get_MinSupportedDateTime()`
  （日期时间 获取_最小支持日期时间（））
- `DateTime get_MaxSupportedDateTime()`
  （日期时间 获取_最大支持日期时间（））
- `EraInfo[] GetEraInfo()`
  （EraInfo[] 获取Era信息（））
- `EraInfo[] GetErasFromRegistry()`
  （EraInfo[] 获取ErasFromRegistry（））
- `Calendar GetDefaultInstance()`
  （Calendar 获取默认的实例（））
- `int get_ID()`
  （整数 获取_ID（））
- `int GetDaysInMonth(int year, int month, int era)`
  （整数 获取_月中的天数（整数 year, 整数 month, 整数 era））
- `int GetDaysInYear(int year, int era)`
  （整数 获取_年中的天数（整数 year, 整数 era））
- `int GetDayOfMonth(DateTime time)`
  （整数 获取_月中的日（日期时间 time））
- `DayOfWeek GetDayOfWeek(DateTime time)`
  （星期几 获取星期几（日期时间 time））
- `int GetMonthsInYear(int year, int era)`
  （整数 获取_年中的月数（整数 year, 整数 era））
- `int GetEra(DateTime time)`
  （整数 获取_纪元（日期时间 time））
- `int GetMonth(DateTime time)`
  （整数 获取_月（日期时间 time））
- `int GetYear(DateTime time)`
  （整数 获取_年（日期时间 time））
- `bool IsLeapYear(int year, int era)`
  （布尔值 是否闰年（整数 year, 整数 era））
- `DateTime ToDateTime(int year, int month, int day, int hour, int minute, int second, int millisecond, int era)`
  （日期时间 转日期时间（整数 year, 整数 month, 整数 day, 整数 hour, 整数 minute, 整数 second, 整数 millisecond, 整数 era））
- `int ToFourDigitYear(int year)`
  （整数 转四位数年份（整数 year））
- `int[] get_Eras()`
  （整数[] 获取_纪元（））
- `string[] EraNames()`
  （string[] EraNames（））
- `string[] AbbrevEraNames()`
  （string[] AbbrevEraNames（））
- `string[] EnglishEraNames()`
  （string[] EnglishEraNames（））
- `bool IsValidYear(int year, int era)`
  （bool 是否ValidYear（int year, int era））
- `int get_TwoDigitYearMax()`
  （整数 获取_两位数年份最大（））

---

## JobHandle（Job句柄）

### 字段 (2)

- `IntPtr jobGroup`（整数Ptr job组）(偏移: 0x0)
- `int version`（整数 版本）(偏移: 0x4)

### 方法 (3)

- `void CompleteAll(NativeArray<JobHandle> jobs)`
  （void Complete所有（NativeArray<JobHandle> jobs））
- `void ScheduleBatchedJobs()`
  （void ScheduleBatchedJobs（））
- `void ScheduleBatchedJobsAndCompleteAll(void* jobs, int count)`
  （void ScheduleBatchedJobsAndComplete所有（void* jobs, int count））

---

## JobRanges（JobRanges）

### 字段 (6)

- `int BatchSize`（int Batch大小）(偏移: 0x0)
- `int NumJobs`（int NumJobs）(偏移: 0x4)
- `int TotalIterationCount`（int TotalIteration数量）(偏移: 0x8)
- `int NumPhases`（int NumPhases）(偏移: 0xC)
- `IntPtr StartEndIndex`（整数Ptr 开始结束索引）(偏移: 0x10)
- `IntPtr PhaseData`（整数Ptr Phase数据）(偏移: 0x14)

---

## JobsUtility（Jobs工具）

### 字段 (1)

- `JobsUtility.PanicFunction_ PanicFunction`（JobsUtility.PanicFunction_ PanicFunction）(偏移: 0x0)

### 方法 (5)

- `JobHandle Schedule(ref JobsUtility.JobScheduleParameters parameters)`
  （Job句柄 Schedule（ref JobsUtility.JobScheduleParameters parameters））
- `IntPtr CreateJobReflectionData(Type wrapperJobType, Type userJobType, object managedJobFunction0, object managedJobFunction1, object managedJobFunction2)`
  （整数Ptr 创建JobReflection数据（类型 wrapperJobType, 类型 userJobType, object managedJobFunction0, object managedJobFunction1, object managedJobFunction2））
- `IntPtr CreateJobReflectionData(Type type, object managedJobFunction0, object managedJobFunction1, object managedJobFunction2)`
  （整数Ptr 创建JobReflection数据（类型 type, object managedJobFunction0, object managedJobFunction1, object managedJobFunction2））
- `void InvokePanicFunction()`
  （void InvokePanicFunction（））
- `void Schedule_Injected(ref JobsUtility.JobScheduleParameters parameters, out JobHandle ret)`
  （void Schedule_Injected（ref JobsUtility.JobScheduleParameters parameters, out JobHandle ret））

---

## JobsUtility.JobScheduleParameters（JobsUtility.JobScheduleParameters）

### 字段 (4)

- `JobHandle Dependency`（Job句柄 Dependency）(偏移: 0x0)
- `int ScheduleMode`（int Schedule模式）(偏移: 0x8)
- `IntPtr ReflectionData`（整数Ptr Reflection数据）(偏移: 0xC)
- `IntPtr JobDataPtr`（整数Ptr Job数据Ptr）(偏移: 0x10)

---

## JobsUtility.PanicFunction_（JobsUtility.PanicFunction_）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke()`
  （void 调用（））
- `IAsyncResult BeginInvoke(AsyncCallback callback, object object)`
  （I异步结果 开始调用（异步回调 callback, 对象 object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## Join（Join）

### 字段 (3)

- `OutPt OutPt1`（OutPt OutPt1）(偏移: 0x8)
- `OutPt OutPt2`（OutPt OutPt2）(偏移: 0xC)
- `IntPoint OffPt`（整数Point OffPt）(偏移: 0x10)

---

## Joint（Joint）

**继承**: Component（组件）

### 方法 (3)

- `Rigidbody get_connectedBody()`
  （刚体 get_connected身体（））
- `void set_connectedAnchor(Vector3 value)`
  （void set_connectedAnchor（三维向量 value））
- `void set_connectedAnchor_Injected(ref Vector3 value)`
  （void set_connectedAnchor_Injected（ref Vector3 value））

---

## KeyBuilder（键构建器）

### 字段 (1)

- `RandomNumberGenerator rng`（随机NumberGenerator rng）(偏移: 0x0)

### 方法 (3)

- `RandomNumberGenerator get_Rng()`
  （随机NumberGenerator get_Rng（））
- `byte[] Key(int size)`
  （byte[] 键（int size））
- `byte[] IV(int size)`
  （byte[] IV（int size））

---

## KeyCode（键Code）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## KeyHandler（键处理器）

### 字段 (10)

- `Hashtable key_to_handler`（Hashtable key_to_handler）(偏移: 0x0)
- `Hashtable dir_to_handler`（Hashtable dir_to_handler）(偏移: 0x4)
- `string Dir`（string Dir）(偏移: 0x8)
- `string ActualDir`（string ActualDir）(偏移: 0xC)
- `bool IsVolatile`（bool 是否Volatile）(偏移: 0x10)
- `Hashtable values`（Hashtable values）(偏移: 0x14)
- `string file`（string file）(偏移: 0x18)
- `bool dirty`（bool dirty）(偏移: 0x1C)
- `string user_store`（string user_store）(偏移: 0x8)
- `string machine_store`（string machine_store）(偏移: 0xC)

### 方法 (23)

- `void Load()`
  （void 加载（））
- `void LoadKey(SecurityElement se)`
  （void 加载键（Security元素 se））
- `RegistryKey Ensure(RegistryKey rkey, string extra, bool writable, bool is_volatile)`
  （Registry键 Ensure（Registry键 rkey, string extra, bool writable, bool is_volatile））
- `RegistryKey Probe(RegistryKey rkey, string extra, bool writable)`
  （Registry键 Probe（Registry键 rkey, string extra, bool writable））
- `string CombineName(RegistryKey rkey, string extra)`
  （string Combine名称（Registry键 rkey, string extra））
- `long GetSystemBootTime()`
  （long 获取系统Boot时间（））
- `long GetRegisteredBootTime(string path)`
  （long 获取RegisteredBoot时间（string path））
- `void SaveRegisteredBootTime(string path, long btime)`
  （void 保存RegisteredBoot时间（string path, long btime））
- `void CleanVolatileKeys()`
  （void CleanVolatileKeys（））
- `bool VolatileKeyExists(string dir)`
  （bool Volatile键Exists（string dir））
- `string GetVolatileDir(string dir)`
  （string 获取VolatileDir（string dir））
- `KeyHandler Lookup(RegistryKey rkey, bool createNonExisting)`
  （键处理器 Lookup（Registry键 rkey, bool createNonExisting））
- `string GetRootFromDir(string dir)`
  （string 获取根FromDir（string dir））
- `void Drop(RegistryKey rkey)`
  （void Drop（Registry键 rkey））
- `object GetValue(string name, RegistryValueOptions options)`
  （object 获取值（string name, Registry值Options options））
- `string[] GetSubKeyNames()`
  （string[] 获取子键Names（））
- `void Flush()`
  （void 刷新（））
- `bool ValueExists(string name)`
  （bool 值Exists（string name））
- `bool get_IsMarkedForDeletion()`
  （bool get_是否MarkedForDeletion（））
- `void Finalize()`
  （void 终结（））
- `void Save()`
  （void 保存（））
- `string get_UserStore()`
  （string get_User商店（））
- `string get_MachineStore()`
  （string get_Machine商店（））

---

## KeyInputState（按键输入状态）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## KeyInputStateExpand（键输入状态Expand）

### 方法 (2)

- `bool IsTouched(KeyInputState state)`
  （bool 是否Touched（按键输入状态 state））
- `KeyInputState GetKeyState(KeyCode keyCode)`
  （按键输入状态 获取键状态（键Code keyCode））

---

## KeyPairPersistence（键PairPersistence）

### 字段 (9)

- `bool _userPathExists`（bool _user路径Exists）(偏移: 0x0)
- `string _userPath`（string _user路径）(偏移: 0x4)
- `bool _machinePathExists`（bool _machine路径Exists）(偏移: 0x8)
- `string _machinePath`（string _machine路径）(偏移: 0xC)
- `CspParameters _params`（CspParameters _params）(偏移: 0x8)
- `string _keyvalue`（string _keyvalue）(偏移: 0xC)
- `string _filename`（string _filename）(偏移: 0x10)
- `string _container`（string _container）(偏移: 0x14)
- `object lockobj`（object lockobj）(偏移: 0x10)

### 方法 (23)

- `string get_Filename()`
  （string get_Filename（））
- `string get_KeyValue()`
  （string get_键值（））
- `void set_KeyValue(string value)`
  （void set_键值（string value））
- `void Save()`
  （void 保存（））
- `void Remove()`
  （void 移除（））
- `string get_UserPath()`
  （string get_User路径（））
- `string get_MachinePath()`
  （string get_Machine路径（））
- `bool _CanSecure(string root)`
  （bool _能否Secure（string root））
- `bool _ProtectUser(string path)`
  （bool _ProtectUser（string path））
- `bool _ProtectMachine(string path)`
  （bool _ProtectMachine（string path））
- `bool _IsUserProtected(string path)`
  （bool _是否User受保护的（string path））
- `bool _IsMachineProtected(string path)`
  （bool _是否Machine受保护的（string path））
- `bool CanSecure(string path)`
  （bool 能否Secure（string path））
- `bool ProtectUser(string path)`
  （bool ProtectUser（string path））
- `bool ProtectMachine(string path)`
  （bool ProtectMachine（string path））
- `bool IsUserProtected(string path)`
  （bool 是否User受保护的（string path））
- `bool IsMachineProtected(string path)`
  （bool 是否Machine受保护的（string path））
- `bool get_CanChange()`
  （bool get_能否Change（））
- `bool get_UseDefaultKeyContainer()`
  （bool get_Use默认的键容器（））
- `bool get_UseMachineKeyStore()`
  （bool get_UseMachine键商店（））
- `string get_ContainerName()`
  （string get_容器名称（））
- `CspParameters Copy(CspParameters p)`
  （CspParameters 复制（CspParameters p））
- `string ToXml()`
  （string ToXml（））

---

## KeySizes（键Sizes）

### 字段 (3)

- `int m_minSize`（int m_min大小）(偏移: 0x8)
- `int m_maxSize`（int m_max大小）(偏移: 0xC)
- `int m_skipSize`（int m_skip大小）(偏移: 0x10)

### 方法 (5)

- `int get_MinSize()`
  （int get_最小大小（））
- `int get_MaxSize()`
  （int get_最大大小（））
- `int get_SkipSize()`
  （int get_Skip大小（））
- `bool IsLegal(int keySize)`
  （bool 是否Legal（int keySize））
- `bool IsLegalKeySize(KeySizes[] legalKeys, int size)`
  （bool 是否Legal键大小（键Sizes[] legalKeys, int size））

---

## KeyValuePair（键值Pair）

### 方法 (1)

- `string PairToString(object key, object value)`
  （string PairTo字符串（object key, object value））

---

## KeyValuePairs（键值Pairs）

### 字段 (2)

- `object key`（对象 key）(偏移: 0x8)
- `object value`（对象 value）(偏移: 0xC)

---

## KeyedHashAlgorithm（KeyedHashAlgorithm）

**继承**: HashAlgorithm（HashAlgorithm）

### 字段 (1)

- `byte[] KeyValue`（byte[] 键值）(偏移: 0x18)

### 方法 (2)

- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `byte[] get_Key()`
  （字节[] 获取_键（））

---

## Keyframe（Keyframe）

### 字段 (7)

- `float m_Time`（float m_时间）(偏移: 0x0)
- `float m_Value`（浮点数 m_值）(偏移: 0x4)
- `float m_InTangent`（float m_InTangent）(偏移: 0x8)
- `float m_OutTangent`（float m_OutTangent）(偏移: 0xC)
- `int m_WeightedMode`（int m_Weighted模式）(偏移: 0x10)
- `float m_InWeight`（float m_InWeight）(偏移: 0x14)
- `float m_OutWeight`（float m_OutWeight）(偏移: 0x18)

### 方法 (8)

- `float get_time()`
  （float get_time（））
- `void set_time(float value)`
  （void set_time（float value））
- `float get_value()`
  （浮点数 获取_值（））
- `void set_value(float value)`
  （void 设置_值（浮点数 value））
- `float get_inTangent()`
  （float get_inTangent（））
- `void set_inTangent(float value)`
  （void set_inTangent（float value））
- `float get_outTangent()`
  （float get_outTangent（））
- `void set_outTangent(float value)`
  （void set_outTangent（float value））

---

## KillMarkAsset（击杀标记资产）

**继承**: ScriptableObject（脚本对象）

### 字段 (9)

- `Texture[] headShot`（Texture[] head射击）(偏移: 0xC)
- `Texture[] multilKill`（Texture[] multil击杀）(偏移: 0x10)
- `Texture[] multilKillEffect`（Texture[] multil击杀特效）(偏移: 0x14)
- `Texture grenade`（纹理 grenade）(偏移: 0x18)
- `Texture[] wallThrough`（Texture[] wallThrough）(偏移: 0x1C)
- `Texture knife`（纹理 knife）(偏移: 0x20)
- `Texture revenge`（纹理 revenge）(偏移: 0x24)
- `Texture firstKill`（纹理 first击杀）(偏移: 0x28)
- `Texture lastKill`（纹理 last击杀）(偏移: 0x2C)

---

## KnifeAttackData（近战武器Attack数据）

### 字段 (7)

- `float damage`（float damage）(偏移: 0x0)
- `float range`（浮点数 范围）(偏移: 0x4)
- `float angle`（float angle）(偏移: 0x8)
- `bool hitStun`（bool hit眩晕）(偏移: 0xC)
- `int damageTag`（int damage标签）(偏移: 0x10)
- `GameObject decal`（游戏对象 decal）(偏移: 0x14)
- `string decalSndName`（string decalSnd名称）(偏移: 0x18)

---

## KnownTerminals（KnownTerminals）

### 方法 (3)

- `byte[] get_linux()`
  （byte[] get_linux（））
- `byte[] get_xterm()`
  （byte[] get_xterm（））
- `byte[] get_ansi()`
  （byte[] get_ansi（））

---

## LODParameters（LODParameters）

**继承**: IEquatable<LODParameters>（IEquatable<LODParameters>）

### 字段 (5)

- `int m_IsOrthographic`（int m_是否Orthographic）(偏移: 0x0)
- `Vector3 m_CameraPosition`（三维向量 m_摄像机Position）(偏移: 0x4)
- `float m_FieldOfView`（float m_FieldOf视图）(偏移: 0x10)
- `float m_OrthoSize`（float m_Ortho大小）(偏移: 0x14)
- `int m_CameraPixelHeight`（int m_摄像机Pixel高度）(偏移: 0x18)

### 方法 (3)

- `bool Equals(LODParameters other)`
  （bool Equals（LODParameters other））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## LargeHeader（Large标题）

**继承**: PropertyAttribute（属性特性）

### 字段 (2)

- `string name`（字符串 名称）(偏移: 0x8)
- `string color`（string color）(偏移: 0xC)

---

## Latin1Encoding（Latin1Encoding）

**继承**: EncodingNLS, ISerializable（EncodingNLS, ISerializable）

### 字段 (1)

- `char[] arrayCharBestFit`（char[] arrayCharBestFit）(偏移: 0x0)

### 方法 (7)

- `int GetByteCount(char* chars, int charCount, EncoderNLS encoder)`
  （int 获取Byte数量（char* chars, int charCount, EncoderNLS encoder））
- `int GetBytes(char* chars, int charCount, byte* bytes, int byteCount, EncoderNLS encoder)`
  （整数 获取字节（字符* chars, 整数 charCount, 字节* bytes, 整数 byteCount, 编码器NLS encoder））
- `int GetCharCount(byte* bytes, int count, DecoderNLS decoder)`
  （int 获取Char数量（byte* bytes, int count, DecoderNLS decoder））
- `int GetChars(byte* bytes, int byteCount, char* chars, int charCount, DecoderNLS decoder)`
  （int 获取Chars（byte* bytes, int byteCount, char* chars, int charCount, DecoderNLS decoder））
- `int GetMaxByteCount(int charCount)`
  （整数 获取_最大字节数量（整数 charCount））
- `int GetMaxCharCount(int byteCount)`
  （整数 获取_最大字符数量（整数 byteCount））
- `char[] GetBestFitUnicodeToBytesData()`
  （char[] 获取BestFitUnicodeToBytes数据（））

---

## LayerConstant（层Constant）

### 字段 (20)

- `int Environment`（int Environment）(偏移: 0x0)
- `int AirWall`（int 空中Wall）(偏移: 0x4)
- `int HitBox`（int 命中Box）(偏移: 0x8)
- `int Water`（int Water）(偏移: 0xC)
- `int Entity`（int 实体）(偏移: 0x10)
- `int DeadEntity`（int Dead实体）(偏移: 0x14)
- `int GhostEntity`（int 幽灵实体）(偏移: 0x18)
- `int WayPoint`（int WayPoint）(偏移: 0x1C)
- `int CharacterModel`（int 角色模型）(偏移: 0x20)
- `int PlayerViewModel`（int 玩家视图模型）(偏移: 0x24)
- `int HideInPVandCV`（int 隐藏InPVand第一人称视角）(偏移: 0x28)
- `int LM_OnlyEnvironment`（int LM_OnlyEnvironment）(偏移: 0x2C)
- `int LM_GroundCheck`（int LM_地面检查）(偏移: 0x30)
- `int LM_GroundCheckWithWater`（int LM_地面检查WithWater）(偏移: 0x34)
- `int LM_GunShoot`（int LM_枪械射击）(偏移: 0x38)
- `int LM_KnifeAttack`（int LM_近战武器Attack）(偏移: 0x3C)
- `int LM_KnifeAttack2`（int LM_近战武器Attack2）(偏移: 0x40)
- `int LM_Entity`（int LM_实体）(偏移: 0x44)
- `int LM_ZoomTargetCheck`（int LM_瞄准目标检查）(偏移: 0x48)
- `int LM_AbsorbBody`（int LM_Absorb身体）(偏移: 0x4C)

---

## LayerGridGraph（层网格Graph）

**继承**: GridGraph, IUpdatableGraph（网格Graph, IUpdatableGraph）

### 字段 (8)

- `int layerCount`（int layer数量）(偏移: 0x158)
- `float mergeSpanRange`（float mergeSpan范围）(偏移: 0x15C)
- `float characterHeight`（float character高度）(偏移: 0x160)
- `int lastScannedWidth`（int lastScanned宽度）(偏移: 0x164)
- `int lastScannedDepth`（int lastScanned深度）(偏移: 0x168)
- `LevelGridNode[] nodes`（等级网格Node[] nodes）(偏移: 0x16C)
- `LayerGridGraph.HitComparer comparer`（层网格Graph.命中Comparer comparer）(偏移: 0x0)
- `LayerGridGraph.HeightSample[] heightSampleBuffer`（层网格Graph.高度Sample[] heightSample缓冲区）(偏移: 0x4)

### 方法 (27)

- `void OnDestroy()`
  （void 销毁时（））
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
- `List<GraphNode> GetNodesInRegion(Bounds b, GraphUpdateShape shape)`
  （List<GraphNode> 获取NodesInRegion（Bounds b, Graph更新Shape shape））
- `List<GraphNode> GetNodesInRegion(IntRect rect)`
  （List<GraphNode> 获取NodesInRegion（整数Rect rect））
- `int GetNodesInRegion(IntRect rect, GridNodeBase[] buffer)`
  （int 获取NodesInRegion（整数Rect rect, 网格节点Base[] buffer））
- `GridNodeBase GetNode(int x, int z)`
  （网格节点基础 获取节点（int x, int z））
- `GridNodeBase GetNode(int x, int z, int layer)`
  （网格节点基础 获取节点（int x, int z, int layer））
- `IEnumerable<Progress> ScanInternal()`
  （IEnumerable<进度> 扫描内部（））
- `LayerGridGraph.HeightSample[] SampleHeights(GraphCollision collision, float mergeSpanRange, Vector3 position, out int numHits)`
  （层网格Graph.高度Sample[] SampleHeights（GraphCollision collision, float mergeSpanRange, 三维向量 position, out int numHits））
- `void RecalculateCell(int x, int z, bool resetPenalties = True, bool resetTags = True)`
  （void RecalculateCell（int x, int z, bool resetPenalties = True, bool resetTags = True））
- `void AddLayers(int count)`
  （void 添加Layers（int count））
- `bool ErosionAnyFalseConnections(GraphNode baseNode)`
  （bool Erosion任意FalseConnections（Graph节点 baseNode））
- `void CalculateConnections(GridNodeBase baseNode)`
  （void 计算Connections（网格节点基础 baseNode））
- `void CalculateConnections(int x, int z, int layerIndex, LevelGridNode node)`
  （void 计算Connections（int x, int z, int layerIndex, 等级网格节点 node））
- `void CalculateConnections(int x, int z)`
  （void 计算Connections（int x, int z））
- `void CalculateConnections(int x, int z, int layerIndex)`
  （void 计算Connections（int x, int z, int layerIndex））
- `NNInfoInternal GetNearest(Vector3 position, NNConstraint constraint, GraphNode hint)`
  （NN信息内部 获取最近（三维向量 position, NN约束 constraint, 图节点 hint））
- `LevelGridNode GetNearestNode(Vector3 position, int x, int z, NNConstraint constraint)`
  （等级网格节点 获取Nearest节点（三维向量 position, int x, int z, NNConstraint constraint））
- `NNInfoInternal GetNearestForce(Vector3 position, NNConstraint constraint)`
  （NN信息内部 获取最近强制（三维向量 position, NN约束 constraint））
- `bool CheckConnection(LevelGridNode node, int dir)`
  （bool 检查连接（等级网格节点 node, int dir））
- `void SerializeExtraInfo(GraphSerializationContext ctx)`
  （void 序列化额外信息（图序列化上下文 ctx））
- `void DeserializeExtraInfo(GraphSerializationContext ctx)`
  （void 反序列化额外信息（图序列化上下文 ctx））
- `void PostDeserialization(GraphSerializationContext ctx)`
  （void 反序列化后（图序列化上下文 ctx））

---

## LayerGridGraph.HeightSample（层网格Graph.高度Sample）

### 字段 (4)

- `Vector3 position`（三维向量 位置）(偏移: 0x0)
- `RaycastHit hit`（Raycast命中 hit）(偏移: 0xC)
- `float height`（浮点数 高度）(偏移: 0x38)
- `bool walkable`（bool walkable）(偏移: 0x3C)

---

## LayerGridGraph.HitComparer（层网格Graph.命中Comparer）

**继承**: IComparer<RaycastHit>（IComparer<RaycastHit>）

### 方法 (1)

- `int Compare(RaycastHit a, RaycastHit b)`
  （int Compare（Raycast命中 a, Raycast命中 b））

---

## LayerGridGraphUpdate（层网格Graph更新）

**继承**: GraphUpdateObject（Graph更新对象）

### 字段 (2)

- `bool recalculateNodes`（bool recalculateNodes）(偏移: 0x48)
- `bool preserveExistingNodes`（bool preserveExistingNodes）(偏移: 0x49)

---

## LayerMask（层掩码）

### 字段 (1)

- `int m_Mask`（int m_掩码）(偏移: 0x0)

### 方法 (6)

- `int op_Implicit(LayerMask mask)`
  （int op_Implicit（层掩码 mask））
- `LayerMask op_Implicit(int intVal)`
  （层掩码 op_Implicit（int intVal））
- `int get_value()`
  （整数 获取_值（））
- `string LayerToName(int layer)`
  （string 层To名称（int layer））
- `int NameToLayer(string layerName)`
  （int 名称To层（string layerName））
- `int GetMask(string[] layerNames)`
  （int 获取掩码（string[] layerNames））

---

## LayerMaskExtensions（层掩码Extensions）

### 方法 (12)

- `bool Contains(LayerMask mask, int layer)`
  （bool Contains（层掩码 mask, int layer））
- `LayerMask Create(string[] layerNames)`
  （层掩码 创建（string[] layerNames））
- `LayerMask Create(int[] layerNumbers)`
  （层掩码 创建（int[] layerNumbers））
- `LayerMask NamesToMask(string[] layerNames)`
  （层掩码 NamesTo掩码（string[] layerNames））
- `LayerMask LayerNumbersToMask(int[] layerNumbers)`
  （层掩码 层NumbersTo掩码（int[] layerNumbers））
- `LayerMask Inverse(LayerMask original)`
  （层掩码 Inverse（层掩码 original））
- `LayerMask AddToMask(LayerMask original, string[] layerNames)`
  （层掩码 添加To掩码（层掩码 original, string[] layerNames））
- `LayerMask RemoveFromMask(LayerMask original, string[] layerNames)`
  （层掩码 移除From掩码（层掩码 original, string[] layerNames））
- `string[] MaskToNames(LayerMask original)`
  （string[] 掩码ToNames（层掩码 original））
- `int[] MaskToNumbers(LayerMask original)`
  （int[] 掩码ToNumbers（层掩码 original））
- `string MaskToString(LayerMask original)`
  （string 掩码To字符串（层掩码 original））
- `string MaskToString(LayerMask original, string delimiter)`
  （string 掩码To字符串（层掩码 original, string delimiter））

---

## LayoutElement（Layout元素）

**继承**: UIBehaviour, ILayoutElement, ILayoutIgnorer（界面Behaviour, ILayout元素, ILayoutIgnorer）

### 字段 (8)

- `bool m_IgnoreLayout`（bool m_IgnoreLayout）(偏移: 0xC)
- `float m_MinWidth`（float m_最小宽度）(偏移: 0x10)
- `float m_MinHeight`（float m_最小高度）(偏移: 0x14)
- `float m_PreferredWidth`（float m_Preferred宽度）(偏移: 0x18)
- `float m_PreferredHeight`（float m_Preferred高度）(偏移: 0x1C)
- `float m_FlexibleWidth`（float m_Flexible宽度）(偏移: 0x20)
- `float m_FlexibleHeight`（float m_Flexible高度）(偏移: 0x24)
- `int m_LayoutPriority`（int m_LayoutPriority）(偏移: 0x28)

### 方法 (24)

- `bool get_ignoreLayout()`
  （bool get_ignoreLayout（））
- `void set_ignoreLayout(bool value)`
  （void set_ignoreLayout（bool value））
- `void CalculateLayoutInputHorizontal()`
  （void 计算布局输入水平（））
- `void CalculateLayoutInputVertical()`
  （void 计算布局输入垂直（））
- `float get_minWidth()`
  （浮点数 获取_最小宽度（））
- `void set_minWidth(float value)`
  （void set_min宽度（float value））
- `float get_minHeight()`
  （浮点数 获取_最小高度（））
- `void set_minHeight(float value)`
  （void set_min高度（float value））
- `float get_preferredWidth()`
  （浮点数 获取_首选宽度（））
- `void set_preferredWidth(float value)`
  （void set_preferred宽度（float value））
- `float get_preferredHeight()`
  （浮点数 获取_首选高度（））
- `void set_preferredHeight(float value)`
  （void set_preferred高度（float value））
- `float get_flexibleWidth()`
  （浮点数 获取_弹性宽度（））
- `void set_flexibleWidth(float value)`
  （void set_flexible宽度（float value））
- `float get_flexibleHeight()`
  （浮点数 获取_弹性高度（））
- `void set_flexibleHeight(float value)`
  （void set_flexible高度（float value））
- `int get_layoutPriority()`
  （整数 获取_布局优先级（））
- `void set_layoutPriority(int value)`
  （void set_layoutPriority（int value））
- `void OnEnable()`
  （void 启用时（））
- `void OnTransformParentChanged()`
  （void 变换父级改变时（））
- `void OnDisable()`
  （void 禁用时（））
- `void OnDidApplyAnimationProperties()`
  （void 已应用动画属性时（））
- `void OnBeforeTransformParentChanged()`
  （void OnBefore变换父级Changed（））
- `void SetDirty()`
  （void 设置_脏（））

---

## LayoutGroup（Layout组）

**继承**: UIBehaviour, ILayoutElement, ILayoutGroup, ILayoutController（界面Behaviour, ILayout元素, ILayout组, ILayout控制器）

### 字段 (8)

- `RectOffset m_Padding`（RectOffset m_Padding）(偏移: 0xC)
- `TextAnchor m_ChildAlignment`（文本Anchor m_子级Alignment）(偏移: 0x10)
- `RectTransform m_Rect`（矩形变换 m_Rect）(偏移: 0x14)
- `DrivenRectTransformTracker m_Tracker`（驱动矩形变换跟踪器 m_跟踪器）(偏移: 0x18)
- `Vector2 m_TotalMinSize`（二维向量 m_Total最小大小）(偏移: 0x1C)
- `Vector2 m_TotalPreferredSize`（二维向量 m_TotalPreferred大小）(偏移: 0x24)
- `Vector2 m_TotalFlexibleSize`（二维向量 m_TotalFlexible大小）(偏移: 0x2C)
- `List<RectTransform> m_RectChildren`（List<RectTransform> m_RectChildren）(偏移: 0x34)

### 方法 (32)

- `RectOffset get_padding()`
  （RectOffset get_padding（））
- `void set_padding(RectOffset value)`
  （void set_padding（RectOffset value））
- `TextAnchor get_childAlignment()`
  （文本Anchor get_childAlignment（））
- `void set_childAlignment(TextAnchor value)`
  （void set_childAlignment（文本Anchor value））
- `RectTransform get_rectTransform()`
  （矩形变换 获取_矩形变换（））
- `List<RectTransform> get_rectChildren()`
  （List<RectTransform> get_rectChildren（））
- `void CalculateLayoutInputHorizontal()`
  （void 计算布局输入水平（））
- `float get_minWidth()`
  （浮点数 获取_最小宽度（））
- `float get_preferredWidth()`
  （浮点数 获取_首选宽度（））
- `float get_flexibleWidth()`
  （浮点数 获取_弹性宽度（））
- `float get_minHeight()`
  （浮点数 获取_最小高度（））
- `float get_preferredHeight()`
  （浮点数 获取_首选高度（））
- `float get_flexibleHeight()`
  （浮点数 获取_弹性高度（））
- `int get_layoutPriority()`
  （整数 获取_布局优先级（））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `void OnDidApplyAnimationProperties()`
  （void 已应用动画属性时（））
- `float GetTotalMinSize(int axis)`
  （float 获取Total最小大小（int axis））
- `float GetTotalPreferredSize(int axis)`
  （float 获取TotalPreferred大小（int axis））
- `float GetTotalFlexibleSize(int axis)`
  （float 获取TotalFlexible大小（int axis））
- `float GetStartOffset(int axis, float requiredSpaceWithoutPadding)`
  （float 获取开始Offset（int axis, float requiredSpaceWithoutPadding））
- `float GetAlignmentOnAxis(int axis)`
  （float 获取AlignmentOn轴（int axis））
- `void SetLayoutInputForAxis(float totalMin, float totalPreferred, float totalFlexible, int axis)`
  （void 集合Layout输入For轴（float totalMin, float totalPreferred, float totalFlexible, int axis））
- `void SetChildAlongAxis(RectTransform rect, int axis, float pos)`
  （void 集合子级Along轴（Rect变换 rect, int axis, float pos））
- `void SetChildAlongAxisWithScale(RectTransform rect, int axis, float pos, float scaleFactor)`
  （void 集合子级Along轴With缩放（Rect变换 rect, int axis, float pos, float scaleFactor））
- `void SetChildAlongAxis(RectTransform rect, int axis, float pos, float size)`
  （void 集合子级Along轴（Rect变换 rect, int axis, float pos, float size））
- `void SetChildAlongAxisWithScale(RectTransform rect, int axis, float pos, float size, float scaleFactor)`
  （void 集合子级Along轴With缩放（Rect变换 rect, int axis, float pos, float size, float scaleFactor））
- `bool get_isRootLayoutGroup()`
  （bool get_is根Layout组（））
- `void OnRectTransformDimensionsChange()`
  （void 矩形变换尺寸改变时（））
- `void OnTransformChildrenChanged()`
  （void 变换子级改变时（））
- `void SetDirty()`
  （void 设置_脏（））
- `IEnumerator DelayedSetDirty(RectTransform rectTransform)`
  （IEnumerator Delayed集合Dirty（Rect变换 rectTransform））

---

## LayoutRebuilder（LayoutRebuilder）

**继承**: ICanvasElement（I画布元素）

### 字段 (3)

- `RectTransform m_ToRebuild`（Rect变换 m_ToRebuild）(偏移: 0x8)
- `int m_CachedHashFromTransform`（int m_CachedHashFrom变换）(偏移: 0xC)
- `ObjectPool<LayoutRebuilder> s_Rebuilders`（对象Pool<LayoutRebuilder> s_Rebuilders）(偏移: 0x0)

### 方法 (18)

- `void Initialize(RectTransform controller)`
  （void 初始化（Rect变换 controller））
- `void Clear()`
  （void 清除（））
- `void ReapplyDrivenProperties(RectTransform driven)`
  （void ReapplyDrivenProperties（Rect变换 driven））
- `Transform get_transform()`
  （变换 获取_transform（））
- `bool IsDestroyed()`
  （bool 是否Destroyed（））
- `void StripDisabledBehavioursFromList(List<Component> components)`
  （void Strip禁用的BehavioursFrom列表（List<Component> components））
- `void ForceRebuildLayoutImmediate(RectTransform layoutRoot)`
  （void 强制RebuildLayoutImmediate（Rect变换 layoutRoot））
- `void Rebuild(CanvasUpdate executing)`
  （void 重建（画布更新 executing））
- `void PerformLayoutControl(RectTransform rect, UnityAction<Component> action)`
  （void 执行Layout控制（Rect变换 rect, Unity引擎Action<Component> action））
- `void PerformLayoutCalculation(RectTransform rect, UnityAction<Component> action)`
  （void 执行LayoutCalculation（Rect变换 rect, Unity引擎Action<Component> action））
- `void MarkLayoutForRebuild(RectTransform rect)`
  （void MarkLayoutForRebuild（Rect变换 rect））
- `bool ValidController(RectTransform layoutRoot, List<Component> comps)`
  （bool Valid控制器（Rect变换 layoutRoot, List<Component> comps））
- `void MarkLayoutRootForRebuild(RectTransform controller)`
  （void MarkLayout根ForRebuild（Rect变换 controller））
- `void LayoutComplete()`
  （void 布局完成（））
- `void GraphicUpdateComplete()`
  （void 图形更新完成（））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `string ToString()`
  （字符串 转字符串（））

---

## LayoutUtility（Layout工具）

### 方法 (11)

- `float GetMinSize(RectTransform rect, int axis)`
  （float 获取最小大小（Rect变换 rect, int axis））
- `float GetPreferredSize(RectTransform rect, int axis)`
  （float 获取Preferred大小（Rect变换 rect, int axis））
- `float GetFlexibleSize(RectTransform rect, int axis)`
  （float 获取Flexible大小（Rect变换 rect, int axis））
- `float GetMinWidth(RectTransform rect)`
  （float 获取最小宽度（Rect变换 rect））
- `float GetPreferredWidth(RectTransform rect)`
  （float 获取Preferred宽度（Rect变换 rect））
- `float GetFlexibleWidth(RectTransform rect)`
  （float 获取Flexible宽度（Rect变换 rect））
- `float GetMinHeight(RectTransform rect)`
  （float 获取最小高度（Rect变换 rect））
- `float GetPreferredHeight(RectTransform rect)`
  （float 获取Preferred高度（Rect变换 rect））
- `float GetFlexibleHeight(RectTransform rect)`
  （float 获取Flexible高度（Rect变换 rect））
- `float GetLayoutProperty(RectTransform rect, Func<ILayoutElement, float> property, float defaultValue)`
  （float 获取Layout属性（Rect变换 rect, Func<ILayout元素, float> property, float defaultValue））
- `float GetLayoutProperty(RectTransform rect, Func<ILayoutElement, float> property, float defaultValue, out ILayoutElement source)`
  （float 获取Layout属性（Rect变换 rect, Func<ILayout元素, float> property, float defaultValue, out ILayoutElement source））

---

## LazyHelpers（LazyHelpers）

### 字段 (1)

- `object PUBLICATION_ONLY_SENTINEL`（object PUBLICATION_ONLY_SENTINEL）(偏移: 0x0)

---

## LazyThreadSafetyMode（LazyThreadSafety模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Lease（Lease）

**继承**: MarshalByRefObject, ILease（MarshalByRef对象, ILease）

### 字段 (8)

- `DateTime _leaseExpireTime`（Date时间 _leaseExpire时间）(偏移: 0x10)
- `LeaseState _currentState`（Lease状态 _current状态）(偏移: 0x18)
- `TimeSpan _initialLeaseTime`（时间Span _initialLease时间）(偏移: 0x20)
- `TimeSpan _renewOnCallTime`（时间Span _renewOnCall时间）(偏移: 0x28)
- `TimeSpan _sponsorshipTimeout`（时间Span _sponsorship超时）(偏移: 0x30)
- `ArrayList _sponsors`（数组列表 _sponsors）(偏移: 0x38)
- `Queue _renewingSponsors`（队列 _renewingSponsors）(偏移: 0x3C)
- `Lease.RenewalDelegate _renewalDelegate`（Lease.Renewal委托 _renewal委托）(偏移: 0x40)

### 方法 (9)

- `TimeSpan get_CurrentLeaseTime()`
  （时间Span get_当前Lease时间（））
- `LeaseState get_CurrentState()`
  （Lease状态 get_当前状态（））
- `void Activate()`
  （void 激活（））
- `TimeSpan get_RenewOnCallTime()`
  （时间Span get_RenewOnCall时间（））
- `TimeSpan Renew(TimeSpan renewalTime)`
  （时间Span Renew（时间Span renewalTime））
- `void Unregister(ISponsor obj)`
  （void Unregister（ISponsor obj））
- `void UpdateState()`
  （void 更新状态（））
- `void CheckNextSponsor()`
  （void 检查下一个Sponsor（））
- `void ProcessSponsorResponse(object state, bool timedOut)`
  （void 处理Sponsor响应（object state, bool timedOut））

---

## Lease.RenewalDelegate（Lease.Renewal委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `TimeSpan Invoke(ILease lease)`
  （时间Span Invoke（ILease lease））
- `IAsyncResult BeginInvoke(ILease lease, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（ILease lease, 异步回调 callback, object object））
- `TimeSpan EndInvoke(IAsyncResult result)`
  （时间Span 结束Invoke（I异步Result result））

---

## LeaseManager（Lease管理器）

### 字段 (2)

- `ArrayList _objects`（数组列表 _objects）(偏移: 0x8)
- `Timer _timer`（计时器 _timer）(偏移: 0xC)

### 方法 (5)

- `void SetPollTime(TimeSpan timeSpan)`
  （void 集合Poll时间（时间Span timeSpan））
- `void TrackLifetime(ServerIdentity identity)`
  （void TrackLifetime（服务器Identity identity））
- `void StartManager()`
  （void 开始管理器（））
- `void StopManager()`
  （void 停止管理器（））
- `void ManageLeases(object state)`
  （void 管理Leases（object state））

---

## LeaseSink（LeaseSink）

**继承**: IMessageSink（IMessage接收器）

### 字段 (1)

- `IMessageSink _nextSink`（IMessageSink _nextSink）(偏移: 0x8)

### 方法 (3)

- `IMessage SyncProcessMessage(IMessage msg)`
  （IMessage 同步处理消息（IMessage msg））
- `IMessageCtrl AsyncProcessMessage(IMessage msg, IMessageSink replySink)`
  （IMessageCtrl 异步处理消息（IMessage msg, IMessageSink replySink））
- `void RenewLease(IMessage msg)`
  （void RenewLease（IMessage msg））

---

## LeaseState（Lease状态）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## LegIK（腿部IK）

**继承**: IK（IK反向运动学）

### 字段 (1)

- `IKSolverLeg solver`（IKSolver腿部 solver）(偏移: 0x1C)

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

## LegacyAIPath（LegacyAI路径）

**继承**: AIPath（AI路径）

### 字段 (7)

- `float forwardLook`（float forwardLook）(偏移: 0x10C)
- `bool closestOnPathCheck`（bool closestOn路径检查）(偏移: 0x110)
- `float minMoveScale`（float min移动缩放）(偏移: 0x114)
- `int currentWaypointIndex`（int currentWaypoint索引）(偏移: 0x118)
- `Vector3 lastFoundWaypointPosition`（三维向量 lastFoundWaypointPosition）(偏移: 0x11C)
- `float lastFoundWaypointTime`（float lastFoundWaypoint时间）(偏移: 0x128)
- `Vector3 targetDirection`（三维向量 target方向）(偏移: 0x12C)

### 方法 (7)

- `void Awake()`
  （void 唤醒（））
- `void OnPathComplete(Path _p)`
  （void On路径Complete（路径 _p））
- `void Update()`
  （void 更新（））
- `float XZSqrMagnitude(Vector3 a, Vector3 b)`
  （float XZSqrMagnitude（三维向量 a, 三维向量 b））
- `Vector3 CalculateVelocity(Vector3 currentPosition)`
  （三维向量 计算速度（三维向量 currentPosition））
- `void RotateTowards(Vector3 dir)`
  （void RotateTowards（三维向量 dir））
- `Vector3 CalculateTargetPoint(Vector3 p, Vector3 a, Vector3 b)`
  （三维向量 计算目标Point（三维向量 p, 三维向量 a, 三维向量 b））

---

## LegacyRVOController（LegacyRVO控制器）

**继承**: RVOController（RVO控制器）

### 字段 (3)

- `LayerMask mask`（层掩码 mask）(偏移: 0x54)
- `bool enableRotation`（布尔值 启用旋转）(偏移: 0x58)
- `float rotationSpeed`（浮点数 旋转速度）(偏移: 0x5C)

### 方法 (1)

- `void Update()`
  （void 更新（））

---

## LegacyRichAI（LegacyRichAI）

**继承**: RichAI（RichAI）

### 字段 (6)

- `bool preciseSlowdown`（bool preciseSlowdown）(偏移: 0x128)
- `bool raycastingForGroundPlacement`（bool raycastingFor地面Placement）(偏移: 0x129)
- `Vector3 velocity`（三维向量 速度）(偏移: 0x12C)
- `Vector3 lastTargetPoint`（三维向量 last目标Point）(偏移: 0x138)
- `Vector3 currentTargetDirection`（三维向量 current目标方向）(偏移: 0x144)
- `float deltaTime`（float delta时间）(偏移: 0x0)

### 方法 (4)

- `void Awake()`
  （void 唤醒（））
- `void Update()`
  （void 更新（））
- `Vector3 RaycastPosition(Vector3 position, float lasty)`
  （三维向量 RaycastPosition（三维向量 position, float lasty））
- `bool RotateTowards(Vector3 trotdir)`
  （bool RotateTowards（三维向量 trotdir））

---

## LensDistortion（LensDistortion）

**继承**: VolumeComponent, IPostProcessComponent（体积组件, I后处理组件）

### 字段 (5)

- `ClampedFloatParameter intensity`（钳制浮点数参数 强度）(偏移: 0x1C)
- `ClampedFloatParameter xMultiplier`（Clamped浮点数Parameter xMultiplier）(偏移: 0x20)
- `ClampedFloatParameter yMultiplier`（Clamped浮点数Parameter yMultiplier）(偏移: 0x24)
- `Vector2Parameter center`（二维向量Parameter center）(偏移: 0x28)
- `ClampedFloatParameter scale`（Clamped浮点数Parameter scale）(偏移: 0x2C)

### 方法 (2)

- `bool IsActive()`
  （布尔值 是否激活的（））
- `bool IsTileCompatible()`
  （布尔值 是否瓦片兼容（））

---

## LensSettings（LensSettings）

### 字段 (7)

- `LensSettings Default`（LensSettings 默认的）(偏移: 0x0)
- `float FieldOfView`（float FieldOf视图）(偏移: 0x0)
- `float OrthographicSize`（float Orthographic大小）(偏移: 0x4)
- `float NearClipPlane`（float Near弹匣Plane）(偏移: 0x8)
- `float FarClipPlane`（float Far弹匣Plane）(偏移: 0xC)
- `float Dutch`（float Dutch）(偏移: 0x10)
- `Vector2 LensShift`（二维向量 LensShift）(偏移: 0x24)

### 方法 (12)

- `bool get_Orthographic()`
  （bool get_Orthographic（））
- `void set_Orthographic(bool value)`
  （void set_Orthographic（bool value））
- `Vector2 get_SensorSize()`
  （二维向量 get_Sensor大小（））
- `void set_SensorSize(Vector2 value)`
  （void set_Sensor大小（二维向量 value））
- `float get_Aspect()`
  （float get_Aspect（））
- `bool get_IsPhysicalCamera()`
  （bool get_是否Physical摄像机（））
- `void set_IsPhysicalCamera(bool value)`
  （void set_是否Physical摄像机（bool value））
- `LensSettings FromCamera(Camera fromCamera)`
  （LensSettings From摄像机（摄像机 fromCamera））
- `void SnapshotCameraReadOnlyProperties(Camera camera)`
  （void Snapshot摄像机ReadOnlyProperties（摄像机 camera））
- `void SnapshotCameraReadOnlyProperties(ref LensSettings lens)`
  （void Snapshot摄像机ReadOnlyProperties（ref LensSettings lens））
- `LensSettings Lerp(LensSettings lensA, LensSettings lensB, float t)`
  （LensSettings Lerp（LensSettings lensA, LensSettings lensB, float t））
- `void Validate()`
  （void 验证（））

---

## Level2Map（Level2映射）

### 字段 (2)

- `byte Source`（byte Source）(偏移: 0x8)
- `byte Replace`（byte Replace）(偏移: 0x9)

---

## LevelGridNode（等级网格节点）

**继承**: GridNodeBase（网格节点基础）

### 字段 (3)

- `LayerGridGraph[] _gridGraphs`（层网格Graph[] _gridGraphs）(偏移: 0x0)
- `ulong gridConnections`（ulong gridConnections）(偏移: 0x30)
- `LayerGridGraph[] gridGraphs`（层网格Graph[] gridGraphs）(偏移: 0x4)

### 方法 (20)

- `LayerGridGraph GetGridGraph(uint graphIndex)`
  （层网格Graph 获取网格Graph（uint graphIndex））
- `void SetGridGraph(int graphIndex, LayerGridGraph graph)`
  （void 集合网格Graph（int graphIndex, 层网格Graph graph））
- `void ResetAllGridConnections()`
  （void 重置所有网格Connections（））
- `bool HasAnyGridConnections()`
  （bool 是否有任意网格Connections（））
- `bool get_HasConnectionsToAllEightNeighbours()`
  （bool get_是否有ConnectionsTo所有EightNeighbours（））
- `int get_LayerCoordinateInGrid()`
  （int get_层CoordinateIn网格（））
- `void set_LayerCoordinateInGrid(int value)`
  （void set_层CoordinateIn网格（int value））
- `void SetPosition(Int3 position)`
  （void 集合Position（Int3 position））
- `int GetGizmoHashCode()`
  （整数 获取辅助线哈希码（））
- `GridNodeBase GetNeighbourAlongDirection(int direction)`
  （网格节点基础 获取NeighbourAlong方向（int direction））
- `void ClearConnections(bool alsoReverse)`
  （void 清除连接（布尔值 也反向））
- `void GetConnections(Action<GraphNode> action)`
  （void 获取连接（Action<GraphNode> action））
- `bool GetConnection(int i)`
  （bool 获取连接（int i））
- `void SetConnectionValue(int dir, int value)`
  （void 集合连接值（int dir, int value））
- `int GetConnectionValue(int dir)`
  （int 获取连接值（int dir））
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

## LifetimeServices（LifetimeServices）

### 字段 (5)

- `TimeSpan _leaseManagerPollTime`（时间Span _lease管理器Poll时间）(偏移: 0x0)
- `TimeSpan _leaseTime`（时间Span _lease时间）(偏移: 0x8)
- `TimeSpan _renewOnCallTime`（时间Span _renewOnCall时间）(偏移: 0x10)
- `TimeSpan _sponsorshipTimeout`（时间Span _sponsorship超时）(偏移: 0x18)
- `LeaseManager _leaseManager`（Lease管理器 _lease管理器）(偏移: 0x20)

### 方法 (9)

- `TimeSpan get_LeaseManagerPollTime()`
  （时间Span get_Lease管理器Poll时间（））
- `void set_LeaseManagerPollTime(TimeSpan value)`
  （void set_Lease管理器Poll时间（时间Span value））
- `TimeSpan get_LeaseTime()`
  （时间Span get_Lease时间（））
- `void set_LeaseTime(TimeSpan value)`
  （void set_Lease时间（时间Span value））
- `TimeSpan get_RenewOnCallTime()`
  （时间Span get_RenewOnCall时间（））
- `void set_RenewOnCallTime(TimeSpan value)`
  （void set_RenewOnCall时间（时间Span value））
- `TimeSpan get_SponsorshipTimeout()`
  （时间Span get_Sponsorship超时（））
- `void set_SponsorshipTimeout(TimeSpan value)`
  （void set_Sponsorship超时（时间Span value））
- `void TrackLifetime(ServerIdentity identity)`
  （void TrackLifetime（服务器Identity identity））

---

## LiftGammaGain（LiftGammaGain）

**继承**: VolumeComponent, IPostProcessComponent（体积组件, I后处理组件）

### 字段 (3)

- `Vector4Parameter lift`（Vector4Parameter lift）(偏移: 0x1C)
- `Vector4Parameter gamma`（Vector4Parameter gamma）(偏移: 0x20)
- `Vector4Parameter gain`（Vector4Parameter gain）(偏移: 0x24)

### 方法 (2)

- `bool IsActive()`
  （布尔值 是否激活的（））
- `bool IsTileCompatible()`
  （布尔值 是否瓦片兼容（））

---

## Light（光照）

**继承**: Behaviour（行为）

### 字段 (1)

- `int m_BakedIndex`（int m_Baked索引）(偏移: 0xC)

### 方法 (21)

- `LightType get_type()`
  （光照类型 get_type（））
- `float get_spotAngle()`
  （float get_spot角度（））
- `float get_innerSpotAngle()`
  （float get_innerSpot角度（））
- `Color get_color()`
  （颜色 获取_颜色（））
- `void set_color(Color value)`
  （void 设置_颜色（颜色 value））
- `float get_intensity()`
  （float get_intensity（））
- `void set_intensity(float value)`
  （void set_intensity（float value））
- `float get_bounceIntensity()`
  （float get_bounceIntensity（））
- `float get_shadowBias()`
  （float get_shadowBias（））
- `float get_shadowNormalBias()`
  （float get_shadow法线Bias（））
- `float get_shadowNearPlane()`
  （float get_shadowNearPlane（））
- `float get_range()`
  （float get_range（））
- `LightBakingOutput get_bakingOutput()`
  （光照BakingOutput get_bakingOutput（））
- `LightShadows get_shadows()`
  （光照Shadows get_shadows（））
- `float get_shadowStrength()`
  （float get_shadowStrength（））
- `void set_shadowStrength(float value)`
  （void set_shadowStrength（float value））
- `float get_cookieSize()`
  （float get_cookie大小（））
- `Texture get_cookie()`
  （纹理 get_cookie（））
- `void get_color_Injected(out Color ret)`
  （void get_color_Injected（out Color ret））
- `void set_color_Injected(ref Color value)`
  （void set_color_Injected（ref Color value））
- `void get_bakingOutput_Injected(out LightBakingOutput ret)`
  （void get_bakingOutput_Injected（out LightBakingOutput ret））

---

## Light2D（Light2D）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (32)

- `Light2D.LightType m_LightType`（Light2D.光照类型 m_光照类型）(偏移: 0xC)
- `int m_BlendStyleIndex`（int m_BlendStyle索引）(偏移: 0x10)
- `float m_FalloffIntensity`（float m_FalloffIntensity）(偏移: 0x14)
- `Color m_Color`（颜色 m_颜色）(偏移: 0x18)
- `float m_Intensity`（float m_Intensity）(偏移: 0x28)
- `float m_LightVolumeOpacity`（float m_光照VolumeOpacity）(偏移: 0x2C)
- `int[] m_ApplyToSortingLayers`（int[] m_应用ToSortingLayers）(偏移: 0x30)
- `Sprite m_LightCookieSprite`（精灵 m_光照Cookie精灵）(偏移: 0x34)
- `bool m_UseNormalMap`（bool m_Use法线映射）(偏移: 0x38)
- `int m_LightOrder`（int m_光照Order）(偏移: 0x3C)
- `bool m_AlphaBlendOnOverlap`（bool m_透明度BlendOnOverlap）(偏移: 0x40)
- `float m_ShadowIntensity`（float m_ShadowIntensity）(偏移: 0x44)
- `float m_ShadowVolumeIntensity`（float m_ShadowVolumeIntensity）(偏移: 0x48)
- `int m_PreviousLightCookieSprite`（int m_上一个光照Cookie精灵）(偏移: 0x4C)
- `Mesh m_Mesh`（网格 m_网格）(偏移: 0x50)
- `Bounds m_LocalBounds`（Bounds m_本地的Bounds）(偏移: 0x54)
- `float m_PointLightInnerAngle`（float m_Point光照Inner角度）(偏移: 0x7C)
- `float m_PointLightOuterAngle`（float m_Point光照Outer角度）(偏移: 0x80)
- `float m_PointLightInnerRadius`（float m_Point光照InnerRadius）(偏移: 0x84)
- `float m_PointLightOuterRadius`（float m_Point光照OuterRadius）(偏移: 0x88)
- `float m_PointLightDistance`（float m_Point光照距离）(偏移: 0x8C)
- `Light2D.PointLightQuality m_PointLightQuality`（Light2D.Point光照Quality m_Point光照Quality）(偏移: 0x90)
- `int m_ShapeLightParametricSides`（int m_Shape光照ParametricSides）(偏移: 0x94)
- `float m_ShapeLightParametricAngleOffset`（float m_Shape光照Parametric角度Offset）(偏移: 0x98)
- `float m_ShapeLightParametricRadius`（float m_Shape光照ParametricRadius）(偏移: 0x9C)
- `float m_ShapeLightFalloffSize`（float m_Shape光照Falloff大小）(偏移: 0xA0)
- `Vector2 m_ShapeLightFalloffOffset`（二维向量 m_Shape光照FalloffOffset）(偏移: 0xA4)
- `Vector3[] m_ShapePath`（Vector3[] m_Shape路径）(偏移: 0xAC)
- `float m_PreviousShapeLightFalloffSize`（float m_上一个Shape光照Falloff大小）(偏移: 0xB0)
- `int m_PreviousShapeLightParametricSides`（int m_上一个Shape光照ParametricSides）(偏移: 0xB4)
- `float m_PreviousShapeLightParametricAngleOffset`（float m_上一个Shape光照Parametric角度Offset）(偏移: 0xB8)
- `float m_PreviousShapeLightParametricRadius`（float m_上一个Shape光照ParametricRadius）(偏移: 0xBC)

### 方法 (49)

- `int[] get_affectedSortingLayers()`
  （int[] get_affectedSortingLayers（））
- `int get_lightCookieSpriteInstanceID()`
  （int get_lightCookie精灵实例ID（））
- `BoundingSphere get_boundingSphere()`
  （BoundingSphere get_boundingSphere（））
- `void set_boundingSphere(BoundingSphere value)`
  （void set_boundingSphere（BoundingSphere value））
- `Mesh get_lightMesh()`
  （网格 get_light网格（））
- `Light2D.LightType get_lightType()`
  （Light2D.光照类型 get_light类型（））
- `void set_lightType(Light2D.LightType value)`
  （void set_light类型（Light2D.光照类型 value））
- `int get_blendStyleIndex()`
  （int get_blendStyle索引（））
- `void set_blendStyleIndex(int value)`
  （void set_blendStyle索引（int value））
- `float get_shadowIntensity()`
  （float get_shadowIntensity（））
- `void set_shadowIntensity(float value)`
  （void set_shadowIntensity（float value））
- `float get_shadowVolumeIntensity()`
  （float get_shadowVolumeIntensity（））
- `void set_shadowVolumeIntensity(float value)`
  （void set_shadowVolumeIntensity（float value））
- `Color get_color()`
  （颜色 获取_颜色（））
- `void set_color(Color value)`
  （void 设置_颜色（颜色 value））
- `float get_intensity()`
  （float get_intensity（））
- `void set_intensity(float value)`
  （void set_intensity（float value））
- `float get_volumeOpacity()`
  （float get_volumeOpacity（））
- `Sprite get_lightCookieSprite()`
  （精灵 get_lightCookie精灵（））
- `float get_falloffIntensity()`
  （float get_falloffIntensity（））
- `bool get_useNormalMap()`
  （bool get_use法线映射（））
- `bool get_alphaBlendOnOverlap()`
  （bool get_alphaBlendOnOverlap（））
- `int get_lightOrder()`
  （int get_lightOrder（））
- `void set_lightOrder(int value)`
  （void set_lightOrder（int value））
- `int GetTopMostLitLayer()`
  （int 获取顶部MostLit层（））
- `void UpdateMesh()`
  （void 更新网格（））
- `void UpdateBoundingSphere()`
  （void 更新BoundingSphere（））
- `bool IsLitLayer(int layer)`
  （bool 是否Lit层（int layer））
- `void Awake()`
  （void 唤醒（））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `void LateUpdate()`
  （void 延迟更新（））
- `float get_pointLightInnerAngle()`
  （float get_point光照Inner角度（））
- `void set_pointLightInnerAngle(float value)`
  （void set_point光照Inner角度（float value））
- `float get_pointLightOuterAngle()`
  （float get_point光照Outer角度（））
- `void set_pointLightOuterAngle(float value)`
  （void set_point光照Outer角度（float value））
- `float get_pointLightInnerRadius()`
  （float get_point光照InnerRadius（））
- `void set_pointLightInnerRadius(float value)`
  （void set_point光照InnerRadius（float value））
- `float get_pointLightOuterRadius()`
  （float get_point光照OuterRadius（））
- `void set_pointLightOuterRadius(float value)`
  （void set_point光照OuterRadius（float value））
- `float get_pointLightDistance()`
  （float get_point光照距离（））
- `Light2D.PointLightQuality get_pointLightQuality()`
  （Light2D.Point光照Quality get_point光照Quality（））
- `bool get_isPointLight()`
  （bool get_isPoint光照（））
- `int get_shapeLightParametricSides()`
  （int get_shape光照ParametricSides（））
- `float get_shapeLightParametricAngleOffset()`
  （float get_shape光照Parametric角度Offset（））
- `float get_shapeLightParametricRadius()`
  （float get_shape光照ParametricRadius（））
- `float get_shapeLightFalloffSize()`
  （float get_shape光照Falloff大小（））
- `Vector2 get_shapeLightFalloffOffset()`
  （二维向量 get_shape光照FalloffOffset（））
- `Vector3[] get_shapePath()`
  （Vector3[] get_shape路径（））

---

## Light2D.LightType（Light2D.光照类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Light2D.PointLightQuality（Light2D.Point光照Quality）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Light2DBlendStyle（Light2DBlendStyle）

### 字段 (6)

- `string name`（字符串 名称）(偏移: 0x0)
- `Light2DBlendStyle.TextureChannel maskTextureChannel`（Light2DBlendStyle.纹理Channel mask纹理Channel）(偏移: 0x4)
- `float renderTextureScale`（float render纹理缩放）(偏移: 0x8)
- `Light2DBlendStyle.BlendMode blendMode`（Light2DBlendStyle.Blend模式 blend模式）(偏移: 0xC)
- `Light2DBlendStyle.BlendFactors customBlendFactors`（Light2DBlendStyle.BlendFactors customBlendFactors）(偏移: 0x10)
- `RenderTargetHandle renderTargetHandle`（Render目标句柄 render目标句柄）(偏移: 0x1C)

### 方法 (6)

- `Vector2 get_blendFactors()`
  （二维向量 get_blendFactors（））
- `Light2DBlendStyle.MaskChannelFilter get_maskTextureChannelFilter()`
  （Light2DBlendStyle.掩码ChannelFilter get_mask纹理ChannelFilter（））
- `bool get_isDirty()`
  （bool get_isDirty（））
- `void set_isDirty(bool value)`
  （void set_isDirty（bool value））
- `bool get_hasRenderTarget()`
  （bool get_hasRender目标（））
- `void set_hasRenderTarget(bool value)`
  （void set_hasRender目标（bool value））

---

## Light2DBlendStyle.BlendFactors（Light2DBlendStyle.BlendFactors）

### 字段 (2)

- `float multiplicative`（float multiplicative）(偏移: 0x0)
- `float additive`（float additive）(偏移: 0x4)

---

## Light2DBlendStyle.BlendMode（Light2DBlendStyle.Blend模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Light2DBlendStyle.MaskChannelFilter（Light2DBlendStyle.掩码ChannelFilter）

### 方法 (4)

- `Vector4 get_mask()`
  （Vector4 get_mask（））
- `void set_mask(Vector4 value)`
  （void set_mask（Vector4 value））
- `Vector4 get_inverted()`
  （Vector4 get_inverted（））
- `void set_inverted(Vector4 value)`
  （void set_inverted（Vector4 value））

---

## Light2DBlendStyle.TextureChannel（Light2DBlendStyle.纹理Channel）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Light2DCullResult（Light2DCullResult）

**继承**: ILight2DCullResult（ILight2DCullResult）

### 字段 (1)

- `List<Light2D> m_VisibleLights`（List<Light2D> m_可见的Lights）(偏移: 0x8)

### 方法 (4)

- `List<Light2D> get_visibleLights()`
  （List<Light2D> get_visibleLights（））
- `bool IsSceneLit()`
  （bool 是否场景Lit（））
- `LightStats GetLightStatsByLayer(int layer)`
  （光照Stats 获取光照StatsBy层（int layer））
- `void SetupCulling(ref ScriptableCullingParameters cullingParameters, Camera camera)`
  （void SetupCulling（ref ScriptableCullingParameters cullingParameters, 摄像机 camera））

---

## Light2DLookupTexture（Light2DLookup纹理）

### 字段 (2)

- `Texture2D s_PointLightLookupTexture`（Texture2D s_Point光照Lookup纹理）(偏移: 0x0)
- `Texture2D s_FalloffLookupTexture`（Texture2D s_FalloffLookup纹理）(偏移: 0x4)

### 方法 (4)

- `Texture GetLightLookupTexture()`
  （纹理 获取光照Lookup纹理（））
- `Texture GetFalloffLookupTexture()`
  （纹理 获取FalloffLookup纹理（））
- `Texture2D CreatePointLightLookupTexture()`
  （Texture2D 创建Point光照Lookup纹理（））
- `Texture2D CreateFalloffLookupTexture()`
  （Texture2D 创建FalloffLookup纹理（））

---

## Light2DManager（Light2D管理器）

### 字段 (1)

- `SortingLayer[] s_SortingLayers`（SortingLayer[] s_SortingLayers）(偏移: 0x0)

### 方法 (7)

- `List<Light2D> get_lights()`
  （List<Light2D> get_lights（））
- `void RegisterLight(Light2D light)`
  （void Register光照（Light2D light））
- `void DeregisterLight(Light2D light)`
  （void Deregister光照（Light2D light））
- `void ErrorIfDuplicateGlobalLight(Light2D light)`
  （void ErrorIfDuplicate全局的光照（Light2D light））
- `bool GetGlobalColor(int sortingLayerIndex, int blendStyleIndex, out Color color)`
  （bool 获取全局的颜色（int sortingLayerIndex, int blendStyleIndex, out Color color））
- `bool ContainsDuplicateGlobalLight(int sortingLayerIndex, int blendStyleIndex)`
  （bool ContainsDuplicate全局的光照（int sortingLayerIndex, int blendStyleIndex））
- `SortingLayer[] GetCachedSortingLayer()`
  （SortingLayer[] 获取CachedSorting层（））

---

## LightBakingOutput（光照BakingOutput）

### 字段 (5)

- `int probeOcclusionLightIndex`（int probeOcclusion光照索引）(偏移: 0x0)
- `int occlusionMaskChannel`（int occlusion掩码Channel）(偏移: 0x4)
- `LightmapBakeType lightmapBakeType`（LightmapBake类型 lightmapBake类型）(偏移: 0x8)
- `MixedLightingMode mixedLightingMode`（MixedLighting模式 mixedLighting模式）(偏移: 0xC)
- `bool isBaked`（bool isBaked）(偏移: 0x10)

---

## LightData（光照数据）

### 字段 (6)

- `int mainLightIndex`（int main光照索引）(偏移: 0x0)
- `int additionalLightsCount`（int additionalLights数量）(偏移: 0x4)
- `int maxPerObjectAdditionalLightsCount`（int maxPer对象AdditionalLights数量）(偏移: 0x8)
- `NativeArray<VisibleLight> visibleLights`（NativeArray<可见的Light> visibleLights）(偏移: 0xC)
- `bool shadeAdditionalLightsPerVertex`（bool shadeAdditionalLightsPerVertex）(偏移: 0x18)
- `bool supportsMixedLighting`（bool supportsMixedLighting）(偏移: 0x19)

---

## LightDataGI（光照数据GI）

### 字段 (16)

- `int instanceID`（整数 实例ID）(偏移: 0x0)
- `int cookieID`（int cookieID）(偏移: 0x4)
- `float cookieScale`（float cookie缩放）(偏移: 0x8)
- `LinearColor color`（线性颜色 color）(偏移: 0xC)
- `LinearColor indirectColor`（线性颜色 间接颜色）(偏移: 0x1C)
- `Quaternion orientation`（四元数 朝向）(偏移: 0x2C)
- `Vector3 position`（三维向量 位置）(偏移: 0x3C)
- `float range`（浮点数 范围）(偏移: 0x48)
- `float coneAngle`（float cone角度）(偏移: 0x4C)
- `float innerConeAngle`（float innerCone角度）(偏移: 0x50)
- `float shape0`（float shape0）(偏移: 0x54)
- `float shape1`（float shape1）(偏移: 0x58)
- `LightType type`（光照类型 type）(偏移: 0x5C)
- `LightMode mode`（光照模式 mode）(偏移: 0x5D)
- `byte shadow`（byte shadow）(偏移: 0x5E)
- `FalloffType falloff`（衰减类型 falloff）(偏移: 0x5F)

### 方法 (6)

- `void Init(ref DirectionalLight light, ref Cookie cookie)`
  （void 初始化（ref DirectionalLight light, ref Cookie cookie））
- `void Init(ref PointLight light, ref Cookie cookie)`
  （void 初始化（ref PointLight light, ref Cookie cookie））
- `void Init(ref SpotLight light, ref Cookie cookie)`
  （void 初始化（ref SpotLight light, ref Cookie cookie））
- `void Init(ref RectangleLight light, ref Cookie cookie)`
  （void 初始化（ref RectangleLight light, ref Cookie cookie））
- `void Init(ref DiscLight light, ref Cookie cookie)`
  （void 初始化（ref DiscLight light, ref Cookie cookie））
- `void InitNoBake(int lightInstanceID)`
  （void 初始化NoBake（int lightInstanceID））

---

## LightFlag（光照标志）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## LightMode（光照模式）

### 字段 (1)

- `byte value__`（字节 值__）(偏移: 0x0)

---

## LightProbes（光照Probes）

**继承**: Object（对象）

### 字段 (2)

- `Action tetrahedralizationCompleted`（动作 tetrahedralizationCompleted）(偏移: 0x0)
- `Action needsRetetrahedralization`（动作 needsRetetrahedralization）(偏移: 0x4)

### 方法 (2)

- `void Internal_CallTetrahedralizationCompletedFunction()`
  （void Internal_CallTetrahedralizationCompletedFunction（））
- `void Internal_CallNeedsRetetrahedralizationFunction()`
  （void Internal_CallNeedsRetetrahedralizationFunction（））

---

## LightRenderingMode（光照Rendering模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## LightShadows（光照Shadows）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## LightStats（光照Stats）

### 字段 (4)

- `int totalLights`（int totalLights）(偏移: 0x0)
- `int totalNormalMapUsage`（int total法线映射Usage）(偏移: 0x4)
- `int totalVolumetricUsage`（int totalVolumetricUsage）(偏移: 0x8)
- `uint blendStylesUsed`（uint blendStylesUsed）(偏移: 0xC)

---

## LightType（光照类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## LightType（光照类型）

### 字段 (1)

- `byte value__`（字节 值__）(偏移: 0x0)

---

## LightUtility（光照工具）

### 方法 (7)

- `bool CheckForChange(int a, ref int b)`
  （bool 检查ForChange（int a, ref int b））
- `bool CheckForChange(float a, ref float b)`
  （bool 检查ForChange（float a, ref float b））
- `bool CheckForChange(bool a, ref bool b)`
  （bool 检查ForChange（bool a, ref bool b））
- `Bounds GenerateParametricMesh(Mesh mesh, float radius, float falloffDistance, float angle, int sides)`
  （Bounds GenerateParametric网格（网格 mesh, float radius, float falloffDistance, float angle, int sides））
- `Bounds GenerateSpriteMesh(Mesh mesh, Sprite sprite)`
  （Bounds Generate精灵网格（网格 mesh, 精灵 sprite））
- `List<Vector2> GetFalloffShape(Vector3[] shapePath)`
  （List<Vector2> 获取FalloffShape（Vector3[] shapePath））
- `Bounds GenerateShapeMesh(Mesh mesh, Vector3[] shapePath, float falloffDistance)`
  （Bounds GenerateShape网格（网格 mesh, Vector3[] shapePath, float falloffDistance））

---

## LightUtility.ParametricLightMeshVertex（光照Utility.Parametric光照网格Vertex）

### 字段 (3)

- `float3 position`（float3 position）(偏移: 0x0)
- `Color color`（颜色 color）(偏移: 0xC)
- `VertexAttributeDescriptor[] VertexLayout`（VertexAttributeDescriptor[] VertexLayout）(偏移: 0x0)

---

## LightUtility.SpriteLightMeshVertex（光照Utility.精灵光照网格Vertex）

### 字段 (4)

- `Vector3 position`（三维向量 位置）(偏移: 0x0)
- `Color color`（颜色 color）(偏移: 0xC)
- `Vector2 uv`（二维向量 uv）(偏移: 0x1C)
- `VertexAttributeDescriptor[] VertexLayout`（VertexAttributeDescriptor[] VertexLayout）(偏移: 0x0)

---

## LightingSettings（LightingSettings）

**继承**: Object（对象）

### 方法 (1)

- `void LightingSettingsDontStripMe()`
  （void LightingSettingsDontStripMe（））

---

## LightmapBakeType（LightmapBake类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## LightmapType（Lightmap类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## LightmapperUtils（LightmapperUtils）

### 方法 (11)

- `LightMode Extract(LightmapBakeType baketype)`
  （光照模式 Extract（LightmapBake类型 baketype））
- `LinearColor ExtractIndirect(Light l)`
  （Linear颜色 ExtractIndirect（光照 l））
- `float ExtractInnerCone(Light l)`
  （float ExtractInnerCone（光照 l））
- `Color ExtractColorTemperature(Light l)`
  （颜色 Extract颜色Temperature（光照 l））
- `void ApplyColorTemperature(Color cct, ref LinearColor lightColor)`
  （void 应用颜色Temperature（颜色 cct, ref LinearColor lightColor））
- `void Extract(Light l, ref DirectionalLight dir)`
  （void Extract（光照 l, ref DirectionalLight dir））
- `void Extract(Light l, ref PointLight point)`
  （void Extract（光照 l, ref PointLight point））
- `void Extract(Light l, ref SpotLight spot)`
  （void Extract（光照 l, ref SpotLight spot））
- `void Extract(Light l, ref RectangleLight rect)`
  （void Extract（光照 l, ref RectangleLight rect））
- `void Extract(Light l, ref DiscLight disc)`
  （void Extract（光照 l, ref DiscLight disc））
- `void Extract(Light l, out Cookie cookie)`
  （void Extract（光照 l, out Cookie cookie））

---

## Lightmapping（Lightmapping）

### 字段 (2)

- `Lightmapping.RequestLightsDelegate s_DefaultDelegate`（Lightmapping.请求Lights委托 s_默认的委托）(偏移: 0x0)
- `Lightmapping.RequestLightsDelegate s_RequestLightsDelegate`（Lightmapping.请求Lights委托 s_请求Lights委托）(偏移: 0x4)

### 方法 (4)

- `void SetDelegate(Lightmapping.RequestLightsDelegate del)`
  （void 集合委托（Lightmapping.请求Lights委托 del））
- `Lightmapping.RequestLightsDelegate GetDelegate()`
  （Lightmapping.请求Lights委托 获取委托（））
- `void ResetDelegate()`
  （void 重置委托（））
- `void RequestLights(Light[] lights, IntPtr outLightsPtr, int outLightsCount)`
  （void 请求Lights（Light[] lights, 整数Ptr outLightsPtr, int outLightsCount））

---

## Lightmapping.RequestLightsDelegate（Lightmapping.请求Lights委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(Light[] requests, NativeArray<LightDataGI> lightsOutput)`
  （void Invoke（Light[] requests, NativeArray<光照数据GI> lightsOutput））
- `IAsyncResult BeginInvoke(Light[] requests, NativeArray<LightDataGI> lightsOutput, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Light[] requests, NativeArray<光照数据GI> lightsOutput, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## LightmapsMode（Lightmaps模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## LimbIK（LimbIK）

**继承**: IK（IK反向运动学）

### 字段 (1)

- `IKSolverLimb solver`（IKSolverLimb solver）(偏移: 0x1C)

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

## Line（Line）

### 字段 (2)

- `Vector2 point`（二维向量 point）(偏移: 0x0)
- `Vector2 dir`（二维向量 dir）(偏移: 0x8)

---

## LineRenderer（Line渲染器）

**继承**: Renderer（渲染器）

### 方法 (5)

- `void SetColors(Color start, Color end)`
  （void 集合Colors（颜色 start, 颜色 end））
- `void set_startColor(Color value)`
  （void set_start颜色（颜色 value））
- `void set_endColor(Color value)`
  （void set_end颜色（颜色 value））
- `void set_startColor_Injected(ref Color value)`
  （void set_startColor_Injected（ref Color value））
- `void set_endColor_Injected(ref Color value)`
  （void set_endColor_Injected（ref Color value））

---

## LinearColor（Linear颜色）

### 字段 (4)

- `float m_red`（float m_red）(偏移: 0x0)
- `float m_green`（float m_green）(偏移: 0x4)
- `float m_blue`（float m_blue）(偏移: 0x8)
- `float m_intensity`（float m_intensity）(偏移: 0xC)

### 方法 (8)

- `float get_red()`
  （float get_red（））
- `void set_red(float value)`
  （void set_red（float value））
- `float get_green()`
  （float get_green（））
- `void set_green(float value)`
  （void set_green（float value））
- `float get_blue()`
  （float get_blue（））
- `void set_blue(float value)`
  （void set_blue（float value））
- `LinearColor Convert(Color color, float intensity)`
  （Linear颜色 转换（颜色 color, float intensity））
- `LinearColor Black()`
  （Linear颜色 Black（））

---

## LinearDecoder（LinearDecoder）

**继承**: ABSPathDecoder（ABS路径Decoder）

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

## LinkBehaviour（LinkBehaviour）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## LinkedVoxelSpan（LinkedVoxelSpan）

### 字段 (4)

- `uint bottom`（uint bottom）(偏移: 0x0)
- `uint top`（uint top）(偏移: 0x4)
- `int next`（int next）(偏移: 0x8)
- `int area`（整数 面积）(偏移: 0xC)

---

## ListDictionary（列表字典）

**继承**: IDictionary, ICollection, IEnumerable（I字典, ICollection, IEnumerable）

### 字段 (5)

- `ListDictionary.DictionaryNode head`（列表Dictionary.字典节点 head）(偏移: 0x8)
- `int version`（整数 版本）(偏移: 0xC)
- `int count`（整数 数量）(偏移: 0x10)
- `IComparer comparer`（I比较器 comparer）(偏移: 0x14)
- `object _syncRoot`（对象 _同步根）(偏移: 0x18)

### 方法 (8)

- `object get_Item(object key)`
  （对象 获取_项（对象 key））
- `void set_Item(object key, object value)`
  （void 设置_项（对象 key, 对象 value））
- `int get_Count()`
  （整数 获取_数量（））
- `object get_SyncRoot()`
  （对象 获取_同步根（））
- `bool Contains(object key)`
  （布尔值 包含（对象 key））
- `void CopyTo(Array array, int index)`
  （void 复制到（数组 array, 整数 index））
- `IDictionaryEnumerator GetEnumerator()`
  （I字典枚举器 获取枚举器（））
- `void Remove(object key)`
  （void 移除（对象 key））

---

## ListDictionary.DictionaryNode（列表Dictionary.字典节点）

### 字段 (3)

- `object key`（对象 key）(偏移: 0x8)
- `object value`（对象 value）(偏移: 0xC)
- `ListDictionary.DictionaryNode next`（列表Dictionary.字典节点 next）(偏移: 0x10)

---

## ListDictionary.NodeEnumerator（列表Dictionary.节点Enumerator）

**继承**: IDictionaryEnumerator, IEnumerator（I字典枚举器, IEnumerator）

### 字段 (4)

- `ListDictionary list`（列表字典 list）(偏移: 0x8)
- `ListDictionary.DictionaryNode current`（列表Dictionary.字典节点 current）(偏移: 0xC)
- `int version`（整数 版本）(偏移: 0x10)
- `bool start`（bool start）(偏移: 0x14)

### 方法 (6)

- `object get_Current()`
  （对象 获取_当前（））
- `DictionaryEntry get_Entry()`
  （字典项 获取_项（））
- `object get_Key()`
  （对象 获取_键（））
- `object get_Value()`
  （对象 获取_值（））
- `bool MoveNext()`
  （布尔值 移动下一个（））
- `void Reset()`
  （void 重置（））

---

## ListDictionaryInternal（列表字典内部的）

**继承**: IDictionary, ICollection, IEnumerable（I字典, ICollection, IEnumerable）

### 字段 (4)

- `ListDictionaryInternal.DictionaryNode head`（列表字典Internal.字典节点 head）(偏移: 0x8)
- `int version`（整数 版本）(偏移: 0xC)
- `int count`（整数 数量）(偏移: 0x10)
- `object _syncRoot`（对象 _同步根）(偏移: 0x14)

### 方法 (8)

- `object get_Item(object key)`
  （对象 获取_项（对象 key））
- `void set_Item(object key, object value)`
  （void 设置_项（对象 key, 对象 value））
- `int get_Count()`
  （整数 获取_数量（））
- `object get_SyncRoot()`
  （对象 获取_同步根（））
- `bool Contains(object key)`
  （布尔值 包含（对象 key））
- `void CopyTo(Array array, int index)`
  （void 复制到（数组 array, 整数 index））
- `IDictionaryEnumerator GetEnumerator()`
  （I字典枚举器 获取枚举器（））
- `void Remove(object key)`
  （void 移除（对象 key））

---

## ListDictionaryInternal.DictionaryNode（列表字典Internal.字典节点）

### 字段 (3)

- `object key`（对象 key）(偏移: 0x8)
- `object value`（对象 value）(偏移: 0xC)
- `ListDictionaryInternal.DictionaryNode next`（列表字典Internal.字典节点 next）(偏移: 0x10)

---

## ListDictionaryInternal.NodeEnumerator（列表字典Internal.节点Enumerator）

**继承**: IDictionaryEnumerator, IEnumerator（I字典枚举器, IEnumerator）

### 字段 (4)

- `ListDictionaryInternal list`（列表字典内部的 list）(偏移: 0x8)
- `ListDictionaryInternal.DictionaryNode current`（列表字典Internal.字典节点 current）(偏移: 0xC)
- `int version`（整数 版本）(偏移: 0x10)
- `bool start`（bool start）(偏移: 0x14)

### 方法 (6)

- `object get_Current()`
  （对象 获取_当前（））
- `DictionaryEntry get_Entry()`
  （字典项 获取_项（））
- `object get_Key()`
  （对象 获取_键（））
- `object get_Value()`
  （对象 获取_值（））
- `bool MoveNext()`
  （布尔值 移动下一个（））
- `void Reset()`
  （void 重置（））

---

## LoadHint（加载Hint）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## LoadSceneMode（加载场景模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## LoadSceneParameters（加载场景Parameters）

### 字段 (2)

- `LoadSceneMode m_LoadSceneMode`（加载场景模式 m_加载场景模式）(偏移: 0x0)
- `LocalPhysicsMode m_LocalPhysicsMode`（本地的物理模式 m_本地的物理模式）(偏移: 0x4)

---

## LocalAppContextSwitches（本地的AppContextSwitches）

### 字段 (1)

- `bool MemberDescriptorEqualsReturnsFalseIfEquivalent`（bool MemberDescriptorEqualsReturnsFalseIfEquivalent）(偏移: 0x0)

---

## LocalBuilder（本地的构建器）

**继承**: LocalVariableInfo（本地的Variable信息）

### 字段 (4)

- `string name`（字符串 名称）(偏移: 0x10)
- `ILGenerator ilgen`（ILGenerator ilgen）(偏移: 0x14)
- `int startOffset`（int startOffset）(偏移: 0x18)
- `int endOffset`（int endOffset）(偏移: 0x1C)

---

## LocalDataStore（本地的数据商店）

### 字段 (2)

- `LocalDataStoreElement[] m_DataTable`（本地的数据商店Element[] m_数据Table）(偏移: 0x8)
- `LocalDataStoreMgr m_Manager`（本地的数据商店Mgr m_管理器）(偏移: 0xC)

### 方法 (5)

- `void Dispose()`
  （void 释放（））
- `object GetData(LocalDataStoreSlot slot)`
  （object 获取数据（本地的数据商店槽位 slot））
- `void SetData(LocalDataStoreSlot slot, object data)`
  （void 集合数据（本地的数据商店槽位 slot, object data））
- `void FreeData(int slot, long cookie)`
  （void Free数据（int slot, long cookie））
- `LocalDataStoreElement PopulateElement(LocalDataStoreSlot slot)`
  （本地的数据商店元素 Populate元素（本地的数据商店槽位 slot））

---

## LocalDataStoreElement（本地的数据商店元素）

### 字段 (2)

- `object m_value`（object m_value）(偏移: 0x8)
- `long m_cookie`（long m_cookie）(偏移: 0x10)

### 方法 (3)

- `object get_Value()`
  （对象 获取_值（））
- `void set_Value(object value)`
  （void set_值（object value））
- `long get_Cookie()`
  （long get_Cookie（））

---

## LocalDataStoreHolder（本地的数据商店Holder）

### 字段 (1)

- `LocalDataStore m_Store`（本地的数据商店 m_商店）(偏移: 0x8)

### 方法 (2)

- `void Finalize()`
  （void 终结（））
- `LocalDataStore get_Store()`
  （本地的数据商店 get_商店（））

---

## LocalDataStoreMgr（本地的数据商店Mgr）

### 字段 (4)

- `bool[] m_SlotInfoTable`（bool[] m_槽位信息Table）(偏移: 0x8)
- `int m_FirstAvailableSlot`（int m_第一个Available槽位）(偏移: 0xC)
- `List<LocalDataStore> m_ManagedLocalDataStores`（List<本地的数据Store> m_Managed本地的数据Stores）(偏移: 0x10)
- `long m_CookieGenerator`（long m_CookieGenerator）(偏移: 0x18)

### 方法 (9)

- `LocalDataStoreHolder CreateLocalDataStore()`
  （本地的数据商店Holder 创建本地的数据商店（））
- `void DeleteLocalDataStore(LocalDataStore store)`
  （void Delete本地的数据商店（本地的数据商店 store））
- `LocalDataStoreSlot AllocateDataSlot()`
  （本地的数据商店槽位 Allocate数据槽位（））
- `LocalDataStoreSlot AllocateNamedDataSlot(string name)`
  （本地的数据商店槽位 AllocateNamed数据槽位（string name））
- `LocalDataStoreSlot GetNamedDataSlot(string name)`
  （本地的数据商店槽位 获取Named数据槽位（string name））
- `void FreeNamedDataSlot(string name)`
  （void FreeNamed数据槽位（string name））
- `void FreeDataSlot(int slot, long cookie)`
  （void Free数据槽位（int slot, long cookie））
- `void ValidateSlot(LocalDataStoreSlot slot)`
  （void 验证槽位（本地的数据商店槽位 slot））
- `int GetSlotTableLength()`
  （int 获取槽位TableLength（））

---

## LocalDataStoreSlot（本地的数据商店槽位）

### 字段 (3)

- `LocalDataStoreMgr m_mgr`（本地的数据商店Mgr m_mgr）(偏移: 0x8)
- `int m_slot`（int m_slot）(偏移: 0xC)
- `long m_cookie`（long m_cookie）(偏移: 0x10)

### 方法 (4)

- `LocalDataStoreMgr get_Manager()`
  （本地的数据商店Mgr get_管理器（））
- `int get_Slot()`
  （int get_槽位（））
- `long get_Cookie()`
  （long get_Cookie（））
- `void Finalize()`
  （void 终结（））

---

## LocalMinima（本地的Minima）

### 字段 (4)

- `long Y`（long Y）(偏移: 0x8)
- `TEdge LeftBound`（TEdge 左Bound）(偏移: 0x10)
- `TEdge RightBound`（TEdge 右Bound）(偏移: 0x14)
- `LocalMinima Next`（本地的Minima 下一个）(偏移: 0x18)

---

## LocalPhysicsMode（本地的物理模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## LocalVariableInfo（本地的Variable信息）

### 字段 (3)

- `Type type`（类型 type）(偏移: 0x8)
- `bool is_pinned`（bool is_pinned）(偏移: 0xC)
- `ushort position`（ushort position）(偏移: 0xE)

### 方法 (1)

- `string ToString()`
  （字符串 转字符串（））

---

## Locale（Locale）

### 方法 (2)

- `string GetText(string msg)`
  （string 获取文本（string msg））
- `string GetText(string fmt, object[] args)`
  （string 获取文本（string fmt, object[] args））

---

## LockVelocityArea（Lock速度Area）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (3)

- `float speed`（浮点数 速度）(偏移: 0xC)
- `float lockTime`（float lock时间）(偏移: 0x10)
- `bool saveVelY`（bool saveVelY）(偏移: 0x14)

### 方法 (1)

- `void OnTriggerStay(Collider other)`
  （void 触发器停留时（碰撞器 other））

---

## LogBehaviour（LogBehaviour）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## LogOption（LogOption）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## LogType（Log类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Logger（Logger）

**继承**: ILogger, ILogHandler（ILogger, ILog处理器）

### 方法 (14)

- `ILogHandler get_logHandler()`
  （ILog处理器 get_log处理器（））
- `void set_logHandler(ILogHandler value)`
  （void set_log处理器（ILog处理器 value））
- `bool get_logEnabled()`
  （bool get_log启用的（））
- `void set_logEnabled(bool value)`
  （void set_log启用的（bool value））
- `LogType get_filterLogType()`
  （Log类型 get_filterLog类型（））
- `void set_filterLogType(LogType value)`
  （void set_filterLog类型（Log类型 value））
- `bool IsLogTypeAllowed(LogType logType)`
  （bool 是否Log类型Allowed（Log类型 logType））
- `string GetString(object message)`
  （string 获取字符串（object message））
- `void Log(LogType logType, object message)`
  （void Log（Log类型 logType, object message））
- `void Log(LogType logType, object message, Object context)`
  （void Log（Log类型 logType, object message, 对象 context））
- `void LogError(string tag, object message)`
  （void LogError（string tag, object message））
- `void LogException(Exception exception, Object context)`
  （void LogException（Exception exception, 对象 context））
- `void LogFormat(LogType logType, string format, object[] args)`
  （void Log格式化（Log类型 logType, string format, object[] args））
- `void LogFormat(LogType logType, Object context, string format, object[] args)`
  （void Log格式化（Log类型 logType, 对象 context, string format, object[] args））

---

## LogicalCallContext（LogicalCallContext）

**继承**: ISerializable, ICloneable（ISerializable, ICloneable）

### 字段 (8)

- `Type s_callContextType`（类型 s_callContext类型）(偏移: 0x0)
- `Hashtable m_Datastore`（Hashtable m_Datastore）(偏移: 0x8)
- `CallContextRemotingData m_RemotingData`（CallContextRemoting数据 m_Remoting数据）(偏移: 0xC)
- `CallContextSecurityData m_SecurityData`（CallContextSecurity数据 m_Security数据）(偏移: 0x10)
- `object m_HostContext`（object m_HostContext）(偏移: 0x14)
- `bool m_IsCorrelationMgr`（bool m_是否CorrelationMgr）(偏移: 0x18)
- `Header[] _sendHeaders`（Header[] _sendHeaders）(偏移: 0x1C)
- `Header[] _recvHeaders`（Header[] _recvHeaders）(偏移: 0x20)

### 方法 (6)

- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））
- `object Clone()`
  （对象 克隆（））
- `void Merge(LogicalCallContext lc)`
  （void Merge（LogicalCallContext lc））
- `bool get_HasInfo()`
  （布尔值 获取_是否有信息（））
- `bool get_HasUserData()`
  （bool get_是否有User数据（））
- `Hashtable get_Datastore()`
  （Hashtable get_Datastore（））

---

## LogicalCallContext.Reader（LogicalCallContext.读取器）

### 字段 (1)

- `LogicalCallContext m_ctx`（LogicalCallContext m_ctx）(偏移: 0x0)

### 方法 (3)

- `bool get_IsNull()`
  （bool get_是否Null（））
- `bool get_HasInfo()`
  （布尔值 获取_是否有信息（））
- `LogicalCallContext Clone()`
  （LogicalCallContext 克隆（））

---

## LongList（Long列表）

### 字段 (4)

- `long[] m_values`（long[] m_values）(偏移: 0x8)
- `int m_count`（int m_count）(偏移: 0xC)
- `int m_totalItems`（int m_totalItems）(偏移: 0x10)
- `int m_currentItem`（int m_current项目）(偏移: 0x14)

### 方法 (7)

- `void Add(long value)`
  （void 添加（long value））
- `int get_Count()`
  （整数 获取_数量（））
- `void StartEnumeration()`
  （void 开始Enumeration（））
- `bool MoveNext()`
  （布尔值 移动下一个（））
- `long get_Current()`
  （long get_当前（））
- `bool RemoveElement(long value)`
  （bool 移除元素（long value））
- `void EnlargeArray()`
  （void Enlarge数组（））

---

## LongPlugin（Long插件）

**继承**: ABSTweenPlugin<long, long, NoOptions>（ABSTweenPlugin<long, long, NoOptions>）

### 方法 (8)

- `void Reset(TweenerCore<long, long, NoOptions> t)`
  （void 重置（TweenerCore<long, long, NoOptions> t））
- `void SetFrom(TweenerCore<long, long, NoOptions> t, bool isRelative)`
  （void 集合From（TweenerCore<long, long, NoOptions> t, bool isRelative））
- `void SetFrom(TweenerCore<long, long, NoOptions> t, long fromValue, bool setImmediately, bool isRelative)`
  （void 集合From（TweenerCore<long, long, NoOptions> t, long fromValue, bool setImmediately, bool isRelative））
- `long ConvertToStartValue(TweenerCore<long, long, NoOptions> t, long value)`
  （long 转换To开始值（TweenerCore<long, long, NoOptions> t, long value））
- `void SetRelativeEndValue(TweenerCore<long, long, NoOptions> t)`
  （void 集合Relative结束值（TweenerCore<long, long, NoOptions> t））
- `void SetChangeValue(TweenerCore<long, long, NoOptions> t)`
  （void 集合Change值（TweenerCore<long, long, NoOptions> t））
- `float GetSpeedBasedDuration(NoOptions options, float unitsXSecond, long changeValue)`
  （float 获取SpeedBased持续时间（NoOptions options, float unitsXSecond, long changeValue））
- `void EvaluateAndApply(NoOptions options, Tween t, bool isRelative, DOGetter<long> getter, DOSetter<long> setter, float elapsed, long startValue, long changeValue, float duration, bool usingInversePosition, UpdateNotice updateNotice)`
  （void EvaluateAnd应用（NoOptions options, Tween t, bool isRelative, DOGetter<long> getter, DOSetter<long> setter, float elapsed, long startValue, long changeValue, float duration, bool usingInversePosition, 更新Notice updateNotice））

---

## LookAtCameraPos（LookAt摄像机Pos）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 方法 (1)

- `void Update()`
  （void 更新（））

---

## LookAtController（LookAt控制器）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (20)

- `LookAtIK ik`（LookAtIK ik）(偏移: 0xC)
- `Transform target`（变换 目标）(偏移: 0x10)
- `float weight`（浮点数 权重）(偏移: 0x14)
- `Vector3 offset`（三维向量 偏移）(偏移: 0x18)
- `float targetSwitchSmoothTime`（float targetSwitchSmooth时间）(偏移: 0x24)
- `float weightSmoothTime`（float weightSmooth时间）(偏移: 0x28)
- `bool smoothTurnTowardsTarget`（bool smoothTurnTowards目标）(偏移: 0x2C)
- `float maxRadiansDelta`（float maxRadiansDelta）(偏移: 0x30)
- `float maxMagnitudeDelta`（float maxMagnitudeDelta）(偏移: 0x34)
- `float slerpSpeed`（float slerpSpeed）(偏移: 0x38)
- `Vector3 pivotOffsetFromRoot`（三维向量 pivotOffsetFrom根）(偏移: 0x3C)
- `float minDistance`（float min距离）(偏移: 0x48)
- `float maxRootAngle`（float max根角度）(偏移: 0x4C)
- `Transform lastTarget`（变换 last目标）(偏移: 0x50)
- `float switchWeight`（float switchWeight）(偏移: 0x54)
- `float switchWeightV`（float switchWeightV）(偏移: 0x58)
- `float weightV`（float weightV）(偏移: 0x5C)
- `Vector3 lastPosition`（三维向量 最后位置）(偏移: 0x60)
- `Vector3 dir`（三维向量 dir）(偏移: 0x6C)
- `bool lastSmoothTowardsTarget`（bool lastSmoothTowards目标）(偏移: 0x78)

### 方法 (5)

- `void Start()`
  （void 开始（））
- `void LateUpdate()`
  （void 延迟更新（））
- `Vector3 get_pivot()`
  （三维向量 get_pivot（））
- `void ApplyMinDistance()`
  （void 应用最小距离（））
- `void RootRotation()`
  （void 根Rotation（））

---

## LookAtIK（LookAtIK）

**继承**: IK（IK反向运动学）

### 字段 (1)

- `IKSolverLookAt solver`（IKSolverLookAt solver）(偏移: 0x1C)

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

## LoopAndDelay（LoopAnd延迟）

**继承**: VFXSpawnerCallbacks（VFXSpawnerCallbacks）

### 字段 (6)

- `int m_LoopMaxCount`（int m_Loop最大数量）(偏移: 0xC)
- `int m_LoopCurrentIndex`（int m_Loop当前索引）(偏移: 0x10)
- `float m_WaitingForTotalTime`（float m_WaitingForTotal时间）(偏移: 0x14)
- `int loopCountPropertyID`（int loop数量属性ID）(偏移: 0x0)
- `int loopDurationPropertyID`（int loop持续时间属性ID）(偏移: 0x4)
- `int delayPropertyID`（int delay属性ID）(偏移: 0x8)

---

## LoopAndDelay.InputProperties（LoopAndDelay.输入Properties）

### 字段 (3)

- `int LoopCount`（int Loop数量）(偏移: 0x8)
- `float LoopDuration`（float Loop持续时间）(偏移: 0xC)
- `float Delay`（float 延迟）(偏移: 0x10)

---

## LoopRotate（LoopRotate）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (1)

- `Vector3 speed`（三维向量 speed）(偏移: 0xC)

### 方法 (1)

- `void Update()`
  （void 更新（））

---

## LoopType（Loop类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## LostWeightSpace（LostWeightSpace）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 方法 (1)

- `void OnTriggerStay(Collider other)`
  （void 触发器停留时（碰撞器 other））

---

## LowLevelComparer（Low等级Comparer）

**继承**: IComparer（I比较器）

### 字段 (1)

- `LowLevelComparer Default`（Low等级Comparer 默认的）(偏移: 0x0)

### 方法 (1)

- `int Compare(object a, object b)`
  （整数 比较（对象 a, 对象 b））

---

## LowerResBlitTexture（下半身ResBlit纹理）

**继承**: Object（对象）

### 方法 (1)

- `void LowerResBlitTextureDontStripMe()`
  （void 下半身ResBlit纹理DontStripMe（））

---

## MACTripleDES（MACTripleDES）

**继承**: KeyedHashAlgorithm（KeyedHashAlgorithm）

### 字段 (5)

- `ICryptoTransform m_encryptor`（ICrypto变换 m_encryptor）(偏移: 0x1C)
- `CryptoStream _cs`（Crypto流 _cs）(偏移: 0x20)
- `TailStream _ts`（Tail流 _ts）(偏移: 0x24)
- `int m_bytesPerBlock`（int m_bytesPerBlock）(偏移: 0x28)
- `TripleDES des`（TripleDES des）(偏移: 0x2C)

### 方法 (4)

- `void Initialize()`
  （void 初始化（））
- `void HashCore(byte[] rgbData, int ibStart, int cbSize)`
  （void HashCore（byte[] rgbData, int ibStart, int cbSize））
- `byte[] HashFinal()`
  （字节[] 哈希最终（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））

---

## MCMDictionary（MCM字典）

**继承**: MessageDictionary（消息字典）

### 字段 (1)

- `string[] InternalKeys`（string[] 内部的Keys）(偏移: 0x0)

---

## MD5（MD5）

**继承**: HashAlgorithm（HashAlgorithm）

### 方法 (1)

- `MD5 Create()`
  （MD5 创建（））

---

## MD5CryptoServiceProvider（MD5Crypto服务提供者）

**继承**: MD5（MD5）

### 字段 (6)

- `uint[] _H`（uint[] _H）(偏移: 0x18)
- `uint[] buff`（uint[] buff）(偏移: 0x1C)
- `ulong count`（ulong count）(偏移: 0x20)
- `byte[] _ProcessingBuffer`（byte[] _Processing缓冲区）(偏移: 0x28)
- `int _ProcessingBufferCount`（int _Processing缓冲区数量）(偏移: 0x2C)
- `uint[] K`（uint[] K）(偏移: 0x0)

### 方法 (8)

- `void Finalize()`
  （void 终结（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `void HashCore(byte[] rgb, int ibStart, int cbSize)`
  （void 哈希核心（字节[] rgb, 整数 ibStart, 整数 cbSize））
- `byte[] HashFinal()`
  （字节[] 哈希最终（））
- `void Initialize()`
  （void 初始化（））
- `void ProcessBlock(byte[] inputBuffer, int inputOffset)`
  （void 处理Block（byte[] inputBuffer, int inputOffset））
- `void ProcessFinalBlock(byte[] inputBuffer, int inputOffset, int inputCount)`
  （void 处理FinalBlock（byte[] inputBuffer, int inputOffset, int inputCount））
- `void AddLength(ulong length, byte[] buffer, int position)`
  （void 添加Length（ulong length, byte[] buffer, int position））

---

## MSAASamples（MSAASamples）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## MSCompatUnicodeTable（MSCompatUnicodeTable）

### 字段 (19)

- `int MaxExpansionLength`（int 最大ExpansionLength）(偏移: 0x0)
- `byte* ignorableFlags`（byte* ignorableFlags）(偏移: 0x4)
- `byte* categories`（byte* categories）(偏移: 0x8)
- `byte* level1`（byte* level1）(偏移: 0xC)
- `byte* level2`（byte* level2）(偏移: 0x10)
- `byte* level3`（byte* level3）(偏移: 0x14)
- `byte* cjkCHScategory`（byte* cjkCHScategory）(偏移: 0x18)
- `byte* cjkCHTcategory`（byte* cjkCHTcategory）(偏移: 0x1C)
- `byte* cjkJAcategory`（byte* cjkJAcategory）(偏移: 0x20)
- `byte* cjkKOcategory`（byte* cjkKOcategory）(偏移: 0x24)
- `byte* cjkCHSlv1`（byte* cjkCHSlv1）(偏移: 0x28)
- `byte* cjkCHTlv1`（byte* cjkCHTlv1）(偏移: 0x2C)
- `byte* cjkJAlv1`（byte* cjkJAlv1）(偏移: 0x30)
- `byte* cjkKOlv1`（byte* cjkKOlv1）(偏移: 0x34)
- `byte* cjkKOlv2`（byte* cjkKOlv2）(偏移: 0x38)
- `char[] tailoringArr`（char[] tailoringArr）(偏移: 0x3C)
- `TailoringInfo[] tailoringInfos`（TailoringInfo[] tailoringInfos）(偏移: 0x40)
- `object forLock`（object forLock）(偏移: 0x44)
- `bool isReady`（bool isReady）(偏移: 0x48)

### 方法 (20)

- `TailoringInfo GetTailoringInfo(int lcid)`
  （Tailoring信息 获取Tailoring信息（int lcid））
- `void BuildTailoringTables(CultureInfo culture, TailoringInfo t, ref Contraction[] contractions, ref Level2Map[] diacriticals)`
  （void BuildTailoringTables（Culture信息 culture, Tailoring信息 t, ref Contraction[] contractions, ref Level2Map[] diacriticals））
- `void SetCJKReferences(string name, ref CodePointIndexer cjkIndexer, ref byte* catTable, ref byte* lv1Table, ref CodePointIndexer lv2Indexer, ref byte* lv2Table)`
  （void 集合CJKReferences（string name, ref CodePointIndexer cjkIndexer, ref byte* catTable, ref byte* lv1Table, ref CodePointIndexer lv2Indexer, ref byte* lv2Table））
- `byte Category(int cp)`
  （byte 类别（int cp））
- `byte Level1(int cp)`
  （byte Level1（int cp））
- `byte Level2(int cp)`
  （byte Level2（int cp））
- `byte Level3(int cp)`
  （byte Level3（int cp））
- `bool IsIgnorable(int cp, byte flag)`
  （bool 是否Ignorable（int cp, byte flag））
- `bool IsIgnorableNonSpacing(int cp)`
  （bool 是否IgnorableNonSpacing（int cp））
- `int ToKanaTypeInsensitive(int i)`
  （int ToKana类型Insensitive（int i））
- `int ToWidthCompat(int i)`
  （int To宽度Compat（int i））
- `bool HasSpecialWeight(char c)`
  （bool 是否有特殊Weight（char c））
- `bool IsHalfWidthKana(char c)`
  （bool 是否Half宽度Kana（char c））
- `bool IsHiragana(char c)`
  （bool 是否Hiragana（char c））
- `bool IsJapaneseSmallLetter(char c)`
  （bool 是否JapaneseSmallLetter（char c））
- `bool get_IsReady()`
  （bool get_是否Ready（））
- `IntPtr GetResource(string name)`
  （整数Ptr 获取资源（string name））
- `uint UInt32FromBytePtr(byte* raw, uint idx)`
  （uint UInt32FromBytePtr（byte* raw, uint idx））
- `void FillCJK(string culture, ref CodePointIndexer cjkIndexer, ref byte* catTable, ref byte* lv1Table, ref CodePointIndexer lv2Indexer, ref byte* lv2Table)`
  （void FillCJK（string culture, ref CodePointIndexer cjkIndexer, ref byte* catTable, ref byte* lv1Table, ref CodePointIndexer lv2Indexer, ref byte* lv2Table））
- `void FillCJKCore(string culture, ref CodePointIndexer cjkIndexer, ref byte* catTable, ref byte* lv1Table, ref CodePointIndexer cjkLv2Indexer, ref byte* lv2Table)`
  （void FillCJKCore（string culture, ref CodePointIndexer cjkIndexer, ref byte* catTable, ref byte* lv1Table, ref CodePointIndexer cjkLv2Indexer, ref byte* lv2Table））

---

## MSCompatUnicodeTableUtil（MSCompatUnicodeTableUtil）

### 字段 (7)

- `CodePointIndexer Ignorable`（CodePointIndexer Ignorable）(偏移: 0x0)
- `CodePointIndexer Category`（CodePointIndexer 类别）(偏移: 0x4)
- `CodePointIndexer Level1`（CodePointIndexer Level1）(偏移: 0x8)
- `CodePointIndexer Level2`（CodePointIndexer Level2）(偏移: 0xC)
- `CodePointIndexer Level3`（CodePointIndexer Level3）(偏移: 0x10)
- `CodePointIndexer CjkCHS`（CodePointIndexer CjkCHS）(偏移: 0x14)
- `CodePointIndexer Cjk`（CodePointIndexer Cjk）(偏移: 0x18)

---

## MainLightShadowCasterPass（主要的光照ShadowCasterPass）

**继承**: ScriptableRenderPass（可脚本化渲染通道）

### 字段 (11)

- `float m_MaxShadowDistance`（float m_最大Shadow距离）(偏移: 0x54)
- `int m_ShadowmapWidth`（int m_Shadowmap宽度）(偏移: 0x58)
- `int m_ShadowmapHeight`（int m_Shadowmap高度）(偏移: 0x5C)
- `int m_ShadowCasterCascadesCount`（int m_ShadowCasterCascades数量）(偏移: 0x60)
- `bool m_SupportsBoxFilterForShadows`（bool m_SupportsBoxFilterForShadows）(偏移: 0x64)
- `RenderTargetHandle m_MainLightShadowmap`（Render目标句柄 m_主要的光照Shadowmap）(偏移: 0x68)
- `RenderTexture m_MainLightShadowmapTexture`（Render纹理 m_主要的光照Shadowmap纹理）(偏移: 0x88)
- `Matrix4x4[] m_MainLightShadowMatrices`（Matrix4x4[] m_主要的光照ShadowMatrices）(偏移: 0x8C)
- `ShadowSliceData[] m_CascadeSlices`（ShadowSliceData[] m_CascadeSlices）(偏移: 0x90)
- `Vector4[] m_CascadeSplitDistances`（Vector4[] m_CascadeSplitDistances）(偏移: 0x94)
- `ProfilingSampler m_ProfilingSetupSampler`（ProfilingSampler m_ProfilingSetupSampler）(偏移: 0x98)

### 方法 (7)

- `bool Setup(ref RenderingData renderingData)`
  （bool Setup（ref RenderingData renderingData））
- `void Configure(CommandBuffer cmd, RenderTextureDescriptor cameraTextureDescriptor)`
  （void 配置（命令缓冲区 cmd, 渲染纹理描述符 cameraTextureDescriptor））
- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（可脚本化渲染上下文 context, 引用 渲染数据 renderingData））
- `void OnCameraCleanup(CommandBuffer cmd)`
  （void 摄像机清理时（命令缓冲区 cmd））
- `void Clear()`
  （void 清除（））
- `void RenderMainLightCascadeShadowmap(ref ScriptableRenderContext context, ref CullingResults cullResults, ref LightData lightData, ref ShadowData shadowData)`
  （void Render主要的光照CascadeShadowmap（ref ScriptableRenderContext context, ref CullingResults cullResults, ref LightData lightData, ref ShadowData shadowData））
- `void SetupMainLightShadowReceiverConstants(CommandBuffer cmd, VisibleLight shadowLight, bool supportsSoftShadows)`
  （void Setup主要的光照ShadowReceiverConstants（Command缓冲区 cmd, 可见的光照 shadowLight, bool supportsSoftShadows））

---

## MainLightShadowCasterPass.MainLightShadowConstantBuffer（主要的光照ShadowCasterPass.主要的光照ShadowConstant缓冲区）

### 字段 (12)

- `int _WorldToShadow`（int _世界的ToShadow）(偏移: 0x0)
- `int _ShadowParams`（int _ShadowParams）(偏移: 0x4)
- `int _CascadeShadowSplitSpheres0`（int _CascadeShadowSplitSpheres0）(偏移: 0x8)
- `int _CascadeShadowSplitSpheres1`（int _CascadeShadowSplitSpheres1）(偏移: 0xC)
- `int _CascadeShadowSplitSpheres2`（int _CascadeShadowSplitSpheres2）(偏移: 0x10)
- `int _CascadeShadowSplitSpheres3`（int _CascadeShadowSplitSpheres3）(偏移: 0x14)
- `int _CascadeShadowSplitSphereRadii`（int _CascadeShadowSplitSphereRadii）(偏移: 0x18)
- `int _ShadowOffset0`（int _ShadowOffset0）(偏移: 0x1C)
- `int _ShadowOffset1`（int _ShadowOffset1）(偏移: 0x20)
- `int _ShadowOffset2`（int _ShadowOffset2）(偏移: 0x24)
- `int _ShadowOffset3`（int _ShadowOffset3）(偏移: 0x28)
- `int _ShadowmapSize`（int _Shadowmap大小）(偏移: 0x2C)

---

## ManagedStreamHelpers（Managed流Helpers）

### 方法 (4)

- `void ValidateLoadFromStream(Stream stream)`
  （void 验证加载From流（流 stream））
- `void ManagedStreamRead(byte[] buffer, int offset, int count, Stream stream, IntPtr returnValueAddress)`
  （void Managed流Read（byte[] buffer, int offset, int count, 流 stream, 整数Ptr returnValueAddress））
- `void ManagedStreamSeek(long offset, uint origin, Stream stream, IntPtr returnValueAddress)`
  （void Managed流Seek（long offset, uint origin, 流 stream, 整数Ptr returnValueAddress））
- `void ManagedStreamLength(Stream stream, IntPtr returnValueAddress)`
  （void Managed流Length（流 stream, 整数Ptr returnValueAddress））

---

## ManifestBasedResourceGroveler（ManifestBased资源Groveler）

**继承**: IResourceGroveler（I资源Groveler）

### 字段 (1)

- `ResourceManager.ResourceManagerMediator _mediator`（资源Manager.资源管理器Mediator _mediator）(偏移: 0x8)

### 方法 (12)

- `ResourceSet GrovelForResourceSet(CultureInfo culture, Dictionary<string, ResourceSet> localResourceSets, bool tryParents, bool createIfNotExists, ref StackCrawlMark stackMark)`
  （资源集合 GrovelFor资源集合（Culture信息 culture, Dictionary<string, 资源Set> localResourceSets, bool tryParents, bool createIfNotExists, ref StackCrawlMark stackMark））
- `CultureInfo UltimateFallbackFixup(CultureInfo lookForCulture)`
  （Culture信息 UltimateFallbackFixup（Culture信息 lookForCulture））
- `CultureInfo GetNeutralResourcesLanguage(Assembly a, ref UltimateResourceFallbackLocation fallbackLocation)`
  （Culture信息 获取NeutralResourcesLanguage（Assembly a, ref UltimateResourceFallbackLocation fallbackLocation））
- `ResourceSet CreateResourceSet(Stream store, Assembly assembly)`
  （资源集合 创建资源集合（流 store, Assembly assembly））
- `Stream GetManifestResourceStream(RuntimeAssembly satellite, string fileName, ref StackCrawlMark stackMark)`
  （流 获取Manifest资源流（RuntimeAssembly satellite, string fileName, ref StackCrawlMark stackMark））
- `Stream CaseInsensitiveManifestResourceStreamLookup(RuntimeAssembly satellite, string name)`
  （流 CaseInsensitiveManifest资源流Lookup（RuntimeAssembly satellite, string name））
- `RuntimeAssembly GetSatelliteAssembly(CultureInfo lookForCulture, ref StackCrawlMark stackMark)`
  （RuntimeAssembly 获取SatelliteAssembly（Culture信息 lookForCulture, ref StackCrawlMark stackMark））
- `bool CanUseDefaultResourceClasses(string readerTypeName, string resSetTypeName)`
  （bool 能否Use默认的资源Classes（string readerTypeName, string resSetTypeName））
- `string GetSatelliteAssemblyName()`
  （string 获取SatelliteAssembly名称（））
- `void HandleSatelliteMissing()`
  （void 句柄SatelliteMissing（））
- `void HandleResourceStreamMissing(string fileName)`
  （void 句柄资源流Missing（string fileName））
- `bool GetNeutralResourcesLanguageAttribute(Assembly assembly, ref string cultureName, ref short fallbackLocation)`
  （bool 获取NeutralResourcesLanguageAttribute（Assembly assembly, ref string cultureName, ref short fallbackLocation））

---

## ManifestBuilder（Manifest构建器）

### 字段 (9)

- `StringBuilder sb`（字符串构建器 sb）(偏移: 0x1C)
- `StringBuilder events`（字符串构建器 events）(偏移: 0x20)
- `StringBuilder templates`（字符串构建器 templates）(偏移: 0x24)
- `ResourceManager resources`（资源管理器 resources）(偏移: 0x28)
- `EventManifestOptions flags`（事件ManifestOptions flags）(偏移: 0x2C)
- `IList<string> errors`（IList<string> errors）(偏移: 0x30)
- `string eventName`（string event名称）(偏移: 0x38)
- `int numParams`（int numParams）(偏移: 0x3C)
- `List<int> byteArrArgIndices`（List<int> byteArrArgIndices）(偏移: 0x40)

### 方法 (22)

- `void AddOpcode(string name, int value)`
  （void 添加Opcode（string name, int value））
- `void AddTask(string name, int value)`
  （void 添加Task（string name, int value））
- `void AddKeyword(string name, ulong value)`
  （void 添加Keyword（string name, ulong value））
- `void StartEvent(string eventName, EventAttribute eventAttribute)`
  （void 开始事件（string eventName, 事件Attribute eventAttribute））
- `void AddEventParameter(Type type, string name)`
  （void 添加事件Parameter（类型 type, string name））
- `void EndEvent()`
  （void 结束事件（））
- `byte[] CreateManifest()`
  （byte[] 创建Manifest（））
- `IList<string> get_Errors()`
  （IList<string> get_Errors（））
- `void ManifestError(string msg, bool runtimeCritical = False)`
  （void ManifestError（string msg, bool runtimeCritical = False））
- `string CreateManifestString()`
  （string 创建Manifest字符串（））
- `void WriteNameAndMessageAttribs(StringBuilder stringBuilder, string elementName, string name)`
  （void Write名称AndMessageAttribs（字符串构建器 stringBuilder, string elementName, string name））
- `void WriteMessageAttrib(StringBuilder stringBuilder, string elementName, string name, string value)`
  （void WriteMessageAttrib（字符串构建器 stringBuilder, string elementName, string name, string value））
- `string GetLocalizedMessage(string key, CultureInfo ci, bool etwFormat)`
  （string 获取LocalizedMessage（string key, Culture信息 ci, bool etwFormat））
- `List<CultureInfo> GetSupportedCultures(ResourceManager resources)`
  （List<CultureInfo> 获取SupportedCultures（资源管理器 resources））
- `string GetLevelName(EventLevel level)`
  （string 获取等级名称（事件等级 level））
- `string GetTaskName(EventTask task, string eventName)`
  （string 获取Task名称（事件Task task, string eventName））
- `string GetOpcodeName(EventOpcode opcode, string eventName)`
  （string 获取Opcode名称（事件Opcode opcode, string eventName））
- `string GetKeywords(ulong keywords, string eventName)`
  （string 获取Keywords（ulong keywords, string eventName））
- `string GetTypeName(Type type)`
  （string 获取类型名称（类型 type））
- `void UpdateStringBuilder(ref StringBuilder stringBuilder, string eventMessage, int startIndex, int count)`
  （void 更新字符串构建器（ref StringBuilder stringBuilder, string eventMessage, int startIndex, int count））
- `string TranslateToManifestConvention(string eventMessage, string evtName)`
  （string TranslateToManifestConvention（string eventMessage, string evtName））
- `int TranslateIndexToManifestConvention(int idx, string evtName)`
  （int Translate索引ToManifestConvention（int idx, string evtName））

---

## ManifestEnvelope（ManifestEnvelope）

### 字段 (6)

- `ManifestEnvelope.ManifestFormats Format`（ManifestEnvelope.ManifestFormats 格式化）(偏移: 0x0)
- `byte MajorVersion`（byte MajorVersion）(偏移: 0x1)
- `byte MinorVersion`（byte MinorVersion）(偏移: 0x2)
- `byte Magic`（byte Magic）(偏移: 0x3)
- `ushort TotalChunks`（ushort TotalChunks）(偏移: 0x4)
- `ushort ChunkNumber`（ushort ChunkNumber）(偏移: 0x6)

---

## ManifestEnvelope.ManifestFormats（ManifestEnvelope.ManifestFormats）

### 字段 (1)

- `byte value__`（字节 值__）(偏移: 0x0)

---

## ManifestResourceInfo（Manifest资源信息）

### 字段 (3)

- `Assembly _containingAssembly`（Assembly _containingAssembly）(偏移: 0x8)
- `string _containingFileName`（string _containing文件名称）(偏移: 0xC)
- `ResourceLocation _resourceLocation`（资源Location _resourceLocation）(偏移: 0x10)

### 方法 (3)

- `Assembly get_ReferencedAssembly()`
  （Assembly get_ReferencedAssembly（））
- `string get_FileName()`
  （string get_文件名称（））
- `ResourceLocation get_ResourceLocation()`
  （资源Location get_资源Location（））

---

## ManualResetEventSlim（手动重置事件Slim）

**继承**: IDisposable（可释放接口）

### 字段 (4)

- `object m_lock`（object m_lock）(偏移: 0x8)
- `ManualResetEvent m_eventObj`（手动重置事件 m_eventObj）(偏移: 0xC)
- `int m_combinedState`（int m_combined状态）(偏移: 0x10)
- `Action<object> s_cancellationTokenCallback`（Action<object> s_cancellation令牌回调）(偏移: 0x0)

### 方法 (20)

- `WaitHandle get_WaitHandle()`
  （Wait句柄 get_Wait句柄（））
- `bool get_IsSet()`
  （bool get_是否集合（））
- `void set_IsSet(bool value)`
  （void set_是否集合（bool value））
- `int get_SpinCount()`
  （int get_Spin数量（））
- `void set_SpinCount(int value)`
  （void set_Spin数量（int value））
- `int get_Waiters()`
  （int get_Waiters（））
- `void set_Waiters(int value)`
  （void set_Waiters（int value））
- `void Initialize(bool initialState, int spinCount)`
  （void 初始化（bool initialState, int spinCount））
- `void EnsureLockObjectCreated()`
  （void EnsureLock对象Created（））
- `bool LazyInitializeEvent()`
  （bool Lazy初始化事件（））
- `void Set()`
  （void 集合（））
- `void Set(bool duringCancellation)`
  （void 集合（bool duringCancellation））
- `bool Wait(int millisecondsTimeout, CancellationToken cancellationToken)`
  （bool Wait（int millisecondsTimeout, Cancellation令牌 cancellationToken））
- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `void ThrowIfDisposed()`
  （void 投掷IfDisposed（））
- `void CancellationTokenCallback(object obj)`
  （void Cancellation令牌回调（object obj））
- `void UpdateStateAtomically(int newBits, int updateBitsMask)`
  （void 更新状态Atomically（int newBits, int updateBitsMask））
- `int ExtractStatePortionAndShiftRight(int state, int mask, int rightBitShiftCount)`
  （int Extract状态PortionAndShift右（int state, int mask, int rightBitShiftCount））
- `int ExtractStatePortion(int state, int mask)`
  （int Extract状态Portion（int state, int mask））

---

## MapAsset（地图资产）

**继承**: ScriptableObject（脚本对象）

### 字段 (3)

- `GameMode gameMode`（游戏模式 game模式）(偏移: 0xC)
- `GameObject gameModePrefab`（游戏对象 game模式预制体）(偏移: 0x10)
- `MapAsset.Map[] datas`（映射Asset.Map[] datas）(偏移: 0x14)

### 方法 (6)

- `void UpdateMapDropDown(Dropdown dropdown)`
  （void 更新映射Drop下（Dropdown dropdown））
- `void UpdateSettingDropdowns(Dropdown[] dropdowns)`
  （void 更新设置Dropdowns（Dropdown[] dropdowns））
- `void ApplyGameSetting(int mapID, Dropdown[] dropdowns)`
  （void 应用游戏设置（int mapID, Dropdown[] dropdowns））
- `void OnSettingDropdownValueChange(int dropdownID, int newValue)`
  （void On设置Dropdown值Change（int dropdownID, int newValue））
- `void SetListString(List<Dropdown.OptionData> list, string str)`
  （void 集合列表字符串（List<Dropdown.OptionData> list, string str））
- `void SetListString(List<Dropdown.OptionData> list, string[] strs)`
  （void 集合列表字符串（List<Dropdown.OptionData> list, string[] strs））

---

## MapAsset.Map（映射Asset.映射）

### 字段 (7)

- `string sceneName`（string scene名称）(偏移: 0x0)
- `string mapName`（string map名称）(偏移: 0x4)
- `Sprite mapIcon`（精灵 map图标）(偏移: 0x8)
- `Texture loadingTex_BL`（纹理 loadingTex_BL）(偏移: 0xC)
- `Texture loadingTex_GR`（纹理 loadingTex_GR）(偏移: 0x10)
- `GameObject gameModePrefabOverride`（游戏对象 game模式预制体重写）(偏移: 0x14)
- `WeaponLimited weaponLimited`（Weapon限制 weapon限制）(偏移: 0x18)

---

## MapAsset_DeathMatch（映射Asset_死亡比赛）

**继承**: MapAsset（地图资产）

### 字段 (3)

- `int[] KillDatas`（int[] 击杀Datas）(偏移: 0x0)
- `string[] KillTexts`（string[] 击杀Texts）(偏移: 0x4)
- `string[] WpnSelectTexts`（string[] 武器选择Texts）(偏移: 0x8)

### 方法 (3)

- `void UpdateSettingDropdowns(Dropdown[] dropdowns)`
  （void 更新设置Dropdowns（Dropdown[] dropdowns））
- `void OnSettingDropdownValueChange(int dropdownID, int newValue)`
  （void On设置Dropdown值Change（int dropdownID, int newValue））
- `void ApplyGameSetting(int mapID, Dropdown[] dropdowns)`
  （void 应用游戏设置（int mapID, Dropdown[] dropdowns））

---

## MapAsset_Nano（映射Asset_纳米）

**继承**: MapAsset（地图资产）

### 字段 (4)

- `Vector2Int GameTime_Nano4`（二维向量整数 游戏Time_Nano4）(偏移: 0x0)
- `Vector2Int GameTime_Nano4Terminator`（二维向量整数 游戏Time_Nano4Terminator）(偏移: 0x8)
- `int[] RoundDatas`（int[] 回合Datas）(偏移: 0x10)
- `string[] RoundTexts`（string[] 回合Texts）(偏移: 0x14)

### 方法 (2)

- `void ApplyGameSetting(int mapID, Dropdown[] dropdowns)`
  （void 应用游戏设置（int mapID, Dropdown[] dropdowns））
- `void UpdateSettingDropdowns(Dropdown[] dropdowns)`
  （void 更新设置Dropdowns（Dropdown[] dropdowns））

---

## MapAsset_Special（映射Asset_特殊）

**继承**: MapAsset_TeamDeath（映射Asset_队伍死亡）

### 字段 (1)

- `string[] WinType2`（string[] WinType2）(偏移: 0x33783359)

---

## MapAsset_TeamDeath（映射Asset_队伍死亡）

**继承**: MapAsset（地图资产）

### 字段 (6)

- `int[] KillDatas`（int[] 击杀Datas）(偏移: 0x0)
- `string[] KillTexts`（string[] 击杀Texts）(偏移: 0x4)
- `Vector2Int KillConditionTime`（二维向量整数 击杀Condition时间）(偏移: 0x8)
- `Vector2Int[] TimeDatas`（二维向量Int[] 时间Datas）(偏移: 0x10)
- `string[] TimeTexts`（string[] 时间Texts）(偏移: 0x14)
- `string[] WinType`（string[] Win类型）(偏移: 0x18)

### 方法 (3)

- `void UpdateSettingDropdowns(Dropdown[] dropdowns)`
  （void 更新设置Dropdowns（Dropdown[] dropdowns））
- `void OnSettingDropdownValueChange(int dropdownID, int newValue)`
  （void On设置Dropdown值Change（int dropdownID, int newValue））
- `void ApplyGameSetting(int mapID, Dropdown[] dropdowns)`
  （void 应用游戏设置（int mapID, Dropdown[] dropdowns））

---

## MapEffectShooter（地图特效射击器）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (3)

- `float duration`（浮点数 持续时间）(偏移: 0xC)
- `ParticleSystem ptc`（粒子系统 ptc）(偏移: 0x10)
- `Vector3[] positions`（Vector3[] positions）(偏移: 0x14)

### 方法 (4)

- `void Awake()`
  （void 唤醒（））
- `void Start()`
  （void 开始（））
- `IEnumerator LoopShoot()`
  （IEnumerator 循环射击（））
- `void Shoot()`
  （void 射击（））

---

## MapGun（地图枪械）

**继承**: MapTrigger（地图触发器）

### 字段 (9)

- `Sprite otherOccupiedTip`（精灵 otherOccupiedTip）(偏移: 0x1C)
- `GameObject leg`（游戏对象 leg）(偏移: 0x20)
- `BoxCollider legCollider`（Box碰撞器 leg碰撞器）(偏移: 0x24)
- `Transform setPos`（变换 setPos）(偏移: 0x28)
- `Player occupier`（玩家 occupier）(偏移: 0x2C)
- `Weapon weapon`（Weapon weapon）(偏移: 0x30)
- `Vector3 defaultEuler`（三维向量 defaultEuler）(偏移: 0x38)
- `Vector3 wpnPos`（三维向量 武器Pos）(偏移: 0x44)
- `Vector3 wpnEuler`（三维向量 武器Euler）(偏移: 0x50)

### 方法 (10)

- `QVModel get_weaponMdl()`
  （QV模型 get_weapon模型（））
- `void set_weaponMdl(QVModel value)`
  （void set_weapon模型（QV模型 value））
- `void Start()`
  （void 开始（））
- `void Update()`
  （void 更新（））
- `void Active(Player player)`
  （void 激活的（玩家 player））
- `void OnPlayerExit(Player player)`
  （void On玩家Exit（玩家 player））
- `void OnMapWpnRecycle()`
  （void On映射武器Recycle（））
- `void ResetEuler()`
  （void 重置Euler（））
- `bool CanInteract()`
  （bool 能否交互（））
- `Sprite GetTipSprite()`
  （精灵 获取Tip精灵（））

---

## MapManager（映射管理器）

**继承**: Singleton<MapManager>（Singleton<映射Manager>）

### 字段 (19)

- `SpawnPointDictionary pointDic`（出生Point字典 pointDic）(偏移: 0xC)
- `SpawnPoint[] SP_BL`（出生Point[] SP_BL）(偏移: 0x10)
- `SpawnPoint[] SP_GR`（出生Point[] SP_GR）(偏移: 0x14)
- `SpawnPoint[] SP_Netural`（出生Point[] SP_Netural）(偏移: 0x18)
- `SpawnPoint[] SP_SupplyBox`（出生Point[] SP_SupplyBox）(偏移: 0x1C)
- `SpawnPoint[] SP_RedBox`（出生Point[] SP_红色Box）(偏移: 0x20)
- `SpawnPoint[] SP_BlueBox`（出生Point[] SP_蓝色Box）(偏移: 0x24)
- `int SPID_BL`（int SPID_BL）(偏移: 0x0)
- `int SPID_GR`（int SPID_GR）(偏移: 0x4)
- `int SPID_Netural`（int SPID_Netural）(偏移: 0x8)
- `List<int> IDList_SupplyBox`（List<int> IDList_SupplyBox）(偏移: 0x28)
- `List<int> IDList_RedBox`（List<int> IDList_红色Box）(偏移: 0x2C)
- `List<int> IDList_BlueBox`（List<int> IDList_蓝色Box）(偏移: 0x30)
- `int mapGunIndex`（int map枪械索引）(偏移: 0x34)
- `Vector2Int mapGunAmmo`（二维向量整数 map枪械弹药）(偏移: 0xC)
- `bool knifeHitStun`（bool knife命中眩晕）(偏移: 0x38)
- `Texture2D minimap`（Texture2D minimap）(偏移: 0x3C)
- `Vector3 radarOriginPos`（三维向量 radarOriginPos）(偏移: 0x40)
- `float pixelPerDistance`（float pixelPer距离）(偏移: 0x4C)

### 方法 (8)

- `void Awake()`
  （void 唤醒（））
- `void OnDestroy()`
  （void 销毁时（））
- `void MapGunInit()`
  （void 映射枪械初始化（））
- `void NewGameRoundStart()`
  （void 新的游戏回合开始（））
- `SpawnPoint GetSpawnPoint(Team team)`
  （出生Point 获取出生Point（队伍 team））
- `void OnDrawGizmos()`
  （void 绘制辅助线时（））
- `int GetSupplyBoxPoint(out SpawnPoint point, SupplyBox.Type type)`
  （int 获取SupplyBoxPoint（out SpawnPoint point, SupplyBox.类型 type））
- `void ReleaseSupplyBoxPoint(int index, SupplyBox.Type boxType)`
  （void ReleaseSupplyBoxPoint（int index, SupplyBox.类型 boxType））

---

## MapShadowCombiner（映射Shadow组合器）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (5)

- `MeshFilter oneSideShadow`（网格Filter one侧面Shadow）(偏移: 0xC)
- `MeshFilter twoSideShadow`（网格Filter two侧面Shadow）(偏移: 0x10)
- `MeshRenderer[] mapShadowCasters`（网格Renderer[] mapShadowCasters）(偏移: 0x14)
- `List<MeshFilter> oneSideMesh`（List<网格Filter> one侧面网格）(偏移: 0x18)
- `List<MeshFilter> twoSideMesh`（List<网格Filter> two侧面网格）(偏移: 0x1C)

### 方法 (3)

- `void Awake()`
  （void 唤醒（））
- `void CheckMeshRender(MeshRenderer mr)`
  （void 检查网格Render（网格渲染器 mr））
- `void Combine(List<MeshFilter> input, MeshFilter output)`
  （void Combine（List<网格Filter> input, 网格Filter output））

---

## MapTrigger（地图触发器）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (4)

- `Sprite tipSprite`（精灵 tip精灵）(偏移: 0xC)
- `GameObject bindGauge`（游戏对象 bindGauge）(偏移: 0x10)
- `float interactNeedTime`（float interact需要时间）(偏移: 0x14)
- `bool posChangeBreak`（bool posChangeBreak）(偏移: 0x18)

### 方法 (9)

- `void OnTriggerStay(Collider other)`
  （void 触发器停留时（碰撞器 other））
- `void OnPlayerStay(Player player)`
  （void On玩家Stay（玩家 player））
- `void OnTriggerExit(Collider other)`
  （void 触发器退出时（碰撞器 other））
- `void OnPlayerExit(Player player)`
  （void On玩家Exit（玩家 player））
- `void Active(Player player)`
  （void 激活的（玩家 player））
- `bool CanBeInteractor(Player player)`
  （bool 能否BeInteractor（玩家 player））
- `bool CanInteract()`
  （bool 能否交互（））
- `void StartInteract(Player player)`
  （void 开始交互（玩家 player））
- `Sprite GetTipSprite()`
  （精灵 获取Tip精灵（））

---

## MarkerFlags（MarkerFlags）

### 字段 (1)

- `ushort value__`（ushort value__）(偏移: 0x0)

---

## MarkerList（Marker列表）

**继承**: ISerializationCallbackReceiver（ISerialization回调接收器）

### 字段 (4)

- `List<ScriptableObject> m_Objects`（List<ScriptableObject> m_Objects）(偏移: 0x0)
- `List<IMarker> m_Cache`（List<IMarker> m_缓存）(偏移: 0x4)
- `bool m_CacheDirty`（bool m_缓存Dirty）(偏移: 0x8)
- `bool m_HasNotifications`（bool m_是否有Notifications）(偏移: 0x9)

### 方法 (12)

- `List<IMarker> get_markers()`
  （List<IMarker> get_markers（））
- `void Add(ScriptableObject item)`
  （void 添加（脚本对象 item））
- `bool Remove(IMarker item)`
  （bool 移除（IMarker item））
- `bool Remove(ScriptableObject item, TimelineAsset timelineAsset, PlayableAsset thingToDirty)`
  （bool 移除（脚本对象 item, Timeline资产 timelineAsset, Playable资产 thingToDirty））
- `void Clear()`
  （void 清除（））
- `IEnumerable<IMarker> GetMarkers()`
  （IEnumerable<IMarker> 获取Markers（））
- `int get_Count()`
  （整数 获取_数量（））
- `IMarker get_Item(int idx)`
  （IMarker get_项目（int idx））
- `List<ScriptableObject> GetRawMarkerList()`
  （List<ScriptableObject> 获取RawMarker列表（））
- `IMarker CreateMarker(Type type, double time, TrackAsset owner)`
  （IMarker 创建Marker（类型 type, double time, Track资产 owner））
- `bool HasNotifications()`
  （bool 是否有Notifications（））
- `void BuildCache()`
  （void Build缓存（））

---

## MarkerTrack（MarkerTrack）

**继承**: TrackAsset（轨道资产）

### 方法 (1)

- `IEnumerable<PlayableBinding> get_outputs()`
  （IEnumerable<可播放绑定> 获取_输出（））

---

## Marshal（Marshal）

### 字段 (2)

- `int SystemMaxDBCSCharSize`（int 系统最大DBCSChar大小）(偏移: 0x0)
- `int SystemDefaultCharSize`（int 系统默认的Char大小）(偏移: 0x4)

### 方法 (12)

- `void copy_from_unmanaged(IntPtr source, int startIndex, Array destination, int length)`
  （void copy_from_unmanaged（整数Ptr source, int startIndex, 数组 destination, int length））
- `void Copy(IntPtr source, byte[] destination, int startIndex, int length)`
  （void 复制（整数Ptr source, byte[] destination, int startIndex, int length））
- `void Copy(IntPtr source, char[] destination, int startIndex, int length)`
  （void 复制（整数Ptr source, char[] destination, int startIndex, int length））
- `void FreeBSTR(IntPtr ptr)`
  （void FreeBSTR（整数Ptr ptr））
- `int GetHRForException(Exception e)`
  （int 获取HRForException（Exception e））
- `int GetLastWin32Error()`
  （int 获取最后一个Win32Error（））
- `string PtrToStringUni(IntPtr ptr)`
  （string PtrTo字符串Uni（整数Ptr ptr））
- `int ReleaseInternal(IntPtr pUnk)`
  （int Release内部的（整数Ptr pUnk））
- `int Release(IntPtr pUnk)`
  （int Release（整数Ptr pUnk））
- `int SizeOf(Type t)`
  （int 大小Of（类型 t））
- `void StructureToPtr(object structure, IntPtr ptr, bool fDeleteOld)`
  （void StructureToPtr（object structure, 整数Ptr ptr, bool fDeleteOld））
- `IntPtr GetFunctionPointerForDelegateInternal(Delegate d)`
  （整数Ptr 获取Function指针For委托内部的（委托 d））

---

## MarshalAsAttribute（MarshalAsAttribute）

**继承**: Attribute（属性）

### 字段 (10)

- `string MarshalCookie`（string MarshalCookie）(偏移: 0x8)
- `string MarshalType`（string Marshal类型）(偏移: 0xC)
- `Type MarshalTypeRef`（类型 Marshal类型Ref）(偏移: 0x10)
- `Type SafeArrayUserDefinedSubType`（类型 Safe数组UserDefined子类型）(偏移: 0x14)
- `UnmanagedType utype`（Unmanaged类型 utype）(偏移: 0x18)
- `UnmanagedType ArraySubType`（Unmanaged类型 数组子类型）(偏移: 0x1C)
- `VarEnum SafeArraySubType`（VarEnum Safe数组子类型）(偏移: 0x20)
- `int SizeConst`（int 大小Const）(偏移: 0x24)
- `int IidParameterIndex`（int IidParameter索引）(偏移: 0x28)
- `short SizeParamIndex`（short 大小Param索引）(偏移: 0x2C)

### 方法 (1)

- `MarshalAsAttribute Copy()`
  （MarshalAsAttribute 复制（））

---

## MarshalByRefObject（MarshalByRef对象）

### 字段 (1)

- `object _identity`（object _identity）(偏移: 0x8)

### 方法 (4)

- `ServerIdentity get_ObjectIdentity()`
  （服务器Identity get_对象Identity（））
- `void set_ObjectIdentity(ServerIdentity value)`
  （void set_对象Identity（服务器Identity value））
- `ObjRef CreateObjRef(Type requestedType)`
  （ObjRef 创建ObjRef（类型 requestedType））
- `object InitializeLifetimeService()`
  （object 初始化Lifetime服务（））

---

## Mask（掩码）

**继承**: UIBehaviour, ICanvasRaycastFilter, IMaterialModifier（界面Behaviour, I画布RaycastFilter, I材质修改器）

### 字段 (5)

- `RectTransform m_RectTransform`（Rect变换 m_Rect变换）(偏移: 0xC)
- `bool m_ShowMaskGraphic`（bool m_显示掩码Graphic）(偏移: 0x10)
- `Graphic m_Graphic`（Graphic m_Graphic）(偏移: 0x14)
- `Material m_MaskMaterial`（材质 m_掩码材质）(偏移: 0x18)
- `Material m_UnmaskMaterial`（材质 m_Unmask材质）(偏移: 0x1C)

### 方法 (10)

- `RectTransform get_rectTransform()`
  （矩形变换 获取_矩形变换（））
- `bool get_showMaskGraphic()`
  （bool get_show掩码Graphic（））
- `void set_showMaskGraphic(bool value)`
  （void set_show掩码Graphic（bool value））
- `Graphic get_graphic()`
  （Graphic get_graphic（））
- `bool MaskEnabled()`
  （bool 掩码启用的（））
- `void OnSiblingGraphicEnabledDisabled()`
  （void OnSiblingGraphic启用的禁用的（））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `bool IsRaycastLocationValid(Vector2 sp, Camera eventCamera)`
  （布尔值 射线检测位置是否有效（二维向量 sp, 摄像机 eventCamera））
- `Material GetModifiedMaterial(Material baseMaterial)`
  （材质 获取Modified材质（材质 baseMaterial））

---

## MaskUtilities（掩码Utilities）

### 方法 (7)

- `void Notify2DMaskStateChanged(Component mask)`
  （void Notify2D掩码状态Changed（组件 mask））
- `void NotifyStencilStateChanged(Component mask)`
  （void NotifyStencil状态Changed（组件 mask））
- `Transform FindRootSortOverrideCanvas(Transform start)`
  （变换 查找根Sort重写画布（变换 start））
- `int GetStencilDepth(Transform transform, Transform stopAfter)`
  （int 获取Stencil深度（变换 transform, 变换 stopAfter））
- `bool IsDescendantOrSelf(Transform father, Transform child)`
  （bool 是否DescendantOrSelf（变换 father, 变换 child））
- `RectMask2D GetRectMaskForClippable(IClippable clippable)`
  （RectMask2D 获取Rect掩码ForClippable（IClippable clippable））
- `void GetRectMasksForClip(RectMask2D clipper, List<RectMask2D> masks)`
  （void 获取RectMasksFor弹匣（RectMask2D clipper, List<RectMask2D> masks））

---

## MaskableGraphic（MaskableGraphic）

**继承**: Graphic, IClippable, IMaskable, IMaterialModifier（Graphic, IClippable, IMaskable, I材质修改器）

### 字段 (10)

- `bool m_ShouldRecalculateStencil`（bool m_应该RecalculateStencil）(偏移: 0x60)
- `Material m_MaskMaterial`（材质 m_掩码材质）(偏移: 0x64)
- `RectMask2D m_ParentMask`（RectMask2D m_父级掩码）(偏移: 0x68)
- `bool m_Maskable`（bool m_Maskable）(偏移: 0x6C)
- `bool m_IsMaskingGraphic`（bool m_是否MaskingGraphic）(偏移: 0x6D)
- `bool m_IncludeForMasking`（bool m_IncludeForMasking）(偏移: 0x6E)
- `MaskableGraphic.CullStateChangedEvent m_OnCullStateChanged`（MaskableGraphic.Cull状态Changed事件 m_OnCull状态Changed）(偏移: 0x70)
- `bool m_ShouldRecalculate`（bool m_应该Recalculate）(偏移: 0x74)
- `int m_StencilValue`（int m_Stencil值）(偏移: 0x78)
- `Vector3[] m_Corners`（Vector3[] m_Corners）(偏移: 0x7C)

### 方法 (20)

- `MaskableGraphic.CullStateChangedEvent get_onCullStateChanged()`
  （MaskableGraphic.Cull状态Changed事件 get_onCull状态Changed（））
- `void set_onCullStateChanged(MaskableGraphic.CullStateChangedEvent value)`
  （void set_onCull状态Changed（MaskableGraphic.Cull状态Changed事件 value））
- `bool get_maskable()`
  （bool get_maskable（））
- `void set_maskable(bool value)`
  （void set_maskable（bool value））
- `bool get_isMaskingGraphic()`
  （bool get_isMaskingGraphic（））
- `void set_isMaskingGraphic(bool value)`
  （void set_isMaskingGraphic（bool value））
- `Material GetModifiedMaterial(Material baseMaterial)`
  （材质 获取Modified材质（材质 baseMaterial））
- `void Cull(Rect clipRect, bool validRect)`
  （void Cull（Rect clipRect, bool validRect））
- `void UpdateCull(bool cull)`
  （void 更新Cull（bool cull））
- `void SetClipRect(Rect clipRect, bool validRect)`
  （void 集合弹匣Rect（Rect clipRect, bool validRect））
- `void SetClipSoftness(Vector2 clipSoftness)`
  （void 集合弹匣Softness（二维向量 clipSoftness））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `void OnTransformParentChanged()`
  （void 变换父级改变时（））
- `void ParentMaskStateChanged()`
  （void 父级掩码状态Changed（））
- `void OnCanvasHierarchyChanged()`
  （void 画布层级改变时（））
- `Rect get_rootCanvasRect()`
  （Rect get_root画布Rect（））
- `void UpdateClipParent()`
  （void 更新弹匣父级（））
- `void RecalculateClipping()`
  （void RecalculateClipping（））
- `void RecalculateMasking()`
  （void RecalculateMasking（））

---

## MasterHeroSkillFX（Master英雄技能FX）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (6)

- `RawImage img`（Raw图像 img）(偏移: 0xC)
- `RectTransform rect`（矩形变换 rect）(偏移: 0x10)
- `float width`（浮点数 宽度）(偏移: 0x14)
- `float height`（浮点数 高度）(偏移: 0x18)
- `Vector2 targetPos`（二维向量 targetPos）(偏移: 0x1C)
- `int side`（int side）(偏移: 0x24)

### 方法 (4)

- `void Awake()`
  （void 唤醒（））
- `void Start()`
  （void 开始（））
- `void Animation()`
  （void 动画（））
- `void Update()`
  （void 更新（））

---

## Match（比赛）

**继承**: Group（组）

### 字段 (10)

- `Match _empty`（比赛 _empty）(偏移: 0x0)
- `GroupCollection _groupcoll`（组Collection _groupcoll）(偏移: 0x20)
- `Regex _regex`（Regex _regex）(偏移: 0x24)
- `int _textbeg`（int _textbeg）(偏移: 0x28)
- `int _textpos`（int _textpos）(偏移: 0x2C)
- `int _textend`（int _textend）(偏移: 0x30)
- `int _textstart`（int _textstart）(偏移: 0x34)
- `int[][] _matches`（int[][] _matches）(偏移: 0x38)
- `int[] _matchcount`（int[] _matchcount）(偏移: 0x3C)
- `bool _balancing`（bool _balancing）(偏移: 0x40)

### 方法 (13)

- `Match get_Empty()`
  （比赛 get_空（））
- `void Reset(Regex regex, string text, int textbeg, int textend, int textstart)`
  （void 重置（Regex regex, string text, int textbeg, int textend, int textstart））
- `GroupCollection get_Groups()`
  （组Collection get_Groups（））
- `Match NextMatch()`
  （比赛 下一个比赛（））
- `string GroupToStringImpl(int groupnum)`
  （string 组To字符串Impl（int groupnum））
- `string LastGroupToStringImpl()`
  （string 最后一个组To字符串Impl（））
- `void AddMatch(int cap, int start, int len)`
  （void 添加比赛（int cap, int start, int len））
- `void BalanceMatch(int cap)`
  （void Balance比赛（int cap））
- `void RemoveMatch(int cap)`
  （void 移除比赛（int cap））
- `bool IsMatched(int cap)`
  （bool 是否Matched（int cap））
- `int MatchIndex(int cap)`
  （int 比赛索引（int cap））
- `int MatchLength(int cap)`
  （int 比赛Length（int cap））
- `void Tidy(int textpos)`
  （void Tidy（int textpos））

---

## MatchSparse（比赛Sparse）

**继承**: Match（比赛）

### 字段 (1)

- `Hashtable _caps`（哈希表 _caps）(偏移: 0x44)

### 方法 (1)

- `GroupCollection get_Groups()`
  （组Collection get_Groups（））

---

## MatchTargetFieldConstants（比赛目标FieldConstants）

### 字段 (4)

- `MatchTargetFields All`（比赛目标Fields 所有）(偏移: 0x0)
- `MatchTargetFields None`（比赛目标Fields 无）(偏移: 0x4)
- `MatchTargetFields Position`（比赛目标Fields Position）(偏移: 0x8)
- `MatchTargetFields Rotation`（比赛目标Fields Rotation）(偏移: 0xC)

---

## MatchTargetFields（比赛目标Fields）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Material（材质）

**继承**: Object（对象）

### 方法 (73)

- `void CreateWithShader(Material self, Shader shader)`
  （void 创建With着色器（材质 self, 着色器 shader））
- `void CreateWithMaterial(Material self, Material source)`
  （void 创建With材质（材质 self, 材质 source））
- `void CreateWithString(Material self)`
  （void 创建With字符串（材质 self））
- `Shader get_shader()`
  （着色器 get_shader（））
- `void set_shader(Shader value)`
  （void set_shader（着色器 value））
- `Color get_color()`
  （颜色 获取_颜色（））
- `void set_color(Color value)`
  （void 设置_颜色（颜色 value））
- `Texture get_mainTexture()`
  （纹理 获取_主纹理（））
- `void set_mainTexture(Texture value)`
  （void set_main纹理（纹理 value））
- `Vector2 get_mainTextureOffset()`
  （二维向量 get_main纹理Offset（））
- `void set_mainTextureOffset(Vector2 value)`
  （void set_main纹理Offset（二维向量 value））
- `Vector2 get_mainTextureScale()`
  （二维向量 get_main纹理缩放（））
- `void set_mainTextureScale(Vector2 value)`
  （void set_main纹理缩放（二维向量 value））
- `int GetFirstPropertyNameIdByAttribute(ShaderPropertyFlags attributeFlag)`
  （int 获取第一个属性名称IdByAttribute（着色器属性Flags attributeFlag））
- `bool HasProperty(int nameID)`
  （bool 是否有属性（int nameID））
- `bool HasProperty(string name)`
  （bool 是否有属性（string name））
- `int get_renderQueue()`
  （int get_render队列（））
- `void set_renderQueue(int value)`
  （void set_render队列（int value））
- `void EnableKeyword(string keyword)`
  （void 启用Keyword（string keyword））
- `void DisableKeyword(string keyword)`
  （void 禁用Keyword（string keyword））
- `int get_passCount()`
  （int get_pass数量（））
- `bool SetPass(int pass)`
  （bool 集合Pass（int pass））
- `void SetShaderKeywords(string[] names)`
  （void 集合着色器Keywords（string[] names））
- `void set_shaderKeywords(string[] value)`
  （void set_shaderKeywords（string[] value））
- `void SetFloatImpl(int name, float value)`
  （void 集合浮点数Impl（int name, float value））
- `void SetColorImpl(int name, Color value)`
  （void 集合颜色Impl（int name, 颜色 value））
- `void SetMatrixImpl(int name, Matrix4x4 value)`
  （void 集合矩阵Impl（int name, Matrix4x4 value））
- `void SetTextureImpl(int name, Texture value)`
  （void 集合纹理Impl（int name, 纹理 value））
- `void SetConstantBufferImpl(int name, ComputeBuffer value, int offset, int size)`
  （void 集合Constant缓冲区Impl（int name, Compute缓冲区 value, int offset, int size））
- `float GetFloatImpl(int name)`
  （float 获取浮点数Impl（int name））
- `Color GetColorImpl(int name)`
  （颜色 获取颜色Impl（int name））
- `Texture GetTextureImpl(int name)`
  （纹理 获取纹理Impl（int name））
- `void SetMatrixArrayImpl(int name, Matrix4x4[] values, int count)`
  （void 集合矩阵数组Impl（int name, Matrix4x4[] values, int count））
- `Vector4 GetTextureScaleAndOffsetImpl(int name)`
  （Vector4 获取纹理缩放AndOffsetImpl（int name））
- `void SetTextureOffsetImpl(int name, Vector2 offset)`
  （void 集合纹理OffsetImpl（int name, 二维向量 offset））
- `void SetTextureScaleImpl(int name, Vector2 scale)`
  （void 集合纹理缩放Impl（int name, 二维向量 scale））
- `void SetMatrixArray(int name, Matrix4x4[] values, int count)`
  （void 集合矩阵数组（int name, Matrix4x4[] values, int count））
- `void SetFloat(string name, float value)`
  （void 集合浮点数（string name, float value））
- `void SetFloat(int nameID, float value)`
  （void 集合浮点数（int nameID, float value））
- `void SetInt(string name, int value)`
  （void 集合整数（string name, int value））
- `void SetInt(int nameID, int value)`
  （void 集合整数（int nameID, int value））
- `void SetColor(string name, Color value)`
  （void 集合颜色（string name, 颜色 value））
- `void SetColor(int nameID, Color value)`
  （void 集合颜色（int nameID, 颜色 value））
- `void SetVector(string name, Vector4 value)`
  （void 集合向量（string name, Vector4 value））
- `void SetVector(int nameID, Vector4 value)`
  （void 集合向量（int nameID, Vector4 value））
- `void SetMatrix(string name, Matrix4x4 value)`
  （void 集合矩阵（string name, Matrix4x4 value））
- `void SetTexture(string name, Texture value)`
  （void 集合纹理（string name, 纹理 value））
- `void SetTexture(int nameID, Texture value)`
  （void 集合纹理（int nameID, 纹理 value））
- `void SetConstantBuffer(int nameID, ComputeBuffer value, int offset, int size)`
  （void 集合Constant缓冲区（int nameID, Compute缓冲区 value, int offset, int size））
- `void SetMatrixArray(string name, Matrix4x4[] values)`
  （void 集合矩阵数组（string name, Matrix4x4[] values））
- `float GetFloat(string name)`
  （float 获取浮点数（string name））
- `float GetFloat(int nameID)`
  （float 获取浮点数（int nameID））
- `int GetInt(string name)`
  （int 获取整数（string name））
- `Color GetColor(string name)`
  （颜色 获取颜色（string name））
- `Color GetColor(int nameID)`
  （颜色 获取颜色（int nameID））
- `Vector4 GetVector(string name)`
  （Vector4 获取向量（string name））
- `Vector4 GetVector(int nameID)`
  （Vector4 获取向量（int nameID））
- `Texture GetTexture(string name)`
  （纹理 获取纹理（string name））
- `Texture GetTexture(int nameID)`
  （纹理 获取纹理（int nameID））
- `void SetTextureOffset(string name, Vector2 value)`
  （void 集合纹理Offset（string name, 二维向量 value））
- `void SetTextureOffset(int nameID, Vector2 value)`
  （void 集合纹理Offset（int nameID, 二维向量 value））
- `void SetTextureScale(string name, Vector2 value)`
  （void 集合纹理缩放（string name, 二维向量 value））
- `void SetTextureScale(int nameID, Vector2 value)`
  （void 集合纹理缩放（int nameID, 二维向量 value））
- `Vector2 GetTextureOffset(string name)`
  （二维向量 获取纹理Offset（string name））
- `Vector2 GetTextureOffset(int nameID)`
  （二维向量 获取纹理Offset（int nameID））
- `Vector2 GetTextureScale(string name)`
  （二维向量 获取纹理缩放（string name））
- `Vector2 GetTextureScale(int nameID)`
  （二维向量 获取纹理缩放（int nameID））
- `void SetColorImpl_Injected(int name, ref Color value)`
  （void 集合颜色Impl_Injected（int name, ref Color value））
- `void SetMatrixImpl_Injected(int name, ref Matrix4x4 value)`
  （void 集合矩阵Impl_Injected（int name, ref Matrix4x4 value））
- `void GetColorImpl_Injected(int name, out Color ret)`
  （void 获取颜色Impl_Injected（int name, out Color ret））
- `void GetTextureScaleAndOffsetImpl_Injected(int name, out Vector4 ret)`
  （void 获取纹理缩放AndOffsetImpl_Injected（int name, out Vector4 ret））
- `void SetTextureOffsetImpl_Injected(int name, ref Vector2 offset)`
  （void 集合纹理OffsetImpl_Injected（int name, ref Vector2 offset））
- `void SetTextureScaleImpl_Injected(int name, ref Vector2 scale)`
  （void 集合纹理缩放Impl_Injected（int name, ref Vector2 scale））

---

## MaterialCache（材质缓存）

### 方法 (2)

- `Material Register(Material material, Hash128 hash, Action<Material> onModify)`
  （材质 Register（材质 material, Hash128 hash, Action<Material> onModify））
- `void Unregister(Hash128 hash)`
  （void Unregister（Hash128 hash））

---

