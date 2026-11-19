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
#include "cfg.h"

typedef void* P;
typedef struct { float x, y, z; } V3;
typedef struct { float x, y; } V2;
typedef struct { float r, g, b, a; } COL;

/* UnityEngine.Object.m_CachedPtr (+0x8) is cleared when the native object is
 * destroyed.  Touching a destroyed component from native code raises a managed
 * MissingReferenceException; IL2CPP cannot unwind into C, so it aborts. */
static int uobj_live(P o) { return o && *(P*)((char*)o + 0x8) != 0; }

/* Conservative readability probe.  Any mangled pointer inside the il2cpp heap
 * turns a plain dereference into an access violation, and IL2CPP cannot unwind
 * back into C - the game just disappears.  Walk the page tables first.
 * 2026-11-16: Ctrl+V crashed at 'mov (%ebx),%ecx' in read_nav (crash.dmp
 * 0x68985C60): a PointNode's connections array had a garbage length and the
 * scan walked 40k entries past it into an uncommitted page. */
static int mem_ok(const void* p, size_t n) {
  MEMORY_BASIC_INFORMATION mbi;
  const char* q = (const char*)p;
  size_t left = n;
  if (!p || !n) return 0;
  while (left) {
    size_t avail;
    if (!VirtualQuery((LPCVOID)q, &mbi, sizeof(mbi))) return 0;
    if (mbi.State != MEM_COMMIT) return 0;
    if (mbi.Protect & (PAGE_NOACCESS | PAGE_GUARD)) return 0;
    avail = (size_t)((const char*)mbi.BaseAddress + mbi.RegionSize - q);
    if (avail > left) avail = left;
    left -= avail;
    q += avail;
  }
  return 1;
}

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

/* ---- 四版路径（2026-11-18）------------------------------------------------
 * ① 备份版 navdata\native / ② 开发版 navdata\dev / ③ 部署版 <游戏目录> /
 * ④ 测试版 navdata\test（导出收件箱 + 测试包）。
 * 插件只负责 ④ 的写入，③ 的 maps\ nav\ 由控制台「部署到游戏」从 ② 推过来。
 * 导出/测试包目录解析顺序：环境变量（控制台启动游戏时注入）> ucf_mod.json > 插件目录。 */
static char g_expDir[MAX_PATH];    /* 导出根：UCF_EXPORT_DIR > cfg export_dir > <dir>\vis */
static char g_packRoot[MAX_PATH];  /* 测试包根：UCF_PACK_DIR > cfg pack_dir > <dir>\packs */
static int  g_navReadOnly;         /* UCF_NAV_READONLY=1：正式版 nav\ 不允许游戏内落盘 */
static int  g_saveWarned;

/* ---- 测试包（UCF_PACK / UCF_FP）-------------------------------------------
 * 「UCF 控制台」启动游戏时递进来的环境变量，决定这次读哪套路线数据：
 *   UCF_PACK=chain_a   读 <插件目录>\packs\chain_a\<指纹>.txt
 *                      （不设 = 读 <插件目录>\nav\<指纹>.txt，即一直以来的正式版）
 *   UCF_FP=n0-...      只有当前场景指纹等于它才套用；别的图整包跳过，不动一个字节
 *   UCF_FPLABEL=...    只用于日志显示（图的中文名）
 * 包目录固定放在插件目录内：vis / markers / 日志也都挂在 g_dir 下，把 nav 单独指到
 * 工程端会让两套数据混用（导出、读数全乱），所以这里只换最后一级目录。 */
static char g_navDir[MAX_PATH];   /* 路线数据目录：<dir>\nav 或 <dir>\packs\<包名> */
static char g_packName[64];       /* 空 = 正式版 */
static char g_packFp[48];         /* 空 = 不限图 */
static char g_packFpLabel[64];    /* 只用于显示 */
static int  g_packSkip;           /* 1 = 当前图不在本次测试清单里 */
static char g_packStat[224] = "数据 正式版（nav）";   /* 日志里的数据来源一行 */

/* ---- 控制台命令通道（游戏运行中切包 / 重读 / 保存）----------------------
 * 控制台写 <插件目录>\ucf_navcmd.txt，插件每 ~0.5 s 查一次 seq；seq 变了才执行。
 * 启动时先读一遍 seq 但不执行，上一次进程留下的旧命令不会被新进程重放。
 *   seq=...  cmd=apply|reload|save|off  pack=<名>  fp=<指纹>
 * apply/reload 会先把图还原成原生底图，再重新读文件套用（见 nav_base_restore）。 */
static unsigned long long g_navCmdSeq;   /* 控制台写毫秒时间戳，32/64 位都收 */
static char g_navCmdPath[MAX_PATH];

/* 原生底图快照：切包 / 回正式版时把 PointGraph 还原成进图时的样子。
 * 连接按 nodeIndex 存（不存 PointNode 指针），场景重建后也不会指到旧对象。 */
typedef struct { unsigned char walk; V3 pos; int cn; unsigned char* conn; } NAVBASENODE;
static NAVBASENODE* g_navBase;
static int  g_navBaseN;
static P    g_navBaseG;
static char g_navBaseFp[48];

static int  g_inited, g_initFail;
static int  g_on, g_team, g_vis = 1;
static int  g_n, g_areaCount, g_curArea = -1;
static P    g_lastAstar;

static P (*x_domain_get)(void);
static P (*x_domain_get_assemblies)(P, int*);
static P (*x_assembly_get_image)(P);
static P (*x_class_from_name)(P, const char*, const char*);
static P (*x_class_get_type)(P);
static P (*x_type_get_object)(P);
static P (*x_object_new)(P);
static P (*x_string_new)(const char*);
static P (*x_thread_attach)(P);
static P (*x_class_get_field_from_name)(P, const char*);
static P (*x_field_get_type)(P);
static P (*x_class_get_element_class)(P);
static void (*x_field_static_get_value)(P, void*);
static P (*x_array_new)(P, unsigned int);
static P (*x_class_get_parent)(P);
static P (*x_class_from_il2cpp_type)(P);
static int (*x_class_instance_size)(P);
static char* (*x_type_get_name)(P);
static void (*x_free)(void*);
static P (*x_domain_assembly_open)(P, const char*);
static unsigned (*x_gchandle_new)(P, unsigned char);
static void (*x_gchandle_free)(P);
static void (*x_gc_wbarrier_set_field)(P, P, P);
static P (*x_class_get_method_from_name)(P, const char*, int);
static P (*x_runtime_invoke)(P, void*, void**, void**);

static P g_goCls, g_camCls, g_colCls, g_boxCls, g_crouchCls, g_areaCls, g_posCls;
static P g_colType, g_boxType, g_crouchType, g_areaType, g_posType;
static P g_rendCls, g_rendType, g_textCls, g_textType, g_canvasCls, g_canvasType, g_fontCls, g_fontType;

static P g_matCls;
static P g_meshCls, g_mfCls, g_mrCls, g_vec3Cls, g_i32Cls;
static P g_guardCls, g_jumpCls, g_tagCls, g_gareaCls, g_jumpLinkCls;
static P g_mmCls, g_mmInstField;
static P g_mfType, g_mrType, g_guardType, g_jumpType, g_tagType, g_gareaType;
static P g_matProto;     /* working template material (game shader) */
static char g_shaderName[96]; /* cached shader path, so materials survive asset unloads */
static P g_matSlot[16];  /* cached material per marker type 1..15   */
static int g_matReady;

/* 路点图编辑（定义在文件后半段，这里提前声明给 ed_init/editor_on_scene 用） */
typedef struct { int kind; int dir; V3 a, b; } NAVED;   /* dir: 0 双向 / 1 A->B / 2 B->A */
#define NAV_ED_MAX 4096
#define NAV_MAXN 20000

/* connections 数组的强根。
 * 只写 connections 字段 + GC 写屏障，在 138 点/105 边这种大图上仍然会在旧图
 * 销毁时崩在 PointNode.ClearConnections：屏障保证“字段→数组”，但数组里
 * Connection.node 的引用和旧图生命周期在 Unity 卸载时很脆。
 * 这里给每个 nodeIndex 的当前 connections 数组保留一个 gchandle，等下一次
 * 同一槽位换数组时再释放；数组在旧图销毁期间绝不会被 GC 回收。
 * 代价是每张图最多 786 个句柄；退出时统一释放，换图后同一槽位换数组时
 * 会在 nav_conn_bind 里释放旧句柄。 */
static unsigned g_connRoot[NAV_MAXN];
static void nav_conn_roots_release(void) {
  int i;
  if (!x_gchandle_free) return;
  for (i = 0; i < NAV_MAXN; i++) {
    if (g_connRoot[i]) {
      x_gchandle_free((P)g_connRoot[i]);
      g_connRoot[i] = 0;
    }
  }
}
static NAVED g_ned[NAV_ED_MAX];
static int g_nedN;
static NAVED g_redo[NAV_ED_MAX];
static int g_redoN;
static int g_nedBlank;      /* 1 = 测试包 blank：先把原生点全禁掉，再套清单里的点/边 */
static char g_nedPath[MAX_PATH];
static char g_nedFp[48];
static int g_nedBaseN;
static int g_nedExpect;     /* 套用后应有的节点数：用来判断图是否被游戏重扫过 */
static int g_nedApplied;
static int g_nedWaitN;
/* 车测自由视角（UCF_FREECAM=1 才启用；正常游戏完全不进这条路径） */
static int g_freeEnv, g_freeOn, g_freeInited, g_freeVcamOff, g_freeWarned, g_freeEnvRead;
static DWORD g_freeLastTick;
static P g_freeCam, g_freeVcamGo, g_freeTrCls, g_freeBrain, g_freeBrainCls;
static V3 g_freePos;
static float g_freeYaw, g_freePitch;
static P   g_nedGraph;
static int g_nedHasA;
static V3  g_nedA;
static P   g_pnodeCls, g_connCls;

static P g_cat;          /* UGUI Text: D-layer category list (left edge) */
static P g_catGo;
static P g_menu;         /* UGUI Text: SyPB-style waypoint menu */
static P g_menuGo;
static int g_wpMenuOn = 1;      /* cfg: wp_menu */
static int g_wpMenuOpen;
static int g_wpMenuSel;
static int g_wpMenuSub;         /* 0 main 1 types 2 paths 3 areas 4 edit 5 display */
static int g_wpMenuSubSel;
static int g_wpBrush;           /* 0 normal 1 jump 2 crouch 3 guard 4 area 5 tag */
static int g_wpPath;            /* 0 both 1 A->B 2 B->A */
static int g_wpAutoGround = 1;  /* cfg: wp_autoground */
static int g_wpArm;             /* next Enter/LMB places */
static int g_wpLinkStep;        /* 1 need A, 2 need B */
static DWORD g_wpEDownAt;
static int g_wpEFired;
static char g_wpBrushName[16] = "normal";
static P g_guiFont;      /* font borrowed from the game UI (has CJK glyphs) */
static unsigned g_fontHandle; /* gchandle: keep the chosen font alive */
static P g_fontRooted;   /* which font g_fontHandle roots */
static int g_cjk;        /* 1 = chosen font really has 中, hint text in Chinese */
static int g_tintLogged; /* one-shot material/shader diagnostic */

#define RVA(x) ((void*)((char*)g_ga + (unsigned)(x)))

#define R_GOCREATE    0x331AF0
#define R_ADDCOMP     0x331A90
#define R_GETCOMP     0x331C10
#define R_CTOR_STR    0x331EA0
#define R_GET_TR      0x332010
#define R_SETACTIVE   0x331CF0
#define R_SET_ENABLED 0x3253E0   /* Behaviour.set_enabled(bool)            */
#define R_SETLAYER    0x332040
#define R_GETGO       0x32CEB0
#define R_SET_POS     0x3F4840
#define R_GET_POS_INJ 0x3F4280
#define R_SET_EULER   0x3F44F0   /* Transform.set_eulerAngles(Vector3)     */
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
#define R_FONT_HASCHAR 0xAC7E00   /* Font.HasCharacter(char) —— 字体到底有没有中文字形 */
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
typedef unsigned char (*has_char_t)(P, unsigned short, void*);
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
static const COL COL_NAVM   = { 0.15f, 1.00f, 0.55f, 1.0f };  /* A* 可走面（NavMeshGraph 三角网） */

/* --- 最近日志环形缓冲：崩溃时回显最后几行到 ucf_mod.log ---------------- */
#define LOG_RING 24
static char g_ring[LOG_RING][128];
static int  g_ringN = 0;

static void log_ring_push(const char* s) {
  int i = g_ringN % LOG_RING, n = 0;
  while (s[n] && n < (int)sizeof(g_ring[0]) - 1) { g_ring[i][n] = s[n]; n++; }
  g_ring[i][n] = 0;
  g_ringN++;
}

static void elog(const char* fmt, ...) {
  char buf[512];
  va_list ap;
  va_start(ap, fmt);
  vsnprintf(buf, sizeof buf, fmt, ap);
  va_end(ap);
  if (g_log[0]) {
    FILE* f = fopen(g_log, "a");
    if (f) {
      SYSTEMTIME st;
      GetLocalTime(&st);
      fprintf(f, "%04d-%02d-%02d %02d:%02d:%02d [edit] %s\n",
              st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond, buf);
      fclose(f);
    }
  }
  log_ring_push(buf);
}

/* ---------------- 崩溃现场记录（VEH）---------------------------------------
 * 2026-11-17 10:22/10:23 两次闪退都落在 GameAssembly.dll+0x1290b1/c1，
 * 崩溃线程栈上一个 ucf_mod 帧都没有 —— 说明崩的是游戏代码，但很可能是我们之
 * 前放进去的对象/数据触发的。这里挂一个向量异常处理：崩的瞬间把「异常地址、
 * 读取/写入哪个地址、栈上所有落在模块里的返回地址、以及最近 24 条日志」写进
 * ucf_mod.log，下次再崩就能直接看到是谁调用的。只记录，不改变异常走向。
 * ---------------------------------------------------------------------- */
static unsigned mod_off(const void* a, const char** nmOut, int needCode) {
  static const char* names[] = { "GameAssembly.dll", "UnityPlayer.dll", "ucf_mod.dll" };
  int i;
  for (i = 0; i < 3; i++) {
    HMODULE h = GetModuleHandleA(names[i]);
    const unsigned char* base;
    const IMAGE_DOS_HEADER* dos;
    const IMAGE_NT_HEADERS* nt;
    unsigned size, off;
    if (!h) continue;
    base = (const unsigned char*)h;
    dos = (const IMAGE_DOS_HEADER*)base;
    if (dos->e_magic != IMAGE_DOS_SIGNATURE) continue;
    nt = (const IMAGE_NT_HEADERS*)(base + dos->e_lfanew);
    if (nt->Signature != IMAGE_NT_SIGNATURE) continue;
    size = nt->OptionalHeader.SizeOfImage;
    if ((const unsigned char*)a < base || (const unsigned char*)a >= base + size) continue;
    off = (unsigned)((const unsigned char*)a - base);
    if (needCode) {
      /* 只认可执行节里的地址。不检查的话 .rdata 里的常数也会被当成返回地址，
       * 10:35 那次的日志里整串 UnityPlayer+0x1478f74 就是这种假帧，把真栈淹了。 */
      const IMAGE_SECTION_HEADER* s = IMAGE_FIRST_SECTION(nt);
      int k, ok = 0;
      for (k = 0; k < nt->FileHeader.NumberOfSections; k++, s++) {
        unsigned va = s->VirtualAddress;
        unsigned vs = s->Misc.VirtualSize ? s->Misc.VirtualSize : s->SizeOfRawData;
        if (off < va || off >= va + vs) continue;
        if (s->Characteristics & IMAGE_SCN_MEM_EXECUTE) ok = 1;
        break;
      }
      if (!ok) continue;
    }
    *nmOut = names[i];
    return off;
  }
  *nmOut = 0;
  return 0;
}

/* 只读「已提交且可读」的内存：VEH 里绝不能因为自己再崩一次而递归 */
static int safe_rd(const void* p, void* out, unsigned n) {
  MEMORY_BASIC_INFORMATION mbi;
  if (!p) return 0;
  if (VirtualQuery(p, &mbi, sizeof mbi) != sizeof mbi) return 0;
  if (mbi.State != MEM_COMMIT) return 0;
  if (mbi.Protect & (PAGE_NOACCESS | PAGE_GUARD)) return 0;
  if ((const unsigned char*)p + n > (const unsigned char*)mbi.BaseAddress + mbi.RegionSize) return 0;
  memcpy(out, p, n);
  return 1;
}

/* ---- 崩溃现场：把「正在被走查的那个对象/数组」也打出来 --------------------
 * 2026-11-17 的五次闪退（10:22 / 10:23 / 10:35 / 11:32 / 11:33）全部停在
 * GameAssembly+0x1290b1 / 0x1290c1，调用链固定为
 *   il2cpp_unity_liveness_calculation_from_statics/root -> 0x144217 -> 0x14458a
 *   -> 0x1441dc -> 0x1290a0
 * 这不是 GC 写屏障（真正的写屏障在 GameAssembly+0x14cd80），而是 Unity 在
 * Resources.UnloadUnusedAssets() 里做的「托管对象存活判定」：它把对象/数组
 * 里的每个槽位当引用逐层走查，走查前先读 obj->klass（+0x1290b1 就是那条
 * mov (%ebx),%eax）。所以 ebx 是「被当成对象」的那个值，edi-0x10 是它所在的
 * 数组/容器。把数组的类名、长度、前 8 个槽位和槽位的类名写进日志，就能直接
 * 看出是谁往引用数组里写了非对象数据。
 * ---------------------------------------------------------------------- */
/* Il2CppClass{image@0, gc_desc@4, name@8, namespaze@0xc, ...} -> 取类名 */
/* il2cpp 的 Il2CppClass 是**运行时分配**的（不在 GameAssembly.dll 里），
 * 所以不能用「指针落在模块内」来判断。改成看结构：
 *   +0x08 name(可读的 ASCII 串)  +0x16 byval_arg.type(1..0x1e)
 * 这两条同时成立才当成类对象。 */
static int looks_like_class(P k) {
  P nm = 0;
  unsigned char ty = 0;
  char c = 0;
  int i, ok = 0;
  if (!k) return 0;
  if (!safe_rd((const void*)((char*)k + 8), &nm, 4) || !nm) return 0;
  if (!safe_rd((const void*)((char*)k + 0x16), &ty, 1)) return 0;
  if (ty < 1 || ty > 0x1E) return 0;
  for (i = 0; i < 32; i++) {
    if (!safe_rd((const char*)nm + i, &c, 1)) return 0;
    if (!c) { ok = (i > 0); break; }
    if ((unsigned char)c < 0x20 || (unsigned char)c > 0x7e) return 0;
  }
  return ok;
}

static int safe_name(P k, char* out, int cap) {
  char* s = 0;
  int i;
  out[0] = 0;
  if (!looks_like_class(k)) return 0;
  if (!safe_rd((const void*)((char*)k + 8), &s, 4) || !s) return 0;
  /* 逐字节读：字符串正好压在页尾时，一次性读满 cap 会失败 */
  for (i = 0; i < cap - 1; i++) {
    char ch;
    if (!safe_rd((const char*)s + i, &ch, 1)) break;
    if (!ch) break;
    if ((unsigned char)ch < 0x20 || (unsigned char)ch > 0x7e) { out[0] = 0; return 0; }
    out[i] = ch;
  }
  out[i] = 0;
  return out[0] != 0;
}

static void probe_obj(const char* tag, P p) {
  P k = 0;
  char nm[64];
  if (!p) { elog("!!! %s %08x", tag, (unsigned)p); return; }
  if (!safe_rd((const void*)p, &k, 4)) { elog("!!! %s %08x (unmapped)", tag, (unsigned)p); return; }
  if (safe_name(k, nm, sizeof nm)) elog("!!! %s %08x klass=%08x '%s'", tag, (unsigned)p, (unsigned)k, nm);
  else elog("!!! %s %08x klass=%08x (?)", tag, (unsigned)p, (unsigned)k);
}

static void probe_arr(const char* tag, P arr) {
  P k = 0, ek = 0;
  char nm[80], en[80];
  int n = 0, i;
  unsigned raw[16];
  if (!arr) return;
  if (!safe_rd(arr, &k, 4)) { elog("!!! %s %08x (unmapped)", tag, (unsigned)arr); return; }
  safe_rd((char*)arr + 0xC, &n, 4);
  if (!safe_name(k, nm, sizeof nm)) strcpy(nm, "?");
  en[0] = 0;
  if (k && safe_rd((char*)k + 0x20, &ek, 4) && safe_name(ek, en, sizeof en))
    elog("!!! %s %08x len=%d klass=%08x '%s' elem='%s'", tag, (unsigned)arr, n, (unsigned)k, nm, en);
  else
    elog("!!! %s %08x len=%d klass=%08x '%s'", tag, (unsigned)arr, n, (unsigned)k, nm);
  if (safe_rd((char*)arr + 0x10, raw, sizeof raw)) {
    elog("!!!   raw %08x %08x %08x %08x %08x %08x %08x %08x",
         raw[0], raw[1], raw[2], raw[3], raw[4], raw[5], raw[6], raw[7]);
  }
  for (i = 0; i < 8 && i < n; i++) {
    P v = 0;
    P ek = 0;
    char en[64];
    if (!safe_rd((char*)arr + 0x10 + i * 4, &v, 4)) { elog("!!!   [%d] unmapped", i); break; }
    if (!v) { elog("!!!   [%d] null", i); continue; }
    if (safe_rd((const void*)v, &ek, 4) && safe_name(ek, en, sizeof en))
      elog("!!!   [%d] %08x klass=%08x '%s'", i, (unsigned)v, (unsigned)ek, en);
    else
      elog("!!!   [%d] %08x (not an object)", i, (unsigned)v);
  }
}

static LONG CALLBACK ed_veh(EXCEPTION_POINTERS* ep) {
  CONTEXT* c = ep->ContextRecord;
  const void* ex = (const void*)ep->ExceptionRecord->ExceptionAddress;
  const char* nm = "?";
  unsigned off;
  unsigned code = (unsigned)ep->ExceptionRecord->ExceptionCode;
  int i;

  /* 这些不是崩溃，是正常控制流：
   *   0x406D1388 RaiseException+SetThreadName（il2cpp/Unity 起线程时必发），
   *   0xE06D7363 C++ throw，0x40080201 WinRT originate。
   * 上一版把它们全当崩溃记，一次进图刷了 120 行，把真正那条埋了。 */
  if (code == 0x406D1388 || code == 0xE06D7363 || code == 0x40080201) return EXCEPTION_CONTINUE_SEARCH;

  off = mod_off(ex, &nm, 0);
  elog("!!! crash code=0x%08x at %p (%s+0x%x)", code, ex, nm ? nm : "?", off);
  if (code == EXCEPTION_ACCESS_VIOLATION && ep->ExceptionRecord->NumberParameters >= 2) {
    elog("!!! access %s at 0x%08x",
         ep->ExceptionRecord->ExceptionInformation[0] ? "write" : "read",
         (unsigned)ep->ExceptionRecord->ExceptionInformation[1]);
  }
  if (c) {
    unsigned sp = (unsigned)c->Esp, bp = (unsigned)c->Ebp;
    unsigned char buf[8];
    /* 寄存器：崩溃时那个坏指针通常还躺在 esi/edi/ebx 里，这是最值钱的一行 */
    elog("!!! reg eax=%08x ebx=%08x ecx=%08x edx=%08x esi=%08x edi=%08x ebp=%08x esp=%08x",
         (unsigned)c->Eax, (unsigned)c->Ebx, (unsigned)c->Ecx, (unsigned)c->Edx,
         (unsigned)c->Esi, (unsigned)c->Edi, bp, sp);
    /* 存活判定走查（0x1290a0）：ebx = 被当成对象解引用的值，edi-0x10 = 它所在的数组/容器。
     * 这是判断「谁往引用数组里写了非对象数据」最直接的证据。 */
    if (code == EXCEPTION_ACCESS_VIOLATION && nm && !strcmp(nm, "GameAssembly.dll") &&
        off >= 0x129090 && off <= 0x1290d0) {
      probe_obj("walk-obj(ebx)", (P)c->Ebx);
      probe_arr("walk-array(edi-0x10)", (P)((char*)c->Edi - 0x10));
      if (bp) {
        unsigned owner = 0;
        if (safe_rd((const void*)(bp + 0xc), &owner, 4)) probe_obj("walk-owner(ebp+0xc)", (P)owner);
      }
    }
    /* 栈扫描从 128 格放宽到 512 格（2 KB）：我们的帧是 -O2 不带 EBP 的，
     * 只靠 EBP 链根本看不到；上次日志只扫到 +0x1ec 就断了。 */
    for (i = 0; i < 512 && sp; i++) {
      unsigned v;
      if (!safe_rd((const void*)(sp + i * 4), &v, 4)) break;
      {
        const char* mn;
        unsigned mo = mod_off((void*)v, &mn, 1);
        if (mn) elog("!!! stack+0x%03x %08x %s+0x%x", i * 4, v, mn, mo);
      }
    }
    if (bp) {
      for (i = 0; i < 24; i++) {
        unsigned prev, ret;
        if (!safe_rd((const void*)bp, buf, 8)) break;
        memcpy(&prev, buf, 4);
        memcpy(&ret, buf + 4, 4);
        if (!ret) break;
        {
          const char* mn;
          unsigned mo = mod_off((void*)ret, &mn, 1);
          if (mn) elog("!!! ebp+%02d %08x %s+0x%x", i, ret, mn, mo);
          /* 走查的这几帧里 [ebp+8..+0x10] 是对象/类型/状态指针，直接点一下 */
          if (mn && !strcmp(mn, "GameAssembly.dll") && i < 6) {
            unsigned a0 = 0, a1 = 0, a2 = 0;
            safe_rd((const void*)(bp + 8), &a0, 4);
            safe_rd((const void*)(bp + 0xc), &a1, 4);
            safe_rd((const void*)(bp + 0x10), &a2, 4);
            if (a0) probe_obj("  arg0", (P)a0);
            if (a1) probe_obj("  arg1", (P)a1);
            if (a2 > 0x10000) probe_obj("  arg2", (P)a2);
          }
        }
        if (prev <= bp) break;
        bp = prev;
      }
    }
  }
  for (i = 1; i <= 16 && i <= g_ringN; i++) {
    int k = (g_ringN - i) % LOG_RING;
    elog("!!! ring[-%d] %s", i, g_ring[k < 0 ? k + LOG_RING : k]);
  }
  return EXCEPTION_CONTINUE_SEARCH;
}

static int g_vehOn;
static void veh_install(void) {
  if (g_vehOn) return;
  if (AddVectoredExceptionHandler(1, ed_veh)) {
    g_vehOn = 1;
    elog("veh: crash logger installed");
  }
}


/* ---------------- GC 根：把我们长期保存的托管对象钉住 --------------------
 * 2026-11-17 10:22 / 10:23 / 10:35 三次闪退都落在 GameAssembly.dll+0x1290b1/e1
 * （il2cpp 运行时读 obj->klass，然后 klass 是 0 —— Boehm 回收后的内存是清零的）。
 * 也就是说：有代码在用**已经被 GC 收掉的托管对象**。Boehm 只扫托管堆和线程栈，
 * 不扫 DLL 的 .data，所以 g_matSlot / g_cat *
 * g_visObj / g_nmObj 这些 C 静态指针必须自己做成 GC 根。
 *
 * 第一版（10:33）用的是「object[2048] + 一个 gchandle」，但 System.Object 找不到
 * （mscorlib 在程序集数组的未初始化尾巴后面，find_cls 的循环 break 掉了），
 * 日志里刷了十几行 "roots: no System.Object class" —— **等于一个都没钉住**，
 * 10:35 照样崩。现在改成每个对象一个 il2cpp_gchandle_new：一个句柄就是一个根，
 * 不依赖任何类的查找。
 * ---------------------------------------------------------------------- */
#define ROOTS_MAX 512
static P g_rootObj[ROOTS_MAX];
static P g_rootH[ROOTS_MAX];
static int g_rootsN, g_rootsFull;
static P find_cls(const char* ns, const char* name);   /* 定义在后面 */
static void list_layout_probe(void);                  /* 定义在后面 */

/* 换场景时调用：上一张图的对象已经被 Unity 销毁了，句柄要还回去，
 * 否则句柄表会一直涨，旧对象也永远回收不掉。 */
static void roots_clear(void) {
  int i;
  if (!g_rootsN) return;
  for (i = 0; i < g_rootsN; i++) {
    if (g_rootH[i] && x_gchandle_free) x_gchandle_free(g_rootH[i]);
    g_rootH[i] = 0;
    g_rootObj[i] = 0;
  }
  elog("roots: cleared %d handle(s)", g_rootsN);
  g_rootsN = 0;
}

static void root_put(P o) {
  int i;
  if (!o || !x_gchandle_new) return;
  for (i = 0; i < g_rootsN; i++) if (g_rootObj[i] == o) return;   /* 同一个对象只钉一次 */
  if (g_rootsN >= ROOTS_MAX) {
    if (!g_rootsFull) { g_rootsFull = 1; elog("roots: full (%d) - new objects are NOT pinned", ROOTS_MAX); }
    return;
  }
  g_rootH[g_rootsN] = (P)x_gchandle_new(o, 0);
  g_rootObj[g_rootsN] = o;
  g_rootsN++;
  if (g_rootsN == 1) elog("roots: first handle ok (%p)", g_rootH[0]);
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
  RESOLVE(class_from_name);
  RESOLVE(class_get_type);
  RESOLVE(type_get_object);
  RESOLVE(object_new);
  RESOLVE(string_new);
  RESOLVE(thread_attach);
  RESOLVE(class_get_field_from_name);
  RESOLVE(field_get_type);
  RESOLVE(class_get_element_class);
  RESOLVE(field_static_get_value);
  RESOLVE(array_new);
  RESOLVE(class_get_parent);
  RESOLVE(class_from_il2cpp_type);
  RESOLVE(class_instance_size);
  RESOLVE(type_get_name);
  RESOLVE(free);
  RESOLVE(domain_assembly_open);
  RESOLVE(gchandle_new);
  RESOLVE(gchandle_free);
  x_gc_wbarrier_set_field = (void (*)(P, P, P))GetProcAddress(g_ga, "il2cpp_gc_wbarrier_set_field");
  RESOLVE(class_get_method_from_name);
  RESOLVE(runtime_invoke);
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
  /* Bot_JumpLink.Link 是嵌套结构；从 links 字段的类型里拿到 Link[] 再取元素类。 */
  if (g_jumpCls && x_class_get_field_from_name && x_field_get_type &&
      x_class_from_il2cpp_type && x_class_get_element_class) {
    P f = x_class_get_field_from_name(g_jumpCls, "links");
    P ft = f ? x_field_get_type(f) : 0;
    P ac = ft ? x_class_from_il2cpp_type(ft) : 0;
    g_jumpLinkCls = ac ? x_class_get_element_class(ac) : 0;
  }
  elog("init: jumpLinkCls=%p", g_jumpLinkCls);
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
  list_layout_probe();     /* 核对我们猜的 List<T> 字段偏移 */
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
    case 15: return &COL_NAVM;
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
    root_put(m);
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
    root_put(m);
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
 *   E  mode state (log only)
 * ------------------------------------------------------------------------- */
P navfix_point_graph(void);
P navfix_add_guard_area(float x, float y, float z);

#define VIS_MAXN    6000
#define VIS_MAXE    20000
#define VIS_MAXF    1400
#define VIS_NBMAX   2048
#define MB_MAXV     20000
#define MB_MAXI     70000
/* 进图后等多少帧再读游戏自己的组件表（SpareAreaList / SpareList_BL/GR …）。
 * 2026-11-17：沙漠要塞一进图就闪退（crash dump 显示停在 comp_pos -> UnityPlayer
 * 0x755e86）。这些静态表在换图瞬间还指着上一张图正在销毁的组件，读位置就是野指针。 */
#define VIS_SCENE_WAIT 90

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

static int g_exporting;            /* 正在导出：忽略可视化开关，各类全读，绝不少导数据 */
static int g_visOn;
static int g_visDirty, g_visNoMesh;
static int g_editAllow = 1;       /* cfg: editor —— 是否允许进编辑模式 */
static int g_collectOnly;         /* 只读采集：不建图/不建蹲点/不建守区/不建任何 UI 对象 */
static int g_exportForce;         /* Ctrl+E 手动导出时绕过“已采过/太小”的过滤 */
/* Ctrl+E 导出：总开关 + 六类内容（独立于可视化开关；关掉哪类，JSON 里就不读/不写哪类） */
static int g_expEnabled = 1;      /* cfg: export_enabled —— 导出总开关 */
static int g_expNodes = 1;        /* cfg: export_nodes —— 路点 / 连线 */
static int g_expCrouch = 1;       /* cfg: export_crouch —— 人类蹲守点 */
static int g_expArea = 1;         /* cfg: export_area —— 幽灵守区 / 幽灵守点 */
static int g_expGuard = 1;        /* cfg: export_guard —— 守卫区 / 守卫点 */
static int g_expSpawn = 1;        /* cfg: export_spawn —— 出生点 / 补给箱 */
static int g_expTags = 1;         /* cfg: export_tags —— 跳点 / 标签区 */
static int g_nmVert, g_nmTri;     /* 本次导出的 NavMeshGraph 顶点/三角形数 */
static int g_nmShow = 1;          /* cfg: navmesh_show —— 画不画 A* 可走面线框 */
/* cfg: vis_* —— 每一类一个开关，同时决定「读不读」和「画不画」。
 * 「名单」= 游戏加载场景时登记出来、一直挂在类上的静态 List，不是实时算出来的；
 * 换图瞬间它们还指着上一张图正在销毁的组件，读位置就是野指针（2026-11-17 沙漠要塞
 * 进图闪退就是这么死的）。哪一类出问题就单独关哪一类。 */
static int g_visNodes  = 1;       /* PointGraph 路点 / 连线（A* 图，不是名单） */
static int g_visNano   = 1;       /* SpareAreaList：幽灵守区 + 幽灵守点 */
static int g_visCrouch = 1;       /* SpareList_BL/GR：人类蹲守点（蓝/红） */
static int g_visGuard  = 1;       /* Bot_GuardArea + Bot_GuardPos：守卫区 / 守卫点 */
static int g_visBorn   = 1;       /* MapManager：幽灵出生 / 保卫者出生 */
static int g_visSupply = 1;       /* MapManager：中立点 / 补给箱 / 红箱 / 蓝箱 */
static int g_visJump   = 1;       /* Bot_JumpLink：跳点（FindObjectsOfType，不是名单） */
static int g_visTag    = 1;       /* PointNodeTagModifier：标签区（同上） */
static int g_nmWireTri, g_nmWireVert;  /* 可走面当前三角形/顶点数（日志显示） */
static P   g_nmObj[16];           /* 可走面自己的网格对象（和可视化对象分开） */
static int g_nmObjN;
static int g_nmDirty = 1;         /* 换图/开关变化后要重建 */
static int g_sceneAge;            /* 进图后过了多少帧（VIS_SCENE_WAIT 之前不碰游戏组件表） */
static int g_sceneReadyOnce;      /* 本张图已经稳定过一次 */

static P   g_trKlass;             /* Transform 的 il2cpp 类：comp_pos 用它挡掉「不是 Transform」的指针 */
static int g_badTr;               /* comp_pos 拦下的坏指针个数（日志可看） */
static char g_nmFile[128];        /* 导航网格二进制文件名 */
static unsigned long long nm_seenFp;  /* 已落盘的导航网格指纹 */
static int nm_seen;
static int g_cArea, g_cPos, g_cCrouch, g_cSpawn, g_cJump, g_cTag, g_cGuard;
static void overlay_refresh(void);
static void overlay_reset(void);
static void nm_tick(void);           /* A* 可走面：按需重建（定义在 nm_dump 之后） */
static void nm_toggle(void);
static void nm_walk(int draw);       /* 只统计 = 0 / 画 = 1 */
static P comp_tr(P comp);
/* 路点体检（实现在 probe.c，本文件末尾 #include） */

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
static int flush_mesh_to(const char* name, int slot, int items, P* list, int* count, int cap) {
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
  {
    /* 这两条 memset 是往托管堆里写，长度必须和请求的完全一致。
     * 万一 il2cpp 给的数组比要的小（元素类型不对），memcpy 就会越界，
     * 把隔壁的托管对象写花 —— 后面任何一次 GC / 列表遍历都会崩。
     * 12:39 那次 SpareAreaList 里出现野值（0xacf898f8）就是这个味道。 */
    int vlen = *(int*)((char*)av + 0xC);
    int ilen = *(int*)((char*)ai + 0xC);
    if (vlen != g_bNV || ilen != g_bNI) {
      elog("!!! vis: ARRAY LEN MISMATCH vec3 %d/%d i32 %d/%d - skip (would overflow)",
           vlen, g_bNV, ilen, g_bNI);
      return 0;
    }
  }
  memcpy((char*)av + 0x10, g_bV, (size_t)g_bNV * 12);
  memcpy((char*)ai + 0x10, g_bI, (size_t)g_bNI * 4);
  ((mesh_arr_t)RVA(R_MESH_VERTS))(mesh, av, 0);
  ((mesh_arr_t)RVA(R_MESH_TRIS))(mesh, ai, 0);
  ((mesh_1_t)RVA(R_MESH_BOUNDS))(mesh, 0);
  ((mf_setmesh_t)RVA(R_MF_SETMESH))(mf, mesh, 0);
  mat = mat_for(slot);
  if (mat) ((set_shmat_t)RVA(R_REND_SETSM))(mr, mat, 0);
  ((set_int1_t)RVA(R_REND_SHADOW))(mr, 0, 0);
  if (*count < cap) { list[(*count)++] = go; root_put(go); }
  elog("vis: mesh '%s' slot=%d items=%d verts=%d tris=%d", name, slot, items, g_bNV, g_bNI / 3);
  return 1;
}

/* 可视化 5 层用的批（对象汇入 g_visObj，Ctrl+V 统一显隐） */
static int vis_flush_mesh(const char* name, int slot, int items) {
  return flush_mesh_to(name, slot, items, g_visObj, &g_visObjN, 80);
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

/* ---- 守卫区列表看门狗 -------------------------------------------------
 * 2026-11-17 12:39 的闪退（沙漠要塞、进图 13 s、有人机）：
 *   Bot.Update -> BotAction.NanoGuard.Update -> Bot_NanoGuardArea.GetPos
 *     -> SpareAreaList.Remove(this) -> List.IndexOf
 *     -> ObjectEqualityComparer.IndexOf -> 对 0xacf898f8（没映射）做虚调用 → 崩
 * 即 SpareAreaList 的 _items 里混进了一个不是对象的野值。这局里只有游戏自己
 * Add/Remove 这个列表；我们唯一会写它的地方是 purge_guard_areas()（这局没触发）。
 * 所以每 2 tick 抄一遍槽位指纹：一变就记一行，出现野值立刻打 !!! + 最近日志，
 * 用来定位「什么时候、在哪一步被写坏的」。
 * ---------------------------------------------------------------------- */
/* 类指针速查表。为什么需要：每校验一个槽位都要看它的类对象，而
 * looks_like_class() 要**逐字节**读类名（Bot_NanoGuardArea 17 字节），每读一个字节
 * 都走一遍 VirtualQuery —— 本机实测 391 ns/次，即一个槽位约 13 us。新寂静村 10 个
 * 守区 x 各自 posList，一秒 4 遍就是几十万次 VirtualQuery。同一个列表里的槽位几乎
 * 总是同一个类，所以把「已验证通过的类指针」记住，只在第一次遇到新类时扫名字。
 * il2cpp 的 Il2CppClass 生命周期等于进程，记住不会失效。 */
static P g_clsMemo[8];
static void cls_memo_put(P k) {
  static int rot;
  g_clsMemo[rot++ & 7] = k;
}
static int obj_klass_ok(P o) {
  P k = 0;
  int i;
  if (!o) return 1;                        /* null 合法 */
  if (!safe_rd((const void*)o, &k, 4)) return 0;
  for (i = 0; i < 8; i++) if (g_clsMemo[i] == k) return 1;
  if (!looks_like_class(k)) return 0;
  cls_memo_put(k);
  return 1;
}

static unsigned g_areaSig;
static int g_areaWatchN = -2;
static int g_areaTicks;
static int g_areaBad;          /* 已经报过同一种坏状态，别刷屏 */

/* 用 il2cpp 自己的元数据核对 List<T> 的字段偏移，别靠猜。
 * FieldInfo{name@0, type@4, parent@8, offset@0xc, token@0x10} */
static int field_off(P cls, const char* name) {
  P f;
  if (!cls || !x_class_get_field_from_name) return -1;
  f = x_class_get_field_from_name(cls, name);
  if (!f) return -1;
  return *(int*)((char*)f + 0xC);
}

static P field_type_class(P cls, const char* name) {
  P f, ty;
  if (!cls || !x_class_get_field_from_name || !x_class_from_il2cpp_type) return 0;
  f = x_class_get_field_from_name(cls, name);
  if (!f) return 0;
  ty = *(P*)((char*)f + 4);              /* FieldInfo.type */
  return ty ? x_class_from_il2cpp_type(ty) : 0;
}

/* 类名：走 il2cpp 自己的 type_get_name，不猜字段偏移 */
static const char* type_name(P klass) {
  static char buf[160];
  char* s;
  if (!klass || !x_class_get_type || !x_type_get_name) return "?";
  s = x_type_get_name(x_class_get_type(klass));
  if (!s) return "?";
  strncpy(buf, s, sizeof buf - 1);
  buf[sizeof buf - 1] = 0;
  if (x_free) x_free(s);
  return buf;
}

/* UCF 调试用：ucf_mod.json 里 "gc_probe": true → 每张图进图时强制一次 GC。
 * 用来区分「我们的写操作写坏了列表」和「一次 GC 就把游戏自己的对象收走了」。 */
static int g_gcProbe = -1;
static void (*x_gc_collect)(void);

void editor_gc_probe(void) {
  if (g_gcProbe < 0) g_gcProbe = cfg_bool("gc_probe", 0) ? 1 : 0;
  if (!g_gcProbe) return;
  if (!x_gc_collect && g_ga) *(void**)&x_gc_collect = GetProcAddress(g_ga, "il2cpp_gc_collect");
  if (x_gc_collect) { x_gc_collect(); elog("gc: forced collect (probe)"); }
}

static void list_layout_probe(void) {
  P lc = field_type_class(g_areaCls, "SpareAreaList");
  if (!lc) { elog("list layout: cannot resolve List<Bot_NanoGuardArea>"); return; }
  elog("list layout: _items=+0x%x _size=+0x%x _version=+0x%x inst=%d",
       field_off(lc, "_items"), field_off(lc, "_size"), field_off(lc, "_version"),
       x_class_instance_size ? x_class_instance_size(lc) : -1);
}

/* "perf": true 时把一次体检的耗时累加，每 60 s 打一行 —— 回答「这东西吃不吃性能」，
 * 不用猜。默认关，关着时只有 2 次 QueryPerformanceCounter 之外没有额外开销。 */
static double g_pfSum, g_pfMax;
static int g_pfCnt;

static void area_watch(void) {
  P l, items;
  int n, cap, i, bad = -1;
  unsigned sig = 2166136261u;
  P badv = 0;
  static int on = -1;
  if (on < 0) on = cfg_bool("area_watch", 1) ? 1 : 0;
  if (!on) return;                         /* 不想让插件碰这张表就设 area_watch:false */
  if (!g_areaCls || !g_inited) return;
  g_areaTicks++;
  l = static_obj(g_areaCls, "SpareAreaList");
  if (!l) {
    if (g_areaWatchN != -1) { g_areaWatchN = -1; elog("areas: list=null"); }
    return;
  }
  items = list_items(l);
  n = list_n(l);
  cap = items ? *(int*)((char*)items + 0xC) : -1;
  if (!items || n < 0 || cap < 0 || n > cap) {
    elog("!!! areas: BAD SIZE n=%d cap=%d list=%p items=%p", n, cap, l, items);
    return;
  }
  for (i = 0; i < cap && i < 512; i++) {
    P o = *(P*)((char*)items + 0x10 + i * 4);
    sig = (sig ^ (unsigned)o) * 16777619u;
    if (bad < 0 && !obj_klass_ok(o)) { bad = i; badv = o; }
  }
  if (bad >= 0) {
    int k;
    P kk = 0;
    if (g_areaBad == 0) g_areaBad = 1; else return;
    safe_rd((const void*)items, &kk, 4);
    elog("!!! areas CORRUPT idx=%d val=%08x n=%d cap=%d list=%p items=%p age=%d",
         bad, (unsigned)badv, n, cap, l, items, g_sceneAge);
    elog("!!! array type = '%s' (klass=%p cls=%d)", type_name(kk), (void*)kk, looks_like_class(kk));
    for (k = 0; k < n && k < 8; k++) {
      P v = *(P*)((char*)items + 0x10 + k * 4);
      P kv = 0;
      int rd = safe_rd((const void*)v, &kv, 4);
      elog("!!!   slot[%d] val=%08x klass=%08x readable=%d cls=%d type='%s'",
           k, (unsigned)v, (unsigned)kv, rd, looks_like_class(kv),
           looks_like_class(kv) ? type_name(kv) : "?");
    }
    for (k = 1; k <= 12 && k <= g_ringN; k++) {
      int r = (g_ringN - k) % LOG_RING;
      elog("!!! areas ring[-%d] %s", k, g_ring[r < 0 ? r + LOG_RING : r]);
    }
    return;
  }
  /* 每个守区自己的 posList（List<Bot_NanoGuardPos>）也一起体检：
   * GetPos 就是先从 posList 取点、空了再从 SpareAreaList 摘自己。 */
  for (i = 0; i < n && i < 64; i++) {
    P a = *(P*)((char*)items + 0x10 + i * 4);
    P pl, pit;
    int pn, pcap, j;
    if (!a) continue;
    pl = *(P*)((char*)a + 0x10);          /* Bot_NanoGuardArea.posList */
    if (!pl) continue;
    pit = list_items(pl);
    pn = list_n(pl);
    pcap = pit ? *(int*)((char*)pit + 0xC) : -1;
    if (!pit || pn < 0 || pcap < 0 || pn > pcap) {
      elog("!!! posList BAD area[%d]=%p pl=%p n=%d cap=%d age=%d", i, a, pl, pn, pcap, g_sceneAge);
      continue;
    }
    for (j = 0; j < pcap && j < 32; j++) {
      P o = *(P*)((char*)pit + 0x10 + j * 4);
      if (!obj_klass_ok(o)) {
        elog("!!! posList CORRUPT area[%d]=%p idx=%d val=%08x n=%d cap=%d age=%d",
             i, a, j, (unsigned)o, pn, pcap, g_sceneAge);
        probe_arr("poslist-array", pit);
        break;
      }
    }
  }
  if (n != g_areaWatchN || sig != g_areaSig) {
    g_areaWatchN = n; g_areaSig = sig;
    elog("areas: n=%d cap=%d sig=%08x age=%d", n, cap, sig, g_sceneAge);
  }
}
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
  P tr;
  if (!comp || !mem_ok(comp, 0x10)) return 0;
  tr = comp_tr(comp);
  if (!tr || !mem_ok(tr, 0x10) || !uobj_live(tr)) return 0;
  /* 组件表里可能混进「根本不是 Component」的指针：拿到的 tr 不是 Transform 类，
   * 再调 GetPosition 就崩在 UnityPlayer 里（沙漠要塞那次）。这里直接拦掉。 */
  if (g_trKlass && *(P*)tr != g_trKlass) { g_badTr++; return 0; }
  ((get_pos_t)RVA(R_GET_POS_INJ))(tr, out, 0);
  return 1;
}

/* 场景切换时游戏自己的静态组件表（SpareAreaList / SpareList_BL/GR / MapManager）
 * 里还挂着上一张图的组件；元素被销毁甚至被别的分配覆盖后，读出来的根本不是对象。
 * 2026-11-17 10:58 那次就是这么崩的：SpareAreaList[0] 读出来是 0x43ef6323
 * （一个 float 478.77），当成 Component 传给 Component.get_transform，
 * 崩在 UnityPlayer.dll+0x755e86。所以列表里的元素逐个校验 klass。 */
static int obj_is(P o, P cls) {
  if (!o || !cls) return 0;
  if (!mem_ok(o, 0x10)) return 0;
  return *(P*)o == cls;
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

static int nav_conn_get(P nd, P* out);    /* 定义在后面（跨边表校验） */
static int g_navBadNode, g_navBadConn;   /* 读图时发现的坏节点/坏连接表 */
static void read_nav(void) {
  P pg, arr;
  int n, i;
  if (!g_visNodes && !g_exporting) return;        /* 导出时忽略可视化开关 */
  pg = navfix_point_graph();
  if (!pg) { miss("pointgraph"); return; }
  if (!mem_ok(pg, 0xF0)) { miss("badgraph"); return; }
  n = *(int*)((char*)pg + 0xEC);
  arr = *(P*)((char*)pg + 0xE8);
  if (!arr || n <= 0) { miss("nodes0"); return; }
  if (n > VIS_MAXN) n = VIS_MAXN;
  if (!mem_ok(arr, 0x10 + (size_t)n * 4)) { miss("badnodes"); return; }
  g_navBadNode = g_navBadConn = 0;
  pm_reset();
  memset(g_vn, 0, sizeof(VN) * (size_t)(n > 0 ? n : 1));
  for (i = 0; i < n; i++) {
    P nd = *(P*)((char*)arr + 0x10 + i * 4);
    unsigned fl;
    if (!nd) continue;
    if (!mem_ok(nd, 0x28)) { g_navBadNode++; continue; }
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
    P cons = 0;
    int cn, j;
    if (!nd) continue;
    cn = nav_conn_get(nd, &cons);     /* 不可信的连接表直接跳过（曾因此闪退） */
    if (cn <= 0) { if (cn < 0) g_navBadConn++; continue; }
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
  if ((!g_visNano && !g_exporting) || !g_areaCls) return;
  l = static_obj(g_areaCls, "SpareAreaList");
  if (!l) { miss("SpareAreaList"); return; }
  n = list_n(l);
  items = list_items(l);
  if (!items) { miss("SpareAreaList.items"); return; }
  if (n > 400) n = 400;
  if (n > 0 && !mem_ok((char*)items + 0x10, (size_t)n * 4)) { miss("SpareAreaList.bad"); return; }
  for (i = 0; i < n; i++) {
    P a = *(P*)((char*)items + 0x10 + i * 4);
    V3 p;
    if (!obj_is(a, g_areaCls)) continue;
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
      int pn = (pl && mem_ok(pl, 0x10)) ? list_n(pl) : 0;
      P pit = (pl && mem_ok(pl, 0x10)) ? list_items(pl) : 0;
      if (!pit) pn = 0;
      if (pn > 20) pn = 20;
      if (pn > 0 && !mem_ok((char*)pit + 0x10, (size_t)pn * 4)) { pn = 0; }
      for (j = 0; j < pn && j < 20; j++) {
        P gp = *(P*)((char*)pit + 0x10 + j * 4);
        V3 q;
        if (!obj_is(gp, g_posCls)) continue;
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
  if ((!g_visCrouch && !g_exporting) || !g_crouchCls) return;
  for (k = 0; k < 2; k++) {
    P l = static_obj(g_crouchCls, fld[k]);
    int n = list_n(l), i;
    P items = l ? list_items(l) : 0;
    if (!l) { miss(k ? "SpareList_GR" : "SpareList_BL"); continue; }
    if (!items) continue;
    if (n > 600) n = 600;
    if (n > 0 && !mem_ok((char*)items + 0x10, (size_t)n * 4)) continue;
    for (i = 0; i < n; i++) {
      P c = *(P*)((char*)items + 0x10 + i * 4);
      V3 p;
      if (!obj_is(c, g_crouchCls)) continue;
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
  if (!g_visGuard && !g_exporting) return;
  read_typed(g_gareaType, g_gareaCls, K_GAREA, "守卫区域", 0);
}

static void read_spawns(void) {
  static const char* nm[6] = { "幽灵出生", "保卫者出生", "中立点", "补给箱", "红箱", "蓝箱" };
  static const int off[6] = { 0x10, 0x14, 0x18, 0x1C, 0x20, 0x24 };
  P mm = 0;
  int k;
  if (!g_visBorn && !g_visSupply && !g_exporting) return;
  if (g_mmInstField) x_field_static_get_value(g_mmInstField, &mm);
  if (!uobj_live(mm)) { miss("MapManager"); return; }
  for (k = 0; k < 6; k++) {
    P arr;
    int n, i;
    /* cfg: vis_born —— k 0..2 幽灵出生 / 保卫者出生 / 中立点；
     * cfg: vis_supply —— k 3..5 补给箱 / 红箱 / 蓝箱。两类各自管理：
     * 关掉哪一类，对应的数组都不读（连同 mem_ok 校验一起跳过）。
     * 导出路径（collect_read）不受这些开关影响：g_exporting 时不看它们。 */
    if (!g_exporting && (k <= 2 ? !g_visBorn : !g_visSupply)) continue;
    arr = *(P*)((char*)mm + off[k]);
    if (!arr || !mem_ok(arr, 0x10)) { miss(nm[k]); continue; }
    n = *(int*)((char*)arr + 0x0C);
    if (n < 0) n = 0;
    if (n > 200) n = 200;
    if (n > 0 && !mem_ok((char*)arr + 0x10, (size_t)n * 16)) { miss(nm[k]); continue; }
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
  if ((!g_visJump && !g_exporting) || !g_jumpType) return;
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
  if ((!g_visTag && !g_exporting) || !g_tagType) return;
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
  for (i = 1; i <= 15; i++) if (!g_matSlot[i]) mat_for(i);
  if (g_visNodes) {
    for (g = 0; g < 3; g++) {
      int c = 0;
      bs_reset();
      for (i = 0; i < g_vnN; i++) {
        V3 h;
        int grp = !g_vn[i].walk ? 2 : (g_vn[i].tag ? 1 : 0);
        if (!g_vn[i].walk && g_nedBlank && g_packName[0]) continue;  /* 空白底图：原生点不画，屏幕才是真空白 */
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
  }
  if (g_visJump && g_jN) {
    bs_reset();
    for (i = 0; i < g_jN; i++) bs_line(g_jA[i], g_jB[i], 0.10f);
    vis_flush_mesh("vis_jump", 4, g_jN);
  }
  if (g_visTag && g_tpN) {
    bs_reset();
    for (i = 0; i < g_tpN; i++) {
      V3 h;
      h.x = 0.45f; h.y = 0.45f; h.z = 0.45f;
      bs_wbox(g_tp[i], h, 0.06f);
    }
    vis_flush_mesh("vis_tags", 7, g_tpN);
  }
  if (g_visCrouch) draw_vf(K_CROUCH, 1, 0, 0.18f, 0.24f, 0.18f);
  if (g_visGuard) {
    draw_vf(K_GUARD, 7, 0, 0.26f, 0.32f, 0.26f);
    draw_vf(K_GAREA, 8, 1, 1.8f, 1.3f, 1.8f);
  }
  if (g_visNano) {
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
  if (g_visBorn || g_visSupply) {
    int k;
    for (k = 0; k < 6; k++) {
      int c = 0, slot = 13;
      if (k <= 2 ? !g_visBorn : !g_visSupply) continue;
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
}

static void vis_clear(void) {
  int i;
  for (i = 0; i < g_visObjN; i++) if (g_visObj[i]) ((destroy_t)RVA(R_DESTROY))(g_visObj[i], 0);
  g_visObjN = 0;
  g_vnN = g_veN = g_vfN = 0;
  g_nN = g_eN = g_jN = g_tpN = 0;
}

static void vis_rebuild(void) {
  vis_clear();
  g_cArea = g_cPos = g_cCrouch = g_cSpawn = g_cJump = g_cTag = g_cGuard = 0;
  g_miss[0] = 0;
  read_nav();
  if (g_visNano)   read_nano();   else miss("vis_nano=off");
  if (g_visCrouch) read_crouch(); else miss("vis_crouch=off");
  if (g_visGuard) {
    read_guardareas();
    read_typed(g_guardType, g_guardCls, K_GUARD, "守卫点", 1);
  } else miss("vis_guard=off");
  if (g_visBorn || g_visSupply) read_spawns();
  else miss("vis_born/supply=off");
  /* 跳点 / 标签区走 FindObjectsOfType，不碰静态名单，各有一个自己的开关。 */
  if (g_visJump) read_jump(); else miss("vis_jump=off");
  if (g_visTag)  read_tags(); else miss("vis_tag=off");
  vis_draw();
  vis_show(1);
  elog("vis: nodes=%d edges=%d features=%d (area=%d pos=%d crouch=%d guard=%d spawn=%d jump=%d tag=%d) badnode=%d badconn=%d badtr=%d missing=[%s]",
       g_vnN, g_veN, g_vfN, g_cArea, g_cPos, g_cCrouch, g_cGuard, g_cSpawn, g_cJump, g_cTag,
       g_navBadNode, g_navBadConn, g_badTr, g_miss);
  {
    int i, s0 = 0, s1 = 0, s2 = 0;
    for (i = 0; i < g_vfN; i++) {
      if (g_vf[i].kind != K_SPAWN) continue;
      if (g_vf[i].aux <= 2) s0++;
      else if (g_vf[i].aux == 3) s1++;
      else s2++;
    }
    elog("vis: spawn groups = 出生点%d 普通补给箱%d 红蓝补给箱%d", s0, s1, s2);
  }
  overlay_refresh();
}

/* the scene changed: the old overlay objects were destroyed with the level */
static void vis_scene_reset(void) {
  g_visObjN = 0;
  g_vnN = g_veN = g_vfN = 0;
  g_nN = g_eN = g_jN = g_tpN = 0;
  g_miss[0] = 0;
  g_sceneAge = 0;          /* 新图：组件表要等稳定才读 */
  g_badTr = 0;
  g_visDirty = g_visOn;
  /* 可走面的 Mesh 对象随旧场景一起被销毁：指针作废，下一帧重建 */
  g_nmObjN = 0;
  g_nmDirty = 1;
}

static void vis_toggle(void) {
  g_visOn = !g_visOn;
  if (g_visOn) { g_visDirty = 0; vis_rebuild(); }
  else vis_show(0);
  elog("vis %s (features=%d)", g_visOn ? "ON" : "OFF", g_vfN);
  overlay_refresh();
}

/* 路点 / 连线：只对本次进程生效（配置开关在控制台「可视化」页） */
static void vis_toggle_nodes(void) {
  g_visNodes = !g_visNodes;
  if (g_visOn) { g_visDirty = 0; vis_rebuild(); }
  elog("vis nodes=%d", g_visNodes);
  overlay_refresh();
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
  if (g_expNodes) read_nav(); else miss("export_nodes=off");
  /* 刚切图的 VIS_SCENE_WAIT 帧内：路点(来自 A* 图)和可走面可信，游戏自己的组件表
   * 还挂着上一张图的东西，整段跳过。这一步是 10:58 那次闪退的正面补丁 ——
   * 进图后导出（Ctrl+E）来得太早，正好撞在没稳定的时候。 */
  if (g_sceneAge < VIS_SCENE_WAIT) {
    miss("scene-not-ready");
    return;
  }
  if (g_expArea) read_nano();
  if (g_expCrouch) read_crouch();
  if (g_expGuard) {
    read_guardareas();
    read_typed(g_guardType, g_guardCls, K_GUARD, "守卫点", 1);
  }
  if (g_expSpawn) read_spawns();
  if (g_expTags) {
    read_jump();
    read_tags();
  }
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

/* ---- A* 可走面：NavMeshGraph 三角网（人机真正在上面跑的那张网）----------
 * 数据来源和 nm_dump 完全相同（运行时 NavmeshBase.tiles -> NavmeshTile），
 * 区别是这里直接进几何批（bs_*）画在屏幕上：
 *   * 只画三角形的边，不填面 —— 填面要吃材质透明度，游戏里那套 shader 不透明，
 *     一填就把整张地图盖住；线框从任何角度看都清爽。
 *   * 顶点是 Int3（1/1000 m，世界坐标）。多 tile 时索引高 12 位才是 tile 号，
 *     低 12 位是 tile 内的顶点号 —— 和 nm_dump 的掩码一致。
 *   * 抬高 5 cm，避免和地面/地形网格打架（z-fighting）。
 * draw=0 时只统计不建面（旧 HUD 用过；现在仅保留给内部统计）。 */
static void nm_walk(int draw) {
  extern P navfix_navmesh_graph(void);
  P g, tiles;
  int ntile, i, j, tri = 0;
  g_nmWireTri = 0;
  g_nmWireVert = 0;
  g = navfix_navmesh_graph();
  if (!g) return;
  tiles = *(P*)((char*)g + 0xD0);
  ntile = tiles ? *(int*)((char*)tiles + 0xC) : 0;
  if (ntile <= 0 || ntile > 4096) return;
  if (draw) bs_reset();
  for (i = 0; i < ntile; i++) {
    P tl = *(P*)((char*)tiles + 0x10 + i * 4);
    P tr, vr;
    int tv, tt, multi = ntile > 1;
    int* vi;
    int* ti;
    if (!tl) continue;
    tr = *(P*)((char*)tl + 0x8);
    vr = *(P*)((char*)tl + 0xC);
    tv = vr ? *(int*)((char*)vr + 0xC) : 0;
    tt = tr ? *(int*)((char*)tr + 0xC) : 0;
    if (tv <= 0 || tv > 200000 || tt <= 0 || tt > 200000) continue;
    g_nmWireVert += tv;
    g_nmWireTri += tt / 3;
    if (!draw) continue;
    vi = (int*)((char*)vr + 0x10);
    ti = (int*)((char*)tr + 0x10);
    for (j = 0; j + 2 < tt; j += 3) {
      V3 a, b, c;
      int ia = ti[j], ib = ti[j + 1], ic = ti[j + 2];
      if (multi) { ia &= 0xFFF; ib &= 0xFFF; ic &= 0xFFF; }
      if (ia < 0 || ib < 0 || ic < 0 || ia >= tv || ib >= tv || ic >= tv) continue;
      a.x = vi[ia * 3] * 0.001f; a.y = vi[ia * 3 + 1] * 0.001f + 0.05f; a.z = vi[ia * 3 + 2] * 0.001f;
      b.x = vi[ib * 3] * 0.001f; b.y = vi[ib * 3 + 1] * 0.001f + 0.05f; b.z = vi[ib * 3 + 2] * 0.001f;
      c.x = vi[ic * 3] * 0.001f; c.y = vi[ic * 3 + 1] * 0.001f + 0.05f; c.z = vi[ic * 3 + 2] * 0.001f;
      bs_line(a, b, 0.035f); bs_line(b, c, 0.035f); bs_line(c, a, 0.035f);
      tri++;
      /* 一条线 = 8 顶点 / 12 索引；批上限 20000 顶点、70000 索引。
       * 到 16000/56000 就落一次，一张图分成两三块网格，不会静默丢三角形。 */
      if (g_bNV > 16000 || g_bNI > 56000) {
        flush_mesh_to("vis_navmesh", 15, tri, g_nmObj, &g_nmObjN, 16);
        tri = 0;
        bs_reset();
      }
    }
  }
  if (draw && g_bNI) flush_mesh_to("vis_navmesh", 15, tri, g_nmObj, &g_nmObjN, 16);
  if (draw) elog("vis: navmesh wire tris=%d verts=%d meshes=%d", g_nmWireTri, g_nmWireVert, g_nmObjN);
}

/* ---- 可走面开关（独立于 Ctrl+V 总开关）--------------------------------
 * cfg navmesh_show 决定进图默认开不开；Ctrl+Shift+6 随时开关，立即重建。
 * 没有 NavMeshGraph 的图（运输船 / 生化酒店 / 暴风）什么都不画，日志里会写
 * 「无（这张图没有 NavMeshGraph）」。 */
static void nm_clear(void) {
  int i;
  for (i = 0; i < g_nmObjN; i++) {
    if (g_nmObj[i] && uobj_live(g_nmObj[i])) ((destroy_t)RVA(R_DESTROY))(g_nmObj[i], 0);
    g_nmObj[i] = 0;
  }
  g_nmObjN = 0;
}

static void nm_build(void) {
  extern P navfix_navmesh_graph(void);
  int i;
  nm_clear();
  g_nmWireTri = g_nmWireVert = 0;
  if (!g_nmShow || g_collectOnly) return;
  if (!navfix_navmesh_graph()) return;
  for (i = 1; i <= 15; i++) if (!g_matSlot[i]) mat_for(i);
  nm_walk(1);
}

/* 主线程 tick：开关/换图之后按需重建一次 */
static void nm_tick(void) {
  extern P navfix_navmesh_graph(void);
  if (!g_nmShow) {
    if (g_nmObjN) nm_clear();
    g_nmDirty = 0;
    return;
  }
  if (!navfix_navmesh_graph()) {
    if (g_nmObjN) nm_clear();
    g_nmWireTri = g_nmWireVert = 0;
    return;
  }
  if (g_nmObjN && !g_nmDirty) return;
  g_nmDirty = 0;
  nm_build();
}

static void nm_toggle(void) {
  g_nmShow = !g_nmShow;
  g_nmDirty = 1;
  nm_tick();
  elog("navmesh %s (%d tris / %d verts)", g_nmShow ? "ON" : "OFF", g_nmWireTri, g_nmWireVert);
  overlay_refresh();
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

  if (!g_expEnabled) {
    elog("vis: export disabled (export_enabled=false)");
    return;
  }

  /* 导出必须**重新读一遍**数据，而且只走只读通道：
   *  - 以前这里看 g_visOn：开着可视化时整段跳过，导出的就是上一个场景的残留（实测写成 0 点的 n0 假文件，
   *    还顺手写了个 _seen_n0 标记，把后面真正有 3063 个点的那张图当成"重复"跳过了 —— 数据就是这么丢的）。
   *  - 也不再用 vis_rebuild()：它会建 Mesh + UGUI 文本，导出时正好赶上场景加载，是崩溃高发点。 */
  if (g_sceneAge < VIS_SCENE_WAIT && !g_sceneReadyOnce) {
    elog("vis: export deferred (scene age %d/%d) - component tables are still the old level's",
         g_sceneAge, VIS_SCENE_WAIT);
    return;
  }
  g_exporting = 1;
  collect_read();
  g_exporting = 0;
  if (g_vnN <= 0 && g_vfN <= 0) {
    elog("vis: export skipped: nothing selected (nodes=0 features=0) - no empty file");
    return;
  }
  GetLocalTime(&st);
  strcpy(dir, g_expDir);          /* ④ 测试版导出收件箱（不再是 ③ 部署版） */
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
  /* 路点关掉时没有节点指纹可用：用特征数当指纹，且不写 _seen 去重标记（见下） */
  if (g_vnN > 0) sprintf(fp, "n%d-%016llx", g_vnN, xr);
  else sprintf(fp, "f%d", g_vfN);
  src = navfix_graph_ours();

  /* 同一张图只导一次：指纹相同说明节点位置完全一致（只对含路点的导出生效） */
  sprintf(mark, "%s\\_seen_%s", g_expDir, fp);
  if (g_vnN > 0 && !g_exportForce) {
    FILE* mf = fopen(mark, "r");
    if (mf) {
      fclose(mf);
      elog("vis: fp=%s already collected, skip duplicate", fp);
      return;
    }
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
  if (g_cjk && !g_collectOnly) overlay_refresh();
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

/* 选一个真的带中文字形的字体。
 * 2026-11-16：原来直接拿 FindObjectOfType(Text) 的第一个字体，常常拿到
 * FPS/数字字体，图例和菜单的中文标签全被吞掉，屏幕上只剩 "00000000" 和 "|++|"。
 * 这里遍历场景里所有 UGUI Text 的字体，用 Font.HasCharacter('中') 验证。 */
static P find_cjk_font(void) {
  P arr;
  int n, i, j;
  static const unsigned short probe[] = { 0x4E2D, 0x56FD, 0x7684, 0x623F, 0x95F4 };
  if (!g_textType) return 0;
  arr = ((find_objs_t)RVA(R_FINDOBJS))(g_textType, 1, 0);
  if (!arr) return 0;
  n = *(int*)((char*)arr + 0x0C);
  if (n > 600) n = 600;
  for (i = 0; i < n; i++) {
    P t = *(P*)((char*)arr + 0x10 + i * 4);
    P font;
    if (!t || !uobj_live(t)) continue;
    font = ((get_font_t)RVA(R_TEXT_GETFONT))(t, 0);
    if (!font || !uobj_live(font)) continue;
    for (j = 0; j < (int)(sizeof(probe) / sizeof(probe[0])); j++) {
      if (((has_char_t)RVA(R_FONT_HASCHAR))(font, probe[j], 0)) {
        elog("ui: cjk font %p from Text #%d (probe U+%04X)", font, i, probe[j]);
        return font;
      }
    }
  }
  elog("ui: no cjk font among %d Text objects", n);
  return 0;
}

static int overlay_init(void) {
  P canvasGo, canvasTr, comp;
  if (g_cat) return 1;
  if (!g_textType || !g_canvasType) { elog("ui: UGUI Text/Canvas class missing"); return 0; }
  if (g_guiFont && !uobj_live(g_guiFont)) { g_guiFont = 0; g_cjk = 0; }  /* 上个场景的字体被卸载 */

  /* 字体必须真的带中文字形。以前直接拿第一个 Text 的字体（常常是 FPS 数字字体），
   * 中文标签全被吞掉，屏幕上只剩 "00000000" 和 "|++|" 这种残片。 */
  if (!g_cjk) {
    P cjk = find_cjk_font();
    if (cjk) { g_guiFont = cjk; g_cjk = 1; }
  }
  if (!g_guiFont && g_textType) {
    P any = ((find_obj_t)RVA(R_FINDOBJ))(g_textType, 1, 0);
    if (any && uobj_live(any)) {
      P f = ((get_font_t)RVA(R_TEXT_GETFONT))(any, 0);
      if (f && uobj_live(f)) {
        g_guiFont = f;
        g_cjk = ((has_char_t)RVA(R_FONT_HASCHAR))(f, 0x4E2D, 0) ? 1 : 0;
      }
    }
  }
  if (!g_guiFont && g_fontType) {
    P p1 = x_string_new("Arial.ttf"), p2 = x_string_new("LegacyRuntime.ttf");
    g_guiFont = ((builtin_t)RVA(R_RES_BUILTIN))(g_fontType, p1, 0);
    if (!g_guiFont) g_guiFont = ((builtin_t)RVA(R_RES_BUILTIN))(g_fontType, p2, 0);
    if (g_guiFont) g_cjk = 0;
  }
  if (!g_guiFont) { elog("ui: no usable font"); return 0; }
  if (x_gchandle_new && g_fontRooted != g_guiFont) {
    if (g_fontHandle && x_gchandle_free) x_gchandle_free((P)g_fontHandle);
    g_fontHandle = x_gchandle_new(g_guiFont, 0);
    g_fontRooted = g_guiFont;
  }

  canvasGo = new_go("UCF_HUD");
  if (!canvasGo) { elog("ui: canvas go failed"); return 0; }
  comp = ((addcomp_t)RVA(R_ADDCOMP))(canvasGo, g_canvasType, 0);
  if (!comp) { elog("ui: Canvas AddComponent failed"); return 0; }
  ((set_int1_t)RVA(R_CANVAS_MODE))(comp, 0, 0);            /* ScreenSpaceOverlay */
  ((set_int1_t)RVA(R_CANVAS_SORT))(comp, 32000, 0);
  canvasTr = get_tr(canvasGo);

  /* left-edge legend: three horizontal rows, stacked vertically */
  g_cat = mk_text_ui(canvasTr, "UCF_HUD_Cats", 0.0f, 0.5f, 0.0f, 0.5f, 14.0f, -140.0f, 520.0f, 132.0f, 26);
  root_put(g_cat);
  if (g_cat) {
    ((set_int1_t)RVA(R_TEXT_ALIGN))(g_cat, 3, 0);   /* MiddleLeft */
    g_catGo = ((get_go_t)RVA(R_GETGO))(g_cat, 0);
  }
  /* 路点菜单：左中一列，默认空；F2 / 长按 E 才填内容 */
  g_menu = mk_text_ui(canvasTr, "UCF_HUD_Menu", 0.0f, 0.5f, 0.0f, 0.5f, 14.0f, 30.0f, 560.0f, 400.0f, 16);
  root_put(g_menu);
  if (g_menu) {
    ((set_int1_t)RVA(R_TEXT_ALIGN))(g_menu, 3, 0);   /* MiddleLeft */
    g_menuGo = ((get_go_t)RVA(R_GETGO))(g_menu, 0);
  }
  /* 记下 Transform 的类对象：comp_pos 用它区分「真 Transform」和野指针 */
  if (!g_trKlass && g_cat) {
    P t = comp_tr(g_cat);
    if (t && mem_ok(t, 0x10) && uobj_live(t)) {
      g_trKlass = *(P*)t;
      elog("ui: transform klass=%p", g_trKlass);
    }
  }
  elog("ui: ready font=%p (%s) cats=%p", g_guiFont, g_cjk ? "game/CJK" : "builtin/ASCII", g_cat);
  return 1;
}

static int cat_count(int lo, int hi) {
  int i, n = 0;
  for (i = 0; i < g_vfN; i++)
    if (g_vf[i].kind == K_SPAWN && g_vf[i].aux >= lo && g_vf[i].aux <= hi) n++;
  return n;
}

static void cat_refresh(void) {
  char s[512];
  int len = 0, spawn, box, color;
  if (!g_cat) return;
  if (!g_visOn || (!g_visBorn && !g_visSupply)) {
    ((set_txt_t)RVA(R_TEXT_SETTEXT))(g_cat, x_string_new(""), 0);
    return;
  }
  s[0] = 0;
  /* 两类各自管理：只显示自己开关打开的那几行，没开的整行不出现 */
  if (g_visBorn) {
    spawn = cat_count(0, 2);   /* 幽灵出生 / 保卫者出生 / 中立点 */
    if (g_cjk) len += sprintf(s + len, "<color=#6EC6FF>出生点  %d</color>", spawn);
    else       len += sprintf(s + len, "Spawn %d", spawn);
  }
  if (g_visSupply) {
    box   = cat_count(3, 3);   /* 普通补给箱 */
    color = cat_count(4, 5);   /* 红色 / 蓝色补给箱 */
    if (g_cjk) {
      if (len) len += sprintf(s + len, "\n");
      len += sprintf(s + len, "<color=#FFD24A>普通补给箱  %d</color>", box);
      len += sprintf(s + len,
        "\n<color=#FF6FB5>红色</color><color=#B9C2CE>/</color><color=#4FE3E3>蓝色</color>"
        "<color=#EDEDED>补给箱  %d</color>", color);
    } else {
      if (len) len += sprintf(s + len, "\n");
      len += sprintf(s + len, "Ammo %d\nRed/Blue %d", box, color);
    }
  }
  ((set_txt_t)RVA(R_TEXT_SETTEXT))(g_cat, x_string_new(s), 0);
}

/* 屏幕覆盖层：只建出生点/补给箱图例和 F2 菜单；数据面板已删除，数看 ucf_mod.log */
static void overlay_refresh(void) {
  /* 大厅/房间没有 PointGraph：不建任何 UGUI 对象。 */
  if (!navfix_point_graph()) return;
  /* 换图后旧 Canvas 已被场景销毁，但 AstarPath 指针可能没变 -> editor_on_scene
   * 不会 reset。这里先验活，避免对已销毁的 UGUI Text 调 SetText 直接崩溃。 */
  if (g_cat && !uobj_live(g_cat)) {
    elog("ui: stale objects after scene change, rebuilding");
    overlay_reset();
  }
  if (!g_cat && !overlay_init()) return;
  cat_refresh();
}

static void overlay_reset(void) { g_cat = 0; g_catGo = 0; g_menu = 0; g_menuGo = 0; }

/* ---- marker store ------------------------------------------------------- */
static int add_mk(int type, V3 p, int aid, int parent, int prm, P go, P comp, P vis) {
  MK* m;
  if (g_n >= MAXM) { elog("marker store full (%d)", MAXM); return 0; }
  m = &g_mk[g_n];
  m->type = type; m->p = p; m->aid = aid; m->parent = parent; m->prm = prm;
  m->go = go; m->comp = comp; m->vis = vis;
  g_n++;
  g_visDirty = 1;      /* 新建标记后让可视化/计数下一帧重读 */
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
  elog("crouch #%d at %.2f %.2f %.2f team=%d type=%s", g_n, p.x, p.y, p.z, g_team,
       comp ? type_name(*(P*)comp) : "?");
  overlay_refresh();
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
  overlay_refresh();
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
  overlay_refresh();
  return 1;
}

/* delete marker at idx, its children, and fix every index reference */
static void del_index(int idx);
static int  save_file(void);
void editor_delete_nearest(void);          /* 定义在文件末尾；菜单里的 Delete 也走它 */

/* 从游戏自己的 List<T> 里摘掉一个元素。
 * 不调用 List.Remove：2026-11-17 的闪退就是 SpareAreaList.Remove →
 * ObjectEqualityComparer.IndexOf 碰到被写花的槽位。这里沿用 navfix.c
 * purge_guard_areas() 验证过的做法：显式 4 字节读槽位、只在需要时 4 字节搬，
 * 最后改 _size / _version，不碰泛型比较器。 */
static int list_drop_item(P list, P item) {
  P items;
  int n, i, w = 0, cap;
  if (!list || !item || !mem_ok(list, 0x14)) return 0;
  items = *(P*)((char*)list + 0x08);
  n = *(int*)((char*)list + 0x0C);
  if (!items || n <= 0 || n > 20000 || !mem_ok(items, 0x10)) return 0;
  cap = *(int*)((char*)items + 0x0C);
  if (cap <= 0 || n > cap) return 0;
  for (i = 0; i < n; i++) {
    unsigned tmp = 0;
    memcpy(&tmp, (char*)items + 0x10 + i * 4, 4);
    if ((P)tmp == item) continue;          /* 丢掉这一个 */
    if (w != i) memcpy((char*)items + 0x10 + w * 4, &tmp, 4);
    w++;
  }
  if (w == n) return 0;
  *(int*)((char*)list + 0x0C) = w;
  (*(int*)((char*)list + 0x10))++;         /* _version：让游戏的枚举/缓存失效 */
  return 1;
}

/* Destroy 之前先把组件从游戏的静态池/父列表里摘掉：
 * 否则 SpareList_BL/GR、SpareAreaList、area.posList 里还挂着已销毁的对象，
 * 人机下一次取点会拿到 Unity 假空指针，可视化也会把死点算进数量。 */
static void marker_unregister(MK* m) {
  int ra, rb;
  if (!m || !m->comp || !uobj_live(m->comp)) return;
  if (m->type == 1) {
    ra = list_drop_item(static_obj(g_crouchCls, "SpareList_BL"), m->comp);
    rb = list_drop_item(static_obj(g_crouchCls, "SpareList_GR"), m->comp);
    if (ra || rb) elog("delete: crouch removed from SpareList (%d/%d)", ra, rb);
  } else if (m->type == 2) {
    if (m->parent >= 0 && m->parent < g_n && g_mk[m->parent].type == 3) {
      P area = g_mk[m->parent].comp;
      if (area && uobj_live(area)) {
        P pl = *(P*)((char*)area + 0x10);  /* Bot_NanoGuardArea.posList */
        if (list_drop_item(pl, m->comp)) elog("delete: nanopos removed from area.posList");
      }
    }
  } else if (m->type == 3) {
    if (list_drop_item(static_obj(g_areaCls, "SpareAreaList"), m->comp))
      elog("delete: area removed from SpareAreaList");
  }
}

static void del_index(int idx) {
  MK m;
  int i;
  if (idx < 0 || idx >= g_n) return;
  /* 子项先删，且从后往前：删子项不会移动父项下标。
   * 旧实现先取 &g_mk[idx] 再 kill_children()，数组一左移，指针就指向了别人的
   * 对象——删聚集区时真正销毁的是下一个标记。 */
  for (i = g_n - 1; i > idx; i--) {
    if (g_mk[i].parent == idx) del_index(i);
  }
  m = g_mk[idx];
  marker_unregister(&m);
  if (m.vis) ((destroy_t)RVA(R_DESTROY))(m.vis, 0);
  if (m.go) ((destroy_t)RVA(R_DESTROY))(m.go, 0);
  if (m.type == 3) {
    if (m.aid >= 0 && m.aid < MAX_AID) g_aidMk[m.aid] = 0;
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
  g_visDirty = 1;      /* 让可视化/计数下一帧重读，别留着已删点的圆点 */
}

static void undo_last(void) {
  if (g_n <= 0) { elog("undo: nothing to undo"); return; }
  elog("undo: removing marker #%d type=%d", g_n - 1, g_mk[g_n - 1].type);
  del_index(g_n - 1);
  overlay_refresh();
}

static int delete_nearest(void) {
  V3 cp, fw, hp;
  int i, byRay = -1, byHit = -1, target = -1;
  float bestPerp = 1e9f, bestHit = 1e9f, bestCam = 1e9f;
  int haveHit, byCam = -1;
  if (!g_n) { elog("delete: no markers"); return 0; }
  if (!cam_ray(&cp, &fw)) { elog("delete: no camera"); return 0; }
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
  } else if (byCam >= 0 && bestCam <= 144.0f) {   /* 相机 12 m 内兜底（原来只有 4 m） */
    target = byCam;
    elog("delete: closest marker #%d to camera (%.2f m)", byCam, sqrt(bestCam));
  } else {
    elog("delete: nothing chosen (markers=%d, ray %.2f m, aim %.2f m, cam %.2f m) - aim at a marker",
         g_n,
         byRay >= 0 ? bestPerp : -1.0f,
         haveHit ? sqrt(bestHit) : -1.0f,
         byCam >= 0 ? sqrt(bestCam) : -1.0f);
    return 0;
  }
  if (target >= 0) {
    elog("delete: removing #%d type=%d at %.2f %.2f %.2f", target, g_mk[target].type,
         g_mk[target].p.x, g_mk[target].p.y, g_mk[target].p.z);
    del_index(target);
    /* 立刻落盘：editor_on_scene() 每次进图都会 load_file() 重放 markers.txt，
     * 不存盘的话删掉的点下次进图又回来了（看起来就像“删不了”）。 */
    save_file();
    overlay_refresh();
    return 1;
  }
  return 0;
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
  overlay_refresh();
}

static void make_tag(V3 p, int tag, float radius);

static int save_file(void) {
  FILE* f;
  int i, c1 = 0, c2 = 0, c3 = 0, c5 = 0;
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
    else if (g_mk[i].type == 5) c5++;
  }
  fprintf(f, "# ucf_mod markers v1  crouch=%d nanopos=%d area=%d tag=%d\n", c1, c2, c3, c5);
  fprintf(f, "# crouch <team> <x> <y> <z>\n");
  fprintf(f, "# area <scale*10> <x> <y> <z>\n");
  fprintf(f, "# nanopos <areaId> <x> <y> <z> <safety>\n");
  fprintf(f, "# tag <tag> <x> <y> <z>\n");
  for (i = 0; i < g_n; i++) {
    MK* m = &g_mk[i];
    if (m->type == 1) fprintf(f, "crouch %d %.3f %.3f %.3f\n", m->prm, m->p.x, m->p.y, m->p.z);
    else if (m->type == 3) fprintf(f, "area %d %.3f %.3f %.3f\n", m->prm, m->p.x, m->p.y, m->p.z);
    else if (m->type == 2) fprintf(f, "nanopos %d %.3f %.3f %.3f %d\n", m->aid, m->p.x, m->p.y, m->p.z, m->prm);
    else if (m->type == 5) fprintf(f, "tag %d %.3f %.3f %.3f\n", m->prm, m->p.x, m->p.y, m->p.z);
  }
  fclose(f);
  elog("saved %d markers (crouch=%d nanopos=%d area=%d tag=%d) -> %s", g_n, c1, c2, c3, c5, g_file);
  overlay_refresh();
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
      /* 文件里的队伍列要生效：make_crouch 用的是 g_team，临时切过去再还原 */
      int savedTeam = g_team;
      g_team = a ? 1 : 0;
      if (make_crouch(p)) made++;
      g_team = savedTeam;
    } else if (sscanf(line, "tag %d %f %f %f", &a, &x, &y, &z) == 4) {
      V3 p; p.x = x; p.y = y; p.z = z;
      make_tag(p, a, 3.0f);
      made++;
    }
  }
  fclose(f);
  elog("loaded %d markers from %s", made, g_file);
  overlay_refresh();
  return made;
}

static void status(void) {
  int c1 = 0, c2 = 0, c3 = 0, c5 = 0, i;
  for (i = 0; i < g_n; i++) {
    if (g_mk[i].type == 1) c1++;
    else if (g_mk[i].type == 2) c2++;
    else if (g_mk[i].type == 3) c3++;
    else if (g_mk[i].type == 5) c5++;
  }
  elog("status: edit=%d vis=%d team=%d markers=%d (crouch=%d nanopos=%d area=%d tag=%d) curAreaAid=%d ui=%d",
       g_on, g_vis, g_team, g_n, c1, c2, c3, c5,
       (g_curArea >= 0 && g_curArea < g_n) ? g_mk[g_curArea].aid : -1, g_cat ? 1 : 0);
  /* 最后一个字段是「屏幕覆盖层是否已建」：1 = 图例/菜单文字已创建 */
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
  overlay_reset();
  elog("scene: ui reset");
  vis_scene_reset();
  elog("scene: vis reset");
  roots_clear();          /* 上一张图的对象已经销毁，句柄还回去 */
  g_rootsFull = 0;
  g_sceneAge = 0;
  g_sceneReadyOnce = 0;
  g_nedGraph = 0;
  g_nedApplied = 0;
  g_nedWaitN = -1;
  g_nedHasA = 0;
  g_nedN = 0;
  /* 自由视角：上一张图的相机/虚拟相机指针已经销毁，下一帧重新找 */
  g_freeCam = 0;
  g_freeVcamGo = 0;
  g_freeVcamOff = 0;
  g_freeInited = 0;
  g_freeWarned = 0;
  g_freeBrain = 0;
  g_nedBlank = 0;
  g_nedPath[0] = 0;
  nm_seen = 0;
  elog("scene changed (astar=%p) - loading markers", astar);
  if (g_collectOnly) {
    elog("collect-only: press Ctrl+E to export, nothing is modified");
    return;
  }
  load_file();
  overlay_refresh();
}

/* called by navfix after it rebuilds the point graph */
void editor_mark_dirty(void) {
  g_visDirty = 1;
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
  sprintf(path, "%s\\navmesh_%s.bin", g_expDir, fp);
  if (nm_dump(path, &g_nmVert, &g_nmTri)) {
    elog("nm: verts=%d tris=%d tiles=%d -> %s", g_nmVert, g_nmTri, ntile, path);
    /* 这里不再 overlay_refresh()：刚进图就 set UGUI 文本是历史崩溃点之一，覆盖层下一次 tick 自己会刷 */
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
  overlay_refresh();
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
/* 清单里的改动是否还在图上（用来判断图是不是被游戏重扫掉了）。
 *
 * 关键：不能逐条独立判断。菜单切边会留下 “edge del A-B … edge add A-B”
 * 这样的历史条目；如果只看第一条，运行图里明明有 A-B，EDEL 永远认为“没删掉”，
 * 于是每 ~4 秒整图重套一次，人机刚拿到路径就被重置。
 * 这里按顺序把所有 edge 条目折叠成“每个有向 pairs 的最终期望状态”，再和运行图比。
 * 方向和先后都以文件里的最后一条为准。 */
#define NAV_EXP_MAX (NAV_ED_MAX * 2)
typedef struct { int a, b; unsigned char want; } NAVEXP;
static NAVEXP g_navExp[NAV_EXP_MAX];

static int nav_exp_add(int a, int b, int on) {
  unsigned h, k;
  int i;
  if (a < 0 || b < 0 || a == b) return 0;
  h = ((unsigned)a * 73856093u) ^ ((unsigned)b * 19349663u);
  for (k = 0; k < NAV_EXP_MAX; k++) {
    i = (int)((h + k) & (NAV_EXP_MAX - 1));
    if (g_navExp[i].a < 0) {
      g_navExp[i].a = a;
      g_navExp[i].b = b;
      g_navExp[i].want = (unsigned char)(on ? 1 : 0);
      return 0;
    }
    if (g_navExp[i].a == a && g_navExp[i].b == b) {
      g_navExp[i].want = (unsigned char)(on ? 1 : 0);
      return 0;
    }
  }
  return -1;
}
static int nav_exp_record(const NAVED* e, int ia, int ib, int on) {
  if (ia < 0 || ib < 0 || ia == ib) return 0;
  if (e->dir == 1) return nav_exp_add(ia, ib, on);
  if (e->dir == 2) return nav_exp_add(ib, ia, on);
  if (nav_exp_add(ia, ib, on) < 0) return -1;
  return nav_exp_add(ib, ia, on);
}
static int nav_exp_check(P g) {
  int i;
  for (i = 0; i < NAV_EXP_MAX; i++) {
    int has;
    if (g_navExp[i].a < 0) continue;
    has = nav_conn_has(nav_node(g, g_navExp[i].a), nav_node(g, g_navExp[i].b));
    if (has != (int)g_navExp[i].want) return 1;
  }
  return 0;
}
static int nav_needs_apply(P g) {
  int i, ia, ib, n;
  if (!g) return 0;
  n = nav_count(g);
  if (n != g_nedExpect) return 1;   /* 图被重扫/重建过：节点数不再是我们套完的样子 */
  for (i = 0; i < NAV_EXP_MAX; i++) g_navExp[i].a = -1;
  if (g_nedBlank && g_packName[0]) {
    /* 空白底图：可走的点必须全是清单里的 node add；原生点只要有一个又活了就重套。 */
    int j;
    for (i = 0; i < n; i++) {
      P nd = nav_node(g, i);
      V3 p;
      int hitAdd = 0;
      if (!nd || !nav_walk(nd)) continue;
      nav_pos(nd, &p);
      for (j = 0; j < g_nedN; j++) {
        if (g_ned[j].kind != NADD) continue;
        if (nav_d2(&g_ned[j].a, &p) <= 0.1225f) { hitAdd = 1; break; }
      }
      if (!hitAdd) return 1;
    }
    for (j = 0; j < g_nedN; j++) {
      NAVED* e = &g_ned[j];
      if (e->kind == NADD && nav_find(g, &e->a, 0.35f) < 0) return 1;
      if (e->kind != EADD && e->kind != EDEL) continue;
      ia = nav_find(g, &e->a, 0.35f);
      ib = nav_find(g, &e->b, 0.35f);
      if (ia < 0 || ib < 0) return 1;
      if (nav_exp_record(e, ia, ib, e->kind == EADD) < 0) return 1;
    }
    return nav_exp_check(g);
  }
  if (!g_nedN) return 0;
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
        if (nav_exp_record(e, ia, ib, e->kind == EADD) < 0) return 1;
      }
    }
  }
  return nav_exp_check(g);
}
/* 一个节点的连接数上限：超过就是数据坏了（A* 里最多几十条）。
 * 返回 -1 = 指针/长度不可信，0 = 没有连接，>0 = 连接数（*out 给出数组指针）。 */
#define NAV_CONN_MAX 2048
static int nav_conn_get(P nd, P* out) {
  P c;
  int n;
  if (!nd || !mem_ok(nd, 0x28)) return -1;
  c = *(P*)((char*)nd + 0x20);
  if (!c) return 0;
  if (!mem_ok(c, 0x10)) return -1;
  n = *(int*)((char*)c + 0x0C);
  if (n < 0 || n > NAV_CONN_MAX) return -1;
  if (n && !mem_ok((char*)c + 0x10, (size_t)n * 12)) return -1;
  if (out) *out = c;
  return n;
}
static int nav_conn_has(P nd, P other) {
  P c = 0;
  int n, i;
  if (!other) return 0;
  n = nav_conn_get(nd, &c);
  if (n <= 0) return 0;
  for (i = 0; i < n; i++)
    if (*(P*)((char*)c + 0x10 + i * 12) == other) return 1;
  return 0;
}
/* 把 nd.connections 换成 nc，并让 nc 一直有强根。
 * 先写字段（写屏障），再释放该槽位的旧句柄；旧数组即使马上被 GC 看到也不会
 * 在 ClearConnections 里变成悬空指针。nc=0 表示恢复成 null。 */
static void nav_conn_bind(P nd, P nc) {
  int idx;
  unsigned old = 0, h = 0;
  if (!nd) return;
  idx = *(int*)((char*)nd + 0x08);
  if (idx >= 0 && idx < NAV_MAXN) {
    old = g_connRoot[idx];
    if (nc && x_gchandle_new) h = x_gchandle_new(nc, 0);
  }
  if (x_gc_wbarrier_set_field) x_gc_wbarrier_set_field(nd, (char*)nd + 0x20, nc);
  else *(P*)((char*)nd + 0x20) = nc;
  if (idx >= 0 && idx < NAV_MAXN) {
    g_connRoot[idx] = h;
    if (old && old != h && x_gchandle_free) x_gchandle_free((P)old);
  } else if (h && x_gchandle_free) {
    x_gchandle_free((P)h);
  }
}
/* add=1 连边 / add=0 断边；返回 1 表示有改动 */
static int nav_conn_set(P nd, P other, int add) {
  P c = 0;
  int n, i, cnt = 0;
  P nc;
  V3 pa, pb;
  unsigned cost;
  if (!nd || !other || nd == other || !g_connCls || !x_array_new) return 0;
  n = nav_conn_get(nd, &c);
  if (n < 0) return 0;              /* 数据坏了：宁可不连，也不越界写 */
  if (add) {
    if (nav_conn_has(nd, other)) return 0;
    nav_pos(nd, &pa); nav_pos(other, &pb);
    cost = (unsigned)(sqrtf(nav_d2(&pa, &pb)) * 1000.0f + 0.5f);
    if (cost < 1u) cost = 1u;
    nc = x_array_new(g_connCls, (unsigned)(n + 1));
    if (!nc) return 0;
    if (n) memcpy((char*)nc + 0x10, (char*)c + 0x10, (size_t)n * 12);
    *(P*)((char*)nc + 0x10 + n * 12) = other;
    *(unsigned*)((char*)nc + 0x14 + n * 12) = cost;
    *(unsigned char*)((char*)nc + 0x18 + n * 12) = 0xFF;
  } else {
    if (!nav_conn_has(nd, other)) return 0;
    nc = x_array_new(g_connCls, (unsigned)(n - 1));
    if (!nc) return 0;
    for (i = 0; i < n; i++) {
      P t = *(P*)((char*)c + 0x10 + i * 12);
      if (t == other) continue;
      *(P*)((char*)nc + 0x10 + cnt * 12) = t;
      *(unsigned*)((char*)nc + 0x14 + cnt * 12) = *(unsigned*)((char*)c + 0x14 + i * 12);
      *(unsigned char*)((char*)nc + 0x18 + cnt * 12) = *(unsigned char*)((char*)c + 0x18 + i * 12);
      cnt++;
    }
  }
  nav_conn_bind(nd, nc);
  return 1;
}
static int nav_conn_clear(P nd) {
  P nc;
  if (!nd || !g_connCls || !x_array_new) return 0;
  nc = x_array_new(g_connCls, 0);
  if (!nc) return 0;
  nav_conn_bind(nd, nc);
  return 1;
}
/* 新建一个点；返回槽位下标，失败 -1。
 * 运行期**绝不增长 nodes 数组**：A* 的 PathHandler.pathNodes 只在 AstarPath.Awake
 * 里按「进图那一刻的节点数」分配（0x104477A0，之后 Scan 也不重建）。append 出来的点
 * nodeIndex 会超出 pathNodes 长度，寻路线程在 PointNode.Open → GetPathNode(idx) 里
 * 直接 IndexOutOfRangeException，A* 打 "Unhandled exception during pathfinding.
 * Terminating." 后寻路线程永久停摆 —— 人机从此拿不到 path，Bot.Update 第一行的
 * Move() 只能沿旧方向直着走（2026-11-16 的「复活后只会直走」就是这个）。
 * 所以这里复用第一个「不可走」的槽位：改坐标 + 标可走 + 清连接，nodeIndex 保持不变。 */
static int nav_add_node(P g, const V3* p) {
  int i, n = nav_count(g);
  if (!g || !g_connCls || !x_array_new) return -1;
  for (i = 0; i < n; i++) {
    P nd = nav_node(g, i);
    if (!nd || nav_walk(nd)) continue;
    nav_set_walk(nd, 1);
    nav_put_pos(nd, p);
    nav_conn_clear(nd);
    return i;
  }
  elog("naved: add refused: no free slot (graph full, %d nodes) - delete a node first; "
       "runtime graph must not grow (PathHandler is sized in AstarPath.Awake)", n);
  return -1;
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
  int blank = g_nedBlank && g_packName[0];
  if (!g_nedPath[0]) return;
  /* 四版纪律：正式版 nav\ 只允许控制台从 ② 开发版推过来，游戏内不许直接写 ③。
   * 想边玩边改就先选一个测试包（④ packs），或去网页编辑器改 ②。 */
  if (g_navReadOnly && !g_packName[0]) {
    if (!g_saveWarned) {
      g_saveWarned = 1;
      elog("naved: save blocked - official nav\\ is read-only (UCF_NAV_READONLY); "
           "use a test pack or the web editor (navdata\\dev)");
    }
    return;
  }
  if (!g_nedN && !blank) { DeleteFileA(g_nedPath); return; }
  f = fopen(g_nedPath, "w");
  if (!f) { elog("naved: save failed %s", g_nedPath); return; }
  fprintf(f, "# ucf-navedit v1 fp=%s\n", g_nedFp);
  if (blank) fprintf(f, "blank\n");
  for (i = 0; i < g_nedN; i++) {
    NAVED* e = &g_ned[i];
    if (e->kind == NADD)
      fprintf(f, "node add %.3f %.3f %.3f\n", e->a.x, e->a.y, e->a.z);
    else if (e->kind == NDEL)
      fprintf(f, "node del %.3f %.3f %.3f\n", e->a.x, e->a.y, e->a.z);
    else {
      const char* verb = "add";
      if (e->kind == EDEL) verb = e->dir == 1 ? "delout" : (e->dir == 2 ? "delin" : "del");
      else if (e->dir == 1) verb = "out";
      else if (e->dir == 2) verb = "in";
      fprintf(f, "edge %s %.3f %.3f %.3f %.3f %.3f %.3f\n",
              verb, e->a.x, e->a.y, e->a.z, e->b.x, e->b.y, e->b.z);
    }
  }
  fclose(f);
  elog("naved: saved %d edits -> %s%s", g_nedN, g_nedPath, blank ? " (blank base)" : "");
}
static void nav_edit_load(const char* path) {
  FILE* f = fopen(path, "r");
  char line[256];
  g_nedN = 0;
  g_redoN = 0;
  g_nedBlank = 0;
  if (!f) return;
  while (fgets(line, sizeof(line), f)) {
    NAVED e;

    float x, y, z, x2, y2, z2;
    char k1[16];
    if (line[0] == '#' || line[0] == '\n') continue;
    /* blank：测试包专用。先把原生图整张禁掉，文件里的 node add / edge add 才是唯一路线。 */
    if (!strncmp(line, "blank", 5) &&
        (line[5] == 0 || line[5] == '\r' || line[5] == '\n' || line[5] == ' ')) {
      g_nedBlank = 1;
      continue;
    }
    memset(&e, 0, sizeof(e));
    if (sscanf(line, "node %15s %f %f %f", k1, &x, &y, &z) == 4) {
      e.kind = (k1[0] == 'a') ? NADD : NDEL;
      e.a.x = x; e.a.y = y; e.a.z = z;
    } else if (sscanf(line, "edge %15s %f %f %f %f %f %f", k1, &x, &y, &z, &x2, &y2, &z2) == 7) {
      e.kind = (k1[0] == 'a' || k1[0] == 'o' || k1[0] == 'i') ? EADD : EDEL;
      e.dir = (k1[0] == 'o' || !strcmp(k1, "delout")) ? 1 :
              ((k1[0] == 'i' || !strcmp(k1, "delin")) ? 2 : 0);
      e.a.x = x; e.a.y = y; e.a.z = z;
      e.b.x = x2; e.b.y = y2; e.b.z = z2;
    } else {
      continue;
    }
    if (g_nedN < NAV_ED_MAX) g_ned[g_nedN++] = e;
  }
  fclose(f);
  elog("naved: loaded %d edits from %s%s", g_nedN, path, g_nedBlank ? " (blank base)" : "");
}
/* 按 dir 只改一个方向（0 双向 / 1 A->B / 2 B->A）。
 * 返回值：有没有真的改到连接。 */
static int nav_conn_apply(P g, const NAVED* e, int on) {
  int ia, ib, ch = 0;
  if (!g || !e) return 0;
  ia = nav_find(g, &e->a, 0.35f);
  ib = nav_find(g, &e->b, 0.35f);
  if (ia < 0 || ib < 0) return 0;
  if (e->dir == 1) {
    ch = nav_conn_set(nav_node(g, ia), nav_node(g, ib), on);
  } else if (e->dir == 2) {
    ch = nav_conn_set(nav_node(g, ib), nav_node(g, ia), on);
  } else {
    ch |= nav_conn_set(nav_node(g, ia), nav_node(g, ib), on);
    ch |= nav_conn_set(nav_node(g, ib), nav_node(g, ia), on);
  }
  return ch;
}
/* 只处理 edge 条目；返回真正改变的条数 */
static int nav_apply_edges(P g) {
  int i, ok = 0;
  for (i = 0; i < g_nedN; i++) {
    NAVED* e = &g_ned[i];
    if (e->kind != EADD && e->kind != EDEL) continue;
    if (nav_conn_apply(g, e, e->kind == EADD)) ok++;
  }
  if (ok) nav_refresh(g);
  return ok;
}

/* ---- 套用编辑清单（运行期改图的唯一安全写法）-------------------------
 * A* 的 PathHandler.pathNodes 只在 AstarPath.Awake → InitializePathProcessor
 * (0x104477A0) 里按「进图那一刻的节点数」分配一次，Scan() 和节点增减都不会重建。
 * 所以运行期绝对不能：
 *   1) 换掉 nodes 数组 / 增长 nodeCount —— 新 nodeIndex 超出 pathNodes 长度，
 *      寻路线程 PointNode.Open → GetPathNode(idx) 抛 IndexOutOfRangeException，
 *      A* 打 "Unhandled exception during pathfinding. Terminating." 后寻路线程永久
 *      停摆；之后 Seeker.StartPath 永不返回，Bot.OnPathComplete 不再触发，
 *      Bot.Update 第一行 Move() 只能沿旧方向走 —— 就是「复活后只会直直走」。
 *   2) 给被删的点写 nodeIndex = -1 —— Bot.gNode_Nearset(+0x88) / Bot.path(+0x80)
 *      等还指着它的引用一旦被 Open，GetPathNode(-1 → 0xFFFFFFFF) 同样越界炸线程。
 * 现在的做法（A* 自己的软删除语义，nodes 数组和 nodeIndex 全程不动）：
 *   删点 = 标不可走（GetNearest 用 NNConstraint.Default，constrainWalkability=1，
 *          会跳过不可走点）+ 摘掉活点里指向它的边；
 *   加点 = 复用被删掉的槽位（nodeIndex 保持原值）。
 */
static unsigned char g_navDead[NAV_MAXN];   /* 本次套用里被标死的槽位 */
static int g_navDeadN;

/* ---- 原生底图快照 / 还原 ------------------------------------------------
 * 控制台在游戏运行中切包时，先把图还原成进图时的样子，再套新包。
 * 连接只记 (nodeIndex,cost,shape)，不记 PointNode 指针：场景重建后点对象会换新，
 * 按 index 还原才不会把旧内存写进新图。 */
static void nav_base_free(void) {
  int i;
  if (g_navBase) {
    for (i = 0; i < g_navBaseN; i++) free(g_navBase[i].conn);
    free(g_navBase);
  }
  g_navBase = 0;
  g_navBaseN = 0;
  g_navBaseG = 0;
  g_navBaseFp[0] = 0;
}

/* 第一次改动之前调用；同一张图只拍一次。 */
static void nav_base_take(P g) {
  char fp[48];
  int i, n;
  if (!g) return;
  n = nav_count(g);
  if (n <= 0 || n > NAV_MAXN) return;
  nav_fp(fp, sizeof fp);
  if (g_navBase && g_navBaseG == g && g_navBaseN == n && !strcmp(g_navBaseFp, fp)) return;
  nav_base_free();
  g_navBase = (NAVBASENODE*)calloc((size_t)n, sizeof(NAVBASENODE));
  if (!g_navBase) { elog("naved: base snapshot alloc failed (%d nodes)", n); return; }
  for (i = 0; i < n; i++) {
    P nd = nav_node(g, i), c = 0;
    NAVBASENODE* s = &g_navBase[i];
    int cn, j;
    if (!nd) { s->cn = -1; continue; }
    s->walk = (unsigned char)(nav_walk(nd) ? 1 : 0);
    nav_pos(nd, &s->pos);
    cn = nav_conn_get(nd, &c);
    if (cn < 0) { s->cn = -1; continue; }
    s->cn = cn;
    if (!cn) continue;
    s->conn = (unsigned char*)malloc((size_t)cn * 12);
    if (!s->conn) { s->cn = 0; continue; }   /* 没内存就按空连接还原，宁可少边不越界 */
    for (j = 0; j < cn; j++) {
      P o = *(P*)((char*)c + 0x10 + j * 12);
      int idx = -1;
      unsigned cost = *(unsigned*)((char*)c + 0x14 + j * 12);
      unsigned char shape = *(unsigned char*)((char*)c + 0x18 + j * 12);
      if (o && mem_ok(o, 0x28)) idx = *(int*)((char*)o + 0x08);
      memcpy(s->conn + j * 12, &idx, 4);
      memcpy(s->conn + j * 12 + 4, &cost, 4);
      s->conn[j * 12 + 8] = shape;
    }
  }
  g_navBaseN = n;
  g_navBaseG = g;
  strcpy(g_navBaseFp, fp);
  elog("naved: base snapshot taken (%d nodes)", n);
}

/* 还原成快照（原生底图）。返回 1 = 已还原。 */
static int nav_base_restore(P g) {
  int i, n;
  if (!g) return 0;
  n = nav_count(g);
  if (!g_navBase || g_navBaseG != g || g_navBaseN != n) return 0;
  if (!g_connCls || !x_array_new) {
    elog("naved: restore skipped (connection class unavailable)");
    return 0;
  }
  for (i = 0; i < n; i++) {
    P nd = nav_node(g, i);
    NAVBASENODE* s = &g_navBase[i];
    if (!nd) continue;
    nav_set_walk(nd, s->walk ? 1 : 0);
    nav_put_pos(nd, &s->pos);
    if (s->cn < 0) { nav_conn_bind(nd, 0); continue; }
    if (s->cn == 0) {
      P nc0 = x_array_new(g_connCls, 0);
      if (nc0) nav_conn_bind(nd, nc0);
      continue;
    }
    {
      int j, v = 0;
      P nc;
      for (j = 0; j < s->cn; j++) {
        int idx;
        memcpy(&idx, s->conn + j * 12, 4);
        if (idx >= 0 && idx < n && nav_node(g, idx)) v++;
      }
      nc = x_array_new(g_connCls, (unsigned)v);
      if (!nc) continue;
      v = 0;
      for (j = 0; j < s->cn; j++) {
        int idx;
        P o;
        memcpy(&idx, s->conn + j * 12, 4);
        o = (idx >= 0 && idx < n) ? nav_node(g, idx) : 0;
        if (!o) continue;
        *(P*)((char*)nc + 0x10 + v * 12) = o;
        memcpy((char*)nc + 0x14 + v * 12, s->conn + j * 12 + 4, 4);
        *(unsigned char*)((char*)nc + 0x18 + v * 12) = s->conn[j * 12 + 8];
        v++;
      }
      nav_conn_bind(nd, nc);
    }
  }
  g_navDeadN = 0;
  nav_refresh(g);
  elog("naved: base restored (%d nodes)", n);
  return 1;
}

static int nav_is_dead(P nd) {
  int idx;
  if (!nd) return 0;
  idx = *(int*)((char*)nd + 0x08);
  if (idx < 0 || idx >= g_navDeadN) return 0;   /* 不认识的槽位：当作活的 */
  return g_navDead[idx];
}
/* 只保留「目标点在本次套用后仍然可走」的连接（不动 nodeIndex、不动 nodes 数组） */
static int nav_conn_filter_dead(P nd) {
  P c = 0;
  int n, i, cnt = 0;
  P nc;
  if (!g_connCls || !x_array_new) return 0;
  n = nav_conn_get(nd, &c);
  if (n < 0) { nav_conn_clear(nd); return 1; }      /* 坏表：清空，别再往下用 */
  if (n == 0) return 0;
  for (i = 0; i < n; i++) {
    P o = *(P*)((char*)c + 0x10 + i * 12);
    if (o && mem_ok(o, 0x28) && !nav_is_dead(o)) cnt++;
  }
  if (cnt == n) return 0;                           /* 没有死边：不重新分配 */
  nc = x_array_new(g_connCls, (unsigned)cnt);
  if (!nc) return 0;
  cnt = 0;
  for (i = 0; i < n; i++) {
    P o = *(P*)((char*)c + 0x10 + i * 12);
    if (!o || !mem_ok(o, 0x28) || nav_is_dead(o)) continue;
    *(P*)((char*)nc + 0x10 + cnt * 12) = o;
    *(unsigned*)((char*)nc + 0x14 + cnt * 12) = *(unsigned*)((char*)c + 0x14 + i * 12);
    *(unsigned char*)((char*)nc + 0x18 + cnt * 12) = *(unsigned char*)((char*)c + 0x18 + i * 12);
    cnt++;
  }
  nav_conn_bind(nd, nc);
  return 1;
}
/* 把一个被删掉的槽位借出来当新点用（nodeIndex 保持原值，nodes 数组不动） */
static int nav_revive_slot(P g, const V3* p) {
  int i, n = g_navDeadN;
  for (i = 0; i < n; i++) {
    P nd;
    if (!g_navDead[i]) continue;
    g_navDead[i] = 0;
    nd = nav_node(g, i);
    if (!nd) continue;
    nav_set_walk(nd, 1);
    nav_put_pos(nd, p);
    nav_conn_clear(nd);
    return i;
  }
  return -1;
}
static int nav_apply_core(P g) {
  int i, n, kill = 0, revived = 0, skipped = 0, ok = 0;
  int blank = g_nedBlank && g_packName[0];
  if (!g) return 0;
  n = nav_count(g);
  if (n <= 0) { elog("naved: graph is empty (0 nodes), nothing to edit"); return 0; }
  if (n > NAV_MAXN) { elog("naved: graph too big (%d > %d), skipped", n, NAV_MAXN); return 0; }
  memset(g_navDead, 0, (size_t)n);
  g_navDeadN = n;
  if (blank) {
    /* 空白底图：原生点全部当作已删，下一步的 node add 再从这些槽位里借点。 */
    for (i = 0; i < n; i++) g_navDead[i] = 1;
    kill = n;
    ok = n;
    elog("naved: blank base: disabled %d native nodes", n);
  }
  /* 1) 删点：只标不可走 */
  for (i = 0; i < g_nedN; i++) {
    NAVED* e = &g_ned[i];
    int k;
    if (e->kind != NDEL) continue;
    k = nav_find_any(g, &e->a, 0.35f);
    if (k >= 0 && k < n && !g_navDead[k]) { g_navDead[k] = 1; kill++; ok++; }
  }
  if (kill) {
    /* 2) 活点：摘掉指向死点的边（每点最多重分配一次连接表）。
     *    blank 底图连死点自己的边也摘掉，确保没有一条原生路线可走。 */
    for (i = 0; i < n; i++) {
      P nd;
      if (!blank && g_navDead[i]) continue;
      nd = nav_node(g, i);
      if (nd) nav_conn_filter_dead(nd);
    }
    /* 3) 死点置不可走。连接表保留：万一带野指针的 bot 指过来，nodeIndex 仍在图内，
     *    最多走到死点为止，不会越界把寻路线程炸掉。 */
    for (i = 0; i < n; i++) {
      P nd;
      if (!g_navDead[i]) continue;
      nd = nav_node(g, i);
      if (nd) nav_set_walk(nd, 0);
    }
  }
  /* 4) 加点：只借被删掉的槽位，绝不 append（append 出来的 nodeIndex 会越界） */
  for (i = 0; i < g_nedN; i++) {
    NAVED* e = &g_ned[i];
    if (e->kind != NADD) continue;
    if (nav_find(g, &e->a, 0.35f) >= 0) continue;        /* 这里已经有可走的点 */
    if (nav_revive_slot(g, &e->a) < 0) { skipped++; continue; }
    revived++; ok++;
  }
  if (!kill && !revived) return nav_apply_edges(g);       /* 只是连边/断边 */
  nav_refresh(g);
  ok += nav_apply_edges(g);
  elog("naved: applied in place: %d disabled, %d revived, %d adds skipped (graph stays %d nodes)%s",
       kill, revived, skipped, n, blank ? " [blank base]" : "");
  return ok;
}
/* 把清单套到活图上；返回实际生效条数 */
static int nav_apply_all(P g) {
  int ok = nav_apply_core(g);
  g_nedExpect = nav_count(g);
  return ok;
}
/* 撤销一条：反向操作 + 出栈；被撤销的条目进 redo 栈。 */
static void nav_undo(void) {
  P g = navfix_point_graph();
  NAVED* e;
  int ia;
  if (!g || !g_nedN) { elog("naved: nothing to undo"); return; }
  e = &g_ned[g_nedN - 1];
  if (g_redoN < NAV_ED_MAX) g_redo[g_redoN++] = *e;
  if (e->kind == NADD) {
    ia = nav_find(g, &e->a, 0.35f);
    if (ia >= 0) nav_kill_node(g, nav_node(g, ia));
  } else if (e->kind == NDEL) {
    ia = nav_find_any(g, &e->a, 0.35f);   /* 被删的点已不可走，用“任意节点”找回来 */
    if (ia >= 0) nav_set_walk(nav_node(g, ia), 1);
    else if (nav_add_node(g, &e->a) < 0) elog("naved: undo: re-add failed");
    /* 重建图时被删的点是从数组里摘掉的，撤销只能按坐标补一个空点回来，
     * 原来的连边要重新连（Ctrl+Shift+J）。 */
  } else {
    nav_conn_apply(g, e, e->kind == EDEL);
  }
  g_nedN--;
  nav_refresh(g);
  nav_save();
  elog("naved: undo -> %d edits left (redo=%d)", g_nedN, g_redoN);
}

static void nav_redo(void) {
  P g = navfix_point_graph();
  NAVED e;
  int ia;
  if (!g || !g_redoN) { elog("naved: nothing to redo"); return; }
  e = g_redo[g_redoN - 1];
  if (e.kind == NADD) {
    ia = nav_add_node(g, &e.a);
    if (ia < 0) { elog("naved: redo: add failed"); return; }
  } else if (e.kind == NDEL) {
    ia = nav_find_any(g, &e.a, 0.35f);
    if (ia >= 0) nav_kill_node(g, nav_node(g, ia));
  } else {
    nav_conn_apply(g, &e, e.kind == EADD);
  }
  if (g_nedN < NAV_ED_MAX) g_ned[g_nedN++] = e;
  g_redoN--;
  nav_refresh(g);
  nav_save();
  elog("naved: redo -> %d edits left (redo=%d)", g_nedN, g_redoN);
}
/* 删掉自己加的点时，把清单里对应的 node add / 相关边一起摘掉。
 * 否则重进图会先 node del 再 node add，点又活过来（空白底图尤其明显）。 */
static int nav_drop_add(const V3* p) {
  int i, j = 0, hit = 0;
  for (i = 0; i < g_nedN; i++) {
    NAVED* e = &g_ned[i];
    int isAdd = (e->kind == NADD && nav_d2(&e->a, p) <= 0.0025f);
    int isEdge = (e->kind == EADD || e->kind == EDEL) &&
                 (nav_d2(&e->a, p) <= 0.0025f || nav_d2(&e->b, p) <= 0.0025f);
    if (isAdd) { hit = 1; continue; }
    if (isEdge) continue;
    g_ned[j++] = *e;
  }
  g_nedN = j;
  return hit;
}
/* 记录一条编辑 + 自动保存 */
static void nav_push(int kind, const V3* a, const V3* b) {
  NAVED* e;
  if (g_nedN >= NAV_ED_MAX) { elog("naved: edit list full"); return; }
  e = &g_ned[g_nedN++];
  e->kind = kind;
  e->dir = 0;
  e->a = *a;
  if (b) e->b = *b; else memset(&e->b, 0, sizeof(e->b));
  g_redoN = 0;
  nav_save();
}
static void nav_push_dir(int kind, const V3* a, const V3* b, int dir) {
  nav_push(kind, a, b);
  if (g_nedN > 0) g_ned[g_nedN - 1].dir = dir;
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
  if (!nav_drop_add(&q)) nav_push(NDEL, &q, 0);
  else nav_save();
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
  if (ia == i) { elog("wpmenu: A and B are the same node; skip self-edge"); return; }
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
  if (!g_nedPath[0] && !g_nedN && !(g_nedBlank && g_packName[0])) {
    elog("naved: no edits for this map");
    return;
  }
  /* 从原生底图重来，再读盘：否则已经套过的 node add 会被当成“已存在”跳过，
   * 文件里删掉的点也还留在图里（控制台「重新应用」和 Ctrl+Shift+R 都走这里）。 */
  if (!nav_base_restore(g)) { elog("naved: reload aborted (no base snapshot)"); return; }
  if (g_nedPath[0]) nav_edit_load(g_nedPath);
  if (g_nedBlank && !g_packName[0]) g_nedBlank = 0;
  ops = nav_apply_all(g);           /* 内部已按需 refresh */
  elog("naved: re-applied %d/%d edits (reloaded from disk)", ops, g_nedN);
}
/* ---- 菜单动作：断边 / 落地 / 单向连边 / 标签区 / 放置 ---- */
static void menu_refresh(void);
static void nav_unlink_here(void) {
  P g = navfix_point_graph();
  V3 p, nb[64];
  int i, n, cnt = 0;
  P c = 0;
  if (!g) { elog("wpmenu: no point graph"); return; }
  if (!cam_point(&p)) { elog("wpmenu: no ground under crosshair"); return; }
  i = nav_pick(&p, 3.0f);
  if (i < 0) { elog("wpmenu: no node near crosshair"); return; }
  nav_pos(nav_node(g, i), &p);
  n = nav_conn_get(nav_node(g, i), &c);
  for (int j = 0; j < n && j < 64; j++) {
    P o = *(P*)((char*)c + 0x10 + j * 12);
    if (o) nav_pos(o, &nb[cnt++]);
  }
  for (int j = 0; j < cnt; j++) {
    int k = nav_find(g, &nb[j], 0.35f);
    if (k < 0) continue;
    nav_conn_set(nav_node(g, i), nav_node(g, k), 0);
    nav_conn_set(nav_node(g, k), nav_node(g, i), 0);
    nav_push(EDEL, &p, &nb[j]);
  }
  nav_refresh(g);
  elog("wpmenu: unlinked %d edges", cnt);
}

/* 只把点贴到地面（Y 对齐）；水平移动/写盘格式本轮不做。 */
static void nav_ground_here(void) {
  P g = navfix_point_graph();
  V3 p, q;
  int i;
  if (!g) return;
  if (!cam_point(&q)) { elog("wpmenu: no ground under crosshair"); return; }
  i = nav_pick(&q, 3.0f);
  if (i < 0) { elog("wpmenu: no node near crosshair"); return; }
  nav_pos(nav_node(g, i), &p);
  p.y = q.y + 0.05f;
  nav_put_pos(nav_node(g, i), &p);
  nav_refresh(g);
  elog("wpmenu: node grounded to y=%.2f (session only; no move format yet)", p.y);
}

/* A 已选时，把 A 和准星点按 g_wpPath 连一条边。 */
static void nav_link_one(void) {
  P g = navfix_point_graph();
  V3 p, q;
  int i, ia;
  if (!g) { elog("wpmenu: no point graph"); return; }
  if (g_wpLinkStep == 1) {
    nav_sel_a();
    if (g_nedHasA) g_wpLinkStep = 2;
    elog("wpmenu: link step=%d A=%d", g_wpLinkStep, g_nedHasA);
    return;
  }
  if (!g_nedHasA) { elog("wpmenu: select A first"); g_wpLinkStep = 1; return; }
  if (!cam_point(&p)) { elog("wpmenu: no ground under crosshair"); return; }
  i = nav_pick(&p, 3.0f);
  if (i < 0) { elog("wpmenu: no node near crosshair"); return; }
  ia = nav_find(g, &g_nedA, 1.5f);
  if (ia < 0) { elog("wpmenu: A disappeared, select again"); g_nedHasA = 0; g_wpLinkStep = 1; return; }
  if (ia == i) {
    elog("wpmenu: A and B are the same node; skip self-edge");
    g_wpLinkStep = 0;
    return;
  }
  nav_pos(nav_node(g, i), &q);
  if (g_wpPath == 1) {
    nav_conn_set(nav_node(g, ia), nav_node(g, i), 1);
    nav_conn_set(nav_node(g, i), nav_node(g, ia), 0);
    nav_push_dir(EADD, &g_nedA, &q, 1);
    elog("wpmenu: edge A->B");
  } else if (g_wpPath == 2) {
    nav_conn_set(nav_node(g, i), nav_node(g, ia), 1);
    nav_conn_set(nav_node(g, ia), nav_node(g, i), 0);
    nav_push_dir(EADD, &g_nedA, &q, 2);
    elog("wpmenu: edge B->A");
  } else {
    nav_conn_set(nav_node(g, ia), nav_node(g, i), 1);
    nav_conn_set(nav_node(g, i), nav_node(g, ia), 1);
    nav_push(EADD, &g_nedA, &q);
    elog("wpmenu: edge A<->B");
  }
  nav_refresh(g);
  g_wpLinkStep = 0;
}

/* 手动给范围内的点打 tag（不改扫描，仅当前会话；markers 里存一条 tag 记录）。 */
static void nav_set_tag(P nd, int tag) {
  unsigned fl;
  if (!nd) return;
  fl = *(unsigned*)((char*)nd + 0x0C);
  fl = (fl & ~0x1F00000u) | (((unsigned)tag & 0x1Fu) << 19);
  *(unsigned*)((char*)nd + 0x0C) = fl;
}
static void make_tag(V3 p, int tag, float radius) {
  P g = navfix_point_graph();
  int i, n, hit = 0;
  if (!g) return;
  n = nav_count(g);
  for (i = 0; i < n; i++) {
    P nd = nav_node(g, i);
    V3 q;
    if (!nd) continue;
    nav_pos(nd, &q);
    if (nav_d2(&p, &q) <= radius * radius) { nav_set_tag(nd, tag); hit++; }
  }
  add_mk(5, p, -1, -1, tag, 0, 0, spawn_vis(p, 0.30f, 5));
  elog("wpmenu: tag zone tag=%d radius=%.1f nodes=%d", tag, radius, hit);
  g_visDirty = 1;
}

/* 跳跃链接：Bot_JumpLink.Link[] 只有一个元素，endTransform 指向终点。
 * 这是本轮的唯一“新建组件”路径；session-only（pack 格式还没有 jump 行），
 * 先用 markers 的可视化球提示，下一轮再补持久化。 */
static int make_jump_link(V3 a, V3 b) {
  P endGo, startGo, comp, links, endTr, startTr, method;
  float dx = b.x - a.x, dy = b.y - a.y, dz = b.z - a.z;
  float len = sqrtf(dx * dx + dy * dy + dz * dz);
  int h = 0;
  if (!g_jumpType || !g_jumpLinkCls || !x_array_new) {
    elog("wpmenu: jump link class missing (type=%p link=%p)", g_jumpType, g_jumpLinkCls);
    return 0;
  }
  if (len < 0.2f) { elog("wpmenu: jump end too close"); return 0; }
  endGo = new_go("UCF_JumpEnd");
  if (!endGo) return 0;
  endTr = get_tr(endGo);
  if (endTr) ((set_pos_t)RVA(R_SET_POS))(endTr, b, 0);
  ((set_active_t)RVA(R_SETACTIVE))(endGo, 1, 0);

  startGo = new_go("UCF_JumpLink");
  if (!startGo) return 0;
  startTr = get_tr(startGo);
  if (startTr) ((set_pos_t)RVA(R_SET_POS))(startTr, a, 0);
  comp = ((addcomp_t)RVA(R_ADDCOMP))(startGo, g_jumpType, 0);
  if (!comp) { elog("wpmenu: Bot_JumpLink AddComponent failed"); return 0; }

  links = x_array_new(g_jumpLinkCls, 1);
  if (!links) { elog("wpmenu: Link[] alloc failed"); return 0; }
  if (x_gchandle_new) h = (int)x_gchandle_new(links, 0);
  *(P*)((char*)links + 0x10) = endTr;              /* endTransform */
  *(P*)((char*)links + 0x14) = 0;                  /* endNode (OnLatePostScan 填) */
  *(float*)((char*)links + 0x18) = 0.0f;           /* needSpeed */
  *(float*)((char*)links + 0x1C) = 1.0f;           /* accuracy */
  *(float*)((char*)links + 0x20) = dx / len;       /* direction */
  *(float*)((char*)links + 0x24) = dy / len;
  *(float*)((char*)links + 0x28) = dz / len;
  *(P*)((char*)comp + 0x24) = links;               /* links */
  ((set_active_t)RVA(R_SETACTIVE))(startGo, 1, 0);

  method = x_class_get_method_from_name ? x_class_get_method_from_name(g_jumpCls, "OnLatePostScan", 0) : 0;
  if (method && x_runtime_invoke) {
    x_runtime_invoke(method, comp, 0, 0);
    elog("wpmenu: jump link created start=(%.2f %.2f %.2f) end=(%.2f %.2f %.2f) method=%p",
         a.x, a.y, a.z, b.x, b.y, b.z, method);
  } else {
    elog("wpmenu: jump component created but OnLatePostScan missing; link inactive");
  }
  if (h && x_gchandle_free) x_gchandle_free((P)h);
  add_mk(4, a, -1, -1, 0, startGo, comp, spawn_vis(a, 0.28f, 4));
  g_visDirty = 1;
  return 1;
}

static void wp_place(void) {
  V3 p;
  if (!cam_point(&p)) { elog("wpmenu: no ground under crosshair"); return; }
  p.y += 0.05f;
  if (g_wpAutoGround) { /* cam_point already returns the ground point */ }
  switch (g_wpBrush) {
    case 0: nav_add_here(); break;
    case 1:
      if (g_nedHasA) {
        if (make_jump_link(g_nedA, p)) elog("wpmenu: jump link A -> crosshair (session only)");
      } else {
        elog("wpmenu: jump link needs A start first (Ctrl+Shift+A or path step 1)");
      }
      break;
    case 2: make_crouch(p); break;
    case 3:
      if (g_curArea >= 0 && g_curArea < g_n && g_mk[g_curArea].type == 3) {
        make_nanopos(g_mk[g_curArea].aid, p, 3);
        elog("wpmenu: guard pos added under current area aid=%d", g_mk[g_curArea].aid);
      } else {
        make_area(30, p);
        if (g_curArea >= 0) make_nanopos(g_mk[g_curArea].aid, p, 3);
        elog("wpmenu: no current area; created area + one guard pos");
      }
      break;
    case 4:
      make_area(30, p);
      break;
    case 5: make_tag(p, 7, 3.0f); break;
    default: break;
  }
  if (g_wpBrush == 2 || g_wpBrush == 3 || g_wpBrush == 4 || g_wpBrush == 5) save_file();
  overlay_refresh();
  menu_refresh();
}

/* ---- 测试包：把环境变量翻译成「读哪个目录」+ 日志一行数据来源 ------------ */
static void pack_stat(void) {
  const char* want = g_packFpLabel[0] ? g_packFpLabel : g_packFp;
  if (!g_packName[0]) {
    snprintf(g_packStat, sizeof g_packStat, "数据 正式版（nav）");
  } else if (!g_packFp[0]) {
    snprintf(g_packStat, sizeof g_packStat, "数据 测试包 %s · 不限图%s",
             g_packName, g_nedBlank ? " · 空白底图" : "");
  } else if (g_packSkip) {
    snprintf(g_packStat, sizeof g_packStat,
             "数据 测试包 %s · 只对 %s 生效 · 当前图已跳过", g_packName, want);
  } else {
    snprintf(g_packStat, sizeof g_packStat,
             "数据 测试包 %s · 只对 %s 生效 · 包内 %d 项改动%s",
             g_packName, want, g_nedN, g_nedBlank ? " · 空白底图" : "");
  }
  elog("pack data: %s", g_packStat);
}

/* 包名/指纹只允许 ASCII 字母数字 _ -：插件用 ANSI 的 CreateDirectoryA/fopen，
 * 中文路径没验证过，先在入口挡掉，别等运行期才发现打不开。 */
static int pack_ok_name(const char* s) {
  int i;
  if (!s || !s[0] || strlen(s) > 48) return 0;
  for (i = 0; s[i]; i++) {
    char c = s[i];
    if (!((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') ||
          (c >= '0' && c <= '9') || c == '_' || c == '-')) return 0;
  }
  return 1;
}

/* 逐级建目录：④ 可能在工程端，路径跨盘且多层目录不一定存在。 */
static void mkdir_p(const char* path) {
  char buf[MAX_PATH];
  int i;
  if (!path || !path[0]) return;
  strncpy(buf, path, sizeof buf - 1);
  buf[sizeof buf - 1] = 0;
  for (i = 3; buf[i]; i++) {          /* 跳过 "D:\" */
    if (buf[i] == '\\' || buf[i] == '/') {
      char c = buf[i];
      buf[i] = 0;
      CreateDirectoryA(buf, 0);
      buf[i] = c;
    }
  }
  CreateDirectoryA(buf, 0);
}

/* 环境变量优先，其次 ucf_mod.json，最后退回插件目录（旧行为）。 */
static void dir_choice(const char* envName, const char* cfgKey, const char* def,
                       char* out, int cap) {
  char buf[MAX_PATH];
  out[0] = 0;
  if (GetEnvironmentVariableA(envName, buf, sizeof buf) > 0 && buf[0]) {
    strncpy(out, buf, cap - 1);
  } else {
    cfg_str(cfgKey, "", out, cap);
    if (!out[0]) strncpy(out, def, cap - 1);
  }
  out[cap - 1] = 0;
}

static void pack_init(void) {
  char buf[160];
  g_packName[0] = g_packFp[0] = g_packFpLabel[0] = 0;
  g_packSkip = 0;
  sprintf(g_navDir, "%s\\nav", g_dir);
  if (GetEnvironmentVariableA("UCF_PACK", buf, sizeof buf) > 0 && buf[0]) {
    if (!pack_ok_name(buf)) {
      elog("pack: ignore UCF_PACK=%s (only [A-Za-z0-9_-], <=48 chars)", buf);
    } else {
      strcpy(g_packName, buf);
      mkdir_p(g_packRoot);
      sprintf(g_navDir, "%s\\%s", g_packRoot, g_packName);
      CreateDirectoryA(g_navDir, 0);
    }
  }
  if (GetEnvironmentVariableA("UCF_FP", buf, sizeof buf) > 0 && buf[0]) {
    if (pack_ok_name(buf)) strcpy(g_packFp, buf);
    else elog("pack: ignore bad UCF_FP=%s", buf);
  }
  if (GetEnvironmentVariableA("UCF_FPLABEL", buf, sizeof buf) > 0 && buf[0]) {
    strncpy(g_packFpLabel, buf, sizeof(g_packFpLabel) - 1);   /* 图名，允许中文 */
    g_packFpLabel[sizeof(g_packFpLabel) - 1] = 0;
  }
  /* 控制台命令文件：只记下当前 seq，旧命令不在新进程里重放。 */
  sprintf(g_navCmdPath, "%s\\ucf_navcmd.txt", g_dir);
  {
    FILE* f = fopen(g_navCmdPath, "r");
    if (f) {
      char line[256];
      unsigned long long s;
      while (fgets(line, sizeof line, f)) {
        if (sscanf(line, "seq=%llu", &s) == 1) g_navCmdSeq = s;
      }
      fclose(f);
    }
  }
  pack_stat();
  elog("pack: %s  dir=%s  target=%s", g_packName[0] ? g_packName : "(none / official nav)",
       g_navDir, g_packFp[0] ? g_packFp : "(any map)");
}

/* ---- 控制台命令：游戏运行中切包 / 重读 / 保存 --------------------------
 * 控制台点「载入到游戏」「重新应用」「保存路线」「回正式版」时写 ucf_navcmd.txt。
 * 这里在主线程 tick 里轮询，不在别的线程碰 Unity 对象。 */
static int nav_cmd_set_pack(P g, const char* pack, const char* fp) {
  int dirty, mapChanged;
  if (pack && pack[0] && !pack_ok_name(pack)) {
    elog("navcmd: bad pack name '%s'", pack);
    return 0;
  }
  if (fp && fp[0] && !pack_ok_name(fp)) {
    elog("navcmd: bad fp '%s'", fp);
    return 0;
  }
  dirty = g_nedApplied && (g_nedN || (g_nedBlank && g_packName[0]));
  if (g && dirty && !nav_base_restore(g)) {
    elog("navcmd: refuse switch: base snapshot unavailable (re-enter the map)");
    return 0;
  }
  mapChanged = !fp || !fp[0] || strcmp(fp, g_packFp) != 0;
  if (pack && pack[0]) {
    strcpy(g_packName, pack);
    mkdir_p(g_packRoot);
    sprintf(g_navDir, "%s\\%s", g_packRoot, g_packName);
    CreateDirectoryA(g_navDir, 0);
    if (fp && fp[0]) strcpy(g_packFp, fp);
    else g_packFp[0] = 0;
  } else {
    g_packName[0] = 0;
    g_packFp[0] = 0;
    sprintf(g_navDir, "%s\\nav", g_dir);
  }
  if (mapChanged) g_packFpLabel[0] = 0;   /* 换图后旧图名不再适用，宁可显示指纹 */
  g_packSkip = 0;
  g_nedApplied = 0;
  g_nedWaitN = -1;
  g_nedN = 0;
  g_nedBlank = 0;
  g_nedPath[0] = 0;
  g_nedExpect = 0;
  g_nedGraph = g;
  pack_stat();
  elog("navcmd: pack -> %s (fp %s)", g_packName[0] ? g_packName : "(official nav)",
       g_packFp[0] ? g_packFp : "(any map)");
  return 1;
}

static int brush_from_name(const char* name);
static void set_brush(int b);
static void menu_open(void);
static void menu_close(void);

static void nav_cmd_tick(P g) {
  FILE* f;
  char line[256];
  char cmd[24] = "";
  char pack[64] = "";
  char fp[48] = "";
  char brush[24] = "";
  char menu[8] = "";
  unsigned long long seq = 0;
  int have = 0;
  if (!g_navCmdPath[0]) return;
  f = fopen(g_navCmdPath, "r");
  if (!f) return;
  while (fgets(line, sizeof line, f)) {
    if (sscanf(line, "seq=%llu", &seq) == 1) { have = 1; continue; }
    if (sscanf(line, "cmd=%23s", cmd) == 1) continue;
    if (sscanf(line, "pack=%63s", pack) == 1) continue;
    if (sscanf(line, "fp=%47s", fp) == 1) continue;
    if (sscanf(line, "brush=%23s", brush) == 1) continue;
    if (sscanf(line, "menu=%7s", menu) == 1) continue;
  }
  fclose(f);
  if (!have || seq == g_navCmdSeq) return;
  g_navCmdSeq = seq;
  elog("navcmd: seq=%llu cmd=%s pack=%s fp=%s", seq,
       cmd[0] ? cmd : "(none)", pack[0] ? pack : "(none)", fp[0] ? fp : "(any)");
  if (!strcmp(cmd, "save")) {
    if (g_nedPath[0]) nav_save();
    else elog("navcmd: save skipped (no edit file for this map)");
    save_file();
    return;
  }
  if (!strcmp(cmd, "undo")) { nav_undo(); return; }
  if (!strcmp(cmd, "redo")) { nav_redo(); return; }
  if (!strcmp(cmd, "brush")) { set_brush(brush_from_name(brush)); return; }
  if (!strcmp(cmd, "menu")) {
    if (menu[0] == '0' || !strcmp(menu, "off")) menu_close();
    else if (menu[0] == '1' || !strcmp(menu, "on")) menu_open();
    return;
  }
  if (!strcmp(cmd, "off")) { nav_cmd_set_pack(g, "", ""); return; }
  if (!strcmp(cmd, "apply") || !strcmp(cmd, "reload")) {
    nav_cmd_set_pack(g, pack, fp);
    return;
  }
  elog("navcmd: unknown cmd '%s'", cmd);
}

/* 主线程 tick：等图稳定 -> 读本图的编辑文件 -> 套用 */
static void nav_edit_tick(void) {
  P g;
  int n, ops;
  if (g_collectOnly || !ed_init()) return;
  g = navfix_point_graph();
  nav_cmd_tick(g);            /* 控制台命令：运行中切包 / 重读 / 保存 */
  if (!g) { g_nedGraph = 0; g_nedApplied = 0; g_nedWaitN = -1; return; }
  if (g != g_nedGraph) {
    g_nedGraph = g;
    g_nedApplied = 0;
    g_nedWaitN = -1;
    g_nedHasA = 0;
    g_nedN = 0;
    g_nedBlank = 0;
    g_nedPath[0] = 0;
    g_packSkip = 0;      /* 换图：让下一张图重新判断一次，并在日志里各记一行 */
    nav_base_free();     /* 旧图的快照只对旧图有效 */
  }
  n = nav_count(g);
  if (!g_nedApplied) {
    if (n <= 0) return;
    if (n != g_nedWaitN) { g_nedWaitN = n; return; }       /* 等两跳稳定 */
    nav_fp(g_nedFp, sizeof(g_nedFp));
    /* 测试包只对一张图生效：指纹不符就整包跳过（宁可不动，也别改错图） */
    if (g_packFp[0] && strcmp(g_packFp, g_nedFp) != 0) {
      if (!g_packSkip) {
        g_packSkip = 1;
        elog("pack: skip %s (want fp %s, current %s)", g_packName, g_packFp, g_nedFp);
        pack_stat();
      }
      g_nedPath[0] = 0;
      g_nedBlank = 0;
      nav_base_take(g);      /* 跳过也拍一张：之后运行中切到匹配的包还能还原 */
      g_nedApplied = 1;      /* 本次进图不再重试；换图时 g_nedGraph 变了会重来 */
      return;
    }
    if (g_packSkip) { g_packSkip = 0; pack_stat(); }
    CreateDirectoryA(g_dir, 0);
    CreateDirectoryA(g_navDir, 0);
    sprintf(g_nedPath, "%s\\%s.txt", g_navDir, g_nedFp);
    nav_base_take(g);     /* 先拍原生底图，再套文件；切包时才能还原 */
    nav_edit_load(g_nedPath);
    if (g_nedBlank && !g_packName[0]) {
      g_nedBlank = 0;
      elog("naved: ignore blank (only a test pack may blank the base)");
    }
    g_nedBaseN = n;
    ops = nav_apply_all(g);
    g_nedApplied = 1;
    pack_stat();
    if (ops) elog("naved: applied %d/%d edits on %s (nodes %d -> %d)%s",
                  ops, g_nedN, g_nedFp, g_nedBaseN, nav_count(g),
                  g_nedBlank ? " [blank base]" : "");
    else elog("naved: no edit file for %s (dir %s)", g_nedFp, g_navDir);
    return;
  }
  /* 图被游戏重扫/重建过 -> 改动没了，重新套用（每 ~1 s 检查一次） */
  if (g_nedN || (g_nedBlank && g_packName[0])) {
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

/* autotest.c 用：把当前地图的中文名读出来（读不到就留空） */
void editor_map_name(char* out, int cap) {
  if (!out || cap <= 0) return;
  out[0] = 0;
  if (!g_inited) return;
  map_name_from_minimap(out, cap);
}

/* main-thread tick: keeps the labels glued to their world positions */
/* ======================= 路点菜单（SyPB 式） =======================
 * F2 开关；长按 E 0.45 s 也可（UCF 没有 E 交互，先按用户确认）。
 * 菜单只做「选操作 → 调已有的 naved / make_* 函数」，不改游戏行为层。
 */
static const char* WP_MENU[10] = {
  "添加路点", "设置笔刷 / 标记", "建立路径", "删除路径 / 路点", "删除标记（准星最近）",
  "落地 / 贴地", "聚集区工具", "撤销 / 保存", "显示图层", "关闭菜单"
};
static const char* WP_TYPES[6] = {
  "普通路点", "跳跃点", "蹲守点", "守点", "聚集区", "标签区"
};
static const char* WP_PATHS[3] = { "双向", "单向 A -> B", "单向 B -> A" };
static const char* WP_AREAS[4] = {
  "新建聚集区", "加守点", "加入口 entrancePos", "加逃跑点 escapePos"
};
static const char* WP_EDIT[4] = { "撤销一步", "重做一步", "保存到文件", "重读并套用" };
static const char* WP_LAYERS[3] = { "路点/连线", "可走面", "路点总开关" };
static const char* WP_DEL[2] = { "删除路径（A-B 连线）", "删除路点（A* 节点）" };

/* 小键盘键码：mingw 的 winuser.h 一般都有；老头文件缺失时兜底。 */
#ifndef VK_NUMPAD0
#define VK_NUMPAD0 0x60
#define VK_NUMPAD1 0x61
#define VK_NUMPAD2 0x62
#define VK_NUMPAD3 0x63
#define VK_NUMPAD4 0x64
#define VK_NUMPAD5 0x65
#define VK_NUMPAD6 0x66
#define VK_NUMPAD7 0x67
#define VK_NUMPAD8 0x68
#define VK_NUMPAD9 0x69
#endif

static void wp_place(void);
static void nav_unlink_here(void);
static void nav_ground_here(void);
static void nav_link_one(void);
static void nav_redo(void);

static void menu_sub_title(char* out, int cap) {
  const char* s = "路点菜单";
  if (g_wpMenuSub == 1) s = "添加路点：选类型";
  else if (g_wpMenuSub == 2) s = "建立路径：选方向";
  else if (g_wpMenuSub == 3) s = "聚集区工具";
  else if (g_wpMenuSub == 4) s = "撤销 / 保存";
  else if (g_wpMenuSub == 5) s = "显示图层";
  else if (g_wpMenuSub == 6) s = "删除：选类型";
  snprintf(out, (size_t)cap, "%s", s);
}

static int menu_sub_count(void) {
  if (g_wpMenuSub == 1) return 6;
  if (g_wpMenuSub == 2) return 3;
  if (g_wpMenuSub == 3) return 4;
  if (g_wpMenuSub == 4) return 4;
  if (g_wpMenuSub == 5) return 3;
  if (g_wpMenuSub == 6) return 2;
  return 10;
}

static const char* menu_sub_label(int i) {
  if (g_wpMenuSub == 1) return (i >= 0 && i < 6) ? WP_TYPES[i] : "";
  if (g_wpMenuSub == 2) return (i >= 0 && i < 3) ? WP_PATHS[i] : "";
  if (g_wpMenuSub == 3) return (i >= 0 && i < 4) ? WP_AREAS[i] : "";
  if (g_wpMenuSub == 4) return (i >= 0 && i < 4) ? WP_EDIT[i] : "";
  if (g_wpMenuSub == 5) return (i >= 0 && i < 3) ? WP_LAYERS[i] : "";
  if (g_wpMenuSub == 6) return (i >= 0 && i < 2) ? WP_DEL[i] : "";
  return "";
}

static void menu_refresh(void) {
  char s[2048];
  char title[64];
  int i, n, off = 0;
  if (g_menu && !uobj_live(g_menu)) overlay_reset();
  if (!g_menu) return;
  if (!g_wpMenuOn || !g_wpMenuOpen) {
    ((set_txt_t)RVA(R_TEXT_SETTEXT))(g_menu, x_string_new(""), 0);
    return;
  }
  menu_sub_title(title, sizeof title);
  off += snprintf(s + off, sizeof s - (size_t)off,
                  "%s   [F2/长按E 关] [Delete 删标记]\n", title);
  if (g_wpMenuSub == 0) {
    for (i = 0; i < 10 && off < (int)sizeof s - 80; i++) {
      off += snprintf(s + off, sizeof s - (size_t)off, "%s%d  %s\n",
                      i == g_wpMenuSel ? "> " : "  ", (i + 1) % 10, WP_MENU[i]);
    }
  } else {
    n = menu_sub_count();
    for (i = 0; i < n && off < (int)sizeof s - 80; i++) {
      off += snprintf(s + off, sizeof s - (size_t)off, "%s%d  %s\n",
                      i == g_wpMenuSubSel ? "> " : "  ", i + 1, menu_sub_label(i));
    }
  }
  if (g_wpArm) {
    off += snprintf(s + off, sizeof s - (size_t)off, "\n[%s] 小键盘5 / 左键 放置\n", WP_TYPES[g_wpBrush]);
  } else if (g_wpLinkStep == 1) {
    off += snprintf(s + off, sizeof s - (size_t)off, "\n对准起点，小键盘5 选 A\n");
  } else if (g_wpLinkStep == 2) {
    off += snprintf(s + off, sizeof s - (size_t)off, "\nA 已选，对准终点，小键盘5 连边\n");
  } else {
    off += snprintf(s + off, sizeof s - (size_t)off, "\n当前笔刷: %s  A: %s\n",
                    WP_TYPES[g_wpBrush], g_nedHasA ? "已选" : "未选");
  }
  if (off < (int)sizeof s - 80)
    off += snprintf(s + off, sizeof s - (size_t)off, "小键盘 8/2 上下   5 确认   0 返回   1-9 直选\n");
  ((set_txt_t)RVA(R_TEXT_SETTEXT))(g_menu, x_string_new(s), 0);
}

static void menu_open(void) {
  if (!g_wpMenuOn) { elog("wpmenu: disabled by cfg wp_menu=0"); return; }
  if (g_collectOnly) { elog("wpmenu: collect-only, menu disabled"); return; }
  if (g_menu && !uobj_live(g_menu)) overlay_reset();
  if (!g_menu) overlay_init();
  g_wpMenuOpen = 1;
  g_wpMenuSel = 0;
  g_wpMenuSub = 0;
  g_wpMenuSubSel = 0;
  g_wpArm = 0;
  g_wpLinkStep = 0;
  elog("wpmenu: open");
  menu_refresh();
}

static void menu_close(void) {
  if (!g_wpMenuOpen) return;
  g_wpMenuOpen = 0;
  g_wpArm = 0;
  g_wpLinkStep = 0;
  g_wpMenuSub = 0;
  elog("wpmenu: close");
  menu_refresh();
}

static void menu_toggle(void) {
  if (g_wpMenuOpen) menu_close(); else menu_open();
}

static void menu_back(void) {
  if (g_wpArm || g_wpLinkStep) {
    g_wpArm = 0;
    g_wpLinkStep = 0;
    g_nedHasA = 0;
    elog("wpmenu: placement cancelled");
    menu_refresh();
    return;
  }
  if (g_wpMenuSub) { g_wpMenuSub = 0; g_wpMenuSubSel = 0; menu_refresh(); return; }
  menu_close();
}

static void menu_move(int delta) {
  int n = g_wpMenuSub ? menu_sub_count() : 10;
  if (!n) return;
  if (g_wpMenuSub) g_wpMenuSubSel = (g_wpMenuSubSel + delta + n) % n;
  else g_wpMenuSel = (g_wpMenuSel + delta + n) % n;
  elog("wpmenu: %s=%d", g_wpMenuSub ? "subsel" : "sel",
       g_wpMenuSub ? g_wpMenuSubSel : g_wpMenuSel);
  menu_refresh();
}

static int brush_from_name(const char* name) {
  if (!name) return 0;
  if (!strcmp(name, "jump")) return 1;
  if (!strcmp(name, "crouch")) return 2;
  if (!strcmp(name, "guard")) return 3;
  if (!strcmp(name, "area")) return 4;
  if (!strcmp(name, "tag")) return 5;
  return 0;
}

static const char* brush_name(int b) {
  static const char* n[6] = { "normal", "jump", "crouch", "guard", "area", "tag" };
  return (b >= 0 && b < 6) ? n[b] : "normal";
}

static void set_brush(int b) {
  if (b < 0 || b > 5) b = 0;
  g_wpBrush = b;
  strncpy(g_wpBrushName, brush_name(b), sizeof g_wpBrushName - 1);
  g_wpBrushName[sizeof g_wpBrushName - 1] = 0;
  elog("wpmenu: brush=%s", g_wpBrushName);
  menu_refresh();
}

/* 菜单确认：主菜单进子菜单 / 子菜单执行；不关菜单，便于连续操作。 */
static void menu_activate(void) {
  int i;
  if (g_wpMenuSub == 0) {
    if (g_wpArm || g_wpLinkStep) {
      g_wpArm = 0;
      g_wpLinkStep = 0;
      g_nedHasA = 0;
      elog("wpmenu: placement cancelled by menu");
    }
    i = g_wpMenuSel;
    if (i == 0) { g_wpMenuSub = 1; g_wpMenuSubSel = g_wpBrush; menu_refresh(); return; }
    if (i == 1) { g_wpMenuSub = 1; g_wpMenuSubSel = g_wpBrush; menu_refresh(); return; }
    if (i == 2) { g_wpMenuSub = 2; g_wpMenuSubSel = g_wpPath; menu_refresh(); return; }
    if (i == 3) { g_wpMenuSub = 6; g_wpMenuSubSel = 0; menu_refresh(); return; }
    if (i == 4) {
      /* 和游戏内 Delete 键同一条路径：删准星最近的那个标记
       * （蹲守点 / 幽灵守点 / 聚集区 / 跳跃链接）。A* 路点的删除在
       * 「删除路径 / 路点」子菜单里，两边分开，不会互相误删。 */
      if (!delete_nearest())
        elog("wpmenu: 准星附近没有可删的标记（蹲守/守点/聚集区/跳链）");
      menu_refresh();
      return;
    }
    if (i == 5) { nav_ground_here(); menu_refresh(); return; }
    if (i == 6) { g_wpMenuSub = 3; g_wpMenuSubSel = 0; menu_refresh(); return; }
    if (i == 7) { g_wpMenuSub = 4; g_wpMenuSubSel = 0; menu_refresh(); return; }
    if (i == 8) { g_wpMenuSub = 5; g_wpMenuSubSel = 0; menu_refresh(); return; }
    if (i == 9) { menu_close(); return; }
    return;
  }
  i = g_wpMenuSubSel;
  if (g_wpMenuSub == 1) {                 /* 类型 */
    set_brush(i);
    g_wpMenuSub = 0;
    g_wpArm = 1;
    menu_refresh();
    return;
  }
  if (g_wpMenuSub == 2) {                 /* 路径方向 */
    g_wpPath = i;
    g_wpMenuSub = 0;
    g_wpLinkStep = 1;
    g_nedHasA = 0;
    elog("wpmenu: path dir=%d, select A first", g_wpPath);
    menu_refresh();
    return;
  }
  if (g_wpMenuSub == 3) {                 /* 聚集区 */
    V3 p;
    if (!cam_point(&p)) { elog("wpmenu: no ground under crosshair"); return; }
    p.y += 0.05f;
    if (i == 0) { make_area(30, p); }
    else if (i == 1) {
      if (g_curArea >= 0 && g_curArea < g_n && g_mk[g_curArea].type == 3)
        make_nanopos(g_mk[g_curArea].aid, p, 3);
      else { make_area(30, p); if (g_curArea >= 0) make_nanopos(g_mk[g_curArea].aid, p, 3); }
    } else {
      elog("wpmenu: entrance/escape not wired yet");
    }
    save_file();
    menu_refresh();
    return;
  }
  if (g_wpMenuSub == 4) {                 /* 撤销 / 保存 */
    if (i == 0) nav_undo();
    else if (i == 1) nav_redo();
    else if (i == 2) nav_save();
    else nav_reapply();
    menu_refresh();
    return;
  }
  if (g_wpMenuSub == 5) {                 /* 显示 */
    if (i == 0) vis_toggle_nodes();
    else if (i == 1) nm_toggle();
    else vis_toggle();
    menu_refresh();
    return;
  }
  if (g_wpMenuSub == 6) {                 /* 删除：路径 / 路点 */
    if (i == 0) nav_unlink_here();
    else nav_del_here();
    g_wpMenuSub = 0;
    menu_refresh();
    return;
  }
}

/* 菜单打开时，Enter / 左键：先放点，再执行当前项 */
static void menu_confirm(void) {
  if (!g_wpMenuOpen) return;
  if (g_wpArm) { wp_place(); menu_refresh(); return; }
  if (g_wpLinkStep) { nav_link_one(); menu_refresh(); return; }
  menu_activate();
}

/* 菜单打开时：菜单键（数字/回车/Esc/小键盘等）先在插件里处理并吞掉；
 * 移动键 W/A/S/D/空格/Shift/Ctrl 留给游戏（选完 A 要能走到 B 再连边）；
 * 其余游戏键（Q/R/G/F/Tab 等）拦掉，避免菜单开着时误触。
 * 2026-11-18 二次调整：用户反馈 Enter/Esc/W/S 与游戏内按键冲突；
 * 菜单主操作改为小键盘 8/2/5/0，W/S 不再控制菜单。 */
static int menu_sys_key(unsigned vk) {
  if (vk == VK_SHIFT || vk == VK_CONTROL || vk == VK_MENU) return 1;
  if (vk == VK_LWIN || vk == VK_RWIN || vk == VK_APPS) return 1;
  if (vk == VK_CAPITAL || vk == VK_NUMLOCK || vk == VK_SCROLL) return 1;
  if (vk == VK_SNAPSHOT) return 1;
  /* Tab/F4/Enter/Space 的 Alt 组合放行；普通 Tab/F4/Enter 仍归菜单，
   * 普通 Space 在下面当移动键放行（跳跃）。 */
  if (vk == VK_TAB || vk == VK_F4 || vk == VK_SPACE || vk == VK_RETURN)
    return (GetAsyncKeyState(VK_MENU) & 0x8000) ? 1 : 0;
  return 0;
}

int editor_menu_key(unsigned vk, int ext) {
  (void)ext;
  /* Win 组合键交给系统（Win+L / Win+Tab 等） */
  if ((GetAsyncKeyState(VK_LWIN) & 0x8000) || (GetAsyncKeyState(VK_RWIN) & 0x8000))
    return 0;
  if (vk == VK_F2) { menu_toggle(); return 1; }
  if (vk == 'E') {
    if (g_wpMenuOn && !g_wpEDownAt) { g_wpEDownAt = GetTickCount(); g_wpEFired = 0; }
    return 1;   /* UCF 没有 E 交互；E 只给菜单长按 */
  }
  if (!g_wpMenuOpen) return 0;
  /* Ctrl+Shift+Esc 留给任务管理器 */
  if (vk == VK_ESCAPE &&
      (GetAsyncKeyState(VK_CONTROL) & 0x8000) &&
      (GetAsyncKeyState(VK_SHIFT) & 0x8000)) return 0;
  if (menu_sys_key(vk)) return 0;

  /* 菜单开着时旧版把其余键全部吞掉：Delete 根本到不了编辑器，蹲守点就“删不了”。
   * 这里直接走和游戏内 Delete 同一条路径。 */
  if (vk == VK_DELETE) { editor_delete_nearest(); return 1; }

  if (vk == VK_NUMPAD8 || vk == VK_UP) { menu_move(-1); return 1; }
  if (vk == VK_NUMPAD2 || vk == VK_DOWN) { menu_move(1); return 1; }
  if (vk == VK_NUMPAD5 || vk == VK_CLEAR || vk == VK_RETURN) { menu_confirm(); return 1; }
  if (vk == VK_NUMPAD0 || vk == VK_INSERT || vk == VK_BACK || vk == VK_ESCAPE) {
    menu_back();
    return 1;
  }
  if (vk >= '0' && vk <= '9') {
    int i = (int)(vk - '1');
    if (vk == '0') {
      if (g_wpMenuSub) menu_back();
      else { g_wpMenuSel = 9; menu_activate(); }
      return 1;
    }
    if (g_wpMenuSub) {
      if (i < menu_sub_count()) { g_wpMenuSubSel = i; menu_activate(); }
    } else if (i >= 0 && i < 10) {
      g_wpMenuSel = i;
      menu_activate();
    }
    return 1;
  }
  /* 移动键留给游戏：选完 A 可以走到 B，再按小键盘5 连边。
   * 只拦菜单键和会误触的武器/功能键（Q/R/G/F/Tab/小键盘等）。 */
  if (vk == 'W' || vk == 'A' || vk == 'S' || vk == 'D' ||
      vk == VK_SPACE || vk == VK_SHIFT || vk == VK_CONTROL) return 0;
  return 1;
}

/* 兼容旧调用：WM_APP+0x53 测试钩子仍走这里 */
void editor_on_key_plain(unsigned vk) { (void)editor_menu_key(vk, 0); }

void editor_on_mouse(int btn) {
  if (!g_wpMenuOpen) return;
  if (btn == 1) menu_confirm();
  else if (btn == 2) menu_back();
}

void editor_menu_wheel(int delta) {
  if (!g_wpMenuOpen) return;
  menu_move(delta > 0 ? -1 : 1);
}

int editor_menu_is_open(void) { return g_wpMenuOpen; }


/* 每 tick：长按 E 计时 + 菜单文本刷新（0.3 s 一次） */
static void menu_tick(void) {
  static int tick;
  tick++;
  if (g_collectOnly) { g_wpMenuOpen = 0; return; }
  if (g_wpMenuOn && g_wpEDownAt && !g_wpEFired) {
    if (!(GetAsyncKeyState('E') & 0x8000)) g_wpEDownAt = 0;
    else if (GetTickCount() - g_wpEDownAt >= 450) {
      g_wpEFired = 1;
      menu_toggle();
    }
  }
  if (g_wpMenuOpen && (tick % 3) == 0) menu_refresh();
}

/* ---- 2026-11-19 人机巡线驱动 -------------------------------------------------
 * 证据（blank_b 实测）：bot.path=0、enemy=0、crouchList BL=9/GR=9、
 * gameRoundOver=0——游戏 AI 不给目的地，人机全程原地。
 * 这里对没有 path 的 bot 用 Seeker.StartPath 沿本图可走点下一条路径，
 * 算完调用 Bot.OnPathComplete 装车；AI 自己有目标/有敌人时不抢。
 * 只在测试包（blank）里生效，正常游戏一行不执行。 */
#define R_SEEK_STARTPATH 0x5A4260
#define R_BOT_ONPATH    0xB31950
typedef P    (*seek_start_t)(P seeker, V3 start, V3 end, P cb, void* mi);
typedef void (*bot_onpath_t)(P bot, P path, void* mi);

static P g_prBotCls, g_prBotType, g_prStopFld;
static int pr_readable(P p, size_t n);
typedef struct { P bot; V3 p; unsigned t; } BPOS;
static BPOS g_bp[32];

typedef struct { P bot, path; unsigned h; unsigned next; } DRV;
static DRV g_drv[32];

static void drv_release(DRV* d) {
  if (d->h && x_gchandle_free) x_gchandle_free((P)(size_t)d->h);
  d->path = 0; d->h = 0;
}

static void drive_tick(void) {
  static int on = -1;
  P arr, g = navfix_point_graph();
  int n, i, j, nn2;
  unsigned now = GetTickCount();
  if (on < 0) on = cfg_bool("bot_drive", 0) ? 1 : 0;   /* 默认关：先复现原版 AI 的目标来源 */
  if (!on || !g || !g_nedBlank || !g_packName[0]) return;
  if (!g_prBotType || g_sceneAge < 12) return;
  nn2 = nav_count(g);
  if (nn2 <= 0) return;
  for (j = 0; j < 32; j++) {
    if (g_drv[j].bot && !uobj_live(g_drv[j].bot)) {
      drv_release(&g_drv[j]); g_drv[j].bot = 0;
    }
  }
  arr = ((find_objs_t)RVA(R_FINDOBJS))(g_prBotType, 1, 0);
  if (!arr) return;
  n = *(int*)((char*)arr + 0x0C);
  if (n > 32) n = 32;
  for (i = 0; i < n; i++) {
    P b = *(P*)((char*)arr + 0x10 + i * 4);
    P tr, path, seeker, ei, enemy;
    DRV* d = 0;
    V3 bp;
    int cand[64], nc = 0;
    if (!b || !uobj_live(b)) continue;
    for (j = 0; j < 32; j++) if (g_drv[j].bot == b) { d = &g_drv[j]; break; }
    if (!d) for (j = 0; j < 32; j++) if (!g_drv[j].bot) { d = &g_drv[j]; d->bot = b; break; }
    if (!d) continue;
    path = *(P*)((char*)b + 0x80);
    if (path) { if (d->path) drv_release(d); d->next = now + 500; continue; }
    ei = *(P*)((char*)b + 0x28);
    enemy = (pr_readable(ei, 0x40) && pr_readable(*(P*)((char*)ei + 0x0C), 0x30))
              ? *(P*)((char*)ei + 0x0C) : 0;
    if (enemy) { if (d->path) drv_release(d); d->next = now + 500; continue; }
    if (d->path) {
      int st = pr_readable(d->path, 0x40) ? *(int*)((char*)d->path + 0x20) : -1;
      P lst = pr_readable(d->path, 0x40) ? *(P*)((char*)d->path + 0x2C) : 0;
      int pts = pr_readable(lst, 0x20) ? *(int*)((char*)lst + 0xC) : -1;
      if ((st == 2 || st == 3) && pts > 0) {
        ((bot_onpath_t)RVA(R_BOT_ONPATH))(b, d->path, 0);
        elog("drive: adopt bot=%p pts=%d", b, pts);
        drv_release(d); d->next = now + 700;
      } else if (now > d->next) {
        drv_release(d); d->next = now + 1500;
      }
      continue;
    }
    if (now < d->next) continue;
    tr = ((get_tr_t)RVA(R_COMP_TR))(b, 0);
    if (!tr) continue;
    ((get_pos_t)RVA(R_GET_POS_INJ))(tr, &bp, 0);
    seeker = *(P*)((char*)b + 0x78);
    if (!seeker) continue;
    /* 选一个离自己 >20m、在对侧的可走点当目标 */
    for (j = 0; j < nn2 && nc < 64; j++) {
      P nd = nav_node(g, j);
      V3 q;
      float dx, dz, dd;
      if (!nd || !nav_walk(nd)) continue;
      nav_pos(nd, &q);
      dx = q.x - bp.x; dz = q.z - bp.z; dd = dx * dx + dz * dz;
      if (dd < 400.0f) continue;
      if (bp.x > 0.0f ? (q.x > bp.x + 5.0f) : (q.x < bp.x - 5.0f)) continue;
      cand[nc++] = j;
    }
    if (!nc) continue;
    {
      V3 tp;
      P pth;
      nav_pos(nav_node(g, cand[(now + (unsigned)(size_t)b) % (unsigned)nc]), &tp);
      pth = ((seek_start_t)RVA(R_SEEK_STARTPATH))(seeker, bp, tp, 0, 0);
      if (pth) {
        d->path = pth;
        d->h = x_gchandle_new ? x_gchandle_new(pth, 0) : 0;
        d->next = now + 4000;
      } else {
        d->next = now + 2000;
      }
      elog("drive: ask bot=%p -> (%.1f,%.1f) path=%p", b, tp.x, tp.z, pth);
    }
  }
}

/* ---- 2026-11-19 人机探针：排查「路线通了人机还是不动」 -----------------
 * 每 ~5 s 打一行：AstarPath 的吸附半径、bot 数、前 3 个 bot 的位置 /
 * 最近可走节点距离 / 当前 path 点数 / 敌人 / stopAllBot。
 * ucf_mod.json 里 "bot_probe": false 可关。 */
static int g_prOn = -1;

static int pr_readable(P p, size_t n) {
  MEMORY_BASIC_INFORMATION m;
  if (!p) return 0;
  if (!VirtualQuery(p, &m, sizeof m)) return 0;
  (void)n;
  return m.State == MEM_COMMIT && !(m.Protect & (PAGE_NOACCESS | PAGE_GUARD));
}

static int pr_walk_count(P g) {
  int n = g ? nav_count(g) : 0, i, c = 0;
  for (i = 0; i < n; i++) { P nd = nav_node(g, i); if (nd && nav_walk(nd)) c++; }
  return c;
}

static float pr_near_walk(P g, const V3* p, P* out) {
  int n = g ? nav_count(g) : 0, i;
  float best = 1e9f;
  P bn = 0;
  for (i = 0; i < n; i++) {
    P nd = nav_node(g, i);
    V3 q;
    float dx, dy, dz, d;
    if (!nd || !nav_walk(nd)) continue;
    nav_pos(nd, &q);
    dx = q.x - p->x; dy = q.y - p->y; dz = q.z - p->z;
    d = dx * dx + dy * dy + dz * dz;
    if (d < best) { best = d; bn = nd; }
  }
  if (out) *out = bn;
  return bn ? sqrtf(best) : -1.0f;
}

static void bot_probe(void) {
  P arr, g = navfix_point_graph();
  unsigned char st = 0;
  int n, i, cnt = 0, shown = 0;
  if (g_prOn < 0) g_prOn = cfg_bool("bot_probe", 1) ? 1 : 0;
  if (!g_prOn) return;
  /* 场景刚切完的头几帧别碰 walkable 节点数组；12 tick ≈ 3 s 后连接表已重建 */
  if (g_sceneAge < 12) return;
  if (!g_prBotType) {
    g_prBotCls = find_cls("", "Bot");
    if (!g_prBotCls || !x_class_get_type) { elog("probe: Bot class not found"); g_prOn = 0; return; }
    g_prBotType = x_type_get_object ? x_type_get_object(x_class_get_type(g_prBotCls)) : 0;
    if (x_class_get_field_from_name) g_prStopFld = x_class_get_field_from_name(g_prBotCls, "stopAllBot");
    if (!g_prBotType) { elog("probe: Bot type missing"); g_prOn = 0; return; }
  }
  if (g_prStopFld && x_field_static_get_value) x_field_static_get_value(g_prStopFld, &st);
  /* 蹲点静态表：我们建的 18 个点有没有被游戏收进 SpareList_BL/GR */
  {
    P ccls = find_cls("", "Bot_CrouchPos");
    if (ccls && x_class_get_field_from_name && x_field_static_get_value) {
      P fb = x_class_get_field_from_name(ccls, "SpareList_BL");
      P fg = x_class_get_field_from_name(ccls, "SpareList_GR");
      P lb = 0, lg = 0;
      if (fb) x_field_static_get_value(fb, &lb);
      if (fg) x_field_static_get_value(fg, &lg);
      elog("probe: crouchList BL=%d GR=%d",
           pr_readable(lb, 0x20) ? *(int*)((char*)lb + 0xC) : -1,
           pr_readable(lg, 0x20) ? *(int*)((char*)lg + 0xC) : -1);
    }
  }
  /* 回合状态：gameRoundOver 为真时游戏会停掉人机的寻路/行动 */
  {
    P gcls = find_cls("", "GameManager");
    P ff = (gcls && x_class_get_field_from_name)
             ? x_class_get_field_from_name(gcls, "<gameRoundOver>k__BackingField") : 0;
    unsigned char ro = 0;
    if (ff && x_field_static_get_value) {
      x_field_static_get_value(ff, &ro);
      elog("probe: gameRoundOver=%d", (int)ro);
    }
  }
  {
    P acls = find_cls("", "AstarPath"), af, a = 0;
    if (acls && x_class_get_field_from_name && x_field_static_get_value) {
      af = x_class_get_field_from_name(acls, "active");
      if (af) x_field_static_get_value(af, &a);
      if (a) elog("probe: astar=%p maxNearest=%.2f fullGetNearest=%d scanOnStart=%d walk=%d/%d",
                  a, *(float*)((char*)a + 0x30), *(unsigned char*)((char*)a + 0x35),
                  *(unsigned char*)((char*)a + 0x34), pr_walk_count(g), g ? nav_count(g) : -1);
    }
  }
  arr = ((find_objs_t)RVA(R_FINDOBJS))(g_prBotType, 1, 0);
  if (!arr) { elog("probe: bots array null (stop=%d)", (int)st); return; }
  n = *(int*)((char*)arr + 0x0C);
  if (n < 0) n = 0;
  if (n > 64) n = 64;
  for (i = 0; i < n; i++) {
    P b = *(P*)((char*)arr + 0x10 + i * 4);
    P tr, nn = 0, path, enemy = 0, ei;
    V3 p;
    float d;
    int pts = -1;
    if (!b || !uobj_live(b)) continue;
    cnt++;
    if (shown >= 3) continue;
    tr = ((get_tr_t)RVA(R_COMP_TR))(b, 0);   /* Component.get_transform：传 GameObject 那个会崩 */
    if (!tr) continue;
    ((get_pos_t)RVA(R_GET_POS_INJ))(tr, &p, 0);
    d = g ? pr_near_walk(g, &p, &nn) : -1.0f;
    path = *(P*)((char*)b + 0x80);
    if (pr_readable(path, 0x40) && pr_readable(*(P*)((char*)path + 0x2C), 0x20)) {
      P lst = *(P*)((char*)path + 0x2C);
      pts = *(int*)((char*)lst + 0xC);
    }
    ei = *(P*)((char*)b + 0x28);
    if (pr_readable(ei, 0x40)) enemy = *(P*)((char*)ei + 0x0C);
    {
      P acts = *(P*)((char*)b + 0x58);
      P sa = *(P*)((char*)b + 0x64);
      P gnear = *(P*)((char*)b + 0x88);
      P gnext = *(P*)((char*)b + 0x8C);
      int an = pr_readable(acts, 0x20) ? *(int*)((char*)acts + 0xC) : -1;
      int isS = -1, over = -1, reach = -1;
      float enemyD = -1.0f;
      float spd = -1.0f;
      char names[200];
      V3 tp;
      int k2;
      names[0] = 0;
      tp.x = tp.y = tp.z = 0.0f;
      if (pr_readable(sa, 0x30)) {
        isS = *(unsigned char*)((char*)sa + 0x10);
        tp.x = *(float*)((char*)sa + 0x14);
        tp.y = *(float*)((char*)sa + 0x18);
        tp.z = *(float*)((char*)sa + 0x1C);
        over = *(unsigned char*)((char*)sa + 0x20);
        reach = *(unsigned char*)((char*)sa + 0x21);
      }
      /* 行为名：actionList 里每个 BotActionBase 的类名（Saunter / GoCrouchPos / CrabStep ...） */
      if (pr_readable(acts, 0x20)) {
        P items = *(P*)((char*)acts + 0x8);
        int ai, cnt2 = an > 10 ? 10 : an;
        if (pr_readable(items, 0x20)) {
          for (ai = 0; ai < cnt2; ai++) {
            P o = *(P*)((char*)items + 0x10 + ai * 4);
            const char* nm = "?";
            if (pr_readable(o, 0x10)) nm = type_name(*(P*)o);
            if (ai) strncat(names, ",", sizeof names - strlen(names) - 1);
            strncat(names, nm, sizeof names - strlen(names) - 1);
          }
        }
      }
      if (enemy && pr_readable(ei, 0x40)) enemyD = *(float*)((char*)ei + 0x28);
      /* 速度：同一 bot 两次采样间的水平位移 / 时间 */
      for (k2 = 0; k2 < 32; k2++) if (g_bp[k2].bot == b) break;
      if (k2 == 32) {
        for (k2 = 0; k2 < 32; k2++) if (!g_bp[k2].bot) {
          g_bp[k2].bot = b; g_bp[k2].p = p; g_bp[k2].t = GetTickCount(); break;
        }
      }
      if (k2 < 32) {
        unsigned dt = GetTickCount() - g_bp[k2].t;
        if (dt > 200) {
          float dx = p.x - g_bp[k2].p.x, dz = p.z - g_bp[k2].p.z;
          spd = sqrtf(dx * dx + dz * dz) / ((float)dt / 1000.0f);
          g_bp[k2].p = p; g_bp[k2].t = GetTickCount();
        }
      }
      elog("beh: bot=%p p=(%.1f,%.1f,%.1f) spd=%.2f acts=[%s] isS=%d tgt=(%.1f,%.1f,%.1f) over=%d reach=%d path=%p pts=%d enemy=%p enemyD=%.1f nearN=%p nextN=%p",
           b, p.x, p.y, p.z, spd, names, isS, tp.x, tp.y, tp.z, over, reach,
           path, pts, enemy, enemyD, gnear, gnext);
    }
    shown++;
  }
  elog("probe: bots=%d stopAllBot=%d", cnt, (int)st);
}

void editor_tick(void) {
  static int ticks;
  if (!g_inited) return;
  {                           /* 守卫区静态列表体检：2 tick 一次 = 0.5 s 一次 */
    static int w, pf = -1;
    if (pf < 0) pf = cfg_bool("perf", 0) ? 1 : 0;
    if ((++w & 1) == 0) {
      if (pf) {
        LARGE_INTEGER a, b, fr;
        double us;
        QueryPerformanceCounter(&a);
        area_watch();
        QueryPerformanceCounter(&b);
        QueryPerformanceFrequency(&fr);
        us = (double)(b.QuadPart - a.QuadPart) * 1e6 / (double)fr.QuadPart;
        g_pfSum += us; g_pfCnt++; if (us > g_pfMax) g_pfMax = us;
        if (g_pfCnt >= 120) {              /* 120 次 x 0.5 s = 60 s */
          elog("perf: area_watch avg=%.1fus max=%.1fus n=%d (~%.3f%% of one core)",
               g_pfSum / g_pfCnt, g_pfMax, g_pfCnt, (g_pfSum / g_pfCnt) * 2.0 / 10000.0);
          g_pfSum = g_pfMax = 0; g_pfCnt = 0;
        }
      } else area_watch();
    }
  }
  if (g_sceneAge < 1000000) g_sceneAge++;
  if (g_sceneAge >= VIS_SCENE_WAIT) g_sceneReadyOnce = 1;
  nm_auto_tick();
  menu_tick();                /* F2 / 长按 E 路点菜单 */
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
  { static int pr; if ((++pr % 20) == 0) bot_probe(); }   /* 人机状态探针：~5 s 一次 */
  { static int dr; if ((++dr % 4) == 0) drive_tick(); }    /* 人机巡线：~1 s 一次 */
  nm_tick();                  /* 可走面独立于可视化：Ctrl+V 关着也能显示 */
  if (!g_visOn) {
    if ((++ticks % 8) == 0) overlay_refresh();   /* 可视化关着也保持面板数字是活的 */
    return;
  }
  if ((ticks % 60) == 0) {
    P pg = navfix_point_graph();
    elog("hb: interactive tick=%d age=%d nodes=%d vis=%d dirty=%d badtr=%d",
         ticks, g_sceneAge, pg ? *(int*)((char*)pg + 0xEC) : -1, g_visOn, g_visDirty, g_badTr);
  }
  if (g_visDirty) {
    /* 刚进图时游戏自己的组件表还挂着上一张图的组件（见 VIS_SCENE_WAIT 注释）。
     * 等场景稳定再读；可走面和水走面线框已经在 nm_tick 里画好了，不受影响。 */
    if (g_sceneAge < VIS_SCENE_WAIT) {
      if ((ticks % 20) == 0)
        elog("vis: defer rebuild (scene age %d/%d)", g_sceneAge, VIS_SCENE_WAIT);
    } else {
      g_visDirty = 0;
      vis_rebuild();
    }
  }
  if ((++ticks % 8) == 0) overlay_refresh();   /* keep the spawn legend live at ~2 s */
}

/* 练习场开关：<插件目录>\nav\nogen.txt 存在时，插件不再自己铺路点。
 * 用来把暴风这种本来没有路点的图变成「真正的空场」，方便新手从 0 开始画。 */
int editor_nogen(void) {
  char p[MAX_PATH + 40];
  FILE* f;
  if (!g_dir[0]) return 0;
  /* 测试包里也可以放一份 nogen.txt：测「空场从 0 画点」时不必动正式版的开关 */
  if (g_navDir[0]) {
    sprintf(p, "%s\\nogen.txt", g_navDir);
    f = fopen(p, "r");
    if (f) { fclose(f); return 1; }
  }
  sprintf(p, "%s\\nav\\nogen.txt", g_dir);
  f = fopen(p, "r");
  if (!f) return 0;
  fclose(f);
  return 1;
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
  if (shift && vk == '6') { nm_toggle(); return; }   /* 可走面独立开关 */

  /* ---- 路点编辑（Ctrl+Shift+字母） ---- */
  if (shift && vk == 'A') { nav_sel_a(); return; }        /* 选 A 点 */
  if (shift && vk == 'N') { nav_add_here(); return; }     /* 准星处加点 */
  if (shift && vk == 'J') { nav_toggle_edge(); return; }  /* A <-> 准星节点 连/断 */
  if (shift && vk == 'D') { nav_del_here(); return; }     /* 禁用准星节点 */
  if (shift && vk == 'Z') { nav_undo(); return; }         /* 撤销上一条 */
  if (shift && vk == 'S') { nav_save(); return; }         /* 手动再存一次 */
  if (shift && vk == 'R') { nav_reapply(); return; }      /* 强制重新套用 */

  if (vk == '1') {
    if (!g_editAllow) { elog("[cfg] editor = off, 游戏内编辑已关闭"); overlay_refresh(); return; }
    g_on = !g_on;
    elog("editor %s (markers=%d)", g_on ? "ON" : "OFF", g_n);
    overlay_refresh();
    return;
  }
  if (vk == '9') { status(); overlay_refresh(); return; }
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
        overlay_refresh();
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
      overlay_refresh();
      break;
    default:
      break;
  }
}

void editor_on_key(unsigned vk) { editor_on_key_mod(vk, 0); }

/* headless entry used by the WM_APP+0x53 test hook (no keyboard focus needed) */
void editor_on_key_any(unsigned vk, int shift) {
  if (!ed_init()) return;
  elog("test-key vk=0x%02X shift=%d menu=%d", vk & 0xFF, shift, g_wpMenuOpen);
  /* 菜单开着时，数字/Enter/W/S/Esc 必须先给菜单，不能被编辑器开关抢走 */
  if (g_wpMenuOpen) {
    (void)editor_menu_key(vk, 0);
    return;   /* 菜单开着只走菜单键，别让测试钩子顺带触发编辑器 Ctrl 热键 */
  }
  if (vk == VK_F2 || vk == 'E') {
    if (editor_menu_key(vk, 0)) return;
  }
  editor_on_key_mod(vk, shift);
}

void editor_on_quit(void) {
  elog("quit: editor stop (markers=%d vis nodes=%d features=%d)", g_n, g_vnN, g_vfN);
  nav_conn_roots_release();
}

/* ---- 车测自由视角（2026-11-18）----------------------------------------
 * 为什么需要：车测用 SceneManager.LoadScene 直接进图，没有玩家、没有玩家控制器，
 * 视角没人管。地图场景自带 Main Camera + CM FreeLook（Cinemachine 虚拟相机），
 * 所以不新建相机，只做两件事：
 *   1) 关掉 CM FreeLook，否则 CinemachineBrain 每帧把相机拽回它的机位；
 *   2) 每 16 ms（navfix 的 WM_TIMER）写一次 position / eulerAngles。
 * 操作：WASD 平移 · Space/Ctrl 升降 · Shift 加速 · 按住右键转头 · F7 开关。
 * 只在 UCF_FREECAM=1（控制台车测页的勾选）时启动，正常游戏一行都不执行。 */

HWND navfix_hwnd(void);
int autotest_in_map(void);

static void freecam_env(void) {
  char a[16], b[8];
  if (g_freeEnvRead) return;
  g_freeEnvRead = 1;
  if (GetEnvironmentVariableA("UCF_AUTOTEST", a, sizeof a) <= 0) return;
  if (GetEnvironmentVariableA("UCF_FREECAM", b, sizeof b) <= 0 || b[0] != '1') return;
  g_freeEnv = 1;
  g_freeOn = 1;
  elog("freecam: enabled by UCF_FREECAM (WASD + RMB, F7 toggles)");
}

static P freecam_find_go(const char* name) {
  P m, s, go;
  void* args[1];
  void* exc = 0;
  if (!x_class_get_method_from_name || !x_runtime_invoke || !x_string_new || !g_goCls) return 0;
  m = x_class_get_method_from_name(g_goCls, "Find", 1);
  if (!m) return 0;
  s = x_string_new(name);
  if (!s) return 0;
  args[0] = s;
  go = x_runtime_invoke(m, 0, args, &exc);
  return exc ? 0 : go;
}

static void freecam_kill_vcam(P cam) {
  P go = cam ? ((get_go_t)RVA(R_GETGO))(cam, 0) : 0;
  P brain = 0, type = 0;
  g_freeVcamOff = 1;                 /* 只尝试一次；失败也不反复刷日志 */
  /* 优先关 CinemachineBrain（挂在 Main Camera 上，每帧把 Transform 拽回 vcam 的机位）。
   * 不靠 GameObject.Find("CM FreeLook")：实测按名字找不到（多半是未激活/改名）。 */
  if (!g_freeBrainCls) g_freeBrainCls = find_cls("Cinemachine", "CinemachineBrain");
  if (!g_freeBrainCls) g_freeBrainCls = find_cls("", "CinemachineBrain");
  if (g_freeBrainCls && x_class_get_type && x_type_get_object) {
    type = x_type_get_object(x_class_get_type(g_freeBrainCls));
  }
  if (go && type) {
    brain = ((getcomp_t)RVA(R_GETCOMP))(go, type, 0);   /* 唯一的 GetComponent(Type) 重载 */
  }
  if (brain && mem_ok(brain, 0x10)) {
    ((set_active_t)RVA(R_SET_ENABLED))(brain, 0, 0);
    g_freeBrain = brain;
    elog("freecam: disabled CinemachineBrain (%p)", brain);
    return;
  }
  {
    P vc;
    elog("freecam: CinemachineBrain not found (cls=%p brain=%p); trying CM FreeLook",
         g_freeBrainCls, brain);
    vc = freecam_find_go("CM FreeLook");
    if (vc) {
      ((set_active_t)RVA(R_SETACTIVE))(vc, 0, 0);
      g_freeVcamGo = vc;
      elog("freecam: disabled CM FreeLook (%p)", vc);
    } else {
      elog("freecam: no CinemachineBrain / CM FreeLook found (camera may still be driven)");
    }
  }
}

static int freecam_cam(P* camOut, P* trOut) {
  P cam = ((cam_main_t)RVA(R_CAM_MAIN))(0);
  P go, tr;
  if (!cam || !mem_ok(cam, 0x20) || !uobj_live(cam)) return 0;
  go = ((get_go_t)RVA(R_GETGO))(cam, 0);
  tr = get_tr(go);
  if (!tr || !mem_ok(tr, 0x10) || !uobj_live(tr)) return 0;
  if (!g_freeTrCls) g_freeTrCls = find_cls("UnityEngine", "Transform");
  if (g_freeTrCls && *(P*)tr != g_freeTrCls) return 0;
  if (camOut) *camOut = cam;
  if (trOut) *trOut = tr;
  return 1;
}

static void freecam_apply(P tr) {
  V3 e;
  ((set_pos_t)RVA(R_SET_POS))(tr, g_freePos, 0);
  e.x = g_freePitch; e.y = g_freeYaw; e.z = 0.0f;
  ((set_pos_t)RVA(R_SET_EULER))(tr, e, 0);
}

/* 用路点图的包围盒算一个能俯视全图的机位；没有路点图的图返回 0（保持游戏机位） */
static int freecam_center(V3* c, float* span) {
  P g = navfix_point_graph();
  int i, n, cnt = 0;
  double sx = 0, sy = 0, sz = 0;
  float minx = 1e9f, maxx = -1e9f, minz = 1e9f, maxz = -1e9f;
  if (!g) return 0;
  n = nav_count(g);
  if (n <= 0) return 0;
  for (i = 0; i < n; i++) {
    P nd = nav_node(g, i);
    V3 p;
    if (!nd || !mem_ok(nd, 0x28)) continue;
    nav_pos(nd, &p);
    if (!(p.x > -20000.0f && p.x < 20000.0f)) continue;
    if (!(p.z > -20000.0f && p.z < 20000.0f)) continue;
    if (!(p.y > -5000.0f && p.y < 5000.0f)) continue;
    sx += p.x; sy += p.y; sz += p.z; cnt++;
    if (p.x < minx) minx = p.x;
    if (p.x > maxx) maxx = p.x;
    if (p.z < minz) minz = p.z;
    if (p.z > maxz) maxz = p.z;
  }
  if (cnt < 8) return 0;
  c->x = (float)(sx / cnt);
  c->y = (float)(sy / cnt);
  c->z = (float)(sz / cnt);
  {
    float dx = maxx - minx, dz = maxz - minz;
    *span = dx > dz ? dx : dz;
    if (*span < 30.0f) *span = 30.0f;
    if (*span > 400.0f) *span = 400.0f;
  }
  return 1;
}

static int freecam_place(P tr) {
  V3 c;
  float span = 0.0f;
  g_freeLastTick = GetTickCount();
  if (freecam_center(&c, &span)) {
    float dx, dy, dz, len;
    g_freePos.x = c.x;
    g_freePos.z = c.z - span * 0.75f;
    g_freePos.y = c.y + span * 0.45f + 15.0f;
    dx = c.x - g_freePos.x; dy = c.y - g_freePos.y; dz = c.z - g_freePos.z;
    len = sqrtf(dx * dx + dy * dy + dz * dz);
    if (len < 1.0f) len = 1.0f;
    g_freeYaw = atan2f(dx, dz) * 57.29578f;
    g_freePitch = -asinf(dy / len) * 57.29578f;
    elog("freecam: place %.1f %.1f %.1f yaw=%.0f pitch=%.0f (graph view, span=%.0f)",
         g_freePos.x, g_freePos.y, g_freePos.z, g_freeYaw, g_freePitch, span);
    return 1;
  }
  {
    V3 cur;
    ((get_pos_t)RVA(R_GET_POS_INJ))(tr, &cur, 0);
    /* 大厅/加载中：相机还在原点、也没有路点图 -> 这一帧不接管，等真正进图再放机位 */
    if (fabsf(cur.x) + fabsf(cur.y) + fabsf(cur.z) < 1.0f) return 0;
    g_freePos = cur;
    g_freeYaw = 0.0f;
    g_freePitch = 12.0f;
    elog("freecam: place %.1f %.1f %.1f (keep scene camera, no point graph)",
         g_freePos.x, g_freePos.y, g_freePos.z);
    return 1;
  }
}

static void freecam_input(P tr) {
  DWORD now = GetTickCount();
  float dt = (now - g_freeLastTick) / 1000.0f;
  HWND hwnd = navfix_hwnd();
  int fg = hwnd && GetForegroundWindow() == hwnd;
  V3 np;
  if (dt < 0.001f) return;
  if (dt > 0.15f) dt = 0.15f;       /* 卡顿/切图后不要一下飞很远 */
  g_freeLastTick = now;
  if (!fg) return;                  /* 游戏不在前台：只保持机位，不读键鼠 */

  if (GetAsyncKeyState(VK_RBUTTON) & 0x8000) {
    RECT rc;
    POINT pt, ctr;
    if (GetClientRect(hwnd, &rc)) {
      ctr.x = (rc.right - rc.left) / 2;
      ctr.y = (rc.bottom - rc.top) / 2;
      ClientToScreen(hwnd, &ctr);
      GetCursorPos(&pt);
      {
        float dx = (float)(pt.x - ctr.x), dy = (float)(pt.y - ctr.y);
        if (dx != 0.0f || dy != 0.0f) {
          g_freeYaw += dx * 0.16f;
          g_freePitch += dy * 0.16f;
          if (g_freePitch > 89.0f) g_freePitch = 89.0f;
          if (g_freePitch < -89.0f) g_freePitch = -89.0f;
          SetCursorPos(ctr.x, ctr.y);
        }
      }
    }
  }

  {
    float sp = 15.0f, step, cy, sy, cyaw, syaw;
    V3 fw, rt;
    np = g_freePos;
    if (GetAsyncKeyState(VK_SHIFT) & 0x8000) sp *= 4.0f;
    step = sp * dt;
    cy = cosf(g_freePitch / 57.29578f);
    sy = sinf(g_freePitch / 57.29578f);
    cyaw = cosf(g_freeYaw / 57.29578f);
    syaw = sinf(g_freeYaw / 57.29578f);
    fw.x = syaw * cy; fw.y = -sy; fw.z = cyaw * cy;
    rt.x = cyaw;      rt.y = 0.0f; rt.z = -syaw;
    if (GetAsyncKeyState('W') & 0x8000) { np.x += fw.x * step; np.y += fw.y * step; np.z += fw.z * step; }
    if (GetAsyncKeyState('S') & 0x8000) { np.x -= fw.x * step; np.y -= fw.y * step; np.z -= fw.z * step; }
    if (GetAsyncKeyState('D') & 0x8000) { np.x += rt.x * step; np.z += rt.z * step; }
    if (GetAsyncKeyState('A') & 0x8000) { np.x -= rt.x * step; np.z -= rt.z * step; }
    if (GetAsyncKeyState(VK_SPACE) & 0x8000) np.y += step;
    if (GetAsyncKeyState(VK_CONTROL) & 0x8000) np.y -= step;
  }
  g_freePos = np;
  freecam_apply(tr);
}

void editor_freecam_toggle(void) {
  freecam_env();
  if (!g_freeEnv) return;
  g_freeOn = !g_freeOn;
  elog("freecam: %s", g_freeOn ? "ON" : "OFF");
  if (!g_freeOn) {
    if (g_freeBrain) {
      ((set_active_t)RVA(R_SET_ENABLED))(g_freeBrain, 1, 0);
      elog("freecam: CinemachineBrain re-enabled");
    }
    if (g_freeVcamGo) {
      ((set_active_t)RVA(R_SETACTIVE))(g_freeVcamGo, 1, 0);
      elog("freecam: CM FreeLook re-enabled");
    }
    g_freeBrain = 0;
    g_freeVcamGo = 0;
    g_freeVcamOff = 0;
  }
}

void editor_freecam_tick(void) {
  P cam, tr;
  freecam_env();
  if (!g_freeEnv || !g_freeOn || !g_inited) return;
  if (!autotest_in_map()) return;    /* 大厅/热身阶段不接管相机 */
  if (!freecam_cam(&cam, &tr)) return;
  if (cam != g_freeCam) {
    g_freeCam = cam;
    g_freeInited = 0;
    g_freeVcamOff = 0;
    g_freeVcamGo = 0;
    g_freeBrain = 0;
    g_freeWarned = 0;
  }
  if (!g_freeVcamOff) {
    if (!freecam_place(tr)) return;     /* 大厅/加载中：下一 tick 再试 */
    g_freeInited = 1;
    freecam_kill_vcam(cam);
    freecam_apply(tr);
  } else if (!g_freeInited) {
    if (!freecam_place(tr)) return;
    g_freeInited = 1;
    freecam_apply(tr);
  }
  if (!g_freeWarned) {
    V3 cur;
    ((get_pos_t)RVA(R_GET_POS_INJ))(tr, &cur, 0);
    if (fabsf(cur.x - g_freePos.x) + fabsf(cur.y - g_freePos.y) +
        fabsf(cur.z - g_freePos.z) > 3.0f) {
      elog("freecam: camera is being overwritten (vcam still active?) - check 'CM FreeLook'");
      g_freeWarned = 1;
    }
  }
  freecam_input(tr);
}

void editor_start(const char* modDir) {
  if (!modDir) return;
  strncpy(g_dir, modDir, sizeof(g_dir) - 1);
  sprintf(g_log, "%s\\ucf_mod.log", g_dir);
  sprintf(g_file, "%s\\markers\\markers.txt", g_dir);
  /* 四版路径先定下来：pack_init 要用 g_packRoot，导出要用 g_expDir。
   * 控制台启动游戏时会带 UCF_EXPORT_DIR / UCF_PACK_DIR / UCF_NAV_READONLY。 */
  {
    char def[MAX_PATH], ro[8];
    sprintf(def, "%s\\vis", g_dir);
    dir_choice("UCF_EXPORT_DIR", "export_dir", def, g_expDir, sizeof g_expDir);
    sprintf(def, "%s\\packs", g_dir);
    dir_choice("UCF_PACK_DIR", "pack_dir", def, g_packRoot, sizeof g_packRoot);
    mkdir_p(g_expDir);
    mkdir_p(g_packRoot);
    g_navReadOnly = (GetEnvironmentVariableA("UCF_NAV_READONLY", ro, sizeof ro) > 0 &&
                     ro[0] == '1') ? 1 : 0;
  }
  pack_init();   /* UCF_PACK / UCF_FP：这次读哪个目录、只对哪张图生效 */
  /* 开关全部来自 ucf_mod.json（cfg.c）：这里各取一次，日志里写清楚，
   * 关掉哪个在日志里都看得见，不用猜。 */
  g_visOn      = cfg_bool("visualizer", 0);
  g_nmShow     = cfg_bool("navmesh_show", 1);
  g_visNodes   = cfg_bool("vis_nodes", 1);
  g_visNano    = cfg_bool("vis_nano", 1);
  g_visCrouch  = cfg_bool("vis_crouch", 1);
  g_visGuard   = cfg_bool("vis_guard", 1);
  g_visBorn    = cfg_bool("vis_born", 1);
  g_visSupply  = cfg_bool("vis_supply", 1);
  g_visJump    = cfg_bool("vis_jump", 1);
  g_visTag     = cfg_bool("vis_tag", 1);
  g_editAllow  = cfg_bool("editor", 1);
  g_wpMenuOn   = cfg_bool("wp_menu", 1);
  g_wpAutoGround = cfg_bool("wp_autoground", 1);
  cfg_str("wp_brush", "normal", g_wpBrushName, sizeof g_wpBrushName);
  g_wpBrush    = brush_from_name(g_wpBrushName);
  g_expEnabled = cfg_bool("export_enabled", 1);
  g_expNodes   = cfg_bool("export_nodes", 1);
  g_expCrouch  = cfg_bool("export_crouch", 1);
  g_expArea    = cfg_bool("export_area", 1);
  g_expGuard   = cfg_bool("export_guard", 1);
  g_expSpawn   = cfg_bool("export_spawn", 1);
  g_expTags    = cfg_bool("export_tags", 1);
  elog("editor ready: visualizer=%d navmesh=%d editor=%d file=%s",
       g_visOn, g_nmShow, g_editAllow, g_file);
  elog("wpmenu: on=%d autoground=%d brush=%s", g_wpMenuOn, g_wpAutoGround, g_wpBrushName);
  elog("vis data: nodes=%d nano=%d crouch=%d guard=%d born=%d supply=%d jump=%d tag=%d",
       g_visNodes, g_visNano, g_visCrouch, g_visGuard, g_visBorn, g_visSupply,
       g_visJump, g_visTag);
  elog("export content: enabled=%d nodes=%d crouch=%d area=%d guard=%d spawn=%d tags=%d",
       g_expEnabled, g_expNodes, g_expCrouch, g_expArea, g_expGuard, g_expSpawn, g_expTags);
  elog("four versions: export=%s packs=%s officialNavSave=%s",
       g_expDir, g_packRoot, g_navReadOnly ? "blocked(read-only)" : "allowed");
  veh_install();   /* 挂了 VEH：任何崩溃都会把调用链写进 ucf_mod.log */
  { void autotest_start(const char*); autotest_start(g_dir); }   /* UCF_AUTOTEST=7,10 才动作 */
  {
    char p[MAX_PATH];
    FILE* fh;
    extern void navfix_set_collect_only(int);
    sprintf(p, "%s\\collect.flag", g_dir);
    if (cfg_bool("collect_only", 0)) g_collectOnly = 1;
    fh = fopen(p, "r");
    if (fh) { fclose(fh); g_collectOnly = 1; }
    navfix_set_collect_only(g_collectOnly);
    elog("mode: %s (flag %s)", g_collectOnly ? "COLLECT-ONLY 只读采集" : "INTERACTIVE 可编辑", p);
    if (g_collectOnly) elog("collect-only: Ctrl+Shift+X 切回交互模式（或直接删掉 collect.flag）");
  }
}
