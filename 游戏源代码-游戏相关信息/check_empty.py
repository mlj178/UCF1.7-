import re

INPUT_FILE = r"d:\trae_project\UCF1.7修改大全\游戏源代码-游戏相关信息\Il2CppDumper\dump.cs"

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Find all class declarations
class_decl_indices = []
for i, line in enumerate(lines):
    if '// TypeDefIndex:' in line and ('class ' in line or 'struct ' in line or 'interface ' in line or 'enum ' in line):
        class_decl_indices.append(i)

empty_classes = []
has_angle_bracket = []
has_content = []

for idx in class_decl_indices:
    decl_line = lines[idx]
    
    name_match = re.search(r'(?:class|struct|interface|enum)\s+(\S+)', decl_line)
    if not name_match:
        continue
    class_name = name_match.group(1)
    
    # Find braces
    brace_start = -1
    for j in range(idx, min(idx + 3, len(lines))):
        if '{' in lines[j]:
            brace_start = j
            break
    
    if brace_start == -1:
        continue
    
    depth = 0
    brace_end = -1
    for j in range(brace_start, len(lines)):
        depth += lines[j].count('{') - lines[j].count('}')
        if depth == 0:
            brace_end = j
            break
    
    if brace_end == -1:
        continue
    
    body_lines = lines[brace_start+1:brace_end]
    body_text = '\n'.join(body_lines)
    
    # Check if has fields or methods
    field_pattern = re.compile(
        r'(?:private|public|protected|internal)\s+(?:static\s+|readonly\s+)*(?:const\s+)?'
        r'[\w<>\[\]\*\.]+\s+\w+\s*;\s*//\s*0x[0-9A-Fa-f]+'
    )
    method_pattern = re.compile(
        r'(?:public|private|protected|internal)\s+'
        r'(?:static\s+|override\s+|virtual\s+|abstract\s+|sealed\s+extern\s+|extern\s+)*'
        r'[\w<>\[\]\*\.]+\s+\w+\s*\([^)]*\)\s*\{'
    )
    
    has_field = bool(field_pattern.search(body_text))
    has_method = bool(method_pattern.search(body_text))
    
    if '<' in class_name and '>' in class_name:
        if has_field or has_method:
            has_angle_bracket.append((class_name, '有内容'))
        else:
            has_angle_bracket.append((class_name, '空白'))
    
    if not has_field and not has_method:
        empty_classes.append(class_name)
    else:
        has_content.append(class_name)

print(f"总类数: {len(class_decl_indices)}")
print(f"有内容的类: {len(has_content)}")
print(f"空白类（无字段无方法）: {len(empty_classes)}")
print(f"带<>的类: {len(has_angle_bracket)}")
print()
print("=== 空白类中，带<>的编译器生成类 ===")
angle_empty = [c for c, s in has_angle_bracket if s == '空白']
print(f"数量: {len(angle_empty)}")
for c in angle_empty[:10]:
    print(f"  {c}")
if len(angle_empty) > 10:
    print(f"  ... 还有 {len(angle_empty)-10} 个")

print()
print("=== 空白类中，不带<>的正常类 ===")
normal_empty = [c for c in empty_classes if '<' not in c]
print(f"数量: {len(normal_empty)}")
for c in normal_empty[:20]:
    print(f"  {c}")
if len(normal_empty) > 20:
    print(f"  ... 还有 {len(normal_empty)-20} 个")
