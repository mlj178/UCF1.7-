## 枚举类汇总

共找到 677 个枚举类

---

### public enum BigInteger.Sign

```csharp
public enum BigInteger.Sign 
{
	public int value__; 
	public const BigInteger.Sign Negative = -1;
	public const BigInteger.Sign Zero = 0;
	public const BigInteger.Sign Positive = 1;
}
```

---

### internal enum ConfidenceFactor

```csharp
internal enum ConfidenceFactor 
{
	public int value__; 
	public const ConfidenceFactor ExtraLow = 0;
	public const ConfidenceFactor Low = 1;
	public const ConfidenceFactor Medium = 2;
	public const ConfidenceFactor High = 3;
	public const ConfidenceFactor ExtraHigh = 4;
	public const ConfidenceFactor Provable = 5;
}
```

---

### internal enum UnsafeNativeMethods.ManifestEtw.ActivityControl

```csharp
internal enum UnsafeNativeMethods.ManifestEtw.ActivityControl 
{
	public uint value__; 
	public const UnsafeNativeMethods.ManifestEtw.ActivityControl EVENT_ACTIVITY_CTRL_GET_ID = 1;
	public const UnsafeNativeMethods.ManifestEtw.ActivityControl EVENT_ACTIVITY_CTRL_SET_ID = 2;
	public const UnsafeNativeMethods.ManifestEtw.ActivityControl EVENT_ACTIVITY_CTRL_CREATE_ID = 3;
	public const UnsafeNativeMethods.ManifestEtw.ActivityControl EVENT_ACTIVITY_CTRL_GET_SET_ID = 4;
	public const UnsafeNativeMethods.ManifestEtw.ActivityControl EVENT_ACTIVITY_CTRL_CREATE_SET_ID = 5;
}
```

---

### internal enum UnsafeNativeMethods.ManifestEtw.EVENT_INFO_CLASS

```csharp
internal enum UnsafeNativeMethods.ManifestEtw.EVENT_INFO_CLASS 
{
	public int value__; 
	public const UnsafeNativeMethods.ManifestEtw.EVENT_INFO_CLASS BinaryTrackInfo = 0;
	public const UnsafeNativeMethods.ManifestEtw.EVENT_INFO_CLASS SetEnableAllKeywords = 1;
	public const UnsafeNativeMethods.ManifestEtw.EVENT_INFO_CLASS SetTraits = 2;
}
```

---

### internal enum UnsafeNativeMethods.ManifestEtw.TRACE_QUERY_INFO_CLASS

```csharp
internal enum UnsafeNativeMethods.ManifestEtw.TRACE_QUERY_INFO_CLASS 
{
	public int value__; 
	public const UnsafeNativeMethods.ManifestEtw.TRACE_QUERY_INFO_CLASS TraceGuidQueryList = 0;
	public const UnsafeNativeMethods.ManifestEtw.TRACE_QUERY_INFO_CLASS TraceGuidQueryInfo = 1;
	public const UnsafeNativeMethods.ManifestEtw.TRACE_QUERY_INFO_CLASS TraceGuidQueryProcess = 2;
	public const UnsafeNativeMethods.ManifestEtw.TRACE_QUERY_INFO_CLASS TraceStackTracingInfo = 3;
	public const UnsafeNativeMethods.ManifestEtw.TRACE_QUERY_INFO_CLASS MaxTraceSetInfoClass = 4;
}
```

---

### public enum RegistryHive

```csharp
public enum RegistryHive 
{
	public int value__; 
	public const RegistryHive ClassesRoot = -2147483648;
	public const RegistryHive CurrentConfig = -2147483643;
	public const RegistryHive CurrentUser = -2147483647;
	public const RegistryHive DynData = -2147483642;
	public const RegistryHive LocalMachine = -2147483646;
	public const RegistryHive PerformanceData = -2147483644;
	public const RegistryHive Users = -2147483645;
}
```

---

### public enum RegistryValueKind

```csharp
public enum RegistryValueKind 
{
	public int value__; 
	public const RegistryValueKind Unknown = 0;
	public const RegistryValueKind String = 1;
	public const RegistryValueKind ExpandString = 2;
	public const RegistryValueKind Binary = 3;
	public const RegistryValueKind DWord = 4;
	public const RegistryValueKind MultiString = 7;
	public const RegistryValueKind QWord = 11;
	public const RegistryValueKind None = -1;
}
```

---

### public enum RegistryValueOptions

```csharp
public enum RegistryValueOptions 
{
	public int value__; 
	public const RegistryValueOptions None = 0;
	public const RegistryValueOptions DoNotExpandEnvironmentNames = 1;
}
```

---

### public enum AttributeTargets

```csharp
public enum AttributeTargets 
{
	public int value__; 
	public const AttributeTargets Assembly = 1;
	public const AttributeTargets Module = 2;
	public const AttributeTargets Class = 4;
	public const AttributeTargets Struct = 8;
	public const AttributeTargets Enum = 16;
	public const AttributeTargets Constructor = 32;
	public const AttributeTargets Method = 64;
	public const AttributeTargets Property = 128;
	public const AttributeTargets Field = 256;
	public const AttributeTargets Event = 512;
	public const AttributeTargets Interface = 1024;
	public const AttributeTargets Parameter = 2048;
	public const AttributeTargets Delegate = 4096;
	public const AttributeTargets ReturnValue = 8192;
	public const AttributeTargets GenericParameter = 16384;
	public const AttributeTargets All = 32767;
}
```

---

### public enum ConsoleColor // TypeDefIndex: 157

```csharp
public enum ConsoleColor // TypeDefIndex: 157
{
	// Fields
	public int value__;
	public const ConsoleColor Black = 0;
	public const ConsoleColor DarkBlue = 1;
	public const ConsoleColor DarkGreen = 2;
	public const ConsoleColor DarkCyan = 3;
	public const ConsoleColor DarkRed = 4;
	public const ConsoleColor DarkMagenta = 5;
	public const ConsoleColor DarkYellow = 6;
	public const ConsoleColor Gray = 7;
	public const ConsoleColor DarkGray = 8;
	public const ConsoleColor Blue = 9;
	public const ConsoleColor Green = 10;
	public const ConsoleColor Cyan = 11;
	public const ConsoleColor Red = 12;
	public const ConsoleColor Magenta = 13;
	public const ConsoleColor Yellow = 14;
	public const ConsoleColor White = 15;
}
```

---

### public enum ConsoleKey // TypeDefIndex: 158

```csharp
public enum ConsoleKey // TypeDefIndex: 158
{
	// Fields
	public int value__;
	public const ConsoleKey Backspace = 8;
	public const ConsoleKey Tab = 9;
	public const ConsoleKey Clear = 12;
	public const ConsoleKey Enter = 13;
	public const ConsoleKey Pause = 19;
	public const ConsoleKey Escape = 27;
	public const ConsoleKey Spacebar = 32;
	public const ConsoleKey PageUp = 33;
	public const ConsoleKey PageDown = 34;
	public const ConsoleKey End = 35;
	public const ConsoleKey Home = 36;
	public const ConsoleKey LeftArrow = 37;
	public const ConsoleKey UpArrow = 38;
	public const ConsoleKey RightArrow = 39;
	public const ConsoleKey DownArrow = 40;
	public const ConsoleKey Select = 41;
	public const ConsoleKey Print = 42;
	public const ConsoleKey Execute = 43;
	public const ConsoleKey PrintScreen = 44;
	public const ConsoleKey Insert = 45;
	public const ConsoleKey Delete = 46;
	public const ConsoleKey Help = 47;
	public const ConsoleKey D0 = 48;
	public const ConsoleKey D1 = 49;
	public const ConsoleKey D2 = 50;
	public const ConsoleKey D3 = 51;
	public const ConsoleKey D4 = 52;
	public const ConsoleKey D5 = 53;
	public const ConsoleKey D6 = 54;
	public const ConsoleKey D7 = 55;
	public const ConsoleKey D8 = 56;
	public const ConsoleKey D9 = 57;
	public const ConsoleKey A = 65;
	public const ConsoleKey B = 66;
	public const ConsoleKey C = 67;
	public const ConsoleKey D = 68;
	public const ConsoleKey E = 69;
	public const ConsoleKey F = 70;
	public const ConsoleKey G = 71;
	public const ConsoleKey H = 72;
	public const ConsoleKey I = 73;
	public const ConsoleKey J = 74;
	public const ConsoleKey K = 75;
	public const ConsoleKey L = 76;
	public const ConsoleKey M = 77;
	public const ConsoleKey N = 78;
	public const ConsoleKey O = 79;
	public const ConsoleKey P = 80;
	public const ConsoleKey Q = 81;
	public const ConsoleKey R = 82;
	public const ConsoleKey S = 83;
	public const ConsoleKey T = 84;
	public const ConsoleKey U = 85;
	public const ConsoleKey V = 86;
	public const ConsoleKey W = 87;
	public const ConsoleKey X = 88;
	public const ConsoleKey Y = 89;
	public const ConsoleKey Z = 90;
	public const ConsoleKey LeftWindows = 91;
	public const ConsoleKey RightWindows = 92;
	public const ConsoleKey Applications = 93;
	public const ConsoleKey Sleep = 95;
	public const ConsoleKey NumPad0 = 96;
	public const ConsoleKey NumPad1 = 97;
	public const ConsoleKey NumPad2 = 98;
	public const ConsoleKey NumPad3 = 99;
	public const ConsoleKey NumPad4 = 100;
	public const ConsoleKey NumPad5 = 101;
	public const ConsoleKey NumPad6 = 102;
	public const ConsoleKey NumPad7 = 103;
	public const ConsoleKey NumPad8 = 104;
	public const ConsoleKey NumPad9 = 105;
	public const ConsoleKey Multiply = 106;
	public const ConsoleKey Add = 107;
	public const ConsoleKey Separator = 108;
	public const ConsoleKey Subtract = 109;
	public const ConsoleKey Decimal = 110;
	public const ConsoleKey Divide = 111;
	public const ConsoleKey F1 = 112;
	public const ConsoleKey F2 = 113;
	public const ConsoleKey F3 = 114;
	public const ConsoleKey F4 = 115;
	public const ConsoleKey F5 = 116;
	public const ConsoleKey F6 = 117;
	public const ConsoleKey F7 = 118;
	public const ConsoleKey F8 = 119;
	public const ConsoleKey F9 = 120;
	public const ConsoleKey F10 = 121;
	public const ConsoleKey F11 = 122;
	public const ConsoleKey F12 = 123;
	public const ConsoleKey F13 = 124;
{
	public void .ctor(object object, IntPtr method) { }
```

---

### public enum ConsoleModifiers

```csharp
public enum ConsoleModifiers 
{
	public int value__; 
	public const ConsoleModifiers Alt = 1;
	public const ConsoleModifiers Shift = 2;
	public const ConsoleModifiers Control = 4;
}
```

---

### public enum ConsoleSpecialKey

```csharp
public enum ConsoleSpecialKey 
{
	public int value__; 
	public const ConsoleSpecialKey ControlC = 0;
	public const ConsoleSpecialKey ControlBreak = 1;
}
```

---

### public enum Base64FormattingOptions

```csharp
public enum Base64FormattingOptions 
{
	public int value__; 
	public const Base64FormattingOptions None = 0;
	public const Base64FormattingOptions InsertLineBreaks = 1;
}
```

---

### public enum DateTimeKind

```csharp
public enum DateTimeKind 
{
	public int value__; 
	public const DateTimeKind Unspecified = 0;
	public const DateTimeKind Utc = 1;
	public const DateTimeKind Local = 2;
}
```

---

### public enum DayOfWeek

```csharp
public enum DayOfWeek 
{
	public int value__; 
	public const DayOfWeek Sunday = 0;
	public const DayOfWeek Monday = 1;
	public const DayOfWeek Tuesday = 2;
	public const DayOfWeek Wednesday = 3;
	public const DayOfWeek Thursday = 4;
	public const DayOfWeek Friday = 5;
	public const DayOfWeek Saturday = 6;
}
```

---

### internal enum Exception.ExceptionMessageKind

```csharp
internal enum Exception.ExceptionMessageKind 
{
	public int value__; 
	public const Exception.ExceptionMessageKind ThreadAbort = 1;
	public const Exception.ExceptionMessageKind ThreadInterrupted = 2;
	public const Exception.ExceptionMessageKind OutOfMemory = 3;
}
```

---

### internal enum DateTimeParse.DTT

```csharp
internal enum DateTimeParse.DTT 
{
	public int value__; 
	public const DateTimeParse.DTT End = 0;
	public const DateTimeParse.DTT NumEnd = 1;
	public const DateTimeParse.DTT NumAmpm = 2;
	public const DateTimeParse.DTT NumSpace = 3;
	public const DateTimeParse.DTT NumDatesep = 4;
	public const DateTimeParse.DTT NumTimesep = 5;
	public const DateTimeParse.DTT MonthEnd = 6;
	public const DateTimeParse.DTT MonthSpace = 7;
	public const DateTimeParse.DTT MonthDatesep = 8;
	public const DateTimeParse.DTT NumDatesuff = 9;
	public const DateTimeParse.DTT NumTimesuff = 10;
	public const DateTimeParse.DTT DayOfWeek = 11;
	public const DateTimeParse.DTT YearSpace = 12;
	public const DateTimeParse.DTT YearDateSep = 13;
	public const DateTimeParse.DTT YearEnd = 14;
	public const DateTimeParse.DTT TimeZone = 15;
	public const DateTimeParse.DTT Era = 16;
	public const DateTimeParse.DTT NumUTCTimeMark = 17;
	public const DateTimeParse.DTT Unk = 18;
	public const DateTimeParse.DTT NumLocalTimeMark = 19;
	public const DateTimeParse.DTT Max = 20;
}
```

---

### internal enum DateTimeParse.TM

```csharp
internal enum DateTimeParse.TM 
{
	public int value__; 
	public const DateTimeParse.TM NotSet = -1;
	public const DateTimeParse.TM AM = 0;
	public const DateTimeParse.TM PM = 1;
}
```

---

### internal enum DateTimeParse.DS

```csharp
internal enum DateTimeParse.DS 
{
	public int value__; 
	public const DateTimeParse.DS BEGIN = 0;
	public const DateTimeParse.DS N = 1;
	public const DateTimeParse.DS NN = 2;
	public const DateTimeParse.DS D_Nd = 3;
	public const DateTimeParse.DS D_NN = 4;
	public const DateTimeParse.DS D_NNd = 5;
	public const DateTimeParse.DS D_M = 6;
	public const DateTimeParse.DS D_MN = 7;
	public const DateTimeParse.DS D_NM = 8;
	public const DateTimeParse.DS D_MNd = 9;
	public const DateTimeParse.DS D_NDS = 10;
	public const DateTimeParse.DS D_Y = 11;
	public const DateTimeParse.DS D_YN = 12;
	public const DateTimeParse.DS D_YNd = 13;
	public const DateTimeParse.DS D_YM = 14;
	public const DateTimeParse.DS D_YMd = 15;
	public const DateTimeParse.DS D_S = 16;
	public const DateTimeParse.DS T_S = 17;
	public const DateTimeParse.DS T_Nt = 18;
	public const DateTimeParse.DS T_NNt = 19;
	public const DateTimeParse.DS ERROR = 20;
	public const DateTimeParse.DS DX_NN = 21;
	public const DateTimeParse.DS DX_NNN = 22;
	public const DateTimeParse.DS DX_MN = 23;
	public const DateTimeParse.DS DX_NM = 24;
	public const DateTimeParse.DS DX_MNN = 25;
	public const DateTimeParse.DS DX_DS = 26;
	public const DateTimeParse.DS DX_DSN = 27;
	public const DateTimeParse.DS DX_NDS = 28;
	public const DateTimeParse.DS DX_NNDS = 29;
	public const DateTimeParse.DS DX_YNN = 30;
	public const DateTimeParse.DS DX_YMN = 31;
	public const DateTimeParse.DS DX_YN = 32;
	public const DateTimeParse.DS DX_YM = 33;
	public const DateTimeParse.DS TX_N = 34;
	public const DateTimeParse.DS TX_NN = 35;
	public const DateTimeParse.DS TX_NNN = 36;
	public const DateTimeParse.DS TX_TS = 37;
	public const DateTimeParse.DS DX_NNY = 38;
}
```

---

### internal enum DTSubStringType

```csharp
internal enum DTSubStringType 
{
	public int value__; 
	public const DTSubStringType Unknown = 0;
	public const DTSubStringType Invalid = 1;
	public const DTSubStringType Number = 2;
	public const DTSubStringType End = 3;
	public const DTSubStringType Other = 4;
}
```

---

### internal enum ParseFailureKind

```csharp
internal enum ParseFailureKind 
{
	public int value__; 
	public const ParseFailureKind None = 0;
	public const ParseFailureKind ArgumentNull = 1;
	public const ParseFailureKind Format = 2;
	public const ParseFailureKind FormatWithParameter = 3;
	public const ParseFailureKind FormatBadDateTimeCalendar = 4;
}
```

---

### internal enum ParseFlags

```csharp
internal enum ParseFlags 
{
	public int value__; 
	public const ParseFlags HaveYear = 1;
	public const ParseFlags HaveMonth = 2;
	public const ParseFlags HaveDay = 4;
	public const ParseFlags HaveHour = 8;
	public const ParseFlags HaveMinute = 16;
	public const ParseFlags HaveSecond = 32;
	public const ParseFlags HaveTime = 64;
	public const ParseFlags HaveDate = 128;
	public const ParseFlags TimeZoneUsed = 256;
	public const ParseFlags TimeZoneUtc = 512;
	public const ParseFlags ParsedMonthName = 1024;
	public const ParseFlags CaptureOffset = 2048;
	public const ParseFlags YearDefault = 4096;
	public const ParseFlags Rfc1123Pattern = 8192;
	public const ParseFlags UtcSortPattern = 16384;
}
```

---

### internal enum TokenType

```csharp
internal enum TokenType 
{
	public int value__; 
	public const TokenType NumberToken = 1;
	public const TokenType YearNumberToken = 2;
	public const TokenType Am = 3;
	public const TokenType Pm = 4;
	public const TokenType MonthToken = 5;
	public const TokenType EndOfString = 6;
	public const TokenType DayOfWeekToken = 7;
	public const TokenType TimeZoneToken = 8;
	public const TokenType EraToken = 9;
	public const TokenType DateWordToken = 10;
	public const TokenType UnknownToken = 11;
	public const TokenType HebrewNumber = 12;
	public const TokenType JapaneseEraToken = 13;
	public const TokenType TEraToken = 14;
	public const TokenType IgnorableSymbol = 15;
	public const TokenType SEP_Unk = 256;
	public const TokenType SEP_End = 512;
	public const TokenType SEP_Space = 768;
	public const TokenType SEP_Am = 1024;
	public const TokenType SEP_Pm = 1280;
	public const TokenType SEP_Date = 1536;
	public const TokenType SEP_Time = 1792;
	public const TokenType SEP_YearSuff = 2048;
	public const TokenType SEP_MonthSuff = 2304;
	public const TokenType SEP_DaySuff = 2560;
	public const TokenType SEP_HourSuff = 2816;
	public const TokenType SEP_MinuteSuff = 3072;
	public const TokenType SEP_SecondSuff = 3328;
	public const TokenType SEP_LocalTimeMark = 3584;
	public const TokenType SEP_DateOrOffset = 3840;
	public const TokenType RegularTokenMask = 255;
	public const TokenType SeparatorTokenMask = 65280;
}
```

---

### internal enum TypeNameFormatFlags

```csharp
internal enum TypeNameFormatFlags 
{
	public int value__; 
	public const TypeNameFormatFlags FormatBasic = 0;
	public const TypeNameFormatFlags FormatNamespace = 1;
	public const TypeNameFormatFlags FormatFullInst = 2;
	public const TypeNameFormatFlags FormatAssembly = 4;
	public const TypeNameFormatFlags FormatSignature = 8;
	public const TypeNameFormatFlags FormatNoVersion = 16;
	public const TypeNameFormatFlags FormatAngleBrackets = 64;
	public const TypeNameFormatFlags FormatStubInfo = 128;
	public const TypeNameFormatFlags FormatGenericParam = 256;
	public const TypeNameFormatFlags FormatSerialization = 259;
}
```

---

### internal enum TypeNameKind

```csharp
internal enum TypeNameKind 
{
	public int value__; 
	public const TypeNameKind Name = 0;
	public const TypeNameKind ToString = 1;
	public const TypeNameKind SerializationName = 2;
	public const TypeNameKind FullName = 3;
}
```

---

### internal enum RuntimeType.MemberListType

```csharp
internal enum RuntimeType.MemberListType 
{
	public int value__; 
	public const RuntimeType.MemberListType All = 0;
	public const RuntimeType.MemberListType CaseSensitive = 1;
	public const RuntimeType.MemberListType CaseInsensitive = 2;
	public const RuntimeType.MemberListType HandleToInfo = 3;
}
```

---

### public enum StringSplitOptions

```csharp
public enum StringSplitOptions 
{
	public int value__; 
	public const StringSplitOptions None = 0;
	public const StringSplitOptions RemoveEmptyEntries = 1;
}
```

---

### internal enum ExceptionArgument

```csharp
internal enum ExceptionArgument 
{
	public int value__; 
	public const ExceptionArgument obj = 0;
	public const ExceptionArgument dictionary = 1;
	public const ExceptionArgument dictionaryCreationThreshold = 2;
	public const ExceptionArgument array = 3;
	public const ExceptionArgument info = 4;
	public const ExceptionArgument key = 5;
	public const ExceptionArgument collection = 6;
	public const ExceptionArgument list = 7;
	public const ExceptionArgument match = 8;
	public const ExceptionArgument converter = 9;
	public const ExceptionArgument queue = 10;
	public const ExceptionArgument stack = 11;
	public const ExceptionArgument capacity = 12;
	public const ExceptionArgument index = 13;
	public const ExceptionArgument startIndex = 14;
	public const ExceptionArgument value = 15;
	public const ExceptionArgument count = 16;
	public const ExceptionArgument arrayIndex = 17;
	public const ExceptionArgument name = 18;
	public const ExceptionArgument mode = 19;
	public const ExceptionArgument item = 20;
	public const ExceptionArgument options = 21;
	public const ExceptionArgument view = 22;
	public const ExceptionArgument sourceBytesToCopy = 23;
	public const ExceptionArgument start = 24;
	public const ExceptionArgument pointer = 25;
	public const ExceptionArgument ownedMemory = 26;
	public const ExceptionArgument text = 27;
}
```

---

### internal enum ExceptionResource

```csharp
internal enum ExceptionResource 
{
	public int value__; 
	public const ExceptionResource Argument_ImplementIComparable = 0;
	public const ExceptionResource Argument_InvalidType = 1;
	public const ExceptionResource Argument_InvalidArgumentForComparison = 2;
	public const ExceptionResource Argument_InvalidRegistryKeyPermissionCheck = 3;
	public const ExceptionResource ArgumentOutOfRange_NeedNonNegNum = 4;
	public const ExceptionResource Arg_ArrayPlusOffTooSmall = 5;
	public const ExceptionResource Arg_NonZeroLowerBound = 6;
	public const ExceptionResource Arg_RankMultiDimNotSupported = 7;
	public const ExceptionResource Arg_RegKeyDelHive = 8;
	public const ExceptionResource Arg_RegKeyStrLenBug = 9;
	public const ExceptionResource Arg_RegSetStrArrNull = 10;
	public const ExceptionResource Arg_RegSetMismatchedKind = 11;
	public const ExceptionResource Arg_RegSubKeyAbsent = 12;
	public const ExceptionResource Arg_RegSubKeyValueAbsent = 13;
	public const ExceptionResource Argument_AddingDuplicate = 14;
	public const ExceptionResource Serialization_InvalidOnDeser = 15;
	public const ExceptionResource Serialization_MissingKeys = 16;
	public const ExceptionResource Serialization_NullKey = 17;
	public const ExceptionResource Argument_InvalidArrayType = 18;
	public const ExceptionResource NotSupported_KeyCollectionSet = 19;
	public const ExceptionResource NotSupported_ValueCollectionSet = 20;
	public const ExceptionResource ArgumentOutOfRange_SmallCapacity = 21;
	public const ExceptionResource ArgumentOutOfRange_Index = 22;
	public const ExceptionResource Argument_InvalidOffLen = 23;
	public const ExceptionResource Argument_ItemNotExist = 24;
	public const ExceptionResource ArgumentOutOfRange_Count = 25;
	public const ExceptionResource ArgumentOutOfRange_InvalidThreshold = 26;
	public const ExceptionResource ArgumentOutOfRange_ListInsert = 27;
	public const ExceptionResource NotSupported_ReadOnlyCollection = 28;
	public const ExceptionResource InvalidOperation_CannotRemoveFromStackOrQueue = 29;
	public const ExceptionResource InvalidOperation_EmptyQueue = 30;
	public const ExceptionResource InvalidOperation_EnumOpCantHappen = 31;
	public const ExceptionResource InvalidOperation_EnumFailedVersion = 32;
	public const ExceptionResource InvalidOperation_EmptyStack = 33;
	public const ExceptionResource ArgumentOutOfRange_BiggerThanCollection = 34;
	public const ExceptionResource InvalidOperation_EnumNotStarted = 35;
	public const ExceptionResource InvalidOperation_EnumEnded = 36;
	public const ExceptionResource NotSupported_SortedListNestedWrite = 37;
	public const ExceptionResource InvalidOperation_NoValue = 38;
	public const ExceptionResource InvalidOperation_RegRemoveSubKey = 39;
	public const ExceptionResource Security_RegistryPermission = 40;
	public const ExceptionResource UnauthorizedAccess_RegistryNoWrite = 41;
	public const ExceptionResource ObjectDisposed_RegKeyClosed = 42;
	public const ExceptionResource NotSupported_InComparableType = 43;
	public const ExceptionResource Argument_InvalidRegistryOptionsCheck = 44;
	public const ExceptionResource Argument_InvalidRegistryViewCheck = 45;
}
```

---

### internal enum TimeZoneInfoOptions

```csharp
internal enum TimeZoneInfoOptions 
{
	public int value__; 
	public const TimeZoneInfoOptions None = 1;
	public const TimeZoneInfoOptions NoThrowOnInvalidTime = 2;
}
```

---

### internal enum Version.ParseFailureKind

```csharp
internal enum Version.ParseFailureKind 
{
	public int value__; 
	public const Version.ParseFailureKind ArgumentNullException = 0;
	public const Version.ParseFailureKind ArgumentException = 1;
	public const Version.ParseFailureKind ArgumentOutOfRangeException = 2;
	public const Version.ParseFailureKind FormatException = 3;
}
```

---

### public enum Environment.SpecialFolder

```csharp
public enum Environment.SpecialFolder 
{
	public int value__; 
	public const Environment.SpecialFolder MyDocuments = 5;
	public const Environment.SpecialFolder Desktop = 0;
	public const Environment.SpecialFolder MyComputer = 17;
	public const Environment.SpecialFolder Programs = 2;
	public const Environment.SpecialFolder Personal = 5;
	public const Environment.SpecialFolder Favorites = 6;
	public const Environment.SpecialFolder Startup = 7;
	public const Environment.SpecialFolder Recent = 8;
	public const Environment.SpecialFolder SendTo = 9;
	public const Environment.SpecialFolder StartMenu = 11;
	public const Environment.SpecialFolder MyMusic = 13;
	public const Environment.SpecialFolder DesktopDirectory = 16;
	public const Environment.SpecialFolder Templates = 21;
	public const Environment.SpecialFolder ApplicationData = 26;
	public const Environment.SpecialFolder LocalApplicationData = 28;
	public const Environment.SpecialFolder InternetCache = 32;
	public const Environment.SpecialFolder Cookies = 33;
	public const Environment.SpecialFolder History = 34;
	public const Environment.SpecialFolder CommonApplicationData = 35;
	public const Environment.SpecialFolder System = 37;
	public const Environment.SpecialFolder ProgramFiles = 38;
	public const Environment.SpecialFolder MyPictures = 39;
	public const Environment.SpecialFolder CommonProgramFiles = 43;
	public const Environment.SpecialFolder MyVideos = 14;
	public const Environment.SpecialFolder NetworkShortcuts = 19;
	public const Environment.SpecialFolder Fonts = 20;
	public const Environment.SpecialFolder CommonStartMenu = 22;
	public const Environment.SpecialFolder CommonPrograms = 23;
	public const Environment.SpecialFolder CommonStartup = 24;
	public const Environment.SpecialFolder CommonDesktopDirectory = 25;
	public const Environment.SpecialFolder PrinterShortcuts = 27;
	public const Environment.SpecialFolder Windows = 36;
	public const Environment.SpecialFolder UserProfile = 40;
	public const Environment.SpecialFolder SystemX86 = 41;
	public const Environment.SpecialFolder ProgramFilesX86 = 42;
	public const Environment.SpecialFolder CommonProgramFilesX86 = 44;
	public const Environment.SpecialFolder CommonTemplates = 45;
	public const Environment.SpecialFolder CommonDocuments = 46;
	public const Environment.SpecialFolder CommonAdminTools = 47;
	public const Environment.SpecialFolder AdminTools = 48;
	public const Environment.SpecialFolder CommonMusic = 53;
	public const Environment.SpecialFolder CommonPictures = 54;
	public const Environment.SpecialFolder CommonVideos = 55;
	public const Environment.SpecialFolder Resources = 56;
	public const Environment.SpecialFolder LocalizedResources = 57;
	public const Environment.SpecialFolder CommonOemLinks = 58;
	public const Environment.SpecialFolder CDBurning = 59;
}
```

---

### public enum Environment.SpecialFolderOption

```csharp
public enum Environment.SpecialFolderOption 
{
	public int value__; 
	public const Environment.SpecialFolderOption None = 0;
	public const Environment.SpecialFolderOption DoNotVerify = 16384;
	public const Environment.SpecialFolderOption Create = 32768;
}
```

---

### internal enum SByteEnum

```csharp
internal enum SByteEnum 
{
	public sbyte value__; 
}
```

---

### internal enum Int16Enum

```csharp
internal enum Int16Enum 
{
	public short value__; 
}
```

---

### internal enum Int32Enum

```csharp
internal enum Int32Enum 
{
	public int value__; 
}
```

---

### internal enum Int64Enum

```csharp
internal enum Int64Enum 
{
	public long value__; 
}
```

---

### internal enum ByteEnum

```csharp
internal enum ByteEnum 
{
	public byte value__; 
}
```

---

### internal enum UInt16Enum

```csharp
internal enum UInt16Enum 
{
	public ushort value__; 
}
```

---

### internal enum UInt32Enum

```csharp
internal enum UInt32Enum 
{
	public uint value__; 
}
```

---

### internal enum UInt64Enum

```csharp
internal enum UInt64Enum 
{
	public ulong value__; 
}
```

---

### public enum PlatformID

```csharp
public enum PlatformID 
{
	public int value__; 
	public const PlatformID Win32S = 0;
	public const PlatformID Win32Windows = 1;
	public const PlatformID Win32NT = 2;
	public const PlatformID WinCE = 3;
	public const PlatformID Unix = 4;
	public const PlatformID Xbox = 5;
	public const PlatformID MacOSX = 6;
}
```

---

### public enum StringComparison

```csharp
public enum StringComparison 
{
	public int value__; 
	public const StringComparison CurrentCulture = 0;
	public const StringComparison CurrentCultureIgnoreCase = 1;
	public const StringComparison InvariantCulture = 2;
	public const StringComparison InvariantCultureIgnoreCase = 3;
	public const StringComparison Ordinal = 4;
	public const StringComparison OrdinalIgnoreCase = 5;
}
```

---

### internal enum TermInfoNumbers

```csharp
internal enum TermInfoNumbers 
{
	public int value__; 
	public const TermInfoNumbers Columns = 0;
	public const TermInfoNumbers InitTabs = 1;
	public const TermInfoNumbers Lines = 2;
	public const TermInfoNumbers LinesOfMemory = 3;
	public const TermInfoNumbers MagicCookieGlitch = 4;
	public const TermInfoNumbers PaddingBaudRate = 5;
	public const TermInfoNumbers VirtualTerminal = 6;
	public const TermInfoNumbers WidthStatusLine = 7;
	public const TermInfoNumbers NumLabels = 8;
	public const TermInfoNumbers LabelHeight = 9;
	public const TermInfoNumbers LabelWidth = 10;
	public const TermInfoNumbers MaxAttributes = 11;
	public const TermInfoNumbers MaximumWindows = 12;
	public const TermInfoNumbers MaxColors = 13;
	public const TermInfoNumbers MaxPairs = 14;
	public const TermInfoNumbers NoColorVideo = 15;
	public const TermInfoNumbers BufferCapacity = 16;
	public const TermInfoNumbers DotVertSpacing = 17;
	public const TermInfoNumbers DotHorzSpacing = 18;
	public const TermInfoNumbers MaxMicroAddress = 19;
	public const TermInfoNumbers MaxMicroJump = 20;
	public const TermInfoNumbers MicroColSize = 21;
	public const TermInfoNumbers MicroLineSize = 22;
	public const TermInfoNumbers NumberOfPins = 23;
	public const TermInfoNumbers OutputResChar = 24;
	public const TermInfoNumbers OutputResLine = 25;
	public const TermInfoNumbers OutputResHorzInch = 26;
	public const TermInfoNumbers OutputResVertInch = 27;
	public const TermInfoNumbers PrintRate = 28;
	public const TermInfoNumbers WideCharSize = 29;
	public const TermInfoNumbers Buttons = 30;
	public const TermInfoNumbers BitImageEntwining = 31;
	public const TermInfoNumbers BitImageType = 32;
	public const TermInfoNumbers Last = 33;
}
```

---

### internal enum TermInfoStrings

```csharp
internal enum TermInfoStrings 
{
	public int value__; 
	public const TermInfoStrings BackTab = 0;
	public const TermInfoStrings Bell = 1;
	public const TermInfoStrings CarriageReturn = 2;
	public const TermInfoStrings ChangeScrollRegion = 3;
	public const TermInfoStrings ClearAllTabs = 4;
	public const TermInfoStrings ClearScreen = 5;
	public const TermInfoStrings ClrEol = 6;
	public const TermInfoStrings ClrEos = 7;
	public const TermInfoStrings ColumnAddress = 8;
	public const TermInfoStrings CommandCharacter = 9;
	public const TermInfoStrings CursorAddress = 10;
	public const TermInfoStrings CursorDown = 11;
	public const TermInfoStrings CursorHome = 12;
	public const TermInfoStrings CursorInvisible = 13;
	public const TermInfoStrings CursorLeft = 14;
	public const TermInfoStrings CursorMemAddress = 15;
	public const TermInfoStrings CursorNormal = 16;
	public const TermInfoStrings CursorRight = 17;
	public const TermInfoStrings CursorToLl = 18;
	public const TermInfoStrings CursorUp = 19;
	public const TermInfoStrings CursorVisible = 20;
	public const TermInfoStrings DeleteCharacter = 21;
	public const TermInfoStrings DeleteLine = 22;
	public const TermInfoStrings DisStatusLine = 23;
	public const TermInfoStrings DownHalfLine = 24;
	public const TermInfoStrings EnterAltCharsetMode = 25;
	public const TermInfoStrings EnterBlinkMode = 26;
	public const TermInfoStrings EnterBoldMode = 27;
	public const TermInfoStrings EnterCaMode = 28;
	public const TermInfoStrings EnterDeleteMode = 29;
	public const TermInfoStrings EnterDimMode = 30;
	public const TermInfoStrings EnterInsertMode = 31;
	public const TermInfoStrings EnterSecureMode = 32;
	public const TermInfoStrings EnterProtectedMode = 33;
	public const TermInfoStrings EnterReverseMode = 34;
	public const TermInfoStrings EnterStandoutMode = 35;
	public const TermInfoStrings EnterUnderlineMode = 36;
	public const TermInfoStrings EraseChars = 37;
	public const TermInfoStrings ExitAltCharsetMode = 38;
	public const TermInfoStrings ExitAttributeMode = 39;
	public const TermInfoStrings ExitCaMode = 40;
	public const TermInfoStrings ExitDeleteMode = 41;
	public const TermInfoStrings ExitInsertMode = 42;
	public const TermInfoStrings ExitStandoutMode = 43;
	public const TermInfoStrings ExitUnderlineMode = 44;
	public const TermInfoStrings FlashScreen = 45;
	public const TermInfoStrings FormFeed = 46;
	public const TermInfoStrings FromStatusLine = 47;
	public const TermInfoStrings Init1string = 48;
	public const TermInfoStrings Init2string = 49;
	public const TermInfoStrings Init3string = 50;
	public const TermInfoStrings InitFile = 51;
	public const TermInfoStrings InsertCharacter = 52;
	public const TermInfoStrings InsertLine = 53;
	public const TermInfoStrings InsertPadding = 54;
	public const TermInfoStrings KeyBackspace = 55;
	public const TermInfoStrings KeyCatab = 56;
	public const TermInfoStrings KeyClear = 57;
	public const TermInfoStrings KeyCtab = 58;
	public const TermInfoStrings KeyDc = 59;
	public const TermInfoStrings KeyDl = 60;
	public const TermInfoStrings KeyDown = 61;
	public const TermInfoStrings KeyEic = 62;
	public const TermInfoStrings KeyEol = 63;
	public const TermInfoStrings KeyEos = 64;
	public const TermInfoStrings KeyF0 = 65;
	public const TermInfoStrings KeyF1 = 66;
	public const TermInfoStrings KeyF10 = 67;
	public const TermInfoStrings KeyF2 = 68;
	public const TermInfoStrings KeyF3 = 69;
	public const TermInfoStrings KeyF4 = 70;
	public const TermInfoStrings KeyF5 = 71;
	public const TermInfoStrings KeyF6 = 72;
	public const TermInfoStrings KeyF7 = 73;
	public const TermInfoStrings KeyF8 = 74;
	public const TermInfoStrings KeyF9 = 75;
	public const TermInfoStrings KeyHome = 76;
	public const TermInfoStrings KeyIc = 77;
	public const TermInfoStrings KeyIl = 78;
	public const TermInfoStrings KeyLeft = 79;
	public const TermInfoStrings KeyLl = 80;
	public const TermInfoStrings KeyNpage = 81;
	public const TermInfoStrings KeyPpage = 82;
	public const TermInfoStrings KeyRight = 83;
	public const TermInfoStrings KeySf = 84;
	public const TermInfoStrings KeySr = 85;
	public const TermInfoStrings KeyStab = 86;
	public const TermInfoStrings KeyUp = 87;
	public const TermInfoStrings KeypadLocal = 88;
	public const TermInfoStrings KeypadXmit = 89;
	public const TermInfoStrings LabF0 = 90;
	public const TermInfoStrings LabF1 = 91;
	public const TermInfoStrings LabF10 = 92;
	public const TermInfoStrings LabF2 = 93;
	public const TermInfoStrings LabF3 = 94;
	public const TermInfoStrings LabF4 = 95;
	public const TermInfoStrings LabF5 = 96;
	public const TermInfoStrings LabF6 = 97;
	public const TermInfoStrings LabF7 = 98;
	public const TermInfoStrings LabF8 = 99;
	public const TermInfoStrings LabF9 = 100;
	public const TermInfoStrings MetaOff = 101;
	public const TermInfoStrings MetaOn = 102;
	public const TermInfoStrings Newline = 103;
	public const TermInfoStrings PadChar = 104;
	public const TermInfoStrings ParmDch = 105;
	public const TermInfoStrings ParmDeleteLine = 106;
	public const TermInfoStrings ParmDownCursor = 107;
	public const TermInfoStrings ParmIch = 108;
	public const TermInfoStrings ParmIndex = 109;
	public const TermInfoStrings ParmInsertLine = 110;
	public const TermInfoStrings ParmLeftCursor = 111;
	public const TermInfoStrings ParmRightCursor = 112;
	public const TermInfoStrings ParmRindex = 113;
	public const TermInfoStrings ParmUpCursor = 114;
	public const TermInfoStrings PkeyKey = 115;
	public const TermInfoStrings PkeyLocal = 116;
	public const TermInfoStrings PkeyXmit = 117;
	public const TermInfoStrings PrintScreen = 118;
	public const TermInfoStrings PrtrOff = 119;
	public const TermInfoStrings PrtrOn = 120;
	public const TermInfoStrings RepeatChar = 121;
	public const TermInfoStrings Reset1string = 122;
	public const TermInfoStrings Reset2string = 123;
	public const TermInfoStrings Reset3string = 124;
	public const TermInfoStrings ResetFile = 125;
	public const TermInfoStrings RestoreCursor = 126;
	public const TermInfoStrings RowAddress = 127;
	public const TermInfoStrings SaveCursor = 128;
	public const TermInfoStrings ScrollForward = 129;
	public const TermInfoStrings ScrollReverse = 130;
	public const TermInfoStrings SetAttributes = 131;
	public const TermInfoStrings SetTab = 132;
	public const TermInfoStrings SetWindow = 133;
	public const TermInfoStrings Tab = 134;
	public const TermInfoStrings ToStatusLine = 135;
	public const TermInfoStrings UnderlineChar = 136;
	public const TermInfoStrings UpHalfLine = 137;
	public const TermInfoStrings InitProg = 138;
	public const TermInfoStrings KeyA1 = 139;
	public const TermInfoStrings KeyA3 = 140;
	public const TermInfoStrings KeyB2 = 141;
	public const TermInfoStrings KeyC1 = 142;
	public const TermInfoStrings KeyC3 = 143;
	public const TermInfoStrings PrtrNon = 144;
	public const TermInfoStrings CharPadding = 145;
	public const TermInfoStrings AcsChars = 146;
	public const TermInfoStrings PlabNorm = 147;
	public const TermInfoStrings KeyBtab = 148;
	public const TermInfoStrings EnterXonMode = 149;
	public const TermInfoStrings ExitXonMode = 150;
	public const TermInfoStrings EnterAmMode = 151;
	public const TermInfoStrings ExitAmMode = 152;
	public const TermInfoStrings XonCharacter = 153;
	public const TermInfoStrings XoffCharacter = 154;
	public const TermInfoStrings EnaAcs = 155;
	public const TermInfoStrings LabelOn = 156;
	public const TermInfoStrings LabelOff = 157;
	public const TermInfoStrings KeyBeg = 158;
	public const TermInfoStrings KeyCancel = 159;
	public const TermInfoStrings KeyClose = 160;
	public const TermInfoStrings KeyCommand = 161;
	public const TermInfoStrings KeyCopy = 162;
	public const TermInfoStrings KeyCreate = 163;
	public const TermInfoStrings KeyEnd = 164;
	public const TermInfoStrings KeyEnter = 165;
	public const TermInfoStrings KeyExit = 166;
	public const TermInfoStrings KeyFind = 167;
	public const TermInfoStrings KeyHelp = 168;
	public const TermInfoStrings KeyMark = 169;
	public const TermInfoStrings KeyMessage = 170;
	public const TermInfoStrings KeyMove = 171;
	public const TermInfoStrings KeyNext = 172;
	public const TermInfoStrings KeyOpen = 173;
	public const TermInfoStrings KeyOptions = 174;
	public const TermInfoStrings KeyPrevious = 175;
	public const TermInfoStrings KeyPrint = 176;
	public const TermInfoStrings KeyRedo = 177;
	public const TermInfoStrings KeyReference = 178;
	public const TermInfoStrings KeyRefresh = 179;
	public const TermInfoStrings KeyReplace = 180;
	public const TermInfoStrings KeyRestart = 181;
	public const TermInfoStrings KeyResume = 182;
	public const TermInfoStrings KeySave = 183;
	public const TermInfoStrings KeySuspend = 184;
	public const TermInfoStrings KeyUndo = 185;
	public const TermInfoStrings KeySbeg = 186;
	public const TermInfoStrings KeyScancel = 187;
	public const TermInfoStrings KeyScommand = 188;
	public const TermInfoStrings KeyScopy = 189;
	public const TermInfoStrings KeyScreate = 190;
	public const TermInfoStrings KeySdc = 191;
	public const TermInfoStrings KeySdl = 192;
	public const TermInfoStrings KeySelect = 193;
	public const TermInfoStrings KeySend = 194;
	public const TermInfoStrings KeySeol = 195;
	public const TermInfoStrings KeySexit = 196;
	public const TermInfoStrings KeySfind = 197;
	public const TermInfoStrings KeyShelp = 198;
	public const TermInfoStrings KeyShome = 199;
	public const TermInfoStrings KeySic = 200;
	public const TermInfoStrings KeySleft = 201;
	public const TermInfoStrings KeySmessage = 202;
	public const TermInfoStrings KeySmove = 203;
	public const TermInfoStrings KeySnext = 204;
	public const TermInfoStrings KeySoptions = 205;
	public const TermInfoStrings KeySprevious = 206;
	public const TermInfoStrings KeySprint = 207;
	public const TermInfoStrings KeySredo = 208;
	public const TermInfoStrings KeySreplace = 209;
	public const TermInfoStrings KeySright = 210;
	public const TermInfoStrings KeySrsume = 211;
	public const TermInfoStrings KeySsave = 212;
	public const TermInfoStrings KeySsuspend = 213;
	public const TermInfoStrings KeySundo = 214;
	public const TermInfoStrings ReqForInput = 215;
	public const TermInfoStrings KeyF11 = 216;
	public const TermInfoStrings KeyF12 = 217;
	public const TermInfoStrings KeyF13 = 218;
	public const TermInfoStrings KeyF14 = 219;
	public const TermInfoStrings KeyF15 = 220;
	public const TermInfoStrings KeyF16 = 221;
	public const TermInfoStrings KeyF17 = 222;
	public const TermInfoStrings KeyF18 = 223;
	public const TermInfoStrings KeyF19 = 224;
	public const TermInfoStrings KeyF20 = 225;
	public const TermInfoStrings KeyF21 = 226;
	public const TermInfoStrings KeyF22 = 227;
	public const TermInfoStrings KeyF23 = 228;
	public const TermInfoStrings KeyF24 = 229;
	public const TermInfoStrings KeyF25 = 230;
	public const TermInfoStrings KeyF26 = 231;
	public const TermInfoStrings KeyF27 = 232;
	public const TermInfoStrings KeyF28 = 233;
	public const TermInfoStrings KeyF29 = 234;
	public const TermInfoStrings KeyF30 = 235;
	public const TermInfoStrings KeyF31 = 236;
	public const TermInfoStrings KeyF32 = 237;
	public const TermInfoStrings KeyF33 = 238;
	public const TermInfoStrings KeyF34 = 239;
	public const TermInfoStrings KeyF35 = 240;
	public const TermInfoStrings KeyF36 = 241;
	public const TermInfoStrings KeyF37 = 242;
	public const TermInfoStrings KeyF38 = 243;
	public const TermInfoStrings KeyF39 = 244;
	public const TermInfoStrings KeyF40 = 245;
	public const TermInfoStrings KeyF41 = 246;
	public const TermInfoStrings KeyF42 = 247;
	public const TermInfoStrings KeyF43 = 248;
	public const TermInfoStrings KeyF44 = 249;
	public const TermInfoStrings KeyF45 = 250;
	public const TermInfoStrings KeyF46 = 251;
	public const TermInfoStrings KeyF47 = 252;
	public const TermInfoStrings KeyF48 = 253;
	public const TermInfoStrings KeyF49 = 254;
	public const TermInfoStrings KeyF50 = 255;
	public const TermInfoStrings KeyF51 = 256;
	public const TermInfoStrings KeyF52 = 257;
	public const TermInfoStrings KeyF53 = 258;
	public const TermInfoStrings KeyF54 = 259;
	public const TermInfoStrings KeyF55 = 260;
	public const TermInfoStrings KeyF56 = 261;
	public const TermInfoStrings KeyF57 = 262;
	public const TermInfoStrings KeyF58 = 263;
	public const TermInfoStrings KeyF59 = 264;
	public const TermInfoStrings KeyF60 = 265;
	public const TermInfoStrings KeyF61 = 266;
	public const TermInfoStrings KeyF62 = 267;
	public const TermInfoStrings KeyF63 = 268;
	public const TermInfoStrings ClrBol = 269;
	public const TermInfoStrings ClearMargins = 270;
	public const TermInfoStrings SetLeftMargin = 271;
	public const TermInfoStrings SetRightMargin = 272;
	public const TermInfoStrings LabelFormat = 273;
	public const TermInfoStrings SetClock = 274;
	public const TermInfoStrings DisplayClock = 275;
	public const TermInfoStrings RemoveClock = 276;
	public const TermInfoStrings CreateWindow = 277;
	public const TermInfoStrings GotoWindow = 278;
	public const TermInfoStrings Hangup = 279;
	public const TermInfoStrings DialPhone = 280;
	public const TermInfoStrings QuickDial = 281;
	public const TermInfoStrings Tone = 282;
	public const TermInfoStrings Pulse = 283;
	public const TermInfoStrings FlashHook = 284;
	public const TermInfoStrings FixedPause = 285;
	public const TermInfoStrings WaitTone = 286;
	public const TermInfoStrings User0 = 287;
	public const TermInfoStrings User1 = 288;
	public const TermInfoStrings User2 = 289;
	public const TermInfoStrings User3 = 290;
	public const TermInfoStrings User4 = 291;
	public const TermInfoStrings User5 = 292;
	public const TermInfoStrings User6 = 293;
	public const TermInfoStrings User7 = 294;
	public const TermInfoStrings User8 = 295;
	public const TermInfoStrings User9 = 296;
	public const TermInfoStrings OrigPair = 297;
	public const TermInfoStrings OrigColors = 298;
	public const TermInfoStrings InitializeColor = 299;
	public const TermInfoStrings InitializePair = 300;
	public const TermInfoStrings SetColorPair = 301;
	public const TermInfoStrings SetForeground = 302;
	public const TermInfoStrings SetBackground = 303;
	public const TermInfoStrings ChangeCharPitch = 304;
	public const TermInfoStrings ChangeLinePitch = 305;
	public const TermInfoStrings ChangeResHorz = 306;
	public const TermInfoStrings ChangeResVert = 307;
	public const TermInfoStrings DefineChar = 308;
	public const TermInfoStrings EnterDoublewideMode = 309;
	public const TermInfoStrings EnterDraftQuality = 310;
	public const TermInfoStrings EnterItalicsMode = 311;
	public const TermInfoStrings EnterLeftwardMode = 312;
	public const TermInfoStrings EnterMicroMode = 313;
	public const TermInfoStrings EnterNearLetterQuality = 314;
	public const TermInfoStrings EnterNormalQuality = 315;
	public const TermInfoStrings EnterShadowMode = 316;
	public const TermInfoStrings EnterSubscriptMode = 317;
	public const TermInfoStrings EnterSuperscriptMode = 318;
	public const TermInfoStrings EnterUpwardMode = 319;
	public const TermInfoStrings ExitDoublewideMode = 320;
	public const TermInfoStrings ExitItalicsMode = 321;
	public const TermInfoStrings ExitLeftwardMode = 322;
	public const TermInfoStrings ExitMicroMode = 323;
	public const TermInfoStrings ExitShadowMode = 324;
	public const TermInfoStrings ExitSubscriptMode = 325;
	public const TermInfoStrings ExitSuperscriptMode = 326;
	public const TermInfoStrings ExitUpwardMode = 327;
	public const TermInfoStrings MicroColumnAddress = 328;
	public const TermInfoStrings MicroDown = 329;
	public const TermInfoStrings MicroLeft = 330;
	public const TermInfoStrings MicroRight = 331;
	public const TermInfoStrings MicroRowAddress = 332;
	public const TermInfoStrings MicroUp = 333;
	public const TermInfoStrings OrderOfPins = 334;
	public const TermInfoStrings ParmDownMicro = 335;
	public const TermInfoStrings ParmLeftMicro = 336;
	public const TermInfoStrings ParmRightMicro = 337;
	public const TermInfoStrings ParmUpMicro = 338;
	public const TermInfoStrings SelectCharSet = 339;
	public const TermInfoStrings SetBottomMargin = 340;
	public const TermInfoStrings SetBottomMarginParm = 341;
	public const TermInfoStrings SetLeftMarginParm = 342;
	public const TermInfoStrings SetRightMarginParm = 343;
	public const TermInfoStrings SetTopMargin = 344;
	public const TermInfoStrings SetTopMarginParm = 345;
	public const TermInfoStrings StartBitImage = 346;
	public const TermInfoStrings StartCharSetDef = 347;
	public const TermInfoStrings StopBitImage = 348;
	public const TermInfoStrings StopCharSetDef = 349;
	public const TermInfoStrings SubscriptCharacters = 350;
	public const TermInfoStrings SuperscriptCharacters = 351;
	public const TermInfoStrings TheseCauseCr = 352;
	public const TermInfoStrings ZeroMotion = 353;
	public const TermInfoStrings CharSetNames = 354;
	public const TermInfoStrings KeyMouse = 355;
	public const TermInfoStrings MouseInfo = 356;
	public const TermInfoStrings ReqMousePos = 357;
	public const TermInfoStrings GetMouse = 358;
	public const TermInfoStrings SetAForeground = 359;
	public const TermInfoStrings SetABackground = 360;
	public const TermInfoStrings PkeyPlab = 361;
	public const TermInfoStrings DeviceType = 362;
	public const TermInfoStrings CodeSetInit = 363;
	public const TermInfoStrings Set0DesSeq = 364;
	public const TermInfoStrings Set1DesSeq = 365;
	public const TermInfoStrings Set2DesSeq = 366;
	public const TermInfoStrings Set3DesSeq = 367;
	public const TermInfoStrings SetLrMargin = 368;
	public const TermInfoStrings SetTbMargin = 369;
	public const TermInfoStrings BitImageRepeat = 370;
	public const TermInfoStrings BitImageNewline = 371;
	public const TermInfoStrings BitImageCarriageReturn = 372;
	public const TermInfoStrings ColorNames = 373;
	public const TermInfoStrings DefineBitImageRegion = 374;
	public const TermInfoStrings EndBitImageRegion = 375;
	public const TermInfoStrings SetColorBand = 376;
	public const TermInfoStrings SetPageLength = 377;
	public const TermInfoStrings DisplayPcChar = 378;
	public const TermInfoStrings EnterPcCharsetMode = 379;
	public const TermInfoStrings ExitPcCharsetMode = 380;
	public const TermInfoStrings EnterScancodeMode = 381;
	public const TermInfoStrings ExitScancodeMode = 382;
	public const TermInfoStrings PcTermOptions = 383;
	public const TermInfoStrings ScancodeEscape = 384;
	public const TermInfoStrings AltScancodeEsc = 385;
	public const TermInfoStrings EnterHorizontalHlMode = 386;
	public const TermInfoStrings EnterLeftHlMode = 387;
	public const TermInfoStrings EnterLowHlMode = 388;
	public const TermInfoStrings EnterRightHlMode = 389;
	public const TermInfoStrings EnterTopHlMode = 390;
	public const TermInfoStrings EnterVerticalHlMode = 391;
	public const TermInfoStrings SetAAttributes = 392;
	public const TermInfoStrings SetPglenInch = 393;
	public const TermInfoStrings Last = 394;
}
```

---

### public enum TypeCode

```csharp
public enum TypeCode 
{
	public int value__; 
	public const TypeCode Empty = 0;
	public const TypeCode Object = 1;
	public const TypeCode DBNull = 2;
	public const TypeCode Boolean = 3;
	public const TypeCode Char = 4;
	public const TypeCode SByte = 5;
	public const TypeCode Byte = 6;
	public const TypeCode Int16 = 7;
	public const TypeCode UInt16 = 8;
	public const TypeCode Int32 = 9;
	public const TypeCode UInt32 = 10;
	public const TypeCode Int64 = 11;
	public const TypeCode UInt64 = 12;
	public const TypeCode Single = 13;
	public const TypeCode Double = 14;
	public const TypeCode Decimal = 15;
	public const TypeCode DateTime = 16;
	public const TypeCode String = 18;
}
```

---

### internal enum TypeSpec.DisplayNameFormat

```csharp
internal enum TypeSpec.DisplayNameFormat 
{
	public int value__; 
	public const TypeSpec.DisplayNameFormat Default = 0;
	public const TypeSpec.DisplayNameFormat WANT_ASSEMBLY = 1;
	public const TypeSpec.DisplayNameFormat NO_MODIFIERS = 2;
}
```

---

### internal enum Handles

```csharp
internal enum Handles 
{
	public int value__; 
	public const Handles STD_INPUT = -10;
	public const Handles STD_OUTPUT = -11;
	public const Handles STD_ERROR = -12;
}
```

---

### public enum AssemblyHashAlgorithm

```csharp
public enum AssemblyHashAlgorithm 
{
	public int value__; 
	public const AssemblyHashAlgorithm None = 0;
	public const AssemblyHashAlgorithm MD5 = 32771;
	public const AssemblyHashAlgorithm SHA1 = 32772;
	public const AssemblyHashAlgorithm SHA256 = 32780;
	public const AssemblyHashAlgorithm SHA384 = 32781;
	public const AssemblyHashAlgorithm SHA512 = 32782;
}
```

---

### public enum AssemblyVersionCompatibility

```csharp
public enum AssemblyVersionCompatibility 
{
	public int value__; 
	public const AssemblyVersionCompatibility SameMachine = 1;
	public const AssemblyVersionCompatibility SameProcess = 2;
	public const AssemblyVersionCompatibility SameDomain = 3;
}
```

---

### internal enum NormalizationCheck

```csharp
internal enum NormalizationCheck 
{
	public int value__; 
	public const NormalizationCheck Yes = 0;
	public const NormalizationCheck No = 1;
	public const NormalizationCheck Maybe = 2;
}
```

---

### public enum NormalizationForm

```csharp
public enum NormalizationForm 
{
	public int value__; 
	public const NormalizationForm FormC = 1;
	public const NormalizationForm FormD = 2;
	public const NormalizationForm FormKC = 5;
	public const NormalizationForm FormKD = 6;
}
```

---

### internal enum ResourceTypeCode

```csharp
internal enum ResourceTypeCode 
{
	public int value__; 
	public const ResourceTypeCode Null = 0;
	public const ResourceTypeCode String = 1;
	public const ResourceTypeCode Boolean = 2;
	public const ResourceTypeCode Char = 3;
	public const ResourceTypeCode Byte = 4;
	public const ResourceTypeCode SByte = 5;
	public const ResourceTypeCode Int16 = 6;
	public const ResourceTypeCode UInt16 = 7;
	public const ResourceTypeCode Int32 = 8;
	public const ResourceTypeCode UInt32 = 9;
	public const ResourceTypeCode Int64 = 10;
	public const ResourceTypeCode UInt64 = 11;
	public const ResourceTypeCode Single = 12;
	public const ResourceTypeCode Double = 13;
	public const ResourceTypeCode Decimal = 14;
	public const ResourceTypeCode DateTime = 15;
	public const ResourceTypeCode TimeSpan = 16;
	public const ResourceTypeCode LastPrimitive = 16;
	public const ResourceTypeCode ByteArray = 32;
	public const ResourceTypeCode Stream = 33;
	public const ResourceTypeCode StartOfUserTypes = 64;
}
```

---

### public enum UltimateResourceFallbackLocation

```csharp
public enum UltimateResourceFallbackLocation 
{
	public int value__; 
	public const UltimateResourceFallbackLocation MainAssembly = 0;
	public const UltimateResourceFallbackLocation Satellite = 1;
}
```

---

### public enum AssemblyNameFlags

```csharp
public enum AssemblyNameFlags 
{
	public int value__; 
	public const AssemblyNameFlags None = 0;
	public const AssemblyNameFlags PublicKey = 1;
	public const AssemblyNameFlags EnableJITcompileOptimizer = 16384;
	public const AssemblyNameFlags EnableJITcompileTracking = 32768;
	public const AssemblyNameFlags Retargetable = 256;
}
```

---

### public enum AssemblyContentType

```csharp
public enum AssemblyContentType 
{
	public int value__; 
	public const AssemblyContentType Default = 0;
	public const AssemblyContentType WindowsRuntime = 1;
}
```

---

### public enum ProcessorArchitecture

```csharp
public enum ProcessorArchitecture 
{
	public int value__; 
	public const ProcessorArchitecture None = 0;
	public const ProcessorArchitecture MSIL = 1;
	public const ProcessorArchitecture X86 = 2;
	public const ProcessorArchitecture IA64 = 3;
	public const ProcessorArchitecture Amd64 = 4;
	public const ProcessorArchitecture Arm = 5;
}
```

---

### public enum BindingFlags

```csharp
public enum BindingFlags 
{
	public int value__; 
	public const BindingFlags Default = 0;
	public const BindingFlags IgnoreCase = 1;
	public const BindingFlags DeclaredOnly = 2;
	public const BindingFlags Instance = 4;
	public const BindingFlags Static = 8;
	public const BindingFlags Public = 16;
	public const BindingFlags NonPublic = 32;
	public const BindingFlags FlattenHierarchy = 64;
	public const BindingFlags InvokeMethod = 256;
	public const BindingFlags CreateInstance = 512;
	public const BindingFlags GetField = 1024;
	public const BindingFlags SetField = 2048;
	public const BindingFlags GetProperty = 4096;
	public const BindingFlags SetProperty = 8192;
	public const BindingFlags PutDispProperty = 16384;
	public const BindingFlags PutRefDispProperty = 32768;
	public const BindingFlags ExactBinding = 65536;
	public const BindingFlags SuppressChangeType = 131072;
	public const BindingFlags OptionalParamBinding = 262144;
	public const BindingFlags IgnoreReturn = 16777216;
}
```

---

### public enum CallingConventions

```csharp
public enum CallingConventions 
{
	public int value__; 
	public const CallingConventions Standard = 1;
	public const CallingConventions VarArgs = 2;
	public const CallingConventions Any = 3;
	public const CallingConventions HasThis = 32;
	public const CallingConventions ExplicitThis = 64;
}
```

---

### public enum EventAttributes

```csharp
public enum EventAttributes 
{
	public int value__; 
	public const EventAttributes None = 0;
	public const EventAttributes SpecialName = 512;
	public const EventAttributes ReservedMask = 1024;
	public const EventAttributes RTSpecialName = 1024;
}
```

---

### public enum FieldAttributes

```csharp
public enum FieldAttributes 
{
	public int value__; 
	public const FieldAttributes FieldAccessMask = 7;
	public const FieldAttributes PrivateScope = 0;
	public const FieldAttributes Private = 1;
	public const FieldAttributes FamANDAssem = 2;
	public const FieldAttributes Assembly = 3;
	public const FieldAttributes Family = 4;
	public const FieldAttributes FamORAssem = 5;
	public const FieldAttributes Public = 6;
	public const FieldAttributes Static = 16;
	public const FieldAttributes InitOnly = 32;
	public const FieldAttributes Literal = 64;
	public const FieldAttributes NotSerialized = 128;
	public const FieldAttributes SpecialName = 512;
	public const FieldAttributes PinvokeImpl = 8192;
	public const FieldAttributes ReservedMask = 38144;
	public const FieldAttributes RTSpecialName = 1024;
	public const FieldAttributes HasFieldMarshal = 4096;
	public const FieldAttributes HasDefault = 32768;
	public const FieldAttributes HasFieldRVA = 256;
}
```

---

### public enum GenericParameterAttributes

```csharp
public enum GenericParameterAttributes 
{
	public int value__; 
	public const GenericParameterAttributes None = 0;
	public const GenericParameterAttributes VarianceMask = 3;
	public const GenericParameterAttributes Covariant = 1;
	public const GenericParameterAttributes Contravariant = 2;
	public const GenericParameterAttributes SpecialConstraintMask = 28;
	public const GenericParameterAttributes ReferenceTypeConstraint = 4;
	public const GenericParameterAttributes NotNullableValueTypeConstraint = 8;
	public const GenericParameterAttributes DefaultConstructorConstraint = 16;
}
```

---

### public enum ResourceLocation

```csharp
public enum ResourceLocation 
{
	public int value__; 
	public const ResourceLocation Embedded = 1;
	public const ResourceLocation ContainedInAnotherAssembly = 2;
	public const ResourceLocation ContainedInManifestFile = 4;
}
```

---

### internal enum PInvokeAttributes

```csharp
internal enum PInvokeAttributes 
{
	public int value__; 
	public const PInvokeAttributes NoMangle = 1;
	public const PInvokeAttributes CharSetMask = 6;
	public const PInvokeAttributes CharSetNotSpec = 0;
	public const PInvokeAttributes CharSetAnsi = 2;
	public const PInvokeAttributes CharSetUnicode = 4;
	public const PInvokeAttributes CharSetAuto = 6;
	public const PInvokeAttributes BestFitUseAssem = 0;
	public const PInvokeAttributes BestFitEnabled = 16;
	public const PInvokeAttributes BestFitDisabled = 32;
	public const PInvokeAttributes BestFitMask = 48;
	public const PInvokeAttributes ThrowOnUnmappableCharUseAssem = 0;
	public const PInvokeAttributes ThrowOnUnmappableCharEnabled = 4096;
	public const PInvokeAttributes ThrowOnUnmappableCharDisabled = 8192;
	public const PInvokeAttributes ThrowOnUnmappableCharMask = 12288;
	public const PInvokeAttributes SupportsLastError = 64;
	public const PInvokeAttributes CallConvMask = 1792;
	public const PInvokeAttributes CallConvWinapi = 256;
	public const PInvokeAttributes CallConvCdecl = 512;
	public const PInvokeAttributes CallConvStdcall = 768;
	public const PInvokeAttributes CallConvThiscall = 1024;
	public const PInvokeAttributes CallConvFastcall = 1280;
	public const PInvokeAttributes MaxValue = 65535;
}
```

---

### public enum MemberTypes

```csharp
public enum MemberTypes 
{
	public int value__; 
	public const MemberTypes Constructor = 1;
	public const MemberTypes Event = 2;
	public const MemberTypes Field = 4;
	public const MemberTypes Method = 8;
	public const MemberTypes Property = 16;
	public const MemberTypes TypeInfo = 32;
	public const MemberTypes Custom = 64;
	public const MemberTypes NestedType = 128;
	public const MemberTypes All = 191;
}
```

---

### public enum MethodAttributes

```csharp
public enum MethodAttributes 
{
	public int value__; 
	public const MethodAttributes MemberAccessMask = 7;
	public const MethodAttributes PrivateScope = 0;
	public const MethodAttributes Private = 1;
	public const MethodAttributes FamANDAssem = 2;
	public const MethodAttributes Assembly = 3;
	public const MethodAttributes Family = 4;
	public const MethodAttributes FamORAssem = 5;
	public const MethodAttributes Public = 6;
	public const MethodAttributes Static = 16;
	public const MethodAttributes Final = 32;
	public const MethodAttributes Virtual = 64;
	public const MethodAttributes HideBySig = 128;
	public const MethodAttributes CheckAccessOnOverride = 512;
	public const MethodAttributes VtableLayoutMask = 256;
	public const MethodAttributes ReuseSlot = 0;
	public const MethodAttributes NewSlot = 256;
	public const MethodAttributes Abstract = 1024;
	public const MethodAttributes SpecialName = 2048;
	public const MethodAttributes PinvokeImpl = 8192;
	public const MethodAttributes UnmanagedExport = 8;
	public const MethodAttributes RTSpecialName = 4096;
	public const MethodAttributes ReservedMask = 53248;
	public const MethodAttributes HasSecurity = 16384;
	public const MethodAttributes RequireSecObject = 32768;
}
```

---

### public enum ExceptionHandlingClauseOptions

```csharp
public enum ExceptionHandlingClauseOptions 
{
	public int value__; 
	public const ExceptionHandlingClauseOptions Clause = 0;
	public const ExceptionHandlingClauseOptions Filter = 1;
	public const ExceptionHandlingClauseOptions Finally = 2;
	public const ExceptionHandlingClauseOptions Fault = 4;
}
```

---

### public enum MethodImplAttributes

```csharp
public enum MethodImplAttributes 
{
	public int value__; 
	public const MethodImplAttributes CodeTypeMask = 3;
	public const MethodImplAttributes IL = 0;
	public const MethodImplAttributes Native = 1;
	public const MethodImplAttributes OPTIL = 2;
	public const MethodImplAttributes Runtime = 3;
	public const MethodImplAttributes ManagedMask = 4;
	public const MethodImplAttributes Unmanaged = 4;
	public const MethodImplAttributes Managed = 0;
	public const MethodImplAttributes ForwardRef = 16;
	public const MethodImplAttributes PreserveSig = 128;
	public const MethodImplAttributes InternalCall = 4096;
	public const MethodImplAttributes Synchronized = 32;
	public const MethodImplAttributes NoInlining = 8;
	[ComVisibleAttribute] 
	public const MethodImplAttributes AggressiveInlining = 256;
	public const MethodImplAttributes NoOptimization = 64;
	public const MethodImplAttributes MaxMethodImplVal = 65535;
}
```

---

### public enum ParameterAttributes

```csharp
public enum ParameterAttributes 
{
	public int value__; 
	public const ParameterAttributes None = 0;
	public const ParameterAttributes In = 1;
	public const ParameterAttributes Out = 2;
	public const ParameterAttributes Lcid = 4;
	public const ParameterAttributes Retval = 8;
	public const ParameterAttributes Optional = 16;
	public const ParameterAttributes ReservedMask = 61440;
	public const ParameterAttributes HasDefault = 4096;
	public const ParameterAttributes HasFieldMarshal = 8192;
	public const ParameterAttributes Reserved3 = 16384;
	public const ParameterAttributes Reserved4 = 32768;
}
```

---

### public enum PropertyAttributes

```csharp
public enum PropertyAttributes 
{
	public int value__; 
	public const PropertyAttributes None = 0;
	public const PropertyAttributes SpecialName = 512;
	public const PropertyAttributes ReservedMask = 62464;
	public const PropertyAttributes RTSpecialName = 1024;
	public const PropertyAttributes HasDefault = 4096;
	public const PropertyAttributes Reserved2 = 8192;
	public const PropertyAttributes Reserved3 = 16384;
	public const PropertyAttributes Reserved4 = 32768;
}
```

---

### public enum TypeAttributes

```csharp
public enum TypeAttributes 
{
	public int value__; 
	public const TypeAttributes VisibilityMask = 7;
	public const TypeAttributes NotPublic = 0;
	public const TypeAttributes Public = 1;
	public const TypeAttributes NestedPublic = 2;
	public const TypeAttributes NestedPrivate = 3;
	public const TypeAttributes NestedFamily = 4;
	public const TypeAttributes NestedAssembly = 5;
	public const TypeAttributes NestedFamANDAssem = 6;
	public const TypeAttributes NestedFamORAssem = 7;
	public const TypeAttributes LayoutMask = 24;
	public const TypeAttributes AutoLayout = 0;
	public const TypeAttributes SequentialLayout = 8;
	public const TypeAttributes ExplicitLayout = 16;
	public const TypeAttributes ClassSemanticsMask = 32;
	public const TypeAttributes Class = 0;
	public const TypeAttributes Interface = 32;
	public const TypeAttributes Abstract = 128;
	public const TypeAttributes Sealed = 256;
	public const TypeAttributes SpecialName = 1024;
	public const TypeAttributes Import = 4096;
	public const TypeAttributes Serializable = 8192;
	[ComVisibleAttribute] 
	public const TypeAttributes WindowsRuntime = 16384;
	public const TypeAttributes StringFormatMask = 196608;
	public const TypeAttributes AnsiClass = 0;
	public const TypeAttributes UnicodeClass = 65536;
	public const TypeAttributes AutoClass = 131072;
	public const TypeAttributes CustomFormatClass = 196608;
	public const TypeAttributes CustomFormatMask = 12582912;
	public const TypeAttributes BeforeFieldInit = 1048576;
	public const TypeAttributes ReservedMask = 264192;
	public const TypeAttributes RTSpecialName = 2048;
	public const TypeAttributes HasSecurity = 262144;
}
```

---

### internal enum PInfo

```csharp
internal enum PInfo 
{
	public int value__; 
	public const PInfo Attributes = 1;
	public const PInfo GetMethod = 2;
	public const PInfo SetMethod = 4;
	public const PInfo ReflectedType = 8;
	public const PInfo DeclaringType = 16;
	public const PInfo Name = 32;
}
```

---

### public enum FileAccess

```csharp
public enum FileAccess 
{
	public int value__; 
	public const FileAccess Read = 1;
	public const FileAccess Write = 2;
	public const FileAccess ReadWrite = 3;
}
```

---

### public enum FileAttributes

```csharp
public enum FileAttributes 
{
	public int value__; 
	public const FileAttributes Archive = 32;
	public const FileAttributes Compressed = 2048;
	public const FileAttributes Device = 64;
	public const FileAttributes Directory = 16;
	public const FileAttributes Encrypted = 16384;
	public const FileAttributes Hidden = 2;
	public const FileAttributes Normal = 128;
	public const FileAttributes NotContentIndexed = 8192;
	public const FileAttributes Offline = 4096;
	public const FileAttributes ReadOnly = 1;
	public const FileAttributes ReparsePoint = 1024;
	public const FileAttributes SparseFile = 512;
	public const FileAttributes System = 4;
	public const FileAttributes Temporary = 256;
	public const FileAttributes IntegrityStream = 32768;
	public const FileAttributes NoScrubData = 131072;
}
```

---

### public enum FileMode

```csharp
public enum FileMode 
{
	public int value__; 
	public const FileMode CreateNew = 1;
	public const FileMode Create = 2;
	public const FileMode Open = 3;
	public const FileMode OpenOrCreate = 4;
	public const FileMode Truncate = 5;
	public const FileMode Append = 6;
}
```

---

### public enum FileOptions

```csharp
public enum FileOptions 
{
	public int value__; 
	public const FileOptions None = 0;
	public const FileOptions Encrypted = 16384;
	public const FileOptions DeleteOnClose = 67108864;
	public const FileOptions SequentialScan = 134217728;
	public const FileOptions RandomAccess = 268435456;
	public const FileOptions Asynchronous = 1073741824;
	public const FileOptions WriteThrough = -2147483648;
}
```

---

### public enum FileShare

```csharp
public enum FileShare 
{
	public int value__; 
	public const FileShare None = 0;
	public const FileShare Read = 1;
	public const FileShare Write = 2;
	public const FileShare ReadWrite = 3;
	public const FileShare Delete = 4;
	public const FileShare Inheritable = 16;
}
```

---

### internal enum MonoFileType

```csharp
internal enum MonoFileType 
{
	public int value__; 
	public const MonoFileType Unknown = 0;
	public const MonoFileType Disk = 1;
	public const MonoFileType Char = 2;
	public const MonoFileType Pipe = 3;
	public const MonoFileType Remote = 32768;
}
```

---

### internal enum MonoIOError

```csharp
internal enum MonoIOError 
{
	public int value__; 
	public const MonoIOError ERROR_SUCCESS = 0;
	public const MonoIOError ERROR_FILE_NOT_FOUND = 2;
	public const MonoIOError ERROR_PATH_NOT_FOUND = 3;
	public const MonoIOError ERROR_TOO_MANY_OPEN_FILES = 4;
	public const MonoIOError ERROR_ACCESS_DENIED = 5;
	public const MonoIOError ERROR_INVALID_HANDLE = 6;
	public const MonoIOError ERROR_INVALID_DRIVE = 15;
	public const MonoIOError ERROR_NOT_SAME_DEVICE = 17;
	public const MonoIOError ERROR_NO_MORE_FILES = 18;
	public const MonoIOError ERROR_NOT_READY = 21;
	public const MonoIOError ERROR_WRITE_FAULT = 29;
	public const MonoIOError ERROR_READ_FAULT = 30;
	public const MonoIOError ERROR_GEN_FAILURE = 31;
	public const MonoIOError ERROR_SHARING_VIOLATION = 32;
	public const MonoIOError ERROR_LOCK_VIOLATION = 33;
	public const MonoIOError ERROR_HANDLE_DISK_FULL = 39;
	public const MonoIOError ERROR_FILE_EXISTS = 80;
	public const MonoIOError ERROR_CANNOT_MAKE = 82;
	public const MonoIOError ERROR_INVALID_PARAMETER = 87;
	public const MonoIOError ERROR_BROKEN_PIPE = 109;
	public const MonoIOError ERROR_INVALID_NAME = 123;
	public const MonoIOError ERROR_DIR_NOT_EMPTY = 145;
	public const MonoIOError ERROR_ALREADY_EXISTS = 183;
	public const MonoIOError ERROR_FILENAME_EXCED_RANGE = 206;
	public const MonoIOError ERROR_DIRECTORY = 267;
	public const MonoIOError ERROR_ENCRYPTION_FAILED = 6000;
}
```

---

### public enum SearchOption

```csharp
public enum SearchOption 
{
	public int value__; 
	public const SearchOption TopDirectoryOnly = 0;
	public const SearchOption AllDirectories = 1;
}
```

---

### public enum SeekOrigin

```csharp
public enum SeekOrigin 
{
	public int value__; 
	public const SeekOrigin Begin = 0;
	public const SeekOrigin Current = 1;
	public const SeekOrigin End = 2;
}
```

---

### public enum CompareOptions

```csharp
public enum CompareOptions 
{
	public int value__; 
	public const CompareOptions None = 0;
	public const CompareOptions IgnoreCase = 1;
	public const CompareOptions IgnoreNonSpace = 2;
	public const CompareOptions IgnoreSymbols = 4;
	public const CompareOptions IgnoreKanaType = 8;
	public const CompareOptions IgnoreWidth = 16;
	public const CompareOptions OrdinalIgnoreCase = 268435456;
	public const CompareOptions StringSort = 536870912;
	public const CompareOptions Ordinal = 1073741824;
}
```

---

### public enum CultureTypes

```csharp
public enum CultureTypes 
{
	public int value__; 
	public const CultureTypes NeutralCultures = 1;
	public const CultureTypes SpecificCultures = 2;
	public const CultureTypes InstalledWin32Cultures = 4;
	public const CultureTypes AllCultures = 7;
	public const CultureTypes UserCustomCulture = 8;
	public const CultureTypes ReplacementCultures = 16;
	[ObsoleteAttribute] 
	public const CultureTypes WindowsOnlyCultures = 32;
	[ObsoleteAttribute] 
	public const CultureTypes FrameworkCultures = 64;
}
```

---

### internal enum MonthNameStyles

```csharp
internal enum MonthNameStyles 
{
	public int value__; 
	public const MonthNameStyles Regular = 0;
	public const MonthNameStyles Genitive = 1;
	public const MonthNameStyles LeapYear = 2;
}
```

---

### internal enum DateTimeFormatFlags

```csharp
internal enum DateTimeFormatFlags 
{
	public int value__; 
	public const DateTimeFormatFlags None = 0;
	public const DateTimeFormatFlags UseGenitiveMonth = 1;
	public const DateTimeFormatFlags UseLeapYearMonth = 2;
	public const DateTimeFormatFlags UseSpacesInMonthNames = 4;
	public const DateTimeFormatFlags UseHebrewRule = 8;
	public const DateTimeFormatFlags UseSpacesInDayNames = 16;
	public const DateTimeFormatFlags UseDigitPrefixInTokens = 32;
	public const DateTimeFormatFlags NotInitialized = -1;
}
```

---

### internal enum FORMATFLAGS

```csharp
internal enum FORMATFLAGS 
{
	public int value__; 
	public const FORMATFLAGS None = 0;
	public const FORMATFLAGS UseGenitiveMonth = 1;
	public const FORMATFLAGS UseLeapYearMonth = 2;
	public const FORMATFLAGS UseSpacesInMonthNames = 4;
	public const FORMATFLAGS UseHebrewParsing = 8;
	public const FORMATFLAGS UseSpacesInDayNames = 16;
	public const FORMATFLAGS UseDigitPrefixInTokens = 32;
}
```

---

### internal enum CalendarId

```csharp
internal enum CalendarId 
{
	public ushort value__; 
	public const CalendarId GREGORIAN = 1;
	public const CalendarId GREGORIAN_US = 2;
	public const CalendarId JAPAN = 3;
	public const CalendarId TAIWAN = 4;
	public const CalendarId KOREA = 5;
	public const CalendarId HIJRI = 6;
	public const CalendarId THAI = 7;
	public const CalendarId HEBREW = 8;
	public const CalendarId GREGORIAN_ME_FRENCH = 9;
	public const CalendarId GREGORIAN_ARABIC = 10;
	public const CalendarId GREGORIAN_XLIT_ENGLISH = 11;
	public const CalendarId GREGORIAN_XLIT_FRENCH = 12;
	public const CalendarId JULIAN = 13;
	public const CalendarId JAPANESELUNISOLAR = 14;
	public const CalendarId CHINESELUNISOLAR = 15;
	public const CalendarId SAKA = 16;
	public const CalendarId LUNAR_ETO_CHN = 17;
	public const CalendarId LUNAR_ETO_KOR = 18;
	public const CalendarId LUNAR_ETO_ROKUYOU = 19;
	public const CalendarId KOREANLUNISOLAR = 20;
	public const CalendarId TAIWANLUNISOLAR = 21;
	public const CalendarId PERSIAN = 22;
	public const CalendarId UMALQURA = 23;
	public const CalendarId LAST_CALENDAR = 23;
}
```

---

### public enum DateTimeStyles

```csharp
public enum DateTimeStyles 
{
	public int value__; 
	public const DateTimeStyles None = 0;
	public const DateTimeStyles AllowLeadingWhite = 1;
	public const DateTimeStyles AllowTrailingWhite = 2;
	public const DateTimeStyles AllowInnerWhite = 4;
	public const DateTimeStyles AllowWhiteSpaces = 7;
	public const DateTimeStyles NoCurrentDateDefault = 8;
	public const DateTimeStyles AdjustToUniversal = 16;
	public const DateTimeStyles AssumeLocal = 32;
	public const DateTimeStyles AssumeUniversal = 64;
	public const DateTimeStyles RoundtripKind = 128;
}
```

---

### public enum GregorianCalendarTypes

```csharp
public enum GregorianCalendarTypes 
{
	public int value__; 
	public const GregorianCalendarTypes Localized = 1;
	public const GregorianCalendarTypes USEnglish = 2;
	public const GregorianCalendarTypes MiddleEastFrench = 9;
	public const GregorianCalendarTypes Arabic = 10;
	public const GregorianCalendarTypes TransliteratedEnglish = 11;
	public const GregorianCalendarTypes TransliteratedFrench = 12;
}
```

---

### internal enum HebrewNumberParsingState

```csharp
internal enum HebrewNumberParsingState 
{
	public int value__; 
	public const HebrewNumberParsingState InvalidHebrewNumber = 0;
	public const HebrewNumberParsingState NotHebrewDigit = 1;
	public const HebrewNumberParsingState FoundEndOfHebrewNumber = 2;
	public const HebrewNumberParsingState ContinueParsing = 3;
}
```

---

### internal enum HebrewNumber.HS

```csharp
internal enum HebrewNumber.HS 
{
	public int value__; 
	public const HebrewNumber.HS _err = -1;
	public const HebrewNumber.HS Start = 0;
	public const HebrewNumber.HS S400 = 1;
	public const HebrewNumber.HS S400_400 = 2;
	public const HebrewNumber.HS S400_X00 = 3;
	public const HebrewNumber.HS S400_X0 = 4;
	public const HebrewNumber.HS X00_DQ = 5;
	public const HebrewNumber.HS S400_X00_X0 = 6;
	public const HebrewNumber.HS X0_DQ = 7;
	public const HebrewNumber.HS X = 8;
	public const HebrewNumber.HS X0 = 9;
	public const HebrewNumber.HS X00 = 10;
	public const HebrewNumber.HS S400_DQ = 11;
	public const HebrewNumber.HS S400_400_DQ = 12;
	public const HebrewNumber.HS S400_400_100 = 13;
	public const HebrewNumber.HS S9 = 14;
	public const HebrewNumber.HS X00_S9 = 15;
	public const HebrewNumber.HS S9_DQ = 16;
	public const HebrewNumber.HS END = 100;
}
```

---

### public enum NumberStyles

```csharp
public enum NumberStyles 
{
	public int value__; 
	public const NumberStyles None = 0;
	public const NumberStyles AllowLeadingWhite = 1;
	public const NumberStyles AllowTrailingWhite = 2;
	public const NumberStyles AllowLeadingSign = 4;
	public const NumberStyles AllowTrailingSign = 8;
	public const NumberStyles AllowParentheses = 16;
	public const NumberStyles AllowDecimalPoint = 32;
	public const NumberStyles AllowThousands = 64;
	public const NumberStyles AllowExponent = 128;
	public const NumberStyles AllowCurrencySymbol = 256;
	public const NumberStyles AllowHexSpecifier = 512;
	public const NumberStyles Integer = 7;
	public const NumberStyles HexNumber = 515;
	public const NumberStyles Number = 111;
	public const NumberStyles Float = 167;
	public const NumberStyles Currency = 383;
	public const NumberStyles Any = 511;
}
```

---

### internal enum TimeSpanFormat.Pattern

```csharp
internal enum TimeSpanFormat.Pattern 
{
	public int value__; 
	public const TimeSpanFormat.Pattern None = 0;
	public const TimeSpanFormat.Pattern Minimum = 1;
	public const TimeSpanFormat.Pattern Full = 2;
}
```

---

### public enum UnicodeCategory

```csharp
public enum UnicodeCategory 
{
	public int value__; 
	public const UnicodeCategory UppercaseLetter = 0;
	public const UnicodeCategory LowercaseLetter = 1;
	public const UnicodeCategory TitlecaseLetter = 2;
	public const UnicodeCategory ModifierLetter = 3;
	public const UnicodeCategory OtherLetter = 4;
	public const UnicodeCategory NonSpacingMark = 5;
	public const UnicodeCategory SpacingCombiningMark = 6;
	public const UnicodeCategory EnclosingMark = 7;
	public const UnicodeCategory DecimalDigitNumber = 8;
	public const UnicodeCategory LetterNumber = 9;
	public const UnicodeCategory OtherNumber = 10;
	public const UnicodeCategory SpaceSeparator = 11;
	public const UnicodeCategory LineSeparator = 12;
	public const UnicodeCategory ParagraphSeparator = 13;
	public const UnicodeCategory Control = 14;
	public const UnicodeCategory Format = 15;
	public const UnicodeCategory Surrogate = 16;
	public const UnicodeCategory PrivateUse = 17;
	public const UnicodeCategory ConnectorPunctuation = 18;
	public const UnicodeCategory DashPunctuation = 19;
	public const UnicodeCategory OpenPunctuation = 20;
	public const UnicodeCategory ClosePunctuation = 21;
	public const UnicodeCategory InitialQuotePunctuation = 22;
	public const UnicodeCategory FinalQuotePunctuation = 23;
	public const UnicodeCategory OtherPunctuation = 24;
	public const UnicodeCategory MathSymbol = 25;
	public const UnicodeCategory CurrencySymbol = 26;
	public const UnicodeCategory ModifierSymbol = 27;
	public const UnicodeCategory OtherSymbol = 28;
	public const UnicodeCategory OtherNotAssigned = 29;
}
```

---

### public enum LazyThreadSafetyMode

```csharp
public enum LazyThreadSafetyMode 
{
	public int value__; 
	public const LazyThreadSafetyMode None = 0;
	public const LazyThreadSafetyMode PublicationOnly = 1;
	public const LazyThreadSafetyMode ExecutionAndPublication = 2;
}
```

---

### public enum EventResetMode

```csharp
public enum EventResetMode 
{
	public int value__; 
	public const EventResetMode AutoReset = 0;
	public const EventResetMode ManualReset = 1;
}
```

---

### internal enum ExecutionContext.CaptureOptions

```csharp
internal enum ExecutionContext.CaptureOptions 
{
	public int value__; 
	public const ExecutionContext.CaptureOptions None = 0;
	public const ExecutionContext.CaptureOptions IgnoreSyncCtx = 1;
	public const ExecutionContext.CaptureOptions OptimizeDefaultCase = 2;
}
```

---

### internal enum SynchronizationContextProperties

```csharp
internal enum SynchronizationContextProperties 
{
	public int value__; 
	public const SynchronizationContextProperties None = 0;
	public const SynchronizationContextProperties RequireWaitNotification = 1;
}
```

---

### internal enum StackCrawlMark

```csharp
internal enum StackCrawlMark 
{
	public int value__; 
	public const StackCrawlMark LookForMe = 0;
	public const StackCrawlMark LookForMyCaller = 1;
	public const StackCrawlMark LookForMyCallersCaller = 2;
	public const StackCrawlMark LookForThread = 3;
}
```

---

### public enum ThreadPriority

```csharp
public enum ThreadPriority 
{
	public int value__; 
	public const ThreadPriority Lowest = 0;
	public const ThreadPriority BelowNormal = 1;
	public const ThreadPriority Normal = 2;
	public const ThreadPriority AboveNormal = 3;
	public const ThreadPriority Highest = 4;
}
```

---

### public enum ThreadState

```csharp
public enum ThreadState 
{
	public int value__; 
	public const ThreadState Running = 0;
	public const ThreadState StopRequested = 1;
	public const ThreadState SuspendRequested = 2;
	public const ThreadState Background = 4;
	public const ThreadState Unstarted = 8;
	public const ThreadState Stopped = 16;
	public const ThreadState WaitSleepJoin = 32;
	public const ThreadState Suspended = 64;
	public const ThreadState AbortRequested = 128;
	public const ThreadState Aborted = 256;
}
```

---

### internal enum CausalityTraceLevel

```csharp
internal enum CausalityTraceLevel 
{
	public int value__; 
	public const CausalityTraceLevel Required = 0;
	public const CausalityTraceLevel Important = 1;
	public const CausalityTraceLevel Verbose = 2;
}
```

---

### internal enum AsyncCausalityStatus

```csharp
internal enum AsyncCausalityStatus 
{
	public int value__; 
	public const AsyncCausalityStatus Started = 0;
	public const AsyncCausalityStatus Completed = 1;
	public const AsyncCausalityStatus Canceled = 2;
	public const AsyncCausalityStatus Error = 3;
}
```

---

### internal enum CausalityRelation

```csharp
internal enum CausalityRelation 
{
	public int value__; 
	public const CausalityRelation AssignDelegate = 0;
	public const CausalityRelation Join = 1;
	public const CausalityRelation Choice = 2;
	public const CausalityRelation Cancel = 3;
	public const CausalityRelation Error = 4;
}
```

---

### internal enum CausalitySynchronousWork

```csharp
internal enum CausalitySynchronousWork 
{
	public int value__; 
	public const CausalitySynchronousWork CompletionNotification = 0;
	public const CausalitySynchronousWork ProgressNotification = 1;
	public const CausalitySynchronousWork Execution = 2;
}
```

---

### public enum TaskStatus

```csharp
public enum TaskStatus 
{
	public int value__; 
	public const TaskStatus Created = 0;
	public const TaskStatus WaitingForActivation = 1;
	public const TaskStatus WaitingToRun = 2;
	public const TaskStatus Running = 3;
	public const TaskStatus WaitingForChildrenToComplete = 4;
	public const TaskStatus RanToCompletion = 5;
	public const TaskStatus Canceled = 6;
	public const TaskStatus Faulted = 7;
}
```

---

### public enum TaskCreationOptions

```csharp
public enum TaskCreationOptions 
{
	public int value__; 
	public const TaskCreationOptions None = 0;
	public const TaskCreationOptions PreferFairness = 1;
	public const TaskCreationOptions LongRunning = 2;
	public const TaskCreationOptions AttachedToParent = 4;
	public const TaskCreationOptions DenyChildAttach = 8;
	public const TaskCreationOptions HideScheduler = 16;
	public const TaskCreationOptions RunContinuationsAsynchronously = 64;
}
```

---

### internal enum InternalTaskOptions

```csharp
internal enum InternalTaskOptions 
{
	public int value__; 
	public const InternalTaskOptions None = 0;
	public const InternalTaskOptions InternalOptionsMask = 65280;
	public const InternalTaskOptions ChildReplica = 256;
	public const InternalTaskOptions ContinuationTask = 512;
	public const InternalTaskOptions PromiseTask = 1024;
	public const InternalTaskOptions SelfReplicating = 2048;
	public const InternalTaskOptions LazyCancellation = 4096;
	public const InternalTaskOptions QueuedByRuntime = 8192;
	public const InternalTaskOptions DoNotDispose = 16384;
}
```

---

### public enum TaskContinuationOptions

```csharp
public enum TaskContinuationOptions 
{
	public int value__; 
	public const TaskContinuationOptions None = 0;
	public const TaskContinuationOptions PreferFairness = 1;
	public const TaskContinuationOptions LongRunning = 2;
	public const TaskContinuationOptions AttachedToParent = 4;
	public const TaskContinuationOptions DenyChildAttach = 8;
	public const TaskContinuationOptions HideScheduler = 16;
	public const TaskContinuationOptions LazyCancellation = 32;
	public const TaskContinuationOptions RunContinuationsAsynchronously = 64;
	public const TaskContinuationOptions NotOnRanToCompletion = 65536;
	public const TaskContinuationOptions NotOnFaulted = 131072;
	public const TaskContinuationOptions NotOnCanceled = 262144;
	public const TaskContinuationOptions OnlyOnRanToCompletion = 393216;
	public const TaskContinuationOptions OnlyOnFaulted = 327680;
	public const TaskContinuationOptions OnlyOnCanceled = 196608;
	public const TaskContinuationOptions ExecuteSynchronously = 524288;
}
```

---

### public enum CipherMode

```csharp
public enum CipherMode 
{
	public int value__; 
	public const CipherMode CBC = 1;
	public const CipherMode ECB = 2;
	public const CipherMode OFB = 3;
	public const CipherMode CFB = 4;
	public const CipherMode CTS = 5;
}
```

---

### public enum PaddingMode

```csharp
public enum PaddingMode 
{
	public int value__; 
	public const PaddingMode None = 1;
	public const PaddingMode PKCS7 = 2;
	public const PaddingMode Zeros = 3;
	public const PaddingMode ANSIX923 = 4;
	public const PaddingMode ISO10126 = 5;
}
```

---

### public enum CspProviderFlags

```csharp
public enum CspProviderFlags 
{
	public int value__; 
	public const CspProviderFlags NoFlags = 0;
	public const CspProviderFlags UseMachineKeyStore = 1;
	public const CspProviderFlags UseDefaultKeyContainer = 2;
	public const CspProviderFlags UseNonExportableKey = 4;
	public const CspProviderFlags UseExistingKey = 8;
	public const CspProviderFlags UseArchivableKey = 16;
	public const CspProviderFlags UseUserProtectedKey = 32;
	public const CspProviderFlags NoPrompt = 64;
	public const CspProviderFlags CreateEphemeralKey = 128;
}
```

---

### public enum CryptoStreamMode

```csharp
public enum CryptoStreamMode 
{
	public int value__; 
	public const CryptoStreamMode Read = 0;
	public const CryptoStreamMode Write = 1;
}
```

---

### internal enum RijndaelManagedTransformMode

```csharp
internal enum RijndaelManagedTransformMode 
{
	public int value__; 
	public const RijndaelManagedTransformMode Encrypt = 0;
	public const RijndaelManagedTransformMode Decrypt = 1;
}
```

---

### internal enum OidGroup

```csharp
internal enum OidGroup 
{
	public int value__; 
	public const OidGroup AllGroups = 0;
	public const OidGroup HashAlgorithm = 1;
	public const OidGroup EncryptionAlgorithm = 2;
	public const OidGroup PublicKeyAlgorithm = 3;
	public const OidGroup SignatureAlgorithm = 4;
	public const OidGroup Attribute = 5;
	public const OidGroup ExtensionOrAttribute = 6;
	public const OidGroup EnhancedKeyUsage = 7;
	public const OidGroup Policy = 8;
	public const OidGroup Template = 9;
	public const OidGroup KeyDerivationFunction = 10;
	public const OidGroup DisableSearchDS = -2147483648;
}
```

---

### public enum StreamingContextStates

```csharp
public enum StreamingContextStates 
{
	public int value__; 
	public const StreamingContextStates CrossProcess = 1;
	public const StreamingContextStates CrossMachine = 2;
	public const StreamingContextStates File = 4;
	public const StreamingContextStates Persistence = 8;
	public const StreamingContextStates Remoting = 16;
	public const StreamingContextStates Other = 32;
	public const StreamingContextStates Clone = 64;
	public const StreamingContextStates CrossAppDomain = 128;
	public const StreamingContextStates All = 255;
}
```

---

### public enum FormatterTypeStyle

```csharp
public enum FormatterTypeStyle 
{
	public int value__; 
	public const FormatterTypeStyle TypesWhenNeeded = 0;
	public const FormatterTypeStyle TypesAlways = 1;
	public const FormatterTypeStyle XsdString = 2;
}
```

---

### public enum FormatterAssemblyStyle

```csharp
public enum FormatterAssemblyStyle 
{
	public int value__; 
	public const FormatterAssemblyStyle Simple = 0;
	public const FormatterAssemblyStyle Full = 1;
}
```

---

### public enum TypeFilterLevel

```csharp
public enum TypeFilterLevel 
{
	public int value__; 
	public const TypeFilterLevel Low = 2;
	public const TypeFilterLevel Full = 3;
}
```

---

### internal enum BinaryHeaderEnum

```csharp
internal enum BinaryHeaderEnum 
{
	public int value__; 
	public const BinaryHeaderEnum SerializedStreamHeader = 0;
	public const BinaryHeaderEnum Object = 1;
	public const BinaryHeaderEnum ObjectWithMap = 2;
	public const BinaryHeaderEnum ObjectWithMapAssemId = 3;
	public const BinaryHeaderEnum ObjectWithMapTyped = 4;
	public const BinaryHeaderEnum ObjectWithMapTypedAssemId = 5;
	public const BinaryHeaderEnum ObjectString = 6;
	public const BinaryHeaderEnum Array = 7;
	public const BinaryHeaderEnum MemberPrimitiveTyped = 8;
	public const BinaryHeaderEnum MemberReference = 9;
	public const BinaryHeaderEnum ObjectNull = 10;
	public const BinaryHeaderEnum MessageEnd = 11;
	public const BinaryHeaderEnum Assembly = 12;
	public const BinaryHeaderEnum ObjectNullMultiple256 = 13;
	public const BinaryHeaderEnum ObjectNullMultiple = 14;
	public const BinaryHeaderEnum ArraySinglePrimitive = 15;
	public const BinaryHeaderEnum ArraySingleObject = 16;
	public const BinaryHeaderEnum ArraySingleString = 17;
	public const BinaryHeaderEnum CrossAppDomainMap = 18;
	public const BinaryHeaderEnum CrossAppDomainString = 19;
	public const BinaryHeaderEnum CrossAppDomainAssembly = 20;
	public const BinaryHeaderEnum MethodCall = 21;
	public const BinaryHeaderEnum MethodReturn = 22;
}
```

---

### internal enum BinaryTypeEnum

```csharp
internal enum BinaryTypeEnum 
{
	public int value__; 
	public const BinaryTypeEnum Primitive = 0;
	public const BinaryTypeEnum String = 1;
	public const BinaryTypeEnum Object = 2;
	public const BinaryTypeEnum ObjectUrt = 3;
	public const BinaryTypeEnum ObjectUser = 4;
	public const BinaryTypeEnum ObjectArray = 5;
	public const BinaryTypeEnum StringArray = 6;
	public const BinaryTypeEnum PrimitiveArray = 7;
}
```

---

### internal enum BinaryArrayTypeEnum

```csharp
internal enum BinaryArrayTypeEnum 
{
	public int value__; 
	public const BinaryArrayTypeEnum Single = 0;
	public const BinaryArrayTypeEnum Jagged = 1;
	public const BinaryArrayTypeEnum Rectangular = 2;
	public const BinaryArrayTypeEnum SingleOffset = 3;
	public const BinaryArrayTypeEnum JaggedOffset = 4;
	public const BinaryArrayTypeEnum RectangularOffset = 5;
}
```

---

### internal enum InternalSerializerTypeE

```csharp
internal enum InternalSerializerTypeE 
{
	public int value__; 
	public const InternalSerializerTypeE Soap = 1;
	public const InternalSerializerTypeE Binary = 2;
}
```

---

### internal enum InternalParseTypeE

```csharp
internal enum InternalParseTypeE 
{
	public int value__; 
	public const InternalParseTypeE Empty = 0;
	public const InternalParseTypeE SerializedStreamHeader = 1;
	public const InternalParseTypeE Object = 2;
	public const InternalParseTypeE Member = 3;
	public const InternalParseTypeE ObjectEnd = 4;
	public const InternalParseTypeE MemberEnd = 5;
	public const InternalParseTypeE Headers = 6;
	public const InternalParseTypeE HeadersEnd = 7;
	public const InternalParseTypeE SerializedStreamHeaderEnd = 8;
	public const InternalParseTypeE Envelope = 9;
	public const InternalParseTypeE EnvelopeEnd = 10;
	public const InternalParseTypeE Body = 11;
	public const InternalParseTypeE BodyEnd = 12;
}
```

---

### internal enum InternalObjectTypeE

```csharp
internal enum InternalObjectTypeE 
{
	public int value__; 
	public const InternalObjectTypeE Empty = 0;
	public const InternalObjectTypeE Object = 1;
	public const InternalObjectTypeE Array = 2;
}
```

---

### internal enum InternalObjectPositionE

```csharp
internal enum InternalObjectPositionE 
{
	public int value__; 
	public const InternalObjectPositionE Empty = 0;
	public const InternalObjectPositionE Top = 1;
	public const InternalObjectPositionE Child = 2;
	public const InternalObjectPositionE Headers = 3;
}
```

---

### internal enum InternalArrayTypeE

```csharp
internal enum InternalArrayTypeE 
{
	public int value__; 
	public const InternalArrayTypeE Empty = 0;
	public const InternalArrayTypeE Single = 1;
	public const InternalArrayTypeE Jagged = 2;
	public const InternalArrayTypeE Rectangular = 3;
	public const InternalArrayTypeE Base64 = 4;
}
```

---

### internal enum InternalMemberTypeE

```csharp
internal enum InternalMemberTypeE 
{
	public int value__; 
	public const InternalMemberTypeE Empty = 0;
	public const InternalMemberTypeE Header = 1;
	public const InternalMemberTypeE Field = 2;
	public const InternalMemberTypeE Item = 3;
}
```

---

### internal enum InternalMemberValueE

```csharp
internal enum InternalMemberValueE 
{
	public int value__; 
	public const InternalMemberValueE Empty = 0;
	public const InternalMemberValueE InlineValue = 1;
	public const InternalMemberValueE Nested = 2;
	public const InternalMemberValueE Reference = 3;
	public const InternalMemberValueE Null = 4;
}
```

---

### internal enum InternalPrimitiveTypeE

```csharp
internal enum InternalPrimitiveTypeE 
{
	public int value__; 
	public const InternalPrimitiveTypeE Invalid = 0;
	public const InternalPrimitiveTypeE Boolean = 1;
	public const InternalPrimitiveTypeE Byte = 2;
	public const InternalPrimitiveTypeE Char = 3;
	public const InternalPrimitiveTypeE Currency = 4;
	public const InternalPrimitiveTypeE Decimal = 5;
	public const InternalPrimitiveTypeE Double = 6;
	public const InternalPrimitiveTypeE Int16 = 7;
	public const InternalPrimitiveTypeE Int32 = 8;
	public const InternalPrimitiveTypeE Int64 = 9;
	public const InternalPrimitiveTypeE SByte = 10;
	public const InternalPrimitiveTypeE Single = 11;
	public const InternalPrimitiveTypeE TimeSpan = 12;
	public const InternalPrimitiveTypeE DateTime = 13;
	public const InternalPrimitiveTypeE UInt16 = 14;
	public const InternalPrimitiveTypeE UInt32 = 15;
	public const InternalPrimitiveTypeE UInt64 = 16;
	public const InternalPrimitiveTypeE Null = 17;
	public const InternalPrimitiveTypeE String = 18;
}
```

---

### internal enum MessageEnum

```csharp
internal enum MessageEnum 
{
	public int value__; 
	public const MessageEnum NoArgs = 1;
	public const MessageEnum ArgsInline = 2;
	public const MessageEnum ArgsIsArray = 4;
	public const MessageEnum ArgsInArray = 8;
	public const MessageEnum NoContext = 16;
	public const MessageEnum ContextInline = 32;
	public const MessageEnum ContextInArray = 64;
	public const MessageEnum MethodSignatureInArray = 128;
	public const MessageEnum PropertyInArray = 256;
	public const MessageEnum NoReturnValue = 512;
	public const MessageEnum ReturnValueVoid = 1024;
	public const MessageEnum ReturnValueInline = 2048;
	public const MessageEnum ReturnValueInArray = 4096;
	public const MessageEnum ExceptionInArray = 8192;
	public const MessageEnum GenericMethod = 32768;
}
```

---

### internal enum ValueFixupEnum

```csharp
internal enum ValueFixupEnum 
{
	public int value__; 
	public const ValueFixupEnum Empty = 0;
	public const ValueFixupEnum Array = 1;
	public const ValueFixupEnum Header = 2;
	public const ValueFixupEnum Member = 3;
}
```

---

### public enum WellKnownObjectMode

```csharp
public enum WellKnownObjectMode 
{
	public int value__; 
	public const WellKnownObjectMode Singleton = 1;
	public const WellKnownObjectMode SingleCall = 2;
}
```

---

### public enum LeaseState

```csharp
public enum LeaseState 
{
	public int value__; 
	public const LeaseState Null = 0;
	public const LeaseState Initial = 1;
	public const LeaseState Active = 2;
	public const LeaseState Renewing = 3;
	public const LeaseState Expired = 4;
}
```

---

### internal enum ArgInfoType

```csharp
internal enum ArgInfoType 
{
	public byte value__; 
	public const ArgInfoType In = 0;
	public const ArgInfoType Out = 1;
}
```

---

### internal enum CallType

```csharp
internal enum CallType 
{
	public int value__; 
	public const CallType Sync = 0;
	public const CallType BeginInvoke = 1;
	public const CallType EndInvoke = 2;
	public const CallType OneWay = 3;
}
```

---

### public enum Consistency

```csharp
public enum Consistency 
{
	public int value__; 
	public const Consistency MayCorruptProcess = 0;
	public const Consistency MayCorruptAppDomain = 1;
	public const Consistency MayCorruptInstance = 2;
	public const Consistency WillNotCorruptState = 3;
}
```

---

### public enum Cer

```csharp
public enum Cer 
{
	public int value__; 
	public const Cer None = 0;
	public const Cer MayFail = 1;
	public const Cer Success = 2;
}
```

---

### public enum LoadHint

```csharp
public enum LoadHint 
{
	public int value__; 
	public const LoadHint Default = 0;
	public const LoadHint Always = 1;
	public const LoadHint Sometimes = 2;
}
```

---

### public enum CompilationRelaxations

```csharp
public enum CompilationRelaxations 
{
	public int value__; 
	public const CompilationRelaxations NoStringInterning = 8;
}
```

---

### public enum ComInterfaceType

```csharp
public enum ComInterfaceType 
{
	public int value__; 
	public const ComInterfaceType InterfaceIsDual = 0;
	public const ComInterfaceType InterfaceIsIUnknown = 1;
	public const ComInterfaceType InterfaceIsIDispatch = 2;
	[ComVisibleAttribute] 
	public const ComInterfaceType InterfaceIsIInspectable = 3;
}
```

---

### public enum ClassInterfaceType

```csharp
public enum ClassInterfaceType 
{
	public int value__; 
	public const ClassInterfaceType None = 0;
	public const ClassInterfaceType AutoDispatch = 1;
	public const ClassInterfaceType AutoDual = 2;
}
```

---

### public enum VarEnum

```csharp
public enum VarEnum 
{
	public int value__; 
	public const VarEnum VT_EMPTY = 0;
	public const VarEnum VT_NULL = 1;
	public const VarEnum VT_I2 = 2;
	public const VarEnum VT_I4 = 3;
	public const VarEnum VT_R4 = 4;
	public const VarEnum VT_R8 = 5;
	public const VarEnum VT_CY = 6;
	public const VarEnum VT_DATE = 7;
	public const VarEnum VT_BSTR = 8;
	public const VarEnum VT_DISPATCH = 9;
	public const VarEnum VT_ERROR = 10;
	public const VarEnum VT_BOOL = 11;
	public const VarEnum VT_VARIANT = 12;
	public const VarEnum VT_UNKNOWN = 13;
	public const VarEnum VT_DECIMAL = 14;
	public const VarEnum VT_I1 = 16;
	public const VarEnum VT_UI1 = 17;
	public const VarEnum VT_UI2 = 18;
	public const VarEnum VT_UI4 = 19;
	public const VarEnum VT_I8 = 20;
	public const VarEnum VT_UI8 = 21;
	public const VarEnum VT_INT = 22;
	public const VarEnum VT_UINT = 23;
	public const VarEnum VT_VOID = 24;
	public const VarEnum VT_HRESULT = 25;
	public const VarEnum VT_PTR = 26;
	public const VarEnum VT_SAFEARRAY = 27;
	public const VarEnum VT_CARRAY = 28;
	public const VarEnum VT_USERDEFINED = 29;
	public const VarEnum VT_LPSTR = 30;
	public const VarEnum VT_LPWSTR = 31;
	public const VarEnum VT_RECORD = 36;
	public const VarEnum VT_FILETIME = 64;
	public const VarEnum VT_BLOB = 65;
	public const VarEnum VT_STREAM = 66;
	public const VarEnum VT_STORAGE = 67;
	public const VarEnum VT_STREAMED_OBJECT = 68;
	public const VarEnum VT_STORED_OBJECT = 69;
	public const VarEnum VT_BLOB_OBJECT = 70;
	public const VarEnum VT_CF = 71;
	public const VarEnum VT_CLSID = 72;
	public const VarEnum VT_VECTOR = 4096;
	public const VarEnum VT_ARRAY = 8192;
	public const VarEnum VT_BYREF = 16384;
}
```

---

### public enum UnmanagedType

```csharp
public enum UnmanagedType 
{
	public int value__; 
	public const UnmanagedType Bool = 2;
	public const UnmanagedType I1 = 3;
	public const UnmanagedType U1 = 4;
	public const UnmanagedType I2 = 5;
	public const UnmanagedType U2 = 6;
	public const UnmanagedType I4 = 7;
	public const UnmanagedType U4 = 8;
	public const UnmanagedType I8 = 9;
	public const UnmanagedType U8 = 10;
	public const UnmanagedType R4 = 11;
	public const UnmanagedType R8 = 12;
	public const UnmanagedType Currency = 15;
	public const UnmanagedType BStr = 19;
	public const UnmanagedType LPStr = 20;
	public const UnmanagedType LPWStr = 21;
	public const UnmanagedType LPTStr = 22;
	public const UnmanagedType ByValTStr = 23;
	public const UnmanagedType IUnknown = 25;
	public const UnmanagedType IDispatch = 26;
	public const UnmanagedType Struct = 27;
	public const UnmanagedType Interface = 28;
	public const UnmanagedType SafeArray = 29;
	public const UnmanagedType ByValArray = 30;
	public const UnmanagedType SysInt = 31;
	public const UnmanagedType SysUInt = 32;
	public const UnmanagedType VBByRefStr = 34;
	public const UnmanagedType AnsiBStr = 35;
	public const UnmanagedType TBStr = 36;
	public const UnmanagedType VariantBool = 37;
	public const UnmanagedType FunctionPtr = 38;
	public const UnmanagedType AsAny = 40;
	public const UnmanagedType LPArray = 42;
	public const UnmanagedType LPStruct = 43;
	public const UnmanagedType CustomMarshaler = 44;
	public const UnmanagedType Error = 45;
	[ComVisibleAttribute] 
	public const UnmanagedType IInspectable = 46;
	[ComVisibleAttribute] 
	public const UnmanagedType HString = 47;
	[ComVisibleAttribute] 
	public const UnmanagedType LPUTF8Str = 48;
}
```

---

### public enum DllImportSearchPath

```csharp
public enum DllImportSearchPath 
{
	public int value__; 
	public const DllImportSearchPath UseDllDirectoryForDependencies = 256;
	public const DllImportSearchPath ApplicationDirectory = 512;
	public const DllImportSearchPath UserDirectories = 1024;
	public const DllImportSearchPath System32 = 2048;
	public const DllImportSearchPath SafeDirectories = 4096;
	public const DllImportSearchPath AssemblyDirectory = 2;
	public const DllImportSearchPath LegacyBehavior = 0;
}
```

---

### public enum CallingConvention

```csharp
public enum CallingConvention 
{
	public int value__; 
	public const CallingConvention Winapi = 1;
	public const CallingConvention Cdecl = 2;
	public const CallingConvention StdCall = 3;
	public const CallingConvention ThisCall = 4;
	public const CallingConvention FastCall = 5;
}
```

---

### public enum CharSet

```csharp
public enum CharSet 
{
	public int value__; 
	public const CharSet None = 1;
	public const CharSet Ansi = 2;
	public const CharSet Unicode = 3;
	public const CharSet Auto = 4;
}
```

---

### public enum GCHandleType

```csharp
public enum GCHandleType 
{
	public int value__; 
	public const GCHandleType Weak = 0;
	public const GCHandleType WeakTrackResurrection = 1;
	public const GCHandleType Normal = 2;
	public const GCHandleType Pinned = 3;
}
```

---

### internal enum InsertionBehavior

```csharp
internal enum InsertionBehavior 
{
	public byte value__; 
	public const InsertionBehavior None = 0;
	public const InsertionBehavior OverwriteExisting = 1;
	public const InsertionBehavior ThrowOnExisting = 2;
}
```

---

### public enum DebuggableAttribute.DebuggingModes

```csharp
public enum DebuggableAttribute.DebuggingModes 
{
	public int value__; 
	public const DebuggableAttribute.DebuggingModes None = 0;
	public const DebuggableAttribute.DebuggingModes Default = 1;
	public const DebuggableAttribute.DebuggingModes DisableOptimizations = 256;
	public const DebuggableAttribute.DebuggingModes IgnoreSymbolStoreSequencePoints = 2;
	public const DebuggableAttribute.DebuggingModes EnableEditAndContinue = 4;
}
```

---

### public enum DebuggerBrowsableState

```csharp
public enum DebuggerBrowsableState 
{
	public int value__; 
	public const DebuggerBrowsableState Never = 0;
	public const DebuggerBrowsableState Collapsed = 2;
	public const DebuggerBrowsableState RootHidden = 3;
}
```

---

### internal enum StackTrace.TraceFormat

```csharp
internal enum StackTrace.TraceFormat 
{
	public int value__; 
	public const StackTrace.TraceFormat Normal = 0;
	public const StackTrace.TraceFormat TrailingNewLine = 1;
	public const StackTrace.TraceFormat NoResourceLookup = 2;
}
```

---

### public enum EventFieldTags

```csharp
public enum EventFieldTags 
{
	public int value__; 
	public const EventFieldTags None = 0;
}
```

---

### public enum EventFieldFormat

```csharp
public enum EventFieldFormat 
{
	public int value__; 
	public const EventFieldFormat Default = 0;
	public const EventFieldFormat String = 2;
	public const EventFieldFormat Boolean = 3;
	public const EventFieldFormat Hexadecimal = 4;
	public const EventFieldFormat Xml = 11;
	public const EventFieldFormat Json = 12;
	public const EventFieldFormat HResult = 15;
}
```

---

### internal enum TraceLoggingDataType

```csharp
internal enum TraceLoggingDataType 
{
	public int value__; 
	public const TraceLoggingDataType Nil = 0;
	public const TraceLoggingDataType Utf16String = 1;
	public const TraceLoggingDataType MbcsString = 2;
	public const TraceLoggingDataType Int8 = 3;
	public const TraceLoggingDataType UInt8 = 4;
	public const TraceLoggingDataType Int16 = 5;
	public const TraceLoggingDataType UInt16 = 6;
	public const TraceLoggingDataType Int32 = 7;
	public const TraceLoggingDataType UInt32 = 8;
	public const TraceLoggingDataType Int64 = 9;
	public const TraceLoggingDataType UInt64 = 10;
	public const TraceLoggingDataType Float = 11;
	public const TraceLoggingDataType Double = 12;
	public const TraceLoggingDataType Boolean32 = 13;
	public const TraceLoggingDataType Binary = 14;
	public const TraceLoggingDataType Guid = 15;
	public const TraceLoggingDataType FileTime = 17;
	public const TraceLoggingDataType SystemTime = 18;
	public const TraceLoggingDataType HexInt32 = 20;
	public const TraceLoggingDataType HexInt64 = 21;
	public const TraceLoggingDataType CountedUtf16String = 22;
	public const TraceLoggingDataType CountedMbcsString = 23;
	public const TraceLoggingDataType Struct = 24;
	public const TraceLoggingDataType Char16 = 518;
	public const TraceLoggingDataType Char8 = 516;
	public const TraceLoggingDataType Boolean8 = 772;
	public const TraceLoggingDataType HexInt8 = 1028;
	public const TraceLoggingDataType HexInt16 = 1030;
	public const TraceLoggingDataType Utf16Xml = 2817;
	public const TraceLoggingDataType MbcsXml = 2818;
	public const TraceLoggingDataType CountedUtf16Xml = 2838;
	public const TraceLoggingDataType CountedMbcsXml = 2839;
	public const TraceLoggingDataType Utf16Json = 3073;
	public const TraceLoggingDataType MbcsJson = 3074;
	public const TraceLoggingDataType CountedUtf16Json = 3094;
	public const TraceLoggingDataType CountedMbcsJson = 3095;
	public const TraceLoggingDataType HResult = 3847;
}
```

---

### public enum EventTags

```csharp
public enum EventTags 
{
	public int value__; 
	public const EventTags None = 0;
}
```

---

### public enum EventActivityOptions

```csharp
public enum EventActivityOptions 
{
	public int value__; 
	public const EventActivityOptions None = 0;
	public const EventActivityOptions Disable = 2;
	public const EventActivityOptions Recursive = 4;
	public const EventActivityOptions Detachable = 8;
}
```

---

### internal enum ControllerCommand

```csharp
internal enum ControllerCommand 
{
	public int value__; 
	public const ControllerCommand Update = 0;
	public const ControllerCommand SendManifest = -1;
	public const ControllerCommand Enable = -2;
	public const ControllerCommand Disable = -3;
}
```

---

### public enum EventProvider.WriteEventErrorCode

```csharp
public enum EventProvider.WriteEventErrorCode 
{
	public int value__; 
	public const EventProvider.WriteEventErrorCode NoError = 0;
	public const EventProvider.WriteEventErrorCode NoFreeBuffers = 1;
	public const EventProvider.WriteEventErrorCode EventTooBig = 2;
	public const EventProvider.WriteEventErrorCode NullInput = 3;
	public const EventProvider.WriteEventErrorCode TooManyArgs = 4;
	public const EventProvider.WriteEventErrorCode Other = 5;
}
```

---

### public enum EventSourceSettings

```csharp
public enum EventSourceSettings 
{
	public int value__; 
	public const EventSourceSettings Default = 0;
	public const EventSourceSettings ThrowOnEventWriteErrors = 1;
	public const EventSourceSettings EtwManifestEventFormat = 4;
	public const EventSourceSettings EtwSelfDescribingEventFormat = 8;
}
```

---

### public enum EventCommand

```csharp
public enum EventCommand 
{
	public int value__; 
	public const EventCommand Update = 0;
	public const EventCommand SendManifest = -1;
	public const EventCommand Enable = -2;
	public const EventCommand Disable = -3;
}
```

---

### public enum EventManifestOptions

```csharp
public enum EventManifestOptions 
{
	public int value__; 
	public const EventManifestOptions None = 0;
	public const EventManifestOptions Strict = 1;
	public const EventManifestOptions AllCultures = 2;
	public const EventManifestOptions OnlyIfNeededForRegistration = 4;
	public const EventManifestOptions AllowEventSourceOverride = 8;
}
```

---

### public enum ManifestEnvelope.ManifestFormats

```csharp
public enum ManifestEnvelope.ManifestFormats 
{
	public byte value__; 
	public const ManifestEnvelope.ManifestFormats SimpleXmlFormat = 1;
}
```

---

### public enum EventLevel

```csharp
public enum EventLevel 
{
	public int value__; 
	public const EventLevel LogAlways = 0;
	public const EventLevel Critical = 1;
	public const EventLevel Error = 2;
	public const EventLevel Warning = 3;
	public const EventLevel Informational = 4;
	public const EventLevel Verbose = 5;
}
```

---

### public enum EventTask

```csharp
public enum EventTask 
{
	public int value__; 
	public const EventTask None = 0;
}
```

---

### public enum EventOpcode

```csharp
public enum EventOpcode 
{
	public int value__; 
	public const EventOpcode Info = 0;
	public const EventOpcode Start = 1;
	public const EventOpcode Stop = 2;
	public const EventOpcode DataCollectionStart = 3;
	public const EventOpcode DataCollectionStop = 4;
	public const EventOpcode Extension = 5;
	public const EventOpcode Reply = 6;
	public const EventOpcode Resume = 7;
	public const EventOpcode Suspend = 8;
	public const EventOpcode Send = 9;
	public const EventOpcode Receive = 240;
}
```

---

### public enum EventChannel

```csharp
public enum EventChannel 
{
	public byte value__; 
	public const EventChannel None = 0;
	public const EventChannel Admin = 16;
	public const EventChannel Operational = 17;
	public const EventChannel Analytic = 18;
	public const EventChannel Debug = 19;
}
```

---

### public enum EventKeywords

```csharp
public enum EventKeywords 
{
	public long value__; 
	public const EventKeywords None = 0;
	public const EventKeywords All = -1;
	public const EventKeywords MicrosoftTelemetry = 562949953421312;
	public const EventKeywords WdiContext = 562949953421312;
	public const EventKeywords WdiDiagnostic = 1125899906842624;
	public const EventKeywords Sqm = 2251799813685248;
	public const EventKeywords AuditFailure = 4503599627370496;
	public const EventKeywords AuditSuccess = 9007199254740992;
	public const EventKeywords CorrelationHint = 4503599627370496;
	public const EventKeywords EventLogClassic = 36028797018963968;
}
```

---

### public enum ConfigurationSaveMode

```csharp
public enum ConfigurationSaveMode 
{
	public int value__; 
	public const ConfigurationSaveMode Full = 2;
	public const ConfigurationSaveMode Minimal = 1;
	public const ConfigurationSaveMode Modified = 0;
}
```

---

### public enum XmlNodeType

```csharp
public enum XmlNodeType 
{
	public int value__; 
	public const XmlNodeType None = 0;
	public const XmlNodeType Element = 1;
	public const XmlNodeType Attribute = 2;
	public const XmlNodeType Text = 3;
	public const XmlNodeType CDATA = 4;
	public const XmlNodeType EntityReference = 5;
	public const XmlNodeType Entity = 6;
	public const XmlNodeType ProcessingInstruction = 7;
	public const XmlNodeType Comment = 8;
	public const XmlNodeType Document = 9;
	public const XmlNodeType DocumentType = 10;
	public const XmlNodeType DocumentFragment = 11;
	public const XmlNodeType Notation = 12;
	public const XmlNodeType Whitespace = 13;
	public const XmlNodeType SignificantWhitespace = 14;
	public const XmlNodeType EndElement = 15;
	public const XmlNodeType EndEntity = 16;
	public const XmlNodeType XmlDeclaration = 17;
}
```

---

### public enum UriKind

```csharp
public enum UriKind 
{
	public int value__; 
	public const UriKind RelativeOrAbsolute = 0;
	public const UriKind Absolute = 1;
	public const UriKind Relative = 2;
}
```

---

### public enum UriComponents

```csharp
public enum UriComponents 
{
	public int value__; 
	public const UriComponents Scheme = 1;
	public const UriComponents UserInfo = 2;
	public const UriComponents Host = 4;
	public const UriComponents Port = 8;
	public const UriComponents Path = 16;
	public const UriComponents Query = 32;
	public const UriComponents Fragment = 64;
	public const UriComponents StrongPort = 128;
	public const UriComponents NormalizedHost = 256;
	public const UriComponents KeepDelimiter = 1073741824;
	public const UriComponents SerializationInfoString = -2147483648;
	public const UriComponents AbsoluteUri = 127;
	public const UriComponents HostAndPort = 132;
	public const UriComponents StrongAuthority = 134;
	public const UriComponents SchemeAndServer = 13;
	public const UriComponents HttpRequestUrl = 61;
	public const UriComponents PathAndQuery = 48;
}
```

---

### public enum UriFormat

```csharp
public enum UriFormat 
{
	public int value__; 
	public const UriFormat UriEscaped = 1;
	public const UriFormat Unescaped = 2;
	public const UriFormat SafeUnescaped = 3;
}
```

---

### public enum UriIdnScope

```csharp
public enum UriIdnScope 
{
	public int value__; 
	public const UriIdnScope None = 0;
	public const UriIdnScope AllExceptIntranet = 1;
	public const UriIdnScope All = 2;
}
```

---

### internal enum ParsingError

```csharp
internal enum ParsingError 
{
	public int value__; 
	public const ParsingError None = 0;
	public const ParsingError BadFormat = 1;
	public const ParsingError BadScheme = 2;
	public const ParsingError BadAuthority = 3;
	public const ParsingError EmptyUriString = 4;
	public const ParsingError LastRelativeUriOkErrIndex = 4;
	public const ParsingError SchemeLimit = 5;
	public const ParsingError SizeLimit = 6;
	public const ParsingError MustRootedPath = 7;
	public const ParsingError BadHostName = 8;
	public const ParsingError NonEmptyHost = 9;
	public const ParsingError BadPort = 10;
	public const ParsingError BadAuthorityTerminator = 11;
	public const ParsingError CannotCreateRelative = 12;
}
```

---

### internal enum UnescapeMode

```csharp
internal enum UnescapeMode 
{
	public int value__; 
	public const UnescapeMode CopyOnly = 0;
	public const UnescapeMode Escape = 1;
	public const UnescapeMode Unescape = 2;
	public const UnescapeMode EscapeUnescape = 3;
	public const UnescapeMode V1ToStringFlag = 4;
	public const UnescapeMode UnescapeAll = 8;
	public const UnescapeMode UnescapeAllOrThrow = 24;
}
```

---

### internal enum UriSyntaxFlags

```csharp
internal enum UriSyntaxFlags 
{
	public int value__; 
	public const UriSyntaxFlags None = 0;
	public const UriSyntaxFlags MustHaveAuthority = 1;
	public const UriSyntaxFlags OptionalAuthority = 2;
	public const UriSyntaxFlags MayHaveUserInfo = 4;
	public const UriSyntaxFlags MayHavePort = 8;
	public const UriSyntaxFlags MayHavePath = 16;
	public const UriSyntaxFlags MayHaveQuery = 32;
	public const UriSyntaxFlags MayHaveFragment = 64;
	public const UriSyntaxFlags AllowEmptyHost = 128;
	public const UriSyntaxFlags AllowUncHost = 256;
	public const UriSyntaxFlags AllowDnsHost = 512;
	public const UriSyntaxFlags AllowIPv4Host = 1024;
	public const UriSyntaxFlags AllowIPv6Host = 2048;
	public const UriSyntaxFlags AllowAnInternetHost = 3584;
	public const UriSyntaxFlags AllowAnyOtherHost = 4096;
	public const UriSyntaxFlags FileLikeUri = 8192;
	public const UriSyntaxFlags MailToLikeUri = 16384;
	public const UriSyntaxFlags V1_UnknownUri = 65536;
	public const UriSyntaxFlags SimpleUserSyntax = 131072;
	public const UriSyntaxFlags BuiltInSyntax = 262144;
	public const UriSyntaxFlags ParserSchemeOnly = 524288;
	public const UriSyntaxFlags AllowDOSPath = 1048576;
	public const UriSyntaxFlags PathIsRooted = 2097152;
	public const UriSyntaxFlags ConvertPathSlashes = 4194304;
	public const UriSyntaxFlags CompressPath = 8388608;
	public const UriSyntaxFlags CanonicalizeAsFilePath = 16777216;
	public const UriSyntaxFlags UnEscapeDotsAndSlashes = 33554432;
	public const UriSyntaxFlags AllowIdn = 67108864;
	public const UriSyntaxFlags AllowIriParsing = 268435456;
}
```

---

### internal enum IOOperation

```csharp
internal enum IOOperation 
{
	public int value__; 
	public const IOOperation Read = 1;
	public const IOOperation Write = 2;
}
```

---

### public enum RegexOptions

```csharp
public enum RegexOptions 
{
	public int value__; 
	public const RegexOptions None = 0;
	public const RegexOptions IgnoreCase = 1;
	public const RegexOptions Multiline = 2;
	public const RegexOptions ExplicitCapture = 4;
	public const RegexOptions Compiled = 8;
	public const RegexOptions Singleline = 16;
	public const RegexOptions IgnorePatternWhitespace = 32;
	public const RegexOptions RightToLeft = 64;
	public const RegexOptions ECMAScript = 256;
	public const RegexOptions CultureInvariant = 512;
}
```

---

### public enum TraceLevel

```csharp
public enum TraceLevel 
{
	public int value__; 
	public const TraceLevel Off = 0;
	public const TraceLevel Error = 1;
	public const TraceLevel Warning = 2;
	public const TraceLevel Info = 3;
	public const TraceLevel Verbose = 4;
}
```

---

### public enum EditorBrowsableState

```csharp
public enum EditorBrowsableState 
{
	public int value__; 
	public const EditorBrowsableState Always = 0;
	public const EditorBrowsableState Never = 1;
	public const EditorBrowsableState Advanced = 2;
}
```

---

### public enum OidGroup

```csharp
public enum OidGroup 
{
	public int value__; 
	public const OidGroup All = 0;
	public const OidGroup HashAlgorithm = 1;
	public const OidGroup EncryptionAlgorithm = 2;
	public const OidGroup PublicKeyAlgorithm = 3;
	public const OidGroup SignatureAlgorithm = 4;
	public const OidGroup Attribute = 5;
	public const OidGroup ExtensionOrAttribute = 6;
	public const OidGroup EnhancedKeyUsage = 7;
	public const OidGroup Policy = 8;
	public const OidGroup Template = 9;
	public const OidGroup KeyDerivationFunction = 10;
}
```

---

### internal enum AsnDecodeStatus

```csharp
internal enum AsnDecodeStatus 
{
	public int value__; 
	public const AsnDecodeStatus NotDecoded = -1;
	public const AsnDecodeStatus Ok = 0;
	public const AsnDecodeStatus BadAsn = 1;
	public const AsnDecodeStatus BadTag = 2;
	public const AsnDecodeStatus BadLength = 3;
	public const AsnDecodeStatus InformationNotAvailable = 4;
}
```

---

### public enum X509KeyUsageFlags

```csharp
public enum X509KeyUsageFlags 
{
	public int value__; 
	public const X509KeyUsageFlags None = 0;
	public const X509KeyUsageFlags EncipherOnly = 1;
	public const X509KeyUsageFlags CrlSign = 2;
	public const X509KeyUsageFlags KeyCertSign = 4;
	public const X509KeyUsageFlags KeyAgreement = 8;
	public const X509KeyUsageFlags DataEncipherment = 16;
	public const X509KeyUsageFlags KeyEncipherment = 32;
	public const X509KeyUsageFlags NonRepudiation = 64;
	public const X509KeyUsageFlags DigitalSignature = 128;
	public const X509KeyUsageFlags DecipherOnly = 32768;
}
```

---

### public enum X509SubjectKeyIdentifierHashAlgorithm

```csharp
public enum X509SubjectKeyIdentifierHashAlgorithm 
{
	public int value__; 
	public const X509SubjectKeyIdentifierHashAlgorithm Sha1 = 0;
	public const X509SubjectKeyIdentifierHashAlgorithm ShortSha1 = 1;
	public const X509SubjectKeyIdentifierHashAlgorithm CapiSha1 = 2;
}
```

---

### public enum AddressFamily

```csharp
public enum AddressFamily 
{
	public int value__; 
	public const AddressFamily Unknown = -1;
	public const AddressFamily Unspecified = 0;
	public const AddressFamily Unix = 1;
	public const AddressFamily InterNetwork = 2;
	public const AddressFamily ImpLink = 3;
	public const AddressFamily Pup = 4;
	public const AddressFamily Chaos = 5;
	public const AddressFamily NS = 6;
	public const AddressFamily Ipx = 6;
	public const AddressFamily Iso = 7;
	public const AddressFamily Osi = 7;
	public const AddressFamily Ecma = 8;
	public const AddressFamily DataKit = 9;
	public const AddressFamily Ccitt = 10;
	public const AddressFamily Sna = 11;
	public const AddressFamily DecNet = 12;
	public const AddressFamily DataLink = 13;
	public const AddressFamily Lat = 14;
	public const AddressFamily HyperChannel = 15;
	public const AddressFamily AppleTalk = 16;
	public const AddressFamily NetBios = 17;
	public const AddressFamily VoiceView = 18;
	public const AddressFamily FireFox = 19;
	public const AddressFamily Banyan = 21;
	public const AddressFamily Atm = 22;
	public const AddressFamily InterNetworkV6 = 23;
	public const AddressFamily Cluster = 24;
	public const AddressFamily Ieee12844 = 25;
	public const AddressFamily Irda = 26;
	public const AddressFamily NetworkDesigners = 28;
	public const AddressFamily Max = 29;
}
```

---

### public enum SocketError

```csharp
public enum SocketError 
{
	public int value__; 
	public const SocketError Success = 0;
	public const SocketError SocketError = -1;
	public const SocketError Interrupted = 10004;
	public const SocketError AccessDenied = 10013;
	public const SocketError Fault = 10014;
	public const SocketError InvalidArgument = 10022;
	public const SocketError TooManyOpenSockets = 10024;
	public const SocketError WouldBlock = 10035;
	public const SocketError InProgress = 10036;
	public const SocketError AlreadyInProgress = 10037;
	public const SocketError NotSocket = 10038;
	public const SocketError DestinationAddressRequired = 10039;
	public const SocketError MessageSize = 10040;
	public const SocketError ProtocolType = 10041;
	public const SocketError ProtocolOption = 10042;
	public const SocketError ProtocolNotSupported = 10043;
	public const SocketError SocketNotSupported = 10044;
	public const SocketError OperationNotSupported = 10045;
	public const SocketError ProtocolFamilyNotSupported = 10046;
	public const SocketError AddressFamilyNotSupported = 10047;
	public const SocketError AddressAlreadyInUse = 10048;
	public const SocketError AddressNotAvailable = 10049;
	public const SocketError NetworkDown = 10050;
	public const SocketError NetworkUnreachable = 10051;
	public const SocketError NetworkReset = 10052;
	public const SocketError ConnectionAborted = 10053;
	public const SocketError ConnectionReset = 10054;
	public const SocketError NoBufferSpaceAvailable = 10055;
	public const SocketError IsConnected = 10056;
	public const SocketError NotConnected = 10057;
	public const SocketError Shutdown = 10058;
	public const SocketError TimedOut = 10060;
	public const SocketError ConnectionRefused = 10061;
	public const SocketError HostDown = 10064;
	public const SocketError HostUnreachable = 10065;
	public const SocketError ProcessLimit = 10067;
	public const SocketError SystemNotReady = 10091;
	public const SocketError VersionNotSupported = 10092;
	public const SocketError NotInitialized = 10093;
	public const SocketError Disconnecting = 10101;
	public const SocketError TypeNotFound = 10109;
	public const SocketError HostNotFound = 11001;
	public const SocketError TryAgain = 11002;
	public const SocketError NoRecovery = 11003;
	public const SocketError NoData = 11004;
	public const SocketError IOPending = 997;
	public const SocketError OperationAborted = 995;
}
```

---

### internal enum TargetType

```csharp
internal enum TargetType 
{
	public int value__; 
	public const TargetType Function = 0;
	public const TargetType Field = 1;
}
```

---

### internal enum CodegenOptions

```csharp
internal enum CodegenOptions 
{
	public int value__; 
	public const CodegenOptions Auto = 0;
	public const CodegenOptions Custom = 1;
	public const CodegenOptions Force = 2;
}
```

---

### internal enum StaticAccessorType

```csharp
internal enum StaticAccessorType 
{
	public int value__; 
	public const StaticAccessorType Dot = 0;
	public const StaticAccessorType Arrow = 1;
	public const StaticAccessorType DoubleColon = 2;
	public const StaticAccessorType ArrowWithDefaultReturnIfNull = 3;
}
```

---

### internal enum LightmapType

```csharp
internal enum LightmapType 
{
	public int value__; 
	public const LightmapType NoLightmap = -1;
	public const LightmapType StaticLightmap = 0;
	public const LightmapType DynamicLightmap = 1;
}
```

---

### public enum TypeInferenceRules

```csharp
public enum TypeInferenceRules 
{
	public int value__; 
	public const TypeInferenceRules TypeReferencedByFirstArgument = 0;
	public const TypeInferenceRules TypeReferencedBySecondArgument = 1;
	public const TypeInferenceRules ArrayOfTypeReferencedByFirstArgument = 2;
	public const TypeInferenceRules TypeOfFirstArgument = 3;
}
```

---

### public enum MarkerFlags

```csharp
public enum MarkerFlags 
{
	public ushort value__; 
	public const MarkerFlags Default = 0;
	public const MarkerFlags Script = 2;
	public const MarkerFlags ScriptInvoke = 32;
	public const MarkerFlags ScriptDeepProfiler = 64;
	public const MarkerFlags AvailabilityEditor = 4;
	public const MarkerFlags Warning = 16;
	public const MarkerFlags Counter = 128;
}
```

---

### public enum ScheduleMode

```csharp
public enum ScheduleMode 
{
	public int value__; 
	public const ScheduleMode Run = 0;
	[ObsoleteAttribute] 
	public const ScheduleMode Batched = 1;
	public const ScheduleMode Parallel = 1;
	public const ScheduleMode Single = 2;
}
```

---

### public enum FileState

```csharp
public enum FileState 
{
	public int value__; 
	public const FileState Absent = 0;
	public const FileState Exists = 1;
}
```

---

### public enum AssetLoadingSubsystem

```csharp
public enum AssetLoadingSubsystem 
{
	public int value__; 
	public const AssetLoadingSubsystem Other = 0;
	public const AssetLoadingSubsystem Texture = 1;
	public const AssetLoadingSubsystem VirtualTexture = 2;
	public const AssetLoadingSubsystem Mesh = 3;
	public const AssetLoadingSubsystem Audio = 4;
	public const AssetLoadingSubsystem Scripts = 5;
	public const AssetLoadingSubsystem EntitiesScene = 6;
	public const AssetLoadingSubsystem EntitiesStreamBinaryReader = 7;
	public const AssetLoadingSubsystem FileInfo = 8;
}
```

---

### public enum Priority

```csharp
public enum Priority 
{
	public int value__; 
	public const Priority PriorityLow = 0;
	public const Priority PriorityHigh = 1;
}
```

---

### public enum ProcessingState

```csharp
public enum ProcessingState 
{
	public int value__; 
	public const ProcessingState Unknown = 0;
	public const ProcessingState InQueue = 1;
	public const ProcessingState Reading = 2;
	public const ProcessingState Completed = 3;
	public const ProcessingState Failed = 4;
	public const ProcessingState Canceled = 5;
}
```

---

### public enum FileReadType

```csharp
public enum FileReadType 
{
	public int value__; 
	public const FileReadType Sync = 0;
	public const FileReadType Async = 1;
}
```

---

### public enum Allocator

```csharp
public enum Allocator 
{
	public int value__; 
	public const Allocator Invalid = 0;
	public const Allocator None = 1;
	public const Allocator Temp = 2;
	public const Allocator TempJob = 3;
	public const Allocator Persistent = 4;
	public const Allocator AudioKernel = 5;
}
```

---

### public enum NativeArrayOptions

```csharp
public enum NativeArrayOptions 
{
	public int value__; 
	public const NativeArrayOptions UninitializedMemory = 0;
	public const NativeArrayOptions ClearMemory = 1;
}
```

---

### public enum SendMessageOptions

```csharp
public enum SendMessageOptions 
{
	public int value__; 
	public const SendMessageOptions RequireReceiver = 0;
	public const SendMessageOptions DontRequireReceiver = 1;
}
```

---

### public enum PrimitiveType

```csharp
public enum PrimitiveType 
{
	public int value__; 
	public const PrimitiveType Sphere = 0;
	public const PrimitiveType Capsule = 1;
	public const PrimitiveType Cylinder = 2;
	public const PrimitiveType Cube = 3;
	public const PrimitiveType Plane = 4;
	public const PrimitiveType Quad = 5;
}
```

---

### public enum Space

```csharp
public enum Space 
{
	public int value__; 
	public const Space World = 0;
	public const Space Self = 1;
}
```

---

### public enum RuntimePlatform

```csharp
public enum RuntimePlatform 
{
	public int value__; 
	public const RuntimePlatform OSXEditor = 0;
	public const RuntimePlatform OSXPlayer = 1;
	public const RuntimePlatform WindowsPlayer = 2;
	[ObsoleteAttribute] 
	public const RuntimePlatform OSXWebPlayer = 3;
	[ObsoleteAttribute] 
	public const RuntimePlatform OSXDashboardPlayer = 4;
	[ObsoleteAttribute] 
	public const RuntimePlatform WindowsWebPlayer = 5;
	public const RuntimePlatform WindowsEditor = 7;
	public const RuntimePlatform IPhonePlayer = 8;
	[ObsoleteAttribute] 
	public const RuntimePlatform XBOX360 = 10;
	[ObsoleteAttribute] 
	public const RuntimePlatform PS3 = 9;
	public const RuntimePlatform Android = 11;
	[ObsoleteAttribute] 
	public const RuntimePlatform NaCl = 12;
	[ObsoleteAttribute] 
	public const RuntimePlatform FlashPlayer = 15;
	public const RuntimePlatform LinuxPlayer = 13;
	public const RuntimePlatform LinuxEditor = 16;
	public const RuntimePlatform WebGLPlayer = 17;
	[ObsoleteAttribute] 
	public const RuntimePlatform MetroPlayerX86 = 18;
	public const RuntimePlatform WSAPlayerX86 = 18;
	[ObsoleteAttribute] 
	public const RuntimePlatform MetroPlayerX64 = 19;
	public const RuntimePlatform WSAPlayerX64 = 19;
	[ObsoleteAttribute] 
	public const RuntimePlatform MetroPlayerARM = 20;
	public const RuntimePlatform WSAPlayerARM = 20;
	[ObsoleteAttribute] 
	public const RuntimePlatform WP8Player = 21;
	[ObsoleteAttribute] 
	public const RuntimePlatform BlackBerryPlayer = 22;
	[ObsoleteAttribute] 
	public const RuntimePlatform TizenPlayer = 23;
	[ObsoleteAttribute] 
	public const RuntimePlatform PSP2 = 24;
	public const RuntimePlatform PS4 = 25;
	[ObsoleteAttribute] 
	public const RuntimePlatform PSM = 26;
	public const RuntimePlatform XboxOne = 27;
	[ObsoleteAttribute] 
	public const RuntimePlatform SamsungTVPlayer = 28;
	[ObsoleteAttribute] 
	public const RuntimePlatform WiiU = 30;
	public const RuntimePlatform tvOS = 31;
	public const RuntimePlatform Switch = 32;
	public const RuntimePlatform Lumin = 33;
	public const RuntimePlatform Stadia = 34;
	public const RuntimePlatform CloudRendering = 35;
	[ObsoleteAttribute] 
	public const RuntimePlatform GameCoreScarlett = 36;
	public const RuntimePlatform GameCoreXboxSeries = 36;
	public const RuntimePlatform GameCoreXboxOne = 37;
	public const RuntimePlatform PS5 = 38;
}
```

---

### public enum LogType

```csharp
public enum LogType 
{
	public int value__; 
	public const LogType Error = 0;
	public const LogType Assert = 1;
	public const LogType Warning = 2;
	public const LogType Log = 3;
	public const LogType Exception = 4;
}
```

---

### public enum LogOption

```csharp
public enum LogOption 
{
	public int value__; 
	public const LogOption None = 0;
	public const LogOption NoStacktrace = 1;
}
```

---

### public enum Camera.StereoscopicEye

```csharp
public enum Camera.StereoscopicEye 
{
	public int value__; 
	public const Camera.StereoscopicEye Left = 0;
	public const Camera.StereoscopicEye Right = 1;
}
```

---

### public enum Camera.MonoOrStereoscopicEye

```csharp
public enum Camera.MonoOrStereoscopicEye 
{
	public int value__; 
	public const Camera.MonoOrStereoscopicEye Left = 0;
	public const Camera.MonoOrStereoscopicEye Right = 1;
	public const Camera.MonoOrStereoscopicEye Mono = 2;
}
```

---

### public enum Camera.RenderRequestMode

```csharp
public enum Camera.RenderRequestMode 
{
	public int value__; 
	public const Camera.RenderRequestMode None = 0;
	public const Camera.RenderRequestMode ObjectId = 1;
	public const Camera.RenderRequestMode Depth = 2;
	public const Camera.RenderRequestMode VertexNormal = 3;
	public const Camera.RenderRequestMode WorldPosition = 4;
	public const Camera.RenderRequestMode EntityId = 5;
	public const Camera.RenderRequestMode BaseColor = 6;
	public const Camera.RenderRequestMode SpecularColor = 7;
	public const Camera.RenderRequestMode Metallic = 8;
	public const Camera.RenderRequestMode Emission = 9;
	public const Camera.RenderRequestMode Normal = 10;
	public const Camera.RenderRequestMode Smoothness = 11;
	public const Camera.RenderRequestMode Occlusion = 12;
	public const Camera.RenderRequestMode DiffuseColor = 13;
}
```

---

### public enum Camera.RenderRequestOutputSpace

```csharp
public enum Camera.RenderRequestOutputSpace 
{
	public int value__; 
	public const Camera.RenderRequestOutputSpace ScreenSpace = -1;
	public const Camera.RenderRequestOutputSpace UV0 = 0;
	public const Camera.RenderRequestOutputSpace UV1 = 1;
	public const Camera.RenderRequestOutputSpace UV2 = 2;
	public const Camera.RenderRequestOutputSpace UV3 = 3;
	public const Camera.RenderRequestOutputSpace UV4 = 4;
	public const Camera.RenderRequestOutputSpace UV5 = 5;
	public const Camera.RenderRequestOutputSpace UV6 = 6;
	public const Camera.RenderRequestOutputSpace UV7 = 7;
	public const Camera.RenderRequestOutputSpace UV8 = 8;
}
```

---

### public enum ReflectionProbe.ReflectionProbeEvent

```csharp
public enum ReflectionProbe.ReflectionProbeEvent 
{
	public int value__; 
	public const ReflectionProbe.ReflectionProbeEvent ReflectionProbeAdded = 0;
	public const ReflectionProbe.ReflectionProbeEvent ReflectionProbeRemoved = 1;
}
```

---

### public enum FullScreenMode

```csharp
public enum FullScreenMode 
{
	public int value__; 
	public const FullScreenMode ExclusiveFullScreen = 0;
	public const FullScreenMode FullScreenWindow = 1;
	public const FullScreenMode MaximizedWindow = 2;
	public const FullScreenMode Windowed = 3;
}
```

---

### public enum ComputeBufferMode

```csharp
public enum ComputeBufferMode 
{
	public int value__; 
	public const ComputeBufferMode Immutable = 0;
	public const ComputeBufferMode Dynamic = 1;
	public const ComputeBufferMode Circular = 2;
	public const ComputeBufferMode StreamOut = 3;
	public const ComputeBufferMode SubUpdates = 4;
}
```

---

### public enum RenderingPath

```csharp
public enum RenderingPath 
{
	public int value__; 
	public const RenderingPath UsePlayerSettings = -1;
	public const RenderingPath VertexLit = 0;
	public const RenderingPath Forward = 1;
	public const RenderingPath DeferredLighting = 2;
	public const RenderingPath DeferredShading = 3;
}
```

---

### public enum TransparencySortMode

```csharp
public enum TransparencySortMode 
{
	public int value__; 
	public const TransparencySortMode Default = 0;
	public const TransparencySortMode Perspective = 1;
	public const TransparencySortMode Orthographic = 2;
	public const TransparencySortMode CustomAxis = 3;
}
```

---

### public enum StereoTargetEyeMask

```csharp
public enum StereoTargetEyeMask 
{
	public int value__; 
	public const StereoTargetEyeMask None = 0;
	public const StereoTargetEyeMask Left = 1;
	public const StereoTargetEyeMask Right = 2;
	public const StereoTargetEyeMask Both = 3;
}
```

---

### public enum CameraType

```csharp
public enum CameraType 
{
	public int value__; 
	public const CameraType Game = 1;
	public const CameraType SceneView = 2;
	public const CameraType Preview = 4;
	public const CameraType VR = 8;
	public const CameraType Reflection = 16;
}
```

---

### public enum ComputeBufferType

```csharp
public enum ComputeBufferType 
{
	public int value__; 
	public const ComputeBufferType Default = 0;
	public const ComputeBufferType Raw = 1;
	public const ComputeBufferType Append = 2;
	public const ComputeBufferType Counter = 4;
	public const ComputeBufferType Constant = 8;
	public const ComputeBufferType Structured = 16;
	[ObsoleteAttribute] 
	public const ComputeBufferType DrawIndirect = 256;
	public const ComputeBufferType IndirectArguments = 256;
	[ObsoleteAttribute] 
	public const ComputeBufferType GPUMemory = 512;
}
```

---

### public enum LightType

```csharp
public enum LightType 
{
	public int value__; 
	public const LightType Spot = 0;
	public const LightType Directional = 1;
	public const LightType Point = 2;
	public const LightType Area = 3;
	public const LightType Rectangle = 3;
	public const LightType Disc = 4;
}
```

---

### public enum LightShadows

```csharp
public enum LightShadows 
{
	public int value__; 
	public const LightShadows None = 0;
	public const LightShadows Hard = 1;
	public const LightShadows Soft = 2;
}
```

---

### public enum LightmapBakeType

```csharp
public enum LightmapBakeType 
{
	public int value__; 
	public const LightmapBakeType Realtime = 4;
	public const LightmapBakeType Baked = 2;
	public const LightmapBakeType Mixed = 1;
}
```

---

### public enum MixedLightingMode

```csharp
public enum MixedLightingMode 
{
	public int value__; 
	public const MixedLightingMode IndirectOnly = 0;
	public const MixedLightingMode Shadowmask = 2;
	public const MixedLightingMode Subtractive = 1;
}
```

---

### public enum ShadowmaskMode

```csharp
public enum ShadowmaskMode 
{
	public int value__; 
	public const ShadowmaskMode Shadowmask = 0;
	public const ShadowmaskMode DistanceShadowmask = 1;
}
```

---

### public enum CameraClearFlags

```csharp
public enum CameraClearFlags 
{
	public int value__; 
	public const CameraClearFlags Skybox = 1;
	public const CameraClearFlags Color = 2;
	public const CameraClearFlags SolidColor = 2;
	public const CameraClearFlags Depth = 3;
	public const CameraClearFlags Nothing = 4;
}
```

---

### public enum MeshTopology

```csharp
public enum MeshTopology 
{
	public int value__; 
	public const MeshTopology Triangles = 0;
	public const MeshTopology Quads = 2;
	public const MeshTopology Lines = 3;
	public const MeshTopology LineStrip = 4;
	public const MeshTopology Points = 5;
}
```

---

### public enum ColorSpace

```csharp
public enum ColorSpace 
{
	public int value__; 
	public const ColorSpace Uninitialized = -1;
	public const ColorSpace Gamma = 0;
	public const ColorSpace Linear = 1;
}
```

---

### public enum FilterMode

```csharp
public enum FilterMode 
{
	public int value__; 
	public const FilterMode Point = 0;
	public const FilterMode Bilinear = 1;
	public const FilterMode Trilinear = 2;
}
```

---

### public enum TextureWrapMode

```csharp
public enum TextureWrapMode 
{
	public int value__; 
	public const TextureWrapMode Repeat = 0;
	public const TextureWrapMode Clamp = 1;
	public const TextureWrapMode Mirror = 2;
	public const TextureWrapMode MirrorOnce = 3;
}
```

---

### public enum TextureFormat

```csharp
public enum TextureFormat 
{
	public int value__; 
	public const TextureFormat Alpha8 = 1;
	public const TextureFormat ARGB4444 = 2;
	public const TextureFormat RGB24 = 3;
	public const TextureFormat RGBA32 = 4;
	public const TextureFormat ARGB32 = 5;
	public const TextureFormat RGB565 = 7;
	public const TextureFormat R16 = 9;
	public const TextureFormat DXT1 = 10;
	public const TextureFormat DXT5 = 12;
	public const TextureFormat RGBA4444 = 13;
	public const TextureFormat BGRA32 = 14;
	public const TextureFormat RHalf = 15;
	public const TextureFormat RGHalf = 16;
	public const TextureFormat RGBAHalf = 17;
	public const TextureFormat RFloat = 18;
	public const TextureFormat RGFloat = 19;
	public const TextureFormat RGBAFloat = 20;
	public const TextureFormat YUY2 = 21;
	public const TextureFormat RGB9e5Float = 22;
	public const TextureFormat BC4 = 26;
	public const TextureFormat BC5 = 27;
	public const TextureFormat BC6H = 24;
	public const TextureFormat BC7 = 25;
	public const TextureFormat DXT1Crunched = 28;
	public const TextureFormat DXT5Crunched = 29;
	public const TextureFormat PVRTC_RGB2 = 30;
	public const TextureFormat PVRTC_RGBA2 = 31;
	public const TextureFormat PVRTC_RGB4 = 32;
	public const TextureFormat PVRTC_RGBA4 = 33;
	public const TextureFormat ETC_RGB4 = 34;
	public const TextureFormat EAC_R = 41;
	public const TextureFormat EAC_R_SIGNED = 42;
	public const TextureFormat EAC_RG = 43;
	public const TextureFormat EAC_RG_SIGNED = 44;
	public const TextureFormat ETC2_RGB = 45;
	public const TextureFormat ETC2_RGBA1 = 46;
	public const TextureFormat ETC2_RGBA8 = 47;
	public const TextureFormat ASTC_4x4 = 48;
	public const TextureFormat ASTC_5x5 = 49;
	public const TextureFormat ASTC_6x6 = 50;
	public const TextureFormat ASTC_8x8 = 51;
	public const TextureFormat ASTC_10x10 = 52;
	public const TextureFormat ASTC_12x12 = 53;
	[ObsoleteAttribute] 
	public const TextureFormat ETC_RGB4_3DS = 60;
	[ObsoleteAttribute] 
	public const TextureFormat ETC_RGBA8_3DS = 61;
	public const TextureFormat RG16 = 62;
	public const TextureFormat R8 = 63;
	public const TextureFormat ETC_RGB4Crunched = 64;
	public const TextureFormat ETC2_RGBA8Crunched = 65;
	public const TextureFormat ASTC_HDR_4x4 = 66;
	public const TextureFormat ASTC_HDR_5x5 = 67;
	public const TextureFormat ASTC_HDR_6x6 = 68;
	public const TextureFormat ASTC_HDR_8x8 = 69;
	public const TextureFormat ASTC_HDR_10x10 = 70;
	public const TextureFormat ASTC_HDR_12x12 = 71;
	public const TextureFormat RG32 = 72;
	public const TextureFormat RGB48 = 73;
	public const TextureFormat RGBA64 = 74;
	[ObsoleteAttribute] 
	[EditorBrowsableAttribute] 
	public const TextureFormat ASTC_RGB_4x4 = 48;
	[EditorBrowsableAttribute] 
	[ObsoleteAttribute] 
	public const TextureFormat ASTC_RGB_5x5 = 49;
	[ObsoleteAttribute] 
	[EditorBrowsableAttribute] 
	public const TextureFormat ASTC_RGB_6x6 = 50;
	[ObsoleteAttribute] 
	[EditorBrowsableAttribute] 
	public const TextureFormat ASTC_RGB_8x8 = 51;
	[EditorBrowsableAttribute] 
	[ObsoleteAttribute] 
	public const TextureFormat ASTC_RGB_10x10 = 52;
	[EditorBrowsableAttribute] 
	[ObsoleteAttribute] 
	public const TextureFormat ASTC_RGB_12x12 = 53;
	[ObsoleteAttribute] 
	[EditorBrowsableAttribute] 
	public const TextureFormat ASTC_RGBA_4x4 = 54;
	[EditorBrowsableAttribute] 
	[ObsoleteAttribute] 
	public const TextureFormat ASTC_RGBA_5x5 = 55;
	[ObsoleteAttribute] 
	[EditorBrowsableAttribute] 
	public const TextureFormat ASTC_RGBA_6x6 = 56;
	[EditorBrowsableAttribute] 
	[ObsoleteAttribute] 
	public const TextureFormat ASTC_RGBA_8x8 = 57;
	[EditorBrowsableAttribute] 
	[ObsoleteAttribute] 
	public const TextureFormat ASTC_RGBA_10x10 = 58;
	[ObsoleteAttribute] 
	[EditorBrowsableAttribute] 
	public const TextureFormat ASTC_RGBA_12x12 = 59;
}
```

---

### public enum CubemapFace

```csharp
public enum CubemapFace 
{
	public int value__; 
	public const CubemapFace Unknown = -1;
	public const CubemapFace PositiveX = 0;
	public const CubemapFace NegativeX = 1;
	public const CubemapFace PositiveY = 2;
	public const CubemapFace NegativeY = 3;
	public const CubemapFace PositiveZ = 4;
	public const CubemapFace NegativeZ = 5;
}
```

---

### public enum RenderTextureFormat

```csharp
public enum RenderTextureFormat 
{
	public int value__; 
	public const RenderTextureFormat ARGB32 = 0;
	public const RenderTextureFormat Depth = 1;
	public const RenderTextureFormat ARGBHalf = 2;
	public const RenderTextureFormat Shadowmap = 3;
	public const RenderTextureFormat RGB565 = 4;
	public const RenderTextureFormat ARGB4444 = 5;
	public const RenderTextureFormat ARGB1555 = 6;
	public const RenderTextureFormat Default = 7;
	public const RenderTextureFormat ARGB2101010 = 8;
	public const RenderTextureFormat DefaultHDR = 9;
	public const RenderTextureFormat ARGB64 = 10;
	public const RenderTextureFormat ARGBFloat = 11;
	public const RenderTextureFormat RGFloat = 12;
	public const RenderTextureFormat RGHalf = 13;
	public const RenderTextureFormat RFloat = 14;
	public const RenderTextureFormat RHalf = 15;
	public const RenderTextureFormat R8 = 16;
	public const RenderTextureFormat ARGBInt = 17;
	public const RenderTextureFormat RGInt = 18;
	public const RenderTextureFormat RInt = 19;
	public const RenderTextureFormat BGRA32 = 20;
	public const RenderTextureFormat RGB111110Float = 22;
	public const RenderTextureFormat RG32 = 23;
	public const RenderTextureFormat RGBAUShort = 24;
	public const RenderTextureFormat RG16 = 25;
	public const RenderTextureFormat BGRA10101010_XR = 26;
	public const RenderTextureFormat BGR101010_XR = 27;
	public const RenderTextureFormat R16 = 28;
}
```

---

### public enum VRTextureUsage

```csharp
public enum VRTextureUsage 
{
	public int value__; 
	public const VRTextureUsage None = 0;
	public const VRTextureUsage OneEye = 1;
	public const VRTextureUsage TwoEyes = 2;
	public const VRTextureUsage DeviceSpecific = 3;
}
```

---

### public enum RenderTextureCreationFlags

```csharp
public enum RenderTextureCreationFlags 
{
	public int value__; 
	public const RenderTextureCreationFlags MipMap = 1;
	public const RenderTextureCreationFlags AutoGenerateMips = 2;
	public const RenderTextureCreationFlags SRGB = 4;
	public const RenderTextureCreationFlags EyeTexture = 8;
	public const RenderTextureCreationFlags EnableRandomWrite = 16;
	public const RenderTextureCreationFlags CreatedFromScript = 32;
	public const RenderTextureCreationFlags AllowVerticalFlip = 128;
	public const RenderTextureCreationFlags NoResolvedColorSurface = 256;
	public const RenderTextureCreationFlags DynamicallyScalable = 1024;
	public const RenderTextureCreationFlags BindMS = 2048;
}
```

---

### public enum RenderTextureReadWrite

```csharp
public enum RenderTextureReadWrite 
{
	public int value__; 
	public const RenderTextureReadWrite Default = 0;
	public const RenderTextureReadWrite Linear = 1;
	public const RenderTextureReadWrite sRGB = 2;
}
```

---

### public enum RenderTextureMemoryless

```csharp
public enum RenderTextureMemoryless 
{
	public int value__; 
	public const RenderTextureMemoryless None = 0;
	public const RenderTextureMemoryless Color = 1;
	public const RenderTextureMemoryless Depth = 2;
	public const RenderTextureMemoryless MSAA = 4;
}
```

---

### public enum LightmapsMode

```csharp
public enum LightmapsMode 
{
	public int value__; 
	public const LightmapsMode NonDirectional = 0;
	public const LightmapsMode CombinedDirectional = 1;
}
```

---

### public enum CursorLockMode

```csharp
public enum CursorLockMode 
{
	public int value__; 
	public const CursorLockMode None = 0;
	public const CursorLockMode Locked = 1;
	public const CursorLockMode Confined = 2;
}
```

---

### public enum KeyCode

```csharp
public enum KeyCode 
{
	public int value__; 
	public const KeyCode None = 0;
	public const KeyCode Backspace = 8;
	public const KeyCode Delete = 127;
	public const KeyCode Tab = 9;
	public const KeyCode Clear = 12;
	public const KeyCode Return = 13;
	public const KeyCode Pause = 19;
	public const KeyCode Escape = 27;
	public const KeyCode Space = 32;
	public const KeyCode Keypad0 = 256;
	public const KeyCode Keypad1 = 257;
	public const KeyCode Keypad2 = 258;
	public const KeyCode Keypad3 = 259;
	public const KeyCode Keypad4 = 260;
	public const KeyCode Keypad5 = 261;
	public const KeyCode Keypad6 = 262;
	public const KeyCode Keypad7 = 263;
	public const KeyCode Keypad8 = 264;
	public const KeyCode Keypad9 = 265;
	public const KeyCode KeypadPeriod = 266;
	public const KeyCode KeypadDivide = 267;
	public const KeyCode KeypadMultiply = 268;
	public const KeyCode KeypadMinus = 269;
	public const KeyCode KeypadPlus = 270;
	public const KeyCode KeypadEnter = 271;
	public const KeyCode KeypadEquals = 272;
	public const KeyCode UpArrow = 273;
	public const KeyCode DownArrow = 274;
	public const KeyCode RightArrow = 275;
	public const KeyCode LeftArrow = 276;
	public const KeyCode Insert = 277;
	public const KeyCode Home = 278;
	public const KeyCode End = 279;
	public const KeyCode PageUp = 280;
	public const KeyCode PageDown = 281;
	public const KeyCode F1 = 282;
	public const KeyCode F2 = 283;
	public const KeyCode F3 = 284;
	public const KeyCode F4 = 285;
	public const KeyCode F5 = 286;
	public const KeyCode F6 = 287;
	public const KeyCode F7 = 288;
	public const KeyCode F8 = 289;
	public const KeyCode F9 = 290;
	public const KeyCode F10 = 291;
	public const KeyCode F11 = 292;
	public const KeyCode F12 = 293;
	public const KeyCode F13 = 294;
	public const KeyCode F14 = 295;
	public const KeyCode F15 = 296;
	public const KeyCode Alpha0 = 48;
	public const KeyCode Alpha1 = 49;
	public const KeyCode Alpha2 = 50;
	public const KeyCode Alpha3 = 51;
	public const KeyCode Alpha4 = 52;
	public const KeyCode Alpha5 = 53;
	public const KeyCode Alpha6 = 54;
	public const KeyCode Alpha7 = 55;
	public const KeyCode Alpha8 = 56;
	public const KeyCode Alpha9 = 57;
	public const KeyCode Exclaim = 33;
	public const KeyCode DoubleQuote = 34;
	public const KeyCode Hash = 35;
	public const KeyCode Dollar = 36;
	public const KeyCode Percent = 37;
	public const KeyCode Ampersand = 38;
	public const KeyCode Quote = 39;
	public const KeyCode LeftParen = 40;
	public const KeyCode RightParen = 41;
	public const KeyCode Asterisk = 42;
	public const KeyCode Plus = 43;
	public const KeyCode Comma = 44;
	public const KeyCode Minus = 45;
	public const KeyCode Period = 46;
	public const KeyCode Slash = 47;
	public const KeyCode Colon = 58;
	public const KeyCode Semicolon = 59;
	public const KeyCode Less = 60;
	public const KeyCode Equals = 61;
	public const KeyCode Greater = 62;
	public const KeyCode Question = 63;
	public const KeyCode At = 64;
	public const KeyCode LeftBracket = 91;
	public const KeyCode Backslash = 92;
	public const KeyCode RightBracket = 93;
	public const KeyCode Caret = 94;
	public const KeyCode Underscore = 95;
	public const KeyCode BackQuote = 96;
	public const KeyCode A = 97;
	public const KeyCode B = 98;
	public const KeyCode C = 99;
	public const KeyCode D = 100;
	public const KeyCode E = 101;
	public const KeyCode F = 102;
	public const KeyCode G = 103;
	public const KeyCode H = 104;
	public const KeyCode I = 105;
	public const KeyCode J = 106;
	public const KeyCode K = 107;
	public const KeyCode L = 108;
	public const KeyCode M = 109;
	public const KeyCode N = 110;
	public const KeyCode O = 111;
	public const KeyCode P = 112;
	public const KeyCode Q = 113;
	public const KeyCode R = 114;
	public const KeyCode S = 115;
	public const KeyCode T = 116;
	public const KeyCode U = 117;
	public const KeyCode V = 118;
	public const KeyCode W = 119;
	public const KeyCode X = 120;
	public const KeyCode Y = 121;
	public const KeyCode Z = 122;
	public const KeyCode LeftCurlyBracket = 123;
	public const KeyCode Pipe = 124;
	public const KeyCode RightCurlyBracket = 125;
	public const KeyCode Tilde = 126;
	public const KeyCode Numlock = 300;
	public const KeyCode CapsLock = 301;
	public const KeyCode ScrollLock = 302;
	public const KeyCode RightShift = 303;
	public const KeyCode LeftShift = 304;
	public const KeyCode RightControl = 305;
	public const KeyCode LeftControl = 306;
	public const KeyCode RightAlt = 307;
	public const KeyCode LeftAlt = 308;
	public const KeyCode LeftCommand = 310;
	public const KeyCode LeftApple = 310;
	public const KeyCode LeftWindows = 311;
	public const KeyCode RightCommand = 309;
	public const KeyCode RightApple = 309;
	public const KeyCode RightWindows = 312;
	public const KeyCode AltGr = 313;
	public const KeyCode Help = 315;
	public const KeyCode Print = 316;
	public const KeyCode SysReq = 317;
	public const KeyCode Break = 318;
	public const KeyCode Menu = 319;
	public const KeyCode Mouse0 = 323;
	public const KeyCode Mouse1 = 324;
	public const KeyCode Mouse2 = 325;
	public const KeyCode Mouse3 = 326;
	public const KeyCode Mouse4 = 327;
	public const KeyCode Mouse5 = 328;
	public const KeyCode Mouse6 = 329;
	public const KeyCode JoystickButton0 = 330;
	public const KeyCode JoystickButton1 = 331;
	public const KeyCode JoystickButton2 = 332;
	public const KeyCode JoystickButton3 = 333;
	public const KeyCode JoystickButton4 = 334;
	public const KeyCode JoystickButton5 = 335;
	public const KeyCode JoystickButton6 = 336;
	public const KeyCode JoystickButton7 = 337;
	public const KeyCode JoystickButton8 = 338;
	public const KeyCode JoystickButton9 = 339;
	public const KeyCode JoystickButton10 = 340;
	public const KeyCode JoystickButton11 = 341;
	public const KeyCode JoystickButton12 = 342;
	public const KeyCode JoystickButton13 = 343;
	public const KeyCode JoystickButton14 = 344;
	public const KeyCode JoystickButton15 = 345;
	public const KeyCode JoystickButton16 = 346;
	public const KeyCode JoystickButton17 = 347;
	public const KeyCode JoystickButton18 = 348;
	public const KeyCode JoystickButton19 = 349;
	public const KeyCode Joystick1Button0 = 350;
	public const KeyCode Joystick1Button1 = 351;
	public const KeyCode Joystick1Button2 = 352;
	public const KeyCode Joystick1Button3 = 353;
	public const KeyCode Joystick1Button4 = 354;
	public const KeyCode Joystick1Button5 = 355;
	public const KeyCode Joystick1Button6 = 356;
	public const KeyCode Joystick1Button7 = 357;
	public const KeyCode Joystick1Button8 = 358;
	public const KeyCode Joystick1Button9 = 359;
	public const KeyCode Joystick1Button10 = 360;
	public const KeyCode Joystick1Button11 = 361;
	public const KeyCode Joystick1Button12 = 362;
	public const KeyCode Joystick1Button13 = 363;
	public const KeyCode Joystick1Button14 = 364;
	public const KeyCode Joystick1Button15 = 365;
	public const KeyCode Joystick1Button16 = 366;
	public const KeyCode Joystick1Button17 = 367;
	public const KeyCode Joystick1Button18 = 368;
	public const KeyCode Joystick1Button19 = 369;
	public const KeyCode Joystick2Button0 = 370;
	public const KeyCode Joystick2Button1 = 371;
	public const KeyCode Joystick2Button2 = 372;
	public const KeyCode Joystick2Button3 = 373;
	public const KeyCode Joystick2Button4 = 374;
	public const KeyCode Joystick2Button5 = 375;
	public const KeyCode Joystick2Button6 = 376;
	public const KeyCode Joystick2Button7 = 377;
	public const KeyCode Joystick2Button8 = 378;
	public const KeyCode Joystick2Button9 = 379;
	public const KeyCode Joystick2Button10 = 380;
	public const KeyCode Joystick2Button11 = 381;
	public const KeyCode Joystick2Button12 = 382;
	public const KeyCode Joystick2Button13 = 383;
	public const KeyCode Joystick2Button14 = 384;
	public const KeyCode Joystick2Button15 = 385;
	public const KeyCode Joystick2Button16 = 386;
	public const KeyCode Joystick2Button17 = 387;
	public const KeyCode Joystick2Button18 = 388;
	public const KeyCode Joystick2Button19 = 389;
	public const KeyCode Joystick3Button0 = 390;
	public const KeyCode Joystick3Button1 = 391;
	public const KeyCode Joystick3Button2 = 392;
	public const KeyCode Joystick3Button3 = 393;
	public const KeyCode Joystick3Button4 = 394;
	public const KeyCode Joystick3Button5 = 395;
	public const KeyCode Joystick3Button6 = 396;
	public const KeyCode Joystick3Button7 = 397;
	public const KeyCode Joystick3Button8 = 398;
	public const KeyCode Joystick3Button9 = 399;
	public const KeyCode Joystick3Button10 = 400;
	public const KeyCode Joystick3Button11 = 401;
	public const KeyCode Joystick3Button12 = 402;
	public const KeyCode Joystick3Button13 = 403;
	public const KeyCode Joystick3Button14 = 404;
	public const KeyCode Joystick3Button15 = 405;
	public const KeyCode Joystick3Button16 = 406;
	public const KeyCode Joystick3Button17 = 407;
	public const KeyCode Joystick3Button18 = 408;
	public const KeyCode Joystick3Button19 = 409;
	public const KeyCode Joystick4Button0 = 410;
	public const KeyCode Joystick4Button1 = 411;
	public const KeyCode Joystick4Button2 = 412;
	public const KeyCode Joystick4Button3 = 413;
	public const KeyCode Joystick4Button4 = 414;
	public const KeyCode Joystick4Button5 = 415;
	public const KeyCode Joystick4Button6 = 416;
	public const KeyCode Joystick4Button7 = 417;
	public const KeyCode Joystick4Button8 = 418;
	public const KeyCode Joystick4Button9 = 419;
	public const KeyCode Joystick4Button10 = 420;
	public const KeyCode Joystick4Button11 = 421;
	public const KeyCode Joystick4Button12 = 422;
	public const KeyCode Joystick4Button13 = 423;
	public const KeyCode Joystick4Button14 = 424;
	public const KeyCode Joystick4Button15 = 425;
	public const KeyCode Joystick4Button16 = 426;
	public const KeyCode Joystick4Button17 = 427;
	public const KeyCode Joystick4Button18 = 428;
	public const KeyCode Joystick4Button19 = 429;
	public const KeyCode Joystick5Button0 = 430;
	public const KeyCode Joystick5Button1 = 431;
	public const KeyCode Joystick5Button2 = 432;
	public const KeyCode Joystick5Button3 = 433;
	public const KeyCode Joystick5Button4 = 434;
	public const KeyCode Joystick5Button5 = 435;
	public const KeyCode Joystick5Button6 = 436;
	public const KeyCode Joystick5Button7 = 437;
	public const KeyCode Joystick5Button8 = 438;
	public const KeyCode Joystick5Button9 = 439;
	public const KeyCode Joystick5Button10 = 440;
	public const KeyCode Joystick5Button11 = 441;
	public const KeyCode Joystick5Button12 = 442;
	public const KeyCode Joystick5Button13 = 443;
	public const KeyCode Joystick5Button14 = 444;
	public const KeyCode Joystick5Button15 = 445;
	public const KeyCode Joystick5Button16 = 446;
	public const KeyCode Joystick5Button17 = 447;
	public const KeyCode Joystick5Button18 = 448;
	public const KeyCode Joystick5Button19 = 449;
	public const KeyCode Joystick6Button0 = 450;
	public const KeyCode Joystick6Button1 = 451;
	public const KeyCode Joystick6Button2 = 452;
	public const KeyCode Joystick6Button3 = 453;
	public const KeyCode Joystick6Button4 = 454;
	public const KeyCode Joystick6Button5 = 455;
	public const KeyCode Joystick6Button6 = 456;
	public const KeyCode Joystick6Button7 = 457;
	public const KeyCode Joystick6Button8 = 458;
	public const KeyCode Joystick6Button9 = 459;
	public const KeyCode Joystick6Button10 = 460;
	public const KeyCode Joystick6Button11 = 461;
	public const KeyCode Joystick6Button12 = 462;
	public const KeyCode Joystick6Button13 = 463;
	public const KeyCode Joystick6Button14 = 464;
	public const KeyCode Joystick6Button15 = 465;
	public const KeyCode Joystick6Button16 = 466;
	public const KeyCode Joystick6Button17 = 467;
	public const KeyCode Joystick6Button18 = 468;
	public const KeyCode Joystick6Button19 = 469;
	public const KeyCode Joystick7Button0 = 470;
	public const KeyCode Joystick7Button1 = 471;
	public const KeyCode Joystick7Button2 = 472;
	public const KeyCode Joystick7Button3 = 473;
	public const KeyCode Joystick7Button4 = 474;
	public const KeyCode Joystick7Button5 = 475;
	public const KeyCode Joystick7Button6 = 476;
	public const KeyCode Joystick7Button7 = 477;
	public const KeyCode Joystick7Button8 = 478;
	public const KeyCode Joystick7Button9 = 479;
	public const KeyCode Joystick7Button10 = 480;
	public const KeyCode Joystick7Button11 = 481;
	public const KeyCode Joystick7Button12 = 482;
	public const KeyCode Joystick7Button13 = 483;
	public const KeyCode Joystick7Button14 = 484;
	public const KeyCode Joystick7Button15 = 485;
	public const KeyCode Joystick7Button16 = 486;
	public const KeyCode Joystick7Button17 = 487;
	public const KeyCode Joystick7Button18 = 488;
	public const KeyCode Joystick7Button19 = 489;
	public const KeyCode Joystick8Button0 = 490;
	public const KeyCode Joystick8Button1 = 491;
	public const KeyCode Joystick8Button2 = 492;
	public const KeyCode Joystick8Button3 = 493;
	public const KeyCode Joystick8Button4 = 494;
	public const KeyCode Joystick8Button5 = 495;
	public const KeyCode Joystick8Button6 = 496;
	public const KeyCode Joystick8Button7 = 497;
	public const KeyCode Joystick8Button8 = 498;
	public const KeyCode Joystick8Button9 = 499;
	public const KeyCode Joystick8Button10 = 500;
	public const KeyCode Joystick8Button11 = 501;
	public const KeyCode Joystick8Button12 = 502;
	public const KeyCode Joystick8Button13 = 503;
	public const KeyCode Joystick8Button14 = 504;
	public const KeyCode Joystick8Button15 = 505;
	public const KeyCode Joystick8Button16 = 506;
	public const KeyCode Joystick8Button17 = 507;
	public const KeyCode Joystick8Button18 = 508;
	public const KeyCode Joystick8Button19 = 509;
}
```

---

### public enum RuntimeInitializeLoadType

```csharp
public enum RuntimeInitializeLoadType 
{
	public int value__; 
	public const RuntimeInitializeLoadType AfterSceneLoad = 0;
	public const RuntimeInitializeLoadType BeforeSceneLoad = 1;
	public const RuntimeInitializeLoadType AfterAssembliesLoaded = 2;
	public const RuntimeInitializeLoadType BeforeSplashScreen = 3;
	public const RuntimeInitializeLoadType SubsystemRegistration = 4;
}
```

---

### public enum HideFlags

```csharp
public enum HideFlags 
{
	public int value__; 
	public const HideFlags None = 0;
	public const HideFlags HideInHierarchy = 1;
	public const HideFlags HideInInspector = 2;
	public const HideFlags DontSaveInEditor = 4;
	public const HideFlags NotEditable = 8;
	public const HideFlags DontSaveInBuild = 16;
	public const HideFlags DontUnloadUnusedAsset = 32;
	public const HideFlags DontSave = 52;
	public const HideFlags HideAndDontSave = 61;
}
```

---

### internal enum DisableBatchingType

```csharp
internal enum DisableBatchingType 
{
	public int value__; 
	public const DisableBatchingType False = 0;
	public const DisableBatchingType True = 1;
	public const DisableBatchingType WhenLODFading = 2;
}
```

---

### public enum OperatingSystemFamily

```csharp
public enum OperatingSystemFamily 
{
	public int value__; 
	public const OperatingSystemFamily Other = 0;
	public const OperatingSystemFamily MacOSX = 1;
	public const OperatingSystemFamily Windows = 2;
	public const OperatingSystemFamily Linux = 3;
}
```

---

### public enum DeviceType

```csharp
public enum DeviceType 
{
	public int value__; 
	public const DeviceType Unknown = 0;
	public const DeviceType Handheld = 1;
	public const DeviceType Console = 2;
	public const DeviceType Desktop = 3;
}
```

---

### public enum TouchScreenKeyboard.Status

```csharp
public enum TouchScreenKeyboard.Status 
{
	public int value__; 
	public const TouchScreenKeyboard.Status Visible = 0;
	public const TouchScreenKeyboard.Status Done = 1;
	public const TouchScreenKeyboard.Status Canceled = 2;
	public const TouchScreenKeyboard.Status LostFocus = 3;
}
```

---

### public enum TouchScreenKeyboardType

```csharp
public enum TouchScreenKeyboardType 
{
	public int value__; 
	public const TouchScreenKeyboardType Default = 0;
	public const TouchScreenKeyboardType ASCIICapable = 1;
	public const TouchScreenKeyboardType NumbersAndPunctuation = 2;
	public const TouchScreenKeyboardType URL = 3;
	public const TouchScreenKeyboardType NumberPad = 4;
	public const TouchScreenKeyboardType PhonePad = 5;
	public const TouchScreenKeyboardType NamePhonePad = 6;
	public const TouchScreenKeyboardType EmailAddress = 7;
	[ObsoleteAttribute] 
	public const TouchScreenKeyboardType NintendoNetworkAccount = 8;
	public const TouchScreenKeyboardType Social = 9;
	public const TouchScreenKeyboardType Search = 10;
	public const TouchScreenKeyboardType DecimalPad = 11;
	public const TouchScreenKeyboardType OneTimeCode = 12;
}
```

---

### public enum DrivenTransformProperties

```csharp
public enum DrivenTransformProperties 
{
	public int value__; 
	public const DrivenTransformProperties None = 0;
	public const DrivenTransformProperties All = -1;
	public const DrivenTransformProperties AnchoredPositionX = 2;
	public const DrivenTransformProperties AnchoredPositionY = 4;
	public const DrivenTransformProperties AnchoredPositionZ = 8;
	public const DrivenTransformProperties Rotation = 16;
	public const DrivenTransformProperties ScaleX = 32;
	public const DrivenTransformProperties ScaleY = 64;
	public const DrivenTransformProperties ScaleZ = 128;
	public const DrivenTransformProperties AnchorMinX = 256;
	public const DrivenTransformProperties AnchorMinY = 512;
	public const DrivenTransformProperties AnchorMaxX = 1024;
	public const DrivenTransformProperties AnchorMaxY = 2048;
	public const DrivenTransformProperties SizeDeltaX = 4096;
	public const DrivenTransformProperties SizeDeltaY = 8192;
	public const DrivenTransformProperties PivotX = 16384;
	public const DrivenTransformProperties PivotY = 32768;
	public const DrivenTransformProperties AnchoredPosition = 6;
	public const DrivenTransformProperties AnchoredPosition3D = 14;
	public const DrivenTransformProperties Scale = 224;
	public const DrivenTransformProperties AnchorMin = 768;
	public const DrivenTransformProperties AnchorMax = 3072;
	public const DrivenTransformProperties Anchors = 3840;
	public const DrivenTransformProperties SizeDelta = 12288;
	public const DrivenTransformProperties Pivot = 49152;
}
```

---

### public enum RectTransform.Axis

```csharp
public enum RectTransform.Axis 
{
	public int value__; 
	public const RectTransform.Axis Horizontal = 0;
	public const RectTransform.Axis Vertical = 1;
}
```

---

### public enum SpriteMaskInteraction

```csharp
public enum SpriteMaskInteraction 
{
	public int value__; 
	public const SpriteMaskInteraction None = 0;
	public const SpriteMaskInteraction VisibleInsideMask = 1;
	public const SpriteMaskInteraction VisibleOutsideMask = 2;
}
```

---

### public enum SpriteMeshType

```csharp
public enum SpriteMeshType 
{
	public int value__; 
	public const SpriteMeshType FullRect = 0;
	public const SpriteMeshType Tight = 1;
}
```

---

### public enum SpritePackingMode

```csharp
public enum SpritePackingMode 
{
	public int value__; 
	public const SpritePackingMode Tight = 0;
	public const SpritePackingMode Rectangle = 1;
}
```

---

### public enum ConfidenceLevel

```csharp
public enum ConfidenceLevel 
{
	public int value__; 
	public const ConfidenceLevel High = 0;
	public const ConfidenceLevel Medium = 1;
	public const ConfidenceLevel Low = 2;
	public const ConfidenceLevel Rejected = 3;
}
```

---

### public enum SpeechSystemStatus

```csharp
public enum SpeechSystemStatus 
{
	public int value__; 
	public const SpeechSystemStatus Stopped = 0;
	public const SpeechSystemStatus Running = 1;
	public const SpeechSystemStatus Failed = 2;
}
```

---

### public enum SpeechError

```csharp
public enum SpeechError 
{
	public int value__; 
	public const SpeechError NoError = 0;
	public const SpeechError TopicLanguageNotSupported = 1;
	public const SpeechError GrammarLanguageMismatch = 2;
	public const SpeechError GrammarCompilationFailure = 3;
	public const SpeechError AudioQualityFailure = 4;
	public const SpeechError PauseLimitExceeded = 5;
	public const SpeechError TimeoutExceeded = 6;
	public const SpeechError NetworkFailure = 7;
	public const SpeechError MicrophoneUnavailable = 8;
	public const SpeechError UnknownError = 9;
}
```

---

### public enum DictationCompletionCause

```csharp
public enum DictationCompletionCause 
{
	public int value__; 
	public const DictationCompletionCause Complete = 0;
	public const DictationCompletionCause AudioQualityFailure = 1;
	public const DictationCompletionCause Canceled = 2;
	public const DictationCompletionCause TimeoutExceeded = 3;
	public const DictationCompletionCause PauseLimitExceeded = 4;
	public const DictationCompletionCause NetworkFailure = 5;
	public const DictationCompletionCause MicrophoneUnavailable = 6;
	public const DictationCompletionCause UnknownError = 7;
}
```

---

### public enum PhotoCapture.CaptureResultType

```csharp
public enum PhotoCapture.CaptureResultType 
{
	public int value__; 
	public const PhotoCapture.CaptureResultType Success = 0;
	public const PhotoCapture.CaptureResultType UnknownError = 1;
}
```

---

### public enum VideoCapture.CaptureResultType

```csharp
public enum VideoCapture.CaptureResultType 
{
	public int value__; 
	public const VideoCapture.CaptureResultType Success = 0;
	public const VideoCapture.CaptureResultType UnknownError = 1;
}
```

---

### public enum CapturePixelFormat

```csharp
public enum CapturePixelFormat 
{
	public int value__; 
	public const CapturePixelFormat BGRA32 = 0;
	public const CapturePixelFormat NV12 = 1;
	public const CapturePixelFormat JPEG = 2;
	public const CapturePixelFormat PNG = 3;
}
```

---

### public enum PersistentListenerMode

```csharp
public enum PersistentListenerMode 
{
	public int value__; 
	public const PersistentListenerMode EventDefined = 0;
	public const PersistentListenerMode Void = 1;
	public const PersistentListenerMode Object = 2;
	public const PersistentListenerMode Int = 3;
	public const PersistentListenerMode Float = 4;
	public const PersistentListenerMode String = 5;
	public const PersistentListenerMode Bool = 6;
}
```

---

### public enum UnityEventCallState

```csharp
public enum UnityEventCallState 
{
	public int value__; 
	public const UnityEventCallState Off = 0;
	public const UnityEventCallState EditorAndRuntime = 1;
	public const UnityEventCallState RuntimeOnly = 2;
}
```

---

### public enum LoadSceneMode

```csharp
public enum LoadSceneMode 
{
	public int value__; 
	public const LoadSceneMode Single = 0;
	public const LoadSceneMode Additive = 1;
}
```

---

### public enum LocalPhysicsMode

```csharp
public enum LocalPhysicsMode 
{
	public int value__; 
	public const LocalPhysicsMode None = 0;
	public const LocalPhysicsMode Physics2D = 1;
	public const LocalPhysicsMode Physics3D = 2;
}
```

---

### public enum SynchronisationStage

```csharp
public enum SynchronisationStage 
{
	public int value__; 
	public const SynchronisationStage VertexProcessing = 0;
	public const SynchronisationStage PixelProcessing = 1;
}
```

---

### public enum IndexFormat

```csharp
public enum IndexFormat 
{
	public int value__; 
	public const IndexFormat UInt16 = 0;
	public const IndexFormat UInt32 = 1;
}
```

---

### public enum MeshUpdateFlags

```csharp
public enum MeshUpdateFlags 
{
	public int value__; 
	public const MeshUpdateFlags Default = 0;
	public const MeshUpdateFlags DontValidateIndices = 1;
	public const MeshUpdateFlags DontResetBoneBounds = 2;
	public const MeshUpdateFlags DontNotifyMeshUsers = 4;
	public const MeshUpdateFlags DontRecalculateBounds = 8;
}
```

---

### public enum VertexAttributeFormat

```csharp
public enum VertexAttributeFormat 
{
	public int value__; 
	public const VertexAttributeFormat Float32 = 0;
	public const VertexAttributeFormat Float16 = 1;
	public const VertexAttributeFormat UNorm8 = 2;
	public const VertexAttributeFormat SNorm8 = 3;
	public const VertexAttributeFormat UNorm16 = 4;
	public const VertexAttributeFormat SNorm16 = 5;
	public const VertexAttributeFormat UInt8 = 6;
	public const VertexAttributeFormat SInt8 = 7;
	public const VertexAttributeFormat UInt16 = 8;
	public const VertexAttributeFormat SInt16 = 9;
	public const VertexAttributeFormat UInt32 = 10;
	public const VertexAttributeFormat SInt32 = 11;
}
```

---

### public enum VertexAttribute

```csharp
public enum VertexAttribute 
{
	public int value__; 
	public const VertexAttribute Position = 0;
	public const VertexAttribute Normal = 1;
	public const VertexAttribute Tangent = 2;
	public const VertexAttribute Color = 3;
	public const VertexAttribute TexCoord0 = 4;
	public const VertexAttribute TexCoord1 = 5;
	public const VertexAttribute TexCoord2 = 6;
	public const VertexAttribute TexCoord3 = 7;
	public const VertexAttribute TexCoord4 = 8;
	public const VertexAttribute TexCoord5 = 9;
	public const VertexAttribute TexCoord6 = 10;
	public const VertexAttribute TexCoord7 = 11;
	public const VertexAttribute BlendWeight = 12;
	public const VertexAttribute BlendIndices = 13;
}
```

---

### public enum OpaqueSortMode

```csharp
public enum OpaqueSortMode 
{
	public int value__; 
	public const OpaqueSortMode Default = 0;
	public const OpaqueSortMode FrontToBack = 1;
	public const OpaqueSortMode NoDistanceSort = 2;
}
```

---

### public enum RenderBufferLoadAction

```csharp
public enum RenderBufferLoadAction 
{
	public int value__; 
	public const RenderBufferLoadAction Load = 0;
	public const RenderBufferLoadAction Clear = 1;
	public const RenderBufferLoadAction DontCare = 2;
}
```

---

### public enum RenderBufferStoreAction

```csharp
public enum RenderBufferStoreAction 
{
	public int value__; 
	public const RenderBufferStoreAction Store = 0;
	public const RenderBufferStoreAction Resolve = 1;
	public const RenderBufferStoreAction StoreAndResolve = 2;
	public const RenderBufferStoreAction DontCare = 3;
}
```

---

### public enum FastMemoryFlags

```csharp
public enum FastMemoryFlags 
{
	public int value__; 
	public const FastMemoryFlags None = 0;
	public const FastMemoryFlags SpillTop = 1;
	public const FastMemoryFlags SpillBottom = 2;
}
```

---

### public enum BlendMode

```csharp
public enum BlendMode 
{
	public int value__; 
	public const BlendMode Zero = 0;
	public const BlendMode One = 1;
	public const BlendMode DstColor = 2;
	public const BlendMode SrcColor = 3;
	public const BlendMode OneMinusDstColor = 4;
	public const BlendMode SrcAlpha = 5;
	public const BlendMode OneMinusSrcColor = 6;
	public const BlendMode DstAlpha = 7;
	public const BlendMode OneMinusDstAlpha = 8;
	public const BlendMode SrcAlphaSaturate = 9;
	public const BlendMode OneMinusSrcAlpha = 10;
}
```

---

### public enum BlendOp

```csharp
public enum BlendOp 
{
	public int value__; 
	public const BlendOp Add = 0;
	public const BlendOp Subtract = 1;
	public const BlendOp ReverseSubtract = 2;
	public const BlendOp Min = 3;
	public const BlendOp Max = 4;
	public const BlendOp LogicalClear = 5;
	public const BlendOp LogicalSet = 6;
	public const BlendOp LogicalCopy = 7;
	public const BlendOp LogicalCopyInverted = 8;
	public const BlendOp LogicalNoop = 9;
	public const BlendOp LogicalInvert = 10;
	public const BlendOp LogicalAnd = 11;
	public const BlendOp LogicalNand = 12;
	public const BlendOp LogicalOr = 13;
	public const BlendOp LogicalNor = 14;
	public const BlendOp LogicalXor = 15;
	public const BlendOp LogicalEquivalence = 16;
	public const BlendOp LogicalAndReverse = 17;
	public const BlendOp LogicalAndInverted = 18;
	public const BlendOp LogicalOrReverse = 19;
	public const BlendOp LogicalOrInverted = 20;
	public const BlendOp Multiply = 21;
	public const BlendOp Screen = 22;
	public const BlendOp Overlay = 23;
	public const BlendOp Darken = 24;
	public const BlendOp Lighten = 25;
	public const BlendOp ColorDodge = 26;
	public const BlendOp ColorBurn = 27;
	public const BlendOp HardLight = 28;
	public const BlendOp SoftLight = 29;
	public const BlendOp Difference = 30;
	public const BlendOp Exclusion = 31;
	public const BlendOp HSLHue = 32;
	public const BlendOp HSLSaturation = 33;
	public const BlendOp HSLColor = 34;
	public const BlendOp HSLLuminosity = 35;
}
```

---

### public enum CompareFunction

```csharp
public enum CompareFunction 
{
	public int value__; 
	public const CompareFunction Disabled = 0;
	public const CompareFunction Never = 1;
	public const CompareFunction Less = 2;
	public const CompareFunction Equal = 3;
	public const CompareFunction LessEqual = 4;
	public const CompareFunction Greater = 5;
	public const CompareFunction NotEqual = 6;
	public const CompareFunction GreaterEqual = 7;
	public const CompareFunction Always = 8;
}
```

---

### public enum CullMode

```csharp
public enum CullMode 
{
	public int value__; 
	public const CullMode Off = 0;
	public const CullMode Front = 1;
	public const CullMode Back = 2;
}
```

---

### public enum ColorWriteMask

```csharp
public enum ColorWriteMask 
{
	public int value__; 
	public const ColorWriteMask Alpha = 1;
	public const ColorWriteMask Blue = 2;
	public const ColorWriteMask Green = 4;
	public const ColorWriteMask Red = 8;
	public const ColorWriteMask All = 15;
}
```

---

### public enum StencilOp

```csharp
public enum StencilOp 
{
	public int value__; 
	public const StencilOp Keep = 0;
	public const StencilOp Zero = 1;
	public const StencilOp Replace = 2;
	public const StencilOp IncrementSaturate = 3;
	public const StencilOp DecrementSaturate = 4;
	public const StencilOp Invert = 5;
	public const StencilOp IncrementWrap = 6;
	public const StencilOp DecrementWrap = 7;
}
```

---

### public enum BuiltinRenderTextureType

```csharp
public enum BuiltinRenderTextureType 
{
	public int value__; 
	public const BuiltinRenderTextureType PropertyName = -4;
	public const BuiltinRenderTextureType BufferPtr = -3;
	public const BuiltinRenderTextureType RenderTexture = -2;
	public const BuiltinRenderTextureType BindableTexture = -1;
	public const BuiltinRenderTextureType None = 0;
	public const BuiltinRenderTextureType CurrentActive = 1;
	public const BuiltinRenderTextureType CameraTarget = 2;
	public const BuiltinRenderTextureType Depth = 3;
	public const BuiltinRenderTextureType DepthNormals = 4;
	public const BuiltinRenderTextureType ResolvedDepth = 5;
	public const BuiltinRenderTextureType PrepassNormalsSpec = 7;
	public const BuiltinRenderTextureType PrepassLight = 8;
	public const BuiltinRenderTextureType PrepassLightSpec = 9;
	public const BuiltinRenderTextureType GBuffer0 = 10;
	public const BuiltinRenderTextureType GBuffer1 = 11;
	public const BuiltinRenderTextureType GBuffer2 = 12;
	public const BuiltinRenderTextureType GBuffer3 = 13;
	public const BuiltinRenderTextureType Reflections = 14;
	public const BuiltinRenderTextureType MotionVectors = 15;
	public const BuiltinRenderTextureType GBuffer4 = 16;
	public const BuiltinRenderTextureType GBuffer5 = 17;
	public const BuiltinRenderTextureType GBuffer6 = 18;
	public const BuiltinRenderTextureType GBuffer7 = 19;
}
```

---

### public enum ShadowCastingMode

```csharp
public enum ShadowCastingMode 
{
	public int value__; 
	public const ShadowCastingMode Off = 0;
	public const ShadowCastingMode On = 1;
	public const ShadowCastingMode TwoSided = 2;
	public const ShadowCastingMode ShadowsOnly = 3;
}
```

---

### public enum GraphicsDeviceType

```csharp
public enum GraphicsDeviceType 
{
	public int value__; 
	[ObsoleteAttribute] 
	public const GraphicsDeviceType OpenGL2 = 0;
	[ObsoleteAttribute] 
	public const GraphicsDeviceType Direct3D9 = 1;
	public const GraphicsDeviceType Direct3D11 = 2;
	[ObsoleteAttribute] 
	public const GraphicsDeviceType PlayStation3 = 3;
	public const GraphicsDeviceType Null = 4;
	[ObsoleteAttribute] 
	public const GraphicsDeviceType Xbox360 = 6;
	public const GraphicsDeviceType OpenGLES2 = 8;
	public const GraphicsDeviceType OpenGLES3 = 11;
	[ObsoleteAttribute] 
	public const GraphicsDeviceType PlayStationVita = 12;
	public const GraphicsDeviceType PlayStation4 = 13;
	public const GraphicsDeviceType XboxOne = 14;
	[ObsoleteAttribute] 
	public const GraphicsDeviceType PlayStationMobile = 15;
	public const GraphicsDeviceType Metal = 16;
	public const GraphicsDeviceType OpenGLCore = 17;
	public const GraphicsDeviceType Direct3D12 = 18;
	[ObsoleteAttribute] 
	public const GraphicsDeviceType N3DS = 19;
	public const GraphicsDeviceType Vulkan = 21;
	public const GraphicsDeviceType Switch = 22;
	public const GraphicsDeviceType XboxOneD3D12 = 23;
	public const GraphicsDeviceType GameCoreXboxOne = 24;
	[ObsoleteAttribute] 
	public const GraphicsDeviceType GameCoreScarlett = 25;
	public const GraphicsDeviceType GameCoreXboxSeries = 25;
	public const GraphicsDeviceType PlayStation5 = 26;
	public const GraphicsDeviceType PlayStation5NGGC = 27;
}
```

---

### public enum GraphicsTier

```csharp
public enum GraphicsTier 
{
	public int value__; 
	public const GraphicsTier Tier1 = 0;
	public const GraphicsTier Tier2 = 1;
	public const GraphicsTier Tier3 = 2;
}
```

---

### public enum RenderTargetFlags

```csharp
public enum RenderTargetFlags 
{
	public int value__; 
	public const RenderTargetFlags None = 0;
	public const RenderTargetFlags ReadOnlyDepth = 1;
	public const RenderTargetFlags ReadOnlyStencil = 2;
	public const RenderTargetFlags ReadOnlyDepthStencil = 3;
}
```

---

### public enum ShadowSamplingMode

```csharp
public enum ShadowSamplingMode 
{
	public int value__; 
	public const ShadowSamplingMode CompareDepths = 0;
	public const ShadowSamplingMode RawDepth = 1;
	public const ShadowSamplingMode None = 2;
}
```

---

### public enum BuiltinShaderDefine

```csharp
public enum BuiltinShaderDefine 
{
	public int value__; 
	public const BuiltinShaderDefine UNITY_NO_DXT5nm = 0;
	public const BuiltinShaderDefine UNITY_NO_RGBM = 1;
	public const BuiltinShaderDefine UNITY_USE_NATIVE_HDR = 2;
	public const BuiltinShaderDefine UNITY_ENABLE_REFLECTION_BUFFERS = 3;
	public const BuiltinShaderDefine UNITY_FRAMEBUFFER_FETCH_AVAILABLE = 4;
	public const BuiltinShaderDefine UNITY_ENABLE_NATIVE_SHADOW_LOOKUPS = 5;
	public const BuiltinShaderDefine UNITY_METAL_SHADOWS_USE_POINT_FILTERING = 6;
	public const BuiltinShaderDefine UNITY_NO_CUBEMAP_ARRAY = 7;
	public const BuiltinShaderDefine UNITY_NO_SCREENSPACE_SHADOWS = 8;
	public const BuiltinShaderDefine UNITY_USE_DITHER_MASK_FOR_ALPHABLENDED_SHADOWS = 9;
	public const BuiltinShaderDefine UNITY_PBS_USE_BRDF1 = 10;
	public const BuiltinShaderDefine UNITY_PBS_USE_BRDF2 = 11;
	public const BuiltinShaderDefine UNITY_PBS_USE_BRDF3 = 12;
	public const BuiltinShaderDefine UNITY_NO_FULL_STANDARD_SHADER = 13;
	public const BuiltinShaderDefine UNITY_SPECCUBE_BOX_PROJECTION = 14;
	public const BuiltinShaderDefine UNITY_SPECCUBE_BLENDING = 15;
	public const BuiltinShaderDefine UNITY_ENABLE_DETAIL_NORMALMAP = 16;
	public const BuiltinShaderDefine SHADER_API_MOBILE = 17;
	public const BuiltinShaderDefine SHADER_API_DESKTOP = 18;
	public const BuiltinShaderDefine UNITY_HARDWARE_TIER1 = 19;
	public const BuiltinShaderDefine UNITY_HARDWARE_TIER2 = 20;
	public const BuiltinShaderDefine UNITY_HARDWARE_TIER3 = 21;
	public const BuiltinShaderDefine UNITY_COLORSPACE_GAMMA = 22;
	public const BuiltinShaderDefine UNITY_LIGHT_PROBE_PROXY_VOLUME = 23;
	public const BuiltinShaderDefine UNITY_HALF_PRECISION_FRAGMENT_SHADER_REGISTERS = 24;
	public const BuiltinShaderDefine UNITY_LIGHTMAP_DLDR_ENCODING = 25;
	public const BuiltinShaderDefine UNITY_LIGHTMAP_RGBM_ENCODING = 26;
	public const BuiltinShaderDefine UNITY_LIGHTMAP_FULL_HDR = 27;
	public const BuiltinShaderDefine UNITY_VIRTUAL_TEXTURING = 28;
	public const BuiltinShaderDefine UNITY_PRETRANSFORM_TO_DISPLAY_ORIENTATION = 29;
	public const BuiltinShaderDefine UNITY_ASTC_NORMALMAP_ENCODING = 30;
	public const BuiltinShaderDefine SHADER_API_GLES30 = 31;
	public const BuiltinShaderDefine UNITY_UNIFIED_SHADER_PRECISION_MODEL = 32;
}
```

---

### public enum TextureDimension

```csharp
public enum TextureDimension 
{
	public int value__; 
	public const TextureDimension Unknown = -1;
	public const TextureDimension None = 0;
	public const TextureDimension Any = 1;
	public const TextureDimension Tex2D = 2;
	public const TextureDimension Tex3D = 3;
	public const TextureDimension Cube = 4;
	public const TextureDimension Tex2DArray = 5;
	public const TextureDimension CubeArray = 6;
}
```

---

### public enum CopyTextureSupport

```csharp
public enum CopyTextureSupport 
{
	public int value__; 
	public const CopyTextureSupport None = 0;
	public const CopyTextureSupport Basic = 1;
	public const CopyTextureSupport Copy3D = 2;
	public const CopyTextureSupport DifferentTypes = 4;
	public const CopyTextureSupport TextureToRT = 8;
	public const CopyTextureSupport RTToTexture = 16;
}
```

---

### public enum ComputeQueueType

```csharp
public enum ComputeQueueType 
{
	public int value__; 
	public const ComputeQueueType Default = 0;
	public const ComputeQueueType Background = 1;
	public const ComputeQueueType Urgent = 2;
}
```

---

### public enum SinglePassStereoMode

```csharp
public enum SinglePassStereoMode 
{
	public int value__; 
	public const SinglePassStereoMode None = 0;
	public const SinglePassStereoMode SideBySide = 1;
	public const SinglePassStereoMode Instancing = 2;
	public const SinglePassStereoMode Multiview = 3;
}
```

---

### public enum CommandBufferExecutionFlags

```csharp
public enum CommandBufferExecutionFlags 
{
	public int value__; 
	public const CommandBufferExecutionFlags None = 0;
	public const CommandBufferExecutionFlags AsyncCompute = 2;
}
```

---

### public enum RenderTextureSubElement

```csharp
public enum RenderTextureSubElement 
{
	public int value__; 
	public const RenderTextureSubElement Color = 0;
	public const RenderTextureSubElement Depth = 1;
	public const RenderTextureSubElement Stencil = 2;
	public const RenderTextureSubElement Default = 3;
}
```

---

### public enum CameraLateLatchMatrixType

```csharp
public enum CameraLateLatchMatrixType 
{
	public int value__; 
	public const CameraLateLatchMatrixType View = 0;
	public const CameraLateLatchMatrixType InverseView = 1;
	public const CameraLateLatchMatrixType ViewProjection = 2;
	public const CameraLateLatchMatrixType InverseViewProjection = 3;
}
```

---

### public enum OpenGLESVersion

```csharp
public enum OpenGLESVersion 
{
	public int value__; 
	public const OpenGLESVersion None = 0;
	public const OpenGLESVersion OpenGLES20 = 1;
	public const OpenGLESVersion OpenGLES30 = 2;
	public const OpenGLESVersion OpenGLES31 = 3;
	public const OpenGLESVersion OpenGLES31AEP = 4;
	public const OpenGLESVersion OpenGLES32 = 5;
}
```

---

### public enum SynchronisationStageFlags

```csharp
public enum SynchronisationStageFlags 
{
	public int value__; 
	public const SynchronisationStageFlags VertexProcessing = 1;
	public const SynchronisationStageFlags PixelProcessing = 2;
	public const SynchronisationStageFlags ComputeProcessing = 4;
	public const SynchronisationStageFlags AllGPUOperations = 7;
}
```

---

### public enum GraphicsFenceType

```csharp
public enum GraphicsFenceType 
{
	public int value__; 
	public const GraphicsFenceType AsyncQueueSynchronisation = 0;
	public const GraphicsFenceType CPUSynchronisation = 1;
}
```

---

### public enum CullingOptions

```csharp
public enum CullingOptions 
{
	public int value__; 
	public const CullingOptions None = 0;
	public const CullingOptions ForceEvenIfCameraIsNotActive = 1;
	public const CullingOptions OcclusionCull = 2;
	public const CullingOptions NeedsLighting = 4;
	public const CullingOptions NeedsReflectionProbes = 8;
	public const CullingOptions Stereo = 16;
	public const CullingOptions DisablePerObjectCulling = 32;
	public const CullingOptions ShadowCasters = 64;
}
```

---

### internal enum DrawRendererFlags

```csharp
internal enum DrawRendererFlags 
{
	public int value__; 
	public const DrawRendererFlags None = 0;
	public const DrawRendererFlags EnableDynamicBatching = 1;
	public const DrawRendererFlags EnableInstancing = 2;
}
```

---

### public enum GizmoSubset

```csharp
public enum GizmoSubset 
{
	public int value__; 
	public const GizmoSubset PreImageEffects = 0;
	public const GizmoSubset PostImageEffects = 1;
}
```

---

### public enum PerObjectData

```csharp
public enum PerObjectData 
{
	public int value__; 
	public const PerObjectData None = 0;
	public const PerObjectData LightProbe = 1;
	public const PerObjectData ReflectionProbes = 2;
	public const PerObjectData LightProbeProxyVolume = 4;
	public const PerObjectData Lightmaps = 8;
	public const PerObjectData LightData = 16;
	public const PerObjectData MotionVectors = 32;
	public const PerObjectData LightIndices = 64;
	public const PerObjectData ReflectionProbeData = 128;
	public const PerObjectData OcclusionProbe = 256;
	public const PerObjectData OcclusionProbeProxyVolume = 512;
	public const PerObjectData ShadowMask = 1024;
}
```

---

### public enum ReflectionProbeSortingCriteria

```csharp
public enum ReflectionProbeSortingCriteria 
{
	public int value__; 
	public const ReflectionProbeSortingCriteria None = 0;
	public const ReflectionProbeSortingCriteria Importance = 1;
	public const ReflectionProbeSortingCriteria Size = 2;
	public const ReflectionProbeSortingCriteria ImportanceThenSize = 3;
}
```

---

### public enum RenderStateMask

```csharp
public enum RenderStateMask 
{
	public int value__; 
	public const RenderStateMask Nothing = 0;
	public const RenderStateMask Blend = 1;
	public const RenderStateMask Raster = 2;
	public const RenderStateMask Depth = 4;
	public const RenderStateMask Stencil = 8;
	public const RenderStateMask Everything = 15;
}
```

---

### public enum SortingCriteria

```csharp
public enum SortingCriteria 
{
	public int value__; 
	public const SortingCriteria None = 0;
	public const SortingCriteria SortingLayer = 1;
	public const SortingCriteria RenderQueue = 2;
	public const SortingCriteria BackToFront = 4;
	public const SortingCriteria QuantizedFrontToBack = 8;
	public const SortingCriteria OptimizeStateChanges = 16;
	public const SortingCriteria CanvasOrder = 32;
	public const SortingCriteria RendererPriority = 64;
	public const SortingCriteria CommonOpaque = 59;
	public const SortingCriteria CommonTransparent = 23;
}
```

---

### public enum DistanceMetric

```csharp
public enum DistanceMetric 
{
	public int value__; 
	public const DistanceMetric Perspective = 0;
	public const DistanceMetric Orthographic = 1;
	public const DistanceMetric CustomAxis = 2;
}
```

---

### public enum SupportedRenderingFeatures.ReflectionProbeModes

```csharp
public enum SupportedRenderingFeatures.ReflectionProbeModes 
{
	public int value__; 
	public const SupportedRenderingFeatures.ReflectionProbeModes None = 0;
	public const SupportedRenderingFeatures.ReflectionProbeModes Rotation = 1;
}
```

---

### public enum SupportedRenderingFeatures.LightmapMixedBakeModes

```csharp
public enum SupportedRenderingFeatures.LightmapMixedBakeModes 
{
	public int value__; 
	public const SupportedRenderingFeatures.LightmapMixedBakeModes None = 0;
	public const SupportedRenderingFeatures.LightmapMixedBakeModes IndirectOnly = 1;
	public const SupportedRenderingFeatures.LightmapMixedBakeModes Subtractive = 2;
	public const SupportedRenderingFeatures.LightmapMixedBakeModes Shadowmask = 4;
}
```

---

### internal enum VisibleLightFlags

```csharp
internal enum VisibleLightFlags 
{
	public int value__; 
	public const VisibleLightFlags IntersectsNearPlane = 1;
	public const VisibleLightFlags IntersectsFarPlane = 2;
}
```

---

### public enum ShaderPropertyFlags

```csharp
public enum ShaderPropertyFlags 
{
	public int value__; 
	public const ShaderPropertyFlags None = 0;
	public const ShaderPropertyFlags HideInInspector = 1;
	public const ShaderPropertyFlags PerRendererData = 2;
	public const ShaderPropertyFlags NoScaleOffset = 4;
	public const ShaderPropertyFlags Normal = 8;
	public const ShaderPropertyFlags HDR = 16;
	public const ShaderPropertyFlags Gamma = 32;
	public const ShaderPropertyFlags NonModifiableTextureData = 64;
	public const ShaderPropertyFlags MainTexture = 128;
	public const ShaderPropertyFlags MainColor = 256;
}
```

---

### internal enum FrameData.Flags

```csharp
internal enum FrameData.Flags 
{
	public int value__; 
	public const FrameData.Flags Evaluate = 1;
	public const FrameData.Flags SeekOccured = 2;
	public const FrameData.Flags Loop = 4;
	public const FrameData.Flags Hold = 8;
	public const FrameData.Flags EffectivePlayStateDelayed = 16;
	public const FrameData.Flags EffectivePlayStatePlaying = 32;
}
```

---

### public enum FrameData.EvaluationType

```csharp
public enum FrameData.EvaluationType 
{
	public int value__; 
	public const FrameData.EvaluationType Evaluate = 0;
	public const FrameData.EvaluationType Playback = 1;
}
```

---

### public enum DirectorWrapMode

```csharp
public enum DirectorWrapMode 
{
	public int value__; 
	public const DirectorWrapMode Hold = 0;
	public const DirectorWrapMode Loop = 1;
	public const DirectorWrapMode None = 2;
}
```

---

### public enum PlayableTraversalMode

```csharp
public enum PlayableTraversalMode 
{
	public int value__; 
	public const PlayableTraversalMode Mix = 0;
	public const PlayableTraversalMode Passthrough = 1;
}
```

---

### public enum PlayState

```csharp
public enum PlayState 
{
	public int value__; 
	public const PlayState Paused = 0;
	public const PlayState Playing = 1;
	[ObsoleteAttribute] 
	public const PlayState Delayed = 2;
}
```

---

### public enum LightType

```csharp
public enum LightType 
{
	public byte value__; 
	public const LightType Directional = 0;
	public const LightType Point = 1;
	public const LightType Spot = 2;
	public const LightType Rectangle = 3;
	public const LightType Disc = 4;
	public const LightType SpotPyramidShape = 5;
	public const LightType SpotBoxShape = 6;
}
```

---

### public enum LightMode

```csharp
public enum LightMode 
{
	public byte value__; 
	public const LightMode Realtime = 0;
	public const LightMode Mixed = 1;
	public const LightMode Baked = 2;
	public const LightMode Unknown = 3;
}
```

---

### public enum FalloffType

```csharp
public enum FalloffType 
{
	public byte value__; 
	public const FalloffType InverseSquared = 0;
	public const FalloffType InverseSquaredNoRangeAttenuation = 1;
	public const FalloffType Linear = 2;
	public const FalloffType Legacy = 3;
	public const FalloffType Undefined = 4;
}
```

---

### public enum AngularFalloffType

```csharp
public enum AngularFalloffType 
{
	public byte value__; 
	public const AngularFalloffType LUT = 0;
	public const AngularFalloffType AnalyticAndInnerAngle = 1;
}
```

---

### public enum TextureCreationFlags

```csharp
public enum TextureCreationFlags 
{
	public int value__; 
	public const TextureCreationFlags None = 0;
	public const TextureCreationFlags MipChain = 1;
	public const TextureCreationFlags Crunch = 64;
}
```

---

### public enum FormatUsage

```csharp
public enum FormatUsage 
{
	public int value__; 
	public const FormatUsage Sample = 0;
	public const FormatUsage Linear = 1;
	public const FormatUsage Sparse = 2;
	public const FormatUsage Render = 4;
	public const FormatUsage Blend = 5;
	public const FormatUsage GetPixels = 6;
	public const FormatUsage SetPixels = 7;
	public const FormatUsage SetPixels32 = 8;
	public const FormatUsage ReadPixels = 9;
	public const FormatUsage LoadStore = 10;
	public const FormatUsage MSAA2x = 11;
	public const FormatUsage MSAA4x = 12;
	public const FormatUsage MSAA8x = 13;
	public const FormatUsage StencilSampling = 16;
}
```

---

### public enum DefaultFormat

```csharp
public enum DefaultFormat 
{
	public int value__; 
	public const DefaultFormat LDR = 0;
	public const DefaultFormat HDR = 1;
}
```

---

### public enum GraphicsFormat

```csharp
public enum GraphicsFormat 
{
	public int value__; 
	public const GraphicsFormat None = 0;
	public const GraphicsFormat R8_SRGB = 1;
	public const GraphicsFormat R8G8_SRGB = 2;
	public const GraphicsFormat R8G8B8_SRGB = 3;
	public const GraphicsFormat R8G8B8A8_SRGB = 4;
	public const GraphicsFormat R8_UNorm = 5;
	public const GraphicsFormat R8G8_UNorm = 6;
	public const GraphicsFormat R8G8B8_UNorm = 7;
	public const GraphicsFormat R8G8B8A8_UNorm = 8;
	public const GraphicsFormat R8_SNorm = 9;
	public const GraphicsFormat R8G8_SNorm = 10;
	public const GraphicsFormat R8G8B8_SNorm = 11;
	public const GraphicsFormat R8G8B8A8_SNorm = 12;
	public const GraphicsFormat R8_UInt = 13;
	public const GraphicsFormat R8G8_UInt = 14;
	public const GraphicsFormat R8G8B8_UInt = 15;
	public const GraphicsFormat R8G8B8A8_UInt = 16;
	public const GraphicsFormat R8_SInt = 17;
	public const GraphicsFormat R8G8_SInt = 18;
	public const GraphicsFormat R8G8B8_SInt = 19;
	public const GraphicsFormat R8G8B8A8_SInt = 20;
	public const GraphicsFormat R16_UNorm = 21;
	public const GraphicsFormat R16G16_UNorm = 22;
	public const GraphicsFormat R16G16B16_UNorm = 23;
	public const GraphicsFormat R16G16B16A16_UNorm = 24;
	public const GraphicsFormat R16_SNorm = 25;
	public const GraphicsFormat R16G16_SNorm = 26;
	public const GraphicsFormat R16G16B16_SNorm = 27;
	public const GraphicsFormat R16G16B16A16_SNorm = 28;
	public const GraphicsFormat R16_UInt = 29;
	public const GraphicsFormat R16G16_UInt = 30;
	public const GraphicsFormat R16G16B16_UInt = 31;
	public const GraphicsFormat R16G16B16A16_UInt = 32;
	public const GraphicsFormat R16_SInt = 33;
	public const GraphicsFormat R16G16_SInt = 34;
	public const GraphicsFormat R16G16B16_SInt = 35;
	public const GraphicsFormat R16G16B16A16_SInt = 36;
	public const GraphicsFormat R32_UInt = 37;
	public const GraphicsFormat R32G32_UInt = 38;
	public const GraphicsFormat R32G32B32_UInt = 39;
	public const GraphicsFormat R32G32B32A32_UInt = 40;
	public const GraphicsFormat R32_SInt = 41;
	public const GraphicsFormat R32G32_SInt = 42;
	public const GraphicsFormat R32G32B32_SInt = 43;
	public const GraphicsFormat R32G32B32A32_SInt = 44;
	public const GraphicsFormat R16_SFloat = 45;
	public const GraphicsFormat R16G16_SFloat = 46;
	public const GraphicsFormat R16G16B16_SFloat = 47;
	public const GraphicsFormat R16G16B16A16_SFloat = 48;
	public const GraphicsFormat R32_SFloat = 49;
	public const GraphicsFormat R32G32_SFloat = 50;
	public const GraphicsFormat R32G32B32_SFloat = 51;
	public const GraphicsFormat R32G32B32A32_SFloat = 52;
	public const GraphicsFormat B8G8R8_SRGB = 56;
	public const GraphicsFormat B8G8R8A8_SRGB = 57;
	public const GraphicsFormat B8G8R8_UNorm = 58;
	public const GraphicsFormat B8G8R8A8_UNorm = 59;
	public const GraphicsFormat B8G8R8_SNorm = 60;
	public const GraphicsFormat B8G8R8A8_SNorm = 61;
	public const GraphicsFormat B8G8R8_UInt = 62;
	public const GraphicsFormat B8G8R8A8_UInt = 63;
	public const GraphicsFormat B8G8R8_SInt = 64;
	public const GraphicsFormat B8G8R8A8_SInt = 65;
	public const GraphicsFormat R4G4B4A4_UNormPack16 = 66;
	public const GraphicsFormat B4G4R4A4_UNormPack16 = 67;
	public const GraphicsFormat R5G6B5_UNormPack16 = 68;
	public const GraphicsFormat B5G6R5_UNormPack16 = 69;
	public const GraphicsFormat R5G5B5A1_UNormPack16 = 70;
	public const GraphicsFormat B5G5R5A1_UNormPack16 = 71;
	public const GraphicsFormat A1R5G5B5_UNormPack16 = 72;
	public const GraphicsFormat E5B9G9R9_UFloatPack32 = 73;
	public const GraphicsFormat B10G11R11_UFloatPack32 = 74;
	public const GraphicsFormat A2B10G10R10_UNormPack32 = 75;
	public const GraphicsFormat A2B10G10R10_UIntPack32 = 76;
	public const GraphicsFormat A2B10G10R10_SIntPack32 = 77;
	public const GraphicsFormat A2R10G10B10_UNormPack32 = 78;
	public const GraphicsFormat A2R10G10B10_UIntPack32 = 79;
	public const GraphicsFormat A2R10G10B10_SIntPack32 = 80;
	public const GraphicsFormat A2R10G10B10_XRSRGBPack32 = 81;
	public const GraphicsFormat A2R10G10B10_XRUNormPack32 = 82;
	public const GraphicsFormat R10G10B10_XRSRGBPack32 = 83;
	public const GraphicsFormat R10G10B10_XRUNormPack32 = 84;
	public const GraphicsFormat A10R10G10B10_XRSRGBPack32 = 85;
	public const GraphicsFormat A10R10G10B10_XRUNormPack32 = 86;
	[EditorBrowsableAttribute] 
	[ObsoleteAttribute] 
	public const GraphicsFormat RGB_DXT1_SRGB = 96;
	public const GraphicsFormat RGBA_DXT1_SRGB = 96;
	[EditorBrowsableAttribute] 
	[ObsoleteAttribute] 
	public const GraphicsFormat RGB_DXT1_UNorm = 97;
	public const GraphicsFormat RGBA_DXT1_UNorm = 97;
	public const GraphicsFormat RGBA_DXT3_SRGB = 98;
	public const GraphicsFormat RGBA_DXT3_UNorm = 99;
	public const GraphicsFormat RGBA_DXT5_SRGB = 100;
	public const GraphicsFormat RGBA_DXT5_UNorm = 101;
	public const GraphicsFormat R_BC4_UNorm = 102;
	public const GraphicsFormat R_BC4_SNorm = 103;
	public const GraphicsFormat RG_BC5_UNorm = 104;
	public const GraphicsFormat RG_BC5_SNorm = 105;
	public const GraphicsFormat RGB_BC6H_UFloat = 106;
	public const GraphicsFormat RGB_BC6H_SFloat = 107;
	public const GraphicsFormat RGBA_BC7_SRGB = 108;
	public const GraphicsFormat RGBA_BC7_UNorm = 109;
	public const GraphicsFormat RGB_PVRTC_2Bpp_SRGB = 110;
	public const GraphicsFormat RGB_PVRTC_2Bpp_UNorm = 111;
	public const GraphicsFormat RGB_PVRTC_4Bpp_SRGB = 112;
	public const GraphicsFormat RGB_PVRTC_4Bpp_UNorm = 113;
	public const GraphicsFormat RGBA_PVRTC_2Bpp_SRGB = 114;
	public const GraphicsFormat RGBA_PVRTC_2Bpp_UNorm = 115;
	public const GraphicsFormat RGBA_PVRTC_4Bpp_SRGB = 116;
	public const GraphicsFormat RGBA_PVRTC_4Bpp_UNorm = 117;
	public const GraphicsFormat RGB_ETC_UNorm = 118;
	public const GraphicsFormat RGB_ETC2_SRGB = 119;
	public const GraphicsFormat RGB_ETC2_UNorm = 120;
	public const GraphicsFormat RGB_A1_ETC2_SRGB = 121;
	public const GraphicsFormat RGB_A1_ETC2_UNorm = 122;
	public const GraphicsFormat RGBA_ETC2_SRGB = 123;
	public const GraphicsFormat RGBA_ETC2_UNorm = 124;
	public const GraphicsFormat R_EAC_UNorm = 125;
	public const GraphicsFormat R_EAC_SNorm = 126;
	public const GraphicsFormat RG_EAC_UNorm = 127;
	public const GraphicsFormat RG_EAC_SNorm = 128;
	public const GraphicsFormat RGBA_ASTC4X4_SRGB = 129;
	public const GraphicsFormat RGBA_ASTC4X4_UNorm = 130;
	public const GraphicsFormat RGBA_ASTC5X5_SRGB = 131;
	public const GraphicsFormat RGBA_ASTC5X5_UNorm = 132;
	public const GraphicsFormat RGBA_ASTC6X6_SRGB = 133;
	public const GraphicsFormat RGBA_ASTC6X6_UNorm = 134;
	public const GraphicsFormat RGBA_ASTC8X8_SRGB = 135;
	public const GraphicsFormat RGBA_ASTC8X8_UNorm = 136;
	public const GraphicsFormat RGBA_ASTC10X10_SRGB = 137;
	public const GraphicsFormat RGBA_ASTC10X10_UNorm = 138;
	public const GraphicsFormat RGBA_ASTC12X12_SRGB = 139;
	public const GraphicsFormat RGBA_ASTC12X12_UNorm = 140;
	public const GraphicsFormat RGBA_ASTC4X4_UFloat = 145;
	public const GraphicsFormat RGBA_ASTC5X5_UFloat = 146;
	public const GraphicsFormat RGBA_ASTC6X6_UFloat = 147;
	public const GraphicsFormat RGBA_ASTC8X8_UFloat = 148;
	public const GraphicsFormat RGBA_ASTC10X10_UFloat = 149;
	public const GraphicsFormat RGBA_ASTC12X12_UFloat = 150;
}
```

---

### public enum TouchPhase

```csharp
public enum TouchPhase 
{
	public int value__; 
	public const TouchPhase Began = 0;
	public const TouchPhase Moved = 1;
	public const TouchPhase Stationary = 2;
	public const TouchPhase Ended = 3;
	public const TouchPhase Canceled = 4;
}
```

---

### public enum IMECompositionMode

```csharp
public enum IMECompositionMode 
{
	public int value__; 
	public const IMECompositionMode Auto = 0;
	public const IMECompositionMode On = 1;
	public const IMECompositionMode Off = 2;
}
```

---

### public enum TouchType

```csharp
public enum TouchType 
{
	public int value__; 
	public const TouchType Direct = 0;
	public const TouchType Indirect = 1;
	public const TouchType Stylus = 2;
}
```

---

### public enum RigidbodyType2D

```csharp
public enum RigidbodyType2D 
{
	public int value__; 
	public const RigidbodyType2D Dynamic = 0;
	public const RigidbodyType2D Kinematic = 1;
	public const RigidbodyType2D Static = 2;
}
```

---

### public enum FontStyle

```csharp
public enum FontStyle 
{
	public int value__; 
	public const FontStyle Normal = 0;
	public const FontStyle Bold = 1;
	public const FontStyle Italic = 2;
	public const FontStyle BoldAndItalic = 3;
}
```

---

### internal enum TextGenerationError

```csharp
internal enum TextGenerationError 
{
	public int value__; 
	public const TextGenerationError None = 0;
	public const TextGenerationError CustomSizeOnNonDynamicFont = 1;
	public const TextGenerationError CustomStyleOnNonDynamicFont = 2;
	public const TextGenerationError NoFont = 4;
}
```

---

### public enum TextAnchor

```csharp
public enum TextAnchor 
{
	public int value__; 
	public const TextAnchor UpperLeft = 0;
	public const TextAnchor UpperCenter = 1;
	public const TextAnchor UpperRight = 2;
	public const TextAnchor MiddleLeft = 3;
	public const TextAnchor MiddleCenter = 4;
	public const TextAnchor MiddleRight = 5;
	public const TextAnchor LowerLeft = 6;
	public const TextAnchor LowerCenter = 7;
	public const TextAnchor LowerRight = 8;
}
```

---

### public enum HorizontalWrapMode

```csharp
public enum HorizontalWrapMode 
{
	public int value__; 
	public const HorizontalWrapMode Wrap = 0;
	public const HorizontalWrapMode Overflow = 1;
}
```

---

### public enum VerticalWrapMode

```csharp
public enum VerticalWrapMode 
{
	public int value__; 
	public const VerticalWrapMode Truncate = 0;
	public const VerticalWrapMode Overflow = 1;
}
```

---

### public enum PlayMode

```csharp
public enum PlayMode 
{
	public int value__; 
	public const PlayMode StopSameLayer = 0;
	public const PlayMode StopAll = 4;
}
```

---

### internal enum AnimationEventSource

```csharp
internal enum AnimationEventSource 
{
	public int value__; 
	public const AnimationEventSource NoSource = 0;
	public const AnimationEventSource Legacy = 1;
	public const AnimationEventSource Animator = 2;
}
```

---

### public enum AvatarIKGoal

```csharp
public enum AvatarIKGoal 
{
	public int value__; 
	public const AvatarIKGoal LeftFoot = 0;
	public const AvatarIKGoal RightFoot = 1;
	public const AvatarIKGoal LeftHand = 2;
	public const AvatarIKGoal RightHand = 3;
}
```

---

### internal enum StateInfoIndex

```csharp
internal enum StateInfoIndex 
{
	public int value__; 
	public const StateInfoIndex CurrentState = 0;
	public const StateInfoIndex NextState = 1;
	public const StateInfoIndex ExitState = 2;
	public const StateInfoIndex InterruptedState = 3;
}
```

---

### public enum AnimatorCullingMode

```csharp
public enum AnimatorCullingMode 
{
	public int value__; 
	public const AnimatorCullingMode AlwaysAnimate = 0;
	public const AnimatorCullingMode CullUpdateTransforms = 1;
	public const AnimatorCullingMode CullCompletely = 2;
}
```

---

### public enum AnimatorUpdateMode

```csharp
public enum AnimatorUpdateMode 
{
	public int value__; 
	public const AnimatorUpdateMode Normal = 0;
	public const AnimatorUpdateMode AnimatePhysics = 1;
	public const AnimatorUpdateMode UnscaledTime = 2;
}
```

---

### public enum HumanBodyBones

```csharp
public enum HumanBodyBones 
{
	public int value__; 
	public const HumanBodyBones Hips = 0;
	public const HumanBodyBones LeftUpperLeg = 1;
	public const HumanBodyBones RightUpperLeg = 2;
	public const HumanBodyBones LeftLowerLeg = 3;
	public const HumanBodyBones RightLowerLeg = 4;
	public const HumanBodyBones LeftFoot = 5;
	public const HumanBodyBones RightFoot = 6;
	public const HumanBodyBones Spine = 7;
	public const HumanBodyBones Chest = 8;
	public const HumanBodyBones UpperChest = 54;
	public const HumanBodyBones Neck = 9;
	public const HumanBodyBones Head = 10;
	public const HumanBodyBones LeftShoulder = 11;
	public const HumanBodyBones RightShoulder = 12;
	public const HumanBodyBones LeftUpperArm = 13;
	public const HumanBodyBones RightUpperArm = 14;
	public const HumanBodyBones LeftLowerArm = 15;
	public const HumanBodyBones RightLowerArm = 16;
	public const HumanBodyBones LeftHand = 17;
	public const HumanBodyBones RightHand = 18;
	public const HumanBodyBones LeftToes = 19;
	public const HumanBodyBones RightToes = 20;
	public const HumanBodyBones LeftEye = 21;
	public const HumanBodyBones RightEye = 22;
	public const HumanBodyBones Jaw = 23;
	public const HumanBodyBones LeftThumbProximal = 24;
	public const HumanBodyBones LeftThumbIntermediate = 25;
	public const HumanBodyBones LeftThumbDistal = 26;
	public const HumanBodyBones LeftIndexProximal = 27;
	public const HumanBodyBones LeftIndexIntermediate = 28;
	public const HumanBodyBones LeftIndexDistal = 29;
	public const HumanBodyBones LeftMiddleProximal = 30;
	public const HumanBodyBones LeftMiddleIntermediate = 31;
	public const HumanBodyBones LeftMiddleDistal = 32;
	public const HumanBodyBones LeftRingProximal = 33;
	public const HumanBodyBones LeftRingIntermediate = 34;
	public const HumanBodyBones LeftRingDistal = 35;
	public const HumanBodyBones LeftLittleProximal = 36;
	public const HumanBodyBones LeftLittleIntermediate = 37;
	public const HumanBodyBones LeftLittleDistal = 38;
	public const HumanBodyBones RightThumbProximal = 39;
	public const HumanBodyBones RightThumbIntermediate = 40;
	public const HumanBodyBones RightThumbDistal = 41;
	public const HumanBodyBones RightIndexProximal = 42;
	public const HumanBodyBones RightIndexIntermediate = 43;
	public const HumanBodyBones RightIndexDistal = 44;
	public const HumanBodyBones RightMiddleProximal = 45;
	public const HumanBodyBones RightMiddleIntermediate = 46;
	public const HumanBodyBones RightMiddleDistal = 47;
	public const HumanBodyBones RightRingProximal = 48;
	public const HumanBodyBones RightRingIntermediate = 49;
	public const HumanBodyBones RightRingDistal = 50;
	public const HumanBodyBones RightLittleProximal = 51;
	public const HumanBodyBones RightLittleIntermediate = 52;
	public const HumanBodyBones RightLittleDistal = 53;
	public const HumanBodyBones LastBone = 55;
}
```

---

### public enum AvatarMaskBodyPart

```csharp
public enum AvatarMaskBodyPart 
{
	public int value__; 
	public const AvatarMaskBodyPart Root = 0;
	public const AvatarMaskBodyPart Body = 1;
	public const AvatarMaskBodyPart Head = 2;
	public const AvatarMaskBodyPart LeftLeg = 3;
	public const AvatarMaskBodyPart RightLeg = 4;
	public const AvatarMaskBodyPart LeftArm = 5;
	public const AvatarMaskBodyPart RightArm = 6;
	public const AvatarMaskBodyPart LeftFingers = 7;
	public const AvatarMaskBodyPart RightFingers = 8;
	public const AvatarMaskBodyPart LeftFootIK = 9;
	public const AvatarMaskBodyPart RightFootIK = 10;
	public const AvatarMaskBodyPart LeftHandIK = 11;
	public const AvatarMaskBodyPart RightHandIK = 12;
	public const AvatarMaskBodyPart LastBodyPart = 13;
}
```

---

### public enum EventType

```csharp
public enum EventType 
{
	public int value__; 
	public const EventType MouseDown = 0;
	public const EventType MouseUp = 1;
	public const EventType MouseMove = 2;
	public const EventType MouseDrag = 3;
	public const EventType KeyDown = 4;
	public const EventType KeyUp = 5;
	public const EventType ScrollWheel = 6;
	public const EventType Repaint = 7;
	public const EventType Layout = 8;
	public const EventType DragUpdated = 9;
	public const EventType DragPerform = 10;
	public const EventType DragExited = 15;
	public const EventType Ignore = 11;
	public const EventType Used = 12;
	public const EventType ValidateCommand = 13;
	public const EventType ExecuteCommand = 14;
	public const EventType ContextClick = 16;
	public const EventType MouseEnterWindow = 20;
	public const EventType MouseLeaveWindow = 21;
	public const EventType TouchDown = 30;
	public const EventType TouchUp = 31;
	public const EventType TouchMove = 32;
	public const EventType TouchEnter = 33;
	public const EventType TouchLeave = 34;
	public const EventType TouchStationary = 35;
	[EditorBrowsableAttribute] 
	[ObsoleteAttribute] 
	public const EventType mouseDown = 0;
	[EditorBrowsableAttribute] 
	[ObsoleteAttribute] 
	public const EventType mouseUp = 1;
	[ObsoleteAttribute] 
	[EditorBrowsableAttribute] 
	public const EventType mouseMove = 2;
	[EditorBrowsableAttribute] 
	[ObsoleteAttribute] 
	public const EventType mouseDrag = 3;
	[EditorBrowsableAttribute] 
	[ObsoleteAttribute] 
	public const EventType keyDown = 4;
	[ObsoleteAttribute] 
	[EditorBrowsableAttribute] 
	public const EventType keyUp = 5;
	[EditorBrowsableAttribute] 
	[ObsoleteAttribute] 
	public const EventType scrollWheel = 6;
	[ObsoleteAttribute] 
	[EditorBrowsableAttribute] 
	public const EventType repaint = 7;
	[EditorBrowsableAttribute] 
	[ObsoleteAttribute] 
	public const EventType layout = 8;
	[ObsoleteAttribute] 
	[EditorBrowsableAttribute] 
	public const EventType dragUpdated = 9;
	[ObsoleteAttribute] 
	[EditorBrowsableAttribute] 
	public const EventType dragPerform = 10;
	[EditorBrowsableAttribute] 
	[ObsoleteAttribute] 
	public const EventType ignore = 11;
	[EditorBrowsableAttribute] 
	[ObsoleteAttribute] 
	public const EventType used = 12;
}
```

---

### public enum EventModifiers

```csharp
public enum EventModifiers 
{
	public int value__; 
	public const EventModifiers None = 0;
	public const EventModifiers Shift = 1;
	public const EventModifiers Control = 2;
	public const EventModifiers Alt = 4;
	public const EventModifiers Command = 8;
	public const EventModifiers Numeric = 16;
	public const EventModifiers CapsLock = 32;
	public const EventModifiers FunctionKey = 64;
}
```

---

### public enum PointerType

```csharp
public enum PointerType 
{
	public int value__; 
	public const PointerType Mouse = 0;
	public const PointerType Touch = 1;
	public const PointerType Pen = 2;
}
```

---

### public enum GUI.ToolbarButtonSize

```csharp
public enum GUI.ToolbarButtonSize 
{
	public int value__; 
	public const GUI.ToolbarButtonSize Fixed = 0;
	public const GUI.ToolbarButtonSize FitToContents = 1;
}
```

---

### public enum FocusType

```csharp
public enum FocusType 
{
	public int value__; 
	[ObsoleteAttribute] 
	public const FocusType Native = 0;
	public const FocusType Keyboard = 1;
	public const FocusType Passive = 2;
}
```

---

### internal enum GUILayoutOption.Type

```csharp
internal enum GUILayoutOption.Type 
{
	public int value__; 
	public const GUILayoutOption.Type fixedWidth = 0;
	public const GUILayoutOption.Type fixedHeight = 1;
	public const GUILayoutOption.Type minWidth = 2;
	public const GUILayoutOption.Type maxWidth = 3;
	public const GUILayoutOption.Type minHeight = 4;
	public const GUILayoutOption.Type maxHeight = 5;
	public const GUILayoutOption.Type stretchWidth = 6;
	public const GUILayoutOption.Type stretchHeight = 7;
	public const GUILayoutOption.Type alignStart = 8;
	public const GUILayoutOption.Type alignMiddle = 9;
	public const GUILayoutOption.Type alignEnd = 10;
	public const GUILayoutOption.Type alignJustify = 11;
	public const GUILayoutOption.Type equalSize = 12;
	public const GUILayoutOption.Type spacing = 13;
}
```

---

### public enum ImagePosition

```csharp
public enum ImagePosition 
{
	public int value__; 
	public const ImagePosition ImageLeft = 0;
	public const ImagePosition ImageAbove = 1;
	public const ImagePosition ImageOnly = 2;
	public const ImagePosition TextOnly = 3;
}
```

---

### public enum TextEditor.DblClickSnapping

```csharp
public enum TextEditor.DblClickSnapping 
{
	public byte value__; 
	public const TextEditor.DblClickSnapping WORDS = 0;
	public const TextEditor.DblClickSnapping PARAGRAPHS = 1;
}
```

---

### public enum ForceMode

```csharp
public enum ForceMode 
{
	public int value__; 
	public const ForceMode Force = 0;
	public const ForceMode Acceleration = 5;
	public const ForceMode Impulse = 1;
	public const ForceMode VelocityChange = 2;
}
```

---

### public enum CollisionFlags

```csharp
public enum CollisionFlags 
{
	public int value__; 
	public const CollisionFlags None = 0;
	public const CollisionFlags Sides = 1;
	public const CollisionFlags Above = 2;
	public const CollisionFlags Below = 4;
	public const CollisionFlags CollidedSides = 1;
	public const CollisionFlags CollidedAbove = 2;
	public const CollisionFlags CollidedBelow = 4;
}
```

---

### public enum QueryTriggerInteraction

```csharp
public enum QueryTriggerInteraction 
{
	public int value__; 
	public const QueryTriggerInteraction UseGlobal = 0;
	public const QueryTriggerInteraction Ignore = 1;
	public const QueryTriggerInteraction Collide = 2;
}
```

---

### public enum Tile.ColliderType

```csharp
public enum Tile.ColliderType 
{
	public int value__; 
	public const Tile.ColliderType None = 0;
	public const Tile.ColliderType Sprite = 1;
	public const Tile.ColliderType Grid = 2;
}
```

---

### public enum TileFlags

```csharp
public enum TileFlags 
{
	public int value__; 
	public const TileFlags None = 0;
	public const TileFlags LockColor = 1;
	public const TileFlags LockTransform = 2;
	public const TileFlags InstantiateGameObjectRuntimeOnly = 4;
	public const TileFlags LockAll = 3;
}
```

---

### public enum RenderMode

```csharp
public enum RenderMode 
{
	public int value__; 
	public const RenderMode ScreenSpaceOverlay = 0;
	public const RenderMode ScreenSpaceCamera = 1;
	public const RenderMode WorldSpace = 2;
}
```

---

### public enum UISystemProfilerApi.SampleType

```csharp
public enum UISystemProfilerApi.SampleType 
{
	public int value__; 
	public const UISystemProfilerApi.SampleType Layout = 0;
	public const UISystemProfilerApi.SampleType Render = 1;
}
```

---

### public enum FFTWindow

```csharp
public enum FFTWindow 
{
	public int value__; 
	public const FFTWindow Rectangular = 0;
	public const FFTWindow Triangle = 1;
	public const FFTWindow Hamming = 2;
	public const FFTWindow Hanning = 3;
	public const FFTWindow Blackman = 4;
	public const FFTWindow BlackmanHarris = 5;
}
```

---

### public enum CanvasUpdate

```csharp
public enum CanvasUpdate 
{
	public int value__; 
	public const CanvasUpdate Prelayout = 0;
	public const CanvasUpdate Layout = 1;
	public const CanvasUpdate PostLayout = 2;
	public const CanvasUpdate PreRender = 3;
	public const CanvasUpdate LatePreRender = 4;
	public const CanvasUpdate MaxUpdateValue = 5;
}
```

---

### public enum GraphicRaycaster.BlockingObjects

```csharp
public enum GraphicRaycaster.BlockingObjects 
{
	public int value__; 
	public const GraphicRaycaster.BlockingObjects None = 0;
	public const GraphicRaycaster.BlockingObjects TwoD = 1;
	public const GraphicRaycaster.BlockingObjects ThreeD = 2;
	public const GraphicRaycaster.BlockingObjects All = 3;
}
```

---

### public enum Image.Type

```csharp
public enum Image.Type 
{
	public int value__; 
	public const Image.Type Simple = 0;
	public const Image.Type Sliced = 1;
	public const Image.Type Tiled = 2;
	public const Image.Type Filled = 3;
}
```

---

### public enum Image.FillMethod

```csharp
public enum Image.FillMethod 
{
	public int value__; 
	public const Image.FillMethod Horizontal = 0;
	public const Image.FillMethod Vertical = 1;
	public const Image.FillMethod Radial90 = 2;
	public const Image.FillMethod Radial180 = 3;
	public const Image.FillMethod Radial360 = 4;
}
```

---

### public enum Image.OriginHorizontal

```csharp
public enum Image.OriginHorizontal 
{
	public int value__; 
	public const Image.OriginHorizontal Left = 0;
	public const Image.OriginHorizontal Right = 1;
}
```

---

### public enum Image.OriginVertical

```csharp
public enum Image.OriginVertical 
{
	public int value__; 
	public const Image.OriginVertical Bottom = 0;
	public const Image.OriginVertical Top = 1;
}
```

---

### public enum Image.Origin90

```csharp
public enum Image.Origin90 
{
	public int value__; 
	public const Image.Origin90 BottomLeft = 0;
	public const Image.Origin90 TopLeft = 1;
	public const Image.Origin90 TopRight = 2;
	public const Image.Origin90 BottomRight = 3;
}
```

---

### public enum Image.Origin180

```csharp
public enum Image.Origin180 
{
	public int value__; 
	public const Image.Origin180 Bottom = 0;
	public const Image.Origin180 Left = 1;
	public const Image.Origin180 Top = 2;
	public const Image.Origin180 Right = 3;
}
```

---

### public enum Image.Origin360

```csharp
public enum Image.Origin360 
{
	public int value__; 
	public const Image.Origin360 Bottom = 0;
	public const Image.Origin360 Right = 1;
	public const Image.Origin360 Top = 2;
	public const Image.Origin360 Left = 3;
}
```

---

### public enum InputField.ContentType

```csharp
public enum InputField.ContentType 
{
	public int value__; 
	public const InputField.ContentType Standard = 0;
	public const InputField.ContentType Autocorrected = 1;
	public const InputField.ContentType IntegerNumber = 2;
	public const InputField.ContentType DecimalNumber = 3;
	public const InputField.ContentType Alphanumeric = 4;
	public const InputField.ContentType Name = 5;
	public const InputField.ContentType EmailAddress = 6;
	public const InputField.ContentType Password = 7;
	public const InputField.ContentType Pin = 8;
	public const InputField.ContentType Custom = 9;
}
```

---

### public enum InputField.InputType

```csharp
public enum InputField.InputType 
{
	public int value__; 
	public const InputField.InputType Standard = 0;
	public const InputField.InputType AutoCorrect = 1;
	public const InputField.InputType Password = 2;
}
```

---

### public enum InputField.CharacterValidation

```csharp
public enum InputField.CharacterValidation 
{
	public int value__; 
	public const InputField.CharacterValidation None = 0;
	public const InputField.CharacterValidation Integer = 1;
	public const InputField.CharacterValidation Decimal = 2;
	public const InputField.CharacterValidation Alphanumeric = 3;
	public const InputField.CharacterValidation Name = 4;
	public const InputField.CharacterValidation EmailAddress = 5;
}
```

---

### public enum InputField.LineType

```csharp
public enum InputField.LineType 
{
	public int value__; 
	public const InputField.LineType SingleLine = 0;
	public const InputField.LineType MultiLineSubmit = 1;
	public const InputField.LineType MultiLineNewline = 2;
}
```

---

### public enum AspectRatioFitter.AspectMode

```csharp
public enum AspectRatioFitter.AspectMode 
{
	public int value__; 
	public const AspectRatioFitter.AspectMode None = 0;
	public const AspectRatioFitter.AspectMode WidthControlsHeight = 1;
	public const AspectRatioFitter.AspectMode HeightControlsWidth = 2;
	public const AspectRatioFitter.AspectMode FitInParent = 3;
	public const AspectRatioFitter.AspectMode EnvelopeParent = 4;
}
```

---

### public enum CanvasScaler.ScaleMode

```csharp
public enum CanvasScaler.ScaleMode 
{
	public int value__; 
	public const CanvasScaler.ScaleMode ConstantPixelSize = 0;
	public const CanvasScaler.ScaleMode ScaleWithScreenSize = 1;
	public const CanvasScaler.ScaleMode ConstantPhysicalSize = 2;
}
```

---

### public enum CanvasScaler.ScreenMatchMode

```csharp
public enum CanvasScaler.ScreenMatchMode 
{
	public int value__; 
	public const CanvasScaler.ScreenMatchMode MatchWidthOrHeight = 0;
	public const CanvasScaler.ScreenMatchMode Expand = 1;
	public const CanvasScaler.ScreenMatchMode Shrink = 2;
}
```

---

### public enum CanvasScaler.Unit

```csharp
public enum CanvasScaler.Unit 
{
	public int value__; 
	public const CanvasScaler.Unit Centimeters = 0;
	public const CanvasScaler.Unit Millimeters = 1;
	public const CanvasScaler.Unit Inches = 2;
	public const CanvasScaler.Unit Points = 3;
	public const CanvasScaler.Unit Picas = 4;
}
```

---

### public enum ContentSizeFitter.FitMode

```csharp
public enum ContentSizeFitter.FitMode 
{
	public int value__; 
	public const ContentSizeFitter.FitMode Unconstrained = 0;
	public const ContentSizeFitter.FitMode MinSize = 1;
	public const ContentSizeFitter.FitMode PreferredSize = 2;
}
```

---

### public enum GridLayoutGroup.Corner

```csharp
public enum GridLayoutGroup.Corner 
{
	public int value__; 
	public const GridLayoutGroup.Corner UpperLeft = 0;
	public const GridLayoutGroup.Corner UpperRight = 1;
	public const GridLayoutGroup.Corner LowerLeft = 2;
	public const GridLayoutGroup.Corner LowerRight = 3;
}
```

---

### public enum GridLayoutGroup.Axis

```csharp
public enum GridLayoutGroup.Axis 
{
	public int value__; 
	public const GridLayoutGroup.Axis Horizontal = 0;
	public const GridLayoutGroup.Axis Vertical = 1;
}
```

---

### public enum GridLayoutGroup.Constraint

```csharp
public enum GridLayoutGroup.Constraint 
{
	public int value__; 
	public const GridLayoutGroup.Constraint Flexible = 0;
	public const GridLayoutGroup.Constraint FixedColumnCount = 1;
	public const GridLayoutGroup.Constraint FixedRowCount = 2;
}
```

---

### public enum Navigation.Mode

```csharp
public enum Navigation.Mode 
{
	public int value__; 
	public const Navigation.Mode None = 0;
	public const Navigation.Mode Horizontal = 1;
	public const Navigation.Mode Vertical = 2;
	public const Navigation.Mode Automatic = 3;
	public const Navigation.Mode Explicit = 4;
}
```

---

### public enum ScrollRect.MovementType

```csharp
public enum ScrollRect.MovementType 
{
	public int value__; 
	public const ScrollRect.MovementType Unrestricted = 0;
	public const ScrollRect.MovementType Elastic = 1;
	public const ScrollRect.MovementType Clamped = 2;
}
```

---

### public enum ScrollRect.ScrollbarVisibility

```csharp
public enum ScrollRect.ScrollbarVisibility 
{
	public int value__; 
	public const ScrollRect.ScrollbarVisibility Permanent = 0;
	public const ScrollRect.ScrollbarVisibility AutoHide = 1;
	public const ScrollRect.ScrollbarVisibility AutoHideAndExpandViewport = 2;
}
```

---

### public enum Scrollbar.Direction

```csharp
public enum Scrollbar.Direction 
{
	public int value__; 
	public const Scrollbar.Direction LeftToRight = 0;
	public const Scrollbar.Direction RightToLeft = 1;
	public const Scrollbar.Direction BottomToTop = 2;
	public const Scrollbar.Direction TopToBottom = 3;
}
```

---

### public enum Selectable.Transition

```csharp
public enum Selectable.Transition 
{
	public int value__; 
	public const Selectable.Transition None = 0;
	public const Selectable.Transition ColorTint = 1;
	public const Selectable.Transition SpriteSwap = 2;
	public const Selectable.Transition Animation = 3;
}
```

---

### public enum Slider.Direction

```csharp
public enum Slider.Direction 
{
	public int value__; 
	public const Slider.Direction LeftToRight = 0;
	public const Slider.Direction RightToLeft = 1;
	public const Slider.Direction BottomToTop = 2;
	public const Slider.Direction TopToBottom = 3;
}
```

---

### public enum Toggle.ToggleTransition

```csharp
public enum Toggle.ToggleTransition 
{
	public int value__; 
	public const Toggle.ToggleTransition None = 0;
	public const Toggle.ToggleTransition Fade = 1;
}
```

---

### public enum ColorTween.ColorTweenMode

```csharp
public enum ColorTween.ColorTweenMode 
{
	public int value__; 
	public const ColorTween.ColorTweenMode All = 0;
	public const ColorTween.ColorTweenMode RGB = 1;
	public const ColorTween.ColorTweenMode Alpha = 2;
}
```

---

### public enum PointerEventData.InputButton

```csharp
public enum PointerEventData.InputButton 
{
	public int value__; 
	public const PointerEventData.InputButton Left = 0;
	public const PointerEventData.InputButton Right = 1;
	public const PointerEventData.InputButton Middle = 2;
}
```

---

### public enum PointerEventData.FramePressState

```csharp
public enum PointerEventData.FramePressState 
{
	public int value__; 
	public const PointerEventData.FramePressState Pressed = 0;
	public const PointerEventData.FramePressState Released = 1;
	public const PointerEventData.FramePressState PressedAndReleased = 2;
	public const PointerEventData.FramePressState NotChanged = 3;
}
```

---

### public enum EventHandle

```csharp
public enum EventHandle 
{
	public int value__; 
	public const EventHandle Unused = 0;
	public const EventHandle Used = 1;
}
```

---

### public enum EventTriggerType

```csharp
public enum EventTriggerType 
{
	public int value__; 
	public const EventTriggerType PointerEnter = 0;
	public const EventTriggerType PointerExit = 1;
	public const EventTriggerType PointerDown = 2;
	public const EventTriggerType PointerUp = 3;
	public const EventTriggerType PointerClick = 4;
	public const EventTriggerType Drag = 5;
	public const EventTriggerType Drop = 6;
	public const EventTriggerType Scroll = 7;
	public const EventTriggerType UpdateSelected = 8;
	public const EventTriggerType Select = 9;
	public const EventTriggerType Deselect = 10;
	public const EventTriggerType Move = 11;
	public const EventTriggerType InitializePotentialDrag = 12;
	public const EventTriggerType BeginDrag = 13;
	public const EventTriggerType EndDrag = 14;
	public const EventTriggerType Submit = 15;
	public const EventTriggerType Cancel = 16;
}
```

---

### public enum StandaloneInputModule.InputMode

```csharp
public enum StandaloneInputModule.InputMode 
{
	public int value__; 
	public const StandaloneInputModule.InputMode Mouse = 0;
	public const StandaloneInputModule.InputMode Buttons = 1;
}
```

---

### public enum MoveDirection

```csharp
public enum MoveDirection 
{
	public int value__; 
	public const MoveDirection Left = 0;
	public const MoveDirection Up = 1;
	public const MoveDirection Right = 2;
	public const MoveDirection Down = 3;
	public const MoveDirection None = 4;
}
```

---

### public enum XRSettings.StereoRenderingMode

```csharp
public enum XRSettings.StereoRenderingMode 
{
	public int value__; 
	public const XRSettings.StereoRenderingMode MultiPass = 0;
	public const XRSettings.StereoRenderingMode SinglePass = 1;
	public const XRSettings.StereoRenderingMode SinglePassInstanced = 2;
	public const XRSettings.StereoRenderingMode SinglePassMultiview = 3;
}
```

---

### public enum DepthAccess

```csharp
public enum DepthAccess 
{
	public int value__; 
	public const DepthAccess Read = 1;
	public const DepthAccess Write = 2;
	public const DepthAccess ReadWrite = 3;
}
```

---

### internal enum RenderGraphProfileId

```csharp
internal enum RenderGraphProfileId 
{
	public int value__; 
	public const RenderGraphProfileId RenderGraphClear = 0;
	public const RenderGraphProfileId RenderGraphClearDebug = 1;
}
```

---

### internal enum RenderGraphResourceType

```csharp
internal enum RenderGraphResourceType 
{
	public int value__; 
	public const RenderGraphResourceType Texture = 0;
	public const RenderGraphResourceType ComputeBuffer = 1;
	public const RenderGraphResourceType Count = 2;
}
```

---

### public enum TextureSizeMode

```csharp
public enum TextureSizeMode 
{
	public int value__; 
	public const TextureSizeMode Explicit = 0;
	public const TextureSizeMode Scale = 1;
	public const TextureSizeMode Functor = 2;
}
```

---

### public enum ClearFlag

```csharp
public enum ClearFlag 
{
	public int value__; 
	public const ClearFlag None = 0;
	public const ClearFlag Color = 1;
	public const ClearFlag Depth = 2;
	public const ClearFlag All = 3;
}
```

---

### public enum DynamicResScalePolicyType

```csharp
public enum DynamicResScalePolicyType 
{
	public int value__; 
	public const DynamicResScalePolicyType ReturnsPercentage = 0;
	public const DynamicResScalePolicyType ReturnsMinMaxLerpFactor = 1;
}
```

---

### public enum DynamicResolutionType

```csharp
public enum DynamicResolutionType 
{
	public byte value__; 
	public const DynamicResolutionType Software = 0;
	public const DynamicResolutionType Hardware = 1;
}
```

---

### public enum DynamicResUpscaleFilter

```csharp
public enum DynamicResUpscaleFilter 
{
	public byte value__; 
	public const DynamicResUpscaleFilter Bilinear = 0;
	public const DynamicResUpscaleFilter CatmullRom = 1;
	public const DynamicResUpscaleFilter Lanczos = 2;
	public const DynamicResUpscaleFilter ContrastAdaptiveSharpen = 3;
}
```

---

### public enum XRGraphics.StereoRenderingMode

```csharp
public enum XRGraphics.StereoRenderingMode 
{
	public int value__; 
	public const XRGraphics.StereoRenderingMode MultiPass = 0;
	public const XRGraphics.StereoRenderingMode SinglePass = 1;
	public const XRGraphics.StereoRenderingMode SinglePassInstanced = 2;
	public const XRGraphics.StereoRenderingMode SinglePassMultiView = 3;
}
```

---

### internal enum DebugAction

```csharp
internal enum DebugAction 
{
	public int value__; 
	public const DebugAction EnableDebugMenu = 0;
	public const DebugAction PreviousDebugPanel = 1;
	public const DebugAction NextDebugPanel = 2;
	public const DebugAction Action = 3;
	public const DebugAction MakePersistent = 4;
	public const DebugAction MoveVertical = 5;
	public const DebugAction MoveHorizontal = 6;
	public const DebugAction Multiplier = 7;
	public const DebugAction ResetAll = 8;
	public const DebugAction DebugActionCount = 9;
}
```

---

### internal enum DebugActionRepeatMode

```csharp
internal enum DebugActionRepeatMode 
{
	public int value__; 
	public const DebugActionRepeatMode Never = 0;
	public const DebugActionRepeatMode Delay = 1;
}
```

---

### public enum DebugUI.Flags

```csharp
public enum DebugUI.Flags 
{
	public int value__; 
	public const DebugUI.Flags None = 0;
	public const DebugUI.Flags EditorOnly = 2;
	public const DebugUI.Flags RuntimeOnly = 4;
	public const DebugUI.Flags EditorForceUpdate = 8;
}
```

---

### public enum PackingRules

```csharp
public enum PackingRules 
{
	public int value__; 
	public const PackingRules Exact = 0;
	public const PackingRules Aggressive = 1;
}
```

---

### public enum FieldPacking

```csharp
public enum FieldPacking 
{
	public int value__; 
	public const FieldPacking NoPacking = 0;
	public const FieldPacking R11G11B10 = 1;
	public const FieldPacking PackedFloat = 2;
	public const FieldPacking PackedUint = 3;
}
```

---

### public enum FieldPrecision

```csharp
public enum FieldPrecision 
{
	public int value__; 
	public const FieldPrecision Half = 0;
	public const FieldPrecision Real = 1;
	public const FieldPrecision Default = 2;
}
```

---

### public enum DepthBits

```csharp
public enum DepthBits 
{
	public int value__; 
	public const DepthBits None = 0;
	public const DepthBits Depth8 = 8;
	public const DepthBits Depth16 = 16;
	public const DepthBits Depth24 = 24;
	public const DepthBits Depth32 = 32;
}
```

---

### public enum MSAASamples

```csharp
public enum MSAASamples 
{
	public int value__; 
	public const MSAASamples None = 1;
	public const MSAASamples MSAA2x = 2;
	public const MSAASamples MSAA4x = 4;
	public const MSAASamples MSAA8x = 8;
}
```

---

### internal enum RTHandleSystem.ResizeMode

```csharp
internal enum RTHandleSystem.ResizeMode 
{
	public int value__; 
	public const RTHandleSystem.ResizeMode Auto = 0;
	public const RTHandleSystem.ResizeMode OnDemand = 1;
}
```

---

### public enum MaterialQuality

```csharp
public enum MaterialQuality 
{
	public int value__; 
	public const MaterialQuality Low = 1;
	public const MaterialQuality Medium = 2;
	public const MaterialQuality High = 4;
}
```

---

### public enum ReloadAttribute.Package

```csharp
public enum ReloadAttribute.Package 
{
	public int value__; 
	public const ReloadAttribute.Package Builtin = 0;
	public const ReloadAttribute.Package Root = 1;
}
```

---

### public enum NavMeshPathStatus

```csharp
public enum NavMeshPathStatus 
{
	public int value__; 
	public const NavMeshPathStatus PathComplete = 0;
	public const NavMeshPathStatus PathPartial = 1;
	public const NavMeshPathStatus PathInvalid = 2;
}
```

---

### internal enum NativeInputUpdateType

```csharp
internal enum NativeInputUpdateType 
{
	public int value__; 
	public const NativeInputUpdateType Dynamic = 1;
	public const NativeInputUpdateType Fixed = 2;
	public const NativeInputUpdateType BeforeRender = 4;
	public const NativeInputUpdateType Editor = 8;
	public const NativeInputUpdateType IgnoreFocus = -2147483648;
}
```

---

### public enum ParticleSystemStopBehavior

```csharp
public enum ParticleSystemStopBehavior 
{
	public int value__; 
	public const ParticleSystemStopBehavior StopEmittingAndClear = 0;
	public const ParticleSystemStopBehavior StopEmitting = 1;
}
```

---

### public enum TerrainUtility.TerrainMap.ErrorCode

```csharp
public enum TerrainUtility.TerrainMap.ErrorCode 
{
	public int value__; 
	public const TerrainUtility.TerrainMap.ErrorCode OK = 0;
	public const TerrainUtility.TerrainMap.ErrorCode Overlapping = 1;
	public const TerrainUtility.TerrainMap.ErrorCode SizeMismatch = 4;
	public const TerrainUtility.TerrainMap.ErrorCode EdgeAlignmentMismatch = 8;
}
```

---

### internal enum YogaMeasureMode

```csharp
internal enum YogaMeasureMode 
{
	public int value__; 
	public const YogaMeasureMode Undefined = 0;
	public const YogaMeasureMode Exactly = 1;
	public const YogaMeasureMode AtMost = 2;
}
```

---

### internal enum RemoteConfigSettingsHelper.Tag

```csharp
internal enum RemoteConfigSettingsHelper.Tag 
{
	public int value__; 
	public const RemoteConfigSettingsHelper.Tag kUnknown = 0;
	public const RemoteConfigSettingsHelper.Tag kIntVal = 1;
	public const RemoteConfigSettingsHelper.Tag kInt64Val = 2;
	public const RemoteConfigSettingsHelper.Tag kUInt64Val = 3;
	public const RemoteConfigSettingsHelper.Tag kDoubleVal = 4;
	public const RemoteConfigSettingsHelper.Tag kBoolVal = 5;
	public const RemoteConfigSettingsHelper.Tag kStringVal = 6;
	public const RemoteConfigSettingsHelper.Tag kArrayVal = 7;
	public const RemoteConfigSettingsHelper.Tag kMixedArrayVal = 8;
	public const RemoteConfigSettingsHelper.Tag kMapVal = 9;
	public const RemoteConfigSettingsHelper.Tag kMaxTags = 10;
}
```

---

### public enum AnalyticsSessionState

```csharp
public enum AnalyticsSessionState 
{
	public int value__; 
	public const AnalyticsSessionState kSessionStopped = 0;
	public const AnalyticsSessionState kSessionStarted = 1;
	public const AnalyticsSessionState kSessionPaused = 2;
	public const AnalyticsSessionState kSessionResumed = 3;
}
```

---

### internal enum UnityWebRequest.UnityWebRequestMethod

```csharp
internal enum UnityWebRequest.UnityWebRequestMethod 
{
	public int value__; 
	public const UnityWebRequest.UnityWebRequestMethod Get = 0;
	public const UnityWebRequest.UnityWebRequestMethod Post = 1;
	public const UnityWebRequest.UnityWebRequestMethod Put = 2;
	public const UnityWebRequest.UnityWebRequestMethod Head = 3;
	public const UnityWebRequest.UnityWebRequestMethod Custom = 4;
}
```

---

### internal enum UnityWebRequest.UnityWebRequestError

```csharp
internal enum UnityWebRequest.UnityWebRequestError 
{
	public int value__; 
	public const UnityWebRequest.UnityWebRequestError OK = 0;
	public const UnityWebRequest.UnityWebRequestError Unknown = 1;
	public const UnityWebRequest.UnityWebRequestError SDKError = 2;
	public const UnityWebRequest.UnityWebRequestError UnsupportedProtocol = 3;
	public const UnityWebRequest.UnityWebRequestError MalformattedUrl = 4;
	public const UnityWebRequest.UnityWebRequestError CannotResolveProxy = 5;
	public const UnityWebRequest.UnityWebRequestError CannotResolveHost = 6;
	public const UnityWebRequest.UnityWebRequestError CannotConnectToHost = 7;
	public const UnityWebRequest.UnityWebRequestError AccessDenied = 8;
	public const UnityWebRequest.UnityWebRequestError GenericHttpError = 9;
	public const UnityWebRequest.UnityWebRequestError WriteError = 10;
	public const UnityWebRequest.UnityWebRequestError ReadError = 11;
	public const UnityWebRequest.UnityWebRequestError OutOfMemory = 12;
	public const UnityWebRequest.UnityWebRequestError Timeout = 13;
	public const UnityWebRequest.UnityWebRequestError HTTPPostError = 14;
	public const UnityWebRequest.UnityWebRequestError SSLCannotConnect = 15;
	public const UnityWebRequest.UnityWebRequestError Aborted = 16;
	public const UnityWebRequest.UnityWebRequestError TooManyRedirects = 17;
	public const UnityWebRequest.UnityWebRequestError ReceivedNoData = 18;
	public const UnityWebRequest.UnityWebRequestError SSLNotSupported = 19;
	public const UnityWebRequest.UnityWebRequestError FailedToSendData = 20;
	public const UnityWebRequest.UnityWebRequestError FailedToReceiveData = 21;
	public const UnityWebRequest.UnityWebRequestError SSLCertificateError = 22;
	public const UnityWebRequest.UnityWebRequestError SSLCipherNotAvailable = 23;
	public const UnityWebRequest.UnityWebRequestError SSLCACertError = 24;
	public const UnityWebRequest.UnityWebRequestError UnrecognizedContentEncoding = 25;
	public const UnityWebRequest.UnityWebRequestError LoginFailed = 26;
	public const UnityWebRequest.UnityWebRequestError SSLShutdownFailed = 27;
	public const UnityWebRequest.UnityWebRequestError NoInternetConnection = 28;
}
```

---

### public enum UnityWebRequest.Result

```csharp
public enum UnityWebRequest.Result 
{
	public int value__; 
	public const UnityWebRequest.Result InProgress = 0;
	public const UnityWebRequest.Result Success = 1;
	public const UnityWebRequest.Result ConnectionError = 2;
	public const UnityWebRequest.Result ProtocolError = 3;
	public const UnityWebRequest.Result DataProcessingError = 4;
}
```

---

### public enum VFXSpawnerLoopState

```csharp
public enum VFXSpawnerLoopState 
{
	public int value__; 
	public const VFXSpawnerLoopState Finished = 0;
	public const VFXSpawnerLoopState DelayingBeforeLoop = 1;
	public const VFXSpawnerLoopState Looping = 2;
	public const VFXSpawnerLoopState DelayingAfterLoop = 3;
}
```

---

### public enum VideoRenderMode

```csharp
public enum VideoRenderMode 
{
	public int value__; 
	public const VideoRenderMode CameraFarPlane = 0;
	public const VideoRenderMode CameraNearPlane = 1;
	public const VideoRenderMode RenderTexture = 2;
	public const VideoRenderMode MaterialOverride = 3;
	public const VideoRenderMode APIOnly = 4;
}
```

---

### public enum Video3DLayout

```csharp
public enum Video3DLayout 
{
	public int value__; 
	public const Video3DLayout No3D = 0;
	public const Video3DLayout SideBySide3D = 1;
	public const Video3DLayout OverUnder3D = 2;
}
```

---

### public enum VideoAspectRatio

```csharp
public enum VideoAspectRatio 
{
	public int value__; 
	public const VideoAspectRatio NoScaling = 0;
	public const VideoAspectRatio FitVertically = 1;
	public const VideoAspectRatio FitHorizontally = 2;
	public const VideoAspectRatio FitInside = 3;
	public const VideoAspectRatio FitOutside = 4;
	public const VideoAspectRatio Stretch = 5;
}
```

---

### public enum VideoTimeSource

```csharp
public enum VideoTimeSource 
{
	public int value__; 
	public const VideoTimeSource AudioDSPTimeSource = 0;
	public const VideoTimeSource GameTimeSource = 1;
}
```

---

### public enum VideoTimeReference

```csharp
public enum VideoTimeReference 
{
	public int value__; 
	public const VideoTimeReference Freerun = 0;
	public const VideoTimeReference InternalTime = 1;
	public const VideoTimeReference ExternalTime = 2;
}
```

---

### public enum VideoSource

```csharp
public enum VideoSource 
{
	public int value__; 
	public const VideoSource VideoClip = 0;
	public const VideoSource Url = 1;
}
```

---

### public enum VideoAudioOutputMode

```csharp
public enum VideoAudioOutputMode 
{
	public int value__; 
	public const VideoAudioOutputMode None = 0;
	public const VideoAudioOutputMode AudioSource = 1;
	public const VideoAudioOutputMode Direct = 2;
	public const VideoAudioOutputMode APIOnly = 3;
}
```

---

### public enum XRNode

```csharp
public enum XRNode 
{
	public int value__; 
	public const XRNode LeftEye = 0;
	public const XRNode RightEye = 1;
	public const XRNode CenterEye = 2;
	public const XRNode Head = 3;
	public const XRNode LeftHand = 4;
	public const XRNode RightHand = 5;
	public const XRNode GameController = 6;
	public const XRNode TrackingReference = 7;
	public const XRNode HardwareTracker = 8;
}
```

---

### internal enum AvailableTrackingData

```csharp
internal enum AvailableTrackingData 
{
	public int value__; 
	public const AvailableTrackingData None = 0;
	public const AvailableTrackingData PositionAvailable = 1;
	public const AvailableTrackingData RotationAvailable = 2;
	public const AvailableTrackingData VelocityAvailable = 4;
	public const AvailableTrackingData AngularVelocityAvailable = 8;
	public const AvailableTrackingData AccelerationAvailable = 16;
	public const AvailableTrackingData AngularAccelerationAvailable = 32;
}
```

---

### internal enum InputFeatureType

```csharp
internal enum InputFeatureType 
{
	public uint value__; 
	public const InputFeatureType Custom = 0;
	public const InputFeatureType Binary = 1;
	public const InputFeatureType DiscreteStates = 2;
	public const InputFeatureType Axis1D = 3;
	public const InputFeatureType Axis2D = 4;
	public const InputFeatureType Axis3D = 5;
	public const InputFeatureType Rotation = 6;
	public const InputFeatureType Hand = 7;
	public const InputFeatureType Bone = 8;
	public const InputFeatureType Eyes = 9;
	public const InputFeatureType kUnityXRInputFeatureTypeInvalid = 4294967295;
}
```

---

### internal enum ConnectionChangeType

```csharp
internal enum ConnectionChangeType 
{
	public uint value__; 
	public const ConnectionChangeType Connected = 0;
	public const ConnectionChangeType Disconnected = 1;
	public const ConnectionChangeType ConfigChange = 2;
}
```

---

### public enum XRDisplaySubsystem.TextureLayout

```csharp
public enum XRDisplaySubsystem.TextureLayout 
{
	public int value__; 
	public const XRDisplaySubsystem.TextureLayout Texture2DArray = 1;
	public const XRDisplaySubsystem.TextureLayout SingleTexture2D = 2;
	public const XRDisplaySubsystem.TextureLayout SeparateTexture2Ds = 4;
}
```

---

### public enum MeshGenerationStatus

```csharp
public enum MeshGenerationStatus 
{
	public int value__; 
	public const MeshGenerationStatus Success = 0;
	public const MeshGenerationStatus InvalidMeshId = 1;
	public const MeshGenerationStatus GenerationAlreadyInProgress = 2;
	public const MeshGenerationStatus Canceled = 3;
	public const MeshGenerationStatus UnknownError = 4;
}
```

---

### public enum MeshVertexAttributes

```csharp
public enum MeshVertexAttributes 
{
	public int value__; 
	public const MeshVertexAttributes None = 0;
	public const MeshVertexAttributes Normals = 1;
	public const MeshVertexAttributes Tangents = 2;
	public const MeshVertexAttributes UVs = 4;
	public const MeshVertexAttributes Colors = 8;
}
```

---

### public enum AutoPlay

```csharp
public enum AutoPlay 
{
	public int value__; 
	public const AutoPlay None = 0;
	public const AutoPlay AutoPlaySequences = 1;
	public const AutoPlay AutoPlayTweeners = 2;
	public const AutoPlay All = 3;
}
```

---

### public enum AxisConstraint

```csharp
public enum AxisConstraint 
{
	public int value__; 
	public const AxisConstraint None = 0;
	public const AxisConstraint X = 2;
	public const AxisConstraint Y = 4;
	public const AxisConstraint Z = 8;
	public const AxisConstraint W = 16;
}
```

---

### public enum Ease

```csharp
public enum Ease 
{
	public int value__; 
	public const Ease Unset = 0;
	public const Ease Linear = 1;
	public const Ease InSine = 2;
	public const Ease OutSine = 3;
	public const Ease InOutSine = 4;
	public const Ease InQuad = 5;
	public const Ease OutQuad = 6;
	public const Ease InOutQuad = 7;
	public const Ease InCubic = 8;
	public const Ease OutCubic = 9;
	public const Ease InOutCubic = 10;
	public const Ease InQuart = 11;
	public const Ease OutQuart = 12;
	public const Ease InOutQuart = 13;
	public const Ease InQuint = 14;
	public const Ease OutQuint = 15;
	public const Ease InOutQuint = 16;
	public const Ease InExpo = 17;
	public const Ease OutExpo = 18;
	public const Ease InOutExpo = 19;
	public const Ease InCirc = 20;
	public const Ease OutCirc = 21;
	public const Ease InOutCirc = 22;
	public const Ease InElastic = 23;
	public const Ease OutElastic = 24;
	public const Ease InOutElastic = 25;
	public const Ease InBack = 26;
	public const Ease OutBack = 27;
	public const Ease InOutBack = 28;
	public const Ease InBounce = 29;
	public const Ease OutBounce = 30;
	public const Ease InOutBounce = 31;
	public const Ease Flash = 32;
	public const Ease InFlash = 33;
	public const Ease OutFlash = 34;
	public const Ease InOutFlash = 35;
	public const Ease INTERNAL_Zero = 36;
	public const Ease INTERNAL_Custom = 37;
}
```

---

### public enum LinkBehaviour

```csharp
public enum LinkBehaviour 
{
	public int value__; 
	public const LinkBehaviour PauseOnDisable = 0;
	public const LinkBehaviour PauseOnDisablePlayOnEnable = 1;
	public const LinkBehaviour PauseOnDisableRestartOnEnable = 2;
	public const LinkBehaviour PlayOnEnable = 3;
	public const LinkBehaviour RestartOnEnable = 4;
	public const LinkBehaviour KillOnDisable = 5;
	public const LinkBehaviour KillOnDestroy = 6;
	public const LinkBehaviour CompleteOnDisable = 7;
	public const LinkBehaviour CompleteAndKillOnDisable = 8;
	public const LinkBehaviour RewindOnDisable = 9;
	public const LinkBehaviour RewindAndKillOnDisable = 10;
}
```

---

### public enum PathMode

```csharp
public enum PathMode 
{
	public int value__; 
	public const PathMode Ignore = 0;
	public const PathMode Full3D = 1;
	public const PathMode TopDown2D = 2;
	public const PathMode Sidescroller2D = 3;
}
```

---

### public enum PathType

```csharp
public enum PathType 
{
	public int value__; 
	public const PathType Linear = 0;
	public const PathType CatmullRom = 1;
	public const PathType CubicBezier = 2;
}
```

---

### public enum RotateMode

```csharp
public enum RotateMode 
{
	public int value__; 
	public const RotateMode Fast = 0;
	public const RotateMode FastBeyond360 = 1;
	public const RotateMode WorldAxisAdd = 2;
	public const RotateMode LocalAxisAdd = 3;
}
```

---

### public enum ScrambleMode

```csharp
public enum ScrambleMode 
{
	public int value__; 
	public const ScrambleMode None = 0;
	public const ScrambleMode All = 1;
	public const ScrambleMode Uppercase = 2;
	public const ScrambleMode Lowercase = 3;
	public const ScrambleMode Numerals = 4;
	public const ScrambleMode Custom = 5;
}
```

---

### public enum LoopType

```csharp
public enum LoopType 
{
	public int value__; 
	public const LoopType Restart = 0;
	public const LoopType Yoyo = 1;
	public const LoopType Incremental = 2;
}
```

---

### public enum LogBehaviour

```csharp
public enum LogBehaviour 
{
	public int value__; 
	public const LogBehaviour Default = 0;
	public const LogBehaviour Verbose = 1;
	public const LogBehaviour ErrorsOnly = 2;
}
```

---

### public enum TweenType

```csharp
public enum TweenType 
{
	public int value__; 
	public const TweenType Tweener = 0;
	public const TweenType Sequence = 1;
	public const TweenType Callback = 2;
}
```

---

### public enum UpdateType

```csharp
public enum UpdateType 
{
	public int value__; 
	public const UpdateType Normal = 0;
	public const UpdateType Late = 1;
	public const UpdateType Fixed = 2;
	public const UpdateType Manual = 3;
}
```

---

### public enum OrientType

```csharp
public enum OrientType 
{
	public int value__; 
	public const OrientType None = 0;
	public const OrientType ToPath = 1;
	public const OrientType LookAtTransform = 2;
	public const OrientType LookAtPosition = 3;
}
```

---

### public enum DOTweenSettings.SettingsLocation

```csharp
public enum DOTweenSettings.SettingsLocation 
{
	public int value__; 
	public const DOTweenSettings.SettingsLocation AssetsDirectory = 0;
	public const DOTweenSettings.SettingsLocation DOTweenDirectory = 1;
	public const DOTweenSettings.SettingsLocation DemigiantDirectory = 2;
}
```

---

### internal enum SafeModeReport.SafeModeReportType

```csharp
internal enum SafeModeReport.SafeModeReportType 
{
	public int value__; 
	public const SafeModeReport.SafeModeReportType Unset = 0;
	public const SafeModeReport.SafeModeReportType TargetOrFieldMissing = 1;
	public const SafeModeReport.SafeModeReportType Callback = 2;
	public const SafeModeReport.SafeModeReportType StartupFailure = 3;
}
```

---

### internal enum TweenManager.CapacityIncreaseMode

```csharp
internal enum TweenManager.CapacityIncreaseMode 
{
	public int value__; 
	public const TweenManager.CapacityIncreaseMode TweenersAndSequences = 0;
	public const TweenManager.CapacityIncreaseMode TweenersOnly = 1;
	public const TweenManager.CapacityIncreaseMode SequencesOnly = 2;
}
```

---

### internal enum FilterType

```csharp
internal enum FilterType 
{
	public int value__; 
	public const FilterType All = 0;
	public const FilterType TargetOrId = 1;
	public const FilterType TargetAndId = 2;
	public const FilterType AllExceptTargetsOrIds = 3;
	public const FilterType DOGetter = 4;
}
```

---

### public enum NestedTweenFailureBehaviour

```csharp
public enum NestedTweenFailureBehaviour 
{
	public int value__; 
	public const NestedTweenFailureBehaviour TryToPreserveSequence = 0;
	public const NestedTweenFailureBehaviour KillWholeSequence = 1;
}
```

---

### internal enum OperationType

```csharp
internal enum OperationType 
{
	public int value__; 
	public const OperationType Complete = 0;
	public const OperationType Despawn = 1;
	public const OperationType Flip = 2;
	public const OperationType Goto = 3;
	public const OperationType Pause = 4;
	public const OperationType Play = 5;
	public const OperationType PlayForward = 6;
	public const OperationType PlayBackwards = 7;
	public const OperationType Rewind = 8;
	public const OperationType SmoothRewind = 9;
	public const OperationType Restart = 10;
	public const OperationType TogglePause = 11;
	public const OperationType IsTweening = 12;
}
```

---

### public enum SafeModeLogBehaviour

```csharp
public enum SafeModeLogBehaviour 
{
	public int value__; 
	public const SafeModeLogBehaviour None = 0;
	public const SafeModeLogBehaviour Normal = 1;
	public const SafeModeLogBehaviour Warning = 2;
	public const SafeModeLogBehaviour Error = 3;
}
```

---

### public enum SpecialStartupMode

```csharp
public enum SpecialStartupMode 
{
	public int value__; 
	public const SpecialStartupMode None = 0;
	public const SpecialStartupMode SetLookAt = 1;
	public const SpecialStartupMode SetShake = 2;
	public const SpecialStartupMode SetPunch = 3;
	public const SpecialStartupMode SetCameraShakePosition = 4;
}
```

---

### public enum UpdateNotice

```csharp
public enum UpdateNotice 
{
	public int value__; 
	public const UpdateNotice None = 0;
	public const UpdateNotice RewindStep = 1;
}
```

---

### internal enum UpdateMode

```csharp
internal enum UpdateMode 
{
	public int value__; 
	public const UpdateMode Update = 0;
	public const UpdateMode Goto = 1;
	public const UpdateMode IgnoreOnUpdate = 2;
	public const UpdateMode IgnoreOnComplete = 3;
}
```

---

### public enum RewindCallbackMode

```csharp
public enum RewindCallbackMode 
{
	public int value__; 
	public const RewindCallbackMode FireIfPositionChanged = 0;
	public const RewindCallbackMode FireAlwaysWithRewind = 1;
	public const RewindCallbackMode FireAlways = 2;
}
```

---

### public enum ClipType

```csharp
public enum ClipType 
{
	public int value__; 
	public const ClipType ctIntersection = 0;
	public const ClipType ctUnion = 1;
	public const ClipType ctDifference = 2;
	public const ClipType ctXor = 3;
}
```

---

### public enum PolyType

```csharp
public enum PolyType 
{
	public int value__; 
	public const PolyType ptSubject = 0;
	public const PolyType ptClip = 1;
}
```

---

### public enum PolyFillType

```csharp
public enum PolyFillType 
{
	public int value__; 
	public const PolyFillType pftEvenOdd = 0;
	public const PolyFillType pftNonZero = 1;
	public const PolyFillType pftPositive = 2;
	public const PolyFillType pftNegative = 3;
}
```

---

### internal enum EdgeSide

```csharp
internal enum EdgeSide 
{
	public int value__; 
	public const EdgeSide esLeft = 0;
	public const EdgeSide esRight = 1;
}
```

---

### internal enum Direction

```csharp
internal enum Direction 
{
	public int value__; 
	public const Direction dRightToLeft = 0;
	public const Direction dLeftToRight = 1;
}
```

---

### public enum EncryptionAlgorithm

```csharp
public enum EncryptionAlgorithm 
{
	public int value__; 
	public const EncryptionAlgorithm None = 0;
	public const EncryptionAlgorithm PkzipWeak = 1;
	public const EncryptionAlgorithm Unsupported = 4;
}
```

---

### public enum ZipProgressEventType

```csharp
public enum ZipProgressEventType 
{
	public int value__; 
	public const ZipProgressEventType Adding_Started = 0;
	public const ZipProgressEventType Adding_AfterAddEntry = 1;
	public const ZipProgressEventType Adding_Completed = 2;
	public const ZipProgressEventType Reading_Started = 3;
	public const ZipProgressEventType Reading_BeforeReadEntry = 4;
	public const ZipProgressEventType Reading_AfterReadEntry = 5;
	public const ZipProgressEventType Reading_Completed = 6;
	public const ZipProgressEventType Reading_ArchiveBytesRead = 7;
	public const ZipProgressEventType Saving_Started = 8;
	public const ZipProgressEventType Saving_BeforeWriteEntry = 9;
	public const ZipProgressEventType Saving_AfterWriteEntry = 10;
	public const ZipProgressEventType Saving_Completed = 11;
	public const ZipProgressEventType Saving_AfterSaveTempArchive = 12;
	public const ZipProgressEventType Saving_BeforeRenameTempArchive = 13;
	public const ZipProgressEventType Saving_AfterRenameTempArchive = 14;
	public const ZipProgressEventType Saving_AfterCompileSelfExtractor = 15;
	public const ZipProgressEventType Saving_EntryBytesRead = 16;
	public const ZipProgressEventType Extracting_BeforeExtractEntry = 17;
	public const ZipProgressEventType Extracting_AfterExtractEntry = 18;
	public const ZipProgressEventType Extracting_ExtractEntryWouldOverwrite = 19;
	public const ZipProgressEventType Extracting_EntryBytesWritten = 20;
	public const ZipProgressEventType Extracting_BeforeExtractAll = 21;
	public const ZipProgressEventType Extracting_AfterExtractAll = 22;
	public const ZipProgressEventType Error_Saving = 23;
}
```

---

### public enum ExtractExistingFileAction

```csharp
public enum ExtractExistingFileAction 
{
	public int value__; 
	public const ExtractExistingFileAction Throw = 0;
	public const ExtractExistingFileAction OverwriteSilently = 1;
	public const ExtractExistingFileAction DoNotOverwrite = 2;
	public const ExtractExistingFileAction InvokeExtractProgressEvent = 3;
}
```

---

### internal enum CryptoMode

```csharp
internal enum CryptoMode 
{
	public int value__; 
	public const CryptoMode Encrypt = 0;
	public const CryptoMode Decrypt = 1;
}
```

---

### public enum ZipEntryTimestamp

```csharp
public enum ZipEntryTimestamp 
{
	public int value__; 
	public const ZipEntryTimestamp None = 0;
	public const ZipEntryTimestamp DOS = 1;
	public const ZipEntryTimestamp Windows = 2;
	public const ZipEntryTimestamp Unix = 4;
	public const ZipEntryTimestamp InfoZip1 = 8;
}
```

---

### public enum CompressionMethod

```csharp
public enum CompressionMethod 
{
	public int value__; 
	public const CompressionMethod None = 0;
	public const CompressionMethod Deflate = 8;
}
```

---

### public enum ZipEntrySource

```csharp
public enum ZipEntrySource 
{
	public int value__; 
	public const ZipEntrySource None = 0;
	public const ZipEntrySource FileSystem = 1;
	public const ZipEntrySource Stream = 2;
	public const ZipEntrySource ZipFile = 3;
	public const ZipEntrySource WriteDelegate = 4;
	public const ZipEntrySource JitStream = 5;
	public const ZipEntrySource ZipOutputStream = 6;
}
```

---

### public enum ZipErrorAction

```csharp
public enum ZipErrorAction 
{
	public int value__; 
	public const ZipErrorAction Throw = 0;
	public const ZipErrorAction Skip = 1;
	public const ZipErrorAction Retry = 2;
	public const ZipErrorAction InvokeErrorEvent = 3;
}
```

---

### public enum Zip64Option

```csharp
public enum Zip64Option 
{
	public int value__; 
	public const Zip64Option Default = 0;
	public const Zip64Option Never = 0;
	public const Zip64Option AsNecessary = 1;
	public const Zip64Option Always = 2;
}
```

---

### public enum ZipOption

```csharp
public enum ZipOption 
{
	public int value__; 
	public const ZipOption Default = 0;
	public const ZipOption Never = 0;
	public const ZipOption AsNecessary = 1;
	public const ZipOption Always = 2;
}
```

---

### internal enum BlockState

```csharp
internal enum BlockState 
{
	public int value__; 
	public const BlockState NeedMore = 0;
	public const BlockState BlockDone = 1;
	public const BlockState FinishStarted = 2;
	public const BlockState FinishDone = 3;
}
```

---

### internal enum DeflateFlavor

```csharp
internal enum DeflateFlavor 
{
	public int value__; 
	public const DeflateFlavor Store = 0;
	public const DeflateFlavor Fast = 1;
	public const DeflateFlavor Slow = 2;
}
```

---

### public enum FlushType

```csharp
public enum FlushType 
{
	public int value__; 
	public const FlushType None = 0;
	public const FlushType Partial = 1;
	public const FlushType Sync = 2;
	public const FlushType Full = 3;
	public const FlushType Finish = 4;
}
```

---

### public enum CompressionLevel

```csharp
public enum CompressionLevel 
{
	public int value__; 
	public const CompressionLevel None = 0;
	public const CompressionLevel Level0 = 0;
	public const CompressionLevel BestSpeed = 1;
	public const CompressionLevel Level1 = 1;
	public const CompressionLevel Level2 = 2;
	public const CompressionLevel Level3 = 3;
	public const CompressionLevel Level4 = 4;
	public const CompressionLevel Level5 = 5;
	public const CompressionLevel Default = 6;
	public const CompressionLevel Level6 = 6;
	public const CompressionLevel Level7 = 7;
	public const CompressionLevel Level8 = 8;
	public const CompressionLevel BestCompression = 9;
	public const CompressionLevel Level9 = 9;
}
```

---

### public enum CompressionStrategy

```csharp
public enum CompressionStrategy 
{
	public int value__; 
	public const CompressionStrategy Default = 0;
	public const CompressionStrategy Filtered = 1;
	public const CompressionStrategy HuffmanOnly = 2;
}
```

---

### public enum CompressionMode

```csharp
public enum CompressionMode 
{
	public int value__; 
	public const CompressionMode Compress = 0;
	public const CompressionMode Decompress = 1;
}
```

---

### internal enum ZlibStreamFlavor

```csharp
internal enum ZlibStreamFlavor 
{
	public int value__; 
	public const ZlibStreamFlavor ZLIB = 1950;
	public const ZlibStreamFlavor DEFLATE = 1951;
	public const ZlibStreamFlavor GZIP = 1952;
}
```

---

### internal enum ZlibBaseStream.StreamMode

```csharp
internal enum ZlibBaseStream.StreamMode 
{
	public int value__; 
	public const ZlibBaseStream.StreamMode Writer = 0;
	public const ZlibBaseStream.StreamMode Reader = 1;
	public const ZlibBaseStream.StreamMode Undefined = 2;
}
```

---

### public enum Orientation

```csharp
public enum Orientation 
{
	public int value__; 
	public const Orientation CW = 0;
	public const Orientation CCW = 1;
	public const Orientation Collinear = 2;
}
```

---

### public enum TriangulationAlgorithm

```csharp
public enum TriangulationAlgorithm 
{
	public int value__; 
	public const TriangulationAlgorithm DTSweep = 0;
}
```

---

### public enum TriangulationMode

```csharp
public enum TriangulationMode 
{
	public int value__; 
	public const TriangulationMode Unconstrained = 0;
	public const TriangulationMode Constrained = 1;
	public const TriangulationMode Polygon = 2;
}
```

---

### public enum ShadowQuality

```csharp
public enum ShadowQuality 
{
	public int value__; 
	public const ShadowQuality Disabled = 0;
	public const ShadowQuality HardShadows = 1;
	public const ShadowQuality SoftShadows = 2;
}
```

---

### public enum ShadowResolution

```csharp
public enum ShadowResolution 
{
	public int value__; 
	public const ShadowResolution _256 = 256;
	public const ShadowResolution _512 = 512;
	public const ShadowResolution _1024 = 1024;
	public const ShadowResolution _2048 = 2048;
	public const ShadowResolution _4096 = 4096;
}
```

---

### public enum MsaaQuality

```csharp
public enum MsaaQuality 
{
	public int value__; 
	public const MsaaQuality Disabled = 1;
	public const MsaaQuality _2x = 2;
	public const MsaaQuality _4x = 4;
	public const MsaaQuality _8x = 8;
}
```

---

### public enum Downsampling

```csharp
public enum Downsampling 
{
	public int value__; 
	public const Downsampling None = 0;
	public const Downsampling _2xBilinear = 1;
	public const Downsampling _4xBox = 2;
	public const Downsampling _4xBilinear = 3;
}
```

---

### internal enum DefaultMaterialType

```csharp
internal enum DefaultMaterialType 
{
	public int value__; 
	public const DefaultMaterialType Standard = 0;
	public const DefaultMaterialType Particle = 1;
	public const DefaultMaterialType Terrain = 2;
	public const DefaultMaterialType Sprite = 3;
	public const DefaultMaterialType UnityBuiltinDefault = 4;
}
```

---

### public enum LightRenderingMode

```csharp
public enum LightRenderingMode 
{
	public int value__; 
	public const LightRenderingMode Disabled = 0;
	public const LightRenderingMode PerVertex = 2;
	public const LightRenderingMode PerPixel = 1;
}
```

---

### public enum ShaderVariantLogLevel

```csharp
public enum ShaderVariantLogLevel 
{
	public int value__; 
	public const ShaderVariantLogLevel Disabled = 0;
	public const ShaderVariantLogLevel OnlyUniversalRPShaders = 1;
	public const ShaderVariantLogLevel AllShaders = 2;
}
```

---

### public enum PipelineDebugLevel

```csharp
public enum PipelineDebugLevel 
{
	public int value__; 
	public const PipelineDebugLevel Disabled = 0;
	public const PipelineDebugLevel Profiling = 1;
}
```

---

### public enum RendererType

```csharp
public enum RendererType 
{
	public int value__; 
	public const RendererType Custom = 0;
	public const RendererType ForwardRenderer = 1;
	public const RendererType _2DRenderer = 2;
}
```

---

### public enum ColorGradingMode

```csharp
public enum ColorGradingMode 
{
	public int value__; 
	public const ColorGradingMode LowDynamicRange = 0;
	public const ColorGradingMode HighDynamicRange = 1;
}
```

---

### public enum StoreActionsOptimization

```csharp
public enum StoreActionsOptimization 
{
	public int value__; 
	public const StoreActionsOptimization Auto = 0;
	public const StoreActionsOptimization Discard = 1;
	public const StoreActionsOptimization Store = 2;
}
```

---

### public enum VolumeFrameworkUpdateMode

```csharp
public enum VolumeFrameworkUpdateMode 
{
	public int value__; 
	[InspectorNameAttribute] 
	public const VolumeFrameworkUpdateMode EveryFrame = 0;
	[InspectorNameAttribute] 
	public const VolumeFrameworkUpdateMode ViaScripting = 1;
	[InspectorNameAttribute] 
	public const VolumeFrameworkUpdateMode UsePipelineSettings = 2;
}
```

---

### public enum ShadowCascadesOption

```csharp
public enum ShadowCascadesOption 
{
	public int value__; 
	public const ShadowCascadesOption NoCascades = 0;
	public const ShadowCascadesOption TwoCascades = 1;
	public const ShadowCascadesOption FourCascades = 2;
}
```

---

### public enum RenderingMode

```csharp
public enum RenderingMode 
{
	public int value__; 
	public const RenderingMode Forward = 0;
	public const RenderingMode Deferred = 1;
}
```

---

### public enum DepthOfFieldMode

```csharp
public enum DepthOfFieldMode 
{
	public int value__; 
	public const DepthOfFieldMode Off = 0;
	public const DepthOfFieldMode Gaussian = 1;
	public const DepthOfFieldMode Bokeh = 2;
}
```

---

### public enum FilmGrainLookup

```csharp
public enum FilmGrainLookup 
{
	public int value__; 
	public const FilmGrainLookup Thin1 = 0;
	public const FilmGrainLookup Thin2 = 1;
	public const FilmGrainLookup Medium1 = 2;
	public const FilmGrainLookup Medium2 = 3;
	public const FilmGrainLookup Medium3 = 4;
	public const FilmGrainLookup Medium4 = 5;
	public const FilmGrainLookup Medium5 = 6;
	public const FilmGrainLookup Medium6 = 7;
	public const FilmGrainLookup Large01 = 8;
	public const FilmGrainLookup Large02 = 9;
	public const FilmGrainLookup Custom = 10;
}
```

---

### public enum MotionBlurMode

```csharp
public enum MotionBlurMode 
{
	public int value__; 
	public const MotionBlurMode CameraOnly = 0;
	public const MotionBlurMode CameraAndObjects = 1;
}
```

---

### public enum MotionBlurQuality

```csharp
public enum MotionBlurQuality 
{
	public int value__; 
	public const MotionBlurQuality Low = 0;
	public const MotionBlurQuality Medium = 1;
	public const MotionBlurQuality High = 2;
}
```

---

### public enum TonemappingMode

```csharp
public enum TonemappingMode 
{
	public int value__; 
	public const TonemappingMode None = 0;
	public const TonemappingMode Neutral = 1;
	public const TonemappingMode ACES = 2;
}
```

---

### public enum ScriptableRenderPassInput

```csharp
public enum ScriptableRenderPassInput 
{
	public int value__; 
	public const ScriptableRenderPassInput None = 0;
	public const ScriptableRenderPassInput Depth = 1;
	public const ScriptableRenderPassInput Normal = 2;
	public const ScriptableRenderPassInput Color = 4;
}
```

---

### public enum RenderPassEvent

```csharp
public enum RenderPassEvent 
{
	public int value__; 
	public const RenderPassEvent BeforeRendering = 0;
	public const RenderPassEvent BeforeRenderingShadows = 50;
	public const RenderPassEvent AfterRenderingShadows = 100;
	public const RenderPassEvent BeforeRenderingPrepasses = 150;
	public const RenderPassEvent AfterRenderingPrePasses = 200;
	public const RenderPassEvent BeforeRenderingOpaques = 250;
	public const RenderPassEvent AfterRenderingOpaques = 300;
	public const RenderPassEvent BeforeRenderingSkybox = 350;
	public const RenderPassEvent AfterRenderingSkybox = 400;
	public const RenderPassEvent BeforeRenderingTransparents = 450;
	public const RenderPassEvent AfterRenderingTransparents = 500;
	public const RenderPassEvent BeforeRenderingPostProcessing = 550;
	public const RenderPassEvent AfterRenderingPostProcessing = 600;
	public const RenderPassEvent AfterRendering = 1000;
}
```

---

### internal enum ScreenSpaceAmbientOcclusionSettings.DepthSource

```csharp
internal enum ScreenSpaceAmbientOcclusionSettings.DepthSource 
{
	public int value__; 
	public const ScreenSpaceAmbientOcclusionSettings.DepthSource Depth = 0;
	public const ScreenSpaceAmbientOcclusionSettings.DepthSource DepthNormals = 1;
}
```

---

### internal enum ScreenSpaceAmbientOcclusionSettings.NormalQuality

```csharp
internal enum ScreenSpaceAmbientOcclusionSettings.NormalQuality 
{
	public int value__; 
	public const ScreenSpaceAmbientOcclusionSettings.NormalQuality Low = 0;
	public const ScreenSpaceAmbientOcclusionSettings.NormalQuality Medium = 1;
	public const ScreenSpaceAmbientOcclusionSettings.NormalQuality High = 2;
}
```

---

### public enum SampleCount

```csharp
public enum SampleCount 
{
	public int value__; 
	public const SampleCount One = 1;
	public const SampleCount Two = 2;
	public const SampleCount Four = 4;
}
```

---

### public enum ShaderPathID

```csharp
public enum ShaderPathID 
{
	public int value__; 
	public const ShaderPathID Lit = 0;
	public const ShaderPathID SimpleLit = 1;
	public const ShaderPathID Unlit = 2;
	public const ShaderPathID TerrainLit = 3;
	public const ShaderPathID ParticlesLit = 4;
	public const ShaderPathID ParticlesSimpleLit = 5;
	public const ShaderPathID ParticlesUnlit = 6;
	public const ShaderPathID BakedLit = 7;
	public const ShaderPathID SpeedTree7 = 8;
	public const ShaderPathID SpeedTree7Billboard = 9;
	public const ShaderPathID SpeedTree8 = 10;
}
```

---

### public enum CameraOverrideOption

```csharp
public enum CameraOverrideOption 
{
	public int value__; 
	public const CameraOverrideOption Off = 0;
	public const CameraOverrideOption On = 1;
	public const CameraOverrideOption UsePipelineSettings = 2;
}
```

---

### public enum RendererOverrideOption

```csharp
public enum RendererOverrideOption 
{
	public int value__; 
	public const RendererOverrideOption Custom = 0;
	public const RendererOverrideOption UsePipelineSettings = 1;
}
```

---

### public enum AntialiasingMode

```csharp
public enum AntialiasingMode 
{
	public int value__; 
	public const AntialiasingMode None = 0;
	public const AntialiasingMode FastApproximateAntialiasing = 1;
	public const AntialiasingMode SubpixelMorphologicalAntiAliasing = 2;
}
```

---

### public enum CameraRenderType

```csharp
public enum CameraRenderType 
{
	public int value__; 
	public const CameraRenderType Base = 0;
	public const CameraRenderType Overlay = 1;
}
```

---

### public enum AntialiasingQuality

```csharp
public enum AntialiasingQuality 
{
	public int value__; 
	public const AntialiasingQuality Low = 0;
	public const AntialiasingQuality Medium = 1;
	public const AntialiasingQuality High = 2;
}
```

---

### public enum MixedLightingSetup

```csharp
public enum MixedLightingSetup 
{
	public int value__; 
	public const MixedLightingSetup None = 0;
	public const MixedLightingSetup ShadowMask = 1;
	public const MixedLightingSetup Subtractive = 2;
}
```

---

### internal enum URPProfileId

```csharp
internal enum URPProfileId 
{
	public int value__; 
	public const URPProfileId UniversalRenderTotal = 0;
	public const URPProfileId UpdateVolumeFramework = 1;
	public const URPProfileId RenderCameraStack = 2;
	public const URPProfileId AdditionalLightsShadow = 3;
	public const URPProfileId ColorGradingLUT = 4;
	public const URPProfileId CopyColor = 5;
	public const URPProfileId CopyDepth = 6;
	public const URPProfileId DepthNormalPrepass = 7;
	public const URPProfileId DepthPrepass = 8;
	public const URPProfileId DrawOpaqueObjects = 9;
	public const URPProfileId DrawTransparentObjects = 10;
	public const URPProfileId MainLightShadow = 11;
	public const URPProfileId ResolveShadows = 12;
	public const URPProfileId SSAO = 13;
	public const URPProfileId StopNaNs = 14;
	public const URPProfileId SMAA = 15;
	public const URPProfileId GaussianDepthOfField = 16;
	public const URPProfileId BokehDepthOfField = 17;
	public const URPProfileId MotionBlur = 18;
	public const URPProfileId PaniniProjection = 19;
	public const URPProfileId UberPostProcess = 20;
	public const URPProfileId Bloom = 21;
	public const URPProfileId FinalBlit = 22;
}
```

---

### internal enum LightFlag

```csharp
internal enum LightFlag 
{
	public int value__; 
	public const LightFlag SubtractiveMixedLighting = 4;
}
```

---

### internal enum DeferredLights.GBufferHandles

```csharp
internal enum DeferredLights.GBufferHandles 
{
	public int value__; 
	public const DeferredLights.GBufferHandles DepthAsColor = 0;
	public const DeferredLights.GBufferHandles Albedo = 1;
	public const DeferredLights.GBufferHandles SpecularMetallic = 2;
	public const DeferredLights.GBufferHandles NormalSmoothness = 3;
	public const DeferredLights.GBufferHandles Lighting = 4;
	public const DeferredLights.GBufferHandles ShadowMask = 5;
	public const DeferredLights.GBufferHandles Count = 6;
}
```

---

### internal enum StencilUsage

```csharp
internal enum StencilUsage 
{
	public int value__; 
	public const StencilUsage UserMask = 15;
	public const StencilUsage StencilLight = 16;
	public const StencilUsage MaterialMask = 96;
	public const StencilUsage MaterialUnlit = 0;
	public const StencilUsage MaterialLit = 32;
	public const StencilUsage MaterialSimpleLit = 64;
}
```

---

### public enum Light2D.LightType

```csharp
public enum Light2D.LightType 
{
	public int value__; 
	public const Light2D.LightType Parametric = 0;
	public const Light2D.LightType Freeform = 1;
	public const Light2D.LightType Sprite = 2;
	public const Light2D.LightType Point = 3;
	public const Light2D.LightType Global = 4;
}
```

---

### public enum Light2D.PointLightQuality

```csharp
public enum Light2D.PointLightQuality 
{
	public int value__; 
	public const Light2D.PointLightQuality Fast = 0;
	public const Light2D.PointLightQuality Accurate = 1;
}
```

---

### internal enum Light2DBlendStyle.TextureChannel

```csharp
internal enum Light2DBlendStyle.TextureChannel 
{
	public int value__; 
	public const Light2DBlendStyle.TextureChannel None = 0;
	public const Light2DBlendStyle.TextureChannel R = 1;
	public const Light2DBlendStyle.TextureChannel G = 2;
	public const Light2DBlendStyle.TextureChannel B = 3;
	public const Light2DBlendStyle.TextureChannel A = 4;
	public const Light2DBlendStyle.TextureChannel OneMinusR = 5;
	public const Light2DBlendStyle.TextureChannel OneMinusG = 6;
	public const Light2DBlendStyle.TextureChannel OneMinusB = 7;
	public const Light2DBlendStyle.TextureChannel OneMinusA = 8;
}
```

---

### internal enum Light2DBlendStyle.BlendMode

```csharp
internal enum Light2DBlendStyle.BlendMode 
{
	public int value__; 
	public const Light2DBlendStyle.BlendMode Additive = 0;
	public const Light2DBlendStyle.BlendMode Multiply = 1;
	public const Light2DBlendStyle.BlendMode Subtractive = 2;
	public const Light2DBlendStyle.BlendMode Custom = 99;
}
```

---

### public enum Renderer2DData.Renderer2DDefaultMaterialType

```csharp
public enum Renderer2DData.Renderer2DDefaultMaterialType 
{
	public int value__; 
	public const Renderer2DData.Renderer2DDefaultMaterialType Lit = 0;
	public const Renderer2DData.Renderer2DDefaultMaterialType Unlit = 1;
	public const Renderer2DData.Renderer2DDefaultMaterialType Custom = 2;
}
```

---

### public enum RenderQueueType

```csharp
public enum RenderQueueType 
{
	public int value__; 
	public const RenderQueueType Opaque = 0;
	public const RenderQueueType Transparent = 1;
}
```

---

### internal enum WindingRule

```csharp
internal enum WindingRule 
{
	public int value__; 
	public const WindingRule EvenOdd = 0;
	public const WindingRule NonZero = 1;
	public const WindingRule Positive = 2;
	public const WindingRule Negative = 3;
	public const WindingRule AbsGeqTwo = 4;
}
```

---

### internal enum ElementType

```csharp
internal enum ElementType 
{
	public int value__; 
	public const ElementType Polygons = 0;
	public const ElementType ConnectedPolygons = 1;
	public const ElementType BoundaryContours = 2;
}
```

---

### internal enum ContourOrientation

```csharp
internal enum ContourOrientation 
{
	public int value__; 
	public const ContourOrientation Original = 0;
	public const ContourOrientation Clockwise = 1;
	public const ContourOrientation CounterClockwise = 2;
}
```

---

### public enum AnimationPlayableAsset.LoopMode

```csharp
public enum AnimationPlayableAsset.LoopMode 
{
	public int value__; 
	[TooltipAttribute] 
	public const AnimationPlayableAsset.LoopMode UseSourceAsset = 0;
	[TooltipAttribute] 
	public const AnimationPlayableAsset.LoopMode On = 1;
	[TooltipAttribute] 
	public const AnimationPlayableAsset.LoopMode Off = 2;
}
```

---

### public enum MatchTargetFields

```csharp
public enum MatchTargetFields 
{
	public int value__; 
	public const MatchTargetFields PositionX = 1;
	public const MatchTargetFields PositionY = 2;
	public const MatchTargetFields PositionZ = 4;
	public const MatchTargetFields RotationX = 8;
	public const MatchTargetFields RotationY = 16;
	public const MatchTargetFields RotationZ = 32;
}
```

---

### public enum TrackOffset

```csharp
public enum TrackOffset 
{
	public int value__; 
	public const TrackOffset ApplyTransformOffsets = 0;
	public const TrackOffset ApplySceneOffsets = 1;
	public const TrackOffset Auto = 2;
}
```

---

### internal enum AppliedOffsetMode

```csharp
internal enum AppliedOffsetMode 
{
	public int value__; 
	public const AppliedOffsetMode NoRootTransform = 0;
	public const AppliedOffsetMode TransformOffset = 1;
	public const AppliedOffsetMode SceneOffset = 2;
	public const AppliedOffsetMode TransformOffsetLegacy = 3;
	public const AppliedOffsetMode SceneOffsetLegacy = 4;
	public const AppliedOffsetMode SceneOffsetEditor = 5;
	public const AppliedOffsetMode SceneOffsetLegacyEditor = 6;
}
```

---

### public enum TimelineClip.ClipExtrapolation

```csharp
public enum TimelineClip.ClipExtrapolation 
{
	public int value__; 
	public const TimelineClip.ClipExtrapolation None = 0;
	public const TimelineClip.ClipExtrapolation Hold = 1;
	public const TimelineClip.ClipExtrapolation Loop = 2;
	public const TimelineClip.ClipExtrapolation PingPong = 3;
	public const TimelineClip.ClipExtrapolation Continue = 4;
}
```

---

### public enum TimelineClip.BlendCurveMode

```csharp
public enum TimelineClip.BlendCurveMode 
{
	public int value__; 
	public const TimelineClip.BlendCurveMode Auto = 0;
	public const TimelineClip.BlendCurveMode Manual = 1;
}
```

---

### public enum TimelineAsset.DurationMode

```csharp
public enum TimelineAsset.DurationMode 
{
	public int value__; 
	public const TimelineAsset.DurationMode BasedOnClips = 0;
	public const TimelineAsset.DurationMode FixedLength = 1;
}
```

---

### public enum ClipCaps

```csharp
public enum ClipCaps 
{
	public int value__; 
	public const ClipCaps None = 0;
	public const ClipCaps Looping = 1;
	public const ClipCaps Extrapolation = 2;
	public const ClipCaps ClipIn = 4;
	public const ClipCaps SpeedMultiplier = 8;
	public const ClipCaps Blending = 16;
	public const ClipCaps AutoScale = 40;
	public const ClipCaps All = -1;
}
```

---

### public enum NotificationFlags

```csharp
public enum NotificationFlags 
{
	public short value__; 
	public const NotificationFlags TriggerInEditMode = 1;
	public const NotificationFlags Retroactive = 2;
	public const NotificationFlags TriggerOnce = 4;
}
```

---

### public enum TrackBindingFlags

```csharp
public enum TrackBindingFlags 
{
	public int value__; 
	public const TrackBindingFlags None = 0;
	public const TrackBindingFlags AllowCreateComponent = 1;
	public const TrackBindingFlags All = 1;
}
```

---

### public enum AstarPath.AstarDistribution

```csharp
public enum AstarPath.AstarDistribution 
{
	public int value__; 
	public const AstarPath.AstarDistribution WebsiteDownload = 0;
	public const AstarPath.AstarDistribution AssetStore = 1;
}
```

---

### public enum Seeker.ModifierPass

```csharp
public enum Seeker.ModifierPass 
{
	public int value__; 
	public const Seeker.ModifierPass PreProcess = 0;
	public const Seeker.ModifierPass PostProcess = 2;
}
```

---

### public enum AutoRepathPolicy.Mode

```csharp
public enum AutoRepathPolicy.Mode 
{
	public int value__; 
	public const AutoRepathPolicy.Mode Never = 0;
	public const AutoRepathPolicy.Mode EveryNSeconds = 1;
	public const AutoRepathPolicy.Mode Dynamic = 2;
}
```

---

### public enum GraphModifier.EventType

```csharp
public enum GraphModifier.EventType 
{
	public int value__; 
	public const GraphModifier.EventType PostScan = 1;
	public const GraphModifier.EventType PreScan = 2;
	public const GraphModifier.EventType LatePostScan = 4;
	public const GraphModifier.EventType PreUpdate = 8;
	public const GraphModifier.EventType PostUpdate = 16;
	public const GraphModifier.EventType PostCacheLoad = 32;
}
```

---

### public enum GraphUpdateThreading

```csharp
public enum GraphUpdateThreading 
{
	public int value__; 
	public const GraphUpdateThreading UnityThread = 0;
	public const GraphUpdateThreading SeparateThread = 1;
	public const GraphUpdateThreading UnityInit = 2;
	public const GraphUpdateThreading UnityPost = 4;
	public const GraphUpdateThreading SeparateAndUnityInit = 3;
}
```

---

### public enum PathLog

```csharp
public enum PathLog 
{
	public int value__; 
	public const PathLog None = 0;
	public const PathLog Normal = 1;
	public const PathLog Heavy = 2;
	public const PathLog InGame = 3;
	public const PathLog OnlyErrors = 4;
}
```

---

### public enum Heuristic

```csharp
public enum Heuristic 
{
	public int value__; 
	public const Heuristic Manhattan = 0;
	public const Heuristic DiagonalManhattan = 1;
	public const Heuristic Euclidean = 2;
	public const Heuristic None = 3;
}
```

---

### public enum GraphDebugMode

```csharp
public enum GraphDebugMode 
{
	public int value__; 
	public const GraphDebugMode SolidColor = 0;
	public const GraphDebugMode G = 1;
	public const GraphDebugMode H = 2;
	public const GraphDebugMode F = 3;
	public const GraphDebugMode Penalty = 4;
	public const GraphDebugMode Areas = 5;
	public const GraphDebugMode Tags = 6;
	public const GraphDebugMode HierarchicalNode = 7;
}
```

---

### public enum ThreadCount

```csharp
public enum ThreadCount 
{
	public int value__; 
	public const ThreadCount AutomaticLowLoad = -1;
	public const ThreadCount AutomaticHighLoad = -2;
	public const ThreadCount None = 0;
	public const ThreadCount One = 1;
	public const ThreadCount Two = 2;
	public const ThreadCount Three = 3;
	public const ThreadCount Four = 4;
	public const ThreadCount Five = 5;
	public const ThreadCount Six = 6;
	public const ThreadCount Seven = 7;
	public const ThreadCount Eight = 8;
}
```

---

### public enum PathState

```csharp
public enum PathState 
{
	public int value__; 
	public const PathState Created = 0;
	public const PathState PathQueue = 1;
	public const PathState Processing = 2;
	public const PathState ReturnQueue = 3;
	public const PathState Returned = 4;
}
```

---

### public enum PathCompleteState

```csharp
public enum PathCompleteState 
{
	public int value__; 
	public const PathCompleteState NotCalculated = 0;
	public const PathCompleteState Error = 1;
	public const PathCompleteState Complete = 2;
	public const PathCompleteState Partial = 3;
}
```

---

### public enum CloseToDestinationMode

```csharp
public enum CloseToDestinationMode 
{
	public int value__; 
	public const CloseToDestinationMode Stop = 0;
	public const CloseToDestinationMode ContinueToExactDestination = 1;
}
```

---

### public enum Side

```csharp
public enum Side 
{
	public byte value__; 
	public const Side Colinear = 0;
	public const Side Left = 1;
	public const Side Right = 2;
}
```

---

### public enum InspectorGridMode

```csharp
public enum InspectorGridMode 
{
	public int value__; 
	public const InspectorGridMode Grid = 0;
	public const InspectorGridMode IsometricGrid = 1;
	public const InspectorGridMode Hexagonal = 2;
	public const InspectorGridMode Advanced = 3;
}
```

---

### public enum OrientationMode

```csharp
public enum OrientationMode 
{
	public int value__; 
	public const OrientationMode ZAxisForward = 0;
	public const OrientationMode YAxisForward = 1;
}
```

---

### public enum ColliderType

```csharp
public enum ColliderType 
{
	public int value__; 
	public const ColliderType Sphere = 0;
	public const ColliderType Capsule = 1;
	public const ColliderType Ray = 2;
}
```

---

### public enum RayDirection

```csharp
public enum RayDirection 
{
	public int value__; 
	public const RayDirection Up = 0;
	public const RayDirection Down = 1;
	public const RayDirection Both = 2;
}
```

---

### public enum GridGraph.TextureData.ChannelUse

```csharp
public enum GridGraph.TextureData.ChannelUse 
{
	public int value__; 
	public const GridGraph.TextureData.ChannelUse None = 0;
	public const GridGraph.TextureData.ChannelUse Penalty = 1;
	public const GridGraph.TextureData.ChannelUse Position = 2;
	public const GridGraph.TextureData.ChannelUse WalkablePenalty = 3;
}
```

---

### public enum NumNeighbours

```csharp
public enum NumNeighbours 
{
	public int value__; 
	public const NumNeighbours Four = 0;
	public const NumNeighbours Eight = 1;
	public const NumNeighbours Six = 2;
}
```

---

### public enum RecastGraph.RelevantGraphSurfaceMode

```csharp
public enum RecastGraph.RelevantGraphSurfaceMode 
{
	public int value__; 
	public const RecastGraph.RelevantGraphSurfaceMode DoNotRequire = 0;
	public const RecastGraph.RelevantGraphSurfaceMode OnlyForCompletelyInsideTile = 1;
	public const RecastGraph.RelevantGraphSurfaceMode RequireForAll = 2;
}
```

---

### public enum HeuristicOptimizationMode

```csharp
public enum HeuristicOptimizationMode 
{
	public int value__; 
	public const HeuristicOptimizationMode None = 0;
	public const HeuristicOptimizationMode Random = 1;
	public const HeuristicOptimizationMode RandomSpreadOut = 2;
	public const HeuristicOptimizationMode Custom = 3;
}
```

---

### public enum RaycastModifier.Quality

```csharp
public enum RaycastModifier.Quality 
{
	public int value__; 
	public const RaycastModifier.Quality Low = 0;
	public const RaycastModifier.Quality Medium = 1;
	public const RaycastModifier.Quality High = 2;
	public const RaycastModifier.Quality Highest = 3;
}
```

---

### public enum SimpleSmoothModifier.SmoothType

```csharp
public enum SimpleSmoothModifier.SmoothType 
{
	public int value__; 
	public const SimpleSmoothModifier.SmoothType Simple = 0;
	public const SimpleSmoothModifier.SmoothType Bezier = 1;
	public const SimpleSmoothModifier.SmoothType OffsetSimple = 2;
	public const SimpleSmoothModifier.SmoothType CurvedNonuniform = 3;
}
```

---

### public enum StartEndModifier.Exactness

```csharp
public enum StartEndModifier.Exactness 
{
	public int value__; 
	public const StartEndModifier.Exactness SnapToNode = 0;
	public const StartEndModifier.Exactness Original = 1;
	public const StartEndModifier.Exactness Interpolate = 2;
	public const StartEndModifier.Exactness ClosestOnNode = 3;
	public const StartEndModifier.Exactness NodeConnection = 4;
}
```

---

### public enum NavmeshAdd.MeshType

```csharp
public enum NavmeshAdd.MeshType 
{
	public int value__; 
	public const NavmeshAdd.MeshType Rectangle = 0;
	public const NavmeshAdd.MeshType CustomMesh = 1;
}
```

---

### public enum NavmeshCut.MeshType

```csharp
public enum NavmeshCut.MeshType 
{
	public int value__; 
	public const NavmeshCut.MeshType Rectangle = 0;
	public const NavmeshCut.MeshType Circle = 1;
	public const NavmeshCut.MeshType CustomMesh = 2;
}
```

---

### public enum MultiTargetPath.HeuristicMode

```csharp
public enum MultiTargetPath.HeuristicMode 
{
	public int value__; 
	public const MultiTargetPath.HeuristicMode None = 0;
	public const MultiTargetPath.HeuristicMode Average = 1;
	public const MultiTargetPath.HeuristicMode MovingAverage = 2;
	public const MultiTargetPath.HeuristicMode Midpoint = 3;
	public const MultiTargetPath.HeuristicMode MovingMidpoint = 4;
	public const MultiTargetPath.HeuristicMode Sequential = 5;
}
```

---

### public enum BlockManager.BlockMode

```csharp
public enum BlockManager.BlockMode 
{
	public int value__; 
	public const BlockManager.BlockMode AllExceptSelector = 0;
	public const BlockManager.BlockMode OnlySelector = 1;
}
```

---

### public enum MovementPlane

```csharp
public enum MovementPlane 
{
	public int value__; 
	public const MovementPlane XZ = 0;
	public const MovementPlane XY = 1;
}
```

---

### public enum RVOLayer

```csharp
public enum RVOLayer 
{
	public int value__; 
	public const RVOLayer DefaultAgent = 1;
	public const RVOLayer DefaultObstacle = 2;
	public const RVOLayer Layer2 = 4;
	public const RVOLayer Layer3 = 8;
	public const RVOLayer Layer4 = 16;
	public const RVOLayer Layer5 = 32;
	public const RVOLayer Layer6 = 64;
	public const RVOLayer Layer7 = 128;
	public const RVOLayer Layer8 = 256;
	public const RVOLayer Layer9 = 512;
	public const RVOLayer Layer10 = 1024;
	public const RVOLayer Layer11 = 2048;
	public const RVOLayer Layer12 = 4096;
	public const RVOLayer Layer13 = 8192;
	public const RVOLayer Layer14 = 16384;
	public const RVOLayer Layer15 = 32768;
	public const RVOLayer Layer16 = 65536;
	public const RVOLayer Layer17 = 131072;
	public const RVOLayer Layer18 = 262144;
	public const RVOLayer Layer19 = 524288;
	public const RVOLayer Layer20 = 1048576;
	public const RVOLayer Layer21 = 2097152;
	public const RVOLayer Layer22 = 4194304;
	public const RVOLayer Layer23 = 8388608;
	public const RVOLayer Layer24 = 16777216;
	public const RVOLayer Layer25 = 33554432;
	public const RVOLayer Layer26 = 67108864;
	public const RVOLayer Layer27 = 134217728;
	public const RVOLayer Layer28 = 268435456;
	public const RVOLayer Layer29 = 536870912;
	public const RVOLayer Layer30 = 1073741824;
}
```

---

### public enum RVOObstacle.ObstacleVertexWinding

```csharp
public enum RVOObstacle.ObstacleVertexWinding 
{
	public int value__; 
	public const RVOObstacle.ObstacleVertexWinding KeepOut = 0;
	public const RVOObstacle.ObstacleVertexWinding KeepIn = 1;
}
```

---

### public enum TileHandler.CutMode

```csharp
public enum TileHandler.CutMode 
{
	public int value__; 
	public const TileHandler.CutMode CutAll = 1;
	public const TileHandler.CutMode CutDual = 2;
	public const TileHandler.CutMode CutExtra = 4;
}
```

---

### public enum ProceduralWorld.RotationRandomness

```csharp
public enum ProceduralWorld.RotationRandomness 
{
	public int value__; 
	public const ProceduralWorld.RotationRandomness AllAxes = 0;
	public const ProceduralWorld.RotationRandomness Y = 1;
}
```

---

### public enum CinemachineBrain.UpdateMethod

```csharp
public enum CinemachineBrain.UpdateMethod 
{
	public int value__; 
	public const CinemachineBrain.UpdateMethod FixedUpdate = 0;
	public const CinemachineBrain.UpdateMethod LateUpdate = 1;
	public const CinemachineBrain.UpdateMethod SmartUpdate = 2;
	public const CinemachineBrain.UpdateMethod ManualUpdate = 3;
}
```

---

### public enum CinemachineBrain.BrainUpdateMethod

```csharp
public enum CinemachineBrain.BrainUpdateMethod 
{
	public int value__; 
	public const CinemachineBrain.BrainUpdateMethod FixedUpdate = 0;
	public const CinemachineBrain.BrainUpdateMethod LateUpdate = 1;
}
```

---

### public enum CinemachineCollider.ResolutionStrategy

```csharp
public enum CinemachineCollider.ResolutionStrategy 
{
	public int value__; 
	public const CinemachineCollider.ResolutionStrategy PullCameraForward = 0;
	public const CinemachineCollider.ResolutionStrategy PreserveCameraHeight = 1;
	public const CinemachineCollider.ResolutionStrategy PreserveCameraDistance = 2;
}
```

---

### public enum CinemachineConfiner.Mode

```csharp
public enum CinemachineConfiner.Mode 
{
	public int value__; 
	public const CinemachineConfiner.Mode Confine2D = 0;
	public const CinemachineConfiner.Mode Confine3D = 1;
}
```

---

### public enum CinemachineDollyCart.UpdateMethod

```csharp
public enum CinemachineDollyCart.UpdateMethod 
{
	public int value__; 
	public const CinemachineDollyCart.UpdateMethod Update = 0;
	public const CinemachineDollyCart.UpdateMethod FixedUpdate = 1;
	public const CinemachineDollyCart.UpdateMethod LateUpdate = 2;
}
```

---

### public enum CinemachineStoryboard.FillStrategy

```csharp
public enum CinemachineStoryboard.FillStrategy 
{
	public int value__; 
	public const CinemachineStoryboard.FillStrategy BestFit = 0;
	public const CinemachineStoryboard.FillStrategy CropImageToFit = 1;
	public const CinemachineStoryboard.FillStrategy StretchToFit = 2;
}
```

---

### public enum CinemachineTargetGroup.PositionMode

```csharp
public enum CinemachineTargetGroup.PositionMode 
{
	public int value__; 
	public const CinemachineTargetGroup.PositionMode GroupCenter = 0;
	public const CinemachineTargetGroup.PositionMode GroupAverage = 1;
}
```

---

### public enum CinemachineTargetGroup.RotationMode

```csharp
public enum CinemachineTargetGroup.RotationMode 
{
	public int value__; 
	public const CinemachineTargetGroup.RotationMode Manual = 0;
	public const CinemachineTargetGroup.RotationMode GroupAverage = 1;
}
```

---

### public enum CinemachineTargetGroup.UpdateMethod

```csharp
public enum CinemachineTargetGroup.UpdateMethod 
{
	public int value__; 
	public const CinemachineTargetGroup.UpdateMethod Update = 0;
	public const CinemachineTargetGroup.UpdateMethod FixedUpdate = 1;
	public const CinemachineTargetGroup.UpdateMethod LateUpdate = 2;
}
```

---

### public enum CinemachineFramingTransposer.FramingMode

```csharp
public enum CinemachineFramingTransposer.FramingMode 
{
	public int value__; 
	public const CinemachineFramingTransposer.FramingMode Horizontal = 0;
	public const CinemachineFramingTransposer.FramingMode Vertical = 1;
	public const CinemachineFramingTransposer.FramingMode HorizontalAndVertical = 2;
	public const CinemachineFramingTransposer.FramingMode None = 3;
}
```

---

### public enum CinemachineFramingTransposer.AdjustmentMode

```csharp
public enum CinemachineFramingTransposer.AdjustmentMode 
{
	public int value__; 
	public const CinemachineFramingTransposer.AdjustmentMode ZoomOnly = 0;
	public const CinemachineFramingTransposer.AdjustmentMode DollyOnly = 1;
	public const CinemachineFramingTransposer.AdjustmentMode DollyThenZoom = 2;
}
```

---

### public enum CinemachineGroupComposer.FramingMode

```csharp
public enum CinemachineGroupComposer.FramingMode 
{
	public int value__; 
	public const CinemachineGroupComposer.FramingMode Horizontal = 0;
	public const CinemachineGroupComposer.FramingMode Vertical = 1;
	public const CinemachineGroupComposer.FramingMode HorizontalAndVertical = 2;
}
```

---

### public enum CinemachineGroupComposer.AdjustmentMode

```csharp
public enum CinemachineGroupComposer.AdjustmentMode 
{
	public int value__; 
	public const CinemachineGroupComposer.AdjustmentMode ZoomOnly = 0;
	public const CinemachineGroupComposer.AdjustmentMode DollyOnly = 1;
	public const CinemachineGroupComposer.AdjustmentMode DollyThenZoom = 2;
}
```

---

### public enum CinemachineOrbitalTransposer.Heading.HeadingDefinition

```csharp
public enum CinemachineOrbitalTransposer.Heading.HeadingDefinition 
{
	public int value__; 
	public const CinemachineOrbitalTransposer.Heading.HeadingDefinition PositionDelta = 0;
	public const CinemachineOrbitalTransposer.Heading.HeadingDefinition Velocity = 1;
	public const CinemachineOrbitalTransposer.Heading.HeadingDefinition TargetForward = 2;
	public const CinemachineOrbitalTransposer.Heading.HeadingDefinition WorldForward = 3;
}
```

---

### public enum CinemachinePOV.RecenterTargetMode

```csharp
public enum CinemachinePOV.RecenterTargetMode 
{
	public int value__; 
	public const CinemachinePOV.RecenterTargetMode None = 0;
	public const CinemachinePOV.RecenterTargetMode FollowTargetForward = 1;
	public const CinemachinePOV.RecenterTargetMode LookAtTargetForward = 2;
}
```

---

### public enum CinemachineTrackedDolly.CameraUpMode

```csharp
public enum CinemachineTrackedDolly.CameraUpMode 
{
	public int value__; 
	public const CinemachineTrackedDolly.CameraUpMode Default = 0;
	public const CinemachineTrackedDolly.CameraUpMode Path = 1;
	public const CinemachineTrackedDolly.CameraUpMode PathNoRoll = 2;
	public const CinemachineTrackedDolly.CameraUpMode FollowTarget = 3;
	public const CinemachineTrackedDolly.CameraUpMode FollowTargetNoRoll = 4;
}
```

---

### public enum CinemachineTransposer.BindingMode

```csharp
public enum CinemachineTransposer.BindingMode 
{
	public int value__; 
	public const CinemachineTransposer.BindingMode LockToTargetOnAssign = 0;
	public const CinemachineTransposer.BindingMode LockToTargetWithWorldUp = 1;
	public const CinemachineTransposer.BindingMode LockToTargetNoRoll = 2;
	public const CinemachineTransposer.BindingMode LockToTarget = 3;
	public const CinemachineTransposer.BindingMode WorldSpace = 4;
	public const CinemachineTransposer.BindingMode SimpleFollowWithWorldUp = 5;
}
```

---

### public enum CinemachineTransposer.AngularDampingMode

```csharp
public enum CinemachineTransposer.AngularDampingMode 
{
	public int value__; 
	public const CinemachineTransposer.AngularDampingMode Euler = 0;
	public const CinemachineTransposer.AngularDampingMode Quaternion = 1;
}
```

---

### public enum AxisState.SpeedMode

```csharp
public enum AxisState.SpeedMode 
{
	public int value__; 
	public const AxisState.SpeedMode MaxSpeed = 0;
	public const AxisState.SpeedMode InputValueGain = 1;
}
```

---

### public enum CameraState.BlendHintValue

```csharp
public enum CameraState.BlendHintValue 
{
	public int value__; 
	public const CameraState.BlendHintValue Nothing = 0;
	public const CameraState.BlendHintValue NoPosition = 1;
	public const CameraState.BlendHintValue NoOrientation = 2;
	public const CameraState.BlendHintValue NoTransform = 3;
	public const CameraState.BlendHintValue SphericalPositionBlend = 4;
	public const CameraState.BlendHintValue CylindricalPositionBlend = 8;
	public const CameraState.BlendHintValue RadialAimBlend = 16;
	public const CameraState.BlendHintValue IgnoreLookAtTarget = 32;
	public const CameraState.BlendHintValue NoLens = 64;
}
```

---

### public enum CinemachineBlendDefinition.Style

```csharp
public enum CinemachineBlendDefinition.Style 
{
	public int value__; 
	public const CinemachineBlendDefinition.Style Cut = 0;
	public const CinemachineBlendDefinition.Style EaseInOut = 1;
	public const CinemachineBlendDefinition.Style EaseIn = 2;
	public const CinemachineBlendDefinition.Style EaseOut = 3;
	public const CinemachineBlendDefinition.Style HardIn = 4;
	public const CinemachineBlendDefinition.Style HardOut = 5;
	public const CinemachineBlendDefinition.Style Linear = 6;
	public const CinemachineBlendDefinition.Style Custom = 7;
}
```

---

### public enum CinemachineCore.Stage

```csharp
public enum CinemachineCore.Stage 
{
	public int value__; 
	public const CinemachineCore.Stage Body = 0;
	public const CinemachineCore.Stage Aim = 1;
	public const CinemachineCore.Stage Noise = 2;
	public const CinemachineCore.Stage Finalize = 3;
}
```

---

### internal enum CinemachineCore.UpdateFilter

```csharp
internal enum CinemachineCore.UpdateFilter 
{
	public int value__; 
	public const CinemachineCore.UpdateFilter Fixed = 0;
	public const CinemachineCore.UpdateFilter Late = 1;
	public const CinemachineCore.UpdateFilter Smart = 8;
	public const CinemachineCore.UpdateFilter SmartFixed = 8;
	public const CinemachineCore.UpdateFilter SmartLate = 9;
}
```

---

### public enum CinemachinePathBase.PositionUnits

```csharp
public enum CinemachinePathBase.PositionUnits 
{
	public int value__; 
	public const CinemachinePathBase.PositionUnits PathUnits = 0;
	public const CinemachinePathBase.PositionUnits Distance = 1;
	public const CinemachinePathBase.PositionUnits Normalized = 2;
}
```

---

### public enum DocumentationSortingAttribute.Level

```csharp
public enum DocumentationSortingAttribute.Level 
{
	public int value__; 
	public const DocumentationSortingAttribute.Level Undoc = 0;
	public const DocumentationSortingAttribute.Level API = 1;
	public const DocumentationSortingAttribute.Level UserRef = 2;
}
```

---

### public enum CinemachineVirtualCameraBase.StandbyUpdateMode

```csharp
public enum CinemachineVirtualCameraBase.StandbyUpdateMode 
{
	public int value__; 
	public const CinemachineVirtualCameraBase.StandbyUpdateMode Never = 0;
	public const CinemachineVirtualCameraBase.StandbyUpdateMode Always = 1;
	public const CinemachineVirtualCameraBase.StandbyUpdateMode RoundRobin = 2;
}
```

---

### public enum CinemachineVirtualCameraBase.BlendHint

```csharp
public enum CinemachineVirtualCameraBase.BlendHint 
{
	public int value__; 
	public const CinemachineVirtualCameraBase.BlendHint None = 0;
	public const CinemachineVirtualCameraBase.BlendHint SphericalPosition = 1;
	public const CinemachineVirtualCameraBase.BlendHint CylindricalPosition = 2;
	public const CinemachineVirtualCameraBase.BlendHint ScreenSpaceAimWhenTargetsDiffer = 3;
}
```

---

### public enum TargetPositionCache.Mode

```csharp
public enum TargetPositionCache.Mode 
{
	public int value__; 
	public const TargetPositionCache.Mode Disabled = 0;
	public const TargetPositionCache.Mode Record = 1;
	public const TargetPositionCache.Mode Playback = 2;
}
```

---

### public enum UpdateTracker.UpdateClock

```csharp
public enum UpdateTracker.UpdateClock 
{
	public int value__; 
	public const UpdateTracker.UpdateClock Fixed = 0;
	public const UpdateTracker.UpdateClock Late = 1;
}
```

---

### public enum CinemachineTriggerAction.ActionSettings.Mode

```csharp
public enum CinemachineTriggerAction.ActionSettings.Mode 
{
	public int value__; 
	public const CinemachineTriggerAction.ActionSettings.Mode Custom = 0;
	public const CinemachineTriggerAction.ActionSettings.Mode PriorityBoost = 1;
	public const CinemachineTriggerAction.ActionSettings.Mode Activate = 2;
	public const CinemachineTriggerAction.ActionSettings.Mode Deactivate = 3;
	public const CinemachineTriggerAction.ActionSettings.Mode Enable = 4;
	public const CinemachineTriggerAction.ActionSettings.Mode Disable = 5;
	public const CinemachineTriggerAction.ActionSettings.Mode Play = 6;
	public const CinemachineTriggerAction.ActionSettings.Mode Stop = 7;
}
```

---

### public enum CinemachineTriggerAction.ActionSettings.TimeMode

```csharp
public enum CinemachineTriggerAction.ActionSettings.TimeMode 
{
	public int value__; 
	public const CinemachineTriggerAction.ActionSettings.TimeMode FromStart = 0;
	public const CinemachineTriggerAction.ActionSettings.TimeMode FromEnd = 1;
	public const CinemachineTriggerAction.ActionSettings.TimeMode BeforeNow = 2;
	public const CinemachineTriggerAction.ActionSettings.TimeMode AfterNow = 3;
}
```

---

### public enum CinemachineImpulseDefinition.RepeatMode

```csharp
public enum CinemachineImpulseDefinition.RepeatMode 
{
	public int value__; 
	public const CinemachineImpulseDefinition.RepeatMode Stretch = 0;
	public const CinemachineImpulseDefinition.RepeatMode Loop = 1;
}
```

---

### public enum CinemachineImpulseManager.ImpulseEvent.DirectionMode

```csharp
public enum CinemachineImpulseManager.ImpulseEvent.DirectionMode 
{
	public int value__; 
	public const CinemachineImpulseManager.ImpulseEvent.DirectionMode Fixed = 0;
	public const CinemachineImpulseManager.ImpulseEvent.DirectionMode RotateTowardSource = 1;
}
```

---

### public enum CinemachineImpulseManager.ImpulseEvent.DissipationMode

```csharp
public enum CinemachineImpulseManager.ImpulseEvent.DissipationMode 
{
	public int value__; 
	public const CinemachineImpulseManager.ImpulseEvent.DissipationMode LinearDecay = 0;
	public const CinemachineImpulseManager.ImpulseEvent.DissipationMode SoftDecay = 1;
	public const CinemachineImpulseManager.ImpulseEvent.DissipationMode ExponentialDecay = 2;
}
```

---

### public enum CinemachineVolumeSettings.FocusTrackingMode

```csharp
public enum CinemachineVolumeSettings.FocusTrackingMode 
{
	public int value__; 
	public const CinemachineVolumeSettings.FocusTrackingMode None = 0;
	public const CinemachineVolumeSettings.FocusTrackingMode LookAtTarget = 1;
	public const CinemachineVolumeSettings.FocusTrackingMode FollowTarget = 2;
	public const CinemachineVolumeSettings.FocusTrackingMode CustomTarget = 3;
	public const CinemachineVolumeSettings.FocusTrackingMode Camera = 4;
}
```

---

### public enum SoftMask.DownSamplingRate

```csharp
public enum SoftMask.DownSamplingRate 
{
	public int value__; 
	public const SoftMask.DownSamplingRate None = 0;
	public const SoftMask.DownSamplingRate x1 = 1;
	public const SoftMask.DownSamplingRate x2 = 2;
	public const SoftMask.DownSamplingRate x4 = 4;
	public const SoftMask.DownSamplingRate x8 = 8;
}
```

---

### public enum VisualEffectActivationBehaviour.AttributeType

```csharp
public enum VisualEffectActivationBehaviour.AttributeType 
{
	public int value__; 
	public const VisualEffectActivationBehaviour.AttributeType Float = 1;
	public const VisualEffectActivationBehaviour.AttributeType Float2 = 2;
	public const VisualEffectActivationBehaviour.AttributeType Float3 = 3;
	public const VisualEffectActivationBehaviour.AttributeType Float4 = 4;
	public const VisualEffectActivationBehaviour.AttributeType Int32 = 5;
	public const VisualEffectActivationBehaviour.AttributeType Uint32 = 6;
	public const VisualEffectActivationBehaviour.AttributeType Boolean = 17;
}
```

---

### public enum VFXMouseEventBinder.Activation

```csharp
public enum VFXMouseEventBinder.Activation 
{
	public int value__; 
	public const VFXMouseEventBinder.Activation OnMouseUp = 0;
	public const VFXMouseEventBinder.Activation OnMouseDown = 1;
	public const VFXMouseEventBinder.Activation OnMouseEnter = 2;
	public const VFXMouseEventBinder.Activation OnMouseExit = 3;
	public const VFXMouseEventBinder.Activation OnMouseOver = 4;
	public const VFXMouseEventBinder.Activation OnMouseDrag = 5;
}
```

---

### public enum VFXTriggerEventBinder.Activation

```csharp
public enum VFXTriggerEventBinder.Activation 
{
	public int value__; 
	public const VFXTriggerEventBinder.Activation OnEnter = 0;
	public const VFXTriggerEventBinder.Activation OnExit = 1;
	public const VFXTriggerEventBinder.Activation OnStay = 2;
}
```

---

### public enum VFXVisibilityEventBinder.Activation

```csharp
public enum VFXVisibilityEventBinder.Activation 
{
	public int value__; 
	public const VFXVisibilityEventBinder.Activation OnBecameVisible = 0;
	public const VFXVisibilityEventBinder.Activation OnBecameInvisible = 1;
}
```

---

### public enum VFXAudioSpectrumBinder.AudioSourceMode

```csharp
public enum VFXAudioSpectrumBinder.AudioSourceMode 
{
	public int value__; 
	public const VFXAudioSpectrumBinder.AudioSourceMode AudioSource = 0;
	public const VFXAudioSpectrumBinder.AudioSourceMode AudioListener = 1;
}
```

---

### public enum VFXEnabledBinder.Check

```csharp
public enum VFXEnabledBinder.Check 
{
	public int value__; 
	public const VFXEnabledBinder.Check ActiveInHierarchy = 0;
	public const VFXEnabledBinder.Check ActiveSelf = 1;
}
```

---

### public enum VFXHierarchyAttributeMapBinder.RadiusMode

```csharp
public enum VFXHierarchyAttributeMapBinder.RadiusMode 
{
	public int value__; 
	public const VFXHierarchyAttributeMapBinder.RadiusMode Fixed = 0;
	public const VFXHierarchyAttributeMapBinder.RadiusMode Interpolate = 1;
}
```

---

### public enum VFXRaycastBinder.Space

```csharp
public enum VFXRaycastBinder.Space 
{
	public int value__; 
	public const VFXRaycastBinder.Space Local = 0;
	public const VFXRaycastBinder.Space World = 1;
}
```

---

### public enum Baker.Mode

```csharp
public enum Baker.Mode 
{
	public int value__; 
	public const Baker.Mode AnimationClips = 0;
	public const Baker.Mode AnimationStates = 1;
	public const Baker.Mode PlayableDirector = 2;
	public const Baker.Mode Realtime = 3;
}
```

---

### public enum Axis

```csharp
public enum Axis 
{
	public int value__; 
	public const Axis X = 0;
	public const Axis Y = 1;
	public const Axis Z = 2;
}
```

---

### public enum BipedNaming.BoneType

```csharp
public enum BipedNaming.BoneType 
{
	public int value__; 
	public const BipedNaming.BoneType Unassigned = 0;
	public const BipedNaming.BoneType Spine = 1;
	public const BipedNaming.BoneType Head = 2;
	public const BipedNaming.BoneType Arm = 3;
	public const BipedNaming.BoneType Leg = 4;
	public const BipedNaming.BoneType Tail = 5;
	public const BipedNaming.BoneType Eye = 6;
}
```

---

### public enum BipedNaming.BoneSide

```csharp
public enum BipedNaming.BoneSide 
{
	public int value__; 
	public const BipedNaming.BoneSide Center = 0;
	public const BipedNaming.BoneSide Left = 1;
	public const BipedNaming.BoneSide Right = 2;
}
```

---

### public enum InterpolationMode

```csharp
public enum InterpolationMode 
{
	public int value__; 
	public const InterpolationMode None = 0;
	public const InterpolationMode InOutCubic = 1;
	public const InterpolationMode InOutQuintic = 2;
	public const InterpolationMode InOutSine = 3;
	public const InterpolationMode InQuintic = 4;
	public const InterpolationMode InQuartic = 5;
	public const InterpolationMode InCubic = 6;
	public const InterpolationMode InQuadratic = 7;
	public const InterpolationMode InElastic = 8;
	public const InterpolationMode InElasticSmall = 9;
	public const InterpolationMode InElasticBig = 10;
	public const InterpolationMode InSine = 11;
	public const InterpolationMode InBack = 12;
	public const InterpolationMode OutQuintic = 13;
	public const InterpolationMode OutQuartic = 14;
	public const InterpolationMode OutCubic = 15;
	public const InterpolationMode OutInCubic = 16;
	public const InterpolationMode OutInQuartic = 17;
	public const InterpolationMode OutElastic = 18;
	public const InterpolationMode OutElasticSmall = 19;
	public const InterpolationMode OutElasticBig = 20;
	public const InterpolationMode OutSine = 21;
	public const InterpolationMode OutBack = 22;
	public const InterpolationMode OutBackCubic = 23;
	public const InterpolationMode OutBackQuartic = 24;
	public const InterpolationMode BackInCubic = 25;
	public const InterpolationMode BackInQuartic = 26;
}
```

---

### public enum Finger.DOF

```csharp
public enum Finger.DOF 
{
	public int value__; 
	public const Finger.DOF One = 0;
	public const Finger.DOF Three = 1;
}
```

---

### public enum Grounding.Quality

```csharp
public enum Grounding.Quality 
{
	public int value__; 
	public const Grounding.Quality Fastest = 0;
	public const Grounding.Quality Simple = 1;
	public const Grounding.Quality Best = 2;
}
```

---

### public enum FBIKChain.Smoothing

```csharp
public enum FBIKChain.Smoothing 
{
	public int value__; 
	public const FBIKChain.Smoothing None = 0;
	public const FBIKChain.Smoothing Exponential = 1;
	public const FBIKChain.Smoothing Cubic = 2;
}
```

---

### public enum IKMappingLimb.BoneMapType

```csharp
public enum IKMappingLimb.BoneMapType 
{
	public int value__; 
	public const IKMappingLimb.BoneMapType Parent = 0;
	public const IKMappingLimb.BoneMapType Bone1 = 1;
	public const IKMappingLimb.BoneMapType Bone2 = 2;
	public const IKMappingLimb.BoneMapType Bone3 = 3;
}
```

---

### public enum FullBodyBipedEffector

```csharp
public enum FullBodyBipedEffector 
{
	public int value__; 
	public const FullBodyBipedEffector Body = 0;
	public const FullBodyBipedEffector LeftShoulder = 1;
	public const FullBodyBipedEffector RightShoulder = 2;
	public const FullBodyBipedEffector LeftThigh = 3;
	public const FullBodyBipedEffector RightThigh = 4;
	public const FullBodyBipedEffector LeftHand = 5;
	public const FullBodyBipedEffector RightHand = 6;
	public const FullBodyBipedEffector LeftFoot = 7;
	public const FullBodyBipedEffector RightFoot = 8;
}
```

---

### public enum FullBodyBipedChain

```csharp
public enum FullBodyBipedChain 
{
	public int value__; 
	public const FullBodyBipedChain LeftArm = 0;
	public const FullBodyBipedChain RightArm = 1;
	public const FullBodyBipedChain LeftLeg = 2;
	public const FullBodyBipedChain RightLeg = 3;
}
```

---

### public enum IKSolverLimb.BendModifier

```csharp
public enum IKSolverLimb.BendModifier 
{
	public int value__; 
	public const IKSolverLimb.BendModifier Animation = 0;
	public const IKSolverLimb.BendModifier Target = 1;
	public const IKSolverLimb.BendModifier Parent = 2;
	public const IKSolverLimb.BendModifier Arm = 3;
	public const IKSolverLimb.BendModifier Goal = 4;
}
```

---

### public enum IKSolverVR.Arm.ShoulderRotationMode

```csharp
public enum IKSolverVR.Arm.ShoulderRotationMode 
{
	public int value__; 
	public const IKSolverVR.Arm.ShoulderRotationMode YawPitch = 0;
	public const IKSolverVR.Arm.ShoulderRotationMode FromTo = 1;
}
```

---

### public enum IKSolverVR.PositionOffset

```csharp
public enum IKSolverVR.PositionOffset 
{
	public int value__; 
	public const IKSolverVR.PositionOffset Pelvis = 0;
	public const IKSolverVR.PositionOffset Chest = 1;
	public const IKSolverVR.PositionOffset Head = 2;
	public const IKSolverVR.PositionOffset LeftHand = 3;
	public const IKSolverVR.PositionOffset RightHand = 4;
	public const IKSolverVR.PositionOffset LeftFoot = 5;
	public const IKSolverVR.PositionOffset RightFoot = 6;
	public const IKSolverVR.PositionOffset LeftHeel = 7;
	public const IKSolverVR.PositionOffset RightHeel = 8;
}
```

---

### public enum IKSolverVR.RotationOffset

```csharp
public enum IKSolverVR.RotationOffset 
{
	public int value__; 
	public const IKSolverVR.RotationOffset Pelvis = 0;
	public const IKSolverVR.RotationOffset Chest = 1;
	public const IKSolverVR.RotationOffset Head = 2;
}
```

---

### public enum InteractionObject.WeightCurve.Type

```csharp
public enum InteractionObject.WeightCurve.Type 
{
	public int value__; 
	public const InteractionObject.WeightCurve.Type PositionWeight = 0;
	public const InteractionObject.WeightCurve.Type RotationWeight = 1;
	public const InteractionObject.WeightCurve.Type PositionOffsetX = 2;
	public const InteractionObject.WeightCurve.Type PositionOffsetY = 3;
	public const InteractionObject.WeightCurve.Type PositionOffsetZ = 4;
	public const InteractionObject.WeightCurve.Type Pull = 5;
	public const InteractionObject.WeightCurve.Type Reach = 6;
	public const InteractionObject.WeightCurve.Type RotateBoneWeight = 7;
	public const InteractionObject.WeightCurve.Type Push = 8;
	public const InteractionObject.WeightCurve.Type PushParent = 9;
	public const InteractionObject.WeightCurve.Type PoserWeight = 10;
	public const InteractionObject.WeightCurve.Type BendGoalWeight = 11;
}
```

---

### public enum Recoil.Handedness

```csharp
public enum Recoil.Handedness 
{
	public int value__; 
	public const Recoil.Handedness Right = 0;
	public const Recoil.Handedness Left = 1;
}
```

---

### public enum Navigator.State

```csharp
public enum Navigator.State 
{
	public int value__; 
	public const Navigator.State Idle = 0;
	public const Navigator.State Seeking = 1;
	public const Navigator.State OnPath = 2;
}
```

---

### public enum ObscuredPrefs.DataType

```csharp
public enum ObscuredPrefs.DataType 
{
	public byte value__; 
	public const ObscuredPrefs.DataType Unknown = 0;
	public const ObscuredPrefs.DataType Int = 5;
	public const ObscuredPrefs.DataType UInt = 10;
	public const ObscuredPrefs.DataType String = 15;
	public const ObscuredPrefs.DataType Float = 20;
	public const ObscuredPrefs.DataType Double = 25;
	public const ObscuredPrefs.DataType Decimal = 27;
	public const ObscuredPrefs.DataType Long = 30;
	public const ObscuredPrefs.DataType ULong = 32;
	public const ObscuredPrefs.DataType Bool = 35;
	public const ObscuredPrefs.DataType ByteArray = 40;
	public const ObscuredPrefs.DataType Vector2 = 45;
	public const ObscuredPrefs.DataType Vector3 = 50;
	public const ObscuredPrefs.DataType Quaternion = 55;
	public const ObscuredPrefs.DataType Color = 60;
	public const ObscuredPrefs.DataType Rect = 65;
}
```

---

### public enum ObscuredPrefs.DeviceLockLevel

```csharp
public enum ObscuredPrefs.DeviceLockLevel 
{
	public byte value__; 
	public const ObscuredPrefs.DeviceLockLevel None = 0;
	public const ObscuredPrefs.DeviceLockLevel Soft = 1;
	public const ObscuredPrefs.DeviceLockLevel Strict = 2;
}
```

---

### public enum TimeCheatingDetector.CheckResult

```csharp
public enum TimeCheatingDetector.CheckResult 
{
	public int value__; 
	public const TimeCheatingDetector.CheckResult Unknown = 0;
	public const TimeCheatingDetector.CheckResult CheckPassed = 5;
	public const TimeCheatingDetector.CheckResult WrongTimeDetected = 10;
	public const TimeCheatingDetector.CheckResult CheatDetected = 15;
	public const TimeCheatingDetector.CheckResult Error = 100;
}
```

---

### public enum TimeCheatingDetector.ErrorKind

```csharp
public enum TimeCheatingDetector.ErrorKind 
{
	public int value__; 
	public const TimeCheatingDetector.ErrorKind NoError = 0;
	public const TimeCheatingDetector.ErrorKind IncorrectUri = 3;
	public const TimeCheatingDetector.ErrorKind OnlineTimeError = 5;
	public const TimeCheatingDetector.ErrorKind NotStarted = 10;
	public const TimeCheatingDetector.ErrorKind AlreadyCheckingForCheat = 15;
	public const TimeCheatingDetector.ErrorKind Unknown = 100;
}
```

---

### public enum TimeCheatingDetector.RequestMethod

```csharp
public enum TimeCheatingDetector.RequestMethod 
{
	public int value__; 
	public const TimeCheatingDetector.RequestMethod Head = 0;
	public const TimeCheatingDetector.RequestMethod Get = 1;
}
```

---

### public enum BotEnemyInfo.DistanceControl

```csharp
public enum BotEnemyInfo.DistanceControl 
{
	public int value__; 
	public const BotEnemyInfo.DistanceControl None = 0;
	public const BotEnemyInfo.DistanceControl Close = 1;
	public const BotEnemyInfo.DistanceControl Escape = 2;
}
```

---

### public enum SocketItem.ItemType

```csharp
public enum SocketItem.ItemType 
{
	public int value__; 
	public const SocketItem.ItemType HeadSet = 0;
	public const SocketItem.ItemType EyeWear = 1;
	public const SocketItem.ItemType Backpack = 2;
	public const SocketItem.ItemType Thigh = 3;
	public const SocketItem.ItemType Waist = 4;
	public const SocketItem.ItemType Shoulder = 5;
}
```

---

### public enum DamageType

```csharp
public enum DamageType 
{
	public int value__; 
	public const DamageType Invalid = 0;
	public const DamageType Gun = 1;
	public const DamageType Knife = 2;
	public const DamageType Grenade = 3;
	public const DamageType Infect = 4;
	public const DamageType Other = 5;
}
```

---

### public enum NanoRoleSelect.Type

```csharp
public enum NanoRoleSelect.Type 
{
	public int value__; 
	public const NanoRoleSelect.Type None = 0;
	public const NanoRoleSelect.Type Normal = 1;
	public const NanoRoleSelect.Type Hero = 2;
	public const NanoRoleSelect.Type Terminataor = 3;
}
```

---

### public enum PlayerMdlInfo.FxType

```csharp
public enum PlayerMdlInfo.FxType 
{
	public int value__; 
	public const PlayerMdlInfo.FxType None = 0;
	public const PlayerMdlInfo.FxType HumanRespawn = 1;
	public const PlayerMdlInfo.FxType NanoInLowHp = 2;
	public const PlayerMdlInfo.FxType Absorbed = 3;
}
```

---

### public enum SkillKey

```csharp
public enum SkillKey 
{
	public int value__; 
	public const SkillKey F = 0;
	public const SkillKey G = 1;
	public const SkillKey H = 2;
	public const SkillKey WW = 3;
}
```

---

### internal enum PlayerVelocity.VelLockType

```csharp
internal enum PlayerVelocity.VelLockType 
{
	public int value__; 
	public const PlayerVelocity.VelLockType None = 0;
	public const PlayerVelocity.VelLockType Map = 1;
	public const PlayerVelocity.VelLockType Dash = 2;
}
```

---

### public enum Player.RespawnType

```csharp
public enum Player.RespawnType 
{
	public int value__; 
	public const Player.RespawnType Team = 0;
	public const Player.RespawnType Stay = 1;
	public const Player.RespawnType EnemyTeam = 2;
}
```

---

### public enum Team

```csharp
public enum Team 
{
	public int value__; 
	public const Team BlackList = 0;
	public const Team GlobalRisk = 1;
	public const Team Neutral = 2;
}
```

---

### public enum GameMode

```csharp
public enum GameMode 
{
	public int value__; 
	public const GameMode TeamDeath = 0;
	public const GameMode DeathMatch = 1;
	public const GameMode Special = 2;
	public const GameMode Nano3 = 3;
	public const GameMode Nano4 = 4;
	public const GameMode Nano6 = 5;
	public const GameMode Nano4_Terminator = 6;
}
```

---

### public enum HUD_PlayerRect.Type

```csharp
public enum HUD_PlayerRect.Type 
{
	public int value__; 
	public const HUD_PlayerRect.Type BL = 0;
	public const HUD_PlayerRect.Type GR = 1;
	public const HUD_PlayerRect.Type Dead = 2;
}
```

---

### public enum NanoRole

```csharp
public enum NanoRole 
{
	public int value__; 
	public const NanoRole Soldier = 0;
	public const NanoRole NanoGhost = 1;
	public const NanoRole Hulk = 2;
	public const NanoRole Nurse = 3;
	public const NanoRole Assassin = 4;
	public const NanoRole Ink = 5;
	public const NanoRole Jiangshi = 6;
	public const NanoRole Psycho = 7;
	public const NanoRole Terminator = 8;
	public const NanoRole GrandTerminator = 9;
	public const NanoRole ArmoredTerminator = 10;
	public const NanoRole DevilTerminator = 11;
	public const NanoRole ArchDevilTerminator = 12;
	public const NanoRole EvilTerminator = 13;
	public const NanoRole DemonTerminator = 14;
	public const NanoRole VoidTerminator = 15;
	public const NanoRole QueenTerminator = 16;
	public const NanoRole OutlawTerminator = 17;
	public const NanoRole Savior = 18;
	public const NanoRole HumanBoss = 19;
	public const NanoRole WomanHumanBoss = 20;
	public const NanoRole GhostBlade = 21;
	public const NanoRole DevilHunter = 22;
	public const NanoRole MasterHumanHero = 23;
	public const NanoRole MasterHunter = 24;
	public const NanoRole AsceticHero = 25;
	public const NanoRole MysticHero = 26;
	public const NanoRole MechanicHero = 27;
}
```

---

### public enum CommonHud_1.Type

```csharp
public enum CommonHud_1.Type 
{
	public int value__; 
	public const CommonHud_1.Type Image = 0;
	public const CommonHud_1.Type RawImage = 1;
	public const CommonHud_1.Type Text = 2;
}
```

---

### public enum HUD_KillMarkUnder.Type

```csharp
public enum HUD_KillMarkUnder.Type 
{
	public int value__; 
	public const HUD_KillMarkUnder.Type Common = 0;
	public const HUD_KillMarkUnder.Type Melee = 1;
	public const HUD_KillMarkUnder.Type Headshot = 2;
	public const HUD_KillMarkUnder.Type Headshot_Gold = 3;
}
```

---

### public enum HUD_ChatBox.Channel

```csharp
public enum HUD_ChatBox.Channel 
{
	public int value__; 
	public const HUD_ChatBox.Channel All = 0;
	public const HUD_ChatBox.Channel Teammate = 1;
	public const HUD_ChatBox.Channel Clan = 2;
}
```

---

### public enum HUD_Crosshair.Type

```csharp
public enum HUD_Crosshair.Type 
{
	public int value__; 
	public const HUD_Crosshair.Type Common = 0;
	public const HUD_Crosshair.Type FalCamo = 1;
}
```

---

### public enum HUD_KillMark.ShowType

```csharp
public enum HUD_KillMark.ShowType 
{
	public int value__; 
	public const HUD_KillMark.ShowType Normal = 0;
	public const HUD_KillMark.ShowType OnlyVoice = 1;
	public const HUD_KillMark.ShowType None = 2;
}
```

---

### public enum HUD_Weapon.AmmoBGType

```csharp
public enum HUD_Weapon.AmmoBGType 
{
	public int value__; 
	public const HUD_Weapon.AmmoBGType None = 0;
	public const HUD_Weapon.AmmoBGType Gun = 1;
	public const HUD_Weapon.AmmoBGType RepeatFireOFF = 2;
	public const HUD_Weapon.AmmoBGType RepeatFireOn = 3;
	public const HUD_Weapon.AmmoBGType Energy = 4;
}
```

---

### public enum HUD_Role.AceSign

```csharp
public enum HUD_Role.AceSign 
{
	public int value__; 
	public const HUD_Role.AceSign None = 0;
	public const HUD_Role.AceSign Gray = 1;
	public const HUD_Role.AceSign Gold = 2;
}
```

---

### public enum KeyInputState

```csharp
public enum KeyInputState 
{
	public int value__; 
	public const KeyInputState Unpressed = 0;
	public const KeyInputState Down = 1;
	public const KeyInputState Pressed = 2;
	public const KeyInputState Up = 3;
}
```

---

### public enum HeadShotType

```csharp
public enum HeadShotType 
{
	public int value__; 
	public const HeadShotType None = 0;
	public const HeadShotType White = 1;
	public const HeadShotType Gold = 2;
}
```

---

### public enum SpecialKillType

```csharp
public enum SpecialKillType 
{
	public int value__; 
	public const SpecialKillType None = 0;
	public const SpecialKillType FirstKill = 1;
	public const SpecialKillType LastKill = 2;
}
```

---

### public enum NanoKillType

```csharp
public enum NanoKillType 
{
	public int value__; 
	public const NanoKillType None = 0;
	public const NanoKillType NanoKillHero = 1;
	public const NanoKillType SoldierKillNanoByKnife = 2;
}
```

---

### public enum WeaponLimited

```csharp
public enum WeaponLimited 
{
	public int value__; 
	public const WeaponLimited None = 0;
	public const WeaponLimited Knife = 1;
	public const WeaponLimited HandGun = 2;
	public const WeaponLimited Sniper = 3;
}
```

---

### public enum CharacterModel.MoveDirection

```csharp
public enum CharacterModel.MoveDirection 
{
	public int value__; 
	public const CharacterModel.MoveDirection Idle = 0;
	public const CharacterModel.MoveDirection Left = 1;
	public const CharacterModel.MoveDirection Right = 2;
	public const CharacterModel.MoveDirection Forawrd = 3;
	public const CharacterModel.MoveDirection Backward = 4;
}
```

---

### public enum CharacterModel.Sex

```csharp
public enum CharacterModel.Sex 
{
	public int value__; 
	public const CharacterModel.Sex Man = 0;
	public const CharacterModel.Sex Woman = 1;
}
```

---

### public enum Model.Type

```csharp
public enum Model.Type 
{
	public int value__; 
	public const Model.Type Character = 0;
	public const Model.Type PlayerView = 1;
}
```

---

### public enum SupplyBox.Type

```csharp
public enum SupplyBox.Type 
{
	public int value__; 
	public const SupplyBox.Type Yellow = 0;
	public const SupplyBox.Type Red = 1;
	public const SupplyBox.Type Blue = 2;
}
```

---

### public enum Nano6ModeAsset.UpgradeAsset.TargetPos

```csharp
public enum Nano6ModeAsset.UpgradeAsset.TargetPos 
{
	public int value__; 
	public const Nano6ModeAsset.UpgradeAsset.TargetPos Ammo = 0;
	public const Nano6ModeAsset.UpgradeAsset.TargetPos Character = 1;
	public const Nano6ModeAsset.UpgradeAsset.TargetPos Radar = 2;
	public const Nano6ModeAsset.UpgradeAsset.TargetPos HPRegen = 3;
	public const Nano6ModeAsset.UpgradeAsset.TargetPos ThermalVision = 4;
}
```

---

### public enum SO_FxGroup.AttachType

```csharp
public enum SO_FxGroup.AttachType 
{
	public int value__; 
	public const SO_FxGroup.AttachType NodeAttach = 0;
	public const SO_FxGroup.AttachType PlayerView = 1;
	public const SO_FxGroup.AttachType PlayerSpace = 2;
}
```

---

### public enum WeaponClass

```csharp
public enum WeaponClass 
{
	public int value__; 
	public const WeaponClass Rifle = 0;
	public const WeaponClass Sniper = 1;
	public const WeaponClass MachineGun = 2;
	public const WeaponClass SubmachineGun = 3;
	public const WeaponClass ShotGun = 4;
	public const WeaponClass Pistol = 5;
	public const WeaponClass Knife = 6;
	public const WeaponClass Grenade = 7;
	public const WeaponClass FlashBang = 8;
	public const WeaponClass SmokeGrenade = 9;
}
```

---

### public enum SO_Item.Level

```csharp
public enum SO_Item.Level 
{
	public int value__; 
	public const SO_Item.Level Normal = 0;
	public const SO_Item.Level VVIP = 1;
}
```

---

### public enum UI_TopMenu.Frame

```csharp
public enum UI_TopMenu.Frame 
{
	public int value__; 
	public const UI_TopMenu.Frame GameRoom = 0;
	public const UI_TopMenu.Frame Inven = 1;
}
```

---

### public enum ShootPosture

```csharp
public enum ShootPosture 
{
	public int value__; 
	public const ShootPosture StandIdle = 0;
	public const ShootPosture CrouchIdle = 1;
	public const ShootPosture StandRun = 2;
	public const ShootPosture CrouchRun = 3;
	public const ShootPosture Floating = 4;
}
```

---

### public enum WPN_Gun.SemiGunFireLinkState

```csharp
public enum WPN_Gun.SemiGunFireLinkState 
{
	public int value__; 
	public const WPN_Gun.SemiGunFireLinkState None = 0;
	public const WPN_Gun.SemiGunFireLinkState Try = 1;
	public const WPN_Gun.SemiGunFireLinkState Finish = 2;
}
```

---

### public enum WPN_Knife.KnifeAttackType

```csharp
public enum WPN_Knife.KnifeAttackType 
{
	public int value__; 
	public const WPN_Knife.KnifeAttackType None = 0;
	public const WPN_Knife.KnifeAttackType Combo1 = 1;
	public const WPN_Knife.KnifeAttackType Combo2 = 2;
	public const WPN_Knife.KnifeAttackType Bigshot = 3;
	public const WPN_Knife.KnifeAttackType Other = 4;
}
```

---

### public enum Weapon.SlotType

```csharp
public enum Weapon.SlotType 
{
	public int value__; 
	public const Weapon.SlotType Normal = 0;
	public const Weapon.SlotType Special = 1;
	public const Weapon.SlotType Temporary = 2;
	public const Weapon.SlotType FKey = 3;
}
```

---

### public enum ItemAttribute.Type

```csharp
public enum ItemAttribute.Type 
{
	public int value__; 
	public const ItemAttribute.Type ClipBuff = 0;
}
```

---

### public enum DataBaseExample.EnumExample

```csharp
public enum DataBaseExample.EnumExample 
{
	public int value__; 
	public const DataBaseExample.EnumExample None = 0;
	public const DataBaseExample.EnumExample Value1 = 1;
	public const DataBaseExample.EnumExample Value2 = 2;
	public const DataBaseExample.EnumExample Value3 = 3;
	public const DataBaseExample.EnumExample Value4 = 4;
	public const DataBaseExample.EnumExample Value5 = 5;
	public const DataBaseExample.EnumExample Value6 = 6;
}
```

---

