#pragma once

#include <windows.h>

struct Il2CppClass;
struct MethodInfo;
struct FieldInfo;

struct Il2CppImage {
    const char* name;
    const char* nameNoExt;
};

struct Il2CppAssembly {
    Il2CppImage* image;
};

class IL2CPPBridge {
public:
    static bool Initialize(HMODULE gameAssembly);
    
    static void* GetDomain();
    static Il2CppAssembly** GetAssemblies(size_t* count);
    static Il2CppImage* GetImage(const char* assemblyName);
    
    static Il2CppClass* GetClass(const char* assemblyName, const char* namespaze, const char* className);
    static MethodInfo* GetMethod(Il2CppClass* klass, const char* methodName, int argsCount);
    static FieldInfo* GetField(Il2CppClass* klass, const char* fieldName);
    static void* Invoke(MethodInfo* method, void* obj, void** args);
    static void* GetStaticFieldValue(FieldInfo* field);
    
    template<typename T>
    static T ReadField(void* obj, int offset) {
        if (!obj) return T();
        return *(T*)((BYTE*)obj + offset);
    }
    
private:
    static HMODULE s_GameAssembly;
    static void* s_ClassFromName;
    static void* s_GetMethodFromName;
    static void* s_GetFieldFromName;
    static void* s_RuntimeInvoke;
    static void* s_FieldStaticGetValue;
    static void* s_DomainGet;
    static void* s_DomainGetAssemblies;
    
    static void* GetExport(const char* name);
};
