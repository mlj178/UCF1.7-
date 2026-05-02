# 游戏类定义 (Part 11/21)

共 200 个类 (总序号 2001 - 2200)

---

## MaterialEffectPlayable（材质特效Playable）

**继承**: IPlayable, IEquatable<MaterialEffectPlayable>（IPlayable, IEquatable<材质特效Playable>）

### 字段 (1)

- `PlayableHandle m_Handle`（Playable句柄 m_句柄）(偏移: 0x0)

### 方法 (2)

- `PlayableHandle GetHandle()`
  （Playable句柄 获取句柄（））
- `bool Equals(MaterialEffectPlayable other)`
  （bool Equals（材质特效Playable other））

---

## MaterialEntry（材质Entry）

### 字段 (2)

- `Material material`（材质 material）(偏移: 0x8)
- `int referenceCount`（int reference数量）(偏移: 0xC)

### 方法 (1)

- `void Release()`
  （void Release（））

---

## MaterialExpand（材质Expand）

### 方法 (10)

- `void SetBlendMode(Material mat, int RGBSrc, int RGBDst, int AlphaSrc, int AlphaDst)`
  （void 集合Blend模式（材质 mat, int RGBSrc, int RGBDst, int AlphaSrc, int AlphaDst））
- `void SetOpaque_MyMat(Material mat)`
  （void 集合Opaque_My材质（材质 mat））
- `void SetTransparent_MyMat(Material mat)`
  （void 集合Transparent_My材质（材质 mat））
- `void SetAdditive_MyMat(Material mat)`
  （void 集合Additive_My材质（材质 mat））
- `void SetOpaque_URP(Material mat)`
  （void 集合Opaque_URP（材质 mat））
- `void SetTransparent_URP(Material mat)`
  （void 集合Transparent_URP（材质 mat））
- `void SetOpaque(Material mat)`
  （void 集合不透明的（材质 mat））
- `void SetTransparent(Material mat)`
  （void 集合透明的（材质 mat））
- `void SetAdditive(Material mat)`
  （void 集合Additive（材质 mat））
- `void SetBaseColor(Material mat, Color color)`
  （void 集合基础颜色（材质 mat, 颜色 color））

---

## MaterialPropertyBlock（材质属性Block）

### 字段 (1)

- `IntPtr m_Ptr`（整数Ptr m_Ptr）(偏移: 0x8)

### 方法 (14)

- `void SetFloatImpl(int name, float value)`
  （void 集合浮点数Impl（int name, float value））
- `void SetVectorImpl(int name, Vector4 value)`
  （void 集合向量Impl（int name, Vector4 value））
- `void SetTextureImpl(int name, Texture value)`
  （void 集合纹理Impl（int name, 纹理 value））
- `IntPtr CreateImpl()`
  （整数Ptr 创建Impl（））
- `void DestroyImpl(IntPtr mpb)`
  （void 销毁Impl（整数Ptr mpb））
- `void Clear(bool keepMemory)`
  （void 清除（bool keepMemory））
- `void Clear()`
  （void 清除（））
- `void Finalize()`
  （void Finalize（））
- `void Dispose()`
  （void 释放（））
- `void SetFloat(int nameID, float value)`
  （void 集合浮点数（int nameID, float value））
- `void SetInt(int nameID, int value)`
  （void 集合整数（int nameID, int value））
- `void SetVector(int nameID, Vector4 value)`
  （void 集合向量（int nameID, Vector4 value））
- `void SetTexture(int nameID, Texture value)`
  （void 集合纹理（int nameID, 纹理 value））
- `void SetVectorImpl_Injected(int name, ref Vector4 value)`
  （void 集合向量Impl_Injected（int name, ref Vector4 value））

---

## MaterialQuality（材质Quality）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## MaterialQualityUtilities（材质QualityUtilities）

### 字段 (3)

- `string[] KeywordNames`（string[] KeywordNames）(偏移: 0x0)
- `string[] EnumNames`（string[] EnumNames）(偏移: 0x4)
- `ShaderKeyword[] Keywords`（着色器Keyword[] Keywords）(偏移: 0x8)

### 方法 (6)

- `MaterialQuality GetHighestQuality(MaterialQuality levels)`
  （材质Quality 获取HighestQuality（材质Quality levels））
- `MaterialQuality GetClosestQuality(MaterialQuality availableLevels, MaterialQuality requestedLevel)`
  （材质Quality 获取ClosestQuality（材质Quality availableLevels, 材质Quality requestedLevel））
- `void SetGlobalShaderKeywords(MaterialQuality level)`
  （void 集合全局的着色器Keywords（材质Quality level））
- `void SetGlobalShaderKeywords(MaterialQuality level, CommandBuffer cmd)`
  （void 集合全局的着色器Keywords（材质Quality level, Command缓冲区 cmd））
- `int ToFirstIndex(MaterialQuality level)`
  （int To第一个索引（材质Quality level））
- `MaterialQuality FromIndex(int index)`
  （材质Quality From索引（int index））

---

## Math（数学）

### 字段 (2)

- `double doubleRoundLimit`（double double回合Limit）(偏移: 0x0)
- `double[] roundPower10Double`（double[] roundPower10Double）(偏移: 0x8)

### 方法 (37)

- `double Acos(double d)`
  （double Acos（double d））
- `double Asin(double d)`
  （double Asin（double d））
- `double Atan(double d)`
  （double Atan（double d））
- `double Atan2(double y, double x)`
  （double Atan2（double y, double x））
- `double Ceiling(double a)`
  （double Ceiling（double a））
- `double Cos(double d)`
  （double Cos（double d））
- `double Floor(double d)`
  （double Floor（double d））
- `double InternalTruncate(double d)`
  （double 内部的Truncate（double d））
- `double Sin(double a)`
  （double Sin（double a））
- `double Tan(double a)`
  （double Tan（double a））
- `double Round(double a)`
  （double 回合（double a））
- `double SplitFractionDouble(double* value)`
  （double SplitFractionDouble（double* value））
- `double Truncate(double d)`
  （double Truncate（double d））
- `double Sqrt(double d)`
  （double Sqrt（double d））
- `double Log(double d)`
  （double Log（double d））
- `double Exp(double d)`
  （double Exp（double d））
- `double Pow(double x, double y)`
  （double Pow（double x, double y））
- `int Abs(int value)`
  （int Abs（int value））
- `int AbsHelper(int value)`
  （int Abs辅助器（int value））
- `long Abs(long value)`
  （long Abs（long value））
- `long AbsHelper(long value)`
  （long Abs辅助器（long value））
- `float Abs(float value)`
  （float Abs（float value））
- `double Abs(double value)`
  （double Abs（double value））
- `byte Max(byte val1, byte val2)`
  （byte 最大（byte val1, byte val2））
- `ushort Max(ushort val1, ushort val2)`
  （ushort 最大（ushort val1, ushort val2））
- `int Max(int val1, int val2)`
  （int 最大（int val1, int val2））
- `uint Max(uint val1, uint val2)`
  （uint 最大（uint val1, uint val2））
- `long Max(long val1, long val2)`
  （long 最大（long val1, long val2））
- `float Max(float val1, float val2)`
  （float 最大（float val1, float val2））
- `double Max(double val1, double val2)`
  （double 最大（double val1, double val2））
- `int Min(int val1, int val2)`
  （int 最小（int val1, int val2））
- `uint Min(uint val1, uint val2)`
  （uint 最小（uint val1, uint val2））
- `long Min(long val1, long val2)`
  （long 最小（long val1, long val2））
- `float Min(float val1, float val2)`
  （float 最小（float val1, float val2））
- `double Min(double val1, double val2)`
  （double 最小（double val1, double val2））
- `double Log(double a, double newBase)`
  （double Log（double a, double newBase））
- `int Sign(int value)`
  （int 标志（int value））

---

## Mathf（Mathf）

### 字段 (1)

- `float Epsilon`（float Epsilon）(偏移: 0x0)

### 方法 (44)

- `int ClosestPowerOfTwo(int value)`
  （int Closest力度OfTwo（int value））
- `int NextPowerOfTwo(int value)`
  （int 下一个力度OfTwo（int value））
- `float GammaToLinearSpace(float value)`
  （float GammaToLinearSpace（float value））
- `float LinearToGammaSpace(float value)`
  （float LinearToGammaSpace（float value））
- `ushort FloatToHalf(float val)`
  （ushort 浮点数ToHalf（float val））
- `float PerlinNoise(float x, float y)`
  （float PerlinNoise（float x, float y））
- `float Sin(float f)`
  （float Sin（float f））
- `float Cos(float f)`
  （float Cos（float f））
- `float Tan(float f)`
  （float Tan（float f））
- `float Asin(float f)`
  （float Asin（float f））
- `float Acos(float f)`
  （float Acos（float f））
- `float Atan(float f)`
  （float Atan（float f））
- `float Atan2(float y, float x)`
  （float Atan2（float y, float x））
- `float Sqrt(float f)`
  （float Sqrt（float f））
- `float Abs(float f)`
  （float Abs（float f））
- `int Abs(int value)`
  （int Abs（int value））
- `float Min(float a, float b)`
  （float 最小（float a, float b））
- `int Min(int a, int b)`
  （int 最小（int a, int b））
- `float Max(float a, float b)`
  （float 最大（float a, float b））
- `int Max(int a, int b)`
  （int 最大（int a, int b））
- `float Pow(float f, float p)`
  （float Pow（float f, float p））
- `float Exp(float power)`
  （float Exp（float power））
- `float Log(float f, float p)`
  （float Log（float f, float p））
- `float Log(float f)`
  （float Log（float f））
- `float Ceil(float f)`
  （float Ceil（float f））
- `float Floor(float f)`
  （float Floor（float f））
- `float Round(float f)`
  （float 回合（float f））
- `int CeilToInt(float f)`
  （int CeilTo整数（float f））
- `int FloorToInt(float f)`
  （int FloorTo整数（float f））
- `int RoundToInt(float f)`
  （int 回合To整数（float f））
- `float Sign(float f)`
  （float 标志（float f））
- `float Clamp(float value, float min, float max)`
  （float Clamp（float value, float min, float max））
- `int Clamp(int value, int min, int max)`
  （int Clamp（int value, int min, int max））
- `float Clamp01(float value)`
  （float Clamp01（float value））
- `float Lerp(float a, float b, float t)`
  （float Lerp（float a, float b, float t））
- `float LerpAngle(float a, float b, float t)`
  （float Lerp角度（float a, float b, float t））
- `float MoveTowards(float current, float target, float maxDelta)`
  （float 移动Towards（float current, float target, float maxDelta））
- `float MoveTowardsAngle(float current, float target, float maxDelta)`
  （float 移动Towards角度（float current, float target, float maxDelta））
- `bool Approximately(float a, float b)`
  （bool Approximately（float a, float b））
- `float SmoothDamp(float current, float target, ref float currentVelocity, float smoothTime)`
  （float SmoothDamp（float current, float target, ref float currentVelocity, float smoothTime））
- `float SmoothDamp(float current, float target, ref float currentVelocity, float smoothTime, float maxSpeed, float deltaTime)`
  （float SmoothDamp（float current, float target, ref float currentVelocity, float smoothTime, float maxSpeed, float deltaTime））
- `float Repeat(float t, float length)`
  （float Repeat（float t, float length））
- `float InverseLerp(float a, float b, float value)`
  （float InverseLerp（float a, float b, float value））
- `float DeltaAngle(float current, float target)`
  （float Delta角度（float current, float target））

---

## MathfInternal（Mathf内部的）

### 字段 (3)

- `float FloatMinNormal`（float 浮点数最小法线）(偏移: 0x0)
- `float FloatMinDenormal`（float 浮点数最小Denormal）(偏移: 0x4)
- `bool IsFlushToZeroEnabled`（bool 是否FlushToZero启用的）(偏移: 0x8)

---

## Matrix4x4（Matrix4x4）

**继承**: IEquatable<Matrix4x4>, IFormattable（IEquatable<Matrix4x4>, IFormattable）

### 字段 (18)

- `float m00`（float m00）(偏移: 0x0)
- `float m10`（float m10）(偏移: 0x4)
- `float m20`（float m20）(偏移: 0x8)
- `float m30`（float m30）(偏移: 0xC)
- `float m01`（float m01）(偏移: 0x10)
- `float m11`（float m11）(偏移: 0x14)
- `float m21`（float m21）(偏移: 0x18)
- `float m31`（float m31）(偏移: 0x1C)
- `float m02`（float m02）(偏移: 0x20)
- `float m12`（float m12）(偏移: 0x24)
- `float m22`（float m22）(偏移: 0x28)
- `float m32`（float m32）(偏移: 0x2C)
- `float m03`（float m03）(偏移: 0x30)
- `float m13`（float m13）(偏移: 0x34)
- `float m23`（float m23）(偏移: 0x38)
- `float m33`（float m33）(偏移: 0x3C)
- `Matrix4x4 zeroMatrix`（Matrix4x4 zero矩阵）(偏移: 0x0)
- `Matrix4x4 identityMatrix`（Matrix4x4 identity矩阵）(偏移: 0x40)

### 方法 (34)

- `bool IsIdentity()`
  （bool 是否Identity（））
- `FrustumPlanes DecomposeProjection()`
  （FrustumPlanes DecomposeProjection（））
- `bool get_isIdentity()`
  （bool get_isIdentity（））
- `FrustumPlanes get_decomposeProjection()`
  （FrustumPlanes get_decomposeProjection（））
- `Matrix4x4 TRS(Vector3 pos, Quaternion q, Vector3 s)`
  （Matrix4x4 TRS（三维向量 pos, Quaternion q, 三维向量 s））
- `Matrix4x4 Inverse(Matrix4x4 m)`
  （Matrix4x4 Inverse（Matrix4x4 m））
- `Matrix4x4 get_inverse()`
  （Matrix4x4 get_inverse（））
- `Matrix4x4 Perspective(float fov, float aspect, float zNear, float zFar)`
  （Matrix4x4 Perspective（float fov, float aspect, float zNear, float zFar））
- `void set_Item(int row, int column, float value)`
  （void set_项目（int row, int column, float value））
- `void set_Item(int index, float value)`
  （void set_项目（int index, float value））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool Equals(object other)`
  （bool Equals（object other））
- `bool Equals(Matrix4x4 other)`
  （bool Equals（Matrix4x4 other））
- `Matrix4x4 op_Multiply(Matrix4x4 lhs, Matrix4x4 rhs)`
  （Matrix4x4 op_Multiply（Matrix4x4 lhs, Matrix4x4 rhs））
- `bool op_Equality(Matrix4x4 lhs, Matrix4x4 rhs)`
  （bool op_Equality（Matrix4x4 lhs, Matrix4x4 rhs））
- `bool op_Inequality(Matrix4x4 lhs, Matrix4x4 rhs)`
  （bool op_Inequality（Matrix4x4 lhs, Matrix4x4 rhs））
- `Vector4 GetColumn(int index)`
  （Vector4 获取Column（int index））
- `Vector4 GetRow(int index)`
  （Vector4 获取Row（int index））
- `void SetColumn(int index, Vector4 column)`
  （void 集合Column（int index, Vector4 column））
- `Vector3 MultiplyPoint(Vector3 point)`
  （三维向量 MultiplyPoint（三维向量 point））
- `Vector3 MultiplyPoint3x4(Vector3 point)`
  （三维向量 MultiplyPoint3x4（三维向量 point））
- `Vector3 MultiplyVector(Vector3 vector)`
  （三维向量 Multiply向量（三维向量 vector））
- `Matrix4x4 Scale(Vector3 vector)`
  （Matrix4x4 缩放（三维向量 vector））
- `Matrix4x4 Translate(Vector3 vector)`
  （Matrix4x4 Translate（三维向量 vector））
- `Matrix4x4 Rotate(Quaternion q)`
  （Matrix4x4 Rotate（Quaternion q））
- `Matrix4x4 get_zero()`
  （Matrix4x4 get_zero（））
- `Matrix4x4 get_identity()`
  （Matrix4x4 get_identity（））
- `string ToString()`
  （string To字符串（））
- `string ToString(string format, IFormatProvider formatProvider)`
  （string To字符串（string format, I格式化提供者 formatProvider））
- `bool IsIdentity_Injected(ref Matrix4x4 _unity_self)`
  （bool 是否Identity_Injected（ref Matrix4x4 _unity_self））
- `void DecomposeProjection_Injected(ref Matrix4x4 _unity_self, out FrustumPlanes ret)`
  （void DecomposeProjection_Injected（ref Matrix4x4 _unity_self, out FrustumPlanes ret））
- `void TRS_Injected(ref Vector3 pos, ref Quaternion q, ref Vector3 s, out Matrix4x4 ret)`
  （void TRS_Injected（ref Vector3 pos, ref Quaternion q, ref Vector3 s, out Matrix4x4 ret））
- `void Inverse_Injected(ref Matrix4x4 m, out Matrix4x4 ret)`
  （void Inverse_Injected（ref Matrix4x4 m, out Matrix4x4 ret））
- `void Perspective_Injected(float fov, float aspect, float zNear, float zFar, out Matrix4x4 ret)`
  （void Perspective_Injected（float fov, float aspect, float zNear, float zFar, out Matrix4x4 ret））

---

## MaxFloatParameter（最大浮点数Parameter）

**继承**: FloatParameter（浮点数Parameter）

### 字段 (1)

- `float max`（float max）(偏移: 0x10)

### 方法 (2)

- `float get_value()`
  （float get_value（））
- `void set_value(float value)`
  （void set_value（float value））

---

## MaxIntParameter（最大整数Parameter）

**继承**: IntParameter（整数Parameter）

### 字段 (1)

- `int max`（int max）(偏移: 0x10)

### 方法 (2)

- `int get_value()`
  （int get_value（））
- `void set_value(int value)`
  （void set_value（int value））

---

## MeasureFunction（MeasureFunction）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `YogaSize Invoke(YogaNode node, float width, YogaMeasureMode widthMode, float height, YogaMeasureMode heightMode)`
  （Yoga大小 Invoke（Yoga节点 node, float width, YogaMeasure模式 widthMode, float height, YogaMeasure模式 heightMode））
- `IAsyncResult BeginInvoke(YogaNode node, float width, YogaMeasureMode widthMode, float height, YogaMeasureMode heightMode, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Yoga节点 node, float width, YogaMeasure模式 widthMode, float height, YogaMeasure模式 heightMode, 异步回调 callback, object object））
- `YogaSize EndInvoke(IAsyncResult result)`
  （Yoga大小 结束Invoke（I异步Result result））

---

## MecanimBridge（MecanimBridge）

**继承**: VersionedMonoBehaviour（VersionedMonoBehaviour）

### 字段 (7)

- `float velocitySmoothing`（float velocitySmoothing）(偏移: 0x10)
- `IAstarAI ai`（IAstarAI ai）(偏移: 0x14)
- `Animator anim`（动画器 anim）(偏移: 0x18)
- `Transform tr`（变换 tr）(偏移: 0x1C)
- `Vector3 smoothedVelocity`（三维向量 smoothed速度）(偏移: 0x20)
- `Vector3[] prevFootPos`（Vector3[] prev脚部Pos）(偏移: 0x2C)
- `Transform[] footTransforms`（Transform[] footTransforms）(偏移: 0x30)

### 方法 (6)

- `void Awake()`
  （void Awake（））
- `void Update()`
  （void 更新（））
- `Vector3 CalculateBlendPoint()`
  （三维向量 计算BlendPoint（））
- `void OnAnimatorMove()`
  （void On动画器移动（））
- `Vector3 RotatePointAround(Vector3 point, Vector3 around, Quaternion rotation)`
  （三维向量 RotatePointAround（三维向量 point, 三维向量 around, Quaternion rotation））
- `Quaternion RotateTowards(Vector3 direction, float maxDegrees)`
  （Quaternion RotateTowards（三维向量 direction, float maxDegrees））

---

## MechanicHero（Mechanic英雄）

**继承**: BotActionBase（机器人动作基础）

### 字段 (1)

- `float stopUseKnifeTime`（float stopUse近战武器时间）(偏移: 0x10)

### 方法 (5)

- `void Bot_Getter_WeaponSlot(ref int slot, ref int priority)`
  （void Bot_Getter_Weapon槽位（ref int slot, ref int priority））
- `void Update()`
  （void 更新（））
- `bool CanDo()`
  （bool 能否Do（））
- `void DoAction()`
  （void Do动作（））
- `void OnActionFinish()`
  （void On动作Finish（））

---

## MemberDescriptor（MemberDescriptor）

### 字段 (12)

- `string name`（string name）(偏移: 0x8)
- `string displayName`（string display名称）(偏移: 0xC)
- `int nameHash`（int nameHash）(偏移: 0x10)
- `AttributeCollection attributeCollection`（AttributeCollection attributeCollection）(偏移: 0x14)
- `Attribute[] attributes`（Attribute[] attributes）(偏移: 0x18)
- `Attribute[] originalAttributes`（Attribute[] originalAttributes）(偏移: 0x1C)
- `bool attributesFiltered`（bool attributesFiltered）(偏移: 0x20)
- `bool attributesFilled`（bool attributesFilled）(偏移: 0x21)
- `int metadataVersion`（int metadataVersion）(偏移: 0x24)
- `string category`（string category）(偏移: 0x28)
- `string description`（string description）(偏移: 0x2C)
- `object lockCookie`（object lockCookie）(偏移: 0x30)

### 方法 (15)

- `Attribute[] get_AttributeArray()`
  （Attribute[] get_Attribute数组（））
- `void set_AttributeArray(Attribute[] value)`
  （void set_Attribute数组（Attribute[] value））
- `AttributeCollection get_Attributes()`
  （AttributeCollection get_Attributes（））
- `string get_Name()`
  （string get_名称（））
- `int get_NameHashCode()`
  （int get_名称HashCode（））
- `string get_DisplayName()`
  （string get_Display名称（））
- `void CheckAttributesValid()`
  （void 检查AttributesValid（））
- `AttributeCollection CreateAttributeCollection()`
  （AttributeCollection 创建AttributeCollection（））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `void FillAttributes(IList attributeList)`
  （void FillAttributes（I列表 attributeList））
- `void FilterAttributesIfNeeded()`
  （void FilterAttributesIfNeeded（））
- `MethodInfo FindMethod(Type componentClass, string name, Type[] args, Type returnType)`
  （Method信息 查找Method（类型 componentClass, string name, Type[] args, 类型 returnType））
- `MethodInfo FindMethod(Type componentClass, string name, Type[] args, Type returnType, bool publicOnly)`
  （Method信息 查找Method（类型 componentClass, string name, Type[] args, 类型 returnType, bool publicOnly））
- `int GetHashCode()`
  （int 获取HashCode（））
- `ISite GetSite(object component)`
  （ISite 获取Site（object component））

---

## MemberFilter（MemberFilter）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `bool Invoke(MemberInfo m, object filterCriteria)`
  （bool Invoke（Member信息 m, object filterCriteria））
- `IAsyncResult BeginInvoke(MemberInfo m, object filterCriteria, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Member信息 m, object filterCriteria, 异步回调 callback, object object））
- `bool EndInvoke(IAsyncResult result)`
  （bool 结束Invoke（I异步Result result））

---

## MemberHolder（MemberHolder）

### 字段 (2)

- `Type memberType`（类型 member类型）(偏移: 0x8)
- `StreamingContext context`（StreamingContext context）(偏移: 0xC)

### 方法 (2)

- `int GetHashCode()`
  （int 获取HashCode（））
- `bool Equals(object obj)`
  （bool Equals（object obj））

---

## MemberInfo（Member信息）

**继承**: ICustomAttributeProvider, _MemberInfo（I自定义的Attribute提供者, _Member信息）

### 方法 (7)

- `IList<CustomAttributeData> GetCustomAttributesData()`
  （IList<自定义的AttributeData> 获取自定义的Attributes数据（））
- `int get_MetadataToken()`
  （int get_Metadata令牌（））
- `Module get_Module()`
  （模块 get_模块（））
- `bool op_Equality(MemberInfo left, MemberInfo right)`
  （bool op_Equality（Member信息 left, Member信息 right））
- `bool op_Inequality(MemberInfo left, MemberInfo right)`
  （bool op_Inequality（Member信息 left, Member信息 right））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## MemberInfoSerializationHolder（Member信息SerializationHolder）

**继承**: ISerializable, IObjectReference（ISerializable, I对象引用）

### 字段 (6)

- `string m_memberName`（string m_member名称）(偏移: 0x8)
- `RuntimeType m_reflectedType`（Runtime类型 m_reflected类型）(偏移: 0xC)
- `string m_signature`（string m_signature）(偏移: 0x10)
- `string m_signature2`（string m_signature2）(偏移: 0x14)
- `MemberTypes m_memberType`（MemberTypes m_member类型）(偏移: 0x18)
- `SerializationInfo m_info`（Serialization信息 m_info）(偏移: 0x1C)

### 方法 (4)

- `void GetSerializationInfo(SerializationInfo info, string name, RuntimeType reflectedClass, string signature, MemberTypes type)`
  （void 获取Serialization信息（Serialization信息 info, string name, Runtime类型 reflectedClass, string signature, MemberTypes type））
- `void GetSerializationInfo(SerializationInfo info, string name, RuntimeType reflectedClass, string signature, string signature2, MemberTypes type, Type[] genericArguments)`
  （void 获取Serialization信息（Serialization信息 info, string name, Runtime类型 reflectedClass, string signature, string signature2, MemberTypes type, Type[] genericArguments））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））
- `object GetRealObject(StreamingContext context)`
  （object 获取Real对象（StreamingContext context））

---

## MemberPrimitiveTyped（MemberPrimitiveTyped）

### 字段 (2)

- `InternalPrimitiveTypeE primitiveTypeEnum`（内部的Primitive类型E primitive类型Enum）(偏移: 0x8)
- `object value`（object value）(偏移: 0xC)

### 方法 (4)

- `void Set(InternalPrimitiveTypeE primitiveTypeEnum, object value)`
  （void 集合（内部的Primitive类型E primitiveTypeEnum, object value））
- `void Write(__BinaryWriter sout)`
  （void Write（__Binary写入器 sout））
- `void Read(__BinaryParser input)`
  （void Read（__BinaryParser input））
- `void Dump()`
  （void Dump（））

---

## MemberPrimitiveUnTyped（MemberPrimitiveUnTyped）

### 字段 (2)

- `InternalPrimitiveTypeE typeInformation`（内部的Primitive类型E typeInformation）(偏移: 0x8)
- `object value`（object value）(偏移: 0xC)

### 方法 (5)

- `void Set(InternalPrimitiveTypeE typeInformation, object value)`
  （void 集合（内部的Primitive类型E typeInformation, object value））
- `void Set(InternalPrimitiveTypeE typeInformation)`
  （void 集合（内部的Primitive类型E typeInformation））
- `void Write(__BinaryWriter sout)`
  （void Write（__Binary写入器 sout））
- `void Read(__BinaryParser input)`
  （void Read（__BinaryParser input））
- `void Dump()`
  （void Dump（））

---

## MemberReference（Member引用）

### 字段 (1)

- `int idRef`（int idRef）(偏移: 0x8)

### 方法 (4)

- `void Set(int idRef)`
  （void 集合（int idRef））
- `void Write(__BinaryWriter sout)`
  （void Write（__Binary写入器 sout））
- `void Read(__BinaryParser input)`
  （void Read（__BinaryParser input））
- `void Dump()`
  （void Dump（））

---

## MemberTypes（MemberTypes）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## MemoryProfiler（MemoryProfiler）

### 字段 (1)

- `Action<MetaData> createMetaData`（Action<MetaData> createMeta数据）(偏移: 0x8)

### 方法 (5)

- `byte[] PrepareMetadata()`
  （byte[] PrepareMetadata（））
- `int WriteIntToByteArray(byte[] array, int offset, int value)`
  （int Write整数ToByte数组（byte[] array, int offset, int value））
- `int WriteStringToByteArray(byte[] array, int offset, string value)`
  （int Write字符串ToByte数组（byte[] array, int offset, string value））
- `void FinalizeSnapshot(string path, bool result)`
  （void FinalizeSnapshot（string path, bool result））
- `void SaveScreenshotToDisk(string path, bool result, IntPtr pixelsPtr, int pixelsCount, TextureFormat format, int width, int height)`
  （void 保存ScreenshotToDisk（string path, bool result, 整数Ptr pixelsPtr, int pixelsCount, 纹理格式化 format, int width, int height））

---

## MemoryStream（Memory流）

**继承**: Stream（流）

### 字段 (10)

- `byte[] _buffer`（byte[] _buffer）(偏移: 0x14)
- `int _origin`（int _origin）(偏移: 0x18)
- `int _position`（int _position）(偏移: 0x1C)
- `int _length`（int _length）(偏移: 0x20)
- `int _capacity`（int _capacity）(偏移: 0x24)
- `bool _expandable`（bool _expandable）(偏移: 0x28)
- `bool _writable`（bool _writable）(偏移: 0x0)
- `bool _exposable`（bool _exposable）(偏移: 0x0)
- `bool _isOpen`（bool _is打开）(偏移: 0x0)
- `Task<int> _lastReadTask`（Task<int> _lastReadTask）(偏移: 0x0)

### 方法 (24)

- `bool get_CanRead()`
  （bool get_能否Read（））
- `bool get_CanSeek()`
  （bool get_能否Seek（））
- `bool get_CanWrite()`
  （bool get_能否Write（））
- `void EnsureWriteable()`
  （void EnsureWriteable（））
- `void Dispose(bool disposing)`
  （void 释放（bool disposing））
- `bool EnsureCapacity(int value)`
  （bool EnsureCapacity（int value））
- `void Flush()`
  （void Flush（））
- `byte[] GetBuffer()`
  （byte[] 获取缓冲区（））
- `byte[] InternalGetBuffer()`
  （byte[] 内部的获取缓冲区（））
- `int InternalGetPosition()`
  （int 内部的获取Position（））
- `int InternalReadInt32()`
  （int 内部的ReadInt32（））
- `int InternalEmulateRead(int count)`
  （int 内部的EmulateRead（int count））
- `int get_Capacity()`
  （int get_Capacity（））
- `void set_Capacity(int value)`
  （void set_Capacity（int value））
- `long get_Length()`
  （long get_Length（））
- `long get_Position()`
  （long get_Position（））
- `void set_Position(long value)`
  （void set_Position（long value））
- `int Read([In] [Out] byte[] buffer, int offset, int count)`
  （int Read（[In] [Out] byte[] buffer, int offset, int count））
- `int ReadByte()`
  （int ReadByte（））
- `long Seek(long offset, SeekOrigin loc)`
  （long Seek（long offset, SeekOrigin loc））
- `void SetLength(long value)`
  （void 集合Length（long value））
- `byte[] ToArray()`
  （byte[] To数组（））
- `void Write(byte[] buffer, int offset, int count)`
  （void Write（byte[] buffer, int offset, int count））
- `void WriteByte(byte value)`
  （void WriteByte（byte value））

---

## Mesh（网格）

**继承**: Object（对象）

### 方法 (86)

- `void Internal_Create(Mesh mono)`
  （void Internal_创建（网格 mono））
- `void set_indexFormat(IndexFormat value)`
  （void set_index格式化（索引格式化 value））
- `void SetVertexBufferParamsFromArray(int vertexCount, VertexAttributeDescriptor[] attributes)`
  （void 集合Vertex缓冲区ParamsFrom数组（int vertexCount, VertexAttributeDescriptor[] attributes））
- `void InternalSetVertexBufferData(int stream, IntPtr data, int dataStart, int meshBufferStart, int count, int elemSize, MeshUpdateFlags flags)`
  （void 内部的集合Vertex缓冲区数据（int stream, 整数Ptr data, int dataStart, int meshBufferStart, int count, int elemSize, 网格更新Flags flags））
- `int GetVertexAttributeCountImpl()`
  （int 获取VertexAttribute数量Impl（））
- `VertexAttributeDescriptor GetVertexAttribute(int index)`
  （VertexAttributeDescriptor 获取VertexAttribute（int index））
- `uint GetIndexCountImpl(int submesh)`
  （uint 获取索引数量Impl（int submesh））
- `int[] GetTrianglesImpl(int submesh, bool applyBaseVertex)`
  （int[] 获取TrianglesImpl（int submesh, bool applyBaseVertex））
- `int[] GetIndicesImpl(int submesh, bool applyBaseVertex)`
  （int[] 获取IndicesImpl（int submesh, bool applyBaseVertex））
- `void SetIndicesImpl(int submesh, MeshTopology topology, IndexFormat indicesFormat, Array indices, int arrayStart, int arraySize, bool calculateBounds, int baseVertex)`
  （void 集合IndicesImpl（int submesh, 网格Topology topology, 索引格式化 indicesFormat, 数组 indices, int arrayStart, int arraySize, bool calculateBounds, int baseVertex））
- `void SetIndicesNativeArrayImpl(int submesh, MeshTopology topology, IndexFormat indicesFormat, IntPtr indices, int arrayStart, int arraySize, bool calculateBounds, int baseVertex)`
  （void 集合IndicesNative数组Impl（int submesh, 网格Topology topology, 索引格式化 indicesFormat, 整数Ptr indices, int arrayStart, int arraySize, bool calculateBounds, int baseVertex））
- `void PrintErrorCantAccessChannel(VertexAttribute ch)`
  （void PrintErrorCantAccessChannel（VertexAttribute ch））
- `bool HasVertexAttribute(VertexAttribute attr)`
  （bool 是否有VertexAttribute（VertexAttribute attr））
- `void SetArrayForChannelImpl(VertexAttribute channel, VertexAttributeFormat format, int dim, Array values, int arraySize, int valuesStart, int valuesCount, MeshUpdateFlags flags)`
  （void 集合数组ForChannelImpl（VertexAttribute channel, VertexAttribute格式化 format, int dim, 数组 values, int arraySize, int valuesStart, int valuesCount, 网格更新Flags flags））
- `Array GetAllocArrayFromChannelImpl(VertexAttribute channel, VertexAttributeFormat format, int dim)`
  （数组 获取Alloc数组FromChannelImpl（VertexAttribute channel, VertexAttribute格式化 format, int dim））
- `void GetArrayFromChannelImpl(VertexAttribute channel, VertexAttributeFormat format, int dim, Array values)`
  （void 获取数组FromChannelImpl（VertexAttribute channel, VertexAttribute格式化 format, int dim, 数组 values））
- `bool IsCloudResource()`
  （bool 是否Cloud资源（））
- `bool get_canAccess()`
  （bool get_canAccess（））
- `int get_vertexCount()`
  （int get_vertex数量（））
- `int get_subMeshCount()`
  （int get_sub网格数量（））
- `SubMeshDescriptor GetSubMesh(int index)`
  （子网格Descriptor 获取子网格（int index））
- `Bounds get_bounds()`
  （Bounds get_bounds（））
- `void ClearImpl(bool keepVertexLayout)`
  （void 清除Impl（bool keepVertexLayout））
- `void RecalculateBoundsImpl(MeshUpdateFlags flags)`
  （void RecalculateBoundsImpl（网格更新Flags flags））
- `void UploadMeshDataImpl(bool markNoLongerReadable)`
  （void Upload网格数据Impl（bool markNoLongerReadable））
- `void CombineMeshesImpl(CombineInstance[] combine, bool mergeSubMeshes, bool useMatrices, bool hasLightmapData)`
  （void CombineMeshesImpl（CombineInstance[] combine, bool mergeSubMeshes, bool useMatrices, bool hasLightmapData））
- `VertexAttribute GetUVChannel(int uvIndex)`
  （VertexAttribute 获取UVChannel（int uvIndex））
- `int DefaultDimensionForChannel(VertexAttribute channel)`
  （int 默认的DimensionForChannel（VertexAttribute channel））
- `void SetSizedArrayForChannel(VertexAttribute channel, VertexAttributeFormat format, int dim, Array values, int valuesArrayLength, int valuesStart, int valuesCount, MeshUpdateFlags flags)`
  （void 集合Sized数组ForChannel（VertexAttribute channel, VertexAttribute格式化 format, int dim, 数组 values, int valuesArrayLength, int valuesStart, int valuesCount, 网格更新Flags flags））
- `Vector3[] get_vertices()`
  （Vector3[] get_vertices（））
- `void set_vertices(Vector3[] value)`
  （void set_vertices（Vector3[] value））
- `Vector3[] get_normals()`
  （Vector3[] get_normals（））
- `void set_normals(Vector3[] value)`
  （void set_normals（Vector3[] value））
- `Vector4[] get_tangents()`
  （Vector4[] get_tangents（））
- `void set_tangents(Vector4[] value)`
  （void set_tangents（Vector4[] value））
- `void set_uv(Vector2[] value)`
  （void set_uv（Vector2[] value））
- `void set_colors(Color[] value)`
  （void set_colors（Color[] value））
- `Color32[] get_colors32()`
  （Color32[] get_colors32（））
- `void SetVertices(List<Vector3> inVertices)`
  （void 集合Vertices（List<Vector3> inVertices））
- `void SetVertices(List<Vector3> inVertices, int start, int length)`
  （void 集合Vertices（List<Vector3> inVertices, int start, int length））
- `void SetVertices(List<Vector3> inVertices, int start, int length, MeshUpdateFlags flags)`
  （void 集合Vertices（List<Vector3> inVertices, int start, int length, 网格更新Flags flags））
- `void SetNormals(List<Vector3> inNormals)`
  （void 集合Normals（List<Vector3> inNormals））
- `void SetNormals(List<Vector3> inNormals, int start, int length)`
  （void 集合Normals（List<Vector3> inNormals, int start, int length））
- `void SetNormals(List<Vector3> inNormals, int start, int length, MeshUpdateFlags flags)`
  （void 集合Normals（List<Vector3> inNormals, int start, int length, 网格更新Flags flags））
- `void SetTangents(List<Vector4> inTangents)`
  （void 集合Tangents（List<Vector4> inTangents））
- `void SetTangents(List<Vector4> inTangents, int start, int length)`
  （void 集合Tangents（List<Vector4> inTangents, int start, int length））
- `void SetTangents(List<Vector4> inTangents, int start, int length, MeshUpdateFlags flags)`
  （void 集合Tangents（List<Vector4> inTangents, int start, int length, 网格更新Flags flags））
- `void SetColors(List<Color32> inColors)`
  （void 集合Colors（List<Color32> inColors））
- `void SetColors(List<Color32> inColors, int start, int length)`
  （void 集合Colors（List<Color32> inColors, int start, int length））
- `void SetColors(List<Color32> inColors, int start, int length, MeshUpdateFlags flags)`
  （void 集合Colors（List<Color32> inColors, int start, int length, 网格更新Flags flags））
- `void SetUVs(int channel, List<Vector2> uvs)`
  （void 集合UVs（int channel, List<Vector2> uvs））
- `void SetUVs(int channel, List<Vector4> uvs)`
  （void 集合UVs（int channel, List<Vector4> uvs））
- `void SetUVs(int channel, List<Vector2> uvs, int start, int length)`
  （void 集合UVs（int channel, List<Vector2> uvs, int start, int length））
- `void SetUVs(int channel, List<Vector2> uvs, int start, int length, MeshUpdateFlags flags)`
  （void 集合UVs（int channel, List<Vector2> uvs, int start, int length, 网格更新Flags flags））
- `void SetUVs(int channel, List<Vector4> uvs, int start, int length)`
  （void 集合UVs（int channel, List<Vector4> uvs, int start, int length））
- `void SetUVs(int channel, List<Vector4> uvs, int start, int length, MeshUpdateFlags flags)`
  （void 集合UVs（int channel, List<Vector4> uvs, int start, int length, 网格更新Flags flags））
- `void GetUVs(int channel, List<Vector4> uvs)`
  （void 获取UVs（int channel, List<Vector4> uvs））
- `int get_vertexAttributeCount()`
  （int get_vertexAttribute数量（））
- `void SetVertexBufferParams(int vertexCount, VertexAttributeDescriptor[] attributes)`
  （void 集合Vertex缓冲区Params（int vertexCount, VertexAttributeDescriptor[] attributes））
- `void PrintErrorCantAccessIndices()`
  （void PrintErrorCantAccessIndices（））
- `bool CheckCanAccessSubmesh(int submesh, bool errorAboutTriangles)`
  （bool 检查能否AccessSubmesh（int submesh, bool errorAboutTriangles））
- `bool CheckCanAccessSubmeshTriangles(int submesh)`
  （bool 检查能否AccessSubmeshTriangles（int submesh））
- `bool CheckCanAccessSubmeshIndices(int submesh)`
  （bool 检查能否AccessSubmeshIndices（int submesh））
- `int[] get_triangles()`
  （int[] get_triangles（））
- `void set_triangles(int[] value)`
  （void set_triangles（int[] value））
- `int[] GetIndices(int submesh)`
  （int[] 获取Indices（int submesh））
- `int[] GetIndices(int submesh, bool applyBaseVertex)`
  （int[] 获取Indices（int submesh, bool applyBaseVertex））
- `uint GetIndexCount(int submesh)`
  （uint 获取索引数量（int submesh））
- `void CheckIndicesArrayRange(int valuesLength, int start, int length)`
  （void 检查Indices数组范围（int valuesLength, int start, int length））
- `void SetTrianglesImpl(int submesh, IndexFormat indicesFormat, Array triangles, int trianglesArrayLength, int start, int length, bool calculateBounds, int baseVertex)`
  （void 集合TrianglesImpl（int submesh, 索引格式化 indicesFormat, 数组 triangles, int trianglesArrayLength, int start, int length, bool calculateBounds, int baseVertex））
- `void SetTriangles(List<int> triangles, int submesh)`
  （void 集合Triangles（List<int> triangles, int submesh））
- `void SetTriangles(List<int> triangles, int submesh, bool calculateBounds, int baseVertex)`
  （void 集合Triangles（List<int> triangles, int submesh, bool calculateBounds, int baseVertex））
- `void SetTriangles(List<int> triangles, int trianglesStart, int trianglesLength, int submesh, bool calculateBounds = True, int baseVertex = 0)`
  （void 集合Triangles（List<int> triangles, int trianglesStart, int trianglesLength, int submesh, bool calculateBounds = True, int baseVertex = 0））
- `void SetIndices(int[] indices, MeshTopology topology, int submesh, bool calculateBounds)`
  （void 集合Indices（int[] indices, 网格Topology topology, int submesh, bool calculateBounds））
- `void SetIndices(int[] indices, MeshTopology topology, int submesh, bool calculateBounds, int baseVertex)`
  （void 集合Indices（int[] indices, 网格Topology topology, int submesh, bool calculateBounds, int baseVertex））
- `void SetIndices(int[] indices, int indicesStart, int indicesLength, MeshTopology topology, int submesh, bool calculateBounds = True, int baseVertex = 0)`
  （void 集合Indices（int[] indices, int indicesStart, int indicesLength, 网格Topology topology, int submesh, bool calculateBounds = True, int baseVertex = 0））
- `void SetIndices(ushort[] indices, MeshTopology topology, int submesh, bool calculateBounds = True, int baseVertex = 0)`
  （void 集合Indices（ushort[] indices, 网格Topology topology, int submesh, bool calculateBounds = True, int baseVertex = 0））
- `void SetIndices(ushort[] indices, int indicesStart, int indicesLength, MeshTopology topology, int submesh, bool calculateBounds = True, int baseVertex = 0)`
  （void 集合Indices（ushort[] indices, int indicesStart, int indicesLength, 网格Topology topology, int submesh, bool calculateBounds = True, int baseVertex = 0））
- `void Clear()`
  （void 清除（））
- `void RecalculateBounds()`
  （void RecalculateBounds（））
- `void RecalculateBounds(MeshUpdateFlags flags)`
  （void RecalculateBounds（网格更新Flags flags））
- `void UploadMeshData(bool markNoLongerReadable)`
  （void Upload网格数据（bool markNoLongerReadable））
- `void CombineMeshes(CombineInstance[] combine, bool mergeSubMeshes)`
  （void CombineMeshes（CombineInstance[] combine, bool mergeSubMeshes））
- `void GetVertexAttribute_Injected(int index, out VertexAttributeDescriptor ret)`
  （void 获取VertexAttribute_Injected（int index, out VertexAttributeDescriptor ret））
- `void GetSubMesh_Injected(int index, out SubMeshDescriptor ret)`
  （void 获取子Mesh_Injected（int index, out SubMeshDescriptor ret））
- `void get_bounds_Injected(out Bounds ret)`
  （void get_bounds_Injected（out Bounds ret））

---

## Mesh（网格）

**继承**: MeshUtils.Pooled<Mesh>（网格Utils.Pooled<Mesh>）

### 字段 (4)

- `MeshUtils.Vertex _vHead`（网格Utils.Vertex _v头部）(偏移: 0x8)
- `MeshUtils.Face _fHead`（网格Utils.Face _f头部）(偏移: 0xC)
- `MeshUtils.Edge _eHead`（网格Utils.Edge _e头部）(偏移: 0x10)
- `MeshUtils.Edge _eHeadSym`（网格Utils.Edge _e头部Sym）(偏移: 0x14)

### 方法 (11)

- `void Reset()`
  （void 重置（））
- `void OnFree()`
  （void OnFree（））
- `MeshUtils.Edge MakeEdge()`
  （网格Utils.Edge MakeEdge（））
- `void Splice(MeshUtils.Edge eOrg, MeshUtils.Edge eDst)`
  （void Splice（网格Utils.Edge eOrg, 网格Utils.Edge eDst））
- `void Delete(MeshUtils.Edge eDel)`
  （void Delete（网格Utils.Edge eDel））
- `MeshUtils.Edge AddEdgeVertex(MeshUtils.Edge eOrg)`
  （网格Utils.Edge 添加EdgeVertex（网格Utils.Edge eOrg））
- `MeshUtils.Edge SplitEdge(MeshUtils.Edge eOrg)`
  （网格Utils.Edge SplitEdge（网格Utils.Edge eOrg））
- `MeshUtils.Edge Connect(MeshUtils.Edge eOrg, MeshUtils.Edge eDst)`
  （网格Utils.Edge Connect（网格Utils.Edge eOrg, 网格Utils.Edge eDst））
- `void ZapFace(MeshUtils.Face fZap)`
  （void ZapFace（网格Utils.Face fZap））
- `void MergeConvexFaces(int maxVertsPerFace)`
  （void MergeConvexFaces（int maxVertsPerFace））
- `void Check()`
  （void 检查（））

---

## Mesh.MeshData（Mesh.网格数据）

### 字段 (1)

- `IntPtr m_Ptr`（整数Ptr m_Ptr）(偏移: 0x0)

---

## MeshCollider（网格碰撞器）

**继承**: Collider（碰撞器）

### 方法 (1)

- `Mesh get_sharedMesh()`
  （网格 get_shared网格（））

---

## MeshFilter（网格Filter）

**继承**: Component（组件）

### 方法 (4)

- `void DontStripMeshFilter()`
  （void DontStrip网格Filter（））
- `Mesh get_sharedMesh()`
  （网格 get_shared网格（））
- `void set_sharedMesh(Mesh value)`
  （void set_shared网格（网格 value））
- `void set_mesh(Mesh value)`
  （void set_mesh（网格 value））

---

## MeshGenerationResult（网格GenerationResult）

**继承**: IEquatable<MeshGenerationResult>（IEquatable<网格GenerationResult>）

### 方法 (8)

- `MeshId get_MeshId()`
  （网格Id get_网格Id（））
- `Mesh get_Mesh()`
  （网格 get_网格（））
- `MeshCollider get_MeshCollider()`
  （网格碰撞器 get_网格碰撞器（））
- `MeshGenerationStatus get_Status()`
  （网格GenerationStatus get_Status（））
- `MeshVertexAttributes get_Attributes()`
  （网格VertexAttributes get_Attributes（））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `bool Equals(MeshGenerationResult other)`
  （bool Equals（网格GenerationResult other））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## MeshGenerationStatus（网格GenerationStatus）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## MeshId（网格Id）

**继承**: IEquatable<MeshId>（IEquatable<网格Id>）

### 字段 (3)

- `MeshId s_InvalidId`（网格Id s_InvalidId）(偏移: 0x0)
- `ulong m_SubId1`（ulong m_子Id1）(偏移: 0x0)
- `ulong m_SubId2`（ulong m_子Id2）(偏移: 0x8)

### 方法 (4)

- `string ToString()`
  （string To字符串（））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `bool Equals(MeshId other)`
  （bool Equals（网格Id other））

---

## MeshNode（网格节点）

**继承**: GraphNode（Graph节点）

### 字段 (1)

- `Connection[] connections`（Connection[] connections）(偏移: 0x20)

### 方法 (11)

- `void ClearConnections(bool alsoReverse)`
  （void 清除Connections（bool alsoReverse））
- `void GetConnections(Action<GraphNode> action)`
  （void 获取Connections（Action<GraphNode> action））
- `bool ContainsConnection(GraphNode node)`
  （bool Contains连接（Graph节点 node））
- `void UpdateRecursiveG(Path path, PathNode pathNode, PathHandler handler)`
  （void 更新RecursiveG（路径 path, 路径节点 pathNode, 路径处理器 handler））
- `void AddConnection(GraphNode node, uint cost)`
  （void 添加连接（Graph节点 node, uint cost））
- `void AddConnection(GraphNode node, uint cost, int shapeEdge)`
  （void 添加连接（Graph节点 node, uint cost, int shapeEdge））
- `void RemoveConnection(GraphNode node)`
  （void 移除连接（Graph节点 node））
- `bool ContainsPoint(Int3 point)`
  （bool ContainsPoint（Int3 point））
- `int GetGizmoHashCode()`
  （int 获取GizmoHashCode（））
- `void SerializeReferences(GraphSerializationContext ctx)`
  （void SerializeReferences（GraphSerializationContext ctx））
- `void DeserializeReferences(GraphSerializationContext ctx)`
  （void DeserializeReferences（GraphSerializationContext ctx））

---

## MeshRenderer（网格渲染器）

**继承**: Renderer（渲染器）

### 方法 (5)

- `void DontStripMeshRenderer()`
  （void DontStrip网格渲染器（））
- `Mesh get_additionalVertexStreams()`
  （网格 get_additionalVertexStreams（））
- `void set_additionalVertexStreams(Mesh value)`
  （void set_additionalVertexStreams（网格 value））
- `Mesh get_enlightenVertexStream()`
  （网格 get_enlightenVertex流（））
- `void set_enlightenVertexStream(Mesh value)`
  （void set_enlightenVertex流（网格 value））

---

## MeshSubsetCombineUtility.MeshContainer（网格SubsetCombineUtility.网格容器）

### 字段 (3)

- `GameObject gameObject`（游戏对象 game对象）(偏移: 0x0)
- `MeshSubsetCombineUtility.MeshInstance instance`（网格SubsetCombineUtility.网格实例 instance）(偏移: 0x4)
- `List<MeshSubsetCombineUtility.SubMeshInstance> subMeshInstances`（List<网格SubsetCombineUtility.子网格Instance> sub网格Instances）(偏移: 0x74)

---

## MeshSubsetCombineUtility.MeshInstance（网格SubsetCombineUtility.网格实例）

### 字段 (7)

- `int meshInstanceID`（int mesh实例ID）(偏移: 0x0)
- `int rendererInstanceID`（int renderer实例ID）(偏移: 0x4)
- `int additionalVertexStreamsMeshInstanceID`（int additionalVertexStreams网格实例ID）(偏移: 0x8)
- `int enlightenVertexStreamMeshInstanceID`（int enlightenVertex流网格实例ID）(偏移: 0xC)
- `Matrix4x4 transform`（Matrix4x4 transform）(偏移: 0x10)
- `Vector4 lightmapScaleOffset`（Vector4 lightmap缩放Offset）(偏移: 0x50)
- `Vector4 realtimeLightmapScaleOffset`（Vector4 realtimeLightmap缩放Offset）(偏移: 0x60)

---

## MeshSubsetCombineUtility.SubMeshInstance（网格SubsetCombineUtility.子网格实例）

### 字段 (5)

- `int meshInstanceID`（int mesh实例ID）(偏移: 0x0)
- `int vertexOffset`（int vertexOffset）(偏移: 0x4)
- `int gameObjectInstanceID`（int game对象实例ID）(偏移: 0x8)
- `int subMeshIndex`（int sub网格索引）(偏移: 0xC)
- `Matrix4x4 transform`（Matrix4x4 transform）(偏移: 0x10)

---

## MeshTopology（网格Topology）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## MeshUpdateFlags（网格更新Flags）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## MeshUtils（网格Utils）

### 方法 (8)

- `MeshUtils.Edge MakeEdge(MeshUtils.Edge eNext)`
  （网格Utils.Edge MakeEdge（网格Utils.Edge eNext））
- `void Splice(MeshUtils.Edge a, MeshUtils.Edge b)`
  （void Splice（网格Utils.Edge a, 网格Utils.Edge b））
- `void MakeVertex(MeshUtils.Edge eOrig, MeshUtils.Vertex vNext)`
  （void MakeVertex（网格Utils.Edge eOrig, 网格Utils.Vertex vNext））
- `void MakeFace(MeshUtils.Edge eOrig, MeshUtils.Face fNext)`
  （void MakeFace（网格Utils.Edge eOrig, 网格Utils.Face fNext））
- `void KillEdge(MeshUtils.Edge eDel)`
  （void 击杀Edge（网格Utils.Edge eDel））
- `void KillVertex(MeshUtils.Vertex vDel, MeshUtils.Vertex newOrg)`
  （void 击杀Vertex（网格Utils.Vertex vDel, 网格Utils.Vertex newOrg））
- `void KillFace(MeshUtils.Face fDel, MeshUtils.Face newLFace)`
  （void 击杀Face（网格Utils.Face fDel, 网格Utils.Face newLFace））
- `float FaceArea(MeshUtils.Face f)`
  （float FaceArea（网格Utils.Face f））

---

## MeshUtils.Edge（网格Utils.Edge）

**继承**: MeshUtils.Pooled<MeshUtils.Edge>（网格Utils.Pooled<网格Utils.Edge>）

### 字段 (9)

- `MeshUtils.EdgePair _pair`（网格Utils.EdgePair _pair）(偏移: 0x8)
- `MeshUtils.Edge _next`（网格Utils.Edge _next）(偏移: 0x10)
- `MeshUtils.Edge _Sym`（网格Utils.Edge _Sym）(偏移: 0x14)
- `MeshUtils.Edge _Onext`（网格Utils.Edge _Onext）(偏移: 0x18)
- `MeshUtils.Edge _Lnext`（网格Utils.Edge _Lnext）(偏移: 0x1C)
- `MeshUtils.Vertex _Org`（网格Utils.Vertex _Org）(偏移: 0x20)
- `MeshUtils.Face _Lface`（网格Utils.Face _Lface）(偏移: 0x24)
- `Tess.ActiveRegion _activeRegion`（Tess.激活的Region _activeRegion）(偏移: 0x28)
- `int _winding`（int _winding）(偏移: 0x2C)

### 方法 (18)

- `MeshUtils.Face get__Rface()`
  （网格Utils.Face get__Rface（））
- `void set__Rface(MeshUtils.Face value)`
  （void set__Rface（网格Utils.Face value））
- `MeshUtils.Vertex get__Dst()`
  （网格Utils.Vertex get__Dst（））
- `void set__Dst(MeshUtils.Vertex value)`
  （void set__Dst（网格Utils.Vertex value））
- `MeshUtils.Edge get__Oprev()`
  （网格Utils.Edge get__Oprev（））
- `void set__Oprev(MeshUtils.Edge value)`
  （void set__Oprev（网格Utils.Edge value））
- `MeshUtils.Edge get__Lprev()`
  （网格Utils.Edge get__Lprev（））
- `void set__Lprev(MeshUtils.Edge value)`
  （void set__Lprev（网格Utils.Edge value））
- `MeshUtils.Edge get__Dprev()`
  （网格Utils.Edge get__Dprev（））
- `void set__Dprev(MeshUtils.Edge value)`
  （void set__Dprev（网格Utils.Edge value））
- `MeshUtils.Edge get__Rprev()`
  （网格Utils.Edge get__Rprev（））
- `void set__Rprev(MeshUtils.Edge value)`
  （void set__Rprev（网格Utils.Edge value））
- `MeshUtils.Edge get__Dnext()`
  （网格Utils.Edge get__Dnext（））
- `void set__Dnext(MeshUtils.Edge value)`
  （void set__Dnext（网格Utils.Edge value））
- `MeshUtils.Edge get__Rnext()`
  （网格Utils.Edge get__Rnext（））
- `void set__Rnext(MeshUtils.Edge value)`
  （void set__Rnext（网格Utils.Edge value））
- `void EnsureFirst(ref MeshUtils.Edge e)`
  （void Ensure第一个（ref MeshUtils.Edge e））
- `void Reset()`
  （void 重置（））

---

## MeshUtils.EdgePair（网格Utils.EdgePair）

### 字段 (2)

- `MeshUtils.Edge _e`（网格Utils.Edge _e）(偏移: 0x0)
- `MeshUtils.Edge _eSym`（网格Utils.Edge _eSym）(偏移: 0x4)

### 方法 (2)

- `MeshUtils.EdgePair Create()`
  （网格Utils.EdgePair 创建（））
- `void Reset()`
  （void 重置（））

---

## MeshUtils.Face（网格Utils.Face）

**继承**: MeshUtils.Pooled<MeshUtils.Face>（网格Utils.Pooled<网格Utils.Face>）

### 字段 (7)

- `MeshUtils.Face _prev`（网格Utils.Face _prev）(偏移: 0x8)
- `MeshUtils.Face _next`（网格Utils.Face _next）(偏移: 0xC)
- `MeshUtils.Edge _anEdge`（网格Utils.Edge _anEdge）(偏移: 0x10)
- `MeshUtils.Face _trail`（网格Utils.Face _trail）(偏移: 0x14)
- `int _n`（int _n）(偏移: 0x18)
- `bool _marked`（bool _marked）(偏移: 0x1C)
- `bool _inside`（bool _inside）(偏移: 0x1D)

### 方法 (2)

- `int get_VertsCount()`
  （int get_Verts数量（））
- `void Reset()`
  （void 重置（））

---

## MeshUtils.Vertex（网格Utils.Vertex）

**继承**: MeshUtils.Pooled<MeshUtils.Vertex>（网格Utils.Pooled<网格Utils.Vertex>）

### 字段 (9)

- `MeshUtils.Vertex _prev`（网格Utils.Vertex _prev）(偏移: 0x8)
- `MeshUtils.Vertex _next`（网格Utils.Vertex _next）(偏移: 0xC)
- `MeshUtils.Edge _anEdge`（网格Utils.Edge _anEdge）(偏移: 0x10)
- `Vec3 _coords`（Vec3 _coords）(偏移: 0x14)
- `float _s`（float _s）(偏移: 0x20)
- `float _t`（float _t）(偏移: 0x24)
- `PQHandle _pqHandle`（PQ句柄 _pq句柄）(偏移: 0x28)
- `int _n`（int _n）(偏移: 0x2C)
- `object _data`（object _data）(偏移: 0x30)

### 方法 (1)

- `void Reset()`
  （void 重置（））

---

## MeshVertexAttributes（网格VertexAttributes）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## MessageDictionary（Message字典）

**继承**: IDictionary, ICollection, IEnumerable（I字典, ICollection, IEnumerable）

### 字段 (4)

- `IDictionary _internalProperties`（I字典 _internalProperties）(偏移: 0x8)
- `IMethodMessage _message`（IMethodMessage _message）(偏移: 0xC)
- `string[] _methodKeys`（string[] _methodKeys）(偏移: 0x10)
- `bool _ownProperties`（bool _ownProperties）(偏移: 0x14)

### 方法 (18)

- `bool HasUserData()`
  （bool 是否有User数据（））
- `IDictionary get_InternalDictionary()`
  （I字典 get_内部的字典（））
- `void set_MethodKeys(string[] value)`
  （void set_MethodKeys（string[] value））
- `IDictionary AllocInternalProperties()`
  （I字典 Alloc内部的Properties（））
- `IDictionary GetInternalProperties()`
  （I字典 获取内部的Properties（））
- `bool IsOverridenKey(string key)`
  （bool 是否Overriden键（string key））
- `object get_Item(object key)`
  （object get_项目（object key））
- `void set_Item(object key, object value)`
  （void set_项目（object key, object value））
- `object GetMethodProperty(string key)`
  （object 获取Method属性（string key））
- `void SetMethodProperty(string key, object value)`
  （void 集合Method属性（string key, object value））
- `ICollection get_Values()`
  （ICollection get_Values（））
- `void Add(object key, object value)`
  （void 添加（object key, object value））
- `bool Contains(object key)`
  （bool Contains（object key））
- `void Remove(object key)`
  （void 移除（object key））
- `int get_Count()`
  （int get_数量（））
- `object get_SyncRoot()`
  （object get_同步根（））
- `void CopyTo(Array array, int index)`
  （void 复制To（数组 array, int index））
- `IDictionaryEnumerator GetEnumerator()`
  （I字典Enumerator 获取Enumerator（））

---

## MessageDictionary.DictionaryEnumerator（MessageDictionary.字典Enumerator）

**继承**: IDictionaryEnumerator, IEnumerator（I字典Enumerator, IEnumerator）

### 字段 (3)

- `MessageDictionary _methodDictionary`（Message字典 _method字典）(偏移: 0x8)
- `IDictionaryEnumerator _hashtableEnum`（I字典Enumerator _hashtableEnum）(偏移: 0xC)
- `int _posMethod`（int _posMethod）(偏移: 0x10)

### 方法 (6)

- `object get_Current()`
  （object get_当前（））
- `bool MoveNext()`
  （bool 移动下一个（））
- `void Reset()`
  （void 重置（））
- `DictionaryEntry get_Entry()`
  （字典Entry get_Entry（））
- `object get_Key()`
  （object get_键（））
- `object get_Value()`
  （object get_值（））

---

## MessageEnd（Message结束）

### 方法 (4)

- `void Write(__BinaryWriter sout)`
  （void Write（__Binary写入器 sout））
- `void Read(__BinaryParser input)`
  （void Read（__BinaryParser input））
- `void Dump()`
  （void Dump（））
- `void Dump(Stream sout)`
  （void Dump（流 sout））

---

## MessageEnum（MessageEnum）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## MessageEventArgs（Message事件Args）

### 字段 (2)

- `int playerId`（int playerId）(偏移: 0x8)
- `byte[] data`（byte[] data）(偏移: 0xC)

---

## MetaData（Meta数据）

### 字段 (2)

- `string content`（string content）(偏移: 0x8)
- `string platform`（string platform）(偏移: 0xC)

---

## MethodAttributes（MethodAttributes）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## MethodBase（Method基础）

**继承**: MemberInfo, _MethodBase（Member信息, _Method基础）

### 方法 (30)

- `MethodBase GetMethodFromHandle(RuntimeMethodHandle handle)`
  （Method基础 获取MethodFrom句柄（RuntimeMethod句柄 handle））
- `bool op_Equality(MethodBase left, MethodBase right)`
  （bool op_Equality（Method基础 left, Method基础 right））
- `bool op_Inequality(MethodBase left, MethodBase right)`
  （bool op_Inequality（Method基础 left, Method基础 right））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））
- `ParameterInfo[] GetParametersNoCopy()`
  （ParameterInfo[] 获取ParametersNo复制（））
- `CallingConventions get_CallingConvention()`
  （CallingConventions get_CallingConvention（））
- `Type[] GetGenericArguments()`
  （Type[] 获取GenericArguments（））
- `bool get_IsGenericMethodDefinition()`
  （bool get_是否GenericMethodDefinition（））
- `bool get_ContainsGenericParameters()`
  （bool get_ContainsGenericParameters（））
- `bool get_IsGenericMethod()`
  （bool get_是否GenericMethod（））
- `bool get_IsSecurityCritical()`
  （bool get_是否SecurityCritical（））
- `object Invoke(object obj, object[] parameters)`
  （object Invoke（object obj, object[] parameters））
- `bool get_IsPublic()`
  （bool get_是否公开的（））
- `bool get_IsStatic()`
  （bool get_是否静态的（））
- `bool get_IsVirtual()`
  （bool get_是否虚拟的（））
- `bool get_IsAbstract()`
  （bool get_是否抽象的（））
- `bool get_IsConstructor()`
  （bool get_是否Constructor（））
- `MethodBody GetMethodBody()`
  （Method身体 获取Method身体（））
- `string ConstructParameters(Type[] parameterTypes, CallingConventions callingConvention, bool serialization)`
  （string ConstructParameters（Type[] parameterTypes, CallingConventions callingConvention, bool serialization））
- `string FormatNameAndSig(bool serialization)`
  （string 格式化名称AndSig（bool serialization））
- `Type[] GetParameterTypes()`
  （Type[] 获取ParameterTypes（））
- `ParameterInfo[] GetParametersInternal()`
  （ParameterInfo[] 获取Parameters内部的（））
- `int GetParametersCount()`
  （int 获取Parameters数量（））
- `MethodBase GetMethodFromHandleNoGenericCheck(RuntimeMethodHandle handle)`
  （Method基础 获取MethodFrom句柄NoGeneric检查（RuntimeMethod句柄 handle））
- `MethodBase GetMethodFromHandleNoGenericCheck(RuntimeMethodHandle handle, RuntimeTypeHandle reflectedType)`
  （Method基础 获取MethodFrom句柄NoGeneric检查（RuntimeMethod句柄 handle, Runtime类型句柄 reflectedType））
- `MethodBody GetMethodBodyInternal(IntPtr handle)`
  （Method身体 获取Method身体内部的（整数Ptr handle））
- `MethodBody GetMethodBody(IntPtr handle)`
  （Method身体 获取Method身体（整数Ptr handle））
- `MethodBase GetMethodFromHandleInternalType(IntPtr method_handle, IntPtr type_handle)`
  （Method基础 获取MethodFrom句柄内部的类型（整数Ptr method_handle, 整数Ptr type_handle））
- `MethodBase GetMethodFromHandleInternalType_native(IntPtr method_handle, IntPtr type_handle, bool genericCheck)`
  （Method基础 获取MethodFrom句柄内部的Type_native（整数Ptr method_handle, 整数Ptr type_handle, bool genericCheck））

---

## MethodBody（Method身体）

### 字段 (6)

- `ExceptionHandlingClause[] clauses`（ExceptionHandlingClause[] clauses）(偏移: 0x8)
- `LocalVariableInfo[] locals`（本地的VariableInfo[] locals）(偏移: 0xC)
- `byte[] il`（byte[] il）(偏移: 0x10)
- `bool init_locals`（bool init_locals）(偏移: 0x14)
- `int sig_token`（int sig_token）(偏移: 0x18)
- `int max_stack`（int max_stack）(偏移: 0x1C)

### 方法 (1)

- `byte[] GetILAsByteArray()`
  （byte[] 获取ILAsByte数组（））

---

## MethodBuilder（Method构建器）

**继承**: MethodInfo（Method信息）

### 方法 (11)

- `MethodAttributes get_Attributes()`
  （MethodAttributes get_Attributes（））
- `Type get_DeclaringType()`
  （类型 get_Declaring类型（））
- `string get_Name()`
  （string get_名称（））
- `ParameterInfo[] GetParameters()`
  （ParameterInfo[] 获取Parameters（））
- `RuntimeMethodHandle get_MethodHandle()`
  （RuntimeMethod句柄 get_Method句柄（））
- `Type get_ReflectedType()`
  （类型 get_Reflected类型（））
- `object[] GetCustomAttributes(bool inherit)`
  （object[] 获取自定义的Attributes（bool inherit））
- `object[] GetCustomAttributes(Type attributeType, bool inherit)`
  （object[] 获取自定义的Attributes（类型 attributeType, bool inherit））
- `MethodImplAttributes GetMethodImplementationFlags()`
  （MethodImplAttributes 获取MethodImplementationFlags（））
- `object Invoke(object obj, BindingFlags invokeAttr, Binder binder, object[] parameters, CultureInfo culture)`
  （object Invoke（object obj, BindingFlags invokeAttr, Binder binder, object[] parameters, Culture信息 culture））
- `bool IsDefined(Type attributeType, bool inherit)`
  （bool 是否Defined（类型 attributeType, bool inherit））

---

## MethodCall（MethodCall）

**继承**: IMethodCallMessage, IMethodMessage, IMessage, ISerializable, IInternalMessage（IMethodCallMessage, IMethodMessage, IMessage, ISerializable, I内部的Message）

### 字段 (11)

- `string _uri`（string _uri）(偏移: 0x8)
- `string _typeName`（string _type名称）(偏移: 0xC)
- `string _methodName`（string _method名称）(偏移: 0x10)
- `object[] _args`（object[] _args）(偏移: 0x14)
- `Type[] _methodSignature`（Type[] _methodSignature）(偏移: 0x18)
- `MethodBase _methodBase`（Method基础 _method基础）(偏移: 0x1C)
- `LogicalCallContext _callContext`（LogicalCallContext _callContext）(偏移: 0x20)
- `Identity _targetIdentity`（Identity _targetIdentity）(偏移: 0x24)
- `Type[] _genericArguments`（Type[] _genericArguments）(偏移: 0x28)
- `IDictionary ExternalProperties`（I字典 外部的Properties）(偏移: 0x2C)
- `IDictionary InternalProperties`（I字典 内部的Properties）(偏移: 0x30)

### 方法 (20)

- `void CopyFrom(IMethodMessage call)`
  （void 复制From（IMethodMessage call））
- `void InitMethodProperty(string key, object value)`
  （void 初始化Method属性（string key, object value））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））
- `int get_ArgCount()`
  （int get_Arg数量（））
- `object[] get_Args()`
  （object[] get_Args（））
- `LogicalCallContext get_LogicalCallContext()`
  （LogicalCallContext get_LogicalCallContext（））
- `MethodBase get_MethodBase()`
  （Method基础 get_Method基础（））
- `string get_MethodName()`
  （string get_Method名称（））
- `object get_MethodSignature()`
  （object get_MethodSignature（））
- `IDictionary get_Properties()`
  （I字典 get_Properties（））
- `void InitDictionary()`
  （void 初始化字典（））
- `string get_TypeName()`
  （string get_类型名称（））
- `string get_Uri()`
  （string get_Uri（））
- `void set_Uri(string value)`
  （void set_Uri（string value））
- `object GetArg(int argNum)`
  （object 获取Arg（int argNum））
- `void Init()`
  （void 初始化（））
- `void ResolveMethod()`
  （void ResolveMethod（））
- `Type CastTo(string clientType, Type serverType)`
  （类型 CastTo（string clientType, 类型 serverType））
- `string GetTypeNameFromAssemblyQualifiedName(string aqname)`
  （string 获取类型名称FromAssemblyQualified名称（string aqname））
- `Type[] get_GenericArguments()`
  （Type[] get_GenericArguments（））

---

## MethodImplAttributes（MethodImplAttributes）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## MethodInfo（Method信息）

**继承**: MethodBase, _MethodInfo（Method基础, _Method信息）

### 方法 (10)

- `bool op_Equality(MethodInfo left, MethodInfo right)`
  （bool op_Equality（Method信息 left, Method信息 right））
- `bool op_Inequality(MethodInfo left, MethodInfo right)`
  （bool op_Inequality（Method信息 left, Method信息 right））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））
- `MemberTypes get_MemberType()`
  （MemberTypes get_Member类型（））
- `Type get_ReturnType()`
  （类型 get_Return类型（））
- `Type[] GetGenericArguments()`
  （Type[] 获取GenericArguments（））
- `MethodInfo GetGenericMethodDefinition()`
  （Method信息 获取GenericMethodDefinition（））
- `MethodInfo MakeGenericMethod(Type[] typeArguments)`
  （Method信息 MakeGenericMethod（Type[] typeArguments））
- `MethodInfo GetBaseMethod()`
  （Method信息 获取基础Method（））

---

## MethodResponse（Method响应）

**继承**: IMethodReturnMessage, IMethodMessage, IMessage, ISerializable, IInternalMessage（IMethodReturnMessage, IMethodMessage, IMessage, ISerializable, I内部的Message）

### 字段 (15)

- `string _methodName`（string _method名称）(偏移: 0x8)
- `string _uri`（string _uri）(偏移: 0xC)
- `string _typeName`（string _type名称）(偏移: 0x10)
- `MethodBase _methodBase`（Method基础 _method基础）(偏移: 0x14)
- `object _returnValue`（object _return值）(偏移: 0x18)
- `Exception _exception`（Exception _exception）(偏移: 0x1C)
- `Type[] _methodSignature`（Type[] _methodSignature）(偏移: 0x20)
- `ArgInfo _inArgInfo`（Arg信息 _inArg信息）(偏移: 0x24)
- `object[] _args`（object[] _args）(偏移: 0x28)
- `object[] _outArgs`（object[] _outArgs）(偏移: 0x2C)
- `IMethodCallMessage _callMsg`（IMethodCallMessage _callMsg）(偏移: 0x30)
- `LogicalCallContext _callContext`（LogicalCallContext _callContext）(偏移: 0x34)
- `Identity _targetIdentity`（Identity _targetIdentity）(偏移: 0x38)
- `IDictionary ExternalProperties`（I字典 外部的Properties）(偏移: 0x3C)
- `IDictionary InternalProperties`（I字典 内部的Properties）(偏移: 0x40)

### 方法 (16)

- `void InitMethodProperty(string key, object value)`
  （void 初始化Method属性（string key, object value））
- `int get_ArgCount()`
  （int get_Arg数量（））
- `object[] get_Args()`
  （object[] get_Args（））
- `Exception get_Exception()`
  （Exception get_Exception（））
- `LogicalCallContext get_LogicalCallContext()`
  （LogicalCallContext get_LogicalCallContext（））
- `MethodBase get_MethodBase()`
  （Method基础 get_Method基础（））
- `string get_MethodName()`
  （string get_Method名称（））
- `object get_MethodSignature()`
  （object get_MethodSignature（））
- `object[] get_OutArgs()`
  （object[] get_OutArgs（））
- `IDictionary get_Properties()`
  （I字典 get_Properties（））
- `object get_ReturnValue()`
  （object get_Return值（））
- `string get_TypeName()`
  （string get_类型名称（））
- `string get_Uri()`
  （string get_Uri（））
- `void set_Uri(string value)`
  （void set_Uri（string value））
- `object GetArg(int argNum)`
  （object 获取Arg（int argNum））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））

---

## MethodReturnDictionary（MethodReturn字典）

**继承**: MessageDictionary（Message字典）

### 字段 (2)

- `string[] InternalReturnKeys`（string[] 内部的ReturnKeys）(偏移: 0x0)
- `string[] InternalExceptionKeys`（string[] 内部的ExceptionKeys）(偏移: 0x4)

---

## MinAttribute（最小Attribute）

**继承**: PropertyAttribute（属性Attribute）

### 字段 (1)

- `float min`（float min）(偏移: 0x8)

---

## MinFloatParameter（最小浮点数Parameter）

**继承**: FloatParameter（浮点数Parameter）

### 字段 (1)

- `float min`（float min）(偏移: 0x10)

### 方法 (2)

- `float get_value()`
  （float get_value（））
- `void set_value(float value)`
  （void set_value（float value））

---

## MinIntParameter（最小整数Parameter）

**继承**: IntParameter（整数Parameter）

### 字段 (1)

- `int min`（int min）(偏移: 0x10)

### 方法 (2)

- `int get_value()`
  （int get_value（））
- `void set_value(int value)`
  （void set_value（int value））

---

## MineBotAI（Mine机器人AI）

**继承**: AIPath（AI路径）

### 字段 (4)

- `Animation anim`（动画 anim）(偏移: 0x10C)
- `float sleepVelocity`（float sleep速度）(偏移: 0x110)
- `float animationSpeed`（float animationSpeed）(偏移: 0x114)
- `GameObject endOfPathEffect`（游戏对象 endOf路径特效）(偏移: 0x118)

---

## MineBotAnimation（Mine机器人动画）

**继承**: VersionedMonoBehaviour（VersionedMonoBehaviour）

### 字段 (6)

- `Animator anim`（动画器 anim）(偏移: 0x10)
- `GameObject endOfPathEffect`（游戏对象 endOf路径特效）(偏移: 0x14)
- `bool isAtDestination`（bool isAtDestination）(偏移: 0x18)
- `IAstarAI ai`（IAstarAI ai）(偏移: 0x1C)
- `Transform tr`（变换 tr）(偏移: 0x20)
- `Vector3 lastTarget`（三维向量 last目标）(偏移: 0x24)

### 方法 (3)

- `void Awake()`
  （void Awake（））
- `void OnTargetReached()`
  （void On目标Reached（））
- `void Update()`
  （void 更新（））

---

## Misc（Misc）

### 方法 (2)

- `void Destroy(Object obj)`
  （void 销毁（对象 obj））
- `void DestroyImmediate(Object obj)`
  （void 销毁Immediate（对象 obj））

---

## MissileData（Missile数据）

### 字段 (11)

- `int clip`（int clip）(偏移: 0x0)
- `int ammo`（int ammo）(偏移: 0x4)
- `GameObject prefab`（游戏对象 prefab）(偏移: 0x8)
- `float damage`（float damage）(偏移: 0xC)
- `float range`（float range）(偏移: 0x10)
- `float damageFactorByDistance`（float damage系数By距离）(偏移: 0x14)
- `float velocity`（float velocity）(偏移: 0x18)
- `float extraGravity`（float extra重力）(偏移: 0x1C)
- `float throwAngle`（float throw角度）(偏移: 0x20)
- `float expTime`（float exp时间）(偏移: 0x24)
- `bool ignoreWall`（bool ignoreWall）(偏移: 0x28)

---

## Missing（Missing）

**继承**: ISerializable（ISerializable）

### 字段 (1)

- `Missing Value`（Missing 值）(偏移: 0x0)

---

## MissingFieldException（MissingFieldException）

**继承**: MissingMemberException, ISerializable（MissingMemberException, ISerializable）

### 方法 (1)

- `string get_Message()`
  （string get_Message（））

---

## MissingMemberException（MissingMemberException）

**继承**: MemberAccessException, ISerializable（MemberAccessException, ISerializable）

### 字段 (3)

- `string ClassName`（string 类名称）(偏移: 0x44)
- `string MemberName`（string Member名称）(偏移: 0x48)
- `byte[] Signature`（byte[] Signature）(偏移: 0x4C)

### 方法 (3)

- `string get_Message()`
  （string get_Message（））
- `string FormatSignature(byte[] signature)`
  （string 格式化Signature（byte[] signature））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））

---

## MissingMethodException（MissingMethodException）

**继承**: MissingMemberException, ISerializable（MissingMemberException, ISerializable）

### 字段 (1)

- `string signature`（string signature）(偏移: 0x50)

### 方法 (1)

- `string get_Message()`
  （string get_Message（））

---

## MissingSatelliteAssemblyException（MissingSatelliteAssemblyException）

**继承**: SystemException（系统Exception）

### 字段 (1)

- `string _cultureName`（string _culture名称）(偏移: 0x44)

---

## MixedLightingMode（MixedLighting模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## MixedLightingSetup（MixedLightingSetup）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ModeBase（模式基础）

**继承**: Singleton<ModeBase>（Singleton<模式Base>）

### 字段 (28)

- `Vector2Int score`（二维向量整数 score）(偏移: 0xC)
- `int currentRound`（int current回合）(偏移: 0x14)
- `int targetRound`（int target回合）(偏移: 0x0)
- `int targetScore`（int target分数）(偏移: 0x4)
- `Vector2Int gameTime`（二维向量整数 game时间）(偏移: 0x8)
- `float respawnTime`（float respawn时间）(偏移: 0x10)
- `bool BLOnLeft`（bool BLOn左）(偏移: 0x18)
- `RawImage scoreBoardImage`（Raw图像 scoreBoard图像）(偏移: 0x1C)
- `Texture[] scoreBoardTex`（Texture[] scoreBoardTex）(偏移: 0x20)
- `Text scoreText_L`（文本 scoreText_L）(偏移: 0x24)
- `Text scoreText_R`（文本 scoreText_R）(偏移: 0x28)
- `Text roundText_T`（文本 roundText_T）(偏移: 0x2C)
- `Text roundText_C`（文本 roundText_C）(偏移: 0x30)
- `Vector2Int restGameTime`（二维向量整数 rest游戏时间）(偏移: 0x34)
- `Text timeText_M`（文本 timeText_M）(偏移: 0x3C)
- `Text timeText_S`（文本 timeText_S）(偏移: 0x40)
- `Material timeFlashMat`（材质 timeFlash材质）(偏移: 0x44)
- `int playerCountBL`（int player数量BL）(偏移: 0x48)
- `int playerCountGR`（int player数量GR）(偏移: 0x4C)
- `int aliveCountBL`（int alive数量BL）(偏移: 0x50)
- `int aliveCountGR`（int alive数量GR）(偏移: 0x54)
- `GameObject rectContainer`（游戏对象 rect容器）(偏移: 0x58)
- `GameObject playerRectPrefab`（游戏对象 playerRect预制体）(偏移: 0x5C)
- `SimpleObjectPool playerRectPool`（Simple对象池 playerRect池）(偏移: 0x60)
- `List<HUD_PlayerRect> playerRect_BL`（List<HUD_玩家Rect> playerRect_BL）(偏移: 0x64)
- `List<HUD_PlayerRect> playerRect_GR`（List<HUD_玩家Rect> playerRect_GR）(偏移: 0x68)
- `Player myPlayer`（玩家 my玩家）(偏移: 0x6C)
- `string[] modeTip`（string[] modeTip）(偏移: 0x70)

### 方法 (24)

- `void set_timeFlash(bool value)`
  （void set_timeFlash（bool value））
- `void set_playerRectVisible(bool value)`
  （void set_playerRect可见的（bool value））
- `bool get_isRoundGame()`
  （bool get_is回合游戏（））
- `void Awake()`
  （void Awake（））
- `void ScoreBoardTexSetting()`
  （void 分数BoardTex设置（））
- `void Start()`
  （void 开始（））
- `void Update()`
  （void 更新（））
- `void UpdatePlayerRect()`
  （void 更新玩家Rect（））
- `void OnStartNewGameRound()`
  （void On开始新的游戏回合（））
- `void ResetTime(int minute, int second)`
  （void 重置时间（int minute, int second））
- `IEnumerator RoundTimer()`
  （IEnumerator 回合计时器（））
- `void UpdateTimeUI()`
  （void 更新时间界面（））
- `void SetCurrentRound(int value)`
  （void 集合当前回合（int value））
- `void AddCurrentRound()`
  （void 添加当前回合（））
- `void SetLeftScore(int value)`
  （void 集合左分数（int value））
- `void AddLeftScore()`
  （void 添加左分数（））
- `void SetRightScore(int value)`
  （void 集合右分数（int value））
- `void AddRightScore()`
  （void 添加右分数（））
- `void OnScoreReachTarget(bool left)`
  （void On分数Reach目标（bool left））
- `void OnTimeOut()`
  （void On时间Out（））
- `void OnMyPlayerJoin(Player myPlayer)`
  （void OnMy玩家Join（玩家 myPlayer））
- `void ShowModeTip()`
  （void 显示模式Tip（））
- `void ExitGame(float delay)`
  （void Exit游戏（float delay））
- `void RefreshNextRound(float waitTime)`
  （void 刷新下一个回合（float waitTime））

---

## ModeBase_Nano（模式Base_纳米）

**继承**: ModeBase（模式基础）

### 字段 (24)

- `NanoModeAsset asset`（纳米模式资产 asset）(偏移: 0x74)
- `NanoModeBasicAsset basicAsset`（纳米模式Basic资产 basic资产）(偏移: 0x78)
- `CommonHud_1 nanoTimerTip`（CommonHud_1 nano计时器Tip）(偏移: 0x7C)
- `HUD_Nano_FinalBattle finalBattle`（HUD_Nano_FinalBattle finalBattle）(偏移: 0x80)
- `CommonHud_1 hpRecoverIcon`（CommonHud_1 hp恢复图标）(偏移: 0x84)
- `CommonHud_1 gKeyTip`（CommonHud_1 g键Tip）(偏移: 0x88)
- `CommonKillMark mark`（Common击杀Mark mark）(偏移: 0x8C)
- `GameObject nanoClothIcon`（游戏对象 nano服装图标）(偏移: 0x90)
- `CommonHud_1 supplyBoxTip`（CommonHud_1 supplyBoxTip）(偏移: 0x94)
- `CommonHud_1 meleeKillNanoTip`（CommonHud_1 melee击杀纳米Tip）(偏移: 0x98)
- `AnimationHud nanoKillMark`（动画Hud nano击杀Mark）(偏移: 0x9C)
- `AnimationHud nanoKillMark_MultiKill`（动画Hud nano击杀Mark_多个击杀）(偏移: 0xA0)
- `int thisRoundPlayer`（int this回合玩家）(偏移: 0xA4)
- `int soldierAttackPower`（int soldierAttack力度）(偏移: 0x0)
- `List<int> ignoreSoldierPowerWpnList`（List<int> ignoreSoldier力度武器列表）(偏移: 0xA8)
- `List<Player> respawningPlayer`（List<Player> respawning玩家）(偏移: 0xAC)
- `NameKeyPool supplyBoxPool`（名称键池 supplyBox池）(偏移: 0xB0)
- `List<Player> randomPlayerList`（List<Player> random玩家列表）(偏移: 0xB4)
- `int[] nanoLevelUpNeedExp`（int[] nano等级上需要Exp）(偏移: 0x8)
- `int BornNanoGhostHP`（int 出生纳米幽灵HP）(偏移: 0xC)
- `float AbsorbNeedTime`（float Absorb需要时间）(偏移: 0x10)
- `int AbsorbCheckCount`（int Absorb检查数量）(偏移: 0x14)
- `string Text_GetSkill`（string Text_获取技能）(偏移: 0x18)
- `string[] Tip_Infect`（string[] Tip_Infect）(偏移: 0x1C)

### 方法 (83)

- `ModeBase_Nano get_instance2()`
  （模式Base_纳米 get_instance2（））
- `bool get_nanoRespawn_Melee()`
  （bool get_nanoRespawn_Melee（））
- `void set_nanoRespawn_Melee(bool value)`
  （void set_nanoRespawn_Melee（bool value））
- `bool get_nanoRespawn_Headshot()`
  （bool get_nanoRespawn_Headshot（））
- `void set_nanoRespawn_Headshot(bool value)`
  （void set_nanoRespawn_Headshot（bool value））
- `int get_maxLevel()`
  （int get_max等级（））
- `void Awake()`
  （void Awake（））
- `void ScoreBoardTexSetting()`
  （void 分数BoardTex设置（））
- `void OnStartNewGameRound()`
  （void On开始新的游戏回合（））
- `int GetNanoAppearTime()`
  （int 获取纳米Appear时间（））
- `IEnumerator NanoTimer()`
  （IEnumerator 纳米计时器（））
- `void InitSetting()`
  （void 初始化设置（））
- `void UpdateRandomPlayerList()`
  （void 更新随机玩家列表（））
- `int GetNanoGhostCount()`
  （int 获取纳米幽灵数量（））
- `void GenerateNanoGhost()`
  （void Generate纳米幽灵（））
- `void ShowTip_NanoAppear()`
  （void 显示Tip_纳米Appear（））
- `void UpdateCharacterModel(Player player)`
  （void 更新角色模型（玩家 player））
- `void UpdateNanoRole(Player player, NanoRole newRole)`
  （void 更新纳米Role（玩家 player, 纳米角色 newRole））
- `void UpdateNanoRole(Player player)`
  （void 更新纳米Role（玩家 player））
- `void CalBornNanoGhostHP()`
  （void Cal出生纳米幽灵HP（））
- `void SetBornNanoGhostHP(Player player, NanoRole role)`
  （void 集合出生纳米幽灵HP（玩家 player, 纳米角色 role））
- `void PlayChangeFX(Player player)`
  （void 播放ChangeFX（玩家 player））
- `void BecomeSoldider(Player player, bool isRoundReset = True)`
  （void BecomeSoldider（玩家 player, bool isRoundReset = True））
- `void DeathEvent(DeathEventData eventData)`
  （void 死亡事件（死亡事件数据 eventData））
- `void RespawnPlayer(Player dead, int respawnTime, bool isNormalRespawn, bool clearExp)`
  （void 重生玩家（玩家 dead, int respawnTime, bool isNormalRespawn, bool clearExp））
- `void SpawnEvent(Player player)`
  （void 出生事件（玩家 player））
- `bool GetShouldResetDeadNanoGhostExp(Player player)`
  （bool 获取应该重置Dead纳米幽灵Exp（玩家 player））
- `void ResetNanoGhostExpAndHp(Player player)`
  （void 重置纳米幽灵ExpAndHp（玩家 player））
- `void InvalidDmgCheck(ref DamageEventData eventData)`
  （void InvalidDmg检查（ref DamageEventData eventData））
- `void PreDamageEvent(ref DamageEventData eventData)`
  （void Pre伤害事件（ref DamageEventData eventData））
- `void PlayNanoClothMark(Texture markTex)`
  （void 播放纳米服装Mark（纹理 markTex））
- `void PostDamageEvent(ref DamageEventData eventData)`
  （void Post伤害事件（ref DamageEventData eventData））
- `float CalKnifeDmg(NanoRole attackerRole, float baseDmg, DamageTag damageTag, int attackerLevel)`
  （float Cal近战武器Dmg（纳米角色 attackerRole, float baseDmg, 伤害标签 damageTag, int attackerLevel））
- `void InfectEvent(Player nanoGhost, Player soldier)`
  （void Infect事件（玩家 nanoGhost, 玩家 soldier））
- `void ShowTip_Infected()`
  （void 显示Tip_Infected（））
- `void AddInfectScore(Player nanoGhost, Player soldier)`
  （void 添加Infect分数（玩家 nanoGhost, 玩家 soldier））
- `void SetInfectedHP(Player nanoGhost, Player soldier)`
  （void 集合InfectedHP（玩家 nanoGhost, 玩家 soldier））
- `void AddInfectExp(Player nanoGhost)`
  （void 添加InfectExp（玩家 nanoGhost））
- `void CheckRoundOver()`
  （void 检查回合Over（））
- `void OnTimeOut()`
  （void On时间Out（））
- `void SoldierWin()`
  （void SoldierWin（））
- `void AddSoldierWinScore()`
  （void 添加SoldierWin分数（））
- `void GhostWin()`
  （void 幽灵Win（））
- `void AddGhostWinScore()`
  （void 添加幽灵Win分数（））
- `void StartGenerateSupplyBox()`
  （void 开始GenerateSupplyBox（））
- `void GenerateSupplyBox(int count)`
  （void GenerateSupplyBox（int count））
- `void OnSupplyBoxArrive()`
  （void OnSupplyBoxArrive（））
- `void AddNanoGhostExp(Player player, int addValue)`
  （void 添加纳米幽灵Exp（玩家 player, int addValue））
- `void SetNanoGhostExp(Player player, int exp)`
  （void 集合纳米幽灵Exp（玩家 player, int exp））
- `void NanoGhostLevelUp(Player player)`
  （void 纳米幽灵等级上（玩家 player））
- `void GiveLevelUpBonusHp(Player player)`
  （void Give等级上奖励的Hp（玩家 player））
- `void PlayAppearSound(NanoRole role)`
  （void 播放Appear音效（纳米角色 role））
- `void SetSkill(Player player)`
  （void 集合技能（玩家 player））
- `void RemoveSkill(Player player, NanoRole oldRole)`
  （void 移除技能（玩家 player, 纳米角色 oldRole））
- `bool TryUseSkill(Player player)`
  （bool TryUse技能（玩家 player））
- `int GetSkillHPcost(Player player)`
  （int 获取技能HPcost（玩家 player））
- `float ModifyNanoSkillColdTime(float input)`
  （float Modify纳米技能Cold时间（float input））
- `bool NanoGhostSkill(Player player)`
  （bool 纳米幽灵技能（玩家 player））
- `bool NurseSkill(Player player)`
  （bool Nurse技能（玩家 player））
- `bool TerminatorSkill(Player player)`
  （bool Terminator技能（玩家 player））
- `bool DemonTerminatorSkill(Player player)`
  （bool DemonTerminator技能（玩家 player））
- `void PlaySkillSND(NanoRole nanoRole)`
  （void 播放技能SND（纳米角色 nanoRole））
- `void ShowTip_GetSkill()`
  （void 显示Tip_获取技能（））
- `void PlayHpRecoverFX(CharacterModel.Sex sex)`
  （void 播放Hp恢复FX（角色Model.Sex sex））
- `void SetNanoClothUI(int count)`
  （void 集合纳米服装界面（int count））
- `void OnPlayerPickUpSupplyBox(Player player, SupplyBox.Type boxType)`
  （void On玩家Pick上SupplyBox（玩家 player, SupplyBox.类型 boxType））
- `bool CheckNanoClothMax(Player player)`
  （bool 检查纳米服装最大（玩家 player））
- `void ShowTip_SupplyBoxArrive(string msg)`
  （void 显示Tip_SupplyBoxArrive（string msg））
- `void ShowTip_GetSupply(string msg)`
  （void 显示Tip_获取Supply（string msg））
- `void ShowTip_MeleeKillNano(string msg)`
  （void 显示Tip_Melee击杀纳米（string msg））
- `void ShowTip_HeroReady(string msg)`
  （void 显示Tip_英雄Ready（string msg））
- `void ShowTip_HpNotEnough()`
  （void 显示Tip_HpNotEnough（））
- `void ShowSupplyBoxTip(string msg)`
  （void 显示SupplyBoxTip（string msg））
- `void ShowNanoTimerTip(string msg)`
  （void 显示纳米计时器Tip（string msg））
- `void ShowMeleeKillNanoTip(string msg)`
  （void 显示Melee击杀纳米Tip（string msg））
- `void KillMarkEvent(ref HUD_KillMark.EventData evtData)`
  （void 击杀Mark事件（ref HUD_KillMark.EventData evtData））
- `void DrawNanoKillMark(NanoRole role, int multiKill)`
  （void Draw纳米击杀Mark（纳米角色 role, int multiKill））
- `void AddSign(Player player)`
  （void 添加标志（玩家 player））
- `void OnNewPlayerJoin(Player newPlayer)`
  （void On新的玩家Join（玩家 newPlayer））
- `void AddAbsorbFuction(Player newPlayer)`
  （void 添加AbsorbFuction（玩家 newPlayer））
- `void AbsorbFunction(Player player, KeyInputState keyState)`
  （void AbsorbFunction（玩家 player, 按键输入状态 keyState））
- `void ChangeNanoGhostType(Player player, NanoRole role)`
  （void Change纳米幽灵类型（玩家 player, 纳米角色 role））
- `void AddNanoGhostItemBonusHP(Player player)`
  （void 添加纳米幽灵项目奖励的HP（玩家 player））

---

## Mode_DeathMatch（Mode_死亡比赛）

**继承**: ModeBase（模式基础）

### 字段 (2)

- `bool firstKill`（bool first击杀）(偏移: 0x74)
- `GameObject invinsibleGauge`（游戏对象 invinsibleGauge）(偏移: 0x78)

### 方法 (8)

- `void Update()`
  （void 更新（））
- `void Start()`
  （void 开始（））
- `void OnMyPlayerJoin(Player myPlayer)`
  （void OnMy玩家Join（玩家 myPlayer））
- `void OnMyKillChange(int oldKill, int newKill)`
  （void OnMy击杀Change（int oldKill, int newKill））
- `void DeathEvent(DeathEventData eventData)`
  （void 死亡事件（死亡事件数据 eventData））
- `void OnTimeOut()`
  （void On时间Out（））
- `void GameOver()`
  （void 游戏Over（））
- `SpecialKillType FirstAndLastKillCheck(Entity killer, Entity dead)`
  （特殊击杀类型 第一个And最后一个击杀检查（实体 killer, 实体 dead））

---

## Mode_Nano4（Mode_Nano4）

**继承**: ModeBase_Nano（模式Base_纳米）

### 字段 (9)

- `Vector2 supplyArriveTip_Pos`（二维向量 supplyArriveTip_Pos）(偏移: 0x4)
- `Vector2 supplyGetTip_Pos`（二维向量 supply获取Tip_Pos）(偏移: 0xC)
- `CommonHud_1 terminatorMsg`（CommonHud_1 terminatorMsg）(偏移: 0xB8)
- `CommonHud_1 characterMark`（CommonHud_1 characterMark）(偏移: 0xBC)
- `HUD_Nano4_HumanGauge humanGauge`（HUD_Nano4_人类Gauge humanGauge）(偏移: 0xC0)
- `CommonHud_1 becomeHeroKeyTip`（CommonHud_1 become英雄键Tip）(偏移: 0xC4)
- `Vector2 heroKeyTip_Pos`（二维向量 hero键Tip_Pos）(偏移: 0x14)
- `int[] heroNeedDeadSoldier`（int[] hero需要DeadSoldier）(偏移: 0x1C)
- `bool isVariant`（bool is变异体）(偏移: 0xC8)

### 方法 (30)

- `Mode_Nano4 get_instance3()`
  （Mode_Nano4 get_instance3（））
- `void set_instance3(Mode_Nano4 value)`
  （void set_instance3（Mode_Nano4 value））
- `bool get_isHeroReady()`
  （bool get_is英雄Ready（））
- `void Awake()`
  （void Awake（））
- `void OnDestroy()`
  （void On销毁（））
- `void OnNewPlayerJoin(Player player)`
  （void On新的玩家Join（玩家 player））
- `void OnStartNewGameRound()`
  （void On开始新的游戏回合（））
- `void GenerateNanoGhost()`
  （void Generate纳米幽灵（））
- `int GetHeroAppearNeedDeadSoldierCount()`
  （int 获取英雄Appear需要DeadSoldier数量（））
- `void GenerateTerminator()`
  （void GenerateTerminator（））
- `int GetTerminatorCount()`
  （int 获取Terminator数量（））
- `NanoRole GetBornTerminatorRole()`
  （纳米角色 获取出生TerminatorRole（））
- `void InfectEvent(Player nanoGhost, Player soldier)`
  （void Infect事件（玩家 nanoGhost, 玩家 soldier））
- `void TryAddDeadSoldierCount()`
  （void Try添加DeadSoldier数量（））
- `NanoRole GetHeroRole(Player player)`
  （纳米角色 获取英雄Role（玩家 player））
- `float CalKnifeDmg(NanoRole attackerRole, float baseDmg, DamageTag damageTag, int attackerLevel)`
  （float Cal近战武器Dmg（纳米角色 attackerRole, float baseDmg, 伤害标签 damageTag, int attackerLevel））
- `void TryBecomeHero(Player player, KeyInputState inputState)`
  （void TryBecome英雄（玩家 player, 按键输入状态 inputState））
- `void BecomeHero(Player player, NanoRole role, bool textTip)`
  （void Become英雄（玩家 player, 纳米角色 role, bool textTip））
- `void BecomeMasterTerminator(Player player, NanoRole role, bool textTip)`
  （void BecomeMasterTerminator（玩家 player, 纳米角色 role, bool textTip））
- `void AddHeroRadarIcon(Player player)`
  （void 添加英雄Radar图标（玩家 player））
- `void ShowTerminatorMsg(string msg)`
  （void 显示TerminatorMsg（string msg））
- `void ShowTip_GetSupply(string msg)`
  （void 显示Tip_获取Supply（string msg））
- `void ShowTip_SupplyBoxArrive(string msg)`
  （void 显示Tip_SupplyBoxArrive（string msg））
- `void ShowTip_GetSkill()`
  （void 显示Tip_获取技能（））
- `void DamageEvent(ref DamageEventData data)`
  （void 伤害事件（ref DamageEventData data））
- `void DeathEvent(DeathEventData eventData)`
  （void 死亡事件（死亡事件数据 eventData））
- `void AddExtraKillScore(Player killer, Player dead)`
  （void 添加额外的击杀分数（玩家 killer, 玩家 dead））
- `void PlayHeroDieSnd(NanoRole role)`
  （void 播放英雄DieSnd（纳米角色 role））
- `void AddInfectScore(Player nanoGhost, Player soldier)`
  （void 添加Infect分数（玩家 nanoGhost, 玩家 soldier））
- `void AddSoldierWinScore()`
  （void 添加SoldierWin分数（））

---

## Mode_Nano4_Terminator（Mode_Nano4_Terminator）

**继承**: Mode_Nano4（Mode_Nano4）

### 字段 (16)

- `Nano4TerminatorModeAsset realAsset`（Nano4Terminator模式资产 real资产）(偏移: 0xCC)
- `HUD_UpgradeBoxTip upgradeBoxTip`（HUD_UpgradeBoxTip upgradeBoxTip）(偏移: 0xD0)
- `CommonHud_1 nanoItemTip`（CommonHud_1 nano项目Tip）(偏移: 0xD4)
- `Nano4T_AttributeAsset attributeAsset`（Nano4T_Attribute资产 attribute资产）(偏移: 0xD8)
- `HUD_Nano4T_Attribute hud_Attribute`（HUD_Nano4T_Attribute hud_Attribute）(偏移: 0xDC)
- `Nano4T_Attribute attribute_Nano`（Nano4T_Attribute attribute_纳米）(偏移: 0xE0)
- `Nano4T_Attribute attribute_Human`（Nano4T_Attribute attribute_人类）(偏移: 0xE4)
- `bool isAttributeEnable`（bool isAttribute启用）(偏移: 0x0)
- `bool isBattleRound`（bool isBattle回合）(偏移: 0x1)
- `bool isBattleStart`（bool isBattle开始）(偏移: 0x2)
- `SimpleObjectPool tombstonePool`（Simple对象池 tombstone池）(偏移: 0xE8)
- `bool getSpecialWpn`（bool get特殊武器）(偏移: 0xEC)
- `List<int> ignoreDmgBuffWeapon`（List<int> ignoreDmg增益Weapon）(偏移: 0xF0)
- `int[] heroNeedDeadSoldier_30`（int[] hero需要DeadSoldier_30）(偏移: 0x4)
- `int[] upgradeBoxCount`（int[] upgradeBox数量）(偏移: 0x8)
- `bool nextNormalTerminator`（bool next法线Terminator）(偏移: 0xF4)

### 方法 (44)

- `void Awake()`
  （void Awake（））
- `void OnDestroy()`
  （void On销毁（））
- `void InitSetting()`
  （void 初始化设置（））
- `int GetHeroAppearNeedDeadSoldierCount()`
  （int 获取英雄Appear需要DeadSoldier数量（））
- `int GetTerminatorCount()`
  （int 获取Terminator数量（））
- `int GetNanoGhostCount()`
  （int 获取纳米幽灵数量（））
- `NanoRole GetBornTerminatorRole()`
  （纳米角色 获取出生TerminatorRole（））
- `bool GetShouldResetDeadNanoGhostExp(Player player)`
  （bool 获取应该重置Dead纳米幽灵Exp（玩家 player））
- `void OnSupplyBoxArrive()`
  （void OnSupplyBoxArrive（））
- `void OnPlayerPickUpSupplyBox(Player player, SupplyBox.Type boxType)`
  （void On玩家Pick上SupplyBox（玩家 player, SupplyBox.类型 boxType））
- `float CalKnifeDmg(NanoRole attackerRole, float baseDmg, DamageTag damageTag, int attackerLevel)`
  （float Cal近战武器Dmg（纳米角色 attackerRole, float baseDmg, 伤害标签 damageTag, int attackerLevel））
- `void OnStartNewGameRound()`
  （void On开始新的游戏回合（））
- `void BecomeSoldider(Player player, bool isRoundReset = True)`
  （void BecomeSoldider（玩家 player, bool isRoundReset = True））
- `void GenerateNanoGhost()`
  （void Generate纳米幽灵（））
- `void ShowTip_NanoAppear()`
  （void 显示Tip_纳米Appear（））
- `void StartGenerateSupplyBox()`
  （void 开始GenerateSupplyBox（））
- `void BecomeRandomMasterHero(Player target, bool deadToTerminator)`
  （void Become随机Master英雄（玩家 target, bool deadToTerminator））
- `void TryBecomeRandomMasterTerminator(Player target)`
  （void TryBecome随机MasterTerminator（玩家 target））
- `NanoRole GetHeroRole(Player player)`
  （纳米角色 获取英雄Role（玩家 player））
- `void SetBornNanoGhostHP(Player player, NanoRole role)`
  （void 集合出生纳米幽灵HP（玩家 player, 纳米角色 role））
- `void GiveLevelUpBonusHp(Player player)`
  （void Give等级上奖励的Hp（玩家 player））
- `void AddNanoGhostItemBonusHP(Player player)`
  （void 添加纳米幽灵项目奖励的HP（玩家 player））
- `int GetSkillHPcost(Player player)`
  （int 获取技能HPcost（玩家 player））
- `void DamageEvent(ref DamageEventData evtData)`
  （void 伤害事件（ref DamageEventData evtData））
- `void DeathEvent(DeathEventData evtData)`
  （void 死亡事件（死亡事件数据 evtData））
- `void SpawnEvent(Player player)`
  （void 出生事件（玩家 player））
- `void InfectEvent(Player nanoGhost, Player soldier)`
  （void Infect事件（玩家 nanoGhost, 玩家 soldier））
- `void AddInfectScore(Player nanoGhost, Player soldier)`
  （void 添加Infect分数（玩家 nanoGhost, 玩家 soldier））
- `void AddExtraKillScore(Player killer, Player dead)`
  （void 添加额外的击杀分数（玩家 killer, 玩家 dead））
- `float ModifyNanoSkillColdTime(float input)`
  （float Modify纳米技能Cold时间（float input））
- `void AddInfectExpLayer(Player player)`
  （void 添加InfectExp层（玩家 player））
- `bool CheckHumanDamageBuff(int wpnID, DamageTag dmgTag, DamageType dmgType)`
  （bool 检查人类伤害增益（int wpnID, 伤害标签 dmgTag, 伤害类型 dmgType））
- `bool CheckKillNanoBuff(int wpnID, DamageTag dmgTag, DamageType dmgType)`
  （bool 检查击杀纳米增益（int wpnID, 伤害标签 dmgTag, 伤害类型 dmgType））
- `bool CheckCriticalBuff(int wpnID, DamageTag dmgTag, DamageType dmgType)`
  （bool 检查Critical增益（int wpnID, 伤害标签 dmgTag, 伤害类型 dmgType））
- `void BecomeSavior(Player player)`
  （void BecomeSavior（玩家 player））
- `void RemoveSkill(Player player, NanoRole oldRole)`
  （void 移除技能（玩家 player, 纳米角色 oldRole））
- `void SetSkill(Player player)`
  （void 集合技能（玩家 player））
- `void AddPropertyModifier(Player newPlayer)`
  （void 添加属性修改器（玩家 newPlayer））
- `void RapidReload(Player player, ref float speed)`
  （void 快速换弹（玩家 player, ref float speed））
- `void NailExtraRange(Player player, ref float range)`
  （void Nail额外的范围（玩家 player, ref float range））
- `void OnGetGrenadeFromBag(Weapon wpn)`
  （void On获取手雷From背包（Weapon wpn））
- `void HotKnifeSpeed(Player player, ref float speed)`
  （void Hot近战武器Speed（玩家 player, ref float speed））
- `void MoveSpeedModifier(Player player, ref float speed)`
  （void 移动Speed修改器（玩家 player, ref float speed））
- `void RespawnPlayer(Player dead, int respawnTime, bool isNormalRespawn, bool clearExp)`
  （void 重生玩家（玩家 dead, int respawnTime, bool isNormalRespawn, bool clearExp））

---

## Mode_Nano6（Mode_Nano6）

**继承**: ModeBase_Nano（模式Base_纳米）

### 字段 (19)

- `Nano6ModeAsset realAsset`（Nano6模式资产 real资产）(偏移: 0xB8)
- `CommonHud_1 eventTip`（CommonHud_1 eventTip）(偏移: 0xBC)
- `CommonHud_1 levelUpTip`（CommonHud_1 level上Tip）(偏移: 0xC0)
- `CommonHud_1[] levelUpText`（CommonHud_1[] level上文本）(偏移: 0xC4)
- `Coroutine levelUpTextDraCoroutine`（协程 level上文本Dra协程）(偏移: 0xC8)
- `GameObject thermalVisionIcon`（游戏对象 thermalVision图标）(偏移: 0xCC)
- `CommonHud_1 skillTip`（CommonHud_1 skillTip）(偏移: 0xD0)
- `Image nanoClothCount`（图像 nano服装数量）(偏移: 0xD4)
- `HUD_ProjectionSign oneshineSign`（HUD_Projection标志 oneshine标志）(偏移: 0xD8)
- `AudioSource radio`（音频Source radio）(偏移: 0xE4)
- `List<Mode_Nano6.RadioMsg> radioPlayList`（List<Mode_Nano6.RadioMsg> radio播放列表）(偏移: 0xE8)
- `bool firstWaveSupplyBox`（bool firstWaveSupplyBox）(偏移: 0xEC)
- `bool firstInfect`（bool firstInfect）(偏移: 0x0)
- `bool firstMeleeKillNano`（bool firstMelee击杀纳米）(偏移: 0x0)
- `bool ghostBladeWillAppearTip`（bool ghost刀锋WillAppearTip）(偏移: 0x0)
- `SimpleObjectPool buffIconPool`（Simple对象池 buff图标池）(偏移: 0x0)
- `GameObject buffIconPrefab`（游戏对象 buff图标预制体）(偏移: 0xF4)
- `Transform[] buffIconTargets`（Transform[] buff图标Targets）(偏移: 0xF8)
- `int[] soldierLevelUpNeedExp`（int[] soldier等级上需要Exp）(偏移: 0x0)

### 方法 (49)

- `Mode_Nano6 get_instance3()`
  （Mode_Nano6 get_instance3（））
- `float get_soldierExp()`
  （float get_soldierExp（））
- `void set_soldierExp(float value)`
  （void set_soldierExp（float value））
- `int get_soldierLevel()`
  （int get_soldier等级（））
- `void set_soldierLevel(int value)`
  （void set_soldier等级（int value））
- `void Awake()`
  （void Awake（））
- `void Update()`
  （void 更新（））
- `void OnDestroy()`
  （void On销毁（））
- `void OnMyPlayerJoin(Player myPlayer)`
  （void OnMy玩家Join（玩家 myPlayer））
- `void InitSetting()`
  （void 初始化设置（））
- `void SetBornNanoGhostHP(Player player, NanoRole role)`
  （void 集合出生纳米幽灵HP（玩家 player, 纳米角色 role））
- `void InvalidDmgCheck(ref DamageEventData eventData)`
  （void InvalidDmg检查（ref DamageEventData eventData））
- `void InfectEvent(Player nanoGhost, Player soldier)`
  （void Infect事件（玩家 nanoGhost, 玩家 soldier））
- `void ShowTip_Infected()`
  （void 显示Tip_Infected（））
- `void AddInfectExp(Player nanoGhost)`
  （void 添加InfectExp（玩家 nanoGhost））
- `void SetInfectedHP(Player nanoGhost, Player soldier)`
  （void 集合InfectedHP（玩家 nanoGhost, 玩家 soldier））
- `void AddInfectScore(Player nanoGhost, Player soldier)`
  （void 添加Infect分数（玩家 nanoGhost, 玩家 soldier））
- `void PostDamageEvent(ref DamageEventData eventData)`
  （void Post伤害事件（ref DamageEventData eventData））
- `void DeathEvent(DeathEventData eventData)`
  （void 死亡事件（死亡事件数据 eventData））
- `bool GetShouldResetDeadNanoGhostExp(Player player)`
  （bool 获取应该重置Dead纳米幽灵Exp（玩家 player））
- `void OnStartNewGameRound()`
  （void On开始新的游戏回合（））
- `void StartGenerateSupplyBox()`
  （void 开始GenerateSupplyBox（））
- `void ShowTip_NanoAppear()`
  （void 显示Tip_纳米Appear（））
- `void OnMyPlayerBecomeNanoGhost(NanoRole oldRole, NanoRole newRole)`
  （void OnMy玩家Become纳米幽灵（纳米角色 oldRole, 纳米角色 newRole））
- `void OnSupplyBoxArrive()`
  （void OnSupplyBoxArrive（））
- `void ShowTip_SupplyBoxArrive(string msg)`
  （void 显示Tip_SupplyBoxArrive（string msg））
- `void ShowTip_GetSupply(string msg)`
  （void 显示Tip_获取Supply（string msg））
- `void SetSoldierExp(float exp)`
  （void 集合SoldierExp（float exp））
- `void SoldierLevelUp()`
  （void Soldier等级上（））
- `void AddSoldierMainWpnAmmo(int count)`
  （void 添加Soldier主要的武器弹药（int count））
- `bool BecomeGhostBlade(Player player)`
  （bool Become幽灵刀锋（玩家 player））
- `void NanoGhostLevelUp(Player player)`
  （void 纳米幽灵等级上（玩家 player））
- `bool BecomeArmoredTerminator(Player player)`
  （bool BecomeArmoredTerminator（玩家 player））
- `void SetNanoGhostHP(Player player)`
  （void 集合纳米幽灵HP（玩家 player））
- `void AddNanoGhostItemBonusHP(Player player)`
  （void 添加纳米幽灵项目奖励的HP（玩家 player））
- `void DrawLevelUpText(Nano6ModeAsset.UpgradeAsset upgradeAsset)`
  （void Draw等级上文本（Nano6模式Asset.Upgrade资产 upgradeAsset））
- `float CalKnifeDmg(NanoRole attackerRole, float baseDmg, DamageTag dmgTag, int attackerLevel)`
  （float Cal近战武器Dmg（纳米角色 attackerRole, float baseDmg, 伤害标签 dmgTag, int attackerLevel））
- `void ThermalVisionSetting()`
  （void ThermalVision设置（））
- `void SetNanoClothUI(int count)`
  （void 集合纳米服装界面（int count））
- `void OnPlayerPickUpSupplyBox(Player player, SupplyBox.Type boxType)`
  （void On玩家Pick上SupplyBox（玩家 player, SupplyBox.类型 boxType））
- `void AddRadioMsg(AudioClip audio, string msg, string attachMark)`
  （void 添加RadioMsg（音频弹匣 audio, string msg, string attachMark））
- `void RadioPlaying()`
  （void RadioPlaying（））
- `void GhostWin()`
  （void 幽灵Win（））
- `void AddGhostWinScore()`
  （void 添加幽灵Win分数（））
- `void SoldierWin()`
  （void SoldierWin（））
- `void AddSoldierWinScore()`
  （void 添加SoldierWin分数（））
- `string NumLerpAnim(int num, float duration)`
  （string NumLerp动画（int num, float duration））
- `void SetOneShineTarget(Transform target)`
  （void 集合OneShine目标（变换 target））
- `int GetSkillHPcost(Player player)`
  （int 获取技能HPcost（玩家 player））

---

## Mode_Nano6.RadioMsg（Mode_Nano6.RadioMsg）

### 字段 (3)

- `AudioClip audio`（音频弹匣 audio）(偏移: 0x0)
- `string message`（string message）(偏移: 0x4)
- `string attachMark`（string attachMark）(偏移: 0x8)

---

## Mode_TeamDeath（Mode_队伍死亡）

**继承**: ModeBase（模式基础）

### 字段 (6)

- `AudioClip remain10KillSound`（音频弹匣 remain10击杀音效）(偏移: 0x74)
- `CommonHud_1 remain10KillTip`（CommonHud_1 remain10击杀Tip）(偏移: 0x78)
- `GameObject invinsibleGauge`（游戏对象 invinsibleGauge）(偏移: 0x7C)
- `bool firstKill`（bool first击杀）(偏移: 0x80)
- `bool lastKill_BL`（bool lastKill_BL）(偏移: 0x81)
- `bool lastKill_GR`（bool lastKill_GR）(偏移: 0x82)

### 方法 (8)

- `void Start()`
  （void 开始（））
- `void OnMyPlayerJoin(Player myPlayer)`
  （void OnMy玩家Join（玩家 myPlayer））
- `void DeathEvent(DeathEventData eventData)`
  （void 死亡事件（死亡事件数据 eventData））
- `SpecialKillType FirstAndLastKillCheck(Entity killer, Entity dead)`
  （特殊击杀类型 第一个And最后一个击杀检查（实体 killer, 实体 dead））
- `void GameOver()`
  （void 游戏Over（））
- `void OnScoreReachTarget(bool left)`
  （void On分数Reach目标（bool left））
- `void OnTimeOut()`
  （void On时间Out（））
- `void Show10KillTip()`
  （void Show10击杀Tip（））

---

## Model（模型）

**继承**: RecyclableObject（Recyclable对象）

### 字段 (3)

- `List<GameObject> objectInPV`（List<游戏Object> objectIn第三人称视角）(偏移: 0x34)
- `List<GameObject> objectInCV`（List<游戏Object> objectIn第一人称视角）(偏移: 0x38)
- `List<Model.Socket> sockets`（List<Model.Socket> sockets）(偏移: 0x3C)

### 方法 (13)

- `Player get_owner()`
  （玩家 get_owner（））
- `void set_owner(Player value)`
  （void set_owner（玩家 value））
- `bool get_isActive()`
  （bool get_is激活的（））
- `void SetOwner(Player newOwner)`
  （void 集合Owner（玩家 newOwner））
- `void SetValidOwner()`
  （void 集合ValidOwner（））
- `void SetNullOwner()`
  （void 集合NullOwner（））
- `void RemoveFromOldOwner()`
  （void 移除From旧的Owner（））
- `void OnOwnerObserveModeChange(Model.Type mode)`
  （void OnOwner观察模式Change（Model.类型 mode））
- `void SetModelLayer(Model.Type mdlType, int layer)`
  （void 集合模型层（Model.类型 mdlType, int layer））
- `void Recycle(bool roundRecycle)`
  （void Recycle（bool roundRecycle））
- `void BindSocket(Transform tsf, string socketName)`
  （void Bind套接字（变换 tsf, string socketName））
- `void BindSocket(Transform tsf, string socketName, Vector3 offset, Vector3 euler)`
  （void Bind套接字（变换 tsf, string socketName, 三维向量 offset, 三维向量 euler））
- `void BindSocketInWorldSpace(Transform tsf, string socketName, Vector3 offset, Vector3 euler)`
  （void Bind套接字In世界的Space（变换 tsf, string socketName, 三维向量 offset, 三维向量 euler））

---

## Model.Socket（Model.套接字）

### 字段 (4)

- `string name`（string name）(偏移: 0x0)
- `Transform node`（变换 node）(偏移: 0x4)
- `Vector3 offset`（三维向量 offset）(偏移: 0x8)
- `Vector3 euler`（三维向量 euler）(偏移: 0x14)

---

## Model.Type（Model.类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Module（模块）

**继承**: ISerializable, ICustomAttributeProvider, _Module（ISerializable, I自定义的Attribute提供者, _模块）

### 字段 (9)

- `TypeFilter FilterTypeName`（类型Filter Filter类型名称）(偏移: 0x0)
- `TypeFilter FilterTypeNameIgnoreCase`（类型Filter Filter类型名称IgnoreCase）(偏移: 0x4)
- `IntPtr _impl`（整数Ptr _impl）(偏移: 0x8)
- `Assembly assembly`（Assembly assembly）(偏移: 0xC)
- `string fqname`（string fqname）(偏移: 0x10)
- `string name`（string name）(偏移: 0x14)
- `string scopename`（string scopename）(偏移: 0x18)
- `bool is_resource`（bool is_resource）(偏移: 0x1C)
- `int token`（int token）(偏移: 0x20)

### 方法 (16)

- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））
- `string ToString()`
  （string To字符串（））
- `Guid GetModuleVersionId()`
  （Guid 获取模块VersionId（））
- `bool filter_by_type_name(Type m, object filterCriteria)`
  （bool filter_by_type_name（类型 m, object filterCriteria））
- `bool filter_by_type_name_ignore_case(Type m, object filterCriteria)`
  （bool filter_by_type_name_ignore_case（类型 m, object filterCriteria））
- `string GetGuidInternal()`
  （string 获取Guid内部的（））
- `bool Equals(object o)`
  （bool Equals（object o））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool op_Equality(Module left, Module right)`
  （bool op_Equality（模块 left, 模块 right））
- `Assembly get_Assembly()`
  （Assembly get_Assembly（））
- `string get_ScopeName()`
  （string get_瞄准镜名称（））
- `Guid get_ModuleVersionId()`
  （Guid get_模块VersionId（））
- `Exception CreateNIE()`
  （Exception 创建NIE（））
- `bool IsResource()`
  （bool 是否资源（））
- `object[] GetCustomAttributes(Type attributeType, bool inherit)`
  （object[] 获取自定义的Attributes（类型 attributeType, bool inherit））
- `bool IsDefined(Type attributeType, bool inherit)`
  （bool 是否Defined（类型 attributeType, bool inherit））

---

## Monitor（Monitor）

### 方法 (20)

- `void Enter(object obj)`
  （void Enter（object obj））
- `void Enter(object obj, ref bool lockTaken)`
  （void Enter（object obj, ref bool lockTaken））
- `void ThrowLockTakenException()`
  （void 投掷LockTakenException（））
- `void Exit(object obj)`
  （void Exit（object obj））
- `bool TryEnter(object obj, int millisecondsTimeout)`
  （bool TryEnter（object obj, int millisecondsTimeout））
- `void TryEnter(object obj, int millisecondsTimeout, ref bool lockTaken)`
  （void TryEnter（object obj, int millisecondsTimeout, ref bool lockTaken））
- `bool Wait(object obj, int millisecondsTimeout, bool exitContext)`
  （bool Wait（object obj, int millisecondsTimeout, bool exitContext））
- `bool Wait(object obj, int millisecondsTimeout)`
  （bool Wait（object obj, int millisecondsTimeout））
- `void Pulse(object obj)`
  （void Pulse（object obj））
- `void PulseAll(object obj)`
  （void Pulse所有（object obj））
- `bool Monitor_test_synchronised(object obj)`
  （bool Monitor_test_synchronised（object obj））
- `void Monitor_pulse(object obj)`
  （void Monitor_pulse（object obj））
- `void ObjPulse(object obj)`
  （void ObjPulse（object obj））
- `void Monitor_pulse_all(object obj)`
  （void Monitor_pulse_all（object obj））
- `void ObjPulseAll(object obj)`
  （void ObjPulse所有（object obj））
- `bool Monitor_wait(object obj, int ms)`
  （bool Monitor_wait（object obj, int ms））
- `bool ObjWait(bool exitContext, int millisecondsTimeout, object obj)`
  （bool ObjWait（bool exitContext, int millisecondsTimeout, object obj））
- `void try_enter_with_atomic_var(object obj, int millisecondsTimeout, ref bool lockTaken)`
  （void try_enter_with_atomic_var（object obj, int millisecondsTimeout, ref bool lockTaken））
- `void ReliableEnterTimeout(object obj, int timeout, ref bool lockTaken)`
  （void ReliableEnter超时（object obj, int timeout, ref bool lockTaken））
- `void ReliableEnter(object obj, ref bool lockTaken)`
  （void ReliableEnter（object obj, ref bool lockTaken））

---

## MonoAssembly（MonoAssembly）

**继承**: RuntimeAssembly（RuntimeAssembly）

### 方法 (3)

- `Type GetType(string name, bool throwOnError, bool ignoreCase)`
  （类型 获取类型（string name, bool throwOnError, bool ignoreCase））
- `Module GetModule(string name)`
  （模块 获取模块（string name））
- `Module[] GetModules(bool getResourceModules)`
  （Module[] 获取Modules（bool getResourceModules））

---

## MonoAssemblyName（MonoAssembly名称）

### 字段 (13)

- `IntPtr name`（整数Ptr name）(偏移: 0x0)
- `IntPtr culture`（整数Ptr culture）(偏移: 0x4)
- `IntPtr hash_value`（整数Ptr hash_value）(偏移: 0x8)
- `IntPtr public_key`（整数Ptr public_key）(偏移: 0xC)
- `MonoAssemblyName.<public_key_token>e__FixedBuffer public_key_token`（MonoAssemblyName.<public_key_token>e__固定缓冲区 public_key_token）(偏移: 0x10)
- `uint hash_alg`（uint hash_alg）(偏移: 0x24)
- `uint hash_len`（uint hash_len）(偏移: 0x28)
- `uint flags`（uint flags）(偏移: 0x2C)
- `ushort major`（ushort major）(偏移: 0x30)
- `ushort minor`（ushort minor）(偏移: 0x32)
- `ushort build`（ushort build）(偏移: 0x34)
- `ushort revision`（ushort revision）(偏移: 0x36)
- `ushort arch`（ushort arch）(偏移: 0x38)

---

## MonoAsyncCall（Mono异步Call）

### 字段 (6)

- `object msg`（object msg）(偏移: 0x8)
- `IntPtr cb_method`（整数Ptr cb_method）(偏移: 0xC)
- `object cb_target`（object cb_target）(偏移: 0x10)
- `object state`（object state）(偏移: 0x14)
- `object res`（object res）(偏移: 0x18)
- `object out_args`（object out_args）(偏移: 0x1C)

---

## MonoBehaviour（MonoBehaviour行为）

**继承**: Behaviour（Behaviour）

### 方法 (28)

- `bool IsInvoking()`
  （bool 是否Invoking（））
- `void CancelInvoke()`
  （void 取消Invoke（））
- `void Invoke(string methodName, float time)`
  （void Invoke（string methodName, float time））
- `void InvokeRepeating(string methodName, float time, float repeatRate)`
  （void InvokeRepeating（string methodName, float time, float repeatRate））
- `void CancelInvoke(string methodName)`
  （void 取消Invoke（string methodName））
- `bool IsInvoking(string methodName)`
  （bool 是否Invoking（string methodName））
- `Coroutine StartCoroutine(string methodName)`
  （协程 开始协程（string methodName））
- `Coroutine StartCoroutine(string methodName, object value)`
  （协程 开始协程（string methodName, object value））
- `Coroutine StartCoroutine(IEnumerator routine)`
  （协程 开始协程（IEnumerator routine））
- `Coroutine StartCoroutine_Auto(IEnumerator routine)`
  （协程 开始Coroutine_自动（IEnumerator routine））
- `void StopCoroutine(IEnumerator routine)`
  （void 停止协程（IEnumerator routine））
- `void StopCoroutine(Coroutine routine)`
  （void 停止协程（协程 routine））
- `void StopCoroutine(string methodName)`
  （void 停止协程（string methodName））
- `void StopAllCoroutines()`
  （void 停止所有Coroutines（））
- `bool get_useGUILayout()`
  （bool get_useGUILayout（））
- `void set_useGUILayout(bool value)`
  （void set_useGUILayout（bool value））
- `void print(object message)`
  （void print（object message））
- `void Internal_CancelInvokeAll(MonoBehaviour self)`
  （void Internal_取消Invoke所有（MonoBehaviour行为 self））
- `bool Internal_IsInvokingAll(MonoBehaviour self)`
  （bool Internal_是否Invoking所有（MonoBehaviour行为 self））
- `void InvokeDelayed(MonoBehaviour self, string methodName, float time, float repeatRate)`
  （void InvokeDelayed（MonoBehaviour行为 self, string methodName, float time, float repeatRate））
- `void CancelInvoke(MonoBehaviour self, string methodName)`
  （void 取消Invoke（MonoBehaviour行为 self, string methodName））
- `bool IsInvoking(MonoBehaviour self, string methodName)`
  （bool 是否Invoking（MonoBehaviour行为 self, string methodName））
- `bool IsObjectMonoBehaviour(Object obj)`
  （bool 是否对象MonoBehaviour（对象 obj））
- `Coroutine StartCoroutineManaged(string methodName, object value)`
  （协程 开始协程Managed（string methodName, object value））
- `Coroutine StartCoroutineManaged2(IEnumerator enumerator)`
  （协程 开始协程Managed2（IEnumerator enumerator））
- `void StopCoroutineManaged(Coroutine routine)`
  （void 停止协程Managed（协程 routine））
- `void StopCoroutineFromEnumeratorManaged(IEnumerator routine)`
  （void 停止协程FromEnumeratorManaged（IEnumerator routine））
- `string GetScriptClassName()`
  （string 获取Script类名称（））

---

## MonoCMethod（MonoCMethod）

**继承**: RuntimeConstructorInfo（RuntimeConstructor信息）

### 字段 (3)

- `IntPtr mhandle`（整数Ptr mhandle）(偏移: 0x8)
- `string name`（string name）(偏移: 0xC)
- `Type reftype`（类型 reftype）(偏移: 0x10)

### 方法 (24)

- `MethodImplAttributes GetMethodImplementationFlags()`
  （MethodImplAttributes 获取MethodImplementationFlags（））
- `ParameterInfo[] GetParameters()`
  （ParameterInfo[] 获取Parameters（））
- `ParameterInfo[] GetParametersInternal()`
  （ParameterInfo[] 获取Parameters内部的（））
- `int GetParametersCount()`
  （int 获取Parameters数量（））
- `object InternalInvoke(object obj, object[] parameters, out Exception exc)`
  （object 内部的Invoke（object obj, object[] parameters, out Exception exc））
- `object Invoke(object obj, BindingFlags invokeAttr, Binder binder, object[] parameters, CultureInfo culture)`
  （object Invoke（object obj, BindingFlags invokeAttr, Binder binder, object[] parameters, Culture信息 culture））
- `object DoInvoke(object obj, BindingFlags invokeAttr, Binder binder, object[] parameters, CultureInfo culture)`
  （object DoInvoke（object obj, BindingFlags invokeAttr, Binder binder, object[] parameters, Culture信息 culture））
- `object InternalInvoke(object obj, object[] parameters)`
  （object 内部的Invoke（object obj, object[] parameters））
- `object Invoke(BindingFlags invokeAttr, Binder binder, object[] parameters, CultureInfo culture)`
  （object Invoke（BindingFlags invokeAttr, Binder binder, object[] parameters, Culture信息 culture））
- `RuntimeMethodHandle get_MethodHandle()`
  （RuntimeMethod句柄 get_Method句柄（））
- `MethodAttributes get_Attributes()`
  （MethodAttributes get_Attributes（））
- `CallingConventions get_CallingConvention()`
  （CallingConventions get_CallingConvention（））
- `bool get_ContainsGenericParameters()`
  （bool get_ContainsGenericParameters（））
- `Type get_ReflectedType()`
  （类型 get_Reflected类型（））
- `Type get_DeclaringType()`
  （类型 get_Declaring类型（））
- `string get_Name()`
  （string get_名称（））
- `bool IsDefined(Type attributeType, bool inherit)`
  （bool 是否Defined（类型 attributeType, bool inherit））
- `object[] GetCustomAttributes(bool inherit)`
  （object[] 获取自定义的Attributes（bool inherit））
- `object[] GetCustomAttributes(Type attributeType, bool inherit)`
  （object[] 获取自定义的Attributes（类型 attributeType, bool inherit））
- `MethodBody GetMethodBody()`
  （Method身体 获取Method身体（））
- `string ToString()`
  （string To字符串（））
- `IList<CustomAttributeData> GetCustomAttributesData()`
  （IList<自定义的AttributeData> 获取自定义的Attributes数据（））
- `int get_core_clr_security_level()`
  （int get_core_clr_security_level（））
- `bool get_IsSecurityCritical()`
  （bool get_是否SecurityCritical（））

---

## MonoCustomAttrs（Mono自定义的Attrs）

### 字段 (2)

- `Assembly corlib`（Assembly corlib）(偏移: 0x0)
- `AttributeUsageAttribute DefaultAttributeUsage`（AttributeUsageAttribute 默认的AttributeUsage）(偏移: 0x4)

### 方法 (16)

- `bool IsUserCattrProvider(object obj)`
  （bool 是否UserCattr提供者（object obj））
- `object[] GetCustomAttributesInternal(ICustomAttributeProvider obj, Type attributeType, bool pseudoAttrs)`
  （object[] 获取自定义的Attributes内部的（I自定义的Attribute提供者 obj, 类型 attributeType, bool pseudoAttrs））
- `object[] GetPseudoCustomAttributes(ICustomAttributeProvider obj, Type attributeType)`
  （object[] 获取Pseudo自定义的Attributes（I自定义的Attribute提供者 obj, 类型 attributeType））
- `object[] GetPseudoCustomAttributes(Type type)`
  （object[] 获取Pseudo自定义的Attributes（类型 type））
- `object[] GetCustomAttributesBase(ICustomAttributeProvider obj, Type attributeType, bool inheritedOnly)`
  （object[] 获取自定义的Attributes基础（I自定义的Attribute提供者 obj, 类型 attributeType, bool inheritedOnly））
- `object[] GetCustomAttributes(ICustomAttributeProvider obj, Type attributeType, bool inherit)`
  （object[] 获取自定义的Attributes（I自定义的Attribute提供者 obj, 类型 attributeType, bool inherit））
- `object[] GetCustomAttributes(ICustomAttributeProvider obj, bool inherit)`
  （object[] 获取自定义的Attributes（I自定义的Attribute提供者 obj, bool inherit））
- `CustomAttributeData[] GetCustomAttributesDataInternal(ICustomAttributeProvider obj)`
  （自定义的AttributeData[] 获取自定义的Attributes数据内部的（I自定义的Attribute提供者 obj））
- `IList<CustomAttributeData> GetCustomAttributesData(ICustomAttributeProvider obj)`
  （IList<自定义的AttributeData> 获取自定义的Attributes数据（I自定义的Attribute提供者 obj））
- `bool IsDefined(ICustomAttributeProvider obj, Type attributeType, bool inherit)`
  （bool 是否Defined（I自定义的Attribute提供者 obj, 类型 attributeType, bool inherit））
- `bool IsDefinedInternal(ICustomAttributeProvider obj, Type AttributeType)`
  （bool 是否Defined内部的（I自定义的Attribute提供者 obj, 类型 AttributeType））
- `PropertyInfo GetBasePropertyDefinition(MonoProperty property)`
  （属性信息 获取基础属性Definition（Mono属性 property））
- `EventInfo GetBaseEventDefinition(MonoEvent evt)`
  （事件信息 获取基础事件Definition（Mono事件 evt））
- `ICustomAttributeProvider GetBase(ICustomAttributeProvider obj)`
  （I自定义的Attribute提供者 获取基础（I自定义的Attribute提供者 obj））
- `AttributeUsageAttribute RetrieveAttributeUsageNoCache(Type attributeType)`
  （AttributeUsageAttribute RetrieveAttributeUsageNo缓存（类型 attributeType））
- `AttributeUsageAttribute RetrieveAttributeUsage(Type attributeType)`
  （AttributeUsageAttribute RetrieveAttributeUsage（类型 attributeType））

---

## MonoCustomAttrs.AttributeInfo（Mono自定义的Attrs.Attribute信息）

### 字段 (2)

- `AttributeUsageAttribute _usage`（AttributeUsageAttribute _usage）(偏移: 0x8)
- `int _inheritanceLevel`（int _inheritance等级）(偏移: 0xC)

### 方法 (2)

- `AttributeUsageAttribute get_Usage()`
  （AttributeUsageAttribute get_Usage（））
- `int get_InheritanceLevel()`
  （int get_Inheritance等级（））

---

## MonoEvent（Mono事件）

**继承**: RuntimeEventInfo（Runtime事件信息）

### 字段 (2)

- `IntPtr klass`（整数Ptr klass）(偏移: 0xC)
- `IntPtr handle`（整数Ptr handle）(偏移: 0x10)

### 方法 (11)

- `MethodInfo GetAddMethod(bool nonPublic)`
  （Method信息 获取添加Method（bool nonPublic））
- `MethodInfo GetRaiseMethod(bool nonPublic)`
  （Method信息 获取RaiseMethod（bool nonPublic））
- `MethodInfo GetRemoveMethod(bool nonPublic)`
  （Method信息 获取移除Method（bool nonPublic））
- `Type get_DeclaringType()`
  （类型 get_Declaring类型（））
- `Type get_ReflectedType()`
  （类型 get_Reflected类型（））
- `string get_Name()`
  （string get_名称（））
- `string ToString()`
  （string To字符串（））
- `bool IsDefined(Type attributeType, bool inherit)`
  （bool 是否Defined（类型 attributeType, bool inherit））
- `object[] GetCustomAttributes(bool inherit)`
  （object[] 获取自定义的Attributes（bool inherit））
- `object[] GetCustomAttributes(Type attributeType, bool inherit)`
  （object[] 获取自定义的Attributes（类型 attributeType, bool inherit））
- `IList<CustomAttributeData> GetCustomAttributesData()`
  （IList<自定义的AttributeData> 获取自定义的Attributes数据（））

---

## MonoEventInfo（Mono事件信息）

### 字段 (8)

- `Type declaring_type`（类型 declaring_type）(偏移: 0x0)
- `Type reflected_type`（类型 reflected_type）(偏移: 0x4)
- `string name`（string name）(偏移: 0x8)
- `MethodInfo add_method`（Method信息 add_method）(偏移: 0xC)
- `MethodInfo remove_method`（Method信息 remove_method）(偏移: 0x10)
- `MethodInfo raise_method`（Method信息 raise_method）(偏移: 0x14)
- `EventAttributes attrs`（事件Attributes attrs）(偏移: 0x18)
- `MethodInfo[] other_methods`（MethodInfo[] other_methods）(偏移: 0x1C)

### 方法 (2)

- `void get_event_info(MonoEvent ev, out MonoEventInfo info)`
  （void get_event_info（Mono事件 ev, out MonoEventInfo info））
- `MonoEventInfo GetEventInfo(MonoEvent ev)`
  （Mono事件信息 获取事件信息（Mono事件 ev））

---

## MonoField（MonoField）

**继承**: RtFieldInfo（RtField信息）

### 字段 (5)

- `IntPtr klass`（整数Ptr klass）(偏移: 0x8)
- `RuntimeFieldHandle fhandle`（RuntimeField句柄 fhandle）(偏移: 0xC)
- `string name`（string name）(偏移: 0x10)
- `Type type`（类型 type）(偏移: 0x14)
- `FieldAttributes attrs`（FieldAttributes attrs）(偏移: 0x18)

### 方法 (20)

- `FieldAttributes get_Attributes()`
  （FieldAttributes get_Attributes（））
- `RuntimeFieldHandle get_FieldHandle()`
  （RuntimeField句柄 get_Field句柄（））
- `Type ResolveType()`
  （类型 Resolve类型（））
- `Type get_FieldType()`
  （类型 get_Field类型（））
- `Type GetParentType(bool declaring)`
  （类型 获取父级类型（bool declaring））
- `Type get_ReflectedType()`
  （类型 get_Reflected类型（））
- `Type get_DeclaringType()`
  （类型 get_Declaring类型（））
- `string get_Name()`
  （string get_名称（））
- `bool IsDefined(Type attributeType, bool inherit)`
  （bool 是否Defined（类型 attributeType, bool inherit））
- `object[] GetCustomAttributes(bool inherit)`
  （object[] 获取自定义的Attributes（bool inherit））
- `object[] GetCustomAttributes(Type attributeType, bool inherit)`
  （object[] 获取自定义的Attributes（类型 attributeType, bool inherit））
- `int GetFieldOffset()`
  （int 获取FieldOffset（））
- `object GetValueInternal(object obj)`
  （object 获取值内部的（object obj））
- `object GetValue(object obj)`
  （object 获取值（object obj））
- `string ToString()`
  （string To字符串（））
- `void SetValueInternal(FieldInfo fi, object obj, object value)`
  （void 集合值内部的（Field信息 fi, object obj, object value））
- `void SetValue(object obj, object val, BindingFlags invokeAttr, Binder binder, CultureInfo culture)`
  （void 集合值（object obj, object val, BindingFlags invokeAttr, Binder binder, Culture信息 culture））
- `object GetRawConstantValue()`
  （object 获取RawConstant值（））
- `IList<CustomAttributeData> GetCustomAttributesData()`
  （IList<自定义的AttributeData> 获取自定义的Attributes数据（））
- `void CheckGeneric()`
  （void 检查Generic（））

---

## MonoFileType（Mono文件类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## MonoIO（MonoIO）

### 字段 (2)

- `IntPtr InvalidHandle`（整数Ptr Invalid句柄）(偏移: 0x0)
- `bool dump_handles`（bool dump_handles）(偏移: 0x4)

### 方法 (49)

- `Exception GetException(MonoIOError error)`
  （Exception 获取Exception（MonoIOError error））
- `Exception GetException(string path, MonoIOError error)`
  （Exception 获取Exception（string path, MonoIOError error））
- `bool CreateDirectory(char* path, out MonoIOError error)`
  （bool 创建Directory（char* path, out MonoIOError error））
- `bool CreateDirectory(string path, out MonoIOError error)`
  （bool 创建Directory（string path, out MonoIOError error））
- `bool RemoveDirectory(char* path, out MonoIOError error)`
  （bool 移除Directory（char* path, out MonoIOError error））
- `bool RemoveDirectory(string path, out MonoIOError error)`
  （bool 移除Directory（string path, out MonoIOError error））
- `string GetCurrentDirectory(out MonoIOError error)`
  （string 获取当前Directory（out MonoIOError error））
- `bool MoveFile(char* path, char* dest, out MonoIOError error)`
  （bool 移动文件（char* path, char* dest, out MonoIOError error））
- `bool MoveFile(string path, string dest, out MonoIOError error)`
  （bool 移动文件（string path, string dest, out MonoIOError error））
- `bool DeleteFile(char* path, out MonoIOError error)`
  （bool Delete文件（char* path, out MonoIOError error））
- `bool DeleteFile(string path, out MonoIOError error)`
  （bool Delete文件（string path, out MonoIOError error））
- `FileAttributes GetFileAttributes(char* path, out MonoIOError error)`
  （文件Attributes 获取文件Attributes（char* path, out MonoIOError error））
- `FileAttributes GetFileAttributes(string path, out MonoIOError error)`
  （文件Attributes 获取文件Attributes（string path, out MonoIOError error））
- `bool SetFileAttributes(char* path, FileAttributes attrs, out MonoIOError error)`
  （bool 集合文件Attributes（char* path, 文件Attributes attrs, out MonoIOError error））
- `bool SetFileAttributes(string path, FileAttributes attrs, out MonoIOError error)`
  （bool 集合文件Attributes（string path, 文件Attributes attrs, out MonoIOError error））
- `MonoFileType GetFileType(IntPtr handle, out MonoIOError error)`
  （Mono文件类型 获取文件类型（整数Ptr handle, out MonoIOError error））
- `MonoFileType GetFileType(SafeHandle safeHandle, out MonoIOError error)`
  （Mono文件类型 获取文件类型（Safe句柄 safeHandle, out MonoIOError error））
- `IntPtr FindFirstFile(char* pathWithPattern, out string fileName, out int fileAttr, out int error)`
  （整数Ptr 查找第一个文件（char* pathWithPattern, out string fileName, out int fileAttr, out int error））
- `IntPtr FindFirstFile(string pathWithPattern, out string fileName, out int fileAttr, out int error)`
  （整数Ptr 查找第一个文件（string pathWithPattern, out string fileName, out int fileAttr, out int error））
- `bool FindNextFile(IntPtr hnd, out string fileName, out int fileAttr, out int error)`
  （bool 查找下一个文件（整数Ptr hnd, out string fileName, out int fileAttr, out int error））
- `bool FindCloseFile(IntPtr hnd)`
  （bool 查找关闭文件（整数Ptr hnd））
- `bool Exists(string path, out MonoIOError error)`
  （bool Exists（string path, out MonoIOError error））
- `bool ExistsFile(string path, out MonoIOError error)`
  （bool Exists文件（string path, out MonoIOError error））
- `bool ExistsDirectory(string path, out MonoIOError error)`
  （bool ExistsDirectory（string path, out MonoIOError error））
- `bool ExistsSymlink(string path, out MonoIOError error)`
  （bool ExistsSymlink（string path, out MonoIOError error））
- `bool GetFileStat(char* path, out MonoIOStat stat, out MonoIOError error)`
  （bool 获取文件Stat（char* path, out MonoIOStat stat, out MonoIOError error））
- `bool GetFileStat(string path, out MonoIOStat stat, out MonoIOError error)`
  （bool 获取文件Stat（string path, out MonoIOStat stat, out MonoIOError error））
- `IntPtr Open(char* filename, FileMode mode, FileAccess access, FileShare share, FileOptions options, out MonoIOError error)`
  （整数Ptr 打开（char* filename, 文件模式 mode, 文件Access access, 文件Share share, 文件Options options, out MonoIOError error））
- `IntPtr Open(string filename, FileMode mode, FileAccess access, FileShare share, FileOptions options, out MonoIOError error)`
  （整数Ptr 打开（string filename, 文件模式 mode, 文件Access access, 文件Share share, 文件Options options, out MonoIOError error））
- `bool Close(IntPtr handle, out MonoIOError error)`
  （bool 关闭（整数Ptr handle, out MonoIOError error））
- `int Read(IntPtr handle, byte[] dest, int dest_offset, int count, out MonoIOError error)`
  （int Read（整数Ptr handle, byte[] dest, int dest_offset, int count, out MonoIOError error））
- `int Read(SafeHandle safeHandle, byte[] dest, int dest_offset, int count, out MonoIOError error)`
  （int Read（Safe句柄 safeHandle, byte[] dest, int dest_offset, int count, out MonoIOError error））
- `int Write(IntPtr handle, [In] byte[] src, int src_offset, int count, out MonoIOError error)`
  （int Write（整数Ptr handle, [In] byte[] src, int src_offset, int count, out MonoIOError error））
- `int Write(SafeHandle safeHandle, byte[] src, int src_offset, int count, out MonoIOError error)`
  （int Write（Safe句柄 safeHandle, byte[] src, int src_offset, int count, out MonoIOError error））
- `long Seek(IntPtr handle, long offset, SeekOrigin origin, out MonoIOError error)`
  （long Seek（整数Ptr handle, long offset, SeekOrigin origin, out MonoIOError error））
- `long Seek(SafeHandle safeHandle, long offset, SeekOrigin origin, out MonoIOError error)`
  （long Seek（Safe句柄 safeHandle, long offset, SeekOrigin origin, out MonoIOError error））
- `long GetLength(IntPtr handle, out MonoIOError error)`
  （long 获取Length（整数Ptr handle, out MonoIOError error））
- `long GetLength(SafeHandle safeHandle, out MonoIOError error)`
  （long 获取Length（Safe句柄 safeHandle, out MonoIOError error））
- `bool SetLength(IntPtr handle, long length, out MonoIOError error)`
  （bool 集合Length（整数Ptr handle, long length, out MonoIOError error））
- `bool SetLength(SafeHandle safeHandle, long length, out MonoIOError error)`
  （bool 集合Length（Safe句柄 safeHandle, long length, out MonoIOError error））
- `IntPtr get_ConsoleOutput()`
  （整数Ptr get_ConsoleOutput（））
- `IntPtr get_ConsoleInput()`
  （整数Ptr get_Console输入（））
- `IntPtr get_ConsoleError()`
  （整数Ptr get_ConsoleError（））
- `char get_VolumeSeparatorChar()`
  （char get_VolumeSeparatorChar（））
- `char get_DirectorySeparatorChar()`
  （char get_DirectorySeparatorChar（））
- `char get_AltDirectorySeparatorChar()`
  （char get_AltDirectorySeparatorChar（））
- `char get_PathSeparator()`
  （char get_路径Separator（））
- `void DumpHandles()`
  （void DumpHandles（））
- `bool RemapPath(string path, out string newPath)`
  （bool Remap路径（string path, out string newPath））

---

## MonoIOError（MonoIOError）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## MonoIOStat（MonoIOStat）

### 字段 (5)

- `FileAttributes fileAttributes`（文件Attributes fileAttributes）(偏移: 0x0)
- `long Length`（long Length）(偏移: 0x8)
- `long CreationTime`（long Creation时间）(偏移: 0x10)
- `long LastAccessTime`（long 最后一个Access时间）(偏移: 0x18)
- `long LastWriteTime`（long 最后一个Write时间）(偏移: 0x20)

---

## MonoListItem（Mono列表项目）

### 字段 (2)

- `MonoListItem next`（Mono列表项目 next）(偏移: 0x8)
- `object data`（object data）(偏移: 0xC)

---

## MonoMethod（MonoMethod）

**继承**: RuntimeMethodInfo（RuntimeMethod信息）

### 字段 (3)

- `IntPtr mhandle`（整数Ptr mhandle）(偏移: 0x8)
- `string name`（string name）(偏移: 0xC)
- `Type reftype`（类型 reftype）(偏移: 0x10)

### 方法 (34)

- `string get_name(MethodBase method)`
  （string get_name（Method基础 method））
- `MonoMethod get_base_method(MonoMethod method, bool definition)`
  （MonoMethod get_base_method（MonoMethod method, bool definition））
- `MethodInfo GetBaseMethod()`
  （Method信息 获取基础Method（））
- `Type get_ReturnType()`
  （类型 get_Return类型（））
- `MethodImplAttributes GetMethodImplementationFlags()`
  （MethodImplAttributes 获取MethodImplementationFlags（））
- `ParameterInfo[] GetParameters()`
  （ParameterInfo[] 获取Parameters（））
- `ParameterInfo[] GetParametersInternal()`
  （ParameterInfo[] 获取Parameters内部的（））
- `int GetParametersCount()`
  （int 获取Parameters数量（））
- `object InternalInvoke(object obj, object[] parameters, out Exception exc)`
  （object 内部的Invoke（object obj, object[] parameters, out Exception exc））
- `object Invoke(object obj, BindingFlags invokeAttr, Binder binder, object[] parameters, CultureInfo culture)`
  （object Invoke（object obj, BindingFlags invokeAttr, Binder binder, object[] parameters, Culture信息 culture））
- `void ConvertValues(Binder binder, object[] args, ParameterInfo[] pinfo, CultureInfo culture, BindingFlags invokeAttr)`
  （void 转换Values（Binder binder, object[] args, ParameterInfo[] pinfo, Culture信息 culture, BindingFlags invokeAttr））
- `RuntimeMethodHandle get_MethodHandle()`
  （RuntimeMethod句柄 get_Method句柄（））
- `MethodAttributes get_Attributes()`
  （MethodAttributes get_Attributes（））
- `CallingConventions get_CallingConvention()`
  （CallingConventions get_CallingConvention（））
- `Type get_ReflectedType()`
  （类型 get_Reflected类型（））
- `Type get_DeclaringType()`
  （类型 get_Declaring类型（））
- `string get_Name()`
  （string get_名称（））
- `bool IsDefined(Type attributeType, bool inherit)`
  （bool 是否Defined（类型 attributeType, bool inherit））
- `object[] GetCustomAttributes(bool inherit)`
  （object[] 获取自定义的Attributes（bool inherit））
- `object[] GetCustomAttributes(Type attributeType, bool inherit)`
  （object[] 获取自定义的Attributes（类型 attributeType, bool inherit））
- `void GetPInvoke(out PInvokeAttributes flags, out string entryPoint, out string dllName)`
  （void 获取PInvoke（out PInvokeAttributes flags, out string entryPoint, out string dllName））
- `object[] GetPseudoCustomAttributes()`
  （object[] 获取Pseudo自定义的Attributes（））
- `MethodInfo MakeGenericMethod(Type[] methodInstantiation)`
  （Method信息 MakeGenericMethod（Type[] methodInstantiation））
- `MethodInfo MakeGenericMethod_impl(Type[] types)`
  （Method信息 MakeGenericMethod_impl（Type[] types））
- `Type[] GetGenericArguments()`
  （Type[] 获取GenericArguments（））
- `MethodInfo GetGenericMethodDefinition_impl()`
  （Method信息 获取GenericMethodDefinition_impl（））
- `MethodInfo GetGenericMethodDefinition()`
  （Method信息 获取GenericMethodDefinition（））
- `bool get_IsGenericMethodDefinition()`
  （bool get_是否GenericMethodDefinition（））
- `bool get_IsGenericMethod()`
  （bool get_是否GenericMethod（））
- `bool get_ContainsGenericParameters()`
  （bool get_ContainsGenericParameters（））
- `MethodBody GetMethodBody()`
  （Method身体 获取Method身体（））
- `IList<CustomAttributeData> GetCustomAttributesData()`
  （IList<自定义的AttributeData> 获取自定义的Attributes数据（））
- `int get_core_clr_security_level()`
  （int get_core_clr_security_level（））
- `bool get_IsSecurityCritical()`
  （bool get_是否SecurityCritical（））

---

## MonoMethodInfo（MonoMethod信息）

### 字段 (5)

- `Type parent`（类型 parent）(偏移: 0x0)
- `Type ret`（类型 ret）(偏移: 0x4)
- `MethodAttributes attrs`（MethodAttributes attrs）(偏移: 0x8)
- `MethodImplAttributes iattrs`（MethodImplAttributes iattrs）(偏移: 0xC)
- `CallingConventions callconv`（CallingConventions callconv）(偏移: 0x10)

### 方法 (10)

- `void get_method_info(IntPtr handle, out MonoMethodInfo info)`
  （void get_method_info（整数Ptr handle, out MonoMethodInfo info））
- `int get_method_attributes(IntPtr handle)`
  （int get_method_attributes（整数Ptr handle））
- `MonoMethodInfo GetMethodInfo(IntPtr handle)`
  （MonoMethod信息 获取Method信息（整数Ptr handle））
- `Type GetDeclaringType(IntPtr handle)`
  （类型 获取Declaring类型（整数Ptr handle））
- `Type GetReturnType(IntPtr handle)`
  （类型 获取Return类型（整数Ptr handle））
- `MethodAttributes GetAttributes(IntPtr handle)`
  （MethodAttributes 获取Attributes（整数Ptr handle））
- `CallingConventions GetCallingConvention(IntPtr handle)`
  （CallingConventions 获取CallingConvention（整数Ptr handle））
- `MethodImplAttributes GetMethodImplementationFlags(IntPtr handle)`
  （MethodImplAttributes 获取MethodImplementationFlags（整数Ptr handle））
- `ParameterInfo[] get_parameter_info(IntPtr handle, MemberInfo member)`
  （ParameterInfo[] get_parameter_info（整数Ptr handle, Member信息 member））
- `ParameterInfo[] GetParametersInfo(IntPtr handle, MemberInfo member)`
  （ParameterInfo[] 获取Parameters信息（整数Ptr handle, Member信息 member））

---

## MonoMethodMessage（MonoMethodMessage）

**继承**: IMethodCallMessage, IMethodMessage, IMessage, IMethodReturnMessage, IInternalMessage（IMethodCallMessage, IMethodMessage, IMessage, IMethodReturnMessage, I内部的Message）

### 字段 (15)

- `MonoMethod method`（MonoMethod method）(偏移: 0x8)
- `object[] args`（object[] args）(偏移: 0xC)
- `string[] names`（string[] names）(偏移: 0x10)
- `byte[] arg_types`（byte[] arg_types）(偏移: 0x14)
- `LogicalCallContext ctx`（LogicalCallContext ctx）(偏移: 0x18)
- `object rval`（object rval）(偏移: 0x1C)
- `Exception exc`（Exception exc）(偏移: 0x20)
- `AsyncResult asyncResult`（异步Result asyncResult）(偏移: 0x24)
- `CallType call_type`（Call类型 call_type）(偏移: 0x28)
- `string uri`（string uri）(偏移: 0x2C)
- `MCMDictionary properties`（MCM字典 properties）(偏移: 0x30)
- `Type[] methodSignature`（Type[] methodSignature）(偏移: 0x34)
- `Identity identity`（Identity identity）(偏移: 0x38)
- `string CallContextKey`（string CallContext键）(偏移: 0x0)
- `string UriKey`（string Uri键）(偏移: 0x4)

### 方法 (21)

- `void InitMessage(MonoMethod method, object[] out_args)`
  （void 初始化Message（MonoMethod method, object[] out_args））
- `MethodInfo GetMethodInfo(Type type, string methodName)`
  （Method信息 获取Method信息（类型 type, string methodName））
- `IDictionary get_Properties()`
  （I字典 get_Properties（））
- `int get_ArgCount()`
  （int get_Arg数量（））
- `object[] get_Args()`
  （object[] get_Args（））
- `LogicalCallContext get_LogicalCallContext()`
  （LogicalCallContext get_LogicalCallContext（））
- `void set_LogicalCallContext(LogicalCallContext value)`
  （void set_LogicalCallContext（LogicalCallContext value））
- `MethodBase get_MethodBase()`
  （Method基础 get_Method基础（））
- `string get_MethodName()`
  （string get_Method名称（））
- `object get_MethodSignature()`
  （object get_MethodSignature（））
- `string get_TypeName()`
  （string get_类型名称（））
- `string get_Uri()`
  （string get_Uri（））
- `void set_Uri(string value)`
  （void set_Uri（string value））
- `object GetArg(int arg_num)`
  （object 获取Arg（int arg_num））
- `Exception get_Exception()`
  （Exception get_Exception（））
- `int get_OutArgCount()`
  （int get_OutArg数量（））
- `object[] get_OutArgs()`
  （object[] get_OutArgs（））
- `object get_ReturnValue()`
  （object get_Return值（））
- `AsyncResult get_AsyncResult()`
  （异步Result get_异步Result（））
- `CallType get_CallType()`
  （Call类型 get_Call类型（））
- `bool NeedsOutProcessing(out int outCount)`
  （bool NeedsOutProcessing（out int outCount））

---

## MonoModifier（Mono修改器）

**继承**: VersionedMonoBehaviour, IPathModifier（VersionedMonoBehaviour, I路径修改器）

### 字段 (1)

- `Seeker seeker`（Seeker seeker）(偏移: 0x10)

### 方法 (3)

- `void OnEnable()`
  （void On启用（））
- `void OnDisable()`
  （void On禁用（））
- `void PreProcess(Path path)`
  （void Pre处理（路径 path））

---

## MonoModule（Mono模块）

**继承**: RuntimeModule（Runtime模块）

### 方法 (8)

- `Assembly get_Assembly()`
  （Assembly get_Assembly（））
- `string get_ScopeName()`
  （string get_瞄准镜名称（））
- `Guid get_ModuleVersionId()`
  （Guid get_模块VersionId（））
- `bool IsResource()`
  （bool 是否资源（））
- `object[] GetCustomAttributes(Type attributeType, bool inherit)`
  （object[] 获取自定义的Attributes（类型 attributeType, bool inherit））
- `bool IsDefined(Type attributeType, bool inherit)`
  （bool 是否Defined（类型 attributeType, bool inherit））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））
- `RuntimeAssembly GetRuntimeAssembly()`
  （RuntimeAssembly 获取RuntimeAssembly（））

---

## MonoParameterInfo（MonoParameter信息）

**继承**: RuntimeParameterInfo（RuntimeParameter信息）

### 方法 (3)

- `object get_DefaultValue()`
  （object get_默认的值（））
- `object[] GetCustomAttributes(Type attributeType, bool inherit)`
  （object[] 获取自定义的Attributes（类型 attributeType, bool inherit））
- `bool IsDefined(Type attributeType, bool inherit)`
  （bool 是否Defined（类型 attributeType, bool inherit））

---

## MonoProperty（Mono属性）

**继承**: RuntimePropertyInfo（Runtime属性信息）

### 字段 (5)

- `IntPtr klass`（整数Ptr klass）(偏移: 0x8)
- `IntPtr prop`（整数Ptr prop）(偏移: 0xC)
- `MonoPropertyInfo info`（Mono属性信息 info）(偏移: 0x10)
- `PInfo cached`（P信息 cached）(偏移: 0x28)
- `MonoProperty.GetterAdapter cached_getter`（MonoProperty.Getter适配器 cached_getter）(偏移: 0x2C)

### 方法 (24)

- `void CachePropertyInfo(PInfo flags)`
  （void 缓存属性信息（P信息 flags））
- `PropertyAttributes get_Attributes()`
  （属性Attributes get_Attributes（））
- `bool get_CanRead()`
  （bool get_能否Read（））
- `bool get_CanWrite()`
  （bool get_能否Write（））
- `Type get_PropertyType()`
  （类型 get_属性类型（））
- `Type get_ReflectedType()`
  （类型 get_Reflected类型（））
- `Type get_DeclaringType()`
  （类型 get_Declaring类型（））
- `string get_Name()`
  （string get_名称（））
- `MethodInfo[] GetAccessors(bool nonPublic)`
  （MethodInfo[] 获取Accessors（bool nonPublic））
- `MethodInfo GetGetMethod(bool nonPublic)`
  （Method信息 获取获取Method（bool nonPublic））
- `ParameterInfo[] GetIndexParameters()`
  （ParameterInfo[] 获取索引Parameters（））
- `MethodInfo GetSetMethod(bool nonPublic)`
  （Method信息 获取集合Method（bool nonPublic））
- `object GetConstantValue()`
  （object 获取Constant值（））
- `object GetRawConstantValue()`
  （object 获取RawConstant值（））
- `bool IsDefined(Type attributeType, bool inherit)`
  （bool 是否Defined（类型 attributeType, bool inherit））
- `object[] GetCustomAttributes(bool inherit)`
  （object[] 获取自定义的Attributes（bool inherit））
- `object[] GetCustomAttributes(Type attributeType, bool inherit)`
  （object[] 获取自定义的Attributes（类型 attributeType, bool inherit））
- `MonoProperty.GetterAdapter CreateGetterDelegate(MethodInfo method)`
  （MonoProperty.Getter适配器 创建Getter委托（Method信息 method））
- `object GetValue(object obj, object[] index)`
  （object 获取值（object obj, object[] index））
- `object GetValue(object obj, BindingFlags invokeAttr, Binder binder, object[] index, CultureInfo culture)`
  （object 获取值（object obj, BindingFlags invokeAttr, Binder binder, object[] index, Culture信息 culture））
- `void SetValue(object obj, object value, BindingFlags invokeAttr, Binder binder, object[] index, CultureInfo culture)`
  （void 集合值（object obj, object value, BindingFlags invokeAttr, Binder binder, object[] index, Culture信息 culture））
- `Type[] GetOptionalCustomModifiers()`
  （Type[] 获取Optional自定义的Modifiers（））
- `Type[] GetRequiredCustomModifiers()`
  （Type[] 获取Required自定义的Modifiers（））
- `IList<CustomAttributeData> GetCustomAttributesData()`
  （IList<自定义的AttributeData> 获取自定义的Attributes数据（））

---

## MonoProperty.GetterAdapter（MonoProperty.Getter适配器）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `object Invoke(object _this)`
  （object Invoke（object _this））
- `IAsyncResult BeginInvoke(object _this, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（object _this, 异步回调 callback, object object））
- `object EndInvoke(IAsyncResult result)`
  （object 结束Invoke（I异步Result result））

---

## MonoPropertyInfo（Mono属性信息）

### 字段 (6)

- `Type parent`（类型 parent）(偏移: 0x0)
- `Type declaring_type`（类型 declaring_type）(偏移: 0x4)
- `string name`（string name）(偏移: 0x8)
- `MethodInfo get_method`（Method信息 get_method）(偏移: 0xC)
- `MethodInfo set_method`（Method信息 set_method）(偏移: 0x10)
- `PropertyAttributes attrs`（属性Attributes attrs）(偏移: 0x14)

### 方法 (3)

- `void get_property_info(MonoProperty prop, ref MonoPropertyInfo info, PInfo req_info)`
  （void get_property_info（Mono属性 prop, ref MonoPropertyInfo info, P信息 req_info））
- `Type[] GetTypeModifiers(MonoProperty prop, bool optional)`
  （Type[] 获取类型Modifiers（Mono属性 prop, bool optional））
- `object get_default_value(MonoProperty prop)`
  （object get_default_value（Mono属性 prop））

---

## MonoTODOAttribute（MonoTODOAttribute）

**继承**: Attribute（Attribute）

### 字段 (1)

- `string comment`（string comment）(偏移: 0x8)

---

## MonoTypeInfo（Mono类型信息）

### 字段 (2)

- `string full_name`（string full_name）(偏移: 0x8)
- `MonoCMethod default_ctor`（MonoCMethod default_ctor）(偏移: 0xC)

---

## MonthNameStyles（Month名称Styles）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Motion（Motion）

**继承**: Object（对象）

### 方法 (1)

- `bool get_isLooping()`
  （bool get_isLooping（））

---

## MotionBlur（MotionBlur）

**继承**: VolumeComponent, IPostProcessComponent（Volume组件, IPost处理组件）

### 字段 (4)

- `MotionBlurModeParameter mode`（MotionBlur模式Parameter mode）(偏移: 0x1C)
- `MotionBlurQualityParameter quality`（MotionBlurQualityParameter quality）(偏移: 0x20)
- `ClampedFloatParameter intensity`（Clamped浮点数Parameter intensity）(偏移: 0x24)
- `ClampedFloatParameter clamp`（Clamped浮点数Parameter clamp）(偏移: 0x28)

### 方法 (2)

- `bool IsActive()`
  （bool 是否激活的（））
- `bool IsTileCompatible()`
  （bool 是否TileCompatible（））

---

## MotionBlurMode（MotionBlur模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## MotionBlurQuality（MotionBlurQuality）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## MousePositionDebug（鼠标PositionDebug）

### 字段 (1)

- `MousePositionDebug s_Instance`（鼠标PositionDebug s_实例）(偏移: 0x30AF30A3)

### 方法 (6)

- `MousePositionDebug get_instance()`
  （鼠标PositionDebug get_instance（））
- `void Build()`
  （void Build（））
- `void Cleanup()`
  （void 清理（））
- `Vector2 GetMousePosition(float ScreenHeight, bool sceneView)`
  （二维向量 获取鼠标Position（float ScreenHeight, bool sceneView））
- `Vector2 GetInputMousePosition()`
  （二维向量 获取输入鼠标Position（））
- `Vector2 GetMouseClickPosition(float ScreenHeight)`
  （二维向量 获取鼠标ClickPosition（float ScreenHeight））

---

## MoveDirection（移动方向）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## MovedFromAttribute（MovedFromAttribute）

**继承**: Attribute（Attribute）

### 字段 (1)

- `MovedFromAttributeData data`（MovedFromAttribute数据 data）(偏移: 0x8)

---

## MovedFromAttributeData（MovedFromAttribute数据）

### 字段 (7)

- `string className`（string class名称）(偏移: 0x0)
- `string nameSpace`（string nameSpace）(偏移: 0x4)
- `string assembly`（string assembly）(偏移: 0x8)
- `bool classHasChanged`（bool class是否有Changed）(偏移: 0xC)
- `bool nameSpaceHasChanged`（bool nameSpace是否有Changed）(偏移: 0xD)
- `bool assemblyHasChanged`（bool assembly是否有Changed）(偏移: 0xE)
- `bool autoUdpateAPI`（bool autoUdpateAPI）(偏移: 0xF)

### 方法 (1)

- `void Set(bool autoUpdateAPI, string sourceNamespace, string sourceAssembly, string sourceClassName)`
  （void 集合（bool autoUpdateAPI, string sourceNamespace, string sourceAssembly, string sourceClassName））

---

## MovementPlane（MovementPlane）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## MovementUtilities（MovementUtilities）

### 方法 (2)

- `Vector2 ClampVelocity(Vector2 velocity, float maxSpeed, float slowdownFactor, bool slowWhenNotFacingTarget, Vector2 forward)`
  （二维向量 Clamp速度（二维向量 velocity, float maxSpeed, float slowdownFactor, bool slowWhenNotFacingTarget, 二维向量 forward））
- `Vector2 CalculateAccelerationToReachPoint(Vector2 deltaPosition, Vector2 targetVelocity, Vector2 currentVelocity, float forwardsAcceleration, float rotationSpeed, float maxSpeed, Vector2 forwardsVector)`
  （二维向量 计算加速度ToReachPoint（二维向量 deltaPosition, 二维向量 targetVelocity, 二维向量 currentVelocity, float forwardsAcceleration, float rotationSpeed, float maxSpeed, 二维向量 forwardsVector））

---

## MsaaQuality（MsaaQuality）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Msl_Arcane（Msl_Arcane）

**继承**: WPN_GRENADE（WPN_GRENADE）

### 方法 (1)

- `DamageEventData GetBasicDamageEventData()`
  （伤害事件数据 获取Basic伤害事件数据（））

---

## Msl_EvilFire（Msl_Evil开火）

**继承**: WPN_GRENADE（WPN_GRENADE）

### 字段 (3)

- `Transform ball`（变换 ball）(偏移: 0x7C)
- `SphereCollider enemyTrigger`（Sphere碰撞器 enemy触发器）(偏移: 0x80)
- `float powerProgress`（float powerProgress）(偏移: 0x84)

### 方法 (2)

- `void SetProgress(float progress)`
  （void 集合Progress（float progress））
- `void PlayExpEffect()`
  （void 播放Exp特效（））

---

## MultiKillTimer（多杀计时器）

### 字段 (3)

- `int multiKill`（int multi击杀）(偏移: 0x8)
- `float breakTime`（float break时间）(偏移: 0xC)
- `float maxInterval`（float max间隔）(偏移: 0x0)

### 方法 (4)

- `void Add()`
  （void 添加（））
- `int Get()`
  （int 获取（））
- `void Check()`
  （void 检查（））
- `void Break()`
  （void Break（））

---

## MultiTargetPath（多个目标路径）

**继承**: ABPath（AB路径）

### 字段 (12)

- `OnPathDelegate[] callbacks`（On路径Delegate[] callbacks）(偏移: 0xCC)
- `GraphNode[] targetNodes`（GraphNode[] targetNodes）(偏移: 0xD0)
- `int targetNodeCount`（int target节点数量）(偏移: 0xD4)
- `bool[] targetsFound`（bool[] targetsFound）(偏移: 0xD8)
- `Vector3[] targetPoints`（Vector3[] targetPoints）(偏移: 0xDC)
- `Vector3[] originalTargetPoints`（Vector3[] original目标Points）(偏移: 0xE0)
- `List<Vector3>[] vectorPaths`（List<Vector3>[] vectorPaths）(偏移: 0xE4)
- `List<GraphNode>[] nodePaths`（List<GraphNode>[] nodePaths）(偏移: 0xE8)
- `bool pathsForAll`（bool pathsFor所有）(偏移: 0xEC)
- `int chosenTarget`（int chosen目标）(偏移: 0xF0)
- `int sequentialTarget`（int sequential目标）(偏移: 0xF4)
- `MultiTargetPath.HeuristicMode heuristicMode`（多个目标Path.Heuristic模式 heuristic模式）(偏移: 0xF8)

### 方法 (20)

- `bool get_inverted()`
  （bool get_inverted（））
- `void set_inverted(bool value)`
  （void set_inverted（bool value））
- `MultiTargetPath Construct(Vector3[] startPoints, Vector3 target, OnPathDelegate[] callbackDelegates, OnPathDelegate callback)`
  （多个目标路径 Construct（Vector3[] startPoints, 三维向量 target, On路径Delegate[] callbackDelegates, On路径委托 callback））
- `MultiTargetPath Construct(Vector3 start, Vector3[] targets, OnPathDelegate[] callbackDelegates, OnPathDelegate callback)`
  （多个目标路径 Construct（三维向量 start, Vector3[] targets, On路径Delegate[] callbackDelegates, On路径委托 callback））
- `void Setup(Vector3 start, Vector3[] targets, OnPathDelegate[] callbackDelegates, OnPathDelegate callback)`
  （void Setup（三维向量 start, Vector3[] targets, On路径Delegate[] callbackDelegates, On路径委托 callback））
- `void Reset()`
  （void 重置（））
- `void OnEnterPool()`
  （void OnEnter池（））
- `void ChooseShortestPath()`
  （void ChooseShortest路径（））
- `void SetPathParametersForReturn(int target)`
  （void 集合路径ParametersForReturn（int target））
- `void ReturnPath()`
  （void Return路径（））
- `void FoundTarget(PathNode nodeR, int i)`
  （void Found目标（路径节点 nodeR, int i））
- `void RebuildOpenList()`
  （void Rebuild打开列表（））
- `void Prepare()`
  （void Prepare（））
- `void RecalculateHTarget(bool firstTime)`
  （void RecalculateH目标（bool firstTime））
- `void Initialize()`
  （void 初始化（））
- `void Cleanup()`
  （void 清理（））
- `void ResetFlags()`
  （void 重置Flags（））
- `void CalculateStep(long targetTick)`
  （void 计算Step（long targetTick））
- `void Trace(PathNode node)`
  （void Trace（路径节点 node））
- `string DebugString(PathLog logMode)`
  （string Debug字符串（路径Log logMode））

---

## MultiTargetPath.HeuristicMode（多个目标Path.Heuristic模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## MulticastDelegate（Multicast委托）

**继承**: Delegate（委托）

### 字段 (1)

- `Delegate[] delegates`（Delegate[] delegates）(偏移: 0x34)

### 方法 (3)

- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（Serialization信息 info, StreamingContext context））
- `MethodInfo GetMethodImpl()`
  （Method信息 获取MethodImpl（））
- `int LastIndexOf(Delegate[] haystack, Delegate[] needle)`
  （int 最后一个索引Of（Delegate[] haystack, Delegate[] needle））

---

## MultilineAttribute（MultilineAttribute）

**继承**: PropertyAttribute（属性Attribute）

### 字段 (1)

- `int lines`（int lines）(偏移: 0x8)

---

## MultipleDisplayUtilities（MultipleDisplayUtilities）

### 方法 (2)

- `bool GetRelativeMousePositionForDrag(PointerEventData eventData, ref Vector2 position)`
  （bool 获取Relative鼠标PositionForDrag（指针事件数据 eventData, ref Vector2 position））
- `Vector2 GetMousePositionRelativeToMainDisplayResolution()`
  （二维向量 获取鼠标PositionRelativeTo主要的DisplayResolution（））

---

## NNConstraint（NNConstraint）

### 字段 (9)

- `GraphMask graphMask`（Graph掩码 graph掩码）(偏移: 0x8)
- `bool constrainArea`（bool constrainArea）(偏移: 0xC)
- `int area`（int area）(偏移: 0x10)
- `bool constrainWalkability`（bool constrainWalkability）(偏移: 0x14)
- `bool walkable`（bool walkable）(偏移: 0x0)
- `bool distanceXZ`（bool distanceXZ）(偏移: 0x0)
- `bool constrainTags`（bool constrainTags）(偏移: 0x0)
- `int tags`（int tags）(偏移: 0x0)
- `bool constrainDistance`（bool constrain距离）(偏移: 0x1C)

### 方法 (4)

- `bool SuitableGraph(int graphIndex, NavGraph graph)`
  （bool SuitableGraph（int graphIndex, NavGraph graph））
- `bool Suitable(GraphNode node)`
  （bool Suitable（Graph节点 node））
- `NNConstraint get_Default()`
  （NNConstraint get_默认的（））
- `NNConstraint get_None()`
  （NNConstraint get_无（））

---

## NNInfo（NN信息）

### 字段 (2)

- `GraphNode node`（Graph节点 node）(偏移: 0x0)
- `Vector3 position`（三维向量 position）(偏移: 0x4)

### 方法 (3)

- `Vector3 get_clampedPosition()`
  （三维向量 get_clampedPosition（））
- `Vector3 op_Explicit(NNInfo ob)`
  （三维向量 op_Explicit（NN信息 ob））
- `GraphNode op_Explicit(NNInfo ob)`
  （Graph节点 op_Explicit（NN信息 ob））

---

## NNInfoInternal（NN信息内部的）

### 字段 (4)

- `GraphNode node`（Graph节点 node）(偏移: 0x0)
- `GraphNode constrainedNode`（Graph节点 constrained节点）(偏移: 0x4)
- `Vector3 clampedPosition`（三维向量 clampedPosition）(偏移: 0x8)
- `Vector3 constClampedPosition`（三维向量 constClampedPosition）(偏移: 0x14)

### 方法 (1)

- `void UpdateInfo()`
  （void 更新信息（））

---

## NameCache（名称缓存）

### 字段 (1)

- `string name`（string name）(偏移: 0x8)

### 方法 (2)

- `object GetCachedValue(string name)`
  （object 获取Cached值（string name））
- `void SetCachedValue(object value)`
  （void 集合Cached值（object value））

---

## NameInfo（名称信息）

### 字段 (13)

- `string NIFullName`（string NI满名称）(偏移: 0x8)
- `long NIobjectId`（long NIobjectId）(偏移: 0x10)
- `long NIassemId`（long NIassemId）(偏移: 0x18)
- `InternalPrimitiveTypeE NIprimitiveTypeEnum`（内部的Primitive类型E NIprimitive类型Enum）(偏移: 0x20)
- `Type NItype`（类型 NItype）(偏移: 0x24)
- `bool NIisSealed`（bool NIisSealed）(偏移: 0x28)
- `bool NIisArray`（bool NIis数组）(偏移: 0x29)
- `bool NIisArrayItem`（bool NIis数组项目）(偏移: 0x2A)
- `bool NItransmitTypeOnObject`（bool NItransmit类型On对象）(偏移: 0x2B)
- `bool NItransmitTypeOnMember`（bool NItransmit类型OnMember）(偏移: 0x2C)
- `bool NIisParentTypeOnObject`（bool NIis父级类型On对象）(偏移: 0x2D)
- `InternalArrayTypeE NIarrayEnum`（内部的数组类型E NIarrayEnum）(偏移: 0x30)
- `bool NIsealedStatusChecked`（bool NIsealedStatusChecked）(偏移: 0x34)

### 方法 (4)

- `void Init()`
  （void 初始化（））
- `bool get_IsSealed()`
  （bool get_是否Sealed（））
- `string get_NIname()`
  （string get_NIname（））
- `void set_NIname(string value)`
  （void set_NIname（string value））

---

## NameInfo（名称信息）

**继承**: ConcurrentSetItem<KeyValuePair<string, EventTags>, NameInfo>（Concurrent集合Item<键值Pair<string, 事件Tags>, 名称Info>）

### 字段 (5)

- `int lastIdentity`（int lastIdentity）(偏移: 0x0)
- `string name`（string name）(偏移: 0x8)
- `EventTags tags`（事件Tags tags）(偏移: 0xC)
- `int identity`（int identity）(偏移: 0x10)
- `byte[] nameMetadata`（byte[] nameMetadata）(偏移: 0x14)

### 方法 (4)

- `void ReserveEventIDsBelow(int eventId)`
  （void Reserve事件IDsBelow（int eventId））
- `int Compare(NameInfo other)`
  （int Compare（名称信息 other））
- `int Compare(KeyValuePair<string, EventTags> key)`
  （int Compare（键值Pair<string, 事件Tags> key））
- `int Compare(string otherName, EventTags otherTags)`
  （int Compare（string otherName, 事件Tags otherTags））

---

## NameKeyPool（名称键池）

**继承**: ObjectPool（对象池）

### 字段 (1)

- `Hashtable hashtable`（Hashtable hashtable）(偏移: 0xC)

### 方法 (3)

- `void Recycle(RecyclableObject obj)`
  （void Recycle（Recyclable对象 obj））
- `RecyclableObject Get(GameObject prefab)`
  （Recyclable对象 获取（游戏对象 prefab））
- `RecyclableObject Get(string name)`
  （Recyclable对象 获取（string name））

---

## Nano4T_Attribute（Nano4T_Attribute）

### 字段 (5)

- `Nano4T_Attribute None`（Nano4T_Attribute 无）(偏移: 0x0)
- `string attributeName`（string attribute名称）(偏移: 0x8)
- `int id`（int id）(偏移: 0xC)
- `Sprite image`（精灵 image）(偏移: 0x10)
- `string description`（string description）(偏移: 0x14)

### 方法 (3)

- `string GetDescription(bool isNano, bool withName)`
  （string 获取Description（bool isNano, bool withName））
- `bool IsMax10()`
  （bool 是否Max10（））
- `bool IsSkillAttribute()`
  （bool 是否技能Attribute（））

---

## Nano4T_AttributeAsset（Nano4T_Attribute资产）

**继承**: ScriptableObject（脚本对象）

### 字段 (9)

- `Nano4T_AttributeAsset.Group normalRound`（Nano4T_AttributeAsset.组 normal回合）(偏移: 0xC)
- `Nano4T_AttributeAsset.Group battleRound`（Nano4T_AttributeAsset.组 battle回合）(偏移: 0x10)
- `Nano4T_Attribute[] attributes`（Nano4T_Attribute[] attributes）(偏移: 0x14)
- `GameObject SkillBtn_GoldShield`（游戏对象 技能Btn_GoldShield）(偏移: 0x18)
- `GameObject SFX_GoldShield`（游戏对象 SFX_GoldShield）(偏移: 0x1C)
- `GameObject FX_GoldShield`（游戏对象 FX_GoldShield）(偏移: 0x20)
- `GameObject SkillBtn_SPAgent`（游戏对象 技能Btn_SPAgent）(偏移: 0x24)
- `GameObject FX_SPAgent`（游戏对象 FX_SPAgent）(偏移: 0x28)
- `GameObject TombStone`（游戏对象 TombStone）(偏移: 0x2C)

### 方法 (9)

- `void Init()`
  （void 初始化（））
- `Nano4T_Attribute GetAttribute(bool isNano)`
  （Nano4T_Attribute 获取Attribute（bool isNano））
- `Nano4T_Attribute GetAttribute(int id)`
  （Nano4T_Attribute 获取Attribute（int id））
- `void SetSkill_GoldShield(Player player)`
  （void 集合Skill_GoldShield（玩家 player））
- `bool Skill_GoldShield(Player player)`
  （bool Skill_GoldShield（玩家 player））
- `BotSkillBase SkillAI_GoldShield(Bot bot)`
  （机器人技能基础 技能AI_GoldShield（机器人 bot））
- `void SetSkill_SPAgent(Player player)`
  （void 集合Skill_SPAgent（玩家 player））
- `bool Skill_SPAgent(Player player)`
  （bool Skill_SPAgent（玩家 player））
- `BotSkillBase SkillAI_SPAgent(Bot bot)`
  （机器人技能基础 技能AI_SPAgent（机器人 bot））

---

## Nano4T_AttributeAsset.Group（Nano4T_AttributeAsset.组）

### 字段 (2)

- `RandomItem nano`（随机项目 nano）(偏移: 0x8)
- `RandomItem human`（随机项目 human）(偏移: 0xC)

---

## Nano4T_Data（Nano4T_数据）

### 字段 (5)

- `SubscribeableProperty<int> humanLayer`（可订阅的Property<int> human层）(偏移: 0x8)
- `SubscribeableProperty<int> nanoLayer`（可订阅的Property<int> nano层）(偏移: 0xC)
- `SubscribeableProperty<int> pickUpBoxCount`（可订阅的Property<int> pick上Box数量）(偏移: 0x10)
- `bool canUseGrave`（bool canUseGrave）(偏移: 0x14)
- `int graveCount`（int grave数量）(偏移: 0x18)

### 方法 (10)

- `int get_Layer_Human()`
  （int get_Layer_人类（））
- `void set_Layer_Human(int value)`
  （void set_Layer_人类（int value））
- `int get_Layer_Nano()`
  （int get_Layer_纳米（））
- `void set_Layer_Nano(int value)`
  （void set_Layer_纳米（int value））
- `int get_Layer_Box()`
  （int get_Layer_Box（））
- `void set_Layer_Box(int value)`
  （void set_Layer_Box（int value））
- `void Clear()`
  （void 清除（））
- `bool TryUseGrave()`
  （bool TryUseGrave（））
- `int GetMaxCountOfBox(Player player)`
  （int 获取最大数量OfBox（玩家 player））
- `void ClearBoxLayer()`
  （void 清除Box层（））

---

## Nano4TerminatorModeAsset（Nano4Terminator模式资产）

**继承**: NanoModeAsset（纳米模式资产）

### 字段 (8)

- `AudioClip SND_UpgradeBox`（音频弹匣 SND_UpgradeBox）(偏移: 0x2C)
- `AudioClip SND_PickUpSupplyBox`（音频弹匣 SND_Pick上SupplyBox）(偏移: 0x30)
- `GameObject heroBox`（游戏对象 heroBox）(偏移: 0x34)
- `GameObject evilBox`（游戏对象 evilBox）(偏移: 0x38)
- `RandomItem nanoGhostSupplyBoxItems`（随机项目 nano幽灵SupplyBoxItems）(偏移: 0x3C)
- `Sprite[] nanoItemSprs`（Sprite[] nano项目Sprs）(偏移: 0x40)
- `GameObject FX_NanoShield`（游戏对象 FX_纳米Shield）(偏移: 0x44)
- `GameObject FX_NanoShield_PV`（游戏对象 FX_纳米Shield_PV）(偏移: 0x48)

---

## Nano6ModeAsset（Nano6模式资产）

**继承**: NanoModeAsset（纳米模式资产）

### 字段 (11)

- `AudioClip[] soldierRadio`（音频Clip[] soldierRadio）(偏移: 0x2C)
- `AudioClip[] nanoGhostRadio`（音频Clip[] nano幽灵Radio）(偏移: 0x30)
- `float[] soldierExpPerInfect`（float[] soldierExpPerInfect）(偏移: 0x34)
- `Nano6ModeAsset.UpgradeAsset up_Soldier_1`（Nano6模式Asset.Upgrade资产 up_Soldier_1）(偏移: 0x38)
- `Nano6ModeAsset.UpgradeAsset up_Soldier_2`（Nano6模式Asset.Upgrade资产 up_Soldier_2）(偏移: 0x44)
- `Nano6ModeAsset.UpgradeAsset up_Nano_1`（Nano6模式Asset.Upgrade资产 up_Nano_1）(偏移: 0x50)
- `Nano6ModeAsset.UpgradeAsset up_Nano_2`（Nano6模式Asset.Upgrade资产 up_Nano_2）(偏移: 0x5C)
- `Texture skillTip_GhostBlade`（纹理 skillTip_幽灵刀锋）(偏移: 0x68)
- `Texture skillTip_ArmoredTerminator`（纹理 skillTip_ArmoredTerminator）(偏移: 0x6C)
- `Sprite[] nanoClothCount`（Sprite[] nano服装数量）(偏移: 0x70)
- `AudioClip pickUpSupplyBox`（音频弹匣 pick上SupplyBox）(偏移: 0x74)

---

## Nano6ModeAsset.UpgradeAsset（Nano6模式Asset.Upgrade资产）

### 字段 (3)

- `Sprite[] textSprite`（Sprite[] text精灵）(偏移: 0x0)
- `Sprite[] iconSprite`（Sprite[] icon精灵）(偏移: 0x4)
- `Nano6ModeAsset.UpgradeAsset.TargetPos[] iconAnimTarget`（Nano6模式Asset.UpgradeAsset.目标Pos[] icon动画目标）(偏移: 0x8)

---

## Nano6ModeAsset.UpgradeAsset.TargetPos（Nano6模式Asset.UpgradeAsset.目标Pos）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## NanoGhostBreath（纳米幽灵Breath）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (4)

- `AudioSource audioSource`（音频Source audioSource）(偏移: 0xC)
- `AudioClip manBreath`（音频弹匣 manBreath）(偏移: 0x10)
- `AudioClip womanBreath`（音频弹匣 womanBreath）(偏移: 0x14)
- `bool isWoman`（bool isWoman）(偏移: 0x18)

### 方法 (3)

- `void Awake()`
  （void Awake（））
- `void Update()`
  （void 更新（））
- `void CheckSound(Player player)`
  （void 检查音效（玩家 player））

---

## NanoGuard（纳米Guard）

### 字段 (3)

- `Bot bot`（机器人 bot）(偏移: 0x8)
- `float nextChangePosTime`（float nextChangePos时间）(偏移: 0x18)
- `Vector3 escapePos`（三维向量 escapePos）(偏移: 0x20)

### 方法 (23)

- `bool get_isArriveArea()`
  （bool get_isArriveArea（））
- `void set_isArriveArea(bool value)`
  （void set_isArriveArea（bool value））
- `bool get_isArrivePos()`
  （bool get_isArrivePos（））
- `void set_isArrivePos(bool value)`
  （void set_isArrivePos（bool value））
- `Bot_NanoGuardArea get_guardArea()`
  （Bot_纳米GuardArea get_guardArea（））
- `void set_guardArea(Bot_NanoGuardArea value)`
  （void set_guardArea（Bot_纳米GuardArea value））
- `Bot_NanoGuardPos get_guardPos()`
  （Bot_纳米GuardPos get_guardPos（））
- `void set_guardPos(Bot_NanoGuardPos value)`
  （void set_guardPos（Bot_纳米GuardPos value））
- `bool get_isGoingGuardPos()`
  （bool get_isGoingGuardPos（））
- `NanoRole get_nanoRole()`
  （纳米角色 get_nanoRole（））
- `bool get_isEscaping()`
  （bool get_isEscaping（））
- `void set_isEscaping(bool value)`
  （void set_isEscaping（bool value））
- `void Bot_Getter_ZoomDirection(ref Vector3 zoomDir, ref int priority)`
  （void Bot_Getter_瞄准方向（ref Vector3 zoomDir, ref int priority））
- `void Bot_Destination_Listener(ref Vector3 pos, ref int priority)`
  （void Bot_Destination_监听器（ref Vector3 pos, ref int priority））
- `void Update()`
  （void 更新（））
- `void Clear()`
  （void 清除（））
- `void UpdateArea()`
  （void 更新Area（））
- `void RandomChangeGuardPos()`
  （void 随机ChangeGuardPos（））
- `void GoToSaferGuardPos()`
  （void GoToSaferGuardPos（））
- `void OnEnterArea()`
  （void OnEnterArea（））
- `void SetAreaTarget(Bot_NanoGuardArea targetArea)`
  （void 集合Area目标（Bot_纳米GuardArea targetArea））
- `void OnExitArea()`
  （void OnExitArea（））
- `void SetGuardPos(Bot_NanoGuardPos newPos)`
  （void 集合GuardPos（Bot_纳米GuardPos newPos））

---

## NanoKillType（纳米击杀类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## NanoModeAsset（纳米模式资产）

**继承**: ScriptableObject（脚本对象）

### 字段 (7)

- `int[] nanoGenerateCount`（int[] nanoGenerate数量）(偏移: 0xC)
- `string nanoTimerString`（string nano计时器字符串）(偏移: 0x10)
- `string nanoAppearString`（string nanoAppear字符串）(偏移: 0x14)
- `GameObject nanoChangeFX`（游戏对象 nanoChangeFX）(偏移: 0x18)
- `GameObject respawnFX`（游戏对象 respawnFX）(偏移: 0x1C)
- `GameObject supplyBox`（游戏对象 supplyBox）(偏移: 0x20)
- `RandomItem supplyBoxItems`（随机项目 supplyBoxItems）(偏移: 0x24)

### 方法 (1)

- `Texture GetMark(string markName)`
  （纹理 获取Mark（string markName））

---

## NanoModeBasicAsset（纳米模式Basic资产）

**继承**: ScriptableObject（脚本对象）

### 字段 (15)

- `AudioClip[] SND_Timer`（音频Clip[] SND_计时器）(偏移: 0xC)
- `AudioClip[] SND_RoundResult`（音频Clip[] SND_回合Result）(偏移: 0x10)
- `AudioClip SND_SupplyBoxArrive`（音频弹匣 SND_SupplyBoxArrive）(偏移: 0x14)
- `AudioClip[] SND_HpRecover`（音频Clip[] SND_Hp恢复）(偏移: 0x18)
- `List<NanoModeBasicAsset.NameIntArray> wpnList`（List<纳米模式BasicAsset.名称整数Array> 武器列表）(偏移: 0x1C)
- `Texture2D mark_Absorb`（Texture2D mark_Absorb）(偏移: 0x20)
- `Texture2D mark_DefenseNano`（Texture2D mark_Defense纳米）(偏移: 0x24)
- `Texture2D mark_InfectFailed`（Texture2D mark_InfectFailed）(偏移: 0x28)
- `Texture2D[] Mark_NanoMultiKill`（Texture2D[] Mark_纳米多个击杀）(偏移: 0x2C)
- `GameObject[] fx_shield`（游戏Object[] fx_shield）(偏移: 0x30)
- `GameObject Gauge_Absorb`（游戏对象 Gauge_Absorb）(偏移: 0x34)
- `GameObject RadarIcon_Hero`（游戏对象 RadarIcon_英雄）(偏移: 0x3C)
- `GameObject NanoRoleSign`（游戏对象 纳米Role标志）(偏移: 0x40)
- `GameObject[] skillBtns`（游戏Object[] skillBtns）(偏移: 0x48)
- `GameObject[] screenEffects`（游戏Object[] screenEffects）(偏移: 0x4C)

### 方法 (6)

- `void GiveWeapon(Player player)`
  （void GiveWeapon（玩家 player））
- `void TrySetHealth(Player player)`
  （void Try集合Health（玩家 player））
- `bool TryGetChangeFx(NanoRole role, out GameObject result)`
  （bool Try获取Change特效（纳米角色 role, out GameObject result））
- `GameObject GetTerminatorShield(NanoRole nanoRole)`
  （游戏对象 获取TerminatorShield（纳米角色 nanoRole））
- `GameObject GetSkillBtn(NanoRole nanoRole)`
  （游戏对象 获取技能Btn（纳米角色 nanoRole））
- `GameObject GetScreenEffect(NanoRole nanoRole)`
  （游戏对象 获取屏幕的特效（纳米角色 nanoRole））

---

## NanoModeBasicAsset.NameIntArray（纳米模式BasicAsset.名称整数数组）

### 字段 (2)

- `string name`（string name）(偏移: 0x0)
- `int[] datas`（int[] datas）(偏移: 0x4)

---

## NanoNurseCE（纳米NurseCE）

**继承**: CharacterEffect（角色特效）

### 方法 (1)

- `void Update()`
  （void 更新（））

---

## NanoRole（纳米角色）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## NanoRoleExpand（纳米RoleExpand）

### 方法 (15)

- `string GetName(NanoRole role)`
  （string 获取名称（纳米角色 role））
- `bool IsSoldierOrSavior(NanoRole role)`
  （bool 是否SoldierOrSavior（纳米角色 role））
- `bool LikeGuard(NanoRole role)`
  （bool LikeGuard（纳米角色 role））
- `bool IsHuman(NanoRole role)`
  （bool 是否人类（纳米角色 role））
- `bool IsHero(NanoRole role)`
  （bool 是否英雄（纳米角色 role））
- `bool IsNormalHero(NanoRole role)`
  （bool 是否法线英雄（纳米角色 role））
- `bool IsMasterHero(NanoRole role)`
  （bool 是否Master英雄（纳米角色 role））
- `bool IsNanoGhost(NanoRole role)`
  （bool 是否纳米幽灵（纳米角色 role））
- `bool IsNormalNanoGhost(NanoRole role)`
  （bool 是否法线纳米幽灵（纳米角色 role））
- `bool IsTerminator(NanoRole role)`
  （bool 是否Terminator（纳米角色 role））
- `bool IsNormalTerminator(NanoRole role)`
  （bool 是否法线Terminator（纳米角色 role））
- `bool IsMasterTerminator(NanoRole role)`
  （bool 是否MasterTerminator（纳米角色 role））
- `Team GetTeam(NanoRole role)`
  （队伍 获取队伍（纳米角色 role））
- `bool ShouldRemoveAllWpn(NanoRole role)`
  （bool 应该移除所有武器（纳米角色 role））
- `bool CanUseGun(NanoRole role)`
  （bool 能否Use枪械（纳米角色 role））

---

## NanoRoleSelect（纳米Role选择）

### 字段 (4)

- `Player owner`（玩家 owner）(偏移: 0x8)
- `int selection`（int selection）(偏移: 0x14)
- `bool closeWhenDead`（bool closeWhenDead）(偏移: 0x18)
- `Action<NanoRoleSelect.Type> Type_Listnner`（Action<纳米RoleSelect.Type> Type_Listnner）(偏移: 0x1C)

### 方法 (19)

- `NanoRoleSelect.Type get_tableType()`
  （纳米RoleSelect.类型 get_table类型（））
- `void set_tableType(NanoRoleSelect.Type value)`
  （void set_table类型（纳米RoleSelect.类型 value））
- `float get_closeTime()`
  （float get_close时间（））
- `void set_closeTime(float value)`
  （void set_close时间（float value））
- `bool get_isClosed()`
  （bool get_isClosed（））
- `void add_Type_Listnner(Action<NanoRoleSelect.Type> value)`
  （void add_Type_Listnner（Action<纳米RoleSelect.Type> value））
- `void remove_Type_Listnner(Action<NanoRoleSelect.Type> value)`
  （void remove_Type_Listnner（Action<纳米RoleSelect.Type> value））
- `void TryOpenNormal()`
  （void Try打开法线（））
- `void OpenMasterRole(bool isHero)`
  （void 打开MasterRole（bool isHero））
- `void SetType(NanoRoleSelect.Type newType)`
  （void 集合类型（纳米RoleSelect.类型 newType））
- `void Open(NanoRoleSelect.Type type, float time)`
  （void 打开（纳米RoleSelect.类型 type, float time））
- `void Close()`
  （void 关闭（））
- `void Select(int key)`
  （void 选择（int key））
- `void OnLifeStateChange(bool isAlive)`
  （void OnLife状态Change（bool isAlive））
- `void Active()`
  （void 激活的（））
- `void SelectNanoGhost()`
  （void 选择纳米幽灵（））
- `void SelectHero()`
  （void 选择英雄（））
- `void SelectTerminator()`
  （void 选择Terminator（））
- `void Update()`
  （void 更新（））

---

## NanoRoleSelect.Type（纳米RoleSelect.类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Native（Native）

### 方法 (2)

- `void YGNodeMeasureInvoke(YogaNode node, float width, YogaMeasureMode widthMode, float height, YogaMeasureMode heightMode, IntPtr returnValueAddress)`
  （void YG节点MeasureInvoke（Yoga节点 node, float width, YogaMeasure模式 widthMode, float height, YogaMeasure模式 heightMode, 整数Ptr returnValueAddress））
- `void YGNodeBaselineInvoke(YogaNode node, float width, float height, IntPtr returnValueAddress)`
  （void YG节点BaselineInvoke（Yoga节点 node, float width, float height, 整数Ptr returnValueAddress））

---

## NativeArrayOptions（Native数组Options）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## NativeClassAttribute（Native类Attribute）

**继承**: Attribute（Attribute）

### 方法 (2)

- `void set_QualifiedNativeName(string value)`
  （void set_QualifiedNative名称（string value））
- `void set_Declaration(string value)`
  （void set_Declaration（string value））

---

## NativeConditionalAttribute（NativeConditionalAttribute）

**继承**: Attribute（Attribute）

### 方法 (3)

- `void set_Condition(string value)`
  （void set_Condition（string value））
- `void set_StubReturnStatement(string value)`
  （void set_StubReturnStatement（string value））
- `void set_Enabled(bool value)`
  （void set_启用的（bool value））

---

## NativeEventCalls（Native事件Calls）

### 方法 (6)

- `IntPtr CreateEvent_internal(bool manual, bool initial, string name, out int errorCode)`
  （整数Ptr 创建Event_internal（bool manual, bool initial, string name, out int errorCode））
- `bool SetEvent(SafeWaitHandle handle)`
  （bool 集合事件（SafeWait句柄 handle））
- `bool SetEvent_internal(IntPtr handle)`
  （bool 集合Event_internal（整数Ptr handle））
- `bool ResetEvent(SafeWaitHandle handle)`
  （bool 重置事件（SafeWait句柄 handle））
- `bool ResetEvent_internal(IntPtr handle)`
  （bool 重置Event_internal（整数Ptr handle））
- `void CloseEvent_internal(IntPtr handle)`
  （void 关闭Event_internal（整数Ptr handle））

---

## NativeHeaderAttribute（Native标题Attribute）

**继承**: Attribute（Attribute）

### 方法 (1)

- `void set_Header(string value)`
  （void set_标题（string value））

---

## NativeInputEventBuffer（Native输入事件缓冲区）

### 字段 (4)

- `void* eventBuffer`（void* event缓冲区）(偏移: 0x0)
- `int eventCount`（int event数量）(偏移: 0x8)
- `int sizeInBytes`（int sizeInBytes）(偏移: 0xC)
- `int capacityInBytes`（int capacityInBytes）(偏移: 0x10)

---

## NativeInputSystem（Native输入系统）

### 字段 (2)

- `NativeUpdateCallback onUpdate`（Native更新回调 on更新）(偏移: 0x0)
- `Action<NativeInputUpdateType> onBeforeUpdate`（Action<Native输入更新Type> onBefore更新）(偏移: 0x4)

### 方法 (5)

- `void NotifyBeforeUpdate(NativeInputUpdateType updateType)`
  （void NotifyBefore更新（Native输入更新类型 updateType））
- `void NotifyUpdate(NativeInputUpdateType updateType, IntPtr eventBuffer)`
  （void Notify更新（Native输入更新类型 updateType, 整数Ptr eventBuffer））
- `void NotifyDeviceDiscovered(int deviceId, string deviceDescriptor)`
  （void NotifyDeviceDiscovered（int deviceId, string deviceDescriptor））
- `void ShouldRunUpdate(NativeInputUpdateType updateType, out bool retval)`
  （void 应该运行更新（Native输入更新类型 updateType, out bool retval））
- `void set_hasDeviceDiscoveredCallback(bool value)`
  （void set_hasDeviceDiscovered回调（bool value））

---

## NativeInputUpdateType（Native输入更新类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## NativeLeakDetection（NativeLeakDetection）

### 字段 (1)

- `int s_NativeLeakDetectionMode`（int s_NativeLeakDetection模式）(偏移: 0x0)

### 方法 (1)

- `void Initialize()`
  （void 初始化（））

---

## NativeMethodAttribute（NativeMethodAttribute）

**继承**: Attribute（Attribute）

### 方法 (5)

- `void set_Name(string value)`
  （void set_名称（string value））
- `void set_IsThreadSafe(bool value)`
  （void set_是否ThreadSafe（bool value））
- `void set_IsFreeFunction(bool value)`
  （void set_是否FreeFunction（bool value））
- `void set_ThrowsException(bool value)`
  （void set_ThrowsException（bool value））
- `void set_HasExplicitThis(bool value)`
  （void set_是否有ExplicitThis（bool value））

---

## NativeNameAttribute（Native名称Attribute）

**继承**: Attribute（Attribute）

### 方法 (1)

- `void set_Name(string value)`
  （void set_名称（string value））

---

## NativeOverlapped（NativeOverlapped）

### 字段 (5)

- `IntPtr InternalLow`（整数Ptr 内部的Low）(偏移: 0x0)
- `IntPtr InternalHigh`（整数Ptr 内部的High）(偏移: 0x4)
- `int OffsetLow`（int OffsetLow）(偏移: 0x8)
- `int OffsetHigh`（int OffsetHigh）(偏移: 0xC)
- `IntPtr EventHandle`（整数Ptr 事件句柄）(偏移: 0x10)

---

## NativePropertyAttribute（Native属性Attribute）

**继承**: NativeMethodAttribute（NativeMethodAttribute）

### 方法 (1)

- `void set_TargetType(TargetType value)`
  （void set_目标类型（目标类型 value））

---

## NativeThrowsAttribute（NativeThrowsAttribute）

**继承**: Attribute（Attribute）

### 方法 (1)

- `void set_ThrowsException(bool value)`
  （void set_ThrowsException（bool value））

---

## NativeTypeAttribute（Native类型Attribute）

**继承**: Attribute（Attribute）

### 方法 (3)

- `void set_Header(string value)`
  （void set_标题（string value））
- `void set_IntermediateScriptingStructName(string value)`
  （void set_IntermediateScriptingStruct名称（string value））
- `void set_CodegenOptions(CodegenOptions value)`
  （void set_CodegenOptions（CodegenOptions value））

---

## NativeUpdateCallback（Native更新回调）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(NativeInputUpdateType updateType, NativeInputEventBuffer* buffer)`
  （void Invoke（Native输入更新类型 updateType, Native输入事件Buffer* buffer））
- `IAsyncResult BeginInvoke(NativeInputUpdateType updateType, NativeInputEventBuffer* buffer, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Native输入更新类型 updateType, Native输入事件Buffer* buffer, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## NativeWritableSelfAttribute（NativeWritableSelfAttribute）

**继承**: Attribute（Attribute）

### 方法 (1)

- `void set_WritableSelf(bool value)`
  （void set_WritableSelf（bool value））

---

## NavGraph（NavGraph）

**继承**: IGraphInternals（IGraphInternals）

### 字段 (11)

- `AstarPath active`（Astar路径 active）(偏移: 0x8)
- `Guid guid`（Guid guid）(偏移: 0x10)
- `uint initialPenalty`（uint initial惩罚）(偏移: 0x20)
- `bool open`（bool open）(偏移: 0x24)
- `uint graphIndex`（uint graph索引）(偏移: 0x28)
- `string name`（string name）(偏移: 0x2C)
- `bool drawGizmos`（bool drawGizmos）(偏移: 0x30)
- `bool infoScreenOpen`（bool info屏幕的打开）(偏移: 0x31)
- `string serializedEditorSettings`（string serializedEditorSettings）(偏移: 0x34)
- `Matrix4x4 matrix`（Matrix4x4 matrix）(偏移: 0x38)
- `Matrix4x4 inverseMatrix`（Matrix4x4 inverse矩阵）(偏移: 0x78)

### 方法 (20)

- `bool get_exists()`
  （bool get_exists（））
- `int CountNodes()`
  （int 数量Nodes（））
- `void GetNodes(Func<GraphNode, bool> action)`
  （void 获取Nodes（Func<Graph节点, bool> action））
- `void SetMatrix(Matrix4x4 m)`
  （void 集合矩阵（Matrix4x4 m））
- `void RelocateNodes(Matrix4x4 oldMatrix, Matrix4x4 newMatrix)`
  （void RelocateNodes（Matrix4x4 oldMatrix, Matrix4x4 newMatrix））
- `void RelocateNodes(Matrix4x4 deltaMatrix)`
  （void RelocateNodes（Matrix4x4 deltaMatrix））
- `NNInfoInternal GetNearest(Vector3 position)`
  （NN信息内部的 获取Nearest（三维向量 position））
- `NNInfoInternal GetNearest(Vector3 position, NNConstraint constraint)`
  （NN信息内部的 获取Nearest（三维向量 position, NNConstraint constraint））
- `NNInfoInternal GetNearest(Vector3 position, NNConstraint constraint, GraphNode hint)`
  （NN信息内部的 获取Nearest（三维向量 position, NNConstraint constraint, Graph节点 hint））
- `NNInfoInternal GetNearestForce(Vector3 position, NNConstraint constraint)`
  （NN信息内部的 获取Nearest强制（三维向量 position, NNConstraint constraint））
- `void OnDestroy()`
  （void On销毁（））
- `void DestroyAllNodes()`
  （void 销毁所有Nodes（））
- `void ScanGraph()`
  （void ScanGraph（））
- `void Scan()`
  （void Scan（））
- `void SerializeExtraInfo(GraphSerializationContext ctx)`
  （void Serialize额外的信息（GraphSerializationContext ctx））
- `void DeserializeExtraInfo(GraphSerializationContext ctx)`
  （void Deserialize额外的信息（GraphSerializationContext ctx））
- `void PostDeserialization(GraphSerializationContext ctx)`
  （void PostDeserialization（GraphSerializationContext ctx））
- `void DeserializeSettingsCompatibility(GraphSerializationContext ctx)`
  （void DeserializeSettingsCompatibility（GraphSerializationContext ctx））
- `void OnDrawGizmos(RetainedGizmos gizmos, bool drawNodes)`
  （void OnDrawGizmos（RetainedGizmos gizmos, bool drawNodes））
- `void DrawUnwalkableNodes(float size)`
  （void DrawUnwalkableNodes（float size））

---

## NavMesh（Nav网格）

### 字段 (1)

- `NavMesh.OnNavMeshPreUpdate onPreUpdate`（NavMesh.OnNav网格Pre更新 onPre更新）(偏移: 0x30D930D2)

### 方法 (6)

- `void Internal_CallOnNavMeshPreUpdate()`
  （void Internal_CallOnNav网格Pre更新（））
- `bool CalculatePath(Vector3 sourcePosition, Vector3 targetPosition, int areaMask, NavMeshPath path)`
  （bool 计算路径（三维向量 sourcePosition, 三维向量 targetPosition, int areaMask, Nav网格路径 path））
- `bool CalculatePathInternal(Vector3 sourcePosition, Vector3 targetPosition, int areaMask, NavMeshPath path)`
  （bool 计算路径内部的（三维向量 sourcePosition, 三维向量 targetPosition, int areaMask, Nav网格路径 path））
- `bool SamplePosition(Vector3 sourcePosition, out NavMeshHit hit, float maxDistance, int areaMask)`
  （bool SamplePosition（三维向量 sourcePosition, out NavMeshHit hit, float maxDistance, int areaMask））
- `bool CalculatePathInternal_Injected(ref Vector3 sourcePosition, ref Vector3 targetPosition, int areaMask, NavMeshPath path)`
  （bool 计算路径Internal_Injected（ref Vector3 sourcePosition, ref Vector3 targetPosition, int areaMask, Nav网格路径 path））
- `bool SamplePosition_Injected(ref Vector3 sourcePosition, out NavMeshHit hit, float maxDistance, int areaMask)`
  （bool SamplePosition_Injected（ref Vector3 sourcePosition, out NavMeshHit hit, float maxDistance, int areaMask））

---

## NavMesh.OnNavMeshPreUpdate（NavMesh.OnNav网格Pre更新）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke()`
  （void Invoke（））
- `IAsyncResult BeginInvoke(AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## NavMeshGraph（Nav网格Graph）

**继承**: NavmeshBase, IUpdatableGraph（Navmesh基础, IUpdatableGraph）

### 字段 (5)

- `Mesh sourceMesh`（网格 source网格）(偏移: 0xF8)
- `Vector3 offset`（三维向量 offset）(偏移: 0xFC)
- `Vector3 rotation`（三维向量 rotation）(偏移: 0x108)
- `float scale`（float scale）(偏移: 0x114)
- `bool recalculateNormals`（bool recalculateNormals）(偏移: 0x118)

### 方法 (9)

- `bool get_RecalculateNormals()`
  （bool get_RecalculateNormals（））
- `float get_TileWorldSizeX()`
  （float get_Tile世界的大小X（））
- `float get_TileWorldSizeZ()`
  （float get_Tile世界的大小Z（））
- `float get_MaxTileConnectionEdgeDistance()`
  （float get_最大Tile连接Edge距离（））
- `GraphTransform CalculateTransform()`
  （Graph变换 计算变换（））
- `void UpdateArea(GraphUpdateObject o, INavmeshHolder graph)`
  （void 更新Area（Graph更新对象 o, INavmeshHolder graph））
- `void ScanInternal(string objMeshPath)`
  （void Scan内部的（string objMeshPath））
- `IEnumerable<Progress> ScanInternal()`
  （IEnumerable<Progress> Scan内部的（））
- `void DeserializeSettingsCompatibility(GraphSerializationContext ctx)`
  （void DeserializeSettingsCompatibility（GraphSerializationContext ctx））

---

## NavMeshHit（Nav网格命中）

### 字段 (5)

- `Vector3 m_Position`（三维向量 m_Position）(偏移: 0x0)
- `Vector3 m_Normal`（三维向量 m_法线）(偏移: 0xC)
- `float m_Distance`（float m_距离）(偏移: 0x18)
- `int m_Mask`（int m_掩码）(偏移: 0x1C)
- `int m_Hit`（int m_命中）(偏移: 0x20)

### 方法 (1)

- `Vector3 get_position()`
  （三维向量 get_position（））

---

## NavMeshPath（Nav网格路径）

### 字段 (2)

- `IntPtr m_Ptr`（整数Ptr m_Ptr）(偏移: 0x8)
- `Vector3[] m_Corners`（Vector3[] m_Corners）(偏移: 0xC)

### 方法 (9)

- `void Finalize()`
  （void Finalize（））
- `IntPtr InitializeNavMeshPath()`
  （整数Ptr 初始化Nav网格路径（））
- `void DestroyNavMeshPath(IntPtr ptr)`
  （void 销毁Nav网格路径（整数Ptr ptr））
- `Vector3[] CalculateCornersInternal()`
  （Vector3[] 计算Corners内部的（））
- `void ClearCornersInternal()`
  （void 清除Corners内部的（））
- `void ClearCorners()`
  （void 清除Corners（））
- `void CalculateCorners()`
  （void 计算Corners（））
- `Vector3[] get_corners()`
  （Vector3[] get_corners（））
- `NavMeshPathStatus get_status()`
  （Nav网格路径Status get_status（））

---

## NavMeshPathStatus（Nav网格路径Status）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Navigation（Navigation）

**继承**: IEquatable<Navigation>（IEquatable<Navigation>）

### 字段 (6)

- `Navigation.Mode m_Mode`（Navigation.模式 m_模式）(偏移: 0x0)
- `bool m_WrapAround`（bool m_WrapAround）(偏移: 0x4)
- `Selectable m_SelectOnUp`（Selectable m_选择On上）(偏移: 0x8)
- `Selectable m_SelectOnDown`（Selectable m_选择On下）(偏移: 0xC)
- `Selectable m_SelectOnLeft`（Selectable m_选择On左）(偏移: 0x10)
- `Selectable m_SelectOnRight`（Selectable m_选择On右）(偏移: 0x14)

### 方法 (14)

- `Navigation.Mode get_mode()`
  （Navigation.模式 get_mode（））
- `void set_mode(Navigation.Mode value)`
  （void set_mode（Navigation.模式 value））
- `bool get_wrapAround()`
  （bool get_wrapAround（））
- `void set_wrapAround(bool value)`
  （void set_wrapAround（bool value））
- `Selectable get_selectOnUp()`
  （Selectable get_selectOn上（））
- `void set_selectOnUp(Selectable value)`
  （void set_selectOn上（Selectable value））
- `Selectable get_selectOnDown()`
  （Selectable get_selectOn下（））
- `void set_selectOnDown(Selectable value)`
  （void set_selectOn下（Selectable value））
- `Selectable get_selectOnLeft()`
  （Selectable get_selectOn左（））
- `void set_selectOnLeft(Selectable value)`
  （void set_selectOn左（Selectable value））
- `Selectable get_selectOnRight()`
  （Selectable get_selectOn右（））
- `void set_selectOnRight(Selectable value)`
  （void set_selectOn右（Selectable value））
- `Navigation get_defaultNavigation()`
  （Navigation get_defaultNavigation（））
- `bool Equals(Navigation other)`
  （bool Equals（Navigation other））

---

## Navigation.Mode（Navigation.模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Navigator（Navigator）

### 字段 (12)

- `bool activeTargetSeeking`（bool active目标Seeking）(偏移: 0x8)
- `float cornerRadius`（float cornerRadius）(偏移: 0xC)
- `float recalculateOnPathDistance`（float recalculateOn路径距离）(偏移: 0x10)
- `float maxSampleDistance`（float maxSample距离）(偏移: 0x14)
- `float nextPathInterval`（float next路径间隔）(偏移: 0x18)
- `Transform transform`（变换 transform）(偏移: 0x2C)
- `int cornerIndex`（int corner索引）(偏移: 0x30)
- `Vector3[] corners`（Vector3[] corners）(偏移: 0x34)
- `NavMeshPath path`（Nav网格路径 path）(偏移: 0x38)
- `Vector3 lastTargetPosition`（三维向量 last目标Position）(偏移: 0x3C)
- `bool initiated`（bool initiated）(偏移: 0x48)
- `float nextPathTime`（float next路径时间）(偏移: 0x4C)

### 方法 (11)

- `Vector3 get_normalizedDeltaPosition()`
  （三维向量 get_normalizedDeltaPosition（））
- `void set_normalizedDeltaPosition(Vector3 value)`
  （void set_normalizedDeltaPosition（三维向量 value））
- `Navigator.State get_state()`
  （Navigator.状态 get_state（））
- `void set_state(Navigator.State value)`
  （void set_state（Navigator.状态 value））
- `void Initiate(Transform transform)`
  （void Initiate（变换 transform））
- `void Update(Vector3 targetPosition)`
  （void 更新（三维向量 targetPosition））
- `void CalculatePath(Vector3 targetPosition)`
  （void 计算路径（三维向量 targetPosition））
- `bool Find(Vector3 targetPosition)`
  （bool 查找（三维向量 targetPosition））
- `void Stop()`
  （void 停止（））
- `float HorDistance(Vector3 p1, Vector3 p2)`
  （float Hor距离（三维向量 p1, 三维向量 p2））
- `void Visualize()`
  （void Visualize（））

---

## Navigator.State（Navigator.状态）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## NavmeshAdd（Navmesh添加）

**继承**: NavmeshClipper（NavmeshClipper）

### 字段 (14)

- `NavmeshAdd.MeshType type`（NavmeshAdd.网格类型 type）(偏移: 0x14)
- `Mesh mesh`（网格 mesh）(偏移: 0x18)
- `Vector3[] verts`（Vector3[] verts）(偏移: 0x1C)
- `int[] tris`（int[] tris）(偏移: 0x20)
- `Vector2 rectangleSize`（二维向量 rectangle大小）(偏移: 0x24)
- `float meshScale`（float mesh缩放）(偏移: 0x2C)
- `Vector3 center`（三维向量 center）(偏移: 0x30)
- `bool useRotationAndScale`（bool useRotationAnd缩放）(偏移: 0x3C)
- `float updateDistance`（float update距离）(偏移: 0x40)
- `float updateRotationDistance`（float updateRotation距离）(偏移: 0x44)
- `Transform tr`（变换 tr）(偏移: 0x48)
- `Vector3 lastPosition`（三维向量 lastPosition）(偏移: 0x4C)
- `Quaternion lastRotation`（Quaternion lastRotation）(偏移: 0x58)
- `Color GizmoColor`（颜色 Gizmo颜色）(偏移: 0x0)

### 方法 (8)

- `bool RequiresUpdate()`
  （bool Requires更新（））
- `void ForceUpdate()`
  （void 强制更新（））
- `void Awake()`
  （void Awake（））
- `void NotifyUpdated()`
  （void NotifyUpdated（））
- `Vector3 get_Center()`
  （三维向量 get_中心（））
- `void RebuildMesh()`
  （void Rebuild网格（））
- `Rect GetBounds(GraphTransform inverseTransform)`
  （Rect 获取Bounds（Graph变换 inverseTransform））
- `void GetMesh(ref Int3[] vbuffer, out int[] tbuffer, GraphTransform inverseTransform)`
  （void 获取网格（ref Int3[] vbuffer, out int[] tbuffer, Graph变换 inverseTransform））

---

## NavmeshAdd.MeshType（NavmeshAdd.网格类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## NavmeshBase（Navmesh基础）

**继承**: NavGraph, INavmesh, INavmeshHolder, ITransformedGraph, IRaycastableGraph（NavGraph, INavmesh, INavmeshHolder, ITransformedGraph, IRaycastableGraph）

### 字段 (18)

- `Vector3 forcedBoundsSize`（三维向量 forcedBounds大小）(偏移: 0xB8)
- `bool showMeshOutline`（bool show网格Outline）(偏移: 0xC4)
- `bool showNodeConnections`（bool show节点Connections）(偏移: 0xC5)
- `bool showMeshSurface`（bool show网格Surface）(偏移: 0xC6)
- `int tileXCount`（int tileX数量）(偏移: 0xC8)
- `int tileZCount`（int tileZ数量）(偏移: 0xCC)
- `NavmeshTile[] tiles`（NavmeshTile[] tiles）(偏移: 0xD0)
- `bool nearestSearchOnlyXZ`（bool nearest搜索OnlyXZ）(偏移: 0xD4)
- `bool enableNavmeshCutting`（bool enableNavmeshCutting）(偏移: 0xD5)
- `NavmeshUpdates.NavmeshUpdateSettings navmeshUpdateData`（NavmeshUpdates.Navmesh更新Settings navmesh更新数据）(偏移: 0xD8)
- `bool batchTileUpdate`（bool batchTile更新）(偏移: 0xDC)
- `List<int> batchUpdatedTiles`（List<int> batchUpdatedTiles）(偏移: 0xE0)
- `List<MeshNode> batchNodesToDestroy`（List<网格Node> batchNodesTo销毁）(偏移: 0xE4)
- `GraphTransform transform`（Graph变换 transform）(偏移: 0xE8)
- `Action<NavmeshTile[]> OnRecalculatedTiles`（Action<NavmeshTile[]> OnRecalculatedTiles）(偏移: 0xEC)
- `NNConstraint NNConstraintDistanceXZ`（NNConstraint NNConstraint距离XZ）(偏移: 0x0)
- `NNConstraint NNConstraintNone`（NNConstraint NNConstraint无）(偏移: 0x4)
- `byte[] LinecastShapeEdgeLookup`（byte[] LinecastShapeEdgeLookup）(偏移: 0x8)

### 方法 (49)

- `NavmeshTile GetTile(int x, int z)`
  （NavmeshTile 获取Tile（int x, int z））
- `Int3 GetVertex(int index)`
  （Int3 获取Vertex（int index））
- `Int3 GetVertexInGraphSpace(int index)`
  （Int3 获取VertexInGraphSpace（int index））
- `int GetTileIndex(int index)`
  （int 获取Tile索引（int index））
- `int GetVertexArrayIndex(int index)`
  （int 获取Vertex数组索引（int index））
- `void GetTileCoordinates(int tileIndex, out int x, out int z)`
  （void 获取TileCoordinates（int tileIndex, out int x, out int z））
- `NavmeshTile[] GetTiles()`
  （NavmeshTile[] 获取Tiles（））
- `Bounds GetTileBounds(IntRect rect)`
  （Bounds 获取TileBounds（整数Rect rect））
- `Bounds GetTileBounds(int x, int z, int width = 1, int depth = 1)`
  （Bounds 获取TileBounds（int x, int z, int width = 1, int depth = 1））
- `Bounds GetTileBoundsInGraphSpace(IntRect rect)`
  （Bounds 获取TileBoundsInGraphSpace（整数Rect rect））
- `Bounds GetTileBoundsInGraphSpace(int x, int z, int width = 1, int depth = 1)`
  （Bounds 获取TileBoundsInGraphSpace（int x, int z, int width = 1, int depth = 1））
- `Int2 GetTileCoordinates(Vector3 position)`
  （Int2 获取TileCoordinates（三维向量 position））
- `void OnDestroy()`
  （void On销毁（））
- `void RelocateNodes(Matrix4x4 deltaMatrix)`
  （void RelocateNodes（Matrix4x4 deltaMatrix））
- `void RelocateNodes(GraphTransform newTransform)`
  （void RelocateNodes（Graph变换 newTransform））
- `NavmeshTile NewEmptyTile(int x, int z)`
  （NavmeshTile 新的空Tile（int x, int z））
- `void GetNodes(Action<GraphNode> action)`
  （void 获取Nodes（Action<GraphNode> action））
- `IntRect GetTouchingTiles(Bounds bounds, float margin = 0)`
  （整数Rect 获取TouchingTiles（Bounds bounds, float margin = 0））
- `IntRect GetTouchingTilesInGraphSpace(Rect rect)`
  （整数Rect 获取TouchingTilesInGraphSpace（Rect rect））
- `IntRect GetTouchingTilesRound(Bounds bounds)`
  （整数Rect 获取TouchingTiles回合（Bounds bounds））
- `void ConnectTileWithNeighbours(NavmeshTile tile, bool onlyUnflagged = False)`
  （void ConnectTileWithNeighbours（NavmeshTile tile, bool onlyUnflagged = False））
- `void RemoveConnectionsFromTile(NavmeshTile tile)`
  （void 移除ConnectionsFromTile（NavmeshTile tile））
- `void RemoveConnectionsFromTo(NavmeshTile a, NavmeshTile b)`
  （void 移除ConnectionsFromTo（NavmeshTile a, NavmeshTile b））
- `NNInfoInternal GetNearest(Vector3 position, NNConstraint constraint, GraphNode hint)`
  （NN信息内部的 获取Nearest（三维向量 position, NNConstraint constraint, Graph节点 hint））
- `NNInfoInternal GetNearestForce(Vector3 position, NNConstraint constraint)`
  （NN信息内部的 获取Nearest强制（三维向量 position, NNConstraint constraint））
- `GraphNode PointOnNavmesh(Vector3 position, NNConstraint constraint)`
  （Graph节点 PointOnNavmesh（三维向量 position, NNConstraint constraint））
- `void FillWithEmptyTiles()`
  （void FillWith空Tiles（））
- `void CreateNodeConnections(TriangleMeshNode[] nodes)`
  （void 创建节点Connections（Triangle网格Node[] nodes））
- `void ConnectTiles(NavmeshTile tile1, NavmeshTile tile2)`
  （void ConnectTiles（NavmeshTile tile1, NavmeshTile tile2））
- `void StartBatchTileUpdate()`
  （void 开始BatchTile更新（））
- `void DestroyNodes(List<MeshNode> nodes)`
  （void 销毁Nodes（List<网格Node> nodes））
- `void TryConnect(int tileIdx1, int tileIdx2)`
  （void TryConnect（int tileIdx1, int tileIdx2））
- `void EndBatchTileUpdate()`
  （void 结束BatchTile更新（））
- `void ClearTile(int x, int z)`
  （void 清除Tile（int x, int z））
- `void PrepareNodeRecycling(int x, int z, Int3[] verts, int[] tris, TriangleMeshNode[] recycledNodeBuffer)`
  （void Prepare节点Recycling（int x, int z, Int3[] verts, int[] tris, Triangle网格Node[] recycledNodeBuffer））
- `void ReplaceTile(int x, int z, Int3[] verts, int[] tris)`
  （void ReplaceTile（int x, int z, Int3[] verts, int[] tris））
- `void CreateNodes(TriangleMeshNode[] buffer, int[] tris, int tileIndex, uint graphIndex)`
  （void 创建Nodes（Triangle网格Node[] buffer, int[] tris, int tileIndex, uint graphIndex））
- `bool Linecast(Vector3 origin, Vector3 end)`
  （bool Linecast（三维向量 origin, 三维向量 end））
- `bool Linecast(Vector3 origin, Vector3 end, GraphNode hint, out GraphHitInfo hit)`
  （bool Linecast（三维向量 origin, 三维向量 end, Graph节点 hint, out GraphHitInfo hit））
- `bool Linecast(Vector3 origin, Vector3 end, GraphNode hint)`
  （bool Linecast（三维向量 origin, 三维向量 end, Graph节点 hint））
- `bool Linecast(Vector3 origin, Vector3 end, GraphNode hint, out GraphHitInfo hit, List<GraphNode> trace)`
  （bool Linecast（三维向量 origin, 三维向量 end, Graph节点 hint, out GraphHitInfo hit, List<GraphNode> trace））
- `bool Linecast(NavmeshBase graph, Vector3 origin, Vector3 end, GraphNode hint, out GraphHitInfo hit)`
  （bool Linecast（Navmesh基础 graph, 三维向量 origin, 三维向量 end, Graph节点 hint, out GraphHitInfo hit））
- `bool Linecast(NavmeshBase graph, Vector3 origin, Vector3 end, GraphNode hint, out GraphHitInfo hit, List<GraphNode> trace)`
  （bool Linecast（Navmesh基础 graph, 三维向量 origin, 三维向量 end, Graph节点 hint, out GraphHitInfo hit, List<GraphNode> trace））
- `void OnDrawGizmos(RetainedGizmos gizmos, bool drawNodes)`
  （void OnDrawGizmos（RetainedGizmos gizmos, bool drawNodes））
- `void CreateNavmeshSurfaceVisualization(NavmeshTile tile, GraphGizmoHelper helper)`
  （void 创建NavmeshSurfaceVisualization（NavmeshTile tile, GraphGizmo辅助器 helper））
- `void CreateNavmeshOutlineVisualization(NavmeshTile tile, GraphGizmoHelper helper)`
  （void 创建NavmeshOutlineVisualization（NavmeshTile tile, GraphGizmo辅助器 helper））
- `void SerializeExtraInfo(GraphSerializationContext ctx)`
  （void Serialize额外的信息（GraphSerializationContext ctx））
- `void DeserializeExtraInfo(GraphSerializationContext ctx)`
  （void Deserialize额外的信息（GraphSerializationContext ctx））
- `void PostDeserialization(GraphSerializationContext ctx)`
  （void PostDeserialization（GraphSerializationContext ctx））

---

## NavmeshClipper（NavmeshClipper）

**继承**: VersionedMonoBehaviour（VersionedMonoBehaviour）

### 字段 (4)

- `Action<NavmeshClipper> OnEnableCallback`（Action<NavmeshClipper> On启用回调）(偏移: 0x0)
- `Action<NavmeshClipper> OnDisableCallback`（Action<NavmeshClipper> On禁用回调）(偏移: 0x4)
- `List<NavmeshClipper> all`（List<NavmeshClipper> all）(偏移: 0x8)
- `int listIndex`（int list索引）(偏移: 0x10)

### 方法 (5)

- `void AddEnableCallback(Action<NavmeshClipper> onEnable, Action<NavmeshClipper> onDisable)`
  （void 添加启用回调（Action<NavmeshClipper> onEnable, Action<NavmeshClipper> onDisable））
- `void RemoveEnableCallback(Action<NavmeshClipper> onEnable, Action<NavmeshClipper> onDisable)`
  （void 移除启用回调（Action<NavmeshClipper> onEnable, Action<NavmeshClipper> onDisable））
- `List<NavmeshClipper> get_allEnabled()`
  （List<NavmeshClipper> get_all启用的（））
- `void OnEnable()`
  （void On启用（））
- `void OnDisable()`
  （void On禁用（））

---

## NavmeshCut（NavmeshCut）

**继承**: NavmeshClipper（NavmeshClipper）

### 字段 (19)

- `NavmeshCut.MeshType type`（NavmeshCut.网格类型 type）(偏移: 0x14)
- `Mesh mesh`（网格 mesh）(偏移: 0x18)
- `Vector2 rectangleSize`（二维向量 rectangle大小）(偏移: 0x1C)
- `float circleRadius`（float circleRadius）(偏移: 0x24)
- `int circleResolution`（int circleResolution）(偏移: 0x28)
- `float height`（float height）(偏移: 0x2C)
- `float meshScale`（float mesh缩放）(偏移: 0x30)
- `Vector3 center`（三维向量 center）(偏移: 0x34)
- `float updateDistance`（float update距离）(偏移: 0x40)
- `bool isDual`（bool isDual）(偏移: 0x44)
- `bool cutsAddedGeom`（bool cutsAddedGeom）(偏移: 0x45)
- `float updateRotationDistance`（float updateRotation距离）(偏移: 0x48)
- `bool useRotationAndScale`（bool useRotationAnd缩放）(偏移: 0x4C)
- `Vector3[][] contours`（Vector3[][] contours）(偏移: 0x50)
- `Transform tr`（变换 tr）(偏移: 0x54)
- `Mesh lastMesh`（网格 last网格）(偏移: 0x58)
- `Vector3 lastPosition`（三维向量 lastPosition）(偏移: 0x5C)
- `Quaternion lastRotation`（Quaternion lastRotation）(偏移: 0x68)
- `Color GizmoColor`（颜色 Gizmo颜色）(偏移: 0x8)

### 方法 (13)

- `void Awake()`
  （void Awake（））
- `void OnEnable()`
  （void On启用（））
- `void ForceUpdate()`
  （void 强制更新（））
- `bool RequiresUpdate()`
  （bool Requires更新（））
- `void UsedForCut()`
  （void UsedForCut（））
- `void NotifyUpdated()`
  （void NotifyUpdated（））
- `void CalculateMeshContour()`
  （void 计算网格Contour（））
- `Rect GetBounds(GraphTransform inverseTransform)`
  （Rect 获取Bounds（Graph变换 inverseTransform））
- `void GetContour(List<List<Vector3>> buffer)`
  （void 获取Contour（List<List<Vector3>> buffer））
- `void TransformBuffer(List<Vector3> buffer, bool reverse)`
  （void 变换缓冲区（List<Vector3> buffer, bool reverse））
- `void OnDrawGizmos()`
  （void OnDrawGizmos（））
- `float GetY(GraphTransform transform)`
  （float 获取Y（Graph变换 transform））
- `void OnDrawGizmosSelected()`
  （void OnDrawGizmos选中的（））

---

## NavmeshCut.MeshType（NavmeshCut.网格类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## NavmeshTile（NavmeshTile）

**继承**: INavmeshHolder, ITransformedGraph, INavmesh（INavmeshHolder, ITransformedGraph, INavmesh）

### 字段 (11)

- `int[] tris`（int[] tris）(偏移: 0x8)
- `Int3[] verts`（Int3[] verts）(偏移: 0xC)
- `Int3[] vertsInGraphSpace`（Int3[] vertsInGraphSpace）(偏移: 0x10)
- `int x`（int x）(偏移: 0x14)
- `int z`（int z）(偏移: 0x18)
- `int w`（int w）(偏移: 0x1C)
- `int d`（int d）(偏移: 0x20)
- `TriangleMeshNode[] nodes`（Triangle网格Node[] nodes）(偏移: 0x24)
- `BBTree bbTree`（BBTree bbTree）(偏移: 0x28)
- `bool flag`（bool flag）(偏移: 0x2C)
- `NavmeshBase graph`（Navmesh基础 graph）(偏移: 0x30)

### 方法 (6)

- `void GetTileCoordinates(int tileIndex, out int x, out int z)`
  （void 获取TileCoordinates（int tileIndex, out int x, out int z））
- `int GetVertexArrayIndex(int index)`
  （int 获取Vertex数组索引（int index））
- `Int3 GetVertex(int index)`
  （Int3 获取Vertex（int index））
- `Int3 GetVertexInGraphSpace(int index)`
  （Int3 获取VertexInGraphSpace（int index））
- `GraphTransform get_transform()`
  （Graph变换 get_transform（））
- `void GetNodes(Action<GraphNode> action)`
  （void 获取Nodes（Action<GraphNode> action））

---

## NavmeshUpdates（NavmeshUpdates）

### 字段 (2)

- `float updateInterval`（float update间隔）(偏移: 0x8)
- `float lastUpdateTime`（float last更新时间）(偏移: 0xC)

### 方法 (7)

- `void OnEnable()`
  （void On启用（））
- `void OnDisable()`
  （void On禁用（））
- `void DiscardPending()`
  （void DiscardPending（））
- `void HandleOnEnableCallback(NavmeshClipper obj)`
  （void 句柄On启用回调（NavmeshClipper obj））
- `void HandleOnDisableCallback(NavmeshClipper obj)`
  （void 句柄On禁用回调（NavmeshClipper obj））
- `void Update()`
  （void 更新（））
- `void ForceUpdate()`
  （void 强制更新（））

---

## NavmeshUpdates.NavmeshUpdateSettings（NavmeshUpdates.Navmesh更新Settings）

### 字段 (3)

- `TileHandler handler`（Tile处理器 handler）(偏移: 0x8)
- `List<IntRect> forcedReloadRects`（List<整数Rect> forced换弹Rects）(偏移: 0xC)
- `NavmeshBase graph`（Navmesh基础 graph）(偏移: 0x10)

### 方法 (4)

- `void Refresh(bool forceCreate = False)`
  （void 刷新（bool forceCreate = False））
- `void OnRecalculatedTiles(NavmeshTile[] tiles)`
  （void OnRecalculatedTiles（NavmeshTile[] tiles））
- `void AddClipper(NavmeshClipper obj)`
  （void 添加Clipper（NavmeshClipper obj））
- `void RemoveClipper(NavmeshClipper obj)`
  （void 移除Clipper（NavmeshClipper obj））

---

## NestedDB（NestedDB）

**继承**: ScriptableObject（脚本对象）

### 字段 (1)

- `MainDict nested`（主要的Dict nested）(偏移: 0xC)

---

