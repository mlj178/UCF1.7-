import re
import os

file_path = r"d:\trae_project\ucf1.7-modifier\01-游戏逆向分析-相关信息\IDA-汇编代码\IDA导出-GameAssembly.dll.lst"

file_size = os.path.getsize(file_path)
print(f"文件大小: {file_size / 1024 / 1024:.2f} MB")

print("\n正在读取文件开头...")
with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    for i in range(200):
        line = f.readline()
        if not line:
            break
        if 'segment' in line.lower() or line.startswith('.'):
            print(f"第 {i+1} 行: {line.strip()[:80]}")

print("\n正在查找段边界...")
segment_positions = {}
chunk_size = 1024 * 1024
with open(file_path, 'rb') as f:
    chunk_num = 0
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        chunk_num += 1
        text = chunk.decode('utf-8', errors='ignore')
        for seg in ['.text:', '.rdata:', '.data:', '.bss:']:
            if seg in text and seg not in segment_positions:
                pos = f.tell() - len(chunk) + text.find(seg)
                segment_positions[seg] = pos
                print(f"发现 {seg} 在约 {pos / 1024 / 1024:.2f} MB 处")
        if chunk_num % 100 == 0:
            print(f"已扫描 {chunk_num * chunk_size / 1024 / 1024:.2f} MB...")

print(f"\n段位置:")
for seg, pos in sorted(segment_positions.items()):
    print(f"  {seg}: {pos / 1024 / 1024:.2f} MB")
