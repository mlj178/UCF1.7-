"""按控件真实宽度折行，避免说明文字被卡片边框裁掉半个字。

背景（125% DPI 的机器上必现）：
    CustomTkinter 会把 CTkLabel 的 wraplength 乘上窗口缩放系数
    （ScalingTracker.get_widget_scaling，125% 缩放下为 1.25），
    而控件的真实宽度来自 Tk 的原始像素布局，不乘这个系数。
    于是 wraplength=280 实际生效为 350px，比标签真实宽度（约 304px）更宽：
    Tk 只在 wraplength 处折行，超出标签宽度的部分不会重新折行，
    直接被标签右边界裁掉，表现为"字显示一半"。

做法：
    给标签绑定 <Configure>，回写 fit_wrap_value(...)：
    即 min(作者写的 wraplength, 真实宽度 / 缩放)。
    因此作者故意写窄的值（例如 190）保持原样，只有真的放不下时才收窄。
    只有当换算结果与当前值相差超过 1px 才回写，避免与布局来回抖动。
"""

import customtkinter as ctk

#: 收窄下限，防止极端布局（例如窗口被压到很窄）把文字挤成一条竖线。
MIN_WRAP = 60


def fit_wrap_value(base_wrap, width_px, scaling, gap=2, minimum=MIN_WRAP):
    """算出 CTkLabel 应该使用的 wraplength（CTk 单位）。

    base_wrap: 作者写在代码里的值（会被 CustomTkinter 乘上 scaling）
    width_px:  控件当前的物理像素宽度（真正的裁剪边界）
    scaling:   ScalingTracker.get_widget_scaling()，例如 1.25

    以作者写的值为上限：放得下就用作者的值，放不下就收到刚好放得下。
    因为每次都从原始值重算，窗口变宽后能自动恢复，不会留下多余的换行。
    """
    if width_px <= 1 or not scaling:
        return base_wrap
    limit = max(minimum, int((width_px - gap) / scaling))
    return min(int(base_wrap), limit)


def _available_wrap(label, gap):
    """把标签当前真实可用宽度换算回 CTk 的 wraplength 单位。"""
    width = label.winfo_width()
    if width <= 1:  # 还没完成布局
        return None
    scaling = ctk.ScalingTracker.get_widget_scaling(label) or 1.0
    return fit_wrap_value(label._wrap_base, width, scaling, gap)


def bind_text_wrap(label, gap=2):
    """让 label 的文字始终按真实宽度折行。

    以"第一次绑定时作者写的值"为上限，之后随窗口宽度双向调整：
    窗口变窄就收窄（不裁字），窗口变宽就恢复（不留下多余的换行）。
    """
    if getattr(label, "_wrap_base", None):
        return  # 已经绑过：重复绑定会把收窄后的值当成本意，越收越窄
    try:
        base_wrap = int(label.cget("wraplength") or 0)
    except Exception:
        return
    if base_wrap <= 0:
        return
    label._wrap_base = base_wrap

    def _apply(_event=None):
        target = _available_wrap(label, gap)
        if target is None:
            return
        try:
            current = int(label.cget("wraplength"))
        except Exception:
            return
        if abs(current - target) <= 1:
            return
        label.configure(wraplength=target)

    label.bind("<Configure>", _apply, add="+")
    _apply()


def bind_text_wrap_tree(widget, gap=2):
    """递归给 widget 及其子控件里所有需要折行的 CTkLabel 套用上面的逻辑。"""
    if isinstance(widget, ctk.CTkLabel):
        try:
            if int(widget.cget("wraplength") or 0) > 0:
                bind_text_wrap(widget, gap)
        except Exception:
            pass
    for child in widget.winfo_children():
        bind_text_wrap_tree(child, gap)
