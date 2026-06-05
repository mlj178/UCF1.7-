// m_loader.js - load m.dll, verify no crash (no function calls)
(function() {
  try {
    var gm = Process.findModuleByName('UnityCrossFire.exe');
    var dp = gm.path.replace(/UnityCrossFire\.exe$/i, 'm.dll');
    console.log('[m] load DLL from: ' + dp);
    var d = Module.load(dp);
    console.log('[m] DLL loaded @ ' + d.base);
    console.log('[m] GAME STILL RUNNING = DLL LOAD OK');
  } catch(e) {
    console.log('[m] FAIL: ' + e.message);
  }
})();
