#!/usr/bin/env python3
"""
split_ai_indexes.py
将大型索引文件切片为 <=10MB 的小文件，供 AI 上传使用。

用法:
    python tools/split_ai_indexes.py
    python tools/split_ai_indexes.py --input-dir indexes --output-dir ai_index_slices --max-mb 10
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# ==================== 字段白名单 ====================

FIELD_WHITELISTS = {
    'ida_xrefs.jsonl': [
        'source_function', 'source_address', 'source_rva', 'source_chunk',
        'target_function', 'target_address', 'target_rva', 'target_chunk',
        'xref_type', 'type',
    ],
    'ida_functions.jsonl': [
        'raw_name', 'resolved_class_name', 'class_name', 'namespace',
        'method_name', 'address', 'rva', 'chunk',
        'chunk_start_line', 'chunk_end_line',
        'part_source_start_line', 'part_source_end_line',
        'function_type', 'matched', 'confidence',
    ],
    'ida_data_symbols.jsonl': [
        'raw_name', 'name', 'symbol_name', 'address', 'rva', 'chunk',
        'segment', 'kind', 'type', 'line', 'source_line',
    ],
    'ida_dumpcs_map.jsonl': [
        'ida_name', 'ida_method', 'ida_address', 'ida_rva',
        'dump_name', 'dump_method', 'dump_rva',
        'class_name', 'full_type_name', 'method_name',
        'chunk', 'match_method', 'confidence', 'matched', 'ambiguity_candidates',
    ],
    'dumpcs_methods.jsonl': [
        'class_name', 'full_type_name', 'namespace', 'method_name', 'name',
        'return_type', 'parameters', 'signature', 'rva', 'va', 'offset', 'method_index',
    ],
    'dumpcs_fields.jsonl': [
        'class_name', 'full_type_name', 'namespace', 'field_name', 'name',
        'type', 'offset', 'attributes', 'is_static',
    ],
}

JSONL_FILES = list(FIELD_WHITELISTS.keys())

# chatgpt_quick_index_v3_1.json 顶层 key 分类
QUICK_INDEX_CORE_KEYS = {'metadata', 'chunk_routes', 'address_ranges'}

# route key -> 输出前缀
QUICK_INDEX_ROUTES = {
    'symbol_routes': 'quick_index_symbol_routes',
    'class_routes': 'quick_index_class_routes',
    'important_data_routes': 'quick_index_data_symbols',
}


def filter_fields(obj, whitelist):
    """根据白名单生成精简对象，只保留白名单中存在的字段"""
    return {k: obj[k] for k in whitelist if k in obj}


def split_jsonl_stream(input_path, output_dir, base_name, whitelist, max_bytes, warnings):
    """
    流式读取 JSONL，按大小切片输出。
    返回 (parts_info, input_line_count, output_line_count, missing_field_count)
    """
    parts = []
    input_line_count = 0
    output_line_count = 0
    missing_field_count = 0
    missing_fields_seen = set()

    part_index = 0
    current_size = 0
    current_lines = 0
    current_file = None
    current_path = None

    def open_new_part():
        nonlocal part_index, current_size, current_lines, current_file, current_path
        if current_file:
            current_file.close()
            parts.append({
                'file': os.path.basename(current_path),
                'size_bytes': current_size,
                'line_count': current_lines,
                'source_file': base_name,
                'part_index': part_index,
            })
        part_index += 1
        current_size = 0
        current_lines = 0
        current_path = os.path.join(output_dir, f'{base_name}.part{part_index:03d}.jsonl')
        current_file = open(current_path, 'w', encoding='utf-8')

    open_new_part()

    with open(input_path, 'r', encoding='utf-8') as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            input_line_count += 1
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                warnings.append(f'{base_name}: line {line_no} JSON parse error, skipped')
                continue

            # 统计缺失字段
            for key in whitelist:
                if key not in obj:
                    missing_field_count += 1
                    missing_fields_seen.add(key)

            filtered = filter_fields(obj, whitelist)
            out_line = json.dumps(filtered, ensure_ascii=False) + '\n'
            out_bytes = len(out_line.encode('utf-8'))

            # 单行超过阈值：单独写入一个 part
            if out_bytes > max_bytes:
                if current_lines > 0:
                    open_new_part()
                current_file.write(out_line)
                current_size += out_bytes
                current_lines += 1
                output_line_count += 1
                warnings.append(
                    f'{base_name}: line {line_no} exceeds {max_bytes} bytes '
                    f'({out_bytes} bytes), written as standalone part'
                )
                open_new_part()
            else:
                if current_size + out_bytes > max_bytes and current_lines > 0:
                    open_new_part()
                current_file.write(out_line)
                current_size += out_bytes
                current_lines += 1
                output_line_count += 1

    # 关闭最后一个 part
    if current_file:
        current_file.close()
        if current_lines > 0:
            parts.append({
                'file': os.path.basename(current_path),
                'size_bytes': current_size,
                'line_count': current_lines,
                'source_file': base_name,
                'part_index': part_index,
            })
        else:
            os.remove(current_path)

    if missing_fields_seen:
        warnings.append(
            f'{base_name}: missing whitelist fields: {sorted(missing_fields_seen)}'
        )

    return parts, input_line_count, output_line_count, missing_field_count


def split_dict_to_jsonl(data, output_dir, out_prefix, max_bytes, warnings, source_name):
    """
    将 dict 转成 JSONL 流式写入，按大小切片。
    每行格式: {"key": ..., "value": ...}
    返回 (parts_info, total_records)
    """
    parts = []
    total_records = 0

    part_index = 0
    current_size = 0
    current_lines = 0
    current_file = None
    current_path = None

    def open_new_part():
        nonlocal part_index, current_size, current_lines, current_file, current_path
        if current_file:
            current_file.close()
            parts.append({
                'file': os.path.basename(current_path),
                'size_bytes': current_size,
                'line_count': current_lines,
                'source_file': source_name,
                'part_index': part_index,
            })
        part_index += 1
        current_size = 0
        current_lines = 0
        current_path = os.path.join(output_dir, f'{out_prefix}.part{part_index:03d}.jsonl')
        current_file = open(current_path, 'w', encoding='utf-8')

    open_new_part()

    for key, value in data.items():
        total_records += 1
        obj = {'key': key, 'value': value}
        out_line = json.dumps(obj, ensure_ascii=False) + '\n'
        out_bytes = len(out_line.encode('utf-8'))

        if out_bytes > max_bytes:
            if current_lines > 0:
                open_new_part()
            current_file.write(out_line)
            current_size += out_bytes
            current_lines += 1
            warnings.append(
                f'{source_name}/{out_prefix}: key "{key}" exceeds {max_bytes} bytes '
                f'({out_bytes} bytes), written as standalone part'
            )
            open_new_part()
        else:
            if current_size + out_bytes > max_bytes and current_lines > 0:
                open_new_part()
            current_file.write(out_line)
            current_size += out_bytes
            current_lines += 1

    if current_file:
        current_file.close()
        if current_lines > 0:
            parts.append({
                'file': os.path.basename(current_path),
                'size_bytes': current_size,
                'line_count': current_lines,
                'source_file': source_name,
                'part_index': part_index,
            })
        else:
            os.remove(current_path)

    return parts, total_records


def process_quick_index(input_path, output_dir, max_bytes, warnings):
    """
    处理 chatgpt_quick_index_v3_1.json:
    1. 提取 core 到 quick_index_core.json
    2. 将 symbol_routes / class_routes / important_data_routes 转 JSONL 切片
    返回 (core_size, route_infos)
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. 提取 core
    core = {k: data[k] for k in QUICK_INDEX_CORE_KEYS if k in data}
    missing_core = QUICK_INDEX_CORE_KEYS - set(data.keys())
    if missing_core:
        warnings.append(f'quick_index: missing core keys: {sorted(missing_core)}')

    core_path = os.path.join(output_dir, 'quick_index_core.json')
    with open(core_path, 'w', encoding='utf-8') as f:
        json.dump(core, f, ensure_ascii=False, indent=2)
    core_size = os.path.getsize(core_path)

    # 2. 切片 route 结构
    route_infos = {}
    for route_key, out_prefix in QUICK_INDEX_ROUTES.items():
        if route_key in data and isinstance(data[route_key], dict):
            parts, total_records = split_dict_to_jsonl(
                data[route_key], output_dir, out_prefix, max_bytes, warnings,
                f'quick_index/{route_key}'
            )
            route_infos[route_key] = {
                'output_prefix': out_prefix,
                'part_count': len(parts),
                'total_records': total_records,
                'parts': parts,
            }
        else:
            warnings.append(f'quick_index: route key "{route_key}" not found or not dict')

    # 3. 检查是否有其他未处理的 dict 顶层 key
    known_keys = QUICK_INDEX_CORE_KEYS | set(QUICK_INDEX_ROUTES.keys())
    extra_keys = set(data.keys()) - known_keys
    if extra_keys:
        warnings.append(f'quick_index: unprocessed top-level keys: {sorted(extra_keys)}')

    return core_size, route_infos


def generate_manifest(output_dir, jsonl_infos, quick_core_size, quick_route_infos,
                      max_part_bytes, input_dir, warnings):
    """生成 manifest.json"""
    manifest = {
        'generated_at': datetime.now().isoformat(),
        'max_part_size_bytes': max_part_bytes,
        'input_dir': str(input_dir),
        'input_files': JSONL_FILES + ['chatgpt_quick_index_v3_1.json'],
        'jsonl_files': {},
        'quick_index': {
            'core_file': 'quick_index_core.json',
            'core_size_bytes': quick_core_size,
            'routes': {},
        },
    }

    for base_name, info in jsonl_infos.items():
        manifest['jsonl_files'][base_name] = {
            'input_line_count': info['input_line_count'],
            'output_line_count': info['output_line_count'],
            'part_count': len(info['parts']),
            'missing_field_count': info['missing_field_count'],
            'parts': info['parts'],
        }

    for route_key, info in quick_route_infos.items():
        manifest['quick_index']['routes'][route_key] = {
            'output_prefix': info['output_prefix'],
            'part_count': info['part_count'],
            'total_records': info['total_records'],
            'parts': info['parts'],
        }

    manifest_path = os.path.join(output_dir, 'manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    return manifest


def validate_output(output_dir, manifest, input_dir, max_bytes):
    """
    验证输出结果，返回 (passed, checks)
    """
    checks = []
    all_passed = True

    def check(name, condition, detail=''):
        nonlocal all_passed
        status = 'PASS' if condition else 'FAIL'
        if not condition:
            all_passed = False
        checks.append({'name': name, 'status': status, 'detail': detail})

    # 1. 所有输出文件都在 ai_index_slices/ 根目录下
    output_path = Path(output_dir)
    subdirs = [p for p in output_path.iterdir() if p.is_dir()]
    check('no_subdirectories', len(subdirs) == 0,
          f'found subdirs: {[d.name for d in subdirs]}' if subdirs else '')

    # 2. 没有按 class/chunk 生成的分散文件
    all_files = [p.name for p in output_path.iterdir() if p.is_file()]
    bad_patterns = ['by_class', 'by_chunk', 'by_source', 'by_target']
    bad_files = [f for f in all_files if any(bp in f for bp in bad_patterns)]
    check('no_scattered_files', len(bad_files) == 0,
          f'found: {bad_files}' if bad_files else '')

    # 3. 每个输出 part 文件 <= 10MB
    max_mb = max_bytes / (1024 * 1024)
    oversized = []
    for f in all_files:
        if f.startswith('split_validation_report') or f == 'manifest.json':
            continue
        fpath = os.path.join(output_dir, f)
        fsize = os.path.getsize(fpath)
        if fsize > max_bytes:
            oversized.append(f'{f} ({fsize / (1024*1024):.1f}MB)')
    check('all_parts_under_limit', len(oversized) == 0,
          f'oversized: {oversized}' if oversized else '')

    # 4. 所有输出 JSONL 每行都能 json.loads
    jsonl_parse_errors = []
    for f in all_files:
        if not f.endswith('.jsonl'):
            continue
        fpath = os.path.join(output_dir, f)
        with open(fpath, 'r', encoding='utf-8') as fh:
            for line_no, line in enumerate(fh, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    json.loads(line)
                except json.JSONDecodeError:
                    jsonl_parse_errors.append(f'{f}:{line_no}')
    check('all_jsonl_valid', len(jsonl_parse_errors) == 0,
          f'parse errors: {jsonl_parse_errors[:10]}' if jsonl_parse_errors else '')

    # 5. 源 JSONL 行数与输出总行数一致
    line_count_mismatches = []
    for base_name, info in manifest['jsonl_files'].items():
        src_path = os.path.join(input_dir, base_name)
        if not os.path.exists(src_path):
            line_count_mismatches.append(f'{base_name}: source not found')
            continue
        # 统计源文件非空行数
        src_count = 0
        with open(src_path, 'r', encoding='utf-8') as fh:
            for line in fh:
                if line.strip():
                    src_count += 1
        out_count = info['output_line_count']
        if src_count != out_count:
            line_count_mismatches.append(
                f'{base_name}: source={src_count} output={out_count}'
            )
    check('line_counts_match', len(line_count_mismatches) == 0,
          f'mismatches: {line_count_mismatches}' if line_count_mismatches else '')

    # 6. quick_index_core.json 可以 json.load
    core_path = os.path.join(output_dir, 'quick_index_core.json')
    core_ok = False
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                json.load(f)
            core_ok = True
        except Exception:
            pass
    check('quick_index_core_valid', core_ok)

    # 7. quick_index route 记录数一致
    route_mismatches = []
    quick_src_path = os.path.join(input_dir, 'chatgpt_quick_index_v3_1.json')
    if os.path.exists(quick_src_path):
        with open(quick_src_path, 'r', encoding='utf-8') as f:
            qi_data = json.load(f)
        for route_key, info in manifest['quick_index']['routes'].items():
            if route_key in qi_data and isinstance(qi_data[route_key], dict):
                src_count = len(qi_data[route_key])
                out_count = info['total_records']
                if src_count != out_count:
                    route_mismatches.append(
                        f'{route_key}: source={src_count} output={out_count}'
                    )
    check('quick_index_route_counts', len(route_mismatches) == 0,
          f'mismatches: {route_mismatches}' if route_mismatches else '')

    # 8. 统计每个源文件的 part 数量
    part_summary = {}
    for base_name, info in manifest['jsonl_files'].items():
        part_summary[base_name] = info['part_count']
    for route_key, info in manifest['quick_index']['routes'].items():
        part_summary[f'quick_index/{route_key}'] = info['part_count']

    return all_passed, checks, part_summary


def main():
    parser = argparse.ArgumentParser(
        description='将大型索引文件切片为 <=10MB 的小文件，供 AI 上传使用。'
    )
    parser.add_argument('--input-dir', default='indexes',
                        help='源文件目录 (默认: indexes)')
    parser.add_argument('--output-dir', default='ai_index_slices',
                        help='输出目录 (默认: ai_index_slices)')
    parser.add_argument('--max-mb', type=float, default=10,
                        help='每个 part 最大 MB (默认: 10，实际阈值 95%%)')
    args = parser.parse_args()

    input_dir = os.path.abspath(args.input_dir)
    output_dir = os.path.abspath(args.output_dir)
    max_bytes = int(args.max_mb * 1024 * 1024 * 0.95)
    max_hard = int(args.max_mb * 1024 * 1024)

    print(f'输入目录: {input_dir}')
    print(f'输出目录: {output_dir}')
    print(f'切片阈值: {max_bytes / (1024*1024):.2f} MB (硬限 {args.max_mb} MB)')
    print()

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    warnings = []
    jsonl_infos = {}

    # ===== 处理 6 个 JSONL 文件 =====
    for base_name in JSONL_FILES:
        src_path = os.path.join(input_dir, base_name)
        if not os.path.exists(src_path):
            warnings.append(f'{base_name}: source file not found, skipped')
            jsonl_infos[base_name] = {
                'parts': [],
                'input_line_count': 0,
                'output_line_count': 0,
                'missing_field_count': 0,
            }
            continue

        whitelist = FIELD_WHITELISTS[base_name]
        file_size_mb = os.path.getsize(src_path) / (1024 * 1024)
        print(f'[1/7 类] 处理 {base_name} ({file_size_mb:.1f} MB) ...')

        t0 = time.time()
        parts, in_count, out_count, missing = split_jsonl_stream(
            src_path, output_dir, base_name.replace('.jsonl', ''), whitelist,
            max_bytes, warnings
        )
        elapsed = time.time() - t0

        jsonl_infos[base_name] = {
            'parts': parts,
            'input_line_count': in_count,
            'output_line_count': out_count,
            'missing_field_count': missing,
        }
        print(f'  -> {len(parts)} parts, {in_count} lines in, {out_count} lines out, '
              f'{elapsed:.1f}s')

    # ===== 处理 chatgpt_quick_index_v3_1.json =====
    qi_path = os.path.join(input_dir, 'chatgpt_quick_index_v3_1.json')
    if os.path.exists(qi_path):
        file_size_mb = os.path.getsize(qi_path) / (1024 * 1024)
        print(f'[7/7] 处理 chatgpt_quick_index_v3_1.json ({file_size_mb:.1f} MB) ...')
        t0 = time.time()
        core_size, route_infos = process_quick_index(
            qi_path, output_dir, max_bytes, warnings
        )
        elapsed = time.time() - t0
        total_parts = sum(r['part_count'] for r in route_infos.values())
        print(f'  -> core.json ({core_size / (1024*1024):.1f} MB) + {total_parts} route parts, '
              f'{elapsed:.1f}s')
    else:
        warnings.append('chatgpt_quick_index_v3_1.json: source file not found, skipped')
        core_size = 0
        route_infos = {}

    # ===== 生成 manifest =====
    print('\n生成 manifest.json ...')
    manifest = generate_manifest(
        output_dir, jsonl_infos, core_size, route_infos, max_bytes, input_dir, warnings
    )

    # ===== 验证 =====
    print('运行验证 ...')
    all_passed, checks, part_summary = validate_output(
        output_dir, manifest, input_dir, max_hard
    )

    # ===== 生成验证报告 =====
    report = {
        'generated_at': datetime.now().isoformat(),
        'overall': 'PASSED' if all_passed else 'FAILED',
        'checks': checks,
        'part_summary': part_summary,
        'warnings_count': len(warnings),
        'warnings': warnings,
    }

    report_json_path = os.path.join(output_dir, 'split_validation_report.json')
    with open(report_json_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    report_txt_path = os.path.join(output_dir, 'split_validation_report.txt')
    with open(report_txt_path, 'w', encoding='utf-8') as f:
        f.write('=' * 60 + '\n')
        f.write('切片验证报告\n')
        f.write('=' * 60 + '\n\n')
        f.write(f'时间: {report["generated_at"]}\n')
        f.write(f'结果: {report["overall"]}\n')
        f.write(f'警告数: {len(warnings)}\n\n')

        f.write('-' * 60 + '\n')
        f.write('验证项:\n')
        f.write('-' * 60 + '\n')
        for c in checks:
            f.write(f'  [{c["status"]}] {c["name"]}')
            if c['detail']:
                f.write(f' -- {c["detail"]}')
            f.write('\n')

        f.write('\n' + '-' * 60 + '\n')
        f.write('切片统计:\n')
        f.write('-' * 60 + '\n')
        for name, count in part_summary.items():
            f.write(f'  {name}: {count} parts\n')

        f.write('\n' + '-' * 60 + '\n')
        f.write(f'警告 ({len(warnings)} 条):\n')
        f.write('-' * 60 + '\n')
        for w in warnings:
            f.write(f'  - {w}\n')

        f.write('\n' + '=' * 60 + '\n')
        f.write(f'最终结果: {report["overall"]}\n')
        f.write('=' * 60 + '\n')

    # 打印结果
    print()
    print('=' * 60)
    for c in checks:
        status = '[OK]' if c['status'] == 'PASS' else '[XX]'
        print(f'  {status} {c["name"]}')
        if c['detail']:
            print(f'      {c["detail"]}')
    print()
    print(f'  警告: {len(warnings)} 条')
    print(f'  结果: {report["overall"]}')
    print('=' * 60)

    if all_passed:
        print('PASSED')
    else:
        print('FAILED')
        sys.exit(1)


if __name__ == '__main__':
    main()
