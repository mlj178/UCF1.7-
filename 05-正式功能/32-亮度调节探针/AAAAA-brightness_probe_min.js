// ============================================================
// AAAAA-brightness_probe_min.js
//
// feature_id: "brightness_probe"
// 功能目标：验证游戏运行时是否可以通过 URP ColorAdjustments.postExposure
//          真实调节画面亮度/曝光。
//
// 实现原理：
//   1. 获取 UnityEngine.Camera.main。
//   2. 通过 CameraExtensions.GetUniversalAdditionalCameraData 读取 URP 相机数据。
//   3. 从 UniversalAdditionalCameraData.volumeStack 获取 ColorAdjustments。
//   4. 直接读写 ColorAdjustments.postExposure 的 VolumeParameter<float>。
//
// RVA / 字段来源：
//   Camera_get_main: 0x00328310
//   CameraExtensions_GetUniversalAdditionalCameraData: 0x00490500
//   CameraExtensions_UpdateVolumeStack: 0x00490820
//   VolumeStack_GetComponent_ColorAdjustments: 0x007D3570
//   MethodInfo_VolumeStack_GetComponent_ColorAdjustments: 0x00E24EEC
//   VolumeStack_GetComponent_LiftGammaGain: 0x007D3570
//   MethodInfo_VolumeStack_GetComponent_LiftGammaGain: 0x00E24FE8
//   CameraManager_TypeInfo: 0x00E263C0
//   UniversalAdditionalCameraData_renderPostProcessing: 0x30
//   UniversalAdditionalCameraData_volumeStack: 0x4C
//   CameraManager_volumeProfile: 0x10
//   VolumeProfile_components: 0x0C
//   List_items: 0x08
//   ColorAdjustments_postExposure: 0x1C
//   ColorAdjustments_contrast: 0x20
//   ColorAdjustments_saturation: 0x2C
//   LiftGammaGain_gamma: 0x20
//   LiftGammaGain_gain: 0x24
//   VolumeParameter_overrideState: 0x08
//   VolumeParameter_floatValue: 0x0C
//
// 注意：
//   这是探针，不是正式功能。写入能读回只证明参数层可控，
//   最终是否影响画面仍需在游戏内目测确认。
// ============================================================

(function () {
    "use strict";

    var MODULE_NAME = "GameAssembly.dll";
    var CALL_CONV = "mscdecl";

    var RVA = {
        Camera_get_main: 0x00328310,
        CameraExtensions_GetUniversalAdditionalCameraData: 0x00490500,
        CameraExtensions_UpdateVolumeStack: 0x00490820,
        VolumeStack_GetComponent_ColorAdjustments: 0x007D3570,
        MethodInfo_VolumeStack_GetComponent_ColorAdjustments: 0x00E24EEC,
        VolumeStack_GetComponent_LiftGammaGain: 0x007D3570,
        MethodInfo_VolumeStack_GetComponent_LiftGammaGain: 0x00E24FE8,
        CameraManager_TypeInfo: 0x00E263C0
    };

    var OFF = {
        Il2CppClass_static_fields: 0x5C,
        UniversalAdditionalCameraData_renderPostProcessing: 0x30,
        UniversalAdditionalCameraData_volumeStack: 0x4C,
        CameraManager_volumeProfile: 0x10,
        VolumeProfile_components: 0x0C,
        List_items: 0x08,
        List_size: 0x0C,
        Array_length: 0x0C,
        Array_items: 0x10,
        ColorAdjustments_postExposure: 0x1C,
        ColorAdjustments_contrast: 0x20,
        ColorAdjustments_saturation: 0x2C,
        LiftGammaGain_gamma: 0x20,
        LiftGammaGain_gain: 0x24,
        VolumeParameter_overrideState: 0x08,
        VolumeParameter_floatValue: 0x0C
    };

    var Runtime = {
        feature_id: "brightness_probe",
        enabled: false,
        initialized: false,
        generation: 0,
        hooks: [],
        timers: [],
        config: {
            exposure: 1.5,
            contrast: 0.0,
            saturation: 0.0,
            gamma: 0.0,
            gain: 0.0,
            force_render_post_processing: false,
            update_volume_stack: true
        },
        cache: {
            camera: ptr(0),
            additionalCameraData: ptr(0),
            volumeStack: ptr(0),
            colorAdjustments: ptr(0),
            liftGammaGain: ptr(0),
            postExposureParam: ptr(0),
            contrastParam: ptr(0),
            saturationParam: ptr(0),
            gammaParam: ptr(0),
            gainParam: ptr(0)
        },
        originals: {},
        stats: {
            applyCount: 0,
            resetCount: 0,
            cleanupCount: 0,
            errorCount: 0,
            lastError: "",
            lastResetReason: "",
            lastApplyResult: ""
        },
        lastStatus: {}
    };

    var native = {
        ready: false,
        cameraGetMain: null,
        getAdditionalCameraData: null,
        updateVolumeStack: null,
        volumeStackGetColorAdjustments: null,
        volumeStackGetLiftGammaGain: null
    };

    var LogLimiter = {};

    function log(level, message) {
        var text = "[" + Runtime.feature_id + "] " + message;
        if (level === "error") console.error(text);
        else if (level === "warn") console.warn(text);
        else console.log(text);
        try {
            send({ type: "log", level: level, message: message });
        } catch (e) {}
    }

    function logOnce(key, level, message, intervalMs) {
        var now = Date.now();
        var wait = intervalMs || 1200;
        if (!LogLimiter[key] || now - LogLimiter[key] >= wait) {
            LogLimiter[key] = now;
            log(level, message);
        }
    }

    function setError(message, error) {
        Runtime.stats.errorCount += 1;
        Runtime.stats.lastError = message + (error ? ": " + error.message : "");
        logOnce("error:" + message, "error", Runtime.stats.lastError, 1500);
    }

    function isNull(p) {
        return !p || p.isNull();
    }

    function isReadablePtr(p) {
        try {
            if (isNull(p)) return false;
            p.readPointer();
            return true;
        } catch (e) {
            return false;
        }
    }

    function ptrText(p) {
        return isNull(p) ? "0x0" : p.toString();
    }

    function readIl2CppClassName(obj) {
        try {
            if (!isReadablePtr(obj)) return "";
            var klass = obj.readPointer();
            if (!isReadablePtr(klass)) return "";
            var namePtr = klass.add(0x08).readPointer();
            if (isNull(namePtr)) return "";
            return namePtr.readCString();
        } catch (error) {
            return "";
        }
    }

    function readListInfo(listPtr) {
        if (!isReadablePtr(listPtr)) {
            return { ptr: ptrText(listPtr), items: "0x0", arrayLength: null, size: null };
        }
        try {
            var items = listPtr.add(OFF.List_items).readPointer();
            var arrayLength = isReadablePtr(items) ? items.add(OFF.Array_length).readS32() : null;
            return {
                ptr: ptrText(listPtr),
                items: ptrText(items),
                arrayLength: arrayLength,
                size: listPtr.add(OFF.List_size).readS32()
            };
        } catch (error) {
            setError("readListInfo failed", error);
            return { ptr: ptrText(listPtr), items: "0x0", arrayLength: null, size: null };
        }
    }

    function readListElement(listPtr, index) {
        if (!isReadablePtr(listPtr)) return ptr(0);
        var items = listPtr.add(OFF.List_items).readPointer();
        if (!isReadablePtr(items)) return ptr(0);
        return items.add(OFF.Array_items + index * Process.pointerSize).readPointer();
    }

    function initNativeFunctions() {
        if (native.ready) return true;

        var mod = Process.findModuleByName(MODULE_NAME);
        if (!mod) {
            Runtime.stats.lastError = MODULE_NAME + " not found";
            return false;
        }

        if (Process.arch !== "ia32" || Process.pointerSize !== 4) {
            Runtime.stats.lastError = "unsupported process: arch=" + Process.arch + ", pointerSize=" + Process.pointerSize;
            log("error", Runtime.stats.lastError);
            return false;
        }

        try {
            native.cameraGetMain = new NativeFunction(
                mod.base.add(RVA.Camera_get_main),
                "pointer",
                ["pointer"],
                CALL_CONV
            );
            native.getAdditionalCameraData = new NativeFunction(
                mod.base.add(RVA.CameraExtensions_GetUniversalAdditionalCameraData),
                "pointer",
                ["pointer", "pointer"],
                CALL_CONV
            );
            native.updateVolumeStack = new NativeFunction(
                mod.base.add(RVA.CameraExtensions_UpdateVolumeStack),
                "void",
                ["pointer", "pointer"],
                CALL_CONV
            );
            native.volumeStackGetColorAdjustments = new NativeFunction(
                mod.base.add(RVA.VolumeStack_GetComponent_ColorAdjustments),
                "pointer",
                ["pointer", "pointer"],
                CALL_CONV
            );
            native.volumeStackGetLiftGammaGain = new NativeFunction(
                mod.base.add(RVA.VolumeStack_GetComponent_LiftGammaGain),
                "pointer",
                ["pointer", "pointer"],
                CALL_CONV
            );
            native.methodInfoColorAdjustments = mod.base.add(RVA.MethodInfo_VolumeStack_GetComponent_ColorAdjustments);
            native.methodInfoLiftGammaGain = mod.base.add(RVA.MethodInfo_VolumeStack_GetComponent_LiftGammaGain);
            native.ready = true;
            Runtime.initialized = true;
            log("info", "native functions ready");
            return true;
        } catch (error) {
            setError("initNativeFunctions failed", error);
            native.ready = false;
            return false;
        }
    }

    function readBoolField(base, offset) {
        try {
            if (!isReadablePtr(base)) return null;
            return base.add(offset).readU8() !== 0;
        } catch (e) {
            return null;
        }
    }

    function writeBoolField(base, offset, value) {
        if (!isReadablePtr(base)) return false;
        base.add(offset).writeU8(value ? 1 : 0);
        return true;
    }

    function readFloatParam(param) {
        try {
            if (!isReadablePtr(param)) return null;
            return {
                ptr: ptrText(param),
                value: param.add(OFF.VolumeParameter_floatValue).readFloat(),
                overrideState: param.add(OFF.VolumeParameter_overrideState).readU8() !== 0
            };
        } catch (error) {
            setError("readFloatParam failed", error);
            return null;
        }
    }

    function readVector4Param(param) {
        try {
            if (!isReadablePtr(param)) return null;
            return {
                ptr: ptrText(param),
                x: param.add(OFF.VolumeParameter_floatValue).readFloat(),
                y: param.add(OFF.VolumeParameter_floatValue + 4).readFloat(),
                z: param.add(OFF.VolumeParameter_floatValue + 8).readFloat(),
                w: param.add(OFF.VolumeParameter_floatValue + 12).readFloat(),
                overrideState: param.add(OFF.VolumeParameter_overrideState).readU8() !== 0
            };
        } catch (error) {
            setError("readVector4Param failed", error);
            return null;
        }
    }

    function rememberOriginalParam(name, param) {
        if (!isReadablePtr(param)) return;
        if (Runtime.originals[name]) return;
        var current = readFloatParam(param);
        if (!current) return;
        Runtime.originals[name] = {
            ptr: param,
            value: current.value,
            overrideState: current.overrideState
        };
    }

    function rememberOriginalVector4Param(name, param) {
        if (!isReadablePtr(param)) return;
        if (Runtime.originals[name]) return;
        var current = readVector4Param(param);
        if (!current) return;
        Runtime.originals[name] = {
            ptr: param,
            vector4: true,
            x: current.x,
            y: current.y,
            z: current.z,
            w: current.w,
            overrideState: current.overrideState
        };
    }

    function rememberOriginalBool(name, base, offset) {
        if (!isReadablePtr(base)) return;
        if (Runtime.originals[name]) return;
        Runtime.originals[name] = {
            ptr: base,
            offset: offset,
            value: readBoolField(base, offset)
        };
    }

    function writeFloatParam(name, param, value) {
        if (!isReadablePtr(param)) return false;
        rememberOriginalParam(name, param);
        param.add(OFF.VolumeParameter_floatValue).writeFloat(Number(value));
        param.add(OFF.VolumeParameter_overrideState).writeU8(1);
        return true;
    }

    function writeVector4Param(name, param, wValue) {
        if (!isReadablePtr(param)) return false;
        rememberOriginalVector4Param(name, param);
        var current = readVector4Param(param) || { x: 1.0, y: 1.0, z: 1.0, w: 0.0 };
        param.add(OFF.VolumeParameter_floatValue).writeFloat(current.x);
        param.add(OFF.VolumeParameter_floatValue + 4).writeFloat(current.y);
        param.add(OFF.VolumeParameter_floatValue + 8).writeFloat(current.z);
        param.add(OFF.VolumeParameter_floatValue + 12).writeFloat(Number(wValue));
        param.add(OFF.VolumeParameter_overrideState).writeU8(1);
        return true;
    }

    function describeLiftGammaGain(component) {
        if (!isReadablePtr(component)) return null;
        Runtime.cache.liftGammaGain = component;
        Runtime.cache.gammaParam = component.add(OFF.LiftGammaGain_gamma).readPointer();
        Runtime.cache.gainParam = component.add(OFF.LiftGammaGain_gain).readPointer();
        return {
            ptr: ptrText(component),
            gamma: readVector4Param(Runtime.cache.gammaParam),
            gain: readVector4Param(Runtime.cache.gainParam)
        };
    }

    function locateLiftGammaGain(source) {
        try {
            if (source === "volume_stack" && isReadablePtr(Runtime.cache.volumeStack)) {
                var component = native.volumeStackGetLiftGammaGain(Runtime.cache.volumeStack, native.methodInfoLiftGammaGain);
                if (!isNull(component)) {
                    return {
                        ok: true,
                        source: "volume_stack",
                        liftGammaGain: describeLiftGammaGain(component)
                    };
                }
            }
            var profile = locateProfileComponent("LiftGammaGain");
            if (profile.ok) {
                return {
                    ok: true,
                    source: "camera_manager_volume_profile",
                    liftGammaGain: describeLiftGammaGain(profile.component)
                };
            }
            return { ok: false, source: source || "", reason: profile.reason || "LiftGammaGain not found" };
        } catch (error) {
            setError("locateLiftGammaGain failed", error);
            return { ok: false, source: source || "", reason: Runtime.stats.lastError };
        }
    }

    function readCameraManagerProfileInfo() {
        var result = {
            ok: false,
            reason: "",
            typeInfo: "0x0",
            klass: "0x0",
            staticFields: "0x0",
            volumeProfile: "0x0",
            components: { ptr: "0x0", size: null }
        };

        try {
            var mod = Process.findModuleByName(MODULE_NAME);
            if (!mod) {
                result.reason = MODULE_NAME + " not found";
                return result;
            }

            var typeInfoSlot = mod.base.add(RVA.CameraManager_TypeInfo);
            result.typeInfo = ptrText(typeInfoSlot);
            var klass = typeInfoSlot.readPointer();
            result.klass = ptrText(klass);
            if (!isReadablePtr(klass)) {
                result.reason = "CameraManager klass unreadable";
                return result;
            }

            var staticFields = klass.add(OFF.Il2CppClass_static_fields).readPointer();
            result.staticFields = ptrText(staticFields);
            if (!isReadablePtr(staticFields)) {
                result.reason = "CameraManager static_fields unreadable";
                return result;
            }

            var profile = staticFields.add(OFF.CameraManager_volumeProfile).readPointer();
            result.volumeProfile = ptrText(profile);
            if (isNull(profile)) {
                result.reason = "CameraManager.volumeProfile is null";
                return result;
            }

            var components = profile.add(OFF.VolumeProfile_components).readPointer();
            result.components = readListInfo(components);
            result.ok = true;
            result.reason = "CameraManager.volumeProfile readable";
            return result;
        } catch (error) {
            result.reason = "readCameraManagerProfileInfo failed: " + error.message;
            setError("readCameraManagerProfileInfo failed", error);
            return result;
        }
    }

    function withCameraManagerProfileInfo(result) {
        result.cameraManagerVolumeProfile = readCameraManagerProfileInfo();
        return result;
    }

    function locateProfileComponent(targetName) {
        var result = {
            ok: false,
            reason: "",
            component: ptr(0),
            componentNames: [],
            profileComponents: null,
            cameraManagerVolumeProfile: {}
        };

        try {
            var profileInfo = readCameraManagerProfileInfo();
            result.cameraManagerVolumeProfile = profileInfo;
            if (!profileInfo.ok) {
                result.reason = profileInfo.reason || "CameraManager.volumeProfile unavailable";
                return result;
            }

            var profile = ptr(profileInfo.volumeProfile);
            var componentsList = profile.add(OFF.VolumeProfile_components).readPointer();
            var profileComponents = readListInfo(componentsList);
            result.profileComponents = profileComponents;
            var size = Number(profileComponents.size);
            var arrayLength = Number(profileComponents.arrayLength);
            if (!isFinite(size) || size <= 0 || !isFinite(arrayLength) || arrayLength <= 0) {
                result.reason = "VolumeProfile.components is empty";
                return result;
            }

            var limit = Math.min(size, arrayLength, 64);
            for (var i = 0; i < limit; i++) {
                var component = readListElement(componentsList, i);
                if (isNull(component)) continue;
                var componentName = readIl2CppClassName(component);
                if (componentName) result.componentNames.push(componentName);
                if (componentName === targetName) {
                    result.ok = true;
                    result.reason = targetName + " located via CameraManager.volumeProfile";
                    result.component = component;
                    result.componentIndex = i;
                    return result;
                }
            }

            result.reason = targetName + " not found in CameraManager.volumeProfile";
            return result;
        } catch (error) {
            setError("locateProfileComponent failed", error);
            result.reason = Runtime.stats.lastError;
            return result;
        }
    }

    function locateProfileColorAdjustments(previousResult) {
        var result = {
            ok: false,
            source: "camera_manager_volume_profile",
            reason: "",
            previous: previousResult || null,
            cameraManagerVolumeProfile: {},
            profileComponents: null,
            componentNames: []
        };

        try {
            var profileInfo = readCameraManagerProfileInfo();
            result.cameraManagerVolumeProfile = profileInfo;
            if (!profileInfo.ok) {
                result.reason = profileInfo.reason || "CameraManager.volumeProfile unavailable";
                return result;
            }

            var profile = ptr(profileInfo.volumeProfile);
            var componentsList = profile.add(OFF.VolumeProfile_components).readPointer();
            var profileComponents = readListInfo(componentsList);
            result.profileComponents = profileComponents;
            var size = Number(profileComponents.size);
            var arrayLength = Number(profileComponents.arrayLength);
            if (!isFinite(size) || size <= 0 || !isFinite(arrayLength) || arrayLength <= 0) {
                result.reason = "VolumeProfile.components is empty";
                return result;
            }

            var limit = Math.min(size, arrayLength, 64);
            var colorAdjustments = ptr(0);
            var liftGammaGain = ptr(0);
            for (var i = 0; i < limit; i++) {
                var component = readListElement(componentsList, i);
                if (isNull(component)) continue;
                var componentName = readIl2CppClassName(component);
                if (componentName) result.componentNames.push(componentName);
                if (componentName === "ColorAdjustments") {
                    colorAdjustments = component;
                    result.componentIndex = i;
                }
                if (componentName === "LiftGammaGain") {
                    liftGammaGain = component;
                    result.liftGammaGainIndex = i;
                }
            }

            if (!isNull(colorAdjustments)) {
                Runtime.cache.volumeStack = ptr(0);
                Runtime.cache.colorAdjustments = colorAdjustments;
                Runtime.cache.postExposureParam = colorAdjustments.add(OFF.ColorAdjustments_postExposure).readPointer();
                Runtime.cache.contrastParam = colorAdjustments.add(OFF.ColorAdjustments_contrast).readPointer();
                Runtime.cache.saturationParam = colorAdjustments.add(OFF.ColorAdjustments_saturation).readPointer();
                result.ok = true;
                result.reason = "ColorAdjustments located via CameraManager.volumeProfile";
                result.colorAdjustments = ptrText(colorAdjustments);
                result.postExposure = readFloatParam(Runtime.cache.postExposureParam);
                result.contrast = readFloatParam(Runtime.cache.contrastParam);
                result.saturation = readFloatParam(Runtime.cache.saturationParam);
                if (!isNull(liftGammaGain)) result.liftGammaGain = describeLiftGammaGain(liftGammaGain);
                return result;
            }

            result.reason = "ColorAdjustments not found in CameraManager.volumeProfile";
            return result;
        } catch (error) {
            setError("locateProfileColorAdjustments failed", error);
            result.reason = Runtime.stats.lastError;
            return result;
        }
    }

    function fallbackToProfile(previousResult) {
        var profileResult = locateProfileColorAdjustments(previousResult);
        if (profileResult.ok) return profileResult;
        previousResult.profileFallback = profileResult;
        return withCameraManagerProfileInfo(previousResult);
    }

    function setConfig(config) {
        Runtime.config = Object.assign(Runtime.config, config || {});
        log("info", "config changed: exposure=" + Runtime.config.exposure + ", forcePost=" + Runtime.config.force_render_post_processing);
        return buildStatus(Runtime.lastStatus || {});
    }

    function resetRuntime(reason) {
        Runtime.generation += 1;
        Runtime.cache.camera = ptr(0);
        Runtime.cache.additionalCameraData = ptr(0);
        Runtime.cache.volumeStack = ptr(0);
        Runtime.cache.colorAdjustments = ptr(0);
        Runtime.cache.liftGammaGain = ptr(0);
        Runtime.cache.postExposureParam = ptr(0);
        Runtime.cache.contrastParam = ptr(0);
        Runtime.cache.saturationParam = ptr(0);
        Runtime.cache.gammaParam = ptr(0);
        Runtime.cache.gainParam = ptr(0);
        Runtime.stats.lastResetReason = reason || "unknown";
        logOnce("reset", "info", "resetRuntime: " + Runtime.stats.lastResetReason + ", gen=" + Runtime.generation, 500);
    }

    function locateColorAdjustments(allowStackUpdate) {
        if (!initNativeFunctions()) {
            return withCameraManagerProfileInfo({ ok: false, reason: Runtime.stats.lastError || "native not ready" });
        }

        var camera = ptr(0);
        var additional = ptr(0);
        var stack = ptr(0);
        var colorAdjustments = ptr(0);

        try {
            camera = native.cameraGetMain(ptr(0));
            Runtime.cache.camera = camera;
            if (isNull(camera)) return fallbackToProfile({ ok: false, reason: "Camera.main is null", camera: ptrText(camera) });

            additional = native.getAdditionalCameraData(camera, ptr(0));
            Runtime.cache.additionalCameraData = additional;
            if (isNull(additional)) return fallbackToProfile({ ok: false, reason: "UniversalAdditionalCameraData is null", camera: ptrText(camera) });

            if (allowStackUpdate && Runtime.config.update_volume_stack) {
                try {
                    native.updateVolumeStack(camera, ptr(0));
                } catch (e) {
                    setError("UpdateVolumeStack failed", e);
                }
            }

            stack = additional.add(OFF.UniversalAdditionalCameraData_volumeStack).readPointer();
            Runtime.cache.volumeStack = stack;
            if (isNull(stack)) {
                return fallbackToProfile({
                    ok: false,
                    reason: "volumeStack is null",
                    camera: ptrText(camera),
                    additionalCameraData: ptrText(additional),
                    renderPostProcessing: readBoolField(additional, OFF.UniversalAdditionalCameraData_renderPostProcessing)
                });
            }

            colorAdjustments = native.volumeStackGetColorAdjustments(stack, native.methodInfoColorAdjustments);
            Runtime.cache.colorAdjustments = colorAdjustments;
            if (isNull(colorAdjustments)) {
                return fallbackToProfile({
                    ok: false,
                    reason: "ColorAdjustments component is null",
                    camera: ptrText(camera),
                    additionalCameraData: ptrText(additional),
                    volumeStack: ptrText(stack),
                    renderPostProcessing: readBoolField(additional, OFF.UniversalAdditionalCameraData_renderPostProcessing)
                });
            }

            Runtime.cache.postExposureParam = colorAdjustments.add(OFF.ColorAdjustments_postExposure).readPointer();
            Runtime.cache.contrastParam = colorAdjustments.add(OFF.ColorAdjustments_contrast).readPointer();
            Runtime.cache.saturationParam = colorAdjustments.add(OFF.ColorAdjustments_saturation).readPointer();

            var located = {
                ok: true,
                source: "volume_stack",
                reason: "ColorAdjustments located",
                camera: ptrText(camera),
                additionalCameraData: ptrText(additional),
                volumeStack: ptrText(stack),
                colorAdjustments: ptrText(colorAdjustments),
                renderPostProcessing: readBoolField(additional, OFF.UniversalAdditionalCameraData_renderPostProcessing),
                postExposure: readFloatParam(Runtime.cache.postExposureParam),
                contrast: readFloatParam(Runtime.cache.contrastParam),
                saturation: readFloatParam(Runtime.cache.saturationParam)
            };
            var liftGammaGain = locateLiftGammaGain("volume_stack");
            if (liftGammaGain.ok) located.liftGammaGain = liftGammaGain.liftGammaGain;
            else located.liftGammaGain = liftGammaGain;
            return withCameraManagerProfileInfo(located);
        } catch (error) {
            setError("locateColorAdjustments failed", error);
            return withCameraManagerProfileInfo({ ok: false, reason: Runtime.stats.lastError });
        }
    }

    function applyBrightness(value) {
        Runtime.stats.applyCount += 1;
        var exposure = Number(value);
        if (!isFinite(exposure)) exposure = Number(Runtime.config.exposure);
        if (!isFinite(exposure)) exposure = 1.5;

        var result = locateColorAdjustments(true);
        if (!result.ok) {
            Runtime.stats.lastApplyResult = "apply failed: " + result.reason;
            log("warn", Runtime.stats.lastApplyResult);
            return buildStatus(result);
        }

        try {
            if (Runtime.config.force_render_post_processing && isReadablePtr(Runtime.cache.additionalCameraData)) {
                rememberOriginalBool(
                    "renderPostProcessing",
                    Runtime.cache.additionalCameraData,
                    OFF.UniversalAdditionalCameraData_renderPostProcessing
                );
                writeBoolField(Runtime.cache.additionalCameraData, OFF.UniversalAdditionalCameraData_renderPostProcessing, true);
            }

            var wroteExposure = writeFloatParam("postExposure", Runtime.cache.postExposureParam, exposure);
            var wroteContrast = writeFloatParam("contrast", Runtime.cache.contrastParam, Number(Runtime.config.contrast));
            var wroteSaturation = writeFloatParam("saturation", Runtime.cache.saturationParam, Number(Runtime.config.saturation));
            var wroteGamma = writeVector4Param("gamma", Runtime.cache.gammaParam, Number(Runtime.config.gamma));
            var wroteGain = writeVector4Param("gain", Runtime.cache.gainParam, Number(Runtime.config.gain));

            if (Runtime.config.update_volume_stack && isReadablePtr(Runtime.cache.camera)) {
                try {
                    native.updateVolumeStack(Runtime.cache.camera, ptr(0));
                } catch (e) {
                    setError("UpdateVolumeStack after apply failed", e);
                }
            }

            result = locateColorAdjustments(false);
            Runtime.stats.lastApplyResult = wroteExposure ? "applied and read back" : "write skipped";
            if (!(wroteContrast && wroteSaturation && wroteGamma && wroteGain)) {
                Runtime.stats.lastApplyResult += " (some extended parameters skipped)";
            }
            Runtime.lastStatus = result;
            log("info", "applyBrightness: exposure=" + exposure + ", result=" + Runtime.stats.lastApplyResult);
            return buildStatus(result);
        } catch (error) {
            setError("applyBrightness failed", error);
            return buildStatus({ ok: false, reason: Runtime.stats.lastError });
        }
    }

    function resetBrightness() {
        Runtime.stats.resetCount += 1;
        var restored = [];

        try {
            if (Runtime.originals.postExposure && isReadablePtr(Runtime.originals.postExposure.ptr)) {
                Runtime.originals.postExposure.ptr.add(OFF.VolumeParameter_floatValue).writeFloat(Runtime.originals.postExposure.value);
                Runtime.originals.postExposure.ptr.add(OFF.VolumeParameter_overrideState).writeU8(Runtime.originals.postExposure.overrideState ? 1 : 0);
                restored.push("postExposure");
            }
            if (Runtime.originals.contrast && isReadablePtr(Runtime.originals.contrast.ptr)) {
                Runtime.originals.contrast.ptr.add(OFF.VolumeParameter_floatValue).writeFloat(Runtime.originals.contrast.value);
                Runtime.originals.contrast.ptr.add(OFF.VolumeParameter_overrideState).writeU8(Runtime.originals.contrast.overrideState ? 1 : 0);
                restored.push("contrast");
            }
            if (Runtime.originals.saturation && isReadablePtr(Runtime.originals.saturation.ptr)) {
                Runtime.originals.saturation.ptr.add(OFF.VolumeParameter_floatValue).writeFloat(Runtime.originals.saturation.value);
                Runtime.originals.saturation.ptr.add(OFF.VolumeParameter_overrideState).writeU8(Runtime.originals.saturation.overrideState ? 1 : 0);
                restored.push("saturation");
            }
            ["gamma", "gain"].forEach(function (name) {
                var original = Runtime.originals[name];
                if (!original || !original.vector4 || !isReadablePtr(original.ptr)) return;
                original.ptr.add(OFF.VolumeParameter_floatValue).writeFloat(original.x);
                original.ptr.add(OFF.VolumeParameter_floatValue + 4).writeFloat(original.y);
                original.ptr.add(OFF.VolumeParameter_floatValue + 8).writeFloat(original.z);
                original.ptr.add(OFF.VolumeParameter_floatValue + 12).writeFloat(original.w);
                original.ptr.add(OFF.VolumeParameter_overrideState).writeU8(original.overrideState ? 1 : 0);
                restored.push(name);
            });
            if (Runtime.originals.renderPostProcessing && isReadablePtr(Runtime.originals.renderPostProcessing.ptr)) {
                writeBoolField(
                    Runtime.originals.renderPostProcessing.ptr,
                    Runtime.originals.renderPostProcessing.offset,
                    Runtime.originals.renderPostProcessing.value
                );
                restored.push("renderPostProcessing");
            }
            Runtime.originals = {};
            Runtime.stats.lastApplyResult = "reset restored: " + (restored.length ? restored.join(", ") : "none");
            log("info", Runtime.stats.lastApplyResult);
            return buildStatus(locateColorAdjustments(true));
        } catch (error) {
            setError("resetBrightness failed", error);
            return buildStatus({ ok: false, reason: Runtime.stats.lastError });
        }
    }

    function cleanupFeature() {
        Runtime.enabled = false;
        Runtime.stats.cleanupCount += 1;
        try {
            resetBrightness();
        } catch (e) {}
        resetRuntime("cleanup");
        Runtime.initialized = false;
        native.ready = false;
        log("info", "cleanup done");
        return buildStatus(Runtime.lastStatus || {});
    }

    function buildStatus(extra) {
        var snapshot = extra || Runtime.lastStatus || {};
        return {
            feature_id: Runtime.feature_id,
            enabled: Runtime.enabled,
            initialized: Runtime.initialized,
            generation: Runtime.generation,
            config: Runtime.config,
            stats: Runtime.stats,
            probe: snapshot,
            originals: {
                postExposure: !!Runtime.originals.postExposure,
                contrast: !!Runtime.originals.contrast,
                saturation: !!Runtime.originals.saturation,
                gamma: !!Runtime.originals.gamma,
                gain: !!Runtime.originals.gain,
                renderPostProcessing: !!Runtime.originals.renderPostProcessing
            }
        };
    }

    rpc.exports = {
        enable() {
            Runtime.enabled = true;
            initNativeFunctions();
            log("info", "enabled");
            return buildStatus(Runtime.lastStatus || {});
        },

        disable() {
            Runtime.enabled = false;
            resetBrightness();
            resetRuntime("disable");
            log("info", "disabled");
            return buildStatus(Runtime.lastStatus || {});
        },

        status() {
            return buildStatus(Runtime.lastStatus || {});
        },

        cleanup() {
            return cleanupFeature();
        },

        setConfig(config) {
            return setConfig(config);
        },

        setconfig(config) {
            return setConfig(config);
        },

        applyBrightness(value) {
            return applyBrightness(value);
        },

        applybrightness(value) {
            return applyBrightness(value);
        },

        resetBrightness() {
            return resetBrightness();
        },

        resetbrightness() {
            return resetBrightness();
        }
    };

    log("info", "brightness probe loaded");
})();
