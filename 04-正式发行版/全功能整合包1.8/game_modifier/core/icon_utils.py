"""
图标透明背景处理工具模块（二次修复版）

提供统一的 PNG 转 ICO、透明背景处理、ICO 验证等功能。

关键修复：
1. 拆分 force_regenerate 为 force_ico_regenerate 和 force_background_removal
2. 已有有效 Alpha 时保留原始透明，不进行 flood fill
3. 使用 img.ico.sizes() 验证 ICO 多尺寸
4. 验证失败时返回 False 并删除错误 ICO
5. 种子点配置化，不盲目生成
6. 原子生成 app_icon.ico
7. 使用 with Image.open 避免文件句柄占用
"""
import os
import tempfile
import logging
from collections import deque
from typing import List, Tuple, Optional, Dict, Any

logger = logging.getLogger(__name__)

# 图标处理配置（按文件名设置）
# 只有确认图片没有有效 Alpha，并且确实存在封闭背景区域时才填写 extra_seed_ratios
ICON_PROCESSING_CONFIG = {
    "App Icon.png": {
        "background_hint": None,  # None 表示自动检测，不硬编码
        "tolerance": 30,
        "extra_seed_ratios": [],  # 空列表表示不使用额外种子点
    },
    "Window Icon.png": {
        "background_hint": None,  # None 表示自动检测，不硬编码
        "tolerance": 35,
        "extra_seed_ratios": [],  # 空列表表示不使用额外种子点
    },
}

# 预期 ICO 尺寸
EXPECTED_ICO_SIZES = [
    (16, 16),
    (24, 24),
    (32, 32),
    (48, 48),
    (64, 64),
    (128, 128),
    (256, 256),
]


def get_icon_config(filename: str) -> Dict[str, Any]:
    """
    获取图标处理配置
    
    Args:
        filename: 图标文件名（如 "App Icon.png")
    
    Returns:
        配置字典
    """
    # 提取文件名（不含路径）
    basename = os.path.basename(filename)
    
    # 查找配置
    if basename in ICON_PROCESSING_CONFIG:
        return ICON_PROCESSING_CONFIG[basename]
    
    # 默认配置
    return {
        "background_hint": None,
        "tolerance": 30,
        "extra_seed_ratios": [],
    }


def inspect_icon_image(path: str) -> Dict[str, Any]:
    """
    检查图标图像属性
    
    Args:
        path: PNG 文件路径
    
    Returns:
        包含图像属性的字典
    """
    from PIL import Image
    
    result = {
        'path': path,
        'exists': os.path.exists(path),
        'mode': None,
        'size': None,
        'alpha_range': None,
        'transparent_count': 0,
        'transparent_ratio': 0.0,
        'corner_colors': [],
        'corner_alpha': [],
        'has_valid_alpha': False,
        'background_color': None,
        'background_type': None,  # 'solid', 'checkerboard', 'complex', 'unknown'
    }
    
    if not result['exists']:
        logger.warning(f"[ICON] 文件不存在: {path}")
        return result
    
    try:
        # 使用 with 打开图像，避免文件句柄占用
        with Image.open(path) as source:
            # 获取原始模式
            original_mode = source.mode
            result['mode'] = original_mode
            result['size'] = source.size
            
            logger.info(f"[ICON] source={path}")
            logger.info(f"[ICON] original_mode={original_mode}")
            logger.info(f"[ICON] size={source.size}")
            
            # 转换为 RGBA 检查 Alpha
            if source.mode == 'RGBA':
                img = source
            elif source.mode == 'LA':
                img = source.convert('RGBA')
            elif source.mode == 'P':
                # P 模式可能有 transparency
                if 'transparency' in source.info:
                    img = source.convert('RGBA')
                else:
                    img = source.convert('RGBA')
            else:
                # RGB 或其他模式
                img = source.convert('RGBA')
            
            logger.info(f"[ICON] converted_mode=RGBA")
            
            # 检查 Alpha 通道
            alpha = img.getchannel('A')
            alpha_range = alpha.getextrema()
            result['alpha_range'] = alpha_range
            
            # 统计透明像素
            alpha_data = alpha.getdata()
            width, height = img.size
            total = width * height
            transparent_count = sum(1 for p in alpha_data if p == 0)
            result['transparent_count'] = transparent_count
            result['transparent_ratio'] = transparent_count / total
            
            logger.info(f"[ICON] alpha_range={alpha_range}")
            logger.info(f"[ICON] transparent_ratio={result['transparent_ratio']:.4f}")
            
            # 获取四角颜色和 Alpha
            pixels = img.load()
            corners = [
                (0, 0),
                (width - 1, 0),
                (0, height - 1),
                (width - 1, height - 1),
            ]
            
            result['corner_colors'] = [pixels[c[0], c[1]][:3] for c in corners]
            result['corner_alpha'] = [pixels[c[0], c[1]][3] for c in corners]
            logger.info(f"[ICON] corner_colors={result['corner_colors']}")
            logger.info(f"[ICON] corner_alpha={result['corner_alpha']}")
            
            # 判断是否有有效透明背景
            # 条件：
            # 1. Alpha 范围包含 0 和 255（有透明和不透明像素）
            # 2. 透明像素比例 > 5%
            # 3. 四角至少有一个透明
            if alpha_range[0] == 0 and alpha_range[1] == 255:
                if result['transparent_ratio'] > 0.05:
                    corner_transparent = any(a == 0 for a in result['corner_alpha'])
                    if corner_transparent:
                        result['has_valid_alpha'] = True
                        logger.info(f"[ICON] has_valid_alpha=True，保留原始透明背景")
            
            # 如果没有有效 Alpha，检测背景颜色
            if not result['has_valid_alpha']:
                # 检查四角颜色是否一致
                corner_colors = result['corner_colors']
                if len(corner_colors) == 4:
                    # 计算四角颜色差异
                    max_diff = max(
                        max(abs(corner_colors[i][j] - corner_colors[k][j]) 
                            for j in range(3) for k in range(4))
                        for i in range(4)
                    )
                    
                    if max_diff <= 30:  # 四角颜色相似
                        # 计算平均背景颜色
                        bg_r = sum(c[0] for c in corner_colors) // 4
                        bg_g = sum(c[1] for c in corner_colors) // 4
                        bg_b = sum(c[2] for c in corner_colors) // 4
                        result['background_color'] = (bg_r, bg_g, bg_b)
                        result['background_type'] = 'solid'
                        logger.info(f"[ICON] background_color={result['background_color']}")
                        logger.info(f"[ICON] background_type=solid")
                    elif max_diff <= 100:  # 四角颜色差异较大，可能是棋盘格
                        result['background_type'] = 'checkerboard'
                        logger.warning(f"[ICON] background_type=checkerboard，无法自动检测背景颜色")
                    else:  # 四角颜色差异很大，复杂背景
                        result['background_type'] = 'complex'
                        logger.warning(f"[ICON] background_type=complex，无法自动检测背景颜色")
                else:
                    result['background_type'] = 'unknown'
                    logger.warning(f"[ICON] background_type=unknown")
        
        return result
        
    except Exception as e:
        logger.exception(f"[ICON] 检查图像失败: {e}")
        return result


def load_icon_with_transparency(
    path: str,
    bg_color_hint: Optional[str] = None,
    tolerance: int = 30,
    extra_seeds: Optional[List[Tuple[int, int]]] = None,
    force_background_removal: bool = False
) -> Optional[Any]:
    """
    加载 PNG 图标并处理透明背景
    
    Args:
        path: PNG 文件路径
        bg_color_hint: 背景颜色提示 ('white', 'black', 'gray', None自动检测)
        tolerance: 颜色相似度容差 (0-255)
        extra_seeds: 额外的 flood fill 种子点列表 [(x, y), ...]
        force_background_removal: 是否强制重新处理背景（即使已有透明背景）
    
    Returns:
        PIL Image 对象 (RGBA 模式，带透明通道)
    
    注意：
        - 如果源 PNG 已有有效 Alpha（has_valid_alpha=True），默认保留原始透明，不进行 flood fill
        - 只有 force_background_removal=True 时才会强制重新处理
        - 透明像素的 RGB 底色可能是 (0,0,0,0)，不能以黑色为背景 flood fill，否则会删除黑色主体
    """
    from PIL import Image
    
    # 检查图像属性
    info = inspect_icon_image(path)
    
    if not info['exists']:
        return None
    
    try:
        # 使用 with 打开图像
        with Image.open(path) as source:
            # 统一转换为 RGBA
            if source.mode == 'RGBA':
                img = source.copy()
            elif source.mode == 'LA':
                img = source.convert('RGBA')
            elif source.mode == 'P':
                if 'transparency' in source.info:
                    img = source.convert('RGBA')
                else:
                    img = source.convert('RGBA')
            else:
                img = source.convert('RGBA')
            
            logger.info(f"[ICON] converted_mode=RGBA")
            
            # 如果已有有效透明背景且不强制重新处理，直接返回
            if info['has_valid_alpha'] and not force_background_removal:
                logger.info(f"[ICON] 保留原始透明背景，不进行 flood fill")
                return img
            
            # 需要处理背景
            logger.info(f"[ICON] 开始处理背景透明")
            
            pixels = img.load()
            width, height = img.size
            
            # 计算背景颜色
            bg_color = None
            
            # 优先使用配置的背景提示
            if bg_color_hint == 'white':
                bg_color = (255, 255, 255)
                logger.info(f"[ICON] 使用配置的背景提示: white")
            elif bg_color_hint == 'black':
                bg_color = (0, 0, 0)
                logger.info(f"[ICON] 使用配置的背景提示: black")
            elif bg_color_hint == 'gray':
                bg_color = (128, 128, 128)
                logger.info(f"[ICON] 使用配置的背景提示: gray")
            else:
                # 自动检测
                if info['background_type'] == 'solid' and info['background_color']:
                    bg_color = info['background_color']
                    logger.info(f"[ICON] 使用自动检测的背景颜色: {bg_color}")
                elif info['background_type'] in ('checkerboard', 'complex', 'unknown'):
                    # 无法检测背景颜色，停止处理
                    logger.error(f"[ICON] 无法检测背景颜色（{info['background_type']}），停止处理")
                    logger.error(f"[ICON] 请手动配置 bg_color_hint 或使用已有透明背景的 PNG")
                    return None
                else:
                    # 默认白色（但输出警告）
                    bg_color = (255, 255, 255)
                    logger.warning(f"[ICON] 无法检测背景颜色，默认使用白色（可能删除白色主体）")
            
            if bg_color is None:
                logger.error(f"[ICON] 无法确定背景颜色，停止处理")
                return None
            
            logger.info(f"[ICON] background_color={bg_color}")
            logger.info(f"[ICON] tolerance={tolerance}")
            
            # 准备种子点
            seeds = [
                (0, 0),
                (width - 1, 0),
                (0, height - 1),
                (width - 1, height - 1),
            ]
            
            # 添加额外种子点（用于内部镂空区域）
            if extra_seeds:
                # 安全检查种子点
                safe_seeds = []
                for seed in extra_seeds:
                    x, y = seed
                    # 越界检查
                    if x < 0 or x >= width or y < 0 or y >= height:
                        logger.warning(f"[ICON] 种子点越界: ({x}, {y})，跳过")
                        continue
                    # 颜色检查
                    pixel = pixels[x, y]
                    r, g, b = pixel[:3]
                    if is_similar_color(r, g, b, bg_color, tolerance):
                        safe_seeds.append(seed)
                        logger.info(f"[ICON] 种子点有效: ({x}, {y})")
                    else:
                        logger.warning(f"[ICON] 种子点颜色不符合背景: ({x}, {y}) RGB({r},{g},{b})，跳过")
                seeds.extend(safe_seeds)
            
            logger.info(f"[ICON] extra_seeds={extra_seeds if extra_seeds else 'None'}")
            logger.info(f"[ICON] total_seeds={len(seeds)}")
            
            # 使用优化的 flood fill
            img = flood_fill_transparency(img, bg_color, tolerance, seeds)
            
            # 验证结果
            alpha = img.getchannel('A')
            alpha_range = alpha.getextrema()
            alpha_data = alpha.getdata()
            total = width * height
            transparent_count = sum(1 for p in alpha_data if p == 0)
            transparent_ratio = transparent_count / total
            
            logger.info(f"[ICON] processed_alpha_range={alpha_range}")
            logger.info(f"[ICON] processed_transparent_ratio={transparent_ratio:.4f}")
            
            # 检查是否删除了主体（Alpha 最大值应为 255）
            if alpha_range[1] != 255:
                logger.error(f"[ICON] Alpha 最大值 {alpha_range[1]} != 255，可能删除了主体")
                return None
            
            return img
        
    except Exception as e:
        logger.exception(f"[ICON] 处理透明背景失败: {e}")
        return None


def is_similar_color(r: int, g: int, b: int, target: Tuple[int, int, int], tolerance: int) -> bool:
    """判断颜色是否相似"""
    return (
        abs(r - target[0]) <= tolerance and
        abs(g - target[1]) <= tolerance and
        abs(b - target[2]) <= tolerance
    )


def flood_fill_transparency(
    img: Any,
    bg_color: Tuple[int, int, int],
    tolerance: int,
    seeds: List[Tuple[int, int]]
) -> Any:
    """
    使用优化的 flood fill 处理透明背景
    
    Args:
        img: PIL Image 对象 (RGBA)
        bg_color: 背景颜色
        tolerance: 颜色相似度容差
        seeds: 种子点列表
    
    Returns:
        处理后的 PIL Image 对象
    """
    pixels = img.load()
    width, height = img.size
    
    # 使用 bytearray 作为 visited 数组（一维，性能更好）
    visited = bytearray(width * height)
    
    # 获取图像数据
    data = list(img.getdata())
    
    # 使用 deque 优化队列操作
    queue = deque()
    
    def process_pixel(x: int, y: int):
        """处理单个像素"""
        if x < 0 or x >= width or y < 0 or y >= height:
            return
        
        idx = y * width + x
        
        # 先检查 visited，避免重复处理
        if visited[idx]:
            return
        
        # 标记为已访问
        visited[idx] = 1
        
        # 获取颜色
        r, g, b, a = data[idx]
        
        # 只处理与背景颜色相似的像素
        if not is_similar_color(r, g, b, bg_color, tolerance):
            return
        
        # 设置为透明
        data[idx] = (r, g, b, 0)
        
        # 添加相邻像素到队列
        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))
    
    # 从所有种子点开始
    for seed in seeds:
        if not visited[seed[1] * width + seed[0]]:
            queue.append(seed)
    
    # 处理队列
    while queue:
        x, y = queue.popleft()
        process_pixel(x, y)
    
    # 更新图像数据
    img.putdata(data)
    
    return img


def save_ico_with_transparency(
    img: Any,
    output_path: str,
    sizes: Optional[List[Tuple[int, int]]] = None
) -> bool:
    """
    保存带透明通道的 ICO 文件
    
    Args:
        img: PIL Image 对象 (RGBA)
        output_path: 输出 ICO 文件路径
        sizes: 尺寸列表，默认 EXPECTED_ICO_SIZES
    
    Returns:
        是否成功（验证失败返回 False）
    """
    from PIL import Image
    
    if sizes is None:
        sizes = EXPECTED_ICO_SIZES
    
    try:
        # 确保图像是 RGBA
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 检查源图尺寸
        if img.size[0] < 256 or img.size[1] < 256:
            logger.warning(f"[ICON] 源图尺寸 {img.size} 小于 256x256，可能影响大尺寸ICO质量")
        
        # 直接从高分辨率原图保存多尺寸 ICO
        img.save(
            output_path,
            format='ICO',
            sizes=sizes
        )
        
        logger.info(f"[ICON] output={output_path}")
        logger.info(f"[ICON] ico_sizes={sizes}")
        
        # 验证生成的 ICO
        verification = verify_ico_transparency(output_path)
        
        # 只有验证通过才返回 True
        if verification.get('valid', False):
            logger.info(f"[ICON] ICO 验证通过")
            return True
        else:
            logger.error(f"[ICON] ICO 验证失败")
            # 删除错误的 ICO
            try:
                os.remove(output_path)
                logger.info(f"[ICON] 删除错误的 ICO: {output_path}")
            except Exception as e:
                logger.warning(f"[ICON] 删除错误的 ICO 失败: {e}")
            return False
        
    except Exception as e:
        logger.exception(f"[ICON] ICO 保存失败: {e}")
        # 删除错误的 ICO
        try:
            if os.path.exists(output_path):
                os.remove(output_path)
                logger.info(f"[ICON] 删除错误的 ICO: {output_path}")
        except Exception as e2:
            logger.warning(f"[ICON] 删除错误的 ICO 失败: {e2}")
        return False


def verify_ico_transparency(path: str) -> Dict[str, Any]:
    """
    验证 ICO 文件的透明度
    
    Args:
        path: ICO 文件路径
    
    Returns:
        验证结果字典，包含：
        - exists: 文件是否存在
        - sizes: 实际尺寸列表
        - frames: 每帧信息
        - all_sizes_present: 是否包含所有预期尺寸
        - all_frames_rgba: 是否所有帧为 RGBA
        - all_frames_have_transparency: 是否所有帧有透明像素
        - valid: 是否验证通过
    """
    from PIL import Image
    
    result = {
        'path': path,
        'exists': os.path.exists(path),
        'sizes': [],
        'frames': [],
        'all_sizes_present': False,
        'all_frames_rgba': False,
        'all_frames_have_transparency': False,
        'valid': False,
    }
    
    if not result['exists']:
        logger.warning(f"[ICON] ICO 文件不存在: {path}")
        return result
    
    try:
        # 使用 with 打开图像
        with Image.open(path) as img:
            # 使用 ICO 插件接口获取所有尺寸
            available_sizes = img.ico.sizes()
            result['sizes'] = list(available_sizes)
            
            logger.info(f"[ICON] ICO 实际尺寸: {available_sizes}")
            
            # 检查是否包含所有预期尺寸
            expected_set = set(EXPECTED_ICO_SIZES)
            actual_set = set(available_sizes)
            result['all_sizes_present'] = expected_set == actual_set
            
            if not result['all_sizes_present']:
                missing = expected_set - actual_set
                extra = actual_set - expected_set
                if missing:
                    logger.warning(f"[ICON] 缺少尺寸: {missing}")
                if extra:
                    logger.warning(f"[ICON] 多余尺寸: {extra}")
            
            # 检查每个尺寸
            all_rgba = True
            all_transparency = True
            
            for size in available_sizes:
                try:
                    # 使用 ICO 插件接口获取特定尺寸的图像
                    frame = img.ico.getimage(size)
                    
                    # 转换为 RGBA
                    if frame.mode != 'RGBA':
                        frame = frame.convert('RGBA')
                    
                    frame_info = {
                        'size': size,
                        'mode': frame.mode,
                        'alpha_range': None,
                        'transparent_count': 0,
                        'transparent_ratio': 0.0,
                        'has_transparency': False,
                    }
                    
                    # 检查 Alpha
                    alpha = frame.getchannel('A')
                    alpha_range = alpha.getextrema()
                    frame_info['alpha_range'] = alpha_range
                    
                    # 统计透明像素
                    alpha_data = alpha.getdata()
                    total = size[0] * size[1]
                    transparent_count = sum(1 for p in alpha_data if p == 0)
                    frame_info['transparent_count'] = transparent_count
                    frame_info['transparent_ratio'] = transparent_count / total
                    
                    # 检查是否有透明像素
                    if alpha_range[0] == 0:
                        frame_info['has_transparency'] = True
                    else:
                        all_transparency = False
                    
                    # 检查是否有不透明主体
                    if alpha_range[1] != 255:
                        logger.error(f"[ICON] size={size} Alpha 最大值 {alpha_range[1]} != 255，可能删除了主体")
                        all_transparency = False
                    
                    result['frames'].append(frame_info)
                    
                    logger.info(f"[ICON] size={size}, mode={frame.mode}, alpha_range={alpha_range}, transparent_ratio={frame_info['transparent_ratio']:.4f}")
                    
                except Exception as e:
                    logger.exception(f"[ICON] 处理尺寸 {size} 失败: {e}")
                    all_rgba = False
                    all_transparency = False
            
            result['all_frames_rgba'] = all_rgba
            result['all_frames_have_transparency'] = all_transparency
            
            # 判断是否验证通过
            # 条件：
            # 1. 所有预期尺寸存在
            # 2. 所有帧为 RGBA
            # 3. 所有帧有透明像素（Alpha 最小值为 0）
            # 4. 所有帧有不透明主体（Alpha 最大值为 255）
            result['valid'] = (
                result['all_sizes_present'] and
                result['all_frames_rgba'] and
                result['all_frames_have_transparency']
            )
            
            if result['valid']:
                logger.info(f"[ICON] verify_result=成功")
            else:
                logger.error(f"[ICON] verify_result=失败")
                logger.error(f"[ICON] all_sizes_present={result['all_sizes_present']}")
                logger.error(f"[ICON] all_frames_rgba={result['all_frames_rgba']}")
                logger.error(f"[ICON] all_frames_have_transparency={result['all_frames_have_transparency']}")
        
        return result
        
    except Exception as e:
        logger.exception(f"[ICON] ICO 验证失败: {e}")
        return result


def generate_app_icon_ico(
    app_icon_png: str,
    app_icon_ico: str,
    force_ico_regenerate: bool = True,
    force_background_removal: bool = False
) -> Optional[str]:
    """
    生成应用图标 ICO（原子操作）
    
    Args:
        app_icon_png: App Icon PNG 文件路径
        app_icon_ico: 输出 ICO 文件路径
        force_ico_regenerate: 是否强制重新生成 ICO
        force_background_removal: 是否强制重新处理背景
    
    Returns:
        生成的 ICO 文件路径，失败返回 None
    
    注意：
        - 使用原子操作：先生成临时 ICO，验证通过后覆盖正式 ICO
        - 如果源 PNG 已有有效 Alpha，默认保留原始透明，不进行 flood fill
        - 只有 force_background_removal=True 时才会强制重新处理背景
    """
    logger.info(f"[ICON] 开始生成 App Icon ICO")
    logger.info(f"[ICON] app_icon_png={app_icon_png}")
    logger.info(f"[ICON] app_icon_ico={app_icon_ico}")
    logger.info(f"[ICON] force_ico_regenerate={force_ico_regenerate}")
    logger.info(f"[ICON] force_background_removal={force_background_removal}")
    
    if not os.path.exists(app_icon_png):
        logger.error(f"[ICON] App Icon PNG 不存在")
        return None
    
    # 检查是否需要重新生成
    need_regenerate = force_ico_regenerate
    
    if not force_ico_regenerate and os.path.exists(app_icon_ico):
        # 比较修改时间
        png_mtime = os.path.getmtime(app_icon_png)
        ico_mtime = os.path.getmtime(app_icon_ico)
        if png_mtime <= ico_mtime:
            need_regenerate = False
            logger.info(f"[ICON] regenerated=False（ICO 比 PNG 新）")
    
    if not need_regenerate:
        # 验证现有 ICO
        verification = verify_ico_transparency(app_icon_ico)
        if verification.get('valid', False):
            logger.info(f"[ICON] 现有 ICO 验证通过，不需要重新生成")
            return app_icon_ico
        else:
            logger.warning(f"[ICON] 现有 ICO 验证失败，需要重新生成")
            need_regenerate = True
    
    if need_regenerate:
        # 获取配置
        config = get_icon_config(app_icon_png)
        
        # 计算种子点（从配置的 extra_seed_ratios）
        extra_seeds = None
        if config['extra_seed_ratios']:
            info = inspect_icon_image(app_icon_png)
            if info['size']:
                width, height = info['size']
                extra_seeds = [
                    (int(width * ratio[0]), int(height * ratio[1]))
                    for ratio in config['extra_seed_ratios']
                ]
        
        # 加载并处理透明背景
        img = load_icon_with_transparency(
            app_icon_png,
            bg_color_hint=config['background_hint'],
            tolerance=config['tolerance'],
            extra_seeds=extra_seeds,
            force_background_removal=force_background_removal
        )
        
        if img is None:
            logger.error(f"[ICON] App Icon 加载失败")
            return None
        
        # 原子操作：先生成临时 ICO
        temp_ico_path = app_icon_ico + '.tmp'
        
        success = save_ico_with_transparency(img, temp_ico_path)
        
        if success:
            # 验证通过，覆盖正式 ICO
            try:
                os.replace(temp_ico_path, app_icon_ico)
                logger.info(f"[ICON] 原子覆盖成功: {app_icon_ico}")
                logger.info(f"[ICON] regenerated=True")
                return app_icon_ico
            except Exception as e:
                logger.exception(f"[ICON] 原子覆盖失败: {e}")
                # 清理临时文件
                try:
                    os.remove(temp_ico_path)
                except:
                    pass
                return None
        else:
            # 验证失败，清理临时文件，保留原 ICO
            logger.error(f"[ICON] ICO 验证失败，保留原 ICO")
            try:
                os.remove(temp_ico_path)
            except:
                pass
            return None
    
    return app_icon_ico


def create_temp_ico_for_window(
    window_icon_png: str,
    force_background_removal: bool = False
) -> Optional[str]:
    """
    为窗口图标创建临时 ICO 文件
    
    Args:
        window_icon_png: Window Icon PNG 文件路径
        force_background_removal: 是否强制重新处理背景
    
    Returns:
        临时 ICO 文件路径，失败返回 None
    
    注意：
        - 如果源 PNG 已有有效 Alpha，默认保留原始透明，不进行 flood fill
        - 只有 force_background_removal=True 时才会强制重新处理背景
    """
    logger.info(f"[ICON] 开始创建窗口临时 ICO")
    logger.info(f"[ICON] window_icon_png={window_icon_png}")
    logger.info(f"[ICON] force_background_removal={force_background_removal}")
    
    if not os.path.exists(window_icon_png):
        logger.warning(f"[ICON] Window Icon PNG 不存在")
        return None
    
    # 获取配置
    config = get_icon_config(window_icon_png)
    
    # 计算种子点（从配置的 extra_seed_ratios）
    extra_seeds = None
    if config['extra_seed_ratios']:
        info = inspect_icon_image(window_icon_png)
        if info['size']:
            width, height = info['size']
            extra_seeds = [
                (int(width * ratio[0]), int(height * ratio[1]))
                for ratio in config['extra_seed_ratios']
            ]
    
    # 加载并处理透明背景
    img = load_icon_with_transparency(
        window_icon_png,
        bg_color_hint=config['background_hint'],
        tolerance=config['tolerance'],
        extra_seeds=extra_seeds,
        force_background_removal=force_background_removal
    )
    
    if img is None:
        logger.error(f"[ICON] Window Icon 加载失败")
        return None
    
    # 创建临时文件（先关闭句柄再写入）
    fd, temp_ico_path = tempfile.mkstemp(suffix='.ico')
    os.close(fd)
    
    logger.info(f"[ICON] temp_ico_path={temp_ico_path}")
    
    # 保存 ICO
    success = save_ico_with_transparency(img, temp_ico_path)
    
    if success:
        return temp_ico_path
    else:
        # 清理临时文件
        try:
            os.remove(temp_ico_path)
        except:
            pass
        return None