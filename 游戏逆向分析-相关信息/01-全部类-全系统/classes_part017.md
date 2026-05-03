# 游戏类定义 (Part 17/21)

共 200 个类 (总序号 3201 - 3400)

---

## StreamReader（流读取器）

**继承**: TextReader（文本读取器）

### 字段 (17)

- `StreamReader Null`（流读取器 Null）(偏移: 0x0)
- `Stream stream`（流 stream）(偏移: 0xC)
- `Encoding encoding`（编码 encoding）(偏移: 0x10)
- `Decoder decoder`（Decoder decoder）(偏移: 0x14)
- `byte[] byteBuffer`（byte[] byte缓冲区）(偏移: 0x18)
- `char[] charBuffer`（char[] char缓冲区）(偏移: 0x1C)
- `byte[] _preamble`（byte[] _preamble）(偏移: 0x20)
- `int charPos`（int charPos）(偏移: 0x24)
- `int charLen`（int charLen）(偏移: 0x28)
- `int byteLen`（int byteLen）(偏移: 0x2C)
- `int bytePos`（int bytePos）(偏移: 0x30)
- `int _maxCharsPerBuffer`（int _maxCharsPer缓冲区）(偏移: 0x34)
- `bool _detectEncoding`（bool _detectEncoding）(偏移: 0x38)
- `bool _checkPreamble`（bool _checkPreamble）(偏移: 0x0)
- `bool _isBlocked`（bool _isBlocked）(偏移: 0x0)
- `bool _closable`（bool _closable）(偏移: 0x0)
- `Task _asyncReadTask`（Task _asyncReadTask）(偏移: 0x0)

### 方法 (18)

- `int get_DefaultBufferSize()`
  （int get_默认的缓冲区大小（））
- `void CheckAsyncTaskInProgress()`
  （void 检查异步TaskInProgress（））
- `void Init(Stream stream, Encoding encoding, bool detectEncodingFromByteOrderMarks, int bufferSize, bool leaveOpen)`
  （void 初始化（流 stream, Encoding encoding, bool detectEncodingFromByteOrderMarks, int bufferSize, bool leaveOpen））
- `void Init(Stream stream)`
  （void 初始化（流 stream））
- `void Close()`
  （void 关闭（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `bool get_LeaveOpen()`
  （bool get_Leave打开（））
- `int Peek()`
  （整数 查看（））
- `bool DataAvailable()`
  （bool 数据Available（））
- `int Read()`
  （整数 读取（））
- `int Read([In] [Out] char[] buffer, int index, int count)`
  （int Read（[In] [Out] char[] buffer, int index, int count））
- `string ReadToEnd()`
  （字符串 读取到结束（））
- `void CompressBuffer(int n)`
  （void Compress缓冲区（int n））
- `void DetectEncoding()`
  （void DetectEncoding（））
- `bool IsPreamble()`
  （bool 是否Preamble（））
- `int ReadBuffer()`
  （int Read缓冲区（））
- `int ReadBuffer(char[] userBuffer, int userOffset, int desiredChars, out bool readToUserBuffer)`
  （int Read缓冲区（char[] userBuffer, int userOffset, int desiredChars, out bool readToUserBuffer））
- `string ReadLine()`
  （字符串 读取行（））

---

## StreamReader.NullStreamReader（流Reader.Null流读取器）

**继承**: StreamReader（流读取器）

### 方法 (7)

- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `int Peek()`
  （整数 查看（））
- `int Read()`
  （整数 读取（））
- `int Read(char[] buffer, int index, int count)`
  （int Read（char[] buffer, int index, int count））
- `string ReadLine()`
  （字符串 读取行（））
- `string ReadToEnd()`
  （字符串 读取到结束（））
- `int ReadBuffer()`
  （int Read缓冲区（））

---

## StreamWriter（流写入器）

**继承**: TextWriter（文本写入器）

### 字段 (13)

- `StreamWriter Null`（流写入器 Null）(偏移: 0x0)
- `Stream stream`（流 stream）(偏移: 0x14)
- `Encoding encoding`（编码 encoding）(偏移: 0x18)
- `Encoder encoder`（Encoder encoder）(偏移: 0x1C)
- `byte[] byteBuffer`（byte[] byte缓冲区）(偏移: 0x20)
- `char[] charBuffer`（char[] char缓冲区）(偏移: 0x24)
- `int charPos`（int charPos）(偏移: 0x28)
- `int charLen`（int charLen）(偏移: 0x2C)
- `bool autoFlush`（bool autoFlush）(偏移: 0x30)
- `bool haveWrittenPreamble`（bool haveWrittenPreamble）(偏移: 0x31)
- `bool closable`（bool closable）(偏移: 0x32)
- `Task _asyncWriteTask`（Task _asyncWriteTask）(偏移: 0x34)
- `Encoding _UTF8NoBOM`（Encoding _UTF8NoBOM）(偏移: 0x4)

### 方法 (14)

- `void CheckAsyncTaskInProgress()`
  （void 检查异步TaskInProgress（））
- `Encoding get_UTF8NoBOM()`
  （Encoding get_UTF8NoBOM（））
- `void Init(Stream streamArg, Encoding encodingArg, int bufferSize, bool shouldLeaveOpen)`
  （void 初始化（流 streamArg, Encoding encodingArg, int bufferSize, bool shouldLeaveOpen））
- `Stream CreateFile(string path, bool append, bool checkHost)`
  （流 创建文件（string path, bool append, bool checkHost））
- `void Close()`
  （void 关闭（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `void Flush()`
  （void 刷新（））
- `void Flush(bool flushStream, bool flushEncoder)`
  （void Flush（bool flushStream, bool flushEncoder））
- `void set_AutoFlush(bool value)`
  （void set_自动Flush（bool value））
- `bool get_LeaveOpen()`
  （bool get_Leave打开（））
- `void Write(char value)`
  （void 写入（字符 value））
- `void Write(char[] buffer)`
  （void Write（char[] buffer））
- `void Write(char[] buffer, int index, int count)`
  （void 写入（字符[] buffer, 整数 index, 整数 count））
- `void Write(string value)`
  （void 写入（字符串 value））

---

## StreamingContext（StreamingContext）

### 字段 (2)

- `object m_additionalContext`（object m_additionalContext）(偏移: 0x0)
- `StreamingContextStates m_state`（StreamingContextStates m_state）(偏移: 0x4)

### 方法 (3)

- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `StreamingContextStates get_State()`
  （StreamingContextStates get_状态（））

---

## StreamingContextStates（StreamingContextStates）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## String（字符串）

**继承**: IComparable, ICloneable, IConvertible, IEnumerable, IComparable<string>, IEnumerable<char>, IEquatable<string>（IComparable, ICloneable, IConvertible, IEnumerable, IComparable<string>, IEnumerable<char>, IEquatable<string>）

### 字段 (3)

- `int m_stringLength`（int m_stringLength）(偏移: 0x8)
- `char m_firstChar`（char m_firstChar）(偏移: 0xC)
- `string Empty`（string 空）(偏移: 0x0)

### 方法 (151)

- `string Join(string separator, string[] value)`
  （string Join（string separator, string[] value））
- `string Join(string separator, string[] value, int startIndex, int count)`
  （string Join（string separator, string[] value, int startIndex, int count））
- `int CompareOrdinalIgnoreCaseHelper(string strA, string strB)`
  （int CompareOrdinalIgnoreCase辅助器（string strA, string strB））
- `bool EqualsHelper(string strA, string strB)`
  （bool Equals辅助器（string strA, string strB））
- `int CompareOrdinalHelper(string strA, string strB)`
  （int CompareOrdinal辅助器（string strA, string strB））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(string value)`
  （bool Equals（string value））
- `bool Equals(string value, StringComparison comparisonType)`
  （bool Equals（string value, 字符串Comparison comparisonType））
- `bool Equals(string a, string b)`
  （bool Equals（string a, string b））
- `bool Equals(string a, string b, StringComparison comparisonType)`
  （bool Equals（string a, string b, 字符串Comparison comparisonType））
- `bool op_Equality(string a, string b)`
  （bool op_Equality（string a, string b））
- `bool op_Inequality(string a, string b)`
  （bool op_Inequality（string a, string b））
- `char get_Chars(int index)`
  （char get_Chars（int index））
- `void CopyTo(int sourceIndex, char[] destination, int destinationIndex, int count)`
  （void 复制To（int sourceIndex, char[] destination, int destinationIndex, int count））
- `char[] ToCharArray()`
  （char[] ToChar数组（））
- `char[] ToCharArray(int startIndex, int length)`
  （char[] ToChar数组（int startIndex, int length））
- `bool IsNullOrEmpty(string value)`
  （bool 是否NullOr空（string value））
- `bool IsNullOrWhiteSpace(string value)`
  （bool 是否NullOrWhiteSpace（string value））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `int GetLegacyNonRandomizedHashCode()`
  （int 获取LegacyNonRandomizedHashCode（））
- `string[] Split(char[] separator)`
  （string[] Split（char[] separator））
- `string[] Split(char[] separator, int count)`
  （string[] Split（char[] separator, int count））
- `string[] Split(char[] separator, StringSplitOptions options)`
  （string[] Split（char[] separator, 字符串SplitOptions options））
- `string[] SplitInternal(char[] separator, int count, StringSplitOptions options)`
  （string[] Split内部的（char[] separator, int count, 字符串SplitOptions options））
- `string[] InternalSplitKeepEmptyEntries(int[] sepList, int[] lengthList, int numReplaces, int count)`
  （string[] 内部的SplitKeep空Entries（int[] sepList, int[] lengthList, int numReplaces, int count））
- `string[] InternalSplitOmitEmptyEntries(int[] sepList, int[] lengthList, int numReplaces, int count)`
  （string[] 内部的SplitOmit空Entries（int[] sepList, int[] lengthList, int numReplaces, int count））
- `int MakeSeparatorList(char[] separator, ref int[] sepList)`
  （int MakeSeparator列表（char[] separator, ref int[] sepList））
- `string Substring(int startIndex)`
  （string Substring（int startIndex））
- `string Substring(int startIndex, int length)`
  （string Substring（int startIndex, int length））
- `string InternalSubString(int startIndex, int length)`
  （string 内部的子字符串（int startIndex, int length））
- `string Trim(char[] trimChars)`
  （string Trim（char[] trimChars））
- `string TrimEnd(char[] trimChars)`
  （string Trim结束（char[] trimChars））
- `string CreateStringFromEncoding(byte* bytes, int byteLength, Encoding encoding)`
  （string 创建字符串FromEncoding（byte* bytes, int byteLength, Encoding encoding））
- `string Normalize(NormalizationForm normalizationForm)`
  （string Normalize（NormalizationForm normalizationForm））
- `string FastAllocateString(int length)`
  （string FastAllocate字符串（int length））
- `void FillStringChecked(string dest, int destPos, string src)`
  （void Fill字符串Checked（string dest, int destPos, string src））
- `void wstrcpy(char* dmem, char* smem, int charCount)`
  （void wstrcpy（char* dmem, char* smem, int charCount））
- `string CtorCharArray(char[] value)`
  （string CtorChar数组（char[] value））
- `string CtorCharArrayStartLength(char[] value, int startIndex, int length)`
  （string CtorChar数组开始Length（char[] value, int startIndex, int length））
- `int wcslen(char* ptr)`
  （int wcslen（char* ptr））
- `string CtorCharPtr(char* ptr)`
  （string CtorCharPtr（char* ptr））
- `string CtorCharPtrStartLength(char* ptr, int startIndex, int length)`
  （string CtorCharPtr开始Length（char* ptr, int startIndex, int length））
- `int Compare(string strA, string strB, StringComparison comparisonType)`
  （int Compare（string strA, string strB, 字符串Comparison comparisonType））
- `int Compare(string strA, string strB, bool ignoreCase, CultureInfo culture)`
  （int Compare（string strA, string strB, bool ignoreCase, Culture信息 culture））
- `int Compare(string strA, int indexA, string strB, int indexB, int length)`
  （int Compare（string strA, int indexA, string strB, int indexB, int length））
- `int Compare(string strA, int indexA, string strB, int indexB, int length, CultureInfo culture, CompareOptions options)`
  （int Compare（string strA, int indexA, string strB, int indexB, int length, Culture信息 culture, CompareOptions options））
- `int Compare(string strA, int indexA, string strB, int indexB, int length, StringComparison comparisonType)`
  （int Compare（string strA, int indexA, string strB, int indexB, int length, 字符串Comparison comparisonType））
- `int CompareTo(object value)`
  （整数 比较到（对象 value））
- `int CompareTo(string strB)`
  （int CompareTo（string strB））
- `int CompareOrdinal(string strA, string strB)`
  （int CompareOrdinal（string strA, string strB））
- `int CompareOrdinal(string strA, int indexA, string strB, int indexB, int length)`
  （int CompareOrdinal（string strA, int indexA, string strB, int indexB, int length））
- `bool Contains(string value)`
  （bool Contains（string value））
- `bool EndsWith(string value)`
  （bool EndsWith（string value））
- `bool EndsWith(string value, StringComparison comparisonType)`
  （bool EndsWith（string value, 字符串Comparison comparisonType））
- `bool EndsWith(char value)`
  （bool EndsWith（char value））
- `int IndexOf(char value)`
  （int 索引Of（char value））
- `int IndexOf(char value, int startIndex)`
  （int 索引Of（char value, int startIndex））
- `int IndexOfAny(char[] anyOf)`
  （int 索引Of任意（char[] anyOf））
- `int IndexOfAny(char[] anyOf, int startIndex)`
  （int 索引Of任意（char[] anyOf, int startIndex））
- `int IndexOf(string value)`
  （int 索引Of（string value））
- `int IndexOf(string value, StringComparison comparisonType)`
  （int 索引Of（string value, 字符串Comparison comparisonType））
- `int IndexOf(string value, int startIndex, int count, StringComparison comparisonType)`
  （int 索引Of（string value, int startIndex, int count, 字符串Comparison comparisonType））
- `int LastIndexOf(char value)`
  （int 最后一个索引Of（char value））
- `int LastIndexOf(char value, int startIndex)`
  （int 最后一个索引Of（char value, int startIndex））
- `int LastIndexOfAny(char[] anyOf)`
  （int 最后一个索引Of任意（char[] anyOf））
- `int LastIndexOfAny(char[] anyOf, int startIndex)`
  （int 最后一个索引Of任意（char[] anyOf, int startIndex））
- `int LastIndexOf(string value)`
  （int 最后一个索引Of（string value））
- `int LastIndexOf(string value, StringComparison comparisonType)`
  （int 最后一个索引Of（string value, 字符串Comparison comparisonType））
- `int LastIndexOf(string value, int startIndex, int count, StringComparison comparisonType)`
  （int 最后一个索引Of（string value, int startIndex, int count, 字符串Comparison comparisonType））
- `string PadLeft(int totalWidth)`
  （string Pad左（int totalWidth））
- `string PadRight(int totalWidth)`
  （string Pad右（int totalWidth））
- `string PadRight(int totalWidth, char paddingChar)`
  （string Pad右（int totalWidth, char paddingChar））
- `bool StartsWith(string value)`
  （bool StartsWith（string value））
- `bool StartsWith(string value, StringComparison comparisonType)`
  （bool StartsWith（string value, 字符串Comparison comparisonType））
- `string ToLower()`
  （string To下半身（））
- `string ToLower(CultureInfo culture)`
  （string To下半身（Culture信息 culture））
- `string ToLowerInvariant()`
  （string To下半身Invariant（））
- `string ToUpper()`
  （string To上半身（））
- `string ToUpper(CultureInfo culture)`
  （string To上半身（Culture信息 culture））
- `string ToUpperInvariant()`
  （string To上半身Invariant（））
- `string ToString()`
  （字符串 转字符串（））
- `string ToString(IFormatProvider provider)`
  （字符串 转字符串（I格式化提供者 provider））
- `object Clone()`
  （对象 克隆（））
- `bool IsBOMWhitespace(char c)`
  （bool 是否BOMWhitespace（char c））
- `string Trim()`
  （string Trim（））
- `string TrimHelper(int trimType)`
  （string Trim辅助器（int trimType））
- `string TrimHelper(char[] trimChars, int trimType)`
  （string Trim辅助器（char[] trimChars, int trimType））
- `string CreateTrimmedString(int start, int end)`
  （string 创建Trimmed字符串（int start, int end））
- `string Insert(int startIndex, string value)`
  （string Insert（int startIndex, string value））
- `string Replace(char oldChar, char newChar)`
  （string Replace（char oldChar, char newChar））
- `string Replace(string oldValue, string newValue)`
  （string Replace（string oldValue, string newValue））
- `string Remove(int startIndex, int count)`
  （string 移除（int startIndex, int count））
- `string Format(string format, object arg0)`
  （string 格式化（string format, object arg0））
- `string Format(string format, object arg0, object arg1)`
  （string 格式化（string format, object arg0, object arg1））
- `string Format(string format, object arg0, object arg1, object arg2)`
  （string 格式化（string format, object arg0, object arg1, object arg2））
- `string Format(string format, object[] args)`
  （string 格式化（string format, object[] args））
- `string Format(IFormatProvider provider, string format, object arg0)`
  （string 格式化（I格式化提供者 provider, string format, object arg0））
- `string Format(IFormatProvider provider, string format, object arg0, object arg1)`
  （string 格式化（I格式化提供者 provider, string format, object arg0, object arg1））
- `string Format(IFormatProvider provider, string format, object arg0, object arg1, object arg2)`
  （string 格式化（I格式化提供者 provider, string format, object arg0, object arg1, object arg2））
- `string Format(IFormatProvider provider, string format, object[] args)`
  （string 格式化（I格式化提供者 provider, string format, object[] args））
- `string FormatHelper(IFormatProvider provider, string format, ParamsArray args)`
  （string 格式化辅助器（I格式化提供者 provider, string format, Params数组 args））
- `string Copy(string str)`
  （string 复制（string str））
- `string Concat(object arg0)`
  （string Concat（object arg0））
- `string Concat(object arg0, object arg1)`
  （string Concat（object arg0, object arg1））
- `string Concat(object arg0, object arg1, object arg2)`
  （string Concat（object arg0, object arg1, object arg2））
- `string Concat(object[] args)`
  （string Concat（object[] args））
- `string Concat(string str0, string str1)`
  （string Concat（string str0, string str1））
- `string Concat(string str0, string str1, string str2)`
  （string Concat（string str0, string str1, string str2））
- `string Concat(string str0, string str1, string str2, string str3)`
  （string Concat（string str0, string str1, string str2, string str3））
- `string ConcatArray(string[] values, int totalLength)`
  （string Concat数组（string[] values, int totalLength））
- `string Concat(string[] values)`
  （string Concat（string[] values））
- `TypeCode GetTypeCode()`
  （类型代码 获取类型代码（））
- `int get_Length()`
  （整数 获取_长度（））
- `int CompareOrdinalUnchecked(string strA, int indexA, int lenA, string strB, int indexB, int lenB)`
  （int CompareOrdinalUnchecked（string strA, int indexA, int lenA, string strB, int indexB, int lenB））
- `int IndexOf(char value, int startIndex, int count)`
  （int 索引Of（char value, int startIndex, int count））
- `int IndexOfUnchecked(char value, int startIndex, int count)`
  （int 索引OfUnchecked（char value, int startIndex, int count））
- `int IndexOfUnchecked(string value, int startIndex, int count)`
  （int 索引OfUnchecked（string value, int startIndex, int count））
- `int IndexOfAny(char[] anyOf, int startIndex, int count)`
  （int 索引Of任意（char[] anyOf, int startIndex, int count））
- `int IndexOfAnyUnchecked(char[] anyOf, int startIndex, int count)`
  （int 索引Of任意Unchecked（char[] anyOf, int startIndex, int count））
- `int LastIndexOf(char value, int startIndex, int count)`
  （int 最后一个索引Of（char value, int startIndex, int count））
- `int LastIndexOfUnchecked(char value, int startIndex, int count)`
  （int 最后一个索引OfUnchecked（char value, int startIndex, int count））
- `int LastIndexOfAny(char[] anyOf, int startIndex, int count)`
  （int 最后一个索引Of任意（char[] anyOf, int startIndex, int count））
- `int LastIndexOfAnyUnchecked(char[] anyOf, int startIndex, int count)`
  （int 最后一个索引Of任意Unchecked（char[] anyOf, int startIndex, int count））
- `int nativeCompareOrdinalEx(string strA, int indexA, string strB, int indexB, int count)`
  （int nativeCompareOrdinalEx（string strA, int indexA, string strB, int indexB, int count））
- `string ReplaceInternal(char oldChar, char newChar)`
  （string Replace内部的（char oldChar, char newChar））
- `string ReplaceInternal(string oldValue, string newValue)`
  （string Replace内部的（string oldValue, string newValue））
- `string ReplaceUnchecked(string oldValue, string newValue)`
  （string ReplaceUnchecked（string oldValue, string newValue））
- `string ReplaceFallback(string oldValue, string newValue, int testedCount)`
  （string ReplaceFallback（string oldValue, string newValue, int testedCount））
- `string PadHelper(int totalWidth, char paddingChar, bool isRightPadded)`
  （string Pad辅助器（int totalWidth, char paddingChar, bool isRightPadded））
- `bool StartsWithOrdinalUnchecked(string value)`
  （bool StartsWithOrdinalUnchecked（string value））
- `bool IsAscii()`
  （bool 是否Ascii（））
- `void CharCopy(char* dest, char* src, int count)`
  （void Char复制（char* dest, char* src, int count））
- `void memset(byte* dest, int val, int len)`
  （void memset（byte* dest, int val, int len））
- `void memcpy(byte* dest, byte* src, int size)`
  （void memcpy（byte* dest, byte* src, int size））
- `void bzero(byte* dest, int len)`
  （void bzero（byte* dest, int len））
- `void bzero_aligned_1(byte* dest, int len)`
  （void bzero_aligned_1（byte* dest, int len））
- `void bzero_aligned_2(byte* dest, int len)`
  （void bzero_aligned_2（byte* dest, int len））
- `void bzero_aligned_4(byte* dest, int len)`
  （void bzero_aligned_4（byte* dest, int len））
- `void bzero_aligned_8(byte* dest, int len)`
  （void bzero_aligned_8（byte* dest, int len））
- `void memcpy_aligned_1(byte* dest, byte* src, int size)`
  （void memcpy_aligned_1（byte* dest, byte* src, int size））
- `void memcpy_aligned_2(byte* dest, byte* src, int size)`
  （void memcpy_aligned_2（byte* dest, byte* src, int size））
- `void memcpy_aligned_4(byte* dest, byte* src, int size)`
  （void memcpy_aligned_4（byte* dest, byte* src, int size））
- `void memcpy_aligned_8(byte* dest, byte* src, int size)`
  （void memcpy_aligned_8（byte* dest, byte* src, int size））
- `string CreateString(sbyte* value)`
  （string 创建字符串（sbyte* value））
- `string CreateString(sbyte* value, int startIndex, int length)`
  （string 创建字符串（sbyte* value, int startIndex, int length））
- `string CreateString(char* value)`
  （string 创建字符串（char* value））
- `string CreateString(char* value, int startIndex, int length)`
  （string 创建字符串（char* value, int startIndex, int length））
- `string CreateString(char[] val, int startIndex, int length)`
  （string 创建字符串（char[] val, int startIndex, int length））
- `string CreateString(char[] val)`
  （string 创建字符串（char[] val））
- `string CreateString(char c, int count)`
  （string 创建字符串（char c, int count））
- `string CreateString(sbyte* value, int startIndex, int length, Encoding enc)`
  （string 创建字符串（sbyte* value, int startIndex, int length, Encoding enc））

---

## StringBuilder（字符串构建器）

**继承**: ISerializable（可序列化接口）

### 字段 (5)

- `char[] m_ChunkChars`（char[] m_ChunkChars）(偏移: 0x8)
- `StringBuilder m_ChunkPrevious`（字符串构建器 m_Chunk上一个）(偏移: 0xC)
- `int m_ChunkLength`（int m_ChunkLength）(偏移: 0x10)
- `int m_ChunkOffset`（int m_ChunkOffset）(偏移: 0x14)
- `int m_MaxCapacity`（int m_最大Capacity）(偏移: 0x18)

### 方法 (51)

- `int get_Capacity()`
  （int get_Capacity（））
- `int get_MaxCapacity()`
  （int get_最大Capacity（））
- `string ToString()`
  （字符串 转字符串（））
- `string ToString(int startIndex, int length)`
  （string To字符串（int startIndex, int length））
- `StringBuilder Clear()`
  （字符串构建器 清除（））
- `int get_Length()`
  （整数 获取_长度（））
- `void set_Length(int value)`
  （void set_Length（int value））
- `char get_Chars(int index)`
  （char get_Chars（int index））
- `void set_Chars(int index, char value)`
  （void set_Chars（int index, char value））
- `StringBuilder Append(char value, int repeatCount)`
  （字符串构建器 Append（char value, int repeatCount））
- `StringBuilder Append(char[] value, int startIndex, int charCount)`
  （字符串构建器 Append（char[] value, int startIndex, int charCount））
- `StringBuilder Append(string value)`
  （字符串构建器 Append（string value））
- `void AppendHelper(string value)`
  （void Append辅助器（string value））
- `StringBuilder Append(string value, int startIndex, int count)`
  （字符串构建器 Append（string value, int startIndex, int count））
- `StringBuilder AppendLine()`
  （字符串构建器 AppendLine（））
- `StringBuilder AppendLine(string value)`
  （字符串构建器 AppendLine（string value））
- `StringBuilder Insert(int index, string value, int count)`
  （字符串构建器 Insert（int index, string value, int count））
- `StringBuilder Remove(int startIndex, int length)`
  （字符串构建器 移除（int startIndex, int length））
- `StringBuilder Append(bool value)`
  （字符串构建器 Append（bool value））
- `StringBuilder Append(byte value)`
  （字符串构建器 Append（byte value））
- `StringBuilder Append(char value)`
  （字符串构建器 Append（char value））
- `StringBuilder Append(int value)`
  （字符串构建器 Append（int value））
- `StringBuilder Append(long value)`
  （字符串构建器 Append（long value））
- `StringBuilder Append(double value)`
  （字符串构建器 Append（double value））
- `StringBuilder Append(ushort value)`
  （字符串构建器 Append（ushort value））
- `StringBuilder Append(uint value)`
  （字符串构建器 Append（uint value））
- `StringBuilder Append(object value)`
  （字符串构建器 Append（object value））
- `StringBuilder Insert(int index, string value)`
  （字符串构建器 Insert（int index, string value））
- `StringBuilder Insert(int index, char value)`
  （字符串构建器 Insert（int index, char value））
- `StringBuilder AppendFormat(string format, object arg0)`
  （字符串构建器 Append格式化（string format, object arg0））
- `StringBuilder AppendFormat(string format, object arg0, object arg1)`
  （字符串构建器 Append格式化（string format, object arg0, object arg1））
- `StringBuilder AppendFormat(string format, object arg0, object arg1, object arg2)`
  （字符串构建器 Append格式化（string format, object arg0, object arg1, object arg2））
- `StringBuilder AppendFormat(string format, object[] args)`
  （字符串构建器 Append格式化（string format, object[] args））
- `StringBuilder AppendFormat(IFormatProvider provider, string format, object arg0)`
  （字符串构建器 Append格式化（I格式化提供者 provider, string format, object arg0））
- `StringBuilder AppendFormat(IFormatProvider provider, string format, object arg0, object arg1)`
  （字符串构建器 Append格式化（I格式化提供者 provider, string format, object arg0, object arg1））
- `void FormatError()`
  （void 格式化Error（））
- `StringBuilder AppendFormatHelper(IFormatProvider provider, string format, ParamsArray args)`
  （字符串构建器 Append格式化辅助器（I格式化提供者 provider, string format, Params数组 args））
- `StringBuilder Replace(string oldValue, string newValue)`
  （字符串构建器 Replace（string oldValue, string newValue））
- `StringBuilder Replace(string oldValue, string newValue, int startIndex, int count)`
  （字符串构建器 Replace（string oldValue, string newValue, int startIndex, int count））
- `StringBuilder Append(char* value, int valueCount)`
  （字符串构建器 Append（char* value, int valueCount））
- `void Insert(int index, char* value, int valueCount)`
  （void Insert（int index, char* value, int valueCount））
- `void ReplaceAllInChunk(int[] replacements, int replacementsCount, StringBuilder sourceChunk, int removeCount, string value)`
  （void Replace所有InChunk（int[] replacements, int replacementsCount, 字符串构建器 sourceChunk, int removeCount, string value））
- `bool StartsWith(StringBuilder chunk, int indexInChunk, int count, string value)`
  （bool StartsWith（字符串构建器 chunk, int indexInChunk, int count, string value））
- `void ReplaceInPlaceAtChunk(ref StringBuilder chunk, ref int indexInChunk, char* value, int count)`
  （void ReplaceInPlaceAtChunk（ref StringBuilder chunk, ref int indexInChunk, char* value, int count））
- `void ThreadSafeCopy(char* sourcePtr, char[] destination, int destinationIndex, int count)`
  （void ThreadSafe复制（char* sourcePtr, char[] destination, int destinationIndex, int count））
- `void ThreadSafeCopy(char[] source, int sourceIndex, char[] destination, int destinationIndex, int count)`
  （void ThreadSafe复制（char[] source, int sourceIndex, char[] destination, int destinationIndex, int count））
- `StringBuilder FindChunkForIndex(int index)`
  （字符串构建器 查找ChunkFor索引（int index））
- `StringBuilder Next(StringBuilder chunk)`
  （字符串构建器 下一个（字符串构建器 chunk））
- `void ExpandByABlock(int minBlockCharCount)`
  （void ExpandByABlock（int minBlockCharCount））
- `void MakeRoom(int index, int count, out StringBuilder chunk, out int indexInChunk, bool doneMoveFollowingChars)`
  （void Make房间（int index, int count, out StringBuilder chunk, out int indexInChunk, bool doneMoveFollowingChars））
- `void Remove(int startIndex, int count, out StringBuilder chunk, out int indexInChunk)`
  （void 移除（int startIndex, int count, out StringBuilder chunk, out int indexInChunk））

---

## StringBuilderCache（字符串构建器缓存）

### 字段 (1)

- `StringBuilder CachedInstance`（字符串构建器 Cached实例）(偏移: 0x80000000)

### 方法 (3)

- `StringBuilder Acquire(int capacity = 16)`
  （字符串构建器 Acquire（int capacity = 16））
- `void Release(StringBuilder sb)`
  （void Release（字符串构建器 sb））
- `string GetStringAndRelease(StringBuilder sb)`
  （string 获取字符串AndRelease（字符串构建器 sb））

---

## StringComparer（字符串Comparer）

**继承**: IComparer, IEqualityComparer, IComparer<string>, IEqualityComparer<string>（IComparer, IEqualityComparer, IComparer<string>, IEqualityComparer<string>）

### 字段 (4)

- `StringComparer _invariantCulture`（字符串Comparer _invariantCulture）(偏移: 0x0)
- `StringComparer _invariantCultureIgnoreCase`（字符串Comparer _invariantCultureIgnoreCase）(偏移: 0x4)
- `StringComparer _ordinal`（字符串Comparer _ordinal）(偏移: 0x8)
- `StringComparer _ordinalIgnoreCase`（字符串Comparer _ordinalIgnoreCase）(偏移: 0xC)

### 方法 (7)

- `StringComparer get_InvariantCultureIgnoreCase()`
  （字符串Comparer get_InvariantCultureIgnoreCase（））
- `StringComparer get_CurrentCultureIgnoreCase()`
  （字符串Comparer get_当前CultureIgnoreCase（））
- `StringComparer get_Ordinal()`
  （字符串Comparer get_Ordinal（））
- `StringComparer get_OrdinalIgnoreCase()`
  （字符串Comparer get_OrdinalIgnoreCase（））
- `int Compare(object x, object y)`
  （int Compare（object x, object y））
- `bool Equals(object x, object y)`
  （bool Equals（object x, object y））
- `int GetHashCode(object obj)`
  （整数 获取哈希码（对象 obj））

---

## StringComparison（字符串Comparison）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## StringConverter（字符串Converter）

**继承**: TypeConverter（类型转换器）

### 方法 (2)

- `bool CanConvertFrom(ITypeDescriptorContext context, Type sourceType)`
  （布尔值 能否转换自（I类型描述符上下文 context, 类型 sourceType））
- `object ConvertFrom(ITypeDescriptorContext context, CultureInfo culture, object value)`
  （对象 转换自（I类型描述符上下文 context, 区域性信息 culture, 对象 value））

---

## StringExpand（字符串Expand）

### 方法 (2)

- `string GetRandomClip(string[] array)`
  （string 获取随机弹匣（string[] array））
- `string ApplyChangeLine(string str)`
  （string 应用ChangeLine（string str））

---

## StringOptions（字符串Options）

**继承**: IPlugOptions（I插件选项）

### 字段 (5)

- `bool richTextEnabled`（bool rich文本启用的）(偏移: 0x0)
- `ScrambleMode scrambleMode`（Scramble模式 scramble模式）(偏移: 0x4)
- `char[] scrambledChars`（char[] scrambledChars）(偏移: 0x8)
- `int startValueStrippedLength`（int start值StrippedLength）(偏移: 0xC)
- `int changeValueStrippedLength`（int change值StrippedLength）(偏移: 0x10)

### 方法 (1)

- `void Reset()`
  （void 重置（））

---

## StringPlugin（字符串插件）

**继承**: ABSTweenPlugin<string, string, StringOptions>（ABSTweenPlugin<string, string, 字符串Options>）

### 字段 (2)

- `StringBuilder _Buffer`（字符串构建器 _缓冲区）(偏移: 0x0)
- `List<char> _OpenedTags`（List<char> _OpenedTags）(偏移: 0x4)

### 方法 (10)

- `void SetFrom(TweenerCore<string, string, StringOptions> t, bool isRelative)`
  （void 集合From（TweenerCore<string, string, 字符串Options> t, bool isRelative））
- `void SetFrom(TweenerCore<string, string, StringOptions> t, string fromValue, bool setImmediately, bool isRelative)`
  （void 集合From（TweenerCore<string, string, 字符串Options> t, string fromValue, bool setImmediately, bool isRelative））
- `void Reset(TweenerCore<string, string, StringOptions> t)`
  （void 重置（TweenerCore<string, string, 字符串Options> t））
- `string ConvertToStartValue(TweenerCore<string, string, StringOptions> t, string value)`
  （string 转换To开始值（TweenerCore<string, string, 字符串Options> t, string value））
- `void SetRelativeEndValue(TweenerCore<string, string, StringOptions> t)`
  （void 集合Relative结束值（TweenerCore<string, string, 字符串Options> t））
- `void SetChangeValue(TweenerCore<string, string, StringOptions> t)`
  （void 集合Change值（TweenerCore<string, string, 字符串Options> t））
- `float GetSpeedBasedDuration(StringOptions options, float unitsXSecond, string changeValue)`
  （float 获取SpeedBased持续时间（字符串Options options, float unitsXSecond, string changeValue））
- `void EvaluateAndApply(StringOptions options, Tween t, bool isRelative, DOGetter<string> getter, DOSetter<string> setter, float elapsed, string startValue, string changeValue, float duration, bool usingInversePosition, UpdateNotice updateNotice)`
  （void EvaluateAnd应用（字符串Options options, Tween t, bool isRelative, DOGetter<string> getter, DOSetter<string> setter, float elapsed, string startValue, string changeValue, float duration, bool usingInversePosition, 更新Notice updateNotice））
- `StringBuilder Append(string value, int startIndex, int length, bool richTextEnabled)`
  （字符串构建器 Append（string value, int startIndex, int length, bool richTextEnabled））
- `char[] ScrambledCharsToUse(StringOptions options)`
  （char[] ScrambledCharsToUse（字符串Options options））

---

## StringPluginExtensions（字符串插件Extensions）

### 字段 (5)

- `char[] ScrambledCharsAll`（char[] ScrambledChars所有）(偏移: 0x0)
- `char[] ScrambledCharsUppercase`（char[] ScrambledCharsUppercase）(偏移: 0x4)
- `char[] ScrambledCharsLowercase`（char[] ScrambledCharsLowercase）(偏移: 0x8)
- `char[] ScrambledCharsNumerals`（char[] ScrambledCharsNumerals）(偏移: 0xC)
- `int _lastRndSeed`（int _lastRndSeed）(偏移: 0x10)

### 方法 (2)

- `void ScrambleChars(char[] chars)`
  （void ScrambleChars（char[] chars））
- `StringBuilder AppendScrambledChars(StringBuilder buffer, int length, char[] chars)`
  （字符串构建器 AppendScrambledChars（字符串构建器 buffer, int length, char[] chars））

---

## StringReader（字符串读取器）

**继承**: TextReader（文本读取器）

### 字段 (3)

- `string _s`（string _s）(偏移: 0xC)
- `int _pos`（int _pos）(偏移: 0x10)
- `int _length`（int _length）(偏移: 0x14)

### 方法 (7)

- `void Close()`
  （void 关闭（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `int Peek()`
  （整数 查看（））
- `int Read()`
  （整数 读取（））
- `int Read([In] [Out] char[] buffer, int index, int count)`
  （int Read（[In] [Out] char[] buffer, int index, int count））
- `string ReadToEnd()`
  （字符串 读取到结束（））
- `string ReadLine()`
  （字符串 读取行（））

---

## StringResultHandler（字符串Result处理器）

**继承**: SearchResultHandler<string>（搜索ResultHandler<string>）

### 字段 (2)

- `bool _includeFiles`（bool _includeFiles）(偏移: 0x8)
- `bool _includeDirs`（bool _includeDirs）(偏移: 0x9)

### 方法 (2)

- `bool IsResultIncluded(SearchResult result)`
  （bool 是否ResultIncluded（搜索Result result））
- `string CreateObject(SearchResult result)`
  （string 创建对象（搜索Result result））

---

## StringSplitOptions（字符串SplitOptions）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## StringTypeInfo（字符串类型信息）

**继承**: TraceLoggingTypeInfo<string>（TraceLogging类型Info<string>）

### 方法 (3)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void 写入元数据（跟踪日志元数据收集器 collector, 字符串 name, 事件字段格式 format））
- `void WriteData(TraceLoggingDataCollector collector, ref string value)`
  （void Write数据（TraceLogging数据Collector collector, ref string value））
- `object GetData(object value)`
  （object 获取数据（object value））

---

## StringWriter（字符串写入器）

**继承**: TextWriter（文本写入器）

### 字段 (2)

- `StringBuilder _sb`（字符串构建器 _sb）(偏移: 0x14)
- `bool _isOpen`（bool _is打开）(偏移: 0x18)

### 方法 (7)

- `void Close()`
  （void 关闭（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `StringBuilder GetStringBuilder()`
  （字符串构建器 获取字符串构建器（））
- `void Write(char value)`
  （void 写入（字符 value））
- `void Write(char[] buffer, int index, int count)`
  （void 写入（字符[] buffer, 整数 index, 整数 count））
- `void Write(string value)`
  （void 写入（字符串 value））
- `string ToString()`
  （字符串 转字符串（））

---

## StrongNameKeyPair（Strong名称键Pair）

**继承**: ISerializable, IDeserializationCallback（ISerializable, IDeserialization回调）

### 字段 (4)

- `byte[] _publicKey`（byte[] _public键）(偏移: 0x8)
- `string _keyPairContainer`（string _keyPair容器）(偏移: 0xC)
- `bool _keyPairExported`（bool _keyPairExported）(偏移: 0x10)
- `byte[] _keyPairArray`（byte[] _keyPair数组）(偏移: 0x14)

---

## StunGrenadeArea（眩晕手雷Area）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (1)

- `AudioClip hitSnd`（音频弹匣 hitSnd）(偏移: 0xC)

### 方法 (2)

- `void Awake()`
  （void 唤醒（））
- `void OnTriggerStay(Collider other)`
  （void 触发器停留时（碰撞器 other））

---

## StunGrenadeBuff（眩晕手雷增益）

**继承**: SpeedBuff（Speed增益）

### 字段 (1)

- `string BuffName`（string 增益名称）(偏移: 0x333A331B)

### 方法 (2)

- `void BuffUpdater(ref bool value)`
  （void 增益更新器（ref bool value））
- `void OnLifeEnd()`
  （void 生命结束时（））

---

## StunGrenadeSFX（眩晕手雷SFX）

**继承**: RecyclableObject（可回收对象）

### 字段 (1)

- `RawImage img`（Raw图像 img）(偏移: 0x30)

### 方法 (1)

- `void Work()`
  （void 工作（））

---

## SubMeshDescriptor（子网格Descriptor）

### 方法 (8)

- `Bounds get_bounds()`
  （边界 获取_边界（））
- `MeshTopology get_topology()`
  （网格Topology get_topology（））
- `int get_indexStart()`
  （int get_index开始（））
- `int get_indexCount()`
  （int get_index数量（））
- `int get_baseVertex()`
  （int get_baseVertex（））
- `int get_firstVertex()`
  （int get_firstVertex（））
- `int get_vertexCount()`
  （int get_vertex数量（））
- `string ToString()`
  （字符串 转字符串（））

---

## SubsystemDescriptor（SubsystemDescriptor）

**继承**: ISubsystemDescriptor（ISubsystemDescriptor）

### 方法 (1)

- `string get_id()`
  （string get_id（））

---

## SubsystemDescriptorBindings（SubsystemDescriptorBindings）

### 方法 (1)

- `string GetId(IntPtr descriptorPtr)`
  （string 获取Id（整数Ptr descriptorPtr））

---

## SubsystemDescriptorStore（SubsystemDescriptor商店）

### 字段 (3)

- `List<IntegratedSubsystemDescriptor> s_IntegratedDescriptors`（List<IntegratedSubsystemDescriptor> s_IntegratedDescriptors）(偏移: 0x0)
- `List<SubsystemDescriptorWithProvider> s_StandaloneDescriptors`（List<SubsystemDescriptorWithProvider> s_StandaloneDescriptors）(偏移: 0x4)
- `List<SubsystemDescriptor> s_DeprecatedDescriptors`（List<SubsystemDescriptor> s_DeprecatedDescriptors）(偏移: 0x8)

### 方法 (4)

- `void InitializeManagedDescriptor(IntPtr ptr, IntegratedSubsystemDescriptor desc)`
  （void 初始化ManagedDescriptor（整数Ptr ptr, IntegratedSubsystemDescriptor desc））
- `void ClearManagedDescriptors()`
  （void 清除ManagedDescriptors（））
- `void ReportSingleSubsystemAnalytics(string id)`
  （void Report单个SubsystemAnalytics（string id））
- `void RegisterDeprecatedDescriptor(SubsystemDescriptor descriptor)`
  （void RegisterDeprecatedDescriptor（SubsystemDescriptor descriptor））

---

## SubsystemDescriptorWithProvider（SubsystemDescriptorWith提供者）

**继承**: ISubsystemDescriptor（ISubsystemDescriptor）

### 方法 (1)

- `string get_id()`
  （string get_id（））

---

## SubsystemManager（Subsystem管理器）

### 字段 (7)

- `Action beforeReloadSubsystems`（动作 before换弹Subsystems）(偏移: 0x0)
- `Action afterReloadSubsystems`（动作 after换弹Subsystems）(偏移: 0x4)
- `List<IntegratedSubsystem> s_IntegratedSubsystems`（List<IntegratedSubsystem> s_IntegratedSubsystems）(偏移: 0x8)
- `List<SubsystemWithProvider> s_StandaloneSubsystems`（List<SubsystemWithProvider> s_StandaloneSubsystems）(偏移: 0xC)
- `List<Subsystem> s_DeprecatedSubsystems`（List<Subsystem> s_DeprecatedSubsystems）(偏移: 0x10)
- `Action reloadSubsytemsStarted`（动作 reloadSubsytemsStarted）(偏移: 0x14)
- `Action reloadSubsytemsCompleted`（动作 reloadSubsytemsCompleted）(偏移: 0x18)

### 方法 (6)

- `void ReloadSubsystemsStarted()`
  （void 换弹SubsystemsStarted（））
- `void ReloadSubsystemsCompleted()`
  （void 换弹SubsystemsCompleted（））
- `void InitializeIntegratedSubsystem(IntPtr ptr, IntegratedSubsystem subsystem)`
  （void 初始化IntegratedSubsystem（整数Ptr ptr, IntegratedSubsystem subsystem））
- `void ClearSubsystems()`
  （void 清除Subsystems（））
- `void StaticConstructScriptingClassMap()`
  （void 静态的ConstructScripting类映射（））
- `IntegratedSubsystem GetIntegratedSubsystemByPtr(IntPtr ptr)`
  （IntegratedSubsystem 获取IntegratedSubsystemByPtr（整数Ptr ptr））

---

## SuperJumpArea（Super跳跃Area）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (1)

- `float speed`（浮点数 速度）(偏移: 0xC)

### 方法 (1)

- `void OnTriggerEnter(Collider other)`
  （void 触发器进入时（碰撞器 other））

---

## SupplyBox（SupplyBox）

**继承**: RecyclableObject（可回收对象）

### 字段 (5)

- `SupplyBox.Type type`（SupplyBox.类型 type）(偏移: 0x30)
- `int occupiedPosID`（int occupiedPosID）(偏移: 0x34)
- `List<SupplyBox> BoxList_Yellow`（List<SupplyBox> BoxList_Yellow）(偏移: 0x0)
- `List<SupplyBox> BoxList_Red`（List<SupplyBox> BoxList_红色）(偏移: 0x4)
- `List<SupplyBox> BoxList_Blue`（List<SupplyBox> BoxList_蓝色）(偏移: 0x8)

### 方法 (11)

- `void OnTriggerStay(Collider other)`
  （void 触发器停留时（碰撞器 other））
- `bool CanPickUp(Player player)`
  （bool 能否Pick上（玩家 player））
- `bool CanPickUpRedBox(Player player)`
  （bool 能否Pick上红色Box（玩家 player））
- `void SetPos(int index, SpawnPoint point)`
  （void 集合Pos（int index, 出生Point point））
- `void Recycle(bool roundRecycle)`
  （void 回收（布尔值 循环回收））
- `void Work()`
  （void 工作（））
- `List<SupplyBox> GetBoxList(SupplyBox.Type boxType)`
  （List<SupplyBox> 获取Box列表（SupplyBox.类型 boxType））
- `SupplyBox GetRandomBox(SupplyBox.Type boxType)`
  （SupplyBox 获取随机Box（SupplyBox.类型 boxType））
- `SupplyBox GetNearestBox(SupplyBox.Type boxType, Vector3 pos)`
  （SupplyBox 获取NearestBox（SupplyBox.类型 boxType, 三维向量 pos））
- `void ClearBoxList()`
  （void 清除Box列表（））
- `SupplyBox.Type GetBoxType()`
  （SupplyBox.类型 获取Box类型（））

---

## SupplyBox.Type（SupplyBox.类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## SupportedRenderingFeatures（SupportedRenderingFeatures）

### 字段 (1)

- `SupportedRenderingFeatures s_Active`（SupportedRenderingFeatures s_激活的）(偏移: 0x0)

### 方法 (21)

- `SupportedRenderingFeatures get_active()`
  （SupportedRenderingFeatures get_active（））
- `void set_active(SupportedRenderingFeatures value)`
  （void set_active（SupportedRenderingFeatures value））
- `SupportedRenderingFeatures.LightmapMixedBakeModes get_defaultMixedLightingModes()`
  （SupportedRenderingFeatures.LightmapMixedBakeModes get_defaultMixedLightingModes（））
- `SupportedRenderingFeatures.LightmapMixedBakeModes get_mixedLightingModes()`
  （SupportedRenderingFeatures.LightmapMixedBakeModes get_mixedLightingModes（））
- `LightmapBakeType get_lightmapBakeTypes()`
  （LightmapBake类型 get_lightmapBakeTypes（））
- `LightmapsMode get_lightmapsModes()`
  （Lightmaps模式 get_lightmapsModes（））
- `bool get_enlighten()`
  （bool get_enlighten（））
- `bool get_rendersUIOverlay()`
  （bool get_renders界面Overlay（））
- `bool get_autoAmbientProbeBaking()`
  （bool get_autoAmbientProbeBaking（））
- `bool get_autoDefaultReflectionProbeBaking()`
  （bool get_auto默认的ReflectionProbeBaking（））
- `void FallbackMixedLightingModeByRef(IntPtr fallbackModePtr)`
  （void FallbackMixedLighting模式ByRef（整数Ptr fallbackModePtr））
- `bool IsMixedLightingModeSupported(MixedLightingMode mixedMode)`
  （bool 是否MixedLighting模式Supported（MixedLighting模式 mixedMode））
- `void IsMixedLightingModeSupportedByRef(MixedLightingMode mixedMode, IntPtr isSupportedPtr)`
  （void 是否MixedLighting模式SupportedByRef（MixedLighting模式 mixedMode, 整数Ptr isSupportedPtr））
- `bool IsLightmapBakeTypeSupported(LightmapBakeType bakeType)`
  （bool 是否LightmapBake类型Supported（LightmapBake类型 bakeType））
- `void IsLightmapBakeTypeSupportedByRef(LightmapBakeType bakeType, IntPtr isSupportedPtr)`
  （void 是否LightmapBake类型SupportedByRef（LightmapBake类型 bakeType, 整数Ptr isSupportedPtr））
- `void IsLightmapsModeSupportedByRef(LightmapsMode mode, IntPtr isSupportedPtr)`
  （void 是否Lightmaps模式SupportedByRef（Lightmaps模式 mode, 整数Ptr isSupportedPtr））
- `void IsLightmapperSupportedByRef(int lightmapper, IntPtr isSupportedPtr)`
  （void 是否LightmapperSupportedByRef（int lightmapper, 整数Ptr isSupportedPtr））
- `void IsUIOverlayRenderedBySRP(IntPtr isSupportedPtr)`
  （void 是否界面OverlayRenderedBySRP（整数Ptr isSupportedPtr））
- `void IsAutoAmbientProbeBakingSupported(IntPtr isSupportedPtr)`
  （void 是否自动AmbientProbeBakingSupported（整数Ptr isSupportedPtr））
- `void IsAutoDefaultReflectionProbeBakingSupported(IntPtr isSupportedPtr)`
  （void 是否自动默认的ReflectionProbeBakingSupported（整数Ptr isSupportedPtr））
- `void FallbackLightmapperByRef(IntPtr lightmapperPtr)`
  （void FallbackLightmapperByRef（整数Ptr lightmapperPtr））

---

## SupportedRenderingFeatures.LightmapMixedBakeModes（SupportedRenderingFeatures.LightmapMixedBakeModes）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## SupportedRenderingFeatures.ReflectionProbeModes（SupportedRenderingFeatures.ReflectionProbeModes）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## SupportsChildTracksAttribute（Supports子级TracksAttribute）

**继承**: Attribute（属性）

### 字段 (2)

- `Type childType`（类型 child类型）(偏移: 0x8)
- `int levels`（int levels）(偏移: 0xC)

---

## SurfaceDataAttributes（Surface数据Attributes）

**继承**: Attribute（属性）

### 字段 (6)

- `string[] displayNames`（string[] displayNames）(偏移: 0x8)
- `bool isDirection`（bool is方向）(偏移: 0xC)
- `bool sRGBDisplay`（bool sRGB颜色Display）(偏移: 0xD)
- `FieldPrecision precision`（FieldPrecision precision）(偏移: 0x10)
- `bool checkIsNormalized`（bool check是否Normalized）(偏移: 0x14)
- `string preprocessor`（string preprocessor）(偏移: 0x18)

---

## Switch（Switch）

### 字段 (6)

- `string description`（string description）(偏移: 0x8)
- `string displayName`（字符串 显示名称）(偏移: 0xC)
- `string switchValueString`（string switch值字符串）(偏移: 0x10)
- `string defaultValue`（string default值）(偏移: 0x14)
- `List<WeakReference> switches`（List<WeakReference> switches）(偏移: 0x0)
- `int s_LastCollectionCount`（int s_最后一个Collection数量）(偏移: 0x4)

### 方法 (1)

- `void _pruneCachedSwitches()`
  （void _pruneCachedSwitches（））

---

## Switch（Switch）

**继承**: ChoiceBase（选择基类）

### 字段 (2)

- `bool value`（bool value）(偏移: 0x14)
- `Action<bool> action`（Action<bool> action）(偏移: 0x18)

### 方法 (2)

- `string GetText()`
  （string 获取文本（））
- `bool OnSelect()`
  （bool On选择（））

---

## SwitchLevelAttribute（Switch等级Attribute）

**继承**: Attribute（属性）

### 字段 (1)

- `Type type`（类型 type）(偏移: 0x8)

### 方法 (1)

- `void set_SwitchLevelType(Type value)`
  （void set_Switch等级类型（类型 value））

---

## SymmetricAlgorithm（对称算法）

**继承**: IDisposable（可释放接口）

### 字段 (9)

- `int BlockSizeValue`（int Block大小值）(偏移: 0x8)
- `int FeedbackSizeValue`（int Feedback大小值）(偏移: 0xC)
- `byte[] IVValue`（byte[] IV值）(偏移: 0x10)
- `byte[] KeyValue`（byte[] 键值）(偏移: 0x14)
- `KeySizes[] LegalBlockSizesValue`（键Sizes[] LegalBlockSizes值）(偏移: 0x18)
- `KeySizes[] LegalKeySizesValue`（键Sizes[] Legal键Sizes值）(偏移: 0x1C)
- `int KeySizeValue`（int 键大小值）(偏移: 0x20)
- `CipherMode ModeValue`（Cipher模式 模式值）(偏移: 0x24)
- `PaddingMode PaddingValue`（Padding模式 Padding值）(偏移: 0x28)

### 方法 (18)

- `void Dispose()`
  （void 释放（））
- `void Clear()`
  （void 清除（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `int get_BlockSize()`
  （int get_Block大小（））
- `void set_BlockSize(int value)`
  （void set_Block大小（int value））
- `int get_FeedbackSize()`
  （int get_Feedback大小（））
- `byte[] get_IV()`
  （byte[] get_IV（））
- `void set_IV(byte[] value)`
  （void set_IV（byte[] value））
- `byte[] get_Key()`
  （字节[] 获取_键（））
- `void set_Key(byte[] value)`
  （void 设置_键（字节[] value））
- `KeySizes[] get_LegalKeySizes()`
  （键Sizes[] get_Legal键Sizes（））
- `int get_KeySize()`
  （整数 获取_键大小（））
- `void set_KeySize(int value)`
  （void 设置_键大小（整数 value））
- `CipherMode get_Mode()`
  （Cipher模式 get_模式（））
- `PaddingMode get_Padding()`
  （Padding模式 get_Padding（））
- `void set_Padding(PaddingMode value)`
  （void set_Padding（Padding模式 value））
- `bool ValidKeySize(int bitLength)`
  （bool Valid键大小（int bitLength））
- `ICryptoTransform CreateEncryptor()`
  （ICrypto变换 创建Encryptor（））

---

## SymmetricTransform（对称变换）

**继承**: ICryptoTransform, IDisposable（ICrypto变换, IDisposable）

### 字段 (12)

- `SymmetricAlgorithm algo`（SymmetricAlgorithm algo）(偏移: 0x8)
- `bool encrypt`（bool encrypt）(偏移: 0xC)
- `int BlockSizeByte`（int Block大小Byte）(偏移: 0x10)
- `byte[] temp`（byte[] temp）(偏移: 0x14)
- `byte[] temp2`（byte[] temp2）(偏移: 0x18)
- `byte[] workBuff`（byte[] work增益）(偏移: 0x1C)
- `byte[] workout`（byte[] workout）(偏移: 0x20)
- `PaddingMode padmode`（Padding模式 padmode）(偏移: 0x24)
- `int FeedBackByte`（int Feed后Byte）(偏移: 0x28)
- `bool m_disposed`（布尔值 m_已释放）(偏移: 0x2C)
- `bool lastBlock`（bool lastBlock）(偏移: 0x2D)
- `RandomNumberGenerator _rng`（随机NumberGenerator _rng）(偏移: 0x30)

### 方法 (19)

- `void Finalize()`
  （void 终结（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `bool get_CanTransformMultipleBlocks()`
  （bool get_能否变换MultipleBlocks（））
- `int get_InputBlockSize()`
  （int get_输入Block大小（））
- `int get_OutputBlockSize()`
  （int get_OutputBlock大小（））
- `void Transform(byte[] input, byte[] output)`
  （void 变换（byte[] input, byte[] output））
- `void CBC(byte[] input, byte[] output)`
  （void CBC（byte[] input, byte[] output））
- `void CFB(byte[] input, byte[] output)`
  （void CFB（byte[] input, byte[] output））
- `void OFB(byte[] input, byte[] output)`
  （void OFB（byte[] input, byte[] output））
- `void CTS(byte[] input, byte[] output)`
  （void CTS（byte[] input, byte[] output））
- `void CheckInput(byte[] inputBuffer, int inputOffset, int inputCount)`
  （void 检查输入（byte[] inputBuffer, int inputOffset, int inputCount））
- `int TransformBlock(byte[] inputBuffer, int inputOffset, int inputCount, byte[] outputBuffer, int outputOffset)`
  （int 变换Block（byte[] inputBuffer, int inputOffset, int inputCount, byte[] outputBuffer, int outputOffset））
- `bool get_KeepLastBlock()`
  （bool get_Keep最后一个Block（））
- `int InternalTransformBlock(byte[] inputBuffer, int inputOffset, int inputCount, byte[] outputBuffer, int outputOffset)`
  （int 内部的变换Block（byte[] inputBuffer, int inputOffset, int inputCount, byte[] outputBuffer, int outputOffset））
- `void Random(byte[] buffer, int start, int length)`
  （void 随机（byte[] buffer, int start, int length））
- `void ThrowBadPaddingException(PaddingMode padding, int length, int position)`
  （void 投掷BadPaddingException（Padding模式 padding, int length, int position））
- `byte[] FinalEncrypt(byte[] inputBuffer, int inputOffset, int inputCount)`
  （byte[] FinalEncrypt（byte[] inputBuffer, int inputOffset, int inputCount））
- `byte[] FinalDecrypt(byte[] inputBuffer, int inputOffset, int inputCount)`
  （byte[] FinalDecrypt（byte[] inputBuffer, int inputOffset, int inputCount））
- `byte[] TransformFinalBlock(byte[] inputBuffer, int inputOffset, int inputCount)`
  （byte[] 变换FinalBlock（byte[] inputBuffer, int inputOffset, int inputCount））

---

## SynchronisationStage（SynchronisationStage）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## SynchronisationStageFlags（SynchronisationStageFlags）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## SynchronizationContext（SynchronizationContext）

### 字段 (6)

- `SynchronizationContextProperties _props`（SynchronizationContextProperties _props）(偏移: 0x8)
- `Type s_cachedPreparedType1`（类型 s_cachedPreparedType1）(偏移: 0x0)
- `Type s_cachedPreparedType2`（类型 s_cachedPreparedType2）(偏移: 0x4)
- `Type s_cachedPreparedType3`（类型 s_cachedPreparedType3）(偏移: 0x8)
- `Type s_cachedPreparedType4`（类型 s_cachedPreparedType4）(偏移: 0xC)
- `Type s_cachedPreparedType5`（类型 s_cachedPreparedType5）(偏移: 0x10)

### 方法 (7)

- `void Send(SendOrPostCallback d, object state)`
  （void 发送（发送OrPost回调 d, object state））
- `void Post(SendOrPostCallback d, object state)`
  （void Post（发送OrPost回调 d, object state））
- `void SetSynchronizationContext(SynchronizationContext syncContext)`
  （void 集合SynchronizationContext（SynchronizationContext syncContext））
- `SynchronizationContext get_Current()`
  （SynchronizationContext get_当前（））
- `SynchronizationContext get_CurrentNoFlow()`
  （SynchronizationContext get_当前NoFlow（））
- `SynchronizationContext GetThreadLocalContext()`
  （SynchronizationContext 获取Thread本地的Context（））
- `SynchronizationContext CreateCopy()`
  （SynchronizationContext 创建复制（））

---

## SynchronizationContextAwaitTaskContinuation（SynchronizationContextAwaitTaskContinuation）

**继承**: AwaitTaskContinuation（AwaitTaskContinuation）

### 字段 (3)

- `SendOrPostCallback s_postCallback`（发送OrPost回调 s_post回调）(偏移: 0x0)
- `ContextCallback s_postActionCallback`（Context回调 s_post动作回调）(偏移: 0x4)
- `SynchronizationContext m_syncContext`（SynchronizationContext m_syncContext）(偏移: 0x10)

### 方法 (2)

- `void PostAction(object state)`
  （void Post动作（object state））
- `ContextCallback GetPostActionCallback()`
  （Context回调 获取Post动作回调（））

---

## SynchronizationContextProperties（SynchronizationContextProperties）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## SystemInfo（系统信息）

### 方法 (52)

- `OperatingSystemFamily get_operatingSystemFamily()`
  （Operating系统Family get_operating系统Family（））
- `string get_processorType()`
  （string get_processor类型（））
- `int get_processorCount()`
  （int get_processor数量（））
- `int get_systemMemorySize()`
  （int get_systemMemory大小（））
- `string get_deviceUniqueIdentifier()`
  （string get_deviceUniqueIdentifier（））
- `DeviceType get_deviceType()`
  （Device类型 get_device类型（））
- `string get_graphicsDeviceVendor()`
  （string get_graphicsDeviceVendor（））
- `GraphicsDeviceType get_graphicsDeviceType()`
  （GraphicsDevice类型 get_graphicsDevice类型（））
- `bool get_graphicsUVStartsAtTop()`
  （bool get_graphicsUVStartsAt顶部（））
- `int get_graphicsShaderLevel()`
  （int get_graphics着色器等级（））
- `bool get_hasHiddenSurfaceRemovalOnGPU()`
  （bool get_has隐藏的SurfaceRemovalOnGPU（））
- `bool get_supportsShadows()`
  （bool get_supportsShadows（））
- `CopyTextureSupport get_copyTextureSupport()`
  （复制纹理Support get_copy纹理Support（））
- `bool get_supportsRenderTargetArrayIndexFromVertexShader()`
  （bool get_supportsRender目标数组索引FromVertex着色器（））
- `int get_supportedRenderTargetCount()`
  （int get_supportedRender目标数量（））
- `int get_supportsMultisampledTextures()`
  （int get_supportsMultisampledTextures（））
- `bool get_supportsMultisampleAutoResolve()`
  （bool get_supportsMultisample自动Resolve（））
- `bool get_usesReversedZBuffer()`
  （bool get_usesReversedZ缓冲区（））
- `bool IsValidEnumValue(Enum value)`
  （bool 是否ValidEnum值（Enum value））
- `bool SupportsRenderTextureFormat(RenderTextureFormat format)`
  （bool SupportsRender纹理格式化（Render纹理格式化 format））
- `bool SupportsTextureFormat(TextureFormat format)`
  （bool Supports纹理格式化（纹理格式化 format））
- `bool get_supportsGraphicsFence()`
  （bool get_supportsGraphicsFence（））
- `bool get_supportsMultiview()`
  （bool get_supportsMultiview（））
- `bool get_supportsStoreAndResolveAction()`
  （bool get_supports商店AndResolve动作（））
- `OperatingSystemFamily GetOperatingSystemFamily()`
  （Operating系统Family 获取Operating系统Family（））
- `string GetProcessorType()`
  （string 获取Processor类型（））
- `int GetProcessorCount()`
  （int 获取Processor数量（））
- `int GetPhysicalMemoryMB()`
  （int 获取PhysicalMemoryMB（））
- `string GetDeviceUniqueIdentifier()`
  （string 获取DeviceUniqueIdentifier（））
- `DeviceType GetDeviceType()`
  （Device类型 获取Device类型（））
- `string GetGraphicsDeviceVendor()`
  （string 获取GraphicsDeviceVendor（））
- `GraphicsDeviceType GetGraphicsDeviceType()`
  （GraphicsDevice类型 获取GraphicsDevice类型（））
- `bool GetGraphicsUVStartsAtTop()`
  （bool 获取GraphicsUVStartsAt顶部（））
- `int GetGraphicsShaderLevel()`
  （int 获取Graphics着色器等级（））
- `bool HasHiddenSurfaceRemovalOnGPU()`
  （bool 是否有隐藏的SurfaceRemovalOnGPU（））
- `bool SupportsShadows()`
  （bool SupportsShadows（））
- `CopyTextureSupport GetCopyTextureSupport()`
  （复制纹理Support 获取复制纹理Support（））
- `bool SupportsRenderTargetArrayIndexFromVertexShader()`
  （bool SupportsRender目标数组索引FromVertex着色器（））
- `int SupportedRenderTargetCount()`
  （int SupportedRender目标数量（））
- `int SupportsMultisampledTextures()`
  （int SupportsMultisampledTextures（））
- `bool SupportsMultisampleAutoResolve()`
  （bool SupportsMultisample自动Resolve（））
- `bool UsesReversedZBuffer()`
  （bool UsesReversedZ缓冲区（））
- `bool HasRenderTextureNative(RenderTextureFormat format)`
  （bool 是否有Render纹理Native（Render纹理格式化 format））
- `bool SupportsTextureFormatNative(TextureFormat format)`
  （bool Supports纹理格式化Native（纹理格式化 format））
- `bool SupportsGPUFence()`
  （bool SupportsGPUFence（））
- `bool IsFormatSupported(GraphicsFormat format, FormatUsage usage)`
  （bool 是否格式化Supported（Graphics格式化 format, 格式化Usage usage））
- `GraphicsFormat GetCompatibleFormat(GraphicsFormat format, FormatUsage usage)`
  （Graphics格式化 获取Compatible格式化（Graphics格式化 format, 格式化Usage usage））
- `GraphicsFormat GetGraphicsFormat(DefaultFormat format)`
  （Graphics格式化 获取Graphics格式化（默认的格式化 format））
- `int GetRenderTextureSupportedMSAASampleCount(RenderTextureDescriptor desc)`
  （int 获取Render纹理SupportedMSAASample数量（Render纹理Descriptor desc））
- `bool SupportsMultiview()`
  （bool SupportsMultiview（））
- `bool SupportsStoreAndResolveAction()`
  （bool Supports商店AndResolve动作（））
- `int GetRenderTextureSupportedMSAASampleCount_Injected(ref RenderTextureDescriptor desc)`
  （int 获取Render纹理SupportedMSAASampleCount_Injected（ref RenderTextureDescriptor desc））

---

## SystemThreadingTasks_TaskDebugView（系统ThreadingTasks_TaskDebug视图）

### 字段 (1)

- `Task m_task`（Task m_task）(偏移: 0x8)

### 方法 (6)

- `object get_AsyncState()`
  （object get_异步状态（））
- `TaskCreationOptions get_CreationOptions()`
  （TaskCreationOptions get_CreationOptions（））
- `Exception get_Exception()`
  （Exception get_Exception（））
- `int get_Id()`
  （int get_Id（））
- `bool get_CancellationPending()`
  （bool get_CancellationPending（））
- `TaskStatus get_Status()`
  （TaskStatus get_Status（））

---

## TEdge（TEdge）

### 字段 (18)

- `IntPoint Bot`（整数Point 机器人）(偏移: 0x8)
- `IntPoint Curr`（整数Point Curr）(偏移: 0x18)
- `IntPoint Top`（整数Point 顶部）(偏移: 0x28)
- `IntPoint Delta`（整数Point Delta）(偏移: 0x38)
- `double Dx`（double Dx）(偏移: 0x48)
- `PolyType PolyTyp`（Poly类型 PolyTyp）(偏移: 0x50)
- `EdgeSide Side`（Edge侧面 侧面）(偏移: 0x54)
- `int WindDelta`（int WindDelta）(偏移: 0x58)
- `int WindCnt`（int WindCnt）(偏移: 0x5C)
- `int WindCnt2`（int WindCnt2）(偏移: 0x60)
- `int OutIdx`（int OutIdx）(偏移: 0x64)
- `TEdge Next`（TEdge 下一个）(偏移: 0x68)
- `TEdge Prev`（TEdge Prev）(偏移: 0x6C)
- `TEdge NextInLML`（TEdge 下一个InLML）(偏移: 0x70)
- `TEdge NextInAEL`（TEdge 下一个InAEL）(偏移: 0x74)
- `TEdge PrevInAEL`（TEdge PrevInAEL）(偏移: 0x78)
- `TEdge NextInSEL`（TEdge 下一个InSEL）(偏移: 0x7C)
- `TEdge PrevInSEL`（TEdge PrevInSEL）(偏移: 0x80)

---

## TQ（TQ）

### 字段 (2)

- `Vector3 t`（三维向量 t）(偏移: 0x8)
- `Quaternion q`（Quaternion q）(偏移: 0x14)

---

## TSBPD_DM（TSBPD_DM）

**继承**: TabScoreBoard_PlayerData（Tab分数Board_玩家数据）

### 字段 (3)

- `Text rankText`（文本 rank文本）(偏移: 0x50)
- `Text kill`（文本 kill）(偏移: 0x54)
- `Text death`（文本 death）(偏移: 0x58)

### 方法 (6)

- `void SetAllTextColor(Color color)`
  （void 集合所有文本颜色（颜色 color））
- `void Bind(Player player)`
  （void 绑定（玩家 player））
- `void UpdateKill(int oldValue, int newValue)`
  （void 更新击杀（int oldValue, int newValue））
- `void UpdateDeath(int oldValue, int newValue)`
  （void 更新死亡（int oldValue, int newValue））
- `void SetRank(int rank)`
  （void 集合排名（int rank））
- `Color GetColor(bool dead)`
  （颜色 获取颜色（bool dead））

---

## TSBPD_Nano（TSBPD_纳米）

**继承**: TabScoreBoard_PlayerData（Tab分数Board_玩家数据）

### 字段 (3)

- `RawImage roleIcon`（Raw图像 role图标）(偏移: 0x50)
- `Text kill`（文本 kill）(偏移: 0x54)
- `Text survival`（文本 survival）(偏移: 0x58)

### 方法 (11)

- `void Bind(Player player)`
  （void 绑定（玩家 player））
- `void AddKillListener(PlayerData playerData)`
  （void 添加击杀监听器（玩家数据 playerData））
- `void SetAllTextColor(Color color)`
  （void 集合所有文本颜色（颜色 color））
- `void OnStartRespawn(Player player)`
  （void On开始重生（玩家 player））
- `void OnRespawn(Player player)`
  （void On重生（玩家 player））
- `void UpdateNanoRoleIcon(NanoRole oldRole, NanoRole newRole)`
  （void 更新纳米Role图标（纳米角色 oldRole, 纳米角色 newRole））
- `void SetRoleIcon(NanoRole nanoRole)`
  （void 集合Role图标（纳米角色 nanoRole））
- `void UpdateKill(int oldValue, int newValue)`
  （void 更新击杀（int oldValue, int newValue））
- `void UpdateSurvival(int oldValue, int newValue)`
  （void 更新生存（int oldValue, int newValue））
- `Color GetColor(bool dead)`
  （颜色 获取颜色（bool dead））
- `int Compare(TabScoreBoard_PlayerData other)`
  （int Compare（Tab分数Board_玩家数据 other））

---

## TSBPD_Nano6（TSBPD_Nano6）

**继承**: TSBPD_Nano（TSBPD_纳米）

### 方法 (2)

- `void AddKillListener(PlayerData playerData)`
  （void 添加击杀监听器（玩家数据 playerData））
- `int Compare(TabScoreBoard_PlayerData other)`
  （int Compare（Tab分数Board_玩家数据 other））

---

## TSBPD_TD（TSBPD_TD）

**继承**: TabScoreBoard_PlayerData（Tab分数Board_玩家数据）

### 字段 (4)

- `Text kill`（文本 kill）(偏移: 0x50)
- `Text death`（文本 death）(偏移: 0x54)
- `Image aceSign`（图像 ace标志）(偏移: 0x58)
- `GameObject deadSign`（游戏对象 dead标志）(偏移: 0x5C)

### 方法 (7)

- `void Bind(Player player)`
  （void 绑定（玩家 player））
- `void SetAllTextColor(Color color)`
  （void 集合所有文本颜色（颜色 color））
- `Color GetColor(bool dead)`
  （颜色 获取颜色（bool dead））
- `void UpdateKill(int oldValue, int newValue)`
  （void 更新击杀（int oldValue, int newValue））
- `void UpdateDeath(int oldValue, int newValue)`
  （void 更新死亡（int oldValue, int newValue））
- `void UpdateLifeState(bool alive)`
  （void 更新Life状态（bool alive））
- `void UpdateAceSign(HUD_Role.AceSign oldSign, HUD_Role.AceSign newSign)`
  （void 更新王牌标志（HUD_Role.王牌标志 oldSign, HUD_Role.王牌标志 newSign））

---

## TabScoreBoard_PlayerData（Tab分数Board_玩家数据）

**继承**: RecyclableObject（可回收对象）

### 字段 (16)

- `Color color_MyDead`（颜色 color_MyDead）(偏移: 0x0)
- `Color color_Teammate`（颜色 color_Teammate）(偏移: 0x10)
- `Color color_Enemy`（颜色 color_Enemy）(偏移: 0x20)
- `Color color_OtherDead`（颜色 color_OtherDead）(偏移: 0x30)
- `Color color_Me_DM`（颜色 color_Me_DM）(偏移: 0x40)
- `Color color_Other_DM`（颜色 color_Other_DM）(偏移: 0x50)
- `Color color_Vip`（颜色 color_Vip）(偏移: 0x60)
- `Color color_Vip_Dead`（颜色 color_Vip_Dead）(偏移: 0x70)
- `RectTransform rect`（矩形变换 rect）(偏移: 0x30)
- `RawImage vipIcon`（Raw图像 vip图标）(偏移: 0x34)
- `RawImage levelIcon`（Raw图像 level图标）(偏移: 0x38)
- `Text playerName`（文本 player名称）(偏移: 0x3C)
- `Text ping`（文本 ping）(偏移: 0x40)
- `GameObject vvipSign`（游戏对象 vvip标志）(偏移: 0x44)
- `Action<TabScoreBoard_PlayerData> rerankAction`（Action<Tab分数Board_玩家Data> rerank动作）(偏移: 0x4C)
- `int DataInterval`（int 数据间隔）(偏移: 0x80)

### 方法 (11)

- `int get_currentRank()`
  （int get_current排名（））
- `void set_currentRank(int value)`
  （void set_current排名（int value））
- `Player get_player()`
  （玩家 get_player（））
- `void set_player(Player value)`
  （void set_player（玩家 value））
- `void Bind(Player player)`
  （void 绑定（玩家 player））
- `void SetRank(int rank)`
  （void 集合排名（int rank））
- `Color GetColor(bool dead)`
  （颜色 获取颜色（bool dead））
- `void SetAllTextColor(Color color)`
  （void 集合所有文本颜色（颜色 color））
- `void UpdateLifeState(bool alive)`
  （void 更新Life状态（bool alive））
- `int Compare(TabScoreBoard_PlayerData other)`
  （int Compare（Tab分数Board_玩家数据 other））
- `int KillAndDeathCompare(Player p1, Player p2)`
  （int 击杀And死亡Compare（玩家 p1, 玩家 p2））

---

## TailStream（Tail流）

**继承**: Stream（流）

### 字段 (4)

- `byte[] _Buffer`（byte[] _缓冲区）(偏移: 0x14)
- `int _BufferSize`（int _缓冲区大小）(偏移: 0x18)
- `int _BufferIndex`（int _缓冲区索引）(偏移: 0x1C)
- `bool _BufferFull`（bool _缓冲区满）(偏移: 0x20)

### 方法 (14)

- `void Clear()`
  （void 清除（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `byte[] get_Buffer()`
  （byte[] get_缓冲区（））
- `bool get_CanRead()`
  （布尔值 获取_能否读取（））
- `bool get_CanSeek()`
  （布尔值 获取_能否查找（））
- `bool get_CanWrite()`
  （布尔值 获取_能否写入（））
- `long get_Length()`
  （长整数 获取_长度（））
- `long get_Position()`
  （长整数 获取_位置（））
- `void set_Position(long value)`
  （void 设置_位置（长整数 value））
- `void Flush()`
  （void 刷新（））
- `long Seek(long offset, SeekOrigin origin)`
  （长整数 查找（长整数 offset, 查找起点 origin））
- `void SetLength(long value)`
  （void 设置_长度（长整数 value））
- `int Read(byte[] buffer, int offset, int count)`
  （整数 读取（字节[] buffer, 整数 offset, 整数 count））
- `void Write(byte[] buffer, int offset, int count)`
  （void 写入（字节[] buffer, 整数 offset, 整数 count））

---

## TailoringInfo（Tailoring信息）

### 字段 (4)

- `int LCID`（int LCID）(偏移: 0x8)
- `int TailoringIndex`（int Tailoring索引）(偏移: 0xC)
- `int TailoringCount`（int Tailoring数量）(偏移: 0x10)
- `bool FrenchSort`（bool FrenchSort）(偏移: 0x14)

---

## TaiwanCalendar（TaiwanCalendar）

**继承**: Calendar（日历）

### 字段 (4)

- `EraInfo[] taiwanEraInfo`（EraInfo[] taiwanEra信息）(偏移: 0x0)
- `Calendar s_defaultInstance`（Calendar s_default实例）(偏移: 0x4)
- `GregorianCalendarHelper helper`（GregorianCalendar辅助器 helper）(偏移: 0x14)
- `DateTime calendarMinValue`（Date时间 calendar最小值）(偏移: 0x8)

### 方法 (17)

- `Calendar GetDefaultInstance()`
  （Calendar 获取默认的实例（））
- `DateTime get_MinSupportedDateTime()`
  （日期时间 获取_最小支持日期时间（））
- `DateTime get_MaxSupportedDateTime()`
  （日期时间 获取_最大支持日期时间（））
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
- `int[] get_Eras()`
  （整数[] 获取_纪元（））
- `int get_TwoDigitYearMax()`
  （整数 获取_两位数年份最大（））
- `int ToFourDigitYear(int year)`
  （整数 转四位数年份（整数 year））

---

## TargetMover（目标Mover）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (6)

- `LayerMask mask`（层掩码 mask）(偏移: 0xC)
- `Transform target`（变换 目标）(偏移: 0x10)
- `IAstarAI[] ais`（IAstarAI[] ais）(偏移: 0x14)
- `bool onlyOnDoubleClick`（bool onlyOnDoubleClick）(偏移: 0x18)
- `bool use2D`（bool use2D）(偏移: 0x19)
- `Camera cam`（摄像机 cam）(偏移: 0x1C)

### 方法 (4)

- `void Start()`
  （void 开始（））
- `void OnGUI()`
  （void GUI时（））
- `void Update()`
  （void 更新（））
- `void UpdateTargetPosition()`
  （void 更新目标Position（））

---

## TargetPositionCache（目标Position缓存）

### 字段 (2)

- `TargetPositionCache.Mode m_CacheMode`（目标PositionCache.模式 m_缓存模式）(偏移: 0x4)
- `TargetPositionCache.TimeRange m_CacheTimeRange`（目标PositionCache.时间范围 m_缓存时间范围）(偏移: 0x18)

### 方法 (19)

- `bool get_UseCache()`
  （bool get_Use缓存（））
- `void set_UseCache(bool value)`
  （void set_Use缓存（bool value））
- `TargetPositionCache.Mode get_CacheMode()`
  （目标PositionCache.模式 get_缓存模式（））
- `void set_CacheMode(TargetPositionCache.Mode value)`
  （void set_缓存模式（目标PositionCache.模式 value））
- `bool get_IsRecording()`
  （bool get_是否Recording（））
- `bool get_CurrentPlaybackTimeValid()`
  （bool get_当前Playback时间Valid（））
- `bool get_IsEmpty()`
  （布尔值 获取_是否为空（））
- `float get_CurrentTime()`
  （float get_当前时间（））
- `void set_CurrentTime(float value)`
  （void set_当前时间（float value））
- `int get_CurrentFrame()`
  （int get_当前Frame（））
- `void set_CurrentFrame(int value)`
  （void set_当前Frame（int value））
- `bool get_IsCameraCut()`
  （bool get_是否摄像机Cut（））
- `void set_IsCameraCut(bool value)`
  （void set_是否摄像机Cut（bool value））
- `TargetPositionCache.TimeRange get_CacheTimeRange()`
  （目标PositionCache.时间范围 get_缓存时间范围（））
- `bool get_HasHurrentTime()`
  （bool get_是否有Hurrent时间（））
- `void ClearCache()`
  （void 清除缓存（））
- `void CreatePlaybackCurves()`
  （void 创建PlaybackCurves（））
- `Vector3 GetTargetPosition(Transform target)`
  （三维向量 获取目标Position（变换 target））
- `Quaternion GetTargetRotation(Transform target)`
  （Quaternion 获取目标Rotation（变换 target））

---

## TargetPositionCache.CacheCurve（目标PositionCache.缓存Curve）

### 字段 (3)

- `float StartTime`（float 开始时间）(偏移: 0x8)
- `float StepSize`（float Step大小）(偏移: 0xC)
- `List<TargetPositionCache.CacheCurve.Item> m_Cache`（List<目标PositionCache.缓存Curve.Item> m_缓存）(偏移: 0x10)

### 方法 (4)

- `int get_Count()`
  （整数 获取_数量（））
- `void Add(TargetPositionCache.CacheCurve.Item item)`
  （void 添加（目标PositionCache.缓存Curve.项目 item））
- `void AddUntil(TargetPositionCache.CacheCurve.Item item, float time, bool isCut)`
  （void 添加Until（目标PositionCache.缓存Curve.项目 item, float time, bool isCut））
- `TargetPositionCache.CacheCurve.Item Evaluate(float time)`
  （目标PositionCache.缓存Curve.项目 Evaluate（float time））

---

## TargetPositionCache.CacheCurve.Item（目标PositionCache.缓存Curve.项目）

### 字段 (2)

- `Vector3 Pos`（三维向量 Pos）(偏移: 0x0)
- `Quaternion Rot`（Quaternion Rot）(偏移: 0xC)

### 方法 (2)

- `TargetPositionCache.CacheCurve.Item Lerp(TargetPositionCache.CacheCurve.Item a, TargetPositionCache.CacheCurve.Item b, float t)`
  （目标PositionCache.缓存Curve.项目 Lerp（目标PositionCache.缓存Curve.项目 a, 目标PositionCache.缓存Curve.项目 b, float t））
- `TargetPositionCache.CacheCurve.Item get_Empty()`
  （目标PositionCache.缓存Curve.项目 get_空（））

---

## TargetPositionCache.CacheEntry（目标PositionCache.缓存Entry）

### 字段 (2)

- `TargetPositionCache.CacheCurve Curve`（目标PositionCache.缓存Curve Curve）(偏移: 0x8)
- `List<TargetPositionCache.CacheEntry.RecordingItem> RawItems`（List<目标PositionCache.缓存Entry.RecordingItem> RawItems）(偏移: 0xC)

### 方法 (2)

- `void AddRawItem(float time, bool isCut, Transform target)`
  （void 添加Raw项目（float time, bool isCut, 变换 target））
- `void CreateCurves()`
  （void 创建Curves（））

---

## TargetPositionCache.CacheEntry.RecordingItem（目标PositionCache.缓存Entry.Recording项目）

### 字段 (3)

- `float Time`（float 时间）(偏移: 0x0)
- `bool IsCut`（bool 是否Cut）(偏移: 0x4)
- `TargetPositionCache.CacheCurve.Item Item`（目标PositionCache.缓存Curve.项目 项目）(偏移: 0x8)

---

## TargetPositionCache.Mode（目标PositionCache.模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## TargetPositionCache.TimeRange（目标PositionCache.时间范围）

### 字段 (2)

- `float Start`（float 开始）(偏移: 0x0)
- `float End`（float 结束）(偏移: 0x4)

### 方法 (4)

- `bool get_IsEmpty()`
  （布尔值 获取_是否为空（））
- `bool Contains(float time)`
  （bool Contains（float time））
- `TargetPositionCache.TimeRange get_Empty()`
  （目标PositionCache.时间范围 get_空（））
- `void Include(float time)`
  （void Include（float time））

---

## TargetType（目标类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Task（Task）

**继承**: IThreadPoolWorkItem, IAsyncResult, IDisposable（IThread池Work项目, I异步Result, IDisposable）

### 字段 (21)

- `Task t_currentTask`（Task t_currentTask）(偏移: 0x80000000)
- `StackGuard t_stackGuard`（栈Guard t_stackGuard）(偏移: 0x80000004)
- `int s_taskIdCounter`（int s_taskIdCounter）(偏移: 0x0)
- `TaskFactory s_factory`（Task工厂 s_factory）(偏移: 0x4)
- `int m_taskId`（int m_taskId）(偏移: 0x8)
- `object m_action`（object m_action）(偏移: 0xC)
- `object m_stateObject`（object m_state对象）(偏移: 0x10)
- `TaskScheduler m_taskScheduler`（TaskScheduler m_taskScheduler）(偏移: 0x14)
- `Task m_parent`（Task m_parent）(偏移: 0x18)
- `int m_stateFlags`（int m_stateFlags）(偏移: 0x1C)
- `object m_continuationObject`（object m_continuation对象）(偏移: 0x20)
- `object s_taskCompletionSentinel`（object s_taskCompletionSentinel）(偏移: 0x8)
- `bool s_asyncDebuggingEnabled`（bool s_asyncDebugging启用的）(偏移: 0xC)
- `object s_activeTasksLock`（object s_activeTasksLock）(偏移: 0x14)
- `Task.ContingentProperties m_contingentProperties`（Task.ContingentProperties m_contingentProperties）(偏移: 0x24)
- `Action<object> s_taskCancelCallback`（Action<object> s_task取消回调）(偏移: 0x18)
- `Func<Task.ContingentProperties> s_createContingentProperties`（Func<Task.ContingentProperties> s_createContingentProperties）(偏移: 0x1C)
- `Task s_completedTask`（Task s_completedTask）(偏移: 0x20)
- `Predicate<Task> s_IsExceptionObservedByParentPredicate`（Predicate<Task> s_是否ExceptionObservedBy父级Predicate）(偏移: 0x24)
- `ContextCallback s_ecCallback`（Context回调 s_ec回调）(偏移: 0x28)
- `Predicate<object> s_IsTaskContinuationNullPredicate`（Predicate<object> s_是否TaskContinuationNullPredicate）(偏移: 0x2C)

### 方法 (111)

- `bool AddToActiveTasks(Task task)`
  （bool 添加To激活的Tasks（Task task））
- `void RemoveFromActiveTasks(int taskId)`
  （void 移除From激活的Tasks（int taskId））
- `void TaskConstructorCore(object action, object state, CancellationToken cancellationToken, TaskCreationOptions creationOptions, InternalTaskOptions internalOptions, TaskScheduler scheduler)`
  （void TaskConstructorCore（object action, object state, Cancellation令牌 cancellationToken, TaskCreationOptions creationOptions, 内部的TaskOptions internalOptions, TaskScheduler scheduler））
- `void AssignCancellationToken(CancellationToken cancellationToken, Task antecedent, TaskContinuation continuation)`
  （void AssignCancellation令牌（Cancellation令牌 cancellationToken, Task antecedent, TaskContinuation continuation））
- `void TaskCancelCallback(object o)`
  （void Task取消回调（object o））
- `string get_DebuggerDisplayMethodDescription()`
  （string get_DebuggerDisplayMethodDescription（））
- `void PossiblyCaptureContext(ref StackCrawlMark stackMark)`
  （void PossiblyCaptureContext（ref StackCrawlMark stackMark））
- `TaskCreationOptions get_Options()`
  （TaskCreationOptions get_Options（））
- `TaskCreationOptions OptionsMethod(int flags)`
  （TaskCreationOptions OptionsMethod（int flags））
- `bool AtomicStateUpdate(int newBits, int illegalBits)`
  （bool Atomic状态更新（int newBits, int illegalBits））
- `bool AtomicStateUpdate(int newBits, int illegalBits, ref int oldFlags)`
  （bool Atomic状态更新（int newBits, int illegalBits, ref int oldFlags））
- `void SetNotificationForWaitCompletion(bool enabled)`
  （void 集合NotificationForWaitCompletion（bool enabled））
- `bool NotifyDebuggerOfWaitCompletionIfNecessary()`
  （bool NotifyDebuggerOfWaitCompletionIfNecessary（））
- `bool get_IsWaitNotificationEnabledOrNotRanToCompletion()`
  （bool get_是否WaitNotification启用的OrNotRanToCompletion（））
- `bool get_ShouldNotifyDebuggerOfWaitCompletion()`
  （bool get_应该NotifyDebuggerOfWaitCompletion（））
- `bool get_IsWaitNotificationEnabled()`
  （bool get_是否WaitNotification启用的（））
- `void NotifyDebuggerOfWaitCompletion()`
  （void NotifyDebuggerOfWaitCompletion（））
- `bool MarkStarted()`
  （bool MarkStarted（））
- `bool FireTaskScheduledIfNeeded(TaskScheduler ts)`
  （bool 开火TaskScheduledIfNeeded（TaskScheduler ts））
- `void AddNewChild()`
  （void 添加新的子级（））
- `void DisregardChild()`
  （void Disregard子级（））
- `Task InternalStartNew(Task creatingTask, Delegate action, object state, CancellationToken cancellationToken, TaskScheduler scheduler, TaskCreationOptions options, InternalTaskOptions internalOptions, ref StackCrawlMark stackMark)`
  （Task 内部的开始新的（Task creatingTask, 委托 action, object state, Cancellation令牌 cancellationToken, TaskScheduler scheduler, TaskCreationOptions options, 内部的TaskOptions internalOptions, ref StackCrawlMark stackMark））
- `int NewId()`
  （int 新的Id（））
- `int get_Id()`
  （int get_Id（））
- `Task get_InternalCurrent()`
  （Task get_内部的当前（））
- `Task InternalCurrentIfAttached(TaskCreationOptions creationOptions)`
  （Task 内部的当前IfAttached（TaskCreationOptions creationOptions））
- `StackGuard get_CurrentStackGuard()`
  （栈Guard get_当前栈Guard（））
- `AggregateException get_Exception()`
  （AggregateException get_Exception（））
- `TaskStatus get_Status()`
  （TaskStatus get_Status（））
- `bool get_IsCanceled()`
  （bool get_是否Canceled（））
- `bool get_IsCancellationRequested()`
  （bool get_是否CancellationRequested（））
- `Task.ContingentProperties EnsureContingentPropertiesInitialized(bool needsProtection)`
  （Task.ContingentProperties EnsureContingentPropertiesInitialized（bool needsProtection））
- `Task.ContingentProperties EnsureContingentPropertiesInitializedCore(bool needsProtection)`
  （Task.ContingentProperties EnsureContingentPropertiesInitializedCore（bool needsProtection））
- `CancellationToken get_CancellationToken()`
  （Cancellation令牌 get_Cancellation令牌（））
- `bool get_IsCancellationAcknowledged()`
  （bool get_是否CancellationAcknowledged（））
- `bool get_IsCompleted()`
  （布尔值 获取_是否完成（））
- `bool IsCompletedMethod(int flags)`
  （bool 是否CompletedMethod（int flags））
- `bool get_IsRanToCompletion()`
  （bool get_是否RanToCompletion（））
- `TaskCreationOptions get_CreationOptions()`
  （TaskCreationOptions get_CreationOptions（））
- `object get_AsyncState()`
  （object get_异步状态（））
- `TaskScheduler get_ExecutingTaskScheduler()`
  （TaskScheduler get_ExecutingTaskScheduler（））
- `TaskFactory get_Factory()`
  （Task工厂 get_工厂（））
- `Task get_CompletedTask()`
  （Task get_CompletedTask（））
- `ManualResetEventSlim get_CompletedEvent()`
  （手动重置事件Slim get_Completed事件（））
- `bool get_IsSelfReplicatingRoot()`
  （bool get_是否SelfReplicating根（））
- `bool get_IsChildReplica()`
  （bool get_是否子级Replica（））
- `bool get_ExceptionRecorded()`
  （bool get_ExceptionRecorded（））
- `bool get_IsFaulted()`
  （bool get_是否Faulted（））
- `ExecutionContext get_CapturedContext()`
  （ExecutionContext get_CapturedContext（））
- `void set_CapturedContext(ExecutionContext value)`
  （void set_CapturedContext（ExecutionContext value））
- `ExecutionContext CopyExecutionContext(ExecutionContext capturedContext)`
  （ExecutionContext 复制ExecutionContext（ExecutionContext capturedContext））
- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `void ScheduleAndStart(bool needsProtection)`
  （void ScheduleAnd开始（bool needsProtection））
- `void AddException(object exceptionObject)`
  （void 添加Exception（object exceptionObject））
- `void AddException(object exceptionObject, bool representsCancellation)`
  （void 添加Exception（object exceptionObject, bool representsCancellation））
- `AggregateException GetExceptions(bool includeTaskCanceledExceptions)`
  （AggregateException 获取Exceptions（bool includeTaskCanceledExceptions））
- `ReadOnlyCollection<ExceptionDispatchInfo> GetExceptionDispatchInfos()`
  （ReadOnlyCollection<ExceptionDispatchInfo> 获取ExceptionDispatchInfos（））
- `ExceptionDispatchInfo GetCancellationExceptionDispatchInfo()`
  （ExceptionDispatch信息 获取CancellationExceptionDispatch信息（））
- `void ThrowIfExceptional(bool includeTaskCanceledExceptions)`
  （void 投掷IfExceptional（bool includeTaskCanceledExceptions））
- `void UpdateExceptionObservedStatus()`
  （void 更新ExceptionObservedStatus（））
- `bool get_IsExceptionObservedByParent()`
  （bool get_是否ExceptionObservedBy父级（））
- `bool get_IsDelegateInvoked()`
  （bool get_是否委托Invoked（））
- `void Finish(bool bUserDelegateExecuted)`
  （void Finish（bool bUserDelegateExecuted））
- `void FinishStageTwo()`
  （void FinishStageTwo（））
- `void FinishStageThree()`
  （void FinishStageThree（））
- `void ProcessChildCompletion(Task childTask)`
  （void 处理子级Completion（Task childTask））
- `void AddExceptionsFromChildren()`
  （void 添加ExceptionsFromChildren（））
- `void FinishThreadAbortedTask(bool bTAEAddedToExceptionHolder, bool delegateRan)`
  （void FinishThreadAbortedTask（bool bTAEAddedToExceptionHolder, bool delegateRan））
- `void Execute()`
  （void 执行（））
- `bool ShouldReplicate()`
  （bool 应该Replicate（））
- `Task CreateReplicaTask(Action<object> taskReplicaDelegate, object stateObject, Task parentTask, TaskScheduler taskScheduler, TaskCreationOptions creationOptionsForReplica, InternalTaskOptions internalOptionsForReplica)`
  （Task 创建ReplicaTask（Action<object> taskReplicaDelegate, object stateObject, Task parentTask, TaskScheduler taskScheduler, TaskCreationOptions creationOptionsForReplica, 内部的TaskOptions internalOptionsForReplica））
- `object get_SavedStateForNextReplica()`
  （object get_Saved状态For下一个Replica（））
- `void set_SavedStateFromPreviousReplica(object value)`
  （void set_Saved状态From上一个Replica（object value））
- `Task get_HandedOverChildReplica()`
  （Task get_HandedOver子级Replica（））
- `void set_HandedOverChildReplica(Task value)`
  （void set_HandedOver子级Replica（Task value））
- `void ExecuteSelfReplicating(Task root)`
  （void 执行SelfReplicating（Task root））
- `bool ExecuteEntry(bool bPreventDoubleExecution)`
  （bool 执行Entry（bool bPreventDoubleExecution））
- `void ExecuteWithThreadLocal(ref Task currentTaskSlot)`
  （void 执行WithThread本地的（ref Task currentTaskSlot））
- `void ExecutionContextCallback(object obj)`
  （void ExecutionContext回调（object obj））
- `void InnerInvoke()`
  （void InnerInvoke（））
- `void InnerInvokeWithArg(Task childTask)`
  （void InnerInvokeWithArg（Task childTask））
- `void HandleException(Exception unhandledException)`
  （void 句柄Exception（Exception unhandledException））
- `TaskAwaiter GetAwaiter()`
  （TaskAwaiter 获取Awaiter（））
- `void SetContinuationForAwait(Action continuationAction, bool continueOnCapturedContext, bool flowExecutionContext, ref StackCrawlMark stackMark)`
  （void 集合ContinuationForAwait（动作 continuationAction, bool continueOnCapturedContext, bool flowExecutionContext, ref StackCrawlMark stackMark））
- `YieldAwaitable Yield()`
  （YieldAwaitable Yield（））
- `bool WrappedTryRunInline()`
  （bool WrappedTry运行Inline（））
- `bool InternalWait(int millisecondsTimeout, CancellationToken cancellationToken)`
  （bool 内部的Wait（int millisecondsTimeout, Cancellation令牌 cancellationToken））
- `bool SpinThenBlockingWait(int millisecondsTimeout, CancellationToken cancellationToken)`
  （bool SpinThenBlockingWait（int millisecondsTimeout, Cancellation令牌 cancellationToken））
- `bool SpinWait(int millisecondsTimeout)`
  （bool SpinWait（int millisecondsTimeout））
- `bool InternalCancel(bool bCancelNonExecutingOnly)`
  （bool 内部的取消（bool bCancelNonExecutingOnly））
- `void RecordInternalCancellationRequest()`
  （void Record内部的Cancellation请求（））
- `void RecordInternalCancellationRequest(CancellationToken tokenToRecord)`
  （void Record内部的Cancellation请求（Cancellation令牌 tokenToRecord））
- `void RecordInternalCancellationRequest(CancellationToken tokenToRecord, object cancellationException)`
  （void Record内部的Cancellation请求（Cancellation令牌 tokenToRecord, object cancellationException））
- `void CancellationCleanupLogic()`
  （void Cancellation清理Logic（））
- `void SetCancellationAcknowledged()`
  （void 集合CancellationAcknowledged（））
- `void FinishContinuations()`
  （void FinishContinuations（））
- `void LogFinishCompletionNotification()`
  （void LogFinishCompletionNotification（））
- `Task ContinueWith(Action<Task, object> continuationAction, object state, CancellationToken cancellationToken, TaskContinuationOptions continuationOptions, TaskScheduler scheduler)`
  （Task ContinueWith（Action<Task, object> continuationAction, object state, Cancellation令牌 cancellationToken, TaskContinuationOptions continuationOptions, TaskScheduler scheduler））
- `Task ContinueWith(Action<Task, object> continuationAction, object state, TaskScheduler scheduler, CancellationToken cancellationToken, TaskContinuationOptions continuationOptions, ref StackCrawlMark stackMark)`
  （Task ContinueWith（Action<Task, object> continuationAction, object state, TaskScheduler scheduler, Cancellation令牌 cancellationToken, TaskContinuationOptions continuationOptions, ref StackCrawlMark stackMark））
- `void CreationOptionsFromContinuationOptions(TaskContinuationOptions continuationOptions, out TaskCreationOptions creationOptions, out InternalTaskOptions internalOptions)`
  （void CreationOptionsFromContinuationOptions（TaskContinuationOptions continuationOptions, out TaskCreationOptions creationOptions, out InternalTaskOptions internalOptions））
- `void ContinueWithCore(Task continuationTask, TaskScheduler scheduler, CancellationToken cancellationToken, TaskContinuationOptions options)`
  （void ContinueWithCore（Task continuationTask, TaskScheduler scheduler, Cancellation令牌 cancellationToken, TaskContinuationOptions options））
- `void AddCompletionAction(ITaskCompletionAction action)`
  （void 添加Completion动作（ITaskCompletion动作 action））
- `void AddCompletionAction(ITaskCompletionAction action, bool addBeforeOthers)`
  （void 添加Completion动作（ITaskCompletion动作 action, bool addBeforeOthers））
- `bool AddTaskContinuationComplex(object tc, bool addBeforeOthers)`
  （bool 添加TaskContinuationComplex（object tc, bool addBeforeOthers））
- `bool AddTaskContinuation(object tc, bool addBeforeOthers)`
  （bool 添加TaskContinuation（object tc, bool addBeforeOthers））
- `void RemoveContinuation(object continuationObject)`
  （void 移除Continuation（object continuationObject））
- `Task FromCancellation(CancellationToken cancellationToken)`
  （Task FromCancellation（Cancellation令牌 cancellationToken））
- `Task Delay(int millisecondsDelay)`
  （Task 延迟（int millisecondsDelay））
- `Task Delay(int millisecondsDelay, CancellationToken cancellationToken)`
  （Task 延迟（int millisecondsDelay, Cancellation令牌 cancellationToken））
- `Task<Task> WhenAny(Task[] tasks)`
  （Task<Task> When任意（Task[] tasks））

---

## Task.ContingentProperties（Task.ContingentProperties）

### 字段 (8)

- `ExecutionContext m_capturedContext`（ExecutionContext m_capturedContext）(偏移: 0x8)
- `ManualResetEventSlim m_completionEvent`（手动重置事件Slim m_completion事件）(偏移: 0xC)
- `TaskExceptionHolder m_exceptionsHolder`（TaskExceptionHolder m_exceptionsHolder）(偏移: 0x10)
- `CancellationToken m_cancellationToken`（Cancellation令牌 m_cancellation令牌）(偏移: 0x14)
- `Shared<CancellationTokenRegistration> m_cancellationRegistration`（Shared<Cancellation令牌Registration> m_cancellationRegistration）(偏移: 0x18)
- `int m_internalCancellationRequested`（int m_internalCancellationRequested）(偏移: 0x1C)
- `int m_completionCountdown`（int m_completionCountdown）(偏移: 0x20)
- `List<Task> m_exceptionalChildren`（List<Task> m_exceptionalChildren）(偏移: 0x24)

### 方法 (2)

- `void SetCompleted()`
  （void 集合Completed（））
- `void DeregisterCancellationCallback()`
  （void DeregisterCancellation回调（））

---

## Task.DelayPromise（Task.延迟Promise）

**继承**: Task<VoidTaskResult>（Task<VoidTaskResult>）

### 字段 (3)

- `CancellationToken Token`（Cancellation令牌 令牌）(偏移: 0x2C)
- `CancellationTokenRegistration Registration`（Cancellation令牌Registration Registration）(偏移: 0x30)
- `Timer Timer`（计时器 计时器）(偏移: 0x3C)

### 方法 (1)

- `void Complete()`
  （void Complete（））

---

## Task.SetOnInvokeMres（Task.集合OnInvokeMres）

**继承**: ManualResetEventSlim, ITaskCompletionAction（手动重置事件Slim, ITaskCompletion动作）

### 方法 (1)

- `void Invoke(Task completingTask)`
  （void Invoke（Task completingTask））

---

## TaskAwaiter（TaskAwaiter）

**继承**: ICriticalNotifyCompletion（ICriticalNotifyCompletion）

### 字段 (1)

- `Task m_task`（Task m_task）(偏移: 0x0)

### 方法 (7)

- `bool get_IsCompleted()`
  （布尔值 获取_是否完成（））
- `void UnsafeOnCompleted(Action continuation)`
  （void UnsafeOnCompleted（动作 continuation））
- `void GetResult()`
  （void 获取Result（））
- `void ValidateEnd(Task task)`
  （void 验证结束（Task task））
- `void HandleNonSuccessAndDebuggerNotification(Task task)`
  （void 句柄NonSuccessAndDebuggerNotification（Task task））
- `void ThrowForNonSuccess(Task task)`
  （void 投掷ForNonSuccess（Task task））
- `void OnCompletedInternal(Task task, Action continuation, bool continueOnCapturedContext, bool flowExecutionContext)`
  （void OnCompleted内部的（Task task, 动作 continuation, bool continueOnCapturedContext, bool flowExecutionContext））

---

## TaskCanceledException（TaskCanceledException）

**继承**: OperationCanceledException（OperationCanceledException）

### 字段 (1)

- `Task m_canceledTask`（Task m_canceledTask）(偏移: 0x48)

---

## TaskContinuation（TaskContinuation）

### 方法 (1)

- `void InlineIfPossibleOrElseQueue(Task task, bool needsProtection)`
  （void InlineIfPossibleOrElse队列（Task task, bool needsProtection））

---

## TaskContinuationOptions（TaskContinuationOptions）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## TaskCreationOptions（TaskCreationOptions）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## TaskExceptionHolder（TaskExceptionHolder）

### 字段 (7)

- `bool s_failFastOnUnobservedException`（bool s_failFastOnUnobservedException）(偏移: 0x0)
- `bool s_domainUnloadStarted`（bool s_domainUnloadStarted）(偏移: 0x1)
- `EventHandler s_adUnloadEventHandler`（事件处理器 s_adUnload事件处理器）(偏移: 0x4)
- `Task m_task`（Task m_task）(偏移: 0x8)
- `List<ExceptionDispatchInfo> m_faultExceptions`（List<ExceptionDispatchInfo> m_faultExceptions）(偏移: 0xC)
- `ExceptionDispatchInfo m_cancellationException`（ExceptionDispatch信息 m_cancellationException）(偏移: 0x10)
- `bool m_isHandled`（bool m_isHandled）(偏移: 0x14)

### 方法 (13)

- `bool ShouldFailFastOnUnobservedException()`
  （bool 应该FailFastOnUnobservedException（））
- `void EnsureADUnloadCallbackRegistered()`
  （void EnsureADUnload回调Registered（））
- `void AppDomainUnloadCallback(object sender, EventArgs e)`
  （void AppDomainUnload回调（object sender, 事件Args e））
- `void Finalize()`
  （void 终结（））
- `bool get_ContainsFaultList()`
  （bool get_ContainsFault列表（））
- `void Add(object exceptionObject, bool representsCancellation)`
  （void 添加（object exceptionObject, bool representsCancellation））
- `void SetCancellationException(object exceptionObject)`
  （void 集合CancellationException（object exceptionObject））
- `void AddFaultException(object exceptionObject)`
  （void 添加FaultException（object exceptionObject））
- `void MarkAsUnhandled()`
  （void MarkAsUnhandled（））
- `void MarkAsHandled(bool calledFromFinalizer)`
  （void MarkAsHandled（bool calledFromFinalizer））
- `AggregateException CreateExceptionObject(bool calledFromFinalizer, Exception includeThisException)`
  （AggregateException 创建Exception对象（bool calledFromFinalizer, Exception includeThisException））
- `ReadOnlyCollection<ExceptionDispatchInfo> GetExceptionDispatchInfos()`
  （ReadOnlyCollection<ExceptionDispatchInfo> 获取ExceptionDispatchInfos（））
- `ExceptionDispatchInfo GetCancellationExceptionDispatchInfo()`
  （ExceptionDispatch信息 获取CancellationExceptionDispatch信息（））

---

## TaskFactory（Task工厂）

### 字段 (4)

- `CancellationToken m_defaultCancellationToken`（Cancellation令牌 m_defaultCancellation令牌）(偏移: 0x8)
- `TaskScheduler m_defaultScheduler`（TaskScheduler m_defaultScheduler）(偏移: 0xC)
- `TaskCreationOptions m_defaultCreationOptions`（TaskCreationOptions m_defaultCreationOptions）(偏移: 0x10)
- `TaskContinuationOptions m_defaultContinuationOptions`（TaskContinuationOptions m_defaultContinuationOptions）(偏移: 0x14)

### 方法 (4)

- `void CheckCreationOptions(TaskCreationOptions creationOptions)`
  （void 检查CreationOptions（TaskCreationOptions creationOptions））
- `Task StartNew(Action action, CancellationToken cancellationToken, TaskCreationOptions creationOptions, TaskScheduler scheduler)`
  （Task 开始新的（动作 action, Cancellation令牌 cancellationToken, TaskCreationOptions creationOptions, TaskScheduler scheduler））
- `Task<Task> CommonCWAnyLogic(IList<Task> tasks)`
  （Task<Task> CommonCW任意Logic（IList<Task> tasks））
- `void CheckMultiTaskContinuationOptions(TaskContinuationOptions continuationOptions)`
  （void 检查多个TaskContinuationOptions（TaskContinuationOptions continuationOptions））

---

## TaskFactory.CompleteOnInvokePromise（TaskFactory.CompleteOnInvokePromise）

**继承**: Task<Task>, ITaskCompletionAction（Task<Task>, ITaskCompletion动作）

### 字段 (2)

- `IList<Task> _tasks`（IList<Task> _tasks）(偏移: 0x2C)
- `int m_firstTaskAlreadyCompleted`（int m_firstTaskAlreadyCompleted）(偏移: 0x30)

### 方法 (1)

- `void Invoke(Task completingTask)`
  （void Invoke（Task completingTask））

---

## TaskScheduler（TaskScheduler）

### 字段 (5)

- `TaskScheduler s_defaultTaskScheduler`（TaskScheduler s_defaultTaskScheduler）(偏移: 0x4)
- `int s_taskSchedulerIdCounter`（int s_taskSchedulerIdCounter）(偏移: 0x8)
- `int m_taskSchedulerId`（int m_taskSchedulerId）(偏移: 0x8)
- `EventHandler<UnobservedTaskExceptionEventArgs> _unobservedTaskException`（事件Handler<UnobservedTaskException事件Args> _unobservedTaskException）(偏移: 0xC)
- `object _unobservedTaskExceptionLockObject`（object _unobservedTaskExceptionLock对象）(偏移: 0x10)

### 方法 (11)

- `bool TryRunInline(Task task, bool taskWasPreviouslyQueued)`
  （bool Try运行Inline（Task task, bool taskWasPreviouslyQueued））
- `bool TryDequeue(Task task)`
  （bool TryDequeue（Task task））
- `void NotifyWorkItemProgress()`
  （void NotifyWork项目Progress（））
- `bool get_RequiresAtomicStartTransition()`
  （bool get_RequiresAtomic开始Transition（））
- `void InternalQueueTask(Task task)`
  （void 内部的队列Task（Task task））
- `void AddToActiveTaskSchedulers()`
  （void 添加To激活的TaskSchedulers（））
- `TaskScheduler get_Default()`
  （TaskScheduler get_默认的（））
- `TaskScheduler get_Current()`
  （TaskScheduler get_当前（））
- `TaskScheduler get_InternalCurrent()`
  （TaskScheduler get_内部的当前（））
- `int get_Id()`
  （int get_Id（））
- `void PublishUnobservedTaskException(object sender, UnobservedTaskExceptionEventArgs ueea)`
  （void PublishUnobservedTaskException（object sender, UnobservedTaskException事件Args ueea））

---

## TaskScheduler.SystemThreadingTasks_TaskSchedulerDebugView（TaskScheduler.系统ThreadingTasks_TaskSchedulerDebug视图）

### 字段 (1)

- `TaskScheduler m_taskScheduler`（TaskScheduler m_taskScheduler）(偏移: 0x8)

### 方法 (2)

- `int get_Id()`
  （int get_Id（））
- `IEnumerable<Task> get_ScheduledTasks()`
  （IEnumerable<Task> get_ScheduledTasks（））

---

## TaskSchedulerAwaitTaskContinuation（TaskSchedulerAwaitTaskContinuation）

**继承**: AwaitTaskContinuation（AwaitTaskContinuation）

### 字段 (1)

- `TaskScheduler m_scheduler`（TaskScheduler m_scheduler）(偏移: 0x10)

---

## TaskStatus（TaskStatus）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Team（队伍）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## TeamExpand（队伍Expand）

### 方法 (1)

- `Team GetEnemyTeam(Team team)`
  （队伍 获取Enemy队伍（队伍 team））

---

## TermInfoDriver（Term信息Driver）

**继承**: IConsoleDriver（IConsoleDriver）

### 字段 (44)

- `int* native_terminal_size`（int* native_terminal_size）(偏移: 0x0)
- `int terminal_size`（int terminal_size）(偏移: 0x4)
- `string[] locations`（string[] locations）(偏移: 0x8)
- `TermInfoReader reader`（Term信息读取器 reader）(偏移: 0x8)
- `int cursorLeft`（int cursor左）(偏移: 0xC)
- `int cursorTop`（int cursor顶部）(偏移: 0x10)
- `string title`（string title）(偏移: 0x14)
- `string titleFormat`（string title格式化）(偏移: 0x18)
- `bool cursorVisible`（bool cursor可见的）(偏移: 0x1C)
- `string csrVisible`（string csr可见的）(偏移: 0x20)
- `string csrInvisible`（string csrInvisible）(偏移: 0x24)
- `string clear`（string clear）(偏移: 0x28)
- `string bell`（string bell）(偏移: 0x2C)
- `string term`（string term）(偏移: 0x30)
- `StreamReader stdin`（流读取器 stdin）(偏移: 0x34)
- `CStreamWriter stdout`（C流写入器 stdout）(偏移: 0x38)
- `int windowWidth`（int window宽度）(偏移: 0x3C)
- `int windowHeight`（int window高度）(偏移: 0x40)
- `int bufferHeight`（int buffer高度）(偏移: 0x44)
- `int bufferWidth`（int buffer宽度）(偏移: 0x48)
- `char[] buffer`（char[] buffer）(偏移: 0x4C)
- `int readpos`（int readpos）(偏移: 0x50)
- `int writepos`（int writepos）(偏移: 0x54)
- `string keypadXmit`（string keypadXmit）(偏移: 0x58)
- `string keypadLocal`（string keypad本地的）(偏移: 0x5C)
- `bool inited`（布尔值 已初始化）(偏移: 0x60)
- `object initLock`（object initLock）(偏移: 0x64)
- `bool initKeys`（bool initKeys）(偏移: 0x68)
- `string origPair`（string origPair）(偏移: 0x6C)
- `string origColors`（string origColors）(偏移: 0x70)
- `string cursorAddress`（string cursorAddress）(偏移: 0x74)
- `ConsoleColor fgcolor`（Console颜色 fgcolor）(偏移: 0x78)
- `string setfgcolor`（string setfgcolor）(偏移: 0x7C)
- `string setbgcolor`（string setbgcolor）(偏移: 0x80)
- `int maxColors`（int maxColors）(偏移: 0x84)
- `bool noGetPosition`（bool no获取Position）(偏移: 0x88)
- `Hashtable keymap`（Hashtable keymap）(偏移: 0x8C)
- `ByteMatcher rootmap`（ByteMatcher rootmap）(偏移: 0x90)
- `int rl_startx`（int rl_startx）(偏移: 0x94)
- `int rl_starty`（int rl_starty）(偏移: 0x98)
- `byte[] control_characters`（byte[] control_characters）(偏移: 0x9C)
- `int[] _consoleColorToAnsiCode`（int[] _console颜色ToAnsiCode）(偏移: 0xC)
- `char[] echobuf`（char[] echobuf）(偏移: 0xA0)
- `int echon`（int echon）(偏移: 0xA4)

### 方法 (32)

- `string TryTermInfoDir(string dir, string term)`
  （string TryTerm信息Dir（string dir, string term））
- `string SearchTerminfo(string term)`
  （string 搜索Terminfo（string term））
- `void WriteConsole(string str)`
  （void WriteConsole（string str））
- `bool get_Initialized()`
  （bool get_Initialized（））
- `void Init()`
  （void 初始化（））
- `void IncrementX()`
  （void IncrementX（））
- `void WriteSpecialKey(ConsoleKeyInfo key)`
  （void Write特殊键（Console键信息 key））
- `void WriteSpecialKey(char c)`
  （void Write特殊键（char c））
- `bool IsSpecialKey(ConsoleKeyInfo key)`
  （bool 是否特殊键（Console键信息 key））
- `bool IsSpecialKey(char c)`
  （bool 是否特殊键（char c））
- `void GetCursorPosition()`
  （void 获取CursorPosition（））
- `void CheckWindowDimensions()`
  （void 检查WindowDimensions（））
- `int get_WindowHeight()`
  （int get_Window高度（））
- `int get_WindowWidth()`
  （int get_Window宽度（））
- `void AddToBuffer(int b)`
  （void 添加To缓冲区（int b））
- `void AdjustBuffer()`
  （void Adjust缓冲区（））
- `ConsoleKeyInfo CreateKeyInfoFromInt(int n, bool alt)`
  （Console键信息 创建键信息From整数（int n, bool alt））
- `object GetKeyFromBuffer(bool cooked)`
  （object 获取键From缓冲区（bool cooked））
- `ConsoleKeyInfo ReadKeyInternal(out bool fresh)`
  （Console键信息 Read键内部的（out bool fresh））
- `bool InputPending()`
  （bool 输入Pending（））
- `void QueueEcho(char c)`
  （void 队列Echo（char c））
- `void Echo(ConsoleKeyInfo key)`
  （void Echo（Console键信息 key））
- `void EchoFlush()`
  （void EchoFlush（））
- `int Read([In] [Out] char[] dest, int index, int count)`
  （int Read（[In] [Out] char[] dest, int index, int count））
- `ConsoleKeyInfo ReadKey(bool intercept)`
  （控制台键信息 读取键（布尔值 拦截））
- `string ReadLine()`
  （字符串 读取行（））
- `string ReadToEnd()`
  （字符串 读取到结束（））
- `string ReadUntilConditionInternal(bool haltOnNewLine)`
  （string ReadUntilCondition内部的（bool haltOnNewLine））
- `void SetCursorPosition(int left, int top)`
  （void 集合CursorPosition（int left, int top））
- `void CreateKeyMap()`
  （void 创建键映射（））
- `void InitKeys()`
  （void 初始化Keys（））
- `void AddStringMapping(TermInfoStrings s)`
  （void 添加字符串Mapping（Term信息Strings s））

---

## TermInfoNumbers（Term信息Numbers）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## TermInfoReader（Term信息读取器）

### 字段 (6)

- `int boolSize`（int bool大小）(偏移: 0x8)
- `int numSize`（int num大小）(偏移: 0xC)
- `int strOffsets`（int strOffsets）(偏移: 0x10)
- `byte[] buffer`（byte[] buffer）(偏移: 0x14)
- `int booleansOffset`（int booleansOffset）(偏移: 0x18)
- `int intOffset`（int intOffset）(偏移: 0x1C)

### 方法 (11)

- `void DetermineVersion(short magic)`
  （void DetermineVersion（short magic））
- `void ReadHeader(byte[] buffer, ref int position)`
  （void Read标题（byte[] buffer, ref int position））
- `void ReadNames(byte[] buffer, ref int position)`
  （void ReadNames（byte[] buffer, ref int position））
- `int Get(TermInfoNumbers number)`
  （int 获取（Term信息Numbers number））
- `string Get(TermInfoStrings tstr)`
  （string 获取（Term信息Strings tstr））
- `byte[] GetStringBytes(TermInfoStrings tstr)`
  （byte[] 获取字符串Bytes（Term信息Strings tstr））
- `short GetInt16(byte[] buffer, int offset)`
  （short 获取Int16（byte[] buffer, int offset））
- `int GetInt32(byte[] buffer, int offset)`
  （int 获取Int32（byte[] buffer, int offset））
- `int GetInteger(byte[] buffer, int offset)`
  （int 获取Integer（byte[] buffer, int offset））
- `string GetString(byte[] buffer, int offset)`
  （string 获取字符串（byte[] buffer, int offset））
- `byte[] GetStringBytes(byte[] buffer, int offset)`
  （byte[] 获取字符串Bytes（byte[] buffer, int offset））

---

## TermInfoStrings（Term信息Strings）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## TerminatorCharacterEffect（Terminator角色特效）

**继承**: CharacterEffect（角色特效）

### 字段 (2)

- `CharacterEffect.FxData oroData`（角色Effect.特效数据 oro数据）(偏移: 0x1C)
- `EffectObj oro`（特效Obj oro）(偏移: 0x3C)

### 方法 (2)

- `void Update()`
  （void 更新（））
- `void Oro_RecycleEvent_Listener()`
  （void Oro_RecycleEvent_监听器（））

---

## TerminatorMoveSnd（Terminator移动Snd）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (2)

- `CharacterModel mdl`（角色模型 mdl）(偏移: 0xC)
- `float nextPlayTime`（float next播放时间）(偏移: 0x10)

### 方法 (2)

- `void Awake()`
  （void 唤醒（））
- `void Update()`
  （void 更新（））

---

## Terrain（Terrain）

**继承**: Behaviour（行为）

### 方法 (7)

- `TerrainData get_terrainData()`
  （Terrain数据 get_terrain数据（））
- `bool get_allowAutoConnect()`
  （bool get_allow自动Connect（））
- `int get_groupingID()`
  （int get_groupingID（））
- `void SetNeighbors(Terrain left, Terrain top, Terrain right, Terrain bottom)`
  （void 集合Neighbors（Terrain left, Terrain top, Terrain right, Terrain bottom））
- `Vector3 GetPosition()`
  （三维向量 获取Position（））
- `Terrain[] get_activeTerrains()`
  （Terrain[] get_activeTerrains（））
- `void GetPosition_Injected(out Vector3 ret)`
  （void 获取Position_Injected（out Vector3 ret））

---

## TerrainCallbacks（TerrainCallbacks）

### 字段 (2)

- `TerrainCallbacks.HeightmapChangedCallback heightmapChanged`（TerrainCallbacks.HeightmapChanged回调 heightmapChanged）(偏移: 0x0)
- `TerrainCallbacks.TextureChangedCallback textureChanged`（TerrainCallbacks.纹理Changed回调 textureChanged）(偏移: 0x4)

### 方法 (2)

- `void InvokeHeightmapChangedCallback(TerrainData terrainData, RectInt heightRegion, bool synched)`
  （void InvokeHeightmapChanged回调（Terrain数据 terrainData, Rect整数 heightRegion, bool synched））
- `void InvokeTextureChangedCallback(TerrainData terrainData, string textureName, RectInt texelRegion, bool synched)`
  （void Invoke纹理Changed回调（Terrain数据 terrainData, string textureName, Rect整数 texelRegion, bool synched））

---

## TerrainCallbacks.HeightmapChangedCallback（TerrainCallbacks.HeightmapChanged回调）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(Terrain terrain, RectInt heightRegion, bool synched)`
  （void Invoke（Terrain terrain, Rect整数 heightRegion, bool synched））
- `IAsyncResult BeginInvoke(Terrain terrain, RectInt heightRegion, bool synched, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Terrain terrain, Rect整数 heightRegion, bool synched, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## TerrainCallbacks.TextureChangedCallback（TerrainCallbacks.纹理Changed回调）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(Terrain terrain, string textureName, RectInt texelRegion, bool synched)`
  （void Invoke（Terrain terrain, string textureName, Rect整数 texelRegion, bool synched））
- `IAsyncResult BeginInvoke(Terrain terrain, string textureName, RectInt texelRegion, bool synched, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Terrain terrain, string textureName, Rect整数 texelRegion, bool synched, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## TerrainData（Terrain数据）

**继承**: Object（对象）

### 字段 (9)

- `int k_MaximumResolution`（int k_MaximumResolution）(偏移: 0x0)
- `int k_MinimumDetailResolutionPerPatch`（int k_MinimumDetailResolutionPerPatch）(偏移: 0x4)
- `int k_MaximumDetailResolutionPerPatch`（int k_MaximumDetailResolutionPerPatch）(偏移: 0x8)
- `int k_MaximumDetailPatchCount`（int k_MaximumDetailPatch数量）(偏移: 0xC)
- `int k_MaximumDetailsPerRes`（int k_MaximumDetailsPerRes）(偏移: 0x10)
- `int k_MinimumAlphamapResolution`（int k_MinimumAlphamapResolution）(偏移: 0x14)
- `int k_MaximumAlphamapResolution`（int k_MaximumAlphamapResolution）(偏移: 0x18)
- `int k_MinimumBaseMapResolution`（int k_Minimum基础映射Resolution）(偏移: 0x1C)
- `int k_MaximumBaseMapResolution`（int k_Maximum基础映射Resolution）(偏移: 0x20)

### 方法 (16)

- `int GetBoundaryValue(TerrainData.BoundaryValueType type)`
  （int 获取Boundary值（TerrainData.Boundary值类型 type））
- `void Internal_Create(TerrainData terrainData)`
  （void Internal_创建（Terrain数据 terrainData））
- `RenderTexture get_heightmapTexture()`
  （Render纹理 get_heightmap纹理（））
- `int get_heightmapResolution()`
  （int get_heightmapResolution（））
- `int get_internalHeightmapResolution()`
  （int get_internalHeightmapResolution（））
- `Vector3 get_heightmapScale()`
  （三维向量 get_heightmap缩放（））
- `Vector3 get_size()`
  （三维向量 get_size（））
- `Bounds get_bounds()`
  （边界 获取_边界（））
- `TreeInstance[] get_treeInstances()`
  （TreeInstance[] get_treeInstances（））
- `TreeInstance[] Internal_GetTreeInstances()`
  （TreeInstance[] Internal_获取TreeInstances（））
- `TreePrototype[] get_treePrototypes()`
  （TreePrototype[] get_treePrototypes（））
- `float GetAlphamapResolutionInternal()`
  （float 获取AlphamapResolution内部的（））
- `Terrain[] get_users()`
  （Terrain[] get_users（））
- `void get_heightmapScale_Injected(out Vector3 ret)`
  （void get_heightmapScale_Injected（out Vector3 ret））
- `void get_size_Injected(out Vector3 ret)`
  （void get_size_Injected（out Vector3 ret））
- `void get_bounds_Injected(out Bounds ret)`
  （void 获取_边界_注入（输出 Bounds ret））

---

## TerrainData.BoundaryValueType（TerrainData.Boundary值类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## TerrainUtility（Terrain工具）

### 方法 (4)

- `bool HasValidTerrains()`
  （bool 是否有ValidTerrains（））
- `void ClearConnectivity()`
  （void 清除Connectivity（））
- `TerrainUtility.TerrainGroups CollectTerrains(bool onlyAutoConnectedTerrains = True)`
  （TerrainUtility.TerrainGroups CollectTerrains（bool onlyAutoConnectedTerrains = True））
- `void AutoConnect()`
  （void 自动Connect（））

---

## TerrainUtility.TerrainMap（TerrainUtility.Terrain映射）

### 字段 (2)

- `Vector3 m_patchSize`（三维向量 m_patch大小）(偏移: 0x8)
- `TerrainUtility.TerrainMap.ErrorCode m_errorCode`（TerrainUtility.TerrainMap.ErrorCode m_errorCode）(偏移: 0x14)

### 方法 (7)

- `Terrain GetTerrain(int tileX, int tileZ)`
  （Terrain 获取Terrain（int tileX, int tileZ））
- `TerrainUtility.TerrainMap CreateFromPlacement(Terrain originTerrain, TerrainUtility.TerrainMap.TerrainFilter filter, bool fullValidation = True)`
  （TerrainUtility.Terrain映射 创建FromPlacement（Terrain originTerrain, TerrainUtility.TerrainMap.TerrainFilter filter, bool fullValidation = True））
- `TerrainUtility.TerrainMap CreateFromPlacement(Vector2 gridOrigin, Vector2 gridSize, TerrainUtility.TerrainMap.TerrainFilter filter, bool fullValidation = True)`
  （TerrainUtility.Terrain映射 创建FromPlacement（二维向量 gridOrigin, 二维向量 gridSize, TerrainUtility.TerrainMap.TerrainFilter filter, bool fullValidation = True））
- `void AddTerrainInternal(int x, int z, Terrain terrain)`
  （void 添加Terrain内部的（int x, int z, Terrain terrain））
- `bool TryToAddTerrain(int tileX, int tileZ, Terrain terrain)`
  （bool TryTo添加Terrain（int tileX, int tileZ, Terrain terrain））
- `void ValidateTerrain(int tileX, int tileZ)`
  （void 验证Terrain（int tileX, int tileZ））
- `TerrainUtility.TerrainMap.ErrorCode Validate()`
  （TerrainUtility.TerrainMap.ErrorCode 验证（））

---

## TerrainUtility.TerrainMap.ErrorCode（TerrainUtility.TerrainMap.ErrorCode）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## TerrainUtility.TerrainMap.TerrainFilter（TerrainUtility.TerrainMap.TerrainFilter）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `bool Invoke(Terrain terrain)`
  （bool Invoke（Terrain terrain））
- `IAsyncResult BeginInvoke(Terrain terrain, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Terrain terrain, 异步回调 callback, object object））
- `bool EndInvoke(IAsyncResult result)`
  （布尔值 结束调用（I异步结果 result））

---

## TerrainUtility.TerrainMap.TileCoord（TerrainUtility.TerrainMap.TileCoord）

### 字段 (2)

- `int tileX`（int tileX）(偏移: 0x0)
- `int tileZ`（int tileZ）(偏移: 0x4)

---

## Tess（Tess）

### 字段 (22)

- `Mesh _mesh`（网格 _mesh）(偏移: 0x8)
- `Vec3 _normal`（Vec3 _normal）(偏移: 0xC)
- `Vec3 _sUnit`（Vec3 _sUnit）(偏移: 0x18)
- `Vec3 _tUnit`（Vec3 _tUnit）(偏移: 0x24)
- `float _bminX`（float _bminX）(偏移: 0x30)
- `float _bminY`（float _bminY）(偏移: 0x34)
- `float _bmaxX`（float _bmaxX）(偏移: 0x38)
- `float _bmaxY`（float _bmaxY）(偏移: 0x3C)
- `WindingRule _windingRule`（WindingRule _windingRule）(偏移: 0x40)
- `Dict<Tess.ActiveRegion> _dict`（Dict<Tess.激活的Region> _dict）(偏移: 0x44)
- `PriorityQueue<MeshUtils.Vertex> _pq`（PriorityQueue<网格Utils.Vertex> _pq）(偏移: 0x48)
- `MeshUtils.Vertex _event`（网格Utils.Vertex _event）(偏移: 0x4C)
- `CombineCallback _combineCallback`（Combine回调 _combine回调）(偏移: 0x50)
- `ContourVertex[] _vertices`（ContourVertex[] _vertices）(偏移: 0x54)
- `int _vertexCount`（int _vertex数量）(偏移: 0x58)
- `int[] _elements`（int[] _elements）(偏移: 0x5C)
- `int _elementCount`（int _element数量）(偏移: 0x60)
- `float SUnitX`（float SUnitX）(偏移: 0x64)
- `float SUnitY`（float SUnitY）(偏移: 0x68)
- `float SentinelCoord`（float SentinelCoord）(偏移: 0x6C)
- `bool NoEmptyPolygons`（bool No空Polygons）(偏移: 0x70)
- `bool UsePooling`（bool UsePooling）(偏移: 0x71)

### 方法 (52)

- `Tess.ActiveRegion RegionBelow(Tess.ActiveRegion reg)`
  （Tess.激活的Region RegionBelow（Tess.激活的Region reg））
- `Tess.ActiveRegion RegionAbove(Tess.ActiveRegion reg)`
  （Tess.激活的Region RegionAbove（Tess.激活的Region reg））
- `bool EdgeLeq(Tess.ActiveRegion reg1, Tess.ActiveRegion reg2)`
  （bool EdgeLeq（Tess.激活的Region reg1, Tess.激活的Region reg2））
- `void DeleteRegion(Tess.ActiveRegion reg)`
  （void DeleteRegion（Tess.激活的Region reg））
- `void FixUpperEdge(Tess.ActiveRegion reg, MeshUtils.Edge newEdge)`
  （void Fix上半身Edge（Tess.激活的Region reg, 网格Utils.Edge newEdge））
- `Tess.ActiveRegion TopLeftRegion(Tess.ActiveRegion reg)`
  （Tess.激活的Region 顶部左Region（Tess.激活的Region reg））
- `Tess.ActiveRegion TopRightRegion(Tess.ActiveRegion reg)`
  （Tess.激活的Region 顶部右Region（Tess.激活的Region reg））
- `Tess.ActiveRegion AddRegionBelow(Tess.ActiveRegion regAbove, MeshUtils.Edge eNewUp)`
  （Tess.激活的Region 添加RegionBelow（Tess.激活的Region regAbove, 网格Utils.Edge eNewUp））
- `void ComputeWinding(Tess.ActiveRegion reg)`
  （void ComputeWinding（Tess.激活的Region reg））
- `void FinishRegion(Tess.ActiveRegion reg)`
  （void FinishRegion（Tess.激活的Region reg））
- `MeshUtils.Edge FinishLeftRegions(Tess.ActiveRegion regFirst, Tess.ActiveRegion regLast)`
  （网格Utils.Edge Finish左Regions（Tess.激活的Region regFirst, Tess.激活的Region regLast））
- `void AddRightEdges(Tess.ActiveRegion regUp, MeshUtils.Edge eFirst, MeshUtils.Edge eLast, MeshUtils.Edge eTopLeft, bool cleanUp)`
  （void 添加右Edges（Tess.激活的Region regUp, 网格Utils.Edge eFirst, 网格Utils.Edge eLast, 网格Utils.Edge eTopLeft, bool cleanUp））
- `void SpliceMergeVertices(MeshUtils.Edge e1, MeshUtils.Edge e2)`
  （void SpliceMergeVertices（网格Utils.Edge e1, 网格Utils.Edge e2））
- `void VertexWeights(MeshUtils.Vertex isect, MeshUtils.Vertex org, MeshUtils.Vertex dst, out float w0, out float w1)`
  （void VertexWeights（网格Utils.Vertex isect, 网格Utils.Vertex org, 网格Utils.Vertex dst, out float w0, out float w1））
- `void GetIntersectData(MeshUtils.Vertex isect, MeshUtils.Vertex orgUp, MeshUtils.Vertex dstUp, MeshUtils.Vertex orgLo, MeshUtils.Vertex dstLo)`
  （void 获取Intersect数据（网格Utils.Vertex isect, 网格Utils.Vertex orgUp, 网格Utils.Vertex dstUp, 网格Utils.Vertex orgLo, 网格Utils.Vertex dstLo））
- `bool CheckForRightSplice(Tess.ActiveRegion regUp)`
  （bool 检查For右Splice（Tess.激活的Region regUp））
- `bool CheckForLeftSplice(Tess.ActiveRegion regUp)`
  （bool 检查For左Splice（Tess.激活的Region regUp））
- `bool CheckForIntersect(Tess.ActiveRegion regUp)`
  （bool 检查ForIntersect（Tess.激活的Region regUp））
- `void WalkDirtyRegions(Tess.ActiveRegion regUp)`
  （void WalkDirtyRegions（Tess.激活的Region regUp））
- `void ConnectRightVertex(Tess.ActiveRegion regUp, MeshUtils.Edge eBottomLeft)`
  （void Connect右Vertex（Tess.激活的Region regUp, 网格Utils.Edge eBottomLeft））
- `void ConnectLeftDegenerate(Tess.ActiveRegion regUp, MeshUtils.Vertex vEvent)`
  （void Connect左Degenerate（Tess.激活的Region regUp, 网格Utils.Vertex vEvent））
- `void ConnectLeftVertex(MeshUtils.Vertex vEvent)`
  （void Connect左Vertex（网格Utils.Vertex vEvent））
- `void SweepEvent(MeshUtils.Vertex vEvent)`
  （void Sweep事件（网格Utils.Vertex vEvent））
- `void AddSentinel(float smin, float smax, float t)`
  （void 添加Sentinel（float smin, float smax, float t））
- `void InitEdgeDict()`
  （void 初始化EdgeDict（））
- `void DoneEdgeDict()`
  （void DoneEdgeDict（））
- `void RemoveDegenerateEdges()`
  （void 移除DegenerateEdges（））
- `void InitPriorityQ()`
  （void 初始化PriorityQ（））
- `void DonePriorityQ()`
  （void DonePriorityQ（））
- `void RemoveDegenerateFaces()`
  （void 移除DegenerateFaces（））
- `void ComputeInterior()`
  （void ComputeInterior（））
- `Vec3 get_Normal()`
  （Vec3 get_法线（））
- `void set_Normal(Vec3 value)`
  （void set_法线（Vec3 value））
- `ContourVertex[] get_Vertices()`
  （ContourVertex[] get_Vertices（））
- `int get_VertexCount()`
  （int get_Vertex数量（））
- `int[] get_Elements()`
  （int[] get_Elements（））
- `int get_ElementCount()`
  （int get_元素数量（））
- `void ComputeNormal(ref Vec3 norm)`
  （void Compute法线（ref Vec3 norm））
- `void CheckOrientation()`
  （void 检查Orientation（））
- `void ProjectPolygon()`
  （void ProjectPolygon（））
- `void TessellateMonoRegion(MeshUtils.Face face)`
  （void TessellateMonoRegion（网格Utils.Face face））
- `void TessellateInterior()`
  （void TessellateInterior（））
- `void DiscardExterior()`
  （void DiscardExterior（））
- `void SetWindingNumber(int value, bool keepOnlyBoundary)`
  （void 集合WindingNumber（int value, bool keepOnlyBoundary））
- `int GetNeighbourFace(MeshUtils.Edge edge)`
  （int 获取NeighbourFace（网格Utils.Edge edge））
- `void OutputPolymesh(ElementType elementType, int polySize)`
  （void OutputPolymesh（元素类型 elementType, int polySize））
- `void OutputContours()`
  （void OutputContours（））
- `float SignedArea(ContourVertex[] vertices)`
  （float SignedArea（ContourVertex[] vertices））
- `void AddContour(ContourVertex[] vertices)`
  （void 添加Contour（ContourVertex[] vertices））
- `void AddContour(ContourVertex[] vertices, ContourOrientation forceOrientation)`
  （void 添加Contour（ContourVertex[] vertices, ContourOrientation forceOrientation））
- `void Tessellate(WindingRule windingRule, ElementType elementType, int polySize)`
  （void Tessellate（WindingRule windingRule, 元素类型 elementType, int polySize））
- `void Tessellate(WindingRule windingRule, ElementType elementType, int polySize, CombineCallback combineCallback)`
  （void Tessellate（WindingRule windingRule, 元素类型 elementType, int polySize, Combine回调 combineCallback））

---

## Tess.ActiveRegion（Tess.激活的Region）

### 字段 (7)

- `MeshUtils.Edge _eUp`（网格Utils.Edge _e上）(偏移: 0x8)
- `Dict.Node<Tess.ActiveRegion> _nodeUp`（Dict.Node<Tess.激活的Region> _node上）(偏移: 0xC)
- `int _windingNumber`（int _windingNumber）(偏移: 0x10)
- `bool _inside`（bool _inside）(偏移: 0x14)
- `bool _sentinel`（bool _sentinel）(偏移: 0x15)
- `bool _dirty`（bool _dirty）(偏移: 0x16)
- `bool _fixUpperEdge`（bool _fix上半身Edge）(偏移: 0x17)

---

## Test（Test）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (1)

- `WeaponData wpnData`（武器数据 武器数据）(偏移: 0xC)

---

## TestPlayer（Test玩家）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (5)

- `Transform destination`（变换 destination）(偏移: 0xC)
- `Transform aim`（变换 aim）(偏移: 0x10)
- `Transform escape`（变换 escape）(偏移: 0x14)
- `Seeker seeker`（寻路器 seeker）(偏移: 0x18)
- `float nextRepathTime`（float nextRepath时间）(偏移: 0x1C)

### 方法 (3)

- `void Awake()`
  （void 唤醒（））
- `void Update()`
  （void 更新（））
- `void OnPathComplete(Path newPath)`
  （void 路径完成时（路径 newPath））

---

## Text（文本）

**继承**: MaskableGraphic, ILayoutElement（MaskableGraphic, ILayout元素）

### 字段 (7)

- `FontData m_FontData`（Font数据 m_Font数据）(偏移: 0x80)
- `string m_Text`（string m_文本）(偏移: 0x84)
- `TextGenerator m_TextCache`（文本Generator m_文本缓存）(偏移: 0x88)
- `TextGenerator m_TextCacheForLayout`（文本Generator m_文本缓存ForLayout）(偏移: 0x8C)
- `Material s_DefaultText`（材质 s_默认的文本）(偏移: 0x0)
- `bool m_DisableFontTextureRebuiltCallback`（bool m_禁用Font纹理Rebuilt回调）(偏移: 0x90)
- `UIVertex[] m_TempVerts`（界面Vertex[] m_TempVerts）(偏移: 0x94)

### 方法 (47)

- `TextGenerator get_cachedTextGenerator()`
  （文本Generator get_cached文本Generator（））
- `TextGenerator get_cachedTextGeneratorForLayout()`
  （文本Generator get_cached文本GeneratorForLayout（））
- `Texture get_mainTexture()`
  （纹理 获取_主纹理（））
- `void FontTextureChanged()`
  （void Font纹理Changed（））
- `Font get_font()`
  （Font get_font（））
- `void set_font(Font value)`
  （void set_font（Font value））
- `string get_text()`
  （字符串 获取_文本（））
- `void set_text(string value)`
  （void 设置_文本（字符串 value））
- `bool get_supportRichText()`
  （bool get_supportRich文本（））
- `void set_supportRichText(bool value)`
  （void set_supportRich文本（bool value））
- `bool get_resizeTextForBestFit()`
  （bool get_resize文本ForBestFit（））
- `void set_resizeTextForBestFit(bool value)`
  （void set_resize文本ForBestFit（bool value））
- `int get_resizeTextMinSize()`
  （int get_resize文本最小大小（））
- `void set_resizeTextMinSize(int value)`
  （void set_resize文本最小大小（int value））
- `int get_resizeTextMaxSize()`
  （int get_resize文本最大大小（））
- `void set_resizeTextMaxSize(int value)`
  （void set_resize文本最大大小（int value））
- `TextAnchor get_alignment()`
  （文本Anchor get_alignment（））
- `void set_alignment(TextAnchor value)`
  （void set_alignment（文本Anchor value））
- `bool get_alignByGeometry()`
  （bool get_alignByGeometry（））
- `void set_alignByGeometry(bool value)`
  （void set_alignByGeometry（bool value））
- `int get_fontSize()`
  （int get_font大小（））
- `void set_fontSize(int value)`
  （void set_font大小（int value））
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
- `FontStyle get_fontStyle()`
  （FontStyle get_fontStyle（））
- `void set_fontStyle(FontStyle value)`
  （void set_fontStyle（FontStyle value））
- `float get_pixelsPerUnit()`
  （float get_pixelsPerUnit（））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `void UpdateGeometry()`
  （void 更新Geometry（））
- `void AssignDefaultFont()`
  （void Assign默认的Font（））
- `TextGenerationSettings GetGenerationSettings(Vector2 extents)`
  （文本GenerationSettings 获取GenerationSettings（二维向量 extents））
- `Vector2 GetTextAnchorPivot(TextAnchor anchor)`
  （二维向量 获取文本AnchorPivot（文本Anchor anchor））
- `void OnPopulateMesh(VertexHelper toFill)`
  （void OnPopulate网格（Vertex辅助器 toFill））
- `void CalculateLayoutInputHorizontal()`
  （void 计算布局输入水平（））
- `void CalculateLayoutInputVertical()`
  （void 计算布局输入垂直（））
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

---

## TextAnchor（文本Anchor）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## TextAreaAttribute（文本AreaAttribute）

**继承**: PropertyAttribute（属性特性）

### 字段 (2)

- `int minLines`（int minLines）(偏移: 0x8)
- `int maxLines`（int maxLines）(偏移: 0xC)

---

## TextAsset（文本资产）

**继承**: Object（对象）

### 方法 (4)

- `byte[] get_bytes()`
  （byte[] get_bytes（））
- `string get_text()`
  （字符串 获取_文本（））
- `string ToString()`
  （字符串 转字符串（））
- `string DecodeString(byte[] bytes)`
  （string Decode字符串（byte[] bytes））

---

## TextAsset.EncodingUtility（文本Asset.Encoding工具）

### 字段 (1)

- `Encoding targetEncoding`（Encoding targetEncoding）(偏移: 0x4)

---

## TextEditor（文本Editor）

### 字段 (16)

- `TouchScreenKeyboard keyboardOnScreen`（触摸屏幕的键盘 keyboardOn屏幕的）(偏移: 0x8)
- `int controlID`（int controlID）(偏移: 0xC)
- `GUIStyle style`（GUIStyle style）(偏移: 0x10)
- `bool multiline`（bool multiline）(偏移: 0x14)
- `bool hasHorizontalCursorPos`（bool has水平CursorPos）(偏移: 0x15)
- `bool isPasswordField`（bool isPasswordField）(偏移: 0x16)
- `Vector2 scrollOffset`（二维向量 scrollOffset）(偏移: 0x18)
- `GUIContent m_Content`（GUIContent m_Content）(偏移: 0x20)
- `int m_CursorIndex`（int m_Cursor索引）(偏移: 0x24)
- `int m_SelectIndex`（int m_选择索引）(偏移: 0x28)
- `bool m_RevealCursor`（bool m_RevealCursor）(偏移: 0x2C)
- `bool m_MouseDragSelectsWholeWords`（bool m_鼠标DragSelectsWholeWords）(偏移: 0x2D)
- `int m_DblClickInitPos`（int m_DblClick初始化Pos）(偏移: 0x30)
- `TextEditor.DblClickSnapping m_DblClickSnap`（文本Editor.DblClickSnapping m_DblClickSnap）(偏移: 0x34)
- `bool m_bJustSelected`（bool m_bJust选中的）(偏移: 0x35)
- `int m_iAltCursorPos`（int m_iAltCursorPos）(偏移: 0x38)

---

## TextEditor.DblClickSnapping（文本Editor.DblClickSnapping）

### 字段 (1)

- `byte value__`（字节 值__）(偏移: 0x0)

---

## TextGenerationError（文本GenerationError）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## TextGenerationSettings（文本GenerationSettings）

### 字段 (18)

- `Font font`（Font font）(偏移: 0x0)
- `Color color`（颜色 color）(偏移: 0x4)
- `int fontSize`（int font大小）(偏移: 0x14)
- `float lineSpacing`（float lineSpacing）(偏移: 0x18)
- `bool richText`（bool rich文本）(偏移: 0x1C)
- `float scaleFactor`（float scale系数）(偏移: 0x20)
- `FontStyle fontStyle`（FontStyle fontStyle）(偏移: 0x24)
- `TextAnchor textAnchor`（文本Anchor textAnchor）(偏移: 0x28)
- `bool alignByGeometry`（bool alignByGeometry）(偏移: 0x2C)
- `bool resizeTextForBestFit`（bool resize文本ForBestFit）(偏移: 0x2D)
- `int resizeTextMinSize`（int resize文本最小大小）(偏移: 0x30)
- `int resizeTextMaxSize`（int resize文本最大大小）(偏移: 0x34)
- `bool updateBounds`（bool updateBounds）(偏移: 0x38)
- `VerticalWrapMode verticalOverflow`（垂直Wrap模式 verticalOverflow）(偏移: 0x3C)
- `HorizontalWrapMode horizontalOverflow`（水平Wrap模式 horizontalOverflow）(偏移: 0x40)
- `Vector2 generationExtents`（二维向量 generationExtents）(偏移: 0x44)
- `Vector2 pivot`（二维向量 pivot）(偏移: 0x4C)
- `bool generateOutOfBounds`（bool generateOutOfBounds）(偏移: 0x54)

### 方法 (3)

- `bool CompareColors(Color left, Color right)`
  （bool CompareColors（颜色 left, 颜色 right））
- `bool CompareVector2(Vector2 left, Vector2 right)`
  （bool Compare二维向量（二维向量 left, 二维向量 right））
- `bool Equals(TextGenerationSettings other)`
  （bool Equals（文本GenerationSettings other））

---

## TextGenerator（文本Generator）

**继承**: IDisposable（可释放接口）

### 字段 (11)

- `IntPtr m_Ptr`（整数指针 m_指针）(偏移: 0x8)
- `string m_LastString`（string m_最后一个字符串）(偏移: 0xC)
- `TextGenerationSettings m_LastSettings`（文本GenerationSettings m_最后一个Settings）(偏移: 0x10)
- `bool m_HasGenerated`（bool m_是否有Generated）(偏移: 0x68)
- `TextGenerationError m_LastValid`（文本GenerationError m_最后一个Valid）(偏移: 0x6C)
- `List<UIVertex> m_Verts`（List<UIVertex> m_Verts）(偏移: 0x70)
- `List<UICharInfo> m_Characters`（List<UICharInfo> m_Characters）(偏移: 0x74)
- `List<UILineInfo> m_Lines`（List<UILineInfo> m_Lines）(偏移: 0x78)
- `bool m_CachedVerts`（bool m_CachedVerts）(偏移: 0x7C)
- `bool m_CachedCharacters`（bool m_CachedCharacters）(偏移: 0x7D)
- `bool m_CachedLines`（bool m_CachedLines）(偏移: 0x7E)

### 方法 (28)

- `void Finalize()`
  （void 终结（））
- `int get_characterCountVisible()`
  （int get_character数量可见的（））
- `TextGenerationSettings ValidatedSettings(TextGenerationSettings settings)`
  （文本GenerationSettings ValidatedSettings（文本GenerationSettings settings））
- `void Invalidate()`
  （void Invalidate（））
- `void GetCharacters(List<UICharInfo> characters)`
  （void 获取Characters（List<UICharInfo> characters））
- `void GetLines(List<UILineInfo> lines)`
  （void 获取Lines（List<UILineInfo> lines））
- `void GetVertices(List<UIVertex> vertices)`
  （void 获取Vertices（List<UIVertex> vertices））
- `float GetPreferredWidth(string str, TextGenerationSettings settings)`
  （float 获取Preferred宽度（string str, 文本GenerationSettings settings））
- `float GetPreferredHeight(string str, TextGenerationSettings settings)`
  （float 获取Preferred高度（string str, 文本GenerationSettings settings））
- `bool PopulateWithErrors(string str, TextGenerationSettings settings, GameObject context)`
  （bool PopulateWithErrors（string str, 文本GenerationSettings settings, 游戏对象 context））
- `bool Populate(string str, TextGenerationSettings settings)`
  （bool Populate（string str, 文本GenerationSettings settings））
- `TextGenerationError PopulateWithError(string str, TextGenerationSettings settings)`
  （文本GenerationError PopulateWithError（string str, 文本GenerationSettings settings））
- `TextGenerationError PopulateAlways(string str, TextGenerationSettings settings)`
  （文本GenerationError PopulateAlways（string str, 文本GenerationSettings settings））
- `IList<UIVertex> get_verts()`
  （IList<UIVertex> get_verts（））
- `IList<UICharInfo> get_characters()`
  （IList<UICharInfo> get_characters（））
- `IList<UILineInfo> get_lines()`
  （IList<UILineInfo> get_lines（））
- `Rect get_rectExtents()`
  （Rect get_rectExtents（））
- `int get_characterCount()`
  （int get_character数量（））
- `int get_lineCount()`
  （int get_line数量（））
- `IntPtr Internal_Create()`
  （整数Ptr Internal_创建（））
- `void Internal_Destroy(IntPtr ptr)`
  （void 内部_销毁（整数指针 ptr））
- `bool Populate_Internal(string str, Font font, Color color, int fontSize, float scaleFactor, float lineSpacing, FontStyle style, bool richText, bool resizeTextForBestFit, int resizeTextMinSize, int resizeTextMaxSize, int verticalOverFlow, int horizontalOverflow, bool updateBounds, TextAnchor anchor, float extentsX, float extentsY, float pivotX, float pivotY, bool generateOutOfBounds, bool alignByGeometry, out uint error)`
  （bool Populate_内部的（string str, Font font, 颜色 color, int fontSize, float scaleFactor, float lineSpacing, FontStyle style, bool richText, bool resizeTextForBestFit, int resizeTextMinSize, int resizeTextMaxSize, int verticalOverFlow, int horizontalOverflow, bool updateBounds, 文本Anchor anchor, float extentsX, float extentsY, float pivotX, float pivotY, bool generateOutOfBounds, bool alignByGeometry, out uint error））
- `bool Populate_Internal(string str, Font font, Color color, int fontSize, float scaleFactor, float lineSpacing, FontStyle style, bool richText, bool resizeTextForBestFit, int resizeTextMinSize, int resizeTextMaxSize, VerticalWrapMode verticalOverFlow, HorizontalWrapMode horizontalOverflow, bool updateBounds, TextAnchor anchor, Vector2 extents, Vector2 pivot, bool generateOutOfBounds, bool alignByGeometry, out TextGenerationError error)`
  （bool Populate_内部的（string str, Font font, 颜色 color, int fontSize, float scaleFactor, float lineSpacing, FontStyle style, bool richText, bool resizeTextForBestFit, int resizeTextMinSize, int resizeTextMaxSize, 垂直Wrap模式 verticalOverFlow, 水平Wrap模式 horizontalOverflow, bool updateBounds, 文本Anchor anchor, 二维向量 extents, 二维向量 pivot, bool generateOutOfBounds, bool alignByGeometry, out TextGenerationError error））
- `void GetVerticesInternal(object vertices)`
  （void 获取Vertices内部的（object vertices））
- `void GetCharactersInternal(object characters)`
  （void 获取Characters内部的（object characters））
- `void GetLinesInternal(object lines)`
  （void 获取Lines内部的（object lines））
- `void get_rectExtents_Injected(out Rect ret)`
  （void get_rectExtents_Injected（out Rect ret））
- `bool Populate_Internal_Injected(string str, Font font, ref Color color, int fontSize, float scaleFactor, float lineSpacing, FontStyle style, bool richText, bool resizeTextForBestFit, int resizeTextMinSize, int resizeTextMaxSize, int verticalOverFlow, int horizontalOverflow, bool updateBounds, TextAnchor anchor, float extentsX, float extentsY, float pivotX, float pivotY, bool generateOutOfBounds, bool alignByGeometry, out uint error)`
  （bool Populate_Internal_Injected（string str, Font font, ref Color color, int fontSize, float scaleFactor, float lineSpacing, FontStyle style, bool richText, bool resizeTextForBestFit, int resizeTextMinSize, int resizeTextMaxSize, int verticalOverFlow, int horizontalOverflow, bool updateBounds, 文本Anchor anchor, float extentsX, float extentsY, float pivotX, float pivotY, bool generateOutOfBounds, bool alignByGeometry, out uint error））

---

## TextInfo（文本信息）

**继承**: ICloneable, IDeserializationCallback（ICloneable, IDeserialization回调）

### 字段 (11)

- `string m_listSeparator`（string m_listSeparator）(偏移: 0x8)
- `bool m_isReadOnly`（布尔值 m_是否只读）(偏移: 0xC)
- `string m_cultureName`（string m_culture名称）(偏移: 0x10)
- `CultureData m_cultureData`（Culture数据 m_culture数据）(偏移: 0x14)
- `string m_textInfoName`（string m_text信息名称）(偏移: 0x18)
- `Nullable<bool> m_IsAsciiCasingSameAsInvariant`（Nullable<bool> m_是否AsciiCasingSameAsInvariant）(偏移: 0x1C)
- `TextInfo s_Invariant`（文本信息 s_Invariant）(偏移: 0x0)
- `string customCultureName`（string customCulture名称）(偏移: 0x20)
- `int m_nDataItem`（int m_n数据项目）(偏移: 0x24)
- `bool m_useUserOverride`（bool m_useUser重写）(偏移: 0x28)
- `int m_win32LangID`（int m_win32LangID）(偏移: 0x2C)

### 方法 (33)

- `TextInfo get_Invariant()`
  （文本信息 get_Invariant（））
- `void OnDeserializing(StreamingContext ctx)`
  （void 反序列化中（流上下文 ctx））
- `void OnDeserialized()`
  （void OnDeserialized（））
- `void OnDeserialized(StreamingContext ctx)`
  （void 反序列化后（流上下文 ctx））
- `void OnSerializing(StreamingContext ctx)`
  （void 序列化中（流上下文 ctx））
- `int GetHashCodeOrdinalIgnoreCase(string s)`
  （int 获取HashCodeOrdinalIgnoreCase（string s））
- `int GetHashCodeOrdinalIgnoreCase(string s, bool forceRandomizedHashing, long additionalEntropy)`
  （int 获取HashCodeOrdinalIgnoreCase（string s, bool forceRandomizedHashing, long additionalEntropy））
- `int CompareOrdinalIgnoreCase(string str1, string str2)`
  （int CompareOrdinalIgnoreCase（string str1, string str2））
- `int CompareOrdinalIgnoreCaseEx(string strA, int indexA, string strB, int indexB, int lengthA, int lengthB)`
  （int CompareOrdinalIgnoreCaseEx（string strA, int indexA, string strB, int indexB, int lengthA, int lengthB））
- `int IndexOfStringOrdinalIgnoreCase(string source, string value, int startIndex, int count)`
  （int 索引Of字符串OrdinalIgnoreCase（string source, string value, int startIndex, int count））
- `int LastIndexOfStringOrdinalIgnoreCase(string source, string value, int startIndex, int count)`
  （int 最后一个索引Of字符串OrdinalIgnoreCase（string source, string value, int startIndex, int count））
- `string get_CultureName()`
  （string get_Culture名称（））
- `object Clone()`
  （对象 克隆（））
- `void SetReadOnlyState(bool readOnly)`
  （void 集合ReadOnly状态（bool readOnly））
- `char ToLower(char c)`
  （char To下半身（char c））
- `string ToLower(string str)`
  （string To下半身（string str））
- `char ToLowerAsciiInvariant(char c)`
  （char To下半身AsciiInvariant（char c））
- `char ToUpper(char c)`
  （char To上半身（char c））
- `string ToUpper(string str)`
  （string To上半身（string str））
- `char ToUpperAsciiInvariant(char c)`
  （char To上半身AsciiInvariant（char c））
- `bool IsAscii(char c)`
  （bool 是否Ascii（char c））
- `bool get_IsAsciiCasingSameAsInvariant()`
  （bool get_是否AsciiCasingSameAsInvariant（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `string ToString()`
  （字符串 转字符串（））
- `int GetCaseInsensitiveHashCode(string str)`
  （int 获取CaseInsensitiveHashCode（string str））
- `int GetCaseInsensitiveHashCode(string str, bool forceRandomizedHashing, long additionalEntropy)`
  （int 获取CaseInsensitiveHashCode（string str, bool forceRandomizedHashing, long additionalEntropy））
- `int GetInvariantCaseInsensitiveHashCode(string str)`
  （int 获取InvariantCaseInsensitiveHashCode（string str））
- `string ToUpperInternal(string str)`
  （string To上半身内部的（string str））
- `string ToLowerInternal(string str)`
  （string To下半身内部的（string str））
- `char ToUpperInternal(char c)`
  （char To上半身内部的（char c））
- `char ToLowerInternal(char c)`
  （char To下半身内部的（char c））
- `int InternalCompareStringOrdinalIgnoreCase(string strA, int indexA, string strB, int indexB, int lenA, int lenB)`
  （int 内部的Compare字符串OrdinalIgnoreCase（string strA, int indexA, string strB, int indexB, int lenA, int lenB））

---

## TextInfoToLowerData（文本信息To下半身数据）

### 字段 (9)

- `char[] range_00c0_0556`（char[] range_00c0_0556）(偏移: 0x0)
- `char[] range_10a0_10c5`（char[] range_10a0_10c5）(偏移: 0x4)
- `char[] range_1e00_1ffc`（char[] range_1e00_1ffc）(偏移: 0x8)
- `char[] range_2160_216f`（char[] range_2160_216f）(偏移: 0xC)
- `char[] range_24b6_24cf`（char[] range_24b6_24cf）(偏移: 0x10)
- `char[] range_2c00_2c2e`（char[] range_2c00_2c2e）(偏移: 0x14)
- `char[] range_2c60_2ce2`（char[] range_2c60_2ce2）(偏移: 0x18)
- `char[] range_a640_a696`（char[] range_a640_a696）(偏移: 0x1C)
- `char[] range_a722_a78b`（char[] range_a722_a78b）(偏移: 0x20)

---

## TextInfoToUpperData（文本信息To上半身数据）

### 字段 (8)

- `char[] range_00e0_0586`（char[] range_00e0_0586）(偏移: 0x0)
- `char[] range_1e01_1ff3`（char[] range_1e01_1ff3）(偏移: 0x4)
- `char[] range_2170_2184`（char[] range_2170_2184）(偏移: 0x8)
- `char[] range_24d0_24e9`（char[] range_24d0_24e9）(偏移: 0xC)
- `char[] range_2c30_2ce3`（char[] range_2c30_2ce3）(偏移: 0x10)
- `char[] range_2d00_2d25`（char[] range_2d00_2d25）(偏移: 0x14)
- `char[] range_a641_a697`（char[] range_a641_a697）(偏移: 0x18)
- `char[] range_a723_a78c`（char[] range_a723_a78c）(偏移: 0x1C)

---

## TextReader（文本读取器）

**继承**: MarshalByRefObject, IDisposable（MarshalByRef对象, 可释放接口）

### 字段 (1)

- `TextReader Null`（文本读取器 Null）(偏移: 0x8)

### 方法 (9)

- `void Close()`
  （void 关闭（））
- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `int Peek()`
  （整数 查看（））
- `int Read()`
  （整数 读取（））
- `int Read([In] [Out] char[] buffer, int index, int count)`
  （int Read（[In] [Out] char[] buffer, int index, int count））
- `string ReadToEnd()`
  （字符串 读取到结束（））
- `string ReadLine()`
  （字符串 读取行（））
- `TextReader Synchronized(TextReader reader)`
  （文本读取器 Synchronized（文本读取器 reader））

---

## TextReader.NullTextReader（文本Reader.Null文本读取器）

**继承**: TextReader（文本读取器）

### 方法 (2)

- `int Read(char[] buffer, int index, int count)`
  （int Read（char[] buffer, int index, int count））
- `string ReadLine()`
  （字符串 读取行（））

---

## TextReader.SyncTextReader（文本Reader.同步文本读取器）

**继承**: TextReader（文本读取器）

### 字段 (1)

- `TextReader _in`（文本读取器 _in）(偏移: 0xC)

### 方法 (7)

- `void Close()`
  （void 关闭（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `int Peek()`
  （整数 查看（））
- `int Read()`
  （整数 读取（））
- `int Read([In] [Out] char[] buffer, int index, int count)`
  （int Read（[In] [Out] char[] buffer, int index, int count））
- `string ReadLine()`
  （字符串 读取行（））
- `string ReadToEnd()`
  （字符串 读取到结束（））

---

## TextWriter（文本写入器）

**继承**: MarshalByRefObject, IDisposable（MarshalByRef对象, 可释放接口）

### 字段 (10)

- `TextWriter Null`（文本写入器 Null）(偏移: 0x0)
- `Action<object> _WriteCharDelegate`（Action<object> _WriteChar委托）(偏移: 0x4)
- `Action<object> _WriteStringDelegate`（Action<object> _Write字符串委托）(偏移: 0x8)
- `Action<object> _WriteCharArrayRangeDelegate`（Action<object> _WriteChar数组范围委托）(偏移: 0xC)
- `Action<object> _WriteLineCharDelegate`（Action<object> _WriteLineChar委托）(偏移: 0x10)
- `Action<object> _WriteLineStringDelegate`（Action<object> _WriteLine字符串委托）(偏移: 0x14)
- `Action<object> _WriteLineCharArrayRangeDelegate`（Action<object> _WriteLineChar数组范围委托）(偏移: 0x18)
- `Action<object> _FlushDelegate`（Action<object> _Flush委托）(偏移: 0x1C)
- `char[] CoreNewLine`（char[] Core新的Line）(偏移: 0xC)
- `IFormatProvider InternalFormatProvider`（I格式化提供者 内部的格式化提供者）(偏移: 0x10)

### 方法 (18)

- `string get_InitialNewLine()`
  （string get_Initial新的Line（））
- `IFormatProvider get_FormatProvider()`
  （I格式化提供者 get_格式化提供者（））
- `void Close()`
  （void 关闭（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `void Dispose()`
  （void 释放（））
- `void Flush()`
  （void 刷新（））
- `TextWriter Synchronized(TextWriter writer)`
  （文本写入器 Synchronized（文本写入器 writer））
- `void Write(char value)`
  （void 写入（字符 value））
- `void Write(char[] buffer)`
  （void Write（char[] buffer））
- `void Write(char[] buffer, int index, int count)`
  （void 写入（字符[] buffer, 整数 index, 整数 count））
- `void Write(string value)`
  （void 写入（字符串 value））
- `void WriteLine()`
  （void WriteLine（））
- `void WriteLine(char value)`
  （void WriteLine（char value））
- `void WriteLine(char[] buffer, int index, int count)`
  （void WriteLine（char[] buffer, int index, int count））
- `void WriteLine(string value)`
  （void 写入行（字符串 value））
- `void WriteLine(string format, object arg0)`
  （void WriteLine（string format, object arg0））
- `void WriteLine(string format, object arg0, object arg1)`
  （void WriteLine（string format, object arg0, object arg1））
- `void WriteLine(string format, object[] arg)`
  （void WriteLine（string format, object[] arg））

---

## TextWriter.NullTextWriter（文本Writer.Null文本写入器）

**继承**: TextWriter（文本写入器）

### 方法 (4)

- `void Write(char[] buffer, int index, int count)`
  （void 写入（字符[] buffer, 整数 index, 整数 count））
- `void Write(string value)`
  （void 写入（字符串 value））
- `void WriteLine()`
  （void WriteLine（））
- `void WriteLine(string value)`
  （void 写入行（字符串 value））

---

## TextWriter.SyncTextWriter（文本Writer.同步文本写入器）

**继承**: TextWriter, IDisposable（文本写入器, IDisposable）

### 字段 (1)

- `TextWriter _out`（文本写入器 _out）(偏移: 0x14)

### 方法 (15)

- `IFormatProvider get_FormatProvider()`
  （I格式化提供者 get_格式化提供者（））
- `void Close()`
  （void 关闭（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `void Flush()`
  （void 刷新（））
- `void Write(char value)`
  （void 写入（字符 value））
- `void Write(char[] buffer)`
  （void Write（char[] buffer））
- `void Write(char[] buffer, int index, int count)`
  （void 写入（字符[] buffer, 整数 index, 整数 count））
- `void Write(string value)`
  （void 写入（字符串 value））
- `void WriteLine()`
  （void WriteLine（））
- `void WriteLine(char value)`
  （void WriteLine（char value））
- `void WriteLine(char[] buffer, int index, int count)`
  （void WriteLine（char[] buffer, int index, int count））
- `void WriteLine(string value)`
  （void 写入行（字符串 value））
- `void WriteLine(string format, object arg0)`
  （void WriteLine（string format, object arg0））
- `void WriteLine(string format, object arg0, object arg1)`
  （void WriteLine（string format, object arg0, object arg1））
- `void WriteLine(string format, object[] arg)`
  （void WriteLine（string format, object[] arg））

---

## Texture（纹理）

**继承**: Object（对象）

### 字段 (1)

- `int GenerateAllMips`（int Generate所有Mips）(偏移: 0x0)

### 方法 (21)

- `GraphicsFormat get_graphicsFormat()`
  （Graphics格式化 get_graphics格式化（））
- `int GetScriptWidth()`
  （int 获取Script宽度（））
- `int GetScriptHeight()`
  （int 获取Script高度（））
- `TextureDimension GetDimension()`
  （纹理Dimension 获取Dimension（））
- `int get_width()`
  （整数 获取_宽度（））
- `void set_width(int value)`
  （void 设置_宽度（整数 value））
- `int get_height()`
  （整数 获取_高度（））
- `void set_height(int value)`
  （void 设置_高度（整数 value））
- `TextureDimension get_dimension()`
  （纹理Dimension get_dimension（））
- `void set_dimension(TextureDimension value)`
  （void set_dimension（纹理Dimension value））
- `bool get_isReadable()`
  （布尔值 获取_是否可读（））
- `TextureWrapMode get_wrapMode()`
  （纹理Wrap模式 get_wrap模式（））
- `void set_wrapMode(TextureWrapMode value)`
  （void set_wrap模式（纹理Wrap模式 value））
- `void set_filterMode(FilterMode value)`
  （void set_filter模式（Filter模式 value））
- `void set_anisoLevel(int value)`
  （void set_aniso等级（int value））
- `void set_mipMapBias(float value)`
  （void set_mip映射Bias（float value））
- `Vector2 get_texelSize()`
  （二维向量 get_texel大小（））
- `bool ValidateFormat(TextureFormat format)`
  （bool 验证格式化（纹理格式化 format））
- `bool ValidateFormat(GraphicsFormat format, FormatUsage usage)`
  （bool 验证格式化（Graphics格式化 format, 格式化Usage usage））
- `UnityException CreateNonReadableException(Texture t)`
  （Unity引擎Exception 创建NonReadableException（纹理 t））
- `void get_texelSize_Injected(out Vector2 ret)`
  （void get_texelSize_Injected（out Vector2 ret））

---

## Texture2D（Texture2D）

**继承**: Texture（纹理）

### 方法 (29)

- `TextureFormat get_format()`
  （纹理格式化 get_format（））
- `Texture2D get_whiteTexture()`
  （Texture2D get_white纹理（））
- `Texture2D get_blackTexture()`
  （Texture2D get_black纹理（））
- `bool Internal_CreateImpl(Texture2D mono, int w, int h, int mipCount, GraphicsFormat format, TextureCreationFlags flags, IntPtr nativeTex)`
  （bool Internal_创建Impl（Texture2D mono, int w, int h, int mipCount, Graphics格式化 format, 纹理CreationFlags flags, 整数Ptr nativeTex））
- `void Internal_Create(Texture2D mono, int w, int h, int mipCount, GraphicsFormat format, TextureCreationFlags flags, IntPtr nativeTex)`
  （void Internal_创建（Texture2D mono, int w, int h, int mipCount, Graphics格式化 format, 纹理CreationFlags flags, 整数Ptr nativeTex））
- `bool get_isReadable()`
  （布尔值 获取_是否可读（））
- `void ApplyImpl(bool updateMipmaps, bool makeNoLongerReadable)`
  （void 应用实现（布尔值 更新Mipmaps, 布尔值 使不再可读））
- `void SetPixelImpl(int image, int x, int y, Color color)`
  （void 集合PixelImpl（int image, int x, int y, 颜色 color））
- `Color GetPixelImpl(int image, int x, int y)`
  （颜色 获取PixelImpl（int image, int x, int y））
- `Color GetPixelBilinearImpl(int image, float u, float v)`
  （颜色 获取PixelBilinearImpl（int image, float u, float v））
- `void ReadPixelsImpl(Rect source, int destX, int destY, bool recalculateMipMaps)`
  （void ReadPixelsImpl（Rect source, int destX, int destY, bool recalculateMipMaps））
- `void SetPixelsImpl(int x, int y, int w, int h, Color[] pixel, int miplevel, int frame)`
  （void 集合PixelsImpl（int x, int y, int w, int h, Color[] pixel, int miplevel, int frame））
- `byte[] GetRawTextureData()`
  （byte[] 获取Raw纹理数据（））
- `Color32[] GetPixels32(int miplevel)`
  （Color32[] 获取Pixels32（int miplevel））
- `Color32[] GetPixels32()`
  （Color32[] 获取Pixels32（））
- `void SetPixel(int x, int y, Color color)`
  （void 集合Pixel（int x, int y, 颜色 color））
- `void SetPixels(int x, int y, int blockWidth, int blockHeight, Color[] colors, int miplevel)`
  （void 集合Pixels（int x, int y, int blockWidth, int blockHeight, Color[] colors, int miplevel））
- `void SetPixels(Color[] colors, int miplevel)`
  （void 集合Pixels（Color[] colors, int miplevel））
- `void SetPixels(Color[] colors)`
  （void 集合Pixels（Color[] colors））
- `Color GetPixel(int x, int y)`
  （颜色 获取Pixel（int x, int y））
- `Color GetPixelBilinear(float u, float v)`
  （颜色 获取PixelBilinear（float u, float v））
- `void Apply(bool updateMipmaps, bool makeNoLongerReadable)`
  （void 应用（布尔值 更新Mipmaps, 布尔值 使不再可读））
- `void Apply()`
  （void 应用（））
- `void ReadPixels(Rect source, int destX, int destY, bool recalculateMipMaps)`
  （void ReadPixels（Rect source, int destX, int destY, bool recalculateMipMaps））
- `void ReadPixels(Rect source, int destX, int destY)`
  （void ReadPixels（Rect source, int destX, int destY））
- `void SetPixelImpl_Injected(int image, int x, int y, ref Color color)`
  （void 集合PixelImpl_Injected（int image, int x, int y, ref Color color））
- `void GetPixelImpl_Injected(int image, int x, int y, out Color ret)`
  （void 获取PixelImpl_Injected（int image, int x, int y, out Color ret））
- `void GetPixelBilinearImpl_Injected(int image, float u, float v, out Color ret)`
  （void 获取PixelBilinearImpl_Injected（int image, float u, float v, out Color ret））
- `void ReadPixelsImpl_Injected(ref Rect source, int destX, int destY, bool recalculateMipMaps)`
  （void ReadPixelsImpl_Injected（ref Rect source, int destX, int destY, bool recalculateMipMaps））

---

## Texture2DArray（Texture2D数组）

**继承**: Texture（纹理）

### 方法 (5)

- `int get_allSlices()`
  （int get_allSlices（））
- `bool get_isReadable()`
  （布尔值 获取_是否可读（））
- `bool Internal_CreateImpl(Texture2DArray mono, int w, int h, int d, int mipCount, GraphicsFormat format, TextureCreationFlags flags)`
  （bool Internal_创建Impl（Texture2D数组 mono, int w, int h, int d, int mipCount, Graphics格式化 format, 纹理CreationFlags flags））
- `void Internal_Create(Texture2DArray mono, int w, int h, int d, int mipCount, GraphicsFormat format, TextureCreationFlags flags)`
  （void Internal_创建（Texture2D数组 mono, int w, int h, int d, int mipCount, Graphics格式化 format, 纹理CreationFlags flags））
- `void ValidateIsNotCrunched(TextureCreationFlags flags)`
  （void 验证是否NotCrunched（纹理CreationFlags flags））

---

## Texture3D（Texture3D）

**继承**: Texture（纹理）

### 方法 (12)

- `bool get_isReadable()`
  （布尔值 获取_是否可读（））
- `void SetPixelImpl(int image, int x, int y, int z, Color color)`
  （void 集合PixelImpl（int image, int x, int y, int z, 颜色 color））
- `bool Internal_CreateImpl(Texture3D mono, int w, int h, int d, int mipCount, GraphicsFormat format, TextureCreationFlags flags, IntPtr nativeTex)`
  （bool Internal_创建Impl（Texture3D mono, int w, int h, int d, int mipCount, Graphics格式化 format, 纹理CreationFlags flags, 整数Ptr nativeTex））
- `void Internal_Create(Texture3D mono, int w, int h, int d, int mipCount, GraphicsFormat format, TextureCreationFlags flags, IntPtr nativeTex)`
  （void Internal_创建（Texture3D mono, int w, int h, int d, int mipCount, Graphics格式化 format, 纹理CreationFlags flags, 整数Ptr nativeTex））
- `void ApplyImpl(bool updateMipmaps, bool makeNoLongerReadable)`
  （void 应用实现（布尔值 更新Mipmaps, 布尔值 使不再可读））
- `void SetPixels(Color[] colors, int miplevel)`
  （void 集合Pixels（Color[] colors, int miplevel））
- `void Apply(bool updateMipmaps, bool makeNoLongerReadable)`
  （void 应用（布尔值 更新Mipmaps, 布尔值 使不再可读））
- `void Apply(bool updateMipmaps)`
  （void 应用（bool updateMipmaps））
- `void Apply()`
  （void 应用（））
- `void SetPixel(int x, int y, int z, Color color, int mipLevel)`
  （void 集合Pixel（int x, int y, int z, 颜色 color, int mipLevel））
- `void ValidateIsNotCrunched(TextureCreationFlags flags)`
  （void 验证是否NotCrunched（纹理CreationFlags flags））
- `void SetPixelImpl_Injected(int image, int x, int y, int z, ref Color color)`
  （void 集合PixelImpl_Injected（int image, int x, int y, int z, ref Color color））

---

## TextureAnimation（纹理动画）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (4)

- `Texture[] textures`（Texture[] textures）(偏移: 0xC)
- `Material thisMaterial`（材质 this材质）(偏移: 0x10)
- `int index`（整数 索引）(偏移: 0x14)
- `float interval`（浮点数 间隔）(偏移: 0x18)

### 方法 (3)

- `void Awake()`
  （void 唤醒（））
- `void Start()`
  （void 开始（））
- `IEnumerator Animation()`
  （IEnumerator 动画（））

---

## TextureCreationFlags（纹理CreationFlags）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## TextureCurve（纹理Curve）

**继承**: IDisposable（可释放接口）

### 字段 (8)

- `bool m_Loop`（bool m_Loop）(偏移: 0xC)
- `float m_ZeroValue`（float m_Zero值）(偏移: 0x10)
- `float m_Range`（float m_范围）(偏移: 0x14)
- `AnimationCurve m_Curve`（动画Curve m_Curve）(偏移: 0x18)
- `AnimationCurve m_LoopingCurve`（动画Curve m_LoopingCurve）(偏移: 0x1C)
- `Texture2D m_Texture`（Texture2D m_纹理）(偏移: 0x20)
- `bool m_IsCurveDirty`（bool m_是否CurveDirty）(偏移: 0x24)
- `bool m_IsTextureDirty`（bool m_是否纹理Dirty）(偏移: 0x25)

### 方法 (14)

- `int get_length()`
  （int get_length（））
- `void set_length(int value)`
  （void set_length（int value））
- `Keyframe get_Item(int index)`
  （Keyframe get_项目（int index））
- `void Finalize()`
  （void 终结（））
- `void Dispose()`
  （void 释放（））
- `void Release()`
  （void 释放（））
- `void SetDirty()`
  （void 设置_脏（））
- `TextureFormat GetTextureFormat()`
  （纹理格式化 获取纹理格式化（））
- `Texture2D GetTexture()`
  （Texture2D 获取纹理（））
- `float Evaluate(float time)`
  （float Evaluate（float time））
- `int AddKey(float time, float value)`
  （int 添加键（float time, float value））
- `int MoveKey(int index, in Keyframe key)`
  （int 移动键（int index, in Keyframe key））
- `void RemoveKey(int index)`
  （void 移除键（int index））
- `void SmoothTangents(int index, float weight)`
  （void SmoothTangents（int index, float weight））

---

## TextureCurveParameter（纹理CurveParameter）

**继承**: VolumeParameter<TextureCurve>（VolumeParameter<纹理Curve>）

### 方法 (1)

- `void Release()`
  （void 释放（））

---

## TextureDesc（纹理Desc）

### 字段 (27)

- `TextureSizeMode sizeMode`（纹理大小模式 size模式）(偏移: 0x0)
- `int width`（整数 宽度）(偏移: 0x4)
- `int height`（int height）(偏移: 0x8)
- `int slices`（int slices）(偏移: 0xC)
- `Vector2 scale`（二维向量 scale）(偏移: 0x10)
- `ScaleFunc func`（缩放Func func）(偏移: 0x18)
- `DepthBits depthBufferBits`（深度Bits depth缓冲区Bits）(偏移: 0x1C)
- `GraphicsFormat colorFormat`（Graphics格式化 color格式化）(偏移: 0x20)
- `FilterMode filterMode`（Filter模式 filter模式）(偏移: 0x24)
- `TextureWrapMode wrapMode`（纹理Wrap模式 wrap模式）(偏移: 0x28)
- `TextureDimension dimension`（纹理Dimension dimension）(偏移: 0x2C)
- `bool enableRandomWrite`（bool enable随机Write）(偏移: 0x30)
- `bool useMipMap`（bool useMip映射）(偏移: 0x0)
- `bool autoGenerateMips`（bool autoGenerateMips）(偏移: 0x0)
- `bool isShadowMap`（bool isShadow映射）(偏移: 0x0)
- `int anisoLevel`（int aniso等级）(偏移: 0x0)
- `float mipMapBias`（float mip映射Bias）(偏移: 0x38)
- `bool enableMSAA`（bool enableMSAA）(偏移: 0x3C)
- `MSAASamples msaaSamples`（MSAASamples msaaSamples）(偏移: 0x40)
- `bool bindTextureMS`（bool bind纹理MS）(偏移: 0x44)
- `bool useDynamicScale`（bool use动态的缩放）(偏移: 0x45)
- `RenderTextureMemoryless memoryless`（Render纹理Memoryless memoryless）(偏移: 0x48)
- `string name`（字符串 名称）(偏移: 0x4C)
- `FastMemoryDesc fastMemoryDesc`（FastMemoryDesc fastMemoryDesc）(偏移: 0x50)
- `bool fallBackToBlackTexture`（bool fall后ToBlack纹理）(偏移: 0x5C)
- `bool clearBuffer`（bool clear缓冲区）(偏移: 0x5D)
- `Color clearColor`（颜色 clear颜色）(偏移: 0x60)

### 方法 (2)

- `void InitDefaultValues(bool dynamicResolution, bool xrReady)`
  （void 初始化默认的Values（bool dynamicResolution, bool xrReady））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## TextureDimension（纹理Dimension）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## TextureFormat（纹理格式化）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## TextureHandle（纹理句柄）

### 字段 (2)

- `TextureHandle s_NullHandle`（纹理句柄 s_Null句柄）(偏移: 0x0)
- `ResourceHandle handle`（资源句柄 handle）(偏移: 0x0)

### 方法 (5)

- `TextureHandle get_nullHandle()`
  （纹理句柄 get_null句柄（））
- `RTHandle op_Implicit(TextureHandle texture)`
  （RT句柄 op_Implicit（纹理句柄 texture））
- `RenderTargetIdentifier op_Implicit(TextureHandle texture)`
  （Render目标Identifier op_Implicit（纹理句柄 texture））
- `RenderTexture op_Implicit(TextureHandle texture)`
  （Render纹理 op_Implicit（纹理句柄 texture））
- `bool IsValid()`
  （布尔值 是否有效（））

---

## TextureMixerPlayable（纹理MixerPlayable）

**继承**: IPlayable, IEquatable<TextureMixerPlayable>（IPlayable, IEquatable<纹理MixerPlayable>）

### 字段 (1)

- `PlayableHandle m_Handle`（可播放句柄 m_句柄）(偏移: 0x0)

### 方法 (2)

- `PlayableHandle GetHandle()`
  （可播放句柄 获取句柄（））
- `bool Equals(TextureMixerPlayable other)`
  （bool Equals（纹理MixerPlayable other））

---

## TexturePlayableOutput（纹理PlayableOutput）

**继承**: IPlayableOutput（I可播放输出）

### 字段 (1)

- `PlayableOutputHandle m_Handle`（可播放输出句柄 m_句柄）(偏移: 0x0)

### 方法 (1)

- `PlayableOutputHandle GetHandle()`
  （可播放输出句柄 获取句柄（））

---

## TexturePool（纹理池）

**继承**: RenderGraphResourcePool<RTHandle>（RenderGraph资源Pool<RTHandle>）

### 方法 (5)

- `void ReleaseInternalResource(RTHandle res)`
  （void Release内部的资源（RT句柄 res））
- `string GetResourceName(RTHandle res)`
  （string 获取资源名称（RT句柄 res））
- `long GetResourceSize(RTHandle res)`
  （long 获取资源大小（RT句柄 res））
- `string GetResourceTypeName()`
  （string 获取资源类型名称（））
- `void PurgeUnusedResources(int currentFrameIndex)`
  （void PurgeUnusedResources（int currentFrameIndex））

---

## TextureSizeMode（纹理大小模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## TextureWrapMode（纹理Wrap模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## TextureXR（纹理XR）

### 字段 (22)

- `int m_MaxViews`（int m_最大Views）(偏移: 0x0)
- `Texture m_BlackUIntTexture2DArray`（纹理 m_BlackU整数Texture2D数组）(偏移: 0x4)
- `Texture m_BlackUIntTexture`（纹理 m_BlackU整数纹理）(偏移: 0x8)
- `RTHandle m_BlackUIntTexture2DArrayRTH`（RT句柄 m_BlackU整数Texture2D数组RTH）(偏移: 0xC)
- `RTHandle m_BlackUIntTextureRTH`（RT句柄 m_BlackU整数纹理RTH）(偏移: 0x10)
- `Texture2DArray m_ClearTexture2DArray`（Texture2D数组 m_清除Texture2D数组）(偏移: 0x14)
- `Texture2D m_ClearTexture`（Texture2D m_清除纹理）(偏移: 0x18)
- `RTHandle m_ClearTexture2DArrayRTH`（RT句柄 m_清除Texture2D数组RTH）(偏移: 0x1C)
- `RTHandle m_ClearTextureRTH`（RT句柄 m_清除纹理RTH）(偏移: 0x20)
- `Texture2DArray m_MagentaTexture2DArray`（Texture2D数组 m_MagentaTexture2D数组）(偏移: 0x24)
- `Texture2D m_MagentaTexture`（Texture2D m_Magenta纹理）(偏移: 0x28)
- `RTHandle m_MagentaTexture2DArrayRTH`（RT句柄 m_MagentaTexture2D数组RTH）(偏移: 0x2C)
- `RTHandle m_MagentaTextureRTH`（RT句柄 m_Magenta纹理RTH）(偏移: 0x30)
- `Texture2D m_BlackTexture`（Texture2D m_Black纹理）(偏移: 0x34)
- `Texture3D m_BlackTexture3D`（Texture3D m_BlackTexture3D）(偏移: 0x38)
- `Texture2DArray m_BlackTexture2DArray`（Texture2D数组 m_BlackTexture2D数组）(偏移: 0x3C)
- `RTHandle m_BlackTexture2DArrayRTH`（RT句柄 m_BlackTexture2D数组RTH）(偏移: 0x40)
- `RTHandle m_BlackTextureRTH`（RT句柄 m_Black纹理RTH）(偏移: 0x44)
- `RTHandle m_BlackTexture3DRTH`（RT句柄 m_BlackTexture3DRTH）(偏移: 0x48)
- `Texture2DArray m_WhiteTexture2DArray`（Texture2D数组 m_WhiteTexture2D数组）(偏移: 0x4C)
- `RTHandle m_WhiteTexture2DArrayRTH`（RT句柄 m_WhiteTexture2D数组RTH）(偏移: 0x50)
- `RTHandle m_WhiteTextureRTH`（RT句柄 m_White纹理RTH）(偏移: 0x54)

### 方法 (16)

- `void set_maxViews(int value)`
  （void set_maxViews（int value））
- `int get_slices()`
  （int get_slices（））
- `bool get_useTexArray()`
  （bool get_useTex数组（））
- `TextureDimension get_dimension()`
  （纹理Dimension get_dimension（））
- `RTHandle GetBlackUIntTexture()`
  （RT句柄 获取BlackU整数纹理（））
- `RTHandle GetClearTexture()`
  （RT句柄 获取清除纹理（））
- `RTHandle GetMagentaTexture()`
  （RT句柄 获取Magenta纹理（））
- `RTHandle GetBlackTexture()`
  （RT句柄 获取Black纹理（））
- `RTHandle GetBlackTextureArray()`
  （RT句柄 获取Black纹理数组（））
- `RTHandle GetBlackTexture3D()`
  （RT句柄 获取BlackTexture3D（））
- `RTHandle GetWhiteTexture()`
  （RT句柄 获取White纹理（））
- `void Initialize(CommandBuffer cmd, ComputeShader clearR32_UIntShader)`
  （void 初始化（Command缓冲区 cmd, Compute着色器 clearR32_UIntShader））
- `Texture2DArray CreateTexture2DArrayFromTexture2D(Texture2D source, string name)`
  （Texture2D数组 创建Texture2D数组FromTexture2D（Texture2D source, string name））
- `Texture CreateBlackUIntTextureArray(CommandBuffer cmd, ComputeShader clearR32_UIntShader)`
  （纹理 创建BlackU整数纹理数组（Command缓冲区 cmd, Compute着色器 clearR32_UIntShader））
- `Texture CreateBlackUintTexture(CommandBuffer cmd, ComputeShader clearR32_UIntShader)`
  （纹理 创建BlackUint纹理（Command缓冲区 cmd, Compute着色器 clearR32_UIntShader））
- `Texture3D CreateBlackTexture3D(string name)`
  （Texture3D 创建BlackTexture3D（string name））

---

## ThaiBuddhistCalendar（ThaiBuddhistCalendar）

**继承**: Calendar（日历）

### 字段 (2)

- `EraInfo[] thaiBuddhistEraInfo`（EraInfo[] thaiBuddhistEra信息）(偏移: 0x0)
- `GregorianCalendarHelper helper`（GregorianCalendar辅助器 helper）(偏移: 0x14)

### 方法 (16)

- `DateTime get_MinSupportedDateTime()`
  （日期时间 获取_最小支持日期时间（））
- `DateTime get_MaxSupportedDateTime()`
  （日期时间 获取_最大支持日期时间（））
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
- `int[] get_Eras()`
  （整数[] 获取_纪元（））
- `int get_TwoDigitYearMax()`
  （整数 获取_两位数年份最大（））
- `int ToFourDigitYear(int year)`
  （整数 转四位数年份（整数 year））

---

## ThermalVision（ThermalVision）

**继承**: VolumeComponent, IPostProcessComponent（体积组件, I后处理组件）

### 字段 (4)

- `FloatParameter Duration`（浮点数Parameter 持续时间）(偏移: 0x1C)
- `ColorParameter MainColor`（颜色Parameter 主要的颜色）(偏移: 0x20)
- `FloatParameter NoiseScale`（浮点数Parameter Noise缩放）(偏移: 0x24)
- `FloatParameter NoisePower`（浮点数Parameter Noise力度）(偏移: 0x28)

### 方法 (2)

- `bool IsActive()`
  （布尔值 是否激活的（））
- `bool IsTileCompatible()`
  （布尔值 是否瓦片兼容（））

---

## ThermalVisionFeature（ThermalVisionFeature）

**继承**: ScriptableRendererFeature（可脚本化渲染器特性）

### 字段 (3)

- `Shader shader`（着色器 shader）(偏移: 0x10)
- `RenderPassEvent passEvent`（RenderPass事件 pass事件）(偏移: 0x14)
- `ThermalVisionPass thermalVisionPass`（ThermalVisionPass thermalVisionPass）(偏移: 0x18)

### 方法 (2)

- `void Create()`
  （void 创建（））
- `void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)`
  （void 添加渲染通道（可脚本化渲染器 renderer, 引用 渲染数据 renderingData））

---

## ThermalVisionPass（ThermalVisionPass）

**继承**: ScriptableRenderPass（可脚本化渲染通道）

### 字段 (10)

- `string k_RenderTag`（string k_Render标签）(偏移: 0x0)
- `int MainTexID`（int 主要的TexID）(偏移: 0x4)
- `int TempID`（int TempID）(偏移: 0x8)
- `int DurationID`（int 持续时间ID）(偏移: 0xC)
- `int MainColorID`（int 主要的颜色ID）(偏移: 0x10)
- `int NoiseScaleID`（int Noise缩放ID）(偏移: 0x14)
- `int NoisePowerID`（int Noise力度ID）(偏移: 0x18)
- `ThermalVision thermalVision`（ThermalVision thermalVision）(偏移: 0x54)
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

## Thread（Thread）

**继承**: CriticalFinalizerObject, _Thread（CriticalFinalizer对象, _Thread）

### 字段 (15)

- `LocalDataStoreMgr s_LocalDataStoreMgr`（本地的数据商店Mgr s_本地的数据商店Mgr）(偏移: 0x0)
- `LocalDataStoreHolder s_LocalDataStore`（本地的数据商店Holder s_本地的数据商店）(偏移: 0x80000000)
- `CultureInfo m_CurrentCulture`（Culture信息 m_当前Culture）(偏移: 0x80000004)
- `CultureInfo m_CurrentUICulture`（Culture信息 m_当前界面Culture）(偏移: 0x80000008)
- `AsyncLocal<CultureInfo> s_asyncLocalCurrentCulture`（异步Local<CultureInfo> s_async本地的当前Culture）(偏移: 0x4)
- `AsyncLocal<CultureInfo> s_asyncLocalCurrentUICulture`（异步Local<CultureInfo> s_async本地的当前界面Culture）(偏移: 0x8)
- `InternalThread internal_thread`（内部的Thread internal_thread）(偏移: 0x8)
- `object m_ThreadStartArg`（object m_Thread开始Arg）(偏移: 0xC)
- `object pending_exception`（object pending_exception）(偏移: 0x10)
- `IPrincipal principal`（IPrincipal principal）(偏移: 0x14)
- `int principal_version`（int principal_version）(偏移: 0x18)
- `Thread current_thread`（Thread current_thread）(偏移: 0x8000000C)
- `MulticastDelegate m_Delegate`（Multicast委托 m_委托）(偏移: 0x1C)
- `ExecutionContext m_ExecutionContext`（ExecutionContext m_ExecutionContext）(偏移: 0x20)
- `bool m_ExecutionContextBelongsToOuterScope`（bool m_ExecutionContextBelongsToOuter瞄准镜）(偏移: 0x24)

### 方法 (55)

- `void Start()`
  （void 开始（））
- `void Start(object parameter)`
  （void 开始（object parameter））
- `void Start(ref StackCrawlMark stackMark)`
  （void 开始（ref StackCrawlMark stackMark））
- `ExecutionContext.Reader GetExecutionContextReader()`
  （ExecutionContext.读取器 获取ExecutionContext读取器（））
- `bool get_ExecutionContextBelongsToCurrentScope()`
  （bool get_ExecutionContextBelongsTo当前瞄准镜（））
- `void set_ExecutionContextBelongsToCurrentScope(bool value)`
  （void set_ExecutionContextBelongsTo当前瞄准镜（bool value））
- `ExecutionContext GetMutableExecutionContext()`
  （ExecutionContext 获取MutableExecutionContext（））
- `void SetExecutionContext(ExecutionContext value, bool belongsToCurrentScope)`
  （void 集合ExecutionContext（ExecutionContext value, bool belongsToCurrentScope））
- `void SetExecutionContext(ExecutionContext.Reader value, bool belongsToCurrentScope)`
  （void 集合ExecutionContext（ExecutionContext.读取器 value, bool belongsToCurrentScope））
- `void set_Priority(ThreadPriority value)`
  （void set_Priority（ThreadPriority value））
- `void SetPriorityNative(int priority)`
  （void 集合PriorityNative（int priority））
- `bool JoinInternal(int millisecondsTimeout)`
  （bool Join内部的（int millisecondsTimeout））
- `bool Join(int millisecondsTimeout)`
  （bool Join（int millisecondsTimeout））
- `void SleepInternal(int millisecondsTimeout)`
  （void Sleep内部的（int millisecondsTimeout））
- `void Sleep(int millisecondsTimeout)`
  （void Sleep（int millisecondsTimeout））
- `bool YieldInternal()`
  （bool Yield内部的（））
- `bool Yield()`
  （bool Yield（））
- `void SetStartHelper(Delegate start, int maxStackSize)`
  （void 集合开始辅助器（委托 start, int maxStackSize））
- `CultureInfo get_CurrentUICulture()`
  （Culture信息 get_当前界面Culture（））
- `CultureInfo GetCurrentUICultureNoAppX()`
  （Culture信息 获取当前界面CultureNoAppX（））
- `CultureInfo get_CurrentCulture()`
  （Culture信息 get_当前Culture（））
- `CultureInfo GetCurrentCultureNoAppX()`
  （Culture信息 获取当前CultureNoAppX（））
- `void MemoryBarrier()`
  （void MemoryBarrier（））
- `void ConstructInternalThread()`
  （void Construct内部的Thread（））
- `InternalThread get_Internal()`
  （内部的Thread get_内部的（））
- `Context get_CurrentContext()`
  （Context get_当前Context（））
- `Thread GetCurrentThread()`
  （Thread 获取当前Thread（））
- `Thread get_CurrentThread()`
  （Thread get_当前Thread（））
- `int get_CurrentThreadId()`
  （int get_当前ThreadId（））
- `int GetDomainID()`
  （int 获取DomainID（））
- `IntPtr Thread_internal(MulticastDelegate start)`
  （整数Ptr Thread_internal（Multicast委托 start））
- `void Finalize()`
  （void 终结（））
- `bool get_IsThreadPoolThread()`
  （bool get_是否Thread池Thread（））
- `bool get_IsThreadPoolThreadInternal()`
  （bool get_是否Thread池Thread内部的（））
- `bool get_IsAlive()`
  （bool get_是否Alive（））
- `void set_IsBackground(bool value)`
  （void set_是否Background（bool value））
- `void SetName_internal(InternalThread thread, string name)`
  （void 集合Name_internal（内部的Thread thread, string name））
- `void set_Name(string value)`
  （void 设置_名称（字符串 value））
- `ThreadState get_ThreadState()`
  （Thread状态 get_Thread状态（））
- `void Abort_internal(InternalThread thread, object stateInfo)`
  （void Abort_internal（内部的Thread thread, object stateInfo））
- `void Abort()`
  （void Abort（））
- `void SpinWait_nop()`
  （void SpinWait_nop（））
- `void SpinWait(int iterations)`
  （void SpinWait（int iterations））
- `void StartInternal(IPrincipal principal, ref StackCrawlMark stackMark)`
  （void 开始内部的（IPrincipal principal, ref StackCrawlMark stackMark））
- `void SetState(InternalThread thread, ThreadState set)`
  （void 集合状态（内部的Thread thread, Thread状态 set））
- `void ClrState(InternalThread thread, ThreadState clr)`
  （void Clr状态（内部的Thread thread, Thread状态 clr））
- `ThreadState GetState(InternalThread thread)`
  （Thread状态 获取状态（内部的Thread thread））
- `int SystemMaxStackStize()`
  （int 系统最大栈Stize（））
- `int GetProcessDefaultStackSize(int maxStackSize)`
  （int 获取处理默认的栈大小（int maxStackSize））
- `void SetStart(MulticastDelegate start, int maxStackSize)`
  （void 集合开始（Multicast委托 start, int maxStackSize））
- `int get_ManagedThreadId()`
  （int get_ManagedThreadId（））
- `void BeginCriticalRegion()`
  （void BeginCriticalRegion（））
- `void EndCriticalRegion()`
  （void 结束CriticalRegion（））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `ThreadState ValidateThreadState()`
  （Thread状态 验证Thread状态（））

---

## ThreadControlQueue（Thread控制队列）

### 字段 (9)

- `Path head`（路径 head）(偏移: 0x8)
- `Path tail`（路径 tail）(偏移: 0xC)
- `object lockObj`（object lockObj）(偏移: 0x10)
- `int numReceivers`（int numReceivers）(偏移: 0x14)
- `bool blocked`（bool blocked）(偏移: 0x18)
- `int blockedReceivers`（int blockedReceivers）(偏移: 0x1C)
- `bool starving`（bool starving）(偏移: 0x20)
- `bool terminate`（bool terminate）(偏移: 0x21)
- `ManualResetEvent block`（手动重置事件 block）(偏移: 0x24)

### 方法 (14)

- `bool get_IsEmpty()`
  （布尔值 获取_是否为空（））
- `bool get_IsTerminating()`
  （bool get_是否Terminating（））
- `void Block()`
  （void Block（））
- `void Unblock()`
  （void Unblock（））
- `void Lock()`
  （void Lock（））
- `void Unlock()`
  （void Unlock（））
- `bool get_AllReceiversBlocked()`
  （bool get_所有ReceiversBlocked（））
- `void PushFront(Path path)`
  （void Push前（路径 path））
- `void Push(Path path)`
  （void Push（路径 path））
- `void Starving()`
  （void Starving（））
- `void TerminateReceivers()`
  （void TerminateReceivers（））
- `Path Pop()`
  （路径 Pop（））
- `void ReceiverTerminated()`
  （void ReceiverTerminated（））
- `Path PopNoBlock(bool blockedBefore)`
  （路径 PopNoBlock（bool blockedBefore））

---

## ThreadCount（Thread数量）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ThreadHelper（Thread辅助器）

### 字段 (4)

- `Delegate _start`（委托 _start）(偏移: 0x8)
- `object _startArg`（object _startArg）(偏移: 0xC)
- `ExecutionContext _executionContext`（ExecutionContext _executionContext）(偏移: 0x10)
- `ContextCallback _ccb`（Context回调 _ccb）(偏移: 0x0)

### 方法 (4)

- `void SetExecutionContextHelper(ExecutionContext ec)`
  （void 集合ExecutionContext辅助器（ExecutionContext ec））
- `void ThreadStart_Context(object state)`
  （void ThreadStart_Context（object state））
- `void ThreadStart(object obj)`
  （void Thread开始（object obj））
- `void ThreadStart()`
  （void Thread开始（））

---

## ThreadPool（Thread池）

### 方法 (17)

- `RegisteredWaitHandle RegisterWaitForSingleObject(WaitHandle waitObject, WaitOrTimerCallback callBack, object state, uint millisecondsTimeOutInterval, bool executeOnlyOnce, ref StackCrawlMark stackMark, bool compressStack)`
  （RegisteredWait句柄 RegisterWaitFor单个对象（Wait句柄 waitObject, WaitOr计时器回调 callBack, object state, uint millisecondsTimeOutInterval, bool executeOnlyOnce, ref StackCrawlMark stackMark, bool compressStack））
- `RegisteredWaitHandle RegisterWaitForSingleObject(WaitHandle waitObject, WaitOrTimerCallback callBack, object state, TimeSpan timeout, bool executeOnlyOnce)`
  （RegisteredWait句柄 RegisterWaitFor单个对象（Wait句柄 waitObject, WaitOr计时器回调 callBack, object state, 时间Span timeout, bool executeOnlyOnce））
- `bool QueueUserWorkItem(WaitCallback callBack, object state)`
  （bool 队列UserWork项目（Wait回调 callBack, object state））
- `bool UnsafeQueueUserWorkItem(WaitCallback callBack, object state)`
  （bool Unsafe队列UserWork项目（Wait回调 callBack, object state））
- `bool QueueUserWorkItemHelper(WaitCallback callBack, object state, ref StackCrawlMark stackMark, bool compressStack)`
  （bool 队列UserWork项目辅助器（Wait回调 callBack, object state, ref StackCrawlMark stackMark, bool compressStack））
- `void UnsafeQueueCustomWorkItem(IThreadPoolWorkItem workItem, bool forceGlobal)`
  （void Unsafe队列自定义的Work项目（IThread池Work项目 workItem, bool forceGlobal））
- `bool TryPopCustomWorkItem(IThreadPoolWorkItem workItem)`
  （bool TryPop自定义的Work项目（IThread池Work项目 workItem））
- `IEnumerable<IThreadPoolWorkItem> GetQueuedWorkItems()`
  （IEnumerable<IThread池WorkItem> 获取QueuedWorkItems（））
- `IEnumerable<IThreadPoolWorkItem> EnumerateQueuedWorkItems(ThreadPoolWorkQueue.WorkStealingQueue[] wsQueues, ThreadPoolWorkQueue.QueueSegment globalQueueTail)`
  （IEnumerable<IThread池WorkItem> EnumerateQueuedWorkItems（Thread池WorkQueue.WorkStealingQueue[] wsQueues, Thread池WorkQueue.队列Segment globalQueueTail））
- `bool RequestWorkerThread()`
  （bool 请求WorkerThread（））
- `void EnsureVMInitialized()`
  （void EnsureVMInitialized（））
- `bool NotifyWorkItemComplete()`
  （bool NotifyWork项目Complete（））
- `void ReportThreadStatus(bool isWorking)`
  （void ReportThreadStatus（bool isWorking））
- `void NotifyWorkItemProgress()`
  （void NotifyWork项目Progress（））
- `void NotifyWorkItemProgressNative()`
  （void NotifyWork项目ProgressNative（））
- `bool IsThreadPoolHosted()`
  （bool 是否Thread池Hosted（））
- `void InitializeVMTp(ref bool enableWorkerTracking)`
  （void 初始化VMTp（ref bool enableWorkerTracking））

---

## ThreadPoolGlobals（Thread池Globals）

### 字段 (6)

- `uint tpQuantum`（uint tpQuantum）(偏移: 0x0)
- `int processorCount`（int processor数量）(偏移: 0x4)
- `bool tpHosted`（bool tpHosted）(偏移: 0x8)
- `bool vmTpInitialized`（bool vmTpInitialized）(偏移: 0x9)
- `bool enableWorkerTracking`（bool enableWorkerTracking）(偏移: 0xA)
- `ThreadPoolWorkQueue workQueue`（Thread池Work队列 work队列）(偏移: 0xC)

---

## ThreadPoolTaskScheduler（Thread池TaskScheduler）

**继承**: TaskScheduler（TaskScheduler）

### 字段 (1)

- `ParameterizedThreadStart s_longRunningThreadWork`（ParameterizedThread开始 s_longRunningThreadWork）(偏移: 0x0)

### 方法 (8)

- `void LongRunningThreadWork(object obj)`
  （void LongRunningThreadWork（object obj））
- `void QueueTask(Task task)`
  （void 队列Task（Task task））
- `bool TryExecuteTaskInline(Task task, bool taskWasPreviouslyQueued)`
  （bool Try执行TaskInline（Task task, bool taskWasPreviouslyQueued））
- `bool TryDequeue(Task task)`
  （bool TryDequeue（Task task））
- `IEnumerable<Task> GetScheduledTasks()`
  （IEnumerable<Task> 获取ScheduledTasks（））
- `IEnumerable<Task> FilterTasksFromWorkItems(IEnumerable<IThreadPoolWorkItem> tpwItems)`
  （IEnumerable<Task> FilterTasksFromWorkItems（IEnumerable<IThread池WorkItem> tpwItems））
- `void NotifyWorkItemProgress()`
  （void NotifyWork项目Progress（））
- `bool get_RequiresAtomicStartTransition()`
  （bool get_RequiresAtomic开始Transition（））

---

## ThreadPoolWorkQueue（Thread池Work队列）

### 字段 (4)

- `ThreadPoolWorkQueue.QueueSegment queueHead`（Thread池WorkQueue.队列Segment queue头部）(偏移: 0x8)
- `ThreadPoolWorkQueue.QueueSegment queueTail`（Thread池WorkQueue.队列Segment queueTail）(偏移: 0xC)
- `ThreadPoolWorkQueue.SparseArray<ThreadPoolWorkQueue.WorkStealingQueue> allThreadQueues`（Thread池WorkQueue.SparseArray<Thread池WorkQueue.WorkStealingQueue> allThreadQueues）(偏移: 0x0)
- `int numOutstandingThreadRequests`（int numOutstandingThreadRequests）(偏移: 0x10)

### 方法 (7)

- `ThreadPoolWorkQueueThreadLocals EnsureCurrentThreadHasQueue()`
  （Thread池Work队列ThreadLocals Ensure当前Thread是否有队列（））
- `void EnsureThreadRequested()`
  （void EnsureThreadRequested（））
- `void MarkThreadRequestSatisfied()`
  （void MarkThread请求Satisfied（））
- `void Enqueue(IThreadPoolWorkItem callback, bool forceGlobal)`
  （void Enqueue（IThread池Work项目 callback, bool forceGlobal））
- `bool LocalFindAndPop(IThreadPoolWorkItem callback)`
  （bool 本地的查找AndPop（IThread池Work项目 callback））
- `void Dequeue(ThreadPoolWorkQueueThreadLocals tl, out IThreadPoolWorkItem callback, out bool missedSteal)`
  （void Dequeue（Thread池Work队列ThreadLocals tl, out IThreadPoolWorkItem callback, out bool missedSteal））
- `bool Dispatch()`
  （bool Dispatch（））

---

## ThreadPoolWorkQueue.QueueSegment（Thread池WorkQueue.队列Segment）

### 字段 (3)

- `IThreadPoolWorkItem[] nodes`（IThread池WorkItem[] nodes）(偏移: 0x8)
- `int indexes`（int indexes）(偏移: 0xC)
- `ThreadPoolWorkQueue.QueueSegment Next`（Thread池WorkQueue.队列Segment 下一个）(偏移: 0x10)

### 方法 (5)

- `void GetIndexes(out int upper, out int lower)`
  （void 获取Indexes（out int upper, out int lower））
- `bool CompareExchangeIndexes(ref int prevUpper, int newUpper, ref int prevLower, int newLower)`
  （bool CompareExchangeIndexes（ref int prevUpper, int newUpper, ref int prevLower, int newLower））
- `bool IsUsedUp()`
  （bool 是否Used上（））
- `bool TryEnqueue(IThreadPoolWorkItem node)`
  （bool TryEnqueue（IThread池Work项目 node））
- `bool TryDequeue(out IThreadPoolWorkItem node)`
  （bool TryDequeue（out IThreadPoolWorkItem node））

---

## ThreadPoolWorkQueue.WorkStealingQueue（Thread池WorkQueue.WorkStealing队列）

### 字段 (5)

- `IThreadPoolWorkItem[] m_array`（IThread池WorkItem[] m_array）(偏移: 0x8)
- `int m_mask`（int m_mask）(偏移: 0xC)
- `int m_headIndex`（int m_head索引）(偏移: 0x10)
- `int m_tailIndex`（int m_tail索引）(偏移: 0x14)
- `SpinLock m_foreignLock`（SpinLock m_foreignLock）(偏移: 0x18)

### 方法 (5)

- `void LocalPush(IThreadPoolWorkItem obj)`
  （void 本地的Push（IThread池Work项目 obj））
- `bool LocalFindAndPop(IThreadPoolWorkItem obj)`
  （bool 本地的查找AndPop（IThread池Work项目 obj））
- `bool LocalPop(out IThreadPoolWorkItem obj)`
  （bool 本地的Pop（out IThreadPoolWorkItem obj））
- `bool TrySteal(out IThreadPoolWorkItem obj, ref bool missedSteal)`
  （bool TrySteal（out IThreadPoolWorkItem obj, ref bool missedSteal））
- `bool TrySteal(out IThreadPoolWorkItem obj, ref bool missedSteal, int millisecondsTimeout)`
  （bool TrySteal（out IThreadPoolWorkItem obj, ref bool missedSteal, int millisecondsTimeout））

---

## ThreadPoolWorkQueueThreadLocals（Thread池Work队列ThreadLocals）

### 字段 (4)

- `ThreadPoolWorkQueueThreadLocals threadLocals`（Thread池Work队列ThreadLocals threadLocals）(偏移: 0x80000000)
- `ThreadPoolWorkQueue workQueue`（Thread池Work队列 work队列）(偏移: 0x8)
- `ThreadPoolWorkQueue.WorkStealingQueue workStealingQueue`（Thread池WorkQueue.WorkStealing队列 workStealing队列）(偏移: 0xC)
- `Random random`（随机 random）(偏移: 0x10)

### 方法 (2)

- `void CleanUp()`
  （void Clean上（））
- `void Finalize()`
  （void 终结（））

---

## ThreadPriority（ThreadPriority）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ThreadSafeRandom（ThreadSafe随机）

### 字段 (2)

- `Random Global`（随机 全局的）(偏移: 0x0)
- `Random local`（随机 local）(偏移: 0x80000000)

### 方法 (3)

- `int Next(int minInclusive, int maxExclusive)`
  （int 下一个（int minInclusive, int maxExclusive））
- `int Next()`
  （int 下一个（））
- `int Next(int maxExclusive)`
  （int 下一个（int maxExclusive））

---

## ThreadStart（Thread开始）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke()`
  （void 调用（））
- `IAsyncResult BeginInvoke(AsyncCallback callback, object object)`
  （I异步结果 开始调用（异步回调 callback, 对象 object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## ThreadState（Thread状态）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ThrowHelper（投掷辅助器）

### 方法 (10)

- `void ThrowArgumentNullException(ExceptionArgument argument)`
  （void 投掷ArgumentNullException（ExceptionArgument argument））
- `Exception CreateArgumentNullException(ExceptionArgument argument)`
  （Exception 创建ArgumentNullException（ExceptionArgument argument））
- `void ThrowArgumentOutOfRangeException()`
  （void 投掷ArgumentOutOf范围Exception（））
- `void ThrowWrongValueTypeArgumentException(object value, Type targetType)`
  （void 投掷Wrong值类型ArgumentException（object value, 类型 targetType））
- `void ThrowArgumentException(ExceptionResource resource)`
  （void 投掷ArgumentException（Exception资源 resource））
- `void ThrowArgumentOutOfRangeException(ExceptionArgument argument, ExceptionResource resource)`
  （void 投掷ArgumentOutOf范围Exception（ExceptionArgument argument, Exception资源 resource））
- `void ThrowInvalidOperationException(ExceptionResource resource)`
  （void 投掷InvalidOperationException（Exception资源 resource））
- `void ThrowNotSupportedException(ExceptionResource resource)`
  （void 投掷NotSupportedException（Exception资源 resource））
- `string GetArgumentName(ExceptionArgument argument)`
  （string 获取Argument名称（ExceptionArgument argument））
- `string GetResourceName(ExceptionResource resource)`
  （string 获取资源名称（Exception资源 resource））

---

## ThrowStub（投掷Stub）

**继承**: ObjectDisposedException（对象DisposedException）

### 方法 (1)

- `void ThrowNotSupportedException()`
  （void 投掷NotSupportedException（））

---

## ThrowStub（投掷Stub）

**继承**: ObjectDisposedException（对象DisposedException）

### 方法 (1)

- `void ThrowNotSupportedException()`
  （void 投掷NotSupportedException（））

---

## ThrowStub（投掷Stub）

**继承**: ObjectDisposedException（对象DisposedException）

### 方法 (1)

- `void ThrowNotSupportedException()`
  （void 投掷NotSupportedException（））

---

## Tile（Tile）

**继承**: TileBase（Tile基础）

### 字段 (6)

- `Sprite m_Sprite`（精灵 m_精灵）(偏移: 0xC)
- `Color m_Color`（颜色 m_颜色）(偏移: 0x10)
- `Matrix4x4 m_Transform`（Matrix4x4 m_变换）(偏移: 0x20)
- `GameObject m_InstancedGameObject`（游戏对象 m_Instanced游戏对象）(偏移: 0x60)
- `TileFlags m_Flags`（TileFlags m_Flags）(偏移: 0x64)
- `Tile.ColliderType m_ColliderType`（Tile.碰撞器类型 m_碰撞器类型）(偏移: 0x68)

### 方法 (13)

- `Sprite get_sprite()`
  （精灵 get_sprite（））
- `void set_sprite(Sprite value)`
  （void set_sprite（精灵 value））
- `Color get_color()`
  （颜色 获取_颜色（））
- `void set_color(Color value)`
  （void 设置_颜色（颜色 value））
- `Matrix4x4 get_transform()`
  （Matrix4x4 get_transform（））
- `void set_transform(Matrix4x4 value)`
  （void set_transform（Matrix4x4 value））
- `GameObject get_gameObject()`
  （游戏对象 获取_游戏对象（））
- `void set_gameObject(GameObject value)`
  （void set_game对象（游戏对象 value））
- `TileFlags get_flags()`
  （TileFlags get_flags（））
- `void set_flags(TileFlags value)`
  （void set_flags（TileFlags value））
- `Tile.ColliderType get_colliderType()`
  （Tile.碰撞器类型 get_collider类型（））
- `void set_colliderType(Tile.ColliderType value)`
  （void set_collider类型（Tile.碰撞器类型 value））
- `void GetTileData(Vector3Int position, ITilemap tilemap, ref TileData tileData)`
  （void 获取Tile数据（三维向量整数 position, ITilemap tilemap, ref TileData tileData））

---

## Tile.ColliderType（Tile.碰撞器类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## TileAnimationData（Tile动画数据）

### 字段 (3)

- `Sprite[] m_AnimatedSprites`（Sprite[] m_AnimatedSprites）(偏移: 0x0)
- `float m_AnimationSpeed`（float m_动画Speed）(偏移: 0x4)
- `float m_AnimationStartTime`（float m_动画开始时间）(偏移: 0x8)

---

## TileBase（Tile基础）

**继承**: ScriptableObject（脚本对象）

### 方法 (6)

- `void RefreshTile(Vector3Int position, ITilemap tilemap)`
  （void 刷新Tile（三维向量整数 position, ITilemap tilemap））
- `void GetTileData(Vector3Int position, ITilemap tilemap, ref TileData tileData)`
  （void 获取Tile数据（三维向量整数 position, ITilemap tilemap, ref TileData tileData））
- `TileData GetTileDataNoRef(Vector3Int position, ITilemap tilemap)`
  （Tile数据 获取Tile数据NoRef（三维向量整数 position, ITilemap tilemap））
- `bool GetTileAnimationData(Vector3Int position, ITilemap tilemap, ref TileAnimationData tileAnimationData)`
  （bool 获取Tile动画数据（三维向量整数 position, ITilemap tilemap, ref TileAnimationData tileAnimationData））
- `TileAnimationData GetTileAnimationDataNoRef(Vector3Int position, ITilemap tilemap)`
  （Tile动画数据 获取Tile动画数据NoRef（三维向量整数 position, ITilemap tilemap））
- `bool StartUp(Vector3Int position, ITilemap tilemap, GameObject go)`
  （bool 开始上（三维向量整数 position, ITilemap tilemap, 游戏对象 go））

---

## TileData（Tile数据）

### 字段 (6)

- `Sprite m_Sprite`（精灵 m_精灵）(偏移: 0x0)
- `Color m_Color`（颜色 m_颜色）(偏移: 0x4)
- `Matrix4x4 m_Transform`（Matrix4x4 m_变换）(偏移: 0x14)
- `GameObject m_GameObject`（游戏对象 m_游戏对象）(偏移: 0x54)
- `TileFlags m_Flags`（TileFlags m_Flags）(偏移: 0x58)
- `Tile.ColliderType m_ColliderType`（Tile.碰撞器类型 m_碰撞器类型）(偏移: 0x5C)

### 方法 (6)

- `void set_sprite(Sprite value)`
  （void set_sprite（精灵 value））
- `void set_color(Color value)`
  （void 设置_颜色（颜色 value））
- `void set_transform(Matrix4x4 value)`
  （void set_transform（Matrix4x4 value））
- `void set_gameObject(GameObject value)`
  （void set_game对象（游戏对象 value））
- `void set_flags(TileFlags value)`
  （void set_flags（TileFlags value））
- `void set_colliderType(Tile.ColliderType value)`
  （void set_collider类型（Tile.碰撞器类型 value））

---

## TileData（Tile数据）

### 字段 (4)

- `uint tileID`（uint tileID）(偏移: 0x0)
- `uint listBitMask`（uint listBit掩码）(偏移: 0x4)
- `uint relLightOffset`（uint rel光照Offset）(偏移: 0x8)
- `uint unused`（uint unused）(偏移: 0xC)

---

## TileDepthRangePass（Tile深度范围Pass）

**继承**: ScriptableRenderPass（可脚本化渲染通道）

### 字段 (2)

- `DeferredLights m_DeferredLights`（DeferredLights m_DeferredLights）(偏移: 0x54)
- `int m_PassIndex`（int m_Pass索引）(偏移: 0x58)

### 方法 (3)

- `void Configure(CommandBuffer cmd, RenderTextureDescriptor cameraTextureDescriptor)`
  （void 配置（命令缓冲区 cmd, 渲染纹理描述符 cameraTextureDescriptor））
- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（可脚本化渲染上下文 context, 引用 渲染数据 renderingData））
- `void OnCameraCleanup(CommandBuffer cmd)`
  （void 摄像机清理时（命令缓冲区 cmd））

---

## TileFlags（TileFlags）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## TileHandler（Tile处理器）

### 字段 (11)

- `NavmeshBase graph`（Navmesh基础 graph）(偏移: 0x8)
- `int tileXCount`（int tileX数量）(偏移: 0xC)
- `int tileZCount`（int tileZ数量）(偏移: 0x10)
- `Clipper clipper`（Clipper clipper）(偏移: 0x14)
- `TileHandler.TileType[] activeTileTypes`（TileHandler.TileType[] activeTileTypes）(偏移: 0x1C)
- `int[] activeTileRotations`（int[] activeTileRotations）(偏移: 0x20)
- `int[] activeTileOffsets`（int[] activeTileOffsets）(偏移: 0x24)
- `bool[] reloadedInBatch`（bool[] reloadedInBatch）(偏移: 0x28)
- `GridLookup<NavmeshClipper> cuts`（网格Lookup<NavmeshClipper> cuts）(偏移: 0x2C)
- `int batchDepth`（int batch深度）(偏移: 0x30)
- `Int3PolygonClipper simpleClipper`（Int3PolygonClipper simpleClipper）(偏移: 0x34)

### 方法 (23)

- `bool get_isBatching()`
  （bool get_isBatching（））
- `bool get_isValid()`
  （布尔值 获取_是否有效（））
- `void OnRecalculatedTiles(NavmeshTile[] recalculatedTiles)`
  （void OnRecalculatedTiles（NavmeshTile[] recalculatedTiles））
- `int GetActiveRotation(Int2 p)`
  （int 获取激活的Rotation（Int2 p））
- `TileHandler.TileType RegisterTileType(Mesh source, Int3 centerOffset, int width = 1, int depth = 1)`
  （TileHandler.Tile类型 RegisterTile类型（网格 source, Int3 centerOffset, int width = 1, int depth = 1））
- `void CreateTileTypesFromGraph()`
  （void 创建TileTypesFromGraph（））
- `void UpdateTileType(NavmeshTile tile)`
  （void 更新Tile类型（NavmeshTile tile））
- `void StartBatchLoad()`
  （void 开始Batch加载（））
- `void EndBatchLoad()`
  （void 结束Batch加载（））
- `TileHandler.CuttingResult CutPoly(Int3[] verts, int[] tris, Int3[] extraShape, GraphTransform graphTransform, IntRect tiles, TileHandler.CutMode mode = 3, int perturbate = -1)`
  （TileHandler.CuttingResult CutPoly（Int3[] verts, int[] tris, Int3[] extraShape, Graph变换 graphTransform, 整数Rect tiles, TileHandler.Cut模式 mode = 3, int perturbate = -1））
- `List<TileHandler.Cut> PrepareNavmeshCutsForCutting(List<NavmeshCut> navmeshCuts, GraphTransform transform, IntRect cutSpaceBounds, int perturbate, bool anyNavmeshAdds)`
  （List<TileHandler.Cut> PrepareNavmeshCutsForCutting（List<NavmeshCut> navmeshCuts, Graph变换 transform, 整数Rect cutSpaceBounds, int perturbate, bool anyNavmeshAdds））
- `void PoolPolygon(Polygon polygon, Stack<Polygon> pool)`
  （void 池Polygon（Polygon polygon, Stack<Polygon> pool））
- `void CutAll(List<IntPoint> poly, List<int> intersectingCutIndices, List<TileHandler.Cut> cuts, PolyTree result)`
  （void Cut所有（List<整数Point> poly, List<int> intersectingCutIndices, List<TileHandler.Cut> cuts, PolyTree result））
- `void CutDual(List<IntPoint> poly, List<int> tmpIntersectingCuts, List<TileHandler.Cut> cuts, bool hasDual, List<List<IntPoint>> intermediateResult, PolyTree result)`
  （void CutDual（List<整数Point> poly, List<int> tmpIntersectingCuts, List<TileHandler.Cut> cuts, bool hasDual, List<List<整数Point>> intermediateResult, PolyTree result））
- `void CutExtra(List<IntPoint> poly, List<IntPoint> extraClipShape, PolyTree result)`
  （void Cut额外的（List<整数Point> poly, List<整数Point> extraClipShape, PolyTree result））
- `int ClipAgainstRectangle(Int3[] clipIn, Int3[] clipOut, Int2 size)`
  （int 弹匣AgainstRectangle（Int3[] clipIn, Int3[] clipOut, Int2 size））
- `void CopyMesh(Int3[] vertices, int[] triangles, List<Int3> outVertices, List<int> outTriangles)`
  （void 复制网格（Int3[] vertices, int[] triangles, List<Int3> outVertices, List<int> outTriangles））
- `void DelaunayRefinement(Int3[] verts, int[] tris, ref int tCount, bool delaunay, bool colinear)`
  （void DelaunayRefinement（Int3[] verts, int[] tris, ref int tCount, bool delaunay, bool colinear））
- `void ClearTile(int x, int z)`
  （void 清除Tile（int x, int z））
- `void ReloadInBounds(Bounds bounds)`
  （void 换弹InBounds（Bounds bounds））
- `void ReloadInBounds(IntRect tiles)`
  （void 换弹InBounds（整数Rect tiles））
- `void ReloadTile(int x, int z)`
  （void 换弹Tile（int x, int z））
- `void LoadTile(TileHandler.TileType tile, int x, int z, int rotation, int yoffset)`
  （void 加载Tile（TileHandler.Tile类型 tile, int x, int z, int rotation, int yoffset））

---

## TileHandler.Cut（TileHandler.Cut）

### 字段 (5)

- `IntRect bounds`（整数Rect bounds）(偏移: 0x8)
- `Int2 boundsY`（Int2 boundsY）(偏移: 0x18)
- `bool isDual`（bool isDual）(偏移: 0x20)
- `bool cutsAddedGeom`（bool cutsAddedGeom）(偏移: 0x21)
- `List<IntPoint> contour`（List<整数Point> contour）(偏移: 0x24)

---

## TileHandler.CutMode（TileHandler.Cut模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## TileHandler.CuttingResult（TileHandler.CuttingResult）

### 字段 (2)

- `Int3[] verts`（Int3[] verts）(偏移: 0x0)
- `int[] tris`（整数[] 三角形）(偏移: 0x4)

---

## TileHandler.TileType（TileHandler.Tile类型）

### 字段 (8)

- `Int3[] verts`（Int3[] verts）(偏移: 0x8)
- `int[] tris`（整数[] 三角形）(偏移: 0xC)
- `Int3 offset`（Int3 offset）(偏移: 0x10)
- `int lastYOffset`（int lastYOffset）(偏移: 0x1C)
- `int lastRotation`（int lastRotation）(偏移: 0x20)
- `int width`（整数 宽度）(偏移: 0x24)
- `int depth`（整数 深度）(偏移: 0x28)
- `int[] Rotations`（int[] Rotations）(偏移: 0x0)

### 方法 (3)

- `int get_Width()`
  （int get_宽度（））
- `int get_Depth()`
  （int get_深度（））
- `void Load(out Int3[] verts, out int[] tris, int rotation, int yoffset)`
  （void 加载（out Int3[] verts, out int[] tris, int rotation, int yoffset））

---

## TileHandlerHelper（Tile处理器辅助器）

**继承**: VersionedMonoBehaviour（版本化MonoBehaviour）

### 方法 (5)

- `float get_updateInterval()`
  （float get_update间隔（））
- `void set_updateInterval(float value)`
  （void set_update间隔（float value））
- `void UseSpecifiedHandler(TileHandler newHandler)`
  （void UseSpecified处理器（Tile处理器 newHandler））
- `void DiscardPending()`
  （void DiscardPending（））
- `void ForceUpdate()`
  （void 强制更新（））

---

## TileLayoutUtils（TileLayoutUtils）

### 方法 (3)

- `bool TryLayoutByTiles(RectInt src, uint tileSize, out RectInt main, out RectInt topRow, out RectInt rightCol, out RectInt topRight)`
  （bool TryLayoutByTiles（Rect整数 src, uint tileSize, out RectInt main, out RectInt topRow, out RectInt rightCol, out RectInt topRight））
- `bool TryLayoutByRow(RectInt src, uint tileSize, out RectInt main, out RectInt other)`
  （bool TryLayoutByRow（Rect整数 src, uint tileSize, out RectInt main, out RectInt other））
- `bool TryLayoutByCol(RectInt src, uint tileSize, out RectInt main, out RectInt other)`
  （bool TryLayoutByCol（Rect整数 src, uint tileSize, out RectInt main, out RectInt other））

---

## Tilemap（Tilemap）

**继承**: GridLayout（网格Layout）

### 方法 (2)

- `void RefreshTile(Vector3Int position)`
  （void 刷新Tile（三维向量整数 position））
- `void RefreshTile_Injected(ref Vector3Int position)`
  （void 刷新Tile_Injected（ref Vector3Int position））

---

## TilemapRenderer（Tilemap渲染器）

**继承**: Renderer（渲染器）

### 方法 (3)

- `void RegisterSpriteAtlasRegistered()`
  （void Register精灵AtlasRegistered（））
- `void UnregisterSpriteAtlasRegistered()`
  （void Unregister精灵AtlasRegistered（））
- `void OnSpriteAtlasRegistered(SpriteAtlas atlas)`
  （void On精灵AtlasRegistered（精灵Atlas atlas））

---

## Time（时间）

### 方法 (11)

- `float get_time()`
  （float get_time（））
- `float get_timeSinceLevelLoad()`
  （float get_timeSince等级加载（））
- `float get_deltaTime()`
  （浮点数 获取_增量时间（））
- `float get_unscaledTime()`
  （float get_unscaled时间（））
- `float get_unscaledDeltaTime()`
  （float get_unscaledDelta时间（））
- `float get_fixedDeltaTime()`
  （float get_fixedDelta时间（））
- `float get_smoothDeltaTime()`
  （float get_smoothDelta时间（））
- `float get_timeScale()`
  （float get_time缩放（））
- `int get_frameCount()`
  （int get_frame数量（））
- `int get_renderedFrameCount()`
  （int get_renderedFrame数量（））
- `float get_realtimeSinceStartup()`
  （float get_realtimeSinceStartup（））

---

## TimeCheatingDetector（时间CheatingDetector）

**继承**: ACTkDetectorBase（反作弊检测器基类）

### 字段 (20)

- `WaitForEndOfFrame cachedEndOfFrame`（WaitFor结束OfFrame cached结束OfFrame）(偏移: 0x0)
- `int instancesInScene`（int instancesIn场景）(偏移: 0x4)
- `bool gettingOnlineTime`（bool gettingOnline时间）(偏移: 0x8)
- `TimeCheatingDetector.TimeCheatingDetectorEventHandler CheatChecked`（时间CheatingDetector.时间CheatingDetector事件处理器 CheatChecked）(偏移: 0x1C)
- `string requestUrl`（string requestUrl）(偏移: 0x20)
- `TimeCheatingDetector.RequestMethod requestMethod`（时间CheatingDetector.请求Method requestMethod）(偏移: 0x24)
- `int timeoutSeconds`（int timeoutSeconds）(偏移: 0x28)
- `float interval`（浮点数 间隔）(偏移: 0x2C)
- `int realCheatThreshold`（int realCheatThreshold）(偏移: 0x30)
- `int wrongTimeThreshold`（int wrong时间Threshold）(偏移: 0x34)
- `string onlineOfflineDifferencePrefsKey`（string onlineOfflineDifferencePrefs键）(偏移: 0x44)
- `Uri cachedUri`（Uri cachedUri）(偏移: 0x48)
- `TimeCheatingDetector.TimeCheatingDetectorEventHandler cheatChecked`（时间CheatingDetector.时间CheatingDetector事件处理器 cheatChecked）(偏移: 0x4C)
- `float timeElapsed`（float timeElapsed）(偏移: 0x50)
- `bool updateAfterPause`（bool updateAfter暂停）(偏移: 0x54)
- `double lastOnlineSecondsUtc`（double lastOnlineSecondsUtc）(偏移: 0x58)
- `Action<TimeCheatingDetector.ErrorKind> Error`（Action<时间CheatingDetector.ErrorKind> Error）(偏移: 0x60)
- `Action CheckPassed`（动作 检查Passed）(偏移: 0x64)
- `int threshold`（int threshold）(偏移: 0x68)
- `string timeServer`（string time服务器）(偏移: 0x6C)

### 方法 (54)

- `void add_CheatChecked(TimeCheatingDetector.TimeCheatingDetectorEventHandler value)`
  （void add_CheatChecked（时间CheatingDetector.时间CheatingDetector事件处理器 value））
- `void remove_CheatChecked(TimeCheatingDetector.TimeCheatingDetectorEventHandler value)`
  （void remove_CheatChecked（时间CheatingDetector.时间CheatingDetector事件处理器 value））
- `string get_RequestUrl()`
  （string get_请求Url（））
- `void set_RequestUrl(string value)`
  （void set_请求Url（string value））
- `TimeCheatingDetector.ErrorKind get_LastError()`
  （时间CheatingDetector.ErrorKind get_最后一个Error（））
- `void set_LastError(TimeCheatingDetector.ErrorKind value)`
  （void set_最后一个Error（时间CheatingDetector.ErrorKind value））
- `TimeCheatingDetector.CheckResult get_LastResult()`
  （时间CheatingDetector.检查Result get_最后一个Result（））
- `void set_LastResult(TimeCheatingDetector.CheckResult value)`
  （void set_最后一个Result（时间CheatingDetector.检查Result value））
- `bool get_IsCheckingForCheat()`
  （bool get_是否CheckingForCheat（））
- `void set_IsCheckingForCheat(bool value)`
  （void set_是否CheckingForCheat（bool value））
- `TimeCheatingDetector get_Instance()`
  （时间CheatingDetector get_实例（））
- `void set_Instance(TimeCheatingDetector value)`
  （void set_实例（时间CheatingDetector value））
- `TimeCheatingDetector get_GetOrCreateInstance()`
  （时间CheatingDetector get_获取Or创建实例（））
- `void Awake()`
  （void 唤醒（））
- `void OnDestroy()`
  （void 销毁时（））
- `void OnLevelWasLoadedNew(Scene scene, LoadSceneMode mode)`
  （void On等级WasLoaded新的（场景 scene, 加载场景模式 mode））
- `void OnApplicationPause(bool pauseStatus)`
  （void OnApplication暂停（bool pauseStatus））
- `void Update()`
  （void 更新（））
- `TimeCheatingDetector AddToSceneOrGetExisting()`
  （时间CheatingDetector 添加To场景Or获取Existing（））
- `void StartDetection(TimeCheatingDetector.TimeCheatingDetectorEventHandler cheatCheckedEventHandler)`
  （void 开始Detection（时间CheatingDetector.时间CheatingDetector事件处理器 cheatCheckedEventHandler））
- `void StartDetection(float interval, TimeCheatingDetector.TimeCheatingDetectorEventHandler cheatCheckedEventHandler)`
  （void 开始Detection（float interval, 时间CheatingDetector.时间CheatingDetector事件处理器 cheatCheckedEventHandler））
- `void StopDetection()`
  （void 停止检测（））
- `void Dispose()`
  （void 释放（））
- `IEnumerator GetOnlineTimeCoroutine(string url, TimeCheatingDetector.OnlineTimeCallback callback, TimeCheatingDetector.RequestMethod method = 0)`
  （IEnumerator 获取Online时间协程（string url, 时间CheatingDetector.Online时间回调 callback, 时间CheatingDetector.请求Method method = 0））
- `IEnumerator GetOnlineTimeCoroutine(Uri uri, TimeCheatingDetector.OnlineTimeCallback callback, TimeCheatingDetector.RequestMethod method = 0)`
  （IEnumerator 获取Online时间协程（Uri uri, 时间CheatingDetector.Online时间回调 callback, 时间CheatingDetector.请求Method method = 0））
- `Task<TimeCheatingDetector.OnlineTimeResult> GetOnlineTimeTask(string url, TimeCheatingDetector.RequestMethod method = 0)`
  （Task<时间CheatingDetector.Online时间Result> 获取Online时间Task（string url, 时间CheatingDetector.请求Method method = 0））
- `Task<TimeCheatingDetector.OnlineTimeResult> GetOnlineTimeTask(Uri uri, TimeCheatingDetector.RequestMethod method = 0)`
  （Task<时间CheatingDetector.Online时间Result> 获取Online时间Task（Uri uri, 时间CheatingDetector.请求Method method = 0））
- `UnityWebRequest GetWebRequest(Uri uri, TimeCheatingDetector.RequestMethod method)`
  （Unity引擎Web请求 获取Web请求（Uri uri, 时间CheatingDetector.请求Method method））
- `void FillRequestResult(UnityWebRequest request, ref TimeCheatingDetector.OnlineTimeResult result)`
  （void Fill请求Result（Unity引擎Web请求 request, ref TimeCheatingDetector.OnlineTimeResult result））
- `Uri UrlToUri(string url)`
  （Uri UrlToUri（string url））
- `bool TryGetDate(string source, out DateTime date)`
  （bool Try获取Date（string source, out DateTime date））
- `bool ForceCheck()`
  （bool 强制检查（））
- `IEnumerator ForceCheckEnumerator()`
  （IEnumerator 强制检查Enumerator（））
- `Task<TimeCheatingDetector.CheckResult> ForceCheckTask()`
  （Task<时间CheatingDetector.检查Result> 强制检查Task（））
- `void StartDetectionInternal(float checkInterval, TimeCheatingDetector.TimeCheatingDetectorEventHandler cheatCheckedEventHandler)`
  （void 开始Detection内部的（float checkInterval, 时间CheatingDetector.时间CheatingDetector事件处理器 cheatCheckedEventHandler））
- `bool Init(ACTkDetectorBase instance, string detectorName)`
  （bool 初始化（ACTkDetector基础 instance, string detectorName））
- `void StartDetectionAutomatically()`
  （void 自动开始检测（））
- `bool DetectorHasCallbacks()`
  （bool Detector是否有Callbacks（））
- `void PauseDetector()`
  （void 暂停Detector（））
- `void StopDetectionInternal()`
  （void 停止Detection内部的（））
- `void DisposeInternal()`
  （void 释放内部（））
- `IEnumerator CheckForCheat()`
  （IEnumerator 检查ForCheat（））
- `void ReportCheckResult()`
  （void Report检查Result（））
- `void OnOnlineTimeReceived(TimeCheatingDetector.OnlineTimeResult result)`
  （void OnOnline时间Received（时间CheatingDetector.Online时间Result result））
- `double GetLocalSecondsUtc()`
  （double 获取本地的SecondsUtc（））
- `void add_Error(Action<TimeCheatingDetector.ErrorKind> value)`
  （void add_Error（Action<时间CheatingDetector.ErrorKind> value））
- `void remove_Error(Action<TimeCheatingDetector.ErrorKind> value)`
  （void remove_Error（Action<时间CheatingDetector.ErrorKind> value））
- `void add_CheckPassed(Action value)`
  （void add_检查Passed（动作 value））
- `void remove_CheckPassed(Action value)`
  （void remove_检查Passed（动作 value））
- `double GetOnlineTime(string server)`
  （double 获取Online时间（string server））
- `void SetErrorCallback(Action<TimeCheatingDetector.ErrorKind> errorCallback)`
  （void 集合Error回调（Action<时间CheatingDetector.ErrorKind> errorCallback））
- `void StartDetection(Action detectionCallback, int interval)`
  （void 开始Detection（动作 detectionCallback, int interval））
- `void StartDetection(Action detectionCallback, Action<TimeCheatingDetector.ErrorKind> errorCallback, int interval)`
  （void 开始Detection（动作 detectionCallback, Action<时间CheatingDetector.ErrorKind> errorCallback, int interval））
- `void StartDetection(float interval, Action detectionCallback, Action<TimeCheatingDetector.ErrorKind> errorCallback, Action checkPassedCallback)`
  （void 开始Detection（float interval, 动作 detectionCallback, Action<时间CheatingDetector.ErrorKind> errorCallback, 动作 checkPassedCallback））

---

## TimeCheatingDetector.CheckResult（时间CheatingDetector.检查Result）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## TimeCheatingDetector.ErrorKind（时间CheatingDetector.ErrorKind）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## TimeCheatingDetector.OnlineTimeCallback（时间CheatingDetector.Online时间回调）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(TimeCheatingDetector.OnlineTimeResult result)`
  （void Invoke（时间CheatingDetector.Online时间Result result））
- `IAsyncResult BeginInvoke(TimeCheatingDetector.OnlineTimeResult result, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（时间CheatingDetector.Online时间Result result, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## TimeCheatingDetector.OnlineTimeResult（时间CheatingDetector.Online时间Result）

### 字段 (4)

- `bool success`（bool success）(偏移: 0x0)
- `string error`（string error）(偏移: 0x4)
- `long errorResponseCode`（long error响应Code）(偏移: 0x8)
- `double onlineSecondsUtc`（double onlineSecondsUtc）(偏移: 0x10)

### 方法 (3)

- `void SetTime(double secondsUtc)`
  （void 集合时间（double secondsUtc））
- `void SetError(string errorText, long responseCode = -1)`
  （void 集合Error（string errorText, long responseCode = -1））
- `string ToString()`
  （字符串 转字符串（））

---

## TimeCheatingDetector.RequestMethod（时间CheatingDetector.请求Method）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## TimeCheatingDetector.TimeCheatingDetectorEventHandler（时间CheatingDetector.时间CheatingDetector事件处理器）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(TimeCheatingDetector.CheckResult checkResult, TimeCheatingDetector.ErrorKind errorKind)`
  （void Invoke（时间CheatingDetector.检查Result checkResult, 时间CheatingDetector.ErrorKind errorKind））
- `IAsyncResult BeginInvoke(TimeCheatingDetector.CheckResult checkResult, TimeCheatingDetector.ErrorKind errorKind, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（时间CheatingDetector.检查Result checkResult, 时间CheatingDetector.ErrorKind errorKind, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## TimeNotificationBehaviour（时间NotificationBehaviour）

**继承**: PlayableBehaviour（可播放行为）

### 字段 (4)

- `List<TimeNotificationBehaviour.NotificationEntry> m_Notifications`（List<时间NotificationBehaviour.NotificationEntry> m_Notifications）(偏移: 0x8)
- `double m_PreviousTime`（double m_上一个时间）(偏移: 0x10)
- `bool m_NeedSortNotifications`（bool m_需要SortNotifications）(偏移: 0x18)
- `Playable m_TimeSource`（Playable m_时间Source）(偏移: 0x1C)

### 方法 (12)

- `void set_timeSource(Playable value)`
  （void set_timeSource（Playable value））
- `ScriptPlayable<TimeNotificationBehaviour> Create(PlayableGraph graph, double duration, DirectorWrapMode loopMode)`
  （ScriptPlayable<时间NotificationBehaviour> 创建（PlayableGraph graph, double duration, DirectorWrap模式 loopMode））
- `void AddNotification(double time, INotification payload, NotificationFlags flags = 2)`
  （void 添加Notification（double time, INotification payload, NotificationFlags flags = 2））
- `void OnGraphStart(Playable playable)`
  （void OnGraph开始（Playable playable））
- `void OnBehaviourPause(Playable playable, FrameData info)`
  （void OnBehaviour暂停（Playable playable, Frame数据 info））
- `void PrepareFrame(Playable playable, FrameData info)`
  （void 准备帧（可播放 playable, 帧数据 info））
- `void SortNotifications()`
  （void SortNotifications（））
- `bool CanRestoreNotification(TimeNotificationBehaviour.NotificationEntry e, FrameData info, double currentTime, double previousTime)`
  （bool 能否RestoreNotification（时间NotificationBehaviour.NotificationEntry e, Frame数据 info, double currentTime, double previousTime））
- `void TriggerNotificationsInRange(double start, double end, FrameData info, Playable playable, bool checkState)`
  （void 触发器NotificationsIn范围（double start, double end, Frame数据 info, Playable playable, bool checkState））
- `void SyncDurationWithExternalSource(Playable playable)`
  （void 同步持续时间With外部的Source（Playable playable））
- `void Trigger_internal(Playable playable, PlayableOutput output, ref TimeNotificationBehaviour.NotificationEntry e)`
  （void Trigger_internal（Playable playable, PlayableOutput output, ref TimeNotificationBehaviour.NotificationEntry e））
- `void Restore_internal(ref TimeNotificationBehaviour.NotificationEntry e)`
  （void Restore_internal（ref TimeNotificationBehaviour.NotificationEntry e））

---

## TimeNotificationBehaviour.NotificationEntry（时间NotificationBehaviour.NotificationEntry）

### 字段 (4)

- `double time`（double time）(偏移: 0x0)
- `INotification payload`（INotification payload）(偏移: 0x8)
- `bool notificationFired`（bool notificationFired）(偏移: 0xC)
- `NotificationFlags flags`（NotificationFlags flags）(偏移: 0xE)

### 方法 (3)

- `bool get_triggerInEditor()`
  （bool get_triggerInEditor（））
- `bool get_prewarm()`
  （bool get_prewarm（））
- `bool get_triggerOnce()`
  （bool get_triggerOnce（））

---

## TimeSpan（时间Span）

**继承**: IComparable, IComparable<TimeSpan>, IEquatable<TimeSpan>, IFormattable（IComparable, IComparable<时间Span>, IEquatable<时间Span>, IFormattable）

### 字段 (6)

- `TimeSpan Zero`（时间Span Zero）(偏移: 0x0)
- `TimeSpan MaxValue`（时间Span 最大值）(偏移: 0x8)
- `TimeSpan MinValue`（时间Span 最小值）(偏移: 0x10)
- `long _ticks`（long _ticks）(偏移: 0x0)
- `bool _legacyConfigChecked`（bool _legacy配置Checked）(偏移: 0x18)
- `bool _legacyMode`（bool _legacy模式）(偏移: 0x19)

### 方法 (39)

- `long get_Ticks()`
  （long get_Ticks（））
- `int get_Hours()`
  （int get_Hours（））
- `int get_Minutes()`
  （int get_Minutes（））
- `double get_TotalDays()`
  （double get_TotalDays（））
- `double get_TotalHours()`
  （double get_TotalHours（））
- `double get_TotalMilliseconds()`
  （double get_TotalMilliseconds（））
- `double get_TotalMinutes()`
  （double get_TotalMinutes（））
- `double get_TotalSeconds()`
  （double get_TotalSeconds（））
- `TimeSpan Add(TimeSpan ts)`
  （时间Span 添加（时间Span ts））
- `int CompareTo(object value)`
  （整数 比较到（对象 value））
- `int CompareTo(TimeSpan value)`
  （int CompareTo（时间Span value））
- `TimeSpan FromDays(double value)`
  （时间Span FromDays（double value））
- `bool Equals(object value)`
  （布尔值 等于（对象 value））
- `bool Equals(TimeSpan obj)`
  （bool Equals（时间Span obj））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `TimeSpan FromHours(double value)`
  （时间Span FromHours（double value））
- `TimeSpan Interval(double value, int scale)`
  （时间Span 间隔（double value, int scale））
- `TimeSpan FromMilliseconds(double value)`
  （时间Span FromMilliseconds（double value））
- `TimeSpan FromMinutes(double value)`
  （时间Span FromMinutes（double value））
- `TimeSpan Negate()`
  （时间Span Negate（））
- `TimeSpan FromSeconds(double value)`
  （时间Span FromSeconds（double value））
- `TimeSpan Subtract(TimeSpan ts)`
  （时间Span Subtract（时间Span ts））
- `TimeSpan FromTicks(long value)`
  （时间Span FromTicks（long value））
- `long TimeToTicks(int hour, int minute, int second)`
  （long 时间ToTicks（int hour, int minute, int second））
- `TimeSpan Parse(string s)`
  （时间Span 解析（string s））
- `TimeSpan Parse(string input, IFormatProvider formatProvider)`
  （时间Span 解析（string input, I格式化提供者 formatProvider））
- `string ToString()`
  （字符串 转字符串（））
- `string ToString(string format)`
  （字符串 转字符串（字符串 格式））
- `string ToString(string format, IFormatProvider formatProvider)`
  （字符串 转字符串（字符串 格式, I格式化提供者 formatProvider））
- `TimeSpan op_Subtraction(TimeSpan t1, TimeSpan t2)`
  （时间Span op_Subtraction（时间Span t1, 时间Span t2））
- `TimeSpan op_Addition(TimeSpan t1, TimeSpan t2)`
  （时间Span op_Addition（时间Span t1, 时间Span t2））
- `bool op_Equality(TimeSpan t1, TimeSpan t2)`
  （bool op_Equality（时间Span t1, 时间Span t2））
- `bool op_Inequality(TimeSpan t1, TimeSpan t2)`
  （bool op_Inequality（时间Span t1, 时间Span t2））
- `bool op_LessThan(TimeSpan t1, TimeSpan t2)`
  （bool op_LessThan（时间Span t1, 时间Span t2））
- `bool op_LessThanOrEqual(TimeSpan t1, TimeSpan t2)`
  （bool op_LessThanOrEqual（时间Span t1, 时间Span t2））
- `bool op_GreaterThan(TimeSpan t1, TimeSpan t2)`
  （bool op_GreaterThan（时间Span t1, 时间Span t2））
- `bool op_GreaterThanOrEqual(TimeSpan t1, TimeSpan t2)`
  （bool op_GreaterThanOrEqual（时间Span t1, 时间Span t2））
- `bool GetLegacyFormatMode()`
  （bool 获取Legacy格式化模式（））
- `bool get_LegacyMode()`
  （bool get_Legacy模式（））

---

## TimeSpanConverter（时间SpanConverter）

**继承**: TypeConverter（类型转换器）

### 方法 (4)

- `bool CanConvertFrom(ITypeDescriptorContext context, Type sourceType)`
  （布尔值 能否转换自（I类型描述符上下文 context, 类型 sourceType））
- `bool CanConvertTo(ITypeDescriptorContext context, Type destinationType)`
  （布尔值 能否转换到（I类型描述符上下文 context, 类型 destinationType））
- `object ConvertFrom(ITypeDescriptorContext context, CultureInfo culture, object value)`
  （对象 转换自（I类型描述符上下文 context, 区域性信息 culture, 对象 value））
- `object ConvertTo(ITypeDescriptorContext context, CultureInfo culture, object value, Type destinationType)`
  （对象 转换到（I类型描述符上下文 context, 区域性信息 culture, 对象 value, 类型 destinationType））

---

## TimeSpanFormat（时间Span格式化）

### 字段 (2)

- `TimeSpanFormat.FormatLiterals PositiveInvariantFormatLiterals`（时间SpanFormat.格式化Literals PositiveInvariant格式化Literals）(偏移: 0x0)
- `TimeSpanFormat.FormatLiterals NegativeInvariantFormatLiterals`（时间SpanFormat.格式化Literals NegativeInvariant格式化Literals）(偏移: 0x1C)

### 方法 (4)

- `string IntToString(int n, int digits)`
  （string 整数To字符串（int n, int digits））
- `string Format(TimeSpan value, string format, IFormatProvider formatProvider)`
  （string 格式化（时间Span value, string format, I格式化提供者 formatProvider））
- `string FormatStandard(TimeSpan value, bool isInvariant, string format, TimeSpanFormat.Pattern pattern)`
  （string 格式化Standard（时间Span value, bool isInvariant, string format, 时间SpanFormat.Pattern pattern））
- `string FormatCustomized(TimeSpan value, string format, DateTimeFormatInfo dtfi)`
  （string 格式化Customized（时间Span value, string format, Date时间格式化信息 dtfi））

---

## TimeSpanFormat.FormatLiterals（时间SpanFormat.格式化Literals）

### 字段 (7)

- `string AppCompatLiteral`（string AppCompatLiteral）(偏移: 0x0)
- `int dd`（int dd）(偏移: 0x4)
- `int hh`（int hh）(偏移: 0x8)
- `int mm`（int mm）(偏移: 0xC)
- `int ss`（int ss）(偏移: 0x10)
- `int ff`（int ff）(偏移: 0x14)
- `string[] literals`（string[] literals）(偏移: 0x18)

### 方法 (8)

- `string get_Start()`
  （string get_开始（））
- `string get_DayHourSep()`
  （string get_DayHourSep（））
- `string get_HourMinuteSep()`
  （string get_HourMinuteSep（））
- `string get_MinuteSecondSep()`
  （string get_MinuteSecondSep（））
- `string get_SecondFractionSep()`
  （string get_SecondFractionSep（））
- `string get_End()`
  （string get_结束（））
- `TimeSpanFormat.FormatLiterals InitInvariant(bool isNegative)`
  （时间SpanFormat.格式化Literals 初始化Invariant（bool isNegative））
- `void Init(string format, bool useInvariantFieldLengths)`
  （void 初始化（string format, bool useInvariantFieldLengths））

---

## TimeSpanFormat.Pattern（时间SpanFormat.Pattern）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

