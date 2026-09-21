from dataclasses import dataclass


USER_AUDIENCES = {"user", "both"}
DEV_AUDIENCES = {"dev", "both"}


@dataclass(frozen=True)
class LogRoute:
    level: str
    module: str
    user_message: str
    dev_message: str
    show_in_ui: bool
    write_to_dev_log: bool


def normalize_audience(audience):
    if audience in ("user", "dev", "both"):
        return audience
    return "user"


def build_log_route(level, module, message, audience="user", dev_detail=""):
    audience = normalize_audience(audience)
    level = level or "info"
    module = module or ""
    message = message or ""
    dev_detail = dev_detail or ""

    dev_message = message
    if dev_detail:
        dev_message = f"{message} | {dev_detail}" if message else dev_detail

    return LogRoute(
        level=level,
        module=module,
        user_message=message,
        dev_message=dev_message if audience in DEV_AUDIENCES else "",
        show_in_ui=audience in USER_AUDIENCES,
        write_to_dev_log=audience in DEV_AUDIENCES,
    )
