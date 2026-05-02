import re
import os
import json
import time
import urllib.request
import urllib.parse

INPUT_DIR = r"d:\trae_project\UCF1.7修改大全\游戏源代码-游戏相关信息\类"
CACHE_FILE = r"d:\trae_project\UCF1.7修改大全\游戏源代码-游戏相关信息\translation_cache.json"

# CF射击游戏专业术语词典
CF_DICT = {
    'Vector3': '三维向量', 'Vector2': '二维向量', 'Vector4': '四维向量',
    'Quaternion': '四元数', 'GameObject': '游戏对象', 'Transform': '变换',
    'MonoBehaviour': 'MonoBehaviour', 'Rigidbody': '刚体', 'Collider': '碰撞器',
    'Renderer': '渲染器', 'Camera': '摄像机', 'Light': '光照',
    'Audio': '音频', 'Animation': '动画', 'Animator': '动画器',
    'ParticleSystem': '粒子系统', 'Sprite': '精灵', 'Texture': '纹理',
    'Material': '材质', 'Shader': '着色器', 'Mesh': '网格',
    'Scene': '场景', 'Prefab': '预制体', 'Coroutine': '协程',
    'Effect': '特效', 'Fx': '特效', 'Mdl': '模型', 'Cmr': '摄像机',
    'WPN': '武器', 'Wpn': '武器', 'Gun': '枪械', 'Rifle': '步枪',
    'Sniper': '狙击枪', 'MachineGun': '机枪', 'SubmachineGun': '冲锋枪',
    'ShotGun': '霰弹枪', 'Pistol': '手枪', 'Knife': '近战武器',
    'Grenade': '手雷', 'FlashBang': '闪光弹', 'SmokeGrenade': '烟雾弹',
    'Clip': '弹匣', 'Ammo': '弹药', 'Bullet': '子弹',
    'Shoot': '射击', 'Shot': '射击', 'Fire': '开火',
    'Reload': '换弹', 'Perturb': '扰动', 'Recoil': '后坐力',
    'WallShot': '穿射', 'Crosshair': '准星', 'Sight': '瞄准镜',
    'Zoom': '瞄准', 'FOV': '视野', 'Damage': '伤害', 'Brain': '爆头',
    'Head': '头部', 'Neck': '颈部', 'Chest': '胸部', 'Abdomen': '腹部',
    'Arm': '手臂', 'Hand': '手部', 'Leg': '腿部', 'Foot': '脚部',
    'Body': '身体', 'Helmet': '头盔', 'Armor': '护甲', 'Cloth': '服装',
    'Nano': '纳米', 'NanoGhost': '纳米幽灵', 'Ghost': '幽灵',
    'Blade': '刀锋', 'SecKill': '秒杀', 'Hero': '英雄',
    'Human': '人类', 'Zombie': '僵尸', 'Mutation': '变异',
    'Biochemical': '生化', 'Variant': '变异体', 'Infection': '感染',
    'MultiKill': '多杀', 'Respawn': '重生', 'Spawn': '出生',
    'Round': '回合', 'Observer': '观察者', 'ViewModel': '第一人称模型',
    'NickName': '昵称', 'Rank': '排名', 'PlayerID': '玩家ID',
    'Hit': '命中', 'HitEffect': '命中特效', 'HitSound': '命中音效',
    'Kill': '击杀', 'Death': '死亡', 'KillMsg': '击杀信息',
    'Icon': '图标', 'Select': '选择', 'Bag': '背包', 'Slot': '槽位',
    'ChangeWeapon': '切换武器', 'Rapid': '快速', 'Anim': '动画',
    'Upper': '上半身', 'Lower': '下半身', 'Side': '侧面',
    'Posture': '姿态', 'Stand': '站立', 'Crouch': '蹲下',
    'Idle': '待机', 'Floating': '浮空', 'Air': '空中',
    'Ground': '地面', 'Grounded': '着地', 'Fall': '坠落',
    'Jump': '跳跃', 'Climb': '攀爬', 'Stair': '楼梯',
    'MoveSpeed': '移动速度', 'Acceleration': '加速度',
    'Velocity': '速度', 'Gravity': '重力', 'Power': '力度',
    'Yaw': '偏航角', 'Pitch': '俯仰角', 'EulerAngle': '欧拉角',
    'Variantion': '变化', 'Factor': '系数', 'Ratio': '比率',
    'Penalty': '惩罚', 'Limited': '限制',
}

# 加载缓存
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        cache = json.load(f)
else:
    cache = {}

def translate_batch_api(terms):
    """批量翻译，每批最多500字符"""
    if not terms:
        return {}
    
    # 分批，每批总长度不超过450字符（留余量）
    batches = []
    current_batch = []
    current_length = 0
    
    for term in terms:
        term_len = len(term) + 3  # +3 for " | "
        if current_length + term_len > 450 and current_batch:
            batches.append(current_batch)
            current_batch = [term]
            current_length = term_len
        else:
            current_batch.append(term)
            current_length += term_len
    
    if current_batch:
        batches.append(current_batch)
    
    results = {}
    for batch in batches:
        text = " | ".join(batch)
        try:
            url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair=en|zh-CN"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode('utf-8'))
                if 'responseData' in data and 'translatedText' in data['responseData']:
                    translated = data['responseData']['translatedText']
                    translated_parts = translated.split(" | ")
                    for i, term in enumerate(batch):
                        if i < len(translated_parts):
                            results[term] = translated_parts[i]
                        else:
                            results[term] = term
                else:
                    for term in batch:
                        results[term] = term
        except Exception as e:
            print(f"    API错误: {e}", flush=True)
            for term in batch:
                results[term] = term
        time.sleep(1)  # 限速
    
    return results

def process_file(filepath):
    """处理一个MD文件"""
    fname = os.path.basename(filepath)
    print(f"处理 {fname}...", flush=True)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找出所有需要翻译的术语
    terms_to_translate = []
    for match in re.finditer(r'（([^）]+)）', content):
        inner = match.group(1)
        chinese_count = len(re.findall(r'[\u4e00-\u9fff]', inner))
        if chinese_count < len(inner) * 0.5:
            if inner not in CF_DICT and inner not in cache:
                terms_to_translate.append(inner)
    
    # 去重但保持顺序
    seen = set()
    unique_terms = []
    for t in terms_to_translate:
        if t not in seen:
            seen.add(t)
            unique_terms.append(t)
    
    print(f"  找到 {len(unique_terms)} 个需要翻译的术语", flush=True)
    
    # 批量翻译
    if unique_terms:
        results = translate_batch_api(unique_terms)
        cache.update(results)
        # 保存缓存
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
        print(f"  翻译完成，缓存总数: {len(cache)}", flush=True)
    
    # 替换术语
    def replace_term(match):
        inner = match.group(1)
        if inner in CF_DICT:
            return f"（{CF_DICT[inner]}）"
        if inner in cache:
            return f"（{cache[inner]}）"
        return match.group(0)
    
    new_content = re.sub(r'（([^）]+)）', replace_term, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✓ 完成: {fname}", flush=True)

# 处理所有文件
files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith('.md')])
print(f"共 {len(files)} 个文件需要处理\n", flush=True)

for fname in files:
    fpath = os.path.join(INPUT_DIR, fname)
    process_file(fpath)
    print()

print(f"\n✅ 全部完成! 缓存术语数: {len(cache)}", flush=True)
