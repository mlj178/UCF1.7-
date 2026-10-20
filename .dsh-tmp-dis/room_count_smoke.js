
'use strict';
const fs = require('fs');
const vm = require('vm');
const path = require('path');

const scriptPath = process.argv[2];
const text = fs.readFileSync(scriptPath, 'utf8');
const BASE = 0x10000000;
const SIZE = 0x1000000;
const mem = new Uint8Array(SIZE);
mem.fill(0xCC);

function P(addr) {
  const a = Number(addr) | 0;
  function inMod() { return a >= BASE && a < BASE + SIZE; }
  const self = {
    __addr: a,
    add(n) { return P(a + n); },
    sub(n) { return P(a - n); },
    isNull() { return a === 0; },
    readU8() { return inMod() ? mem[a - BASE] : 0; },
    readU32() { return inMod() ? (mem[a-BASE] | (mem[a-BASE+1]<<8) | (mem[a-BASE+2]<<16) | (mem[a-BASE+3]<<24)) >>> 0 : 0; },
    readS32() { return inMod() ? (mem[a-BASE] | (mem[a-BASE+1]<<8) | (mem[a-BASE+2]<<16) | (mem[a-BASE+3]<<24)) : 0; },
    readPointer() { return P(self.readU32()); },
    readCString() { return ''; },
    writeU8(v) { if (inMod()) mem[a - BASE] = v & 0xff; return self; },
    writeU32(v) { for (let i=0;i<4;i++) { if (inMod()) mem[a-BASE+i] = (v >>> (i*8)) & 0xff; } return self; },
    writeByteArray(arr) { for (let i=0;i<arr.length;i++) { if (inMod()) mem[a-BASE+i] = arr[i] & 0xff; } return self; },
  };
  return self;
}
function writeAt(rva, bytes) { for (let i=0;i<bytes.length;i++) mem[rva+i] = bytes[i]; }
function hexToBytes(s) { return s.trim().split(/\s+/).map(x => parseInt(x,16)); }
function bytesAt(rva, n) { return Array.from(mem.slice(rva, rva+n)); }

// base profile
const block = text.split('var BASE_30_TO_V3_PROFILE = [')[1].split('];')[0];
const re = /\[0x([0-9A-Fa-f]+), '([^']*)', '([^']*)'\]/g;
let m, entries = 0; const parsed = [];
while ((m = re.exec(block))) {
  const rva = parseInt(m[1], 16);
  writeAt(rva, hexToBytes(m[2]));
  parsed.push({rva: rva, base: hexToBytes(m[2]), v3: hexToBytes(m[3])});
  entries++;
}
const legacyBlock = text.split('var LEGACY_CHEAT_CAVES = [')[1].split('];')[0];
const legacy = [];
{ const re2 = /\[0x([0-9A-Fa-f]+), '([^']*)', '([^']*)'\]/g; let m2;
  while ((m2 = re2.exec(legacyBlock))) legacy.push({rva: parseInt(m2[1],16), base: hexToBytes(m2[2]), v3: hexToBytes(m2[3])}); }
// inspectLayout anchors
writeAt(0xAF9C67, [0x83,0xFE,0x1E,0x0F,0x8C,0x70,0xFF,0xFF,0xFF]);
writeAt(0xAF04EA, [0x48,0x3B,0x41,0x0C,0x73,0x0B]);
writeAt(0xAF04FB, hexToBytes('6a 00 e8 fe 74 67 ff 50 e8 28 78 67 ff'));
writeAt(0xB44895, [0x8B,0x87,0xCC,0x00,0x00,0x00]);
mem[0xB25C5A] = 0x00;
writeAt(0xB25C68, [0x75,0x0F]);
writeAt(0xAFAD8B, [0x83,0xFF,0x1E,0x7C,0x80]);
writeAt(0xAFD065, [0x6A,0x1E,0xFF,0x35]);

function makeWorld() {
  const sends = [], timers = [];
  const sandbox = {
    ptr: (v) => P(v === undefined || v === null ? 0 : v),
    Process: {
      arch: 'ia32', pointerSize: 4,
      findModuleByName(name) { return name === 'GameAssembly.dll' ? { name, base: P(BASE), size: SIZE, path: 'C:/game/GameAssembly.dll' } : null; },
      findRangeByAddress() { return { base: P(BASE), size: SIZE, protection: 'r-x' }; },
    },
    Memory: {
      protect() { return true; },
      alloc(n) { return P(0x20000000); },
    },
    send(p) { sends.push(p); },
    rpc: { exports: {} },
    setInterval(fn, ms) { const id = timers.length; timers.push({fn, ms}); return id; },
    clearInterval(id) { if (timers[id]) timers[id].cleared = true; },
    setTimeout() { return 0; },
    console: { log() {}, warn() {}, error(...a) { console.log('SANDBOX-ERR ' + a.join(' ')); } },
  };
  sandbox.globalThis = sandbox;
  const ctx = vm.createContext(sandbox);
  vm.runInContext(text, ctx, {filename: scriptPath});
  return { rpc: sandbox.rpc, sends, timers };
}

function check(name, ok, detail) {
  console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail === undefined ? '' : ' | ' + detail));
  if (!ok) process.exitCode = 1;
}

const w = makeWorld();
let res, err;
try { w.rpc.exports.enable({total_players: 70}); res = w.rpc.exports.setConfig({total_players: 70}); } catch (e) { err = e; }
check('enable() does not throw', !err, err && err.stack);
check('enable() ok', !!res && res.ok === true, JSON.stringify(res));
check('profile entries parsed', entries === 9, entries);
check('legacy cave list parsed', legacy.length === 4, legacy.length);
// 0xB30F3C / 0xB67F07 are code caves that writeState() intentionally rewrites.
const stateCaves = new Set([0xB30F3C, 0xB67F07]);
for (const e of parsed) { if (stateCaves.has(e.rva)) continue; const a = bytesAt(e.rva, e.v3.length); if (a.join(',') !== e.v3.join(',')) console.log('MISMATCH 0x' + e.rva.toString(16) + ' actual=' + a.join(' ') + ' expected=' + e.v3.join(' ')); }
check('0xB44895 stays original', JSON.stringify(bytesAt(0xB44895,6)) === JSON.stringify([0x8b,0x87,0xcc,0,0,0]), JSON.stringify(bytesAt(0xB44895,6)));
check('0x2BF6F8 stays padding', bytesAt(0x2BF6F8,1)[0] === 0xcc, bytesAt(0x2BF6F8,4).join(' '));
check('0x154FBA stays padding', bytesAt(0x154FBA,1)[0] === 0xcc, bytesAt(0x154FBA,4).join(' '));
check('0x5C0E4B stays padding', bytesAt(0x5C0E4B,1)[0] === 0xcc, bytesAt(0x5C0E4B,4).join(' '));
for (const c of legacy) check('cave 0x' + c.rva.toString(16) + ' stays padding', bytesAt(c.rva, c.base.length).every(b => b === 0xCC), bytesAt(c.rva,4).join(' '));
check('capacity 0xAF9C69=100', bytesAt(0xAF9C69,1)[0] === 0x64, bytesAt(0xAF9C69,1)[0]);
check('capacity 0xAFAD8D=100', bytesAt(0xAFAD8D,1)[0] === 0x64, bytesAt(0xAFAD8D,1)[0]);
check('capacity 0xAFD066=100', bytesAt(0xAFD066,1)[0] === 0x64, bytesAt(0xAFD066,1)[0]);
check('bot branch nop', bytesAt(0xB30F3C+7,2).join(',') === '144,144', bytesAt(0xB30F3C+7,2).join(' '));
check('bot count=69', (bytesAt(0xB30F3C+10,4)[0] | (bytesAt(0xB30F3C+11,4)[0]<<8)) === 69, bytesAt(0xB30F3C+10,4).join(' '));

let dres, derr;
try { dres = w.rpc.exports.disable(); } catch (e) { derr = e; }
check('disable() does not throw', !derr, derr && derr.stack);
check('0xB44895 still original after disable', JSON.stringify(bytesAt(0xB44895,6)) === JSON.stringify([0x8b,0x87,0xcc,0,0,0]), JSON.stringify(bytesAt(0xB44895,6)));
check('capacity restored 30', bytesAt(0xAF9C69,1)[0] === 0x1E, bytesAt(0xAF9C69,1)[0]);
// full baseline restore rewrites the whole bot cave back to int3 padding
check('bot cave restored to padding', bytesAt(0xB30F3C+7,2).join(',') === '204,204', bytesAt(0xB30F3C+7,2).join(' '));

// Legacy process: old v3 jump already present.
const w2 = makeWorld();
writeAt(0xB44895, [0xE9,0x5E,0xAE,0x77,0xFF,0x90]);
for (const c of legacy) writeAt(c.rva, c.v3);
let r2, e2;
try { w2.rpc.exports.enable({total_players: 70}); r2 = w2.rpc.exports.setConfig({total_players: 70}); } catch (e) { e2 = e; }
check('legacy enable() does not throw', !e2, e2 && e2.stack);
for (const c of legacy) check('legacy cave 0x' + c.rva.toString(16) + ' restored', bytesAt(c.rva, c.base.length).every(b => b === 0xCC), bytesAt(c.rva,4).join(' '));
check('legacy jump cleared', JSON.stringify(bytesAt(0xB44895,6)) === JSON.stringify([0x8b,0x87,0xcc,0,0,0]), JSON.stringify(bytesAt(0xB44895,6)));
check('legacy enable() ok', !!r2 && r2.ok === true, JSON.stringify(r2));