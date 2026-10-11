(function () {
    'use strict';

    /*
     * UCF1.7 最小可用第三人称射击版 v3.14-owner-perf（稳定水平视角）
     *
     * 只保留：
     * 1. 第三人称 FreeLook 相机；
     * 2. 第三人称人物模型；
     * 3. 相机相对 WASD 移动；
     * 4. 人物水平朝向平滑跟随相机；
     * 5. 最终相机中心射线 -> 场景目标 -> 枪口收敛；
     * 6. 切枪、死亡、复活、出生的必要生命周期恢复。
     *
     * 已完全移除：
     * 动态换肩、V 键、遮挡淡出、AimIK、上半身俯仰、ADS、
     * CinemachineCollider 参数改写及其配置/遥测。
     */

    var FEATURE_ID = 'third_person_camera';
    var MODULE_NAME = 'GameAssembly.dll';
    var module = Process.findModuleByName(MODULE_NAME);

    function sendLog(level, message, extra) {
        var detail = '';

        if (extra !== undefined) {
            try {
                detail = typeof extra === 'string'
                    ? extra
                    : JSON.stringify(extra);
            } catch (_) {
                detail = String(extra);
            }
        }

        var payload = {
            type: 'log',
            level: level,
            module: 'TP-MIN',
            message: message,

            /*
             * P0 诊断修复（2026-10-11）：
             * 整合包的消息管道只认 audience + dev_detail
             * （core/frida_manager.py:239-247），
             * 原来把诊断放在 extra 里会被整包静默丢弃，
             * 所以 [TPSStatus] / Hook 日志一直是裸行。
             * 同时保留 extra，兼容独立版工具。
             */
            audience: 'dev',
            dev_detail: detail
        };

        if (extra !== undefined) payload.extra = extra;
        send(payload);
    }

    function sendPluginEvent(event, payload) {
        send({
            type: 'plugin_event',
            feature: FEATURE_ID,
            event: event,
            payload: payload || {},
            audience: 'dev'
        });
    }

    function sendStatus(feature, enabled) {
        try { send({ type: 'status', feature: feature, enabled: enabled }); } catch (_) {}
    }

    if (module === null) {
        sendLog('error', MODULE_NAME + ' 未加载');
        sendPluginEvent('runtime_error', {
            message: MODULE_NAME + ' 未加载'
        });
        return;
    }

    if (Process.arch !== 'ia32' || Process.pointerSize !== 4) {
        sendLog('error', '只支持 32 位 x86 游戏进程', {
            arch: Process.arch,
            pointerSize: Process.pointerSize
        });
        sendPluginEvent('runtime_error', {
            message: '只支持 32 位 x86 游戏进程',
            arch: Process.arch,
            pointerSize: Process.pointerSize
        });
        return;
    }

    var base = module.base;
    var CALL_CONV = 'mscdecl';
    var PTR_SIZE = 4;

    var RVA = {
        CameraManager_Awake:                   0x00B35550,
        CameraManager_Update:                  0x00B36FA0,
        CameraManager_OnDestroy:               0x00B360E0,
        CameraManager_ChangePVandCV:           0x00B35920,
        CameraManager_SetFreeLookCameraActive: 0x00B36790,

        GameManager_Awake:                     0x00AFA250,
        GameManager_OnDestroy:                 0x00AFB6F0,
        MapManager_NewGameRoundStart:          0x00AEBCB0,

        Player_get_isMyPlayer:                 0x00B55FD0,
        Player_UpdateCameraRotaion:            0x00B54870,
        Player_GetWalkVelocity:                 0x00B54220,
        Player_OnEntityDeath:                  0x00B51210,
        Player_SetWeapon:                      0x00B53650,
        Player_Respawn:                        0x00B527A0,
        Player_Spawn:                          0x00B53760,

        PlayerData_SetObserveMode:             0x00B13AD0,
        Model_OnOwnerObserveModeChange:        0x00B4B300,
        Weapon_SynchronizeHand:                0x00B6DA20,

        CinemachineFreeLook_set_Follow:        0x00439270,
        CinemachineFreeLook_set_LookAt:        0x002E7E10,

        Singleton_GetInstance:                 0x004A8170,
        GameManager_SingletonMethodInfo:       0x00E1CE64,
        CameraManager_SingletonMethodInfo:     0x00E1CD68,

        Brain_PushStateToUnityCamera:          0x0082B750,
        Brain_get_OutputCamera:                0x0082CDB0,


        Component_get_transform:               0x0032CF40,
        Transform_get_position_Injected:       0x003F4280,
        Transform_get_forward_Injected:        0x003F3F20,
        Transform_set_position_Injected:       0x003F4810,
        Transform_set_rotation_Injected:       0x003F4870,

        Physics_get_defaultPhysicsScene_Injected: 0x00ABB6F0,
        PhysicsScene_Internal_Raycast_Injected:    0x00AB8C20,

        Recoil_GetShootRay:                    0x00B195C0
    };

    var OFF = {
        CM_focusPlayer:             0x0C,
        CM_freeLookCamera:          0x10,
        GM_allPlayers:              0x1C,

        Player_cameraRotation:      0x4C,
        Player_recoil:              0x54,
        Player_characterContainer:  0x58,
        Player_currentCharacter:    0x5C,
        Player_playerData:          0x98,
        Player_wpns:                0xA0,

        PD_observeMode:             0x08,
        PD_playerViewModelVisible:  0x24,

        PW_inUse:                   0x18,
        WPN_Gun_gunFire:            0x114,

        CFL_m_LookAt:               0x40,
        CFL_m_Follow:               0x44,
        CFL_m_YAxis:                0x88,

        AX_Value:                   0x00,
        AX_MaxSpeed:                0x08,
        AX_InputAxisName:           0x14,
        AX_InputAxisValue:          0x18,
        AX_InvertInput:             0x1C,
        AX_MinValue:                0x20,
        AX_MaxValue:                0x24,
        AX_Wrap:                    0x28,
        AX_InputProvider:           0x54
    };

    /*
     * v3.7 配置只保留 4 项：
     * 固定居中、镜头距离、上背部枢轴高度、鼠标反转。
     *
     * ScreenY、FOV 和俯仰倍率不再读取或写入，
     * 避免与游戏自身实时相机状态互相争夺。
     */
    var config = {
        shoulder: 'center',
        distance: 3.0,
        pivotHeight: 1.35,
        invertY: false
    };

    var LIMITS = {
        maxAimDistance: 1000.0,
        cameraCacheMaxAgeMs: 250,

        /*
         * 成熟 TPS：同一个最终相机帧只计算一次瞄准目标。
         * 不跨时间复用，不使用 50ms/角度/距离的猜测缓存。
         */
        lifecycleWeaponDelayMs: 140,
        lifecycleSpawnDelayMs: 180,
        lifecycleCameraDelayMs: 80,

        bodyYawIntervalMs: 33,
        bodyYawFollowSpeed: 12.0,

        /*
         * 不再每个相机帧做内存页可读性检查。
         * 缓存指针改为低频健康检查。
         */
        cameraCacheHealthCheckMs: 1000,

        statusLogIntervalMs: 20000,

        /*
         * P0 诊断：性能采样日志间隔。
         * 测试期 5 秒一条；定完因后设为 0 即可关闭 [TPSPerf]。
         */
        perfLogIntervalMs: 5000,

        maxCameraPitchDegrees: 75.0,
        cameraPitchFollowSpeed: 20.0,
        maxCameraPitchStepDegrees: 10.0
    };

    var STATE = {
        NO_GAME: 'NO_GAME',
        READY: 'READY',
        ENABLED: 'ENABLED'
    };

    var state = STATE.NO_GAME;
    var installed = false;
    var enabled = false;
    var sessionDestroyed = false;

    var gameManager = null;
    var cameraManager = null;
    var localPlayer = null;
    var listeners = [];

    var pendingEnable = false;
    var pendingDisable = false;
    var commandBusy = false;

    /*
     * 生命周期事件合并队列：
     * set_weapon / respawn / spawn 等短时间连续触发时，
     * 只在主线程执行一次模型、相机和枪口刷新。
     */
    var refreshQueue = {
        pending: false,
        dueAt: 0,
        model: false,
        camera: false,
        muzzle: false,
        eventCount: 0,
        lastReason: 'none'
    };

    var runtime = {
        playerDead: false,

        camera: {
            valid: false,
            camera: null,
            transform: null,
            characterContainer: null,
            position: { x: 0.0, y: 0.0, z: 0.0 },
            forward: { x: 0.0, y: 0.0, z: 1.0 },
            yaw: 0.0,
            pitch: 0.0,
            frameId: 0,
            lastWriteTime: 0,
            lastHealthCheckTime: 0
        },

        cameraInput: {
            valid: false,
            rawYaw: 0.0,
            pitch: 0.0,
            lastSampleTime: 0
        },

        cameraPivot: {
            initialized: false,
            smoothedPitch: 0.0,
            lastWriteTime: 0
        },

        movement: {
            initialized: false,
            smoothYaw: 0.0,
            lastYawUpdateTime: 0
        },

        muzzle: {
            valid: false,
            weapon: null,
            transform: null,
            source: 'none'
        },

        shootRay: {
            valid: false,
            origin: { x: 0.0, y: 0.0, z: 0.0 },
            direction: { x: 0.0, y: 0.0, z: 1.0 },
            targetPoint: { x: 0.0, y: 0.0, z: 0.0 },
            aimSource: 'camera_center'
        },

        /*
         * 成熟 TPS 的单帧瞄准方案：
         * 同一 Camera frame 内如果 GetShootRay 被调用多次，
         * 复用同一个目标；进入下一相机帧立即重新计算。
         */
        aimSolution: {
            valid: false,
            frameId: -1,
            targetX: 0.0,
            targetY: 0.0,
            targetZ: 0.0,
            reusedLast: false
        },

        physicsDisabled: false,
        physicsFailures: 0,
        lastStatusLogTime: 0
    };

    var stats = {
        cameraFrames: 0,
        cameraFailures: 0,
        pitchInputSamples: 0,

        yawNativeReads: 0,

        movementCalls: 0,
        movementVectorsModified: 0,
        movementYawUpdates: 0,

        physicsRaycastCalls: 0,
        shootRayCalls: 0,
        shootRayModified: 0,
        shootRayFailures: 0,
        aimFramesComputed: 0,
        sameFrameAimReuses: 0,

        muzzleResolves: 0,
        muzzleFailures: 0,
        muzzleOwnerChecks: 0,
        muzzleOwnerMismatches: 0,

        safeRestoreSkips: 0,
        safeRestoreRebinds: 0,
        stalePointerSkips: 0,
        staleCameraResets: 0,
        staleMuzzleInvalidations: 0,
        cameraCacheHealthChecks: 0,
        hotPathReadableChecksRemoved: true,

        lifecycleEvents: 0,
        lifecycleBatches: 0,
        lifecycleEventsMerged: 0,

        inputFailures: 0,
        errors: 0
    };

    /*
     * ========== P0 诊断：只观测，不改任何相机行为 ==========
     *
     * 目的：把“第三人称卡顿”从猜测变成数字。
     *
     * 1) 微秒级时钟：优先 QueryPerformanceCounter；
     *    解析不到时降级 Date.now（毫秒级，日志 clock 字段会标明）。
     * 2) 统计每个热路径回调的 calls / avg / p99 / max（微秒）。
     * 3) 统计 CameraManager.Update 相邻两次之间
     *    PushStateToUnityCamera 被调了几次：
     *    pushPerUpdateFrameMax >= 2 就说明“游戏一帧刷新了多次相机”。
     *
     * 采样本身有约 0.2~1us 开销，读数会略偏大，
     * 但足够区分“几十微秒”和“几百微秒”。
     *
     * 说明：avg / max 覆盖整个统计窗口（默认 5 秒）；
     *      p99 只覆盖最近 128 个样本（环形缓冲，
     *      避免热路径里分配内存）。
     */
    var PERF_SAMPLES = 128;

    function makePerfMetric() {
        var samples = new Array(PERF_SAMPLES);

        for (var sampleIndex = 0;
             sampleIndex < PERF_SAMPLES;
             sampleIndex++) {
            samples[sampleIndex] = 0.0;
        }

        return {
            count: 0,
            totalUs: 0.0,
            maxUs: 0.0,
            cursor: 0,
            filled: 0,
            samples: samples
        };
    }

    function resetPerfMetric(metric) {
        metric.count = 0;
        metric.totalUs = 0.0;
        metric.maxUs = 0.0;
        metric.cursor = 0;
        metric.filled = 0;

        for (var sampleIndex = 0;
             sampleIndex < PERF_SAMPLES;
             sampleIndex++) {
            metric.samples[sampleIndex] = 0.0;
        }
    }

    function recordPerfMetric(metric, elapsedUs) {
        metric.count++;
        metric.totalUs += elapsedUs;

        if (elapsedUs > metric.maxUs) {
            metric.maxUs = elapsedUs;
        }

        metric.samples[metric.cursor] = elapsedUs;
        metric.cursor++;

        if (metric.cursor >= PERF_SAMPLES) {
            metric.cursor = 0;
        }

        if (metric.filled < PERF_SAMPLES) {
            metric.filled++;
        }
    }

    function summarizePerfMetric(metric) {
        if (metric.count === 0) {
            return {
                calls: 0,
                avgUs: 0.0,
                p99Us: 0.0,
                maxUs: 0.0
            };
        }

        var sorted = metric.samples.slice(
            0,
            metric.filled
        );

        sorted.sort(function (left, right) {
            return left - right;
        });

        var p99Index = sorted.length - 1;

        if (sorted.length > 1) {
            p99Index = Math.floor(
                (sorted.length - 1) * 0.99
            );
        }

        return {
            calls: metric.count,
            avgUs: Math.round(
                metric.totalUs / metric.count * 10.0
            ) / 10.0,
            p99Us: Math.round(
                sorted[p99Index] * 10.0
            ) / 10.0,
            maxUs: Math.round(
                metric.maxUs * 10.0
            ) / 10.0
        };
    }

    function resolveProcExport(moduleNames, exportName) {
        try {
            if (typeof Module.getGlobalExportByName ===
                'function') {
                var global = Module.getGlobalExportByName(
                    exportName
                );

                if (!isNull(global)) return global;
            }
        } catch (_) {
        }

        try {
            if (typeof Module.findGlobalExportByName ===
                'function') {
                var found = Module.findGlobalExportByName(
                    exportName
                );

                if (!isNull(found)) return found;
            }
        } catch (_) {
        }

        for (var index = 0;
             index < moduleNames.length;
             index++) {
            try {
                if (typeof Module.getExportByName ===
                    'function') {
                    return Module.getExportByName(
                        moduleNames[index],
                        exportName
                    );
                }
            } catch (_) {
            }

            try {
                if (typeof Module.findExportByName ===
                    'function') {
                    return Module.findExportByName(
                        moduleNames[index],
                        exportName
                    );
                }
            } catch (_) {
            }

            try {
                var owner = Process.findModuleByName(
                    moduleNames[index]
                );

                if (owner &&
                    typeof owner.getExportByName ===
                        'function') {
                    return owner.getExportByName(exportName);
                }

                if (owner &&
                    typeof owner.findExportByName ===
                        'function') {
                    return owner.findExportByName(exportName);
                }
            } catch (_) {
            }
        }

        return null;
    }

    function makeWinApiProbe(address) {
        try {
            return new NativeFunction(
                address,
                'int',
                ['pointer'],
                'stdcall'
            );
        } catch (_) {
        }

        try {
            return new NativeFunction(
                address,
                'int',
                ['pointer']
            );
        } catch (_) {
            return null;
        }
    }

    var perfClock = (function () {
        try {
            if (typeof performance !== 'undefined' &&
                performance !== null &&
                typeof performance.now === 'function') {
                return {
                    name: 'performance.now',
                    now: function () {
                        return performance.now() * 1000.0;
                    }
                };
            }
        } catch (_) {
        }

        try {
            var counterBuffer = Memory.alloc(8);
            var frequencyBuffer = Memory.alloc(8);
            var systemModules = [
                'kernel32.dll',
                'KernelBase.dll',
                'ntdll.dll'
            ];

            var counterAddress = resolveProcExport(
                systemModules,
                'QueryPerformanceCounter'
            );

            var frequencyAddress = resolveProcExport(
                systemModules,
                'QueryPerformanceFrequency'
            );

            if (!isNull(counterAddress) &&
                !isNull(frequencyAddress)) {
                var queryCounter = makeWinApiProbe(
                    counterAddress
                );
                var queryFrequency = makeWinApiProbe(
                    frequencyAddress
                );

                if (queryCounter !== null &&
                    queryFrequency !== null) {
                    queryFrequency(frequencyBuffer);

                    var frequency =
                        frequencyBuffer.readU32() +
                        frequencyBuffer.add(4).readU32() *
                        4294967296.0;

                    if (frequency > 0.0) {
                        var toMicros =
                            1000000.0 / frequency;

                        return {
                            name: 'qpc',
                            now: function () {
                                queryCounter(counterBuffer);

                                return (
                                    counterBuffer.readU32() +
                                    counterBuffer.add(4)
                                        .readU32() *
                                        4294967296.0
                                ) * toMicros;
                            }
                        };
                    }
                }
            }
        } catch (_) {
        }

        return {
            name: 'date_now_ms',
            now: function () {
                return Date.now() * 1000.0;
            }
        };
    })();

    var perf = {
        clock: perfClock.name,

        frames: 0,
        pushStateCalls: 0,
        pushStreak: 0,
        pushPerUpdateFrameMax: 0,

        windowFrames: 0,
        windowPushStateCalls: 0,
        windowPushPerUpdateFrameMax: 0,

        windowFrameGapTotalMs: 0.0,
        windowFrameGapMaxMs: 0.0,
        windowFrameGapSamples: 0,
        lastFrameTimeMs: 0,
        lastLogTime: 0,

        metrics: {
            cmUpdate: makePerfMetric(),
            finalCamera: makePerfMetric(),
            healthCheck: makePerfMetric(),
            cameraInput: makePerfMetric(),
            walkVelocity: makePerfMetric()
        }
    };

    function resetPerfWindow() {
        perf.windowFrames = 0;
        perf.windowPushStateCalls = 0;
        perf.windowPushPerUpdateFrameMax = 0;

        perf.windowFrameGapTotalMs = 0.0;
        perf.windowFrameGapMaxMs = 0.0;
        perf.windowFrameGapSamples = 0;

        resetPerfMetric(perf.metrics.cmUpdate);
        resetPerfMetric(perf.metrics.finalCamera);
        resetPerfMetric(perf.metrics.healthCheck);
        resetPerfMetric(perf.metrics.cameraInput);
        resetPerfMetric(perf.metrics.walkVelocity);

        readableProbe.windowCalls = 0;
        readableProbe.windowTotalUs = 0.0;
        readableProbe.windowMaxUs = 0.0;
        readableProbe.slowSites = {};
        readableProbe.slowSiteKeys = [];
    }

    function resetPerf() {
        perf.frames = 0;
        perf.pushStateCalls = 0;
        perf.pushStreak = 0;
        perf.pushPerUpdateFrameMax = 0;
        perf.lastFrameTimeMs = 0;
        perf.lastLogTime = 0;

        readableProbe.calls = 0;
        readableProbe.totalUs = 0.0;
        readableProbe.maxUs = 0.0;

        resetPerfWindow();
    }

    /*
     * 每经过一次 CameraManager.Update 记一个“游戏帧”，
     * 并用两次之间的间隔估算帧时间（只用于观察）。
     */
    function noteGameFrame() {
        var now = Date.now();

        if (perf.lastFrameTimeMs > 0) {
            var gapMs = now - perf.lastFrameTimeMs;

            if (gapMs >= 0 && gapMs < 2000) {
                perf.windowFrameGapTotalMs += gapMs;
                perf.windowFrameGapSamples++;

                if (gapMs > perf.windowFrameGapMaxMs) {
                    perf.windowFrameGapMaxMs = gapMs;
                }
            }
        }

        perf.lastFrameTimeMs = now;
        perf.frames++;
        perf.windowFrames++;

        if (perf.pushStreak >
            perf.windowPushPerUpdateFrameMax) {
            perf.windowPushPerUpdateFrameMax =
                perf.pushStreak;
        }

        if (perf.pushStreak >
            perf.pushPerUpdateFrameMax) {
            perf.pushPerUpdateFrameMax =
                perf.pushStreak;
        }

        perf.pushStreak = 0;
    }

    function emitPerfStatus() {
        if (!enabled) return;

        if (LIMITS.perfLogIntervalMs <= 0) return;

        var now = Date.now();

        if (now - perf.lastLogTime <
            LIMITS.perfLogIntervalMs) {
            return;
        }

        perf.lastLogTime = now;

        var gapAvgMs = perf.windowFrameGapSamples > 0
            ? Math.round(
                perf.windowFrameGapTotalMs /
                perf.windowFrameGapSamples * 100.0
            ) / 100.0
            : 0.0;

        var pushPerFrameAvg = perf.windowFrames > 0
            ? Math.round(
                perf.windowPushStateCalls /
                perf.windowFrames * 100.0
            ) / 100.0
            : 0.0;

        sendLog('info', '[TPSPerf]', {
            clock: perf.clock,

            frames: perf.windowFrames,
            pushStateCalls: perf.windowPushStateCalls,
            pushPerFrameAvg: pushPerFrameAvg,
            pushPerUpdateFrameMax:
                perf.windowPushPerUpdateFrameMax,
            pushPerUpdateFrameMaxTotal:
                perf.pushPerUpdateFrameMax,

            frameGapAvgMs: gapAvgMs,
            frameGapMaxMs: perf.windowFrameGapMaxMs,

            camWrites: stats.cameraFrames,
            camFails: stats.cameraFailures,

            finalCameraUs: summarizePerfMetric(
                perf.metrics.finalCamera
            ),
            healthCheckUs: summarizePerfMetric(
                perf.metrics.healthCheck
            ),
            isReadableUs: {
                calls: readableProbe.windowCalls,
                totalUs: Math.round(
                    readableProbe.windowTotalUs * 10.0
                ) / 10.0,
                maxUs: Math.round(
                    readableProbe.windowMaxUs * 10.0
                ) / 10.0,
                maxUsTotal: Math.round(
                    readableProbe.maxUs * 10.0
                ) / 10.0
            },
            isReadableSlowSites: summarizeReadableSites(),
            cmUpdateUs: summarizePerfMetric(
                perf.metrics.cmUpdate
            ),
            cameraInputUs: summarizePerfMetric(
                perf.metrics.cameraInput
            ),
            walkVelocityUs: summarizePerfMetric(
                perf.metrics.walkVelocity
            )
        });

        resetPerfWindow();
    }

    var saved = {
        cameraCaptured: false,
        modelCaptured: false,

        freeLook: null,
        originalFollow: null,
        originalLookAt: null,

        yAxisCaptured: false,
        yAxisInputName: null,
        yAxisInputProvider: null,
        yAxisInputValue: 0.0,
        yAxisInvert: false,
        yAxisMaxSpeed: 0.0,
        yAxisMinValue: 0.0,
        yAxisMaxValue: 1.0,
        yAxisWrap: false,
        yAxisValue: 0.5,

        playerData: null,
        character: null,
        weapon: null,
        observeMode: 0,
        playerViewModelVisible: true
    };

    var positionBuffer = Memory.alloc(12);
    var forwardBuffer = Memory.alloc(12);
    var cameraWritePositionBuffer = Memory.alloc(12);
    var cameraWriteRotationBuffer = Memory.alloc(16);

    var physicsSceneBuffer = Memory.alloc(4);
    var rayBuffer = Memory.alloc(24);
    var raycastHitBuffer = Memory.alloc(0x2C);

    var tempRawForward = { x: 0.0, y: 0.0, z: 1.0 };
    var tempCharacterPosition = { x: 0.0, y: 0.0, z: 0.0 };
    var tempMuzzlePosition = { x: 0.0, y: 0.0, z: 0.0 };

    function isNull(pointer) {
        if (pointer === null || pointer === undefined) return true;
        try {
            return pointer.isNull();
        } catch (_) {
            return true;
        }
    }

    // P1：UnityEngine.Object 活体校验（m_CachedPtr 在 +0x8，为 0 表示 native 对象已销毁）
    function isAliveUnityObject(pointer) {
        try {
            if (isNull(pointer)) return false;
            var cached = pointer.add(0x8).readPointer();
            return !!(cached && !cached.isNull());
        } catch (_) {
            return false;
        }
    }


    function invalidateAimSolution() {
        runtime.aimSolution.valid = false;
        runtime.aimSolution.frameId = -1;
        runtime.aimSolution.reusedLast = false;
    }

    function readTransformPositionInto(transform, output) {
        /*
         * 热路径优化：Transform 读取前只做 null 判断。
         * 旧指针由低频健康检查和生命周期清理负责。
         */
        if (isNull(transform)) {
            return false;
        }

        try {
            transformGetPosition(
                transform,
                positionBuffer,
                ptr(0)
            );

            var x = positionBuffer.readFloat();
            var y = positionBuffer.add(4).readFloat();
            var z = positionBuffer.add(8).readFloat();

            if (!isFinite(x) ||
                !isFinite(y) ||
                !isFinite(z)) {
                return false;
            }

            output.x = x;
            output.y = y;
            output.z = z;
            return true;
        } catch (_) {
            return false;
        }
    }

    function readTransformForwardInto(transform, output) {
        /*
         * 热路径优化：Transform 读取前只做 null 判断。
         */
        if (isNull(transform)) {
            return false;
        }

        try {
            transformGetForward(
                forwardBuffer,
                transform,
                ptr(0)
            );

            var x = forwardBuffer.readFloat();
            var y = forwardBuffer.add(4).readFloat();
            var z = forwardBuffer.add(8).readFloat();

            var length = Math.sqrt(
                x * x +
                y * y +
                z * z
            );

            if (!isFinite(length) ||
                length < 0.00001) {
                return false;
            }

            var inv = 1.0 / length;
            output.x = x * inv;
            output.y = y * inv;
            output.z = z * inv;
            return true;
        } catch (_) {
            return false;
        }
    }

    /*
     * P0 诊断：累计 isReadable 的调用次数与耗时；
     * 出现慢调用时记录调用栈，用于归因。
     */
    var readableProbe = {
        calls: 0,
        totalUs: 0.0,
        maxUs: 0.0,
        windowCalls: 0,
        windowTotalUs: 0.0,
        windowMaxUs: 0.0,
        slowSites: {},
        slowSiteKeys: []
    };

    var READABLE_SLOW_THRESHOLD_US = 2000.0;

    function noteReadableSlowSite() {
        var key = 'unknown';

        try {
            var stack = new Error().stack;

            if (stack) {
                var lines = String(stack).split('\n');
                var picked = [];

                for (var index = 0;
                     index < lines.length &&
                     picked.length < 3;
                     index++) {
                    var frame = lines[index].trim();

                    if (frame.length === 0 ||
                        frame.indexOf('noteReadableSlowSite') !== -1 ||
                        frame.indexOf('isReadable') !== -1) {
                        continue;
                    }

                    picked.push(frame);
                }

                if (picked.length > 0) {
                    key = picked.join(' <- ').slice(0, 200);
                }
            }
        } catch (_) {
        }

        if (readableProbe.slowSites[key] === undefined) {
            if (readableProbe.slowSiteKeys.length >= 6) {
                return;
            }

            readableProbe.slowSites[key] = 0;
            readableProbe.slowSiteKeys.push(key);
        }

        readableProbe.slowSites[key]++;
    }

    function summarizeReadableSites() {
        var output = [];

        for (var index = 0;
             index < readableProbe.slowSiteKeys.length;
             index++) {
            var key = readableProbe.slowSiteKeys[index];

            output.push(
                readableProbe.slowSites[key] + 'x ' + key
            );
        }

        return output;
    }

    /*
     * P0 修复（根因）：
     * 原先用 Process.findRangeByAddress 判断地址可读性，
     * 它在 Windows 上会枚举整个地址空间，
     * 实测单次 7~13ms，是每秒/每发枪卡顿的根因。
     *
     * 改为受保护的单字节读取：
     *   地址可读     -> 读成功 -> true；
     *   未映射/不可读/仅执行 -> 抛异常 -> false。
     * Windows 上 Frida 用 ReadProcessMemory 实现读取，
     * 非法地址只会失败，不会让进程崩溃。
     * 单次约 1us，与“存在可读内存段”语义等价。
     */
    function isReadable(pointer) {
        if (isNull(pointer)) return false;

        var probeStart = perfClock.now();
        var readable = false;

        try {
            pointer.readU8();
            readable = true;
        } catch (_) {
            readable = false;
        }

        var probeUs = perfClock.now() - probeStart;

        readableProbe.calls++;
        readableProbe.totalUs += probeUs;
        readableProbe.windowCalls++;
        readableProbe.windowTotalUs += probeUs;

        if (probeUs > readableProbe.maxUs) {
            readableProbe.maxUs = probeUs;
        }

        if (probeUs > readableProbe.windowMaxUs) {
            readableProbe.windowMaxUs = probeUs;
        }

        if (probeUs >= READABLE_SLOW_THRESHOLD_US) {
            noteReadableSlowSite();
        }

        return readable;
    }

    function isExecutable(address) {
        try {
            var range = Process.findRangeByAddress(address);
            return range !== null &&
                range.protection.indexOf('x') !== -1;
        } catch (_) {
            return false;
        }
    }

    function guarded(label, callback, fallback) {
        try {
            return callback();
        } catch (error) {
            stats.errors++;
            sendLog('error', label + ': ' + error);
            return fallback;
        }
    }

    function setState(nextState) {
        if (state === nextState) return;
        var previous = state;
        state = nextState;
        sendLog('info', '状态: ' + previous + ' -> ' + nextState);
        sendPluginEvent('state_changed', {
            oldState: previous,
            newState: nextState
        });
    }

    var isMyPlayer = new NativeFunction(
        base.add(RVA.Player_get_isMyPlayer),
        'bool',
        ['pointer', 'pointer'],
        CALL_CONV
    );

    var singletonGetInstance = new NativeFunction(
        base.add(RVA.Singleton_GetInstance),
        'pointer',
        ['pointer'],
        CALL_CONV
    );

    var setFreeLookActive = new NativeFunction(
        base.add(RVA.CameraManager_SetFreeLookCameraActive),
        'void',
        ['pointer', 'bool', 'pointer'],
        CALL_CONV
    );

    var setObserveMode = new NativeFunction(
        base.add(RVA.PlayerData_SetObserveMode),
        'void',
        ['pointer', 'int', 'pointer'],
        CALL_CONV
    );

    var onOwnerObserveModeChange = new NativeFunction(
        base.add(RVA.Model_OnOwnerObserveModeChange),
        'void',
        ['pointer', 'int', 'pointer'],
        CALL_CONV
    );

    var synchronizeHand = new NativeFunction(
        base.add(RVA.Weapon_SynchronizeHand),
        'void',
        ['pointer', 'pointer'],
        CALL_CONV
    );

    var setFollow = new NativeFunction(
        base.add(RVA.CinemachineFreeLook_set_Follow),
        'void',
        ['pointer', 'pointer', 'pointer'],
        CALL_CONV
    );

    var setLookAt = new NativeFunction(
        base.add(RVA.CinemachineFreeLook_set_LookAt),
        'void',
        ['pointer', 'pointer', 'pointer'],
        CALL_CONV
    );

    var brainGetOutputCamera = new NativeFunction(
        base.add(RVA.Brain_get_OutputCamera),
        'pointer',
        ['pointer', 'pointer'],
        CALL_CONV
    );

    var componentGetTransform = new NativeFunction(
        base.add(RVA.Component_get_transform),
        'pointer',
        ['pointer', 'pointer'],
        CALL_CONV
    );

    var transformGetPosition = new NativeFunction(
        base.add(RVA.Transform_get_position_Injected),
        'void',
        ['pointer', 'pointer', 'pointer'],
        CALL_CONV
    );

    /*
     * 本游戏版本的 Transform.get_forward_Injected 包装函数调用顺序
     * 已通过 v3.x 运行日志验证为：返回缓冲区、Transform、MethodInfo。
     */
    var transformGetForward = new NativeFunction(
        base.add(RVA.Transform_get_forward_Injected),
        'void',
        ['pointer', 'pointer', 'pointer'],
        CALL_CONV
    );

    var transformSetPosition = new NativeFunction(
        base.add(RVA.Transform_set_position_Injected),
        'void',
        ['pointer', 'pointer', 'pointer'],
        CALL_CONV
    );

    var transformSetRotation = new NativeFunction(
        base.add(RVA.Transform_set_rotation_Injected),
        'void',
        ['pointer', 'pointer', 'pointer'],
        CALL_CONV
    );

    var physicsGetDefaultSceneInjected = new NativeFunction(
        base.add(RVA.Physics_get_defaultPhysicsScene_Injected),
        'void',
        ['pointer', 'pointer'],
        CALL_CONV
    );

    var physicsInternalRaycastInjected = new NativeFunction(
        base.add(RVA.PhysicsScene_Internal_Raycast_Injected),
        'bool',
        [
            'pointer',
            'pointer',
            'float',
            'pointer',
            'int',
            'int',
            'pointer'
        ],
        CALL_CONV
    );

    function normalizeAngle(angle) {
        var value = angle % 360.0;
        if (value > 180.0) value -= 360.0;
        if (value < -180.0) value += 360.0;
        return value;
    }

    function deltaAngle(current, target) {
        return normalizeAngle(target - current);
    }

    function readVector3(pointer) {
        try {
            var result = {
                x: pointer.readFloat(),
                y: pointer.add(4).readFloat(),
                z: pointer.add(8).readFloat(),
                valid: true
            };

            result.valid =
                isFinite(result.x) &&
                isFinite(result.y) &&
                isFinite(result.z);

            return result;
        } catch (_) {
            return {
                x: 0.0,
                y: 0.0,
                z: 0.0,
                valid: false
            };
        }
    }

    /*
     * Unity Quaternion.Euler(pitch, yaw, 0) 的等价计算。
     * 正的 Unity X 角度表示向下看，负值表示向上看。
     */


    /*
     * 将修正后的 UnityEngine.Ray 写回 GetShootRay 的隐藏返回缓冲区。
     *
     * Ray 的内存布局：
     *   +0x00 origin.x
     *   +0x04 origin.y
     *   +0x08 origin.z
     *   +0x0C direction.x
     *   +0x10 direction.y
     *   +0x14 direction.z
     *
     * v3.9 在精简时误删了该函数，导致每次开枪都抛出
     * ReferenceError，修正后的射线从未真正交给游戏。
     */
    function writeRay(pointer, origin, direction) {
        if (isNull(pointer) ||
            origin === null ||
            direction === null) {
            return false;
        }

        try {
            var length = Math.sqrt(
                direction.x * direction.x +
                direction.y * direction.y +
                direction.z * direction.z
            );

            if (!isFinite(length) ||
                length < 0.00001) {
                return false;
            }

            var inv = 1.0 / length;

            pointer.writeFloat(origin.x);
            pointer.add(4).writeFloat(origin.y);
            pointer.add(8).writeFloat(origin.z);

            pointer.add(12).writeFloat(
                direction.x * inv
            );
            pointer.add(16).writeFloat(
                direction.y * inv
            );
            pointer.add(20).writeFloat(
                direction.z * inv
            );

            return true;
        } catch (error) {
            stats.errors++;

            if (stats.shootRayFailures < 3) {
                sendLog(
                    'error',
                    '[Shooting] Ray 写回失败: ' +
                        error
                );
            }

            return false;
        }
    }

    function clearBuffer(pointer, size) {
        var offset = 0;

        while (offset + 4 <= size) {
            pointer.add(offset).writeU32(0);
            offset += 4;
        }

        while (offset < size) {
            pointer.add(offset).writeU8(0);
            offset++;
        }
    }

    function safeTransformPosition(transform) {
        var output = {
            x: 0.0,
            y: 0.0,
            z: 0.0
        };

        return readTransformPositionInto(
            transform,
            output
        )
            ? output
            : null;
    }

    function safeTransformForward(transform) {
        var output = {
            x: 0.0,
            y: 0.0,
            z: 1.0
        };

        return readTransformForwardInto(
            transform,
            output
        )
            ? output
            : null;
    }

    function cacheCameraManager(instance, source) {
        if (isNull(instance)) return false;

        var changed =
            isNull(cameraManager) ||
            !cameraManager.equals(instance);

        if (changed && !isReadable(instance)) return false;

        cameraManager = instance;
        sessionDestroyed = false;

        if (changed) {
            localPlayer = null;
            runtime.camera.valid = false;
            runtime.camera.camera = null;
            runtime.camera.transform = null;

            sendLog('info', '[Lifecycle] CameraManager 已捕获', {
                pointer: instance.toString(),
                source: source || 'unknown'
            });
        }

        if (state === STATE.NO_GAME) {
            setState(STATE.READY);
        }
        return true;
    }

    function cacheLocalPlayer(instance, source) {
        if (isNull(instance) || !isReadable(instance)) return false;

        var changed =
            isNull(localPlayer) ||
            !localPlayer.equals(instance);

        localPlayer = instance;

        if (changed) {
            runtime.camera.characterContainer = null;
            runtime.movement.initialized = false;
            clearMuzzleCache(null);

            if (enabled) {
                scheduleRefresh(
                    'local_player_changed',
                    true,
                    true,
                    true,
                    100
                );
            }

            sendLog('info', '[Lifecycle] 本地玩家已捕获', {
                pointer: instance.toString(),
                source: source || 'unknown'
            });
        }
        return true;
    }

    function resolveGameManager() {
        if (!isNull(gameManager) && isReadable(gameManager)) {
            return gameManager;
        }

        return guarded('解析 GameManager Singleton', function () {
            var slot = base.add(
                RVA.GameManager_SingletonMethodInfo
            );
            if (!isReadable(slot)) return null;

            var methodInfo = slot.readPointer();
            if (isNull(methodInfo) ||
                !isReadable(methodInfo)) {
                return null;
            }

            var instance = singletonGetInstance(methodInfo);
            if (isNull(instance) ||
                !isReadable(instance)) {
                return null;
            }

            gameManager = instance;
            return instance;
        }, null);
    }

    function resolveCameraManager() {
        if (!isNull(cameraManager) &&
            isReadable(cameraManager)) {
            return cameraManager;
        }

        return guarded('解析 CameraManager Singleton', function () {
            var slot = base.add(
                RVA.CameraManager_SingletonMethodInfo
            );
            if (!isReadable(slot)) return null;

            var methodInfo = slot.readPointer();
            if (isNull(methodInfo) ||
                !isReadable(methodInfo)) {
                return null;
            }

            var instance = singletonGetInstance(methodInfo);
            if (isNull(instance) ||
                !isReadable(instance)) {
                return null;
            }

            cacheCameraManager(
                instance,
                'singleton_fallback'
            );
            return instance;
        }, null);
    }

    function resolveLocalPlayer() {
        if (!isNull(localPlayer) &&
            isReadable(localPlayer)) {
            return localPlayer;
        }

        var manager = resolveCameraManager();
        if (!isNull(manager)) {
            var focusPlayer = guarded(
                '读取 CameraManager.focusPlayer',
                function () {
                    return manager.add(
                        OFF.CM_focusPlayer
                    ).readPointer();
                },
                null
            );

            if (!isNull(focusPlayer) &&
                isReadable(focusPlayer)) {
                var local = guarded(
                    '验证 focusPlayer',
                    function () {
                        return isMyPlayer(
                            focusPlayer,
                            ptr(0)
                        );
                    },
                    false
                );

                if (local) {
                    cacheLocalPlayer(
                        focusPlayer,
                        'CameraManager.focusPlayer'
                    );
                    return localPlayer;
                }
            }
        }

        var gm = resolveGameManager();
        if (isNull(gm)) return null;

        return guarded('遍历本地玩家', function () {
            var array = gm.add(
                OFF.GM_allPlayers
            ).readPointer();

            if (isNull(array) || !isReadable(array)) {
                return null;
            }

            var count = array.add(0x0C).readU32();
            if (count < 1 || count > 64) return null;

            for (var index = 0; index < count; index++) {
                var player = array.add(
                    0x10 + index * PTR_SIZE
                ).readPointer();

                if (isNull(player) ||
                    !isReadable(player)) {
                    continue;
                }

                if (isMyPlayer(player, ptr(0))) {
                    cacheLocalPlayer(
                        player,
                        'GameManager.allPlayers'
                    );
                    return player;
                }
            }

            return null;
        }, null);
    }

    function isLocalPlayer(candidate) {
        var player = resolveLocalPlayer();
        return !isNull(candidate) &&
            !isNull(player) &&
            candidate.equals(player);
    }


    function readableOrNull(pointer) {
        if (isNull(pointer)) {
            return ptr(0);
        }

        if (isReadable(pointer)) {
            return pointer;
        }

        stats.stalePointerSkips++;
        return ptr(0);
    }

    function getCachedCameraManagerForRestore() {
        if (sessionDestroyed ||
            isNull(cameraManager) ||
            !isReadable(cameraManager)) {
            stats.safeRestoreSkips++;
            return null;
        }

        return cameraManager;
    }

    function getCurrentFreeLookForRestore(manager) {
        if (isNull(manager) ||
            !isReadable(manager)) {
            stats.safeRestoreSkips++;
            return null;
        }

        try {
            var freeLook = manager.add(
                OFF.CM_freeLookCamera
            ).readPointer();

            if (isNull(freeLook) ||
                !isReadable(freeLook)) {
                stats.safeRestoreSkips++;
                return null;
            }

            return freeLook;
        } catch (_) {
            stats.safeRestoreSkips++;
            return null;
        }
    }

    function readCurrentWeaponForRestore(player) {
        if (isNull(player) ||
            !isReadable(player)) {
            return null;
        }

        try {
            var weapons = player.add(
                OFF.Player_wpns
            ).readPointer();

            if (isNull(weapons) ||
                !isReadable(weapons)) {
                return null;
            }

            var weapon = weapons.add(
                OFF.PW_inUse
            ).readPointer();

            if (isNull(weapon) ||
                !isReadable(weapon)) {
                return null;
            }

            return weapon;
        } catch (_) {
            return null;
        }
    }

    function readCurrentModelRefsForRestore() {
        var player = localPlayer;

        if (isNull(player) ||
            !isReadable(player)) {
            stats.safeRestoreSkips++;
            return null;
        }

        try {
            var playerData = player.add(
                OFF.Player_playerData
            ).readPointer();

            var character = player.add(
                OFF.Player_currentCharacter
            ).readPointer();

            if (isNull(playerData) ||
                !isReadable(playerData) ||
                isNull(character) ||
                !isReadable(character)) {
                stats.safeRestoreSkips++;
                return null;
            }

            return {
                player: player,
                playerData: playerData,
                character: character,
                weapon: readCurrentWeaponForRestore(player)
            };
        } catch (_) {
            stats.safeRestoreSkips++;
            return null;
        }
    }

    function captureYAxis(freeLook) {
        if (saved.yAxisCaptured) return true;
        try {
            var axis = freeLook.add(OFF.CFL_m_YAxis);
            saved.yAxisValue = axis.add(OFF.AX_Value).readFloat();
            saved.yAxisInputName = axis.add(OFF.AX_InputAxisName).readPointer();
            saved.yAxisInputProvider = axis.add(OFF.AX_InputProvider).readPointer();
            saved.yAxisInputValue = axis.add(OFF.AX_InputAxisValue).readFloat();
            saved.yAxisInvert = axis.add(OFF.AX_InvertInput).readU8() !== 0;
            saved.yAxisMaxSpeed = axis.add(OFF.AX_MaxSpeed).readFloat();
            saved.yAxisMinValue = axis.add(OFF.AX_MinValue).readFloat();
            saved.yAxisMaxValue = axis.add(OFF.AX_MaxValue).readFloat();
            saved.yAxisWrap = axis.add(OFF.AX_Wrap).readU8() !== 0;
            saved.yAxisCaptured = true;
            return true;
        } catch (error) {
            stats.errors++;
            sendLog('error', '保存 FreeLook YAxis 失败: ' + error);
            return false;
        }
    }

    function lockYAxis(freeLook) {
        if (!captureYAxis(freeLook)) return false;
        try {
            var axis = freeLook.add(OFF.CFL_m_YAxis);
            axis.add(OFF.AX_Value).writeFloat(0.5);
            axis.add(OFF.AX_InputAxisName).writePointer(ptr(0));
            axis.add(OFF.AX_InputProvider).writePointer(ptr(0));
            axis.add(OFF.AX_InputAxisValue).writeFloat(0.0);
            axis.add(OFF.AX_MaxSpeed).writeFloat(0.0);
            axis.add(OFF.AX_InvertInput).writeU8(0);
            axis.add(OFF.AX_MinValue).writeFloat(0.0);
            axis.add(OFF.AX_MaxValue).writeFloat(1.0);
            axis.add(OFF.AX_Wrap).writeU8(0);
            return true;
        } catch (error) {
            stats.errors++;
            sendLog('error', '锁定 FreeLook YAxis 失败: ' + error);
            return false;
        }
    }

    function restoreYAxis(freeLook) {
        if (!saved.yAxisCaptured ||
            isNull(freeLook) ||
            !isReadable(freeLook)) {
            return;
        }

        try {
            var axis = freeLook.add(OFF.CFL_m_YAxis);

            axis.add(OFF.AX_Value).writeFloat(
                saved.yAxisValue
            );

            axis.add(OFF.AX_InputAxisName).writePointer(
                readableOrNull(saved.yAxisInputName)
            );

            axis.add(OFF.AX_InputProvider).writePointer(
                readableOrNull(saved.yAxisInputProvider)
            );

            axis.add(OFF.AX_InputAxisValue).writeFloat(
                saved.yAxisInputValue
            );

            axis.add(OFF.AX_InvertInput).writeU8(
                saved.yAxisInvert ? 1 : 0
            );

            axis.add(OFF.AX_MaxSpeed).writeFloat(
                saved.yAxisMaxSpeed
            );

            axis.add(OFF.AX_MinValue).writeFloat(
                saved.yAxisMinValue
            );

            axis.add(OFF.AX_MaxValue).writeFloat(
                saved.yAxisMaxValue
            );

            axis.add(OFF.AX_Wrap).writeU8(
                saved.yAxisWrap ? 1 : 0
            );
        } catch (_) {
            stats.safeRestoreSkips++;
        }
    }

    function captureCameraState(freeLook) {
        if (saved.cameraCaptured) return true;

        return guarded('保存必要 FreeLook 状态', function () {
            saved.freeLook = freeLook;

            saved.originalFollow = freeLook.add(
                OFF.CFL_m_Follow
            ).readPointer();

            saved.originalLookAt = freeLook.add(
                OFF.CFL_m_LookAt
            ).readPointer();

            if (!captureYAxis(freeLook)) {
                return false;
            }

            saved.cameraCaptured = true;
            return true;
        }, false);
    }

    function applyCameraConfiguration() {
        var manager = resolveCameraManager();
        var player = resolveLocalPlayer();

        if (isNull(manager) || isNull(player)) {
            return false;
        }

        return guarded('应用最小第三人称相机', function () {
            var freeLook = manager.add(
                OFF.CM_freeLookCamera
            ).readPointer();

            var characterContainer = player.add(
                OFF.Player_characterContainer
            ).readPointer();

            if (isNull(freeLook) ||
                !isReadable(freeLook) ||
                isNull(characterContainer) ||
                !isReadable(characterContainer)) {
                return false;
            }

            if (!captureCameraState(freeLook)) {
                return false;
            }

            /*
             * FreeLook 只保留三个基础职责：
             * 1. 提供水平 Yaw；
             * 2. 跟随本地人物；
             * 3. 处理场景相机生命周期。
             *
             * 轨道高度、半径和 Composer 不再修改。
             */
            setFollow(
                freeLook,
                characterContainer,
                ptr(0)
            );

            setLookAt(
                freeLook,
                characterContainer,
                ptr(0)
            );

            lockYAxis(freeLook);

            setFreeLookActive(
                manager,
                1,
                ptr(0)
            );

            sendLog('info', '[Camera] 第三人称相机已配置', {
                shoulder: 'center',
                distance: config.distance,
                pivotHeight: config.pivotHeight,
                pitchMode:
                    'independent_final_camera_pivot',
                freeLookMode:
                    'follow_lookat_yaw_only'
            });

            return true;
        }, false);
    }

    function applyModelMode(player) {
        return guarded('显示第三人称人物模型', function () {
            var playerData = player.add(
                OFF.Player_playerData
            ).readPointer();

            var character = player.add(
                OFF.Player_currentCharacter
            ).readPointer();

            if (isNull(playerData) ||
                !isReadable(playerData) ||
                isNull(character) ||
                !isReadable(character)) {
                return false;
            }

            if (!saved.modelCaptured) {
                saved.playerData = playerData;
                saved.observeMode = playerData.add(
                    OFF.PD_observeMode
                ).readS32();

                saved.playerViewModelVisible =
                    playerData.add(
                        OFF.PD_playerViewModelVisible
                    ).readU8() !== 0;

                saved.modelCaptured = true;
            }

            saved.character = character;

            setObserveMode(
                playerData,
                0,
                ptr(0)
            );

            onOwnerObserveModeChange(
                character,
                0,
                ptr(0)
            );

            playerData.add(
                OFF.PD_playerViewModelVisible
            ).writeU8(0);

            var weapons = player.add(
                OFF.Player_wpns
            ).readPointer();

            if (!isNull(weapons) &&
                isReadable(weapons)) {
                var weapon = weapons.add(
                    OFF.PW_inUse
                ).readPointer();

                if (!isNull(weapon) &&
                    isReadable(weapon)) {
                    saved.weapon = weapon;
                    synchronizeHand(
                        weapon,
                        ptr(0)
                    );
                }
            }

            return true;
        }, false);
    }

    function restoreCameraState() {
        if (!saved.cameraCaptured) return;

        var manager =
            getCachedCameraManagerForRestore();

        if (isNull(manager)) return;

        var currentFreeLook =
            getCurrentFreeLookForRestore(manager);

        if (isNull(currentFreeLook)) return;

        /*
         * 如果当前 FreeLook 已不是开启时保存的对象，
         * 说明场景/背包/相机链可能已经重建。
         * 此时不再把旧 Follow/LookAt 写回新对象，避免旧指针导致闪退。
         */
        if (!isNull(saved.freeLook) &&
            !currentFreeLook.equals(saved.freeLook)) {
            stats.safeRestoreSkips++;
            return;
        }

        restoreYAxis(currentFreeLook);

        guarded('安全恢复原始相机状态', function () {
            setFollow(
                currentFreeLook,
                readableOrNull(
                    saved.originalFollow
                ),
                ptr(0)
            );

            setLookAt(
                currentFreeLook,
                readableOrNull(
                    saved.originalLookAt
                ),
                ptr(0)
            );

            stats.safeRestoreRebinds++;
        }, null);
    }

    function restoreModelMode() {
        if (!saved.modelCaptured) {
            return;
        }

        var refs =
            readCurrentModelRefsForRestore();

        if (refs === null) {
            /*
             * 关闭时如果玩家、角色或背包已被游戏重建/销毁，
             * 直接跳过模型恢复比强行使用 saved 旧指针更安全。
             */
            return;
        }

        guarded('安全恢复原始人物模型模式', function () {
            onOwnerObserveModeChange(
                refs.character,
                saved.observeMode,
                ptr(0)
            );

            setObserveMode(
                refs.playerData,
                saved.observeMode,
                ptr(0)
            );

            refs.playerData.add(
                OFF.PD_playerViewModelVisible
            ).writeU8(
                saved.playerViewModelVisible
                    ? 1
                    : 0
            );

            /*
             * 不再使用 saved.weapon。
             * 背包/武器切换后 saved.weapon 可能是旧武器对象，
             * 关闭时只同步当前 inUse 武器。
             */
            if (!isNull(refs.weapon) &&
                isReadable(refs.weapon)) {
                synchronizeHand(
                    refs.weapon,
                    ptr(0)
                );
            }

            stats.safeRestoreRebinds++;
        }, null);
    }

    function resetSavedState() {
        saved = {
            cameraCaptured: false,
            modelCaptured: false,

            freeLook: null,
            originalFollow: null,
            originalLookAt: null,

            yAxisCaptured: false,
            yAxisInputName: null,
            yAxisInputProvider: null,
            yAxisInputValue: 0.0,
            yAxisInvert: false,
            yAxisMaxSpeed: 0.0,
            yAxisMinValue: 0.0,
            yAxisMaxValue: 1.0,
            yAxisWrap: false,
            yAxisValue: 0.5,

            playerData: null,
            character: null,
            weapon: null,
            observeMode: 0,
            playerViewModelVisible: true
        };
    }

    /*
     * v3.6 核心：
     *
     * Cinemachine 先正常输出水平第三人称相机。
     * 随后以人物上背部为虚拟 Pivot，重新计算最终相机：
     *
     *   CameraPosition = Pivot - Forward(yaw, pitch) * distance
     *
     * 这样鼠标上下会真正改变镜头方向和位置，
     * 而不是只在三条高度很接近的 FreeLook 轨道之间移动。
     */


    function maybeValidateCameraCache(now) {
        var cameraState = runtime.camera;

        if (now -
            cameraState.lastHealthCheckTime <
                LIMITS.cameraCacheHealthCheckMs) {
            return true;
        }

        cameraState.lastHealthCheckTime = now;
        stats.cameraCacheHealthChecks++;

        /*
         * 低频执行旧指针验证，避免每帧执行高成本检查。
         *
         * P0 修复：
         * 原先这里用 isReadable -> Process.findRangeByAddress，
         * 实测单次 7~13ms（开的功能越多越慢），
         * 每秒 3 次正好造成“每秒掉一帧”的卡顿。
         * 根因已在 isReadable 内部修掉（受保护单字节读取），
         * 这里再叠一层只读 m_CachedPtr 的活体校验：
         *   - native 对象已销毁 -> m_CachedPtr 为 0 -> 判失效；
         *   - 指针本身已不可访问 -> 读取抛异常被捕获 -> 判失效。
         * 成本由毫秒级降到亚微秒级，判定语义不变。
         */
        if (!isNull(cameraState.transform) &&
            !isAliveUnityObject(cameraState.transform)) {
            cameraState.transform = null;
            cameraState.camera = null;
            cameraState.valid = false;
            stats.staleCameraResets++;
            return false;
        }

        if (!isNull(cameraState.characterContainer) &&
            !isAliveUnityObject(cameraState.characterContainer)) {
            cameraState.characterContainer = null;
            cameraState.valid = false;
            stats.staleCameraResets++;
            return false;
        }

        if (!isNull(localPlayer) &&
            !isAliveUnityObject(localPlayer)) {
            localPlayer = null;
            cameraState.characterContainer = null;
            cameraState.valid = false;
            stats.staleCameraResets++;
            return false;
        }

        return true;
    }

    function readNativeCameraYaw(cameraTransform) {
        if (!readTransformForwardInto(
            cameraTransform,
            tempRawForward
        )) {
            return null;
        }

        var horizontalLength = Math.sqrt(
            tempRawForward.x *
                tempRawForward.x +
            tempRawForward.z *
                tempRawForward.z
        );

        if (horizontalLength < 0.00001) {
            return null;
        }

        stats.yawNativeReads++;

        return normalizeAngle(
            Math.atan2(
                tempRawForward.x /
                    horizontalLength,
                tempRawForward.z /
                    horizontalLength
            ) * 180.0 / Math.PI
        );
    }


    function updateFinalCamera(brain) {
        if (!enabled || runtime.playerDead || !runtime.cameraInput.valid) {
            return false;
        }

        try {
            var cameraState = runtime.camera;

            var now = Date.now();

            /*
             * P0 诊断：把低频健康检查（含 isReadable）单独计时，
             * 与 finalCameraUs 的其余部分区分开。
             */
            var healthCheckStart = perfClock.now();

            maybeValidateCameraCache(now);

            recordPerfMetric(
                perf.metrics.healthCheck,
                perfClock.now() - healthCheckStart
            );

            if (isNull(cameraState.transform)) {
                var camera = brainGetOutputCamera(brain, ptr(0));
                if (isNull(camera)) {
                    return false;
                }

                var cameraTransform = componentGetTransform(camera, ptr(0));
                if (isNull(cameraTransform)) {
                    return false;
                }

                /*
                 * 新解析对象时检查一次即可，不要每帧检查。
                 */
                if (!isReadable(camera) ||
                    !isReadable(cameraTransform)) {
                    return false;
                }

                cameraState.camera = camera;
                cameraState.transform = cameraTransform;
            }

            if (isNull(cameraState.characterContainer)) {
                if (isNull(localPlayer)) {
                    return false;
                }

                cameraState.characterContainer = localPlayer.add(
                    OFF.Player_characterContainer
                ).readPointer();

                if (isNull(cameraState.characterContainer)) {
                    return false;
                }

                /*
                 * 新解析对象时检查一次即可，不要每帧检查。
                 */
                if (!isReadable(localPlayer) ||
                    !isReadable(cameraState.characterContainer)) {
                    cameraState.characterContainer = null;
                    return false;
                }
            }

            /*
             * 复活、场景切换和 FreeLook 重建后，
             * XAxis 的绑定模式、初始值和更新时机可能变化。
             * 始终读取最终 Camera Transform.forward，
             * 不再猜测 XAxis 正负方向。
             */
            var yaw =
                readNativeCameraYaw(
                    cameraState.transform
                );

            var haveCharacterPosition =
                readTransformPositionInto(
                    cameraState.characterContainer,
                    tempCharacterPosition
                );

            if (yaw === null ||
                !haveCharacterPosition) {
                stats.cameraFailures++;
                return false;
            }

            var desiredPitch = runtime.cameraInput.pitch;
            if (!config.invertY) desiredPitch = -desiredPitch;
            desiredPitch = Math.max(
                -LIMITS.maxCameraPitchDegrees,
                Math.min(LIMITS.maxCameraPitchDegrees, desiredPitch)
            );

            var pivot = runtime.cameraPivot;

            if (!pivot.initialized) {
                pivot.smoothedPitch = desiredPitch;
                pivot.initialized = true;
            } else {
                var deltaMs = Math.max(
                    1,
                    Math.min(100, now - pivot.lastWriteTime)
                );
                var alpha = 1.0 - Math.exp(
                    -(deltaMs / 1000.0) *
                    LIMITS.cameraPitchFollowSpeed
                );
                var step = (
                    desiredPitch - pivot.smoothedPitch
                ) * alpha;
                step = Math.max(
                    -LIMITS.maxCameraPitchStepDegrees,
                    Math.min(LIMITS.maxCameraPitchStepDegrees, step)
                );
                pivot.smoothedPitch += step;
            }
            pivot.lastWriteTime = now;

            var pitchRadians = pivot.smoothedPitch * Math.PI / 180.0;
            var yawRadians = yaw * Math.PI / 180.0;
            var cosPitch = Math.cos(pitchRadians);
            var forwardX = Math.sin(yawRadians) * cosPitch;
            var forwardY = -Math.sin(pitchRadians);
            var forwardZ = Math.cos(yawRadians) * cosPitch;

            var pivotX = tempCharacterPosition.x;
            var pivotY =
                tempCharacterPosition.y +
                config.pivotHeight;
            var pivotZ = tempCharacterPosition.z;

            var cameraX = pivotX - forwardX * config.distance;
            var cameraY = pivotY - forwardY * config.distance;
            var cameraZ = pivotZ - forwardZ * config.distance;

            cameraWritePositionBuffer.writeFloat(cameraX);
            cameraWritePositionBuffer.add(4).writeFloat(cameraY);
            cameraWritePositionBuffer.add(8).writeFloat(cameraZ);

            var halfPitch = pitchRadians * 0.5;
            var halfYaw = yawRadians * 0.5;
            var sx = Math.sin(halfPitch);
            var cx = Math.cos(halfPitch);
            var sy = Math.sin(halfYaw);
            var cy = Math.cos(halfYaw);

            cameraWriteRotationBuffer.writeFloat(cy * sx);
            cameraWriteRotationBuffer.add(4).writeFloat(sy * cx);
            cameraWriteRotationBuffer.add(8).writeFloat(-sy * sx);
            cameraWriteRotationBuffer.add(12).writeFloat(cy * cx);

            // P1：热路径只判 null 不够——Transform 可能已随相机销毁，写前验活
            if (isAliveUnityObject(cameraState.transform)) {
                transformSetPosition(
                    cameraState.transform,
                    cameraWritePositionBuffer,
                    ptr(0)
                );
                transformSetRotation(
                    cameraState.transform,
                    cameraWriteRotationBuffer,
                    ptr(0)
                );
            } else {
                cameraState.valid = false;
            }

            cameraState.valid = true;
            cameraState.position.x = cameraX;
            cameraState.position.y = cameraY;
            cameraState.position.z = cameraZ;
            cameraState.forward.x = forwardX;
            cameraState.forward.y = forwardY;
            cameraState.forward.z = forwardZ;
            cameraState.yaw = yaw;
            cameraState.pitch = -pivot.smoothedPitch;
            cameraState.lastWriteTime = now;
            cameraState.frameId++;

            stats.cameraFrames++;
            return true;
        } catch (error) {
            stats.errors++;
            stats.cameraFailures++;
            if (stats.cameraFailures <= 3) {
                sendLog('error', '[Camera] 最终相机更新失败: ' + error);
            }
            return false;
        }
    }

    /*
     * v3.4 核心性能修复：
     *
     * 不再在 Player.MoveByLocalDirection 前后各旋转一次 Transform。
     * 直接 Hook 编译器生成的 GetWalkVelocity：
     *
     *   返回缓冲区、Player、DisplayClass(x/z/moveSpeed)、MethodInfo
     *
     * 原函数先计算完整速度和各种移动倍率。
     * 我们只替换最终水平 X/Z 方向，保留原来的速度大小和 Y 分量，
     * 因此不会破坏跳跃、重力、碰撞、加速度和速度惩罚。
     */
    function rotateWalkVelocityToCamera(
        returnBuffer,
        player,
        displayClass
    ) {
        if (!enabled ||
            runtime.playerDead ||
            !runtime.camera.valid ||
            isNull(returnBuffer) ||
            isNull(displayClass) ||
            isNull(localPlayer) ||
            !player.equals(localPlayer)) {
            return false;
        }

        try {
            var inputX = displayClass.readS32();
            var inputZ = displayClass.add(4).readS32();
            stats.movementCalls++;

            if (inputX === 0 && inputZ === 0) return false;

            var originalX = returnBuffer.readFloat();
            var originalY = returnBuffer.add(4).readFloat();
            var originalZ = returnBuffer.add(8).readFloat();
            var speed = Math.sqrt(
                originalX * originalX + originalZ * originalZ
            );
            if (!isFinite(speed) || speed < 0.00001) return false;

            var forwardX = runtime.camera.forward.x;
            var forwardZ = runtime.camera.forward.z;
            var forwardLength = Math.sqrt(
                forwardX * forwardX + forwardZ * forwardZ
            );
            if (forwardLength < 0.00001) return false;

            forwardX /= forwardLength;
            forwardZ /= forwardLength;

            var desiredX = forwardZ * inputX + forwardX * inputZ;
            var desiredZ = -forwardX * inputX + forwardZ * inputZ;
            var desiredLength = Math.sqrt(
                desiredX * desiredX + desiredZ * desiredZ
            );
            if (desiredLength < 0.00001) return false;

            returnBuffer.writeFloat(
                desiredX / desiredLength * speed
            );
            returnBuffer.add(4).writeFloat(originalY);
            returnBuffer.add(8).writeFloat(
                desiredZ / desiredLength * speed
            );

            stats.movementVectorsModified++;
            return true;
        } catch (_) {
            stats.errors++;
            return false;
        }
    }

    /*
     * 人物身体只做水平 Yaw 跟随：
     * - 在原相机输入函数执行后写入；
     * - 只写 cameraRotation.x；
     * - 绝不修改 cameraRotation.y（Pitch）；
     * - 不修改人物 Transform 的 X/Z 旋转。
     *
     * 因此人物根节点始终直立，鼠标上下只控制镜头。
     */

    function handleCameraInputAndBodyYaw(player) {
        if (!enabled ||
            runtime.playerDead ||
            isNull(localPlayer) ||
            !player.equals(localPlayer)) {
            return;
        }

        try {
            var rawYaw = player.add(
                OFF.Player_cameraRotation
            ).readFloat();
            var pitch = player.add(
                OFF.Player_cameraRotation + 4
            ).readFloat();

            if (!isFinite(rawYaw) ||
                !isFinite(pitch) ||
                pitch < -180.0 ||
                pitch > 180.0) {
                stats.inputFailures++;
                return;
            }

            var now = Date.now();
            runtime.cameraInput.valid = true;
            runtime.cameraInput.rawYaw = rawYaw;
            runtime.cameraInput.pitch = pitch;
            runtime.cameraInput.lastSampleTime = now;
            stats.pitchInputSamples++;

            if (!runtime.camera.valid ||
                now - runtime.movement.lastYawUpdateTime <
                    LIMITS.bodyYawIntervalMs) {
                return;
            }

            var movement = runtime.movement;
            if (!movement.initialized) {
                movement.smoothYaw = rawYaw;
                movement.initialized = true;
            }

            var deltaMs = movement.lastYawUpdateTime === 0
                ? LIMITS.bodyYawIntervalMs
                : Math.max(
                    1,
                    Math.min(100, now - movement.lastYawUpdateTime)
                );

            movement.lastYawUpdateTime = now;

            var targetYaw = runtime.camera.yaw;
            var alpha = 1.0 - Math.exp(
                -(deltaMs / 1000.0) *
                LIMITS.bodyYawFollowSpeed
            );
            movement.smoothYaw = normalizeAngle(
                movement.smoothYaw +
                deltaAngle(movement.smoothYaw, targetYaw) * alpha
            );

            player.add(
                OFF.Player_cameraRotation
            ).writeFloat(movement.smoothYaw);

            stats.movementYawUpdates++;
        } catch (_) {
            stats.errors++;
        }
    }


    /*
     * 获取游戏真正显示的 HUD 准星像素坐标。
     * v3.8 假定准星等于屏幕中心，因此当 HUD 准星略高时，
     * 子弹会稳定落在准星下方。
     */



    /*
     * 按真实 HUD 准星位置构造世界空间射线。
     * 只在真实开枪时运行，不增加每帧负担。
     */

    function computeAimTargetForCurrentFrame() {
        var camera = runtime.camera;
        var solution = runtime.aimSolution;

        if (!camera.valid) return false;

        if (solution.valid &&
            solution.frameId ===
                camera.frameId) {
            solution.reusedLast = true;
            stats.sameFrameAimReuses++;
            return true;
        }

        var originX = camera.position.x;
        var originY = camera.position.y;
        var originZ = camera.position.z;

        var directionX = camera.forward.x;
        var directionY = camera.forward.y;
        var directionZ = camera.forward.z;

        var haveHit = false;

        if (!runtime.physicsDisabled) {
            stats.physicsRaycastCalls++;

            try {
                clearBuffer(
                    raycastHitBuffer,
                    0x2C
                );

                physicsGetDefaultSceneInjected(
                    physicsSceneBuffer,
                    ptr(0)
                );

                rayBuffer.writeFloat(originX);
                rayBuffer.add(4).writeFloat(originY);
                rayBuffer.add(8).writeFloat(originZ);
                rayBuffer.add(12).writeFloat(
                    directionX
                );
                rayBuffer.add(16).writeFloat(
                    directionY
                );
                rayBuffer.add(20).writeFloat(
                    directionZ
                );

                haveHit =
                    physicsInternalRaycastInjected(
                        physicsSceneBuffer,
                        rayBuffer,
                        LIMITS.maxAimDistance,
                        raycastHitBuffer,
                        -1,
                        0,
                        ptr(0)
                    );

                runtime.physicsFailures = 0;
            } catch (error) {
                stats.errors++;
                runtime.physicsFailures++;

                if (runtime.physicsFailures >= 3) {
                    runtime.physicsDisabled = true;
                    sendLog(
                        'warning',
                        '[Shooting] 物理射线连续失败，改用相机远点'
                    );
                }

                haveHit = false;
            }
        }

        if (haveHit) {
            var hitX =
                raycastHitBuffer.readFloat();
            var hitY =
                raycastHitBuffer.add(4).readFloat();
            var hitZ =
                raycastHitBuffer.add(8).readFloat();

            if (isFinite(hitX) &&
                isFinite(hitY) &&
                isFinite(hitZ)) {
                solution.targetX = hitX;
                solution.targetY = hitY;
                solution.targetZ = hitZ;
            } else {
                haveHit = false;
            }
        }

        if (!haveHit) {
            solution.targetX =
                originX +
                directionX *
                LIMITS.maxAimDistance;

            solution.targetY =
                originY +
                directionY *
                LIMITS.maxAimDistance;

            solution.targetZ =
                originZ +
                directionZ *
                LIMITS.maxAimDistance;
        }

        solution.valid = true;
        solution.frameId = camera.frameId;
        solution.reusedLast = false;

        stats.aimFramesComputed++;
        return true;
    }

    function clearMuzzleCache(reason) {
        runtime.muzzle.valid = false;
        runtime.muzzle.weapon = null;
        runtime.muzzle.transform = null;
        runtime.muzzle.source = 'none';
        runtime.shootRay.valid = false;
        invalidateAimSolution();

        if (enabled && reason) {
            sendLog('info', '[Lifecycle] 已刷新武器缓存', {
                reason: reason
            });
        }
    }


    function validateCachedMuzzleOwner(player) {
        if (isNull(player) ||
            !runtime.muzzle.valid ||
            isNull(runtime.muzzle.weapon) ||
            isNull(runtime.muzzle.transform)) {
            return false;
        }

        try {
            var weapons = player.add(
                OFF.Player_wpns
            ).readPointer();

            if (isNull(weapons) ||
                !isReadable(weapons)) {
                stats.muzzleOwnerMismatches++;
                return false;
            }

            var currentWeapon = weapons.add(
                OFF.PW_inUse
            ).readPointer();

            stats.muzzleOwnerChecks++;

            if (!isNull(currentWeapon) &&
                currentWeapon.equals(
                    runtime.muzzle.weapon
                )) {
                return true;
            }

            stats.muzzleOwnerMismatches++;
            return false;
        } catch (_) {
            stats.muzzleOwnerMismatches++;
            return false;
        }
    }

    function resolveMuzzleTransform(force) {
        if (!enabled || runtime.playerDead) {
            return false;
        }

        var player = localPlayer;
        if (isNull(player)) return false;

        if (!force &&
            runtime.muzzle.valid &&
            !isNull(runtime.muzzle.weapon) &&
            !isNull(runtime.muzzle.transform)) {
            /*
             * 轻量 owner 验证：
             * 只确认本地玩家当前 inUse 武器是否仍等于缓存 weapon。
             * 不调用 Unity NativeFunction，不重新解析 Transform。
             */
            if (validateCachedMuzzleOwner(player)) {
                return true;
            }

            /*
             * 当前武器已经不是缓存武器，说明切枪/复活/对象复用后
             * 缓存枪口失效。清空后继续走当前武器重新解析。
             */
            clearMuzzleCache(null);
        }

        return guarded('解析当前武器枪口', function () {
            var weapons = player.add(
                OFF.Player_wpns
            ).readPointer();

            if (isNull(weapons) ||
                !isReadable(weapons)) {
                stats.muzzleFailures++;
                return false;
            }

            var weapon = weapons.add(
                OFF.PW_inUse
            ).readPointer();

            if (isNull(weapon) ||
                !isReadable(weapon)) {
                stats.muzzleFailures++;
                return false;
            }

            var transform = null;
            var source = 'none';

            var gunFire = weapon.add(
                OFF.WPN_Gun_gunFire
            ).readPointer();

            if (!isNull(gunFire) &&
                isReadable(gunFire)) {
                transform = componentGetTransform(
                    gunFire,
                    ptr(0)
                );

                if (!isNull(transform) &&
                    isReadable(transform)) {
                    source = 'WPN_Gun.gunFire';
                }
            }

            if (isNull(transform) ||
                !isReadable(transform)) {
                transform = componentGetTransform(
                    weapon,
                    ptr(0)
                );

                if (!isNull(transform) &&
                    isReadable(transform)) {
                    source =
                        'weapon.transform_fallback';
                }
            }

            if (isNull(transform) ||
                !isReadable(transform)) {
                stats.muzzleFailures++;
                return false;
            }

            runtime.muzzle.weapon = weapon;
            runtime.muzzle.transform = transform;
            runtime.muzzle.source = source;
            runtime.muzzle.valid = true;
            stats.muzzleResolves++;

            sendLog('info', '[Shooting] 枪口已解析', {
                weapon: weapon.toString(),
                transform: transform.toString(),
                source: source
            });

            return true;
        }, false);
    }

    /*
     * v3.4：开枪时才进行一次 Physics Raycast 和一次枪口位置读取。
     * 平时不再每 50ms 计算目标点和枪口位置。
     */


    function buildShotSolutionOnDemand() {
        if (!enabled ||
            runtime.playerDead ||
            !runtime.camera.valid) {
            return false;
        }

        var now = Date.now();

        if (now -
            runtime.camera.lastWriteTime >
                LIMITS.cameraCacheMaxAgeMs) {
            return false;
        }

        if (!resolveMuzzleTransform(false)) {
            return false;
        }

        /*
         * 标准 TPS 双射线：
         * 1. 最终相机中心射线确定世界目标；
         * 2. 每发读取最新枪口位置；
         * 3. 从枪口指向该目标。
         */
        if (!computeAimTargetForCurrentFrame()) {
            return false;
        }

        if (!readTransformPositionInto(
            runtime.muzzle.transform,
            tempMuzzlePosition
        )) {
            stats.muzzleFailures++;
            stats.staleMuzzleInvalidations++;
            clearMuzzleCache(null);
            return false;
        }

        var target =
            runtime.aimSolution;

        var dx =
            target.targetX -
            tempMuzzlePosition.x;

        var dy =
            target.targetY -
            tempMuzzlePosition.y;

        var dz =
            target.targetZ -
            tempMuzzlePosition.z;

        var length = Math.sqrt(
            dx * dx +
            dy * dy +
            dz * dz
        );

        if (!isFinite(length) ||
            length < 0.00001) {
            return false;
        }

        var inv = 1.0 / length;

        runtime.shootRay.valid = true;

        runtime.shootRay.origin.x =
            tempMuzzlePosition.x;
        runtime.shootRay.origin.y =
            tempMuzzlePosition.y;
        runtime.shootRay.origin.z =
            tempMuzzlePosition.z;

        runtime.shootRay.direction.x =
            dx * inv;
        runtime.shootRay.direction.y =
            dy * inv;
        runtime.shootRay.direction.z =
            dz * inv;

        runtime.shootRay.targetPoint.x =
            target.targetX;
        runtime.shootRay.targetPoint.y =
            target.targetY;
        runtime.shootRay.targetPoint.z =
            target.targetZ;

        runtime.shootRay.aimSource =
            'camera_center';

        return true;
    }


    function resetRefreshQueue() {
        refreshQueue.pending = false;
        refreshQueue.dueAt = 0;
        refreshQueue.model = false;
        refreshQueue.camera = false;
        refreshQueue.muzzle = false;
        refreshQueue.eventCount = 0;
        refreshQueue.lastReason = 'none';
    }

    function scheduleRefresh(
        reason,
        model,
        camera,
        muzzle,
        delayMs
    ) {
        if (!enabled) return;

        var now = Date.now();
        var dueAt = now + Math.max(
            0,
            delayMs || 0
        );

        refreshQueue.pending = true;
        refreshQueue.model =
            refreshQueue.model || !!model;
        refreshQueue.camera =
            refreshQueue.camera || !!camera;
        refreshQueue.muzzle =
            refreshQueue.muzzle || !!muzzle;
        refreshQueue.eventCount++;
        refreshQueue.lastReason =
            reason || 'unknown';

        /*
         * 生命周期爆发使用 debounce：
         * 每个新事件都会把执行时间推迟到本次事件之后。
         * delay=0 的配置更新则在下一次主线程 Update 立即执行。
         */
        if (delayMs === 0) {
            refreshQueue.dueAt = now;
        } else {
            refreshQueue.dueAt = Math.max(
                refreshQueue.dueAt,
                dueAt
            );
        }

        stats.lifecycleEvents++;
    }

    function processRefreshQueue() {
        if (!enabled ||
            !refreshQueue.pending ||
            Date.now() < refreshQueue.dueAt) {
            return;
        }

        if (isNull(localPlayer) ||
            isNull(cameraManager)) {
            refreshQueue.dueAt =
                Date.now() + 100;
            return;
        }

        var doModel = refreshQueue.model;
        var doCamera = refreshQueue.camera;
        var doMuzzle = refreshQueue.muzzle;
        var eventCount =
            refreshQueue.eventCount;
        var lastReason =
            refreshQueue.lastReason;

        resetRefreshQueue();

        if (doModel) {
            applyModelMode(localPlayer);
        }

        if (doCamera) {
            runtime.camera.characterContainer =
                null;
            runtime.camera.transform = null;
            runtime.camera.camera = null;
            runtime.camera.valid = false;

            invalidateAimSolution();
            applyCameraConfiguration();
        }

        if (doMuzzle) {
            clearMuzzleCache(null);

            if (!runtime.playerDead) {
                resolveMuzzleTransform(true);
            }
        }

        stats.lifecycleBatches++;
        stats.lifecycleEventsMerged +=
            Math.max(0, eventCount - 1);

        /*
         * 只在确实合并了多个事件时记录，避免普通切枪刷日志。
         */
        if (eventCount > 1) {
            sendLog(
                'info',
                '[Lifecycle] 合并刷新完成',
                {
                    events: eventCount,
                    merged:
                        eventCount - 1,
                    reason: lastReason,
                    model: doModel,
                    camera: doCamera,
                    muzzle: doMuzzle
                }
            );
        }
    }

    function updateRuntimeMainThread() {
        if (!enabled) return;

        processRefreshQueue();
        emitBasicStatus();
        emitPerfStatus();
    }

    function emitBasicStatus() {
        if (!enabled) return;

        var now = Date.now();

        if (now -
            runtime.lastStatusLogTime <
                LIMITS.statusLogIntervalMs) {
            return;
        }

        runtime.lastStatusLogTime = now;

        sendLog('info', '[TPSStatus]', {
            cameraFrames:
                stats.cameraFrames,
            cameraFailures:
                stats.cameraFailures,
            inputPitch:
                runtime.cameraInput.pitch,
            renderedPitch:
                runtime.camera.pitch,

            yawSource:
                'transform_forward_stable',

            movementVectorsModified:
                stats.movementVectorsModified,

            physicsRaycastCalls:
                stats.physicsRaycastCalls,

            shootRayModified:
                stats.shootRayModified,

            muzzleOwnerChecks:
                stats.muzzleOwnerChecks,

            muzzleOwnerMismatches:
                stats.muzzleOwnerMismatches,

            safeRestoreSkips:
                stats.safeRestoreSkips,

            stalePointerSkips:
                stats.stalePointerSkips,

            staleCameraResets:
                stats.staleCameraResets,

            staleMuzzleInvalidations:
                stats.staleMuzzleInvalidations,

            cameraCacheHealthChecks:
                stats.cameraCacheHealthChecks,

            hotPathReadableChecksRemoved:
                stats.hotPathReadableChecksRemoved,

            aimFramesComputed:
                stats.aimFramesComputed,

            sameFrameAimReuses:
                stats.sameFrameAimReuses,

            lifecycleEvents:
                stats.lifecycleEvents,

            lifecycleBatches:
                stats.lifecycleBatches,

            lifecycleEventsMerged:
                stats.lifecycleEventsMerged,

            playerDead:
                runtime.playerDead
        });
    }

    function resetRuntime() {
        runtime.playerDead = false;

        runtime.camera.valid = false;
        runtime.camera.camera = null;
        runtime.camera.transform = null;
        runtime.camera.characterContainer = null;
        runtime.camera.position.x = 0.0;
        runtime.camera.position.y = 0.0;
        runtime.camera.position.z = 0.0;
        runtime.camera.forward.x = 0.0;
        runtime.camera.forward.y = 0.0;
        runtime.camera.forward.z = 1.0;
        runtime.camera.yaw = 0.0;
        runtime.camera.pitch = 0.0;
        runtime.camera.frameId = 0;
        runtime.camera.lastWriteTime = 0;
        runtime.camera.lastHealthCheckTime = 0;

        runtime.cameraInput.valid = false;
        runtime.cameraInput.rawYaw = 0.0;
        runtime.cameraInput.pitch = 0.0;
        runtime.cameraInput.lastSampleTime = 0;

        runtime.cameraPivot.initialized = false;
        runtime.cameraPivot.smoothedPitch = 0.0;
        runtime.cameraPivot.lastWriteTime = 0;

        runtime.movement.initialized = false;
        runtime.movement.smoothYaw = 0.0;
        runtime.movement.lastYawUpdateTime = 0;

        clearMuzzleCache(null);

        invalidateAimSolution();
        resetRefreshQueue();

        runtime.physicsDisabled = false;
        runtime.physicsFailures = 0;
        runtime.lastStatusLogTime = 0;

        resetPerf();
    }

    function performEnable() {
        if (enabled) {
            pendingEnable = false;
            return {
                ok: true,
                enabled: true,
                message: '已经启用'
            };
        }

        var manager = resolveCameraManager();
        var player = resolveLocalPlayer();

        if (isNull(manager) ||
            isNull(player)) {
            return {
                ok: false,
                enabled: false,
                error: isNull(manager)
                    ? 'CameraManager 未就绪'
                    : '本地玩家未就绪'
            };
        }

        commandBusy = true;
        resetRuntime();

        var modelOk =
            applyModelMode(player);

        var cameraOk =
            applyCameraConfiguration();

        // 启用阶段已经直接完成配置，清空旧生命周期队列。
        resetRefreshQueue();

        if (!modelOk || !cameraOk) {
            restoreCameraState();
            restoreModelMode();
            resetSavedState();
            commandBusy = false;

            return {
                ok: false,
                enabled: false,
                error:
                    !modelOk
                        ? '人物模型切换失败'
                        : '第三人称相机配置失败'
            };
        }

        enabled = true;
        sendStatus('third_person_camera', true);
        pendingEnable = false;
        resolveMuzzleTransform(true);
        setState(STATE.ENABLED);
        commandBusy = false;

        sendLog('info', '最小可用第三人称射击已启用', {
            camera: true,
            model: true,
            movement: 'camera_relative',
            shooting: 'muzzle_to_crosshair'
        });

        sendPluginEvent('enabled', {
            ok: true,
            enabled: true
        });

        return {
            ok: true,
            enabled: true
        };
    }

    function performDisable() {
        pendingEnable = false;
        pendingDisable = false;
        resetRefreshQueue();

        if (!enabled) {
            return {
                ok: true,
                enabled: false
            };
        }

        commandBusy = true;

        /*
         * 关闭前先让射击相关缓存失效。
         * 这样即使关闭过程中背包/武器已经变化，
         * 也不会再用旧枪口 Transform。
         */
        clearMuzzleCache(null);
        invalidateAimSolution();

        enabled = false;
        sendStatus('third_person_camera', false);

        var manager =
            getCachedCameraManagerForRestore();

        if (!isNull(manager)) {
            restoreCameraState();

            guarded('安全关闭 FreeLook', function () {
                if (!isNull(manager) &&
                    isReadable(manager)) {
                    setFreeLookActive(
                        manager,
                        0,
                        ptr(0)
                    );
                }
            }, null);
        }

        restoreModelMode();
        resetRuntime();
        resetSavedState();

        setState(
            !isNull(gameManager) &&
            isReadable(gameManager)
                ? STATE.READY
                : STATE.NO_GAME
        );

        commandBusy = false;

        sendLog('info', '最小可用第三人称射击已关闭');
        sendPluginEvent('disabled', {
            ok: true,
            enabled: false
        });

        return {
            ok: true,
            enabled: false
        };
    }

    function processCommands() {
        if (commandBusy) return;

        if (pendingDisable) {
            performDisable();
            return;
        }

        if (pendingEnable && !enabled) {
            performEnable();
            return;
        }
    }

    function requestEnable(input) {
        var validation = validateConfig(input || {});
        if (!validation.ok) {
            return validation;
        }

        config = validation.config;
        pendingDisable = false;
        pendingEnable = true;
        sendStatus('third_person_camera', true);

        return {
            ok: true,
            enabled: enabled,
            queued: !enabled,
            message:
                enabled
                    ? '已经启用'
                    : '开启命令已排队'
        };
    }

    function requestDisable() {
        pendingEnable = false;
        pendingDisable = true;
        sendStatus('third_person_camera', false);

        return {
            ok: true,
            enabled: enabled,
            queued: true,
            message: '关闭命令已排队'
        };
    }

    function validateConfig(input) {
        var next = {
            shoulder: 'center',
            distance: config.distance,
            pivotHeight: config.pivotHeight,
            invertY: config.invertY
        };

        function numberField(
            name,
            minimum,
            maximum
        ) {
            if (input[name] === undefined) {
                return null;
            }

            var value = Number(input[name]);
            if (!isFinite(value) ||
                value < minimum ||
                value > maximum) {
                return name +
                    ' 必须在 ' +
                    minimum +
                    '～' +
                    maximum +
                    ' 之间';
            }

            next[name] = value;
            return null;
        }

        var error = numberField(
            'distance',
            1.5,
            8.0
        );
        if (error) return {
            ok: false,
            error: error
        };

        error = numberField(
            'pivotHeight',
            0.5,
            2.5
        );
        if (error) return {
            ok: false,
            error: error
        };

        if (input.invertY !== undefined) {
            next.invertY = !!input.invertY;
        }

        return {
            ok: true,
            config: next
        };
    }

    function installHooks() {
        /*
         * JavaScript 语法检查不会发现“函数名存在调用但未定义”。
         * 在安装 Hook 前主动检查关键射击函数。
         */
        if (typeof writeRay !== 'function' ||
            typeof buildShotSolutionOnDemand !== 'function' ||
            typeof computeAimTargetForCurrentFrame !== 'function') {
            throw new Error(
                '射击核心函数不完整，拒绝安装 Hook'
            );
        }

        if (installed) {
            return {
                ok: true,
                installed: true
            };
        }

        function attach(name, rva, callbacks) {
            var address = base.add(rva);

            if (!isExecutable(address)) {
                throw new Error(
                    name +
                    ' 地址不可执行: ' +
                    address
                );
            }

            var listener = Interceptor.attach(
                address,
                callbacks
            );

            listeners.push(listener);

            sendLog('info', 'Hook 已安装: ' + name, {
                rva: '0x' + rva.toString(16),
                runtime: address.toString()
            });
        }

        try {
            attach(
                'CameraManager.Awake',
                RVA.CameraManager_Awake,
                {
                    onEnter: function (args) {
                        cacheCameraManager(
                            args[0],
                            'CameraManager.Awake'
                        );
                    }
                }
            );

            attach(
                'CameraManager.Update',
                RVA.CameraManager_Update,
                {
                    onLeave: function () {
                        var perfStart = perfClock.now();

                        try {
                            processCommands();
                            updateRuntimeMainThread();
                        } finally {
                            recordPerfMetric(
                                perf.metrics.cmUpdate,
                                perfClock.now() - perfStart
                            );

                            noteGameFrame();
                        }
                    }
                }
            );

            attach(
                'CinemachineBrain.PushStateToUnityCamera',
                RVA.Brain_PushStateToUnityCamera,
                {
                    onEnter: function (args) {
                        this.brain = args[0];
                    },
                    onLeave: function () {
                        perf.pushStateCalls++;
                        perf.windowPushStateCalls++;
                        perf.pushStreak++;

                        if (!enabled) return;

                        /*
                         * 顺序不能交换：
                         * 先应用独立俯仰，再采样最终 Camera，
                         * 射击和 WASD 才会使用真正的镜头方向。
                         */
                        var perfStart = perfClock.now();

                        try {
                            updateFinalCamera(this.brain);
                        } finally {
                            recordPerfMetric(
                                perf.metrics.finalCamera,
                                perfClock.now() - perfStart
                            );
                        }
                    }
                }
            );

            /*
             * 相机相对 WASD：
             * Hook 返回 Vector3 的辅助函数，只修改最终水平速度方向。
             * 不再在热路径调用 Transform.get/set_rotation。
             */
            attach(
                'Player.GetWalkVelocity',
                RVA.Player_GetWalkVelocity,
                {
                    onEnter: function (args) {
                        this.returnBuffer = args[0];
                        this.player = args[1];
                        this.displayClass = args[2];
                    },
                    onLeave: function () {
                        var perfStart = perfClock.now();

                        try {
                            rotateWalkVelocityToCamera(
                                this.returnBuffer,
                                this.player,
                                this.displayClass
                            );
                        } finally {
                            recordPerfMetric(
                                perf.metrics.walkVelocity,
                                perfClock.now() - perfStart
                            );
                        }
                    }
                }
            );

            /*
             * 相机输入与人物 Yaw 分离：
             * 1. onEnter 只保存 Player；
             * 2. 原函数正常处理鼠标上下左右；
             * 3. onLeave 读取本帧最新 Pitch；
             * 4. 最后只平滑覆盖水平 Yaw。
             */
            attach(
                'Player.UpdateCameraRotaion',
                RVA.Player_UpdateCameraRotaion,
                {
                    onEnter: function (args) {
                        this.player = args[0];
                    },
                    onLeave: function () {
                        var perfStart = perfClock.now();

                        try {
                            handleCameraInputAndBodyYaw(
                                this.player
                            );
                        } finally {
                            recordPerfMetric(
                                perf.metrics.cameraInput,
                                perfClock.now() - perfStart
                            );
                        }
                    }
                }
            );

            attach(
                'Recoil.GetShootRay',
                RVA.Recoil_GetShootRay,
                {
                    onEnter: function (args) {
                        this.retBuffer = args[0];
                        this.localShot = false;

                        if (!enabled ||
                            runtime.playerDead ||
                            isNull(localPlayer)) {
                            return;
                        }

                        try {
                            var localRecoil = localPlayer.add(
                                OFF.Player_recoil
                            ).readPointer();

                            this.localShot =
                                !isNull(localRecoil) &&
                                localRecoil.equals(args[1]);
                        } catch (_) {
                        }
                    },
                    onLeave: function () {
                        if (!enabled || !this.localShot) return;

                        stats.shootRayCalls++;

                        // 只有真实开枪时才读取枪口并做 Physics Raycast。
                        if (!buildShotSolutionOnDemand()) {
                            stats.shootRayFailures++;
                            return;
                        }

                        if (!writeRay(
                            this.retBuffer,
                            runtime.shootRay.origin,
                            runtime.shootRay.direction
                        )) {
                            stats.shootRayFailures++;
                            return;
                        }

                        stats.shootRayModified++;

                        /*
                         * 第一发和每 250 发记录一次。
                         * 不再输出 HUD 坐标，也不序列化向量对象。
                         */
                        if (stats.shootRayModified === 1 ||
                            stats.shootRayModified % 250 === 0) {
                            sendLog(
                                'info',
                                '[Shooting] 双射线已写回',
                                {
                                    shot:
                                        stats.shootRayModified,
                                    source:
                                        'camera_center',
                                    targetReusedSameFrame:
                                        runtime.aimSolution.reusedLast,
                                    physicsCalls:
                                        stats.physicsRaycastCalls,
                                    aimFrames:
                                        stats.aimFramesComputed,
                                    sameFrameReuses:
                                        stats.sameFrameAimReuses
                                }
                            );
                        }
                    }
                }
            );

            attach(
                'Player.SetWeapon',
                RVA.Player_SetWeapon,
                {
                    onEnter: function (args) {
                        this.player = args[0];
                    },
                    onLeave: function () {
                        if (!isLocalPlayer(
                            this.player
                        )) {
                            return;
                        }

                        scheduleRefresh(
                            'set_weapon',
                            true,
                            false,
                            true,
                            LIMITS.lifecycleWeaponDelayMs
                        );
                    }
                }
            );

            attach(
                'Player.OnEntityDeath',
                RVA.Player_OnEntityDeath,
                {
                    onEnter: function (args) {
                        this.player = args[0];
                    },
                    onLeave: function () {
                        if (!isLocalPlayer(
                            this.player
                        )) {
                            return;
                        }

                        runtime.playerDead = true;
                        resetRefreshQueue();
                        clearMuzzleCache(null);
                        invalidateAimSolution();
                    }
                }
            );

            attach(
                'Player.Respawn',
                RVA.Player_Respawn,
                {
                    onEnter: function (args) {
                        this.player = args[0];
                    },
                    onLeave: function () {
                        if (!isLocalPlayer(
                            this.player
                        )) {
                            return;
                        }

                        runtime.playerDead = false;
                        scheduleRefresh(
                            'respawn',
                            true,
                            true,
                            true,
                            LIMITS.lifecycleSpawnDelayMs
                        );
                    }
                }
            );

            attach(
                'Player.Spawn',
                RVA.Player_Spawn,
                {
                    onEnter: function (args) {
                        this.player = args[0];
                    },
                    onLeave: function () {
                        if (!isLocalPlayer(
                            this.player
                        )) {
                            return;
                        }

                        runtime.playerDead = false;
                        scheduleRefresh(
                            'spawn',
                            true,
                            true,
                            true,
                            LIMITS.lifecycleSpawnDelayMs
                        );
                    }
                }
            );

            attach(
                'CameraManager.ChangePVandCV',
                RVA.CameraManager_ChangePVandCV,
                {
                    onEnter: function (args) {
                        cacheCameraManager(
                            args[0],
                            'CameraManager.ChangePVandCV'
                        );
                    },
                    onLeave: function () {
                        if (!enabled) return;

                        scheduleRefresh(
                            'change_pv_cv',
                            true,
                            true,
                            true,
                            LIMITS.lifecycleCameraDelayMs
                        );
                    }
                }
            );

            attach(
                'CameraManager.OnDestroy',
                RVA.CameraManager_OnDestroy,
                {
                    onEnter: function (args) {
                        if (isNull(cameraManager) ||
                            !args[0].equals(
                                cameraManager
                            )) {
                            return;
                        }

                        enabled = false;
                        sessionDestroyed = true;
                        pendingEnable = false;
                        pendingDisable = false;
                        resetRefreshQueue();

                        cameraManager = null;
                        localPlayer = null;

                        resetRuntime();
                        resetSavedState();
                        setState(STATE.NO_GAME);

                        sendPluginEvent('session_destroyed', {
                            reason: 'CameraManager.OnDestroy'
                        });
                    }
                }
            );

            attach(
                'GameManager.Awake',
                RVA.GameManager_Awake,
                {
                    onEnter: function (args) {
                        gameManager = args[0];
                        localPlayer = null;
                        setState(STATE.READY);
                    }
                }
            );

            attach(
                'GameManager.OnDestroy',
                RVA.GameManager_OnDestroy,
                {
                    onEnter: function (args) {
                        if (isNull(gameManager) ||
                            !args[0].equals(
                                gameManager
                            )) {
                            return;
                        }

                        enabled = false;
                        resetRefreshQueue();
                        gameManager = null;
                        localPlayer = null;
                        cameraManager = null;

                        resetRuntime();
                        resetSavedState();
                        setState(STATE.NO_GAME);
                    }
                }
            );

            attach(
                'MapManager.NewGameRoundStart',
                RVA.MapManager_NewGameRoundStart,
                {
                    onEnter: function () {
                        localPlayer = null;

                        if (enabled) {
                            scheduleRefresh(
                                'new_round',
                                true,
                                true,
                                true,
                                250
                            );
                        } else {
                            setState(STATE.READY);
                        }
                    }
                }
            );

            installed = true;
            sendLog(
                'info',
                '最小可用第三人称射击 v3.14-owner-perf Hook 安装完成'
            );

            return {
                ok: true,
                installed: true
            };
        } catch (error) {
            sendLog(
                'error',
                'Hook 安装失败: ' + error
            );

            // P1：部分安装失败时把已挂的 listener 回滚，避免再次 enable 时重复 attach
            for (var index = 0; index < listeners.length; index++) {
                try { listeners[index].detach(); } catch (_) {}
            }
            listeners = [];
            installed = false;

            return {
                ok: false,
                error: String(error)
            };
        }
    }

    function cleanup(payload) {
        var reason =
            payload && payload.reason
                ? payload.reason
                : 'cleanup';
        var wasEnabled = enabled;
        var disableResult = null;

        pendingEnable = false;
        resetRefreshQueue();

        if (enabled) {
            try {
                disableResult = performDisable();
            } catch (error) {
                stats.errors++;
                enabled = false;
                pendingDisable = false;
                sendLog(
                    'error',
                    'cleanup 同步关闭失败: ' + error
                );
                sendPluginEvent('runtime_error', {
                    message: 'cleanup 同步关闭失败: ' + error,
                    reason: reason
                });
            }
        }

        enabled = false;
        pendingDisable = false;

        for (var index = 0;
             index < listeners.length;
             index++) {
            try {
                listeners[index].detach();
            } catch (_) {
            }
        }

        listeners = [];
        installed = false;
        resetRuntime();
        resetSavedState();

        if (wasEnabled && disableResult === null) {
            sendPluginEvent('disabled', {
                reason: reason,
                ok: true,
                enabled: false
            });
        }

        return {
            ok: true,
            enabled: false,
            reason: reason
        };
    }

    rpc.exports = {
        enable: requestEnable,
        disable: requestDisable,

        setConfig: function (input) {
            var validation = validateConfig(input || {});
            if (!validation.ok) return validation;

            config = validation.config;
            invalidateAimSolution();

            if (enabled) {
                scheduleRefresh(
                    'config_changed',
                    false,
                    true,
                    false,
                    0
                );
            }

            sendPluginEvent('config_applied', {
                config: config,
                queued: enabled
            });

            return {
                ok: true,
                queued: enabled,
                config: config,
                message: enabled
                    ? '相机参数将在主线程重新应用'
                    : '参数已保存'
            };
        },

        status: function () {
            return {
                ok: true,
                installed: installed,
                enabled: enabled,
                pendingEnable: pendingEnable,
                pendingDisable: pendingDisable,
                sessionDestroyed: sessionDestroyed,
                state: state,
                haveGameManager:
                    !isNull(gameManager) &&
                    isReadable(gameManager),
                haveCameraManager:
                    !isNull(cameraManager) &&
                    isReadable(cameraManager),
                haveLocalPlayer:
                    !isNull(localPlayer) &&
                    isReadable(localPlayer),
                config: config,
                stats: stats,
                runtime: {
                    playerDead: runtime.playerDead,
                    camera: {
                        valid: runtime.camera.valid,
                        yaw: runtime.camera.yaw,
                        pitch: runtime.camera.pitch,
                        inputPitch:
                            runtime.cameraInput.pitch,
                        yawSource:
                            'transform_forward_stable'
                    },
                    muzzle: {
                        valid: runtime.muzzle.valid,
                        source: runtime.muzzle.source,
                        ownerChecks:
                            stats.muzzleOwnerChecks,
                        ownerMismatches:
                            stats.muzzleOwnerMismatches,
                        staleInvalidations:
                            stats.staleMuzzleInvalidations
                    },
                    safeRestore: {
                        skips:
                            stats.safeRestoreSkips,
                        rebinds:
                            stats.safeRestoreRebinds,
                        stalePointers:
                            stats.stalePointerSkips,
                        staleCameraResets:
                            stats.staleCameraResets,
                        cameraHealthChecks:
                            stats.cameraCacheHealthChecks,
                        hotPathReadableChecksRemoved:
                            stats.hotPathReadableChecksRemoved
                    },
                    shootRay: {
                        valid:
                            runtime.shootRay.valid,
                        aimSource:
                            runtime.shootRay.aimSource,
                        targetReusedSameFrame:
                            runtime.aimSolution.reusedLast
                    },
                    aimSolution: {
                        valid:
                            runtime.aimSolution.valid,
                        frameId:
                            runtime.aimSolution.frameId
                    },
                    refreshQueue: {
                        pending:
                            refreshQueue.pending,
                        eventCount:
                            refreshQueue.eventCount,
                        lastReason:
                            refreshQueue.lastReason
                    }
                },
                design: {
                    camera:
                        'single-pass final camera pivot',
                    movement:
                        'camera-relative returned velocity',
                    shooting:
                        'camera center ray -> world target -> live muzzle ray',
                    muzzleCache:
                        'validate cached weapon against localPlayer.wpns.inUse before reuse',
                    safeShutdown:
                        'restore current player/camera objects only; never call saved stale weapon/character',
                    hotPathPerformance:
                        'no per-frame isReadable; camera cache health checked at low frequency',
                    aimAuthority:
                        'gameplay camera is authoritative; HUD is presentation only',
                    aimReuse:
                        'same final-camera frame only',
                    cameraSetup:
                        'Follow + LookAt + one-time YAxis lock',
                    horizontalYaw:
                        'always derived from final Camera Transform.forward',
                    lifecycle:
                        'debounced event batch on main thread'
                }
            };
        },

        cleanup: cleanup
    };

    rpc.exports.setconfig = rpc.exports.setConfig;
    rpc.exports.getstatus = rpc.exports.status;

    var installResult = installHooks();

    sendPluginEvent(
        installResult.ok ? 'runtime_ready' : 'runtime_error',
        installResult.ok
            ? {
                installed: true
            }
            : {
                message:
                    installResult.error ||
                    '脚本加载失败',
                installResult: installResult
            }
    );

    sendLog(
        installResult.ok
            ? 'info'
            : 'error',
        installResult.ok
            ? '最小可用第三人称射击 v3.14-owner-perf 脚本已加载'
            : '脚本加载失败',
        {
            base: base.toString(),
            arch: Process.arch,
            pointerSize:
                Process.pointerSize,
            installResult:
                installResult
        }
    );
})();
