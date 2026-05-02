import re
import os
import json

INPUT_DIR = r"d:\trae_project\UCF1.7修改大全\游戏源代码-游戏相关信息\类"
OUTPUT_FILE = r"d:\trae_project\UCF1.7修改大全\游戏源代码-游戏相关信息\terms_to_translate.json"

# Collect all unique English terms from the MD files
all_terms = set()

for fname in sorted(os.listdir(INPUT_DIR)):
    if not fname.endswith('.md'):
        continue
    with open(os.path.join(INPUT_DIR, fname), 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find terms in parentheses that contain English
    # Pattern: （xxx） where xxx contains English letters
    matches = re.findall(r'（([^）]+)）', content)
    for m in matches:
        # Check if it contains English letters (not pure Chinese)
        if re.search(r'[a-zA-Z]', m):
            all_terms.add(m.strip())

# Also extract class names, field names, method names from original dump.cs
# to get a complete list
terms_list = sorted(list(all_terms))

print(f"Found {len(terms_list)} unique terms to translate")

# Save to JSON for batch processing
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(terms_list, f, ensure_ascii=False, indent=2)

print(f"Saved to {OUTPUT_FILE}")

# Show first 50 terms as sample
print("\nFirst 50 terms:")
for t in terms_list[:50]:
    print(f"  {t}")
