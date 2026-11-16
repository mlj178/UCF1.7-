"""3D 视口：自由飞行相机 + 带贴图的地图几何 + 路点叠加 + 点选检视。

渲染用独立 moderngl 上下文画到自己的 FBO，再读回成 QImage 显示。
这样绕开了 QOpenGLWidget 与 moderngl 之间的 FBO / current 上下文纠纷，
稳定、可截帧、也不挑驱动。
"""
import math
import time

import moderngl
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

MESH_VS = """
#version 330
in vec3 in_pos;
in vec3 in_nrm;
in vec2 in_uv;
in vec3 in_col;
uniform mat4 mvp;
uniform vec3 cam;
out vec3 v_nrm;
out vec2 v_uv;
out vec3 v_col;
out vec3 v_wpos;
out float v_dist;
void main() {
    v_nrm = in_nrm;
    v_uv = in_uv;
    v_col = in_col;
    v_wpos = in_pos;
    v_dist = length(in_pos - cam);
    gl_Position = mvp * vec4(in_pos, 1.0);
}
"""

MESH_FS = """
#version 330
in vec3 v_nrm;
in vec2 v_uv;
in vec3 v_col;
in vec3 v_wpos;
in float v_dist;
uniform sampler2D albedo;
uniform bool use_tex;
uniform vec3 tint;
uniform float alpha;
uniform float alpha_cut;
uniform vec3 bg;
uniform float fog_start;
uniform float fog_end;
uniform float unlit;
// 游戏里真实的光照：Unity RenderSettings 的三色环境光 + 场景里的灯
uniform vec3 amb_sky;
uniform vec3 amb_equator;
uniform vec3 amb_ground;
uniform vec3 sun_dir;
uniform vec3 sun_color;
uniform int n_points;
uniform vec4 point_pos[8];
uniform vec3 point_color[8];
out vec4 f_col;

vec3 ambient_trilight(vec3 n) {
    float up = n.y * 0.5 + 0.5;
    vec3 c = mix(amb_ground, amb_equator, clamp(up * 2.0, 0.0, 1.0));
    return mix(c, amb_sky, clamp(up * 2.0 - 1.0, 0.0, 1.0));
}

void main() {
    vec4 src = vec4(1.0);
    vec3 base = v_col;
    float a = alpha;
    if (use_tex) {
        src = texture(albedo, v_uv) * vec4(tint, 1.0);
        base = src.rgb;
        a = alpha * src.a;
        if (alpha_cut > 0.001 && src.a < alpha_cut) discard;
    }
    if (unlit > 0.5) {
        f_col = vec4(base, a);
        return;
    }
    vec3 n = normalize(v_nrm);
    vec3 lit = ambient_trilight(n);
    lit += sun_color * max(dot(n, -sun_dir), 0.0);
    for (int i = 0; i < 8; i++) {
        if (i >= n_points) break;
        float r = point_pos[i].w;
        vec3 dv = point_pos[i].xyz - v_wpos;
        float dist = length(dv);
        if (dist < r) {
            float att = 1.0 - dist / r;
            lit += point_color[i] * att * att * max(dot(n, normalize(dv)), 0.0);
        }
    }
    vec3 c = base * lit;
    float fog = clamp((v_dist - fog_start) / max(fog_end - fog_start, 1.0), 0.0, 1.0);
    f_col = vec4(mix(c, bg, fog), a);
}
"""

FLAT_VS = """
#version 330
in vec3 in_pos;
in float in_size;
uniform mat4 mvp;
uniform float point_size;
void main() {
    gl_Position = mvp * vec4(in_pos, 1.0);
    gl_PointSize = point_size * in_size;
}
"""

FLAT_FS = """
#version 330
uniform vec4 color;
uniform bool round_point;
out vec4 f_col;
void main() {
    if (round_point) {
        vec2 d = gl_PointCoord - vec2(0.5);
        if (dot(d, d) > 0.25) discard;
    }
    f_col = color;
}
"""


class Camera(object):
    def __init__(self):
        self.pos = np.array([0.0, 40.0, 120.0], dtype=np.float64)
        self.yaw = math.pi
        self.pitch = -0.35
        self.fov = 75.0
        self.near = 0.05
        self.far = 5000.0

    def forward(self):
        cp = math.cos(self.pitch)
        return np.array([cp * math.sin(self.yaw), math.sin(self.pitch), -cp * math.cos(self.yaw)])

    def right(self):
        f = self.forward()
        r = np.cross(f, np.array([0.0, 1.0, 0.0]))
        n = np.linalg.norm(r)
        return r / n if n > 1e-9 else np.array([1.0, 0.0, 0.0])

    def up(self):
        return np.cross(self.right(), self.forward())

    def view(self):
        f = self.forward()
        r = self.right()
        u = np.cross(r, f)
        m = np.eye(4)
        m[0, :3] = r
        m[1, :3] = u
        m[2, :3] = -f
        m[0, 3] = -r.dot(self.pos)
        m[1, 3] = -u.dot(self.pos)
        m[2, 3] = f.dot(self.pos)
        return m

    def proj(self, aspect):
        fy = 1.0 / math.tan(math.radians(self.fov) * 0.5)
        m = np.zeros((4, 4))
        m[0, 0] = fy / max(aspect, 1e-6)
        m[1, 1] = fy
        m[2, 2] = (self.far + self.near) / (self.near - self.far)
        m[2, 3] = (2 * self.far * self.near) / (self.near - self.far)
        m[3, 2] = -1.0
        return m

    def mvp(self, aspect):
        return self.proj(aspect) @ self.view()

    def move_at(self, target, dist=120.0):
        target = np.asarray(target, dtype=np.float64)
        self.pos = target - self.forward() * dist

    def look_dir(self, direction):
        d = np.asarray(direction, dtype=np.float64)
        n = np.linalg.norm(d)
        if n < 1e-9:
            return
        d = d / n
        self.yaw = math.atan2(d[0], -d[2])
        self.pitch = math.asin(max(-1.0, min(1.0, d[1])))

    def look_at(self, target, dist=None, yaw=None, pitch=None):
        if yaw is not None:
            self.yaw = yaw
        if pitch is not None:
            self.pitch = pitch
        self.move_at(target, 120.0 if dist is None else dist)


class Viewport(QtWidgets.QWidget):
    stats = QtCore.pyqtSignal(str)
    picked = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setMouseTracking(True)
        self.camera = Camera()
        self.geo = None
        self.env = {}
        self.nav = None
        self.keys = set()
        self.grab_look = False
        self.pan_drag = False
        self.last_mouse = None
        self.press_pos = None
        self.bg = (0.24, 0.34, 0.46)
        self.bg_dark = (0.07, 0.08, 0.10)
        self.sky = True
        self.fog_start = 130.0
        self.fog_end = 620.0
        self.show_mesh = True
        self.show_tex = True
        self.show_shadow = False
        self.show_cull = True
        self.show_cards = False
        self.unlit = False
        self.show_nodes = True
        self.show_edges = True
        self.show_features = True
        self.show_overlay = True
        self.show_grid = True
        self.speed = 20.0
        self.image = None
        self.isolated = 0
        self.feature_counts = {}
        self.init_error = ""
        self.fps = 0.0
        self.tex_loaded = 0
        self.tex_failed = 0
        self._mesh_vao = None
        self._mesh_vbo = None
        self._mesh_ibo = None
        self._textures = {}
        self._node_vao = None
        self._iso_vao = None
        self._edge_vao = None
        self._feat_vaos = []
        self._grid_vao = None
        self._fbo = None
        self._fbo_size = (0, 0)
        self._last_frame = time.time()
        self.selected_chunk = -1
        self.isolate_chunk = -1
        try:
            self.ctx = moderngl.create_standalone_context(require=330)
            self.mesh_prog = self.ctx.program(vertex_shader=MESH_VS, fragment_shader=MESH_FS)
            self.flat_prog = self.ctx.program(vertex_shader=FLAT_VS, fragment_shader=FLAT_FS)
            self.ctx.enable(moderngl.DEPTH_TEST)
            # Unity 的正面是顺时针；经过我们的坐标变换后，在 GL 里表现为逆时针，
            # 所以默认的 CCW 正面刚好对得上，直接开背面剔除。
            self.ctx.enable(moderngl.CULL_FACE)
            self.ctx.front_face = "ccw"
            self.gl_info = self.ctx.info.get("GL_RENDERER", "?")
            self.ready = True
        except Exception as exc:
            self.ctx = None
            self.ready = False
            self.gl_info = ""
            self.init_error = repr(exc)
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(16)

    # ---- FBO --------------------------------------------------------
    def _ensure_fbo(self, w, h):
        if self._fbo is not None and self._fbo_size == (w, h):
            return
        if self._fbo is not None:
            try:
                self._fbo.release()
            except Exception:
                pass
        tex = self.ctx.texture((w, h), 4)
        dep = self.ctx.depth_texture((w, h))
        self._fbo = self.ctx.framebuffer(color_attachments=[tex], depth_attachment=dep)
        self._fbo_size = (w, h)

    # ---- 贴图 -------------------------------------------------------
    def _load_texture(self, chunk):
        key = (chunk.get("tex") or "", chunk.get("vstart", 0))
        if key in self._textures:
            return self._textures[key]
        tex = None
        path = self.geo.tex_path(chunk) if self.geo is not None else ""
        if path and QtCore.QFileInfo(path).exists():
            img = QtGui.QImage(path)
            if not img.isNull():
                if img.format() != QtGui.QImage.Format_RGBA8888:
                    img = img.convertToFormat(QtGui.QImage.Format_RGBA8888)
                img = img.mirrored(False, True)
                w, h = img.width(), img.height()
                try:
                    data = img.constBits().asstring(img.sizeInBytes())
                    tex = self.ctx.texture((w, h), 4, data)
                    tex.build_mipmaps()
                    tex.filter = (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR)
                    try:
                        tex.anisotropy = 4.0
                    except Exception:
                        pass
                    tex.repeat_x = True
                    tex.repeat_y = True
                    self.tex_loaded += 1
                except Exception:
                    tex = None
        if tex is None:
            self.tex_failed += 1
        self._textures[key] = tex
        return tex

    def _drop_textures(self):
        for t in self._textures.values():
            if t is not None:
                try:
                    t.release()
                except Exception:
                    pass
        self._textures = {}
        self.tex_loaded = 0
        self.tex_failed = 0

    # ---- 渲染 -------------------------------------------------------
    def render_frame(self):
        if not self.ready:
            return
        dpr = float(self.devicePixelRatioF())
        w = max(1, int(round(self.width() * dpr)))
        h = max(1, int(round(self.height() * dpr)))
        self._ensure_fbo(w, h)
        self._fbo.use()
        if self.show_cull:
            self.ctx.enable(moderngl.CULL_FACE)
        else:
            self.ctx.disable(moderngl.CULL_FACE)
        self.ctx.viewport = (0, 0, w, h)
        self.ctx.clear(*self.bg, 1.0)
        aspect = w / float(h)
        mvp = np.ascontiguousarray(self.camera.mvp(aspect).T, dtype="f4").tobytes()

        if self.show_mesh and self._mesh_vao is not None:
            p = self.mesh_prog
            p["mvp"].write(mvp)
            p["cam"].value = tuple(float(v) for v in self.camera.pos)
            p["bg"].value = self.bg
            p["fog_start"].value = self.fog_start
            p["fog_end"].value = self.fog_end
            p["unlit"].value = 1.0 if self.unlit else 0.0
            p["albedo"].value = 0
            chunks = self.geo.chunks if self.geo is not None else []
            if self.show_tex and chunks:
                self._draw_chunks(False)
                self.ctx.enable(moderngl.BLEND)
                self.ctx.depth_mask = False
                self._draw_chunks(True)
                self.ctx.depth_mask = True
                self.ctx.disable(moderngl.BLEND)
            else:
                p["use_tex"].value = False
                p["tint"].value = (1.0, 1.0, 1.0)
                p["alpha"].value = 1.0
                p["alpha_cut"].value = 0.0
                self._mesh_vao.render(moderngl.TRIANGLES)

        self.flat_prog["mvp"].write(mvp)
        if self._grid_vao is not None and self.show_grid:
            self.flat_prog["point_size"].value = 1.0
            self.flat_prog["round_point"].value = False
            self.flat_prog["color"].value = (0.19, 0.22, 0.27, 1.0)
            self._grid_vao.render(moderngl.LINES)
        if self.show_edges and self._edge_vao is not None:
            self.flat_prog["color"].value = (0.14, 0.55, 0.32, 1.0)
            self._edge_vao.render(moderngl.LINES)
        if self.show_nodes:
            self.ctx.enable(moderngl.PROGRAM_POINT_SIZE)
            self.flat_prog["round_point"].value = True
            if self._node_vao is not None:
                self.flat_prog["color"].value = (0.22, 0.95, 0.55, 1.0)
                self.flat_prog["point_size"].value = 4.2
                self._node_vao.render(moderngl.POINTS)
            if self._iso_vao is not None:
                self.flat_prog["color"].value = (0.98, 0.25, 0.25, 1.0)
                self.flat_prog["point_size"].value = 6.5
                self._iso_vao.render(moderngl.POINTS)
            self.ctx.disable(moderngl.PROGRAM_POINT_SIZE)
        if self.show_features and self._feat_vaos:
            self.ctx.enable(moderngl.PROGRAM_POINT_SIZE)
            self.flat_prog["round_point"].value = True
            self.flat_prog["point_size"].value = 7.5
            for kind, vao, col in self._feat_vaos:
                self.flat_prog["color"].value = (col[0], col[1], col[2], 1.0)
                vao.render(moderngl.POINTS)
            self.ctx.disable(moderngl.PROGRAM_POINT_SIZE)

        data = self._fbo.read(components=3)
        arr = np.frombuffer(data, dtype=np.uint8).reshape(h, w, 3)[::-1]
        self.image = QtGui.QImage(arr.copy().data, w, h, 3 * w, QtGui.QImage.Format_RGB888).copy()
        now = time.time()
        dt = max(1e-3, now - self._last_frame)
        self._last_frame = now
        self.fps = 0.9 * self.fps + 0.1 / dt

    def _draw_chunks(self, transparent_pass):
        p = self.mesh_prog
        geo = self.geo
        for i, c in enumerate(geo.chunks):
            if self.isolate_chunk >= 0 and i != self.isolate_chunk:
                continue
            if (c.get("shadow") or c.get("blocker")) and not self.show_shadow:
                continue
            if c.get("card") and not self.show_cards:
                continue
            if bool(c.get("transparent")) != transparent_pass:
                continue
            tex = self._load_texture(c) if c.get("tex") else None
            if tex is not None:
                tex.use(0)
                p["use_tex"].value = True
            else:
                p["use_tex"].value = False
            col = c.get("color") or (1.0, 1.0, 1.0, 1.0)
            p["tint"].value = (float(col[0]), float(col[1]), float(col[2]))
            p["alpha"].value = float(c.get("alpha", 1.0))
            p["alpha_cut"].value = float(c.get("alpha_test", 0.0))
            self._mesh_vao.render(moderngl.TRIANGLES, int(c["count"]), int(c["start"]))

    # ---- 事件 -------------------------------------------------------
    def paintEvent(self, ev):
        p = QtGui.QPainter(self)
        if self.image is not None:
            p.drawImage(self.rect(), self.image)
        else:
            p.fillRect(self.rect(), QtGui.QColor(18, 20, 26))
            if not self.ready:
                p.setPen(QtGui.QColor(230, 120, 120))
                p.drawText(20, 30, "OpenGL 初始化失败：" + self.init_error)
        if self.show_overlay:
            self._draw_overlay(p)
        p.end()

    def _draw_overlay(self, p):
        p.setPen(QtGui.QColor(150, 200, 230, 215))
        fnt = p.font()
        fnt.setPointSize(9)
        p.setFont(fnt)
        pos = self.camera.pos
        head = "FPS %4.0f   相机 %.1f, %.1f, %.1f   偏航 %3.0f  俯仰 %3.0f  FOV %2.0f" % (
            self.fps, pos[0], pos[1], pos[2], math.degrees(self.camera.yaw),
            math.degrees(self.camera.pitch), self.camera.fov)
        hint = "右键转视角  WASD 移动  Q/E 升降  Shift 加速  滚轮推拉  左键点选  F 聚焦  T 贴图  M 地形  G 路点"
        p.drawText(12, self.height() - 30, head)
        p.drawText(12, self.height() - 12, hint)
        if self.selected_chunk >= 0 and self.geo is not None and self.selected_chunk < len(self.geo.chunks):
            c = self.geo.chunks[self.selected_chunk]
            mat = self.geo.mats[c["mat"]] if c["mat"] < len(self.geo.mats) else None
            p.setPen(QtGui.QColor(255, 220, 120, 235))
            txt = "已选：%s   %s" % (c.get("name", ""), (mat.name if mat else ""))
            p.drawText(12, 22, txt)
        if not self.show_nodes or not self.show_features:
            return
        from .navdata import KIND_NAMES, KIND_COLORS
        rows = []
        if self.nav is not None and len(self.nav.nodes):
            rows.append(((0.22, 0.95, 0.55), "路点 %d" % (len(self.nav.nodes) - self.isolated)))
            if self.isolated:
                rows.append(((0.98, 0.25, 0.25), "孤立路点 %d" % self.isolated))
        for kind, cnt in sorted(self.feature_counts.items()):
            rows.append((KIND_COLORS.get(kind, (0.8, 0.8, 0.8)), "%s %d" % (KIND_NAMES.get(kind, str(kind)), cnt)))
        y = self.height() - 54
        for col, label in rows:
            p.setPen(QtGui.QColor(int(col[0] * 255), int(col[1] * 255), int(col[2] * 255)))
            p.drawText(14, y, "●")
            p.setPen(QtGui.QColor(150, 200, 230, 215))
            p.drawText(30, y, label)
            y -= 15

    def _tick(self):
        if self.keys:
            dt = 0.016
            boost = 4.0 if QtCore.Qt.Key_Shift in self.keys else 1.0
            v = self.speed * boost * dt
            f = self.camera.forward()
            r = self.camera.right()
            move = np.zeros(3)
            if QtCore.Qt.Key_W in self.keys:
                move += f
            if QtCore.Qt.Key_S in self.keys:
                move -= f
            if QtCore.Qt.Key_A in self.keys:
                move -= r
            if QtCore.Qt.Key_D in self.keys:
                move += r
            if QtCore.Qt.Key_E in self.keys:
                move += np.array([0.0, 1.0, 0.0])
            if QtCore.Qt.Key_Q in self.keys:
                move -= np.array([0.0, 1.0, 0.0])
            if np.any(move):
                self.camera.pos = self.camera.pos + move * v
        self.render_frame()
        self.update()

    # ---- 数据 -------------------------------------------------------
    def set_env(self, env):
        """把场景里读到的真实光照参数灌进 shader。"""
        self.env = env or {}
        if not self.ready:
            return
        p = self.mesh_prog

        def srgb(c):
            return tuple(min(1.0, max(0.0, float(x)) ** (1.0 / 2.2)) for x in c)

        amb = self.env.get("ambient") or {}
        for key, name, dflt in (("sky", "amb_sky", (0.5, 0.5, 0.5)),
                                ("equator", "amb_equator", (0.3, 0.3, 0.3)),
                                ("ground", "amb_ground", (0.15, 0.15, 0.15))):
            try:
                p[name].value = srgb(amb.get(key) or dflt)
            except Exception:
                pass
        sun = self.env.get("sun") or {}
        try:
            p["sun_dir"].value = tuple(sun.get("dir") or (0.3, -0.9, 0.2))
        except Exception:
            pass
        try:
            p["sun_color"].value = srgb(sun.get("color") or (1.0, 1.0, 1.0))
        except Exception:
            pass
        pts = (self.env.get("points") or [])[:8]
        arr = np.zeros((8, 4), dtype="f4")
        cols = np.zeros((8, 3), dtype="f4")
        for i, pt in enumerate(pts):
            arr[i, :3] = pt.get("pos", (0.0, 0.0, 0.0))
            arr[i, 3] = float(pt.get("range", 10.0))
            cols[i] = srgb(pt.get("color", (1.0, 1.0, 1.0)))
        try:
            p["point_pos"].write(arr.tobytes())
            p["point_color"].write(cols.tobytes())
            p["n_points"].value = int(len(pts))
        except Exception:
            pass
        fog = self.env.get("fog") or {}
        if fog.get("on"):
            self.fog_start = max(0.0, float(fog.get("start") or 0.0))
            self.fog_end = max(self.fog_start + 1.0, float(fog.get("end") or 300.0))
        if self.sky:
            sky = srgb(amb.get("sky") or (0.24, 0.34, 0.46))
            self.bg = tuple(min(1.0, float(c) * 0.82) for c in sky)

    def set_geometry(self, geo):
        self.geo = geo
        self.set_env(getattr(geo, "env", None) if geo is not None else None)
        self._drop_textures()
        self.selected_chunk = -1
        self.isolate_chunk = -1
        if not self.ready or geo is None:
            return
        inter = np.hstack([geo.positions, geo.normals, geo.uvs, geo.colors]).astype("f4")
        self._mesh_vbo = self.ctx.buffer(inter.tobytes())
        self._mesh_ibo = self.ctx.buffer(np.ascontiguousarray(geo.indices, dtype="i4").tobytes())
        self._mesh_vao = self.ctx.vertex_array(
            self.mesh_prog,
            [(self._mesh_vbo, "3f 3f 2f 3f", "in_pos", "in_nrm", "in_uv", "in_col")],
            index_buffer=self._mesh_ibo, index_element_size=4)
        self.render_frame()

    def set_nav(self, nav):
        self.nav = nav
        if not self.ready or nav is None:
            return
        self._node_vao = None
        self._iso_vao = None
        self._edge_vao = None
        self._feat_vaos = []
        if len(nav.nodes):
            deg = np.zeros(len(nav.nodes), dtype=np.int32)
            if len(nav.edges):
                np.add.at(deg, nav.edges[:, 0], 1)
                np.add.at(deg, nav.edges[:, 1], 1)
            self.isolated = int((deg == 0).sum())
            for sel, attr in ((deg > 0, "_node_vao"), (deg == 0, "_iso_vao")):
                sub = nav.nodes[sel]
                if len(sub) == 0:
                    continue
                arr = np.hstack([sub, np.ones((len(sub), 1), dtype="f4")]).astype("f4")
                setattr(self, attr, self.ctx.vertex_array(
                    self.flat_prog, [(self.ctx.buffer(arr.tobytes()), "3f 1f", "in_pos", "in_size")]))
        if len(nav.edges) and len(nav.nodes):
            seg = np.zeros((len(nav.edges) * 2, 4), dtype="f4")
            seg[0::2, :3] = nav.nodes[nav.edges[:, 0]]
            seg[1::2, :3] = nav.nodes[nav.edges[:, 1]]
            seg[:, 3] = 1.0
            self._edge_vao = self.ctx.vertex_array(
                self.flat_prog, [(self.ctx.buffer(seg.tobytes()), "3f 1f", "in_pos", "in_size")])
        from .navdata import KIND_COLORS, KIND_NAMES
        by_kind = {}
        for f in nav.features:
            by_kind.setdefault(int(f["kind"]), []).append(f["pos"])
        for kind in sorted(by_kind):
            pts = np.array([[p[0], p[1], p[2], 1.0] for p in by_kind[kind]], dtype="f4")
            vao = self.ctx.vertex_array(
                self.flat_prog, [(self.ctx.buffer(pts.tobytes()), "3f 1f", "in_pos", "in_size")])
            self._feat_vaos.append((kind, vao, KIND_COLORS.get(kind, (0.8, 0.8, 0.8))))
        self.feature_counts = {k: len(v) for k, v in by_kind.items()}
        self.render_frame()

    def set_grid(self, bbox, spacing=4.0):
        if not self.ready or bbox is None:
            return
        lo = np.array(bbox[0], dtype=np.float64)
        hi = np.array(bbox[1], dtype=np.float64)
        y = float(lo[1]) - 0.05
        cx = (lo[0] + hi[0]) / 2.0
        cz = (lo[2] + hi[2]) / 2.0
        half = max(120.0, max(hi[0] - lo[0], hi[2] - lo[2]) * 0.9)
        n = int(half / spacing) + 1
        pts = []
        for i in range(-n, n + 1):
            x = cx + i * spacing
            pts.append((x, y, cz - half, 1.0))
            pts.append((x, y, cz + half, 1.0))
            z = cz + i * spacing
            pts.append((cx - half, y, z, 1.0))
            pts.append((cx + half, y, z, 1.0))
        arr = np.array(pts, dtype="f4")
        self._grid_vao = self.ctx.vertex_array(
            self.flat_prog, [(self.ctx.buffer(arr.tobytes()), "3f 1f", "in_pos", "in_size")])
        self.render_frame()

    # ---- 点选 -------------------------------------------------------
    def ray_from_pixel(self, x, y):
        w = max(1, self.width())
        h = max(1, self.height())
        nx = 2.0 * x / w - 1.0
        ny = 1.0 - 2.0 * y / h
        aspect = w / float(h)
        t = math.tan(math.radians(self.camera.fov) * 0.5)
        d = self.camera.forward() + self.camera.right() * (nx * t * aspect) + self.camera.up() * (ny * t)
        return self.camera.pos.copy(), d / np.linalg.norm(d)

    def pick(self, x, y):
        """射线拾取：返回 {chunk, point, dist, tri} 或 None。"""
        if self.geo is None or len(self.geo.indices) == 0:
            return None
        t0 = time.time()
        o, d = self.ray_from_pixel(x, y)
        tri = self.geo.indices
        pos = self.geo.positions
        v0 = pos[tri[:, 0]].astype(np.float64)
        e1 = pos[tri[:, 1]].astype(np.float64) - v0
        e2 = pos[tri[:, 2]].astype(np.float64) - v0
        pv = np.cross(d, e2)
        det = (e1 * pv).sum(1)
        ok = np.abs(det) > 1e-12
        inv = np.zeros_like(det)
        inv[ok] = 1.0 / det[ok]
        tv = o - v0
        u = (tv * pv).sum(1) * inv
        qv = np.cross(tv, e1)
        v = (d * qv).sum(1) * inv
        t = (e2 * qv).sum(1) * inv
        hit = ok & (u >= 0) & (u <= 1) & (v >= 0) & (u + v <= 1) & (t > 0.05)
        if not hit.any():
            return None
        idx = np.where(hit)[0]
        k = int(idx[np.argmin(t[idx])])
        chunk = -1
        if self.geo.chunks:
            starts = np.array([c["start"] for c in self.geo.chunks])
            chunk = int(np.clip(np.searchsorted(starts, k, side="right") - 1, 0, len(starts) - 1))
        self.selected_chunk = chunk
        return {
            "chunk": chunk,
            "tri": k,
            "dist": float(t[k]),
            "point": (o + d * float(t[k])).tolist(),
            "seconds": time.time() - t0,
        }

    def enter_first_person(self):
        """默认机位：站到连通度最高的路点上，看向它最远的邻居。"""
        nav = self.nav
        if nav is None or len(nav.nodes) == 0:
            self.focus_nav()
            return
        deg = np.zeros(len(nav.nodes), dtype=np.int32)
        if len(nav.edges):
            np.add.at(deg, nav.edges[:, 0], 1)
            np.add.at(deg, nav.edges[:, 1], 1)
        idx = int(np.argmax(deg))
        eye = nav.nodes[idx].astype(np.float64) + np.array([0.0, 1.7, 0.0])
        tgt = None
        if len(nav.edges):
            nb = nav.edges[(nav.edges[:, 0] == idx) | (nav.edges[:, 1] == idx)]
            if len(nb):
                cand = np.where(nb[:, 0] == idx, nb[:, 1], nb[:, 0])
                d = np.linalg.norm(nav.nodes[cand] - nav.nodes[idx], axis=1)
                tgt = nav.nodes[int(cand[int(np.argmax(d))])].astype(np.float64)
        if tgt is None:
            c = nav.nodes.mean(0).astype(np.float64)
            tgt = c
        self.camera.pos = eye
        self.camera.look_dir(tgt - np.array([eye[0], eye[1] - 1.5, eye[2]]))
        self.render_frame()
        self.update()

    def focus_nav(self):
        if self.nav is not None and len(self.nav.nodes):
            bb = self.nav.bbox()
        elif self.geo is not None:
            bb = self.geo.bbox
        else:
            return
        c = (bb[0] + bb[1]) / 2.0
        span = float(np.linalg.norm(bb[1] - bb[0]))
        self.camera.move_at(c, max(40.0, span * 1.1))
        self.render_frame()
        self.update()

    def readback_stats(self):
        if self._fbo is None:
            return None, None
        w, h = self._fbo_size
        data = self._fbo.read(components=3)
        img = np.frombuffer(data, dtype=np.uint8).reshape(h, w, 3)[::-1]
        bg = np.array([int(c * 255) for c in self.bg])
        return int((np.abs(img.astype(int) - bg).sum(2) > 8).sum()), img

    def snapshot(self):
        self.render_frame()
        return self.image

    # ---- 输入 -------------------------------------------------------
    def keyPressEvent(self, ev):
        k = ev.key()
        if k in (QtCore.Qt.Key_W, QtCore.Qt.Key_A, QtCore.Qt.Key_S, QtCore.Qt.Key_D,
                 QtCore.Qt.Key_Q, QtCore.Qt.Key_E):
            self.keys.add(k)
            return
        if k == QtCore.Qt.Key_F:
            self.focus_nav()
        elif k == QtCore.Qt.Key_Tab:
            self.camera.pitch = -1.45
            self.camera.pos = self.camera.pos + np.array([0.0, 40.0, 0.0])
        elif k == QtCore.Qt.Key_M:
            self.show_mesh = not self.show_mesh
        elif k == QtCore.Qt.Key_T:
            self.show_tex = not self.show_tex
        elif k == QtCore.Qt.Key_G:
            self.show_nodes = not self.show_nodes
        elif k == QtCore.Qt.Key_R:
            self.show_edges = not self.show_edges
        super().keyPressEvent(ev)

    def keyReleaseEvent(self, ev):
        self.keys.discard(ev.key())
        super().keyReleaseEvent(ev)

    def mousePressEvent(self, ev):
        self.last_mouse = ev.pos()
        self.press_pos = ev.pos()
        if ev.button() == QtCore.Qt.RightButton:
            self.grab_look = True
            self.setCursor(QtCore.Qt.BlankCursor)
        elif ev.button() == QtCore.Qt.MiddleButton:
            self.pan_drag = True
        self.setFocus()
        super().mousePressEvent(ev)

    def mouseReleaseEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.grab_look = False
            self.setCursor(QtCore.Qt.ArrowCursor)
        elif ev.button() == QtCore.Qt.MiddleButton:
            self.pan_drag = False
        elif ev.button() == QtCore.Qt.LeftButton and self.press_pos is not None:
            moved = (ev.pos() - self.press_pos).manhattanLength()
            if moved < 5:
                hit = self.pick(ev.pos().x(), ev.pos().y())
                self.picked.emit(hit)
        super().mouseReleaseEvent(ev)

    def mouseMoveEvent(self, ev):
        if self.last_mouse is None:
            self.last_mouse = ev.pos()
        dx = ev.pos().x() - self.last_mouse.x()
        dy = ev.pos().y() - self.last_mouse.y()
        self.last_mouse = ev.pos()
        if self.grab_look:
            self.camera.yaw += dx * 0.004
            self.camera.pitch -= dy * 0.004
            lim = math.radians(89.0)
            self.camera.pitch = max(-lim, min(lim, self.camera.pitch))
        elif self.pan_drag:
            r = self.camera.right()
            up = np.cross(r, self.camera.forward())
            scale = max(0.05, abs(self.camera.pos[1]) * 0.0016 + 0.05)
            self.camera.pos = self.camera.pos - r * dx * scale + up * dy * scale
        super().mouseMoveEvent(ev)

    def wheelEvent(self, ev):
        steps = ev.angleDelta().y() / 120.0
        self.camera.pos = self.camera.pos + self.camera.forward() * (steps * 10.0)
        super().wheelEvent(ev)
