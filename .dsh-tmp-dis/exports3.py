
import struct
DLL = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\GameAssembly.dll"
data = open(DLL,"rb").read()
pe = struct.unpack_from("<I", data, 0x3C)[0]
nsec = struct.unpack_from("<H", data, pe+6)[0]
optsz = struct.unpack_from("<H", data, pe+20)[0]
opt = pe+24
magic = struct.unpack_from("<H", data, opt)[0]
ddoff = opt + (96 if magic == 0x10b else 112)
exp_rva, exp_size = struct.unpack_from("<II", data, ddoff)
print("export dir rva=0x%X size=0x%X" % (exp_rva, exp_size))
# sections
secs=[]
so = opt+optsz
for i in range(nsec):
    s=so+i*40
    vs,va,rs,rp = struct.unpack_from("<IIII", data, s+8)
    secs.append((va,vs,rs,rp))
def r2o(rva):
    for va,vs,rs,rp in secs:
        if va <= rva < va+max(vs,rs): return rp+(rva-va)
    return None
o = r2o(exp_rva)
(nam_rva, ordbase, nfuncs, nnames, addr_funcs, addr_names, addr_ords) = struct.unpack_from("<IIIIIII", data, o+12)
print("nfuncs=%d nnames=%d" % (nfuncs, nnames))
names=[]
no = r2o(addr_names)
for i in range(nnames):
    nrva = struct.unpack_from("<I", data, no+i*4)[0]
    so2 = r2o(nrva)
    end = data.index(b"\x00", so2)
    nm = data[so2:end].decode("latin1")
    names.append(nm)
want = ["il2cpp_object_new","il2cpp_array_new","il2cpp_array_new_specific","il2cpp_array_class_get","il2cpp_runtime_invoke","il2cpp_class_get_methods","il2cpp_thread_attach","il2cpp_class_from_name","il2cpp_type_get_object","il2cpp_gc_wbarrier_set_field","il2cpp_field_get_offset"]
for w in want:
    print(("%-32s" % w), "YES" if w in names else "no")
print("total exports:", len(names))
print("sample:", [n for n in names if n.startswith("il2cpp_")][:40])
