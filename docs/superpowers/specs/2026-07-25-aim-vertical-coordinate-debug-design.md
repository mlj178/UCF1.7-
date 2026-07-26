# Aim Vertical Coordinate Debug Design

## Goal

Fix the vertical aiming error that appears when the local player and target are
at different world heights, while adding low-frequency diagnostics that remain
available in packaged builds.

## Root Cause

The target pitch is calculated from the world-space height delta:

`atan2(target.y - origin.y, horizontalDistance)`

The current write path negates that result before storing it in
`Player.cameraRotation.y`. The original implementation and the 2.1/2.2
packages write the calculated pitch directly. A zero pitch hides this mismatch
when both players are level, while any non-zero height delta reverses the
vertical aim direction.

## Design

- Keep the existing world-space angle calculation and pitch clamp.
- Read and write `Player.cameraRotation.y` in the same sign convention as the
  original working implementation.
- Preserve the real-bone-first and coordinate-fallback target selection.
- Tag aim origins and target points with their coordinate source for diagnosis.
- Emit one diagnostic sample per second while auto aim is actively writing.
- Route samples through a feature-local plugin event to
  `logs/aim_debug.log`, so diagnostics still work when the global packaged log
  handler is disabled.
- Rotate the diagnostic file at 2 MB and keep two backups.

## Diagnostic Fields

Each line includes the origin source, target source, origin XYZ, target XYZ,
world height delta, horizontal distance, calculated pitch, current pitch,
final pitch, and the raw pitch value written to memory.

## Validation

- Static regression tests verify direct pitch read/write without sign inversion.
- Static tests verify one-second throttling and the diagnostic payload fields.
- Python tests verify the feature-local log writer and rotation setup.
- JavaScript syntax is checked with Node.
