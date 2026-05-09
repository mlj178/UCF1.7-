# 游戏类定义 (Part 5/21)

共 200 个类 (总序号 801 - 1000)

---

## CubemapFace（CubemapFace）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CubicBezierDecoder（CubicBezierDecoder）

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

## CullMode（Cull模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CullingAllocationInfo（CullingAllocation信息）

### 字段 (6)

- `VisibleLight* visibleLightsPtr`（可见的Light* visibleLightsPtr）(偏移: 0x0)
- `VisibleLight* visibleOffscreenVertexLightsPtr`（可见的Light* visibleOffscreenVertexLightsPtr）(偏移: 0x4)
- `VisibleReflectionProbe* visibleReflectionProbesPtr`（可见的ReflectionProbe* visibleReflectionProbesPtr）(偏移: 0x8)
- `int visibleLightCount`（int visible光照数量）(偏移: 0xC)
- `int visibleOffscreenVertexLightCount`（int visibleOffscreenVertex光照数量）(偏移: 0x10)
- `int visibleReflectionProbeCount`（int visibleReflectionProbe数量）(偏移: 0x14)

---

## CullingGroup（Culling组）

### 字段 (2)

- `IntPtr m_Ptr`（整数指针 m_指针）(偏移: 0x8)
- `CullingGroup.StateChanged m_OnStateChanged`（CullingGroup.状态Changed m_On状态Changed）(偏移: 0xC)

### 方法 (1)

- `void SendEvents(CullingGroup cullingGroup, IntPtr eventsPtr, int count)`
  （void 发送Events（Culling组 cullingGroup, 整数Ptr eventsPtr, int count））

---

## CullingGroup.StateChanged（CullingGroup.状态Changed）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(CullingGroupEvent sphere)`
  （void Invoke（Culling组事件 sphere））
- `IAsyncResult BeginInvoke(CullingGroupEvent sphere, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Culling组事件 sphere, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## CullingGroupEvent（Culling组事件）

### 字段 (3)

- `int m_Index`（int m_索引）(偏移: 0x0)
- `byte m_PrevState`（byte m_Prev状态）(偏移: 0x4)
- `byte m_ThisState`（byte m_This状态）(偏移: 0x5)

---

## CullingOptions（CullingOptions）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CullingResults（CullingResults）

**继承**: IEquatable<CullingResults>（IEquatable<CullingResults>）

### 字段 (2)

- `IntPtr ptr`（整数Ptr ptr）(偏移: 0x0)
- `CullingAllocationInfo* m_AllocationInfo`（CullingAllocationInfo* m_Allocation信息）(偏移: 0x4)

### 方法 (21)

- `int GetLightIndexCount(IntPtr cullingResultsPtr)`
  （int 获取光照索引数量（整数Ptr cullingResultsPtr））
- `int GetReflectionProbeIndexCount(IntPtr cullingResultsPtr)`
  （int 获取ReflectionProbe索引数量（整数Ptr cullingResultsPtr））
- `void FillLightAndReflectionProbeIndices(IntPtr cullingResultsPtr, ComputeBuffer computeBuffer)`
  （void Fill光照AndReflectionProbeIndices（整数Ptr cullingResultsPtr, Compute缓冲区 computeBuffer））
- `int GetLightIndexMapSize(IntPtr cullingResultsPtr)`
  （int 获取光照索引映射大小（整数Ptr cullingResultsPtr））
- `void FillLightIndexMap(IntPtr cullingResultsPtr, IntPtr indexMapPtr, int indexMapSize)`
  （void Fill光照索引映射（整数Ptr cullingResultsPtr, 整数Ptr indexMapPtr, int indexMapSize））
- `void SetLightIndexMap(IntPtr cullingResultsPtr, IntPtr indexMapPtr, int indexMapSize)`
  （void 集合光照索引映射（整数Ptr cullingResultsPtr, 整数Ptr indexMapPtr, int indexMapSize））
- `bool GetShadowCasterBounds(IntPtr cullingResultsPtr, int lightIndex, out Bounds bounds)`
  （bool 获取ShadowCasterBounds（整数Ptr cullingResultsPtr, int lightIndex, out Bounds bounds））
- `bool ComputeSpotShadowMatricesAndCullingPrimitives(IntPtr cullingResultsPtr, int activeLightIndex, out Matrix4x4 viewMatrix, out Matrix4x4 projMatrix, out ShadowSplitData shadowSplitData)`
  （bool ComputeSpotShadowMatricesAndCullingPrimitives（整数Ptr cullingResultsPtr, int activeLightIndex, out Matrix4x4 viewMatrix, out Matrix4x4 projMatrix, out ShadowSplitData shadowSplitData））
- `bool ComputeDirectionalShadowMatricesAndCullingPrimitives(IntPtr cullingResultsPtr, int activeLightIndex, int splitIndex, int splitCount, Vector3 splitRatio, int shadowResolution, float shadowNearPlaneOffset, out Matrix4x4 viewMatrix, out Matrix4x4 projMatrix, out ShadowSplitData shadowSplitData)`
  （bool ComputeDirectionalShadowMatricesAndCullingPrimitives（整数Ptr cullingResultsPtr, int activeLightIndex, int splitIndex, int splitCount, 三维向量 splitRatio, int shadowResolution, float shadowNearPlaneOffset, out Matrix4x4 viewMatrix, out Matrix4x4 projMatrix, out ShadowSplitData shadowSplitData））
- `NativeArray<VisibleLight> get_visibleLights()`
  （NativeArray<可见的Light> get_visibleLights（））
- `int get_lightAndReflectionProbeIndexCount()`
  （int get_lightAndReflectionProbe索引数量（））
- `void FillLightAndReflectionProbeIndices(ComputeBuffer computeBuffer)`
  （void Fill光照AndReflectionProbeIndices（Compute缓冲区 computeBuffer））
- `NativeArray<int> GetLightIndexMap(Allocator allocator)`
  （NativeArray<int> 获取光照索引映射（Allocator allocator））
- `void SetLightIndexMap(NativeArray<int> lightIndexMap)`
  （void 集合光照索引映射（NativeArray<int> lightIndexMap））
- `bool GetShadowCasterBounds(int lightIndex, out Bounds outBounds)`
  （bool 获取ShadowCasterBounds（int lightIndex, out Bounds outBounds））
- `bool ComputeSpotShadowMatricesAndCullingPrimitives(int activeLightIndex, out Matrix4x4 viewMatrix, out Matrix4x4 projMatrix, out ShadowSplitData shadowSplitData)`
  （bool ComputeSpotShadowMatricesAndCullingPrimitives（int activeLightIndex, out Matrix4x4 viewMatrix, out Matrix4x4 projMatrix, out ShadowSplitData shadowSplitData））
- `bool ComputeDirectionalShadowMatricesAndCullingPrimitives(int activeLightIndex, int splitIndex, int splitCount, Vector3 splitRatio, int shadowResolution, float shadowNearPlaneOffset, out Matrix4x4 viewMatrix, out Matrix4x4 projMatrix, out ShadowSplitData shadowSplitData)`
  （bool ComputeDirectionalShadowMatricesAndCullingPrimitives（int activeLightIndex, int splitIndex, int splitCount, 三维向量 splitRatio, int shadowResolution, float shadowNearPlaneOffset, out Matrix4x4 viewMatrix, out Matrix4x4 projMatrix, out ShadowSplitData shadowSplitData））
- `bool Equals(CullingResults other)`
  （bool Equals（CullingResults other））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `bool ComputeDirectionalShadowMatricesAndCullingPrimitives_Injected(IntPtr cullingResultsPtr, int activeLightIndex, int splitIndex, int splitCount, ref Vector3 splitRatio, int shadowResolution, float shadowNearPlaneOffset, out Matrix4x4 viewMatrix, out Matrix4x4 projMatrix, out ShadowSplitData shadowSplitData)`
  （bool ComputeDirectionalShadowMatricesAndCullingPrimitives_Injected（整数Ptr cullingResultsPtr, int activeLightIndex, int splitIndex, int splitCount, ref Vector3 splitRatio, int shadowResolution, float shadowNearPlaneOffset, out Matrix4x4 viewMatrix, out Matrix4x4 projMatrix, out ShadowSplitData shadowSplitData））

---

## CultureAwareComparer（CultureAwareComparer）

**继承**: StringComparer（字符串Comparer）

### 字段 (3)

- `CompareInfo _compareInfo`（Compare信息 _compare信息）(偏移: 0x8)
- `bool _ignoreCase`（bool _ignoreCase）(偏移: 0xC)
- `CompareOptions _options`（CompareOptions _options）(偏移: 0x10)

### 方法 (5)

- `int Compare(string x, string y)`
  （int Compare（string x, string y））
- `bool Equals(string x, string y)`
  （bool Equals（string x, string y））
- `int GetHashCode(string obj)`
  （int 获取HashCode（string obj））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## CultureData（Culture数据）

### 字段 (21)

- `string sAM1159`（string sAM1159）(偏移: 0x8)
- `string sPM2359`（string sPM2359）(偏移: 0xC)
- `string sTimeSeparator`（string s时间Separator）(偏移: 0x10)
- `string[] saLongTimes`（string[] saLongTimes）(偏移: 0x14)
- `string[] saShortTimes`（string[] saShortTimes）(偏移: 0x18)
- `int iFirstDayOfWeek`（int i第一个DayOfWeek）(偏移: 0x1C)
- `int iFirstWeekOfYear`（int i第一个WeekOfYear）(偏移: 0x20)
- `int[] waCalendars`（int[] waCalendars）(偏移: 0x24)
- `CalendarData[] calendars`（CalendarData[] calendars）(偏移: 0x28)
- `string sISO639Language`（string sISO639Language）(偏移: 0x2C)
- `string sRealName`（string sReal名称）(偏移: 0x30)
- `bool bUseOverrides`（bool bUseOverrides）(偏移: 0x34)
- `int calendarId`（int calendarId）(偏移: 0x38)
- `int numberIndex`（int number索引）(偏移: 0x3C)
- `int iDefaultAnsiCodePage`（int i默认的AnsiCodePage）(偏移: 0x40)
- `int iDefaultOemCodePage`（int i默认的OemCodePage）(偏移: 0x44)
- `int iDefaultMacCodePage`（int i默认的MacCodePage）(偏移: 0x48)
- `int iDefaultEbcdicCodePage`（int i默认的EbcdicCodePage）(偏移: 0x4C)
- `bool isRightToLeft`（bool is右To左）(偏移: 0x50)
- `string sListSeparator`（string s列表Separator）(偏移: 0x54)
- `CultureData s_Invariant`（Culture数据 s_Invariant）(偏移: 0x0)

### 方法 (44)

- `CultureData get_Invariant()`
  （Culture数据 get_Invariant（））
- `CultureData GetCultureData(string cultureName, bool useUserOverride)`
  （Culture数据 获取Culture数据（string cultureName, bool useUserOverride））
- `CultureData GetCultureData(string cultureName, bool useUserOverride, int datetimeIndex, int calendarId, int numberIndex, string iso2lang, int ansiCodePage, int oemCodePage, int macCodePage, int ebcdicCodePage, bool rightToLeft, string listSeparator)`
  （Culture数据 获取Culture数据（string cultureName, bool useUserOverride, int datetimeIndex, int calendarId, int numberIndex, string iso2lang, int ansiCodePage, int oemCodePage, int macCodePage, int ebcdicCodePage, bool rightToLeft, string listSeparator））
- `CultureData GetCultureData(int culture, bool bUseUserOverride)`
  （Culture数据 获取Culture数据（int culture, bool bUseUserOverride））
- `void fill_culture_data(int datetimeIndex)`
  （void fill_culture_data（int datetimeIndex））
- `CalendarData GetCalendar(int calendarId)`
  （Calendar数据 获取Calendar（int calendarId））
- `string[] get_LongTimes()`
  （string[] get_LongTimes（））
- `string[] get_ShortTimes()`
  （string[] get_ShortTimes（））
- `string get_SISO639LANGNAME()`
  （string get_SISO639LANGNAME（））
- `int get_IFIRSTDAYOFWEEK()`
  （int get_IFIRSTDAYOFWEEK（））
- `int get_IFIRSTWEEKOFYEAR()`
  （int get_IFIRSTWEEKOFYEAR（））
- `string get_SAM1159()`
  （string get_SAM1159（））
- `string get_SPM2359()`
  （string get_SPM2359（））
- `string get_TimeSeparator()`
  （string get_时间Separator（））
- `int[] get_CalendarIds()`
  （int[] get_CalendarIds（））
- `bool get_IsInvariantCulture()`
  （bool get_是否InvariantCulture（））
- `string get_CultureName()`
  （string get_Culture名称（））
- `string get_SCOMPAREINFO()`
  （string get_SCOMPAREINFO（））
- `string get_STEXTINFO()`
  （string get_STEXTINFO（））
- `int get_ILANGUAGE()`
  （int get_ILANGUAGE（））
- `bool get_UseUserOverride()`
  （bool get_UseUser重写（））
- `string[] EraNames(int calendarId)`
  （string[] EraNames（int calendarId））
- `string[] AbbrevEraNames(int calendarId)`
  （string[] AbbrevEraNames（int calendarId））
- `string[] AbbreviatedEnglishEraNames(int calendarId)`
  （string[] AbbreviatedEnglishEraNames（int calendarId））
- `string[] ShortDates(int calendarId)`
  （string[] ShortDates（int calendarId））
- `string[] LongDates(int calendarId)`
  （string[] LongDates（int calendarId））
- `string[] YearMonths(int calendarId)`
  （string[] YearMonths（int calendarId））
- `string[] DayNames(int calendarId)`
  （string[] DayNames（int calendarId））
- `string[] AbbreviatedDayNames(int calendarId)`
  （string[] AbbreviatedDayNames（int calendarId））
- `string[] MonthNames(int calendarId)`
  （string[] MonthNames（int calendarId））
- `string[] GenitiveMonthNames(int calendarId)`
  （string[] GenitiveMonthNames（int calendarId））
- `string[] AbbreviatedMonthNames(int calendarId)`
  （string[] AbbreviatedMonthNames（int calendarId））
- `string[] AbbreviatedGenitiveMonthNames(int calendarId)`
  （string[] AbbreviatedGenitiveMonthNames（int calendarId））
- `string[] LeapYearMonthNames(int calendarId)`
  （string[] LeapYearMonthNames（int calendarId））
- `string MonthDay(int calendarId)`
  （string MonthDay（int calendarId））
- `string DateSeparator(int calendarId)`
  （string DateSeparator（int calendarId））
- `string GetDateSeparator(string format)`
  （string 获取DateSeparator（string format））
- `string GetSeparator(string format, string timeParts)`
  （string 获取Separator（string format, string timeParts））
- `int IndexOfTimePart(string format, int startIndex, string timeParts)`
  （int 索引Of时间Part（string format, int startIndex, string timeParts））
- `string UnescapeNlsString(string str, int start, int end)`
  （string UnescapeNls字符串（string str, int start, int end））
- `string[] ReescapeWin32Strings(string[] array)`
  （string[] ReescapeWin32Strings（string[] array））
- `string ReescapeWin32String(string str)`
  （string ReescapeWin32字符串（string str））
- `void GetNFIValues(NumberFormatInfo nfi)`
  （void 获取NFIValues（Number格式化信息 nfi））
- `void fill_number_data(NumberFormatInfo nfi, int numberIndex)`
  （void fill_number_data（Number格式化信息 nfi, int numberIndex））

---

## CultureInfo（Culture信息）

**继承**: ICloneable, IFormatProvider（ICloneable, I格式化提供者）

### 字段 (33)

- `CultureInfo invariant_culture_info`（Culture信息 invariant_culture_info）(偏移: 0x0)
- `object shared_table_lock`（object shared_table_lock）(偏移: 0x4)
- `CultureInfo default_current_culture`（Culture信息 default_current_culture）(偏移: 0x8)
- `bool m_isReadOnly`（布尔值 m_是否只读）(偏移: 0x8)
- `int cultureID`（int cultureID）(偏移: 0xC)
- `int parent_lcid`（int parent_lcid）(偏移: 0x10)
- `int datetime_index`（int datetime_index）(偏移: 0x14)
- `int number_index`（int number_index）(偏移: 0x18)
- `int default_calendar_type`（int default_calendar_type）(偏移: 0x1C)
- `bool m_useUserOverride`（bool m_useUser重写）(偏移: 0x20)
- `NumberFormatInfo numInfo`（Number格式化信息 num信息）(偏移: 0x24)
- `DateTimeFormatInfo dateTimeInfo`（Date时间格式化信息 date时间信息）(偏移: 0x28)
- `TextInfo textInfo`（文本信息 text信息）(偏移: 0x2C)
- `string m_name`（字符串 m_名称）(偏移: 0x30)
- `string englishname`（string englishname）(偏移: 0x34)
- `string nativename`（string nativename）(偏移: 0x38)
- `string iso3lang`（string iso3lang）(偏移: 0x3C)
- `string iso2lang`（string iso2lang）(偏移: 0x40)
- `string win3lang`（string win3lang）(偏移: 0x44)
- `string territory`（string territory）(偏移: 0x48)
- `string[] native_calendar_names`（string[] native_calendar_names）(偏移: 0x4C)
- `CompareInfo compareInfo`（Compare信息 compare信息）(偏移: 0x50)
- `void* textinfo_data`（void* textinfo_data）(偏移: 0x54)
- `int m_dataItem`（int m_data项目）(偏移: 0x58)
- `Calendar calendar`（Calendar calendar）(偏移: 0x5C)
- `CultureInfo parent_culture`（Culture信息 parent_culture）(偏移: 0x60)
- `bool constructed`（bool constructed）(偏移: 0x64)
- `byte[] cached_serialized_form`（byte[] cached_serialized_form）(偏移: 0x68)
- `CultureData m_cultureData`（Culture数据 m_culture数据）(偏移: 0x6C)
- `bool m_isInherited`（bool m_isInherited）(偏移: 0x70)
- `CultureInfo s_DefaultThreadCurrentUICulture`（Culture信息 s_默认的Thread当前界面Culture）(偏移: 0xC)
- `CultureInfo s_DefaultThreadCurrentCulture`（Culture信息 s_默认的Thread当前Culture）(偏移: 0x10)
- `bool IsTaiwanSku`（bool 是否TaiwanSku）(偏移: 0x1C)

### 方法 (51)

- `CultureInfo get_InvariantCulture()`
  （Culture信息 get_InvariantCulture（））
- `CultureInfo get_CurrentCulture()`
  （Culture信息 get_当前Culture（））
- `CultureInfo get_CurrentUICulture()`
  （Culture信息 get_当前界面Culture（））
- `CultureInfo ConstructCurrentCulture()`
  （Culture信息 Construct当前Culture（））
- `CultureInfo ConstructCurrentUICulture()`
  （Culture信息 Construct当前界面Culture（））
- `string get_Territory()`
  （string get_Territory（））
- `int get_LCID()`
  （int get_LCID（））
- `string get_Name()`
  （字符串 获取_名称（））
- `Calendar get_Calendar()`
  （Calendar get_Calendar（））
- `CultureInfo get_Parent()`
  （Culture信息 get_父级（））
- `TextInfo get_TextInfo()`
  （文本信息 get_文本信息（））
- `object Clone()`
  （对象 克隆（））
- `bool Equals(object value)`
  （布尔值 等于（对象 value））
- `CultureInfo[] GetCultures(CultureTypes types)`
  （CultureInfo[] 获取Cultures（CultureTypes types））
- `CultureInfo.Data GetTextInfoData()`
  （CultureInfo.数据 获取文本信息数据（））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `string ToString()`
  （字符串 转字符串（））
- `CompareInfo get_CompareInfo()`
  （Compare信息 get_Compare信息（））
- `bool get_IsNeutralCulture()`
  （bool get_是否NeutralCulture（））
- `void CheckNeutral()`
  （void 检查Neutral（））
- `NumberFormatInfo get_NumberFormat()`
  （Number格式化信息 get_Number格式化（））
- `void set_NumberFormat(NumberFormatInfo value)`
  （void set_Number格式化（Number格式化信息 value））
- `DateTimeFormatInfo get_DateTimeFormat()`
  （Date时间格式化信息 get_Date时间格式化（））
- `void set_DateTimeFormat(DateTimeFormatInfo value)`
  （void set_Date时间格式化（Date时间格式化信息 value））
- `string get_EnglishName()`
  （string get_English名称（））
- `bool get_IsReadOnly()`
  （布尔值 获取_是否只读（））
- `object GetFormat(Type formatType)`
  （object 获取格式化（类型 formatType））
- `void Construct()`
  （void Construct（））
- `bool construct_internal_locale_from_lcid(int lcid)`
  （bool construct_internal_locale_from_lcid（int lcid））
- `bool construct_internal_locale_from_name(string name)`
  （bool construct_internal_locale_from_name（string name））
- `string get_current_locale_name()`
  （string get_current_locale_name（））
- `CultureInfo[] internal_get_cultures(bool neutral, bool specific, bool installed)`
  （CultureInfo[] internal_get_cultures（bool neutral, bool specific, bool installed））
- `void ConstructInvariant(bool read_only)`
  （void ConstructInvariant（bool read_only））
- `TextInfo CreateTextInfo(bool readOnly)`
  （文本信息 创建文本信息（bool readOnly））
- `void insert_into_shared_tables(CultureInfo c)`
  （void insert_into_shared_tables（Culture信息 c））
- `CultureInfo GetCultureInfo(int culture)`
  （Culture信息 获取Culture信息（int culture））
- `CultureInfo GetCultureInfo(string name)`
  （Culture信息 获取Culture信息（string name））
- `CultureInfo CreateCulture(string name, bool reference)`
  （Culture信息 创建Culture（string name, bool reference））
- `CultureInfo CreateSpecificCulture(string name)`
  （Culture信息 创建SpecificCulture（string name））
- `CultureInfo CreateSpecificCultureFromNeutral(string name)`
  （Culture信息 创建SpecificCultureFromNeutral（string name））
- `int get_CalendarType()`
  （int get_Calendar类型（））
- `Calendar CreateCalendar(int calendarType)`
  （Calendar 创建Calendar（int calendarType））
- `Exception CreateNotFoundException(string name)`
  （Exception 创建NotFoundException（string name））
- `CultureInfo get_DefaultThreadCurrentCulture()`
  （Culture信息 get_默认的Thread当前Culture（））
- `CultureInfo get_DefaultThreadCurrentUICulture()`
  （Culture信息 get_默认的Thread当前界面Culture（））
- `string get_SortName()`
  （string get_Sort名称（））
- `CultureInfo get_UserDefaultUICulture()`
  （Culture信息 get_User默认的界面Culture（））
- `CultureInfo get_UserDefaultCulture()`
  （Culture信息 get_User默认的Culture（））
- `void CheckDomainSafetyObject(object obj, object container)`
  （void 检查DomainSafety对象（object obj, object container））
- `bool get_HasInvariantCultureName()`
  （bool get_是否有InvariantCulture名称（））
- `bool VerifyCultureName(string cultureName, bool throwException)`
  （bool VerifyCulture名称（string cultureName, bool throwException））

---

## CultureInfo.Data（CultureInfo.数据）

### 字段 (6)

- `int ansi`（int ansi）(偏移: 0x0)
- `int ebcdic`（int ebcdic）(偏移: 0x4)
- `int mac`（int mac）(偏移: 0x8)
- `int oem`（int oem）(偏移: 0xC)
- `bool right_to_left`（bool right_to_left）(偏移: 0x10)
- `byte list_sep`（byte list_sep）(偏移: 0x11)

---

## CultureNotFoundException（CultureNotFoundException）

**继承**: ArgumentException, ISerializable（ArgumentException, ISerializable）

### 字段 (2)

- `string m_invalidCultureName`（string m_invalidCulture名称）(偏移: 0x48)
- `Nullable<int> m_invalidCultureId`（Nullable<int> m_invalidCultureId）(偏移: 0x4C)

### 方法 (6)

- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））
- `Nullable<int> get_InvalidCultureId()`
  （Nullable<int> get_InvalidCultureId（））
- `string get_InvalidCultureName()`
  （string get_InvalidCulture名称（））
- `string get_DefaultMessage()`
  （string get_默认的Message（））
- `string get_FormatedInvalidCultureId()`
  （string get_FormatedInvalidCultureId（））
- `string get_Message()`
  （字符串 获取_消息（））

---

## CultureTypes（CultureTypes）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CurrentSystemTimeZone（当前系统时间Zone）

**继承**: TimeZone（时间Zone）

### 字段 (1)

- `TimeZoneInfo LocalTimeZone`（时间Zone信息 本地的时间Zone）(偏移: 0x8)

### 方法 (1)

- `bool GetTimeZoneData(int year, out long[] data, out string[] names, out bool daylight_inverted)`
  （bool 获取时间Zone数据（int year, out long[] data, out string[] names, out bool daylight_inverted））

---

## Cursor（Cursor）

### 方法 (2)

- `CursorLockMode get_lockState()`
  （CursorLock模式 get_lock状态（））
- `void set_lockState(CursorLockMode value)`
  （void set_lock状态（CursorLock模式 value））

---

## CursorLockMode（CursorLock模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## CustomAttributeData（自定义的Attribute数据）

### 字段 (4)

- `ConstructorInfo ctorInfo`（Constructor信息 ctor信息）(偏移: 0x8)
- `IList<CustomAttributeTypedArgument> ctorArgs`（IList<自定义的AttributeTypedArgument> ctorArgs）(偏移: 0xC)
- `IList<CustomAttributeNamedArgument> namedArgs`（IList<自定义的AttributeNamedArgument> namedArgs）(偏移: 0x10)
- `CustomAttributeData.LazyCAttrData lazyData`（自定义的AttributeData.LazyCAttr数据 lazy数据）(偏移: 0x14)

### 方法 (14)

- `void ResolveArgumentsInternal(ConstructorInfo ctor, Assembly assembly, IntPtr data, uint data_length, out object[] ctorArgs, out object[] namedArgs)`
  （void ResolveArguments内部的（Constructor信息 ctor, Assembly assembly, 整数Ptr data, uint data_length, out object[] ctorArgs, out object[] namedArgs））
- `void ResolveArguments()`
  （void ResolveArguments（））
- `ConstructorInfo get_Constructor()`
  （Constructor信息 get_Constructor（））
- `IList<CustomAttributeTypedArgument> get_ConstructorArguments()`
  （IList<自定义的AttributeTypedArgument> get_ConstructorArguments（））
- `IList<CustomAttributeNamedArgument> get_NamedArguments()`
  （IList<自定义的AttributeNamedArgument> get_NamedArguments（））
- `IList<CustomAttributeData> GetCustomAttributes(Assembly target)`
  （IList<自定义的AttributeData> 获取自定义的Attributes（Assembly target））
- `IList<CustomAttributeData> GetCustomAttributes(MemberInfo target)`
  （IList<自定义的AttributeData> 获取自定义的Attributes（Member信息 target））
- `IList<CustomAttributeData> GetCustomAttributesInternal(RuntimeType target)`
  （IList<自定义的AttributeData> 获取自定义的Attributes内部的（Runtime类型 target））
- `IList<CustomAttributeData> GetCustomAttributes(Module target)`
  （IList<自定义的AttributeData> 获取自定义的Attributes（模块 target））
- `IList<CustomAttributeData> GetCustomAttributes(ParameterInfo target)`
  （IList<自定义的AttributeData> 获取自定义的Attributes（Parameter信息 target））
- `Type get_AttributeType()`
  （类型 get_Attribute类型（））
- `string ToString()`
  （字符串 转字符串（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## CustomAttributeData.LazyCAttrData（自定义的AttributeData.LazyCAttr数据）

### 字段 (3)

- `Assembly assembly`（Assembly assembly）(偏移: 0x8)
- `IntPtr data`（整数Ptr data）(偏移: 0xC)
- `uint data_length`（uint data_length）(偏移: 0x10)

---

## CustomAttributeExtensions（自定义的AttributeExtensions）

### 方法 (1)

- `Attribute GetCustomAttribute(Assembly element, Type attributeType)`
  （Attribute 获取自定义的Attribute（Assembly element, 类型 attributeType））

---

## CustomAttributeNamedArgument（自定义的AttributeNamedArgument）

### 字段 (2)

- `CustomAttributeTypedArgument typedArgument`（自定义的AttributeTypedArgument typedArgument）(偏移: 0x0)
- `MemberInfo memberInfo`（Member信息 member信息）(偏移: 0x8)

### 方法 (5)

- `MemberInfo get_MemberInfo()`
  （Member信息 get_Member信息（））
- `CustomAttributeTypedArgument get_TypedValue()`
  （自定义的AttributeTypedArgument get_Typed值（））
- `string ToString()`
  （字符串 转字符串（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## CustomAttributeTypedArgument（自定义的AttributeTypedArgument）

### 字段 (2)

- `Type argumentType`（类型 argument类型）(偏移: 0x0)
- `object value`（对象 value）(偏移: 0x4)

### 方法 (4)

- `object get_Value()`
  （对象 获取_值（））
- `string ToString()`
  （字符串 转字符串（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## CustomRenderTextureManager（自定义的Render纹理管理器）

### 字段 (2)

- `Action<CustomRenderTexture> textureLoaded`（Action<自定义的RenderTexture> textureLoaded）(偏移: 0x0)
- `Action<CustomRenderTexture> textureUnloaded`（Action<自定义的RenderTexture> textureUnloaded）(偏移: 0x4)

### 方法 (2)

- `void InvokeOnTextureLoaded_Internal(CustomRenderTexture source)`
  （void InvokeOn纹理Loaded_内部的（自定义的Render纹理 source））
- `void InvokeOnTextureUnloaded_Internal(CustomRenderTexture source)`
  （void InvokeOn纹理Unloaded_内部的（自定义的Render纹理 source））

---

## CustomSampler（自定义的Sampler）

**继承**: Sampler（Sampler）

### 字段 (1)

- `CustomSampler s_InvalidCustomSampler`（自定义的Sampler s_Invalid自定义的Sampler）(偏移: 0x0)

### 方法 (2)

- `CustomSampler Create(string name, bool collectGpuData = False)`
  （自定义的Sampler 创建（string name, bool collectGpuData = False））
- `IntPtr CreateInternal(string name, bool collectGpuData)`
  （整数Ptr 创建内部的（string name, bool collectGpuData））

---

## CustomTexSheet（自定义的TexSheet）

**继承**: RO_WorkListener（RO_Work监听器）

### 字段 (10)

- `Material mat`（材质 mat）(偏移: 0xC)
- `Texture2D[] textures`（Texture2D[] textures）(偏移: 0x10)
- `float duration`（浮点数 持续时间）(偏移: 0x14)
- `int cycle`（int cycle）(偏移: 0x18)
- `float lifeOfCycle`（float lifeOfCycle）(偏移: 0x1C)
- `float delay`（浮点数 延迟）(偏移: 0x20)
- `float lifeTime`（float life时间）(偏移: 0x24)
- `Gradient colorOverLife`（Gradient colorOverLife）(偏移: 0x28)
- `float startTime`（float start时间）(偏移: 0x2C)
- `bool isContinuous`（bool isContinuous）(偏移: 0x30)

### 方法 (5)

- `void Awake()`
  （void 唤醒（））
- `void Update()`
  （void 更新（））
- `void UpdateMaterial(float lifeRate)`
  （void 更新材质（float lifeRate））
- `void Work()`
  （void 工作（））
- `void PlayOnce()`
  （void 播放Once（））

---

## CustomTypeDescriptor（自定义的类型Descriptor）

**继承**: ICustomTypeDescriptor（I自定义类型描述符）

### 字段 (1)

- `ICustomTypeDescriptor _parent`（I自定义的类型Descriptor _parent）(偏移: 0x8)

### 方法 (11)

- `AttributeCollection GetAttributes()`
  （AttributeCollection 获取Attributes（））
- `string GetClassName()`
  （string 获取类名称（））
- `string GetComponentName()`
  （string 获取组件名称（））
- `TypeConverter GetConverter()`
  （类型Converter 获取Converter（））
- `EventDescriptor GetDefaultEvent()`
  （事件Descriptor 获取默认的事件（））
- `PropertyDescriptor GetDefaultProperty()`
  （属性Descriptor 获取默认的属性（））
- `object GetEditor(Type editorBaseType)`
  （object 获取Editor（类型 editorBaseType））
- `EventDescriptorCollection GetEvents()`
  （事件DescriptorCollection 获取Events（））
- `EventDescriptorCollection GetEvents(Attribute[] attributes)`
  （事件DescriptorCollection 获取Events（Attribute[] attributes））
- `PropertyDescriptorCollection GetProperties()`
  （属性DescriptorCollection 获取Properties（））
- `PropertyDescriptorCollection GetProperties(Attribute[] attributes)`
  （属性DescriptorCollection 获取Properties（Attribute[] attributes））

---

## CustomYieldInstruction（自定义Yield指令）

**继承**: IEnumerator（IEnumerator枚举器）

### 方法 (3)

- `object get_Current()`
  （对象 获取_当前（））
- `bool MoveNext()`
  （布尔值 移动下一个（））
- `void Reset()`
  （void 重置（））

---

## DBNull（DBNull）

**继承**: ISerializable, IConvertible（ISerializable, IConvertible）

### 字段 (1)

- `DBNull Value`（DBNull 值）(偏移: 0x0)

### 方法 (4)

- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））
- `string ToString()`
  （字符串 转字符串（））
- `string ToString(IFormatProvider provider)`
  （字符串 转字符串（I格式化提供者 provider））
- `TypeCode GetTypeCode()`
  （类型代码 获取类型代码（））

---

## DES（DES）

**继承**: SymmetricAlgorithm（对称算法）

### 字段 (2)

- `KeySizes[] s_legalBlockSizes`（密钥大小[] s_合法块大小）(偏移: 0x0)
- `KeySizes[] s_legalKeySizes`（密钥大小[] s_合法密钥大小）(偏移: 0x4)

### 方法 (7)

- `byte[] get_Key()`
  （字节[] 获取_键（））
- `void set_Key(byte[] value)`
  （void 设置_键（字节[] value））
- `DES Create()`
  （DES 创建（））
- `bool IsWeakKey(byte[] rgbKey)`
  （bool 是否Weak键（byte[] rgbKey））
- `bool IsSemiWeakKey(byte[] rgbKey)`
  （bool 是否SemiWeak键（byte[] rgbKey））
- `bool IsLegalKeySize(byte[] rgbKey)`
  （bool 是否Legal键大小（byte[] rgbKey））
- `ulong QuadWordFromBigEndian(byte[] block)`
  （ulong QuadWordFromBigEndian（byte[] block））

---

## DESCryptoServiceProvider（DESCrypto服务提供者）

**继承**: DES（DES）

### 方法 (4)

- `ICryptoTransform CreateEncryptor(byte[] rgbKey, byte[] rgbIV)`
  （ICrypto变换 创建Encryptor（byte[] rgbKey, byte[] rgbIV））
- `ICryptoTransform CreateDecryptor(byte[] rgbKey, byte[] rgbIV)`
  （ICrypto变换 创建Decryptor（byte[] rgbKey, byte[] rgbIV））
- `void GenerateKey()`
  （void 生成密钥（））
- `void GenerateIV()`
  （void 生成IV（））

---

## DESTransform（DES变换）

**继承**: SymmetricTransform（对称变换）

### 字段 (13)

- `int KEY_BIT_SIZE`（int KEY_BIT_SIZE）(偏移: 0x0)
- `int KEY_BYTE_SIZE`（int KEY_BYTE_SIZE）(偏移: 0x4)
- `int BLOCK_BIT_SIZE`（int BLOCK_BIT_SIZE）(偏移: 0x8)
- `int BLOCK_BYTE_SIZE`（int BLOCK_BYTE_SIZE）(偏移: 0xC)
- `byte[] keySchedule`（byte[] keySchedule）(偏移: 0x34)
- `byte[] byteBuff`（byte[] byte增益）(偏移: 0x38)
- `uint[] dwordBuff`（uint[] dword增益）(偏移: 0x3C)
- `uint[] spBoxes`（uint[] spBoxes）(偏移: 0x10)
- `byte[] PC1`（byte[] PC1）(偏移: 0x14)
- `byte[] leftRotTotal`（byte[] leftRotTotal）(偏移: 0x18)
- `byte[] PC2`（byte[] PC2）(偏移: 0x1C)
- `uint[] ipTab`（uint[] ipTab）(偏移: 0x20)
- `uint[] fpTab`（uint[] fpTab）(偏移: 0x24)

### 方法 (7)

- `uint CipherFunct(uint r, int n)`
  （uint CipherFunct（uint r, int n））
- `void Permutation(byte[] input, byte[] output, uint[] permTab, bool preSwap)`
  （void Permutation（byte[] input, byte[] output, uint[] permTab, bool preSwap））
- `void BSwap(byte[] byteBuff)`
  （void BSwap（byte[] byteBuff））
- `void SetKey(byte[] key)`
  （void 集合键（byte[] key））
- `void ProcessBlock(byte[] input, byte[] output)`
  （void 处理Block（byte[] input, byte[] output））
- `void ECB(byte[] input, byte[] output)`
  （void ECB（字节[] input, 字节[] output））
- `byte[] GetStrongKey()`
  （byte[] 获取Strong键（））

---

## DOCurve.CubicBezier（DOCurve.CubicBezier）

### 方法 (3)

- `Vector3 GetPointOnSegment(Vector3 startPoint, Vector3 startControlPoint, Vector3 endPoint, Vector3 endControlPoint, float factor)`
  （三维向量 获取PointOnSegment（三维向量 startPoint, 三维向量 startControlPoint, 三维向量 endPoint, 三维向量 endControlPoint, float factor））
- `Vector3[] GetSegmentPointCloud(Vector3 startPoint, Vector3 startControlPoint, Vector3 endPoint, Vector3 endControlPoint, int resolution = 10)`
  （Vector3[] 获取SegmentPointCloud（三维向量 startPoint, 三维向量 startControlPoint, 三维向量 endPoint, 三维向量 endControlPoint, int resolution = 10））
- `void GetSegmentPointCloud(List<Vector3> addToList, Vector3 startPoint, Vector3 startControlPoint, Vector3 endPoint, Vector3 endControlPoint, int resolution = 10)`
  （void 获取SegmentPointCloud（List<Vector3> addToList, 三维向量 startPoint, 三维向量 startControlPoint, 三维向量 endPoint, 三维向量 endControlPoint, int resolution = 10））

---

## DOTween（DOTween）

### 字段 (30)

- `string Version`（string Version）(偏移: 0x0)
- `bool useSafeMode`（bool useSafe模式）(偏移: 0x4)
- `SafeModeLogBehaviour safeModeLogBehaviour`（Safe模式LogBehaviour safe模式LogBehaviour）(偏移: 0x8)
- `NestedTweenFailureBehaviour nestedTweenFailureBehaviour`（NestedTweenFailureBehaviour nestedTweenFailureBehaviour）(偏移: 0xC)
- `bool showUnityEditorReport`（bool showUnity引擎EditorReport）(偏移: 0x10)
- `float timeScale`（float time缩放）(偏移: 0x14)
- `bool useSmoothDeltaTime`（bool useSmoothDelta时间）(偏移: 0x18)
- `float maxSmoothUnscaledTime`（float maxSmoothUnscaled时间）(偏移: 0x1C)
- `RewindCallbackMode rewindCallbackMode`（Rewind回调模式 rewind回调模式）(偏移: 0x20)
- `LogBehaviour _logBehaviour`（LogBehaviour _logBehaviour）(偏移: 0x24)
- `bool drawGizmos`（bool drawGizmos）(偏移: 0x2C)
- `bool debugMode`（bool debug模式）(偏移: 0x2D)
- `bool _fooDebugStoreTargetId`（bool _fooDebug商店目标Id）(偏移: 0x2E)
- `UpdateType defaultUpdateType`（更新类型 default更新类型）(偏移: 0x30)
- `bool defaultTimeScaleIndependent`（bool default时间缩放Independent）(偏移: 0x34)
- `AutoPlay defaultAutoPlay`（自动播放 default自动播放）(偏移: 0x38)
- `bool defaultAutoKill`（bool default自动击杀）(偏移: 0x3C)
- `LoopType defaultLoopType`（Loop类型 defaultLoop类型）(偏移: 0x40)
- `bool defaultRecyclable`（bool defaultRecyclable）(偏移: 0x44)
- `Ease defaultEaseType`（Ease defaultEase类型）(偏移: 0x48)
- `float defaultEaseOvershootOrAmplitude`（float defaultEaseOvershootOrAmplitude）(偏移: 0x4C)
- `float defaultEasePeriod`（float defaultEasePeriod）(偏移: 0x50)
- `DOTweenComponent instance`（DOTween组件 instance）(偏移: 0x54)
- `bool _foo_isQuitting`（bool _foo_isQuitting）(偏移: 0x58)
- `int maxActiveTweenersReached`（int max激活的TweenersReached）(偏移: 0x5C)
- `int maxActiveSequencesReached`（int max激活的SequencesReached）(偏移: 0x60)
- `SafeModeReport safeModeReport`（Safe模式Report safe模式Report）(偏移: 0x64)
- `List<TweenCallback> GizmosDelegates`（List<TweenCallback> GizmosDelegates）(偏移: 0x74)
- `bool initialized`（bool initialized）(偏移: 0x78)
- `int _isQuittingFrame`（int _isQuittingFrame）(偏移: 0x7C)

### 方法 (61)

- `LogBehaviour get_logBehaviour()`
  （LogBehaviour get_logBehaviour（））
- `void set_logBehaviour(LogBehaviour value)`
  （void set_logBehaviour（LogBehaviour value））
- `bool get_debugStoreTargetId()`
  （bool get_debug商店目标Id（））
- `void set_debugStoreTargetId(bool value)`
  （void set_debug商店目标Id（bool value））
- `bool get_isQuitting()`
  （bool get_isQuitting（））
- `void set_isQuitting(bool value)`
  （void set_isQuitting（bool value））
- `IDOTweenInit Init(Nullable<bool> recycleAllByDefault, Nullable<bool> useSafeMode, Nullable<LogBehaviour> logBehaviour)`
  （IDOTween初始化 初始化（Nullable<bool> recycleAllByDefault, Nullable<bool> useSafeMode, Nullable<LogBehaviour> logBehaviour））
- `void AutoInit()`
  （void 自动初始化（））
- `IDOTweenInit Init(DOTweenSettings settings, Nullable<bool> recycleAllByDefault, Nullable<bool> useSafeMode, Nullable<LogBehaviour> logBehaviour)`
  （IDOTween初始化 初始化（DOTweenSettings settings, Nullable<bool> recycleAllByDefault, Nullable<bool> useSafeMode, Nullable<LogBehaviour> logBehaviour））
- `void SetTweensCapacity(int tweenersCapacity, int sequencesCapacity)`
  （void 集合TweensCapacity（int tweenersCapacity, int sequencesCapacity））
- `void Clear(bool destroy = False)`
  （void 清除（bool destroy = False））
- `void Clear(bool destroy, bool isApplicationQuitting)`
  （void 清除（bool destroy, bool isApplicationQuitting））
- `void ClearCachedTweens()`
  （void 清除CachedTweens（））
- `int Validate()`
  （int 验证（））
- `void ManualUpdate(float deltaTime, float unscaledDeltaTime)`
  （void 手动更新（float deltaTime, float unscaledDeltaTime））
- `Tweener To(DOGetter<RectOffset> getter, DOSetter<RectOffset> setter, RectOffset endValue, float duration)`
  （Tweener To（DOGetter<RectOffset> getter, DOSetter<RectOffset> setter, RectOffset endValue, float duration））
- `Tweener To(DOSetter<float> setter, float startValue, float endValue, float duration)`
  （Tweener To（DOSetter<float> setter, float startValue, float endValue, float duration））
- `Sequence Sequence()`
  （Sequence Sequence（））
- `Sequence Sequence(object target)`
  （Sequence Sequence（object target））
- `int CompleteAll(bool withCallbacks = False)`
  （int Complete所有（bool withCallbacks = False））
- `int Complete(object targetOrId, bool withCallbacks = False)`
  （int Complete（object targetOrId, bool withCallbacks = False））
- `int CompleteAndReturnKilledTot()`
  （int CompleteAndReturnKilledTot（））
- `int CompleteAndReturnKilledTot(object targetOrId)`
  （int CompleteAndReturnKilledTot（object targetOrId））
- `int CompleteAndReturnKilledTot(object target, object id)`
  （int CompleteAndReturnKilledTot（object target, object id））
- `int CompleteAndReturnKilledTotExceptFor(object[] excludeTargetsOrIds)`
  （int CompleteAndReturnKilledTotExceptFor（object[] excludeTargetsOrIds））
- `int FlipAll()`
  （int Flip所有（））
- `int Flip(object targetOrId)`
  （int Flip（object targetOrId））
- `int GotoAll(float to, bool andPlay = False)`
  （int Goto所有（float to, bool andPlay = False））
- `int Goto(object targetOrId, float to, bool andPlay = False)`
  （int Goto（object targetOrId, float to, bool andPlay = False））
- `int KillAll(bool complete = False)`
  （int 击杀所有（bool complete = False））
- `int KillAll(bool complete, object[] idsOrTargetsToExclude)`
  （int 击杀所有（bool complete, object[] idsOrTargetsToExclude））
- `int Kill(object targetOrId, bool complete = False)`
  （int 击杀（object targetOrId, bool complete = False））
- `int Kill(object target, object id, bool complete = False)`
  （int 击杀（object target, object id, bool complete = False））
- `int PauseAll()`
  （int 暂停所有（））
- `int Pause(object targetOrId)`
  （int 暂停（object targetOrId））
- `int PlayAll()`
  （int 播放所有（））
- `int Play(object targetOrId)`
  （int 播放（object targetOrId））
- `int Play(object target, object id)`
  （int 播放（object target, object id））
- `int PlayBackwardsAll()`
  （int 播放Backwards所有（））
- `int PlayBackwards(object targetOrId)`
  （int 播放Backwards（object targetOrId））
- `int PlayBackwards(object target, object id)`
  （int 播放Backwards（object target, object id））
- `int PlayForwardAll()`
  （int 播放前进所有（））
- `int PlayForward(object targetOrId)`
  （int 播放前进（object targetOrId））
- `int PlayForward(object target, object id)`
  （int 播放前进（object target, object id））
- `int RestartAll(bool includeDelay = True)`
  （int Restart所有（bool includeDelay = True））
- `int Restart(object targetOrId, bool includeDelay = True, float changeDelayTo = -1)`
  （int Restart（object targetOrId, bool includeDelay = True, float changeDelayTo = -1））
- `int Restart(object target, object id, bool includeDelay = True, float changeDelayTo = -1)`
  （int Restart（object target, object id, bool includeDelay = True, float changeDelayTo = -1））
- `int RewindAll(bool includeDelay = True)`
  （int Rewind所有（bool includeDelay = True））
- `int Rewind(object targetOrId, bool includeDelay = True)`
  （int Rewind（object targetOrId, bool includeDelay = True））
- `int SmoothRewindAll()`
  （int SmoothRewind所有（））
- `int SmoothRewind(object targetOrId)`
  （int SmoothRewind（object targetOrId））
- `int TogglePauseAll()`
  （int 开关暂停所有（））
- `int TogglePause(object targetOrId)`
  （int 开关暂停（object targetOrId））
- `bool IsTweening(object targetOrId, bool alsoCheckIfIsPlaying = False)`
  （bool 是否Tweening（object targetOrId, bool alsoCheckIfIsPlaying = False））
- `int TotalActiveTweens()`
  （int Total激活的Tweens（））
- `int TotalPlayingTweens()`
  （int TotalPlayingTweens（））
- `List<Tween> PlayingTweens(List<Tween> fillableList)`
  （List<Tween> PlayingTweens（List<Tween> fillableList））
- `List<Tween> PausedTweens(List<Tween> fillableList)`
  （List<Tween> PausedTweens（List<Tween> fillableList））
- `List<Tween> TweensById(object id, bool playingOnly = False, List<Tween> fillableList)`
  （List<Tween> TweensById（object id, bool playingOnly = False, List<Tween> fillableList））
- `List<Tween> TweensByTarget(object target, bool playingOnly = False, List<Tween> fillableList)`
  （List<Tween> TweensBy目标（object target, bool playingOnly = False, List<Tween> fillableList））
- `void InitCheck()`
  （void 初始化检查（））

---

## DOTweenCYInstruction.WaitForCompletion（DOTweenCYInstruction.WaitForCompletion）

**继承**: CustomYieldInstruction（自定义Yield指令）

### 字段 (1)

- `Tween t`（补间 t）(偏移: 0x8)

### 方法 (1)

- `bool get_keepWaiting()`
  （布尔值 获取_保持等待（））

---

## DOTweenCYInstruction.WaitForElapsedLoops（DOTweenCYInstruction.WaitForElapsedLoops）

**继承**: CustomYieldInstruction（自定义Yield指令）

### 字段 (2)

- `Tween t`（补间 t）(偏移: 0x8)
- `int elapsedLoops`（int elapsedLoops）(偏移: 0xC)

### 方法 (1)

- `bool get_keepWaiting()`
  （布尔值 获取_保持等待（））

---

## DOTweenCYInstruction.WaitForKill（DOTweenCYInstruction.WaitFor击杀）

**继承**: CustomYieldInstruction（自定义Yield指令）

### 字段 (1)

- `Tween t`（补间 t）(偏移: 0x8)

### 方法 (1)

- `bool get_keepWaiting()`
  （布尔值 获取_保持等待（））

---

## DOTweenCYInstruction.WaitForPosition（DOTweenCYInstruction.WaitForPosition）

**继承**: CustomYieldInstruction（自定义Yield指令）

### 字段 (2)

- `Tween t`（补间 t）(偏移: 0x8)
- `float position`（float position）(偏移: 0xC)

### 方法 (1)

- `bool get_keepWaiting()`
  （布尔值 获取_保持等待（））

---

## DOTweenCYInstruction.WaitForRewind（DOTweenCYInstruction.WaitForRewind）

**继承**: CustomYieldInstruction（自定义Yield指令）

### 字段 (1)

- `Tween t`（补间 t）(偏移: 0x8)

### 方法 (1)

- `bool get_keepWaiting()`
  （布尔值 获取_保持等待（））

---

## DOTweenCYInstruction.WaitForStart（DOTweenCYInstruction.WaitFor开始）

**继承**: CustomYieldInstruction（自定义Yield指令）

### 字段 (1)

- `Tween t`（补间 t）(偏移: 0x8)

### 方法 (1)

- `bool get_keepWaiting()`
  （布尔值 获取_保持等待（））

---

## DOTweenComponent（DOTween组件）

**继承**: MonoBehaviour, IDOTweenInit（MonoBehaviour行为, IDOTween初始化）

### 字段 (7)

- `int inspectorUpdater`（int inspectorUpdater）(偏移: 0xC)
- `float _unscaledTime`（float _unscaled时间）(偏移: 0x10)
- `float _unscaledDeltaTime`（float _unscaledDelta时间）(偏移: 0x14)
- `bool _paused`（bool _paused）(偏移: 0x18)
- `float _pausedTime`（float _paused时间）(偏移: 0x1C)
- `bool _isQuitting`（bool _isQuitting）(偏移: 0x20)
- `bool _duplicateToDestroy`（bool _duplicateTo销毁）(偏移: 0x21)

### 方法 (18)

- `void Awake()`
  （void 唤醒（））
- `void Start()`
  （void 开始（））
- `void Update()`
  （void 更新（））
- `void LateUpdate()`
  （void 延迟更新（））
- `void FixedUpdate()`
  （void 固定更新（））
- `void OnDrawGizmos()`
  （void 绘制辅助线时（））
- `void OnDestroy()`
  （void 销毁时（））
- `void OnApplicationPause(bool pauseStatus)`
  （void OnApplication暂停（bool pauseStatus））
- `void OnApplicationQuit()`
  （void 应用退出时（））
- `IDOTweenInit SetCapacity(int tweenersCapacity, int sequencesCapacity)`
  （IDOTween初始化 集合Capacity（int tweenersCapacity, int sequencesCapacity））
- `IEnumerator WaitForCompletion(Tween t)`
  （IEnumerator WaitForCompletion（Tween t））
- `IEnumerator WaitForRewind(Tween t)`
  （IEnumerator WaitForRewind（Tween t））
- `IEnumerator WaitForKill(Tween t)`
  （IEnumerator WaitFor击杀（Tween t））
- `IEnumerator WaitForElapsedLoops(Tween t, int elapsedLoops)`
  （IEnumerator WaitForElapsedLoops（Tween t, int elapsedLoops））
- `IEnumerator WaitForPosition(Tween t, float position)`
  （IEnumerator WaitForPosition（Tween t, float position））
- `IEnumerator WaitForStart(Tween t)`
  （IEnumerator WaitFor开始（Tween t））
- `void Create()`
  （void 创建（））
- `void DestroyInstance()`
  （void 销毁实例（））

---

## DOTweenExternalCommand（DOTween外部的Command）

### 方法 (3)

- `void add_SetOrientationOnPath(Action<PathOptions, Tween, Quaternion, Transform> value)`
  （void add_集合OrientationOn路径（Action<路径Options, Tween, Quaternion, Transform> value））
- `void remove_SetOrientationOnPath(Action<PathOptions, Tween, Quaternion, Transform> value)`
  （void remove_集合OrientationOn路径（Action<路径Options, Tween, Quaternion, Transform> value））
- `void Dispatch_SetOrientationOnPath(PathOptions options, Tween t, Quaternion newRot, Transform trans)`
  （void Dispatch_集合OrientationOn路径（路径Options options, Tween t, Quaternion newRot, 变换 trans））

---

## DOTweenModuleAudio（DOTween模块音频）

### 方法 (12)

- `int DOComplete(AudioMixer target, bool withCallbacks = False)`
  （int DOComplete（音频Mixer target, bool withCallbacks = False））
- `int DOKill(AudioMixer target, bool complete = False)`
  （int DO击杀（音频Mixer target, bool complete = False））
- `int DOFlip(AudioMixer target)`
  （int DOFlip（音频Mixer target））
- `int DOGoto(AudioMixer target, float to, bool andPlay = False)`
  （int DOGoto（音频Mixer target, float to, bool andPlay = False））
- `int DOPause(AudioMixer target)`
  （int DO暂停（音频Mixer target））
- `int DOPlay(AudioMixer target)`
  （int DO播放（音频Mixer target））
- `int DOPlayBackwards(AudioMixer target)`
  （int DO播放Backwards（音频Mixer target））
- `int DOPlayForward(AudioMixer target)`
  （int DO播放前进（音频Mixer target））
- `int DORestart(AudioMixer target)`
  （int DORestart（音频Mixer target））
- `int DORewind(AudioMixer target)`
  （int DORewind（音频Mixer target））
- `int DOSmoothRewind(AudioMixer target)`
  （int DOSmoothRewind（音频Mixer target））
- `int DOTogglePause(AudioMixer target)`
  （int DO开关暂停（音频Mixer target））

---

## DOTweenModulePhysics（DOTween模块物理）

### 方法 (1)

- `Sequence DOJump(Rigidbody target, Vector3 endValue, float jumpPower, int numJumps, float duration, bool snapping = False)`
  （Sequence DO跳跃（刚体 target, 三维向量 endValue, float jumpPower, int numJumps, float duration, bool snapping = False））

---

## DOTweenModulePhysics2D（DOTween模块Physics2D）

### 方法 (1)

- `Sequence DOJump(Rigidbody2D target, Vector2 endValue, float jumpPower, int numJumps, float duration, bool snapping = False)`
  （Sequence DO跳跃（Rigidbody2D target, 二维向量 endValue, float jumpPower, int numJumps, float duration, bool snapping = False））

---

## DOTweenModuleSprite（DOTween模块精灵）

### 方法 (2)

- `Sequence DOGradientColor(SpriteRenderer target, Gradient gradient, float duration)`
  （Sequence DOGradient颜色（精灵渲染器 target, Gradient gradient, float duration））
- `Tweener DOBlendableColor(SpriteRenderer target, Color endValue, float duration)`
  （Tweener DOBlendable颜色（精灵渲染器 target, 颜色 endValue, float duration））

---

## DOTweenModuleUI（DOTween模块界面）

### 方法 (11)

- `Sequence DOGradientColor(Image target, Gradient gradient, float duration)`
  （Sequence DOGradient颜色（图像 target, Gradient gradient, float duration））
- `Tweener DOPunchAnchorPos(RectTransform target, Vector2 punch, float duration, int vibrato = 10, float elasticity = 1, bool snapping = False)`
  （Tweener DOPunchAnchorPos（Rect变换 target, 二维向量 punch, float duration, int vibrato = 10, float elasticity = 1, bool snapping = False））
- `Tweener DOShakeAnchorPos(RectTransform target, float duration, float strength = 100, int vibrato = 10, float randomness = 90, bool snapping = False, bool fadeOut = True)`
  （Tweener DO震动AnchorPos（Rect变换 target, float duration, float strength = 100, int vibrato = 10, float randomness = 90, bool snapping = False, bool fadeOut = True））
- `Tweener DOShakeAnchorPos(RectTransform target, float duration, Vector2 strength, int vibrato = 10, float randomness = 90, bool snapping = False, bool fadeOut = True)`
  （Tweener DO震动AnchorPos（Rect变换 target, float duration, 二维向量 strength, int vibrato = 10, float randomness = 90, bool snapping = False, bool fadeOut = True））
- `Sequence DOJumpAnchorPos(RectTransform target, Vector2 endValue, float jumpPower, int numJumps, float duration, bool snapping = False)`
  （Sequence DO跳跃AnchorPos（Rect变换 target, 二维向量 endValue, float jumpPower, int numJumps, float duration, bool snapping = False））
- `Tweener DONormalizedPos(ScrollRect target, Vector2 endValue, float duration, bool snapping = False)`
  （Tweener DONormalizedPos（滚动Rect target, 二维向量 endValue, float duration, bool snapping = False））
- `Tweener DOHorizontalNormalizedPos(ScrollRect target, float endValue, float duration, bool snapping = False)`
  （Tweener DO水平NormalizedPos（滚动Rect target, float endValue, float duration, bool snapping = False））
- `Tweener DOVerticalNormalizedPos(ScrollRect target, float endValue, float duration, bool snapping = False)`
  （Tweener DO垂直NormalizedPos（滚动Rect target, float endValue, float duration, bool snapping = False））
- `Tweener DOBlendableColor(Graphic target, Color endValue, float duration)`
  （Tweener DOBlendable颜色（Graphic target, 颜色 endValue, float duration））
- `Tweener DOBlendableColor(Image target, Color endValue, float duration)`
  （Tweener DOBlendable颜色（图像 target, 颜色 endValue, float duration））
- `Tweener DOBlendableColor(Text target, Color endValue, float duration)`
  （Tweener DOBlendable颜色（文本 target, 颜色 endValue, float duration））

---

## DOTweenModuleUI.Utils（DOTween模块UI.Utils）

### 方法 (1)

- `Vector2 SwitchToRectTransform(RectTransform from, RectTransform to)`
  （二维向量 SwitchToRect变换（Rect变换 from, Rect变换 to））

---

## DOTweenModuleUnityVersion（DOTween模块Unity引擎Version）

### 方法 (14)

- `Sequence DOGradientColor(Material target, Gradient gradient, float duration)`
  （Sequence DOGradient颜色（材质 target, Gradient gradient, float duration））
- `Sequence DOGradientColor(Material target, Gradient gradient, string property, float duration)`
  （Sequence DOGradient颜色（材质 target, Gradient gradient, string property, float duration））
- `CustomYieldInstruction WaitForCompletion(Tween t, bool returnCustomYieldInstruction)`
  （自定义的YieldInstruction WaitForCompletion（Tween t, bool returnCustomYieldInstruction））
- `CustomYieldInstruction WaitForRewind(Tween t, bool returnCustomYieldInstruction)`
  （自定义的YieldInstruction WaitForRewind（Tween t, bool returnCustomYieldInstruction））
- `CustomYieldInstruction WaitForKill(Tween t, bool returnCustomYieldInstruction)`
  （自定义的YieldInstruction WaitFor击杀（Tween t, bool returnCustomYieldInstruction））
- `CustomYieldInstruction WaitForElapsedLoops(Tween t, int elapsedLoops, bool returnCustomYieldInstruction)`
  （自定义的YieldInstruction WaitForElapsedLoops（Tween t, int elapsedLoops, bool returnCustomYieldInstruction））
- `CustomYieldInstruction WaitForPosition(Tween t, float position, bool returnCustomYieldInstruction)`
  （自定义的YieldInstruction WaitForPosition（Tween t, float position, bool returnCustomYieldInstruction））
- `CustomYieldInstruction WaitForStart(Tween t, bool returnCustomYieldInstruction)`
  （自定义的YieldInstruction WaitFor开始（Tween t, bool returnCustomYieldInstruction））
- `Task AsyncWaitForCompletion(Tween t)`
  （Task 异步WaitForCompletion（Tween t））
- `Task AsyncWaitForRewind(Tween t)`
  （Task 异步WaitForRewind（Tween t））
- `Task AsyncWaitForKill(Tween t)`
  （Task 异步WaitFor击杀（Tween t））
- `Task AsyncWaitForElapsedLoops(Tween t, int elapsedLoops)`
  （Task 异步WaitForElapsedLoops（Tween t, int elapsedLoops））
- `Task AsyncWaitForPosition(Tween t, float position)`
  （Task 异步WaitForPosition（Tween t, float position））
- `Task AsyncWaitForStart(Tween t)`
  （Task 异步WaitFor开始（Tween t））

---

## DOTweenModuleUtils（DOTween模块Utils）

### 字段 (1)

- `bool _initialized`（bool _initialized）(偏移: 0x3BAB3B89)

### 方法 (2)

- `void Init()`
  （void 初始化（））
- `void Preserver()`
  （void Preserver（））

---

## DOTweenModuleUtils.Physics（DOTween模块Utils.物理）

### 方法 (3)

- `void SetOrientationOnPath(PathOptions options, Tween t, Quaternion newRot, Transform trans)`
  （void 集合OrientationOn路径（路径Options options, Tween t, Quaternion newRot, 变换 trans））
- `bool HasRigidbody2D(Component target)`
  （bool 是否有Rigidbody2D（组件 target））
- `bool HasRigidbody(Component target)`
  （bool 是否有刚体（组件 target））

---

## DOTweenSettings（DOTweenSettings）

**继承**: ScriptableObject（脚本对象）

### 字段 (26)

- `bool useSafeMode`（bool useSafe模式）(偏移: 0xC)
- `DOTweenSettings.SafeModeOptions safeModeOptions`（DOTweenSettings.Safe模式Options safe模式Options）(偏移: 0x10)
- `float timeScale`（float time缩放）(偏移: 0x14)
- `bool useSmoothDeltaTime`（bool useSmoothDelta时间）(偏移: 0x18)
- `float maxSmoothUnscaledTime`（float maxSmoothUnscaled时间）(偏移: 0x1C)
- `RewindCallbackMode rewindCallbackMode`（Rewind回调模式 rewind回调模式）(偏移: 0x20)
- `bool showUnityEditorReport`（bool showUnity引擎EditorReport）(偏移: 0x24)
- `LogBehaviour logBehaviour`（LogBehaviour logBehaviour）(偏移: 0x28)
- `bool drawGizmos`（bool drawGizmos）(偏移: 0x2C)
- `bool defaultRecyclable`（bool defaultRecyclable）(偏移: 0x2D)
- `AutoPlay defaultAutoPlay`（自动播放 default自动播放）(偏移: 0x30)
- `UpdateType defaultUpdateType`（更新类型 default更新类型）(偏移: 0x34)
- `bool defaultTimeScaleIndependent`（bool default时间缩放Independent）(偏移: 0x38)
- `Ease defaultEaseType`（Ease defaultEase类型）(偏移: 0x3C)
- `float defaultEaseOvershootOrAmplitude`（float defaultEaseOvershootOrAmplitude）(偏移: 0x40)
- `float defaultEasePeriod`（float defaultEasePeriod）(偏移: 0x44)
- `bool defaultAutoKill`（bool default自动击杀）(偏移: 0x48)
- `LoopType defaultLoopType`（Loop类型 defaultLoop类型）(偏移: 0x4C)
- `bool debugMode`（bool debug模式）(偏移: 0x50)
- `bool debugStoreTargetId`（bool debug商店目标Id）(偏移: 0x51)
- `bool showPreviewPanel`（bool showPreview面板）(偏移: 0x52)
- `DOTweenSettings.SettingsLocation storeSettingsLocation`（DOTweenSettings.SettingsLocation storeSettingsLocation）(偏移: 0x54)
- `DOTweenSettings.ModulesSetup modules`（DOTweenSettings.ModulesSetup modules）(偏移: 0x58)
- `bool createASMDEF`（bool createASMDEF）(偏移: 0x5C)
- `bool showPlayingTweens`（bool showPlayingTweens）(偏移: 0x5D)
- `bool showPausedTweens`（bool showPausedTweens）(偏移: 0x5E)

---

## DOTweenSettings.ModulesSetup（DOTweenSettings.ModulesSetup）

### 字段 (11)

- `bool showPanel`（bool show面板）(偏移: 0x8)
- `bool audioEnabled`（bool audio启用的）(偏移: 0x9)
- `bool physicsEnabled`（bool physics启用的）(偏移: 0xA)
- `bool physics2DEnabled`（bool physics2D启用的）(偏移: 0xB)
- `bool spriteEnabled`（bool sprite启用的）(偏移: 0xC)
- `bool uiEnabled`（bool ui启用的）(偏移: 0xD)
- `bool textMeshProEnabled`（bool text网格Pro启用的）(偏移: 0xE)
- `bool tk2DEnabled`（bool tk2D启用的）(偏移: 0xF)
- `bool deAudioEnabled`（bool de音频启用的）(偏移: 0x10)
- `bool deUnityExtendedEnabled`（bool deUnity引擎Extended启用的）(偏移: 0x11)
- `bool epoOutlineEnabled`（bool epoOutline启用的）(偏移: 0x12)

---

## DOTweenSettings.SafeModeOptions（DOTweenSettings.Safe模式Options）

### 字段 (2)

- `SafeModeLogBehaviour logBehaviour`（Safe模式LogBehaviour logBehaviour）(偏移: 0x8)
- `NestedTweenFailureBehaviour nestedTweenFailureBehaviour`（NestedTweenFailureBehaviour nestedTweenFailureBehaviour）(偏移: 0xC)

---

## DOTweenSettings.SettingsLocation（DOTweenSettings.SettingsLocation）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DOTweenUtils（DOTweenUtils）

### 字段 (2)

- `Assembly[] _loadedAssemblies`（Assembly[] _loadedAssemblies）(偏移: 0x0)
- `string[] _defAssembliesToQuery`（string[] _defAssembliesToQuery）(偏移: 0x4)

### 方法 (6)

- `Vector3 Vector3FromAngle(float degrees, float magnitude)`
  （三维向量 三维向量From角度（float degrees, float magnitude））
- `float Angle2D(Vector3 from, Vector3 to)`
  （float Angle2D（三维向量 from, 三维向量 to））
- `Vector3 RotateAroundPivot(Vector3 point, Vector3 pivot, Quaternion rotation)`
  （三维向量 RotateAroundPivot（三维向量 point, 三维向量 pivot, Quaternion rotation））
- `Vector2 GetPointOnCircle(Vector2 center, float radius, float degrees)`
  （二维向量 获取PointOnCircle（二维向量 center, float radius, float degrees））
- `bool Vector3AreApproximatelyEqual(Vector3 a, Vector3 b)`
  （bool 三维向量AreApproximatelyEqual（三维向量 a, 三维向量 b））
- `Type GetLooseScriptType(string typeName)`
  （类型 获取LooseScript类型（string typeName））

---

## DOVirtual（DO虚拟的）

### 方法 (9)

- `Tweener Float(float from, float to, float duration, TweenCallback<float> onVirtualUpdate)`
  （Tweener 浮点数（float from, float to, float duration, TweenCallback<float> onVirtualUpdate））
- `Tweener Int(int from, int to, float duration, TweenCallback<int> onVirtualUpdate)`
  （Tweener 整数（int from, int to, float duration, TweenCallback<int> onVirtualUpdate））
- `Tweener Vector3(Vector3 from, Vector3 to, float duration, TweenCallback<Vector3> onVirtualUpdate)`
  （Tweener 三维向量（三维向量 from, 三维向量 to, float duration, TweenCallback<Vector3> onVirtualUpdate））
- `Tweener Color(Color from, Color to, float duration, TweenCallback<Color> onVirtualUpdate)`
  （Tweener 颜色（颜色 from, 颜色 to, float duration, TweenCallback<Color> onVirtualUpdate））
- `float EasedValue(float from, float to, float lifetimePercentage, Ease easeType)`
  （float Eased值（float from, float to, float lifetimePercentage, Ease easeType））
- `float EasedValue(float from, float to, float lifetimePercentage, Ease easeType, float overshoot)`
  （float Eased值（float from, float to, float lifetimePercentage, Ease easeType, float overshoot））
- `float EasedValue(float from, float to, float lifetimePercentage, Ease easeType, float amplitude, float period)`
  （float Eased值（float from, float to, float lifetimePercentage, Ease easeType, float amplitude, float period））
- `float EasedValue(float from, float to, float lifetimePercentage, AnimationCurve easeCurve)`
  （float Eased值（float from, float to, float lifetimePercentage, 动画Curve easeCurve））
- `Tween DelayedCall(float delay, TweenCallback callback, bool ignoreTimeScale = True)`
  （Tween DelayedCall（float delay, Tween回调 callback, bool ignoreTimeScale = True））

---

## DSA（DSA）

**继承**: AsymmetricAlgorithm（AsymmetricAlgorithm）

### 方法 (1)

- `string ToXmlString(bool includePrivateParameters)`
  （字符串 转XML字符串（布尔值 包含私有参数））

---

## DSACryptoServiceProvider（DSACrypto服务提供者）

**继承**: DSA（DSA）

### 字段 (7)

- `KeyPairPersistence store`（键PairPersistence store）(偏移: 0x10)
- `bool persistKey`（bool persist键）(偏移: 0x14)
- `bool persisted`（bool persisted）(偏移: 0x0)
- `bool privateKeyExportable`（bool private键Exportable）(偏移: 0x0)
- `bool m_disposed`（布尔值 m_已释放）(偏移: 0x0)
- `DSAManaged dsa`（DSAManaged dsa）(偏移: 0x0)
- `bool useMachineKeyStore`（bool useMachine键商店）(偏移: 0x0)

### 方法 (6)

- `void Common(int dwKeySize, bool parameters)`
  （void Common（int dwKeySize, bool parameters））
- `void Finalize()`
  （void 终结（））
- `int get_KeySize()`
  （整数 获取_键大小（））
- `DSAParameters ExportParameters(bool includePrivateParameters)`
  （DSAParameters ExportParameters（bool includePrivateParameters））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `void OnKeyGenerated(object sender, EventArgs e)`
  （void On键Generated（object sender, 事件Args e））

---

## DSAManaged（DSAManaged）

**继承**: DSA（DSA）

### 字段 (13)

- `bool keypairGenerated`（bool keypairGenerated）(偏移: 0x10)
- `bool m_disposed`（布尔值 m_已释放）(偏移: 0x11)
- `BigInteger p`（BigInteger p）(偏移: 0x14)
- `BigInteger q`（BigInteger q）(偏移: 0x18)
- `BigInteger g`（BigInteger g）(偏移: 0x1C)
- `BigInteger x`（BigInteger x）(偏移: 0x20)
- `BigInteger y`（BigInteger y）(偏移: 0x24)
- `BigInteger j`（BigInteger j）(偏移: 0x28)
- `BigInteger seed`（BigInteger seed）(偏移: 0x2C)
- `int counter`（int counter）(偏移: 0x30)
- `bool j_missing`（bool j_missing）(偏移: 0x34)
- `RandomNumberGenerator rng`（随机NumberGenerator rng）(偏移: 0x38)
- `DSAManaged.KeyGeneratedEventHandler KeyGenerated`（DSAManaged.键Generated事件处理器 键Generated）(偏移: 0x3C)

### 方法 (13)

- `void Finalize()`
  （void 终结（））
- `void Generate()`
  （void Generate（））
- `void GenerateKeyPair()`
  （void Generate键Pair（））
- `void add(byte[] a, byte[] b, int value)`
  （void add（byte[] a, byte[] b, int value））
- `void GenerateParams(int keyLength)`
  （void GenerateParams（int keyLength））
- `RandomNumberGenerator get_Random()`
  （随机NumberGenerator get_随机（））
- `int get_KeySize()`
  （整数 获取_键大小（））
- `bool get_PublicOnly()`
  （bool get_公开的Only（））
- `byte[] NormalizeArray(byte[] array)`
  （byte[] Normalize数组（byte[] array））
- `DSAParameters ExportParameters(bool includePrivateParameters)`
  （DSAParameters ExportParameters（bool includePrivateParameters））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `void add_KeyGenerated(DSAManaged.KeyGeneratedEventHandler value)`
  （void add_键Generated（DSAManaged.键Generated事件处理器 value））
- `void remove_KeyGenerated(DSAManaged.KeyGeneratedEventHandler value)`
  （void remove_键Generated（DSAManaged.键Generated事件处理器 value））

---

## DSAManaged.KeyGeneratedEventHandler（DSAManaged.键Generated事件处理器）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(object sender, EventArgs e)`
  （void Invoke（object sender, 事件Args e））
- `IAsyncResult BeginInvoke(object sender, EventArgs e, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（object sender, 事件Args e, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## DSAParameters（DSAParameters）

### 字段 (8)

- `byte[] P`（byte[] P）(偏移: 0x0)
- `byte[] Q`（byte[] Q）(偏移: 0x4)
- `byte[] G`（byte[] G）(偏移: 0x8)
- `byte[] Y`（byte[] Y）(偏移: 0xC)
- `byte[] J`（byte[] J）(偏移: 0x10)
- `byte[] X`（byte[] X）(偏移: 0x14)
- `byte[] Seed`（byte[] Seed）(偏移: 0x18)
- `int Counter`（int Counter）(偏移: 0x1C)

---

## DSASignatureDeformatter（DSASignatureDeformatter）

**继承**: AsymmetricSignatureDeformatter（AsymmetricSignatureDeformatter）

### 字段 (1)

- `string _oid`（string _oid）(偏移: 0x8)

---

## DSASignatureFormatter（DSASignatureFormatter）

**继承**: AsymmetricSignatureFormatter（AsymmetricSignatureFormatter）

### 字段 (1)

- `string _oid`（string _oid）(偏移: 0x8)

---

## DTSubString（DT子字符串）

### 字段 (5)

- `string s`（string s）(偏移: 0x0)
- `int index`（整数 索引）(偏移: 0x4)
- `int length`（整数 长度）(偏移: 0x8)
- `DTSubStringType type`（DT子字符串类型 type）(偏移: 0xC)
- `int value`（整数 value）(偏移: 0x10)

### 方法 (1)

- `char get_Item(int relativeIndex)`
  （char get_项目（int relativeIndex））

---

## DTSubStringType（DT子字符串类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DTSweep（DTSweep）

### 方法 (32)

- `void Triangulate(DTSweepContext tcx)`
  （void Triangulate（DTSweepContext tcx））
- `void Sweep(DTSweepContext tcx)`
  （void Sweep（DTSweepContext tcx））
- `void FinalizationConvexHull(DTSweepContext tcx)`
  （void FinalizationConvexHull（DTSweepContext tcx））
- `void TurnAdvancingFrontConvex(DTSweepContext tcx, AdvancingFrontNode b, AdvancingFrontNode c)`
  （void TurnAdvancing前Convex（DTSweepContext tcx, Advancing前节点 b, Advancing前节点 c））
- `void FinalizationPolygon(DTSweepContext tcx)`
  （void FinalizationPolygon（DTSweepContext tcx））
- `AdvancingFrontNode PointEvent(DTSweepContext tcx, TriangulationPoint point)`
  （Advancing前节点 Point事件（DTSweepContext tcx, TriangulationPoint point））
- `AdvancingFrontNode NewFrontTriangle(DTSweepContext tcx, TriangulationPoint point, AdvancingFrontNode node)`
  （Advancing前节点 新的前Triangle（DTSweepContext tcx, TriangulationPoint point, Advancing前节点 node））
- `void EdgeEvent(DTSweepContext tcx, DTSweepConstraint edge, AdvancingFrontNode node)`
  （void Edge事件（DTSweepContext tcx, DTSweepConstraint edge, Advancing前节点 node））
- `void FillEdgeEvent(DTSweepContext tcx, DTSweepConstraint edge, AdvancingFrontNode node)`
  （void FillEdge事件（DTSweepContext tcx, DTSweepConstraint edge, Advancing前节点 node））
- `void FillRightConcaveEdgeEvent(DTSweepContext tcx, DTSweepConstraint edge, AdvancingFrontNode node)`
  （void Fill右ConcaveEdge事件（DTSweepContext tcx, DTSweepConstraint edge, Advancing前节点 node））
- `void FillRightConvexEdgeEvent(DTSweepContext tcx, DTSweepConstraint edge, AdvancingFrontNode node)`
  （void Fill右ConvexEdge事件（DTSweepContext tcx, DTSweepConstraint edge, Advancing前节点 node））
- `void FillRightBelowEdgeEvent(DTSweepContext tcx, DTSweepConstraint edge, AdvancingFrontNode node)`
  （void Fill右BelowEdge事件（DTSweepContext tcx, DTSweepConstraint edge, Advancing前节点 node））
- `void FillRightAboveEdgeEvent(DTSweepContext tcx, DTSweepConstraint edge, AdvancingFrontNode node)`
  （void Fill右AboveEdge事件（DTSweepContext tcx, DTSweepConstraint edge, Advancing前节点 node））
- `void FillLeftConvexEdgeEvent(DTSweepContext tcx, DTSweepConstraint edge, AdvancingFrontNode node)`
  （void Fill左ConvexEdge事件（DTSweepContext tcx, DTSweepConstraint edge, Advancing前节点 node））
- `void FillLeftConcaveEdgeEvent(DTSweepContext tcx, DTSweepConstraint edge, AdvancingFrontNode node)`
  （void Fill左ConcaveEdge事件（DTSweepContext tcx, DTSweepConstraint edge, Advancing前节点 node））
- `void FillLeftBelowEdgeEvent(DTSweepContext tcx, DTSweepConstraint edge, AdvancingFrontNode node)`
  （void Fill左BelowEdge事件（DTSweepContext tcx, DTSweepConstraint edge, Advancing前节点 node））
- `void FillLeftAboveEdgeEvent(DTSweepContext tcx, DTSweepConstraint edge, AdvancingFrontNode node)`
  （void Fill左AboveEdge事件（DTSweepContext tcx, DTSweepConstraint edge, Advancing前节点 node））
- `bool IsEdgeSideOfTriangle(DelaunayTriangle triangle, TriangulationPoint ep, TriangulationPoint eq)`
  （bool 是否Edge侧面OfTriangle（DelaunayTriangle triangle, TriangulationPoint ep, TriangulationPoint eq））
- `void EdgeEvent(DTSweepContext tcx, TriangulationPoint ep, TriangulationPoint eq, DelaunayTriangle triangle, TriangulationPoint point)`
  （void Edge事件（DTSweepContext tcx, TriangulationPoint ep, TriangulationPoint eq, DelaunayTriangle triangle, TriangulationPoint point））
- `void FlipEdgeEvent(DTSweepContext tcx, TriangulationPoint ep, TriangulationPoint eq, DelaunayTriangle t, TriangulationPoint p)`
  （void FlipEdge事件（DTSweepContext tcx, TriangulationPoint ep, TriangulationPoint eq, DelaunayTriangle t, TriangulationPoint p））
- `TriangulationPoint NextFlipPoint(TriangulationPoint ep, TriangulationPoint eq, DelaunayTriangle ot, TriangulationPoint op)`
  （TriangulationPoint 下一个FlipPoint（TriangulationPoint ep, TriangulationPoint eq, DelaunayTriangle ot, TriangulationPoint op））
- `DelaunayTriangle NextFlipTriangle(DTSweepContext tcx, Orientation o, DelaunayTriangle t, DelaunayTriangle ot, TriangulationPoint p, TriangulationPoint op)`
  （DelaunayTriangle 下一个FlipTriangle（DTSweepContext tcx, Orientation o, DelaunayTriangle t, DelaunayTriangle ot, TriangulationPoint p, TriangulationPoint op））
- `void FlipScanEdgeEvent(DTSweepContext tcx, TriangulationPoint ep, TriangulationPoint eq, DelaunayTriangle flipTriangle, DelaunayTriangle t, TriangulationPoint p)`
  （void FlipScanEdge事件（DTSweepContext tcx, TriangulationPoint ep, TriangulationPoint eq, DelaunayTriangle flipTriangle, DelaunayTriangle t, TriangulationPoint p））
- `void FillAdvancingFront(DTSweepContext tcx, AdvancingFrontNode n)`
  （void FillAdvancing前（DTSweepContext tcx, Advancing前节点 n））
- `void FillBasin(DTSweepContext tcx, AdvancingFrontNode node)`
  （void FillBasin（DTSweepContext tcx, Advancing前节点 node））
- `void FillBasinReq(DTSweepContext tcx, AdvancingFrontNode node)`
  （void FillBasinReq（DTSweepContext tcx, Advancing前节点 node））
- `bool IsShallow(DTSweepContext tcx, AdvancingFrontNode node)`
  （bool 是否Shallow（DTSweepContext tcx, Advancing前节点 node））
- `double HoleAngle(AdvancingFrontNode node)`
  （double Hole角度（Advancing前节点 node））
- `double BasinAngle(AdvancingFrontNode node)`
  （double Basin角度（Advancing前节点 node））
- `void Fill(DTSweepContext tcx, AdvancingFrontNode node)`
  （void Fill（DTSweepContext tcx, Advancing前节点 node））
- `bool Legalize(DTSweepContext tcx, DelaunayTriangle t)`
  （bool Legalize（DTSweepContext tcx, DelaunayTriangle t））
- `void RotateTrianglePair(DelaunayTriangle t, TriangulationPoint p, DelaunayTriangle ot, TriangulationPoint op)`
  （void RotateTrianglePair（DelaunayTriangle t, TriangulationPoint p, DelaunayTriangle ot, TriangulationPoint op））

---

## DTSweepBasin（DTSweepBasin）

### 字段 (5)

- `AdvancingFrontNode leftNode`（Advancing前节点 left节点）(偏移: 0x8)
- `AdvancingFrontNode bottomNode`（Advancing前节点 bottom节点）(偏移: 0xC)
- `AdvancingFrontNode rightNode`（Advancing前节点 right节点）(偏移: 0x10)
- `double width`（double width）(偏移: 0x18)
- `bool leftHighest`（bool leftHighest）(偏移: 0x20)

---

## DTSweepContext（DTSweepContext）

**继承**: TriangulationContext（TriangulationContext）

### 字段 (5)

- `float ALPHA`（float ALPHA）(偏移: 0x24)
- `AdvancingFront Front`（Advancing前 前）(偏移: 0x28)
- `DTSweepBasin Basin`（DTSweepBasin Basin）(偏移: 0x2C)
- `DTSweepEdgeEvent EdgeEvent`（DTSweepEdge事件 Edge事件）(偏移: 0x30)
- `DTSweepPointComparator _comparator`（DTSweepPointComparator _comparator）(偏移: 0x34)

### 方法 (18)

- `TriangulationPoint get_Head()`
  （TriangulationPoint get_头部（））
- `void set_Head(TriangulationPoint value)`
  （void set_头部（TriangulationPoint value））
- `TriangulationPoint get_Tail()`
  （TriangulationPoint get_Tail（））
- `void set_Tail(TriangulationPoint value)`
  （void set_Tail（TriangulationPoint value））
- `bool get_IsDebugEnabled()`
  （bool get_是否Debug启用的（））
- `void RemoveFromList(DelaunayTriangle triangle)`
  （void 移除From列表（DelaunayTriangle triangle））
- `void MeshClean(DelaunayTriangle triangle)`
  （void 网格Clean（DelaunayTriangle triangle））
- `void MeshCleanReq(DelaunayTriangle triangle)`
  （void 网格CleanReq（DelaunayTriangle triangle））
- `void Clear()`
  （void 清除（））
- `void AddNode(AdvancingFrontNode node)`
  （void 添加节点（Advancing前节点 node））
- `void RemoveNode(AdvancingFrontNode node)`
  （void 移除节点（Advancing前节点 node））
- `AdvancingFrontNode LocateNode(TriangulationPoint point)`
  （Advancing前节点 Locate节点（TriangulationPoint point））
- `void CreateAdvancingFront()`
  （void 创建Advancing前（））
- `void MapTriangleToNodes(DelaunayTriangle t)`
  （void 映射TriangleToNodes（DelaunayTriangle t））
- `void PrepareTriangulation(Triangulatable t)`
  （void PrepareTriangulation（Triangulatable t））
- `void FinalizeTriangulation()`
  （void FinalizeTriangulation（））
- `TriangulationConstraint NewConstraint(TriangulationPoint a, TriangulationPoint b)`
  （TriangulationConstraint 新的Constraint（TriangulationPoint a, TriangulationPoint b））
- `TriangulationAlgorithm get_Algorithm()`
  （TriangulationAlgorithm get_Algorithm（））

---

## DTSweepDebugContext（DTSweepDebugContext）

**继承**: TriangulationDebugContext（TriangulationDebugContext）

### 字段 (5)

- `DelaunayTriangle _primaryTriangle`（DelaunayTriangle _primaryTriangle）(偏移: 0xC)
- `DelaunayTriangle _secondaryTriangle`（DelaunayTriangle _secondaryTriangle）(偏移: 0x10)
- `TriangulationPoint _activePoint`（TriangulationPoint _activePoint）(偏移: 0x14)
- `AdvancingFrontNode _activeNode`（Advancing前节点 _active节点）(偏移: 0x18)
- `DTSweepConstraint _activeConstraint`（DTSweepConstraint _activeConstraint）(偏移: 0x1C)

### 方法 (6)

- `void set_PrimaryTriangle(DelaunayTriangle value)`
  （void set_PrimaryTriangle（DelaunayTriangle value））
- `void set_SecondaryTriangle(DelaunayTriangle value)`
  （void set_SecondaryTriangle（DelaunayTriangle value））
- `void set_ActivePoint(TriangulationPoint value)`
  （void set_激活的Point（TriangulationPoint value））
- `void set_ActiveNode(AdvancingFrontNode value)`
  （void set_激活的节点（Advancing前节点 value））
- `void set_ActiveConstraint(DTSweepConstraint value)`
  （void set_激活的Constraint（DTSweepConstraint value））
- `void Clear()`
  （void 清除（））

---

## DTSweepEdgeEvent（DTSweepEdge事件）

### 字段 (2)

- `DTSweepConstraint ConstrainedEdge`（DTSweepConstraint ConstrainedEdge）(偏移: 0x8)
- `bool Right`（bool 右）(偏移: 0xC)

---

## DTSweepPointComparator（DTSweepPointComparator）

**继承**: IComparer<TriangulationPoint>（IComparer<TriangulationPoint>）

### 方法 (1)

- `int Compare(TriangulationPoint p1, TriangulationPoint p2)`
  （int Compare（TriangulationPoint p1, TriangulationPoint p2））

---

## DamageBodyRatio（伤害身体比率）

### 字段 (9)

- `float brainRatio`（float brain比率）(偏移: 0x0)
- `float headRatio`（float head比率）(偏移: 0x4)
- `float neckRatio`（float neck比率）(偏移: 0x8)
- `float chestRatio`（float chest比率）(偏移: 0xC)
- `float abdomenRatio`（float abdomen比率）(偏移: 0x10)
- `float armRatio`（float arm比率）(偏移: 0x14)
- `float handRatio`（float hand比率）(偏移: 0x18)
- `float legRatio`（float leg比率）(偏移: 0x1C)
- `float footRatio`（float foot比率）(偏移: 0x20)

### 方法 (1)

- `float Get(string tag, float damage)`
  （float 获取（string tag, float damage））

---

## DamageEventData（伤害事件数据）

### 字段 (14)

- `Entity attacker`（实体 attacker）(偏移: 0x0)
- `Entity victim`（实体 victim）(偏移: 0x4)
- `float damage`（float damage）(偏移: 0x8)
- `Vector3 origin`（三维向量 origin）(偏移: 0xC)
- `Vector3 hitPos`（三维向量 hitPos）(偏移: 0x18)
- `string hitTag`（string hit标签）(偏移: 0x24)
- `string hitSndName`（string hitSnd名称）(偏移: 0x28)
- `string hitEffect`（string hit特效）(偏移: 0x2C)
- `bool wallThrough`（bool wallThrough）(偏移: 0x30)
- `DamageType type`（伤害类型 type）(偏移: 0x34)
- `DamageTag damageTag`（伤害标签 damage标签）(偏移: 0x38)
- `int wpnIndex`（int 武器索引）(偏移: 0x3C)
- `int wpnSprIndex`（int 武器Spr索引）(偏移: 0x40)
- `bool ignoreDmgRate`（bool ignoreDmgRate）(偏移: 0x44)

### 方法 (3)

- `Sprite get_killMsgIcon()`
  （精灵 get_killMsg图标（））
- `void TakePlace()`
  （void TakePlace（））
- `void Print()`
  （void Print（））

---

## DamageRateBuff（伤害Rate增益）

**继承**: Buff（增益）

### 字段 (1)

- `float damageRate`（float damageRate）(偏移: 0x24)

### 方法 (2)

- `void DamageRateBuffUpdate(ref float damageUp, ref float damageDown)`
  （void 伤害Rate增益更新（ref float damageUp, ref float damageDown））
- `void OnLifeEnd()`
  （void 生命结束时（））

---

## DamageTag（伤害标签）

### 方法 (16)

- `int get_tag()`
  （int get_tag（））
- `void set_tag(int value)`
  （void set_tag（int value））
- `bool get_isHitLower()`
  （bool get_is命中下半身（））
- `void set_isHitLower(bool value)`
  （void set_is命中下半身（bool value））
- `bool get_isBigshot()`
  （bool get_is爆头（））
- `void set_isBigshot(bool value)`
  （void set_is爆头（bool value））
- `bool get_isGhostBladeSecKill()`
  （bool get_is幽灵刀锋Sec击杀（））
- `void set_isGhostBladeSecKill(bool value)`
  （void set_is幽灵刀锋Sec击杀（bool value））
- `bool get_isMasterHeroSlash()`
  （bool get_isMaster英雄Slash（））
- `void set_isMasterHeroSlash(bool value)`
  （void set_isMaster英雄Slash（bool value））
- `bool get_isArcane()`
  （bool get_isArcane（））
- `void set_isArcane(bool value)`
  （void set_isArcane（bool value））
- `bool get_isCritical()`
  （bool get_isCritical（））
- `void set_isCritical(bool value)`
  （void set_isCritical（bool value））
- `void SetState(int bit, bool enable)`
  （void 集合状态（int bit, bool enable））
- `bool GetState(int bit)`
  （bool 获取状态（int bit））

---

## DamageType（伤害类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DamageTypeExpand（伤害类型扩展）

### 方法 (1)

- `bool IsGunOrKnife(DamageType type)`
  （bool 是否枪械Or近战武器（伤害类型 type））

---

## Damper（Damper）

### 方法 (5)

- `float DecayConstant(float time, float residual)`
  （float 衰减Constant（float time, float residual））
- `float DecayedRemainder(float initial, float decayConstant, float deltaTime)`
  （float DecayedRemainder（float initial, float decayConstant, float deltaTime））
- `float Damp(float initial, float dampTime, float deltaTime)`
  （float Damp（float initial, float dampTime, float deltaTime））
- `Vector3 Damp(Vector3 initial, Vector3 dampTime, float deltaTime)`
  （三维向量 Damp（三维向量 initial, 三维向量 dampTime, float deltaTime））
- `Vector3 Damp(Vector3 initial, float dampTime, float deltaTime)`
  （三维向量 Damp（三维向量 initial, float dampTime, float deltaTime））

---

## DataBaseExample（数据基础Example）

**继承**: ScriptableObject（脚本对象）

### 字段 (19)

- `DataBaseExample.Generic_String _genericString`（数据基础Example.Generic_字符串 _generic字符串）(偏移: 0xC)
- `DataBaseExample.Generic_Generic _genericGeneric`（数据基础Example.Generic_Generic _genericGeneric）(偏移: 0x10)
- `DataBaseExample.S_GenericDictionary _stringGeneric`（数据基础Example.S_Generic字典 _stringGeneric）(偏移: 0x14)
- `DataBaseExample.I_GenericDictionary _intGeneric`（数据基础Example.I_Generic字典 _intGeneric）(偏移: 0x18)
- `DataBaseExample.I_GO _intGameobject`（数据基础Example.I_GO _intGameobject）(偏移: 0x1C)
- `DataBaseExample.GO_I _gameobjectInt`（数据基础Example.GO_I _gameobject整数）(偏移: 0x20)
- `DataBaseExample.S_GO _stringGameobject`（数据基础Example.S_GO _stringGameobject）(偏移: 0x24)
- `DataBaseExample.GO_S _gameobjectString`（数据基础Example.GO_S _gameobject字符串）(偏移: 0x28)
- `DataBaseExample.S_Mat _stringMaterial`（数据基础Example.S_材质 _string材质）(偏移: 0x2C)
- `DataBaseExample.Mat_S _materialString`（数据基础Example.Mat_S _material字符串）(偏移: 0x30)
- `DataBaseExample.V3_Q _vector3Quaternion`（数据基础Example.V3_Q _vector3Quaternion）(偏移: 0x34)
- `DataBaseExample.Q_V3 _quaternionVector3`（数据基础Example.Q_V3 _quaternion三维向量）(偏移: 0x38)
- `DataBaseExample.S_AC _stringAudioClip`（数据基础Example.S_AC _string音频弹匣）(偏移: 0x3C)
- `DataBaseExample.AC_S _audioClipString`（数据基础Example.AC_S _audio弹匣字符串）(偏移: 0x40)
- `DataBaseExample.C_Int _charInt`（数据基础Example.C_整数 _char整数）(偏移: 0x44)
- `DataBaseExample.G_Int _gradientInt`（数据基础Example.G_整数 _gradient整数）(偏移: 0x48)
- `DataBaseExample.Int_IntArray _intArray`（数据基础Example.Int_整数数组 _int数组）(偏移: 0x4C)
- `DataBaseExample.Enum_String _enumString`（数据基础Example.Enum_字符串 _enum字符串）(偏移: 0x50)
- `DataBaseExample.AdvanGeneric_String _advancedGenericKey`（数据基础Example.AdvanGeneric_字符串 _advancedGeneric键）(偏移: 0x54)

---

## DataBaseExample.AdvancedGenericClass（数据基础Example.AdvancedGeneric类）

### 字段 (1)

- `float value`（float value）(偏移: 0x8)

### 方法 (3)

- `bool Equals(DataBaseExample.AdvancedGenericClass other)`
  （bool Equals（数据基础Example.AdvancedGeneric类 other））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## DataBaseExample.ArrayTest（数据基础Example.数组Test）

### 字段 (1)

- `int[] myArray`（int[] my数组）(偏移: 0x8)

---

## DataBaseExample.ChildTest（数据基础Example.子级Test）

### 字段 (3)

- `Color myChildColor`（颜色 my子级颜色）(偏移: 0x8)
- `bool myChildBool`（bool my子级布尔值）(偏移: 0x18)
- `Gradient test`（Gradient test）(偏移: 0x1C)

---

## DataBaseExample.ClassTest（数据基础Example.类Test）

### 字段 (5)

- `string id`（string id）(偏移: 0x8)
- `float test`（float test）(偏移: 0xC)
- `string test2`（string test2）(偏移: 0x10)
- `Quaternion quat`（Quaternion quat）(偏移: 0x14)
- `DataBaseExample.ChildTest[] childTest`（数据基础Example.子级Test[] childTest）(偏移: 0x24)

---

## DataBaseExample.EnumExample（数据基础Example.EnumExample）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DataCollector（数据Collector）

### 字段 (12)

- `DataCollector ThreadInstance`（数据Collector Thread实例）(偏移: 0x80000000)
- `byte* scratchEnd`（byte* scratch结束）(偏移: 0x0)
- `EventSource.EventData* datasEnd`（事件Source.事件Data* datas结束）(偏移: 0x4)
- `GCHandle* pinsEnd`（GCHandle* pins结束）(偏移: 0x8)
- `EventSource.EventData* datasStart`（事件Source.事件Data* datas开始）(偏移: 0xC)
- `byte* scratch`（byte* scratch）(偏移: 0x10)
- `EventSource.EventData* datas`（事件Source.事件Data* datas）(偏移: 0x14)
- `GCHandle* pins`（GCHandle* pins）(偏移: 0x18)
- `byte[] buffer`（byte[] buffer）(偏移: 0x1C)
- `int bufferPos`（int bufferPos）(偏移: 0x20)
- `int bufferNesting`（int bufferNesting）(偏移: 0x24)
- `bool writingScalars`（bool writingScalars）(偏移: 0x28)

### 方法 (17)

- `void Enable(byte* scratch, int scratchSize, EventSource.EventData* datas, int dataCount, GCHandle* pins, int pinCount)`
  （void 启用（byte* scratch, int scratchSize, 事件Source.事件Data* datas, int dataCount, GCHandle* pins, int pinCount））
- `void Disable()`
  （void 禁用（））
- `EventSource.EventData* Finish()`
  （事件Source.事件Data* Finish（））
- `void AddScalar(void* value, int size)`
  （void 添加Scalar（void* value, int size））
- `void AddBinary(string value, int size)`
  （void 添加Binary（string value, int size））
- `void AddBinary(Array value, int size)`
  （void 添加Binary（数组 value, int size））
- `void AddArray(Array value, int length, int itemSize)`
  （void 添加数组（数组 value, int length, int itemSize））
- `int BeginBufferedArray()`
  （int BeginBuffered数组（））
- `void EndBufferedArray(int bookmark, int count)`
  （void 结束Buffered数组（int bookmark, int count））
- `void BeginBuffered()`
  （void BeginBuffered（））
- `void EndBuffered()`
  （void 结束Buffered（））
- `void EnsureBuffer()`
  （void Ensure缓冲区（））
- `void EnsureBuffer(int additionalSize)`
  （void Ensure缓冲区（int additionalSize））
- `void GrowBuffer(int required)`
  （void Grow缓冲区（int required））
- `void PinArray(object value, int size)`
  （void Pin数组（object value, int size））
- `void ScalarsBegin()`
  （void ScalarsBegin（））
- `void ScalarsEnd()`
  （void Scalars结束（））

---

## DataUtility（数据工具）

### 方法 (4)

- `Vector4 GetInnerUV(Sprite sprite)`
  （Vector4 获取InnerUV（精灵 sprite））
- `Vector4 GetOuterUV(Sprite sprite)`
  （Vector4 获取OuterUV（精灵 sprite））
- `Vector4 GetPadding(Sprite sprite)`
  （Vector4 获取Padding（精灵 sprite））
- `Vector2 GetMinSize(Sprite sprite)`
  （二维向量 获取最小大小（精灵 sprite））

---

## DateTime（Date时间）

**继承**: IComparable, IFormattable, IConvertible, ISerializable, IComparable<DateTime>, IEquatable<DateTime>（IComparable, IFormattable, IConvertible, ISerializable, IComparable<DateTime>, IEquatable<DateTime>）

### 字段 (5)

- `int[] DaysToMonth365`（int[] DaysToMonth365）(偏移: 0x0)
- `int[] DaysToMonth366`（int[] DaysToMonth366）(偏移: 0x4)
- `DateTime MinValue`（Date时间 最小值）(偏移: 0x8)
- `DateTime MaxValue`（Date时间 最大值）(偏移: 0x10)
- `ulong dateData`（ulong date数据）(偏移: 0x0)

### 方法 (63)

- `long get_InternalTicks()`
  （long get_内部的Ticks（））
- `ulong get_InternalKind()`
  （ulong get_内部的Kind（））
- `DateTime Add(TimeSpan value)`
  （Date时间 添加（时间Span value））
- `DateTime Add(double value, int scale)`
  （Date时间 添加（double value, int scale））
- `DateTime AddDays(double value)`
  （Date时间 添加Days（double value））
- `DateTime AddMilliseconds(double value)`
  （Date时间 添加Milliseconds（double value））
- `DateTime AddMonths(int months)`
  （Date时间 添加Months（int months））
- `DateTime AddSeconds(double value)`
  （Date时间 添加Seconds（double value））
- `DateTime AddTicks(long value)`
  （Date时间 添加Ticks（long value））
- `DateTime AddYears(int value)`
  （Date时间 添加Years（int value））
- `int CompareTo(object value)`
  （整数 比较到（对象 value））
- `int CompareTo(DateTime value)`
  （int CompareTo（Date时间 value））
- `long DateToTicks(int year, int month, int day)`
  （long DateToTicks（int year, int month, int day））
- `long TimeToTicks(int hour, int minute, int second)`
  （long 时间ToTicks（int hour, int minute, int second））
- `int DaysInMonth(int year, int month)`
  （int DaysInMonth（int year, int month））
- `bool Equals(object value)`
  （布尔值 等于（对象 value））
- `bool Equals(DateTime value)`
  （bool Equals（Date时间 value））
- `DateTime FromBinary(long dateData)`
  （Date时间 FromBinary（long dateData））
- `DateTime FromBinaryRaw(long dateData)`
  （Date时间 FromBinaryRaw（long dateData））
- `DateTime FromFileTime(long fileTime)`
  （Date时间 From文件时间（long fileTime））
- `DateTime FromFileTimeUtc(long fileTime)`
  （Date时间 From文件时间Utc（long fileTime））
- `bool IsDaylightSavingTime()`
  （bool 是否DaylightSaving时间（））
- `DateTime SpecifyKind(DateTime value, DateTimeKind kind)`
  （Date时间 SpecifyKind（Date时间 value, Date时间Kind kind））
- `long ToBinaryRaw()`
  （long ToBinaryRaw（））
- `DateTime get_Date()`
  （Date时间 get_Date（））
- `int GetDatePart(int part)`
  （int 获取DatePart（int part））
- `int get_Day()`
  （int get_Day（））
- `DayOfWeek get_DayOfWeek()`
  （DayOfWeek get_DayOfWeek（））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `int get_Hour()`
  （int get_Hour（））
- `bool IsAmbiguousDaylightSavingTime()`
  （bool 是否AmbiguousDaylightSaving时间（））
- `DateTimeKind get_Kind()`
  （Date时间Kind get_Kind（））
- `int get_Minute()`
  （int get_Minute（））
- `int get_Month()`
  （int get_Month（））
- `DateTime get_Now()`
  （Date时间 get_Now（））
- `DateTime get_UtcNow()`
  （Date时间 get_UtcNow（））
- `long GetSystemTimeAsFileTime()`
  （long 获取系统时间As文件时间（））
- `int get_Second()`
  （int get_Second（））
- `long get_Ticks()`
  （long get_Ticks（））
- `TimeSpan get_TimeOfDay()`
  （时间Span get_时间OfDay（））
- `int get_Year()`
  （int get_Year（））
- `bool IsLeapYear(int year)`
  （bool 是否LeapYear（int year））
- `DateTime Parse(string s, IFormatProvider provider)`
  （Date时间 解析（string s, I格式化提供者 provider））
- `TimeSpan Subtract(DateTime value)`
  （时间Span Subtract（Date时间 value））
- `long ToFileTime()`
  （long To文件时间（））
- `long ToFileTimeUtc()`
  （long To文件时间Utc（））
- `DateTime ToLocalTime()`
  （Date时间 To本地的时间（））
- `DateTime ToLocalTime(bool throwOnOverflow)`
  （Date时间 To本地的时间（bool throwOnOverflow））
- `string ToString()`
  （字符串 转字符串（））
- `string ToString(IFormatProvider provider)`
  （字符串 转字符串（I格式化提供者 provider））
- `string ToString(string format, IFormatProvider provider)`
  （字符串 转字符串（字符串 格式, I格式化提供者 provider））
- `DateTime ToUniversalTime()`
  （Date时间 ToUniversal时间（））
- `bool TryParse(string s, IFormatProvider provider, DateTimeStyles styles, out DateTime result)`
  （bool Try解析（string s, I格式化提供者 provider, Date时间Styles styles, out DateTime result））
- `DateTime op_Addition(DateTime d, TimeSpan t)`
  （Date时间 op_Addition（Date时间 d, 时间Span t））
- `DateTime op_Subtraction(DateTime d, TimeSpan t)`
  （Date时间 op_Subtraction（Date时间 d, 时间Span t））
- `TimeSpan op_Subtraction(DateTime d1, DateTime d2)`
  （时间Span op_Subtraction（Date时间 d1, Date时间 d2））
- `bool op_Equality(DateTime d1, DateTime d2)`
  （bool op_Equality（Date时间 d1, Date时间 d2））
- `bool op_LessThan(DateTime t1, DateTime t2)`
  （bool op_LessThan（Date时间 t1, Date时间 t2））
- `bool op_LessThanOrEqual(DateTime t1, DateTime t2)`
  （bool op_LessThanOrEqual（Date时间 t1, Date时间 t2））
- `bool op_GreaterThan(DateTime t1, DateTime t2)`
  （bool op_GreaterThan（Date时间 t1, Date时间 t2））
- `bool op_GreaterThanOrEqual(DateTime t1, DateTime t2)`
  （bool op_GreaterThanOrEqual（Date时间 t1, Date时间 t2））
- `TypeCode GetTypeCode()`
  （类型代码 获取类型代码（））
- `bool TryCreate(int year, int month, int day, int hour, int minute, int second, int millisecond, out DateTime result)`
  （bool Try创建（int year, int month, int day, int hour, int minute, int second, int millisecond, out DateTime result））

---

## DateTimeConstantAttribute（Date时间ConstantAttribute）

**继承**: CustomConstantAttribute（自定义的ConstantAttribute）

### 字段 (1)

- `DateTime date`（Date时间 date）(偏移: 0x8)

### 方法 (1)

- `object get_Value()`
  （对象 获取_值（））

---

## DateTimeFormat（Date时间格式化）

### 字段 (3)

- `TimeSpan NullOffset`（时间Span NullOffset）(偏移: 0x0)
- `char[] allStandardFormats`（char[] allStandardFormats）(偏移: 0x8)
- `string[] fixedNumberFormats`（string[] fixedNumberFormats）(偏移: 0xC)

### 方法 (19)

- `void FormatDigits(StringBuilder outputBuffer, int value, int len)`
  （void 格式化Digits（字符串构建器 outputBuffer, int value, int len））
- `void FormatDigits(StringBuilder outputBuffer, int value, int len, bool overrideLengthLimit)`
  （void 格式化Digits（字符串构建器 outputBuffer, int value, int len, bool overrideLengthLimit））
- `void HebrewFormatDigits(StringBuilder outputBuffer, int digits)`
  （void Hebrew格式化Digits（字符串构建器 outputBuffer, int digits））
- `int ParseRepeatPattern(string format, int pos, char patternChar)`
  （int 解析RepeatPattern（string format, int pos, char patternChar））
- `string FormatDayOfWeek(int dayOfWeek, int repeat, DateTimeFormatInfo dtfi)`
  （string 格式化DayOfWeek（int dayOfWeek, int repeat, Date时间格式化信息 dtfi））
- `string FormatMonth(int month, int repeatCount, DateTimeFormatInfo dtfi)`
  （string 格式化Month（int month, int repeatCount, Date时间格式化信息 dtfi））
- `string FormatHebrewMonthName(DateTime time, int month, int repeatCount, DateTimeFormatInfo dtfi)`
  （string 格式化HebrewMonth名称（Date时间 time, int month, int repeatCount, Date时间格式化信息 dtfi））
- `int ParseQuoteString(string format, int pos, StringBuilder result)`
  （int 解析Quote字符串（string format, int pos, 字符串构建器 result））
- `int ParseNextChar(string format, int pos)`
  （int 解析下一个Char（string format, int pos））
- `bool IsUseGenitiveForm(string format, int index, int tokenLen, char patternToMatch)`
  （bool 是否UseGenitiveForm（string format, int index, int tokenLen, char patternToMatch））
- `string FormatCustomized(DateTime dateTime, string format, DateTimeFormatInfo dtfi, TimeSpan offset)`
  （string 格式化Customized（Date时间 dateTime, string format, Date时间格式化信息 dtfi, 时间Span offset））
- `void FormatCustomizedTimeZone(DateTime dateTime, TimeSpan offset, string format, int tokenLen, bool timeOnly, StringBuilder result)`
  （void 格式化Customized时间Zone（Date时间 dateTime, 时间Span offset, string format, int tokenLen, bool timeOnly, 字符串构建器 result））
- `void FormatCustomizedRoundripTimeZone(DateTime dateTime, TimeSpan offset, StringBuilder result)`
  （void 格式化CustomizedRoundrip时间Zone（Date时间 dateTime, 时间Span offset, 字符串构建器 result））
- `string GetRealFormat(string format, DateTimeFormatInfo dtfi)`
  （string 获取Real格式化（string format, Date时间格式化信息 dtfi））
- `string ExpandPredefinedFormat(string format, ref DateTime dateTime, ref DateTimeFormatInfo dtfi, ref TimeSpan offset)`
  （string ExpandPredefined格式化（string format, ref DateTime dateTime, ref DateTimeFormatInfo dtfi, ref TimeSpan offset））
- `string Format(DateTime dateTime, string format, DateTimeFormatInfo dtfi)`
  （string 格式化（Date时间 dateTime, string format, Date时间格式化信息 dtfi））
- `string Format(DateTime dateTime, string format, DateTimeFormatInfo dtfi, TimeSpan offset)`
  （string 格式化（Date时间 dateTime, string format, Date时间格式化信息 dtfi, 时间Span offset））
- `void InvalidFormatForLocal(string format, DateTime dateTime)`
  （void Invalid格式化For本地的（string format, Date时间 dateTime））
- `void InvalidFormatForUtc(string format, DateTime dateTime)`
  （void Invalid格式化ForUtc（string format, Date时间 dateTime））

---

## DateTimeFormatFlags（Date时间格式化Flags）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DateTimeFormatInfo（Date时间格式化信息）

**继承**: ICloneable, IFormatProvider（ICloneable, I格式化提供者）

### 字段 (55)

- `DateTimeFormatInfo invariantInfo`（Date时间格式化信息 invariant信息）(偏移: 0x0)
- `CultureData m_cultureData`（Culture数据 m_culture数据）(偏移: 0x8)
- `string m_name`（字符串 m_名称）(偏移: 0xC)
- `string m_langName`（string m_lang名称）(偏移: 0x10)
- `CompareInfo m_compareInfo`（比较信息 m_compare信息）(偏移: 0x14)
- `CultureInfo m_cultureInfo`（Culture信息 m_culture信息）(偏移: 0x18)
- `string amDesignator`（string amDesignator）(偏移: 0x1C)
- `string pmDesignator`（string pmDesignator）(偏移: 0x20)
- `string dateSeparator`（string dateSeparator）(偏移: 0x24)
- `string generalShortTimePattern`（string generalShort时间Pattern）(偏移: 0x28)
- `string generalLongTimePattern`（string generalLong时间Pattern）(偏移: 0x2C)
- `string timeSeparator`（string timeSeparator）(偏移: 0x30)
- `string monthDayPattern`（string monthDayPattern）(偏移: 0x34)
- `string dateTimeOffsetPattern`（string date时间OffsetPattern）(偏移: 0x38)
- `Calendar calendar`（Calendar calendar）(偏移: 0x3C)
- `int firstDayOfWeek`（int firstDayOfWeek）(偏移: 0x40)
- `int calendarWeekRule`（int calendarWeekRule）(偏移: 0x44)
- `string fullDateTimePattern`（string fullDate时间Pattern）(偏移: 0x48)
- `string[] abbreviatedDayNames`（string[] abbreviatedDayNames）(偏移: 0x4C)
- `string[] m_superShortDayNames`（string[] m_superShortDayNames）(偏移: 0x50)
- `string[] dayNames`（string[] dayNames）(偏移: 0x54)
- `string[] abbreviatedMonthNames`（string[] abbreviatedMonthNames）(偏移: 0x58)
- `string[] monthNames`（string[] monthNames）(偏移: 0x5C)
- `string[] genitiveMonthNames`（string[] genitiveMonthNames）(偏移: 0x60)
- `string[] m_genitiveAbbreviatedMonthNames`（string[] m_genitiveAbbreviatedMonthNames）(偏移: 0x64)
- `string[] leapYearMonthNames`（string[] leapYearMonthNames）(偏移: 0x68)
- `string longDatePattern`（string longDatePattern）(偏移: 0x6C)
- `string shortDatePattern`（string shortDatePattern）(偏移: 0x70)
- `string yearMonthPattern`（string yearMonthPattern）(偏移: 0x74)
- `string longTimePattern`（string long时间Pattern）(偏移: 0x78)
- `string shortTimePattern`（string short时间Pattern）(偏移: 0x7C)
- `string[] allYearMonthPatterns`（string[] allYearMonthPatterns）(偏移: 0x80)
- `string[] allShortDatePatterns`（string[] allShortDatePatterns）(偏移: 0x84)
- `string[] allLongDatePatterns`（string[] allLongDatePatterns）(偏移: 0x88)
- `string[] allShortTimePatterns`（string[] allShort时间Patterns）(偏移: 0x8C)
- `string[] allLongTimePatterns`（string[] allLong时间Patterns）(偏移: 0x90)
- `string[] m_eraNames`（string[] m_eraNames）(偏移: 0x94)
- `string[] m_abbrevEraNames`（string[] m_abbrevEraNames）(偏移: 0x98)
- `string[] m_abbrevEnglishEraNames`（string[] m_abbrevEnglishEraNames）(偏移: 0x9C)
- `int[] optionalCalendars`（int[] optionalCalendars）(偏移: 0xA0)
- `bool m_isReadOnly`（布尔值 m_是否只读）(偏移: 0xA4)
- `DateTimeFormatFlags formatFlags`（Date时间格式化Flags formatFlags）(偏移: 0xA8)
- `bool preferExistingTokens`（bool preferExistingTokens）(偏移: 0x4)
- `int CultureID`（int CultureID）(偏移: 0xAC)
- `bool m_useUserOverride`（bool m_useUser重写）(偏移: 0xB0)
- `bool bUseCalendarInfo`（bool bUseCalendar信息）(偏移: 0xB1)
- `int nDataItem`（int n数据项目）(偏移: 0xB4)
- `bool m_isDefaultCalendar`（bool m_is默认的Calendar）(偏移: 0xB8)
- `Hashtable s_calendarNativeNames`（Hashtable s_calendarNativeNames）(偏移: 0x8)
- `string[] m_dateWords`（string[] m_dateWords）(偏移: 0xBC)
- `string m_fullTimeSpanPositivePattern`（string m_full时间SpanPositivePattern）(偏移: 0xC0)
- `string m_fullTimeSpanNegativePattern`（string m_full时间SpanNegativePattern）(偏移: 0xC4)
- `TokenHashValue[] m_dtfiTokenHash`（令牌HashValue[] m_dtfi令牌Hash）(偏移: 0xC8)
- `DateTimeFormatInfo s_jajpDTFI`（Date时间格式化信息 s_jajpDTFI）(偏移: 0xC)
- `DateTimeFormatInfo s_zhtwDTFI`（Date时间格式化信息 s_zhtwDTFI）(偏移: 0x10)

### 方法 (90)

- `bool InitPreferExistingTokens()`
  （bool 初始化PreferExistingTokens（））
- `string get_CultureName()`
  （string get_Culture名称（））
- `CultureInfo get_Culture()`
  （Culture信息 get_Culture（））
- `string get_LanguageName()`
  （string get_Language名称（））
- `string[] internalGetAbbreviatedDayOfWeekNames()`
  （string[] internal获取AbbreviatedDayOfWeekNames（））
- `string[] internalGetDayOfWeekNames()`
  （string[] internal获取DayOfWeekNames（））
- `string[] internalGetAbbreviatedMonthNames()`
  （string[] internal获取AbbreviatedMonthNames（））
- `string[] internalGetMonthNames()`
  （string[] internal获取MonthNames（））
- `void InitializeOverridableProperties(CultureData cultureData, int calendarID)`
  （void 初始化OverridableProperties（Culture数据 cultureData, int calendarID））
- `void OnDeserialized(StreamingContext ctx)`
  （void 反序列化后（流上下文 ctx））
- `void OnSerializing(StreamingContext ctx)`
  （void 序列化中（流上下文 ctx））
- `DateTimeFormatInfo get_InvariantInfo()`
  （Date时间格式化信息 get_Invariant信息（））
- `DateTimeFormatInfo get_CurrentInfo()`
  （Date时间格式化信息 get_当前信息（））
- `DateTimeFormatInfo GetInstance(IFormatProvider provider)`
  （Date时间格式化信息 获取实例（I格式化提供者 provider））
- `object GetFormat(Type formatType)`
  （object 获取格式化（类型 formatType））
- `object Clone()`
  （对象 克隆（））
- `string get_AMDesignator()`
  （string get_AMDesignator（））
- `Calendar get_Calendar()`
  （Calendar get_Calendar（））
- `void set_Calendar(Calendar value)`
  （void set_Calendar（Calendar value））
- `int[] get_OptionalCalendars()`
  （int[] get_OptionalCalendars（））
- `string[] get_EraNames()`
  （string[] get_EraNames（））
- `string GetEraName(int era)`
  （string 获取Era名称（int era））
- `string[] get_AbbreviatedEraNames()`
  （string[] get_AbbreviatedEraNames（））
- `string GetAbbreviatedEraName(int era)`
  （string 获取AbbreviatedEra名称（int era））
- `string[] get_AbbreviatedEnglishEraNames()`
  （string[] get_AbbreviatedEnglishEraNames（））
- `string get_DateSeparator()`
  （string get_DateSeparator（））
- `string get_FullDateTimePattern()`
  （string get_满Date时间Pattern（））
- `string get_LongDatePattern()`
  （string get_LongDatePattern（））
- `void set_LongDatePattern(string value)`
  （void set_LongDatePattern（string value））
- `string get_LongTimePattern()`
  （string get_Long时间Pattern（））
- `void set_LongTimePattern(string value)`
  （void set_Long时间Pattern（string value））
- `string get_MonthDayPattern()`
  （string get_MonthDayPattern（））
- `string get_PMDesignator()`
  （string get_PMDesignator（））
- `string get_RFC1123Pattern()`
  （string get_RFC1123Pattern（））
- `string get_ShortDatePattern()`
  （string get_ShortDatePattern（））
- `void set_ShortDatePattern(string value)`
  （void set_ShortDatePattern（string value））
- `string get_ShortTimePattern()`
  （string get_Short时间Pattern（））
- `void set_ShortTimePattern(string value)`
  （void set_Short时间Pattern（string value））
- `string get_SortableDateTimePattern()`
  （string get_SortableDate时间Pattern（））
- `string get_GeneralShortTimePattern()`
  （string get_GeneralShort时间Pattern（））
- `string get_GeneralLongTimePattern()`
  （string get_GeneralLong时间Pattern（））
- `string get_DateTimeOffsetPattern()`
  （string get_Date时间OffsetPattern（））
- `string get_TimeSeparator()`
  （string get_时间Separator（））
- `string get_UniversalSortableDateTimePattern()`
  （string get_UniversalSortableDate时间Pattern（））
- `string get_YearMonthPattern()`
  （string get_YearMonthPattern（））
- `void set_YearMonthPattern(string value)`
  （void set_YearMonthPattern（string value））
- `string[] get_AbbreviatedDayNames()`
  （string[] get_AbbreviatedDayNames（））
- `string[] get_DayNames()`
  （string[] get_DayNames（））
- `string[] get_AbbreviatedMonthNames()`
  （string[] get_AbbreviatedMonthNames（））
- `string[] get_MonthNames()`
  （string[] get_MonthNames（））
- `bool get_HasSpacesInMonthNames()`
  （bool get_是否有SpacesInMonthNames（））
- `bool get_HasSpacesInDayNames()`
  （bool get_是否有SpacesInDayNames（））
- `string internalGetMonthName(int month, MonthNameStyles style, bool abbreviated)`
  （string internal获取Month名称（int month, Month名称Styles style, bool abbreviated））
- `string[] internalGetGenitiveMonthNames(bool abbreviated)`
  （string[] internal获取GenitiveMonthNames（bool abbreviated））
- `string[] internalGetLeapYearMonthNames()`
  （string[] internal获取LeapYearMonthNames（））
- `string GetAbbreviatedDayName(DayOfWeek dayofweek)`
  （string 获取AbbreviatedDay名称（DayOfWeek dayofweek））
- `string[] GetCombinedPatterns(string[] patterns1, string[] patterns2, string connectString)`
  （string[] 获取CombinedPatterns（string[] patterns1, string[] patterns2, string connectString））
- `string[] GetAllDateTimePatterns(char format)`
  （string[] 获取所有Date时间Patterns（char format））
- `string GetDayName(DayOfWeek dayofweek)`
  （string 获取Day名称（DayOfWeek dayofweek））
- `string GetAbbreviatedMonthName(int month)`
  （string 获取AbbreviatedMonth名称（int month））
- `string GetMonthName(int month)`
  （string 获取Month名称（int month））
- `string[] GetMergedPatterns(string[] patterns, string defaultPattern)`
  （string[] 获取MergedPatterns（string[] patterns, string defaultPattern））
- `string[] get_AllYearMonthPatterns()`
  （string[] get_所有YearMonthPatterns（））
- `string[] get_AllShortDatePatterns()`
  （string[] get_所有ShortDatePatterns（））
- `string[] get_AllShortTimePatterns()`
  （string[] get_所有Short时间Patterns（））
- `string[] get_AllLongDatePatterns()`
  （string[] get_所有LongDatePatterns（））
- `string[] get_AllLongTimePatterns()`
  （string[] get_所有Long时间Patterns（））
- `string[] get_UnclonedYearMonthPatterns()`
  （string[] get_UnclonedYearMonthPatterns（））
- `string[] get_UnclonedShortDatePatterns()`
  （string[] get_UnclonedShortDatePatterns（））
- `string[] get_UnclonedLongDatePatterns()`
  （string[] get_UnclonedLongDatePatterns（））
- `string[] get_UnclonedShortTimePatterns()`
  （string[] get_UnclonedShort时间Patterns（））
- `string[] get_UnclonedLongTimePatterns()`
  （string[] get_UnclonedLong时间Patterns（））
- `bool get_IsReadOnly()`
  （布尔值 获取_是否只读（））
- `string get_FullTimeSpanPositivePattern()`
  （string get_满时间SpanPositivePattern（））
- `string get_FullTimeSpanNegativePattern()`
  （string get_满时间SpanNegativePattern（））
- `CompareInfo get_CompareInfo()`
  （Compare信息 get_Compare信息（））
- `void ValidateStyles(DateTimeStyles style, string parameterName)`
  （void 验证Styles（Date时间Styles style, string parameterName））
- `DateTimeFormatFlags get_FormatFlags()`
  （Date时间格式化Flags get_格式化Flags（））
- `bool get_HasForceTwoDigitYears()`
  （bool get_是否有强制TwoDigitYears（））
- `bool YearMonthAdjustment(ref int year, ref int month, bool parsedMonthName)`
  （bool YearMonthAdjustment（ref int year, ref int month, bool parsedMonthName））
- `DateTimeFormatInfo GetJapaneseCalendarDTFI()`
  （Date时间格式化信息 获取JapaneseCalendarDTFI（））
- `DateTimeFormatInfo GetTaiwanCalendarDTFI()`
  （Date时间格式化信息 获取TaiwanCalendarDTFI（））
- `void ClearTokenHashTable()`
  （void 清除令牌HashTable（））
- `TokenHashValue[] CreateTokenHashTable()`
  （令牌HashValue[] 创建令牌HashTable（））
- `void AddMonthNames(TokenHashValue[] temp, string monthPostfix)`
  （void 添加MonthNames（令牌HashValue[] temp, string monthPostfix））
- `bool TryParseHebrewNumber(ref __DTString str, out bool badFormat, out int number)`
  （bool Try解析HebrewNumber（ref __DTString str, out bool badFormat, out int number））
- `bool IsHebrewChar(char ch)`
  （bool 是否HebrewChar（char ch））
- `bool Tokenize(TokenType TokenMask, out TokenType tokenType, out int tokenValue, ref __DTString str)`
  （bool Tokenize（令牌类型 TokenMask, out TokenType tokenType, out int tokenValue, ref __DTString str））
- `void InsertAtCurrentHashNode(TokenHashValue[] hashTable, string str, char ch, TokenType tokenType, int tokenValue, int pos, int hashcode, int hashProbe)`
  （void InsertAt当前Hash节点（令牌HashValue[] hashTable, string str, char ch, 令牌类型 tokenType, int tokenValue, int pos, int hashcode, int hashProbe））
- `void InsertHash(TokenHashValue[] hashTable, string str, TokenType tokenType, int tokenValue)`
  （void InsertHash（令牌HashValue[] hashTable, string str, 令牌类型 tokenType, int tokenValue））

---

## DateTimeFormatInfoScanner（Date时间格式化信息Scanner）

### 字段 (2)

- `List<string> m_dateWords`（List<string> m_dateWords）(偏移: 0x8)
- `DateTimeFormatInfoScanner.FoundDatePattern m_ymdFlags`（Date时间格式化信息Scanner.FoundDatePattern m_ymdFlags）(偏移: 0xC)

### 方法 (14)

- `int SkipWhiteSpacesAndNonLetter(string pattern, int currentIndex)`
  （int SkipWhiteSpacesAndNonLetter（string pattern, int currentIndex））
- `void AddDateWordOrPostfix(string formatPostfix, string str)`
  （void 添加DateWordOrPostfix（string formatPostfix, string str））
- `int AddDateWords(string pattern, int index, string formatPostfix)`
  （int 添加DateWords（string pattern, int index, string formatPostfix））
- `int ScanRepeatChar(string pattern, char ch, int index, out int count)`
  （int ScanRepeatChar（string pattern, char ch, int index, out int count））
- `void AddIgnorableSymbols(string text)`
  （void 添加IgnorableSymbols（string text））
- `void ScanDateWord(string pattern)`
  （void ScanDateWord（string pattern））
- `string[] GetDateWordsOfDTFI(DateTimeFormatInfo dtfi)`
  （string[] 获取DateWordsOfDTFI（Date时间格式化信息 dtfi））
- `FORMATFLAGS GetFormatFlagGenitiveMonth(string[] monthNames, string[] genitveMonthNames, string[] abbrevMonthNames, string[] genetiveAbbrevMonthNames)`
  （FORMATFLAGS 获取格式化标志GenitiveMonth（string[] monthNames, string[] genitveMonthNames, string[] abbrevMonthNames, string[] genetiveAbbrevMonthNames））
- `FORMATFLAGS GetFormatFlagUseSpaceInMonthNames(string[] monthNames, string[] genitveMonthNames, string[] abbrevMonthNames, string[] genetiveAbbrevMonthNames)`
  （FORMATFLAGS 获取格式化标志UseSpaceInMonthNames（string[] monthNames, string[] genitveMonthNames, string[] abbrevMonthNames, string[] genetiveAbbrevMonthNames））
- `FORMATFLAGS GetFormatFlagUseSpaceInDayNames(string[] dayNames, string[] abbrevDayNames)`
  （FORMATFLAGS 获取格式化标志UseSpaceInDayNames（string[] dayNames, string[] abbrevDayNames））
- `FORMATFLAGS GetFormatFlagUseHebrewCalendar(int calID)`
  （FORMATFLAGS 获取格式化标志UseHebrewCalendar（int calID））
- `bool EqualStringArrays(string[] array1, string[] array2)`
  （bool Equal字符串Arrays（string[] array1, string[] array2））
- `bool ArrayElementsHaveSpace(string[] array)`
  （bool 数组ElementsHaveSpace（string[] array））
- `bool ArrayElementsBeginWithDigit(string[] array)`
  （bool 数组ElementsBeginWithDigit（string[] array））

---

## DateTimeFormatInfoScanner.FoundDatePattern（Date时间格式化信息Scanner.FoundDatePattern）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DateTimeKind（Date时间Kind）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DateTimeOffset（Date时间Offset）

**继承**: IComparable, IFormattable, ISerializable, IDeserializationCallback, IComparable<DateTimeOffset>, IEquatable<DateTimeOffset>（IComparable, IFormattable, ISerializable, IDeserialization回调, IComparable<Date时间Offset>, IEquatable<Date时间Offset>）

### 字段 (4)

- `DateTimeOffset MinValue`（Date时间Offset 最小值）(偏移: 0x0)
- `DateTimeOffset MaxValue`（Date时间Offset 最大值）(偏移: 0x10)
- `DateTime m_dateTime`（Date时间 m_date时间）(偏移: 0x0)
- `short m_offsetMinutes`（short m_offsetMinutes）(偏移: 0x8)

### 方法 (12)

- `DateTime get_UtcDateTime()`
  （Date时间 get_UtcDate时间（））
- `DateTime get_ClockDateTime()`
  （Date时间 get_时钟Date时间（））
- `TimeSpan get_Offset()`
  （时间Span get_Offset（））
- `long get_Ticks()`
  （long get_Ticks（））
- `int CompareTo(DateTimeOffset other)`
  （int CompareTo（Date时间Offset other））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(DateTimeOffset other)`
  （bool Equals（Date时间Offset other））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `string ToString()`
  （字符串 转字符串（））
- `string ToString(string format, IFormatProvider formatProvider)`
  （字符串 转字符串（字符串 格式, I格式化提供者 formatProvider））
- `short ValidateOffset(TimeSpan offset)`
  （short 验证Offset（时间Span offset））
- `DateTime ValidateDate(DateTime dateTime, TimeSpan offset)`
  （Date时间 验证Date（Date时间 dateTime, 时间Span offset））

---

## DateTimeOffsetTypeInfo（Date时间Offset类型信息）

**继承**: TraceLoggingTypeInfo<DateTimeOffset>（TraceLogging类型Info<Date时间Offset>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void 写入元数据（跟踪日志元数据收集器 collector, 字符串 name, 事件字段格式 format））
- `void WriteData(TraceLoggingDataCollector collector, ref DateTimeOffset value)`
  （void Write数据（TraceLogging数据Collector collector, ref DateTimeOffset value））

---

## DateTimeParse（Date时间解析）

### 字段 (2)

- `DateTimeParse.MatchNumberDelegate m_hebrewNumberParser`（Date时间Parse.比赛Number委托 m_hebrewNumberParser）(偏移: 0x0)
- `DateTimeParse.DS[][] dateParsingStates`（Date时间Parse.DS[][] dateParsingStates）(偏移: 0x4)

### 方法 (51)

- `bool IsDigit(char ch)`
  （bool 是否Digit（char ch））
- `bool ParseFraction(ref __DTString str, out double result)`
  （bool 解析Fraction（ref __DTString str, out double result））
- `bool ParseTimeZone(ref __DTString str, ref TimeSpan result)`
  （bool 解析时间Zone（ref __DTString str, ref TimeSpan result））
- `bool HandleTimeZone(ref __DTString str, ref DateTimeResult result)`
  （bool 句柄时间Zone（ref __DTString str, ref DateTimeResult result））
- `bool Lex(DateTimeParse.DS dps, ref __DTString str, ref DateTimeToken dtok, ref DateTimeRawInfo raw, ref DateTimeResult result, ref DateTimeFormatInfo dtfi, DateTimeStyles styles)`
  （bool Lex（Date时间Parse.DS dps, ref __DTString str, ref DateTimeToken dtok, ref DateTimeRawInfo raw, ref DateTimeResult result, ref DateTimeFormatInfo dtfi, Date时间Styles styles））
- `bool VerifyValidPunctuation(ref __DTString str)`
  （bool VerifyValidPunctuation（ref __DTString str））
- `bool GetYearMonthDayOrder(string datePattern, DateTimeFormatInfo dtfi, out int order)`
  （bool 获取YearMonthDayOrder（string datePattern, Date时间格式化信息 dtfi, out int order））
- `bool GetYearMonthOrder(string pattern, DateTimeFormatInfo dtfi, out int order)`
  （bool 获取YearMonthOrder（string pattern, Date时间格式化信息 dtfi, out int order））
- `bool GetMonthDayOrder(string pattern, DateTimeFormatInfo dtfi, out int order)`
  （bool 获取MonthDayOrder（string pattern, Date时间格式化信息 dtfi, out int order））
- `bool TryAdjustYear(ref DateTimeResult result, int year, out int adjustedYear)`
  （bool TryAdjustYear（ref DateTimeResult result, int year, out int adjustedYear））
- `bool SetDateYMD(ref DateTimeResult result, int year, int month, int day)`
  （bool 集合DateYMD（ref DateTimeResult result, int year, int month, int day））
- `bool SetDateMDY(ref DateTimeResult result, int month, int day, int year)`
  （bool 集合DateMDY（ref DateTimeResult result, int month, int day, int year））
- `bool SetDateDMY(ref DateTimeResult result, int day, int month, int year)`
  （bool 集合DateDMY（ref DateTimeResult result, int day, int month, int year））
- `bool SetDateYDM(ref DateTimeResult result, int year, int day, int month)`
  （bool 集合DateYDM（ref DateTimeResult result, int year, int day, int month））
- `void GetDefaultYear(ref DateTimeResult result, ref DateTimeStyles styles)`
  （void 获取默认的Year（ref DateTimeResult result, ref DateTimeStyles styles））
- `bool GetDayOfNN(ref DateTimeResult result, ref DateTimeStyles styles, ref DateTimeRawInfo raw, DateTimeFormatInfo dtfi)`
  （bool 获取DayOfNN（ref DateTimeResult result, ref DateTimeStyles styles, ref DateTimeRawInfo raw, Date时间格式化信息 dtfi））
- `bool GetDayOfNNN(ref DateTimeResult result, ref DateTimeRawInfo raw, DateTimeFormatInfo dtfi)`
  （bool 获取DayOfNNN（ref DateTimeResult result, ref DateTimeRawInfo raw, Date时间格式化信息 dtfi））
- `bool GetDayOfMN(ref DateTimeResult result, ref DateTimeStyles styles, ref DateTimeRawInfo raw, DateTimeFormatInfo dtfi)`
  （bool 获取DayOfMN（ref DateTimeResult result, ref DateTimeStyles styles, ref DateTimeRawInfo raw, Date时间格式化信息 dtfi））
- `bool GetHebrewDayOfNM(ref DateTimeResult result, ref DateTimeRawInfo raw, DateTimeFormatInfo dtfi)`
  （bool 获取HebrewDayOfNM（ref DateTimeResult result, ref DateTimeRawInfo raw, Date时间格式化信息 dtfi））
- `bool GetDayOfNM(ref DateTimeResult result, ref DateTimeStyles styles, ref DateTimeRawInfo raw, DateTimeFormatInfo dtfi)`
  （bool 获取DayOfNM（ref DateTimeResult result, ref DateTimeStyles styles, ref DateTimeRawInfo raw, Date时间格式化信息 dtfi））
- `bool GetDayOfMNN(ref DateTimeResult result, ref DateTimeRawInfo raw, DateTimeFormatInfo dtfi)`
  （bool 获取DayOfMNN（ref DateTimeResult result, ref DateTimeRawInfo raw, Date时间格式化信息 dtfi））
- `bool GetDayOfYNN(ref DateTimeResult result, ref DateTimeRawInfo raw, DateTimeFormatInfo dtfi)`
  （bool 获取DayOfYNN（ref DateTimeResult result, ref DateTimeRawInfo raw, Date时间格式化信息 dtfi））
- `bool GetDayOfNNY(ref DateTimeResult result, ref DateTimeRawInfo raw, DateTimeFormatInfo dtfi)`
  （bool 获取DayOfNNY（ref DateTimeResult result, ref DateTimeRawInfo raw, Date时间格式化信息 dtfi））
- `bool GetDayOfYMN(ref DateTimeResult result, ref DateTimeRawInfo raw, DateTimeFormatInfo dtfi)`
  （bool 获取DayOfYMN（ref DateTimeResult result, ref DateTimeRawInfo raw, Date时间格式化信息 dtfi））
- `bool GetDayOfYN(ref DateTimeResult result, ref DateTimeRawInfo raw, DateTimeFormatInfo dtfi)`
  （bool 获取DayOfYN（ref DateTimeResult result, ref DateTimeRawInfo raw, Date时间格式化信息 dtfi））
- `bool GetDayOfYM(ref DateTimeResult result, ref DateTimeRawInfo raw, DateTimeFormatInfo dtfi)`
  （bool 获取DayOfYM（ref DateTimeResult result, ref DateTimeRawInfo raw, Date时间格式化信息 dtfi））
- `void AdjustTimeMark(DateTimeFormatInfo dtfi, ref DateTimeRawInfo raw)`
  （void Adjust时间Mark（Date时间格式化信息 dtfi, ref DateTimeRawInfo raw））
- `bool AdjustHour(ref int hour, DateTimeParse.TM timeMark)`
  （bool AdjustHour（ref int hour, Date时间Parse.TM timeMark））
- `bool GetTimeOfN(DateTimeFormatInfo dtfi, ref DateTimeResult result, ref DateTimeRawInfo raw)`
  （bool 获取时间OfN（Date时间格式化信息 dtfi, ref DateTimeResult result, ref DateTimeRawInfo raw））
- `bool GetTimeOfNN(DateTimeFormatInfo dtfi, ref DateTimeResult result, ref DateTimeRawInfo raw)`
  （bool 获取时间OfNN（Date时间格式化信息 dtfi, ref DateTimeResult result, ref DateTimeRawInfo raw））
- `bool GetTimeOfNNN(DateTimeFormatInfo dtfi, ref DateTimeResult result, ref DateTimeRawInfo raw)`
  （bool 获取时间OfNNN（Date时间格式化信息 dtfi, ref DateTimeResult result, ref DateTimeRawInfo raw））
- `bool GetDateOfDSN(ref DateTimeResult result, ref DateTimeRawInfo raw)`
  （bool 获取DateOfDSN（ref DateTimeResult result, ref DateTimeRawInfo raw））
- `bool GetDateOfNDS(ref DateTimeResult result, ref DateTimeRawInfo raw)`
  （bool 获取DateOfNDS（ref DateTimeResult result, ref DateTimeRawInfo raw））
- `bool GetDateOfNNDS(ref DateTimeResult result, ref DateTimeRawInfo raw, DateTimeFormatInfo dtfi)`
  （bool 获取DateOfNNDS（ref DateTimeResult result, ref DateTimeRawInfo raw, Date时间格式化信息 dtfi））
- `bool ProcessDateTimeSuffix(ref DateTimeResult result, ref DateTimeRawInfo raw, ref DateTimeToken dtok)`
  （bool 处理Date时间Suffix（ref DateTimeResult result, ref DateTimeRawInfo raw, ref DateTimeToken dtok））
- `bool ProcessHebrewTerminalState(DateTimeParse.DS dps, ref DateTimeResult result, ref DateTimeStyles styles, ref DateTimeRawInfo raw, DateTimeFormatInfo dtfi)`
  （bool 处理HebrewTerminal状态（Date时间Parse.DS dps, ref DateTimeResult result, ref DateTimeStyles styles, ref DateTimeRawInfo raw, Date时间格式化信息 dtfi））
- `bool ProcessTerminaltState(DateTimeParse.DS dps, ref DateTimeResult result, ref DateTimeStyles styles, ref DateTimeRawInfo raw, DateTimeFormatInfo dtfi)`
  （bool 处理Terminalt状态（Date时间Parse.DS dps, ref DateTimeResult result, ref DateTimeStyles styles, ref DateTimeRawInfo raw, Date时间格式化信息 dtfi））
- `DateTime Parse(string s, DateTimeFormatInfo dtfi, DateTimeStyles styles)`
  （Date时间 解析（string s, Date时间格式化信息 dtfi, Date时间Styles styles））
- `bool TryParse(string s, DateTimeFormatInfo dtfi, DateTimeStyles styles, out DateTime result)`
  （bool Try解析（string s, Date时间格式化信息 dtfi, Date时间Styles styles, out DateTime result））
- `bool TryParse(string s, DateTimeFormatInfo dtfi, DateTimeStyles styles, ref DateTimeResult result)`
  （bool Try解析（string s, Date时间格式化信息 dtfi, Date时间Styles styles, ref DateTimeResult result））
- `bool DetermineTimeZoneAdjustments(ref DateTimeResult result, DateTimeStyles styles, bool bTimeOnly)`
  （bool Determine时间ZoneAdjustments（ref DateTimeResult result, Date时间Styles styles, bool bTimeOnly））
- `bool DateTimeOffsetTimeZonePostProcessing(ref DateTimeResult result, DateTimeStyles styles)`
  （bool Date时间Offset时间ZonePostProcessing（ref DateTimeResult result, Date时间Styles styles））
- `bool AdjustTimeZoneToUniversal(ref DateTimeResult result)`
  （bool Adjust时间ZoneToUniversal（ref DateTimeResult result））
- `bool AdjustTimeZoneToLocal(ref DateTimeResult result, bool bTimeOnly)`
  （bool Adjust时间ZoneTo本地的（ref DateTimeResult result, bool bTimeOnly））
- `bool ParseISO8601(ref DateTimeRawInfo raw, ref __DTString str, DateTimeStyles styles, ref DateTimeResult result)`
  （bool 解析ISO8601（ref DateTimeRawInfo raw, ref __DTString str, Date时间Styles styles, ref DateTimeResult result））
- `bool MatchHebrewDigits(ref __DTString str, int digitLen, out int number)`
  （bool 比赛HebrewDigits（ref __DTString str, int digitLen, out int number））
- `bool ParseDigits(ref __DTString str, int digitLen, out int result)`
  （bool 解析Digits（ref __DTString str, int digitLen, out int result））
- `bool ParseDigits(ref __DTString str, int minDigitLen, int maxDigitLen, out int result)`
  （bool 解析Digits（ref __DTString str, int minDigitLen, int maxDigitLen, out int result））
- `DateTime GetDateTimeNow(ref DateTimeResult result, ref DateTimeStyles styles)`
  （Date时间 获取Date时间Now（ref DateTimeResult result, ref DateTimeStyles styles））
- `bool CheckDefaultDateTime(ref DateTimeResult result, ref Calendar cal, DateTimeStyles styles)`
  （bool 检查默认的Date时间（ref DateTimeResult result, ref Calendar cal, Date时间Styles styles））
- `Exception GetDateTimeParseException(ref DateTimeResult result)`
  （Exception 获取Date时间解析Exception（ref DateTimeResult result））

---

## DateTimeParse.DS（Date时间Parse.DS）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DateTimeParse.DTT（Date时间Parse.DTT）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DateTimeParse.MatchNumberDelegate（Date时间Parse.比赛Number委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `bool Invoke(ref __DTString str, int digitLen, out int result)`
  （bool Invoke（ref __DTString str, int digitLen, out int result））
- `IAsyncResult BeginInvoke(ref __DTString str, int digitLen, out int result, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（ref __DTString str, int digitLen, out int result, 异步回调 callback, object object））
- `bool EndInvoke(ref __DTString str, out int result, IAsyncResult __result)`
  （bool 结束Invoke（ref __DTString str, out int result, I异步Result __result））

---

## DateTimeParse.TM（Date时间Parse.TM）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DateTimeRawInfo（Date时间Raw信息）

### 字段 (10)

- `int* num`（int* num）(偏移: 0x0)
- `int numCount`（int num数量）(偏移: 0x4)
- `int month`（int month）(偏移: 0x8)
- `int year`（int year）(偏移: 0xC)
- `int dayOfWeek`（int dayOfWeek）(偏移: 0x10)
- `int era`（int era）(偏移: 0x14)
- `DateTimeParse.TM timeMark`（Date时间Parse.TM timeMark）(偏移: 0x18)
- `double fraction`（double fraction）(偏移: 0x20)
- `bool hasSameDateAndTimeSeparators`（bool hasSameDateAnd时间Separators）(偏移: 0x28)
- `bool timeZone`（bool timeZone）(偏移: 0x29)

### 方法 (3)

- `void Init(int* numberBuffer)`
  （void 初始化（int* numberBuffer））
- `void AddNumber(int value)`
  （void 添加Number（int value））
- `int GetNumber(int index)`
  （int 获取Number（int index））

---

## DateTimeResult（Date时间Result）

### 字段 (16)

- `int Year`（int Year）(偏移: 0x0)
- `int Month`（int Month）(偏移: 0x4)
- `int Day`（int Day）(偏移: 0x8)
- `int Hour`（int Hour）(偏移: 0xC)
- `int Minute`（int Minute）(偏移: 0x10)
- `int Second`（int Second）(偏移: 0x14)
- `double fraction`（double fraction）(偏移: 0x18)
- `int era`（int era）(偏移: 0x20)
- `ParseFlags flags`（解析Flags flags）(偏移: 0x24)
- `TimeSpan timeZoneOffset`（时间Span timeZoneOffset）(偏移: 0x28)
- `Calendar calendar`（Calendar calendar）(偏移: 0x30)
- `DateTime parsedDate`（Date时间 parsedDate）(偏移: 0x38)
- `ParseFailureKind failure`（解析FailureKind failure）(偏移: 0x40)
- `string failureMessageID`（string failureMessageID）(偏移: 0x44)
- `object failureMessageFormatArgument`（object failureMessage格式化Argument）(偏移: 0x48)
- `string failureArgumentName`（string failureArgument名称）(偏移: 0x4C)

### 方法 (4)

- `void Init()`
  （void 初始化（））
- `void SetDate(int year, int month, int day)`
  （void 集合Date（int year, int month, int day））
- `void SetFailure(ParseFailureKind failure, string failureMessageID, object failureMessageFormatArgument)`
  （void 集合Failure（解析FailureKind failure, string failureMessageID, object failureMessageFormatArgument））
- `void SetFailure(ParseFailureKind failure, string failureMessageID, object failureMessageFormatArgument, string failureArgumentName)`
  （void 集合Failure（解析FailureKind failure, string failureMessageID, object failureMessageFormatArgument, string failureArgumentName））

---

## DateTimeStyles（Date时间Styles）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DateTimeToken（Date时间令牌）

### 字段 (3)

- `DateTimeParse.DTT dtt`（Date时间Parse.DTT dtt）(偏移: 0x0)
- `TokenType suffix`（令牌类型 suffix）(偏移: 0x4)
- `int num`（int num）(偏移: 0x8)

---

## DateTimeTypeInfo（Date时间类型信息）

**继承**: TraceLoggingTypeInfo<DateTime>（TraceLogging类型Info<DateTime>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void 写入元数据（跟踪日志元数据收集器 collector, 字符串 name, 事件字段格式 format））
- `void WriteData(TraceLoggingDataCollector collector, ref DateTime value)`
  （void Write数据（TraceLogging数据Collector collector, ref DateTime value））

---

## DayOfWeek（DayOfWeek）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DeathEventData（死亡事件数据）

### 字段 (12)

- `Entity killer`（实体 killer）(偏移: 0x0)
- `Entity dead`（实体 dead）(偏移: 0x4)
- `HeadShotType headShot`（头部射击类型 head射击）(偏移: 0x8)
- `bool wallThrough`（bool wallThrough）(偏移: 0xC)
- `DamageType damageType`（伤害类型 damage类型）(偏移: 0x10)
- `Vector3 damageOrigin`（三维向量 damageOrigin）(偏移: 0x14)
- `SpecialKillType specialKill`（特殊击杀类型 special击杀）(偏移: 0x20)
- `NanoKillType nanoKill`（纳米击杀类型 nano击杀）(偏移: 0x24)
- `bool revenge`（bool revenge）(偏移: 0x28)
- `DamageTag damageTag`（伤害标签 damage标签）(偏移: 0x2C)
- `int wpnIndex`（int 武器索引）(偏移: 0x30)
- `int wpnSprIndex`（int 武器Spr索引）(偏移: 0x34)

### 方法 (3)

- `Sprite get_killMsgIcon()`
  （精灵 get_killMsg图标（））
- `bool get_isVVIP()`
  （bool get_isVVIP（））
- `string get_wpnName()`
  （string get_wpn名称（））

---

## Debug（Debug）

### 字段 (2)

- `ILogger s_DefaultLogger`（ILogger s_默认的Logger）(偏移: 0x0)
- `ILogger s_Logger`（ILogger s_Logger）(偏移: 0x4)

### 方法 (23)

- `ILogger get_unityLogger()`
  （ILogger get_unityLogger（））
- `void DrawLine(Vector3 start, Vector3 end, Color color, float duration)`
  （void DrawLine（三维向量 start, 三维向量 end, 颜色 color, float duration））
- `void DrawLine(Vector3 start, Vector3 end, Color color)`
  （void DrawLine（三维向量 start, 三维向量 end, 颜色 color））
- `void DrawLine(Vector3 start, Vector3 end)`
  （void DrawLine（三维向量 start, 三维向量 end））
- `void DrawLine(Vector3 start, Vector3 end, Color color, float duration, bool depthTest)`
  （void DrawLine（三维向量 start, 三维向量 end, 颜色 color, float duration, bool depthTest））
- `void DrawRay(Vector3 start, Vector3 dir, Color color)`
  （void DrawRay（三维向量 start, 三维向量 dir, 颜色 color））
- `void DrawRay(Vector3 start, Vector3 dir, Color color, float duration, bool depthTest)`
  （void DrawRay（三维向量 start, 三维向量 dir, 颜色 color, float duration, bool depthTest））
- `int ExtractStackTraceNoAlloc(byte* buffer, int bufferMax, string projectFolder)`
  （int Extract栈TraceNoAlloc（byte* buffer, int bufferMax, string projectFolder））
- `void Log(object message)`
  （void Log（object message））
- `void Log(object message, Object context)`
  （void Log（object message, 对象 context））
- `void LogError(object message)`
  （void LogError（object message））
- `void LogError(object message, Object context)`
  （void LogError（object message, 对象 context））
- `void LogErrorFormat(string format, object[] args)`
  （void LogError格式化（string format, object[] args））
- `void LogErrorFormat(Object context, string format, object[] args)`
  （void LogError格式化（对象 context, string format, object[] args））
- `void LogException(Exception exception)`
  （void LogException（Exception exception））
- `void LogException(Exception exception, Object context)`
  （void LogException（Exception exception, 对象 context））
- `void LogWarning(object message)`
  （void LogWarning（object message））
- `void LogWarning(object message, Object context)`
  （void LogWarning（object message, 对象 context））
- `void LogWarningFormat(Object context, string format, object[] args)`
  （void LogWarning格式化（对象 context, string format, object[] args））
- `bool get_isDebugBuild()`
  （bool get_isDebugBuild（））
- `bool CallOverridenDebugHandler(Exception exception, Object obj)`
  （bool CallOverridenDebug处理器（Exception exception, 对象 obj））
- `bool IsLoggingEnabled()`
  （bool 是否Logging启用的（））
- `void DrawLine_Injected(ref Vector3 start, ref Vector3 end, ref Color color, float duration, bool depthTest)`
  （void DrawLine_Injected（ref Vector3 start, ref Vector3 end, ref Color color, float duration, bool depthTest））

---

## DebugAction（Debug动作）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DebugActionDesc（Debug动作Desc）

### 字段 (5)

- `string axisTrigger`（string axis触发器）(偏移: 0x8)
- `List<string[]> buttonTriggerList`（List<string[]> button触发器列表）(偏移: 0xC)
- `List<KeyCode[]> keyTriggerList`（List<键Code[]> key触发器列表）(偏移: 0x10)
- `DebugActionRepeatMode repeatMode`（Debug动作Repeat模式 repeat模式）(偏移: 0x14)
- `float repeatDelay`（float repeat延迟）(偏移: 0x18)

---

## DebugActionRepeatMode（Debug动作Repeat模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DebugActionState（Debug动作状态）

### 字段 (6)

- `DebugActionState.DebugActionKeyType m_Type`（Debug动作State.Debug动作键类型 m_类型）(偏移: 0x8)
- `string[] m_PressedButtons`（string[] m_按下的Buttons）(偏移: 0xC)
- `string m_PressedAxis`（string m_按下的轴）(偏移: 0x10)
- `KeyCode[] m_PressedKeys`（键Code[] m_按下的Keys）(偏移: 0x14)
- `bool[] m_TriggerPressedUp`（bool[] m_触发器按下的上）(偏移: 0x18)
- `float m_Timer`（float m_计时器）(偏移: 0x1C)

### 方法 (10)

- `bool get_runningAction()`
  （bool get_running动作（））
- `void set_runningAction(bool value)`
  （void set_running动作（bool value））
- `float get_actionState()`
  （float get_action状态（））
- `void set_actionState(float value)`
  （void set_action状态（float value））
- `void Trigger(int triggerCount, float state)`
  （void 触发器（int triggerCount, float state））
- `void TriggerWithButton(string[] buttons, float state)`
  （void 触发器With按钮（string[] buttons, float state））
- `void TriggerWithAxis(string axis, float state)`
  （void 触发器With轴（string axis, float state））
- `void TriggerWithKey(KeyCode[] keys, float state)`
  （void 触发器With键（键Code[] keys, float state））
- `void Reset()`
  （void 重置（））
- `void Update(DebugActionDesc desc)`
  （void 更新（Debug动作Desc desc））

---

## DebugActionState.DebugActionKeyType（Debug动作State.Debug动作键类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DebugLogHandler（DebugLog处理器）

**继承**: ILogHandler（ILog处理器）

### 方法 (4)

- `void Internal_Log(LogType level, LogOption options, string msg, Object obj)`
  （void Internal_Log（Log类型 level, LogOption options, string msg, 对象 obj））
- `void Internal_LogException(Exception ex, Object obj)`
  （void Internal_LogException（Exception ex, 对象 obj））
- `void LogFormat(LogType logType, Object context, string format, object[] args)`
  （void Log格式化（Log类型 logType, 对象 context, string format, object[] args））
- `void LogException(Exception exception, Object context)`
  （void LogException（Exception exception, 对象 context））

---

## DebugManager（Debug管理器）

### 字段 (15)

- `DebugActionDesc[] m_DebugActions`（Debug动作Desc[] m_DebugActions）(偏移: 0x8)
- `DebugActionState[] m_DebugActionStates`（Debug动作State[] m_Debug动作States）(偏移: 0xC)
- `Lazy<DebugManager> s_Instance`（Lazy<DebugManager> s_实例）(偏移: 0x0)
- `ReadOnlyCollection<DebugUI.Panel> m_ReadOnlyPanels`（ReadOnlyCollection<DebugUI.Panel> m_ReadOnlyPanels）(偏移: 0x10)
- `List<DebugUI.Panel> m_Panels`（List<DebugUI.Panel> m_Panels）(偏移: 0x14)
- `Action<bool> onDisplayRuntimeUIChanged`（Action<bool> onDisplayRuntime界面Changed）(偏移: 0x18)
- `Action onSetDirty`（动作 on集合Dirty）(偏移: 0x1C)
- `Action resetData`（动作 reset数据）(偏移: 0x20)
- `bool refreshEditorRequested`（bool refreshEditorRequested）(偏移: 0x24)
- `GameObject m_Root`（游戏对象 m_根）(偏移: 0x28)
- `DebugUIHandlerCanvas m_RootUICanvas`（Debug界面处理器画布 m_根界面画布）(偏移: 0x2C)
- `GameObject m_PersistentRoot`（游戏对象 m_持久的根）(偏移: 0x30)
- `DebugUIHandlerPersistentCanvas m_RootUIPersistentCanvas`（Debug界面处理器持久的画布 m_根界面持久的画布）(偏移: 0x34)
- `bool m_EditorOpen`（bool m_Editor打开）(偏移: 0x38)
- `bool m_EnableRuntimeUI`（bool m_启用Runtime界面）(偏移: 0x39)

### 方法 (40)

- `void RegisterActions()`
  （void RegisterActions（））
- `void AddAction(DebugAction action, DebugActionDesc desc)`
  （void 添加动作（Debug动作 action, Debug动作Desc desc））
- `void SampleAction(int actionIndex)`
  （void Sample动作（int actionIndex））
- `void UpdateAction(int actionIndex)`
  （void 更新动作（int actionIndex））
- `void UpdateActions()`
  （void 更新Actions（））
- `float GetAction(DebugAction action)`
  （float 获取动作（Debug动作 action））
- `void RegisterInputs()`
  （void RegisterInputs（））
- `DebugManager get_instance()`
  （Debug管理器 get_instance（））
- `void UpdateReadOnlyCollection()`
  （void 更新ReadOnlyCollection（））
- `ReadOnlyCollection<DebugUI.Panel> get_panels()`
  （ReadOnlyCollection<DebugUI.Panel> get_panels（））
- `void add_onDisplayRuntimeUIChanged(Action<bool> value)`
  （void add_onDisplayRuntime界面Changed（Action<bool> value））
- `void remove_onDisplayRuntimeUIChanged(Action<bool> value)`
  （void remove_onDisplayRuntime界面Changed（Action<bool> value））
- `void add_onSetDirty(Action value)`
  （void add_on集合Dirty（动作 value））
- `void remove_onSetDirty(Action value)`
  （void remove_on集合Dirty（动作 value））
- `void add_resetData(Action value)`
  （void add_reset数据（动作 value））
- `void remove_resetData(Action value)`
  （void remove_reset数据（动作 value））
- `bool get_displayEditorUI()`
  （bool get_displayEditor界面（））
- `void ToggleEditorUI(bool open)`
  （void 开关Editor界面（bool open））
- `bool get_enableRuntimeUI()`
  （bool get_enableRuntime界面（））
- `void set_enableRuntimeUI(bool value)`
  （void set_enableRuntime界面（bool value））
- `bool get_displayRuntimeUI()`
  （bool get_displayRuntime界面（））
- `void set_displayRuntimeUI(bool value)`
  （void set_displayRuntime界面（bool value））
- `bool get_displayPersistentRuntimeUI()`
  （bool get_display持久的Runtime界面（））
- `void set_displayPersistentRuntimeUI(bool value)`
  （void set_display持久的Runtime界面（bool value））
- `void RefreshEditor()`
  （void 刷新Editor（））
- `void Reset()`
  （void 重置（））
- `void ReDrawOnScreenDebug()`
  （void ReDrawOn屏幕的Debug（））
- `void RegisterData(IDebugData data)`
  （void Register数据（IDebug数据 data））
- `void UnregisterData(IDebugData data)`
  （void Unregister数据（IDebug数据 data））
- `int GetState()`
  （int 获取状态（））
- `void RegisterRootCanvas(DebugUIHandlerCanvas root)`
  （void Register根画布（Debug界面处理器画布 root））
- `void ChangeSelection(DebugUIHandlerWidget widget, bool fromNext)`
  （void ChangeSelection（Debug界面处理器Widget widget, bool fromNext））
- `void CheckPersistentCanvas()`
  （void 检查持久的画布（））
- `void TogglePersistent(DebugUI.Widget widget)`
  （void 开关持久的（DebugUI.Widget widget））
- `void OnPanelDirty(DebugUI.Panel panel)`
  （void On面板Dirty（DebugUI.面板 panel））
- `DebugUI.Panel GetPanel(string displayName, bool createIfNull = False, int groupIndex = 0, bool overrideIfExist = False)`
  （DebugUI.面板 获取面板（string displayName, bool createIfNull = False, int groupIndex = 0, bool overrideIfExist = False））
- `void RemovePanel(string displayName)`
  （void 移除面板（string displayName））
- `void RemovePanel(DebugUI.Panel panel)`
  （void 移除面板（DebugUI.面板 panel））
- `DebugUI.Widget GetItem(string queryPath)`
  （DebugUI.Widget 获取项目（string queryPath））
- `DebugUI.Widget GetItem(string queryPath, DebugUI.IContainer container)`
  （DebugUI.Widget 获取项目（string queryPath, DebugUI.I容器 container））

---

## DebugScreenCapture（Debug屏幕的Capture）

### 方法 (4)

- `void set_rawImageDataReference(NativeArray<byte> value)`
  （void set_raw图像数据引用（NativeArray<byte> value））
- `void set_imageFormat(TextureFormat value)`
  （void set_image格式化（纹理格式化 value））
- `void set_width(int value)`
  （void 设置_宽度（整数 value））
- `void set_height(int value)`
  （void 设置_高度（整数 value））

---

## DebugShapes（DebugShapes）

### 字段 (5)

- `DebugShapes s_Instance`（DebugShapes s_实例）(偏移: 0x0)
- `Mesh m_sphereMesh`（网格 m_sphere网格）(偏移: 0x8)
- `Mesh m_boxMesh`（网格 m_box网格）(偏移: 0xC)
- `Mesh m_coneMesh`（网格 m_cone网格）(偏移: 0x10)
- `Mesh m_pyramidMesh`（网格 m_pyramid网格）(偏移: 0x14)

### 方法 (11)

- `DebugShapes get_instance()`
  （DebugShapes get_instance（））
- `void BuildSphere(ref Mesh outputMesh, float radius, uint longSubdiv, uint latSubdiv)`
  （void BuildSphere（ref Mesh outputMesh, float radius, uint longSubdiv, uint latSubdiv））
- `void BuildBox(ref Mesh outputMesh, float length, float width, float height)`
  （void BuildBox（ref Mesh outputMesh, float length, float width, float height））
- `void BuildCone(ref Mesh outputMesh, float height, float topRadius, float bottomRadius, int nbSides)`
  （void BuildCone（ref Mesh outputMesh, float height, float topRadius, float bottomRadius, int nbSides））
- `void BuildPyramid(ref Mesh outputMesh, float width, float height, float depth)`
  （void BuildPyramid（ref Mesh outputMesh, float width, float height, float depth））
- `void BuildShapes()`
  （void BuildShapes（））
- `void RebuildResources()`
  （void RebuildResources（））
- `Mesh RequestSphereMesh()`
  （网格 请求Sphere网格（））
- `Mesh RequestBoxMesh()`
  （网格 请求Box网格（））
- `Mesh RequestConeMesh()`
  （网格 请求Cone网格（））
- `Mesh RequestPyramidMesh()`
  （网格 请求Pyramid网格（））

---

## DebugUI.BitField（DebugUI.BitField）

**继承**: DebugUI.Field<Enum>（DebugUI.Field<Enum>）

### 字段 (1)

- `Type m_EnumType`（类型 m_Enum类型）(偏移: 0x30)

### 方法 (6)

- `GUIContent[] get_enumNames()`
  （GUIContent[] get_enumNames（））
- `void set_enumNames(GUIContent[] value)`
  （void set_enumNames（GUIContent[] value））
- `int[] get_enumValues()`
  （int[] get_enumValues（））
- `void set_enumValues(int[] value)`
  （void set_enumValues（int[] value））
- `void set_enumType(Type value)`
  （void set_enum类型（类型 value））
- `Type get_enumType()`
  （类型 get_enum类型（））

---

## DebugUI.Button（DebugUI.按钮）

**继承**: DebugUI.Widget（DebugUI.Widget）

### 方法 (2)

- `Action get_action()`
  （动作 get_action（））
- `void set_action(Action value)`
  （void set_action（动作 value））

---

## DebugUI.ColorField（DebugUI.颜色Field）

**继承**: DebugUI.Field<Color>（DebugUI.Field<Color>）

### 字段 (6)

- `bool hdr`（布尔值 hdr）(偏移: 0x28)
- `bool showAlpha`（布尔值 显示透明度）(偏移: 0x29)
- `bool showPicker`（bool showPicker）(偏移: 0x2A)
- `float incStep`（浮点数 递增步长）(偏移: 0x2C)
- `float incStepMult`（浮点数 递增步长倍数）(偏移: 0x30)
- `int decimals`（整数 小数位数）(偏移: 0x34)

### 方法 (1)

- `Color ValidateValue(Color value)`
  （颜色 验证值（颜色 value））

---

## DebugUI.Container（DebugUI.容器）

**继承**: DebugUI.Widget, DebugUI.IContainer（DebugUI.Widget, DebugUI.I容器）

### 方法 (8)

- `ObservableList<DebugUI.Widget> get_children()`
  （ObservableList<DebugUI.Widget> get_children（））
- `void set_children(ObservableList<DebugUI.Widget> value)`
  （void set_children（ObservableList<DebugUI.Widget> value））
- `DebugUI.Panel get_panel()`
  （DebugUI.面板 get_panel（））
- `void set_panel(DebugUI.Panel value)`
  （void set_panel（DebugUI.面板 value））
- `void GenerateQueryPath()`
  （void GenerateQuery路径（））
- `void OnItemAdded(ObservableList<DebugUI.Widget> sender, ListChangedEventArgs<DebugUI.Widget> e)`
  （void On项目Added（ObservableList<DebugUI.Widget> sender, 列表Changed事件Args<DebugUI.Widget> e））
- `void OnItemRemoved(ObservableList<DebugUI.Widget> sender, ListChangedEventArgs<DebugUI.Widget> e)`
  （void On项目Removed（ObservableList<DebugUI.Widget> sender, 列表Changed事件Args<DebugUI.Widget> e））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## DebugUI.EnumField（DebugUI.EnumField）

**继承**: DebugUI.Field<int>（DebugUI.Field<int>）

### 字段 (4)

- `GUIContent[] enumNames`（GUIContent[] enumNames）(偏移: 0x28)
- `int[] enumValues`（int[] enumValues）(偏移: 0x2C)
- `int[] quickSeparators`（int[] quickSeparators）(偏移: 0x30)
- `int[] indexes`（int[] indexes）(偏移: 0x34)

### 方法 (9)

- `Func<int> get_getIndex()`
  （Func<int> get_get索引（））
- `void set_getIndex(Func<int> value)`
  （void set_get索引（Func<int> value））
- `Action<int> get_setIndex()`
  （Action<int> get_set索引（））
- `void set_setIndex(Action<int> value)`
  （void set_set索引（Action<int> value））
- `int get_currentIndex()`
  （int get_current索引（））
- `void set_currentIndex(int value)`
  （void set_current索引（int value））
- `void set_autoEnum(Type value)`
  （void set_autoEnum（类型 value））
- `void InitQuickSeparators()`
  （void 初始化QuickSeparators（））
- `void InitIndexes()`
  （void 初始化Indexes（））

---

## DebugUI.Flags（DebugUI.Flags）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DebugUI.FloatField（DebugUI.浮点数Field）

**继承**: DebugUI.Field<float>（DebugUI.Field<float>）

### 字段 (5)

- `Func<float> min`（Func<float> min）(偏移: 0x28)
- `Func<float> max`（Func<float> max）(偏移: 0x2C)
- `float incStep`（浮点数 递增步长）(偏移: 0x30)
- `float incStepMult`（浮点数 递增步长倍数）(偏移: 0x34)
- `int decimals`（整数 小数位数）(偏移: 0x38)

### 方法 (1)

- `float ValidateValue(float value)`
  （float 验证值（float value））

---

## DebugUI.Foldout（DebugUI.Foldout）

**继承**: DebugUI.Container, DebugUI.IValueField（DebugUI.容器, DebugUI.I值Field）

### 字段 (1)

- `bool opened`（bool opened）(偏移: 0x20)

### 方法 (7)

- `bool get_isReadOnly()`
  （bool get_isReadOnly（））
- `string[] get_columnLabels()`
  （string[] get_columnLabels（））
- `void set_columnLabels(string[] value)`
  （void set_columnLabels（string[] value））
- `bool GetValue()`
  （bool 获取值（））
- `void SetValue(object value)`
  （void 集合值（object value））
- `object ValidateValue(object value)`
  （object 验证值（object value））
- `void SetValue(bool value)`
  （void 集合值（bool value））

---

## DebugUI.HistoryBoolField（DebugUI.History布尔值Field）

**继承**: DebugUI.BoolField（DebugUI.布尔值Field）

### 方法 (4)

- `Func<bool>[] get_historyGetter()`
  （Func<bool>[] get_historyGetter（））
- `void set_historyGetter(Func<bool>[] value)`
  （void set_historyGetter（Func<bool>[] value））
- `int get_historyDepth()`
  （int get_history深度（））
- `bool GetHistoryValue(int historyIndex)`
  （bool 获取History值（int historyIndex））

---

## DebugUI.HistoryEnumField（DebugUI.HistoryEnumField）

**继承**: DebugUI.EnumField（DebugUI.EnumField）

### 方法 (4)

- `Func<int>[] get_historyIndexGetter()`
  （Func<int>[] get_history索引Getter（））
- `void set_historyIndexGetter(Func<int>[] value)`
  （void set_history索引Getter（Func<int>[] value））
- `int get_historyDepth()`
  （int get_history深度（））
- `int GetHistoryValue(int historyIndex)`
  （int 获取History值（int historyIndex））

---

## DebugUI.IntField（DebugUI.整数Field）

**继承**: DebugUI.Field<int>（DebugUI.Field<int>）

### 字段 (4)

- `Func<int> min`（Func<int> min）(偏移: 0x28)
- `Func<int> max`（Func<int> max）(偏移: 0x2C)
- `int incStep`（int incStep）(偏移: 0x30)
- `int intStepMult`（int intStepMult）(偏移: 0x34)

### 方法 (1)

- `int ValidateValue(int value)`
  （int 验证值（int value））

---

## DebugUI.Panel（DebugUI.面板）

**继承**: DebugUI.IContainer, IComparable<DebugUI.Panel>（DebugUI.I容器, IComparable<DebugUI.Panel>）

### 字段 (1)

- `Action<DebugUI.Panel> onSetDirty`（Action<DebugUI.Panel> on集合Dirty）(偏移: 0x18)

### 方法 (19)

- `DebugUI.Flags get_flags()`
  （DebugUI.Flags get_flags（））
- `void set_flags(DebugUI.Flags value)`
  （void set_flags（DebugUI.Flags value））
- `string get_displayName()`
  （string get_display名称（））
- `void set_displayName(string value)`
  （void set_display名称（string value））
- `int get_groupIndex()`
  （int get_group索引（））
- `void set_groupIndex(int value)`
  （void set_group索引（int value））
- `string get_queryPath()`
  （string get_query路径（））
- `bool get_isEditorOnly()`
  （bool get_isEditorOnly（））
- `bool get_isRuntimeOnly()`
  （bool get_isRuntimeOnly（））
- `bool get_isInactiveInEditor()`
  （bool get_isInactiveInEditor（））
- `bool get_editorForceUpdate()`
  （bool get_editor强制更新（））
- `ObservableList<DebugUI.Widget> get_children()`
  （ObservableList<DebugUI.Widget> get_children（））
- `void set_children(ObservableList<DebugUI.Widget> value)`
  （void set_children（ObservableList<DebugUI.Widget> value））
- `void add_onSetDirty(Action<DebugUI.Panel> value)`
  （void add_on集合Dirty（Action<DebugUI.Panel> value））
- `void remove_onSetDirty(Action<DebugUI.Panel> value)`
  （void remove_on集合Dirty（Action<DebugUI.Panel> value））
- `void OnItemAdded(ObservableList<DebugUI.Widget> sender, ListChangedEventArgs<DebugUI.Widget> e)`
  （void On项目Added（ObservableList<DebugUI.Widget> sender, 列表Changed事件Args<DebugUI.Widget> e））
- `void OnItemRemoved(ObservableList<DebugUI.Widget> sender, ListChangedEventArgs<DebugUI.Widget> e)`
  （void On项目Removed（ObservableList<DebugUI.Widget> sender, 列表Changed事件Args<DebugUI.Widget> e））
- `void SetDirty()`
  （void 设置_脏（））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## DebugUI.Table（DebugUI.Table）

**继承**: DebugUI.Container（DebugUI.容器）

### 字段 (2)

- `bool isReadOnly`（bool isReadOnly）(偏移: 0x20)
- `bool[] m_Header`（bool[] m_标题）(偏移: 0x24)

### 方法 (5)

- `void SetColumnVisibility(int index, bool visible)`
  （void 集合ColumnVisibility（int index, bool visible））
- `bool GetColumnVisibility(int index)`
  （bool 获取ColumnVisibility（int index））
- `bool[] get_VisibleColumns()`
  （bool[] get_可见的Columns（））
- `void OnItemAdded(ObservableList<DebugUI.Widget> sender, ListChangedEventArgs<DebugUI.Widget> e)`
  （void On项目Added（ObservableList<DebugUI.Widget> sender, 列表Changed事件Args<DebugUI.Widget> e））
- `void OnItemRemoved(ObservableList<DebugUI.Widget> sender, ListChangedEventArgs<DebugUI.Widget> e)`
  （void On项目Removed（ObservableList<DebugUI.Widget> sender, 列表Changed事件Args<DebugUI.Widget> e））

---

## DebugUI.UIntField（DebugUI.U整数Field）

**继承**: DebugUI.Field<uint>（DebugUI.Field<uint>）

### 字段 (4)

- `Func<uint> min`（Func<uint> min）(偏移: 0x28)
- `Func<uint> max`（Func<uint> max）(偏移: 0x2C)
- `uint incStep`（uint incStep）(偏移: 0x30)
- `uint intStepMult`（uint intStepMult）(偏移: 0x34)

### 方法 (1)

- `uint ValidateValue(uint value)`
  （uint 验证值（uint value））

---

## DebugUI.Value（DebugUI.值）

**继承**: DebugUI.Widget（DebugUI.Widget）

### 字段 (1)

- `float refreshRate`（float refreshRate）(偏移: 0x20)

### 方法 (3)

- `Func<object> get_getter()`
  （Func<object> get_getter（））
- `void set_getter(Func<object> value)`
  （void set_getter（Func<object> value））
- `object GetValue()`
  （object 获取值（））

---

## DebugUI.Vector2Field（DebugUI.二维向量Field）

**继承**: DebugUI.Field<Vector2>（DebugUI.Field<Vector2>）

### 字段 (3)

- `float incStep`（浮点数 递增步长）(偏移: 0x28)
- `float incStepMult`（浮点数 递增步长倍数）(偏移: 0x2C)
- `int decimals`（整数 小数位数）(偏移: 0x30)

---

## DebugUI.Vector3Field（DebugUI.三维向量Field）

**继承**: DebugUI.Field<Vector3>（DebugUI.Field<Vector3>）

### 字段 (3)

- `float incStep`（浮点数 递增步长）(偏移: 0x28)
- `float incStepMult`（浮点数 递增步长倍数）(偏移: 0x2C)
- `int decimals`（整数 小数位数）(偏移: 0x30)

---

## DebugUI.Vector4Field（DebugUI.Vector4Field）

**继承**: DebugUI.Field<Vector4>（DebugUI.Field<Vector4>）

### 字段 (3)

- `float incStep`（浮点数 递增步长）(偏移: 0x28)
- `float incStepMult`（浮点数 递增步长倍数）(偏移: 0x2C)
- `int decimals`（整数 小数位数）(偏移: 0x30)

---

## DebugUI.Widget（DebugUI.Widget）

### 字段 (2)

- `DebugUI.Panel m_Panel`（DebugUI.面板 m_面板）(偏移: 0x8)
- `DebugUI.IContainer m_Parent`（DebugUI.I容器 m_父级）(偏移: 0xC)

### 方法 (15)

- `DebugUI.Panel get_panel()`
  （DebugUI.面板 get_panel（））
- `void set_panel(DebugUI.Panel value)`
  （void set_panel（DebugUI.面板 value））
- `DebugUI.IContainer get_parent()`
  （DebugUI.I容器 get_parent（））
- `void set_parent(DebugUI.IContainer value)`
  （void set_parent（DebugUI.I容器 value））
- `DebugUI.Flags get_flags()`
  （DebugUI.Flags get_flags（））
- `void set_flags(DebugUI.Flags value)`
  （void set_flags（DebugUI.Flags value））
- `string get_displayName()`
  （string get_display名称（））
- `void set_displayName(string value)`
  （void set_display名称（string value））
- `string get_queryPath()`
  （string get_query路径（））
- `void set_queryPath(string value)`
  （void set_query路径（string value））
- `bool get_isEditorOnly()`
  （bool get_isEditorOnly（））
- `bool get_isRuntimeOnly()`
  （bool get_isRuntimeOnly（））
- `bool get_isInactiveInEditor()`
  （bool get_isInactiveInEditor（））
- `void GenerateQueryPath()`
  （void GenerateQuery路径（））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## DebugUIHandlerBitField（Debug界面处理器BitField）

**继承**: DebugUIHandlerWidget（调试界面处理器控件）

### 字段 (5)

- `Text nameLabel`（文本 名称标签）(偏移: 0x3C)
- `UIFoldout valueToggle`（UI折叠值开关）(偏移: 0x40)
- `List<DebugUIHandlerIndirectToggle> toggles`（List<Debug界面处理器IndirectToggle> toggles）(偏移: 0x44)
- `DebugUI.BitField m_Field`（DebugUI.BitField m_Field）(偏移: 0x48)
- `DebugUIHandlerContainer m_Container`（Debug界面处理器容器 m_容器）(偏移: 0x4C)

### 方法 (9)

- `void SetWidget(DebugUI.Widget widget)`
  （void 设置控件（DebugUI.控件 widget））
- `bool GetValue(int index)`
  （bool 获取值（int index））
- `void SetValue(int index, bool value)`
  （void 集合值（int index, bool value））
- `bool OnSelection(bool fromNext, DebugUIHandlerWidget previous)`
  （布尔值 选中时（布尔值 来自下一个, 调试界面处理器控件 previous））
- `void OnDeselection()`
  （void 取消选中时（））
- `void OnIncrement(bool fast)`
  （void 递增时（布尔值 快速））
- `void OnDecrement(bool fast)`
  （void 递减时（布尔值 快速））
- `void OnAction()`
  （void 动作时（））
- `DebugUIHandlerWidget Next()`
  （调试界面处理器控件 下一个（））

---

## DebugUIHandlerButton（Debug界面处理器按钮）

**继承**: DebugUIHandlerWidget（调试界面处理器控件）

### 字段 (2)

- `Text nameLabel`（文本 名称标签）(偏移: 0x3C)
- `DebugUI.Button m_Field`（DebugUI.按钮 m_Field）(偏移: 0x40)

### 方法 (4)

- `void SetWidget(DebugUI.Widget widget)`
  （void 设置控件（DebugUI.控件 widget））
- `bool OnSelection(bool fromNext, DebugUIHandlerWidget previous)`
  （布尔值 选中时（布尔值 来自下一个, 调试界面处理器控件 previous））
- `void OnDeselection()`
  （void 取消选中时（））
- `void OnAction()`
  （void 动作时（））

---

## DebugUIHandlerCanvas（Debug界面处理器画布）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (7)

- `int m_DebugTreeState`（int m_DebugTree状态）(偏移: 0xC)
- `Transform panelPrefab`（变换 panel预制体）(偏移: 0x14)
- `List<DebugUIPrefabBundle> prefabs`（List<Debug界面预制体Bundle> prefabs）(偏移: 0x18)
- `List<DebugUIHandlerPanel> m_UIPanels`（List<Debug界面处理器Panel> m_UIPanels）(偏移: 0x1C)
- `int m_SelectedPanel`（int m_选中的面板）(偏移: 0x20)
- `DebugUIHandlerWidget m_SelectedWidget`（Debug界面处理器Widget m_选中的Widget）(偏移: 0x24)
- `string m_CurrentQueryPath`（string m_当前Query路径）(偏移: 0x28)

### 方法 (13)

- `void OnEnable()`
  （void 启用时（））
- `void Update()`
  （void 更新（））
- `void ResetAllHierarchy()`
  （void 重置所有Hierarchy（））
- `void Rebuild()`
  （void Rebuild（））
- `void Traverse(DebugUI.IContainer container, Transform parentTransform, DebugUIHandlerWidget parentUIHandler)`
  （void Traverse（DebugUI.I容器 container, 变换 parentTransform, Debug界面处理器Widget parentUIHandler））
- `DebugUIHandlerWidget GetWidgetFromPath(string queryPath)`
  （Debug界面处理器Widget 获取WidgetFrom路径（string queryPath））
- `void ActivatePanel(int index, bool tryAndKeepSelection = False)`
  （void 激活面板（int index, bool tryAndKeepSelection = False））
- `void ChangeSelection(DebugUIHandlerWidget widget, bool fromNext)`
  （void ChangeSelection（Debug界面处理器Widget widget, bool fromNext））
- `void SelectPreviousItem()`
  （void 选择上一个项目（））
- `void SelectNextItem()`
  （void 选择下一个项目（））
- `void ChangeSelectionValue(float multiplier)`
  （void ChangeSelection值（float multiplier））
- `void ActivateSelection()`
  （void 激活Selection（））
- `void HandleInput()`
  （void 句柄输入（））

---

## DebugUIHandlerColor（Debug界面处理器颜色）

**继承**: DebugUIHandlerWidget（调试界面处理器控件）

### 字段 (9)

- `Text nameLabel`（文本 名称标签）(偏移: 0x3C)
- `UIFoldout valueToggle`（UI折叠值开关）(偏移: 0x40)
- `Image colorImage`（图像 color图像）(偏移: 0x44)
- `DebugUIHandlerIndirectFloatField fieldR`（Debug界面处理器Indirect浮点数Field fieldR）(偏移: 0x48)
- `DebugUIHandlerIndirectFloatField fieldG`（Debug界面处理器Indirect浮点数Field fieldG）(偏移: 0x4C)
- `DebugUIHandlerIndirectFloatField fieldB`（Debug界面处理器Indirect浮点数Field fieldB）(偏移: 0x50)
- `DebugUIHandlerIndirectFloatField fieldA`（Debug界面处理器Indirect浮点数Field fieldA）(偏移: 0x54)
- `DebugUI.ColorField m_Field`（DebugUI.颜色Field m_Field）(偏移: 0x58)
- `DebugUIHandlerContainer m_Container`（Debug界面处理器容器 m_容器）(偏移: 0x5C)

### 方法 (10)

- `void SetWidget(DebugUI.Widget widget)`
  （void 设置控件（DebugUI.控件 widget））
- `void SetValue(float x, bool r = False, bool g = False, bool b = False, bool a = False)`
  （void 集合值（float x, bool r = False, bool g = False, bool b = False, bool a = False））
- `void SetupSettings(DebugUIHandlerIndirectFloatField field)`
  （void SetupSettings（Debug界面处理器Indirect浮点数Field field））
- `bool OnSelection(bool fromNext, DebugUIHandlerWidget previous)`
  （布尔值 选中时（布尔值 来自下一个, 调试界面处理器控件 previous））
- `void OnDeselection()`
  （void 取消选中时（））
- `void OnIncrement(bool fast)`
  （void 递增时（布尔值 快速））
- `void OnDecrement(bool fast)`
  （void 递减时（布尔值 快速））
- `void OnAction()`
  （void 动作时（））
- `void UpdateColor()`
  （void 更新颜色（））
- `DebugUIHandlerWidget Next()`
  （调试界面处理器控件 下一个（））

---

## DebugUIHandlerContainer（Debug界面处理器容器）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (1)

- `RectTransform contentHolder`（Rect变换 contentHolder）(偏移: 0xC)

### 方法 (4)

- `DebugUIHandlerWidget GetFirstItem()`
  （Debug界面处理器Widget 获取第一个项目（））
- `DebugUIHandlerWidget GetLastItem()`
  （Debug界面处理器Widget 获取最后一个项目（））
- `bool IsDirectChild(DebugUIHandlerWidget widget)`
  （bool 是否Direct子级（Debug界面处理器Widget widget））
- `List<DebugUIHandlerWidget> GetActiveChildren()`
  （List<Debug界面处理器Widget> 获取激活的Children（））

---

## DebugUIHandlerEnumField（Debug界面处理器EnumField）

**继承**: DebugUIHandlerWidget（调试界面处理器控件）

### 字段 (3)

- `Text nameLabel`（文本 名称标签）(偏移: 0x3C)
- `Text valueLabel`（文本 值标签）(偏移: 0x40)
- `DebugUI.EnumField m_Field`（DebugUI.EnumField m_Field）(偏移: 0x44)

### 方法 (7)

- `void SetWidget(DebugUI.Widget widget)`
  （void 设置控件（DebugUI.控件 widget））
- `bool OnSelection(bool fromNext, DebugUIHandlerWidget previous)`
  （布尔值 选中时（布尔值 来自下一个, 调试界面处理器控件 previous））
- `void OnDeselection()`
  （void 取消选中时（））
- `void OnAction()`
  （void 动作时（））
- `void OnIncrement(bool fast)`
  （void 递增时（布尔值 快速））
- `void OnDecrement(bool fast)`
  （void 递减时（布尔值 快速））
- `void UpdateValueLabel()`
  （void 更新值标签（））

---

## DebugUIHandlerEnumHistory（Debug界面处理器EnumHistory）

**继承**: DebugUIHandlerEnumField（Debug界面处理器EnumField）

### 字段 (1)

- `Text[] historyValues`（Text[] historyValues）(偏移: 0x48)

### 方法 (3)

- `void SetWidget(DebugUI.Widget widget)`
  （void 设置控件（DebugUI.控件 widget））
- `void UpdateValueLabel()`
  （void 更新值标签（））
- `IEnumerator RefreshAfterSanitization()`
  （IEnumerator 刷新AfterSanitization（））

---

## DebugUIHandlerFloatField（Debug界面处理器浮点数Field）

**继承**: DebugUIHandlerWidget（调试界面处理器控件）

### 字段 (3)

- `Text nameLabel`（文本 名称标签）(偏移: 0x3C)
- `Text valueLabel`（文本 值标签）(偏移: 0x40)
- `DebugUI.FloatField m_Field`（DebugUI.浮点数Field m_Field）(偏移: 0x44)

### 方法 (7)

- `void SetWidget(DebugUI.Widget widget)`
  （void 设置控件（DebugUI.控件 widget））
- `bool OnSelection(bool fromNext, DebugUIHandlerWidget previous)`
  （布尔值 选中时（布尔值 来自下一个, 调试界面处理器控件 previous））
- `void OnDeselection()`
  （void 取消选中时（））
- `void OnIncrement(bool fast)`
  （void 递增时（布尔值 快速））
- `void OnDecrement(bool fast)`
  （void 递减时（布尔值 快速））
- `void ChangeValue(bool fast, float multiplier)`
  （void Change值（bool fast, float multiplier））
- `void UpdateValueLabel()`
  （void 更新值标签（））

---

## DebugUIHandlerFoldout（Debug界面处理器Foldout）

**继承**: DebugUIHandlerWidget（调试界面处理器控件）

### 字段 (4)

- `Text nameLabel`（文本 名称标签）(偏移: 0x3C)
- `UIFoldout valueToggle`（UI折叠值开关）(偏移: 0x40)
- `DebugUI.Foldout m_Field`（DebugUI.Foldout m_Field）(偏移: 0x44)
- `DebugUIHandlerContainer m_Container`（Debug界面处理器容器 m_容器）(偏移: 0x48)

### 方法 (8)

- `void SetWidget(DebugUI.Widget widget)`
  （void 设置控件（DebugUI.控件 widget））
- `bool OnSelection(bool fromNext, DebugUIHandlerWidget previous)`
  （布尔值 选中时（布尔值 来自下一个, 调试界面处理器控件 previous））
- `void OnDeselection()`
  （void 取消选中时（））
- `void OnIncrement(bool fast)`
  （void 递增时（布尔值 快速））
- `void OnDecrement(bool fast)`
  （void 递减时（布尔值 快速））
- `void OnAction()`
  （void 动作时（））
- `void UpdateValue()`
  （void 更新值（））
- `DebugUIHandlerWidget Next()`
  （调试界面处理器控件 下一个（））

---

## DebugUIHandlerGroup（Debug界面处理器组）

**继承**: DebugUIHandlerWidget（调试界面处理器控件）

### 字段 (4)

- `Text nameLabel`（文本 名称标签）(偏移: 0x3C)
- `Transform header`（变换 header）(偏移: 0x40)
- `DebugUI.Container m_Field`（DebugUI.容器 m_Field）(偏移: 0x44)
- `DebugUIHandlerContainer m_Container`（Debug界面处理器容器 m_容器）(偏移: 0x48)

### 方法 (3)

- `void SetWidget(DebugUI.Widget widget)`
  （void 设置控件（DebugUI.控件 widget））
- `bool OnSelection(bool fromNext, DebugUIHandlerWidget previous)`
  （布尔值 选中时（布尔值 来自下一个, 调试界面处理器控件 previous））
- `DebugUIHandlerWidget Next()`
  （调试界面处理器控件 下一个（））

---

## DebugUIHandlerHBox（Debug界面处理器HBox）

**继承**: DebugUIHandlerWidget（调试界面处理器控件）

### 字段 (1)

- `DebugUIHandlerContainer m_Container`（Debug界面处理器容器 m_容器）(偏移: 0x3C)

### 方法 (3)

- `void SetWidget(DebugUI.Widget widget)`
  （void 设置控件（DebugUI.控件 widget））
- `bool OnSelection(bool fromNext, DebugUIHandlerWidget previous)`
  （布尔值 选中时（布尔值 来自下一个, 调试界面处理器控件 previous））
- `DebugUIHandlerWidget Next()`
  （调试界面处理器控件 下一个（））

---

## DebugUIHandlerIndirectFloatField（Debug界面处理器Indirect浮点数Field）

**继承**: DebugUIHandlerWidget（调试界面处理器控件）

### 字段 (7)

- `Text nameLabel`（文本 名称标签）(偏移: 0x3C)
- `Text valueLabel`（文本 值标签）(偏移: 0x40)
- `Func<float> getter`（Func<float> getter）(偏移: 0x44)
- `Action<float> setter`（Action<float> setter）(偏移: 0x48)
- `Func<float> incStepGetter`（Func<float> incStepGetter）(偏移: 0x4C)
- `Func<float> incStepMultGetter`（Func<float> incStepMultGetter）(偏移: 0x50)
- `Func<float> decimalsGetter`（Func<float> decimalsGetter）(偏移: 0x54)

### 方法 (7)

- `void Init()`
  （void 初始化（））
- `bool OnSelection(bool fromNext, DebugUIHandlerWidget previous)`
  （布尔值 选中时（布尔值 来自下一个, 调试界面处理器控件 previous））
- `void OnDeselection()`
  （void 取消选中时（））
- `void OnIncrement(bool fast)`
  （void 递增时（布尔值 快速））
- `void OnDecrement(bool fast)`
  （void 递减时（布尔值 快速））
- `void ChangeValue(bool fast, float multiplier)`
  （void Change值（bool fast, float multiplier））
- `void UpdateValueLabel()`
  （void 更新值标签（））

---

## DebugUIHandlerIndirectToggle（Debug界面处理器Indirect开关）

**继承**: DebugUIHandlerWidget（调试界面处理器控件）

### 字段 (4)

- `Text nameLabel`（文本 名称标签）(偏移: 0x3C)
- `Toggle valueToggle`（开关 value开关）(偏移: 0x40)
- `Image checkmarkImage`（图像 checkmark图像）(偏移: 0x44)
- `int index`（整数 索引）(偏移: 0x50)

### 方法 (5)

- `void Init()`
  （void 初始化（））
- `bool OnSelection(bool fromNext, DebugUIHandlerWidget previous)`
  （布尔值 选中时（布尔值 来自下一个, 调试界面处理器控件 previous））
- `void OnDeselection()`
  （void 取消选中时（））
- `void OnAction()`
  （void 动作时（））
- `void UpdateValueLabel()`
  （void 更新值标签（））

---

## DebugUIHandlerIntField（Debug界面处理器整数Field）

**继承**: DebugUIHandlerWidget（调试界面处理器控件）

### 字段 (3)

- `Text nameLabel`（文本 名称标签）(偏移: 0x3C)
- `Text valueLabel`（文本 值标签）(偏移: 0x40)
- `DebugUI.IntField m_Field`（DebugUI.整数Field m_Field）(偏移: 0x44)

### 方法 (7)

- `void SetWidget(DebugUI.Widget widget)`
  （void 设置控件（DebugUI.控件 widget））
- `bool OnSelection(bool fromNext, DebugUIHandlerWidget previous)`
  （布尔值 选中时（布尔值 来自下一个, 调试界面处理器控件 previous））
- `void OnDeselection()`
  （void 取消选中时（））
- `void OnIncrement(bool fast)`
  （void 递增时（布尔值 快速））
- `void OnDecrement(bool fast)`
  （void 递减时（布尔值 快速））
- `void ChangeValue(bool fast, int multiplier)`
  （void Change值（bool fast, int multiplier））
- `void UpdateValueLabel()`
  （void 更新值标签（））

---

## DebugUIHandlerPanel（Debug界面处理器面板）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (7)

- `Text nameLabel`（文本 名称标签）(偏移: 0xC)
- `ScrollRect scrollRect`（滚动Rect scrollRect）(偏移: 0x10)
- `RectTransform viewport`（Rect变换 viewport）(偏移: 0x14)
- `RectTransform m_ScrollTransform`（Rect变换 m_滚动变换）(偏移: 0x18)
- `RectTransform m_ContentTransform`（Rect变换 m_Content变换）(偏移: 0x1C)
- `RectTransform m_MaskTransform`（Rect变换 m_掩码变换）(偏移: 0x20)
- `DebugUI.Panel m_Panel`（DebugUI.面板 m_面板）(偏移: 0x24)

### 方法 (6)

- `void OnEnable()`
  （void 启用时（））
- `void SetPanel(DebugUI.Panel panel)`
  （void 集合面板（DebugUI.面板 panel））
- `DebugUI.Panel GetPanel()`
  （DebugUI.面板 获取面板（））
- `void ScrollTo(DebugUIHandlerWidget target)`
  （void 滚动To（Debug界面处理器Widget target））
- `float GetYPosInScroll(RectTransform target)`
  （float 获取YPosIn滚动（Rect变换 target））
- `DebugUIHandlerWidget GetFirstItem()`
  （Debug界面处理器Widget 获取第一个项目（））

---

## DebugUIHandlerPersistentCanvas（Debug界面处理器持久的画布）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (3)

- `RectTransform panel`（Rect变换 panel）(偏移: 0xC)
- `RectTransform valuePrefab`（Rect变换 value预制体）(偏移: 0x10)
- `List<DebugUIHandlerValue> m_Items`（List<Debug界面处理器Value> m_Items）(偏移: 0x14)

### 方法 (2)

- `void Toggle(DebugUI.Value widget)`
  （void 开关（DebugUI.值 widget））
- `void Clear()`
  （void 清除（））

---

## DebugUIHandlerRow（Debug界面处理器Row）

**继承**: DebugUIHandlerFoldout（Debug界面处理器Foldout）

### 字段 (1)

- `float m_Timer`（float m_计时器）(偏移: 0x4C)

### 方法 (2)

- `void OnEnable()`
  （void 启用时（））
- `void Update()`
  （void 更新（））

---

## DebugUIHandlerToggle（Debug界面处理器开关）

**继承**: DebugUIHandlerWidget（调试界面处理器控件）

### 字段 (4)

- `Text nameLabel`（文本 名称标签）(偏移: 0x3C)
- `Toggle valueToggle`（开关 value开关）(偏移: 0x40)
- `Image checkmarkImage`（图像 checkmark图像）(偏移: 0x44)
- `DebugUI.BoolField m_Field`（DebugUI.布尔值Field m_Field）(偏移: 0x48)

### 方法 (5)

- `void SetWidget(DebugUI.Widget widget)`
  （void 设置控件（DebugUI.控件 widget））
- `bool OnSelection(bool fromNext, DebugUIHandlerWidget previous)`
  （布尔值 选中时（布尔值 来自下一个, 调试界面处理器控件 previous））
- `void OnDeselection()`
  （void 取消选中时（））
- `void OnAction()`
  （void 动作时（））
- `void UpdateValueLabel()`
  （void 更新值标签（））

---

## DebugUIHandlerToggleHistory（Debug界面处理器开关History）

**继承**: DebugUIHandlerToggle（Debug界面处理器开关）

### 字段 (1)

- `Toggle[] historyToggles`（Toggle[] historyToggles）(偏移: 0x4C)

### 方法 (3)

- `void SetWidget(DebugUI.Widget widget)`
  （void 设置控件（DebugUI.控件 widget））
- `void UpdateValueLabel()`
  （void 更新值标签（））
- `IEnumerator RefreshAfterSanitization()`
  （IEnumerator 刷新AfterSanitization（））

---

## DebugUIHandlerUIntField（Debug界面处理器U整数Field）

**继承**: DebugUIHandlerWidget（调试界面处理器控件）

### 字段 (3)

- `Text nameLabel`（文本 名称标签）(偏移: 0x3C)
- `Text valueLabel`（文本 值标签）(偏移: 0x40)
- `DebugUI.UIntField m_Field`（DebugUI.U整数Field m_Field）(偏移: 0x44)

### 方法 (7)

- `void SetWidget(DebugUI.Widget widget)`
  （void 设置控件（DebugUI.控件 widget））
- `bool OnSelection(bool fromNext, DebugUIHandlerWidget previous)`
  （布尔值 选中时（布尔值 来自下一个, 调试界面处理器控件 previous））
- `void OnDeselection()`
  （void 取消选中时（））
- `void OnIncrement(bool fast)`
  （void 递增时（布尔值 快速））
- `void OnDecrement(bool fast)`
  （void 递减时（布尔值 快速））
- `void ChangeValue(bool fast, int multiplier)`
  （void Change值（bool fast, int multiplier））
- `void UpdateValueLabel()`
  （void 更新值标签（））

---

## DebugUIHandlerVBox（Debug界面处理器VBox）

**继承**: DebugUIHandlerWidget（调试界面处理器控件）

### 字段 (1)

- `DebugUIHandlerContainer m_Container`（Debug界面处理器容器 m_容器）(偏移: 0x3C)

### 方法 (3)

- `void SetWidget(DebugUI.Widget widget)`
  （void 设置控件（DebugUI.控件 widget））
- `bool OnSelection(bool fromNext, DebugUIHandlerWidget previous)`
  （布尔值 选中时（布尔值 来自下一个, 调试界面处理器控件 previous））
- `DebugUIHandlerWidget Next()`
  （调试界面处理器控件 下一个（））

---

## DebugUIHandlerValue（Debug界面处理器值）

**继承**: DebugUIHandlerWidget（调试界面处理器控件）

### 字段 (4)

- `Text nameLabel`（文本 名称标签）(偏移: 0x3C)
- `Text valueLabel`（文本 值标签）(偏移: 0x40)
- `DebugUI.Value m_Field`（DebugUI.值 m_Field）(偏移: 0x44)
- `float m_Timer`（float m_计时器）(偏移: 0x48)

### 方法 (5)

- `void OnEnable()`
  （void 启用时（））
- `void SetWidget(DebugUI.Widget widget)`
  （void 设置控件（DebugUI.控件 widget））
- `bool OnSelection(bool fromNext, DebugUIHandlerWidget previous)`
  （布尔值 选中时（布尔值 来自下一个, 调试界面处理器控件 previous））
- `void OnDeselection()`
  （void 取消选中时（））
- `void Update()`
  （void 更新（））

---

## DebugUIHandlerVector2（Debug界面处理器二维向量）

**继承**: DebugUIHandlerWidget（调试界面处理器控件）

### 字段 (6)

- `Text nameLabel`（文本 名称标签）(偏移: 0x3C)
- `UIFoldout valueToggle`（UI折叠值开关）(偏移: 0x40)
- `DebugUIHandlerIndirectFloatField fieldX`（Debug界面处理器Indirect浮点数Field fieldX）(偏移: 0x44)
- `DebugUIHandlerIndirectFloatField fieldY`（Debug界面处理器Indirect浮点数Field fieldY）(偏移: 0x48)
- `DebugUI.Vector2Field m_Field`（DebugUI.二维向量Field m_Field）(偏移: 0x4C)
- `DebugUIHandlerContainer m_Container`（Debug界面处理器容器 m_容器）(偏移: 0x50)

### 方法 (9)

- `void SetWidget(DebugUI.Widget widget)`
  （void 设置控件（DebugUI.控件 widget））
- `void SetValue(float v, bool x = False, bool y = False)`
  （void 集合值（float v, bool x = False, bool y = False））
- `void SetupSettings(DebugUIHandlerIndirectFloatField field)`
  （void SetupSettings（Debug界面处理器Indirect浮点数Field field））
- `bool OnSelection(bool fromNext, DebugUIHandlerWidget previous)`
  （布尔值 选中时（布尔值 来自下一个, 调试界面处理器控件 previous））
- `void OnDeselection()`
  （void 取消选中时（））
- `void OnIncrement(bool fast)`
  （void 递增时（布尔值 快速））
- `void OnDecrement(bool fast)`
  （void 递减时（布尔值 快速））
- `void OnAction()`
  （void 动作时（））
- `DebugUIHandlerWidget Next()`
  （调试界面处理器控件 下一个（））

---

## DebugUIHandlerVector3（Debug界面处理器三维向量）

**继承**: DebugUIHandlerWidget（调试界面处理器控件）

### 字段 (7)

- `Text nameLabel`（文本 名称标签）(偏移: 0x3C)
- `UIFoldout valueToggle`（UI折叠值开关）(偏移: 0x40)
- `DebugUIHandlerIndirectFloatField fieldX`（Debug界面处理器Indirect浮点数Field fieldX）(偏移: 0x44)
- `DebugUIHandlerIndirectFloatField fieldY`（Debug界面处理器Indirect浮点数Field fieldY）(偏移: 0x48)
- `DebugUIHandlerIndirectFloatField fieldZ`（Debug界面处理器Indirect浮点数Field fieldZ）(偏移: 0x4C)
- `DebugUI.Vector3Field m_Field`（DebugUI.三维向量Field m_Field）(偏移: 0x50)
- `DebugUIHandlerContainer m_Container`（Debug界面处理器容器 m_容器）(偏移: 0x54)

### 方法 (9)

- `void SetWidget(DebugUI.Widget widget)`
  （void 设置控件（DebugUI.控件 widget））
- `void SetValue(float v, bool x = False, bool y = False, bool z = False)`
  （void 集合值（float v, bool x = False, bool y = False, bool z = False））
- `void SetupSettings(DebugUIHandlerIndirectFloatField field)`
  （void SetupSettings（Debug界面处理器Indirect浮点数Field field））
- `bool OnSelection(bool fromNext, DebugUIHandlerWidget previous)`
  （布尔值 选中时（布尔值 来自下一个, 调试界面处理器控件 previous））
- `void OnDeselection()`
  （void 取消选中时（））
- `void OnIncrement(bool fast)`
  （void 递增时（布尔值 快速））
- `void OnDecrement(bool fast)`
  （void 递减时（布尔值 快速））
- `void OnAction()`
  （void 动作时（））
- `DebugUIHandlerWidget Next()`
  （调试界面处理器控件 下一个（））

---

## DebugUIHandlerVector4（Debug界面处理器Vector4）

**继承**: DebugUIHandlerWidget（调试界面处理器控件）

### 字段 (8)

- `Text nameLabel`（文本 名称标签）(偏移: 0x3C)
- `UIFoldout valueToggle`（UI折叠值开关）(偏移: 0x40)
- `DebugUIHandlerIndirectFloatField fieldX`（Debug界面处理器Indirect浮点数Field fieldX）(偏移: 0x44)
- `DebugUIHandlerIndirectFloatField fieldY`（Debug界面处理器Indirect浮点数Field fieldY）(偏移: 0x48)
- `DebugUIHandlerIndirectFloatField fieldZ`（Debug界面处理器Indirect浮点数Field fieldZ）(偏移: 0x4C)
- `DebugUIHandlerIndirectFloatField fieldW`（Debug界面处理器Indirect浮点数Field fieldW）(偏移: 0x50)
- `DebugUI.Vector4Field m_Field`（DebugUI.Vector4Field m_Field）(偏移: 0x54)
- `DebugUIHandlerContainer m_Container`（Debug界面处理器容器 m_容器）(偏移: 0x58)

### 方法 (9)

- `void SetWidget(DebugUI.Widget widget)`
  （void 设置控件（DebugUI.控件 widget））
- `void SetValue(float v, bool x = False, bool y = False, bool z = False, bool w = False)`
  （void 集合值（float v, bool x = False, bool y = False, bool z = False, bool w = False））
- `void SetupSettings(DebugUIHandlerIndirectFloatField field)`
  （void SetupSettings（Debug界面处理器Indirect浮点数Field field））
- `bool OnSelection(bool fromNext, DebugUIHandlerWidget previous)`
  （布尔值 选中时（布尔值 来自下一个, 调试界面处理器控件 previous））
- `void OnDeselection()`
  （void 取消选中时（））
- `void OnIncrement(bool fast)`
  （void 递增时（布尔值 快速））
- `void OnDecrement(bool fast)`
  （void 递减时（布尔值 快速））
- `void OnAction()`
  （void 动作时（））
- `DebugUIHandlerWidget Next()`
  （调试界面处理器控件 下一个（））

---

## DebugUIHandlerWidget（调试界面处理器控件）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (3)

- `Color colorDefault`（颜色 color默认的）(偏移: 0xC)
- `Color colorSelected`（颜色 color选中的）(偏移: 0x1C)
- `DebugUI.Widget m_Widget`（DebugUI.Widget m_Widget）(偏移: 0x38)

### 方法 (16)

- `DebugUIHandlerWidget get_parentUIHandler()`
  （Debug界面处理器Widget get_parent界面处理器（））
- `void set_parentUIHandler(DebugUIHandlerWidget value)`
  （void set_parent界面处理器（Debug界面处理器Widget value））
- `DebugUIHandlerWidget get_previousUIHandler()`
  （Debug界面处理器Widget get_previous界面处理器（））
- `void set_previousUIHandler(DebugUIHandlerWidget value)`
  （void set_previous界面处理器（Debug界面处理器Widget value））
- `DebugUIHandlerWidget get_nextUIHandler()`
  （Debug界面处理器Widget get_next界面处理器（））
- `void set_nextUIHandler(DebugUIHandlerWidget value)`
  （void set_next界面处理器（Debug界面处理器Widget value））
- `void OnEnable()`
  （void 启用时（））
- `void SetWidget(DebugUI.Widget widget)`
  （void 设置控件（DebugUI.控件 widget））
- `DebugUI.Widget GetWidget()`
  （DebugUI.Widget 获取Widget（））
- `bool OnSelection(bool fromNext, DebugUIHandlerWidget previous)`
  （布尔值 选中时（布尔值 来自下一个, 调试界面处理器控件 previous））
- `void OnDeselection()`
  （void 取消选中时（））
- `void OnAction()`
  （void 动作时（））
- `void OnIncrement(bool fast)`
  （void 递增时（布尔值 快速））
- `void OnDecrement(bool fast)`
  （void 递减时（布尔值 快速））
- `DebugUIHandlerWidget Previous()`
  （Debug界面处理器Widget 上一个（））
- `DebugUIHandlerWidget Next()`
  （调试界面处理器控件 下一个（））

---

## DebugUIPrefabBundle（Debug界面预制体捆绑包）

### 字段 (2)

- `string type`（string type）(偏移: 0x8)
- `RectTransform prefab`（Rect变换 prefab）(偏移: 0xC)

---

## DebugUpdater（DebugUpdater）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 方法 (2)

- `void RuntimeInit()`
  （void Runtime初始化（））
- `void Update()`
  （void 更新（））

---

## DebuggableAttribute（DebuggableAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `DebuggableAttribute.DebuggingModes m_debuggingModes`（DebuggableAttribute.DebuggingModes m_debuggingModes）(偏移: 0x8)

---

## DebuggableAttribute.DebuggingModes（DebuggableAttribute.DebuggingModes）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Debugger（Debugger）

### 字段 (1)

- `string DefaultCategory`（string 默认的类别）(偏移: 0x0)

### 方法 (4)

- `bool get_IsAttached()`
  （bool get_是否Attached（））
- `bool IsAttached_internal()`
  （bool 是否Attached_internal（））
- `void Log(int level, string category, string message)`
  （void Log（int level, string category, string message））
- `void NotifyOfCrossThreadDependency()`
  （void NotifyOfCrossThreadDependency（））

---

## Debugger（Debugger）

### 字段 (1)

- `int _logPriority`（int _logPriority）(偏移: 0x3133312A)

### 方法 (19)

- `int get_logPriority()`
  （int get_logPriority（））
- `void Log(object message)`
  （void Log（object message））
- `void LogWarning(object message, Tween t)`
  （void LogWarning（object message, Tween t））
- `void LogError(object message, Tween t)`
  （void LogError（object message, Tween t））
- `void LogSafeModeCapturedError(object message, Tween t)`
  （void LogSafe模式CapturedError（object message, Tween t））
- `void LogReport(object message)`
  （void LogReport（object message））
- `void LogSafeModeReport(object message)`
  （void LogSafe模式Report（object message））
- `void LogInvalidTween(Tween t)`
  （void LogInvalidTween（Tween t））
- `void LogNestedTween(Tween t)`
  （void LogNestedTween（Tween t））
- `void LogNullTween(Tween t)`
  （void LogNullTween（Tween t））
- `void LogNonPathTween(Tween t)`
  （void LogNon路径Tween（Tween t））
- `void LogMissingMaterialProperty(string propertyName)`
  （void LogMissing材质属性（string propertyName））
- `void LogMissingMaterialProperty(int propertyId)`
  （void LogMissing材质属性（int propertyId））
- `void LogRemoveActiveTweenError(string errorInfo, Tween t)`
  （void Log移除激活的TweenError（string errorInfo, Tween t））
- `void LogAddActiveTweenError(string errorInfo, Tween t)`
  （void Log添加激活的TweenError（string errorInfo, Tween t））
- `void SetLogPriority(LogBehaviour logBehaviour)`
  （void 集合LogPriority（LogBehaviour logBehaviour））
- `bool ShouldLogSafeModeCapturedError()`
  （bool 应该LogSafe模式CapturedError（））
- `string GetDebugDataMessage(Tween t)`
  （string 获取Debug数据Message（Tween t））
- `void AddDebugDataToMessage(ref string message, Tween t)`
  （void 添加Debug数据ToMessage（ref string message, Tween t））

---

## Debugger.Sequence（Debugger.Sequence）

### 方法 (6)

- `void LogAddToNullSequence()`
  （void Log添加ToNullSequence（））
- `void LogAddToInactiveSequence()`
  （void Log添加ToInactiveSequence（））
- `void LogAddToLockedSequence()`
  （void Log添加To锁定的Sequence（））
- `void LogAddNullTween()`
  （void Log添加NullTween（））
- `void LogAddInactiveTween(Tween t)`
  （void Log添加InactiveTween（Tween t））
- `void LogAddAlreadySequencedTween(Tween t)`
  （void Log添加AlreadySequencedTween（Tween t））

---

## DebuggerBrowsableAttribute（DebuggerBrowsableAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `DebuggerBrowsableState state`（DebuggerBrowsable状态 state）(偏移: 0x8)

---

## DebuggerBrowsableState（DebuggerBrowsable状态）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DebuggerDisplayAttribute（DebuggerDisplayAttribute）

**继承**: Attribute（属性）

### 字段 (3)

- `string name`（字符串 名称）(偏移: 0x8)
- `string value`（string value）(偏移: 0xC)
- `string type`（string type）(偏移: 0x10)

### 方法 (2)

- `void set_Name(string value)`
  （void 设置_名称（字符串 value））
- `void set_Type(string value)`
  （void set_类型（string value））

---

## DebuggerDisplayXmlNodeProxy（DebuggerDisplayXml节点代理）

### 字段 (1)

- `XmlNode node`（Xml节点 node）(偏移: 0x0)

### 方法 (1)

- `string ToString()`
  （字符串 转字符串（））

---

## DebuggerTypeProxyAttribute（Debugger类型代理Attribute）

**继承**: Attribute（属性）

### 字段 (1)

- `string typeName`（字符串 类型名称）(偏移: 0x8)

---

## Decimal（Decimal）

**继承**: IFormattable, IComparable, IConvertible, IDeserializationCallback, IComparable<Decimal>, IEquatable<Decimal>（IFormattable, IComparable, IConvertible, IDeserialization回调, IComparable<Decimal>, IEquatable<Decimal>）

### 字段 (12)

- `uint[] Powers10`（uint[] Powers10）(偏移: 0x0)
- `Decimal Zero`（Decimal Zero）(偏移: 0x4)
- `Decimal One`（Decimal One）(偏移: 0x14)
- `Decimal MinusOne`（Decimal MinusOne）(偏移: 0x24)
- `Decimal MaxValue`（Decimal 最大值）(偏移: 0x34)
- `Decimal MinValue`（Decimal 最小值）(偏移: 0x44)
- `Decimal NearNegativeZero`（Decimal NearNegativeZero）(偏移: 0x54)
- `Decimal NearPositiveZero`（Decimal NearPositiveZero）(偏移: 0x64)
- `int flags`（int flags）(偏移: 0x0)
- `int hi`（int hi）(偏移: 0x4)
- `int lo`（int lo）(偏移: 0x8)
- `int mid`（int mid）(偏移: 0xC)

### 方法 (52)

- `void SetBits(int[] bits)`
  （void 集合Bits（int[] bits））
- `void OnSerializing(StreamingContext ctx)`
  （void 序列化中（流上下文 ctx））
- `void FCallAddSub(ref Decimal d1, ref Decimal d2, byte bSign)`
  （void FCall添加子（ref Decimal d1, ref Decimal d2, byte bSign））
- `int FCallCompare(ref Decimal d1, ref Decimal d2)`
  （int FCallCompare（ref Decimal d1, ref Decimal d2））
- `int CompareTo(object value)`
  （整数 比较到（对象 value））
- `int CompareTo(Decimal value)`
  （int CompareTo（Decimal value））
- `bool Equals(object value)`
  （布尔值 等于（对象 value））
- `bool Equals(Decimal value)`
  （bool Equals（Decimal value））
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
- `Decimal Parse(string s, IFormatProvider provider)`
  （Decimal 解析（string s, I格式化提供者 provider））
- `Decimal Parse(string s, NumberStyles style, IFormatProvider provider)`
  （Decimal 解析（string s, NumberStyles style, I格式化提供者 provider））
- `bool TryParse(string s, out Decimal result)`
  （bool Try解析（string s, out Decimal result））
- `int[] GetBits(Decimal d)`
  （int[] 获取Bits（Decimal d））
- `Decimal ToDecimal(byte[] buffer)`
  （Decimal ToDecimal（byte[] buffer））
- `void FCallMultiply(ref Decimal d1, ref Decimal d2)`
  （void FCallMultiply（ref Decimal d1, ref Decimal d2））
- `Decimal Round(Decimal d, int decimals)`
  （Decimal 回合（Decimal d, int decimals））
- `void FCallRound(ref Decimal d, int decimals)`
  （void FCall回合（ref Decimal d, int decimals））
- `byte ToByte(Decimal value)`
  （byte ToByte（Decimal value））
- `sbyte ToSByte(Decimal value)`
  （sbyte ToSByte（Decimal value））
- `short ToInt16(Decimal value)`
  （short ToInt16（Decimal value））
- `double ToDouble(Decimal d)`
  （double ToDouble（Decimal d））
- `int FCallToInt32(Decimal d)`
  （int FCallToInt32（Decimal d））
- `int ToInt32(Decimal d)`
  （int ToInt32（Decimal d））
- `long ToInt64(Decimal d)`
  （long ToInt64（Decimal d））
- `ushort ToUInt16(Decimal value)`
  （ushort ToUInt16（Decimal value））
- `uint ToUInt32(Decimal d)`
  （uint ToUInt32（Decimal d））
- `ulong ToUInt64(Decimal d)`
  （ulong ToUInt64（Decimal d））
- `float ToSingle(Decimal d)`
  （float To单个（Decimal d））
- `void FCallTruncate(ref Decimal d)`
  （void FCallTruncate（ref Decimal d））
- `Decimal op_Implicit(byte value)`
  （Decimal op_Implicit（byte value））
- `Decimal op_Implicit(sbyte value)`
  （Decimal op_Implicit（sbyte value））
- `Decimal op_Implicit(short value)`
  （Decimal op_Implicit（short value））
- `Decimal op_Implicit(ushort value)`
  （Decimal op_Implicit（ushort value））
- `Decimal op_Implicit(int value)`
  （Decimal op_Implicit（int value））
- `Decimal op_Implicit(uint value)`
  （Decimal op_Implicit（uint value））
- `Decimal op_Implicit(long value)`
  （Decimal op_Implicit（long value））
- `Decimal op_Implicit(ulong value)`
  （Decimal op_Implicit（ulong value））
- `Decimal op_Explicit(float value)`
  （Decimal op_Explicit（float value））
- `Decimal op_Explicit(double value)`
  （Decimal op_Explicit（double value））
- `ulong op_Explicit(Decimal value)`
  （ulong op_Explicit（Decimal value））
- `float op_Explicit(Decimal value)`
  （float op_Explicit（Decimal value））
- `double op_Explicit(Decimal value)`
  （double op_Explicit（Decimal value））
- `Decimal op_Addition(Decimal d1, Decimal d2)`
  （Decimal op_Addition（Decimal d1, Decimal d2））
- `Decimal op_Subtraction(Decimal d1, Decimal d2)`
  （Decimal op_Subtraction（Decimal d1, Decimal d2））
- `Decimal op_Multiply(Decimal d1, Decimal d2)`
  （Decimal op_Multiply（Decimal d1, Decimal d2））
- `bool op_Equality(Decimal d1, Decimal d2)`
  （bool op_Equality（Decimal d1, Decimal d2））
- `bool op_Inequality(Decimal d1, Decimal d2)`
  （bool op_Inequality（Decimal d1, Decimal d2））
- `TypeCode GetTypeCode()`
  （类型代码 获取类型代码（））

---

## DecimalConstantAttribute（DecimalConstantAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `Decimal dec`（Decimal dec）(偏移: 0x8)

### 方法 (1)

- `Decimal get_Value()`
  （Decimal get_值（））

---

## DecimalConverter（DecimalConverter）

**继承**: BaseNumberConverter（基础数字转换器）

### 方法 (8)

- `bool get_AllowHex()`
  （布尔值 获取_允许十六进制（））
- `Type get_TargetType()`
  （类型 get_目标类型（））
- `bool CanConvertTo(ITypeDescriptorContext context, Type destinationType)`
  （布尔值 能否转换到（I类型描述符上下文 context, 类型 destinationType））
- `object ConvertTo(ITypeDescriptorContext context, CultureInfo culture, object value, Type destinationType)`
  （对象 转换到（I类型描述符上下文 context, 区域性信息 culture, 对象 value, 类型 destinationType））
- `object FromString(string value, int radix)`
  （对象 从字符串（字符串 value, 整数 radix））
- `object FromString(string value, NumberFormatInfo formatInfo)`
  （对象 从字符串（字符串 value, 数字格式信息 formatInfo））
- `object FromString(string value, CultureInfo culture)`
  （对象 从字符串（字符串 value, 区域性信息 culture））
- `string ToString(object value, NumberFormatInfo formatInfo)`
  （字符串 转字符串（对象 value, 数字格式信息 formatInfo））

---

## DecimalTypeInfo（Decimal类型信息）

**继承**: TraceLoggingTypeInfo<Decimal>（TraceLogging类型Info<Decimal>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void 写入元数据（跟踪日志元数据收集器 collector, 字符串 name, 事件字段格式 format））
- `void WriteData(TraceLoggingDataCollector collector, ref Decimal value)`
  （void Write数据（TraceLogging数据Collector collector, ref Decimal value））

---

## Decoder（Decoder）

### 字段 (2)

- `DecoderFallback m_fallback`（DecoderFallback m_fallback）(偏移: 0x8)
- `DecoderFallbackBuffer m_fallbackBuffer`（DecoderFallback缓冲区 m_fallback缓冲区）(偏移: 0xC)

### 方法 (9)

- `void SerializeDecoder(SerializationInfo info)`
  （void SerializeDecoder（Serialization信息 info））
- `DecoderFallback get_Fallback()`
  （DecoderFallback get_Fallback（））
- `DecoderFallbackBuffer get_FallbackBuffer()`
  （DecoderFallback缓冲区 get_Fallback缓冲区（））
- `bool get_InternalHasFallbackBuffer()`
  （bool get_内部的是否有Fallback缓冲区（））
- `void Reset()`
  （void 重置（））
- `int GetCharCount(byte[] bytes, int index, int count, bool flush)`
  （int 获取Char数量（byte[] bytes, int index, int count, bool flush））
- `int GetCharCount(byte* bytes, int count, bool flush)`
  （int 获取Char数量（byte* bytes, int count, bool flush））
- `int GetChars(byte[] bytes, int byteIndex, int byteCount, char[] chars, int charIndex, bool flush)`
  （int 获取Chars（byte[] bytes, int byteIndex, int byteCount, char[] chars, int charIndex, bool flush））
- `int GetChars(byte* bytes, int byteCount, char* chars, int charCount, bool flush)`
  （int 获取Chars（byte* bytes, int byteCount, char* chars, int charCount, bool flush））

---

## DecoderExceptionFallback（DecoderExceptionFallback）

**继承**: DecoderFallback（解码器回退）

### 方法 (4)

- `DecoderFallbackBuffer CreateFallbackBuffer()`
  （DecoderFallback缓冲区 创建Fallback缓冲区（））
- `int get_MaxCharCount()`
  （整数 获取_最大字符数量（））
- `bool Equals(object value)`
  （布尔值 等于（对象 value））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## DecoderExceptionFallbackBuffer（DecoderExceptionFallback缓冲区）

**继承**: DecoderFallbackBuffer（解码器回退缓冲区）

### 方法 (3)

- `bool Fallback(byte[] bytesUnknown, int index)`
  （bool Fallback（byte[] bytesUnknown, int index））
- `char GetNextChar()`
  （字符 获取下一个字符（））
- `void Throw(byte[] bytesUnknown, int index)`
  （void 投掷（byte[] bytesUnknown, int index））

---

## DecoderFallback（解码器回退）

### 字段 (4)

- `bool bIsMicrosoftBestFitFallback`（bool b是否MicrosoftBestFitFallback）(偏移: 0x8)
- `DecoderFallback replacementFallback`（DecoderFallback replacementFallback）(偏移: 0x0)
- `DecoderFallback exceptionFallback`（DecoderFallback exceptionFallback）(偏移: 0x4)
- `object s_InternalSyncObject`（对象 s_内部同步对象）(偏移: 0x8)

### 方法 (3)

- `object get_InternalSyncObject()`
  （对象 获取_内部同步对象（））
- `DecoderFallback get_ReplacementFallback()`
  （DecoderFallback get_ReplacementFallback（））
- `DecoderFallback get_ExceptionFallback()`
  （DecoderFallback get_ExceptionFallback（））

---

## DecoderFallbackBuffer（解码器回退缓冲区）

### 字段 (2)

- `byte* byteStart`（byte* byte开始）(偏移: 0x8)
- `char* charEnd`（char* char结束）(偏移: 0xC)

### 方法 (6)

- `void Reset()`
  （void 重置（））
- `void InternalReset()`
  （void 内部的重置（））
- `void InternalInitialize(byte* byteStart, char* charEnd)`
  （void 内部的初始化（byte* byteStart, char* charEnd））
- `bool InternalFallback(byte[] bytes, byte* pBytes, ref char* chars)`
  （bool 内部的Fallback（byte[] bytes, byte* pBytes, ref char* chars））
- `int InternalFallback(byte[] bytes, byte* pBytes)`
  （int 内部的Fallback（byte[] bytes, byte* pBytes））
- `void ThrowLastBytesRecursive(byte[] bytesUnknown)`
  （void 投掷最后一个BytesRecursive（byte[] bytesUnknown））

---

## DecoderFallbackException（DecoderFallbackException）

**继承**: ArgumentException（ArgumentException）

### 字段 (2)

- `byte[] bytesUnknown`（byte[] bytesUnknown）(偏移: 0x48)
- `int index`（整数 索引）(偏移: 0x4C)

---

## DecoderNLS（DecoderNLS）

**继承**: Decoder, ISerializable（Decoder, ISerializable）

### 字段 (4)

- `Encoding m_encoding`（Encoding m_encoding）(偏移: 0x10)
- `bool m_mustFlush`（bool m_mustFlush）(偏移: 0x14)
- `bool m_throwOnOverflow`（bool m_throwOnOverflow）(偏移: 0x15)
- `int m_bytesUsed`（int m_bytesUsed）(偏移: 0x18)

### 方法 (10)

- `void Reset()`
  （void 重置（））
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
- `bool get_MustFlush()`
  （bool get_MustFlush（））
- `bool get_HasState()`
  （布尔值 获取_是否有状态（））
- `void ClearMustFlush()`
  （void 清除MustFlush（））

---

## DecoderReplacementFallback（DecoderReplacementFallback）

**继承**: DecoderFallback（解码器回退）

### 字段 (1)

- `string strDefault`（string str默认的）(偏移: 0xC)

### 方法 (5)

- `string get_DefaultString()`
  （string get_默认的字符串（））
- `DecoderFallbackBuffer CreateFallbackBuffer()`
  （DecoderFallback缓冲区 创建Fallback缓冲区（））
- `int get_MaxCharCount()`
  （整数 获取_最大字符数量（））
- `bool Equals(object value)`
  （布尔值 等于（对象 value））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## DecoderReplacementFallbackBuffer（DecoderReplacementFallback缓冲区）

**继承**: DecoderFallbackBuffer（解码器回退缓冲区）

### 字段 (3)

- `string strDefault`（string str默认的）(偏移: 0x10)
- `int fallbackCount`（int fallback数量）(偏移: 0x14)
- `int fallbackIndex`（int fallback索引）(偏移: 0x18)

### 方法 (4)

- `bool Fallback(byte[] bytesUnknown, int index)`
  （bool Fallback（byte[] bytesUnknown, int index））
- `char GetNextChar()`
  （字符 获取下一个字符（））
- `void Reset()`
  （void 重置（））
- `int InternalFallback(byte[] bytes, byte* pBytes)`
  （int 内部的Fallback（byte[] bytes, byte* pBytes））

---

## DefaultBinder（默认的Binder）

**继承**: Binder（Binder）

### 方法 (20)

- `MethodBase BindToMethod(BindingFlags bindingAttr, MethodBase[] match, ref object[] args, ParameterModifier[] modifiers, CultureInfo cultureInfo, string[] names, out object state)`
  （Method基础 BindToMethod（BindingFlags bindingAttr, MethodBase[] match, ref object[] args, ParameterModifier[] modifiers, Culture信息 cultureInfo, string[] names, out object state））
- `FieldInfo BindToField(BindingFlags bindingAttr, FieldInfo[] match, object value, CultureInfo cultureInfo)`
  （Field信息 BindToField（BindingFlags bindingAttr, FieldInfo[] match, object value, Culture信息 cultureInfo））
- `MethodBase SelectMethod(BindingFlags bindingAttr, MethodBase[] match, Type[] types, ParameterModifier[] modifiers)`
  （Method基础 选择Method（BindingFlags bindingAttr, MethodBase[] match, Type[] types, ParameterModifier[] modifiers））
- `PropertyInfo SelectProperty(BindingFlags bindingAttr, PropertyInfo[] match, Type returnType, Type[] indexes, ParameterModifier[] modifiers)`
  （属性信息 选择属性（BindingFlags bindingAttr, 属性Info[] match, 类型 returnType, Type[] indexes, ParameterModifier[] modifiers））
- `object ChangeType(object value, Type type, CultureInfo cultureInfo)`
  （object Change类型（object value, 类型 type, Culture信息 cultureInfo））
- `void ReorderArgumentArray(ref object[] args, object state)`
  （void ReorderArgument数组（ref object[] args, object state））
- `MethodBase ExactBinding(MethodBase[] match, Type[] types, ParameterModifier[] modifiers)`
  （Method基础 ExactBinding（MethodBase[] match, Type[] types, ParameterModifier[] modifiers））
- `PropertyInfo ExactPropertyBinding(PropertyInfo[] match, Type returnType, Type[] types, ParameterModifier[] modifiers)`
  （属性信息 Exact属性Binding（属性Info[] match, 类型 returnType, Type[] types, ParameterModifier[] modifiers））
- `int FindMostSpecific(ParameterInfo[] p1, int[] paramOrder1, Type paramArrayType1, ParameterInfo[] p2, int[] paramOrder2, Type paramArrayType2, Type[] types, object[] args)`
  （int 查找MostSpecific（ParameterInfo[] p1, int[] paramOrder1, 类型 paramArrayType1, ParameterInfo[] p2, int[] paramOrder2, 类型 paramArrayType2, Type[] types, object[] args））
- `int FindMostSpecificType(Type c1, Type c2, Type t)`
  （int 查找MostSpecific类型（类型 c1, 类型 c2, 类型 t））
- `int FindMostSpecificMethod(MethodBase m1, int[] paramOrder1, Type paramArrayType1, MethodBase m2, int[] paramOrder2, Type paramArrayType2, Type[] types, object[] args)`
  （int 查找MostSpecificMethod（Method基础 m1, int[] paramOrder1, 类型 paramArrayType1, Method基础 m2, int[] paramOrder2, 类型 paramArrayType2, Type[] types, object[] args））
- `int FindMostSpecificField(FieldInfo cur1, FieldInfo cur2)`
  （int 查找MostSpecificField（Field信息 cur1, Field信息 cur2））
- `int FindMostSpecificProperty(PropertyInfo cur1, PropertyInfo cur2)`
  （int 查找MostSpecific属性（属性信息 cur1, 属性信息 cur2））
- `bool CompareMethodSigAndName(MethodBase m1, MethodBase m2)`
  （bool CompareMethodSigAnd名称（Method基础 m1, Method基础 m2））
- `int GetHierarchyDepth(Type t)`
  （int 获取Hierarchy深度（类型 t））
- `MethodBase FindMostDerivedNewSlotMeth(MethodBase[] match, int cMatches)`
  （Method基础 查找Most派生的新的槽位Meth（MethodBase[] match, int cMatches））
- `void ReorderParams(int[] paramOrder, object[] vars)`
  （void ReorderParams（int[] paramOrder, object[] vars））
- `bool CreateParamOrder(int[] paramOrder, ParameterInfo[] pars, string[] names)`
  （bool 创建ParamOrder（int[] paramOrder, ParameterInfo[] pars, string[] names））
- `bool CanConvertPrimitive(RuntimeType source, RuntimeType target)`
  （bool 能否转换Primitive（Runtime类型 source, Runtime类型 target））
- `bool CanConvertPrimitiveObjectToType(object source, RuntimeType type)`
  （bool 能否转换Primitive对象To类型（object source, Runtime类型 type））

---

## DefaultBinder.BinderState（默认的Binder.Binder状态）

### 字段 (3)

- `int[] m_argsMap`（int[] m_args映射）(偏移: 0x8)
- `int m_originalSize`（int m_original大小）(偏移: 0xC)
- `bool m_isParamArray`（bool m_isParam数组）(偏移: 0x10)

---

## DefaultControls（默认的Controls）

### 字段 (7)

- `DefaultControls.IFactoryControls m_CurrentFactory`（默认的Controls.I工厂Controls m_当前工厂）(偏移: 0x0)
- `Vector2 s_ThickElementSize`（二维向量 s_Thick元素大小）(偏移: 0x4)
- `Vector2 s_ThinElementSize`（二维向量 s_Thin元素大小）(偏移: 0xC)
- `Vector2 s_ImageElementSize`（二维向量 s_图像元素大小）(偏移: 0x14)
- `Color s_DefaultSelectableColor`（颜色 s_默认的Selectable颜色）(偏移: 0x1C)
- `Color s_PanelColor`（颜色 s_面板颜色）(偏移: 0x2C)
- `Color s_TextColor`（颜色 s_文本颜色）(偏移: 0x3C)

### 方法 (18)

- `DefaultControls.IFactoryControls get_factory()`
  （默认的Controls.I工厂Controls get_factory（））
- `GameObject CreateUIElementRoot(string name, Vector2 size, Type[] components)`
  （游戏对象 创建界面元素根（string name, 二维向量 size, Type[] components））
- `GameObject CreateUIObject(string name, GameObject parent, Type[] components)`
  （游戏对象 创建界面对象（string name, 游戏对象 parent, Type[] components））
- `void SetDefaultTextValues(Text lbl)`
  （void 集合默认的文本Values（文本 lbl））
- `void SetDefaultColorTransitionValues(Selectable slider)`
  （void 集合默认的颜色TransitionValues（Selectable slider））
- `void SetParentAndAlign(GameObject child, GameObject parent)`
  （void 集合父级AndAlign（游戏对象 child, 游戏对象 parent））
- `void SetLayerRecursively(GameObject go, int layer)`
  （void 集合层Recursively（游戏对象 go, int layer））
- `GameObject CreatePanel(DefaultControls.Resources resources)`
  （游戏对象 创建面板（默认的Controls.Resources resources））
- `GameObject CreateButton(DefaultControls.Resources resources)`
  （游戏对象 创建按钮（默认的Controls.Resources resources））
- `GameObject CreateText(DefaultControls.Resources resources)`
  （游戏对象 创建文本（默认的Controls.Resources resources））
- `GameObject CreateImage(DefaultControls.Resources resources)`
  （游戏对象 创建图像（默认的Controls.Resources resources））
- `GameObject CreateRawImage(DefaultControls.Resources resources)`
  （游戏对象 创建Raw图像（默认的Controls.Resources resources））
- `GameObject CreateSlider(DefaultControls.Resources resources)`
  （游戏对象 创建滑块（默认的Controls.Resources resources））
- `GameObject CreateScrollbar(DefaultControls.Resources resources)`
  （游戏对象 创建Scrollbar（默认的Controls.Resources resources））
- `GameObject CreateToggle(DefaultControls.Resources resources)`
  （游戏对象 创建开关（默认的Controls.Resources resources））
- `GameObject CreateInputField(DefaultControls.Resources resources)`
  （游戏对象 创建输入Field（默认的Controls.Resources resources））
- `GameObject CreateDropdown(DefaultControls.Resources resources)`
  （游戏对象 创建Dropdown（默认的Controls.Resources resources））
- `GameObject CreateScrollView(DefaultControls.Resources resources)`
  （游戏对象 创建滚动视图（默认的Controls.Resources resources））

---

## DefaultControls.DefaultRuntimeFactory（默认的Controls.默认的Runtime工厂）

**继承**: DefaultControls.IFactoryControls（默认的Controls.I工厂Controls）

### 字段 (1)

- `DefaultControls.IFactoryControls Default`（默认的Controls.I工厂Controls 默认的）(偏移: 0x0)

### 方法 (1)

- `GameObject CreateGameObject(string name, Type[] components)`
  （游戏对象 创建游戏对象（string name, Type[] components））

---

## DefaultControls.Resources（默认的Controls.Resources）

### 字段 (7)

- `Sprite standard`（精灵 standard）(偏移: 0x0)
- `Sprite background`（精灵 background）(偏移: 0x4)
- `Sprite inputField`（精灵 inputField）(偏移: 0x8)
- `Sprite knob`（精灵 knob）(偏移: 0xC)
- `Sprite checkmark`（精灵 checkmark）(偏移: 0x10)
- `Sprite dropdown`（精灵 dropdown）(偏移: 0x14)
- `Sprite mask`（精灵 mask）(偏移: 0x18)

---

## DefaultDependencyAttribute（默认的DependencyAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `LoadHint loadHint`（加载Hint loadHint）(偏移: 0x8)

---

## DefaultDllImportSearchPathsAttribute（默认的DllImport搜索PathsAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `DllImportSearchPath _paths`（DllImport搜索路径 _paths）(偏移: 0x8)

---

## DefaultEventAttribute（默认的事件Attribute）

**继承**: Attribute（属性）

### 字段 (2)

- `string name`（字符串 名称）(偏移: 0x8)
- `DefaultEventAttribute Default`（默认的事件Attribute 默认的）(偏移: 0x0)

### 方法 (3)

- `string get_Name()`
  （字符串 获取_名称（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## DefaultExecutionOrder（默认的ExecutionOrder）

**继承**: Attribute（属性）

### 字段 (1)

- `int m_Order`（int m_Order）(偏移: 0x8)

### 方法 (1)

- `int get_order()`
  （int get_order（））

---

## DefaultFormat（默认的格式化）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## DefaultITraversalProvider（默认的ITraversal提供者）

### 方法 (2)

- `bool CanTraverse(Path path, GraphNode node)`
  （bool 能否Traverse（路径 path, Graph节点 node））
- `uint GetTraversalCost(Path path, GraphNode node)`
  （uint 获取TraversalCost（路径 path, Graph节点 node））

---

