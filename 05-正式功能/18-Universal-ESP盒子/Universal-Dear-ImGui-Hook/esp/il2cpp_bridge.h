#pragma once
#include <windows.h>

namespace esp {

// IL2CPP Bridge - Simplified type definitions

typedef void* Il2CppClass;
typedef void* MethodInfo;
typedef void* FieldInfo;
typedef void* Il2CppImage;
typedef void* Il2CppAssembly;
typedef void* Il2CppDomain;

// RVA constants (from IDA and dump.cs)
struct RVAConstants {
    // GameManager_TypeInfo (from IDA: .data:10E2933C)
    static constexpr uintptr_t GameManager_TypeInfo = 0x0E2933C;

    // Singleton.get_instance function
    static constexpr uintptr_t SingletonGet = 0x4A8170;

    // GameManager.get_instance MethodInfo pointer
    static constexpr uintptr_t GM_Singleton_MethodInfo = 0xE1CE64;

    // GameManager.AddPlayer (for Hook method)
    static constexpr uintptr_t GM_AddPlayer = 0xAF9A90;

    // Component.get_transform
    static constexpr uintptr_t Component_get_transform = 0x32CF40;

    // Transform.get_position (Address 4145840 = RVA 0x3F42B0)
    // Signature: void(Vector3* ret, Transform* transform, MethodInfo*)
    static constexpr uintptr_t Transform_get_position = 0x3F42B0;

    // Camera.WorldToScreenPoint_Injected (RVA 0x327EE0, NOT 0x327F20)
    // Signature: void(Camera*, Vector3* position, int eye, Vector3* ret, MethodInfo*)
    static constexpr uintptr_t Camera_WorldToScreenPoint_Injected = 0x327EE0;

    // Camera.get_main
    static constexpr uintptr_t Camera_get_main = 0x328310;

    // Entity.get_isDead (RVA: 0xB400E0)
    static constexpr uintptr_t Entity_get_isDead = 0xB400E0;

    // Collider.get_bounds_Injected (RVA: 0xAB85E0)
    // Signature: void(Collider* this, Bounds* ret, MethodInfo*)
    static constexpr uintptr_t Collider_get_bounds_Injected = 0xAB85E0;

};

// Field offset constants (from dump.cs)
struct OffsetConstants {
    // IL2CPP klass static_fields offset
    static constexpr uintptr_t Klass_staticFields = 0x5C;  // Standard IL2CPP offset

    // GameManager static fields (from dump.cs line 242584)
    static constexpr uintptr_t GM_myPlayer = 0x00;         // static Player myPlayer

    // GameManager instance fields
    static constexpr uintptr_t GM_allPlayers = 0x1C;       // Player[] allPlayers
    static constexpr uintptr_t GM_playersBL = 0x20;        // List<Player> playersBL
    static constexpr uintptr_t GM_playersBL_Alive = 0x24;  // List<Player> playersBL_Alive
    static constexpr uintptr_t GM_playersGR = 0x28;        // List<Player> playersGR
    static constexpr uintptr_t GM_playersGR_Alive = 0x2C;  // List<Player> playersGR_Alive

    // Entity fields
    static constexpr uintptr_t E_team = 0x20;              // Team (int32)
    static constexpr uintptr_t E_characterController = 0x2C; // CharacterController

    // Player fields
    static constexpr uintptr_t P_characterContainer = 0x58;  // Transform (body root)
    static constexpr uintptr_t P_currentCharacter = 0x5C;    // CharacterModel

    // CharacterModel fields
    static constexpr uintptr_t CM_spine = 0x5C;               // Transform
    static constexpr uintptr_t CM_spine1 = 0x60;              // Transform
    static constexpr uintptr_t CM_neck = 0x64;                // Transform
    static constexpr uintptr_t CM_helmet = 0x6C;              // Helmet object
    static constexpr uintptr_t CM_hitboxes = 0x74;            // Transform[]

    // Helmet fields (Helmet object + 0x10 = helmetCollider)
    static constexpr uintptr_t Helmet_collider = 0x10;        // Collider*

    // IL2CPP array
    static constexpr uintptr_t Arr_len = 0x0C;             // array length
    static constexpr uintptr_t Arr_data = 0x10;            // data start

    // IL2CPP List
    static constexpr uintptr_t List_items = 0x08;          // T[] _items
    static constexpr uintptr_t List_size = 0x0C;           // int _size
};

// Simplified IL2CPP bridge class
class IL2CPPBridge {
public:
    // Singleton.get_instance function pointer (public for helper function)
    typedef void* (*SingletonGetFn)(void* methodInfo);

    static bool Initialize(HMODULE gameAssembly);
    static bool IsInitialized() { return s_Initialized; }
    static bool IsGameAssemblyReady();
    static void ResetSessionState();

    // Get GameManager instance (pure RVA method)
    static void* GetGameManagerInstance();

    // Get GameAssembly base address
    static void* GetBase() { return s_GameAssemblyBase; }

private:
    static void* s_GameAssemblyBase;
    static bool s_Initialized;
    static void* s_CachedInstance;
    static SingletonGetFn s_SingletonGet;

    static void* TryGetGameManagerInstance();
    static bool ValidateGameManagerInstance(void* instance);
};

}
