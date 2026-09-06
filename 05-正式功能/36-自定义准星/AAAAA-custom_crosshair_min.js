(function () {
  'use strict';
  // FEATURE_ID = 'custom_crosshair'
  var FEATURE_ID = 'custom_crosshair';
  var mod = Process.findModuleByName('GameAssembly.dll');
  var supported = !!mod && Process.arch === 'ia32';
  var RVA = {
    HudCrosshair_Awake: 0x00B049E0, HudCrosshair_OnDestroy: 0x00B05000,
    HudCrosshair_Update: 0x00B05390, HudCrosshair_SetType: 0x00B05180,
    RectTransform_get_anchoredPosition_Injected: 0x004F47D0, RectTransform_get_sizeDelta_Injected: 0x004F4920,
    RectTransform_set_anchoredPosition_Injected: 0x004F4B60, RectTransform_set_sizeDelta_Injected: 0x004F5060,
    Component_GetComponent: 0x0032CD50, Component_GetComponentInChildren: 0x0032CC90, Transform_get_parent: 0x003F31D0,
    GameObject_GetComponent: 0x00331C10, GameObject_GetComponentInChildren: 0x00331B80, Graphic_set_color: 0x00321260
  };
  var OFF = { HudCrosshair_allCrosshair: 0x1C, HudCrosshair_crosshair1_horizontal: 0x20, HudCrosshair_crosshair1_vertical: 0x24 };
  var Runtime = {
    enabled:false, initialized:false, generation:0, hooks:[], hud:ptr(0), originals:{}, imageType:ptr(0), uiTypes:{},
    config:{r:0.0,g:1.0,b:0.0,a:0.9,scale:1.0,offset_x:0,offset_y:0},
    stats:{hookHits:0,awakeHits:0,setTypeHits:0,colorWrites:0,errorCount:0,lastError:'',lastResetReason:'',firstUpdateLogged:false,loggedColorTargets:{}}
  };
  var v2 = Memory.alloc(8);
  var setPos, setSize, getPos, getSize, getComponent, getComponentInChildren, gameObjectGetComponent, gameObjectGetComponentInChildren, getParent, setColor;
  function log(message, level) { try { send({type:'log', level:level || 'info', module:FEATURE_ID, message:String(message)}); } catch (_) {} }
  function pointerText(value) { return value && !value.isNull() ? value.toString() : 'NULL'; }
  function readable(value) { try { return !!value && !value.isNull() && !value.readPointer().isNull(); } catch (_) { return false; } }
  function initFunctions() {
    if (!supported || setPos) return;
    setPos = new NativeFunction(mod.base.add(RVA.RectTransform_set_anchoredPosition_Injected), 'void', ['pointer','pointer','pointer']);
    setSize = new NativeFunction(mod.base.add(RVA.RectTransform_set_sizeDelta_Injected), 'void', ['pointer','pointer','pointer']);
    getPos = new NativeFunction(mod.base.add(RVA.RectTransform_get_anchoredPosition_Injected), 'void', ['pointer','pointer','pointer']);
    getSize = new NativeFunction(mod.base.add(RVA.RectTransform_get_sizeDelta_Injected), 'void', ['pointer','pointer','pointer']);
    getComponent = new NativeFunction(mod.base.add(RVA.Component_GetComponent), 'pointer', ['pointer','pointer','pointer']);
    getComponentInChildren = new NativeFunction(mod.base.add(RVA.Component_GetComponentInChildren), 'pointer', ['pointer','pointer','int','pointer']);
    gameObjectGetComponent = new NativeFunction(mod.base.add(RVA.GameObject_GetComponent), 'pointer', ['pointer','pointer','pointer']);
    gameObjectGetComponentInChildren = new NativeFunction(mod.base.add(RVA.GameObject_GetComponentInChildren), 'pointer', ['pointer','pointer','int','pointer']);
    getParent = new NativeFunction(mod.base.add(RVA.Transform_get_parent), 'pointer', ['pointer','pointer']);
    setColor = new NativeFunction(mod.base.add(RVA.Graphic_set_color),'void',['pointer','float','float','float','float','pointer']);
  }
  function resetRuntime(reason) { Runtime.generation++; Runtime.hud=ptr(0); Runtime.originals={}; Runtime.stats.lastResetReason=reason || 'unknown'; }
  function resolveType(namespaceName,className) {
    var key=namespaceName+'.'+className;
    if (Runtime.uiTypes[key] && !Runtime.uiTypes[key].isNull()) return Runtime.uiTypes[key];
    try {
      var domainGet = Module.findGlobalExportByName('il2cpp_domain_get');
      var assembliesGet = Module.findGlobalExportByName('il2cpp_domain_get_assemblies');
      var imageGet = Module.findGlobalExportByName('il2cpp_assembly_get_image');
      var classFromName = Module.findGlobalExportByName('il2cpp_class_from_name');
      var classGetType = Module.findGlobalExportByName('il2cpp_class_get_type');
      if (!domainGet || !assembliesGet || !imageGet || !classFromName || !classGetType) throw new Error('missing IL2CPP export');
      var domain = new NativeFunction(domainGet,'pointer',[])();
      var count = Memory.alloc(4); count.writeU32(0);
      var assemblies = new NativeFunction(assembliesGet,'pointer',['pointer','pointer'])(domain,count);
      var ns = Memory.allocUtf8String(namespaceName), name = Memory.allocUtf8String(className);
      var getImage = new NativeFunction(imageGet,'pointer',['pointer']);
      var findClass = new NativeFunction(classFromName,'pointer',['pointer','pointer','pointer']);
      var typeForClass = new NativeFunction(classGetType,'pointer',['pointer']);
      for (var i=0; i<count.readU32(); i++) {
        var klass = findClass(getImage(assemblies.add(i * 4).readPointer()), ns, name);
        if (klass && !klass.isNull()) { Runtime.uiTypes[key] = typeForClass(klass); break; }
      }
    } catch (e) { Runtime.stats.lastError=key+' type: '+e.message; }
    return Runtime.uiTypes[key] || ptr(0);
  }
  function resolveUiType(className) { return resolveType('UnityEngine.UI',className); }
  function resolveImageType() { Runtime.imageType=resolveUiType('Image'); return Runtime.imageType; }
  function vectorSnapshot(rt) {
    if (!readable(rt)) return {pointer:pointerText(rt), valid:false};
    try {
      getPos(rt, v2, ptr(0)); var px=v2.readFloat(), py=v2.add(4).readFloat();
      getSize(rt, v2, ptr(0)); var sx=v2.readFloat(), sy=v2.add(4).readFloat();
      return {pointer:pointerText(rt), valid:true, anchored_position:{x:px,y:py}, size_delta:{x:sx,y:sy}};
    } catch (e) { return {pointer:pointerText(rt), valid:false, error:e.message}; }
  }
  function fieldPointer(offset) { try { return readable(Runtime.hud) ? Runtime.hud.add(offset).readPointer() : ptr(0); } catch (_) { return ptr(0); } }
  function inspectGraphicTargets(rt) {
    var result={};
    var classes=[['UnityEngine.UI','Image'],['UnityEngine.UI','RawImage'],['UnityEngine.UI','Graphic'],['UnityEngine','CanvasRenderer'],['UnityEngine','SpriteRenderer'],['UnityEngine','MeshRenderer'],['UnityEngine','Renderer'],['UnityEngine','MeshFilter'],['UnityEngine','ParticleSystem']];
    classes.forEach(function(entry) {
      var className=entry[1], type=resolveType(entry[0],className), direct=ptr(0), child=ptr(0), error='';
      try { if (readable(rt) && !type.isNull()) { direct=getComponent(rt,type,ptr(0)); child=getComponentInChildren(rt,type,1,ptr(0)); } }
      catch (e) { error=e.message; }
      result[className]={type:pointerText(type),direct:pointerText(direct),in_children:pointerText(child),error:error};
    });
    return result;
  }
  function inspectAncestorTargets(rt) {
    var result=[], cursor=rt;
    for (var depth=0; depth<6 && readable(cursor); depth++) {
      result.push({depth:depth,transform:pointerText(cursor),candidates:inspectGraphicTargets(cursor)});
      try { cursor=getParent(cursor,ptr(0)); } catch (e) { result.push({depth:depth,error:e.message}); break; }
    }
    return result;
  }
  function inspectGameObject(go) {
    var result={game_object:pointerText(go),components:{}};
    var classes=[['UnityEngine','CanvasRenderer'],['UnityEngine','SpriteRenderer'],['UnityEngine','MeshRenderer'],['UnityEngine','Renderer'],['UnityEngine','MeshFilter'],['UnityEngine','ParticleSystem'],['UnityEngine.UI','Image'],['UnityEngine.UI','RawImage'],['UnityEngine.UI','Graphic']];
    classes.forEach(function(entry) {
      var className=entry[1], type=resolveType(entry[0],className), direct=ptr(0), child=ptr(0), error='';
      try { if (readable(go) && !type.isNull()) { direct=gameObjectGetComponent(go,type,ptr(0)); child=gameObjectGetComponentInChildren(go,type,1,ptr(0)); } }
      catch (e) { error=e.message; }
      result.components[className]={type:pointerText(type),direct:pointerText(direct),in_children:pointerText(child),error:error};
    });
    return result;
  }
  function inspectAllCrosshair() {
    var array=fieldPointer(OFF.HudCrosshair_allCrosshair), result={array:pointerText(array),length:0,items:[]};
    try {
      if (!readable(array)) return result;
      result.length=array.add(0xC).readU32();
      for (var i=0;i<Math.min(result.length,16);i++) result.items.push({index:i,detail:inspectGameObject(array.add(0x10+i*4).readPointer())});
    } catch (e) { result.error=e.message; }
    return result;
  }
  // probe: reads runtime pointers and RectTransform values only. It never changes game memory or Unity UI state.
  function buildProbeSnapshot() {
    var horizontal=fieldPointer(OFF.HudCrosshair_crosshair1_horizontal), vertical=fieldPointer(OFF.HudCrosshair_crosshair1_vertical);
    var imageType=resolveImageType();
    return {supported:supported, architecture:Process.arch, game_assembly:mod ? {base:mod.base.toString(),size:mod.size} : null,
      initialized:Runtime.initialized, enabled:Runtime.enabled, hud:pointerText(Runtime.hud), hooks:Runtime.stats,
      image_type:pointerText(imageType), horizontal:vectorSnapshot(horizontal), vertical:vectorSnapshot(vertical),
      graphic_candidates:{horizontal:inspectGraphicTargets(horizontal),vertical:inspectGraphicTargets(vertical)},
      ancestor_graphic_candidates:{horizontal:inspectAncestorTargets(horizontal),vertical:inspectAncestorTargets(vertical)}, all_crosshair:inspectAllCrosshair()};
  }
  function snapshotLog(snapshot) { log('probe completed: hud='+snapshot.hud+', allCrosshair='+snapshot.all_crosshair.length); return snapshot; }
  function readOriginal(rt,key) { if (Runtime.originals[key]) return Runtime.originals[key]; Runtime.originals[key]={rt:rt}; return Runtime.originals[key]; }
  function applyOne(rt,key) {
    if (!readable(rt)) return;
    readOriginal(rt,key); var c=Runtime.config;
    v2.writeFloat(c.offset_x); v2.add(4).writeFloat(c.offset_y); setPos(rt,v2,ptr(0));
    v2.writeFloat(100*c.scale); v2.add(4).writeFloat(100*c.scale); setSize(rt,v2,ptr(0));
    var type=resolveImageType();
    if (!type.isNull()) { var image=getComponent(rt,type,ptr(0)); if (image && !image.isNull()) { setColor(image,c.r,c.g,c.b,c.a,ptr(0)); Runtime.stats.colorWrites++; if (!Runtime.stats.loggedColorTargets[key]) { Runtime.stats.loggedColorTargets[key]=true; log('Graphic.set_color wrote '+key+' image='+pointerText(image)+' rgba='+[c.r,c.g,c.b,c.a].join(',')); } } else { Runtime.stats.lastError='Image component missing for '+key; } }
  }
  function applyConfiguredCrosshair() {
    if (!Runtime.enabled || !readable(Runtime.hud)) return;
    try { applyOne(fieldPointer(OFF.HudCrosshair_crosshair1_horizontal),'h'); applyOne(fieldPointer(OFF.HudCrosshair_crosshair1_vertical),'v'); }
    catch (e) { Runtime.stats.errorCount++; Runtime.stats.lastError=e.message; log('apply error: '+e.message,'error'); }
  }
  function restoreOriginals() { Runtime.originals={}; }
  function attachHook(name,rva,callbacks) { try { Runtime.hooks.push(Interceptor.attach(mod.base.add(rva),callbacks)); log('hook installed: '+name); } catch(e) { Runtime.stats.lastError=name+': '+e.message; log(Runtime.stats.lastError,'error'); } }
  function installHooks() {
    if (Runtime.initialized || !supported) return;
    initFunctions();
    attachHook('HUD_Crosshair.Awake',RVA.HudCrosshair_Awake,{onEnter:function(a){this.h=a[0];},onLeave:function(){Runtime.stats.awakeHits++; Runtime.hud=this.h; log('HUD_Crosshair.Awake captured: '+pointerText(this.h));}});
    attachHook('HUD_Crosshair.Update',RVA.HudCrosshair_Update,{onEnter:function(a){Runtime.stats.hookHits++; Runtime.hud=a[0]; if(!Runtime.stats.firstUpdateLogged){Runtime.stats.firstUpdateLogged=true;log('HUD_Crosshair.Update first hit: '+pointerText(a[0]));}},onLeave:function(){applyConfiguredCrosshair();}});
    attachHook('HUD_Crosshair.SetType',RVA.HudCrosshair_SetType,{onEnter:function(){Runtime.stats.setTypeHits++;},onLeave:function(){applyConfiguredCrosshair();}});
    attachHook('HUD_Crosshair.OnDestroy',RVA.HudCrosshair_OnDestroy,{onEnter:function(){restoreOriginals();resetRuntime('HUD_Crosshair.OnDestroy');}});
    Runtime.initialized=true; log('probe hooks ready; click run read-only probe after returning to the match');
  }
  rpc.exports={
    enable:function(){installHooks(); if(!supported) throw new Error('GameAssembly.dll missing or target is not x86'); Runtime.enabled=true; applyConfiguredCrosshair(); return true;},
    disable:function(){Runtime.enabled=false;restoreOriginals();resetRuntime('disable');return true;},
    setconfig:function(c){c=c||{};['r','g','b','a','scale','offset_x','offset_y'].forEach(function(k){if(typeof c[k]==='number'&&isFinite(c[k]))Runtime.config[k]=c[k];});applyConfiguredCrosshair();return Runtime.config;},
    debugdump:function(){installHooks(); return snapshotLog(buildProbeSnapshot());},
    status:function(){return {feature_id:FEATURE_ID,supported:supported,enabled:Runtime.enabled,initialized:Runtime.initialized,generation:Runtime.generation,hook_hits:Runtime.stats.hookHits,awake_hits:Runtime.stats.awakeHits,set_type_hits:Runtime.stats.setTypeHits,color_writes:Runtime.stats.colorWrites,error_count:Runtime.stats.errorCount,last_error:Runtime.stats.lastError,last_reset_reason:Runtime.stats.lastResetReason,hud:pointerText(Runtime.hud),config:Runtime.config};},
    cleanup:function(){Runtime.enabled=false;restoreOriginals();Runtime.hooks.forEach(function(h){try{h.detach();}catch(_){}});Runtime.hooks=[];Runtime.initialized=false;resetRuntime('cleanup');return true;}
  };
  log(supported ? 'script loaded; read-only probe is available' : 'unsupported: GameAssembly.dll missing or process architecture is not x86','info');
}());
