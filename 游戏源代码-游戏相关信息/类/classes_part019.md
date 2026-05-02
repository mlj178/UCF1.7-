# 游戏类定义 (Part 19/21)

共 200 个类 (总序号 3601 - 3800)

---

## UTF32Encoding.UTF32Decoder（UTF32Encoding.UTF32Decoder）

**继承**: DecoderNLS（DecoderNLS）

### 字段 (2)

- `int iChar`（int iChar）(偏移: 0x1C)
- `int readByteCount`（int readByte数量）(偏移: 0x20)

### 方法 (2)

- `void Reset()`
  （void 重置（））
- `bool get_HasState()`
  （bool get_是否有状态（））

---

## UTF7Encoding（UTF7Encoding）

**继承**: Encoding（Encoding）

### 字段 (4)

- `byte[] base64Bytes`（byte[] base64Bytes）(偏移: 0x1C)
- `sbyte[] base64Values`（sbyte[] base64Values）(偏移: 0x20)
- `bool[] directEncode`（bool[] directEncode）(偏移: 0x24)
- `bool m_allowOptionals`（bool m_allowOptionals）(偏移: 0x28)

### 方法 (25)

- `void MakeTables()`
  （void MakeTables（））
- `void SetDefaultFallbacks()`
  （void 集合默认的Fallbacks（））
- `void OnDeserializing(StreamingContext ctx)`
  （void OnDeserializing（StreamingContext ctx））
- `void OnDeserialized(StreamingContext ctx)`
  （void OnDeserialized（StreamingContext ctx））
- `bool Equals(object value)`
  （bool Equals（object value））
- `int GetHashCode()`
  （int 获取HashCode（））
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
- `int GetByteCount(char* chars, int count, EncoderNLS baseEncoder)`
  （int 获取Byte数量（char* chars, int count, EncoderNLS baseEncoder））
- `int GetBytes(char* chars, int charCount, byte* bytes, int byteCount, EncoderNLS baseEncoder)`
  （int 获取Bytes（char* chars, int charCount, byte* bytes, int byteCount, EncoderNLS baseEncoder））
- `int GetCharCount(byte* bytes, int count, DecoderNLS baseDecoder)`
  （int 获取Char数量（byte* bytes, int count, DecoderNLS baseDecoder））
- `int GetChars(byte* bytes, int byteCount, char* chars, int charCount, DecoderNLS baseDecoder)`
  （int 获取Chars（byte* bytes, int byteCount, char* chars, int charCount, DecoderNLS baseDecoder））
- `Decoder GetDecoder()`
  （Decoder 获取Decoder（））
- `Encoder GetEncoder()`
  （Encoder 获取Encoder（））
- `int GetMaxByteCount(int charCount)`
  （int 获取最大Byte数量（int charCount））
- `int GetMaxCharCount(int byteCount)`
  （int 获取最大Char数量（int byteCount））

---

## UTF7Encoding.Decoder（UTF7Encoding.Decoder）

**继承**: DecoderNLS, ISerializable（DecoderNLS, ISerializable）

### 字段 (3)

- `int bits`（int bits）(偏移: 0x1C)
- `int bitCount`（int bit数量）(偏移: 0x20)
- `bool firstByte`（bool firstByte）(偏移: 0x24)

### 方法 (2)

- `void Reset()`
  （void 重置（））
- `bool get_HasState()`
  （bool get_是否有状态（））

---

## UTF7Encoding.DecoderUTF7Fallback（UTF7Encoding.DecoderUTF7Fallback）

**继承**: DecoderFallback（DecoderFallback）

### 方法 (4)

- `DecoderFallbackBuffer CreateFallbackBuffer()`
  （DecoderFallback缓冲区 创建Fallback缓冲区（））
- `int get_MaxCharCount()`
  （int get_最大Char数量（））
- `bool Equals(object value)`
  （bool Equals（object value））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## UTF7Encoding.DecoderUTF7FallbackBuffer（UTF7Encoding.DecoderUTF7Fallback缓冲区）

**继承**: DecoderFallbackBuffer（DecoderFallback缓冲区）

### 字段 (3)

- `char cFallback`（char cFallback）(偏移: 0x10)
- `int iCount`（int i数量）(偏移: 0x14)
- `int iSize`（int i大小）(偏移: 0x18)

### 方法 (4)

- `bool Fallback(byte[] bytesUnknown, int index)`
  （bool Fallback（byte[] bytesUnknown, int index））
- `char GetNextChar()`
  （char 获取下一个Char（））
- `void Reset()`
  （void 重置（））
- `int InternalFallback(byte[] bytes, byte* pBytes)`
  （int 内部的Fallback（byte[] bytes, byte* pBytes））

---

## UTF7Encoding.Encoder（UTF7Encoding.Encoder）

**继承**: EncoderNLS, ISerializable（EncoderNLS, ISerializable）

### 字段 (2)

- `int bits`（int bits）(偏移: 0x20)
- `int bitCount`（int bit数量）(偏移: 0x24)

### 方法 (1)

- `void Reset()`
  （void 重置（））

---

## UTF8Encoding（UTF8Encoding）

**继承**: Encoding（Encoding）

### 字段 (2)

- `bool emitUTF8Identifier`（bool emitUTF8Identifier）(偏移: 0x1C)
- `bool isThrowException`（bool is投掷Exception）(偏移: 0x1D)

### 方法 (29)

- `void SetDefaultFallbacks()`
  （void 集合默认的Fallbacks（））
- `int GetByteCount(char[] chars, int index, int count)`
  （int 获取Byte数量（char[] chars, int index, int count））
- `int GetByteCount(string chars)`
  （int 获取Byte数量（string chars））
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
- `int GetByteCount(char* chars, int count, EncoderNLS baseEncoder)`
  （int 获取Byte数量（char* chars, int count, EncoderNLS baseEncoder））
- `int PtrDiff(char* a, char* b)`
  （int PtrDiff（char* a, char* b））
- `int PtrDiff(byte* a, byte* b)`
  （int PtrDiff（byte* a, byte* b））
- `bool InRange(int ch, int start, int end)`
  （bool In范围（int ch, int start, int end））
- `int GetBytes(char* chars, int charCount, byte* bytes, int byteCount, EncoderNLS baseEncoder)`
  （int 获取Bytes（char* chars, int charCount, byte* bytes, int byteCount, EncoderNLS baseEncoder））
- `int GetCharCount(byte* bytes, int count, DecoderNLS baseDecoder)`
  （int 获取Char数量（byte* bytes, int count, DecoderNLS baseDecoder））
- `int GetChars(byte* bytes, int byteCount, char* chars, int charCount, DecoderNLS baseDecoder)`
  （int 获取Chars（byte* bytes, int byteCount, char* chars, int charCount, DecoderNLS baseDecoder））
- `bool FallbackInvalidByteSequence(ref byte* pSrc, int ch, DecoderFallbackBuffer fallback, ref char* pTarget)`
  （bool FallbackInvalidByteSequence（ref byte* pSrc, int ch, DecoderFallback缓冲区 fallback, ref char* pTarget））
- `int FallbackInvalidByteSequence(byte* pSrc, int ch, DecoderFallbackBuffer fallback)`
  （int FallbackInvalidByteSequence（byte* pSrc, int ch, DecoderFallback缓冲区 fallback））
- `byte[] GetBytesUnknown(ref byte* pSrc, int ch)`
  （byte[] 获取BytesUnknown（ref byte* pSrc, int ch））
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

## UTF8Encoding.UTF8Decoder（UTF8Encoding.UTF8Decoder）

**继承**: DecoderNLS, ISerializable（DecoderNLS, ISerializable）

### 字段 (1)

- `int bits`（int bits）(偏移: 0x1C)

### 方法 (2)

- `void Reset()`
  （void 重置（））
- `bool get_HasState()`
  （bool get_是否有状态（））

---

## UTF8Encoding.UTF8Encoder（UTF8Encoding.UTF8Encoder）

**继承**: EncoderNLS, ISerializable（EncoderNLS, ISerializable）

### 字段 (1)

- `int surrogateChar`（int surrogateChar）(偏移: 0x20)

### 方法 (1)

- `void Reset()`
  （void 重置（））

---

## UintOptions（UintOptions）

**继承**: IPlugOptions（IPlugOptions）

### 字段 (1)

- `bool isNegativeChangeValue`（bool isNegativeChange值）(偏移: 0x0)

### 方法 (1)

- `void Reset()`
  （void 重置（））

---

## UintPlugin（Uint插件）

**继承**: ABSTweenPlugin<uint, uint, UintOptions>（ABSTweenPlugin<uint, uint, UintOptions>）

### 方法 (8)

- `void Reset(TweenerCore<uint, uint, UintOptions> t)`
  （void 重置（TweenerCore<uint, uint, UintOptions> t））
- `void SetFrom(TweenerCore<uint, uint, UintOptions> t, bool isRelative)`
  （void 集合From（TweenerCore<uint, uint, UintOptions> t, bool isRelative））
- `void SetFrom(TweenerCore<uint, uint, UintOptions> t, uint fromValue, bool setImmediately, bool isRelative)`
  （void 集合From（TweenerCore<uint, uint, UintOptions> t, uint fromValue, bool setImmediately, bool isRelative））
- `uint ConvertToStartValue(TweenerCore<uint, uint, UintOptions> t, uint value)`
  （uint 转换To开始值（TweenerCore<uint, uint, UintOptions> t, uint value））
- `void SetRelativeEndValue(TweenerCore<uint, uint, UintOptions> t)`
  （void 集合Relative结束值（TweenerCore<uint, uint, UintOptions> t））
- `void SetChangeValue(TweenerCore<uint, uint, UintOptions> t)`
  （void 集合Change值（TweenerCore<uint, uint, UintOptions> t））
- `float GetSpeedBasedDuration(UintOptions options, float unitsXSecond, uint changeValue)`
  （float 获取SpeedBased持续时间（UintOptions options, float unitsXSecond, uint changeValue））
- `void EvaluateAndApply(UintOptions options, Tween t, bool isRelative, DOGetter<uint> getter, DOSetter<uint> setter, float elapsed, uint startValue, uint changeValue, float duration, bool usingInversePosition, UpdateNotice updateNotice)`
  （void EvaluateAnd应用（UintOptions options, Tween t, bool isRelative, DOGetter<uint> getter, DOSetter<uint> setter, float elapsed, uint startValue, uint changeValue, float duration, bool usingInversePosition, 更新Notice updateNotice））

---

## UlongPlugin（Ulong插件）

**继承**: ABSTweenPlugin<ulong, ulong, NoOptions>（ABSTweenPlugin<ulong, ulong, NoOptions>）

### 方法 (8)

- `void Reset(TweenerCore<ulong, ulong, NoOptions> t)`
  （void 重置（TweenerCore<ulong, ulong, NoOptions> t））
- `void SetFrom(TweenerCore<ulong, ulong, NoOptions> t, bool isRelative)`
  （void 集合From（TweenerCore<ulong, ulong, NoOptions> t, bool isRelative））
- `void SetFrom(TweenerCore<ulong, ulong, NoOptions> t, ulong fromValue, bool setImmediately, bool isRelative)`
  （void 集合From（TweenerCore<ulong, ulong, NoOptions> t, ulong fromValue, bool setImmediately, bool isRelative））
- `ulong ConvertToStartValue(TweenerCore<ulong, ulong, NoOptions> t, ulong value)`
  （ulong 转换To开始值（TweenerCore<ulong, ulong, NoOptions> t, ulong value））
- `void SetRelativeEndValue(TweenerCore<ulong, ulong, NoOptions> t)`
  （void 集合Relative结束值（TweenerCore<ulong, ulong, NoOptions> t））
- `void SetChangeValue(TweenerCore<ulong, ulong, NoOptions> t)`
  （void 集合Change值（TweenerCore<ulong, ulong, NoOptions> t））
- `float GetSpeedBasedDuration(NoOptions options, float unitsXSecond, ulong changeValue)`
  （float 获取SpeedBased持续时间（NoOptions options, float unitsXSecond, ulong changeValue））
- `void EvaluateAndApply(NoOptions options, Tween t, bool isRelative, DOGetter<ulong> getter, DOSetter<ulong> setter, float elapsed, ulong startValue, ulong changeValue, float duration, bool usingInversePosition, UpdateNotice updateNotice)`
  （void EvaluateAnd应用（NoOptions options, Tween t, bool isRelative, DOGetter<ulong> getter, DOSetter<ulong> setter, float elapsed, ulong startValue, ulong changeValue, float duration, bool usingInversePosition, 更新Notice updateNotice））

---

## UltimateResourceFallbackLocation（Ultimate资源FallbackLocation）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UmAlQuraCalendar（UmAlQuraCalendar）

**继承**: Calendar（Calendar）

### 字段 (3)

- `UmAlQuraCalendar.DateMapping[] HijriYearInfo`（UmAlQuraCalendar.DateMapping[] HijriYear信息）(偏移: 0x0)
- `DateTime minDate`（Date时间 minDate）(偏移: 0x8)
- `DateTime maxDate`（Date时间 maxDate）(偏移: 0x10)

### 方法 (27)

- `UmAlQuraCalendar.DateMapping[] InitDateMapping()`
  （UmAlQuraCalendar.DateMapping[] 初始化DateMapping（））
- `DateTime get_MinSupportedDateTime()`
  （Date时间 get_最小SupportedDate时间（））
- `DateTime get_MaxSupportedDateTime()`
  （Date时间 get_最大SupportedDate时间（））
- `int get_BaseCalendarID()`
  （int get_基础CalendarID（））
- `int get_ID()`
  （int get_ID（））
- `void ConvertHijriToGregorian(int HijriYear, int HijriMonth, int HijriDay, ref int yg, ref int mg, ref int dg)`
  （void 转换HijriToGregorian（int HijriYear, int HijriMonth, int HijriDay, ref int yg, ref int mg, ref int dg））
- `long GetAbsoluteDateUmAlQura(int year, int month, int day)`
  （long 获取AbsoluteDateUmAlQura（int year, int month, int day））
- `void CheckTicksRange(long ticks)`
  （void 检查Ticks范围（long ticks））
- `void CheckEraRange(int era)`
  （void 检查Era范围（int era））
- `void CheckYearRange(int year, int era)`
  （void 检查Year范围（int year, int era））
- `void CheckYearMonthRange(int year, int month, int era)`
  （void 检查YearMonth范围（int year, int month, int era））
- `void ConvertGregorianToHijri(DateTime time, ref int HijriYear, ref int HijriMonth, ref int HijriDay)`
  （void 转换GregorianToHijri（Date时间 time, ref int HijriYear, ref int HijriMonth, ref int HijriDay））
- `int GetDatePart(DateTime time, int part)`
  （int 获取DatePart（Date时间 time, int part））
- `int GetDayOfMonth(DateTime time)`
  （int 获取DayOfMonth（Date时间 time））
- `DayOfWeek GetDayOfWeek(DateTime time)`
  （DayOfWeek 获取DayOfWeek（Date时间 time））
- `int GetDaysInMonth(int year, int month, int era)`
  （int 获取DaysInMonth（int year, int month, int era））
- `int RealGetDaysInYear(int year)`
  （int Real获取DaysInYear（int year））
- `int GetDaysInYear(int year, int era)`
  （int 获取DaysInYear（int year, int era））
- `int GetEra(DateTime time)`
  （int 获取Era（Date时间 time））
- `int[] get_Eras()`
  （int[] get_Eras（））
- `int GetMonth(DateTime time)`
  （int 获取Month（Date时间 time））
- `int GetMonthsInYear(int year, int era)`
  （int 获取MonthsInYear（int year, int era））
- `int GetYear(DateTime time)`
  （int 获取Year（Date时间 time））
- `bool IsLeapYear(int year, int era)`
  （bool 是否LeapYear（int year, int era））
- `DateTime ToDateTime(int year, int month, int day, int hour, int minute, int second, int millisecond, int era)`
  （Date时间 ToDate时间（int year, int month, int day, int hour, int minute, int second, int millisecond, int era））
- `int get_TwoDigitYearMax()`
  （int get_TwoDigitYear最大（））
- `int ToFourDigitYear(int year)`
  （int ToFourDigitYear（int year））

---

## UmAlQuraCalendar.DateMapping（UmAlQuraCalendar.DateMapping）

### 字段 (2)

- `int HijriMonthsLengthFlags`（int HijriMonthsLengthFlags）(偏移: 0x0)
- `DateTime GregorianDate`（Date时间 GregorianDate）(偏移: 0x8)

---

## UnSafeCharBuffer（UnSafeChar缓冲区）

### 字段 (3)

- `char* m_buffer`（char* m_buffer）(偏移: 0x0)
- `int m_totalSize`（int m_total大小）(偏移: 0x4)
- `int m_length`（int m_length）(偏移: 0x8)

### 方法 (1)

- `void AppendString(string stringToAppend)`
  （void Append字符串（string stringToAppend））

---

## UncNameHelper（Unc名称辅助器）

### 方法 (2)

- `string ParseCanonicalName(string str, int start, int end, ref bool loopback)`
  （string 解析Canonical名称（string str, int start, int end, ref bool loopback））
- `bool IsValid(char* name, ushort start, ref int returnedEnd, bool notImplicitFile)`
  （bool 是否Valid（char* name, ushort start, ref int returnedEnd, bool notImplicitFile））

---

## UnescapeMode（Unescape模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UnexceptionalStreamReader（Unexceptional流读取器）

**继承**: StreamReader（流读取器）

### 字段 (2)

- `bool[] newline`（bool[] newline）(偏移: 0x0)
- `char newlineChar`（char newlineChar）(偏移: 0x4)

### 方法 (6)

- `int Peek()`
  （int Peek（））
- `int Read()`
  （int Read（））
- `int Read([In] [Out] char[] dest_buffer, int index, int count)`
  （int Read（[In] [Out] char[] dest_buffer, int index, int count））
- `bool CheckEOL(char current)`
  （bool 检查EOL（char current））
- `string ReadLine()`
  （string ReadLine（））
- `string ReadToEnd()`
  （string ReadTo结束（））

---

## UnexceptionalStreamWriter（Unexceptional流写入器）

**继承**: StreamWriter（流写入器）

### 方法 (5)

- `void Flush()`
  （void Flush（））
- `void Write(char[] buffer, int index, int count)`
  （void Write（char[] buffer, int index, int count））
- `void Write(char value)`
  （void Write（char value））
- `void Write(char[] value)`
  （void Write（char[] value））
- `void Write(string value)`
  （void Write（string value））

---

## UnhandledExceptionEventArgs（UnhandledException事件Args）

**继承**: EventArgs（事件Args）

### 字段 (2)

- `object _Exception`（object _Exception）(偏移: 0x8)
- `bool _IsTerminating`（bool _是否Terminating）(偏移: 0xC)

### 方法 (2)

- `object get_ExceptionObject()`
  （object get_Exception对象（））
- `bool get_IsTerminating()`
  （bool get_是否Terminating（））

---

## UnhandledExceptionEventHandler（UnhandledException事件处理器）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(object sender, UnhandledExceptionEventArgs e)`
  （void Invoke（object sender, UnhandledException事件Args e））
- `IAsyncResult BeginInvoke(object sender, UnhandledExceptionEventArgs e, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（object sender, UnhandledException事件Args e, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## UnhandledExceptionHandler（UnhandledException处理器）

### 方法 (1)

- `void RegisterUECatcher()`
  （void RegisterUECatcher（））

---

## UnicodeCategory（Unicode类别）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UnicodeEncoding（UnicodeEncoding）

**继承**: Encoding（Encoding）

### 字段 (4)

- `bool isThrowException`（bool is投掷Exception）(偏移: 0x1C)
- `bool bigEndian`（bool bigEndian）(偏移: 0x1D)
- `bool byteOrderMark`（bool byteOrderMark）(偏移: 0x1E)
- `ulong highLowPatternMask`（ulong highLowPattern掩码）(偏移: 0x0)

### 方法 (24)

- `void OnDeserializing(StreamingContext ctx)`
  （void OnDeserializing（StreamingContext ctx））
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
- `Encoder GetEncoder()`
  （Encoder 获取Encoder（））
- `Decoder GetDecoder()`
  （Decoder 获取Decoder（））
- `byte[] GetPreamble()`
  （byte[] 获取Preamble（））
- `int GetMaxByteCount(int charCount)`
  （int 获取最大Byte数量（int charCount））
- `int GetMaxCharCount(int byteCount)`
  （int 获取最大Char数量（int byteCount））
- `bool Equals(object value)`
  （bool Equals（object value））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## UnicodeEncoding.Decoder（UnicodeEncoding.Decoder）

**继承**: DecoderNLS, ISerializable（DecoderNLS, ISerializable）

### 字段 (2)

- `int lastByte`（int lastByte）(偏移: 0x1C)
- `char lastChar`（char lastChar）(偏移: 0x20)

### 方法 (2)

- `void Reset()`
  （void 重置（））
- `bool get_HasState()`
  （bool get_是否有状态（））

---

## UniqueComponentAttribute（Unique组件Attribute）

**继承**: Attribute（Attribute）

### 字段 (1)

- `string tag`（string tag）(偏移: 0x8)

---

## UnityAction（Unity引擎动作）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke()`
  （void Invoke（））
- `IAsyncResult BeginInvoke(AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## UnityEvent（Unity引擎事件）

**继承**: UnityEventBase（Unity引擎事件基础）

### 字段 (1)

- `object[] m_InvokeArray`（object[] m_Invoke数组）(偏移: 0x14)

### 方法 (5)

- `void AddListener(UnityAction call)`
  （void 添加监听器（Unity引擎动作 call））
- `MethodInfo FindMethod_Impl(string name, Type targetObjType)`
  （Method信息 查找Method_Impl（string name, 类型 targetObjType））
- `BaseInvokableCall GetDelegate(object target, MethodInfo theFunction)`
  （基础InvokableCall 获取委托（object target, Method信息 theFunction））
- `BaseInvokableCall GetDelegate(UnityAction action)`
  （基础InvokableCall 获取委托（Unity引擎动作 action））
- `void Invoke()`
  （void Invoke（））

---

## UnityEventBase（Unity引擎事件基础）

**继承**: ISerializationCallbackReceiver（ISerialization回调Receiver）

### 字段 (3)

- `InvokableCallList m_Calls`（InvokableCall列表 m_Calls）(偏移: 0x8)
- `PersistentCallGroup m_PersistentCalls`（持久的Call组 m_持久的Calls）(偏移: 0xC)
- `bool m_CallsDirty`（bool m_CallsDirty）(偏移: 0x10)

### 方法 (9)

- `MethodInfo FindMethod(PersistentCall call)`
  （Method信息 查找Method（持久的Call call））
- `MethodInfo FindMethod(string name, Type listenerType, PersistentListenerMode mode, Type argumentType)`
  （Method信息 查找Method（string name, 类型 listenerType, 持久的监听器模式 mode, 类型 argumentType））
- `void DirtyPersistentCalls()`
  （void Dirty持久的Calls（））
- `void RebuildPersistentCallsIfNeeded()`
  （void Rebuild持久的CallsIfNeeded（））
- `void AddCall(BaseInvokableCall call)`
  （void 添加Call（基础InvokableCall call））
- `void RemoveListener(object targetObj, MethodInfo method)`
  （void 移除监听器（object targetObj, Method信息 method））
- `List<BaseInvokableCall> PrepareInvoke()`
  （List<基础InvokableCall> PrepareInvoke（））
- `string ToString()`
  （string To字符串（））
- `MethodInfo GetValidMethodInfo(Type objectType, string functionName, Type[] argumentTypes)`
  （Method信息 获取ValidMethod信息（类型 objectType, string functionName, Type[] argumentTypes））

---

## UnityEventCallState（Unity引擎事件Call状态）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UnityEventTools（Unity引擎事件Tools）

### 方法 (1)

- `string TidyAssemblyTypeName(string assemblyTypeName)`
  （string TidyAssembly类型名称（string assemblyTypeName））

---

## UnityLogWriter（Unity引擎Log写入器）

**继承**: TextWriter（文本写入器）

### 方法 (6)

- `void WriteStringToUnityLog(string s)`
  （void Write字符串ToUnity引擎Log（string s））
- `void WriteStringToUnityLogImpl(string s)`
  （void Write字符串ToUnity引擎LogImpl（string s））
- `void Init()`
  （void 初始化（））
- `void Write(char value)`
  （void Write（char value））
- `void Write(string s)`
  （void Write（string s））
- `void Write(char[] buffer, int index, int count)`
  （void Write（char[] buffer, int index, int count））

---

## UnityQuaternionExtensions（Unity引擎QuaternionExtensions）

### 方法 (4)

- `Quaternion SlerpWithReferenceUp(Quaternion qA, Quaternion qB, float t, Vector3 up)`
  （Quaternion SlerpWith引用上（Quaternion qA, Quaternion qB, float t, 三维向量 up））
- `Quaternion Normalized(Quaternion q)`
  （Quaternion Normalized（Quaternion q））
- `Vector2 GetCameraRotationToTarget(Quaternion orient, Vector3 lookAtDir, Vector3 worldUp)`
  （二维向量 获取摄像机RotationTo目标（Quaternion orient, 三维向量 lookAtDir, 三维向量 worldUp））
- `Quaternion ApplyCameraRotation(Quaternion orient, Vector2 rot, Vector3 worldUp)`
  （Quaternion 应用摄像机Rotation（Quaternion orient, 二维向量 rot, 三维向量 worldUp））

---

## UnityRectExtensions（Unity引擎RectExtensions）

### 方法 (1)

- `Rect Inflated(Rect r, Vector2 delta)`
  （Rect Inflated（Rect r, 二维向量 delta））

---

## UnityReferenceHelper（Unity引擎引用辅助器）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (1)

- `string guid`（string guid）(偏移: 0xC)

### 方法 (3)

- `string GetGUID()`
  （string 获取GUID（））
- `void Awake()`
  （void Awake（））
- `void Reset()`
  （void 重置（））

---

## UnitySerializationHolder（Unity引擎SerializationHolder）

**继承**: ISerializable, IObjectReference（ISerializable, I对象引用）

### 字段 (8)

- `Type[] m_instantiation`（Type[] m_instantiation）(偏移: 0x8)
- `int[] m_elementTypes`（int[] m_elementTypes）(偏移: 0xC)
- `int m_genericParameterPosition`（int m_genericParameterPosition）(偏移: 0x10)
- `Type m_declaringType`（类型 m_declaring类型）(偏移: 0x14)
- `MethodBase m_declaringMethod`（Method基础 m_declaringMethod）(偏移: 0x18)
- `string m_data`（string m_data）(偏移: 0x1C)
- `string m_assemblyName`（string m_assembly名称）(偏移: 0x20)
- `int m_unityType`（int m_unity类型）(偏移: 0x24)

### 方法 (8)

- `void GetUnitySerializationInfo(SerializationInfo info, Missing missing)`
  （void 获取Unity引擎Serialization信息（Serialization信息 info, Missing missing））
- `RuntimeType AddElementTypes(SerializationInfo info, RuntimeType type)`
  （Runtime类型 添加元素Types（Serialization信息 info, Runtime类型 type））
- `Type MakeElementTypes(Type type)`
  （类型 Make元素Types（类型 type））
- `void GetUnitySerializationInfo(SerializationInfo info, RuntimeType type)`
  （void 获取Unity引擎Serialization信息（Serialization信息 info, Runtime类型 type））
- `void GetUnitySerializationInfo(SerializationInfo info, int unityType, string data, RuntimeAssembly assembly)`
  （void 获取Unity引擎Serialization信息（Serialization信息 info, int unityType, string data, RuntimeAssembly assembly））
- `void ThrowInsufficientInformation(string field)`
  （void 投掷InsufficientInformation（string field））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））
- `object GetRealObject(StreamingContext context)`
  （object 获取Real对象（StreamingContext context））

---

## UnityString（Unity引擎字符串）

### 方法 (1)

- `string Format(string fmt, object[] args)`
  （string 格式化（string fmt, object[] args））

---

## UnitySynchronizationContext（Unity引擎SynchronizationContext）

**继承**: SynchronizationContext（SynchronizationContext）

### 字段 (4)

- `List<UnitySynchronizationContext.WorkRequest> m_AsyncWorkQueue`（List<Unity引擎SynchronizationContext.WorkRequest> m_异步Work队列）(偏移: 0xC)
- `List<UnitySynchronizationContext.WorkRequest> m_CurrentFrameWork`（List<Unity引擎SynchronizationContext.WorkRequest> m_当前FrameWork）(偏移: 0x10)
- `int m_MainThreadID`（int m_主要的ThreadID）(偏移: 0x14)
- `int m_TrackedCount`（int m_Tracked数量）(偏移: 0x18)

### 方法 (8)

- `void Send(SendOrPostCallback callback, object state)`
  （void 发送（发送OrPost回调 callback, object state））
- `void Post(SendOrPostCallback callback, object state)`
  （void Post（发送OrPost回调 callback, object state））
- `SynchronizationContext CreateCopy()`
  （SynchronizationContext 创建复制（））
- `void Exec()`
  （void Exec（））
- `bool HasPendingTasks()`
  （bool 是否有PendingTasks（））
- `void InitializeSynchronizationContext()`
  （void 初始化SynchronizationContext（））
- `void ExecuteTasks()`
  （void 执行Tasks（））
- `bool ExecutePendingTasks(long millisecondsTimeout)`
  （bool 执行PendingTasks（long millisecondsTimeout））

---

## UnitySynchronizationContext.WorkRequest（Unity引擎SynchronizationContext.Work请求）

### 字段 (3)

- `SendOrPostCallback m_DelagateCallback`（发送OrPost回调 m_Delagate回调）(偏移: 0x0)
- `object m_DelagateState`（object m_Delagate状态）(偏移: 0x4)
- `ManualResetEvent m_WaitHandle`（手动重置事件 m_Wait句柄）(偏移: 0x8)

### 方法 (1)

- `void Invoke()`
  （void Invoke（））

---

## UnityVectorExtensions（Unity引擎向量Extensions）

### 方法 (9)

- `float ClosestPointOnSegment(Vector3 p, Vector3 s0, Vector3 s1)`
  （float ClosestPointOnSegment（三维向量 p, 三维向量 s0, 三维向量 s1））
- `float ClosestPointOnSegment(Vector2 p, Vector2 s0, Vector2 s1)`
  （float ClosestPointOnSegment（二维向量 p, 二维向量 s0, 二维向量 s1））
- `Vector3 ProjectOntoPlane(Vector3 vector, Vector3 planeNormal)`
  （三维向量 ProjectOntoPlane（三维向量 vector, 三维向量 planeNormal））
- `Vector3 Abs(Vector3 v)`
  （三维向量 Abs（三维向量 v））
- `bool AlmostZero(Vector3 v)`
  （bool AlmostZero（三维向量 v））
- `float Angle(Vector3 v1, Vector3 v2)`
  （float 角度（三维向量 v1, 三维向量 v2））
- `float SignedAngle(Vector3 v1, Vector3 v2, Vector3 up)`
  （float Signed角度（三维向量 v1, 三维向量 v2, 三维向量 up））
- `Quaternion SafeFromToRotation(Vector3 v1, Vector3 v2, Vector3 up)`
  （Quaternion SafeFromToRotation（三维向量 v1, 三维向量 v2, 三维向量 up））
- `Vector3 SlerpWithReferenceUp(Vector3 vA, Vector3 vB, float t, Vector3 up)`
  （三维向量 SlerpWith引用上（三维向量 vA, 三维向量 vB, float t, 三维向量 up））

---

## UnityWebRequest（Unity引擎Web请求）

**继承**: IDisposable（IDisposable）

### 字段 (5)

- `IntPtr m_Ptr`（整数Ptr m_Ptr）(偏移: 0x8)
- `DownloadHandler m_DownloadHandler`（Download处理器 m_Download处理器）(偏移: 0xC)
- `UploadHandler m_UploadHandler`（Upload处理器 m_Upload处理器）(偏移: 0x10)
- `CertificateHandler m_CertificateHandler`（Certificate处理器 m_Certificate处理器）(偏移: 0x14)
- `Uri m_Uri`（Uri m_Uri）(偏移: 0x18)

### 方法 (41)

- `string GetWebErrorString(UnityWebRequest.UnityWebRequestError err)`
  （string 获取WebError字符串（Unity引擎WebRequest.Unity引擎Web请求Error err））
- `string GetHTTPStatusString(long responseCode)`
  （string 获取HTTPStatus字符串（long responseCode））
- `bool get_disposeCertificateHandlerOnDispose()`
  （bool get_disposeCertificate处理器On释放（））
- `void set_disposeCertificateHandlerOnDispose(bool value)`
  （void set_disposeCertificate处理器On释放（bool value））
- `bool get_disposeDownloadHandlerOnDispose()`
  （bool get_disposeDownload处理器On释放（））
- `void set_disposeDownloadHandlerOnDispose(bool value)`
  （void set_disposeDownload处理器On释放（bool value））
- `bool get_disposeUploadHandlerOnDispose()`
  （bool get_disposeUpload处理器On释放（））
- `void set_disposeUploadHandlerOnDispose(bool value)`
  （void set_disposeUpload处理器On释放（bool value））
- `IntPtr Create()`
  （整数Ptr 创建（））
- `void Release()`
  （void Release（））
- `void InternalDestroy()`
  （void 内部的销毁（））
- `void InternalSetDefaults()`
  （void 内部的集合Defaults（））
- `void Finalize()`
  （void Finalize（））
- `void Dispose()`
  （void 释放（））
- `void DisposeHandlers()`
  （void 释放Handlers（））
- `UnityWebRequestAsyncOperation BeginWebRequest()`
  （Unity引擎Web请求异步Operation BeginWeb请求（））
- `UnityWebRequestAsyncOperation SendWebRequest()`
  （Unity引擎Web请求异步Operation 发送Web请求（））
- `void Abort()`
  （void Abort（））
- `UnityWebRequest.UnityWebRequestError SetMethod(UnityWebRequest.UnityWebRequestMethod methodType)`
  （Unity引擎WebRequest.Unity引擎Web请求Error 集合Method（Unity引擎WebRequest.Unity引擎Web请求Method methodType））
- `void InternalSetMethod(UnityWebRequest.UnityWebRequestMethod methodType)`
  （void 内部的集合Method（Unity引擎WebRequest.Unity引擎Web请求Method methodType））
- `UnityWebRequest.UnityWebRequestError SetCustomMethod(string customMethodName)`
  （Unity引擎WebRequest.Unity引擎Web请求Error 集合自定义的Method（string customMethodName））
- `void InternalSetCustomMethod(string customMethodName)`
  （void 内部的集合自定义的Method（string customMethodName））
- `void set_method(string value)`
  （void set_method（string value））
- `UnityWebRequest.UnityWebRequestError GetError()`
  （Unity引擎WebRequest.Unity引擎Web请求Error 获取Error（））
- `string get_error()`
  （string get_error（））
- `void set_use100Continue(bool value)`
  （void set_use100Continue（bool value））
- `void set_useHttpContinue(bool value)`
  （void set_useHttpContinue（bool value））
- `void set_uri(Uri value)`
  （void set_uri（Uri value））
- `UnityWebRequest.UnityWebRequestError SetUrl(string url)`
  （Unity引擎WebRequest.Unity引擎Web请求Error 集合Url（string url））
- `void InternalSetUrl(string url)`
  （void 内部的集合Url（string url））
- `long get_responseCode()`
  （long get_responseCode（））
- `bool get_isModifiable()`
  （bool get_isModifiable（））
- `UnityWebRequest.Result get_result()`
  （Unity引擎WebRequest.Result get_result（））
- `string GetResponseHeader(string name)`
  （string 获取响应标题（string name））
- `UploadHandler get_uploadHandler()`
  （Upload处理器 get_upload处理器（））
- `DownloadHandler get_downloadHandler()`
  （Download处理器 get_download处理器（））
- `UnityWebRequest.UnityWebRequestError SetCertificateHandler(CertificateHandler ch)`
  （Unity引擎WebRequest.Unity引擎Web请求Error 集合Certificate处理器（Certificate处理器 ch））
- `CertificateHandler get_certificateHandler()`
  （Certificate处理器 get_certificate处理器（））
- `void set_certificateHandler(CertificateHandler value)`
  （void set_certificate处理器（Certificate处理器 value））
- `UnityWebRequest.UnityWebRequestError SetTimeoutMsec(int timeout)`
  （Unity引擎WebRequest.Unity引擎Web请求Error 集合超时Msec（int timeout））
- `void set_timeout(int value)`
  （void set_timeout（int value））

---

## UnityWebRequest.Result（Unity引擎WebRequest.Result）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UnityWebRequest.UnityWebRequestError（Unity引擎WebRequest.Unity引擎Web请求Error）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UnityWebRequest.UnityWebRequestMethod（Unity引擎WebRequest.Unity引擎Web请求Method）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UnityWebRequestAsyncOperation（Unity引擎Web请求异步Operation）

**继承**: AsyncOperation（异步Operation）

### 方法 (1)

- `void set_webRequest(UnityWebRequest value)`
  （void set_web请求（Unity引擎Web请求 value））

---

## UniversalAdditionalCameraData（UniversalAdditional摄像机数据）

**继承**: MonoBehaviour, ISerializationCallbackReceiver（MonoBehaviour行为, ISerialization回调Receiver）

### 字段 (22)

- `bool m_RenderShadows`（bool m_RenderShadows）(偏移: 0xC)
- `CameraOverrideOption m_RequiresDepthTextureOption`（摄像机重写Option m_Requires深度纹理Option）(偏移: 0x10)
- `CameraOverrideOption m_RequiresOpaqueTextureOption`（摄像机重写Option m_Requires不透明的纹理Option）(偏移: 0x14)
- `CameraRenderType m_CameraType`（摄像机Render类型 m_摄像机类型）(偏移: 0x18)
- `List<Camera> m_Cameras`（List<Camera> m_Cameras）(偏移: 0x1C)
- `int m_RendererIndex`（int m_渲染器索引）(偏移: 0x20)
- `LayerMask m_VolumeLayerMask`（层掩码 m_Volume层掩码）(偏移: 0x24)
- `Transform m_VolumeTrigger`（变换 m_Volume触发器）(偏移: 0x28)
- `VolumeFrameworkUpdateMode m_VolumeFrameworkUpdateModeOption`（VolumeFramework更新模式 m_VolumeFramework更新模式Option）(偏移: 0x2C)
- `bool m_RenderPostProcessing`（bool m_RenderPostProcessing）(偏移: 0x30)
- `AntialiasingMode m_Antialiasing`（Antialiasing模式 m_Antialiasing）(偏移: 0x34)
- `AntialiasingQuality m_AntialiasingQuality`（AntialiasingQuality m_AntialiasingQuality）(偏移: 0x38)
- `bool m_StopNaN`（bool m_停止NaN）(偏移: 0x3C)
- `bool m_Dithering`（bool m_Dithering）(偏移: 0x0)
- `bool m_ClearDepth`（bool m_清除深度）(偏移: 0x0)
- `bool m_AllowXRRendering`（bool m_允许XRRendering）(偏移: 0x0)
- `Camera m_Camera`（摄像机 m_摄像机）(偏移: 0x0)
- `bool m_RequiresDepthTexture`（bool m_Requires深度纹理）(偏移: 0x44)
- `bool m_RequiresColorTexture`（bool m_Requires颜色纹理）(偏移: 0x45)
- `float m_Version`（float m_Version）(偏移: 0x48)
- `UniversalAdditionalCameraData s_DefaultAdditionalCameraData`（UniversalAdditional摄像机数据 s_默认的Additional摄像机数据）(偏移: 0x0)
- `VolumeStack m_VolumeStack`（Volume栈 m_Volume栈）(偏移: 0x4C)

### 方法 (44)

- `float get_version()`
  （float get_version（））
- `UniversalAdditionalCameraData get_defaultAdditionalCameraData()`
  （UniversalAdditional摄像机数据 get_defaultAdditional摄像机数据（））
- `Camera get_camera()`
  （摄像机 get_camera（））
- `bool get_renderShadows()`
  （bool get_renderShadows（））
- `void set_renderShadows(bool value)`
  （void set_renderShadows（bool value））
- `CameraOverrideOption get_requiresDepthOption()`
  （摄像机重写Option get_requires深度Option（））
- `void set_requiresDepthOption(CameraOverrideOption value)`
  （void set_requires深度Option（摄像机重写Option value））
- `CameraOverrideOption get_requiresColorOption()`
  （摄像机重写Option get_requires颜色Option（））
- `void set_requiresColorOption(CameraOverrideOption value)`
  （void set_requires颜色Option（摄像机重写Option value））
- `CameraRenderType get_renderType()`
  （摄像机Render类型 get_render类型（））
- `void set_renderType(CameraRenderType value)`
  （void set_render类型（摄像机Render类型 value））
- `List<Camera> get_cameraStack()`
  （List<Camera> get_camera栈（））
- `void UpdateCameraStack()`
  （void 更新摄像机栈（））
- `bool get_clearDepth()`
  （bool get_clear深度（））
- `bool get_requiresDepthTexture()`
  （bool get_requires深度纹理（））
- `void set_requiresDepthTexture(bool value)`
  （void set_requires深度纹理（bool value））
- `bool get_requiresColorTexture()`
  （bool get_requires颜色纹理（））
- `void set_requiresColorTexture(bool value)`
  （void set_requires颜色纹理（bool value））
- `ScriptableRenderer get_scriptableRenderer()`
  （Scriptable渲染器 get_scriptable渲染器（））
- `void SetRenderer(int index)`
  （void 集合渲染器（int index））
- `LayerMask get_volumeLayerMask()`
  （层掩码 get_volume层掩码（））
- `void set_volumeLayerMask(LayerMask value)`
  （void set_volume层掩码（层掩码 value））
- `Transform get_volumeTrigger()`
  （变换 get_volume触发器（））
- `void set_volumeTrigger(Transform value)`
  （void set_volume触发器（变换 value））
- `VolumeFrameworkUpdateMode get_volumeFrameworkUpdateMode()`
  （VolumeFramework更新模式 get_volumeFramework更新模式（））
- `void set_volumeFrameworkUpdateMode(VolumeFrameworkUpdateMode value)`
  （void set_volumeFramework更新模式（VolumeFramework更新模式 value））
- `bool get_requiresVolumeFrameworkUpdate()`
  （bool get_requiresVolumeFramework更新（））
- `VolumeStack get_volumeStack()`
  （Volume栈 get_volume栈（））
- `void set_volumeStack(VolumeStack value)`
  （void set_volume栈（Volume栈 value））
- `bool get_renderPostProcessing()`
  （bool get_renderPostProcessing（））
- `void set_renderPostProcessing(bool value)`
  （void set_renderPostProcessing（bool value））
- `AntialiasingMode get_antialiasing()`
  （Antialiasing模式 get_antialiasing（））
- `void set_antialiasing(AntialiasingMode value)`
  （void set_antialiasing（Antialiasing模式 value））
- `AntialiasingQuality get_antialiasingQuality()`
  （AntialiasingQuality get_antialiasingQuality（））
- `void set_antialiasingQuality(AntialiasingQuality value)`
  （void set_antialiasingQuality（AntialiasingQuality value））
- `bool get_stopNaN()`
  （bool get_stopNaN（））
- `void set_stopNaN(bool value)`
  （void set_stopNaN（bool value））
- `bool get_dithering()`
  （bool get_dithering（））
- `void set_dithering(bool value)`
  （void set_dithering（bool value））
- `bool get_allowXRRendering()`
  （bool get_allowXRRendering（））
- `void set_allowXRRendering(bool value)`
  （void set_allowXRRendering（bool value））
- `void OnBeforeSerialize()`
  （void OnBeforeSerialize（））
- `void OnAfterDeserialize()`
  （void OnAfterDeserialize（））
- `void OnDrawGizmos()`
  （void OnDrawGizmos（））

---

## UniversalAdditionalLightData（UniversalAdditional光照数据）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (1)

- `bool m_UsePipelineSettings`（bool m_UsePipelineSettings）(偏移: 0xC)

### 方法 (2)

- `bool get_usePipelineSettings()`
  （bool get_usePipelineSettings（））
- `void set_usePipelineSettings(bool value)`
  （void set_usePipelineSettings（bool value））

---

## UniversalRenderPipeline（UniversalRenderPipeline）

**继承**: RenderPipeline（RenderPipeline）

### 字段 (10)

- `XRSystem m_XRSystem`（XR系统 m_XR系统）(偏移: 0x0)
- `Vector4 k_DefaultLightPosition`（Vector4 k_默认的光照Position）(偏移: 0x4)
- `Vector4 k_DefaultLightColor`（Vector4 k_默认的光照颜色）(偏移: 0x14)
- `Vector4 k_DefaultLightAttenuation`（Vector4 k_默认的光照Attenuation）(偏移: 0x24)
- `Vector4 k_DefaultLightSpotDirection`（Vector4 k_默认的光照Spot方向）(偏移: 0x34)
- `Vector4 k_DefaultLightsProbeChannel`（Vector4 k_默认的LightsProbeChannel）(偏移: 0x44)
- `List<Vector4> m_ShadowBiasData`（List<Vector4> m_ShadowBias数据）(偏移: 0x54)
- `List<XRDisplaySubsystem> displaySubsystemList`（List<XRDisplaySubsystem> displaySubsystem列表）(偏移: 0x58)
- `Comparison<Camera> cameraComparison`（Comparison<Camera> cameraComparison）(偏移: 0xC)
- `Lightmapping.RequestLightsDelegate lightsDelegate`（Lightmapping.请求Lights委托 lights委托）(偏移: 0x5C)

### 方法 (34)

- `float get_maxShadowBias()`
  （float get_maxShadowBias（））
- `float get_minRenderScale()`
  （float get_minRender缩放（））
- `float get_maxRenderScale()`
  （float get_maxRender缩放（））
- `int get_maxPerObjectLights()`
  （int get_maxPer对象Lights（））
- `int get_maxVisibleAdditionalLights()`
  （int get_max可见的AdditionalLights（））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））
- `void Render(ScriptableRenderContext renderContext, Camera[] cameras)`
  （void Render（ScriptableRenderContext renderContext, Camera[] cameras））
- `void RenderSingleCamera(ScriptableRenderContext context, Camera camera)`
  （void Render单个摄像机（ScriptableRenderContext context, 摄像机 camera））
- `bool TryGetCullingParameters(CameraData cameraData, out ScriptableCullingParameters cullingParams)`
  （bool Try获取CullingParameters（摄像机数据 cameraData, out ScriptableCullingParameters cullingParams））
- `void RenderSingleCamera(ScriptableRenderContext context, CameraData cameraData, bool anyPostProcessingEnabled)`
  （void Render单个摄像机（ScriptableRenderContext context, 摄像机数据 cameraData, bool anyPostProcessingEnabled））
- `void RenderCameraStack(ScriptableRenderContext context, Camera baseCamera)`
  （void Render摄像机栈（ScriptableRenderContext context, 摄像机 baseCamera））
- `void UpdateVolumeFramework(Camera camera, UniversalAdditionalCameraData additionalCameraData)`
  （void 更新VolumeFramework（摄像机 camera, UniversalAdditional摄像机数据 additionalCameraData））
- `bool CheckPostProcessForDepth(in CameraData cameraData)`
  （bool 检查Post处理For深度（in CameraData cameraData））
- `void SetSupportedRenderingFeatures()`
  （void 集合SupportedRenderingFeatures（））
- `void InitializeCameraData(Camera camera, UniversalAdditionalCameraData additionalCameraData, bool resolveFinalTarget, out CameraData cameraData)`
  （void 初始化摄像机数据（摄像机 camera, UniversalAdditional摄像机数据 additionalCameraData, bool resolveFinalTarget, out CameraData cameraData））
- `void InitializeStackedCameraData(Camera baseCamera, UniversalAdditionalCameraData baseAdditionalCameraData, ref CameraData cameraData)`
  （void 初始化Stacked摄像机数据（摄像机 baseCamera, UniversalAdditional摄像机数据 baseAdditionalCameraData, ref CameraData cameraData））
- `void InitializeAdditionalCameraData(Camera camera, UniversalAdditionalCameraData additionalCameraData, bool resolveFinalTarget, ref CameraData cameraData)`
  （void 初始化Additional摄像机数据（摄像机 camera, UniversalAdditional摄像机数据 additionalCameraData, bool resolveFinalTarget, ref CameraData cameraData））
- `void InitializeRenderingData(UniversalRenderPipelineAsset settings, ref CameraData cameraData, ref CullingResults cullResults, bool anyPostProcessingEnabled, out RenderingData renderingData)`
  （void 初始化Rendering数据（UniversalRenderPipeline资产 settings, ref CameraData cameraData, ref CullingResults cullResults, bool anyPostProcessingEnabled, out RenderingData renderingData））
- `void InitializeShadowData(UniversalRenderPipelineAsset settings, NativeArray<VisibleLight> visibleLights, bool mainLightCastShadows, bool additionalLightsCastShadows, out ShadowData shadowData)`
  （void 初始化Shadow数据（UniversalRenderPipeline资产 settings, NativeArray<可见的Light> visibleLights, bool mainLightCastShadows, bool additionalLightsCastShadows, out ShadowData shadowData））
- `void InitializePostProcessingData(UniversalRenderPipelineAsset settings, out PostProcessingData postProcessingData)`
  （void 初始化PostProcessing数据（UniversalRenderPipeline资产 settings, out PostProcessingData postProcessingData））
- `void InitializeLightData(UniversalRenderPipelineAsset settings, NativeArray<VisibleLight> visibleLights, int mainLightIndex, out LightData lightData)`
  （void 初始化光照数据（UniversalRenderPipeline资产 settings, NativeArray<可见的Light> visibleLights, int mainLightIndex, out LightData lightData））
- `PerObjectData GetPerObjectLightFlags(int additionalLightsCount)`
  （Per对象数据 获取Per对象光照Flags（int additionalLightsCount））
- `int GetMainLightIndex(UniversalRenderPipelineAsset settings, NativeArray<VisibleLight> visibleLights)`
  （int 获取主要的光照索引（UniversalRenderPipeline资产 settings, NativeArray<可见的Light> visibleLights））
- `void SetupPerFrameShaderConstants()`
  （void SetupPerFrame着色器Constants（））
- `bool IsGameCamera(Camera camera)`
  （bool 是否游戏摄像机（摄像机 camera））
- `bool IsStereoEnabled(Camera camera)`
  （bool 是否Stereo启用的（摄像机 camera））
- `UniversalRenderPipelineAsset get_asset()`
  （UniversalRenderPipeline资产 get_asset（））
- `bool IsMultiPassStereoEnabled(Camera camera)`
  （bool 是否多个PassStereo启用的（摄像机 camera））
- `XRDisplaySubsystem GetFirstXRDisplaySubsystem()`
  （XRDisplaySubsystem 获取第一个XRDisplaySubsystem（））
- `bool IsRunningHololens(CameraData cameraData)`
  （bool 是否RunningHololens（摄像机数据 cameraData））
- `void SortCameras(Camera[] cameras)`
  （void SortCameras（Camera[] cameras））
- `RenderTextureDescriptor CreateRenderTextureDescriptor(Camera camera, float renderScale, bool isHdrEnabled, int msaaSamples, bool needsAlpha, bool requiresOpaqueTexture)`
  （Render纹理Descriptor 创建Render纹理Descriptor（摄像机 camera, float renderScale, bool isHdrEnabled, int msaaSamples, bool needsAlpha, bool requiresOpaqueTexture））
- `void GetLightAttenuationAndSpotDirection(LightType lightType, float lightRange, Matrix4x4 lightLocalToWorldMatrix, float spotAngle, Nullable<float> innerSpotAngle, out Vector4 lightAttenuation, out Vector4 lightSpotDir)`
  （void 获取光照AttenuationAndSpot方向（光照类型 lightType, float lightRange, Matrix4x4 lightLocalToWorldMatrix, float spotAngle, Nullable<float> innerSpotAngle, out Vector4 lightAttenuation, out Vector4 lightSpotDir））
- `void InitializeLightConstants_Common(NativeArray<VisibleLight> lights, int lightIndex, out Vector4 lightPos, out Vector4 lightColor, out Vector4 lightAttenuation, out Vector4 lightSpotDir, out Vector4 lightOcclusionProbeChannel)`
  （void 初始化光照Constants_Common（NativeArray<可见的Light> lights, int lightIndex, out Vector4 lightPos, out Vector4 lightColor, out Vector4 lightAttenuation, out Vector4 lightSpotDir, out Vector4 lightOcclusionProbeChannel））

---

## UniversalRenderPipeline.Profiling（UniversalRenderPipeline.Profiling）

### 字段 (1)

- `ProfilingSampler unknownSampler`（ProfilingSampler unknownSampler）(偏移: 0x4)

### 方法 (1)

- `ProfilingSampler TryGetOrAddCameraSampler(Camera camera)`
  （ProfilingSampler Try获取Or添加摄像机Sampler（摄像机 camera））

---

## UniversalRenderPipeline.Profiling.Pipeline（UniversalRenderPipeline.Profiling.Pipeline）

### 字段 (13)

- `ProfilingSampler beginFrameRendering`（ProfilingSampler beginFrameRendering）(偏移: 0x0)
- `ProfilingSampler endFrameRendering`（ProfilingSampler endFrameRendering）(偏移: 0x4)
- `ProfilingSampler beginCameraRendering`（ProfilingSampler begin摄像机Rendering）(偏移: 0x8)
- `ProfilingSampler endCameraRendering`（ProfilingSampler end摄像机Rendering）(偏移: 0xC)
- `ProfilingSampler initializeCameraData`（ProfilingSampler initialize摄像机数据）(偏移: 0x10)
- `ProfilingSampler initializeStackedCameraData`（ProfilingSampler initializeStacked摄像机数据）(偏移: 0x14)
- `ProfilingSampler initializeAdditionalCameraData`（ProfilingSampler initializeAdditional摄像机数据）(偏移: 0x18)
- `ProfilingSampler initializeRenderingData`（ProfilingSampler initializeRendering数据）(偏移: 0x1C)
- `ProfilingSampler initializeShadowData`（ProfilingSampler initializeShadow数据）(偏移: 0x20)
- `ProfilingSampler initializeLightData`（ProfilingSampler initialize光照数据）(偏移: 0x24)
- `ProfilingSampler getPerObjectLightFlags`（ProfilingSampler getPer对象光照Flags）(偏移: 0x28)
- `ProfilingSampler getMainLightIndex`（ProfilingSampler get主要的光照索引）(偏移: 0x2C)
- `ProfilingSampler setupPerFrameShaderConstants`（ProfilingSampler setupPerFrame着色器Constants）(偏移: 0x30)

---

## UniversalRenderPipeline.Profiling.Pipeline.Context（UniversalRenderPipeline.Profiling.Pipeline.Context）

### 字段 (1)

- `ProfilingSampler submit`（ProfilingSampler submit）(偏移: 0x34873465)

---

## UniversalRenderPipeline.Profiling.Pipeline.Renderer（UniversalRenderPipeline.Profiling.Pipeline.渲染器）

### 字段 (2)

- `ProfilingSampler setupCullingParameters`（ProfilingSampler setupCullingParameters）(偏移: 0x0)
- `ProfilingSampler setup`（ProfilingSampler setup）(偏移: 0x4)

---

## UniversalRenderPipeline.Profiling.Pipeline.XR（UniversalRenderPipeline.Profiling.Pipeline.XR）

### 字段 (1)

- `ProfilingSampler mirrorView`（ProfilingSampler mirror视图）(偏移: 0x34CB34A9)

---

## UniversalRenderPipelineAsset（UniversalRenderPipeline资产）

**继承**: RenderPipelineAsset, ISerializationCallbackReceiver（RenderPipeline资产, ISerialization回调Receiver）

### 字段 (46)

- `Shader m_DefaultShader`（着色器 m_默认的着色器）(偏移: 0xC)
- `ScriptableRenderer[] m_Renderers`（ScriptableRenderer[] m_Renderers）(偏移: 0x10)
- `int k_AssetVersion`（int k_资产Version）(偏移: 0x14)
- `int k_AssetPreviousVersion`（int k_资产上一个Version）(偏移: 0x18)
- `RendererType m_RendererType`（渲染器类型 m_渲染器类型）(偏移: 0x1C)
- `ScriptableRendererData m_RendererData`（Scriptable渲染器数据 m_渲染器数据）(偏移: 0x20)
- `ScriptableRendererData[] m_RendererDataList`（Scriptable渲染器Data[] m_渲染器数据列表）(偏移: 0x24)
- `int m_DefaultRendererIndex`（int m_默认的渲染器索引）(偏移: 0x28)
- `bool m_RequireDepthTexture`（bool m_Require深度纹理）(偏移: 0x2C)
- `bool m_RequireOpaqueTexture`（bool m_Require不透明的纹理）(偏移: 0x2D)
- `Downsampling m_OpaqueDownsampling`（Downsampling m_不透明的Downsampling）(偏移: 0x30)
- `bool m_SupportsTerrainHoles`（bool m_SupportsTerrainHoles）(偏移: 0x34)
- `StoreActionsOptimization m_StoreActionsOptimization`（商店ActionsOptimization m_商店ActionsOptimization）(偏移: 0x38)
- `bool m_SupportsHDR`（bool m_SupportsHDR）(偏移: 0x3C)
- `MsaaQuality m_MSAA`（MsaaQuality m_MSAA）(偏移: 0x40)
- `float m_RenderScale`（float m_Render缩放）(偏移: 0x44)
- `LightRenderingMode m_MainLightRenderingMode`（光照Rendering模式 m_主要的光照Rendering模式）(偏移: 0x48)
- `bool m_MainLightShadowsSupported`（bool m_主要的光照ShadowsSupported）(偏移: 0x4C)
- `ShadowResolution m_MainLightShadowmapResolution`（ShadowResolution m_主要的光照ShadowmapResolution）(偏移: 0x50)
- `LightRenderingMode m_AdditionalLightsRenderingMode`（光照Rendering模式 m_AdditionalLightsRendering模式）(偏移: 0x54)
- `int m_AdditionalLightsPerObjectLimit`（int m_AdditionalLightsPer对象Limit）(偏移: 0x58)
- `bool m_AdditionalLightShadowsSupported`（bool m_Additional光照ShadowsSupported）(偏移: 0x5C)
- `ShadowResolution m_AdditionalLightsShadowmapResolution`（ShadowResolution m_AdditionalLightsShadowmapResolution）(偏移: 0x60)
- `float m_ShadowDistance`（float m_Shadow距离）(偏移: 0x64)
- `int m_ShadowCascadeCount`（int m_ShadowCascade数量）(偏移: 0x68)
- `float m_Cascade2Split`（float m_Cascade2Split）(偏移: 0x6C)
- `Vector2 m_Cascade3Split`（二维向量 m_Cascade3Split）(偏移: 0x70)
- `Vector3 m_Cascade4Split`（三维向量 m_Cascade4Split）(偏移: 0x78)
- `float m_ShadowDepthBias`（float m_Shadow深度Bias）(偏移: 0x84)
- `float m_ShadowNormalBias`（float m_Shadow法线Bias）(偏移: 0x88)
- `bool m_SoftShadowsSupported`（bool m_SoftShadowsSupported）(偏移: 0x8C)
- `bool m_UseSRPBatcher`（bool m_UseSRPBatcher）(偏移: 0x8D)
- `bool m_SupportsDynamicBatching`（bool m_Supports动态的Batching）(偏移: 0x8E)
- `bool m_MixedLightingSupported`（bool m_MixedLightingSupported）(偏移: 0x8F)
- `PipelineDebugLevel m_DebugLevel`（PipelineDebug等级 m_Debug等级）(偏移: 0x90)
- `bool m_UseAdaptivePerformance`（bool m_UseAdaptivePerformance）(偏移: 0x94)
- `ColorGradingMode m_ColorGradingMode`（颜色Grading模式 m_颜色Grading模式）(偏移: 0x98)
- `int m_ColorGradingLutSize`（int m_颜色GradingLut大小）(偏移: 0x9C)
- `ShadowQuality m_ShadowType`（ShadowQuality m_Shadow类型）(偏移: 0xA0)
- `bool m_LocalShadowsSupported`（bool m_本地的ShadowsSupported）(偏移: 0xA4)
- `ShadowResolution m_LocalShadowsAtlasResolution`（ShadowResolution m_本地的ShadowsAtlasResolution）(偏移: 0xA8)
- `int m_MaxPixelLights`（int m_最大PixelLights）(偏移: 0xAC)
- `ShadowResolution m_ShadowAtlasResolution`（ShadowResolution m_ShadowAtlasResolution）(偏移: 0xB0)
- `ShaderVariantLogLevel m_ShaderVariantLogLevel`（着色器变异体Log等级 m_着色器变异体Log等级）(偏移: 0xB4)
- `VolumeFrameworkUpdateMode m_VolumeFrameworkUpdateMode`（VolumeFramework更新模式 m_VolumeFramework更新模式）(偏移: 0xB8)
- `ShadowCascadesOption m_ShadowCascades`（ShadowCascadesOption m_ShadowCascades）(偏移: 0xBC)

### 方法 (79)

- `ScriptableRendererData LoadBuiltinRendererData(RendererType type = 1)`
  （Scriptable渲染器数据 加载Builtin渲染器数据（渲染器类型 type = 1））
- `RenderPipeline CreatePipeline()`
  （RenderPipeline 创建Pipeline（））
- `void DestroyRenderers()`
  （void 销毁Renderers（））
- `void DestroyRenderer(ref ScriptableRenderer renderer)`
  （void 销毁渲染器（ref ScriptableRenderer renderer））
- `void OnValidate()`
  （void On验证（））
- `void OnDisable()`
  （void On禁用（））
- `void CreateRenderers()`
  （void 创建Renderers（））
- `Material GetMaterial(DefaultMaterialType materialType)`
  （材质 获取材质（默认的材质类型 materialType））
- `ScriptableRenderer get_scriptableRenderer()`
  （Scriptable渲染器 get_scriptable渲染器（））
- `ScriptableRenderer GetRenderer(int index)`
  （Scriptable渲染器 获取渲染器（int index））
- `ScriptableRendererData get_scriptableRendererData()`
  （Scriptable渲染器数据 get_scriptable渲染器数据（））
- `int[] get_rendererIndexList()`
  （int[] get_renderer索引列表（））
- `bool get_supportsCameraDepthTexture()`
  （bool get_supports摄像机深度纹理（））
- `void set_supportsCameraDepthTexture(bool value)`
  （void set_supports摄像机深度纹理（bool value））
- `bool get_supportsCameraOpaqueTexture()`
  （bool get_supports摄像机不透明的纹理（））
- `void set_supportsCameraOpaqueTexture(bool value)`
  （void set_supports摄像机不透明的纹理（bool value））
- `Downsampling get_opaqueDownsampling()`
  （Downsampling get_opaqueDownsampling（））
- `bool get_supportsTerrainHoles()`
  （bool get_supportsTerrainHoles（））
- `StoreActionsOptimization get_storeActionsOptimization()`
  （商店ActionsOptimization get_storeActionsOptimization（））
- `void set_storeActionsOptimization(StoreActionsOptimization value)`
  （void set_storeActionsOptimization（商店ActionsOptimization value））
- `bool get_supportsHDR()`
  （bool get_supportsHDR（））
- `void set_supportsHDR(bool value)`
  （void set_supportsHDR（bool value））
- `int get_msaaSampleCount()`
  （int get_msaaSample数量（））
- `void set_msaaSampleCount(int value)`
  （void set_msaaSample数量（int value））
- `float get_renderScale()`
  （float get_render缩放（））
- `void set_renderScale(float value)`
  （void set_render缩放（float value））
- `LightRenderingMode get_mainLightRenderingMode()`
  （光照Rendering模式 get_main光照Rendering模式（））
- `bool get_supportsMainLightShadows()`
  （bool get_supports主要的光照Shadows（））
- `int get_mainLightShadowmapResolution()`
  （int get_main光照ShadowmapResolution（））
- `LightRenderingMode get_additionalLightsRenderingMode()`
  （光照Rendering模式 get_additionalLightsRendering模式（））
- `int get_maxAdditionalLightsCount()`
  （int get_maxAdditionalLights数量（））
- `void set_maxAdditionalLightsCount(int value)`
  （void set_maxAdditionalLights数量（int value））
- `bool get_supportsAdditionalLightShadows()`
  （bool get_supportsAdditional光照Shadows（））
- `int get_additionalLightsShadowmapResolution()`
  （int get_additionalLightsShadowmapResolution（））
- `float get_shadowDistance()`
  （float get_shadow距离（））
- `void set_shadowDistance(float value)`
  （void set_shadow距离（float value））
- `int get_shadowCascadeCount()`
  （int get_shadowCascade数量（））
- `void set_shadowCascadeCount(int value)`
  （void set_shadowCascade数量（int value））
- `float get_cascade2Split()`
  （float get_cascade2Split（））
- `Vector2 get_cascade3Split()`
  （二维向量 get_cascade3Split（））
- `Vector3 get_cascade4Split()`
  （三维向量 get_cascade4Split（））
- `float get_shadowDepthBias()`
  （float get_shadow深度Bias（））
- `void set_shadowDepthBias(float value)`
  （void set_shadow深度Bias（float value））
- `float get_shadowNormalBias()`
  （float get_shadow法线Bias（））
- `void set_shadowNormalBias(float value)`
  （void set_shadow法线Bias（float value））
- `bool get_supportsSoftShadows()`
  （bool get_supportsSoftShadows（））
- `bool get_supportsDynamicBatching()`
  （bool get_supports动态的Batching（））
- `void set_supportsDynamicBatching(bool value)`
  （void set_supports动态的Batching（bool value））
- `bool get_supportsMixedLighting()`
  （bool get_supportsMixedLighting（））
- `ShaderVariantLogLevel get_shaderVariantLogLevel()`
  （着色器变异体Log等级 get_shader变异体Log等级（））
- `void set_shaderVariantLogLevel(ShaderVariantLogLevel value)`
  （void set_shader变异体Log等级（着色器变异体Log等级 value））
- `VolumeFrameworkUpdateMode get_volumeFrameworkUpdateMode()`
  （VolumeFramework更新模式 get_volumeFramework更新模式（））
- `PipelineDebugLevel get_debugLevel()`
  （PipelineDebug等级 get_debug等级（））
- `bool get_useSRPBatcher()`
  （bool get_useSRPBatcher（））
- `void set_useSRPBatcher(bool value)`
  （void set_useSRPBatcher（bool value））
- `ColorGradingMode get_colorGradingMode()`
  （颜色Grading模式 get_colorGrading模式（））
- `void set_colorGradingMode(ColorGradingMode value)`
  （void set_colorGrading模式（颜色Grading模式 value））
- `int get_colorGradingLutSize()`
  （int get_colorGradingLut大小（））
- `void set_colorGradingLutSize(int value)`
  （void set_colorGradingLut大小（int value））
- `bool get_useAdaptivePerformance()`
  （bool get_useAdaptivePerformance（））
- `void set_useAdaptivePerformance(bool value)`
  （void set_useAdaptivePerformance（bool value））
- `Material get_defaultMaterial()`
  （材质 get_default材质（））
- `Material get_defaultParticleMaterial()`
  （材质 get_default粒子材质（））
- `Material get_defaultLineMaterial()`
  （材质 get_defaultLine材质（））
- `Material get_defaultTerrainMaterial()`
  （材质 get_defaultTerrain材质（））
- `Material get_defaultUIMaterial()`
  （材质 get_default界面材质（））
- `Material get_defaultUIOverdrawMaterial()`
  （材质 get_default界面Overdraw材质（））
- `Material get_defaultUIETC1SupportedMaterial()`
  （材质 get_defaultUIETC1Supported材质（））
- `Material get_default2DMaterial()`
  （材质 get_default2D材质（））
- `Shader get_defaultShader()`
  （着色器 get_default着色器（））
- `void OnBeforeSerialize()`
  （void OnBeforeSerialize（））
- `void OnAfterDeserialize()`
  （void OnAfterDeserialize（））
- `float ValidateShadowBias(float value)`
  （float 验证ShadowBias（float value））
- `int ValidatePerObjectLights(int value)`
  （int 验证Per对象Lights（int value））
- `float ValidateRenderScale(float value)`
  （float 验证Render缩放（float value））
- `bool ValidateRendererDataList(bool partial = False)`
  （bool 验证渲染器数据列表（bool partial = False））
- `bool ValidateRendererData(int index)`
  （bool 验证渲染器数据（int index））
- `ShadowCascadesOption get_shadowCascadeOption()`
  （ShadowCascadesOption get_shadowCascadeOption（））
- `void set_shadowCascadeOption(ShadowCascadesOption value)`
  （void set_shadowCascadeOption（ShadowCascadesOption value））

---

## UniversalRenderPipelineEditorResources（UniversalRenderPipelineEditorResources）

**继承**: ScriptableObject（脚本对象）

### 字段 (2)

- `UniversalRenderPipelineEditorResources.ShaderResources shaders`（UniversalRenderPipelineEditorResources.着色器Resources shaders）(偏移: 0xC)
- `UniversalRenderPipelineEditorResources.MaterialResources materials`（UniversalRenderPipelineEditorResources.材质Resources materials）(偏移: 0x10)

---

## UniversalRenderPipelineEditorResources.MaterialResources（UniversalRenderPipelineEditorResources.材质Resources）

### 字段 (3)

- `Material lit`（材质 lit）(偏移: 0x8)
- `Material particleLit`（材质 particleLit）(偏移: 0xC)
- `Material terrainLit`（材质 terrainLit）(偏移: 0x10)

---

## UniversalRenderPipelineEditorResources.ShaderResources（UniversalRenderPipelineEditorResources.着色器Resources）

### 字段 (8)

- `Shader autodeskInteractivePS`（着色器 autodeskInteractivePS）(偏移: 0x8)
- `Shader autodeskInteractiveTransparentPS`（着色器 autodeskInteractive透明的PS）(偏移: 0xC)
- `Shader autodeskInteractiveMaskedPS`（着色器 autodeskInteractiveMaskedPS）(偏移: 0x10)
- `Shader terrainDetailLitPS`（着色器 terrainDetailLitPS）(偏移: 0x14)
- `Shader terrainDetailGrassPS`（着色器 terrainDetailGrassPS）(偏移: 0x18)
- `Shader terrainDetailGrassBillboardPS`（着色器 terrainDetailGrassBillboardPS）(偏移: 0x1C)
- `Shader defaultSpeedTree7PS`（着色器 defaultSpeedTree7PS）(偏移: 0x20)
- `Shader defaultSpeedTree8PS`（着色器 defaultSpeedTree8PS）(偏移: 0x24)

---

## UnixRegistryApi（UnixRegistryApi）

**继承**: IRegistryApi（IRegistryApi）

### 方法 (11)

- `string ToUnix(string keyname)`
  （string ToUnix（string keyname））
- `bool IsWellKnownKey(string parentKeyName, string keyname)`
  （bool 是否WellKnown键（string parentKeyName, string keyname））
- `RegistryKey OpenSubKey(RegistryKey rkey, string keyname, bool writable)`
  （Registry键 打开子键（Registry键 rkey, string keyname, bool writable））
- `void Flush(RegistryKey rkey)`
  （void Flush（Registry键 rkey））
- `void Close(RegistryKey rkey)`
  （void 关闭（Registry键 rkey））
- `object GetValue(RegistryKey rkey, string name, object default_value, RegistryValueOptions options)`
  （object 获取值（Registry键 rkey, string name, object default_value, Registry值Options options））
- `string[] GetSubKeyNames(RegistryKey rkey)`
  （string[] 获取子键Names（Registry键 rkey））
- `string ToString(RegistryKey rkey)`
  （string To字符串（Registry键 rkey））
- `RegistryKey CreateSubKey(RegistryKey rkey, string keyname, bool writable)`
  （Registry键 创建子键（Registry键 rkey, string keyname, bool writable））
- `RegistryKey CreateSubKey(RegistryKey rkey, string keyname, bool writable, bool is_volatile)`
  （Registry键 创建子键（Registry键 rkey, string keyname, bool writable, bool is_volatile））
- `IntPtr GetHandle(RegistryKey key)`
  （整数Ptr 获取句柄（Registry键 key））

---

## UnmanagedFunctionPointerAttribute（UnmanagedFunction指针Attribute）

**继承**: Attribute（Attribute）

### 字段 (5)

- `CallingConvention m_callingConvention`（CallingConvention m_callingConvention）(偏移: 0x8)
- `CharSet CharSet`（Char集合 Char集合）(偏移: 0xC)
- `bool BestFitMapping`（bool BestFitMapping）(偏移: 0x10)
- `bool ThrowOnUnmappableChar`（bool 投掷OnUnmappableChar）(偏移: 0x11)
- `bool SetLastError`（bool 集合最后一个Error）(偏移: 0x12)

---

## UnmanagedMemoryStream（UnmanagedMemory流）

**继承**: Stream（流）

### 字段 (8)

- `SafeBuffer _buffer`（Safe缓冲区 _buffer）(偏移: 0x14)
- `byte* _mem`（byte* _mem）(偏移: 0x18)
- `long _length`（long _length）(偏移: 0x20)
- `long _capacity`（long _capacity）(偏移: 0x28)
- `long _position`（long _position）(偏移: 0x30)
- `long _offset`（long _offset）(偏移: 0x38)
- `FileAccess _access`（文件Access _access）(偏移: 0x40)
- `bool _isOpen`（bool _is打开）(偏移: 0x44)

### 方法 (16)

- `void Initialize(byte* pointer, long length, long capacity, FileAccess access, bool skipSecurityCheck)`
  （void 初始化（byte* pointer, long length, long capacity, 文件Access access, bool skipSecurityCheck））
- `bool get_CanRead()`
  （bool get_能否Read（））
- `bool get_CanSeek()`
  （bool get_能否Seek（））
- `bool get_CanWrite()`
  （bool get_能否Write（））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））
- `void Flush()`
  （void Flush（））
- `long get_Length()`
  （long get_Length（））
- `long get_Position()`
  （long get_Position（））
- `void set_Position(long value)`
  （void set_Position（long value））
- `byte* get_PositionPointer()`
  （byte* get_Position指针（））
- `int Read([In] [Out] byte[] buffer, int offset, int count)`
  （int Read（[In] [Out] byte[] buffer, int offset, int count））
- `int ReadByte()`
  （int ReadByte（））
- `long Seek(long offset, SeekOrigin loc)`
  （long Seek（long offset, SeekOrigin loc））
- `void SetLength(long value)`
  （void 集合Length（long value））
- `void Write(byte[] buffer, int offset, int count)`
  （void Write（byte[] buffer, int offset, int count））
- `void WriteByte(byte value)`
  （void WriteByte（byte value））

---

## UnmanagedType（Unmanaged类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UnobservedTaskExceptionEventArgs（UnobservedTaskException事件Args）

**继承**: EventArgs（事件Args）

### 字段 (2)

- `AggregateException m_exception`（AggregateException m_exception）(偏移: 0x8)
- `bool m_observed`（bool m_observed）(偏移: 0xC)

---

## UnsafeNativeMethods.ManifestEtw（UnsafeNativeMethods.ManifestEtw）

### 方法 (7)

- `uint EventRegister(in Guid providerId, [In] UnsafeNativeMethods.ManifestEtw.EtwEnableCallback enableCallback, [In] void* callbackContext, ref long registrationHandle)`
  （uint 事件Register（in Guid providerId, [In] UnsafeNativeMethods.ManifestEtw.EtwEnableCallback enableCallback, [In] void* callbackContext, ref long registrationHandle））
- `uint EventUnregister([In] long registrationHandle)`
  （uint 事件Unregister（[In] long registrationHandle））
- `int EventWriteTransferWrapper(long registrationHandle, ref EventDescriptor eventDescriptor, Guid* activityId, Guid* relatedActivityId, int userDataCount, EventProvider.EventData* userData)`
  （int 事件WriteTransfer包装器（long registrationHandle, ref EventDescriptor eventDescriptor, Guid* activityId, Guid* relatedActivityId, int userDataCount, 事件Provider.事件Data* userData））
- `int EventWriteTransfer([In] long registrationHandle, in EventDescriptor eventDescriptor, [In] Guid* activityId, [In] Guid* relatedActivityId, [In] int userDataCount, [In] EventProvider.EventData* userData)`
  （int 事件WriteTransfer（[In] long registrationHandle, in EventDescriptor eventDescriptor, [In] Guid* activityId, [In] Guid* relatedActivityId, [In] int userDataCount, [In] EventProvider.EventData* userData））
- `int EventActivityIdControl([In] UnsafeNativeMethods.ManifestEtw.ActivityControl ControlCode, ref Guid ActivityId)`
  （int 事件ActivityId控制（[In] UnsafeNativeMethods.ManifestEtw.ActivityControl ControlCode, ref Guid ActivityId））
- `int EventSetInformation([In] long registrationHandle, [In] UnsafeNativeMethods.ManifestEtw.EVENT_INFO_CLASS informationClass, [In] void* eventInformation, [In] int informationLength)`
  （int 事件集合Information（[In] long registrationHandle, [In] UnsafeNativeMethods.ManifestEtw.EVENT_INFO_CLASS informationClass, [In] void* eventInformation, [In] int informationLength））
- `int EnumerateTraceGuidsEx(UnsafeNativeMethods.ManifestEtw.TRACE_QUERY_INFO_CLASS TraceQueryInfoClass, void* InBuffer, int InBufferSize, void* OutBuffer, int OutBufferSize, ref int ReturnLength)`
  （int EnumerateTraceGuidsEx（UnsafeNativeMethods.ManifestEtw.TRACE_QUERY_INFO_CLASS TraceQueryInfoClass, void* InBuffer, int InBufferSize, void* OutBuffer, int OutBufferSize, ref int ReturnLength））

---

## UnsafeNativeMethods.ManifestEtw.ActivityControl（UnsafeNativeMethods.ManifestEtw.Activity控制）

### 字段 (1)

- `uint value__`（uint value__）(偏移: 0x0)

---

## UnsafeNativeMethods.ManifestEtw.EVENT_FILTER_DESCRIPTOR（UnsafeNativeMethods.ManifestEtw.EVENT_FILTER_DESCRIPTOR）

### 字段 (3)

- `long Ptr`（long Ptr）(偏移: 0x0)
- `int Size`（int 大小）(偏移: 0x8)
- `int Type`（int 类型）(偏移: 0xC)

---

## UnsafeNativeMethods.ManifestEtw.EVENT_INFO_CLASS（UnsafeNativeMethods.ManifestEtw.EVENT_INFO_CLASS）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UnsafeNativeMethods.ManifestEtw.EtwEnableCallback（UnsafeNativeMethods.ManifestEtw.Etw启用回调）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(in Guid sourceId, [In] int isEnabled, [In] byte level, [In] long matchAnyKeywords, [In] long matchAllKeywords, [In] UnsafeNativeMethods.ManifestEtw.EVENT_FILTER_DESCRIPTOR* filterData, [In] void* callbackContext)`
  （void Invoke（in Guid sourceId, [In] int isEnabled, [In] byte level, [In] long matchAnyKeywords, [In] long matchAllKeywords, [In] UnsafeNativeMethods.ManifestEtw.EVENT_FILTER_DESCRIPTOR* filterData, [In] void* callbackContext））
- `IAsyncResult BeginInvoke(in Guid sourceId, [In] int isEnabled, [In] byte level, [In] long matchAnyKeywords, [In] long matchAllKeywords, [In] UnsafeNativeMethods.ManifestEtw.EVENT_FILTER_DESCRIPTOR* filterData, [In] void* callbackContext, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（in Guid sourceId, [In] int isEnabled, [In] byte level, [In] long matchAnyKeywords, [In] long matchAllKeywords, [In] UnsafeNativeMethods.ManifestEtw.EVENT_FILTER_DESCRIPTOR* filterData, [In] void* callbackContext, 异步回调 callback, object object））
- `void EndInvoke(in Guid sourceId, IAsyncResult result)`
  （void 结束Invoke（in Guid sourceId, I异步Result result））

---

## UnsafeNativeMethods.ManifestEtw.TRACE_ENABLE_INFO（UnsafeNativeMethods.ManifestEtw.TRACE_ENABLE_INFO）

### 字段 (8)

- `int IsEnabled`（int 是否启用的）(偏移: 0x0)
- `byte Level`（byte 等级）(偏移: 0x4)
- `byte Reserved1`（byte Reserved1）(偏移: 0x5)
- `ushort LoggerId`（ushort LoggerId）(偏移: 0x6)
- `int EnableProperty`（int 启用属性）(偏移: 0x8)
- `int Reserved2`（int Reserved2）(偏移: 0xC)
- `long MatchAnyKeyword`（long 比赛任意Keyword）(偏移: 0x10)
- `long MatchAllKeyword`（long 比赛所有Keyword）(偏移: 0x18)

---

## UnsafeNativeMethods.ManifestEtw.TRACE_GUID_INFO（UnsafeNativeMethods.ManifestEtw.TRACE_GUID_INFO）

### 字段 (2)

- `int InstanceCount`（int 实例数量）(偏移: 0x0)
- `int Reserved`（int Reserved）(偏移: 0x4)

---

## UnsafeNativeMethods.ManifestEtw.TRACE_PROVIDER_INSTANCE_INFO（UnsafeNativeMethods.ManifestEtw.TRACE_PROVIDER_INSTANCE_INFO）

### 字段 (4)

- `int NextOffset`（int 下一个Offset）(偏移: 0x0)
- `int EnableCount`（int 启用数量）(偏移: 0x4)
- `int Pid`（int Pid）(偏移: 0x8)
- `int Flags`（int Flags）(偏移: 0xC)

---

## UnsafeNativeMethods.ManifestEtw.TRACE_QUERY_INFO_CLASS（UnsafeNativeMethods.ManifestEtw.TRACE_QUERY_INFO_CLASS）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UnsafeUtility（Unsafe工具）

### 方法 (12)

- `void* Malloc(long size, int alignment, Allocator allocator)`
  （void* Malloc（long size, int alignment, Allocator allocator））
- `void Free(void* memory, Allocator allocator)`
  （void Free（void* memory, Allocator allocator））
- `void MemCpy(void* destination, void* source, long size)`
  （void MemCpy（void* destination, void* source, long size））
- `void MemCpyStride(void* destination, int destinationStride, void* source, int sourceStride, int elementSize, int count)`
  （void MemCpyStride（void* destination, int destinationStride, void* source, int sourceStride, int elementSize, int count））
- `void MemSet(void* destination, byte value, long size)`
  （void Mem集合（void* destination, byte value, long size））
- `void MemClear(void* destination, long size)`
  （void Mem清除（void* destination, long size））
- `int SizeOf(Type type)`
  （int 大小Of（类型 type））
- `bool IsBlittable(Type type)`
  （bool 是否Blittable（类型 type））
- `bool IsBlittableValueType(Type t)`
  （bool 是否Blittable值类型（类型 t））
- `string GetReasonForTypeNonBlittableImpl(Type t, string name)`
  （string 获取ReasonFor类型NonBlittableImpl（类型 t, string name））
- `bool IsArrayBlittable(Array arr)`
  （bool 是否数组Blittable（数组 arr））
- `string GetReasonForArrayNonBlittable(Array arr)`
  （string 获取ReasonFor数组NonBlittable（数组 arr））

---

## UpdateMode（更新模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UpdateNotice（更新Notice）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UpdateTracker（更新Tracker）

### 字段 (2)

- `List<Transform> sToDelete`（List<Transform> sToDelete）(偏移: 0x4)
- `float mLastUpdateTime`（float m最后一个更新时间）(偏移: 0x8)

### 方法 (4)

- `void InitializeModule()`
  （void 初始化模块（））
- `void UpdateTargets(UpdateTracker.UpdateClock currentClock)`
  （void 更新Targets（更新Tracker.更新时钟 currentClock））
- `UpdateTracker.UpdateClock GetPreferredUpdate(Transform target)`
  （更新Tracker.更新时钟 获取Preferred更新（变换 target））
- `void OnUpdate(UpdateTracker.UpdateClock currentClock)`
  （void On更新（更新Tracker.更新时钟 currentClock））

---

## UpdateTracker.UpdateClock（更新Tracker.更新时钟）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UpdateTracker.UpdateStatus（更新Tracker.更新Status）

### 字段 (6)

- `int windowStart`（int window开始）(偏移: 0x8)
- `int numWindowLateUpdateMoves`（int numWindow延迟更新Moves）(偏移: 0xC)
- `int numWindowFixedUpdateMoves`（int numWindow固定更新Moves）(偏移: 0x10)
- `int numWindows`（int numWindows）(偏移: 0x14)
- `int lastFrameUpdated`（int lastFrameUpdated）(偏移: 0x18)
- `Matrix4x4 lastPos`（Matrix4x4 lastPos）(偏移: 0x1C)

### 方法 (3)

- `UpdateTracker.UpdateClock get_PreferredUpdate()`
  （更新Tracker.更新时钟 get_Preferred更新（））
- `void set_PreferredUpdate(UpdateTracker.UpdateClock value)`
  （void set_Preferred更新（更新Tracker.更新时钟 value））
- `void OnUpdate(int currentFrame, UpdateTracker.UpdateClock currentClock, Matrix4x4 pos)`
  （void On更新（int currentFrame, 更新Tracker.更新时钟 currentClock, Matrix4x4 pos））

---

## UpdateType（更新类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UploadHandler（Upload处理器）

### 字段 (1)

- `IntPtr m_Ptr`（整数Ptr m_Ptr）(偏移: 0x8)

### 方法 (2)

- `void Release()`
  （void Release（））
- `void Dispose()`
  （void 释放（））

---

## Uri（Uri）

**继承**: ISerializable（ISerializable）

### 字段 (29)

- `string UriSchemeFile`（string UriScheme文件）(偏移: 0x0)
- `string UriSchemeFtp`（string UriSchemeFtp）(偏移: 0x4)
- `string UriSchemeGopher`（string UriSchemeGopher）(偏移: 0x8)
- `string UriSchemeHttp`（string UriSchemeHttp）(偏移: 0xC)
- `string UriSchemeHttps`（string UriSchemeHttps）(偏移: 0x10)
- `string UriSchemeWs`（string UriSchemeWs）(偏移: 0x14)
- `string UriSchemeWss`（string UriSchemeWss）(偏移: 0x18)
- `string UriSchemeMailto`（string UriSchemeMailto）(偏移: 0x1C)
- `string UriSchemeNews`（string UriSchemeNews）(偏移: 0x20)
- `string UriSchemeNntp`（string UriSchemeNntp）(偏移: 0x24)
- `string UriSchemeNetTcp`（string UriSchemeNetTcp）(偏移: 0x28)
- `string UriSchemeNetPipe`（string UriSchemeNetPipe）(偏移: 0x2C)
- `string SchemeDelimiter`（string SchemeDelimiter）(偏移: 0x30)
- `string m_String`（string m_字符串）(偏移: 0x8)
- `string m_originalUnicodeString`（string m_originalUnicode字符串）(偏移: 0xC)
- `UriParser m_Syntax`（UriParser m_Syntax）(偏移: 0x10)
- `string m_DnsSafeHost`（string m_DnsSafeHost）(偏移: 0x14)
- `Uri.Flags m_Flags`（Uri.Flags m_Flags）(偏移: 0x18)
- `Uri.UriInfo m_Info`（Uri.Uri信息 m_信息）(偏移: 0x20)
- `bool m_iriParsing`（bool m_iriParsing）(偏移: 0x24)
- `bool s_ConfigInitialized`（bool s_配置Initialized）(偏移: 0x34)
- `bool s_ConfigInitializing`（bool s_配置Initializing）(偏移: 0x35)
- `UriIdnScope s_IdnScope`（UriIdn瞄准镜 s_Idn瞄准镜）(偏移: 0x38)
- `bool s_IriParsing`（bool s_IriParsing）(偏移: 0x3C)
- `bool useDotNetRelativeOrAbsolute`（bool useDotNetRelativeOrAbsolute）(偏移: 0x3D)
- `bool IsWindowsFileSystem`（bool 是否Windows文件系统）(偏移: 0x3E)
- `object s_initLock`（object s_initLock）(偏移: 0x40)
- `char[] HexLowerChars`（char[] Hex下半身Chars）(偏移: 0x44)
- `char[] _WSchars`（char[] _WSchars）(偏移: 0x48)

### 方法 (97)

- `bool get_IsImplicitFile()`
  （bool get_是否Implicit文件（））
- `bool get_IsUncOrDosPath()`
  （bool get_是否UncOrDos路径（））
- `bool get_IsDosPath()`
  （bool get_是否Dos路径（））
- `bool get_IsUncPath()`
  （bool get_是否Unc路径（））
- `Uri.Flags get_HostType()`
  （Uri.Flags get_Host类型（））
- `UriParser get_Syntax()`
  （UriParser get_Syntax（））
- `bool get_IsNotAbsoluteUri()`
  （bool get_是否NotAbsoluteUri（））
- `bool IriParsingStatic(UriParser syntax)`
  （bool IriParsing静态的（UriParser syntax））
- `bool get_AllowIdn()`
  （bool get_允许Idn（））
- `bool AllowIdnStatic(UriParser syntax, Uri.Flags flags)`
  （bool 允许Idn静态的（UriParser syntax, Uri.Flags flags））
- `bool IsIntranet(string schemeHost)`
  （bool 是否Intranet（string schemeHost））
- `bool get_UserDrivenParsing()`
  （bool get_UserDrivenParsing（））
- `void SetUserDrivenParsing()`
  （void 集合UserDrivenParsing（））
- `ushort get_SecuredPathIndex()`
  （ushort get_Secured路径索引（））
- `bool NotAny(Uri.Flags flags)`
  （bool Not任意（Uri.Flags flags））
- `bool InFact(Uri.Flags flags)`
  （bool InFact（Uri.Flags flags））
- `bool StaticNotAny(Uri.Flags allFlags, Uri.Flags checkFlags)`
  （bool 静态的Not任意（Uri.Flags allFlags, Uri.Flags checkFlags））
- `bool StaticInFact(Uri.Flags allFlags, Uri.Flags checkFlags)`
  （bool 静态的InFact（Uri.Flags allFlags, Uri.Flags checkFlags））
- `Uri.UriInfo EnsureUriInfo()`
  （Uri.Uri信息 EnsureUri信息（））
- `void EnsureParseRemaining()`
  （void Ensure解析Remaining（））
- `void EnsureHostString(bool allowDnsOptimization)`
  （void EnsureHost字符串（bool allowDnsOptimization））
- `ParsingError GetCombinedString(Uri baseUri, string relativeStr, bool dontEscape, ref string result)`
  （ParsingError 获取Combined字符串（Uri baseUri, string relativeStr, bool dontEscape, ref string result））
- `UriFormatException GetException(ParsingError err)`
  （Uri格式化Exception 获取Exception（ParsingError err））
- `void GetObjectData(SerializationInfo serializationInfo, StreamingContext streamingContext)`
  （void 获取对象数据（Serialization信息 serializationInfo, StreamingContext streamingContext））
- `string get_AbsolutePath()`
  （string get_Absolute路径（））
- `string get_PrivateAbsolutePath()`
  （string get_私有的Absolute路径（））
- `string get_AbsoluteUri()`
  （string get_AbsoluteUri（））
- `bool get_IsFile()`
  （bool get_是否文件（））
- `bool get_IsLoopback()`
  （bool get_是否Loopback（））
- `string get_PathAndQuery()`
  （string get_路径AndQuery（））
- `bool get_IsUnc()`
  （bool get_是否Unc（））
- `bool StaticIsFile(UriParser syntax)`
  （bool 静态的是否文件（UriParser syntax））
- `object get_InitializeLock()`
  （object get_初始化Lock（））
- `void InitializeUriConfig()`
  （void 初始化Uri配置（））
- `int get_Port()`
  （int get_Port（））
- `string get_Fragment()`
  （string get_Fragment（））
- `string get_Scheme()`
  （string get_Scheme（））
- `bool get_OriginalStringSwitched()`
  （bool get_Original字符串Switched（））
- `string get_OriginalString()`
  （string get_Original字符串（））
- `string get_DnsSafeHost()`
  （string get_DnsSafeHost（））
- `bool get_IsAbsoluteUri()`
  （bool get_是否AbsoluteUri（））
- `bool get_UserEscaped()`
  （bool get_UserEscaped（））
- `bool IsGenDelim(char ch)`
  （bool 是否GenDelim（char ch））
- `bool IsHexDigit(char character)`
  （bool 是否HexDigit（char character））
- `int FromHex(char digit)`
  （int FromHex（char digit））
- `int GetHashCode()`
  （int 获取HashCode（））
- `string ToString()`
  （string To字符串（））
- `bool op_Equality(Uri uri1, Uri uri2)`
  （bool op_Equality（Uri uri1, Uri uri2））
- `bool op_Inequality(Uri uri1, Uri uri2)`
  （bool op_Inequality（Uri uri1, Uri uri2））
- `bool Equals(object comparand)`
  （bool Equals（object comparand））
- `ParsingError ParseScheme(string uriString, ref Uri.Flags flags, ref UriParser syntax)`
  （ParsingError 解析Scheme（string uriString, ref Uri.Flags flags, ref UriParser syntax））
- `UriFormatException ParseMinimal()`
  （Uri格式化Exception 解析Minimal（））
- `ParsingError PrivateParseMinimal()`
  （ParsingError 私有的解析Minimal（））
- `void PrivateParseMinimalIri(string newHost, ushort idx)`
  （void 私有的解析MinimalIri（string newHost, ushort idx））
- `void CreateUriInfo(Uri.Flags cF)`
  （void 创建Uri信息（Uri.Flags cF））
- `void CreateHostString()`
  （void 创建Host字符串（））
- `string CreateHostStringHelper(string str, ushort idx, ushort end, ref Uri.Flags flags, ref string scopeId)`
  （string 创建Host字符串辅助器（string str, ushort idx, ushort end, ref Uri.Flags flags, ref string scopeId））
- `void GetHostViaCustomSyntax()`
  （void 获取HostVia自定义的Syntax（））
- `string GetParts(UriComponents uriParts, UriFormat formatAs)`
  （string 获取Parts（UriComponents uriParts, Uri格式化 formatAs））
- `string GetEscapedParts(UriComponents uriParts)`
  （string 获取EscapedParts（UriComponents uriParts））
- `string GetUnescapedParts(UriComponents uriParts, UriFormat formatAs)`
  （string 获取UnescapedParts（UriComponents uriParts, Uri格式化 formatAs））
- `string ReCreateParts(UriComponents parts, ushort nonCanonical, UriFormat formatAs)`
  （string Re创建Parts（UriComponents parts, ushort nonCanonical, Uri格式化 formatAs））
- `string GetUriPartsFromUserString(UriComponents uriParts)`
  （string 获取UriPartsFromUser字符串（UriComponents uriParts））
- `void ParseRemaining()`
  （void 解析Remaining（））
- `ushort ParseSchemeCheckImplicitFile(char* uriString, ushort length, ref ParsingError err, ref Uri.Flags flags, ref UriParser syntax)`
  （ushort 解析Scheme检查Implicit文件（char* uriString, ushort length, ref ParsingError err, ref Uri.Flags flags, ref UriParser syntax））
- `bool CheckKnownSchemes(long* lptr, ushort nChars, ref UriParser syntax)`
  （bool 检查KnownSchemes（long* lptr, ushort nChars, ref UriParser syntax））
- `ParsingError CheckSchemeSyntax(char* ptr, ushort length, ref UriParser syntax)`
  （ParsingError 检查SchemeSyntax（char* ptr, ushort length, ref UriParser syntax））
- `ushort CheckAuthorityHelper(char* pString, ushort idx, ushort length, ref ParsingError err, ref Uri.Flags flags, UriParser syntax, ref string newHost)`
  （ushort 检查Authority辅助器（char* pString, ushort idx, ushort length, ref ParsingError err, ref Uri.Flags flags, UriParser syntax, ref string newHost））
- `void CheckAuthorityHelperHandleDnsIri(char* pString, ushort start, int end, int startInput, bool iriParsing, bool hasUnicode, UriParser syntax, string userInfoString, ref Uri.Flags flags, ref bool justNormalized, ref string newHost, ref ParsingError err)`
  （void 检查Authority辅助器句柄DnsIri（char* pString, ushort start, int end, int startInput, bool iriParsing, bool hasUnicode, UriParser syntax, string userInfoString, ref Uri.Flags flags, ref bool justNormalized, ref string newHost, ref ParsingError err））
- `void CheckAuthorityHelperHandleAnyHostIri(char* pString, int startInput, int end, bool iriParsing, bool hasUnicode, UriParser syntax, ref Uri.Flags flags, ref string newHost, ref ParsingError err)`
  （void 检查Authority辅助器句柄任意HostIri（char* pString, int startInput, int end, bool iriParsing, bool hasUnicode, UriParser syntax, ref Uri.Flags flags, ref string newHost, ref ParsingError err））
- `void FindEndOfComponent(string input, ref ushort idx, ushort end, char delim)`
  （void 查找结束Of组件（string input, ref ushort idx, ushort end, char delim））
- `void FindEndOfComponent(char* str, ref ushort idx, ushort end, char delim)`
  （void 查找结束Of组件（char* str, ref ushort idx, ushort end, char delim））
- `Uri.Check CheckCanonical(char* str, ref ushort idx, ushort end, char delim)`
  （Uri.检查 检查Canonical（char* str, ref ushort idx, ushort end, char delim））
- `char[] GetCanonicalPath(char[] dest, ref int pos, UriFormat formatAs)`
  （char[] 获取Canonical路径（char[] dest, ref int pos, Uri格式化 formatAs））
- `void UnescapeOnly(char* pch, int start, ref int end, char ch1, char ch2, char ch3)`
  （void UnescapeOnly（char* pch, int start, ref int end, char ch1, char ch2, char ch3））
- `char[] Compress(char[] dest, ushort start, ref int destLength, UriParser syntax)`
  （char[] Compress（char[] dest, ushort start, ref int destLength, UriParser syntax））
- `int CalculateCaseInsensitiveHashCode(string text)`
  （int 计算CaseInsensitiveHashCode（string text））
- `string CombineUri(Uri basePart, string relativePart, UriFormat uriFormat)`
  （string CombineUri（Uri basePart, string relativePart, Uri格式化 uriFormat））
- `bool IsLWS(char ch)`
  （bool 是否LWS（char ch））
- `bool IsAsciiLetter(char character)`
  （bool 是否AsciiLetter（char character））
- `bool IsAsciiLetterOrDigit(char character)`
  （bool 是否AsciiLetterOrDigit（char character））
- `bool IsBidiControlCharacter(char ch)`
  （bool 是否Bidi控制角色（char ch））
- `string StripBidiControlCharacter(char* strToClean, int start, int length)`
  （string StripBidi控制角色（char* strToClean, int start, int length））
- `void CreateThis(string uri, bool dontEscape, UriKind uriKind)`
  （void 创建This（string uri, bool dontEscape, UriKind uriKind））
- `void InitializeUri(ParsingError err, UriKind uriKind, out UriFormatException e)`
  （void 初始化Uri（ParsingError err, UriKind uriKind, out UriFormatException e））
- `bool CheckForConfigLoad(string data)`
  （bool 检查For配置加载（string data））
- `bool CheckForUnicode(string data)`
  （bool 检查ForUnicode（string data））
- `bool CheckForEscapedUnreserved(string data)`
  （bool 检查ForEscapedUnreserved（string data））
- `bool TryCreate(string uriString, UriKind uriKind, out Uri result)`
  （bool Try创建（string uriString, UriKind uriKind, out Uri result））
- `string GetComponents(UriComponents components, UriFormat format)`
  （string 获取Components（UriComponents components, Uri格式化 format））
- `string UnescapeDataString(string stringToUnescape)`
  （string Unescape数据字符串（string stringToUnescape））
- `string EscapeUnescapeIri(string input, int start, int end, UriComponents component)`
  （string EscapeUnescapeIri（string input, int start, int end, UriComponents component））
- `Uri CreateHelper(string uriString, bool dontEscape, UriKind uriKind, ref UriFormatException e)`
  （Uri 创建辅助器（string uriString, bool dontEscape, UriKind uriKind, ref UriFormatException e））
- `Uri ResolveHelper(Uri baseUri, Uri relativeUri, ref string newUriString, ref bool userEscaped, out UriFormatException e)`
  （Uri Resolve辅助器（Uri baseUri, Uri relativeUri, ref string newUriString, ref bool userEscaped, out UriFormatException e））
- `string GetRelativeSerializationString(UriFormat format)`
  （string 获取RelativeSerialization字符串（Uri格式化 format））
- `string GetComponentsHelper(UriComponents uriComponents, UriFormat uriFormat)`
  （string 获取Components辅助器（UriComponents uriComponents, Uri格式化 uriFormat））
- `void CreateThisFromUri(Uri otherUri)`
  （void 创建ThisFromUri（Uri otherUri））

---

## Uri.Check（Uri.检查）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Uri.Flags（Uri.Flags）

### 字段 (1)

- `ulong value__`（ulong value__）(偏移: 0x0)

---

## Uri.MoreInfo（Uri.More信息）

### 字段 (6)

- `string Path`（string 路径）(偏移: 0x8)
- `string Query`（string Query）(偏移: 0xC)
- `string Fragment`（string Fragment）(偏移: 0x10)
- `string AbsoluteUri`（string AbsoluteUri）(偏移: 0x14)
- `int Hash`（int Hash）(偏移: 0x18)
- `string RemoteUrl`（string RemoteUrl）(偏移: 0x1C)

---

## Uri.Offset（Uri.Offset）

### 字段 (8)

- `ushort Scheme`（ushort Scheme）(偏移: 0x0)
- `ushort User`（ushort User）(偏移: 0x2)
- `ushort Host`（ushort Host）(偏移: 0x4)
- `ushort PortValue`（ushort Port值）(偏移: 0x6)
- `ushort Path`（ushort 路径）(偏移: 0x8)
- `ushort Query`（ushort Query）(偏移: 0xA)
- `ushort Fragment`（ushort Fragment）(偏移: 0xC)
- `ushort End`（ushort 结束）(偏移: 0xE)

---

## Uri.UriInfo（Uri.Uri信息）

### 字段 (6)

- `string Host`（string Host）(偏移: 0x8)
- `string ScopeId`（string 瞄准镜Id）(偏移: 0xC)
- `string String`（string 字符串）(偏移: 0x10)
- `Uri.Offset Offset`（Uri.Offset Offset）(偏移: 0x14)
- `string DnsSafeHost`（string DnsSafeHost）(偏移: 0x24)
- `Uri.MoreInfo MoreInfo`（Uri.More信息 More信息）(偏移: 0x28)

---

## UriComponents（UriComponents）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UriFormat（Uri格式化）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UriHelper（Uri辅助器）

### 字段 (1)

- `char[] HexUpperChars`（char[] Hex上半身Chars）(偏移: 0x0)

### 方法 (11)

- `char[] EscapeString(string input, int start, int end, char[] dest, ref int destPos, bool isUriString, char force1, char force2, char rsvd)`
  （char[] Escape字符串（string input, int start, int end, char[] dest, ref int destPos, bool isUriString, char force1, char force2, char rsvd））
- `char[] EnsureDestinationSize(char* pStr, char[] dest, int currentInputPos, short charsToAdd, short minReallocateChars, ref int destPos, int prevInputPos)`
  （char[] EnsureDestination大小（char* pStr, char[] dest, int currentInputPos, short charsToAdd, short minReallocateChars, ref int destPos, int prevInputPos））
- `char[] UnescapeString(string input, int start, int end, char[] dest, ref int destPosition, char rsvd1, char rsvd2, char rsvd3, UnescapeMode unescapeMode, UriParser syntax, bool isQuery)`
  （char[] Unescape字符串（string input, int start, int end, char[] dest, ref int destPosition, char rsvd1, char rsvd2, char rsvd3, Unescape模式 unescapeMode, UriParser syntax, bool isQuery））
- `char[] UnescapeString(char* pStr, int start, int end, char[] dest, ref int destPosition, char rsvd1, char rsvd2, char rsvd3, UnescapeMode unescapeMode, UriParser syntax, bool isQuery)`
  （char[] Unescape字符串（char* pStr, int start, int end, char[] dest, ref int destPosition, char rsvd1, char rsvd2, char rsvd3, Unescape模式 unescapeMode, UriParser syntax, bool isQuery））
- `void MatchUTF8Sequence(char* pDest, char[] dest, ref int destOffset, char[] unescapedChars, int charCount, byte[] bytes, int byteCount, bool isQuery, bool iriParsing)`
  （void 比赛UTF8Sequence（char* pDest, char[] dest, ref int destOffset, char[] unescapedChars, int charCount, byte[] bytes, int byteCount, bool isQuery, bool iriParsing））
- `void EscapeAsciiChar(char ch, char[] to, ref int pos)`
  （void EscapeAsciiChar（char ch, char[] to, ref int pos））
- `char EscapedAscii(char digit, char next)`
  （char EscapedAscii（char digit, char next））
- `bool IsNotSafeForUnescape(char ch)`
  （bool 是否NotSafeForUnescape（char ch））
- `bool IsReservedUnreservedOrHash(char c)`
  （bool 是否ReservedUnreservedOrHash（char c））
- `bool IsUnreserved(char c)`
  （bool 是否Unreserved（char c））
- `bool Is3986Unreserved(char c)`
  （bool Is3986Unreserved（char c））

---

## UriIdnScope（UriIdn瞄准镜）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UriKind（UriKind）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UriParser（UriParser）

### 字段 (24)

- `UriSyntaxFlags m_Flags`（UriSyntaxFlags m_Flags）(偏移: 0x8)
- `UriSyntaxFlags m_UpdatableFlags`（UriSyntaxFlags m_UpdatableFlags）(偏移: 0xC)
- `bool m_UpdatableFlagsUsed`（bool m_UpdatableFlagsUsed）(偏移: 0x10)
- `int m_Port`（int m_Port）(偏移: 0x14)
- `string m_Scheme`（string m_Scheme）(偏移: 0x18)
- `UriParser HttpUri`（UriParser HttpUri）(偏移: 0x8)
- `UriParser HttpsUri`（UriParser HttpsUri）(偏移: 0xC)
- `UriParser WsUri`（UriParser WsUri）(偏移: 0x10)
- `UriParser WssUri`（UriParser WssUri）(偏移: 0x14)
- `UriParser FtpUri`（UriParser FtpUri）(偏移: 0x18)
- `UriParser FileUri`（UriParser 文件Uri）(偏移: 0x1C)
- `UriParser GopherUri`（UriParser GopherUri）(偏移: 0x20)
- `UriParser NntpUri`（UriParser NntpUri）(偏移: 0x24)
- `UriParser NewsUri`（UriParser NewsUri）(偏移: 0x28)
- `UriParser MailToUri`（UriParser MailToUri）(偏移: 0x2C)
- `UriParser UuidUri`（UriParser UuidUri）(偏移: 0x30)
- `UriParser TelnetUri`（UriParser TelnetUri）(偏移: 0x34)
- `UriParser LdapUri`（UriParser LdapUri）(偏移: 0x38)
- `UriParser NetTcpUri`（UriParser NetTcpUri）(偏移: 0x3C)
- `UriParser NetPipeUri`（UriParser NetPipeUri）(偏移: 0x40)
- `UriParser VsMacrosUri`（UriParser VsMacrosUri）(偏移: 0x44)
- `UriParser.UriQuirksVersion s_QuirksVersion`（UriParser.UriQuirksVersion s_QuirksVersion）(偏移: 0x48)
- `UriSyntaxFlags HttpSyntaxFlags`（UriSyntaxFlags HttpSyntaxFlags）(偏移: 0x4C)
- `UriSyntaxFlags FileSyntaxFlags`（UriSyntaxFlags 文件SyntaxFlags）(偏移: 0x50)

### 方法 (18)

- `string get_SchemeName()`
  （string get_Scheme名称（））
- `int get_DefaultPort()`
  （int get_默认的Port（））
- `UriParser OnNewUri()`
  （UriParser On新的Uri（））
- `void InitializeAndValidate(Uri uri, out UriFormatException parsingError)`
  （void 初始化And验证（Uri uri, out UriFormatException parsingError））
- `string Resolve(Uri baseUri, Uri relativeUri, out UriFormatException parsingError)`
  （string Resolve（Uri baseUri, Uri relativeUri, out UriFormatException parsingError））
- `string GetComponents(Uri uri, UriComponents components, UriFormat format)`
  （string 获取Components（Uri uri, UriComponents components, Uri格式化 format））
- `bool get_ShouldUseLegacyV2Quirks()`
  （bool get_应该UseLegacyV2Quirks（））
- `UriSyntaxFlags get_Flags()`
  （UriSyntaxFlags get_Flags（））
- `bool NotAny(UriSyntaxFlags flags)`
  （bool Not任意（UriSyntaxFlags flags））
- `bool InFact(UriSyntaxFlags flags)`
  （bool InFact（UriSyntaxFlags flags））
- `bool IsAllSet(UriSyntaxFlags flags)`
  （bool 是否所有集合（UriSyntaxFlags flags））
- `bool IsFullMatch(UriSyntaxFlags flags, UriSyntaxFlags expected)`
  （bool 是否满比赛（UriSyntaxFlags flags, UriSyntaxFlags expected））
- `UriParser FindOrFetchAsUnknownV1Syntax(string lwrCaseScheme)`
  （UriParser 查找OrFetchAsUnknownV1Syntax（string lwrCaseScheme））
- `bool get_IsSimple()`
  （bool get_是否Simple（））
- `UriParser InternalOnNewUri()`
  （UriParser 内部的On新的Uri（））
- `void InternalValidate(Uri thisUri, out UriFormatException parsingError)`
  （void 内部的验证（Uri thisUri, out UriFormatException parsingError））
- `string InternalResolve(Uri thisBaseUri, Uri uriLink, out UriFormatException parsingError)`
  （string 内部的Resolve（Uri thisBaseUri, Uri uriLink, out UriFormatException parsingError））
- `string InternalGetComponents(Uri thisUri, UriComponents uriComponents, UriFormat uriFormat)`
  （string 内部的获取Components（Uri thisUri, UriComponents uriComponents, Uri格式化 uriFormat））

---

## UriParser.UriQuirksVersion（UriParser.UriQuirksVersion）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UriSyntaxFlags（UriSyntaxFlags）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## UriTypeConverter（Uri类型Converter）

**继承**: TypeConverter（类型Converter）

### 方法 (5)

- `bool CanConvert(Type type)`
  （bool 能否转换（类型 type））
- `bool CanConvertFrom(ITypeDescriptorContext context, Type sourceType)`
  （bool 能否转换From（I类型DescriptorContext context, 类型 sourceType））
- `bool CanConvertTo(ITypeDescriptorContext context, Type destinationType)`
  （bool 能否转换To（I类型DescriptorContext context, 类型 destinationType））
- `object ConvertFrom(ITypeDescriptorContext context, CultureInfo culture, object value)`
  （object 转换From（I类型DescriptorContext context, Culture信息 culture, object value））
- `object ConvertTo(ITypeDescriptorContext context, CultureInfo culture, object value, Type destinationType)`
  （object 转换To（I类型DescriptorContext context, Culture信息 culture, object value, 类型 destinationType））

---

## UsedByNativeCodeAttribute（UsedByNativeCodeAttribute）

**继承**: Attribute（Attribute）

### 方法 (1)

- `void set_Name(string value)`
  （void set_名称（string value））

---

## Utility（工具）

### 字段 (8)

- `Action<bool> GraphicsResourcesRecreate`（Action<bool> GraphicsResourcesRecreate）(偏移: 0x0)
- `Action EngineUpdate`（动作 引擎更新）(偏移: 0x4)
- `Action FlushPendingResources`（动作 FlushPendingResources）(偏移: 0x8)
- `Action<Camera> RegisterIntermediateRenderers`（Action<Camera> RegisterIntermediateRenderers）(偏移: 0xC)
- `Action<IntPtr> RenderNodeAdd`（Action<整数Ptr> Render节点添加）(偏移: 0x10)
- `Action<IntPtr> RenderNodeExecute`（Action<整数Ptr> Render节点执行）(偏移: 0x14)
- `Action<IntPtr> RenderNodeCleanup`（Action<整数Ptr> Render节点清理）(偏移: 0x18)
- `ProfilerMarker s_MarkerRaiseEngineUpdate`（ProfilerMarker s_MarkerRaise引擎更新）(偏移: 0x1C)

### 方法 (7)

- `void RaiseGraphicsResourcesRecreate(bool recreate)`
  （void RaiseGraphicsResourcesRecreate（bool recreate））
- `void RaiseEngineUpdate()`
  （void Raise引擎更新（））
- `void RaiseFlushPendingResources()`
  （void RaiseFlushPendingResources（））
- `void RaiseRegisterIntermediateRenderers(Camera camera)`
  （void RaiseRegisterIntermediateRenderers（摄像机 camera））
- `void RaiseRenderNodeAdd(IntPtr userData)`
  （void RaiseRender节点添加（整数Ptr userData））
- `void RaiseRenderNodeExecute(IntPtr userData)`
  （void RaiseRender节点执行（整数Ptr userData））
- `void RaiseRenderNodeCleanup(IntPtr userData)`
  （void RaiseRender节点清理（整数Ptr userData））

---

## Utility（工具）

### 方法 (3)

- `float Min(float a, float b, float c)`
  （float 最小（float a, float b, float c））
- `float Max(float a, float b, float c)`
  （float 最大（float a, float b, float c））
- `Int3[] RemoveDuplicateVertices(Int3[] vertices, int[] triangles)`
  （Int3[] 移除DuplicateVertices（Int3[] vertices, int[] triangles））

---

## Utils（Utils）

### 字段 (1)

- `RNGCryptoServiceProvider _rng`（RNGCrypto服务提供者 _rng）(偏移: 0x0)

### 方法 (12)

- `RNGCryptoServiceProvider get_StaticRandomNumberGenerator()`
  （RNGCrypto服务提供者 get_静态的随机NumberGenerator（））
- `byte[] GenerateRandom(int keySize)`
  （byte[] Generate随机（int keySize））
- `bool HasAlgorithm(int dwCalg, int dwKeySize)`
  （bool 是否有Algorithm（int dwCalg, int dwKeySize））
- `byte[] ConvertIntToByteArray(int dwInput)`
  （byte[] 转换整数ToByte数组（int dwInput））
- `byte[] FixupKeyParity(byte[] key)`
  （byte[] Fixup键Parity（byte[] key））
- `void DWORDFromLittleEndian(uint* x, int digits, byte* block)`
  （void DWORDFromLittleEndian（uint* x, int digits, byte* block））
- `void DWORDToLittleEndian(byte[] block, uint[] x, int digits)`
  （void DWORDToLittleEndian（byte[] block, uint[] x, int digits））
- `void DWORDFromBigEndian(uint* x, int digits, byte* block)`
  （void DWORDFromBigEndian（uint* x, int digits, byte* block））
- `void DWORDToBigEndian(byte[] block, uint[] x, int digits)`
  （void DWORDToBigEndian（byte[] block, uint[] x, int digits））
- `void QuadWordFromBigEndian(ulong* x, int digits, byte* block)`
  （void QuadWordFromBigEndian（ulong* x, int digits, byte* block））
- `void QuadWordToBigEndian(byte[] block, ulong[] x, int digits)`
  （void QuadWordToBigEndian（byte[] block, ulong[] x, int digits））
- `bool _ProduceLegacyHmacValues()`
  （bool _ProduceLegacyHmacValues（））

---

## V3Tools（V3Tools）

### 方法 (11)

- `Vector3 Lerp(Vector3 fromVector, Vector3 toVector, float weight)`
  （三维向量 Lerp（三维向量 fromVector, 三维向量 toVector, float weight））
- `Vector3 Slerp(Vector3 fromVector, Vector3 toVector, float weight)`
  （三维向量 Slerp（三维向量 fromVector, 三维向量 toVector, float weight））
- `Vector3 ExtractVertical(Vector3 v, Vector3 verticalAxis, float weight)`
  （三维向量 Extract垂直（三维向量 v, 三维向量 verticalAxis, float weight））
- `Vector3 ExtractHorizontal(Vector3 v, Vector3 normal, float weight)`
  （三维向量 Extract水平（三维向量 v, 三维向量 normal, float weight））
- `Vector3 ClampDirection(Vector3 direction, Vector3 normalDirection, float clampWeight, int clampSmoothing)`
  （三维向量 Clamp方向（三维向量 direction, 三维向量 normalDirection, float clampWeight, int clampSmoothing））
- `Vector3 ClampDirection(Vector3 direction, Vector3 normalDirection, float clampWeight, int clampSmoothing, out bool changed)`
  （三维向量 Clamp方向（三维向量 direction, 三维向量 normalDirection, float clampWeight, int clampSmoothing, out bool changed））
- `Vector3 ClampDirection(Vector3 direction, Vector3 normalDirection, float clampWeight, int clampSmoothing, out float clampValue)`
  （三维向量 Clamp方向（三维向量 direction, 三维向量 normalDirection, float clampWeight, int clampSmoothing, out float clampValue））
- `Vector3 LineToPlane(Vector3 origin, Vector3 direction, Vector3 planeNormal, Vector3 planePoint)`
  （三维向量 LineToPlane（三维向量 origin, 三维向量 direction, 三维向量 planeNormal, 三维向量 planePoint））
- `Vector3 PointToPlane(Vector3 point, Vector3 planePosition, Vector3 planeNormal)`
  （三维向量 PointToPlane（三维向量 point, 三维向量 planePosition, 三维向量 planeNormal））
- `Vector3 TransformPointUnscaled(Transform t, Vector3 point)`
  （三维向量 变换PointUnscaled（变换 t, 三维向量 point））
- `Vector3 InverseTransformPointUnscaled(Transform t, Vector3 point)`
  （三维向量 Inverse变换PointUnscaled（变换 t, 三维向量 point））

---

## VFXAudioSpectrumBinder（VFX音频SpectrumBinder）

**继承**: VFXBinderBase（VFXBinder基础）

### 字段 (9)

- `ExposedProperty m_CountProperty`（Exposed属性 m_数量属性）(偏移: 0x10)
- `ExposedProperty m_TextureProperty`（Exposed属性 m_纹理属性）(偏移: 0x14)
- `FFTWindow FFTWindow`（FFTWindow FFTWindow）(偏移: 0x18)
- `uint Samples`（uint Samples）(偏移: 0x1C)
- `VFXAudioSpectrumBinder.AudioSourceMode Mode`（VFX音频SpectrumBinder.音频Source模式 模式）(偏移: 0x20)
- `AudioSource AudioSource`（音频Source 音频Source）(偏移: 0x24)
- `Texture2D m_Texture`（Texture2D m_纹理）(偏移: 0x28)
- `float[] m_AudioCache`（float[] m_音频缓存）(偏移: 0x2C)
- `Color[] m_ColorCache`（Color[] m_颜色缓存）(偏移: 0x30)

### 方法 (8)

- `string get_CountProperty()`
  （string get_数量属性（））
- `void set_CountProperty(string value)`
  （void set_数量属性（string value））
- `string get_TextureProperty()`
  （string get_纹理属性（））
- `void set_TextureProperty(string value)`
  （void set_纹理属性（string value））
- `bool IsValid(VisualEffect component)`
  （bool 是否Valid（Visual特效 component））
- `void UpdateTexture()`
  （void 更新纹理（））
- `void UpdateBinding(VisualEffect component)`
  （void 更新Binding（Visual特效 component））
- `string ToString()`
  （string To字符串（））

---

## VFXAudioSpectrumBinder.AudioSourceMode（VFX音频SpectrumBinder.音频Source模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## VFXBinderAttribute（VFXBinderAttribute）

**继承**: PropertyAttribute（属性Attribute）

### 字段 (1)

- `string MenuPath`（string 菜单路径）(偏移: 0x8)

---

## VFXBinderBase（VFXBinder基础）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (1)

- `VFXPropertyBinder binder`（VFX属性Binder binder）(偏移: 0xC)

### 方法 (5)

- `void Reset()`
  （void 重置（））
- `void Awake()`
  （void Awake（））
- `void OnEnable()`
  （void On启用（））
- `void OnDisable()`
  （void On禁用（））
- `string ToString()`
  （string To字符串（））

---

## VFXEnabledBinder（VFX启用的Binder）

**继承**: VFXBinderBase（VFXBinder基础）

### 字段 (3)

- `VFXEnabledBinder.Check check`（VFX启用的Binder.检查 check）(偏移: 0x10)
- `ExposedProperty m_Property`（Exposed属性 m_属性）(偏移: 0x14)
- `GameObject Target`（游戏对象 目标）(偏移: 0x18)

### 方法 (5)

- `string get_Property()`
  （string get_属性（））
- `void set_Property(string value)`
  （void set_属性（string value））
- `bool IsValid(VisualEffect component)`
  （bool 是否Valid（Visual特效 component））
- `void UpdateBinding(VisualEffect component)`
  （void 更新Binding（Visual特效 component））
- `string ToString()`
  （string To字符串（））

---

## VFXEnabledBinder.Check（VFX启用的Binder.检查）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## VFXEventAttribute（VFX事件Attribute）

**继承**: IDisposable（IDisposable）

### 字段 (3)

- `IntPtr m_Ptr`（整数Ptr m_Ptr）(偏移: 0x8)
- `bool m_Owner`（bool m_Owner）(偏移: 0xC)
- `VisualEffectAsset m_VfxAsset`（Visual特效资产 m_Vfx资产）(偏移: 0x10)

### 方法 (18)

- `IntPtr Internal_Create()`
  （整数Ptr Internal_创建（））
- `VFXEventAttribute Internal_InstanciateVFXEventAttribute(VisualEffectAsset vfxAsset)`
  （VFX事件Attribute Internal_InstanciateVFX事件Attribute（Visual特效资产 vfxAsset））
- `void Internal_InitFromAsset(VisualEffectAsset vfxAsset)`
  （void Internal_初始化From资产（Visual特效资产 vfxAsset））
- `VisualEffectAsset get_vfxAsset()`
  （Visual特效资产 get_vfx资产（））
- `void Release()`
  （void Release（））
- `void Finalize()`
  （void Finalize（））
- `void Dispose()`
  （void 释放（））
- `void Internal_Destroy(IntPtr ptr)`
  （void Internal_销毁（整数Ptr ptr））
- `void SetBool(int nameID, bool b)`
  （void 集合布尔值（int nameID, bool b））
- `void SetInt(int nameID, int i)`
  （void 集合整数（int nameID, int i））
- `void SetUint(int nameID, uint i)`
  （void 集合Uint（int nameID, uint i））
- `void SetFloat(int nameID, float f)`
  （void 集合浮点数（int nameID, float f））
- `void SetVector2(int nameID, Vector2 v)`
  （void 集合二维向量（int nameID, 二维向量 v））
- `void SetVector3(int nameID, Vector3 v)`
  （void 集合三维向量（int nameID, 三维向量 v））
- `void SetVector4(int nameID, Vector4 v)`
  （void 集合Vector4（int nameID, Vector4 v））
- `void SetVector2_Injected(int nameID, ref Vector2 v)`
  （void 集合Vector2_Injected（int nameID, ref Vector2 v））
- `void SetVector3_Injected(int nameID, ref Vector3 v)`
  （void 集合Vector3_Injected（int nameID, ref Vector3 v））
- `void SetVector4_Injected(int nameID, ref Vector4 v)`
  （void 集合Vector4_Injected（int nameID, ref Vector4 v））

---

## VFXEventBinderBase（VFX事件Binder基础）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (3)

- `VisualEffect target`（Visual特效 target）(偏移: 0xC)
- `string EventName`（string 事件名称）(偏移: 0x10)
- `VFXEventAttribute eventAttribute`（VFX事件Attribute eventAttribute）(偏移: 0x14)

### 方法 (4)

- `void OnEnable()`
  （void On启用（））
- `void OnValidate()`
  （void On验证（））
- `void UpdateCacheEventAttribute()`
  （void 更新缓存事件Attribute（））
- `void SendEventToVisualEffect(object[] parameters)`
  （void 发送事件ToVisual特效（object[] parameters））

---

## VFXExpressionValues（VFXExpressionValues）

### 字段 (1)

- `IntPtr m_Ptr`（整数Ptr m_Ptr）(偏移: 0x8)

### 方法 (7)

- `VFXExpressionValues CreateExpressionValuesWrapper(IntPtr ptr)`
  （VFXExpressionValues 创建ExpressionValues包装器（整数Ptr ptr））
- `bool GetBool(int nameID)`
  （bool 获取布尔值（int nameID））
- `int GetInt(int nameID)`
  （int 获取整数（int nameID））
- `uint GetUInt(int nameID)`
  （uint 获取U整数（int nameID））
- `float GetFloat(int nameID)`
  （float 获取浮点数（int nameID））
- `Vector3 GetVector3(int nameID)`
  （三维向量 获取三维向量（int nameID））
- `void GetVector3_Injected(int nameID, out Vector3 ret)`
  （void 获取Vector3_Injected（int nameID, out Vector3 ret））

---

## VFXHierarchyAttributeMapBinder（VFXHierarchyAttribute映射Binder）

**继承**: VFXBinderBase（VFXBinder基础）

### 字段 (12)

- `ExposedProperty m_BoneCount`（Exposed属性 m_Bone数量）(偏移: 0x10)
- `ExposedProperty m_PositionMap`（Exposed属性 m_Position映射）(偏移: 0x14)
- `ExposedProperty m_TargetPositionMap`（Exposed属性 m_目标Position映射）(偏移: 0x18)
- `ExposedProperty m_RadiusPositionMap`（Exposed属性 m_RadiusPosition映射）(偏移: 0x1C)
- `Transform HierarchyRoot`（变换 Hierarchy根）(偏移: 0x20)
- `float DefaultRadius`（float 默认的Radius）(偏移: 0x24)
- `uint MaximumDepth`（uint Maximum深度）(偏移: 0x28)
- `VFXHierarchyAttributeMapBinder.RadiusMode Radius`（VFXHierarchyAttribute映射Binder.Radius模式 Radius）(偏移: 0x2C)
- `Texture2D position`（Texture2D position）(偏移: 0x30)
- `Texture2D targetPosition`（Texture2D targetPosition）(偏移: 0x34)
- `Texture2D radius`（Texture2D radius）(偏移: 0x38)
- `List<VFXHierarchyAttributeMapBinder.Bone> bones`（List<VFXHierarchyAttribute映射Binder.Bone> bones）(偏移: 0x3C)

### 方法 (8)

- `void OnEnable()`
  （void On启用（））
- `void OnValidate()`
  （void On验证（））
- `void UpdateHierarchy()`
  （void 更新Hierarchy（））
- `List<VFXHierarchyAttributeMapBinder.Bone> ChildrenOf(Transform source, uint depth)`
  （List<VFXHierarchyAttribute映射Binder.Bone> ChildrenOf（变换 source, uint depth））
- `void UpdateData()`
  （void 更新数据（））
- `bool IsValid(VisualEffect component)`
  （bool 是否Valid（Visual特效 component））
- `void UpdateBinding(VisualEffect component)`
  （void 更新Binding（Visual特效 component））
- `string ToString()`
  （string To字符串（））

---

## VFXHierarchyAttributeMapBinder.Bone（VFXHierarchyAttribute映射Binder.Bone）

### 字段 (4)

- `Transform source`（变换 source）(偏移: 0x0)
- `float sourceRadius`（float sourceRadius）(偏移: 0x4)
- `Transform target`（变换 target）(偏移: 0x8)
- `float targetRadius`（float targetRadius）(偏移: 0xC)

---

## VFXHierarchyAttributeMapBinder.RadiusMode（VFXHierarchyAttribute映射Binder.Radius模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## VFXInputAxisBinder（VFX输入轴Binder）

**继承**: VFXBinderBase（VFXBinder基础）

### 字段 (4)

- `ExposedProperty m_AxisProperty`（Exposed属性 m_轴属性）(偏移: 0x10)
- `string AxisName`（string 轴名称）(偏移: 0x14)
- `float AccumulateSpeed`（float AccumulateSpeed）(偏移: 0x18)
- `bool Accumulate`（bool Accumulate）(偏移: 0x1C)

### 方法 (5)

- `string get_AxisProperty()`
  （string get_轴属性（））
- `void set_AxisProperty(string value)`
  （void set_轴属性（string value））
- `bool IsValid(VisualEffect component)`
  （bool 是否Valid（Visual特效 component））
- `void UpdateBinding(VisualEffect component)`
  （void 更新Binding（Visual特效 component））
- `string ToString()`
  （string To字符串（））

---

## VFXInputButtonBinder（VFX输入按钮Binder）

**继承**: VFXBinderBase（VFXBinder基础）

### 字段 (6)

- `ExposedProperty m_ButtonProperty`（Exposed属性 m_按钮属性）(偏移: 0x10)
- `ExposedProperty m_ButtonSmoothProperty`（Exposed属性 m_按钮Smooth属性）(偏移: 0x14)
- `string ButtonName`（string 按钮名称）(偏移: 0x18)
- `float SmoothSpeed`（float SmoothSpeed）(偏移: 0x1C)
- `bool UseButtonSmooth`（bool Use按钮Smooth）(偏移: 0x20)
- `float m_CachedSmoothValue`（float m_CachedSmooth值）(偏移: 0x24)

### 方法 (8)

- `string get_ButtonProperty()`
  （string get_按钮属性（））
- `void set_ButtonProperty(string value)`
  （void set_按钮属性（string value））
- `string get_ButtonSmoothProperty()`
  （string get_按钮Smooth属性（））
- `void set_ButtonSmoothProperty(string value)`
  （void set_按钮Smooth属性（string value））
- `bool IsValid(VisualEffect component)`
  （bool 是否Valid（Visual特效 component））
- `void Start()`
  （void 开始（））
- `void UpdateBinding(VisualEffect component)`
  （void 更新Binding（Visual特效 component））
- `string ToString()`
  （string To字符串（））

---

## VFXInputKeyBinder（VFX输入键Binder）

**继承**: VFXBinderBase（VFXBinder基础）

### 字段 (6)

- `ExposedProperty m_KeyProperty`（Exposed属性 m_键属性）(偏移: 0x10)
- `ExposedProperty m_KeySmoothProperty`（Exposed属性 m_键Smooth属性）(偏移: 0x14)
- `KeyCode Key`（键Code 键）(偏移: 0x18)
- `float SmoothSpeed`（float SmoothSpeed）(偏移: 0x1C)
- `bool UseKeySmooth`（bool Use键Smooth）(偏移: 0x20)
- `float m_CachedSmoothValue`（float m_CachedSmooth值）(偏移: 0x24)

### 方法 (8)

- `string get_KeyProperty()`
  （string get_键属性（））
- `void set_KeyProperty(string value)`
  （void set_键属性（string value））
- `string get_KeySmoothProperty()`
  （string get_键Smooth属性（））
- `void set_KeySmoothProperty(string value)`
  （void set_键Smooth属性（string value））
- `bool IsValid(VisualEffect component)`
  （bool 是否Valid（Visual特效 component））
- `void Start()`
  （void 开始（））
- `void UpdateBinding(VisualEffect component)`
  （void 更新Binding（Visual特效 component））
- `string ToString()`
  （string To字符串（））

---

## VFXInputMouseBinder（VFX输入鼠标Binder）

**继承**: VFXBinderBase（VFXBinder基础）

### 字段 (10)

- `ExposedProperty m_MouseLeftClickProperty`（Exposed属性 m_鼠标左Click属性）(偏移: 0x10)
- `ExposedProperty m_MouseRightClickProperty`（Exposed属性 m_鼠标右Click属性）(偏移: 0x14)
- `ExposedProperty m_PositionProperty`（Exposed属性 m_Position属性）(偏移: 0x18)
- `ExposedProperty m_VelocityProperty`（Exposed属性 m_速度属性）(偏移: 0x1C)
- `Camera Target`（摄像机 目标）(偏移: 0x20)
- `float Distance`（float 距离）(偏移: 0x24)
- `bool SetVelocity`（bool 集合速度）(偏移: 0x28)
- `bool CheckLeftClick`（bool 检查左Click）(偏移: 0x29)
- `bool CheckRightClick`（bool 检查右Click）(偏移: 0x2A)
- `Vector3 m_PreviousPosition`（三维向量 m_上一个Position）(偏移: 0x2C)

### 方法 (14)

- `string get_MouseLeftClickProperty()`
  （string get_鼠标左Click属性（））
- `void set_MouseLeftClickProperty(string value)`
  （void set_鼠标左Click属性（string value））
- `string get_MouseRightClickProperty()`
  （string get_鼠标右Click属性（））
- `void set_MouseRightClickProperty(string value)`
  （void set_鼠标右Click属性（string value））
- `string get_PositionProperty()`
  （string get_Position属性（））
- `void set_PositionProperty(string value)`
  （void set_Position属性（string value））
- `string get_VelocityProperty()`
  （string get_速度属性（））
- `void set_VelocityProperty(string value)`
  （void set_速度属性（string value））
- `bool IsValid(VisualEffect component)`
  （bool 是否Valid（Visual特效 component））
- `void UpdateBinding(VisualEffect component)`
  （void 更新Binding（Visual特效 component））
- `bool IsRightClickPressed()`
  （bool 是否右Click按下的（））
- `bool IsLeftClickPressed()`
  （bool 是否左Click按下的（））
- `Vector2 GetMousePosition()`
  （二维向量 获取鼠标Position（））
- `string ToString()`
  （string To字符串（））

---

## VFXInputTouchBinder（VFX输入触摸Binder）

**继承**: VFXBinderBase（VFXBinder基础）

### 字段 (9)

- `ExposedProperty m_TouchEnabledProperty`（Exposed属性 m_触摸启用的属性）(偏移: 0x10)
- `ExposedProperty m_Parameter`（Exposed属性 m_Parameter）(偏移: 0x14)
- `ExposedProperty m_VelocityParameter`（Exposed属性 m_速度Parameter）(偏移: 0x18)
- `int TouchIndex`（int 触摸索引）(偏移: 0x1C)
- `Camera Target`（摄像机 目标）(偏移: 0x20)
- `float Distance`（float 距离）(偏移: 0x24)
- `bool SetVelocity`（bool 集合速度）(偏移: 0x28)
- `Vector3 m_PreviousPosition`（三维向量 m_上一个Position）(偏移: 0x2C)
- `bool m_PreviousTouch`（bool m_上一个触摸）(偏移: 0x38)

### 方法 (11)

- `string get_TouchEnabledProperty()`
  （string get_触摸启用的属性（））
- `void set_TouchEnabledProperty(string value)`
  （void set_触摸启用的属性（string value））
- `string get_Parameter()`
  （string get_Parameter（））
- `void set_Parameter(string value)`
  （void set_Parameter（string value））
- `string get_VelocityParameter()`
  （string get_速度Parameter（））
- `void set_VelocityParameter(string value)`
  （void set_速度Parameter（string value））
- `bool IsValid(VisualEffect component)`
  （bool 是否Valid（Visual特效 component））
- `void UpdateBinding(VisualEffect component)`
  （void 更新Binding（Visual特效 component））
- `int GetTouchCount()`
  （int 获取触摸数量（））
- `Vector2 GetTouchPosition(int touchIndex)`
  （二维向量 获取触摸Position（int touchIndex））
- `string ToString()`
  （string To字符串（））

---

## VFXLightBinder（VFX光照Binder）

**继承**: VFXBinderBase（VFXBinder基础）

### 字段 (7)

- `ExposedProperty m_ColorProperty`（Exposed属性 m_颜色属性）(偏移: 0x10)
- `ExposedProperty m_BrightnessProperty`（Exposed属性 m_Brightness属性）(偏移: 0x14)
- `ExposedProperty m_RadiusProperty`（Exposed属性 m_Radius属性）(偏移: 0x18)
- `Light Target`（光照 目标）(偏移: 0x1C)
- `bool BindColor`（bool Bind颜色）(偏移: 0x20)
- `bool BindBrightness`（bool BindBrightness）(偏移: 0x21)
- `bool BindRadius`（bool BindRadius）(偏移: 0x22)

### 方法 (9)

- `string get_ColorProperty()`
  （string get_颜色属性（））
- `void set_ColorProperty(string value)`
  （void set_颜色属性（string value））
- `string get_BrightnessProperty()`
  （string get_Brightness属性（））
- `void set_BrightnessProperty(string value)`
  （void set_Brightness属性（string value））
- `string get_RadiusProperty()`
  （string get_Radius属性（））
- `void set_RadiusProperty(string value)`
  （void set_Radius属性（string value））
- `bool IsValid(VisualEffect component)`
  （bool 是否Valid（Visual特效 component））
- `void UpdateBinding(VisualEffect component)`
  （void 更新Binding（Visual特效 component））
- `string ToString()`
  （string To字符串（））

---

## VFXManager（VFX管理器）

### 方法 (2)

- `void PrepareCamera(Camera cam)`
  （void Prepare摄像机（摄像机 cam））
- `void ProcessCameraCommand(Camera cam, CommandBuffer cmd)`
  （void 处理摄像机Command（摄像机 cam, Command缓冲区 cmd））

---

## VFXMouseEventBinder（VFX鼠标事件Binder）

**继承**: VFXEventBinderBase（VFX事件Binder基础）

### 字段 (3)

- `VFXMouseEventBinder.Activation activation`（VFX鼠标事件Binder.Activation activation）(偏移: 0x18)
- `ExposedProperty position`（Exposed属性 position）(偏移: 0x1C)
- `bool RaycastMousePosition`（bool Raycast鼠标Position）(偏移: 0x20)

### 方法 (14)

- `void SetEventAttribute(object[] parameters)`
  （void 集合事件Attribute（object[] parameters））
- `Vector2 GetMousePosition()`
  （二维向量 获取鼠标Position（））
- `void DoOnMouseDown()`
  （void DoOn鼠标下（））
- `void DoOnMouseUp()`
  （void DoOn鼠标上（））
- `void DoOnMouseDrag()`
  （void DoOn鼠标Drag（））
- `void DoOnMouseOver()`
  （void DoOn鼠标Over（））
- `void DoOnMouseEnter()`
  （void DoOn鼠标Enter（））
- `void DoOnMouseExit()`
  （void DoOn鼠标Exit（））
- `void OnMouseDown()`
  （void On鼠标下（））
- `void OnMouseUp()`
  （void On鼠标上（））
- `void OnMouseDrag()`
  （void On鼠标Drag（））
- `void OnMouseOver()`
  （void On鼠标Over（））
- `void OnMouseEnter()`
  （void On鼠标Enter（））
- `void OnMouseExit()`
  （void On鼠标Exit（））

---

## VFXMouseEventBinder.Activation（VFX鼠标事件Binder.Activation）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## VFXMultiplePositionBinder（VFXMultiplePositionBinder）

**继承**: VFXBinderBase（VFXBinder基础）

### 字段 (6)

- `ExposedProperty PositionMapProperty`（Exposed属性 Position映射属性）(偏移: 0x10)
- `ExposedProperty PositionCountProperty`（Exposed属性 Position数量属性）(偏移: 0x14)
- `GameObject[] Targets`（游戏Object[] Targets）(偏移: 0x18)
- `bool EveryFrame`（bool EveryFrame）(偏移: 0x1C)
- `Texture2D positionMap`（Texture2D position映射）(偏移: 0x20)
- `int count`（int count）(偏移: 0x24)

### 方法 (5)

- `void OnEnable()`
  （void On启用（））
- `bool IsValid(VisualEffect component)`
  （bool 是否Valid（Visual特效 component））
- `void UpdateBinding(VisualEffect component)`
  （void 更新Binding（Visual特效 component））
- `void UpdateTexture()`
  （void 更新纹理（））
- `string ToString()`
  （string To字符串（））

---

## VFXOutputEventAbstractHandler（VFXOutput事件抽象的处理器）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (2)

- `bool executeInEditor`（bool executeInEditor）(偏移: 0xC)
- `ExposedProperty outputEvent`（Exposed属性 output事件）(偏移: 0x10)

### 方法 (5)

- `void set_m_VisualEffect(VisualEffect value)`
  （void set_m_Visual特效（Visual特效 value））
- `VisualEffect get_m_VisualEffect()`
  （Visual特效 get_m_Visual特效（））
- `void OnEnable()`
  （void On启用（））
- `void OnDisable()`
  （void On禁用（））
- `void OnOutputEventRecieved(VFXOutputEventArgs args)`
  （void OnOutput事件Recieved（VFXOutput事件Args args））

---

## VFXOutputEventArgs（VFXOutput事件Args）

### 方法 (2)

- `int get_nameId()`
  （int get_nameId（））
- `VFXEventAttribute get_eventAttribute()`
  （VFX事件Attribute get_eventAttribute（））

---

## VFXPlaneBinder（VFXPlaneBinder）

**继承**: VFXBinderBase（VFXBinder基础）

### 字段 (4)

- `ExposedProperty m_Property`（Exposed属性 m_属性）(偏移: 0x10)
- `Transform Target`（变换 目标）(偏移: 0x14)
- `ExposedProperty Position`（Exposed属性 Position）(偏移: 0x18)
- `ExposedProperty Normal`（Exposed属性 法线）(偏移: 0x1C)

### 方法 (8)

- `string get_Property()`
  （string get_属性（））
- `void set_Property(string value)`
  （void set_属性（string value））
- `void OnEnable()`
  （void On启用（））
- `void OnValidate()`
  （void On验证（））
- `void UpdateSubProperties()`
  （void 更新子Properties（））
- `bool IsValid(VisualEffect component)`
  （bool 是否Valid（Visual特效 component））
- `void UpdateBinding(VisualEffect component)`
  （void 更新Binding（Visual特效 component））
- `string ToString()`
  （string To字符串（））

---

## VFXPositionBinder（VFXPositionBinder）

**继承**: VFXBinderBase（VFXBinder基础）

### 字段 (2)

- `ExposedProperty m_Property`（Exposed属性 m_属性）(偏移: 0x10)
- `Transform Target`（变换 目标）(偏移: 0x14)

### 方法 (5)

- `string get_Property()`
  （string get_属性（））
- `void set_Property(string value)`
  （void set_属性（string value））
- `bool IsValid(VisualEffect component)`
  （bool 是否Valid（Visual特效 component））
- `void UpdateBinding(VisualEffect component)`
  （void 更新Binding（Visual特效 component））
- `string ToString()`
  （string To字符串（））

---

## VFXPreviousPositionBinder（VFX上一个PositionBinder）

**继承**: VFXBinderBase（VFXBinder基础）

### 字段 (3)

- `ExposedProperty m_Property`（Exposed属性 m_属性）(偏移: 0x10)
- `Transform Target`（变换 目标）(偏移: 0x14)
- `Vector3 oldPosition`（三维向量 oldPosition）(偏移: 0x18)

### 方法 (4)

- `void OnEnable()`
  （void On启用（））
- `bool IsValid(VisualEffect component)`
  （bool 是否Valid（Visual特效 component））
- `void UpdateBinding(VisualEffect component)`
  （void 更新Binding（Visual特效 component））
- `string ToString()`
  （string To字符串（））

---

## VFXPropertyBinder（VFX属性Binder）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (3)

- `bool m_ExecuteInEditor`（bool m_执行InEditor）(偏移: 0xC)
- `List<VFXBinderBase> m_Bindings`（List<VFXBinderBase> m_Bindings）(偏移: 0x10)
- `VisualEffect m_VisualEffect`（Visual特效 m_Visual特效）(偏移: 0x14)

### 方法 (10)

- `void OnEnable()`
  （void On启用（））
- `void OnValidate()`
  （void On验证（））
- `void SafeDestroy(Object toDelete)`
  （void Safe销毁（对象 toDelete））
- `void Reload()`
  （void 换弹（））
- `void Reset()`
  （void 重置（））
- `void LateUpdate()`
  （void 延迟更新（））
- `void ClearPropertyBinders()`
  （void 清除属性Binders（））
- `void ClearParameterBinders()`
  （void 清除ParameterBinders（））
- `void RemovePropertyBinder(VFXBinderBase binder)`
  （void 移除属性Binder（VFXBinder基础 binder））
- `void RemoveParameterBinder(VFXBinderBase binder)`
  （void 移除ParameterBinder（VFXBinder基础 binder））

---

## VFXPropertyBindingAttribute（VFX属性BindingAttribute）

**继承**: PropertyAttribute（属性Attribute）

### 字段 (1)

- `string[] EditorTypes`（string[] EditorTypes）(偏移: 0x8)

---

## VFXRaycastBinder（VFXRaycastBinder）

**继承**: VFXBinderBase（VFXBinder基础）

### 字段 (11)

- `ExposedProperty m_TargetPosition`（Exposed属性 m_目标Position）(偏移: 0x10)
- `ExposedProperty m_TargetNormal`（Exposed属性 m_目标法线）(偏移: 0x14)
- `ExposedProperty m_TargetHit`（Exposed属性 m_目标命中）(偏移: 0x18)
- `ExposedProperty m_TargetPosition_position`（Exposed属性 m_目标Position_position）(偏移: 0x1C)
- `ExposedProperty m_TargetNormal_direction`（Exposed属性 m_目标Normal_direction）(偏移: 0x20)
- `GameObject RaycastSource`（游戏对象 RaycastSource）(偏移: 0x24)
- `Vector3 RaycastDirection`（三维向量 Raycast方向）(偏移: 0x28)
- `VFXRaycastBinder.Space RaycastDirectionSpace`（VFXRaycastBinder.Space Raycast方向Space）(偏移: 0x34)
- `LayerMask Layers`（层掩码 Layers）(偏移: 0x38)
- `float MaxDistance`（float 最大距离）(偏移: 0x3C)
- `RaycastHit m_HitInfo`（Raycast命中 m_命中信息）(偏移: 0x40)

### 方法 (12)

- `string get_TargetPosition()`
  （string get_目标Position（））
- `void set_TargetPosition(string value)`
  （void set_目标Position（string value））
- `string get_TargetNormal()`
  （string get_目标法线（））
- `void set_TargetNormal(string value)`
  （void set_目标法线（string value））
- `string get_TargetHit()`
  （string get_目标命中（））
- `void set_TargetHit(string value)`
  （void set_目标命中（string value））
- `void OnEnable()`
  （void On启用（））
- `void OnValidate()`
  （void On验证（））
- `void UpdateSubProperties()`
  （void 更新子Properties（））
- `bool IsValid(VisualEffect component)`
  （bool 是否Valid（Visual特效 component））
- `void UpdateBinding(VisualEffect component)`
  （void 更新Binding（Visual特效 component））
- `string ToString()`
  （string To字符串（））

---

## VFXRaycastBinder.Space（VFXRaycastBinder.Space）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## VFXRigidBodyCollisionEventBinder（VFXRigid身体Collision事件Binder）

**继承**: VFXEventBinderBase（VFX事件Binder基础）

### 字段 (2)

- `ExposedProperty positionParameter`（Exposed属性 positionParameter）(偏移: 0x18)
- `ExposedProperty directionParameter`（Exposed属性 directionParameter）(偏移: 0x1C)

### 方法 (2)

- `void SetEventAttribute(object[] parameters)`
  （void 集合事件Attribute（object[] parameters））
- `void OnCollisionEnter(Collision collision)`
  （void OnCollisionEnter（Collision collision））

---

## VFXSpawnerLoopState（VFXSpawnerLoop状态）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## VFXSpawnerState（VFXSpawner状态）

**继承**: IDisposable（IDisposable）

### 字段 (2)

- `IntPtr m_Ptr`（整数Ptr m_Ptr）(偏移: 0x8)
- `bool m_Owner`（bool m_Owner）(偏移: 0xC)

### 方法 (16)

- `VFXSpawnerState CreateSpawnerStateWrapper()`
  （VFXSpawner状态 创建Spawner状态包装器（））
- `void SetWrapValue(IntPtr ptr)`
  （void 集合Wrap值（整数Ptr ptr））
- `void Release()`
  （void Release（））
- `void Finalize()`
  （void Finalize（））
- `void Dispose()`
  （void 释放（））
- `void Internal_Destroy(IntPtr ptr)`
  （void Internal_销毁（整数Ptr ptr））
- `bool get_playing()`
  （bool get_playing（））
- `void set_playing(bool value)`
  （void set_playing（bool value））
- `VFXSpawnerLoopState get_loopState()`
  （VFXSpawnerLoop状态 get_loop状态（））
- `void set_loopState(VFXSpawnerLoopState value)`
  （void set_loop状态（VFXSpawnerLoop状态 value））
- `float get_spawnCount()`
  （float get_spawn数量（））
- `void set_spawnCount(float value)`
  （void set_spawn数量（float value））
- `float get_deltaTime()`
  （float get_delta时间（））
- `float get_totalTime()`
  （float get_total时间（））
- `void set_totalTime(float value)`
  （void set_total时间（float value））
- `VFXEventAttribute get_vfxEventAttribute()`
  （VFX事件Attribute get_vfx事件Attribute（））

---

## VFXSphereBinder（VFXSphereBinder）

**继承**: VFXBinderBase（VFXBinder基础）

### 字段 (4)

- `ExposedProperty m_Property`（Exposed属性 m_属性）(偏移: 0x10)
- `SphereCollider Target`（Sphere碰撞器 目标）(偏移: 0x14)
- `ExposedProperty Center`（Exposed属性 中心）(偏移: 0x18)
- `ExposedProperty Radius`（Exposed属性 Radius）(偏移: 0x1C)

### 方法 (9)

- `string get_Property()`
  （string get_属性（））
- `void set_Property(string value)`
  （void set_属性（string value））
- `void OnEnable()`
  （void On启用（））
- `void OnValidate()`
  （void On验证（））
- `void UpdateSubProperties()`
  （void 更新子Properties（））
- `bool IsValid(VisualEffect component)`
  （bool 是否Valid（Visual特效 component））
- `void UpdateBinding(VisualEffect component)`
  （void 更新Binding（Visual特效 component））
- `float GetSphereColliderScale(Vector3 scale)`
  （float 获取Sphere碰撞器缩放（三维向量 scale））
- `string ToString()`
  （string To字符串（））

---

## VFXTerrainBinder（VFXTerrainBinder）

**继承**: VFXBinderBase（VFXBinder基础）

### 字段 (6)

- `ExposedProperty m_Property`（Exposed属性 m_属性）(偏移: 0x10)
- `Terrain Terrain`（Terrain Terrain）(偏移: 0x14)
- `ExposedProperty Terrain_Bounds_center`（Exposed属性 Terrain_Bounds_center）(偏移: 0x18)
- `ExposedProperty Terrain_Bounds_size`（Exposed属性 Terrain_Bounds_size）(偏移: 0x1C)
- `ExposedProperty Terrain_HeightMap`（Exposed属性 Terrain_高度映射）(偏移: 0x20)
- `ExposedProperty Terrain_Height`（Exposed属性 Terrain_高度）(偏移: 0x24)

### 方法 (8)

- `string get_Property()`
  （string get_属性（））
- `void set_Property(string value)`
  （void set_属性（string value））
- `void OnEnable()`
  （void On启用（））
- `void OnValidate()`
  （void On验证（））
- `void UpdateSubProperties()`
  （void 更新子Properties（））
- `bool IsValid(VisualEffect component)`
  （bool 是否Valid（Visual特效 component））
- `void UpdateBinding(VisualEffect component)`
  （void 更新Binding（Visual特效 component））
- `string ToString()`
  （string To字符串（））

---

## VFXTransformBinder（VFX变换Binder）

**继承**: VFXBinderBase（VFXBinder基础）

### 字段 (5)

- `ExposedProperty m_Property`（Exposed属性 m_属性）(偏移: 0x10)
- `Transform Target`（变换 目标）(偏移: 0x14)
- `ExposedProperty Position`（Exposed属性 Position）(偏移: 0x18)
- `ExposedProperty Angles`（Exposed属性 Angles）(偏移: 0x1C)
- `ExposedProperty Scale`（Exposed属性 缩放）(偏移: 0x20)

### 方法 (8)

- `string get_Property()`
  （string get_属性（））
- `void set_Property(string value)`
  （void set_属性（string value））
- `void OnEnable()`
  （void On启用（））
- `void OnValidate()`
  （void On验证（））
- `void UpdateSubProperties()`
  （void 更新子Properties（））
- `bool IsValid(VisualEffect component)`
  （bool 是否Valid（Visual特效 component））
- `void UpdateBinding(VisualEffect component)`
  （void 更新Binding（Visual特效 component））
- `string ToString()`
  （string To字符串（））

---

## VFXTriggerEventBinder（VFX触发器事件Binder）

**继承**: VFXEventBinderBase（VFX事件Binder基础）

### 字段 (3)

- `List<Collider> colliders`（List<Collider> colliders）(偏移: 0x18)
- `VFXTriggerEventBinder.Activation activation`（VFX触发器事件Binder.Activation activation）(偏移: 0x1C)
- `ExposedProperty positionParameter`（Exposed属性 positionParameter）(偏移: 0x20)

### 方法 (4)

- `void SetEventAttribute(object[] parameters)`
  （void 集合事件Attribute（object[] parameters））
- `void OnTriggerEnter(Collider other)`
  （void On触发器Enter（碰撞器 other））
- `void OnTriggerExit(Collider other)`
  （void On触发器Exit（碰撞器 other））
- `void OnTriggerStay(Collider other)`
  （void On触发器Stay（碰撞器 other））

---

## VFXTriggerEventBinder.Activation（VFX触发器事件Binder.Activation）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## VFXUIDropdownBinder（VFXUIDropdownBinder）

**继承**: VFXBinderBase（VFXBinder基础）

### 字段 (2)

- `ExposedProperty m_Property`（Exposed属性 m_属性）(偏移: 0x10)
- `Dropdown Target`（Dropdown 目标）(偏移: 0x14)

### 方法 (5)

- `string get_Property()`
  （string get_属性（））
- `void set_Property(string value)`
  （void set_属性（string value））
- `bool IsValid(VisualEffect component)`
  （bool 是否Valid（Visual特效 component））
- `void UpdateBinding(VisualEffect component)`
  （void 更新Binding（Visual特效 component））
- `string ToString()`
  （string To字符串（））

---

## VFXUISliderBinder（VFXUI滑块Binder）

**继承**: VFXBinderBase（VFXBinder基础）

### 字段 (2)

- `ExposedProperty m_Property`（Exposed属性 m_属性）(偏移: 0x10)
- `Slider Target`（滑块 目标）(偏移: 0x14)

### 方法 (5)

- `string get_Property()`
  （string get_属性（））
- `void set_Property(string value)`
  （void set_属性（string value））
- `bool IsValid(VisualEffect component)`
  （bool 是否Valid（Visual特效 component））
- `void UpdateBinding(VisualEffect component)`
  （void 更新Binding（Visual特效 component））
- `string ToString()`
  （string To字符串（））

---

## VFXUIToggleBinder（VFXUI开关Binder）

**继承**: VFXBinderBase（VFXBinder基础）

### 字段 (2)

- `ExposedProperty m_Property`（Exposed属性 m_属性）(偏移: 0x10)
- `Toggle Target`（开关 目标）(偏移: 0x14)

### 方法 (5)

- `string get_Property()`
  （string get_属性（））
- `void set_Property(string value)`
  （void set_属性（string value））
- `bool IsValid(VisualEffect component)`
  （bool 是否Valid（Visual特效 component））
- `void UpdateBinding(VisualEffect component)`
  （void 更新Binding（Visual特效 component））
- `string ToString()`
  （string To字符串（））

---

## VFXVelocityBinder（VFX速度Binder）

**继承**: VFXBinderBase（VFXBinder基础）

### 字段 (5)

- `ExposedProperty m_Property`（Exposed属性 m_属性）(偏移: 0x10)
- `Transform Target`（变换 目标）(偏移: 0x14)
- `float invalidPreviousTime`（float invalid上一个时间）(偏移: 0x0)
- `float m_PreviousTime`（float m_上一个时间）(偏移: 0x18)
- `Vector3 m_PreviousPosition`（三维向量 m_上一个Position）(偏移: 0x1C)

### 方法 (6)

- `string get_Property()`
  （string get_属性（））
- `void set_Property(string value)`
  （void set_属性（string value））
- `bool IsValid(VisualEffect component)`
  （bool 是否Valid（Visual特效 component））
- `void Reset()`
  （void 重置（））
- `void UpdateBinding(VisualEffect component)`
  （void 更新Binding（Visual特效 component））
- `string ToString()`
  （string To字符串（））

---

## VFXVisibilityEventBinder（VFXVisibility事件Binder）

**继承**: VFXEventBinderBase（VFX事件Binder基础）

### 字段 (1)

- `VFXVisibilityEventBinder.Activation activation`（VFXVisibility事件Binder.Activation activation）(偏移: 0x18)

### 方法 (3)

- `void SetEventAttribute(object[] parameters)`
  （void 集合事件Attribute（object[] parameters））
- `void OnBecameVisible()`
  （void OnBecame可见的（））
- `void OnBecameInvisible()`
  （void OnBecameInvisible（））

---

## VFXVisibilityEventBinder.Activation（VFXVisibility事件Binder.Activation）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## VRIK（VRIK）

**继承**: IK（IK）

### 字段 (2)

- `VRIK.References references`（VRIK.References references）(偏移: 0x1C)
- `IKSolverVR solver`（IKSolverVR solver）(偏移: 0x20)

### 方法 (8)

- `void OpenUserManual()`
  （void 打开User手动（））
- `void OpenScriptReference()`
  （void 打开Script引用（））
- `void OpenSetupTutorial()`
  （void 打开SetupTutorial（））
- `void AutoDetectReferences()`
  （void 自动DetectReferences（））
- `void GuessHandOrientations()`
  （void Guess手部Orientations（））
- `IKSolver GetIKSolver()`
  （IKSolver 获取IKSolver（））
- `void InitiateSolver()`
  （void InitiateSolver（））
- `void UpdateSolver()`
  （void 更新Solver（））

---

## VRIK.References（VRIK.References）

### 字段 (22)

- `Transform root`（变换 root）(偏移: 0x8)
- `Transform pelvis`（变换 pelvis）(偏移: 0xC)
- `Transform spine`（变换 spine）(偏移: 0x10)
- `Transform chest`（变换 chest）(偏移: 0x14)
- `Transform neck`（变换 neck）(偏移: 0x18)
- `Transform head`（变换 head）(偏移: 0x1C)
- `Transform leftShoulder`（变换 leftShoulder）(偏移: 0x20)
- `Transform leftUpperArm`（变换 left上半身手臂）(偏移: 0x24)
- `Transform leftForearm`（变换 leftForearm）(偏移: 0x28)
- `Transform leftHand`（变换 left手部）(偏移: 0x2C)
- `Transform rightShoulder`（变换 rightShoulder）(偏移: 0x30)
- `Transform rightUpperArm`（变换 right上半身手臂）(偏移: 0x34)
- `Transform rightForearm`（变换 rightForearm）(偏移: 0x38)
- `Transform rightHand`（变换 right手部）(偏移: 0x3C)
- `Transform leftThigh`（变换 leftThigh）(偏移: 0x40)
- `Transform leftCalf`（变换 leftCalf）(偏移: 0x44)
- `Transform leftFoot`（变换 left脚部）(偏移: 0x48)
- `Transform leftToes`（变换 leftToes）(偏移: 0x4C)
- `Transform rightThigh`（变换 rightThigh）(偏移: 0x50)
- `Transform rightCalf`（变换 rightCalf）(偏移: 0x54)
- `Transform rightFoot`（变换 right脚部）(偏移: 0x58)
- `Transform rightToes`（变换 rightToes）(偏移: 0x5C)

### 方法 (4)

- `Transform[] GetTransforms()`
  （Transform[] 获取Transforms（））
- `bool get_isFilled()`
  （bool get_isFilled（））
- `bool get_isEmpty()`
  （bool get_is空（））
- `bool AutoDetectReferences(Transform root, out VRIK.References references)`
  （bool 自动DetectReferences（变换 root, out VRIK.References references））

---

## VRIKCalibrator（VRIKCalibrator）

### 方法 (5)

- `void RecalibrateScale(VRIK ik, VRIKCalibrator.Settings settings)`
  （void Recalibrate缩放（VRIK ik, VRIKCalibrator.Settings settings））
- `VRIKCalibrator.CalibrationData Calibrate(VRIK ik, VRIKCalibrator.Settings settings, Transform headTracker, Transform bodyTracker, Transform leftHandTracker, Transform rightHandTracker, Transform leftFootTracker, Transform rightFootTracker)`
  （VRIKCalibrator.Calibration数据 Calibrate（VRIK ik, VRIKCalibrator.Settings settings, 变换 headTracker, 变换 bodyTracker, 变换 leftHandTracker, 变换 rightHandTracker, 变换 leftFootTracker, 变换 rightFootTracker））
- `void CalibrateLeg(VRIKCalibrator.Settings settings, Transform tracker, IKSolverVR.Leg leg, Transform lastBone, Vector3 rootForward, bool isLeft)`
  （void Calibrate腿部（VRIKCalibrator.Settings settings, 变换 tracker, IKSolverVR.腿部 leg, 变换 lastBone, 三维向量 rootForward, bool isLeft））
- `void Calibrate(VRIK ik, VRIKCalibrator.CalibrationData data, Transform headTracker, Transform bodyTracker, Transform leftHandTracker, Transform rightHandTracker, Transform leftFootTracker, Transform rightFootTracker)`
  （void Calibrate（VRIK ik, VRIKCalibrator.Calibration数据 data, 变换 headTracker, 变换 bodyTracker, 变换 leftHandTracker, 变换 rightHandTracker, 变换 leftFootTracker, 变换 rightFootTracker））
- `void CalibrateLeg(VRIKCalibrator.CalibrationData data, Transform tracker, IKSolverVR.Leg leg, Transform lastBone, Vector3 rootForward, bool isLeft)`
  （void Calibrate腿部（VRIKCalibrator.Calibration数据 data, 变换 tracker, IKSolverVR.腿部 leg, 变换 lastBone, 三维向量 rootForward, bool isLeft））

---

## VRIKCalibrator.CalibrationData（VRIKCalibrator.Calibration数据）

### 字段 (12)

- `float scale`（float scale）(偏移: 0x8)
- `VRIKCalibrator.CalibrationData.Target head`（VRIKCalibrator.CalibrationData.目标 head）(偏移: 0xC)
- `VRIKCalibrator.CalibrationData.Target leftHand`（VRIKCalibrator.CalibrationData.目标 left手部）(偏移: 0x10)
- `VRIKCalibrator.CalibrationData.Target rightHand`（VRIKCalibrator.CalibrationData.目标 right手部）(偏移: 0x14)
- `VRIKCalibrator.CalibrationData.Target pelvis`（VRIKCalibrator.CalibrationData.目标 pelvis）(偏移: 0x18)
- `VRIKCalibrator.CalibrationData.Target leftFoot`（VRIKCalibrator.CalibrationData.目标 left脚部）(偏移: 0x1C)
- `VRIKCalibrator.CalibrationData.Target rightFoot`（VRIKCalibrator.CalibrationData.目标 right脚部）(偏移: 0x20)
- `VRIKCalibrator.CalibrationData.Target leftLegGoal`（VRIKCalibrator.CalibrationData.目标 left腿部Goal）(偏移: 0x24)
- `VRIKCalibrator.CalibrationData.Target rightLegGoal`（VRIKCalibrator.CalibrationData.目标 right腿部Goal）(偏移: 0x28)
- `Vector3 pelvisTargetRight`（三维向量 pelvis目标右）(偏移: 0x2C)
- `float pelvisPositionWeight`（float pelvisPositionWeight）(偏移: 0x38)
- `float pelvisRotationWeight`（float pelvisRotationWeight）(偏移: 0x3C)

---

## VRIKCalibrator.CalibrationData.Target（VRIKCalibrator.CalibrationData.目标）

### 字段 (3)

- `bool used`（bool used）(偏移: 0x8)
- `Vector3 localPosition`（三维向量 localPosition）(偏移: 0xC)
- `Quaternion localRotation`（Quaternion localRotation）(偏移: 0x18)

### 方法 (1)

- `void SetTo(Transform t)`
  （void 集合To（变换 t））

---

## VRIKCalibrator.Settings（VRIKCalibrator.Settings）

### 字段 (16)

- `float scaleMlp`（float scaleMlp）(偏移: 0x8)
- `Vector3 headTrackerForward`（三维向量 headTracker前进）(偏移: 0xC)
- `Vector3 headTrackerUp`（三维向量 headTracker上）(偏移: 0x18)
- `Vector3 bodyTrackerForward`（三维向量 bodyTracker前进）(偏移: 0x24)
- `Vector3 bodyTrackerUp`（三维向量 bodyTracker上）(偏移: 0x30)
- `Vector3 handTrackerForward`（三维向量 handTracker前进）(偏移: 0x3C)
- `Vector3 handTrackerUp`（三维向量 handTracker上）(偏移: 0x48)
- `Vector3 footTrackerForward`（三维向量 footTracker前进）(偏移: 0x54)
- `Vector3 footTrackerUp`（三维向量 footTracker上）(偏移: 0x60)
- `Vector3 headOffset`（三维向量 headOffset）(偏移: 0x6C)
- `Vector3 handOffset`（三维向量 handOffset）(偏移: 0x78)
- `float footForwardOffset`（float foot前进Offset）(偏移: 0x84)
- `float footInwardOffset`（float footInwardOffset）(偏移: 0x88)
- `float footHeadingOffset`（float footHeadingOffset）(偏移: 0x8C)
- `float pelvisPositionWeight`（float pelvisPositionWeight）(偏移: 0x90)
- `float pelvisRotationWeight`（float pelvisRotationWeight）(偏移: 0x94)

---

## VRIKLODController（VRIKLOD控制器）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (4)

- `Renderer LODRenderer`（渲染器 LOD渲染器）(偏移: 0xC)
- `float LODDistance`（float LOD距离）(偏移: 0x10)
- `bool allowCulled`（bool allowCulled）(偏移: 0x14)
- `VRIK ik`（VRIK ik）(偏移: 0x18)

### 方法 (3)

- `void Start()`
  （void 开始（））
- `void Update()`
  （void 更新（））
- `int GetLODLevel()`
  （int 获取LOD等级（））

---

## VRIKRootController（VRIK根控制器）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (4)

- `Transform pelvisTarget`（变换 pelvis目标）(偏移: 0x18)
- `Transform leftFootTarget`（变换 left脚部目标）(偏移: 0x1C)
- `Transform rightFootTarget`（变换 right脚部目标）(偏移: 0x20)
- `VRIK ik`（VRIK ik）(偏移: 0x24)

### 方法 (7)

- `Vector3 get_pelvisTargetRight()`
  （三维向量 get_pelvis目标右（））
- `void set_pelvisTargetRight(Vector3 value)`
  （void set_pelvis目标右（三维向量 value））
- `void Awake()`
  （void Awake（））
- `void Calibrate()`
  （void Calibrate（））
- `void Calibrate(VRIKCalibrator.CalibrationData data)`
  （void Calibrate（VRIKCalibrator.Calibration数据 data））
- `void OnPreUpdate()`
  （void OnPre更新（））
- `void OnDestroy()`
  （void On销毁（））

---

## VRTextureUsage（VR纹理Usage）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ValueFixup（值Fixup）

### 字段 (8)

- `ValueFixupEnum valueFixupEnum`（值FixupEnum valueFixupEnum）(偏移: 0x8)
- `Array arrayObj`（数组 arrayObj）(偏移: 0xC)
- `int[] indexMap`（int[] index映射）(偏移: 0x10)
- `object header`（object header）(偏移: 0x14)
- `object memberObject`（object member对象）(偏移: 0x18)
- `MemberInfo valueInfo`（Member信息 value信息）(偏移: 0x0)
- `ReadObjectInfo objectInfo`（Read对象信息 object信息）(偏移: 0x1C)
- `string memberName`（string member名称）(偏移: 0x20)

### 方法 (1)

- `void Fixup(ParseRecord record, ParseRecord parent)`
  （void Fixup（解析Record record, 解析Record parent））

---

## ValueFixupEnum（值FixupEnum）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ValueTuple（值Tuple）

**继承**: IEquatable<ValueTuple>, IStructuralEquatable, IStructuralComparable, IComparable, IComparable<ValueTuple>（IEquatable<值Tuple>, IStructuralEquatable, IStructuralComparable, IComparable, IComparable<值Tuple>）

### 方法 (7)

- `bool Equals(object obj)`
  （bool Equals（object obj））
- `bool Equals(ValueTuple other)`
  （bool Equals（值Tuple other））
- `int CompareTo(ValueTuple other)`
  （int CompareTo（值Tuple other））
- `int GetHashCode()`
  （int 获取HashCode（））
- `string ToString()`
  （string To字符串（））
- `int CombineHashCodes(int h1, int h2)`
  （int CombineHashCodes（int h1, int h2））
- `int CombineHashCodes(int h1, int h2, int h3)`
  （int CombineHashCodes（int h1, int h2, int h3））

---

## ValueType（值类型）

### 方法 (7)

- `bool InternalEquals(object o1, object o2, out object[] fields)`
  （bool 内部的Equals（object o1, object o2, out object[] fields））
- `bool DefaultEquals(object o1, object o2)`
  （bool 默认的Equals（object o1, object o2））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int InternalGetHashCode(object o, out object[] fields)`
  （int 内部的获取HashCode（object o, out object[] fields））
- `int GetHashCode()`
  （int 获取HashCode（））
- `int GetHashCodeOfPtr(IntPtr ptr)`
  （int 获取HashCodeOfPtr（整数Ptr ptr））
- `string ToString()`
  （string To字符串（））

---

## ValueType.Internal（值Type.内部的）

### 字段 (1)

- `int hash_code_of_ptr_seed`（int hash_code_of_ptr_seed）(偏移: 0x0)

---

## ValueTypeFixupInfo（值类型Fixup信息）

### 字段 (3)

- `long m_containerID`（long m_containerID）(偏移: 0x8)
- `FieldInfo m_parentField`（Field信息 m_parentField）(偏移: 0x10)
- `int[] m_parentIndex`（int[] m_parent索引）(偏移: 0x14)

### 方法 (3)

- `long get_ContainerID()`
  （long get_容器ID（））
- `FieldInfo get_ParentField()`
  （Field信息 get_父级Field（））
- `int[] get_ParentIndex()`
  （int[] get_父级索引（））

---

## VarEnum（VarEnum）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Variant（变异体）

### 字段 (20)

- `short vt`（short vt）(偏移: 0x0)
- `ushort wReserved1`（ushort wReserved1）(偏移: 0x2)
- `ushort wReserved2`（ushort wReserved2）(偏移: 0x4)
- `ushort wReserved3`（ushort wReserved3）(偏移: 0x6)
- `long llVal`（long llVal）(偏移: 0x8)
- `int lVal`（int lVal）(偏移: 0x8)
- `byte bVal`（byte bVal）(偏移: 0x8)
- `short iVal`（short iVal）(偏移: 0x8)
- `float fltVal`（float fltVal）(偏移: 0x8)
- `double dblVal`（double dblVal）(偏移: 0x8)
- `short boolVal`（short boolVal）(偏移: 0x8)
- `IntPtr bstrVal`（整数Ptr bstrVal）(偏移: 0x8)
- `sbyte cVal`（sbyte cVal）(偏移: 0x8)
- `ushort uiVal`（ushort uiVal）(偏移: 0x8)
- `uint ulVal`（uint ulVal）(偏移: 0x8)
- `ulong ullVal`（ulong ullVal）(偏移: 0x8)
- `int intVal`（int intVal）(偏移: 0x8)
- `uint uintVal`（uint uintVal）(偏移: 0x8)
- `IntPtr pdispVal`（整数Ptr pdispVal）(偏移: 0x8)
- `BRECORD bRecord`（BRECORD bRecord）(偏移: 0x8)

### 方法 (1)

- `void Clear()`
  （void 清除（））

---

## Vec3（Vec3）

### 字段 (4)

- `Vec3 Zero`（Vec3 Zero）(偏移: 0x0)
- `float X`（float X）(偏移: 0x0)
- `float Y`（float Y）(偏移: 0x4)
- `float Z`（float Z）(偏移: 0x8)

### 方法 (8)

- `float get_Item(int index)`
  （float get_项目（int index））
- `void set_Item(int index, float value)`
  （void set_项目（int index, float value））
- `void Sub(ref Vec3 lhs, ref Vec3 rhs, out Vec3 result)`
  （void 子（ref Vec3 lhs, ref Vec3 rhs, out Vec3 result））
- `void Neg(ref Vec3 v)`
  （void Neg（ref Vec3 v））
- `void Dot(ref Vec3 u, ref Vec3 v, out float dot)`
  （void Dot（ref Vec3 u, ref Vec3 v, out float dot））
- `void Normalize(ref Vec3 v)`
  （void Normalize（ref Vec3 v））
- `int LongAxis(ref Vec3 v)`
  （int Long轴（ref Vec3 v））
- `string ToString()`
  （string To字符串（））

---

## Vector2（二维向量）

**继承**: IEquatable<Vector2>, IFormattable（IEquatable<Vector2>, IFormattable）

### 字段 (10)

- `float x`（float x）(偏移: 0x0)
- `float y`（float y）(偏移: 0x4)
- `Vector2 zeroVector`（二维向量 zero向量）(偏移: 0x0)
- `Vector2 oneVector`（二维向量 one向量）(偏移: 0x8)
- `Vector2 upVector`（二维向量 up向量）(偏移: 0x10)
- `Vector2 downVector`（二维向量 down向量）(偏移: 0x18)
- `Vector2 leftVector`（二维向量 left向量）(偏移: 0x20)
- `Vector2 rightVector`（二维向量 right向量）(偏移: 0x28)
- `Vector2 positiveInfinityVector`（二维向量 positive无限向量）(偏移: 0x30)
- `Vector2 negativeInfinityVector`（二维向量 negative无限向量）(偏移: 0x38)

### 方法 (38)

- `float get_Item(int index)`
  （float get_项目（int index））
- `void set_Item(int index, float value)`
  （void set_项目（int index, float value））
- `Vector2 Lerp(Vector2 a, Vector2 b, float t)`
  （二维向量 Lerp（二维向量 a, 二维向量 b, float t））
- `Vector2 Scale(Vector2 a, Vector2 b)`
  （二维向量 缩放（二维向量 a, 二维向量 b））
- `void Normalize()`
  （void Normalize（））
- `Vector2 get_normalized()`
  （二维向量 get_normalized（））
- `string ToString()`
  （string To字符串（））
- `string ToString(string format)`
  （string To字符串（string format））
- `string ToString(string format, IFormatProvider formatProvider)`
  （string To字符串（string format, I格式化提供者 formatProvider））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool Equals(object other)`
  （bool Equals（object other））
- `bool Equals(Vector2 other)`
  （bool Equals（二维向量 other））
- `float Dot(Vector2 lhs, Vector2 rhs)`
  （float Dot（二维向量 lhs, 二维向量 rhs））
- `float get_magnitude()`
  （float get_magnitude（））
- `float get_sqrMagnitude()`
  （float get_sqrMagnitude（））
- `float Angle(Vector2 from, Vector2 to)`
  （float 角度（二维向量 from, 二维向量 to））
- `float Distance(Vector2 a, Vector2 b)`
  （float 距离（二维向量 a, 二维向量 b））
- `Vector2 ClampMagnitude(Vector2 vector, float maxLength)`
  （二维向量 ClampMagnitude（二维向量 vector, float maxLength））
- `float SqrMagnitude(Vector2 a)`
  （float SqrMagnitude（二维向量 a））
- `Vector2 Min(Vector2 lhs, Vector2 rhs)`
  （二维向量 最小（二维向量 lhs, 二维向量 rhs））
- `Vector2 Max(Vector2 lhs, Vector2 rhs)`
  （二维向量 最大（二维向量 lhs, 二维向量 rhs））
- `Vector2 op_Addition(Vector2 a, Vector2 b)`
  （二维向量 op_Addition（二维向量 a, 二维向量 b））
- `Vector2 op_Subtraction(Vector2 a, Vector2 b)`
  （二维向量 op_Subtraction（二维向量 a, 二维向量 b））
- `Vector2 op_Multiply(Vector2 a, Vector2 b)`
  （二维向量 op_Multiply（二维向量 a, 二维向量 b））
- `Vector2 op_Division(Vector2 a, Vector2 b)`
  （二维向量 op_Division（二维向量 a, 二维向量 b））
- `Vector2 op_UnaryNegation(Vector2 a)`
  （二维向量 op_UnaryNegation（二维向量 a））
- `Vector2 op_Multiply(Vector2 a, float d)`
  （二维向量 op_Multiply（二维向量 a, float d））
- `Vector2 op_Multiply(float d, Vector2 a)`
  （二维向量 op_Multiply（float d, 二维向量 a））
- `Vector2 op_Division(Vector2 a, float d)`
  （二维向量 op_Division（二维向量 a, float d））
- `bool op_Equality(Vector2 lhs, Vector2 rhs)`
  （bool op_Equality（二维向量 lhs, 二维向量 rhs））
- `bool op_Inequality(Vector2 lhs, Vector2 rhs)`
  （bool op_Inequality（二维向量 lhs, 二维向量 rhs））
- `Vector2 op_Implicit(Vector3 v)`
  （二维向量 op_Implicit（三维向量 v））
- `Vector3 op_Implicit(Vector2 v)`
  （三维向量 op_Implicit（二维向量 v））
- `Vector2 get_zero()`
  （二维向量 get_zero（））
- `Vector2 get_one()`
  （二维向量 get_one（））
- `Vector2 get_up()`
  （二维向量 get_up（））
- `Vector2 get_down()`
  （二维向量 get_down（））
- `Vector2 get_right()`
  （二维向量 get_right（））

---

## Vector2Int（二维向量整数）

**继承**: IEquatable<Vector2Int>, IFormattable（IEquatable<二维向量Int>, IFormattable）

### 字段 (8)

- `int m_X`（int m_X）(偏移: 0x0)
- `int m_Y`（int m_Y）(偏移: 0x4)
- `Vector2Int s_Zero`（二维向量整数 s_Zero）(偏移: 0x0)
- `Vector2Int s_One`（二维向量整数 s_One）(偏移: 0x8)
- `Vector2Int s_Up`（二维向量整数 s_上）(偏移: 0x10)
- `Vector2Int s_Down`（二维向量整数 s_下）(偏移: 0x18)
- `Vector2Int s_Left`（二维向量整数 s_左）(偏移: 0x20)
- `Vector2Int s_Right`（二维向量整数 s_右）(偏移: 0x28)

### 方法 (15)

- `int get_x()`
  （int get_x（））
- `void set_x(int value)`
  （void set_x（int value））
- `int get_y()`
  （int get_y（））
- `void set_y(int value)`
  （void set_y（int value））
- `Vector2Int Max(Vector2Int lhs, Vector2Int rhs)`
  （二维向量整数 最大（二维向量整数 lhs, 二维向量整数 rhs））
- `Vector2 op_Implicit(Vector2Int v)`
  （二维向量 op_Implicit（二维向量整数 v））
- `bool op_Equality(Vector2Int lhs, Vector2Int rhs)`
  （bool op_Equality（二维向量整数 lhs, 二维向量整数 rhs））
- `bool op_Inequality(Vector2Int lhs, Vector2Int rhs)`
  （bool op_Inequality（二维向量整数 lhs, 二维向量整数 rhs））
- `bool Equals(object other)`
  （bool Equals（object other））
- `bool Equals(Vector2Int other)`
  （bool Equals（二维向量整数 other））
- `int GetHashCode()`
  （int 获取HashCode（））
- `string ToString()`
  （string To字符串（））
- `string ToString(string format, IFormatProvider formatProvider)`
  （string To字符串（string format, I格式化提供者 formatProvider））
- `Vector2Int get_zero()`
  （二维向量整数 get_zero（））
- `Vector2Int get_one()`
  （二维向量整数 get_one（））

---

## Vector2Parameter（二维向量Parameter）

**继承**: VolumeParameter<Vector2>（VolumeParameter<Vector2>）

### 方法 (1)

- `void Interp(Vector2 from, Vector2 to, float t)`
  （void Interp（二维向量 from, 二维向量 to, float t））

---

## Vector2Plugin（二维向量插件）

**继承**: ABSTweenPlugin<Vector2, Vector2, VectorOptions>（ABSTweenPlugin<二维向量, 二维向量, 向量Options>）

### 方法 (8)

- `void Reset(TweenerCore<Vector2, Vector2, VectorOptions> t)`
  （void 重置（TweenerCore<二维向量, 二维向量, 向量Options> t））
- `void SetFrom(TweenerCore<Vector2, Vector2, VectorOptions> t, bool isRelative)`
  （void 集合From（TweenerCore<二维向量, 二维向量, 向量Options> t, bool isRelative））
- `void SetFrom(TweenerCore<Vector2, Vector2, VectorOptions> t, Vector2 fromValue, bool setImmediately, bool isRelative)`
  （void 集合From（TweenerCore<二维向量, 二维向量, 向量Options> t, 二维向量 fromValue, bool setImmediately, bool isRelative））
- `Vector2 ConvertToStartValue(TweenerCore<Vector2, Vector2, VectorOptions> t, Vector2 value)`
  （二维向量 转换To开始值（TweenerCore<二维向量, 二维向量, 向量Options> t, 二维向量 value））
- `void SetRelativeEndValue(TweenerCore<Vector2, Vector2, VectorOptions> t)`
  （void 集合Relative结束值（TweenerCore<二维向量, 二维向量, 向量Options> t））
- `void SetChangeValue(TweenerCore<Vector2, Vector2, VectorOptions> t)`
  （void 集合Change值（TweenerCore<二维向量, 二维向量, 向量Options> t））
- `float GetSpeedBasedDuration(VectorOptions options, float unitsXSecond, Vector2 changeValue)`
  （float 获取SpeedBased持续时间（向量Options options, float unitsXSecond, 二维向量 changeValue））
- `void EvaluateAndApply(VectorOptions options, Tween t, bool isRelative, DOGetter<Vector2> getter, DOSetter<Vector2> setter, float elapsed, Vector2 startValue, Vector2 changeValue, float duration, bool usingInversePosition, UpdateNotice updateNotice)`
  （void EvaluateAnd应用（向量Options options, Tween t, bool isRelative, DOGetter<Vector2> getter, DOSetter<Vector2> setter, float elapsed, 二维向量 startValue, 二维向量 changeValue, float duration, bool usingInversePosition, 更新Notice updateNotice））

---

## Vector3（三维向量）

**继承**: IEquatable<Vector3>, IFormattable（IEquatable<Vector3>, IFormattable）

### 字段 (13)

- `float x`（float x）(偏移: 0x0)
- `float y`（float y）(偏移: 0x4)
- `float z`（float z）(偏移: 0x8)
- `Vector3 zeroVector`（三维向量 zero向量）(偏移: 0x0)
- `Vector3 oneVector`（三维向量 one向量）(偏移: 0xC)
- `Vector3 upVector`（三维向量 up向量）(偏移: 0x18)
- `Vector3 downVector`（三维向量 down向量）(偏移: 0x24)
- `Vector3 leftVector`（三维向量 left向量）(偏移: 0x30)
- `Vector3 rightVector`（三维向量 right向量）(偏移: 0x3C)
- `Vector3 forwardVector`（三维向量 forward向量）(偏移: 0x48)
- `Vector3 backVector`（三维向量 back向量）(偏移: 0x54)
- `Vector3 positiveInfinityVector`（三维向量 positive无限向量）(偏移: 0x60)
- `Vector3 negativeInfinityVector`（三维向量 negative无限向量）(偏移: 0x6C)

### 方法 (54)

- `Vector3 Slerp(Vector3 a, Vector3 b, float t)`
  （三维向量 Slerp（三维向量 a, 三维向量 b, float t））
- `void OrthoNormalize2(ref Vector3 a, ref Vector3 b)`
  （void OrthoNormalize2（ref Vector3 a, ref Vector3 b））
- `void OrthoNormalize(ref Vector3 normal, ref Vector3 tangent)`
  （void OrthoNormalize（ref Vector3 normal, ref Vector3 tangent））
- `Vector3 RotateTowards(Vector3 current, Vector3 target, float maxRadiansDelta, float maxMagnitudeDelta)`
  （三维向量 RotateTowards（三维向量 current, 三维向量 target, float maxRadiansDelta, float maxMagnitudeDelta））
- `Vector3 Lerp(Vector3 a, Vector3 b, float t)`
  （三维向量 Lerp（三维向量 a, 三维向量 b, float t））
- `Vector3 LerpUnclamped(Vector3 a, Vector3 b, float t)`
  （三维向量 LerpUnclamped（三维向量 a, 三维向量 b, float t））
- `Vector3 SmoothDamp(Vector3 current, Vector3 target, ref Vector3 currentVelocity, float smoothTime)`
  （三维向量 SmoothDamp（三维向量 current, 三维向量 target, ref Vector3 currentVelocity, float smoothTime））
- `Vector3 SmoothDamp(Vector3 current, Vector3 target, ref Vector3 currentVelocity, float smoothTime, float maxSpeed, float deltaTime)`
  （三维向量 SmoothDamp（三维向量 current, 三维向量 target, ref Vector3 currentVelocity, float smoothTime, float maxSpeed, float deltaTime））
- `float get_Item(int index)`
  （float get_项目（int index））
- `void set_Item(int index, float value)`
  （void set_项目（int index, float value））
- `Vector3 Scale(Vector3 a, Vector3 b)`
  （三维向量 缩放（三维向量 a, 三维向量 b））
- `void Scale(Vector3 scale)`
  （void 缩放（三维向量 scale））
- `Vector3 Cross(Vector3 lhs, Vector3 rhs)`
  （三维向量 Cross（三维向量 lhs, 三维向量 rhs））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool Equals(object other)`
  （bool Equals（object other））
- `bool Equals(Vector3 other)`
  （bool Equals（三维向量 other））
- `Vector3 Reflect(Vector3 inDirection, Vector3 inNormal)`
  （三维向量 Reflect（三维向量 inDirection, 三维向量 inNormal））
- `Vector3 Normalize(Vector3 value)`
  （三维向量 Normalize（三维向量 value））
- `void Normalize()`
  （void Normalize（））
- `Vector3 get_normalized()`
  （三维向量 get_normalized（））
- `float Dot(Vector3 lhs, Vector3 rhs)`
  （float Dot（三维向量 lhs, 三维向量 rhs））
- `Vector3 Project(Vector3 vector, Vector3 onNormal)`
  （三维向量 Project（三维向量 vector, 三维向量 onNormal））
- `Vector3 ProjectOnPlane(Vector3 vector, Vector3 planeNormal)`
  （三维向量 ProjectOnPlane（三维向量 vector, 三维向量 planeNormal））
- `float Angle(Vector3 from, Vector3 to)`
  （float 角度（三维向量 from, 三维向量 to））
- `float SignedAngle(Vector3 from, Vector3 to, Vector3 axis)`
  （float Signed角度（三维向量 from, 三维向量 to, 三维向量 axis））
- `float Distance(Vector3 a, Vector3 b)`
  （float 距离（三维向量 a, 三维向量 b））
- `Vector3 ClampMagnitude(Vector3 vector, float maxLength)`
  （三维向量 ClampMagnitude（三维向量 vector, float maxLength））
- `float Magnitude(Vector3 vector)`
  （float Magnitude（三维向量 vector））
- `float get_magnitude()`
  （float get_magnitude（））
- `float SqrMagnitude(Vector3 vector)`
  （float SqrMagnitude（三维向量 vector））
- `float get_sqrMagnitude()`
  （float get_sqrMagnitude（））
- `Vector3 Min(Vector3 lhs, Vector3 rhs)`
  （三维向量 最小（三维向量 lhs, 三维向量 rhs））
- `Vector3 Max(Vector3 lhs, Vector3 rhs)`
  （三维向量 最大（三维向量 lhs, 三维向量 rhs））
- `Vector3 get_zero()`
  （三维向量 get_zero（））
- `Vector3 get_one()`
  （三维向量 get_one（））
- `Vector3 get_forward()`
  （三维向量 get_forward（））
- `Vector3 get_back()`
  （三维向量 get_back（））
- `Vector3 get_up()`
  （三维向量 get_up（））
- `Vector3 get_down()`
  （三维向量 get_down（））
- `Vector3 get_left()`
  （三维向量 get_left（））
- `Vector3 get_right()`
  （三维向量 get_right（））
- `Vector3 op_Addition(Vector3 a, Vector3 b)`
  （三维向量 op_Addition（三维向量 a, 三维向量 b））
- `Vector3 op_Subtraction(Vector3 a, Vector3 b)`
  （三维向量 op_Subtraction（三维向量 a, 三维向量 b））
- `Vector3 op_UnaryNegation(Vector3 a)`
  （三维向量 op_UnaryNegation（三维向量 a））
- `Vector3 op_Multiply(Vector3 a, float d)`
  （三维向量 op_Multiply（三维向量 a, float d））
- `Vector3 op_Multiply(float d, Vector3 a)`
  （三维向量 op_Multiply（float d, 三维向量 a））
- `Vector3 op_Division(Vector3 a, float d)`
  （三维向量 op_Division（三维向量 a, float d））
- `bool op_Equality(Vector3 lhs, Vector3 rhs)`
  （bool op_Equality（三维向量 lhs, 三维向量 rhs））
- `bool op_Inequality(Vector3 lhs, Vector3 rhs)`
  （bool op_Inequality（三维向量 lhs, 三维向量 rhs））
- `string ToString()`
  （string To字符串（））
- `string ToString(string format)`
  （string To字符串（string format））
- `string ToString(string format, IFormatProvider formatProvider)`
  （string To字符串（string format, I格式化提供者 formatProvider））
- `void Slerp_Injected(ref Vector3 a, ref Vector3 b, float t, out Vector3 ret)`
  （void Slerp_Injected（ref Vector3 a, ref Vector3 b, float t, out Vector3 ret））
- `void RotateTowards_Injected(ref Vector3 current, ref Vector3 target, float maxRadiansDelta, float maxMagnitudeDelta, out Vector3 ret)`
  （void RotateTowards_Injected（ref Vector3 current, ref Vector3 target, float maxRadiansDelta, float maxMagnitudeDelta, out Vector3 ret））

---

## Vector3ArrayOptions（三维向量数组Options）

**继承**: IPlugOptions（IPlugOptions）

### 字段 (3)

- `AxisConstraint axisConstraint`（轴Constraint axisConstraint）(偏移: 0x0)
- `bool snapping`（bool snapping）(偏移: 0x4)
- `float[] durations`（float[] durations）(偏移: 0x8)

### 方法 (1)

- `void Reset()`
  （void 重置（））

---

## Vector3ArrayPlugin（三维向量数组插件）

**继承**: ABSTweenPlugin<Vector3, Vector3[], Vector3ArrayOptions>（ABSTweenPlugin<三维向量, Vector3[], 三维向量数组Options>）

### 方法 (8)

- `void Reset(TweenerCore<Vector3, Vector3[], Vector3ArrayOptions> t)`
  （void 重置（TweenerCore<三维向量, Vector3[], 三维向量数组Options> t））
- `void SetFrom(TweenerCore<Vector3, Vector3[], Vector3ArrayOptions> t, bool isRelative)`
  （void 集合From（TweenerCore<三维向量, Vector3[], 三维向量数组Options> t, bool isRelative））
- `void SetFrom(TweenerCore<Vector3, Vector3[], Vector3ArrayOptions> t, Vector3[] fromValue, bool setImmediately, bool isRelative)`
  （void 集合From（TweenerCore<三维向量, Vector3[], 三维向量数组Options> t, Vector3[] fromValue, bool setImmediately, bool isRelative））
- `Vector3[] ConvertToStartValue(TweenerCore<Vector3, Vector3[], Vector3ArrayOptions> t, Vector3 value)`
  （Vector3[] 转换To开始值（TweenerCore<三维向量, Vector3[], 三维向量数组Options> t, 三维向量 value））
- `void SetRelativeEndValue(TweenerCore<Vector3, Vector3[], Vector3ArrayOptions> t)`
  （void 集合Relative结束值（TweenerCore<三维向量, Vector3[], 三维向量数组Options> t））
- `void SetChangeValue(TweenerCore<Vector3, Vector3[], Vector3ArrayOptions> t)`
  （void 集合Change值（TweenerCore<三维向量, Vector3[], 三维向量数组Options> t））
- `float GetSpeedBasedDuration(Vector3ArrayOptions options, float unitsXSecond, Vector3[] changeValue)`
  （float 获取SpeedBased持续时间（三维向量数组Options options, float unitsXSecond, Vector3[] changeValue））
- `void EvaluateAndApply(Vector3ArrayOptions options, Tween t, bool isRelative, DOGetter<Vector3> getter, DOSetter<Vector3> setter, float elapsed, Vector3[] startValue, Vector3[] changeValue, float duration, bool usingInversePosition, UpdateNotice updateNotice)`
  （void EvaluateAnd应用（三维向量数组Options options, Tween t, bool isRelative, DOGetter<Vector3> getter, DOSetter<Vector3> setter, float elapsed, Vector3[] startValue, Vector3[] changeValue, float duration, bool usingInversePosition, 更新Notice updateNotice））

---

## Vector3Int（三维向量整数）

**继承**: IEquatable<Vector3Int>, IFormattable（IEquatable<三维向量Int>, IFormattable）

### 字段 (11)

- `int m_X`（int m_X）(偏移: 0x0)
- `int m_Y`（int m_Y）(偏移: 0x4)
- `int m_Z`（int m_Z）(偏移: 0x8)
- `Vector3Int s_Zero`（三维向量整数 s_Zero）(偏移: 0x0)
- `Vector3Int s_One`（三维向量整数 s_One）(偏移: 0xC)
- `Vector3Int s_Up`（三维向量整数 s_上）(偏移: 0x18)
- `Vector3Int s_Down`（三维向量整数 s_下）(偏移: 0x24)
- `Vector3Int s_Left`（三维向量整数 s_左）(偏移: 0x30)
- `Vector3Int s_Right`（三维向量整数 s_右）(偏移: 0x3C)
- `Vector3Int s_Forward`（三维向量整数 s_前进）(偏移: 0x48)
- `Vector3Int s_Back`（三维向量整数 s_后）(偏移: 0x54)

### 方法 (20)

- `int get_x()`
  （int get_x（））
- `void set_x(int value)`
  （void set_x（int value））
- `int get_y()`
  （int get_y（））
- `void set_y(int value)`
  （void set_y（int value））
- `int get_z()`
  （int get_z（））
- `void set_z(int value)`
  （void set_z（int value））
- `Vector3 op_Implicit(Vector3Int v)`
  （三维向量 op_Implicit（三维向量整数 v））
- `Vector3Int op_Addition(Vector3Int a, Vector3Int b)`
  （三维向量整数 op_Addition（三维向量整数 a, 三维向量整数 b））
- `Vector3Int op_Subtraction(Vector3Int a, Vector3Int b)`
  （三维向量整数 op_Subtraction（三维向量整数 a, 三维向量整数 b））
- `Vector3Int op_Multiply(Vector3Int a, int b)`
  （三维向量整数 op_Multiply（三维向量整数 a, int b））
- `bool op_Equality(Vector3Int lhs, Vector3Int rhs)`
  （bool op_Equality（三维向量整数 lhs, 三维向量整数 rhs））
- `bool op_Inequality(Vector3Int lhs, Vector3Int rhs)`
  （bool op_Inequality（三维向量整数 lhs, 三维向量整数 rhs））
- `bool Equals(object other)`
  （bool Equals（object other））
- `bool Equals(Vector3Int other)`
  （bool Equals（三维向量整数 other））
- `int GetHashCode()`
  （int 获取HashCode（））
- `string ToString()`
  （string To字符串（））
- `string ToString(string format)`
  （string To字符串（string format））
- `string ToString(string format, IFormatProvider formatProvider)`
  （string To字符串（string format, I格式化提供者 formatProvider））
- `Vector3Int get_zero()`
  （三维向量整数 get_zero（））
- `Vector3Int get_forward()`
  （三维向量整数 get_forward（））

---

## Vector3Parameter（三维向量Parameter）

**继承**: VolumeParameter<Vector3>（VolumeParameter<Vector3>）

### 方法 (1)

- `void Interp(Vector3 from, Vector3 to, float t)`
  （void Interp（三维向量 from, 三维向量 to, float t））

---

## Vector3Plugin（三维向量插件）

**继承**: ABSTweenPlugin<Vector3, Vector3, VectorOptions>（ABSTweenPlugin<三维向量, 三维向量, 向量Options>）

### 方法 (8)

- `void Reset(TweenerCore<Vector3, Vector3, VectorOptions> t)`
  （void 重置（TweenerCore<三维向量, 三维向量, 向量Options> t））
- `void SetFrom(TweenerCore<Vector3, Vector3, VectorOptions> t, bool isRelative)`
  （void 集合From（TweenerCore<三维向量, 三维向量, 向量Options> t, bool isRelative））
- `void SetFrom(TweenerCore<Vector3, Vector3, VectorOptions> t, Vector3 fromValue, bool setImmediately, bool isRelative)`
  （void 集合From（TweenerCore<三维向量, 三维向量, 向量Options> t, 三维向量 fromValue, bool setImmediately, bool isRelative））
- `Vector3 ConvertToStartValue(TweenerCore<Vector3, Vector3, VectorOptions> t, Vector3 value)`
  （三维向量 转换To开始值（TweenerCore<三维向量, 三维向量, 向量Options> t, 三维向量 value））
- `void SetRelativeEndValue(TweenerCore<Vector3, Vector3, VectorOptions> t)`
  （void 集合Relative结束值（TweenerCore<三维向量, 三维向量, 向量Options> t））
- `void SetChangeValue(TweenerCore<Vector3, Vector3, VectorOptions> t)`
  （void 集合Change值（TweenerCore<三维向量, 三维向量, 向量Options> t））
- `float GetSpeedBasedDuration(VectorOptions options, float unitsXSecond, Vector3 changeValue)`
  （float 获取SpeedBased持续时间（向量Options options, float unitsXSecond, 三维向量 changeValue））
- `void EvaluateAndApply(VectorOptions options, Tween t, bool isRelative, DOGetter<Vector3> getter, DOSetter<Vector3> setter, float elapsed, Vector3 startValue, Vector3 changeValue, float duration, bool usingInversePosition, UpdateNotice updateNotice)`
  （void EvaluateAnd应用（向量Options options, Tween t, bool isRelative, DOGetter<Vector3> getter, DOSetter<Vector3> setter, float elapsed, 三维向量 startValue, 三维向量 changeValue, float duration, bool usingInversePosition, 更新Notice updateNotice））

---

## Vector4（Vector4）

**继承**: IEquatable<Vector4>, IFormattable（IEquatable<Vector4>, IFormattable）

### 字段 (8)

- `float x`（float x）(偏移: 0x0)
- `float y`（float y）(偏移: 0x4)
- `float z`（float z）(偏移: 0x8)
- `float w`（float w）(偏移: 0xC)
- `Vector4 zeroVector`（Vector4 zero向量）(偏移: 0x0)
- `Vector4 oneVector`（Vector4 one向量）(偏移: 0x10)
- `Vector4 positiveInfinityVector`（Vector4 positive无限向量）(偏移: 0x20)
- `Vector4 negativeInfinityVector`（Vector4 negative无限向量）(偏移: 0x30)

### 方法 (26)

- `float get_Item(int index)`
  （float get_项目（int index））
- `void set_Item(int index, float value)`
  （void set_项目（int index, float value））
- `Vector4 Lerp(Vector4 a, Vector4 b, float t)`
  （Vector4 Lerp（Vector4 a, Vector4 b, float t））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool Equals(object other)`
  （bool Equals（object other））
- `bool Equals(Vector4 other)`
  （bool Equals（Vector4 other））
- `Vector4 Normalize(Vector4 a)`
  （Vector4 Normalize（Vector4 a））
- `Vector4 get_normalized()`
  （Vector4 get_normalized（））
- `float Dot(Vector4 a, Vector4 b)`
  （float Dot（Vector4 a, Vector4 b））
- `float Magnitude(Vector4 a)`
  （float Magnitude（Vector4 a））
- `float get_magnitude()`
  （float get_magnitude（））
- `float get_sqrMagnitude()`
  （float get_sqrMagnitude（））
- `Vector4 get_zero()`
  （Vector4 get_zero（））
- `Vector4 get_one()`
  （Vector4 get_one（））
- `Vector4 op_Addition(Vector4 a, Vector4 b)`
  （Vector4 op_Addition（Vector4 a, Vector4 b））
- `Vector4 op_Subtraction(Vector4 a, Vector4 b)`
  （Vector4 op_Subtraction（Vector4 a, Vector4 b））
- `Vector4 op_UnaryNegation(Vector4 a)`
  （Vector4 op_UnaryNegation（Vector4 a））
- `Vector4 op_Multiply(Vector4 a, float d)`
  （Vector4 op_Multiply（Vector4 a, float d））
- `Vector4 op_Multiply(float d, Vector4 a)`
  （Vector4 op_Multiply（float d, Vector4 a））
- `Vector4 op_Division(Vector4 a, float d)`
  （Vector4 op_Division（Vector4 a, float d））
- `bool op_Equality(Vector4 lhs, Vector4 rhs)`
  （bool op_Equality（Vector4 lhs, Vector4 rhs））
- `Vector4 op_Implicit(Vector3 v)`
  （Vector4 op_Implicit（三维向量 v））
- `Vector3 op_Implicit(Vector4 v)`
  （三维向量 op_Implicit（Vector4 v））
- `Vector4 op_Implicit(Vector2 v)`
  （Vector4 op_Implicit（二维向量 v））
- `string ToString()`
  （string To字符串（））
- `string ToString(string format, IFormatProvider formatProvider)`
  （string To字符串（string format, I格式化提供者 formatProvider））

---

## Vector4Parameter（Vector4Parameter）

**继承**: VolumeParameter<Vector4>（VolumeParameter<Vector4>）

### 方法 (1)

- `void Interp(Vector4 from, Vector4 to, float t)`
  （void Interp（Vector4 from, Vector4 to, float t））

---

## Vector4Plugin（Vector4插件）

**继承**: ABSTweenPlugin<Vector4, Vector4, VectorOptions>（ABSTweenPlugin<Vector4, Vector4, 向量Options>）

### 方法 (8)

- `void Reset(TweenerCore<Vector4, Vector4, VectorOptions> t)`
  （void 重置（TweenerCore<Vector4, Vector4, 向量Options> t））
- `void SetFrom(TweenerCore<Vector4, Vector4, VectorOptions> t, bool isRelative)`
  （void 集合From（TweenerCore<Vector4, Vector4, 向量Options> t, bool isRelative））
- `void SetFrom(TweenerCore<Vector4, Vector4, VectorOptions> t, Vector4 fromValue, bool setImmediately, bool isRelative)`
  （void 集合From（TweenerCore<Vector4, Vector4, 向量Options> t, Vector4 fromValue, bool setImmediately, bool isRelative））
- `Vector4 ConvertToStartValue(TweenerCore<Vector4, Vector4, VectorOptions> t, Vector4 value)`
  （Vector4 转换To开始值（TweenerCore<Vector4, Vector4, 向量Options> t, Vector4 value））
- `void SetRelativeEndValue(TweenerCore<Vector4, Vector4, VectorOptions> t)`
  （void 集合Relative结束值（TweenerCore<Vector4, Vector4, 向量Options> t））
- `void SetChangeValue(TweenerCore<Vector4, Vector4, VectorOptions> t)`
  （void 集合Change值（TweenerCore<Vector4, Vector4, 向量Options> t））
- `float GetSpeedBasedDuration(VectorOptions options, float unitsXSecond, Vector4 changeValue)`
  （float 获取SpeedBased持续时间（向量Options options, float unitsXSecond, Vector4 changeValue））
- `void EvaluateAndApply(VectorOptions options, Tween t, bool isRelative, DOGetter<Vector4> getter, DOSetter<Vector4> setter, float elapsed, Vector4 startValue, Vector4 changeValue, float duration, bool usingInversePosition, UpdateNotice updateNotice)`
  （void EvaluateAnd应用（向量Options options, Tween t, bool isRelative, DOGetter<Vector4> getter, DOSetter<Vector4> setter, float elapsed, Vector4 startValue, Vector4 changeValue, float duration, bool usingInversePosition, 更新Notice updateNotice））

---

## VectorMath（向量数学）

### 方法 (55)

- `Vector2 ComplexMultiply(Vector2 a, Vector2 b)`
  （二维向量 ComplexMultiply（二维向量 a, 二维向量 b））
- `Vector2 ComplexMultiplyConjugate(Vector2 a, Vector2 b)`
  （二维向量 ComplexMultiplyConjugate（二维向量 a, 二维向量 b））
- `Vector3 ClosestPointOnLine(Vector3 lineStart, Vector3 lineEnd, Vector3 point)`
  （三维向量 ClosestPointOnLine（三维向量 lineStart, 三维向量 lineEnd, 三维向量 point））
- `float ClosestPointOnLineFactor(Vector3 lineStart, Vector3 lineEnd, Vector3 point)`
  （float ClosestPointOnLine系数（三维向量 lineStart, 三维向量 lineEnd, 三维向量 point））
- `float ClosestPointOnLineFactor(Int3 lineStart, Int3 lineEnd, Int3 point)`
  （float ClosestPointOnLine系数（Int3 lineStart, Int3 lineEnd, Int3 point））
- `float ClosestPointOnLineFactor(Int2 lineStart, Int2 lineEnd, Int2 point)`
  （float ClosestPointOnLine系数（Int2 lineStart, Int2 lineEnd, Int2 point））
- `Vector3 ClosestPointOnSegment(Vector3 lineStart, Vector3 lineEnd, Vector3 point)`
  （三维向量 ClosestPointOnSegment（三维向量 lineStart, 三维向量 lineEnd, 三维向量 point））
- `Vector3 ClosestPointOnSegmentXZ(Vector3 lineStart, Vector3 lineEnd, Vector3 point)`
  （三维向量 ClosestPointOnSegmentXZ（三维向量 lineStart, 三维向量 lineEnd, 三维向量 point））
- `float SqrDistancePointSegmentApproximate(int x, int z, int px, int pz, int qx, int qz)`
  （float Sqr距离PointSegmentApproximate（int x, int z, int px, int pz, int qx, int qz））
- `float SqrDistancePointSegmentApproximate(Int3 a, Int3 b, Int3 p)`
  （float Sqr距离PointSegmentApproximate（Int3 a, Int3 b, Int3 p））
- `float SqrDistancePointSegment(Vector3 a, Vector3 b, Vector3 p)`
  （float Sqr距离PointSegment（三维向量 a, 三维向量 b, 三维向量 p））
- `float SqrDistanceSegmentSegment(Vector3 s1, Vector3 e1, Vector3 s2, Vector3 e2)`
  （float Sqr距离SegmentSegment（三维向量 s1, 三维向量 e1, 三维向量 s2, 三维向量 e2））
- `float SqrDistanceXZ(Vector3 a, Vector3 b)`
  （float Sqr距离XZ（三维向量 a, 三维向量 b））
- `long SignedTriangleAreaTimes2XZ(Int3 a, Int3 b, Int3 c)`
  （long SignedTriangleAreaTimes2XZ（Int3 a, Int3 b, Int3 c））
- `float SignedTriangleAreaTimes2XZ(Vector3 a, Vector3 b, Vector3 c)`
  （float SignedTriangleAreaTimes2XZ（三维向量 a, 三维向量 b, 三维向量 c））
- `bool RightXZ(Vector3 a, Vector3 b, Vector3 p)`
  （bool 右XZ（三维向量 a, 三维向量 b, 三维向量 p））
- `bool RightXZ(Int3 a, Int3 b, Int3 p)`
  （bool 右XZ（Int3 a, Int3 b, Int3 p））
- `Side SideXZ(Int3 a, Int3 b, Int3 p)`
  （侧面 侧面XZ（Int3 a, Int3 b, Int3 p））
- `bool RightOrColinear(Vector2 a, Vector2 b, Vector2 p)`
  （bool 右OrColinear（二维向量 a, 二维向量 b, 二维向量 p））
- `bool RightOrColinear(Int2 a, Int2 b, Int2 p)`
  （bool 右OrColinear（Int2 a, Int2 b, Int2 p））
- `bool RightOrColinearXZ(Vector3 a, Vector3 b, Vector3 p)`
  （bool 右OrColinearXZ（三维向量 a, 三维向量 b, 三维向量 p））
- `bool RightOrColinearXZ(Int3 a, Int3 b, Int3 p)`
  （bool 右OrColinearXZ（Int3 a, Int3 b, Int3 p））
- `bool IsClockwiseMarginXZ(Vector3 a, Vector3 b, Vector3 c)`
  （bool 是否ClockwiseMarginXZ（三维向量 a, 三维向量 b, 三维向量 c））
- `bool IsClockwiseXZ(Vector3 a, Vector3 b, Vector3 c)`
  （bool 是否ClockwiseXZ（三维向量 a, 三维向量 b, 三维向量 c））
- `bool IsClockwiseXZ(Int3 a, Int3 b, Int3 c)`
  （bool 是否ClockwiseXZ（Int3 a, Int3 b, Int3 c））
- `bool IsClockwiseOrColinearXZ(Int3 a, Int3 b, Int3 c)`
  （bool 是否ClockwiseOrColinearXZ（Int3 a, Int3 b, Int3 c））
- `bool IsClockwiseOrColinear(Int2 a, Int2 b, Int2 c)`
  （bool 是否ClockwiseOrColinear（Int2 a, Int2 b, Int2 c））
- `bool IsColinear(Vector3 a, Vector3 b, Vector3 c)`
  （bool 是否Colinear（三维向量 a, 三维向量 b, 三维向量 c））
- `bool IsColinear(Vector2 a, Vector2 b, Vector2 c)`
  （bool 是否Colinear（二维向量 a, 二维向量 b, 二维向量 c））
- `bool IsColinearXZ(Int3 a, Int3 b, Int3 c)`
  （bool 是否ColinearXZ（Int3 a, Int3 b, Int3 c））
- `bool IsColinearXZ(Vector3 a, Vector3 b, Vector3 c)`
  （bool 是否ColinearXZ（三维向量 a, 三维向量 b, 三维向量 c））
- `bool IsColinearAlmostXZ(Int3 a, Int3 b, Int3 c)`
  （bool 是否ColinearAlmostXZ（Int3 a, Int3 b, Int3 c））
- `bool SegmentsIntersect(Int2 start1, Int2 end1, Int2 start2, Int2 end2)`
  （bool SegmentsIntersect（Int2 start1, Int2 end1, Int2 start2, Int2 end2））
- `bool SegmentsIntersectXZ(Int3 start1, Int3 end1, Int3 start2, Int3 end2)`
  （bool SegmentsIntersectXZ（Int3 start1, Int3 end1, Int3 start2, Int3 end2））
- `bool SegmentsIntersectXZ(Vector3 start1, Vector3 end1, Vector3 start2, Vector3 end2)`
  （bool SegmentsIntersectXZ（三维向量 start1, 三维向量 end1, 三维向量 start2, 三维向量 end2））
- `Vector3 LineDirIntersectionPointXZ(Vector3 start1, Vector3 dir1, Vector3 start2, Vector3 dir2)`
  （三维向量 LineDirIntersectionPointXZ（三维向量 start1, 三维向量 dir1, 三维向量 start2, 三维向量 dir2））
- `Vector3 LineDirIntersectionPointXZ(Vector3 start1, Vector3 dir1, Vector3 start2, Vector3 dir2, out bool intersects)`
  （三维向量 LineDirIntersectionPointXZ（三维向量 start1, 三维向量 dir1, 三维向量 start2, 三维向量 dir2, out bool intersects））
- `bool RaySegmentIntersectXZ(Int3 start1, Int3 end1, Int3 start2, Int3 end2)`
  （bool RaySegmentIntersectXZ（Int3 start1, Int3 end1, Int3 start2, Int3 end2））
- `bool LineIntersectionFactorXZ(Int3 start1, Int3 end1, Int3 start2, Int3 end2, out float factor1, out float factor2)`
  （bool LineIntersection系数XZ（Int3 start1, Int3 end1, Int3 start2, Int3 end2, out float factor1, out float factor2））
- `bool LineIntersectionFactorXZ(Vector3 start1, Vector3 end1, Vector3 start2, Vector3 end2, out float factor1, out float factor2)`
  （bool LineIntersection系数XZ（三维向量 start1, 三维向量 end1, 三维向量 start2, 三维向量 end2, out float factor1, out float factor2））
- `float LineRayIntersectionFactorXZ(Int3 start1, Int3 end1, Int3 start2, Int3 end2)`
  （float LineRayIntersection系数XZ（Int3 start1, Int3 end1, Int3 start2, Int3 end2））
- `float LineIntersectionFactorXZ(Vector3 start1, Vector3 end1, Vector3 start2, Vector3 end2)`
  （float LineIntersection系数XZ（三维向量 start1, 三维向量 end1, 三维向量 start2, 三维向量 end2））
- `Vector3 LineIntersectionPointXZ(Vector3 start1, Vector3 end1, Vector3 start2, Vector3 end2)`
  （三维向量 LineIntersectionPointXZ（三维向量 start1, 三维向量 end1, 三维向量 start2, 三维向量 end2））
- `Vector3 LineIntersectionPointXZ(Vector3 start1, Vector3 end1, Vector3 start2, Vector3 end2, out bool intersects)`
  （三维向量 LineIntersectionPointXZ（三维向量 start1, 三维向量 end1, 三维向量 start2, 三维向量 end2, out bool intersects））
- `Vector2 LineIntersectionPoint(Vector2 start1, Vector2 end1, Vector2 start2, Vector2 end2)`
  （二维向量 LineIntersectionPoint（二维向量 start1, 二维向量 end1, 二维向量 start2, 二维向量 end2））
- `Vector2 LineIntersectionPoint(Vector2 start1, Vector2 end1, Vector2 start2, Vector2 end2, out bool intersects)`
  （二维向量 LineIntersectionPoint（二维向量 start1, 二维向量 end1, 二维向量 start2, 二维向量 end2, out bool intersects））
- `Vector3 SegmentIntersectionPointXZ(Vector3 start1, Vector3 end1, Vector3 start2, Vector3 end2, out bool intersects)`
  （三维向量 SegmentIntersectionPointXZ（三维向量 start1, 三维向量 end1, 三维向量 start2, 三维向量 end2, out bool intersects））
- `bool SegmentIntersectsBounds(Bounds bounds, Vector3 a, Vector3 b)`
  （bool SegmentIntersectsBounds（Bounds bounds, 三维向量 a, 三维向量 b））
- `float LineCircleIntersectionFactor(Vector3 circleCenter, Vector3 linePoint1, Vector3 linePoint2, float radius)`
  （float LineCircleIntersection系数（三维向量 circleCenter, 三维向量 linePoint1, 三维向量 linePoint2, float radius））
- `bool ReversesFaceOrientations(Matrix4x4 matrix)`
  （bool ReversesFaceOrientations（Matrix4x4 matrix））
- `bool ReversesFaceOrientationsXZ(Matrix4x4 matrix)`
  （bool ReversesFaceOrientationsXZ（Matrix4x4 matrix））
- `Vector3 Normalize(Vector3 v, out float magnitude)`
  （三维向量 Normalize（三维向量 v, out float magnitude））
- `Vector2 Normalize(Vector2 v, out float magnitude)`
  （二维向量 Normalize（二维向量 v, out float magnitude））
- `Vector3 ClampMagnitudeXZ(Vector3 v, float maxMagnitude)`
  （三维向量 ClampMagnitudeXZ（三维向量 v, float maxMagnitude））
- `float MagnitudeXZ(Vector3 v)`
  （float MagnitudeXZ（三维向量 v））

---

## VectorOptions（向量Options）

**继承**: IPlugOptions（IPlugOptions）

### 字段 (2)

- `AxisConstraint axisConstraint`（轴Constraint axisConstraint）(偏移: 0x0)
- `bool snapping`（bool snapping）(偏移: 0x4)

### 方法 (1)

- `void Reset()`
  （void 重置（））

---

## Version（Version）

**继承**: ICloneable, IComparable, IComparable<Version>, IEquatable<Version>（ICloneable, IComparable, IComparable<Version>, IEquatable<Version>）

### 字段 (5)

- `int _Major`（int _Major）(偏移: 0x8)
- `int _Minor`（int _Minor）(偏移: 0xC)
- `int _Build`（int _Build）(偏移: 0x10)
- `int _Revision`（int _Revision）(偏移: 0x14)
- `char[] SeparatorsArray`（char[] Separators数组）(偏移: 0x0)

### 方法 (20)

- `int get_Major()`
  （int get_Major（））
- `int get_Minor()`
  （int get_Minor（））
- `int get_Build()`
  （int get_Build（））
- `int get_Revision()`
  （int get_Revision（））
- `object Clone()`
  （object 克隆（））
- `int CompareTo(object version)`
  （int CompareTo（object version））
- `int CompareTo(Version value)`
  （int CompareTo（Version value））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `bool Equals(Version obj)`
  （bool Equals（Version obj））
- `int GetHashCode()`
  （int 获取HashCode（））
- `string ToString()`
  （string To字符串（））
- `string ToString(int fieldCount)`
  （string To字符串（int fieldCount））
- `void AppendPositiveNumber(int num, StringBuilder sb)`
  （void AppendPositiveNumber（int num, 字符串构建器 sb））
- `Version Parse(string input)`
  （Version 解析（string input））
- `bool TryParseVersion(string version, ref Version.VersionResult result)`
  （bool Try解析Version（string version, ref Version.VersionResult result））
- `bool TryParseComponent(string component, string componentName, ref Version.VersionResult result, out int parsedComponent)`
  （bool Try解析组件（string component, string componentName, ref Version.VersionResult result, out int parsedComponent））
- `bool op_Equality(Version v1, Version v2)`
  （bool op_Equality（Version v1, Version v2））
- `bool op_Inequality(Version v1, Version v2)`
  （bool op_Inequality（Version v1, Version v2））
- `bool op_LessThan(Version v1, Version v2)`
  （bool op_LessThan（Version v1, Version v2））
- `bool op_GreaterThan(Version v1, Version v2)`
  （bool op_GreaterThan（Version v1, Version v2））

---

## Version.ParseFailureKind（Version.解析FailureKind）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Version.VersionResult（Version.VersionResult）

### 字段 (5)

- `Version m_parsedVersion`（Version m_parsedVersion）(偏移: 0x0)
- `Version.ParseFailureKind m_failure`（Version.解析FailureKind m_failure）(偏移: 0x4)
- `string m_exceptionArgument`（string m_exceptionArgument）(偏移: 0x8)
- `string m_argumentName`（string m_argument名称）(偏移: 0xC)
- `bool m_canThrow`（bool m_can投掷）(偏移: 0x10)

### 方法 (4)

- `void Init(string argumentName, bool canThrow)`
  （void 初始化（string argumentName, bool canThrow））
- `void SetFailure(Version.ParseFailureKind failure)`
  （void 集合Failure（Version.解析FailureKind failure））
- `void SetFailure(Version.ParseFailureKind failure, string argument)`
  （void 集合Failure（Version.解析FailureKind failure, string argument））
- `Exception GetVersionParseException()`
  （Exception 获取Version解析Exception（））

---

## VersionedMonoBehaviour（VersionedMonoBehaviour）

**继承**: MonoBehaviour, ISerializationCallbackReceiver, IVersionedMonoBehaviourInternal（MonoBehaviour行为, ISerialization回调Receiver, IVersionedMonoBehaviour内部的）

### 字段 (1)

- `int version`（int version）(偏移: 0xC)

### 方法 (3)

- `void Awake()`
  （void Awake（））
- `void Reset()`
  （void 重置（））
- `int OnUpgradeSerializedData(int version, bool unityThread)`
  （int OnUpgradeSerialized数据（int version, bool unityThread））

---

## VertexAttribute（VertexAttribute）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## VertexAttributeDescriptor（VertexAttributeDescriptor）

**继承**: IEquatable<VertexAttributeDescriptor>（IEquatable<VertexAttributeDescriptor>）

### 方法 (12)

- `VertexAttribute get_attribute()`
  （VertexAttribute get_attribute（））
- `void set_attribute(VertexAttribute value)`
  （void set_attribute（VertexAttribute value））
- `VertexAttributeFormat get_format()`
  （VertexAttribute格式化 get_format（））
- `void set_format(VertexAttributeFormat value)`
  （void set_format（VertexAttribute格式化 value））
- `int get_dimension()`
  （int get_dimension（））
- `void set_dimension(int value)`
  （void set_dimension（int value））
- `int get_stream()`
  （int get_stream（））
- `void set_stream(int value)`
  （void set_stream（int value））
- `string ToString()`
  （string To字符串（））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool Equals(object other)`
  （bool Equals（object other））
- `bool Equals(VertexAttributeDescriptor other)`
  （bool Equals（VertexAttributeDescriptor other））

---

## VertexAttributeFormat（VertexAttribute格式化）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## VertexHelper（Vertex辅助器）

**继承**: IDisposable（IDisposable）

### 字段 (12)

- `List<Vector3> m_Positions`（List<Vector3> m_Positions）(偏移: 0x8)
- `List<Color32> m_Colors`（List<Color32> m_Colors）(偏移: 0xC)
- `List<Vector4> m_Uv0S`（List<Vector4> m_Uv0S）(偏移: 0x10)
- `List<Vector4> m_Uv1S`（List<Vector4> m_Uv1S）(偏移: 0x14)
- `List<Vector4> m_Uv2S`（List<Vector4> m_Uv2S）(偏移: 0x18)
- `List<Vector4> m_Uv3S`（List<Vector4> m_Uv3S）(偏移: 0x1C)
- `List<Vector3> m_Normals`（List<Vector3> m_Normals）(偏移: 0x20)
- `List<Vector4> m_Tangents`（List<Vector4> m_Tangents）(偏移: 0x24)
- `List<int> m_Indices`（List<int> m_Indices）(偏移: 0x28)
- `Vector4 s_DefaultTangent`（Vector4 s_默认的Tangent）(偏移: 0x0)
- `Vector3 s_DefaultNormal`（三维向量 s_默认的法线）(偏移: 0x10)
- `bool m_ListsInitalized`（bool m_ListsInitalized）(偏移: 0x2C)

### 方法 (17)

- `void InitializeListIfRequired()`
  （void 初始化列表IfRequired（））
- `void Dispose()`
  （void 释放（））
- `void Clear()`
  （void 清除（））
- `int get_currentVertCount()`
  （int get_currentVert数量（））
- `int get_currentIndexCount()`
  （int get_current索引数量（））
- `void PopulateUIVertex(ref UIVertex vertex, int i)`
  （void Populate界面Vertex（ref UIVertex vertex, int i））
- `void SetUIVertex(UIVertex vertex, int i)`
  （void 集合界面Vertex（界面Vertex vertex, int i））
- `void FillMesh(Mesh mesh)`
  （void Fill网格（网格 mesh））
- `void AddVert(Vector3 position, Color32 color, Vector4 uv0, Vector4 uv1, Vector4 uv2, Vector4 uv3, Vector3 normal, Vector4 tangent)`
  （void 添加Vert（三维向量 position, Color32 color, Vector4 uv0, Vector4 uv1, Vector4 uv2, Vector4 uv3, 三维向量 normal, Vector4 tangent））
- `void AddVert(Vector3 position, Color32 color, Vector4 uv0, Vector4 uv1, Vector3 normal, Vector4 tangent)`
  （void 添加Vert（三维向量 position, Color32 color, Vector4 uv0, Vector4 uv1, 三维向量 normal, Vector4 tangent））
- `void AddVert(Vector3 position, Color32 color, Vector4 uv0)`
  （void 添加Vert（三维向量 position, Color32 color, Vector4 uv0））
- `void AddVert(UIVertex v)`
  （void 添加Vert（界面Vertex v））
- `void AddTriangle(int idx0, int idx1, int idx2)`
  （void 添加Triangle（int idx0, int idx1, int idx2））
- `void AddUIVertexQuad(UIVertex[] verts)`
  （void 添加界面VertexQuad（界面Vertex[] verts））
- `void AddUIVertexStream(List<UIVertex> verts, List<int> indices)`
  （void 添加界面Vertex流（List<UIVertex> verts, List<int> indices））
- `void AddUIVertexTriangleStream(List<UIVertex> verts)`
  （void 添加界面VertexTriangle流（List<UIVertex> verts））
- `void GetUIVertexStream(List<UIVertex> stream)`
  （void 获取界面Vertex流（List<UIVertex> stream））

---

## VerticalLayoutGroup（垂直Layout组）

**继承**: HorizontalOrVerticalLayoutGroup（水平Or垂直Layout组）

### 方法 (4)

- `void CalculateLayoutInputHorizontal()`
  （void 计算Layout输入水平（））
- `void CalculateLayoutInputVertical()`
  （void 计算Layout输入垂直（））
- `void SetLayoutHorizontal()`
  （void 集合Layout水平（））
- `void SetLayoutVertical()`
  （void 集合Layout垂直（））

---

## VerticalWrapMode（垂直Wrap模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Video3DLayout（Video3DLayout）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## VideoAspectRatio（VideoAspect比率）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## VideoAudioOutputMode（Video音频Output模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## VideoCapture（VideoCapture）

**继承**: IDisposable（IDisposable）

### 字段 (2)

- `IntPtr m_NativePtr`（整数Ptr m_NativePtr）(偏移: 0x8)
- `long HR_SUCCESS`（long HR_SUCCESS）(偏移: 0x0)

### 方法 (10)

- `VideoCapture.VideoCaptureResult MakeCaptureResult(long hResult)`
  （VideoCapture.VideoCaptureResult MakeCaptureResult（long hResult））
- `void InvokeOnCreatedVideoCaptureResourceDelegate(VideoCapture.OnVideoCaptureResourceCreatedCallback callback, IntPtr nativePtr)`
  （void InvokeOnCreatedVideoCapture资源委托（VideoCapture.OnVideoCapture资源Created回调 callback, 整数Ptr nativePtr））
- `void InvokeOnVideoModeStartedDelegate(VideoCapture.OnVideoModeStartedCallback callback, long hResult)`
  （void InvokeOnVideo模式Started委托（VideoCapture.OnVideo模式Started回调 callback, long hResult））
- `void InvokeOnVideoModeStoppedDelegate(VideoCapture.OnVideoModeStoppedCallback callback, long hResult)`
  （void InvokeOnVideo模式Stopped委托（VideoCapture.OnVideo模式Stopped回调 callback, long hResult））
- `void InvokeOnStartedRecordingVideoToDiskDelegate(VideoCapture.OnStartedRecordingVideoCallback callback, long hResult)`
  （void InvokeOnStartedRecordingVideoToDisk委托（VideoCapture.OnStartedRecordingVideo回调 callback, long hResult））
- `void InvokeOnStoppedRecordingVideoToDiskDelegate(VideoCapture.OnStoppedRecordingVideoCallback callback, long hResult)`
  （void InvokeOnStoppedRecordingVideoToDisk委托（VideoCapture.OnStoppedRecordingVideo回调 callback, long hResult））
- `void Dispose()`
  （void 释放（））
- `void Dispose_Internal()`
  （void Dispose_内部的（））
- `void Finalize()`
  （void Finalize（））
- `void DisposeThreaded_Internal()`
  （void 释放Threaded_内部的（））

---

## VideoCapture.CaptureResultType（VideoCapture.CaptureResult类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## VideoCapture.OnStartedRecordingVideoCallback（VideoCapture.OnStartedRecordingVideo回调）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(VideoCapture.VideoCaptureResult result)`
  （void Invoke（VideoCapture.VideoCaptureResult result））
- `IAsyncResult BeginInvoke(VideoCapture.VideoCaptureResult result, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（VideoCapture.VideoCaptureResult result, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## VideoCapture.OnStoppedRecordingVideoCallback（VideoCapture.OnStoppedRecordingVideo回调）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(VideoCapture.VideoCaptureResult result)`
  （void Invoke（VideoCapture.VideoCaptureResult result））
- `IAsyncResult BeginInvoke(VideoCapture.VideoCaptureResult result, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（VideoCapture.VideoCaptureResult result, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## VideoCapture.OnVideoCaptureResourceCreatedCallback（VideoCapture.OnVideoCapture资源Created回调）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(VideoCapture captureObject)`
  （void Invoke（VideoCapture captureObject））
- `IAsyncResult BeginInvoke(VideoCapture captureObject, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（VideoCapture captureObject, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## VideoCapture.OnVideoModeStartedCallback（VideoCapture.OnVideo模式Started回调）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(VideoCapture.VideoCaptureResult result)`
  （void Invoke（VideoCapture.VideoCaptureResult result））
- `IAsyncResult BeginInvoke(VideoCapture.VideoCaptureResult result, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（VideoCapture.VideoCaptureResult result, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## VideoCapture.OnVideoModeStoppedCallback（VideoCapture.OnVideo模式Stopped回调）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(VideoCapture.VideoCaptureResult result)`
  （void Invoke（VideoCapture.VideoCaptureResult result））
- `IAsyncResult BeginInvoke(VideoCapture.VideoCaptureResult result, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（VideoCapture.VideoCaptureResult result, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## VideoCapture.VideoCaptureResult（VideoCapture.VideoCaptureResult）

### 字段 (2)

- `VideoCapture.CaptureResultType resultType`（VideoCapture.CaptureResult类型 result类型）(偏移: 0x0)
- `long hResult`（long hResult）(偏移: 0x8)

---

## VideoClipPlayable（Video弹匣Playable）

**继承**: IPlayable, IEquatable<VideoClipPlayable>（IPlayable, IEquatable<Video弹匣Playable>）

### 字段 (1)

- `PlayableHandle m_Handle`（Playable句柄 m_句柄）(偏移: 0x0)

### 方法 (2)

- `PlayableHandle GetHandle()`
  （Playable句柄 获取句柄（））
- `bool Equals(VideoClipPlayable other)`
  （bool Equals（Video弹匣Playable other））

---

