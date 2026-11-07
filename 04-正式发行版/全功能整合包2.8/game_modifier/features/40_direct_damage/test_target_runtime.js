'use strict';

// 纯目标策略测试：不连游戏，只验证 direct_damage 与 aim 共用的
// “外锥 -> 内锥优先 -> 角度优先 -> 距离 tiebreak -> 轻粘滞”算法。

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const scriptPath = path.join(__dirname, 'script.js');
let source = fs.readFileSync(scriptPath, 'utf8').replace(/^\uFEFF/, '');

const exportPattern = '    rpc.exports = {';
assert(source.includes(exportPattern), 'rpc.exports block not found');

source = source.replace(exportPattern, `    rpc.exports = {
        __test: {
            getRuntime: function () { return Runtime; },
            pickBestCandidate: pickBestCandidate,
            selectTargetFromCandidates: selectTargetFromCandidates,
            resetTargetLock: resetTargetLock,
            pickNearestCandidate: pickNearestCandidate
        },`);

function fakePtr() {
    const value = {
        isNull: () => true,
        add: () => fakePtr(),
        readPointer: () => fakePtr(),
        readS32: () => 0,
        readU32: () => 0,
        readFloat: () => 0,
        writeFloat: () => {},
        writeU32: () => {},
        writeS32: () => {},
        writePointer: () => {},
        equals: (other) => other === value,
        toString: () => '0x0'
    };
    return value;
}

const context = {
    console: console,
    Date: Date,
    Process: {
        arch: 'ia32',
        pointerSize: 4,
        findModuleByName: () => null,
        findRangeByAddress: () => null
    },
    Memory: { alloc: () => fakePtr() },
    NativeFunction: function NativeFunction() {},
    Interceptor: {
        attach: () => ({ detach: () => {} }),
        replace: () => {},
        revert: () => {}
    },
    ptr: () => fakePtr(),
    rpc: { exports: {} },
    send: () => {},
    setInterval: () => 1,
    clearInterval: () => {}
};
vm.createContext(context);
vm.runInContext(source, context, { filename: scriptPath });

const test = context.rpc.exports.__test;
assert(test, 'direct_damage __test exports missing');
const Runtime = test.getRuntime();

assert.strictEqual(Runtime.config.target_outer_cone_deg, 30.0);
assert.strictEqual(Runtime.config.target_inner_cone_deg, 20.0);
assert.strictEqual(Runtime.config.target_angle_tie_deg, 1.0);
assert.strictEqual(Runtime.config.target_switch_margin_deg, 1.2);
assert.strictEqual(Runtime.config.target_switch_confirm_scans, 1);
assert.strictEqual(Runtime.config.target_switch_cooldown_ms, 100);

const playerA = { id: 'A' };
const playerB = { id: 'B' };
const playerC = { id: 'C' };
const playerD = { id: 'D' };
const candidate = (player, angleDeg, dist) => ({ player: player, angleDeg: angleDeg, dist: dist });

assert.strictEqual(
    test.pickBestCandidate([candidate(playerB, 6.0, 5.0), candidate(playerA, 4.0, 20.0)], 5.0, 1.0).player,
    playerA,
    'inner cone must win over a closer outer target'
);
assert.strictEqual(
    test.pickBestCandidate([candidate(playerA, 2.0, 10.0), candidate(playerB, 2.5, 5.0)], 5.0, 1.0).player,
    playerB,
    'within angle tie, the closer target wins'
);
assert.strictEqual(test.pickBestCandidate([], 5.0, 1.0), null);

test.resetTargetLock(Runtime.targetLock, 'runtime-test');
Runtime.targetLock = null;
let now = 1000;
let candidates = [candidate(playerA, 4.0, 10.0), candidate(playerB, 6.0, 5.0)];
assert.strictEqual(test.selectTargetFromCandidates(candidates, now).player, playerA);
assert.strictEqual(Runtime.targetLock.reason, 'acquire');

now = 1040;
candidates = [candidate(playerA, 4.0, 10.0), candidate(playerC, 2.5, 20.0)];
assert.strictEqual(
    test.selectTargetFromCandidates(candidates, now).player,
    playerA,
    'switch cooldown after acquire must suppress an immediate flip'
);
assert.strictEqual(Runtime.targetLock.reason, 'cooldown_hold');

now = 1100;
assert.strictEqual(test.selectTargetFromCandidates(candidates, now).player, playerC);
assert.strictEqual(Runtime.targetLock.switchCount, 1);

now = 1120;
candidates = [candidate(playerC, 2.5, 20.0), candidate(playerD, 0.5, 30.0)];
assert.strictEqual(test.selectTargetFromCandidates(candidates, now).player, playerC);
assert.strictEqual(Runtime.targetLock.reason, 'cooldown_hold');

now = 1200;
assert.strictEqual(test.selectTargetFromCandidates(candidates, now).player, playerD);
assert.strictEqual(Runtime.targetLock.reason, 'angle_advantage');

test.resetTargetLock(Runtime.targetLock, 'inner-override-test');
Runtime.targetLock = null;
now = 2000;
candidates = [candidate(playerA, 18.0, 10.0), candidate(playerB, 25.0, 5.0)];
assert.strictEqual(test.selectTargetFromCandidates(candidates, now).player, playerA);
now = 2100;
candidates = [candidate(playerA, 25.0, 10.0), candidate(playerB, 18.0, 5.0)];
assert.strictEqual(test.selectTargetFromCandidates(candidates, now).player, playerB);
assert.strictEqual(Runtime.targetLock.reason, 'inner_override');

test.resetTargetLock(Runtime.targetLock, 'current-lost-test');
Runtime.targetLock = null;
now = 3000;
candidates = [candidate(playerA, 4.0, 10.0), candidate(playerB, 6.0, 5.0)];
assert.strictEqual(test.selectTargetFromCandidates(candidates, now).player, playerA);
now = 3040;
assert.strictEqual(test.selectTargetFromCandidates([candidate(playerB, 6.0, 5.0)], now).player, playerB);
assert.strictEqual(Runtime.targetLock.reason, 'current_lost');

const nearest = test.pickNearestCandidate([
    { player: playerA, dist: 20.0, angleDeg: 1.0 },
    { player: playerB, dist: 8.0, angleDeg: 9.0 }
], 10.0);
assert.strictEqual(nearest.player, playerB, 'fallback must choose the nearest target inside max distance');
assert.strictEqual(test.pickNearestCandidate([{ player: playerA, dist: 20.0 }], 10.0), null);

console.log('direct damage target runtime tests passed');
