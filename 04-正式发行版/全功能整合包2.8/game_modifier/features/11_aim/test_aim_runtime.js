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
  '      calculateVisibilityRayDistance: calculateVisibilityRayDistance,',
  '      calculateSelectionRayDistance: calculateSelectionRayDistance,',
  '      buildShotDirection: buildShotDirection,',
  '      buildChestAimPointCandidates: buildChestAimPointCandidates,',
  '      isTargetDamageHit: isTargetDamageHit,',
  '      pickBestCandidate: pickBestCandidate,',
  '      selectTargetWithPolicy: selectTargetWithPolicy,',
  '      resetTargetLockState: resetTargetLockState,',
  '      TARGET_POLICY: TARGET_POLICY,',
  '      targetLockState: targetLockState,',
  '      updateManualAimAccumulator: updateManualAimAccumulator,',
  '      emitBoneReadDiagnostic: emitBoneReadDiagnostic,',
  '      emitAimScanDiagnostic: emitAimScanDiagnostic,',
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
  Memory: { alloc: () => ({}) },
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

const playerA = { id: 'A' };
const playerB = { id: 'B' };
const playerC = { id: 'C' };
const playerD = { id: 'D' };
const candidate = (player, angleDeg, dist) => ({ player: player, angleDeg: angleDeg, dist: dist });

const innerPreferred = aim.pickBestCandidate([
  candidate(playerB, 6.0, 5.0),
  candidate(playerA, 4.0, 20.0),
], 5.0, 1.0);
assert.strictEqual(innerPreferred.player, playerA, 'inner cone must win over a closer outer target');

const angleTieUsesDistance = aim.pickBestCandidate([
  candidate(playerA, 2.0, 10.0),
  candidate(playerB, 2.5, 5.0),
], 5.0, 1.0);
assert.strictEqual(angleTieUsesDistance.player, playerB, 'within angle tie, the closer target wins');
assert.strictEqual(aim.pickBestCandidate([], 5.0, 1.0), null);

aim.resetTargetLockState('runtime-test');
let lockNow = 1000;
let lockCandidates = [candidate(playerA, 4.0, 10.0), candidate(playerB, 6.0, 5.0)];
assert.strictEqual(aim.selectTargetWithPolicy(lockCandidates, lockNow).player, playerA);
assert.strictEqual(aim.targetLockState.reason, 'acquire');

lockNow = 1040;
assert.strictEqual(aim.selectTargetWithPolicy(lockCandidates, lockNow).player, playerA);
assert.strictEqual(aim.targetLockState.reason, 'hold');

lockNow = 1080;
lockCandidates = [candidate(playerA, 4.0, 10.0), candidate(playerC, 3.2, 20.0)];
assert.strictEqual(
  aim.selectTargetWithPolicy(lockCandidates, lockNow).player,
  playerA,
  'small angle improvements inside the stickiness margin must not switch'
);

lockNow = 1100;
lockCandidates = [candidate(playerA, 4.0, 10.0), candidate(playerC, 2.5, 20.0)];
assert.strictEqual(aim.selectTargetWithPolicy(lockCandidates, lockNow).player, playerA);
assert.strictEqual(aim.targetLockState.reason, 'confirming');

lockNow = 1120;
assert.strictEqual(aim.selectTargetWithPolicy(lockCandidates, lockNow).player, playerC);
assert.strictEqual(aim.targetLockState.switchCount, 1);

lockNow = 1140;
lockCandidates = [candidate(playerC, 2.5, 20.0), candidate(playerD, 0.5, 30.0)];
assert.strictEqual(
  aim.selectTargetWithPolicy(lockCandidates, lockNow).player,
  playerC,
  'switch cooldown must suppress a flip immediately after a switch'
);
assert.strictEqual(aim.targetLockState.reason, 'cooldown_hold');

lockNow = 1240;
assert.strictEqual(aim.selectTargetWithPolicy(lockCandidates, lockNow).player, playerC);
lockNow = 1260;
assert.strictEqual(aim.selectTargetWithPolicy(lockCandidates, lockNow).player, playerD);

aim.resetTargetLockState('inner-override-test');
lockNow = 2000;
lockCandidates = [candidate(playerA, 18.0, 10.0), candidate(playerB, 25.0, 5.0)];
assert.strictEqual(aim.selectTargetWithPolicy(lockCandidates, lockNow).player, playerA);
lockNow = 2100;
lockCandidates = [candidate(playerA, 25.0, 10.0), candidate(playerB, 18.0, 5.0)];
assert.strictEqual(aim.selectTargetWithPolicy(lockCandidates, lockNow).player, playerA);
assert.strictEqual(aim.targetLockState.reason, 'confirming');
lockNow = 2120;
assert.strictEqual(aim.selectTargetWithPolicy(lockCandidates, lockNow).player, playerB);
assert.strictEqual(aim.targetLockState.reason, 'inner_override');

aim.resetTargetLockState('current-lost-test');
lockNow = 3000;
lockCandidates = [candidate(playerA, 4.0, 10.0), candidate(playerB, 6.0, 5.0)];
assert.strictEqual(aim.selectTargetWithPolicy(lockCandidates, lockNow).player, playerA);
lockNow = 3040;
assert.strictEqual(
  aim.selectTargetWithPolicy([candidate(playerB, 6.0, 5.0)], lockNow).player,
  playerB,
  'losing the current candidate must reacquire immediately'
);
assert.strictEqual(aim.targetLockState.reason, 'current_lost');
assert(Math.abs(aim.calculateVisibilityRayDistance(10.0, 0.20, 0.50) - 10.30) < 0.000001);
assert.strictEqual(aim.calculateVisibilityRayDistance(0.10, 0.20, 0.0), 0.0);
assert(Math.abs(aim.calculateSelectionRayDistance(10.0, 0.20, 0.10) - 9.70) < 0.000001);
assert.strictEqual(aim.calculateSelectionRayDistance(0.25, 0.20, 0.10), 0.0);

const shotDirection = aim.buildShotDirection(
  { x: 1, y: 2, z: 3 },
  { x: 4, y: 6, z: 3 }
);
assert(Math.abs(shotDirection.x - 0.6) < 0.000001);
assert(Math.abs(shotDirection.y - 0.8) < 0.000001);
assert(Math.abs(shotDirection.z) < 0.000001);
assert.strictEqual(aim.buildShotDirection({ x: 1, y: 2, z: 3 }, { x: 1, y: 2, z: 3 }), null);

const chestPoints = aim.buildChestAimPointCandidates(
  { x: 10, y: 20, z: 30, source: 'character_spine1' },
  0.18,
  0.22
);
assert.strictEqual(chestPoints.length, 9);
assert.deepStrictEqual(
  { x: chestPoints[0].x, y: chestPoints[0].y, z: chestPoints[0].z },
  { x: 10, y: 20, z: 30 }
);
assert(chestPoints.some((point) => point.y > 20), 'multipoint scan must probe above chest center');
assert(chestPoints.some((point) => point.x !== 10 || point.z !== 30), 'multipoint scan must probe chest width');
assert.strictEqual(aim.isTargetDamageHit(true, 3, 3), true);
assert.strictEqual(
  aim.isTargetDamageHit(true, 0, 3),
  false,
  'a target-owned environment collider must not be accepted as a damage hitbox'
);
assert.strictEqual(
  aim.isTargetDamageHit(false, 3, 3),
  false,
  'another entity hitbox must not be accepted for the selected target'
);

let manualState = { accumulatedDeg: 0.0, lastInputAtMs: 0 };
manualState = aim.updateManualAimAccumulator(manualState, 1.1, 1000);
assert.strictEqual(manualState.shouldOverride, false);
manualState = aim.updateManualAimAccumulator(manualState, 1.1, 1040);
assert.strictEqual(manualState.shouldOverride, false);
manualState = aim.updateManualAimAccumulator(manualState, 1.1, 1080);
assert.strictEqual(manualState.shouldOverride, true);
manualState = aim.updateManualAimAccumulator({ accumulatedDeg: 2.5, lastInputAtMs: 1000 }, 1.0, 1201);
assert.strictEqual(manualState.shouldOverride, false, 'stale manual movement must not accumulate forever');

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
assert.strictEqual(sentMessages[1].payload.selectionVisibilityMode, 'wall_only');
assert.strictEqual(
  Object.prototype.hasOwnProperty.call(sentMessages[1].payload, 'visibilityLayer'),
  false,
  'visual aim samples must not present stale selection data as an actual bullet hit'
);

aim.emitAimScanDiagnostic({
  players: 4,
  enemies: 3,
  aimPoints: 3,
  inFov: 2,
  visible: 0,
  targets: [
    { player: '0x1', status: 'candidate' },
    { player: '0x2', status: 'blocked_environment' },
    { player: '0x3', status: 'out_fov' },
  ],
});
assert.strictEqual(sentMessages.length, 3);
assert.strictEqual(sentMessages[2].payload.stage, 'target_scan');
assert.strictEqual(sentMessages[2].payload.reason, 'no_ranked_candidate');
assert.strictEqual(sentMessages[2].payload.visible, 0);
assert.strictEqual(sentMessages[2].payload.targets.length, 3);
nowMs = 2500;
aim.emitAimScanDiagnostic({ players: 4, enemies: 3, aimPoints: 3, inFov: 2, visible: 0 });
assert.strictEqual(sentMessages.length, 3, 'empty scan diagnostics must be rate limited');

const fakeBonePlayer = { toString: () => '0x1234' };
aim.emitBoneReadDiagnostic('animator_missing', fakeBonePlayer, 7, '');
assert.strictEqual(sentMessages.length, 4);
assert.strictEqual(sentMessages[3].payload.stage, 'bone_read');
assert.strictEqual(sentMessages[3].payload.reason, 'animator_missing');
assert.strictEqual(sentMessages[3].payload.animatorSource, 'player');
assert.strictEqual(sentMessages[3].payload.requestedBoneIndex, 7);
assert.strictEqual(sentMessages[3].payload.humanBoneIndex, 8);
assert.strictEqual(sentMessages[3].payload.player, '0x1234');
nowMs = 3000;
aim.emitBoneReadDiagnostic('animator_missing', fakeBonePlayer, 7, '');
assert.strictEqual(sentMessages.length, 4, 'bone diagnostics must be rate limited');
nowMs = 3500;
aim.emitBoneReadDiagnostic('bone_transform_missing', fakeBonePlayer, 7, '', 'currentCharacter');
assert.strictEqual(sentMessages.length, 5);
assert.strictEqual(sentMessages[4].payload.animatorSource, 'currentCharacter');

console.log('aim runtime behavior tests passed');
