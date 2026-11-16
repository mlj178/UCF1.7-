"""导航编辑器主窗口：看地形（带贴图）、看路点、自由飞行、点选检视。"""
import glob
import os
import sys

import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets

from . import assets, navdata
from .viewport import Viewport

APP_NAME = "UCF 导航编辑器"
ORG = "ucf-modifier"
VERSION = "v0.2"


def configure_surface_format():
    """必须在创建任何 QOpenGLWidget 之前调用：要 24 位深度缓冲，否则深度测试会全裁掉。"""
    fmt = QtGui.QSurfaceFormat()
    fmt.setVersion(3, 3)
    fmt.setProfile(QtGui.QSurfaceFormat.CoreProfile)
    fmt.setDepthBufferSize(24)
    fmt.setStencilBufferSize(8)
    fmt.setSamples(4)
    fmt.setSwapInterval(1)
    QtGui.QSurfaceFormat.setDefaultFormat(fmt)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        configure_surface_format()
        super().__init__()
        self.setWindowTitle(APP_NAME + " " + VERSION)
        self.resize(1600, 950)
        self.settings = QtCore.QSettings(ORG, "navedit")
        self.data_dir = self.settings.value("data_dir", "", type=str)
        self.db = None
        self.geo = None
        self.nav = None
        self.current_scene = ""
        self.last_support = None

        self.view = Viewport(self)
        self.setCentralWidget(self.view)
        self.view.picked.connect(self._on_picked)

        self._build_map_dock()
        self._build_inspector()
        self._build_menus()
        self.statusBar().showMessage("就绪")
        QtCore.QTimer.singleShot(50, self._startup)

    # ---- UI ---------------------------------------------------------
    def _build_map_dock(self):
        dock = QtWidgets.QDockWidget("地图", self)
        dock.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable)
        w = QtWidgets.QWidget()
        lay = QtWidgets.QVBoxLayout(w)
        lay.setContentsMargins(8, 8, 8, 8)

        self.dir_label = QtWidgets.QLabel("游戏目录未设置")
        self.dir_label.setWordWrap(True)
        self.dir_label.setStyleSheet("color:#9fb3c8;font-size:11px")
        lay.addWidget(self.dir_label)

        self.map_list = QtWidgets.QListWidget()
        self.map_list.itemDoubleClicked.connect(lambda _it: self._open_selected())
        lay.addWidget(self.map_list, 1)

        self.btn_open = QtWidgets.QPushButton("打开选中地图")
        self.btn_open.clicked.connect(lambda: self._open_selected())
        lay.addWidget(self.btn_open)

        self.btn_dir = QtWidgets.QPushButton("选择游戏目录…")
        self.btn_dir.clicked.connect(self._pick_dir)
        lay.addWidget(self.btn_dir)

        self.info = QtWidgets.QLabel("")
        self.info.setWordWrap(True)
        self.info.setStyleSheet("color:#8fb99f;font-size:11px")
        lay.addWidget(self.info)

        dock.setWidget(w)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
        self.map_dock = dock

    def _build_inspector(self):
        dock = QtWidgets.QDockWidget("检视（左键点模型）", self)
        w = QtWidgets.QWidget()
        lay = QtWidgets.QVBoxLayout(w)
        lay.setContentsMargins(8, 8, 8, 8)

        self.thumb = QtWidgets.QLabel("贴图")
        self.thumb.setAlignment(QtCore.Qt.AlignCenter)
        self.thumb.setMinimumSize(180, 180)
        self.thumb.setStyleSheet("background:#15181e;color:#556;border:1px solid #2a2f38")
        lay.addWidget(self.thumb)

        self.insp = QtWidgets.QTextBrowser()
        self.insp.setOpenExternalLinks(False)
        self.insp.setStyleSheet("background:#15181e;color:#cfe3f2;font-size:12px;border:1px solid #2a2f38")
        self.insp.setHtml("<span style='color:#667'>在世界里左键点一下模型看看</span>")
        lay.addWidget(self.insp, 1)

        self.btn_selonly = QtWidgets.QPushButton("只看选中这块（再点一次取消）")
        self.btn_selonly.clicked.connect(self._toggle_isolate)
        lay.addWidget(self.btn_selonly)
        self.isolate = False

        dock.setWidget(w)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
        self.insp_dock = dock

    def _build_menus(self):
        m = self.menuBar().addMenu("文件")
        a = m.addAction("选择游戏目录…"); a.triggered.connect(self._pick_dir)
        a = m.addAction("打开路点文件…"); a.triggered.connect(self._pick_nav)
        a = m.addAction("重新提取几何"); a.triggered.connect(lambda: self._open_selected(force=True))
        a = m.addAction("回到路点视角"); a.triggered.connect(lambda: self.view.enter_first_person())
        m.addSeparator()
        a = m.addAction("退出"); a.triggered.connect(self.close)

        m2 = self.menuBar().addMenu("视图")
        for label, attr in (("显示地形", "show_mesh"), ("显示贴图", "show_tex"),
                            ("显示阴影体", "show_shadow"), ("显示装饰板", "show_cards"),
                            ("显示路点", "show_nodes"),
                            ("显示连线", "show_edges"), ("显示标记", "show_features"),
                            ("显示网格", "show_grid"), ("天空背景", "sky")):
            act = m2.addAction(label)
            act.setCheckable(True)
            act.setChecked(bool(getattr(self.view, attr)))
            act.toggled.connect(lambda v, a=attr: self._toggle(a, v))
        m2.addSeparator()
        a = m2.addAction("聚焦到路点 (F)"); a.triggered.connect(self.view.focus_nav)
        a = m2.addAction("俯视角 (Tab)"); a.triggered.connect(self._top_view)

        m3 = self.menuBar().addMenu("帮助")
        a = m3.addAction("操作说明"); a.triggered.connect(self._help)

    def _toggle(self, attr, val):
        setattr(self.view, attr, val)
        self.view.update()

    def _top_view(self):
        self.view.camera.pitch = -1.45
        self.view.camera.pos = self.view.camera.pos + np.array([0.0, 40.0, 0.0])
        self.view.update()

    def _toggle_isolate(self):
        self.isolate = not self.isolate
        if not self.isolate:
            self.view.isolate_chunk = -1
            return
        self.view.isolate_chunk = self.view.selected_chunk
        self.view.update()

    def _help(self):
        QtWidgets.QMessageBox.information(self, "操作说明", "\n".join([
            "右键拖动：转动视角",
            "W/A/S/D：前后左右   Q/E：下降/上升",
            "Shift：加速 4 倍     滚轮：向前/向后推拉",
            "中键拖动：平移",
            "左键点一下：选中模型，右侧显示名字/材质/贴图",
            "F：聚焦到路点整体    Tab：切到俯视角",
            "M：地形    T：贴图    G：路点    R：连线",
        ]))

    def _startup(self):
        if self.data_dir and os.path.isdir(self.data_dir):
            self._load_maps()
        else:
            found = assets.find_data_dir()
            if found:
                self.data_dir = found
                self._load_maps()
            else:
                self.statusBar().showMessage("请先选择游戏目录（含 UnityCrossFire_Data）")

    def _pick_dir(self):
        d = QtWidgets.QFileDialog.getExistingDirectory(self, "选择 UnityCrossFire_Data 目录", self.data_dir or "")
        if not d:
            return
        if os.path.basename(d.rstrip("\\/")) != "UnityCrossFire_Data":
            alt = os.path.join(d, "UnityCrossFire_Data")
            if os.path.isdir(alt):
                d = alt
        self.data_dir = d
        self.settings.setValue("data_dir", d)
        self._load_maps()

    def _load_maps(self):
        self.settings.setValue("data_dir", self.data_dir)
        self.dir_label.setText(self.data_dir)
        self.map_list.clear()
        names = []
        try:
            for fn in sorted(os.listdir(self.data_dir)):
                low = fn.lower()
                if low.startswith("level") and "." not in low:
                    names.append(fn)
        except Exception as exc:
            self.statusBar().showMessage("读取目录失败：%r" % (exc,))
            return
        names.sort(key=lambda s: (len(s), s))
        for fn in names:
            it = QtWidgets.QListWidgetItem(fn)
            it.setData(QtCore.Qt.UserRole, fn)
            self.map_list.addItem(it)
        self.statusBar().showMessage("找到 %d 个场景文件" % len(names))
        if names:
            self.map_list.setCurrentRow(0)

    def _open_selected(self, force=False):
        it = self.map_list.currentItem()
        if it is None:
            return
        self.open_scene(it.data(QtCore.Qt.UserRole), force=force)

    def open_scene(self, scene, force=False):
        if not self.data_dir:
            return
        self.current_scene = scene
        self.statusBar().showMessage("正在读取 %s …" % scene)
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        try:
            if self.db is None:
                self.db = assets.AssetDB(self.data_dir).open()
            elif self.db.data_dir != self.data_dir:
                self.db = assets.AssetDB(self.data_dir).open()
            geo = self.db.extract(scene, use_cache=not force)
            self.geo = geo
            QtWidgets.QApplication.restoreOverrideCursor()
            self.view.set_geometry(geo)
            self.view.set_grid(geo.bbox)
            self._auto_nav()
            self.view.enter_first_person()
            tex = geo.textured_count
            info = "场景 %s\n三角形 %s\n顶点 %s\n模型块 %d（带贴图 %d）\n提取 %.1f 秒" % (
                scene, format(geo.triangle_count, ","), format(geo.vertex_count, ","),
                len(geo.chunks), tex, getattr(self.db, "last_extract_seconds", 0.0))
            if self.nav is not None:
                info += "\n路点 %d  连线 %d  标记 %d" % (
                    self.nav.node_count, self.nav.edge_count, len(self.nav.features))
            self.info.setText(info)
            self.statusBar().showMessage("已打开 %s" % scene)
        except Exception as exc:
            QtWidgets.QApplication.restoreOverrideCursor()
            self.statusBar().showMessage("打开失败：%r" % (exc,))
            QtWidgets.QMessageBox.warning(self, "打开失败", repr(exc))
        self.view.setFocus()

    def _nav_fits_geo(self, nav):
        """判断一份路点数据是不是这张图的：包围盒必须落在几何范围内。"""
        if self.geo is None or nav is None or nav.node_count == 0:
            return True
        gb = np.asarray(self.geo.bbox, dtype=float)
        nb = nav.bbox().astype(float)
        gspan = gb[1] - gb[0]
        nspan = nb[1] - nb[0]
        if np.any(gspan <= 0):
            return True
        center = (nb[0] + nb[1]) * 0.5
        margin = gspan * 0.15
        inside = np.all((center >= gb[0] - margin) & (center <= gb[1] + margin))
        scale_ok = np.all(nspan <= gspan * 1.6 + 5.0)
        if not (inside and scale_ok):
            return False
        ratio, miss, total = assets.support_ratio(self.geo, nav.nodes)
        self.last_support = (ratio, miss, total)
        return ratio >= 0.45

    def _auto_nav(self):
        root = os.path.dirname(os.path.abspath(self.data_dir))
        cands = []
        for pattern in ("ucf_mod/nav/*.json", "ucf_mod/vis/*.json"):
            cands.extend(glob.glob(os.path.join(root, pattern.replace("/", os.sep))))
        if not cands:
            return
        cands.sort(key=os.path.getmtime, reverse=True)
        for path in cands:
            try:
                nav = navdata.load(path)
            except Exception:
                continue
            if self._nav_fits_geo(nav):
                self.nav = nav
                self.view.set_nav(nav)
                self.statusBar().showMessage("路点：%s（%d 点 / %d 边）" % (
                    os.path.basename(path), nav.node_count, nav.edge_count))
                return
        self.nav = None
        self.view.set_nav(navdata.NavData())
        self.statusBar().showMessage("这张图没有匹配的路点数据（vis/ 里没有对得上包围盒的文件）")

    def _load_nav(self, path):
        try:
            nav = navdata.load(path)
        except Exception as exc:
            self.statusBar().showMessage("路点加载失败：%r" % (exc,))
            return
        self.nav = nav
        self.view.set_nav(nav)
        self.statusBar().showMessage("路点：%s（%d 点 / %d 边）" % (
            os.path.basename(path), nav.node_count, nav.edge_count))

    def _pick_nav(self):
        start = self.data_dir or ""
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "打开路点 JSON", start, "JSON (*.json)")
        if path:
            self._load_nav(path)
            self.view.focus_nav()

    # ---- 检视 -------------------------------------------------------
    def _on_picked(self, hit):
        if not hit or self.geo is None:
            self.insp.setHtml("<span style='color:#667'>这里没有模型</span>")
            self.thumb.setPixmap(QtGui.QPixmap())
            self.thumb.setText("贴图")
            return
        geo = self.geo
        ci = hit["chunk"]
        if ci < 0 or ci >= len(geo.chunks):
            return
        c = geo.chunks[ci]
        mat = geo.mats[c["mat"]] if c["mat"] < len(geo.mats) else None
        rows = [
            ("对象", c.get("name", "")),
            ("网格", c.get("mesh", "")),
            ("材质", mat.name if mat else ""),
            ("着色器", mat.shader if mat else ""),
        ]
        if mat is not None and mat.tex:
            rows.append(("贴图", "%s（%dx%d %s）" % (mat.tex, mat.tex_w, mat.tex_h, mat.tex_fmt)))
        elif mat is not None:
            rows.append(("贴图", "无（纯色）"))
        rows.append(("三角形", format(int(c["count"]), ",")))
        p = hit.get("point") or (0, 0, 0)
        rows.append(("点击位置", "%.2f, %.2f, %.2f" % (p[0], p[1], p[2])))
        rows.append(("距离", "%.1f m" % float(hit.get("dist", 0.0))))
        if self.nav is not None and len(self.nav.nodes):
            d = np.linalg.norm(self.nav.nodes - np.asarray(p, dtype=np.float32), axis=1)
            k = int(np.argmin(d))
            rows.append(("最近路点", "#%d  相距 %.1f m" % (k, float(d[k]))))
        html = ["<table cellspacing='0' cellpadding='3'>"]
        for k, v in rows:
            html.append("<tr><td style='color:#7f93a8'>%s</td><td style='color:#e8f2fb'>%s</td></tr>" % (
                k, str(v).replace("<", "&lt;")))
        html.append("</table>")
        self.insp.setHtml("".join(html))
        path = geo.tex_path(c) if mat is not None else ""
        if path and os.path.isfile(path):
            pm = QtGui.QPixmap(path)
            if not pm.isNull():
                self.thumb.setPixmap(pm.scaled(180, 180, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            else:
                self.thumb.setText("贴图读取失败")
        else:
            self.thumb.setPixmap(QtGui.QPixmap())
            self.thumb.setText("无贴图")
        self.statusBar().showMessage("选中 %s（%s）" % (c.get("name", ""), mat.name if mat else ""))


def run():
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    configure_surface_format()
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    win = MainWindow()
    win.show()
    return app.exec_()