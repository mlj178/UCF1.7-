import re
import os
import json
import time
import urllib.request
import urllib.parse

INPUT_DIR = r"d:\trae_project\UCF1.7修改大全\游戏源代码-游戏相关信息\类"
TERMS_FILE = r"d:\trae_project\UCF1.7修改大全\游戏源代码-游戏相关信息\terms_to_translate.json"
TRANSLATION_CACHE = r"d:\trae_project\UCF1.7修改大全\游戏源代码-游戏相关信息\translation_cache.json"

# Load existing cache
if os.path.exists(TRANSLATION_CACHE):
    with open(TRANSLATION_CACHE, 'r', encoding='utf-8') as f:
        cache = json.load(f)
else:
    cache = {}

# Load terms
with open(TERMS_FILE, 'r', encoding='utf-8') as f:
    all_terms = json.load(f)

# Filter: only translate terms not in cache
terms_to_translate = [t for t in all_terms if t not in cache]

print(f"Total terms: {len(all_terms)}")
print(f"Already cached: {len(cache)}")
print(f"Need to translate: {len(terms_to_translate)}")

def translate_via_api(text):
    """Use free translation API"""
    try:
        url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair=en|zh-CN"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if 'responseData' in data and 'translatedText' in data['responseData']:
                return data['responseData']['translatedText']
    except:
        pass
    return text

# Batch translate - 50 terms per batch to avoid rate limiting
BATCH_SIZE = 50
total_batches = (len(terms_to_translate) + BATCH_SIZE - 1) // BATCH_SIZE

for i in range(0, len(terms_to_translate), BATCH_SIZE):
    batch = terms_to_translate[i:i+BATCH_SIZE]
    batch_num = i // BATCH_SIZE + 1
    
    print(f"\nBatch {batch_num}/{total_batches} ({len(batch)} terms)")
    
    for term in batch:
        if term not in cache:
            translated = translate_via_api(term)
            cache[term] = translated
            print(f"  {term} -> {translated}")
            time.sleep(0.3)  # Rate limit
    
    # Save cache after each batch
    with open(TRANSLATION_CACHE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
    
    print(f"  Cache saved ({len(cache)} terms total)")

print(f"\nDone! Translated {len(terms_to_translate)} terms")
