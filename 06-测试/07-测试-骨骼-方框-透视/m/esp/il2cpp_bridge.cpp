#include "il2cpp_bridge.h"
#include "esp_log.h"
#include <stdio.h>

HMODULE IL2CPPBridge::s_GameAssembly = NULL;
void* IL2CPPBridge::s_ClassFromName = NULL;
void* IL2CPPBridge::s_GetMethodFromName = NULL;
void* IL2CPPBridge::s_GetFieldFromName = NULL;
void* IL2CPPBridge::s_RuntimeInvoke = NULL;
void* IL2CPPBridge::s_FieldStaticGetValue = NULL;
void* IL2CPPBridge::s_DomainGet = NULL;
void* IL2CPPBridge::s_DomainGetAssemblies = NULL;

typedef void* (__stdcall *FnDomainGet)();
typedef Il2CppAssembly** (__stdcall *FnGetAssemblies)(void*, size_t*);
typedef Il2CppClass* (__stdcall *FnClassFromName)(void*, const char*, const char*);
typedef MethodInfo* (__stdcall *FnGetMethodFromName)(Il2CppClass*, const char*, int);
typedef FieldInfo* (__stdcall *FnGetFieldFromName)(Il2CppClass*, const char*);
typedef void* (__stdcall *FnRuntimeInvoke)(MethodInfo*, void*, void**, void**);
typedef void (__stdcall *FnFieldStaticGetValue)(FieldInfo*, void*);

void* IL2CPPBridge::GetExport(const char* name) {
    if (!s_GameAssembly) return NULL;
    return (void*)GetProcAddress(s_GameAssembly, name);
}

bool IL2CPPBridge::Initialize(HMODULE gameAssembly) {
    s_GameAssembly = gameAssembly;
    
    s_DomainGet = GetExport("il2cpp_domain_get");
    s_DomainGetAssemblies = GetExport("il2cpp_domain_get_assemblies");
    s_ClassFromName = GetExport("il2cpp_class_from_name");
    s_GetMethodFromName = GetExport("il2cpp_class_get_method_from_name");
    s_GetFieldFromName = GetExport("il2cpp_class_get_field_from_name");
    s_RuntimeInvoke = GetExport("il2cpp_runtime_invoke");
    s_FieldStaticGetValue = GetExport("il2cpp_field_static_get_value");
    
    if (!s_ClassFromName || !s_GetMethodFromName || !s_GetFieldFromName || !s_DomainGet || !s_DomainGetAssemblies) {
        dbg("[IL2CPP] Failed to get exports");
        return false;
    }
    
    dbg("[IL2CPP] Initialized OK");
    dbg("[IL2CPP]   domain_get: 0x%p", s_DomainGet);
    dbg("[IL2CPP]   domain_get_assemblies: 0x%p", s_DomainGetAssemblies);
    dbg("[IL2CPP]   class_from_name: 0x%p", s_ClassFromName);
    dbg("[IL2CPP]   get_method: 0x%p", s_GetMethodFromName);
    dbg("[IL2CPP]   get_field: 0x%p", s_GetFieldFromName);
    
    return true;
}

void* IL2CPPBridge::GetDomain() {
    if (!s_DomainGet) return NULL;
    return ((FnDomainGet)s_DomainGet)();
}

Il2CppAssembly** IL2CPPBridge::GetAssemblies(size_t* count) {
    if (!s_DomainGetAssemblies || !count) return NULL;
    void* domain = GetDomain();
    if (!domain) return NULL;
    return ((FnGetAssemblies)s_DomainGetAssemblies)(domain, count);
}

Il2CppImage* IL2CPPBridge::GetImage(const char* assemblyName) {
    size_t count = 0;
    Il2CppAssembly** assemblies = GetAssemblies(&count);
    if (!assemblies || count == 0) {
        dbg("[IL2CPP] GetImage: no assemblies found");
        return NULL;
    }
    
    dbg("[IL2CPP] GetImage: searching %s in %zu assemblies", assemblyName, count);
    
    for (size_t i = 0; i < count; i++) {
        Il2CppAssembly* assembly = assemblies[i];
        if (!assembly) continue;
        
        Il2CppImage* image = assembly->image;
        if (!image || !image->name) continue;
        
        dbg("[IL2CPP] GetImage: assembly[%zu] = %s", i, image->name);
        
        if (strcmp(image->name, assemblyName) == 0 || 
            strcmp(image->nameNoExt, assemblyName) == 0) {
            dbg("[IL2CPP] GetImage: found %s at 0x%p", assemblyName, image);
            return image;
        }
    }
    
    dbg("[IL2CPP] GetImage: %s not found", assemblyName);
    return NULL;
}

Il2CppClass* IL2CPPBridge::GetClass(const char* assemblyName, const char* namespaze, const char* className) {
    dbg("[IL2CPP] GetClass: %s::%s (assembly: %s)", namespaze, className, assemblyName);
    
    if (!s_ClassFromName) {
        dbg("[IL2CPP] GetClass: s_ClassFromName is NULL");
        return NULL;
    }
    
    Il2CppImage* image = GetImage(assemblyName);
    if (!image) {
        dbg("[IL2CPP] GetClass: image not found for %s", assemblyName);
        return NULL;
    }
    
    dbg("[IL2CPP] GetClass: calling function at 0x%p with image=0x%p", s_ClassFromName, image);
    
    Il2CppClass* klass = ((FnClassFromName)s_ClassFromName)(image, namespaze, className);
    
    dbg("[IL2CPP] GetClass: result = 0x%p", klass);
    
    if (!klass) {
        dbg("[IL2CPP] Class not found: %s::%s", namespaze, className);
    }
    
    return klass;
}

MethodInfo* IL2CPPBridge::GetMethod(Il2CppClass* klass, const char* methodName, int argsCount) {
    dbg("[IL2CPP] GetMethod: %s (args=%d)", methodName, argsCount);
    
    if (!klass || !s_GetMethodFromName) {
        dbg("[IL2CPP] GetMethod: invalid params klass=0x%p", klass);
        return NULL;
    }
    
    dbg("[IL2CPP] GetMethod: calling function at 0x%p", s_GetMethodFromName);
    
    MethodInfo* method = ((FnGetMethodFromName)s_GetMethodFromName)(klass, methodName, argsCount);
    
    dbg("[IL2CPP] GetMethod: result = 0x%p", method);
    
    if (!method) {
        dbg("[IL2CPP] Method not found: %s (args=%d)", methodName, argsCount);
    }
    
    return method;
}

FieldInfo* IL2CPPBridge::GetField(Il2CppClass* klass, const char* fieldName) {
    dbg("[IL2CPP] GetField: %s", fieldName);
    
    if (!klass || !s_GetFieldFromName) {
        dbg("[IL2CPP] GetField: invalid params klass=0x%p", klass);
        return NULL;
    }
    
    dbg("[IL2CPP] GetField: calling function at 0x%p", s_GetFieldFromName);
    
    FieldInfo* field = ((FnGetFieldFromName)s_GetFieldFromName)(klass, fieldName);
    
    dbg("[IL2CPP] GetField: result = 0x%p", field);
    
    if (!field) {
        dbg("[IL2CPP] Field not found: %s", fieldName);
    }
    
    return field;
}

void* IL2CPPBridge::Invoke(MethodInfo* method, void* obj, void** args) {
    if (!method || !s_RuntimeInvoke) return NULL;
    
    void* exception = NULL;
    void* result = ((FnRuntimeInvoke)s_RuntimeInvoke)(method, obj, args, &exception);
    
    if (exception) {
        dbg("[IL2CPP] Invoke exception!");
    }
    
    return result;
}

void* IL2CPPBridge::GetStaticFieldValue(FieldInfo* field) {
    if (!field || !s_FieldStaticGetValue) return NULL;
    
    void* value = NULL;
    ((FnFieldStaticGetValue)s_FieldStaticGetValue)(field, &value);
    
    return value;
}
