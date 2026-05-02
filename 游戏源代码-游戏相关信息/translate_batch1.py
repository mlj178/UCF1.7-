import re
import os
import json
import time
import urllib.request
import urllib.parse

INPUT_DIR = r"d:\trae_project\UCF1.7修改大全\游戏源代码-游戏相关信息\类"
TRANSLATION_CACHE = r"d:\trae_project\UCF1.7修改大全\游戏源代码-游戏相关信息\translation_cache.json"

# Load cache
if os.path.exists(TRANSLATION_CACHE):
    with open(TRANSLATION_CACHE, 'r', encoding='utf-8') as f:
        cache = json.load(f)
else:
    cache = {}

def translate_term(text):
    """Translate using MyMemory free API"""
    if text in cache:
        return cache[text]
    
    try:
        url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair=en|zh-CN"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if 'responseData' in data and 'translatedText' in data['responseData']:
                result = data['responseData']['translatedText']
                cache[text] = result
                return result
    except Exception as e:
        print(f"    API error: {e}")
    
    cache[text] = text
    return text

def process_file(filepath):
    """Process one MD file, translate all terms"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all terms in parentheses: （xxx）
    # Replace English terms with translated versions
    def replace_term(match):
        full = match.group(0)
        inner = match.group(1)
        
        # Skip if already mostly Chinese
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', inner))
        total_chars = len(inner)
        if chinese_chars > total_chars * 0.5:
            return full
        
        # Translate the term
        translated = translate_term(inner)
        return f"（{translated}）"
    
    new_content = re.sub(r'（([^）]+)）', replace_term, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

# Process batch 1: part001, part002, part003
batch_files = ['classes_part001.md', 'classes_part002.md', 'classes_part003.md']

for fname in batch_files:
    fpath = os.path.join(INPUT_DIR, fname)
    if os.path.exists(fpath):
        print(f"Processing {fname}...")
        process_file(fpath)
        print(f"  Done: {fname}")
        
        # Save cache
        with open(TRANSLATION_CACHE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
        
        time.sleep(1)

print(f"\nBatch 1 complete. Cache size: {len(cache)} terms")
