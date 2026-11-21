import sys, io
sys.path.insert(0, r'D:\trae_project\ucf1.7-modifier\06-测试\ucf_mod\tools')
import ucf_rec as R
p = r'D:\trae_project\ucf1.7-modifier\06-测试\ucf_mod\navdata\dev\vis\rec\level1_TransportShip_20261121_140112_20261121-140155.jsonl'
text = io.open(p, encoding='utf-8').read()
samples = R.parse_lines(text.splitlines())
res = R.analyse(samples)
print('samples', len(samples))
print(R.summary(res))
lines = R.save_lines(res)
print('lines', len(lines))
for L in lines:
    if L.startswith('jump'): print('  JUMP', L)
print('nodes', sum(1 for L in lines if L.startswith('node ')), 'edges', sum(1 for L in lines if L.startswith('edge ')))