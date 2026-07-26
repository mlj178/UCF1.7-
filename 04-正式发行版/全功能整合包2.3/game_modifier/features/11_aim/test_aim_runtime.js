'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const scriptPath = path.join(__dirname, 'script.js');
let source = fs.readFileSync(scriptPath, 'utf8').replace(/^\uFEFF/, '');
const returnPattern = /  return \{\r?\n    enable: function\(\) \{/;
const testExports = [
  '  return {',
  '    __test: {',
  '      calculateTargetAngles: calculateTargetAngles,',
  '      chooseTargetCandidate: chooseTargetCandidate,',
  '      emitAimDiagnostic: emitAimDiagnostic,',
  '      resetAimState: resetAimState,',
  '      readCameraRotation: readCameraRotation,',
  '      writeCameraRotation: writeCameraRotation',
  '    },',
  '    enable: function() {',
].join('\n');

assert(returnPattern.test(source), 'aim module return block not found');
source = source.replace(returnPattern, testExports);

let nowMs = 1000;
const sentMessages = [];
const context = {
  clearInterval: () => {},
  console: console,
  Date: { now: () => nowMs },
  Interceptor: { attach: () => ({ detach: () => {} }) },
  Memory: {},
  NativeFunction: function NativeFunction() {},
  Process: { findModuleByName: () => null },
  ptr: () => null,
  rpc: { exports: {} },
  send: (message) => sentMessages.push(message),
  setInterval: () => 1,
};
vm.createContext(context);
vm.runInContext(source, context, { filename: scriptPath });

const aim = context.modules.aim.__test;

const angles = aim.calculateTargetAngles(
  { x: 0, y: 1, z: 0 },
  { x: 0, y: 3, z: 10 }
);
assert(angles.targetPitchDeg > 0, 'target above origin must produce positive pitch');
assert(Math.abs(angles.rawPitchDeg - 11.309932) < 0.0001);

const selected = aim.chooseTargetCandidate([
  { id: 'nearest', selectionDistance: 10.0, angleDeg: 20.0 },
  { id: 'best-angle-in-band', selectionDistance: 11.5, angleDeg: 5.0 },
  { id: 'outside-band', selectionDistance: 12.01, angleDeg: 1.0 },
], 2.0);
assert.strictEqual(selected.id, 'best-angle-in-band');
assert.strictEqual(aim.chooseTargetCandidate([], 2.0), null);

const values = { 0x4C: 45, 0x50: 12.5 };
const writes = {};
const fakePlayer = {
  add: (offset) => ({
    readFloat: () => values[offset],
    writeFloat: (value) => { writes[offset] = value; },
  }),
};
assert.strictEqual(aim.readCameraRotation(fakePlayer).pitchDeg, 12.5);
aim.writeCameraRotation(fakePlayer, 90, -17.25);
assert.strictEqual(writes[0x4C], 90);
assert.strictEqual(writes[0x50], -17.25);

const refreshed = {
  from: {
    x: 0,
    y: 1,
    z: 0,
    source: 'camera',
    rootSource: 'player_transform',
  },
  pos: {
    x: 0,
    y: 3,
    z: 10,
    source: 'real_bone',
    rootSource: 'player_transform',
  },
  dy: 2,
  hDist: 10,
  targetYawDeg: 0,
  rawPitchDeg: angles.rawPitchDeg,
  targetPitchDeg: angles.targetPitchDeg,
};
const currentRotation = { yawDeg: 5, pitchDeg: 6 };

aim.emitAimDiagnostic(refreshed, currentRotation, 7, 8);
nowMs = 1500;
aim.emitAimDiagnostic(refreshed, currentRotation, 7, 8);
assert.strictEqual(sentMessages.length, 1);

aim.resetAimState('room_change');
nowMs = 1600;
aim.emitAimDiagnostic(refreshed, currentRotation, 7, 8);
assert.strictEqual(
  sentMessages.length,
  1,
  'state reset must not bypass one-second diagnostic throttle'
);

nowMs = 2000;
aim.emitAimDiagnostic(refreshed, currentRotation, 7, 8);
assert.strictEqual(sentMessages.length, 2);
assert.strictEqual(sentMessages[1].payload.rawPitchDeg, angles.rawPitchDeg);
assert.strictEqual(sentMessages[1].payload.writtenYawDeg, 7);
assert.strictEqual(sentMessages[1].payload.writtenPitchDeg, 8);

console.log('aim runtime behavior tests passed');
