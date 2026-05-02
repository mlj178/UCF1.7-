# 游戏类定义 (Part 21/21)

共 27 个类 (总序号 4001 - 4027)

---

## ZoomAction（瞄准动作）

### 字段 (4)

- `float openTime`（float open时间）(偏移: 0x0)
- `float closeTime`（float close时间）(偏移: 0x4)
- `ZoomAction.ZoomData[] datas`（瞄准Action.瞄准Data[] datas）(偏移: 0x8)
- `bool closeZoomWhenShoot`（bool close瞄准When射击）(偏移: 0xC)

---

## ZoomAction.ZoomData（瞄准Action.瞄准数据）

### 字段 (3)

- `int type`（int type）(偏移: 0x0)
- `float fovScale`（float fov缩放）(偏移: 0x4)
- `Sprite sprite`（精灵 sprite）(偏移: 0x8)

---

## _AndroidJNIHelper（_AndroidJNI辅助器）

### 方法 (15)

- `IntPtr CreateJavaProxy(IntPtr delegateHandle, AndroidJavaProxy proxy)`
  （整数Ptr 创建Java代理（整数Ptr delegateHandle, AndroidJava代理 proxy））
- `IntPtr CreateJavaRunnable(AndroidJavaRunnable jrunnable)`
  （整数Ptr 创建JavaRunnable（AndroidJavaRunnable jrunnable））
- `IntPtr InvokeJavaProxyMethod(AndroidJavaProxy proxy, IntPtr jmethodName, IntPtr jargs)`
  （整数Ptr InvokeJava代理Method（AndroidJava代理 proxy, 整数Ptr jmethodName, 整数Ptr jargs））
- `jvalue[] CreateJNIArgArray(object[] args)`
  （jvalue[] 创建JNIArg数组（object[] args））
- `object UnboxArray(AndroidJavaObject obj)`
  （object Unbox数组（AndroidJava对象 obj））
- `object Unbox(AndroidJavaObject obj)`
  （object Unbox（AndroidJava对象 obj））
- `AndroidJavaObject Box(object obj)`
  （AndroidJava对象 Box（object obj））
- `void DeleteJNIArgArray(object[] args, jvalue[] jniArgs)`
  （void DeleteJNIArg数组（object[] args, jvalue[] jniArgs））
- `IntPtr ConvertToJNIArray(Array array)`
  （整数Ptr 转换ToJNI数组（数组 array））
- `IntPtr GetConstructorID(IntPtr jclass, object[] args)`
  （整数Ptr 获取ConstructorID（整数Ptr jclass, object[] args））
- `IntPtr GetConstructorID(IntPtr jclass, string signature)`
  （整数Ptr 获取ConstructorID（整数Ptr jclass, string signature））
- `IntPtr GetMethodID(IntPtr jclass, string methodName, string signature, bool isStatic)`
  （整数Ptr 获取MethodID（整数Ptr jclass, string methodName, string signature, bool isStatic））
- `IntPtr GetMethodIDFallback(IntPtr jclass, string methodName, string signature, bool isStatic)`
  （整数Ptr 获取MethodIDFallback（整数Ptr jclass, string methodName, string signature, bool isStatic））
- `string GetSignature(object obj)`
  （string 获取Signature（object obj））
- `string GetSignature(object[] args)`
  （string 获取Signature（object[] args））

---

## _ThreadPoolWaitCallback（_Thread池Wait回调）

### 方法 (1)

- `bool PerformWaitCallback()`
  （bool 执行Wait回调（））

---

## __BinaryParser（__BinaryParser）

### 字段 (25)

- `ObjectReader objectReader`（对象读取器 object读取器）(偏移: 0x8)
- `Stream input`（流 input）(偏移: 0xC)
- `long topId`（long topId）(偏移: 0x10)
- `long headerId`（long headerId）(偏移: 0x18)
- `SizedArray objectMapIdTable`（Sized数组 object映射IdTable）(偏移: 0x20)
- `SizedArray assemIdToAssemblyTable`（Sized数组 assemIdToAssemblyTable）(偏移: 0x24)
- `SerStack stack`（Ser栈 stack）(偏移: 0x28)
- `BinaryTypeEnum expectedType`（Binary类型Enum expected类型）(偏移: 0x2C)
- `object expectedTypeInformation`（object expected类型Information）(偏移: 0x30)
- `ParseRecord PRS`（解析Record PRS）(偏移: 0x34)
- `BinaryAssemblyInfo systemAssemblyInfo`（BinaryAssembly信息 systemAssembly信息）(偏移: 0x38)
- `BinaryReader dataReader`（Binary读取器 data读取器）(偏移: 0x3C)
- `Encoding encoding`（Encoding encoding）(偏移: 0x0)
- `SerStack opPool`（Ser栈 op池）(偏移: 0x40)
- `BinaryObject binaryObject`（Binary对象 binary对象）(偏移: 0x44)
- `BinaryObjectWithMap bowm`（Binary对象With映射 bowm）(偏移: 0x48)
- `BinaryObjectWithMapTyped bowmt`（Binary对象With映射Typed bowmt）(偏移: 0x4C)
- `BinaryObjectString objectString`（Binary对象字符串 object字符串）(偏移: 0x50)
- `BinaryCrossAppDomainString crossAppDomainString`（BinaryCrossAppDomain字符串 crossAppDomain字符串）(偏移: 0x54)
- `MemberPrimitiveTyped memberPrimitiveTyped`（MemberPrimitiveTyped memberPrimitiveTyped）(偏移: 0x58)
- `byte[] byteBuffer`（byte[] byte缓冲区）(偏移: 0x5C)
- `MemberPrimitiveUnTyped memberPrimitiveUnTyped`（MemberPrimitiveUnTyped memberPrimitiveUnTyped）(偏移: 0x60)
- `MemberReference memberReference`（Member引用 member引用）(偏移: 0x64)
- `ObjectNull objectNull`（对象Null objectNull）(偏移: 0x68)
- `MessageEnd messageEnd`（Message结束 message结束）(偏移: 0x4)

### 方法 (45)

- `BinaryAssemblyInfo get_SystemAssemblyInfo()`
  （BinaryAssembly信息 get_系统Assembly信息（））
- `SizedArray get_ObjectMapIdTable()`
  （Sized数组 get_对象映射IdTable（））
- `SizedArray get_AssemIdToAssemblyTable()`
  （Sized数组 get_AssemIdToAssemblyTable（））
- `ParseRecord get_prs()`
  （解析Record get_prs（））
- `void Run()`
  （void 运行（））
- `void ReadBegin()`
  （void ReadBegin（））
- `void ReadEnd()`
  （void Read结束（））
- `bool ReadBoolean()`
  （bool ReadBoolean（））
- `byte ReadByte()`
  （byte ReadByte（））
- `byte[] ReadBytes(int length)`
  （byte[] ReadBytes（int length））
- `void ReadBytes(byte[] byteA, int offset, int size)`
  （void ReadBytes（byte[] byteA, int offset, int size））
- `char ReadChar()`
  （char ReadChar（））
- `char[] ReadChars(int length)`
  （char[] ReadChars（int length））
- `Decimal ReadDecimal()`
  （Decimal ReadDecimal（））
- `float ReadSingle()`
  （float Read单个（））
- `double ReadDouble()`
  （double ReadDouble（））
- `short ReadInt16()`
  （short ReadInt16（））
- `int ReadInt32()`
  （int ReadInt32（））
- `long ReadInt64()`
  （long ReadInt64（））
- `sbyte ReadSByte()`
  （sbyte ReadSByte（））
- `string ReadString()`
  （string Read字符串（））
- `TimeSpan ReadTimeSpan()`
  （时间Span Read时间Span（））
- `DateTime ReadDateTime()`
  （Date时间 ReadDate时间（））
- `ushort ReadUInt16()`
  （ushort ReadUInt16（））
- `uint ReadUInt32()`
  （uint ReadUInt32（））
- `ulong ReadUInt64()`
  （ulong ReadUInt64（））
- `void ReadSerializationHeaderRecord()`
  （void ReadSerialization标题Record（））
- `void ReadAssembly(BinaryHeaderEnum binaryHeaderEnum)`
  （void ReadAssembly（Binary标题Enum binaryHeaderEnum））
- `void ReadObject()`
  （void Read对象（））
- `void ReadCrossAppDomainMap()`
  （void ReadCrossAppDomain映射（））
- `void ReadObjectWithMap(BinaryHeaderEnum binaryHeaderEnum)`
  （void Read对象With映射（Binary标题Enum binaryHeaderEnum））
- `void ReadObjectWithMap(BinaryObjectWithMap record)`
  （void Read对象With映射（Binary对象With映射 record））
- `void ReadObjectWithMapTyped(BinaryHeaderEnum binaryHeaderEnum)`
  （void Read对象With映射Typed（Binary标题Enum binaryHeaderEnum））
- `void ReadObjectWithMapTyped(BinaryObjectWithMapTyped record)`
  （void Read对象With映射Typed（Binary对象With映射Typed record））
- `void ReadObjectString(BinaryHeaderEnum binaryHeaderEnum)`
  （void Read对象字符串（Binary标题Enum binaryHeaderEnum））
- `void ReadMemberPrimitiveTyped()`
  （void ReadMemberPrimitiveTyped（））
- `void ReadArray(BinaryHeaderEnum binaryHeaderEnum)`
  （void Read数组（Binary标题Enum binaryHeaderEnum））
- `void ReadArrayAsBytes(ParseRecord pr)`
  （void Read数组AsBytes（解析Record pr））
- `void ReadMemberPrimitiveUnTyped()`
  （void ReadMemberPrimitiveUnTyped（））
- `void ReadMemberReference()`
  （void ReadMember引用（））
- `void ReadObjectNull(BinaryHeaderEnum binaryHeaderEnum)`
  （void Read对象Null（Binary标题Enum binaryHeaderEnum））
- `void ReadMessageEnd()`
  （void ReadMessage结束（））
- `object ReadValue(InternalPrimitiveTypeE code)`
  （object Read值（内部的Primitive类型E code））
- `ObjectProgress GetOp()`
  （对象Progress 获取Op（））
- `void PutOp(ObjectProgress op)`
  （void PutOp（对象Progress op））

---

## __BinaryWriter（__Binary写入器）

### 字段 (21)

- `Stream sout`（流 sout）(偏移: 0x8)
- `FormatterTypeStyle formatterTypeStyle`（Formatter类型Style formatter类型Style）(偏移: 0xC)
- `Hashtable objectMapTable`（Hashtable object映射Table）(偏移: 0x10)
- `ObjectWriter objectWriter`（对象写入器 object写入器）(偏移: 0x14)
- `BinaryWriter dataWriter`（Binary写入器 data写入器）(偏移: 0x18)
- `int m_nestedObjectCount`（int m_nested对象数量）(偏移: 0x1C)
- `int nullCount`（int null数量）(偏移: 0x20)
- `BinaryMethodCall binaryMethodCall`（BinaryMethodCall binaryMethodCall）(偏移: 0x24)
- `BinaryMethodReturn binaryMethodReturn`（BinaryMethodReturn binaryMethodReturn）(偏移: 0x28)
- `BinaryObject binaryObject`（Binary对象 binary对象）(偏移: 0x2C)
- `BinaryObjectWithMap binaryObjectWithMap`（Binary对象With映射 binary对象With映射）(偏移: 0x30)
- `BinaryObjectWithMapTyped binaryObjectWithMapTyped`（Binary对象With映射Typed binary对象With映射Typed）(偏移: 0x34)
- `BinaryObjectString binaryObjectString`（Binary对象字符串 binary对象字符串）(偏移: 0x38)
- `BinaryArray binaryArray`（Binary数组 binary数组）(偏移: 0x3C)
- `byte[] byteBuffer`（byte[] byte缓冲区）(偏移: 0x40)
- `int chunkSize`（int chunk大小）(偏移: 0x44)
- `MemberPrimitiveUnTyped memberPrimitiveUnTyped`（MemberPrimitiveUnTyped memberPrimitiveUnTyped）(偏移: 0x48)
- `MemberPrimitiveTyped memberPrimitiveTyped`（MemberPrimitiveTyped memberPrimitiveTyped）(偏移: 0x4C)
- `ObjectNull objectNull`（对象Null objectNull）(偏移: 0x50)
- `MemberReference memberReference`（Member引用 member引用）(偏移: 0x54)
- `BinaryAssembly binaryAssembly`（BinaryAssembly binaryAssembly）(偏移: 0x58)

### 方法 (46)

- `void WriteBegin()`
  （void WriteBegin（））
- `void WriteEnd()`
  （void Write结束（））
- `void WriteBoolean(bool value)`
  （void WriteBoolean（bool value））
- `void WriteByte(byte value)`
  （void WriteByte（byte value））
- `void WriteBytes(byte[] value)`
  （void WriteBytes（byte[] value））
- `void WriteBytes(byte[] byteA, int offset, int size)`
  （void WriteBytes（byte[] byteA, int offset, int size））
- `void WriteChar(char value)`
  （void WriteChar（char value））
- `void WriteChars(char[] value)`
  （void WriteChars（char[] value））
- `void WriteDecimal(Decimal value)`
  （void WriteDecimal（Decimal value））
- `void WriteSingle(float value)`
  （void Write单个（float value））
- `void WriteDouble(double value)`
  （void WriteDouble（double value））
- `void WriteInt16(short value)`
  （void WriteInt16（short value））
- `void WriteInt32(int value)`
  （void WriteInt32（int value））
- `void WriteInt64(long value)`
  （void WriteInt64（long value））
- `void WriteSByte(sbyte value)`
  （void WriteSByte（sbyte value））
- `void WriteString(string value)`
  （void Write字符串（string value））
- `void WriteTimeSpan(TimeSpan value)`
  （void Write时间Span（时间Span value））
- `void WriteDateTime(DateTime value)`
  （void WriteDate时间（Date时间 value））
- `void WriteUInt16(ushort value)`
  （void WriteUInt16（ushort value））
- `void WriteUInt32(uint value)`
  （void WriteUInt32（uint value））
- `void WriteUInt64(ulong value)`
  （void WriteUInt64（ulong value））
- `void WriteObjectEnd(NameInfo memberNameInfo, NameInfo typeNameInfo)`
  （void Write对象结束（名称信息 memberNameInfo, 名称信息 typeNameInfo））
- `void WriteSerializationHeaderEnd()`
  （void WriteSerialization标题结束（））
- `void WriteSerializationHeader(int topId, int headerId, int minorVersion, int majorVersion)`
  （void WriteSerialization标题（int topId, int headerId, int minorVersion, int majorVersion））
- `void WriteMethodCall()`
  （void WriteMethodCall（））
- `void WriteMethodReturn()`
  （void WriteMethodReturn（））
- `void WriteObject(NameInfo nameInfo, NameInfo typeNameInfo, int numMembers, string[] memberNames, Type[] memberTypes, WriteObjectInfo[] memberObjectInfos)`
  （void Write对象（名称信息 nameInfo, 名称信息 typeNameInfo, int numMembers, string[] memberNames, Type[] memberTypes, Write对象Info[] memberObjectInfos））
- `void WriteObjectString(int objectId, string value)`
  （void Write对象字符串（int objectId, string value））
- `void WriteSingleArray(NameInfo memberNameInfo, NameInfo arrayNameInfo, WriteObjectInfo objectInfo, NameInfo arrayElemTypeNameInfo, int length, int lowerBound, Array array)`
  （void Write单个数组（名称信息 memberNameInfo, 名称信息 arrayNameInfo, Write对象信息 objectInfo, 名称信息 arrayElemTypeNameInfo, int length, int lowerBound, 数组 array））
- `void WriteArrayAsBytes(Array array, int typeLength)`
  （void Write数组AsBytes（数组 array, int typeLength））
- `void WriteJaggedArray(NameInfo memberNameInfo, NameInfo arrayNameInfo, WriteObjectInfo objectInfo, NameInfo arrayElemTypeNameInfo, int length, int lowerBound)`
  （void WriteJagged数组（名称信息 memberNameInfo, 名称信息 arrayNameInfo, Write对象信息 objectInfo, 名称信息 arrayElemTypeNameInfo, int length, int lowerBound））
- `void WriteRectangleArray(NameInfo memberNameInfo, NameInfo arrayNameInfo, WriteObjectInfo objectInfo, NameInfo arrayElemTypeNameInfo, int rank, int[] lengthA, int[] lowerBoundA)`
  （void WriteRectangle数组（名称信息 memberNameInfo, 名称信息 arrayNameInfo, Write对象信息 objectInfo, 名称信息 arrayElemTypeNameInfo, int rank, int[] lengthA, int[] lowerBoundA））
- `void WriteObjectByteArray(NameInfo memberNameInfo, NameInfo arrayNameInfo, WriteObjectInfo objectInfo, NameInfo arrayElemTypeNameInfo, int length, int lowerBound, byte[] byteA)`
  （void Write对象Byte数组（名称信息 memberNameInfo, 名称信息 arrayNameInfo, Write对象信息 objectInfo, 名称信息 arrayElemTypeNameInfo, int length, int lowerBound, byte[] byteA））
- `void WriteMember(NameInfo memberNameInfo, NameInfo typeNameInfo, object value)`
  （void WriteMember（名称信息 memberNameInfo, 名称信息 typeNameInfo, object value））
- `void WriteNullMember(NameInfo memberNameInfo, NameInfo typeNameInfo)`
  （void WriteNullMember（名称信息 memberNameInfo, 名称信息 typeNameInfo））
- `void WriteMemberObjectRef(NameInfo memberNameInfo, int idRef)`
  （void WriteMember对象Ref（名称信息 memberNameInfo, int idRef））
- `void WriteMemberNested(NameInfo memberNameInfo)`
  （void WriteMemberNested（名称信息 memberNameInfo））
- `void WriteMemberString(NameInfo memberNameInfo, NameInfo typeNameInfo, string value)`
  （void WriteMember字符串（名称信息 memberNameInfo, 名称信息 typeNameInfo, string value））
- `void WriteItem(NameInfo itemNameInfo, NameInfo typeNameInfo, object value)`
  （void Write项目（名称信息 itemNameInfo, 名称信息 typeNameInfo, object value））
- `void WriteNullItem(NameInfo itemNameInfo, NameInfo typeNameInfo)`
  （void WriteNull项目（名称信息 itemNameInfo, 名称信息 typeNameInfo））
- `void WriteDelayedNullItem()`
  （void WriteDelayedNull项目（））
- `void WriteItemEnd()`
  （void Write项目结束（））
- `void InternalWriteItemNull()`
  （void 内部的Write项目Null（））
- `void WriteItemObjectRef(NameInfo nameInfo, int idRef)`
  （void Write项目对象Ref（名称信息 nameInfo, int idRef））
- `void WriteAssembly(Type type, string assemblyString, int assemId, bool isNew)`
  （void WriteAssembly（类型 type, string assemblyString, int assemId, bool isNew））
- `void WriteValue(InternalPrimitiveTypeE code, object value)`
  （void Write值（内部的Primitive类型E code, object value））

---

## __DTString（__DT字符串）

### 字段 (7)

- `string Value`（string 值）(偏移: 0x0)
- `int Index`（int 索引）(偏移: 0x4)
- `int len`（int len）(偏移: 0x8)
- `char m_current`（char m_current）(偏移: 0xC)
- `CompareInfo m_info`（Compare信息 m_info）(偏移: 0x10)
- `bool m_checkDigitToken`（bool m_checkDigit令牌）(偏移: 0x14)
- `char[] WhiteSpaceChecks`（char[] WhiteSpaceChecks）(偏移: 0x0)

### 方法 (14)

- `bool GetNext()`
  （bool 获取下一个（））
- `bool AtEnd()`
  （bool At结束（））
- `bool Advance(int count)`
  （bool Advance（int count））
- `void GetRegularToken(out TokenType tokenType, out int tokenValue, DateTimeFormatInfo dtfi)`
  （void 获取Regular令牌（out TokenType tokenType, out int tokenValue, Date时间格式化信息 dtfi））
- `TokenType GetSeparatorToken(DateTimeFormatInfo dtfi, out int indexBeforeSeparator, out char charBeforeSeparator)`
  （令牌类型 获取Separator令牌（Date时间格式化信息 dtfi, out int indexBeforeSeparator, out char charBeforeSeparator））
- `bool MatchSpecifiedWords(string target, bool checkWordBoundary, ref int matchLength)`
  （bool 比赛SpecifiedWords（string target, bool checkWordBoundary, ref int matchLength））
- `bool Match(char ch)`
  （bool 比赛（char ch））
- `bool GetNextDigit()`
  （bool 获取下一个Digit（））
- `char GetChar()`
  （char 获取Char（））
- `int GetDigit()`
  （int 获取Digit（））
- `void SkipWhiteSpaces()`
  （void SkipWhiteSpaces（））
- `bool SkipWhiteSpaceCurrent()`
  （bool SkipWhiteSpace当前（））
- `DTSubString GetSubString()`
  （DT子字符串 获取子字符串（））
- `void ConsumeSubString(DTSubString sub)`
  （void Consume子字符串（DT子字符串 sub））

---

## __Error（__Error）

### 方法 (13)

- `void EndOfFile()`
  （void 结束Of文件（））
- `void FileNotOpen()`
  （void 文件Not打开（））
- `void StreamIsClosed()`
  （void 流是否Closed（））
- `void MemoryStreamNotExpandable()`
  （void Memory流NotExpandable（））
- `void ReaderClosed()`
  （void 读取器Closed（））
- `void ReadNotSupported()`
  （void ReadNotSupported（））
- `void WrongAsyncResult()`
  （void Wrong异步Result（））
- `void EndReadCalledTwice()`
  （void 结束ReadCalledTwice（））
- `void EndWriteCalledTwice()`
  （void 结束WriteCalledTwice（））
- `string GetDisplayablePath(string path, bool isInvalidPath)`
  （string 获取Displayable路径（string path, bool isInvalidPath））
- `void WinIOError(int errorCode, string maybeFullPath)`
  （void WinIOError（int errorCode, string maybeFullPath））
- `void WriteNotSupported()`
  （void WriteNotSupported（））
- `void WriterClosed()`
  （void 写入器Closed（））

---

## __Filters（__Filters）

### 字段 (1)

- `__Filters Instance`（__Filters 实例）(偏移: 0x0)

### 方法 (3)

- `bool FilterAttribute(MemberInfo m, object filterCriteria)`
  （bool FilterAttribute（Member信息 m, object filterCriteria））
- `bool FilterName(MemberInfo m, object filterCriteria)`
  （bool Filter名称（Member信息 m, object filterCriteria））
- `bool FilterIgnoreCase(MemberInfo m, object filterCriteria)`
  （bool FilterIgnoreCase（Member信息 m, object filterCriteria））

---

## __Il2CppComDelegate（__Il2CppCom委托）

**继承**: __Il2CppComObject（__Il2CppCom对象）

### 方法 (1)

- `void Finalize()`
  （void Finalize（））

---

## __Il2CppComObject（__Il2CppCom对象）

### 方法 (1)

- `void Finalize()`
  （void Finalize（））

---

## float2（float2）

**继承**: IEquatable<float2>, IFormattable（IEquatable<float2>, IFormattable）

### 字段 (2)

- `float x`（float x）(偏移: 0x0)
- `float y`（float y）(偏移: 0x4)

### 方法 (9)

- `float2 op_Multiply(float2 lhs, float2 rhs)`
  （float2 op_Multiply（float2 lhs, float2 rhs））
- `float2 op_Multiply(float2 lhs, float rhs)`
  （float2 op_Multiply（float2 lhs, float rhs））
- `float2 op_Subtraction(float2 lhs, float2 rhs)`
  （float2 op_Subtraction（float2 lhs, float2 rhs））
- `bool Equals(float2 rhs)`
  （bool Equals（float2 rhs））
- `bool Equals(object o)`
  （bool Equals（object o））
- `int GetHashCode()`
  （int 获取HashCode（））
- `string ToString()`
  （string To字符串（））
- `string ToString(string format, IFormatProvider formatProvider)`
  （string To字符串（string format, I格式化提供者 formatProvider））
- `float2 op_Implicit(Vector2 v)`
  （float2 op_Implicit（二维向量 v））

---

## float2.DebuggerProxy（float2.Debugger代理）

### 字段 (2)

- `float x`（float x）(偏移: 0x8)
- `float y`（float y）(偏移: 0xC)

---

## float3（float3）

**继承**: IEquatable<float3>, IFormattable（IEquatable<float3>, IFormattable）

### 字段 (4)

- `float x`（float x）(偏移: 0x0)
- `float y`（float y）(偏移: 0x4)
- `float z`（float z）(偏移: 0x8)
- `float3 zero`（float3 zero）(偏移: 0x0)

### 方法 (13)

- `float3 op_Multiply(float3 lhs, float3 rhs)`
  （float3 op_Multiply（float3 lhs, float3 rhs））
- `float3 op_Multiply(float3 lhs, float rhs)`
  （float3 op_Multiply（float3 lhs, float rhs））
- `float3 op_Multiply(float lhs, float3 rhs)`
  （float3 op_Multiply（float lhs, float3 rhs））
- `float3 op_Addition(float3 lhs, float3 rhs)`
  （float3 op_Addition（float3 lhs, float3 rhs））
- `float3 op_Subtraction(float3 lhs, float3 rhs)`
  （float3 op_Subtraction（float3 lhs, float3 rhs））
- `float3 get_yzx()`
  （float3 get_yzx（））
- `bool Equals(float3 rhs)`
  （bool Equals（float3 rhs））
- `bool Equals(object o)`
  （bool Equals（object o））
- `int GetHashCode()`
  （int 获取HashCode（））
- `string ToString()`
  （string To字符串（））
- `string ToString(string format, IFormatProvider formatProvider)`
  （string To字符串（string format, I格式化提供者 formatProvider））
- `Vector3 op_Implicit(float3 v)`
  （三维向量 op_Implicit（float3 v））
- `float3 op_Implicit(Vector3 v)`
  （float3 op_Implicit（三维向量 v））

---

## float3.DebuggerProxy（float3.Debugger代理）

### 字段 (3)

- `float x`（float x）(偏移: 0x8)
- `float y`（float y）(偏移: 0xC)
- `float z`（float z）(偏移: 0x10)

---

## float4（float4）

**继承**: IEquatable<float4>, IFormattable（IEquatable<float4>, IFormattable）

### 字段 (4)

- `float x`（float x）(偏移: 0x0)
- `float y`（float y）(偏移: 0x4)
- `float z`（float z）(偏移: 0x8)
- `float w`（float w）(偏移: 0xC)

### 方法 (6)

- `float3 get_xyz()`
  （float3 get_xyz（））
- `bool Equals(float4 rhs)`
  （bool Equals（float4 rhs））
- `bool Equals(object o)`
  （bool Equals（object o））
- `int GetHashCode()`
  （int 获取HashCode（））
- `string ToString()`
  （string To字符串（））
- `string ToString(string format, IFormatProvider formatProvider)`
  （string To字符串（string format, I格式化提供者 formatProvider））

---

## float4.DebuggerProxy（float4.Debugger代理）

### 字段 (4)

- `float x`（float x）(偏移: 0x8)
- `float y`（float y）(偏移: 0xC)
- `float z`（float z）(偏移: 0x10)
- `float w`（float w）(偏移: 0x14)

---

## jvalue（jvalue）

### 字段 (9)

- `bool z`（bool z）(偏移: 0x0)
- `sbyte b`（sbyte b）(偏移: 0x0)
- `char c`（char c）(偏移: 0x0)
- `short s`（short s）(偏移: 0x0)
- `int i`（int i）(偏移: 0x0)
- `long j`（long j）(偏移: 0x0)
- `float f`（float f）(偏移: 0x0)
- `double d`（double d）(偏移: 0x0)
- `IntPtr l`（整数Ptr l）(偏移: 0x0)

---

## math（math）

### 方法 (37)

- `float2 float2(float x, float y)`
  （float2 float2（float x, float y））
- `uint hash(float2 v)`
  （uint hash（float2 v））
- `uint hash(float3 v)`
  （uint hash（float3 v））
- `uint hash(float4 v)`
  （uint hash（float4 v））
- `int asint(float x)`
  （int asint（float x））
- `uint asuint(float x)`
  （uint asuint（float x））
- `uint2 asuint(float2 x)`
  （uint2 asuint（float2 x））
- `uint3 asuint(float3 x)`
  （uint3 asuint（float3 x））
- `uint4 asuint(float4 x)`
  （uint4 asuint（float4 x））
- `float asfloat(int x)`
  （float asfloat（int x））
- `float asfloat(uint x)`
  （float asfloat（uint x））
- `float2 asfloat(uint2 x)`
  （float2 asfloat（uint2 x））
- `int min(int x, int y)`
  （int min（int x, int y））
- `float min(float x, float y)`
  （float min（float x, float y））
- `float3 min(float3 x, float3 y)`
  （float3 min（float3 x, float3 y））
- `int max(int x, int y)`
  （int max（int x, int y））
- `float max(float x, float y)`
  （float max（float x, float y））
- `float3 max(float3 x, float3 y)`
  （float3 max（float3 x, float3 y））
- `float2 abs(float2 x)`
  （float2 abs（float2 x））
- `float dot(float3 x, float3 y)`
  （float dot（float3 x, float3 y））
- `float cos(float x)`
  （float cos（float x））
- `float sin(float x)`
  （float sin（float x））
- `float sqrt(float x)`
  （float sqrt（float x））
- `float rsqrt(float x)`
  （float rsqrt（float x））
- `float3 normalize(float3 x)`
  （float3 normalize（float3 x））
- `float length(float3 x)`
  （float length（float3 x））
- `float3 cross(float3 x, float3 y)`
  （float3 cross（float3 x, float3 y））
- `uint select(uint a, uint b, bool c)`
  （uint select（uint a, uint b, bool c））
- `uint csum(uint2 x)`
  （uint csum（uint2 x））
- `uint csum(uint3 x)`
  （uint csum（uint3 x））
- `uint csum(uint4 x)`
  （uint csum（uint4 x））
- `uint2 uint2(uint x, uint y)`
  （uint2 uint2（uint x, uint y））
- `uint hash(uint2 v)`
  （uint hash（uint2 v））
- `uint3 uint3(uint x, uint y, uint z)`
  （uint3 uint3（uint x, uint y, uint z））
- `uint hash(uint3 v)`
  （uint hash（uint3 v））
- `uint4 uint4(uint x, uint y, uint z, uint w)`
  （uint4 uint4（uint x, uint y, uint z, uint w））
- `uint hash(uint4 v)`
  （uint hash（uint4 v））

---

## math.IntFloatUnion（math.整数浮点数Union）

### 字段 (2)

- `int intValue`（int int值）(偏移: 0x0)
- `float floatValue`（float float值）(偏移: 0x0)

---

## uint2（uint2）

**继承**: IEquatable<uint2>, IFormattable（IEquatable<uint2>, IFormattable）

### 字段 (2)

- `uint x`（uint x）(偏移: 0x0)
- `uint y`（uint y）(偏移: 0x4)

### 方法 (7)

- `uint2 op_Multiply(uint2 lhs, uint2 rhs)`
  （uint2 op_Multiply（uint2 lhs, uint2 rhs））
- `uint2 op_BitwiseAnd(uint2 lhs, uint rhs)`
  （uint2 op_BitwiseAnd（uint2 lhs, uint rhs））
- `bool Equals(uint2 rhs)`
  （bool Equals（uint2 rhs））
- `bool Equals(object o)`
  （bool Equals（object o））
- `int GetHashCode()`
  （int 获取HashCode（））
- `string ToString()`
  （string To字符串（））
- `string ToString(string format, IFormatProvider formatProvider)`
  （string To字符串（string format, I格式化提供者 formatProvider））

---

## uint2.DebuggerProxy（uint2.Debugger代理）

### 字段 (2)

- `uint x`（uint x）(偏移: 0x8)
- `uint y`（uint y）(偏移: 0xC)

---

## uint3（uint3）

**继承**: IEquatable<uint3>, IFormattable（IEquatable<uint3>, IFormattable）

### 字段 (3)

- `uint x`（uint x）(偏移: 0x0)
- `uint y`（uint y）(偏移: 0x4)
- `uint z`（uint z）(偏移: 0x8)

### 方法 (6)

- `uint3 op_Multiply(uint3 lhs, uint3 rhs)`
  （uint3 op_Multiply（uint3 lhs, uint3 rhs））
- `bool Equals(uint3 rhs)`
  （bool Equals（uint3 rhs））
- `bool Equals(object o)`
  （bool Equals（object o））
- `int GetHashCode()`
  （int 获取HashCode（））
- `string ToString()`
  （string To字符串（））
- `string ToString(string format, IFormatProvider formatProvider)`
  （string To字符串（string format, I格式化提供者 formatProvider））

---

## uint3.DebuggerProxy（uint3.Debugger代理）

### 字段 (3)

- `uint x`（uint x）(偏移: 0x8)
- `uint y`（uint y）(偏移: 0xC)
- `uint z`（uint z）(偏移: 0x10)

---

## uint4（uint4）

**继承**: IEquatable<uint4>, IFormattable（IEquatable<uint4>, IFormattable）

### 字段 (4)

- `uint x`（uint x）(偏移: 0x0)
- `uint y`（uint y）(偏移: 0x4)
- `uint z`（uint z）(偏移: 0x8)
- `uint w`（uint w）(偏移: 0xC)

### 方法 (6)

- `uint4 op_Multiply(uint4 lhs, uint4 rhs)`
  （uint4 op_Multiply（uint4 lhs, uint4 rhs））
- `bool Equals(uint4 rhs)`
  （bool Equals（uint4 rhs））
- `bool Equals(object o)`
  （bool Equals（object o））
- `int GetHashCode()`
  （int 获取HashCode（））
- `string ToString()`
  （string To字符串（））
- `string ToString(string format, IFormatProvider formatProvider)`
  （string To字符串（string format, I格式化提供者 formatProvider））

---

## uint4.DebuggerProxy（uint4.Debugger代理）

### 字段 (4)

- `uint x`（uint x）(偏移: 0x8)
- `uint y`（uint y）(偏移: 0xC)
- `uint z`（uint z）(偏移: 0x10)
- `uint w`（uint w）(偏移: 0x14)

---

## xxHash（xxHash）

### 方法 (1)

- `uint CalculateHash(byte[] buf, int len, uint seed)`
  （uint 计算Hash（byte[] buf, int len, uint seed））

---

