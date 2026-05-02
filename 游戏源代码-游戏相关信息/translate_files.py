import re
import os
import json
import time
import urllib.request
import urllib.parse
import sys

INPUT_DIR = r"d:\trae_project\UCF1.7修改大全\游戏源代码-游戏相关信息\类"
CACHE_FILE = r"d:\trae_project\UCF1.7修改大全\游戏源代码-游戏相关信息\translation_cache.json"

# Load cache
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        cache = json.load(f)
else:
    cache = {}

def translate_batch(terms):
    if not terms:
        return {}
    text = " | ".join(terms)
    try:
        url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair=en|zh-CN"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            if 'responseData' in data and 'translatedText' in data['responseData']:
                translated = data['responseData']['translatedText']
                results = translated.split(" | ")
                return dict(zip(terms, results))
    except Exception as e:
        print(f"  API error: {e}", flush=True)
    return None

def process_file(filepath):
    fname = os.path.basename(filepath)
    print(f"Processing {fname}...", flush=True)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    terms_to_translate = []
    for match in re.finditer(r'（([^）]+)）', content):
        inner = match.group(1)
        chinese_count = len(re.findall(r'[\u4e00-\u9fff]', inner))
        if chinese_count < len(inner) * 0.5 and inner not in cache:
            terms_to_translate.append(inner)
    
    seen = set()
    unique_terms = []
    for t in terms_to_translate:
        if t not in seen:
            seen.add(t)
            unique_terms.append(t)
    
    print(f"  Found {len(unique_terms)} terms to translate", flush=True)
    
    for i in range(0, len(unique_terms), 20):
        batch = unique_terms[i:i+20]
        results = translate_batch(batch)
        if results:
            for term, translated in results.items():
                cache[term] = translated
        else:
            for term in batch:
                cache[term] = term
        time.sleep(1)
    
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
    
    def replace_term(match):
        inner = match.group(1)
        translated = cache.get(inner, inner)
        return f"（{translated}）"
    
    new_content = re.sub(r'（([^）]+)）', replace_term, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  Done: {fname}", flush=True)

# Process first 3 files
for i in range(1, 4):
    fpath = os.path.join(INPUT_DIR, f"classes_part{i:03d}.md")
    if os.path.exists(fpath):
        process_file(fpath)

print(f"\nBatch complete. Cache size: {len(cache)}", flush=True)
