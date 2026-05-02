# 游戏类定义 (Part 18/21)

共 200 个类 (总序号 3401 - 3600)

---

## TimeSpanParse（时间Span解析）

### 字段 (1)

- `TimeSpanParse.TimeSpanToken zero`（时间SpanParse.时间Span令牌 zero）(偏移: 0x0)

### 方法 (9)

- `bool TryTimeToTicks(bool positive, TimeSpanParse.TimeSpanToken days, TimeSpanParse.TimeSpanToken hours, TimeSpanParse.TimeSpanToken minutes, TimeSpanParse.TimeSpanToken seconds, TimeSpanParse.TimeSpanToken fraction, out long result)`
  （bool Try时间ToTicks（bool positive, 时间SpanParse.时间Span令牌 days, 时间SpanParse.时间Span令牌 hours, 时间SpanParse.时间Span令牌 minutes, 时间SpanParse.时间Span令牌 seconds, 时间SpanParse.时间Span令牌 fraction, out long result））
- `TimeSpan Parse(string input, IFormatProvider formatProvider)`
  （时间Span 解析（string input, I格式化提供者 formatProvider））
- `bool TryParseTimeSpan(string input, TimeSpanParse.TimeSpanStandardStyles style, IFormatProvider formatProvider, ref TimeSpanParse.TimeSpanResult result)`
  （bool Try解析时间Span（string input, 时间SpanParse.时间SpanStandardStyles style, I格式化提供者 formatProvider, ref TimeSpanParse.TimeSpanResult result））
- `bool ProcessTerminalState(ref TimeSpanParse.TimeSpanRawInfo raw, TimeSpanParse.TimeSpanStandardStyles style, ref TimeSpanParse.TimeSpanResult result)`
  （bool 处理Terminal状态（ref TimeSpanParse.TimeSpanRawInfo raw, 时间SpanParse.时间SpanStandardStyles style, ref TimeSpanParse.TimeSpanResult result））
- `bool ProcessTerminal_DHMSF(ref TimeSpanParse.TimeSpanRawInfo raw, TimeSpanParse.TimeSpanStandardStyles style, ref TimeSpanParse.TimeSpanResult result)`
  （bool 处理Terminal_DHMSF（ref TimeSpanParse.TimeSpanRawInfo raw, 时间SpanParse.时间SpanStandardStyles style, ref TimeSpanParse.TimeSpanResult result））
- `bool ProcessTerminal_HMS_F_D(ref TimeSpanParse.TimeSpanRawInfo raw, TimeSpanParse.TimeSpanStandardStyles style, ref TimeSpanParse.TimeSpanResult result)`
  （bool 处理Terminal_HMS_F_D（ref TimeSpanParse.TimeSpanRawInfo raw, 时间SpanParse.时间SpanStandardStyles style, ref TimeSpanParse.TimeSpanResult result））
- `bool ProcessTerminal_HM_S_D(ref TimeSpanParse.TimeSpanRawInfo raw, TimeSpanParse.TimeSpanStandardStyles style, ref TimeSpanParse.TimeSpanResult result)`
  （bool 处理Terminal_HM_S_D（ref TimeSpanParse.TimeSpanRawInfo raw, 时间SpanParse.时间SpanStandardStyles style, ref TimeSpanParse.TimeSpanResult result））
- `bool ProcessTerminal_HM(ref TimeSpanParse.TimeSpanRawInfo raw, TimeSpanParse.TimeSpanStandardStyles style, ref TimeSpanParse.TimeSpanResult result)`
  （bool 处理Terminal_HM（ref TimeSpanParse.TimeSpanRawInfo raw, 时间SpanParse.时间SpanStandardStyles style, ref TimeSpanParse.TimeSpanResult result））
- `bool ProcessTerminal_D(ref TimeSpanParse.TimeSpanRawInfo raw, TimeSpanParse.TimeSpanStandardStyles style, ref TimeSpanParse.TimeSpanResult result)`
  （bool 处理Terminal_D（ref TimeSpanParse.TimeSpanRawInfo raw, 时间SpanParse.时间SpanStandardStyles style, ref TimeSpanParse.TimeSpanResult result））

---

## TimeSpanParse.ParseFailureKind（时间SpanParse.解析FailureKind）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TimeSpanParse.TTT（时间SpanParse.TTT）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TimeSpanParse.TimeSpanRawInfo（时间SpanParse.时间SpanRaw信息）

### 字段 (12)

- `TimeSpanParse.TTT lastSeenTTT`（时间SpanParse.TTT lastSeenTTT）(偏移: 0x0)
- `int tokenCount`（int token数量）(偏移: 0x4)
- `int SepCount`（int Sep数量）(偏移: 0x8)
- `int NumCount`（int Num数量）(偏移: 0xC)
- `string[] literals`（string[] literals）(偏移: 0x10)
- `TimeSpanParse.TimeSpanToken[] numbers`（时间SpanParse.时间SpanToken[] numbers）(偏移: 0x14)
- `TimeSpanFormat.FormatLiterals m_posLoc`（时间SpanFormat.格式化Literals m_posLoc）(偏移: 0x18)
- `TimeSpanFormat.FormatLiterals m_negLoc`（时间SpanFormat.格式化Literals m_negLoc）(偏移: 0x34)
- `bool m_posLocInit`（bool m_posLoc初始化）(偏移: 0x50)
- `bool m_negLocInit`（bool m_negLoc初始化）(偏移: 0x51)
- `string m_fullPosPattern`（string m_fullPosPattern）(偏移: 0x54)
- `string m_fullNegPattern`（string m_fullNegPattern）(偏移: 0x58)

### 方法 (17)

- `TimeSpanFormat.FormatLiterals get_PositiveInvariant()`
  （时间SpanFormat.格式化Literals get_PositiveInvariant（））
- `TimeSpanFormat.FormatLiterals get_NegativeInvariant()`
  （时间SpanFormat.格式化Literals get_NegativeInvariant（））
- `TimeSpanFormat.FormatLiterals get_PositiveLocalized()`
  （时间SpanFormat.格式化Literals get_PositiveLocalized（））
- `TimeSpanFormat.FormatLiterals get_NegativeLocalized()`
  （时间SpanFormat.格式化Literals get_NegativeLocalized（））
- `bool FullAppCompatMatch(TimeSpanFormat.FormatLiterals pattern)`
  （bool 满AppCompat比赛（时间SpanFormat.格式化Literals pattern））
- `bool PartialAppCompatMatch(TimeSpanFormat.FormatLiterals pattern)`
  （bool PartialAppCompat比赛（时间SpanFormat.格式化Literals pattern））
- `bool FullMatch(TimeSpanFormat.FormatLiterals pattern)`
  （bool 满比赛（时间SpanFormat.格式化Literals pattern））
- `bool FullDMatch(TimeSpanFormat.FormatLiterals pattern)`
  （bool 满D比赛（时间SpanFormat.格式化Literals pattern））
- `bool FullHMMatch(TimeSpanFormat.FormatLiterals pattern)`
  （bool 满HM比赛（时间SpanFormat.格式化Literals pattern））
- `bool FullDHMMatch(TimeSpanFormat.FormatLiterals pattern)`
  （bool 满DHM比赛（时间SpanFormat.格式化Literals pattern））
- `bool FullHMSMatch(TimeSpanFormat.FormatLiterals pattern)`
  （bool 满HMS比赛（时间SpanFormat.格式化Literals pattern））
- `bool FullDHMSMatch(TimeSpanFormat.FormatLiterals pattern)`
  （bool 满DHMS比赛（时间SpanFormat.格式化Literals pattern））
- `bool FullHMSFMatch(TimeSpanFormat.FormatLiterals pattern)`
  （bool 满HMSF比赛（时间SpanFormat.格式化Literals pattern））
- `void Init(DateTimeFormatInfo dtfi)`
  （void 初始化（Date时间格式化信息 dtfi））
- `bool ProcessToken(ref TimeSpanParse.TimeSpanToken tok, ref TimeSpanParse.TimeSpanResult result)`
  （bool 处理令牌（ref TimeSpanParse.TimeSpanToken tok, ref TimeSpanParse.TimeSpanResult result））
- `bool AddSep(string sep, ref TimeSpanParse.TimeSpanResult result)`
  （bool 添加Sep（string sep, ref TimeSpanParse.TimeSpanResult result））
- `bool AddNum(TimeSpanParse.TimeSpanToken num, ref TimeSpanParse.TimeSpanResult result)`
  （bool 添加Num（时间SpanParse.时间Span令牌 num, ref TimeSpanParse.TimeSpanResult result））

---

## TimeSpanParse.TimeSpanResult（时间SpanParse.时间SpanResult）

### 字段 (6)

- `TimeSpan parsedTimeSpan`（时间Span parsed时间Span）(偏移: 0x0)
- `TimeSpanParse.TimeSpanThrowStyle throwStyle`（时间SpanParse.时间Span投掷Style throwStyle）(偏移: 0x8)
- `TimeSpanParse.ParseFailureKind m_failure`（时间SpanParse.解析FailureKind m_failure）(偏移: 0xC)
- `string m_failureMessageID`（string m_failureMessageID）(偏移: 0x10)
- `object m_failureMessageFormatArgument`（object m_failureMessage格式化Argument）(偏移: 0x14)
- `string m_failureArgumentName`（string m_failureArgument名称）(偏移: 0x18)

### 方法 (5)

- `void Init(TimeSpanParse.TimeSpanThrowStyle canThrow)`
  （void 初始化（时间SpanParse.时间Span投掷Style canThrow））
- `void SetFailure(TimeSpanParse.ParseFailureKind failure, string failureMessageID)`
  （void 集合Failure（时间SpanParse.解析FailureKind failure, string failureMessageID））
- `void SetFailure(TimeSpanParse.ParseFailureKind failure, string failureMessageID, object failureMessageFormatArgument)`
  （void 集合Failure（时间SpanParse.解析FailureKind failure, string failureMessageID, object failureMessageFormatArgument））
- `void SetFailure(TimeSpanParse.ParseFailureKind failure, string failureMessageID, object failureMessageFormatArgument, string failureArgumentName)`
  （void 集合Failure（时间SpanParse.解析FailureKind failure, string failureMessageID, object failureMessageFormatArgument, string failureArgumentName））
- `Exception GetTimeSpanParseException()`
  （Exception 获取时间Span解析Exception（））

---

## TimeSpanParse.TimeSpanStandardStyles（时间SpanParse.时间SpanStandardStyles）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TimeSpanParse.TimeSpanThrowStyle（时间SpanParse.时间Span投掷Style）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TimeSpanParse.TimeSpanToken（时间SpanParse.时间Span令牌）

### 字段 (4)

- `TimeSpanParse.TTT ttt`（时间SpanParse.TTT ttt）(偏移: 0x0)
- `int num`（int num）(偏移: 0x4)
- `int zeroes`（int zeroes）(偏移: 0x8)
- `string sep`（string sep）(偏移: 0xC)

### 方法 (1)

- `bool IsInvalidNumber(int maxValue, int maxPrecision)`
  （bool 是否InvalidNumber（int maxValue, int maxPrecision））

---

## TimeSpanParse.TimeSpanTokenizer（时间SpanParse.时间SpanTokenizer）

### 字段 (2)

- `int m_pos`（int m_pos）(偏移: 0x0)
- `string m_value`（string m_value）(偏移: 0x4)

### 方法 (6)

- `void Init(string input)`
  （void 初始化（string input））
- `void Init(string input, int startPosition)`
  （void 初始化（string input, int startPosition））
- `TimeSpanParse.TimeSpanToken GetNextToken()`
  （时间SpanParse.时间Span令牌 获取下一个令牌（））
- `bool get_EOL()`
  （bool get_EOL（））
- `char get_NextChar()`
  （char get_下一个Char（））
- `char get_CurrentChar()`
  （char get_当前Char（））

---

## TimeSpanTypeInfo（时间Span类型信息）

**继承**: TraceLoggingTypeInfo<TimeSpan>（TraceLogging类型Info<时间Span>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void WriteMetadata（TraceLoggingMetadataCollector collector, string name, 事件Field格式化 format））
- `void WriteData(TraceLoggingDataCollector collector, ref TimeSpan value)`
  （void Write数据（TraceLogging数据Collector collector, ref TimeSpan value））

---

## TimeType（时间类型）

### 字段 (3)

- `int Offset`（int Offset）(偏移: 0x8)
- `bool IsDst`（bool 是否Dst）(偏移: 0xC)
- `string Name`（string 名称）(偏移: 0x10)

### 方法 (1)

- `string ToString()`
  （string To字符串（））

---

## TimeUtility（时间工具）

### 字段 (3)

- `double kTimeEpsilon`（double k时间Epsilon）(偏移: 0x0)
- `double kFrameRateEpsilon`（double kFrameRateEpsilon）(偏移: 0x8)
- `double k_MaxTimelineDurationInSeconds`（double k_最大Timeline持续时间InSeconds）(偏移: 0x10)

### 方法 (1)

- `double GetAnimationClipLength(AnimationClip clip)`
  （double 获取动画弹匣Length（动画弹匣 clip））

---

## TimeZone（时间Zone）

### 字段 (1)

- `object tz_lock`（object tz_lock）(偏移: 0x0)

---

## TimeZoneInfo（时间Zone信息）

**继承**: IEquatable<TimeZoneInfo>, ISerializable, IDeserializationCallback（IEquatable<时间ZoneInfo>, ISerializable, IDeserialization回调）

### 字段 (14)

- `TimeSpan baseUtcOffset`（时间Span baseUtcOffset）(偏移: 0x8)
- `string daylightDisplayName`（string daylightDisplay名称）(偏移: 0x10)
- `string displayName`（string display名称）(偏移: 0x14)
- `string id`（string id）(偏移: 0x18)
- `TimeZoneInfo local`（时间Zone信息 local）(偏移: 0x0)
- `bool readlinkNotFound`（bool readlinkNotFound）(偏移: 0x4)
- `string standardDisplayName`（string standardDisplay名称）(偏移: 0x20)
- `bool supportsDaylightSavingTime`（bool supportsDaylightSaving时间）(偏移: 0x24)
- `TimeZoneInfo utc`（时间Zone信息 utc）(偏移: 0x8)
- `string timeZoneDirectory`（string timeZoneDirectory）(偏移: 0xC)
- `TimeZoneInfo.AdjustmentRule[] adjustmentRules`（时间ZoneInfo.AdjustmentRule[] adjustmentRules）(偏移: 0x28)
- `RegistryKey timeZoneKey`（Registry键 timeZone键）(偏移: 0x10)
- `RegistryKey localZoneKey`（Registry键 localZone键）(偏移: 0x14)
- `ReadOnlyCollection<TimeZoneInfo> systemTimeZones`（ReadOnlyCollection<时间ZoneInfo> system时间Zones）(偏移: 0x18)

### 方法 (78)

- `bool UtcOffsetOutOfRange(TimeSpan offset)`
  （bool UtcOffsetOutOf范围（时间Span offset））
- `List<TimeZoneInfo.AdjustmentRule> CreateAdjustmentRule(int year, out long[] data, out string[] names, string standardNameCurrentYear, string daylightNameCurrentYear)`
  （List<时间ZoneInfo.AdjustmentRule> 创建AdjustmentRule（int year, out long[] data, out string[] names, string standardNameCurrentYear, string daylightNameCurrentYear））
- `TimeZoneInfo CreateLocalUnity()`
  （时间Zone信息 创建本地的Unity引擎（））
- `uint EnumDynamicTimeZoneInformation(uint dwIndex, out TimeZoneInfo.DYNAMIC_TIME_ZONE_INFORMATION lpTimeZoneInformation)`
  （uint Enum动态的时间ZoneInformation（uint dwIndex, out TimeZoneInfo.DYNAMIC_TIME_ZONE_INFORMATION lpTimeZoneInformation））
- `uint GetDynamicTimeZoneInformation(out TimeZoneInfo.DYNAMIC_TIME_ZONE_INFORMATION pTimeZoneInformation)`
  （uint 获取动态的时间ZoneInformation（out TimeZoneInfo.DYNAMIC_TIME_ZONE_INFORMATION pTimeZoneInformation））
- `uint GetDynamicTimeZoneInformationWin32(out TimeZoneInfo.DYNAMIC_TIME_ZONE_INFORMATION pTimeZoneInformation)`
  （uint 获取动态的时间ZoneInformationWin32（out TimeZoneInfo.DYNAMIC_TIME_ZONE_INFORMATION pTimeZoneInformation））
- `uint GetDynamicTimeZoneInformationEffectiveYears(ref TimeZoneInfo.DYNAMIC_TIME_ZONE_INFORMATION lpTimeZoneInformation, out uint FirstYear, out uint LastYear)`
  （uint 获取动态的时间ZoneInformationEffectiveYears（ref TimeZoneInfo.DYNAMIC_TIME_ZONE_INFORMATION lpTimeZoneInformation, out uint FirstYear, out uint LastYear））
- `bool GetTimeZoneInformationForYear(ushort wYear, ref TimeZoneInfo.DYNAMIC_TIME_ZONE_INFORMATION pdtzi, out TimeZoneInfo.TIME_ZONE_INFORMATION ptzi)`
  （bool 获取时间ZoneInformationForYear（ushort wYear, ref TimeZoneInfo.DYNAMIC_TIME_ZONE_INFORMATION pdtzi, out TimeZoneInfo.TIME_ZONE_INFORMATION ptzi））
- `TimeZoneInfo.AdjustmentRule CreateAdjustmentRuleFromTimeZoneInformation(ref TimeZoneInfo.DYNAMIC_TIME_ZONE_INFORMATION timeZoneInformation, DateTime startDate, DateTime endDate, int defaultBaseUtcOffset)`
  （时间ZoneInfo.AdjustmentRule 创建AdjustmentRuleFrom时间ZoneInformation（ref TimeZoneInfo.DYNAMIC_TIME_ZONE_INFORMATION timeZoneInformation, Date时间 startDate, Date时间 endDate, int defaultBaseUtcOffset））
- `bool TransitionTimeFromTimeZoneInformation(TimeZoneInfo.DYNAMIC_TIME_ZONE_INFORMATION timeZoneInformation, out TimeZoneInfo.TransitionTime transitionTime, bool readStartDate)`
  （bool Transition时间From时间ZoneInformation（时间ZoneInfo.DYNAMIC_TIME_ZONE_INFORMATION timeZoneInformation, out TimeZoneInfo.TransitionTime transitionTime, bool readStartDate））
- `TimeZoneInfo TryCreateTimeZone(TimeZoneInfo.DYNAMIC_TIME_ZONE_INFORMATION timeZoneInformation)`
  （时间Zone信息 Try创建时间Zone（时间ZoneInfo.DYNAMIC_TIME_ZONE_INFORMATION timeZoneInformation））
- `TimeZoneInfo GetLocalTimeZoneInfoWinRTFallback()`
  （时间Zone信息 获取本地的时间Zone信息WinRTFallback（））
- `string GetLocalTimeZoneKeyNameWin32Fallback()`
  （string 获取本地的时间Zone键名称Win32Fallback（））
- `TimeZoneInfo FindSystemTimeZoneByIdWinRTFallback(string id)`
  （时间Zone信息 查找系统时间ZoneByIdWinRTFallback（string id））
- `List<TimeZoneInfo> GetSystemTimeZonesWinRTFallback()`
  （List<时间ZoneInfo> 获取系统时间ZonesWinRTFallback（））
- `TimeSpan get_BaseUtcOffset()`
  （时间Span get_基础UtcOffset（））
- `string get_DisplayName()`
  （string get_Display名称（））
- `string get_Id()`
  （string get_Id（））
- `TimeZoneInfo get_Local()`
  （时间Zone信息 get_本地的（））
- `int readlink(string path, byte[] buffer, int buflen)`
  （int readlink（string path, byte[] buffer, int buflen））
- `string readlink(string path)`
  （string readlink（string path））
- `bool TryGetNameFromPath(string path, out string name)`
  （bool Try获取名称From路径（string path, out string name））
- `TimeZoneInfo CreateLocal()`
  （时间Zone信息 创建本地的（））
- `TimeZoneInfo FindSystemTimeZoneByIdCore(string id)`
  （时间Zone信息 查找系统时间ZoneByIdCore（string id））
- `void GetSystemTimeZonesCore(List<TimeZoneInfo> systemTimeZones)`
  （void 获取系统时间ZonesCore（List<时间ZoneInfo> systemTimeZones））
- `bool get_SupportsDaylightSavingTime()`
  （bool get_SupportsDaylightSaving时间（））
- `TimeZoneInfo get_Utc()`
  （时间Zone信息 get_Utc（））
- `string get_TimeZoneDirectory()`
  （string get_时间ZoneDirectory（））
- `bool get_IsWindows()`
  （bool get_是否Windows（））
- `string TrimSpecial(string str)`
  （string Trim特殊（string str））
- `RegistryKey get_TimeZoneKey()`
  （Registry键 get_时间Zone键（））
- `RegistryKey get_LocalZoneKey()`
  （Registry键 get_本地的Zone键（））
- `bool TryAddTicks(DateTime date, long ticks, out DateTime result, DateTimeKind kind = 0)`
  （bool Try添加Ticks（Date时间 date, long ticks, out DateTime result, Date时间Kind kind = 0））
- `DateTime ConvertTime(DateTime dateTime, TimeZoneInfo sourceTimeZone, TimeZoneInfo destinationTimeZone)`
  （Date时间 转换时间（Date时间 dateTime, 时间Zone信息 sourceTimeZone, 时间Zone信息 destinationTimeZone））
- `DateTime ConvertTimeFromUtc(DateTime dateTime)`
  （Date时间 转换时间FromUtc（Date时间 dateTime））
- `DateTime ConvertTimeFromUtc(DateTime dateTime, TimeZoneInfo destinationTimeZone)`
  （Date时间 转换时间FromUtc（Date时间 dateTime, 时间Zone信息 destinationTimeZone））
- `DateTime ConvertTimeToUtc(DateTime dateTime, TimeZoneInfoOptions flags)`
  （Date时间 转换时间ToUtc（Date时间 dateTime, 时间Zone信息Options flags））
- `DateTime ConvertTimeToUtc(DateTime dateTime, TimeZoneInfo sourceTimeZone)`
  （Date时间 转换时间ToUtc（Date时间 dateTime, 时间Zone信息 sourceTimeZone））
- `DateTime ConvertTimeToUtc(DateTime dateTime, TimeZoneInfo sourceTimeZone, TimeZoneInfoOptions flags)`
  （Date时间 转换时间ToUtc（Date时间 dateTime, 时间Zone信息 sourceTimeZone, 时间Zone信息Options flags））
- `TimeSpan GetDateTimeNowUtcOffsetFromUtc(DateTime time, out bool isAmbiguousLocalDst)`
  （时间Span 获取Date时间NowUtcOffsetFromUtc（Date时间 time, out bool isAmbiguousLocalDst））
- `TimeZoneInfo CreateCustomTimeZone(string id, TimeSpan baseUtcOffset, string displayName, string standardDisplayName)`
  （时间Zone信息 创建自定义的时间Zone（string id, 时间Span baseUtcOffset, string displayName, string standardDisplayName））
- `TimeZoneInfo CreateCustomTimeZone(string id, TimeSpan baseUtcOffset, string displayName, string standardDisplayName, string daylightDisplayName, TimeZoneInfo.AdjustmentRule[] adjustmentRules)`
  （时间Zone信息 创建自定义的时间Zone（string id, 时间Span baseUtcOffset, string displayName, string standardDisplayName, string daylightDisplayName, 时间ZoneInfo.AdjustmentRule[] adjustmentRules））
- `TimeZoneInfo CreateCustomTimeZone(string id, TimeSpan baseUtcOffset, string displayName, string standardDisplayName, string daylightDisplayName, TimeZoneInfo.AdjustmentRule[] adjustmentRules, bool disableDaylightSavingTime)`
  （时间Zone信息 创建自定义的时间Zone（string id, 时间Span baseUtcOffset, string displayName, string standardDisplayName, string daylightDisplayName, 时间ZoneInfo.AdjustmentRule[] adjustmentRules, bool disableDaylightSavingTime））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `bool Equals(TimeZoneInfo other)`
  （bool Equals（时间Zone信息 other））
- `TimeZoneInfo FindSystemTimeZoneById(string id)`
  （时间Zone信息 查找系统时间ZoneById（string id））
- `TimeZoneInfo FindSystemTimeZoneByFileName(string id, string filepath)`
  （时间Zone信息 查找系统时间ZoneBy文件名称（string id, string filepath））
- `TimeZoneInfo FromRegistryKey(string id, RegistryKey key)`
  （时间Zone信息 FromRegistry键（string id, Registry键 key））
- `void ParseRegTzi(List<TimeZoneInfo.AdjustmentRule> adjustmentRules, int start_year, int end_year, byte[] buffer)`
  （void 解析RegTzi（List<时间ZoneInfo.AdjustmentRule> adjustmentRules, int start_year, int end_year, byte[] buffer））
- `TimeZoneInfo.AdjustmentRule[] GetAdjustmentRules()`
  （时间ZoneInfo.AdjustmentRule[] 获取AdjustmentRules（））
- `int GetHashCode()`
  （int 获取HashCode（））
- `ReadOnlyCollection<TimeZoneInfo> GetSystemTimeZones()`
  （ReadOnlyCollection<时间ZoneInfo> 获取系统时间Zones（））
- `TimeSpan GetUtcOffset(DateTime dateTime)`
  （时间Span 获取UtcOffset（Date时间 dateTime））
- `TimeSpan GetUtcOffset(DateTime dateTime, out bool isDST, bool forOffset = False)`
  （时间Span 获取UtcOffset（Date时间 dateTime, out bool isDST, bool forOffset = False））
- `TimeSpan GetUtcOffsetHelper(DateTime dateTime, TimeZoneInfo tz, out bool isDST, bool forOffset = False)`
  （时间Span 获取UtcOffset辅助器（Date时间 dateTime, 时间Zone信息 tz, out bool isDST, bool forOffset = False））
- `bool HasSameRules(TimeZoneInfo other)`
  （bool 是否有SameRules（时间Zone信息 other））
- `bool IsAmbiguousTime(DateTime dateTime)`
  （bool 是否Ambiguous时间（Date时间 dateTime））
- `bool IsAmbiguousLocalDstFromUtc(DateTime dateTime)`
  （bool 是否Ambiguous本地的DstFromUtc（Date时间 dateTime））
- `bool IsInDST(TimeZoneInfo.AdjustmentRule rule, DateTime dateTime)`
  （bool 是否InDST（时间ZoneInfo.AdjustmentRule rule, Date时间 dateTime））
- `bool IsInDSTForYear(TimeZoneInfo.AdjustmentRule rule, DateTime dateTime, int year)`
  （bool 是否InDSTForYear（时间ZoneInfo.AdjustmentRule rule, Date时间 dateTime, int year））
- `bool IsDaylightSavingTime(DateTime dateTime)`
  （bool 是否DaylightSaving时间（Date时间 dateTime））
- `bool IsDaylightSavingTime(DateTime dateTime, TimeZoneInfoOptions flags)`
  （bool 是否DaylightSaving时间（Date时间 dateTime, 时间Zone信息Options flags））
- `bool IsInvalidTime(DateTime dateTime)`
  （bool 是否Invalid时间（Date时间 dateTime））
- `void Validate(string id, TimeSpan baseUtcOffset, TimeZoneInfo.AdjustmentRule[] adjustmentRules)`
  （void 验证（string id, 时间Span baseUtcOffset, 时间ZoneInfo.AdjustmentRule[] adjustmentRules））
- `string ToString()`
  （string To字符串（））
- `TimeZoneInfo.AdjustmentRule GetApplicableRule(DateTime dateTime)`
  （时间ZoneInfo.AdjustmentRule 获取ApplicableRule（Date时间 dateTime））
- `bool TryGetTransitionOffset(DateTime dateTime, out TimeSpan offset, out bool isDst, bool forOffset = False)`
  （bool Try获取TransitionOffset（Date时间 dateTime, out TimeSpan offset, out bool isDst, bool forOffset = False））
- `DateTime TransitionPoint(TimeZoneInfo.TransitionTime transition, int year)`
  （Date时间 TransitionPoint（时间ZoneInfo.Transition时间 transition, int year））
- `TimeZoneInfo.AdjustmentRule[] ValidateRules(List<TimeZoneInfo.AdjustmentRule> adjustmentRules)`
  （时间ZoneInfo.AdjustmentRule[] 验证Rules（List<时间ZoneInfo.AdjustmentRule> adjustmentRules））
- `TimeZoneInfo BuildFromStream(string id, Stream stream)`
  （时间Zone信息 BuildFrom流（string id, 流 stream））
- `bool ValidTZFile(byte[] buffer, int length)`
  （bool ValidTZ文件（byte[] buffer, int length））
- `int SwapInt32(int i)`
  （int SwapInt32（int i））
- `int ReadBigEndianInt32(byte[] buffer, int start)`
  （int ReadBigEndianInt32（byte[] buffer, int start））
- `TimeZoneInfo ParseTZBuffer(string id, byte[] buffer, int length)`
  （时间Zone信息 解析TZ缓冲区（string id, byte[] buffer, int length））
- `DateTime DateTimeFromUnixTime(long unix_time)`
  （Date时间 Date时间FromUnix时间（long unix_time））
- `TimeSpan GetLocalUtcOffset(DateTime dateTime, TimeZoneInfoOptions flags)`
  （时间Span 获取本地的UtcOffset（Date时间 dateTime, 时间Zone信息Options flags））
- `TimeSpan GetUtcOffset(DateTime dateTime, TimeZoneInfoOptions flags)`
  （时间Span 获取UtcOffset（Date时间 dateTime, 时间Zone信息Options flags））
- `TimeSpan GetUtcOffsetFromUtc(DateTime time, TimeZoneInfo zone, out bool isDaylightSavings, out bool isAmbiguousLocalDst)`
  （时间Span 获取UtcOffsetFromUtc（Date时间 time, 时间Zone信息 zone, out bool isDaylightSavings, out bool isAmbiguousLocalDst））

---

## TimeZoneInfo.AdjustmentRule（时间ZoneInfo.AdjustmentRule）

**继承**: IEquatable<TimeZoneInfo.AdjustmentRule>, ISerializable, IDeserializationCallback（IEquatable<时间ZoneInfo.AdjustmentRule>, ISerializable, IDeserialization回调）

### 字段 (6)

- `DateTime m_dateStart`（Date时间 m_date开始）(偏移: 0x8)
- `DateTime m_dateEnd`（Date时间 m_date结束）(偏移: 0x10)
- `TimeSpan m_daylightDelta`（时间Span m_daylightDelta）(偏移: 0x18)
- `TimeZoneInfo.TransitionTime m_daylightTransitionStart`（时间ZoneInfo.Transition时间 m_daylightTransition开始）(偏移: 0x20)
- `TimeZoneInfo.TransitionTime m_daylightTransitionEnd`（时间ZoneInfo.Transition时间 m_daylightTransition结束）(偏移: 0x38)
- `TimeSpan m_baseUtcOffsetDelta`（时间Span m_baseUtcOffsetDelta）(偏移: 0x50)

### 方法 (10)

- `DateTime get_DateStart()`
  （Date时间 get_Date开始（））
- `DateTime get_DateEnd()`
  （Date时间 get_Date结束（））
- `TimeSpan get_DaylightDelta()`
  （时间Span get_DaylightDelta（））
- `TimeZoneInfo.TransitionTime get_DaylightTransitionStart()`
  （时间ZoneInfo.Transition时间 get_DaylightTransition开始（））
- `TimeZoneInfo.TransitionTime get_DaylightTransitionEnd()`
  （时间ZoneInfo.Transition时间 get_DaylightTransition结束（））
- `bool Equals(TimeZoneInfo.AdjustmentRule other)`
  （bool Equals（时间ZoneInfo.AdjustmentRule other））
- `int GetHashCode()`
  （int 获取HashCode（））
- `TimeZoneInfo.AdjustmentRule CreateAdjustmentRule(DateTime dateStart, DateTime dateEnd, TimeSpan daylightDelta, TimeZoneInfo.TransitionTime daylightTransitionStart, TimeZoneInfo.TransitionTime daylightTransitionEnd)`
  （时间ZoneInfo.AdjustmentRule 创建AdjustmentRule（Date时间 dateStart, Date时间 dateEnd, 时间Span daylightDelta, 时间ZoneInfo.Transition时间 daylightTransitionStart, 时间ZoneInfo.Transition时间 daylightTransitionEnd））
- `TimeZoneInfo.AdjustmentRule CreateAdjustmentRule(DateTime dateStart, DateTime dateEnd, TimeSpan daylightDelta, TimeZoneInfo.TransitionTime daylightTransitionStart, TimeZoneInfo.TransitionTime daylightTransitionEnd, TimeSpan baseUtcOffsetDelta)`
  （时间ZoneInfo.AdjustmentRule 创建AdjustmentRule（Date时间 dateStart, Date时间 dateEnd, 时间Span daylightDelta, 时间ZoneInfo.Transition时间 daylightTransitionStart, 时间ZoneInfo.Transition时间 daylightTransitionEnd, 时间Span baseUtcOffsetDelta））
- `void ValidateAdjustmentRule(DateTime dateStart, DateTime dateEnd, TimeSpan daylightDelta, TimeZoneInfo.TransitionTime daylightTransitionStart, TimeZoneInfo.TransitionTime daylightTransitionEnd)`
  （void 验证AdjustmentRule（Date时间 dateStart, Date时间 dateEnd, 时间Span daylightDelta, 时间ZoneInfo.Transition时间 daylightTransitionStart, 时间ZoneInfo.Transition时间 daylightTransitionEnd））

---

## TimeZoneInfo.DYNAMIC_TIME_ZONE_INFORMATION（时间ZoneInfo.DYNAMIC_TIME_ZONE_INFORMATION）

### 字段 (3)

- `TimeZoneInfo.TIME_ZONE_INFORMATION TZI`（时间ZoneInfo.TIME_ZONE_INFORMATION TZI）(偏移: 0x0)
- `string TimeZoneKeyName`（string 时间Zone键名称）(偏移: 0x34)
- `byte DynamicDaylightTimeDisabled`（byte 动态的Daylight时间禁用的）(偏移: 0x38)

---

## TimeZoneInfo.SYSTEMTIME（时间ZoneInfo.SYSTEMTIME）

### 字段 (8)

- `ushort wYear`（ushort wYear）(偏移: 0x0)
- `ushort wMonth`（ushort wMonth）(偏移: 0x2)
- `ushort wDayOfWeek`（ushort wDayOfWeek）(偏移: 0x4)
- `ushort wDay`（ushort wDay）(偏移: 0x6)
- `ushort wHour`（ushort wHour）(偏移: 0x8)
- `ushort wMinute`（ushort wMinute）(偏移: 0xA)
- `ushort wSecond`（ushort wSecond）(偏移: 0xC)
- `ushort wMilliseconds`（ushort wMilliseconds）(偏移: 0xE)

---

## TimeZoneInfo.TIME_ZONE_INFORMATION（时间ZoneInfo.TIME_ZONE_INFORMATION）

### 字段 (7)

- `int Bias`（int Bias）(偏移: 0x0)
- `string StandardName`（string Standard名称）(偏移: 0x4)
- `TimeZoneInfo.SYSTEMTIME StandardDate`（时间ZoneInfo.SYSTEMTIME StandardDate）(偏移: 0x8)
- `int StandardBias`（int StandardBias）(偏移: 0x18)
- `string DaylightName`（string Daylight名称）(偏移: 0x1C)
- `TimeZoneInfo.SYSTEMTIME DaylightDate`（时间ZoneInfo.SYSTEMTIME DaylightDate）(偏移: 0x20)
- `int DaylightBias`（int DaylightBias）(偏移: 0x30)

---

## TimeZoneInfo.TransitionTime（时间ZoneInfo.Transition时间）

**继承**: IEquatable<TimeZoneInfo.TransitionTime>, ISerializable, IDeserializationCallback（IEquatable<时间ZoneInfo.TransitionTime>, ISerializable, IDeserialization回调）

### 字段 (6)

- `DateTime m_timeOfDay`（Date时间 m_timeOfDay）(偏移: 0x0)
- `byte m_month`（byte m_month）(偏移: 0x8)
- `byte m_week`（byte m_week）(偏移: 0x9)
- `byte m_day`（byte m_day）(偏移: 0xA)
- `DayOfWeek m_dayOfWeek`（DayOfWeek m_dayOfWeek）(偏移: 0xC)
- `bool m_isFixedDateRule`（bool m_is固定DateRule）(偏移: 0x10)

### 方法 (14)

- `DateTime get_TimeOfDay()`
  （Date时间 get_时间OfDay（））
- `int get_Month()`
  （int get_Month（））
- `int get_Week()`
  （int get_Week（））
- `int get_Day()`
  （int get_Day（））
- `DayOfWeek get_DayOfWeek()`
  （DayOfWeek get_DayOfWeek（））
- `bool get_IsFixedDateRule()`
  （bool get_是否固定DateRule（））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `bool op_Inequality(TimeZoneInfo.TransitionTime t1, TimeZoneInfo.TransitionTime t2)`
  （bool op_Inequality（时间ZoneInfo.Transition时间 t1, 时间ZoneInfo.Transition时间 t2））
- `bool Equals(TimeZoneInfo.TransitionTime other)`
  （bool Equals（时间ZoneInfo.Transition时间 other））
- `int GetHashCode()`
  （int 获取HashCode（））
- `TimeZoneInfo.TransitionTime CreateFixedDateRule(DateTime timeOfDay, int month, int day)`
  （时间ZoneInfo.Transition时间 创建固定DateRule（Date时间 timeOfDay, int month, int day））
- `TimeZoneInfo.TransitionTime CreateFloatingDateRule(DateTime timeOfDay, int month, int week, DayOfWeek dayOfWeek)`
  （时间ZoneInfo.Transition时间 创建浮空DateRule（Date时间 timeOfDay, int month, int week, DayOfWeek dayOfWeek））
- `TimeZoneInfo.TransitionTime CreateTransitionTime(DateTime timeOfDay, int month, int week, int day, DayOfWeek dayOfWeek, bool isFixedDateRule)`
  （时间ZoneInfo.Transition时间 创建Transition时间（Date时间 timeOfDay, int month, int week, int day, DayOfWeek dayOfWeek, bool isFixedDateRule））
- `void ValidateTransitionTime(DateTime timeOfDay, int month, int week, int day, DayOfWeek dayOfWeek)`
  （void 验证Transition时间（Date时间 timeOfDay, int month, int week, int day, DayOfWeek dayOfWeek））

---

## TimeZoneInfoOptions（时间Zone信息Options）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TimelineAsset（Timeline资产）

**继承**: PlayableAsset, ISerializationCallbackReceiver, ITimelineClipAsset, IPropertyPreview（Playable资产, ISerialization回调Receiver, ITimeline弹匣资产, I属性Preview）

### 字段 (9)

- `int m_Version`（int m_Version）(偏移: 0xC)
- `List<ScriptableObject> m_Tracks`（List<ScriptableObject> m_Tracks）(偏移: 0x10)
- `double m_FixedDuration`（double m_固定持续时间）(偏移: 0x18)
- `TrackAsset[] m_CacheOutputTracks`（TrackAsset[] m_缓存OutputTracks）(偏移: 0x20)
- `List<TrackAsset> m_CacheRootTracks`（List<TrackAsset> m_缓存根Tracks）(偏移: 0x24)
- `List<TrackAsset> m_CacheFlattenedTracks`（List<TrackAsset> m_缓存FlattenedTracks）(偏移: 0x28)
- `TimelineAsset.EditorSettings m_EditorSettings`（TimelineAsset.EditorSettings m_EditorSettings）(偏移: 0x2C)
- `TimelineAsset.DurationMode m_DurationMode`（TimelineAsset.持续时间模式 m_持续时间模式）(偏移: 0x30)
- `MarkerTrack m_MarkerTrack`（MarkerTrack m_MarkerTrack）(偏移: 0x34)

### 方法 (39)

- `void UpgradeToLatestVersion()`
  （void UpgradeToLatestVersion（））
- `TimelineAsset.EditorSettings get_editorSettings()`
  （TimelineAsset.EditorSettings get_editorSettings（））
- `double get_duration()`
  （double get_duration（））
- `double get_fixedDuration()`
  （double get_fixed持续时间（））
- `void set_fixedDuration(double value)`
  （void set_fixed持续时间（double value））
- `TimelineAsset.DurationMode get_durationMode()`
  （TimelineAsset.持续时间模式 get_duration模式（））
- `void set_durationMode(TimelineAsset.DurationMode value)`
  （void set_duration模式（TimelineAsset.持续时间模式 value））
- `IEnumerable<PlayableBinding> get_outputs()`
  （IEnumerable<PlayableBinding> get_outputs（））
- `ClipCaps get_clipCaps()`
  （弹匣Caps get_clipCaps（））
- `int get_outputTrackCount()`
  （int get_outputTrack数量（））
- `int get_rootTrackCount()`
  （int get_rootTrack数量（））
- `void OnValidate()`
  （void On验证（））
- `float GetValidFramerate(float framerate)`
  （float 获取ValidFramerate（float framerate））
- `TrackAsset GetRootTrack(int index)`
  （Track资产 获取根Track（int index））
- `IEnumerable<TrackAsset> GetRootTracks()`
  （IEnumerable<TrackAsset> 获取根Tracks（））
- `TrackAsset GetOutputTrack(int index)`
  （Track资产 获取OutputTrack（int index））
- `IEnumerable<TrackAsset> GetOutputTracks()`
  （IEnumerable<TrackAsset> 获取OutputTracks（））
- `void UpdateRootTrackCache()`
  （void 更新根Track缓存（））
- `void UpdateOutputTrackCache()`
  （void 更新OutputTrack缓存（））
- `IEnumerable<TrackAsset> get_flattenedTracks()`
  （IEnumerable<TrackAsset> get_flattenedTracks（））
- `MarkerTrack get_markerTrack()`
  （MarkerTrack get_markerTrack（））
- `List<ScriptableObject> get_trackObjects()`
  （List<ScriptableObject> get_trackObjects（））
- `void AddTrackInternal(TrackAsset track)`
  （void 添加Track内部的（Track资产 track））
- `void RemoveTrack(TrackAsset track)`
  （void 移除Track（Track资产 track））
- `Playable CreatePlayable(PlayableGraph graph, GameObject go)`
  （Playable 创建Playable（PlayableGraph graph, 游戏对象 go））
- `void __internalAwake()`
  （void __internalAwake（））
- `void GatherProperties(PlayableDirector director, IPropertyCollector driver)`
  （void GatherProperties（PlayableDirector director, I属性Collector driver））
- `void CreateMarkerTrack()`
  （void 创建MarkerTrack（））
- `void Invalidate()`
  （void Invalidate（））
- `void UpdateFixedDurationWithItemsDuration()`
  （void 更新固定持续时间WithItems持续时间（））
- `DiscreteTime CalculateItemsDuration()`
  （Discrete时间 计算Items持续时间（））
- `void AddSubTracksRecursive(TrackAsset track, ref List<TrackAsset> allTracks)`
  （void 添加子TracksRecursive（Track资产 track, ref List<TrackAsset> allTracks））
- `TrackAsset CreateTrack(Type type, TrackAsset parent, string name)`
  （Track资产 创建Track（类型 type, Track资产 parent, string name））
- `bool DeleteClip(TimelineClip clip)`
  （bool Delete弹匣（Timeline弹匣 clip））
- `bool DeleteTrack(TrackAsset track)`
  （bool DeleteTrack（Track资产 track））
- `void MoveLastTrackBefore(TrackAsset asset)`
  （void 移动最后一个TrackBefore（Track资产 asset））
- `TrackAsset AllocateTrack(TrackAsset trackAssetParent, string trackName, Type trackType)`
  （Track资产 AllocateTrack（Track资产 trackAssetParent, string trackName, 类型 trackType））
- `void DeleteRecordedAnimation(TrackAsset track)`
  （void DeleteRecorded动画（Track资产 track））
- `void DeleteRecordedAnimation(TimelineClip clip)`
  （void DeleteRecorded动画（Timeline弹匣 clip））

---

## TimelineAsset.DurationMode（TimelineAsset.持续时间模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TimelineAsset.EditorSettings（TimelineAsset.EditorSettings）

### 字段 (5)

- `float kMinFps`（float k最小Fps）(偏移: 0x0)
- `float kMaxFps`（float k最大Fps）(偏移: 0x4)
- `float kDefaultFps`（float k默认的Fps）(偏移: 0x8)
- `float m_Framerate`（float m_Framerate）(偏移: 0x8)
- `bool m_ScenePreview`（bool m_场景Preview）(偏移: 0xC)

### 方法 (2)

- `float get_fps()`
  （float get_fps（））
- `void set_fps(float value)`
  （void set_fps（float value））

---

## TimelineClip（Timeline弹匣）

**继承**: ICurvesOwner, ISerializationCallbackReceiver（ICurvesOwner, ISerialization回调Receiver）

### 字段 (30)

- `int m_Version`（int m_Version）(偏移: 0x8)
- `ClipCaps kDefaultClipCaps`（弹匣Caps k默认的弹匣Caps）(偏移: 0x0)
- `float kDefaultClipDurationInSeconds`（float k默认的弹匣持续时间InSeconds）(偏移: 0x4)
- `double kTimeScaleMin`（double k时间缩放最小）(偏移: 0x8)
- `double kTimeScaleMax`（double k时间缩放最大）(偏移: 0x10)
- `string kDefaultCurvesName`（string k默认的Curves名称）(偏移: 0x18)
- `double kMinDuration`（double k最小持续时间）(偏移: 0x20)
- `double kMaxTimeValue`（double k最大时间值）(偏移: 0x28)
- `double m_Start`（double m_开始）(偏移: 0x10)
- `double m_ClipIn`（double m_弹匣In）(偏移: 0x18)
- `Object m_Asset`（对象 m_资产）(偏移: 0x20)
- `double m_Duration`（double m_持续时间）(偏移: 0x28)
- `double m_TimeScale`（double m_时间缩放）(偏移: 0x30)
- `TrackAsset m_ParentTrack`（Track资产 m_父级Track）(偏移: 0x38)
- `double m_EaseInDuration`（double m_EaseIn持续时间）(偏移: 0x40)
- `double m_EaseOutDuration`（double m_EaseOut持续时间）(偏移: 0x48)
- `double m_BlendInDuration`（double m_BlendIn持续时间）(偏移: 0x50)
- `double m_BlendOutDuration`（double m_BlendOut持续时间）(偏移: 0x58)
- `AnimationCurve m_MixInCurve`（动画Curve m_MixInCurve）(偏移: 0x60)
- `AnimationCurve m_MixOutCurve`（动画Curve m_MixOutCurve）(偏移: 0x64)
- `TimelineClip.BlendCurveMode m_BlendInCurveMode`（TimelineClip.BlendCurve模式 m_BlendInCurve模式）(偏移: 0x68)
- `TimelineClip.BlendCurveMode m_BlendOutCurveMode`（TimelineClip.BlendCurve模式 m_BlendOutCurve模式）(偏移: 0x6C)
- `List<string> m_ExposedParameterNames`（List<string> m_ExposedParameterNames）(偏移: 0x70)
- `AnimationClip m_AnimationCurves`（动画弹匣 m_动画Curves）(偏移: 0x74)
- `bool m_Recordable`（bool m_Recordable）(偏移: 0x78)
- `TimelineClip.ClipExtrapolation m_PostExtrapolationMode`（TimelineClip.弹匣Extrapolation m_PostExtrapolation模式）(偏移: 0x7C)
- `TimelineClip.ClipExtrapolation m_PreExtrapolationMode`（TimelineClip.弹匣Extrapolation m_PreExtrapolation模式）(偏移: 0x80)
- `double m_PostExtrapolationTime`（double m_PostExtrapolation时间）(偏移: 0x88)
- `double m_PreExtrapolationTime`（double m_PreExtrapolation时间）(偏移: 0x90)
- `string m_DisplayName`（string m_Display名称）(偏移: 0x98)

### 方法 (51)

- `void UpgradeToLatestVersion()`
  （void UpgradeToLatestVersion（））
- `double get_timeScale()`
  （double get_time缩放（））
- `double get_start()`
  （double get_start（））
- `void set_start(double value)`
  （void set_start（double value））
- `double get_duration()`
  （double get_duration（））
- `void set_duration(double value)`
  （void set_duration（double value））
- `double get_end()`
  （double get_end（））
- `double get_clipIn()`
  （double get_clipIn（））
- `string get_displayName()`
  （string get_display名称（））
- `void set_displayName(string value)`
  （void set_display名称（string value））
- `AnimationClip get_curves()`
  （动画弹匣 get_curves（））
- `Object get_asset()`
  （对象 get_asset（））
- `void set_asset(Object value)`
  （void set_asset（对象 value））
- `TrackAsset get_parentTrack()`
  （Track资产 get_parentTrack（））
- `void set_parentTrack(TrackAsset value)`
  （void set_parentTrack（Track资产 value））
- `double get_easeInDuration()`
  （double get_easeIn持续时间（））
- `double get_easeOutDuration()`
  （double get_easeOut持续时间（））
- `double get_blendInDuration()`
  （double get_blendIn持续时间（））
- `double get_blendOutDuration()`
  （double get_blendOut持续时间（））
- `bool get_hasBlendIn()`
  （bool get_hasBlendIn（））
- `bool get_hasBlendOut()`
  （bool get_hasBlendOut（））
- `AnimationCurve get_mixInCurve()`
  （动画Curve get_mixInCurve（））
- `void set_mixInCurve(AnimationCurve value)`
  （void set_mixInCurve（动画Curve value））
- `double get_mixInDuration()`
  （double get_mixIn持续时间（））
- `AnimationCurve get_mixOutCurve()`
  （动画Curve get_mixOutCurve（））
- `void set_mixOutCurve(AnimationCurve value)`
  （void set_mixOutCurve（动画Curve value））
- `double get_mixOutTime()`
  （double get_mixOut时间（））
- `double get_mixOutDuration()`
  （double get_mixOut持续时间（））
- `bool get_recordable()`
  （bool get_recordable（））
- `void set_recordable(bool value)`
  （void set_recordable（bool value））
- `ClipCaps get_clipCaps()`
  （弹匣Caps get_clipCaps（））
- `int Hash()`
  （int Hash（））
- `float EvaluateMixOut(double time)`
  （float EvaluateMixOut（double time））
- `float EvaluateMixIn(double time)`
  （float EvaluateMixIn（double time））
- `AnimationCurve GetDefaultMixInCurve()`
  （动画Curve 获取默认的MixInCurve（））
- `AnimationCurve GetDefaultMixOutCurve()`
  （动画Curve 获取默认的MixOutCurve（））
- `double ToLocalTime(double time)`
  （double To本地的时间（double time））
- `double SanitizeTimeValue(double value, double defaultValue)`
  （double Sanitize时间值（double value, double defaultValue））
- `TimelineClip.ClipExtrapolation get_postExtrapolationMode()`
  （TimelineClip.弹匣Extrapolation get_postExtrapolation模式（））
- `void set_postExtrapolationMode(TimelineClip.ClipExtrapolation value)`
  （void set_postExtrapolation模式（TimelineClip.弹匣Extrapolation value））
- `TimelineClip.ClipExtrapolation get_preExtrapolationMode()`
  （TimelineClip.弹匣Extrapolation get_preExtrapolation模式（））
- `void set_preExtrapolationMode(TimelineClip.ClipExtrapolation value)`
  （void set_preExtrapolation模式（TimelineClip.弹匣Extrapolation value））
- `void SetPostExtrapolationTime(double time)`
  （void 集合PostExtrapolation时间（double time））
- `void SetPreExtrapolationTime(double time)`
  （void 集合PreExtrapolation时间（double time））
- `bool IsPreExtrapolatedTime(double sequenceTime)`
  （bool 是否PreExtrapolated时间（double sequenceTime））
- `bool IsPostExtrapolatedTime(double sequenceTime)`
  （bool 是否PostExtrapolated时间（double sequenceTime））
- `double get_extrapolatedStart()`
  （double get_extrapolated开始（））
- `double get_extrapolatedDuration()`
  （double get_extrapolated持续时间（））
- `double GetExtrapolatedTime(double time, TimelineClip.ClipExtrapolation mode, double duration)`
  （double 获取Extrapolated时间（double time, TimelineClip.弹匣Extrapolation mode, double duration））
- `string ToString()`
  （string To字符串（））
- `void UpdateDirty(double oldValue, double newValue)`
  （void 更新Dirty（double oldValue, double newValue））

---

## TimelineClip.BlendCurveMode（TimelineClip.BlendCurve模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TimelineClip.ClipExtrapolation（TimelineClip.弹匣Extrapolation）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TimelineClip.TimelineClipUpgrade（TimelineClip.Timeline弹匣Upgrade）

### 方法 (1)

- `void UpgradeClipInFromGlobalToLocal(TimelineClip clip)`
  （void Upgrade弹匣InFrom全局的To本地的（Timeline弹匣 clip））

---

## TimelineClipCapsExtensions（Timeline弹匣CapsExtensions）

### 方法 (2)

- `bool SupportsExtrapolation(TimelineClip clip)`
  （bool SupportsExtrapolation（Timeline弹匣 clip））
- `bool HasAny(ClipCaps caps, ClipCaps flags)`
  （bool 是否有任意（弹匣Caps caps, 弹匣Caps flags））

---

## TimelineCreateUtilities（Timeline创建Utilities）

### 方法 (4)

- `string GenerateUniqueActorName(List<ScriptableObject> tracks, string name)`
  （string GenerateUniqueActor名称（List<ScriptableObject> tracks, string name））
- `void SaveAssetIntoObject(Object childAsset, Object masterAsset)`
  （void 保存资产Into对象（对象 childAsset, 对象 masterAsset））
- `AnimationClip CreateAnimationClipForTrack(string name, TrackAsset track, bool isLegacy)`
  （动画弹匣 创建动画弹匣ForTrack（string name, Track资产 track, bool isLegacy））
- `bool ValidateParentTrack(TrackAsset parent, Type childType)`
  （bool 验证父级Track（Track资产 parent, 类型 childType））

---

## TimelinePlayable（TimelinePlayable）

**继承**: PlayableBehaviour（PlayableBehaviour）

### 字段 (6)

- `IntervalTree<RuntimeElement> m_IntervalTree`（间隔Tree<RuntimeElement> m_间隔Tree）(偏移: 0x8)
- `List<RuntimeElement> m_ActiveClips`（List<RuntimeElement> m_激活的Clips）(偏移: 0xC)
- `List<RuntimeElement> m_CurrentListOfActiveClips`（List<RuntimeElement> m_当前列表Of激活的Clips）(偏移: 0x10)
- `int m_ActiveBit`（int m_激活的Bit）(偏移: 0x14)
- `List<ITimelineEvaluateCallback> m_EvaluateCallbacks`（List<ITimelineEvaluateCallback> m_EvaluateCallbacks）(偏移: 0x18)
- `bool muteAudioScrubbing`（bool mute音频Scrubbing）(偏移: 0x0)

### 方法 (10)

- `ScriptPlayable<TimelinePlayable> Create(PlayableGraph graph, IEnumerable<TrackAsset> tracks, GameObject go, bool autoRebalance, bool createOutputs)`
  （ScriptPlayable<TimelinePlayable> 创建（PlayableGraph graph, IEnumerable<TrackAsset> tracks, 游戏对象 go, bool autoRebalance, bool createOutputs））
- `void Compile(PlayableGraph graph, Playable timelinePlayable, IEnumerable<TrackAsset> tracks, GameObject go, bool autoRebalance, bool createOutputs)`
  （void Compile（PlayableGraph graph, Playable timelinePlayable, IEnumerable<TrackAsset> tracks, 游戏对象 go, bool autoRebalance, bool createOutputs））
- `void CompileTrackList(PlayableGraph graph, Playable timelinePlayable, IEnumerable<TrackAsset> tracks, GameObject go, bool createOutputs)`
  （void CompileTrack列表（PlayableGraph graph, Playable timelinePlayable, IEnumerable<TrackAsset> tracks, 游戏对象 go, bool createOutputs））
- `void CreateTrackOutput(PlayableGraph graph, TrackAsset track, GameObject go, Playable playable, int port)`
  （void 创建TrackOutput（PlayableGraph graph, Track资产 track, 游戏对象 go, Playable playable, int port））
- `void EvaluateWeightsForAnimationPlayableOutput(TrackAsset track, AnimationPlayableOutput animOutput)`
  （void EvaluateWeightsFor动画PlayableOutput（Track资产 track, 动画PlayableOutput animOutput））
- `Playable CreatePlayableGraph(PlayableGraph graph, TrackAsset asset, GameObject go, IntervalTree<RuntimeElement> tree, Playable timelinePlayable)`
  （Playable 创建PlayableGraph（PlayableGraph graph, Track资产 asset, 游戏对象 go, 间隔Tree<RuntimeElement> tree, Playable timelinePlayable））
- `Playable CreateTrackPlayable(PlayableGraph graph, Playable timelinePlayable, TrackAsset track, GameObject go, bool createOutputs)`
  （Playable 创建TrackPlayable（PlayableGraph graph, Playable timelinePlayable, Track资产 track, 游戏对象 go, bool createOutputs））
- `void PrepareFrame(Playable playable, FrameData info)`
  （void PrepareFrame（Playable playable, Frame数据 info））
- `void Evaluate(Playable playable, FrameData frameData)`
  （void Evaluate（Playable playable, Frame数据 frameData））
- `void CacheTrack(TrackAsset track, Playable playable, int port, Playable parent)`
  （void 缓存Track（Track资产 track, Playable playable, int port, Playable parent））

---

## TimelineUndo（TimelineUndo）

### 方法 (1)

- `void PushDestroyUndo(TimelineAsset timeline, Object thingToDirty, Object objectToDestroy)`
  （void Push销毁Undo（Timeline资产 timeline, 对象 thingToDirty, 对象 objectToDestroy））

---

## Timeout（超时）

### 字段 (1)

- `TimeSpan InfiniteTimeSpan`（时间Span Infinite时间Span）(偏移: 0x0)

---

## TimeoutHelper（超时辅助器）

### 方法 (2)

- `uint GetTime()`
  （uint 获取时间（））
- `int UpdateTimeOut(uint startTime, int originalWaitMillisecondsTimeout)`
  （int 更新时间Out（uint startTime, int originalWaitMillisecondsTimeout））

---

## Timer（计时器）

**继承**: MarshalByRefObject, IDisposable（MarshalByRef对象, IDisposable）

### 字段 (7)

- `Timer.Scheduler scheduler`（Timer.Scheduler scheduler）(偏移: 0x0)
- `TimerCallback callback`（计时器回调 callback）(偏移: 0xC)
- `object state`（object state）(偏移: 0x10)
- `long due_time_ms`（long due_time_ms）(偏移: 0x18)
- `long period_ms`（long period_ms）(偏移: 0x20)
- `long next_run`（long next_run）(偏移: 0x28)
- `bool disposed`（bool disposed）(偏移: 0x30)

### 方法 (6)

- `void Init(TimerCallback callback, object state, long dueTime, long period)`
  （void 初始化（计时器回调 callback, object state, long dueTime, long period））
- `bool Change(TimeSpan dueTime, TimeSpan period)`
  （bool Change（时间Span dueTime, 时间Span period））
- `void Dispose()`
  （void 释放（））
- `bool Change(long dueTime, long period, bool first)`
  （bool Change（long dueTime, long period, bool first））
- `void KeepRootedWhileScheduled()`
  （void KeepRootedWhileScheduled（））
- `long GetTimeMonotonic()`
  （long 获取时间Monotonic（））

---

## Timer.Scheduler（Timer.Scheduler）

### 字段 (3)

- `Timer.Scheduler instance`（Timer.Scheduler instance）(偏移: 0x0)
- `SortedList list`（Sorted列表 list）(偏移: 0x8)
- `ManualResetEvent changed`（手动重置事件 changed）(偏移: 0xC)

### 方法 (9)

- `Timer.Scheduler get_Instance()`
  （Timer.Scheduler get_实例（））
- `void Remove(Timer timer)`
  （void 移除（计时器 timer））
- `void Change(Timer timer, long new_next_run)`
  （void Change（计时器 timer, long new_next_run））
- `int FindByDueTime(long nr)`
  （int 查找ByDue时间（long nr））
- `void Add(Timer timer)`
  （void 添加（计时器 timer））
- `int InternalRemove(Timer timer)`
  （int 内部的移除（计时器 timer））
- `void TimerCB(object o)`
  （void 计时器CB（object o））
- `void SchedulerThread()`
  （void SchedulerThread（））
- `void ShrinkIfNeeded(List<Timer> list, int initial)`
  （void ShrinkIfNeeded（List<Timer> list, int initial））

---

## Timer.TimerComparer（Timer.计时器Comparer）

**继承**: IComparer（IComparer）

### 方法 (1)

- `int Compare(object x, object y)`
  （int Compare（object x, object y））

---

## TimerCallback（计时器回调）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(object state)`
  （void Invoke（object state））
- `IAsyncResult BeginInvoke(object state, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（object state, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## TinyJsonDeserializer（TinyJsonDeserializer）

### 字段 (3)

- `TextReader reader`（文本读取器 reader）(偏移: 0x8)
- `NumberFormatInfo numberFormat`（Number格式化信息 number格式化）(偏移: 0x0)
- `StringBuilder builder`（字符串构建器 builder）(偏移: 0xC)

### 方法 (10)

- `object Deserialize(string text, Type type, object populate)`
  （object Deserialize（string text, 类型 type, object populate））
- `object Deserialize(Type tp, object populate)`
  （object Deserialize（类型 tp, object populate））
- `Object DeserializeUnityObject()`
  （对象 DeserializeUnity引擎对象（））
- `Object DeserializeUnityObjectInner()`
  （对象 DeserializeUnity引擎对象Inner（））
- `void EatWhitespace()`
  （void EatWhitespace（））
- `void Eat(string s)`
  （void Eat（string s））
- `string EatUntil(string c, bool inString)`
  （string EatUntil（string c, bool inString））
- `bool TryEat(char c)`
  （bool TryEat（char c））
- `string EatField()`
  （string EatField（））
- `void SkipFieldData()`
  （void SkipField数据（））

---

## TinyJsonSerializer（TinyJsonSerializer）

### 字段 (2)

- `StringBuilder output`（字符串构建器 output）(偏移: 0x8)
- `CultureInfo invariantCulture`（Culture信息 invariantCulture）(偏移: 0x0)

### 方法 (4)

- `void Serialize(object obj, StringBuilder output)`
  （void Serialize（object obj, 字符串构建器 output））
- `void Serialize(object obj)`
  （void Serialize（object obj））
- `void QuotedField(string name, string contents)`
  （void QuotedField（string name, string contents））
- `void SerializeUnityObject(Object obj)`
  （void SerializeUnity引擎对象（对象 obj））

---

## Toggle（开关）

**继承**: Selectable, IPointerClickHandler, IEventSystemHandler, ISubmitHandler, ICanvasElement（Selectable, I指针Click处理器, I事件系统处理器, ISubmit处理器, I画布元素）

### 字段 (5)

- `Toggle.ToggleTransition toggleTransition`（Toggle.开关Transition toggleTransition）(偏移: 0xB0)
- `Graphic graphic`（Graphic graphic）(偏移: 0xB4)
- `ToggleGroup m_Group`（开关组 m_组）(偏移: 0xB8)
- `Toggle.ToggleEvent onValueChanged`（Toggle.开关事件 on值Changed）(偏移: 0xBC)
- `bool m_IsOn`（bool m_是否On）(偏移: 0xC0)

### 方法 (19)

- `ToggleGroup get_group()`
  （开关组 get_group（））
- `void set_group(ToggleGroup value)`
  （void set_group（开关组 value））
- `void Rebuild(CanvasUpdate executing)`
  （void Rebuild（画布更新 executing））
- `void LayoutComplete()`
  （void LayoutComplete（））
- `void GraphicUpdateComplete()`
  （void Graphic更新Complete（））
- `void OnDestroy()`
  （void On销毁（））
- `void OnEnable()`
  （void On启用（））
- `void OnDisable()`
  （void On禁用（））
- `void OnDidApplyAnimationProperties()`
  （void OnDid应用动画Properties（））
- `void SetToggleGroup(ToggleGroup newGroup, bool setMemberValue)`
  （void 集合开关组（开关组 newGroup, bool setMemberValue））
- `bool get_isOn()`
  （bool get_isOn（））
- `void set_isOn(bool value)`
  （void set_isOn（bool value））
- `void SetIsOnWithoutNotify(bool value)`
  （void 集合是否OnWithoutNotify（bool value））
- `void Set(bool value, bool sendCallback = True)`
  （void 集合（bool value, bool sendCallback = True））
- `void PlayEffect(bool instant)`
  （void 播放特效（bool instant））
- `void Start()`
  （void 开始（））
- `void InternalToggle()`
  （void 内部的开关（））
- `void OnPointerClick(PointerEventData eventData)`
  （void On指针Click（指针事件数据 eventData））
- `void OnSubmit(BaseEventData eventData)`
  （void OnSubmit（基础事件数据 eventData））

---

## Toggle.ToggleTransition（Toggle.开关Transition）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ToggleGroup（开关组）

**继承**: UIBehaviour（界面Behaviour）

### 字段 (2)

- `bool m_AllowSwitchOff`（bool m_允许SwitchOff）(偏移: 0xC)
- `List<Toggle> m_Toggles`（List<Toggle> m_Toggles）(偏移: 0x10)

### 方法 (13)

- `bool get_allowSwitchOff()`
  （bool get_allowSwitchOff（））
- `void set_allowSwitchOff(bool value)`
  （void set_allowSwitchOff（bool value））
- `void Start()`
  （void 开始（））
- `void OnEnable()`
  （void On启用（））
- `void ValidateToggleIsInGroup(Toggle toggle)`
  （void 验证开关是否In组（开关 toggle））
- `void NotifyToggleOn(Toggle toggle, bool sendCallback = True)`
  （void Notify开关On（开关 toggle, bool sendCallback = True））
- `void UnregisterToggle(Toggle toggle)`
  （void Unregister开关（开关 toggle））
- `void RegisterToggle(Toggle toggle)`
  （void Register开关（开关 toggle））
- `void EnsureValidState()`
  （void EnsureValid状态（））
- `bool AnyTogglesOn()`
  （bool 任意TogglesOn（））
- `IEnumerable<Toggle> ActiveToggles()`
  （IEnumerable<Toggle> 激活的Toggles（））
- `Toggle GetFirstActiveToggle()`
  （开关 获取第一个激活的开关（））
- `void SetAllTogglesOff(bool sendCallback = True)`
  （void 集合所有TogglesOff（bool sendCallback = True））

---

## TokenHashValue（令牌Hash值）

### 字段 (3)

- `string tokenString`（string token字符串）(偏移: 0x8)
- `TokenType tokenType`（令牌类型 token类型）(偏移: 0xC)
- `int tokenValue`（int token值）(偏移: 0x10)

---

## TokenType（令牌类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TombStone（TombStone）

**继承**: Entity（实体）

### 字段 (5)

- `Player owner`（玩家 owner）(偏移: 0x48)
- `GameObject effect`（游戏对象 effect）(偏移: 0x4C)
- `HUD_HealthBar bar`（HUD_HealthBar bar）(偏移: 0x50)
- `Transform[] hitbox`（Transform[] hitbox）(偏移: 0x54)
- `RecyclableObject RO`（Recyclable对象 RO）(偏移: 0x58)

### 方法 (11)

- `void Awake()`
  （void Awake（））
- `void Update()`
  （void 更新（））
- `void OnEnable()`
  （void On启用（））
- `void OnRecycle()`
  （void OnRecycle（））
- `void OnNoRoundRecycle()`
  （void OnNo回合Recycle（））
- `void Spawn()`
  （void 出生（））
- `void OnEntityHurt(DamageEventData eventData)`
  （void On实体Hurt（伤害事件数据 eventData））
- `void OnEntityDeath(DeathEventData eventData)`
  （void On实体死亡（死亡事件数据 eventData））
- `void SetOwner(Player owner)`
  （void 集合Owner（玩家 owner））
- `string GetName()`
  （string 获取名称（））
- `Transform GetVisibleHitBox(Ray viewRay)`
  （变换 获取可见的命中Box（Ray viewRay））

---

## Tonemapping（Tonemapping）

**继承**: VolumeComponent, IPostProcessComponent（Volume组件, IPost处理组件）

### 字段 (1)

- `TonemappingModeParameter mode`（Tonemapping模式Parameter mode）(偏移: 0x1C)

### 方法 (2)

- `bool IsActive()`
  （bool 是否激活的（））
- `bool IsTileCompatible()`
  （bool 是否TileCompatible（））

---

## TonemappingMode（Tonemapping模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TooltipAttribute（TooltipAttribute）

**继承**: PropertyAttribute（属性Attribute）

### 字段 (1)

- `string tooltip`（string tooltip）(偏移: 0x8)

---

## Touch（触摸）

### 字段 (14)

- `int m_FingerId`（int m_FingerId）(偏移: 0x0)
- `Vector2 m_Position`（二维向量 m_Position）(偏移: 0x4)
- `Vector2 m_RawPosition`（二维向量 m_RawPosition）(偏移: 0xC)
- `Vector2 m_PositionDelta`（二维向量 m_PositionDelta）(偏移: 0x14)
- `float m_TimeDelta`（float m_时间Delta）(偏移: 0x1C)
- `int m_TapCount`（int m_Tap数量）(偏移: 0x20)
- `TouchPhase m_Phase`（触摸Phase m_Phase）(偏移: 0x24)
- `TouchType m_Type`（触摸类型 m_类型）(偏移: 0x28)
- `float m_Pressure`（float m_Pressure）(偏移: 0x2C)
- `float m_maximumPossiblePressure`（float m_maximumPossiblePressure）(偏移: 0x30)
- `float m_Radius`（float m_Radius）(偏移: 0x34)
- `float m_RadiusVariance`（float m_RadiusVariance）(偏移: 0x38)
- `float m_AltitudeAngle`（float m_Altitude角度）(偏移: 0x3C)
- `float m_AzimuthAngle`（float m_Azimuth角度）(偏移: 0x40)

### 方法 (5)

- `int get_fingerId()`
  （int get_fingerId（））
- `Vector2 get_position()`
  （二维向量 get_position（））
- `Vector2 get_deltaPosition()`
  （二维向量 get_deltaPosition（））
- `TouchPhase get_phase()`
  （触摸Phase get_phase（））
- `TouchType get_type()`
  （触摸类型 get_type（））

---

## TouchInputModule（触摸输入模块）

**继承**: PointerInputModule（指针输入模块）

### 字段 (4)

- `Vector2 m_LastMousePosition`（二维向量 m_最后一个鼠标Position）(偏移: 0x2C)
- `Vector2 m_MousePosition`（二维向量 m_鼠标Position）(偏移: 0x34)
- `PointerEventData m_InputPointerEvent`（指针事件数据 m_输入指针事件）(偏移: 0x3C)
- `bool m_ForceModuleActive`（bool m_强制模块激活的）(偏移: 0x40)

### 方法 (14)

- `bool get_allowActivationOnStandalone()`
  （bool get_allowActivationOnStandalone（））
- `void set_allowActivationOnStandalone(bool value)`
  （void set_allowActivationOnStandalone（bool value））
- `bool get_forceModuleActive()`
  （bool get_force模块激活的（））
- `void set_forceModuleActive(bool value)`
  （void set_force模块激活的（bool value））
- `void UpdateModule()`
  （void 更新模块（））
- `bool IsModuleSupported()`
  （bool 是否模块Supported（））
- `bool ShouldActivateModule()`
  （bool 应该激活模块（））
- `bool UseFakeInput()`
  （bool UseFake输入（））
- `void Process()`
  （void 处理（））
- `void FakeTouches()`
  （void FakeTouches（））
- `void ProcessTouchEvents()`
  （void 处理触摸Events（））
- `void ProcessTouchPress(PointerEventData pointerEvent, bool pressed, bool released)`
  （void 处理触摸Press（指针事件数据 pointerEvent, bool pressed, bool released））
- `void DeactivateModule()`
  （void 停用模块（））
- `string ToString()`
  （string To字符串（））

---

## TouchPhase（触摸Phase）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TouchScreenKeyboard（触摸屏幕的键盘）

### 字段 (1)

- `IntPtr m_Ptr`（整数Ptr m_Ptr）(偏移: 0x8)

### 方法 (21)

- `void Internal_Destroy(IntPtr ptr)`
  （void Internal_销毁（整数Ptr ptr））
- `void Destroy()`
  （void 销毁（））
- `void Finalize()`
  （void Finalize（））
- `IntPtr TouchScreenKeyboard_InternalConstructorHelper(ref TouchScreenKeyboard_InternalConstructorHelperArguments arguments, string text, string textPlaceholder)`
  （整数Ptr 触摸屏幕的Keyboard_内部的Constructor辅助器（ref TouchScreenKeyboard_InternalConstructorHelperArguments arguments, string text, string textPlaceholder））
- `bool get_isSupported()`
  （bool get_isSupported（））
- `bool get_disableInPlaceEditing()`
  （bool get_disableInPlaceEditing（））
- `bool get_isInPlaceEditingAllowed()`
  （bool get_isInPlaceEditingAllowed（））
- `TouchScreenKeyboard Open(string text, TouchScreenKeyboardType keyboardType, bool autocorrection, bool multiline, bool secure, bool alert, string textPlaceholder, int characterLimit)`
  （触摸屏幕的键盘 打开（string text, 触摸屏幕的键盘类型 keyboardType, bool autocorrection, bool multiline, bool secure, bool alert, string textPlaceholder, int characterLimit））
- `string get_text()`
  （string get_text（））
- `void set_text(string value)`
  （void set_text（string value））
- `void set_hideInput(bool value)`
  （void set_hide输入（bool value））
- `bool get_active()`
  （bool get_active（））
- `void set_active(bool value)`
  （void set_active（bool value））
- `TouchScreenKeyboard.Status get_status()`
  （触摸屏幕的Keyboard.Status get_status（））
- `void set_characterLimit(int value)`
  （void set_characterLimit（int value））
- `bool get_canGetSelection()`
  （bool get_can获取Selection（））
- `bool get_canSetSelection()`
  （bool get_can集合Selection（））
- `RangeInt get_selection()`
  （范围整数 get_selection（））
- `void set_selection(RangeInt value)`
  （void set_selection（范围整数 value））
- `void GetSelection(out int start, out int length)`
  （void 获取Selection（out int start, out int length））
- `void SetSelection(int start, int length)`
  （void 集合Selection（int start, int length））

---

## TouchScreenKeyboard.Status（触摸屏幕的Keyboard.Status）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TouchScreenKeyboardType（触摸屏幕的键盘类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TouchScreenKeyboard_InternalConstructorHelperArguments（触摸屏幕的Keyboard_内部的Constructor辅助器Arguments）

### 字段 (6)

- `uint keyboardType`（uint keyboard类型）(偏移: 0x0)
- `uint autocorrection`（uint autocorrection）(偏移: 0x4)
- `uint multiline`（uint multiline）(偏移: 0x8)
- `uint secure`（uint secure）(偏移: 0xC)
- `uint alert`（uint alert）(偏移: 0x10)
- `int characterLimit`（int characterLimit）(偏移: 0x14)

---

## TouchType（触摸类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TplEtwProvider（TplEtw提供者）

**继承**: EventSource（事件Source）

### 字段 (1)

- `TplEtwProvider Log`（TplEtw提供者 Log）(偏移: 0x0)

### 方法 (4)

- `bool get_Debug()`
  （bool get_Debug（））
- `void DebugFacilityMessage(string Facility, string Message)`
  （void DebugFacilityMessage（string Facility, string Message））
- `void DebugFacilityMessage1(string Facility, string Message, string Arg)`
  （void DebugFacilityMessage1（string Facility, string Message, string Arg））
- `void SetActivityId(Guid Id)`
  （void 集合ActivityId（Guid Id））

---

## TraceLevel（Trace等级）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TraceLoggingDataCollector（TraceLogging数据Collector）

### 字段 (1)

- `TraceLoggingDataCollector Instance`（TraceLogging数据Collector 实例）(偏移: 0x0)

### 方法 (33)

- `int BeginBufferedArray()`
  （int BeginBuffered数组（））
- `void EndBufferedArray(int bookmark, int count)`
  （void 结束Buffered数组（int bookmark, int count））
- `void AddScalar(bool value)`
  （void 添加Scalar（bool value））
- `void AddScalar(sbyte value)`
  （void 添加Scalar（sbyte value））
- `void AddScalar(byte value)`
  （void 添加Scalar（byte value））
- `void AddScalar(short value)`
  （void 添加Scalar（short value））
- `void AddScalar(ushort value)`
  （void 添加Scalar（ushort value））
- `void AddScalar(int value)`
  （void 添加Scalar（int value））
- `void AddScalar(uint value)`
  （void 添加Scalar（uint value））
- `void AddScalar(long value)`
  （void 添加Scalar（long value））
- `void AddScalar(ulong value)`
  （void 添加Scalar（ulong value））
- `void AddScalar(IntPtr value)`
  （void 添加Scalar（整数Ptr value））
- `void AddScalar(UIntPtr value)`
  （void 添加Scalar（U整数Ptr value））
- `void AddScalar(float value)`
  （void 添加Scalar（float value））
- `void AddScalar(double value)`
  （void 添加Scalar（double value））
- `void AddScalar(char value)`
  （void 添加Scalar（char value））
- `void AddScalar(Guid value)`
  （void 添加Scalar（Guid value））
- `void AddBinary(string value)`
  （void 添加Binary（string value））
- `void AddBinary(byte[] value)`
  （void 添加Binary（byte[] value））
- `void AddArray(bool[] value)`
  （void 添加数组（bool[] value））
- `void AddArray(sbyte[] value)`
  （void 添加数组（sbyte[] value））
- `void AddArray(short[] value)`
  （void 添加数组（short[] value））
- `void AddArray(ushort[] value)`
  （void 添加数组（ushort[] value））
- `void AddArray(int[] value)`
  （void 添加数组（int[] value））
- `void AddArray(uint[] value)`
  （void 添加数组（uint[] value））
- `void AddArray(long[] value)`
  （void 添加数组（long[] value））
- `void AddArray(ulong[] value)`
  （void 添加数组（ulong[] value））
- `void AddArray(IntPtr[] value)`
  （void 添加数组（整数Ptr[] value））
- `void AddArray(UIntPtr[] value)`
  （void 添加数组（U整数Ptr[] value））
- `void AddArray(float[] value)`
  （void 添加数组（float[] value））
- `void AddArray(double[] value)`
  （void 添加数组（double[] value））
- `void AddArray(char[] value)`
  （void 添加数组（char[] value））
- `void AddArray(Guid[] value)`
  （void 添加数组（Guid[] value））

---

## TraceLoggingDataType（TraceLogging数据类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TraceLoggingEventTypes（TraceLogging事件Types）

### 字段 (10)

- `TraceLoggingTypeInfo[] typeInfos`（TraceLogging类型Info[] typeInfos）(偏移: 0x8)
- `string name`（string name）(偏移: 0xC)
- `EventTags tags`（事件Tags tags）(偏移: 0x10)
- `byte level`（byte level）(偏移: 0x14)
- `byte opcode`（byte opcode）(偏移: 0x15)
- `EventKeywords keywords`（事件Keywords keywords）(偏移: 0x18)
- `byte[] typeMetadata`（byte[] typeMetadata）(偏移: 0x20)
- `int scratchSize`（int scratch大小）(偏移: 0x24)
- `int dataCount`（int data数量）(偏移: 0x28)
- `int pinCount`（int pin数量）(偏移: 0x2C)

### 方法 (5)

- `string get_Name()`
  （string get_名称（））
- `EventTags get_Tags()`
  （事件Tags get_Tags（））
- `NameInfo GetNameInfo(string name, EventTags tags)`
  （名称信息 获取名称信息（string name, 事件Tags tags））
- `TraceLoggingTypeInfo[] MakeArray(ParameterInfo[] paramInfos)`
  （TraceLogging类型Info[] Make数组（ParameterInfo[] paramInfos））
- `TraceLoggingTypeInfo[] MakeArray(Type[] types)`
  （TraceLogging类型Info[] Make数组（Type[] types））

---

## TraceLoggingMetadataCollector（TraceLoggingMetadataCollector）

### 字段 (3)

- `TraceLoggingMetadataCollector.Impl impl`（TraceLoggingMetadataCollector.Impl impl）(偏移: 0x8)
- `FieldMetadata currentGroup`（FieldMetadata current组）(偏移: 0xC)
- `int bufferedArrayFieldCount`（int buffered数组Field数量）(偏移: 0x10)

### 方法 (14)

- `EventFieldTags get_Tags()`
  （事件FieldTags get_Tags（））
- `void set_Tags(EventFieldTags value)`
  （void set_Tags（事件FieldTags value））
- `int get_ScratchSize()`
  （int get_Scratch大小（））
- `int get_DataCount()`
  （int get_数据数量（））
- `int get_PinCount()`
  （int get_Pin数量（））
- `bool get_BeginningBufferedArray()`
  （bool get_BeginningBuffered数组（））
- `TraceLoggingMetadataCollector AddGroup(string name)`
  （TraceLoggingMetadataCollector 添加组（string name））
- `void AddScalar(string name, TraceLoggingDataType type)`
  （void 添加Scalar（string name, TraceLogging数据类型 type））
- `void AddBinary(string name, TraceLoggingDataType type)`
  （void 添加Binary（string name, TraceLogging数据类型 type））
- `void AddArray(string name, TraceLoggingDataType type)`
  （void 添加数组（string name, TraceLogging数据类型 type））
- `void BeginBufferedArray()`
  （void BeginBuffered数组（））
- `void EndBufferedArray()`
  （void 结束Buffered数组（））
- `byte[] GetMetadata()`
  （byte[] 获取Metadata（））
- `void AddField(FieldMetadata fieldMetadata)`
  （void 添加Field（FieldMetadata fieldMetadata））

---

## TraceLoggingMetadataCollector.Impl（TraceLoggingMetadataCollector.Impl）

### 字段 (6)

- `List<FieldMetadata> fields`（List<FieldMetadata> fields）(偏移: 0x8)
- `short scratchSize`（short scratch大小）(偏移: 0xC)
- `sbyte dataCount`（sbyte data数量）(偏移: 0xE)
- `sbyte pinCount`（sbyte pin数量）(偏移: 0xF)
- `int bufferNesting`（int bufferNesting）(偏移: 0x10)
- `bool scalar`（bool scalar）(偏移: 0x14)

### 方法 (5)

- `void AddScalar(int size)`
  （void 添加Scalar（int size））
- `void AddNonscalar()`
  （void 添加Nonscalar（））
- `void BeginBuffered()`
  （void BeginBuffered（））
- `void EndBuffered()`
  （void 结束Buffered（））
- `int Encode(byte[] metadata)`
  （int Encode（byte[] metadata））

---

## TraceLoggingTypeInfo（TraceLogging类型信息）

### 字段 (6)

- `string name`（string name）(偏移: 0x8)
- `EventKeywords keywords`（事件Keywords keywords）(偏移: 0x10)
- `EventLevel level`（事件等级 level）(偏移: 0x18)
- `EventOpcode opcode`（事件Opcode opcode）(偏移: 0x1C)
- `EventTags tags`（事件Tags tags）(偏移: 0x20)
- `Type dataType`（类型 data类型）(偏移: 0x24)

### 方法 (7)

- `string get_Name()`
  （string get_名称（））
- `EventLevel get_Level()`
  （事件等级 get_等级（））
- `EventOpcode get_Opcode()`
  （事件Opcode get_Opcode（））
- `EventKeywords get_Keywords()`
  （事件Keywords get_Keywords（））
- `EventTags get_Tags()`
  （事件Tags get_Tags（））
- `Type get_DataType()`
  （类型 get_数据类型（））
- `object GetData(object value)`
  （object 获取数据（object value））

---

## TrackAsset（Track资产）

**继承**: PlayableAsset, ISerializationCallbackReceiver, IPropertyPreview, ICurvesOwner（Playable资产, ISerialization回调Receiver, I属性Preview, ICurvesOwner）

### 字段 (19)

- `int m_Version`（int m_Version）(偏移: 0xC)
- `AnimationClip m_AnimClip`（动画弹匣 m_动画弹匣）(偏移: 0x10)
- `TrackAsset.TransientBuildData s_BuildData`（TrackAsset.TransientBuild数据 s_Build数据）(偏移: 0x0)
- `bool m_Locked`（bool m_锁定的）(偏移: 0x14)
- `bool m_Muted`（bool m_Muted）(偏移: 0x15)
- `string m_CustomPlayableFullTypename`（string m_自定义的Playable满Typename）(偏移: 0x18)
- `AnimationClip m_Curves`（动画弹匣 m_Curves）(偏移: 0x1C)
- `PlayableAsset m_Parent`（Playable资产 m_父级）(偏移: 0x20)
- `List<ScriptableObject> m_Children`（List<ScriptableObject> m_Children）(偏移: 0x24)
- `int m_ItemsHash`（int m_ItemsHash）(偏移: 0x28)
- `TimelineClip[] m_ClipsCache`（TimelineClip[] m_Clips缓存）(偏移: 0x2C)
- `DiscreteTime m_Start`（Discrete时间 m_开始）(偏移: 0x30)
- `DiscreteTime m_End`（Discrete时间 m_结束）(偏移: 0x38)
- `bool m_CacheSorted`（bool m_缓存Sorted）(偏移: 0x40)
- `Nullable<bool> m_SupportsNotifications`（Nullable<bool> m_SupportsNotifications）(偏移: 0x41)
- `TrackAsset[] s_EmptyCache`（TrackAsset[] s_空缓存）(偏移: 0x14)
- `IEnumerable<TrackAsset> m_ChildTrackCache`（IEnumerable<TrackAsset> m_子级Track缓存）(偏移: 0x44)
- `List<TimelineClip> m_Clips`（List<TimelineClip> m_Clips）(偏移: 0x48)
- `MarkerList m_Markers`（Marker列表 m_Markers）(偏移: 0x4C)

### 方法 (90)

- `void OnBeforeTrackSerialize()`
  （void OnBeforeTrackSerialize（））
- `void OnAfterTrackDeserialize()`
  （void OnAfterTrackDeserialize（））
- `void OnUpgradeFromVersion(int oldVersion)`
  （void OnUpgradeFromVersion（int oldVersion））
- `void UpgradeToLatestVersion()`
  （void UpgradeToLatestVersion（））
- `void add_OnClipPlayableCreate(Action<TimelineClip, GameObject, Playable> value)`
  （void add_On弹匣Playable创建（Action<Timeline弹匣, 游戏对象, Playable> value））
- `void remove_OnClipPlayableCreate(Action<TimelineClip, GameObject, Playable> value)`
  （void remove_On弹匣Playable创建（Action<Timeline弹匣, 游戏对象, Playable> value））
- `void add_OnTrackAnimationPlayableCreate(Action<TrackAsset, GameObject, Playable> value)`
  （void add_OnTrack动画Playable创建（Action<Track资产, 游戏对象, Playable> value））
- `void remove_OnTrackAnimationPlayableCreate(Action<TrackAsset, GameObject, Playable> value)`
  （void remove_OnTrack动画Playable创建（Action<Track资产, 游戏对象, Playable> value））
- `double get_start()`
  （double get_start（））
- `double get_end()`
  （double get_end（））
- `bool get_muted()`
  （bool get_muted（））
- `void set_muted(bool value)`
  （void set_muted（bool value））
- `bool get_mutedInHierarchy()`
  （bool get_mutedInHierarchy（））
- `TimelineAsset get_timelineAsset()`
  （Timeline资产 get_timeline资产（））
- `PlayableAsset get_parent()`
  （Playable资产 get_parent（））
- `void set_parent(PlayableAsset value)`
  （void set_parent（Playable资产 value））
- `IEnumerable<TimelineClip> GetClips()`
  （IEnumerable<TimelineClip> 获取Clips（））
- `TimelineClip[] get_clips()`
  （TimelineClip[] get_clips（））
- `bool get_isEmpty()`
  （bool get_is空（））
- `bool get_hasClips()`
  （bool get_hasClips（））
- `bool get_hasCurves()`
  （bool get_hasCurves（））
- `bool get_isSubTrack()`
  （bool get_is子Track（））
- `IEnumerable<PlayableBinding> get_outputs()`
  （IEnumerable<PlayableBinding> get_outputs（））
- `IEnumerable<TrackAsset> GetChildTracks()`
  （IEnumerable<TrackAsset> 获取子级Tracks（））
- `string get_customPlayableTypename()`
  （string get_customPlayableTypename（））
- `void set_customPlayableTypename(string value)`
  （void set_customPlayableTypename（string value））
- `AnimationClip get_curves()`
  （动画弹匣 get_curves（））
- `void set_curves(AnimationClip value)`
  （void set_curves（动画弹匣 value））
- `List<ScriptableObject> get_subTracksObjects()`
  （List<ScriptableObject> get_subTracksObjects（））
- `bool get_locked()`
  （bool get_locked（））
- `void set_locked(bool value)`
  （void set_locked（bool value））
- `bool get_lockedInHierarchy()`
  （bool get_lockedInHierarchy（））
- `bool get_supportsNotifications()`
  （bool get_supportsNotifications（））
- `void __internalAwake()`
  （void __internalAwake（））
- `void CreateCurves(string curvesClipName)`
  （void 创建Curves（string curvesClipName））
- `Playable CreateTrackMixer(PlayableGraph graph, GameObject go, int inputCount)`
  （Playable 创建TrackMixer（PlayableGraph graph, 游戏对象 go, int inputCount））
- `TimelineClip CreateDefaultClip()`
  （Timeline弹匣 创建默认的弹匣（））
- `bool DeleteClip(TimelineClip clip)`
  （bool Delete弹匣（Timeline弹匣 clip））
- `IMarker CreateMarker(Type type, double time)`
  （IMarker 创建Marker（类型 type, double time））
- `bool DeleteMarker(IMarker marker)`
  （bool DeleteMarker（IMarker marker））
- `IEnumerable<IMarker> GetMarkers()`
  （IEnumerable<IMarker> 获取Markers（））
- `int GetMarkerCount()`
  （int 获取Marker数量（））
- `IMarker GetMarker(int idx)`
  （IMarker 获取Marker（int idx））
- `TimelineClip CreateClip(Type requestedType)`
  （Timeline弹匣 创建弹匣（类型 requestedType））
- `TimelineClip CreateAndAddNewClipOfType(Type requestedType)`
  （Timeline弹匣 创建And添加新的弹匣Of类型（类型 requestedType））
- `TimelineClip CreateClipOfType(Type requestedType)`
  （Timeline弹匣 创建弹匣Of类型（类型 requestedType））
- `TimelineClip CreateClipFromPlayableAsset(IPlayableAsset asset)`
  （Timeline弹匣 创建弹匣FromPlayable资产（IPlayable资产 asset））
- `TimelineClip CreateClipFromAsset(ScriptableObject playableAsset)`
  （Timeline弹匣 创建弹匣From资产（脚本对象 playableAsset））
- `IEnumerable<ScriptableObject> GetMarkersRaw()`
  （IEnumerable<ScriptableObject> 获取MarkersRaw（））
- `void ClearMarkers()`
  （void 清除Markers（））
- `void AddMarker(ScriptableObject e)`
  （void 添加Marker（脚本对象 e））
- `bool DeleteMarkerRaw(ScriptableObject marker)`
  （bool DeleteMarkerRaw（脚本对象 marker））
- `int GetTimeRangeHash()`
  （int 获取时间范围Hash（））
- `void AddClip(TimelineClip newClip)`
  （void 添加弹匣（Timeline弹匣 newClip））
- `Playable CreateNotificationsPlayable(PlayableGraph graph, Playable mixerPlayable, GameObject go, Playable timelinePlayable)`
  （Playable 创建NotificationsPlayable（PlayableGraph graph, Playable mixerPlayable, 游戏对象 go, Playable timelinePlayable））
- `Playable CreatePlayableGraph(PlayableGraph graph, GameObject go, IntervalTree<RuntimeElement> tree, Playable timelinePlayable)`
  （Playable 创建PlayableGraph（PlayableGraph graph, 游戏对象 go, 间隔Tree<RuntimeElement> tree, Playable timelinePlayable））
- `Playable CompileClips(PlayableGraph graph, GameObject go, IList<TimelineClip> timelineClips, IntervalTree<RuntimeElement> tree)`
  （Playable CompileClips（PlayableGraph graph, 游戏对象 go, IList<TimelineClip> timelineClips, 间隔Tree<RuntimeElement> tree））
- `void GatherCompilableTracks(IList<TrackAsset> tracks)`
  （void GatherCompilableTracks（IList<TrackAsset> tracks））
- `void GatherNotificiations(List<IMarker> markers)`
  （void GatherNotificiations（List<IMarker> markers））
- `Playable OnCreateClipPlayableGraph(PlayableGraph graph, GameObject go, IntervalTree<RuntimeElement> tree)`
  （Playable On创建弹匣PlayableGraph（PlayableGraph graph, 游戏对象 go, 间隔Tree<RuntimeElement> tree））
- `void ConfigureTrackAnimation(IntervalTree<RuntimeElement> tree, GameObject go, Playable blend)`
  （void ConfigureTrack动画（间隔Tree<RuntimeElement> tree, 游戏对象 go, Playable blend））
- `void SortClips()`
  （void SortClips（））
- `void ClearClipsInternal()`
  （void 清除Clips内部的（））
- `void ClearSubTracksInternal()`
  （void 清除子Tracks内部的（））
- `void OnClipMove()`
  （void On弹匣移动（））
- `TimelineClip CreateNewClipContainerInternal()`
  （Timeline弹匣 创建新的弹匣容器内部的（））
- `void AddChild(TrackAsset child)`
  （void 添加子级（Track资产 child））
- `void MoveLastTrackBefore(TrackAsset asset)`
  （void 移动最后一个TrackBefore（Track资产 asset））
- `bool RemoveSubTrack(TrackAsset child)`
  （bool 移除子Track（Track资产 child））
- `void RemoveClip(TimelineClip clip)`
  （void 移除弹匣（Timeline弹匣 clip））
- `void GetEvaluationTime(out double outStart, out double outDuration)`
  （void 获取Evaluation时间（out double outStart, out double outDuration））
- `void GetSequenceTime(out double outStart, out double outDuration)`
  （void 获取Sequence时间（out double outStart, out double outDuration））
- `void GatherProperties(PlayableDirector director, IPropertyCollector driver)`
  （void GatherProperties（PlayableDirector director, I属性Collector driver））
- `GameObject GetGameObjectBinding(PlayableDirector director)`
  （游戏对象 获取游戏对象Binding（PlayableDirector director））
- `bool ValidateClipType(Type clipType)`
  （bool 验证弹匣类型（类型 clipType））
- `void OnCreateClip(TimelineClip clip)`
  （void On创建弹匣（Timeline弹匣 clip））
- `void UpdateDuration()`
  （void 更新持续时间（））
- `int CalculateItemsHash()`
  （int 计算ItemsHash（））
- `Playable CreatePlayable(PlayableGraph graph, GameObject gameObject, TimelineClip clip)`
  （Playable 创建Playable（PlayableGraph graph, 游戏对象 gameObject, Timeline弹匣 clip））
- `void Invalidate()`
  （void Invalidate（））
- `double GetNotificationDuration()`
  （double 获取Notification持续时间（））
- `bool CanCompileClips()`
  （bool 能否CompileClips（））
- `bool IsCompilable()`
  （bool 是否Compilable（））
- `void UpdateChildTrackCache()`
  （void 更新子级Track缓存（））
- `int Hash()`
  （int Hash（））
- `int GetClipsHash()`
  （int 获取ClipsHash（））
- `int GetAnimationClipHash(AnimationClip clip)`
  （int 获取动画弹匣Hash（动画弹匣 clip））
- `bool HasNotifications()`
  （bool 是否有Notifications（））
- `bool CanCompileNotifications()`
  （bool 能否CompileNotifications（））
- `bool CanCompileClipsRecursive()`
  （bool 能否CompileClipsRecursive（））

---

## TrackAsset.TransientBuildData（TrackAsset.TransientBuild数据）

### 字段 (3)

- `List<TrackAsset> trackList`（List<TrackAsset> track列表）(偏移: 0x0)
- `List<TimelineClip> clipList`（List<TimelineClip> clip列表）(偏移: 0x4)
- `List<IMarker> markerList`（List<IMarker> marker列表）(偏移: 0x8)

### 方法 (2)

- `TrackAsset.TransientBuildData Create()`
  （TrackAsset.TransientBuild数据 创建（））
- `void Clear()`
  （void 清除（））

---

## TrackBindingFlags（TrackBindingFlags）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TrackBindingTypeAttribute（TrackBinding类型Attribute）

**继承**: Attribute（Attribute）

### 字段 (2)

- `Type type`（类型 type）(偏移: 0x8)
- `TrackBindingFlags flags`（TrackBindingFlags flags）(偏移: 0xC)

---

## TrackClipTypeAttribute（Track弹匣类型Attribute）

**继承**: Attribute（Attribute）

### 字段 (2)

- `Type inspectedType`（类型 inspected类型）(偏移: 0x8)
- `bool allowAutoCreate`（bool allow自动创建）(偏移: 0xC)

---

## TrackColorAttribute（Track颜色Attribute）

**继承**: Attribute（Attribute）

### 字段 (1)

- `Color m_Color`（颜色 m_颜色）(偏移: 0x8)

---

## TrackOffset（TrackOffset）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TrackedReference（Tracked引用）

### 字段 (1)

- `IntPtr m_Ptr`（整数Ptr m_Ptr）(偏移: 0x8)

### 方法 (3)

- `bool op_Equality(TrackedReference x, TrackedReference y)`
  （bool op_Equality（Tracked引用 x, Tracked引用 y））
- `bool Equals(object o)`
  （bool Equals（object o））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## TrackingServices（TrackingServices）

### 字段 (1)

- `ArrayList _handlers`（数组列表 _handlers）(偏移: 0x0)

### 方法 (3)

- `void NotifyMarshaledObject(object obj, ObjRef or)`
  （void NotifyMarshaled对象（object obj, ObjRef or））
- `void NotifyUnmarshaledObject(object obj, ObjRef or)`
  （void NotifyUnmarshaled对象（object obj, ObjRef or））
- `void NotifyDisconnectedObject(object obj)`
  （void NotifyDisconnected对象（object obj））

---

## TrailRenderer（Trail渲染器）

**继承**: Renderer（渲染器）

### 方法 (7)

- `float get_time()`
  （float get_time（））
- `void set_time(float value)`
  （void set_time（float value））
- `float get_startWidth()`
  （float get_start宽度（））
- `void set_startWidth(float value)`
  （void set_start宽度（float value））
- `float get_endWidth()`
  （float get_end宽度（））
- `void set_endWidth(float value)`
  （void set_end宽度（float value））
- `void Clear()`
  （void 清除（））

---

## Transform（变换）

**继承**: Component, IEnumerable（组件, IEnumerable）

### 方法 (77)

- `Vector3 get_position()`
  （三维向量 get_position（））
- `void set_position(Vector3 value)`
  （void set_position（三维向量 value））
- `Vector3 get_localPosition()`
  （三维向量 get_localPosition（））
- `void set_localPosition(Vector3 value)`
  （void set_localPosition（三维向量 value））
- `Vector3 get_eulerAngles()`
  （三维向量 get_eulerAngles（））
- `void set_eulerAngles(Vector3 value)`
  （void set_eulerAngles（三维向量 value））
- `Vector3 get_localEulerAngles()`
  （三维向量 get_localEulerAngles（））
- `void set_localEulerAngles(Vector3 value)`
  （void set_localEulerAngles（三维向量 value））
- `Vector3 get_right()`
  （三维向量 get_right（））
- `Vector3 get_up()`
  （三维向量 get_up（））
- `Vector3 get_forward()`
  （三维向量 get_forward（））
- `void set_forward(Vector3 value)`
  （void set_forward（三维向量 value））
- `Quaternion get_rotation()`
  （Quaternion get_rotation（））
- `void set_rotation(Quaternion value)`
  （void set_rotation（Quaternion value））
- `Quaternion get_localRotation()`
  （Quaternion get_localRotation（））
- `void set_localRotation(Quaternion value)`
  （void set_localRotation（Quaternion value））
- `Vector3 get_localScale()`
  （三维向量 get_local缩放（））
- `void set_localScale(Vector3 value)`
  （void set_local缩放（三维向量 value））
- `Transform get_parent()`
  （变换 get_parent（））
- `void set_parent(Transform value)`
  （void set_parent（变换 value））
- `Transform get_parentInternal()`
  （变换 get_parent内部的（））
- `void set_parentInternal(Transform value)`
  （void set_parent内部的（变换 value））
- `Transform GetParent()`
  （变换 获取父级（））
- `void SetParent(Transform p)`
  （void 集合父级（变换 p））
- `void SetParent(Transform parent, bool worldPositionStays)`
  （void 集合父级（变换 parent, bool worldPositionStays））
- `Matrix4x4 get_worldToLocalMatrix()`
  （Matrix4x4 get_worldTo本地的矩阵（））
- `Matrix4x4 get_localToWorldMatrix()`
  （Matrix4x4 get_localTo世界的矩阵（））
- `void SetPositionAndRotation(Vector3 position, Quaternion rotation)`
  （void 集合PositionAndRotation（三维向量 position, Quaternion rotation））
- `void Translate(Vector3 translation, Space relativeTo)`
  （void Translate（三维向量 translation, Space relativeTo））
- `void Rotate(Vector3 eulers, Space relativeTo)`
  （void Rotate（三维向量 eulers, Space relativeTo））
- `void Rotate(float xAngle, float yAngle, float zAngle)`
  （void Rotate（float xAngle, float yAngle, float zAngle））
- `void RotateAroundInternal(Vector3 axis, float angle)`
  （void RotateAround内部的（三维向量 axis, float angle））
- `void RotateAround(Vector3 point, Vector3 axis, float angle)`
  （void RotateAround（三维向量 point, 三维向量 axis, float angle））
- `void LookAt(Transform target, Vector3 worldUp)`
  （void LookAt（变换 target, 三维向量 worldUp））
- `void LookAt(Vector3 worldPosition, Vector3 worldUp)`
  （void LookAt（三维向量 worldPosition, 三维向量 worldUp））
- `void Internal_LookAt(Vector3 worldPosition, Vector3 worldUp)`
  （void Internal_LookAt（三维向量 worldPosition, 三维向量 worldUp））
- `Vector3 TransformDirection(Vector3 direction)`
  （三维向量 变换方向（三维向量 direction））
- `Vector3 InverseTransformDirection(Vector3 direction)`
  （三维向量 Inverse变换方向（三维向量 direction））
- `Vector3 InverseTransformVector(Vector3 vector)`
  （三维向量 Inverse变换向量（三维向量 vector））
- `Vector3 TransformPoint(Vector3 position)`
  （三维向量 变换Point（三维向量 position））
- `Vector3 TransformPoint(float x, float y, float z)`
  （三维向量 变换Point（float x, float y, float z））
- `Vector3 InverseTransformPoint(Vector3 position)`
  （三维向量 Inverse变换Point（三维向量 position））
- `Transform get_root()`
  （变换 get_root（））
- `Transform GetRoot()`
  （变换 获取根（））
- `int get_childCount()`
  （int get_child数量（））
- `void SetAsFirstSibling()`
  （void 集合As第一个Sibling（））
- `void SetAsLastSibling()`
  （void 集合As最后一个Sibling（））
- `void SetSiblingIndex(int index)`
  （void 集合Sibling索引（int index））
- `Transform FindRelativeTransformWithPath(Transform transform, string path, bool isActiveOnly)`
  （变换 查找Relative变换With路径（变换 transform, string path, bool isActiveOnly））
- `Transform Find(string n)`
  （变换 查找（string n））
- `Vector3 get_lossyScale()`
  （三维向量 get_lossy缩放（））
- `bool IsChildOf(Transform parent)`
  （bool 是否子级Of（变换 parent））
- `bool get_hasChanged()`
  （bool get_hasChanged（））
- `void set_hasChanged(bool value)`
  （void set_hasChanged（bool value））
- `IEnumerator GetEnumerator()`
  （IEnumerator 获取Enumerator（））
- `Transform GetChild(int index)`
  （变换 获取子级（int index））
- `void get_position_Injected(out Vector3 ret)`
  （void get_position_Injected（out Vector3 ret））
- `void set_position_Injected(ref Vector3 value)`
  （void set_position_Injected（ref Vector3 value））
- `void get_localPosition_Injected(out Vector3 ret)`
  （void get_localPosition_Injected（out Vector3 ret））
- `void set_localPosition_Injected(ref Vector3 value)`
  （void set_localPosition_Injected（ref Vector3 value））
- `void get_rotation_Injected(out Quaternion ret)`
  （void get_rotation_Injected（out Quaternion ret））
- `void set_rotation_Injected(ref Quaternion value)`
  （void set_rotation_Injected（ref Quaternion value））
- `void get_localRotation_Injected(out Quaternion ret)`
  （void get_localRotation_Injected（out Quaternion ret））
- `void set_localRotation_Injected(ref Quaternion value)`
  （void set_localRotation_Injected（ref Quaternion value））
- `void get_localScale_Injected(out Vector3 ret)`
  （void get_localScale_Injected（out Vector3 ret））
- `void set_localScale_Injected(ref Vector3 value)`
  （void set_localScale_Injected（ref Vector3 value））
- `void get_worldToLocalMatrix_Injected(out Matrix4x4 ret)`
  （void get_worldTo本地的Matrix_Injected（out Matrix4x4 ret））
- `void get_localToWorldMatrix_Injected(out Matrix4x4 ret)`
  （void get_localTo世界的Matrix_Injected（out Matrix4x4 ret））
- `void SetPositionAndRotation_Injected(ref Vector3 position, ref Quaternion rotation)`
  （void 集合PositionAndRotation_Injected（ref Vector3 position, ref Quaternion rotation））
- `void RotateAroundInternal_Injected(ref Vector3 axis, float angle)`
  （void RotateAroundInternal_Injected（ref Vector3 axis, float angle））
- `void Internal_LookAt_Injected(ref Vector3 worldPosition, ref Vector3 worldUp)`
  （void Internal_LookAt_Injected（ref Vector3 worldPosition, ref Vector3 worldUp））
- `void TransformDirection_Injected(ref Vector3 direction, out Vector3 ret)`
  （void 变换Direction_Injected（ref Vector3 direction, out Vector3 ret））
- `void InverseTransformDirection_Injected(ref Vector3 direction, out Vector3 ret)`
  （void Inverse变换Direction_Injected（ref Vector3 direction, out Vector3 ret））
- `void InverseTransformVector_Injected(ref Vector3 vector, out Vector3 ret)`
  （void Inverse变换Vector_Injected（ref Vector3 vector, out Vector3 ret））
- `void TransformPoint_Injected(ref Vector3 position, out Vector3 ret)`
  （void 变换Point_Injected（ref Vector3 position, out Vector3 ret））
- `void InverseTransformPoint_Injected(ref Vector3 position, out Vector3 ret)`
  （void Inverse变换Point_Injected（ref Vector3 position, out Vector3 ret））
- `void get_lossyScale_Injected(out Vector3 ret)`
  （void get_lossyScale_Injected（out Vector3 ret））

---

## Transform.Enumerator（Transform.Enumerator）

**继承**: IEnumerator（IEnumerator）

### 字段 (2)

- `Transform outer`（变换 outer）(偏移: 0x8)
- `int currentIndex`（int current索引）(偏移: 0xC)

### 方法 (3)

- `object get_Current()`
  （object get_当前（））
- `bool MoveNext()`
  （bool 移动下一个（））
- `void Reset()`
  （void 重置（））

---

## TransparencySortMode（TransparencySort模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TransparentBuff（透明的增益）

**继承**: Buff（增益）

### 字段 (2)

- `float cvAlpha`（float cv透明度）(偏移: 0x24)
- `float pvAlpha`（float pv透明度）(偏移: 0x28)

### 方法 (2)

- `void ModelInfo_Getter_Alpha(ref float cv, ref float pv)`
  （void 模型Info_Getter_透明度（ref float cv, ref float pv））
- `void OnLifeEnd()`
  （void OnLife结束（））

---

## TransparentProxy（透明的代理）

### 字段 (3)

- `RealProxy _rp`（Real代理 _rp）(偏移: 0x8)
- `RuntimeRemoteClassHandle _class`（RuntimeRemote类句柄 _class）(偏移: 0xC)
- `bool _custom_type_info`（bool _custom_type_info）(偏移: 0x10)

### 方法 (6)

- `RuntimeType GetProxyType()`
  （Runtime类型 获取代理类型（））
- `bool get_IsContextBoundObject()`
  （bool get_是否ContextBound对象（））
- `Context get_TargetContext()`
  （Context get_目标Context（））
- `bool InCurrentContext()`
  （bool In当前Context（））
- `object LoadRemoteFieldNew(IntPtr classPtr, IntPtr fieldPtr)`
  （object 加载RemoteField新的（整数Ptr classPtr, 整数Ptr fieldPtr））
- `void StoreRemoteField(IntPtr classPtr, IntPtr fieldPtr, object arg)`
  （void 商店RemoteField（整数Ptr classPtr, 整数Ptr fieldPtr, object arg））

---

## TransparentSettingsPass（透明的SettingsPass）

**继承**: ScriptableRenderPass（ScriptableRenderPass）

### 字段 (2)

- `bool m_shouldReceiveShadows`（bool m_should接收Shadows）(偏移: 0x54)
- `ProfilingSampler m_ProfilingSampler`（ProfilingSampler m_ProfilingSampler）(偏移: 0x0)

### 方法 (2)

- `bool Setup(ref RenderingData renderingData)`
  （bool Setup（ref RenderingData renderingData））
- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（ScriptableRenderContext context, ref RenderingData renderingData））

---

## Tree（Tree）

### 字段 (12)

- `int HEAP_SIZE`（int HEAP_SIZE）(偏移: 0x0)
- `int[] ExtraLengthBits`（int[] 额外的LengthBits）(偏移: 0x4)
- `int[] ExtraDistanceBits`（int[] 额外的距离Bits）(偏移: 0x8)
- `int[] extra_blbits`（int[] extra_blbits）(偏移: 0xC)
- `sbyte[] bl_order`（sbyte[] bl_order）(偏移: 0x10)
- `sbyte[] _dist_code`（sbyte[] _dist_code）(偏移: 0x14)
- `sbyte[] LengthCode`（sbyte[] LengthCode）(偏移: 0x18)
- `int[] LengthBase`（int[] Length基础）(偏移: 0x1C)
- `int[] DistanceBase`（int[] 距离基础）(偏移: 0x20)
- `short[] dyn_tree`（short[] dyn_tree）(偏移: 0x8)
- `int max_code`（int max_code）(偏移: 0xC)
- `StaticTree staticTree`（静态的Tree staticTree）(偏移: 0x10)

### 方法 (5)

- `int DistanceCode(int dist)`
  （int 距离Code（int dist））
- `void gen_bitlen(DeflateManager s)`
  （void gen_bitlen（Deflate管理器 s））
- `void build_tree(DeflateManager s)`
  （void build_tree（Deflate管理器 s））
- `void gen_codes(short[] tree, int max_code, short[] bl_count)`
  （void gen_codes（short[] tree, int max_code, short[] bl_count））
- `int bi_reverse(int code, int len)`
  （int bi_reverse（int code, int len））

---

## TreeInstance（Tree实例）

### 字段 (8)

- `Vector3 position`（三维向量 position）(偏移: 0x0)
- `float widthScale`（float width缩放）(偏移: 0xC)
- `float heightScale`（float height缩放）(偏移: 0x10)
- `float rotation`（float rotation）(偏移: 0x14)
- `Color32 color`（Color32 color）(偏移: 0x18)
- `Color32 lightmapColor`（Color32 lightmap颜色）(偏移: 0x1C)
- `int prototypeIndex`（int prototype索引）(偏移: 0x20)
- `float temporaryDistance`（float temporary距离）(偏移: 0x24)

---

## TreePrototype（TreePrototype）

### 字段 (3)

- `GameObject m_Prefab`（游戏对象 m_预制体）(偏移: 0x8)
- `float m_BendFactor`（float m_Bend系数）(偏移: 0xC)
- `int m_NavMeshLod`（int m_Nav网格Lod）(偏移: 0x10)

### 方法 (6)

- `GameObject get_prefab()`
  （游戏对象 get_prefab（））
- `float get_bendFactor()`
  （float get_bend系数（））
- `int get_navMeshLod()`
  （int get_nav网格Lod（））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool Equals(TreePrototype other)`
  （bool Equals（TreePrototype other））

---

## TriangleMeshNode（Triangle网格节点）

**继承**: MeshNode（网格节点）

### 字段 (5)

- `int v0`（int v0）(偏移: 0x24)
- `int v1`（int v1）(偏移: 0x28)
- `int v2`（int v2）(偏移: 0x2C)
- `INavmeshHolder[] _navmeshHolders`（INavmeshHolder[] _navmeshHolders）(偏移: 0x0)
- `object lockObject`（object lock对象）(偏移: 0x4)

### 方法 (24)

- `INavmeshHolder GetNavmeshHolder(uint graphIndex)`
  （INavmeshHolder 获取NavmeshHolder（uint graphIndex））
- `void SetNavmeshHolder(int graphIndex, INavmeshHolder graph)`
  （void 集合NavmeshHolder（int graphIndex, INavmeshHolder graph））
- `void UpdatePositionFromVertices()`
  （void 更新PositionFromVertices（））
- `int GetVertexIndex(int i)`
  （int 获取Vertex索引（int i））
- `int GetVertexArrayIndex(int i)`
  （int 获取Vertex数组索引（int i））
- `void GetVertices(out Int3 v0, out Int3 v1, out Int3 v2)`
  （void 获取Vertices（out Int3 v0, out Int3 v1, out Int3 v2））
- `void GetVerticesInGraphSpace(out Int3 v0, out Int3 v1, out Int3 v2)`
  （void 获取VerticesInGraphSpace（out Int3 v0, out Int3 v1, out Int3 v2））
- `Int3 GetVertex(int i)`
  （Int3 获取Vertex（int i））
- `Int3 GetVertexInGraphSpace(int i)`
  （Int3 获取VertexInGraphSpace（int i））
- `int GetVertexCount()`
  （int 获取Vertex数量（））
- `Vector3 ClosestPointOnNode(Vector3 p)`
  （三维向量 ClosestPointOn节点（三维向量 p））
- `Int3 ClosestPointOnNodeXZInGraphSpace(Vector3 p)`
  （Int3 ClosestPointOn节点XZInGraphSpace（三维向量 p））
- `Vector3 ClosestPointOnNodeXZ(Vector3 p)`
  （三维向量 ClosestPointOn节点XZ（三维向量 p））
- `bool ContainsPoint(Vector3 p)`
  （bool ContainsPoint（三维向量 p））
- `bool ContainsPointInGraphSpace(Int3 p)`
  （bool ContainsPointInGraphSpace（Int3 p））
- `void UpdateRecursiveG(Path path, PathNode pathNode, PathHandler handler)`
  （void 更新RecursiveG（路径 path, 路径节点 pathNode, 路径处理器 handler））
- `void Open(Path path, PathNode pathNode, PathHandler handler)`
  （void 打开（路径 path, 路径节点 pathNode, 路径处理器 handler））
- `int SharedEdge(GraphNode other)`
  （int SharedEdge（Graph节点 other））
- `bool GetPortal(GraphNode toNode, List<Vector3> left, List<Vector3> right, bool backwards)`
  （bool 获取Portal（Graph节点 toNode, List<Vector3> left, List<Vector3> right, bool backwards））
- `bool GetPortal(GraphNode toNode, List<Vector3> left, List<Vector3> right, bool backwards, out int aIndex, out int bIndex)`
  （bool 获取Portal（Graph节点 toNode, List<Vector3> left, List<Vector3> right, bool backwards, out int aIndex, out int bIndex））
- `float SurfaceArea()`
  （float SurfaceArea（））
- `Vector3 RandomPointOnSurface()`
  （三维向量 随机PointOnSurface（））
- `void SerializeNode(GraphSerializationContext ctx)`
  （void Serialize节点（GraphSerializationContext ctx））
- `void DeserializeNode(GraphSerializationContext ctx)`
  （void Deserialize节点（GraphSerializationContext ctx））

---

## TriangulationAlgorithm（TriangulationAlgorithm）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TriangulationConstraint（TriangulationConstraint）

### 字段 (2)

- `TriangulationPoint P`（TriangulationPoint P）(偏移: 0x8)
- `TriangulationPoint Q`（TriangulationPoint Q）(偏移: 0xC)

---

## TriangulationContext（TriangulationContext）

### 字段 (2)

- `List<DelaunayTriangle> Triangles`（List<DelaunayTriangle> Triangles）(偏移: 0x8)
- `List<TriangulationPoint> Points`（List<TriangulationPoint> Points）(偏移: 0xC)

### 方法 (13)

- `TriangulationDebugContext get_DebugContext()`
  （TriangulationDebugContext get_DebugContext（））
- `TriangulationMode get_TriangulationMode()`
  （Triangulation模式 get_Triangulation模式（））
- `void set_TriangulationMode(TriangulationMode value)`
  （void set_Triangulation模式（Triangulation模式 value））
- `Triangulatable get_Triangulatable()`
  （Triangulatable get_Triangulatable（））
- `void set_Triangulatable(Triangulatable value)`
  （void set_Triangulatable（Triangulatable value））
- `int get_StepCount()`
  （int get_Step数量（））
- `void set_StepCount(int value)`
  （void set_Step数量（int value））
- `void Done()`
  （void Done（））
- `void PrepareTriangulation(Triangulatable t)`
  （void PrepareTriangulation（Triangulatable t））
- `void Update(string message)`
  （void 更新（string message））
- `void Clear()`
  （void 清除（））
- `bool get_IsDebugEnabled()`
  （bool get_是否Debug启用的（））
- `DTSweepDebugContext get_DTDebugContext()`
  （DTSweepDebugContext get_DTDebugContext（））

---

## TriangulationDebugContext（TriangulationDebugContext）

### 字段 (1)

- `TriangulationContext _tcx`（TriangulationContext _tcx）(偏移: 0x8)

---

## TriangulationMode（Triangulation模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TriangulationPoint（TriangulationPoint）

### 字段 (2)

- `double X`（double X）(偏移: 0x8)
- `double Y`（double Y）(偏移: 0x10)

### 方法 (5)

- `List<DTSweepConstraint> get_Edges()`
  （List<DTSweepConstraint> get_Edges（））
- `void set_Edges(List<DTSweepConstraint> value)`
  （void set_Edges（List<DTSweepConstraint> value））
- `string ToString()`
  （string To字符串（））
- `void AddEdge(DTSweepConstraint e)`
  （void 添加Edge（DTSweepConstraint e））
- `bool get_HasEdges()`
  （bool get_是否有Edges（））

---

## TriangulationUtil（TriangulationUtil）

### 字段 (1)

- `double EPSILON`（double EPSILON）(偏移: 0x31563137)

### 方法 (3)

- `bool SmartIncircle(TriangulationPoint pa, TriangulationPoint pb, TriangulationPoint pc, TriangulationPoint pd)`
  （bool SmartIncircle（TriangulationPoint pa, TriangulationPoint pb, TriangulationPoint pc, TriangulationPoint pd））
- `bool InScanArea(TriangulationPoint pa, TriangulationPoint pb, TriangulationPoint pc, TriangulationPoint pd)`
  （bool InScanArea（TriangulationPoint pa, TriangulationPoint pb, TriangulationPoint pc, TriangulationPoint pd））
- `Orientation Orient2d(TriangulationPoint pa, TriangulationPoint pb, TriangulationPoint pc)`
  （Orientation Orient2d（TriangulationPoint pa, TriangulationPoint pb, TriangulationPoint pc））

---

## TriggerEnterSound（触发器Enter音效）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (1)

- `AudioClip sound`（音频弹匣 sound）(偏移: 0xC)

### 方法 (1)

- `void OnTriggerEnter(Collider other)`
  （void On触发器Enter（碰撞器 other））

---

## TriggerEventBroadcaster（触发器事件Broadcaster）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (1)

- `GameObject target`（游戏对象 target）(偏移: 0xC)

### 方法 (3)

- `void OnTriggerEnter(Collider collider)`
  （void On触发器Enter（碰撞器 collider））
- `void OnTriggerStay(Collider collider)`
  （void On触发器Stay（碰撞器 collider））
- `void OnTriggerExit(Collider collider)`
  （void On触发器Exit（碰撞器 collider））

---

## TrigonometricIK（TrigonometricIK）

**继承**: IK（IK）

### 字段 (1)

- `IKSolverTrigonometric solver`（IKSolverTrigonometric solver）(偏移: 0x1C)

### 方法 (5)

- `void OpenUserManual()`
  （void 打开User手动（））
- `void OpenScriptReference()`
  （void 打开Script引用（））
- `void SupportGroup()`
  （void Support组（））
- `void ASThread()`
  （void ASThread（））
- `IKSolver GetIKSolver()`
  （IKSolver 获取IKSolver（））

---

## TripleDES（TripleDES）

**继承**: SymmetricAlgorithm（SymmetricAlgorithm）

### 字段 (2)

- `KeySizes[] s_legalBlockSizes`（键Sizes[] s_legalBlockSizes）(偏移: 0x0)
- `KeySizes[] s_legalKeySizes`（键Sizes[] s_legal键Sizes）(偏移: 0x4)

### 方法 (6)

- `byte[] get_Key()`
  （byte[] get_键（））
- `void set_Key(byte[] value)`
  （void set_键（byte[] value））
- `TripleDES Create()`
  （TripleDES 创建（））
- `bool IsWeakKey(byte[] rgbKey)`
  （bool 是否Weak键（byte[] rgbKey））
- `bool EqualBytes(byte[] rgbKey, int start1, int start2, int count)`
  （bool EqualBytes（byte[] rgbKey, int start1, int start2, int count））
- `bool IsLegalKeySize(byte[] rgbKey)`
  （bool 是否Legal键大小（byte[] rgbKey））

---

## TripleDESCryptoServiceProvider（TripleDESCrypto服务提供者）

**继承**: TripleDES（TripleDES）

### 方法 (4)

- `ICryptoTransform CreateEncryptor(byte[] rgbKey, byte[] rgbIV)`
  （ICrypto变换 创建Encryptor（byte[] rgbKey, byte[] rgbIV））
- `ICryptoTransform CreateDecryptor(byte[] rgbKey, byte[] rgbIV)`
  （ICrypto变换 创建Decryptor（byte[] rgbKey, byte[] rgbIV））
- `void GenerateKey()`
  （void Generate键（））
- `void GenerateIV()`
  （void GenerateIV（））

---

## TripleDESTransform（TripleDES变换）

**继承**: SymmetricTransform（Symmetric变换）

### 字段 (6)

- `DESTransform E1`（DES变换 E1）(偏移: 0x34)
- `DESTransform D2`（DES变换 D2）(偏移: 0x38)
- `DESTransform E3`（DES变换 E3）(偏移: 0x3C)
- `DESTransform D1`（DES变换 D1）(偏移: 0x40)
- `DESTransform E2`（DES变换 E2）(偏移: 0x44)
- `DESTransform D3`（DES变换 D3）(偏移: 0x48)

### 方法 (2)

- `void ECB(byte[] input, byte[] output)`
  （void ECB（byte[] input, byte[] output））
- `byte[] GetStrongKey()`
  （byte[] 获取Strong键（））

---

## Tuple（Tuple）

### 方法 (2)

- `int CombineHashCodes(int h1, int h2)`
  （int CombineHashCodes（int h1, int h2））
- `int CombineHashCodes(int h1, int h2, int h3)`
  （int CombineHashCodes（int h1, int h2, int h3））

---

## TupleElementNamesAttribute（Tuple元素NamesAttribute）

**继承**: Attribute（Attribute）

### 字段 (1)

- `string[] _transformNames`（string[] _transformNames）(偏移: 0x8)

---

## TurnBasedAI（TurnBasedAI）

**继承**: VersionedMonoBehaviour（VersionedMonoBehaviour）

### 字段 (5)

- `int movementPoints`（int movementPoints）(偏移: 0x10)
- `BlockManager blockManager`（Block管理器 block管理器）(偏移: 0x14)
- `SingleNodeBlocker blocker`（单个节点Blocker blocker）(偏移: 0x18)
- `GraphNode targetNode`（Graph节点 target节点）(偏移: 0x1C)
- `BlockManager.TraversalProvider traversalProvider`（BlockManager.Traversal提供者 traversal提供者）(偏移: 0x20)

### 方法 (2)

- `void Start()`
  （void 开始（））
- `void Awake()`
  （void Awake（））

---

## Tween（Tween）

**继承**: ABSSequentiable（ABSSequentiable）

### 字段 (47)

- `float timeScale`（float time缩放）(偏移: 0x18)
- `bool isBackwards`（bool isBackwards）(偏移: 0x1C)
- `bool isInverted`（bool isInverted）(偏移: 0x1D)
- `object id`（object id）(偏移: 0x20)
- `string stringId`（string stringId）(偏移: 0x24)
- `int intId`（int intId）(偏移: 0x28)
- `object target`（object target）(偏移: 0x2C)
- `UpdateType updateType`（更新类型 update类型）(偏移: 0x30)
- `bool isIndependentUpdate`（bool isIndependent更新）(偏移: 0x34)
- `TweenCallback onPlay`（Tween回调 on播放）(偏移: 0x38)
- `TweenCallback onPause`（Tween回调 on暂停）(偏移: 0x3C)
- `TweenCallback onRewind`（Tween回调 onRewind）(偏移: 0x40)
- `TweenCallback onUpdate`（Tween回调 on更新）(偏移: 0x44)
- `TweenCallback onStepComplete`（Tween回调 onStepComplete）(偏移: 0x48)
- `TweenCallback onComplete`（Tween回调 onComplete）(偏移: 0x4C)
- `TweenCallback onKill`（Tween回调 on击杀）(偏移: 0x50)
- `TweenCallback<int> onWaypointChange`（TweenCallback<int> onWaypointChange）(偏移: 0x54)
- `bool isFrom`（bool isFrom）(偏移: 0x58)
- `bool isBlendable`（bool isBlendable）(偏移: 0x0)
- `bool isRecyclable`（bool isRecyclable）(偏移: 0x0)
- `bool isSpeedBased`（bool isSpeedBased）(偏移: 0x0)
- `bool autoKill`（bool auto击杀）(偏移: 0x0)
- `float duration`（float duration）(偏移: 0x60)
- `int loops`（int loops）(偏移: 0x64)
- `LoopType loopType`（Loop类型 loop类型）(偏移: 0x68)
- `float delay`（float delay）(偏移: 0x6C)
- `Ease easeType`（Ease ease类型）(偏移: 0x74)
- `EaseFunction customEase`（EaseFunction customEase）(偏移: 0x78)
- `float easeOvershootOrAmplitude`（float easeOvershootOrAmplitude）(偏移: 0x7C)
- `float easePeriod`（float easePeriod）(偏移: 0x80)
- `string debugTargetId`（string debug目标Id）(偏移: 0x84)
- `Type typeofT1`（类型 typeofT1）(偏移: 0x88)
- `Type typeofT2`（类型 typeofT2）(偏移: 0x8C)
- `Type typeofTPlugOptions`（类型 typeofTPlugOptions）(偏移: 0x90)
- `bool isSequenced`（bool isSequenced）(偏移: 0x95)
- `Sequence sequenceParent`（Sequence sequence父级）(偏移: 0x98)
- `int activeId`（int activeId）(偏移: 0x9C)
- `SpecialStartupMode specialStartupMode`（特殊Startup模式 specialStartup模式）(偏移: 0xA0)
- `bool creationLocked`（bool creation锁定的）(偏移: 0xA4)
- `bool startupDone`（bool startupDone）(偏移: 0xA5)
- `float fullDuration`（float full持续时间）(偏移: 0xAC)
- `int completedLoops`（int completedLoops）(偏移: 0xB0)
- `bool isPlaying`（bool isPlaying）(偏移: 0xB4)
- `bool isComplete`（bool isComplete）(偏移: 0xB5)
- `float elapsedDelay`（float elapsed延迟）(偏移: 0xB8)
- `bool delayComplete`（bool delayComplete）(偏移: 0xBC)
- `int miscInt`（int misc整数）(偏移: 0xC0)

### 方法 (15)

- `bool get_isRelative()`
  （bool get_isRelative（））
- `void set_isRelative(bool value)`
  （void set_isRelative（bool value））
- `bool get_active()`
  （bool get_active（））
- `void set_active(bool value)`
  （void set_active（bool value））
- `float get_fullPosition()`
  （float get_fullPosition（））
- `void set_fullPosition(float value)`
  （void set_fullPosition（float value））
- `bool get_hasLoops()`
  （bool get_hasLoops（））
- `bool get_playedOnce()`
  （bool get_playedOnce（））
- `void set_playedOnce(bool value)`
  （void set_playedOnce（bool value））
- `float get_position()`
  （float get_position（））
- `void set_position(float value)`
  （void set_position（float value））
- `void Reset()`
  （void 重置（））
- `float UpdateDelay(float elapsed)`
  （float 更新延迟（float elapsed））
- `bool DoGoto(Tween t, float toPosition, int toCompletedLoops, UpdateMode updateMode)`
  （bool DoGoto（Tween t, float toPosition, int toCompletedLoops, 更新模式 updateMode））
- `bool OnTweenCallback(TweenCallback callback, Tween t)`
  （bool OnTween回调（Tween回调 callback, Tween t））

---

## TweenCallback（Tween回调）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke()`
  （void Invoke（））
- `IAsyncResult BeginInvoke(AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## TweenExtensions（TweenExtensions）

### 方法 (38)

- `void Complete(Tween t)`
  （void Complete（Tween t））
- `void Complete(Tween t, bool withCallbacks)`
  （void Complete（Tween t, bool withCallbacks））
- `void Flip(Tween t)`
  （void Flip（Tween t））
- `void ForceInit(Tween t)`
  （void 强制初始化（Tween t））
- `void Goto(Tween t, float to, bool andPlay = False)`
  （void Goto（Tween t, float to, bool andPlay = False））
- `void GotoWithCallbacks(Tween t, float to, bool andPlay = False)`
  （void GotoWithCallbacks（Tween t, float to, bool andPlay = False））
- `void DoGoto(Tween t, float to, bool andPlay, bool withCallbacks)`
  （void DoGoto（Tween t, float to, bool andPlay, bool withCallbacks））
- `void Kill(Tween t, bool complete = False)`
  （void 击杀（Tween t, bool complete = False））
- `void ManualUpdate(Tween t, float deltaTime, float unscaledDeltaTime)`
  （void 手动更新（Tween t, float deltaTime, float unscaledDeltaTime））
- `void PlayBackwards(Tween t)`
  （void 播放Backwards（Tween t））
- `void PlayForward(Tween t)`
  （void 播放前进（Tween t））
- `void Restart(Tween t, bool includeDelay = True, float changeDelayTo = -1)`
  （void Restart（Tween t, bool includeDelay = True, float changeDelayTo = -1））
- `void Rewind(Tween t, bool includeDelay = True)`
  （void Rewind（Tween t, bool includeDelay = True））
- `void SmoothRewind(Tween t)`
  （void SmoothRewind（Tween t））
- `void TogglePause(Tween t)`
  （void 开关暂停（Tween t））
- `void GotoWaypoint(Tween t, int waypointIndex, bool andPlay = False)`
  （void GotoWaypoint（Tween t, int waypointIndex, bool andPlay = False））
- `YieldInstruction WaitForCompletion(Tween t)`
  （YieldInstruction WaitForCompletion（Tween t））
- `YieldInstruction WaitForRewind(Tween t)`
  （YieldInstruction WaitForRewind（Tween t））
- `YieldInstruction WaitForKill(Tween t)`
  （YieldInstruction WaitFor击杀（Tween t））
- `YieldInstruction WaitForElapsedLoops(Tween t, int elapsedLoops)`
  （YieldInstruction WaitForElapsedLoops（Tween t, int elapsedLoops））
- `YieldInstruction WaitForPosition(Tween t, float position)`
  （YieldInstruction WaitForPosition（Tween t, float position））
- `Coroutine WaitForStart(Tween t)`
  （协程 WaitFor开始（Tween t））
- `int CompletedLoops(Tween t)`
  （int CompletedLoops（Tween t））
- `float Delay(Tween t)`
  （float 延迟（Tween t））
- `float ElapsedDelay(Tween t)`
  （float Elapsed延迟（Tween t））
- `float Duration(Tween t, bool includeLoops = True)`
  （float 持续时间（Tween t, bool includeLoops = True））
- `float Elapsed(Tween t, bool includeLoops = True)`
  （float Elapsed（Tween t, bool includeLoops = True））
- `float ElapsedPercentage(Tween t, bool includeLoops = True)`
  （float ElapsedPercentage（Tween t, bool includeLoops = True））
- `float ElapsedDirectionalPercentage(Tween t)`
  （float ElapsedDirectionalPercentage（Tween t））
- `bool IsActive(Tween t)`
  （bool 是否激活的（Tween t））
- `bool IsBackwards(Tween t)`
  （bool 是否Backwards（Tween t））
- `bool IsComplete(Tween t)`
  （bool 是否Complete（Tween t））
- `bool IsInitialized(Tween t)`
  （bool 是否Initialized（Tween t））
- `bool IsPlaying(Tween t)`
  （bool 是否Playing（Tween t））
- `int Loops(Tween t)`
  （int Loops（Tween t））
- `Vector3 PathGetPoint(Tween t, float pathPercentage)`
  （三维向量 路径获取Point（Tween t, float pathPercentage））
- `Vector3[] PathGetDrawPoints(Tween t, int subdivisionsXSegment = 10)`
  （Vector3[] 路径获取DrawPoints（Tween t, int subdivisionsXSegment = 10））
- `float PathLength(Tween t)`
  （float 路径Length（Tween t））

---

## TweenLink（TweenLink）

### 字段 (3)

- `GameObject target`（游戏对象 target）(偏移: 0x8)
- `LinkBehaviour behaviour`（LinkBehaviour behaviour）(偏移: 0xC)
- `bool lastSeenActive`（bool lastSeen激活的）(偏移: 0x10)

---

## TweenManager（Tween管理器）

### 字段 (33)

- `bool isUnityEditor`（bool isUnity引擎Editor）(偏移: 0x0)
- `bool isDebugBuild`（bool isDebugBuild）(偏移: 0x1)
- `int maxActive`（int max激活的）(偏移: 0x4)
- `int maxTweeners`（int maxTweeners）(偏移: 0x8)
- `int maxSequences`（int maxSequences）(偏移: 0xC)
- `bool hasActiveTweens`（bool has激活的Tweens）(偏移: 0x10)
- `bool hasActiveDefaultTweens`（bool has激活的默认的Tweens）(偏移: 0x0)
- `bool hasActiveLateTweens`（bool has激活的延迟Tweens）(偏移: 0x0)
- `bool hasActiveFixedTweens`（bool has激活的固定Tweens）(偏移: 0x0)
- `bool hasActiveManualTweens`（bool has激活的手动Tweens）(偏移: 0x0)
- `int totActiveTweens`（int tot激活的Tweens）(偏移: 0x18)
- `int totActiveDefaultTweens`（int tot激活的默认的Tweens）(偏移: 0x1C)
- `int totActiveLateTweens`（int tot激活的延迟Tweens）(偏移: 0x20)
- `int totActiveFixedTweens`（int tot激活的固定Tweens）(偏移: 0x24)
- `int totActiveManualTweens`（int tot激活的手动Tweens）(偏移: 0x28)
- `int totActiveTweeners`（int tot激活的Tweeners）(偏移: 0x2C)
- `int totActiveSequences`（int tot激活的Sequences）(偏移: 0x30)
- `int totPooledTweeners`（int totPooledTweeners）(偏移: 0x34)
- `int totPooledSequences`（int totPooledSequences）(偏移: 0x38)
- `int totTweeners`（int totTweeners）(偏移: 0x3C)
- `int totSequences`（int totSequences）(偏移: 0x40)
- `bool isUpdateLoop`（bool is更新Loop）(偏移: 0x44)
- `Tween[] _activeTweens`（Tween[] _activeTweens）(偏移: 0x48)
- `Tween[] _pooledTweeners`（Tween[] _pooledTweeners）(偏移: 0x4C)
- `Stack<Tween> _PooledSequences`（Stack<Tween> _PooledSequences）(偏移: 0x50)
- `List<Tween> _KillList`（List<Tween> _击杀列表）(偏移: 0x54)
- `int _totTweenLinks`（int _totTweenLinks）(偏移: 0x5C)
- `int _maxActiveLookupId`（int _max激活的LookupId）(偏移: 0x60)
- `bool _requiresActiveReorganization`（bool _requires激活的Reorganization）(偏移: 0x64)
- `int _reorganizeFromId`（int _reorganizeFromId）(偏移: 0x68)
- `int _minPooledTweenerId`（int _minPooledTweenerId）(偏移: 0x6C)
- `int _maxPooledTweenerId`（int _maxPooledTweenerId）(偏移: 0x70)
- `bool _despawnAllCalledFromUpdateLoopCallback`（bool _despawn所有CalledFrom更新Loop回调）(偏移: 0x74)

### 方法 (41)

- `Sequence GetSequence()`
  （Sequence 获取Sequence（））
- `void SetUpdateType(Tween t, UpdateType updateType, bool isIndependentUpdate)`
  （void 集合更新类型（Tween t, 更新类型 updateType, bool isIndependentUpdate））
- `void AddActiveTweenToSequence(Tween t)`
  （void 添加激活的TweenToSequence（Tween t））
- `int DespawnAll()`
  （int Despawn所有（））
- `void Despawn(Tween t, bool modifyActiveLists = True)`
  （void Despawn（Tween t, bool modifyActiveLists = True））
- `void PurgeAll(bool isApplicationQuitting)`
  （void Purge所有（bool isApplicationQuitting））
- `void PurgePools()`
  （void PurgePools（））
- `void AddTweenLink(Tween t, TweenLink tweenLink)`
  （void 添加TweenLink（Tween t, TweenLink tweenLink））
- `void RemoveTweenLink(Tween t)`
  （void 移除TweenLink（Tween t））
- `void ResetCapacities()`
  （void 重置Capacities（））
- `void SetCapacities(int tweenersCapacity, int sequencesCapacity)`
  （void 集合Capacities（int tweenersCapacity, int sequencesCapacity））
- `int Validate()`
  （int 验证（））
- `void Update(UpdateType updateType, float deltaTime, float independentTime)`
  （void 更新（更新类型 updateType, float deltaTime, float independentTime））
- `bool Update(Tween t, float deltaTime, float independentTime, bool isSingleTweenManualUpdate)`
  （bool 更新（Tween t, float deltaTime, float independentTime, bool isSingleTweenManualUpdate））
- `int FilteredOperation(OperationType operationType, FilterType filterType, object id, bool optionalBool, float optionalFloat, object optionalObj, object[] optionalArray)`
  （int FilteredOperation（Operation类型 operationType, Filter类型 filterType, object id, bool optionalBool, float optionalFloat, object optionalObj, object[] optionalArray））
- `bool Complete(Tween t, bool modifyActiveLists = True, UpdateMode updateMode = 1)`
  （bool Complete（Tween t, bool modifyActiveLists = True, 更新模式 updateMode = 1））
- `bool Flip(Tween t)`
  （bool Flip（Tween t））
- `void ForceInit(Tween t, bool isSequenced = False)`
  （void 强制初始化（Tween t, bool isSequenced = False））
- `bool Goto(Tween t, float to, bool andPlay = False, UpdateMode updateMode = 1)`
  （bool Goto（Tween t, float to, bool andPlay = False, 更新模式 updateMode = 1））
- `bool Pause(Tween t)`
  （bool 暂停（Tween t））
- `bool Play(Tween t)`
  （bool 播放（Tween t））
- `bool PlayBackwards(Tween t)`
  （bool 播放Backwards（Tween t））
- `bool PlayForward(Tween t)`
  （bool 播放前进（Tween t））
- `bool Restart(Tween t, bool includeDelay = True, float changeDelayTo = -1)`
  （bool Restart（Tween t, bool includeDelay = True, float changeDelayTo = -1））
- `bool Rewind(Tween t, bool includeDelay = True)`
  （bool Rewind（Tween t, bool includeDelay = True））
- `bool SmoothRewind(Tween t)`
  （bool SmoothRewind（Tween t））
- `bool TogglePause(Tween t)`
  （bool 开关暂停（Tween t））
- `int TotalPooledTweens()`
  （int TotalPooledTweens（））
- `int TotalPlayingTweens()`
  （int TotalPlayingTweens（））
- `List<Tween> GetActiveTweens(bool playing, List<Tween> fillableList)`
  （List<Tween> 获取激活的Tweens（bool playing, List<Tween> fillableList））
- `List<Tween> GetTweensById(object id, bool playingOnly, List<Tween> fillableList)`
  （List<Tween> 获取TweensById（object id, bool playingOnly, List<Tween> fillableList））
- `List<Tween> GetTweensByTarget(object target, bool playingOnly, List<Tween> fillableList)`
  （List<Tween> 获取TweensBy目标（object target, bool playingOnly, List<Tween> fillableList））
- `void MarkForKilling(Tween t, bool isSingleTweenManualUpdate = False)`
  （void MarkForKilling（Tween t, bool isSingleTweenManualUpdate = False））
- `void EvaluateTweenLink(Tween t)`
  （void EvaluateTweenLink（Tween t））
- `void AddActiveTween(Tween t)`
  （void 添加激活的Tween（Tween t））
- `void ReorganizeActiveTweens()`
  （void Reorganize激活的Tweens（））
- `void DespawnActiveTweens(List<Tween> tweens)`
  （void Despawn激活的Tweens（List<Tween> tweens））
- `void RemoveActiveTween(Tween t)`
  （void 移除激活的Tween（Tween t））
- `void ClearTweenArray(Tween[] tweens)`
  （void 清除Tween数组（Tween[] tweens））
- `void IncreaseCapacities(TweenManager.CapacityIncreaseMode increaseMode)`
  （void IncreaseCapacities（TweenManager.CapacityIncrease模式 increaseMode））
- `void ManageOnRewindCallbackWhenAlreadyRewinded(Tween t, bool isPlayBackwardsOrSmoothRewind)`
  （void 管理OnRewind回调WhenAlreadyRewinded（Tween t, bool isPlayBackwardsOrSmoothRewind））

---

## TweenManager.CapacityIncreaseMode（TweenManager.CapacityIncrease模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TweenParams（TweenParams）

### 字段 (24)

- `TweenParams Params`（TweenParams Params）(偏移: 0x0)
- `object id`（object id）(偏移: 0x8)
- `object target`（object target）(偏移: 0xC)
- `UpdateType updateType`（更新类型 update类型）(偏移: 0x10)
- `bool isIndependentUpdate`（bool isIndependent更新）(偏移: 0x14)
- `TweenCallback onStart`（Tween回调 on开始）(偏移: 0x18)
- `TweenCallback onPlay`（Tween回调 on播放）(偏移: 0x1C)
- `TweenCallback onRewind`（Tween回调 onRewind）(偏移: 0x20)
- `TweenCallback onUpdate`（Tween回调 on更新）(偏移: 0x24)
- `TweenCallback onStepComplete`（Tween回调 onStepComplete）(偏移: 0x28)
- `TweenCallback onComplete`（Tween回调 onComplete）(偏移: 0x2C)
- `TweenCallback onKill`（Tween回调 on击杀）(偏移: 0x30)
- `TweenCallback<int> onWaypointChange`（TweenCallback<int> onWaypointChange）(偏移: 0x34)
- `bool isRecyclable`（bool isRecyclable）(偏移: 0x38)
- `bool isSpeedBased`（bool isSpeedBased）(偏移: 0x39)
- `bool autoKill`（bool auto击杀）(偏移: 0x3A)
- `int loops`（int loops）(偏移: 0x3C)
- `LoopType loopType`（Loop类型 loop类型）(偏移: 0x40)
- `float delay`（float delay）(偏移: 0x44)
- `bool isRelative`（bool isRelative）(偏移: 0x48)
- `Ease easeType`（Ease ease类型）(偏移: 0x4C)
- `EaseFunction customEase`（EaseFunction customEase）(偏移: 0x50)
- `float easeOvershootOrAmplitude`（float easeOvershootOrAmplitude）(偏移: 0x54)
- `float easePeriod`（float easePeriod）(偏移: 0x58)

### 方法 (22)

- `TweenParams Clear()`
  （TweenParams 清除（））
- `TweenParams SetAutoKill(bool autoKillOnCompletion = True)`
  （TweenParams 集合自动击杀（bool autoKillOnCompletion = True））
- `TweenParams SetId(object id)`
  （TweenParams 集合Id（object id））
- `TweenParams SetTarget(object target)`
  （TweenParams 集合目标（object target））
- `TweenParams SetLoops(int loops, Nullable<LoopType> loopType)`
  （TweenParams 集合Loops（int loops, Nullable<LoopType> loopType））
- `TweenParams SetEase(Ease ease, Nullable<float> overshootOrAmplitude, Nullable<float> period)`
  （TweenParams 集合Ease（Ease ease, Nullable<float> overshootOrAmplitude, Nullable<float> period））
- `TweenParams SetEase(AnimationCurve animCurve)`
  （TweenParams 集合Ease（动画Curve animCurve））
- `TweenParams SetEase(EaseFunction customEase)`
  （TweenParams 集合Ease（EaseFunction customEase））
- `TweenParams SetRecyclable(bool recyclable = True)`
  （TweenParams 集合Recyclable（bool recyclable = True））
- `TweenParams SetUpdate(bool isIndependentUpdate)`
  （TweenParams 集合更新（bool isIndependentUpdate））
- `TweenParams SetUpdate(UpdateType updateType, bool isIndependentUpdate = False)`
  （TweenParams 集合更新（更新类型 updateType, bool isIndependentUpdate = False））
- `TweenParams OnStart(TweenCallback action)`
  （TweenParams On开始（Tween回调 action））
- `TweenParams OnPlay(TweenCallback action)`
  （TweenParams On播放（Tween回调 action））
- `TweenParams OnRewind(TweenCallback action)`
  （TweenParams OnRewind（Tween回调 action））
- `TweenParams OnUpdate(TweenCallback action)`
  （TweenParams On更新（Tween回调 action））
- `TweenParams OnStepComplete(TweenCallback action)`
  （TweenParams OnStepComplete（Tween回调 action））
- `TweenParams OnComplete(TweenCallback action)`
  （TweenParams OnComplete（Tween回调 action））
- `TweenParams OnKill(TweenCallback action)`
  （TweenParams On击杀（Tween回调 action））
- `TweenParams OnWaypointChange(TweenCallback<int> action)`
  （TweenParams OnWaypointChange（TweenCallback<int> action））
- `TweenParams SetDelay(float delay)`
  （TweenParams 集合延迟（float delay））
- `TweenParams SetRelative(bool isRelative = True)`
  （TweenParams 集合Relative（bool isRelative = True））
- `TweenParams SetSpeedBased(bool isSpeedBased = True)`
  （TweenParams 集合SpeedBased（bool isSpeedBased = True））

---

## TweenSettingsExtensions（TweenSettingsExtensions）

### 方法 (25)

- `Sequence Append(Sequence s, Tween t)`
  （Sequence Append（Sequence s, Tween t））
- `Sequence Prepend(Sequence s, Tween t)`
  （Sequence Prepend（Sequence s, Tween t））
- `Sequence Join(Sequence s, Tween t)`
  （Sequence Join（Sequence s, Tween t））
- `Sequence Insert(Sequence s, float atPosition, Tween t)`
  （Sequence Insert（Sequence s, float atPosition, Tween t））
- `Sequence AppendInterval(Sequence s, float interval)`
  （Sequence Append间隔（Sequence s, float interval））
- `Sequence PrependInterval(Sequence s, float interval)`
  （Sequence Prepend间隔（Sequence s, float interval））
- `Sequence AppendCallback(Sequence s, TweenCallback callback)`
  （Sequence Append回调（Sequence s, Tween回调 callback））
- `Sequence PrependCallback(Sequence s, TweenCallback callback)`
  （Sequence Prepend回调（Sequence s, Tween回调 callback））
- `Sequence InsertCallback(Sequence s, float atPosition, TweenCallback callback)`
  （Sequence Insert回调（Sequence s, float atPosition, Tween回调 callback））
- `bool ValidateAddToSequence(Sequence s, Tween t, bool ignoreTween = False)`
  （bool 验证添加ToSequence（Sequence s, Tween t, bool ignoreTween = False））
- `Tweener SetOptions(TweenerCore<float, float, FloatOptions> t, bool snapping)`
  （Tweener 集合Options（TweenerCore<float, float, 浮点数Options> t, bool snapping））
- `Tweener SetOptions(TweenerCore<Vector2, Vector2, VectorOptions> t, bool snapping)`
  （Tweener 集合Options（TweenerCore<二维向量, 二维向量, 向量Options> t, bool snapping））
- `Tweener SetOptions(TweenerCore<Vector2, Vector2, VectorOptions> t, AxisConstraint axisConstraint, bool snapping = False)`
  （Tweener 集合Options（TweenerCore<二维向量, 二维向量, 向量Options> t, 轴Constraint axisConstraint, bool snapping = False））
- `Tweener SetOptions(TweenerCore<Vector3, Vector3, VectorOptions> t, bool snapping)`
  （Tweener 集合Options（TweenerCore<三维向量, 三维向量, 向量Options> t, bool snapping））
- `Tweener SetOptions(TweenerCore<Vector3, Vector3, VectorOptions> t, AxisConstraint axisConstraint, bool snapping = False)`
  （Tweener 集合Options（TweenerCore<三维向量, 三维向量, 向量Options> t, 轴Constraint axisConstraint, bool snapping = False））
- `Tweener SetOptions(TweenerCore<Vector4, Vector4, VectorOptions> t, bool snapping)`
  （Tweener 集合Options（TweenerCore<Vector4, Vector4, 向量Options> t, bool snapping））
- `Tweener SetOptions(TweenerCore<Vector4, Vector4, VectorOptions> t, AxisConstraint axisConstraint, bool snapping = False)`
  （Tweener 集合Options（TweenerCore<Vector4, Vector4, 向量Options> t, 轴Constraint axisConstraint, bool snapping = False））
- `Tweener SetOptions(TweenerCore<Quaternion, Vector3, QuaternionOptions> t, bool useShortest360Route = True)`
  （Tweener 集合Options（TweenerCore<Quaternion, 三维向量, QuaternionOptions> t, bool useShortest360Route = True））
- `Tweener SetOptions(TweenerCore<Color, Color, ColorOptions> t, bool alphaOnly)`
  （Tweener 集合Options（TweenerCore<颜色, 颜色, 颜色Options> t, bool alphaOnly））
- `Tweener SetOptions(TweenerCore<Rect, Rect, RectOptions> t, bool snapping)`
  （Tweener 集合Options（TweenerCore<Rect, Rect, RectOptions> t, bool snapping））
- `Tweener SetOptions(TweenerCore<string, string, StringOptions> t, bool richTextEnabled, ScrambleMode scrambleMode = 0, string scrambleChars)`
  （Tweener 集合Options（TweenerCore<string, string, 字符串Options> t, bool richTextEnabled, Scramble模式 scrambleMode = 0, string scrambleChars））
- `Tweener SetOptions(TweenerCore<Vector3, Vector3[], Vector3ArrayOptions> t, bool snapping)`
  （Tweener 集合Options（TweenerCore<三维向量, Vector3[], 三维向量数组Options> t, bool snapping））
- `Tweener SetOptions(TweenerCore<Vector3, Vector3[], Vector3ArrayOptions> t, AxisConstraint axisConstraint, bool snapping = False)`
  （Tweener 集合Options（TweenerCore<三维向量, Vector3[], 三维向量数组Options> t, 轴Constraint axisConstraint, bool snapping = False））
- `Tweener SetOptions(TweenerCore<Vector2, Vector2, CircleOptions> t, float endValueDegrees, bool relativeCenter = True, bool snapping = False)`
  （Tweener 集合Options（TweenerCore<二维向量, 二维向量, CircleOptions> t, float endValueDegrees, bool relativeCenter = True, bool snapping = False））
- `void SetPathForwardDirection(TweenerCore<Vector3, Path, PathOptions> t, Nullable<Vector3> forwardDirection, Nullable<Vector3> up)`
  （void 集合路径前进方向（TweenerCore<三维向量, 路径, 路径Options> t, Nullable<Vector3> forwardDirection, Nullable<Vector3> up））

---

## TweenType（Tween类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Tweener（Tweener）

**继承**: Tween（Tween）

### 字段 (2)

- `bool hasManuallySetStartValue`（bool hasManually集合开始值）(偏移: 0xC4)
- `bool isFromAllowed`（bool isFromAllowed）(偏移: 0xC5)

---

## TwistRelaxer（TwistRelaxer）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (10)

- `IK ik`（IK ik）(偏移: 0xC)
- `Transform parent`（变换 parent）(偏移: 0x10)
- `Transform child`（变换 child）(偏移: 0x14)
- `float weight`（float weight）(偏移: 0x18)
- `float parentChildCrossfade`（float parent子级Crossfade）(偏移: 0x1C)
- `float twistAngleOffset`（float twist角度Offset）(偏移: 0x20)
- `Vector3 twistAxis`（三维向量 twist轴）(偏移: 0x24)
- `Vector3 axis`（三维向量 axis）(偏移: 0x30)
- `Vector3 axisRelativeToParentDefault`（三维向量 axisRelativeTo父级默认的）(偏移: 0x3C)
- `Vector3 axisRelativeToChildDefault`（三维向量 axisRelativeTo子级默认的）(偏移: 0x48)

### 方法 (5)

- `void Relax()`
  （void Relax（））
- `void Start()`
  （void 开始（））
- `void OnPostUpdate()`
  （void OnPost更新（））
- `void LateUpdate()`
  （void 延迟更新（））
- `void OnDestroy()`
  （void On销毁（））

---

## Type（类型）

**继承**: MemberInfo, _Type（Member信息, _类型）

### 字段 (8)

- `MemberFilter FilterAttribute`（MemberFilter FilterAttribute）(偏移: 0x0)
- `MemberFilter FilterName`（MemberFilter Filter名称）(偏移: 0x4)
- `MemberFilter FilterNameIgnoreCase`（MemberFilter Filter名称IgnoreCase）(偏移: 0x8)
- `object Missing`（object Missing）(偏移: 0xC)
- `char Delimiter`（char Delimiter）(偏移: 0x10)
- `Type[] EmptyTypes`（Type[] 空Types）(偏移: 0x14)
- `Binder defaultBinder`（Binder defaultBinder）(偏移: 0x18)
- `RuntimeTypeHandle _impl`（Runtime类型句柄 _impl）(偏移: 0x8)

### 方法 (103)

- `MemberTypes get_MemberType()`
  （MemberTypes get_Member类型（））
- `Type get_DeclaringType()`
  （类型 get_Declaring类型（））
- `MethodBase get_DeclaringMethod()`
  （Method基础 get_DeclaringMethod（））
- `Type get_ReflectedType()`
  （类型 get_Reflected类型（））
- `Type GetType(string typeName, Func<AssemblyName, Assembly> assemblyResolver, Func<Assembly, string, bool, Type> typeResolver, bool throwOnError)`
  （类型 获取类型（string typeName, Func<Assembly名称, Assembly> assemblyResolver, Func<Assembly, string, bool, Type> typeResolver, bool throwOnError））
- `Type MakePointerType()`
  （类型 Make指针类型（））
- `Type MakeByRefType()`
  （类型 MakeByRef类型（））
- `Type MakeArrayType()`
  （类型 Make数组类型（））
- `Type MakeArrayType(int rank)`
  （类型 Make数组类型（int rank））
- `TypeCode GetTypeCode(Type type)`
  （类型Code 获取类型Code（类型 type））
- `TypeCode GetTypeCodeImpl()`
  （类型Code 获取类型CodeImpl（））
- `Binder get_DefaultBinder()`
  （Binder get_默认的Binder（））
- `void CreateBinder()`
  （void 创建Binder（））
- `RuntimeTypeHandle get_TypeHandle()`
  （Runtime类型句柄 get_类型句柄（））
- `RuntimeTypeHandle GetTypeHandle(object o)`
  （Runtime类型句柄 获取类型句柄（object o））
- `int GetArrayRank()`
  （int 获取数组排名（））
- `ConstructorInfo GetConstructor(BindingFlags bindingAttr, Binder binder, CallingConventions callConvention, Type[] types, ParameterModifier[] modifiers)`
  （Constructor信息 获取Constructor（BindingFlags bindingAttr, Binder binder, CallingConventions callConvention, Type[] types, ParameterModifier[] modifiers））
- `ConstructorInfo GetConstructor(BindingFlags bindingAttr, Binder binder, Type[] types, ParameterModifier[] modifiers)`
  （Constructor信息 获取Constructor（BindingFlags bindingAttr, Binder binder, Type[] types, ParameterModifier[] modifiers））
- `ConstructorInfo GetConstructor(Type[] types)`
  （Constructor信息 获取Constructor（Type[] types））
- `MethodInfo GetMethod(string name, BindingFlags bindingAttr, Binder binder, Type[] types, ParameterModifier[] modifiers)`
  （Method信息 获取Method（string name, BindingFlags bindingAttr, Binder binder, Type[] types, ParameterModifier[] modifiers））
- `MethodInfo GetMethod(string name, Type[] types)`
  （Method信息 获取Method（string name, Type[] types））
- `MethodInfo GetMethod(string name, BindingFlags bindingAttr)`
  （Method信息 获取Method（string name, BindingFlags bindingAttr））
- `MethodInfo GetMethod(string name)`
  （Method信息 获取Method（string name））
- `MethodInfo[] GetMethods()`
  （MethodInfo[] 获取Methods（））
- `FieldInfo GetField(string name)`
  （Field信息 获取Field（string name））
- `Type[] FindInterfaces(TypeFilter filter, object filterCriteria)`
  （Type[] 查找Interfaces（类型Filter filter, object filterCriteria））
- `EventInfo GetEvent(string name)`
  （事件信息 获取事件（string name））
- `PropertyInfo GetProperty(string name, BindingFlags bindingAttr, Binder binder, Type returnType, Type[] types, ParameterModifier[] modifiers)`
  （属性信息 获取属性（string name, BindingFlags bindingAttr, Binder binder, 类型 returnType, Type[] types, ParameterModifier[] modifiers））
- `PropertyInfo GetProperty(string name, BindingFlags bindingAttr)`
  （属性信息 获取属性（string name, BindingFlags bindingAttr））
- `PropertyInfo GetProperty(string name, Type returnType, Type[] types)`
  （属性信息 获取属性（string name, 类型 returnType, Type[] types））
- `PropertyInfo GetProperty(string name, Type returnType)`
  （属性信息 获取属性（string name, 类型 returnType））
- `PropertyInfo[] GetProperties()`
  （属性Info[] 获取Properties（））
- `Type GetNestedType(string name)`
  （类型 获取Nested类型（string name））
- `MemberInfo[] GetMember(string name)`
  （MemberInfo[] 获取Member（string name））
- `MemberInfo[] GetMember(string name, BindingFlags bindingAttr)`
  （MemberInfo[] 获取Member（string name, BindingFlags bindingAttr））
- `MemberInfo[] GetMember(string name, MemberTypes type, BindingFlags bindingAttr)`
  （MemberInfo[] 获取Member（string name, MemberTypes type, BindingFlags bindingAttr））
- `bool get_IsNested()`
  （bool get_是否Nested（））
- `TypeAttributes get_Attributes()`
  （类型Attributes get_Attributes（））
- `GenericParameterAttributes get_GenericParameterAttributes()`
  （GenericParameterAttributes get_GenericParameterAttributes（））
- `bool get_IsVisible()`
  （bool get_是否可见的（））
- `bool get_IsNotPublic()`
  （bool get_是否Not公开的（））
- `bool get_IsPublic()`
  （bool get_是否公开的（））
- `bool get_IsNestedPublic()`
  （bool get_是否Nested公开的（））
- `bool get_IsNestedAssembly()`
  （bool get_是否NestedAssembly（））
- `bool get_IsExplicitLayout()`
  （bool get_是否ExplicitLayout（））
- `bool get_IsClass()`
  （bool get_是否类（））
- `bool get_IsInterface()`
  （bool get_是否Interface（））
- `bool get_IsValueType()`
  （bool get_是否值类型（））
- `bool get_IsAbstract()`
  （bool get_是否抽象的（））
- `bool get_IsSealed()`
  （bool get_是否Sealed（））
- `bool get_IsEnum()`
  （bool get_是否Enum（））
- `bool get_IsSerializable()`
  （bool get_是否Serializable（））
- `bool get_IsArray()`
  （bool get_是否数组（））
- `bool get_IsSzArray()`
  （bool get_是否Sz数组（））
- `bool get_IsGenericType()`
  （bool get_是否Generic类型（））
- `bool get_IsGenericTypeDefinition()`
  （bool get_是否Generic类型Definition（））
- `bool get_IsGenericParameter()`
  （bool get_是否GenericParameter（））
- `int get_GenericParameterPosition()`
  （int get_GenericParameterPosition（））
- `bool get_ContainsGenericParameters()`
  （bool get_ContainsGenericParameters（））
- `Type[] GetGenericParameterConstraints()`
  （Type[] 获取GenericParameterConstraints（））
- `bool get_IsByRef()`
  （bool get_是否ByRef（））
- `bool get_IsPointer()`
  （bool get_是否指针（））
- `bool get_IsPrimitive()`
  （bool get_是否Primitive（））
- `bool get_IsCOMObject()`
  （bool get_是否COM对象（））
- `bool get_HasElementType()`
  （bool get_是否有元素类型（））
- `bool get_IsContextful()`
  （bool get_是否Contextful（））
- `bool get_IsMarshalByRef()`
  （bool get_是否MarshalByRef（））
- `bool IsValueTypeImpl()`
  （bool 是否值类型Impl（））
- `Type MakeGenericType(Type[] typeArguments)`
  （类型 MakeGeneric类型（Type[] typeArguments））
- `bool IsContextfulImpl()`
  （bool 是否ContextfulImpl（））
- `bool IsMarshalByRefImpl()`
  （bool 是否MarshalByRefImpl（））
- `Type[] GetGenericArguments()`
  （Type[] 获取GenericArguments（））
- `Type GetGenericTypeDefinition()`
  （类型 获取Generic类型Definition（））
- `Type GetRootElementType()`
  （类型 获取根元素类型（））
- `string[] GetEnumNames()`
  （string[] 获取EnumNames（））
- `Array GetEnumValues()`
  （数组 获取EnumValues（））
- `Array GetEnumRawConstantValues()`
  （数组 获取EnumRawConstantValues（））
- `void GetEnumData(out string[] enumNames, out Array enumValues)`
  （void 获取Enum数据（out string[] enumNames, out Array enumValues））
- `Type GetEnumUnderlyingType()`
  （类型 获取EnumUnderlying类型（））
- `bool IsEnumDefined(object value)`
  （bool 是否EnumDefined（object value））
- `string GetEnumName(object value)`
  （string 获取Enum名称（object value））
- `int BinarySearch(Array array, object value)`
  （int Binary搜索（数组 array, object value））
- `bool IsIntegerType(Type t)`
  （bool 是否Integer类型（类型 t））
- `bool IsSubclassOf(Type c)`
  （bool 是否SubclassOf（类型 c））
- `bool IsInstanceOfType(object o)`
  （bool 是否实例Of类型（object o））
- `bool IsAssignableFrom(Type c)`
  （bool 是否AssignableFrom（类型 c））
- `bool IsEquivalentTo(Type other)`
  （bool 是否EquivalentTo（类型 other））
- `bool ImplementInterface(Type ifaceType)`
  （bool ImplementInterface（类型 ifaceType））
- `string FormatTypeName()`
  （string 格式化类型名称（））
- `string FormatTypeName(bool serialization)`
  （string 格式化类型名称（bool serialization））
- `string ToString()`
  （string To字符串（））
- `bool Equals(object o)`
  （bool Equals（object o））
- `bool Equals(Type o)`
  （bool Equals（类型 o））
- `bool op_Equality(Type left, Type right)`
  （bool op_Equality（类型 left, 类型 right））
- `bool op_Inequality(Type left, Type right)`
  （bool op_Inequality（类型 left, 类型 right））
- `int GetHashCode()`
  （int 获取HashCode（））
- `Type GetType()`
  （类型 获取类型（））
- `Type internal_from_name(string name, bool throwOnError, bool ignoreCase)`
  （类型 internal_from_name（string name, bool throwOnError, bool ignoreCase））
- `Type GetType(string typeName)`
  （类型 获取类型（string typeName））
- `Type GetType(string typeName, bool throwOnError)`
  （类型 获取类型（string typeName, bool throwOnError））
- `Type GetType(string typeName, bool throwOnError, bool ignoreCase)`
  （类型 获取类型（string typeName, bool throwOnError, bool ignoreCase））
- `Type GetTypeFromHandle(RuntimeTypeHandle handle)`
  （类型 获取类型From句柄（Runtime类型句柄 handle））
- `Type internal_from_handle(IntPtr handle)`
  （类型 internal_from_handle（整数Ptr handle））

---

## TypeAnalysis（类型Analysis）

### 字段 (6)

- `PropertyAnalysis[] properties`（属性Analysis[] properties）(偏移: 0x8)
- `string name`（string name）(偏移: 0xC)
- `EventKeywords keywords`（事件Keywords keywords）(偏移: 0x10)
- `EventLevel level`（事件等级 level）(偏移: 0x18)
- `EventOpcode opcode`（事件Opcode opcode）(偏移: 0x1C)
- `EventTags tags`（事件Tags tags）(偏移: 0x20)

---

## TypeAttributes（类型Attributes）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TypeBuilder（类型构建器）

**继承**: TypeInfo（类型信息）

### 方法 (32)

- `Assembly get_Assembly()`
  （Assembly get_Assembly（））
- `string get_AssemblyQualifiedName()`
  （string get_AssemblyQualified名称（））
- `Type get_BaseType()`
  （类型 get_基础类型（））
- `string get_FullName()`
  （string get_满名称（））
- `Module get_Module()`
  （模块 get_模块（））
- `string get_Name()`
  （string get_名称（））
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
  （object[] 获取自定义的Attributes（bool inherit））
- `object[] GetCustomAttributes(Type attributeType, bool inherit)`
  （object[] 获取自定义的Attributes（类型 attributeType, bool inherit））
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
  （bool 是否Defined（类型 attributeType, bool inherit））
- `bool IsPointerImpl()`
  （bool 是否指针Impl（））
- `bool IsPrimitiveImpl()`
  （bool 是否PrimitiveImpl（））

---

## TypeBuilderInstantiation（类型构建器Instantiation）

**继承**: TypeInfo（类型信息）

### 方法 (1)

- `Type MakeGenericType(Type type, Type[] typeArguments)`
  （类型 MakeGeneric类型（类型 type, Type[] typeArguments））

---

## TypeCode（类型Code）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TypeConverter（类型Converter）

### 字段 (1)

- `bool useCompatibleTypeConversion`（bool useCompatible类型Conversion）(偏移: 0x0)

### 方法 (39)

- `bool get_UseCompatibleTypeConversion()`
  （bool get_UseCompatible类型Conversion（））
- `bool CanConvertFrom(Type sourceType)`
  （bool 能否转换From（类型 sourceType））
- `bool CanConvertFrom(ITypeDescriptorContext context, Type sourceType)`
  （bool 能否转换From（I类型DescriptorContext context, 类型 sourceType））
- `bool CanConvertTo(Type destinationType)`
  （bool 能否转换To（类型 destinationType））
- `bool CanConvertTo(ITypeDescriptorContext context, Type destinationType)`
  （bool 能否转换To（I类型DescriptorContext context, 类型 destinationType））
- `object ConvertFrom(object value)`
  （object 转换From（object value））
- `object ConvertFrom(ITypeDescriptorContext context, CultureInfo culture, object value)`
  （object 转换From（I类型DescriptorContext context, Culture信息 culture, object value））
- `object ConvertFromInvariantString(string text)`
  （object 转换FromInvariant字符串（string text））
- `object ConvertFromInvariantString(ITypeDescriptorContext context, string text)`
  （object 转换FromInvariant字符串（I类型DescriptorContext context, string text））
- `object ConvertFromString(string text)`
  （object 转换From字符串（string text））
- `object ConvertFromString(ITypeDescriptorContext context, string text)`
  （object 转换From字符串（I类型DescriptorContext context, string text））
- `object ConvertFromString(ITypeDescriptorContext context, CultureInfo culture, string text)`
  （object 转换From字符串（I类型DescriptorContext context, Culture信息 culture, string text））
- `object ConvertTo(object value, Type destinationType)`
  （object 转换To（object value, 类型 destinationType））
- `object ConvertTo(ITypeDescriptorContext context, CultureInfo culture, object value, Type destinationType)`
  （object 转换To（I类型DescriptorContext context, Culture信息 culture, object value, 类型 destinationType））
- `string ConvertToInvariantString(object value)`
  （string 转换ToInvariant字符串（object value））
- `string ConvertToInvariantString(ITypeDescriptorContext context, object value)`
  （string 转换ToInvariant字符串（I类型DescriptorContext context, object value））
- `string ConvertToString(object value)`
  （string 转换To字符串（object value））
- `string ConvertToString(ITypeDescriptorContext context, object value)`
  （string 转换To字符串（I类型DescriptorContext context, object value））
- `string ConvertToString(ITypeDescriptorContext context, CultureInfo culture, object value)`
  （string 转换To字符串（I类型DescriptorContext context, Culture信息 culture, object value））
- `object CreateInstance(IDictionary propertyValues)`
  （object 创建实例（I字典 propertyValues））
- `object CreateInstance(ITypeDescriptorContext context, IDictionary propertyValues)`
  （object 创建实例（I类型DescriptorContext context, I字典 propertyValues））
- `Exception GetConvertFromException(object value)`
  （Exception 获取转换FromException（object value））
- `Exception GetConvertToException(object value, Type destinationType)`
  （Exception 获取转换ToException（object value, 类型 destinationType））
- `bool GetCreateInstanceSupported()`
  （bool 获取创建实例Supported（））
- `bool GetCreateInstanceSupported(ITypeDescriptorContext context)`
  （bool 获取创建实例Supported（I类型DescriptorContext context））
- `PropertyDescriptorCollection GetProperties(object value)`
  （属性DescriptorCollection 获取Properties（object value））
- `PropertyDescriptorCollection GetProperties(ITypeDescriptorContext context, object value)`
  （属性DescriptorCollection 获取Properties（I类型DescriptorContext context, object value））
- `PropertyDescriptorCollection GetProperties(ITypeDescriptorContext context, object value, Attribute[] attributes)`
  （属性DescriptorCollection 获取Properties（I类型DescriptorContext context, object value, Attribute[] attributes））
- `bool GetPropertiesSupported()`
  （bool 获取PropertiesSupported（））
- `bool GetPropertiesSupported(ITypeDescriptorContext context)`
  （bool 获取PropertiesSupported（I类型DescriptorContext context））
- `ICollection GetStandardValues()`
  （ICollection 获取StandardValues（））
- `TypeConverter.StandardValuesCollection GetStandardValues(ITypeDescriptorContext context)`
  （类型Converter.StandardValuesCollection 获取StandardValues（I类型DescriptorContext context））
- `bool GetStandardValuesExclusive()`
  （bool 获取StandardValuesExclusive（））
- `bool GetStandardValuesExclusive(ITypeDescriptorContext context)`
  （bool 获取StandardValuesExclusive（I类型DescriptorContext context））
- `bool GetStandardValuesSupported()`
  （bool 获取StandardValuesSupported（））
- `bool GetStandardValuesSupported(ITypeDescriptorContext context)`
  （bool 获取StandardValuesSupported（I类型DescriptorContext context））
- `bool IsValid(object value)`
  （bool 是否Valid（object value））
- `bool IsValid(ITypeDescriptorContext context, object value)`
  （bool 是否Valid（I类型DescriptorContext context, object value））
- `PropertyDescriptorCollection SortProperties(PropertyDescriptorCollection props, string[] names)`
  （属性DescriptorCollection SortProperties（属性DescriptorCollection props, string[] names））

---

## TypeConverter.SimplePropertyDescriptor（类型Converter.Simple属性Descriptor）

**继承**: PropertyDescriptor（属性Descriptor）

### 字段 (2)

- `Type componentType`（类型 component类型）(偏移: 0x44)
- `Type propertyType`（类型 property类型）(偏移: 0x48)

### 方法 (3)

- `Type get_ComponentType()`
  （类型 get_组件类型（））
- `bool get_IsReadOnly()`
  （bool get_是否ReadOnly（））
- `Type get_PropertyType()`
  （类型 get_属性类型（））

---

## TypeConverter.StandardValuesCollection（类型Converter.StandardValuesCollection）

**继承**: ICollection, IEnumerable（ICollection, IEnumerable）

### 字段 (2)

- `ICollection values`（ICollection values）(偏移: 0x8)
- `Array valueArray`（数组 value数组）(偏移: 0xC)

### 方法 (3)

- `int get_Count()`
  （int get_数量（））
- `void CopyTo(Array array, int index)`
  （void 复制To（数组 array, int index））
- `IEnumerator GetEnumerator()`
  （IEnumerator 获取Enumerator（））

---

## TypeConverterAttribute（类型ConverterAttribute）

**继承**: Attribute（Attribute）

### 字段 (2)

- `string typeName`（string type名称）(偏移: 0x8)
- `TypeConverterAttribute Default`（类型ConverterAttribute 默认的）(偏移: 0x0)

### 方法 (3)

- `string get_ConverterTypeName()`
  （string get_Converter类型名称（））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## TypeDependencyAttribute（类型DependencyAttribute）

**继承**: Attribute（Attribute）

### 字段 (1)

- `string typeName`（string type名称）(偏移: 0x8)

---

## TypeDescriptionProvider（类型Description提供者）

### 字段 (2)

- `TypeDescriptionProvider _parent`（类型Description提供者 _parent）(偏移: 0x8)
- `TypeDescriptionProvider.EmptyCustomTypeDescriptor _emptyDescriptor`（类型DescriptionProvider.空自定义的类型Descriptor _emptyDescriptor）(偏移: 0xC)

### 方法 (11)

- `object CreateInstance(IServiceProvider provider, Type objectType, Type[] argTypes, object[] args)`
  （object 创建实例（I服务提供者 provider, 类型 objectType, Type[] argTypes, object[] args））
- `IDictionary GetCache(object instance)`
  （I字典 获取缓存（object instance））
- `ICustomTypeDescriptor GetExtendedTypeDescriptor(object instance)`
  （I自定义的类型Descriptor 获取Extended类型Descriptor（object instance））
- `IExtenderProvider[] GetExtenderProviders(object instance)`
  （IExtenderProvider[] 获取ExtenderProviders（object instance））
- `string GetFullComponentName(object component)`
  （string 获取满组件名称（object component））
- `Type GetReflectionType(Type objectType)`
  （类型 获取Reflection类型（类型 objectType））
- `Type GetReflectionType(object instance)`
  （类型 获取Reflection类型（object instance））
- `Type GetReflectionType(Type objectType, object instance)`
  （类型 获取Reflection类型（类型 objectType, object instance））
- `ICustomTypeDescriptor GetTypeDescriptor(Type objectType)`
  （I自定义的类型Descriptor 获取类型Descriptor（类型 objectType））
- `ICustomTypeDescriptor GetTypeDescriptor(object instance)`
  （I自定义的类型Descriptor 获取类型Descriptor（object instance））
- `ICustomTypeDescriptor GetTypeDescriptor(Type objectType, object instance)`
  （I自定义的类型Descriptor 获取类型Descriptor（类型 objectType, object instance））

---

## TypeDescriptionProviderAttribute（类型Description提供者Attribute）

**继承**: Attribute（Attribute）

### 字段 (1)

- `string _typeName`（string _type名称）(偏移: 0x8)

### 方法 (1)

- `string get_TypeName()`
  （string get_类型名称（））

---

## TypeDescriptor（类型Descriptor）

### 字段 (13)

- `WeakHashtable _providerTable`（WeakHashtable _providerTable）(偏移: 0x0)
- `Hashtable _providerTypeTable`（Hashtable _provider类型Table）(偏移: 0x4)
- `Hashtable _defaultProviders`（Hashtable _defaultProviders）(偏移: 0x8)
- `WeakHashtable _associationTable`（WeakHashtable _associationTable）(偏移: 0xC)
- `int _metadataVersion`（int _metadataVersion）(偏移: 0x10)
- `int _collisionIndex`（int _collision索引）(偏移: 0x14)
- `BooleanSwitch TraceDescriptor`（BooleanSwitch TraceDescriptor）(偏移: 0x18)
- `Guid[] _pipelineInitializeKeys`（Guid[] _pipeline初始化Keys）(偏移: 0x1C)
- `Guid[] _pipelineMergeKeys`（Guid[] _pipelineMergeKeys）(偏移: 0x20)
- `Guid[] _pipelineFilterKeys`（Guid[] _pipelineFilterKeys）(偏移: 0x24)
- `Guid[] _pipelineAttributeFilterKeys`（Guid[] _pipelineAttributeFilterKeys）(偏移: 0x28)
- `object _internalSyncObject`（object _internal同步对象）(偏移: 0x2C)
- `RefreshEventHandler Refreshed`（刷新事件处理器 Refreshed）(偏移: 0x30)

### 方法 (104)

- `IComNativeDescriptorHandler get_ComNativeDescriptorHandler()`
  （IComNativeDescriptor处理器 get_ComNativeDescriptor处理器（））
- `void set_ComNativeDescriptorHandler(IComNativeDescriptorHandler value)`
  （void set_ComNativeDescriptor处理器（IComNativeDescriptor处理器 value））
- `Type get_ComObjectType()`
  （类型 get_Com对象类型（））
- `Type get_InterfaceType()`
  （类型 get_Interface类型（））
- `int get_MetadataVersion()`
  （int get_MetadataVersion（））
- `void add_Refreshed(RefreshEventHandler value)`
  （void add_Refreshed（刷新事件处理器 value））
- `void remove_Refreshed(RefreshEventHandler value)`
  （void remove_Refreshed（刷新事件处理器 value））
- `TypeDescriptionProvider AddAttributes(Type type, Attribute[] attributes)`
  （类型Description提供者 添加Attributes（类型 type, Attribute[] attributes））
- `TypeDescriptionProvider AddAttributes(object instance, Attribute[] attributes)`
  （类型Description提供者 添加Attributes（object instance, Attribute[] attributes））
- `void AddEditorTable(Type editorBaseType, Hashtable table)`
  （void 添加EditorTable（类型 editorBaseType, Hashtable table））
- `void AddProvider(TypeDescriptionProvider provider, Type type)`
  （void 添加提供者（类型Description提供者 provider, 类型 type））
- `void AddProvider(TypeDescriptionProvider provider, object instance)`
  （void 添加提供者（类型Description提供者 provider, object instance））
- `void AddProviderTransparent(TypeDescriptionProvider provider, Type type)`
  （void 添加提供者透明的（类型Description提供者 provider, 类型 type））
- `void AddProviderTransparent(TypeDescriptionProvider provider, object instance)`
  （void 添加提供者透明的（类型Description提供者 provider, object instance））
- `void CheckDefaultProvider(Type type)`
  （void 检查默认的提供者（类型 type））
- `void CreateAssociation(object primary, object secondary)`
  （void 创建Association（object primary, object secondary））
- `IDesigner CreateDesigner(IComponent component, Type designerBaseType)`
  （IDesigner 创建Designer（I组件 component, 类型 designerBaseType））
- `EventDescriptor CreateEvent(Type componentType, string name, Type type, Attribute[] attributes)`
  （事件Descriptor 创建事件（类型 componentType, string name, 类型 type, Attribute[] attributes））
- `EventDescriptor CreateEvent(Type componentType, EventDescriptor oldEventDescriptor, Attribute[] attributes)`
  （事件Descriptor 创建事件（类型 componentType, 事件Descriptor oldEventDescriptor, Attribute[] attributes））
- `object CreateInstance(IServiceProvider provider, Type objectType, Type[] argTypes, object[] args)`
  （object 创建实例（I服务提供者 provider, 类型 objectType, Type[] argTypes, object[] args））
- `PropertyDescriptor CreateProperty(Type componentType, string name, Type type, Attribute[] attributes)`
  （属性Descriptor 创建属性（类型 componentType, string name, 类型 type, Attribute[] attributes））
- `PropertyDescriptor CreateProperty(Type componentType, PropertyDescriptor oldPropertyDescriptor, Attribute[] attributes)`
  （属性Descriptor 创建属性（类型 componentType, 属性Descriptor oldPropertyDescriptor, Attribute[] attributes））
- `void DebugValidate(Type type, AttributeCollection attributes, AttributeCollection debugAttributes)`
  （void Debug验证（类型 type, AttributeCollection attributes, AttributeCollection debugAttributes））
- `void DebugValidate(AttributeCollection attributes, AttributeCollection debugAttributes)`
  （void Debug验证（AttributeCollection attributes, AttributeCollection debugAttributes））
- `void DebugValidate(AttributeCollection attributes, Type type)`
  （void Debug验证（AttributeCollection attributes, 类型 type））
- `void DebugValidate(AttributeCollection attributes, object instance, bool noCustomTypeDesc)`
  （void Debug验证（AttributeCollection attributes, object instance, bool noCustomTypeDesc））
- `void DebugValidate(TypeConverter converter, Type type)`
  （void Debug验证（类型Converter converter, 类型 type））
- `void DebugValidate(TypeConverter converter, object instance, bool noCustomTypeDesc)`
  （void Debug验证（类型Converter converter, object instance, bool noCustomTypeDesc））
- `void DebugValidate(EventDescriptorCollection events, Type type, Attribute[] attributes)`
  （void Debug验证（事件DescriptorCollection events, 类型 type, Attribute[] attributes））
- `void DebugValidate(EventDescriptorCollection events, object instance, Attribute[] attributes, bool noCustomTypeDesc)`
  （void Debug验证（事件DescriptorCollection events, object instance, Attribute[] attributes, bool noCustomTypeDesc））
- `void DebugValidate(PropertyDescriptorCollection properties, Type type, Attribute[] attributes)`
  （void Debug验证（属性DescriptorCollection properties, 类型 type, Attribute[] attributes））
- `void DebugValidate(PropertyDescriptorCollection properties, object instance, Attribute[] attributes, bool noCustomTypeDesc)`
  （void Debug验证（属性DescriptorCollection properties, object instance, Attribute[] attributes, bool noCustomTypeDesc））
- `ArrayList FilterMembers(IList members, Attribute[] attributes)`
  （数组列表 FilterMembers（I列表 members, Attribute[] attributes））
- `object GetAssociation(Type type, object primary)`
  （object 获取Association（类型 type, object primary））
- `AttributeCollection GetAttributes(Type componentType)`
  （AttributeCollection 获取Attributes（类型 componentType））
- `AttributeCollection GetAttributes(object component)`
  （AttributeCollection 获取Attributes（object component））
- `AttributeCollection GetAttributes(object component, bool noCustomTypeDesc)`
  （AttributeCollection 获取Attributes（object component, bool noCustomTypeDesc））
- `IDictionary GetCache(object instance)`
  （I字典 获取缓存（object instance））
- `string GetClassName(object component)`
  （string 获取类名称（object component））
- `string GetClassName(object component, bool noCustomTypeDesc)`
  （string 获取类名称（object component, bool noCustomTypeDesc））
- `string GetClassName(Type componentType)`
  （string 获取类名称（类型 componentType））
- `string GetComponentName(object component)`
  （string 获取组件名称（object component））
- `string GetComponentName(object component, bool noCustomTypeDesc)`
  （string 获取组件名称（object component, bool noCustomTypeDesc））
- `TypeConverter GetConverter(object component)`
  （类型Converter 获取Converter（object component））
- `TypeConverter GetConverter(object component, bool noCustomTypeDesc)`
  （类型Converter 获取Converter（object component, bool noCustomTypeDesc））
- `TypeConverter GetConverter(Type type)`
  （类型Converter 获取Converter（类型 type））
- `EventDescriptor GetDefaultEvent(Type componentType)`
  （事件Descriptor 获取默认的事件（类型 componentType））
- `EventDescriptor GetDefaultEvent(object component)`
  （事件Descriptor 获取默认的事件（object component））
- `EventDescriptor GetDefaultEvent(object component, bool noCustomTypeDesc)`
  （事件Descriptor 获取默认的事件（object component, bool noCustomTypeDesc））
- `PropertyDescriptor GetDefaultProperty(Type componentType)`
  （属性Descriptor 获取默认的属性（类型 componentType））
- `PropertyDescriptor GetDefaultProperty(object component)`
  （属性Descriptor 获取默认的属性（object component））
- `PropertyDescriptor GetDefaultProperty(object component, bool noCustomTypeDesc)`
  （属性Descriptor 获取默认的属性（object component, bool noCustomTypeDesc））
- `ICustomTypeDescriptor GetDescriptor(Type type, string typeName)`
  （I自定义的类型Descriptor 获取Descriptor（类型 type, string typeName））
- `ICustomTypeDescriptor GetDescriptor(object component, bool noCustomTypeDesc)`
  （I自定义的类型Descriptor 获取Descriptor（object component, bool noCustomTypeDesc））
- `ICustomTypeDescriptor GetExtendedDescriptor(object component)`
  （I自定义的类型Descriptor 获取ExtendedDescriptor（object component））
- `object GetEditor(object component, Type editorBaseType)`
  （object 获取Editor（object component, 类型 editorBaseType））
- `object GetEditor(object component, Type editorBaseType, bool noCustomTypeDesc)`
  （object 获取Editor（object component, 类型 editorBaseType, bool noCustomTypeDesc））
- `object GetEditor(Type type, Type editorBaseType)`
  （object 获取Editor（类型 type, 类型 editorBaseType））
- `EventDescriptorCollection GetEvents(Type componentType)`
  （事件DescriptorCollection 获取Events（类型 componentType））
- `EventDescriptorCollection GetEvents(Type componentType, Attribute[] attributes)`
  （事件DescriptorCollection 获取Events（类型 componentType, Attribute[] attributes））
- `EventDescriptorCollection GetEvents(object component)`
  （事件DescriptorCollection 获取Events（object component））
- `EventDescriptorCollection GetEvents(object component, bool noCustomTypeDesc)`
  （事件DescriptorCollection 获取Events（object component, bool noCustomTypeDesc））
- `EventDescriptorCollection GetEvents(object component, Attribute[] attributes)`
  （事件DescriptorCollection 获取Events（object component, Attribute[] attributes））
- `EventDescriptorCollection GetEvents(object component, Attribute[] attributes, bool noCustomTypeDesc)`
  （事件DescriptorCollection 获取Events（object component, Attribute[] attributes, bool noCustomTypeDesc））
- `string GetExtenderCollisionSuffix(MemberDescriptor member)`
  （string 获取ExtenderCollisionSuffix（MemberDescriptor member））
- `string GetFullComponentName(object component)`
  （string 获取满组件名称（object component））
- `Type GetNodeForBaseType(Type searchType)`
  （类型 获取节点For基础类型（类型 searchType））
- `PropertyDescriptorCollection GetProperties(Type componentType)`
  （属性DescriptorCollection 获取Properties（类型 componentType））
- `PropertyDescriptorCollection GetProperties(Type componentType, Attribute[] attributes)`
  （属性DescriptorCollection 获取Properties（类型 componentType, Attribute[] attributes））
- `PropertyDescriptorCollection GetProperties(object component)`
  （属性DescriptorCollection 获取Properties（object component））
- `PropertyDescriptorCollection GetProperties(object component, bool noCustomTypeDesc)`
  （属性DescriptorCollection 获取Properties（object component, bool noCustomTypeDesc））
- `PropertyDescriptorCollection GetProperties(object component, Attribute[] attributes)`
  （属性DescriptorCollection 获取Properties（object component, Attribute[] attributes））
- `PropertyDescriptorCollection GetProperties(object component, Attribute[] attributes, bool noCustomTypeDesc)`
  （属性DescriptorCollection 获取Properties（object component, Attribute[] attributes, bool noCustomTypeDesc））
- `PropertyDescriptorCollection GetPropertiesImpl(object component, Attribute[] attributes, bool noCustomTypeDesc, bool noAttributes)`
  （属性DescriptorCollection 获取PropertiesImpl（object component, Attribute[] attributes, bool noCustomTypeDesc, bool noAttributes））
- `TypeDescriptionProvider GetProvider(Type type)`
  （类型Description提供者 获取提供者（类型 type））
- `TypeDescriptionProvider GetProvider(object instance)`
  （类型Description提供者 获取提供者（object instance））
- `TypeDescriptionProvider GetProviderRecursive(Type type)`
  （类型Description提供者 获取提供者Recursive（类型 type））
- `Type GetReflectionType(Type type)`
  （类型 获取Reflection类型（类型 type））
- `Type GetReflectionType(object instance)`
  （类型 获取Reflection类型（object instance））
- `TypeDescriptor.TypeDescriptionNode NodeFor(Type type)`
  （类型Descriptor.类型Description节点 节点For（类型 type））
- `TypeDescriptor.TypeDescriptionNode NodeFor(Type type, bool createDelegator)`
  （类型Descriptor.类型Description节点 节点For（类型 type, bool createDelegator））
- `TypeDescriptor.TypeDescriptionNode NodeFor(object instance)`
  （类型Descriptor.类型Description节点 节点For（object instance））
- `TypeDescriptor.TypeDescriptionNode NodeFor(object instance, bool createDelegator)`
  （类型Descriptor.类型Description节点 节点For（object instance, bool createDelegator））
- `void NodeRemove(object key, TypeDescriptionProvider provider)`
  （void 节点移除（object key, 类型Description提供者 provider））
- `ICollection PipelineAttributeFilter(int pipelineType, ICollection members, Attribute[] filter, object instance, IDictionary cache)`
  （ICollection PipelineAttributeFilter（int pipelineType, ICollection members, Attribute[] filter, object instance, I字典 cache））
- `ICollection PipelineFilter(int pipelineType, ICollection members, object instance, IDictionary cache)`
  （ICollection PipelineFilter（int pipelineType, ICollection members, object instance, I字典 cache））
- `ICollection PipelineInitialize(int pipelineType, ICollection members, IDictionary cache)`
  （ICollection Pipeline初始化（int pipelineType, ICollection members, I字典 cache））
- `ICollection PipelineMerge(int pipelineType, ICollection primary, ICollection secondary, object instance, IDictionary cache)`
  （ICollection PipelineMerge（int pipelineType, ICollection primary, ICollection secondary, object instance, I字典 cache））
- `void RaiseRefresh(object component)`
  （void Raise刷新（object component））
- `void RaiseRefresh(Type type)`
  （void Raise刷新（类型 type））
- `void Refresh(object component)`
  （void 刷新（object component））
- `void Refresh(object component, bool refreshReflectionProvider)`
  （void 刷新（object component, bool refreshReflectionProvider））
- `void Refresh(Type type)`
  （void 刷新（类型 type））
- `void Refresh(Module module)`
  （void 刷新（模块 module））
- `void Refresh(Assembly assembly)`
  （void 刷新（Assembly assembly））
- `void RemoveAssociation(object primary, object secondary)`
  （void 移除Association（object primary, object secondary））
- `void RemoveAssociations(object primary)`
  （void 移除Associations（object primary））
- `void RemoveProvider(TypeDescriptionProvider provider, Type type)`
  （void 移除提供者（类型Description提供者 provider, 类型 type））
- `void RemoveProvider(TypeDescriptionProvider provider, object instance)`
  （void 移除提供者（类型Description提供者 provider, object instance））
- `void RemoveProviderTransparent(TypeDescriptionProvider provider, Type type)`
  （void 移除提供者透明的（类型Description提供者 provider, 类型 type））
- `void RemoveProviderTransparent(TypeDescriptionProvider provider, object instance)`
  （void 移除提供者透明的（类型Description提供者 provider, object instance））
- `bool ShouldHideMember(MemberDescriptor member, Attribute attribute)`
  （bool 应该隐藏Member（MemberDescriptor member, Attribute attribute））
- `void SortDescriptorArray(IList infos)`
  （void SortDescriptor数组（I列表 infos））
- `void Trace(string message, object[] args)`
  （void Trace（string message, object[] args））

---

## TypeDescriptor.AttributeFilterCacheItem（类型Descriptor.AttributeFilter缓存项目）

### 字段 (2)

- `Attribute[] _filter`（Attribute[] _filter）(偏移: 0x8)
- `ICollection FilteredMembers`（ICollection FilteredMembers）(偏移: 0xC)

### 方法 (1)

- `bool IsValid(Attribute[] filter)`
  （bool 是否Valid（Attribute[] filter））

---

## TypeDescriptor.AttributeProvider（类型Descriptor.Attribute提供者）

**继承**: TypeDescriptionProvider（类型Description提供者）

### 字段 (1)

- `Attribute[] _attrs`（Attribute[] _attrs）(偏移: 0x10)

### 方法 (1)

- `ICustomTypeDescriptor GetTypeDescriptor(Type objectType, object instance)`
  （I自定义的类型Descriptor 获取类型Descriptor（类型 objectType, object instance））

---

## TypeDescriptor.AttributeProvider.AttributeTypeDescriptor（类型Descriptor.AttributeProvider.Attribute类型Descriptor）

**继承**: CustomTypeDescriptor（自定义的类型Descriptor）

### 字段 (1)

- `Attribute[] _attributeArray`（Attribute[] _attribute数组）(偏移: 0xC)

### 方法 (1)

- `AttributeCollection GetAttributes()`
  （AttributeCollection 获取Attributes（））

---

## TypeDescriptor.ComNativeDescriptionProvider（类型Descriptor.ComNativeDescription提供者）

**继承**: TypeDescriptionProvider（类型Description提供者）

### 字段 (1)

- `IComNativeDescriptorHandler _handler`（IComNativeDescriptor处理器 _handler）(偏移: 0x10)

### 方法 (3)

- `IComNativeDescriptorHandler get_Handler()`
  （IComNativeDescriptor处理器 get_处理器（））
- `void set_Handler(IComNativeDescriptorHandler value)`
  （void set_处理器（IComNativeDescriptor处理器 value））
- `ICustomTypeDescriptor GetTypeDescriptor(Type objectType, object instance)`
  （I自定义的类型Descriptor 获取类型Descriptor（类型 objectType, object instance））

---

## TypeDescriptor.ComNativeDescriptionProvider.ComNativeTypeDescriptor（类型Descriptor.ComNativeDescriptionProvider.ComNative类型Descriptor）

**继承**: ICustomTypeDescriptor（I自定义的类型Descriptor）

### 字段 (2)

- `IComNativeDescriptorHandler _handler`（IComNativeDescriptor处理器 _handler）(偏移: 0x8)
- `object _instance`（object _instance）(偏移: 0xC)

---

## TypeDescriptor.FilterCacheItem（类型Descriptor.Filter缓存项目）

### 字段 (2)

- `ITypeDescriptorFilterService _filterService`（I类型DescriptorFilter服务 _filter服务）(偏移: 0x8)
- `ICollection FilteredMembers`（ICollection FilteredMembers）(偏移: 0xC)

### 方法 (1)

- `bool IsValid(ITypeDescriptorFilterService filterService)`
  （bool 是否Valid（I类型DescriptorFilter服务 filterService））

---

## TypeDescriptor.MemberDescriptorComparer（类型Descriptor.MemberDescriptorComparer）

**继承**: IComparer（IComparer）

### 字段 (1)

- `TypeDescriptor.MemberDescriptorComparer Instance`（类型Descriptor.MemberDescriptorComparer 实例）(偏移: 0x0)

### 方法 (1)

- `int Compare(object left, object right)`
  （int Compare（object left, object right））

---

## TypeDescriptor.MergedTypeDescriptor（类型Descriptor.Merged类型Descriptor）

**继承**: ICustomTypeDescriptor（I自定义的类型Descriptor）

### 字段 (2)

- `ICustomTypeDescriptor _primary`（I自定义的类型Descriptor _primary）(偏移: 0x8)
- `ICustomTypeDescriptor _secondary`（I自定义的类型Descriptor _secondary）(偏移: 0xC)

---

## TypeDescriptor.TypeDescriptionNode（类型Descriptor.类型Description节点）

**继承**: TypeDescriptionProvider（类型Description提供者）

### 字段 (2)

- `TypeDescriptor.TypeDescriptionNode Next`（类型Descriptor.类型Description节点 下一个）(偏移: 0x10)
- `TypeDescriptionProvider Provider`（类型Description提供者 提供者）(偏移: 0x14)

### 方法 (7)

- `object CreateInstance(IServiceProvider provider, Type objectType, Type[] argTypes, object[] args)`
  （object 创建实例（I服务提供者 provider, 类型 objectType, Type[] argTypes, object[] args））
- `IDictionary GetCache(object instance)`
  （I字典 获取缓存（object instance））
- `ICustomTypeDescriptor GetExtendedTypeDescriptor(object instance)`
  （I自定义的类型Descriptor 获取Extended类型Descriptor（object instance））
- `IExtenderProvider[] GetExtenderProviders(object instance)`
  （IExtenderProvider[] 获取ExtenderProviders（object instance））
- `string GetFullComponentName(object component)`
  （string 获取满组件名称（object component））
- `Type GetReflectionType(Type objectType, object instance)`
  （类型 获取Reflection类型（类型 objectType, object instance））
- `ICustomTypeDescriptor GetTypeDescriptor(Type objectType, object instance)`
  （I自定义的类型Descriptor 获取类型Descriptor（类型 objectType, object instance））

---

## TypeDescriptor.TypeDescriptionNode.DefaultExtendedTypeDescriptor（类型Descriptor.类型DescriptionNode.默认的Extended类型Descriptor）

**继承**: ICustomTypeDescriptor（I自定义的类型Descriptor）

### 字段 (2)

- `TypeDescriptor.TypeDescriptionNode _node`（类型Descriptor.类型Description节点 _node）(偏移: 0x0)
- `object _instance`（object _instance）(偏移: 0x4)

---

## TypeDescriptor.TypeDescriptionNode.DefaultTypeDescriptor（类型Descriptor.类型DescriptionNode.默认的类型Descriptor）

**继承**: ICustomTypeDescriptor（I自定义的类型Descriptor）

### 字段 (3)

- `TypeDescriptor.TypeDescriptionNode _node`（类型Descriptor.类型Description节点 _node）(偏移: 0x0)
- `Type _objectType`（类型 _object类型）(偏移: 0x4)
- `object _instance`（object _instance）(偏移: 0x8)

---

## TypeEntry（类型Entry）

### 字段 (2)

- `string assembly_name`（string assembly_name）(偏移: 0x8)
- `string type_name`（string type_name）(偏移: 0xC)

### 方法 (4)

- `string get_AssemblyName()`
  （string get_Assembly名称（））
- `void set_AssemblyName(string value)`
  （void set_Assembly名称（string value））
- `string get_TypeName()`
  （string get_类型名称（））
- `void set_TypeName(string value)`
  （void set_类型名称（string value））

---

## TypeFilter（类型Filter）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `bool Invoke(Type m, object filterCriteria)`
  （bool Invoke（类型 m, object filterCriteria））
- `IAsyncResult BeginInvoke(Type m, object filterCriteria, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（类型 m, object filterCriteria, 异步回调 callback, object object））
- `bool EndInvoke(IAsyncResult result)`
  （bool 结束Invoke（I异步Result result））

---

## TypeFilterLevel（类型Filter等级）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TypeForwardedFromAttribute（类型ForwardedFromAttribute）

**继承**: Attribute（Attribute）

### 字段 (1)

- `string assemblyFullName`（string assembly满名称）(偏移: 0x8)

### 方法 (1)

- `string get_AssemblyFullName()`
  （string get_Assembly满名称（））

---

## TypeIdentifiers（类型Identifiers）

### 方法 (1)

- `TypeIdentifier FromDisplay(string displayName)`
  （类型Identifier FromDisplay（string displayName））

---

## TypeIdentifiers.Display（类型Identifiers.Display）

**继承**: TypeNames.ATypeName, TypeIdentifier, TypeName, IEquatable<TypeName>（类型Names.A类型名称, 类型Identifier, 类型名称, IEquatable<类型Name>）

### 字段 (2)

- `string displayName`（string display名称）(偏移: 0x8)
- `string internal_name`（string internal_name）(偏移: 0xC)

### 方法 (3)

- `string get_DisplayName()`
  （string get_Display名称（））
- `string get_InternalName()`
  （string get_内部的名称（））
- `string GetInternalName()`
  （string 获取内部的名称（））

---

## TypeInferenceRuleAttribute（类型InferenceRuleAttribute）

**继承**: Attribute（Attribute）

### 字段 (1)

- `string _rule`（string _rule）(偏移: 0x8)

### 方法 (1)

- `string ToString()`
  （string To字符串（））

---

## TypeInferenceRules（类型InferenceRules）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TypeInfo（类型信息）

**继承**: IRemotingTypeInfo（IRemoting类型信息）

### 字段 (3)

- `string serverType`（string server类型）(偏移: 0x8)
- `string[] serverHierarchy`（string[] serverHierarchy）(偏移: 0xC)
- `string[] interfacesImplemented`（string[] interfacesImplemented）(偏移: 0x10)

### 方法 (2)

- `string get_TypeName()`
  （string get_类型名称（））
- `bool CanCastTo(Type fromType, object o)`
  （bool 能否CastTo（类型 fromType, object o））

---

## TypeInformation（类型Information）

### 字段 (3)

- `string fullTypeName`（string full类型名称）(偏移: 0x8)
- `string assemblyString`（string assembly字符串）(偏移: 0xC)
- `bool hasTypeForwardedFrom`（bool has类型ForwardedFrom）(偏移: 0x10)

### 方法 (3)

- `string get_FullTypeName()`
  （string get_满类型名称（））
- `string get_AssemblyString()`
  （string get_Assembly字符串（））
- `bool get_HasTypeForwardedFrom()`
  （bool get_是否有类型ForwardedFrom（））

---

## TypeInitializationException（类型InitializationException）

**继承**: SystemException（系统Exception）

### 字段 (1)

- `string _typeName`（string _type名称）(偏移: 0x44)

### 方法 (2)

- `string get_TypeName()`
  （string get_类型名称（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））

---

## TypeLoadException（类型加载Exception）

**继承**: SystemException, ISerializable（系统Exception, ISerializable）

### 字段 (4)

- `string ClassName`（string 类名称）(偏移: 0x44)
- `string AssemblyName`（string Assembly名称）(偏移: 0x48)
- `string MessageArg`（string MessageArg）(偏移: 0x4C)
- `int ResourceId`（int 资源Id）(偏移: 0x50)

### 方法 (3)

- `string get_Message()`
  （string get_Message（））
- `void SetMessageField()`
  （void 集合MessageField（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））

---

## TypeLoadExceptionHolder（类型加载ExceptionHolder）

### 字段 (1)

- `string m_typeName`（string m_type名称）(偏移: 0x8)

### 方法 (1)

- `string get_TypeName()`
  （string get_类型名称（））

---

## TypeNameFormatFlags（类型名称格式化Flags）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TypeNameKind（类型名称Kind）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TypeNameParser（类型名称Parser）

### 方法 (1)

- `Type GetType(string typeName, Func<AssemblyName, Assembly> assemblyResolver, Func<Assembly, string, bool, Type> typeResolver, bool throwOnError, bool ignoreCase, ref StackCrawlMark stackMark)`
  （类型 获取类型（string typeName, Func<Assembly名称, Assembly> assemblyResolver, Func<Assembly, string, bool, Type> typeResolver, bool throwOnError, bool ignoreCase, ref StackCrawlMark stackMark））

---

## TypeNames.ATypeName（类型Names.A类型名称）

**继承**: TypeName, IEquatable<TypeName>（类型名称, IEquatable<类型Name>）

### 方法 (3)

- `bool Equals(TypeName other)`
  （bool Equals（类型名称 other））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool Equals(object other)`
  （bool Equals（object other））

---

## TypeSpec（类型Spec）

### 字段 (7)

- `TypeIdentifier name`（类型Identifier name）(偏移: 0x8)
- `string assembly_name`（string assembly_name）(偏移: 0xC)
- `List<TypeIdentifier> nested`（List<类型Identifier> nested）(偏移: 0x10)
- `List<TypeSpec> generic_params`（List<类型Spec> generic_params）(偏移: 0x14)
- `List<ModifierSpec> modifier_spec`（List<修改器Spec> modifier_spec）(偏移: 0x18)
- `bool is_byref`（bool is_byref）(偏移: 0x1C)
- `string display_fullname`（string display_fullname）(偏移: 0x20)

### 方法 (13)

- `bool get_HasModifiers()`
  （bool get_是否有Modifiers（））
- `string GetDisplayFullName(TypeSpec.DisplayNameFormat flags)`
  （string 获取Display满名称（类型Spec.Display名称格式化 flags））
- `StringBuilder GetModifierString(StringBuilder sb)`
  （字符串构建器 获取修改器字符串（字符串构建器 sb））
- `string get_DisplayFullName()`
  （string get_Display满名称（））
- `TypeSpec Parse(string typeName)`
  （类型Spec 解析（string typeName））
- `string UnescapeInternalName(string displayName)`
  （string Unescape内部的名称（string displayName））
- `Type Resolve(Func<AssemblyName, Assembly> assemblyResolver, Func<Assembly, string, bool, Type> typeResolver, bool throwOnError, bool ignoreCase)`
  （类型 Resolve（Func<Assembly名称, Assembly> assemblyResolver, Func<Assembly, string, bool, Type> typeResolver, bool throwOnError, bool ignoreCase））
- `void AddName(string type_name)`
  （void 添加名称（string type_name））
- `void AddModifier(ModifierSpec md)`
  （void 添加修改器（修改器Spec md））
- `void SkipSpace(string name, ref int pos)`
  （void SkipSpace（string name, ref int pos））
- `void BoundCheck(int idx, string s)`
  （void Bound检查（int idx, string s））
- `TypeIdentifier ParsedTypeIdentifier(string displayName)`
  （类型Identifier Parsed类型Identifier（string displayName））
- `TypeSpec Parse(string name, ref int p, bool is_recurse, bool allow_aqn)`
  （类型Spec 解析（string name, ref int p, bool is_recurse, bool allow_aqn））

---

## TypeSpec.DisplayNameFormat（类型Spec.Display名称格式化）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## TypedReference（Typed引用）

### 字段 (3)

- `RuntimeTypeHandle type`（Runtime类型句柄 type）(偏移: 0x0)
- `IntPtr Value`（整数Ptr 值）(偏移: 0x4)
- `IntPtr Type`（整数Ptr 类型）(偏移: 0x8)

### 方法 (6)

- `TypedReference MakeTypedReference(object target, FieldInfo[] flds)`
  （Typed引用 MakeTyped引用（object target, FieldInfo[] flds））
- `TypedReference MakeTypedReferenceInternal(object target, FieldInfo[] fields)`
  （Typed引用 MakeTyped引用内部的（object target, FieldInfo[] fields））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool Equals(object o)`
  （bool Equals（object o））
- `bool get_IsNull()`
  （bool get_是否Null（））
- `void SetTypedReference(TypedReference target, object value)`
  （void 集合Typed引用（Typed引用 target, object value））

---

## UIBehaviour（界面Behaviour）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 方法 (13)

- `void Awake()`
  （void Awake（））
- `void OnEnable()`
  （void On启用（））
- `void Start()`
  （void 开始（））
- `void OnDisable()`
  （void On禁用（））
- `void OnDestroy()`
  （void On销毁（））
- `bool IsActive()`
  （bool 是否激活的（））
- `void OnRectTransformDimensionsChange()`
  （void OnRect变换DimensionsChange（））
- `void OnBeforeTransformParentChanged()`
  （void OnBefore变换父级Changed（））
- `void OnTransformParentChanged()`
  （void On变换父级Changed（））
- `void OnDidApplyAnimationProperties()`
  （void OnDid应用动画Properties（））
- `void OnCanvasGroupChanged()`
  （void On画布组Changed（））
- `void OnCanvasHierarchyChanged()`
  （void On画布HierarchyChanged（））
- `bool IsDestroyed()`
  （bool 是否Destroyed（））

---

## UICharInfo（界面Char信息）

### 字段 (2)

- `Vector2 cursorPos`（二维向量 cursorPos）(偏移: 0x0)
- `float charWidth`（float char宽度）(偏移: 0x8)

---

## UIElementsRuntimeUtilityNative（界面ElementsRuntime工具Native）

### 字段 (2)

- `Action RepaintOverlayPanelsCallback`（动作 RepaintOverlayPanels回调）(偏移: 0x0)
- `Action UpdateRuntimePanelsCallback`（动作 更新RuntimePanels回调）(偏移: 0x4)

### 方法 (2)

- `void RepaintOverlayPanels()`
  （void RepaintOverlayPanels（））
- `void UpdateRuntimePanels()`
  （void 更新RuntimePanels（））

---

## UIFoldout（界面Foldout）

**继承**: Toggle（开关）

### 字段 (3)

- `GameObject content`（游戏对象 content）(偏移: 0xC4)
- `GameObject arrowOpened`（游戏对象 arrowOpened）(偏移: 0xC8)
- `GameObject arrowClosed`（游戏对象 arrowClosed）(偏移: 0xCC)

### 方法 (4)

- `void Start()`
  （void 开始（））
- `void OnValidate()`
  （void On验证（））
- `void SetState(bool state)`
  （void 集合状态（bool state））
- `void SetState(bool state, bool rebuildLayout)`
  （void 集合状态（bool state, bool rebuildLayout））

---

## UILineInfo（界面Line信息）

### 字段 (4)

- `int startCharIdx`（int startCharIdx）(偏移: 0x0)
- `int height`（int height）(偏移: 0x4)
- `float topY`（float topY）(偏移: 0x8)
- `float leading`（float leading）(偏移: 0xC)

---

## UISystemProfilerApi（界面系统ProfilerApi）

### 方法 (3)

- `void BeginSample(UISystemProfilerApi.SampleType type)`
  （void BeginSample（界面系统ProfilerApi.Sample类型 type））
- `void EndSample(UISystemProfilerApi.SampleType type)`
  （void 结束Sample（界面系统ProfilerApi.Sample类型 type））
- `void AddMarker(string name, Object obj)`
  （void 添加Marker（string name, 对象 obj））

---

## UISystemProfilerApi.SampleType（界面系统ProfilerApi.Sample类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UIVertex（界面Vertex）

### 字段 (11)

- `Vector3 position`（三维向量 position）(偏移: 0x0)
- `Vector3 normal`（三维向量 normal）(偏移: 0xC)
- `Vector4 tangent`（Vector4 tangent）(偏移: 0x18)
- `Color32 color`（Color32 color）(偏移: 0x28)
- `Vector4 uv0`（Vector4 uv0）(偏移: 0x2C)
- `Vector4 uv1`（Vector4 uv1）(偏移: 0x3C)
- `Vector4 uv2`（Vector4 uv2）(偏移: 0x4C)
- `Vector4 uv3`（Vector4 uv3）(偏移: 0x5C)
- `Color32 s_DefaultColor`（Color32 s_默认的颜色）(偏移: 0x0)
- `Vector4 s_DefaultTangent`（Vector4 s_默认的Tangent）(偏移: 0x4)
- `UIVertex simpleVert`（界面Vertex simpleVert）(偏移: 0x14)

---

## UI_GameEnd（UI_游戏结束）

**继承**: Singleton<UI_GameEnd>（Singleton<UI_游戏End>）

### 方法 (2)

- `void OnGameEndBtnDown()`
  （void On游戏结束Btn下（））
- `void QuitApplication()`
  （void QuitApplication（））

---

## UI_GameLoading（UI_游戏Loading）

**继承**: Singleton<UI_GameLoading>（Singleton<UI_游戏Loading>）

### 字段 (2)

- `RawImage loadingBG`（Raw图像 loadingBG）(偏移: 0xC)
- `Image gaugeImage`（图像 gauge图像）(偏移: 0x10)

### 方法 (2)

- `void set_progress(float value)`
  （void set_progress（float value））
- `void set_loadingTex(Texture value)`
  （void set_loadingTex（纹理 value））

---

## UI_GameRoom（UI_游戏房间）

**继承**: Singleton<UI_GameRoom>（Singleton<UI_游戏Room>）

### 字段 (17)

- `Dropdown matchTypeDropdown`（Dropdown match类型Dropdown）(偏移: 0xC)
- `Dropdown mapDropdown`（Dropdown mapDropdown）(偏移: 0x10)
- `Dropdown winTypeDropdown`（Dropdown win类型Dropdown）(偏移: 0x14)
- `Dropdown conditionDropdown`（Dropdown conditionDropdown）(偏移: 0x18)
- `Dropdown weaponSelectDropdown`（Dropdown weapon选择Dropdown）(偏移: 0x1C)
- `UI_SelectionGroup wpnBagTab`（UI_Selection组 武器背包Tab）(偏移: 0x20)
- `UI_ItemBox[] wpnSlots`（UI_项目Box[] 武器Slots）(偏移: 0x24)
- `UI_ItemBox_Throw wpnSlot_Throw`（UI_项目Box_投掷 武器Slot_投掷）(偏移: 0x28)
- `List<ClientData> players`（List<客户端Data> players）(偏移: 0x0)
- `int[] respawnTime`（int[] respawn时间）(偏移: 0x4)
- `MapAsset[] mapDatas`（映射Asset[] mapDatas）(偏移: 0x2C)
- `MapAsset currentMapAsset`（地图资产 current映射资产）(偏移: 0x30)
- `AsyncOperation gameSceneAsync`（异步Operation game场景异步）(偏移: 0x34)
- `Dropdown[] gameSettingDropdowns`（Dropdown[] game设置Dropdowns）(偏移: 0x38)
- `Dropdown botCountDropDown`（Dropdown bot数量Drop下）(偏移: 0x3C)
- `Dropdown joinTeamDropDown`（Dropdown join队伍Drop下）(偏移: 0x40)
- `List<string> botNames`（List<string> botNames）(偏移: 0x44)

### 方法 (8)

- `void Awake()`
  （void Awake（））
- `void OnMatchTypeChange(int value)`
  （void On比赛类型Change（int value））
- `void OnWindTypeChange(int value)`
  （void OnWind类型Change（int value））
- `void OnStartGameBtnDown()`
  （void On开始游戏Btn下（））
- `void OnInvenLoadFinish()`
  （void OnInven加载Finish（））
- `void OnEnterPannel()`
  （void OnEnterPannel（））
- `void OnWpnBagValueChange(int index)`
  （void On武器背包值Change（int index））
- `void GenerateBotClient()`
  （void Generate机器人客户端（））

---

## UI_Inven（UI_Inven）

**继承**: Singleton<UI_Inven>（Singleton<UI_Inven>）

### 字段 (21)

- `string dataPath`（string data路径）(偏移: 0x0)
- `UI_Tab tab`（UI_Tab tab）(偏移: 0xC)
- `UI_Tab leftTab`（UI_Tab leftTab）(偏移: 0x10)
- `UI_SelectionGroup wpnBagTab`（UI_Selection组 武器背包Tab）(偏移: 0x14)
- `UI_ItemBox[] wpnSlots`（UI_项目Box[] 武器Slots）(偏移: 0x18)
- `UI_ItemBox_Throw wpnSlot_Throw`（UI_项目Box_投掷 武器Slot_投掷）(偏移: 0x1C)
- `GameObject[] extractWpnBtns`（游戏Object[] extract武器Btns）(偏移: 0x20)
- `UI_SelectionGroup weaponTabs`（UI_Selection组 weaponTabs）(偏移: 0x24)
- `UI_ItemPanel itemPanel`（UI_项目面板 item面板）(偏移: 0x28)
- `Texture2D[] categoryTexs`（Texture2D[] categoryTexs）(偏移: 0x2C)
- `List<ItemObject> myWeapons`（List<项目Object> myWeapons）(偏移: 0x8)
- `List<ItemObject> myCharacters`（List<项目Object> myCharacters）(偏移: 0xC)
- `List<ItemObject> myItems`（List<项目Object> myItems）(偏移: 0x10)
- `List<ItemObject> tempItemList`（List<项目Object> temp项目列表）(偏移: 0x30)
- `ItemObject knifeItem`（项目对象 knife项目）(偏移: 0x14)
- `string defaultBagStr`（string default背包Str）(偏移: 0x18)
- `List<int> wpnList_Main`（List<int> 武器List_主要的）(偏移: 0x1C)
- `List<int> wpnList_Secondary`（List<int> 武器List_Secondary）(偏移: 0x20)
- `List<int> wpnList_Knife`（List<int> 武器List_近战武器）(偏移: 0x24)
- `List<int> wpnList_Throw`（List<int> 武器List_投掷）(偏移: 0x28)
- `List<int> characterList`（List<int> character列表）(偏移: 0x2C)

### 方法 (28)

- `int[][] get_wpnBags()`
  （int[][] get_wpnBags（））
- `void Awake()`
  （void Awake（））
- `void OnEnterPannel()`
  （void OnEnterPannel（））
- `void OnExitPannel()`
  （void OnExitPannel（））
- `void OnTabValueChange(int value)`
  （void OnTab值Change（int value））
- `void OnWpnTabValueChange(int value)`
  （void On武器Tab值Change（int value））
- `void OnCharTabValueChange(int value)`
  （void OnCharTab值Change（int value））
- `void OnItemTabValueChange(int value)`
  （void On项目Tab值Change（int value））
- `int WeaponItemSort(ItemObject x, ItemObject y)`
  （int Weapon项目Sort（项目对象 x, 项目对象 y））
- `int ItemNameSort(ItemObject x, ItemObject y)`
  （int 项目名称Sort（项目对象 x, 项目对象 y））
- `void OnItemBtnDown(UI_ItemBox itemBox)`
  （void On项目Btn下（UI_项目Box itemBox））
- `void EquipWeapon(ItemObject newItem)`
  （void EquipWeapon（项目对象 newItem））
- `void EquipCharacter(ItemObject item)`
  （void Equip角色（项目对象 item））
- `void EquipItem(UI_ItemBox itemBox)`
  （void Equip项目（UI_项目Box itemBox））
- `void OnExtractWpnBtnDown(int slot)`
  （void OnExtract武器Btn下（int slot））
- `void OnBagTabValueChange(int bagID)`
  （void On背包Tab值Change（int bagID））
- `ItemObject GetWpnBagItem(int bagID, int slot)`
  （项目对象 获取武器背包项目（int bagID, int slot））
- `void LoadData()`
  （void 加载数据（））
- `void SaveData()`
  （void 保存数据（））
- `int[][] TranslateWpnBag(int[][] bags)`
  （int[][] Translate武器背包（int[][] bags））
- `SO_Item_Character GetCharacterItem(int itemID)`
  （SO_Item_角色 获取角色项目（int itemID））
- `bool TryGetItem(int itemID, out SO_Item result)`
  （bool Try获取项目（int itemID, out SO_Item result））
- `void UpdateItemBox(UI_ItemBox input)`
  （void 更新项目Box（UI_项目Box input））
- `void UpdateItemBoxClipBuff(UI_ItemBox input)`
  （void 更新项目Box弹匣增益（UI_项目Box input））
- `void ItemSortOut(SO_Item item)`
  （void 项目SortOut（SO_项目 item））
- `void RandomizeInven(ClientData client)`
  （void RandomizeInven（客户端数据 client））
- `void OnClipBuffUpdate(bool updatePannel = True)`
  （void On弹匣增益更新（bool updatePannel = True））
- `void UpdateBagClipBuff()`
  （void 更新背包弹匣增益（））

---

## UI_InvenItem（UI_Inven项目）

**继承**: UI_ItemBox（UI_项目Box）

### 字段 (1)

- `GameObject selectBox`（游戏对象 selectBox）(偏移: 0x28)

### 方法 (2)

- `bool get_isSelected()`
  （bool get_is选中的（））
- `void set_isSelected(bool value)`
  （void set_is选中的（bool value））

---

## UI_ItemBox（UI_项目Box）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (6)

- `RawImage itemBox`（Raw图像 itemBox）(偏移: 0xC)
- `RawImage itemIcon`（Raw图像 item图标）(偏移: 0x10)
- `Text itemName`（文本 item名称）(偏移: 0x14)
- `Button itemBtn`（按钮 itemBtn）(偏移: 0x18)
- `Text clipBuffText`（文本 clip增益文本）(偏移: 0x1C)
- `RawImage categoryImg`（Raw图像 categoryImg）(偏移: 0x20)

### 方法 (6)

- `void set_clipBuffCount(int value)`
  （void set_clip增益数量（int value））
- `void set_category(Texture2D value)`
  （void set_category（Texture2D value））
- `ItemObject get_item()`
  （项目对象 get_item（））
- `void set_item(ItemObject value)`
  （void set_item（项目对象 value））
- `void BindItem(ItemObject item)`
  （void Bind项目（项目对象 item））
- `void BindBtnFunction(Action<UI_ItemBox> btnFunc)`
  （void BindBtnFunction（Action<UI_项目Box> btnFunc））

---

## UI_ItemBox_Throw（UI_项目Box_投掷）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (3)

- `RawImage itemBox`（Raw图像 itemBox）(偏移: 0xC)
- `RawImage[] itemIcons`（RawImage[] itemIcons）(偏移: 0x10)
- `Button[] itemBtns`（Button[] itemBtns）(偏移: 0x14)

### 方法 (3)

- `ItemObject get_item()`
  （项目对象 get_item（））
- `void set_item(ItemObject value)`
  （void set_item（项目对象 value））
- `void BindItem(int slot, ItemObject item)`
  （void Bind项目（int slot, 项目对象 item））

---

## UI_ItemPanel（UI_项目面板）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (10)

- `GameObject itemBoxPrefab`（游戏对象 itemBox预制体）(偏移: 0xC)
- `int maxCount`（int max数量）(偏移: 0x10)
- `Scrollbar scrollbar`（Scrollbar scrollbar）(偏移: 0x14)
- `Vector4 scrollArea`（Vector4 scrollArea）(偏移: 0x18)
- `List<UI_ItemBox> boxList`（List<UI_项目Box> box列表）(偏移: 0x28)
- `int curPage`（int curPage）(偏移: 0x2C)
- `int totalPageCount`（int totalPage数量）(偏移: 0x30)
- `float scrollValuePerPage`（float scroll值PerPage）(偏移: 0x34)
- `List<ItemObject> list`（List<项目Object> list）(偏移: 0x38)
- `Action<UI_ItemBox> updateBoxFunc`（Action<UI_项目Box> updateBoxFunc）(偏移: 0x3C)

### 方法 (6)

- `void Update()`
  （void 更新（））
- `void Init(Action<UI_ItemBox> btnFunc)`
  （void 初始化（Action<UI_项目Box> btnFunc））
- `void SetItems(List<ItemObject> newList)`
  （void 集合Items（List<项目Object> newList））
- `void OnScrollBarValueChange(float value)`
  （void On滚动Bar值Change（float value））
- `void JumpToItemPage(int pageID)`
  （void 跳跃To项目Page（int pageID））
- `void UpdateAllItemBox()`
  （void 更新所有项目Box（））

---

## UI_Option（UI_Option）

**继承**: Singleton<UI_Option>（Singleton<UI_Option>）

### 字段 (13)

- `UI_Tab tab`（UI_Tab tab）(偏移: 0xC)
- `Dropdown dpd_Resolution`（Dropdown dpd_Resolution）(偏移: 0x10)
- `UI_SelectionGroup fullScreenSwitch`（UI_Selection组 full屏幕的Switch）(偏移: 0x14)
- `Slider mouseSpeed`（滑块 mouseSpeed）(偏移: 0x18)
- `Slider zoomSpeed`（滑块 zoomSpeed）(偏移: 0x1C)
- `AudioMixer audioMixer`（音频Mixer audioMixer）(偏移: 0x20)
- `UI_SelectionGroup bgmSwitch`（UI_Selection组 bgmSwitch）(偏移: 0x24)
- `Slider bgmSlider`（滑块 bgm滑块）(偏移: 0x28)
- `UI_SelectionGroup sndSwitch`（UI_Selection组 sndSwitch）(偏移: 0x2C)
- `Slider sndSlider`（滑块 snd滑块）(偏移: 0x30)
- `UI_SelectionGroup radioSwitch`（UI_Selection组 radioSwitch）(偏移: 0x34)
- `Slider radioSlider`（滑块 radio滑块）(偏移: 0x38)
- `Vector2Int[] resolutions`（二维向量Int[] resolutions）(偏移: 0x0)

### 方法 (14)

- `void Start()`
  （void 开始（））
- `void OnCancelBtnDown()`
  （void On取消Btn下（））
- `void OnBgmSwitchValueChange(int value)`
  （void OnBgmSwitch值Change（int value））
- `void OnBgmSliderValueChange(float value)`
  （void OnBgm滑块值Change（float value））
- `void OnSndSwitchValueChange(int value)`
  （void OnSndSwitch值Change（int value））
- `void OnSndSliderValueChange(float value)`
  （void OnSnd滑块值Change（float value））
- `void OnRadioSwitchValueChange(int value)`
  （void OnRadioSwitch值Change（int value））
- `void OnRadioSliderValueChange(float value)`
  （void OnRadio滑块值Change（float value））
- `float CalculateAudioVolume(float value)`
  （float 计算音频Volume（float value））
- `void UpdateUI()`
  （void 更新界面（））
- `void OnSaveBtnDown()`
  （void On保存Btn下（））
- `void SetVisible(bool visible)`
  （void 集合可见的（bool visible））
- `void SetResolution()`
  （void 集合Resolution（））
- `void SetMouseSpeed()`
  （void 集合鼠标Speed（））

---

## UI_SelectionGroup（UI_Selection组）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (2)

- `Button[] buttons`（Button[] buttons）(偏移: 0xC)
- `UnityEvent<int> OnValueChange`（Unity引擎Event<int> On值Change）(偏移: 0x14)

### 方法 (3)

- `int get_currentSelection()`
  （int get_currentSelection（））
- `void set_currentSelection(int value)`
  （void set_currentSelection（int value））
- `void OnSelectValueChange(int index)`
  （void On选择值Change（int index））

---

## UI_SliderValueText（UI_滑块值文本）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (2)

- `string formatStr`（string formatStr）(偏移: 0xC)
- `Text text`（文本 text）(偏移: 0x10)

### 方法 (1)

- `void UpdateText(float value)`
  （void 更新文本（float value））

---

## UI_Tab（UI_Tab）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (4)

- `GameObject[] tabs`（游戏Object[] tabs）(偏移: 0xC)
- `GameObject[] buttons`（游戏Object[] buttons）(偏移: 0x10)
- `int curTabIndex`（int curTab索引）(偏移: 0x14)
- `UnityEvent<int> OnValueChange`（Unity引擎Event<int> On值Change）(偏移: 0x18)

### 方法 (1)

- `void ChangeTab(int index)`
  （void ChangeTab（int index））

---

## UI_Tab2（UI_Tab2）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (4)

- `Image tabImage`（图像 tab图像）(偏移: 0xC)
- `Sprite[] tabSprites`（Sprite[] tabSprites）(偏移: 0x10)
- `GameObject[] buttons`（游戏Object[] buttons）(偏移: 0x14)
- `int curTabIndex`（int curTab索引）(偏移: 0x18)

### 方法 (1)

- `void ChangeTab(int index)`
  （void ChangeTab（int index））

---

## UI_Temploray（UI_Temploray）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (4)

- `WeaponAsset wpnAsset`（武器资产 武器资产）(偏移: 0xC)
- `InputField registerCodeInput`（输入Field registerCode输入）(偏移: 0x10)
- `InputField password`（输入Field password）(偏移: 0x14)
- `GameObject mySelfBtn`（游戏对象 mySelfBtn）(偏移: 0x18)

### 方法 (5)

- `void Awake()`
  （void Awake（））
- `void Update()`
  （void 更新（））
- `void Myself()`
  （void Myself（））
- `void OnRegisterBtnDown()`
  （void OnRegisterBtn下（））
- `void CopyMachineCode()`
  （void 复制MachineCode（））

---

## UI_TopMenu（UI_顶部菜单）

**继承**: Singleton<UI_TopMenu>（Singleton<UI_顶部Menu>）

### 字段 (4)

- `AudioClip[] music`（音频Clip[] music）(偏移: 0xC)
- `AudioSource bgmSource`（音频Source bgmSource）(偏移: 0x10)
- `Button[] changeFrameBtns`（Button[] changeFrameBtns）(偏移: 0x14)
- `UI_TopMenu.Frame curFrame`（UI_顶部Menu.Frame curFrame）(偏移: 0x18)

### 方法 (7)

- `void Awake()`
  （void Awake（））
- `void OnMediaBtnDown()`
  （void OnMediaBtn下（））
- `void OnInvenBtnDown()`
  （void OnInvenBtn下（））
- `void OnBackBtnDown()`
  （void On后Btn下（））
- `void ChangeFrame(UI_TopMenu.Frame newFrame)`
  （void ChangeFrame（UI_顶部Menu.Frame newFrame））
- `void SetFrameVisible(UI_TopMenu.Frame frame, bool visible)`
  （void 集合Frame可见的（UI_顶部Menu.Frame frame, bool visible））
- `void PlayBGM(int index)`
  （void 播放BGM（int index））

---

## UI_TopMenu.Frame（UI_顶部Menu.Frame）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UInt16（UInt16）

**继承**: IComparable, IFormattable, IConvertible, IComparable<ushort>, IEquatable<ushort>（IComparable, IFormattable, IConvertible, IComparable<ushort>, IEquatable<ushort>）

### 字段 (1)

- `ushort m_value`（ushort m_value）(偏移: 0x0)

### 方法 (13)

- `int CompareTo(object value)`
  （int CompareTo（object value））
- `int CompareTo(ushort value)`
  （int CompareTo（ushort value））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `bool Equals(ushort obj)`
  （bool Equals（ushort obj））
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
- `ushort Parse(string s, IFormatProvider provider)`
  （ushort 解析（string s, I格式化提供者 provider））
- `ushort Parse(string s, NumberStyles style, IFormatProvider provider)`
  （ushort 解析（string s, NumberStyles style, I格式化提供者 provider））
- `ushort Parse(string s, NumberStyles style, NumberFormatInfo info)`
  （ushort 解析（string s, NumberStyles style, Number格式化信息 info））
- `TypeCode GetTypeCode()`
  （类型Code 获取类型Code（））

---

## UInt16ArrayTypeInfo（UInt16数组类型信息）

**继承**: TraceLoggingTypeInfo<ushort[]>（TraceLogging类型Info<ushort[]>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void WriteMetadata（TraceLoggingMetadataCollector collector, string name, 事件Field格式化 format））
- `void WriteData(TraceLoggingDataCollector collector, ref ushort[] value)`
  （void Write数据（TraceLogging数据Collector collector, ref ushort[] value））

---

## UInt16Converter（UInt16Converter）

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

## UInt16Enum（UInt16Enum）

### 字段 (1)

- `ushort value__`（ushort value__）(偏移: 0x0)

---

## UInt16TypeInfo（UInt16类型信息）

**继承**: TraceLoggingTypeInfo<ushort>（TraceLogging类型Info<ushort>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void WriteMetadata（TraceLoggingMetadataCollector collector, string name, 事件Field格式化 format））
- `void WriteData(TraceLoggingDataCollector collector, ref ushort value)`
  （void Write数据（TraceLogging数据Collector collector, ref ushort value））

---

## UInt32（UInt32）

**继承**: IComparable, IFormattable, IConvertible, IComparable<uint>, IEquatable<uint>（IComparable, IFormattable, IConvertible, IComparable<uint>, IEquatable<uint>）

### 字段 (1)

- `uint m_value`（uint m_value）(偏移: 0x0)

### 方法 (13)

- `int CompareTo(object value)`
  （int CompareTo（object value））
- `int CompareTo(uint value)`
  （int CompareTo（uint value））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `bool Equals(uint obj)`
  （bool Equals（uint obj））
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
- `uint Parse(string s, IFormatProvider provider)`
  （uint 解析（string s, I格式化提供者 provider））
- `uint Parse(string s, NumberStyles style, IFormatProvider provider)`
  （uint 解析（string s, NumberStyles style, I格式化提供者 provider））
- `bool TryParse(string s, out uint result)`
  （bool Try解析（string s, out uint result））
- `TypeCode GetTypeCode()`
  （类型Code 获取类型Code（））

---

## UInt32ArrayTypeInfo（UInt32数组类型信息）

**继承**: TraceLoggingTypeInfo<uint[]>（TraceLogging类型Info<uint[]>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void WriteMetadata（TraceLoggingMetadataCollector collector, string name, 事件Field格式化 format））
- `void WriteData(TraceLoggingDataCollector collector, ref uint[] value)`
  （void Write数据（TraceLogging数据Collector collector, ref uint[] value））

---

## UInt32Converter（UInt32Converter）

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

## UInt32Enum（UInt32Enum）

### 字段 (1)

- `uint value__`（uint value__）(偏移: 0x0)

---

## UInt32TypeInfo（UInt32类型信息）

**继承**: TraceLoggingTypeInfo<uint>（TraceLogging类型Info<uint>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void WriteMetadata（TraceLoggingMetadataCollector collector, string name, 事件Field格式化 format））
- `void WriteData(TraceLoggingDataCollector collector, ref uint value)`
  （void Write数据（TraceLogging数据Collector collector, ref uint value））

---

## UInt64（UInt64）

**继承**: IComparable, IFormattable, IConvertible, IComparable<ulong>, IEquatable<ulong>（IComparable, IFormattable, IConvertible, IComparable<ulong>, IEquatable<ulong>）

### 字段 (1)

- `ulong m_value`（ulong m_value）(偏移: 0x0)

### 方法 (13)

- `int CompareTo(object value)`
  （int CompareTo（object value））
- `int CompareTo(ulong value)`
  （int CompareTo（ulong value））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `bool Equals(ulong obj)`
  （bool Equals（ulong obj））
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
- `ulong Parse(string s, IFormatProvider provider)`
  （ulong 解析（string s, I格式化提供者 provider））
- `ulong Parse(string s, NumberStyles style, IFormatProvider provider)`
  （ulong 解析（string s, NumberStyles style, I格式化提供者 provider））
- `bool TryParse(string s, out ulong result)`
  （bool Try解析（string s, out ulong result））
- `TypeCode GetTypeCode()`
  （类型Code 获取类型Code（））

---

## UInt64ArrayTypeInfo（UInt64数组类型信息）

**继承**: TraceLoggingTypeInfo<ulong[]>（TraceLogging类型Info<ulong[]>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void WriteMetadata（TraceLoggingMetadataCollector collector, string name, 事件Field格式化 format））
- `void WriteData(TraceLoggingDataCollector collector, ref ulong[] value)`
  （void Write数据（TraceLogging数据Collector collector, ref ulong[] value））

---

## UInt64Converter（UInt64Converter）

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

## UInt64Enum（UInt64Enum）

### 字段 (1)

- `ulong value__`（ulong value__）(偏移: 0x0)

---

## UInt64TypeInfo（UInt64类型信息）

**继承**: TraceLoggingTypeInfo<ulong>（TraceLogging类型Info<ulong>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void WriteMetadata（TraceLoggingMetadataCollector collector, string name, 事件Field格式化 format））
- `void WriteData(TraceLoggingDataCollector collector, ref ulong value)`
  （void Write数据（TraceLogging数据Collector collector, ref ulong value））

---

## UIntPtr（U整数Ptr）

**继承**: ISerializable（ISerializable）

### 字段 (2)

- `UIntPtr Zero`（U整数Ptr Zero）(偏移: 0x0)
- `void* _pointer`（void* _pointer）(偏移: 0x0)

### 方法 (7)

- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））
- `string ToString()`
  （string To字符串（））
- `bool op_Equality(UIntPtr value1, UIntPtr value2)`
  （bool op_Equality（U整数Ptr value1, U整数Ptr value2））
- `ulong op_Explicit(UIntPtr value)`
  （ulong op_Explicit（U整数Ptr value））
- `UIntPtr op_Explicit(void* value)`
  （U整数Ptr op_Explicit（void* value））
- `int get_Size()`
  （int get_大小（））

---

## UIntPtrArrayTypeInfo（U整数Ptr数组类型信息）

**继承**: TraceLoggingTypeInfo<UIntPtr[]>（TraceLogging类型Info<U整数Ptr[]>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void WriteMetadata（TraceLoggingMetadataCollector collector, string name, 事件Field格式化 format））
- `void WriteData(TraceLoggingDataCollector collector, ref UIntPtr[] value)`
  （void Write数据（TraceLogging数据Collector collector, ref UIntPtr[] value））

---

## UIntPtrTypeInfo（U整数Ptr类型信息）

**继承**: TraceLoggingTypeInfo<UIntPtr>（TraceLogging类型Info<U整数Ptr>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void WriteMetadata（TraceLoggingMetadataCollector collector, string name, 事件Field格式化 format））
- `void WriteData(TraceLoggingDataCollector collector, ref UIntPtr value)`
  （void Write数据（TraceLogging数据Collector collector, ref UIntPtr value））

---

## URPProfileId（URPProfileId）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UTF32Encoding（UTF32Encoding）

**继承**: Encoding（Encoding）

### 字段 (3)

- `bool emitUTF32ByteOrderMark`（bool emitUTF32ByteOrderMark）(偏移: 0x1C)
- `bool isThrowException`（bool is投掷Exception）(偏移: 0x1D)
- `bool bigEndian`（bool bigEndian）(偏移: 0x1E)

### 方法 (26)

- `void SetDefaultFallbacks()`
  （void 集合默认的Fallbacks（））
- `int GetByteCount(char[] chars, int index, int count)`
  （int 获取Byte数量（char[] chars, int index, int count））
- `int GetByteCount(string s)`
  （int 获取Byte数量（string s））
- `int GetByteCount(char* chars, int count)`
  （int 获取Byte数量（char* chars, int count））
- `int GetBytes(string s, int charIndex, int charCount, byte[] bytes, int byteIndex)`
  （int 获取Bytes（string s, int charIndex, int charCount, byte[] bytes, int byteIndex））
- `int GetBytes(char[] chars, int charIndex, int charCount, byte[] bytes, int byteIndex)`
  （int 获取Bytes（char[] chars, int charIndex, int charCount, byte[] bytes, int byteIndex））
- `int GetBytes(char* chars, int charCount, byte* bytes, int byteCount)`
  （int 获取Bytes（char* chars, int charCount, byte* bytes, int byteCount））
- `int GetCharCount(byte[] bytes, int index, int count)`
  （int 获取Char数量（byte[] bytes, int index, int count））
- `int GetCharCount(byte* bytes, int count)`
  （int 获取Char数量（byte* bytes, int count））
- `int GetChars(byte[] bytes, int byteIndex, int byteCount, char[] chars, int charIndex)`
  （int 获取Chars（byte[] bytes, int byteIndex, int byteCount, char[] chars, int charIndex））
- `int GetChars(byte* bytes, int byteCount, char* chars, int charCount)`
  （int 获取Chars（byte* bytes, int byteCount, char* chars, int charCount））
- `string GetString(byte[] bytes, int index, int count)`
  （string 获取字符串（byte[] bytes, int index, int count））
- `int GetByteCount(char* chars, int count, EncoderNLS encoder)`
  （int 获取Byte数量（char* chars, int count, EncoderNLS encoder））
- `int GetBytes(char* chars, int charCount, byte* bytes, int byteCount, EncoderNLS encoder)`
  （int 获取Bytes（char* chars, int charCount, byte* bytes, int byteCount, EncoderNLS encoder））
- `int GetCharCount(byte* bytes, int count, DecoderNLS baseDecoder)`
  （int 获取Char数量（byte* bytes, int count, DecoderNLS baseDecoder））
- `int GetChars(byte* bytes, int byteCount, char* chars, int charCount, DecoderNLS baseDecoder)`
  （int 获取Chars（byte* bytes, int byteCount, char* chars, int charCount, DecoderNLS baseDecoder））
- `uint GetSurrogate(char cHigh, char cLow)`
  （uint 获取Surrogate（char cHigh, char cLow））
- `char GetHighSurrogate(uint iChar)`
  （char 获取HighSurrogate（uint iChar））
- `char GetLowSurrogate(uint iChar)`
  （char 获取LowSurrogate（uint iChar））
- `Decoder GetDecoder()`
  （Decoder 获取Decoder（））
- `Encoder GetEncoder()`
  （Encoder 获取Encoder（））
- `int GetMaxByteCount(int charCount)`
  （int 获取最大Byte数量（int charCount））
- `int GetMaxCharCount(int byteCount)`
  （int 获取最大Char数量（int byteCount））
- `byte[] GetPreamble()`
  （byte[] 获取Preamble（））
- `bool Equals(object value)`
  （bool Equals（object value））
- `int GetHashCode()`
  （int 获取HashCode（））

---

