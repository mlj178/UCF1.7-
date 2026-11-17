# -*- coding: utf-8 -*-
"""rva_dis.py - 把 GameAssembly.dll 的 RVA 段反汇编出来（不依赖 IDA）。"

用法：
  python rva_dis.py 0x129050 --len 0xC0
  python rva_dis.py 0x129050 --len 0xC0 --raw     只打印十六进制
"""
import argparse
import os
import struct
import subprocess
import sys
import tempfile

GAME = os.environ.get('UCF_GAME', r'D:/BaiduNetdiskDownload/UnityCrossFire1.7.1/UnityCrossFire1.7.1')
DLL = os.path.join(GAME, 'GameAssembly.dll')
OBJDUMP = r'D:/Program Files/mingw32/bin/objdump.exe'


def sections(path):
    with open(path, 'rb') as f:
        data = f.read()
    if data[:2] != b'MZ':
        raise SystemExit('不是 PE')
    pe = struct.unpack_from('<I', data, 0x3C)[0]
    nsec = struct.unpack_from('<H', data, pe + 6)[0]
    optsz = struct.unpack_from('<H', data, pe + 20)[0]
    sec0 = pe + 24 + optsz
    out = []
    for i in range(nsec):
        off = sec0 + i * 40
        name = data[off:off + 8].rstrip(b'\x00').decode('latin-1')
        vsize, vaddr, rawsize, rawptr = struct.unpack_from('<IIII', data, off + 8)
        out.append((name, vaddr, vsize, rawptr, rawsize))
    return data, out


def read_rva(path, rva, length):
    data, secs = sections(path)
    for name, vaddr, vsize, rawptr, rawsize in secs:
        if vaddr <= rva < vaddr + max(vsize, rawsize):
            delta = rva - vaddr
            if delta >= rawsize:
                return b''
            return data[rawptr + delta: rawptr + delta + length]
    raise SystemExit('RVA 不在任何节里: 0x%X' % rva)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('rva', help='起始 RVA，如 0x129050')
    ap.add_argument('--len', default='0xC0', help='字节数，默认 0xC0')
    ap.add_argument('--raw', action='store_true')
    ap.add_argument('--dll', default=DLL)
    args = ap.parse_args(argv)
    rva = int(args.rva, 0)
    length = int(args.len, 0)
    buf = read_rva(args.dll, rva, length)
    if not buf:
        raise SystemExit('读不到字节')
    if args.raw:
        for i in range(0, len(buf), 16):
            chunk = buf[i:i + 16]
            print('%08X  %s' % (rva + i, ' '.join('%02x' % b for b in chunk)))
        return 0
    fd, tmp = tempfile.mkstemp(suffix='.bin')
    os.close(fd)
    try:
        with open(tmp, 'wb') as f:
            f.write(buf)
        cmd = [OBJDUMP, '-D', '-b', 'binary', '-m', 'i386', '--adjust-vma=0x%X' % rva, tmp]
        res = subprocess.run(cmd, capture_output=True, text=True)
        text = res.stdout
        keep = []
        started = False
        for line in text.splitlines():
            if line.startswith(' '):
                started = True
            if started:
                keep.append(line)
        print('\n'.join(keep[:400]))
        if res.stderr.strip():
            print(res.stderr.strip(), file=sys.stderr)
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))