# -*- coding: utf-8 -*-
import re

# 测试行
test_lines = [
    '<div class="field-item"><span class="field-type">float</span> defaultMoveSpeed</div>',
    '<div class="field-item"><span class="field-type">List<CharacterModel></span> characters</div>',
    '<div class="field-item"><span class="field-type">Action<Player></span> StartRespawn_Listener</div>',
]

for line in test_lines:
    print(f"Line: {line}")
    # 尝试匹配字段名
    match1 = re.search(r'</span>\s*(\w+)\s*$', line.rstrip())
    print(f"  Match1 (</span>\\s*(\\w+)\\s*$): {match1.group(1) if match1 else 'None'}")
    
    # 尝试另一种方式
    match2 = re.search(r'>\s*(\w+)\s*</div>', line)
    print(f"  Match2 (>\\s*(\\w+)\\s*</div>): {match2.group(1) if match2 else 'None'}")
    print()
