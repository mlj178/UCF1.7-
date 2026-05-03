# 游戏类定义 (Part 2/21)

共 200 个类 (总序号 201 - 400)

---

## AsyncReadManagerMetricsFilters（异步Read管理器MetricsFilters）

### 字段 (5)

- `ulong[] TypeIDs`（ulong[] 类型IDs）(偏移: 0x8)
- `ProcessingState[] States`（ProcessingState[] States）(偏移: 0xC)
- `FileReadType[] ReadTypes`（文件ReadType[] ReadTypes）(偏移: 0x10)
- `Priority[] PriorityLevels`（Priority[] PriorityLevels）(偏移: 0x14)
- `AssetLoadingSubsystem[] Subsystems`（资产LoadingSubsystem[] Subsystems）(偏移: 0x18)

---

## AsyncRequest（异步请求）

### 字段 (2)

- `IMessageSink ReplySink`（IMessageSink ReplySink）(偏移: 0x8)
- `IMessage MsgRequest`（IMessage Msg请求）(偏移: 0xC)

---

## AsyncResult（异步Result）

**继承**: IAsyncResult, IMessageSink, IThreadPoolWorkItem（I异步Result, IMessageSink, IThread池Work项目）

### 字段 (17)

- `object async_state`（object async_state）(偏移: 0x8)
- `WaitHandle handle`（Wait句柄 handle）(偏移: 0xC)
- `object async_delegate`（object async_delegate）(偏移: 0x10)
- `IntPtr data`（整数Ptr data）(偏移: 0x14)
- `object object_data`（object object_data）(偏移: 0x18)
- `bool sync_completed`（bool sync_completed）(偏移: 0x1C)
- `bool completed`（bool completed）(偏移: 0x1D)
- `bool endinvoke_called`（bool endinvoke_called）(偏移: 0x1E)
- `object async_callback`（object async_callback）(偏移: 0x20)
- `ExecutionContext current`（ExecutionContext current）(偏移: 0x24)
- `ExecutionContext original`（ExecutionContext original）(偏移: 0x28)
- `long add_time`（long add_time）(偏移: 0x30)
- `MonoMethodMessage call_message`（MonoMethodMessage call_message）(偏移: 0x38)
- `IMessageCtrl message_ctrl`（IMessageCtrl message_ctrl）(偏移: 0x3C)
- `IMessage reply_message`（IMessage reply_message）(偏移: 0x40)
- `WaitCallback orig_cb`（Wait回调 orig_cb）(偏移: 0x44)
- `ContextCallback ccb`（Context回调 ccb）(偏移: 0x0)

### 方法 (18)

- `void WaitCallback_Context(object state)`
  （void WaitCallback_Context（object state））
- `object get_AsyncState()`
  （object get_异步状态（））
- `WaitHandle get_AsyncWaitHandle()`
  （Wait句柄 get_异步Wait句柄（））
- `bool get_CompletedSynchronously()`
  （bool get_CompletedSynchronously（））
- `bool get_IsCompleted()`
  （布尔值 获取_是否完成（））
- `bool get_EndInvokeCalled()`
  （bool get_结束InvokeCalled（））
- `void set_EndInvokeCalled(bool value)`
  （void set_结束InvokeCalled（bool value））
- `object get_AsyncDelegate()`
  （object get_异步委托（））
- `IMessageSink get_NextSink()`
  （IMessageSink get_下一个Sink（））
- `IMessageCtrl AsyncProcessMessage(IMessage msg, IMessageSink replySink)`
  （IMessageCtrl 异步处理消息（IMessage msg, IMessageSink replySink））
- `IMessage GetReplyMessage()`
  （IMessage 获取ReplyMessage（））
- `void SetMessageCtrl(IMessageCtrl mc)`
  （void 集合MessageCtrl（IMessageCtrl mc））
- `void SetCompletedSynchronously(bool completed)`
  （void 集合CompletedSynchronously（bool completed））
- `IMessage EndInvoke()`
  （IMessage 结束Invoke（））
- `IMessage SyncProcessMessage(IMessage msg)`
  （IMessage 同步处理消息（IMessage msg））
- `MonoMethodMessage get_CallMessage()`
  （MonoMethodMessage get_CallMessage（））
- `void set_CallMessage(MonoMethodMessage value)`
  （void set_CallMessage（MonoMethodMessage value））
- `object Invoke()`
  （object Invoke（））

---

## AsyncTaskCache（异步Task缓存）

### 字段 (3)

- `Task<bool> TrueTask`（Task<bool> TrueTask）(偏移: 0x0)
- `Task<bool> FalseTask`（Task<bool> FalseTask）(偏移: 0x4)
- `Task<int>[] Int32Tasks`（Task<int>[] Int32Tasks）(偏移: 0x8)

### 方法 (1)

- `Task<int>[] CreateInt32Tasks()`
  （Task<int>[] 创建Int32Tasks（））

---

## AsyncTaskMethodBuilder（异步TaskMethod构建器）

### 字段 (2)

- `Task<VoidTaskResult> s_cachedCompleted`（Task<VoidTaskResult> s_cachedCompleted）(偏移: 0x0)
- `AsyncTaskMethodBuilder<VoidTaskResult> m_builder`（异步TaskMethodBuilder<VoidTaskResult> m_builder）(偏移: 0x0)

### 方法 (5)

- `AsyncTaskMethodBuilder Create()`
  （异步TaskMethod构建器 创建（））
- `void SetStateMachine(IAsyncStateMachine stateMachine)`
  （void 集合状态Machine（I异步状态Machine stateMachine））
- `Task get_Task()`
  （Task get_Task（））
- `void SetResult()`
  （void 集合Result（））
- `void SetException(Exception exception)`
  （void 集合Exception（Exception exception））

---

## AttachFollowEffect（AttachFollow特效）

**继承**: RO_WorkListener（RO_Work监听器）

### 字段 (2)

- `GameObject effect`（游戏对象 特效）(偏移: 0xC)
- `Vector3 offset`（三维向量 偏移）(偏移: 0x10)

### 方法 (1)

- `void Work()`
  （void 工作（））

---

## AttachSimpleEffect（AttachSimple特效）

**继承**: RO_WorkListener（RO_Work监听器）

### 字段 (2)

- `GameObject effect`（游戏对象 特效）(偏移: 0xC)
- `Vector3 offset`（三维向量 偏移）(偏移: 0x10)

### 方法 (1)

- `void Work()`
  （void 工作（））

---

## Attribute（属性）

### 方法 (18)

- `Attribute[] InternalGetCustomAttributes(PropertyInfo element, Type type, bool inherit)`
  （Attribute[] 内部的获取自定义的Attributes（属性信息 element, 类型 type, bool inherit））
- `Attribute[] InternalGetCustomAttributes(EventInfo element, Type type, bool inherit)`
  （Attribute[] 内部的获取自定义的Attributes（事件信息 element, 类型 type, bool inherit））
- `bool InternalIsDefined(PropertyInfo element, Type attributeType, bool inherit)`
  （bool 内部的是否Defined（属性信息 element, 类型 attributeType, bool inherit））
- `bool InternalIsDefined(EventInfo element, Type attributeType, bool inherit)`
  （bool 内部的是否Defined（事件信息 element, 类型 attributeType, bool inherit））
- `Attribute[] GetCustomAttributes(MemberInfo element, Type type, bool inherit)`
  （Attribute[] 获取自定义的Attributes（Member信息 element, 类型 type, bool inherit））
- `bool IsDefined(MemberInfo element, Type attributeType)`
  （bool 是否Defined（Member信息 element, 类型 attributeType））
- `bool IsDefined(MemberInfo element, Type attributeType, bool inherit)`
  （bool 是否Defined（Member信息 element, 类型 attributeType, bool inherit））
- `Attribute GetCustomAttribute(MemberInfo element, Type attributeType)`
  （Attribute 获取自定义的Attribute（Member信息 element, 类型 attributeType））
- `Attribute GetCustomAttribute(MemberInfo element, Type attributeType, bool inherit)`
  （Attribute 获取自定义的Attribute（Member信息 element, 类型 attributeType, bool inherit））
- `Attribute[] GetCustomAttributes(Assembly element, Type attributeType, bool inherit)`
  （Attribute[] 获取自定义的Attributes（Assembly element, 类型 attributeType, bool inherit））
- `Attribute GetCustomAttribute(Assembly element, Type attributeType)`
  （Attribute 获取自定义的Attribute（Assembly element, 类型 attributeType））
- `Attribute GetCustomAttribute(Assembly element, Type attributeType, bool inherit)`
  （Attribute 获取自定义的Attribute（Assembly element, 类型 attributeType, bool inherit））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool AreFieldValuesEqual(object thisValue, object thatValue)`
  （bool AreFieldValuesEqual（object thisValue, object thatValue））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `object get_TypeId()`
  （object get_类型Id（））
- `bool Match(object obj)`
  （bool 比赛（object obj））
- `bool IsDefaultAttribute()`
  （布尔值 是否默认属性（））

---

## AttributeCollection（AttributeCollection）

**继承**: ICollection, IEnumerable（ICollection, IEnumerable）

### 字段 (6)

- `AttributeCollection Empty`（AttributeCollection 空）(偏移: 0x0)
- `Hashtable _defaultAttributes`（Hashtable _defaultAttributes）(偏移: 0x4)
- `Attribute[] _attributes`（Attribute[] _attributes）(偏移: 0x8)
- `object internalSyncObject`（object internal同步对象）(偏移: 0x8)
- `AttributeCollection.AttributeEntry[] _foundAttributeTypes`（AttributeCollection.AttributeEntry[] _foundAttributeTypes）(偏移: 0xC)
- `int _index`（整数 _索引）(偏移: 0x10)

### 方法 (8)

- `Attribute[] get_Attributes()`
  （Attribute[] get_Attributes（））
- `int get_Count()`
  （整数 获取_数量（））
- `Attribute get_Item(int index)`
  （Attribute get_项目（int index））
- `Attribute get_Item(Type attributeType)`
  （Attribute get_项目（类型 attributeType））
- `bool Contains(Attribute attribute)`
  （bool Contains（Attribute attribute））
- `Attribute GetDefaultAttribute(Type attributeType)`
  （Attribute 获取默认的Attribute（类型 attributeType））
- `IEnumerator GetEnumerator()`
  （IEnumerator 获取枚举器（））
- `void CopyTo(Array array, int index)`
  （void 复制到（数组 array, 整数 index））

---

## AttributeCollection.AttributeEntry（AttributeCollection.AttributeEntry）

### 字段 (2)

- `Type type`（类型 type）(偏移: 0x0)
- `int index`（整数 索引）(偏移: 0x4)

---

## AttributeHelperEngine（Attribute辅助器引擎）

### 字段 (3)

- `DisallowMultipleComponent[] _disallowMultipleComponentArray`（DisallowMultipleComponent[] _disallowMultiple组件数组）(偏移: 0x0)
- `ExecuteInEditMode[] _executeInEditModeArray`（执行InEditMode[] _executeInEdit模式数组）(偏移: 0x4)
- `RequireComponent[] _requireComponentArray`（RequireComponent[] _require组件数组）(偏移: 0x8)

### 方法 (5)

- `Type GetParentTypeDisallowingMultipleInclusion(Type type)`
  （类型 获取父级类型DisallowingMultipleInclusion（类型 type））
- `Type[] GetRequiredComponents(Type klass)`
  （Type[] 获取RequiredComponents（类型 klass））
- `int GetExecuteMode(Type klass)`
  （int 获取执行模式（类型 klass））
- `int CheckIsEditorScript(Type klass)`
  （int 检查是否EditorScript（类型 klass））
- `int GetDefaultExecutionOrderFor(Type klass)`
  （int 获取默认的ExecutionOrderFor（类型 klass））

---

## AttributeProviderAttribute（Attribute提供者Attribute）

**继承**: Attribute（属性）

### 字段 (2)

- `string _typeName`（字符串 _类型名称）(偏移: 0x8)
- `string _propertyName`（string _property名称）(偏移: 0xC)

### 方法 (2)

- `string get_TypeName()`
  （字符串 获取_类型名称（））
- `string get_PropertyName()`
  （string get_属性名称（））

---

## AttributeTargets（AttributeTargets）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AttributeUsageAttribute（AttributeUsageAttribute）

**继承**: Attribute（属性）

### 字段 (4)

- `AttributeTargets m_attributeTarget`（AttributeTargets m_attribute目标）(偏移: 0x8)
- `bool m_allowMultiple`（bool m_allowMultiple）(偏移: 0xC)
- `bool m_inherited`（bool m_inherited）(偏移: 0xD)
- `AttributeUsageAttribute Default`（AttributeUsageAttribute 默认的）(偏移: 0x0)

### 方法 (4)

- `bool get_AllowMultiple()`
  （bool get_允许Multiple（））
- `void set_AllowMultiple(bool value)`
  （void set_允许Multiple（bool value））
- `bool get_Inherited()`
  （bool get_Inherited（））
- `void set_Inherited(bool value)`
  （void set_Inherited（bool value））

---

## AudioClip（音频弹匣）

**继承**: Object（对象）

### 字段 (2)

- `AudioClip.PCMReaderCallback m_PCMReaderCallback`（音频Clip.PCM读取器回调 m_PCM读取器回调）(偏移: 0xC)
- `AudioClip.PCMSetPositionCallback m_PCMSetPositionCallback`（音频Clip.PCM集合Position回调 m_PCM集合Position回调）(偏移: 0x10)

### 方法 (3)

- `float get_length()`
  （浮点数 获取_长度（））
- `void InvokePCMReaderCallback_Internal(float[] data)`
  （void InvokePCM读取器Callback_内部的（float[] data））
- `void InvokePCMSetPositionCallback_Internal(int position)`
  （void InvokePCM集合PositionCallback_内部的（int position））

---

## AudioClip.PCMReaderCallback（音频Clip.PCM读取器回调）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(float[] data)`
  （void Invoke（float[] data））
- `IAsyncResult BeginInvoke(float[] data, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（float[] data, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## AudioClip.PCMSetPositionCallback（音频Clip.PCM集合Position回调）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(int position)`
  （void Invoke（int position））
- `IAsyncResult BeginInvoke(int position, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（int position, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## AudioClipPlayable（音频弹匣Playable）

**继承**: IPlayable, IEquatable<AudioClipPlayable>（IPlayable, IEquatable<音频弹匣Playable>）

### 字段 (1)

- `PlayableHandle m_Handle`（可播放句柄 m_句柄）(偏移: 0x0)

### 方法 (2)

- `PlayableHandle GetHandle()`
  （可播放句柄 获取句柄（））
- `bool Equals(AudioClipPlayable other)`
  （bool Equals（音频弹匣Playable other））

---

## AudioListener（音频监听器）

**继承**: AudioBehaviour（音频Behaviour）

### 方法 (2)

- `void GetSpectrumDataHelper([Out] float[] samples, int channel, FFTWindow window)`
  （void 获取Spectrum数据辅助器（[Out] float[] samples, int channel, FFTWindow window））
- `void GetSpectrumData(float[] samples, int channel, FFTWindow window)`
  （void 获取Spectrum数据（float[] samples, int channel, FFTWindow window））

---

## AudioMixer（音频Mixer）

**继承**: Object（对象）

### 方法 (2)

- `bool SetFloat(string name, float value)`
  （bool 集合浮点数（string name, float value））
- `bool GetFloat(string name, out float value)`
  （bool 获取浮点数（string name, out float value））

---

## AudioMixerPlayable（音频MixerPlayable）

**继承**: IPlayable, IEquatable<AudioMixerPlayable>（IPlayable, IEquatable<音频MixerPlayable>）

### 字段 (1)

- `PlayableHandle m_Handle`（可播放句柄 m_句柄）(偏移: 0x0)

### 方法 (2)

- `PlayableHandle GetHandle()`
  （可播放句柄 获取句柄（））
- `bool Equals(AudioMixerPlayable other)`
  （bool Equals（音频MixerPlayable other））

---

## AudioPlayableOutput（音频PlayableOutput）

**继承**: IPlayableOutput（I可播放输出）

### 字段 (1)

- `PlayableOutputHandle m_Handle`（可播放输出句柄 m_句柄）(偏移: 0x0)

### 方法 (4)

- `PlayableOutputHandle GetHandle()`
  （可播放输出句柄 获取句柄（））
- `AudioPlayableOutput op_Explicit(PlayableOutput output)`
  （音频PlayableOutput op_Explicit（PlayableOutput output））
- `void SetEvaluateOnSeek(bool value)`
  （void 集合EvaluateOnSeek（bool value））
- `void InternalSetEvaluateOnSeek(ref PlayableOutputHandle output, bool value)`
  （void 内部的集合EvaluateOnSeek（ref PlayableOutputHandle output, bool value））

---

## AudioSampleProvider（音频Sample提供者）

### 字段 (2)

- `AudioSampleProvider.SampleFramesHandler sampleFramesAvailable`（音频SampleProvider.SampleFrames处理器 sampleFramesAvailable）(偏移: 0x8)
- `AudioSampleProvider.SampleFramesHandler sampleFramesOverflow`（音频SampleProvider.SampleFrames处理器 sampleFramesOverflow）(偏移: 0xC)

### 方法 (2)

- `void InvokeSampleFramesAvailable(int sampleFrameCount)`
  （void InvokeSampleFramesAvailable（int sampleFrameCount））
- `void InvokeSampleFramesOverflow(int droppedSampleFrameCount)`
  （void InvokeSampleFramesOverflow（int droppedSampleFrameCount））

---

## AudioSampleProvider.SampleFramesHandler（音频SampleProvider.SampleFrames处理器）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(AudioSampleProvider provider, uint sampleFrameCount)`
  （void Invoke（音频Sample提供者 provider, uint sampleFrameCount））
- `IAsyncResult BeginInvoke(AudioSampleProvider provider, uint sampleFrameCount, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（音频Sample提供者 provider, uint sampleFrameCount, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## AudioSettings（音频Settings）

### 字段 (3)

- `AudioSettings.AudioConfigurationChangeHandler OnAudioConfigurationChanged`（音频Settings.音频ConfigurationChange处理器 On音频ConfigurationChanged）(偏移: 0x0)
- `Action OnAudioSystemShuttingDown`（动作 On音频系统Shutting下）(偏移: 0x4)
- `Action OnAudioSystemStartedUp`（动作 On音频系统Started上）(偏移: 0x8)

### 方法 (3)

- `void InvokeOnAudioConfigurationChanged(bool deviceWasChanged)`
  （void InvokeOn音频ConfigurationChanged（bool deviceWasChanged））
- `void InvokeOnAudioSystemShuttingDown()`
  （void InvokeOn音频系统Shutting下（））
- `void InvokeOnAudioSystemStartedUp()`
  （void InvokeOn音频系统Started上（））

---

## AudioSettings.AudioConfigurationChangeHandler（音频Settings.音频ConfigurationChange处理器）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(bool deviceWasChanged)`
  （void Invoke（bool deviceWasChanged））
- `IAsyncResult BeginInvoke(bool deviceWasChanged, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（bool deviceWasChanged, 异步回调 callback, object object））
- `void EndInvoke(IAsyncResult result)`
  （void 结束调用（I异步结果 result））

---

## AudioSource（音频Source）

**继承**: AudioBehaviour（音频Behaviour）

### 方法 (22)

- `float GetPitch(AudioSource source)`
  （float 获取俯仰角（音频Source source））
- `void SetPitch(AudioSource source, float pitch)`
  （void 集合俯仰角（音频Source source, float pitch））
- `void PlayHelper(AudioSource source, ulong delay)`
  （void 播放辅助器（音频Source source, ulong delay））
- `void Stop(bool stopOneShots)`
  （void 停止（bool stopOneShots））
- `void GetSpectrumDataHelper(AudioSource source, [Out] float[] samples, int channel, FFTWindow window)`
  （void 获取Spectrum数据辅助器（音频Source source, [Out] float[] samples, int channel, FFTWindow window））
- `float get_volume()`
  （float get_volume（））
- `void set_volume(float value)`
  （void set_volume（float value））
- `float get_pitch()`
  （float get_pitch（））
- `void set_pitch(float value)`
  （void set_pitch（float value））
- `void set_time(float value)`
  （void set_time（float value））
- `AudioClip get_clip()`
  （音频弹匣 get_clip（））
- `void set_clip(AudioClip value)`
  （void set_clip（音频弹匣 value））
- `void Play()`
  （void 播放（））
- `void Stop()`
  （void 停止（））
- `bool get_isPlaying()`
  （bool get_isPlaying（））
- `void set_loop(bool value)`
  （void set_loop（bool value））
- `void set_spatialBlend(float value)`
  （void set_spatialBlend（float value））
- `int get_priority()`
  （int get_priority（））
- `void set_priority(int value)`
  （void set_priority（int value））
- `void set_minDistance(float value)`
  （void set_min距离（float value））
- `void set_maxDistance(float value)`
  （void set_max距离（float value））
- `void GetSpectrumData(float[] samples, int channel, FFTWindow window)`
  （void 获取Spectrum数据（float[] samples, int channel, FFTWindow window））

---

## AutoPlay（自动播放）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AutoRepathPolicy（自动RepathPolicy）

### 字段 (7)

- `AutoRepathPolicy.Mode mode`（自动RepathPolicy.模式 mode）(偏移: 0x8)
- `float interval`（浮点数 间隔）(偏移: 0xC)
- `float sensitivity`（float sensitivity）(偏移: 0x10)
- `float maximumInterval`（float maximum间隔）(偏移: 0x14)
- `bool visualizeSensitivity`（bool visualizeSensitivity）(偏移: 0x18)
- `Vector3 lastDestination`（三维向量 lastDestination）(偏移: 0x1C)
- `float lastRepathTime`（float lastRepath时间）(偏移: 0x28)

### 方法 (4)

- `bool ShouldRecalculatePath(IAstarAI ai)`
  （bool 应该Recalculate路径（IAstarAI ai））
- `void Reset()`
  （void 重置（））
- `void DidRecalculatePath(Vector3 destination)`
  （void DidRecalculate路径（三维向量 destination））
- `void DrawGizmos(IAstarAI ai)`
  （void DrawGizmos（IAstarAI ai））

---

## AutoRepathPolicy.Mode（自动RepathPolicy.模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AvailableTrackingData（AvailableTracking数据）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Avatar（Avatar）

**继承**: Object（对象）

### 方法 (9)

- `bool get_isValid()`
  （布尔值 获取_是否有效（））
- `bool get_isHuman()`
  （bool get_is人类（））
- `HumanDescription get_humanDescription()`
  （人类Description get_humanDescription（））
- `float GetAxisLength(int humanId)`
  （float 获取轴Length（int humanId））
- `Quaternion GetPostRotation(int humanId)`
  （Quaternion 获取PostRotation（int humanId））
- `float Internal_GetAxisLength(int humanId)`
  （float Internal_获取轴Length（int humanId））
- `Quaternion Internal_GetPostRotation(int humanId)`
  （Quaternion Internal_获取PostRotation（int humanId））
- `void get_humanDescription_Injected(out HumanDescription ret)`
  （void get_humanDescription_Injected（out HumanDescription ret））
- `void Internal_GetPostRotation_Injected(int humanId, out Quaternion ret)`
  （void Internal_获取PostRotation_Injected（int humanId, out Quaternion ret））

---

## AvatarIKGoal（AvatarIKGoal）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AvatarMask（Avatar掩码）

**继承**: Object（对象）

### 方法 (5)

- `bool GetHumanoidBodyPartActive(AvatarMaskBodyPart index)`
  （bool 获取Humanoid身体Part激活的（Avatar掩码身体Part index））
- `int get_transformCount()`
  （int get_transform数量（））
- `string GetTransformPath(int index)`
  （string 获取变换路径（int index））
- `float GetTransformWeight(int index)`
  （float 获取变换Weight（int index））
- `bool GetTransformActive(int index)`
  （bool 获取变换激活的（int index））

---

## AvatarMaskBodyPart（Avatar掩码身体Part）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AvatarUtility（Avatar工具）

### 方法 (3)

- `Quaternion GetPostRotation(Avatar avatar, AvatarIKGoal avatarIKGoal)`
  （Quaternion 获取PostRotation（Avatar avatar, AvatarIKGoal avatarIKGoal））
- `TQ GetIKGoalTQ(Avatar avatar, float humanScale, AvatarIKGoal avatarIKGoal, TQ bodyPositionRotation, TQ boneTQ)`
  （TQ 获取IKGoalTQ（Avatar avatar, float humanScale, AvatarIKGoal avatarIKGoal, TQ bodyPositionRotation, TQ boneTQ））
- `HumanBodyBones HumanIDFromAvatarIKGoal(AvatarIKGoal avatarIKGoal)`
  （人类身体Bones 人类IDFromAvatarIKGoal（AvatarIKGoal avatarIKGoal））

---

## AwaitTaskContinuation（AwaitTaskContinuation）

**继承**: TaskContinuation, IThreadPoolWorkItem（TaskContinuation, IThread池Work项目）

### 字段 (3)

- `ExecutionContext m_capturedContext`（ExecutionContext m_capturedContext）(偏移: 0x8)
- `Action m_action`（动作 m_action）(偏移: 0xC)
- `ContextCallback s_invokeActionCallback`（Context回调 s_invoke动作回调）(偏移: 0x0)

### 方法 (10)

- `Task CreateTask(Action<object> action, object state, TaskScheduler scheduler)`
  （Task 创建Task（Action<object> action, object state, TaskScheduler scheduler））
- `void Run(Task task, bool canInlineContinuationTask)`
  （void 运行（Task task, bool canInlineContinuationTask））
- `bool get_IsValidLocationForInlining()`
  （bool get_是否ValidLocationForInlining（））
- `void ExecuteWorkItemHelper()`
  （void 执行Work项目辅助器（））
- `void InvokeAction(object state)`
  （void Invoke动作（object state））
- `ContextCallback GetInvokeActionCallback()`
  （Context回调 获取Invoke动作回调（））
- `void RunCallback(ContextCallback callback, object state, ref Task currentTask)`
  （void 运行回调（Context回调 callback, object state, ref Task currentTask））
- `void RunOrScheduleAction(Action action, bool allowInlining, ref Task currentTask)`
  （void 运行OrSchedule动作（动作 action, bool allowInlining, ref Task currentTask））
- `void UnsafeScheduleAction(Action action, Task task)`
  （void UnsafeSchedule动作（动作 action, Task task））
- `void ThrowAsyncIfNecessary(Exception exc)`
  （void 投掷异步IfNecessary（Exception exc））

---

## Axis（轴）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AxisBase（轴基础）

### 字段 (4)

- `float m_Value`（浮点数 m_值）(偏移: 0x0)
- `float m_MinValue`（float m_最小值）(偏移: 0x4)
- `float m_MaxValue`（float m_最大值）(偏移: 0x8)
- `bool m_Wrap`（bool m_Wrap）(偏移: 0xC)

### 方法 (1)

- `void Validate()`
  （void 验证（））

---

## AxisConstraint（轴Constraint）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AxisEventData（轴事件数据）

**继承**: BaseEventData（基础事件数据）

### 方法 (4)

- `Vector2 get_moveVector()`
  （二维向量 get_move向量（））
- `void set_moveVector(Vector2 value)`
  （void set_move向量（二维向量 value））
- `MoveDirection get_moveDir()`
  （移动方向 get_moveDir（））
- `void set_moveDir(MoveDirection value)`
  （void set_moveDir（移动方向 value））

---

## AxisState（轴状态）

### 字段 (17)

- `float Value`（float 值）(偏移: 0x0)
- `AxisState.SpeedMode m_SpeedMode`（轴State.Speed模式 m_Speed模式）(偏移: 0x4)
- `float m_MaxSpeed`（float m_最大Speed）(偏移: 0x8)
- `float m_AccelTime`（float m_Accel时间）(偏移: 0xC)
- `float m_DecelTime`（float m_Decel时间）(偏移: 0x10)
- `string m_InputAxisName`（string m_输入轴名称）(偏移: 0x14)
- `float m_InputAxisValue`（float m_输入轴值）(偏移: 0x18)
- `bool m_InvertInput`（bool m_Invert输入）(偏移: 0x1C)
- `float m_MinValue`（float m_最小值）(偏移: 0x20)
- `float m_MaxValue`（float m_最大值）(偏移: 0x24)
- `bool m_Wrap`（bool m_Wrap）(偏移: 0x28)
- `AxisState.Recentering m_Recentering`（轴State.Recentering m_Recentering）(偏移: 0x2C)
- `float m_CurrentSpeed`（float m_当前Speed）(偏移: 0x48)
- `float m_LastUpdateTime`（float m_最后一个更新时间）(偏移: 0x4C)
- `int m_LastUpdateFrame`（int m_最后一个更新Frame）(偏移: 0x50)
- `AxisState.IInputAxisProvider m_InputAxisProvider`（轴State.I输入轴提供者 m_输入轴提供者）(偏移: 0x54)
- `int m_InputAxisIndex`（int m_输入轴索引）(偏移: 0x58)

### 方法 (12)

- `void Validate()`
  （void 验证（））
- `void Reset()`
  （void 重置（））
- `void SetInputAxisProvider(int axis, AxisState.IInputAxisProvider provider)`
  （void 集合输入轴提供者（int axis, 轴State.I输入轴提供者 provider））
- `bool get_HasInputProvider()`
  （bool get_是否有输入提供者（））
- `bool Update(float deltaTime)`
  （bool 更新（float deltaTime））
- `float ClampValue(float v)`
  （float Clamp值（float v））
- `bool MaxSpeedUpdate(float input, float deltaTime)`
  （bool 最大Speed更新（float input, float deltaTime））
- `float GetMaxSpeed()`
  （float 获取最大Speed（））
- `bool get_ValueRangeLocked()`
  （bool get_值范围锁定的（））
- `void set_ValueRangeLocked(bool value)`
  （void set_值范围锁定的（bool value））
- `bool get_HasRecentering()`
  （bool get_是否有Recentering（））
- `void set_HasRecentering(bool value)`
  （void set_是否有Recentering（bool value））

---

## AxisState.Recentering（轴State.Recentering）

### 字段 (7)

- `bool m_enabled`（bool m_enabled）(偏移: 0x0)
- `float m_WaitTime`（float m_Wait时间）(偏移: 0x4)
- `float m_RecenteringTime`（float m_Recentering时间）(偏移: 0x8)
- `float mLastAxisInputTime`（float m最后一个轴输入时间）(偏移: 0xC)
- `float mRecenteringVelocity`（float mRecentering速度）(偏移: 0x10)
- `int m_LegacyHeadingDefinition`（int m_LegacyHeadingDefinition）(偏移: 0x14)
- `int m_LegacyVelocityFilterStrength`（int m_Legacy速度FilterStrength）(偏移: 0x18)

### 方法 (6)

- `void Validate()`
  （void 验证（））
- `void CopyStateFrom(ref AxisState.Recentering other)`
  （void 复制状态From（ref AxisState.Recentering other））
- `void CancelRecentering()`
  （void 取消Recentering（））
- `void RecenterNow()`
  （void RecenterNow（））
- `void DoRecentering(ref AxisState axis, float deltaTime, float recenterTarget)`
  （void DoRecentering（ref AxisState axis, float deltaTime, float recenterTarget））
- `bool LegacyUpgrade(ref int heading, ref int velocityFilter)`
  （bool LegacyUpgrade（ref int heading, ref int velocityFilter））

---

## AxisState.SpeedMode（轴State.Speed模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## AxisTools（轴Tools）

### 方法 (7)

- `Vector3 ToVector3(Axis axis)`
  （三维向量 To三维向量（轴 axis））
- `Axis ToAxis(Vector3 v)`
  （轴 To轴（三维向量 v））
- `Axis GetAxisToPoint(Transform t, Vector3 worldPosition)`
  （轴 获取轴ToPoint（变换 t, 三维向量 worldPosition））
- `Axis GetAxisToDirection(Transform t, Vector3 direction)`
  （轴 获取轴To方向（变换 t, 三维向量 direction））
- `Vector3 GetAxisVectorToPoint(Transform t, Vector3 worldPosition)`
  （三维向量 获取轴向量ToPoint（变换 t, 三维向量 worldPosition））
- `Vector3 GetAxisVectorToDirection(Transform t, Vector3 direction)`
  （三维向量 获取轴向量To方向（变换 t, 三维向量 direction））
- `Vector3 GetAxisVectorToDirection(Quaternion r, Vector3 direction)`
  （三维向量 获取轴向量To方向（Quaternion r, 三维向量 direction））

---

## BA_BecomeHero（BA_Become英雄）

**继承**: BotActionBase（机器人动作基础）

### 字段 (2)

- `bool isNano4T`（bool isNano4T）(偏移: 0x10)
- `float tryBecomeTime`（float tryBecome时间）(偏移: 0x14)

### 方法 (3)

- `bool CanDo()`
  （布尔值 能否执行（））
- `void DoAction()`
  （void 执行动作（））
- `void Update()`
  （void 更新（））

---

## BA_Nano_WatchOutTeammate（BA_Nano_WatchOutTeammate）

**继承**: BotActionBase（机器人动作基础）

### 字段 (3)

- `float nextChangeTime`（float nextChange时间）(偏移: 0x10)
- `Transform teammate`（变换 teammate）(偏移: 0x14)
- `List<Collider> cldList`（List<Collider> cld列表）(偏移: 0x18)

### 方法 (5)

- `void Bot_Getter_ZoomDirection(ref Vector3 zoomDir, ref int priority)`
  （void Bot_Getter_瞄准方向（ref Vector3 zoomDir, ref int priority））
- `void Update()`
  （void 更新（））
- `void OnActionFinish()`
  （void 动作完成时（））
- `bool CanDo()`
  （布尔值 能否执行（））
- `void DoAction()`
  （void 执行动作（））

---

## BA_PickUpUpgradeBox（BA_Pick上UpgradeBox）

**继承**: BotActionBase（机器人动作基础）

### 字段 (2)

- `SupplyBox target`（SupplyBox target）(偏移: 0x10)
- `bool ignoreBoxSavior`（bool ignoreBoxSavior）(偏移: 0x14)

### 方法 (4)

- `void Bot_Destination_Listener(ref Vector3 pos, ref int priority)`
  （void Bot_目的地_监听器（引用 Vector3 pos, 引用 整数 priority））
- `bool CanDo()`
  （布尔值 能否执行（））
- `void DoAction()`
  （void 执行动作（））
- `void FindUpgradeBox()`
  （void 查找UpgradeBox（））

---

## BA_WantInfected（BA_想要Infected）

**继承**: BotActionBase（机器人动作基础）

### 字段 (3)

- `float Rate`（float Rate）(偏移: 0x0)
- `bool goDie`（bool goDie）(偏移: 0x10)
- `float nextCheckTime`（float next检查时间）(偏移: 0x14)

### 方法 (5)

- `void Bot_Destination_Listener(ref Vector3 pos, ref int priority)`
  （void Bot_目的地_监听器（引用 Vector3 pos, 引用 整数 priority））
- `bool CanDo()`
  （布尔值 能否执行（））
- `void DoAction()`
  （void 执行动作（））
- `void UpdateNextCheckTime()`
  （void 更新下一个检查时间（））
- `void SetDefaultRate()`
  （void 集合默认的Rate（））

---

## BBTree（BBTree）

**继承**: IAstarPooledObject（IAstarPooled对象）

### 字段 (4)

- `BBTree.BBTreeBox[] tree`（BBTree.BBTreeBox[] tree）(偏移: 0x8)
- `TriangleMeshNode[] nodeLookup`（Triangle网格Node[] nodeLookup）(偏移: 0xC)
- `int count`（整数 数量）(偏移: 0x10)
- `int leafNodes`（int leafNodes）(偏移: 0x14)

### 方法 (25)

- `Rect get_Size()`
  （Rect get_大小（））
- `void Clear()`
  （void 清除（））
- `void EnsureCapacity(int c)`
  （void EnsureCapacity（int c））
- `void EnsureNodeCapacity(int c)`
  （void Ensure节点Capacity（int c））
- `int GetBox(IntRect rect)`
  （int 获取Box（整数Rect rect））
- `void RebuildFrom(TriangleMeshNode[] nodes)`
  （void RebuildFrom（Triangle网格Node[] nodes））
- `int SplitByX(TriangleMeshNode[] nodes, int[] permutation, int from, int to, int divider)`
  （int SplitByX（Triangle网格Node[] nodes, int[] permutation, int from, int to, int divider））
- `int SplitByZ(TriangleMeshNode[] nodes, int[] permutation, int from, int to, int divider)`
  （int SplitByZ（Triangle网格Node[] nodes, int[] permutation, int from, int to, int divider））
- `int RebuildFromInternal(TriangleMeshNode[] nodes, int[] permutation, IntRect[] nodeBounds, int from, int to, bool odd)`
  （int RebuildFrom内部的（Triangle网格Node[] nodes, int[] permutation, 整数Rect[] nodeBounds, int from, int to, bool odd））
- `IntRect NodeBounds(int[] permutation, IntRect[] nodeBounds, int from, int to)`
  （整数Rect 节点Bounds（int[] permutation, 整数Rect[] nodeBounds, int from, int to））
- `void DrawDebugRect(IntRect rect)`
  （void DrawDebugRect（整数Rect rect））
- `void DrawDebugNode(TriangleMeshNode node, float yoffset, Color color)`
  （void DrawDebug节点（Triangle网格节点 node, float yoffset, 颜色 color））
- `NNInfoInternal QueryClosest(Vector3 p, NNConstraint constraint, out float distance)`
  （NN信息内部的 QueryClosest（三维向量 p, NNConstraint constraint, out float distance））
- `NNInfoInternal QueryClosestXZ(Vector3 p, NNConstraint constraint, ref float distance, NNInfoInternal previous)`
  （NN信息内部的 QueryClosestXZ（三维向量 p, NNConstraint constraint, ref float distance, NN信息内部的 previous））
- `void SearchBoxClosestXZ(int boxi, Vector3 p, ref float closestSqrDist, NNConstraint constraint, ref NNInfoInternal nnInfo)`
  （void 搜索BoxClosestXZ（int boxi, 三维向量 p, ref float closestSqrDist, NNConstraint constraint, ref NNInfoInternal nnInfo））
- `NNInfoInternal QueryClosest(Vector3 p, NNConstraint constraint, ref float distance, NNInfoInternal previous)`
  （NN信息内部的 QueryClosest（三维向量 p, NNConstraint constraint, ref float distance, NN信息内部的 previous））
- `void SearchBoxClosest(int boxi, Vector3 p, ref float closestSqrDist, NNConstraint constraint, ref NNInfoInternal nnInfo)`
  （void 搜索BoxClosest（int boxi, 三维向量 p, ref float closestSqrDist, NNConstraint constraint, ref NNInfoInternal nnInfo））
- `void GetOrderedChildren(ref int first, ref int second, out float firstDist, out float secondDist, Vector3 p)`
  （void 获取OrderedChildren（ref int first, ref int second, out float firstDist, out float secondDist, 三维向量 p））
- `TriangleMeshNode QueryInside(Vector3 p, NNConstraint constraint)`
  （Triangle网格节点 QueryInside（三维向量 p, NNConstraint constraint））
- `TriangleMeshNode SearchBoxInside(int boxi, Vector3 p, NNConstraint constraint)`
  （Triangle网格节点 搜索BoxInside（int boxi, 三维向量 p, NNConstraint constraint））
- `void OnDrawGizmos()`
  （void 绘制辅助线时（））
- `void OnDrawGizmos(int boxi, int depth)`
  （void OnDrawGizmos（int boxi, int depth））
- `bool NodeIntersectsCircle(TriangleMeshNode node, Vector3 p, float radius)`
  （bool 节点IntersectsCircle（Triangle网格节点 node, 三维向量 p, float radius））
- `bool RectIntersectsCircle(IntRect r, Vector3 p, float radius)`
  （bool RectIntersectsCircle（整数Rect r, 三维向量 p, float radius））
- `float SquaredRectPointDistance(IntRect r, Vector3 p)`
  （float SquaredRectPoint距离（整数Rect r, 三维向量 p））

---

## BBTree.BBTreeBox（BBTree.BBTreeBox）

### 字段 (4)

- `IntRect rect`（整数Rect rect）(偏移: 0x0)
- `int nodeOffset`（int nodeOffset）(偏移: 0x10)
- `int left`（int left）(偏移: 0x14)
- `int right`（int right）(偏移: 0x18)

### 方法 (2)

- `bool get_IsLeaf()`
  （bool get_是否Leaf（））
- `bool Contains(Vector3 point)`
  （布尔值 包含（三维向量 point））

---

## BRECORD（BRECORD）

### 字段 (2)

- `IntPtr pvRecord`（整数Ptr pvRecord）(偏移: 0x0)
- `IntPtr pRecInfo`（整数Ptr pRec信息）(偏移: 0x4)

---

## BadImageFormatException（Bad图像格式化Exception）

**继承**: SystemException（系统异常）

### 字段 (2)

- `string _fileName`（string _file名称）(偏移: 0x44)
- `string _fusionLog`（string _fusionLog）(偏移: 0x48)

### 方法 (5)

- `string get_Message()`
  （字符串 获取_消息（））
- `void SetMessageField()`
  （void 设置消息字段（））
- `string ToString()`
  （字符串 转字符串（））
- `string get_FusionLog()`
  （string get_FusionLog（））
- `void GetObjectData(SerializationInfo info, StreamingContext context)`
  （void 获取对象数据（序列化信息 info, 流上下文 context））

---

## Baker（Baker）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (11)

- `int frameRate`（int frameRate）(偏移: 0xC)
- `float keyReductionError`（float keyReductionError）(偏移: 0x10)
- `Baker.Mode mode`（Baker.模式 mode）(偏移: 0x14)
- `AnimationClip[] animationClips`（动画Clip[] animationClips）(偏移: 0x18)
- `string[] animationStates`（string[] animationStates）(偏移: 0x1C)
- `bool loop`（bool loop）(偏移: 0x20)
- `string saveToFolder`（string saveToFolder）(偏移: 0x24)
- `string appendName`（string append名称）(偏移: 0x28)
- `string saveName`（string save名称）(偏移: 0x2C)
- `Animator animator`（动画器 animator）(偏移: 0x38)
- `PlayableDirector director`（PlayableDirector director）(偏移: 0x3C)

### 方法 (13)

- `void OpenUserManual()`
  （void 打开用户手动（））
- `void OpenScriptReference()`
  （void 打开脚本引用（））
- `void SupportGroup()`
  （void 支持组（））
- `void ASThread()`
  （void 异步线程（））
- `bool get_isBaking()`
  （bool get_isBaking（））
- `void set_isBaking(bool value)`
  （void set_isBaking（bool value））
- `float get_bakingProgress()`
  （float get_bakingProgress（））
- `void set_bakingProgress(float value)`
  （void set_bakingProgress（float value））
- `float get_clipLength()`
  （float get_clipLength（））
- `void set_clipLength(float value)`
  （void set_clipLength（float value））
- `void BakeClip()`
  （void Bake弹匣（））
- `void StartBaking()`
  （void 开始Baking（））
- `void StopBaking()`
  （void 停止Baking（））

---

## Baker.Mode（Baker.模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## BakerHumanoidQT（BakerHumanoidQT）

### 字段 (18)

- `Transform transform`（变换 transform）(偏移: 0x8)
- `string Qx`（string Qx）(偏移: 0xC)
- `string Qy`（string Qy）(偏移: 0x10)
- `string Qz`（string Qz）(偏移: 0x14)
- `string Qw`（string Qw）(偏移: 0x18)
- `string Tx`（string Tx）(偏移: 0x1C)
- `string Ty`（string Ty）(偏移: 0x20)
- `string Tz`（string Tz）(偏移: 0x24)
- `AnimationCurve rotX`（动画Curve rotX）(偏移: 0x28)
- `AnimationCurve rotY`（动画Curve rotY）(偏移: 0x2C)
- `AnimationCurve rotZ`（动画Curve rotZ）(偏移: 0x30)
- `AnimationCurve rotW`（动画Curve rotW）(偏移: 0x34)
- `AnimationCurve posX`（动画Curve posX）(偏移: 0x38)
- `AnimationCurve posY`（动画Curve posY）(偏移: 0x3C)
- `AnimationCurve posZ`（动画Curve posZ）(偏移: 0x40)
- `AvatarIKGoal goal`（AvatarIKGoal goal）(偏移: 0x44)
- `Quaternion lastQ`（Quaternion lastQ）(偏移: 0x48)
- `bool lastQSet`（bool lastQ集合）(偏移: 0x58)

### 方法 (8)

- `void Reset()`
  （void 重置（））
- `void SetIKKeyframes(float time, Avatar avatar, float humanScale, Vector3 bodyPosition, Quaternion bodyRotation)`
  （void 集合IKKeyframes（float time, Avatar avatar, float humanScale, 三维向量 bodyPosition, Quaternion bodyRotation））
- `void SetKeyframes(float time, Vector3 pos, Quaternion rot)`
  （void 集合Keyframes（float time, 三维向量 pos, Quaternion rot））
- `void MoveLastKeyframes(float time)`
  （void 移动最后一个Keyframes（float time））
- `void SetLoopFrame(float time)`
  （void 集合LoopFrame（float time））
- `void MoveLastKeyframe(float time, AnimationCurve curve)`
  （void 移动最后一个Keyframe（float time, 动画Curve curve））
- `void MultiplyLength(AnimationCurve curve, float mlp)`
  （void MultiplyLength（动画Curve curve, float mlp））
- `void SetCurves(ref AnimationClip clip, float maxError, float lengthMlp)`
  （void 集合Curves（ref AnimationClip clip, float maxError, float lengthMlp））

---

## BakerMuscle（BakerMuscle）

### 字段 (3)

- `AnimationCurve curve`（动画Curve curve）(偏移: 0x8)
- `int muscleIndex`（int muscle索引）(偏移: 0xC)
- `string propertyName`（string property名称）(偏移: 0x10)

### 方法 (6)

- `string MuscleNameToPropertyName(string n)`
  （string Muscle名称To属性名称（string n））
- `void MultiplyLength(AnimationCurve curve, float mlp)`
  （void MultiplyLength（动画Curve curve, float mlp））
- `void SetCurves(ref AnimationClip clip, float maxError, float lengthMlp)`
  （void 集合Curves（ref AnimationClip clip, float maxError, float lengthMlp））
- `void Reset()`
  （void 重置（））
- `void SetKeyframe(float time, float[] muscles)`
  （void 集合Keyframe（float time, float[] muscles））
- `void SetLoopFrame(float time)`
  （void 集合LoopFrame（float time））

---

## BakerTransform（Baker变换）

### 字段 (13)

- `Transform transform`（变换 transform）(偏移: 0x8)
- `AnimationCurve posX`（动画Curve posX）(偏移: 0xC)
- `AnimationCurve posY`（动画Curve posY）(偏移: 0x10)
- `AnimationCurve posZ`（动画Curve posZ）(偏移: 0x14)
- `AnimationCurve rotX`（动画Curve rotX）(偏移: 0x18)
- `AnimationCurve rotY`（动画Curve rotY）(偏移: 0x1C)
- `AnimationCurve rotZ`（动画Curve rotZ）(偏移: 0x20)
- `AnimationCurve rotW`（动画Curve rotW）(偏移: 0x24)
- `string relativePath`（string relative路径）(偏移: 0x28)
- `bool recordPosition`（bool recordPosition）(偏移: 0x2C)
- `Vector3 relativePosition`（三维向量 relativePosition）(偏移: 0x30)
- `bool isRootNode`（bool is根节点）(偏移: 0x3C)
- `Quaternion relativeRotation`（Quaternion relativeRotation）(偏移: 0x40)

### 方法 (7)

- `void SetRelativeSpace(Vector3 position, Quaternion rotation)`
  （void 集合RelativeSpace（三维向量 position, Quaternion rotation））
- `void SetCurves(ref AnimationClip clip)`
  （void 集合Curves（ref AnimationClip clip））
- `void AddRootMotionCurves(ref AnimationClip clip)`
  （void 添加根MotionCurves（ref AnimationClip clip））
- `void Reset()`
  （void 重置（））
- `void ReduceKeyframes(float maxError)`
  （void ReduceKeyframes（float maxError））
- `void SetKeyframes(float time)`
  （void 集合Keyframes（float time））
- `void AddLoopFrame(float time)`
  （void 添加LoopFrame（float time））

---

## BakerUtilities（BakerUtilities）

### 方法 (5)

- `void ReduceKeyframes(AnimationCurve curve, float maxError)`
  （void ReduceKeyframes（动画Curve curve, float maxError））
- `Keyframe[] GetReducedKeyframes(AnimationCurve curve, float maxError)`
  （Keyframe[] 获取ReducedKeyframes（动画Curve curve, float maxError））
- `void SetLoopFrame(float time, AnimationCurve curve)`
  （void 集合LoopFrame（float time, 动画Curve curve））
- `void SetTangentMode(AnimationCurve curve)`
  （void 集合Tangent模式（动画Curve curve））
- `Quaternion EnsureQuaternionContinuity(Quaternion lastQ, Quaternion q)`
  （Quaternion EnsureQuaternionContinuity（Quaternion lastQ, Quaternion q））

---

## Base64FormattingOptions（Base64FormattingOptions）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## BaseEventData（基础事件数据）

**继承**: AbstractEventData（抽象的事件数据）

### 字段 (1)

- `EventSystem m_EventSystem`（事件系统 m_事件系统）(偏移: 0xC)

### 方法 (3)

- `BaseInputModule get_currentInputModule()`
  （基础输入模块 get_current输入模块（））
- `GameObject get_selectedObject()`
  （游戏对象 get_selected对象（））
- `void set_selectedObject(GameObject value)`
  （void set_selected对象（游戏对象 value））

---

## BaseInput（基础输入）

**继承**: UIBehaviour（UI行为）

### 方法 (16)

- `string get_compositionString()`
  （string get_composition字符串（））
- `IMECompositionMode get_imeCompositionMode()`
  （IMEComposition模式 get_imeComposition模式（））
- `void set_imeCompositionMode(IMECompositionMode value)`
  （void set_imeComposition模式（IMEComposition模式 value））
- `Vector2 get_compositionCursorPos()`
  （二维向量 get_compositionCursorPos（））
- `void set_compositionCursorPos(Vector2 value)`
  （void set_compositionCursorPos（二维向量 value））
- `bool get_mousePresent()`
  （bool get_mousePresent（））
- `bool GetMouseButtonDown(int button)`
  （bool 获取鼠标按钮下（int button））
- `bool GetMouseButtonUp(int button)`
  （bool 获取鼠标按钮上（int button））
- `bool GetMouseButton(int button)`
  （bool 获取鼠标按钮（int button））
- `Vector2 get_mousePosition()`
  （二维向量 get_mousePosition（））
- `Vector2 get_mouseScrollDelta()`
  （二维向量 get_mouse滚动Delta（））
- `bool get_touchSupported()`
  （bool get_touchSupported（））
- `int get_touchCount()`
  （int get_touch数量（））
- `Touch GetTouch(int index)`
  （触摸 获取触摸（int index））
- `float GetAxisRaw(string axisName)`
  （float 获取轴Raw（string axisName））
- `bool GetButtonDown(string buttonName)`
  （bool 获取按钮下（string buttonName））

---

## BaseInputModule（基础输入模块）

**继承**: UIBehaviour（UI行为）

### 字段 (6)

- `List<RaycastResult> m_RaycastResultCache`（List<RaycastResult> m_RaycastResult缓存）(偏移: 0xC)
- `AxisEventData m_AxisEventData`（轴事件数据 m_轴事件数据）(偏移: 0x10)
- `EventSystem m_EventSystem`（事件系统 m_事件系统）(偏移: 0x14)
- `BaseEventData m_BaseEventData`（基础事件数据 m_基础事件数据）(偏移: 0x18)
- `BaseInput m_InputOverride`（基础输入 m_输入重写）(偏移: 0x1C)
- `BaseInput m_DefaultInput`（基础输入 m_默认的输入）(偏移: 0x20)

### 方法 (19)

- `BaseInput get_input()`
  （基础输入 get_input（））
- `BaseInput get_inputOverride()`
  （基础输入 get_input重写（））
- `void set_inputOverride(BaseInput value)`
  （void set_input重写（基础输入 value））
- `EventSystem get_eventSystem()`
  （事件系统 get_event系统（））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `RaycastResult FindFirstRaycast(List<RaycastResult> candidates)`
  （RaycastResult 查找第一个Raycast（List<RaycastResult> candidates））
- `MoveDirection DetermineMoveDirection(float x, float y)`
  （移动方向 Determine移动方向（float x, float y））
- `MoveDirection DetermineMoveDirection(float x, float y, float deadZone)`
  （移动方向 Determine移动方向（float x, float y, float deadZone））
- `GameObject FindCommonRoot(GameObject g1, GameObject g2)`
  （游戏对象 查找Common根（游戏对象 g1, 游戏对象 g2））
- `void HandlePointerExitAndEnter(PointerEventData currentPointerData, GameObject newEnterTarget)`
  （void 句柄指针ExitAndEnter（指针事件数据 currentPointerData, 游戏对象 newEnterTarget））
- `AxisEventData GetAxisEventData(float x, float y, float moveDeadZone)`
  （轴事件数据 获取轴事件数据（float x, float y, float moveDeadZone））
- `BaseEventData GetBaseEventData()`
  （基础事件数据 获取基础事件数据（））
- `bool IsPointerOverGameObject(int pointerId)`
  （bool 是否指针Over游戏对象（int pointerId））
- `bool ShouldActivateModule()`
  （bool 应该激活模块（））
- `void DeactivateModule()`
  （void 停用模块（））
- `void ActivateModule()`
  （void 激活模块（））
- `void UpdateModule()`
  （void 更新模块（））
- `bool IsModuleSupported()`
  （bool 是否模块Supported（））

---

## BaseInvokableCall（基础InvokableCall）

### 方法 (1)

- `bool AllowInvoke(Delegate delegate)`
  （bool 允许Invoke（委托 delegate））

---

## BaseMeshEffect（基础网格特效）

**继承**: UIBehaviour, IMeshModifier（界面Behaviour, I网格修改器）

### 字段 (1)

- `Graphic m_Graphic`（Graphic m_Graphic）(偏移: 0xC)

### 方法 (5)

- `Graphic get_graphic()`
  （Graphic get_graphic（））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `void OnDidApplyAnimationProperties()`
  （void 已应用动画属性时（））
- `void ModifyMesh(Mesh mesh)`
  （void Modify网格（网格 mesh））

---

## BaseNumberConverter（基础数字转换器）

**继承**: TypeConverter（类型转换器）

### 方法 (6)

- `bool get_AllowHex()`
  （布尔值 获取_允许十六进制（））
- `Exception FromStringError(string failedText, Exception innerException)`
  （Exception From字符串Error（string failedText, Exception innerException））
- `bool CanConvertFrom(ITypeDescriptorContext context, Type sourceType)`
  （布尔值 能否转换自（I类型描述符上下文 context, 类型 sourceType））
- `object ConvertFrom(ITypeDescriptorContext context, CultureInfo culture, object value)`
  （对象 转换自（I类型描述符上下文 context, 区域性信息 culture, 对象 value））
- `object ConvertTo(ITypeDescriptorContext context, CultureInfo culture, object value, Type destinationType)`
  （对象 转换到（I类型描述符上下文 context, 区域性信息 culture, 对象 value, 类型 destinationType））
- `bool CanConvertTo(ITypeDescriptorContext context, Type t)`
  （bool 能否转换To（I类型DescriptorContext context, 类型 t））

---

## BaseRaycaster（基础Raycaster）

**继承**: UIBehaviour（UI行为）

### 字段 (1)

- `BaseRaycaster m_RootRaycaster`（基础Raycaster m_根Raycaster）(偏移: 0xC)

### 方法 (9)

- `int get_priority()`
  （int get_priority（））
- `int get_sortOrderPriority()`
  （int get_sortOrderPriority（））
- `int get_renderOrderPriority()`
  （int get_renderOrderPriority（））
- `BaseRaycaster get_rootRaycaster()`
  （基础Raycaster get_rootRaycaster（））
- `string ToString()`
  （字符串 转字符串（））
- `void OnEnable()`
  （void 启用时（））
- `void OnDisable()`
  （void 禁用时（））
- `void OnCanvasHierarchyChanged()`
  （void 画布层级改变时（））
- `void OnTransformParentChanged()`
  （void 变换父级改变时（））

---

## BaselineFunction（BaselineFunction）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `float Invoke(YogaNode node, float width, float height)`
  （float Invoke（Yoga节点 node, float width, float height））
- `IAsyncResult BeginInvoke(YogaNode node, float width, float height, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Yoga节点 node, float width, float height, 异步回调 callback, object object））
- `float EndInvoke(IAsyncResult result)`
  （浮点数 结束调用（I异步结果 result））

---

## BatchCullingContext（BatchCullingContext）

### 字段 (7)

- `NativeArray<Plane> cullingPlanes`（NativeArray<Plane> cullingPlanes）(偏移: 0x0)
- `NativeArray<BatchVisibility> batchVisibility`（NativeArray<BatchVisibility> batchVisibility）(偏移: 0xC)
- `NativeArray<int> visibleIndices`（NativeArray<int> visibleIndices）(偏移: 0x18)
- `NativeArray<int> visibleIndicesY`（NativeArray<int> visibleIndicesY）(偏移: 0x24)
- `LODParameters lodParameters`（LODParameters lodParameters）(偏移: 0x30)
- `Matrix4x4 cullingMatrix`（Matrix4x4 culling矩阵）(偏移: 0x4C)
- `float nearPlane`（float nearPlane）(偏移: 0x8C)

---

## BatchRendererCullingOutput（Batch渲染器CullingOutput）

### 字段 (10)

- `JobHandle cullingJobsFence`（Job句柄 cullingJobsFence）(偏移: 0x0)
- `Matrix4x4 cullingMatrix`（Matrix4x4 culling矩阵）(偏移: 0x8)
- `Plane* cullingPlanes`（Plane* cullingPlanes）(偏移: 0x48)
- `BatchVisibility* batchVisibility`（BatchVisibility* batchVisibility）(偏移: 0x4C)
- `int* visibleIndices`（int* visibleIndices）(偏移: 0x50)
- `int* visibleIndicesY`（int* visibleIndicesY）(偏移: 0x54)
- `int cullingPlanesCount`（int cullingPlanes数量）(偏移: 0x58)
- `int batchVisibilityCount`（int batchVisibility数量）(偏移: 0x5C)
- `int visibleIndicesCount`（int visibleIndices数量）(偏移: 0x60)
- `float nearPlane`（float nearPlane）(偏移: 0x64)

---

## BatchRendererGroup（Batch渲染器组）

### 字段 (2)

- `IntPtr m_GroupHandle`（整数Ptr m_组句柄）(偏移: 0x8)
- `BatchRendererGroup.OnPerformCulling m_PerformCulling`（Batch渲染器Group.On执行Culling m_执行Culling）(偏移: 0xC)

### 方法 (1)

- `void InvokeOnPerformCulling(BatchRendererGroup group, ref BatchRendererCullingOutput context, ref LODParameters lodParameters)`
  （void InvokeOn执行Culling（Batch渲染器组 group, ref BatchRendererCullingOutput context, ref LODParameters lodParameters））

---

## BatchRendererGroup.OnPerformCulling（Batch渲染器Group.On执行Culling）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `JobHandle Invoke(BatchRendererGroup rendererGroup, BatchCullingContext cullingContext)`
  （Job句柄 Invoke（Batch渲染器组 rendererGroup, BatchCullingContext cullingContext））
- `IAsyncResult BeginInvoke(BatchRendererGroup rendererGroup, BatchCullingContext cullingContext, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（Batch渲染器组 rendererGroup, BatchCullingContext cullingContext, 异步回调 callback, object object））
- `JobHandle EndInvoke(IAsyncResult result)`
  （Job句柄 结束Invoke（I异步Result result））

---

## BatchVisibility（BatchVisibility）

### 字段 (3)

- `int offset`（int offset）(偏移: 0x0)
- `int instancesCount`（int instances数量）(偏移: 0x4)
- `int visibleCount`（int visible数量）(偏移: 0x8)

---

## BeforeRenderHelper（BeforeRender辅助器）

### 字段 (1)

- `List<BeforeRenderHelper.OrderBlock> s_OrderBlocks`（List<BeforeRenderHelper.OrderBlock> s_OrderBlocks）(偏移: 0x0)

### 方法 (1)

- `void Invoke()`
  （void 调用（））

---

## BeforeRenderHelper.OrderBlock（BeforeRenderHelper.OrderBlock）

### 字段 (2)

- `int order`（int order）(偏移: 0x0)
- `UnityAction callback`（Unity引擎动作 callback）(偏移: 0x4)

---

## Behaviour（行为）

**继承**: Component（组件）

### 方法 (3)

- `bool get_enabled()`
  （布尔值 获取_已启用（））
- `void set_enabled(bool value)`
  （void 设置_已启用（布尔值 value））
- `bool get_isActiveAndEnabled()`
  （bool get_is激活的And启用的（））

---

## BigInteger（BigInteger）

### 字段 (4)

- `uint length`（uint length）(偏移: 0x8)
- `uint[] data`（uint[] data）(偏移: 0xC)
- `uint[] smallPrimes`（uint[] smallPrimes）(偏移: 0x0)
- `RandomNumberGenerator rng`（随机NumberGenerator rng）(偏移: 0x4)

### 方法 (42)

- `BigInteger op_Implicit(uint value)`
  （BigInteger op_Implicit（uint value））
- `BigInteger op_Implicit(int value)`
  （BigInteger op_Implicit（int value））
- `BigInteger op_Subtraction(BigInteger bi1, BigInteger bi2)`
  （BigInteger op_Subtraction（BigInteger bi1, BigInteger bi2））
- `uint op_Modulus(BigInteger bi, uint ui)`
  （uint op_Modulus（BigInteger bi, uint ui））
- `BigInteger op_Modulus(BigInteger bi1, BigInteger bi2)`
  （BigInteger op_Modulus（BigInteger bi1, BigInteger bi2））
- `BigInteger op_Division(BigInteger bi1, BigInteger bi2)`
  （BigInteger op_Division（BigInteger bi1, BigInteger bi2））
- `BigInteger op_Multiply(BigInteger bi1, BigInteger bi2)`
  （BigInteger op_Multiply（BigInteger bi1, BigInteger bi2））
- `BigInteger op_Multiply(BigInteger bi, int i)`
  （BigInteger op_Multiply（BigInteger bi, int i））
- `BigInteger op_LeftShift(BigInteger bi1, int shiftVal)`
  （BigInteger op_左Shift（BigInteger bi1, int shiftVal））
- `BigInteger op_RightShift(BigInteger bi1, int shiftVal)`
  （BigInteger op_右Shift（BigInteger bi1, int shiftVal））
- `RandomNumberGenerator get_Rng()`
  （随机NumberGenerator get_Rng（））
- `BigInteger GenerateRandom(int bits, RandomNumberGenerator rng)`
  （BigInteger Generate随机（int bits, 随机NumberGenerator rng））
- `BigInteger GenerateRandom(int bits)`
  （BigInteger Generate随机（int bits））
- `void Randomize(RandomNumberGenerator rng)`
  （void Randomize（随机NumberGenerator rng））
- `void Randomize()`
  （void Randomize（））
- `int BitCount()`
  （int Bit数量（））
- `bool TestBit(uint bitNum)`
  （bool TestBit（uint bitNum））
- `bool TestBit(int bitNum)`
  （bool TestBit（int bitNum））
- `void SetBit(uint bitNum)`
  （void 集合Bit（uint bitNum））
- `void SetBit(uint bitNum, bool value)`
  （void 集合Bit（uint bitNum, bool value））
- `int LowestSetBit()`
  （int Lowest集合Bit（））
- `byte[] GetBytes()`
  （byte[] 获取Bytes（））
- `bool op_Equality(BigInteger bi1, uint ui)`
  （bool op_Equality（BigInteger bi1, uint ui））
- `bool op_Inequality(BigInteger bi1, uint ui)`
  （bool op_Inequality（BigInteger bi1, uint ui））
- `bool op_Equality(BigInteger bi1, BigInteger bi2)`
  （bool op_Equality（BigInteger bi1, BigInteger bi2））
- `bool op_Inequality(BigInteger bi1, BigInteger bi2)`
  （bool op_Inequality（BigInteger bi1, BigInteger bi2））
- `bool op_GreaterThan(BigInteger bi1, BigInteger bi2)`
  （bool op_GreaterThan（BigInteger bi1, BigInteger bi2））
- `bool op_LessThan(BigInteger bi1, BigInteger bi2)`
  （bool op_LessThan（BigInteger bi1, BigInteger bi2））
- `bool op_GreaterThanOrEqual(BigInteger bi1, BigInteger bi2)`
  （bool op_GreaterThanOrEqual（BigInteger bi1, BigInteger bi2））
- `bool op_LessThanOrEqual(BigInteger bi1, BigInteger bi2)`
  （bool op_LessThanOrEqual（BigInteger bi1, BigInteger bi2））
- `string ToString(uint radix)`
  （string To字符串（uint radix））
- `string ToString(uint radix, string characterSet)`
  （string To字符串（uint radix, string characterSet））
- `void Normalize()`
  （void Normalize（））
- `void Clear()`
  （void 清除（））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `string ToString()`
  （字符串 转字符串（））
- `bool Equals(object o)`
  （布尔值 等于（对象 o））
- `BigInteger ModInverse(BigInteger modulus)`
  （BigInteger ModInverse（BigInteger modulus））
- `BigInteger ModPow(BigInteger exp, BigInteger n)`
  （BigInteger ModPow（BigInteger exp, BigInteger n））
- `bool IsProbablePrime()`
  （bool 是否ProbablePrime（））
- `BigInteger GeneratePseudoPrime(int bits)`
  （BigInteger GeneratePseudoPrime（int bits））
- `void Incr2()`
  （void Incr2（））

---

## BigInteger.Kernel（BigInteger.Kernel）

### 方法 (15)

- `BigInteger Subtract(BigInteger big, BigInteger small)`
  （BigInteger Subtract（BigInteger big, BigInteger small））
- `void MinusEq(BigInteger big, BigInteger small)`
  （void MinusEq（BigInteger big, BigInteger small））
- `void PlusEq(BigInteger bi1, BigInteger bi2)`
  （void PlusEq（BigInteger bi1, BigInteger bi2））
- `BigInteger.Sign Compare(BigInteger bi1, BigInteger bi2)`
  （BigInteger.标志 Compare（BigInteger bi1, BigInteger bi2））
- `uint SingleByteDivideInPlace(BigInteger n, uint d)`
  （uint 单个ByteDivideInPlace（BigInteger n, uint d））
- `uint DwordMod(BigInteger n, uint d)`
  （uint DwordMod（BigInteger n, uint d））
- `BigInteger[] DwordDivMod(BigInteger n, uint d)`
  （BigInteger[] DwordDivMod（BigInteger n, uint d））
- `BigInteger[] multiByteDivide(BigInteger bi1, BigInteger bi2)`
  （BigInteger[] multiByteDivide（BigInteger bi1, BigInteger bi2））
- `BigInteger LeftShift(BigInteger bi, int n)`
  （BigInteger 左Shift（BigInteger bi, int n））
- `BigInteger RightShift(BigInteger bi, int n)`
  （BigInteger 右Shift（BigInteger bi, int n））
- `BigInteger MultiplyByDword(BigInteger n, uint f)`
  （BigInteger MultiplyByDword（BigInteger n, uint f））
- `void Multiply(uint[] x, uint xOffset, uint xLen, uint[] y, uint yOffset, uint yLen, uint[] d, uint dOffset)`
  （void Multiply（uint[] x, uint xOffset, uint xLen, uint[] y, uint yOffset, uint yLen, uint[] d, uint dOffset））
- `void MultiplyMod2p32pmod(uint[] x, int xOffset, int xLen, uint[] y, int yOffest, int yLen, uint[] d, int dOffset, int mod)`
  （void MultiplyMod2p32pmod（uint[] x, int xOffset, int xLen, uint[] y, int yOffest, int yLen, uint[] d, int dOffset, int mod））
- `uint modInverse(BigInteger bi, uint modulus)`
  （uint modInverse（BigInteger bi, uint modulus））
- `BigInteger modInverse(BigInteger bi, BigInteger modulus)`
  （BigInteger modInverse（BigInteger bi, BigInteger modulus））

---

## BigInteger.ModulusRing（BigInteger.ModulusRing）

### 字段 (2)

- `BigInteger mod`（BigInteger mod）(偏移: 0x8)
- `BigInteger constant`（BigInteger constant）(偏移: 0xC)

### 方法 (5)

- `void BarrettReduction(BigInteger x)`
  （void BarrettReduction（BigInteger x））
- `BigInteger Multiply(BigInteger a, BigInteger b)`
  （BigInteger Multiply（BigInteger a, BigInteger b））
- `BigInteger Difference(BigInteger a, BigInteger b)`
  （BigInteger Difference（BigInteger a, BigInteger b））
- `BigInteger Pow(BigInteger a, BigInteger k)`
  （BigInteger Pow（BigInteger a, BigInteger k））
- `BigInteger Pow(uint b, BigInteger exp)`
  （BigInteger Pow（uint b, BigInteger exp））

---

## BigInteger.Sign（BigInteger.标志）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## BinaryArray（Binary数组）

### 字段 (9)

- `int objectId`（整数 对象ID）(偏移: 0x8)
- `int rank`（int rank）(偏移: 0xC)
- `int[] lengthA`（int[] lengthA）(偏移: 0x10)
- `int[] lowerBoundA`（int[] lowerBoundA）(偏移: 0x14)
- `BinaryTypeEnum binaryTypeEnum`（Binary类型Enum binary类型Enum）(偏移: 0x18)
- `object typeInformation`（object typeInformation）(偏移: 0x1C)
- `int assemId`（整数 程序集ID）(偏移: 0x20)
- `BinaryHeaderEnum binaryHeaderEnum`（二进制头枚举 binary头枚举）(偏移: 0x24)
- `BinaryArrayTypeEnum binaryArrayTypeEnum`（Binary数组类型Enum binary数组类型Enum）(偏移: 0x28)

### 方法 (3)

- `void Set(int objectId, int rank, int[] lengthA, int[] lowerBoundA, BinaryTypeEnum binaryTypeEnum, object typeInformation, BinaryArrayTypeEnum binaryArrayTypeEnum, int assemId)`
  （void 集合（int objectId, int rank, int[] lengthA, int[] lowerBoundA, Binary类型Enum binaryTypeEnum, object typeInformation, Binary数组类型Enum binaryArrayTypeEnum, int assemId））
- `void Write(__BinaryWriter sout)`
  （void 写入（__二进制写入器 sout））
- `void Read(__BinaryParser input)`
  （void 读取（__二进制解析器 input））

---

## BinaryArrayTypeEnum（Binary数组类型Enum）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## BinaryAssembly（BinaryAssembly）

### 字段 (2)

- `int assemId`（整数 程序集ID）(偏移: 0x8)
- `string assemblyString`（字符串 程序集字符串）(偏移: 0xC)

### 方法 (4)

- `void Set(int assemId, string assemblyString)`
  （void 集合（int assemId, string assemblyString））
- `void Write(__BinaryWriter sout)`
  （void 写入（__二进制写入器 sout））
- `void Read(__BinaryParser input)`
  （void 读取（__二进制解析器 input））
- `void Dump()`
  （void 转储（））

---

## BinaryAssemblyInfo（BinaryAssembly信息）

### 字段 (2)

- `string assemblyString`（字符串 程序集字符串）(偏移: 0x8)
- `Assembly assembly`（Assembly assembly）(偏移: 0xC)

### 方法 (1)

- `Assembly GetAssembly()`
  （Assembly 获取Assembly（））

---

## BinaryCompatibility（BinaryCompatibility）

### 字段 (2)

- `bool TargetsAtLeast_Desktop_V4_5`（bool TargetsAtLeast_Desktop_V4_5）(偏移: 0x0)
- `bool TargetsAtLeast_Desktop_V4_5_1`（bool TargetsAtLeast_Desktop_V4_5_1）(偏移: 0x1)

---

## BinaryConverter（BinaryConverter）

### 方法 (5)

- `BinaryTypeEnum GetBinaryTypeInfo(Type type, WriteObjectInfo objectInfo, string typeName, ObjectWriter objectWriter, out object typeInformation, out int assemId)`
  （Binary类型Enum 获取Binary类型信息（类型 type, Write对象信息 objectInfo, string typeName, 对象写入器 objectWriter, out object typeInformation, out int assemId））
- `BinaryTypeEnum GetParserBinaryTypeInfo(Type type, out object typeInformation)`
  （Binary类型Enum 获取ParserBinary类型信息（类型 type, out object typeInformation））
- `void WriteTypeInfo(BinaryTypeEnum binaryTypeEnum, object typeInformation, int assemId, __BinaryWriter sout)`
  （void Write类型信息（Binary类型Enum binaryTypeEnum, object typeInformation, int assemId, __Binary写入器 sout））
- `object ReadTypeInfo(BinaryTypeEnum binaryTypeEnum, __BinaryParser input, out int assemId)`
  （object Read类型信息（Binary类型Enum binaryTypeEnum, __BinaryParser input, out int assemId））
- `void TypeFromInfo(BinaryTypeEnum binaryTypeEnum, object typeInformation, ObjectReader objectReader, BinaryAssemblyInfo assemblyInfo, out InternalPrimitiveTypeE primitiveTypeEnum, out string typeString, out Type type, out bool isVariant)`
  （void 类型From信息（Binary类型Enum binaryTypeEnum, object typeInformation, 对象读取器 objectReader, BinaryAssembly信息 assemblyInfo, out InternalPrimitiveTypeE primitiveTypeEnum, out string typeString, out Type type, out bool isVariant））

---

## BinaryCrossAppDomainAssembly（BinaryCrossAppDomainAssembly）

### 字段 (2)

- `int assemId`（整数 程序集ID）(偏移: 0x8)
- `int assemblyIndex`（int assembly索引）(偏移: 0xC)

### 方法 (2)

- `void Read(__BinaryParser input)`
  （void 读取（__二进制解析器 input））
- `void Dump()`
  （void 转储（））

---

## BinaryCrossAppDomainMap（BinaryCrossAppDomain映射）

### 字段 (1)

- `int crossAppDomainArrayIndex`（int crossAppDomain数组索引）(偏移: 0x8)

### 方法 (2)

- `void Read(__BinaryParser input)`
  （void 读取（__二进制解析器 input））
- `void Dump()`
  （void 转储（））

---

## BinaryCrossAppDomainString（BinaryCrossAppDomain字符串）

### 字段 (2)

- `int objectId`（整数 对象ID）(偏移: 0x8)
- `int value`（整数 value）(偏移: 0xC)

### 方法 (2)

- `void Read(__BinaryParser input)`
  （void 读取（__二进制解析器 input））
- `void Dump()`
  （void 转储（））

---

## BinaryFormatter（BinaryFormatter）

### 字段 (7)

- `ISurrogateSelector m_surrogates`（ISurrogateSelector m_surrogates）(偏移: 0x8)
- `StreamingContext m_context`（流上下文 m_上下文）(偏移: 0xC)
- `SerializationBinder m_binder`（SerializationBinder m_binder）(偏移: 0x14)
- `FormatterTypeStyle m_typeFormat`（Formatter类型Style m_type格式化）(偏移: 0x18)
- `FormatterAssemblyStyle m_assemblyFormat`（FormatterAssemblyStyle m_assembly格式化）(偏移: 0x1C)
- `TypeFilterLevel m_securityLevel`（类型Filter等级 m_security等级）(偏移: 0x20)
- `object[] m_crossAppDomainArray`（object[] m_crossAppDomain数组）(偏移: 0x24)

### 方法 (9)

- `void set_AssemblyFormat(FormatterAssemblyStyle value)`
  （void set_Assembly格式化（FormatterAssemblyStyle value））
- `void set_SurrogateSelector(ISurrogateSelector value)`
  （void set_SurrogateSelector（ISurrogateSelector value））
- `object Deserialize(Stream serializationStream)`
  （object Deserialize（流 serializationStream））
- `object Deserialize(Stream serializationStream, HeaderHandler handler, bool fCheck)`
  （object Deserialize（流 serializationStream, 标题处理器 handler, bool fCheck））
- `object Deserialize(Stream serializationStream, HeaderHandler handler)`
  （object Deserialize（流 serializationStream, 标题处理器 handler））
- `void Serialize(Stream serializationStream, object graph)`
  （void Serialize（流 serializationStream, object graph））
- `void Serialize(Stream serializationStream, object graph, Header[] headers)`
  （void Serialize（流 serializationStream, object graph, Header[] headers））
- `void Serialize(Stream serializationStream, object graph, Header[] headers, bool fCheck)`
  （void Serialize（流 serializationStream, object graph, Header[] headers, bool fCheck））
- `TypeInformation GetTypeInformation(Type type)`
  （类型Information 获取类型Information（类型 type））

---

## BinaryHeaderEnum（Binary标题Enum）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## BinaryHeap（BinaryHeap）

### 字段 (3)

- `int numberOfItems`（int numberOfItems）(偏移: 0x8)
- `float growthFactor`（float growth系数）(偏移: 0xC)
- `BinaryHeap.Tuple[] heap`（BinaryHeap.Tuple[] heap）(偏移: 0x10)

### 方法 (11)

- `bool get_isEmpty()`
  （布尔值 获取_是否为空（））
- `int RoundUpToNextMultipleMod1(int v)`
  （int 回合上To下一个MultipleMod1（int v））
- `void Clear()`
  （void 清除（））
- `PathNode GetNode(int i)`
  （路径节点 获取节点（int i））
- `void SetF(int i, uint f)`
  （void 集合F（int i, uint f））
- `void Expand()`
  （void Expand（））
- `void Add(PathNode node)`
  （void 添加（路径节点 node））
- `void DecreaseKey(BinaryHeap.Tuple node, ushort index)`
  （void Decrease键（BinaryHeap.Tuple node, ushort index））
- `PathNode Remove()`
  （路径节点 移除（））
- `void Validate()`
  （void 验证（））
- `void Rebuild()`
  （void Rebuild（））

---

## BinaryHeap.Tuple（BinaryHeap.Tuple）

### 字段 (2)

- `PathNode node`（路径节点 node）(偏移: 0x0)
- `uint F`（uint F）(偏移: 0x4)

---

## BinaryMethodCall（BinaryMethodCall）

### 字段 (7)

- `string methodName`（string method名称）(偏移: 0x8)
- `string typeName`（字符串 类型名称）(偏移: 0xC)
- `object[] args`（对象[] 参数）(偏移: 0x10)
- `object callContext`（object callContext）(偏移: 0x14)
- `Type[] argTypes`（Type[] argTypes）(偏移: 0x18)
- `bool bArgsPrimitive`（bool bArgsPrimitive）(偏移: 0x1C)
- `MessageEnum messageEnum`（MessageEnum messageEnum）(偏移: 0x20)

### 方法 (2)

- `void Write(__BinaryWriter sout)`
  （void 写入（__二进制写入器 sout））
- `void Dump()`
  （void 转储（））

---

## BinaryMethodReturn（BinaryMethodReturn）

### 字段 (8)

- `object returnValue`（object return值）(偏移: 0x8)
- `object[] args`（对象[] 参数）(偏移: 0xC)
- `object callContext`（object callContext）(偏移: 0x10)
- `Type[] argTypes`（Type[] argTypes）(偏移: 0x14)
- `bool bArgsPrimitive`（bool bArgsPrimitive）(偏移: 0x18)
- `MessageEnum messageEnum`（MessageEnum messageEnum）(偏移: 0x1C)
- `Type returnType`（类型 return类型）(偏移: 0x20)
- `object instanceOfVoid`（object instanceOfVoid）(偏移: 0x0)

### 方法 (2)

- `void Write(__BinaryWriter sout)`
  （void 写入（__二进制写入器 sout））
- `void Dump()`
  （void 转储（））

---

## BinaryObject（Binary对象）

### 字段 (2)

- `int objectId`（整数 对象ID）(偏移: 0x8)
- `int mapId`（int mapId）(偏移: 0xC)

### 方法 (4)

- `void Set(int objectId, int mapId)`
  （void 集合（int objectId, int mapId））
- `void Write(__BinaryWriter sout)`
  （void 写入（__二进制写入器 sout））
- `void Read(__BinaryParser input)`
  （void 读取（__二进制解析器 input））
- `void Dump()`
  （void 转储（））

---

## BinaryObjectString（Binary对象字符串）

### 字段 (2)

- `int objectId`（整数 对象ID）(偏移: 0x8)
- `string value`（string value）(偏移: 0xC)

### 方法 (4)

- `void Set(int objectId, string value)`
  （void 集合（int objectId, string value））
- `void Write(__BinaryWriter sout)`
  （void 写入（__二进制写入器 sout））
- `void Read(__BinaryParser input)`
  （void 读取（__二进制解析器 input））
- `void Dump()`
  （void 转储（））

---

## BinaryObjectWithMap（Binary对象With映射）

### 字段 (6)

- `BinaryHeaderEnum binaryHeaderEnum`（二进制头枚举 binary头枚举）(偏移: 0x8)
- `int objectId`（整数 对象ID）(偏移: 0xC)
- `string name`（字符串 名称）(偏移: 0x10)
- `int numMembers`（int numMembers）(偏移: 0x14)
- `string[] memberNames`（字符串[] 成员名称）(偏移: 0x18)
- `int assemId`（整数 程序集ID）(偏移: 0x1C)

### 方法 (4)

- `void Set(int objectId, string name, int numMembers, string[] memberNames, int assemId)`
  （void 集合（int objectId, string name, int numMembers, string[] memberNames, int assemId））
- `void Write(__BinaryWriter sout)`
  （void 写入（__二进制写入器 sout））
- `void Read(__BinaryParser input)`
  （void 读取（__二进制解析器 input））
- `void Dump()`
  （void 转储（））

---

## BinaryObjectWithMapTyped（Binary对象With映射Typed）

### 字段 (9)

- `BinaryHeaderEnum binaryHeaderEnum`（二进制头枚举 binary头枚举）(偏移: 0x8)
- `int objectId`（整数 对象ID）(偏移: 0xC)
- `string name`（字符串 名称）(偏移: 0x10)
- `int numMembers`（int numMembers）(偏移: 0x14)
- `string[] memberNames`（字符串[] 成员名称）(偏移: 0x18)
- `BinaryTypeEnum[] binaryTypeEnumA`（Binary类型Enum[] binary类型EnumA）(偏移: 0x1C)
- `object[] typeInformationA`（object[] typeInformationA）(偏移: 0x20)
- `int[] memberAssemIds`（int[] memberAssemIds）(偏移: 0x24)
- `int assemId`（整数 程序集ID）(偏移: 0x28)

### 方法 (3)

- `void Set(int objectId, string name, int numMembers, string[] memberNames, BinaryTypeEnum[] binaryTypeEnumA, object[] typeInformationA, int[] memberAssemIds, int assemId)`
  （void 集合（int objectId, string name, int numMembers, string[] memberNames, Binary类型Enum[] binaryTypeEnumA, object[] typeInformationA, int[] memberAssemIds, int assemId））
- `void Write(__BinaryWriter sout)`
  （void 写入（__二进制写入器 sout））
- `void Read(__BinaryParser input)`
  （void 读取（__二进制解析器 input））

---

## BinaryReader（Binary读取器）

**继承**: IDisposable（可释放接口）

### 字段 (10)

- `Stream m_stream`（流 m_stream）(偏移: 0x8)
- `byte[] m_buffer`（byte[] m_buffer）(偏移: 0xC)
- `Decoder m_decoder`（Decoder m_decoder）(偏移: 0x10)
- `byte[] m_charBytes`（byte[] m_charBytes）(偏移: 0x14)
- `char[] m_singleChar`（char[] m_singleChar）(偏移: 0x18)
- `char[] m_charBuffer`（char[] m_char缓冲区）(偏移: 0x1C)
- `int m_maxCharsSize`（int m_maxChars大小）(偏移: 0x20)
- `bool m_2BytesPerChar`（bool m_2BytesPerChar）(偏移: 0x24)
- `bool m_isMemoryStream`（bool m_isMemory流）(偏移: 0x25)
- `bool m_leaveOpen`（bool m_leave打开）(偏移: 0x26)

### 方法 (26)

- `Stream get_BaseStream()`
  （流 get_基础流（））
- `void Close()`
  （void 关闭（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `void Dispose()`
  （void 释放（））
- `int Read()`
  （整数 读取（））
- `bool ReadBoolean()`
  （bool ReadBoolean（））
- `byte ReadByte()`
  （byte ReadByte（））
- `sbyte ReadSByte()`
  （sbyte ReadSByte（））
- `char ReadChar()`
  （char ReadChar（））
- `short ReadInt16()`
  （short ReadInt16（））
- `ushort ReadUInt16()`
  （ushort ReadUInt16（））
- `int ReadInt32()`
  （int ReadInt32（））
- `uint ReadUInt32()`
  （uint ReadUInt32（））
- `long ReadInt64()`
  （long ReadInt64（））
- `ulong ReadUInt64()`
  （ulong ReadUInt64（））
- `float ReadSingle()`
  （float Read单个（））
- `double ReadDouble()`
  （double ReadDouble（））
- `Decimal ReadDecimal()`
  （Decimal ReadDecimal（））
- `string ReadString()`
  （string Read字符串（））
- `int InternalReadChars(char[] buffer, int index, int count)`
  （int 内部的ReadChars（char[] buffer, int index, int count））
- `int InternalReadOneChar()`
  （int 内部的ReadOneChar（））
- `char[] ReadChars(int count)`
  （char[] ReadChars（int count））
- `int Read(byte[] buffer, int index, int count)`
  （int Read（byte[] buffer, int index, int count））
- `byte[] ReadBytes(int count)`
  （byte[] ReadBytes（int count））
- `void FillBuffer(int numBytes)`
  （void Fill缓冲区（int numBytes））
- `int Read7BitEncodedInt()`
  （int Read7BitEncoded整数（））

---

## BinaryTypeEnum（Binary类型Enum）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## BinaryWriter（Binary写入器）

**继承**: IDisposable（可释放接口）

### 字段 (8)

- `BinaryWriter Null`（Binary写入器 Null）(偏移: 0x0)
- `Stream OutStream`（流 Out流）(偏移: 0x8)
- `byte[] _buffer`（字节[] _缓冲区）(偏移: 0xC)
- `Encoding _encoding`（Encoding _encoding）(偏移: 0x10)
- `Encoder _encoder`（Encoder _encoder）(偏移: 0x14)
- `bool _leaveOpen`（布尔值 _保持打开）(偏移: 0x18)
- `byte[] _largeByteBuffer`（byte[] _largeByte缓冲区）(偏移: 0x1C)
- `int _maxChars`（int _maxChars）(偏移: 0x20)

### 方法 (20)

- `void Close()`
  （void 关闭（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `void Dispose()`
  （void 释放（））
- `void Flush()`
  （void 刷新（））
- `void Write(bool value)`
  （void Write（bool value））
- `void Write(byte value)`
  （void Write（byte value））
- `void Write(byte[] buffer)`
  （void Write（byte[] buffer））
- `void Write(byte[] buffer, int index, int count)`
  （void Write（byte[] buffer, int index, int count））
- `void Write(char ch)`
  （void Write（char ch））
- `void Write(char[] chars)`
  （void Write（char[] chars））
- `void Write(double value)`
  （void Write（double value））
- `void Write(short value)`
  （void Write（short value））
- `void Write(ushort value)`
  （void Write（ushort value））
- `void Write(int value)`
  （void Write（int value））
- `void Write(uint value)`
  （void Write（uint value））
- `void Write(long value)`
  （void Write（long value））
- `void Write(ulong value)`
  （void Write（ulong value））
- `void Write(float value)`
  （void Write（float value））
- `void Write(string value)`
  （void 写入（字符串 value））
- `void Write7BitEncodedInt(int value)`
  （void Write7BitEncoded整数（int value））

---

## BindingFlags（BindingFlags）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## BipedIK（BipedIK）

**继承**: SolverManager（求解器管理器）

### 字段 (2)

- `BipedReferences references`（BipedReferences references）(偏移: 0x1C)
- `BipedIKSolvers solvers`（BipedIKSolvers solvers）(偏移: 0x20)

### 方法 (24)

- `void OpenUserManual()`
  （void 打开用户手动（））
- `void OpenScriptReference()`
  （void 打开脚本引用（））
- `void SupportGroup()`
  （void 支持组（））
- `void ASThread()`
  （void 异步线程（））
- `float GetIKPositionWeight(AvatarIKGoal goal)`
  （float 获取IKPositionWeight（AvatarIKGoal goal））
- `float GetIKRotationWeight(AvatarIKGoal goal)`
  （float 获取IKRotationWeight（AvatarIKGoal goal））
- `void SetIKPositionWeight(AvatarIKGoal goal, float weight)`
  （void 集合IKPositionWeight（AvatarIKGoal goal, float weight））
- `void SetIKRotationWeight(AvatarIKGoal goal, float weight)`
  （void 集合IKRotationWeight（AvatarIKGoal goal, float weight））
- `void SetIKPosition(AvatarIKGoal goal, Vector3 IKPosition)`
  （void 集合IKPosition（AvatarIKGoal goal, 三维向量 IKPosition））
- `void SetIKRotation(AvatarIKGoal goal, Quaternion IKRotation)`
  （void 集合IKRotation（AvatarIKGoal goal, Quaternion IKRotation））
- `Vector3 GetIKPosition(AvatarIKGoal goal)`
  （三维向量 获取IKPosition（AvatarIKGoal goal））
- `Quaternion GetIKRotation(AvatarIKGoal goal)`
  （Quaternion 获取IKRotation（AvatarIKGoal goal））
- `void SetLookAtWeight(float weight, float bodyWeight, float headWeight, float eyesWeight, float clampWeight, float clampWeightHead, float clampWeightEyes)`
  （void 集合LookAtWeight（float weight, float bodyWeight, float headWeight, float eyesWeight, float clampWeight, float clampWeightHead, float clampWeightEyes））
- `void SetLookAtPosition(Vector3 lookAtPosition)`
  （void 集合LookAtPosition（三维向量 lookAtPosition））
- `void SetSpinePosition(Vector3 spinePosition)`
  （void 集合SpinePosition（三维向量 spinePosition））
- `void SetSpineWeight(float weight)`
  （void 集合SpineWeight（float weight））
- `IKSolverLimb GetGoalIK(AvatarIKGoal goal)`
  （IKSolverLimb 获取GoalIK（AvatarIKGoal goal））
- `void InitiateBipedIK()`
  （void InitiateBipedIK（））
- `void UpdateBipedIK()`
  （void 更新BipedIK（））
- `void SetToDefaults()`
  （void 集合ToDefaults（））
- `void FixTransforms()`
  （void 修复变换（））
- `void InitiateSolver()`
  （void 启动求解器（））
- `void UpdateSolver()`
  （void 更新求解器（））
- `void LogWarning(string message)`
  （void 记录警告（字符串 message））

---

## BipedIKSolvers（BipedIKSolvers）

### 字段 (10)

- `IKSolverLimb leftFoot`（IKSolverLimb left脚部）(偏移: 0x8)
- `IKSolverLimb rightFoot`（IKSolverLimb right脚部）(偏移: 0xC)
- `IKSolverLimb leftHand`（IKSolverLimb left手部）(偏移: 0x10)
- `IKSolverLimb rightHand`（IKSolverLimb right手部）(偏移: 0x14)
- `IKSolverFABRIK spine`（IKSolverFABRIK spine）(偏移: 0x18)
- `IKSolverLookAt lookAt`（IKSolverLookAt lookAt）(偏移: 0x1C)
- `IKSolverAim aim`（IKSolverAim aim）(偏移: 0x20)
- `Constraints pelvis`（Constraints pelvis）(偏移: 0x24)
- `IKSolverLimb[] _limbs`（IKSolverLimb[] _limbs）(偏移: 0x28)
- `IKSolver[] _ikSolvers`（IKSolver[] _ikSolvers）(偏移: 0x2C)

### 方法 (3)

- `IKSolverLimb[] get_limbs()`
  （IKSolverLimb[] get_limbs（））
- `IKSolver[] get_ikSolvers()`
  （IKSolver[] get_ikSolvers（））
- `void AssignReferences(BipedReferences references)`
  （void AssignReferences（BipedReferences references））

---

## BipedLimbOrientations（BipedLimbOrientations）

### 字段 (4)

- `BipedLimbOrientations.LimbOrientation leftArm`（BipedLimbOrientations.LimbOrientation left手臂）(偏移: 0x8)
- `BipedLimbOrientations.LimbOrientation rightArm`（BipedLimbOrientations.LimbOrientation right手臂）(偏移: 0xC)
- `BipedLimbOrientations.LimbOrientation leftLeg`（BipedLimbOrientations.LimbOrientation left腿部）(偏移: 0x10)
- `BipedLimbOrientations.LimbOrientation rightLeg`（BipedLimbOrientations.LimbOrientation right腿部）(偏移: 0x14)

### 方法 (2)

- `BipedLimbOrientations get_UMA()`
  （BipedLimbOrientations get_UMA（））
- `BipedLimbOrientations get_MaxBiped()`
  （BipedLimbOrientations get_最大Biped（））

---

## BipedLimbOrientations.LimbOrientation（BipedLimbOrientations.LimbOrientation）

### 字段 (3)

- `Vector3 upperBoneForwardAxis`（三维向量 upperBone前进轴）(偏移: 0x8)
- `Vector3 lowerBoneForwardAxis`（三维向量 lowerBone前进轴）(偏移: 0x14)
- `Vector3 lastBoneLeftAxis`（三维向量 lastBone左轴）(偏移: 0x20)

---

## BipedNaming（BipedNaming）

### 字段 (18)

- `string[] typeLeft`（string[] type左）(偏移: 0x0)
- `string[] typeRight`（string[] type右）(偏移: 0x4)
- `string[] typeSpine`（string[] typeSpine）(偏移: 0x8)
- `string[] typeHead`（string[] type头部）(偏移: 0xC)
- `string[] typeArm`（string[] type手臂）(偏移: 0x10)
- `string[] typeLeg`（string[] type腿部）(偏移: 0x14)
- `string[] typeTail`（string[] typeTail）(偏移: 0x18)
- `string[] typeEye`（string[] typeEye）(偏移: 0x1C)
- `string[] typeExclude`（string[] typeExclude）(偏移: 0x20)
- `string[] typeExcludeSpine`（string[] typeExcludeSpine）(偏移: 0x24)
- `string[] typeExcludeHead`（string[] typeExclude头部）(偏移: 0x28)
- `string[] typeExcludeArm`（string[] typeExclude手臂）(偏移: 0x2C)
- `string[] typeExcludeLeg`（string[] typeExclude腿部）(偏移: 0x30)
- `string[] typeExcludeTail`（string[] typeExcludeTail）(偏移: 0x34)
- `string[] typeExcludeEye`（string[] typeExcludeEye）(偏移: 0x38)
- `string[] pelvis`（string[] pelvis）(偏移: 0x3C)
- `string[] hand`（string[] hand）(偏移: 0x40)
- `string[] foot`（string[] foot）(偏移: 0x44)

### 方法 (23)

- `Transform[] GetBonesOfType(BipedNaming.BoneType boneType, Transform[] bones)`
  （Transform[] 获取BonesOf类型（BipedNaming.Bone类型 boneType, Transform[] bones））
- `Transform[] GetBonesOfSide(BipedNaming.BoneSide boneSide, Transform[] bones)`
  （Transform[] 获取BonesOf侧面（BipedNaming.Bone侧面 boneSide, Transform[] bones））
- `Transform[] GetBonesOfTypeAndSide(BipedNaming.BoneType boneType, BipedNaming.BoneSide boneSide, Transform[] bones)`
  （Transform[] 获取BonesOf类型And侧面（BipedNaming.Bone类型 boneType, BipedNaming.Bone侧面 boneSide, Transform[] bones））
- `Transform GetFirstBoneOfTypeAndSide(BipedNaming.BoneType boneType, BipedNaming.BoneSide boneSide, Transform[] bones)`
  （变换 获取第一个BoneOf类型And侧面（BipedNaming.Bone类型 boneType, BipedNaming.Bone侧面 boneSide, Transform[] bones））
- `Transform GetNamingMatch(Transform[] transforms, string[][] namings)`
  （变换 获取Naming比赛（Transform[] transforms, string[][] namings））
- `BipedNaming.BoneType GetBoneType(string boneName)`
  （BipedNaming.Bone类型 获取Bone类型（string boneName））
- `BipedNaming.BoneSide GetBoneSide(string boneName)`
  （BipedNaming.Bone侧面 获取Bone侧面（string boneName））
- `Transform GetBone(Transform[] transforms, BipedNaming.BoneType boneType, BipedNaming.BoneSide boneSide = 0, string[][] namings)`
  （变换 获取Bone（Transform[] transforms, BipedNaming.Bone类型 boneType, BipedNaming.Bone侧面 boneSide = 0, string[][] namings））
- `bool isLeft(string boneName)`
  （bool is左（string boneName））
- `bool isRight(string boneName)`
  （bool is右（string boneName））
- `bool isSpine(string boneName)`
  （bool isSpine（string boneName））
- `bool isHead(string boneName)`
  （bool is头部（string boneName））
- `bool isArm(string boneName)`
  （bool is手臂（string boneName））
- `bool isLeg(string boneName)`
  （bool is腿部（string boneName））
- `bool isTail(string boneName)`
  （bool isTail（string boneName））
- `bool isEye(string boneName)`
  （bool isEye（string boneName））
- `bool isTypeExclude(string boneName)`
  （bool is类型Exclude（string boneName））
- `bool matchesNaming(string boneName, string[] namingConvention)`
  （bool matchesNaming（string boneName, string[] namingConvention））
- `bool excludesNaming(string boneName, string[] namingConvention)`
  （bool excludesNaming（string boneName, string[] namingConvention））
- `bool matchesLastLetter(string boneName, string[] namingConvention)`
  （bool matches最后一个Letter（string boneName, string[] namingConvention））
- `bool LastLetterIs(string boneName, string letter)`
  （bool 最后一个Letter是否（string boneName, string letter））
- `string firstLetter(string boneName)`
  （string firstLetter（string boneName））
- `string lastLetter(string boneName)`
  （string lastLetter（string boneName））

---

## BipedNaming.BoneSide（BipedNaming.Bone侧面）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## BipedNaming.BoneType（BipedNaming.Bone类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## BipedReferences（BipedReferences）

### 字段 (17)

- `Transform root`（变换 根节点）(偏移: 0x8)
- `Transform pelvis`（变换 骨盆）(偏移: 0xC)
- `Transform leftThigh`（变换 leftThigh）(偏移: 0x10)
- `Transform leftCalf`（变换 leftCalf）(偏移: 0x14)
- `Transform leftFoot`（变换 left脚部）(偏移: 0x18)
- `Transform rightThigh`（变换 rightThigh）(偏移: 0x1C)
- `Transform rightCalf`（变换 rightCalf）(偏移: 0x20)
- `Transform rightFoot`（变换 right脚部）(偏移: 0x24)
- `Transform leftUpperArm`（变换 left上半身手臂）(偏移: 0x28)
- `Transform leftForearm`（变换 leftForearm）(偏移: 0x2C)
- `Transform leftHand`（变换 left手部）(偏移: 0x30)
- `Transform rightUpperArm`（变换 right上半身手臂）(偏移: 0x34)
- `Transform rightForearm`（变换 rightForearm）(偏移: 0x38)
- `Transform rightHand`（变换 right手部）(偏移: 0x3C)
- `Transform head`（变换 头部）(偏移: 0x40)
- `Transform[] spine`（Transform[] spine）(偏移: 0x44)
- `Transform[] eyes`（Transform[] eyes）(偏移: 0x48)

### 方法 (23)

- `bool get_isFilled()`
  （bool get_isFilled（））
- `bool get_isEmpty()`
  （布尔值 获取_是否为空（））
- `bool IsEmpty(bool includeRoot)`
  （bool 是否空（bool includeRoot））
- `bool Contains(Transform t, bool ignoreRoot = False)`
  （bool Contains（变换 t, bool ignoreRoot = False））
- `bool AutoDetectReferences(ref BipedReferences references, Transform root, BipedReferences.AutoDetectParams autoDetectParams)`
  （bool 自动DetectReferences（ref BipedReferences references, 变换 root, BipedReferences.自动DetectParams autoDetectParams））
- `void DetectReferencesByNaming(ref BipedReferences references, Transform root, BipedReferences.AutoDetectParams autoDetectParams)`
  （void DetectReferencesByNaming（ref BipedReferences references, 变换 root, BipedReferences.自动DetectParams autoDetectParams））
- `void AssignHumanoidReferences(ref BipedReferences references, Animator animator, BipedReferences.AutoDetectParams autoDetectParams)`
  （void AssignHumanoidReferences（ref BipedReferences references, 动画器 animator, BipedReferences.自动DetectParams autoDetectParams））
- `bool SetupError(BipedReferences references, ref string errorMessage)`
  （bool SetupError（BipedReferences references, ref string errorMessage））
- `bool SetupWarning(BipedReferences references, ref string warningMessage)`
  （bool SetupWarning（BipedReferences references, ref string warningMessage））
- `bool IsNeckBone(Transform bone, Transform leftUpperArm)`
  （bool 是否颈部Bone（变换 bone, 变换 leftUpperArm））
- `bool AddBoneToEyes(Transform bone, ref BipedReferences references, BipedReferences.AutoDetectParams autoDetectParams)`
  （bool 添加BoneToEyes（变换 bone, ref BipedReferences references, BipedReferences.自动DetectParams autoDetectParams））
- `bool AddBoneToSpine(Transform bone, ref BipedReferences references, BipedReferences.AutoDetectParams autoDetectParams)`
  （bool 添加BoneToSpine（变换 bone, ref BipedReferences references, BipedReferences.自动DetectParams autoDetectParams））
- `void DetectLimb(BipedNaming.BoneType boneType, BipedNaming.BoneSide boneSide, ref Transform firstBone, ref Transform secondBone, ref Transform lastBone, Transform[] transforms)`
  （void DetectLimb（BipedNaming.Bone类型 boneType, BipedNaming.Bone侧面 boneSide, ref Transform firstBone, ref Transform secondBone, ref Transform lastBone, Transform[] transforms））
- `void AddBoneToHierarchy(ref Transform[] bones, Transform transform)`
  （void 添加BoneToHierarchy（ref Transform[] bones, 变换 transform））
- `bool LimbError(Transform bone1, Transform bone2, Transform bone3, ref string errorMessage)`
  （bool LimbError（变换 bone1, 变换 bone2, 变换 bone3, ref string errorMessage））
- `bool LimbWarning(Transform bone1, Transform bone2, Transform bone3, ref string warningMessage)`
  （bool LimbWarning（变换 bone1, 变换 bone2, 变换 bone3, ref string warningMessage））
- `bool SpineError(BipedReferences references, ref string errorMessage)`
  （bool SpineError（BipedReferences references, ref string errorMessage））
- `bool SpineWarning(BipedReferences references, ref string warningMessage)`
  （bool SpineWarning（BipedReferences references, ref string warningMessage））
- `bool EyesError(BipedReferences references, ref string errorMessage)`
  （bool EyesError（BipedReferences references, ref string errorMessage））
- `bool EyesWarning(BipedReferences references, ref string warningMessage)`
  （bool EyesWarning（BipedReferences references, ref string warningMessage））
- `bool RootHeightWarning(BipedReferences references, ref string warningMessage)`
  （bool 根高度Warning（BipedReferences references, ref string warningMessage））
- `bool FacingAxisWarning(BipedReferences references, ref string warningMessage)`
  （bool Facing轴Warning（BipedReferences references, ref string warningMessage））
- `float GetVerticalOffset(Vector3 p1, Vector3 p2, Quaternion rotation)`
  （float 获取垂直Offset（三维向量 p1, 三维向量 p2, Quaternion rotation））

---

## BipedReferences.AutoDetectParams（BipedReferences.自动DetectParams）

### 字段 (2)

- `bool legsParentInSpine`（bool legs父级InSpine）(偏移: 0x0)
- `bool includeEyes`（bool includeEyes）(偏移: 0x1)

### 方法 (1)

- `BipedReferences.AutoDetectParams get_Default()`
  （BipedReferences.自动DetectParams get_默认的（））

---

## BitArray（Bit数组）

**继承**: IDisposable（可释放接口）

### 字段 (3)

- `NativeArray<uint> m_Mem`（NativeArray<uint> m_Mem）(偏移: 0x0)
- `int m_BitCount`（int m_Bit数量）(偏移: 0xC)
- `int m_IntCount`（int m_整数数量）(偏移: 0x10)

### 方法 (4)

- `void Dispose()`
  （void 释放（））
- `void Clear()`
  （void 清除（））
- `bool IsSet(int bitIndex)`
  （bool 是否集合（int bitIndex））
- `void Set(int bitIndex, bool val)`
  （void 集合（int bitIndex, bool val））

---

## BitArray128（BitArray128）

**继承**: IBitArray（IBit数组）

### 字段 (2)

- `ulong data1`（ulong data1）(偏移: 0x0)
- `ulong data2`（ulong data2）(偏移: 0x8)

### 方法 (16)

- `uint get_capacity()`
  （无符号整数 获取_容量（））
- `bool get_allFalse()`
  （布尔值 获取_全假（））
- `bool get_allTrue()`
  （布尔值 获取_全真（））
- `string get_humanizedData()`
  （字符串 获取_人性化数据（））
- `bool get_Item(uint index)`
  （布尔值 获取_项（无符号整数 index））
- `void set_Item(uint index, bool value)`
  （void 设置_项（无符号整数 index, 布尔值 value））
- `BitArray128 op_OnesComplement(BitArray128 a)`
  （BitArray128 op_OnesComplement（BitArray128 a））
- `BitArray128 op_BitwiseOr(BitArray128 a, BitArray128 b)`
  （BitArray128 op_BitwiseOr（BitArray128 a, BitArray128 b））
- `BitArray128 op_BitwiseAnd(BitArray128 a, BitArray128 b)`
  （BitArray128 op_BitwiseAnd（BitArray128 a, BitArray128 b））
- `IBitArray BitAnd(IBitArray other)`
  （IBit数组 位与（IBit数组 other））
- `IBitArray BitOr(IBitArray other)`
  （IBit数组 位或（IBit数组 other））
- `IBitArray BitNot()`
  （IBit数组 位非（））
- `bool op_Equality(BitArray128 a, BitArray128 b)`
  （bool op_Equality（BitArray128 a, BitArray128 b））
- `bool op_Inequality(BitArray128 a, BitArray128 b)`
  （bool op_Inequality（BitArray128 a, BitArray128 b））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## BitArray16（BitArray16）

**继承**: IBitArray（IBit数组）

### 字段 (1)

- `ushort data`（ushort data）(偏移: 0x0)

### 方法 (16)

- `uint get_capacity()`
  （无符号整数 获取_容量（））
- `bool get_allFalse()`
  （布尔值 获取_全假（））
- `bool get_allTrue()`
  （布尔值 获取_全真（））
- `string get_humanizedData()`
  （字符串 获取_人性化数据（））
- `bool get_Item(uint index)`
  （布尔值 获取_项（无符号整数 index））
- `void set_Item(uint index, bool value)`
  （void 设置_项（无符号整数 index, 布尔值 value））
- `BitArray16 op_OnesComplement(BitArray16 a)`
  （BitArray16 op_OnesComplement（BitArray16 a））
- `BitArray16 op_BitwiseOr(BitArray16 a, BitArray16 b)`
  （BitArray16 op_BitwiseOr（BitArray16 a, BitArray16 b））
- `BitArray16 op_BitwiseAnd(BitArray16 a, BitArray16 b)`
  （BitArray16 op_BitwiseAnd（BitArray16 a, BitArray16 b））
- `IBitArray BitAnd(IBitArray other)`
  （IBit数组 位与（IBit数组 other））
- `IBitArray BitOr(IBitArray other)`
  （IBit数组 位或（IBit数组 other））
- `IBitArray BitNot()`
  （IBit数组 位非（））
- `bool op_Equality(BitArray16 a, BitArray16 b)`
  （bool op_Equality（BitArray16 a, BitArray16 b））
- `bool op_Inequality(BitArray16 a, BitArray16 b)`
  （bool op_Inequality（BitArray16 a, BitArray16 b））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## BitArray256（BitArray256）

**继承**: IBitArray（IBit数组）

### 字段 (4)

- `ulong data1`（ulong data1）(偏移: 0x0)
- `ulong data2`（ulong data2）(偏移: 0x8)
- `ulong data3`（ulong data3）(偏移: 0x10)
- `ulong data4`（ulong data4）(偏移: 0x18)

### 方法 (16)

- `uint get_capacity()`
  （无符号整数 获取_容量（））
- `bool get_allFalse()`
  （布尔值 获取_全假（））
- `bool get_allTrue()`
  （布尔值 获取_全真（））
- `string get_humanizedData()`
  （字符串 获取_人性化数据（））
- `bool get_Item(uint index)`
  （布尔值 获取_项（无符号整数 index））
- `void set_Item(uint index, bool value)`
  （void 设置_项（无符号整数 index, 布尔值 value））
- `BitArray256 op_OnesComplement(BitArray256 a)`
  （BitArray256 op_OnesComplement（BitArray256 a））
- `BitArray256 op_BitwiseOr(BitArray256 a, BitArray256 b)`
  （BitArray256 op_BitwiseOr（BitArray256 a, BitArray256 b））
- `BitArray256 op_BitwiseAnd(BitArray256 a, BitArray256 b)`
  （BitArray256 op_BitwiseAnd（BitArray256 a, BitArray256 b））
- `IBitArray BitAnd(IBitArray other)`
  （IBit数组 位与（IBit数组 other））
- `IBitArray BitOr(IBitArray other)`
  （IBit数组 位或（IBit数组 other））
- `IBitArray BitNot()`
  （IBit数组 位非（））
- `bool op_Equality(BitArray256 a, BitArray256 b)`
  （bool op_Equality（BitArray256 a, BitArray256 b））
- `bool op_Inequality(BitArray256 a, BitArray256 b)`
  （bool op_Inequality（BitArray256 a, BitArray256 b））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## BitArray32（BitArray32）

**继承**: IBitArray（IBit数组）

### 字段 (1)

- `uint data`（uint data）(偏移: 0x0)

### 方法 (17)

- `uint get_capacity()`
  （无符号整数 获取_容量（））
- `bool get_allFalse()`
  （布尔值 获取_全假（））
- `bool get_allTrue()`
  （布尔值 获取_全真（））
- `string get_humanizedVersion()`
  （string get_humanizedVersion（））
- `string get_humanizedData()`
  （字符串 获取_人性化数据（））
- `bool get_Item(uint index)`
  （布尔值 获取_项（无符号整数 index））
- `void set_Item(uint index, bool value)`
  （void 设置_项（无符号整数 index, 布尔值 value））
- `IBitArray BitAnd(IBitArray other)`
  （IBit数组 位与（IBit数组 other））
- `IBitArray BitOr(IBitArray other)`
  （IBit数组 位或（IBit数组 other））
- `IBitArray BitNot()`
  （IBit数组 位非（））
- `BitArray32 op_OnesComplement(BitArray32 a)`
  （BitArray32 op_OnesComplement（BitArray32 a））
- `BitArray32 op_BitwiseOr(BitArray32 a, BitArray32 b)`
  （BitArray32 op_BitwiseOr（BitArray32 a, BitArray32 b））
- `BitArray32 op_BitwiseAnd(BitArray32 a, BitArray32 b)`
  （BitArray32 op_BitwiseAnd（BitArray32 a, BitArray32 b））
- `bool op_Equality(BitArray32 a, BitArray32 b)`
  （bool op_Equality（BitArray32 a, BitArray32 b））
- `bool op_Inequality(BitArray32 a, BitArray32 b)`
  （bool op_Inequality（BitArray32 a, BitArray32 b））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## BitArray64（BitArray64）

**继承**: IBitArray（IBit数组）

### 字段 (1)

- `ulong data`（ulong data）(偏移: 0x0)

### 方法 (16)

- `uint get_capacity()`
  （无符号整数 获取_容量（））
- `bool get_allFalse()`
  （布尔值 获取_全假（））
- `bool get_allTrue()`
  （布尔值 获取_全真（））
- `string get_humanizedData()`
  （字符串 获取_人性化数据（））
- `bool get_Item(uint index)`
  （布尔值 获取_项（无符号整数 index））
- `void set_Item(uint index, bool value)`
  （void 设置_项（无符号整数 index, 布尔值 value））
- `BitArray64 op_OnesComplement(BitArray64 a)`
  （BitArray64 op_OnesComplement（BitArray64 a））
- `BitArray64 op_BitwiseOr(BitArray64 a, BitArray64 b)`
  （BitArray64 op_BitwiseOr（BitArray64 a, BitArray64 b））
- `BitArray64 op_BitwiseAnd(BitArray64 a, BitArray64 b)`
  （BitArray64 op_BitwiseAnd（BitArray64 a, BitArray64 b））
- `IBitArray BitAnd(IBitArray other)`
  （IBit数组 位与（IBit数组 other））
- `IBitArray BitOr(IBitArray other)`
  （IBit数组 位或（IBit数组 other））
- `IBitArray BitNot()`
  （IBit数组 位非（））
- `bool op_Equality(BitArray64 a, BitArray64 b)`
  （bool op_Equality（BitArray64 a, BitArray64 b））
- `bool op_Inequality(BitArray64 a, BitArray64 b)`
  （bool op_Inequality（BitArray64 a, BitArray64 b））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## BitArray8（BitArray8）

**继承**: IBitArray（IBit数组）

### 字段 (1)

- `byte data`（byte data）(偏移: 0x0)

### 方法 (16)

- `uint get_capacity()`
  （无符号整数 获取_容量（））
- `bool get_allFalse()`
  （布尔值 获取_全假（））
- `bool get_allTrue()`
  （布尔值 获取_全真（））
- `string get_humanizedData()`
  （字符串 获取_人性化数据（））
- `bool get_Item(uint index)`
  （布尔值 获取_项（无符号整数 index））
- `void set_Item(uint index, bool value)`
  （void 设置_项（无符号整数 index, 布尔值 value））
- `BitArray8 op_OnesComplement(BitArray8 a)`
  （BitArray8 op_OnesComplement（BitArray8 a））
- `BitArray8 op_BitwiseOr(BitArray8 a, BitArray8 b)`
  （BitArray8 op_BitwiseOr（BitArray8 a, BitArray8 b））
- `BitArray8 op_BitwiseAnd(BitArray8 a, BitArray8 b)`
  （BitArray8 op_BitwiseAnd（BitArray8 a, BitArray8 b））
- `IBitArray BitAnd(IBitArray other)`
  （IBit数组 位与（IBit数组 other））
- `IBitArray BitOr(IBitArray other)`
  （IBit数组 位或（IBit数组 other））
- `IBitArray BitNot()`
  （IBit数组 位非（））
- `bool op_Equality(BitArray8 a, BitArray8 b)`
  （bool op_Equality（BitArray8 a, BitArray8 b））
- `bool op_Inequality(BitArray8 a, BitArray8 b)`
  （bool op_Inequality（BitArray8 a, BitArray8 b））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## BitArrayUtilities（Bit数组Utilities）

### 方法 (12)

- `bool Get8(uint index, byte data)`
  （bool Get8（uint index, byte data））
- `bool Get16(uint index, ushort data)`
  （bool Get16（uint index, ushort data））
- `bool Get32(uint index, uint data)`
  （bool Get32（uint index, uint data））
- `bool Get64(uint index, ulong data)`
  （bool Get64（uint index, ulong data））
- `bool Get128(uint index, ulong data1, ulong data2)`
  （bool Get128（uint index, ulong data1, ulong data2））
- `bool Get256(uint index, ulong data1, ulong data2, ulong data3, ulong data4)`
  （bool Get256（uint index, ulong data1, ulong data2, ulong data3, ulong data4））
- `void Set8(uint index, ref byte data, bool value)`
  （void Set8（uint index, ref byte data, bool value））
- `void Set16(uint index, ref ushort data, bool value)`
  （void Set16（uint index, ref ushort data, bool value））
- `void Set32(uint index, ref uint data, bool value)`
  （void Set32（uint index, ref uint data, bool value））
- `void Set64(uint index, ref ulong data, bool value)`
  （void Set64（uint index, ref ulong data, bool value））
- `void Set128(uint index, ref ulong data1, ref ulong data2, bool value)`
  （void Set128（uint index, ref ulong data1, ref ulong data2, bool value））
- `void Set256(uint index, ref ulong data1, ref ulong data2, ref ulong data3, ref ulong data4, bool value)`
  （void Set256（uint index, ref ulong data1, ref ulong data2, ref ulong data3, ref ulong data4, bool value））

---

## BitConverter（BitConverter）

### 字段 (1)

- `bool IsLittleEndian`（bool 是否LittleEndian）(偏移: 0x0)

### 方法 (24)

- `bool AmILittleEndian()`
  （bool AmILittleEndian（））
- `byte[] GetBytes(bool value)`
  （byte[] 获取Bytes（bool value））
- `byte[] GetBytes(short value)`
  （byte[] 获取Bytes（short value））
- `byte[] GetBytes(int value)`
  （byte[] 获取Bytes（int value））
- `byte[] GetBytes(long value)`
  （byte[] 获取Bytes（long value））
- `byte[] GetBytes(ushort value)`
  （byte[] 获取Bytes（ushort value））
- `byte[] GetBytes(uint value)`
  （byte[] 获取Bytes（uint value））
- `byte[] GetBytes(ulong value)`
  （byte[] 获取Bytes（ulong value））
- `byte[] GetBytes(float value)`
  （byte[] 获取Bytes（float value））
- `byte[] GetBytes(double value)`
  （byte[] 获取Bytes（double value））
- `short ToInt16(byte[] value, int startIndex)`
  （short ToInt16（byte[] value, int startIndex））
- `int ToInt32(byte[] value, int startIndex)`
  （int ToInt32（byte[] value, int startIndex））
- `long ToInt64(byte[] value, int startIndex)`
  （long ToInt64（byte[] value, int startIndex））
- `ushort ToUInt16(byte[] value, int startIndex)`
  （ushort ToUInt16（byte[] value, int startIndex））
- `uint ToUInt32(byte[] value, int startIndex)`
  （uint ToUInt32（byte[] value, int startIndex））
- `ulong ToUInt64(byte[] value, int startIndex)`
  （ulong ToUInt64（byte[] value, int startIndex））
- `float ToSingle(byte[] value, int startIndex)`
  （float To单个（byte[] value, int startIndex））
- `double ToDouble(byte[] value, int startIndex)`
  （double ToDouble（byte[] value, int startIndex））
- `char GetHexValue(int i)`
  （char 获取Hex值（int i））
- `string ToString(byte[] value, int startIndex, int length)`
  （string To字符串（byte[] value, int startIndex, int length））
- `string ToString(byte[] value)`
  （string To字符串（byte[] value））
- `bool ToBoolean(byte[] value, int startIndex)`
  （bool ToBoolean（byte[] value, int startIndex））
- `long DoubleToInt64Bits(double value)`
  （long DoubleToInt64Bits（double value））
- `double Int64BitsToDouble(long value)`
  （double Int64BitsToDouble（long value））

---

## BitConverterLE（BitConverterLE）

### 方法 (8)

- `byte[] GetUIntBytes(byte* bytes)`
  （byte[] 获取U整数Bytes（byte* bytes））
- `byte[] GetULongBytes(byte* bytes)`
  （byte[] 获取ULongBytes（byte* bytes））
- `byte[] GetBytes(float value)`
  （byte[] 获取Bytes（float value））
- `byte[] GetBytes(double value)`
  （byte[] 获取Bytes（double value））
- `void UIntFromBytes(byte* dst, byte[] src, int startIndex)`
  （void U整数FromBytes（byte* dst, byte[] src, int startIndex））
- `void ULongFromBytes(byte* dst, byte[] src, int startIndex)`
  （void ULongFromBytes（byte* dst, byte[] src, int startIndex））
- `float ToSingle(byte[] value, int startIndex)`
  （float To单个（byte[] value, int startIndex））
- `double ToDouble(byte[] value, int startIndex)`
  （double ToDouble（byte[] value, int startIndex））

---

## BitConverterLE（BitConverterLE）

### 方法 (2)

- `byte[] GetUIntBytes(byte* bytes)`
  （byte[] 获取U整数Bytes（byte* bytes））
- `byte[] GetBytes(int value)`
  （byte[] 获取Bytes（int value））

---

## BitVector32（BitVector32）

### 字段 (1)

- `uint data`（uint data）(偏移: 0x0)

### 方法 (8)

- `bool get_Item(int bit)`
  （bool get_项目（int bit））
- `void set_Item(int bit, bool value)`
  （void set_项目（int bit, bool value））
- `int CreateMask()`
  （int 创建掩码（））
- `int CreateMask(int previous)`
  （int 创建掩码（int previous））
- `bool Equals(object o)`
  （布尔值 等于（对象 o））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `string ToString(BitVector32 value)`
  （string To字符串（BitVector32 value））
- `string ToString()`
  （字符串 转字符串（））

---

## BitconverterExt（BitconverterExt）

### 方法 (2)

- `byte[] GetBytes(Decimal dec)`
  （byte[] 获取Bytes（Decimal dec））
- `Decimal ToDecimal(byte[] bytes)`
  （Decimal ToDecimal（byte[] bytes））

---

## BlendMode（Blend模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## BlendOp（BlendOp）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## BlendSourceVirtualCamera（BlendSource虚拟的摄像机）

**继承**: ICinemachineCamera（ICinemachine摄像机）

### 方法 (21)

- `CinemachineBlend get_Blend()`
  （CinemachineBlend get_Blend（））
- `void set_Blend(CinemachineBlend value)`
  （void set_Blend（CinemachineBlend value））
- `string get_Name()`
  （字符串 获取_名称（））
- `string get_Description()`
  （字符串 获取_描述（））
- `int get_Priority()`
  （int get_Priority（））
- `void set_Priority(int value)`
  （void set_Priority（int value））
- `Transform get_LookAt()`
  （变换 获取_看向（））
- `void set_LookAt(Transform value)`
  （void 设置_看向（变换 value））
- `Transform get_Follow()`
  （变换 获取_跟随（））
- `void set_Follow(Transform value)`
  （void 设置_跟随（变换 value））
- `CameraState get_State()`
  （摄像机状态 get_状态（））
- `void set_State(CameraState value)`
  （void set_状态（摄像机状态 value））
- `GameObject get_VirtualCameraGameObject()`
  （游戏对象 get_虚拟的摄像机游戏对象（））
- `bool get_IsValid()`
  （布尔值 获取_是否有效（））
- `ICinemachineCamera get_ParentCamera()`
  （ICinemachine摄像机 get_父级摄像机（））
- `bool IsLiveChild(ICinemachineCamera vcam, bool dominantChildOnly = False)`
  （布尔值 是否活动子级（ICinemachine摄像机 vcam, 布尔值 仅主从子级 = 假））
- `CameraState CalculateNewState(float deltaTime)`
  （摄像机状态 计算新的状态（float deltaTime））
- `void UpdateCameraState(Vector3 worldUp, float deltaTime)`
  （void 更新摄像机状态（三维向量 worldUp, 浮点数 deltaTime））
- `void InternalUpdateCameraState(Vector3 worldUp, float deltaTime)`
  （void 内部更新摄像机状态（三维向量 worldUp, 浮点数 deltaTime））
- `void OnTransitionFromCamera(ICinemachineCamera fromCam, Vector3 worldUp, float deltaTime)`
  （void 从摄像机过渡时（ICinemachine摄像机 fromCam, 三维向量 worldUp, 浮点数 deltaTime））
- `void OnTargetObjectWarped(Transform target, Vector3 positionDelta)`
  （void 目标对象扭曲时（变换 target, 三维向量 位置增量））

---

## BlendState（Blend状态）

**继承**: IEquatable<BlendState>（IEquatable<BlendState>）

### 字段 (11)

- `RenderTargetBlendState m_BlendState0`（Render目标Blend状态 m_BlendState0）(偏移: 0x0)
- `RenderTargetBlendState m_BlendState1`（Render目标Blend状态 m_BlendState1）(偏移: 0x8)
- `RenderTargetBlendState m_BlendState2`（Render目标Blend状态 m_BlendState2）(偏移: 0x10)
- `RenderTargetBlendState m_BlendState3`（Render目标Blend状态 m_BlendState3）(偏移: 0x18)
- `RenderTargetBlendState m_BlendState4`（Render目标Blend状态 m_BlendState4）(偏移: 0x20)
- `RenderTargetBlendState m_BlendState5`（Render目标Blend状态 m_BlendState5）(偏移: 0x28)
- `RenderTargetBlendState m_BlendState6`（Render目标Blend状态 m_BlendState6）(偏移: 0x30)
- `RenderTargetBlendState m_BlendState7`（Render目标Blend状态 m_BlendState7）(偏移: 0x38)
- `byte m_SeparateMRTBlendStates`（byte m_SeparateMRTBlendStates）(偏移: 0x40)
- `byte m_AlphaToMask`（byte m_透明度To掩码）(偏移: 0x41)
- `short m_Padding`（short m_Padding）(偏移: 0x42)

### 方法 (4)

- `BlendState get_defaultValue()`
  （Blend状态 get_default值（））
- `bool Equals(BlendState other)`
  （bool Equals（Blend状态 other））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## BlockManager（Block管理器）

**继承**: VersionedMonoBehaviour（版本化MonoBehaviour）

### 方法 (5)

- `void Start()`
  （void 开始（））
- `bool NodeContainsAnyOf(GraphNode node, List<SingleNodeBlocker> selector)`
  （bool 节点Contains任意Of（Graph节点 node, List<单个节点Blocker> selector））
- `bool NodeContainsAnyExcept(GraphNode node, List<SingleNodeBlocker> selector)`
  （bool 节点Contains任意Except（Graph节点 node, List<单个节点Blocker> selector））
- `void InternalBlock(GraphNode node, SingleNodeBlocker blocker)`
  （void 内部的Block（Graph节点 node, 单个节点Blocker blocker））
- `void InternalUnblock(GraphNode node, SingleNodeBlocker blocker)`
  （void 内部的Unblock（Graph节点 node, 单个节点Blocker blocker））

---

## BlockManager.BlockMode（BlockManager.Block模式）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## BlockManager.TraversalProvider（BlockManager.Traversal提供者）

**继承**: ITraversalProvider（ITraversal提供者）

### 字段 (2)

- `BlockManager blockManager`（Block管理器 block管理器）(偏移: 0x8)
- `List<SingleNodeBlocker> selector`（List<单个节点Blocker> selector）(偏移: 0x10)

### 方法 (4)

- `BlockManager.BlockMode get_mode()`
  （BlockManager.Block模式 get_mode（））
- `void set_mode(BlockManager.BlockMode value)`
  （void set_mode（BlockManager.Block模式 value））
- `bool CanTraverse(Path path, GraphNode node)`
  （bool 能否Traverse（路径 path, Graph节点 node））
- `uint GetTraversalCost(Path path, GraphNode node)`
  （uint 获取TraversalCost（路径 path, Graph节点 node））

---

## BlockState（Block状态）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Bloom（Bloom）

**继承**: VolumeComponent, IPostProcessComponent（体积组件, I后处理组件）

### 字段 (9)

- `MinFloatParameter threshold`（最小浮点数Parameter threshold）(偏移: 0x1C)
- `MinFloatParameter intensity`（最小浮点数Parameter intensity）(偏移: 0x20)
- `ClampedFloatParameter scatter`（Clamped浮点数Parameter scatter）(偏移: 0x24)
- `MinFloatParameter clamp`（最小浮点数Parameter clamp）(偏移: 0x28)
- `ColorParameter tint`（颜色Parameter tint）(偏移: 0x2C)
- `BoolParameter highQualityFiltering`（布尔值Parameter highQualityFiltering）(偏移: 0x30)
- `ClampedIntParameter skipIterations`（Clamped整数Parameter skipIterations）(偏移: 0x34)
- `TextureParameter dirtTexture`（纹理Parameter dirt纹理）(偏移: 0x38)
- `MinFloatParameter dirtIntensity`（最小浮点数Parameter dirtIntensity）(偏移: 0x3C)

### 方法 (2)

- `bool IsActive()`
  （布尔值 是否激活的（））
- `bool IsTileCompatible()`
  （布尔值 是否瓦片兼容（））

---

## BodyTilt（身体Tilt）

**继承**: OffsetModifier（偏移修改器）

### 字段 (6)

- `float tiltSpeed`（float tiltSpeed）(偏移: 0x18)
- `float tiltSensitivity`（float tiltSensitivity）(偏移: 0x1C)
- `OffsetPose poseLeft`（OffsetPose pose左）(偏移: 0x20)
- `OffsetPose poseRight`（OffsetPose pose右）(偏移: 0x24)
- `float tiltAngle`（float tilt角度）(偏移: 0x28)
- `Vector3 lastForward`（三维向量 last前进）(偏移: 0x2C)

### 方法 (2)

- `void Start()`
  （void 开始（））
- `void OnModifyOffset()`
  （void 修改偏移时（））

---

## Bone（Bone）

**继承**: IEquatable<Bone>（IEquatable<Bone>）

### 字段 (2)

- `ulong m_DeviceId`（无符号长整数 m_设备ID）(偏移: 0x0)
- `uint m_FeatureIndex`（uint m_Feature索引）(偏移: 0x8)

### 方法 (5)

- `ulong get_deviceId()`
  （无符号长整数 获取_设备ID（））
- `uint get_featureIndex()`
  （uint get_feature索引（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(Bone other)`
  （bool Equals（Bone other））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## BoneWeight（BoneWeight）

**继承**: IEquatable<BoneWeight>（IEquatable<BoneWeight>）

### 字段 (8)

- `float m_Weight0`（float m_Weight0）(偏移: 0x0)
- `float m_Weight1`（float m_Weight1）(偏移: 0x4)
- `float m_Weight2`（float m_Weight2）(偏移: 0x8)
- `float m_Weight3`（float m_Weight3）(偏移: 0xC)
- `int m_BoneIndex0`（int m_BoneIndex0）(偏移: 0x10)
- `int m_BoneIndex1`（int m_BoneIndex1）(偏移: 0x14)
- `int m_BoneIndex2`（int m_BoneIndex2）(偏移: 0x18)
- `int m_BoneIndex3`（int m_BoneIndex3）(偏移: 0x1C)

### 方法 (11)

- `float get_weight0()`
  （float get_weight0（））
- `float get_weight1()`
  （float get_weight1（））
- `float get_weight2()`
  （float get_weight2（））
- `float get_weight3()`
  （float get_weight3（））
- `int get_boneIndex0()`
  （int get_boneIndex0（））
- `int get_boneIndex1()`
  （int get_boneIndex1（））
- `int get_boneIndex2()`
  （int get_boneIndex2（））
- `int get_boneIndex3()`
  （int get_boneIndex3（））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `bool Equals(object other)`
  （布尔值 等于（对象 other））
- `bool Equals(BoneWeight other)`
  （bool Equals（BoneWeight other））

---

## Boolean（Boolean）

**继承**: IComparable, IConvertible, IComparable<bool>, IEquatable<bool>（IComparable, IConvertible, IComparable<bool>, IEquatable<bool>）

### 字段 (3)

- `bool m_value`（bool m_value）(偏移: 0x0)
- `string TrueString`（string True字符串）(偏移: 0x0)
- `string FalseString`（string False字符串）(偏移: 0x4)

### 方法 (11)

- `int GetHashCode()`
  （整数 获取哈希码（））
- `string ToString()`
  （字符串 转字符串（））
- `string ToString(IFormatProvider provider)`
  （字符串 转字符串（I格式化提供者 provider））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(bool obj)`
  （bool Equals（bool obj））
- `int CompareTo(object obj)`
  （整数 比较到（对象 obj））
- `int CompareTo(bool value)`
  （int CompareTo（bool value））
- `bool Parse(string value)`
  （bool 解析（string value））
- `bool TryParse(string value, out bool result)`
  （bool Try解析（string value, out bool result））
- `string TrimWhiteSpaceAndNull(string value)`
  （string TrimWhiteSpaceAndNull（string value））
- `TypeCode GetTypeCode()`
  （类型代码 获取类型代码（））

---

## BooleanArrayTypeInfo（Boolean数组类型信息）

**继承**: TraceLoggingTypeInfo<bool[]>（TraceLogging类型Info<bool[]>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void 写入元数据（跟踪日志元数据收集器 collector, 字符串 name, 事件字段格式 format））
- `void WriteData(TraceLoggingDataCollector collector, ref bool[] value)`
  （void Write数据（TraceLogging数据Collector collector, ref bool[] value））

---

## BooleanConverter（BooleanConverter）

**继承**: TypeConverter（类型转换器）

### 字段 (1)

- `TypeConverter.StandardValuesCollection values`（类型Converter.StandardValuesCollection values）(偏移: 0x0)

### 方法 (5)

- `bool CanConvertFrom(ITypeDescriptorContext context, Type sourceType)`
  （布尔值 能否转换自（I类型描述符上下文 context, 类型 sourceType））
- `object ConvertFrom(ITypeDescriptorContext context, CultureInfo culture, object value)`
  （对象 转换自（I类型描述符上下文 context, 区域性信息 culture, 对象 value））
- `TypeConverter.StandardValuesCollection GetStandardValues(ITypeDescriptorContext context)`
  （类型转换器.标准值集合 获取标准值（I类型描述符上下文 context））
- `bool GetStandardValuesExclusive(ITypeDescriptorContext context)`
  （布尔值 获取标准值独占（I类型描述符上下文 context））
- `bool GetStandardValuesSupported(ITypeDescriptorContext context)`
  （布尔值 获取标准值支持（I类型描述符上下文 context））

---

## BooleanTypeInfo（Boolean类型信息）

**继承**: TraceLoggingTypeInfo<bool>（TraceLogging类型Info<bool>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void 写入元数据（跟踪日志元数据收集器 collector, 字符串 name, 事件字段格式 format））
- `void WriteData(TraceLoggingDataCollector collector, ref bool value)`
  （void Write数据（TraceLogging数据Collector collector, ref bool value））

---

## BootConfigData（Boot配置数据）

### 字段 (1)

- `IntPtr m_Ptr`（整数指针 m_指针）(偏移: 0x8)

### 方法 (1)

- `BootConfigData WrapBootConfigData(IntPtr nativeHandle)`
  （Boot配置数据 WrapBoot配置数据（整数Ptr nativeHandle））

---

## Bootstring（Bootstring）

### 字段 (8)

- `char delimiter`（char delimiter）(偏移: 0x8)
- `int base_num`（int base_num）(偏移: 0xC)
- `int tmin`（int tmin）(偏移: 0x10)
- `int tmax`（int tmax）(偏移: 0x14)
- `int skew`（int skew）(偏移: 0x18)
- `int damp`（int damp）(偏移: 0x1C)
- `int initial_bias`（int initial_bias）(偏移: 0x20)
- `int initial_n`（int initial_n）(偏移: 0x24)

### 方法 (5)

- `string Encode(string s, int offset)`
  （string Encode（string s, int offset））
- `char EncodeDigit(int d)`
  （char EncodeDigit（int d））
- `int DecodeDigit(char c)`
  （int DecodeDigit（char c））
- `int Adapt(int delta, int numPoints, bool firstTime)`
  （int Adapt（int delta, int numPoints, bool firstTime））
- `string Decode(string s, int offset)`
  （string Decode（string s, int offset））

---

## Bot（机器人）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (41)

- `float Cos10`（float Cos10）(偏移: 0x0)
- `float Cos30`（float Cos30）(偏移: 0x4)
- `float Cos45`（float Cos45）(偏移: 0x8)
- `BotAbility ability`（机器人能力 ability）(偏移: 0xC)
- `BotEnemyInfo enemyInfo`（机器人Enemy信息 enemy信息）(偏移: 0x28)
- `bool faceToEnemy`（bool faceToEnemy）(偏移: 0x30)
- `int nextTargetCheckIndex`（int next目标检查索引）(偏移: 0x34)
- `float nextCheckEnemyInViewTime`（float next检查EnemyIn视图时间）(偏移: 0x38)
- `float nextAttackTime`（float nextAttack时间）(偏移: 0x3C)
- `int knifeAttackType`（int knifeAttack类型）(偏移: 0x40)
- `float knifeAttackEndTime`（float knifeAttack结束时间）(偏移: 0x44)
- `float watchOutEndTime`（float watchOut结束时间）(偏移: 0x48)
- `Vector3 watchOutPos`（三维向量 watchOutPos）(偏移: 0x4C)
- `bool stopAllBot`（bool stop所有机器人）(偏移: 0xC)
- `List<BotActionBase> actionList`（List<机器人动作Base> action列表）(偏移: 0x58)
- `Bot.ZoomDirectionGetter Getter_ZoomDirection`（Bot.瞄准方向Getter Getter_瞄准方向）(偏移: 0x5C)
- `CrabStep crabStepAction`（CrabStep crabStep动作）(偏移: 0x60)
- `Saunter saunterAction`（Saunter saunter动作）(偏移: 0x64)
- `float nextSelectWpnTime`（float next选择武器时间）(偏移: 0x68)
- `List<int> selectWpnActionList`（List<int> select武器动作列表）(偏移: 0x6C)
- `RefInt Getter_WeaponSlot`（Ref整数 Getter_Weapon槽位）(偏移: 0x70)
- `float nextUseSkillCheckTime`（float nextUse技能检查时间）(偏移: 0x74)
- `AlternativePath alternative`（Alternative路径 alternative）(偏移: 0x7C)
- `Path path`（路径 path）(偏移: 0x80)
- `GraphNode gNode_Nearset`（Graph节点 gNode_Nearset）(偏移: 0x88)
- `GraphNode gNode_Next`（Graph节点 gNode_下一个）(偏移: 0x8C)
- `int nextPathVectorID`（int next路径向量ID）(偏移: 0x90)
- `Vector3 lastStartPoint`（三维向量 last开始Point）(偏移: 0x94)
- `Vector3 nextPathPos`（三维向量 next路径Pos）(偏移: 0xA0)
- `Vector3 dirToNextNode`（三维向量 dirTo下一个节点）(偏移: 0xAC)
- `float nextFindPathTime`（float next查找路径时间）(偏移: 0xB8)
- `PathInterpolator interpolator`（路径Interpolator interpolator）(偏移: 0xBC)
- `RefPosition Destination_Listener`（RefPosition Destination_监听器）(偏移: 0xC0)
- `GraphNode nextJumpStartNode`（Graph节点 next跳跃开始节点）(偏移: 0xC8)
- `Bot_JumpLink.Link nextJumpLink`（Bot_跳跃Link.Link next跳跃Link）(偏移: 0xCC)
- `float nextJumpTime`（float next跳跃时间）(偏移: 0xE8)
- `float blockedTime`（float blocked时间）(偏移: 0xEC)
- `float crouchEndTime`（float crouch结束时间）(偏移: 0xF0)
- `List<Bot> hangoutList`（List<Bot> hangout列表）(偏移: 0x10)
- `int maxHangoutCount`（int maxHangout数量）(偏移: 0x14)
- `ObscuredBool hangoutTag`（模糊的布尔值 hangout标签）(偏移: 0xF4)

### 方法 (58)

- `bool get_isDead()`
  （布尔值 获取_是否死亡（））
- `void set_abilityLevel(float value)`
  （void set_ability等级（float value））
- `Player get_thisPlayer()`
  （玩家 get_this玩家（））
- `void set_thisPlayer(Player value)`
  （void set_this玩家（玩家 value））
- `Vector3 get_cameraPos()`
  （三维向量 get_cameraPos（））
- `Vector3 get_cameraFoward()`
  （三维向量 get_cameraFoward（））
- `Entity get_tryFindEnemy()`
  （实体 get_try查找Enemy（））
- `void set_tryFindEnemy(Entity value)`
  （void set_try查找Enemy（实体 value））
- `bool get_isStopped()`
  （布尔值 获取_已停止（））
- `void add_Getter_ZoomDirection(Bot.ZoomDirectionGetter value)`
  （void add_Getter_瞄准方向（Bot.瞄准方向Getter value））
- `void remove_Getter_ZoomDirection(Bot.ZoomDirectionGetter value)`
  （void remove_Getter_瞄准方向（Bot.瞄准方向Getter value））
- `void add_Getter_WeaponSlot(RefInt value)`
  （void add_Getter_Weapon槽位（Ref整数 value））
- `void remove_Getter_WeaponSlot(RefInt value)`
  （void remove_Getter_Weapon槽位（Ref整数 value））
- `Seeker get_seeker()`
  （Seeker get_seeker（））
- `void set_seeker(Seeker value)`
  （void set_seeker（Seeker value））
- `float get_pathLength()`
  （float get_pathLength（））
- `void set_pathLength(float value)`
  （void set_pathLength（float value））
- `void add_Destination_Listener(RefPosition value)`
  （void add_Destination_监听器（RefPosition value））
- `void remove_Destination_Listener(RefPosition value)`
  （void remove_Destination_监听器（RefPosition value））
- `NanoGuard get_nanoGuard()`
  （纳米Guard get_nanoGuard（））
- `void set_nanoGuard(NanoGuard value)`
  （void set_nanoGuard（纳米Guard value））
- `bool get_isArriveJumpStartNode()`
  （bool get_isArrive跳跃开始节点（））
- `bool get_canJump()`
  （bool get_can跳跃（））
- `void InitHangOutCount()`
  （void 初始化HangOut数量（））
- `void Awake()`
  （void 唤醒（））
- `void Update()`
  （void 更新（））
- `void OnDrawGizmosSelected()`
  （void 绘制选中辅助线时（））
- `void UpdateNearestGraphNode()`
  （void 更新NearestGraph节点（））
- `void PathSetting()`
  （void 路径设置（））
- `bool IsPosInReachDistance(Vector3 pos)`
  （bool 是否PosInReach距离（三维向量 pos））
- `bool IsPosInReachDistance(Vector3 pos, float distance)`
  （bool 是否PosInReach距离（三维向量 pos, float distance））
- `void OnPathComplete(Path newPath)`
  （void 路径完成时（路径 newPath））
- `void Move()`
  （void 移动（））
- `void JumpCheck()`
  （void 跳跃检查（））
- `void Jump(float delay = 0)`
  （void 跳跃（float delay = 0））
- `void TryCrouch()`
  （void Try蹲下（））
- `Vector2Int GetMoveStateByDir(Vector3 targetDir)`
  （二维向量整数 获取移动状态ByDir（三维向量 targetDir））
- `void CameraRotation()`
  （void 摄像机Rotation（））
- `void OnLifeStateChange(bool isAlive)`
  （void 生命状态改变时（布尔值 isAlive））
- `void TakeDamageEvent(ref DamageEventData eventData)`
  （void Take伤害事件（ref DamageEventData eventData））
- `void SpawnDelayEvent()`
  （void 出生延迟事件（））
- `void OnEnterNanoGuardArea(Bot_NanoGuardArea enterArea)`
  （void OnEnter纳米GuardArea（Bot_纳米GuardArea enterArea））
- `void OnExitNanoGuardArea(Bot_NanoGuardArea exitAarea)`
  （void OnExit纳米GuardArea（Bot_纳米GuardArea exitAarea））
- `IEnumerator FindAttackTarget()`
  （IEnumerator 查找Attack目标（））
- `bool TrySetAttackTarget(Entity target)`
  （bool Try集合Attack目标（实体 target））
- `bool CheckHitBox(Entity target)`
  （bool 检查命中Box（实体 target））
- `void CheckAttackTarget()`
  （void 检查Attack目标（））
- `void UseWeapon()`
  （void UseWeapon（））
- `void SelectWeapon()`
  （void 选择Weapon（））
- `void AddSelectWpnAction(int slot)`
  （void 添加选择武器动作（int slot））
- `void UseSkill()`
  （void Use技能（））
- `void OnNanoRoleChange(NanoRole oldRole, NanoRole newRole)`
  （void On纳米RoleChange（纳米角色 oldRole, 纳米角色 newRole））
- `void UpdateAction()`
  （void 更新动作（））
- `void OnNanoRoleTableTypeChange(NanoRoleSelect.Type tableType)`
  （void On纳米RoleTable类型Change（纳米RoleSelect.类型 tableType））
- `void OnPlayerSetSkill(Skill newSkill)`
  （void On玩家集合技能（技能 newSkill））
- `bool IsPathLengthToEnemyLess(float length)`
  （bool 是否路径LengthToEnemyLess（float length））
- `void UpdateGhostEntityState()`
  （void 更新幽灵实体状态（））
- `Vector3 GetZoomDirectionByPos(Vector3 pos)`
  （三维向量 获取瞄准方向ByPos（三维向量 pos））

---

## Bot.ZoomDirectionGetter（Bot.瞄准方向Getter）

**继承**: MulticastDelegate（多播委托）

### 方法 (3)

- `void Invoke(ref Vector3 zoomDir, ref int priority)`
  （void Invoke（ref Vector3 zoomDir, ref int priority））
- `IAsyncResult BeginInvoke(ref Vector3 zoomDir, ref int priority, AsyncCallback callback, object object)`
  （I异步Result BeginInvoke（ref Vector3 zoomDir, ref int priority, 异步回调 callback, object object））
- `void EndInvoke(ref Vector3 zoomDir, ref int priority, IAsyncResult result)`
  （void 结束Invoke（ref Vector3 zoomDir, ref int priority, I异步Result result））

---

## BotAbility（机器人能力）

### 方法 (15)

- `float get_zoomSpeed()`
  （float get_zoomSpeed（））
- `void set_zoomSpeed(float value)`
  （void set_zoomSpeed（float value））
- `float get_shootAccuracy()`
  （float get_shootAccuracy（））
- `void set_shootAccuracy(float value)`
  （void set_shootAccuracy（float value））
- `float get_recoilControl_X()`
  （float get_recoilControl_X（））
- `void set_recoilControl_X(float value)`
  （void set_recoilControl_X（float value））
- `float get_recoilControlRange_X()`
  （float get_recoil控制Range_X（））
- `void set_recoilControlRange_X(float value)`
  （void set_recoil控制Range_X（float value））
- `float get_randomRecoilControl_X()`
  （float get_random后坐力Control_X（））
- `float get_recoilControl_Y()`
  （float get_recoilControl_Y（））
- `void set_recoilControl_Y(float value)`
  （void set_recoilControl_Y（float value））
- `float get_recoilControlRange_Y()`
  （float get_recoil控制Range_Y（））
- `void set_recoilControlRange_Y(float value)`
  （void set_recoil控制Range_Y（float value））
- `float get_randomRecoilControl_Y()`
  （float get_random后坐力Control_Y（））
- `void SetAbility(float ability)`
  （void 集合能力（float ability））

---

## BotActionBase（机器人动作基础）

### 字段 (1)

- `Bot bot`（机器人 bot）(偏移: 0x8)

### 方法 (6)

- `Player get_player()`
  （玩家 get_player（））
- `bool get_isFinished()`
  （bool get_isFinished（））
- `void set_isFinished(bool value)`
  （void set_isFinished（bool value））
- `void Update()`
  （void 更新（））
- `void Finish()`
  （void Finish（））
- `void OnActionFinish()`
  （void 动作完成时（））

---

## BotControlData（机器人控制数据）

### 字段 (1)

- `float bigshotRate`（float bigshotRate）(偏移: 0x8)

---

## BotEnemyInfo（机器人Enemy信息）

### 字段 (9)

- `Bot bot`（机器人 bot）(偏移: 0x8)
- `Entity enemy`（实体 enemy）(偏移: 0xC)
- `float findTime`（float find时间）(偏移: 0x10)
- `float lastLostTime`（float lastLost时间）(偏移: 0x14)
- `Transform hitBox`（变换 hitBox）(偏移: 0x38)
- `BotEnemyInfo.DistanceControl distanceControl`（机器人EnemyInfo.距离控制 distance控制）(偏移: 0x3C)
- `float distanceControlChangeTime`（float distance控制Change时间）(偏移: 0x40)
- `bool isClosing`（bool isClosing）(偏移: 0x44)
- `float nextCheckVisibleTime`（float next检查可见的时间）(偏移: 0x48)

### 方法 (17)

- `float get_lostEnemyTime()`
  （float get_lostEnemy时间（））
- `bool get_haveEnemy()`
  （bool get_haveEnemy（））
- `bool get_isPlayer()`
  （bool get_is玩家（））
- `void set_isPlayer(bool value)`
  （void set_is玩家（bool value））
- `Vector3 get_enemyPos()`
  （三维向量 get_enemyPos（））
- `void set_enemyPos(Vector3 value)`
  （void set_enemyPos（三维向量 value））
- `float get_distance()`
  （浮点数 获取_距离（））
- `void set_distance(float value)`
  （void set_distance（float value））
- `Vector3 get_dirToEnemy()`
  （三维向量 get_dirToEnemy（））
- `void set_dirToEnemy(Vector3 value)`
  （void set_dirToEnemy（三维向量 value））
- `Vector3 get_dirToHitBox()`
  （三维向量 get_dirTo命中Box（））
- `void set_dirToHitBox(Vector3 value)`
  （void set_dirTo命中Box（三维向量 value））
- `float get_dotToHitBox()`
  （float get_dotTo命中Box（））
- `void CalGunDistanceControl(float wpnShotDistance)`
  （void Cal枪械距离控制（float wpnShotDistance））
- `void CalKnifeDistanceControl()`
  （void Cal近战武器距离控制（））
- `void Update()`
  （void 更新（））
- `bool ShouldWaitKnifeAttack()`
  （bool 应该Wait近战武器Attack（））

---

## BotEnemyInfo.DistanceControl（机器人EnemyInfo.距离控制）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## BotSkillBase（机器人技能基础）

**继承**: BotActionBase（机器人动作基础）

### 字段 (2)

- `SkillKey skillKey`（技能键 skill键）(偏移: 0x10)
- `float nextCheckTime`（float next检查时间）(偏移: 0x14)

### 方法 (2)

- `void DoAction()`
  （void 执行动作（））
- `void AddNextCheckTime(float min, float max)`
  （void 添加下一个检查时间（float min, float max））

---

## BotTarget（机器人目标）

### 字段 (2)

- `GameObject[] points`（游戏Object[] points）(偏移: 0x0)
- `bool sneakWay`（bool sneakWay）(偏移: 0x4)

---

## Bot_CrouchPos（Bot_蹲下Pos）

**继承**: Bot_GuardPos（Bot_GuardPos）

### 字段 (4)

- `bool crouchDisabled`（bool crouch禁用的）(偏移: 0x20)
- `bool always`（bool always）(偏移: 0x21)
- `List<Bot_CrouchPos> SpareList_BL`（List<Bot_蹲下Pos> SpareList_BL）(偏移: 0x0)
- `List<Bot_CrouchPos> SpareList_GR`（List<Bot_蹲下Pos> SpareList_GR）(偏移: 0x4)

### 方法 (8)

- `bool get_isAlways()`
  （bool get_isAlways（））
- `void Awake()`
  （void 唤醒（））
- `void AddToSpareList()`
  （void 添加ToSpare列表（））
- `void RemoveFromSpareList()`
  （void 移除FromSpare列表（））
- `void OnSetNullOwner()`
  （void On集合NullOwner（））
- `void OnSetValidOwner()`
  （void On集合ValidOwner（））
- `void Clear()`
  （void 清除（））
- `Bot_CrouchPos GetRandomPos(Team playerTeam)`
  （Bot_蹲下Pos 获取随机Pos（队伍 playerTeam））

---

## Bot_GuardPos（Bot_GuardPos）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (4)

- `Team team`（队伍 team）(偏移: 0xC)
- `Vector3[] zoomPos`（Vector3[] zoomPos）(偏移: 0x10)
- `int zoomPosIndex`（int zoomPos索引）(偏移: 0x14)
- `float nextZoomPosChangeTime`（float next瞄准PosChange时间）(偏移: 0x18)

### 方法 (9)

- `Player get_owner()`
  （玩家 get_owner（））
- `void set_owner(Player value)`
  （void set_owner（玩家 value））
- `void Update()`
  （void 更新（））
- `void SetOwner(Player newOwner)`
  （void 集合Owner（玩家 newOwner））
- `void OnSetValidOwner()`
  （void On集合ValidOwner（））
- `void OnSetNullOwner()`
  （void On集合NullOwner（））
- `void OnDrawGizmos()`
  （void 绘制辅助线时（））
- `void OnDrawGizmosSelected()`
  （void 绘制选中辅助线时（））
- `bool TryGetZoomPos(out Vector3 pos)`
  （bool Try获取瞄准Pos（out Vector3 pos））

---

## Bot_JumpLink（Bot_跳跃Link）

**继承**: GraphModifier（图修改器）

### 字段 (1)

- `Bot_JumpLink.Link[] links`（Bot_跳跃Link.Link[] links）(偏移: 0x24)

### 方法 (6)

- `GraphNode get_startNode()`
  （Graph节点 get_start节点（））
- `void set_startNode(GraphNode value)`
  （void set_start节点（Graph节点 value））
- `bool GetLink(GraphNode graphNode, out Bot_JumpLink jumpLink)`
  （bool 获取Link（Graph节点 graphNode, out Bot_JumpLink jumpLink））
- `void OnLatePostScan()`
  （void 延迟后扫描时（））
- `bool GetLinkEndByGraphNode(GraphNode node, out Bot_JumpLink.Link output)`
  （bool 获取Link结束ByGraph节点（Graph节点 node, out Bot_JumpLink.Link output））
- `void OnDrawGizmosSelected()`
  （void 绘制选中辅助线时（））

---

## Bot_JumpLink.Link（Bot_跳跃Link.Link）

### 字段 (6)

- `Transform endTransform`（变换 end变换）(偏移: 0x0)
- `GraphNode endNode`（Graph节点 end节点）(偏移: 0x4)
- `float needSpeed`（float needSpeed）(偏移: 0x8)
- `float accuracy`（float accuracy）(偏移: 0xC)
- `Vector3 direction`（三维向量 方向）(偏移: 0x10)
- `Bot_JumpLink.Link empty`（Bot_跳跃Link.Link empty）(偏移: 0x0)

### 方法 (1)

- `void CaculateDirection(Transform startPoint)`
  （void Caculate方向（变换 startPoint））

---

## Bot_NanoGuardArea（Bot_纳米GuardArea）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (6)

- `List<Bot_NanoGuardArea> SpareAreaList`（List<Bot_纳米GuardArea> SpareArea列表）(偏移: 0x0)
- `Vector3[] entrancePos`（Vector3[] entrancePos）(偏移: 0xC)
- `List<Bot_NanoGuardPos> posList`（List<Bot_纳米GuardPos> pos列表）(偏移: 0x10)
- `Bot_NanoGuardArea[] neighborAreas`（Bot_纳米GuardArea[] neighborAreas）(偏移: 0x14)
- `Bot_NanoGuardArea[] escapeAreas`（Bot_纳米GuardArea[] escapeAreas）(偏移: 0x18)
- `Vector3[] escapePos`（Vector3[] escapePos）(偏移: 0x1C)

### 方法 (13)

- `bool get_isFull()`
  （bool get_is满（））
- `void Awake()`
  （void 唤醒（））
- `void OnTriggerEnter(Collider other)`
  （void 触发器进入时（碰撞器 other））
- `void OnTriggerExit(Collider other)`
  （void 触发器退出时（碰撞器 other））
- `Bot_NanoGuardPos GetPos()`
  （Bot_纳米GuardPos 获取Pos（））
- `void RecyclePos(Bot_NanoGuardPos pos)`
  （void RecyclePos（Bot_纳米GuardPos pos））
- `Bot_NanoGuardArea GetRandomArea()`
  （Bot_纳米GuardArea 获取随机Area（））
- `bool GetRandomEscapePos(out Vector3 pos)`
  （bool 获取随机EscapePos（out Vector3 pos））
- `Bot_NanoGuardArea GetRandomAreaExclude(Bot_NanoGuardArea exclude)`
  （Bot_纳米GuardArea 获取随机AreaExclude（Bot_纳米GuardArea exclude））
- `void OnDrawGizmosSelected()`
  （void 绘制选中辅助线时（））
- `Bot_NanoGuardPos GetSaferPos(int safety)`
  （Bot_纳米GuardPos 获取SaferPos（int safety））
- `Bot_NanoGuardArea GetEscapeArea()`
  （Bot_纳米GuardArea 获取EscapeArea（））
- `Bot_NanoGuardArea GetNeighborArea()`
  （Bot_纳米GuardArea 获取NeighborArea（））

---

## Bot_NanoGuardPos（Bot_纳米GuardPos）

**继承**: MonoBehaviour（MonoBehaviour行为）

### 字段 (4)

- `Vector3[] zoomPos`（Vector3[] zoomPos）(偏移: 0x10)
- `float nextRandomTime`（float next随机时间）(偏移: 0x14)
- `int lastZoomPosIndex`（int last瞄准Pos索引）(偏移: 0x18)
- `int _safety`（int _safety）(偏移: 0x1C)

### 方法 (8)

- `Bot_NanoGuardArea get_area()`
  （Bot_纳米GuardArea get_area（））
- `void set_area(Bot_NanoGuardArea value)`
  （void set_area（Bot_纳米GuardArea value））
- `int get_safety()`
  （int get_safety（））
- `void Init(Bot_NanoGuardArea area)`
  （void 初始化（Bot_纳米GuardArea area））
- `void Leave()`
  （void Leave（））
- `void OnDrawGizmosSelected()`
  （void 绘制选中辅助线时（））
- `Vector3 GetRandomZoomPos()`
  （三维向量 获取随机瞄准Pos（））
- `void OnDrawGizmos()`
  （void 绘制辅助线时（））

---

## Bounce（Bounce）

### 方法 (3)

- `float EaseIn(float time, float duration, float unusedOvershootOrAmplitude, float unusedPeriod)`
  （float EaseIn（float time, float duration, float unusedOvershootOrAmplitude, float unusedPeriod））
- `float EaseOut(float time, float duration, float unusedOvershootOrAmplitude, float unusedPeriod)`
  （float EaseOut（float time, float duration, float unusedOvershootOrAmplitude, float unusedPeriod））
- `float EaseInOut(float time, float duration, float unusedOvershootOrAmplitude, float unusedPeriod)`
  （float EaseInOut（float time, float duration, float unusedOvershootOrAmplitude, float unusedPeriod））

---

## BoundingSphere（BoundingSphere）

### 字段 (2)

- `Vector3 position`（三维向量 位置）(偏移: 0x0)
- `float radius`（浮点数 半径）(偏移: 0xC)

---

## Bounds（Bounds）

**继承**: IEquatable<Bounds>, IFormattable（IEquatable<Bounds>, IFormattable）

### 字段 (2)

- `Vector3 m_Center`（三维向量 m_中心）(偏移: 0x0)
- `Vector3 m_Extents`（三维向量 m_Extents）(偏移: 0xC)

### 方法 (25)

- `int GetHashCode()`
  （整数 获取哈希码（））
- `bool Equals(object other)`
  （布尔值 等于（对象 other））
- `bool Equals(Bounds other)`
  （bool Equals（Bounds other））
- `Vector3 get_center()`
  （三维向量 获取_中心（））
- `void set_center(Vector3 value)`
  （void set_center（三维向量 value））
- `Vector3 get_size()`
  （三维向量 get_size（））
- `void set_size(Vector3 value)`
  （void set_size（三维向量 value））
- `Vector3 get_extents()`
  （三维向量 get_extents（））
- `void set_extents(Vector3 value)`
  （void set_extents（三维向量 value））
- `Vector3 get_min()`
  （三维向量 get_min（））
- `void set_min(Vector3 value)`
  （void set_min（三维向量 value））
- `Vector3 get_max()`
  （三维向量 get_max（））
- `void set_max(Vector3 value)`
  （void set_max（三维向量 value））
- `bool op_Equality(Bounds lhs, Bounds rhs)`
  （bool op_Equality（Bounds lhs, Bounds rhs））
- `bool op_Inequality(Bounds lhs, Bounds rhs)`
  （bool op_Inequality（Bounds lhs, Bounds rhs））
- `void SetMinMax(Vector3 min, Vector3 max)`
  （void 集合最小最大（三维向量 min, 三维向量 max））
- `void Encapsulate(Vector3 point)`
  （void Encapsulate（三维向量 point））
- `void Encapsulate(Bounds bounds)`
  （void Encapsulate（Bounds bounds））
- `void Expand(float amount)`
  （void Expand（float amount））
- `void Expand(Vector3 amount)`
  （void Expand（三维向量 amount））
- `bool Intersects(Bounds bounds)`
  （bool Intersects（Bounds bounds））
- `string ToString()`
  （字符串 转字符串（））
- `string ToString(string format, IFormatProvider formatProvider)`
  （字符串 转字符串（字符串 格式, I格式化提供者 formatProvider））
- `bool Contains(Vector3 point)`
  （布尔值 包含（三维向量 point））
- `bool Contains_Injected(ref Bounds _unity_self, ref Vector3 point)`
  （bool Contains_Injected（ref Bounds _unity_self, ref Vector3 point））

---

## BoxCollider（Box碰撞器）

**继承**: Collider（碰撞器）

### 方法 (4)

- `Vector3 get_center()`
  （三维向量 获取_中心（））
- `Vector3 get_size()`
  （三维向量 get_size（））
- `void get_center_Injected(out Vector3 ret)`
  （void 获取_中心_注入（输出 Vector3 ret））
- `void get_size_Injected(out Vector3 ret)`
  （void get_size_Injected（out Vector3 ret））

---

## BrowsableAttribute（BrowsableAttribute）

**继承**: Attribute（属性）

### 字段 (4)

- `BrowsableAttribute Yes`（BrowsableAttribute Yes）(偏移: 0x0)
- `BrowsableAttribute No`（BrowsableAttribute No）(偏移: 0x4)
- `BrowsableAttribute Default`（BrowsableAttribute 默认的）(偏移: 0x8)
- `bool browsable`（bool browsable）(偏移: 0x8)

### 方法 (4)

- `bool get_Browsable()`
  （bool get_Browsable（））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `bool IsDefaultAttribute()`
  （布尔值 是否默认属性（））

---

## Buff（增益）

### 字段 (4)

- `Action timeOutAction`（动作 timeOut动作）(偏移: 0x14)
- `Action removeAction`（动作 remove动作）(偏移: 0x18)
- `Action lifeEndAction`（动作 life结束动作）(偏移: 0x1C)
- `int priority`（整数 优先级）(偏移: 0x20)

### 方法 (17)

- `string get_name()`
  （字符串 获取_名称（））
- `void set_name(string value)`
  （void 设置_名称（字符串 value））
- `Entity get_owner()`
  （实体 get_owner（））
- `void set_owner(Entity value)`
  （void set_owner（实体 value））
- `float get_endTime()`
  （float get_end时间（））
- `void set_endTime(float value)`
  （void set_end时间（float value））
- `void add_timeOutAction(Action value)`
  （void add_timeOut动作（动作 value））
- `void remove_timeOutAction(Action value)`
  （void remove_timeOut动作（动作 value））
- `void add_removeAction(Action value)`
  （void add_remove动作（动作 value））
- `void remove_removeAction(Action value)`
  （void remove_remove动作（动作 value））
- `void add_lifeEndAction(Action value)`
  （void add_life结束动作（动作 value））
- `void remove_lifeEndAction(Action value)`
  （void remove_life结束动作（动作 value））
- `bool get_isEffective()`
  （bool get_isEffective（））
- `void Refreshime(float duration)`
  （void Refreshime（float duration））
- `void TimeOut()`
  （void 时间Out（））
- `void Remove()`
  （void 移除（））
- `void OnLifeEnd()`
  （void 生命结束时（））

---

## Buffer（缓冲区）

### 方法 (12)

- `bool InternalBlockCopy(Array src, int srcOffsetBytes, Array dst, int dstOffsetBytes, int byteCount)`
  （bool 内部的Block复制（数组 src, int srcOffsetBytes, 数组 dst, int dstOffsetBytes, int byteCount））
- `int IndexOfByte(byte* src, byte value, int index, int count)`
  （int 索引OfByte（byte* src, byte value, int index, int count））
- `int _ByteLength(Array array)`
  （int _ByteLength（数组 array））
- `void ZeroMemory(byte* src, long len)`
  （void ZeroMemory（byte* src, long len））
- `void Memcpy(byte[] dest, int destIndex, byte* src, int srcIndex, int len)`
  （void Memcpy（byte[] dest, int destIndex, byte* src, int srcIndex, int len））
- `void Memcpy(byte* pDest, int destIndex, byte[] src, int srcIndex, int len)`
  （void Memcpy（byte* pDest, int destIndex, byte[] src, int srcIndex, int len））
- `int ByteLength(Array array)`
  （int ByteLength（数组 array））
- `void BlockCopy(Array src, int srcOffset, Array dst, int dstOffset, int count)`
  （void Block复制（数组 src, int srcOffset, 数组 dst, int dstOffset, int count））
- `void memcpy4(byte* dest, byte* src, int size)`
  （void memcpy4（byte* dest, byte* src, int size））
- `void memcpy2(byte* dest, byte* src, int size)`
  （void memcpy2（byte* dest, byte* src, int size））
- `void memcpy1(byte* dest, byte* src, int size)`
  （void memcpy1（byte* dest, byte* src, int size））
- `void Memcpy(byte* dest, byte* src, int size)`
  （void Memcpy（byte* dest, byte* src, int size））

---

## BufferedRTHandleSystem（BufferedRT句柄系统）

**继承**: IDisposable（可释放接口）

### 字段 (2)

- `RTHandleSystem m_RTHandleSystem`（RT句柄系统 m_RT句柄系统）(偏移: 0xC)
- `bool m_DisposedValue`（bool m_Disposed值）(偏移: 0x10)

### 方法 (13)

- `int get_maxWidth()`
  （int get_max宽度（））
- `int get_maxHeight()`
  （int get_max高度（））
- `RTHandleProperties get_rtHandleProperties()`
  （RT句柄属性 获取_rt句柄属性（））
- `RTHandle GetFrameRT(int bufferId, int frameIndex)`
  （RT句柄 获取FrameRT（int bufferId, int frameIndex））
- `void AllocBuffer(int bufferId, Func<RTHandleSystem, int, RTHandle> allocator, int bufferCount)`
  （void Alloc缓冲区（int bufferId, Func<RT句柄系统, int, RTHandle> allocator, int bufferCount））
- `void ReleaseBuffer(int bufferId)`
  （void Release缓冲区（int bufferId））
- `void SwapAndSetReferenceSize(int width, int height, MSAASamples msaaSamples)`
  （void SwapAnd集合引用大小（int width, int height, MSAASamples msaaSamples））
- `void ResetReferenceSize(int width, int height)`
  （void 重置引用大小（int width, int height））
- `int GetNumFramesAllocated(int bufferId)`
  （int 获取NumFramesAllocated（int bufferId））
- `void Swap()`
  （void Swap（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `void Dispose()`
  （void 释放（））
- `void ReleaseAll()`
  （void Release所有（））

---

## BuiltinRenderTextureType（BuiltinRender纹理类型）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## BuiltinRuntimeReflectionSystem（BuiltinRuntimeReflection系统）

**继承**: IScriptableRuntimeReflectionSystem, IDisposable（IScriptableRuntimeReflection系统, IDisposable）

### 方法 (5)

- `bool TickRealtimeProbes()`
  （bool TickRealtimeProbes（））
- `void Dispose()`
  （void 释放（））
- `void Dispose(bool disposing)`
  （void 释放（布尔值 正在释放））
- `bool BuiltinUpdate()`
  （bool Builtin更新（））
- `BuiltinRuntimeReflectionSystem Internal_BuiltinRuntimeReflectionSystem_New()`
  （BuiltinRuntimeReflection系统 Internal_BuiltinRuntimeReflectionSystem_新的（））

---

## BuiltinShaderDefine（Builtin着色器Define）

### 字段 (1)

- `int value__`（整数 值__）(偏移: 0x0)

---

## Button（按钮）

**继承**: Selectable, IPointerClickHandler, IEventSystemHandler, ISubmitHandler（Selectable, I指针Click处理器, I事件系统处理器, ISubmit处理器）

### 字段 (1)

- `Button.ButtonClickedEvent m_OnClick`（Button.按钮Clicked事件 m_OnClick）(偏移: 0xB0)

### 方法 (6)

- `Button.ButtonClickedEvent get_onClick()`
  （Button.按钮Clicked事件 get_onClick（））
- `void set_onClick(Button.ButtonClickedEvent value)`
  （void set_onClick（Button.按钮Clicked事件 value））
- `void Press()`
  （void Press（））
- `void OnPointerClick(PointerEventData eventData)`
  （void 指针点击时（指针事件数据 eventData））
- `void OnSubmit(BaseEventData eventData)`
  （void 提交时（基础事件数据 eventData））
- `IEnumerator OnFinishSubmit()`
  （IEnumerator OnFinishSubmit（））

---

## Byte（Byte）

**继承**: IComparable, IFormattable, IConvertible, IComparable<byte>, IEquatable<byte>（IComparable, IFormattable, IConvertible, IComparable<byte>, IEquatable<byte>）

### 字段 (1)

- `byte m_value`（byte m_value）(偏移: 0x0)

### 方法 (15)

- `int CompareTo(object value)`
  （整数 比较到（对象 value））
- `int CompareTo(byte value)`
  （int CompareTo（byte value））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `bool Equals(byte obj)`
  （bool Equals（byte obj））
- `int GetHashCode()`
  （整数 获取哈希码（））
- `byte Parse(string s, IFormatProvider provider)`
  （byte 解析（string s, I格式化提供者 provider））
- `byte Parse(string s, NumberStyles style, IFormatProvider provider)`
  （byte 解析（string s, NumberStyles style, I格式化提供者 provider））
- `byte Parse(string s, NumberStyles style, NumberFormatInfo info)`
  （byte 解析（string s, NumberStyles style, Number格式化信息 info））
- `bool TryParse(string s, out byte result)`
  （bool Try解析（string s, out byte result））
- `bool TryParse(string s, NumberStyles style, NumberFormatInfo info, out byte result)`
  （bool Try解析（string s, NumberStyles style, Number格式化信息 info, out byte result））
- `string ToString()`
  （字符串 转字符串（））
- `string ToString(string format)`
  （字符串 转字符串（字符串 格式））
- `string ToString(IFormatProvider provider)`
  （字符串 转字符串（I格式化提供者 provider））
- `string ToString(string format, IFormatProvider provider)`
  （字符串 转字符串（字符串 格式, I格式化提供者 provider））
- `TypeCode GetTypeCode()`
  （类型代码 获取类型代码（））

---

## ByteArrayTypeInfo（Byte数组类型信息）

**继承**: TraceLoggingTypeInfo<byte[]>（TraceLogging类型Info<byte[]>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void 写入元数据（跟踪日志元数据收集器 collector, 字符串 name, 事件字段格式 format））
- `void WriteData(TraceLoggingDataCollector collector, ref byte[] value)`
  （void Write数据（TraceLogging数据Collector collector, ref byte[] value））

---

## ByteConverter（ByteConverter）

**继承**: BaseNumberConverter（基础数字转换器）

### 方法 (5)

- `Type get_TargetType()`
  （类型 get_目标类型（））
- `object FromString(string value, int radix)`
  （对象 从字符串（字符串 value, 整数 radix））
- `object FromString(string value, NumberFormatInfo formatInfo)`
  （对象 从字符串（字符串 value, 数字格式信息 formatInfo））
- `object FromString(string value, CultureInfo culture)`
  （对象 从字符串（字符串 value, 区域性信息 culture））
- `string ToString(object value, NumberFormatInfo formatInfo)`
  （字符串 转字符串（对象 value, 数字格式信息 formatInfo））

---

## ByteEnum（ByteEnum）

### 字段 (1)

- `byte value__`（字节 值__）(偏移: 0x0)

---

## ByteEqualityComparer（ByteEqualityComparer）

**继承**: EqualityComparer<byte>（EqualityComparer<byte>）

### 方法 (6)

- `bool Equals(byte x, byte y)`
  （bool Equals（byte x, byte y））
- `int GetHashCode(byte b)`
  （int 获取HashCode（byte b））
- `int IndexOf(byte[] array, byte value, int startIndex, int count)`
  （int 索引Of（byte[] array, byte value, int startIndex, int count））
- `int LastIndexOf(byte[] array, byte value, int startIndex, int count)`
  （int 最后一个索引Of（byte[] array, byte value, int startIndex, int count））
- `bool Equals(object obj)`
  （布尔值 等于（对象 obj））
- `int GetHashCode()`
  （整数 获取哈希码（））

---

## ByteMatcher（ByteMatcher）

### 字段 (2)

- `Hashtable map`（Hashtable map）(偏移: 0x8)
- `Hashtable starts`（Hashtable starts）(偏移: 0xC)

### 方法 (4)

- `void AddMapping(TermInfoStrings key, byte[] val)`
  （void 添加Mapping（Term信息Strings key, byte[] val））
- `void Sort()`
  （void 排序（））
- `bool StartsWith(int c)`
  （bool StartsWith（int c））
- `TermInfoStrings Match(char[] buffer, int offset, int length, out int used)`
  （Term信息Strings 比赛（char[] buffer, int offset, int length, out int used））

---

## ByteTypeInfo（Byte类型信息）

**继承**: TraceLoggingTypeInfo<byte>（TraceLogging类型Info<byte>）

### 方法 (2)

- `void WriteMetadata(TraceLoggingMetadataCollector collector, string name, EventFieldFormat format)`
  （void 写入元数据（跟踪日志元数据收集器 collector, 字符串 name, 事件字段格式 format））
- `void WriteData(TraceLoggingDataCollector collector, ref byte value)`
  （void Write数据（TraceLogging数据Collector collector, ref byte value））

---

## CADArgHolder（CADArgHolder）

### 字段 (1)

- `int index`（整数 索引）(偏移: 0x8)

---

## CADMessageBase（CADMessage基础）

### 字段 (5)

- `object[] _args`（对象[] _参数）(偏移: 0x8)
- `byte[] _serializedArgs`（byte[] _serializedArgs）(偏移: 0xC)
- `int _propertyCount`（int _property数量）(偏移: 0x10)
- `CADArgHolder _callContext`（CADArgHolder _callContext）(偏移: 0x14)
- `byte[] serializedMethod`（byte[] serializedMethod）(偏移: 0x18)

### 方法 (11)

- `MethodBase GetMethod()`
  （Method基础 获取Method（））
- `Type[] GetSignature(MethodBase methodBase, bool load)`
  （Type[] 获取Signature（Method基础 methodBase, bool load））
- `int MarshalProperties(IDictionary dict, ref ArrayList args)`
  （int MarshalProperties（I字典 dict, ref ArrayList args））
- `void UnmarshalProperties(IDictionary dict, int count, ArrayList args)`
  （void UnmarshalProperties（I字典 dict, int count, 数组列表 args））
- `bool IsPossibleToIgnoreMarshal(object obj)`
  （bool 是否PossibleToIgnoreMarshal（object obj））
- `object MarshalArgument(object arg, ref ArrayList args)`
  （object MarshalArgument（object arg, ref ArrayList args））
- `object UnmarshalArgument(object arg, ArrayList args)`
  （object UnmarshalArgument（object arg, 数组列表 args））
- `object[] MarshalArguments(object[] arguments, ref ArrayList args)`
  （object[] MarshalArguments（object[] arguments, ref ArrayList args））
- `object[] UnmarshalArguments(object[] arguments, ArrayList args)`
  （object[] UnmarshalArguments（object[] arguments, 数组列表 args））
- `void SaveLogicalCallContext(IMethodMessage msg, ref ArrayList serializeList)`
  （void 保存LogicalCallContext（IMethodMessage msg, ref ArrayList serializeList））
- `LogicalCallContext GetLogicalCallContext(ArrayList args)`
  （LogicalCallContext 获取LogicalCallContext（数组列表 args））

---

## CADMethodCallMessage（CADMethodCallMessage）

**继承**: CADMessageBase（CADMessage基础）

### 字段 (1)

- `string _uri`（字符串 _uri）(偏移: 0x1C)

### 方法 (5)

- `string get_Uri()`
  （字符串 获取_Uri（））
- `CADMethodCallMessage Create(IMessage callMsg)`
  （CADMethodCallMessage 创建（IMessage callMsg））
- `ArrayList GetArguments()`
  （数组列表 获取Arguments（））
- `object[] GetArgs(ArrayList args)`
  （object[] 获取Args（数组列表 args））
- `int get_PropertiesCount()`
  （int get_Properties数量（））

---

## CADMethodRef（CADMethodRef）

### 字段 (5)

- `bool ctor`（bool ctor）(偏移: 0x8)
- `string typeName`（字符串 类型名称）(偏移: 0xC)
- `string methodName`（string method名称）(偏移: 0x10)
- `string[] param_names`（string[] param_names）(偏移: 0x14)
- `string[] generic_arg_names`（string[] generic_arg_names）(偏移: 0x18)

### 方法 (2)

- `Type[] GetTypes(string[] typeArray)`
  （Type[] 获取Types（string[] typeArray））
- `MethodBase Resolve()`
  （Method基础 Resolve（））

---

## CADMethodReturnMessage（CADMethodReturnMessage）

**继承**: CADMessageBase（CADMessage基础）

### 字段 (3)

- `object _returnValue`（object _return值）(偏移: 0x1C)
- `CADArgHolder _exception`（CADArgHolder _exception）(偏移: 0x20)
- `Type[] _sig`（Type[] _sig）(偏移: 0x24)

### 方法 (6)

- `CADMethodReturnMessage Create(IMessage callMsg)`
  （CADMethodReturnMessage 创建（IMessage callMsg））
- `ArrayList GetArguments()`
  （数组列表 获取Arguments（））
- `object[] GetArgs(ArrayList args)`
  （object[] 获取Args（数组列表 args））
- `object GetReturnValue(ArrayList args)`
  （object 获取Return值（数组列表 args））
- `Exception GetException(ArrayList args)`
  （Exception 获取Exception（数组列表 args））
- `int get_PropertiesCount()`
  （int get_Properties数量（））

---

## CADObjRef（CADObjRef）

### 字段 (3)

- `ObjRef objref`（ObjRef objref）(偏移: 0x8)
- `int SourceDomain`（int SourceDomain）(偏移: 0xC)
- `byte[] TypeInfo`（byte[] 类型信息）(偏移: 0x10)

---

## CADSerializer（CADSerializer）

### 方法 (5)

- `IMessage DeserializeMessage(MemoryStream mem, IMethodCallMessage msg)`
  （IMessage DeserializeMessage（Memory流 mem, IMethodCallMessage msg））
- `MemoryStream SerializeMessage(IMessage msg)`
  （Memory流 SerializeMessage（IMessage msg））
- `object DeserializeObjectSafe(byte[] mem)`
  （object Deserialize对象Safe（byte[] mem））
- `MemoryStream SerializeObject(object obj)`
  （Memory流 Serialize对象（object obj））
- `object DeserializeObject(MemoryStream mem)`
  （object Deserialize对象（Memory流 mem））

---

## CAPI（CAPI）

### 方法 (2)

- `string CryptFindOIDInfoNameFromKey(string key, OidGroup oidGroup)`
  （string Crypt查找OID信息名称From键（string key, Oid组 oidGroup））
- `string CryptFindOIDInfoKeyFromName(string name, OidGroup oidGroup)`
  （string Crypt查找OID信息键From名称（string name, Oid组 oidGroup））

---

## CCDIK（CCDIK）

**继承**: IK（IK反向运动学）

### 字段 (1)

- `IKSolverCCD solver`（IKSolverCCD solver）(偏移: 0x1C)

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

## CDSCollectionETWBCLProvider（CDSCollectionETWBCL提供者）

**继承**: EventSource（事件Source）

### 字段 (1)

- `CDSCollectionETWBCLProvider Log`（CDSCollectionETWBCL提供者 Log）(偏移: 0x0)

### 方法 (1)

- `void ConcurrentDictionary_AcquiringAllLocks(int numOfBuckets)`
  （void ConcurrentDictionary_Acquiring所有Locks（int numOfBuckets））

---

## CFAnimator（CF动画器）

**继承**: Model（模型）

### 字段 (5)

- `SO_AnimationLerpData animLerpData`（SO_动画Lerp数据 animLerp数据）(偏移: 0x44)
- `bool changeMode`（bool change模式）(偏移: 0x54)
- `bool alwaysRunAnim`（bool always运行动画）(偏移: 0x5C)
- `RefString AnimName_Modifier`（Ref字符串 动画Name_修改器）(偏移: 0x60)
- `Coroutine knifeStun`（协程 knife眩晕）(偏移: 0x64)

### 方法 (36)

- `Animator get_characterAnimator()`
  （动画器 get_character动画器（））
- `Animator get_handAnimator()`
  （动画器 get_hand动画器（））
- `Animator get_animator()`
  （动画器 get_animator（））
- `void set_animator(Animator value)`
  （void set_animator（动画器 value））
- `string get_currentAnimName()`
  （string get_current动画名称（））
- `void set_currentAnimName(string value)`
  （void set_current动画名称（string value））
- `string get_currentAnimTag()`
  （string get_current动画标签（））
- `void set_currentAnimTag(string value)`
  （void set_current动画标签（string value））
- `string get_tempAnimName()`
  （string get_temp动画名称（））
- `void set_tempAnimName(string value)`
  （void set_temp动画名称（string value））
- `bool get_isAnimEmptyTag()`
  （bool get_is动画空标签（））
- `bool get_isSelecting()`
  （bool get_isSelecting（））
- `bool get_isReloading()`
  （bool get_isReloading（））
- `bool get_semiGunShooting()`
  （bool get_semi枪械Shooting（））
- `void add_AnimEnd_Listener(Action<string, string> value)`
  （void add_动画End_监听器（Action<string, string> value））
- `void remove_AnimEnd_Listener(Action<string, string> value)`
  （void remove_动画End_监听器（Action<string, string> value））
- `void add_AnimName_Modifier(RefString value)`
  （void add_动画Name_修改器（Ref字符串 value））
- `void remove_AnimName_Modifier(RefString value)`
  （void remove_动画Name_修改器（Ref字符串 value））
- `void Update()`
  （void 更新（））
- `float GetAnimLerpTime(string animName)`
  （float 获取动画Lerp时间（string animName））
- `void PlayAnim(string animName, string animTag, bool isLoopAnim, float offset)`
  （void 播放动画（string animName, string animTag, bool isLoopAnim, float offset））
- `void PlayAnimIfNotPlaying(string animName, string animTag, bool isLoopAnim = False)`
  （void 播放动画IfNotPlaying（string animName, string animTag, bool isLoopAnim = False））
- `void PlayTempAnim(string animName, bool isLoopAnim = False, bool cancelIfPlaying = True, float offset = 0)`
  （void 播放Temp动画（string animName, bool isLoopAnim = False, bool cancelIfPlaying = True, float offset = 0））
- `void PlayWeaponAnimWithSameTag(string animName)`
  （void 播放Weapon动画WithSame标签（string animName））
- `void PlayWeaponAnim(string animName, string animTag)`
  （void 播放Weapon动画（string animName, string animTag））
- `void AnimationEndMessage(AnimatorStateInfo stateInfo)`
  （void 动画结束Message（动画器状态信息 stateInfo））
- `void OnAnimationEnter(string animName, string animTag)`
  （void On动画Enter（string animName, string animTag））
- `void OnAnimationEnd(string animName, string animTag)`
  （void 动画结束时（字符串 animName, 字符串 animTag））
- `void OnAnimationExit(string animName, string animTag)`
  （void On动画Exit（string animName, string animTag））
- `void UpdateRunAnimation()`
  （void 更新运行动画（））
- `void SetFloat(string name, float value, bool character)`
  （void 集合浮点数（string name, float value, bool character））
- `void UpdateAnimator(float deltaTime)`
  （void 更新动画器（float deltaTime））
- `void AnimatorInit()`
  （void 动画器初始化（））
- `void PlayKnifeHitStunAnim(bool isBigshot)`
  （void 播放近战武器命中眩晕动画（bool isBigshot））
- `void ChangeCurAnimToTemp()`
  （void ChangeCur动画ToTemp（））
- `string ModifyAnimName(string animName)`
  （string Modify动画名称（string animName））

---

## CLRConfig（CLR配置）

### 方法 (1)

- `bool CheckThrowUnobservedTaskExceptions()`
  （bool 检查投掷UnobservedTaskExceptions（））

---

## CLSCompliantAttribute（CLSCompliantAttribute）

**继承**: Attribute（属性）

### 字段 (1)

- `bool m_compliant`（bool m_compliant）(偏移: 0x8)

---

## COMException（COMException）

**继承**: ExternalException（外部的Exception）

### 方法 (1)

- `string ToString()`
  （字符串 转字符串（））

---

## CRC32（CRC32）

### 字段 (5)

- `uint dwPolynomial`（uint dwPolynomial）(偏移: 0x8)
- `long _TotalBytesRead`（long _TotalBytesRead）(偏移: 0x10)
- `bool reverseBits`（bool reverseBits）(偏移: 0x18)
- `uint[] crc32Table`（uint[] crc32Table）(偏移: 0x1C)
- `uint _register`（uint _register）(偏移: 0x20)

### 方法 (13)

- `long get_TotalBytesRead()`
  （long get_TotalBytesRead（））
- `int get_Crc32Result()`
  （int get_Crc32Result（））
- `int GetCrc32(Stream input)`
  （int 获取Crc32（流 input））
- `int GetCrc32AndCopy(Stream input, Stream output)`
  （int 获取Crc32And复制（流 input, 流 output））
- `int ComputeCrc32(int W, byte B)`
  （int ComputeCrc32（int W, byte B））
- `int _InternalComputeCrc32(uint W, byte B)`
  （int _内部的ComputeCrc32（uint W, byte B））
- `void SlurpBlock(byte[] block, int offset, int count)`
  （void SlurpBlock（byte[] block, int offset, int count））
- `uint ReverseBits(uint data)`
  （uint ReverseBits（uint data））
- `byte ReverseBits(byte data)`
  （byte ReverseBits（byte data））
- `void GenerateLookupTable()`
  （void GenerateLookupTable（））
- `uint gf2_matrix_times(uint[] matrix, uint vec)`
  （uint gf2_matrix_times（uint[] matrix, uint vec））
- `void gf2_matrix_square(uint[] square, uint[] mat)`
  （void gf2_matrix_square（uint[] square, uint[] mat））
- `void Combine(int crc, int length)`
  （void Combine（int crc, int length））

---

## CStreamReader（C流读取器）

**继承**: StreamReader（流读取器）

### 字段 (1)

- `TermInfoDriver driver`（Term信息Driver driver）(偏移: 0x40)

### 方法 (5)

- `int Peek()`
  （整数 查看（））
- `int Read()`
  （整数 读取（））
- `int Read([In] [Out] char[] dest, int index, int count)`
  （int Read（[In] [Out] char[] dest, int index, int count））
- `string ReadLine()`
  （字符串 读取行（））
- `string ReadToEnd()`
  （字符串 读取到结束（））

---

## CStreamWriter（C流写入器）

**继承**: StreamWriter（流写入器）

### 字段 (1)

- `TermInfoDriver driver`（Term信息Driver driver）(偏移: 0x38)

### 方法 (7)

- `void Write(char[] buffer, int index, int count)`
  （void 写入（字符[] buffer, 整数 index, 整数 count））
- `void Write(char val)`
  （void Write（char val））
- `void InternalWriteString(string val)`
  （void 内部的Write字符串（string val））
- `void InternalWriteChar(char val)`
  （void 内部的WriteChar（char val））
- `void InternalWriteChars(char[] buffer, int n)`
  （void 内部的WriteChars（char[] buffer, int n））
- `void Write(char[] val)`
  （void Write（char[] val））
- `void Write(string val)`
  （void Write（string val））

---

## CachedCodeEntry（CachedCodeEntry）

### 字段 (9)

- `string _key`（string _key）(偏移: 0x8)
- `RegexCode _code`（RegexCode _code）(偏移: 0xC)
- `Hashtable _caps`（哈希表 _caps）(偏移: 0x10)
- `Hashtable _capnames`（Hashtable _capnames）(偏移: 0x14)
- `string[] _capslist`（string[] _capslist）(偏移: 0x18)
- `int _capsize`（int _capsize）(偏移: 0x1C)
- `RegexRunnerFactory _factory`（RegexRunner工厂 _factory）(偏移: 0x20)
- `ExclusiveReference _runnerref`（Exclusive引用 _runnerref）(偏移: 0x24)
- `SharedReference _replref`（Shared引用 _replref）(偏移: 0x28)

---

## Calendar（日历）

**继承**: ICloneable（ICloneable可克隆）

### 字段 (3)

- `int m_currentEraValue`（int m_currentEra值）(偏移: 0x8)
- `bool m_isReadOnly`（布尔值 m_是否只读）(偏移: 0xC)
- `int twoDigitYearMax`（int twoDigitYear最大）(偏移: 0x10)

### 方法 (16)

- `DateTime get_MinSupportedDateTime()`
  （日期时间 获取_最小支持日期时间（））
- `DateTime get_MaxSupportedDateTime()`
  （日期时间 获取_最大支持日期时间（））
- `int get_ID()`
  （整数 获取_ID（））
- `int get_BaseCalendarID()`
  （int get_基础CalendarID（））
- `object Clone()`
  （对象 克隆（））
- `void SetReadOnlyState(bool readOnly)`
  （void 集合ReadOnly状态（bool readOnly））
- `int get_CurrentEraValue()`
  （int get_当前Era值（））
- `bool IsLeapYear(int year)`
  （bool 是否LeapYear（int year））
- `bool TryToDateTime(int year, int month, int day, int hour, int minute, int second, int millisecond, int era, out DateTime result)`
  （bool TryToDate时间（int year, int month, int day, int hour, int minute, int second, int millisecond, int era, out DateTime result））
- `bool IsValidYear(int year, int era)`
  （bool 是否ValidYear（int year, int era））
- `bool IsValidMonth(int year, int month, int era)`
  （bool 是否ValidMonth（int year, int month, int era））
- `bool IsValidDay(int year, int month, int day, int era)`
  （bool 是否ValidDay（int year, int month, int day, int era））
- `int get_TwoDigitYearMax()`
  （整数 获取_两位数年份最大（））
- `int ToFourDigitYear(int year)`
  （整数 转四位数年份（整数 year））
- `long TimeToTicks(int hour, int minute, int second, int millisecond)`
  （long 时间ToTicks（int hour, int minute, int second, int millisecond））
- `int GetSystemTwoDigitYearSetting(int CalID, int defaultYearValue)`
  （int 获取系统TwoDigitYear设置（int CalID, int defaultYearValue））

---

## CalendarData（Calendar数据）

### 字段 (20)

- `string sNativeName`（string sNative名称）(偏移: 0x8)
- `string[] saShortDates`（string[] saShortDates）(偏移: 0xC)
- `string[] saYearMonths`（string[] saYearMonths）(偏移: 0x10)
- `string[] saLongDates`（string[] saLongDates）(偏移: 0x14)
- `string sMonthDay`（string sMonthDay）(偏移: 0x18)
- `string[] saEraNames`（string[] saEraNames）(偏移: 0x1C)
- `string[] saAbbrevEraNames`（string[] saAbbrevEraNames）(偏移: 0x20)
- `string[] saAbbrevEnglishEraNames`（string[] saAbbrevEnglishEraNames）(偏移: 0x24)
- `string[] saDayNames`（string[] saDayNames）(偏移: 0x28)
- `string[] saAbbrevDayNames`（string[] saAbbrevDayNames）(偏移: 0x2C)
- `string[] saSuperShortDayNames`（string[] saSuperShortDayNames）(偏移: 0x30)
- `string[] saMonthNames`（string[] saMonthNames）(偏移: 0x34)
- `string[] saAbbrevMonthNames`（string[] saAbbrevMonthNames）(偏移: 0x38)
- `string[] saMonthGenitiveNames`（string[] saMonthGenitiveNames）(偏移: 0x3C)
- `string[] saAbbrevMonthGenitiveNames`（string[] saAbbrevMonthGenitiveNames）(偏移: 0x40)
- `string[] saLeapYearMonthNames`（string[] saLeapYearMonthNames）(偏移: 0x44)
- `int iTwoDigitYearMax`（int iTwoDigitYear最大）(偏移: 0x48)
- `int iCurrentEra`（int i当前Era）(偏移: 0x4C)
- `bool bUseUserOverrides`（bool bUseUserOverrides）(偏移: 0x50)
- `CalendarData Invariant`（Calendar数据 Invariant）(偏移: 0x0)

### 方法 (7)

- `void InitializeEraNames(string localeName, int calendarId)`
  （void 初始化EraNames（string localeName, int calendarId））
- `void InitializeAbbreviatedEraNames(string localeName, int calendarId)`
  （void 初始化AbbreviatedEraNames（string localeName, int calendarId））
- `CalendarData GetCalendarData(int calendarId)`
  （Calendar数据 获取Calendar数据（int calendarId））
- `string CalendarIdToCultureName(int calendarId)`
  （string CalendarIdToCulture名称（int calendarId））
- `int nativeGetTwoDigitYearMax(int calID)`
  （int native获取TwoDigitYear最大（int calID））
- `bool nativeGetCalendarData(CalendarData data, string localeName, int calendarId)`
  （bool native获取Calendar数据（Calendar数据 data, string localeName, int calendarId））
- `bool fill_calendar_data(string localeName, int datetimeIndex)`
  （bool fill_calendar_data（string localeName, int datetimeIndex））

---

## CalendarId（CalendarId）

### 字段 (1)

- `ushort value__`（ushort value__）(偏移: 0x0)

---

## CallContext（CallContext）

### 方法 (2)

- `object SetCurrentCallContext(LogicalCallContext ctx)`
  （object 集合当前CallContext（LogicalCallContext ctx））
- `LogicalCallContext SetLogicalCallContext(LogicalCallContext callCtx)`
  （LogicalCallContext 集合LogicalCallContext（LogicalCallContext callCtx））

---

## CallContextRemotingData（CallContextRemoting数据）

**继承**: ICloneable（ICloneable可克隆）

### 字段 (1)

- `string _logicalCallID`（string _logicalCallID）(偏移: 0x8)

### 方法 (4)

- `string get_LogicalCallID()`
  （string get_LogicalCallID（））
- `void set_LogicalCallID(string value)`
  （void set_LogicalCallID（string value））
- `bool get_HasInfo()`
  （布尔值 获取_是否有信息（））
- `object Clone()`
  （对象 克隆（））

---

