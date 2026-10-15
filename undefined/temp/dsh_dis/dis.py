
import json, capstone, collections
d = json.load(open(r"undefined\\temp\\dsh_dis\\in.json", encoding="utf-8"))
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
md.detail = True
out = {}
targets = collections.OrderedDict()
for name, rec in d.items():
    bs = bytes(int(x, 16) for x in rec["hex"].split())
    base = int(rec["address"], 16)
    lines = []
    for ins in md.disasm(bs, base):
        mn = ins.mnemonic
        op = ins.op_str
        if mn in ("call", "jmp") and op.startswith("0x"):
            t = int(op, 16)
            targets.setdefault(t, []).append((name, ins.address))
            op = "sub_%X" % t
        lines.append("%06X  %-8s %s" % (ins.address, mn, op))
    out[name] = lines
print(json.dumps({"out": out, "targets": sorted(targets.keys())}))
