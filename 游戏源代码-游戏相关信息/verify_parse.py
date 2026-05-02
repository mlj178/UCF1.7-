import re
import os

INPUT_FILE = r"d:\trae_project\UCF1.7修改大全\游戏源代码-游戏相关信息\Il2CppDumper\dump.cs"
OUTPUT_DIR = r"d:\trae_project\UCF1.7修改大全\游戏源代码-游戏相关信息\类"

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Count fields in original dump.cs
field_count = 0
field_pattern_src = re.compile(
    r'(?:private|public|protected|internal)\s+(?:static\s+|readonly\s+)*(?:const\s+)?'
    r'[\w<>\[\]\*\.]+\s+\w+\s*;\s*//\s*0x[0-9A-Fa-f]+'
)
for line in lines:
    if field_pattern_src.search(line):
        field_count += 1

# Count methods in original dump.cs
method_count = 0
method_pattern_src = re.compile(
    r'(?:public|private|protected|internal)\s+'
    r'(?:static\s+|override\s+|virtual\s+|abstract\s+|sealed\s+extern\s+|extern\s+)*'
    r'[\w<>\[\]\*\.]+\s+\w+\s*\([^)]*\)\s*\{'
)
for line in lines:
    if method_pattern_src.search(line):
        method_count += 1

# Count classes
class_count = 0
for line in lines:
    if '// TypeDefIndex:' in line and ('class ' in line or 'struct ' in line or 'interface ' in line or 'enum ' in line):
        class_count += 1

# Count in generated files
gen_fields = 0
gen_methods = 0
gen_classes = 0

for fname in sorted(os.listdir(OUTPUT_DIR)):
    if not fname.endswith('.md'):
        continue
    with open(os.path.join(OUTPUT_DIR, fname), 'r', encoding='utf-8') as f:
        gcontent = f.read()
    
    # Count classes (## ClassName)
    gen_classes += len(re.findall(r'^## ', gcontent, re.MULTILINE))
    
    # Count fields (lines with 偏移:)
    gen_fields += len(re.findall(r'\(偏移:', gcontent))
    
    # Count methods (lines with method signatures but not 偏移)
    for m in re.findall(r'^- `[^`]+`$', gcontent, re.MULTILINE):
        if '(偏移:' not in m:
            gen_methods += 1

print(f"=== dump.cs 原始数据 ===")
print(f"类: {class_count}")
print(f"字段: {field_count}")
print(f"方法: {method_count}")
print()
print(f"=== 生成的 MD 文件 ===")
print(f"类: {gen_classes}")
print(f"字段: {gen_fields}")
print(f"方法: {gen_methods}")
print()
print(f"=== 差异 ===")
print(f"类差异: {class_count - gen_classes}")
print(f"字段差异: {field_count - gen_fields}")
print(f"方法差异: {method_count - gen_methods}")
