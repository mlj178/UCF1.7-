#include "il2cpp_api.h"
#include "../core/logger.h"
#include <Windows.h>
#include <string.h>

namespace IL2CPP {
    HMODULE API::s_GameAssembly = nullptr;
    
    API::FnDomainGet API::s_DomainGet = nullptr;
    API::FnDomainGetAssemblies API::s_DomainGetAssemblies = nullptr;
    API::FnImageFromName API::s_ImageFromName = nullptr;
    API::FnClassFromName API::s_ClassFromName = nullptr;
    API::FnMethodFromName API::s_MethodFromName = nullptr;
    API::FnFieldFromName API::s_FieldFromName = nullptr;
    API::FnRuntimeInvoke API::s_RuntimeInvoke = nullptr;
    API::FnFieldGetOffset API::s_FieldGetOffset = nullptr;
    API::FnClassGetName API::s_ClassGetName = nullptr;
    API::FnClassGetNamespace API::s_ClassGetNamespace = nullptr;
    API::FnObjectGetClass API::s_ObjectGetClass = nullptr;
    
    bool API::Initialize(HMODULE gameAssembly) {
        if (!gameAssembly) {
            LOG_ERROR("IL2CPP", "Invalid GameAssembly handle");
            return false;
        }
        
        s_GameAssembly = gameAssembly;
        
        s_DomainGet = (FnDomainGet)GetProcAddress(s_GameAssembly, "il2cpp_domain_get");
        s_DomainGetAssemblies = (FnDomainGetAssemblies)GetProcAddress(s_GameAssembly, "il2cpp_domain_get_assemblies");
        s_ImageFromName = (FnImageFromName)GetProcAddress(s_GameAssembly, "il2cpp_assembly_get_image");
        s_ClassFromName = (FnClassFromName)GetProcAddress(s_GameAssembly, "il2cpp_class_from_name");
        s_MethodFromName = (FnMethodFromName)GetProcAddress(s_GameAssembly, "il2cpp_class_get_method_from_name");
        s_FieldFromName = (FnFieldFromName)GetProcAddress(s_GameAssembly, "il2cpp_class_get_field_from_name");
        s_RuntimeInvoke = (FnRuntimeInvoke)GetProcAddress(s_GameAssembly, "il2cpp_runtime_invoke");
        s_FieldGetOffset = (FnFieldGetOffset)GetProcAddress(s_GameAssembly, "il2cpp_field_get_offset");
        s_ClassGetName = (FnClassGetName)GetProcAddress(s_GameAssembly, "il2cpp_class_get_name");
        s_ClassGetNamespace = (FnClassGetNamespace)GetProcAddress(s_GameAssembly, "il2cpp_class_get_namespace");
        s_ObjectGetClass = (FnObjectGetClass)GetProcAddress(s_GameAssembly, "il2cpp_object_get_class");
        
        if (!s_DomainGet || !s_ClassFromName || !s_MethodFromName || !s_FieldFromName) {
            LOG_ERROR("IL2CPP", "Failed to get required exports");
            return false;
        }
        
        LOG("IL2CPP", "Initialized successfully");
        return true;
    }
    
    void API::Shutdown() {
        s_GameAssembly = nullptr;
        s_DomainGet = nullptr;
        s_DomainGetAssemblies = nullptr;
        s_ImageFromName = nullptr;
        s_ClassFromName = nullptr;
        s_MethodFromName = nullptr;
        s_FieldFromName = nullptr;
        s_RuntimeInvoke = nullptr;
        s_FieldGetOffset = nullptr;
        s_ClassGetName = nullptr;
        s_ClassGetNamespace = nullptr;
        s_ObjectGetClass = nullptr;
    }
    
    void* API::GetDomain() {
        if (!s_DomainGet) return nullptr;
        return s_DomainGet();
    }
    
    Il2CppAssembly** API::GetAssemblies(size_t* count) {
        if (!s_DomainGetAssemblies || !count) return nullptr;
        void* domain = GetDomain();
        if (!domain) return nullptr;
        return s_DomainGetAssemblies(domain, count);
    }
    
    Il2CppImage* API::GetImage(const char* assemblyName) {
        if (!assemblyName) return nullptr;
        
        size_t count = 0;
        Il2CppAssembly** assemblies = GetAssemblies(&count);
        if (!assemblies || count == 0) return nullptr;
        
        for (size_t i = 0; i < count; i++) {
            if (!assemblies[i]) continue;
            
            Il2CppImage* image = s_ImageFromName(assemblies[i]);
            if (!image) continue;
            
            const char* name = *(const char**)image;
            if (name && strcmp(name, assemblyName) == 0) {
                return image;
            }
        }
        
        return nullptr;
    }
    
    Il2CppClass* API::GetClass(const char* assemblyName, const char* namespaceName, const char* className) {
        if (!s_ClassFromName || !assemblyName || !className) return nullptr;
        
        Il2CppImage* image = GetImage(assemblyName);
        if (!image) {
            LOG_ERROR("IL2CPP", "Failed to get image: %s", assemblyName);
            return nullptr;
        }
        
        Il2CppClass* klass = s_ClassFromName(image, namespaceName ? namespaceName : "", className);
        if (!klass) {
            LOG_ERROR("IL2CPP", "Failed to get class: %s::%s", namespaceName, className);
        }
        
        return klass;
    }
    
    Il2CppClass* API::GetClassFromObject(void* obj) {
        if (!s_ObjectGetClass || !obj) return nullptr;
        return s_ObjectGetClass(obj);
    }
    
    const char* API::GetClassSimpleName(Il2CppClass* klass) {
        if (!s_ClassGetName || !klass) return nullptr;
        return s_ClassGetName(klass);
    }
    
    const char* API::GetClassNamespace(Il2CppClass* klass) {
        if (!s_ClassGetNamespace || !klass) return nullptr;
        return s_ClassGetNamespace(klass);
    }
    
    MethodInfo* API::GetMethod(Il2CppClass* klass, const char* methodName, int argsCount) {
        if (!s_MethodFromName || !klass || !methodName) return nullptr;
        
        MethodInfo* method = s_MethodFromName(klass, methodName, argsCount);
        if (!method) {
            LOG_ERROR("IL2CPP", "Failed to get method: %s (args=%d)", methodName, argsCount);
        }
        
        return method;
    }
    
    void* API::InvokeMethod(MethodInfo* method, void* obj, void** args) {
        if (!s_RuntimeInvoke || !method) return nullptr;
        
        void* exception = nullptr;
        void* result = s_RuntimeInvoke(method, obj, args, &exception);
        
        if (exception) {
            LOG_ERROR("IL2CPP", "Method invocation threw exception");
        }
        
        return result;
    }
    
    const char* API::GetMethodName(MethodInfo* method) {
        if (!method) return nullptr;
        return *(const char**)method;
    }
    
    FieldInfo* API::GetField(Il2CppClass* klass, const char* fieldName) {
        if (!s_FieldFromName || !klass || !fieldName) return nullptr;
        
        FieldInfo* field = s_FieldFromName(klass, fieldName);
        if (!field) {
            LOG_ERROR("IL2CPP", "Failed to get field: %s", fieldName);
        }
        
        return field;
    }
    
    int API::GetFieldOffset(FieldInfo* field) {
        if (!s_FieldGetOffset || !field) return 0;
        return s_FieldGetOffset(field);
    }
    
    void* API::GetFieldValue(void* obj, int offset) {
        if (!obj) return nullptr;
        return (void*)((BYTE*)obj + offset);
    }
    
    void API::SetFieldValue(void* obj, int offset, void* value) {
        if (!obj || !value) return;
        memcpy((BYTE*)obj + offset, value, sizeof(void*));
    }
    
    Il2CppClass* API::GetObjectClass(void* obj) {
        return GetClassFromObject(obj);
    }
    
    const char* Class::GetName() const {
        return API::GetClassSimpleName(m_Ptr);
    }
    
    const char* Class::GetNamespace() const {
        return API::GetClassNamespace(m_Ptr);
    }
    
    MethodInfo* Class::GetMethod(const char* name, int argsCount) {
        return API::GetMethod(m_Ptr, name, argsCount);
    }
    
    FieldInfo* Class::GetField(const char* name) {
        return API::GetField(m_Ptr, name);
    }
    
    const char* Method::GetName() const {
        return API::GetMethodName(m_Ptr);
    }
    
    void* Method::Invoke(void* obj, void** args) {
        return API::InvokeMethod(m_Ptr, obj, args);
    }
    
    int Field::GetOffset() const {
        return API::GetFieldOffset(m_Ptr);
    }
}
