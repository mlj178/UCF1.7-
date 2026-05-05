# -*- coding: utf-8 -*-
import re
from collections import Counter

# 读取两个文件
file1_path = r'd:\trae_project\UCF1.7修改大全\游戏逆向分析-相关信息\02-部分系统\02-完整版可视化.html'
file2_path = r'd:\trae_project\UCF1.7修改大全\游戏逆向分析-相关信息\02-部分系统\03--核心类详细定义.html'

with open(file1_path, 'r', encoding='utf-8') as f:
    content1 = f.read()

with open(file2_path, 'r', encoding='utf-8') as f:
    content2 = f.read()

# 从文件1提取字段名
# 格式: "fieldName (translation) : type" 或 "fieldName : type"
fields1 = re.findall(r'"(\w+)\s*(?:\([^)]*\))?\s*:', content1)

# 从文件2提取字段名
# 格式: <span class="field-type">type</span> fieldName
fields2 = re.findall(r'<span class="field-type">[^<]+</span>\s*(\w+)', content2)

# 合并所有字段名
all_fields = fields1 + fields2
print(f"文件1字段数: {len(fields1)}")
print(f"文件2字段数: {len(fields2)}")
print(f"总字段数: {len(all_fields)}")
print(f"去重后字段数: {len(set(all_fields))}")
print()

# 拆分驼峰命名，统计单词
words = []
for field in all_fields:
    # 拆分驼峰命名
    parts = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|[0-9]|\b)', field)
    words.extend([w.lower() for w in parts if len(w) > 2])

# 统计高频单词
word_counts = Counter(words)
print("=== 高频单词统计 (出现3次以上) ===")
for word, count in word_counts.most_common():
    if count >= 3:
        print(f"{word}: {count}次")
