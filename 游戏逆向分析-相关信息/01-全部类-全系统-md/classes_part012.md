# 游戏类定义 (Part 12/21)

共 200 个类 (总序号 2201 - 2400)

---

## NestedExample（NestedExample）

### 字段 (4)

- `GameObject prefab`（游戏对象 预制体）(偏移: 0x8)
- `float speed`（浮点数 速度）(偏移: 0xC)
- `Color color`（颜色 color）(偏移: 0x10)
- `Nested2Dict deepNested`（Nested2Dict deepNested）(偏移: 0x20)

---

## NestedTweenFailureBehaviour（NestedTweenFailureBehaviour）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## NeutralResourcesLanguageAttribute（NeutralResourcesLanguageAttribute）

**继承**: Attribute（属性）

### 字段 (2)

- `string _culture`（string _culture）(偏移: 0x8)
- `UltimateResourceFallbackLocation _fallbackLoc`（Ultimate资源FallbackLocation _fallbackLoc）(偏移: 0xC)

### 方法 (2)

- `string get_CultureName()`
  （string get_Culture名称（））
- `UltimateResourceFallbackLocation get_Location()`
  （Ultimate资源FallbackLocation get_Location（））

---

## NoAllocHelpers（NoAllocHelpers）

### 方法 (3)

- `int SafeLength(Array values)`
  （int SafeLength（数组 values））
- `void Internal_ResizeList(object list, int size)`
  （void Internal_Resize列表（object list, int size））
- `Array ExtractArrayFromList(object list)`
  （数组 Extract数组From列表（object list））

---

## NoInterpClampedFloatParameter（NoInterpClamped浮点数Parameter）

**继承**: VolumeParameter<float>（VolumeParameter<float>）

### 字段 (2)

- `float min`（浮点数 最小值）(偏移: 0x10)
- `float max`（浮点数 最大值）(偏移: 0x14)

### 方法 (2)

- `float get_value()`
  （浮点数 获取_值（））
- `void set_value(float value)`
  （void 设置_值（浮点数 value））

---

## NoInterpClampedIntParameter（NoInterpClamped整数Parameter）

**继承**: VolumeParameter<int>（VolumeParameter<int>）

### 字段 (2)

- `int min`（整数 最小值）(偏移: 0x10)
- `int max`（整数 最大值）(偏移: 0x14)

### 方法 (2)

- `int get_value()`
  （整数 获取_值（））
- `void set_value(int value)`
  （void 设置_值（整数 value））

---

## NoInterpColorParameter（NoInterp颜色Parameter）

**继承**: VolumeParameter<Color>（VolumeParameter<Color>）

### 字段 (3)

- `bool hdr`（布尔值 hdr）(偏移: 0x1C)
- `bool showAlpha`（布尔值 显示透明度）(偏移: 0x1D)
- `bool showEyeDropper`（bool showEyeDropper）(偏移: 0x1E)

---

## NoInterpFloatRangeParameter（NoInterp浮点数范围Parameter）

**继承**: VolumeParameter<Vector2>（VolumeParameter<Vector2>）

### 字段 (2)

- `float min`（浮点数 最小值）(偏移: 0x14)
- `float max`（浮点数 最大值）(偏移: 0x18)

### 方法 (2)

- `Vector2 get_value()`
  （二维向量 get_value（））
- `void set_value(Vector2 value)`
  （void set_value（二维向量 value））

---

## NoInterpMaxFloatParameter（NoInterp最大浮点数Parameter）

**继承**: VolumeParameter<float>（VolumeParameter<float>）

### 字段 (1)

- `float max`（浮点数 最大值）(偏移: 0x10)

### 方法 (2)

- `float get_value()`
  （浮点数 获取_值（））
- `void set_value(float value)`
  （void 设置_值（浮点数 value））

---

## NoInterpMaxIntParameter（NoInterp最大整数Parameter）

**继承**: VolumeParameter<int>（VolumeParameter<int>）

### 字段 (1)

- `int max`（整数 最大值）(偏移: 0x10)

### 方法 (2)

- `int get_value()`
  （整数 获取_值（））
- `void set_value(int value)`
  （void 设置_值（整数 value））

---

## NoInterpMinFloatParameter（NoInterp最小浮点数Parameter）

**继承**: VolumeParameter<float>（VolumeParameter<float>）

### 字段 (1)

- `float min`（浮点数 最小值）(偏移: 0x10)

### 方法 (2)

- `float get_value()`
  （浮点数 获取_值（））
- `void set_value(float value)`
  （void 设置_值（浮点数 value））

---

## NoInterpMinIntParameter（NoInterp最小整数Parameter）

**继承**: VolumeParameter<int>（VolumeParameter<int>）

### 字段 (1)

- `int min`（整数 最小值）(偏移: 0x10)

### 方法 (2)

- `int get_value()`
  （整数 获取_值（））
- `void set_value(int value)`
  （void 设置_值（整数 value））

---

## NoOptions（NoOptions）

**继承**: IPlugOptions（I插件选项）

### 方法 (1)

- `void Reset()`
  （void 重置（））

---

## NodeLink（节点Link）

**继承**: GraphModifier（图修改器）

### 字段 (4)

- `Transform end`（变换 end）(偏移: 0x20)
- `float costFactor`（float cost系数）(偏移: 0x24)
- `bool oneWay`（bool oneWay）(偏移: 0x28)
- `bool deleteConnection`（bool delete连接）(偏移: 0x29)

### 方法 (7)

- `Transform get_Start()`
  （变换 get_开始（））
- `Transform get_End()`
  （变换 get_结束（））
- `void OnPostScan()`
  （void 扫描后（））
- `void InternalOnPostScan()`
  （void 内部的OnPostScan（））
- `void OnGraphsPostUpdate()`
  （void 图后更新时（））
- `void Apply()`
  （void 应用（））
- `void OnDrawGizmos()`
  （void 绘制辅助线时（））

---

## NodeLink2（节点Link2）

**继承**: GraphModifier（图修改器）

### 字段 (10)

- `Transform end`（变换 end）(偏移: 0x20)
- `float costFactor`（float cost系数）(偏移: 0x24)
- `bool oneWay`（bool oneWay）(偏移: 0x28)
- `GraphNode connectedNode1`（Graph节点 connectedNode1）(偏移: 0x34)
- `GraphNode connectedNode2`（Graph节点 connectedNode2）(偏移: 0x38)
- `Vector3 clamped1`（三维向量 clamped1）(偏移: 0x3C)
- `Vector3 clamped2`（三维向量 clamped2）(偏移: 0x48)
- `bool postScanCalled`（bool postScanCalled）(偏移: 0x54)
- `Color GizmosColor`（颜色 Gizmos颜色）(偏移: 0x4)
- `Color GizmosColorSelected`（颜色 Gizmos颜色选中的）(偏移: 0x14)

### 方法 (22)

- `NodeLink2 GetNodeLink(GraphNode node)`
  （节点Link2 获取节点Link（Graph节点 node））
- `Transform get_StartTransform()`
  （变换 get_开始变换（））
- `Transform get_EndTransform()`
  （变换 get_结束变换（））
- `PointNode get_startNode()`
  （Point节点 get_start节点（））
- `void set_startNode(PointNode value)`
  （void set_start节点（Point节点 value））
- `PointNode get_endNode()`
  （Point节点 get_end节点（））
- `void set_endNode(PointNode value)`
  （void set_end节点（Point节点 value））
- `GraphNode get_StartNode()`
  （Graph节点 get_开始节点（））
- `GraphNode get_EndNode()`
  （Graph节点 get_结束节点（））
- `void OnPostScan()`
  （void 扫描后（））
- `void InternalOnPostScan()`
  （void 内部的OnPostScan（））
- `void OnGraphsPostUpdate()`
  （void 图后更新时（））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `void RemoveConnections(GraphNode node)`
  （void 移除Connections（Graph节点 node））
- `void ContextApplyForce()`
  （void Context应用强制（））
- `void Apply(bool forceNewCheck)`
  （void 应用（bool forceNewCheck））
- `void OnDrawGizmosSelected()`
  （void 绘制选中辅助线时（））
- `void OnDrawGizmos()`
  （void 绘制辅助线时（））
- `void OnDrawGizmos(bool selected)`
  （void OnDrawGizmos（bool selected））
- `void SerializeReferences(GraphSerializationContext ctx)`
  （void 序列化引用（图序列化上下文 ctx））
- `void DeserializeReferences(GraphSerializationContext ctx)`
  （void 反序列化引用（图序列化上下文 ctx））

---

## NodeLink3（节点Link3）

**继承**: GraphModifier（图修改器）

### 字段 (12)

- `Transform end`（变换 end）(偏移: 0x20)
- `float costFactor`（float cost系数）(偏移: 0x24)
- `bool oneWay`（bool oneWay）(偏移: 0x28)
- `NodeLink3Node startNode`（节点Link3节点 start节点）(偏移: 0x2C)
- `NodeLink3Node endNode`（节点Link3节点 end节点）(偏移: 0x30)
- `MeshNode connectedNode1`（网格节点 connectedNode1）(偏移: 0x34)
- `MeshNode connectedNode2`（网格节点 connectedNode2）(偏移: 0x38)
- `Vector3 clamped1`（三维向量 clamped1）(偏移: 0x3C)
- `Vector3 clamped2`（三维向量 clamped2）(偏移: 0x48)
- `bool postScanCalled`（bool postScanCalled）(偏移: 0x54)
- `Color GizmosColor`（颜色 Gizmos颜色）(偏移: 0x4)
- `Color GizmosColorSelected`（颜色 Gizmos颜色选中的）(偏移: 0x14)

### 方法 (16)

- `NodeLink3 GetNodeLink(GraphNode node)`
  （节点Link3 获取节点Link（Graph节点 node））
- `Transform get_StartTransform()`
  （变换 get_开始变换（））
- `Transform get_EndTransform()`
  （变换 get_结束变换（））
- `GraphNode get_StartNode()`
  （Graph节点 get_开始节点（））
- `GraphNode get_EndNode()`
  （Graph节点 get_结束节点（））
- `void OnPostScan()`
  （void 扫描后（））
- `void InternalOnPostScan()`
  （void 内部的OnPostScan（））
- `void OnGraphsPostUpdate()`
  （void 图后更新时（））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `void RemoveConnections(GraphNode node)`
  （void 移除Connections（Graph节点 node））
- `void ContextApplyForce()`
  （void Context应用强制（））
- `void Apply(bool forceNewCheck)`
  （void 应用（bool forceNewCheck））
- `void OnDrawGizmosSelected()`
  （void 绘制选中辅助线时（））
- `void OnDrawGizmos()`
  （void 绘制辅助线时（））
- `void OnDrawGizmos(bool selected)`
  （void OnDrawGizmos（bool selected））

---

## NodeLink3Node（节点Link3节点）

**继承**: PointNode（Point节点）

### 字段 (3)

- `NodeLink3 link`（节点Link3 link）(偏移: 0x28)
- `Vector3 portalA`（三维向量 portalA）(偏移: 0x2C)
- `Vector3 portalB`（三维向量 portalB）(偏移: 0x38)

### 方法 (3)

- `bool GetPortal(GraphNode other, List<Vector3> left, List<Vector3> right, bool backwards)`
  （bool 获取Portal（Graph节点 other, List<Vector3> left, List<Vector3> right, bool backwards））
- `GraphNode GetOther(GraphNode a)`
  （Graph节点 获取Other（Graph节点 a））
- `GraphNode GetOtherInternal(GraphNode a)`
  （Graph节点 获取Other内部的（Graph节点 a））

---

## NoiseSettings（NoiseSettings）

**继承**: SignalSourceAsset（信号Source资产）

### 字段 (2)

- `NoiseSettings.TransformNoiseParams[] PositionNoise`（NoiseSettings.变换NoiseParams[] PositionNoise）(偏移: 0xC)
- `NoiseSettings.TransformNoiseParams[] OrientationNoise`（NoiseSettings.变换NoiseParams[] OrientationNoise）(偏移: 0x10)

### 方法 (3)

- `Vector3 GetCombinedFilterResults(NoiseSettings.TransformNoiseParams[] noiseParams, float time, Vector3 timeOffsets)`
  （三维向量 获取CombinedFilterResults（NoiseSettings.变换NoiseParams[] noiseParams, float time, 三维向量 timeOffsets））
- `float get_SignalDuration()`
  （float get_信号持续时间（））
- `void GetSignal(float timeSinceSignalStart, out Vector3 pos, out Quaternion rot)`
  （void 获取信号（float timeSinceSignalStart, out Vector3 pos, out Quaternion rot））

---

## NoiseSettings.NoiseParams（NoiseSettings.NoiseParams）

### 字段 (3)

- `float Frequency`（float Frequency）(偏移: 0x0)
- `float Amplitude`（float Amplitude）(偏移: 0x4)
- `bool Constant`（bool Constant）(偏移: 0x8)

### 方法 (1)

- `float GetValueAt(float time, float timeOffset)`
  （float 获取值At（float time, float timeOffset））

---

## NoiseSettings.TransformNoiseParams（NoiseSettings.变换NoiseParams）

### 字段 (3)

- `NoiseSettings.NoiseParams X`（NoiseSettings.NoiseParams X）(偏移: 0x0)
- `NoiseSettings.NoiseParams Y`（NoiseSettings.NoiseParams Y）(偏移: 0xC)
- `NoiseSettings.NoiseParams Z`（NoiseSettings.NoiseParams Z）(偏移: 0x18)

### 方法 (1)

- `Vector3 GetValueAt(float time, Vector3 timeOffsets)`
  （三维向量 获取值At（float time, 三维向量 timeOffsets））

---

## Normalization（Normalization）

### 字段 (8)

- `byte* props`（byte* props）(偏移: 0x0)
- `int* mappedChars`（int* mappedChars）(偏移: 0x4)
- `short* charMapIndex`（short* char映射索引）(偏移: 0x8)
- `short* helperIndex`（short* helper索引）(偏移: 0xC)
- `ushort* mapIdxToComposite`（ushort* mapIdxToComposite）(偏移: 0x10)
- `byte* combiningClass`（byte* combining类）(偏移: 0x14)
- `object forLock`（object forLock）(偏移: 0x18)
- `bool isReady`（bool isReady）(偏移: 0x1C)

### 方法 (22)

- `uint PropValue(int cp)`
  （uint Prop值（int cp））
- `int CharMapIdx(int cp)`
  （int Char映射Idx（int cp））
- `byte GetCombiningClass(int c)`
  （byte 获取Combining类（int c））
- `int GetPrimaryCompositeFromMapIndex(int src)`
  （int 获取PrimaryCompositeFrom映射索引（int src））
- `int GetPrimaryCompositeHelperIndex(int cp)`
  （int 获取PrimaryComposite辅助器索引（int cp））
- `string Compose(string source, int checkType)`
  （string Compose（string source, int checkType））
- `StringBuilder Combine(string source, int start, int checkType)`
  （字符串构建器 Combine（string source, int start, int checkType））
- `void Combine(StringBuilder sb, int i, int checkType)`
  （void Combine（字符串构建器 sb, int i, int checkType））
- `int CombineHangul(StringBuilder sb, string s, int current)`
  （int CombineHangul（字符串构建器 sb, string s, int current））
- `int Fetch(StringBuilder sb, string s, int i)`
  （int Fetch（字符串构建器 sb, string s, int i））
- `int TryComposeWithPreviousStarter(StringBuilder sb, string s, int current)`
  （int TryComposeWith上一个Starter（字符串构建器 sb, string s, int current））
- `int TryCompose(int i, int starter, int candidate)`
  （int TryCompose（int i, int starter, int candidate））
- `string Decompose(string source, int checkType)`
  （string Decompose（string source, int checkType））
- `void Decompose(string source, ref StringBuilder sb, int checkType)`
  （void Decompose（string source, ref StringBuilder sb, int checkType））
- `void ReorderCanonical(string src, ref StringBuilder sb, int start)`
  （void ReorderCanonical（string src, ref StringBuilder sb, int start））
- `void DecomposeChar(ref StringBuilder sb, ref int[] buf, string s, int i, int checkType, ref int start)`
  （void DecomposeChar（ref StringBuilder sb, ref int[] buf, string s, int i, int checkType, ref int start））
- `NormalizationCheck QuickCheck(char c, int type)`
  （Normalization检查 Quick检查（char c, int type））
- `int GetCanonicalHangul(int s, int[] buf, int bufIdx)`
  （int 获取CanonicalHangul（int s, int[] buf, int bufIdx））
- `int GetCanonical(int c, int[] buf, int bufIdx, int checkType)`
  （int 获取Canonical（int c, int[] buf, int bufIdx, int checkType））
- `string Normalize(string source, NormalizationForm normalizationForm)`
  （string Normalize（string source, NormalizationForm normalizationForm））
- `string Normalize(string source, int type)`
  （string Normalize（string source, int type））
- `void load_normalization_resource(out IntPtr props, out IntPtr mappedChars, out IntPtr charMapIndex, out IntPtr helperIndex, out IntPtr mapIdxToComposite, out IntPtr combiningClass)`
  （void load_normalization_resource（out IntPtr props, out IntPtr mappedChars, out IntPtr charMapIndex, out IntPtr helperIndex, out IntPtr mapIdxToComposite, out IntPtr combiningClass））

---

## NormalizationCheck（Normalization检查）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## NormalizationForm（NormalizationForm）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## NormalizationTableUtil（NormalizationTableUtil）

### 字段 (5)

- `CodePointIndexer Prop`（CodePointIndexer Prop）(偏移: 0x0)
- `CodePointIndexer Map`（CodePointIndexer 映射）(偏移: 0x4)
- `CodePointIndexer Combining`（CodePointIndexer Combining）(偏移: 0x8)
- `CodePointIndexer Composite`（CodePointIndexer Composite）(偏移: 0xC)
- `CodePointIndexer Helper`（CodePointIndexer 辅助器）(偏移: 0x10)

### 方法 (2)

- `int PropIdx(int cp)`
  （int PropIdx（int cp））
- `int MapIdx(int cp)`
  （int 映射Idx（int cp））

---

## NotNullAttribute（NotNullAttribute）

**继承**: Attribute（属性）

### 方法 (1)

- `void set_Exception(string value)`
  （void set_Exception（string value））

---

## NotificationFlags（NotificationFlags）

### 字段 (1)

- `short value__`（short value__）(偏移: 0x0)

---

## NotificationUtilities（NotificationUtilities）

### 方法 (2)

- `ScriptPlayable<TimeNotificationBehaviour> CreateNotificationsPlayable(PlayableGraph graph, IEnumerable<IMarker> markers, GameObject go)`
  （ScriptPlayable<时间NotificationBehaviour> 创建NotificationsPlayable（PlayableGraph graph, IEnumerable<IMarker> markers, 游戏对象 go））
- `bool TrackTypeSupportsNotifications(Type type)`
  （bool Track类型SupportsNotifications（类型 type））

---

## NullConsoleDriver（NullConsoleDriver）

**继承**: IConsoleDriver（IConsoleDriver）

### 字段 (1)

- `ConsoleKeyInfo EmptyConsoleKeyInfo`（Console键信息 空Console键信息）(偏移: 0x0)

### 方法 (1)

- `ConsoleKeyInfo ReadKey(bool intercept)`
  （控制台键信息 读取键（布尔值 拦截））

---

## Nullable（Nullable）

### 方法 (1)

- `Type GetUnderlyingType(Type nullableType)`
  （类型 获取Underlying类型（类型 nullableType））

---

## NumNeighbours（NumNeighbours）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Number（Number）

### 方法 (39)

- `bool NumberBufferToDecimal(byte* number, ref Decimal value)`
  （bool Number缓冲区ToDecimal（byte* number, ref Decimal value））
- `bool NumberBufferToDouble(byte* number, ref double value)`
  （bool Number缓冲区ToDouble（byte* number, ref double value））
- `string FormatDecimal(Decimal value, string format, NumberFormatInfo info)`
  （string 格式化Decimal（Decimal value, string format, Number格式化信息 info））
- `string FormatDouble(double value, string format, NumberFormatInfo info)`
  （string 格式化Double（double value, string format, Number格式化信息 info））
- `string FormatInt32(int value, string format, NumberFormatInfo info)`
  （string 格式化Int32（int value, string format, Number格式化信息 info））
- `string FormatUInt32(uint value, string format, NumberFormatInfo info)`
  （string 格式化UInt32（uint value, string format, Number格式化信息 info））
- `string FormatInt64(long value, string format, NumberFormatInfo info)`
  （string 格式化Int64（long value, string format, Number格式化信息 info））
- `string FormatUInt64(ulong value, string format, NumberFormatInfo info)`
  （string 格式化UInt64（ulong value, string format, Number格式化信息 info））
- `string FormatSingle(float value, string format, NumberFormatInfo info)`
  （string 格式化单个（float value, string format, Number格式化信息 info））
- `bool HexNumberToInt32(ref Number.NumberBuffer number, ref int value)`
  （bool HexNumberToInt32（ref Number.NumberBuffer number, ref int value））
- `bool HexNumberToInt64(ref Number.NumberBuffer number, ref long value)`
  （bool HexNumberToInt64（ref Number.NumberBuffer number, ref long value））
- `bool HexNumberToUInt32(ref Number.NumberBuffer number, ref uint value)`
  （bool HexNumberToUInt32（ref Number.NumberBuffer number, ref uint value））
- `bool HexNumberToUInt64(ref Number.NumberBuffer number, ref ulong value)`
  （bool HexNumberToUInt64（ref Number.NumberBuffer number, ref ulong value））
- `bool IsWhite(char ch)`
  （bool 是否White（char ch））
- `bool NumberToInt32(ref Number.NumberBuffer number, ref int value)`
  （bool NumberToInt32（ref Number.NumberBuffer number, ref int value））
- `bool NumberToInt64(ref Number.NumberBuffer number, ref long value)`
  （bool NumberToInt64（ref Number.NumberBuffer number, ref long value））
- `bool NumberToUInt32(ref Number.NumberBuffer number, ref uint value)`
  （bool NumberToUInt32（ref Number.NumberBuffer number, ref uint value））
- `bool NumberToUInt64(ref Number.NumberBuffer number, ref ulong value)`
  （bool NumberToUInt64（ref Number.NumberBuffer number, ref ulong value））
- `char* MatchChars(char* p, string str)`
  （char* 比赛Chars（char* p, string str））
- `char* MatchChars(char* p, char* str)`
  （char* 比赛Chars（char* p, char* str））
- `Decimal ParseDecimal(string value, NumberStyles options, NumberFormatInfo numfmt)`
  （Decimal 解析Decimal（string value, NumberStyles options, Number格式化信息 numfmt））
- `double ParseDouble(string value, NumberStyles options, NumberFormatInfo numfmt)`
  （double 解析Double（string value, NumberStyles options, Number格式化信息 numfmt））
- `int ParseInt32(string s, NumberStyles style, NumberFormatInfo info)`
  （int 解析Int32（string s, NumberStyles style, Number格式化信息 info））
- `long ParseInt64(string value, NumberStyles options, NumberFormatInfo numfmt)`
  （long 解析Int64（string value, NumberStyles options, Number格式化信息 numfmt））
- `bool ParseNumber(ref char* str, NumberStyles options, ref Number.NumberBuffer number, StringBuilder sb, NumberFormatInfo numfmt, bool parseDecimal)`
  （bool 解析Number（ref char* str, NumberStyles options, ref Number.NumberBuffer number, 字符串构建器 sb, Number格式化信息 numfmt, bool parseDecimal））
- `float ParseSingle(string value, NumberStyles options, NumberFormatInfo numfmt)`
  （float 解析单个（string value, NumberStyles options, Number格式化信息 numfmt））
- `uint ParseUInt32(string value, NumberStyles options, NumberFormatInfo numfmt)`
  （uint 解析UInt32（string value, NumberStyles options, Number格式化信息 numfmt））
- `ulong ParseUInt64(string value, NumberStyles options, NumberFormatInfo numfmt)`
  （ulong 解析UInt64（string value, NumberStyles options, Number格式化信息 numfmt））
- `void StringToNumber(string str, NumberStyles options, ref Number.NumberBuffer number, NumberFormatInfo info, bool parseDecimal)`
  （void 字符串ToNumber（string str, NumberStyles options, ref Number.NumberBuffer number, Number格式化信息 info, bool parseDecimal））
- `bool TrailingZeros(string s, int index)`
  （bool TrailingZeros（string s, int index））
- `bool TryParseDecimal(string value, NumberStyles options, NumberFormatInfo numfmt, out Decimal result)`
  （bool Try解析Decimal（string value, NumberStyles options, Number格式化信息 numfmt, out Decimal result））
- `bool TryParseDouble(string value, NumberStyles options, NumberFormatInfo numfmt, out double result)`
  （bool Try解析Double（string value, NumberStyles options, Number格式化信息 numfmt, out double result））
- `bool TryParseInt32(string s, NumberStyles style, NumberFormatInfo info, out int result)`
  （bool Try解析Int32（string s, NumberStyles style, Number格式化信息 info, out int result））
- `bool TryParseInt64(string s, NumberStyles style, NumberFormatInfo info, out long result)`
  （bool Try解析Int64（string s, NumberStyles style, Number格式化信息 info, out long result））
- `bool TryParseSingle(string value, NumberStyles options, NumberFormatInfo numfmt, out float result)`
  （bool Try解析单个（string value, NumberStyles options, Number格式化信息 numfmt, out float result））
- `bool TryParseUInt32(string s, NumberStyles style, NumberFormatInfo info, out uint result)`
  （bool Try解析UInt32（string s, NumberStyles style, Number格式化信息 info, out uint result））
- `bool TryParseUInt64(string s, NumberStyles style, NumberFormatInfo info, out ulong result)`
  （bool Try解析UInt64（string s, NumberStyles style, Number格式化信息 info, out ulong result））
- `bool TryStringToNumber(string str, NumberStyles options, ref Number.NumberBuffer number, NumberFormatInfo numfmt, bool parseDecimal)`
  （bool Try字符串ToNumber（string str, NumberStyles options, ref Number.NumberBuffer number, Number格式化信息 numfmt, bool parseDecimal））
- `bool TryStringToNumber(string str, NumberStyles options, ref Number.NumberBuffer number, StringBuilder sb, NumberFormatInfo numfmt, bool parseDecimal)`
  （bool Try字符串ToNumber（string str, NumberStyles options, ref Number.NumberBuffer number, 字符串构建器 sb, Number格式化信息 numfmt, bool parseDecimal））

---

## Number.NumberBuffer（Number.Number缓冲区）

### 字段 (6)

- `int NumberBufferBytes`（int Number缓冲区Bytes）(偏移: 0x0)
- `byte* baseAddress`（byte* baseAddress）(偏移: 0x0)
- `char* digits`（char* digits）(偏移: 0x4)
- `int precision`（int precision）(偏移: 0x8)
- `int scale`（int scale）(偏移: 0xC)
- `bool sign`（bool sign）(偏移: 0x10)

### 方法 (1)

- `byte* PackForNative()`
  （byte* PackForNative（））

---

## NumberFormatInfo（Number格式化信息）

**继承**: ICloneable, IFormatProvider（ICloneable, I格式化提供者）

### 字段 (35)

- `NumberFormatInfo invariantInfo`（Number格式化信息 invariant信息）(偏移: 0x0)
- `int[] numberGroupSizes`（int[] number组Sizes）(偏移: 0x8)
- `int[] currencyGroupSizes`（int[] currency组Sizes）(偏移: 0xC)
- `int[] percentGroupSizes`（int[] percent组Sizes）(偏移: 0x10)
- `string positiveSign`（string positive标志）(偏移: 0x14)
- `string negativeSign`（string negative标志）(偏移: 0x18)
- `string numberDecimalSeparator`（string numberDecimalSeparator）(偏移: 0x1C)
- `string numberGroupSeparator`（string number组Separator）(偏移: 0x20)
- `string currencyGroupSeparator`（string currency组Separator）(偏移: 0x24)
- `string currencyDecimalSeparator`（string currencyDecimalSeparator）(偏移: 0x28)
- `string currencySymbol`（string currencySymbol）(偏移: 0x2C)
- `string ansiCurrencySymbol`（string ansi货币Symbol）(偏移: 0x30)
- `string nanSymbol`（string nanSymbol）(偏移: 0x34)
- `string positiveInfinitySymbol`（string positive无限Symbol）(偏移: 0x38)
- `string negativeInfinitySymbol`（string negative无限Symbol）(偏移: 0x3C)
- `string percentDecimalSeparator`（string percentDecimalSeparator）(偏移: 0x40)
- `string percentGroupSeparator`（string percent组Separator）(偏移: 0x44)
- `string percentSymbol`（string percentSymbol）(偏移: 0x48)
- `string perMilleSymbol`（string perMilleSymbol）(偏移: 0x4C)
- `string[] nativeDigits`（string[] nativeDigits）(偏移: 0x50)
- `int m_dataItem`（int m_data项目）(偏移: 0x54)
- `int numberDecimalDigits`（int numberDecimalDigits）(偏移: 0x58)
- `int currencyDecimalDigits`（int currencyDecimalDigits）(偏移: 0x5C)
- `int currencyPositivePattern`（int currencyPositivePattern）(偏移: 0x60)
- `int currencyNegativePattern`（int currencyNegativePattern）(偏移: 0x64)
- `int numberNegativePattern`（int numberNegativePattern）(偏移: 0x68)
- `int percentPositivePattern`（int percentPositivePattern）(偏移: 0x6C)
- `int percentNegativePattern`（int percentNegativePattern）(偏移: 0x70)
- `int percentDecimalDigits`（int percentDecimalDigits）(偏移: 0x74)
- `int digitSubstitution`（int digitSubstitution）(偏移: 0x78)
- `bool isReadOnly`（bool isReadOnly）(偏移: 0x7C)
- `bool m_useUserOverride`（bool m_useUser重写）(偏移: 0x0)
- `bool m_isInvariant`（bool m_isInvariant）(偏移: 0x0)
- `bool validForParseAsNumber`（bool validFor解析AsNumber）(偏移: 0x0)
- `bool validForParseAsCurrency`（bool validFor解析As货币）(偏移: 0x0)

### 方法 (37)

- `void OnSerializing(StreamingContext ctx)`
  （void 序列化中（流上下文 ctx））
- `void OnDeserializing(StreamingContext ctx)`
  （void 反序列化中（流上下文 ctx））
- `void OnDeserialized(StreamingContext ctx)`
  （void 反序列化后（流上下文 ctx））
- `NumberFormatInfo get_InvariantInfo()`
  （Number格式化信息 get_Invariant信息（））
- `NumberFormatInfo GetInstance(IFormatProvider formatProvider)`
  （Number格式化信息 获取实例（I格式化提供者 formatProvider））
- `object Clone()`
  （对象 克隆（））
- `int get_CurrencyDecimalDigits()`
  （int get_货币DecimalDigits（））
- `string get_CurrencyDecimalSeparator()`
  （string get_货币DecimalSeparator（））
- `bool get_IsReadOnly()`
  （布尔值 获取_是否只读（））
- `int[] get_CurrencyGroupSizes()`
  （int[] get_货币组Sizes（））
- `int[] get_NumberGroupSizes()`
  （int[] get_Number组Sizes（））
- `int[] get_PercentGroupSizes()`
  （int[] get_Percent组Sizes（））
- `string get_CurrencyGroupSeparator()`
  （string get_货币组Separator（））
- `string get_CurrencySymbol()`
  （string get_货币Symbol（））
- `NumberFormatInfo get_CurrentInfo()`
  （Number格式化信息 get_当前信息（））
- `string get_NaNSymbol()`
  （string get_NaNSymbol（））
- `int get_CurrencyNegativePattern()`
  （int get_货币NegativePattern（））
- `int get_NumberNegativePattern()`
  （int get_NumberNegativePattern（））
- `int get_PercentPositivePattern()`
  （int get_PercentPositivePattern（））
- `int get_PercentNegativePattern()`
  （int get_PercentNegativePattern（））
- `string get_NegativeInfinitySymbol()`
  （string get_Negative无限Symbol（））
- `string get_NegativeSign()`
  （string get_Negative标志（））
- `int get_NumberDecimalDigits()`
  （int get_NumberDecimalDigits（））
- `string get_NumberDecimalSeparator()`
  （string get_NumberDecimalSeparator（））
- `string get_NumberGroupSeparator()`
  （string get_Number组Separator（））
- `int get_CurrencyPositivePattern()`
  （int get_货币PositivePattern（））
- `string get_PositiveInfinitySymbol()`
  （string get_Positive无限Symbol（））
- `string get_PositiveSign()`
  （string get_Positive标志（））
- `int get_PercentDecimalDigits()`
  （int get_PercentDecimalDigits（））
- `string get_PercentDecimalSeparator()`
  （string get_PercentDecimalSeparator（））
- `string get_PercentGroupSeparator()`
  （string get_Percent组Separator（））
- `string get_PercentSymbol()`
  （string get_PercentSymbol（））
- `string get_PerMilleSymbol()`
  （string get_PerMilleSymbol（））
- `object GetFormat(Type formatType)`
  （object 获取格式化（类型 formatType））
- `NumberFormatInfo ReadOnly(NumberFormatInfo nfi)`
  （Number格式化信息 ReadOnly（Number格式化信息 nfi））
- `void ValidateParseStyleInteger(NumberStyles style)`
  （void 验证解析StyleInteger（NumberStyles style））
- `void ValidateParseStyleFloatingPoint(NumberStyles style)`
  （void 验证解析Style浮空Point（NumberStyles style））

---

## NumberFormatter（NumberFormatter）

### 字段 (26)

- `ulong* MantissaBitsTable`（ulong* MantissaBitsTable）(偏移: 0x0)
- `int* TensExponentTable`（int* TensExponentTable）(偏移: 0x4)
- `char* DigitLowerTable`（char* Digit下半身Table）(偏移: 0x8)
- `char* DigitUpperTable`（char* Digit上半身Table）(偏移: 0xC)
- `long* TenPowersList`（long* TenPowers列表）(偏移: 0x10)
- `int* DecHexDigits`（int* DecHexDigits）(偏移: 0x14)
- `NumberFormatInfo _nfi`（Number格式化信息 _nfi）(偏移: 0x8)
- `char[] _cbuf`（char[] _cbuf）(偏移: 0xC)
- `bool _NaN`（bool _NaN）(偏移: 0x10)
- `bool _infinity`（bool _infinity）(偏移: 0x0)
- `bool _isCustomFormat`（bool _is自定义的格式化）(偏移: 0x0)
- `bool _specifierIsUpper`（bool _specifier是否上半身）(偏移: 0x0)
- `bool _positive`（bool _positive）(偏移: 0x0)
- `char _specifier`（char _specifier）(偏移: 0x16)
- `int _precision`（int _precision）(偏移: 0x18)
- `int _defPrecision`（int _defPrecision）(偏移: 0x1C)
- `int _digitsLen`（int _digitsLen）(偏移: 0x20)
- `int _offset`（int _offset）(偏移: 0x24)
- `int _decPointPos`（int _decPointPos）(偏移: 0x28)
- `uint _val1`（uint _val1）(偏移: 0x2C)
- `uint _val2`（uint _val2）(偏移: 0x30)
- `uint _val3`（uint _val3）(偏移: 0x34)
- `uint _val4`（uint _val4）(偏移: 0x38)
- `int _ind`（int _ind）(偏移: 0x3C)
- `NumberFormatter threadNumberFormatter`（NumberFormatter threadNumberFormatter）(偏移: 0x80000000)
- `NumberFormatter userFormatProvider`（NumberFormatter user格式化提供者）(偏移: 0x80000004)

### 方法 (79)

- `void GetFormatterTables(out ulong* MantissaBitsTable, out int* TensExponentTable, out char* DigitLowerTable, out char* DigitUpperTable, out long* TenPowersList, out int* DecHexDigits)`
  （void 获取FormatterTables（out ulong* MantissaBitsTable, out int* TensExponentTable, out char* DigitLowerTable, out char* DigitUpperTable, out long* TenPowersList, out int* DecHexDigits））
- `long GetTenPowerOf(int i)`
  （long 获取Ten力度Of（int i））
- `void InitDecHexDigits(uint value)`
  （void 初始化DecHexDigits（uint value））
- `void InitDecHexDigits(ulong value)`
  （void 初始化DecHexDigits（ulong value））
- `void InitDecHexDigits(uint hi, ulong lo)`
  （void 初始化DecHexDigits（uint hi, ulong lo））
- `uint FastToDecHex(int val)`
  （uint FastToDecHex（int val））
- `uint ToDecHex(int val)`
  （uint ToDecHex（int val））
- `int FastDecHexLen(int val)`
  （int FastDecHexLen（int val））
- `int DecHexLen(uint val)`
  （int DecHexLen（uint val））
- `int DecHexLen()`
  （int DecHexLen（））
- `int ScaleOrder(long hi)`
  （int 缩放Order（long hi））
- `int InitialFloatingPrecision()`
  （int Initial浮空Precision（））
- `int ParsePrecision(string format)`
  （int 解析Precision（string format））
- `void Init(string format)`
  （void 初始化（string format））
- `void InitHex(ulong value)`
  （void 初始化Hex（ulong value））
- `void Init(string format, int value, int defPrecision)`
  （void 初始化（string format, int value, int defPrecision））
- `void Init(string format, uint value, int defPrecision)`
  （void 初始化（string format, uint value, int defPrecision））
- `void Init(string format, long value)`
  （void 初始化（string format, long value））
- `void Init(string format, ulong value)`
  （void 初始化（string format, ulong value））
- `void Init(string format, double value, int defPrecision)`
  （void 初始化（string format, double value, int defPrecision））
- `void Init(string format, Decimal value)`
  （void 初始化（string format, Decimal value））
- `void ResetCharBuf(int size)`
  （void 重置CharBuf（int size））
- `void Resize(int len)`
  （void Resize（int len））
- `void Append(char c)`
  （void Append（char c））
- `void Append(char c, int cnt)`
  （void Append（char c, int cnt））
- `void Append(string s)`
  （void Append（string s））
- `NumberFormatInfo GetNumberFormatInstance(IFormatProvider fp)`
  （Number格式化信息 获取Number格式化实例（I格式化提供者 fp））
- `void set_CurrentCulture(CultureInfo value)`
  （void set_当前Culture（Culture信息 value））
- `int get_IntegerDigits()`
  （int get_IntegerDigits（））
- `int get_DecimalDigits()`
  （int get_DecimalDigits（））
- `bool get_IsFloatingSource()`
  （bool get_是否浮空Source（））
- `bool get_IsZero()`
  （bool get_是否Zero（））
- `bool get_IsZeroInteger()`
  （bool get_是否ZeroInteger（））
- `void RoundPos(int pos)`
  （void 回合Pos（int pos））
- `bool RoundDecimal(int decimals)`
  （bool 回合Decimal（int decimals））
- `bool RoundBits(int shift)`
  （bool 回合Bits（int shift））
- `void RemoveTrailingZeros()`
  （void 移除TrailingZeros（））
- `void AddOneToDecHex()`
  （void 添加OneToDecHex（））
- `uint AddOneToDecHex(uint val)`
  （uint 添加OneToDecHex（uint val））
- `int CountTrailingZeros()`
  （int 数量TrailingZeros（））
- `int CountTrailingZeros(uint val)`
  （int 数量TrailingZeros（uint val））
- `NumberFormatter GetInstance(IFormatProvider fp)`
  （NumberFormatter 获取实例（I格式化提供者 fp））
- `void Release()`
  （void 释放（））
- `string NumberToString(string format, uint value, IFormatProvider fp)`
  （string NumberTo字符串（string format, uint value, I格式化提供者 fp））
- `string NumberToString(string format, int value, IFormatProvider fp)`
  （string NumberTo字符串（string format, int value, I格式化提供者 fp））
- `string NumberToString(string format, ulong value, IFormatProvider fp)`
  （string NumberTo字符串（string format, ulong value, I格式化提供者 fp））
- `string NumberToString(string format, long value, IFormatProvider fp)`
  （string NumberTo字符串（string format, long value, I格式化提供者 fp））
- `string NumberToString(string format, float value, IFormatProvider fp)`
  （string NumberTo字符串（string format, float value, I格式化提供者 fp））
- `string NumberToString(string format, double value, IFormatProvider fp)`
  （string NumberTo字符串（string format, double value, I格式化提供者 fp））
- `string NumberToString(string format, Decimal value, IFormatProvider fp)`
  （string NumberTo字符串（string format, Decimal value, I格式化提供者 fp））
- `string IntegerToString(string format, IFormatProvider fp)`
  （string IntegerTo字符串（string format, I格式化提供者 fp））
- `string NumberToString(string format, NumberFormatInfo nfi)`
  （string NumberTo字符串（string format, Number格式化信息 nfi））
- `string FormatCurrency(int precision, NumberFormatInfo nfi)`
  （string 格式化货币（int precision, Number格式化信息 nfi））
- `string FormatDecimal(int precision, NumberFormatInfo nfi)`
  （string 格式化Decimal（int precision, Number格式化信息 nfi））
- `string FormatHexadecimal(int precision)`
  （string 格式化Hexadecimal（int precision））
- `string FormatFixedPoint(int precision, NumberFormatInfo nfi)`
  （string 格式化固定Point（int precision, Number格式化信息 nfi））
- `string FormatRoundtrip(double origval, NumberFormatInfo nfi)`
  （string 格式化Roundtrip（double origval, Number格式化信息 nfi））
- `string FormatRoundtrip(float origval, NumberFormatInfo nfi)`
  （string 格式化Roundtrip（float origval, Number格式化信息 nfi））
- `string FormatGeneral(int precision, NumberFormatInfo nfi)`
  （string 格式化General（int precision, Number格式化信息 nfi））
- `string FormatNumber(int precision, NumberFormatInfo nfi)`
  （string 格式化Number（int precision, Number格式化信息 nfi））
- `string FormatPercent(int precision, NumberFormatInfo nfi)`
  （string 格式化Percent（int precision, Number格式化信息 nfi））
- `string FormatExponential(int precision, NumberFormatInfo nfi)`
  （string 格式化Exponential（int precision, Number格式化信息 nfi））
- `string FormatExponential(int precision, NumberFormatInfo nfi, int expDigits)`
  （string 格式化Exponential（int precision, Number格式化信息 nfi, int expDigits））
- `string FormatCustom(string format, NumberFormatInfo nfi)`
  （string 格式化自定义的（string format, Number格式化信息 nfi））
- `void ZeroTrimEnd(StringBuilder sb, bool canEmpty)`
  （void ZeroTrim结束（字符串构建器 sb, bool canEmpty））
- `bool IsZeroOnly(StringBuilder sb)`
  （bool 是否ZeroOnly（字符串构建器 sb））
- `void AppendNonNegativeNumber(StringBuilder sb, int v)`
  （void AppendNonNegativeNumber（字符串构建器 sb, int v））
- `void AppendIntegerString(int minLength, StringBuilder sb)`
  （void AppendInteger字符串（int minLength, 字符串构建器 sb））
- `void AppendIntegerString(int minLength)`
  （void AppendInteger字符串（int minLength））
- `void AppendDecimalString(int precision, StringBuilder sb)`
  （void AppendDecimal字符串（int precision, 字符串构建器 sb））
- `void AppendDecimalString(int precision)`
  （void AppendDecimal字符串（int precision））
- `void AppendIntegerStringWithGroupSeparator(int[] groups, string groupSeparator)`
  （void AppendInteger字符串With组Separator（int[] groups, string groupSeparator））
- `void AppendExponent(NumberFormatInfo nfi, int exponent, int minDigits)`
  （void AppendExponent（Number格式化信息 nfi, int exponent, int minDigits））
- `void AppendOneDigit(int start)`
  （void AppendOneDigit（int start））
- `void AppendDigits(int start, int end)`
  （void AppendDigits（int start, int end））
- `void AppendDigits(int start, int end, StringBuilder sb)`
  （void AppendDigits（int start, int end, 字符串构建器 sb））
- `void Multiply10(int count)`
  （void Multiply10（int count））
- `void Divide10(int count)`
  （void Divide10（int count））
- `NumberFormatter GetClone()`
  （NumberFormatter 获取克隆（））

---

## NumberFormatter.CustomInfo（NumberFormatter.自定义的信息）

### 字段 (14)

- `bool UseGroup`（bool Use组）(偏移: 0x8)
- `int DecimalDigits`（int DecimalDigits）(偏移: 0xC)
- `int DecimalPointPos`（int DecimalPointPos）(偏移: 0x10)
- `int DecimalTailSharpDigits`（int DecimalTailSharpDigits）(偏移: 0x14)
- `int IntegerDigits`（int IntegerDigits）(偏移: 0x18)
- `int IntegerHeadSharpDigits`（int Integer头部SharpDigits）(偏移: 0x1C)
- `int IntegerHeadPos`（int Integer头部Pos）(偏移: 0x20)
- `bool UseExponent`（bool UseExponent）(偏移: 0x24)
- `int ExponentDigits`（int ExponentDigits）(偏移: 0x28)
- `int ExponentTailSharpDigits`（int ExponentTailSharpDigits）(偏移: 0x2C)
- `bool ExponentNegativeSignOnly`（bool ExponentNegative标志Only）(偏移: 0x30)
- `int DividePlaces`（int DividePlaces）(偏移: 0x34)
- `int Percents`（int Percents）(偏移: 0x38)
- `int Permilles`（int Permilles）(偏移: 0x3C)

### 方法 (3)

- `void GetActiveSection(string format, ref bool positive, bool zero, ref int offset, ref int length)`
  （void 获取激活的Section（string format, ref bool positive, bool zero, ref int offset, ref int length））
- `NumberFormatter.CustomInfo Parse(string format, int offset, int length, NumberFormatInfo nfi)`
  （NumberFormatter.自定义的信息 解析（string format, int offset, int length, Number格式化信息 nfi））
- `string Format(string format, int offset, int length, NumberFormatInfo nfi, bool positive, StringBuilder sb_int, StringBuilder sb_dec, StringBuilder sb_exp)`
  （string 格式化（string format, int offset, int length, Number格式化信息 nfi, bool positive, 字符串构建器 sb_int, 字符串构建器 sb_dec, 字符串构建器 sb_exp））

---

## NumberStyles（NumberStyles）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## OSSpecificSynchronizationContext（OSSpecificSynchronizationContext）

**继承**: SynchronizationContext（SynchronizationContext）

### 字段 (1)

- `object m_OSSynchronizationContext`（object m_OSSynchronizationContext）(偏移: 0xC)

### 方法 (7)

- `OSSpecificSynchronizationContext Get()`
  （OSSpecificSynchronizationContext 获取（））
- `SynchronizationContext CreateCopy()`
  （SynchronizationContext 创建复制（））
- `void Send(SendOrPostCallback d, object state)`
  （void 发送（发送OrPost回调 d, object state））
- `void Post(SendOrPostCallback d, object state)`
  （void Post（发送OrPost回调 d, object state））
- `void InvocationEntry(IntPtr arg)`
  （void InvocationEntry（整数Ptr arg））
- `object GetOSContext()`
  （object 获取OSContext（））
- `void PostInternal(object osSynchronizationContext, IntPtr callback, IntPtr arg)`
  （void Post内部的（object osSynchronizationContext, 整数Ptr callback, 整数Ptr arg））

---

## OSSpecificSynchronizationContext.InvocationContext（OSSpecificSynchronizationContext.InvocationContext）

### 字段 (2)

- `SendOrPostCallback m_Delegate`（发送OrPost回调 m_委托）(偏移: 0x8)
- `object m_State`（object m_状态）(偏移: 0xC)

### 方法 (1)

- `void Invoke()`
  （void 调用（））

---

## OSSpecificSynchronizationContext.InvocationEntryDelegate（OSSpecificSynchronizationContext.InvocationEntry委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(IntPtr arg)`
  （void Invoke（整数Ptr arg））
- `IAsyncResult BeginInvoke(IntPtr arg, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（整数Ptr arg, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## ObjImporter（ObjImporter）

### 方法 (3)

- `Mesh ImportFile(string filePath)`
  （网格 Import文件（string filePath））
- `ObjImporter.meshStruct createMeshStruct(string filename)`
  （ObjImporter.meshStruct create网格Struct（string filename））
- `void populateMeshStruct(ref ObjImporter.meshStruct mesh)`
  （void populate网格Struct（ref ObjImporter.meshStruct mesh））

---

## ObjImporter.meshStruct（ObjImporter.meshStruct）

### 字段 (11)

- `Vector3[] vertices`（Vector3[] vertices）(偏移: 0x0)
- `Vector3[] normals`（Vector3[] normals）(偏移: 0x4)
- `Vector2[] uv`（Vector2[] uv）(偏移: 0x8)
- `Vector2[] uv1`（Vector2[] uv1）(偏移: 0xC)
- `Vector2[] uv2`（Vector2[] uv2）(偏移: 0x10)
- `int[] triangles`（int[] triangles）(偏移: 0x14)
- `int[] faceVerts`（int[] faceVerts）(偏移: 0x18)
- `int[] faceUVs`（int[] faceUVs）(偏移: 0x1C)
- `Vector3[] faceData`（Vector3[] face数据）(偏移: 0x20)
- `string name`（字符串 名称）(偏移: 0x24)
- `string fileName`（string file名称）(偏移: 0x28)

---

## ObjRef（ObjRef）

**继承**: IObjectReference, ISerializable（I对象引用, ISerializable）

### 字段 (8)

- `IChannelInfo channel_info`（IChannel信息 channel_info）(偏移: 0x8)
- `string uri`（string uri）(偏移: 0xC)
- `IRemotingTypeInfo typeInfo`（IRemoting类型信息 type信息）(偏移: 0x10)
- `IEnvoyInfo envoyInfo`（IEnvoy信息 envoy信息）(偏移: 0x14)
- `int flags`（int flags）(偏移: 0x18)
- `Type _serverType`（类型 _server类型）(偏移: 0x1C)
- `int MarshalledObjectRef`（int Marshalled对象Ref）(偏移: 0x0)
- `int WellKnowObjectRef`（int WellKnow对象Ref）(偏移: 0x4)

### 方法 (14)

- `ObjRef DeserializeInTheCurrentDomain(int domainId, byte[] tInfo)`
  （ObjRef DeserializeInThe当前Domain（int domainId, byte[] tInfo））
- `byte[] SerializeType()`
  （byte[] Serialize类型（））
- `bool get_IsReferenceToWellKnow()`
  （bool get_是否引用ToWellKnow（））
- `IChannelInfo get_ChannelInfo()`
  （IChannel信息 get_Channel信息（））
- `IEnvoyInfo get_EnvoyInfo()`
  （IEnvoy信息 get_Envoy信息（））
- `void set_EnvoyInfo(IEnvoyInfo value)`
  （void set_Envoy信息（IEnvoy信息 value））
- `IRemotingTypeInfo get_TypeInfo()`
  （IRemoting类型信息 get_类型信息（））
- `void set_TypeInfo(IRemotingTypeInfo value)`
  （void set_类型信息（IRemoting类型信息 value））
- `string get_URI()`
  （string get_URI（））
- `void set_URI(string value)`
  （void set_URI（string value））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））
- `object GetRealObject(StreamingContext context)`
  （对象 获取真实对象（流上下文 context））
- `void UpdateChannelInfo()`
  （void 更新Channel信息（））
- `Type get_ServerType()`
  （类型 get_服务器类型（））

---

## ObjRefSurrogate（ObjRefSurrogate）

**继承**: ISerializationSurrogate（ISerializationSurrogate）

### 方法 (2)

- `void GetObjectData(object obj, SerializationInfo si, StreamingContext sc)`
  （void 获取对象数据（object obj, Serialization信息 si, StreamingContext sc））
- `object SetObjectData(object obj, SerializationInfo si, StreamingContext sc, ISurrogateSelector selector)`
  （object 集合对象数据（object obj, Serialization信息 si, StreamingContext sc, ISurrogateSelector selector））

---

## Object（对象）

### 方法 (11)

- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(object objA, object objB)`
  （bool Equals（object objA, object objB））
- `void Finalize()`
  （void 终结（））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `Type GetType()`
  （类型 获取类型（））
- `object MemberwiseClone()`
  （object Memberwise克隆（））
- `string ToString()`
  （字符串 转字符串（））
- `bool ReferenceEquals(object objA, object objB)`
  （bool 引用Equals（object objA, object objB））
- `int InternalGetHashCode(object o)`
  （int 内部的获取HashCode（object o））
- `void FieldGetter(string typeName, string fieldName, ref object val)`
  （void FieldGetter（string typeName, string fieldName, ref object val））
- `void FieldSetter(string typeName, string fieldName, object val)`
  （void FieldSetter（string typeName, string fieldName, object val））

---

## Object（对象）

### 字段 (2)

- `IntPtr m_CachedPtr`（整数Ptr m_CachedPtr）(偏移: 0x8)
- `int OffsetOfInstanceIDInCPlusPlusObject`（int OffsetOf实例IDInCPlusPlus对象）(偏移: 0x0)

### 方法 (35)

- `int GetInstanceID()`
  （int 获取实例ID（））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `bool Equals(object other)`
  （布尔值 等于（对象 other））
- `bool op_Implicit(Object exists)`
  （bool op_Implicit（对象 exists））
- `bool CompareBaseObjects(Object lhs, Object rhs)`
  （bool Compare基础Objects（对象 lhs, 对象 rhs））
- `bool IsNativeObjectAlive(Object o)`
  （bool 是否Native对象Alive（对象 o））
- `IntPtr GetCachedPtr()`
  （整数Ptr 获取CachedPtr（））
- `string get_name()`
  （字符串 获取_名称（））
- `void set_name(string value)`
  （void 设置_名称（字符串 value））
- `Object Instantiate(Object original, Vector3 position, Quaternion rotation)`
  （对象 Instantiate（对象 original, 三维向量 position, Quaternion rotation））
- `Object Instantiate(Object original)`
  （对象 Instantiate（对象 original））
- `Object Instantiate(Object original, Transform parent, bool instantiateInWorldSpace)`
  （对象 Instantiate（对象 original, 变换 parent, bool instantiateInWorldSpace））
- `void Destroy(Object obj, float t)`
  （void 销毁（对象 obj, float t））
- `void Destroy(Object obj)`
  （void 销毁（对象 obj））
- `void DestroyImmediate(Object obj, bool allowDestroyingAssets)`
  （void 销毁Immediate（对象 obj, bool allowDestroyingAssets））
- `void DestroyImmediate(Object obj)`
  （void 销毁Immediate（对象 obj））
- `Object[] FindObjectsOfType(Type type)`
  （Object[] 查找ObjectsOf类型（类型 type））
- `Object[] FindObjectsOfType(Type type, bool includeInactive)`
  （Object[] 查找ObjectsOf类型（类型 type, bool includeInactive））
- `void DontDestroyOnLoad(Object target)`
  （void Dont销毁On加载（对象 target））
- `HideFlags get_hideFlags()`
  （隐藏Flags get_hideFlags（））
- `void set_hideFlags(HideFlags value)`
  （void set_hideFlags（隐藏Flags value））
- `void CheckNullArgument(object arg, string message)`
  （void 检查NullArgument（object arg, string message））
- `Object FindObjectOfType(Type type, bool includeInactive)`
  （对象 查找对象Of类型（类型 type, bool includeInactive））
- `string ToString()`
  （字符串 转字符串（））
- `bool op_Equality(Object x, Object y)`
  （bool op_Equality（对象 x, 对象 y））
- `bool op_Inequality(Object x, Object y)`
  （bool op_Inequality（对象 x, 对象 y））
- `int GetOffsetOfInstanceIDInCPlusPlusObject()`
  （int 获取OffsetOf实例IDInCPlusPlus对象（））
- `Object Internal_CloneSingle(Object data)`
  （对象 Internal_克隆单个（对象 data））
- `Object Internal_CloneSingleWithParent(Object data, Transform parent, bool worldPositionStays)`
  （对象 Internal_克隆单个With父级（对象 data, 变换 parent, bool worldPositionStays））
- `Object Internal_InstantiateSingle(Object data, Vector3 pos, Quaternion rot)`
  （对象 Internal_Instantiate单个（对象 data, 三维向量 pos, Quaternion rot））
- `string ToString(Object obj)`
  （string To字符串（对象 obj））
- `string GetName(Object obj)`
  （string 获取名称（对象 obj））
- `void SetName(Object obj, string name)`
  （void 集合名称（对象 obj, string name））
- `Object FindObjectFromInstanceID(int instanceID)`
  （对象 查找对象From实例ID（int instanceID））
- `Object Internal_InstantiateSingle_Injected(Object data, ref Vector3 pos, ref Quaternion rot)`
  （对象 Internal_InstantiateSingle_Injected（对象 data, ref Vector3 pos, ref Quaternion rot））

---

## ObjectDisposedException（对象DisposedException）

**继承**: InvalidOperationException（InvalidOperationException）

### 字段 (1)

- `string objectName`（string object名称）(偏移: 0x44)

### 方法 (3)

- `string get_Message()`
  （字符串 获取_消息（））
- `string get_ObjectName()`
  （string get_对象名称（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））

---

## ObjectEqualityComparer（对象EqualityComparer）

**继承**: IEqualityComparer（IEqualityComparer）

### 字段 (1)

- `ObjectEqualityComparer Default`（对象EqualityComparer 默认的）(偏移: 0x0)

---

## ObjectHolder（对象Holder）

### 字段 (14)

- `object m_object`（object m_object）(偏移: 0x8)
- `long m_id`（long m_id）(偏移: 0x10)
- `int m_missingElementsRemaining`（int m_missingElementsRemaining）(偏移: 0x18)
- `int m_missingDecendents`（int m_missingDecendents）(偏移: 0x1C)
- `SerializationInfo m_serInfo`（Serialization信息 m_ser信息）(偏移: 0x20)
- `ISerializationSurrogate m_surrogate`（ISerializationSurrogate m_surrogate）(偏移: 0x24)
- `FixupHolderList m_missingElements`（FixupHolder列表 m_missingElements）(偏移: 0x28)
- `LongList m_dependentObjects`（Long列表 m_dependentObjects）(偏移: 0x2C)
- `ObjectHolder m_next`（对象Holder m_next）(偏移: 0x30)
- `int m_flags`（int m_flags）(偏移: 0x34)
- `bool m_markForFixupWhenAvailable`（bool m_markForFixupWhenAvailable）(偏移: 0x38)
- `ValueTypeFixupInfo m_valueFixup`（值类型Fixup信息 m_valueFixup）(偏移: 0x3C)
- `TypeLoadExceptionHolder m_typeLoad`（类型加载ExceptionHolder m_type加载）(偏移: 0x40)
- `bool m_reachable`（bool m_reachable）(偏移: 0x44)

### 方法 (38)

- `void IncrementDescendentFixups(int amount)`
  （void IncrementDescendentFixups（int amount））
- `void DecrementFixupsRemaining(ObjectManager manager)`
  （void DecrementFixupsRemaining（对象管理器 manager））
- `void RemoveDependency(long id)`
  （void 移除Dependency（long id））
- `void AddFixup(FixupHolder fixup, ObjectManager manager)`
  （void 添加Fixup（FixupHolder fixup, 对象管理器 manager））
- `void UpdateDescendentDependencyChain(int amount, ObjectManager manager)`
  （void 更新DescendentDependencyChain（int amount, 对象管理器 manager））
- `void AddDependency(long dependentObject)`
  （void 添加Dependency（long dependentObject））
- `void UpdateData(object obj, SerializationInfo info, ISerializationSurrogate surrogate, long idOfContainer, FieldInfo field, int[] arrayIndex, ObjectManager manager)`
  （void 更新数据（object obj, Serialization信息 info, ISerializationSurrogate surrogate, long idOfContainer, Field信息 field, int[] arrayIndex, 对象管理器 manager））
- `void MarkForCompletionWhenAvailable()`
  （void MarkForCompletionWhenAvailable（））
- `void SetFlags()`
  （void 集合Flags（））
- `bool get_IsIncompleteObjectReference()`
  （bool get_是否Incomplete对象引用（））
- `void set_IsIncompleteObjectReference(bool value)`
  （void set_是否Incomplete对象引用（bool value））
- `bool get_RequiresDelayedFixup()`
  （bool get_RequiresDelayedFixup（））
- `bool get_RequiresValueTypeFixup()`
  （bool get_Requires值类型Fixup（））
- `bool get_ValueTypeFixupPerformed()`
  （bool get_值类型FixupPerformed（））
- `void set_ValueTypeFixupPerformed(bool value)`
  （void set_值类型FixupPerformed（bool value））
- `bool get_HasISerializable()`
  （bool get_是否有ISerializable（））
- `bool get_HasSurrogate()`
  （bool get_是否有Surrogate（））
- `bool get_CanSurrogatedObjectValueChange()`
  （bool get_能否Surrogated对象值Change（））
- `bool get_CanObjectValueChange()`
  （bool get_能否对象值Change（））
- `int get_DirectlyDependentObjects()`
  （int get_DirectlyDependentObjects（））
- `int get_TotalDependentObjects()`
  （int get_TotalDependentObjects（））
- `bool get_Reachable()`
  （bool get_Reachable（））
- `void set_Reachable(bool value)`
  （void set_Reachable（bool value））
- `bool get_TypeLoadExceptionReachable()`
  （bool get_类型加载ExceptionReachable（））
- `TypeLoadExceptionHolder get_TypeLoadException()`
  （类型加载ExceptionHolder get_类型加载Exception（））
- `void set_TypeLoadException(TypeLoadExceptionHolder value)`
  （void set_类型加载Exception（类型加载ExceptionHolder value））
- `object get_ObjectValue()`
  （object get_对象值（））
- `void SetObjectValue(object obj, ObjectManager manager)`
  （void 集合对象值（object obj, 对象管理器 manager））
- `SerializationInfo get_SerializationInfo()`
  （Serialization信息 get_Serialization信息（））
- `void set_SerializationInfo(SerializationInfo value)`
  （void set_Serialization信息（Serialization信息 value））
- `ISerializationSurrogate get_Surrogate()`
  （ISerializationSurrogate get_Surrogate（））
- `LongList get_DependentObjects()`
  （Long列表 get_DependentObjects（））
- `void set_DependentObjects(LongList value)`
  （void set_DependentObjects（Long列表 value））
- `bool get_RequiresSerInfoFixup()`
  （bool get_RequiresSer信息Fixup（））
- `void set_RequiresSerInfoFixup(bool value)`
  （void set_RequiresSer信息Fixup（bool value））
- `ValueTypeFixupInfo get_ValueFixup()`
  （值类型Fixup信息 get_值Fixup（））
- `bool get_CompletelyFixed()`
  （bool get_Completely固定（））
- `long get_ContainerID()`
  （long get_容器ID（））

---

## ObjectHolderList（对象Holder列表）

### 字段 (2)

- `ObjectHolder[] m_values`（对象Holder[] m_values）(偏移: 0x8)
- `int m_count`（int m_count）(偏移: 0xC)

### 方法 (5)

- `void Add(ObjectHolder value)`
  （void 添加（对象Holder value））
- `ObjectHolderListEnumerator GetFixupEnumerator()`
  （对象Holder列表Enumerator 获取FixupEnumerator（））
- `void EnlargeArray()`
  （void Enlarge数组（））
- `int get_Version()`
  （int get_Version（））
- `int get_Count()`
  （整数 获取_数量（））

---

## ObjectHolderListEnumerator（对象Holder列表Enumerator）

### 字段 (4)

- `bool m_isFixupEnumerator`（bool m_isFixupEnumerator）(偏移: 0x8)
- `ObjectHolderList m_list`（对象Holder列表 m_list）(偏移: 0xC)
- `int m_startingVersion`（int m_startingVersion）(偏移: 0x10)
- `int m_currPos`（int m_currPos）(偏移: 0x14)

### 方法 (2)

- `bool MoveNext()`
  （布尔值 移动下一个（））
- `ObjectHolder get_Current()`
  （对象Holder get_当前（））

---

## ObjectIDGenerator（对象IDGenerator）

### 字段 (5)

- `int m_currentCount`（int m_current数量）(偏移: 0x8)
- `int m_currentSize`（int m_current大小）(偏移: 0xC)
- `long[] m_ids`（long[] m_ids）(偏移: 0x10)
- `object[] m_objs`（object[] m_objs）(偏移: 0x14)
- `int[] sizes`（int[] sizes）(偏移: 0x0)

### 方法 (4)

- `int FindElement(object obj, out bool found)`
  （int 查找元素（object obj, out bool found））
- `long GetId(object obj, out bool firstTime)`
  （long 获取Id（object obj, out bool firstTime））
- `long HasId(object obj, out bool firstTime)`
  （long 是否有Id（object obj, out bool firstTime））
- `void Rehash()`
  （void Rehash（））

---

## ObjectManager（对象管理器）

### 字段 (8)

- `DeserializationEventHandler m_onDeserializationHandler`（Deserialization事件处理器 m_onDeserialization处理器）(偏移: 0x8)
- `SerializationEventHandler m_onDeserializedHandler`（Serialization事件处理器 m_onDeserialized处理器）(偏移: 0xC)
- `ObjectHolder[] m_objects`（对象Holder[] m_objects）(偏移: 0x10)
- `object m_topObject`（object m_top对象）(偏移: 0x14)
- `ObjectHolderList m_specialFixupObjects`（对象Holder列表 m_specialFixupObjects）(偏移: 0x18)
- `long m_fixupCount`（long m_fixup数量）(偏移: 0x20)
- `ISurrogateSelector m_selector`（ISurrogateSelector m_selector）(偏移: 0x28)
- `StreamingContext m_context`（流上下文 m_上下文）(偏移: 0x2C)

### 方法 (28)

- `bool CanCallGetType(object obj)`
  （bool 能否Call获取类型（object obj））
- `void set_TopObject(object value)`
  （void set_顶部对象（object value））
- `object get_TopObject()`
  （object get_顶部对象（））
- `ObjectHolderList get_SpecialFixupObjects()`
  （对象Holder列表 get_特殊FixupObjects（））
- `ObjectHolder FindObjectHolder(long objectID)`
  （对象Holder 查找对象Holder（long objectID））
- `ObjectHolder FindOrCreateObjectHolder(long objectID)`
  （对象Holder 查找Or创建对象Holder（long objectID））
- `void AddObjectHolder(ObjectHolder holder)`
  （void 添加对象Holder（对象Holder holder））
- `bool GetCompletionInfo(FixupHolder fixup, out ObjectHolder holder, out object member, bool bThrowIfMissing)`
  （bool 获取Completion信息（FixupHolder fixup, out ObjectHolder holder, out object member, bool bThrowIfMissing））
- `void FixupSpecialObject(ObjectHolder holder)`
  （void Fixup特殊对象（对象Holder holder））
- `bool ResolveObjectReference(ObjectHolder holder)`
  （bool Resolve对象引用（对象Holder holder））
- `bool DoValueTypeFixup(FieldInfo memberToFix, ObjectHolder holder, object value)`
  （bool Do值类型Fixup（Field信息 memberToFix, 对象Holder holder, object value））
- `void CompleteObject(ObjectHolder holder, bool bObjectFullyComplete)`
  （void Complete对象（对象Holder holder, bool bObjectFullyComplete））
- `void DoNewlyRegisteredObjectFixups(ObjectHolder holder)`
  （void DoNewlyRegistered对象Fixups（对象Holder holder））
- `object GetObject(long objectID)`
  （object 获取对象（long objectID））
- `void RegisterString(string obj, long objectID, SerializationInfo info, long idOfContainingObj, MemberInfo member)`
  （void Register字符串（string obj, long objectID, Serialization信息 info, long idOfContainingObj, Member信息 member））
- `void RegisterObject(object obj, long objectID, SerializationInfo info, long idOfContainingObj, MemberInfo member, int[] arrayIndex)`
  （void Register对象（object obj, long objectID, Serialization信息 info, long idOfContainingObj, Member信息 member, int[] arrayIndex））
- `void CompleteISerializableObject(object obj, SerializationInfo info, StreamingContext context)`
  （void CompleteISerializable对象（object obj, Serialization信息 info, StreamingContext context））
- `RuntimeConstructorInfo GetConstructor(RuntimeType t)`
  （RuntimeConstructor信息 获取Constructor（Runtime类型 t））
- `void DoFixups()`
  （void DoFixups（））
- `void RegisterFixup(FixupHolder fixup, long objectToBeFixed, long objectRequired)`
  （void RegisterFixup（FixupHolder fixup, long objectToBeFixed, long objectRequired））
- `void RecordFixup(long objectToBeFixed, MemberInfo member, long objectRequired)`
  （void RecordFixup（long objectToBeFixed, Member信息 member, long objectRequired））
- `void RecordDelayedFixup(long objectToBeFixed, string memberName, long objectRequired)`
  （void RecordDelayedFixup（long objectToBeFixed, string memberName, long objectRequired））
- `void RecordArrayElementFixup(long arrayToBeFixed, int[] indices, long objectRequired)`
  （void Record数组元素Fixup（long arrayToBeFixed, int[] indices, long objectRequired））
- `void RaiseDeserializationEvent()`
  （void RaiseDeserialization事件（））
- `void AddOnDeserialization(DeserializationEventHandler handler)`
  （void 添加OnDeserialization（Deserialization事件处理器 handler））
- `void AddOnDeserialized(object obj)`
  （void 添加OnDeserialized（object obj））
- `void RaiseOnDeserializedEvent(object obj)`
  （void RaiseOnDeserialized事件（object obj））
- `void RaiseOnDeserializingEvent(object obj)`
  （void RaiseOnDeserializing事件（object obj））

---

## ObjectMap（对象映射）

### 字段 (11)

- `string objectName`（string object名称）(偏移: 0x8)
- `Type objectType`（类型 object类型）(偏移: 0xC)
- `BinaryTypeEnum[] binaryTypeEnumA`（Binary类型Enum[] binary类型EnumA）(偏移: 0x10)
- `object[] typeInformationA`（object[] typeInformationA）(偏移: 0x14)
- `Type[] memberTypes`（Type[] memberTypes）(偏移: 0x18)
- `string[] memberNames`（字符串[] 成员名称）(偏移: 0x1C)
- `ReadObjectInfo objectInfo`（Read对象信息 object信息）(偏移: 0x20)
- `bool isInitObjectInfo`（bool is初始化对象信息）(偏移: 0x24)
- `ObjectReader objectReader`（对象读取器 object读取器）(偏移: 0x28)
- `int objectId`（整数 对象ID）(偏移: 0x2C)
- `BinaryAssemblyInfo assemblyInfo`（BinaryAssembly信息 assembly信息）(偏移: 0x30)

### 方法 (3)

- `ReadObjectInfo CreateObjectInfo(ref SerializationInfo si, ref object[] memberData)`
  （Read对象信息 创建对象信息（ref SerializationInfo si, ref object[] memberData））
- `ObjectMap Create(string name, Type objectType, string[] memberNames, ObjectReader objectReader, int objectId, BinaryAssemblyInfo assemblyInfo)`
  （对象映射 创建（string name, 类型 objectType, string[] memberNames, 对象读取器 objectReader, int objectId, BinaryAssembly信息 assemblyInfo））
- `ObjectMap Create(string name, string[] memberNames, BinaryTypeEnum[] binaryTypeEnumA, object[] typeInformationA, int[] memberAssemIds, ObjectReader objectReader, int objectId, BinaryAssemblyInfo assemblyInfo, SizedArray assemIdToAssemblyTable)`
  （对象映射 创建（string name, string[] memberNames, Binary类型Enum[] binaryTypeEnumA, object[] typeInformationA, int[] memberAssemIds, 对象读取器 objectReader, int objectId, BinaryAssembly信息 assemblyInfo, Sized数组 assemIdToAssemblyTable））

---

## ObjectMapInfo（对象映射信息）

### 字段 (4)

- `int objectId`（整数 对象ID）(偏移: 0x8)
- `int numMembers`（int numMembers）(偏移: 0xC)
- `string[] memberNames`（字符串[] 成员名称）(偏移: 0x10)
- `Type[] memberTypes`（Type[] memberTypes）(偏移: 0x14)

### 方法 (1)

- `bool isCompatible(int numMembers, string[] memberNames, Type[] memberTypes)`
  （bool isCompatible（int numMembers, string[] memberNames, Type[] memberTypes））

---

## ObjectNull（对象Null）

### 字段 (1)

- `int nullCount`（int null数量）(偏移: 0x8)

### 方法 (4)

- `void SetNullCount(int nullCount)`
  （void 集合Null数量（int nullCount））
- `void Write(__BinaryWriter sout)`
  （void 写入（__二进制写入器 sout））
- `void Read(__BinaryParser input, BinaryHeaderEnum binaryHeaderEnum)`
  （void Read（__BinaryParser input, Binary标题Enum binaryHeaderEnum））
- `void Dump()`
  （void 转储（））

---

## ObjectPlacer（对象Placer）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (3)

- `GameObject go`（游戏对象 go）(偏移: 0xC)
- `bool direct`（bool direct）(偏移: 0x10)
- `bool issueGUOs`（bool issueGUOs）(偏移: 0x11)

### 方法 (3)

- `void Update()`
  （void 更新（））
- `void PlaceObject()`
  （void Place对象（））
- `IEnumerator RemoveObject()`
  （IEnumerator 移除对象（））

---

## ObjectPool（对象池）

### 方法 (2)

- `Transform get_container()`
  （变换 get_container（））
- `void set_container(Transform value)`
  （void set_container（变换 value））

---

## ObjectProgress（对象Progress）

### 字段 (20)

- `int opRecordIdCount`（int opRecordId数量）(偏移: 0x0)
- `bool isInitial`（bool isInitial）(偏移: 0x8)
- `int count`（整数 数量）(偏移: 0xC)
- `BinaryTypeEnum expectedType`（Binary类型Enum expected类型）(偏移: 0x10)
- `object expectedTypeInformation`（object expected类型Information）(偏移: 0x14)
- `string name`（字符串 名称）(偏移: 0x18)
- `InternalObjectTypeE objectTypeEnum`（内部的对象类型E object类型Enum）(偏移: 0x1C)
- `InternalMemberTypeE memberTypeEnum`（内部的Member类型E member类型Enum）(偏移: 0x20)
- `InternalMemberValueE memberValueEnum`（内部的Member值E member值Enum）(偏移: 0x24)
- `Type dtType`（类型 dt类型）(偏移: 0x28)
- `int numItems`（int numItems）(偏移: 0x2C)
- `BinaryTypeEnum binaryTypeEnum`（Binary类型Enum binary类型Enum）(偏移: 0x30)
- `object typeInformation`（object typeInformation）(偏移: 0x34)
- `int nullCount`（int null数量）(偏移: 0x38)
- `int memberLength`（int memberLength）(偏移: 0x3C)
- `BinaryTypeEnum[] binaryTypeEnumA`（Binary类型Enum[] binary类型EnumA）(偏移: 0x40)
- `object[] typeInformationA`（object[] typeInformationA）(偏移: 0x44)
- `string[] memberNames`（字符串[] 成员名称）(偏移: 0x48)
- `Type[] memberTypes`（Type[] memberTypes）(偏移: 0x4C)
- `ParseRecord pr`（解析Record pr）(偏移: 0x50)

### 方法 (3)

- `void Init()`
  （void 初始化（））
- `void ArrayCountIncrement(int value)`
  （void 数组数量Increment（int value））
- `bool GetNext(out BinaryTypeEnum outBinaryTypeEnum, out object outTypeInformation)`
  （bool 获取下一个（out BinaryTypeEnum outBinaryTypeEnum, out object outTypeInformation））

---

## ObjectReader（对象读取器）

### 字段 (24)

- `Stream m_stream`（流 m_stream）(偏移: 0x8)
- `ISurrogateSelector m_surrogates`（ISurrogateSelector m_surrogates）(偏移: 0xC)
- `StreamingContext m_context`（流上下文 m_上下文）(偏移: 0x10)
- `ObjectManager m_objectManager`（对象管理器 m_object管理器）(偏移: 0x18)
- `InternalFE formatterEnums`（内部的FE formatterEnums）(偏移: 0x1C)
- `SerializationBinder m_binder`（SerializationBinder m_binder）(偏移: 0x20)
- `long topId`（long topId）(偏移: 0x28)
- `bool bSimpleAssembly`（bool bSimpleAssembly）(偏移: 0x30)
- `object handlerObject`（object handler对象）(偏移: 0x34)
- `object m_topObject`（object m_top对象）(偏移: 0x38)
- `Header[] headers`（Header[] headers）(偏移: 0x3C)
- `HeaderHandler handler`（标题处理器 handler）(偏移: 0x40)
- `SerObjectInfoInit serObjectInfoInit`（Ser对象信息初始化 ser对象信息初始化）(偏移: 0x44)
- `IFormatterConverter m_formatterConverter`（IFormatterConverter m_formatterConverter）(偏移: 0x48)
- `SerStack stack`（Ser栈 stack）(偏移: 0x4C)
- `SerStack valueFixupStack`（Ser栈 valueFixup栈）(偏移: 0x50)
- `object[] crossAppDomainArray`（object[] crossAppDomain数组）(偏移: 0x54)
- `bool bFullDeserialization`（bool b满Deserialization）(偏移: 0x58)
- `bool bOldFormatDetected`（bool b旧的格式化Detected）(偏移: 0x59)
- `IntSizedArray valTypeObjectIdTable`（整数Sized数组 val类型对象IdTable）(偏移: 0x5C)
- `NameCache typeCache`（名称缓存 type缓存）(偏移: 0x60)
- `string previousAssemblyString`（string previousAssembly字符串）(偏移: 0x64)
- `string previousName`（string previous名称）(偏移: 0x68)
- `Type previousType`（类型 previous类型）(偏移: 0x6C)

### 方法 (32)

- `SerStack get_ValueFixupStack()`
  （Ser栈 get_值Fixup栈（））
- `object get_TopObject()`
  （object get_顶部对象（））
- `void set_TopObject(object value)`
  （void set_顶部对象（object value））
- `object Deserialize(HeaderHandler handler, __BinaryParser serParser, bool fCheck)`
  （object Deserialize（标题处理器 handler, __BinaryParser serParser, bool fCheck））
- `bool HasSurrogate(Type t)`
  （bool 是否有Surrogate（类型 t））
- `void CheckSerializable(Type t)`
  （void 检查Serializable（类型 t））
- `void InitFullDeserialization()`
  （void 初始化满Deserialization（））
- `object CrossAppDomainArray(int index)`
  （object CrossAppDomain数组（int index））
- `ReadObjectInfo CreateReadObjectInfo(Type objectType)`
  （Read对象信息 创建Read对象信息（类型 objectType））
- `ReadObjectInfo CreateReadObjectInfo(Type objectType, string[] memberNames, Type[] memberTypes)`
  （Read对象信息 创建Read对象信息（类型 objectType, string[] memberNames, Type[] memberTypes））
- `void Parse(ParseRecord pr)`
  （void 解析（解析Record pr））
- `void ParseError(ParseRecord processing, ParseRecord onStack)`
  （void 解析Error（解析Record processing, 解析Record onStack））
- `void ParseSerializedStreamHeader(ParseRecord pr)`
  （void 解析Serialized流标题（解析Record pr））
- `void ParseSerializedStreamHeaderEnd(ParseRecord pr)`
  （void 解析Serialized流标题结束（解析Record pr））
- `void ParseObject(ParseRecord pr)`
  （void 解析对象（解析Record pr））
- `void ParseObjectEnd(ParseRecord pr)`
  （void 解析对象结束（解析Record pr））
- `void ParseArray(ParseRecord pr)`
  （void 解析数组（解析Record pr））
- `void NextRectangleMap(ParseRecord pr)`
  （void 下一个Rectangle映射（解析Record pr））
- `void ParseArrayMember(ParseRecord pr)`
  （void 解析数组Member（解析Record pr））
- `void ParseArrayMemberEnd(ParseRecord pr)`
  （void 解析数组Member结束（解析Record pr））
- `void ParseMember(ParseRecord pr)`
  （void 解析Member（解析Record pr））
- `void ParseMemberEnd(ParseRecord pr)`
  （void 解析Member结束（解析Record pr））
- `void ParseString(ParseRecord pr, ParseRecord parentPr)`
  （void 解析字符串（解析Record pr, 解析Record parentPr））
- `void RegisterObject(object obj, ParseRecord pr, ParseRecord objectPr)`
  （void Register对象（object obj, 解析Record pr, 解析Record objectPr））
- `void RegisterObject(object obj, ParseRecord pr, ParseRecord objectPr, bool bIsString)`
  （void Register对象（object obj, 解析Record pr, 解析Record objectPr, bool bIsString））
- `long GetId(long objectId)`
  （long 获取Id（long objectId））
- `Type Bind(string assemblyString, string typeString)`
  （类型 Bind（string assemblyString, string typeString））
- `Type FastBindToType(string assemblyName, string typeName)`
  （类型 FastBindTo类型（string assemblyName, string typeName））
- `Assembly ResolveSimpleAssemblyName(AssemblyName assemblyName)`
  （Assembly ResolveSimpleAssembly名称（Assembly名称 assemblyName））
- `void GetSimplyNamedTypeFromAssembly(Assembly assm, string typeName, ref Type type)`
  （void 获取SimplyNamed类型FromAssembly（Assembly assm, string typeName, ref Type type））
- `Type GetType(BinaryAssemblyInfo assemblyInfo, string name)`
  （类型 获取类型（BinaryAssembly信息 assemblyInfo, string name））
- `void CheckTypeForwardedTo(Assembly sourceAssembly, Assembly destAssembly, Type resolvedType)`
  （void 检查类型ForwardedTo（Assembly sourceAssembly, Assembly destAssembly, 类型 resolvedType））

---

## ObjectReader.TopLevelAssemblyTypeResolver（对象Reader.顶部等级Assembly类型Resolver）

### 字段 (1)

- `Assembly m_topLevelAssembly`（Assembly m_top等级Assembly）(偏移: 0x8)

### 方法 (1)

- `Type ResolveType(Assembly assembly, string simpleTypeName, bool ignoreCase)`
  （类型 Resolve类型（Assembly assembly, string simpleTypeName, bool ignoreCase））

---

## ObjectReader.TypeNAssembly（对象Reader.类型NAssembly）

### 字段 (2)

- `Type type`（类型 type）(偏移: 0x8)
- `string assemblyName`（string assembly名称）(偏移: 0xC)

---

## ObjectWriter（对象写入器）

### 字段 (21)

- `Queue m_objectQueue`（队列 m_object队列）(偏移: 0x8)
- `ObjectIDGenerator m_idGenerator`（对象IDGenerator m_idGenerator）(偏移: 0xC)
- `int m_currentId`（int m_currentId）(偏移: 0x10)
- `ISurrogateSelector m_surrogates`（ISurrogateSelector m_surrogates）(偏移: 0x14)
- `StreamingContext m_context`（流上下文 m_上下文）(偏移: 0x18)
- `__BinaryWriter serWriter`（__Binary写入器 ser写入器）(偏移: 0x20)
- `SerializationObjectManager m_objectManager`（Serialization对象管理器 m_object管理器）(偏移: 0x24)
- `long topId`（long topId）(偏移: 0x28)
- `string topName`（string top名称）(偏移: 0x30)
- `Header[] headers`（Header[] headers）(偏移: 0x34)
- `InternalFE formatterEnums`（内部的FE formatterEnums）(偏移: 0x38)
- `SerializationBinder m_binder`（SerializationBinder m_binder）(偏移: 0x3C)
- `SerObjectInfoInit serObjectInfoInit`（Ser对象信息初始化 ser对象信息初始化）(偏移: 0x40)
- `IFormatterConverter m_formatterConverter`（IFormatterConverter m_formatterConverter）(偏移: 0x44)
- `object[] crossAppDomainArray`（object[] crossAppDomain数组）(偏移: 0x48)
- `object previousObj`（object previousObj）(偏移: 0x4C)
- `long previousId`（long previousId）(偏移: 0x50)
- `Type previousType`（类型 previous类型）(偏移: 0x58)
- `InternalPrimitiveTypeE previousCode`（内部的Primitive类型E previousCode）(偏移: 0x5C)
- `Hashtable assemblyToIdTable`（Hashtable assemblyToIdTable）(偏移: 0x60)
- `SerStack niPool`（Ser栈 ni池）(偏移: 0x64)

### 方法 (30)

- `void Serialize(object graph, Header[] inHeaders, __BinaryWriter serWriter, bool fCheck)`
  （void Serialize（object graph, Header[] inHeaders, __Binary写入器 serWriter, bool fCheck））
- `SerializationObjectManager get_ObjectManager()`
  （Serialization对象管理器 get_对象管理器（））
- `void Write(WriteObjectInfo objectInfo, NameInfo memberNameInfo, NameInfo typeNameInfo)`
  （void Write（Write对象信息 objectInfo, 名称信息 memberNameInfo, 名称信息 typeNameInfo））
- `void Write(WriteObjectInfo objectInfo, NameInfo memberNameInfo, NameInfo typeNameInfo, string[] memberNames, Type[] memberTypes, object[] memberData, WriteObjectInfo[] memberObjectInfos)`
  （void Write（Write对象信息 objectInfo, 名称信息 memberNameInfo, 名称信息 typeNameInfo, string[] memberNames, Type[] memberTypes, object[] memberData, Write对象Info[] memberObjectInfos））
- `void WriteMemberSetup(WriteObjectInfo objectInfo, NameInfo memberNameInfo, NameInfo typeNameInfo, string memberName, Type memberType, object memberData, WriteObjectInfo memberObjectInfo)`
  （void WriteMemberSetup（Write对象信息 objectInfo, 名称信息 memberNameInfo, 名称信息 typeNameInfo, string memberName, 类型 memberType, object memberData, Write对象信息 memberObjectInfo））
- `void WriteMembers(NameInfo memberNameInfo, NameInfo memberTypeNameInfo, object memberData, WriteObjectInfo objectInfo, NameInfo typeNameInfo, WriteObjectInfo memberObjectInfo)`
  （void WriteMembers（名称信息 memberNameInfo, 名称信息 memberTypeNameInfo, object memberData, Write对象信息 objectInfo, 名称信息 typeNameInfo, Write对象信息 memberObjectInfo））
- `void WriteArray(WriteObjectInfo objectInfo, NameInfo memberNameInfo, WriteObjectInfo memberObjectInfo)`
  （void Write数组（Write对象信息 objectInfo, 名称信息 memberNameInfo, Write对象信息 memberObjectInfo））
- `void WriteArrayMember(WriteObjectInfo objectInfo, NameInfo arrayElemTypeNameInfo, object data)`
  （void Write数组Member（Write对象信息 objectInfo, 名称信息 arrayElemTypeNameInfo, object data））
- `void WriteRectangle(WriteObjectInfo objectInfo, int rank, int[] maxA, Array array, NameInfo arrayElemNameTypeInfo, int[] lowerBoundA)`
  （void WriteRectangle（Write对象信息 objectInfo, int rank, int[] maxA, 数组 array, 名称信息 arrayElemNameTypeInfo, int[] lowerBoundA））
- `object GetNext(out long objID)`
  （object 获取下一个（out long objID））
- `long InternalGetId(object obj, bool assignUniqueIdToValueType, Type type, out bool isNew)`
  （long 内部的获取Id（object obj, bool assignUniqueIdToValueType, 类型 type, out bool isNew））
- `long Schedule(object obj, bool assignUniqueIdToValueType, Type type)`
  （long Schedule（object obj, bool assignUniqueIdToValueType, 类型 type））
- `long Schedule(object obj, bool assignUniqueIdToValueType, Type type, WriteObjectInfo objectInfo)`
  （long Schedule（object obj, bool assignUniqueIdToValueType, 类型 type, Write对象信息 objectInfo））
- `bool WriteKnownValueClass(NameInfo memberNameInfo, NameInfo typeNameInfo, object data)`
  （bool WriteKnown值类（名称信息 memberNameInfo, 名称信息 typeNameInfo, object data））
- `void WriteObjectRef(NameInfo nameInfo, long objectId)`
  （void Write对象Ref（名称信息 nameInfo, long objectId））
- `void WriteString(NameInfo memberNameInfo, NameInfo typeNameInfo, object stringObject)`
  （void Write字符串（名称信息 memberNameInfo, 名称信息 typeNameInfo, object stringObject））
- `bool CheckForNull(WriteObjectInfo objectInfo, NameInfo memberNameInfo, NameInfo typeNameInfo, object data)`
  （bool 检查ForNull（Write对象信息 objectInfo, 名称信息 memberNameInfo, 名称信息 typeNameInfo, object data））
- `void WriteSerializedStreamHeader(long topId, long headerId)`
  （void WriteSerialized流标题（long topId, long headerId））
- `NameInfo TypeToNameInfo(Type type, WriteObjectInfo objectInfo, InternalPrimitiveTypeE code, NameInfo nameInfo)`
  （名称信息 类型To名称信息（类型 type, Write对象信息 objectInfo, 内部的Primitive类型E code, 名称信息 nameInfo））
- `NameInfo TypeToNameInfo(Type type)`
  （名称信息 类型To名称信息（类型 type））
- `NameInfo TypeToNameInfo(WriteObjectInfo objectInfo)`
  （名称信息 类型To名称信息（Write对象信息 objectInfo））
- `NameInfo TypeToNameInfo(WriteObjectInfo objectInfo, NameInfo nameInfo)`
  （名称信息 类型To名称信息（Write对象信息 objectInfo, 名称信息 nameInfo））
- `void TypeToNameInfo(Type type, NameInfo nameInfo)`
  （void 类型To名称信息（类型 type, 名称信息 nameInfo））
- `NameInfo MemberToNameInfo(string name)`
  （名称信息 MemberTo名称信息（string name））
- `InternalPrimitiveTypeE ToCode(Type type)`
  （内部的Primitive类型E ToCode（类型 type））
- `long GetAssemblyId(WriteObjectInfo objectInfo)`
  （long 获取AssemblyId（Write对象信息 objectInfo））
- `Type GetType(object obj)`
  （类型 获取类型（object obj））
- `NameInfo GetNameInfo()`
  （名称信息 获取名称信息（））
- `bool CheckTypeFormat(FormatterTypeStyle test, FormatterTypeStyle want)`
  （bool 检查类型格式化（Formatter类型Style test, Formatter类型Style want））
- `void PutNameInfo(NameInfo nameInfo)`
  （void Put名称信息（名称信息 nameInfo））

---

## ObscuredBool（模糊的布尔值）

**继承**: IEquatable<ObscuredBool>, IComparable<ObscuredBool>, IComparable<bool>, IComparable（IEquatable<模糊的Bool>, IComparable<模糊的Bool>, IComparable<bool>, IComparable）

### 字段 (6)

- `byte cryptoKey`（byte crypto键）(偏移: 0x0)
- `byte currentCryptoKey`（byte currentCrypto键）(偏移: 0x0)
- `int hiddenValue`（int hidden值）(偏移: 0x4)
- `bool inited`（布尔值 已初始化）(偏移: 0x8)
- `bool fakeValue`（bool fake值）(偏移: 0x9)
- `bool fakeValueActive`（布尔值 假值激活的）(偏移: 0xA)

### 方法 (21)

- `void SetNewCryptoKey(byte newKey)`
  （void 集合新的Crypto键（byte newKey））
- `int Encrypt(bool value)`
  （int Encrypt（bool value））
- `int Encrypt(bool value, byte key)`
  （int Encrypt（bool value, byte key））
- `bool Decrypt(int value)`
  （bool Decrypt（int value））
- `bool Decrypt(int value, byte key)`
  （bool Decrypt（int value, byte key））
- `ObscuredBool FromEncrypted(int encrypted)`
  （模糊的布尔值 FromEncrypted（int encrypted））
- `void ApplyNewCryptoKey()`
  （void 应用新加密密钥（））
- `void RandomizeCryptoKey()`
  （void 随机化加密密钥（））
- `int GetEncrypted()`
  （int 获取Encrypted（））
- `void SetEncrypted(int encrypted)`
  （void 集合Encrypted（int encrypted））
- `bool GetDecrypted()`
  （bool 获取Decrypted（））
- `bool InternalDecrypt()`
  （bool 内部的Decrypt（））
- `ObscuredBool op_Implicit(bool value)`
  （模糊的布尔值 op_Implicit（bool value））
- `bool op_Implicit(ObscuredBool value)`
  （bool op_Implicit（模糊的布尔值 value））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `string ToString()`
  （字符串 转字符串（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(ObscuredBool obj)`
  （bool Equals（模糊的布尔值 obj））
- `int CompareTo(ObscuredBool other)`
  （int CompareTo（模糊的布尔值 other））
- `int CompareTo(bool other)`
  （int CompareTo（bool other））
- `int CompareTo(object obj)`
  （整数 比较到（对象 obj））

---

## ObscuredByte（模糊的Byte）

**继承**: IFormattable, IEquatable<ObscuredByte>, IComparable<ObscuredByte>, IComparable<byte>, IComparable（IFormattable, IEquatable<模糊的Byte>, IComparable<模糊的Byte>, IComparable<byte>, IComparable）

### 字段 (6)

- `byte cryptoKey`（byte crypto键）(偏移: 0x0)
- `byte currentCryptoKey`（byte currentCrypto键）(偏移: 0x0)
- `byte hiddenValue`（byte hidden值）(偏移: 0x0)
- `bool inited`（布尔值 已初始化）(偏移: 0x0)
- `byte fakeValue`（byte fake值）(偏移: 0x0)
- `bool fakeValueActive`（布尔值 假值激活的）(偏移: 0x0)

### 方法 (26)

- `void SetNewCryptoKey(byte newKey)`
  （void 集合新的Crypto键（byte newKey））
- `byte EncryptDecrypt(byte value)`
  （byte EncryptDecrypt（byte value））
- `void EncryptDecrypt(byte[] value)`
  （void EncryptDecrypt（byte[] value））
- `byte EncryptDecrypt(byte value, byte key)`
  （byte EncryptDecrypt（byte value, byte key））
- `void EncryptDecrypt(byte[] value, byte key)`
  （void EncryptDecrypt（byte[] value, byte key））
- `ObscuredByte FromEncrypted(byte encrypted)`
  （模糊的Byte FromEncrypted（byte encrypted））
- `void ApplyNewCryptoKey()`
  （void 应用新加密密钥（））
- `void RandomizeCryptoKey()`
  （void 随机化加密密钥（））
- `byte GetEncrypted()`
  （byte 获取Encrypted（））
- `void SetEncrypted(byte encrypted)`
  （void 集合Encrypted（byte encrypted））
- `byte GetDecrypted()`
  （byte 获取Decrypted（））
- `byte InternalDecrypt()`
  （byte 内部的Decrypt（））
- `ObscuredByte op_Implicit(byte value)`
  （模糊的Byte op_Implicit（byte value））
- `byte op_Implicit(ObscuredByte value)`
  （byte op_Implicit（模糊的Byte value））
- `ObscuredByte op_Increment(ObscuredByte input)`
  （模糊的Byte op_Increment（模糊的Byte input））
- `ObscuredByte op_Decrement(ObscuredByte input)`
  （模糊的Byte op_Decrement（模糊的Byte input））
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
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(ObscuredByte obj)`
  （bool Equals（模糊的Byte obj））
- `int CompareTo(ObscuredByte other)`
  （int CompareTo（模糊的Byte other））
- `int CompareTo(byte other)`
  （int CompareTo（byte other））
- `int CompareTo(object obj)`
  （整数 比较到（对象 obj））

---

## ObscuredChar（模糊的Char）

**继承**: IEquatable<ObscuredChar>, IComparable<ObscuredChar>, IComparable<char>, IComparable（IEquatable<模糊的Char>, IComparable<模糊的Char>, IComparable<char>, IComparable）

### 字段 (6)

- `char cryptoKey`（char crypto键）(偏移: 0x0)
- `char currentCryptoKey`（char currentCrypto键）(偏移: 0x0)
- `char hiddenValue`（char hidden值）(偏移: 0x2)
- `bool inited`（布尔值 已初始化）(偏移: 0x4)
- `char fakeValue`（char fake值）(偏移: 0x6)
- `bool fakeValueActive`（布尔值 假值激活的）(偏移: 0x8)

### 方法 (22)

- `void SetNewCryptoKey(char newKey)`
  （void 集合新的Crypto键（char newKey））
- `char EncryptDecrypt(char value)`
  （char EncryptDecrypt（char value））
- `char EncryptDecrypt(char value, char key)`
  （char EncryptDecrypt（char value, char key））
- `ObscuredChar FromEncrypted(char encrypted)`
  （模糊的Char FromEncrypted（char encrypted））
- `void ApplyNewCryptoKey()`
  （void 应用新加密密钥（））
- `void RandomizeCryptoKey()`
  （void 随机化加密密钥（））
- `char GetEncrypted()`
  （char 获取Encrypted（））
- `void SetEncrypted(char encrypted)`
  （void 集合Encrypted（char encrypted））
- `char GetDecrypted()`
  （char 获取Decrypted（））
- `char InternalDecrypt()`
  （char 内部的Decrypt（））
- `ObscuredChar op_Implicit(char value)`
  （模糊的Char op_Implicit（char value））
- `char op_Implicit(ObscuredChar value)`
  （char op_Implicit（模糊的Char value））
- `ObscuredChar op_Increment(ObscuredChar input)`
  （模糊的Char op_Increment（模糊的Char input））
- `ObscuredChar op_Decrement(ObscuredChar input)`
  （模糊的Char op_Decrement（模糊的Char input））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `string ToString()`
  （字符串 转字符串（））
- `string ToString(IFormatProvider provider)`
  （字符串 转字符串（I格式化提供者 provider））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(ObscuredChar obj)`
  （bool Equals（模糊的Char obj））
- `int CompareTo(ObscuredChar other)`
  （int CompareTo（模糊的Char other））
- `int CompareTo(char other)`
  （int CompareTo（char other））
- `int CompareTo(object obj)`
  （整数 比较到（对象 obj））

---

## ObscuredCheatingDetector（模糊的CheatingDetector）

**继承**: ACTkDetectorBase（反作弊检测器基类）

### 字段 (6)

- `int instancesInScene`（int instancesIn场景）(偏移: 0x0)
- `double doubleEpsilon`（double doubleEpsilon）(偏移: 0x20)
- `float floatEpsilon`（float floatEpsilon）(偏移: 0x28)
- `float vector2Epsilon`（float vector2Epsilon）(偏移: 0x2C)
- `float vector3Epsilon`（float vector3Epsilon）(偏移: 0x30)
- `float quaternionEpsilon`（float quaternionEpsilon）(偏移: 0x34)

### 方法 (15)

- `ObscuredCheatingDetector AddToSceneOrGetExisting()`
  （模糊的CheatingDetector 添加To场景Or获取Existing（））
- `void StartDetection()`
  （void 开始Detection（））
- `void StartDetection(Action callback)`
  （void 开始Detection（动作 callback））
- `void StopDetection()`
  （void 停止检测（））
- `void Dispose()`
  （void 释放（））
- `ObscuredCheatingDetector get_Instance()`
  （模糊的CheatingDetector get_实例（））
- `void set_Instance(ObscuredCheatingDetector value)`
  （void set_实例（模糊的CheatingDetector value））
- `ObscuredCheatingDetector get_GetOrCreateInstance()`
  （模糊的CheatingDetector get_获取Or创建实例（））
- `bool get_ExistsAndIsRunning()`
  （bool get_ExistsAnd是否Running（））
- `void Awake()`
  （void 唤醒（））
- `void OnDestroy()`
  （void 销毁时（））
- `void OnLevelWasLoadedNew(Scene scene, LoadSceneMode mode)`
  （void On等级WasLoaded新的（场景 scene, 加载场景模式 mode））
- `void StartDetectionInternal(Action callback)`
  （void 开始Detection内部的（动作 callback））
- `void StartDetectionAutomatically()`
  （void 自动开始检测（））
- `void DisposeInternal()`
  （void 释放内部（））

---

## ObscuredDecimal（模糊的Decimal）

**继承**: IFormattable, IEquatable<ObscuredDecimal>, IComparable<ObscuredDecimal>, IComparable<Decimal>, IComparable（IFormattable, IEquatable<模糊的Decimal>, IComparable<模糊的Decimal>, IComparable<Decimal>, IComparable）

### 字段 (6)

- `long cryptoKey`（long crypto键）(偏移: 0x0)
- `long currentCryptoKey`（long currentCrypto键）(偏移: 0x0)
- `ACTkByte16 hiddenValue`（ACTkByte16 hidden值）(偏移: 0x8)
- `bool inited`（布尔值 已初始化）(偏移: 0x18)
- `Decimal fakeValue`（Decimal fake值）(偏移: 0x1C)
- `bool fakeValueActive`（布尔值 假值激活的）(偏移: 0x2C)

### 方法 (29)

- `void SetNewCryptoKey(long newKey)`
  （void 集合新的Crypto键（long newKey））
- `Decimal Encrypt(Decimal value)`
  （Decimal Encrypt（Decimal value））
- `Decimal Encrypt(Decimal value, long key)`
  （Decimal Encrypt（Decimal value, long key））
- `ACTkByte16 InternalEncrypt(Decimal value)`
  （ACTkByte16 内部的Encrypt（Decimal value））
- `ACTkByte16 InternalEncrypt(Decimal value, long key)`
  （ACTkByte16 内部的Encrypt（Decimal value, long key））
- `Decimal Decrypt(Decimal value)`
  （Decimal Decrypt（Decimal value））
- `Decimal Decrypt(Decimal value, long key)`
  （Decimal Decrypt（Decimal value, long key））
- `ObscuredDecimal FromEncrypted(Decimal encrypted)`
  （模糊的Decimal FromEncrypted（Decimal encrypted））
- `void ApplyNewCryptoKey()`
  （void 应用新加密密钥（））
- `void RandomizeCryptoKey()`
  （void 随机化加密密钥（））
- `Decimal GetEncrypted()`
  （Decimal 获取Encrypted（））
- `void SetEncrypted(Decimal encrypted)`
  （void 集合Encrypted（Decimal encrypted））
- `Decimal GetDecrypted()`
  （Decimal 获取Decrypted（））
- `Decimal InternalDecrypt()`
  （Decimal 内部的Decrypt（））
- `ObscuredDecimal op_Implicit(Decimal value)`
  （模糊的Decimal op_Implicit（Decimal value））
- `Decimal op_Implicit(ObscuredDecimal value)`
  （Decimal op_Implicit（模糊的Decimal value））
- `ObscuredDecimal op_Explicit(ObscuredFloat f)`
  （模糊的Decimal op_Explicit（模糊的浮点数 f））
- `ObscuredDecimal op_Increment(ObscuredDecimal input)`
  （模糊的Decimal op_Increment（模糊的Decimal input））
- `ObscuredDecimal op_Decrement(ObscuredDecimal input)`
  （模糊的Decimal op_Decrement（模糊的Decimal input））
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
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(ObscuredDecimal obj)`
  （bool Equals（模糊的Decimal obj））
- `int CompareTo(ObscuredDecimal other)`
  （int CompareTo（模糊的Decimal other））
- `int CompareTo(Decimal other)`
  （int CompareTo（Decimal other））
- `int CompareTo(object obj)`
  （整数 比较到（对象 obj））

---

## ObscuredDecimal.DecimalLongBytesUnion（模糊的Decimal.DecimalLongBytesUnion）

### 字段 (4)

- `Decimal d`（Decimal d）(偏移: 0x0)
- `long l1`（long l1）(偏移: 0x0)
- `long l2`（long l2）(偏移: 0x8)
- `ACTkByte16 b16`（ACTkByte16 b16）(偏移: 0x0)

---

## ObscuredDouble（模糊的Double）

**继承**: IFormattable, IEquatable<ObscuredDouble>, IComparable<ObscuredDouble>, IComparable<double>, IComparable（IFormattable, IEquatable<模糊的Double>, IComparable<模糊的Double>, IComparable<double>, IComparable）

### 字段 (7)

- `long cryptoKey`（long crypto键）(偏移: 0x0)
- `long currentCryptoKey`（long currentCrypto键）(偏移: 0x0)
- `long hiddenValue`（long hidden值）(偏移: 0x8)
- `ACTkByte8 hiddenValueOldByte8`（ACTkByte8 hidden值旧的Byte8）(偏移: 0x10)
- `bool inited`（布尔值 已初始化）(偏移: 0x18)
- `double fakeValue`（double fake值）(偏移: 0x20)
- `bool fakeValueActive`（布尔值 假值激活的）(偏移: 0x28)

### 方法 (29)

- `void SetNewCryptoKey(long newKey)`
  （void 集合新的Crypto键（long newKey））
- `long Encrypt(double value)`
  （long Encrypt（double value））
- `long Encrypt(double value, long key)`
  （long Encrypt（double value, long key））
- `long InternalEncrypt(double value, long key = 0)`
  （long 内部的Encrypt（double value, long key = 0））
- `double Decrypt(long value)`
  （double Decrypt（long value））
- `double Decrypt(long value, long key)`
  （double Decrypt（long value, long key））
- `long MigrateEncrypted(long encrypted, byte fromVersion = 0, byte toVersion = 2)`
  （long MigrateEncrypted（long encrypted, byte fromVersion = 0, byte toVersion = 2））
- `ObscuredDouble FromEncrypted(long encrypted)`
  （模糊的Double FromEncrypted（long encrypted））
- `void ApplyNewCryptoKey()`
  （void 应用新加密密钥（））
- `void RandomizeCryptoKey()`
  （void 随机化加密密钥（））
- `long GetEncrypted()`
  （long 获取Encrypted（））
- `void SetEncrypted(long encrypted)`
  （void 集合Encrypted（long encrypted））
- `double GetDecrypted()`
  （double 获取Decrypted（））
- `double InternalDecrypt()`
  （double 内部的Decrypt（））
- `ObscuredDouble op_Implicit(double value)`
  （模糊的Double op_Implicit（double value））
- `double op_Implicit(ObscuredDouble value)`
  （double op_Implicit（模糊的Double value））
- `ObscuredDouble op_Explicit(ObscuredFloat f)`
  （模糊的Double op_Explicit（模糊的浮点数 f））
- `ObscuredDouble op_Increment(ObscuredDouble input)`
  （模糊的Double op_Increment（模糊的Double input））
- `ObscuredDouble op_Decrement(ObscuredDouble input)`
  （模糊的Double op_Decrement（模糊的Double input））
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
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(ObscuredDouble obj)`
  （bool Equals（模糊的Double obj））
- `int CompareTo(ObscuredDouble other)`
  （int CompareTo（模糊的Double other））
- `int CompareTo(double other)`
  （int CompareTo（double other））
- `int CompareTo(object obj)`
  （整数 比较到（对象 obj））

---

## ObscuredDouble.DoubleLongBytesUnion（模糊的Double.DoubleLongBytesUnion）

### 字段 (3)

- `double d`（double d）(偏移: 0x0)
- `long l`（long l）(偏移: 0x0)
- `ACTkByte8 b8`（ACTkByte8 b8）(偏移: 0x0)

---

## ObscuredFloat（模糊的浮点数）

**继承**: IFormattable, IEquatable<ObscuredFloat>, IComparable<ObscuredFloat>, IComparable<float>, IComparable（IFormattable, IEquatable<模糊的Float>, IComparable<模糊的Float>, IComparable<float>, IComparable）

### 字段 (7)

- `int cryptoKey`（整数 加密密钥）(偏移: 0x0)
- `int currentCryptoKey`（整数 当前加密密钥）(偏移: 0x0)
- `int hiddenValue`（int hidden值）(偏移: 0x4)
- `ACTkByte4 hiddenValueOldByte4`（ACTkByte4 hidden值旧的Byte4）(偏移: 0x8)
- `bool inited`（布尔值 已初始化）(偏移: 0xC)
- `float fakeValue`（float fake值）(偏移: 0x10)
- `bool fakeValueActive`（布尔值 假值激活的）(偏移: 0x14)

### 方法 (28)

- `void SetNewCryptoKey(int newKey)`
  （void 设置新加密密钥（整数 newKey））
- `int Encrypt(float value)`
  （int Encrypt（float value））
- `int Encrypt(float value, int key)`
  （int Encrypt（float value, int key））
- `int InternalEncrypt(float value, int key = 0)`
  （int 内部的Encrypt（float value, int key = 0））
- `float Decrypt(int value)`
  （float Decrypt（int value））
- `float Decrypt(int value, int key)`
  （float Decrypt（int value, int key））
- `int MigrateEncrypted(int encrypted, byte fromVersion = 0, byte toVersion = 2)`
  （int MigrateEncrypted（int encrypted, byte fromVersion = 0, byte toVersion = 2））
- `ObscuredFloat FromEncrypted(int encrypted)`
  （模糊的浮点数 FromEncrypted（int encrypted））
- `void ApplyNewCryptoKey()`
  （void 应用新加密密钥（））
- `void RandomizeCryptoKey()`
  （void 随机化加密密钥（））
- `int GetEncrypted()`
  （int 获取Encrypted（））
- `void SetEncrypted(int encrypted)`
  （void 集合Encrypted（int encrypted））
- `float GetDecrypted()`
  （float 获取Decrypted（））
- `float InternalDecrypt()`
  （float 内部的Decrypt（））
- `ObscuredFloat op_Implicit(float value)`
  （模糊的浮点数 op_Implicit（float value））
- `float op_Implicit(ObscuredFloat value)`
  （float op_Implicit（模糊的浮点数 value））
- `ObscuredFloat op_Increment(ObscuredFloat input)`
  （模糊的浮点数 op_Increment（模糊的浮点数 input））
- `ObscuredFloat op_Decrement(ObscuredFloat input)`
  （模糊的浮点数 op_Decrement（模糊的浮点数 input））
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
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(ObscuredFloat obj)`
  （bool Equals（模糊的浮点数 obj））
- `int CompareTo(ObscuredFloat other)`
  （int CompareTo（模糊的浮点数 other））
- `int CompareTo(float other)`
  （int CompareTo（float other））
- `int CompareTo(object obj)`
  （整数 比较到（对象 obj））

---

## ObscuredFloat.FloatIntBytesUnion（模糊的Float.浮点数整数BytesUnion）

### 字段 (3)

- `float f`（float f）(偏移: 0x0)
- `int i`（int i）(偏移: 0x0)
- `ACTkByte4 b4`（ACTkByte4 b4）(偏移: 0x0)

---

## ObscuredInt（模糊整数）

**继承**: IFormattable, IEquatable<ObscuredInt>, IComparable<ObscuredInt>, IComparable<int>, IComparable（IFormattable, IEquatable<模糊的Int>, IComparable<模糊的Int>, IComparable<int>, IComparable）

### 字段 (6)

- `int cryptoKey`（整数 加密密钥）(偏移: 0x0)
- `int currentCryptoKey`（整数 当前加密密钥）(偏移: 0x0)
- `int hiddenValue`（int hidden值）(偏移: 0x4)
- `bool inited`（布尔值 已初始化）(偏移: 0x8)
- `int fakeValue`（int fake值）(偏移: 0xC)
- `bool fakeValueActive`（布尔值 假值激活的）(偏移: 0x10)

### 方法 (29)

- `void SetNewCryptoKey(int newKey)`
  （void 设置新加密密钥（整数 newKey））
- `int Encrypt(int value)`
  （int Encrypt（int value））
- `int Encrypt(int value, int key)`
  （int Encrypt（int value, int key））
- `int Decrypt(int value)`
  （int Decrypt（int value））
- `int Decrypt(int value, int key)`
  （int Decrypt（int value, int key））
- `ObscuredInt FromEncrypted(int encrypted)`
  （模糊整数 FromEncrypted（int encrypted））
- `void ApplyNewCryptoKey()`
  （void 应用新加密密钥（））
- `void RandomizeCryptoKey()`
  （void 随机化加密密钥（））
- `int GetEncrypted()`
  （int 获取Encrypted（））
- `void SetEncrypted(int encrypted)`
  （void 集合Encrypted（int encrypted））
- `int GetDecrypted()`
  （int 获取Decrypted（））
- `int InternalDecrypt()`
  （int 内部的Decrypt（））
- `ObscuredInt op_Implicit(int value)`
  （模糊整数 op_Implicit（int value））
- `int op_Implicit(ObscuredInt value)`
  （int op_Implicit（模糊整数 value））
- `ObscuredFloat op_Implicit(ObscuredInt value)`
  （模糊的浮点数 op_Implicit（模糊整数 value））
- `ObscuredDouble op_Implicit(ObscuredInt value)`
  （模糊的Double op_Implicit（模糊整数 value））
- `ObscuredUInt op_Explicit(ObscuredInt value)`
  （模糊的U整数 op_Explicit（模糊整数 value））
- `ObscuredInt op_Increment(ObscuredInt input)`
  （模糊整数 op_Increment（模糊整数 input））
- `ObscuredInt op_Decrement(ObscuredInt input)`
  （模糊整数 op_Decrement（模糊整数 input））
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
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(ObscuredInt obj)`
  （bool Equals（模糊整数 obj））
- `int CompareTo(ObscuredInt other)`
  （int CompareTo（模糊整数 other））
- `int CompareTo(int other)`
  （int CompareTo（int other））
- `int CompareTo(object obj)`
  （整数 比较到（对象 obj））

---

## ObscuredLong（模糊的Long）

**继承**: IFormattable, IEquatable<ObscuredLong>, IComparable<ObscuredLong>, IComparable<long>, IComparable（IFormattable, IEquatable<模糊的Long>, IComparable<模糊的Long>, IComparable<long>, IComparable）

### 字段 (6)

- `long cryptoKey`（long crypto键）(偏移: 0x0)
- `long currentCryptoKey`（long currentCrypto键）(偏移: 0x0)
- `long hiddenValue`（long hidden值）(偏移: 0x8)
- `bool inited`（布尔值 已初始化）(偏移: 0x10)
- `long fakeValue`（long fake值）(偏移: 0x18)
- `bool fakeValueActive`（布尔值 假值激活的）(偏移: 0x20)

### 方法 (26)

- `void SetNewCryptoKey(long newKey)`
  （void 集合新的Crypto键（long newKey））
- `long Encrypt(long value)`
  （long Encrypt（long value））
- `long Decrypt(long value)`
  （long Decrypt（long value））
- `long Encrypt(long value, long key)`
  （long Encrypt（long value, long key））
- `long Decrypt(long value, long key)`
  （long Decrypt（long value, long key））
- `ObscuredLong FromEncrypted(long encrypted)`
  （模糊的Long FromEncrypted（long encrypted））
- `void ApplyNewCryptoKey()`
  （void 应用新加密密钥（））
- `void RandomizeCryptoKey()`
  （void 随机化加密密钥（））
- `long GetEncrypted()`
  （long 获取Encrypted（））
- `void SetEncrypted(long encrypted)`
  （void 集合Encrypted（long encrypted））
- `long GetDecrypted()`
  （long 获取Decrypted（））
- `long InternalDecrypt()`
  （long 内部的Decrypt（））
- `ObscuredLong op_Implicit(long value)`
  （模糊的Long op_Implicit（long value））
- `long op_Implicit(ObscuredLong value)`
  （long op_Implicit（模糊的Long value））
- `ObscuredLong op_Increment(ObscuredLong input)`
  （模糊的Long op_Increment（模糊的Long input））
- `ObscuredLong op_Decrement(ObscuredLong input)`
  （模糊的Long op_Decrement（模糊的Long input））
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
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(ObscuredLong obj)`
  （bool Equals（模糊的Long obj））
- `int CompareTo(ObscuredLong other)`
  （int CompareTo（模糊的Long other））
- `int CompareTo(long other)`
  （int CompareTo（long other））
- `int CompareTo(object obj)`
  （整数 比较到（对象 obj））

---

## ObscuredPerformanceTests（模糊的PerformanceTests）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (25)

- `bool boolTest`（bool boolTest）(偏移: 0xC)
- `int boolIterations`（int boolIterations）(偏移: 0x10)
- `bool byteTest`（bool byteTest）(偏移: 0x14)
- `int byteIterations`（int byteIterations）(偏移: 0x18)
- `bool shortTest`（bool shortTest）(偏移: 0x1C)
- `int shortIterations`（int shortIterations）(偏移: 0x20)
- `bool ushortTest`（bool ushortTest）(偏移: 0x24)
- `int ushortIterations`（int ushortIterations）(偏移: 0x28)
- `bool intTest`（bool intTest）(偏移: 0x2C)
- `int intIterations`（int intIterations）(偏移: 0x30)
- `bool uintTest`（bool uintTest）(偏移: 0x34)
- `int uintIterations`（int uintIterations）(偏移: 0x38)
- `bool longTest`（bool longTest）(偏移: 0x3C)
- `int longIterations`（int longIterations）(偏移: 0x40)
- `bool floatTest`（bool floatTest）(偏移: 0x44)
- `int floatIterations`（int floatIterations）(偏移: 0x48)
- `bool doubleTest`（bool doubleTest）(偏移: 0x4C)
- `int doubleIterations`（int doubleIterations）(偏移: 0x50)
- `bool stringTest`（bool stringTest）(偏移: 0x54)
- `int stringIterations`（int stringIterations）(偏移: 0x58)
- `bool vector3Test`（bool vector3Test）(偏移: 0x5C)
- `int vector3Iterations`（int vector3Iterations）(偏移: 0x60)
- `bool prefsTest`（bool prefsTest）(偏移: 0x64)
- `int prefsIterations`（int prefsIterations）(偏移: 0x68)
- `StringBuilder logBuilder`（字符串构建器 log构建器）(偏移: 0x6C)

### 方法 (14)

- `void Start()`
  （void 开始（））
- `void StartTests()`
  （void 开始Tests（））
- `void TestBool()`
  （void Test布尔值（））
- `void TestByte()`
  （void TestByte（））
- `void TestShort()`
  （void TestShort（））
- `void TestUShort()`
  （void TestUShort（））
- `void TestDouble()`
  （void TestDouble（））
- `void TestFloat()`
  （void Test浮点数（））
- `void TestInt()`
  （void Test整数（））
- `void TestLong()`
  （void TestLong（））
- `void TestString()`
  （void Test字符串（））
- `void TestUInt()`
  （void TestU整数（））
- `void TestVector3()`
  （void Test三维向量（））
- `void TestPrefs()`
  （void TestPrefs（））

---

## ObscuredPrefs（模糊的Prefs）

### 字段 (14)

- `bool alterationReported`（bool alterationReported）(偏移: 0x0)
- `bool foreignSavesReported`（bool foreignSavesReported）(偏移: 0x1)
- `string cryptoKey`（string crypto键）(偏移: 0x4)
- `string deviceId`（string deviceId）(偏移: 0x8)
- `uint deviceIdHash`（uint deviceIdHash）(偏移: 0xC)
- `Action onAlterationDetected`（动作 onAlterationDetected）(偏移: 0x10)
- `Action OnAlterationDetected`（动作 OnAlterationDetected）(偏移: 0x14)
- `Action onPossibleForeignSavesDetected`（动作 onPossibleForeignSavesDetected）(偏移: 0x18)
- `Action OnPossibleForeignSavesDetected`（动作 OnPossibleForeignSavesDetected）(偏移: 0x1C)
- `bool preservePlayerPrefs`（bool preserve玩家Prefs）(偏移: 0x20)
- `ObscuredPrefs.DeviceLockLevel lockToDevice`（模糊的Prefs.DeviceLock等级 lockToDevice）(偏移: 0x21)
- `bool readForeignSaves`（bool readForeignSaves）(偏移: 0x22)
- `bool emergencyMode`（bool emergency模式）(偏移: 0x23)
- `string deprecatedDeviceId`（string deprecatedDeviceId）(偏移: 0x24)

### 方法 (107)

- `void set_CryptoKey(string value)`
  （void set_Crypto键（string value））
- `string get_CryptoKey()`
  （string get_Crypto键（））
- `string get_DeviceId()`
  （string get_DeviceId（））
- `void set_DeviceId(string value)`
  （void set_DeviceId（string value））
- `string get_DeviceID()`
  （string get_DeviceID（））
- `void set_DeviceID(string value)`
  （void set_DeviceID（string value））
- `uint get_DeviceIdHash()`
  （uint get_DeviceIdHash（））
- `void add_OnAlterationDetected(Action value)`
  （void add_OnAlterationDetected（动作 value））
- `void remove_OnAlterationDetected(Action value)`
  （void remove_OnAlterationDetected（动作 value））
- `void add_OnPossibleForeignSavesDetected(Action value)`
  （void add_OnPossibleForeignSavesDetected（动作 value））
- `void remove_OnPossibleForeignSavesDetected(Action value)`
  （void remove_OnPossibleForeignSavesDetected（动作 value））
- `void ForceLockToDeviceInit()`
  （void 强制LockToDevice初始化（））
- `void SetNewCryptoKey(string newKey)`
  （void 集合新的Crypto键（string newKey））
- `void SetInt(string key, int value)`
  （void 集合整数（string key, int value））
- `int GetInt(string key)`
  （int 获取整数（string key））
- `int GetInt(string key, int defaultValue)`
  （int 获取整数（string key, int defaultValue））
- `string EncryptIntValue(string key, int value)`
  （string Encrypt整数值（string key, int value））
- `int DecryptIntValue(string key, string encryptedInput, int defaultValue)`
  （int Decrypt整数值（string key, string encryptedInput, int defaultValue））
- `void SetUInt(string key, uint value)`
  （void 集合U整数（string key, uint value））
- `uint GetUInt(string key)`
  （uint 获取U整数（string key））
- `uint GetUInt(string key, uint defaultValue)`
  （uint 获取U整数（string key, uint defaultValue））
- `string EncryptUIntValue(string key, uint value)`
  （string EncryptU整数值（string key, uint value））
- `uint DecryptUIntValue(string key, string encryptedInput, uint defaultValue)`
  （uint DecryptU整数值（string key, string encryptedInput, uint defaultValue））
- `void SetString(string key, string value)`
  （void 集合字符串（string key, string value））
- `string GetString(string key)`
  （string 获取字符串（string key））
- `string GetString(string key, string defaultValue)`
  （string 获取字符串（string key, string defaultValue））
- `string EncryptStringValue(string key, string value)`
  （string Encrypt字符串值（string key, string value））
- `string DecryptStringValue(string key, string encryptedInput, string defaultValue)`
  （string Decrypt字符串值（string key, string encryptedInput, string defaultValue））
- `void SetFloat(string key, float value)`
  （void 集合浮点数（string key, float value））
- `float GetFloat(string key)`
  （float 获取浮点数（string key））
- `float GetFloat(string key, float defaultValue)`
  （float 获取浮点数（string key, float defaultValue））
- `string EncryptFloatValue(string key, float value)`
  （string Encrypt浮点数值（string key, float value））
- `float DecryptFloatValue(string key, string encryptedInput, float defaultValue)`
  （float Decrypt浮点数值（string key, string encryptedInput, float defaultValue））
- `void SetDouble(string key, double value)`
  （void 集合Double（string key, double value））
- `double GetDouble(string key)`
  （double 获取Double（string key））
- `double GetDouble(string key, double defaultValue)`
  （double 获取Double（string key, double defaultValue））
- `string EncryptDoubleValue(string key, double value)`
  （string EncryptDouble值（string key, double value））
- `double DecryptDoubleValue(string key, string encryptedInput, double defaultValue)`
  （double DecryptDouble值（string key, string encryptedInput, double defaultValue））
- `void SetDecimal(string key, Decimal value)`
  （void 集合Decimal（string key, Decimal value））
- `Decimal GetDecimal(string key)`
  （Decimal 获取Decimal（string key））
- `Decimal GetDecimal(string key, Decimal defaultValue)`
  （Decimal 获取Decimal（string key, Decimal defaultValue））
- `string EncryptDecimalValue(string key, Decimal value)`
  （string EncryptDecimal值（string key, Decimal value））
- `Decimal DecryptDecimalValue(string key, string encryptedInput, Decimal defaultValue)`
  （Decimal DecryptDecimal值（string key, string encryptedInput, Decimal defaultValue））
- `void SetLong(string key, long value)`
  （void 集合Long（string key, long value））
- `long GetLong(string key)`
  （long 获取Long（string key））
- `long GetLong(string key, long defaultValue)`
  （long 获取Long（string key, long defaultValue））
- `string EncryptLongValue(string key, long value)`
  （string EncryptLong值（string key, long value））
- `long DecryptLongValue(string key, string encryptedInput, long defaultValue)`
  （long DecryptLong值（string key, string encryptedInput, long defaultValue））
- `void SetULong(string key, ulong value)`
  （void 集合ULong（string key, ulong value））
- `ulong GetULong(string key)`
  （ulong 获取ULong（string key））
- `ulong GetULong(string key, ulong defaultValue)`
  （ulong 获取ULong（string key, ulong defaultValue））
- `string EncryptULongValue(string key, ulong value)`
  （string EncryptULong值（string key, ulong value））
- `ulong DecryptULongValue(string key, string encryptedInput, ulong defaultValue)`
  （ulong DecryptULong值（string key, string encryptedInput, ulong defaultValue））
- `void SetBool(string key, bool value)`
  （void 集合布尔值（string key, bool value））
- `bool GetBool(string key)`
  （bool 获取布尔值（string key））
- `bool GetBool(string key, bool defaultValue)`
  （bool 获取布尔值（string key, bool defaultValue））
- `string EncryptBoolValue(string key, bool value)`
  （string Encrypt布尔值值（string key, bool value））
- `bool DecryptBoolValue(string key, string encryptedInput, bool defaultValue)`
  （bool Decrypt布尔值值（string key, string encryptedInput, bool defaultValue））
- `void SetByteArray(string key, byte[] value)`
  （void 集合Byte数组（string key, byte[] value））
- `byte[] GetByteArray(string key)`
  （byte[] 获取Byte数组（string key））
- `byte[] GetByteArray(string key, byte defaultValue, int defaultLength)`
  （byte[] 获取Byte数组（string key, byte defaultValue, int defaultLength））
- `string EncryptByteArrayValue(string key, byte[] value)`
  （string EncryptByte数组值（string key, byte[] value））
- `byte[] DecryptByteArrayValue(string key, string encryptedInput, byte defaultValue, int defaultLength)`
  （byte[] DecryptByte数组值（string key, string encryptedInput, byte defaultValue, int defaultLength））
- `byte[] ConstructByteArray(byte value, int length)`
  （byte[] ConstructByte数组（byte value, int length））
- `void SetVector2(string key, Vector2 value)`
  （void 集合二维向量（string key, 二维向量 value））
- `Vector2 GetVector2(string key)`
  （二维向量 获取二维向量（string key））
- `Vector2 GetVector2(string key, Vector2 defaultValue)`
  （二维向量 获取二维向量（string key, 二维向量 defaultValue））
- `string EncryptVector2Value(string key, Vector2 value)`
  （string Encrypt二维向量值（string key, 二维向量 value））
- `Vector2 DecryptVector2Value(string key, string encryptedInput, Vector2 defaultValue)`
  （二维向量 Decrypt二维向量值（string key, string encryptedInput, 二维向量 defaultValue））
- `void SetVector3(string key, Vector3 value)`
  （void 集合三维向量（string key, 三维向量 value））
- `Vector3 GetVector3(string key)`
  （三维向量 获取三维向量（string key））
- `Vector3 GetVector3(string key, Vector3 defaultValue)`
  （三维向量 获取三维向量（string key, 三维向量 defaultValue））
- `string EncryptVector3Value(string key, Vector3 value)`
  （string Encrypt三维向量值（string key, 三维向量 value））
- `Vector3 DecryptVector3Value(string key, string encryptedInput, Vector3 defaultValue)`
  （三维向量 Decrypt三维向量值（string key, string encryptedInput, 三维向量 defaultValue））
- `void SetQuaternion(string key, Quaternion value)`
  （void 集合Quaternion（string key, Quaternion value））
- `Quaternion GetQuaternion(string key)`
  （Quaternion 获取Quaternion（string key））
- `Quaternion GetQuaternion(string key, Quaternion defaultValue)`
  （Quaternion 获取Quaternion（string key, Quaternion defaultValue））
- `string EncryptQuaternionValue(string key, Quaternion value)`
  （string EncryptQuaternion值（string key, Quaternion value））
- `Quaternion DecryptQuaternionValue(string key, string encryptedInput, Quaternion defaultValue)`
  （Quaternion DecryptQuaternion值（string key, string encryptedInput, Quaternion defaultValue））
- `void SetColor(string key, Color32 value)`
  （void 集合颜色（string key, Color32 value））
- `Color32 GetColor(string key)`
  （Color32 获取颜色（string key））
- `Color32 GetColor(string key, Color32 defaultValue)`
  （Color32 获取颜色（string key, Color32 defaultValue））
- `string EncryptColorValue(string key, uint value)`
  （string Encrypt颜色值（string key, uint value））
- `void SetRect(string key, Rect value)`
  （void 集合Rect（string key, Rect value））
- `Rect GetRect(string key)`
  （Rect 获取Rect（string key））
- `Rect GetRect(string key, Rect defaultValue)`
  （Rect 获取Rect（string key, Rect defaultValue））
- `string EncryptRectValue(string key, Rect value)`
  （string EncryptRect值（string key, Rect value））
- `Rect DecryptRectValue(string key, string encryptedInput, Rect defaultValue)`
  （Rect DecryptRect值（string key, string encryptedInput, Rect defaultValue））
- `void SetRawValue(string key, string encryptedValue)`
  （void 集合Raw值（string key, string encryptedValue））
- `string GetRawValue(string key)`
  （string 获取Raw值（string key））
- `ObscuredPrefs.DataType GetRawValueType(string value)`
  （模糊的Prefs.数据类型 获取Raw值类型（string value））
- `string EncryptKey(string key)`
  （string Encrypt键（string key））
- `bool HasKey(string key)`
  （bool 是否有键（string key））
- `void DeleteKey(string key)`
  （void Delete键（string key））
- `void DeleteAll()`
  （void Delete所有（））
- `void Save()`
  （void 保存（））
- `string GetEncryptedPrefsString(string key, string encryptedKey)`
  （string 获取EncryptedPrefs字符串（string key, string encryptedKey））
- `string EncryptData(string key, byte[] cleanBytes, ObscuredPrefs.DataType type)`
  （string Encrypt数据（string key, byte[] cleanBytes, 模糊的Prefs.数据类型 type））
- `byte[] DecryptData(string key, string encryptedInput)`
  （byte[] Decrypt数据（string key, string encryptedInput））
- `uint CalculateChecksum(string input)`
  （uint 计算Checksum（string input））
- `void SavesTampered()`
  （void SavesTampered（））
- `void PossibleForeignSavesDetected()`
  （void PossibleForeignSavesDetected（））
- `string GetDeviceId()`
  （string 获取DeviceId（））
- `byte[] EncryptDecryptBytes(byte[] bytes, int dataLength, string key)`
  （byte[] EncryptDecryptBytes（byte[] bytes, int dataLength, string key））
- `string DeprecatedDecryptValue(string value)`
  （string DeprecatedDecrypt值（string value））
- `string DeprecatedCalculateChecksum(string input)`
  （string Deprecated计算Checksum（string input））
- `string get_DeprecatedDeviceId()`
  （string get_DeprecatedDeviceId（））

---

## ObscuredPrefs.DataType（模糊的Prefs.数据类型）

### 字段 (1)

- `byte value__`（字节 值__）(偏移: 0x0)

---

## ObscuredPrefs.DeviceLockLevel（模糊的Prefs.DeviceLock等级）

### 字段 (1)

- `byte value__`（字节 值__）(偏移: 0x0)

---

## ObscuredPrefsExamples（模糊的PrefsExamples）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (5)

- `string prefsEncryptionKey`（string prefsEncryption键）(偏移: 0xC)
- `string regularPrefs`（string regularPrefs）(偏移: 0x10)
- `string obscuredPrefs`（string obscuredPrefs）(偏移: 0x14)
- `bool savesAlterationDetected`（bool savesAlterationDetected）(偏移: 0x18)
- `bool foreignSavesDetected`（bool foreignSavesDetected）(偏移: 0x19)

### 方法 (17)

- `bool get_PreservePlayerPrefs()`
  （bool get_Preserve玩家Prefs（））
- `void set_PreservePlayerPrefs(bool value)`
  （void set_Preserve玩家Prefs（bool value））
- `bool get_EmergencyMode()`
  （bool get_Emergency模式（））
- `void set_EmergencyMode(bool value)`
  （void set_Emergency模式（bool value））
- `bool get_ReadForeignSaves()`
  （bool get_ReadForeignSaves（））
- `void set_ReadForeignSaves(bool value)`
  （void set_ReadForeignSaves（bool value））
- `void Awake()`
  （void 唤醒（））
- `void OnDestroy()`
  （void 销毁时（））
- `void SavesAlterationDetected()`
  （void SavesAlterationDetected（））
- `void ForeignSavesDetected()`
  （void ForeignSavesDetected（））
- `void LoadRegularPrefs()`
  （void 加载RegularPrefs（））
- `void SaveRegularPrefs()`
  （void 保存RegularPrefs（））
- `void DeleteRegularPrefs()`
  （void DeleteRegularPrefs（））
- `void LockObscuredPrefsToDevice(ObscuredPrefs.DeviceLockLevel level)`
  （void Lock模糊的PrefsToDevice（模糊的Prefs.DeviceLock等级 level））
- `void LoadObscuredPrefs()`
  （void 加载模糊的Prefs（））
- `void SaveObscuredPrefs()`
  （void 保存模糊的Prefs（））
- `void DeleteObscuredPrefs()`
  （void Delete模糊的Prefs（））

---

## ObscuredQuaternion（模糊的Quaternion）

### 字段 (7)

- `int cryptoKey`（整数 加密密钥）(偏移: 0x0)
- `Quaternion identity`（Quaternion identity）(偏移: 0x4)
- `int currentCryptoKey`（整数 当前加密密钥）(偏移: 0x0)
- `ObscuredQuaternion.RawEncryptedQuaternion hiddenValue`（模糊的Quaternion.RawEncryptedQuaternion hidden值）(偏移: 0x4)
- `bool inited`（布尔值 已初始化）(偏移: 0x14)
- `Quaternion fakeValue`（Quaternion fake值）(偏移: 0x18)
- `bool fakeValueActive`（布尔值 假值激活的）(偏移: 0x28)

### 方法 (19)

- `void SetNewCryptoKey(int newKey)`
  （void 设置新加密密钥（整数 newKey））
- `ObscuredQuaternion.RawEncryptedQuaternion Encrypt(Quaternion value)`
  （模糊的Quaternion.RawEncryptedQuaternion Encrypt（Quaternion value））
- `ObscuredQuaternion.RawEncryptedQuaternion Encrypt(Quaternion value, int key)`
  （模糊的Quaternion.RawEncryptedQuaternion Encrypt（Quaternion value, int key））
- `ObscuredQuaternion.RawEncryptedQuaternion Encrypt(float x, float y, float z, float w, int key)`
  （模糊的Quaternion.RawEncryptedQuaternion Encrypt（float x, float y, float z, float w, int key））
- `Quaternion Decrypt(ObscuredQuaternion.RawEncryptedQuaternion value)`
  （Quaternion Decrypt（模糊的Quaternion.RawEncryptedQuaternion value））
- `Quaternion Decrypt(ObscuredQuaternion.RawEncryptedQuaternion value, int key)`
  （Quaternion Decrypt（模糊的Quaternion.RawEncryptedQuaternion value, int key））
- `ObscuredQuaternion FromEncrypted(ObscuredQuaternion.RawEncryptedQuaternion encrypted)`
  （模糊的Quaternion FromEncrypted（模糊的Quaternion.RawEncryptedQuaternion encrypted））
- `void ApplyNewCryptoKey()`
  （void 应用新加密密钥（））
- `void RandomizeCryptoKey()`
  （void 随机化加密密钥（））
- `ObscuredQuaternion.RawEncryptedQuaternion GetEncrypted()`
  （模糊的Quaternion.RawEncryptedQuaternion 获取Encrypted（））
- `void SetEncrypted(ObscuredQuaternion.RawEncryptedQuaternion encrypted)`
  （void 集合Encrypted（模糊的Quaternion.RawEncryptedQuaternion encrypted））
- `Quaternion GetDecrypted()`
  （Quaternion 获取Decrypted（））
- `Quaternion InternalDecrypt()`
  （Quaternion 内部的Decrypt（））
- `bool CompareQuaternionsWithTolerance(Quaternion q1, Quaternion q2)`
  （bool CompareQuaternionsWithTolerance（Quaternion q1, Quaternion q2））
- `ObscuredQuaternion op_Implicit(Quaternion value)`
  （模糊的Quaternion op_Implicit（Quaternion value））
- `Quaternion op_Implicit(ObscuredQuaternion value)`
  （Quaternion op_Implicit（模糊的Quaternion value））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `string ToString()`
  （字符串 转字符串（））
- `string ToString(string format)`
  （字符串 转字符串（字符串 格式））

---

## ObscuredQuaternion.RawEncryptedQuaternion（模糊的Quaternion.RawEncryptedQuaternion）

### 字段 (4)

- `int x`（整数 x）(偏移: 0x0)
- `int y`（整数 y）(偏移: 0x4)
- `int z`（整数 z）(偏移: 0x8)
- `int w`（int w）(偏移: 0xC)

---

## ObscuredSByte（模糊的SByte）

**继承**: IFormattable, IEquatable<ObscuredSByte>, IComparable<ObscuredSByte>, IComparable<sbyte>, IComparable（IFormattable, IEquatable<模糊的SByte>, IComparable<模糊的SByte>, IComparable<sbyte>, IComparable）

### 字段 (6)

- `sbyte cryptoKey`（sbyte crypto键）(偏移: 0x0)
- `sbyte currentCryptoKey`（sbyte currentCrypto键）(偏移: 0x0)
- `sbyte hiddenValue`（sbyte hidden值）(偏移: 0x0)
- `bool inited`（布尔值 已初始化）(偏移: 0x0)
- `sbyte fakeValue`（sbyte fake值）(偏移: 0x0)
- `bool fakeValueActive`（布尔值 假值激活的）(偏移: 0x0)

### 方法 (24)

- `void SetNewCryptoKey(sbyte newKey)`
  （void 集合新的Crypto键（sbyte newKey））
- `sbyte EncryptDecrypt(sbyte value)`
  （sbyte EncryptDecrypt（sbyte value））
- `sbyte EncryptDecrypt(sbyte value, sbyte key)`
  （sbyte EncryptDecrypt（sbyte value, sbyte key））
- `ObscuredSByte FromEncrypted(sbyte encrypted)`
  （模糊的SByte FromEncrypted（sbyte encrypted））
- `void ApplyNewCryptoKey()`
  （void 应用新加密密钥（））
- `void RandomizeCryptoKey()`
  （void 随机化加密密钥（））
- `sbyte GetEncrypted()`
  （sbyte 获取Encrypted（））
- `void SetEncrypted(sbyte encrypted)`
  （void 集合Encrypted（sbyte encrypted））
- `sbyte GetDecrypted()`
  （sbyte 获取Decrypted（））
- `sbyte InternalDecrypt()`
  （sbyte 内部的Decrypt（））
- `ObscuredSByte op_Implicit(sbyte value)`
  （模糊的SByte op_Implicit（sbyte value））
- `sbyte op_Implicit(ObscuredSByte value)`
  （sbyte op_Implicit（模糊的SByte value））
- `ObscuredSByte op_Increment(ObscuredSByte input)`
  （模糊的SByte op_Increment（模糊的SByte input））
- `ObscuredSByte op_Decrement(ObscuredSByte input)`
  （模糊的SByte op_Decrement（模糊的SByte input））
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
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(ObscuredSByte obj)`
  （bool Equals（模糊的SByte obj））
- `int CompareTo(ObscuredSByte other)`
  （int CompareTo（模糊的SByte other））
- `int CompareTo(sbyte other)`
  （int CompareTo（sbyte other））
- `int CompareTo(object obj)`
  （整数 比较到（对象 obj））

---

## ObscuredShort（模糊的Short）

**继承**: IFormattable, IEquatable<ObscuredShort>, IComparable<ObscuredShort>, IComparable<short>, IComparable（IFormattable, IEquatable<模糊的Short>, IComparable<模糊的Short>, IComparable<short>, IComparable）

### 字段 (6)

- `short cryptoKey`（short crypto键）(偏移: 0x0)
- `short currentCryptoKey`（short currentCrypto键）(偏移: 0x0)
- `short hiddenValue`（short hidden值）(偏移: 0x2)
- `bool inited`（布尔值 已初始化）(偏移: 0x4)
- `short fakeValue`（short fake值）(偏移: 0x6)
- `bool fakeValueActive`（布尔值 假值激活的）(偏移: 0x8)

### 方法 (24)

- `void SetNewCryptoKey(short newKey)`
  （void 集合新的Crypto键（short newKey））
- `short EncryptDecrypt(short value)`
  （short EncryptDecrypt（short value））
- `short EncryptDecrypt(short value, short key)`
  （short EncryptDecrypt（short value, short key））
- `ObscuredShort FromEncrypted(short encrypted)`
  （模糊的Short FromEncrypted（short encrypted））
- `void ApplyNewCryptoKey()`
  （void 应用新加密密钥（））
- `void RandomizeCryptoKey()`
  （void 随机化加密密钥（））
- `short GetEncrypted()`
  （short 获取Encrypted（））
- `void SetEncrypted(short encrypted)`
  （void 集合Encrypted（short encrypted））
- `short GetDecrypted()`
  （short 获取Decrypted（））
- `short InternalDecrypt()`
  （short 内部的Decrypt（））
- `ObscuredShort op_Implicit(short value)`
  （模糊的Short op_Implicit（short value））
- `short op_Implicit(ObscuredShort value)`
  （short op_Implicit（模糊的Short value））
- `ObscuredShort op_Increment(ObscuredShort input)`
  （模糊的Short op_Increment（模糊的Short input））
- `ObscuredShort op_Decrement(ObscuredShort input)`
  （模糊的Short op_Decrement（模糊的Short input））
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
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(ObscuredShort obj)`
  （bool Equals（模糊的Short obj））
- `int CompareTo(ObscuredShort other)`
  （int CompareTo（模糊的Short other））
- `int CompareTo(short other)`
  （int CompareTo（short other））
- `int CompareTo(object obj)`
  （整数 比较到（对象 obj））

---

## ObscuredString（模糊的字符串）

**继承**: IComparable<ObscuredString>, IComparable<string>, IComparable（IComparable<模糊的String>, IComparable<string>, IComparable）

### 字段 (6)

- `string cryptoKey`（string crypto键）(偏移: 0x0)
- `string currentCryptoKey`（string currentCrypto键）(偏移: 0x8)
- `byte[] hiddenValue`（byte[] hidden值）(偏移: 0xC)
- `bool inited`（布尔值 已初始化）(偏移: 0x10)
- `string fakeValue`（string fake值）(偏移: 0x14)
- `bool fakeValueActive`（布尔值 假值激活的）(偏移: 0x18)

### 方法 (28)

- `void SetNewCryptoKey(string newKey)`
  （void 集合新的Crypto键（string newKey））
- `string EncryptDecrypt(string value)`
  （string EncryptDecrypt（string value））
- `string EncryptDecrypt(string value, string key)`
  （string EncryptDecrypt（string value, string key））
- `ObscuredString FromEncrypted(string encrypted)`
  （模糊的字符串 FromEncrypted（string encrypted））
- `void ApplyNewCryptoKey()`
  （void 应用新加密密钥（））
- `void RandomizeCryptoKey()`
  （void 随机化加密密钥（））
- `string GetEncrypted()`
  （string 获取Encrypted（））
- `void SetEncrypted(string encrypted)`
  （void 集合Encrypted（string encrypted））
- `string GetDecrypted()`
  （string 获取Decrypted（））
- `byte[] InternalEncrypt(string value)`
  （byte[] 内部的Encrypt（string value））
- `byte[] InternalEncrypt(string value, string key)`
  （byte[] 内部的Encrypt（string value, string key））
- `string InternalDecrypt()`
  （string 内部的Decrypt（））
- `int get_Length()`
  （整数 获取_长度（））
- `ObscuredString op_Implicit(string value)`
  （模糊的字符串 op_Implicit（string value））
- `string op_Implicit(ObscuredString value)`
  （string op_Implicit（模糊的字符串 value））
- `bool op_Equality(ObscuredString a, ObscuredString b)`
  （bool op_Equality（模糊的字符串 a, 模糊的字符串 b））
- `bool op_Inequality(ObscuredString a, ObscuredString b)`
  （bool op_Inequality（模糊的字符串 a, 模糊的字符串 b））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `string ToString()`
  （字符串 转字符串（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(ObscuredString value)`
  （bool Equals（模糊的字符串 value））
- `bool Equals(ObscuredString value, StringComparison comparisonType)`
  （bool Equals（模糊的字符串 value, 字符串Comparison comparisonType））
- `int CompareTo(ObscuredString other)`
  （int CompareTo（模糊的字符串 other））
- `int CompareTo(string other)`
  （int CompareTo（string other））
- `int CompareTo(object obj)`
  （整数 比较到（对象 obj））
- `byte[] GetBytes(string str)`
  （byte[] 获取Bytes（string str））
- `string GetString(byte[] bytes)`
  （string 获取字符串（byte[] bytes））
- `bool ArraysEquals(byte[] a1, byte[] a2)`
  （bool ArraysEquals（byte[] a1, byte[] a2））

---

## ObscuredTypesExamples（模糊的TypesExamples）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (16)

- `string regularString`（string regular字符串）(偏移: 0xC)
- `int regularInt`（int regular整数）(偏移: 0x10)
- `float regularFloat`（float regular浮点数）(偏移: 0x14)
- `Vector3 regularVector3`（三维向量 regular三维向量）(偏移: 0x18)
- `ObscuredString obscuredString`（模糊的字符串 obscured字符串）(偏移: 0x24)
- `ObscuredInt obscuredInt`（模糊整数 obscured整数）(偏移: 0x28)
- `ObscuredFloat obscuredFloat`（模糊的浮点数 obscured浮点数）(偏移: 0x3C)
- `ObscuredVector3 obscuredVector3`（模糊的三维向量 obscured三维向量）(偏移: 0x54)
- `ObscuredBool obscuredBool`（模糊的布尔值 obscured布尔值）(偏移: 0x78)
- `ObscuredLong obscuredLong`（模糊的Long obscuredLong）(偏移: 0x88)
- `ObscuredDouble obscuredDouble`（模糊的Double obscuredDouble）(偏移: 0xB0)
- `ObscuredVector2 obscuredVector2`（模糊的二维向量 obscured二维向量）(偏移: 0xE0)
- `ObscuredDecimal obscuredDecimal`（模糊的Decimal obscuredDecimal）(偏移: 0x100)
- `ObscuredVector2Int obscuredVector2Int`（模糊的二维向量整数 obscured二维向量整数）(偏移: 0x130)
- `ObscuredVector3Int obscuredVector3Int`（模糊的三维向量整数 obscured三维向量整数）(偏移: 0x14C)
- `StringBuilder logBuilder`（字符串构建器 log构建器）(偏移: 0x170)

### 方法 (5)

- `void Awake()`
  （void 唤醒（））
- `void Start()`
  （void 开始（））
- `void RandomizeObscuredVars()`
  （void Randomize模糊的Vars（））
- `void ObscuredStringExample()`
  （void 模糊的字符串Example（））
- `void ObscuredIntExample()`
  （void 模糊的整数Example（））

---

## ObscuredUInt（模糊的U整数）

**继承**: IFormattable, IEquatable<ObscuredUInt>, IComparable<ObscuredUInt>, IComparable<uint>, IComparable（IFormattable, IEquatable<模糊的UInt>, IComparable<模糊的UInt>, IComparable<uint>, IComparable）

### 字段 (6)

- `uint cryptoKey`（uint crypto键）(偏移: 0x0)
- `uint currentCryptoKey`（uint currentCrypto键）(偏移: 0x0)
- `uint hiddenValue`（uint hidden值）(偏移: 0x4)
- `bool inited`（布尔值 已初始化）(偏移: 0x8)
- `uint fakeValue`（uint fake值）(偏移: 0xC)
- `bool fakeValueActive`（布尔值 假值激活的）(偏移: 0x10)

### 方法 (27)

- `void SetNewCryptoKey(uint newKey)`
  （void 集合新的Crypto键（uint newKey））
- `uint Encrypt(uint value)`
  （uint Encrypt（uint value））
- `uint Decrypt(uint value)`
  （uint Decrypt（uint value））
- `uint Encrypt(uint value, uint key)`
  （uint Encrypt（uint value, uint key））
- `uint Decrypt(uint value, uint key)`
  （uint Decrypt（uint value, uint key））
- `ObscuredUInt FromEncrypted(uint encrypted)`
  （模糊的U整数 FromEncrypted（uint encrypted））
- `void ApplyNewCryptoKey()`
  （void 应用新加密密钥（））
- `void RandomizeCryptoKey()`
  （void 随机化加密密钥（））
- `uint GetEncrypted()`
  （uint 获取Encrypted（））
- `void SetEncrypted(uint encrypted)`
  （void 集合Encrypted（uint encrypted））
- `uint GetDecrypted()`
  （uint 获取Decrypted（））
- `uint InternalDecrypt()`
  （uint 内部的Decrypt（））
- `ObscuredUInt op_Implicit(uint value)`
  （模糊的U整数 op_Implicit（uint value））
- `uint op_Implicit(ObscuredUInt value)`
  （uint op_Implicit（模糊的U整数 value））
- `ObscuredInt op_Explicit(ObscuredUInt value)`
  （模糊整数 op_Explicit（模糊的U整数 value））
- `ObscuredUInt op_Increment(ObscuredUInt input)`
  （模糊的U整数 op_Increment（模糊的U整数 input））
- `ObscuredUInt op_Decrement(ObscuredUInt input)`
  （模糊的U整数 op_Decrement（模糊的U整数 input））
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
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(ObscuredUInt obj)`
  （bool Equals（模糊的U整数 obj））
- `int CompareTo(ObscuredUInt other)`
  （int CompareTo（模糊的U整数 other））
- `int CompareTo(uint other)`
  （int CompareTo（uint other））
- `int CompareTo(object obj)`
  （整数 比较到（对象 obj））

---

## ObscuredULong（模糊的ULong）

**继承**: IFormattable, IEquatable<ObscuredULong>, IComparable<ObscuredULong>, IComparable<ulong>, IComparable（IFormattable, IEquatable<模糊的ULong>, IComparable<模糊的ULong>, IComparable<ulong>, IComparable）

### 字段 (6)

- `ulong cryptoKey`（ulong crypto键）(偏移: 0x0)
- `ulong currentCryptoKey`（ulong currentCrypto键）(偏移: 0x0)
- `ulong hiddenValue`（ulong hidden值）(偏移: 0x8)
- `bool inited`（布尔值 已初始化）(偏移: 0x10)
- `ulong fakeValue`（ulong fake值）(偏移: 0x18)
- `bool fakeValueActive`（布尔值 假值激活的）(偏移: 0x20)

### 方法 (26)

- `void SetNewCryptoKey(ulong newKey)`
  （void 集合新的Crypto键（ulong newKey））
- `ulong Encrypt(ulong value)`
  （ulong Encrypt（ulong value））
- `ulong Decrypt(ulong value)`
  （ulong Decrypt（ulong value））
- `ulong Encrypt(ulong value, ulong key)`
  （ulong Encrypt（ulong value, ulong key））
- `ulong Decrypt(ulong value, ulong key)`
  （ulong Decrypt（ulong value, ulong key））
- `ObscuredULong FromEncrypted(ulong encrypted)`
  （模糊的ULong FromEncrypted（ulong encrypted））
- `void ApplyNewCryptoKey()`
  （void 应用新加密密钥（））
- `void RandomizeCryptoKey()`
  （void 随机化加密密钥（））
- `ulong GetEncrypted()`
  （ulong 获取Encrypted（））
- `void SetEncrypted(ulong encrypted)`
  （void 集合Encrypted（ulong encrypted））
- `ulong GetDecrypted()`
  （ulong 获取Decrypted（））
- `ulong InternalDecrypt()`
  （ulong 内部的Decrypt（））
- `ObscuredULong op_Implicit(ulong value)`
  （模糊的ULong op_Implicit（ulong value））
- `ulong op_Implicit(ObscuredULong value)`
  （ulong op_Implicit（模糊的ULong value））
- `ObscuredULong op_Increment(ObscuredULong input)`
  （模糊的ULong op_Increment（模糊的ULong input））
- `ObscuredULong op_Decrement(ObscuredULong input)`
  （模糊的ULong op_Decrement（模糊的ULong input））
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
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(ObscuredULong obj)`
  （bool Equals（模糊的ULong obj））
- `int CompareTo(ObscuredULong other)`
  （int CompareTo（模糊的ULong other））
- `int CompareTo(ulong other)`
  （int CompareTo（ulong other））
- `int CompareTo(object obj)`
  （整数 比较到（对象 obj））

---

## ObscuredUShort（模糊的UShort）

**继承**: IFormattable, IEquatable<ObscuredUShort>, IComparable<ObscuredUShort>, IComparable<ushort>, IComparable（IFormattable, IEquatable<模糊的UShort>, IComparable<模糊的UShort>, IComparable<ushort>, IComparable）

### 字段 (6)

- `ushort cryptoKey`（ushort crypto键）(偏移: 0x0)
- `ushort currentCryptoKey`（ushort currentCrypto键）(偏移: 0x0)
- `ushort hiddenValue`（ushort hidden值）(偏移: 0x2)
- `bool inited`（布尔值 已初始化）(偏移: 0x4)
- `ushort fakeValue`（ushort fake值）(偏移: 0x6)
- `bool fakeValueActive`（布尔值 假值激活的）(偏移: 0x8)

### 方法 (24)

- `void SetNewCryptoKey(ushort newKey)`
  （void 集合新的Crypto键（ushort newKey））
- `ushort EncryptDecrypt(ushort value)`
  （ushort EncryptDecrypt（ushort value））
- `ushort EncryptDecrypt(ushort value, ushort key)`
  （ushort EncryptDecrypt（ushort value, ushort key））
- `ObscuredUShort FromEncrypted(ushort encrypted)`
  （模糊的UShort FromEncrypted（ushort encrypted））
- `void ApplyNewCryptoKey()`
  （void 应用新加密密钥（））
- `void RandomizeCryptoKey()`
  （void 随机化加密密钥（））
- `ushort GetEncrypted()`
  （ushort 获取Encrypted（））
- `void SetEncrypted(ushort encrypted)`
  （void 集合Encrypted（ushort encrypted））
- `ushort GetDecrypted()`
  （ushort 获取Decrypted（））
- `ushort InternalDecrypt()`
  （ushort 内部的Decrypt（））
- `ObscuredUShort op_Implicit(ushort value)`
  （模糊的UShort op_Implicit（ushort value））
- `ushort op_Implicit(ObscuredUShort value)`
  （ushort op_Implicit（模糊的UShort value））
- `ObscuredUShort op_Increment(ObscuredUShort input)`
  （模糊的UShort op_Increment（模糊的UShort input））
- `ObscuredUShort op_Decrement(ObscuredUShort input)`
  （模糊的UShort op_Decrement（模糊的UShort input））
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
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(ObscuredUShort obj)`
  （bool Equals（模糊的UShort obj））
- `int CompareTo(ObscuredUShort other)`
  （int CompareTo（模糊的UShort other））
- `int CompareTo(ushort other)`
  （int CompareTo（ushort other））
- `int CompareTo(object obj)`
  （整数 比较到（对象 obj））

---

## ObscuredVector2（模糊的二维向量）

### 字段 (7)

- `int cryptoKey`（整数 加密密钥）(偏移: 0x0)
- `Vector2 zero`（二维向量 zero）(偏移: 0x4)
- `int currentCryptoKey`（整数 当前加密密钥）(偏移: 0x0)
- `ObscuredVector2.RawEncryptedVector2 hiddenValue`（模糊的Vector2.RawEncrypted二维向量 hidden值）(偏移: 0x4)
- `bool inited`（布尔值 已初始化）(偏移: 0xC)
- `Vector2 fakeValue`（二维向量 fake值）(偏移: 0x10)
- `bool fakeValueActive`（布尔值 假值激活的）(偏移: 0x18)

### 方法 (28)

- `float get_x()`
  （float get_x（））
- `void set_x(float value)`
  （void set_x（float value））
- `float get_y()`
  （float get_y（））
- `void set_y(float value)`
  （void set_y（float value））
- `float get_Item(int index)`
  （浮点数 获取_项（整数 index））
- `void set_Item(int index, float value)`
  （void 设置_项（整数 index, 浮点数 value））
- `void SetNewCryptoKey(int newKey)`
  （void 设置新加密密钥（整数 newKey））
- `ObscuredVector2.RawEncryptedVector2 Encrypt(Vector2 value)`
  （模糊的Vector2.RawEncrypted二维向量 Encrypt（二维向量 value））
- `ObscuredVector2.RawEncryptedVector2 Encrypt(Vector2 value, int key)`
  （模糊的Vector2.RawEncrypted二维向量 Encrypt（二维向量 value, int key））
- `ObscuredVector2.RawEncryptedVector2 Encrypt(float x, float y, int key)`
  （模糊的Vector2.RawEncrypted二维向量 Encrypt（float x, float y, int key））
- `Vector2 Decrypt(ObscuredVector2.RawEncryptedVector2 value)`
  （二维向量 Decrypt（模糊的Vector2.RawEncrypted二维向量 value））
- `Vector2 Decrypt(ObscuredVector2.RawEncryptedVector2 value, int key)`
  （二维向量 Decrypt（模糊的Vector2.RawEncrypted二维向量 value, int key））
- `ObscuredVector2 FromEncrypted(ObscuredVector2.RawEncryptedVector2 encrypted)`
  （模糊的二维向量 FromEncrypted（模糊的Vector2.RawEncrypted二维向量 encrypted））
- `void ApplyNewCryptoKey()`
  （void 应用新加密密钥（））
- `void RandomizeCryptoKey()`
  （void 随机化加密密钥（））
- `ObscuredVector2.RawEncryptedVector2 GetEncrypted()`
  （模糊的Vector2.RawEncrypted二维向量 获取Encrypted（））
- `void SetEncrypted(ObscuredVector2.RawEncryptedVector2 encrypted)`
  （void 集合Encrypted（模糊的Vector2.RawEncrypted二维向量 encrypted））
- `Vector2 GetDecrypted()`
  （二维向量 获取Decrypted（））
- `Vector2 InternalDecrypt()`
  （二维向量 内部的Decrypt（））
- `bool CompareVectorsWithTolerance(Vector2 vector1, Vector2 vector2)`
  （bool CompareVectorsWithTolerance（二维向量 vector1, 二维向量 vector2））
- `float InternalDecryptField(int encrypted)`
  （float 内部的DecryptField（int encrypted））
- `int InternalEncryptField(float encrypted)`
  （int 内部的EncryptField（float encrypted））
- `ObscuredVector2 op_Implicit(Vector2 value)`
  （模糊的二维向量 op_Implicit（二维向量 value））
- `Vector2 op_Implicit(ObscuredVector2 value)`
  （二维向量 op_Implicit（模糊的二维向量 value））
- `Vector3 op_Implicit(ObscuredVector2 value)`
  （三维向量 op_Implicit（模糊的二维向量 value））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `string ToString()`
  （字符串 转字符串（））
- `string ToString(string format)`
  （字符串 转字符串（字符串 格式））

---

## ObscuredVector2.RawEncryptedVector2（模糊的Vector2.RawEncrypted二维向量）

### 字段 (2)

- `int x`（整数 x）(偏移: 0x0)
- `int y`（整数 y）(偏移: 0x4)

---

## ObscuredVector2Int（模糊的二维向量整数）

### 字段 (7)

- `int cryptoKey`（整数 加密密钥）(偏移: 0x0)
- `Vector2Int zero`（二维向量整数 zero）(偏移: 0x4)
- `int currentCryptoKey`（整数 当前加密密钥）(偏移: 0x0)
- `ObscuredVector2Int.RawEncryptedVector2Int hiddenValue`（模糊的二维向量Int.RawEncrypted二维向量整数 hidden值）(偏移: 0x4)
- `bool inited`（布尔值 已初始化）(偏移: 0xC)
- `Vector2Int fakeValue`（二维向量整数 fake值）(偏移: 0x10)
- `bool fakeValueActive`（布尔值 假值激活的）(偏移: 0x18)

### 方法 (26)

- `int get_x()`
  （整数 获取_x（））
- `void set_x(int value)`
  （void 设置_x（整数 value））
- `int get_y()`
  （整数 获取_y（））
- `void set_y(int value)`
  （void 设置_y（整数 value））
- `int get_Item(int index)`
  （int get_项目（int index））
- `void set_Item(int index, int value)`
  （void set_项目（int index, int value））
- `void SetNewCryptoKey(int newKey)`
  （void 设置新加密密钥（整数 newKey））
- `ObscuredVector2Int.RawEncryptedVector2Int Encrypt(Vector2Int value)`
  （模糊的二维向量Int.RawEncrypted二维向量整数 Encrypt（二维向量整数 value））
- `ObscuredVector2Int.RawEncryptedVector2Int Encrypt(Vector2Int value, int key)`
  （模糊的二维向量Int.RawEncrypted二维向量整数 Encrypt（二维向量整数 value, int key））
- `ObscuredVector2Int.RawEncryptedVector2Int Encrypt(int x, int y, int key)`
  （模糊的二维向量Int.RawEncrypted二维向量整数 Encrypt（int x, int y, int key））
- `Vector2Int Decrypt(ObscuredVector2Int.RawEncryptedVector2Int value)`
  （二维向量整数 Decrypt（模糊的二维向量Int.RawEncrypted二维向量整数 value））
- `Vector2Int Decrypt(ObscuredVector2Int.RawEncryptedVector2Int value, int key)`
  （二维向量整数 Decrypt（模糊的二维向量Int.RawEncrypted二维向量整数 value, int key））
- `ObscuredVector2Int FromEncrypted(ObscuredVector2Int.RawEncryptedVector2Int encrypted)`
  （模糊的二维向量整数 FromEncrypted（模糊的二维向量Int.RawEncrypted二维向量整数 encrypted））
- `void ApplyNewCryptoKey()`
  （void 应用新加密密钥（））
- `void RandomizeCryptoKey()`
  （void 随机化加密密钥（））
- `ObscuredVector2Int.RawEncryptedVector2Int GetEncrypted()`
  （模糊的二维向量Int.RawEncrypted二维向量整数 获取Encrypted（））
- `void SetEncrypted(ObscuredVector2Int.RawEncryptedVector2Int encrypted)`
  （void 集合Encrypted（模糊的二维向量Int.RawEncrypted二维向量整数 encrypted））
- `Vector2Int GetDecrypted()`
  （二维向量整数 获取Decrypted（））
- `Vector2Int InternalDecrypt()`
  （二维向量整数 内部的Decrypt（））
- `int InternalDecryptField(int encrypted)`
  （int 内部的DecryptField（int encrypted））
- `int InternalEncryptField(int encrypted)`
  （int 内部的EncryptField（int encrypted））
- `ObscuredVector2Int op_Implicit(Vector2Int value)`
  （模糊的二维向量整数 op_Implicit（二维向量整数 value））
- `Vector2Int op_Implicit(ObscuredVector2Int value)`
  （二维向量整数 op_Implicit（模糊的二维向量整数 value））
- `Vector2 op_Implicit(ObscuredVector2Int value)`
  （二维向量 op_Implicit（模糊的二维向量整数 value））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `string ToString()`
  （字符串 转字符串（））

---

## ObscuredVector2Int.RawEncryptedVector2Int（模糊的二维向量Int.RawEncrypted二维向量整数）

### 字段 (2)

- `int x`（整数 x）(偏移: 0x0)
- `int y`（整数 y）(偏移: 0x4)

---

## ObscuredVector3（模糊的三维向量）

### 字段 (7)

- `int cryptoKey`（整数 加密密钥）(偏移: 0x0)
- `Vector3 zero`（三维向量 zero）(偏移: 0x4)
- `int currentCryptoKey`（整数 当前加密密钥）(偏移: 0x0)
- `ObscuredVector3.RawEncryptedVector3 hiddenValue`（模糊的Vector3.RawEncrypted三维向量 hidden值）(偏移: 0x4)
- `bool inited`（布尔值 已初始化）(偏移: 0x10)
- `Vector3 fakeValue`（三维向量 fake值）(偏移: 0x14)
- `bool fakeValueActive`（布尔值 假值激活的）(偏移: 0x20)

### 方法 (46)

- `float get_x()`
  （float get_x（））
- `void set_x(float value)`
  （void set_x（float value））
- `float get_y()`
  （float get_y（））
- `void set_y(float value)`
  （void set_y（float value））
- `float get_z()`
  （float get_z（））
- `void set_z(float value)`
  （void set_z（float value））
- `float get_Item(int index)`
  （浮点数 获取_项（整数 index））
- `void set_Item(int index, float value)`
  （void 设置_项（整数 index, 浮点数 value））
- `void SetNewCryptoKey(int newKey)`
  （void 设置新加密密钥（整数 newKey））
- `ObscuredVector3.RawEncryptedVector3 Encrypt(Vector3 value)`
  （模糊的Vector3.RawEncrypted三维向量 Encrypt（三维向量 value））
- `ObscuredVector3.RawEncryptedVector3 Encrypt(Vector3 value, int key)`
  （模糊的Vector3.RawEncrypted三维向量 Encrypt（三维向量 value, int key））
- `ObscuredVector3.RawEncryptedVector3 Encrypt(float x, float y, float z, int key)`
  （模糊的Vector3.RawEncrypted三维向量 Encrypt（float x, float y, float z, int key））
- `Vector3 Decrypt(ObscuredVector3.RawEncryptedVector3 value)`
  （三维向量 Decrypt（模糊的Vector3.RawEncrypted三维向量 value））
- `Vector3 Decrypt(ObscuredVector3.RawEncryptedVector3 value, int key)`
  （三维向量 Decrypt（模糊的Vector3.RawEncrypted三维向量 value, int key））
- `ObscuredVector3 FromEncrypted(ObscuredVector3.RawEncryptedVector3 encrypted)`
  （模糊的三维向量 FromEncrypted（模糊的Vector3.RawEncrypted三维向量 encrypted））
- `void ApplyNewCryptoKey()`
  （void 应用新加密密钥（））
- `void RandomizeCryptoKey()`
  （void 随机化加密密钥（））
- `ObscuredVector3.RawEncryptedVector3 GetEncrypted()`
  （模糊的Vector3.RawEncrypted三维向量 获取Encrypted（））
- `void SetEncrypted(ObscuredVector3.RawEncryptedVector3 encrypted)`
  （void 集合Encrypted（模糊的Vector3.RawEncrypted三维向量 encrypted））
- `Vector3 GetDecrypted()`
  （三维向量 获取Decrypted（））
- `Vector3 InternalDecrypt()`
  （三维向量 内部的Decrypt（））
- `bool CompareVectorsWithTolerance(Vector3 vector1, Vector3 vector2)`
  （bool CompareVectorsWithTolerance（三维向量 vector1, 三维向量 vector2））
- `float InternalDecryptField(int encrypted)`
  （float 内部的DecryptField（int encrypted））
- `int InternalEncryptField(float encrypted)`
  （int 内部的EncryptField（float encrypted））
- `ObscuredVector3 op_Implicit(Vector3 value)`
  （模糊的三维向量 op_Implicit（三维向量 value））
- `Vector3 op_Implicit(ObscuredVector3 value)`
  （三维向量 op_Implicit（模糊的三维向量 value））
- `ObscuredVector3 op_Addition(ObscuredVector3 a, ObscuredVector3 b)`
  （模糊的三维向量 op_Addition（模糊的三维向量 a, 模糊的三维向量 b））
- `ObscuredVector3 op_Addition(Vector3 a, ObscuredVector3 b)`
  （模糊的三维向量 op_Addition（三维向量 a, 模糊的三维向量 b））
- `ObscuredVector3 op_Addition(ObscuredVector3 a, Vector3 b)`
  （模糊的三维向量 op_Addition（模糊的三维向量 a, 三维向量 b））
- `ObscuredVector3 op_Subtraction(ObscuredVector3 a, ObscuredVector3 b)`
  （模糊的三维向量 op_Subtraction（模糊的三维向量 a, 模糊的三维向量 b））
- `ObscuredVector3 op_Subtraction(Vector3 a, ObscuredVector3 b)`
  （模糊的三维向量 op_Subtraction（三维向量 a, 模糊的三维向量 b））
- `ObscuredVector3 op_Subtraction(ObscuredVector3 a, Vector3 b)`
  （模糊的三维向量 op_Subtraction（模糊的三维向量 a, 三维向量 b））
- `ObscuredVector3 op_UnaryNegation(ObscuredVector3 a)`
  （模糊的三维向量 op_UnaryNegation（模糊的三维向量 a））
- `ObscuredVector3 op_Multiply(ObscuredVector3 a, float d)`
  （模糊的三维向量 op_Multiply（模糊的三维向量 a, float d））
- `ObscuredVector3 op_Multiply(float d, ObscuredVector3 a)`
  （模糊的三维向量 op_Multiply（float d, 模糊的三维向量 a））
- `ObscuredVector3 op_Division(ObscuredVector3 a, float d)`
  （模糊的三维向量 op_Division（模糊的三维向量 a, float d））
- `bool op_Equality(ObscuredVector3 lhs, ObscuredVector3 rhs)`
  （bool op_Equality（模糊的三维向量 lhs, 模糊的三维向量 rhs））
- `bool op_Equality(Vector3 lhs, ObscuredVector3 rhs)`
  （bool op_Equality（三维向量 lhs, 模糊的三维向量 rhs））
- `bool op_Equality(ObscuredVector3 lhs, Vector3 rhs)`
  （bool op_Equality（模糊的三维向量 lhs, 三维向量 rhs））
- `bool op_Inequality(ObscuredVector3 lhs, ObscuredVector3 rhs)`
  （bool op_Inequality（模糊的三维向量 lhs, 模糊的三维向量 rhs））
- `bool op_Inequality(Vector3 lhs, ObscuredVector3 rhs)`
  （bool op_Inequality（三维向量 lhs, 模糊的三维向量 rhs））
- `bool op_Inequality(ObscuredVector3 lhs, Vector3 rhs)`
  （bool op_Inequality（模糊的三维向量 lhs, 三维向量 rhs））
- `bool Equals(object other)`
  （布尔值 等于（对象 other））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `string ToString()`
  （字符串 转字符串（））
- `string ToString(string format)`
  （字符串 转字符串（字符串 格式））

---

## ObscuredVector3.RawEncryptedVector3（模糊的Vector3.RawEncrypted三维向量）

### 字段 (3)

- `int x`（整数 x）(偏移: 0x0)
- `int y`（整数 y）(偏移: 0x4)
- `int z`（整数 z）(偏移: 0x8)

---

## ObscuredVector3Int（模糊的三维向量整数）

### 字段 (7)

- `int cryptoKey`（整数 加密密钥）(偏移: 0x0)
- `Vector3Int zero`（三维向量整数 zero）(偏移: 0x4)
- `int currentCryptoKey`（整数 当前加密密钥）(偏移: 0x0)
- `ObscuredVector3Int.RawEncryptedVector3Int hiddenValue`（模糊的三维向量Int.RawEncrypted三维向量整数 hidden值）(偏移: 0x4)
- `bool inited`（布尔值 已初始化）(偏移: 0x10)
- `Vector3Int fakeValue`（三维向量整数 fake值）(偏移: 0x14)
- `bool fakeValueActive`（布尔值 假值激活的）(偏移: 0x20)

### 方法 (43)

- `int get_x()`
  （整数 获取_x（））
- `void set_x(int value)`
  （void 设置_x（整数 value））
- `int get_y()`
  （整数 获取_y（））
- `void set_y(int value)`
  （void 设置_y（整数 value））
- `int get_z()`
  （int get_z（））
- `void set_z(int value)`
  （void set_z（int value））
- `int get_Item(int index)`
  （int get_项目（int index））
- `void set_Item(int index, int value)`
  （void set_项目（int index, int value））
- `void SetNewCryptoKey(int newKey)`
  （void 设置新加密密钥（整数 newKey））
- `ObscuredVector3Int.RawEncryptedVector3Int Encrypt(Vector3Int value)`
  （模糊的三维向量Int.RawEncrypted三维向量整数 Encrypt（三维向量整数 value））
- `ObscuredVector3Int.RawEncryptedVector3Int Encrypt(Vector3Int value, int key)`
  （模糊的三维向量Int.RawEncrypted三维向量整数 Encrypt（三维向量整数 value, int key））
- `ObscuredVector3Int.RawEncryptedVector3Int Encrypt(int x, int y, int z, int key)`
  （模糊的三维向量Int.RawEncrypted三维向量整数 Encrypt（int x, int y, int z, int key））
- `Vector3Int Decrypt(ObscuredVector3Int.RawEncryptedVector3Int value)`
  （三维向量整数 Decrypt（模糊的三维向量Int.RawEncrypted三维向量整数 value））
- `Vector3Int Decrypt(ObscuredVector3Int.RawEncryptedVector3Int value, int key)`
  （三维向量整数 Decrypt（模糊的三维向量Int.RawEncrypted三维向量整数 value, int key））
- `ObscuredVector3Int FromEncrypted(ObscuredVector3Int.RawEncryptedVector3Int encrypted)`
  （模糊的三维向量整数 FromEncrypted（模糊的三维向量Int.RawEncrypted三维向量整数 encrypted））
- `void ApplyNewCryptoKey()`
  （void 应用新加密密钥（））
- `void RandomizeCryptoKey()`
  （void 随机化加密密钥（））
- `ObscuredVector3Int.RawEncryptedVector3Int GetEncrypted()`
  （模糊的三维向量Int.RawEncrypted三维向量整数 获取Encrypted（））
- `void SetEncrypted(ObscuredVector3Int.RawEncryptedVector3Int encrypted)`
  （void 集合Encrypted（模糊的三维向量Int.RawEncrypted三维向量整数 encrypted））
- `Vector3Int GetDecrypted()`
  （三维向量整数 获取Decrypted（））
- `Vector3Int InternalDecrypt()`
  （三维向量整数 内部的Decrypt（））
- `int InternalDecryptField(int encrypted)`
  （int 内部的DecryptField（int encrypted））
- `int InternalEncryptField(int encrypted)`
  （int 内部的EncryptField（int encrypted））
- `ObscuredVector3Int op_Implicit(Vector3Int value)`
  （模糊的三维向量整数 op_Implicit（三维向量整数 value））
- `Vector3Int op_Implicit(ObscuredVector3Int value)`
  （三维向量整数 op_Implicit（模糊的三维向量整数 value））
- `Vector3 op_Implicit(ObscuredVector3Int value)`
  （三维向量 op_Implicit（模糊的三维向量整数 value））
- `ObscuredVector3Int op_Addition(ObscuredVector3Int a, ObscuredVector3Int b)`
  （模糊的三维向量整数 op_Addition（模糊的三维向量整数 a, 模糊的三维向量整数 b））
- `ObscuredVector3Int op_Addition(Vector3Int a, ObscuredVector3Int b)`
  （模糊的三维向量整数 op_Addition（三维向量整数 a, 模糊的三维向量整数 b））
- `ObscuredVector3Int op_Addition(ObscuredVector3Int a, Vector3Int b)`
  （模糊的三维向量整数 op_Addition（模糊的三维向量整数 a, 三维向量整数 b））
- `ObscuredVector3Int op_Subtraction(ObscuredVector3Int a, ObscuredVector3Int b)`
  （模糊的三维向量整数 op_Subtraction（模糊的三维向量整数 a, 模糊的三维向量整数 b））
- `ObscuredVector3Int op_Subtraction(Vector3Int a, ObscuredVector3Int b)`
  （模糊的三维向量整数 op_Subtraction（三维向量整数 a, 模糊的三维向量整数 b））
- `ObscuredVector3Int op_Subtraction(ObscuredVector3Int a, Vector3Int b)`
  （模糊的三维向量整数 op_Subtraction（模糊的三维向量整数 a, 三维向量整数 b））
- `ObscuredVector3Int op_Multiply(ObscuredVector3Int a, int d)`
  （模糊的三维向量整数 op_Multiply（模糊的三维向量整数 a, int d））
- `bool op_Equality(ObscuredVector3Int lhs, ObscuredVector3Int rhs)`
  （bool op_Equality（模糊的三维向量整数 lhs, 模糊的三维向量整数 rhs））
- `bool op_Equality(Vector3Int lhs, ObscuredVector3Int rhs)`
  （bool op_Equality（三维向量整数 lhs, 模糊的三维向量整数 rhs））
- `bool op_Equality(ObscuredVector3Int lhs, Vector3Int rhs)`
  （bool op_Equality（模糊的三维向量整数 lhs, 三维向量整数 rhs））
- `bool op_Inequality(ObscuredVector3Int lhs, ObscuredVector3Int rhs)`
  （bool op_Inequality（模糊的三维向量整数 lhs, 模糊的三维向量整数 rhs））
- `bool op_Inequality(Vector3Int lhs, ObscuredVector3Int rhs)`
  （bool op_Inequality（三维向量整数 lhs, 模糊的三维向量整数 rhs））
- `bool op_Inequality(ObscuredVector3Int lhs, Vector3Int rhs)`
  （bool op_Inequality（模糊的三维向量整数 lhs, 三维向量整数 rhs））
- `bool Equals(object other)`
  （布尔值 等于（对象 other））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `string ToString()`
  （字符串 转字符串（））
- `string ToString(string format)`
  （字符串 转字符串（字符串 格式））

---

## ObscuredVector3Int.RawEncryptedVector3Int（模糊的三维向量Int.RawEncrypted三维向量整数）

### 字段 (3)

- `int x`（整数 x）(偏移: 0x0)
- `int y`（整数 y）(偏移: 0x4)
- `int z`（整数 z）(偏移: 0x8)

---

## ObsoleteAttribute（ObsoleteAttribute）

**继承**: Attribute（属性）

### 字段 (2)

- `string _message`（string _message）(偏移: 0x8)
- `bool _error`（bool _error）(偏移: 0xC)

### 方法 (1)

- `string get_Message()`
  （字符串 获取_消息（））

---

## ObstacleVertex（ObstacleVertex）

### 字段 (7)

- `bool ignore`（bool ignore）(偏移: 0x8)
- `Vector3 position`（三维向量 位置）(偏移: 0xC)
- `Vector2 dir`（二维向量 dir）(偏移: 0x18)
- `float height`（浮点数 高度）(偏移: 0x20)
- `RVOLayer layer`（RVO层 layer）(偏移: 0x24)
- `ObstacleVertex next`（ObstacleVertex next）(偏移: 0x28)
- `ObstacleVertex prev`（ObstacleVertex prev）(偏移: 0x2C)

---

## OffsetModifier（偏移修改器）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (3)

- `float weight`（浮点数 权重）(偏移: 0xC)
- `FullBodyBipedIK ik`（全身双足IK ik）(偏移: 0x10)
- `float lastTime`（浮点数 上次时间）(偏移: 0x14)

### 方法 (6)

- `float get_deltaTime()`
  （浮点数 获取_增量时间（））
- `void Start()`
  （void 开始（））
- `IEnumerator Initiate()`
  （IEnumerator Initiate（））
- `void ModifyOffset()`
  （void ModifyOffset（））
- `void ApplyLimits(OffsetModifier.OffsetLimits[] limits)`
  （void 应用Limits（OffsetModifier.OffsetLimits[] limits））
- `void OnDestroy()`
  （void 销毁时（））

---

## OffsetModifier.OffsetLimits（OffsetModifier.OffsetLimits）

### 字段 (11)

- `FullBodyBipedEffector effector`（全身双足效应器 effector）(偏移: 0x8)
- `float spring`（float spring）(偏移: 0xC)
- `bool x`（bool x）(偏移: 0x10)
- `bool y`（bool y）(偏移: 0x11)
- `bool z`（bool z）(偏移: 0x12)
- `float minX`（float minX）(偏移: 0x14)
- `float maxX`（float maxX）(偏移: 0x18)
- `float minY`（float minY）(偏移: 0x1C)
- `float maxY`（float maxY）(偏移: 0x20)
- `float minZ`（float minZ）(偏移: 0x24)
- `float maxZ`（float maxZ）(偏移: 0x28)

### 方法 (3)

- `void Apply(IKEffector e, Quaternion rootRotation)`
  （void 应用（IKEffector e, Quaternion rootRotation））
- `float SpringAxis(float value, float min, float max)`
  （float Spring轴（float value, float min, float max））
- `float Spring(float value, float limit, bool negative)`
  （float Spring（float value, float limit, bool negative））

---

## OffsetModifierVRIK（Offset修改器VRIK）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (3)

- `float weight`（浮点数 权重）(偏移: 0xC)
- `VRIK ik`（VRIK ik）(偏移: 0x10)
- `float lastTime`（浮点数 上次时间）(偏移: 0x14)

### 方法 (5)

- `float get_deltaTime()`
  （浮点数 获取_增量时间（））
- `void Start()`
  （void 开始（））
- `IEnumerator Initiate()`
  （IEnumerator Initiate（））
- `void ModifyOffset()`
  （void ModifyOffset（））
- `void OnDestroy()`
  （void 销毁时（））

---

## OffsetPose（OffsetPose）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (1)

- `OffsetPose.EffectorLink[] effectorLinks`（OffsetPose.EffectorLink[] effectorLinks）(偏移: 0xC)

### 方法 (2)

- `void Apply(IKSolverFullBodyBiped solver, float weight)`
  （void 应用（IKSolver满身体Biped solver, float weight））
- `void Apply(IKSolverFullBodyBiped solver, float weight, Quaternion rotation)`
  （void 应用（IKSolver满身体Biped solver, float weight, Quaternion rotation））

---

## OffsetPose.EffectorLink（OffsetPose.EffectorLink）

### 字段 (4)

- `FullBodyBipedEffector effector`（全身双足效应器 effector）(偏移: 0x8)
- `Vector3 offset`（三维向量 偏移）(偏移: 0xC)
- `Vector3 pin`（三维向量 pin）(偏移: 0x18)
- `Vector3 pinWeight`（三维向量 pinWeight）(偏移: 0x24)

### 方法 (1)

- `void Apply(IKSolverFullBodyBiped solver, float weight, Quaternion rotation)`
  （void 应用（IKSolver满身体Biped solver, float weight, Quaternion rotation））

---

## OffsetStream（Offset流）

**继承**: Stream, IDisposable（流, IDisposable）

### 字段 (2)

- `long _originalPosition`（long _originalPosition）(偏移: 0x18)
- `Stream _innerStream`（流 _内部流）(偏移: 0x20)

### 方法 (12)

- `int Read(byte[] buffer, int offset, int count)`
  （整数 读取（字节[] buffer, 整数 offset, 整数 count））
- `void Write(byte[] buffer, int offset, int count)`
  （void 写入（字节[] buffer, 整数 offset, 整数 count））
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
- `long Seek(long offset, SeekOrigin origin)`
  （长整数 查找（长整数 offset, 查找起点 origin））
- `void SetLength(long value)`
  （void 设置_长度（长整数 value））
- `void Close()`
  （void 关闭（））

---

## Oid（Oid）

### 字段 (3)

- `string m_value`（string m_value）(偏移: 0x8)
- `string m_friendlyName`（string m_friendly名称）(偏移: 0xC)
- `OidGroup m_group`（Oid组 m_group）(偏移: 0x10)

### 方法 (2)

- `string get_Value()`
  （字符串 获取_值（））
- `void set_Value(string value)`
  （void set_值（string value））

---

## OidCollection（OidCollection）

**继承**: ICollection, IEnumerable（ICollection, IEnumerable）

### 字段 (1)

- `ArrayList m_list`（数组列表 m_list）(偏移: 0x8)

### 方法 (4)

- `int Add(Oid oid)`
  （int 添加（Oid oid））
- `Oid get_Item(int index)`
  （Oid get_项目（int index））
- `int get_Count()`
  （整数 获取_数量（））
- `object get_SyncRoot()`
  （对象 获取_同步根（））

---

## OidEnumerator（OidEnumerator）

**继承**: IEnumerator（IEnumerator枚举器）

### 字段 (2)

- `OidCollection m_oids`（OidCollection m_oids）(偏移: 0x8)
- `int m_current`（int m_current）(偏移: 0xC)

### 方法 (2)

- `bool MoveNext()`
  （布尔值 移动下一个（））
- `void Reset()`
  （void 重置（））

---

## OidGroup（Oid组）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## OidGroup（Oid组）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## OnDemandRendering（OnDemandRendering）

### 字段 (1)

- `int m_RenderFrameInterval`（int m_RenderFrame间隔）(偏移: 0x0)

### 方法 (2)

- `int get_renderFrameInterval()`
  （int get_renderFrame间隔（））
- `void GetRenderFrameInterval(out int frameInterval)`
  （void 获取RenderFrame间隔（out int frameInterval））

---

## OnGraphDelegate（OnGraph委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(NavGraph graph)`
  （void Invoke（NavGraph graph））
- `IAsyncResult BeginInvoke(NavGraph graph, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（NavGraph graph, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## OnPathDelegate（On路径委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(Path p)`
  （void Invoke（路径 p））
- `IAsyncResult BeginInvoke(Path p, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（路径 p, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## OnScanDelegate（OnScan委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(AstarPath script)`
  （void Invoke（Astar路径 script））
- `IAsyncResult BeginInvoke(AstarPath script, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Astar路径 script, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## OnScanStatus（OnScanStatus）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(Progress progress)`
  （void Invoke（Progress progress））
- `IAsyncResult BeginInvoke(Progress progress, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Progress progress, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## OneShineRenderFeature（OneShineRenderFeature）

**继承**: ScriptableRendererFeature（可脚本化渲染器特性）

### 字段 (3)

- `Shader shader`（着色器 shader）(偏移: 0x10)
- `RenderPassEvent passEvent`（RenderPass事件 pass事件）(偏移: 0x14)
- `GhostBladeOneShinePass oneShinePass`（幽灵刀锋OneShinePass oneShinePass）(偏移: 0x18)

### 方法 (2)

- `void Create()`
  （void 创建（））
- `void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)`
  （void 添加渲染通道（可脚本化渲染器 renderer, 引用 渲染数据 renderingData））

---

## OpaqueSortMode（不透明的Sort模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## OpenDelegate（打开委托）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `Stream Invoke(string entryName)`
  （流 Invoke（string entryName））
- `IAsyncResult BeginInvoke(string entryName, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（string entryName, 异步回调 callback, object object））
- `Stream EndInvoke(IAsyncResult result)`
  （流 结束Invoke（I异步Result result））

---

## OpenGLESVersion（打开GLESVersion）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## OperatingSystem（Operating系统）

**继承**: ICloneable, ISerializable（ICloneable, ISerializable）

### 字段 (3)

- `PlatformID _platform`（PlatformID _platform）(偏移: 0x8)
- `Version _version`（Version _version）(偏移: 0xC)
- `string _servicePack`（string _servicePack）(偏移: 0x10)

### 方法 (6)

- `PlatformID get_Platform()`
  （PlatformID get_Platform（））
- `Version get_Version()`
  （Version get_Version（））
- `string get_ServicePack()`
  （string get_服务Pack（））
- `object Clone()`
  （对象 克隆（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））
- `string ToString()`
  （字符串 转字符串（））

---

## OperatingSystemFamily（Operating系统Family）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## OperationCanceledException（OperationCanceledException）

**继承**: SystemException（系统异常）

### 字段 (1)

- `CancellationToken _cancellationToken`（Cancellation令牌 _cancellation令牌）(偏移: 0x44)

### 方法 (2)

- `CancellationToken get_CancellationToken()`
  （Cancellation令牌 get_Cancellation令牌（））
- `void set_CancellationToken(CancellationToken value)`
  （void set_Cancellation令牌（Cancellation令牌 value））

---

## OperationType（Operation类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## OptionalFieldAttribute（OptionalFieldAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `int versionAdded`（int versionAdded）(偏移: 0x8)

### 方法 (1)

- `void set_VersionAdded(int value)`
  （void set_VersionAdded（int value））

---

## OrderedDictionary（Ordered字典）

**继承**: IDictionary, ICollection, IEnumerable, ISerializable, IDeserializationCallback（I字典, ICollection, IEnumerable, ISerializable, IDeserialization回调）

### 字段 (7)

- `ArrayList _objectsArray`（数组列表 _objects数组）(偏移: 0x8)
- `Hashtable _objectsTable`（Hashtable _objectsTable）(偏移: 0xC)
- `int _initialCapacity`（int _initialCapacity）(偏移: 0x10)
- `IEqualityComparer _comparer`（IEqualityComparer _comparer）(偏移: 0x14)
- `bool _readOnly`（bool _readOnly）(偏移: 0x18)
- `object _syncRoot`（对象 _同步根）(偏移: 0x1C)
- `SerializationInfo _siInfo`（Serialization信息 _si信息）(偏移: 0x20)

### 方法 (14)

- `int get_Count()`
  （整数 获取_数量（））
- `ArrayList get_objectsArray()`
  （数组列表 get_objects数组（））
- `Hashtable get_objectsTable()`
  （Hashtable get_objectsTable（））
- `object get_Item(object key)`
  （对象 获取_项（对象 key））
- `void set_Item(object key, object value)`
  （void 设置_项（对象 key, 对象 value））
- `ICollection get_Values()`
  （ICollection get_Values（））
- `void Add(object key, object value)`
  （void 添加（对象 key, 对象 value））
- `bool Contains(object key)`
  （布尔值 包含（对象 key））
- `void CopyTo(Array array, int index)`
  （void 复制到（数组 array, 整数 index））
- `int IndexOfKey(object key)`
  （int 索引Of键（object key））
- `void OnDeserialization(object sender)`
  （void 反序列化时（对象 sender））
- `void Remove(object key)`
  （void 移除（对象 key））
- `IDictionaryEnumerator GetEnumerator()`
  （I字典枚举器 获取枚举器（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））

---

## OrderedDictionary.OrderedDictionaryEnumerator（OrderedDictionary.Ordered字典Enumerator）

**继承**: IDictionaryEnumerator, IEnumerator（I字典枚举器, IEnumerator）

### 字段 (2)

- `int _objectReturnType`（int _objectReturn类型）(偏移: 0x8)
- `IEnumerator arrayEnumerator`（IEnumerator arrayEnumerator）(偏移: 0xC)

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

## OrderedDictionary.OrderedDictionaryKeyValueCollection（OrderedDictionary.Ordered字典键值Collection）

**继承**: ICollection, IEnumerable（ICollection, IEnumerable）

### 字段 (2)

- `ArrayList _objects`（数组列表 _objects）(偏移: 0x8)
- `bool isKeys`（bool isKeys）(偏移: 0xC)

---

## OrdinalComparer（OrdinalComparer）

**继承**: StringComparer（字符串Comparer）

### 字段 (1)

- `bool _ignoreCase`（bool _ignoreCase）(偏移: 0x8)

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

## OrientType（Orient类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Orientation（Orientation）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## OrientationMode（Orientation模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## OutPt（OutPt）

### 字段 (4)

- `int Idx`（int Idx）(偏移: 0x8)
- `IntPoint Pt`（整数Point Pt）(偏移: 0x10)
- `OutPt Next`（OutPt 下一个）(偏移: 0x20)
- `OutPt Prev`（OutPt Prev）(偏移: 0x24)

---

## OutRec（OutRec）

### 字段 (7)

- `int Idx`（int Idx）(偏移: 0x8)
- `bool IsHole`（bool 是否Hole）(偏移: 0xC)
- `bool IsOpen`（bool 是否打开）(偏移: 0xD)
- `OutRec FirstLeft`（OutRec 第一个左）(偏移: 0x10)
- `OutPt Pts`（OutPt Pts）(偏移: 0x14)
- `OutPt BottomPt`（OutPt 底部Pt）(偏移: 0x18)
- `PolyNode PolyNode`（Poly节点 Poly节点）(偏移: 0x1C)

---

## Outline（Outline）

**继承**: Shadow（Shadow）

### 方法 (1)

- `void ModifyMesh(VertexHelper vh)`
  （void Modify网格（Vertex辅助器 vh））

---

## P2T（P2T）

### 字段 (1)

- `TriangulationAlgorithm _defaultAlgorithm`（TriangulationAlgorithm _defaultAlgorithm）(偏移: 0x311530F9)

### 方法 (4)

- `void Triangulate(Polygon p)`
  （void Triangulate（Polygon p））
- `TriangulationContext CreateContext(TriangulationAlgorithm algorithm)`
  （TriangulationContext 创建Context（TriangulationAlgorithm algorithm））
- `void Triangulate(TriangulationAlgorithm algorithm, Triangulatable t)`
  （void Triangulate（TriangulationAlgorithm algorithm, Triangulatable t））
- `void Triangulate(TriangulationContext tcx)`
  （void Triangulate（TriangulationContext tcx））

---

## PInfo（P信息）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## PInvokeAttributes（PInvokeAttributes）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## PQHandle（PQ句柄）

### 字段 (2)

- `int Invalid`（int Invalid）(偏移: 0x0)
- `int _handle`（int _handle）(偏移: 0x0)

---

## PackingAttribute（PackingAttribute）

**继承**: Attribute（属性）

### 字段 (9)

- `string[] displayNames`（string[] displayNames）(偏移: 0x8)
- `float[] range`（float[] range）(偏移: 0xC)
- `FieldPacking packingScheme`（FieldPacking packingScheme）(偏移: 0x10)
- `int offsetInSource`（int offsetInSource）(偏移: 0x14)
- `int sizeInBits`（int sizeInBits）(偏移: 0x18)
- `bool isDirection`（bool is方向）(偏移: 0x1C)
- `bool sRGBDisplay`（bool sRGB颜色Display）(偏移: 0x1D)
- `bool checkIsNormalized`（bool check是否Normalized）(偏移: 0x1E)
- `string preprocessor`（string preprocessor）(偏移: 0x20)

---

## PackingRules（PackingRules）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## PaddingMode（Padding模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## PaniniProjection（PaniniProjection）

**继承**: VolumeComponent, IPostProcessComponent（体积组件, I后处理组件）

### 字段 (2)

- `ClampedFloatParameter distance`（Clamped浮点数Parameter distance）(偏移: 0x1C)
- `ClampedFloatParameter cropToFit`（Clamped浮点数Parameter cropToFit）(偏移: 0x20)

### 方法 (2)

- `bool IsActive()`
  （布尔值 是否激活的（））
- `bool IsTileCompatible()`
  （布尔值 是否瓦片兼容（））

---

## ParallelDeflateOutputStream（ParallelDeflateOutput流）

**继承**: Stream（流）

### 字段 (27)

- `int IO_BUFFER_SIZE_DEFAULT`（int IO_BUFFER_SIZE_DEFAULT）(偏移: 0x0)
- `int BufferPairsPerCore`（int 缓冲区PairsPerCore）(偏移: 0x4)
- `List<WorkItem> _pool`（List<WorkItem> _pool）(偏移: 0x14)
- `bool _leaveOpen`（布尔值 _保持打开）(偏移: 0x18)
- `bool emitting`（bool emitting）(偏移: 0x19)
- `Stream _outStream`（流 _out流）(偏移: 0x1C)
- `int _maxBufferPairs`（int _max缓冲区Pairs）(偏移: 0x20)
- `int _bufferSize`（int _buffer大小）(偏移: 0x24)
- `AutoResetEvent _newlyCompressedBlob`（自动重置事件 _newlyCompressedBlob）(偏移: 0x28)
- `object _outputLock`（object _outputLock）(偏移: 0x2C)
- `bool _isClosed`（bool _isClosed）(偏移: 0x30)
- `bool _firstWriteDone`（bool _firstWriteDone）(偏移: 0x31)
- `int _currentlyFilling`（int _currentlyFilling）(偏移: 0x34)
- `int _lastFilled`（int _lastFilled）(偏移: 0x38)
- `int _lastWritten`（int _lastWritten）(偏移: 0x3C)
- `int _latestCompressed`（int _latestCompressed）(偏移: 0x40)
- `int _Crc32`（int _Crc32）(偏移: 0x44)
- `CRC32 _runningCrc`（CRC32 _runningCrc）(偏移: 0x48)
- `object _latestLock`（object _latestLock）(偏移: 0x4C)
- `Queue<int> _toWrite`（Queue<int> _toWrite）(偏移: 0x50)
- `Queue<int> _toFill`（Queue<int> _toFill）(偏移: 0x54)
- `long _totalBytesProcessed`（long _totalBytesProcessed）(偏移: 0x58)
- `CompressionLevel _compressLevel`（Compression等级 _compress等级）(偏移: 0x60)
- `Exception _pendingException`（Exception _pendingException）(偏移: 0x64)
- `bool _handlingException`（bool _handlingException）(偏移: 0x68)
- `object _eLock`（object _eLock）(偏移: 0x6C)
- `ParallelDeflateOutputStream.TraceBits _DesiredTrace`（ParallelDeflateOutputStream.TraceBits _DesiredTrace）(偏移: 0x70)

### 方法 (25)

- `CompressionStrategy get_Strategy()`
  （CompressionStrategy get_Strategy（））
- `void set_Strategy(CompressionStrategy value)`
  （void set_Strategy（CompressionStrategy value））
- `void set_MaxBufferPairs(int value)`
  （void set_最大缓冲区Pairs（int value））
- `void set_BufferSize(int value)`
  （void set_缓冲区大小（int value））
- `void _InitializePoolOfWorkItems()`
  （void _初始化池OfWorkItems（））
- `void Write(byte[] buffer, int offset, int count)`
  （void 写入（字节[] buffer, 整数 offset, 整数 count））
- `void _FlushFinish()`
  （void _FlushFinish（））
- `void _Flush(bool lastInput)`
  （void _Flush（bool lastInput））
- `void Flush()`
  （void 刷新（））
- `void Close()`
  （void 关闭（））
- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `void Reset(Stream stream)`
  （void 重置（流 stream））
- `void EmitPendingBuffers(bool doAll, bool mustWait)`
  （void EmitPendingBuffers（bool doAll, bool mustWait））
- `void _DeflateOne(object wi)`
  （void _DeflateOne（object wi））
- `bool DeflateOneSegment(WorkItem workitem)`
  （bool DeflateOneSegment（Work项目 workitem））
- `bool get_CanSeek()`
  （布尔值 获取_能否查找（））
- `bool get_CanRead()`
  （布尔值 获取_能否读取（））
- `bool get_CanWrite()`
  （布尔值 获取_能否写入（））
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

---

## ParallelDeflateOutputStream.TraceBits（ParallelDeflateOutputStream.TraceBits）

### 字段 (1)

- `uint value__`（无符号整数 值__）(偏移: 0x0)

---

## ParameterAttributes（ParameterAttributes）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ParameterInfo（Parameter信息）

**继承**: ICustomAttributeProvider, IObjectReference, _ParameterInfo（I自定义的Attribute提供者, I对象引用, _Parameter信息）

### 字段 (7)

- `Type ClassImpl`（类型 类Impl）(偏移: 0x8)
- `object DefaultValueImpl`（object 默认的值Impl）(偏移: 0xC)
- `MemberInfo MemberImpl`（Member信息 MemberImpl）(偏移: 0x10)
- `string NameImpl`（string 名称Impl）(偏移: 0x14)
- `int PositionImpl`（int PositionImpl）(偏移: 0x18)
- `ParameterAttributes AttrsImpl`（ParameterAttributes AttrsImpl）(偏移: 0x1C)
- `MarshalAsAttribute marshalAs`（MarshalAsAttribute marshalAs）(偏移: 0x20)

### 方法 (17)

- `string ToString()`
  （字符串 转字符串（））
- `void FormatParameters(StringBuilder sb, ParameterInfo[] p, CallingConventions callingConvention, bool serialization)`
  （void 格式化Parameters（字符串构建器 sb, ParameterInfo[] p, CallingConventions callingConvention, bool serialization））
- `Type get_ParameterType()`
  （类型 get_Parameter类型（））
- `ParameterAttributes get_Attributes()`
  （ParameterAttributes get_Attributes（））
- `bool get_IsIn()`
  （bool get_是否In（））
- `bool get_IsOptional()`
  （bool get_是否Optional（））
- `bool get_IsOut()`
  （bool get_是否Out（））
- `bool get_IsRetval()`
  （bool get_是否Retval（））
- `string get_Name()`
  （字符串 获取_名称（））
- `int get_Position()`
  （int get_Position（））
- `object[] GetPseudoCustomAttributes()`
  （object[] 获取Pseudo自定义的Attributes（））
- `object GetDefaultValueImpl()`
  （object 获取默认的值Impl（））
- `object get_DefaultValue()`
  （object get_默认的值（））
- `object[] GetCustomAttributes(Type attributeType, bool inherit)`
  （对象[] 获取自定义属性（类型 attributeType, 布尔值 继承））
- `object GetRealObject(StreamingContext context)`
  （对象 获取真实对象（流上下文 context））
- `bool IsDefined(Type attributeType, bool inherit)`
  （布尔值 是否已定义（类型 attributeType, 布尔值 继承））
- `ParameterInfo New(ParameterInfo pinfo, MemberInfo member)`
  （Parameter信息 新的（Parameter信息 pinfo, Member信息 member））

---

## ParameterModifier（Parameter修改器）

### 字段 (1)

- `bool[] _byRef`（bool[] _byRef）(偏移: 0x0)

---

## ParameterizedStrings（ParameterizedStrings）

### 字段 (1)

- `ParameterizedStrings.LowLevelStack _cachedStack`（ParameterizedStrings.Low等级栈 _cached栈）(偏移: 0x80000000)

### 方法 (9)

- `string Evaluate(string format, ParameterizedStrings.FormatParam[] args)`
  （string Evaluate（string format, ParameterizedStrings.格式化Param[] args））
- `string EvaluateInternal(string format, ref int pos, ParameterizedStrings.FormatParam[] args, ParameterizedStrings.LowLevelStack stack, ref ParameterizedStrings.FormatParam[] dynamicVars, ref ParameterizedStrings.FormatParam[] staticVars)`
  （string Evaluate内部的（string format, ref int pos, ParameterizedStrings.格式化Param[] args, ParameterizedStrings.Low等级栈 stack, ref ParameterizedStrings.FormatParam[] dynamicVars, ref ParameterizedStrings.FormatParam[] staticVars））
- `bool AsBool(int i)`
  （bool As布尔值（int i））
- `int AsInt(bool b)`
  （int As整数（bool b））
- `string StringFromAsciiBytes(byte[] buffer, int offset, int length)`
  （string 字符串FromAsciiBytes（byte[] buffer, int offset, int length））
- `int snprintf(byte* str, IntPtr size, string format, string arg1)`
  （int snprintf（byte* str, 整数Ptr size, string format, string arg1））
- `int snprintf(byte* str, IntPtr size, string format, int arg1)`
  （int snprintf（byte* str, 整数Ptr size, string format, int arg1））
- `string FormatPrintF(string format, object arg)`
  （string 格式化PrintF（string format, object arg））
- `ParameterizedStrings.FormatParam[] GetDynamicOrStaticVariables(char c, ref ParameterizedStrings.FormatParam[] dynamicVars, ref ParameterizedStrings.FormatParam[] staticVars, out int index)`
  （ParameterizedStrings.格式化Param[] 获取动态的Or静态的Variables（char c, ref ParameterizedStrings.FormatParam[] dynamicVars, ref ParameterizedStrings.FormatParam[] staticVars, out int index））

---

## ParameterizedStrings.FormatParam（ParameterizedStrings.格式化Param）

### 字段 (2)

- `int _int32`（int _int32）(偏移: 0x0)
- `string _string`（string _string）(偏移: 0x4)

### 方法 (4)

- `ParameterizedStrings.FormatParam op_Implicit(int value)`
  （ParameterizedStrings.格式化Param op_Implicit（int value））
- `int get_Int32()`
  （int get_Int32（））
- `string get_String()`
  （string get_字符串（））
- `object get_Object()`
  （object get_对象（））

---

## ParameterizedStrings.LowLevelStack（ParameterizedStrings.Low等级栈）

### 字段 (2)

- `ParameterizedStrings.FormatParam[] _arr`（ParameterizedStrings.格式化Param[] _arr）(偏移: 0x8)
- `int _count`（int _count）(偏移: 0xC)

### 方法 (3)

- `ParameterizedStrings.FormatParam Pop()`
  （ParameterizedStrings.格式化Param Pop（））
- `void Push(ParameterizedStrings.FormatParam item)`
  （void Push（ParameterizedStrings.格式化Param item））
- `void Clear()`
  （void 清除（））

---

## ParameterizedThreadStart（ParameterizedThread开始）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(object obj)`
  （void Invoke（object obj））
- `IAsyncResult BeginInvoke(object obj, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（object obj, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## ParamsArray（Params数组）

### 字段 (7)

- `object[] oneArgArray`（object[] oneArg数组）(偏移: 0x0)
- `object[] twoArgArray`（object[] twoArg数组）(偏移: 0x4)
- `object[] threeArgArray`（object[] threeArg数组）(偏移: 0x8)
- `object arg0`（object arg0）(偏移: 0x0)
- `object arg1`（object arg1）(偏移: 0x4)
- `object arg2`（object arg2）(偏移: 0x8)
- `object[] args`（对象[] 参数）(偏移: 0xC)

### 方法 (3)

- `int get_Length()`
  （整数 获取_长度（））
- `object get_Item(int index)`
  （对象 获取_项（整数 index））
- `object GetAtSlow(int index)`
  （object 获取AtSlow（int index））

---

## Parent（父级）

**继承**: ChoiceBase（选择基类）

### 字段 (1)

- `ChoiceBase[] childs`（ChoiceBase[] childs）(偏移: 0x14)

### 方法 (1)

- `bool OnSelect()`
  （bool On选择（））

---

## ParseFailureKind（解析FailureKind）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ParseFlags（解析Flags）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ParseNumbers（解析Numbers）

### 方法 (10)

- `int StringToInt(string value, int fromBase, int flags)`
  （int 字符串To整数（string value, int fromBase, int flags））
- `int StringToInt(string value, int fromBase, int flags, int* parsePos)`
  （int 字符串To整数（string value, int fromBase, int flags, int* parsePos））
- `string LongToString(long value, int toBase, int width, char paddingChar, int flags)`
  （string LongTo字符串（long value, int toBase, int width, char paddingChar, int flags））
- `long StringToLong(string value, int fromBase, int flags)`
  （long 字符串ToLong（string value, int fromBase, int flags））
- `long StringToLong(string value, int fromBase, int flags, int* parsePos)`
  （long 字符串ToLong（string value, int fromBase, int flags, int* parsePos））
- `string IntToString(int value, int toBase, int width, char paddingChar, int flags)`
  （string 整数To字符串（int value, int toBase, int width, char paddingChar, int flags））
- `void EndianSwap(ref byte[] value)`
  （void EndianSwap（ref byte[] value））
- `StringBuilder ConvertToBase2(byte[] value)`
  （字符串构建器 转换ToBase2（byte[] value））
- `StringBuilder ConvertToBase8(byte[] value)`
  （字符串构建器 转换ToBase8（byte[] value））
- `StringBuilder ConvertToBase16(byte[] value)`
  （字符串构建器 转换ToBase16（byte[] value））

---

## ParseRecord（解析Record）

### 字段 (41)

- `int parseRecordIdCount`（int parseRecordId数量）(偏移: 0x0)
- `InternalParseTypeE PRparseTypeEnum`（内部的解析类型E PRparse类型Enum）(偏移: 0x8)
- `InternalObjectTypeE PRobjectTypeEnum`（内部的对象类型E PRobject类型Enum）(偏移: 0xC)
- `InternalArrayTypeE PRarrayTypeEnum`（内部的数组类型E PRarray类型Enum）(偏移: 0x10)
- `InternalMemberTypeE PRmemberTypeEnum`（内部的Member类型E PRmember类型Enum）(偏移: 0x14)
- `InternalMemberValueE PRmemberValueEnum`（内部的Member值E PRmember值Enum）(偏移: 0x18)
- `InternalObjectPositionE PRobjectPositionEnum`（内部的对象PositionE PRobjectPositionEnum）(偏移: 0x1C)
- `string PRname`（string PRname）(偏移: 0x20)
- `string PRvalue`（string PRvalue）(偏移: 0x24)
- `object PRvarValue`（object PRvar值）(偏移: 0x28)
- `string PRkeyDt`（string PRkeyDt）(偏移: 0x2C)
- `Type PRdtType`（类型 PRdt类型）(偏移: 0x30)
- `InternalPrimitiveTypeE PRdtTypeCode`（内部的Primitive类型E PRdt类型Code）(偏移: 0x34)
- `bool PRisEnum`（bool PRisEnum）(偏移: 0x38)
- `long PRobjectId`（long PRobjectId）(偏移: 0x40)
- `long PRidRef`（long PRidRef）(偏移: 0x48)
- `string PRarrayElementTypeString`（string PRarray元素类型字符串）(偏移: 0x50)
- `Type PRarrayElementType`（类型 PRarray元素类型）(偏移: 0x54)
- `bool PRisArrayVariant`（bool PRis数组变异体）(偏移: 0x58)
- `InternalPrimitiveTypeE PRarrayElementTypeCode`（内部的Primitive类型E PRarray元素类型Code）(偏移: 0x5C)
- `int PRrank`（int PRrank）(偏移: 0x60)
- `int[] PRlengthA`（int[] PRlengthA）(偏移: 0x64)
- `int[] PRpositionA`（int[] PRpositionA）(偏移: 0x68)
- `int[] PRlowerBoundA`（int[] PRlowerBoundA）(偏移: 0x6C)
- `int[] PRupperBoundA`（int[] PRupperBoundA）(偏移: 0x70)
- `int[] PRindexMap`（int[] PRindex映射）(偏移: 0x74)
- `int PRmemberIndex`（int PRmember索引）(偏移: 0x78)
- `int PRlinearlength`（int PRlinearlength）(偏移: 0x7C)
- `int[] PRrectangularMap`（int[] PRrectangular映射）(偏移: 0x80)
- `bool PRisLowerBound`（bool PRis下半身Bound）(偏移: 0x84)
- `long PRtopId`（long PRtopId）(偏移: 0x88)
- `long PRheaderId`（long PRheaderId）(偏移: 0x90)
- `ReadObjectInfo PRobjectInfo`（Read对象信息 PRobject信息）(偏移: 0x98)
- `bool PRisValueTypeFixup`（bool PRis值类型Fixup）(偏移: 0x9C)
- `object PRnewObj`（object PRnewObj）(偏移: 0xA0)
- `object[] PRobjectA`（object[] PRobjectA）(偏移: 0xA4)
- `PrimitiveArray PRprimitiveArray`（Primitive数组 PRprimitive数组）(偏移: 0xA8)
- `bool PRisRegistered`（bool PRisRegistered）(偏移: 0xAC)
- `object[] PRmemberData`（object[] PRmember数据）(偏移: 0xB0)
- `SerializationInfo PRsi`（Serialization信息 PRsi）(偏移: 0xB4)
- `int PRnullCount`（int PRnull数量）(偏移: 0xB8)

### 方法 (1)

- `void Init()`
  （void 初始化（））

---

## ParsingError（ParsingError）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## ParticleSpaceSetter（粒子SpaceSetter）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (1)

- `ParticleSystem[] particleSystems`（粒子System[] particleSystems）(偏移: 0xC)

### 方法 (1)

- `void SetSpace(Transform tsf)`
  （void 集合Space（变换 tsf））

---

## ParticleSystem（粒子系统）

**继承**: Component（组件）

### 方法 (17)

- `void Emit(Vector3 position, Vector3 velocity, float size, float lifetime, Color32 color)`
  （void Emit（三维向量 position, 三维向量 velocity, float size, float lifetime, Color32 color））
- `void Emit(ParticleSystem.Particle particle)`
  （void Emit（粒子System.粒子 particle））
- `bool get_isPlaying()`
  （bool get_isPlaying（））
- `bool get_isEmitting()`
  （bool get_isEmitting（））
- `void Play(bool withChildren)`
  （void 播放（bool withChildren））
- `void Play()`
  （void 播放（））
- `void Stop(bool withChildren, ParticleSystemStopBehavior stopBehavior)`
  （void 停止（bool withChildren, 粒子系统停止Behavior stopBehavior））
- `void Stop(bool withChildren)`
  （void 停止（bool withChildren））
- `void Stop()`
  （void 停止（））
- `void Clear(bool withChildren)`
  （void 清除（bool withChildren））
- `void Clear()`
  （void 清除（））
- `void Emit(int count)`
  （void Emit（int count））
- `void Emit_Internal(int count)`
  （void Emit_内部的（int count））
- `void Emit(ParticleSystem.EmitParams emitParams, int count)`
  （void Emit（粒子System.EmitParams emitParams, int count））
- `void EmitOld_Internal(ref ParticleSystem.Particle particle)`
  （void EmitOld_内部的（ref ParticleSystem.Particle particle））
- `ParticleSystem.MainModule get_main()`
  （粒子System.主要的模块 get_main（））
- `void Emit_Injected(ref ParticleSystem.EmitParams emitParams, int count)`
  （void Emit_Injected（ref ParticleSystem.EmitParams emitParams, int count））

---

## ParticleSystem.EmitParams（粒子System.EmitParams）

### 字段 (12)

- `ParticleSystem.Particle m_Particle`（粒子System.粒子 m_粒子）(偏移: 0x0)
- `bool m_PositionSet`（bool m_Position集合）(偏移: 0x84)
- `bool m_VelocitySet`（bool m_速度集合）(偏移: 0x85)
- `bool m_AxisOfRotationSet`（bool m_轴OfRotation集合）(偏移: 0x86)
- `bool m_RotationSet`（bool m_Rotation集合）(偏移: 0x87)
- `bool m_AngularVelocitySet`（bool m_Angular速度集合）(偏移: 0x88)
- `bool m_StartSizeSet`（bool m_开始大小集合）(偏移: 0x89)
- `bool m_StartColorSet`（bool m_开始颜色集合）(偏移: 0x8A)
- `bool m_RandomSeedSet`（bool m_随机Seed集合）(偏移: 0x8B)
- `bool m_StartLifetimeSet`（bool m_开始Lifetime集合）(偏移: 0x8C)
- `bool m_MeshIndexSet`（bool m_网格索引集合）(偏移: 0x8D)
- `bool m_ApplyShapeToPosition`（bool m_应用ShapeToPosition）(偏移: 0x8E)

---

## ParticleSystem.MainModule（粒子System.主要的模块）

### 字段 (1)

- `ParticleSystem m_ParticleSystem`（粒子系统 m_粒子系统）(偏移: 0x0)

### 方法 (2)

- `void set_customSimulationSpace(Transform value)`
  （void set_customSimulationSpace（变换 value））
- `void set_customSimulationSpace_Injected(ref ParticleSystem.MainModule _unity_self, Transform value)`
  （void set_customSimulationSpace_Injected（ref ParticleSystem.MainModule _unity_self, 变换 value））

---

## ParticleSystem.Particle（粒子System.粒子）

### 字段 (17)

- `Vector3 m_Position`（三维向量 m_位置）(偏移: 0x0)
- `Vector3 m_Velocity`（三维向量 m_速度）(偏移: 0xC)
- `Vector3 m_AnimatedVelocity`（三维向量 m_Animated速度）(偏移: 0x18)
- `Vector3 m_InitialVelocity`（三维向量 m_Initial速度）(偏移: 0x24)
- `Vector3 m_AxisOfRotation`（三维向量 m_轴OfRotation）(偏移: 0x30)
- `Vector3 m_Rotation`（三维向量 m_Rotation）(偏移: 0x3C)
- `Vector3 m_AngularVelocity`（三维向量 m_Angular速度）(偏移: 0x48)
- `Vector3 m_StartSize`（三维向量 m_开始大小）(偏移: 0x54)
- `Color32 m_StartColor`（Color32 m_开始颜色）(偏移: 0x60)
- `uint m_RandomSeed`（uint m_随机Seed）(偏移: 0x64)
- `uint m_ParentRandomSeed`（uint m_父级随机Seed）(偏移: 0x68)
- `float m_Lifetime`（float m_Lifetime）(偏移: 0x6C)
- `float m_StartLifetime`（float m_开始Lifetime）(偏移: 0x70)
- `int m_MeshIndex`（int m_网格索引）(偏移: 0x74)
- `float m_EmitAccumulator0`（float m_EmitAccumulator0）(偏移: 0x78)
- `float m_EmitAccumulator1`（float m_EmitAccumulator1）(偏移: 0x7C)
- `uint m_Flags`（uint m_Flags）(偏移: 0x80)

### 方法 (10)

- `void set_lifetime(float value)`
  （void set_lifetime（float value））
- `void set_position(Vector3 value)`
  （void 设置_位置（三维向量 value））
- `void set_velocity(Vector3 value)`
  （void set_velocity（三维向量 value））
- `void set_remainingLifetime(float value)`
  （void set_remainingLifetime（float value））
- `void set_startLifetime(float value)`
  （void set_startLifetime（float value））
- `void set_startColor(Color32 value)`
  （void set_start颜色（Color32 value））
- `void set_randomSeed(uint value)`
  （void set_randomSeed（uint value））
- `void set_startSize(float value)`
  （void set_start大小（float value））
- `void set_rotation3D(Vector3 value)`
  （void set_rotation3D（三维向量 value））
- `void set_angularVelocity3D(Vector3 value)`
  （void set_angularVelocity3D（三维向量 value））

---

## ParticleSystemRenderer（粒子系统渲染器）

**继承**: Renderer（渲染器）

### 方法 (1)

- `int GetMeshes([Out] Mesh[] meshes)`
  （int 获取Meshes（[Out] Mesh[] meshes））

---

## ParticleSystemStopBehavior（粒子系统停止Behavior）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Path（路径）

### 字段 (10)

- `char[] InvalidPathChars`（char[] Invalid路径Chars）(偏移: 0x0)
- `char AltDirectorySeparatorChar`（char AltDirectorySeparatorChar）(偏移: 0x4)
- `char DirectorySeparatorChar`（char DirectorySeparatorChar）(偏移: 0x6)
- `char PathSeparator`（char 路径Separator）(偏移: 0x8)
- `string DirectorySeparatorStr`（string DirectorySeparatorStr）(偏移: 0xC)
- `char VolumeSeparatorChar`（char VolumeSeparatorChar）(偏移: 0x10)
- `char[] PathSeparatorChars`（char[] 路径SeparatorChars）(偏移: 0x14)
- `bool dirEqualsVolume`（bool dirEqualsVolume）(偏移: 0x18)
- `char[] trimEndCharsWindows`（char[] trim结束CharsWindows）(偏移: 0x1C)
- `char[] trimEndCharsUnix`（char[] trim结束CharsUnix）(偏移: 0x20)

### 方法 (29)

- `string ChangeExtension(string path, string extension)`
  （string Change扩展（string path, string extension））
- `string Combine(string path1, string path2)`
  （string Combine（string path1, string path2））
- `string CleanPath(string s)`
  （string Clean路径（string s））
- `string GetDirectoryName(string path)`
  （string 获取Directory名称（string path））
- `string GetFileName(string path)`
  （string 获取文件名称（string path））
- `string GetFileNameWithoutExtension(string path)`
  （string 获取文件名称Without扩展（string path））
- `string GetFullPath(string path)`
  （string 获取满路径（string path））
- `string GetFullPathInternal(string path)`
  （string 获取满路径内部的（string path））
- `int GetFullPathName(string path, int numBufferChars, StringBuilder buffer, ref IntPtr lpFilePartOrNull)`
  （int 获取满路径名称（string path, int numBufferChars, 字符串构建器 buffer, ref IntPtr lpFilePartOrNull））
- `string GetFullPathName(string path)`
  （string 获取满路径名称（string path））
- `string WindowsDriveAdjustment(string path)`
  （string WindowsDriveAdjustment（string path））
- `string InsecureGetFullPath(string path)`
  （string Insecure获取满路径（string path））
- `bool IsDirectorySeparator(char c)`
  （bool 是否DirectorySeparator（char c））
- `string GetPathRoot(string path)`
  （string 获取路径根（string path））
- `bool IsPathRooted(string path)`
  （bool 是否路径Rooted（string path））
- `char[] GetInvalidPathChars()`
  （char[] 获取Invalid路径Chars（））
- `int findExtension(string path)`
  （int find扩展（string path））
- `string GetServerAndShare(string path)`
  （string 获取服务器AndShare（string path））
- `bool SameRoot(string root, string path)`
  （bool Same根（string root, string path））
- `string CanonicalizePath(string path)`
  （string Canonicalize路径（string path））
- `string Combine(string[] paths)`
  （string Combine（string[] paths））
- `string Combine(string path1, string path2, string path3)`
  （string Combine（string path1, string path2, string path3））
- `void Validate(string path)`
  （void 验证（string path））
- `void Validate(string path, string parameterName)`
  （void 验证（string path, string parameterName））
- `string get_DirectorySeparatorCharAsString()`
  （string get_DirectorySeparatorCharAs字符串（））
- `char[] get_TrimEndChars()`
  （char[] get_Trim结束Chars（））
- `void CheckSearchPattern(string searchPattern)`
  （void 检查搜索Pattern（string searchPattern））
- `void CheckInvalidPathChars(string path, bool checkAdditional = False)`
  （void 检查Invalid路径Chars（string path, bool checkAdditional = False））
- `string InternalCombine(string path1, string path2)`
  （string 内部的Combine（string path1, string path2））

---

## Path（路径）

### 字段 (25)

- `CatmullRomDecoder _catmullRomDecoder`（CatmullRomDecoder _catmullRomDecoder）(偏移: 0x0)
- `LinearDecoder _linearDecoder`（LinearDecoder _linearDecoder）(偏移: 0x4)
- `CubicBezierDecoder _cubicBezierDecoder`（CubicBezierDecoder _cubicBezierDecoder）(偏移: 0x8)
- `float[] wpLengths`（float[] wpLengths）(偏移: 0x8)
- `Vector3[] wps`（Vector3[] wps）(偏移: 0xC)
- `PathType type`（路径类型 type）(偏移: 0x10)
- `int subdivisionsXSegment`（int subdivisionsXSegment）(偏移: 0x14)
- `int subdivisions`（int subdivisions）(偏移: 0x18)
- `ControlPoint[] controlPoints`（控制Point[] controlPoints）(偏移: 0x1C)
- `float length`（浮点数 长度）(偏移: 0x20)
- `bool isFinalized`（bool isFinalized）(偏移: 0x24)
- `float[] timesTable`（float[] timesTable）(偏移: 0x28)
- `float[] lengthsTable`（float[] lengthsTable）(偏移: 0x2C)
- `int linearWPIndex`（int linearWP索引）(偏移: 0x30)
- `bool addedExtraStartWp`（bool added额外的开始Wp）(偏移: 0x34)
- `bool addedExtraEndWp`（bool added额外的结束Wp）(偏移: 0x35)
- `PathOptions plugOptions`（路径Options plugOptions）(偏移: 0x38)
- `Path _incrementalClone`（路径 _incremental克隆）(偏移: 0x98)
- `int _incrementalIndex`（int _incremental索引）(偏移: 0x9C)
- `ABSPathDecoder _decoder`（ABS路径Decoder _decoder）(偏移: 0xA0)
- `bool _changed`（bool _changed）(偏移: 0xA4)
- `Vector3[] nonLinearDrawWps`（Vector3[] nonLinearDrawWps）(偏移: 0xA8)
- `Vector3 targetPosition`（三维向量 targetPosition）(偏移: 0xAC)
- `Nullable<Vector3> lookAtPosition`（Nullable<Vector3> lookAtPosition）(偏移: 0xB8)
- `Color gizmoColor`（颜色 gizmo颜色）(偏移: 0xC8)

### 方法 (14)

- `int get_minInputWaypoints()`
  （整数 获取_最小输入路点（））
- `void FinalizePath(bool isClosedPath, AxisConstraint lockPositionAxes, Vector3 currTargetVal)`
  （void Finalize路径（bool isClosedPath, 轴Constraint lockPositionAxes, 三维向量 currTargetVal））
- `Vector3 GetPoint(float perc, bool convertToConstantPerc = False)`
  （三维向量 获取Point（float perc, bool convertToConstantPerc = False））
- `float ConvertToConstantPathPerc(float perc)`
  （float 转换ToConstant路径Perc（float perc））
- `int GetWaypointIndexFromPerc(float perc, bool isMovingForward)`
  （int 获取Waypoint索引FromPerc（float perc, bool isMovingForward））
- `Vector3[] GetDrawPoints(Path p, int drawSubdivisionsXSegment)`
  （Vector3[] 获取DrawPoints（路径 p, int drawSubdivisionsXSegment））
- `void RefreshNonLinearDrawWps(Path p)`
  （void 刷新NonLinearDrawWps（路径 p））
- `void Destroy()`
  （void 销毁（））
- `Path CloneIncremental(int loopIncrement)`
  （路径 克隆Incremental（int loopIncrement））
- `void AssignWaypoints(Vector3[] newWps, bool cloneWps = False)`
  （void AssignWaypoints（Vector3[] newWps, bool cloneWps = False））
- `void AssignDecoder(PathType pathType)`
  （void AssignDecoder（路径类型 pathType））
- `void Draw()`
  （void Draw（））
- `void Draw(Path p)`
  （void Draw（路径 p））
- `Vector3 ConvertToDrawPoint(Vector3 wp, PathOptions plugOptions)`
  （三维向量 转换ToDrawPoint（三维向量 wp, 路径Options plugOptions））

---

## Path（路径）

**继承**: IPathInternals（I路径Internals）

### 字段 (24)

- `PathHandler pathHandler`（路径处理器 path处理器）(偏移: 0x8)
- `OnPathDelegate callback`（On路径委托 callback）(偏移: 0xC)
- `OnPathDelegate immediateCallback`（On路径委托 immediate回调）(偏移: 0x10)
- `object stateLock`（object stateLock）(偏移: 0x18)
- `ITraversalProvider traversalProvider`（ITraversal提供者 traversal提供者）(偏移: 0x1C)
- `PathCompleteState completeState`（路径Complete状态 complete状态）(偏移: 0x20)
- `List<GraphNode> path`（List<GraphNode> path）(偏移: 0x28)
- `List<Vector3> vectorPath`（List<Vector3> vector路径）(偏移: 0x2C)
- `PathNode currentR`（路径节点 currentR）(偏移: 0x30)
- `float duration`（浮点数 持续时间）(偏移: 0x34)
- `int searchedNodes`（int searchedNodes）(偏移: 0x38)
- `bool hasBeenReset`（bool hasBeen重置）(偏移: 0x3D)
- `NNConstraint nnConstraint`（NNConstraint nnConstraint）(偏移: 0x40)
- `Path next`（路径 next）(偏移: 0x44)
- `Heuristic heuristic`（Heuristic heuristic）(偏移: 0x48)
- `float heuristicScale`（float heuristic缩放）(偏移: 0x4C)
- `GraphNode hTargetNode`（Graph节点 h目标节点）(偏移: 0x54)
- `Int3 hTarget`（Int3 h目标）(偏移: 0x58)
- `int enabledTags`（int enabledTags）(偏移: 0x64)
- `int[] ZeroTagPenalties`（int[] Zero标签Penalties）(偏移: 0x0)
- `int[] internalTagPenalties`（int[] internal标签Penalties）(偏移: 0x68)
- `int[] manualTagPenalties`（int[] manual标签Penalties）(偏移: 0x6C)
- `List<object> claimed`（List<object> claimed）(偏移: 0x70)
- `bool releasedNotSilent`（bool releasedNotSilent）(偏移: 0x74)

### 方法 (41)

- `PathState get_PipelineState()`
  （路径状态 get_Pipeline状态（））
- `void set_PipelineState(PathState value)`
  （void set_Pipeline状态（路径状态 value））
- `PathCompleteState get_CompleteState()`
  （路径Complete状态 get_Complete状态（））
- `void set_CompleteState(PathCompleteState value)`
  （void set_Complete状态（路径Complete状态 value））
- `bool get_error()`
  （bool get_error（））
- `string get_errorLog()`
  （string get_errorLog（））
- `void set_errorLog(string value)`
  （void set_errorLog（string value））
- `bool get_recycled()`
  （bool get_recycled（））
- `ushort get_pathID()`
  （ushort get_pathID（））
- `void set_pathID(ushort value)`
  （void set_pathID（ushort value））
- `int[] get_tagPenalties()`
  （int[] get_tagPenalties（））
- `void set_tagPenalties(int[] value)`
  （void set_tagPenalties（int[] value））
- `bool get_FloodingPath()`
  （布尔值 获取_泛洪路径（））
- `float GetTotalLength()`
  （float 获取TotalLength（））
- `IEnumerator WaitForPath()`
  （IEnumerator WaitFor路径（））
- `void BlockUntilCalculated()`
  （void BlockUntilCalculated（））
- `uint CalculateHScore(GraphNode node)`
  （uint 计算H分数（Graph节点 node））
- `uint GetTagPenalty(int tag)`
  （uint 获取标签惩罚（int tag））
- `Int3 GetHTarget()`
  （Int3 获取H目标（））
- `bool CanTraverse(GraphNode node)`
  （bool 能否Traverse（Graph节点 node））
- `uint GetTraversalCost(GraphNode node)`
  （uint 获取TraversalCost（Graph节点 node））
- `uint GetConnectionSpecialCost(GraphNode a, GraphNode b, uint currentCost)`
  （uint 获取连接特殊Cost（Graph节点 a, Graph节点 b, uint currentCost））
- `bool IsDone()`
  （bool 是否Done（））
- `PathState GetState()`
  （路径状态 获取状态（））
- `void FailWithError(string msg)`
  （void FailWithError（string msg））
- `void LogError(string msg)`
  （void LogError（string msg））
- `void Log(string msg)`
  （void Log（string msg））
- `void Error()`
  （void Error（））
- `void ErrorCheck()`
  （void Error检查（））
- `void OnEnterPool()`
  （void 进入池时（））
- `void Reset()`
  （void 重置（））
- `void Claim(object o)`
  （void Claim（object o））
- `void ReleaseSilent(object o)`
  （void ReleaseSilent（object o））
- `void Release(object o, bool silent = False)`
  （void Release（object o, bool silent = False））
- `void Trace(PathNode from)`
  （void Trace（路径节点 from））
- `void DebugStringPrefix(PathLog logMode, StringBuilder text)`
  （void Debug字符串Prefix（路径Log logMode, 字符串构建器 text））
- `void DebugStringSuffix(PathLog logMode, StringBuilder text)`
  （void Debug字符串Suffix（路径Log logMode, 字符串构建器 text））
- `string DebugString(PathLog logMode)`
  （string Debug字符串（路径Log logMode））
- `void ReturnPath()`
  （void Return路径（））
- `void PrepareBase(PathHandler pathHandler)`
  （void Prepare基础（路径处理器 pathHandler））
- `void Cleanup()`
  （void 清理（））

---

## PathCompleteState（路径Complete状态）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## PathEndingCondition（路径EndingCondition）

### 字段 (1)

- `Path path`（路径 path）(偏移: 0x8)

---

## PathHandler（路径处理器）

### 字段 (6)

- `ushort pathID`（ushort pathID）(偏移: 0x8)
- `int threadID`（int threadID）(偏移: 0xC)
- `int totalThreadCount`（int totalThread数量）(偏移: 0x10)
- `BinaryHeap heap`（BinaryHeap heap）(偏移: 0x14)
- `PathNode[] nodes`（路径Node[] nodes）(偏移: 0x18)
- `StringBuilder DebugStringBuilder`（字符串构建器 Debug字符串构建器）(偏移: 0x1C)

### 方法 (7)

- `ushort get_PathID()`
  （ushort get_路径ID（））
- `void InitializeForPath(Path p)`
  （void 初始化For路径（路径 p））
- `void DestroyNode(GraphNode node)`
  （void 销毁节点（Graph节点 node））
- `void InitializeNode(GraphNode node)`
  （void 初始化节点（Graph节点 node））
- `PathNode GetPathNode(int nodeIndex)`
  （路径节点 获取路径节点（int nodeIndex））
- `PathNode GetPathNode(GraphNode node)`
  （路径节点 获取路径节点（Graph节点 node））
- `void ClearPathIDs()`
  （void 清除路径IDs（））

---

## PathInternal（路径内部的）

### 方法 (2)

- `bool IsPartiallyQualified(string path)`
  （bool 是否PartiallyQualified（string path））
- `bool HasIllegalCharacters(string path, bool checkAdditional)`
  （bool 是否有IllegalCharacters（string path, bool checkAdditional））

---

## PathInterpolator（路径Interpolator）

### 字段 (5)

- `List<Vector3> path`（List<Vector3> path）(偏移: 0x8)
- `float distanceToSegmentStart`（float distanceToSegment开始）(偏移: 0xC)
- `float currentDistance`（float current距离）(偏移: 0x10)
- `float currentSegmentLength`（float currentSegmentLength）(偏移: 0x14)
- `float totalDistance`（float total距离）(偏移: 0x18)

### 方法 (17)

- `Vector3 get_position()`
  （三维向量 获取_位置（））
- `Vector3 get_endPoint()`
  （三维向量 get_endPoint（））
- `Vector3 get_tangent()`
  （三维向量 get_tangent（））
- `float get_remainingDistance()`
  （浮点数 获取_剩余距离（））
- `void set_remainingDistance(float value)`
  （void set_remaining距离（float value））
- `float get_distance()`
  （浮点数 获取_距离（））
- `void set_distance(float value)`
  （void set_distance（float value））
- `int get_segmentIndex()`
  （int get_segment索引（））
- `void set_segmentIndex(int value)`
  （void set_segment索引（int value））
- `bool get_valid()`
  （bool get_valid（））
- `void SetPath(List<Vector3> path)`
  （void 集合路径（List<Vector3> path））
- `void MoveToSegment(int index, float fractionAlongSegment)`
  （void 移动ToSegment（int index, float fractionAlongSegment））
- `void MoveToClosestPoint(Vector3 point)`
  （void 移动ToClosestPoint（三维向量 point））
- `void MoveToLocallyClosestPoint(Vector3 point, bool allowForwards = True, bool allowBackwards = True)`
  （void 移动ToLocallyClosestPoint（三维向量 point, bool allowForwards = True, bool allowBackwards = True））
- `void MoveToCircleIntersection2D(Vector3 circleCenter3D, float radius, IMovementPlane transform)`
  （void 移动ToCircleIntersection2D（三维向量 circleCenter3D, float radius, IMovementPlane transform））
- `void PrevSegment()`
  （void PrevSegment（））
- `void NextSegment()`
  （void 下一个Segment（））

---

## PathLog（路径Log）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## PathMode（路径模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## PathModifier（路径修改器）

**继承**: IPathModifier（I路径修改器）

### 字段 (1)

- `Seeker seeker`（寻路器 seeker）(偏移: 0x8)

### 方法 (3)

- `void Awake(Seeker seeker)`
  （void Awake（Seeker seeker））
- `void OnDestroy(Seeker seeker)`
  （void On销毁（Seeker seeker））
- `void PreProcess(Path path)`
  （void Pre处理（路径 path））

---

## PathNNConstraint（路径NNConstraint）

**继承**: NNConstraint（NNConstraint）

### 方法 (2)

- `PathNNConstraint get_Default()`
  （路径NNConstraint get_默认的（））
- `void SetStart(GraphNode node)`
  （void 集合开始（Graph节点 node））

---

## PathNode（路径节点）

### 字段 (7)

- `GraphNode node`（图节点 node）(偏移: 0x8)
- `PathNode parent`（路径节点 parent）(偏移: 0xC)
- `ushort pathID`（ushort pathID）(偏移: 0x10)
- `ushort heapIndex`（ushort heap索引）(偏移: 0x12)
- `uint flags`（uint flags）(偏移: 0x14)
- `uint g`（uint g）(偏移: 0x18)
- `uint h`（uint h）(偏移: 0x1C)

### 方法 (12)

- `uint get_cost()`
  （uint get_cost（））
- `void set_cost(uint value)`
  （void set_cost（uint value））
- `bool get_flag1()`
  （bool get_flag1（））
- `void set_flag1(bool value)`
  （void set_flag1（bool value））
- `bool get_flag2()`
  （bool get_flag2（））
- `void set_flag2(bool value)`
  （void set_flag2（bool value））
- `uint get_G()`
  （uint get_G（））
- `void set_G(uint value)`
  （void set_G（uint value））
- `uint get_H()`
  （uint get_H（））
- `void set_H(uint value)`
  （void set_H（uint value））
- `uint get_F()`
  （uint get_F（））
- `void UpdateG(Path path)`
  （void 更新G（路径 path））

---

## PathOptions（路径Options）

**继承**: IPlugOptions（I插件选项）

### 字段 (19)

- `PathMode mode`（路径模式 mode）(偏移: 0x0)
- `OrientType orientType`（Orient类型 orient类型）(偏移: 0x4)
- `AxisConstraint lockPositionAxis`（轴Constraint lockPosition轴）(偏移: 0x8)
- `AxisConstraint lockRotationAxis`（轴Constraint lockRotation轴）(偏移: 0xC)
- `bool isClosedPath`（bool isClosed路径）(偏移: 0x10)
- `Vector3 lookAtPosition`（三维向量 lookAtPosition）(偏移: 0x14)
- `Transform lookAtTransform`（变换 lookAt变换）(偏移: 0x20)
- `float lookAhead`（float lookAhead）(偏移: 0x24)
- `bool hasCustomForwardDirection`（bool has自定义的前进方向）(偏移: 0x28)
- `Quaternion forward`（Quaternion forward）(偏移: 0x2C)
- `bool useLocalPosition`（bool use本地的Position）(偏移: 0x3C)
- `Transform parent`（变换 parent）(偏移: 0x40)
- `bool isRigidbody`（bool is刚体）(偏移: 0x44)
- `bool isRigidbody2D`（bool isRigidbody2D）(偏移: 0x45)
- `bool stableZRotation`（bool stableZRotation）(偏移: 0x46)
- `Quaternion startupRot`（Quaternion startupRot）(偏移: 0x48)
- `float startupZRot`（float startupZRot）(偏移: 0x58)
- `bool addedExtraStartWp`（bool added额外的开始Wp）(偏移: 0x5C)
- `bool addedExtraEndWp`（bool added额外的结束Wp）(偏移: 0x5D)

### 方法 (1)

- `void Reset()`
  （void 重置（））

---

## PathPlugin（路径插件）

**继承**: ABSTweenPlugin<Vector3, Path, PathOptions>（ABSTweenPlugin<三维向量, 路径, 路径Options>）

### 方法 (11)

- `void Reset(TweenerCore<Vector3, Path, PathOptions> t)`
  （void 重置（TweenerCore<三维向量, 路径, 路径Options> t））
- `void SetFrom(TweenerCore<Vector3, Path, PathOptions> t, bool isRelative)`
  （void 集合From（TweenerCore<三维向量, 路径, 路径Options> t, bool isRelative））
- `void SetFrom(TweenerCore<Vector3, Path, PathOptions> t, Path fromValue, bool setImmediately, bool isRelative)`
  （void 集合From（TweenerCore<三维向量, 路径, 路径Options> t, 路径 fromValue, bool setImmediately, bool isRelative））
- `Path ConvertToStartValue(TweenerCore<Vector3, Path, PathOptions> t, Vector3 value)`
  （路径 转换To开始值（TweenerCore<三维向量, 路径, 路径Options> t, 三维向量 value））
- `void SetRelativeEndValue(TweenerCore<Vector3, Path, PathOptions> t)`
  （void 集合Relative结束值（TweenerCore<三维向量, 路径, 路径Options> t））
- `void SetChangeValue(TweenerCore<Vector3, Path, PathOptions> t)`
  （void 集合Change值（TweenerCore<三维向量, 路径, 路径Options> t））
- `float GetSpeedBasedDuration(PathOptions options, float unitsXSecond, Path changeValue)`
  （float 获取SpeedBased持续时间（路径Options options, float unitsXSecond, 路径 changeValue））
- `void EvaluateAndApply(PathOptions options, Tween t, bool isRelative, DOGetter<Vector3> getter, DOSetter<Vector3> setter, float elapsed, Path startValue, Path changeValue, float duration, bool usingInversePosition, UpdateNotice updateNotice)`
  （void EvaluateAnd应用（路径Options options, Tween t, bool isRelative, DOGetter<Vector3> getter, DOSetter<Vector3> setter, float elapsed, 路径 startValue, 路径 changeValue, float duration, bool usingInversePosition, 更新Notice updateNotice））
- `void SetOrientation(PathOptions options, Tween t, Path path, float pathPerc, Vector3 tPos, UpdateNotice updateNotice)`
  （void 集合Orientation（路径Options options, Tween t, 路径 path, float pathPerc, 三维向量 tPos, 更新Notice updateNotice））
- `Vector3 DivideVectorByVector(Vector3 vector, Vector3 byVector)`
  （三维向量 Divide向量By向量（三维向量 vector, 三维向量 byVector））
- `Vector3 MultiplyVectorByVector(Vector3 vector, Vector3 byVector)`
  （三维向量 Multiply向量By向量（三维向量 vector, 三维向量 byVector））

---

## PathPool（路径池）

### 方法 (3)

- `void Pool(Path path)`
  （void 池（路径 path））
- `int GetTotalCreated(Type type)`
  （int 获取TotalCreated（类型 type））
- `int GetSize(Type type)`
  （int 获取大小（类型 type））

---

## PathProcessor（路径Processor）

### 字段 (14)

- `Action<Path> OnPathPreSearch`（Action<Path> On路径Pre搜索）(偏移: 0x8)
- `Action<Path> OnPathPostSearch`（Action<Path> On路径Post搜索）(偏移: 0xC)
- `Action OnQueueUnblocked`（动作 On队列Unblocked）(偏移: 0x10)
- `ThreadControlQueue queue`（Thread控制队列 queue）(偏移: 0x14)
- `AstarPath astar`（Astar路径 astar）(偏移: 0x18)
- `PathReturnQueue returnQueue`（路径Return队列 return队列）(偏移: 0x1C)
- `PathHandler[] pathHandlers`（路径Handler[] pathHandlers）(偏移: 0x20)
- `Thread[] threads`（Thread[] threads）(偏移: 0x24)
- `IEnumerator threadCoroutine`（IEnumerator thread协程）(偏移: 0x28)
- `int nextNodeIndex`（int next节点索引）(偏移: 0x2C)
- `Stack<int> nodeIndexPool`（Stack<int> node索引池）(偏移: 0x30)
- `List<int> locks`（List<int> locks）(偏移: 0x34)
- `int nextLockID`（int nextLockID）(偏移: 0x38)
- `CustomSampler profilingSampler`（自定义的Sampler profilingSampler）(偏移: 0x3C)

### 方法 (19)

- `void add_OnPathPreSearch(Action<Path> value)`
  （void add_On路径Pre搜索（Action<Path> value））
- `void remove_OnPathPreSearch(Action<Path> value)`
  （void remove_On路径Pre搜索（Action<Path> value））
- `void add_OnPathPostSearch(Action<Path> value)`
  （void add_On路径Post搜索（Action<Path> value））
- `void remove_OnPathPostSearch(Action<Path> value)`
  （void remove_On路径Post搜索（Action<Path> value））
- `void add_OnQueueUnblocked(Action value)`
  （void add_On队列Unblocked（动作 value））
- `void remove_OnQueueUnblocked(Action value)`
  （void remove_On队列Unblocked（动作 value））
- `int get_NumThreads()`
  （int get_NumThreads（））
- `bool get_IsUsingMultithreading()`
  （bool get_是否UsingMultithreading（））
- `int Lock(bool block)`
  （int Lock（bool block））
- `void Unlock(int id)`
  （void Unlock（int id））
- `PathProcessor.GraphUpdateLock PausePathfinding(bool block)`
  （路径Processor.Graph更新Lock 暂停Pathfinding（bool block））
- `void TickNonMultithreaded()`
  （void TickNonMultithreaded（））
- `void JoinThreads()`
  （void JoinThreads（））
- `void AbortThreads()`
  （void AbortThreads（））
- `int GetNewNodeIndex()`
  （int 获取新的节点索引（））
- `void InitializeNode(GraphNode node)`
  （void 初始化节点（Graph节点 node））
- `void DestroyNode(GraphNode node)`
  （void 销毁节点（Graph节点 node））
- `void CalculatePathsThreaded(PathHandler pathHandler)`
  （void 计算PathsThreaded（路径处理器 pathHandler））
- `IEnumerator CalculatePaths(PathHandler pathHandler)`
  （IEnumerator 计算Paths（路径处理器 pathHandler））

---

## PathProcessor.GraphUpdateLock（路径Processor.Graph更新Lock）

### 字段 (2)

- `PathProcessor pathProcessor`（路径Processor pathProcessor）(偏移: 0x0)
- `int id`（整数 id）(偏移: 0x4)

### 方法 (2)

- `bool get_Held()`
  （bool get_Held（））
- `void Release()`
  （void 释放（））

---

## PathReturnQueue（路径Return队列）

### 字段 (2)

- `Queue<Path> pathReturnQueue`（Queue<Path> pathReturn队列）(偏移: 0x8)
- `object pathsClaimedSilentlyBy`（object pathsClaimedSilentlyBy）(偏移: 0xC)

### 方法 (2)

- `void Enqueue(Path path)`
  （void Enqueue（路径 path））
- `void ReturnPaths(bool timeSlice)`
  （void ReturnPaths（bool timeSlice））

---

## PathState（路径状态）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## PathType（路径类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## PathUtilities（路径Utilities）

### 字段 (1)

- `Queue<GraphNode> BFSQueue`（Queue<GraphNode> BFS队列）(偏移: 0x0)

### 方法 (10)

- `bool IsPathPossible(GraphNode node1, GraphNode node2)`
  （bool 是否路径Possible（Graph节点 node1, Graph节点 node2））
- `bool IsPathPossible(List<GraphNode> nodes)`
  （bool 是否路径Possible（List<GraphNode> nodes））
- `bool IsPathPossible(List<GraphNode> nodes, int tagMask)`
  （bool 是否路径Possible（List<GraphNode> nodes, int tagMask））
- `List<GraphNode> GetReachableNodes(GraphNode seed, int tagMask = -1, Func<GraphNode, bool> filter)`
  （List<GraphNode> 获取ReachableNodes（Graph节点 seed, int tagMask = -1, Func<Graph节点, bool> filter））
- `List<GraphNode> BFS(GraphNode seed, int depth, int tagMask = -1, Func<GraphNode, bool> filter)`
  （List<GraphNode> BFS（Graph节点 seed, int depth, int tagMask = -1, Func<Graph节点, bool> filter））
- `List<Vector3> GetSpiralPoints(int count, float clearance)`
  （List<Vector3> 获取SpiralPoints（int count, float clearance））
- `Vector3 InvoluteOfCircle(float a, float t)`
  （三维向量 InvoluteOfCircle（float a, float t））
- `void GetPointsAroundPointWorld(Vector3 p, IRaycastableGraph g, List<Vector3> previousPoints, float radius, float clearanceRadius)`
  （void 获取PointsAroundPoint世界的（三维向量 p, IRaycastableGraph g, List<Vector3> previousPoints, float radius, float clearanceRadius））
- `void GetPointsAroundPoint(Vector3 center, IRaycastableGraph g, List<Vector3> previousPoints, float radius, float clearanceRadius)`
  （void 获取PointsAroundPoint（三维向量 center, IRaycastableGraph g, List<Vector3> previousPoints, float radius, float clearanceRadius））
- `List<Vector3> GetPointsOnNodes(List<GraphNode> nodes, int count, float clearanceRadius = 0)`
  （List<Vector3> 获取PointsOnNodes（List<GraphNode> nodes, int count, float clearanceRadius = 0））

---

## Patrol（Patrol）

**继承**: VersionedMonoBehaviour（版本化MonoBehaviour）

### 字段 (5)

- `Transform[] targets`（Transform[] targets）(偏移: 0x10)
- `float delay`（浮点数 延迟）(偏移: 0x14)
- `int index`（整数 索引）(偏移: 0x18)
- `IAstarAI agent`（IAstarAI agent）(偏移: 0x1C)
- `float switchTime`（float switch时间）(偏移: 0x20)

### 方法 (2)

- `void Awake()`
  （void 唤醒（））
- `void Update()`
  （void 更新（））

---

## PenetrationAvoidance（PenetrationAvoidance）

**继承**: OffsetModifier（偏移修改器）

### 字段 (1)

- `PenetrationAvoidance.Avoider[] avoiders`（PenetrationAvoidance.Avoider[] avoiders）(偏移: 0x18)

### 方法 (1)

- `void OnModifyOffset()`
  （void 修改偏移时（））

---

## PenetrationAvoidance.Avoider（PenetrationAvoidance.Avoider）

### 字段 (10)

- `Transform[] raycastFrom`（Transform[] raycastFrom）(偏移: 0x8)
- `Transform raycastTo`（变换 raycastTo）(偏移: 0xC)
- `float raycastRadius`（float raycastRadius）(偏移: 0x10)
- `PenetrationAvoidance.Avoider.EffectorLink[] effectors`（PenetrationAvoidance.Avoider.EffectorLink[] effectors）(偏移: 0x14)
- `float smoothTimeIn`（float smooth时间In）(偏移: 0x18)
- `float smoothTimeOut`（float smooth时间Out）(偏移: 0x1C)
- `LayerMask layers`（层掩码 layers）(偏移: 0x20)
- `Vector3 offset`（三维向量 偏移）(偏移: 0x24)
- `Vector3 offsetTarget`（三维向量 offset目标）(偏移: 0x30)
- `Vector3 offsetV`（三维向量 offsetV）(偏移: 0x3C)

### 方法 (3)

- `void Solve(IKSolverFullBodyBiped solver, float weight)`
  （void Solve（IKSolver满身体Biped solver, float weight））
- `Vector3 GetOffsetTarget(IKSolverFullBodyBiped solver)`
  （三维向量 获取Offset目标（IKSolver满身体Biped solver））
- `Vector3 Raycast(Vector3 from, Vector3 to)`
  （三维向量 Raycast（三维向量 from, 三维向量 to））

---

## PenetrationAvoidance.Avoider.EffectorLink（PenetrationAvoidance.Avoider.EffectorLink）

### 字段 (2)

- `FullBodyBipedEffector effector`（全身双足效应器 effector）(偏移: 0x8)
- `float weight`（浮点数 权重）(偏移: 0xC)

---

## PerObjectData（Per对象数据）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## PerformDynamicRes（执行动态的Res）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `float Invoke()`
  （float Invoke（））
- `IAsyncResult BeginInvoke(AsyncCallback callback, object object)`
  （I异步结果 开始调用（异步回调 callback, 对象 object））
- `float EndInvoke(IAsyncResult result)`
  （浮点数 结束调用（I异步结果 result））

---

## PerformanceCountersElement（PerformanceCounters元素）

**继承**: ConfigurationElement（配置元素）

### 方法 (1)

- `ConfigurationPropertyCollection get_Properties()`
  （配置属性集合 获取_属性（））

---

## PersistentCall（持久的Call）

**继承**: ISerializationCallbackReceiver（ISerialization回调接收器）

### 字段 (6)

- `Object m_Target`（对象 m_目标）(偏移: 0x8)
- `string m_TargetAssemblyTypeName`（string m_目标Assembly类型名称）(偏移: 0xC)
- `string m_MethodName`（string m_Method名称）(偏移: 0x10)
- `PersistentListenerMode m_Mode`（持久的监听器模式 m_模式）(偏移: 0x14)
- `ArgumentCache m_Arguments`（Argument缓存 m_Arguments）(偏移: 0x18)
- `UnityEventCallState m_CallState`（Unity引擎事件Call状态 m_Call状态）(偏移: 0x1C)

### 方法 (10)

- `Object get_target()`
  （对象 get_target（））
- `string get_targetAssemblyTypeName()`
  （string get_targetAssembly类型名称（））
- `string get_methodName()`
  （string get_method名称（））
- `PersistentListenerMode get_mode()`
  （持久的监听器模式 get_mode（））
- `ArgumentCache get_arguments()`
  （Argument缓存 get_arguments（））
- `bool IsValid()`
  （布尔值 是否有效（））
- `BaseInvokableCall GetRuntimeCall(UnityEventBase theEvent)`
  （基础InvokableCall 获取RuntimeCall（Unity引擎事件基础 theEvent））
- `BaseInvokableCall GetObjectCall(Object target, MethodInfo method, ArgumentCache arguments)`
  （基础InvokableCall 获取对象Call（对象 target, Method信息 method, Argument缓存 arguments））
- `void OnBeforeSerialize()`
  （void 序列化前（））
- `void OnAfterDeserialize()`
  （void 反序列化后（））

---

## PersistentCallGroup（持久的Call组）

### 字段 (1)

- `List<PersistentCall> m_Calls`（List<持久的Call> m_Calls）(偏移: 0x8)

### 方法 (1)

- `void Initialize(InvokableCallList invokableList, UnityEventBase unityEventBase)`
  （void 初始化（InvokableCall列表 invokableList, Unity引擎事件基础 unityEventBase））

---

## PersistentListenerMode（持久的监听器模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## PhotoCapture（PhotoCapture）

**继承**: IDisposable（可释放接口）

### 字段 (2)

- `IntPtr m_NativePtr`（整数Ptr m_NativePtr）(偏移: 0x8)
- `long HR_SUCCESS`（long HR_SUCCESS）(偏移: 0x0)

### 方法 (10)

- `PhotoCapture.PhotoCaptureResult MakeCaptureResult(long hResult)`
  （PhotoCapture.PhotoCaptureResult MakeCaptureResult（long hResult））
- `void InvokeOnCreatedResourceDelegate(PhotoCapture.OnCaptureResourceCreatedCallback callback, IntPtr nativePtr)`
  （void InvokeOnCreated资源委托（PhotoCapture.OnCapture资源Created回调 callback, 整数Ptr nativePtr））
- `void InvokeOnPhotoModeStartedDelegate(PhotoCapture.OnPhotoModeStartedCallback callback, long hResult)`
  （void InvokeOnPhoto模式Started委托（PhotoCapture.OnPhoto模式Started回调 callback, long hResult））
- `void InvokeOnPhotoModeStoppedDelegate(PhotoCapture.OnPhotoModeStoppedCallback callback, long hResult)`
  （void InvokeOnPhoto模式Stopped委托（PhotoCapture.OnPhoto模式Stopped回调 callback, long hResult））
- `void InvokeOnCapturedPhotoToDiskDelegate(PhotoCapture.OnCapturedToDiskCallback callback, long hResult)`
  （void InvokeOnCapturedPhotoToDisk委托（PhotoCapture.OnCapturedToDisk回调 callback, long hResult））
- `void InvokeOnCapturedPhotoToMemoryDelegate(PhotoCapture.OnCapturedToMemoryCallback callback, long hResult, IntPtr photoCaptureFramePtr)`
  （void InvokeOnCapturedPhotoToMemory委托（PhotoCapture.OnCapturedToMemory回调 callback, long hResult, 整数Ptr photoCaptureFramePtr））
- `void Dispose()`
  （void 释放（））
- `void Dispose_Internal()`
  （void Dispose_内部的（））
- `void Finalize()`
  （void 终结（））
- `void DisposeThreaded_Internal()`
  （void 释放Threaded_内部的（））

---

## PhotoCapture.CaptureResultType（PhotoCapture.CaptureResult类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## PhotoCapture.OnCaptureResourceCreatedCallback（PhotoCapture.OnCapture资源Created回调）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(PhotoCapture captureObject)`
  （void Invoke（PhotoCapture captureObject））
- `IAsyncResult BeginInvoke(PhotoCapture captureObject, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（PhotoCapture captureObject, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## PhotoCapture.OnCapturedToDiskCallback（PhotoCapture.OnCapturedToDisk回调）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(PhotoCapture.PhotoCaptureResult result)`
  （void Invoke（PhotoCapture.PhotoCaptureResult result））
- `IAsyncResult BeginInvoke(PhotoCapture.PhotoCaptureResult result, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（PhotoCapture.PhotoCaptureResult result, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

