import os
import re

file_path = r"d:\trae_project\ucf1.7-modifier\01-游戏逆向分析-相关信息\IDA-汇编代码\IDA导出-GameAssembly.dll.lst"
output_dir = r"d:\trae_project\ucf1.7-modifier\01-游戏逆向分析-相关信息\IDA-汇编代码\IDA导出-分割"
max_size = 90 * 1024 * 1024  # 90MB

os.makedirs(output_dir, exist_ok=True)

print(f"源文件: {file_path}")
print(f"输出目录: {output_dir}")
print(f"每部分最大: 90 MB")
print("-" * 50)

file_size = os.path.getsize(file_path)
print(f"文件总大小: {file_size / 1024 / 1024:.2f} MB")

header_lines = []
segment_info = []
current_segment = None

print("\n读取文件头...")
with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    for i in range(50):
        line = f.readline()
        if not line:
            break
        header_lines.append(line)

print(f"文件头共 {len(header_lines)} 行")

print("\n开始分割...")

part_num = 1
current_size = 0
current_lines = []
func_start_pattern = re.compile(r'^\.(\w+):[\dA-F]+.*proc near')
func_end_pattern = re.compile(r'^\.(\w+):[\dA-F]+\s+\w+\s+endp')
segment_pattern = re.compile(r'^\.(\w+):')
last_func_end_line = None
in_function = False
func_buffer = []
total_written = 0

with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    line_num = 0
    for line in f:
        line_num += 1
        line_size = len(line.encode('utf-8', errors='ignore'))
        
        func_start = func_start_pattern.match(line)
        func_end = func_end_pattern.match(line)
        
        if func_start:
            in_function = True
            func_buffer = [line]
        elif in_function:
            func_buffer.append(line)
            if func_end:
                in_function = False
                func_size = sum(len(l.encode('utf-8', errors='ignore')) for l in func_buffer)
                
                if current_size + func_size > max_size and current_lines:
                    output_file = os.path.join(output_dir, f"GameAssembly_part{part_num}.lst")
                    with open(output_file, 'w', encoding='utf-8') as out:
                        out.writelines(header_lines)
                        out.write(f"\n; ========== Part {part_num} ==========\n\n")
                        out.writelines(current_lines)
                    
                    part_size = os.path.getsize(output_file)
                    total_written += part_size
                    print(f"Part {part_num}: {part_size / 1024 / 1024:.2f} MB (第 {line_num} 行)")
                    
                    part_num += 1
                    current_lines = []
                    current_size = 0
                
                current_lines.extend(func_buffer)
                current_size += func_size
                func_buffer = []
        else:
            if not in_function:
                if current_size + line_size > max_size and current_lines:
                    output_file = os.path.join(output_dir, f"GameAssembly_part{part_num}.lst")
                    with open(output_file, 'w', encoding='utf-8') as out:
                        out.writelines(header_lines)
                        out.write(f"\n; ========== Part {part_num} ==========\n\n")
                        out.writelines(current_lines)
                    
                    part_size = os.path.getsize(output_file)
                    total_written += part_size
                    print(f"Part {part_num}: {part_size / 1024 / 1024:.2f} MB (第 {line_num} 行)")
                    
                    part_num += 1
                    current_lines = []
                    current_size = 0
                
                current_lines.append(line)
                current_size += line_size
        
        if line_num % 100000 == 0:
            print(f"已处理 {line_num} 行...")

if current_lines:
    output_file = os.path.join(output_dir, f"GameAssembly_part{part_num}.lst")
    with open(output_file, 'w', encoding='utf-8') as out:
        out.writelines(header_lines)
        out.write(f"\n; ========== Part {part_num} ==========\n\n")
        out.writelines(current_lines)
    
    part_size = os.path.getsize(output_file)
    total_written += part_size
    print(f"Part {part_num}: {part_size / 1024 / 1024:.2f} MB")

print("\n" + "=" * 50)
print(f"分割完成！共 {part_num} 个部分")
print(f"总写入: {total_written / 1024 / 1024:.2f} MB")

index_file = os.path.join(output_dir, "README.txt")
with open(index_file, 'w', encoding='utf-8') as f:
    f.write("IDA导出-GameAssembly.dll.lst 分割文件索引\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"原始文件大小: {file_size / 1024 / 1024:.2f} MB\n")
    f.write(f"分割数量: {part_num} 个部分\n")
    f.write(f"每部分限制: 90 MB\n\n")
    f.write("文件列表:\n")
    for i in range(1, part_num + 1):
        part_file = os.path.join(output_dir, f"GameAssembly_part{i}.lst")
        if os.path.exists(part_file):
            size = os.path.getsize(part_file)
            f.write(f"  Part {i}: GameAssembly_part{i}.lst ({size / 1024 / 1024:.2f} MB)\n")
    f.write("\n说明:\n")
    f.write("- 每个部分都包含完整的文件头信息\n")
    f.write("- 分割按函数边界进行，保证函数完整性\n")
    f.write("- 可以使用文本编辑器分别查看每个部分\n")

print(f"\n索引文件已创建: {index_file}")
