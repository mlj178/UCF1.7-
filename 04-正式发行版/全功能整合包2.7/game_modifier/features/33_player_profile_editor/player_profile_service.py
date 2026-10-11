from __future__ import annotations

import codecs
from dataclasses import dataclass
import shutil
from pathlib import Path
import re
from typing import Optional


COMPANY_NAME = "Alexander_GaGa"
PRODUCT_NAME = "UnityCrossFire"
PLAYER_DATA_FILENAME = "PlayerData.dat"


@dataclass(frozen=True)
class PlayerProfile:
    nickname: str
    level: int
    vip_level: int


@dataclass(frozen=True)
class SaveResult:
    path: Path
    created_file: bool


def get_default_player_data_path(home_dir: Optional[Path] = None) -> Path:
    home = Path(home_dir) if home_dir is not None else Path.home()
    return home / "AppData" / "LocalLow" / COMPANY_NAME / PRODUCT_NAME / PLAYER_DATA_FILENAME


def validate_profile(profile: PlayerProfile) -> PlayerProfile:
    nickname = str(profile.nickname).strip()
    if not nickname:
        raise ValueError("昵称不能为空")
    if "\n" in nickname or "\r" in nickname:
        raise ValueError("昵称不能包含换行")

    level = int(profile.level)
    vip_level = int(profile.vip_level)
    if level < 0:
        raise ValueError("等级不能小于 0")
    if vip_level < 0:
        raise ValueError("VIP等级不能小于 0")

    return PlayerProfile(nickname=nickname, level=level, vip_level=vip_level)


def build_player_section(profile: PlayerProfile) -> str:
    safe_profile = validate_profile(profile)
    return (
        "[Player]\n"
        f"NickName={safe_profile.nickname}\n"
        f"Level={safe_profile.level}\n"
        f"VipLevel={safe_profile.vip_level}\n"
    )


def update_player_section_text(content: str, profile: PlayerProfile) -> str:
    normalized = _normalize_newlines(content)
    player_section = build_player_section(profile)

    player_match = _find_section(normalized, "Player")
    if player_match:
        prefix = normalized[: player_match.start]
        suffix = normalized[player_match.end :]
        return _join_sections(prefix, player_section, suffix)

    inven_match = _find_section(normalized, "Inven")
    if inven_match:
        prefix = normalized[: inven_match.start]
        suffix = normalized[inven_match.start :]
        return _join_sections(prefix, player_section, suffix)

    return _join_sections(normalized, player_section, "")


def load_profile(path: Path) -> Optional[PlayerProfile]:
    file_path = Path(path)
    if not file_path.exists():
        return None

    # P1：兼容 BOM 与 GBK（旧版本游戏文件），并避免解码异常打断界面
    try:
        raw = file_path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        raw = file_path.read_text(encoding="gbk", errors="replace")
    content = _normalize_newlines(raw)
    player_match = _find_section(content, "Player")
    if not player_match:
        return None

    section_text = content[player_match.start : player_match.end]
    values = {}
    for line in section_text.splitlines():
        if "=" not in line or line.startswith("["):
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()

    if not {"NickName", "Level", "VipLevel"}.issubset(values):
        return None

    try:
        level = int(values["Level"])
        vip_level = int(values["VipLevel"])
    except (TypeError, ValueError):
        return None

    return PlayerProfile(
        nickname=values["NickName"],
        level=level,
        vip_level=vip_level,
    )


def _next_backup_path(file_path: Path) -> Path:
    candidate = file_path.with_name(file_path.name + ".bak")
    if not candidate.exists():
        return candidate
    index = 1
    while True:
        candidate = file_path.with_name(file_path.name + f".bak.{index}")
        if not candidate.exists():
            return candidate
        index += 1


def save_profile(path: Path, profile: PlayerProfile) -> SaveResult:
    file_path = Path(path)
    created_file = not file_path.exists()

    if created_file:
        original = ""
        has_bom = False
        file_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        raw_bytes = file_path.read_bytes()
        # P2：原实现按 utf-8 读取，UTF-8 BOM 会作为正文保留，_find_section 匹配不到
        # 行首的 [Player]，保存时会追加出重复的 [Player] 段落。改为按 utf-8-sig
        # 解码，并在写回时按原文件是否带 BOM 还原编码（不带 BOM 的文件行为不变）。
        # 非 UTF-8（如 GBK）仍会抛 UnicodeDecodeError，由调用方按原样处理。
        has_bom = raw_bytes.startswith(codecs.BOM_UTF8)
        original = raw_bytes.decode("utf-8-sig")
        # P1：保存前递增备份（独立版有，集成版丢了），避免一次误保存不可恢复
        try:
            shutil.copy2(file_path, _next_backup_path(file_path))
        except OSError:
            pass

    updated = update_player_section_text(original, profile)
    file_path.write_text(updated, encoding="utf-8-sig" if has_bom else "utf-8", newline="\n")

    return SaveResult(path=file_path, created_file=created_file)


@dataclass(frozen=True)
class SectionSpan:
    start: int
    end: int


def _normalize_newlines(content: str) -> str:
    return content.replace("\r\n", "\n").replace("\r", "\n")


def _find_section(content: str, section_name: str) -> Optional[SectionSpan]:
    header_pattern = re.compile(rf"(?im)^\[{re.escape(section_name)}\]\s*$")
    header_match = header_pattern.search(content)
    if not header_match:
        return None

    next_header = re.compile(r"(?m)^\[[^\]\r\n]+\]\s*$").search(content, header_match.end())
    end = next_header.start() if next_header else len(content)
    return SectionSpan(start=header_match.start(), end=end)


def _join_sections(prefix: str, player_section: str, suffix: str) -> str:
    parts = []

    clean_prefix = prefix.rstrip("\n")
    if clean_prefix:
        parts.append(clean_prefix)

    parts.append(player_section.rstrip("\n"))

    clean_suffix = suffix.lstrip("\n")
    if clean_suffix:
        parts.append(clean_suffix.rstrip("\n"))

    return "\n\n".join(parts) + "\n"
