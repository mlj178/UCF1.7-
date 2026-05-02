# 游戏类定义 (Part 9/21)

共 200 个类 (总序号 1601 - 1800)

---

## HitReaction.HitPoint（命中Reaction.命中Point）

### 字段 (6)

- `string name`（string name）(偏移: 0x8)
- `Collider collider`（碰撞器 collider）(偏移: 0xC)
- `float crossFadeTime`（float crossFade时间）(偏移: 0x10)
- `float length`（float length）(偏移: 0x34)
- `float crossFadeSpeed`（float crossFadeSpeed）(偏移: 0x38)
- `float lastTime`（float last时间）(偏移: 0x3C)

### 方法 (11)

- `bool get_inProgress()`
  （bool get_inProgress（））
- `float get_crossFader()`
  （float get_crossFader（））
- `void set_crossFader(float value)`
  （void set_crossFader（float value））
- `float get_timer()`
  （float get_timer（））
- `void set_timer(float value)`
  （void set_timer（float value））
- `Vector3 get_force()`
  （三维向量 get_force（））
- `void set_force(Vector3 value)`
  （void set_force（三维向量 value））
- `Vector3 get_point()`
  （三维向量 get_point（））
- `void set_point(Vector3 value)`
  （void set_point（三维向量 value））
- `void Hit(Vector3 force, Vector3 point)`
  （void 命中（三维向量 force, 三维向量 point））
- `void Apply(IKSolverFullBodyBiped solver, float weight)`
  （void 应用（IKSolver满身体Biped solver, float weight））

---

## HitReaction.HitPointBone（命中Reaction.命中PointBone）

**继承**: HitReaction.HitPoint（命中Reaction.命中Point）

### 字段 (3)

- `AnimationCurve aroundCenterOfMass`（动画Curve around中心OfMass）(偏移: 0x40)
- `HitReaction.HitPointBone.BoneLink[] boneLinks`（命中Reaction.命中PointBone.BoneLink[] boneLinks）(偏移: 0x44)
- `Rigidbody rigidbody`（刚体 rigidbody）(偏移: 0x48)

### 方法 (3)

- `float GetLength()`
  （float 获取Length（））
- `void CrossFadeStart()`
  （void CrossFade开始（））
- `void OnApply(IKSolverFullBodyBiped solver, float weight)`
  （void On应用（IKSolver满身体Biped solver, float weight））

---

## HitReaction.HitPointBone.BoneLink（命中Reaction.命中PointBone.BoneLink）

### 字段 (4)

- `Transform bone`（变换 bone）(偏移: 0x8)
- `float weight`（float weight）(偏移: 0xC)
- `Quaternion lastValue`（Quaternion last值）(偏移: 0x10)
- `Quaternion current`（Quaternion current）(偏移: 0x20)

### 方法 (2)

- `void Apply(IKSolverFullBodyBiped solver, Quaternion offset, float crossFader)`
  （void 应用（IKSolver满身体Biped solver, Quaternion offset, float crossFader））
- `void CrossFadeStart()`
  （void CrossFade开始（））

---

## HitReaction.HitPointEffector（命中Reaction.命中PointEffector）

**继承**: HitReaction.HitPoint（命中Reaction.命中Point）

### 字段 (3)

- `AnimationCurve offsetInForceDirection`（动画Curve offsetIn强制方向）(偏移: 0x40)
- `AnimationCurve offsetInUpDirection`（动画Curve offsetIn上方向）(偏移: 0x44)
- `HitReaction.HitPointEffector.EffectorLink[] effectorLinks`（命中Reaction.命中PointEffector.EffectorLink[] effectorLinks）(偏移: 0x48)

### 方法 (3)

- `float GetLength()`
  （float 获取Length（））
- `void CrossFadeStart()`
  （void CrossFade开始（））
- `void OnApply(IKSolverFullBodyBiped solver, float weight)`
  （void On应用（IKSolver满身体Biped solver, float weight））

---

## HitReaction.HitPointEffector.EffectorLink（命中Reaction.命中PointEffector.EffectorLink）

### 字段 (4)

- `FullBodyBipedEffector effector`（满身体BipedEffector effector）(偏移: 0x8)
- `float weight`（float weight）(偏移: 0xC)
- `Vector3 lastValue`（三维向量 last值）(偏移: 0x10)
- `Vector3 current`（三维向量 current）(偏移: 0x1C)

### 方法 (2)

- `void Apply(IKSolverFullBodyBiped solver, Vector3 offset, float crossFader)`
  （void 应用（IKSolver满身体Biped solver, 三维向量 offset, float crossFader））
- `void CrossFadeStart()`
  （void CrossFade开始（））

---

## HitReactionVRIK（命中ReactionVRIK）

**继承**: OffsetModifierVRIK（Offset修改器VRIK）

### 字段 (3)

- `AnimationCurve[] offsetCurves`（动画Curve[] offsetCurves）(偏移: 0x18)
- `HitReactionVRIK.PositionOffset[] positionOffsets`（命中ReactionVRIK.PositionOffset[] positionOffsets）(偏移: 0x1C)
- `HitReactionVRIK.RotationOffset[] rotationOffsets`（命中ReactionVRIK.RotationOffset[] rotationOffsets）(偏移: 0x20)

### 方法 (2)

- `void OnModifyOffset()`
  （void OnModifyOffset（））
- `void Hit(Collider collider, Vector3 force, Vector3 point)`
  （void 命中（碰撞器 collider, 三维向量 force, 三维向量 point））

---

## HitReactionVRIK.Offset（命中ReactionVRIK.Offset）

### 字段 (6)

- `string name`（string name）(偏移: 0x8)
- `Collider collider`（碰撞器 collider）(偏移: 0xC)
- `float crossFadeTime`（float crossFade时间）(偏移: 0x10)
- `float length`（float length）(偏移: 0x34)
- `float crossFadeSpeed`（float crossFadeSpeed）(偏移: 0x38)
- `float lastTime`（float last时间）(偏移: 0x3C)

### 方法 (10)

- `float get_crossFader()`
  （float get_crossFader（））
- `void set_crossFader(float value)`
  （void set_crossFader（float value））
- `float get_timer()`
  （float get_timer（））
- `void set_timer(float value)`
  （void set_timer（float value））
- `Vector3 get_force()`
  （三维向量 get_force（））
- `void set_force(Vector3 value)`
  （void set_force（三维向量 value））
- `Vector3 get_point()`
  （三维向量 get_point（））
- `void set_point(Vector3 value)`
  （void set_point（三维向量 value））
- `void Hit(Vector3 force, AnimationCurve[] curves, Vector3 point)`
  （void 命中（三维向量 force, 动画Curve[] curves, 三维向量 point））
- `void Apply(VRIK ik, AnimationCurve[] curves, float weight)`
  （void 应用（VRIK ik, 动画Curve[] curves, float weight））

---

## HitReactionVRIK.PositionOffset（命中ReactionVRIK.PositionOffset）

**继承**: HitReactionVRIK.Offset（命中ReactionVRIK.Offset）

### 字段 (3)

- `int forceDirCurveIndex`（int forceDirCurve索引）(偏移: 0x40)
- `int upDirCurveIndex`（int upDirCurve索引）(偏移: 0x44)
- `HitReactionVRIK.PositionOffset.PositionOffsetLink[] offsetLinks`（命中ReactionVRIK.PositionOffset.PositionOffsetLink[] offsetLinks）(偏移: 0x48)

### 方法 (3)

- `float GetLength(AnimationCurve[] curves)`
  （float 获取Length（动画Curve[] curves））
- `void CrossFadeStart()`
  （void CrossFade开始（））
- `void OnApply(VRIK ik, AnimationCurve[] curves, float weight)`
  （void On应用（VRIK ik, 动画Curve[] curves, float weight））

---

## HitReactionVRIK.PositionOffset.PositionOffsetLink（命中ReactionVRIK.PositionOffset.PositionOffsetLink）

### 字段 (4)

- `IKSolverVR.PositionOffset positionOffset`（IKSolverVR.PositionOffset positionOffset）(偏移: 0x8)
- `float weight`（float weight）(偏移: 0xC)
- `Vector3 lastValue`（三维向量 last值）(偏移: 0x10)
- `Vector3 current`（三维向量 current）(偏移: 0x1C)

### 方法 (2)

- `void Apply(VRIK ik, Vector3 offset, float crossFader)`
  （void 应用（VRIK ik, 三维向量 offset, float crossFader））
- `void CrossFadeStart()`
  （void CrossFade开始（））

---

## HitReactionVRIK.RotationOffset（命中ReactionVRIK.RotationOffset）

**继承**: HitReactionVRIK.Offset（命中ReactionVRIK.Offset）

### 字段 (3)

- `int curveIndex`（int curve索引）(偏移: 0x40)
- `HitReactionVRIK.RotationOffset.RotationOffsetLink[] offsetLinks`（命中ReactionVRIK.RotationOffset.RotationOffsetLink[] offsetLinks）(偏移: 0x44)
- `Rigidbody rigidbody`（刚体 rigidbody）(偏移: 0x48)

### 方法 (3)

- `float GetLength(AnimationCurve[] curves)`
  （float 获取Length（动画Curve[] curves））
- `void CrossFadeStart()`
  （void CrossFade开始（））
- `void OnApply(VRIK ik, AnimationCurve[] curves, float weight)`
  （void On应用（VRIK ik, 动画Curve[] curves, float weight））

---

## HitReactionVRIK.RotationOffset.RotationOffsetLink（命中ReactionVRIK.RotationOffset.RotationOffsetLink）

### 字段 (4)

- `IKSolverVR.RotationOffset rotationOffset`（IKSolverVR.RotationOffset rotationOffset）(偏移: 0x8)
- `float weight`（float weight）(偏移: 0xC)
- `Quaternion lastValue`（Quaternion last值）(偏移: 0x10)
- `Quaternion current`（Quaternion current）(偏移: 0x20)

### 方法 (2)

- `void Apply(VRIK ik, Quaternion offset, float crossFader)`
  （void 应用（VRIK ik, Quaternion offset, float crossFader））
- `void CrossFadeStart()`
  （void CrossFade开始（））

---

## HorizontalLayoutGroup（水平Layout组）

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

## HorizontalOrVerticalLayoutGroup（水平Or垂直Layout组）

**继承**: LayoutGroup（Layout组）

### 字段 (8)

- `float m_Spacing`（float m_Spacing）(偏移: 0x38)
- `bool m_ChildForceExpandWidth`（bool m_子级强制Expand宽度）(偏移: 0x3C)
- `bool m_ChildForceExpandHeight`（bool m_子级强制Expand高度）(偏移: 0x3D)
- `bool m_ChildControlWidth`（bool m_子级控制宽度）(偏移: 0x3E)
- `bool m_ChildControlHeight`（bool m_子级控制高度）(偏移: 0x3F)
- `bool m_ChildScaleWidth`（bool m_子级缩放宽度）(偏移: 0x40)
- `bool m_ChildScaleHeight`（bool m_子级缩放高度）(偏移: 0x41)
- `bool m_ReverseArrangement`（bool m_ReverseArrangement）(偏移: 0x42)

### 方法 (19)

- `float get_spacing()`
  （float get_spacing（））
- `void set_spacing(float value)`
  （void set_spacing（float value））
- `bool get_childForceExpandWidth()`
  （bool get_child强制Expand宽度（））
- `void set_childForceExpandWidth(bool value)`
  （void set_child强制Expand宽度（bool value））
- `bool get_childForceExpandHeight()`
  （bool get_child强制Expand高度（））
- `void set_childForceExpandHeight(bool value)`
  （void set_child强制Expand高度（bool value））
- `bool get_childControlWidth()`
  （bool get_child控制宽度（））
- `void set_childControlWidth(bool value)`
  （void set_child控制宽度（bool value））
- `bool get_childControlHeight()`
  （bool get_child控制高度（））
- `void set_childControlHeight(bool value)`
  （void set_child控制高度（bool value））
- `bool get_childScaleWidth()`
  （bool get_child缩放宽度（））
- `void set_childScaleWidth(bool value)`
  （void set_child缩放宽度（bool value））
- `bool get_childScaleHeight()`
  （bool get_child缩放高度（））
- `void set_childScaleHeight(bool value)`
  （void set_child缩放高度（bool value））
- `bool get_reverseArrangement()`
  （bool get_reverseArrangement（））
- `void set_reverseArrangement(bool value)`
  （void set_reverseArrangement（bool value））
- `void CalcAlongAxis(int axis, bool isVertical)`
  （void CalcAlong轴（int axis, bool isVertical））
- `void SetChildrenAlongAxis(int axis, bool isVertical)`
  （void 集合ChildrenAlong轴（int axis, bool isVertical））
- `void GetChildSizes(RectTransform child, int axis, bool controlSize, bool childForceExpand, out float min, out float preferred, out float flexible)`
  （void 获取子级Sizes（Rect变换 child, int axis, bool controlSize, bool childForceExpand, out float min, out float preferred, out float flexible））

---

## HorizontalWrapMode（水平Wrap模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## HttpWebRequestElement（HttpWeb请求元素）

**继承**: ConfigurationElement（Configuration元素）

### 方法 (1)

- `ConfigurationPropertyCollection get_Properties()`
  （Configuration属性Collection get_Properties（））

---

## HumanBodyBones（人类身体Bones）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## HumanBone（人类Bone）

### 字段 (3)

- `string m_BoneName`（string m_Bone名称）(偏移: 0x0)
- `string m_HumanName`（string m_人类名称）(偏移: 0x4)
- `HumanLimit limit`（人类Limit limit）(偏移: 0x8)

---

## HumanCatchFeature（人类CatchFeature）

**继承**: ScriptableRendererFeature（Scriptable渲染器Feature）

### 字段 (4)

- `Material overrideMat`（材质 override材质）(偏移: 0x10)
- `LayerMask layerMask`（层掩码 layer掩码）(偏移: 0x14)
- `RenderPassEvent passEvent`（RenderPass事件 pass事件）(偏移: 0x18)
- `HumanCatchPass humanCatchPass`（人类CatchPass humanCatchPass）(偏移: 0x1C)

### 方法 (2)

- `void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)`
  （void 添加RenderPasses（Scriptable渲染器 renderer, ref RenderingData renderingData））
- `void Create()`
  （void 创建（））

---

## HumanCatchPass（人类CatchPass）

**继承**: ScriptableRenderPass（ScriptableRenderPass）

### 字段 (3)

- `Material mat`（材质 mat）(偏移: 0x54)
- `RenderStateBlock m_RenderStateBlock`（Render状态Block m_Render状态Block）(偏移: 0x58)
- `FilteringSettings m_FilteringSettings`（FilteringSettings m_FilteringSettings）(偏移: 0xC4)

### 方法 (1)

- `void Execute(ScriptableRenderContext context, ref RenderingData renderingData)`
  （void 执行（ScriptableRenderContext context, ref RenderingData renderingData））

---

## HumanDescription（人类Description）

### 字段 (14)

- `HumanBone[] human`（人类Bone[] human）(偏移: 0x0)
- `SkeletonBone[] skeleton`（SkeletonBone[] skeleton）(偏移: 0x4)
- `float m_ArmTwist`（float m_手臂Twist）(偏移: 0x8)
- `float m_ForeArmTwist`（float m_Fore手臂Twist）(偏移: 0xC)
- `float m_UpperLegTwist`（float m_上半身腿部Twist）(偏移: 0x10)
- `float m_LegTwist`（float m_腿部Twist）(偏移: 0x14)
- `float m_ArmStretch`（float m_手臂Stretch）(偏移: 0x18)
- `float m_LegStretch`（float m_腿部Stretch）(偏移: 0x1C)
- `float m_FeetSpacing`（float m_FeetSpacing）(偏移: 0x20)
- `float m_GlobalScale`（float m_全局的缩放）(偏移: 0x24)
- `string m_RootMotionBoneName`（string m_根MotionBone名称）(偏移: 0x28)
- `bool m_HasTranslationDoF`（bool m_是否有TranslationDoF）(偏移: 0x2C)
- `bool m_HasExtraRoot`（bool m_是否有额外的根）(偏移: 0x2D)
- `bool m_SkeletonHasParents`（bool m_Skeleton是否有Parents）(偏移: 0x2E)

---

## HumanLimit（人类Limit）

### 字段 (5)

- `Vector3 m_Min`（三维向量 m_最小）(偏移: 0x0)
- `Vector3 m_Max`（三维向量 m_最大）(偏移: 0xC)
- `Vector3 m_Center`（三维向量 m_中心）(偏移: 0x18)
- `float m_AxisLength`（float m_轴Length）(偏移: 0x24)
- `int m_UseDefaultValues`（int m_Use默认的Values）(偏移: 0x28)

---

## HumanPose（人类Pose）

### 字段 (3)

- `Vector3 bodyPosition`（三维向量 bodyPosition）(偏移: 0x0)
- `Quaternion bodyRotation`（Quaternion bodyRotation）(偏移: 0xC)
- `float[] muscles`（float[] muscles）(偏移: 0x1C)

### 方法 (1)

- `void Init()`
  （void 初始化（））

---

## HumanPoseHandler（人类Pose处理器）

**继承**: IDisposable（IDisposable）

### 字段 (1)

- `IntPtr m_Ptr`（整数Ptr m_Ptr）(偏移: 0x8)

### 方法 (5)

- `IntPtr Internal_CreateFromRoot(Avatar avatar, Transform root)`
  （整数Ptr Internal_创建From根（Avatar avatar, 变换 root））
- `void Internal_Destroy(IntPtr ptr)`
  （void Internal_销毁（整数Ptr ptr））
- `void GetHumanPose(out Vector3 bodyPosition, out Quaternion bodyRotation, [Out] float[] muscles)`
  （void 获取人类Pose（out Vector3 bodyPosition, out Quaternion bodyRotation, [Out] float[] muscles））
- `void Dispose()`
  （void 释放（））
- `void GetHumanPose(ref HumanPose humanPose)`
  （void 获取人类Pose（ref HumanPose humanPose））

---

## HumanTrait（人类Trait）

### 方法 (3)

- `int get_MuscleCount()`
  （int get_Muscle数量（））
- `int GetBoneIndexFromMono(int humanId)`
  （int 获取Bone索引FromMono（int humanId））
- `string[] get_MuscleName()`
  （string[] get_Muscle名称（））

---

## HumanoidBaker（HumanoidBaker）

**继承**: Baker（Baker）

### 字段 (16)

- `bool bakeHandIK`（bool bake手部IK）(偏移: 0x44)
- `float IKKeyReductionError`（float IK键ReductionError）(偏移: 0x48)
- `int muscleFrameRateDiv`（int muscleFrameRateDiv）(偏移: 0x4C)
- `BakerMuscle[] bakerMuscles`（BakerMuscle[] bakerMuscles）(偏移: 0x50)
- `BakerHumanoidQT rootQT`（BakerHumanoidQT rootQT）(偏移: 0x54)
- `BakerHumanoidQT leftFootQT`（BakerHumanoidQT left脚部QT）(偏移: 0x58)
- `BakerHumanoidQT rightFootQT`（BakerHumanoidQT right脚部QT）(偏移: 0x5C)
- `BakerHumanoidQT leftHandQT`（BakerHumanoidQT left手部QT）(偏移: 0x60)
- `BakerHumanoidQT rightHandQT`（BakerHumanoidQT right手部QT）(偏移: 0x64)
- `float[] muscles`（float[] muscles）(偏移: 0x68)
- `HumanPose pose`（人类Pose pose）(偏移: 0x6C)
- `HumanPoseHandler handler`（人类Pose处理器 handler）(偏移: 0x8C)
- `Vector3 bodyPosition`（三维向量 bodyPosition）(偏移: 0x90)
- `Quaternion bodyRotation`（Quaternion bodyRotation）(偏移: 0x9C)
- `int mN`（int mN）(偏移: 0xAC)
- `Quaternion lastBodyRotation`（Quaternion last身体Rotation）(偏移: 0xB0)

### 方法 (7)

- `void Awake()`
  （void Awake（））
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
- `void UpdateHumanPose()`
  （void 更新人类Pose（））

---

## HybridDictionary（Hybrid字典）

**继承**: IDictionary, ICollection, IEnumerable（I字典, ICollection, IEnumerable）

### 字段 (3)

- `ListDictionary list`（列表字典 list）(偏移: 0x8)
- `Hashtable hashtable`（Hashtable hashtable）(偏移: 0xC)
- `bool caseInsensitive`（bool caseInsensitive）(偏移: 0x10)

### 方法 (10)

- `object get_Item(object key)`
  （object get_项目（object key））
- `void set_Item(object key, object value)`
  （void set_项目（object key, object value））
- `ListDictionary get_List()`
  （列表字典 get_列表（））
- `void ChangeOver()`
  （void ChangeOver（））
- `int get_Count()`
  （int get_数量（））
- `object get_SyncRoot()`
  （object get_同步根（））
- `bool Contains(object key)`
  （bool Contains（object key））
- `void CopyTo(Array array, int index)`
  （void 复制To（数组 array, int index））
- `IDictionaryEnumerator GetEnumerator()`
  （I字典Enumerator 获取Enumerator（））
- `void Remove(object key)`
  （void 移除（object key））

---

## IDAttribute（IDAttribute）

**继承**: Attribute（Attribute）

### 字段 (1)

- `string _id`（string _id）(偏移: 0x8)

### 方法 (1)

- `string get_Id()`
  （string get_Id（））

---

## IK（IK）

**继承**: SolverManager（Solver管理器）

### 方法 (3)

- `void UpdateSolver()`
  （void 更新Solver（））
- `void InitiateSolver()`
  （void InitiateSolver（））
- `void FixTransforms()`
  （void FixTransforms（））

---

## IKConstraintBend（IKConstraintBend）

### 字段 (17)

- `Transform bone1`（变换 bone1）(偏移: 0x8)
- `Transform bone2`（变换 bone2）(偏移: 0xC)
- `Transform bone3`（变换 bone3）(偏移: 0x10)
- `Transform bendGoal`（变换 bendGoal）(偏移: 0x14)
- `Vector3 direction`（三维向量 direction）(偏移: 0x18)
- `Quaternion rotationOffset`（Quaternion rotationOffset）(偏移: 0x24)
- `float weight`（float weight）(偏移: 0x34)
- `Vector3 defaultLocalDirection`（三维向量 default本地的方向）(偏移: 0x38)
- `Vector3 defaultChildDirection`（三维向量 default子级方向）(偏移: 0x44)
- `float clampF`（float clampF）(偏移: 0x50)
- `int chainIndex1`（int chainIndex1）(偏移: 0x54)
- `int nodeIndex1`（int nodeIndex1）(偏移: 0x58)
- `int chainIndex2`（int chainIndex2）(偏移: 0x5C)
- `int nodeIndex2`（int nodeIndex2）(偏移: 0x60)
- `int chainIndex3`（int chainIndex3）(偏移: 0x64)
- `int nodeIndex3`（int nodeIndex3）(偏移: 0x68)
- `bool limbOrientationsSet`（bool limbOrientations集合）(偏移: 0x6D)

### 方法 (10)

- `bool IsValid(IKSolverFullBody solver, Warning.Logger logger)`
  （bool 是否Valid（IKSolver满身体 solver, Warning.Logger logger））
- `bool get_initiated()`
  （bool get_initiated（））
- `void set_initiated(bool value)`
  （void set_initiated（bool value））
- `void SetBones(Transform bone1, Transform bone2, Transform bone3)`
  （void 集合Bones（变换 bone1, 变换 bone2, 变换 bone3））
- `void Initiate(IKSolverFullBody solver)`
  （void Initiate（IKSolver满身体 solver））
- `void SetLimbOrientation(Vector3 upper, Vector3 lower, Vector3 last)`
  （void 集合LimbOrientation（三维向量 upper, 三维向量 lower, 三维向量 last））
- `void LimitBend(float solverWeight, float positionWeight)`
  （void LimitBend（float solverWeight, float positionWeight））
- `Vector3 GetDir(IKSolverFullBody solver)`
  （三维向量 获取Dir（IKSolver满身体 solver））
- `Vector3 OrthoToLimb(IKSolverFullBody solver, Vector3 tangent)`
  （三维向量 OrthoToLimb（IKSolver满身体 solver, 三维向量 tangent））
- `Vector3 OrthoToBone1(IKSolverFullBody solver, Vector3 tangent)`
  （三维向量 OrthoToBone1（IKSolver满身体 solver, 三维向量 tangent））

---

## IKEffector（IKEffector）

### 字段 (31)

- `Transform bone`（变换 bone）(偏移: 0x8)
- `Transform target`（变换 target）(偏移: 0xC)
- `float positionWeight`（float positionWeight）(偏移: 0x10)
- `float rotationWeight`（float rotationWeight）(偏移: 0x14)
- `Vector3 position`（三维向量 position）(偏移: 0x18)
- `Quaternion rotation`（Quaternion rotation）(偏移: 0x24)
- `Vector3 positionOffset`（三维向量 positionOffset）(偏移: 0x34)
- `bool effectChildNodes`（bool effect子级Nodes）(偏移: 0x41)
- `float maintainRelativePositionWeight`（float maintainRelativePositionWeight）(偏移: 0x44)
- `Transform[] childBones`（Transform[] childBones）(偏移: 0x48)
- `Transform planeBone1`（变换 planeBone1）(偏移: 0x4C)
- `Transform planeBone2`（变换 planeBone2）(偏移: 0x50)
- `Transform planeBone3`（变换 planeBone3）(偏移: 0x54)
- `Quaternion planeRotationOffset`（Quaternion planeRotationOffset）(偏移: 0x58)
- `float posW`（float posW）(偏移: 0x68)
- `float rotW`（float rotW）(偏移: 0x6C)
- `Vector3[] localPositions`（Vector3[] localPositions）(偏移: 0x70)
- `bool usePlaneNodes`（bool usePlaneNodes）(偏移: 0x74)
- `Quaternion animatedPlaneRotation`（Quaternion animatedPlaneRotation）(偏移: 0x78)
- `Vector3 animatedPosition`（三维向量 animatedPosition）(偏移: 0x88)
- `bool firstUpdate`（bool first更新）(偏移: 0x94)
- `int chainIndex`（int chain索引）(偏移: 0x98)
- `int nodeIndex`（int node索引）(偏移: 0x9C)
- `int plane1ChainIndex`（int plane1Chain索引）(偏移: 0xA0)
- `int plane1NodeIndex`（int plane1节点索引）(偏移: 0xA4)
- `int plane2ChainIndex`（int plane2Chain索引）(偏移: 0xA8)
- `int plane2NodeIndex`（int plane2节点索引）(偏移: 0xAC)
- `int plane3ChainIndex`（int plane3Chain索引）(偏移: 0xB0)
- `int plane3NodeIndex`（int plane3节点索引）(偏移: 0xB4)
- `int[] childChainIndexes`（int[] childChainIndexes）(偏移: 0xB8)
- `int[] childNodeIndexes`（int[] child节点Indexes）(偏移: 0xBC)

### 方法 (13)

- `IKSolver.Node GetNode(IKSolverFullBody solver)`
  （IKSolver.节点 获取节点（IKSolver满身体 solver））
- `bool get_isEndEffector()`
  （bool get_is结束Effector（））
- `void set_isEndEffector(bool value)`
  （void set_is结束Effector（bool value））
- `void PinToBone(float positionWeight, float rotationWeight)`
  （void PinToBone（float positionWeight, float rotationWeight））
- `bool IsValid(IKSolver solver, ref string message)`
  （bool 是否Valid（IKSolver solver, ref string message））
- `void Initiate(IKSolverFullBody solver)`
  （void Initiate（IKSolver满身体 solver））
- `void ResetOffset(IKSolverFullBody solver)`
  （void 重置Offset（IKSolver满身体 solver））
- `void SetToTarget()`
  （void 集合To目标（））
- `void OnPreSolve(IKSolverFullBody solver)`
  （void OnPreSolve（IKSolver满身体 solver））
- `void OnPostWrite()`
  （void OnPostWrite（））
- `Quaternion GetPlaneRotation(IKSolverFullBody solver)`
  （Quaternion 获取PlaneRotation（IKSolver满身体 solver））
- `void Update(IKSolverFullBody solver)`
  （void 更新（IKSolver满身体 solver））
- `Vector3 GetPosition(IKSolverFullBody solver, out Quaternion planeRotationOffset)`
  （三维向量 获取Position（IKSolver满身体 solver, out Quaternion planeRotationOffset））

---

## IKExecutionOrder（IKExecutionOrder）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (3)

- `IK[] IKComponents`（IK[] IKComponents）(偏移: 0xC)
- `Animator animator`（动画器 animator）(偏移: 0x10)
- `bool fixedFrame`（bool fixedFrame）(偏移: 0x14)

### 方法 (6)

- `bool get_animatePhysics()`
  （bool get_animate物理（））
- `void Start()`
  （void 开始（））
- `void Update()`
  （void 更新（））
- `void FixedUpdate()`
  （void 固定更新（））
- `void LateUpdate()`
  （void 延迟更新（））
- `void FixTransforms()`
  （void FixTransforms（））

---

## IKMapping（IKMapping）

### 方法 (4)

- `bool IsValid(IKSolver solver, ref string message)`
  （bool 是否Valid（IKSolver solver, ref string message））
- `void Initiate(IKSolverFullBody solver)`
  （void Initiate（IKSolver满身体 solver））
- `bool BoneIsValid(Transform bone, IKSolver solver, ref string message, Warning.Logger logger)`
  （bool Bone是否Valid（变换 bone, IKSolver solver, ref string message, Warning.Logger logger））
- `Vector3 SolveFABRIKJoint(Vector3 pos1, Vector3 pos2, float length)`
  （三维向量 SolveFABRIKJoint（三维向量 pos1, 三维向量 pos2, float length））

---

## IKMapping.BoneMap（IKMapping.Bone映射）

### 字段 (22)

- `Transform transform`（变换 transform）(偏移: 0x8)
- `int chainIndex`（int chain索引）(偏移: 0xC)
- `int nodeIndex`（int node索引）(偏移: 0x10)
- `Vector3 defaultLocalPosition`（三维向量 default本地的Position）(偏移: 0x14)
- `Quaternion defaultLocalRotation`（Quaternion default本地的Rotation）(偏移: 0x20)
- `Vector3 localSwingAxis`（三维向量 localSwing轴）(偏移: 0x30)
- `Vector3 localTwistAxis`（三维向量 localTwist轴）(偏移: 0x3C)
- `Vector3 planePosition`（三维向量 planePosition）(偏移: 0x48)
- `Vector3 ikPosition`（三维向量 ikPosition）(偏移: 0x54)
- `Quaternion defaultLocalTargetRotation`（Quaternion default本地的目标Rotation）(偏移: 0x60)
- `Quaternion maintainRotation`（Quaternion maintainRotation）(偏移: 0x70)
- `float length`（float length）(偏移: 0x80)
- `Quaternion animatedRotation`（Quaternion animatedRotation）(偏移: 0x84)
- `Transform planeBone1`（变换 planeBone1）(偏移: 0x94)
- `Transform planeBone2`（变换 planeBone2）(偏移: 0x98)
- `Transform planeBone3`（变换 planeBone3）(偏移: 0x9C)
- `int plane1ChainIndex`（int plane1Chain索引）(偏移: 0xA0)
- `int plane1NodeIndex`（int plane1节点索引）(偏移: 0xA4)
- `int plane2ChainIndex`（int plane2Chain索引）(偏移: 0xA8)
- `int plane2NodeIndex`（int plane2节点索引）(偏移: 0xAC)
- `int plane3ChainIndex`（int plane3Chain索引）(偏移: 0xB0)
- `int plane3NodeIndex`（int plane3节点索引）(偏移: 0xB4)

### 方法 (25)

- `void Initiate(Transform transform, IKSolverFullBody solver)`
  （void Initiate（变换 transform, IKSolver满身体 solver））
- `Vector3 get_swingDirection()`
  （三维向量 get_swing方向（））
- `void StoreDefaultLocalState()`
  （void 商店默认的本地的状态（））
- `void FixTransform(bool position)`
  （void Fix变换（bool position））
- `bool get_isNodeBone()`
  （bool get_is节点Bone（））
- `void SetLength(IKMapping.BoneMap nextBone)`
  （void 集合Length（IKMapping.Bone映射 nextBone））
- `void SetLocalSwingAxis(IKMapping.BoneMap swingTarget)`
  （void 集合本地的Swing轴（IKMapping.Bone映射 swingTarget））
- `void SetLocalSwingAxis(IKMapping.BoneMap bone1, IKMapping.BoneMap bone2)`
  （void 集合本地的Swing轴（IKMapping.Bone映射 bone1, IKMapping.Bone映射 bone2））
- `void SetLocalTwistAxis(Vector3 twistDirection, Vector3 normalDirection)`
  （void 集合本地的Twist轴（三维向量 twistDirection, 三维向量 normalDirection））
- `void SetPlane(IKSolverFullBody solver, Transform planeBone1, Transform planeBone2, Transform planeBone3)`
  （void 集合Plane（IKSolver满身体 solver, 变换 planeBone1, 变换 planeBone2, 变换 planeBone3））
- `void UpdatePlane(bool rotation, bool position)`
  （void 更新Plane（bool rotation, bool position））
- `void SetIKPosition()`
  （void 集合IKPosition（））
- `void MaintainRotation()`
  （void MaintainRotation（））
- `void SetToIKPosition()`
  （void 集合ToIKPosition（））
- `void FixToNode(IKSolverFullBody solver, float weight, IKSolver.Node fixNode)`
  （void FixTo节点（IKSolver满身体 solver, float weight, IKSolver.节点 fixNode））
- `Vector3 GetPlanePosition(IKSolverFullBody solver)`
  （三维向量 获取PlanePosition（IKSolver满身体 solver））
- `void PositionToPlane(IKSolverFullBody solver)`
  （void PositionToPlane（IKSolver满身体 solver））
- `void RotateToPlane(IKSolverFullBody solver, float weight)`
  （void RotateToPlane（IKSolver满身体 solver, float weight））
- `void Swing(Vector3 swingTarget, float weight)`
  （void Swing（三维向量 swingTarget, float weight））
- `void Swing(Vector3 pos1, Vector3 pos2, float weight)`
  （void Swing（三维向量 pos1, 三维向量 pos2, float weight））
- `void Twist(Vector3 twistDirection, Vector3 normalDirection, float weight)`
  （void Twist（三维向量 twistDirection, 三维向量 normalDirection, float weight））
- `void RotateToMaintain(float weight)`
  （void RotateToMaintain（float weight））
- `void RotateToEffector(IKSolverFullBody solver, float weight)`
  （void RotateToEffector（IKSolver满身体 solver, float weight））
- `Quaternion GetTargetRotation(IKSolverFullBody solver)`
  （Quaternion 获取目标Rotation（IKSolver满身体 solver））
- `Quaternion get_lastAnimatedTargetRotation()`
  （Quaternion get_lastAnimated目标Rotation（））

---

## IKMappingBone（IKMappingBone）

**继承**: IKMapping（IKMapping）

### 字段 (3)

- `Transform bone`（变换 bone）(偏移: 0x8)
- `float maintainRotationWeight`（float maintainRotationWeight）(偏移: 0xC)
- `IKMapping.BoneMap boneMap`（IKMapping.Bone映射 bone映射）(偏移: 0x10)

### 方法 (6)

- `bool IsValid(IKSolver solver, ref string message)`
  （bool 是否Valid（IKSolver solver, ref string message））
- `void StoreDefaultLocalState()`
  （void 商店默认的本地的状态（））
- `void FixTransforms()`
  （void FixTransforms（））
- `void Initiate(IKSolverFullBody solver)`
  （void Initiate（IKSolver满身体 solver））
- `void ReadPose()`
  （void ReadPose（））
- `void WritePose(float solverWeight)`
  （void WritePose（float solverWeight））

---

## IKMappingLimb（IKMappingLimb）

**继承**: IKMapping（IKMapping）

### 字段 (11)

- `Transform parentBone`（变换 parentBone）(偏移: 0x8)
- `Transform bone1`（变换 bone1）(偏移: 0xC)
- `Transform bone2`（变换 bone2）(偏移: 0x10)
- `Transform bone3`（变换 bone3）(偏移: 0x14)
- `float maintainRotationWeight`（float maintainRotationWeight）(偏移: 0x18)
- `float weight`（float weight）(偏移: 0x1C)
- `bool updatePlaneRotations`（bool updatePlaneRotations）(偏移: 0x20)
- `IKMapping.BoneMap boneMapParent`（IKMapping.Bone映射 bone映射父级）(偏移: 0x24)
- `IKMapping.BoneMap boneMap1`（IKMapping.Bone映射 boneMap1）(偏移: 0x28)
- `IKMapping.BoneMap boneMap2`（IKMapping.Bone映射 boneMap2）(偏移: 0x2C)
- `IKMapping.BoneMap boneMap3`（IKMapping.Bone映射 boneMap3）(偏移: 0x30)

### 方法 (9)

- `bool IsValid(IKSolver solver, ref string message)`
  （bool 是否Valid（IKSolver solver, ref string message））
- `IKMapping.BoneMap GetBoneMap(IKMappingLimb.BoneMapType boneMap)`
  （IKMapping.Bone映射 获取Bone映射（IKMappingLimb.Bone映射类型 boneMap））
- `void SetLimbOrientation(Vector3 upper, Vector3 lower)`
  （void 集合LimbOrientation（三维向量 upper, 三维向量 lower））
- `void SetBones(Transform bone1, Transform bone2, Transform bone3, Transform parentBone)`
  （void 集合Bones（变换 bone1, 变换 bone2, 变换 bone3, 变换 parentBone））
- `void StoreDefaultLocalState()`
  （void 商店默认的本地的状态（））
- `void FixTransforms()`
  （void FixTransforms（））
- `void Initiate(IKSolverFullBody solver)`
  （void Initiate（IKSolver满身体 solver））
- `void ReadPose()`
  （void ReadPose（））
- `void WritePose(IKSolverFullBody solver, bool fullBody)`
  （void WritePose（IKSolver满身体 solver, bool fullBody））

---

## IKMappingLimb.BoneMapType（IKMappingLimb.Bone映射类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## IKMappingSpine（IKMappingSpine）

**继承**: IKMapping（IKMapping）

### 字段 (14)

- `Transform[] spineBones`（Transform[] spineBones）(偏移: 0x8)
- `Transform leftUpperArmBone`（变换 left上半身手臂Bone）(偏移: 0xC)
- `Transform rightUpperArmBone`（变换 right上半身手臂Bone）(偏移: 0x10)
- `Transform leftThighBone`（变换 leftThighBone）(偏移: 0x14)
- `Transform rightThighBone`（变换 rightThighBone）(偏移: 0x18)
- `int iterations`（int iterations）(偏移: 0x1C)
- `float twistWeight`（float twistWeight）(偏移: 0x20)
- `int rootNodeIndex`（int root节点索引）(偏移: 0x24)
- `IKMapping.BoneMap[] spine`（IKMapping.BoneMap[] spine）(偏移: 0x28)
- `IKMapping.BoneMap leftUpperArm`（IKMapping.Bone映射 left上半身手臂）(偏移: 0x2C)
- `IKMapping.BoneMap rightUpperArm`（IKMapping.Bone映射 right上半身手臂）(偏移: 0x30)
- `IKMapping.BoneMap leftThigh`（IKMapping.Bone映射 leftThigh）(偏移: 0x34)
- `IKMapping.BoneMap rightThigh`（IKMapping.Bone映射 rightThigh）(偏移: 0x38)
- `bool useFABRIK`（bool useFABRIK）(偏移: 0x3C)

### 方法 (11)

- `bool IsValid(IKSolver solver, ref string message)`
  （bool 是否Valid（IKSolver solver, ref string message））
- `void SetBones(Transform[] spineBones, Transform leftUpperArmBone, Transform rightUpperArmBone, Transform leftThighBone, Transform rightThighBone)`
  （void 集合Bones（Transform[] spineBones, 变换 leftUpperArmBone, 变换 rightUpperArmBone, 变换 leftThighBone, 变换 rightThighBone））
- `void StoreDefaultLocalState()`
  （void 商店默认的本地的状态（））
- `void FixTransforms()`
  （void FixTransforms（））
- `void Initiate(IKSolverFullBody solver)`
  （void Initiate（IKSolver满身体 solver））
- `bool UseFABRIK()`
  （bool UseFABRIK（））
- `void ReadPose()`
  （void ReadPose（））
- `void WritePose(IKSolverFullBody solver)`
  （void WritePose（IKSolver满身体 solver））
- `void ForwardReach(Vector3 position)`
  （void 前进Reach（三维向量 position））
- `void BackwardReach(Vector3 position)`
  （void 后退Reach（三维向量 position））
- `void MapToSolverPositions(IKSolverFullBody solver)`
  （void 映射ToSolverPositions（IKSolver满身体 solver））

---

## IKSolver（IKSolver）

### 字段 (8)

- `Vector3 IKPosition`（三维向量 IKPosition）(偏移: 0x8)
- `float IKPositionWeight`（float IKPositionWeight）(偏移: 0x14)
- `IKSolver.UpdateDelegate OnPreInitiate`（IKSolver.更新委托 OnPreInitiate）(偏移: 0x1C)
- `IKSolver.UpdateDelegate OnPostInitiate`（IKSolver.更新委托 OnPostInitiate）(偏移: 0x20)
- `IKSolver.UpdateDelegate OnPreUpdate`（IKSolver.更新委托 OnPre更新）(偏移: 0x24)
- `IKSolver.UpdateDelegate OnPostUpdate`（IKSolver.更新委托 OnPost更新）(偏移: 0x28)
- `bool firstInitiation`（bool firstInitiation）(偏移: 0x2C)
- `Transform root`（变换 root）(偏移: 0x30)

### 方法 (14)

- `bool IsValid()`
  （bool 是否Valid（））
- `void Initiate(Transform root)`
  （void Initiate（变换 root））
- `void Update()`
  （void 更新（））
- `Vector3 GetIKPosition()`
  （三维向量 获取IKPosition（））
- `void SetIKPosition(Vector3 position)`
  （void 集合IKPosition（三维向量 position））
- `float GetIKPositionWeight()`
  （float 获取IKPositionWeight（））
- `void SetIKPositionWeight(float weight)`
  （void 集合IKPositionWeight（float weight））
- `Transform GetRoot()`
  （变换 获取根（））
- `bool get_initiated()`
  （bool get_initiated（））
- `void set_initiated(bool value)`
  （void set_initiated（bool value））
- `void LogWarning(string message)`
  （void LogWarning（string message））
- `Transform ContainsDuplicateBone(IKSolver.Bone[] bones)`
  （变换 ContainsDuplicateBone（IKSolver.Bone[] bones））
- `bool HierarchyIsValid(IKSolver.Bone[] bones)`
  （bool Hierarchy是否Valid（IKSolver.Bone[] bones））
- `float PreSolveBones(ref IKSolver.Bone[] bones)`
  （float PreSolveBones（ref IKSolver.Bone[] bones））

---

## IKSolver.Bone（IKSolver.Bone）

**继承**: IKSolver.Point（IKSolver.Point）

### 字段 (5)

- `float length`（float length）(偏移: 0x48)
- `float sqrMag`（float sqrMag）(偏移: 0x4C)
- `Vector3 axis`（三维向量 axis）(偏移: 0x50)
- `RotationLimit _rotationLimit`（RotationLimit _rotationLimit）(偏移: 0x5C)
- `bool isLimited`（bool is限制）(偏移: 0x60)

### 方法 (6)

- `RotationLimit get_rotationLimit()`
  （RotationLimit get_rotationLimit（））
- `void set_rotationLimit(RotationLimit value)`
  （void set_rotationLimit（RotationLimit value））
- `void Swing(Vector3 swingTarget, float weight = 1)`
  （void Swing（三维向量 swingTarget, float weight = 1））
- `void SolverSwing(IKSolver.Bone[] bones, int index, Vector3 swingTarget, float weight = 1)`
  （void SolverSwing（IKSolver.Bone[] bones, int index, 三维向量 swingTarget, float weight = 1））
- `void Swing2D(Vector3 swingTarget, float weight = 1)`
  （void Swing2D（三维向量 swingTarget, float weight = 1））
- `void SetToSolverPosition()`
  （void 集合ToSolverPosition（））

---

## IKSolver.IterationDelegate（IKSolver.Iteration委托）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(int i)`
  （void Invoke（int i））
- `IAsyncResult BeginInvoke(int i, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（int i, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## IKSolver.Node（IKSolver.节点）

**继承**: IKSolver.Point（IKSolver.Point）

### 字段 (4)

- `float length`（float length）(偏移: 0x48)
- `float effectorPositionWeight`（float effectorPositionWeight）(偏移: 0x4C)
- `float effectorRotationWeight`（float effectorRotationWeight）(偏移: 0x50)
- `Vector3 offset`（三维向量 offset）(偏移: 0x54)

---

## IKSolver.Point（IKSolver.Point）

### 字段 (6)

- `Transform transform`（变换 transform）(偏移: 0x8)
- `float weight`（float weight）(偏移: 0xC)
- `Vector3 solverPosition`（三维向量 solverPosition）(偏移: 0x10)
- `Quaternion solverRotation`（Quaternion solverRotation）(偏移: 0x1C)
- `Vector3 defaultLocalPosition`（三维向量 default本地的Position）(偏移: 0x2C)
- `Quaternion defaultLocalRotation`（Quaternion default本地的Rotation）(偏移: 0x38)

### 方法 (6)

- `void StoreDefaultLocalState()`
  （void 商店默认的本地的状态（））
- `void FixTransform()`
  （void Fix变换（））
- `void UpdateSolverPosition()`
  （void 更新SolverPosition（））
- `void UpdateSolverLocalPosition()`
  （void 更新Solver本地的Position（））
- `void UpdateSolverState()`
  （void 更新Solver状态（））
- `void UpdateSolverLocalState()`
  （void 更新Solver本地的状态（））

---

## IKSolver.UpdateDelegate（IKSolver.更新委托）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke()`
  （void Invoke（））
- `IAsyncResult BeginInvoke(AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## IKSolverAim（IKSolverAim）

**继承**: IKSolverHeuristic（IKSolverHeuristic）

### 字段 (13)

- `Transform transform`（变换 transform）(偏移: 0x58)
- `Vector3 axis`（三维向量 axis）(偏移: 0x5C)
- `Vector3 poleAxis`（三维向量 pole轴）(偏移: 0x68)
- `Vector3 polePosition`（三维向量 polePosition）(偏移: 0x74)
- `float poleWeight`（float poleWeight）(偏移: 0x80)
- `Transform poleTarget`（变换 pole目标）(偏移: 0x84)
- `float clampWeight`（float clampWeight）(偏移: 0x88)
- `int clampSmoothing`（int clampSmoothing）(偏移: 0x8C)
- `IKSolver.IterationDelegate OnPreIteration`（IKSolver.Iteration委托 OnPreIteration）(偏移: 0x90)
- `float step`（float step）(偏移: 0x94)
- `Vector3 clampedIKPosition`（三维向量 clampedIKPosition）(偏移: 0x98)
- `RotationLimit transformLimit`（RotationLimit transformLimit）(偏移: 0xA4)
- `Transform lastTransform`（变换 last变换）(偏移: 0xA8)

### 方法 (10)

- `float GetAngle()`
  （float 获取角度（））
- `Vector3 get_transformAxis()`
  （三维向量 get_transform轴（））
- `Vector3 get_transformPoleAxis()`
  （三维向量 get_transformPole轴（））
- `void OnInitiate()`
  （void OnInitiate（））
- `void OnUpdate()`
  （void On更新（））
- `int get_minBones()`
  （int get_minBones（））
- `void Solve()`
  （void Solve（））
- `Vector3 GetClampedIKPosition()`
  （三维向量 获取ClampedIKPosition（））
- `void RotateToTarget(Vector3 targetPosition, IKSolver.Bone bone, float weight)`
  （void RotateTo目标（三维向量 targetPosition, IKSolver.Bone bone, float weight））
- `Vector3 get_localDirection()`
  （三维向量 get_local方向（））

---

## IKSolverArm（IKSolver手臂）

**继承**: IKSolver（IKSolver）

### 字段 (11)

- `float IKRotationWeight`（float IKRotationWeight）(偏移: 0x34)
- `Quaternion IKRotation`（Quaternion IKRotation）(偏移: 0x38)
- `IKSolver.Point chest`（IKSolver.Point chest）(偏移: 0x48)
- `IKSolver.Point shoulder`（IKSolver.Point shoulder）(偏移: 0x4C)
- `IKSolver.Point upperArm`（IKSolver.Point upper手臂）(偏移: 0x50)
- `IKSolver.Point forearm`（IKSolver.Point forearm）(偏移: 0x54)
- `IKSolver.Point hand`（IKSolver.Point hand）(偏移: 0x58)
- `bool isLeft`（bool is左）(偏移: 0x5C)
- `IKSolverVR.Arm arm`（IKSolverVR.手臂 arm）(偏移: 0x60)
- `Vector3[] positions`（Vector3[] positions）(偏移: 0x64)
- `Quaternion[] rotations`（Quaternion[] rotations）(偏移: 0x68)

### 方法 (11)

- `bool IsValid(ref string message)`
  （bool 是否Valid（ref string message））
- `bool SetChain(Transform chest, Transform shoulder, Transform upperArm, Transform forearm, Transform hand, Transform root)`
  （bool 集合Chain（变换 chest, 变换 shoulder, 变换 upperArm, 变换 forearm, 变换 hand, 变换 root））
- `IKSolver.Point[] GetPoints()`
  （IKSolver.Point[] 获取Points（））
- `IKSolver.Point GetPoint(Transform transform)`
  （IKSolver.Point 获取Point（变换 transform））
- `void StoreDefaultLocalState()`
  （void 商店默认的本地的状态（））
- `void FixTransforms()`
  （void FixTransforms（））
- `void OnInitiate()`
  （void OnInitiate（））
- `void OnUpdate()`
  （void On更新（））
- `void Solve()`
  （void Solve（））
- `void Read()`
  （void Read（））
- `void Write()`
  （void Write（））

---

## IKSolverCCD（IKSolverCCD）

**继承**: IKSolverHeuristic（IKSolverHeuristic）

### 字段 (1)

- `IKSolver.IterationDelegate OnPreIteration`（IKSolver.Iteration委托 OnPreIteration）(偏移: 0x58)

### 方法 (4)

- `void FadeOutBoneWeights()`
  （void FadeOutBoneWeights（））
- `void OnInitiate()`
  （void OnInitiate（））
- `void OnUpdate()`
  （void On更新（））
- `void Solve(Vector3 targetPosition)`
  （void Solve（三维向量 targetPosition））

---

## IKSolverFABRIK（IKSolverFABRIK）

**继承**: IKSolverHeuristic（IKSolverHeuristic）

### 字段 (3)

- `IKSolver.IterationDelegate OnPreIteration`（IKSolver.Iteration委托 OnPreIteration）(偏移: 0x58)
- `bool[] limitedBones`（bool[] limitedBones）(偏移: 0x5C)
- `Vector3[] solverLocalPositions`（Vector3[] solver本地的Positions）(偏移: 0x60)

### 方法 (24)

- `void SolveForward(Vector3 position)`
  （void Solve前进（三维向量 position））
- `void SolveBackward(Vector3 position)`
  （void Solve后退（三维向量 position））
- `Vector3 GetIKPosition()`
  （三维向量 获取IKPosition（））
- `void OnInitiate()`
  （void OnInitiate（））
- `void OnUpdate()`
  （void On更新（））
- `bool get_boneLengthCanBeZero()`
  （bool get_boneLength能否BeZero（））
- `Vector3 SolveJoint(Vector3 pos1, Vector3 pos2, float length)`
  （三维向量 SolveJoint（三维向量 pos1, 三维向量 pos2, float length））
- `void OnPreSolve()`
  （void OnPreSolve（））
- `void OnPostSolve()`
  （void OnPostSolve（））
- `void Solve(Vector3 targetPosition)`
  （void Solve（三维向量 targetPosition））
- `void ForwardReach(Vector3 position)`
  （void 前进Reach（三维向量 position））
- `void SolverMove(int index, Vector3 offset)`
  （void Solver移动（int index, 三维向量 offset））
- `void SolverRotate(int index, Quaternion rotation, bool recursive)`
  （void SolverRotate（int index, Quaternion rotation, bool recursive））
- `void SolverRotateChildren(int index, Quaternion rotation)`
  （void SolverRotateChildren（int index, Quaternion rotation））
- `void SolverMoveChildrenAroundPoint(int index, Quaternion rotation)`
  （void Solver移动ChildrenAroundPoint（int index, Quaternion rotation））
- `Quaternion GetParentSolverRotation(int index)`
  （Quaternion 获取父级SolverRotation（int index））
- `Vector3 GetParentSolverPosition(int index)`
  （三维向量 获取父级SolverPosition（int index））
- `Quaternion GetLimitedRotation(int index, Quaternion q, out bool changed)`
  （Quaternion 获取限制Rotation（int index, Quaternion q, out bool changed））
- `void LimitForward(int rotateBone, int limitBone)`
  （void Limit前进（int rotateBone, int limitBone））
- `void BackwardReach(Vector3 position)`
  （void 后退Reach（三维向量 position））
- `void BackwardReachUnlimited(Vector3 position)`
  （void 后退ReachUnlimited（三维向量 position））
- `void BackwardReachLimited(Vector3 position)`
  （void 后退Reach限制（三维向量 position））
- `void MapToSolverPositions()`
  （void 映射ToSolverPositions（））
- `void MapToSolverPositionsLimited()`
  （void 映射ToSolverPositions限制（））

---

## IKSolverFABRIKRoot（IKSolverFABRIK根）

**继承**: IKSolver（IKSolver）

### 字段 (6)

- `int iterations`（int iterations）(偏移: 0x34)
- `float rootPin`（float rootPin）(偏移: 0x38)
- `FABRIKChain[] chains`（FABRIKChain[] chains）(偏移: 0x3C)
- `bool zeroWeightApplied`（bool zeroWeightApplied）(偏移: 0x40)
- `bool[] isRoot`（bool[] is根）(偏移: 0x44)
- `Vector3 rootDefaultPosition`（三维向量 root默认的Position）(偏移: 0x48)

### 方法 (10)

- `bool IsValid(ref string message)`
  （bool 是否Valid（ref string message））
- `void StoreDefaultLocalState()`
  （void 商店默认的本地的状态（））
- `void FixTransforms()`
  （void FixTransforms（））
- `void OnInitiate()`
  （void OnInitiate（））
- `bool IsRoot(int index)`
  （bool 是否根（int index））
- `void OnUpdate()`
  （void On更新（））
- `IKSolver.Point[] GetPoints()`
  （IKSolver.Point[] 获取Points（））
- `IKSolver.Point GetPoint(Transform transform)`
  （IKSolver.Point 获取Point（变换 transform））
- `void AddPointsToArray(ref IKSolver.Point[] array, FABRIKChain chain)`
  （void 添加PointsTo数组（ref IKSolver.Point[] array, FABRIKChain chain））
- `Vector3 GetCentroid()`
  （三维向量 获取Centroid（））

---

## IKSolverFullBody（IKSolver满身体）

**继承**: IKSolver（IKSolver）

### 字段 (15)

- `int iterations`（int iterations）(偏移: 0x34)
- `FBIKChain[] chain`（FBIKChain[] chain）(偏移: 0x38)
- `IKEffector[] effectors`（IKEffector[] effectors）(偏移: 0x3C)
- `IKMappingSpine spineMapping`（IKMappingSpine spineMapping）(偏移: 0x40)
- `IKMappingBone[] boneMappings`（IKMappingBone[] boneMappings）(偏移: 0x44)
- `IKMappingLimb[] limbMappings`（IKMappingLimb[] limbMappings）(偏移: 0x48)
- `bool FABRIKPass`（bool FABRIKPass）(偏移: 0x4C)
- `IKSolver.UpdateDelegate OnPreRead`（IKSolver.更新委托 OnPreRead）(偏移: 0x50)
- `IKSolver.UpdateDelegate OnPreSolve`（IKSolver.更新委托 OnPreSolve）(偏移: 0x54)
- `IKSolver.IterationDelegate OnPreIteration`（IKSolver.Iteration委托 OnPreIteration）(偏移: 0x58)
- `IKSolver.IterationDelegate OnPostIteration`（IKSolver.Iteration委托 OnPostIteration）(偏移: 0x5C)
- `IKSolver.UpdateDelegate OnPreBend`（IKSolver.更新委托 OnPreBend）(偏移: 0x60)
- `IKSolver.UpdateDelegate OnPostSolve`（IKSolver.更新委托 OnPostSolve）(偏移: 0x64)
- `IKSolver.UpdateDelegate OnStoreDefaultLocalState`（IKSolver.更新委托 On商店默认的本地的状态）(偏移: 0x68)
- `IKSolver.UpdateDelegate OnFixTransforms`（IKSolver.更新委托 OnFixTransforms）(偏移: 0x6C)

### 方法 (16)

- `IKEffector GetEffector(Transform t)`
  （IKEffector 获取Effector（变换 t））
- `FBIKChain GetChain(Transform transform)`
  （FBIKChain 获取Chain（变换 transform））
- `int GetChainIndex(Transform transform)`
  （int 获取Chain索引（变换 transform））
- `IKSolver.Node GetNode(int chainIndex, int nodeIndex)`
  （IKSolver.节点 获取节点（int chainIndex, int nodeIndex））
- `void GetChainAndNodeIndexes(Transform transform, out int chainIndex, out int nodeIndex)`
  （void 获取ChainAnd节点Indexes（变换 transform, out int chainIndex, out int nodeIndex））
- `IKSolver.Point[] GetPoints()`
  （IKSolver.Point[] 获取Points（））
- `IKSolver.Point GetPoint(Transform transform)`
  （IKSolver.Point 获取Point（变换 transform））
- `bool IsValid(ref string message)`
  （bool 是否Valid（ref string message））
- `void StoreDefaultLocalState()`
  （void 商店默认的本地的状态（））
- `void FixTransforms()`
  （void FixTransforms（））
- `void OnInitiate()`
  （void OnInitiate（））
- `void OnUpdate()`
  （void On更新（））
- `void ReadPose()`
  （void ReadPose（））
- `void Solve()`
  （void Solve（））
- `void ApplyBendConstraints()`
  （void 应用BendConstraints（））
- `void WritePose()`
  （void WritePose（））

---

## IKSolverFullBodyBiped（IKSolver满身体Biped）

**继承**: IKSolverFullBody（IKSolver满身体）

### 字段 (5)

- `Transform rootNode`（变换 root节点）(偏移: 0x70)
- `float spineStiffness`（float spineStiffness）(偏移: 0x74)
- `float pullBodyVertical`（float pull身体垂直）(偏移: 0x78)
- `float pullBodyHorizontal`（float pull身体水平）(偏移: 0x7C)
- `Vector3 offset`（三维向量 offset）(偏移: 0x8C)

### 方法 (45)

- `IKEffector get_bodyEffector()`
  （IKEffector get_bodyEffector（））
- `IKEffector get_leftShoulderEffector()`
  （IKEffector get_leftShoulderEffector（））
- `IKEffector get_rightShoulderEffector()`
  （IKEffector get_rightShoulderEffector（））
- `IKEffector get_leftThighEffector()`
  （IKEffector get_leftThighEffector（））
- `IKEffector get_rightThighEffector()`
  （IKEffector get_rightThighEffector（））
- `IKEffector get_leftHandEffector()`
  （IKEffector get_left手部Effector（））
- `IKEffector get_rightHandEffector()`
  （IKEffector get_right手部Effector（））
- `IKEffector get_leftFootEffector()`
  （IKEffector get_left脚部Effector（））
- `IKEffector get_rightFootEffector()`
  （IKEffector get_right脚部Effector（））
- `FBIKChain get_leftArmChain()`
  （FBIKChain get_left手臂Chain（））
- `FBIKChain get_rightArmChain()`
  （FBIKChain get_right手臂Chain（））
- `FBIKChain get_leftLegChain()`
  （FBIKChain get_left腿部Chain（））
- `FBIKChain get_rightLegChain()`
  （FBIKChain get_right腿部Chain（））
- `IKMappingLimb get_leftArmMapping()`
  （IKMappingLimb get_left手臂Mapping（））
- `IKMappingLimb get_rightArmMapping()`
  （IKMappingLimb get_right手臂Mapping（））
- `IKMappingLimb get_leftLegMapping()`
  （IKMappingLimb get_left腿部Mapping（））
- `IKMappingLimb get_rightLegMapping()`
  （IKMappingLimb get_right腿部Mapping（））
- `IKMappingBone get_headMapping()`
  （IKMappingBone get_headMapping（））
- `void SetChainWeights(FullBodyBipedChain c, float pull, float reach = 0)`
  （void 集合ChainWeights（满身体BipedChain c, float pull, float reach = 0））
- `void SetEffectorWeights(FullBodyBipedEffector effector, float positionWeight, float rotationWeight)`
  （void 集合EffectorWeights（满身体BipedEffector effector, float positionWeight, float rotationWeight））
- `FBIKChain GetChain(FullBodyBipedChain c)`
  （FBIKChain 获取Chain（满身体BipedChain c））
- `FBIKChain GetChain(FullBodyBipedEffector effector)`
  （FBIKChain 获取Chain（满身体BipedEffector effector））
- `IKEffector GetEffector(FullBodyBipedEffector effector)`
  （IKEffector 获取Effector（满身体BipedEffector effector））
- `IKEffector GetEndEffector(FullBodyBipedChain c)`
  （IKEffector 获取结束Effector（满身体BipedChain c））
- `IKMappingLimb GetLimbMapping(FullBodyBipedChain chain)`
  （IKMappingLimb 获取LimbMapping（满身体BipedChain chain））
- `IKMappingLimb GetLimbMapping(FullBodyBipedEffector effector)`
  （IKMappingLimb 获取LimbMapping（满身体BipedEffector effector））
- `IKMappingSpine GetSpineMapping()`
  （IKMappingSpine 获取SpineMapping（））
- `IKMappingBone GetHeadMapping()`
  （IKMappingBone 获取头部Mapping（））
- `IKConstraintBend GetBendConstraint(FullBodyBipedChain limb)`
  （IKConstraintBend 获取BendConstraint（满身体BipedChain limb））
- `bool IsValid(ref string message)`
  （bool 是否Valid（ref string message））
- `void SetToReferences(BipedReferences references, Transform rootNode)`
  （void 集合ToReferences（BipedReferences references, 变换 rootNode））
- `Transform DetectRootNodeBone(BipedReferences references)`
  （变换 Detect根节点Bone（BipedReferences references））
- `void SetLimbOrientations(BipedLimbOrientations o)`
  （void 集合LimbOrientations（BipedLimbOrientations o））
- `Vector3 get_pullBodyOffset()`
  （三维向量 get_pull身体Offset（））
- `void set_pullBodyOffset(Vector3 value)`
  （void set_pull身体Offset（三维向量 value））
- `void SetLimbOrientation(FullBodyBipedChain chain, BipedLimbOrientations.LimbOrientation limbOrientation)`
  （void 集合LimbOrientation（满身体BipedChain chain, BipedLimbOrientations.LimbOrientation limbOrientation））
- `Transform GetLeftClavicle(BipedReferences references)`
  （变换 获取左Clavicle（BipedReferences references））
- `Transform GetRightClavicle(BipedReferences references)`
  （变换 获取右Clavicle（BipedReferences references））
- `bool Contains(Transform[] array, Transform transform)`
  （bool Contains（Transform[] array, 变换 transform））
- `void ReadPose()`
  （void ReadPose（））
- `void PullBody()`
  （void Pull身体（））
- `Vector3 GetBodyOffset()`
  （三维向量 获取身体Offset（））
- `Vector3 GetHandBodyPull(IKEffector effector, FBIKChain arm, Vector3 offset)`
  （三维向量 获取手部身体Pull（IKEffector effector, FBIKChain arm, 三维向量 offset））
- `void ApplyBendConstraints()`
  （void 应用BendConstraints（））
- `void WritePose()`
  （void WritePose（））

---

## IKSolverHeuristic（IKSolverHeuristic）

**继承**: IKSolver（IKSolver）

### 字段 (8)

- `Transform target`（变换 target）(偏移: 0x34)
- `float tolerance`（float tolerance）(偏移: 0x38)
- `int maxIterations`（int maxIterations）(偏移: 0x3C)
- `bool useRotationLimits`（bool useRotationLimits）(偏移: 0x40)
- `bool XY`（bool XY）(偏移: 0x41)
- `IKSolver.Bone[] bones`（IKSolver.Bone[] bones）(偏移: 0x44)
- `Vector3 lastLocalDirection`（三维向量 last本地的方向）(偏移: 0x48)
- `float chainLength`（float chainLength）(偏移: 0x54)

### 方法 (17)

- `bool SetChain(Transform[] hierarchy, Transform root)`
  （bool 集合Chain（Transform[] hierarchy, 变换 root））
- `void AddBone(Transform bone)`
  （void 添加Bone（变换 bone））
- `void StoreDefaultLocalState()`
  （void 商店默认的本地的状态（））
- `void FixTransforms()`
  （void FixTransforms（））
- `bool IsValid(ref string message)`
  （bool 是否Valid（ref string message））
- `IKSolver.Point[] GetPoints()`
  （IKSolver.Point[] 获取Points（））
- `IKSolver.Point GetPoint(Transform transform)`
  （IKSolver.Point 获取Point（变换 transform））
- `int get_minBones()`
  （int get_minBones（））
- `bool get_boneLengthCanBeZero()`
  （bool get_boneLength能否BeZero（））
- `bool get_allowCommonParent()`
  （bool get_allowCommon父级（））
- `void OnInitiate()`
  （void OnInitiate（））
- `void OnUpdate()`
  （void On更新（））
- `void InitiateBones()`
  （void InitiateBones（））
- `Vector3 get_localDirection()`
  （三维向量 get_local方向（））
- `float get_positionOffset()`
  （float get_positionOffset（））
- `Vector3 GetSingularityOffset()`
  （三维向量 获取SingularityOffset（））
- `bool SingularityDetected()`
  （bool SingularityDetected（））

---

## IKSolverLeg（IKSolver腿部）

**继承**: IKSolver（IKSolver）

### 字段 (11)

- `float IKRotationWeight`（float IKRotationWeight）(偏移: 0x34)
- `Quaternion IKRotation`（Quaternion IKRotation）(偏移: 0x38)
- `IKSolver.Point pelvis`（IKSolver.Point pelvis）(偏移: 0x48)
- `IKSolver.Point thigh`（IKSolver.Point thigh）(偏移: 0x4C)
- `IKSolver.Point calf`（IKSolver.Point calf）(偏移: 0x50)
- `IKSolver.Point foot`（IKSolver.Point foot）(偏移: 0x54)
- `IKSolver.Point toe`（IKSolver.Point toe）(偏移: 0x58)
- `IKSolverVR.Leg leg`（IKSolverVR.腿部 leg）(偏移: 0x5C)
- `Vector3 heelOffset`（三维向量 heelOffset）(偏移: 0x60)
- `Vector3[] positions`（Vector3[] positions）(偏移: 0x6C)
- `Quaternion[] rotations`（Quaternion[] rotations）(偏移: 0x70)

### 方法 (11)

- `bool IsValid(ref string message)`
  （bool 是否Valid（ref string message））
- `bool SetChain(Transform pelvis, Transform thigh, Transform calf, Transform foot, Transform toe, Transform root)`
  （bool 集合Chain（变换 pelvis, 变换 thigh, 变换 calf, 变换 foot, 变换 toe, 变换 root））
- `IKSolver.Point[] GetPoints()`
  （IKSolver.Point[] 获取Points（））
- `IKSolver.Point GetPoint(Transform transform)`
  （IKSolver.Point 获取Point（变换 transform））
- `void StoreDefaultLocalState()`
  （void 商店默认的本地的状态（））
- `void FixTransforms()`
  （void FixTransforms（））
- `void OnInitiate()`
  （void OnInitiate（））
- `void OnUpdate()`
  （void On更新（））
- `void Solve()`
  （void Solve（））
- `void Read()`
  （void Read（））
- `void Write()`
  （void Write（））

---

## IKSolverLimb（IKSolverLimb）

**继承**: IKSolverTrigonometric（IKSolverTrigonometric）

### 字段 (16)

- `AvatarIKGoal goal`（AvatarIKGoal goal）(偏移: 0x74)
- `IKSolverLimb.BendModifier bendModifier`（IKSolverLimb.Bend修改器 bend修改器）(偏移: 0x78)
- `float maintainRotationWeight`（float maintainRotationWeight）(偏移: 0x7C)
- `float bendModifierWeight`（float bend修改器Weight）(偏移: 0x80)
- `Transform bendGoal`（变换 bendGoal）(偏移: 0x84)
- `bool maintainBendFor1Frame`（bool maintainBendFor1Frame）(偏移: 0x88)
- `bool maintainRotationFor1Frame`（bool maintainRotationFor1Frame）(偏移: 0x89)
- `Quaternion defaultRootRotation`（Quaternion default根Rotation）(偏移: 0x8C)
- `Quaternion parentDefaultRotation`（Quaternion parent默认的Rotation）(偏移: 0x9C)
- `Quaternion bone3RotationBeforeSolve`（Quaternion bone3RotationBeforeSolve）(偏移: 0xAC)
- `Quaternion maintainRotation`（Quaternion maintainRotation）(偏移: 0xBC)
- `Quaternion bone3DefaultRotation`（Quaternion bone3默认的Rotation）(偏移: 0xCC)
- `Vector3 _bendNormal`（三维向量 _bend法线）(偏移: 0xDC)
- `Vector3 animationNormal`（三维向量 animation法线）(偏移: 0xE8)
- `IKSolverLimb.AxisDirection[] axisDirectionsLeft`（IKSolverLimb.轴Direction[] axisDirections左）(偏移: 0xF4)
- `IKSolverLimb.AxisDirection[] axisDirectionsRight`（IKSolverLimb.轴Direction[] axisDirections右）(偏移: 0xF8)

### 方法 (8)

- `void MaintainRotation()`
  （void MaintainRotation（））
- `void MaintainBend()`
  （void MaintainBend（））
- `void OnInitiateVirtual()`
  （void OnInitiate虚拟的（））
- `void OnUpdateVirtual()`
  （void On更新虚拟的（））
- `void OnPostSolveVirtual()`
  （void OnPostSolve虚拟的（））
- `IKSolverLimb.AxisDirection[] get_axisDirections()`
  （IKSolverLimb.轴Direction[] get_axisDirections（））
- `void StoreAxisDirections(ref IKSolverLimb.AxisDirection[] axisDirections)`
  （void 商店轴Directions（ref IKSolverLimb.AxisDirection[] axisDirections））
- `Vector3 GetModifiedBendNormal()`
  （三维向量 获取ModifiedBend法线（））

---

## IKSolverLimb.AxisDirection（IKSolverLimb.轴方向）

### 字段 (3)

- `Vector3 direction`（三维向量 direction）(偏移: 0x0)
- `Vector3 axis`（三维向量 axis）(偏移: 0xC)
- `float dot`（float dot）(偏移: 0x18)

---

## IKSolverLimb.BendModifier（IKSolverLimb.Bend修改器）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## IKSolverLookAt（IKSolverLookAt）

**继承**: IKSolver（IKSolver）

### 字段 (16)

- `Transform target`（变换 target）(偏移: 0x34)
- `IKSolverLookAt.LookAtBone[] spine`（IKSolverLookAt.LookAtBone[] spine）(偏移: 0x38)
- `IKSolverLookAt.LookAtBone head`（IKSolverLookAt.LookAtBone head）(偏移: 0x3C)
- `IKSolverLookAt.LookAtBone[] eyes`（IKSolverLookAt.LookAtBone[] eyes）(偏移: 0x40)
- `float bodyWeight`（float bodyWeight）(偏移: 0x44)
- `float headWeight`（float headWeight）(偏移: 0x48)
- `float eyesWeight`（float eyesWeight）(偏移: 0x4C)
- `float clampWeight`（float clampWeight）(偏移: 0x50)
- `float clampWeightHead`（float clampWeight头部）(偏移: 0x54)
- `float clampWeightEyes`（float clampWeightEyes）(偏移: 0x58)
- `int clampSmoothing`（int clampSmoothing）(偏移: 0x5C)
- `AnimationCurve spineWeightCurve`（动画Curve spineWeightCurve）(偏移: 0x60)
- `Vector3 spineTargetOffset`（三维向量 spine目标Offset）(偏移: 0x64)
- `Vector3[] spineForwards`（Vector3[] spineForwards）(偏移: 0x70)
- `Vector3[] headForwards`（Vector3[] headForwards）(偏移: 0x74)
- `Vector3[] eyeForward`（Vector3[] eye前进）(偏移: 0x78)

### 方法 (25)

- `void SetLookAtWeight(float weight)`
  （void 集合LookAtWeight（float weight））
- `void SetLookAtWeight(float weight, float bodyWeight)`
  （void 集合LookAtWeight（float weight, float bodyWeight））
- `void SetLookAtWeight(float weight, float bodyWeight, float headWeight)`
  （void 集合LookAtWeight（float weight, float bodyWeight, float headWeight））
- `void SetLookAtWeight(float weight, float bodyWeight, float headWeight, float eyesWeight)`
  （void 集合LookAtWeight（float weight, float bodyWeight, float headWeight, float eyesWeight））
- `void SetLookAtWeight(float weight, float bodyWeight, float headWeight, float eyesWeight, float clampWeight)`
  （void 集合LookAtWeight（float weight, float bodyWeight, float headWeight, float eyesWeight, float clampWeight））
- `void SetLookAtWeight(float weight, float bodyWeight = 0, float headWeight = 1, float eyesWeight = 0.5, float clampWeight = 0.5, float clampWeightHead = 0.5, float clampWeightEyes = 0.3)`
  （void 集合LookAtWeight（float weight, float bodyWeight = 0, float headWeight = 1, float eyesWeight = 0.5, float clampWeight = 0.5, float clampWeightHead = 0.5, float clampWeightEyes = 0.3））
- `void StoreDefaultLocalState()`
  （void 商店默认的本地的状态（））
- `void FixTransforms()`
  （void FixTransforms（））
- `bool IsValid(ref string message)`
  （bool 是否Valid（ref string message））
- `IKSolver.Point[] GetPoints()`
  （IKSolver.Point[] 获取Points（））
- `IKSolver.Point GetPoint(Transform transform)`
  （IKSolver.Point 获取Point（变换 transform））
- `bool SetChain(Transform[] spine, Transform head, Transform[] eyes, Transform root)`
  （bool 集合Chain（Transform[] spine, 变换 head, Transform[] eyes, 变换 root））
- `void OnInitiate()`
  （void OnInitiate（））
- `void OnUpdate()`
  （void On更新（））
- `bool get_spineIsValid()`
  （bool get_spine是否Valid（））
- `bool get_spineIsEmpty()`
  （bool get_spine是否空（））
- `void SolveSpine()`
  （void SolveSpine（））
- `bool get_headIsValid()`
  （bool get_head是否Valid（））
- `bool get_headIsEmpty()`
  （bool get_head是否空（））
- `void SolveHead()`
  （void Solve头部（））
- `bool get_eyesIsValid()`
  （bool get_eyes是否Valid（））
- `bool get_eyesIsEmpty()`
  （bool get_eyes是否空（））
- `void SolveEyes()`
  （void SolveEyes（））
- `Vector3[] GetForwards(ref Vector3[] forwards, Vector3 baseForward, Vector3 targetForward, int bones, float clamp)`
  （Vector3[] 获取Forwards（ref Vector3[] forwards, 三维向量 baseForward, 三维向量 targetForward, int bones, float clamp））
- `void SetBones(Transform[] array, ref IKSolverLookAt.LookAtBone[] bones)`
  （void 集合Bones（Transform[] array, ref IKSolverLookAt.LookAtBone[] bones））

---

## IKSolverLookAt.LookAtBone（IKSolverLookAt.LookAtBone）

**继承**: IKSolver.Bone（IKSolver.Bone）

### 字段 (1)

- `Vector3 baseForwardOffsetEuler`（三维向量 base前进OffsetEuler）(偏移: 0x64)

### 方法 (3)

- `void Initiate(Transform root)`
  （void Initiate（变换 root））
- `void LookAt(Vector3 direction, float weight)`
  （void LookAt（三维向量 direction, float weight））
- `Vector3 get_forward()`
  （三维向量 get_forward（））

---

## IKSolverTrigonometric（IKSolverTrigonometric）

**继承**: IKSolver（IKSolver）

### 字段 (9)

- `Transform target`（变换 target）(偏移: 0x34)
- `float IKRotationWeight`（float IKRotationWeight）(偏移: 0x38)
- `Quaternion IKRotation`（Quaternion IKRotation）(偏移: 0x3C)
- `Vector3 bendNormal`（三维向量 bend法线）(偏移: 0x4C)
- `IKSolverTrigonometric.TrigonometricBone bone1`（IKSolverTrigonometric.TrigonometricBone bone1）(偏移: 0x58)
- `IKSolverTrigonometric.TrigonometricBone bone2`（IKSolverTrigonometric.TrigonometricBone bone2）(偏移: 0x5C)
- `IKSolverTrigonometric.TrigonometricBone bone3`（IKSolverTrigonometric.TrigonometricBone bone3）(偏移: 0x60)
- `Vector3 weightIKPosition`（三维向量 weightIKPosition）(偏移: 0x64)
- `bool directHierarchy`（bool directHierarchy）(偏移: 0x70)

### 方法 (22)

- `void SetBendGoalPosition(Vector3 goalPosition, float weight)`
  （void 集合BendGoalPosition（三维向量 goalPosition, float weight））
- `void SetBendPlaneToCurrent()`
  （void 集合BendPlaneTo当前（））
- `void SetIKRotation(Quaternion rotation)`
  （void 集合IKRotation（Quaternion rotation））
- `void SetIKRotationWeight(float weight)`
  （void 集合IKRotationWeight（float weight））
- `Quaternion GetIKRotation()`
  （Quaternion 获取IKRotation（））
- `float GetIKRotationWeight()`
  （float 获取IKRotationWeight（））
- `IKSolver.Point[] GetPoints()`
  （IKSolver.Point[] 获取Points（））
- `IKSolver.Point GetPoint(Transform transform)`
  （IKSolver.Point 获取Point（变换 transform））
- `void StoreDefaultLocalState()`
  （void 商店默认的本地的状态（））
- `void FixTransforms()`
  （void FixTransforms（））
- `bool IsValid(ref string message)`
  （bool 是否Valid（ref string message））
- `bool SetChain(Transform bone1, Transform bone2, Transform bone3, Transform root)`
  （bool 集合Chain（变换 bone1, 变换 bone2, 变换 bone3, 变换 root））
- `void Solve(Transform bone1, Transform bone2, Transform bone3, Vector3 targetPosition, Vector3 bendNormal, float weight)`
  （void Solve（变换 bone1, 变换 bone2, 变换 bone3, 三维向量 targetPosition, 三维向量 bendNormal, float weight））
- `Vector3 GetDirectionToBendPoint(Vector3 direction, float directionMag, Vector3 bendDirection, float sqrMag1, float sqrMag2)`
  （三维向量 获取方向ToBendPoint（三维向量 direction, float directionMag, 三维向量 bendDirection, float sqrMag1, float sqrMag2））
- `void OnInitiate()`
  （void OnInitiate（））
- `bool IsDirectHierarchy()`
  （bool 是否DirectHierarchy（））
- `void InitiateBones()`
  （void InitiateBones（））
- `void OnUpdate()`
  （void On更新（））
- `void OnInitiateVirtual()`
  （void OnInitiate虚拟的（））
- `void OnUpdateVirtual()`
  （void On更新虚拟的（））
- `void OnPostSolveVirtual()`
  （void OnPostSolve虚拟的（））
- `Vector3 GetBendDirection(Vector3 IKPosition, Vector3 bendNormal)`
  （三维向量 获取Bend方向（三维向量 IKPosition, 三维向量 bendNormal））

---

## IKSolverTrigonometric.TrigonometricBone（IKSolverTrigonometric.TrigonometricBone）

**继承**: IKSolver.Bone（IKSolver.Bone）

### 字段 (2)

- `Quaternion targetToLocalSpace`（Quaternion targetTo本地的Space）(偏移: 0x64)
- `Vector3 defaultLocalBendNormal`（三维向量 default本地的Bend法线）(偏移: 0x74)

### 方法 (3)

- `void Initiate(Vector3 childPosition, Vector3 bendNormal)`
  （void Initiate（三维向量 childPosition, 三维向量 bendNormal））
- `Quaternion GetRotation(Vector3 direction, Vector3 bendNormal)`
  （Quaternion 获取Rotation（三维向量 direction, 三维向量 bendNormal））
- `Vector3 GetBendNormalFromCurrentRotation()`
  （三维向量 获取Bend法线From当前Rotation（））

---

## IKSolverVR（IKSolverVR）

**继承**: IKSolver（IKSolver）

### 字段 (35)

- `Transform[] solverTransforms`（Transform[] solverTransforms）(偏移: 0x34)
- `bool hasChest`（bool has胸部）(偏移: 0x38)
- `bool hasNeck`（bool has颈部）(偏移: 0x0)
- `bool hasShoulders`（bool hasShoulders）(偏移: 0x0)
- `bool hasToes`（bool hasToes）(偏移: 0x0)
- `bool hasLegs`（bool hasLegs）(偏移: 0x0)
- `Vector3[] readPositions`（Vector3[] readPositions）(偏移: 0x40)
- `Quaternion[] readRotations`（Quaternion[] readRotations）(偏移: 0x44)
- `Vector3[] solvedPositions`（Vector3[] solvedPositions）(偏移: 0x48)
- `Quaternion[] solvedRotations`（Quaternion[] solvedRotations）(偏移: 0x4C)
- `Quaternion[] defaultLocalRotations`（Quaternion[] default本地的Rotations）(偏移: 0x50)
- `Vector3[] defaultLocalPositions`（Vector3[] default本地的Positions）(偏移: 0x54)
- `Vector3 rootV`（三维向量 rootV）(偏移: 0x58)
- `Vector3 rootVelocity`（三维向量 root速度）(偏移: 0x64)
- `Vector3 bodyOffset`（三维向量 bodyOffset）(偏移: 0x70)
- `int supportLegIndex`（int support腿部索引）(偏移: 0x7C)
- `int lastLOD`（int lastLOD）(偏移: 0x80)
- `int LOD`（int LOD）(偏移: 0x84)
- `bool plantFeet`（bool plantFeet）(偏移: 0x88)
- `IKSolverVR.Spine spine`（IKSolverVR.Spine spine）(偏移: 0x90)
- `IKSolverVR.Arm leftArm`（IKSolverVR.手臂 left手臂）(偏移: 0x94)
- `IKSolverVR.Arm rightArm`（IKSolverVR.手臂 right手臂）(偏移: 0x98)
- `IKSolverVR.Leg leftLeg`（IKSolverVR.腿部 left腿部）(偏移: 0x9C)
- `IKSolverVR.Leg rightLeg`（IKSolverVR.腿部 right腿部）(偏移: 0xA0)
- `IKSolverVR.Locomotion locomotion`（IKSolverVR.Locomotion locomotion）(偏移: 0xA4)
- `IKSolverVR.Leg[] legs`（IKSolverVR.Leg[] legs）(偏移: 0xA8)
- `IKSolverVR.Arm[] arms`（IKSolverVR.Arm[] arms）(偏移: 0xAC)
- `Vector3 headPosition`（三维向量 headPosition）(偏移: 0xB0)
- `Vector3 headDeltaPosition`（三维向量 headDeltaPosition）(偏移: 0xBC)
- `Vector3 raycastOriginPelvis`（三维向量 raycastOriginPelvis）(偏移: 0xC8)
- `Vector3 lastOffset`（三维向量 lastOffset）(偏移: 0xD4)
- `Vector3 debugPos1`（三维向量 debugPos1）(偏移: 0xE0)
- `Vector3 debugPos2`（三维向量 debugPos2）(偏移: 0xEC)
- `Vector3 debugPos3`（三维向量 debugPos3）(偏移: 0xF8)
- `Vector3 debugPos4`（三维向量 debugPos4）(偏移: 0x104)

### 方法 (29)

- `void SetToReferences(VRIK.References references)`
  （void 集合ToReferences（VRIK.References references））
- `void GuessHandOrientations(VRIK.References references, bool onlyIfZero)`
  （void Guess手部Orientations（VRIK.References references, bool onlyIfZero））
- `void DefaultAnimationCurves()`
  （void 默认的动画Curves（））
- `void AddPositionOffset(IKSolverVR.PositionOffset positionOffset, Vector3 value)`
  （void 添加PositionOffset（IKSolverVR.PositionOffset positionOffset, 三维向量 value））
- `void AddRotationOffset(IKSolverVR.RotationOffset rotationOffset, Vector3 value)`
  （void 添加RotationOffset（IKSolverVR.RotationOffset rotationOffset, 三维向量 value））
- `void AddRotationOffset(IKSolverVR.RotationOffset rotationOffset, Quaternion value)`
  （void 添加RotationOffset（IKSolverVR.RotationOffset rotationOffset, Quaternion value））
- `void AddPlatformMotion(Vector3 deltaPosition, Quaternion deltaRotation, Vector3 platformPivot)`
  （void 添加PlatformMotion（三维向量 deltaPosition, Quaternion deltaRotation, 三维向量 platformPivot））
- `void Reset()`
  （void 重置（））
- `void StoreDefaultLocalState()`
  （void 商店默认的本地的状态（））
- `void FixTransforms()`
  （void FixTransforms（））
- `IKSolver.Point[] GetPoints()`
  （IKSolver.Point[] 获取Points（））
- `IKSolver.Point GetPoint(Transform transform)`
  （IKSolver.Point 获取Point（变换 transform））
- `bool IsValid(ref string message)`
  （bool 是否Valid（ref string message））
- `Vector3 GetNormal(Transform[] transforms)`
  （三维向量 获取法线（Transform[] transforms））
- `Vector3 GuessWristToPalmAxis(Transform hand, Transform forearm)`
  （三维向量 GuessWristToPalm轴（变换 hand, 变换 forearm））
- `Vector3 GuessPalmToThumbAxis(Transform hand, Transform forearm)`
  （三维向量 GuessPalmToThumb轴（变换 hand, 变换 forearm））
- `Keyframe[] GetSineKeyframes(float mag)`
  （Keyframe[] 获取SineKeyframes（float mag））
- `void UpdateSolverTransforms()`
  （void 更新SolverTransforms（））
- `void OnInitiate()`
  （void OnInitiate（））
- `void OnUpdate()`
  （void On更新（））
- `void WriteTransforms()`
  （void WriteTransforms（））
- `void Read(Vector3[] positions, Quaternion[] rotations, bool hasChest, bool hasNeck, bool hasShoulders, bool hasToes, bool hasLegs)`
  （void Read（Vector3[] positions, Quaternion[] rotations, bool hasChest, bool hasNeck, bool hasShoulders, bool hasToes, bool hasLegs））
- `void Solve()`
  （void Solve（））
- `Vector3 GetPosition(int index)`
  （三维向量 获取Position（int index））
- `Quaternion GetRotation(int index)`
  （Quaternion 获取Rotation（int index））
- `IKSolverVR.VirtualBone get_rootBone()`
  （IKSolverVR.虚拟的Bone get_rootBone（））
- `void set_rootBone(IKSolverVR.VirtualBone value)`
  （void set_rootBone（IKSolverVR.虚拟的Bone value））
- `void Write()`
  （void Write（））
- `Vector3 GetPelvisOffset()`
  （三维向量 获取PelvisOffset（））

---

## IKSolverVR.Arm（IKSolverVR.手臂）

**继承**: IKSolverVR.BodyPart（IKSolverVR.身体Part）

### 字段 (25)

- `Transform target`（变换 target）(偏移: 0x3C)
- `Transform bendGoal`（变换 bendGoal）(偏移: 0x40)
- `float positionWeight`（float positionWeight）(偏移: 0x44)
- `float rotationWeight`（float rotationWeight）(偏移: 0x48)
- `IKSolverVR.Arm.ShoulderRotationMode shoulderRotationMode`（IKSolverVR.Arm.ShoulderRotation模式 shoulderRotation模式）(偏移: 0x4C)
- `float shoulderRotationWeight`（float shoulderRotationWeight）(偏移: 0x50)
- `float shoulderTwistWeight`（float shoulderTwistWeight）(偏移: 0x54)
- `float bendGoalWeight`（float bendGoalWeight）(偏移: 0x58)
- `float swivelOffset`（float swivelOffset）(偏移: 0x5C)
- `Vector3 wristToPalmAxis`（三维向量 wristToPalm轴）(偏移: 0x60)
- `Vector3 palmToThumbAxis`（三维向量 palmToThumb轴）(偏移: 0x6C)
- `float armLengthMlp`（float armLengthMlp）(偏移: 0x78)
- `AnimationCurve stretchCurve`（动画Curve stretchCurve）(偏移: 0x7C)
- `Vector3 IKPosition`（三维向量 IKPosition）(偏移: 0x80)
- `Quaternion IKRotation`（Quaternion IKRotation）(偏移: 0x8C)
- `Vector3 bendDirection`（三维向量 bend方向）(偏移: 0x9C)
- `Vector3 handPositionOffset`（三维向量 handPositionOffset）(偏移: 0xA8)
- `bool hasShoulder`（bool hasShoulder）(偏移: 0xD0)
- `Vector3 chestForwardAxis`（三维向量 chest前进轴）(偏移: 0xD4)
- `Vector3 chestUpAxis`（三维向量 chest上轴）(偏移: 0xE0)
- `Quaternion chestRotation`（Quaternion chestRotation）(偏移: 0xEC)
- `Vector3 chestForward`（三维向量 chest前进）(偏移: 0xFC)
- `Vector3 chestUp`（三维向量 chest上）(偏移: 0x108)
- `Quaternion forearmRelToUpperArm`（Quaternion forearmRelTo上半身手臂）(偏移: 0x114)
- `Vector3 upperArmBendAxis`（三维向量 upper手臂Bend轴）(偏移: 0x124)

### 方法 (18)

- `Vector3 get_position()`
  （三维向量 get_position（））
- `void set_position(Vector3 value)`
  （void set_position（三维向量 value））
- `Quaternion get_rotation()`
  （Quaternion get_rotation（））
- `void set_rotation(Quaternion value)`
  （void set_rotation（Quaternion value））
- `IKSolverVR.VirtualBone get_shoulder()`
  （IKSolverVR.虚拟的Bone get_shoulder（））
- `IKSolverVR.VirtualBone get_upperArm()`
  （IKSolverVR.虚拟的Bone get_upper手臂（））
- `IKSolverVR.VirtualBone get_forearm()`
  （IKSolverVR.虚拟的Bone get_forearm（））
- `IKSolverVR.VirtualBone get_hand()`
  （IKSolverVR.虚拟的Bone get_hand（））
- `void OnRead(Vector3[] positions, Quaternion[] rotations, bool hasChest, bool hasNeck, bool hasShoulders, bool hasToes, bool hasLegs, int rootIndex, int index)`
  （void OnRead（Vector3[] positions, Quaternion[] rotations, bool hasChest, bool hasNeck, bool hasShoulders, bool hasToes, bool hasLegs, int rootIndex, int index））
- `void PreSolve()`
  （void PreSolve（））
- `void ApplyOffsets()`
  （void 应用Offsets（））
- `void Stretching()`
  （void Stretching（））
- `void Solve(bool isLeft)`
  （void Solve（bool isLeft））
- `void ResetOffsets()`
  （void 重置Offsets（））
- `void Write(ref Vector3[] solvedPositions, ref Quaternion[] solvedRotations)`
  （void Write（ref Vector3[] solvedPositions, ref Quaternion[] solvedRotations））
- `float DamperValue(float value, float min, float max, float weight = 1)`
  （float Damper值（float value, float min, float max, float weight = 1））
- `Vector3 GetBendNormal(Vector3 dir)`
  （三维向量 获取Bend法线（三维向量 dir））
- `void Visualize(IKSolverVR.VirtualBone bone1, IKSolverVR.VirtualBone bone2, IKSolverVR.VirtualBone bone3, Color color)`
  （void Visualize（IKSolverVR.虚拟的Bone bone1, IKSolverVR.虚拟的Bone bone2, IKSolverVR.虚拟的Bone bone3, 颜色 color））

---

## IKSolverVR.Arm.ShoulderRotationMode（IKSolverVR.Arm.ShoulderRotation模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## IKSolverVR.BodyPart（IKSolverVR.身体Part）

### 字段 (6)

- `IKSolverVR.VirtualBone[] bones`（IKSolverVR.虚拟的Bone[] bones）(偏移: 0x10)
- `bool initiated`（bool initiated）(偏移: 0x14)
- `Vector3 rootPosition`（三维向量 rootPosition）(偏移: 0x18)
- `Quaternion rootRotation`（Quaternion rootRotation）(偏移: 0x24)
- `int index`（int index）(偏移: 0x34)
- `int LOD`（int LOD）(偏移: 0x38)

### 方法 (13)

- `float get_sqrMag()`
  （float get_sqrMag（））
- `void set_sqrMag(float value)`
  （void set_sqrMag（float value））
- `float get_mag()`
  （float get_mag（））
- `void set_mag(float value)`
  （void set_mag（float value））
- `void SetLOD(int LOD)`
  （void 集合LOD（int LOD））
- `void Read(Vector3[] positions, Quaternion[] rotations, bool hasChest, bool hasNeck, bool hasShoulders, bool hasToes, bool hasLegs, int rootIndex, int index)`
  （void Read（Vector3[] positions, Quaternion[] rotations, bool hasChest, bool hasNeck, bool hasShoulders, bool hasToes, bool hasLegs, int rootIndex, int index））
- `void MovePosition(Vector3 position)`
  （void 移动Position（三维向量 position））
- `void MoveRotation(Quaternion rotation)`
  （void 移动Rotation（Quaternion rotation））
- `void Translate(Vector3 position, Quaternion rotation)`
  （void Translate（三维向量 position, Quaternion rotation））
- `void TranslateRoot(Vector3 newRootPos, Quaternion newRootRot)`
  （void Translate根（三维向量 newRootPos, Quaternion newRootRot））
- `void RotateTo(IKSolverVR.VirtualBone bone, Quaternion rotation, float weight = 1)`
  （void RotateTo（IKSolverVR.虚拟的Bone bone, Quaternion rotation, float weight = 1））
- `void Visualize(Color color)`
  （void Visualize（颜色 color））
- `void Visualize()`
  （void Visualize（））

---

## IKSolverVR.Footstep（IKSolverVR.Footstep）

### 字段 (13)

- `float stepSpeed`（float stepSpeed）(偏移: 0x8)
- `Vector3 characterSpaceOffset`（三维向量 characterSpaceOffset）(偏移: 0xC)
- `Vector3 position`（三维向量 position）(偏移: 0x18)
- `Quaternion rotation`（Quaternion rotation）(偏移: 0x24)
- `Quaternion stepToRootRot`（Quaternion stepTo根Rot）(偏移: 0x34)
- `bool isSupportLeg`（bool isSupport腿部）(偏移: 0x44)
- `Vector3 stepFrom`（三维向量 stepFrom）(偏移: 0x4C)
- `Vector3 stepTo`（三维向量 stepTo）(偏移: 0x58)
- `Quaternion stepFromRot`（Quaternion stepFromRot）(偏移: 0x64)
- `Quaternion stepToRot`（Quaternion stepToRot）(偏移: 0x74)
- `Quaternion footRelativeToRoot`（Quaternion footRelativeTo根）(偏移: 0x84)
- `float supportLegW`（float support腿部W）(偏移: 0x94)
- `float supportLegWV`（float support腿部WV）(偏移: 0x98)

### 方法 (8)

- `bool get_isStepping()`
  （bool get_isStepping（））
- `float get_stepProgress()`
  （float get_stepProgress（））
- `void set_stepProgress(float value)`
  （void set_stepProgress（float value））
- `void Reset(Quaternion rootRotation, Vector3 footPosition, Quaternion footRotation)`
  （void 重置（Quaternion rootRotation, 三维向量 footPosition, Quaternion footRotation））
- `void StepTo(Vector3 p, Quaternion rootRotation, float stepThreshold)`
  （void StepTo（三维向量 p, Quaternion rootRotation, float stepThreshold））
- `void UpdateStepping(Vector3 p, Quaternion rootRotation, float speed)`
  （void 更新Stepping（三维向量 p, Quaternion rootRotation, float speed））
- `void UpdateStanding(Quaternion rootRotation, float minAngle, float speed)`
  （void 更新Standing（Quaternion rootRotation, float minAngle, float speed））
- `void Update(InterpolationMode interpolation, UnityEvent onStep)`
  （void 更新（Interpolation模式 interpolation, Unity引擎事件 onStep））

---

## IKSolverVR.Leg（IKSolverVR.腿部）

**继承**: IKSolverVR.BodyPart（IKSolverVR.身体Part）

### 字段 (23)

- `Transform target`（变换 target）(偏移: 0x3C)
- `Transform bendGoal`（变换 bendGoal）(偏移: 0x40)
- `float positionWeight`（float positionWeight）(偏移: 0x44)
- `float rotationWeight`（float rotationWeight）(偏移: 0x48)
- `float bendGoalWeight`（float bendGoalWeight）(偏移: 0x4C)
- `float swivelOffset`（float swivelOffset）(偏移: 0x50)
- `float bendToTargetWeight`（float bendTo目标Weight）(偏移: 0x54)
- `float legLengthMlp`（float legLengthMlp）(偏移: 0x58)
- `AnimationCurve stretchCurve`（动画Curve stretchCurve）(偏移: 0x5C)
- `Vector3 IKPosition`（三维向量 IKPosition）(偏移: 0x60)
- `Quaternion IKRotation`（Quaternion IKRotation）(偏移: 0x6C)
- `Vector3 footPositionOffset`（三维向量 footPositionOffset）(偏移: 0x7C)
- `Vector3 heelPositionOffset`（三维向量 heelPositionOffset）(偏移: 0x88)
- `Quaternion footRotationOffset`（Quaternion footRotationOffset）(偏移: 0x94)
- `float currentMag`（float currentMag）(偏移: 0xA4)
- `bool useAnimatedBendNormal`（bool useAnimatedBend法线）(偏移: 0xA8)
- `Vector3 footPosition`（三维向量 footPosition）(偏移: 0xD8)
- `Quaternion footRotation`（Quaternion footRotation）(偏移: 0xE4)
- `Vector3 bendNormal`（三维向量 bend法线）(偏移: 0xF4)
- `Quaternion calfRelToThigh`（Quaternion calfRelToThigh）(偏移: 0x100)
- `Quaternion thighRelToFoot`（Quaternion thighRelTo脚部）(偏移: 0x110)
- `Vector3 bendNormalRelToPelvis`（三维向量 bend法线RelToPelvis）(偏移: 0x120)
- `Vector3 bendNormalRelToTarget`（三维向量 bend法线RelTo目标）(偏移: 0x12C)

### 方法 (23)

- `Vector3 get_position()`
  （三维向量 get_position（））
- `void set_position(Vector3 value)`
  （void set_position（三维向量 value））
- `Quaternion get_rotation()`
  （Quaternion get_rotation（））
- `void set_rotation(Quaternion value)`
  （void set_rotation（Quaternion value））
- `bool get_hasToes()`
  （bool get_hasToes（））
- `void set_hasToes(bool value)`
  （void set_hasToes（bool value））
- `IKSolverVR.VirtualBone get_thigh()`
  （IKSolverVR.虚拟的Bone get_thigh（））
- `IKSolverVR.VirtualBone get_calf()`
  （IKSolverVR.虚拟的Bone get_calf（））
- `IKSolverVR.VirtualBone get_foot()`
  （IKSolverVR.虚拟的Bone get_foot（））
- `IKSolverVR.VirtualBone get_toes()`
  （IKSolverVR.虚拟的Bone get_toes（））
- `IKSolverVR.VirtualBone get_lastBone()`
  （IKSolverVR.虚拟的Bone get_lastBone（））
- `Vector3 get_thighRelativeToPelvis()`
  （三维向量 get_thighRelativeToPelvis（））
- `void set_thighRelativeToPelvis(Vector3 value)`
  （void set_thighRelativeToPelvis（三维向量 value））
- `void OnRead(Vector3[] positions, Quaternion[] rotations, bool hasChest, bool hasNeck, bool hasShoulders, bool hasToes, bool hasLegs, int rootIndex, int index)`
  （void OnRead（Vector3[] positions, Quaternion[] rotations, bool hasChest, bool hasNeck, bool hasShoulders, bool hasToes, bool hasLegs, int rootIndex, int index））
- `void PreSolve()`
  （void PreSolve（））
- `void ApplyOffsets()`
  （void 应用Offsets（））
- `void ApplyPositionOffset(Vector3 offset, float weight)`
  （void 应用PositionOffset（三维向量 offset, float weight））
- `void ApplyRotationOffset(Quaternion offset, float weight)`
  （void 应用RotationOffset（Quaternion offset, float weight））
- `void Solve(bool stretch)`
  （void Solve（bool stretch））
- `void FixTwistRotations()`
  （void FixTwistRotations（））
- `void Stretching()`
  （void Stretching（））
- `void Write(ref Vector3[] solvedPositions, ref Quaternion[] solvedRotations)`
  （void Write（ref Vector3[] solvedPositions, ref Quaternion[] solvedRotations））
- `void ResetOffsets()`
  （void 重置Offsets（））

---

## IKSolverVR.Locomotion（IKSolverVR.Locomotion）

### 字段 (27)

- `float weight`（float weight）(偏移: 0x8)
- `float footDistance`（float foot距离）(偏移: 0xC)
- `float stepThreshold`（float stepThreshold）(偏移: 0x10)
- `float angleThreshold`（float angleThreshold）(偏移: 0x14)
- `float comAngleMlp`（float com角度Mlp）(偏移: 0x18)
- `float maxVelocity`（float max速度）(偏移: 0x1C)
- `float velocityFactor`（float velocity系数）(偏移: 0x20)
- `float maxLegStretch`（float max腿部Stretch）(偏移: 0x24)
- `float rootSpeed`（float rootSpeed）(偏移: 0x28)
- `float stepSpeed`（float stepSpeed）(偏移: 0x2C)
- `AnimationCurve stepHeight`（动画Curve step高度）(偏移: 0x30)
- `AnimationCurve heelHeight`（动画Curve heel高度）(偏移: 0x34)
- `float relaxLegTwistMinAngle`（float relax腿部Twist最小角度）(偏移: 0x38)
- `float relaxLegTwistSpeed`（float relax腿部TwistSpeed）(偏移: 0x3C)
- `InterpolationMode stepInterpolation`（Interpolation模式 stepInterpolation）(偏移: 0x40)
- `Vector3 offset`（三维向量 offset）(偏移: 0x44)
- `bool blockingEnabled`（bool blocking启用的）(偏移: 0x50)
- `LayerMask blockingLayers`（层掩码 blockingLayers）(偏移: 0x54)
- `float raycastRadius`（float raycastRadius）(偏移: 0x58)
- `float raycastHeight`（float raycast高度）(偏移: 0x5C)
- `UnityEvent onLeftFootstep`（Unity引擎事件 on左Footstep）(偏移: 0x60)
- `UnityEvent onRightFootstep`（Unity引擎事件 on右Footstep）(偏移: 0x64)
- `IKSolverVR.Footstep[] footsteps`（IKSolverVR.Footstep[] footsteps）(偏移: 0x74)
- `Vector3 lastComPosition`（三维向量 lastComPosition）(偏移: 0x78)
- `Vector3 comVelocity`（三维向量 com速度）(偏移: 0x84)
- `int leftFootIndex`（int left脚部索引）(偏移: 0x90)
- `int rightFootIndex`（int right脚部索引）(偏移: 0x94)

### 方法 (14)

- `Vector3 get_centerOfMass()`
  （三维向量 get_centerOfMass（））
- `void set_centerOfMass(Vector3 value)`
  （void set_centerOfMass（三维向量 value））
- `void Initiate(Vector3[] positions, Quaternion[] rotations, bool hasToes)`
  （void Initiate（Vector3[] positions, Quaternion[] rotations, bool hasToes））
- `void Reset(Vector3[] positions, Quaternion[] rotations)`
  （void 重置（Vector3[] positions, Quaternion[] rotations））
- `void AddDeltaRotation(Quaternion delta, Vector3 pivot)`
  （void 添加DeltaRotation（Quaternion delta, 三维向量 pivot））
- `void AddDeltaPosition(Vector3 delta)`
  （void 添加DeltaPosition（三维向量 delta））
- `void Solve(IKSolverVR.VirtualBone rootBone, IKSolverVR.Spine spine, IKSolverVR.Leg leftLeg, IKSolverVR.Leg rightLeg, IKSolverVR.Arm leftArm, IKSolverVR.Arm rightArm, int supportLegIndex, out Vector3 leftFootPosition, out Vector3 rightFootPosition, out Quaternion leftFootRotation, out Quaternion rightFootRotation, out float leftFootOffset, out float rightFootOffset, out float leftHeelOffset, out float rightHeelOffset)`
  （void Solve（IKSolverVR.虚拟的Bone rootBone, IKSolverVR.Spine spine, IKSolverVR.腿部 leftLeg, IKSolverVR.腿部 rightLeg, IKSolverVR.手臂 leftArm, IKSolverVR.手臂 rightArm, int supportLegIndex, out Vector3 leftFootPosition, out Vector3 rightFootPosition, out Quaternion leftFootRotation, out Quaternion rightFootRotation, out float leftFootOffset, out float rightFootOffset, out float leftHeelOffset, out float rightHeelOffset））
- `Vector3 get_leftFootstepPosition()`
  （三维向量 get_leftFootstepPosition（））
- `Vector3 get_rightFootstepPosition()`
  （三维向量 get_rightFootstepPosition（））
- `Quaternion get_leftFootstepRotation()`
  （Quaternion get_leftFootstepRotation（））
- `Quaternion get_rightFootstepRotation()`
  （Quaternion get_rightFootstepRotation（））
- `bool StepBlocked(Vector3 fromPosition, Vector3 toPosition, Vector3 rootPosition)`
  （bool StepBlocked（三维向量 fromPosition, 三维向量 toPosition, 三维向量 rootPosition））
- `bool CanStep()`
  （bool 能否Step（））
- `bool GetLineSphereCollision(Vector3 lineStart, Vector3 lineEnd, Vector3 sphereCenter, float sphereRadius)`
  （bool 获取LineSphereCollision（三维向量 lineStart, 三维向量 lineEnd, 三维向量 sphereCenter, float sphereRadius））

---

## IKSolverVR.PositionOffset（IKSolverVR.PositionOffset）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## IKSolverVR.RotationOffset（IKSolverVR.RotationOffset）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## IKSolverVR.Spine（IKSolverVR.Spine）

**继承**: IKSolverVR.BodyPart（IKSolverVR.身体Part）

### 字段 (53)

- `Transform headTarget`（变换 head目标）(偏移: 0x3C)
- `Transform pelvisTarget`（变换 pelvis目标）(偏移: 0x40)
- `float positionWeight`（float positionWeight）(偏移: 0x44)
- `float rotationWeight`（float rotationWeight）(偏移: 0x48)
- `float pelvisPositionWeight`（float pelvisPositionWeight）(偏移: 0x4C)
- `float pelvisRotationWeight`（float pelvisRotationWeight）(偏移: 0x50)
- `Transform chestGoal`（变换 chestGoal）(偏移: 0x54)
- `float chestGoalWeight`（float chestGoalWeight）(偏移: 0x58)
- `float minHeadHeight`（float min头部高度）(偏移: 0x5C)
- `float bodyPosStiffness`（float bodyPosStiffness）(偏移: 0x60)
- `float bodyRotStiffness`（float bodyRotStiffness）(偏移: 0x64)
- `float neckStiffness`（float neckStiffness）(偏移: 0x68)
- `float rotateChestByHands`（float rotate胸部ByHands）(偏移: 0x6C)
- `float chestClampWeight`（float chestClampWeight）(偏移: 0x70)
- `float headClampWeight`（float headClampWeight）(偏移: 0x74)
- `float moveBodyBackWhenCrouching`（float move身体后WhenCrouching）(偏移: 0x78)
- `float maintainPelvisPosition`（float maintainPelvisPosition）(偏移: 0x7C)
- `float maxRootAngle`（float max根角度）(偏移: 0x80)
- `float rootHeadingOffset`（float rootHeadingOffset）(偏移: 0x84)
- `Vector3 IKPositionHead`（三维向量 IKPosition头部）(偏移: 0x88)
- `Quaternion IKRotationHead`（Quaternion IKRotation头部）(偏移: 0x94)
- `Vector3 IKPositionPelvis`（三维向量 IKPositionPelvis）(偏移: 0xA4)
- `Quaternion IKRotationPelvis`（Quaternion IKRotationPelvis）(偏移: 0xB0)
- `Vector3 goalPositionChest`（三维向量 goalPosition胸部）(偏移: 0xC0)
- `Vector3 pelvisPositionOffset`（三维向量 pelvisPositionOffset）(偏移: 0xCC)
- `Vector3 chestPositionOffset`（三维向量 chestPositionOffset）(偏移: 0xD8)
- `Vector3 headPositionOffset`（三维向量 headPositionOffset）(偏移: 0xE4)
- `Quaternion pelvisRotationOffset`（Quaternion pelvisRotationOffset）(偏移: 0xF0)
- `Quaternion chestRotationOffset`（Quaternion chestRotationOffset）(偏移: 0x100)
- `Quaternion headRotationOffset`（Quaternion headRotationOffset）(偏移: 0x110)
- `Vector3 faceDirection`（三维向量 face方向）(偏移: 0x120)
- `Vector3 locomotionHeadPositionOffset`（三维向量 locomotion头部PositionOffset）(偏移: 0x12C)
- `Vector3 headPosition`（三维向量 headPosition）(偏移: 0x138)
- `Quaternion headRotation`（Quaternion headRotation）(偏移: 0x164)
- `Quaternion pelvisRotation`（Quaternion pelvisRotation）(偏移: 0x174)
- `Quaternion anchorRelativeToPelvis`（Quaternion anchorRelativeToPelvis）(偏移: 0x184)
- `Quaternion pelvisRelativeRotation`（Quaternion pelvisRelativeRotation）(偏移: 0x194)
- `Quaternion chestRelativeRotation`（Quaternion chestRelativeRotation）(偏移: 0x1A4)
- `Vector3 headDeltaPosition`（三维向量 headDeltaPosition）(偏移: 0x1B4)
- `Quaternion pelvisDeltaRotation`（Quaternion pelvisDeltaRotation）(偏移: 0x1C0)
- `Quaternion chestTargetRotation`（Quaternion chest目标Rotation）(偏移: 0x1D0)
- `int pelvisIndex`（int pelvis索引）(偏移: 0x1E0)
- `int spineIndex`（int spine索引）(偏移: 0x1E4)
- `int chestIndex`（int chest索引）(偏移: 0x1E8)
- `int neckIndex`（int neck索引）(偏移: 0x1EC)
- `int headIndex`（int head索引）(偏移: 0x1F0)
- `float length`（float length）(偏移: 0x1F4)
- `bool hasChest`（bool has胸部）(偏移: 0x1F8)
- `bool hasNeck`（bool has颈部）(偏移: 0x1F9)
- `bool hasLegs`（bool hasLegs）(偏移: 0x1FA)
- `float headHeight`（float head高度）(偏移: 0x1FC)
- `float sizeMlp`（float sizeMlp）(偏移: 0x200)
- `Vector3 chestForward`（三维向量 chest前进）(偏移: 0x204)

### 方法 (24)

- `IKSolverVR.VirtualBone get_pelvis()`
  （IKSolverVR.虚拟的Bone get_pelvis（））
- `IKSolverVR.VirtualBone get_firstSpineBone()`
  （IKSolverVR.虚拟的Bone get_firstSpineBone（））
- `IKSolverVR.VirtualBone get_chest()`
  （IKSolverVR.虚拟的Bone get_chest（））
- `IKSolverVR.VirtualBone get_neck()`
  （IKSolverVR.虚拟的Bone get_neck（））
- `IKSolverVR.VirtualBone get_head()`
  （IKSolverVR.虚拟的Bone get_head（））
- `Quaternion get_anchorRotation()`
  （Quaternion get_anchorRotation（））
- `void set_anchorRotation(Quaternion value)`
  （void set_anchorRotation（Quaternion value））
- `Quaternion get_anchorRelativeToHead()`
  （Quaternion get_anchorRelativeTo头部（））
- `void set_anchorRelativeToHead(Quaternion value)`
  （void set_anchorRelativeTo头部（Quaternion value））
- `void OnRead(Vector3[] positions, Quaternion[] rotations, bool hasChest, bool hasNeck, bool hasShoulders, bool hasToes, bool hasLegs, int rootIndex, int index)`
  （void OnRead（Vector3[] positions, Quaternion[] rotations, bool hasChest, bool hasNeck, bool hasShoulders, bool hasToes, bool hasLegs, int rootIndex, int index））
- `void PreSolve()`
  （void PreSolve（））
- `void ApplyOffsets()`
  （void 应用Offsets（））
- `void CalculateChestTargetRotation(IKSolverVR.VirtualBone rootBone, IKSolverVR.Arm[] arms)`
  （void 计算胸部目标Rotation（IKSolverVR.虚拟的Bone rootBone, IKSolverVR.Arm[] arms））
- `void Solve(IKSolverVR.VirtualBone rootBone, IKSolverVR.Leg[] legs, IKSolverVR.Arm[] arms)`
  （void Solve（IKSolverVR.虚拟的Bone rootBone, IKSolverVR.Leg[] legs, IKSolverVR.Arm[] arms））
- `void FABRIKPass(Vector3 animatedPelvisPos, Vector3 rootUp, float weight)`
  （void FABRIKPass（三维向量 animatedPelvisPos, 三维向量 rootUp, float weight））
- `void SolvePelvis()`
  （void SolvePelvis（））
- `void Write(ref Vector3[] solvedPositions, ref Quaternion[] solvedRotations)`
  （void Write（ref Vector3[] solvedPositions, ref Quaternion[] solvedRotations））
- `void ResetOffsets()`
  （void 重置Offsets（））
- `void AdjustChestByHands(ref Quaternion chestTargetRotation, IKSolverVR.Arm[] arms)`
  （void Adjust胸部ByHands（ref Quaternion chestTargetRotation, IKSolverVR.Arm[] arms））
- `void InverseTranslateToHead(IKSolverVR.Leg[] legs, bool limited, bool useCurrentLegMag, Vector3 offset, float w)`
  （void InverseTranslateTo头部（IKSolverVR.Leg[] legs, bool limited, bool useCurrentLegMag, 三维向量 offset, float w））
- `void TranslatePelvis(IKSolverVR.Leg[] legs, Vector3 deltaPosition, Quaternion deltaRotation)`
  （void TranslatePelvis（IKSolverVR.Leg[] legs, 三维向量 deltaPosition, Quaternion deltaRotation））
- `Vector3 LimitPelvisPosition(IKSolverVR.Leg[] legs, Vector3 pelvisPosition, bool useCurrentLegMag, int it = 2)`
  （三维向量 LimitPelvisPosition（IKSolverVR.Leg[] legs, 三维向量 pelvisPosition, bool useCurrentLegMag, int it = 2））
- `void Bend(IKSolverVR.VirtualBone[] bones, int firstIndex, int lastIndex, Quaternion targetRotation, float clampWeight, bool uniformWeight, float w)`
  （void Bend（IKSolverVR.虚拟的Bone[] bones, int firstIndex, int lastIndex, Quaternion targetRotation, float clampWeight, bool uniformWeight, float w））
- `void Bend(IKSolverVR.VirtualBone[] bones, int firstIndex, int lastIndex, Quaternion targetRotation, Quaternion rotationOffset, float clampWeight, bool uniformWeight, float w)`
  （void Bend（IKSolverVR.虚拟的Bone[] bones, int firstIndex, int lastIndex, Quaternion targetRotation, Quaternion rotationOffset, float clampWeight, bool uniformWeight, float w））

---

## IKSolverVR.VirtualBone（IKSolverVR.虚拟的Bone）

### 字段 (7)

- `Vector3 readPosition`（三维向量 readPosition）(偏移: 0x8)
- `Quaternion readRotation`（Quaternion readRotation）(偏移: 0x14)
- `Vector3 solverPosition`（三维向量 solverPosition）(偏移: 0x24)
- `Quaternion solverRotation`（Quaternion solverRotation）(偏移: 0x30)
- `float length`（float length）(偏移: 0x40)
- `float sqrMag`（float sqrMag）(偏移: 0x44)
- `Vector3 axis`（三维向量 axis）(偏移: 0x48)

### 方法 (12)

- `void Read(Vector3 position, Quaternion rotation)`
  （void Read（三维向量 position, Quaternion rotation））
- `void SwingRotation(IKSolverVR.VirtualBone[] bones, int index, Vector3 swingTarget, float weight = 1)`
  （void SwingRotation（IKSolverVR.虚拟的Bone[] bones, int index, 三维向量 swingTarget, float weight = 1））
- `float PreSolve(ref IKSolverVR.VirtualBone[] bones)`
  （float PreSolve（ref IKSolverVR.VirtualBone[] bones））
- `void RotateAroundPoint(IKSolverVR.VirtualBone[] bones, int index, Vector3 point, Quaternion rotation)`
  （void RotateAroundPoint（IKSolverVR.虚拟的Bone[] bones, int index, 三维向量 point, Quaternion rotation））
- `void RotateBy(IKSolverVR.VirtualBone[] bones, int index, Quaternion rotation)`
  （void RotateBy（IKSolverVR.虚拟的Bone[] bones, int index, Quaternion rotation））
- `void RotateBy(IKSolverVR.VirtualBone[] bones, Quaternion rotation)`
  （void RotateBy（IKSolverVR.虚拟的Bone[] bones, Quaternion rotation））
- `void RotateTo(IKSolverVR.VirtualBone[] bones, int index, Quaternion rotation)`
  （void RotateTo（IKSolverVR.虚拟的Bone[] bones, int index, Quaternion rotation））
- `void SolveTrigonometric(IKSolverVR.VirtualBone[] bones, int first, int second, int third, Vector3 targetPosition, Vector3 bendNormal, float weight)`
  （void SolveTrigonometric（IKSolverVR.虚拟的Bone[] bones, int first, int second, int third, 三维向量 targetPosition, 三维向量 bendNormal, float weight））
- `Vector3 GetDirectionToBendPoint(Vector3 direction, float directionMag, Vector3 bendDirection, float sqrMag1, float sqrMag2)`
  （三维向量 获取方向ToBendPoint（三维向量 direction, float directionMag, 三维向量 bendDirection, float sqrMag1, float sqrMag2））
- `void SolveFABRIK(IKSolverVR.VirtualBone[] bones, Vector3 startPosition, Vector3 targetPosition, float weight, float minNormalizedTargetDistance, int iterations, float length, Vector3 startOffset)`
  （void SolveFABRIK（IKSolverVR.虚拟的Bone[] bones, 三维向量 startPosition, 三维向量 targetPosition, float weight, float minNormalizedTargetDistance, int iterations, float length, 三维向量 startOffset））
- `Vector3 SolveFABRIKJoint(Vector3 pos1, Vector3 pos2, float length)`
  （三维向量 SolveFABRIKJoint（三维向量 pos1, 三维向量 pos2, float length））
- `void SolveCCD(IKSolverVR.VirtualBone[] bones, Vector3 targetPosition, float weight, int iterations)`
  （void SolveCCD（IKSolverVR.虚拟的Bone[] bones, 三维向量 targetPosition, float weight, int iterations））

---

## IMECompositionMode（IMEComposition模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## INIParser（INIParser）

### 字段 (6)

- `int error`（int error）(偏移: 0x8)
- `object m_Lock`（object m_Lock）(偏移: 0xC)
- `string m_FileName`（string m_文件名称）(偏移: 0x10)
- `string m_iniString`（string m_ini字符串）(偏移: 0x14)
- `bool m_AutoFlush`（bool m_自动Flush）(偏移: 0x18)
- `bool m_CacheModified`（bool m_缓存Modified）(偏移: 0x24)

### 方法 (33)

- `string get_FileName()`
  （string get_文件名称（））
- `string get_iniString()`
  （string get_ini字符串（））
- `void Open(string path)`
  （void 打开（string path））
- `void Open(TextAsset name)`
  （void 打开（文本资产 name））
- `void OpenFromString(string str)`
  （void 打开From字符串（string str））
- `string ToString()`
  （string To字符串（））
- `void Initialize(string iniString, bool AutoFlush)`
  （void 初始化（string iniString, bool AutoFlush））
- `void Close()`
  （void 关闭（））
- `string ParseSectionName(string Line)`
  （string 解析Section名称（string Line））
- `bool ParseKeyValuePair(string Line, ref string Key, ref string Value)`
  （bool 解析键值Pair（string Line, ref string Key, ref string Value））
- `bool isComment(string Line)`
  （bool isComment（string Line））
- `void Refresh()`
  （void 刷新（））
- `void PerformFlush()`
  （void 执行Flush（））
- `bool IsSectionExists(string SectionName)`
  （bool 是否SectionExists（string SectionName））
- `bool IsKeyExists(string SectionName, string Key)`
  （bool 是否键Exists（string SectionName, string Key））
- `void SectionDelete(string SectionName)`
  （void SectionDelete（string SectionName））
- `void KeyDelete(string SectionName, string Key)`
  （void 键Delete（string SectionName, string Key））
- `string ReadValue(string SectionName, string Key, string DefaultValue)`
  （string Read值（string SectionName, string Key, string DefaultValue））
- `void WriteValue(string SectionName, string Key, string Value)`
  （void Write值（string SectionName, string Key, string Value））
- `string EncodeByteArray(byte[] Value)`
  （string EncodeByte数组（byte[] Value））
- `byte[] DecodeByteArray(string Value)`
  （byte[] DecodeByte数组（string Value））
- `bool ReadValue(string SectionName, string Key, bool DefaultValue)`
  （bool Read值（string SectionName, string Key, bool DefaultValue））
- `int ReadValue(string SectionName, string Key, int DefaultValue)`
  （int Read值（string SectionName, string Key, int DefaultValue））
- `long ReadValue(string SectionName, string Key, long DefaultValue)`
  （long Read值（string SectionName, string Key, long DefaultValue））
- `double ReadValue(string SectionName, string Key, double DefaultValue)`
  （double Read值（string SectionName, string Key, double DefaultValue））
- `byte[] ReadValue(string SectionName, string Key, byte[] DefaultValue)`
  （byte[] Read值（string SectionName, string Key, byte[] DefaultValue））
- `DateTime ReadValue(string SectionName, string Key, DateTime DefaultValue)`
  （Date时间 Read值（string SectionName, string Key, Date时间 DefaultValue））
- `void WriteValue(string SectionName, string Key, bool Value)`
  （void Write值（string SectionName, string Key, bool Value））
- `void WriteValue(string SectionName, string Key, int Value)`
  （void Write值（string SectionName, string Key, int Value））
- `void WriteValue(string SectionName, string Key, long Value)`
  （void Write值（string SectionName, string Key, long Value））
- `void WriteValue(string SectionName, string Key, double Value)`
  （void Write值（string SectionName, string Key, double Value））
- `void WriteValue(string SectionName, string Key, byte[] Value)`
  （void Write值（string SectionName, string Key, byte[] Value））
- `void WriteValue(string SectionName, string Key, DateTime Value)`
  （void Write值（string SectionName, string Key, Date时间 Value））

---

## IOAsyncCallback（IO异步回调）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(IOAsyncResult ioares)`
  （void Invoke（IO异步Result ioares））
- `IAsyncResult BeginInvoke(IOAsyncResult ioares, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（IO异步Result ioares, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## IOAsyncResult（IO异步Result）

### 字段 (5)

- `AsyncCallback async_callback`（异步回调 async_callback）(偏移: 0x8)
- `object async_state`（object async_state）(偏移: 0xC)
- `ManualResetEvent wait_handle`（手动重置事件 wait_handle）(偏移: 0x10)
- `bool completed_synchronously`（bool completed_synchronously）(偏移: 0x14)
- `bool completed`（bool completed）(偏移: 0x15)

---

## IOException（IOException）

**继承**: SystemException（系统Exception）

### 字段 (1)

- `string _maybeFullPath`（string _maybe满路径）(偏移: 0x44)

---

## IOOperation（IOOperation）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## IOSelectorJob（IOSelectorJob）

### 字段 (3)

- `IOOperation operation`（IOOperation operation）(偏移: 0x8)
- `IOAsyncCallback callback`（IO异步回调 callback）(偏移: 0xC)
- `IOAsyncResult state`（IO异步Result state）(偏移: 0x10)

---

## IOUtil（IOUtil）

### 方法 (3)

- `bool FlagTest(MessageEnum flag, MessageEnum target)`
  （bool 标志Test（MessageEnum flag, MessageEnum target））
- `void WriteStringWithCode(string value, __BinaryWriter sout)`
  （void Write字符串WithCode（string value, __Binary写入器 sout））
- `void WriteWithCode(Type type, object value, __BinaryWriter sout)`
  （void WriteWithCode（类型 type, object value, __Binary写入器 sout））

---

## IPAddress（IPAddress）

### 字段 (13)

- `IPAddress Any`（IPAddress 任意）(偏移: 0x0)
- `IPAddress Loopback`（IPAddress Loopback）(偏移: 0x4)
- `IPAddress Broadcast`（IPAddress Broadcast）(偏移: 0x8)
- `IPAddress None`（IPAddress 无）(偏移: 0xC)
- `long m_Address`（long m_Address）(偏移: 0x8)
- `string m_ToString`（string m_To字符串）(偏移: 0x10)
- `IPAddress IPv6Any`（IPAddress IPv6任意）(偏移: 0x10)
- `IPAddress IPv6Loopback`（IPAddress IPv6Loopback）(偏移: 0x14)
- `IPAddress IPv6None`（IPAddress IPv6无）(偏移: 0x18)
- `AddressFamily m_Family`（AddressFamily m_Family）(偏移: 0x14)
- `ushort[] m_Numbers`（ushort[] m_Numbers）(偏移: 0x18)
- `long m_ScopeId`（long m_瞄准镜Id）(偏移: 0x20)
- `int m_HashCode`（int m_HashCode）(偏移: 0x28)

### 方法 (5)

- `long get_ScopeId()`
  （long get_瞄准镜Id（））
- `string ToString()`
  （string To字符串（））
- `bool Equals(object comparandObj, bool compareScopeId)`
  （bool Equals（object comparandObj, bool compareScopeId））
- `bool Equals(object comparand)`
  （bool Equals（object comparand））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## IPv4AddressHelper（IPv4Address辅助器）

### 方法 (7)

- `string ParseCanonicalName(string str, int start, int end, ref bool isLoopback)`
  （string 解析Canonical名称（string str, int start, int end, ref bool isLoopback））
- `int ParseHostNumber(string str, int start, int end)`
  （int 解析HostNumber（string str, int start, int end））
- `bool IsValid(char* name, int start, ref int end, bool allowIPv6, bool notImplicitFile, bool unknownScheme)`
  （bool 是否Valid（char* name, int start, ref int end, bool allowIPv6, bool notImplicitFile, bool unknownScheme））
- `bool IsValidCanonical(char* name, int start, ref int end, bool allowIPv6, bool notImplicitFile)`
  （bool 是否ValidCanonical（char* name, int start, ref int end, bool allowIPv6, bool notImplicitFile））
- `long ParseNonCanonical(char* name, int start, ref int end, bool notImplicitFile)`
  （long 解析NonCanonical（char* name, int start, ref int end, bool notImplicitFile））
- `bool Parse(string name, byte* numbers, int start, int end)`
  （bool 解析（string name, byte* numbers, int start, int end））
- `bool ParseCanonical(string name, byte* numbers, int start, int end)`
  （bool 解析Canonical（string name, byte* numbers, int start, int end））

---

## IPv6AddressFormatter（IPv6AddressFormatter）

### 字段 (2)

- `ushort[] address`（ushort[] address）(偏移: 0x0)
- `long scopeId`（long scopeId）(偏移: 0x8)

### 方法 (5)

- `ushort SwapUShort(ushort number)`
  （ushort SwapUShort（ushort number））
- `uint AsIPv4Int()`
  （uint AsIPv4整数（））
- `bool IsIPv4Compatible()`
  （bool 是否IPv4Compatible（））
- `bool IsIPv4Mapped()`
  （bool 是否IPv4Mapped（））
- `string ToString()`
  （string To字符串（））

---

## IPv6AddressHelper（IPv6Address辅助器）

### 方法 (6)

- `string ParseCanonicalName(string str, int start, ref bool isLoopback, ref string scopeId)`
  （string 解析Canonical名称（string str, int start, ref bool isLoopback, ref string scopeId））
- `string CreateCanonicalName(ushort* numbers)`
  （string 创建Canonical名称（ushort* numbers））
- `bool ShouldHaveIpv4Embedded(ushort* numbers)`
  （bool 应该HaveIpv4Embedded（ushort* numbers））
- `bool InternalIsValid(char* name, int start, ref int end, bool validateStrictAddress)`
  （bool 内部的是否Valid（char* name, int start, ref int end, bool validateStrictAddress））
- `bool IsValid(char* name, int start, ref int end)`
  （bool 是否Valid（char* name, int start, ref int end））
- `bool Parse(string address, ushort* numbers, int start, ref string scopeId)`
  （bool 解析（string address, ushort* numbers, int start, ref string scopeId））

---

## ITilemap（ITilemap）

### 字段 (2)

- `ITilemap s_Instance`（ITilemap s_实例）(偏移: 0x0)
- `Tilemap m_Tilemap`（Tilemap m_Tilemap）(偏移: 0x8)

### 方法 (2)

- `void RefreshTile(Vector3Int position)`
  （void 刷新Tile（三维向量整数 position））
- `ITilemap CreateInstance()`
  （ITilemap 创建实例（））

---

## Identity（Identity）

### 字段 (7)

- `string _objectUri`（string _objectUri）(偏移: 0x8)
- `IMessageSink _channelSink`（IMessageSink _channelSink）(偏移: 0xC)
- `IMessageSink _envoySink`（IMessageSink _envoySink）(偏移: 0x10)
- `DynamicPropertyCollection _clientDynamicProperties`（动态的属性Collection _client动态的Properties）(偏移: 0x14)
- `DynamicPropertyCollection _serverDynamicProperties`（动态的属性Collection _server动态的Properties）(偏移: 0x18)
- `ObjRef _objRef`（ObjRef _objRef）(偏移: 0x1C)
- `bool _disposed`（bool _disposed）(偏移: 0x20)

### 方法 (12)

- `IMessageSink get_ChannelSink()`
  （IMessageSink get_ChannelSink（））
- `void set_ChannelSink(IMessageSink value)`
  （void set_ChannelSink（IMessageSink value））
- `IMessageSink get_EnvoySink()`
  （IMessageSink get_EnvoySink（））
- `string get_ObjectUri()`
  （string get_对象Uri（））
- `void set_ObjectUri(string value)`
  （void set_对象Uri（string value））
- `bool get_IsConnected()`
  （bool get_是否Connected（））
- `bool get_Disposed()`
  （bool get_Disposed（））
- `void set_Disposed(bool value)`
  （void set_Disposed（bool value））
- `DynamicPropertyCollection get_ClientDynamicProperties()`
  （动态的属性Collection get_客户端动态的Properties（））
- `bool get_HasServerDynamicSinks()`
  （bool get_是否有服务器动态的Sinks（））
- `void NotifyClientDynamicSinks(bool start, IMessage req_msg, bool client_site, bool async)`
  （void Notify客户端动态的Sinks（bool start, IMessage req_msg, bool client_site, bool async））
- `void NotifyServerDynamicSinks(bool start, IMessage req_msg, bool client_site, bool async)`
  （void Notify服务器动态的Sinks（bool start, IMessage req_msg, bool client_site, bool async））

---

## IdnMapping（IdnMapping）

### 字段 (3)

- `bool allow_unassigned`（bool allow_unassigned）(偏移: 0x8)
- `bool use_std3`（bool use_std3）(偏移: 0x9)
- `Punycode puny`（Punycode puny）(偏移: 0xC)

### 方法 (13)

- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））
- `string GetAscii(string unicode)`
  （string 获取Ascii（string unicode））
- `string GetAscii(string unicode, int index, int count)`
  （string 获取Ascii（string unicode, int index, int count））
- `string Convert(string input, int index, int count, bool toAscii)`
  （string 转换（string input, int index, int count, bool toAscii））
- `string ToAscii(string s, int offset)`
  （string ToAscii（string s, int offset））
- `void VerifyLength(string s, int offset)`
  （void VerifyLength（string s, int offset））
- `string NamePrep(string s, int offset)`
  （string 名称Prep（string s, int offset））
- `void VerifyProhibitedCharacters(string s, int offset)`
  （void VerifyProhibitedCharacters（string s, int offset））
- `void VerifyStd3AsciiRules(string s, int offset)`
  （void VerifyStd3AsciiRules（string s, int offset））
- `string GetUnicode(string ascii)`
  （string 获取Unicode（string ascii））
- `string GetUnicode(string ascii, int index, int count)`
  （string 获取Unicode（string ascii, int index, int count））
- `string ToUnicode(string s, int offset)`
  （string ToUnicode（string s, int offset））

---

## IgnoreAttribute（IgnoreAttribute）

**继承**: Attribute（Attribute）

### 方法 (1)

- `void set_DoesNotContributeToSize(bool value)`
  （void set_DoesNotContributeTo大小（bool value））

---

## IgnoreSection（IgnoreSection）

**继承**: ConfigurationSection（ConfigurationSection）

### 方法 (6)

- `ConfigurationPropertyCollection get_Properties()`
  （Configuration属性Collection get_Properties（））
- `void DeserializeSection(XmlReader xmlReader)`
  （void DeserializeSection（Xml读取器 xmlReader））
- `bool IsModified()`
  （bool 是否Modified（））
- `void Reset(ConfigurationElement parentSection)`
  （void 重置（Configuration元素 parentSection））
- `void ResetModified()`
  （void 重置Modified（））
- `string SerializeSection(ConfigurationElement parentSection, string name, ConfigurationSaveMode saveMode)`
  （string SerializeSection（Configuration元素 parentSection, string name, Configuration保存模式 saveMode））

---

## IllogicalCallContext（IllogicalCallContext）

### 字段 (2)

- `Hashtable m_Datastore`（Hashtable m_Datastore）(偏移: 0x8)
- `object m_HostContext`（object m_HostContext）(偏移: 0xC)

### 方法 (5)

- `Hashtable get_Datastore()`
  （Hashtable get_Datastore（））
- `object get_HostContext()`
  （object get_HostContext（））
- `void set_HostContext(object value)`
  （void set_HostContext（object value））
- `bool get_HasUserData()`
  （bool get_是否有User数据（））
- `IllogicalCallContext CreateCopy()`
  （IllogicalCallContext 创建复制（））

---

## Image（图像）

**继承**: MaskableGraphic, ISerializationCallbackReceiver, ILayoutElement, ICanvasRaycastFilter（MaskableGraphic, ISerialization回调Receiver, ILayout元素, I画布RaycastFilter）

### 字段 (21)

- `Material s_ETC1DefaultUI`（材质 s_ETC1默认的界面）(偏移: 0x0)
- `Sprite m_Sprite`（精灵 m_精灵）(偏移: 0x80)
- `Sprite m_OverrideSprite`（精灵 m_重写精灵）(偏移: 0x84)
- `Image.Type m_Type`（Image.类型 m_类型）(偏移: 0x88)
- `bool m_PreserveAspect`（bool m_PreserveAspect）(偏移: 0x8C)
- `bool m_FillCenter`（bool m_Fill中心）(偏移: 0x8D)
- `Image.FillMethod m_FillMethod`（Image.FillMethod m_FillMethod）(偏移: 0x90)
- `float m_FillAmount`（float m_FillAmount）(偏移: 0x94)
- `bool m_FillClockwise`（bool m_FillClockwise）(偏移: 0x98)
- `int m_FillOrigin`（int m_FillOrigin）(偏移: 0x9C)
- `float m_AlphaHitTestMinimumThreshold`（float m_透明度命中TestMinimumThreshold）(偏移: 0xA0)
- `bool m_Tracked`（bool m_Tracked）(偏移: 0xA4)
- `bool m_UseSpriteMesh`（bool m_Use精灵网格）(偏移: 0xA5)
- `float m_PixelsPerUnitMultiplier`（float m_PixelsPerUnitMultiplier）(偏移: 0xA8)
- `float m_CachedReferencePixelsPerUnit`（float m_Cached引用PixelsPerUnit）(偏移: 0xAC)
- `Vector2[] s_VertScratch`（Vector2[] s_VertScratch）(偏移: 0x4)
- `Vector2[] s_UVScratch`（Vector2[] s_UVScratch）(偏移: 0x8)
- `Vector3[] s_Xy`（Vector3[] s_Xy）(偏移: 0xC)
- `Vector3[] s_Uv`（Vector3[] s_Uv）(偏移: 0x10)
- `List<Image> m_TrackedTexturelessImages`（List<Image> m_TrackedTexturelessImages）(偏移: 0x14)
- `bool s_Initialized`（bool s_Initialized）(偏移: 0x18)

### 方法 (71)

- `Sprite get_sprite()`
  （精灵 get_sprite（））
- `void set_sprite(Sprite value)`
  （void set_sprite（精灵 value））
- `void DisableSpriteOptimizations()`
  （void 禁用精灵Optimizations（））
- `Sprite get_overrideSprite()`
  （精灵 get_override精灵（））
- `void set_overrideSprite(Sprite value)`
  （void set_override精灵（精灵 value））
- `Sprite get_activeSprite()`
  （精灵 get_active精灵（））
- `Image.Type get_type()`
  （Image.类型 get_type（））
- `void set_type(Image.Type value)`
  （void set_type（Image.类型 value））
- `bool get_preserveAspect()`
  （bool get_preserveAspect（））
- `void set_preserveAspect(bool value)`
  （void set_preserveAspect（bool value））
- `bool get_fillCenter()`
  （bool get_fill中心（））
- `void set_fillCenter(bool value)`
  （void set_fill中心（bool value））
- `Image.FillMethod get_fillMethod()`
  （Image.FillMethod get_fillMethod（））
- `void set_fillMethod(Image.FillMethod value)`
  （void set_fillMethod（Image.FillMethod value））
- `float get_fillAmount()`
  （float get_fillAmount（））
- `void set_fillAmount(float value)`
  （void set_fillAmount（float value））
- `bool get_fillClockwise()`
  （bool get_fillClockwise（））
- `void set_fillClockwise(bool value)`
  （void set_fillClockwise（bool value））
- `int get_fillOrigin()`
  （int get_fillOrigin（））
- `void set_fillOrigin(int value)`
  （void set_fillOrigin（int value））
- `float get_eventAlphaThreshold()`
  （float get_event透明度Threshold（））
- `void set_eventAlphaThreshold(float value)`
  （void set_event透明度Threshold（float value））
- `float get_alphaHitTestMinimumThreshold()`
  （float get_alpha命中TestMinimumThreshold（））
- `void set_alphaHitTestMinimumThreshold(float value)`
  （void set_alpha命中TestMinimumThreshold（float value））
- `bool get_useSpriteMesh()`
  （bool get_use精灵网格（））
- `void set_useSpriteMesh(bool value)`
  （void set_use精灵网格（bool value））
- `Material get_defaultETC1GraphicMaterial()`
  （材质 get_defaultETC1Graphic材质（））
- `Texture get_mainTexture()`
  （纹理 get_main纹理（））
- `bool get_hasBorder()`
  （bool get_hasBorder（））
- `float get_pixelsPerUnitMultiplier()`
  （float get_pixelsPerUnitMultiplier（））
- `void set_pixelsPerUnitMultiplier(float value)`
  （void set_pixelsPerUnitMultiplier（float value））
- `float get_pixelsPerUnit()`
  （float get_pixelsPerUnit（））
- `float get_multipliedPixelsPerUnit()`
  （float get_multipliedPixelsPerUnit（））
- `Material get_material()`
  （材质 get_material（））
- `void set_material(Material value)`
  （void set_material（材质 value））
- `void OnBeforeSerialize()`
  （void OnBeforeSerialize（））
- `void OnAfterDeserialize()`
  （void OnAfterDeserialize（））
- `void PreserveSpriteAspectRatio(ref Rect rect, Vector2 spriteSize)`
  （void Preserve精灵Aspect比率（ref Rect rect, 二维向量 spriteSize））
- `Vector4 GetDrawingDimensions(bool shouldPreserveAspect)`
  （Vector4 获取DrawingDimensions（bool shouldPreserveAspect））
- `void SetNativeSize()`
  （void 集合Native大小（））
- `void OnPopulateMesh(VertexHelper toFill)`
  （void OnPopulate网格（Vertex辅助器 toFill））
- `void TrackSprite()`
  （void Track精灵（））
- `void OnEnable()`
  （void On启用（））
- `void OnDisable()`
  （void On禁用（））
- `void UpdateMaterial()`
  （void 更新材质（））
- `void OnCanvasHierarchyChanged()`
  （void On画布HierarchyChanged（））
- `void GenerateSimpleSprite(VertexHelper vh, bool lPreserveAspect)`
  （void GenerateSimple精灵（Vertex辅助器 vh, bool lPreserveAspect））
- `void GenerateSprite(VertexHelper vh, bool lPreserveAspect)`
  （void Generate精灵（Vertex辅助器 vh, bool lPreserveAspect））
- `void GenerateSlicedSprite(VertexHelper toFill)`
  （void GenerateSliced精灵（Vertex辅助器 toFill））
- `void GenerateTiledSprite(VertexHelper toFill)`
  （void GenerateTiled精灵（Vertex辅助器 toFill））
- `void AddQuad(VertexHelper vertexHelper, Vector3[] quadPositions, Color32 color, Vector3[] quadUVs)`
  （void 添加Quad（Vertex辅助器 vertexHelper, Vector3[] quadPositions, Color32 color, Vector3[] quadUVs））
- `void AddQuad(VertexHelper vertexHelper, Vector2 posMin, Vector2 posMax, Color32 color, Vector2 uvMin, Vector2 uvMax)`
  （void 添加Quad（Vertex辅助器 vertexHelper, 二维向量 posMin, 二维向量 posMax, Color32 color, 二维向量 uvMin, 二维向量 uvMax））
- `Vector4 GetAdjustedBorders(Vector4 border, Rect adjustedRect)`
  （Vector4 获取AdjustedBorders（Vector4 border, Rect adjustedRect））
- `void GenerateFilledSprite(VertexHelper toFill, bool preserveAspect)`
  （void GenerateFilled精灵（Vertex辅助器 toFill, bool preserveAspect））
- `bool RadialCut(Vector3[] xy, Vector3[] uv, float fill, bool invert, int corner)`
  （bool RadialCut（Vector3[] xy, Vector3[] uv, float fill, bool invert, int corner））
- `void RadialCut(Vector3[] xy, float cos, float sin, bool invert, int corner)`
  （void RadialCut（Vector3[] xy, float cos, float sin, bool invert, int corner））
- `void CalculateLayoutInputHorizontal()`
  （void 计算Layout输入水平（））
- `void CalculateLayoutInputVertical()`
  （void 计算Layout输入垂直（））
- `float get_minWidth()`
  （float get_min宽度（））
- `float get_preferredWidth()`
  （float get_preferred宽度（））
- `float get_flexibleWidth()`
  （float get_flexible宽度（））
- `float get_minHeight()`
  （float get_min高度（））
- `float get_preferredHeight()`
  （float get_preferred高度（））
- `float get_flexibleHeight()`
  （float get_flexible高度（））
- `int get_layoutPriority()`
  （int get_layoutPriority（））
- `bool IsRaycastLocationValid(Vector2 screenPoint, Camera eventCamera)`
  （bool 是否RaycastLocationValid（二维向量 screenPoint, 摄像机 eventCamera））
- `Vector2 MapCoordinate(Vector2 local, Rect rect)`
  （二维向量 映射Coordinate（二维向量 local, Rect rect））
- `void RebuildImage(SpriteAtlas spriteAtlas)`
  （void Rebuild图像（精灵Atlas spriteAtlas））
- `void TrackImage(Image g)`
  （void Track图像（图像 g））
- `void UnTrackImage(Image g)`
  （void UnTrack图像（图像 g））
- `void OnDidApplyAnimationProperties()`
  （void OnDid应用动画Properties（））

---

## Image.FillMethod（Image.FillMethod）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Image.Origin180（Image.Origin180）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Image.Origin360（Image.Origin360）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Image.Origin90（Image.Origin90）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Image.OriginHorizontal（Image.Origin水平）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Image.OriginVertical（Image.Origin垂直）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Image.Type（Image.类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ImagePosition（图像Position）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## ImpulseGenerator（ImpulseGenerator）

**继承**: RO_WorkListener（RO_Work监听器）

### 字段 (8)

- `float power`（float power）(偏移: 0xC)
- `float duration`（float duration）(偏移: 0x10)
- `float minRadius`（float minRadius）(偏移: 0x14)
- `float maxRadius`（float maxRadius）(偏移: 0x18)
- `float delay`（float delay）(偏移: 0x1C)
- `int totalCount`（int total数量）(偏移: 0x20)
- `float interval`（float interval）(偏移: 0x24)
- `int restCount`（int rest数量）(偏移: 0x28)

### 方法 (2)

- `void Work()`
  （void Work（））
- `IEnumerator Generator()`
  （IEnumerator Generator（））

---

## IncrementStripIndexOnStart（IncrementStrip索引On开始）

**继承**: VFXSpawnerCallbacks（VFXSpawnerCallbacks）

### 字段 (3)

- `int stripMaxCountID`（int strip最大数量ID）(偏移: 0x0)
- `int stripIndexID`（int strip索引ID）(偏移: 0x4)
- `uint m_Index`（uint m_索引）(偏移: 0xC)

### 方法 (3)

- `void OnPlay(VFXSpawnerState state, VFXExpressionValues vfxValues, VisualEffect vfxComponent)`
  （void On播放（VFXSpawner状态 state, VFXExpressionValues vfxValues, Visual特效 vfxComponent））
- `void OnStop(VFXSpawnerState state, VFXExpressionValues vfxValues, VisualEffect vfxComponent)`
  （void On停止（VFXSpawner状态 state, VFXExpressionValues vfxValues, Visual特效 vfxComponent））
- `void OnUpdate(VFXSpawnerState state, VFXExpressionValues vfxValues, VisualEffect vfxComponent)`
  （void On更新（VFXSpawner状态 state, VFXExpressionValues vfxValues, Visual特效 vfxComponent））

---

## IncrementStripIndexOnStart.InputProperties（IncrementStrip索引OnStart.输入Properties）

### 字段 (1)

- `uint StripMaxCount`（uint Strip最大数量）(偏移: 0x8)

---

## IndexFormat（索引格式化）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Inertia（Inertia）

**继承**: OffsetModifier（Offset修改器）

### 字段 (2)

- `Inertia.Body[] bodies`（Inertia.Body[] bodies）(偏移: 0x18)
- `OffsetModifier.OffsetLimits[] limits`（OffsetModifier.OffsetLimits[] limits）(偏移: 0x1C)

### 方法 (2)

- `void ResetBodies()`
  （void 重置Bodies（））
- `void OnModifyOffset()`
  （void OnModifyOffset（））

---

## Inertia.Body（Inertia.身体）

### 字段 (11)

- `Transform transform`（变换 transform）(偏移: 0x8)
- `Inertia.Body.EffectorLink[] effectorLinks`（Inertia.Body.EffectorLink[] effectorLinks）(偏移: 0xC)
- `float speed`（float speed）(偏移: 0x10)
- `float acceleration`（float acceleration）(偏移: 0x14)
- `float matchVelocity`（float match速度）(偏移: 0x18)
- `float gravity`（float gravity）(偏移: 0x1C)
- `Vector3 delta`（三维向量 delta）(偏移: 0x20)
- `Vector3 lazyPoint`（三维向量 lazyPoint）(偏移: 0x2C)
- `Vector3 direction`（三维向量 direction）(偏移: 0x38)
- `Vector3 lastPosition`（三维向量 lastPosition）(偏移: 0x44)
- `bool firstUpdate`（bool first更新）(偏移: 0x50)

### 方法 (2)

- `void Reset()`
  （void 重置（））
- `void Update(IKSolverFullBodyBiped solver, float weight, float deltaTime)`
  （void 更新（IKSolver满身体Biped solver, float weight, float deltaTime））

---

## Inertia.Body.EffectorLink（Inertia.Body.EffectorLink）

### 字段 (2)

- `FullBodyBipedEffector effector`（满身体BipedEffector effector）(偏移: 0x8)
- `float weight`（float weight）(偏移: 0xC)

---

## InfTree（InfTree）

### 字段 (12)

- `int[] fixed_tl`（int[] fixed_tl）(偏移: 0x0)
- `int[] fixed_td`（int[] fixed_td）(偏移: 0x4)
- `int[] cplens`（int[] cplens）(偏移: 0x8)
- `int[] cplext`（int[] cplext）(偏移: 0xC)
- `int[] cpdist`（int[] cpdist）(偏移: 0x10)
- `int[] cpdext`（int[] cpdext）(偏移: 0x14)
- `int[] hn`（int[] hn）(偏移: 0x8)
- `int[] v`（int[] v）(偏移: 0xC)
- `int[] c`（int[] c）(偏移: 0x10)
- `int[] r`（int[] r）(偏移: 0x14)
- `int[] u`（int[] u）(偏移: 0x18)
- `int[] x`（int[] x）(偏移: 0x1C)

### 方法 (5)

- `int huft_build(int[] b, int bindex, int n, int s, int[] d, int[] e, int[] t, int[] m, int[] hp, int[] hn, int[] v)`
  （int huft_build（int[] b, int bindex, int n, int s, int[] d, int[] e, int[] t, int[] m, int[] hp, int[] hn, int[] v））
- `int inflate_trees_bits(int[] c, int[] bb, int[] tb, int[] hp, ZlibCodec z)`
  （int inflate_trees_bits（int[] c, int[] bb, int[] tb, int[] hp, ZlibCodec z））
- `int inflate_trees_dynamic(int nl, int nd, int[] c, int[] bl, int[] bd, int[] tl, int[] td, int[] hp, ZlibCodec z)`
  （int inflate_trees_dynamic（int nl, int nd, int[] c, int[] bl, int[] bd, int[] tl, int[] td, int[] hp, ZlibCodec z））
- `int inflate_trees_fixed(int[] bl, int[] bd, int[][] tl, int[][] td, ZlibCodec z)`
  （int inflate_trees_fixed（int[] bl, int[] bd, int[][] tl, int[][] td, ZlibCodec z））
- `void initWorkArea(int vsize)`
  （void initWorkArea（int vsize））

---

## InfiniteRotator（InfiniteRotator）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (1)

- `float speed`（float speed）(偏移: 0xC)

### 方法 (1)

- `void Update()`
  （void 更新（））

---

## InfiniteRuntimeClip（InfiniteRuntime弹匣）

**继承**: RuntimeElement（Runtime元素）

### 字段 (2)

- `Playable m_Playable`（Playable m_Playable）(偏移: 0xC)
- `long kIntervalEnd`（long k间隔结束）(偏移: 0x0)

### 方法 (4)

- `long get_intervalStart()`
  （long get_interval开始（））
- `long get_intervalEnd()`
  （long get_interval结束（））
- `void set_enable(bool value)`
  （void set_enable（bool value））
- `void EvaluateAt(double localTime, FrameData frameData)`
  （void EvaluateAt（double localTime, Frame数据 frameData））

---

## InfinityAmmoBuff（无限弹药增益）

**继承**: Buff（增益）

### 方法 (2)

- `void BuffUpdater(ref bool value)`
  （void 增益更新器（ref bool value））
- `void OnLifeEnd()`
  （void OnLife结束（））

---

## InflateBlocks（InflateBlocks）

### 字段 (21)

- `int[] border`（int[] border）(偏移: 0x0)
- `InflateBlocks.InflateBlockMode mode`（InflateBlocks.InflateBlock模式 mode）(偏移: 0x8)
- `int left`（int left）(偏移: 0xC)
- `int table`（int table）(偏移: 0x10)
- `int index`（int index）(偏移: 0x14)
- `int[] blens`（int[] blens）(偏移: 0x18)
- `int[] bb`（int[] bb）(偏移: 0x1C)
- `int[] tb`（int[] tb）(偏移: 0x20)
- `InflateCodes codes`（InflateCodes codes）(偏移: 0x24)
- `int last`（int last）(偏移: 0x28)
- `ZlibCodec _codec`（ZlibCodec _codec）(偏移: 0x2C)
- `int bitk`（int bitk）(偏移: 0x30)
- `int bitb`（int bitb）(偏移: 0x34)
- `int[] hufts`（int[] hufts）(偏移: 0x38)
- `byte[] window`（byte[] window）(偏移: 0x3C)
- `int end`（int end）(偏移: 0x40)
- `int readAt`（int readAt）(偏移: 0x44)
- `int writeAt`（int writeAt）(偏移: 0x48)
- `object checkfn`（object checkfn）(偏移: 0x4C)
- `uint check`（uint check）(偏移: 0x50)
- `InfTree inftree`（InfTree inftree）(偏移: 0x54)

### 方法 (4)

- `uint Reset()`
  （uint 重置（））
- `int Process(int r)`
  （int 处理（int r））
- `void Free()`
  （void Free（））
- `int Flush(int r)`
  （int Flush（int r））

---

## InflateBlocks.InflateBlockMode（InflateBlocks.InflateBlock模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## InflateCodes（InflateCodes）

### 字段 (14)

- `int mode`（int mode）(偏移: 0x8)
- `int len`（int len）(偏移: 0xC)
- `int[] tree`（int[] tree）(偏移: 0x10)
- `int tree_index`（int tree_index）(偏移: 0x14)
- `int need`（int need）(偏移: 0x18)
- `int lit`（int lit）(偏移: 0x1C)
- `int bitsToGet`（int bitsTo获取）(偏移: 0x20)
- `int dist`（int dist）(偏移: 0x24)
- `byte lbits`（byte lbits）(偏移: 0x28)
- `byte dbits`（byte dbits）(偏移: 0x29)
- `int[] ltree`（int[] ltree）(偏移: 0x2C)
- `int ltree_index`（int ltree_index）(偏移: 0x30)
- `int[] dtree`（int[] dtree）(偏移: 0x34)
- `int dtree_index`（int dtree_index）(偏移: 0x38)

### 方法 (3)

- `void Init(int bl, int bd, int[] tl, int tl_index, int[] td, int td_index)`
  （void 初始化（int bl, int bd, int[] tl, int tl_index, int[] td, int td_index））
- `int Process(InflateBlocks blocks, int r)`
  （int 处理（InflateBlocks blocks, int r））
- `int InflateFast(int bl, int bd, int[] tl, int tl_index, int[] td, int td_index, InflateBlocks s, ZlibCodec z)`
  （int InflateFast（int bl, int bd, int[] tl, int tl_index, int[] td, int td_index, InflateBlocks s, ZlibCodec z））

---

## InflateManager（Inflate管理器）

### 字段 (10)

- `InflateManager.InflateManagerMode mode`（InflateManager.Inflate管理器模式 mode）(偏移: 0x8)
- `ZlibCodec _codec`（ZlibCodec _codec）(偏移: 0xC)
- `int method`（int method）(偏移: 0x10)
- `uint computedCheck`（uint computed检查）(偏移: 0x14)
- `uint expectedCheck`（uint expected检查）(偏移: 0x18)
- `int marker`（int marker）(偏移: 0x1C)
- `bool _handleRfc1950HeaderBytes`（bool _handleRfc1950标题Bytes）(偏移: 0x20)
- `int wbits`（int wbits）(偏移: 0x24)
- `InflateBlocks blocks`（InflateBlocks blocks）(偏移: 0x28)
- `byte[] mark`（byte[] mark）(偏移: 0x0)

### 方法 (5)

- `bool get_HandleRfc1950HeaderBytes()`
  （bool get_句柄Rfc1950标题Bytes（））
- `int Reset()`
  （int 重置（））
- `int End()`
  （int 结束（））
- `int Initialize(ZlibCodec codec, int w)`
  （int 初始化（ZlibCodec codec, int w））
- `int Inflate(FlushType flush)`
  （int Inflate（Flush类型 flush））

---

## InflateManager.InflateManagerMode（InflateManager.Inflate管理器模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## InjectionDetector（InjectionDetector）

**继承**: ACTkDetectorBase（ACTkDetector基础）

### 方法 (6)

- `InjectionDetector get_Instance()`
  （InjectionDetector get_实例（））
- `void StartDetection()`
  （void 开始Detection（））
- `void StartDetection(Action<string> callback)`
  （void 开始Detection（Action<string> callback））
- `void StopDetection()`
  （void 停止Detection（））
- `void Dispose()`
  （void 释放（））
- `void StartDetectionAutomatically()`
  （void 开始DetectionAutomatically（））

---

## Input（输入）

### 方法 (33)

- `bool GetKeyInt(KeyCode key)`
  （bool 获取键整数（键Code key））
- `bool GetKeyUpInt(KeyCode key)`
  （bool 获取键上整数（键Code key））
- `bool GetKeyDownInt(KeyCode key)`
  （bool 获取键下整数（键Code key））
- `bool GetKeyDownString(string name)`
  （bool 获取键下字符串（string name））
- `float GetAxis(string axisName)`
  （float 获取轴（string axisName））
- `float GetAxisRaw(string axisName)`
  （float 获取轴Raw（string axisName））
- `bool GetButton(string buttonName)`
  （bool 获取按钮（string buttonName））
- `bool GetButtonDown(string buttonName)`
  （bool 获取按钮下（string buttonName））
- `bool GetButtonUp(string buttonName)`
  （bool 获取按钮上（string buttonName））
- `bool GetMouseButton(int button)`
  （bool 获取鼠标按钮（int button））
- `bool GetMouseButtonDown(int button)`
  （bool 获取鼠标按钮下（int button））
- `bool GetMouseButtonUp(int button)`
  （bool 获取鼠标按钮上（int button））
- `Touch GetTouch(int index)`
  （触摸 获取触摸（int index））
- `bool GetKey(KeyCode key)`
  （bool 获取键（键Code key））
- `bool GetKeyUp(KeyCode key)`
  （bool 获取键上（键Code key））
- `bool GetKeyDown(KeyCode key)`
  （bool 获取键下（键Code key））
- `bool GetKeyDown(string name)`
  （bool 获取键下（string name））
- `Vector3 get_mousePosition()`
  （三维向量 get_mousePosition（））
- `Vector2 get_mouseScrollDelta()`
  （二维向量 get_mouse滚动Delta（））
- `IMECompositionMode get_imeCompositionMode()`
  （IMEComposition模式 get_imeComposition模式（））
- `void set_imeCompositionMode(IMECompositionMode value)`
  （void set_imeComposition模式（IMEComposition模式 value））
- `string get_compositionString()`
  （string get_composition字符串（））
- `Vector2 get_compositionCursorPos()`
  （二维向量 get_compositionCursorPos（））
- `void set_compositionCursorPos(Vector2 value)`
  （void set_compositionCursorPos（二维向量 value））
- `bool get_mousePresent()`
  （bool get_mousePresent（））
- `int get_touchCount()`
  （int get_touch数量（））
- `bool get_touchSupported()`
  （bool get_touchSupported（））
- `Touch[] get_touches()`
  （Touch[] get_touches（））
- `void GetTouch_Injected(int index, out Touch ret)`
  （void 获取Touch_Injected（int index, out Touch ret））
- `void get_mousePosition_Injected(out Vector3 ret)`
  （void get_mousePosition_Injected（out Vector3 ret））
- `void get_mouseScrollDelta_Injected(out Vector2 ret)`
  （void get_mouse滚动Delta_Injected（out Vector2 ret））
- `void get_compositionCursorPos_Injected(out Vector2 ret)`
  （void get_compositionCursorPos_Injected（out Vector2 ret））
- `void set_compositionCursorPos_Injected(ref Vector2 value)`
  （void set_compositionCursorPos_Injected（ref Vector2 value））

---

## InputDevice（输入Device）

**继承**: IEquatable<InputDevice>（IEquatable<输入Device>）

### 字段 (2)

- `ulong m_DeviceId`（ulong m_DeviceId）(偏移: 0x0)
- `bool m_Initialized`（bool m_Initialized）(偏移: 0x8)

### 方法 (4)

- `ulong get_deviceId()`
  （ulong get_deviceId（））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `bool Equals(InputDevice other)`
  （bool Equals（输入Device other））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## InputDevices（输入Devices）

### 字段 (3)

- `Action<InputDevice> deviceConnected`（Action<输入Device> deviceConnected）(偏移: 0x0)
- `Action<InputDevice> deviceDisconnected`（Action<输入Device> deviceDisconnected）(偏移: 0x4)
- `Action<InputDevice> deviceConfigChanged`（Action<输入Device> device配置Changed）(偏移: 0x8)

### 方法 (1)

- `void InvokeConnectionEvent(ulong deviceId, ConnectionChangeType change)`
  （void Invoke连接事件（ulong deviceId, 连接Change类型 change））

---

## InputFeatureType（输入Feature类型）

### 字段 (1)

- `uint value__`（uint value__）(偏移: 0x0)

---

## InputFeatureUsage（输入FeatureUsage）

**继承**: IEquatable<InputFeatureUsage>（IEquatable<输入FeatureUsage>）

### 字段 (2)

- `string m_Name`（string m_名称）(偏移: 0x0)
- `InputFeatureType m_InternalType`（输入Feature类型 m_内部的类型）(偏移: 0x4)

### 方法 (5)

- `string get_name()`
  （string get_name（））
- `InputFeatureType get_internalType()`
  （输入Feature类型 get_internal类型（））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `bool Equals(InputFeatureUsage other)`
  （bool Equals（输入FeatureUsage other））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## InputField（输入Field）

**继承**: Selectable, IUpdateSelectedHandler, IEventSystemHandler, IBeginDragHandler, IDragHandler, IEndDragHandler, IPointerClickHandler, ISubmitHandler, ICanvasElement, ILayoutElement（Selectable, I更新选中的处理器, I事件系统处理器, IBeginDrag处理器, IDrag处理器, I结束Drag处理器, I指针Click处理器, ISubmit处理器, I画布元素, ILayout元素）

### 字段 (47)

- `TouchScreenKeyboard m_Keyboard`（触摸屏幕的键盘 m_键盘）(偏移: 0xB0)
- `char[] kSeparators`（char[] kSeparators）(偏移: 0x0)
- `Text m_TextComponent`（文本 m_文本组件）(偏移: 0xB4)
- `Graphic m_Placeholder`（Graphic m_Placeholder）(偏移: 0xB8)
- `InputField.ContentType m_ContentType`（输入Field.Content类型 m_Content类型）(偏移: 0xBC)
- `InputField.InputType m_InputType`（输入Field.输入类型 m_输入类型）(偏移: 0xC0)
- `char m_AsteriskChar`（char m_AsteriskChar）(偏移: 0xC4)
- `TouchScreenKeyboardType m_KeyboardType`（触摸屏幕的键盘类型 m_键盘类型）(偏移: 0xC8)
- `InputField.LineType m_LineType`（输入Field.Line类型 m_Line类型）(偏移: 0xCC)
- `bool m_HideMobileInput`（bool m_隐藏Mobile输入）(偏移: 0xD0)
- `InputField.CharacterValidation m_CharacterValidation`（输入Field.角色Validation m_角色Validation）(偏移: 0xD4)
- `int m_CharacterLimit`（int m_角色Limit）(偏移: 0xD8)
- `InputField.SubmitEvent m_OnEndEdit`（输入Field.Submit事件 m_On结束Edit）(偏移: 0xDC)
- `InputField.OnChangeEvent m_OnValueChanged`（输入Field.OnChange事件 m_On值Changed）(偏移: 0xE0)
- `InputField.OnValidateInput m_OnValidateInput`（输入Field.On验证输入 m_On验证输入）(偏移: 0xE4)
- `Color m_CaretColor`（颜色 m_Caret颜色）(偏移: 0xE8)
- `bool m_CustomCaretColor`（bool m_自定义的Caret颜色）(偏移: 0xF8)
- `Color m_SelectionColor`（颜色 m_Selection颜色）(偏移: 0xFC)
- `string m_Text`（string m_文本）(偏移: 0x10C)
- `float m_CaretBlinkRate`（float m_CaretBlinkRate）(偏移: 0x110)
- `int m_CaretWidth`（int m_Caret宽度）(偏移: 0x114)
- `bool m_ReadOnly`（bool m_ReadOnly）(偏移: 0x118)
- `bool m_ShouldActivateOnSelect`（bool m_应该激活On选择）(偏移: 0x119)
- `int m_CaretPosition`（int m_CaretPosition）(偏移: 0x11C)
- `int m_CaretSelectPosition`（int m_Caret选择Position）(偏移: 0x120)
- `RectTransform caretRectTrans`（Rect变换 caretRectTrans）(偏移: 0x124)
- `UIVertex[] m_CursorVerts`（界面Vertex[] m_CursorVerts）(偏移: 0x128)
- `TextGenerator m_InputTextCache`（文本Generator m_输入文本缓存）(偏移: 0x12C)
- `CanvasRenderer m_CachedInputRenderer`（画布渲染器 m_Cached输入渲染器）(偏移: 0x130)
- `bool m_PreventFontCallback`（bool m_阻止Font回调）(偏移: 0x134)
- `Mesh m_Mesh`（网格 m_网格）(偏移: 0x138)
- `bool m_AllowInput`（bool m_允许输入）(偏移: 0x13C)
- `bool m_ShouldActivateNextUpdate`（bool m_应该激活下一个更新）(偏移: 0x13D)
- `bool m_UpdateDrag`（bool m_更新Drag）(偏移: 0x13E)
- `bool m_DragPositionOutOfBounds`（bool m_DragPositionOutOfBounds）(偏移: 0x13F)
- `bool m_CaretVisible`（bool m_Caret可见的）(偏移: 0x140)
- `Coroutine m_BlinkCoroutine`（协程 m_Blink协程）(偏移: 0x144)
- `float m_BlinkStartTime`（float m_Blink开始时间）(偏移: 0x148)
- `int m_DrawStart`（int m_Draw开始）(偏移: 0x14C)
- `int m_DrawEnd`（int m_Draw结束）(偏移: 0x150)
- `Coroutine m_DragCoroutine`（协程 m_Drag协程）(偏移: 0x154)
- `string m_OriginalText`（string m_Original文本）(偏移: 0x158)
- `bool m_WasCanceled`（bool m_WasCanceled）(偏移: 0x15C)
- `bool m_HasDoneFocusTransition`（bool m_是否有Done聚焦Transition）(偏移: 0x15D)
- `WaitForSecondsRealtime m_WaitForSecondsRealtime`（WaitForSecondsRealtime m_WaitForSecondsRealtime）(偏移: 0x160)
- `bool m_TouchKeyboardAllowsInPlaceEditing`（bool m_触摸键盘AllowsInPlaceEditing）(偏移: 0x164)
- `Event m_ProcessingEvent`（事件 m_Processing事件）(偏移: 0x168)

### 方法 (156)

- `BaseInput get_input()`
  （基础输入 get_input（））
- `string get_compositionString()`
  （string get_composition字符串（））
- `Mesh get_mesh()`
  （网格 get_mesh（））
- `TextGenerator get_cachedInputTextGenerator()`
  （文本Generator get_cached输入文本Generator（））
- `void set_shouldHideMobileInput(bool value)`
  （void set_should隐藏Mobile输入（bool value））
- `bool get_shouldHideMobileInput()`
  （bool get_should隐藏Mobile输入（））
- `void set_shouldActivateOnSelect(bool value)`
  （void set_should激活On选择（bool value））
- `bool get_shouldActivateOnSelect()`
  （bool get_should激活On选择（））
- `string get_text()`
  （string get_text（））
- `void set_text(string value)`
  （void set_text（string value））
- `void SetTextWithoutNotify(string input)`
  （void 集合文本WithoutNotify（string input））
- `void SetText(string value, bool sendCallback = True)`
  （void 集合文本（string value, bool sendCallback = True））
- `bool get_isFocused()`
  （bool get_is聚焦的（））
- `float get_caretBlinkRate()`
  （float get_caretBlinkRate（））
- `void set_caretBlinkRate(float value)`
  （void set_caretBlinkRate（float value））
- `int get_caretWidth()`
  （int get_caret宽度（））
- `void set_caretWidth(int value)`
  （void set_caret宽度（int value））
- `Text get_textComponent()`
  （文本 get_text组件（））
- `void set_textComponent(Text value)`
  （void set_text组件（文本 value））
- `Graphic get_placeholder()`
  （Graphic get_placeholder（））
- `void set_placeholder(Graphic value)`
  （void set_placeholder（Graphic value））
- `Color get_caretColor()`
  （颜色 get_caret颜色（））
- `void set_caretColor(Color value)`
  （void set_caret颜色（颜色 value））
- `bool get_customCaretColor()`
  （bool get_customCaret颜色（））
- `void set_customCaretColor(bool value)`
  （void set_customCaret颜色（bool value））
- `Color get_selectionColor()`
  （颜色 get_selection颜色（））
- `void set_selectionColor(Color value)`
  （void set_selection颜色（颜色 value））
- `InputField.SubmitEvent get_onEndEdit()`
  （输入Field.Submit事件 get_on结束Edit（））
- `void set_onEndEdit(InputField.SubmitEvent value)`
  （void set_on结束Edit（输入Field.Submit事件 value））
- `InputField.OnChangeEvent get_onValueChange()`
  （输入Field.OnChange事件 get_on值Change（））
- `void set_onValueChange(InputField.OnChangeEvent value)`
  （void set_on值Change（输入Field.OnChange事件 value））
- `InputField.OnChangeEvent get_onValueChanged()`
  （输入Field.OnChange事件 get_on值Changed（））
- `void set_onValueChanged(InputField.OnChangeEvent value)`
  （void set_on值Changed（输入Field.OnChange事件 value））
- `InputField.OnValidateInput get_onValidateInput()`
  （输入Field.On验证输入 get_on验证输入（））
- `void set_onValidateInput(InputField.OnValidateInput value)`
  （void set_on验证输入（输入Field.On验证输入 value））
- `int get_characterLimit()`
  （int get_characterLimit（））
- `void set_characterLimit(int value)`
  （void set_characterLimit（int value））
- `InputField.ContentType get_contentType()`
  （输入Field.Content类型 get_content类型（））
- `void set_contentType(InputField.ContentType value)`
  （void set_content类型（输入Field.Content类型 value））
- `InputField.LineType get_lineType()`
  （输入Field.Line类型 get_line类型（））
- `void set_lineType(InputField.LineType value)`
  （void set_line类型（输入Field.Line类型 value））
- `InputField.InputType get_inputType()`
  （输入Field.输入类型 get_input类型（））
- `void set_inputType(InputField.InputType value)`
  （void set_input类型（输入Field.输入类型 value））
- `TouchScreenKeyboard get_touchScreenKeyboard()`
  （触摸屏幕的键盘 get_touch屏幕的键盘（））
- `TouchScreenKeyboardType get_keyboardType()`
  （触摸屏幕的键盘类型 get_keyboard类型（））
- `void set_keyboardType(TouchScreenKeyboardType value)`
  （void set_keyboard类型（触摸屏幕的键盘类型 value））
- `InputField.CharacterValidation get_characterValidation()`
  （输入Field.角色Validation get_characterValidation（））
- `void set_characterValidation(InputField.CharacterValidation value)`
  （void set_characterValidation（输入Field.角色Validation value））
- `bool get_readOnly()`
  （bool get_readOnly（））
- `void set_readOnly(bool value)`
  （void set_readOnly（bool value））
- `bool get_multiLine()`
  （bool get_multiLine（））
- `char get_asteriskChar()`
  （char get_asteriskChar（））
- `void set_asteriskChar(char value)`
  （void set_asteriskChar（char value））
- `bool get_wasCanceled()`
  （bool get_wasCanceled（））
- `void ClampPos(ref int pos)`
  （void ClampPos（ref int pos））
- `int get_caretPositionInternal()`
  （int get_caretPosition内部的（））
- `void set_caretPositionInternal(int value)`
  （void set_caretPosition内部的（int value））
- `int get_caretSelectPositionInternal()`
  （int get_caret选择Position内部的（））
- `void set_caretSelectPositionInternal(int value)`
  （void set_caret选择Position内部的（int value））
- `bool get_hasSelection()`
  （bool get_hasSelection（））
- `int get_caretPosition()`
  （int get_caretPosition（））
- `void set_caretPosition(int value)`
  （void set_caretPosition（int value））
- `int get_selectionAnchorPosition()`
  （int get_selectionAnchorPosition（））
- `void set_selectionAnchorPosition(int value)`
  （void set_selectionAnchorPosition（int value））
- `int get_selectionFocusPosition()`
  （int get_selection聚焦Position（））
- `void set_selectionFocusPosition(int value)`
  （void set_selection聚焦Position（int value））
- `void OnEnable()`
  （void On启用（））
- `void OnDisable()`
  （void On禁用（））
- `IEnumerator CaretBlink()`
  （IEnumerator CaretBlink（））
- `void SetCaretVisible()`
  （void 集合Caret可见的（））
- `void SetCaretActive()`
  （void 集合Caret激活的（））
- `void UpdateCaretMaterial()`
  （void 更新Caret材质（））
- `void OnFocus()`
  （void On聚焦（））
- `void SelectAll()`
  （void 选择所有（））
- `void MoveTextEnd(bool shift)`
  （void 移动文本结束（bool shift））
- `void MoveTextStart(bool shift)`
  （void 移动文本开始（bool shift））
- `string get_clipboard()`
  （string get_clipboard（））
- `void set_clipboard(string value)`
  （void set_clipboard（string value））
- `bool TouchScreenKeyboardShouldBeUsed()`
  （bool 触摸屏幕的键盘应该BeUsed（））
- `bool InPlaceEditing()`
  （bool InPlaceEditing（））
- `bool InPlaceEditingChanged()`
  （bool InPlaceEditingChanged（））
- `void UpdateCaretFromKeyboard()`
  （void 更新CaretFrom键盘（））
- `void LateUpdate()`
  （void 延迟更新（））
- `Vector2 ScreenToLocal(Vector2 screen)`
  （二维向量 屏幕的To本地的（二维向量 screen））
- `int GetUnclampedCharacterLineFromPosition(Vector2 pos, TextGenerator generator)`
  （int 获取Unclamped角色LineFromPosition（二维向量 pos, 文本Generator generator））
- `int GetCharacterIndexFromPosition(Vector2 pos)`
  （int 获取角色索引FromPosition（二维向量 pos））
- `bool MayDrag(PointerEventData eventData)`
  （bool MayDrag（指针事件数据 eventData））
- `void OnBeginDrag(PointerEventData eventData)`
  （void OnBeginDrag（指针事件数据 eventData））
- `void OnDrag(PointerEventData eventData)`
  （void OnDrag（指针事件数据 eventData））
- `IEnumerator MouseDragOutsideRect(PointerEventData eventData)`
  （IEnumerator 鼠标DragOutsideRect（指针事件数据 eventData））
- `void OnEndDrag(PointerEventData eventData)`
  （void On结束Drag（指针事件数据 eventData））
- `void OnPointerDown(PointerEventData eventData)`
  （void On指针下（指针事件数据 eventData））
- `InputField.EditState KeyPressed(Event evt)`
  （输入Field.Edit状态 键按下的（事件 evt））
- `bool IsValidChar(char c)`
  （bool 是否ValidChar（char c））
- `void ProcessEvent(Event e)`
  （void 处理事件（事件 e））
- `void OnUpdateSelected(BaseEventData eventData)`
  （void On更新选中的（基础事件数据 eventData））
- `string GetSelectedString()`
  （string 获取选中的字符串（））
- `int FindtNextWordBegin()`
  （int Findt下一个WordBegin（））
- `void MoveRight(bool shift, bool ctrl)`
  （void 移动右（bool shift, bool ctrl））
- `int FindtPrevWordBegin()`
  （int FindtPrevWordBegin（））
- `void MoveLeft(bool shift, bool ctrl)`
  （void 移动左（bool shift, bool ctrl））
- `int DetermineCharacterLine(int charPos, TextGenerator generator)`
  （int Determine角色Line（int charPos, 文本Generator generator））
- `int LineUpCharacterPosition(int originalPos, bool goToFirstChar)`
  （int Line上角色Position（int originalPos, bool goToFirstChar））
- `int LineDownCharacterPosition(int originalPos, bool goToLastChar)`
  （int Line下角色Position（int originalPos, bool goToLastChar））
- `void MoveDown(bool shift)`
  （void 移动下（bool shift））
- `void MoveDown(bool shift, bool goToLastChar)`
  （void 移动下（bool shift, bool goToLastChar））
- `void MoveUp(bool shift)`
  （void 移动上（bool shift））
- `void MoveUp(bool shift, bool goToFirstChar)`
  （void 移动上（bool shift, bool goToFirstChar））
- `void Delete()`
  （void Delete（））
- `void ForwardSpace()`
  （void 前进Space（））
- `void Backspace()`
  （void Backspace（））
- `void Insert(char c)`
  （void Insert（char c））
- `void UpdateTouchKeyboardFromEditChanges()`
  （void 更新触摸键盘FromEditChanges（））
- `void SendOnValueChangedAndUpdateLabel()`
  （void 发送On值ChangedAnd更新标签（））
- `void SendOnValueChanged()`
  （void 发送On值Changed（））
- `void SendOnSubmit()`
  （void 发送OnSubmit（））
- `void Append(string input)`
  （void Append（string input））
- `void Append(char input)`
  （void Append（char input））
- `void UpdateLabel()`
  （void 更新标签（））
- `bool IsSelectionVisible()`
  （bool 是否Selection可见的（））
- `int GetLineStartPosition(TextGenerator gen, int line)`
  （int 获取Line开始Position（文本Generator gen, int line））
- `int GetLineEndPosition(TextGenerator gen, int line)`
  （int 获取Line结束Position（文本Generator gen, int line））
- `void SetDrawRangeToContainCaretPosition(int caretPos)`
  （void 集合Draw范围ToContainCaretPosition（int caretPos））
- `void ForceLabelUpdate()`
  （void 强制标签更新（））
- `void MarkGeometryAsDirty()`
  （void MarkGeometryAsDirty（））
- `void Rebuild(CanvasUpdate update)`
  （void Rebuild（画布更新 update））
- `void LayoutComplete()`
  （void LayoutComplete（））
- `void GraphicUpdateComplete()`
  （void Graphic更新Complete（））
- `void UpdateGeometry()`
  （void 更新Geometry（））
- `void AssignPositioningIfNeeded()`
  （void AssignPositioningIfNeeded（））
- `void OnFillVBO(Mesh vbo)`
  （void OnFillVBO（网格 vbo））
- `void GenerateCaret(VertexHelper vbo, Vector2 roundingOffset)`
  （void GenerateCaret（Vertex辅助器 vbo, 二维向量 roundingOffset））
- `void CreateCursorVerts()`
  （void 创建CursorVerts（））
- `void GenerateHighlight(VertexHelper vbo, Vector2 roundingOffset)`
  （void GenerateHighlight（Vertex辅助器 vbo, 二维向量 roundingOffset））
- `char Validate(string text, int pos, char ch)`
  （char 验证（string text, int pos, char ch））
- `void ActivateInputField()`
  （void 激活输入Field（））
- `void ActivateInputFieldInternal()`
  （void 激活输入Field内部的（））
- `void OnSelect(BaseEventData eventData)`
  （void On选择（基础事件数据 eventData））
- `void OnPointerClick(PointerEventData eventData)`
  （void On指针Click（指针事件数据 eventData））
- `void DeactivateInputField()`
  （void 停用输入Field（））
- `void OnDeselect(BaseEventData eventData)`
  （void On取消选择（基础事件数据 eventData））
- `void OnSubmit(BaseEventData eventData)`
  （void OnSubmit（基础事件数据 eventData））
- `void EnforceContentType()`
  （void EnforceContent类型（））
- `void EnforceTextHOverflow()`
  （void Enforce文本HOverflow（））
- `void SetToCustomIfContentTypeIsNot(InputField.ContentType[] allowedContentTypes)`
  （void 集合To自定义的IfContent类型是否Not（输入Field.ContentType[] allowedContentTypes））
- `void SetToCustom()`
  （void 集合To自定义的（））
- `void DoStateTransition(Selectable.SelectionState state, bool instant)`
  （void Do状态Transition（Selectable.Selection状态 state, bool instant））
- `void CalculateLayoutInputHorizontal()`
  （void 计算Layout输入水平（））
- `void CalculateLayoutInputVertical()`
  （void 计算Layout输入垂直（））
- `float get_minWidth()`
  （float get_min宽度（））
- `float get_preferredWidth()`
  （float get_preferred宽度（））
- `float get_flexibleWidth()`
  （float get_flexible宽度（））
- `float get_minHeight()`
  （float get_min高度（））
- `float get_preferredHeight()`
  （float get_preferred高度（））
- `float get_flexibleHeight()`
  （float get_flexible高度（））
- `int get_layoutPriority()`
  （int get_layoutPriority（））

---

## InputField.CharacterValidation（输入Field.角色Validation）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## InputField.ContentType（输入Field.Content类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## InputField.EditState（输入Field.Edit状态）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## InputField.InputType（输入Field.输入类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## InputField.LineType（输入Field.Line类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## InputField.OnValidateInput（输入Field.On验证输入）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `char Invoke(string text, int charIndex, char addedChar)`
  （char Invoke（string text, int charIndex, char addedChar））
- `IAsyncResult BeginInvoke(string text, int charIndex, char addedChar, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（string text, int charIndex, char addedChar, 异步回调 callback, object object））
- `char EndInvoke(IAsyncResult result)`
  （char 结束Invoke（I异步Result result））

---

## InputRecord（输入Record）

### 字段 (9)

- `short EventType`（short 事件类型）(偏移: 0x0)
- `bool KeyDown`（bool 键下）(偏移: 0x2)
- `short RepeatCount`（short Repeat数量）(偏移: 0x4)
- `short VirtualKeyCode`（short 虚拟的键Code）(偏移: 0x6)
- `short VirtualScanCode`（short 虚拟的ScanCode）(偏移: 0x8)
- `char Character`（char 角色）(偏移: 0xA)
- `int ControlKeyState`（int 控制键状态）(偏移: 0xC)
- `int pad1`（int pad1）(偏移: 0x10)
- `bool pad2`（bool pad2）(偏移: 0x14)

---

## InputTracking（输入Tracking）

### 字段 (4)

- `Action<XRNodeState> trackingAcquired`（Action<XR节点State> trackingAcquired）(偏移: 0x0)
- `Action<XRNodeState> trackingLost`（Action<XR节点State> trackingLost）(偏移: 0x4)
- `Action<XRNodeState> nodeAdded`（Action<XR节点State> nodeAdded）(偏移: 0x8)
- `Action<XRNodeState> nodeRemoved`（Action<XR节点State> nodeRemoved）(偏移: 0xC)

### 方法 (1)

- `void InvokeTrackingEvent(InputTracking.TrackingStateEventType eventType, XRNode nodeType, long uniqueID, bool tracked)`
  （void InvokeTracking事件（输入Tracking.Tracking状态事件类型 eventType, XR节点 nodeType, long uniqueID, bool tracked））

---

## InputTracking.TrackingStateEventType（输入Tracking.Tracking状态事件类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## InsertionBehavior（InsertionBehavior）

### 字段 (1)

- `byte value__`（byte value__）(偏移: 0x0)

---

## InspectorComment（InspectorComment）

**继承**: PropertyAttribute（属性Attribute）

### 字段 (2)

- `string name`（string name）(偏移: 0x8)
- `string color`（string color）(偏移: 0xC)

---

## InspectorGridMode（Inspector网格模式）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## InspectorNameAttribute（Inspector名称Attribute）

**继承**: PropertyAttribute（属性Attribute）

### 字段 (1)

- `string displayName`（string display名称）(偏移: 0x8)

---

## InstanceDescriptor（实例Descriptor）

### 字段 (3)

- `MemberInfo member`（Member信息 member）(偏移: 0x8)
- `ICollection arguments`（ICollection arguments）(偏移: 0xC)
- `bool isComplete`（bool isComplete）(偏移: 0x10)

### 方法 (1)

- `object Invoke()`
  （object Invoke（））

---

## Int128（Int128）

### 字段 (2)

- `long hi`（long hi）(偏移: 0x0)
- `ulong lo`（ulong lo）(偏移: 0x8)

### 方法 (10)

- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））
- `Int128 Int128Mul(long lhs, long rhs)`
  （Int128 Int128Mul（long lhs, long rhs））
- `bool op_Equality(Int128 val1, Int128 val2)`
  （bool op_Equality（Int128 val1, Int128 val2））
- `bool op_GreaterThan(Int128 val1, Int128 val2)`
  （bool op_GreaterThan（Int128 val1, Int128 val2））
- `bool op_LessThan(Int128 val1, Int128 val2)`
  （bool op_LessThan（Int128 val1, Int128 val2））
- `Int128 op_Addition(Int128 lhs, Int128 rhs)`
  （Int128 op_Addition（Int128 lhs, Int128 rhs））
- `Int128 op_Subtraction(Int128 lhs, Int128 rhs)`
  （Int128 op_Subtraction（Int128 lhs, Int128 rhs））
- `Int128 op_UnaryNegation(Int128 val)`
  （Int128 op_UnaryNegation（Int128 val））
- `Int128 op_Division(Int128 lhs, Int128 rhs)`
  （Int128 op_Division（Int128 lhs, Int128 rhs））

---

## Int16（Int16）

**继承**: IComparable, IFormattable, IConvertible, IComparable<short>, IEquatable<short>（IComparable, IFormattable, IConvertible, IComparable<short>, IEquatable<short>）

### 字段 (1)

- `short m_value`（short m_value）(偏移: 0x0)

### 方法 (14)

- `int CompareTo(object value)`
  （int CompareTo（object value））
- `int CompareTo(short value)`
  （int CompareTo（short value））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `bool Equals(short obj)`
  （bool Equals（short obj））
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
- `string ToString(string format, NumberFormatInfo info)`
  （string To字符串（string format, Number格式化信息 info））
- `short Parse(string s, IFormatProvider provider)`
  （short 解析（string s, I格式化提供者 provider））
- `short Parse(string s, NumberStyles style, IFormatProvider provider)`
  （short 解析（string s, NumberStyles style, I格式化提供者 provider））
- `short Parse(string s, NumberStyles style, NumberFormatInfo info)`
  （short 解析（string s, NumberStyles style, Number格式化信息 info））
- `TypeCode GetTypeCode()`
  （类型Code 获取类型Code（））

---

## Int16ArrayTypeInfo（Int16数组类型信息）

**继承**: TraceLoggingTypeInfo<short[]>（TraceLogging类型Info<short[]>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void WriteMetadata（TraceLoggingMetadataCollector collector, string name, 事件Field格式化 format））
- `void WriteData(TraceLoggingDataCollector collector, ref short[] value)`
  （void Write数据（TraceLogging数据Collector collector, ref short[] value））

---

## Int16Converter（Int16Converter）

**继承**: BaseNumberConverter（基础NumberConverter）

### 方法 (5)

- `Type get_TargetType()`
  （类型 get_目标类型（））
- `object FromString(string value, int radix)`
  （object From字符串（string value, int radix））
- `object FromString(string value, CultureInfo culture)`
  （object From字符串（string value, Culture信息 culture））
- `object FromString(string value, NumberFormatInfo formatInfo)`
  （object From字符串（string value, Number格式化信息 formatInfo））
- `string ToString(object value, NumberFormatInfo formatInfo)`
  （string To字符串（object value, Number格式化信息 formatInfo））

---

## Int16Enum（Int16Enum）

### 字段 (1)

- `short value__`（short value__）(偏移: 0x0)

---

## Int16TypeInfo（Int16类型信息）

**继承**: TraceLoggingTypeInfo<short>（TraceLogging类型Info<short>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void WriteMetadata（TraceLoggingMetadataCollector collector, string name, 事件Field格式化 format））
- `void WriteData(TraceLoggingDataCollector collector, ref short value)`
  （void Write数据（TraceLogging数据Collector collector, ref short value））

---

## Int2（Int2）

**继承**: IEquatable<Int2>（IEquatable<Int2>）

### 字段 (2)

- `int x`（int x）(偏移: 0x0)
- `int y`（int y）(偏移: 0x4)

### 方法 (14)

- `long get_sqrMagnitudeLong()`
  （long get_sqrMagnitudeLong（））
- `Int2 op_Addition(Int2 a, Int2 b)`
  （Int2 op_Addition（Int2 a, Int2 b））
- `Int2 op_Subtraction(Int2 a, Int2 b)`
  （Int2 op_Subtraction（Int2 a, Int2 b））
- `bool op_Equality(Int2 a, Int2 b)`
  （bool op_Equality（Int2 a, Int2 b））
- `bool op_Inequality(Int2 a, Int2 b)`
  （bool op_Inequality（Int2 a, Int2 b））
- `long DotLong(Int2 a, Int2 b)`
  （long DotLong（Int2 a, Int2 b））
- `bool Equals(object o)`
  （bool Equals（object o））
- `bool Equals(Int2 other)`
  （bool Equals（Int2 other））
- `int GetHashCode()`
  （int 获取HashCode（））
- `Int2 Min(Int2 a, Int2 b)`
  （Int2 最小（Int2 a, Int2 b））
- `Int2 Max(Int2 a, Int2 b)`
  （Int2 最大（Int2 a, Int2 b））
- `Int2 FromInt3XZ(Int3 o)`
  （Int2 FromInt3XZ（Int3 o））
- `Int3 ToInt3XZ(Int2 o)`
  （Int3 ToInt3XZ（Int2 o））
- `string ToString()`
  （string To字符串（））

---

## Int3（Int3）

**继承**: IEquatable<Int3>（IEquatable<Int3>）

### 字段 (3)

- `int x`（int x）(偏移: 0x0)
- `int y`（int y）(偏移: 0x4)
- `int z`（int z）(偏移: 0x8)

### 方法 (27)

- `Int3 get_zero()`
  （Int3 get_zero（））
- `bool op_Equality(Int3 lhs, Int3 rhs)`
  （bool op_Equality（Int3 lhs, Int3 rhs））
- `bool op_Inequality(Int3 lhs, Int3 rhs)`
  （bool op_Inequality（Int3 lhs, Int3 rhs））
- `Int3 op_Explicit(Vector3 ob)`
  （Int3 op_Explicit（三维向量 ob））
- `Vector3 op_Explicit(Int3 ob)`
  （三维向量 op_Explicit（Int3 ob））
- `Int3 op_Subtraction(Int3 lhs, Int3 rhs)`
  （Int3 op_Subtraction（Int3 lhs, Int3 rhs））
- `Int3 op_UnaryNegation(Int3 lhs)`
  （Int3 op_UnaryNegation（Int3 lhs））
- `Int3 op_Addition(Int3 lhs, Int3 rhs)`
  （Int3 op_Addition（Int3 lhs, Int3 rhs））
- `Int3 op_Multiply(Int3 lhs, int rhs)`
  （Int3 op_Multiply（Int3 lhs, int rhs））
- `Int3 op_Multiply(Int3 lhs, float rhs)`
  （Int3 op_Multiply（Int3 lhs, float rhs））
- `Int3 op_Multiply(Int3 lhs, double rhs)`
  （Int3 op_Multiply（Int3 lhs, double rhs））
- `Int3 op_Division(Int3 lhs, float rhs)`
  （Int3 op_Division（Int3 lhs, float rhs））
- `int get_Item(int i)`
  （int get_项目（int i））
- `void set_Item(int i, int value)`
  （void set_项目（int i, int value））
- `float Angle(Int3 lhs, Int3 rhs)`
  （float 角度（Int3 lhs, Int3 rhs））
- `int Dot(Int3 lhs, Int3 rhs)`
  （int Dot（Int3 lhs, Int3 rhs））
- `long DotLong(Int3 lhs, Int3 rhs)`
  （long DotLong（Int3 lhs, Int3 rhs））
- `Int3 Normal2D()`
  （Int3 Normal2D（））
- `float get_magnitude()`
  （float get_magnitude（））
- `int get_costMagnitude()`
  （int get_costMagnitude（））
- `float get_sqrMagnitude()`
  （float get_sqrMagnitude（））
- `long get_sqrMagnitudeLong()`
  （long get_sqrMagnitudeLong（））
- `string op_Implicit(Int3 obj)`
  （string op_Implicit（Int3 obj））
- `string ToString()`
  （string To字符串（））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `bool Equals(Int3 other)`
  （bool Equals（Int3 other））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## Int32（Int32）

**继承**: IComparable, IFormattable, IConvertible, IComparable<int>, IEquatable<int>（IComparable, IFormattable, IConvertible, IComparable<int>, IEquatable<int>）

### 字段 (1)

- `int m_value`（int m_value）(偏移: 0x0)

### 方法 (15)

- `int CompareTo(object value)`
  （int CompareTo（object value））
- `int CompareTo(int value)`
  （int CompareTo（int value））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `bool Equals(int obj)`
  （bool Equals（int obj））
- `int GetHashCode()`
  （int 获取HashCode（））
- `string ToString()`
  （string To字符串（））
- `string ToString(string format)`
  （string To字符串（string format））
- `string ToString(IFormatProvider provider)`
  （string To字符串（I格式化提供者 provider））
- `string ToString(string format, IFormatProvider provider)`
  （string To字符串（string format, I格式化提供者 provider））
- `int Parse(string s)`
  （int 解析（string s））
- `int Parse(string s, IFormatProvider provider)`
  （int 解析（string s, I格式化提供者 provider））
- `int Parse(string s, NumberStyles style, IFormatProvider provider)`
  （int 解析（string s, NumberStyles style, I格式化提供者 provider））
- `bool TryParse(string s, out int result)`
  （bool Try解析（string s, out int result））
- `bool TryParse(string s, NumberStyles style, IFormatProvider provider, out int result)`
  （bool Try解析（string s, NumberStyles style, I格式化提供者 provider, out int result））
- `TypeCode GetTypeCode()`
  （类型Code 获取类型Code（））

---

## Int32ArrayTypeInfo（Int32数组类型信息）

**继承**: TraceLoggingTypeInfo<int[]>（TraceLogging类型Info<int[]>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void WriteMetadata（TraceLoggingMetadataCollector collector, string name, 事件Field格式化 format））
- `void WriteData(TraceLoggingDataCollector collector, ref int[] value)`
  （void Write数据（TraceLogging数据Collector collector, ref int[] value））

---

## Int32Converter（Int32Converter）

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

## Int32Enum（Int32Enum）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## Int32TypeInfo（Int32类型信息）

**继承**: TraceLoggingTypeInfo<int>（TraceLogging类型Info<int>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void WriteMetadata（TraceLoggingMetadataCollector collector, string name, 事件Field格式化 format））
- `void WriteData(TraceLoggingDataCollector collector, ref int value)`
  （void Write数据（TraceLogging数据Collector collector, ref int value））

---

## Int3PolygonClipper（Int3PolygonClipper）

### 字段 (2)

- `float[] clipPolygonCache`（float[] clipPolygon缓存）(偏移: 0x0)
- `int[] clipPolygonIntCache`（int[] clipPolygon整数缓存）(偏移: 0x4)

### 方法 (2)

- `void Init()`
  （void 初始化（））
- `int ClipPolygon(Int3[] vIn, int n, Int3[] vOut, int multi, int offset, int axis)`
  （int 弹匣Polygon（Int3[] vIn, int n, Int3[] vOut, int multi, int offset, int axis））

---

## Int64（Int64）

**继承**: IComparable, IFormattable, IConvertible, IComparable<long>, IEquatable<long>（IComparable, IFormattable, IConvertible, IComparable<long>, IEquatable<long>）

### 字段 (1)

- `long m_value`（long m_value）(偏移: 0x0)

### 方法 (15)

- `int CompareTo(object value)`
  （int CompareTo（object value））
- `int CompareTo(long value)`
  （int CompareTo（long value））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `bool Equals(long obj)`
  （bool Equals（long obj））
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
- `long Parse(string s)`
  （long 解析（string s））
- `long Parse(string s, IFormatProvider provider)`
  （long 解析（string s, I格式化提供者 provider））
- `long Parse(string s, NumberStyles style, IFormatProvider provider)`
  （long 解析（string s, NumberStyles style, I格式化提供者 provider））
- `bool TryParse(string s, out long result)`
  （bool Try解析（string s, out long result））
- `bool TryParse(string s, NumberStyles style, IFormatProvider provider, out long result)`
  （bool Try解析（string s, NumberStyles style, I格式化提供者 provider, out long result））
- `TypeCode GetTypeCode()`
  （类型Code 获取类型Code（））

---

## Int64ArrayTypeInfo（Int64数组类型信息）

**继承**: TraceLoggingTypeInfo<long[]>（TraceLogging类型Info<long[]>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void WriteMetadata（TraceLoggingMetadataCollector collector, string name, 事件Field格式化 format））
- `void WriteData(TraceLoggingDataCollector collector, ref long[] value)`
  （void Write数据（TraceLogging数据Collector collector, ref long[] value））

---

## Int64Converter（Int64Converter）

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

## Int64Enum（Int64Enum）

### 字段 (1)

- `long value__`（long value__）(偏移: 0x0)

---

## Int64TypeInfo（Int64类型信息）

**继承**: TraceLoggingTypeInfo<long>（TraceLogging类型Info<long>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void WriteMetadata（TraceLoggingMetadataCollector collector, string name, 事件Field格式化 format））
- `void WriteData(TraceLoggingDataCollector collector, ref long value)`
  （void Write数据（TraceLogging数据Collector collector, ref long value））

---

## IntPlugin（整数插件）

**继承**: ABSTweenPlugin<int, int, NoOptions>（ABSTweenPlugin<int, int, NoOptions>）

### 方法 (8)

- `void Reset(TweenerCore<int, int, NoOptions> t)`
  （void 重置（TweenerCore<int, int, NoOptions> t））
- `void SetFrom(TweenerCore<int, int, NoOptions> t, bool isRelative)`
  （void 集合From（TweenerCore<int, int, NoOptions> t, bool isRelative））
- `void SetFrom(TweenerCore<int, int, NoOptions> t, int fromValue, bool setImmediately, bool isRelative)`
  （void 集合From（TweenerCore<int, int, NoOptions> t, int fromValue, bool setImmediately, bool isRelative））
- `int ConvertToStartValue(TweenerCore<int, int, NoOptions> t, int value)`
  （int 转换To开始值（TweenerCore<int, int, NoOptions> t, int value））
- `void SetRelativeEndValue(TweenerCore<int, int, NoOptions> t)`
  （void 集合Relative结束值（TweenerCore<int, int, NoOptions> t））
- `void SetChangeValue(TweenerCore<int, int, NoOptions> t)`
  （void 集合Change值（TweenerCore<int, int, NoOptions> t））
- `float GetSpeedBasedDuration(NoOptions options, float unitsXSecond, int changeValue)`
  （float 获取SpeedBased持续时间（NoOptions options, float unitsXSecond, int changeValue））
- `void EvaluateAndApply(NoOptions options, Tween t, bool isRelative, DOGetter<int> getter, DOSetter<int> setter, float elapsed, int startValue, int changeValue, float duration, bool usingInversePosition, UpdateNotice updateNotice)`
  （void EvaluateAnd应用（NoOptions options, Tween t, bool isRelative, DOGetter<int> getter, DOSetter<int> setter, float elapsed, int startValue, int changeValue, float duration, bool usingInversePosition, 更新Notice updateNotice））

---

## IntPoint（整数Point）

### 字段 (2)

- `long X`（long X）(偏移: 0x0)
- `long Y`（long Y）(偏移: 0x8)

### 方法 (4)

- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））
- `bool op_Equality(IntPoint a, IntPoint b)`
  （bool op_Equality（整数Point a, 整数Point b））
- `bool op_Inequality(IntPoint a, IntPoint b)`
  （bool op_Inequality（整数Point a, 整数Point b））

---

## IntPtr（整数Ptr）

**继承**: ISerializable（ISerializable）

### 字段 (2)

- `void* m_value`（void* m_value）(偏移: 0x0)
- `IntPtr Zero`（整数Ptr Zero）(偏移: 0x0)

### 方法 (16)

- `int get_Size()`
  （int get_大小（））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））
- `long ToInt64()`
  （long ToInt64（））
- `void* ToPointer()`
  （void* To指针（））
- `string ToString()`
  （string To字符串（））
- `string ToString(string format)`
  （string To字符串（string format））
- `bool op_Equality(IntPtr value1, IntPtr value2)`
  （bool op_Equality（整数Ptr value1, 整数Ptr value2））
- `bool op_Inequality(IntPtr value1, IntPtr value2)`
  （bool op_Inequality（整数Ptr value1, 整数Ptr value2））
- `IntPtr op_Explicit(int value)`
  （整数Ptr op_Explicit（int value））
- `IntPtr op_Explicit(long value)`
  （整数Ptr op_Explicit（long value））
- `IntPtr op_Explicit(void* value)`
  （整数Ptr op_Explicit（void* value））
- `int op_Explicit(IntPtr value)`
  （int op_Explicit（整数Ptr value））
- `long op_Explicit(IntPtr value)`
  （long op_Explicit（整数Ptr value））
- `void* op_Explicit(IntPtr value)`
  （void* op_Explicit（整数Ptr value））
- `bool IsNull()`
  （bool 是否Null（））

---

## IntPtrArrayTypeInfo（整数Ptr数组类型信息）

**继承**: TraceLoggingTypeInfo<IntPtr[]>（TraceLogging类型Info<整数Ptr[]>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void WriteMetadata（TraceLoggingMetadataCollector collector, string name, 事件Field格式化 format））
- `void WriteData(TraceLoggingDataCollector collector, ref IntPtr[] value)`
  （void Write数据（TraceLogging数据Collector collector, ref IntPtr[] value））

---

## IntPtrTypeInfo（整数Ptr类型信息）

**继承**: TraceLoggingTypeInfo<IntPtr>（TraceLogging类型Info<整数Ptr>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void WriteMetadata（TraceLoggingMetadataCollector collector, string name, 事件Field格式化 format））
- `void WriteData(TraceLoggingDataCollector collector, ref IntPtr value)`
  （void Write数据（TraceLogging数据Collector collector, ref IntPtr value））

---

## IntRect（整数Rect）

### 字段 (4)

- `int xmin`（int xmin）(偏移: 0x0)
- `int ymin`（int ymin）(偏移: 0x4)
- `int xmax`（int xmax）(偏移: 0x8)
- `int ymax`（int ymax）(偏移: 0xC)

### 方法 (15)

- `bool Contains(int x, int y)`
  （bool Contains（int x, int y））
- `int get_Width()`
  （int get_宽度（））
- `int get_Height()`
  （int get_高度（））
- `bool IsValid()`
  （bool 是否Valid（））
- `bool op_Equality(IntRect a, IntRect b)`
  （bool op_Equality（整数Rect a, 整数Rect b））
- `bool op_Inequality(IntRect a, IntRect b)`
  （bool op_Inequality（整数Rect a, 整数Rect b））
- `bool Equals(object obj)`
  （bool Equals（object obj））
- `int GetHashCode()`
  （int 获取HashCode（））
- `IntRect Intersection(IntRect a, IntRect b)`
  （整数Rect Intersection（整数Rect a, 整数Rect b））
- `bool Intersects(IntRect a, IntRect b)`
  （bool Intersects（整数Rect a, 整数Rect b））
- `IntRect Union(IntRect a, IntRect b)`
  （整数Rect Union（整数Rect a, 整数Rect b））
- `IntRect ExpandToContain(int x, int y)`
  （整数Rect ExpandToContain（int x, int y））
- `IntRect Expand(int range)`
  （整数Rect Expand（int range））
- `string ToString()`
  （string To字符串（））
- `void DebugDraw(GraphTransform transform, Color color)`
  （void DebugDraw（Graph变换 transform, 颜色 color））

---

## IntSizedArray（整数Sized数组）

**继承**: ICloneable（ICloneable）

### 字段 (2)

- `int[] objects`（int[] objects）(偏移: 0x8)
- `int[] negObjects`（int[] negObjects）(偏移: 0xC)

### 方法 (4)

- `object Clone()`
  （object 克隆（））
- `int get_Item(int index)`
  （int get_项目（int index））
- `void set_Item(int index, int value)`
  （void set_项目（int index, int value））
- `void IncreaseCapacity(int index)`
  （void IncreaseCapacity（int index））

---

## IntegratedSubsystem（IntegratedSubsystem）

**继承**: ISubsystem（ISubsystem）

### 字段 (2)

- `IntPtr m_Ptr`（整数Ptr m_Ptr）(偏移: 0x8)
- `ISubsystemDescriptor m_SubsystemDescriptor`（ISubsystemDescriptor m_SubsystemDescriptor）(偏移: 0xC)

### 方法 (4)

- `void SetHandle(IntegratedSubsystem subsystem)`
  （void 集合句柄（IntegratedSubsystem subsystem））
- `bool get_running()`
  （bool get_running（））
- `bool get_valid()`
  （bool get_valid（））
- `bool IsRunning()`
  （bool 是否Running（））

---

## IntegratedSubsystemDescriptor（IntegratedSubsystemDescriptor）

**继承**: ISubsystemDescriptor（ISubsystemDescriptor）

### 字段 (1)

- `IntPtr m_Ptr`（整数Ptr m_Ptr）(偏移: 0x8)

### 方法 (1)

- `string get_id()`
  （string get_id（））

---

## InteractionEffector（InteractionEffector）

### 字段 (33)

- `Poser poser`（Poser poser）(偏移: 0x14)
- `IKEffector effector`（IKEffector effector）(偏移: 0x18)
- `float timer`（float timer）(偏移: 0x1C)
- `float length`（float length）(偏移: 0x20)
- `float weight`（float weight）(偏移: 0x24)
- `float fadeInSpeed`（float fadeInSpeed）(偏移: 0x28)
- `float defaultPositionWeight`（float defaultPositionWeight）(偏移: 0x2C)
- `float defaultRotationWeight`（float defaultRotationWeight）(偏移: 0x30)
- `float defaultPull`（float defaultPull）(偏移: 0x34)
- `float defaultReach`（float defaultReach）(偏移: 0x38)
- `float defaultPush`（float defaultPush）(偏移: 0x3C)
- `float defaultPushParent`（float defaultPush父级）(偏移: 0x40)
- `float defaultBendGoalWeight`（float defaultBendGoalWeight）(偏移: 0x44)
- `float resetTimer`（float reset计时器）(偏移: 0x48)
- `bool positionWeightUsed`（bool positionWeightUsed）(偏移: 0x4C)
- `bool rotationWeightUsed`（bool rotationWeightUsed）(偏移: 0x4D)
- `bool pullUsed`（bool pullUsed）(偏移: 0x4E)
- `bool reachUsed`（bool reachUsed）(偏移: 0x4F)
- `bool pushUsed`（bool pushUsed）(偏移: 0x50)
- `bool pushParentUsed`（bool push父级Used）(偏移: 0x51)
- `bool bendGoalWeightUsed`（bool bendGoalWeightUsed）(偏移: 0x52)
- `bool pickedUp`（bool picked上）(偏移: 0x53)
- `bool defaults`（bool defaults）(偏移: 0x54)
- `bool pickUpOnPostFBBIK`（bool pick上OnPostFBBIK）(偏移: 0x55)
- `Vector3 pickUpPosition`（三维向量 pick上Position）(偏移: 0x58)
- `Vector3 pausePositionRelative`（三维向量 pausePositionRelative）(偏移: 0x64)
- `Quaternion pickUpRotation`（Quaternion pick上Rotation）(偏移: 0x70)
- `Quaternion pauseRotationRelative`（Quaternion pauseRotationRelative）(偏移: 0x80)
- `InteractionTarget interactionTarget`（Interaction目标 interaction目标）(偏移: 0x90)
- `Transform target`（变换 target）(偏移: 0x94)
- `List<bool> triggered`（List<bool> triggered）(偏移: 0x98)
- `InteractionSystem interactionSystem`（Interaction系统 interaction系统）(偏移: 0x9C)
- `bool started`（bool started）(偏移: 0xA0)

### 方法 (19)

- `FullBodyBipedEffector get_effectorType()`
  （满身体BipedEffector get_effector类型（））
- `void set_effectorType(FullBodyBipedEffector value)`
  （void set_effector类型（满身体BipedEffector value））
- `bool get_isPaused()`
  （bool get_isPaused（））
- `void set_isPaused(bool value)`
  （void set_isPaused（bool value））
- `InteractionObject get_interactionObject()`
  （Interaction对象 get_interaction对象（））
- `void set_interactionObject(InteractionObject value)`
  （void set_interaction对象（Interaction对象 value））
- `bool get_inInteraction()`
  （bool get_inInteraction（））
- `void Initiate(InteractionSystem interactionSystem)`
  （void Initiate（Interaction系统 interactionSystem））
- `void StoreDefaults()`
  （void 商店Defaults（））
- `bool ResetToDefaults(float speed)`
  （bool 重置ToDefaults（float speed））
- `bool Pause()`
  （bool 暂停（））
- `bool Resume()`
  （bool 恢复（））
- `bool Start(InteractionObject interactionObject, string tag, float fadeInTime, bool interrupt)`
  （bool 开始（Interaction对象 interactionObject, string tag, float fadeInTime, bool interrupt））
- `void Update(Transform root, float speed)`
  （void 更新（变换 root, float speed））
- `float get_progress()`
  （float get_progress（））
- `void TriggerUntriggeredEvents(bool checkTime, out bool pickUp, out bool pause)`
  （void 触发器UntriggeredEvents（bool checkTime, out bool pickUp, out bool pause））
- `void PickUp(Transform root)`
  （void Pick上（变换 root））
- `bool Stop()`
  （bool 停止（））
- `void OnPostFBBIK()`
  （void OnPostFBBIK（））

---

## InteractionLookAt（InteractionLookAt）

### 字段 (8)

- `LookAtIK ik`（LookAtIK ik）(偏移: 0x8)
- `float lerpSpeed`（float lerpSpeed）(偏移: 0xC)
- `float weightSpeed`（float weightSpeed）(偏移: 0x10)
- `bool isPaused`（bool isPaused）(偏移: 0x14)
- `Transform lookAtTarget`（变换 lookAt目标）(偏移: 0x18)
- `float stopLookTime`（float stopLook时间）(偏移: 0x1C)
- `float weight`（float weight）(偏移: 0x20)
- `bool firstFBBIKSolve`（bool firstFBBIKSolve）(偏移: 0x24)

### 方法 (5)

- `void Look(Transform target, float time)`
  （void Look（变换 target, float time））
- `void OnFixTransforms()`
  （void OnFixTransforms（））
- `void Update()`
  （void 更新（））
- `void SolveSpine()`
  （void SolveSpine（））
- `void SolveHead()`
  （void Solve头部（））

---

## InteractionObject（Interaction对象）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (7)

- `Transform otherLookAtTarget`（变换 otherLookAt目标）(偏移: 0xC)
- `Transform otherTargetsRoot`（变换 otherTargets根）(偏移: 0x10)
- `Transform positionOffsetSpace`（变换 positionOffsetSpace）(偏移: 0x14)
- `InteractionObject.WeightCurve[] weightCurves`（InteractionObject.WeightCurve[] weightCurves）(偏移: 0x18)
- `InteractionObject.Multiplier[] multipliers`（InteractionObject.Multiplier[] multipliers）(偏移: 0x1C)
- `InteractionObject.InteractionEvent[] events`（InteractionObject.InteractionEvent[] events）(偏移: 0x20)
- `InteractionTarget[] targets`（InteractionTarget[] targets）(偏移: 0x2C)

### 方法 (27)

- `void OpenUserManual()`
  （void 打开User手动（））
- `void OpenScriptReference()`
  （void 打开Script引用（））
- `void OpenTutorial1()`
  （void 打开Tutorial1（））
- `void OpenTutorial2()`
  （void 打开Tutorial2（））
- `void OpenTutorial3()`
  （void 打开Tutorial3（））
- `void OpenTutorial4()`
  （void 打开Tutorial4（））
- `void SupportGroup()`
  （void Support组（））
- `void ASThread()`
  （void ASThread（））
- `float get_length()`
  （float get_length（））
- `void set_length(float value)`
  （void set_length（float value））
- `InteractionSystem get_lastUsedInteractionSystem()`
  （Interaction系统 get_lastUsedInteraction系统（））
- `void set_lastUsedInteractionSystem(InteractionSystem value)`
  （void set_lastUsedInteraction系统（Interaction系统 value））
- `void Initiate()`
  （void Initiate（））
- `Transform get_lookAtTarget()`
  （变换 get_lookAt目标（））
- `InteractionTarget GetTarget(FullBodyBipedEffector effectorType, InteractionSystem interactionSystem)`
  （Interaction目标 获取目标（满身体BipedEffector effectorType, Interaction系统 interactionSystem））
- `bool CurveUsed(InteractionObject.WeightCurve.Type type)`
  （bool CurveUsed（InteractionObject.WeightCurve.类型 type））
- `InteractionTarget[] GetTargets()`
  （InteractionTarget[] 获取Targets（））
- `Transform GetTarget(FullBodyBipedEffector effectorType, string tag)`
  （变换 获取目标（满身体BipedEffector effectorType, string tag））
- `void OnStartInteraction(InteractionSystem interactionSystem)`
  （void On开始Interaction（Interaction系统 interactionSystem））
- `void Apply(IKSolverFullBodyBiped solver, FullBodyBipedEffector effector, InteractionTarget target, float timer, float weight)`
  （void 应用（IKSolver满身体Biped solver, 满身体BipedEffector effector, Interaction目标 target, float timer, float weight））
- `float GetValue(InteractionObject.WeightCurve.Type weightCurveType, InteractionTarget target, float timer)`
  （float 获取值（InteractionObject.WeightCurve.类型 weightCurveType, Interaction目标 target, float timer））
- `Transform get_targetsRoot()`
  （变换 get_targets根（））
- `void Start()`
  （void 开始（））
- `void Apply(IKSolverFullBodyBiped solver, FullBodyBipedEffector effector, InteractionObject.WeightCurve.Type type, float value, float weight)`
  （void 应用（IKSolver满身体Biped solver, 满身体BipedEffector effector, InteractionObject.WeightCurve.类型 type, float value, float weight））
- `Transform GetTarget(FullBodyBipedEffector effectorType)`
  （变换 获取目标（满身体BipedEffector effectorType））
- `int GetWeightCurveIndex(InteractionObject.WeightCurve.Type weightCurveType)`
  （int 获取WeightCurve索引（InteractionObject.WeightCurve.类型 weightCurveType））
- `int GetMultiplierIndex(InteractionObject.WeightCurve.Type weightCurveType)`
  （int 获取Multiplier索引（InteractionObject.WeightCurve.类型 weightCurveType））

---

## InteractionObject.AnimatorEvent（InteractionObject.动画器事件）

### 字段 (6)

- `Animator animator`（动画器 animator）(偏移: 0x8)
- `Animation animation`（动画 animation）(偏移: 0xC)
- `string animationState`（string animation状态）(偏移: 0x10)
- `float crossfadeTime`（float crossfade时间）(偏移: 0x14)
- `int layer`（int layer）(偏移: 0x18)
- `bool resetNormalizedTime`（bool resetNormalized时间）(偏移: 0x1C)

### 方法 (3)

- `void Activate(bool pickUp)`
  （void 激活（bool pickUp））
- `void Activate(Animator animator)`
  （void 激活（动画器 animator））
- `void Activate(Animation animation)`
  （void 激活（动画 animation））

---

## InteractionObject.InteractionEvent（InteractionObject.Interaction事件）

### 字段 (6)

- `float time`（float time）(偏移: 0x8)
- `bool pause`（bool pause）(偏移: 0xC)
- `bool pickUp`（bool pick上）(偏移: 0xD)
- `InteractionObject.AnimatorEvent[] animations`（InteractionObject.动画器Event[] animations）(偏移: 0x10)
- `InteractionObject.Message[] messages`（InteractionObject.Message[] messages）(偏移: 0x14)
- `UnityEvent unityEvent`（Unity引擎事件 unity事件）(偏移: 0x18)

### 方法 (1)

- `void Activate(Transform t)`
  （void 激活（变换 t））

---

## InteractionObject.Message（InteractionObject.Message）

### 字段 (2)

- `string function`（string function）(偏移: 0x8)
- `GameObject recipient`（游戏对象 recipient）(偏移: 0xC)

### 方法 (1)

- `void Send(Transform t)`
  （void 发送（变换 t））

---

## InteractionObject.Multiplier（InteractionObject.Multiplier）

### 字段 (3)

- `InteractionObject.WeightCurve.Type curve`（InteractionObject.WeightCurve.类型 curve）(偏移: 0x8)
- `float multiplier`（float multiplier）(偏移: 0xC)
- `InteractionObject.WeightCurve.Type result`（InteractionObject.WeightCurve.类型 result）(偏移: 0x10)

### 方法 (1)

- `float GetValue(InteractionObject.WeightCurve weightCurve, float timer)`
  （float 获取值（InteractionObject.WeightCurve weightCurve, float timer））

---

## InteractionObject.WeightCurve（InteractionObject.WeightCurve）

### 字段 (2)

- `InteractionObject.WeightCurve.Type type`（InteractionObject.WeightCurve.类型 type）(偏移: 0x8)
- `AnimationCurve curve`（动画Curve curve）(偏移: 0xC)

### 方法 (1)

- `float GetValue(float timer)`
  （float 获取值（float timer））

---

## InteractionObject.WeightCurve.Type（InteractionObject.WeightCurve.类型）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## InteractionSystem（Interaction系统）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (23)

- `string targetTag`（string target标签）(偏移: 0xC)
- `float fadeInTime`（float fadeIn时间）(偏移: 0x10)
- `float speed`（float speed）(偏移: 0x14)
- `float resetToDefaultsSpeed`（float resetToDefaultsSpeed）(偏移: 0x18)
- `Collider characterCollider`（碰撞器 character碰撞器）(偏移: 0x1C)
- `Transform FPSCamera`（变换 FPS摄像机）(偏移: 0x20)
- `LayerMask camRaycastLayers`（层掩码 camRaycastLayers）(偏移: 0x24)
- `float camRaycastDistance`（float camRaycast距离）(偏移: 0x28)
- `List<InteractionTrigger> inContact`（List<InteractionTrigger> inContact）(偏移: 0x30)
- `List<int> bestRangeIndexes`（List<int> best范围Indexes）(偏移: 0x34)
- `InteractionSystem.InteractionDelegate OnInteractionStart`（InteractionSystem.Interaction委托 OnInteraction开始）(偏移: 0x38)
- `InteractionSystem.InteractionDelegate OnInteractionPause`（InteractionSystem.Interaction委托 OnInteraction暂停）(偏移: 0x3C)
- `InteractionSystem.InteractionDelegate OnInteractionPickUp`（InteractionSystem.Interaction委托 OnInteractionPick上）(偏移: 0x40)
- `InteractionSystem.InteractionDelegate OnInteractionResume`（InteractionSystem.Interaction委托 OnInteraction恢复）(偏移: 0x44)
- `InteractionSystem.InteractionDelegate OnInteractionStop`（InteractionSystem.Interaction委托 OnInteraction停止）(偏移: 0x48)
- `InteractionSystem.InteractionEventDelegate OnInteractionEvent`（InteractionSystem.Interaction事件委托 OnInteraction事件）(偏移: 0x4C)
- `RaycastHit raycastHit`（Raycast命中 raycast命中）(偏移: 0x50)
- `FullBodyBipedIK fullBody`（满身体BipedIK full身体）(偏移: 0x7C)
- `InteractionLookAt lookAt`（InteractionLookAt lookAt）(偏移: 0x80)
- `InteractionEffector[] interactionEffectors`（InteractionEffector[] interactionEffectors）(偏移: 0x84)
- `bool initiated`（bool initiated）(偏移: 0x88)
- `Collider lastCollider`（碰撞器 last碰撞器）(偏移: 0x8C)
- `Collider c`（碰撞器 c）(偏移: 0x90)

### 方法 (57)

- `void OpenUserManual()`
  （void 打开User手动（））
- `void OpenScriptReference()`
  （void 打开Script引用（））
- `void OpenTutorial1()`
  （void 打开Tutorial1（））
- `void OpenTutorial2()`
  （void 打开Tutorial2（））
- `void OpenTutorial3()`
  （void 打开Tutorial3（））
- `void OpenTutorial4()`
  （void 打开Tutorial4（））
- `void SupportGroup()`
  （void Support组（））
- `void ASThread()`
  （void ASThread（））
- `bool get_inInteraction()`
  （bool get_inInteraction（））
- `bool IsInInteraction(FullBodyBipedEffector effectorType)`
  （bool 是否InInteraction（满身体BipedEffector effectorType））
- `bool IsPaused(FullBodyBipedEffector effectorType)`
  （bool 是否Paused（满身体BipedEffector effectorType））
- `bool IsPaused()`
  （bool 是否Paused（））
- `bool IsInSync()`
  （bool 是否In同步（））
- `bool StartInteraction(FullBodyBipedEffector effectorType, InteractionObject interactionObject, bool interrupt)`
  （bool 开始Interaction（满身体BipedEffector effectorType, Interaction对象 interactionObject, bool interrupt））
- `bool PauseInteraction(FullBodyBipedEffector effectorType)`
  （bool 暂停Interaction（满身体BipedEffector effectorType））
- `bool ResumeInteraction(FullBodyBipedEffector effectorType)`
  （bool 恢复Interaction（满身体BipedEffector effectorType））
- `bool StopInteraction(FullBodyBipedEffector effectorType)`
  （bool 停止Interaction（满身体BipedEffector effectorType））
- `void PauseAll()`
  （void 暂停所有（））
- `void ResumeAll()`
  （void 恢复所有（））
- `void StopAll()`
  （void 停止所有（））
- `InteractionObject GetInteractionObject(FullBodyBipedEffector effectorType)`
  （Interaction对象 获取Interaction对象（满身体BipedEffector effectorType））
- `float GetProgress(FullBodyBipedEffector effectorType)`
  （float 获取Progress（满身体BipedEffector effectorType））
- `float GetMinActiveProgress()`
  （float 获取最小激活的Progress（））
- `bool TriggerInteraction(int index, bool interrupt)`
  （bool 触发器Interaction（int index, bool interrupt））
- `bool TriggerInteraction(int index, bool interrupt, out InteractionObject interactionObject)`
  （bool 触发器Interaction（int index, bool interrupt, out InteractionObject interactionObject））
- `bool TriggerInteraction(int index, bool interrupt, out InteractionTarget interactionTarget)`
  （bool 触发器Interaction（int index, bool interrupt, out InteractionTarget interactionTarget））
- `InteractionTrigger.Range GetClosestInteractionRange()`
  （InteractionTrigger.范围 获取ClosestInteraction范围（））
- `InteractionObject GetClosestInteractionObjectInRange()`
  （Interaction对象 获取ClosestInteraction对象In范围（））
- `InteractionTarget GetClosestInteractionTargetInRange()`
  （Interaction目标 获取ClosestInteraction目标In范围（））
- `InteractionObject[] GetClosestInteractionObjectsInRange()`
  （InteractionObject[] 获取ClosestInteractionObjectsIn范围（））
- `InteractionTarget[] GetClosestInteractionTargetsInRange()`
  （InteractionTarget[] 获取ClosestInteractionTargetsIn范围（））
- `bool TriggerEffectorsReady(int index)`
  （bool 触发器EffectorsReady（int index））
- `InteractionTrigger.Range GetTriggerRange(int index)`
  （InteractionTrigger.范围 获取触发器范围（int index））
- `int GetClosestTriggerIndex()`
  （int 获取Closest触发器索引（））
- `FullBodyBipedIK get_ik()`
  （满身体BipedIK get_ik（））
- `void set_ik(FullBodyBipedIK value)`
  （void set_ik（满身体BipedIK value））
- `List<InteractionTrigger> get_triggersInRange()`
  （List<InteractionTrigger> get_triggersIn范围（））
- `void set_triggersInRange(List<InteractionTrigger> value)`
  （void set_triggersIn范围（List<InteractionTrigger> value））
- `void Start()`
  （void 开始（））
- `void InteractionPause(FullBodyBipedEffector effector, InteractionObject interactionObject)`
  （void Interaction暂停（满身体BipedEffector effector, Interaction对象 interactionObject））
- `void InteractionResume(FullBodyBipedEffector effector, InteractionObject interactionObject)`
  （void Interaction恢复（满身体BipedEffector effector, Interaction对象 interactionObject））
- `void InteractionStop(FullBodyBipedEffector effector, InteractionObject interactionObject)`
  （void Interaction停止（满身体BipedEffector effector, Interaction对象 interactionObject））
- `void LookAtInteraction(FullBodyBipedEffector effector, InteractionObject interactionObject)`
  （void LookAtInteraction（满身体BipedEffector effector, Interaction对象 interactionObject））
- `void OnTriggerEnter(Collider c)`
  （void On触发器Enter（碰撞器 c））
- `void OnTriggerExit(Collider c)`
  （void On触发器Exit（碰撞器 c））
- `bool ContactIsInRange(int index, out int bestRangeIndex)`
  （bool Contact是否In范围（int index, out int bestRangeIndex））
- `void OnDrawGizmosSelected()`
  （void OnDrawGizmos选中的（））
- `void Update()`
  （void 更新（））
- `void Raycasting()`
  （void Raycasting（））
- `void UpdateTriggerEventBroadcasting()`
  （void 更新触发器事件Broadcasting（））
- `void UpdateEffectors()`
  （void 更新Effectors（））
- `void OnPreFBBIK()`
  （void OnPreFBBIK（））
- `void OnPostFBBIK()`
  （void OnPostFBBIK（））
- `void OnFixTransforms()`
  （void OnFixTransforms（））
- `void OnDestroy()`
  （void On销毁（））
- `bool IsValid(bool log)`
  （bool 是否Valid（bool log））
- `bool TriggerIndexIsValid(int index)`
  （bool 触发器索引是否Valid（int index））

---

## InteractionSystem.InteractionDelegate（InteractionSystem.Interaction委托）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(FullBodyBipedEffector effectorType, InteractionObject interactionObject)`
  （void Invoke（满身体BipedEffector effectorType, Interaction对象 interactionObject））
- `IAsyncResult BeginInvoke(FullBodyBipedEffector effectorType, InteractionObject interactionObject, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（满身体BipedEffector effectorType, Interaction对象 interactionObject, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## InteractionSystem.InteractionEventDelegate（InteractionSystem.Interaction事件委托）

**继承**: MulticastDelegate（Multicast委托）

### 方法 (3)

- `void Invoke(FullBodyBipedEffector effectorType, InteractionObject interactionObject, InteractionObject.InteractionEvent interactionEvent)`
  （void Invoke（满身体BipedEffector effectorType, Interaction对象 interactionObject, InteractionObject.Interaction事件 interactionEvent））
- `IAsyncResult BeginInvoke(FullBodyBipedEffector effectorType, InteractionObject interactionObject, InteractionObject.InteractionEvent interactionEvent, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（满身体BipedEffector effectorType, Interaction对象 interactionObject, InteractionObject.Interaction事件 interactionEvent, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束Invoke（I异步Result result））

---

## InteractionTarget（Interaction目标）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (10)

- `FullBodyBipedEffector effectorType`（满身体BipedEffector effector类型）(偏移: 0xC)
- `InteractionTarget.Multiplier[] multipliers`（InteractionTarget.Multiplier[] multipliers）(偏移: 0x10)
- `float interactionSpeedMlp`（float interactionSpeedMlp）(偏移: 0x14)
- `Transform pivot`（变换 pivot）(偏移: 0x18)
- `Vector3 twistAxis`（三维向量 twist轴）(偏移: 0x1C)
- `float twistWeight`（float twistWeight）(偏移: 0x28)
- `float swingWeight`（float swingWeight）(偏移: 0x2C)
- `bool rotateOnce`（bool rotateOnce）(偏移: 0x30)
- `Quaternion defaultLocalRotation`（Quaternion default本地的Rotation）(偏移: 0x34)
- `Transform lastPivot`（变换 lastPivot）(偏移: 0x44)

### 方法 (11)

- `void OpenUserManual()`
  （void 打开User手动（））
- `void OpenScriptReference()`
  （void 打开Script引用（））
- `void OpenTutorial1()`
  （void 打开Tutorial1（））
- `void OpenTutorial2()`
  （void 打开Tutorial2（））
- `void OpenTutorial3()`
  （void 打开Tutorial3（））
- `void OpenTutorial4()`
  （void 打开Tutorial4（））
- `void SupportGroup()`
  （void Support组（））
- `void ASThread()`
  （void ASThread（））
- `float GetValue(InteractionObject.WeightCurve.Type curveType)`
  （float 获取值（InteractionObject.WeightCurve.类型 curveType））
- `void ResetRotation()`
  （void 重置Rotation（））
- `void RotateTo(Vector3 position)`
  （void RotateTo（三维向量 position））

---

## InteractionTarget.Multiplier（InteractionTarget.Multiplier）

### 字段 (2)

- `InteractionObject.WeightCurve.Type curve`（InteractionObject.WeightCurve.类型 curve）(偏移: 0x8)
- `float multiplier`（float multiplier）(偏移: 0xC)

---

## InteractionTrigger（Interaction触发器）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (1)

- `InteractionTrigger.Range[] ranges`（InteractionTrigger.Range[] ranges）(偏移: 0xC)

### 方法 (7)

- `void OpenUserManual()`
  （void 打开User手动（））
- `void OpenScriptReference()`
  （void 打开Script引用（））
- `void OpenTutorial4()`
  （void 打开Tutorial4（））
- `void SupportGroup()`
  （void Support组（））
- `void ASThread()`
  （void ASThread（））
- `void Start()`
  （void 开始（））
- `int GetBestRangeIndex(Transform character, Transform raycastFrom, RaycastHit raycastHit)`
  （int 获取Best范围索引（变换 character, 变换 raycastFrom, Raycast命中 raycastHit））

---

## InteractionTrigger.CameraPosition（InteractionTrigger.摄像机Position）

### 字段 (5)

- `Collider lookAtTarget`（碰撞器 lookAt目标）(偏移: 0x8)
- `Vector3 direction`（三维向量 direction）(偏移: 0xC)
- `float maxDistance`（float max距离）(偏移: 0x18)
- `float maxAngle`（float max角度）(偏移: 0x1C)
- `bool fixYAxis`（bool fixY轴）(偏移: 0x20)

### 方法 (2)

- `Quaternion GetRotation()`
  （Quaternion 获取Rotation（））
- `bool IsInRange(Transform raycastFrom, RaycastHit hit, Transform trigger, out float error)`
  （bool 是否In范围（变换 raycastFrom, Raycast命中 hit, 变换 trigger, out float error））

---

## InteractionTrigger.CharacterPosition（InteractionTrigger.角色Position）

### 字段 (7)

- `bool use`（bool use）(偏移: 0x8)
- `Vector2 offset`（二维向量 offset）(偏移: 0xC)
- `float angleOffset`（float angleOffset）(偏移: 0x14)
- `float maxAngle`（float max角度）(偏移: 0x18)
- `float radius`（float radius）(偏移: 0x1C)
- `bool orbit`（bool orbit）(偏移: 0x20)
- `bool fixYAxis`（bool fixY轴）(偏移: 0x21)

### 方法 (3)

- `Vector3 get_offset3D()`
  （三维向量 get_offset3D（））
- `Vector3 get_direction3D()`
  （三维向量 get_direction3D（））
- `bool IsInRange(Transform character, Transform trigger, out float error)`
  （bool 是否In范围（变换 character, 变换 trigger, out float error））

---

## InteractionTrigger.Range（InteractionTrigger.范围）

### 字段 (5)

- `string name`（string name）(偏移: 0x8)
- `bool show`（bool show）(偏移: 0xC)
- `InteractionTrigger.CharacterPosition characterPosition`（InteractionTrigger.角色Position characterPosition）(偏移: 0x10)
- `InteractionTrigger.CameraPosition cameraPosition`（InteractionTrigger.摄像机Position cameraPosition）(偏移: 0x14)
- `InteractionTrigger.Range.Interaction[] interactions`（InteractionTrigger.Range.Interaction[] interactions）(偏移: 0x18)

### 方法 (1)

- `bool IsInRange(Transform character, Transform raycastFrom, RaycastHit raycastHit, Transform trigger, out float maxError)`
  （bool 是否In范围（变换 character, 变换 raycastFrom, Raycast命中 raycastHit, 变换 trigger, out float maxError））

---

## InteractionTrigger.Range.Interaction（InteractionTrigger.Range.Interaction）

### 字段 (2)

- `InteractionObject interactionObject`（Interaction对象 interaction对象）(偏移: 0x8)
- `FullBodyBipedEffector[] effectors`（满身体BipedEffector[] effectors）(偏移: 0xC)

---

## InterfaceTypeAttribute（Interface类型Attribute）

**继承**: Attribute（Attribute）

### 字段 (1)

- `ComInterfaceType _val`（ComInterface类型 _val）(偏移: 0x8)

---

## Interlocked（Interlocked）

### 方法 (18)

- `int CompareExchange(ref int location1, int value, int comparand)`
  （int CompareExchange（ref int location1, int value, int comparand））
- `int CompareExchange(ref int location1, int value, int comparand, ref bool succeeded)`
  （int CompareExchange（ref int location1, int value, int comparand, ref bool succeeded））
- `object CompareExchange(ref object location1, object value, object comparand)`
  （object CompareExchange（ref object location1, object value, object comparand））
- `float CompareExchange(ref float location1, float value, float comparand)`
  （float CompareExchange（ref float location1, float value, float comparand））
- `int Decrement(ref int location)`
  （int Decrement（ref int location））
- `int Increment(ref int location)`
  （int Increment（ref int location））
- `long Increment(ref long location)`
  （long Increment（ref long location））
- `int Exchange(ref int location1, int value)`
  （int Exchange（ref int location1, int value））
- `object Exchange(ref object location1, object value)`
  （object Exchange（ref object location1, object value））
- `float Exchange(ref float location1, float value)`
  （float Exchange（ref float location1, float value））
- `long CompareExchange(ref long location1, long value, long comparand)`
  （long CompareExchange（ref long location1, long value, long comparand））
- `IntPtr CompareExchange(ref IntPtr location1, IntPtr value, IntPtr comparand)`
  （整数Ptr CompareExchange（ref IntPtr location1, 整数Ptr value, 整数Ptr comparand））
- `double CompareExchange(ref double location1, double value, double comparand)`
  （double CompareExchange（ref double location1, double value, double comparand））
- `long Exchange(ref long location1, long value)`
  （long Exchange（ref long location1, long value））
- `IntPtr Exchange(ref IntPtr location1, IntPtr value)`
  （整数Ptr Exchange（ref IntPtr location1, 整数Ptr value））
- `double Exchange(ref double location1, double value)`
  （double Exchange（ref double location1, double value））
- `long Read(ref long location)`
  （long Read（ref long location））
- `int Add(ref int location1, int value)`
  （int 添加（ref int location1, int value））

---

## InternalArrayTypeE（内部的数组类型E）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## InternalCodePageDataItem（内部的CodePage数据项目）

### 字段 (4)

- `ushort codePage`（ushort codePage）(偏移: 0x0)
- `ushort uiFamilyCodePage`（ushort uiFamilyCodePage）(偏移: 0x2)
- `uint flags`（uint flags）(偏移: 0x4)
- `string Names`（string Names）(偏移: 0x8)

---

## InternalConstants（内部的Constants）

### 字段 (10)

- `int MAX_BITS`（int MAX_BITS）(偏移: 0x0)
- `int BL_CODES`（int BL_CODES）(偏移: 0x4)
- `int D_CODES`（int D_CODES）(偏移: 0x8)
- `int LITERALS`（int LITERALS）(偏移: 0xC)
- `int LENGTH_CODES`（int LENGTH_CODES）(偏移: 0x10)
- `int L_CODES`（int L_CODES）(偏移: 0x14)
- `int MAX_BL_BITS`（int MAX_BL_BITS）(偏移: 0x18)
- `int REP_3_6`（int REP_3_6）(偏移: 0x1C)
- `int REPZ_3_10`（int REPZ_3_10）(偏移: 0x20)
- `int REPZ_11_138`（int REPZ_11_138）(偏移: 0x24)

---

## InternalDecoderBestFitFallback（内部的DecoderBestFitFallback）

**继承**: DecoderFallback（DecoderFallback）

### 字段 (3)

- `Encoding encoding`（Encoding encoding）(偏移: 0xC)
- `char[] arrayBestFit`（char[] arrayBestFit）(偏移: 0x10)
- `char cReplacement`（char cReplacement）(偏移: 0x14)

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

## InternalDecoderBestFitFallbackBuffer（内部的DecoderBestFitFallback缓冲区）

**继承**: DecoderFallbackBuffer（DecoderFallback缓冲区）

### 字段 (5)

- `char cBestFit`（char cBestFit）(偏移: 0x10)
- `int iCount`（int i数量）(偏移: 0x14)
- `int iSize`（int i大小）(偏移: 0x18)
- `InternalDecoderBestFitFallback oFallback`（内部的DecoderBestFitFallback oFallback）(偏移: 0x1C)
- `object s_InternalSyncObject`（object s_内部的同步对象）(偏移: 0x0)

### 方法 (6)

- `object get_InternalSyncObject()`
  （object get_内部的同步对象（））
- `bool Fallback(byte[] bytesUnknown, int index)`
  （bool Fallback（byte[] bytesUnknown, int index））
- `char GetNextChar()`
  （char 获取下一个Char（））
- `void Reset()`
  （void 重置（））
- `int InternalFallback(byte[] bytes, byte* pBytes)`
  （int 内部的Fallback（byte[] bytes, byte* pBytes））
- `char TryBestFit(byte[] bytesCheck)`
  （char TryBestFit（byte[] bytesCheck））

---

## InternalEncoderBestFitFallback（内部的EncoderBestFitFallback）

**继承**: EncoderFallback（EncoderFallback）

### 字段 (2)

- `Encoding encoding`（Encoding encoding）(偏移: 0xC)
- `char[] arrayBestFit`（char[] arrayBestFit）(偏移: 0x10)

### 方法 (4)

- `EncoderFallbackBuffer CreateFallbackBuffer()`
  （EncoderFallback缓冲区 创建Fallback缓冲区（））
- `int get_MaxCharCount()`
  （int get_最大Char数量（））
- `bool Equals(object value)`
  （bool Equals（object value））
- `int GetHashCode()`
  （int 获取HashCode（））

---

## InternalEncoderBestFitFallbackBuffer（内部的EncoderBestFitFallback缓冲区）

**继承**: EncoderFallbackBuffer（EncoderFallback缓冲区）

### 字段 (5)

- `char cBestFit`（char cBestFit）(偏移: 0x1C)
- `InternalEncoderBestFitFallback oFallback`（内部的EncoderBestFitFallback oFallback）(偏移: 0x20)
- `int iCount`（int i数量）(偏移: 0x24)
- `int iSize`（int i大小）(偏移: 0x28)
- `object s_InternalSyncObject`（object s_内部的同步对象）(偏移: 0x0)

### 方法 (8)

- `object get_InternalSyncObject()`
  （object get_内部的同步对象（））
- `bool Fallback(char charUnknown, int index)`
  （bool Fallback（char charUnknown, int index））
- `bool Fallback(char charUnknownHigh, char charUnknownLow, int index)`
  （bool Fallback（char charUnknownHigh, char charUnknownLow, int index））
- `char GetNextChar()`
  （char 获取下一个Char（））
- `bool MovePrevious()`
  （bool 移动上一个（））
- `int get_Remaining()`
  （int get_Remaining（））
- `void Reset()`
  （void 重置（））
- `char TryBestFit(char cUnknown)`
  （char TryBestFit（char cUnknown））

---

## InternalEncodingDataItem（内部的Encoding数据项目）

### 字段 (2)

- `string webName`（string web名称）(偏移: 0x0)
- `ushort codePage`（ushort codePage）(偏移: 0x4)

---

## InternalFE（内部的FE）

### 字段 (4)

- `FormatterTypeStyle FEtypeFormat`（Formatter类型Style FEtype格式化）(偏移: 0x8)
- `FormatterAssemblyStyle FEassemblyFormat`（FormatterAssemblyStyle FEassembly格式化）(偏移: 0xC)
- `TypeFilterLevel FEsecurityLevel`（类型Filter等级 FEsecurity等级）(偏移: 0x10)
- `InternalSerializerTypeE FEserializerTypeEnum`（内部的Serializer类型E FEserializer类型Enum）(偏移: 0x14)

---

## InternalInflateConstants（内部的InflateConstants）

### 字段 (1)

- `int[] InflateMask`（int[] Inflate掩码）(偏移: 0x30DA30BB)

---

## InternalMemberTypeE（内部的Member类型E）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## InternalMemberValueE（内部的Member值E）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## InternalObjectPositionE（内部的对象PositionE）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## InternalObjectTypeE（内部的对象类型E）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## InternalParseTypeE（内部的解析类型E）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## InternalPrimitiveTypeE（内部的Primitive类型E）

### 字段 (1)

- `int value__`（int value__）(偏移: 0x0)

---

## InternalRemotingServices（内部的RemotingServices）

### 字段 (1)

- `Hashtable _soapAttributes`（Hashtable _soapAttributes）(偏移: 0x0)

### 方法 (1)

- `SoapAttribute GetCachedSoapAttribute(object reflectionObject)`
  （SoapAttribute 获取CachedSoapAttribute（object reflectionObject））

---

