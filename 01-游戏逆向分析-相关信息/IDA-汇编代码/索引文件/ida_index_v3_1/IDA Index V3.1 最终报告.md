# IDA Index V3.1 最终报告

## 一、目录和版本

**v3.1 完整目录**：
```
d:\trae_project\ucf1.7-modifier\01-游戏逆向分析-相关信息\IDA-汇编代码\切分输出\ida_index_v3_1\
├── ida_indexer_v3_1.py          # 主解析器（约1500行）
├── indexes\
│   ├── chatgpt_quick_index_v3_1.json  # 精简索引（53.8 MB）
│   ├── ida_functions.jsonl            # 函数索引（49852条）
│   ├── ida_classes.json               # 类索引（6124个）
│   ├── ida_methods.jsonl              # 方法索引（37438条）
│   ├── ida_data_symbols.jsonl         # 数据符号（87768条）
│   ├── ida_xrefs.jsonl                # XREF索引（595257条）
│   ├── dumpcs_classes.json            # dump.cs类（5563个）
│   ├── dumpcs_methods.jsonl           # dump.cs方法（33278条）
│   ├── dumpcs_fields.jsonl            # dump.cs字段（17609条）
│   ├── ida_dumpcs_map.jsonl           # IDA-dump.cs关联（37438条）
│   ├── validation_report.json         # 验证报告（JSON）
│   └ validation_report.txt            # 验证报告（TXT）
├── tools\
│   └ query_ida_index_v3_1.py          # 查询工具
└── tests\
    └ test_v3_1.py                     # 测试脚本
```

**metadata**：
- `index_version: 3.1`
- `based_on: 3.0`

---

## 二、修改的文件

| 文件 | 修改内容 |
|------|----------|
| `ida_indexer_v3_1.py` | 全部重写，实现所有核心修复 |
| `query_ida_index_v3_1.py` | 新建，默认只加载quick index |
| `test_v3_1.py` | 新建，覆盖所有修复点测试 |

---

## 三、测试通过数

**60 通过，0 失败**

---

## 四、扫描全部 42 个 chunk

✅ **42 个 chunk 全部扫描**

---

## 五、数量统计

| 类型 | 数量 |
|------|------|
| 函数总数 | 49852 |
| IL2CPP 命名函数 | 37438 |
| Native sub 函数 | 12414 |
| 类 | 6124 |
| 方法 | 37438 |
| 数据符号 | 87768 |
| XREF | 595257 |
| dump.cs 类 | 5563 |
| dump.cs 方法 | 33278 |
| dump.cs 字段 | 17609 |
| 跨分片函数 | 21 |

---

## 六、匹配数量

| 匹配类型 | 数量 |
|----------|------|
| 唯一精确 VA 匹配 | 26418 |
| 歧义精确 VA 匹配 | 172 |
| 唯一精确 RVA 匹配 | 0 |
| 歧义精确 RVA 匹配 | 0 |
| 精确名称匹配 | 1 |
| 候选匹配（fuzzy降级） | 4006 |
| 未匹配 IDA | 6841 |
| 未匹配 dump | 6860 |
| 带 ambiguity_candidates 的记录 | 5220 |

---

## 七、类覆盖问题

✅ **已消除**

- dump.cs 类 ID 采用 `namespace::class_name#TypeDefIndex` 格式
- class method_count 总和 = 33278，与 dumpcs_methods.jsonl 行数一致
- class field_count 总和 = 17609，与 dumpcs_fields.jsonl 行数一致

---

## 八、JSONL 最终重读验证结果

✅ **验证报告 stats_source = re_read_final_files**

- 0 个 JSONL 无效行
- 0 个重复地址
- 0 个未匹配 endp
- 0 个解析错误

---

## 九、抽查查询结果

| 查询 | 结果 |
|------|------|
| `WPN_Gun$$Damage` | ✅ 匹配 `WPN_Gun.Damage()`，VA=0x10B613D0，chunk=part3.chunk007，置信度100 |
| `RootMotion_FinalIK_Grounding$$get_pelvis` | ✅ 匹配 `Grounding.get_pelvis()`，命名空间 `RootMotion.FinalIK`，不再关联 GUISkin |
| `UnityEngine_Camera$$WorldToScreenPoint` | ✅ 匹配 `Camera.WorldToScreenPoint()`，命名空间 `UnityEngine` |
| `WPN_Gun` 类 | ✅ 61 个方法 |
| `FuncInfo` | ✅ 1895 个 FuncInfo 数据符号 |
| `outgoing_call` | ✅ 方向正确 |
| `outgoing_jump` | ✅ 方向正确 |

---

## 十、quick index 路径和大小

**路径**：
```
indexes/chatgpt_quick_index_v3_1.json
```

**大小**：53.8 MB

---

## 十一、查询工具启动耗时

**0.5 秒**（仅加载 quick index）

---

## 十二、尚存限制

1. **歧义精确 VA 匹配仍有 172 个**：这些是同一 VA 对应多个 dump.cs 方法且无法通过类名+方法名消歧的情况，已正确标记为 `matched=false, confidence=0, ambiguity_candidates`。

2. **未匹配 IDA 6841 个**：包括 12414 个 native sub 函数和部分无法匹配的 il2cpp_named 函数。

3. **未匹配 dump 6860 个**：dump.cs 中未在 IDA 中找到对应地址的方法。

4. **quick index 53.8 MB**：比预期稍大，但仍在合理范围内（<100MB）。

---

## 十三、核心修复确认

| 修复点 | 状态 |
|--------|------|
| 共享地址消歧（不默认选 candidates[0]） | ✅ |
| fuzzy 降级为候选（matched=false） | ✅ |
| dump.cs 类 ID 含 TypeDefIndex | ✅ |
| FuncInfo/HandlerType/UnwindMapEntry/TryBlockMapEntry 识别 | ✅ |
| XREF 方向修正（incoming/outgoing） | ✅ |
| JMP 正则修复（匹配 segment:address 格式） | ✅ |
| 验证报告重新读取最终文件 | ✅ |
| quick index 不包含错误确认的签名 | ✅ |
| 查询工具默认只加载 quick index | ✅ |
| 49852 函数保持 | ✅ |
| 21 跨分片函数保持 | ✅ |

---

## 十四、使用说明

### 查询工具

```bash
# 查询符号
python tools/query_ida_index_v3_1.py --symbol 'WPN_Gun$$Damage'

# 查询类
python tools/query_ida_index_v3_1.py --class 'WPN_Gun'

# 查询关键字
python tools/query_ida_index_v3_1.py --keyword 'Damage'

# 查询地址
python tools/query_ida_index_v3_1.py --address 0x10B613D0

# 查询 RVA
python tools/query_ida_index_v3_1.py --rva 0x00B613D0

# 显示 XREF（懒加载）
python tools/query_ida_index_v3_1.py --symbol 'WPN_Gun$$Damage' --xrefs
```

### 测试脚本

```bash
python tests/test_v3_1.py
```

---

**IDA Index V3.1 已完成全部修复和验证。**