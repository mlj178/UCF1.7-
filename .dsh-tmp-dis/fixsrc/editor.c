/* editor.c - ucf_mod in-game AI marker editor
 *
 * phase 1: crouch / nano guard pos / nano guard area placement + save/load
 * phase 2: per-type colours, delete ANY marker near the crosshair, on-screen HUD
 *
 * Ctrl+1  toggle edit mode        Ctrl+2  place Bot_CrouchPos (crosshair ground)
 * Ctrl+3  place Bot_NanoGuardPos  Ctrl+4  new Bot_NanoGuardArea
 * Ctrl+5  undo last marker        Ctrl+6  save markers file
 * Ctrl+7  reload markers file     Ctrl+8  team BL/GR for new crouch points
 * Ctrl+9  status log              Ctrl+0  show/hide every marker visual
 * Ctrl+Del remove the marker nearest the crosshair (within 3 m)
 *
 * Marker colours: crouch=red  nanopos=green  area=blue  jumplink=yellow
 */
#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>
#include <stdlib.h>
#include <math.h>

typedef void* P;
typedef struct { float x, y, z; } V3;
typedef struct { float x, y; } V2;
typedef struct { float r, g, b, a; } COL;

/* UnityEngine.Object.m_CachedPtr (+0x8) is cleared when the native object is
 * destroyed.  Touching a destroyed component from native code raises a managed
 * MissingReferenceException; IL2CPP cannot unwind into C, so it aborts. */
static int uobj_live(P o) { return o && *(P*)((char*)o + 0x8) != 0; }

#define MAXM      600
#define MAX_AID   64
#define DEL_RADIUS 3.0f

/* Nano guard area / position creation is DISABLED in this build.
 * Reason (verified from GameAssembly decompilation on 2026-11-14):
 *   Bot_NanoGuardArea.Awake() reads this.posList FIRST and only fills it
 *   (GetComponentsInChildren + Init loop) when the field is non-null; a
 *   runtime AddComponent() leaves it null, so the area stays registered but
 *   posless -> Bot.Update throws NullReferenceException every frame.
 *   Bot_NanoGuardPos.Init() additionally does List.AddRange(zoomPos) and
 *   List.AddRange(area.entrancePos), both of which throw on null, and
 *   GetRandomZoomPos() indexes zoomPos[0], so a pos needs >=1 zoom target.
 * Re-enable only after posList / entrancePos / zoomPos are constructed properly. */
#define ED_AREA_ENABLED 0

static HMODULE g_ga;
static char g_log[MAX_PATH];
static char g_dir[MAX_PATH];
static char g_file[MAX_PATH];
static int  g_inited, g_initFail;
static int  g_on, g_team, g_vis = 1;
static int  g_n, g_areaCount, g_curArea = -1;
static P    g_lastAstar;

static P (*x_domain_get)(void);
static P (*x_domain_get_assemblies)(P, int*);
static P (*x_assembly_get_image)(P);
static const char* (*x_image_get_name)(P);
static P (*x_class_from_name)(P, const char*, const char*);
static P (*x_class_get_type)(P);
static P (*x_type_get_object)(P);
static P (*x_object_new)(P);
static P (*x_string_new)(const char*);
static P (*x_thread_attach)(P);
static P (*x_class_get_field_from_name)(P, const char*);
static void (*x_field_static_get_value)(P, void*);
static P (*x_array_new)(P, unsigned int);
static P (*x_class_get_parent)(P);
static P (*x_domain_assembly_open)(P, const char*);
static unsigned (*x_gchandle_new)(P, unsigned char);
static void (*x_gchandle_free)(P);

static P g_goCls, g_camCls, g_colCls, g_boxCls, g_crouchCls, g_areaCls, g_posCls;
static P g_colType, g_boxType, g_crouchType, g_areaType, g_posType;
static P g_rendCls, g_rendType, g_textCls, g_textType, g_canvasCls, g_canvasType, g_fontCls, g_fontType;

static P g_matCls;
static P g_meshCls, g_mfCls, g_mrCls, g_vec3Cls, g_i32Cls;
static P g_guardCls, g_jumpCls, g_tagCls, g_gareaCls;
static P g_mmCls, g_mmInstField;
static P g_mfType, g_mrType, g_guardType, g_jumpType, g_tagType, g_gareaType;
static P g_matProto;     /* working template material (game shader) */
static char g_shaderName[96]; /* cached shader path, so materials survive asset unloads */
static P g_matSlot[16];  /* cached material per marker type 1..15   */
static int g_matReady;

/* 路点图编辑（定义在文件后半段，这里提前声明给 ed_init/editor_on_scene 用） */
typedef struct { int kind; V3 a, b; } NAVED;
#define NAV_ED_MAX 512
static NAVED g_ned[NAV_ED_MAX];
static int g_nedN;
static char g_nedPath[MAX_PATH];
static char g_nedFp[48];
static int g_nedBaseN;
static int g_nedApplied;
static int g_nedWaitN;
static P   g_nedGraph;
static int g_nedHasA;
static V3  g_nedA;
static P   g_pnodeCls, g_connCls;

static P g_hud;          /* UGUI Text component: status panel */
static P g_hudGo;
static P g_keys;         /* UGUI Text component: hotkey panel */
static P g_keysGo;
static P g_guiFont;      /* font borrowed from the game UI (has CJK glyphs) */
static int g_cjk;        /* 1 = game font available, hint text in Chinese */
static int g_tintLogged; /* one-shot material/shader diagnostic */

#define RVA(x) ((void*)((char*)g_ga + (unsigned)(x)))

#define R_GOCREATE    0x331AF0
#define R_ADDCOMP     0x331A90
#define R_GETCOMP     0x331C10
#define R_CTOR_STR    0x331EA0
#define R_GET_TR      0x332010
#define R_SETACTIVE   0x331CF0
#define R_SETLAYER    0x332040
#define R_GETGO       0x32CEB0
#define R_SET_POS     0x3F4840
#define R_GET_POS_INJ 0x3F4280
#define R_TDIR_INJ    0x3F3B70
#define R_SET_SCALE   0x3F4730
#define R_SET_PARENT  0x3F3AB0
#define R_CAM_MAIN    0x328310
#define R_DESTROY     0x4E9210
#define R_IS_TRIGGER  0xAB86E0
#define R_RAYCAST     0xABB0A0
#define R_POS_INIT    0xB30E80
/* phase 2: colours + HUD */
#define R_REND_GETMAT  0x3E4BE0   /* Renderer.get_material  (instanced)      */
#define R_REND_SHADOW  0x3E50C0   /* Renderer.set_shadowCastingMode(enum)    */
#define R_MAT_HASPROP  0x4E1830   /* Material.HasProperty(string)            */
#define R_MAT_SETCOL_S 0x4E18D0   /* Material.SetColor(string, Color)        */
#define R_MAT_SETCOL   0x4E25C0   /* Material.set_color(Color)               */
#define R_CANVAS_MODE  0xAC6D10   /* Canvas.set_renderMode                   */
#define R_CANVAS_SORT  0xAC6DB0   /* Canvas.set_sortingOrder                 */
#define R_TEXT_GETFONT 0x9621D0
#define R_TEXT_SETFONT 0x9629D0
#define R_TEXT_SETTEXT 0x962CE0
#define R_TEXT_SETSIZE 0x962930
#define R_TEXT_ALIGN   0x9628E0
#define R_TEXT_HOVER   0x962AF0
#define R_TEXT_VOVER   0x962DA0
#define R_GRAPHIC_COL  0x321260   /* Graphic.set_color(Color)                */
#define R_GRAPHIC_RAY  0x321340   /* Graphic.set_raycastTarget(bool)         */
#define R_RT_AMIN      0x4F4AB0
#define R_RT_AMAX      0x4F4A50
#define R_RT_PIVOT     0x4F5030
#define R_RT_APOS      0x4F4B90
#define R_RT_SDELTA    0x4F5090
#define R_FINDOBJ      0x4E95A0   /* Object.FindObjectOfType(Type, bool)     */
#define R_RES_BUILTIN  0x3E5530   /* Resources.GetBuiltinResource(Type,str)  */
#define R_MAT_GETSH   0x4E2590   /* Material.get_shader                     */
#define R_SHADER_FIND 0x3E8A70   /* Shader.Find(string)                     */
#define R_MAT_CTOR_SH 0x4E21F0   /* Material..ctor(Shader)                  */
#define R_MAT_CTOR_MT 0x4E2170   /* Material..ctor(Material source)         */
#define R_REND_GETSM  0x3E4C40   /* Renderer.get_sharedMaterial             */
#define R_REND_SETSM  0x3E4CA0   /* Renderer.set_sharedMaterial             */
#define R_OBJ_NAME    0x4EA1B0   /* Object.get_name                         */
/* phase 3: real-graph visualizer */
#define R_COMP_TR     0x32CF40   /* Component.get_transform                 */
#define R_W2S_INJ     0x327EE0   /* Camera.WorldToScreenPoint_Injected      */
#define R_W2S         0x327F70   /* Camera.WorldToScreenPoint(Vector3)      */
#define R_FINDOBJS    0x4E9620   /* Object.FindObjectsOfType(Type,bool)     */
#define R_MESH_CTOR   0x4E8030   /* Mesh..ctor()                            */
#define R_MESH_VERTS  0x4E8510   /* Mesh.set_vertices(Vector3[])            */
#define R_MESH_TRIS   0x4E8420   /* Mesh.set_triangles(int[])               */
#define R_MESH_BOUNDS 0x4E6F50   /* Mesh.RecalculateBounds()                */
#define R_MF_SETMESH  0x4E62A0   /* MeshFilter.set_mesh(Mesh)               */

typedef unsigned char (*raycast_t)(V3, V3, void*, float, int, void*);
typedef void (*ctor_str_t)(P, P, void*);
typedef P    (*get_tr_t)(P, void*);
typedef P    (*get_go_t)(P, void*);
typedef void (*set_pos_t)(P, V3, void*);
typedef void (*get_pos_t)(P, V3*, void*);
typedef void (*tdir_t)(P, V3*, V3*, void*);
typedef void (*set_parent_t)(P, P, unsigned char, void*);
typedef void (*set_scale_t)(P, V3, void*);
typedef void (*set_active_t)(P, unsigned char, void*);
typedef void (*set_layer_t)(P, int, void*);
typedef void (*set_trigger_t)(P, unsigned char, void*);
typedef void (*destroy_t)(P, void*);
typedef P    (*create_prim_t)(int, void*);
typedef P    (*addcomp_t)(P, P, void*);
typedef P    (*getcomp_t)(P, P, void*);
typedef P    (*cam_main_t)(void*);
typedef void (*pos_init_t)(P, P, void*);
typedef P    (*get_mat_t)(P, void*);
typedef void (*set_int1_t)(P, int, void*);
typedef unsigned char (*has_prop_t)(P, P, void*);
typedef void (*set_col_s_t)(P, P, COL, void*);
typedef void (*set_col_t)(P, COL, void*);
typedef P    (*find_obj_t)(P, unsigned char, void*);
typedef P    (*builtin_t)(P, P, void*);
typedef void (*set_txt_t)(P, P, void*);
typedef P    (*get_font_t)(P, void*);
typedef void (*set_font_t)(P, P, void*);
typedef void (*set_v2_t)(P, V2, void*);
typedef P    (*get_name_t)(P, void*);
typedef P    (*get_shader_t)(P, void*);
typedef P    (*shader_find_t)(P, void*);
typedef void (*ctor_sh_t)(P, P, void*);
typedef void (*ctor_mat_t)(P, P, void*);
typedef P    (*get_shmat_t)(P, void*);
typedef void (*set_shmat_t)(P, P, void*);
typedef void (*w2s_t)(P, V3*, int, V3*);
typedef V3   (*w2s2_t)(P, V3, void*);
typedef P    (*find_objs_t)(P, unsigned char, void*);
typedef void (*mesh_ctor_t)(P, void*);
typedef void (*mesh_arr_t)(P, P, void*);
typedef void (*mesh_1_t)(P, void*);
typedef void (*mf_setmesh_t)(P, P, void*);

typedef struct {
  int type;     /* 1=crouch 2=nanopos 3=area 4=jumplink */
  V3  p;
  int aid;
  int parent;
  int prm;
  P   go;
  P   comp;
  P   vis;
} MK;

static MK g_mk[MAXM];
static P  g_aidMk[MAX_AID];

/* marker type colours */
static const COL COL_CROUCH = { 1.00f, 0.15f, 0.12f, 1.0f };  /* red    */
static const COL COL_POS    = { 0.10f, 1.00f, 0.25f, 1.0f };  /* green  */
static const COL COL_AREA   = { 0.15f, 0.40f, 1.00f, 1.0f };  /* blue   */
static const COL COL_JUMP   = { 1.00f, 0.88f, 0.05f, 1.0f };  /* yellow */
static const COL COL_WHITE  = { 1.00f, 1.00f, 1.00f, 1.0f };
/* visualizer palette (slots 5..15) */
static const COL COL_NODE   = { 0.80f, 0.88f, 1.00f, 1.0f };  /* graph node, tag 1 */
static const COL COL_NODE1  = { 1.00f, 0.55f, 0.05f, 1.0f };  /* graph node, tag != 0 / guard pos */
static const COL COL_EDGE   = { 0.25f, 0.45f, 0.95f, 1.0f };  /* point graph connection */
static const COL COL_CYAN   = { 0.10f, 0.95f, 0.95f, 1.0f };
static const COL COL_PURPLE = { 0.75f, 0.35f, 1.00f, 1.0f };
static const COL COL_PINK   = { 1.00f, 0.35f, 0.70f, 1.0f };
static const COL COL_GOLD   = { 1.00f, 0.85f, 0.20f, 1.0f };
static const COL COL_GRAY   = { 0.70f, 0.70f, 0.70f, 1.0f };

static void elog(const char* fmt, ...) {
  FILE* f;
  SYSTEMTIME st;
  va_list ap;
  if (!g_log[0]) return;
  f = fopen(g_log, "a");
  if (!f) return;
  GetLocalTime(&st);
  fprintf(f, "%04d-%02d-%02d %02d:%02d:%02d [edit] ", st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond);
  va_start(ap, fmt);
  vfprintf(f, fmt, ap);
  va_end(ap);
  fprintf(f, "\n");
  fclose(f);
}

static P find_img(const char* name) {
  int n = 0;
  P arr;
  int i;
  if (!x_domain_get || !x_domain_get_assemblies) return 0;
  arr = x_domain_get_assemblies(x_domain_get(), &n);
  if (!arr) return 0;
  for (i = 0; i < n; i++) {
    P asm_ = *(P*)((char*)arr + 0x10 + i * 4);
    P img;
    if (!asm_) break;
    img = x_assembly_get_image(asm_);
    if (img && strcmp(x_image_get_name(img), name) == 0) return img;
  }
  return 0;
}

static int g_clsProbe;

static P find_cls(const char* ns, const char* name) {
  int n = 0;
  P arr;
  int i;
  if (!x_domain_get) return 0;
  arr = x_domain_get_assemblies(x_domain_get(), &n);
  if (g_clsProbe) elog("cls probe ns='%s' name='%s' n=%d arr=%p", ns, name, n, arr);
  if (!arr) return 0;
  for (i = 0; i < n; i++) {
    P asm_ = *(P*)((char*)arr + 0x10 + i * 4);
    P img;
    P c;
    if (!asm_) break;   /* tail of the assembly array is uninitialised */
    img = x_assembly_get_image(asm_);
    if (!img) continue;
    if (g_clsProbe) elog("cls probe i=%d img=%p", i, img);
    c = x_class_from_name(img, ns, name);
    if (g_clsProbe) elog("cls probe i=%d -> %p", i, c);
    if (c) return c;
  }
  return 0;
}

#define RESOLVE(n) do { *(void**)&x_##n = GetProcAddress(g_ga, "il2cpp_" #n); } while (0)

static int ed_init(void) {
  if (g_inited) return 1;
  elog("init: start");
  if (!g_ga) g_ga = GetModuleHandleA("GameAssembly.dll");
  if (!g_ga) return 0;
  if (g_initFail) return 0;

  RESOLVE(domain_get);
  RESOLVE(domain_get_assemblies);
  RESOLVE(assembly_get_image);
  RESOLVE(image_get_name);
  RESOLVE(class_from_name);
  RESOLVE(class_get_type);
  RESOLVE(type_get_object);
  RESOLVE(object_new);
  RESOLVE(string_new);
  RESOLVE(thread_attach);
  RESOLVE(class_get_field_from_name);
  RESOLVE(field_static_get_value);
  RESOLVE(array_new);
  RESOLVE(class_get_parent);
  RESOLVE(domain_assembly_open);
  RESOLVE(gchandle_new);
  RESOLVE(gchandle_free);
  if (!x_domain_get || !x_object_new || !x_string_new || !x_class_from_name || !x_class_get_type) {
    g_initFail = 1;
    elog("il2cpp exports missing");
    return 0;
  }
  elog("init: exports ok (array_new=%p parent=%p)", (void*)x_array_new, (void*)x_class_get_parent);
  if (!x_domain_get()) return 0;
  elog("init: domain=%p", x_domain_get());
  if (x_thread_attach) x_thread_attach(x_domain_get());
  elog("init: thread attached");

  g_goCls = find_cls("UnityEngine", "GameObject");
  g_camCls = find_cls("UnityEngine", "Camera");
  g_colCls = find_cls("UnityEngine", "Collider");
  g_boxCls = find_cls("UnityEngine", "BoxCollider");
  g_crouchCls = find_cls("", "Bot_CrouchPos");
  g_areaCls = find_cls("", "Bot_NanoGuardArea");
  g_posCls = find_cls("", "Bot_NanoGuardPos");
  g_rendCls = find_cls("UnityEngine", "Renderer");
  g_matCls = find_cls("UnityEngine", "Material");
  g_textCls = find_cls("UnityEngine.UI", "Text");
  g_canvasCls = find_cls("UnityEngine", "Canvas");
  g_fontCls = find_cls("UnityEngine", "Font");
  g_meshCls = find_cls("UnityEngine", "Mesh");
  g_mfCls = find_cls("UnityEngine", "MeshFilter");
  g_mrCls = find_cls("UnityEngine", "MeshRenderer");
  g_vec3Cls = find_cls("UnityEngine", "Vector3");
  elog("init: render classes ok");
  /* System.Int32 lives in the core library, which sits past the uninitialised
   * tail of the assemblies array - open that assembly by name instead. */
  g_i32Cls = 0;
  if (x_domain_assembly_open) {
    static const char* core[] = { "mscorlib.dll", "mscorlib", "System.Private.CoreLib.dll", "System.Private.CoreLib" };
    int ci;
    for (ci = 0; ci < 4 && !g_i32Cls; ci++) {
      P asm_ = x_domain_assembly_open(x_domain_get(), core[ci]);
      P img = asm_ ? x_assembly_get_image(asm_) : 0;
      elog("init: core '%s' asm=%p img=%p", core[ci], asm_, img);
      if (img) g_i32Cls = x_class_from_name(img, "System", "Int32");
    }
  }
  elog("init: i32=%p", g_i32Cls);
  g_pnodeCls = find_cls("Pathfinding", "PointNode");
  g_connCls = find_cls("Pathfinding", "Connection");
  elog("init: pointnode=%p connection=%p", g_pnodeCls, g_connCls);
  g_guardCls = find_cls("", "Bot_GuardPos");
  g_jumpCls = find_cls("", "Bot_JumpLink");
  g_tagCls = find_cls("", "PointNodeTagModifier");
  g_gareaCls = find_cls("", "Bot_GuardArea");
  elog("init: core classes ok");
  g_mmCls = find_cls("", "MapManager");
  if (g_mmCls && x_class_get_parent) {
    P base = x_class_get_parent(g_mmCls);
    if (base) g_mmInstField = x_class_get_field_from_name(base, "<instance>k__BackingField");
  }

  if (g_colCls) g_colType = x_type_get_object(x_class_get_type(g_colCls));
  if (g_boxCls) g_boxType = x_type_get_object(x_class_get_type(g_boxCls));
  if (g_crouchCls) g_crouchType = x_type_get_object(x_class_get_type(g_crouchCls));
  if (g_areaCls) g_areaType = x_type_get_object(x_class_get_type(g_areaCls));
  if (g_posCls) g_posType = x_type_get_object(x_class_get_type(g_posCls));
  if (g_rendCls) g_rendType = x_type_get_object(x_class_get_type(g_rendCls));
  if (g_textCls) g_textType = x_type_get_object(x_class_get_type(g_textCls));
  if (g_canvasCls) g_canvasType = x_type_get_object(x_class_get_type(g_canvasCls));
  if (g_fontCls) g_fontType = x_type_get_object(x_class_get_type(g_fontCls));
  if (g_mfCls) g_mfType = x_type_get_object(x_class_get_type(g_mfCls));
  if (g_mrCls) g_mrType = x_type_get_object(x_class_get_type(g_mrCls));
  if (g_guardCls) g_guardType = x_type_get_object(x_class_get_type(g_guardCls));
  if (g_jumpCls) g_jumpType = x_type_get_object(x_class_get_type(g_jumpCls));
  if (g_tagCls) g_tagType = x_type_get_object(x_class_get_type(g_tagCls));
  if (g_gareaCls) g_gareaType = x_type_get_object(x_class_get_type(g_gareaCls));

  g_inited = 1;
  elog("init: GameObject=%p Camera=%p Collider=%p Box=%p crouch=%p area=%p pos=%p renderer=%p text=%p canvas=%p font=%p",
       g_goCls, g_camCls, g_colCls, g_boxCls, g_crouchCls, g_areaCls, g_posCls, g_rendCls, g_textCls, g_canvasCls, g_fontCls);
  if (!g_goCls || !g_camCls || !g_crouchType || !g_areaType || !g_posType) {
    elog("init: REQUIRED class missing - editor disabled");
    g_initFail = 1;
    return 0;
  }
  return 1;
}

static P get_tr(P go) { return go ? ((get_tr_t)RVA(R_GET_TR))(go, 0) : 0; }
static P new_go(const char* name) {
  P go = x_object_new(g_goCls);
  if (!go) return 0;
  ((ctor_str_t)RVA(R_CTOR_STR))(go, x_string_new(name), 0);
  return go;
}

static int cam_ray(V3* cpos, V3* fwd) {
  P cam, go, tr;
  V3 dir;
  cam = ((cam_main_t)RVA(R_CAM_MAIN))(0);
  if (!cam) return 0;
  go = ((get_go_t)RVA(R_GETGO))(cam, 0);
  tr = get_tr(go);
  if (!tr) return 0;
  ((get_pos_t)RVA(R_GET_POS_INJ))(tr, cpos, 0);
  dir.x = 0.0f; dir.y = 0.0f; dir.z = 1.0f;
  ((tdir_t)RVA(R_TDIR_INJ))(tr, &dir, fwd, 0);
  return 1;
}

static int cam_point(V3* out) {
  P cam, go, tr;
  V3 pos, dir, fw;
  char hit[128];
  raycast_t rc = (raycast_t)RVA(R_RAYCAST);
  cam = ((cam_main_t)RVA(R_CAM_MAIN))(0);
  if (!cam) return 0;
  go = ((get_go_t)RVA(R_GETGO))(cam, 0);
  tr = get_tr(go);
  if (!tr) return 0;
  ((get_pos_t)RVA(R_GET_POS_INJ))(tr, &pos, 0);
  dir.x = 0.0f; dir.y = 0.0f; dir.z = 1.0f;
  ((tdir_t)RVA(R_TDIR_INJ))(tr, &dir, &fw, 0);
  pos.x += fw.x * 0.4f; pos.y += fw.y * 0.4f; pos.z += fw.z * 0.4f;
  if (rc(pos, fw, hit, 300.0f, 1, 0)) { *out = *(V3*)hit; return 1; }
  dir.x = 0.0f; dir.y = -1.0f; dir.z = 0.0f;
  if (rc(pos, dir, hit, 120.0f, 1, 0)) { *out = *(V3*)hit; return 1; }
  return 0;
}

/* ---- per-type colour ---------------------------------------------------- */
static void str_ascii(P s, char* out, int cap) {
  int i, n;
  if (!s || cap <= 0) { if (cap > 0) out[0] = 0; return; }
  n = *(int*)((char*)s + 0x08);
  if (n < 0) n = 0;
  if (n > cap - 1) n = cap - 1;
  for (i = 0; i < n; i++) {
    unsigned short ch = *(unsigned short*)((char*)s + 0x0C + i * 2);
    out[i] = (ch > 0 && ch < 128) ? (char)ch : '?';
  }
  out[n] = 0;
}

static const COL* col_of(int slot) {
  switch (slot) {
    case 1: return &COL_CROUCH;
    case 2: return &COL_POS;
    case 3: return &COL_AREA;
    case 4: return &COL_JUMP;
    case 5: return &COL_NODE;
    case 6: return &COL_CYAN;
    case 7: return &COL_NODE1;
    case 8: return &COL_PURPLE;
    case 9: return &COL_PINK;
    case 10: return &COL_EDGE;
    case 11: return &COL_AREA;
    case 12: return &COL_CROUCH;
    case 13: return &COL_GRAY;
    case 14: return &COL_GOLD;
    default: return &COL_WHITE;
  }
}

static int mat_usable(P m) {
  has_prop_t hasProp = (has_prop_t)RVA(R_MAT_HASPROP);
  if (!m) return 0;
  return hasProp(m, x_string_new("_BaseColor"), 0) || hasProp(m, x_string_new("_Color"), 0);
}

/* The runtime primitive ships with Hidden/InternalErrorShader (the build stripped
 * Unity's default material), so every marker gets a material we build ourselves. */
static int mat_setup(void) {
  static const char* cand[] = {
    "Universal Render Pipeline/Unlit",
    "Universal Render Pipeline/Lit",
    "Universal Render Pipeline/Simple Lit",
    "Sprites/Default",
    "Unlit/Color",
    "Standard",
    "Legacy Shaders/Diffuse",
    "Hidden/Internal-Colored"
  };
  int i;
  if (g_matReady) return 1;
  if (!g_matCls) { elog("mat: no Material class"); return 0; }
  for (i = 0; i < (int)(sizeof(cand) / sizeof(cand[0])); i++) {
    P sh = ((shader_find_t)RVA(R_SHADER_FIND))(x_string_new(cand[i]), 0);
    P m;
    if (!sh) continue;
    m = x_object_new(g_matCls);
    if (!m) continue;
    ((ctor_sh_t)RVA(R_MAT_CTOR_SH))(m, sh, 0);
    if (mat_usable(m)) {
      g_matProto = m;
      g_matReady = 1;
      strncpy(g_shaderName, cand[i], sizeof(g_shaderName) - 1);
      if (x_gchandle_new) x_gchandle_new(m, 1);
      elog("mat: using shader '%s' (candidate #%d)", cand[i], i);
      return 1;
    }
  }
  if (g_rendType) {   /* fallback: clone a material the scene already renders with */
    P any = ((find_obj_t)RVA(R_FINDOBJ))(g_rendType, 1, 0);
    P src = any ? ((get_shmat_t)RVA(R_REND_GETSM))(any, 0) : 0;
    if (src && mat_usable(src)) {
      P m = x_object_new(g_matCls);
      if (m) {
        char nm[96];
        ((ctor_mat_t)RVA(R_MAT_CTOR_MT))(m, src, 0);
        g_matProto = m;
        g_matReady = 1;
        str_ascii(((get_name_t)RVA(R_OBJ_NAME))(src, 0), nm, sizeof(nm));
        elog("mat: cloned scene material '%s'", nm);
        return 1;
      }
    }
  }
  elog("mat: no usable shader - markers stay invisible");
  return 0;
}

static P mat_for(int slot) {
  COL c;
  P m;
  has_prop_t hasProp;
  set_col_s_t setColS;
  if (slot < 0 || slot > 15) slot = 0;
  if (g_matSlot[slot]) return g_matSlot[slot];
  if (!g_matReady && !mat_setup()) return 0;
  c = *col_of(slot);
  m = 0;
  if (g_shaderName[0]) {
    P sh = ((shader_find_t)RVA(R_SHADER_FIND))(x_string_new(g_shaderName), 0);
    if (sh) {
      m = x_object_new(g_matCls);
      if (m) ((ctor_sh_t)RVA(R_MAT_CTOR_SH))(m, sh, 0);
    }
  }
  if (!m) {
    elog("mat_for %d: no shader, cloning prototype", slot);
    if (!g_matProto) return 0;
    m = x_object_new(g_matCls);
    if (!m) return 0;
    ((ctor_mat_t)RVA(R_MAT_CTOR_MT))(m, g_matProto, 0);
  }
  hasProp = (has_prop_t)RVA(R_MAT_HASPROP);
  setColS = (set_col_s_t)RVA(R_MAT_SETCOL_S);
  if (hasProp(m, x_string_new("_BaseColor"), 0)) setColS(m, x_string_new("_BaseColor"), c, 0);
  if (hasProp(m, x_string_new("_Color"), 0)) setColS(m, x_string_new("_Color"), c, 0);
  g_matSlot[slot] = m;
  if (x_gchandle_new) x_gchandle_new(m, 1);   /* root: C globals are not GC roots */
  return m;
}

static void tint(P go, int slot) {
  P rend, mat;
  if (!go || !g_rendType) return;
  rend = ((getcomp_t)RVA(R_GETCOMP))(go, g_rendType, 0);
  if (!rend) return;
  ((set_int1_t)RVA(R_REND_SHADOW))(rend, 0, 0);      /* no shadows */
  mat = mat_for(slot);
  if (mat) {
    ((set_shmat_t)RVA(R_REND_SETSM))(rend, mat, 0);
    if (!g_tintLogged) {
      char mn[96], sn[96];
      P sh = ((get_shader_t)RVA(R_MAT_GETSH))(mat, 0);
      str_ascii(((get_name_t)RVA(R_OBJ_NAME))(mat, 0), mn, sizeof(mn));
      if (sh) str_ascii(((get_name_t)RVA(R_OBJ_NAME))(sh, 0), sn, sizeof(sn)); else strcpy(sn, "<null>");
      elog("tint: slot=%d material='%s' shader='%s'", slot, mn, sn);
      g_tintLogged = 1;
    }
    return;
  }
  mat = ((get_mat_t)RVA(R_REND_GETMAT))(rend, 0);
  if (mat) ((set_col_t)RVA(R_MAT_SETCOL))(mat, *col_of(slot), 0);
}

static P spawn_vis(V3 p, float s, int slot) {
  P go, tr, col;
  V3 sc = { s, s, s }, up = { p.x, p.y + 0.45f, p.z };
  if (!g_vis) return 0;
  go = ((create_prim_t)RVA(R_GOCREATE))(0, 0);
  if (!go) return 0;
  /* layer must be inside Camera.cullingMask (measured 0x1f3 - layer 2 "Ignore
   * Raycast" is NOT included, which made phase-1 markers invisible) */
  ((set_layer_t)RVA(R_SETLAYER))(go, 0, 0);
  tr = get_tr(go);
  if (tr) {
    ((set_scale_t)RVA(R_SET_SCALE))(tr, sc, 0);
    ((set_pos_t)RVA(R_SET_POS))(tr, up, 0);
  }
  if (g_colType) {
    col = ((getcomp_t)RVA(R_GETCOMP))(go, g_colType, 0);
    if (col) ((destroy_t)RVA(R_DESTROY))(col, 0);
  }
  tint(go, slot);
  return go;
}

/* ===================== graph visualizer: layers A-E ======================
 * Reads the real runtime data on the game main thread and renders it as
 * batched meshes + UGUI labels.  Nothing here feeds back into the AI.
 *
 *   A  A* PointGraph nodes / connections, Bot_JumpLink, PointNodeTagModifier
 *   B  Bot_CrouchPos (SpareList_BL/GR), Bot_GuardPos, Bot_GuardArea
 *   C  Bot_NanoGuardArea (SpareAreaList) + Bot_NanoGuardPos
 *   D  MapManager SP_BL / GR / Netural / SupplyBox / RedBox / BlueBox
 *   E  mode state (HUD only)
 * ------------------------------------------------------------------------- */
P navfix_point_graph(void);
P navfix_add_guard_area(float x, float y, float z);

#define VIS_MAXN    6000
#define VIS_MAXE    20000
#define VIS_MAXF    1400
#define VIS_NBMAX   2048
#define MB_MAXV     20000
#define MB_MAXI     70000

#define LAY_A 0x01
#define LAY_B 0x02
#define LAY_C 0x04
#define LAY_D 0x08
#define LAY_E 0x10

#define K_NAREA   1
#define K_NPOS    2
#define K_CROUCH  3
#define K_GUARD   4
#define K_GAREA   5
#define K_SPAWN   6
#define K_JUMP    7
#define K_TAG     8

typedef struct { V3 p; int tag; int walk; unsigned int pen; } VN;
typedef struct { int a, b; } VE;
typedef struct { V3 p; int kind; int aux; char name[48]; } VF;

static VN g_vn[VIS_MAXN];
static int g_vnN;
static VE g_ve[VIS_MAXE];
static int g_veN;
static VF g_vf[VIS_MAXF];
static int g_vfN;
static V3 g_nA[VIS_NBMAX], g_nB[VIS_NBMAX];
static int g_nN;
static V3 g_eA[VIS_NBMAX], g_eB[VIS_NBMAX];
static int g_eN;
static V3 g_jA[512], g_jB[512];
static int g_jN;
static V3 g_tp[512];
static int g_tpN;

static P g_visObj[80];
static int g_visObjN;
static P g_lblCanvas, g_lblTr;
static P g_lblComp[VIS_MAXF];
static unsigned char g_lblHidden[VIS_MAXF];
static int g_lblShown;

static int g_visOn, g_lay = LAY_A | LAY_B | LAY_C | LAY_D | LAY_E, g_lblMode = 0;  /* 0 = no world-space text: it clutters the view */
static int g_visDirty, g_visNoMesh;
static int g_autoExport = 1;      /* 图有节点且稳定后自动导出一份路点 JSON */
static int g_aeNodes = -1;        /* 自动导出：上次看到的节点数 */
static int g_aeHold;              /* 自动导出：稳定倒计时（tick 数） */
static int g_collectOnly;         /* 只读采集：不建图/不建蹲点/不建守区/不建任何 UI 对象 */
static int g_exportForce;         /* Ctrl+E 手动导出时绕过“已采过/太小”的过滤 */
static int g_nmVert, g_nmTri;     /* 本次导出的 NavMeshGraph 顶点/三角形数 */
static char g_nmFile[128];        /* 导航网格二进制文件名 */
static unsigned long long nm_seenFp;  /* 已落盘的导航网格指纹 */
static int nm_seen;
static int g_cArea, g_cPos, g_cCrouch, g_cSpawn, g_cJump, g_cTag, g_cGuard;
static int g_helpOn = 1;

static void hud_refresh(void);
static P comp_tr(P comp);
/* 路点体检（实现在 probe.c，本文件末尾 #include） */
static void probe_tick(void);
static void probe_draw(void);
static void probe_reset(void);

/* --- geometry batch ----------------------------------------------------- */
static V3 g_bV[MB_MAXV];
static int g_bI[MB_MAXI];
static int g_bNV, g_bNI;

static void bs_reset(void) { g_bNV = 0; g_bNI = 0; }

static int bs_v(V3 p) {
  if (g_bNV >= MB_MAXV) return -1;
  g_bV[g_bNV] = p;
  return g_bNV++;
}

static void bs_tri(int a, int b, int c) {
  if (a < 0 || b < 0 || c < 0) return;
  if (g_bNI + 3 > MB_MAXI) return;
  g_bI[g_bNI++] = a; g_bI[g_bNI++] = b; g_bI[g_bNI++] = c;
}

/* double sided quad: winding does not matter, always visible */
static void bs_face(V3 a, V3 b, V3 c, V3 d) {
  int i = bs_v(a), j = bs_v(b), k = bs_v(c), l = bs_v(d);
  bs_tri(i, j, k); bs_tri(i, k, l);
  bs_tri(i, k, j); bs_tri(i, l, k);
}

static void bs_solid(V3 c, V3 h) {
  V3 a = { c.x - h.x, c.y - h.y, c.z - h.z };
  V3 b = { c.x + h.x, c.y - h.y, c.z - h.z };
  V3 d = { c.x + h.x, c.y + h.y, c.z - h.z };
  V3 e = { c.x - h.x, c.y + h.y, c.z - h.z };
  V3 f = { c.x - h.x, c.y - h.y, c.z + h.z };
  V3 g = { c.x + h.x, c.y - h.y, c.z + h.z };
  V3 i2 = { c.x + h.x, c.y + h.y, c.z + h.z };
  V3 j2 = { c.x - h.x, c.y + h.y, c.z + h.z };
  bs_face(a, b, d, e);
  bs_face(f, g, i2, j2);
  bs_face(a, f, j2, e);
  bs_face(b, g, i2, d);
  bs_face(a, b, g, f);
  bs_face(e, d, i2, j2);
}

static void bs_line(V3 a, V3 b, float w) {
  V3 d, u, v, ua, va;
  float len, h, ul, vl;
  d.x = b.x - a.x; d.y = b.y - a.y; d.z = b.z - a.z;
  len = sqrtf(d.x * d.x + d.y * d.y + d.z * d.z);
  if (len < 0.0005f) return;
  h = w * 0.5f;
  if (fabsf(d.y) < 0.9f * len) { u.x = 0.0f; u.y = -d.z; u.z = d.y; }
  else { u.x = -d.z; u.y = 0.0f; u.z = d.x; }
  ul = sqrtf(u.x * u.x + u.y * u.y + u.z * u.z);
  /* 水平且沿 X 的边 (dy==dz==0) 在第一个分支里得到 (0,0,0)：必须回退到
   * 另一个轴的构造，否则所有「纯 X 方向」的边会被静默丢掉（路点图看起来
   * 只剩一排排平行的横线）。 */
  if (ul < 1e-6f) {
    u.x = -d.z; u.y = 0.0f; u.z = d.x;
    ul = sqrtf(u.x * u.x + u.y * u.y + u.z * u.z);
    if (ul < 1e-6f) return;
  }
  u.x /= ul; u.y /= ul; u.z /= ul;
  v.x = d.y * u.z - d.z * u.y;
  v.y = d.z * u.x - d.x * u.z;
  v.z = d.x * u.y - d.y * u.x;
  vl = sqrtf(v.x * v.x + v.y * v.y + v.z * v.z);
  if (vl < 1e-6f) return;
  v.x /= vl; v.y /= vl; v.z /= vl;
  ua.x = u.x * h; ua.y = u.y * h; ua.z = u.z * h;
  va.x = v.x * h; va.y = v.y * h; va.z = v.z * h;
  {
    V3 p1 = { a.x - ua.x, a.y - ua.y, a.z - ua.z };
    V3 p2 = { a.x + ua.x, a.y + ua.y, a.z + ua.z };
    V3 p3 = { b.x + ua.x, b.y + ua.y, b.z + ua.z };
    V3 p4 = { b.x - ua.x, b.y - ua.y, b.z - ua.z };
    bs_face(p1, p2, p3, p4);
  }
  {
    V3 p1 = { a.x - va.x, a.y - va.y, a.z - va.z };
    V3 p2 = { a.x + va.x, a.y + va.y, a.z + va.z };
    V3 p3 = { b.x + va.x, b.y + va.y, b.z + va.z };
    V3 p4 = { b.x - va.x, b.y - va.y, b.z - va.z };
    bs_face(p1, p2, p3, p4);
  }
}

static void bs_wbox(V3 c, V3 h, float w) {
  int i;
  V3 p[8];
  static const int eg[12][2] = {
    {0,1},{1,2},{2,3},{3,0},{4,5},{5,6},{6,7},{7,4},{0,4},{1,5},{2,6},{3,7}
  };
  p[0].x = c.x - h.x; p[0].y = c.y - h.y; p[0].z = c.z - h.z;
  p[1].x = c.x + h.x; p[1].y = c.y - h.y; p[1].z = c.z - h.z;
  p[2].x = c.x + h.x; p[2].y = c.y + h.y; p[2].z = c.z - h.z;
  p[3].x = c.x - h.x; p[3].y = c.y + h.y; p[3].z = c.z - h.z;
  p[4].x = c.x - h.x; p[4].y = c.y - h.y; p[4].z = c.z + h.z;
  p[5].x = c.x + h.x; p[5].y = c.y - h.y; p[5].z = c.z + h.z;
  p[6].x = c.x + h.x; p[6].y = c.y + h.y; p[6].z = c.z + h.z;
  p[7].x = c.x - h.x; p[7].y = c.y + h.y; p[7].z = c.z + h.z;
  for (i = 0; i < 12; i++) bs_line(p[eg[i][0]], p[eg[i][1]], w);
}

/* --- one batched mesh per colour ---------------------------------------- */
static int vis_flush_mesh(const char* name, int slot, int items) {
  P go, mf, mr, mesh, av, ai, mat;
  if (g_bNI == 0) return 1;
  if (!g_meshCls || !g_mfType || !g_mrType || !g_vec3Cls || !g_i32Cls || !x_array_new) {
    if (!g_visNoMesh) {
      elog("vis: mesh classes missing (mesh=%p mf=%p mr=%p vec3=%p i32=%p arr=%p)",
           g_meshCls, g_mfType, g_mrType, g_vec3Cls, g_i32Cls, (void*)x_array_new);
      g_visNoMesh = 1;
    }
    return 0;
  }
  go = new_go(name);
  if (!go) return 0;
  ((set_layer_t)RVA(R_SETLAYER))(go, 0, 0);
  mf = ((addcomp_t)RVA(R_ADDCOMP))(go, g_mfType, 0);
  mr = ((addcomp_t)RVA(R_ADDCOMP))(go, g_mrType, 0);
  if (!mf || !mr) { elog("vis: MeshFilter/MeshRenderer add failed"); return 0; }
  mesh = x_object_new(g_meshCls);
  if (!mesh) return 0;
  ((mesh_ctor_t)RVA(R_MESH_CTOR))(mesh, 0);
  av = x_array_new(g_vec3Cls, (unsigned)g_bNV);
  ai = x_array_new(g_i32Cls, (unsigned)g_bNI);
  if (!av || !ai) { elog("vis: array alloc failed"); return 0; }
  memcpy((char*)av + 0x10, g_bV, (size_t)g_bNV * 12);
  memcpy((char*)ai + 0x10, g_bI, (size_t)g_bNI * 4);
  ((mesh_arr_t)RVA(R_MESH_VERTS))(mesh, av, 0);
  ((mesh_arr_t)RVA(R_MESH_TRIS))(mesh, ai, 0);
  ((mesh_1_t)RVA(R_MESH_BOUNDS))(mesh, 0);
  ((mf_setmesh_t)RVA(R_MF_SETMESH))(mf, mesh, 0);
  mat = mat_for(slot);
  if (mat) ((set_shmat_t)RVA(R_REND_SETSM))(mr, mat, 0);
  ((set_int1_t)RVA(R_REND_SHADOW))(mr, 0, 0);
  if (g_visObjN < 80) g_visObj[g_visObjN++] = go;
  elog("vis: mesh '%s' slot=%d items=%d verts=%d tris=%d", name, slot, items, g_bNV, g_bNI / 3);
  return 1;
}

static void draw_vf(int kind, int slot, int wire, float sx, float sy, float sz) {
  int i, c = 0;
  V3 h;
  h.x = sx; h.y = sy; h.z = sz;
  bs_reset();
  for (i = 0; i < g_vfN; i++) {
    if (g_vf[i].kind != kind) continue;
    if (wire) bs_wbox(g_vf[i].p, h, 0.05f);
    else bs_solid(g_vf[i].p, h);
    c++;
  }
  if (c) vis_flush_mesh("vis_layer", slot, c);
}

/* --- labels (lazy UGUI Text, moved from the main-thread tick) ----------- */
static int vis_canvas_init(void) {
  P go, comp;
  if (g_lblCanvas) return 1;
  if (!g_textType || !g_canvasType || !g_guiFont) return 0;
  go = new_go("UCF_VIS_LABELS");
  if (!go) return 0;
  comp = ((addcomp_t)RVA(R_ADDCOMP))(go, g_canvasType, 0);
  if (!comp) return 0;
  ((set_int1_t)RVA(R_CANVAS_MODE))(comp, 0, 0);          /* ScreenSpaceOverlay */
  ((set_int1_t)RVA(R_CANVAS_SORT))(comp, 31000, 0);
  g_lblCanvas = go;
  g_lblTr = get_tr(go);
  return 1;
}

static P vis_label_make(int i, const COL* c) {
  P go, comp, tr;
  V2 amin = { 0.0f, 0.0f }, amax = { 0.0f, 0.0f }, piv = { 0.5f, 0.5f };
  V2 ap = { -9999.0f, -9999.0f }, sz = { 300.0f, 26.0f };
  if (!vis_canvas_init()) return 0;
  go = new_go("UCF_VLBL");
  if (!go) return 0;
  comp = ((addcomp_t)RVA(R_ADDCOMP))(go, g_textType, 0);
  if (!comp) return 0;
  tr = get_tr(go);
  if (g_lblTr && tr) ((set_parent_t)RVA(R_SET_PARENT))(tr, g_lblTr, 0, 0);
  ((set_v2_t)RVA(R_RT_AMIN))(tr, amin, 0);
  ((set_v2_t)RVA(R_RT_AMAX))(tr, amax, 0);
  ((set_v2_t)RVA(R_RT_PIVOT))(tr, piv, 0);
  ((set_v2_t)RVA(R_RT_APOS))(tr, ap, 0);
  ((set_v2_t)RVA(R_RT_SDELTA))(tr, sz, 0);
  ((set_font_t)RVA(R_TEXT_SETFONT))(comp, g_guiFont, 0);
  ((set_int1_t)RVA(R_TEXT_SETSIZE))(comp, 12, 0);
  ((set_int1_t)RVA(R_TEXT_ALIGN))(comp, 4, 0);           /* MiddleCenter */
  ((set_int1_t)RVA(R_TEXT_HOVER))(comp, 1, 0);
  ((set_int1_t)RVA(R_TEXT_VOVER))(comp, 1, 0);
  ((set_int1_t)RVA(R_GRAPHIC_RAY))(comp, 0, 0);
  ((set_col_t)RVA(R_GRAPHIC_COL))(comp, *c, 0);
  (void)i;
  return comp;
}

static const COL* label_col(int kind) {
  switch (kind) {
    case K_NAREA:  return &COL_POS;
    case K_NPOS:   return &COL_CYAN;
    case K_CROUCH: return &COL_CROUCH;
    case K_GUARD:  return &COL_NODE1;
    case K_GAREA:  return &COL_PURPLE;
    case K_SPAWN:  return &COL_GOLD;
    case K_JUMP:   return &COL_JUMP;
    case K_TAG:    return &COL_NODE1;
    default:       return &COL_WHITE;
  }
}

static void vis_label_build(int i) {
  char buf[160];
  P comp;
  VF* f = &g_vf[i];
  if (f->kind == K_NPOS) sprintf(buf, "%s#%d\n%.1f,%.1f,%.1f\nsafe=%d", f->name, i, f->p.x, f->p.y, f->p.z, f->aux);
  else if (f->kind == K_TAG) sprintf(buf, "%s#%d\n%.1f,%.1f,%.1f\ntag=%d", f->name, i, f->p.x, f->p.y, f->p.z, f->aux);
  else sprintf(buf, "%s#%d\n%.1f,%.1f,%.1f", f->name, i, f->p.x, f->p.y, f->p.z);
  comp = vis_label_make(i, label_col(f->kind));
  if (!comp) return;
  ((set_txt_t)RVA(R_TEXT_SETTEXT))(comp, x_string_new(buf), 0);
  g_lblComp[i] = comp;
  g_lblHidden[i] = 1;
}

static void vis_label_hide(int i) {
  V2 v = { -9999.0f, -9999.0f };
  P tr;
  if (!g_lblComp[i] || g_lblHidden[i]) return;
  tr = comp_tr(g_lblComp[i]);
  if (!tr) return;
  ((set_v2_t)RVA(R_RT_APOS))(tr, v, 0);
  g_lblHidden[i] = 1;
}

static void vis_label_tick(void) {
  P cam, ctr;
  V3 cp;
  int i, shown = 0;
  if (!g_visOn || g_lblMode == 0 || !g_vfN) return;
  cam = ((cam_main_t)RVA(R_CAM_MAIN))(0);
  if (!uobj_live(cam)) return;
  ctr = get_tr(((get_go_t)RVA(R_GETGO))(cam, 0));
  if (!ctr) return;
  ((get_pos_t)RVA(R_GET_POS_INJ))(ctr, &cp, 0);
  for (i = 0; i < g_vfN; i++) {
    float dx = g_vf[i].p.x - cp.x, dy = g_vf[i].p.y - cp.y, dz = g_vf[i].p.z - cp.z;
    float d2 = dx * dx + dy * dy + dz * dz;
    float rng = (g_lblMode == 1) ? 35.0f : 400.0f;
    V3 wp, sp;
    if (d2 > rng * rng) { vis_label_hide(i); continue; }
    if (!g_lblComp[i]) {
      vis_label_build(i);
      if (!g_lblComp[i]) continue;
    }
    wp = g_vf[i].p;
    wp.y += 0.6f;
    sp = ((w2s2_t)RVA(R_W2S))(cam, wp, 0);
    if (sp.z <= 0.1f || sp.x < -200.0f || sp.y < -100.0f || sp.x > 6000.0f || sp.y > 4000.0f) {
      vis_label_hide(i);
      continue;
    }
    {
      V2 v;
      P tr = comp_tr(g_lblComp[i]);
      if (!tr) continue;
      v.x = sp.x; v.y = sp.y;
      ((set_v2_t)RVA(R_RT_APOS))(tr, v, 0);
    }
    g_lblHidden[i] = 0;
    shown++;
  }
  g_lblShown = shown;
}

/* --- readers ------------------------------------------------------------ */
static P static_obj(P cls, const char* field) {
  P f, v = 0;
  if (!cls || !x_class_get_field_from_name) return 0;
  f = x_class_get_field_from_name(cls, field);
  if (!f) return 0;
  x_field_static_get_value(f, &v);
  return v;
}
static int list_n(P l) { return l ? *(int*)((char*)l + 0x0C) : 0; }
static P list_items(P l) { return l ? *(P*)((char*)l + 0x08) : 0; }
/* A destroyed UnityEngine.Object keeps its managed wrapper but clears
 * m_CachedPtr (+0x8).  Calling GetComponent/GetPosition on it raises a
 * managed MissingReferenceException.  There is no managed catch here, so
 * IL2CPP calls abort() -> the "Microsoft Visual C++ Runtime Library"
 * dialog.  This happens right after a scene change, when SpareAreaList /
 * SpareList_BL/GR still hold components from the previous level. */
static P comp_tr(P comp) {
  if (!uobj_live(comp)) return 0;
  return ((get_tr_t)RVA(R_COMP_TR))(comp, 0);
}
static int comp_pos(P comp, V3* out) {
  P tr = comp_tr(comp);
  if (!tr) return 0;
  ((get_pos_t)RVA(R_GET_POS_INJ))(tr, out, 0);
  return 1;
}

static int vf_add(V3 p, int kind, int aux, const char* name) {
  VF* f;
  if (g_vfN >= VIS_MAXF) return -1;
  f = &g_vf[g_vfN];
  f->p = p;
  f->kind = kind;
  f->aux = aux;
  strncpy(f->name, name, sizeof(f->name) - 1);
  f->name[sizeof(f->name) - 1] = 0;
  return g_vfN++;
}

static char g_miss[256];
static void miss(const char* what) {
  if (strstr(g_miss, what)) return;
  if (strlen(g_miss) + strlen(what) + 2 < sizeof(g_miss)) {
    strcat(g_miss, what);
    strcat(g_miss, " ");
  }
}

typedef struct { P k[8192]; int v[8192]; } PMAP;
static PMAP g_pm;
static unsigned pm_hash(P k) { return ((unsigned)(UINT_PTR)k >> 4) & 8191u; }
static void pm_reset(void) { memset(&g_pm, 0, sizeof(g_pm)); }
static void pm_put(P k, int v) {
  unsigned h = pm_hash(k);
  while (g_pm.k[h]) { if (g_pm.k[h] == k) return; h = (h + 1) & 8191u; }
  g_pm.k[h] = k; g_pm.v[h] = v;
}
static int pm_get(P k) {
  unsigned h = pm_hash(k);
  while (g_pm.k[h]) { if (g_pm.k[h] == k) return g_pm.v[h]; h = (h + 1) & 8191u; }
  return -1;
}

static void read_nav(void) {
  P pg, arr;
  int n, i;
  if (!(g_lay & LAY_A)) return;
  pg = navfix_point_graph();
  if (!pg) { miss("pointgraph"); return; }
  n = *(int*)((char*)pg + 0xEC);
  arr = *(P*)((char*)pg + 0xE8);
  if (!arr || n <= 0) { miss("nodes0"); return; }
  if (n > VIS_MAXN) n = VIS_MAXN;
  pm_reset();
  memset(g_vn, 0, sizeof(VN) * (size_t)(n > 0 ? n : 1));
  for (i = 0; i < n; i++) {
    P nd = *(P*)((char*)arr + 0x10 + i * 4);
    unsigned fl;
    if (!nd) continue;
    fl = *(unsigned*)((char*)nd + 0x0C);
    g_vn[i].p.x = *(int*)((char*)nd + 0x14) * 0.001f;
    g_vn[i].p.y = *(int*)((char*)nd + 0x18) * 0.001f;
    g_vn[i].p.z = *(int*)((char*)nd + 0x1C) * 0.001f;
    g_vn[i].tag = (int)((fl >> 19) & 0x1F);
    g_vn[i].walk = (int)(fl & 1u);
    g_vn[i].pen = *(unsigned*)((char*)nd + 0x10);
    pm_put(nd, i);
  }
  g_vnN = n;
  for (i = 0; i < n && g_veN < VIS_MAXE; i++) {
    P nd = *(P*)((char*)arr + 0x10 + i * 4);
    P cons;
    int cn, j;
    if (!nd) continue;
    cons = *(P*)((char*)nd + 0x20);
    if (!cons) continue;
    cn = *(int*)((char*)cons + 0x0C);
    for (j = 0; j < cn && g_veN < VIS_MAXE; j++) {
      P other = *(P*)((char*)cons + 0x10 + j * 12);
      int oi = pm_get(other);
      if (oi > i) {
        g_ve[g_veN].a = i;
        g_ve[g_veN].b = oi;
        g_veN++;
      }
    }
  }
}

static void read_nano(void) {
  P l, items, aptr[VIS_MAXF];
  V3 apos[VIS_MAXF];
  int n, an = 0, i;
  if (!(g_lay & LAY_C) || !g_areaCls) return;
  l = static_obj(g_areaCls, "SpareAreaList");
  if (!l) { miss("SpareAreaList"); return; }
  n = list_n(l);
  items = list_items(l);
  if (n > 400) n = 400;
  for (i = 0; i < n; i++) {
    P a = *(P*)((char*)items + 0x10 + i * 4);
    V3 p;
    if (!a) continue;
    if (!comp_pos(a, &p)) continue;
    apos[an] = p;
    aptr[an] = a;
    an++;
  }
  for (i = 0; i < an; i++) {
    P a = aptr[i];
    V3 p = apos[i];
    int j;
    vf_add(p, K_NAREA, i, "幽灵守区");
    g_cArea++;
    {
      P pl = *(P*)((char*)a + 0x10);
      int pn = pl ? list_n(pl) : 0;
      P pit = pl ? list_items(pl) : 0;
      if (!pit) pn = 0;
      for (j = 0; j < pn && j < 20; j++) {
        P gp = *(P*)((char*)pit + 0x10 + j * 4);
        V3 q;
        if (!gp) continue;
        if (!comp_pos(gp, &q)) continue;
        vf_add(q, K_NPOS, *(int*)((char*)gp + 0x1C), "幽灵守点");
        g_cPos++;
      }
    }
    {
      P arr = *(P*)((char*)a + 0x0C);            /* entrancePos */
      int en = arr ? *(int*)((char*)arr + 0x0C) : 0;
      for (j = 0; j < en && j < 8 && g_eN < VIS_NBMAX; j++) {
        g_eA[g_eN] = p;
        g_eB[g_eN] = *(V3*)((char*)arr + 0x10 + j * 12);
        g_eN++;
      }
    }
    {
      P arr = *(P*)((char*)a + 0x1C);            /* escapePos */
      int en = arr ? *(int*)((char*)arr + 0x0C) : 0;
      for (j = 0; j < en && j < 8 && g_eN < VIS_NBMAX; j++) {
        g_eA[g_eN] = p;
        g_eB[g_eN] = *(V3*)((char*)arr + 0x10 + j * 12);
        g_eN++;
      }
    }
    {
      P arr = *(P*)((char*)a + 0x14);            /* neighborAreas */
      int nn = arr ? *(int*)((char*)arr + 0x0C) : 0;
      for (j = 0; j < nn && j < 6 && g_nN < VIS_NBMAX; j++) {
        P nb = *(P*)((char*)arr + 0x10 + j * 4);
        int k;
        for (k = 0; k < an; k++) if (aptr[k] == nb) break;
        if (k < an) {
          g_nA[g_nN] = p;
          g_nB[g_nN] = apos[k];
          g_nN++;
        }
      }
    }
    {
      P arr = *(P*)((char*)a + 0x18);            /* escapeAreas */
      int nn = arr ? *(int*)((char*)arr + 0x0C) : 0;
      for (j = 0; j < nn && j < 4 && g_eN < VIS_NBMAX; j++) {
        P nb = *(P*)((char*)arr + 0x10 + j * 4);
        int k;
        for (k = 0; k < an; k++) if (aptr[k] == nb) break;
        if (k < an) {
          g_eA[g_eN] = p;
          g_eB[g_eN] = apos[k];
          g_eN++;
        }
      }
    }
  }
}

static void read_crouch(void) {
  static const char* fld[2] = { "SpareList_BL", "SpareList_GR" };
  static const char* nm[2] = { "蹲守点BL", "蹲守点GR" };
  int k;
  if (!(g_lay & LAY_B) || !g_crouchCls) return;
  for (k = 0; k < 2; k++) {
    P l = static_obj(g_crouchCls, fld[k]);
    int n = list_n(l), i;
    P items = l ? list_items(l) : 0;
    if (!l) { miss(k ? "SpareList_GR" : "SpareList_BL"); continue; }
    if (!items) continue;
    if (n > 600) n = 600;
    for (i = 0; i < n; i++) {
      P c = *(P*)((char*)items + 0x10 + i * 4);
      V3 p;
      if (!c) continue;
      if (!comp_pos(c, &p)) continue;
      vf_add(p, K_CROUCH, k, nm[k]);
      g_cCrouch++;
    }
  }
}

static void read_typed(P type, P cls, int kind, const char* nm, int skip_crouch) {
  P arr;
  int n, i;
  if (!type) return;
  arr = ((find_objs_t)RVA(R_FINDOBJS))(type, 1, 0);
  if (!arr) return;
  n = *(int*)((char*)arr + 0x0C);
  if (n > 600) n = 600;
  for (i = 0; i < n; i++) {
    P c = *(P*)((char*)arr + 0x10 + i * 4);
    V3 p;
    if (!c) continue;
    if (skip_crouch && g_crouchCls && *(P*)c == g_crouchCls) continue;
    if (!comp_pos(c, &p)) continue;
    vf_add(p, kind, i, nm);
    if (kind == K_GUARD) g_cGuard++;
  }
  (void)cls;
}

static void read_guardareas(void) {
  if (!(g_lay & LAY_B)) return;
  read_typed(g_gareaType, g_gareaCls, K_GAREA, "守卫区域", 0);
}

static void read_spawns(void) {
  static const char* nm[6] = { "保卫者出生", "幽灵出生", "中立点", "补给箱", "红箱", "蓝箱" };
  static const int off[6] = { 0x10, 0x14, 0x18, 0x1C, 0x20, 0x24 };
  P mm = 0;
  int k;
  if (!(g_lay & LAY_D)) return;
  if (g_mmInstField) x_field_static_get_value(g_mmInstField, &mm);
  if (!uobj_live(mm)) { miss("MapManager"); return; }
  for (k = 0; k < 6; k++) {
    P arr = *(P*)((char*)mm + off[k]);
    int n, i;
    if (!arr) { miss(nm[k]); continue; }
    n = *(int*)((char*)arr + 0x0C);
    if (n > 200) n = 200;
    for (i = 0; i < n; i++) {
      V3 p = *(V3*)((char*)arr + 0x10 + i * 16);
      vf_add(p, K_SPAWN, k, nm[k]);
      g_cSpawn++;
    }
  }
}

static void read_jump(void) {
  P arr;
  int n, i;
  if (!(g_lay & LAY_A) || !g_jumpType) return;
  arr = ((find_objs_t)RVA(R_FINDOBJS))(g_jumpType, 1, 0);
  if (!arr) return;
  n = *(int*)((char*)arr + 0x0C);
  if (n > 200) n = 200;
  for (i = 0; i < n; i++) {
    P c = *(P*)((char*)arr + 0x10 + i * 4);
    P links;
    V3 p;
    int ln, j;
    if (!c) continue;
    if (!comp_pos(c, &p)) continue;
    vf_add(p, K_JUMP, i, "跳跃链接");
    g_cJump++;
    links = *(P*)((char*)c + 0x24);
    ln = links ? *(int*)((char*)links + 0x0C) : 0;
    for (j = 0; j < ln && j < 8 && g_jN < 512; j++) {
      P endTr = *(P*)((char*)links + 0x10 + j * 28);
      V3 ep;
      if (!uobj_live(endTr)) continue;
      ((get_pos_t)RVA(R_GET_POS_INJ))(endTr, &ep, 0);
      g_jA[g_jN] = p;
      g_jB[g_jN] = ep;
      g_jN++;
    }
  }
}

static void read_tags(void) {
  P arr;
  int n, i;
  if (!(g_lay & LAY_A) || !g_tagType) return;
  arr = ((find_objs_t)RVA(R_FINDOBJS))(g_tagType, 1, 0);
  if (!arr) return;
  n = *(int*)((char*)arr + 0x0C);
  if (n > 200) n = 200;
  for (i = 0; i < n; i++) {
    P c = *(P*)((char*)arr + 0x10 + i * 4);
    P pts;
    int pn, j;
    unsigned tag;
    if (!c) continue;
    pts = *(P*)((char*)c + 0x20);
    tag = *(unsigned*)((char*)c + 0x24);
    pn = pts ? *(int*)((char*)pts + 0x0C) : 0;
    for (j = 0; j < pn && j < 64 && g_tpN < 512; j++) {
      g_tp[g_tpN] = *(V3*)((char*)pts + 0x10 + j * 12);
      if (j == 0) vf_add(g_tp[g_tpN], K_TAG, (int)tag, "标签区");
      g_tpN++;
    }
    g_cTag++;
  }
}

/* --- build / show ------------------------------------------------------- */
static void vis_draw(void) {
  int i, g;
  /* create every layer material before the big vertex/index arrays exist, so a
   * GC during those allocations cannot invalidate a material we still need */
  for (i = 1; i <= 14; i++) if (!g_matSlot[i]) mat_for(i);
  if (g_lay & LAY_A) {
    for (g = 0; g < 3; g++) {
      int c = 0;
      bs_reset();
      for (i = 0; i < g_vnN; i++) {
        V3 h;
        int grp = !g_vn[i].walk ? 2 : (g_vn[i].tag ? 1 : 0);
        if (grp != g) continue;
        h.x = 0.14f; h.y = 0.14f; h.z = 0.14f;
        bs_solid(g_vn[i].p, h);
        c++;
      }
      if (c) vis_flush_mesh(g == 0 ? "vis_nodes" : (g == 1 ? "vis_nodes_tag" : "vis_nodes_blk"),
                            g == 0 ? 5 : (g == 1 ? 7 : 1), c);
    }
    bs_reset();
    for (i = 0; i < g_veN; i++) bs_line(g_vn[g_ve[i].a].p, g_vn[g_ve[i].b].p, 0.05f);
    vis_flush_mesh("vis_edges", 10, g_veN);
    if (g_jN) {
      bs_reset();
      for (i = 0; i < g_jN; i++) bs_line(g_jA[i], g_jB[i], 0.10f);
      vis_flush_mesh("vis_jump", 4, g_jN);
    }
    if (g_tpN) {
      bs_reset();
      for (i = 0; i < g_tpN; i++) {
        V3 h;
        h.x = 0.45f; h.y = 0.45f; h.z = 0.45f;
        bs_wbox(g_tp[i], h, 0.06f);
      }
      vis_flush_mesh("vis_tags", 7, g_tpN);
    }
  }
  if (g_lay & LAY_B) {
    draw_vf(K_CROUCH, 1, 0, 0.18f, 0.24f, 0.18f);
    draw_vf(K_GUARD, 7, 0, 0.26f, 0.32f, 0.26f);
    draw_vf(K_GAREA, 8, 1, 1.8f, 1.3f, 1.8f);
  }
  if (g_lay & LAY_C) {
    draw_vf(K_NAREA, 2, 1, 2.4f, 1.7f, 2.4f);
    draw_vf(K_NPOS, 6, 0, 0.16f, 0.26f, 0.16f);
    if (g_eN) {
      bs_reset();
      for (i = 0; i < g_eN; i++) bs_line(g_eA[i], g_eB[i], 0.05f);
      vis_flush_mesh("vis_entr", 9, g_eN);
    }
    if (g_nN) {
      bs_reset();
      for (i = 0; i < g_nN; i++) bs_line(g_nA[i], g_nB[i], 0.06f);
      vis_flush_mesh("vis_nb", 7, g_nN);
    }
  }
  if (g_lay & LAY_D) {
    int k;
    for (k = 0; k < 6; k++) {
      int c = 0, slot = 13;
      if (k == 0) slot = 11;
      else if (k == 1) slot = 12;
      else if (k == 2) slot = 13;
      else if (k == 3) slot = 14;
      else if (k == 4) slot = 9;
      else if (k == 5) slot = 6;
      bs_reset();
      for (i = 0; i < g_vfN; i++) {
        V3 h;
        if (g_vf[i].kind != K_SPAWN || g_vf[i].aux != k) continue;
        h.x = 0.30f; h.y = 0.90f; h.z = 0.30f;
        bs_solid(g_vf[i].p, h);
        c++;
      }
      if (c) vis_flush_mesh("vis_spawn", slot, c);
    }
  }
}

static void vis_show(int on) {
  int i;
  for (i = 0; i < g_visObjN; i++) if (g_visObj[i]) ((set_active_t)RVA(R_SETACTIVE))(g_visObj[i], (unsigned char)on, 0);
  if (g_lblCanvas) ((set_active_t)RVA(R_SETACTIVE))(g_lblCanvas, (unsigned char)on, 0);
}

static void vis_clear(void) {
  int i;
  for (i = 0; i < g_vfN; i++) {
    if (g_lblComp[i]) {
      if (uobj_live(g_lblComp[i])) {
        P go = ((get_go_t)RVA(R_GETGO))(g_lblComp[i], 0);
        if (uobj_live(go)) ((destroy_t)RVA(R_DESTROY))(go, 0);
      }
      g_lblComp[i] = 0;
      g_lblHidden[i] = 0;
    }
  }
  for (i = 0; i < g_visObjN; i++) if (g_visObj[i]) ((destroy_t)RVA(R_DESTROY))(g_visObj[i], 0);
  g_visObjN = 0;
  g_vnN = g_veN = g_vfN = 0;
  g_nN = g_eN = g_jN = g_tpN = 0;
  g_lblShown = 0;
}

static void vis_rebuild(void) {
  vis_clear();
  g_cArea = g_cPos = g_cCrouch = g_cSpawn = g_cJump = g_cTag = g_cGuard = 0;
  g_miss[0] = 0;
  read_nav();
  read_nano();
  read_crouch();
  read_guardareas();
  read_typed(g_guardType, g_guardCls, K_GUARD, "守卫点", 1);
  read_spawns();
  read_jump();
  read_tags();
  vis_draw();
  probe_draw();
  vis_show(1);
  elog("vis: nodes=%d edges=%d labels=%d (area=%d pos=%d crouch=%d guard=%d spawn=%d jump=%d tag=%d) missing=[%s]",
       g_vnN, g_veN, g_vfN, g_cArea, g_cPos, g_cCrouch, g_cGuard, g_cSpawn, g_cJump, g_cTag, g_miss);
  hud_refresh();
}

/* the scene changed: the old overlay objects were destroyed with the level */
static void vis_scene_reset(void) {
  g_visObjN = 0;
  g_lblCanvas = 0;
  g_lblTr = 0;
  g_lblShown = 0;
  g_vnN = g_veN = g_vfN = 0;
  g_nN = g_eN = g_jN = g_tpN = 0;
  g_miss[0] = 0;
  g_visDirty = g_visOn;
}

static void vis_toggle(void) {
  g_visOn = !g_visOn;
  if (g_visOn) { g_visDirty = 0; vis_rebuild(); }
  else vis_show(0);
  elog("vis %s (layers=0x%X labels=%d)", g_visOn ? "ON" : "OFF", g_lay, g_vfN);
  hud_refresh();
}

static void vis_toggle_layer(int bit) {
  g_lay ^= bit;
  if (g_visOn) { g_visDirty = 0; vis_rebuild(); }
  elog("vis layers=0x%X (toggled 0x%X)", g_lay, bit);
  hud_refresh();
}

/* --- export v2: stable ids + map fingerprint -----------------------------
 * Every node gets a 64-bit id hashed from its quantised (1 cm) position, so
 * the ids survive a re-scan that renumbers the PointGraph nodes.  The hash is
 * taken over the *printed* %.2f value, which is exactly what the viewer sees,
 * so the viewer can recompute an id for any coordinate. */
#define R_OBJ_GETNAME 0x4EA1B0

static unsigned long long fnv_u32(unsigned long long h, unsigned int v) {
  int i;
  for (i = 0; i < 4; i++) {
    h ^= (unsigned char)((v >> (i * 8)) & 0xFFu);
    h *= 1099511628211ULL;
  }
  return h;
}

static int qcm(float v) {
  char b[32];
  sprintf(b, "%.2f", v);
  return (int)floorf((float)atof(b) * 100.0f + 0.5f);
}

static unsigned long long pt_hash(const V3* p, unsigned int seed) {
  unsigned long long h = 14695981039346656037ULL;
  h = fnv_u32(h, seed);
  h = fnv_u32(h, (unsigned int)qcm(p->x));
  h = fnv_u32(h, (unsigned int)qcm(p->y));
  h = fnv_u32(h, (unsigned int)qcm(p->z));
  return h;
}

static void id_of(const V3* p, unsigned int seed, char* out) {
  sprintf(out, "%016llx", pt_hash(p, seed));
}

static const char* kind_name(int k) {
  switch (k) {
  case K_NAREA:  return "nano_area";
  case K_NPOS:   return "nano_pos";
  case K_CROUCH: return "crouch";
  case K_GUARD:  return "guard";
  case K_GAREA:  return "guard_area";
  case K_SPAWN:  return "spawn";
  case K_JUMP:   return "jump";
  case K_TAG:    return "tag_region";
  default:       return "unknown";
  }
}

static P mapmanager_instance(void) {
  P mm = 0;
  if (g_mmInstField) x_field_static_get_value(g_mmInstField, &mm);
  return mm;
}

/* the minimap Texture2D usually carries the map's asset name */
static void map_name_from_minimap(char* out, int cap) {
  P mm = mapmanager_instance();
  P tex;
  char* nm;
  int i, j = 0;
  out[0] = 0;
  if (!mm) return;
  tex = *(P*)((char*)mm + 0x3C);
  if (!tex) return;
  nm = ((get_name_t)RVA(R_OBJ_GETNAME))(tex, 0);
  if (!nm) return;
  for (i = 0; nm[i] && j < cap - 1; i++) {
    char c = nm[i];
    if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') ||
        c == '_' || c == '-') out[j++] = c;
    else if (j && out[j - 1] != '_') out[j++] = '_';
  }
  out[j] = 0;
}

/* 只读采集：只把游戏里的数据读进内存，不创建任何 GameObject/材质/UI。
 * 采集模式下走这条路径，避免在“进图闪退”的地图上雪上加霜。 */
static void collect_read(void) {
  g_cArea = g_cPos = g_cCrouch = g_cSpawn = g_cJump = g_cTag = g_cGuard = 0;
  g_miss[0] = 0;
  g_vnN = g_veN = g_vfN = 0;
  g_nN = g_eN = g_jN = 0;
  read_nav();
  read_nano();
  read_crouch();
  read_guardareas();
  read_typed(g_guardType, g_guardCls, K_GUARD, "守卫点", 1);
  read_spawns();
  read_jump();
  read_tags();
}

/* ---- NavMeshGraph 导出（A* 烘焙出来的人机可走面）----------------------
 * NavmeshBase{tileXCount 0xC8, tileZCount 0xCC, tiles 0xD0, transform 0xE8}
 *   transform 是 A* 的 GraphTransform 类，不是 Unity 的 Transform：
 *   GraphTransform{identity 0x8, onlyTranslational 0x9, isXY 0xA, isXZ 0xB,
 *                  matrix 0xC (Matrix4x4), inverseMatrix 0x4C,
 *                  up 0x8C, translation 0x98, i3translation 0xA4}
 * NavmeshTile{tris 0x8, verts 0xC, vertsInGraphSpace 0x10}
 *   verts 已经是世界坐标（Int3，1/1000 m），vertsInGraphSpace 是图空间。
 * 二进制 UCFNM3：
 *   "UCFNM3\0" | int32 nv | int32 nt | int32 ntile | uint8 id,ot,xy,xz
 *   | float matrix[16] | float translation[3]
 *   | int32 verts[nv*3] | int32 gverts[nv*3] | int32 tris[nt*3]
 * 两张顶点表都写：万一 verts 不是世界坐标，离线还能用 matrix 自己算。 */
#define NM_MAGIC "UCFNM3"

static int nm_dump(const char* path, int* out_nv, int* out_nt) {
  extern P navfix_navmesh_graph(void);
  P g, tiles, gt;
  int ntile, i, j, nv = 0, nt = 0, vbase = 0, wbase = 0, ok = 1;
  int *vb = 0, *tb = 0, *gb = 0;
  float m[16], t[3];
  unsigned char fl[4];
  FILE* f;
  *out_nv = *out_nt = 0;
  g = navfix_navmesh_graph();
  if (!g) return 0;
  tiles = *(P*)((char*)g + 0xD0);
  ntile = tiles ? *(int*)((char*)tiles + 0xC) : 0;
  if (ntile <= 0 || ntile > 4096) return 0;
  for (i = 0; i < ntile; i++) {
    P tl = *(P*)((char*)tiles + 0x10 + i * 4);
    P tr, vr;
    if (!tl) continue;
    tr = *(P*)((char*)tl + 0x8);
    vr = *(P*)((char*)tl + 0xC);
    nv += vr ? *(int*)((char*)vr + 0xC) : 0;
    nt += tr ? *(int*)((char*)tr + 0xC) : 0;
  }
  if (nv <= 0 || nt <= 0 || nv > 3000000 || nt > 3000000) return 0;

  vb = (int*)malloc((size_t)nv * 3 * sizeof(int));
  gb = (int*)malloc((size_t)nv * 3 * sizeof(int));
  tb = (int*)malloc((size_t)nt * 3 * sizeof(int));
  if (!vb || !gb || !tb) { free(vb); free(gb); free(tb); return 0; }
  for (i = 0; i < nv * 3; i++) { vb[i] = 0; gb[i] = 0; }

  for (i = 0; i < ntile && ok; i++) {
    P tl = *(P*)((char*)tiles + 0x10 + i * 4);
    P tr, vr, vg;
    int tv, tt;
    if (!tl) continue;
    tr = *(P*)((char*)tl + 0x8);
    vr = *(P*)((char*)tl + 0xC);
    vg = *(P*)((char*)tl + 0x10);
    tv = vr ? *(int*)((char*)vr + 0xC) : 0;
    tt = tr ? *(int*)((char*)tr + 0xC) : 0;
    if (tv > 0) {
      if (vbase + tv > nv) { ok = 0; break; }
      memcpy(vb + vbase * 3, (char*)vr + 0x10, (size_t)tv * 12);
      if (vg && *(int*)((char*)vg + 0xC) == tv)
        memcpy(gb + vbase * 3, (char*)vg + 0x10, (size_t)tv * 12);
      else
        memcpy(gb + vbase * 3, (char*)vr + 0x10, (size_t)tv * 12);
    }
    for (j = 0; j < tt; j++) {
      int vi = *(int*)((char*)tr + 0x10 + j * 4);
      if (ntile > 1) vi &= 0xFFF;               /* 多 tile 时高位是 tile 索引 */
      if (wbase + j >= nt * 3) { ok = 0; break; }
      tb[wbase + j] = vi + vbase;
    }
    vbase += tv;
    wbase += tt;
  }
  if (!ok) { free(vb); free(gb); free(tb); return 0; }

  /* GraphTransform：直接读内存，不调 il2cpp */
  gt = *(P*)((char*)g + 0xE8);
  for (i = 0; i < 4; i++) fl[i] = 0;
  for (i = 0; i < 16; i++) m[i] = (i % 5) ? 0.0f : 1.0f;
  t[0] = t[1] = t[2] = 0.0f;
  if (gt) {
    fl[0] = *(unsigned char*)((char*)gt + 0x8);
    fl[1] = *(unsigned char*)((char*)gt + 0x9);
    fl[2] = *(unsigned char*)((char*)gt + 0xA);
    fl[3] = *(unsigned char*)((char*)gt + 0xB);
    memcpy(m, (char*)gt + 0xC, 64);
    memcpy(t, (char*)gt + 0x98, 12);
  }

  f = fopen(path, "wb");
  if (!f) { free(vb); free(gb); free(tb); return 0; }
  fwrite(NM_MAGIC, 1, 7, f);
  fwrite(&nv, 4, 1, f);
  fwrite(&nt, 4, 1, f);
  fwrite(&ntile, 4, 1, f);
  fwrite(fl, 1, 4, f);
  fwrite(m, 4, 16, f);
  fwrite(t, 4, 3, f);
  fwrite(vb, 4, (size_t)nv * 3, f);
  fwrite(gb, 4, (size_t)nv * 3, f);
  fwrite(tb, 4, (size_t)nt * 3, f);
  fclose(f);
  free(vb); free(gb); free(tb);
  *out_nv = nv;
  *out_nt = nt;
  return 1;
}

static void vis_export(void) {
  char dir[MAX_PATH], path[MAX_PATH];
  char mapname[80], fname[80], fp[40], id1[24], id2[24], mark[MAX_PATH];
  FILE* f;
  SYSTEMTIME st;
  V3 lo, hi;
  unsigned long long xr = 0;
  int i, ok, src;
  extern int navfix_graph_ours(void);

  if (!g_visOn) {
    if (g_collectOnly) collect_read();
    else { vis_rebuild(); vis_show(0); }
  }
  GetLocalTime(&st);
  sprintf(dir, "%s\\vis", g_dir);
  CreateDirectoryA(dir, 0);

  map_name_from_minimap(mapname, sizeof(mapname));
  lo.x = lo.y = lo.z = 1e9f;
  hi.x = hi.y = hi.z = -1e9f;
  for (i = 0; i < g_vnN; i++) {
    V3 p = g_vn[i].p;
    xr ^= pt_hash(&p, 0);
    if (p.x < lo.x) lo.x = p.x;
    if (p.y < lo.y) lo.y = p.y;
    if (p.z < lo.z) lo.z = p.z;
    if (p.x > hi.x) hi.x = p.x;
    if (p.y > hi.y) hi.y = p.y;
    if (p.z > hi.z) hi.z = p.z;
  }
  if (!g_vnN) { lo.x = lo.y = lo.z = hi.x = hi.y = hi.z = 0.0f; }
  sprintf(fp, "n%d-%016llx", g_vnN, xr);
  src = navfix_graph_ours();

  /* 同一张图只导一次：指纹相同说明节点位置完全一致 */
  sprintf(mark, "%s\\vis\\_seen_%s", g_dir, fp);
  if (!g_exportForce) {
    FILE* mf = fopen(mark, "r");
    if (mf) { fclose(mf); elog("vis: fp=%s already collected, skip duplicate", fp); return; }
  }

  if (mapname[0]) strcpy(fname, mapname);
  else sprintf(fname, "map_%s", fp);   /* 小地图没名字时用指纹命名，免得一堆 unnamed 互相覆盖 */

  sprintf(path, "%s\\%s_%04d%02d%02d_%02d%02d%02d.json",
          dir, fname,
          st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond);
  /* 顺带把 A* 烘焙的 NavMeshGraph（真正的人机可走面）导成二进制 */
  {
    char nmp[MAX_PATH];
    const char* base;
    strcpy(nmp, path);
    { char* e = strrchr(nmp, '.'); if (e) strcpy(e, ".navmesh.bin"); }
    g_nmVert = g_nmTri = 0;
    g_nmFile[0] = 0;
    if (nm_dump(nmp, &g_nmVert, &g_nmTri)) {
      base = strrchr(nmp, '\\');
      strncpy(g_nmFile, base ? base + 1 : nmp, sizeof(g_nmFile) - 1);
      elog("vis: navmesh verts=%d tris=%d -> %s", g_nmVert, g_nmTri, nmp);
    }
  }

  f = fopen(path, "w");
  if (!f) { elog("vis: export failed %s", path); return; }

  fprintf(f, "{\n");
  fprintf(f, "  \"format\": \"ucf-navgraph\",\n");
  fprintf(f, "  \"version\": 1,\n");
  fprintf(f, "  \"generated\": \"%04d-%02d-%02d %02d:%02d:%02d\",\n",
          st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond);
  fprintf(f, "  \"plugin\": \"ucf_mod 2026-11-15\",\n");
  fprintf(f, "  \"map\": {\n");
  fprintf(f, "    \"name\": \"%s\",\n", mapname);
  fprintf(f, "    \"fingerprint\": \"%s\",\n", fp);
  fprintf(f, "    \"source\": \"%s\",\n", src ? "ours" : "game");
  fprintf(f, "    \"node_count\": %d,\n", g_vnN);
  fprintf(f, "    \"bbox\": [[%.2f,%.2f,%.2f],[%.2f,%.2f,%.2f]]", lo.x, lo.y, lo.z, hi.x, hi.y, hi.z);
  if (g_nmVert) fprintf(f, ",\n    \"navmesh\": {\"file\": \"%s\", \"verts\": %d, \"tris\": %d}", g_nmFile, g_nmVert, g_nmTri);
  fprintf(f, "\n");
  fprintf(f, "  },\n");
  fprintf(f, "  \"counts\": {\"nodes\": %d, \"edges\": %d, \"features\": %d, \"nano_area\": %d, "
             "\"nano_pos\": %d, \"crouch\": %d, \"guard\": %d, \"spawn\": %d, \"jump\": %d, \"tag\": %d},\n",
          g_vnN, g_veN, g_vfN, g_cArea, g_cPos, g_cCrouch, g_cGuard, g_cSpawn, g_cJump, g_cTag);
  fprintf(f, "  \"nodes\": [\n");
  for (i = 0; i < g_vnN; i++) {
    id_of(&g_vn[i].p, 0, id1);
    fprintf(f, "    {\"id\":\"%s\",\"p\":[%.2f,%.2f,%.2f],\"tag\":%d,\"walk\":%d,\"pen\":%u}%s\n",
            id1, g_vn[i].p.x, g_vn[i].p.y, g_vn[i].p.z,
            g_vn[i].tag, g_vn[i].walk, g_vn[i].pen, (i + 1 < g_vnN) ? "," : "");
  }
  fprintf(f, "  ],\n  \"edges\": [\n");
  for (i = 0; i < g_veN; i++) {
    id_of(&g_vn[g_ve[i].a].p, 0, id1);
    id_of(&g_vn[g_ve[i].b].p, 0, id2);
    fprintf(f, "    [\"%s\",\"%s\"]%s\n", id1, id2, (i + 1 < g_veN) ? "," : "");
  }
  fprintf(f, "  ],\n  \"features\": [\n");
  for (i = 0; i < g_vfN; i++) {
    id_of(&g_vf[i].p, (unsigned int)(g_vf[i].kind * 100 + g_vf[i].aux), id1);
    fprintf(f, "    {\"id\":\"%s\",\"kind\":\"%s\",\"name\":\"%s\",\"aux\":%d,\"p\":[%.2f,%.2f,%.2f]}%s\n",
            id1, kind_name(g_vf[i].kind), g_vf[i].name, g_vf[i].aux,
            g_vf[i].p.x, g_vf[i].p.y, g_vf[i].p.z, (i + 1 < g_vfN) ? "," : "");
  }
  fprintf(f, "  ],\n  \"lines\": {\n    \"nano_neighbor\": [");
  for (i = 0; i < g_nN; i++)
    fprintf(f, "%s[[%.2f,%.2f,%.2f],[%.2f,%.2f,%.2f]]", i ? "," : "",
            g_nA[i].x, g_nA[i].y, g_nA[i].z, g_nB[i].x, g_nB[i].y, g_nB[i].z);
  fprintf(f, "\n    ],\n    \"entrance_escape\": [");
  for (i = 0; i < g_eN; i++)
    fprintf(f, "%s[[%.2f,%.2f,%.2f],[%.2f,%.2f,%.2f]]", i ? "," : "",
            g_eA[i].x, g_eA[i].y, g_eA[i].z, g_eB[i].x, g_eB[i].y, g_eB[i].z);
  fprintf(f, "\n    ],\n    \"jump\": [");
  for (i = 0; i < g_jN; i++)
    fprintf(f, "%s[[%.2f,%.2f,%.2f],[%.2f,%.2f,%.2f]]", i ? "," : "",
            g_jA[i].x, g_jA[i].y, g_jA[i].z, g_jB[i].x, g_jB[i].y, g_jB[i].z);
  fprintf(f, "\n    ]\n  }\n}\n");
  fclose(f);
  ok = 1;
  { FILE* mf = fopen(mark, "w"); if (mf) { fprintf(mf, "%s\n", path); fclose(mf); } }
  elog("vis: exported nodes=%d edges=%d features=%d map='%s' fp=%s src=%s -> %s",
       g_vnN, g_veN, g_vfN, mapname, fp, src ? "ours" : "game", path);
  (void)ok;
  if (g_cjk && !g_collectOnly) hud_refresh();
}

/* ---- on-screen mode hint ------------------------------------------------ */
static P mk_text_ui(P canvasTr, const char* name, float ax, float ay, float px, float py,
                    float x, float y, float w, float h, int fs) {
  P go, comp, tr;
  V2 v;
  go = new_go(name);
  if (!go) return 0;
  comp = ((addcomp_t)RVA(R_ADDCOMP))(go, g_textType, 0);
  if (!comp) return 0;
  tr = get_tr(go);
  if (canvasTr && tr) ((set_parent_t)RVA(R_SET_PARENT))(tr, canvasTr, 0, 0);
  v.x = ax; v.y = ay; ((set_v2_t)RVA(R_RT_AMIN))(tr, v, 0);
  v.x = ax; v.y = ay; ((set_v2_t)RVA(R_RT_AMAX))(tr, v, 0);
  v.x = px; v.y = py; ((set_v2_t)RVA(R_RT_PIVOT))(tr, v, 0);
  v.x = x;  v.y = y;  ((set_v2_t)RVA(R_RT_APOS))(tr, v, 0);
  v.x = w;  v.y = h;  ((set_v2_t)RVA(R_RT_SDELTA))(tr, v, 0);
  ((set_font_t)RVA(R_TEXT_SETFONT))(comp, g_guiFont, 0);
  ((set_int1_t)RVA(R_TEXT_SETSIZE))(comp, fs, 0);
  ((set_int1_t)RVA(R_TEXT_ALIGN))(comp, 0, 0);
  ((set_int1_t)RVA(R_TEXT_HOVER))(comp, 1, 0);
  ((set_int1_t)RVA(R_TEXT_VOVER))(comp, 1, 0);
  ((set_int1_t)RVA(R_GRAPHIC_RAY))(comp, 0, 0);
  ((set_col_t)RVA(R_GRAPHIC_COL))(comp, COL_WHITE, 0);
  return comp;
}

static int hud_init(void) {
  P canvasGo, canvasTr, txtGo, tr, comp;
  V2 v;
  if (g_hud) return 1;
  if (!g_textType || !g_canvasType) { elog("hud: UGUI Text/Canvas class missing"); return 0; }

  if (!g_guiFont && g_textType) {
    P any = ((find_obj_t)RVA(R_FINDOBJ))(g_textType, 1, 0);
    if (any) {
      g_guiFont = ((get_font_t)RVA(R_TEXT_GETFONT))(any, 0);
      if (g_guiFont) g_cjk = 1;
    }
  }
  if (!g_guiFont && g_fontType) {
    P p1 = x_string_new("Arial.ttf"), p2 = x_string_new("LegacyRuntime.ttf");
    g_guiFont = ((builtin_t)RVA(R_RES_BUILTIN))(g_fontType, p1, 0);
    if (!g_guiFont) g_guiFont = ((builtin_t)RVA(R_RES_BUILTIN))(g_fontType, p2, 0);
  }
  if (!g_guiFont) { elog("hud: no usable font"); return 0; }

  canvasGo = new_go("UCF_HUD");
  if (!canvasGo) { elog("hud: canvas go failed"); return 0; }
  comp = ((addcomp_t)RVA(R_ADDCOMP))(canvasGo, g_canvasType, 0);
  if (!comp) { elog("hud: Canvas AddComponent failed"); return 0; }
  ((set_int1_t)RVA(R_CANVAS_MODE))(comp, 0, 0);            /* ScreenSpaceOverlay */
  ((set_int1_t)RVA(R_CANVAS_SORT))(comp, 32000, 0);
  canvasTr = get_tr(canvasGo);

  txtGo = new_go("UCF_HUD_Text");
  if (!txtGo) { elog("hud: text go failed"); return 0; }
  comp = ((addcomp_t)RVA(R_ADDCOMP))(txtGo, g_textType, 0);
  if (!comp) { elog("hud: Text AddComponent failed"); return 0; }
  tr = get_tr(txtGo);
  if (canvasTr && tr) ((set_parent_t)RVA(R_SET_PARENT))(tr, canvasTr, 0, 0);

  v.x = 0.0f; v.y = 1.0f;
  ((set_v2_t)RVA(R_RT_AMIN))(tr, v, 0);
  ((set_v2_t)RVA(R_RT_AMAX))(tr, v, 0);      /* top-left anchored */
  v.x = 0.0f; v.y = 1.0f;
  ((set_v2_t)RVA(R_RT_PIVOT))(tr, v, 0);
  v.x = 14.0f; v.y = -10.0f;
  ((set_v2_t)RVA(R_RT_APOS))(tr, v, 0);
  v.x = 720.0f; v.y = 110.0f;
  ((set_v2_t)RVA(R_RT_SDELTA))(tr, v, 0);

  ((set_font_t)RVA(R_TEXT_SETFONT))(comp, g_guiFont, 0);
  ((set_int1_t)RVA(R_TEXT_SETSIZE))(comp, 20, 0);
  ((set_int1_t)RVA(R_TEXT_ALIGN))(comp, 0, 0);    /* UpperLeft  */
  ((set_int1_t)RVA(R_TEXT_HOVER))(comp, 1, 0);    /* Overflow   */
  ((set_int1_t)RVA(R_TEXT_VOVER))(comp, 1, 0);
  ((set_int1_t)RVA(R_GRAPHIC_RAY))(comp, 0, 0);   /* no raycast */
  ((set_col_t)RVA(R_GRAPHIC_COL))(comp, COL_WHITE, 0);

  g_hud = comp;
  g_hudGo = txtGo;
  g_keys = mk_text_ui(canvasTr, "UCF_HUD_Keys", 0.0f, 1.0f, 0.0f, 1.0f, 14.0f, -130.0f, 1180.0f, 96.0f, 14);
  if (g_keys) elog("hud: keys go=%p font=%p", g_keysGo, ((get_font_t)RVA(R_TEXT_GETFONT))(g_keys, 0));
  g_keysGo = g_keys ? ((get_go_t)RVA(R_GETGO))(g_keys, 0) : 0;
  elog("hud: ready font=%p (%s) keys=%p", g_guiFont, g_cjk ? "game/CJK" : "builtin/ASCII", g_keys);
  return 1;
}

static void hud_refresh(void) {
  char s[1500];
  char miss[200];
  int c1 = 0, c2 = 0, c3 = 0, i;
  if (!g_hud && !hud_init()) return;
  for (i = 0; i < g_n; i++) {
    if (g_mk[i].type == 1) c1++;
    else if (g_mk[i].type == 2) c2++;
    else if (g_mk[i].type == 3) c3++;
  }
  if (g_miss[0]) sprintf(miss, "   缺:%s", g_miss);
  else miss[0] = 0;
  if (g_cjk) {
    sprintf(s,
      "可视化 %s   A路点:%s B人类:%s C幽灵:%s D出生:%s E模式:%s   标签:%s\n"
      "节点 %d  连接 %d  守区 %d  守点 %d  蹲守 %d  守卫 %d  出生 %d  跳链 %d  标签区 %d%s\n"
      "编辑 %s   已放标记 %d (蹲%d/守%d/区%d)   屏上标签 %d/%d%s",
      g_visOn ? "开" : "关",
      (g_lay & LAY_A) ? "开" : "关", (g_lay & LAY_B) ? "开" : "关",
      (g_lay & LAY_C) ? "开" : "关", (g_lay & LAY_D) ? "开" : "关",
      (g_lay & LAY_E) ? "开" : "关",
      g_lblMode == 0 ? "关" : (g_lblMode == 1 ? "近距" : "全部"),
      g_vnN, g_veN, g_cArea, g_cPos, g_cCrouch, g_cGuard, g_cSpawn, g_cJump, g_cTag, miss,
      g_on ? "开" : "关", g_n, c1, c2, c3, g_lblShown, g_vfN,
      g_visOn && g_visDirty ? "  [待重建]" : "");
  } else {
    sprintf(s,
      "VIS %s | A %s B %s C %s D %s E %s | labels %s\n"
      "nodes %d edges %d nano %d/%d crouch %d guard %d spawn %d jump %d tag %d%s\n"
      "edit %s markers %d (c %d/p %d/a %d) on-screen labels %d/%d",
      g_visOn ? "ON" : "OFF",
      (g_lay & LAY_A) ? "on" : "off", (g_lay & LAY_B) ? "on" : "off",
      (g_lay & LAY_C) ? "on" : "off", (g_lay & LAY_D) ? "on" : "off",
      (g_lay & LAY_E) ? "on" : "off",
      g_lblMode == 0 ? "off" : (g_lblMode == 1 ? "near" : "all"),
      g_vnN, g_veN, g_cArea, g_cPos, g_cCrouch, g_cGuard, g_cSpawn, g_cJump, g_cTag, miss,
      g_on ? "ON" : "OFF", g_n, c1, c2, c3, g_lblShown, g_vfN);
  }
  ((set_txt_t)RVA(R_TEXT_SETTEXT))(g_hud, x_string_new(s), 0);
  if (g_keys) {
    if (g_helpOn) {
      const char* k = "Ctrl+V 可视化总开关   Ctrl+Shift+1..5  A路点/B人类/C幽灵/D出生/E模式   Ctrl+Shift+L 文字标签 关/近距/全部\n"
                      "Ctrl+E 导出数据   Ctrl+H 本面板开关   Delete 删除准星最近标记   Ctrl+0 显示/隐藏已放标记\n"
                      "Ctrl+1 编辑模式  Ctrl+2 蹲守点  Ctrl+4 幽灵守区  Ctrl+5 撤销  Ctrl+6 保存  Ctrl+7 重载  Ctrl+8 阵营  Ctrl+9 状态\n"
                      "路点编辑: Ctrl+Shift+A 选A点  Ctrl+Shift+N 加点  Ctrl+Shift+J A↔点 连/断  Ctrl+Shift+D 禁用点  Ctrl+Shift+Z 撤销  Ctrl+Shift+R 重套用（改完自动存盘）";
      ((set_txt_t)RVA(R_TEXT_SETTEXT))(g_keys, x_string_new(k), 0);
    } else {
      ((set_txt_t)RVA(R_TEXT_SETTEXT))(g_keys, x_string_new("Ctrl+H 显示快捷键"), 0);
    }
  }
}

static void hud_reset(void) { g_hud = 0; g_hudGo = 0; g_keys = 0; g_keysGo = 0; g_lblCanvas = 0; g_lblTr = 0; }

/* ---- marker store ------------------------------------------------------- */
static int add_mk(int type, V3 p, int aid, int parent, int prm, P go, P comp, P vis) {
  MK* m;
  if (g_n >= MAXM) { elog("marker store full (%d)", MAXM); return 0; }
  m = &g_mk[g_n];
  m->type = type; m->p = p; m->aid = aid; m->parent = parent; m->prm = prm;
  m->go = go; m->comp = comp; m->vis = vis;
  g_n++;
  return 1;
}

static int make_crouch(V3 p) {
  P go, comp;
  go = new_go("UCF_CrouchPos");
  if (!go) return 0;
  ((set_active_t)RVA(R_SETACTIVE))(go, 0, 0);
  comp = ((addcomp_t)RVA(R_ADDCOMP))(go, g_crouchType, 0);
  if (!comp) { elog("crouch: AddComponent failed"); return 0; }
  *(int*)((char*)comp + 0x0C) = g_team;
  ((set_pos_t)RVA(R_SET_POS))(get_tr(go), p, 0);
  ((set_active_t)RVA(R_SETACTIVE))(go, 1, 0);
  if (!add_mk(1, p, -1, -1, g_team, go, comp, spawn_vis(p, 0.24f, 1))) return 0;
  elog("crouch #%d at %.2f %.2f %.2f team=%d", g_n, p.x, p.y, p.z, g_team);
  hud_refresh();
  return 1;
}

static int make_area(int scale10, V3 p) {
  P go, comp, box;
  V3 sc;
  int aid = g_areaCount;
  float s = scale10 / 10.0f;
  if (aid >= MAX_AID) { elog("area limit %d", MAX_AID); return 0; }
  if (s < 1.0f) s = 1.0f;
  go = new_go("UCF_GuardArea");
  if (!go) return 0;
  sc.x = s; sc.y = s; sc.z = s;
  ((set_scale_t)RVA(R_SET_SCALE))(get_tr(go), sc, 0);
  ((set_pos_t)RVA(R_SET_POS))(get_tr(go), p, 0);
  comp = ((addcomp_t)RVA(R_ADDCOMP))(go, g_areaType, 0);
  if (!comp) { elog("area: AddComponent failed"); return 0; }
  if (g_boxType) {
    box = ((addcomp_t)RVA(R_ADDCOMP))(go, g_boxType, 0);
    if (box) ((set_trigger_t)RVA(R_IS_TRIGGER))(box, 1, 0);
    else elog("area: BoxCollider add failed");
  }
  g_areaCount++;
  g_aidMk[aid] = (P)(g_n);
  if (!add_mk(3, p, aid, -1, scale10, go, comp, spawn_vis(p, 0.42f, 3))) return 0;
  g_curArea = g_n - 1;
  elog("area #%d (aid=%d scale=%.1f) at %.2f %.2f %.2f -> current", g_n - 1, aid, s, p.x, p.y, p.z);
  hud_refresh();
  return 1;
}

static int make_nanopos(int aid, V3 p, int safety) {
  P go, comp, areaGo, areaComp, areaTr, tr;
  int parent;
  if (aid < 0 || aid >= g_areaCount) { elog("nanopos: no area aid=%d", aid); return 0; }
  parent = (int)(INT_PTR)g_aidMk[aid];
  if (parent < 0 || parent >= g_n || g_mk[parent].type != 3) { elog("nanopos: bad parent aid=%d", aid); return 0; }
  areaGo = g_mk[parent].go;
  areaComp = g_mk[parent].comp;
  go = new_go("UCF_NanoGuardPos");
  if (!go) return 0;
  comp = ((addcomp_t)RVA(R_ADDCOMP))(go, g_posType, 0);
  if (!comp) { elog("nanopos: AddComponent failed"); return 0; }
  if (safety) *(int*)((char*)comp + 0x1C) = safety;
  areaTr = get_tr(areaGo);
  tr = get_tr(go);
  if (areaTr && tr) ((set_parent_t)RVA(R_SET_PARENT))(tr, areaTr, 0, 0);
  if (tr) ((set_pos_t)RVA(R_SET_POS))(tr, p, 0);
  ((pos_init_t)RVA(R_POS_INIT))(comp, areaComp, 0);
  if (!add_mk(2, p, aid, parent, safety, go, comp, spawn_vis(p, 0.32f, 2))) return 0;
  {
    P list = *(P*)((char*)areaComp + 0x10);
    int cnt = list ? *(int*)((char*)list + 0x0C) : -1;
    elog("nanopos #%d at %.2f %.2f %.2f aid=%d safety=%d areaPosList=%d", g_n, p.x, p.y, p.z, aid, safety, cnt);
  }
  hud_refresh();
  return 1;
}

/* delete marker at idx, its children, and fix every index reference */
static void del_index(int idx);

static void kill_children(int idx) {
  int i = 0;
  while (i < g_n) {
    if (g_mk[i].parent == idx) del_index(i);
    else i++;
  }
}

static void del_index(int idx) {
  MK* m;
  int i;
  if (idx < 0 || idx >= g_n) return;
  m = &g_mk[idx];
  kill_children(idx);
  if (m->vis) ((destroy_t)RVA(R_DESTROY))(m->vis, 0);
  if (m->go) ((destroy_t)RVA(R_DESTROY))(m->go, 0);
  if (m->type == 3) {
    if (m->aid >= 0 && m->aid < MAX_AID) g_aidMk[m->aid] = 0;
    if (g_areaCount > 0) g_areaCount--;
  }
  for (i = idx; i < g_n - 1; i++) g_mk[i] = g_mk[i + 1];
  g_n--;
  for (i = 0; i < g_n; i++) if (g_mk[i].parent > idx) g_mk[i].parent--;
  for (i = 0; i < MAX_AID; i++) {
    int v = (int)(INT_PTR)g_aidMk[i];
    if (v > idx) g_aidMk[i] = (P)(v - 1);
  }
  if (g_curArea == idx) g_curArea = -1;
  else if (g_curArea > idx) g_curArea--;
}

static void undo_last(void) {
  if (g_n <= 0) { elog("undo: nothing to undo"); return; }
  elog("undo: removing marker #%d type=%d", g_n - 1, g_mk[g_n - 1].type);
  del_index(g_n - 1);
  hud_refresh();
}

static void delete_nearest(void) {
  V3 cp, fw, hp;
  int i, byRay = -1, byHit = -1, target = -1;
  float bestPerp = 1e9f, bestHit = 1e9f, bestCam = 1e9f;
  int haveHit, byCam = -1;
  if (!g_n) { elog("delete: no markers"); return; }
  if (!cam_ray(&cp, &fw)) { elog("delete: no camera"); return; }
  haveHit = cam_point(&hp);
  for (i = 0; i < g_n; i++) {
    float vx = g_mk[i].p.x - cp.x, vy = g_mk[i].p.y - cp.y, vz = g_mk[i].p.z - cp.z;
    float t = vx * fw.x + vy * fw.y + vz * fw.z;
    if (t > 0.3f && t < 60.0f) {
      float px = vx - fw.x * t, py = vy - fw.y * t, pz = vz - fw.z * t;
      float perp = sqrtf(px * px + py * py + pz * pz);
      if (perp < bestPerp) { bestPerp = perp; byRay = i; }
    }
    if (haveHit) {
      float dx = g_mk[i].p.x - hp.x, dy = g_mk[i].p.y - hp.y, dz = g_mk[i].p.z - hp.z;
      float d2 = dx * dx + dy * dy + dz * dz;
      if (d2 < bestHit) { bestHit = d2; byHit = i; }
    }
    {
      float d2 = vx * vx + vy * vy + vz * vz;
      if (d2 < bestCam) { bestCam = d2; byCam = i; }
    }
  }
  if (byRay >= 0 && bestPerp <= 1.0f) {
    target = byRay;
    elog("delete: aimed at marker #%d (ray offset %.2f m)", byRay, bestPerp);
  } else if (byHit >= 0 && bestHit <= 144.0f) {
    target = byHit;
    elog("delete: nearest marker #%d to aim point (%.2f m)", byHit, sqrt(bestHit));
  } else if (byCam >= 0 && bestCam <= 16.0f) {
    target = byCam;
    elog("delete: closest marker #%d to camera (%.2f m)", byCam, sqrt(bestCam));
  } else {
    elog("delete: nothing chosen (ray %.2f m, aim %.2f m, cam %.2f m) - aim at a marker",
         byRay >= 0 ? bestPerp : -1.0f,
         haveHit ? sqrt(bestHit) : -1.0f,
         byCam >= 0 ? sqrt(bestCam) : -1.0f);
    return;
  }
  if (target >= 0) {
    elog("delete: removing #%d type=%d at %.2f %.2f %.2f", target, g_mk[target].type,
         g_mk[target].p.x, g_mk[target].p.y, g_mk[target].p.z);
    del_index(target);
    hud_refresh();
  }
}

static void toggle_visuals(void) {
  int i;
  g_vis = !g_vis;
  for (i = 0; i < g_n; i++) {
    P v = g_mk[i].vis;
    if (!v) continue;
    ((set_active_t)RVA(R_SETACTIVE))(v, (unsigned char)g_vis, 0);
  }
  elog("visuals %s (markers=%d)", g_vis ? "ON" : "OFF", g_n);
  hud_refresh();
}

static int save_file(void) {
  FILE* f;
  int i, c1 = 0, c2 = 0, c3 = 0;
  if (!g_file[0]) return 0;
  CreateDirectoryA(g_dir, 0);
  {
    char dir[MAX_PATH];
    strcpy(dir, g_file);
    { char* s = strrchr(dir, '\\'); if (s) *s = 0; }
    CreateDirectoryA(dir, 0);
  }
  f = fopen(g_file, "w");
  if (!f) { elog("save: cannot open %s", g_file); return 0; }
  for (i = 0; i < g_n; i++) {
    if (g_mk[i].type == 1) c1++;
    else if (g_mk[i].type == 2) c2++;
    else if (g_mk[i].type == 3) c3++;
  }
  fprintf(f, "# ucf_mod markers v1  crouch=%d nanopos=%d area=%d\n", c1, c2, c3);
  fprintf(f, "# crouch <team> <x> <y> <z>\n");
  fprintf(f, "# area <scale*10> <x> <y> <z>\n");
  fprintf(f, "# nanopos <areaId> <x> <y> <z> <safety>\n");
  for (i = 0; i < g_n; i++) {
    MK* m = &g_mk[i];
    if (m->type == 1) fprintf(f, "crouch %d %.3f %.3f %.3f\n", m->prm, m->p.x, m->p.y, m->p.z);
    else if (m->type == 3) fprintf(f, "area %d %.3f %.3f %.3f\n", m->prm, m->p.x, m->p.y, m->p.z);
    else if (m->type == 2) fprintf(f, "nanopos %d %.3f %.3f %.3f %d\n", m->aid, m->p.x, m->p.y, m->p.z, m->prm);
  }
  fclose(f);
  elog("saved %d markers (crouch=%d nanopos=%d area=%d) -> %s", g_n, c1, c2, c3, g_file);
  hud_refresh();
  return 1;
}

static void reset_markers(void) {
  g_n = 0;
  g_areaCount = 0;
  g_curArea = -1;
  memset(g_aidMk, 0, sizeof(g_aidMk));
}

static int load_file(void) {
  FILE* f;
  char line[256];
  int made = 0;
  if (!g_file[0]) return 0;
  f = fopen(g_file, "r");
  if (!f) { elog("load: no markers file yet (%s)", g_file); return 0; }
  while (fgets(line, sizeof(line), f)) {
    float x, y, z;
    int a, b;
    if (line[0] == '#' || line[0] == '\n' || line[0] == '\r') continue;
    if (sscanf(line, "area %d %f %f %f", &a, &x, &y, &z) == 4) {
      V3 p; p.x = x; p.y = y; p.z = z;
      if (make_area(a, p)) made++;
    } else if (sscanf(line, "nanopos %d %f %f %f %d", &a, &x, &y, &z, &b) == 5) {
      V3 p; p.x = x; p.y = y; p.z = z;
      if (make_nanopos(a, p, b)) made++;
    } else if (sscanf(line, "crouch %d %f %f %f", &a, &x, &y, &z) == 4) {
      V3 p; p.x = x; p.y = y; p.z = z;
      if (make_crouch(p)) made++;
    }
  }
  fclose(f);
  elog("loaded %d markers from %s", made, g_file);
  hud_refresh();
  return made;
}

static void status(void) {
  int c1 = 0, c2 = 0, c3 = 0, i;
  for (i = 0; i < g_n; i++) {
    if (g_mk[i].type == 1) c1++;
    else if (g_mk[i].type == 2) c2++;
    else if (g_mk[i].type == 3) c3++;
  }
  elog("status: edit=%d vis=%d team=%d markers=%d (crouch=%d nanopos=%d area=%d) curAreaAid=%d hud=%d",
       g_on, g_vis, g_team, g_n, c1, c2, c3,
       (g_curArea >= 0 && g_curArea < g_n) ? g_mk[g_curArea].aid : -1, g_hud ? 1 : 0);
  if (g_areaCls && x_class_get_field_from_name) {
    P f = x_class_get_field_from_name(g_areaCls, "SpareAreaList");
    if (f) {
      P l = 0;
      x_field_static_get_value(f, &l);
      elog("status: SpareAreaList=%d", l ? *(int*)((char*)l + 0x0C) : -1);
    }
  }
  if (g_crouchCls && x_class_get_field_from_name) {
    P f = x_class_get_field_from_name(g_crouchCls, "SpareList_BL");
    if (f) {
      P l = 0;
      x_field_static_get_value(f, &l);
      elog("status: SpareList_BL=%d", l ? *(int*)((char*)l + 0x0C) : -1);
    }
  }
  elog("status: file=%s", g_file);
}

/* how many crouch markers this editor created (so navfix can tell them apart
 * from the map's own points before deciding to bulk-inject its draft grid) */
int editor_crouch_made(void) {
  int i, c = 0;
  for (i = 0; i < g_n; i++) if (g_mk[i].type == 1) c++;
  return c;
}

void editor_on_scene(void* astar) {
  if (!astar) return;
  if (!ed_init()) return;
  if (astar == g_lastAstar) return;
  elog("scene: enter astar=%p inited=%d", astar, g_inited);
  g_lastAstar = (P)astar;
  reset_markers();
  elog("scene: markers reset");
  hud_reset();
  elog("scene: hud reset");
  vis_scene_reset();
  elog("scene: vis reset");
  g_aeNodes = -1;
  g_nedGraph = 0;
  g_nedApplied = 0;
  g_nedWaitN = -1;
  g_nedHasA = 0;
  g_nedN = 0;
  g_nedPath[0] = 0;
  probe_reset();
  nm_seen = 0;
  g_aeHold = 8;
  elog("scene changed (astar=%p) - loading markers", astar);
  if (g_collectOnly) {
    elog("collect-only: graph will be exported automatically, nothing is modified");
    return;
  }
  load_file();
  hud_refresh();
}

/* called by navfix after it rebuilds the point graph */
void editor_mark_dirty(void) {
  g_visDirty = 1;
}

/* 关掉"进图自动导出"（目前没有热键，留给后续配置用） */
void editor_set_auto_export(int on) { g_autoExport = on ? 1 : 0; }

/* 自动导出：当前场景的路点图只要有节点、且节点数稳定 ~2 s，就落一份 JSON。
 * 旧实现只在“我们自己重建过图”之后才导出，游戏自己建好的图永远导不出来。 */
static void auto_export_tick(void) {
  P pg = navfix_point_graph();
  int n = pg ? *(int*)((char*)pg + 0xEC) : -1;
  if (n > 0 && n == g_aeNodes) {
    if (g_aeHold > 0 && --g_aeHold == 0) {
      elog("auto-export: graph stable at %d nodes, writing JSON", n);
      vis_export();
    }
  } else {
    g_aeNodes = n;
    g_aeHold = 8;
  }
}

/* NavMeshGraph 自动落盘：和 PointGraph 无关。
 * 很多图的 PointGraph 是空的或只剩十来个残点，但每张图都有 A* 烘焙的可走面，
 * 人机真正在上面跑。场景里可走面的指纹一变就写一份 vis\navmesh_<fp>.bin。 */
static void nm_auto_tick(void) {
  extern P navfix_navmesh_graph(void);
  P g, tiles;
  int ntile, i, nv = 0, nt = 0;
  unsigned long long h = 1469598103934665603ULL;
  char fp[48], path[MAX_PATH];
  g = navfix_navmesh_graph();
  if (!g) { nm_seen = 0; return; }
  tiles = *(P*)((char*)g + 0xD0);
  ntile = tiles ? *(int*)((char*)tiles + 0xC) : 0;
  if (ntile <= 0 || ntile > 4096) return;
  for (i = 0; i < ntile; i++) {
    P tl = *(P*)((char*)tiles + 0x10 + i * 4);
    P tr, vr;
    if (!tl) continue;
    tr = *(P*)((char*)tl + 0x8);
    vr = *(P*)((char*)tl + 0xC);
    nv += vr ? *(int*)((char*)vr + 0xC) : 0;
    nt += tr ? *(int*)((char*)tr + 0xC) : 0;
  }
  if (nv <= 0 || nt <= 0 || nv > 3000000 || nt > 3000000) return;
  h ^= (unsigned long long)nv; h *= 1099511628211ULL;
  h ^= (unsigned long long)nt; h *= 1099511628211ULL;
  for (i = 0; i < ntile; i++) {
    P tl = *(P*)((char*)tiles + 0x10 + i * 4);
    P vr;
    int k, tv;
    if (!tl) continue;
    vr = *(P*)((char*)tl + 0xC);
    tv = vr ? *(int*)((char*)vr + 0xC) : 0;
    if (tv > 64) tv = 64;
    if (!vr) continue;
    for (k = 0; k < tv * 3; k++) { h ^= (unsigned long long)((int*)((char*)vr + 0x10))[k]; h *= 1099511628211ULL; }
  }
  if (nm_seen && h == nm_seenFp) return;
  nm_seenFp = h;
  nm_seen = 1;
  sprintf(fp, "nm%d-%016llx", nv, h);
  sprintf(path, "%s\\vis\\navmesh_%s.bin", g_dir, fp);
  if (nm_dump(path, &g_nmVert, &g_nmTri)) {
    elog("nm: verts=%d tris=%d tiles=%d -> %s", g_nmVert, g_nmTri, ntile, path);
    hud_refresh();
  }
}

/* 只读采集模式开关：写/删 collect.flag，重启后保持 */
static void set_collect_only(int on) {
  char p[MAX_PATH];
  extern void navfix_set_collect_only(int);
  g_collectOnly = on ? 1 : 0;
  navfix_set_collect_only(on);
  sprintf(p, "%s\\collect.flag", g_dir);
  if (on) { FILE* fh = fopen(p, "w"); if (fh) { fputs("1\n", fh); fclose(fh); } }
  else DeleteFileA(p);
  elog("collect-only %s -> %s", on ? "ON (只读采集)" : "OFF (可编辑)", on ? p : "(flag removed)");
  hud_refresh();
}

/* ============ 路点图手动编辑（游戏内） + 进图自动套用 ==================
 * 点图是运行期对象（AstarPath.active.graphs 里的 PointGraph），每次进图都会
 * 重建，所以这里三件事一起做：
 *   1) 编辑直接改活着的那张图 —— 立刻见效，人机马上能用新路线；
 *   2) 每次编辑自动写 ucf_mod\nav\<图指纹>.txt —— 一张图一个文件，互不干扰；
 *   3) 进图后等节点数稳定，自动把该图的编辑清单重新套用一遍。
 * 布局（x86，dump.cs）：PointGraph.nodes +0xE8 / nodeCount +0xEC；
 *   GraphNode: nodeIndex +0x8, flags +0xC, penalty +0x10, position +0x14；
 *   PointNode: connections +0x20, gameObject +0x24；
 *   Connection: node +0, cost +4, shapeEdge +8（步长 12）。
 * 删除节点不改数组（避免所有 nodeIndex 位移），只把它标记成不可走并断开所有边，
 * A* 的 GetNearest 用的是 NNConstraint.Default（constrainWalkability=1），
 * 不可走的节点不会被选中。
 */
#define R_PG_REBUILD   0x5F0370
#define NADD 1
#define NDEL 2
#define EADD 3
#define EDEL 4


static int nav_count(P g) { return g ? *(int*)((char*)g + 0xEC) : 0; }
static P nav_arr(P g) { return g ? *(P*)((char*)g + 0xE8) : 0; }
static P nav_node(P g, int i) {
  P arr = nav_arr(g);
  if (!arr || i < 0 || i >= nav_count(g)) return 0;
  return *(P*)((char*)arr + 0x10 + i * 4);
}
static void nav_pos(P nd, V3* p) {
  p->x = (float)*(int*)((char*)nd + 0x14) * 0.001f;
  p->y = (float)*(int*)((char*)nd + 0x18) * 0.001f;
  p->z = (float)*(int*)((char*)nd + 0x1C) * 0.001f;
}
static void nav_put_pos(P nd, const V3* p) {
  *(int*)((char*)nd + 0x14) = (int)(p->x * 1000.0f);
  *(int*)((char*)nd + 0x18) = (int)(p->y * 1000.0f);
  *(int*)((char*)nd + 0x1C) = (int)(p->z * 1000.0f);
}
static float nav_d2(const V3* a, const V3* b) {
  float dx = a->x - b->x, dy = a->y - b->y, dz = a->z - b->z;
  return dx * dx + dy * dy + dz * dz;
}
static int nav_walk(P nd) { return (int)(*(unsigned*)((char*)nd + 0x0C) & 1u); }
static void nav_set_walk(P nd, int on) {
  unsigned f = *(unsigned*)((char*)nd + 0x0C);
  *(unsigned*)((char*)nd + 0x0C) = on ? (f | 1u) : (f & ~1u);
}
/* 最近的可走节点；maxd<=0 表示不限距离 */
static int nav_find(P g, const V3* p, float maxd) {
  int i, best = -1;
  float bestd = (maxd > 0.0f) ? maxd * maxd : 1e18f;
  for (i = 0; i < nav_count(g); i++) {
    P nd = nav_node(g, i);
    V3 q;
    float d;
    if (!nd || !nav_walk(nd)) continue;
    nav_pos(nd, &q);
    d = nav_d2(p, &q);
    if (d < bestd) { bestd = d; best = i; }
  }
  return best;
}
static int nav_conn_has(P nd, P other);
static int nav_find_any(P g, const V3* p, float maxd) {
  int i, best = -1;
  float bestd = (maxd > 0.0f) ? maxd * maxd : 1e18f;
  for (i = 0; i < nav_count(g); i++) {
    P nd = nav_node(g, i);
    V3 q;
    float d;
    if (!nd) continue;
    nav_pos(nd, &q);
    d = nav_d2(p, &q);
    if (d < bestd) { bestd = d; best = i; }
  }
  return best;
}
/* 清单里的改动是否还在图上（用来判断图是不是被游戏重扫掉了） */
static int nav_needs_apply(P g) {
  int i, ia, ib, n;
  if (!g || !g_nedN) return 0;
  n = nav_count(g);
  if (n < g_nedBaseN) return 1;
  for (i = 0; i < g_nedN; i++) {
    NAVED* e = &g_ned[i];
    if (e->kind == NADD) {
      if (nav_find_any(g, &e->a, 0.35f) < 0) return 1;
    } else if (e->kind == NDEL) {
      ia = nav_find_any(g, &e->a, 0.35f);
      if (ia >= 0 && nav_walk(nav_node(g, ia))) return 1;
    } else {
      ia = nav_find_any(g, &e->a, 0.35f);
      ib = nav_find_any(g, &e->b, 0.35f);
      if (ia >= 0 && ib >= 0) {
        int has = nav_conn_has(nav_node(g, ia), nav_node(g, ib));
        if (e->kind == EADD && !has) return 1;
        if (e->kind == EDEL && has) return 1;
      }
    }
  }
  return 0;
}
static int nav_conn_has(P nd, P other) {
  P c = *(P*)((char*)nd + 0x20);
  int n = c ? *(int*)((char*)c + 0x0C) : 0, i;
  for (i = 0; i < n; i++)
    if (*(P*)((char*)c + 0x10 + i * 12) == other) return 1;
  return 0;
}
/* add=1 连边 / add=0 断边；返回 1 表示有改动 */
static int nav_conn_set(P nd, P other, int add) {
  P c = *(P*)((char*)nd + 0x20);
  if (!nd || !other || !g_connCls || !x_array_new) return 0;
  int n = c ? *(int*)((char*)c + 0x0C) : 0;
  int i, cnt = 0, hnd = 0;
  P nc;
  V3 pa, pb;
  unsigned cost;
  if (add) {
    if (nav_conn_has(nd, other)) return 0;
    nav_pos(nd, &pa); nav_pos(other, &pb);
    cost = (unsigned)(sqrtf(nav_d2(&pa, &pb)) * 1000.0f + 0.5f);
    if (cost < 1u) cost = 1u;
    nc = x_array_new(g_connCls, (unsigned)(n + 1));
    if (!nc) return 0;
    if (x_gchandle_new) hnd = (int)x_gchandle_new(nc, 0);
    if (n) memcpy((char*)nc + 0x10, (char*)c + 0x10, (size_t)n * 12);
    *(P*)((char*)nc + 0x10 + n * 12) = other;
    *(unsigned*)((char*)nc + 0x14 + n * 12) = cost;
    *(unsigned char*)((char*)nc + 0x18 + n * 12) = 0xFF;
  } else {
    if (!nav_conn_has(nd, other)) return 0;
    nc = x_array_new(g_connCls, (unsigned)(n - 1));
    if (!nc) return 0;
    if (x_gchandle_new) hnd = (int)x_gchandle_new(nc, 0);
    for (i = 0; i < n; i++) {
      P t = *(P*)((char*)c + 0x10 + i * 12);
      if (t == other) continue;
      *(P*)((char*)nc + 0x10 + cnt * 12) = t;
      *(unsigned*)((char*)nc + 0x14 + cnt * 12) = *(unsigned*)((char*)c + 0x14 + i * 12);
      *(unsigned char*)((char*)nc + 0x18 + cnt * 12) = *(unsigned char*)((char*)c + 0x18 + i * 12);
      cnt++;
    }
  }
  *(P*)((char*)nd + 0x20) = nc;
  if (hnd && x_gchandle_free) x_gchandle_free((P)hnd);
  return 1;
}
static int nav_conn_clear(P nd) {
  P nc;
  if (!nd || !g_connCls || !x_array_new) return 0;
  nc = x_array_new(g_connCls, 0);
  if (!nc) return 0;
  *(P*)((char*)nd + 0x20) = nc;
  return 1;
}
/* 新建一个 PointNode 并挂到 graph 末尾；返回新下标，失败 -1 */
static int nav_add_node(P g, const V3* p) {
  int n = nav_count(g), i, cap, hnd = 0, hcon = 0, ncap;
  P arr = nav_arr(g), nd, cons, tmpl = 0, na, hn = 0;
  unsigned flags;
  if (!g || !g_pnodeCls || !g_connCls || !x_array_new || !x_object_new) return -1;
  for (i = n - 1; i >= 0; i--) { P q = nav_node(g, i); if (q) { tmpl = q; break; } }
  if (!tmpl) return -1;
  nd = x_object_new(g_pnodeCls);
  if (!nd) return -1;
  if (x_gchandle_new) hnd = (int)x_gchandle_new(nd, 0);
  cons = x_array_new(g_connCls, 0);
  if (!cons) { if (hnd && x_gchandle_free) x_gchandle_free((P)hnd); return -1; }
  if (x_gchandle_new) hcon = (int)x_gchandle_new(cons, 0);
  flags = *(unsigned*)((char*)tmpl + 0x0C);
  flags = (flags & 0xFF000000u) | 1u;              /* 同一张图，walkable，tag=0 */
  *(int*)((char*)nd + 0x08) = n;                    /* nodeIndex */
  *(unsigned*)((char*)nd + 0x0C) = flags;
  *(unsigned*)((char*)nd + 0x10) = *(unsigned*)((char*)tmpl + 0x10);
  nav_put_pos(nd, p);
  *(P*)((char*)nd + 0x20) = cons;
  *(P*)((char*)nd + 0x24) = 0;
  cap = arr ? *(int*)((char*)arr + 0x0C) : 0;
  if (!arr || n >= cap) {
    ncap = (n + 4 > n * 2) ? n + 4 : n * 2;
    na = x_array_new(g_pnodeCls, (unsigned)ncap);
    if (!na) {
      if (hcon && x_gchandle_free) x_gchandle_free((P)hcon);
      if (hnd && x_gchandle_free) x_gchandle_free((P)hnd);
      return -1;
    }
    if (x_gchandle_new) hn = (P)x_gchandle_new(na, 0);
    if (arr && n) memcpy((char*)na + 0x10, (char*)arr + 0x10, (size_t)n * 4);
    *(P*)((char*)g + 0xE8) = na;
    arr = na;
    if (hn && x_gchandle_free) x_gchandle_free(hn);
  }
  *(P*)((char*)arr + 0x10 + n * 4) = nd;
  *(int*)((char*)g + 0xEC) = n + 1;
  if (hcon && x_gchandle_free) x_gchandle_free((P)hcon);
  if (hnd && x_gchandle_free) x_gchandle_free((P)hnd);
  return n;
}
static void nav_refresh(P g) {
  if (g && g_ga) ((void (*)(P))RVA(R_PG_REBUILD))(g);
  g_visDirty = 1;
}
/* 彻底断开一个节点（不可走 + 清连接 + 清别人的反向引用） */
static void nav_kill_node(P g, P nd) {
  int i, n = nav_count(g);
  nav_set_walk(nd, 0);
  nav_conn_clear(nd);
  for (i = 0; i < n; i++) {
    P q = nav_node(g, i);
    if (q && q != nd && nav_conn_has(q, nd)) nav_conn_set(q, nd, 0);
  }
}
static void nav_edge(P g, P a, P b, int on) {
  if (a && b && a != b) {
    nav_conn_set(a, b, on);
    nav_conn_set(b, a, on);
    nav_refresh(g);
  }
}
/* ---- 编辑清单的落盘/读取（每张图一个文件） ---- */
static void nav_fp(char* out, int cap) {
  P g = navfix_point_graph();
  unsigned long long xr = 0;
  int i, n = nav_count(g);
  for (i = 0; i < n; i++) {
    P nd = nav_node(g, i);
    V3 p;
    if (!nd) continue;
    nav_pos(nd, &p);
    xr ^= pt_hash(&p, 0);
  }
  sprintf(out, "n%d-%016llx", n, xr);
  (void)cap;
}
static void nav_save(void) {
  FILE* f;
  int i;
  if (!g_nedPath[0]) return;
  if (!g_nedN) { DeleteFileA(g_nedPath); return; }
  f = fopen(g_nedPath, "w");
  if (!f) { elog("naved: save failed %s", g_nedPath); return; }
  fprintf(f, "# ucf-navedit v1 fp=%s\n", g_nedFp);
  for (i = 0; i < g_nedN; i++) {
    NAVED* e = &g_ned[i];
    if (e->kind == NADD)
      fprintf(f, "node add %.3f %.3f %.3f\n", e->a.x, e->a.y, e->a.z);
    else if (e->kind == NDEL)
      fprintf(f, "node del %.3f %.3f %.3f\n", e->a.x, e->a.y, e->a.z);
    else
      fprintf(f, "edge %s %.3f %.3f %.3f %.3f %.3f %.3f\n",
              e->kind == EADD ? "add" : "del",
              e->a.x, e->a.y, e->a.z, e->b.x, e->b.y, e->b.z);
  }
  fclose(f);
  elog("naved: saved %d edits -> %s", g_nedN, g_nedPath);
}
static void nav_edit_load(const char* path) {
  FILE* f = fopen(path, "r");
  char line[256];
  g_nedN = 0;
  if (!f) return;
  while (fgets(line, sizeof(line), f)) {
    NAVED e;
    char k1[16], k2[16];
    float x, y, z, x2, y2, z2;
    if (line[0] == '#' || line[0] == '\n') continue;
    memset(&e, 0, sizeof(e));
    if (sscanf(line, "node %15s %f %f %f", k1, &x, &y, &z) == 4) {
      e.kind = (k1[0] == 'a') ? NADD : NDEL;
      e.a.x = x; e.a.y = y; e.a.z = z;
    } else if (sscanf(line, "edge %15s %f %f %f %f %f %f", k1, &x, &y, &z, &x2, &y2, &z2) == 7) {
      e.kind = (k1[0] == 'a') ? EADD : EDEL;
      e.a.x = x; e.a.y = y; e.a.z = z;
      e.b.x = x2; e.b.y = y2; e.b.z = z2;
    } else {
      continue;
    }
    if (g_nedN < NAV_ED_MAX) g_ned[g_nedN++] = e;
  }
  fclose(f);
  elog("naved: loaded %d edits from %s", g_nedN, path);
}
/* 把清单套到活图上；返回实际生效条数 */
static int nav_apply_all(P g) {
  int i, ok = 0, ia, ib;
  for (i = 0; i < g_nedN; i++) {
    NAVED* e = &g_ned[i];
    if (e->kind == NADD) {
      if (nav_find(g, &e->a, 0.35f) < 0 && nav_add_node(g, &e->a) >= 0) ok++;
    } else if (e->kind == NDEL) {
      ia = nav_find(g, &e->a, 0.35f);
      if (ia >= 0) { nav_kill_node(g, nav_node(g, ia)); ok++; }
    } else {
      ia = nav_find(g, &e->a, 0.35f);
      ib = nav_find(g, &e->b, 0.35f);
      if (ia >= 0 && ib >= 0) {
        nav_conn_set(nav_node(g, ia), nav_node(g, ib), e->kind == EADD);
        nav_conn_set(nav_node(g, ib), nav_node(g, ia), e->kind == EADD);
        ok++;
      }
    }
  }
  nav_refresh(g);
  return ok;
}
/* 撤销一条：反向操作 + 出栈 */
static void nav_undo(void) {
  P g = navfix_point_graph();
  NAVED* e;
  int ia, ib;
  if (!g || !g_nedN) { elog("naved: nothing to undo"); return; }
  e = &g_ned[g_nedN - 1];
  if (e->kind == NADD) {
    ia = nav_find(g, &e->a, 0.35f);
    if (ia >= 0) nav_kill_node(g, nav_node(g, ia));
  } else if (e->kind == NDEL) {
    ia = nav_find_any(g, &e->a, 0.35f);   /* 被删的点已不可走，用“任意节点”找回来 */
    if (ia >= 0) nav_set_walk(nav_node(g, ia), 1);
  } else {
    ia = nav_find(g, &e->a, 0.35f);
    ib = nav_find(g, &e->b, 0.35f);
    if (ia >= 0 && ib >= 0) {
      nav_conn_set(nav_node(g, ia), nav_node(g, ib), e->kind == EDEL);
      nav_conn_set(nav_node(g, ib), nav_node(g, ia), e->kind == EDEL);
    }
  }
  g_nedN--;
  nav_refresh(g);
  nav_save();
  elog("naved: undo -> %d edits left", g_nedN);
}
/* 记录一条编辑 + 自动保存 */
static void nav_push(int kind, const V3* a, const V3* b) {
  NAVED* e;
  if (g_nedN >= NAV_ED_MAX) { elog("naved: edit list full"); return; }
  e = &g_ned[g_nedN++];
  e->kind = kind;
  e->a = *a;
  if (b) e->b = *b; else memset(&e->b, 0, sizeof(e->b));
  nav_save();
}
/* ---- 交互：加点 / 删点 / 连断边 / 选 A ---- */
static int nav_pick(const V3* hint, float maxd) {
  P g = navfix_point_graph();
  return g ? nav_find(g, hint, maxd) : -1;
}
static void nav_sel_a(void) {
  P g = navfix_point_graph();
  V3 p;
  int i;
  if (!g) { elog("naved: no point graph"); return; }
  if (!cam_point(&p)) { elog("naved: no ground under crosshair"); return; }
  i = nav_pick(&p, 3.0f);
  if (i < 0) { elog("naved: no node near crosshair (%.2f %.2f %.2f)", p.x, p.y, p.z); return; }
  nav_pos(nav_node(g, i), &g_nedA);
  g_nedHasA = 1;
  elog("naved: A selected idx=%d at %.2f %.2f %.2f", i, g_nedA.x, g_nedA.y, g_nedA.z);
}
static void nav_add_here(void) {
  P g = navfix_point_graph();
  V3 p;
  int idx, ia;
  if (!g) return;
  if (!cam_point(&p)) { elog("naved: no ground under crosshair"); return; }
  p.y += 0.05f;
  if (nav_find(g, &p, 0.4f) >= 0) { elog("naved: node already exists here"); return; }
  idx = nav_add_node(g, &p);
  if (idx < 0) { elog("naved: add node failed"); return; }
  nav_push(NADD, &p, 0);
  if (g_nedHasA) {
    ia = nav_find(g, &g_nedA, 1.5f);
    if (ia >= 0) {
      nav_edge(g, nav_node(g, ia), nav_node(g, idx), 1);
      nav_push(EADD, &g_nedA, &p);
      elog("naved: also linked A -> new node");
    }
  }
  nav_refresh(g);
  elog("naved: node added idx=%d at %.2f %.2f %.2f", idx, p.x, p.y, p.z);
}
static void nav_del_here(void) {
  P g = navfix_point_graph();
  V3 p, q;
  int i;
  if (!g) return;
  if (!cam_point(&p)) { elog("naved: no ground under crosshair"); return; }
  i = nav_pick(&p, 3.0f);
  if (i < 0) { elog("naved: no node near crosshair"); return; }
  nav_pos(nav_node(g, i), &q);
  nav_kill_node(g, nav_node(g, i));
  nav_push(NDEL, &q, 0);
  nav_refresh(g);
  elog("naved: node disabled idx=%d at %.2f %.2f %.2f", i, q.x, q.y, q.z);
}
static void nav_toggle_edge(void) {
  P g = navfix_point_graph();
  V3 p, q;
  int i, ia;
  if (!g) return;
  if (!g_nedHasA) { elog("naved: select A first (Ctrl+Shift+A)"); return; }
  if (!cam_point(&p)) { elog("naved: no ground under crosshair"); return; }
  i = nav_pick(&p, 3.0f);
  if (i < 0) { elog("naved: no node near crosshair"); return; }
  ia = nav_find(g, &g_nedA, 1.5f);
  if (ia < 0) { elog("naved: A node disappeared, re-select it"); g_nedHasA = 0; return; }
  nav_pos(nav_node(g, i), &q);
  if (nav_conn_has(nav_node(g, ia), nav_node(g, i))) {
    nav_conn_set(nav_node(g, ia), nav_node(g, i), 0);
    nav_conn_set(nav_node(g, i), nav_node(g, ia), 0);
    nav_push(EDEL, &g_nedA, &q);
    elog("naved: edge A<->node removed");
  } else {
    nav_edge(g, nav_node(g, ia), nav_node(g, i), 1);
    nav_push(EADD, &g_nedA, &q);
    elog("naved: edge A<->node added");
  }
  nav_refresh(g);
}
static void nav_reapply(void) {
  P g = navfix_point_graph();
  int ops;
  if (!g) { elog("naved: no point graph"); return; }
  if (!g_nedN) { elog("naved: no edits for this map"); return; }
  ops = nav_apply_all(g);
  nav_refresh(g);
  elog("naved: re-applied %d/%d edits", ops, g_nedN);
}
/* 主线程 tick：等图稳定 -> 读本图的编辑文件 -> 套用 */
static void nav_edit_tick(void) {
  P g;
  int n, ops;
  if (g_collectOnly || !ed_init()) return;
  g = navfix_point_graph();
  if (!g) { g_nedGraph = 0; g_nedApplied = 0; g_nedWaitN = -1; return; }
  if (g != g_nedGraph) {
    g_nedGraph = g;
    g_nedApplied = 0;
    g_nedWaitN = -1;
    g_nedHasA = 0;
    g_nedN = 0;
    g_nedPath[0] = 0;
  }
  n = nav_count(g);
  if (!g_nedApplied) {
    if (n <= 0) return;
    if (n != g_nedWaitN) { g_nedWaitN = n; return; }       /* 等两跳稳定 */
    nav_fp(g_nedFp, sizeof(g_nedFp));
    CreateDirectoryA(g_dir, 0);
    {
      char nd[MAX_PATH];
      sprintf(nd, "%s\\nav", g_dir);
      CreateDirectoryA(nd, 0);
    }
    sprintf(g_nedPath, "%s\\nav\\%s.txt", g_dir, g_nedFp);
    nav_edit_load(g_nedPath);
    g_nedBaseN = n;
    ops = nav_apply_all(g);
    g_nedApplied = 1;
    if (ops) elog("naved: applied %d/%d edits on %s (nodes %d -> %d)",
                  ops, g_nedN, g_nedFp, g_nedBaseN, nav_count(g));
    else elog("naved: no edit file for %s", g_nedFp);
    return;
  }
  /* 图被游戏重扫/重建过 -> 改动没了，重新套用（每 ~1 s 检查一次） */
  if (g_nedN) {
    static int probe;
    if ((++probe % 16) == 0 && nav_needs_apply(g)) {
      ops = nav_apply_all(g);
      if (ops) {
        elog("naved: graph rebuilt, re-applied %d edits", ops);
        nav_refresh(g);
      }
    }
  }
}

#include "probe.c"

/* main-thread tick: keeps the labels glued to their world positions */
void editor_tick(void) {
  static int ticks;
  if (!g_inited) return;
  if (g_autoExport) auto_export_tick();
  nm_auto_tick();
  probe_tick();               /* 路点体检：读开关 / 停战 / 采样 / 写状态 */
  if (g_collectOnly) {
    if ((++ticks % 20) == 0) {   /* 每 5 s 一行心跳，崩溃时日志能指到具体地图 */
      char mn[80];
      P pg = navfix_point_graph();
      map_name_from_minimap(mn, sizeof(mn));
      elog("hb: collect-only map='%s' nodes=%d markers=%d", mn, pg ? *(int*)((char*)pg + 0xEC) : -1, g_n);
    }
    return;
  }
  nav_edit_tick();            /* 等图稳定后自动套用本图的编辑（不看 vis 开关） */
  if (!g_visOn) return;
  if (g_visDirty) {
    g_visDirty = 0;
    vis_rebuild();
  }
  vis_label_tick();
  if ((++ticks % 8) == 0) hud_refresh();   /* keep counters live at ~2 s */
}

/* warm up the il2cpp lookups on a quiet main-thread tick, not during a scene load */
void editor_ensure_init(void) { ed_init(); }

void editor_delete_nearest(void) {
  if (!ed_init()) return;
  delete_nearest();
}

void editor_on_key_mod(unsigned vk, int shift) {
  V3 p;
  if (!ed_init()) return;

  /* ---- visualizer hotkeys (work with or without edit mode) ---- */
  if (vk == 'V') { vis_toggle(); return; }
  if (shift && vk == 'X') { set_collect_only(!g_collectOnly); return; }
  if (vk == 'E') { g_exportForce = 1; vis_export(); g_exportForce = 0; return; }
  if (vk == 'H') { g_helpOn = !g_helpOn; hud_refresh(); return; }
  if (shift && vk == 'L') {
    g_lblMode = (g_lblMode + 1) % 3;
    elog("vis labels -> %d (0=off 1=near 2=all)", g_lblMode);
    hud_refresh();
    return;
  }
  if (shift && vk >= '1' && vk <= '5') {
    vis_toggle_layer(1 << (vk - '1'));
    return;
  }

  /* ---- 路点编辑（Ctrl+Shift+字母） ---- */
  if (shift && vk == 'A') { nav_sel_a(); return; }        /* 选 A 点 */
  if (shift && vk == 'N') { nav_add_here(); return; }     /* 准星处加点 */
  if (shift && vk == 'J') { nav_toggle_edge(); return; }  /* A <-> 准星节点 连/断 */
  if (shift && vk == 'D') { nav_del_here(); return; }     /* 禁用准星节点 */
  if (shift && vk == 'Z') { nav_undo(); return; }         /* 撤销上一条 */
  if (shift && vk == 'S') { nav_save(); return; }         /* 手动再存一次 */
  if (shift && vk == 'R') { nav_reapply(); return; }      /* 强制重新套用 */

  if (vk == '1') {
    g_on = !g_on;
    elog("editor %s (markers=%d)", g_on ? "ON" : "OFF", g_n);
    hud_refresh();
    return;
  }
  if (vk == '9') { status(); hud_refresh(); return; }
  if (!g_on) return;
  switch (vk) {
    case '0':
      toggle_visuals();
      break;
    case '2':
      if (!cam_point(&p)) { elog("crouch: no ground under crosshair"); break; }
      make_crouch(p);
      break;
    case '3':
      elog("nanopos: use Ctrl+4 (navfix creates area+pos with correct wiring)");
      break;
    case '4':
      if (!cam_point(&p)) { elog("area: no ground under crosshair"); break; }
      {
        P ext = navfix_add_guard_area(p.x, p.y, p.z);
        elog("area: navfix created %p at %.2f %.2f %.2f", ext, p.x, p.y, p.z);
        editor_mark_dirty();
        vis_rebuild();
        hud_refresh();
      }
      break;
    case 0x2E:  /* VK_DELETE */
      delete_nearest();
      break;
    case '5':
      undo_last();
      break;
    case '6':
      save_file();
      break;
    case '7':
      reset_markers();
      load_file();
      break;
    case '8':
      g_team = g_team ? 0 : 1;
      elog("team -> %d (%s) for new crouch points", g_team, g_team ? "GR" : "BL");
      hud_refresh();
      break;
    default:
      break;
  }
}

void editor_on_key(unsigned vk) { editor_on_key_mod(vk, 0); }

/* headless entry used by the WM_APP+0x53 test hook (no keyboard focus needed) */
void editor_on_key_any(unsigned vk, int shift) {
  if (!ed_init()) return;
  elog("test-key vk=0x%02X shift=%d", vk & 0xFF, shift);
  editor_on_key_mod(vk, shift);
}

void editor_on_quit(void) {
  elog("quit: editor stop (markers=%d vis nodes=%d labels=%d)", g_n, g_vnN, g_vfN);
}

void editor_start(const char* modDir) {
  if (!modDir) return;
  strncpy(g_dir, modDir, sizeof(g_dir) - 1);
  sprintf(g_log, "%s\\ucf_mod.log", g_dir);
  sprintf(g_file, "%s\\markers\\markers.txt", g_dir);
  elog("editor ready: Ctrl+V vis, Ctrl+Shift+1..5 layers, Ctrl+E export, Delete remove, file=%s", g_file);
  {
    char p[MAX_PATH];
    FILE* fh;
    extern void navfix_set_collect_only(int);
    sprintf(p, "%s\\collect.flag", g_dir);
    fh = fopen(p, "r");
    if (fh) { fclose(fh); g_collectOnly = 1; }
    navfix_set_collect_only(g_collectOnly);
    elog("mode: %s (flag %s)", g_collectOnly ? "COLLECT-ONLY 只读采集" : "INTERACTIVE 可编辑", p);
    if (g_collectOnly) elog("collect-only: Ctrl+Shift+X 切回交互模式（或直接删掉 collect.flag）");
  }
}
