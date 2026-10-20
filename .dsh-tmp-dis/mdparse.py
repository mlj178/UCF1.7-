
import struct, sys, os, json

path = sys.argv[1]
data = open(path,'rb').read()
print('size', len(data))
sig, ver, nstreams, dir_rva, checksum, tds, flags = struct.unpack_from('<IIIIIIQ', data, 0)
print('sig', data[:4], 'ver', hex(ver), 'streams', nstreams, 'dir', hex(dir_rva), 'time', tds)

types = {3:'ThreadList',4:'ModuleList',5:'MemoryList',6:'Exception',7:'SystemInfo',9:'Memory64List',15:'MemoryInfoList',16:'ThreadInfoList'}
streams = {}
for i in range(nstreams):
    st, size, rva = struct.unpack_from('<III', data, dir_rva + i*12)
    streams.setdefault(st, []).append((size, rva, i))
    print('stream', i, hex(st), types.get(st,'?'), 'size', size, 'rva', hex(rva))

# system info
if 7 in streams:
    size, rva, _ = streams[7][0]
    arch, level, rev, nproc, ptype = struct.unpack_from('<HHHBB', data, rva)
    print('arch', arch, '(0=x86)', 'nproc', nproc)

# modules
mods = []
if 4 in streams:
    size, rva, _ = streams[4][0]
    n = struct.unpack_from('<I', data, rva)[0]
    print('modules', n)
    off = rva+4
    for i in range(n):
        base, imgsize, cksum, ts, namerva = struct.unpack_from('<QIIII', data, off)
        nameoff = struct.unpack_from('<I', data, namerva)[0]
        name = data[namerva+4:namerva+4+nameoff].decode('utf-16-le', 'replace')
        mods.append((base, imgsize, name))
        off += 108
    for b,s,nm in mods:
        print('  mod %016x size %08x %s' % (b,s,nm))

# exception
if 6 in streams:
    size, rva, _ = streams[6][0]
    tid, align = struct.unpack_from('<II', data, rva)
    code, eflags, erec, eaddr, nparams, unused = struct.unpack_from('<IIQQII', data, rva+8)
    params = struct.unpack_from('<15Q', data, rva+8+32)
    csize, crva = struct.unpack_from('<II', data, rva+8+144)
    print('EXCEPTION tid', tid, 'code', hex(code), 'flags', hex(eflags), 'addr', hex(eaddr), 'nparams', nparams)
    print('  params', [hex(p) for p in params[:nparams]])
    print('  context size', csize, 'rva', hex(crva))
    # x86 context
    ctx = data[crva:crva+csize]
    if csize >= 204:
        edi, esi, ebx, edx, ecx, eax = struct.unpack_from('<6I', ctx, 156)
        ebp, eip, segcs, eflags2, esp, segss = struct.unpack_from('<6I', ctx, 180)
        print('  ctx EIP=%08x ESP=%08x EBP=%08x EAX=%08x EBX=%08x ECX=%08x EDX=%08x ESI=%08x EDI=%08x' % (eip,esp,ebp,eax,ebx,ecx,edx,esi,edi))
    # save context
    open(os.path.splitext(path)[0]+'_excctx.bin','wb').write(ctx)

# threads
threads = []
if 3 in streams:
    size, rva, _ = streams[3][0]
    n = struct.unpack_from('<I', data, rva)[0]
    print('threads', n)
    off = rva+4
    for i in range(n):
        tid, susp, pclass, prio = struct.unpack_from('<IIII', data, off)
        teb = struct.unpack_from('<Q', data, off+16)[0]
        st_start, st_size, st_rva = struct.unpack_from('<QII', data, off+24)
        cs, cr = struct.unpack_from('<II', data, off+40)
        threads.append(dict(tid=tid, teb=teb, stack_start=st_start, stack_size=st_size, stack_rva=st_rva, ctx_rva=cr, ctx_size=cs, susp=susp))
        off += 48
    for t in threads[:80]:
        print('  tid %d teb %x stack %x+%x ctx %x+%x susp %d' % (t['tid'], t['teb'], t['stack_start'], t['stack_size'], t['ctx_rva'], t['ctx_size'], t['susp']))

json.dump(dict(mods=mods, threads=threads), open(os.path.splitext(path)[0]+'_meta.json','w'))
