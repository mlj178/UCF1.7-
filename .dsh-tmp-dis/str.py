
import struct, sys
sys.argv=['x']
src=open(r'D:/trae_project/ucf1.7-modifier/.dsh-tmp-dis/tool.py',encoding='utf-8').read()
exec(src.split("md = Cs")[0])
def rdstr(addr):
    hdr = read_rva(addr, 12)
    ln = struct.unpack_from('<i', hdr, 8)[0]
    if ln<0 or ln>400: return None
    body = read_rva(addr+12, ln*2)
    return body.decode('utf-16-le', 'replace')
for a in (0x10e31094, 0x10e28db8, 0x10e25358, 0x10e2f408):
    try:
        print(hex(a), repr(rdstr(a)))
    except Exception as e:
        print(hex(a), 'ERR', e)
