import sys, io, json, math
sys.path.insert(0, r'D:\trae_project\ucf1.7-modifier\06-测试\ucf_mod\tools')
import ucf_rec as R
p = r'D:\trae_project\ucf1.7-modifier\06-测试\ucf_mod\navdata\dev\vis\rec\level1_TransportShip_20261121_140112_20261121-140155.jsonl'
text = io.open(p, encoding='utf-8').read()
samples = R.parse_lines(text.splitlines())
res = R.analyse(samples)
print('keys', list(res.keys()))
for ev in res.get('jumps', []):
    print('JUMP', ev)
print('---- raw samples with sp=1 ----')
for s in samples:
    if s.get('sp'):
        print(round(s['t'],2), round(s['x'],2), round(s['y'],2), round(s['z'],2), 'gy', s.get('gy'), 'sp', s['sp'], 'ct', s.get('ct'))