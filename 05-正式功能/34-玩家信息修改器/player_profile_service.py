from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import shutil
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
    backup_path: Path
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

    content = _normalize_newlines(file_path.read_text(encoding="utf-8"))
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

    return PlayerProfile(
        nickname=values["NickName"],
        level=int(values["Level"]),
        vip_level=int(values["VipLevel"]),
    )


def save_profile(path: Path, profile: PlayerProfile, create_backup: bool = True) -> SaveResult:
    file_path = Path(path)
    created_file = not file_path.exists()

    if created_file:
        original = ""
        file_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        original = file_path.read_text(encoding="utf-8")

    backup_path = file_path.with_suffix(file_path.suffix + ".bak")
    if create_backup and not created_file:
        backup_path = _next_backup_path(backup_path)
        shutil.copy2(file_path, backup_path)

    updated = update_player_section_text(original, profile)
    file_path.write_text(updated, encoding="utf-8", newline="\n")

    return SaveResult(path=file_path, backup_path=backup_path, created_file=created_file)


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


def _next_backup_path(base_backup_path: Path) -> Path:
    if not base_backup_path.exists():
        return base_backup_path

    index = 1
    while True:
        candidate = base_backup_path.with_name(f"{base_backup_path.name}.{index}")
        if not candidate.exists():
            return candidate
        index += 1
