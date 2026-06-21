# 未生成 HTML 类/类型功能分析

范围：这里只分析“已经出现在当前 10 张字段关系图里，但还没有生成独立 HTML”的类/类型。功能判断来自 `dump.cs` 的类名、字段名、字段类型，以及 Unity/CF 对局语义。

- 未生成项总数：658 个
- 建议优先生成：47 个
- 可按需求生成：611 个
- 暂时可不生成：0 个

## 优先级总览

### 高优先级（47 个）

`BA_Nano_WatchOutTeammate`、`BotTarget`、`HUD_MapGun`、`HUD_Nano4_HumanGauge`、`HUD_Nano4T_Attribute`、`HUD_Nano4T_AttributeIcon`、`HUD_Nano4T_BoxTimer`、`HUD_Nano4T_Critical`、`HUD_Nano6_BuffIcon`、`HUD_Nano6Gauge`、`HUD_NanoDamageScore`、`HUD_NanoDamageScore_Effect`、`HUD_NanoDamageScore_Star`、`HUD_NanoExpGauge`、`HUD_TabScoreBoard_Nano`、`HUD_WeaponSlot`、`HUD_WeaponSlotIndividual`、`MapAsset_Nano`、`MapAsset_TeamDeath`、`MineBotAI`、`MineBotAnimation`、`Mode_Nano4`、`Mode_Nano4_Terminator`、`Mode_Nano6`、`Mode_Nano6.RadioMsg`、`Mode_TeamDeath`、`Nano4T_Attribute`、`Nano4T_AttributeAsset`、`Nano4TerminatorModeAsset`、`Nano6ModeAsset`、`Nano6ModeAsset.UpgradeAsset`、`NanoGhostBreath`、`NanoModeBasicAsset.NameIntArray`、`TestPlayer`、`TSBPD_Nano`、`WeaponData_Gun`、`WeaponData_Knife`、`WPN_ArmoredTerminator`、`WPN_AsceticHero`、`WPN_EvilTerminator`、`WPN_GRENADE`、`WPN_Gun.SemiGunFireLinkState`、`WPN_Prefire`、`WPN_RecoverAmmo`、`WPN_RepeatFire`、`WPN_Rope`、`WPN_StunGrenade2`

### 中优先级（611 个）

`ABPath`、`ACTkDetectorBase`、`AddSimpleRadarIcon`、`AdvancedSmooth.ConstantTurn`、`AdvancedSmooth.MaxTurn`、`AdvancedSmooth.TurnConstructor`、`Agent`、`Agent.VO`、`AIBase`、`AIDestinationSetter`、`AILerp`、`AimController`、`AimPoser.Pose`、`AIPath`、`AmmoRecoverAndDecay`、`Amplifier.Body`、`AnimationCurve`、`AnimationEventReceiver`、`AnimationHud.Anim`、`AnimationLink`、`AnimationLink.LinkClip`、`AnimationPlayableAsset`、`AnimationTrack`、`AnimSFX`、`AsceticHeroSFX`、`AspectRatioFitter`、`AstarColor`、`AstarDebugger`、`AstarSmoothFollow2`、`AsyncOperation`、`AttachFollowEffect`、`AttachSimpleEffect`、`AutoRepathPolicy`、`AxisEventData`、`AxisState`、`AxisState.Recentering`、`Baker`、`BakerHumanoidQT`、`BakerTransform`、`BipedLimbOrientations.LimbOrientation`、`BipedReferences`、`BlendSourceVirtualCamera`、`BlockManager`、`BodyTilt`、`BoundingSphere`、`Bounds`、`CameraCaptureBridge`、`CameraData`、`CameraProperties`、`CameraState`、`CameraSwitcher`、`CanvasScaler`、`CatmullRomDecoder`、`CFAnimator`、`ChangeMovingRealSize`、`CharacterEffect.FxData`、`Cinemachine3rdPersonAim`、`Cinemachine3rdPersonFollow`、`CinemachineBasicMultiChannelPerlin`、`CinemachineBlend`、`CinemachineBlendDefinition`、`CinemachineBlenderSettings`、`CinemachineBlendListCamera`、`CinemachineBrain.BrainEvent`、`CinemachineBrain.BrainFrame`、`CinemachineBrain.BrainUpdateMethod`、`CinemachineBrain.UpdateMethod`、`CinemachineBrain.VcamActivatedEvent`、`CinemachineCameraOffset`、`CinemachineClearShot`、`CinemachineCollider`、`CinemachineCollider.VcamExtraState`、`CinemachineCollisionImpulseSource`、`CinemachineComponentBase`、`CinemachineComposer`、`CinemachineConfiner`、`CinemachineConfiner.VcamExtraState`、`CinemachineCore`、`CinemachineExternalCamera`、`CinemachineFramingTransposer`、`CinemachineFreeLook.Orbit`、`CinemachineHardLockToTarget`、`CinemachineImpulseDefinition.SignalSource`、`CinemachineImpulseManager.ImpulseEvent`、`CinemachineIndependentImpulseListener`、`CinemachineMixer`、`CinemachineMixingCamera`、`CinemachineOrbitalTransposer`、`CinemachineOrbitalTransposer.Heading`、`CinemachinePath.Waypoint`、`CinemachinePathBase.Appearance`、`CinemachineSmoothPath.Waypoint`、`CinemachineStateDrivenCamera`、`CinemachineStoryboard`、`CinemachineStoryboard.CanvasInfo`、`CinemachineTargetGroup`、`CinemachineTargetGroup.Target`、`CinemachineTrackedDolly`、`CinemachineTransposer`、`CinemachineTransposer.BindingMode`、`CinemachineTriggerAction`、`CinemachineVirtualCameraBase`、`CinemachineVirtualCameraBase.BlendHint`、`CinemachineVirtualCameraBase.TransitionParams`、`CinemachineVolumeSettings`、`CinemachineVolumeSettings.VcamExtraState`、`CircleOptions`、`ClipBuff`、`Collider`、`Collision`、`Collision2D`、`Color2`、`ColorBlock`、`ColorGradingLutPass`、`ColorParameter`、`ColorTween`、`CommonHud_1.Type`、`ComponentDataBase`、`Connection`、`ConstantPath`、`Constraint`、`ConstraintPosition`、`ConstraintPositionOffset`、`Constraints`、`ContactPoint`、`ContactPoint2D`、`ContentSizeFitter`、`ControllerColliderHit`、`ControlPoint`、`Cookie`、`CopyColorPass`、`CopyDepthPass`、`Core`、`CoreUtils`、`CriticalDamageText`、`CubicBezierDecoder`、`CustomTexSheet`、`DataBaseExample.ChildTest`、`DebugManager`、`DebugUIHandlerBitField`、`DebugUIHandlerButton`、`DebugUIHandlerCanvas`、`DebugUIHandlerColor`、`DebugUIHandlerContainer`、`DebugUIHandlerEnumField`、`DebugUIHandlerEnumHistory`、`DebugUIHandlerFloatField`、`DebugUIHandlerFoldout`、`DebugUIHandlerGroup`、`DebugUIHandlerIndirectFloatField`、`DebugUIHandlerIndirectToggle`、`DebugUIHandlerIntField`、`DebugUIHandlerPanel`、`DebugUIHandlerPersistentCanvas`、`DebugUIHandlerToggle`、`DebugUIHandlerUIntField`、`DebugUIHandlerValue`、`DebugUIHandlerVector2`、`DebugUIHandlerVector3`、`DebugUIHandlerVector4`、`DebugUIHandlerWidget`、`DebugUIPrefabBundle`、`DefaultControls`、`DefaultControls.Resources`、`DeferredLights`、`DelayOneShootData`、`DemoGUIMessage`、`DirectionalLight`、`DiscLight`、`Dropdown`、`Dropdown.DropdownItem`、`Dropdown.OptionData`、`DynamicGridObstacle`、`DynamicResolutionHandler`、`EffectAsset.EffectData`、`EffectManager`、`EffectTester`、`EuclideanEmbedding`、`EventSystem`、`ExecuteEvents`、`FBBIKArmBending`、`FBBIKHeadEffector`、`FBBIKHeadEffector.BendBone`、`FBIKChain.ChildConstraint`、`FinalBlitPass`、`Finger`、`FKOffset`、`FKOffset.Offset`、`FloatParameter`、`FloodPath`、`Font`、`FontData`、`FontUpdateTracker`、`ForwardRenderer`、`ForwardRendererData.ShaderResources`、`Funnel.FunnelPortals`、`Funnel.PathPart`、`GameAsset`、`GenericBaker`、`GenericPoser.Map`、`GhostBladeOneShinePass`、`GradientColorKey`、`GraphCollision`、`GraphGizmoHelper`、`GraphHitInfo`、`Graphic`、`GraphMask`、`GraphSerializationContext`、`GraphTransform`、`GraphUpdateObject`、`GraphUpdateScene`、`GraphUpdateShape`、`GridGraph`、`GridGraph.TextureData`、`GridLayoutGroup`、`GrounderBipedIK`、`GrounderFBBIK`、`GrounderIK`、`GrounderQuadruped`、`GrounderQuadruped.Foot`、`GrounderVRIK`、`Grounding`、`Grounding.Leg`、`Grounding.Pelvis`、`GUIContent`、`GUISettings`、`HandPoser`、`Hashtable`、`HeadingTracker`、`HeadingTracker.Item`、`Heuristic`、`HierarchicalGraph`、`HitReaction.HitPoint`、`HitReaction.HitPointBone`、`HitReaction.HitPointBone.BoneLink`、`HitReaction.HitPointEffector.EffectorLink`、`HitReactionVRIK.Offset`、`HitReactionVRIK.PositionOffset.PositionOffsetLink`、`HitReactionVRIK.RotationOffset`、`HUD_BagButton`、`HUD_ChatBox`、`HUD_Cheat`、`HUD_CheatChoice`、`HUD_CommonMsg`、`HUD_Crosshair.Type`、`HUD_DamageArrow`、`HUD_EscMenu`、`HUD_GameResult`、`HUD_Gauge`、`HUD_Gauge_EvilFire`、`HUD_KillMark`、`HUD_KillMark.ShowType`、`HUD_KillMarkUnder`、`HUD_KillMsg`、`HUD_KillMsgIndividual`、`HUD_ProjectionID`、`HUD_ProjectionSign`、`HUD_Radar`、`HUD_RadarIcon`、`HUD_RadarIcon_SupplyBox`、`HUD_ScreenFX`、`HUD_SkillBtn`、`HUD_Spectate`、`HUD_SpectateMsg`、`HUD_SupplyBoxSign`、`HUD_TabScoreBoard_DM`、`HUD_TabScoreBoard_TD`、`HUD_TerminatorSign`、`HumanCatchFeature`、`HumanCatchPass`、`HumanLimit`、`HumanoidBaker`、`HumanPose`、`ICinemachineCamera`、`IKConstraintBend`、`IKEffector`、`IKExecutionOrder`、`IKMapping.BoneMap`、`IKMappingBone`、`IKMappingLimb`、`IKMappingSpine`、`IKSolver`、`IKSolver.Bone`、`IKSolver.Node`、`IKSolver.Point`、`IKSolverAim`、`IKSolverArm`、`IKSolverFABRIK`、`IKSolverFABRIKRoot`、`IKSolverFullBodyBiped`、`IKSolverHeuristic`、`IKSolverLeg`、`IKSolverLimb`、`IKSolverLimb.AxisDirection`、`IKSolverLookAt`、`IKSolverLookAt.LookAtBone`、`IKSolverTrigonometric`、`IKSolverTrigonometric.TrigonometricBone`、`IKSolverVR`、`IKSolverVR.Arm`、`IKSolverVR.BodyPart`、`IKSolverVR.Footstep`、`IKSolverVR.Leg`、`IKSolverVR.Locomotion`、`IKSolverVR.Spine`、`IKSolverVR.VirtualBone`、`Image.FillMethod`、`Image.Type`、`Inertia.Body`、`InputField`、`Int3`、`InteractionEffector`、`InteractionLookAt`、`InteractionObject`、`InteractionObject.AnimatorEvent`、`InteractionObject.Message`、`InteractionSystem`、`InteractionTarget`、`InteractionTrigger.CameraPosition`、`InteractionTrigger.CharacterPosition`、`IPathModifier`、`ITraversalProvider`、`KillMarkAsset`、`KnifeAttackData`、`LayerGridGraph.HeightSample`、`LayerMask`、`LayoutGroup`、`LayoutRebuilder`、`LegacyAIPath`、`LegacyRichAI`、`LensSettings`、`Light2D`、`Light2DLookupTexture`、`LightDataGI`、`LightUtility.ParametricLightMeshVertex`、`LightUtility.SpriteLightMeshVertex`、`Line`、`LODParameters`、`LookAtController`、`LoopRotate`、`MapEffectShooter`、`Mask`、`MaskableGraphic`、`MasterHeroSkillFX`、`MaterialEntry`、`MecanimBridge`、`MeshSubsetCombineUtility.MeshContainer`、`MissileData`、`Mode_DeathMatch`、`Model.Socket`、`MonoModifier`、`Msl_EvilFire`、`MultiTargetPath`、`Navigator`、`NavmeshAdd`、`NavmeshBase`、`NavmeshCut`、`NavMeshGraph`、`NavMeshHit`、`NavMeshPath`、`NestedExample`、`NNConstraint`、`NNInfo`、`NNInfoInternal`、`NodeLink`、`NodeLink2`、`NodeLink3`、`NodeLink3Node`、`ObjectPlacer`、`ObjectPool`、`ObjImporter.meshStruct`、`ObscuredTypesExamples`、`ObscuredVector2`、`ObscuredVector2Int`、`ObscuredVector3`、`ObscuredVector3Int`、`ObstacleVertex`、`OffsetPose.EffectorLink`、`ParticleSpaceSetter`、`ParticleSystem.MainModule`、`ParticleSystem.Particle`、`PathCompleteState`、`PathEndingCondition`、`PathHandler`、`PathModifier`、`PathNode`、`PathOptions`、`PathPool`、`PathReturnQueue`、`PathState`、`PathUtilities`、`Patrol`、`PenetrationAvoidance.Avoider`、`PhysicsRaycaster`、`PixelPerfectCamera`、`Plane`、`PointerEventData`、`PointGraph`、`PointKDTree`、`PointKDTree.Node`、`PointLight`、`PointNode`、`PointNodeTagModifier`、`Poser`、`PositionPredictor`、`PostProcessData`、`PostProcessData.TextureResources`、`PostProcessPass`、`PostProcessPass.MaterialLibrary`、`PostureFloat`、`ProceduralGridMover`、`ProceduralWorld`、`ProceduralWorld.ProceduralPrefab`、`ProceduralWorld.ProceduralTile`、`PunctualLightData`、`QuaternionOptions`、`Queue`、`QVModel.Data`、`RagdollUtility`、`RagdollUtility.Child`、`RagdollUtility.Rigidbone`、`Random`、`RandomItem`、`RandomPath`、`RasterizationMesh`、`Ray`、`RaycastHit2D`、`RaycastModifier`、`RaycastResult`、`RecastGraph`、`RecastMeshGatherer`、`RecastMeshGatherer.CapsuleCache`、`Recoil.RecoilOffset`、`Rect`、`RectangleLight`、`RectangularVertexClipper`、`RectMask2D`、`RectTransformUtility`、`RelevantGraphSurface`、`Renderer2D`、`Renderer2DData`、`RendererLighting`、`RendererListDesc`、`RenderingMode`、`RenderingUtils`、`RenderObjects.RenderObjectsSettings`、`RenderObjectsPass`、`RenderPipelineManager`、`RequiredReferences`、`RetainedGizmos`、`RetainedGizmos.Builder`、`RichAI`、`RichFunnel`、`RichPath`、`RichSpecial`、`RopeTrigger`、`RotationLimit`、`RotationLimitPolygonal`、`RotationLimitPolygonal.LimitPoint`、`RotationLimitPolygonal.ReachCone`、`RTHandle`、`RTHandleProperties`、`RuntimeUtility`、`RVOController`、`RVOObstacle`、`RVOQuadtree.QuadtreeQuery`、`RVOSquareObstacle`、`SceneViewDepthCopyPass`、`ScreenSpaceAmbientOcclusion`、`ScreenSpaceAmbientOcclusion.ScreenSpaceAmbientOcclusionPass`、`ScreenSpaceShadowResolvePass`、`ScriptableCullingParameters`、`ScriptableRenderer`、`ScriptableRendererData`、`ScriptableRenderPass`、`Scrollbar`、`ScrollRect`、`SendMouseEvents`、`SendMouseEvents.HitInfo`、`SentryGunSystem`、`Shadow`、`ShadowCaster2D`、`ShadowData`、`ShootPosture`、`SideReactDirect`、`SimpleHudBase`、`Simulator.WorkerContext`、`SingleNodeBlocker`、`SkeletonBone`、`Slider`、`SO_2dSound`、`SO_3dSound`、`SO_FxGroup.FxData`、`SO_Item`、`SO_Item_Wpn`、`SO_Item_Wpn_Throw`、`SocketItem`、`SoftMask`、`SoftMaskable`、`SolverManager`、`SortingSettings`、`SoundManager`、`SpawnOverDistance`、`SpawnOverDistance.InputProperties`、`SpotLight`、`SpriteBone`、`SpriteIntermediateRendererInfo`、`SpriteState`、`StandaloneInputModule`、`StartEndModifier`、`StaticPointVirtualCamera`、`StencilMaterial.MatEntry`、`StencilStateData`、`StunGrenadeArea`、`StunGrenadeSFX`、`TargetMover`、`TargetPositionCache`、`TargetPositionCache.CacheCurve.Item`、`TerminatorCharacterEffect`、`TerrainUtility.TerrainMap`、`TextEditor`、`TextGenerationSettings`、`TextGenerator`、`TextureAnimation`、`TextureCurve`、`TextureDesc`、`TextureXR`、`ThermalVisionPass`、`ThreadControlQueue`、`Tile`、`TileAnimationData`、`Touch`、`TouchInputModule`、`TQ`、`TrackColorAttribute`、`Transform.Enumerator`、`TreeInstance`、`TreePrototype`、`TriggerEnterSound`、`TriggerEventBroadcaster`、`TSBPD_DM`、`TSBPD_TD`、`TurnBasedAI`、`TweenLink`、`TwistRelaxer`、`UI_GameLoading`、`UI_Inven`、`UI_InvenItem`、`UI_ItemBox`、`UI_ItemBox_Throw`、`UI_ItemPanel`、`UI_Option`、`UI_SelectionGroup`、`UI_SliderValueText`、`UI_Tab`、`UI_Tab2`、`UI_TopMenu`、`UICharInfo`、`UIFoldout`、`UIVertex`、`UniversalAdditionalCameraData`、`UniversalRenderPipeline`、`UniversalRenderPipelineAsset`、`UniversalRenderPipelineEditorResources.MaterialResources`、`UpdateTracker`、`Vector4`、`VertexHelper`、`VFXAudioSpectrumBinder`、`VFXEnabledBinder`、`VFXHierarchyAttributeMapBinder`、`VFXHierarchyAttributeMapBinder.Bone`、`VFXInputMouseBinder`、`VFXInputTouchBinder`、`VFXMultiplePositionBinder`、`VFXPlaneBinder`、`VFXPositionBinder`、`VFXPreviousPositionBinder`、`VFXRaycastBinder`、`VFXTransformBinder`、`VFXVelocityBinder`、`VisibleLight`、`VisibleReflectionProbe`、`Volume`、`VolumeComponent`、`VoxelArea`、`Voxelize`、`VRIK.References`、`VRIKCalibrator.CalibrationData`、`VRIKCalibrator.CalibrationData.Target`、`VRIKCalibrator.Settings`、`VRIKLODController`、`VRIKRootController`、`WaitForFixedUpdate`、`WallHackDetector`、`WD_AsceticHero`、`WD_EvilTerminator`、`WD_GrenadeGun`、`WD_MasterHero`、`WD_MasterHunter`、`WD_MechanicHero`、`WD_Missile`、`WD_RPG`、`WD_SentryGun`、`WD_SkillKnife`、`WD_VoidTerminator`、`XRLayout`、`XRNodeState`、`XRPass`、`XRSystem`、`XRSystemData`、`ZoomAction.ZoomData`

### 低优先级（0 个）



## 详细分析

### 高优先级

#### BA_Nano_WatchOutTeammate

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Collider`、`Transform`
- 字段依据示例：-

#### BotTarget

- 功能分析：Bot 路径/目标点数据：辅助 AI 移动和战术路线
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`GameObject`
- 字段依据示例：-

#### HUD_MapGun

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`GameObject`、`RawImage`、`Text`
- 字段依据示例：-

#### HUD_Nano4_HumanGauge

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Mode_Nano4`
- 它保存了哪些类型：7 个，`AnimationHud`、`AudioClip`、`GameObject`、`Image`、`RawImage`、`Text`、`Texture`
- 字段依据示例：`Mode_Nano4` -> `humanGauge`: `HUD_Nano4_HumanGauge`

#### HUD_Nano4T_Attribute

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Mode_Nano4_Terminator`
- 它保存了哪些类型：5 个，`GameObject`、`HUD_Nano4T_AttributeIcon`、`Image`、`Sprite`、`Text`
- 字段依据示例：`Mode_Nano4_Terminator` -> `hud_Attribute`: `HUD_Nano4T_Attribute`

#### HUD_Nano4T_AttributeIcon

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`HUD_Nano4T_Attribute`
- 它保存了哪些类型：5 个，`Image`、`Nano4T_Attribute`、`RectTransform`、`Text`、`Vector2`
- 字段依据示例：`HUD_Nano4T_Attribute` -> `nanoIcon`: `HUD_Nano4T_AttributeIcon`；`humanIcon`: `HUD_Nano4T_AttributeIcon`

#### HUD_Nano4T_BoxTimer

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Text`
- 字段依据示例：-

#### HUD_Nano4T_Critical

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`GameObject`、`SimpleObjectPool`
- 字段依据示例：-

#### HUD_Nano6_BuffIcon

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Image`、`Vector3`
- 字段依据示例：-

#### HUD_Nano6Gauge

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`Image`、`RectTransform`、`Sprite`
- 字段依据示例：-

#### HUD_NanoDamageScore

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：8 个，`AnimationHud`、`CommonKillMark`、`GameObject`、`Queue`、`RawImage`、`RectTransform`、`SimpleObjectPool`、`Texture`
- 字段依据示例：-

#### HUD_NanoDamageScore_Effect

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`RawImage`、`RectTransform`、`Vector3`
- 字段依据示例：-

#### HUD_NanoDamageScore_Star

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`RawImage`、`RectTransform`、`Vector2`
- 字段依据示例：-

#### HUD_NanoExpGauge

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`GameObject`
- 字段依据示例：-

#### HUD_TabScoreBoard_Nano

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`HUD_TabScoreBoard_Nano`
- 它保存了哪些类型：3 个，`HUD_TabScoreBoard_Nano`、`SerializableDictionaryBase`、`Texture`
- 字段依据示例：`HUD_TabScoreBoard_Nano` -> `instance2`: `HUD_TabScoreBoard_Nano`

#### HUD_WeaponSlot

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`HUD_WeaponSlotIndividual`、`RawImage`、`Texture2D`、`Vector2`
- 字段依据示例：-

#### HUD_WeaponSlotIndividual

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`HUD_WeaponSlot`
- 它保存了哪些类型：4 个，`Color`、`RawImage`、`RectTransform`、`Vector2`
- 字段依据示例：`HUD_WeaponSlot` -> `slots`: `HUD_WeaponSlotIndividual[]`

#### MapAsset_Nano

- 功能分析：资源索引类型：保存可加载资源、图标、预制体或表现素材引用
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector2Int`
- 字段依据示例：-

#### MapAsset_TeamDeath

- 功能分析：资源索引类型：保存可加载资源、图标、预制体或表现素材引用
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector2Int`
- 字段依据示例：-

#### MineBotAI

- 功能分析：AI 行为类型：用于电脑角色、代理移动、决策或目标选择
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Animation`、`GameObject`
- 字段依据示例：-

#### MineBotAnimation

- 功能分析：AI 行为类型：用于电脑角色、代理移动、决策或目标选择
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`Animator`、`GameObject`、`IAstarAI`、`Transform`、`Vector3`
- 字段依据示例：-

#### Mode_Nano4

- 功能分析：具体玩法模式类：实现某种模式的规则和流程
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Mode_Nano4`
- 它保存了哪些类型：4 个，`CommonHud_1`、`HUD_Nano4_HumanGauge`、`Mode_Nano4`、`Vector2`
- 字段依据示例：`Mode_Nano4` -> `<instance3>k__BackingField`: `Mode_Nano4`

#### Mode_Nano4_Terminator

- 功能分析：具体玩法模式类：实现某种模式的规则和流程
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：7 个，`CommonHud_1`、`HUD_Nano4T_Attribute`、`HUD_UpgradeBoxTip`、`Nano4T_Attribute`、`Nano4T_AttributeAsset`、`Nano4TerminatorModeAsset`、`SimpleObjectPool`
- 字段依据示例：-

#### Mode_Nano6

- 功能分析：具体玩法模式类：实现某种模式的规则和流程
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：10 个，`AudioSource`、`CommonHud_1`、`Coroutine`、`GameObject`、`HUD_ProjectionSign`、`Image`、`Mode_Nano6.RadioMsg`、`Nano6ModeAsset` 等 10 个
- 字段依据示例：-

#### Mode_Nano6.RadioMsg

- 功能分析：具体玩法模式类：实现某种模式的规则和流程
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Mode_Nano6`
- 它保存了哪些类型：1 个，`AudioClip`
- 字段依据示例：`Mode_Nano6` -> `radioPlayList`: `List<Mode_Nano6.RadioMsg>`

#### Mode_TeamDeath

- 功能分析：具体玩法模式类：实现某种模式的规则和流程
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`AudioClip`、`CommonHud_1`、`GameObject`
- 字段依据示例：-

#### Nano4T_Attribute

- 功能分析：纳米模式相关类型：处理终结者/幽灵玩法数据或行为
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：4 个，`HUD_Nano4T_AttributeIcon`、`Mode_Nano4_Terminator`、`Nano4T_Attribute`、`Nano4T_AttributeAsset`
- 它保存了哪些类型：2 个，`Nano4T_Attribute`、`Sprite`
- 字段依据示例：`HUD_Nano4T_AttributeIcon` -> `<attribute>k__BackingField`: `Nano4T_Attribute`；`Mode_Nano4_Terminator` -> `attribute_Nano`: `Nano4T_Attribute`；`attribute_Human`: `Nano4T_Attribute`；`Nano4T_Attribute` -> `None`: `Nano4T_Attribute`；`Nano4T_AttributeAsset` -> `attributes`: `Nano4T_Attribute[]`

#### Nano4T_AttributeAsset

- 功能分析：纳米模式相关类型：处理终结者/幽灵玩法数据或行为
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Mode_Nano4_Terminator`
- 它保存了哪些类型：3 个，`GameObject`、`Nano4T_Attribute`、`Nano4T_AttributeAsset.Group`
- 字段依据示例：`Mode_Nano4_Terminator` -> `attributeAsset`: `Nano4T_AttributeAsset`

#### Nano4TerminatorModeAsset

- 功能分析：纳米模式相关类型：处理终结者/幽灵玩法数据或行为
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Mode_Nano4_Terminator`
- 它保存了哪些类型：4 个，`AudioClip`、`GameObject`、`RandomItem`、`Sprite`
- 字段依据示例：`Mode_Nano4_Terminator` -> `realAsset`: `Nano4TerminatorModeAsset`

#### Nano6ModeAsset

- 功能分析：纳米模式相关类型：处理终结者/幽灵玩法数据或行为
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Mode_Nano6`
- 它保存了哪些类型：4 个，`AudioClip`、`Nano6ModeAsset.UpgradeAsset`、`Sprite`、`Texture`
- 字段依据示例：`Mode_Nano6` -> `realAsset`: `Nano6ModeAsset`

#### Nano6ModeAsset.UpgradeAsset

- 功能分析：纳米模式相关类型：处理终结者/幽灵玩法数据或行为
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`Nano6ModeAsset`、`Nano6ModeAsset.UpgradeAsset`
- 它保存了哪些类型：3 个，`Nano6ModeAsset.UpgradeAsset`、`Sprite`、`TargetPos`
- 字段依据示例：`Nano6ModeAsset` -> `up_Soldier_1`: `Nano6ModeAsset.UpgradeAsset`；`up_Soldier_2`: `Nano6ModeAsset.UpgradeAsset`；`up_Nano_1`: `Nano6ModeAsset.UpgradeAsset`；`Nano6ModeAsset.UpgradeAsset` -> `iconAnimTarget`: `Nano6ModeAsset.UpgradeAsset.TargetPos[]`

#### NanoGhostBreath

- 功能分析：纳米模式相关类型：处理终结者/幽灵玩法数据或行为
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`AudioClip`、`AudioSource`
- 字段依据示例：-

#### NanoModeBasicAsset.NameIntArray

- 功能分析：纳米模式相关类型：处理终结者/幽灵玩法数据或行为
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`NanoModeBasicAsset`
- 它保存了哪些类型：0 个，-
- 字段依据示例：`NanoModeBasicAsset` -> `wpnList`: `List<NanoModeBasicAsset.NameIntArray>`

#### TestPlayer

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Seeker`、`Transform`
- 字段依据示例：-

#### TSBPD_Nano

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`RawImage`、`Text`
- 字段依据示例：-

#### WeaponData_Gun

- 功能分析：武器相关类型：用于武器数据、发射逻辑、弹药、投掷物或特殊武器表现
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`WPN_Gun`
- 它保存了哪些类型：9 个，`AmmoRecoverAndDecay`、`ChangeMovingRealSize`、`DamageBodyRatio`、`DelayOneShootData`、`KnifeAttackData`、`PostureFloat`、`SideReactDirect`、`Vector3` 等 9 个
- 字段依据示例：`WPN_Gun` -> `realData`: `WeaponData_Gun`

#### WeaponData_Knife

- 功能分析：武器相关类型：用于武器数据、发射逻辑、弹药、投掷物或特殊武器表现
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`DamageBodyRatio`、`KnifeAttackData`、`Vector3`
- 字段依据示例：-

#### WPN_ArmoredTerminator

- 功能分析：武器逻辑类：处理特定武器的攻击、表现或特殊效果
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`GameObject`、`Skill_Common`
- 字段依据示例：-

#### WPN_AsceticHero

- 功能分析：武器逻辑类：处理特定武器的攻击、表现或特殊效果
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`RecyclableObject`、`Skill_Common`、`WD_AsceticHero`
- 字段依据示例：-

#### WPN_EvilTerminator

- 功能分析：武器逻辑类：处理特定武器的攻击、表现或特殊效果
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`EffectObj`、`RecyclableSound`、`Skill_Common`、`WD_EvilTerminator`
- 字段依据示例：-

#### WPN_GRENADE

- 功能分析：武器逻辑类：处理特定武器的攻击、表现或特殊效果
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`GameObject`
- 字段依据示例：-

#### WPN_Gun.SemiGunFireLinkState

- 功能分析：武器逻辑类：处理特定武器的攻击、表现或特殊效果
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 enum 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：0 个，-
- 字段依据示例：-

#### WPN_Prefire

- 功能分析：武器逻辑类：处理特定武器的攻击、表现或特殊效果
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`WPN_Gun`
- 字段依据示例：-

#### WPN_RecoverAmmo

- 功能分析：武器逻辑类：处理特定武器的攻击、表现或特殊效果
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`WPN_Gun`
- 字段依据示例：-

#### WPN_RepeatFire

- 功能分析：武器逻辑类：处理特定武器的攻击、表现或特殊效果
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Coroutine`、`RepeatFireData`
- 字段依据示例：-

#### WPN_Rope

- 功能分析：武器逻辑类：处理特定武器的攻击、表现或特殊效果
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`GameObject`、`Vector3`
- 字段依据示例：-

#### WPN_StunGrenade2

- 功能分析：武器逻辑类：处理特定武器的攻击、表现或特殊效果
- 建议价值：高。和对局规则、玩家/Bot、武器、伤害、地图点位直接相关，适合优先继续生成独立关系图。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`GameObject`
- 字段依据示例：-

### 中优先级

#### ABPath

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`ABPathEndingCondition`、`AILerp`
- 它保存了哪些类型：6 个，`GraphNode`、`GridNode`、`Int3`、`NNConstraint`、`PathNode`、`Vector3`
- 字段依据示例：`ABPathEndingCondition` -> `abPath`: `ABPath`；`AILerp` -> `path`: `ABPath`

#### ACTkDetectorBase

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`GameObject`、`UnityEvent`
- 字段依据示例：-

#### AddSimpleRadarIcon

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Sprite`
- 字段依据示例：-

#### AdvancedSmooth.ConstantTurn

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`AdvancedSmooth`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`AdvancedSmooth` -> `turnConstruct2`: `AdvancedSmooth.ConstantTurn`

#### AdvancedSmooth.MaxTurn

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`AdvancedSmooth`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`AdvancedSmooth` -> `turnConstruct1`: `AdvancedSmooth.MaxTurn`

#### AdvancedSmooth.TurnConstructor

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`AdvancedSmooth.Turn`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`AdvancedSmooth.Turn` -> `constructor`: `AdvancedSmooth.TurnConstructor`

#### Agent

- 功能分析：AI 行为类型：用于电脑角色、代理移动、决策或目标选择
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：4 个，`Agent`、`RVOQuadtree.Node`、`RVOQuadtree.QuadtreeQuery`、`Simulator`
- 它保存了哪些类型：5 个，`Agent`、`ObstacleVertex`、`RVOLayer`、`Simulator`、`Vector2`
- 字段依据示例：`Agent` -> `next`: `Agent`；`neighbours`: `List<Agent>`；`RVOQuadtree.Node` -> `linkedList`: `Agent`；`RVOQuadtree.QuadtreeQuery` -> `agent`: `Agent`；`Simulator` -> `agents`: `List<Agent>`

#### Agent.VO

- 功能分析：AI 行为类型：用于电脑角色、代理移动、决策或目标选择
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Agent.VOBuffer`
- 它保存了哪些类型：1 个，`Vector2`
- 字段依据示例：`Agent.VOBuffer` -> `buffer`: `Agent.VO[]`

#### AIBase

- 功能分析：AI 行为类型：用于电脑角色、代理移动、决策或目标选择
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：13 个，`CharacterController`、`Color`、`IMovementPlane`、`LayerMask`、`OrientationMode`、`Quaternion`、`RVOController`、`Rigidbody` 等 13 个
- 字段依据示例：-

#### AIDestinationSetter

- 功能分析：AI 行为类型：用于电脑角色、代理移动、决策或目标选择
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`IAstarAI`、`Transform`
- 字段依据示例：-

#### AILerp

- 功能分析：AI 行为类型：用于电脑角色、代理移动、决策或目标选择
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：7 个，`ABPath`、`OrientationMode`、`PathInterpolator`、`Quaternion`、`Seeker`、`Transform`、`Vector3`
- 字段依据示例：-

#### AimController

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`AimIK`、`Transform`、`Vector3`
- 字段依据示例：-

#### AimPoser.Pose

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`AimPoser`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`AimPoser` -> `poses`: `AimPoser.Pose[]`

#### AIPath

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`CloseToDestinationMode`、`NNConstraint`、`Path`、`PathInterpolator`
- 字段依据示例：-

#### AmmoRecoverAndDecay

- 功能分析：武器相关类型：用于武器数据、发射逻辑、弹药、投掷物或特殊武器表现
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`Recoil`、`WeaponData_Gun`
- 它保存了哪些类型：1 个，`AmmoRecoverAndDecay.Data`
- 字段依据示例：`Recoil` -> `shotReactYaw`: `AmmoRecoverAndDecay`；`shotReactPitch`: `AmmoRecoverAndDecay`；`WeaponData_Gun` -> `shotReactYaw`: `AmmoRecoverAndDecay[]`；`shotReactPitch`: `AmmoRecoverAndDecay[]`；`cameraYawAndPitch`: `AmmoRecoverAndDecay[]`

#### Amplifier.Body

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`Amplifier`、`Amplifier.Body`
- 它保存了哪些类型：4 个，`Amplifier.Body`、`EffectorLink`、`Transform`、`Vector3`
- 字段依据示例：`Amplifier` -> `bodies`: `Amplifier.Body[]`；`Amplifier.Body` -> `effectorLinks`: `Amplifier.Body.EffectorLink[]`

#### AnimationCurve

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：20 个，`BakerHumanoidQT`、`BakerMuscle`、`BakerTransform`、`CinemachineBlend`、`CinemachineBlendDefinition`、`CinemachineBrain`、`CinemachineFixedSignal`、`CinemachineImpulseManager.EnvelopeDefinition` 等 20 个
- 它保存了哪些类型：0 个，-
- 字段依据示例：`BakerHumanoidQT` -> `rotX`: `AnimationCurve`；`rotY`: `AnimationCurve`；`rotZ`: `AnimationCurve`；`BakerMuscle` -> `curve`: `AnimationCurve`；`BakerTransform` -> `posX`: `AnimationCurve`；`posY`: `AnimationCurve`；`posZ`: `AnimationCurve`；`CinemachineBlend` -> `<BlendCurve>k__BackingField`: `AnimationCurve`；`CinemachineBlendDefinition` -> `m_CustomCurve`: `AnimationCurve`；`sStandardCurves`: `AnimationCurve[]`；另有 15 个来源

#### AnimationEventReceiver

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`Model`、`ParticleSystem`、`SO_FxGroup`
- 字段依据示例：-

#### AnimationHud.Anim

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`AnimationHud`
- 它保存了哪些类型：2 个，`Sprite`、`Texture`
- 字段依据示例：`AnimationHud` -> `animations`: `AnimationHud.Anim[]`

#### AnimationLink

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`AnimationLink.LinkClip`、`GameObject`
- 字段依据示例：-

#### AnimationLink.LinkClip

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`AnimationLink`
- 它保存了哪些类型：2 个，`AnimationClip`、`Vector3`
- 字段依据示例：`AnimationLink` -> `sequence`: `AnimationLink.LinkClip[]`

#### AnimationPlayableAsset

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：6 个，`AnimationClip`、`AnimationPlayableAsset.LoopMode`、`AppliedOffsetMode`、`MatchTargetFields`、`Quaternion`、`Vector3`
- 字段依据示例：-

#### AnimationTrack

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：10 个，`AnimationClip`、`AnimationPlayableAsset.LoopMode`、`AvatarMask`、`MatchTargetFields`、`Quaternion`、`Queue`、`TimelineClip.ClipExtrapolation`、`TrackOffset` 等 10 个
- 字段依据示例：-

#### AnimSFX

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`RawImage`
- 字段依据示例：-

#### AsceticHeroSFX

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Texture`
- 字段依据示例：-

#### AspectRatioFitter

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`AspectRatioFitter.AspectMode`、`DrivenRectTransformTracker`、`RectTransform`
- 字段依据示例：-

#### AstarColor

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`AstarPath`
- 它保存了哪些类型：1 个，`Color`
- 字段依据示例：`AstarPath` -> `colorSettings`: `AstarColor`

#### AstarDebugger

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：7 个，`AstarDebugger.GraphPoint`、`AstarDebugger.PathTypeDebug`、`Camera`、`Font`、`GUIStyle`、`Rect`、`StringBuilder`
- 字段依据示例：-

#### AstarSmoothFollow2

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Transform`
- 字段依据示例：-

#### AsyncOperation

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`UI_GameRoom`
- 它保存了哪些类型：0 个，-
- 字段依据示例：`UI_GameRoom` -> `gameSceneAsync`: `AsyncOperation`

#### AttachFollowEffect

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`GameObject`、`Vector3`
- 字段依据示例：-

#### AttachSimpleEffect

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`GameObject`、`Vector3`
- 字段依据示例：-

#### AutoRepathPolicy

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`AutoRepathPolicy.Mode`、`Vector3`
- 字段依据示例：-

#### AxisEventData

- 功能分析：配置/数据类型：保存运行参数、资源引用、显示数据或系统配置
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`BaseInputModule`
- 它保存了哪些类型：2 个，`MoveDirection`、`Vector2`
- 字段依据示例：`BaseInputModule` -> `m_AxisEventData`: `AxisEventData`

#### AxisState

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`CinemachineFreeLook`、`CinemachineOrbitalTransposer`、`CinemachinePOV`
- 它保存了哪些类型：3 个，`AxisState.IInputAxisProvider`、`AxisState.Recentering`、`AxisState.SpeedMode`
- 字段依据示例：`CinemachineFreeLook` -> `m_YAxis`: `AxisState`；`m_XAxis`: `AxisState`；`CinemachineOrbitalTransposer` -> `m_XAxis`: `AxisState`；`CinemachinePOV` -> `m_VerticalAxis`: `AxisState`；`m_HorizontalAxis`: `AxisState`

#### AxisState.Recentering

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：4 个，`AxisState`、`CinemachineFreeLook`、`CinemachineOrbitalTransposer`、`CinemachinePOV`
- 它保存了哪些类型：0 个，-
- 字段依据示例：`AxisState` -> `m_Recentering`: `AxisState.Recentering`；`CinemachineFreeLook` -> `m_YAxisRecentering`: `AxisState.Recentering`；`m_RecenterToTargetHeading`: `AxisState.Recentering`；`CinemachineOrbitalTransposer` -> `m_RecenterToTargetHeading`: `AxisState.Recentering`；`CinemachinePOV` -> `m_VerticalRecentering`: `AxisState.Recentering`；`m_HorizontalRecentering`: `AxisState.Recentering`

#### Baker

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`AnimationClip`、`Animator`、`Baker.Mode`、`PlayableDirector`
- 字段依据示例：-

#### BakerHumanoidQT

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`HumanoidBaker`
- 它保存了哪些类型：4 个，`AnimationCurve`、`AvatarIKGoal`、`Quaternion`、`Transform`
- 字段依据示例：`HumanoidBaker` -> `rootQT`: `BakerHumanoidQT`；`leftFootQT`: `BakerHumanoidQT`；`rightFootQT`: `BakerHumanoidQT`

#### BakerTransform

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`GenericBaker`
- 它保存了哪些类型：4 个，`AnimationCurve`、`Quaternion`、`Transform`、`Vector3`
- 字段依据示例：`GenericBaker` -> `children`: `BakerTransform[]`；`rootChild`: `BakerTransform`

#### BipedLimbOrientations.LimbOrientation

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`BipedLimbOrientations`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`BipedLimbOrientations` -> `leftArm`: `BipedLimbOrientations.LimbOrientation`；`rightArm`: `BipedLimbOrientations.LimbOrientation`；`leftLeg`: `BipedLimbOrientations.LimbOrientation`

#### BipedReferences

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`BipedIK`、`FullBodyBipedIK`
- 它保存了哪些类型：1 个，`Transform`
- 字段依据示例：`BipedIK` -> `references`: `BipedReferences`；`FullBodyBipedIK` -> `references`: `BipedReferences`

#### BlendSourceVirtualCamera

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`CinemachineBrain.BrainFrame`
- 它保存了哪些类型：3 个，`CameraState`、`CinemachineBlend`、`Transform`
- 字段依据示例：`CinemachineBrain.BrainFrame` -> `workingBlendSource`: `BlendSourceVirtualCamera`

#### BlockManager

- 功能分析：管理器类：集中维护对应系统的运行时对象和流程
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`BlockManager.TraversalProvider`、`SingleNodeBlocker`、`TurnBasedAI`
- 它保存了哪些类型：2 个，`GraphNode`、`SingleNodeBlocker`
- 字段依据示例：`BlockManager.TraversalProvider` -> `blockManager`: `BlockManager`；`SingleNodeBlocker` -> `manager`: `BlockManager`；`TurnBasedAI` -> `blockManager`: `BlockManager`

#### BodyTilt

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`OffsetPose`、`Vector3`
- 字段依据示例：-

#### BoundingSphere

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`CinemachineTargetGroup`、`Light2D`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`CinemachineTargetGroup` -> `m_BoundingSphere`: `BoundingSphere`；`Light2D` -> `<boundingSphere>k__BackingField`: `BoundingSphere`

#### Bounds

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：16 个，`CinemachineFramingTransposer`、`CinemachineGroupComposer`、`CinemachineTargetGroup`、`DoorController`、`DynamicGridObstacle`、`GraphUpdateObject`、`Light2D`、`RasterizationMesh` 等 16 个
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`CinemachineFramingTransposer` -> `<LastBounds>k__BackingField`: `Bounds`；`CinemachineGroupComposer` -> `<LastBounds>k__BackingField`: `Bounds`；`CinemachineTargetGroup` -> `<BoundingBox>k__BackingField`: `Bounds`；`DoorController` -> `bounds`: `Bounds`；`DynamicGridObstacle` -> `prevBounds`: `Bounds`；另有 11 个来源

#### CameraCaptureBridge

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`Camera`、`CommandBuffer`、`HashSet`、`RenderTargetIdentifier`
- 字段依据示例：-

#### CameraData

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`RenderingData`
- 它保存了哪些类型：16 个，`AntialiasingMode`、`AntialiasingQuality`、`Camera`、`CameraRenderType`、`CameraType`、`CommandBuffer`、`LayerMask`、`Matrix4x4` 等 16 个
- 字段依据示例：`RenderingData` -> `cameraData`: `CameraData`

#### CameraProperties

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`CameraProperties`、`ScriptableCullingParameters`
- 它保存了哪些类型：8 个，`CameraProperties`、`CoreCameraValues`、`Matrix4x4`、`Rect`、`Vector3`、`layerCullDistances`、`m_CameraCullPlanes`、`m_ShadowCullPlanes`
- 字段依据示例：`CameraProperties` -> `m_ShadowCullPlanes`: `CameraProperties.<m_ShadowCullPlanes>e__FixedBuffer`；`m_CameraCullPlanes`: `CameraProperties.<m_CameraCullPlanes>e__FixedBuffer`；`layerCullDistances`: `CameraProperties.<layerCullDistances>e__FixedBuffer`；`ScriptableCullingParameters` -> `m_CameraProperties`: `CameraProperties`

#### CameraState

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：10 个，`BlendSourceVirtualCamera`、`CinemachineBlendListCamera`、`CinemachineBrain`、`CinemachineClearShot`、`CinemachineExternalCamera`、`CinemachineFreeLook`、`CinemachineMixingCamera`、`CinemachineStateDrivenCamera` 等 10 个
- 它保存了哪些类型：5 个，`CameraState.BlendHintValue`、`CameraState.CustomBlendable`、`LensSettings`、`Quaternion`、`Vector3`
- 字段依据示例：`BlendSourceVirtualCamera` -> `<State>k__BackingField`: `CameraState`；`CinemachineBlendListCamera` -> `m_State`: `CameraState`；`CinemachineBrain` -> `<CurrentCameraState>k__BackingField`: `CameraState`；`CinemachineClearShot` -> `m_State`: `CameraState`；`CinemachineExternalCamera` -> `m_State`: `CameraState`；另有 5 个来源

#### CameraSwitcher

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`Camera`、`DebugUI.EnumField`、`GUIContent`、`Quaternion`、`Vector3`
- 字段依据示例：-

#### CanvasScaler

- 功能分析：UI 控件类型：用于界面布局、文本、按钮、滚动、图形或交互控件
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`Canvas`、`CanvasScaler.ScaleMode`、`CanvasScaler.ScreenMatchMode`、`CanvasScaler.Unit`、`Vector2`
- 字段依据示例：-

#### CatmullRomDecoder

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`ControlPoint`、`Vector3`
- 字段依据示例：-

#### CFAnimator

- 功能分析：项目封装类型：穿越火线项目对 Unity 或 gameplay 逻辑的二次封装
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`Animator`、`Coroutine`、`SO_AnimationLerpData`
- 字段依据示例：-

#### ChangeMovingRealSize

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`Recoil`、`WeaponData_Gun`
- 它保存了哪些类型：0 个，-
- 字段依据示例：`Recoil` -> `changeMovingRealSize`: `ChangeMovingRealSize`；`WeaponData_Gun` -> `changeMovingRealSize`: `ChangeMovingRealSize`

#### CharacterEffect.FxData

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`CharacterEffect`、`TerminatorCharacterEffect`
- 它保存了哪些类型：3 个，`GameObject`、`Transform`、`Vector3`
- 字段依据示例：`CharacterEffect` -> `datas`: `CharacterEffect.FxData[]`；`TerminatorCharacterEffect` -> `oroData`: `CharacterEffect.FxData`

#### Cinemachine3rdPersonAim

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`LayerMask`、`RectTransform`
- 字段依据示例：-

#### Cinemachine3rdPersonFollow

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`LayerMask`、`Vector3`
- 字段依据示例：-

#### CinemachineBasicMultiChannelPerlin

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`NoiseSettings`、`Vector3`
- 字段依据示例：-

#### CinemachineBlend

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：7 个，`BlendSourceVirtualCamera`、`CinemachineBlendListCamera`、`CinemachineBrain`、`CinemachineBrain.BrainFrame`、`CinemachineClearShot`、`CinemachineFreeLook`、`CinemachineStateDrivenCamera`
- 它保存了哪些类型：2 个，`AnimationCurve`、`ICinemachineCamera`
- 字段依据示例：`BlendSourceVirtualCamera` -> `<Blend>k__BackingField`: `CinemachineBlend`；`CinemachineBlendListCamera` -> `mActiveBlend`: `CinemachineBlend`；`CinemachineBrain` -> `mCurrentLiveCameras`: `CinemachineBlend`；`CinemachineBrain.BrainFrame` -> `blend`: `CinemachineBlend`；`workingBlend`: `CinemachineBlend`；`CinemachineClearShot` -> `mActiveBlend`: `CinemachineBlend`；另有 2 个来源

#### CinemachineBlendDefinition

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：5 个，`CinemachineBlendListCamera.Instruction`、`CinemachineBlenderSettings.CustomBlend`、`CinemachineBrain`、`CinemachineClearShot`、`CinemachineStateDrivenCamera`
- 它保存了哪些类型：2 个，`AnimationCurve`、`CinemachineBlendDefinition.Style`
- 字段依据示例：`CinemachineBlenderSettings.CustomBlend` -> `m_Blend`: `CinemachineBlendDefinition`；`CinemachineBlendListCamera.Instruction` -> `m_Blend`: `CinemachineBlendDefinition`；`CinemachineBrain` -> `m_DefaultBlend`: `CinemachineBlendDefinition`；`CinemachineClearShot` -> `m_DefaultBlend`: `CinemachineBlendDefinition`；`CinemachineStateDrivenCamera` -> `m_DefaultBlend`: `CinemachineBlendDefinition`

#### CinemachineBlenderSettings

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`CinemachineBrain`、`CinemachineClearShot`、`CinemachineStateDrivenCamera`
- 它保存了哪些类型：1 个，`CinemachineBlenderSettings.CustomBlend`
- 字段依据示例：`CinemachineBrain` -> `m_CustomBlends`: `CinemachineBlenderSettings`；`CinemachineClearShot` -> `m_CustomBlends`: `CinemachineBlenderSettings`；`CinemachineStateDrivenCamera` -> `m_CustomBlends`: `CinemachineBlenderSettings`

#### CinemachineBlendListCamera

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：6 个，`CameraState`、`CinemachineBlend`、`CinemachineBlendListCamera.Instruction`、`CinemachineVirtualCameraBase`、`ICinemachineCamera`、`Transform`
- 字段依据示例：-

#### CinemachineBrain.BrainEvent

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`CinemachineBrain`、`CinemachineCore`
- 它保存了哪些类型：0 个，-
- 字段依据示例：`CinemachineBrain` -> `m_CameraCutEvent`: `CinemachineBrain.BrainEvent`；`CinemachineCore` -> `CameraUpdatedEvent`: `CinemachineBrain.BrainEvent`；`CameraCutEvent`: `CinemachineBrain.BrainEvent`

#### CinemachineBrain.BrainFrame

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`CinemachineBrain`
- 它保存了哪些类型：2 个，`BlendSourceVirtualCamera`、`CinemachineBlend`
- 字段依据示例：`CinemachineBrain` -> `mFrameStack`: `List<CinemachineBrain.BrainFrame>`

#### CinemachineBrain.BrainUpdateMethod

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 enum 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：0 个，-
- 字段依据示例：-

#### CinemachineBrain.UpdateMethod

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 enum 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：0 个，-
- 字段依据示例：-

#### CinemachineBrain.VcamActivatedEvent

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`CinemachineBrain`、`CinemachineVirtualCameraBase.TransitionParams`
- 它保存了哪些类型：0 个，-
- 字段依据示例：`CinemachineBrain` -> `m_CameraActivatedEvent`: `CinemachineBrain.VcamActivatedEvent`；`CinemachineVirtualCameraBase.TransitionParams` -> `m_OnCameraLive`: `CinemachineBrain.VcamActivatedEvent`

#### CinemachineCameraOffset

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`CinemachineCore.Stage`、`Vector3`
- 字段依据示例：-

#### CinemachineClearShot

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：7 个，`CameraState`、`CinemachineBlend`、`CinemachineBlendDefinition`、`CinemachineBlenderSettings`、`CinemachineVirtualCameraBase`、`ICinemachineCamera`、`Transform`
- 字段依据示例：-

#### CinemachineCollider

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：6 个，`CinemachineCollider.ResolutionStrategy`、`Collider`、`GameObject`、`LayerMask`、`RaycastHit`、`SphereCollider`
- 字段依据示例：-

#### CinemachineCollider.VcamExtraState

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：-

#### CinemachineCollisionImpulseSource

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`LayerMask`、`Rigidbody`、`Rigidbody2D`
- 字段依据示例：-

#### CinemachineComponentBase

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`CinemachineVirtualCamera`
- 它保存了哪些类型：3 个，`CinemachineVirtualCameraBase`、`ICinemachineTargetGroup`、`Transform`
- 字段依据示例：`CinemachineVirtualCamera` -> `m_ComponentPipeline`: `CinemachineComponentBase[]`

#### CinemachineComposer

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`CinemachineComposer.FovCache`、`PositionPredictor`、`Quaternion`、`Vector2`、`Vector3`
- 字段依据示例：-

#### CinemachineConfiner

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`CinemachineConfiner.Mode`、`Collider`、`Collider2D`、`Vector2`
- 字段依据示例：-

#### CinemachineConfiner.VcamExtraState

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：-

#### CinemachineCore

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`CinemachineCore`
- 它保存了哪些类型：6 个，`CinemachineBrain`、`CinemachineBrain.BrainEvent`、`CinemachineCore`、`CinemachineCore.UpdateFilter`、`CinemachineCore.UpdateStatus`、`CinemachineVirtualCameraBase`
- 字段依据示例：`CinemachineCore` -> `sInstance`: `CinemachineCore`

#### CinemachineExternalCamera

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`Camera`、`CameraState`、`CinemachineVirtualCameraBase.BlendHint`、`Transform`
- 字段依据示例：-

#### CinemachineFramingTransposer

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：7 个，`Bounds`、`CinemachineFramingTransposer.AdjustmentMode`、`CinemachineFramingTransposer.FramingMode`、`Matrix4x4`、`PositionPredictor`、`Quaternion`、`Vector3`
- 字段依据示例：-

#### CinemachineFreeLook.Orbit

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`CinemachineFreeLook`
- 它保存了哪些类型：0 个，-
- 字段依据示例：`CinemachineFreeLook` -> `m_Orbits`: `CinemachineFreeLook.Orbit[]`；`m_CachedOrbits`: `CinemachineFreeLook.Orbit[]`

#### CinemachineHardLockToTarget

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：-

#### CinemachineImpulseDefinition.SignalSource

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`CinemachineImpulseDefinition`、`Vector3`
- 字段依据示例：-

#### CinemachineImpulseManager.ImpulseEvent

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`CinemachineImpulseDefinition`、`CinemachineImpulseManager`、`CinemachineImpulseManager.ImpulseEvent`
- 它保存了哪些类型：6 个，`CinemachineImpulseManager.EnvelopeDefinition`、`CinemachineImpulseManager.ImpulseEvent`、`DirectionMode`、`DissipationMode`、`ISignalSource6D`、`Vector3`
- 字段依据示例：`CinemachineImpulseDefinition` -> `m_DirectionMode`: `CinemachineImpulseManager.ImpulseEvent.DirectionMode`；`m_DissipationMode`: `CinemachineImpulseManager.ImpulseEvent.DissipationMode`；`CinemachineImpulseManager` -> `m_ExpiredEvents`: `List<CinemachineImpulseManager.ImpulseEvent>`；`m_ActiveEvents`: `List<CinemachineImpulseManager.ImpulseEvent>`；`CinemachineImpulseManager.ImpulseEvent` -> `m_DirectionMode`: `CinemachineImpulseManager.ImpulseEvent.DirectionMode`；`m_DissipationMode`: `CinemachineImpulseManager.ImpulseEvent.DissipationMode`

#### CinemachineIndependentImpulseListener

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Quaternion`、`Vector3`
- 字段依据示例：-

#### CinemachineMixer

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`CinemachineBrain`
- 字段依据示例：-

#### CinemachineMixingCamera

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`CameraState`、`CinemachineVirtualCameraBase`、`ICinemachineCamera`、`Transform`
- 字段依据示例：-

#### CinemachineOrbitalTransposer

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`CinemachineFreeLook`
- 它保存了哪些类型：7 个，`AxisState`、`AxisState.Recentering`、`CinemachineOrbitalTransposer.Heading`、`HeadingTracker`、`Rigidbody`、`Transform`、`Vector3`
- 字段依据示例：`CinemachineFreeLook` -> `mOrbitals`: `CinemachineOrbitalTransposer[]`

#### CinemachineOrbitalTransposer.Heading

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`CinemachineFreeLook`、`CinemachineOrbitalTransposer`、`CinemachineOrbitalTransposer.Heading`
- 它保存了哪些类型：2 个，`CinemachineOrbitalTransposer.Heading`、`HeadingDefinition`
- 字段依据示例：`CinemachineFreeLook` -> `m_Heading`: `CinemachineOrbitalTransposer.Heading`；`CinemachineOrbitalTransposer` -> `m_Heading`: `CinemachineOrbitalTransposer.Heading`；`CinemachineOrbitalTransposer.Heading` -> `m_Definition`: `CinemachineOrbitalTransposer.Heading.HeadingDefinition`

#### CinemachinePath.Waypoint

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`CinemachinePath`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`CinemachinePath` -> `m_Waypoints`: `CinemachinePath.Waypoint[]`

#### CinemachinePathBase.Appearance

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`CinemachinePathBase`
- 它保存了哪些类型：1 个，`Color`
- 字段依据示例：`CinemachinePathBase` -> `m_Appearance`: `CinemachinePathBase.Appearance`

#### CinemachineSmoothPath.Waypoint

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`CinemachineSmoothPath`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`CinemachineSmoothPath` -> `m_Waypoints`: `CinemachineSmoothPath.Waypoint[]`；`m_ControlPoints1`: `CinemachineSmoothPath.Waypoint[]`；`m_ControlPoints2`: `CinemachineSmoothPath.Waypoint[]`

#### CinemachineStateDrivenCamera

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：13 个，`AnimationClip`、`Animator`、`AnimatorClipInfo`、`CameraState`、`CinemachineBlend`、`CinemachineBlendDefinition`、`CinemachineBlenderSettings`、`CinemachineStateDrivenCamera.HashPair` 等 13 个
- 字段依据示例：-

#### CinemachineStoryboard

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`CinemachineStoryboard.CanvasInfo`、`CinemachineStoryboard.FillStrategy`、`Texture`、`Vector2`、`Vector3`
- 字段依据示例：-

#### CinemachineStoryboard.CanvasInfo

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`CinemachineStoryboard`
- 它保存了哪些类型：4 个，`CinemachineBrain`、`GameObject`、`RawImage`、`RectTransform`
- 字段依据示例：`CinemachineStoryboard` -> `mCanvasInfo`: `List<CinemachineStoryboard.CanvasInfo>`

#### CinemachineTargetGroup

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`GroupWeightManipulator`
- 它保存了哪些类型：7 个，`BoundingSphere`、`Bounds`、`CinemachineTargetGroup.PositionMode`、`CinemachineTargetGroup.RotationMode`、`CinemachineTargetGroup.Target`、`CinemachineTargetGroup.UpdateMethod`、`Vector3`
- 字段依据示例：`GroupWeightManipulator` -> `m_group`: `CinemachineTargetGroup`

#### CinemachineTargetGroup.Target

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`CinemachineTargetGroup`
- 它保存了哪些类型：1 个，`Transform`
- 字段依据示例：`CinemachineTargetGroup` -> `m_Targets`: `CinemachineTargetGroup.Target[]`

#### CinemachineTrackedDolly

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：6 个，`CinemachinePathBase`、`CinemachinePathBase.PositionUnits`、`CinemachineTrackedDolly.AutoDolly`、`CinemachineTrackedDolly.CameraUpMode`、`Quaternion`、`Vector3`
- 字段依据示例：-

#### CinemachineTransposer

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`CinemachineTransposer.AngularDampingMode`、`CinemachineTransposer.BindingMode`、`Quaternion`、`Transform`、`Vector3`
- 字段依据示例：-

#### CinemachineTransposer.BindingMode

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 enum 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：0 个，-
- 字段依据示例：-

#### CinemachineTriggerAction

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`CinemachineTriggerAction.ActionSettings`、`GameObject`、`HashSet`、`LayerMask`
- 字段依据示例：-

#### CinemachineVirtualCameraBase

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：13 个，`CinemachineBlendListCamera`、`CinemachineBlendListCamera.Instruction`、`CinemachineClearShot`、`CinemachineComponentBase`、`CinemachineCore`、`CinemachineExtension`、`CinemachineMixingCamera`、`CinemachineShot` 等 13 个
- 它保存了哪些类型：4 个，`CinemachineCore.Stage`、`CinemachineExtension`、`CinemachineVirtualCameraBase`、`CinemachineVirtualCameraBase.StandbyUpdateMode`
- 字段依据示例：`CinemachineBlendListCamera` -> `m_ChildCameras`: `CinemachineVirtualCameraBase[]`；`CinemachineBlendListCamera.Instruction` -> `m_VirtualCamera`: `CinemachineVirtualCameraBase`；`CinemachineClearShot` -> `m_ChildCameras`: `CinemachineVirtualCameraBase[]`；`m_RandomizedChilden`: `CinemachineVirtualCameraBase[]`；`CinemachineComponentBase` -> `m_vcamOwner`: `CinemachineVirtualCameraBase`；`mCachedFollowTargetVcam`: `CinemachineVirtualCameraBase`；`mCachedLookAtTargetVcam`: `CinemachineVirtualCameraBase`；`CinemachineCore` -> `mActiveCameras`: `List<CinemachineVirtualCameraBase>`；`mAllCameras`: `List<List<CinemachineVirtualCameraBase>>`；`mRoundRobinVcamLastFrame`: `CinemachineVirtualCameraBase`；另有 8 个来源

#### CinemachineVirtualCameraBase.BlendHint

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 enum 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：0 个，-
- 字段依据示例：-

#### CinemachineVirtualCameraBase.TransitionParams

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`CinemachineFreeLook`、`CinemachineVirtualCamera`
- 它保存了哪些类型：2 个，`CinemachineBrain.VcamActivatedEvent`、`CinemachineVirtualCameraBase.BlendHint`
- 字段依据示例：`CinemachineFreeLook` -> `m_Transitions`: `CinemachineVirtualCameraBase.TransitionParams`；`CinemachineVirtualCamera` -> `m_Transitions`: `CinemachineVirtualCameraBase.TransitionParams`

#### CinemachineVolumeSettings

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`CinemachineVolumeSettings.FocusTrackingMode`、`Transform`、`Volume`、`VolumeProfile`
- 字段依据示例：-

#### CinemachineVolumeSettings.VcamExtraState

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`VolumeProfile`
- 字段依据示例：-

#### CircleOptions

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector2`
- 字段依据示例：-

#### ClipBuff

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`WeaponClass`
- 字段依据示例：-

#### Collider

- 功能分析：物理检测类型：用于碰撞、射线检测、触发器或命中查询
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：14 个，`BA_Nano_WatchOutTeammate`、`CinemachineCollider`、`CinemachineConfiner`、`Collision`、`ControllerColliderHit`、`DynamicGridObstacle`、`Helmet`、`HitReaction.HitPoint` 等 14 个
- 它保存了哪些类型：0 个，-
- 字段依据示例：`BA_Nano_WatchOutTeammate` -> `cldList`: `List<Collider>`；`CinemachineCollider` -> `mColliderBuffer`: `Collider[]`；`CinemachineConfiner` -> `m_BoundingVolume`: `Collider`；`Collision` -> `m_Collider`: `Collider`；`ControllerColliderHit` -> `m_Collider`: `Collider`；另有 9 个来源

#### Collision

- 功能分析：物理检测类型：用于碰撞、射线检测、触发器或命中查询
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`Collider`、`Component`、`ContactPoint`、`Vector3`
- 字段依据示例：-

#### Collision2D

- 功能分析：物理检测类型：用于碰撞、射线检测、触发器或命中查询
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`ContactPoint2D`、`Vector2`
- 字段依据示例：-

#### Color2

- 功能分析：颜色配置类型：用于 UI、特效、渲染或阵营表现的颜色数据
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Color`
- 字段依据示例：-

#### ColorBlock

- 功能分析：颜色配置类型：用于 UI、特效、渲染或阵营表现的颜色数据
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`ColorBlock`、`Selectable`
- 它保存了哪些类型：2 个，`Color`、`ColorBlock`
- 字段依据示例：`ColorBlock` -> `defaultColorBlock`: `ColorBlock`；`Selectable` -> `m_Colors`: `ColorBlock`

#### ColorGradingLutPass

- 功能分析：颜色配置类型：用于 UI、特效、渲染或阵营表现的颜色数据
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`ForwardRenderer`、`Renderer2D`
- 它保存了哪些类型：3 个，`GraphicsFormat`、`Material`、`RenderTargetHandle`
- 字段依据示例：`ForwardRenderer` -> `m_ColorGradingLutPass`: `ColorGradingLutPass`；`Renderer2D` -> `m_ColorGradingLutPass`: `ColorGradingLutPass`

#### ColorParameter

- 功能分析：颜色配置类型：用于 UI、特效、渲染或阵营表现的颜色数据
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：5 个，`Bloom`、`ColorAdjustments`、`SplitToning`、`ThermalVision`、`Vignette`
- 它保存了哪些类型：0 个，-
- 字段依据示例：`Bloom` -> `tint`: `ColorParameter`；`ColorAdjustments` -> `colorFilter`: `ColorParameter`；`SplitToning` -> `shadows`: `ColorParameter`；`highlights`: `ColorParameter`；`ThermalVision` -> `MainColor`: `ColorParameter`；`Vignette` -> `color`: `ColorParameter`

#### ColorTween

- 功能分析：颜色配置类型：用于 UI、特效、渲染或阵营表现的颜色数据
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Graphic`
- 它保存了哪些类型：3 个，`Color`、`ColorTween.ColorTweenCallback`、`ColorTween.ColorTweenMode`
- 字段依据示例：`Graphic` -> `m_ColorTweenRunner`: `TweenRunner<ColorTween>`

#### CommonHud_1.Type

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 enum 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：0 个，-
- 字段依据示例：-

#### ComponentDataBase

- 功能分析：配置/数据类型：保存运行参数、资源引用、显示数据或系统配置
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`ComponentData`
- 它保存了哪些类型：0 个，-
- 字段依据示例：`ComponentData` -> `list`: `List<ComponentDataBase>`

#### Connection

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`GridNodeBase`、`MeshNode`、`PointNode`
- 它保存了哪些类型：1 个，`GraphNode`
- 字段依据示例：`GridNodeBase` -> `connections`: `Connection[]`；`MeshNode` -> `connections`: `Connection[]`；`PointNode` -> `connections`: `Connection[]`

#### ConstantPath

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`GraphNode`、`PathEndingCondition`、`Vector3`
- 字段依据示例：-

#### Constraint

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Transform`
- 字段依据示例：-

#### ConstraintPosition

- 功能分析：空间数据类型：保存位置、方向、旋转、速度或坐标信息
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：-

#### ConstraintPositionOffset

- 功能分析：空间数据类型：保存位置、方向、旋转、速度或坐标信息
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：-

#### Constraints

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`BipedIKSolvers`
- 它保存了哪些类型：2 个，`Transform`、`Vector3`
- 字段依据示例：`BipedIKSolvers` -> `pelvis`: `Constraints`

#### ContactPoint

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Collision`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`Collision` -> `m_ReusedContacts`: `ContactPoint[]`；`m_LegacyContacts`: `ContactPoint[]`

#### ContactPoint2D

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Collision2D`
- 它保存了哪些类型：1 个，`Vector2`
- 字段依据示例：`Collision2D` -> `m_ReusedContacts`: `ContactPoint2D[]`；`m_LegacyContacts`: `ContactPoint2D[]`

#### ContentSizeFitter

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`ContentSizeFitter.FitMode`、`DrivenRectTransformTracker`、`RectTransform`
- 字段依据示例：-

#### ControllerColliderHit

- 功能分析：战斗结算类型：用于伤害、命中、击杀、爆头或战斗反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`CharacterController`、`Collider`、`Vector3`
- 字段依据示例：-

#### ControlPoint

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`CatmullRomDecoder`、`CubicBezierDecoder`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`CatmullRomDecoder` -> `_PartialControlPs`: `ControlPoint[]`；`CubicBezierDecoder` -> `_PartialControlPs`: `ControlPoint[]`

#### Cookie

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector2`
- 字段依据示例：-

#### CopyColorPass

- 功能分析：颜色配置类型：用于 UI、特效、渲染或阵营表现的颜色数据
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`ForwardRenderer`
- 它保存了哪些类型：4 个，`Downsampling`、`Material`、`RenderTargetHandle`、`RenderTargetIdentifier`
- 字段依据示例：`ForwardRenderer` -> `m_CopyColorPass`: `CopyColorPass`

#### CopyDepthPass

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`ForwardRenderer`
- 它保存了哪些类型：2 个，`Material`、`RenderTargetHandle`
- 字段依据示例：`ForwardRenderer` -> `m_GBufferCopyDepthPass`: `CopyDepthPass`；`m_CopyDepthPass`: `CopyDepthPass`；`m_XRCopyDepthPass`: `CopyDepthPass`

#### Core

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Color`
- 字段依据示例：-

#### CoreUtils

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：6 个，`Cubemap`、`CubemapArray`、`RenderTexture`、`Texture3D`、`Type`、`Vector3`
- 字段依据示例：-

#### CriticalDamageText

- 功能分析：战斗结算类型：用于伤害、命中、击杀、爆头或战斗反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Text`
- 字段依据示例：-

#### CubicBezierDecoder

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`ControlPoint`、`Vector3`
- 字段依据示例：-

#### CustomTexSheet

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`Gradient`、`Material`、`Texture2D`
- 字段依据示例：-

#### DataBaseExample.ChildTest

- 功能分析：配置/数据类型：保存运行参数、资源引用、显示数据或系统配置
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`DataBaseExample.ClassTest`
- 它保存了哪些类型：2 个，`Color`、`Gradient`
- 字段依据示例：`DataBaseExample.ClassTest` -> `childTest`: `DataBaseExample.ChildTest[]`

#### DebugManager

- 功能分析：管理器类：集中维护对应系统的运行时对象和流程
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`DebugManager`
- 它保存了哪些类型：9 个，`DebugActionDesc`、`DebugActionState`、`DebugManager`、`DebugUI.Panel`、`DebugUIHandlerCanvas`、`DebugUIHandlerPersistentCanvas`、`GameObject`、`Lazy` 等 9 个
- 字段依据示例：`DebugManager` -> `s_Instance`: `Lazy<DebugManager>`

#### DebugUIHandlerBitField

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`DebugUI.BitField`、`DebugUIHandlerContainer`、`DebugUIHandlerIndirectToggle`、`Text`、`UIFoldout`
- 字段依据示例：-

#### DebugUIHandlerButton

- 功能分析：UI 控件类型：用于界面布局、文本、按钮、滚动、图形或交互控件
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`DebugUI.Button`、`Text`
- 字段依据示例：-

#### DebugUIHandlerCanvas

- 功能分析：UI 控件类型：用于界面布局、文本、按钮、滚动、图形或交互控件
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`DebugManager`
- 它保存了哪些类型：5 个，`DebugUIHandlerPanel`、`DebugUIHandlerWidget`、`DebugUIPrefabBundle`、`Transform`、`Type`
- 字段依据示例：`DebugManager` -> `m_RootUICanvas`: `DebugUIHandlerCanvas`

#### DebugUIHandlerColor

- 功能分析：颜色配置类型：用于 UI、特效、渲染或阵营表现的颜色数据
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：6 个，`DebugUI.ColorField`、`DebugUIHandlerContainer`、`DebugUIHandlerIndirectFloatField`、`Image`、`Text`、`UIFoldout`
- 字段依据示例：-

#### DebugUIHandlerContainer

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：9 个，`DebugUIHandlerBitField`、`DebugUIHandlerColor`、`DebugUIHandlerFoldout`、`DebugUIHandlerGroup`、`DebugUIHandlerHBox`、`DebugUIHandlerVBox`、`DebugUIHandlerVector2`、`DebugUIHandlerVector3` 等 9 个
- 它保存了哪些类型：1 个，`RectTransform`
- 字段依据示例：`DebugUIHandlerBitField` -> `m_Container`: `DebugUIHandlerContainer`；`DebugUIHandlerColor` -> `m_Container`: `DebugUIHandlerContainer`；`DebugUIHandlerFoldout` -> `m_Container`: `DebugUIHandlerContainer`；`DebugUIHandlerGroup` -> `m_Container`: `DebugUIHandlerContainer`；`DebugUIHandlerHBox` -> `m_Container`: `DebugUIHandlerContainer`；另有 4 个来源

#### DebugUIHandlerEnumField

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`DebugUI.EnumField`、`Text`
- 字段依据示例：-

#### DebugUIHandlerEnumHistory

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Text`
- 字段依据示例：-

#### DebugUIHandlerFloatField

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`DebugUI.FloatField`、`Text`
- 字段依据示例：-

#### DebugUIHandlerFoldout

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`DebugUI.Foldout`、`DebugUIHandlerContainer`、`Text`、`UIFoldout`
- 字段依据示例：-

#### DebugUIHandlerGroup

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`DebugUI.Container`、`DebugUIHandlerContainer`、`Text`、`Transform`
- 字段依据示例：-

#### DebugUIHandlerIndirectFloatField

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：4 个，`DebugUIHandlerColor`、`DebugUIHandlerVector2`、`DebugUIHandlerVector3`、`DebugUIHandlerVector4`
- 它保存了哪些类型：1 个，`Text`
- 字段依据示例：`DebugUIHandlerColor` -> `fieldR`: `DebugUIHandlerIndirectFloatField`；`fieldG`: `DebugUIHandlerIndirectFloatField`；`fieldB`: `DebugUIHandlerIndirectFloatField`；`DebugUIHandlerVector2` -> `fieldX`: `DebugUIHandlerIndirectFloatField`；`fieldY`: `DebugUIHandlerIndirectFloatField`；`DebugUIHandlerVector3` -> `fieldX`: `DebugUIHandlerIndirectFloatField`；`fieldY`: `DebugUIHandlerIndirectFloatField`；`fieldZ`: `DebugUIHandlerIndirectFloatField`；`DebugUIHandlerVector4` -> `fieldX`: `DebugUIHandlerIndirectFloatField`；`fieldY`: `DebugUIHandlerIndirectFloatField`；`fieldZ`: `DebugUIHandlerIndirectFloatField`

#### DebugUIHandlerIndirectToggle

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`DebugUIHandlerBitField`
- 它保存了哪些类型：3 个，`Image`、`Text`、`Toggle`
- 字段依据示例：`DebugUIHandlerBitField` -> `toggles`: `List<DebugUIHandlerIndirectToggle>`

#### DebugUIHandlerIntField

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`DebugUI.IntField`、`Text`
- 字段依据示例：-

#### DebugUIHandlerPanel

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`DebugUIHandlerCanvas`
- 它保存了哪些类型：4 个，`DebugUI.Panel`、`RectTransform`、`ScrollRect`、`Text`
- 字段依据示例：`DebugUIHandlerCanvas` -> `m_UIPanels`: `List<DebugUIHandlerPanel>`

#### DebugUIHandlerPersistentCanvas

- 功能分析：UI 控件类型：用于界面布局、文本、按钮、滚动、图形或交互控件
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`DebugManager`
- 它保存了哪些类型：2 个，`DebugUIHandlerValue`、`RectTransform`
- 字段依据示例：`DebugManager` -> `m_RootUIPersistentCanvas`: `DebugUIHandlerPersistentCanvas`

#### DebugUIHandlerToggle

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`DebugUI.BoolField`、`Image`、`Text`、`Toggle`
- 字段依据示例：-

#### DebugUIHandlerUIntField

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`DebugUI.UIntField`、`Text`
- 字段依据示例：-

#### DebugUIHandlerValue

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`DebugUIHandlerPersistentCanvas`
- 它保存了哪些类型：2 个，`DebugUI.Value`、`Text`
- 字段依据示例：`DebugUIHandlerPersistentCanvas` -> `m_Items`: `List<DebugUIHandlerValue>`

#### DebugUIHandlerVector2

- 功能分析：空间数据类型：保存位置、方向、旋转、速度或坐标信息
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`DebugUI.Vector2Field`、`DebugUIHandlerContainer`、`DebugUIHandlerIndirectFloatField`、`Text`、`UIFoldout`
- 字段依据示例：-

#### DebugUIHandlerVector3

- 功能分析：空间数据类型：保存位置、方向、旋转、速度或坐标信息
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`DebugUI.Vector3Field`、`DebugUIHandlerContainer`、`DebugUIHandlerIndirectFloatField`、`Text`、`UIFoldout`
- 字段依据示例：-

#### DebugUIHandlerVector4

- 功能分析：空间数据类型：保存位置、方向、旋转、速度或坐标信息
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`DebugUI.Vector4Field`、`DebugUIHandlerContainer`、`DebugUIHandlerIndirectFloatField`、`Text`、`UIFoldout`
- 字段依据示例：-

#### DebugUIHandlerWidget

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`DebugUIHandlerCanvas`、`DebugUIHandlerWidget`
- 它保存了哪些类型：3 个，`Color`、`DebugUI.Widget`、`DebugUIHandlerWidget`
- 字段依据示例：`DebugUIHandlerCanvas` -> `m_SelectedWidget`: `DebugUIHandlerWidget`；`DebugUIHandlerWidget` -> `<parentUIHandler>k__BackingField`: `DebugUIHandlerWidget`；`<previousUIHandler>k__BackingField`: `DebugUIHandlerWidget`；`<nextUIHandler>k__BackingField`: `DebugUIHandlerWidget`

#### DebugUIPrefabBundle

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`DebugUIHandlerCanvas`
- 它保存了哪些类型：1 个，`RectTransform`
- 字段依据示例：`DebugUIHandlerCanvas` -> `prefabs`: `List<DebugUIPrefabBundle>`

#### DefaultControls

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`Color`、`DefaultControls.IFactoryControls`、`Vector2`
- 字段依据示例：-

#### DefaultControls.Resources

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Sprite`
- 字段依据示例：-

#### DeferredLights

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：4 个，`DeferredPass`、`ForwardRenderer`、`GBufferPass`、`TileDepthRangePass`
- 它保存了哪些类型：10 个，`AdditionalLightsShadowCasterPass`、`DeferredTiler`、`Material`、`Matrix4x4`、`Mesh`、`MixedLightingSetup`、`NativeArray`、`ProfilingSampler` 等 10 个
- 字段依据示例：`DeferredPass` -> `m_DeferredLights`: `DeferredLights`；`ForwardRenderer` -> `m_DeferredLights`: `DeferredLights`；`GBufferPass` -> `m_DeferredLights`: `DeferredLights`；`TileDepthRangePass` -> `m_DeferredLights`: `DeferredLights`

#### DelayOneShootData

- 功能分析：配置/数据类型：保存运行参数、资源引用、显示数据或系统配置
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`Recoil`、`WeaponData_Gun`
- 它保存了哪些类型：0 个，-
- 字段依据示例：`Recoil` -> `delayOneShootTime`: `DelayOneShootData`；`WeaponData_Gun` -> `delayOneShootTime`: `DelayOneShootData`

#### DemoGUIMessage

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Color`
- 字段依据示例：-

#### DirectionalLight

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`LightMode`、`LinearColor`、`Quaternion`、`Vector3`
- 字段依据示例：-

#### DiscLight

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`FalloffType`、`LightMode`、`LinearColor`、`Quaternion`、`Vector3`
- 字段依据示例：-

#### Dropdown

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`UI_GameRoom`、`UI_Option`、`VFXUIDropdownBinder`
- 它保存了哪些类型：10 个，`Dropdown.DropdownEvent`、`Dropdown.DropdownItem`、`Dropdown.OptionData`、`Dropdown.OptionDataList`、`FloatTween`、`GameObject`、`Image`、`RectTransform` 等 10 个
- 字段依据示例：`UI_GameRoom` -> `matchTypeDropdown`: `Dropdown`；`mapDropdown`: `Dropdown`；`winTypeDropdown`: `Dropdown`；`UI_Option` -> `dpd_Resolution`: `Dropdown`；`VFXUIDropdownBinder` -> `Target`: `Dropdown`

#### Dropdown.DropdownItem

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Dropdown`
- 它保存了哪些类型：4 个，`Image`、`RectTransform`、`Text`、`Toggle`
- 字段依据示例：`Dropdown` -> `m_Items`: `List<Dropdown.DropdownItem>`

#### Dropdown.OptionData

- 功能分析：配置/数据类型：保存运行参数、资源引用、显示数据或系统配置
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`Dropdown`、`Dropdown.OptionDataList`
- 它保存了哪些类型：1 个，`Sprite`
- 字段依据示例：`Dropdown` -> `s_NoOptionData`: `Dropdown.OptionData`；`Dropdown.OptionDataList` -> `m_Options`: `List<Dropdown.OptionData>`

#### DynamicGridObstacle

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`Bounds`、`Collider`、`Collider2D`、`Quaternion`、`Transform`
- 字段依据示例：-

#### DynamicResolutionHandler

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`DynamicResolutionHandler`
- 它保存了哪些类型：7 个，`DynamicResScalePolicyType`、`DynamicResUpscaleFilter`、`DynamicResolutionHandler`、`DynamicResolutionType`、`GlobalDynamicResolutionSettings`、`Vector2Int`、`WeakReference`
- 字段依据示例：`DynamicResolutionHandler` -> `s_CameraInstances`: `Dictionary<int, DynamicResolutionHandler>`；`s_DefaultInstance`: `DynamicResolutionHandler`；`s_ActiveInstance`: `DynamicResolutionHandler`

#### EffectAsset.EffectData

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`EffectAsset`
- 它保存了哪些类型：1 个，`GameObject`
- 字段依据示例：`EffectAsset` -> `asset`: `List<EffectAsset.EffectData>`

#### EffectManager

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`EffectAsset`、`GameObject`、`NameKeyPool`、`SimpleObjectPool`
- 字段依据示例：-

#### EffectTester

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Quaternion`、`Vector3`
- 字段依据示例：-

#### EuclideanEmbedding

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`AstarPath`
- 它保存了哪些类型：3 个，`GraphNode`、`HeuristicOptimizationMode`、`Transform`
- 字段依据示例：`AstarPath` -> `euclideanEmbedding`: `EuclideanEmbedding`

#### EventSystem

- 功能分析：事件数据类型：用于在系统之间传递状态变化、动画回调或玩法通知
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`BaseEventData`、`BaseInputModule`、`EventSystem`
- 它保存了哪些类型：6 个，`BaseEventData`、`BaseInputModule`、`Comparison`、`EventSystem`、`GameObject`、`RaycastResult`
- 字段依据示例：`BaseEventData` -> `m_EventSystem`: `EventSystem`；`BaseInputModule` -> `m_EventSystem`: `EventSystem`；`EventSystem` -> `m_EventSystems`: `List<EventSystem>`

#### ExecuteEvents

- 功能分析：事件数据类型：用于在系统之间传递状态变化、动画回调或玩法通知
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：21 个，`ExecuteEvents.EventFunction`、`IBeginDragHandler`、`ICancelHandler`、`IDeselectHandler`、`IDragHandler`、`IDropHandler`、`IEndDragHandler`、`IEventSystemHandler` 等 21 个
- 字段依据示例：-

#### FBBIKArmBending

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`FullBodyBipedIK`、`Quaternion`、`Vector3`
- 字段依据示例：-

#### FBBIKHeadEffector

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`FBBIKHeadEffector.BendBone`、`FullBodyBipedIK`、`Quaternion`、`Transform`、`Vector3`
- 字段依据示例：-

#### FBBIKHeadEffector.BendBone

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`FBBIKHeadEffector`
- 它保存了哪些类型：2 个，`Quaternion`、`Transform`
- 字段依据示例：`FBBIKHeadEffector` -> `bendBones`: `FBBIKHeadEffector.BendBone[]`

#### FBIKChain.ChildConstraint

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`FBIKChain`
- 它保存了哪些类型：1 个，`Transform`
- 字段依据示例：`FBIKChain` -> `childConstraints`: `FBIKChain.ChildConstraint[]`

#### FinalBlitPass

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`ForwardRenderer`、`Renderer2D`
- 它保存了哪些类型：2 个，`Material`、`RenderTargetHandle`
- 字段依据示例：`ForwardRenderer` -> `m_FinalBlitPass`: `FinalBlitPass`；`Renderer2D` -> `m_FinalBlitPass`: `FinalBlitPass`

#### Finger

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`FingerRig`
- 它保存了哪些类型：5 个，`Finger.DOF`、`IKSolverLimb`、`Quaternion`、`Transform`、`Vector3`
- 字段依据示例：`FingerRig` -> `fingers`: `Finger[]`

#### FKOffset

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Animator`、`FKOffset.Offset`
- 字段依据示例：-

#### FKOffset.Offset

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`FKOffset`
- 它保存了哪些类型：3 个，`HumanBodyBones`、`Transform`、`Vector3`
- 字段依据示例：`FKOffset` -> `offsets`: `FKOffset.Offset[]`

#### FloatParameter

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`ColorAdjustments`、`GhostBladeOneShine`、`ThermalVision`
- 它保存了哪些类型：0 个，-
- 字段依据示例：`ColorAdjustments` -> `postExposure`: `FloatParameter`；`GhostBladeOneShine` -> `RedDuration`: `FloatParameter`；`WhiteDuration`: `FloatParameter`；`PosterizePower`: `FloatParameter`；`ThermalVision` -> `Duration`: `FloatParameter`；`NoiseScale`: `FloatParameter`；`NoisePower`: `FloatParameter`

#### FloodPath

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`FloodPathConstraint`、`FloodPathTracer`
- 它保存了哪些类型：2 个，`GraphNode`、`Vector3`
- 字段依据示例：`FloodPathConstraint` -> `path`: `FloodPath`；`FloodPathTracer` -> `flood`: `FloodPath`

#### Font

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：6 个，`AstarDebugger`、`FontData`、`FontUpdateTracker`、`GUISkin`、`HUD_Nano_FinalBattle`、`TextGenerationSettings`
- 它保存了哪些类型：0 个，-
- 字段依据示例：`AstarDebugger` -> `font`: `Font`；`FontData` -> `m_Font`: `Font`；`FontUpdateTracker` -> `m_Tracked`: `Dictionary<Font, HashSet<Text>>`；`GUISkin` -> `m_Font`: `Font`；`HUD_Nano_FinalBattle` -> `normalFont`: `Font`；`flashFont`: `Font`；另有 1 个来源

#### FontData

- 功能分析：配置/数据类型：保存运行参数、资源引用、显示数据或系统配置
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Text`
- 它保存了哪些类型：5 个，`Font`、`FontStyle`、`HorizontalWrapMode`、`TextAnchor`、`VerticalWrapMode`
- 字段依据示例：`Text` -> `m_FontData`: `FontData`

#### FontUpdateTracker

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`Font`、`HashSet`、`Text`
- 字段依据示例：-

#### ForwardRenderer

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：24 个，`AdditionalLightsShadowCasterPass`、`CapturePass`、`ColorGradingLutPass`、`CopyColorPass`、`CopyDepthPass`、`DeferredLights`、`DeferredPass`、`DepthNormalOnlyPass` 等 24 个
- 字段依据示例：-

#### ForwardRendererData.ShaderResources

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`ForwardRendererData`
- 它保存了哪些类型：1 个，`Shader`
- 字段依据示例：`ForwardRendererData` -> `shaders`: `ForwardRendererData.ShaderResources`

#### Funnel.FunnelPortals

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：-

#### Funnel.PathPart

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：-

#### GameAsset

- 功能分析：资源索引类型：保存可加载资源、图标、预制体或表现素材引用
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`AssetManager`
- 它保存了哪些类型：2 个，`Texture2D`、`Vector2`
- 字段依据示例：`AssetManager` -> `asset`: `GameAsset`

#### GenericBaker

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`BakerTransform`、`Transform`
- 字段依据示例：-

#### GenericPoser.Map

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`GenericPoser`
- 它保存了哪些类型：3 个，`Quaternion`、`Transform`、`Vector3`
- 字段依据示例：`GenericPoser` -> `maps`: `GenericPoser.Map[]`

#### GhostBladeOneShinePass

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`OneShineRenderFeature`
- 它保存了哪些类型：3 个，`GhostBladeOneShine`、`Material`、`RenderTargetIdentifier`
- 字段依据示例：`OneShineRenderFeature` -> `oneShinePass`: `GhostBladeOneShinePass`

#### GradientColorKey

- 功能分析：输入交互类型：用于鼠标、触摸、按键或输入模块状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Color`
- 字段依据示例：-

#### GraphCollision

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`GridGraph`
- 它保存了哪些类型：5 个，`ColliderType`、`LayerMask`、`RayDirection`、`RaycastHit`、`Vector3`
- 字段依据示例：`GridGraph` -> `collision`: `GraphCollision`

#### GraphGizmoHelper

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：7 个，`Color`、`GraphDebugMode`、`PathHandler`、`RetainedGizmos`、`RetainedGizmos.Builder`、`RetainedGizmos.Hasher`、`Vector3`
- 字段依据示例：-

#### GraphHitInfo

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`GraphNode`、`Vector3`
- 字段依据示例：-

#### Graphic

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：8 个，`BaseMeshEffect`、`GraphicRaycaster`、`GraphicRegistry`、`InputField`、`Mask`、`Selectable`、`SoftMaskable`、`Toggle`
- 它保存了哪些类型：12 个，`Canvas`、`CanvasRenderer`、`Color`、`ColorTween`、`Material`、`Mesh`、`RectTransform`、`Texture2D` 等 12 个
- 字段依据示例：`BaseMeshEffect` -> `m_Graphic`: `Graphic`；`GraphicRaycaster` -> `m_RaycastResults`: `List<Graphic>`；`s_SortedGraphics`: `List<Graphic>`；`GraphicRegistry` -> `m_Graphics`: `Dictionary<Canvas, IndexedSet<Graphic>>`；`m_RaycastableGraphics`: `Dictionary<Canvas, IndexedSet<Graphic>>`；`s_EmptyList`: `List<Graphic>`；`InputField` -> `m_Placeholder`: `Graphic`；`Mask` -> `m_Graphic`: `Graphic`；另有 3 个来源

#### GraphMask

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`NNConstraint`、`Seeker`
- 它保存了哪些类型：0 个，-
- 字段依据示例：`NNConstraint` -> `graphMask`: `GraphMask`；`Seeker` -> `graphMask`: `GraphMask`

#### GraphSerializationContext

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`BinaryReader`、`BinaryWriter`、`GraphMeta`、`GraphNode`
- 字段依据示例：-

#### GraphTransform

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：4 个，`GraphTransform`、`GridGraph`、`NavmeshBase`、`Voxelize`
- 它保存了哪些类型：5 个，`GraphTransform`、`Int3`、`Matrix4x4`、`Quaternion`、`Vector3`
- 字段依据示例：`GraphTransform` -> `identityTransform`: `GraphTransform`；`GridGraph` -> `<transform>k__BackingField`: `GraphTransform`；`NavmeshBase` -> `transform`: `GraphTransform`；`Voxelize` -> `transform`: `GraphTransform`；`<transformVoxel2Graph>k__BackingField`: `GraphTransform`

#### GraphUpdateObject

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`GraphUpdateProcessor`、`GraphUpdateProcessor.GUOSingle`
- 它保存了哪些类型：5 个，`Bounds`、`GraphNode`、`GraphUpdateShape`、`Int3`、`NNConstraint`
- 字段依据示例：`GraphUpdateProcessor` -> `graphUpdateQueue`: `Queue<GraphUpdateObject>`；`GraphUpdateProcessor.GUOSingle` -> `obj`: `GraphUpdateObject`

#### GraphUpdateScene

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：-

#### GraphUpdateShape

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`GraphUpdateObject`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`GraphUpdateObject` -> `shape`: `GraphUpdateShape`

#### GridGraph

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`AstarData`、`GridNode`、`ProceduralGridMover`
- 它保存了哪些类型：8 个，`GraphCollision`、`GraphTransform`、`GridGraph.TextureData`、`GridNode`、`InspectorGridMode`、`NumNeighbours`、`Vector2`、`Vector3`
- 字段依据示例：`AstarData` -> `<gridGraph>k__BackingField`: `GridGraph`；`GridNode` -> `_gridGraphs`: `GridGraph[]`；`ProceduralGridMover` -> `graph`: `GridGraph`

#### GridGraph.TextureData

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`GridGraph`、`GridGraph.TextureData`
- 它保存了哪些类型：4 个，`ChannelUse`、`Color32`、`GridGraph.TextureData`、`Texture2D`
- 字段依据示例：`GridGraph` -> `textureData`: `GridGraph.TextureData`；`GridGraph.TextureData` -> `channels`: `GridGraph.TextureData.ChannelUse[]`

#### GridLayoutGroup

- 功能分析：UI 控件类型：用于界面布局、文本、按钮、滚动、图形或交互控件
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`GridLayoutGroup.Axis`、`GridLayoutGroup.Constraint`、`GridLayoutGroup.Corner`、`Vector2`
- 字段依据示例：-

#### GrounderBipedIK

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`BipedIK`、`Quaternion`、`Transform`、`Vector3`
- 字段依据示例：-

#### GrounderFBBIK

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`FullBodyBipedIK`、`GrounderFBBIK.SpineEffector`、`Transform`、`Vector3`
- 字段依据示例：-

#### GrounderIK

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`IK`、`Quaternion`、`Rigidbody`、`Transform`、`Vector3`
- 字段依据示例：-

#### GrounderQuadruped

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：7 个，`GrounderQuadruped.Foot`、`Grounding`、`IK`、`Quaternion`、`Rigidbody`、`Transform`、`Vector3`
- 字段依据示例：-

#### GrounderQuadruped.Foot

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`GrounderQuadruped`
- 它保存了哪些类型：4 个，`Grounding.Leg`、`IKSolver`、`Quaternion`、`Transform`
- 字段依据示例：`GrounderQuadruped` -> `feet`: `GrounderQuadruped.Foot[]`

#### GrounderVRIK

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Transform`、`VRIK`
- 字段依据示例：-

#### Grounding

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：4 个，`Grounder`、`GrounderQuadruped`、`Grounding.Leg`、`Grounding.Pelvis`
- 它保存了哪些类型：6 个，`Grounding.Leg`、`Grounding.Pelvis`、`Grounding.Quality`、`LayerMask`、`RaycastHit`、`Transform`
- 字段依据示例：`Grounder` -> `solver`: `Grounding`；`GrounderQuadruped` -> `forelegSolver`: `Grounding`；`Grounding.Leg` -> `grounding`: `Grounding`；`Grounding.Pelvis` -> `grounding`: `Grounding`

#### Grounding.Leg

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`GrounderQuadruped.Foot`、`Grounding`
- 它保存了哪些类型：5 个，`Grounding`、`Quaternion`、`RaycastHit`、`Transform`、`Vector3`
- 字段依据示例：`GrounderQuadruped.Foot` -> `leg`: `Grounding.Leg`；`Grounding` -> `<legs>k__BackingField`: `Grounding.Leg[]`

#### Grounding.Pelvis

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Grounding`
- 它保存了哪些类型：2 个，`Grounding`、`Vector3`
- 字段依据示例：`Grounding` -> `<pelvis>k__BackingField`: `Grounding.Pelvis`

#### GUIContent

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：6 个，`CameraSwitcher`、`DebugUI.BitField`、`DebugUI.EnumField`、`GUIContent`、`GUIWordWrapSizer`、`TextEditor`
- 它保存了哪些类型：2 个，`GUIContent`、`Texture`
- 字段依据示例：`CameraSwitcher` -> `m_CameraNames`: `GUIContent[]`；`DebugUI.BitField` -> `<enumNames>k__BackingField`: `GUIContent[]`；`DebugUI.EnumField` -> `enumNames`: `GUIContent[]`；`GUIContent` -> `s_Text`: `GUIContent`；`s_Image`: `GUIContent`；`s_TextImage`: `GUIContent`；`GUIWordWrapSizer` -> `m_Content`: `GUIContent`；另有 1 个来源

#### GUISettings

- 功能分析：配置/数据类型：保存运行参数、资源引用、显示数据或系统配置
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`GUISkin`
- 它保存了哪些类型：1 个，`Color`
- 字段依据示例：`GUISkin` -> `m_Settings`: `GUISettings`

#### HandPoser

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`Quaternion`、`Transform`、`Vector3`
- 字段依据示例：-

#### Hashtable

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：42 个，`AttributeCollection`、`ByteMatcher`、`CachedCodeEntry`、`ChannelData`、`CrossAppDomainSink`、`DateTimeFormatInfo`、`Encoding`、`EncodingTable` 等 42 个
- 它保存了哪些类型：3 个，`Hashtable.bucket`、`ICollection`、`IEqualityComparer`
- 字段依据示例：`AttributeCollection` -> `_defaultAttributes`: `Hashtable`；`ByteMatcher` -> `map`: `Hashtable`；`starts`: `Hashtable`；`CachedCodeEntry` -> `_caps`: `Hashtable`；`_capnames`: `Hashtable`；`ChannelData` -> `_customProperties`: `Hashtable`；`CrossAppDomainSink` -> `s_sinks`: `Hashtable`；另有 37 个来源

#### HeadingTracker

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`CinemachineOrbitalTransposer`
- 它保存了哪些类型：2 个，`HeadingTracker.Item`、`Vector3`
- 字段依据示例：`CinemachineOrbitalTransposer` -> `mHeadingTracker`: `HeadingTracker`

#### HeadingTracker.Item

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`HeadingTracker`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`HeadingTracker` -> `mHistory`: `HeadingTracker.Item[]`

#### Heuristic

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 enum 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：0 个，-
- 字段依据示例：-

#### HierarchicalGraph

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`AstarPath`
- 它保存了哪些类型：3 个，`GraphNode`、`Queue`、`Stack`
- 字段依据示例：`AstarPath` -> `hierarchicalGraph`: `HierarchicalGraph`

#### HitReaction.HitPoint

- 功能分析：战斗结算类型：用于伤害、命中、击杀、爆头或战斗反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Collider`、`Vector3`
- 字段依据示例：-

#### HitReaction.HitPointBone

- 功能分析：战斗结算类型：用于伤害、命中、击杀、爆头或战斗反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`HitReaction`、`HitReaction.HitPointBone`
- 它保存了哪些类型：4 个，`AnimationCurve`、`BoneLink`、`HitReaction.HitPointBone`、`Rigidbody`
- 字段依据示例：`HitReaction` -> `boneHitPoints`: `HitReaction.HitPointBone[]`；`HitReaction.HitPointBone` -> `boneLinks`: `HitReaction.HitPointBone.BoneLink[]`

#### HitReaction.HitPointBone.BoneLink

- 功能分析：战斗结算类型：用于伤害、命中、击杀、爆头或战斗反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Quaternion`、`Transform`
- 字段依据示例：-

#### HitReaction.HitPointEffector.EffectorLink

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`FullBodyBipedEffector`、`Vector3`
- 字段依据示例：-

#### HitReactionVRIK.Offset

- 功能分析：战斗结算类型：用于伤害、命中、击杀、爆头或战斗反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Collider`、`Vector3`
- 字段依据示例：-

#### HitReactionVRIK.PositionOffset.PositionOffsetLink

- 功能分析：战斗结算类型：用于伤害、命中、击杀、爆头或战斗反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`IKSolverVR.PositionOffset`、`Vector3`
- 字段依据示例：-

#### HitReactionVRIK.RotationOffset

- 功能分析：战斗结算类型：用于伤害、命中、击杀、爆头或战斗反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`HitReactionVRIK`、`HitReactionVRIK.RotationOffset`
- 它保存了哪些类型：3 个，`HitReactionVRIK.RotationOffset`、`Rigidbody`、`RotationOffsetLink`
- 字段依据示例：`HitReactionVRIK` -> `rotationOffsets`: `HitReactionVRIK.RotationOffset[]`；`HitReactionVRIK.RotationOffset` -> `offsetLinks`: `HitReactionVRIK.RotationOffset.RotationOffsetLink[]`

#### HUD_BagButton

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`HUD_Bag`
- 它保存了哪些类型：2 个，`Image`、`Sprite`
- 字段依据示例：`HUD_Bag` -> `buttons`: `HUD_BagButton[]`

#### HUD_ChatBox

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`HUD_ChatBox.MsgMaskRectData`、`InputField`、`Queue`、`RectTransform`、`Text`
- 字段依据示例：-

#### HUD_Cheat

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：7 个，`ChoiceBase`、`GameObject`、`HUD_CheatChoice`、`Radio`、`RectTransform`、`SimpleObjectPool`、`Texture`
- 字段依据示例：-

#### HUD_CheatChoice

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`HUD_Cheat`
- 它保存了哪些类型：3 个，`RawImage`、`RectTransform`、`Text`
- 字段依据示例：`HUD_Cheat` -> `curChoiceList`: `List<HUD_CheatChoice>`

#### HUD_CommonMsg

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：6 个，`CommonHud_1`、`GameObject`、`HUD_Gauge`、`Image`、`RectTransform`、`Text`
- 字段依据示例：-

#### HUD_Crosshair.Type

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 enum 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：0 个，-
- 字段依据示例：-

#### HUD_DamageArrow

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`Color`、`Image`、`RectTransform`、`Vector3`
- 字段依据示例：-

#### HUD_EscMenu

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`GameObject`
- 字段依据示例：-

#### HUD_GameResult

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Image`、`Sprite`
- 字段依据示例：-

#### HUD_Gauge

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`HUD_CommonMsg`、`HUD_GaugeSystem`
- 它保存了哪些类型：2 个，`RectTransform`、`Text`
- 字段依据示例：`HUD_CommonMsg` -> `settingGauge`: `HUD_Gauge`；`HUD_GaugeSystem` -> `gaugeDic`: `Dictionary<string, HUD_Gauge>`

#### HUD_Gauge_EvilFire

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`Color`、`GameObject`、`RawImage`
- 字段依据示例：-

#### HUD_KillMark

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：6 个，`AudioSource`、`CharacterVoice`、`CommonKillMark`、`KillMarkAsset`、`RawImage`、`RectTransform`
- 字段依据示例：-

#### HUD_KillMark.ShowType

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 enum 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：0 个，-
- 字段依据示例：-

#### HUD_KillMarkUnder

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`GameObject`、`Image`、`Sprite`
- 字段依据示例：-

#### HUD_KillMsg

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`Color`、`HUD_KillMsgIndividual`、`Material`、`Queue`、`Sprite`
- 字段依据示例：-

#### HUD_KillMsgIndividual

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`HUD_KillMsg`
- 它保存了哪些类型：3 个，`Image`、`RectTransform`、`Text`
- 字段依据示例：`HUD_KillMsg` -> `spareMsg`: `List<HUD_KillMsgIndividual>`；`busyMsg`: `List<HUD_KillMsgIndividual>`

#### HUD_ProjectionID

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`GameObject`、`HUD_KillerSign`、`NameKeyPool`、`RectTransform`
- 字段依据示例：-

#### HUD_ProjectionSign

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Mode_Nano6`
- 它保存了哪些类型：5 个，`Image`、`RectTransform`、`Text`、`Transform`、`Vector3`
- 字段依据示例：`Mode_Nano6` -> `oneshineSign`: `HUD_ProjectionSign`

#### HUD_Radar

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`GameObject`、`NameKeyPool`、`RectTransform`
- 字段依据示例：-

#### HUD_RadarIcon

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`Image`、`RectTransform`、`Transform`、`Vector3`
- 字段依据示例：-

#### HUD_RadarIcon_SupplyBox

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Sprite`、`SupplyBox.Type`
- 字段依据示例：-

#### HUD_ScreenFX

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`NameKeyPool`、`RawImage`
- 字段依据示例：-

#### HUD_SkillBtn

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`HUD_Role`、`Skill`
- 它保存了哪些类型：3 个，`Image`、`Skill`、`Sprite`
- 字段依据示例：`HUD_Role` -> `skillBtns`: `HUD_SkillBtn[]`；`Skill` -> `skillBtn`: `HUD_SkillBtn`

#### HUD_Spectate

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：9 个，`GameObject`、`HUD_Spectate.Data`、`HUD_SpectateMsg`、`RawImage`、`RectTransform`、`Sprite`、`Text`、`Vector2` 等 9 个
- 字段依据示例：-

#### HUD_SpectateMsg

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`HUD_Spectate`、`HUD_Spectate.Data`
- 它保存了哪些类型：5 个，`Color`、`Image`、`RawImage`、`RectTransform`、`Text`
- 字段依据示例：`HUD_Spectate` -> `spareMsg`: `List<HUD_SpectateMsg>`；`busyMsg`: `List<HUD_SpectateMsg>`；`HUD_Spectate.Data` -> `bindMsg`: `HUD_SpectateMsg`

#### HUD_SupplyBoxSign

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Sprite`、`SupplyBox.Type`
- 字段依据示例：-

#### HUD_TabScoreBoard_DM

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`GameObject`
- 字段依据示例：-

#### HUD_TabScoreBoard_TD

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`GameObject`、`Image`、`RankField`、`Sprite`
- 字段依据示例：-

#### HUD_TerminatorSign

- 功能分析：HUD 界面组件：显示玩家状态、提示、图标或模式信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Button`、`Text`
- 字段依据示例：-

#### HumanCatchFeature

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`HumanCatchPass`、`LayerMask`、`Material`、`RenderPassEvent`
- 字段依据示例：-

#### HumanCatchPass

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`HumanCatchFeature`
- 它保存了哪些类型：3 个，`FilteringSettings`、`Material`、`RenderStateBlock`
- 字段依据示例：`HumanCatchFeature` -> `humanCatchPass`: `HumanCatchPass`

#### HumanLimit

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`HumanBone`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`HumanBone` -> `limit`: `HumanLimit`

#### HumanoidBaker

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：6 个，`BakerHumanoidQT`、`BakerMuscle`、`HumanPose`、`HumanPoseHandler`、`Quaternion`、`Vector3`
- 字段依据示例：-

#### HumanPose

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`HumanoidBaker`
- 它保存了哪些类型：2 个，`Quaternion`、`Vector3`
- 字段依据示例：`HumanoidBaker` -> `pose`: `HumanPose`

#### ICinemachineCamera

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：未发现同名 class/struct/enum，可能是 Unity 类型或外部类型
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：0 个，-
- 字段依据示例：-

#### IKConstraintBend

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`FBIKChain`
- 它保存了哪些类型：3 个，`Quaternion`、`Transform`、`Vector3`
- 字段依据示例：`FBIKChain` -> `bendConstraint`: `IKConstraintBend`

#### IKEffector

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`IKSolverFullBody`、`InteractionEffector`
- 它保存了哪些类型：3 个，`Quaternion`、`Transform`、`Vector3`
- 字段依据示例：`IKSolverFullBody` -> `effectors`: `IKEffector[]`；`InteractionEffector` -> `effector`: `IKEffector`

#### IKExecutionOrder

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Animator`、`IK`
- 字段依据示例：-

#### IKMapping.BoneMap

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`IKMappingBone`、`IKMappingLimb`、`IKMappingSpine`
- 它保存了哪些类型：3 个，`Quaternion`、`Transform`、`Vector3`
- 字段依据示例：`IKMappingBone` -> `boneMap`: `IKMapping.BoneMap`；`IKMappingLimb` -> `boneMapParent`: `IKMapping.BoneMap`；`boneMap1`: `IKMapping.BoneMap`；`boneMap2`: `IKMapping.BoneMap`；`IKMappingSpine` -> `spine`: `IKMapping.BoneMap[]`；`leftUpperArm`: `IKMapping.BoneMap`；`rightUpperArm`: `IKMapping.BoneMap`

#### IKMappingBone

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`IKSolverFullBody`
- 它保存了哪些类型：2 个，`IKMapping.BoneMap`、`Transform`
- 字段依据示例：`IKSolverFullBody` -> `boneMappings`: `IKMappingBone[]`

#### IKMappingLimb

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`IKSolverFullBody`
- 它保存了哪些类型：2 个，`IKMapping.BoneMap`、`Transform`
- 字段依据示例：`IKSolverFullBody` -> `limbMappings`: `IKMappingLimb[]`

#### IKMappingSpine

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`IKSolverFullBody`
- 它保存了哪些类型：2 个，`IKMapping.BoneMap`、`Transform`
- 字段依据示例：`IKSolverFullBody` -> `spineMapping`: `IKMappingSpine`

#### IKSolver

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`BipedIKSolvers`、`GrounderQuadruped.Foot`
- 它保存了哪些类型：2 个，`Transform`、`Vector3`
- 字段依据示例：`BipedIKSolvers` -> `_ikSolvers`: `IKSolver[]`；`GrounderQuadruped.Foot` -> `solver`: `IKSolver`

#### IKSolver.Bone

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`IKSolverHeuristic`
- 它保存了哪些类型：2 个，`RotationLimit`、`Vector3`
- 字段依据示例：`IKSolverHeuristic` -> `bones`: `IKSolver.Bone[]`

#### IKSolver.Node

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`FBIKChain`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`FBIKChain` -> `nodes`: `IKSolver.Node[]`

#### IKSolver.Point

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`FBIKChain`、`IKSolverArm`、`IKSolverLeg`
- 它保存了哪些类型：3 个，`Quaternion`、`Transform`、`Vector3`
- 字段依据示例：`FBIKChain` -> `p`: `IKSolver.Point`；`IKSolverArm` -> `chest`: `IKSolver.Point`；`shoulder`: `IKSolver.Point`；`upperArm`: `IKSolver.Point`；`IKSolverLeg` -> `pelvis`: `IKSolver.Point`；`thigh`: `IKSolver.Point`；`calf`: `IKSolver.Point`

#### IKSolverAim

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`AimIK`、`BipedIKSolvers`
- 它保存了哪些类型：3 个，`RotationLimit`、`Transform`、`Vector3`
- 字段依据示例：`AimIK` -> `solver`: `IKSolverAim`；`BipedIKSolvers` -> `aim`: `IKSolverAim`

#### IKSolverArm

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`ArmIK`
- 它保存了哪些类型：4 个，`IKSolver.Point`、`IKSolverVR.Arm`、`Quaternion`、`Vector3`
- 字段依据示例：`ArmIK` -> `solver`: `IKSolverArm`

#### IKSolverFABRIK

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`BipedIKSolvers`、`FABRIK`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`BipedIKSolvers` -> `spine`: `IKSolverFABRIK`；`FABRIK` -> `solver`: `IKSolverFABRIK`

#### IKSolverFABRIKRoot

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`FABRIKRoot`
- 它保存了哪些类型：2 个，`FABRIKChain`、`Vector3`
- 字段依据示例：`FABRIKRoot` -> `solver`: `IKSolverFABRIKRoot`

#### IKSolverFullBodyBiped

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`FullBodyBipedIK`
- 它保存了哪些类型：2 个，`Transform`、`Vector3`
- 字段依据示例：`FullBodyBipedIK` -> `solver`: `IKSolverFullBodyBiped`

#### IKSolverHeuristic

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`IKSolver.Bone`、`Transform`、`Vector3`
- 字段依据示例：-

#### IKSolverLeg

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`LegIK`
- 它保存了哪些类型：4 个，`IKSolver.Point`、`IKSolverVR.Leg`、`Quaternion`、`Vector3`
- 字段依据示例：`LegIK` -> `solver`: `IKSolverLeg`

#### IKSolverLimb

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`BipedIKSolvers`、`Finger`、`LimbIK`
- 它保存了哪些类型：6 个，`AvatarIKGoal`、`IKSolverLimb.AxisDirection`、`IKSolverLimb.BendModifier`、`Quaternion`、`Transform`、`Vector3`
- 字段依据示例：`BipedIKSolvers` -> `leftFoot`: `IKSolverLimb`；`rightFoot`: `IKSolverLimb`；`leftHand`: `IKSolverLimb`；`Finger` -> `solver`: `IKSolverLimb`；`LimbIK` -> `solver`: `IKSolverLimb`

#### IKSolverLimb.AxisDirection

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`IKSolverLimb`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`IKSolverLimb` -> `axisDirectionsLeft`: `IKSolverLimb.AxisDirection[]`；`axisDirectionsRight`: `IKSolverLimb.AxisDirection[]`

#### IKSolverLookAt

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`BipedIKSolvers`、`LookAtIK`
- 它保存了哪些类型：4 个，`AnimationCurve`、`IKSolverLookAt.LookAtBone`、`Transform`、`Vector3`
- 字段依据示例：`BipedIKSolvers` -> `lookAt`: `IKSolverLookAt`；`LookAtIK` -> `solver`: `IKSolverLookAt`

#### IKSolverLookAt.LookAtBone

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`IKSolverLookAt`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`IKSolverLookAt` -> `spine`: `IKSolverLookAt.LookAtBone[]`；`head`: `IKSolverLookAt.LookAtBone`；`eyes`: `IKSolverLookAt.LookAtBone[]`

#### IKSolverTrigonometric

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`TrigonometricIK`
- 它保存了哪些类型：4 个，`IKSolverTrigonometric.TrigonometricBone`、`Quaternion`、`Transform`、`Vector3`
- 字段依据示例：`TrigonometricIK` -> `solver`: `IKSolverTrigonometric`

#### IKSolverTrigonometric.TrigonometricBone

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`IKSolverTrigonometric`
- 它保存了哪些类型：2 个，`Quaternion`、`Vector3`
- 字段依据示例：`IKSolverTrigonometric` -> `bone1`: `IKSolverTrigonometric.TrigonometricBone`；`bone2`: `IKSolverTrigonometric.TrigonometricBone`；`bone3`: `IKSolverTrigonometric.TrigonometricBone`

#### IKSolverVR

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`VRIK`
- 它保存了哪些类型：8 个，`IKSolverVR.Arm`、`IKSolverVR.Leg`、`IKSolverVR.Locomotion`、`IKSolverVR.Spine`、`IKSolverVR.VirtualBone`、`Quaternion`、`Transform`、`Vector3`
- 字段依据示例：`VRIK` -> `solver`: `IKSolverVR`

#### IKSolverVR.Arm

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`IKSolverArm`、`IKSolverVR`、`IKSolverVR.Arm`
- 它保存了哪些类型：6 个，`AnimationCurve`、`IKSolverVR.Arm`、`Quaternion`、`ShoulderRotationMode`、`Transform`、`Vector3`
- 字段依据示例：`IKSolverArm` -> `arm`: `IKSolverVR.Arm`；`IKSolverVR` -> `leftArm`: `IKSolverVR.Arm`；`rightArm`: `IKSolverVR.Arm`；`arms`: `IKSolverVR.Arm[]`；`IKSolverVR.Arm` -> `shoulderRotationMode`: `IKSolverVR.Arm.ShoulderRotationMode`

#### IKSolverVR.BodyPart

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`IKSolverVR.VirtualBone`、`Quaternion`、`Vector3`
- 字段依据示例：-

#### IKSolverVR.Footstep

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`IKSolverVR.Locomotion`
- 它保存了哪些类型：2 个，`Quaternion`、`Vector3`
- 字段依据示例：`IKSolverVR.Locomotion` -> `footsteps`: `IKSolverVR.Footstep[]`

#### IKSolverVR.Leg

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`IKSolverLeg`、`IKSolverVR`
- 它保存了哪些类型：4 个，`AnimationCurve`、`Quaternion`、`Transform`、`Vector3`
- 字段依据示例：`IKSolverLeg` -> `leg`: `IKSolverVR.Leg`；`IKSolverVR` -> `leftLeg`: `IKSolverVR.Leg`；`rightLeg`: `IKSolverVR.Leg`；`legs`: `IKSolverVR.Leg[]`

#### IKSolverVR.Locomotion

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`IKSolverVR`
- 它保存了哪些类型：6 个，`AnimationCurve`、`IKSolverVR.Footstep`、`InterpolationMode`、`LayerMask`、`UnityEvent`、`Vector3`
- 字段依据示例：`IKSolverVR` -> `locomotion`: `IKSolverVR.Locomotion`

#### IKSolverVR.Spine

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`IKSolverVR`
- 它保存了哪些类型：3 个，`Quaternion`、`Transform`、`Vector3`
- 字段依据示例：`IKSolverVR` -> `spine`: `IKSolverVR.Spine`

#### IKSolverVR.VirtualBone

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`IKSolverVR`、`IKSolverVR.BodyPart`
- 它保存了哪些类型：2 个，`Quaternion`、`Vector3`
- 字段依据示例：`IKSolverVR` -> `<rootBone>k__BackingField`: `IKSolverVR.VirtualBone`；`IKSolverVR.BodyPart` -> `bones`: `IKSolverVR.VirtualBone[]`

#### Image.FillMethod

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 enum 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：0 个，-
- 字段依据示例：-

#### Image.Type

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 enum 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：0 个，-
- 字段依据示例：-

#### Inertia.Body

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`Inertia`、`Inertia.Body`
- 它保存了哪些类型：4 个，`EffectorLink`、`Inertia.Body`、`Transform`、`Vector3`
- 字段依据示例：`Inertia` -> `bodies`: `Inertia.Body[]`；`Inertia.Body` -> `effectorLinks`: `Inertia.Body.EffectorLink[]`

#### InputField

- 功能分析：输入交互类型：用于鼠标、触摸、按键或输入模块状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`HUD_ChatBox`、`UI_Temploray`
- 它保存了哪些类型：19 个，`CanvasRenderer`、`Color`、`Coroutine`、`Event`、`Graphic`、`InputField.CharacterValidation`、`InputField.ContentType`、`InputField.InputType` 等 19 个
- 字段依据示例：`HUD_ChatBox` -> `inputField`: `InputField`；`UI_Temploray` -> `registerCodeInput`: `InputField`；`password`: `InputField`

#### Int3

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：10 个，`ABPath`、`GraphNode`、`GraphTransform`、`GraphUpdateObject`、`NavmeshTile`、`Path`、`Polygon`、`TileHandler.CuttingResult` 等 10 个
- 它保存了哪些类型：0 个，-
- 字段依据示例：`ABPath` -> `startIntPoint`: `Int3`；`GraphNode` -> `position`: `Int3`；`GraphTransform` -> `i3translation`: `Int3`；`GraphUpdateObject` -> `backupPositionData`: `List<Int3>`；`NavmeshTile` -> `verts`: `Int3[]`；`vertsInGraphSpace`: `Int3[]`；另有 5 个来源

#### InteractionEffector

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`InteractionSystem`
- 它保存了哪些类型：9 个，`FullBodyBipedEffector`、`IKEffector`、`InteractionObject`、`InteractionSystem`、`InteractionTarget`、`Poser`、`Quaternion`、`Transform` 等 9 个
- 字段依据示例：`InteractionSystem` -> `interactionEffectors`: `InteractionEffector[]`

#### InteractionLookAt

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`InteractionSystem`
- 它保存了哪些类型：2 个，`LookAtIK`、`Transform`
- 字段依据示例：`InteractionSystem` -> `lookAt`: `InteractionLookAt`

#### InteractionObject

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`InteractionEffector`、`InteractionTrigger.Range.Interaction`
- 它保存了哪些类型：6 个，`InteractionObject.InteractionEvent`、`InteractionObject.Multiplier`、`InteractionObject.WeightCurve`、`InteractionSystem`、`InteractionTarget`、`Transform`
- 字段依据示例：`InteractionEffector` -> `<interactionObject>k__BackingField`: `InteractionObject`；`InteractionTrigger.Range.Interaction` -> `interactionObject`: `InteractionObject`

#### InteractionObject.AnimatorEvent

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`InteractionObject.InteractionEvent`
- 它保存了哪些类型：2 个，`Animation`、`Animator`
- 字段依据示例：`InteractionObject.InteractionEvent` -> `animations`: `InteractionObject.AnimatorEvent[]`

#### InteractionObject.Message

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`InteractionObject.InteractionEvent`
- 它保存了哪些类型：1 个，`GameObject`
- 字段依据示例：`InteractionObject.InteractionEvent` -> `messages`: `InteractionObject.Message[]`

#### InteractionSystem

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`InteractionEffector`、`InteractionObject`
- 它保存了哪些类型：8 个，`Collider`、`FullBodyBipedIK`、`InteractionEffector`、`InteractionLookAt`、`InteractionTrigger`、`LayerMask`、`RaycastHit`、`Transform`
- 字段依据示例：`InteractionEffector` -> `interactionSystem`: `InteractionSystem`；`InteractionObject` -> `<lastUsedInteractionSystem>k__BackingField`: `InteractionSystem`

#### InteractionTarget

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`InteractionEffector`、`InteractionObject`
- 它保存了哪些类型：5 个，`FullBodyBipedEffector`、`InteractionTarget.Multiplier`、`Quaternion`、`Transform`、`Vector3`
- 字段依据示例：`InteractionEffector` -> `interactionTarget`: `InteractionTarget`；`InteractionObject` -> `targets`: `InteractionTarget[]`

#### InteractionTrigger.CameraPosition

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`InteractionTrigger.Range`
- 它保存了哪些类型：2 个，`Collider`、`Vector3`
- 字段依据示例：`InteractionTrigger.Range` -> `cameraPosition`: `InteractionTrigger.CameraPosition`

#### InteractionTrigger.CharacterPosition

- 功能分析：空间数据类型：保存位置、方向、旋转、速度或坐标信息
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`InteractionTrigger.Range`
- 它保存了哪些类型：1 个，`Vector2`
- 字段依据示例：`InteractionTrigger.Range` -> `characterPosition`: `InteractionTrigger.CharacterPosition`

#### IPathModifier

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：未发现同名 class/struct/enum，可能是 Unity 类型或外部类型
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：0 个，-
- 字段依据示例：-

#### ITraversalProvider

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：未发现同名 class/struct/enum，可能是 Unity 类型或外部类型
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：0 个，-
- 字段依据示例：-

#### KillMarkAsset

- 功能分析：战斗结算类型：用于伤害、命中、击杀、爆头或战斗反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`HUD_KillMark`
- 它保存了哪些类型：1 个，`Texture`
- 字段依据示例：`HUD_KillMark` -> `asset`: `KillMarkAsset`

#### KnifeAttackData

- 功能分析：配置/数据类型：保存运行参数、资源引用、显示数据或系统配置
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`WeaponData_Gun`、`WeaponData_Knife`
- 它保存了哪些类型：1 个，`GameObject`
- 字段依据示例：`WeaponData_Gun` -> `knifeAttacks`: `KnifeAttackData[]`；`WeaponData_Knife` -> `knifeAttacks`: `KnifeAttackData[]`

#### LayerGridGraph.HeightSample

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`LayerGridGraph`
- 它保存了哪些类型：2 个，`RaycastHit`、`Vector3`
- 字段依据示例：`LayerGridGraph` -> `heightSampleBuffer`: `LayerGridGraph.HeightSample[]`

#### LayerMask

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：27 个，`AIBase`、`CameraData`、`Cinemachine3rdPersonAim`、`Cinemachine3rdPersonFollow`、`CinemachineCollider`、`CinemachineCollisionImpulseSource`、`CinemachineTriggerAction`、`ContactFilter2D` 等 27 个
- 它保存了哪些类型：0 个，-
- 字段依据示例：`AIBase` -> `groundMask`: `LayerMask`；`CameraData` -> `volumeLayerMask`: `LayerMask`；`Cinemachine3rdPersonAim` -> `AimCollisionFilter`: `LayerMask`；`Cinemachine3rdPersonFollow` -> `CameraCollisionFilter`: `LayerMask`；`CinemachineCollider` -> `m_CollideAgainst`: `LayerMask`；`m_TransparentLayers`: `LayerMask`；另有 22 个来源

#### LayoutGroup

- 功能分析：UI 控件类型：用于界面布局、文本、按钮、滚动、图形或交互控件
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`DrivenRectTransformTracker`、`RectOffset`、`RectTransform`、`TextAnchor`、`Vector2`
- 字段依据示例：-

#### LayoutRebuilder

- 功能分析：UI 控件类型：用于界面布局、文本、按钮、滚动、图形或交互控件
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`LayoutRebuilder`
- 它保存了哪些类型：3 个，`LayoutRebuilder`、`ObjectPool`、`RectTransform`
- 字段依据示例：`LayoutRebuilder` -> `s_Rebuilders`: `ObjectPool<LayoutRebuilder>`

#### LegacyAIPath

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：-

#### LegacyRichAI

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：-

#### LensSettings

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：4 个，`CameraState`、`CinemachineFreeLook`、`CinemachineVirtualCamera`、`LensSettings`
- 它保存了哪些类型：2 个，`LensSettings`、`Vector2`
- 字段依据示例：`CameraState` -> `<Lens>k__BackingField`: `LensSettings`；`CinemachineFreeLook` -> `m_Lens`: `LensSettings`；`CinemachineVirtualCamera` -> `m_Lens`: `LensSettings`；`LensSettings` -> `Default`: `LensSettings`

#### Light2D

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`Light2DCullResult`、`Light2DManager`
- 它保存了哪些类型：9 个，`BoundingSphere`、`Bounds`、`Color`、`Light2D.LightType`、`Light2D.PointLightQuality`、`Mesh`、`Sprite`、`Vector2` 等 9 个
- 字段依据示例：`Light2DCullResult` -> `m_VisibleLights`: `List<Light2D>`；`Light2DManager` -> `<lights>k__BackingField`: `List<Light2D>`

#### Light2DLookupTexture

- 功能分析：UI 控件类型：用于界面布局、文本、按钮、滚动、图形或交互控件
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Texture2D`
- 字段依据示例：-

#### LightDataGI

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：6 个，`FalloffType`、`LightMode`、`LightType`、`LinearColor`、`Quaternion`、`Vector3`
- 字段依据示例：-

#### LightUtility.ParametricLightMeshVertex

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`Color`、`VertexAttributeDescriptor`、`float3`
- 字段依据示例：-

#### LightUtility.SpriteLightMeshVertex

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`Color`、`Vector2`、`Vector3`、`VertexAttributeDescriptor`
- 字段依据示例：-

#### Line

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector2`
- 字段依据示例：-

#### LODParameters

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`BatchCullingContext`、`ScriptableCullingParameters`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`BatchCullingContext` -> `lodParameters`: `LODParameters`；`ScriptableCullingParameters` -> `m_LODParameters`: `LODParameters`

#### LookAtController

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`LookAtIK`、`Transform`、`Vector3`
- 字段依据示例：-

#### LoopRotate

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：-

#### MapEffectShooter

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`ParticleSystem`、`Vector3`
- 字段依据示例：-

#### Mask

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`Graphic`、`Material`、`RectTransform`
- 字段依据示例：-

#### MaskableGraphic

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`RectMask2D`
- 它保存了哪些类型：4 个，`MaskableGraphic.CullStateChangedEvent`、`Material`、`RectMask2D`、`Vector3`
- 字段依据示例：`RectMask2D` -> `m_MaskableTargets`: `HashSet<MaskableGraphic>`

#### MasterHeroSkillFX

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`RawImage`、`RectTransform`、`Vector2`
- 字段依据示例：-

#### MaterialEntry

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`MaterialCache`
- 它保存了哪些类型：1 个，`Material`
- 字段依据示例：`MaterialCache` -> `s_MaterialMap`: `Dictionary<Hash128, MaterialEntry>`

#### MecanimBridge

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`Animator`、`IAstarAI`、`Transform`、`Vector3`
- 字段依据示例：-

#### MeshSubsetCombineUtility.MeshContainer

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`GameObject`、`MeshSubsetCombineUtility.MeshInstance`、`MeshSubsetCombineUtility.SubMeshInstance`
- 字段依据示例：-

#### MissileData

- 功能分析：武器相关类型：用于武器数据、发射逻辑、弹药、投掷物或特殊武器表现
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：4 个，`WD_EvilTerminator`、`WD_GrenadeGun`、`WD_Missile`、`WD_RPG`
- 它保存了哪些类型：1 个，`GameObject`
- 字段依据示例：`WD_EvilTerminator` -> `missileData`: `MissileData`；`WD_GrenadeGun` -> `missileData`: `MissileData`；`WD_Missile` -> `missileData`: `MissileData`；`WD_RPG` -> `missileData`: `MissileData`

#### Mode_DeathMatch

- 功能分析：具体玩法模式类：实现某种模式的规则和流程
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`GameObject`
- 字段依据示例：-

#### Model.Socket

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Model`
- 它保存了哪些类型：2 个，`Transform`、`Vector3`
- 字段依据示例：`Model` -> `sockets`: `List<Model.Socket>`

#### MonoModifier

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Seeker`
- 字段依据示例：-

#### Msl_EvilFire

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`SphereCollider`、`Transform`
- 字段依据示例：-

#### MultiTargetPath

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`GraphNode`、`MultiTargetPath.HeuristicMode`、`Vector3`
- 字段依据示例：-

#### Navigator

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`NavMeshPath`、`Navigator.State`、`Transform`、`Vector3`
- 字段依据示例：-

#### NavmeshAdd

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：7 个，`Color`、`Mesh`、`NavmeshAdd.MeshType`、`Quaternion`、`Transform`、`Vector2`、`Vector3`
- 字段依据示例：-

#### NavmeshBase

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：4 个，`NavmeshTile`、`NavmeshUpdates.NavmeshUpdateSettings`、`RichFunnel`、`TileHandler`
- 它保存了哪些类型：6 个，`GraphTransform`、`MeshNode`、`NNConstraint`、`NavmeshTile`、`NavmeshUpdates.NavmeshUpdateSettings`、`Vector3`
- 字段依据示例：`NavmeshTile` -> `graph`: `NavmeshBase`；`NavmeshUpdates.NavmeshUpdateSettings` -> `graph`: `NavmeshBase`；`RichFunnel` -> `graph`: `NavmeshBase`；`TileHandler` -> `graph`: `NavmeshBase`

#### NavmeshCut

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：8 个，`Color`、`Int2`、`Mesh`、`NavmeshCut.MeshType`、`Quaternion`、`Transform`、`Vector2`、`Vector3`
- 字段依据示例：-

#### NavMeshGraph

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`AstarData`
- 它保存了哪些类型：2 个，`Mesh`、`Vector3`
- 字段依据示例：`AstarData` -> `<navmesh>k__BackingField`: `NavMeshGraph`

#### NavMeshHit

- 功能分析：战斗结算类型：用于伤害、命中、击杀、爆头或战斗反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：-

#### NavMeshPath

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Navigator`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`Navigator` -> `path`: `NavMeshPath`

#### NestedExample

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`Color`、`GameObject`、`Nested2Dict`
- 字段依据示例：-

#### NNConstraint

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：6 个，`ABPath`、`AIPath`、`AstarPath`、`GraphUpdateObject`、`NavmeshBase`、`Path`
- 它保存了哪些类型：1 个，`GraphMask`
- 字段依据示例：`ABPath` -> `NNConstraintNone`: `NNConstraint`；`AIPath` -> `cachedNNConstraint`: `NNConstraint`；`AstarPath` -> `NNConstraintNone`: `NNConstraint`；`GraphUpdateObject` -> `nnConstraint`: `NNConstraint`；`NavmeshBase` -> `NNConstraintDistanceXZ`: `NNConstraint`；`NNConstraintNone`: `NNConstraint`；另有 1 个来源

#### NNInfo

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`GraphNode`、`Vector3`
- 字段依据示例：-

#### NNInfoInternal

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`GraphNode`、`Vector3`
- 字段依据示例：-

#### NodeLink

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Transform`
- 字段依据示例：-

#### NodeLink2

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`NodeLink2`、`RichSpecial`
- 它保存了哪些类型：6 个，`Color`、`GraphNode`、`NodeLink2`、`PointNode`、`Transform`、`Vector3`
- 字段依据示例：`NodeLink2` -> `reference`: `Dictionary<GraphNode, NodeLink2>`；`RichSpecial` -> `nodeLink`: `NodeLink2`

#### NodeLink3

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`NodeLink3`、`NodeLink3Node`
- 它保存了哪些类型：7 个，`Color`、`GraphNode`、`MeshNode`、`NodeLink3`、`NodeLink3Node`、`Transform`、`Vector3`
- 字段依据示例：`NodeLink3` -> `reference`: `Dictionary<GraphNode, NodeLink3>`；`NodeLink3Node` -> `link`: `NodeLink3`

#### NodeLink3Node

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`NodeLink3`
- 它保存了哪些类型：2 个，`NodeLink3`、`Vector3`
- 字段依据示例：`NodeLink3` -> `startNode`: `NodeLink3Node`；`endNode`: `NodeLink3Node`

#### ObjectPlacer

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`GameObject`
- 字段依据示例：-

#### ObjectPool

- 功能分析：缓存/对象池类型：用于复用对象、缓存计算结果或降低运行时分配
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：4 个，`CommandBufferPool`、`ExecuteEvents`、`LayoutRebuilder`、`RecyclableObject`
- 它保存了哪些类型：1 个，`Transform`
- 字段依据示例：`CommandBufferPool` -> `s_BufferPool`: `ObjectPool<CommandBuffer>`；`ExecuteEvents` -> `s_HandlerListPool`: `ObjectPool<List<IEventSystemHandler>>`；`LayoutRebuilder` -> `s_Rebuilders`: `ObjectPool<LayoutRebuilder>`；`RecyclableObject` -> `pool`: `ObjectPool`

#### ObjImporter.meshStruct

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Vector2`、`Vector3`
- 字段依据示例：-

#### ObscuredTypesExamples

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`ExamplesGUI`
- 它保存了哪些类型：13 个，`ObscuredBool`、`ObscuredDecimal`、`ObscuredDouble`、`ObscuredFloat`、`ObscuredInt`、`ObscuredLong`、`ObscuredString`、`ObscuredVector2` 等 13 个
- 字段依据示例：`ExamplesGUI` -> `obscuredTypesExamples`: `ObscuredTypesExamples`

#### ObscuredVector2

- 功能分析：空间数据类型：保存位置、方向、旋转、速度或坐标信息
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`ObscuredTypesExamples`
- 它保存了哪些类型：2 个，`ObscuredVector2.RawEncryptedVector2`、`Vector2`
- 字段依据示例：`ObscuredTypesExamples` -> `obscuredVector2`: `ObscuredVector2`

#### ObscuredVector2Int

- 功能分析：空间数据类型：保存位置、方向、旋转、速度或坐标信息
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`ObscuredTypesExamples`
- 它保存了哪些类型：2 个，`ObscuredVector2Int.RawEncryptedVector2Int`、`Vector2Int`
- 字段依据示例：`ObscuredTypesExamples` -> `obscuredVector2Int`: `ObscuredVector2Int`

#### ObscuredVector3

- 功能分析：空间数据类型：保存位置、方向、旋转、速度或坐标信息
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`ObscuredTypesExamples`
- 它保存了哪些类型：2 个，`ObscuredVector3.RawEncryptedVector3`、`Vector3`
- 字段依据示例：`ObscuredTypesExamples` -> `obscuredVector3`: `ObscuredVector3`

#### ObscuredVector3Int

- 功能分析：空间数据类型：保存位置、方向、旋转、速度或坐标信息
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`ObscuredTypesExamples`
- 它保存了哪些类型：2 个，`ObscuredVector3Int.RawEncryptedVector3Int`、`Vector3Int`
- 字段依据示例：`ObscuredTypesExamples` -> `obscuredVector3Int`: `ObscuredVector3Int`

#### ObstacleVertex

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：5 个，`Agent`、`ObstacleVertex`、`RVONavmesh`、`RVOObstacle`、`Simulator`
- 它保存了哪些类型：4 个，`ObstacleVertex`、`RVOLayer`、`Vector2`、`Vector3`
- 字段依据示例：`Agent` -> `obstaclesBuffered`: `List<ObstacleVertex>`；`obstacles`: `List<ObstacleVertex>`；`ObstacleVertex` -> `next`: `ObstacleVertex`；`prev`: `ObstacleVertex`；`RVONavmesh` -> `obstacles`: `List<ObstacleVertex>`；`RVOObstacle` -> `addedObstacles`: `List<ObstacleVertex>`；`Simulator` -> `obstacles`: `List<ObstacleVertex>`

#### OffsetPose.EffectorLink

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`OffsetPose`
- 它保存了哪些类型：2 个，`FullBodyBipedEffector`、`Vector3`
- 字段依据示例：`OffsetPose` -> `effectorLinks`: `OffsetPose.EffectorLink[]`

#### ParticleSpaceSetter

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`ParticleSystem`
- 字段依据示例：-

#### ParticleSystem.MainModule

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`ParticleSystem`
- 字段依据示例：-

#### ParticleSystem.Particle

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`ParticleSystem.EmitParams`
- 它保存了哪些类型：2 个，`Color32`、`Vector3`
- 字段依据示例：`ParticleSystem.EmitParams` -> `m_Particle`: `ParticleSystem.Particle`

#### PathCompleteState

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 enum 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：0 个，-
- 字段依据示例：-

#### PathEndingCondition

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`ConstantPath`、`XPath`
- 它保存了哪些类型：1 个，`Path`
- 字段依据示例：`ConstantPath` -> `endingCondition`: `PathEndingCondition`；`XPath` -> `endingCondition`: `PathEndingCondition`

#### PathHandler

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：5 个，`AstarPath`、`GraphGizmoHelper`、`Path`、`PathProcessor`、`RetainedGizmos.Hasher`
- 它保存了哪些类型：3 个，`BinaryHeap`、`PathNode`、`StringBuilder`
- 字段依据示例：`AstarPath` -> `debugPathData`: `PathHandler`；`GraphGizmoHelper` -> `debugData`: `PathHandler`；`Path` -> `pathHandler`: `PathHandler`；`PathProcessor` -> `pathHandlers`: `PathHandler[]`；`RetainedGizmos.Hasher` -> `debugData`: `PathHandler`

#### PathModifier

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Seeker`
- 字段依据示例：-

#### PathNode

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：6 个，`ABPath`、`BinaryHeap.Tuple`、`Path`、`PathHandler`、`PathNode`、`RandomPath`
- 它保存了哪些类型：2 个，`GraphNode`、`PathNode`
- 字段依据示例：`ABPath` -> `partialBestTarget`: `PathNode`；`BinaryHeap.Tuple` -> `node`: `PathNode`；`Path` -> `currentR`: `PathNode`；`PathHandler` -> `nodes`: `PathNode[]`；`PathNode` -> `parent`: `PathNode`；另有 1 个来源

#### PathOptions

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：6 个，`AxisConstraint`、`OrientType`、`PathMode`、`Quaternion`、`Transform`、`Vector3`
- 字段依据示例：-

#### PathPool

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`Path`、`Stack`、`Type`
- 字段依据示例：-

#### PathReturnQueue

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`AstarPath`、`PathProcessor`
- 它保存了哪些类型：2 个，`Path`、`Queue`
- 字段依据示例：`AstarPath` -> `pathReturnQueue`: `PathReturnQueue`；`PathProcessor` -> `returnQueue`: `PathReturnQueue`

#### PathState

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 enum 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：0 个，-
- 字段依据示例：-

#### PathUtilities

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`GraphNode`、`Queue`
- 字段依据示例：-

#### Patrol

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`IAstarAI`、`Transform`
- 字段依据示例：-

#### PenetrationAvoidance.Avoider

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`PenetrationAvoidance`、`PenetrationAvoidance.Avoider`
- 它保存了哪些类型：5 个，`EffectorLink`、`LayerMask`、`PenetrationAvoidance.Avoider`、`Transform`、`Vector3`
- 字段依据示例：`PenetrationAvoidance` -> `avoiders`: `PenetrationAvoidance.Avoider[]`；`PenetrationAvoidance.Avoider` -> `effectors`: `PenetrationAvoidance.Avoider.EffectorLink[]`

#### PhysicsRaycaster

- 功能分析：物理检测类型：用于碰撞、射线检测、触发器或命中查询
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`Camera`、`LayerMask`、`RaycastHit`
- 字段依据示例：-

#### PixelPerfectCamera

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`PixelPerfectCameraInternal`
- 它保存了哪些类型：2 个，`Camera`、`PixelPerfectCameraInternal`
- 字段依据示例：`PixelPerfectCameraInternal` -> `m_SerializableComponent`: `PixelPerfectCamera`

#### Plane

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`BatchCullingContext`、`BatchRendererCullingOutput`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`BatchCullingContext` -> `cullingPlanes`: `NativeArray<Plane>`；`BatchRendererCullingOutput` -> `cullingPlanes`: `Plane*`

#### PointerEventData

- 功能分析：配置/数据类型：保存运行参数、资源引用、显示数据或系统配置
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：4 个，`PointerInputModule`、`PointerInputModule.MouseButtonEventData`、`StandaloneInputModule`、`TouchInputModule`
- 它保存了哪些类型：5 个，`GameObject`、`PointerEventData.InputButton`、`RaycastResult`、`Vector2`、`Vector3`
- 字段依据示例：`PointerInputModule` -> `m_PointerData`: `Dictionary<int, PointerEventData>`；`PointerInputModule.MouseButtonEventData` -> `buttonData`: `PointerEventData`；`StandaloneInputModule` -> `m_InputPointerEvent`: `PointerEventData`；`TouchInputModule` -> `m_InputPointerEvent`: `PointerEventData`

#### PointGraph

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`AstarData`
- 它保存了哪些类型：5 个，`LayerMask`、`PointKDTree`、`PointNode`、`Transform`、`Vector3`
- 字段依据示例：`AstarData` -> `<pointGraph>k__BackingField`: `PointGraph`

#### PointKDTree

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`PointGraph`
- 它保存了哪些类型：4 个，`GraphNode`、`IComparer`、`PointKDTree.Node`、`Stack`
- 字段依据示例：`PointGraph` -> `lookupTree`: `PointKDTree`

#### PointKDTree.Node

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`PointKDTree`
- 它保存了哪些类型：1 个，`GraphNode`
- 字段依据示例：`PointKDTree` -> `tree`: `PointKDTree.Node[]`

#### PointLight

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`FalloffType`、`LightMode`、`LinearColor`、`Quaternion`、`Vector3`
- 字段依据示例：-

#### PointNode

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`NodeLink2`、`PointGraph`
- 它保存了哪些类型：2 个，`Connection`、`GameObject`
- 字段依据示例：`NodeLink2` -> `<startNode>k__BackingField`: `PointNode`；`<endNode>k__BackingField`: `PointNode`；`PointGraph` -> `nodes`: `PointNode[]`

#### PointNodeTagModifier

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：-

#### Poser

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`InteractionEffector`
- 它保存了哪些类型：1 个，`Transform`
- 字段依据示例：`InteractionEffector` -> `poser`: `Poser`

#### PositionPredictor

- 功能分析：空间数据类型：保存位置、方向、旋转、速度或坐标信息
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`CinemachineComposer`、`CinemachineFramingTransposer`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`CinemachineComposer` -> `m_Predictor`: `PositionPredictor`；`CinemachineFramingTransposer` -> `m_Predictor`: `PositionPredictor`

#### PostProcessData

- 功能分析：配置/数据类型：保存运行参数、资源引用、显示数据或系统配置
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`ForwardRendererData`、`PostProcessPass`、`Renderer2DData`
- 它保存了哪些类型：2 个，`PostProcessData.ShaderResources`、`PostProcessData.TextureResources`
- 字段依据示例：`ForwardRendererData` -> `postProcessData`: `PostProcessData`；`PostProcessPass` -> `m_Data`: `PostProcessData`；`Renderer2DData` -> `m_PostProcessData`: `PostProcessData`

#### PostProcessData.TextureResources

- 功能分析：UI 控件类型：用于界面布局、文本、按钮、滚动、图形或交互控件
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`PostProcessData`
- 它保存了哪些类型：1 个，`Texture2D`
- 字段依据示例：`PostProcessData` -> `textures`: `PostProcessData.TextureResources`

#### PostProcessPass

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`ForwardRenderer`、`Renderer2D`
- 它保存了哪些类型：21 个，`Bloom`、`ChromaticAberration`、`ColorAdjustments`、`ColorLookup`、`DepthOfField`、`FilmGrain`、`GraphicsFormat`、`LensDistortion` 等 21 个
- 字段依据示例：`ForwardRenderer` -> `m_PostProcessPass`: `PostProcessPass`；`m_FinalPostProcessPass`: `PostProcessPass`；`Renderer2D` -> `m_PostProcessPass`: `PostProcessPass`；`m_FinalPostProcessPass`: `PostProcessPass`

#### PostProcessPass.MaterialLibrary

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`PostProcessPass`
- 它保存了哪些类型：1 个，`Material`
- 字段依据示例：`PostProcessPass` -> `m_Materials`: `PostProcessPass.MaterialLibrary`

#### PostureFloat

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`Recoil`、`WeaponData_Gun`
- 它保存了哪些类型：0 个，-
- 字段依据示例：`Recoil` -> `perturbMin`: `PostureFloat`；`perturbMax`: `PostureFloat`；`detailedReactYawShot`: `PostureFloat`；`WeaponData_Gun` -> `perturbMin`: `PostureFloat[]`；`perturbMax`: `PostureFloat[]`；`detailPerturbShot`: `PostureFloat[]`

#### ProceduralGridMover

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`GridGraph`、`GridNodeBase`、`Transform`
- 字段依据示例：-

#### ProceduralWorld

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`ProceduralWorld.ProceduralTile`
- 它保存了哪些类型：5 个，`Int2`、`ProceduralWorld.ProceduralPrefab`、`ProceduralWorld.ProceduralTile`、`Queue`、`Transform`
- 字段依据示例：`ProceduralWorld.ProceduralTile` -> `world`: `ProceduralWorld`

#### ProceduralWorld.ProceduralPrefab

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`ProceduralWorld`
- 它保存了哪些类型：3 个，`GameObject`、`ProceduralWorld.RotationRandomness`、`Vector2`
- 字段依据示例：`ProceduralWorld` -> `prefabs`: `ProceduralWorld.ProceduralPrefab[]`

#### ProceduralWorld.ProceduralTile

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`ProceduralWorld`
- 它保存了哪些类型：3 个，`ProceduralWorld`、`Random`、`Transform`
- 字段依据示例：`ProceduralWorld` -> `tiles`: `Dictionary<Int2, ProceduralWorld.ProceduralTile>`

#### PunctualLightData

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Vector3`、`Vector4`
- 字段依据示例：-

#### QuaternionOptions

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`AxisConstraint`、`RotateMode`、`Vector3`
- 字段依据示例：-

#### Queue

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：16 个，`AnimationTrack`、`GraphUpdateProcessor`、`HUD_ChatBox`、`HUD_KillMsg`、`HUD_NanoDamageScore`、`HierarchicalGraph`、`Lease`、`ObjectWriter` 等 16 个
- 它保存了哪些类型：0 个，-
- 字段依据示例：`AnimationTrack` -> `s_CachedQueue`: `Queue<Transform>`；`GraphUpdateProcessor` -> `graphUpdateQueue`: `Queue<GraphUpdateObject>`；`graphUpdateQueueAsync`: `Queue<GraphUpdateProcessor.GUOSingle>`；`graphUpdateQueuePost`: `Queue<GraphUpdateProcessor.GUOSingle>`；`HierarchicalGraph` -> `temporaryQueue`: `Queue<GraphNode>`；`HUD_ChatBox` -> `maskDataQueue`: `Queue<HUD_ChatBox.MsgMaskRectData>`；`HUD_KillMsg` -> `refreshTime`: `Queue<float>`；另有 11 个来源

#### QVModel.Data

- 功能分析：配置/数据类型：保存运行参数、资源引用、显示数据或系统配置
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`QVModel`
- 它保存了哪些类型：3 个，`ParticleSystem`、`Transform`、`Vector3`
- 字段依据示例：`QVModel` -> `left`: `QVModel.Data`；`right`: `QVModel.Data`

#### RagdollUtility

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`Animator`、`AnimatorUpdateMode`、`IK`、`RagdollUtility.Child`、`RagdollUtility.Rigidbone`
- 字段依据示例：-

#### RagdollUtility.Child

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`RagdollUtility`
- 它保存了哪些类型：3 个，`Quaternion`、`Transform`、`Vector3`
- 字段依据示例：`RagdollUtility` -> `children`: `RagdollUtility.Child[]`

#### RagdollUtility.Rigidbone

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`RagdollUtility`
- 它保存了哪些类型：6 个，`Collider`、`Joint`、`Quaternion`、`Rigidbody`、`Transform`、`Vector3`
- 字段依据示例：`RagdollUtility` -> `rigidbones`: `RagdollUtility.Rigidbone[]`

#### Random

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：6 个，`AlternativePath`、`Guid`、`ProceduralWorld.ProceduralTile`、`RandomPath`、`ThreadPoolWorkQueueThreadLocals`、`ThreadSafeRandom`
- 它保存了哪些类型：0 个，-
- 字段依据示例：`AlternativePath` -> `rnd`: `Random`；`Guid` -> `random`: `Random`；`ProceduralWorld.ProceduralTile` -> `rnd`: `Random`；`RandomPath` -> `rnd`: `Random`；`ThreadPoolWorkQueueThreadLocals` -> `random`: `Random`；另有 1 个来源

#### RandomItem

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`Nano4T_AttributeAsset.Group`、`Nano4TerminatorModeAsset`、`NanoModeAsset`
- 它保存了哪些类型：1 个，`RandomItem.Item`
- 字段依据示例：`Nano4T_AttributeAsset.Group` -> `nano`: `RandomItem`；`human`: `RandomItem`；`Nano4TerminatorModeAsset` -> `nanoGhostSupplyBoxItems`: `RandomItem`；`NanoModeAsset` -> `supplyBoxItems`: `RandomItem`

#### RandomPath

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`PathNode`、`Random`、`Vector3`
- 字段依据示例：-

#### RasterizationMesh

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Voxelize`
- 它保存了哪些类型：4 个，`Bounds`、`Matrix4x4`、`MeshFilter`、`Vector3`
- 字段依据示例：`Voxelize` -> `inputMeshes`: `List<RasterizationMesh>`

#### Ray

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：-

#### RaycastHit2D

- 功能分析：战斗结算类型：用于伤害、命中、击杀、爆头或战斗反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Physics2DRaycaster`
- 它保存了哪些类型：1 个，`Vector2`
- 字段依据示例：`Physics2DRaycaster` -> `m_Hits`: `RaycastHit2D[]`

#### RaycastModifier

- 功能分析：物理检测类型：用于碰撞、射线检测、触发器或命中查询
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`LayerMask`、`RaycastModifier.Quality`、`Vector3`
- 字段依据示例：-

#### RaycastResult

- 功能分析：物理检测类型：用于碰撞、射线检测、触发器或命中查询
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`BaseInputModule`、`EventSystem`、`PointerEventData`
- 它保存了哪些类型：4 个，`BaseRaycaster`、`GameObject`、`Vector2`、`Vector3`
- 字段依据示例：`BaseInputModule` -> `m_RaycastResultCache`: `List<RaycastResult>`；`EventSystem` -> `s_RaycastComparer`: `Comparison<RaycastResult>`；`PointerEventData` -> `<pointerCurrentRaycast>k__BackingField`: `RaycastResult`；`<pointerPressRaycast>k__BackingField`: `RaycastResult`

#### RecastGraph

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`AstarData`
- 它保存了哪些类型：5 个，`LayerMask`、`NavmeshTile`、`RecastGraph.RelevantGraphSurfaceMode`、`Vector3`、`Voxelize`
- 字段依据示例：`AstarData` -> `<recastGraph>k__BackingField`: `RecastGraph`

#### RecastMeshGatherer

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`Bounds`、`LayerMask`、`RecastMeshGatherer.CapsuleCache`、`Vector3`
- 字段依据示例：-

#### RecastMeshGatherer.CapsuleCache

- 功能分析：缓存/对象池类型：用于复用对象、缓存计算结果或降低运行时分配
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`RecastMeshGatherer`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`RecastMeshGatherer` -> `capsuleCache`: `List<RecastMeshGatherer.CapsuleCache>`

#### Recoil.RecoilOffset

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Recoil.RecoilOffset`
- 它保存了哪些类型：3 个，`EffectorLink`、`Recoil.RecoilOffset`、`Vector3`
- 字段依据示例：`Recoil.RecoilOffset` -> `effectorLinks`: `Recoil.RecoilOffset.EffectorLink[]`

#### Rect

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：17 个，`AstarDebugger`、`CameraData`、`CameraProperties`、`CinemachineComposer.FovCache`、`GUI`、`GUILayoutEntry`、`GUILayoutUtility`、`PixelPerfectCameraInternal` 等 17 个
- 它保存了哪些类型：0 个，-
- 字段依据示例：`AstarDebugger` -> `boxRect`: `Rect`；`CameraData` -> `pixelRect`: `Rect`；`CameraProperties` -> `screenRect`: `Rect`；`CinemachineComposer.FovCache` -> `mFovSoftGuideRect`: `Rect`；`mFovHardGuideRect`: `Rect`；`mSoftGuideRect`: `Rect`；`GUI` -> `s_ToolTipRect`: `Rect`；另有 12 个来源

#### RectangleLight

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`FalloffType`、`LightMode`、`LinearColor`、`Quaternion`、`Vector3`
- 字段依据示例：-

#### RectangularVertexClipper

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`RectMask2D`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`RectMask2D` -> `m_VertexClipper`: `RectangularVertexClipper`

#### RectMask2D

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`MaskableGraphic`、`RectMask2D`
- 它保存了哪些类型：11 个，`Canvas`、`HashSet`、`IClippable`、`MaskableGraphic`、`Rect`、`RectMask2D`、`RectTransform`、`RectangularVertexClipper` 等 11 个
- 字段依据示例：`MaskableGraphic` -> `m_ParentMask`: `RectMask2D`；`RectMask2D` -> `m_Clippers`: `List<RectMask2D>`

#### RectTransformUtility

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：-

#### RelevantGraphSurface

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`RelevantGraphSurface`
- 它保存了哪些类型：2 个，`RelevantGraphSurface`、`Vector3`
- 字段依据示例：`RelevantGraphSurface` -> `root`: `RelevantGraphSurface`；`prev`: `RelevantGraphSurface`；`next`: `RelevantGraphSurface`

#### Renderer2D

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：10 个，`ColorGradingLutPass`、`FinalBlitPass`、`Light2DCullResult`、`Material`、`PixelPerfectBackgroundPass`、`PostProcessPass`、`ProfilingSampler`、`Render2DLightingPass` 等 10 个
- 字段依据示例：-

#### Renderer2DData

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`Render2DLightingPass`、`Renderer2D`
- 它保存了哪些类型：8 个，`ILight2DCullResult`、`Light2DBlendStyle`、`Material`、`PostProcessData`、`RenderTargetHandle`、`Shader`、`TransparencySortMode`、`Vector3`
- 字段依据示例：`Render2DLightingPass` -> `m_Renderer2DData`: `Renderer2DData`；`Renderer2D` -> `m_Renderer2DData`: `Renderer2DData`

#### RendererLighting

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`Color`、`GraphicsFormat`、`ProfilingSampler`、`ShaderTagId`
- 字段依据示例：-

#### RendererListDesc

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`RenderGraphResourceRegistry.RendererListResource`
- 它保存了哪些类型：8 个，`Camera`、`CullingResults`、`Material`、`PerObjectData`、`RenderQueueRange`、`RenderStateBlock`、`ShaderTagId`、`SortingCriteria`
- 字段依据示例：`RenderGraphResourceRegistry.RendererListResource` -> `desc`: `RendererListDesc`

#### RenderingMode

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 enum 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：0 个，-
- 字段依据示例：-

#### RenderingUtils

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：7 个，`FormatUsage`、`GraphicsFormat`、`Material`、`Mesh`、`RenderTextureFormat`、`RenderingUtils.StereoConstants`、`ShaderTagId`
- 字段依据示例：-

#### RenderObjects.RenderObjectsSettings

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`RenderObjects`
- 它保存了哪些类型：6 个，`CompareFunction`、`Material`、`RenderObjects.CustomCameraSettings`、`RenderObjects.FilterSettings`、`RenderPassEvent`、`StencilStateData`
- 字段依据示例：`RenderObjects` -> `settings`: `RenderObjects.RenderObjectsSettings`

#### RenderObjectsPass

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`RenderObjects`
- 它保存了哪些类型：7 个，`FilteringSettings`、`Material`、`ProfilingSampler`、`RenderObjects.CustomCameraSettings`、`RenderQueueType`、`RenderStateBlock`、`ShaderTagId`
- 字段依据示例：`RenderObjects` -> `renderObjectsPass`: `RenderObjectsPass`

#### RenderPipelineManager

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`Camera`、`RenderPipeline`、`RenderPipelineAsset`
- 字段依据示例：-

#### RequiredReferences

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`DrawableDictionary`
- 它保存了哪些类型：3 个，`AudioClip`、`GameObject`、`Material`
- 字段依据示例：`DrawableDictionary` -> `reqReferences`: `RequiredReferences`

#### RetainedGizmos

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`AstarPath`、`GraphGizmoHelper`
- 它保存了哪些类型：5 个，`HashSet`、`Material`、`Mesh`、`RetainedGizmos.MeshWithHash`、`Stack`
- 字段依据示例：`AstarPath` -> `gizmos`: `RetainedGizmos`；`GraphGizmoHelper` -> `gizmos`: `RetainedGizmos`

#### RetainedGizmos.Builder

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`GraphGizmoHelper`
- 它保存了哪些类型：3 个，`Color32`、`Mesh`、`Vector3`
- 字段依据示例：`GraphGizmoHelper` -> `<builder>k__BackingField`: `RetainedGizmos.Builder`

#### RichAI

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`AnimationLinkTraverser`
- 它保存了哪些类型：4 个，`Animation`、`Color`、`RichPath`、`Vector3`
- 字段依据示例：`AnimationLinkTraverser` -> `ai`: `RichAI`

#### RichFunnel

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`NavmeshBase`、`Queue`、`RichPath`、`TriangleMeshNode`、`Vector3`
- 字段依据示例：-

#### RichPath

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`RichAI`、`RichFunnel`
- 它保存了哪些类型：4 个，`ITransform`、`RichPathPart`、`Seeker`、`Vector3`
- 字段依据示例：`RichAI` -> `richPath`: `RichPath`；`RichFunnel` -> `path`: `RichPath`

#### RichSpecial

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`NodeLink2`、`Transform`
- 字段依据示例：-

#### RopeTrigger

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：-

#### RotationLimit

- 功能分析：空间数据类型：保存位置、方向、旋转、速度或坐标信息
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`IKSolver.Bone`、`IKSolverAim`
- 它保存了哪些类型：2 个，`Quaternion`、`Vector3`
- 字段依据示例：`IKSolver.Bone` -> `_rotationLimit`: `RotationLimit`；`IKSolverAim` -> `transformLimit`: `RotationLimit`

#### RotationLimitPolygonal

- 功能分析：空间数据类型：保存位置、方向、旋转、速度或坐标信息
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`RotationLimitPolygonal.LimitPoint`、`RotationLimitPolygonal.ReachCone`、`Vector3`
- 字段依据示例：-

#### RotationLimitPolygonal.LimitPoint

- 功能分析：空间数据类型：保存位置、方向、旋转、速度或坐标信息
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`RotationLimitPolygonal`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`RotationLimitPolygonal` -> `points`: `RotationLimitPolygonal.LimitPoint[]`

#### RotationLimitPolygonal.ReachCone

- 功能分析：空间数据类型：保存位置、方向、旋转、速度或坐标信息
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`RotationLimitPolygonal`
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：`RotationLimitPolygonal` -> `reachCones`: `RotationLimitPolygonal.ReachCone[]`

#### RTHandle

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：5 个，`BufferedRTHandleSystem`、`RTHandleSystem`、`RenderGraphDefaultResources`、`RenderGraphResourceRegistry`、`TextureXR`
- 它保存了哪些类型：6 个，`RTHandleSystem`、`RenderTargetIdentifier`、`RenderTexture`、`Texture`、`Vector2`、`Vector2Int`
- 字段依据示例：`BufferedRTHandleSystem` -> `m_RTHandles`: `Dictionary<int, RTHandle[]>`；`RenderGraphDefaultResources` -> `m_BlackTexture2D`: `RTHandle`；`m_WhiteTexture2D`: `RTHandle`；`m_ShadowTexture2D`: `RTHandle`；`RenderGraphResourceRegistry` -> `m_CurrentBackbuffer`: `RTHandle`；`RTHandleSystem` -> `m_AutoSizedRTs`: `HashSet<RTHandle>`；`m_AutoSizedRTsArray`: `RTHandle[]`；`m_ResizeOnDemandRTs`: `HashSet<RTHandle>`；`TextureXR` -> `m_BlackUIntTexture2DArrayRTH`: `RTHandle`；`m_BlackUIntTextureRTH`: `RTHandle`；`m_ClearTexture2DArrayRTH`: `RTHandle`

#### RTHandleProperties

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`RTHandleSystem`
- 它保存了哪些类型：2 个，`Vector2Int`、`Vector4`
- 字段依据示例：`RTHandleSystem` -> `m_RTHandleProperties`: `RTHandleProperties`

#### RuntimeUtility

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`GameObject`、`RaycastHit`、`SphereCollider`
- 字段依据示例：-

#### RVOController

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`AIBase`
- 它保存了哪些类型：5 个，`IAgent`、`IAstarAI`、`RVOLayer`、`Simulator`、`Transform`
- 字段依据示例：`AIBase` -> `rvoController`: `RVOController`

#### RVOObstacle

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：6 个，`Matrix4x4`、`ObstacleVertex`、`RVOLayer`、`RVOObstacle.ObstacleVertexWinding`、`Simulator`、`Vector3`
- 字段依据示例：-

#### RVOQuadtree.QuadtreeQuery

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`Agent`、`RVOQuadtree.Node`、`Vector2`
- 字段依据示例：-

#### RVOSquareObstacle

- 功能分析：寻路/导航类型：用于 AI 路径搜索、导航网格、避障或路径节点
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector2`
- 字段依据示例：-

#### SceneViewDepthCopyPass

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`Material`、`ProfilingSampler`、`RenderTargetHandle`
- 字段依据示例：-

#### ScreenSpaceAmbientOcclusion

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`Material`、`ScreenSpaceAmbientOcclusion.ScreenSpaceAmbientOcclusionPass`、`ScreenSpaceAmbientOcclusionSettings`、`Shader`
- 字段依据示例：-

#### ScreenSpaceAmbientOcclusion.ScreenSpaceAmbientOcclusionPass

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`ScreenSpaceAmbientOcclusion`
- 它保存了哪些类型：5 个，`Material`、`ProfilingSampler`、`RenderTargetIdentifier`、`RenderTextureDescriptor`、`ScreenSpaceAmbientOcclusionSettings`
- 字段依据示例：`ScreenSpaceAmbientOcclusion` -> `m_SSAOPass`: `ScreenSpaceAmbientOcclusion.ScreenSpaceAmbientOcclusionPass`

#### ScreenSpaceShadowResolvePass

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`Material`、`RenderTargetHandle`、`RenderTextureDescriptor`
- 字段依据示例：-

#### ScriptableCullingParameters

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`ScriptableCullingParameters`、`XRPass`、`XRPassCreateInfo`
- 它保存了哪些类型：9 个，`CameraProperties`、`CullingOptions`、`LODParameters`、`Matrix4x4`、`ReflectionProbeSortingCriteria`、`ScriptableCullingParameters`、`Vector3`、`m_CullingPlanes` 等 9 个
- 字段依据示例：`ScriptableCullingParameters` -> `m_CullingPlanes`: `ScriptableCullingParameters.<m_CullingPlanes>e__FixedBuffer`；`m_LayerFarCullDistances`: `ScriptableCullingParameters.<m_LayerFarCullDistances>e__FixedBuffer`；`XRPass` -> `<cullingParams>k__BackingField`: `ScriptableCullingParameters`；`XRPassCreateInfo` -> `cullingParameters`: `ScriptableCullingParameters`

#### ScriptableRenderer

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`CameraData`、`ScriptableRenderer`、`UniversalRenderPipelineAsset`
- 它保存了哪些类型：9 个，`GraphicsDeviceType`、`ProfilingSampler`、`RenderBufferStoreAction`、`RenderTargetIdentifier`、`ScriptableRenderPass`、`ScriptableRenderer`、`ScriptableRenderer.RenderingFeatures`、`ScriptableRendererFeature` 等 9 个
- 字段依据示例：`CameraData` -> `renderer`: `ScriptableRenderer`；`ScriptableRenderer` -> `current`: `ScriptableRenderer`；`UniversalRenderPipelineAsset` -> `m_Renderers`: `ScriptableRenderer[]`

#### ScriptableRendererData

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`UniversalRenderPipelineAsset`
- 它保存了哪些类型：1 个，`ScriptableRendererFeature`
- 字段依据示例：`UniversalRenderPipelineAsset` -> `m_RendererData`: `ScriptableRendererData`；`m_RendererDataList`: `ScriptableRendererData[]`

#### ScriptableRenderPass

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`ScriptableRenderer`
- 它保存了哪些类型：7 个，`ClearFlag`、`Color`、`ProfilingSampler`、`RenderBufferStoreAction`、`RenderPassEvent`、`RenderTargetIdentifier`、`ScriptableRenderPassInput`
- 字段依据示例：`ScriptableRenderer` -> `m_ActiveRenderPassQueue`: `List<ScriptableRenderPass>`

#### Scrollbar

- 功能分析：UI 控件类型：用于界面布局、文本、按钮、滚动、图形或交互控件
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`ScrollRect`、`UI_ItemPanel`
- 它保存了哪些类型：6 个，`Coroutine`、`DrivenRectTransformTracker`、`RectTransform`、`Scrollbar.Direction`、`Scrollbar.ScrollEvent`、`Vector2`
- 字段依据示例：`ScrollRect` -> `m_HorizontalScrollbar`: `Scrollbar`；`m_VerticalScrollbar`: `Scrollbar`；`UI_ItemPanel` -> `scrollbar`: `Scrollbar`

#### ScrollRect

- 功能分析：UI 控件类型：用于界面布局、文本、按钮、滚动、图形或交互控件
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`DebugUIHandlerPanel`
- 它保存了哪些类型：9 个，`Bounds`、`DrivenRectTransformTracker`、`RectTransform`、`ScrollRect.MovementType`、`ScrollRect.ScrollRectEvent`、`ScrollRect.ScrollbarVisibility`、`Scrollbar`、`Vector2` 等 9 个
- 字段依据示例：`DebugUIHandlerPanel` -> `scrollRect`: `ScrollRect`

#### SendMouseEvents

- 功能分析：输入交互类型：用于鼠标、触摸、按键或输入模块状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Camera`、`SendMouseEvents.HitInfo`
- 字段依据示例：-

#### SendMouseEvents.HitInfo

- 功能分析：战斗结算类型：用于伤害、命中、击杀、爆头或战斗反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`SendMouseEvents`
- 它保存了哪些类型：2 个，`Camera`、`GameObject`
- 字段依据示例：`SendMouseEvents` -> `m_LastHit`: `SendMouseEvents.HitInfo[]`；`m_MouseDownHit`: `SendMouseEvents.HitInfo[]`；`m_CurrentHit`: `SendMouseEvents.HitInfo[]`

#### SentryGunSystem

- 功能分析：武器相关类型：用于武器数据、发射逻辑、弹药、投掷物或特殊武器表现
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`NameKeyPool`
- 字段依据示例：-

#### Shadow

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Color`、`Vector2`
- 字段依据示例：-

#### ShadowCaster2D

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`ShadowCasterGroup2D`
- 它保存了哪些类型：3 个，`Mesh`、`ShadowCasterGroup2D`、`Vector3`
- 字段依据示例：`ShadowCasterGroup2D` -> `m_ShadowCasters`: `List<ShadowCaster2D>`

#### ShadowData

- 功能分析：配置/数据类型：保存运行参数、资源引用、显示数据或系统配置
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`RenderingData`
- 它保存了哪些类型：2 个，`Vector3`、`Vector4`
- 字段依据示例：`RenderingData` -> `shadowData`: `ShadowData`

#### ShootPosture

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 enum 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：0 个，-
- 字段依据示例：-

#### SideReactDirect

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`Recoil`、`WeaponData_Gun`
- 它保存了哪些类型：1 个，`SideReactDirect.Data`
- 字段依据示例：`Recoil` -> `sideReactDirect`: `SideReactDirect`；`WeaponData_Gun` -> `sideReactDirect`: `SideReactDirect`

#### SimpleHudBase

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`GameObject`
- 字段依据示例：-

#### Simulator.WorkerContext

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`Simulator`、`Simulator.Worker`
- 它保存了哪些类型：2 个，`Agent.VOBuffer`、`Vector2`
- 字段依据示例：`Simulator` -> `coroutineWorkerContext`: `Simulator.WorkerContext`；`Simulator.Worker` -> `context`: `Simulator.WorkerContext`

#### SingleNodeBlocker

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`BlockManager`、`BlockManager.TraversalProvider`、`TurnBasedAI`
- 它保存了哪些类型：2 个，`BlockManager`、`GraphNode`
- 字段依据示例：`BlockManager` -> `blocked`: `Dictionary<GraphNode, List<SingleNodeBlocker>>`；`BlockManager.TraversalProvider` -> `selector`: `List<SingleNodeBlocker>`；`TurnBasedAI` -> `blocker`: `SingleNodeBlocker`

#### SkeletonBone

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`HumanDescription`
- 它保存了哪些类型：2 个，`Quaternion`、`Vector3`
- 字段依据示例：`HumanDescription` -> `skeleton`: `SkeletonBone[]`

#### Slider

- 功能分析：UI 控件类型：用于界面布局、文本、按钮、滚动、图形或交互控件
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`UI_Option`、`VFXUISliderBinder`
- 它保存了哪些类型：7 个，`DrivenRectTransformTracker`、`Image`、`RectTransform`、`Slider.Direction`、`Slider.SliderEvent`、`Transform`、`Vector2`
- 字段依据示例：`UI_Option` -> `mouseSpeed`: `Slider`；`zoomSpeed`: `Slider`；`bgmSlider`: `Slider`；`VFXUISliderBinder` -> `Target`: `Slider`

#### SO_2dSound

- 功能分析：ScriptableObject 配置资源：用资源文件保存声音、道具、武器或界面配置
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`SoundManager`
- 它保存了哪些类型：1 个，`AudioClip`
- 字段依据示例：`SoundManager` -> `_2dSnd`: `Dictionary<string, SO_2dSound>`

#### SO_3dSound

- 功能分析：ScriptableObject 配置资源：用资源文件保存声音、道具、武器或界面配置
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`SoundManager`
- 它保存了哪些类型：1 个，`AudioClip`
- 字段依据示例：`SoundManager` -> `_3dSnd`: `Dictionary<string, SO_3dSound>`

#### SO_FxGroup.FxData

- 功能分析：ScriptableObject 配置资源：用资源文件保存声音、道具、武器或界面配置
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`SO_FxGroup`
- 它保存了哪些类型：2 个，`GameObject`、`Vector3`
- 字段依据示例：`SO_FxGroup` -> `allFx`: `SO_FxGroup.FxData[]`

#### SO_Item

- 功能分析：ScriptableObject 配置资源：用资源文件保存声音、道具、武器或界面配置
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`ItemObject`、`UI_Inven`
- 它保存了哪些类型：3 个，`ItemAttribute`、`SO_Item.Level`、`Texture`
- 字段依据示例：`ItemObject` -> `<data>k__BackingField`: `SO_Item`；`UI_Inven` -> `itemDic`: `Dictionary<int, SO_Item>`

#### SO_Item_Wpn

- 功能分析：ScriptableObject 配置资源：用资源文件保存声音、道具、武器或界面配置
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`WeaponClass`
- 字段依据示例：-

#### SO_Item_Wpn_Throw

- 功能分析：ScriptableObject 配置资源：用资源文件保存声音、道具、武器或界面配置
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Texture`
- 字段依据示例：-

#### SocketItem

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`SocketItem.ItemType`、`Vector3`
- 字段依据示例：-

#### SoftMask

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`SoftMask`、`SoftMaskable`
- 它保存了哪些类型：11 个，`Color`、`CommandBuffer`、`Material`、`MaterialPropertyBlock`、`Matrix4x4`、`Mesh`、`RenderTexture`、`Shader` 等 11 个
- 字段依据示例：`SoftMask` -> `s_TmpSoftMasks`: `List<SoftMask>[]`；`s_ActiveSoftMasks`: `List<SoftMask>`；`s_TempRelatables`: `List<SoftMask>`；`SoftMaskable` -> `_softMask`: `SoftMask`

#### SoftMaskable

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`SoftMaskable`
- 它保存了哪些类型：5 个，`Graphic`、`Hash128`、`Material`、`SoftMask`、`SoftMaskable`
- 字段依据示例：`SoftMaskable` -> `s_ActiveSoftMaskables`: `List<SoftMaskable>`

#### SolverManager

- 功能分析：管理器类：集中维护对应系统的运行时对象和流程
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Animation`、`Animator`
- 字段依据示例：-

#### SortingSettings

- 功能分析：配置/数据类型：保存运行参数、资源引用、显示数据或系统配置
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`DrawingSettings`
- 它保存了哪些类型：4 个，`DistanceMetric`、`Matrix4x4`、`SortingCriteria`、`Vector3`
- 字段依据示例：`DrawingSettings` -> `m_SortingSettings`: `SortingSettings`

#### SoundManager

- 功能分析：声音类型：用于音效资源、触发播放、脚步声、武器声或环境声
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：7 个，`AudioClip`、`ChannelSound`、`GameObject`、`SO_2dSound`、`SO_3dSound`、`SimpleObjectPool`、`Vector2`
- 字段依据示例：-

#### SpawnOverDistance

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：-

#### SpawnOverDistance.InputProperties

- 功能分析：输入交互类型：用于鼠标、触摸、按键或输入模块状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：-

#### SpotLight

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：6 个，`AngularFalloffType`、`FalloffType`、`LightMode`、`LinearColor`、`Quaternion`、`Vector3`
- 字段依据示例：-

#### SpriteBone

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Quaternion`、`Vector3`
- 字段依据示例：-

#### SpriteIntermediateRendererInfo

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`Bounds`、`Color`、`Matrix4x4`
- 字段依据示例：-

#### SpriteState

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Selectable`
- 它保存了哪些类型：1 个，`Sprite`
- 字段依据示例：`Selectable` -> `m_SpriteState`: `SpriteState`

#### StandaloneInputModule

- 功能分析：输入交互类型：用于鼠标、触摸、按键或输入模块状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`GameObject`、`PointerEventData`、`Vector2`
- 字段依据示例：-

#### StartEndModifier

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Seeker`
- 它保存了哪些类型：3 个，`GraphNode`、`LayerMask`、`StartEndModifier.Exactness`
- 字段依据示例：`Seeker` -> `startEndModifier`: `StartEndModifier`

#### StaticPointVirtualCamera

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`CameraState`、`Transform`
- 字段依据示例：-

#### StencilMaterial.MatEntry

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`StencilMaterial`
- 它保存了哪些类型：4 个，`ColorWriteMask`、`CompareFunction`、`Material`、`StencilOp`
- 字段依据示例：`StencilMaterial` -> `m_List`: `List<StencilMaterial.MatEntry>`

#### StencilStateData

- 功能分析：配置/数据类型：保存运行参数、资源引用、显示数据或系统配置
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`ForwardRendererData`、`RenderObjects.RenderObjectsSettings`
- 它保存了哪些类型：2 个，`CompareFunction`、`StencilOp`
- 字段依据示例：`ForwardRendererData` -> `m_DefaultStencilState`: `StencilStateData`；`RenderObjects.RenderObjectsSettings` -> `stencilSettings`: `StencilStateData`

#### StunGrenadeArea

- 功能分析：武器相关类型：用于武器数据、发射逻辑、弹药、投掷物或特殊武器表现
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`AudioClip`
- 字段依据示例：-

#### StunGrenadeSFX

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`RawImage`
- 字段依据示例：-

#### TargetMover

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`Camera`、`IAstarAI`、`LayerMask`、`Transform`
- 字段依据示例：-

#### TargetPositionCache

- 功能分析：缓存/对象池类型：用于复用对象、缓存计算结果或降低运行时分配
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`TargetPositionCache.CacheEntry`、`TargetPositionCache.Mode`、`TargetPositionCache.TimeRange`、`Transform`
- 字段依据示例：-

#### TargetPositionCache.CacheCurve.Item

- 功能分析：缓存/对象池类型：用于复用对象、缓存计算结果或降低运行时分配
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Quaternion`、`Vector3`
- 字段依据示例：-

#### TerminatorCharacterEffect

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`CharacterEffect.FxData`、`EffectObj`
- 字段依据示例：-

#### TerrainUtility.TerrainMap

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`TerrainUtility.TerrainMap`
- 它保存了哪些类型：5 个，`ErrorCode`、`Terrain`、`TerrainUtility.TerrainMap`、`TileCoord`、`Vector3`
- 字段依据示例：`TerrainUtility.TerrainMap` -> `m_errorCode`: `TerrainUtility.TerrainMap.ErrorCode`；`m_terrainTiles`: `Dictionary<TerrainUtility.TerrainMap.TileCoord, Terrain>`

#### TextEditor

- 功能分析：UI 控件类型：用于界面布局、文本、按钮、滚动、图形或交互控件
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`GUIContent`、`GUIStyle`、`TextEditor.DblClickSnapping`、`TouchScreenKeyboard`、`Vector2`
- 字段依据示例：-

#### TextGenerationSettings

- 功能分析：UI 控件类型：用于界面布局、文本、按钮、滚动、图形或交互控件
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`TextGenerator`
- 它保存了哪些类型：7 个，`Color`、`Font`、`FontStyle`、`HorizontalWrapMode`、`TextAnchor`、`Vector2`、`VerticalWrapMode`
- 字段依据示例：`TextGenerator` -> `m_LastSettings`: `TextGenerationSettings`

#### TextGenerator

- 功能分析：UI 控件类型：用于界面布局、文本、按钮、滚动、图形或交互控件
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`InputField`、`Text`
- 它保存了哪些类型：5 个，`TextGenerationError`、`TextGenerationSettings`、`UICharInfo`、`UILineInfo`、`UIVertex`
- 字段依据示例：`InputField` -> `m_InputTextCache`: `TextGenerator`；`Text` -> `m_TextCache`: `TextGenerator`；`m_TextCacheForLayout`: `TextGenerator`

#### TextureAnimation

- 功能分析：UI 控件类型：用于界面布局、文本、按钮、滚动、图形或交互控件
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Material`、`Texture`
- 字段依据示例：-

#### TextureCurve

- 功能分析：UI 控件类型：用于界面布局、文本、按钮、滚动、图形或交互控件
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`AnimationCurve`、`Texture2D`
- 字段依据示例：-

#### TextureDesc

- 功能分析：UI 控件类型：用于界面布局、文本、按钮、滚动、图形或交互控件
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：11 个，`Color`、`DepthBits`、`FastMemoryDesc`、`FilterMode`、`GraphicsFormat`、`MSAASamples`、`RenderTextureMemoryless`、`TextureDimension` 等 11 个
- 字段依据示例：-

#### TextureXR

- 功能分析：UI 控件类型：用于界面布局、文本、按钮、滚动、图形或交互控件
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`RTHandle`、`Texture`、`Texture2D`、`Texture2DArray`、`Texture3D`
- 字段依据示例：-

#### ThermalVisionPass

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`ThermalVisionFeature`
- 它保存了哪些类型：3 个，`Material`、`RenderTargetIdentifier`、`ThermalVision`
- 字段依据示例：`ThermalVisionFeature` -> `thermalVisionPass`: `ThermalVisionPass`

#### ThreadControlQueue

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`PathProcessor`
- 它保存了哪些类型：2 个，`ManualResetEvent`、`Path`
- 字段依据示例：`PathProcessor` -> `queue`: `ThreadControlQueue`

#### Tile

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：6 个，`Color`、`GameObject`、`Matrix4x4`、`Sprite`、`Tile.ColliderType`、`TileFlags`
- 字段依据示例：-

#### TileAnimationData

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Sprite`
- 字段依据示例：-

#### Touch

- 功能分析：输入交互类型：用于鼠标、触摸、按键或输入模块状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`TouchPhase`、`TouchType`、`Vector2`
- 字段依据示例：-

#### TouchInputModule

- 功能分析：输入交互类型：用于鼠标、触摸、按键或输入模块状态
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`PointerEventData`、`Vector2`
- 字段依据示例：-

#### TQ

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Quaternion`、`Vector3`
- 字段依据示例：-

#### TrackColorAttribute

- 功能分析：颜色配置类型：用于 UI、特效、渲染或阵营表现的颜色数据
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Color`
- 字段依据示例：-

#### Transform.Enumerator

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Transform`
- 字段依据示例：-

#### TreeInstance

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Color32`、`Vector3`
- 字段依据示例：-

#### TreePrototype

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`GameObject`
- 字段依据示例：-

#### TriggerEnterSound

- 功能分析：声音类型：用于音效资源、触发播放、脚步声、武器声或环境声
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`AudioClip`
- 字段依据示例：-

#### TriggerEventBroadcaster

- 功能分析：事件数据类型：用于在系统之间传递状态变化、动画回调或玩法通知
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`GameObject`
- 字段依据示例：-

#### TSBPD_DM

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Text`
- 字段依据示例：-

#### TSBPD_TD

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`GameObject`、`Image`、`Text`
- 字段依据示例：-

#### TurnBasedAI

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`BlockManager`、`BlockManager.TraversalProvider`、`GraphNode`、`SingleNodeBlocker`
- 字段依据示例：-

#### TweenLink

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`TweenManager`
- 它保存了哪些类型：2 个，`GameObject`、`LinkBehaviour`
- 字段依据示例：`TweenManager` -> `_TweenLinks`: `Dictionary<Tween, TweenLink>`

#### TwistRelaxer

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`IK`、`Transform`、`Vector3`
- 字段依据示例：-

#### UI_GameLoading

- 功能分析：UI 界面类：负责菜单、房间、背包或游戏内交互显示
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Image`、`RawImage`
- 字段依据示例：-

#### UI_Inven

- 功能分析：UI 界面类：负责菜单、房间、背包或游戏内交互显示
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：9 个，`GameObject`、`ItemObject`、`SO_Item`、`Texture2D`、`UI_ItemBox`、`UI_ItemBox_Throw`、`UI_ItemPanel`、`UI_SelectionGroup` 等 9 个
- 字段依据示例：-

#### UI_InvenItem

- 功能分析：UI 界面类：负责菜单、房间、背包或游戏内交互显示
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`GameObject`
- 字段依据示例：-

#### UI_ItemBox

- 功能分析：UI 界面类：负责菜单、房间、背包或游戏内交互显示
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`UI_GameRoom`、`UI_Inven`、`UI_ItemPanel`
- 它保存了哪些类型：4 个，`Button`、`ItemObject`、`RawImage`、`Text`
- 字段依据示例：`UI_GameRoom` -> `wpnSlots`: `UI_ItemBox[]`；`UI_Inven` -> `wpnSlots`: `UI_ItemBox[]`；`UI_ItemPanel` -> `boxList`: `List<UI_ItemBox>`

#### UI_ItemBox_Throw

- 功能分析：UI 界面类：负责菜单、房间、背包或游戏内交互显示
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`UI_GameRoom`、`UI_Inven`
- 它保存了哪些类型：3 个，`Button`、`ItemObject`、`RawImage`
- 字段依据示例：`UI_GameRoom` -> `wpnSlot_Throw`: `UI_ItemBox_Throw`；`UI_Inven` -> `wpnSlot_Throw`: `UI_ItemBox_Throw`

#### UI_ItemPanel

- 功能分析：UI 界面类：负责菜单、房间、背包或游戏内交互显示
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`UI_Inven`
- 它保存了哪些类型：5 个，`GameObject`、`ItemObject`、`Scrollbar`、`UI_ItemBox`、`Vector4`
- 字段依据示例：`UI_Inven` -> `itemPanel`: `UI_ItemPanel`

#### UI_Option

- 功能分析：UI 界面类：负责菜单、房间、背包或游戏内交互显示
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：6 个，`AudioMixer`、`Dropdown`、`Slider`、`UI_SelectionGroup`、`UI_Tab`、`Vector2Int`
- 字段依据示例：-

#### UI_SelectionGroup

- 功能分析：UI 界面类：负责菜单、房间、背包或游戏内交互显示
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`UI_GameRoom`、`UI_Inven`、`UI_Option`
- 它保存了哪些类型：2 个，`Button`、`UnityEvent`
- 字段依据示例：`UI_GameRoom` -> `wpnBagTab`: `UI_SelectionGroup`；`UI_Inven` -> `wpnBagTab`: `UI_SelectionGroup`；`weaponTabs`: `UI_SelectionGroup`；`UI_Option` -> `fullScreenSwitch`: `UI_SelectionGroup`；`bgmSwitch`: `UI_SelectionGroup`；`sndSwitch`: `UI_SelectionGroup`

#### UI_SliderValueText

- 功能分析：UI 界面类：负责菜单、房间、背包或游戏内交互显示
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Text`
- 字段依据示例：-

#### UI_Tab

- 功能分析：UI 界面类：负责菜单、房间、背包或游戏内交互显示
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`UI_Inven`、`UI_Option`
- 它保存了哪些类型：2 个，`GameObject`、`UnityEvent`
- 字段依据示例：`UI_Inven` -> `tab`: `UI_Tab`；`leftTab`: `UI_Tab`；`UI_Option` -> `tab`: `UI_Tab`

#### UI_Tab2

- 功能分析：UI 界面类：负责菜单、房间、背包或游戏内交互显示
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`GameObject`、`Image`、`Sprite`
- 字段依据示例：-

#### UI_TopMenu

- 功能分析：UI 界面类：负责菜单、房间、背包或游戏内交互显示
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`AudioClip`、`AudioSource`、`Button`、`UI_TopMenu.Frame`
- 字段依据示例：-

#### UICharInfo

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`TextGenerator`
- 它保存了哪些类型：1 个，`Vector2`
- 字段依据示例：`TextGenerator` -> `m_Characters`: `List<UICharInfo>`

#### UIFoldout

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：6 个，`DebugUIHandlerBitField`、`DebugUIHandlerColor`、`DebugUIHandlerFoldout`、`DebugUIHandlerVector2`、`DebugUIHandlerVector3`、`DebugUIHandlerVector4`
- 它保存了哪些类型：1 个，`GameObject`
- 字段依据示例：`DebugUIHandlerBitField` -> `valueToggle`: `UIFoldout`；`DebugUIHandlerColor` -> `valueToggle`: `UIFoldout`；`DebugUIHandlerFoldout` -> `valueToggle`: `UIFoldout`；`DebugUIHandlerVector2` -> `valueToggle`: `UIFoldout`；`DebugUIHandlerVector3` -> `valueToggle`: `UIFoldout`；另有 1 个来源

#### UIVertex

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：4 个，`InputField`、`Text`、`TextGenerator`、`UIVertex`
- 它保存了哪些类型：4 个，`Color32`、`UIVertex`、`Vector3`、`Vector4`
- 字段依据示例：`InputField` -> `m_CursorVerts`: `UIVertex[]`；`Text` -> `m_TempVerts`: `UIVertex[]`；`TextGenerator` -> `m_Verts`: `List<UIVertex>`；`UIVertex` -> `simpleVert`: `UIVertex`

#### UniversalAdditionalCameraData

- 功能分析：相机/镜头控制类型：用于虚拟相机、镜头混合、视角参数或相机状态
- 建议价值：中。偏表现、UI、相机或资源组织，适合在确认功能需求后继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`UniversalAdditionalCameraData`
- 它保存了哪些类型：10 个，`AntialiasingMode`、`AntialiasingQuality`、`Camera`、`CameraOverrideOption`、`CameraRenderType`、`LayerMask`、`Transform`、`UniversalAdditionalCameraData` 等 10 个
- 字段依据示例：`UniversalAdditionalCameraData` -> `s_DefaultAdditionalCameraData`: `UniversalAdditionalCameraData`

#### UniversalRenderPipeline

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`Camera`、`Comparison`、`Vector4`、`XRDisplaySubsystem`、`XRSystem`
- 字段依据示例：-

#### UniversalRenderPipelineAsset

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：17 个，`ColorGradingMode`、`Downsampling`、`LightRenderingMode`、`MsaaQuality`、`PipelineDebugLevel`、`RendererType`、`ScriptableRenderer`、`ScriptableRendererData` 等 17 个
- 字段依据示例：-

#### UniversalRenderPipelineEditorResources.MaterialResources

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`UniversalRenderPipelineEditorResources`
- 它保存了哪些类型：1 个，`Material`
- 字段依据示例：`UniversalRenderPipelineEditorResources` -> `materials`: `UniversalRenderPipelineEditorResources.MaterialResources`

#### UpdateTracker

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Transform`、`UpdateTracker.UpdateStatus`
- 字段依据示例：-

#### Vector4

- 功能分析：空间数据类型：保存位置、方向、旋转、速度或坐标信息
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：26 个，`AdditionalLightsShadowCasterPass`、`CinemachineFreeLook`、`CombineInstance`、`ForwardLights`、`Graphic`、`Light2DBlendStyle.MaskChannelFilter`、`MainLightShadowCasterPass`、`MeshSubsetCombineUtility.MeshInstance` 等 26 个
- 它保存了哪些类型：1 个，`Vector4`
- 字段依据示例：`AdditionalLightsShadowCasterPass` -> `m_AdditionalLightsShadowParams`: `Vector4[]`；`CinemachineFreeLook` -> `m_CachedKnots`: `Vector4[]`；`m_CachedCtrl1`: `Vector4[]`；`m_CachedCtrl2`: `Vector4[]`；`CombineInstance` -> `m_LightmapScaleOffset`: `Vector4`；`m_RealtimeLightmapScaleOffset`: `Vector4`；`ForwardLights` -> `m_AdditionalLightPositions`: `Vector4[]`；`m_AdditionalLightColors`: `Vector4[]`；`m_AdditionalLightAttenuations`: `Vector4[]`；`Graphic` -> `m_RaycastPadding`: `Vector4`；另有 21 个来源

#### VertexHelper

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Graphic`
- 它保存了哪些类型：3 个，`Color32`、`Vector3`、`Vector4`
- 字段依据示例：`Graphic` -> `s_VertexHelper`: `VertexHelper`

#### VFXAudioSpectrumBinder

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：6 个，`AudioSource`、`Color`、`ExposedProperty`、`FFTWindow`、`Texture2D`、`VFXAudioSpectrumBinder.AudioSourceMode`
- 字段依据示例：-

#### VFXEnabledBinder

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`ExposedProperty`、`GameObject`、`VFXEnabledBinder.Check`
- 字段依据示例：-

#### VFXHierarchyAttributeMapBinder

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：5 个，`ExposedProperty`、`Texture2D`、`Transform`、`VFXHierarchyAttributeMapBinder.Bone`、`VFXHierarchyAttributeMapBinder.RadiusMode`
- 字段依据示例：-

#### VFXHierarchyAttributeMapBinder.Bone

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`VFXHierarchyAttributeMapBinder`
- 它保存了哪些类型：1 个，`Transform`
- 字段依据示例：`VFXHierarchyAttributeMapBinder` -> `bones`: `List<VFXHierarchyAttributeMapBinder.Bone>`

#### VFXInputMouseBinder

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`Camera`、`ExposedProperty`、`Vector3`
- 字段依据示例：-

#### VFXInputTouchBinder

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`Camera`、`ExposedProperty`、`Vector3`
- 字段依据示例：-

#### VFXMultiplePositionBinder

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`ExposedProperty`、`GameObject`、`Texture2D`
- 字段依据示例：-

#### VFXPlaneBinder

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`ExposedProperty`、`Transform`
- 字段依据示例：-

#### VFXPositionBinder

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`ExposedProperty`、`Transform`
- 字段依据示例：-

#### VFXPreviousPositionBinder

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`ExposedProperty`、`Transform`、`Vector3`
- 字段依据示例：-

#### VFXRaycastBinder

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：6 个，`ExposedProperty`、`GameObject`、`LayerMask`、`RaycastHit`、`VFXRaycastBinder.Space`、`Vector3`
- 字段依据示例：-

#### VFXTransformBinder

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`ExposedProperty`、`Transform`
- 字段依据示例：-

#### VFXVelocityBinder

- 功能分析：视觉特效类型：用于粒子、屏幕特效、技能表现或受击反馈
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`ExposedProperty`、`Transform`、`Vector3`
- 字段依据示例：-

#### VisibleLight

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`CullingAllocationInfo`、`LightData`
- 它保存了哪些类型：5 个，`Color`、`LightType`、`Matrix4x4`、`Rect`、`VisibleLightFlags`
- 字段依据示例：`CullingAllocationInfo` -> `visibleLightsPtr`: `VisibleLight*`；`visibleOffscreenVertexLightsPtr`: `VisibleLight*`；`LightData` -> `visibleLights`: `NativeArray<VisibleLight>`

#### VisibleReflectionProbe

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`CullingAllocationInfo`
- 它保存了哪些类型：4 个，`Bounds`、`Matrix4x4`、`Vector3`、`Vector4`
- 字段依据示例：`CullingAllocationInfo` -> `visibleReflectionProbesPtr`: `VisibleReflectionProbe*`

#### Volume

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`CinemachineVolumeSettings`、`VolumeManager`
- 它保存了哪些类型：1 个，`VolumeProfile`
- 字段依据示例：`CinemachineVolumeSettings` -> `sVolumes`: `List<Volume>`；`VolumeManager` -> `m_SortedVolumes`: `Dictionary<int, List<Volume>>`；`m_Volumes`: `List<Volume>`

#### VolumeComponent

- 功能分析：渲染/光照类型：用于渲染管线、光照、材质、后处理或屏幕效果
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：3 个，`VolumeManager`、`VolumeProfile`、`VolumeStack`
- 它保存了哪些类型：2 个，`ReadOnlyCollection`、`VolumeParameter`
- 字段依据示例：`VolumeManager` -> `m_ComponentsDefaultState`: `List<VolumeComponent>`；`VolumeProfile` -> `components`: `List<VolumeComponent>`；`VolumeStack` -> `components`: `Dictionary<Type, VolumeComponent>`

#### VoxelArea

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`Voxelize`
- 它保存了哪些类型：4 个，`CompactVoxelCell`、`CompactVoxelSpan`、`LinkedVoxelSpan`、`Vector3`
- 字段依据示例：`Voxelize` -> `voxelArea`: `VoxelArea`

#### Voxelize

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`RecastGraph`
- 它保存了哪些类型：7 个，`Bounds`、`GraphTransform`、`RasterizationMesh`、`RecastGraph.RelevantGraphSurfaceMode`、`Vector3`、`VoxelArea`、`VoxelContourSet`
- 字段依据示例：`RecastGraph` -> `globalVox`: `Voxelize`

#### VRIK.References

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`VRIK`
- 它保存了哪些类型：1 个，`Transform`
- 字段依据示例：`VRIK` -> `references`: `VRIK.References`

#### VRIKCalibrator.CalibrationData

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`VRIKCalibrator.CalibrationData`
- 它保存了哪些类型：3 个，`Target`、`VRIKCalibrator.CalibrationData`、`Vector3`
- 字段依据示例：`VRIKCalibrator.CalibrationData` -> `head`: `VRIKCalibrator.CalibrationData.Target`；`leftHand`: `VRIKCalibrator.CalibrationData.Target`；`rightHand`: `VRIKCalibrator.CalibrationData.Target`

#### VRIKCalibrator.CalibrationData.Target

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Quaternion`、`Vector3`
- 字段依据示例：-

#### VRIKCalibrator.Settings

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`Vector3`
- 字段依据示例：-

#### VRIKLODController

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Renderer`、`VRIK`
- 字段依据示例：-

#### VRIKRootController

- 功能分析：动画/骨骼类型：用于角色动画、IK、布娃娃、状态机或动作桥接
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`Transform`、`VRIK`、`Vector3`
- 字段依据示例：-

#### WaitForFixedUpdate

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`CinemachineBrain`
- 它保存了哪些类型：0 个，-
- 字段依据示例：`CinemachineBrain` -> `mWaitForFixedUpdate`: `WaitForFixedUpdate`

#### WallHackDetector

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`WallHackDetector`
- 它保存了哪些类型：14 个，`Camera`、`CharacterController`、`Color`、`GameObject`、`Material`、`MeshRenderer`、`RaycastHit`、`RenderTexture` 等 14 个
- 字段依据示例：`WallHackDetector` -> `<Instance>k__BackingField`: `WallHackDetector`

#### WD_AsceticHero

- 功能分析：武器数据配置：保存某个具体武器的伤害、弹药、技能或表现参数
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`WPN_AsceticHero`
- 它保存了哪些类型：2 个，`AudioClip`、`GameObject`
- 字段依据示例：`WPN_AsceticHero` -> `realData2`: `WD_AsceticHero`

#### WD_EvilTerminator

- 功能分析：武器数据配置：保存某个具体武器的伤害、弹药、技能或表现参数
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`WPN_EvilTerminator`
- 它保存了哪些类型：2 个，`GameObject`、`MissileData`
- 字段依据示例：`WPN_EvilTerminator` -> `realData2`: `WD_EvilTerminator`

#### WD_GrenadeGun

- 功能分析：武器数据配置：保存某个具体武器的伤害、弹药、技能或表现参数
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：3 个，`CharWpnAnimData`、`MissileData`、`WpnSpriteAsset`
- 字段依据示例：-

#### WD_MasterHero

- 功能分析：武器数据配置：保存某个具体武器的伤害、弹药、技能或表现参数
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`WPN_MasterHero`
- 它保存了哪些类型：1 个，`GameObject`
- 字段依据示例：`WPN_MasterHero` -> `realData2`: `WD_MasterHero`

#### WD_MasterHunter

- 功能分析：武器数据配置：保存某个具体武器的伤害、弹药、技能或表现参数
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`WPN_MasterHunter`
- 它保存了哪些类型：1 个，`GameObject`
- 字段依据示例：`WPN_MasterHunter` -> `realData2`: `WD_MasterHunter`

#### WD_MechanicHero

- 功能分析：武器数据配置：保存某个具体武器的伤害、弹药、技能或表现参数
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`WPN_MechanicHero`
- 它保存了哪些类型：1 个，`GameObject`
- 字段依据示例：`WPN_MechanicHero` -> `realData2`: `WD_MechanicHero`

#### WD_Missile

- 功能分析：武器数据配置：保存某个具体武器的伤害、弹药、技能或表现参数
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`WPN_Throw`
- 它保存了哪些类型：1 个，`MissileData`
- 字段依据示例：`WPN_Throw` -> `realData`: `WD_Missile`

#### WD_RPG

- 功能分析：武器数据配置：保存某个具体武器的伤害、弹药、技能或表现参数
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`WPN_RPG`
- 它保存了哪些类型：1 个，`MissileData`
- 字段依据示例：`WPN_RPG` -> `realData`: `WD_RPG`

#### WD_SentryGun

- 功能分析：武器数据配置：保存某个具体武器的伤害、弹药、技能或表现参数
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`WPN_SentryGun`
- 它保存了哪些类型：2 个，`AudioClip`、`GameObject`
- 字段依据示例：`WPN_SentryGun` -> `realData`: `WD_SentryGun`

#### WD_SkillKnife

- 功能分析：武器数据配置：保存某个具体武器的伤害、弹药、技能或表现参数
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`GameObject`
- 字段依据示例：-

#### WD_VoidTerminator

- 功能分析：武器数据配置：保存某个具体武器的伤害、弹药、技能或表现参数
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：1 个，`GameObject`
- 字段依据示例：-

#### XRLayout

- 功能分析：UI 控件类型：用于界面布局、文本、按钮、滚动、图形或交互控件
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：2 个，`Camera`、`XRSystem`
- 字段依据示例：-

#### XRNodeState

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：0 个，-
- 它保存了哪些类型：4 个，`AvailableTrackingData`、`Quaternion`、`Vector3`、`XRNode`
- 字段依据示例：-

#### XRPass

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`CameraData`、`XRSystem`
- 它保存了哪些类型：9 个，`Material`、`Matrix4x4`、`Mesh`、`ProfilingSampler`、`RenderTargetIdentifier`、`RenderTextureDescriptor`、`ScriptableCullingParameters`、`Vector4` 等 9 个
- 字段依据示例：`CameraData` -> `xr`: `XRPass`；`XRSystem` -> `emptyPass`: `XRPass`；`framePasses`: `List<XRPass>`

#### XRSystem

- 功能分析：项目字段类型：在当前字段关系中作为数据、组件或资源引用出现，具体用途看字段名和保存它的类
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：2 个，`UniversalRenderPipeline`、`XRLayout`
- 它保存了哪些类型：6 个，`Material`、`MaterialPropertyBlock`、`ProfilingSampler`、`RenderTexture`、`XRDisplaySubsystem`、`XRPass`
- 字段依据示例：`UniversalRenderPipeline` -> `m_XRSystem`: `XRSystem`；`XRLayout` -> `xrSystem`: `XRSystem`

#### XRSystemData

- 功能分析：配置/数据类型：保存运行参数、资源引用、显示数据或系统配置
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`ForwardRendererData`
- 它保存了哪些类型：1 个，`XRSystemData.ShaderResources`
- 字段依据示例：`ForwardRendererData` -> `xrSystemData`: `XRSystemData`

#### ZoomAction.ZoomData

- 功能分析：配置/数据类型：保存运行参数、资源引用、显示数据或系统配置
- 建议价值：中。在当前关系图中已出现，建议结合保存它的字段名判断是否继续展开。
- dump.cs 定义：有 class/struct 定义
- 谁保存了这个类：1 个，`ZoomAction`
- 它保存了哪些类型：1 个，`Sprite`
- 字段依据示例：`ZoomAction` -> `datas`: `ZoomAction.ZoomData[]`

### 低优先级

