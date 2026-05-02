import re
import os
import json
import time
import urllib.request
import urllib.parse

INPUT_DIR = r"d:\trae_project\UCF1.7修改大全\游戏源代码-游戏相关信息\类"
TRANSLATION_CACHE = r"d:\trae_project\UCF1.7修改大全\游戏源代码-游戏相关信息\translation_cache.json"
BATCH_SIZE = 20  # Translate 20 terms per API call

# Load cache
if os.path.exists(TRANSLATION_CACHE):
    with open(TRANSLATION_CACHE, 'r', encoding='utf-8') as f:
        cache = json.load(f)
else:
    cache = {}

# Extract all unique English terms from all MD files
all_terms = set()
for fname in sorted(os.listdir(INPUT_DIR)):
    if not fname.endswith('.md'):
        continue
    with open(os.path.join(INPUT_DIR, fname), 'r', encoding='utf-8') as f:
        content = f.read()
    matches = re.findall(r'（([^）]+)）', content)
    for m in matches:
        if re.search(r'[a-zA-Z]', m) and len(re.findall(r'[\u4e00-\u9fff]', m)) < len(m) * 0.5:
            all_terms.add(m.strip())

terms_list = sorted([t for t in all_terms if t not in cache])
print(f"Terms to translate: {len(terms_list)}")
print(f"Already cached: {len(cache)}")

def translate_batch(terms):
    """Translate a batch of terms using MyMemory API"""
    # Join terms with | separator
    text = " | ".join(terms)
    try:
        url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair=en|zh-CN"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            if 'responseData' in data and 'translatedText' in data['responseData']:
                translated = data['responseData']['translatedText']
                # Split by | and map back to original terms
                results = translated.split(" | ")
                return dict(zip(terms, results))
    except Exception as e:
        print(f"    API error: {e}")
    return None

# Process in batches
total = len(terms_list)
for i in range(0, total, BATCH_SIZE):
    batch = terms_list[i:i+BATCH_SIZE]
    batch_num = i // BATCH_SIZE + 1
    total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
    
    print(f"Batch {batch_num}/{total_batches}: {len(batch)} terms")
    
    results = translate_batch(batch)
    if results:
        for term, translated in results.items():
            cache[term] = translated
        for term, translated in results.items():
            print(f"  {term} -> {translated}")
    else:
        for term in batch:
            cache[term] = term
        print("  Failed, using original terms")
    
    # Save cache every 5 batches
    if batch_num % 5 == 0:
        with open(TRANSLATION_CACHE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
        print(f"  Cache saved ({len(cache)} terms)")
    
    time.sleep(1)  # Rate limit

# Final save
with open(TRANSLATION_CACHE, 'w', encoding='utf-8') as f:
    json.dump(cache, f, ensure_ascii=False, indent=2)

print(f"\nDone! Total cached: {len(cache)} terms")
