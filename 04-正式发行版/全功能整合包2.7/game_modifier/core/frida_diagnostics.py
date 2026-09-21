import ctypes
import os
import platform
import sys
from dataclasses import dataclass
from pathlib import Path

import psutil


# Frida 连接诊断日志：
# 这个开关只控制“连接失败时输出到程序日志区域的诊断摘要”。
# 如果后期想临时关闭这部分日志，把 True 改成 False 即可。
ENABLE_FRIDA_CONNECT_DIAGNOSTICS = True


def _trim_one_line(value, limit=160):
    text = str(value or "").replace("\r", " ").replace("\n", " ").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def is_process_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def windows_version_label():
    try:
        release = platform.release() or "Windows"
        version = platform.version() or ""
        build = version.split(".")[-1] if version else ""
        if build:
            return f"Windows {release} build {build}"
        return f"Windows {release}"
    except Exception:
        return "Windows 版本未知"


def _has_non_ascii(text):
    try:
        text.encode("ascii")
        return False
    except UnicodeEncodeError:
        return True


def _is_protected_location(path_text):
    lower = path_text.lower()
    protected_markers = (
        "\\program files\\",
        "\\program files (x86)\\",
        "\\windows\\",
        "\\system32\\",
    )
    return any(marker in lower for marker in protected_markers)


def _is_sync_location(path_text):
    lower = path_text.lower()
    sync_markers = (
        "\\onedrive\\",
        "\\dropbox\\",
        "\\google drive\\",
        "\\baidunetdisk\\",
        "\\百度网盘\\",
        "\\nutstore\\",
        "\\jianguoyun\\",
    )
    return any(marker in lower for marker in sync_markers)


@dataclass(frozen=True)
class PathDiagnostic:
    drive: str = "未知盘"
    writable: bool = None
    protected_location: bool = False
    sync_location: bool = False
    has_non_ascii: bool = False
    has_spaces: bool = False
    status: str = "unknown"

    @classmethod
    def collect(cls, path_text, check_writable=False):
        if not path_text:
            return cls(status="path_unreadable")
        try:
            path = Path(path_text)
            parent = path if path.is_dir() else path.parent
            drive = path.drive or "未知盘"
            writable = None
            if check_writable:
                writable = os.access(str(parent), os.W_OK)
            return cls(
                drive=drive or "未知盘",
                writable=writable,
                protected_location=_is_protected_location(str(path)),
                sync_location=_is_sync_location(str(path)),
                has_non_ascii=_has_non_ascii(str(path)),
                has_spaces=(" " in str(path)),
                status="ok",
            )
        except Exception:
            return cls(status="path_error")

    def to_summary(self, label):
        if self.status == "path_unreadable":
            return f"{label}：路径不可读"
        if self.status == "path_error":
            return f"{label}：路径检测异常"

        parts = [self._drive_label()]
        if self.protected_location:
            parts.append("保护目录")
        if self.sync_location:
            parts.append("网盘同步目录")
        if self.writable is True:
            parts.append("目录可写")
        elif self.writable is False:
            parts.append("目录不可写")
        if self.has_non_ascii:
            parts.append("含中文")
        if self.has_spaces:
            parts.append("含空格")
        return f"{label}：" + "/".join(parts)

    def _drive_label(self):
        if self.drive and self.drive != "未知盘":
            return f"{self.drive.rstrip(':')}盘"
        return "未知盘"


def inspect_target_process(pid):
    name = "未知进程"
    access = "unknown"
    exe_path = ""
    try:
        proc = psutil.Process(pid)
        name = proc.name() or name
        proc.create_time()
        access = "basic_info_ok"
        try:
            exe_path = proc.exe()
            access = "exe_path_ok"
        except psutil.AccessDenied:
            access = "basic_info_ok_exe_denied"
        except Exception:
            pass
    except psutil.AccessDenied:
        access = "access_denied"
    except psutil.NoSuchProcess:
        access = "process_missing"
    except Exception as exc:
        access = f"inspect_error:{_trim_one_line(exc, 60)}"
    return name, access, exe_path


@dataclass(frozen=True)
class FridaConnectDiagnostic:
    code: str
    pid: int = None
    process_name: str = "未知进程"
    is_admin: bool = False
    windows_version: str = "Windows 版本未知"
    target_access: str = "unknown"
    frozen: bool = False
    exception_type: str = ""
    exception_message: str = ""
    app_path: PathDiagnostic = None
    game_path: PathDiagnostic = None

    @classmethod
    def collect(cls, code, pid, exception=None):
        process_name, target_access, game_exe_path = inspect_target_process(pid)
        return cls(
            code=code,
            pid=pid,
            process_name=process_name,
            is_admin=is_process_admin(),
            windows_version=windows_version_label(),
            target_access=target_access,
            frozen=bool(getattr(sys, "frozen", False)),
            exception_type=type(exception).__name__ if exception else "",
            exception_message=_trim_one_line(exception),
            app_path=PathDiagnostic.collect(sys.executable, check_writable=True),
            game_path=PathDiagnostic.collect(game_exe_path, check_writable=False),
        )

    def to_ui_lines(self):
        title = self._title_line()
        permission = "管理员" if self.is_admin else "非管理员"
        pid_text = self.pid if self.pid is not None else "未知"
        detail = (
            f"诊断：修改器权限：{permission}；"
            f"游戏进程：{self.process_name} PID={pid_text}；"
            f"进程访问：{self._target_access_label()}；"
            f"系统：{self.windows_version}"
        )
        path_detail = (
            f"路径：{self._app_path().to_summary('修改器路径')}；"
            f"{self._game_path().to_summary('游戏路径')}"
        )
        suggestion = f"建议：{self._suggestion_text()}"
        if self.exception_type or self.exception_message:
            raw = f"Frida原始错误：{self.exception_type}"
            if self.exception_message:
                raw = f"{raw}: {self.exception_message}" if self.exception_type else self.exception_message
            suggestion = f"{suggestion}；{raw}"
        return [title, detail, path_detail, suggestion]

    def _title_line(self):
        titles = {
            "permission_denied": "Frida 连接失败：权限被拒绝",
            "process_not_found": "Frida 连接失败：游戏进程不存在",
            "architecture_mismatch": "Frida 连接失败：架构不匹配",
            "connection_failed": "Frida 连接失败：底层连接异常",
            "already_connecting": "Frida 连接失败：已有连接正在进行",
        }
        return titles.get(self.code, f"Frida 连接失败：{self.code}")

    def _suggestion_text(self):
        if self.code == "permission_denied":
            if not self.is_admin:
                return "右键修改器以管理员身份运行，并确认 UAC 提权窗口点了“是”"
            return "权限已足够但仍被拒绝，疑似安全软件、进程保护或系统策略拦截"
        if self.code == "architecture_mismatch":
            return "确认修改器和游戏同为 32 位环境，并使用对应 Frida 运行时"
        if self.code == "process_not_found":
            return "重新启动游戏后再连接"
        if self.code == "already_connecting":
            return "等待当前连接完成，不要连续点击连接"
        return "复制这三行日志反馈；优先检查安全软件拦截、系统策略和游戏是否正在退出"

    def _target_access_label(self):
        labels = {
            "basic_info_ok": "可读取基础信息",
            "exe_path_ok": "可读取完整路径",
            "basic_info_ok_exe_denied": "基础信息可读，路径被拒绝",
            "access_denied": "进程信息读取被拒绝",
            "process_missing": "进程已不存在",
            "unknown": "未知",
        }
        return labels.get(self.target_access, self.target_access)

    def _app_path(self):
        return self.app_path or PathDiagnostic(status="path_unreadable")

    def _game_path(self):
        return self.game_path or PathDiagnostic(status="path_unreadable")


class DiagnosticDeduper:
    def __init__(self):
        self._emitted = set()

    def should_emit(self, diagnostic):
        key = (diagnostic.pid, diagnostic.code)
        if key in self._emitted:
            return False
        self._emitted.add(key)
        return True

    def reset(self):
        self._emitted.clear()
