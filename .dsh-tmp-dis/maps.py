import json, io, os
base = r'D:\trae_project\ucf1.7-modifier\06-测试\ucf_mod\navdata\dev\maps'
for fn in sorted(os.listdir(base)):
    if not fn.endswith('.json') or fn.startswith('_'): continue
    d = json.load(io.open(os.path.join(base, fn), encoding='utf-8'))
    keys = list(d.keys())[:12]
    f = d.get('features') or d.get('feat')
    cnt = {}
    if isinstance(f, dict):
        for k, v in f.items(): cnt[k] = len(v) if isinstance(v, list) else v
    elif isinstance(f, list):
        for it in f:
            k = it.get('kind') or it.get('type') or '?'
            cnt[k] = cnt.get(k, 0) + 1
    print(fn, '| keys:', keys, '| nodes', len(d.get('nodes', [])), '| edges', len(d.get('edges', [])), '| feat', cnt)