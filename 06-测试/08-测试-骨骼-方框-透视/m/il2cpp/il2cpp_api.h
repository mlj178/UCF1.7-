#pragma once
#include <Windows.h>
#include "il2cpp_types.h"
#include <vector>

namespace IL2CPP {
    class API {
    public:
        static bool Initialize(HMODULE gameAssembly);
        static void Shutdown();
        
        static void* GetDomain();
        static Il2CppAssembly** GetAssemblies(size_t* count);
        static Il2CppImage* GetImage(const char* assemblyName);
        
        static Il2CppClass* GetClass(const char* assemblyName, const char* namespaceName, const char* className);
        static Il2CppClass* GetClassFromObject(void* obj);
        static const char* GetClassSimpleName(Il2CppClass* klass);
        static const char* GetClassNamespace(Il2CppClass* klass);
        
        static MethodInfo* GetMethod(Il2CppClass* klass, const char* methodName, int argsCount);
        static void* InvokeMethod(MethodInfo* method, void* obj, void** args);
        static const char* GetMethodName(MethodInfo* method);
        
        static FieldInfo* GetField(Il2CppClass* klass, const char* fieldName);
        static int GetFieldOffset(FieldInfo* field);
        static void* GetFieldValue(void* obj, int offset);
        static void SetFieldValue(void* obj, int offset, void* value);
        
        static Il2CppClass* GetObjectClass(void* obj);
        
    private:
        static HMODULE s_GameAssembly;
        
        typedef void* (__stdcall *FnDomainGet)();
        typedef Il2CppAssembly** (__stdcall *FnDomainGetAssemblies)(void*, size_t*);
        typedef Il2CppImage* (__stdcall *FnImageFromName)(Il2CppAssembly*);
        typedef Il2CppClass* (__stdcall *FnClassFromName)(Il2CppImage*, const char*, const char*);
        typedef MethodInfo* (__stdcall *FnMethodFromName)(Il2CppClass*, const char*, int);
        typedef FieldInfo* (__stdcall *FnFieldFromName)(Il2CppClass*, const char*);
        typedef void* (__stdcall *FnRuntimeInvoke)(MethodInfo*, void*, void**, void**);
        typedef int (__stdcall *FnFieldGetOffset)(FieldInfo*);
        typedef const char* (__stdcall *FnClassGetName)(Il2CppClass*);
        typedef const char* (__stdcall *FnClassGetNamespace)(Il2CppClass*);
        typedef Il2CppClass* (__stdcall *FnObjectGetClass)(void*);
        
        static FnDomainGet s_DomainGet;
        static FnDomainGetAssemblies s_DomainGetAssemblies;
        static FnImageFromName s_ImageFromName;
        static FnClassFromName s_ClassFromName;
        static FnMethodFromName s_MethodFromName;
        static FnFieldFromName s_FieldFromName;
        static FnRuntimeInvoke s_RuntimeInvoke;
        static FnFieldGetOffset s_FieldGetOffset;
        static FnClassGetName s_ClassGetName;
        static FnClassGetNamespace s_ClassGetNamespace;
        static FnObjectGetClass s_ObjectGetClass;
    };
    
    class Class {
    public:
        Class() : m_Ptr(nullptr) {}
        Class(Il2CppClass* ptr) : m_Ptr(ptr) {}
        
        const char* GetName() const;
        const char* GetNamespace() const;
        MethodInfo* GetMethod(const char* name, int argsCount);
        FieldInfo* GetField(const char* name);
        
        bool IsValid() const { return m_Ptr != nullptr; }
        Il2CppClass* GetPtr() const { return m_Ptr; }
        
    private:
        Il2CppClass* m_Ptr;
    };
    
    class Method {
    public:
        Method() : m_Ptr(nullptr) {}
        Method(MethodInfo* ptr) : m_Ptr(ptr) {}
        
        const char* GetName() const;
        void* Invoke(void* obj, void** args);
        
        bool IsValid() const { return m_Ptr != nullptr; }
        MethodInfo* GetPtr() const { return m_Ptr; }
        
    private:
        MethodInfo* m_Ptr;
    };
    
    class Field {
    public:
        Field(FieldInfo* ptr) : m_Ptr(ptr) {}
        
        int GetOffset() const;
        template<typename T>
        T GetValue(void* obj) {
            return *(T*)((BYTE*)obj + GetOffset());
        }
        
        bool IsValid() const { return m_Ptr != nullptr; }
        FieldInfo* GetPtr() const { return m_Ptr; }
        
    private:
        FieldInfo* m_Ptr;
    };
}
