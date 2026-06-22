#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IDA .lst 文件结构化索引生成器
用于提取函数、方法、字段等信息，生成结构化索引供 ChatGPT 快速定位

功能：
1. 解析 IDA 导出文件，提取函数定义
2. 建立函数名、地址、行号、分片的映射关系
3. 生成结构化 JSON 索引，便于 ChatGPT 查询
4. 支持按函数名、地址、类型快速定位

作者：AI Assistant
日期：2025
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class IDAIndexGenerator:
    """IDA 文件结构化索引生成器"""
    
    def __init__(self, split_output_dir: str):
        """
        初始化索引生成器
        
        Args:
            split_output_dir: 切分输出目录路径
        """
        self.split_output_dir = Path(split_output_dir)
        self.functions = {}  # 函数索引
        self.classes = {}    # 类索引
        self.fields = {}     # 字段索引
        self.methods = {}    # 方法索引
        
    def parse_all_parts(self):
        """解析所有 part 目录"""
        print("开始解析所有分片文件...")
        
        # 查找所有 part 目录
        part_dirs = [d for d in self.split_output_dir.iterdir() if d.is_dir() and d.name.startswith('part')]
        
        for part_dir in sorted(part_dirs):
            print(f"解析 {part_dir.name}...")
            self.parse_part(part_dir)
        
        print(f"\n解析完成！")
        print(f"函数总数: {len(self.functions)}")
        print(f"类总数: {len(self.classes)}")
        print(f"方法总数: {len(self.methods)}")
        print(f"字段总数: {len(self.fields)}")
    
    def parse_part(self, part_dir: Path):
        """解析单个 part 目录"""
        # 读取索引文件，获取分片信息
        index_file = part_dir / 'split_index.json'
        if not index_file.exists():
            return
        
        with open(index_file, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
        
        # 解析每个分片
        for chunk_info in index_data['chunks']:
            chunk_file = part_dir / chunk_info['chunk_file']
            if chunk_file.exists():
                self.parse_chunk(chunk_file, chunk_info)
    
    def parse_chunk(self, chunk_file: Path, chunk_info: Dict):
        """解析单个分片文件"""
        with open(chunk_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # 提取函数定义
        for i, line in enumerate(lines, start=chunk_info['start_line']):
            # 匹配函数定义：.text:XXXXXXXX sub_XXXXXXXX proc near
            func_match = re.match(r'^\.text:[0-9A-Fa-f]+\s+([a-zA-Z_][a-zA-Z0-9_]*|sub_[0-9A-Fa-f]+)\s+proc\s+near', line)
            if func_match:
                func_name = func_match.group(1)
                
                # 查找函数结束标记
                end_line = i
                for j in range(i, min(i + 500, chunk_info['end_line'])):  # 最多查找500行
                    if j < len(lines) and re.match(r'^\.text:[0-9A-Fa-f]+\s+' + func_name + r'\s+endp', lines[j - chunk_info['start_line']]):
                        end_line = j
                        break
                
                # 提取地址
                addr_match = re.match(r'^\.text:([0-9A-Fa-f]+)', line)
                address = addr_match.group(1) if addr_match else None
                
                # 提取注释（前几行可能包含注释）
                comments = []
                for k in range(max(0, i - chunk_info['start_line'] - 5), i - chunk_info['start_line']):
                    if k >= 0 and k < len(lines):
                        comment_line = lines[k].strip()
                        if comment_line.startswith(';') and not comment_line.startswith('; ='):
                            comments.append(comment_line[1:].strip())
                
                # 分类函数
                func_type = self.classify_function(func_name)
                
                # 存储函数信息
                func_info = {
                    'name': func_name,
                    'address': address,
                    'type': func_type,
                    'start_line': i,
                    'end_line': end_line,
                    'chunk_file': chunk_info['chunk_file'],
                    'part': chunk_file.parent.name,
                    'comments': comments[:3],  # 只保留前3条注释
                    'size_lines': end_line - i + 1
                }
                
                self.functions[func_name] = func_info
                
                # 如果是类方法，添加到类索引
                if '__' in func_name:
                    class_name = func_name.split('__')[0]
                    if class_name not in self.classes:
                        self.classes[class_name] = {
                            'name': class_name,
                            'methods': [],
                            'fields': []
                        }
                    self.classes[class_name]['methods'].append(func_name)
                    self.methods[func_name] = func_info
    
    def classify_function(self, func_name: str) -> str:
        """
        分类函数类型
        
        Args:
            func_name: 函数名
        
        Returns:
            函数类型
        """
        if func_name.startswith('sub_'):
            return 'unknown'
        elif '__' in func_name:
            parts = func_name.split('__')
            if len(parts) >= 2:
                method_name = parts[1]
                if method_name.startswith('get_') or method_name.startswith('set_'):
                    return 'property'
                elif method_name.startswith('_'):
                    return 'private_method'
                else:
                    return 'public_method'
        elif func_name.startswith('_'):
            return 'private_function'
        else:
            return 'public_function'
    
    def generate_structured_index(self, output_file: str):
        """生成结构化索引文件"""
        print("\n生成结构化索引...")
        
        index_data = {
            'metadata': {
                'total_functions': len(self.functions),
                'total_classes': len(self.classes),
                'total_methods': len(self.methods),
                'total_fields': len(self.fields),
                'generated_at': '2025-06-22'
            },
            'classes': self.classes,
            'functions': self.functions,
            'methods': self.methods,
            'fields': self.fields,
            'quick_reference': {
                'by_address': {},
                'by_type': {}
            }
        }
        
        # 按地址建立快速索引
        for func_name, func_info in self.functions.items():
            if func_info['address']:
                index_data['quick_reference']['by_address'][func_info['address']] = func_name
        
        # 按类型建立快速索引
        for func_type in ['public_method', 'private_method', 'property', 'unknown']:
            index_data['quick_reference']['by_type'][func_type] = [
                name for name, info in self.functions.items() 
                if info['type'] == func_type
            ]
        
        # 输出 JSON 文件
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] 结构化索引已生成: {output_path}")
        print(f"  文件大小: {output_path.stat().st_size / 1024:.2f} KB")
    
    def generate_chatgpt_index(self, output_file: str):
        """生成 ChatGPT 专用索引（精简版）"""
        print("\n生成 ChatGPT 专用索引...")
        
        # 只包含最常用的信息
        chatgpt_index = {
            'summary': {
                'total_functions': len(self.functions),
                'total_classes': len(self.classes),
                'top_classes': sorted(self.classes.keys())[:50]  # 前50个类
            },
            'popular_functions': {},
            'class_methods': {},
            'function_locations': {}
        }
        
        # 添加热门函数（按大小排序，前100个）
        sorted_funcs = sorted(self.functions.items(), key=lambda x: x[1]['size_lines'], reverse=True)[:100]
        for func_name, func_info in sorted_funcs:
            chatgpt_index['popular_functions'][func_name] = {
                'address': func_info['address'],
                'chunk': func_info['chunk_file'],
                'lines': f"{func_info['start_line']}-{func_info['end_line']}",
                'type': func_info['type']
            }
        
        # 添加类方法映射
        for class_name, class_info in self.classes.items():
            chatgpt_index['class_methods'][class_name] = {
                'methods': class_info['methods'][:20],  # 每个类最多20个方法
                'total_methods': len(class_info['methods'])
            }
        
        # 添加函数定位信息（按名称）
        for func_name, func_info in self.functions.items():
            chatgpt_index['function_locations'][func_name] = {
                'chunk': func_info['chunk_file'],
                'line': func_info['start_line'],
                'address': func_info['address']
            }
        
        # 输出精简 JSON
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(chatgpt_index, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] ChatGPT 专用索引已生成: {output_path}")
        print(f"  文件大小: {output_path.stat().st_size / 1024:.2f} KB")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='IDA .lst 文件结构化索引生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python generate_ida_index.py --input "切分输出目录" --output "ida_structured_index.json"
  
  # 生成完整索引
  python generate_ida_index.py --input "切分输出" --output "ida_full_index.json" --full
  
  # 生成 ChatGPT 专用索引
  python generate_ida_index.py --input "切分输出" --output "chatgpt_index.json" --chatgpt
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='切分输出目录路径'
    )
    
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='输出索引文件路径'
    )
    
    parser.add_argument(
        '--full',
        action='store_true',
        help='生成完整索引（包含所有信息）'
    )
    
    parser.add_argument(
        '--chatgpt',
        action='store_true',
        help='生成 ChatGPT 专用索引（精简版）'
    )
    
    args = parser.parse_args()
    
    try:
        # 创建索引生成器
        generator = IDAIndexGenerator(args.input)
        
        # 解析所有文件
        generator.parse_all_parts()
        
        # 生成索引
        if args.full:
            generator.generate_structured_index(args.output)
        elif args.chatgpt:
            generator.generate_chatgpt_index(args.output)
        else:
            # 默认生成两种索引
            generator.generate_structured_index(args.output)
            chatgpt_output = Path(args.output).parent / 'chatgpt_quick_index.json'
            generator.generate_chatgpt_index(str(chatgpt_output))
        
        print("\n" + "="*60)
        print("[OK] 索引生成完成！")
        print("="*60)
        
    except Exception as e:
        print(f"\n[ERROR] 错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()