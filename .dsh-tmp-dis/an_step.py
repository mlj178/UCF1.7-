import sys, io
sys.path.insert(0, r'D:\trae_project\ucf1.7-modifier\06-测试\ucf_mod\tools')
import ucf_rec as R
p = r'D:\trae_project\ucf1.7-modifier\06-测试\ucf_mod\navdata\dev\vis\rec\level1_TransportShip_20261121_140112_20261121-140155.jsonl'
text = io.open(p, encoding='utf-8').read()
samples = R.parse_lines(text.splitlines())
print('STEP_DEFAULT', R.STEP_DEFAULT)
for step in (2.5, 3, 4, 6):
    res = R.analyse(samples, step=step)
    lines = R.save_lines(res, allow_both=False)
    n = sum(1 for L in lines if L.startswith('node '))
    e = sum(1 for L in lines if L.startswith('edge '))
    j = sum(1 for L in lines if L.startswith('jump '))
    d = sum(1 for L in lines if L.startswith('node ') and False)
    print(step, 'nodes', n, 'edges', e, 'jumps', j)