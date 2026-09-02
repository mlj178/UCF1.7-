'use strict';

// 只读观察脚本：不修改游戏内存，也不调用修改器功能。
(function () {
    const MODULE_NAME = 'GameAssembly.dll';
    const RVA = {
        playerMoveByLocalDirection: 0x00B50A00,
        characterControllerMove: 0x00AB8210,
        playerIsMine: 0x00B55FD0
    };
    const OFFSET = {
        playerGrounded: 0x70,
        playerAirField: 0x88,
        playerVelocity: 0x90,
        playerController: 0x2C,
        velocityY: 0x10
    };
    const SAMPLE_INTERVAL_MS = 100;
    const MOVE_INTERVAL_MS = 50;

    let module = null;
    let localPlayer = null;
    let localController = null;
    let lastSnapshotAt = 0;
    let lastMoveAt = 0;

    function emit(event) {
        try {
            event.timestamp = Date.now();
            send(event);
        } catch (_) {
        }
    }

    function error(stage, detail) {
        emit({ type: 'probe_error', stage: stage, message: String(detail) });
    }

    function pointerText(value) {
        try {
            return value && !value.isNull() ? value.toString() : '';
        } catch (_) {
            return '';
        }
    }

    function readPlayerSnapshot(player) {
        try {
            if (!player || player.isNull()) {
                return null;
            }
            const velocity = player.add(OFFSET.playerVelocity).readPointer();
            return {
                type: 'player_snapshot',
                player: pointerText(player),
                grounded: player.add(OFFSET.playerGrounded).readU8() !== 0,
                field_0x88: player.add(OFFSET.playerAirField).readFloat(),
                velocity_pointer: pointerText(velocity),
                velocity_y: velocity && !velocity.isNull()
                    ? velocity.add(OFFSET.velocityY).readFloat()
                    : null
            };
        } catch (caught) {
            error('read_player_snapshot', caught);
            return null;
        }
    }

    const floatBits = new ArrayBuffer(4);
    const floatView = new DataView(floatBits);

    function stackArgToFloat(stackArg) {
        try {
            floatView.setUint32(0, stackArg.toUInt32(), true);
            return floatView.getFloat32(0, true);
        } catch (caught) {
            error('decode_stack_float', caught);
            return null;
        }
    }

    function captureLocalPlayerFromGetter(player) {
        if (localPlayer || !player || player.isNull()) {
            return;
        }
        try {
            localPlayer = player;
            localController = player.add(OFFSET.playerController).readPointer();
            emit({
                type: 'local_player_captured',
                player: pointerText(localPlayer),
                controller: pointerText(localController)
            });
        } catch (caught) {
            error('capture_local_player_from_getter', caught);
        }
    }

    function install() {
        module = Process.findModuleByName(MODULE_NAME);
        if (!module) {
            error('find_module', MODULE_NAME + ' not loaded');
            return;
        }
        emit({
            type: 'probe_metadata',
            module: module.name,
            base: module.base.toString(),
            size: module.size,
            arch: Process.arch,
            pointer_size: Process.pointerSize
        });

        try {
            // Player.get_isMyPlayer：只观察游戏原本发起的 getter 调用，不主动进入游戏函数。
            Interceptor.attach(module.base.add(RVA.playerIsMine), {
                onEnter(args) {
                    this.player = args[0];
                },
                onLeave(retval) {
                    try {
                        if (retval.toInt32() !== 0) {
                            captureLocalPlayerFromGetter(this.player);
                        }
                    } catch (caught) {
                        error('observe_is_my_player', caught);
                    }
                }
            });
            emit({ type: 'hook_installed', hook: 'Player.get_isMyPlayer', rva: RVA.playerIsMine });
        } catch (caught) {
            error('hook_is_my_player', caught);
        }

        try {
            Interceptor.attach(module.base.add(RVA.playerMoveByLocalDirection), {
                onEnter(args) {
                    emit({ type: 'hook_hit', hook: 'Player.MoveByLocalDirection' });
                }
            });
            emit({ type: 'hook_installed', hook: 'Player.MoveByLocalDirection', rva: RVA.playerMoveByLocalDirection });
        } catch (caught) {
            error('hook_player_move', caught);
        }

        try {
            Interceptor.attach(module.base.add(RVA.characterControllerMove), {
                onEnter(args) {
                    if (!localController || !args[0].equals(localController)) {
                        return;
                    }
                    const now = Date.now();
                    if (now - lastMoveAt < MOVE_INTERVAL_MS) {
                        return;
                    }
                    lastMoveAt = now;
                    const x = stackArgToFloat(args[1]);
                    const y = stackArgToFloat(args[2]);
                    const z = stackArgToFloat(args[3]);
                    emit({
                        type: 'controller_move',
                        controller: pointerText(args[0]),
                        vector_layout: 'x86_stack_by_value',
                        vector_readable: x !== null && y !== null && z !== null,
                        motion: { x: x, y: y, z: z }
                    });
                    emit({ type: 'hook_hit', hook: 'CharacterController.Move' });
                }
            });
            emit({ type: 'hook_installed', hook: 'CharacterController.Move', rva: RVA.characterControllerMove });
        } catch (caught) {
            error('hook_controller_move', caught);
        }

        setInterval(function () {
            const now = Date.now();
            if (!localPlayer || now - lastSnapshotAt < SAMPLE_INTERVAL_MS) {
                return;
            }
            lastSnapshotAt = now;
            const snapshot = readPlayerSnapshot(localPlayer);
            if (snapshot) {
                emit(snapshot);
            }
        }, 25);
    }

    install();
}());
