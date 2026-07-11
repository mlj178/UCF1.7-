import re


APP_VERSION = "v2.0"
APP_DISPLAY_NAME = f"全功能整合包 {APP_VERSION}"
APP_TITLE = APP_DISPLAY_NAME
STARTUP_LOG_TITLE = APP_DISPLAY_NAME

MAIN_WINDOW_GEOMETRY = "610x700+10+10"
MAIN_WINDOW_MIN_SIZE = (610, 400)
COLLAPSED_WINDOW_SIZE = (400, 62)


def collapsed_geometry_for(current_geometry):
    match = re.match(r"^\d+x\d+([+-]\d+[+-]\d+)$", current_geometry)
    width, height = COLLAPSED_WINDOW_SIZE
    if not match:
        return f"{width}x{height}"
    return f"{width}x{height}{match.group(1)}"
