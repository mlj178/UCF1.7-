# Aim Vertical Coordinate Debug Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Correct vertical auto-aim pitch and write one structured diagnostic sample per second to `logs/aim_debug.log`.

**Architecture:** Keep coordinate acquisition and target selection in the Frida
script. Send rate-limited structured samples through the existing plugin-event
bridge, and let a feature-local Python event handler own the rotating file.

**Tech Stack:** Frida JavaScript, Python 3 `logging`, `unittest`

---

### Task 1: Pitch Sign Regression

**Files:**
- Modify: `04-正式发行版/全功能整合包2.3/game_modifier/features/11_aim/test_aim_static.py`
- Modify: `04-正式发行版/全功能整合包2.3/game_modifier/features/11_aim/script.js`

- [x] **Step 1: Write the failing test**

Add assertions that `readCameraRotation` returns the stored pitch directly and
`writeCameraRotation` writes `pitchDeg` directly. Assert that
`toStoredPitchDeg` and `fromStoredPitchDeg` no longer exist.

- [x] **Step 2: Run test to verify it fails**

Run:

```powershell
python "04-正式发行版\全功能整合包2.3\game_modifier\features\11_aim\test_aim_static.py" -v
```

Expected: the pitch-sign regression test fails because the current script
negates pitch on read and write.

- [x] **Step 3: Implement direct pitch read/write**

Use this convention:

```javascript
function readCameraRotation(player) {
  var yawDeg = player.add(OFF_AIM.P_cameraRotation).readFloat();
  var pitchDeg = player.add(OFF_AIM.P_cameraRotation + 4).readFloat();
  return { yawDeg: yawDeg, pitchDeg: pitchDeg, storedPitchDeg: pitchDeg };
}

function writeCameraRotation(player, yawDeg, pitchDeg) {
  player.add(OFF_AIM.P_cameraRotation).writeFloat(yawDeg);
  player.add(OFF_AIM.P_cameraRotation + 4).writeFloat(pitchDeg);
}
```

- [x] **Step 4: Run the focused test**

Expected: the pitch-sign regression passes.

### Task 2: Structured One-Second Diagnostics

**Files:**
- Modify: `04-正式发行版/全功能整合包2.3/game_modifier/features/11_aim/test_aim_static.py`
- Modify: `04-正式发行版/全功能整合包2.3/game_modifier/features/11_aim/script.js`
- Create: `04-正式发行版/全功能整合包2.3/game_modifier/features/11_aim/test_aim_runtime.js`

- [x] **Step 1: Write failing static assertions**

Require `diagnosticLogIntervalMs: 1000`, a last-sample timestamp, coordinate source
tags, a `plugin_event` named `aim_debug_sample`, and a call after the camera
rotation write.

- [x] **Step 2: Run test to verify it fails**

Expected: failures identify the missing throttle, source tags, and event.

- [x] **Step 3: Add the minimal diagnostic emitter**

Send a structured payload containing:

```javascript
{
  originSource: refreshed.from.source,
  originRootSource: refreshed.from.rootSource,
  targetSource: refreshed.pos.source,
  targetRootSource: refreshed.pos.rootSource,
  from: { x: refreshed.from.x, y: refreshed.from.y, z: refreshed.from.z },
  to: { x: refreshed.pos.x, y: refreshed.pos.y, z: refreshed.pos.z },
  dy: refreshed.dy,
  horizontalDistance: refreshed.hDist,
  targetPitchDeg: refreshed.targetPitchDeg,
  currentPitchDeg: currentRotation.pitchDeg,
  finalPitchDeg: finalPitchDeg,
  writtenPitchDeg: finalPitchDeg
}
```

Guard emission with `Date.now() - lastDiagnosticLogAt < 1000`.

- [x] **Step 4: Run the focused static and runtime tests**

Expected: all static tests pass.

### Task 3: Feature-Local Rotating Log File

**Files:**
- Create: `04-正式发行版/全功能整合包2.3/game_modifier/features/11_aim/events.py`
- Create: `04-正式发行版/全功能整合包2.3/game_modifier/features/11_aim/test_aim_debug_log.py`

- [x] **Step 1: Write a failing file-output test**

Load `events.py` with a temporary `APP_DIR`, route an `aim_debug_sample`, flush
the handler, and assert that `logs/aim_debug.log` contains the JSON payload.

- [x] **Step 2: Run test to verify it fails**

Run:

```powershell
python "04-正式发行版\全功能整合包2.3\game_modifier\features\11_aim\test_aim_debug_log.py" -v
```

Expected: failure because `events.py` does not exist.

- [x] **Step 3: Implement the rotating writer**

Create a non-propagating feature logger using `RotatingFileHandler` with
`maxBytes=2 * 1024 * 1024`, `backupCount=2`, UTF-8 encoding, and JSON payload
serialization. Ignore unrelated plugin events and empty payloads.

- [x] **Step 4: Run the file-output test**

Expected: the test passes and cleans up its temporary directory.

### Task 4: Full Verification

**Files:**
- Verify all files above.

- [x] **Step 1: Run both Python test files**

```powershell
python "04-正式发行版\全功能整合包2.3\game_modifier\features\11_aim\test_aim_static.py" -v
python "04-正式发行版\全功能整合包2.3\game_modifier\features\11_aim\test_aim_debug_log.py" -v
```

- [x] **Step 2: Check JavaScript syntax**

```powershell
node --check "04-正式发行版\全功能整合包2.3\game_modifier\features\11_aim\script.js"
```

- [x] **Step 3: Inspect the scoped diff**

Confirm only the aim feature, its tests, and the two design records changed for
this task. Do not stage or commit unrelated working-tree changes.
