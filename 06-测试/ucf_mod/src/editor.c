/* editor.c - ucf_mod in-game AI marker editor
 *
 * phase 1: crouch / nano guard pos / nano guard area placement + save/load
 * phase 2: per-type colours, typed marker delete (F2 menu 5), on-screen HUD
 *
 * 2026-11-26 热键大精简：游戏里只留 F2 菜单 + 下面这几个键。
 * 删掉的：Ctrl+0/1/2/3/4/5/6/7/8/9（编辑模式那一套）、Ctrl+Shift+A/N/J/D/Z/R/S、
 * Ctrl+Shift+6/+7（可走面 / 罗盘）。它们做的事 F2 菜单里都有；可视化各层改由控制台
 * 「插件开关 → 可视化」实时下发（ucf_navcmd 的 cmd=vis，0.5 s 内生效）。
 *
 * Ctrl+S  SAVE ALL（markers + 点图）        Ctrl+V  可视化总开关（数据 + 点位小球）
 * Delete  删准星最近标记（3 m 内）          F2 / 长按 E 0.45 s  路点菜单
 * Ctrl+E  手动导出 JSON                    Ctrl+Shift+X  只读采集（这两个待定）
 *
 * 2026-11-25 用户要求：游戏内编辑**必须手动保存**。所有加点/删点/连线/跳链/
 * 蹲守点/守卫区/标签/出生点只在内存和场景里生效，只有 Ctrl+S（F2 菜单
 * 「撤销 / 保存」里的「保存」，或控制台 cmd=save）才写文件；不保存就退出
 * 房间 = 改动全部丢弃。以前每次编辑自动落盘、另外还给过另存快捷键（已全部删除），
 * 这些口子全部取消（用户明确「其他快捷键的保存都不要」）。
 * F2 menu 5: typed point delete (1 crouch 2 guard pos 3 jump 4 tag 5 spawn BL
 *            6 spawn GR 7 any point)   F2 menu 6: delete area (guard area)
 * Ctrl+Shift+6  A* navmesh wireframe on/off            (cfg navmesh_show)
 * Ctrl+Shift+7  compass rose on/off (汉字东南西北)      (cfg vis_compass)
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

/* 守卫区 / 守卫点（Bot_NanoGuardArea / Bot_NanoGuardPos）现造是可以的，但
 * Awake / Init 依赖的字段必须先补齐 —— 2026-11-25 16:17 的闪退就是没补：
 *   1) Bot_NanoGuardArea.Awake()（GameAssembly 0x10B300A0）先读 this.posList，
 *      非空才用 GetComponentsInChildren 收子物体再登记 SpareAreaList；运行时
 *      AddComponent 只有 .ctor 里 new 的 posList 非空，entrancePos / neighborAreas /
 *      escapeAreas / escapePos 四个数组全是 null。
 *   2) Bot_NanoGuardPos.Init()（0x10B30E80）是
 *        this.area = area;
 *        l = new List<Vector3>(); l.AddRange(this.zoomPos);
 *        l.AddRange(area.entrancePos);  this.zoomPos = l.ToArray();
 *      两个 AddRange 碰到 null 都抛 ArgumentNullException。这个托管异常是在我们自己
 *      的 C 线程里抛的，IL2CPP 没有托管栈帧可以展开 -> std::terminate -> CRT 弹
 *      "This application has requested the Runtime to terminate it in an unusual
 *      way"（就是菜单「守卫区工具 -> 加守卫点」那一下闪退）。
 *   3) GetRandomZoomPos() 还要按随机下标取 zoomPos，所以 zoomPos 至少 1 个元素。
 * 现在 make_area / make_nanopos 的顺序是：守卫区先不激活 -> 补齐四个数组 -> 建点位并
 * 补 zoomPos -> Init -> 挂进 posList -> 最后激活守卫区，让 Awake 一次性把子点和自己
 * 登记好。改这两个函数之前先读这段。 */

static HMODULE g_ga;
static char g_log[MAX_PATH];
static char g_dir[MAX_PATH];
static char g_file[MAX_PATH];

/* ---- 三区路径（2026-11-18 建，2026-11-21 四区改三区）------------------------
 * ① 备份版 navdata\native / ② 开发版 navdata\dev / ③ 游戏目录 <ucf_mod>（运行时）。
 * ② 里 final\ 是成品（多版本，一版一整套）、packs\ 是编辑中，vis\ 收件箱，archive\ 历史。
 * 三档启动（控制台决定）：成品 = UCF_PACK_DIR=②\final + UCF_PACK=<版本名>，
 * 按「包」读 ②\final\<版本>\<指纹>.txt —— 一版一整套数据，控制台选启动哪个版本；
 * 和编辑中同一套加载逻辑（grow/keep 建点也生效），只读靠文件属性（游戏内保存失败）；
 * 编辑中 = UCF_PACK 指向 ② packs\（可写）；原版 = 总开关关，插件待机。
 * 2026-11-21 起 ③ 不再存数据（只放 dll / 配置 / markers\），游戏不读 ③\maps。
 * 导出/测试包目录解析顺序：环境变量（控制台启动游戏时注入）> ucf_mod.json > 插件目录。 */
static char g_expDir[MAX_PATH];    /* 可走面落盘根：UCF_EXPORT_DIR > cfg export_dir > <dir>\vis */
static char g_packRoot[MAX_PATH];  /* 测试包根：UCF_PACK_DIR > cfg pack_dir > <dir>\packs */
static int  g_navReadOnly;         /* UCF_NAV_READONLY=1：正式版 nav\ 不允许游戏内落盘 */
static int  g_saveWarned;

/* ---- 手动保存（2026-11-25 用户要求）--------------------------------------
 * 游戏内所有编辑只改内存 / 场景；只有 Ctrl+S（或 F2 菜单「撤销 / 保存」里的
 * 「保存」，或控制台 cmd=save）才落盘。不保存就退出房间 = 改动丢弃。
 * 这里只记「哪一边有没落盘的改动」，用来在菜单里显示、并在退房间时打日志；
 * 保存时也只写脏的那一边 —— 控制台 / 录制可能刚往同一个文件追加过内容，
 * 没改过的文件不重写，免得把别人的追加盖掉。 */
static int  g_dirtyMk;             /* markers.txt：蹲守 / 守卫 / 标签 / 出生点 */
static int  g_dirtyNav;            /* <指纹>.txt：加点 / 删点 / 连线 / 跳链 */
static int  editor_unsaved(void) { return g_dirtyMk || g_dirtyNav; }
static void editor_dirty_mk(void)  { g_dirtyMk = 1; }
static void editor_dirty_nav(void) { g_dirtyNav = 1; }

/* ---- 测试包（UCF_PACK / UCF_FP）-------------------------------------------
 * 「UCF 控制台」启动游戏时递进来的环境变量，决定这次读哪套路线数据：
 *   UCF_PACK=chain_a   读 <插件目录>\packs\chain_a\<指纹>.txt
 *                      （不设 = 读 <插件目录>\nav\<指纹>.txt，即一直以来的正式版）
 *   UCF_FP=n0-...      只有当前场景指纹等于它才套用；别的图整包跳过，不动一个字节
 *   UCF_FPLABEL=...    只用于日志显示（图的中文名）
 * 包目录固定放在插件目录内：vis / markers / 日志也都挂在 g_dir 下，把 nav 单独指到
 * 工程端会让两套数据混用（导出、读数全乱），所以这里只换最后一级目录。 */
static char g_navDir[MAX_PATH];   /* 路线数据目录：<dir>\nav 或 <dir>\packs\<包名> */
static char g_packName[160];      /* 空 = 正式版；地图文件夹\包名，可以是中文文件夹 */
static char g_packFp[48];         /* 空 = 不限图 */
static char g_packFpLabel[64];    /* 只用于显示 */
static int  g_packSkip;           /* 1 = 当前图不在本次测试清单里 */
static char g_packStat[224] = "数据 正式版（nav）";   /* 日志里的数据来源一行 */

/* ---- 成品档：一图一夹（2026-11-27）---------------------------------------
 * 成品在各图自己的文件夹里：<packRoot>\<图文件夹>\<sub>\<指纹>.txt
 *   UCF_PACK_DIR=<data\maps>  UCF_NAV_SEARCH=1  UCF_NAV_SUB=final
 * 成品档不设 UCF_PACK（没有“唯一一张图”），所以按当前场景指纹去各图文件夹里找；
 * 找到哪张图，markers.txt 就跟着那张图走（g_mapDirName）。 */
static int  g_navSearch;          /* 1 = 按指纹搜 <packRoot>\*\<sub>\ */
static char g_navSub[48];         /* 子目录名（成品 = "final"） */
static char g_mapDirName[160];    /* 搜到的图文件夹名：markers\<图>\markers.txt 用它 */
static char g_mkFp[64];           /* g_file 是按哪张图的指纹算出来的（防每帧重载） */

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
static int  g_team;
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
static void (*x_field_static_set_value)(P, void*);
static P (*x_array_new)(P, unsigned int);
static int (*x_array_get_byte_length)(P);
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
/* Bot_NanoGuardArea.posList 的实际类型 List<Bot_NanoGuardPos> 和它的 Add()，
 * 以及 SpareAreaList（List<Bot_NanoGuardArea>）的 Add()：
 * 运行时新建的守卫区/守卫点必须自己挂进这两个列表（Awake 只在激活那一刻收一次）。 */
static P g_nposListCls, g_nposListAdd, g_nareaListAdd;
/* Bot_JumpLink.linkDic（Dictionary<GraphNode, Bot_JumpLink>）的类型和 Remove(TKey)：
 * 删跳链时要把登记一起摘掉，否则 GetLink 一直能查到已销毁的对象。 */
static P g_linkDicCls, g_linkDicRemove;
static P g_rendCls, g_rendType, g_textCls, g_textType, g_canvasCls, g_canvasType, g_fontCls, g_fontType;

static P g_matCls;
static P g_meshCls, g_mfCls, g_mrCls, g_vec3Cls, g_i32Cls;
static P g_jumpCls, g_tagCls, g_jumpLinkCls;
/* 2026-11-26 删除旧守卫（Bot_GuardArea / Bot_GuardPos）：游戏里没人用 ——
 * Bot_GuardArea 是空类、没被任何类引用；Bot_GuardPos 只当 Bot_CrouchPos 的基类。
 * 它们的类指针 / vis 开关 / 导出项一并删掉，别再去 FindObjectsOfType 白读。 */
static P g_mmCls, g_mmInstField;
static P g_mfType, g_mrType, g_jumpType, g_tagType;
static P g_matProto;     /* working template material (game shader) */
static char g_shaderName[96]; /* cached shader path, so materials survive asset unloads */
static P g_matSlot[16];  /* cached material per marker type 1..15   */
static unsigned g_matSlotH[16];  /* 每个槽位材质的 gchandle（换图时释放，见 mat_reset） */
static unsigned g_matProtoH;     /* g_matProto 的 gchandle */
static int g_matReady;
static unsigned g_matSetupFailMs; /* mat_setup 失败冷却：别每帧跑 8 次 Shader.Find */
static int g_matDeadLog;          /* 「材质死了」只记一次日志，免得刷屏 */

/* 路点图编辑（定义在文件后半段，这里提前声明给 ed_init/editor_on_scene 用） */
typedef struct {
  int kind; int dir; V3 a, b;      /* dir: 0 双向 / 1 A->B / 2 B->A */
  float jspeed;                    /* 跳链 needSpeed（-1 = 用默认 0） */
  float jacc;                      /* 跳链 accuracy（-1 = 用默认 1.0） */
  int   jdir;                      /* 跳链 direction: 0 = B-A 归一化 / 1 = 正上 / 2 = 前上 */
  /* 蹲（2026-11-27）：录制结算出来的「这一跳要蹲」。
   * jct0 / jct1 = 空中开始 / 结束蹲（相对起跳秒，-1 = 没蹲 / 蹲到落地）；
   * jctb = 起跳那一帧是否蹲着；jctb < 0 = 老文件没有这三列（未知）。 */
  float jct0, jct1;
  int   jctb;
  /* 撤销步号：一次用户动作（放一个点 / 连一条边 / 贴一次地）里的条目同号。
   * 2026-11-26：以前「撤销一步」只弹一条记录，加点 + 自动连边是两条、跳点是三条，
   * 用户按一次撤销只看到一半变化（甚至只弹掉一条没有可见效果的 jump add），
   * 以为撤销坏了。现在一次动作整组反做。0 = 读盘的旧条目（没有组，一次撤一条）。 */
  int   grp;
} NAVED;
/* 点图编辑的种类（NAVED.kind）。定义放前面：del_index / 撤销记录都要用。 */
#define NADD 1     /* node add */
#define NDEL 2     /* node del */
#define EADD 3     /* edge add */
#define EDEL 4     /* edge del */
#define JADD 5     /* jump add：进图套完点和边后建 Bot_JumpLink（跳箱 / 上下层） */
#define NMOVE 6    /* 贴地：a = 原坐标，b = 新坐标（会话级，不落盘） */
#define NPOPADD 7  /* 删掉「本次会话里加的点」：a = 坐标，dir = g_drop 槽位 */
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
/* 撤销步号：一次用户动作（放点 / 连边 / 贴地 / 删点）+1，同一步里的条目整组撤销。 */
static int g_edStep;
/* 路点菜单里显示「上一手到底做了什么」。撤销/重做没有可见变化时，
 * 用户至少能在菜单上看到原因（以前只有控制台日志里有一行）。 */
static char g_wpHint[192];
static void wp_hint(const char* fmt, ...) {
  va_list ap;
  va_start(ap, fmt);
  vsnprintf(g_wpHint, sizeof g_wpHint, fmt, ap);
  va_end(ap);
}
static void ed_step(void) { g_edStep++; }
/* 删掉「本次会话里加的点」时从清单摘掉的条目：撤销要把它们原样补回去。
 * 条目顺序 = 原来的 node add + 相关边，补回清单后重套/落盘行为不变。 */
#define NAVDROP_MAX 64
#define NAVDROP_SLOTS 8
typedef struct { int step; int n; NAVED e[NAVDROP_SLOTS]; } NAVDROP;
static NAVDROP g_drop[NAVDROP_MAX];
static int g_dropNext;
static NAVDROP g_lastDrop;   /* 最近一次 nav_drop_add 摘掉的条目（撤销/重做用） */
static NAVED g_lastJump;     /* 最近一次 nav_drop_jump 摘掉的 jump add（撤销跳链删除用） */
static int g_nedBlank;      /* 1 = 空白地图：原生点全禁；旧文件里的 blank 行也当 grow 读 */
static int g_nedGrow;       /* 1 = 文件写了 grow：原生点标死 + 用 AddNode 新建节点 */
static int g_pgSynthetic;   /* 1 = 本图的 PointGraph 是插件现场补的（纯面图：胜利广场 / 死亡擂台） */
static int g_pgNmDropped;   /* 1 = 已经摘掉可走面（一张图只摘一次） */
static int g_nedKeep;       /* 1 = 文件写了 keep：原生点一个都不动，只新增节点 */
static P   g_growGraph;     /* 已经 grow 过的图：同一张图只新建一次（节点没有删除 API） */
/* 本次进图已经建过的跳链（起终点坐标）：重套包时只补新建的，不整批重建。
 * Bot_JumpLink 组件删不掉，重复建会「一图多条」。 */
#define JSEEN_MAX 128
static V3  g_jumpSeenA[JSEEN_MAX];
static V3  g_jumpSeenB[JSEEN_MAX];
static int g_jumpSeenN;
static int g_growBase;      /* grow 之前的原生节点数 */
static int g_growMade;      /* 上次 grow 新建的点数 */
static int g_nedZeroTicks;  /* 0 节点图连续帧计数（grow 放行前要等 5 帧） */
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
/* 屏幕中央提示（toast）：禁止操作 / 失败原因直接显示在屏幕中间（2026-11-26 用户要求）。
 * 和 F2 菜单共用一张 Canvas：黑影 + 亮红字两个 Text，锚点/轴心都在中心，
 * Y 上移 TOAST_Y 免得压住准星，TOAST_MS 之后自动隐藏。 */
static P g_toast, g_toastGo, g_toastSh, g_toastShGo;
static unsigned g_toastUntil;
#define TOAST_MS 3000
#define TOAST_Y  90.0f
static const COL COL_TOAST    = { 1.00f, 0.23f, 0.16f, 1.00f };   /* 亮红：禁止 / 失败 */
static const COL COL_TOAST_OK  = { 0.35f, 0.95f, 0.45f, 1.00f };   /* 亮绿：成功 */
static const COL COL_TOAST_SH  = { 0.00f, 0.00f, 0.00f, 0.90f };   /* 黑影子：亮场景也看得清 */
#define TOAST_MS_OK  1600
#define TOAST_MS_ERR 3000
static int g_wpMenuOn = 1;      /* cfg: wp_menu */
static int g_wpMenuOpen;
static int g_wpMenuSel;
static int g_wpMenuSub;         /* 0 main 1 types 2 paths 3 areas 4 edit 5 display
                                 * 6 删路径/路点 7 删点位（按类型） 8 删区域（守卫区） */
static int g_wpMenuSubSel;
/* 删除页当前选中的类型：-1 还没选，MT_* = 只删这个类型，
 * MT_ANY_POINT = 任意点位（不含守卫区）。2026-11-25 用户要求按类型分开选，
 * 别靠"最近"盲删；2026-11-25 再拆成「删除点位 / 删除区域」两页。 */
static int g_delType = -1;
/* 0 normal 1 jump 2 crouch 3 guard 4 area 5 tag 6 出生点 BL 7 出生点 GR 8 出生点 中立 */
static int g_wpBrush;
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
#define R_SPR_INJ     0x327AD0   /* Camera.ScreenPointToRay_Injected        */
#define R_SCREEN_W    0x3E6820   /* Screen.get_width                        */
#define R_SCREEN_H    0x3E6800   /* Screen.get_height                       */
#define R_FINDOBJS    0x4E9620   /* Object.FindObjectsOfType(Type,bool)     */
#define R_TIME_GET    0x3F2540   /* UnityEngine.Time.get_time() -> float     */
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
/* 屏幕中心射线 / 投影。IDA 0x10327AD0 确认签名（x86 cdecl，全是栈参）：
 *   void ScreenPointToRay_Injected(Camera*, Vector2* pos, int eye, Ray* ret, MethodInfo*)
 *   void WorldToScreenPoint_Injected(Camera*, Vector3* pos, int eye, Vector3* ret, MethodInfo*)
 * eye：MonoOrStereoscopicEye.Mono = 2。Ray 是 24 字节（origin 0x0 / direction 0xC），
 * 走 out 指针返回 —— 别按结构体返回值调，x86 上那是另一套约定。 */
typedef struct { V3 o, d; } RAY;
typedef void (*spr_t)(P, V2*, int, RAY*, void*);
typedef void (*w2s_inj_t)(P, V3*, int, V3*, void*);
typedef int  (*screen_dim_t)(void*);   /* Screen.get_width/height(const MethodInfo*) */
typedef P    (*find_objs_t)(P, unsigned char, void*);
typedef void (*mesh_ctor_t)(P, void*);
typedef void (*mesh_arr_t)(P, P, void*);
typedef void (*mesh_1_t)(P, void*);
typedef void (*mf_setmesh_t)(P, P, void*);

typedef struct {
  int type;     /* MT_*: 1 crouch 2 nanopos 3 area 4 jumplink 5 tag */
  V3  p;
  int aid;
  int parent;
  int prm;
  float yaw;    /* 朝向（度，0=北 90=东，与屏幕罗盘同一套；YAW_NONE = 未知） */
  P   go;
  P   comp;
  P   vis;
} MK;

/* 标记类型（g_mk[].type）。删除标记按这些值分支出 1-5 项：
 * 守卫点就在守卫区那个 3 m 框里，只按"准星最近"挑很容易删错对象。 */
#define MT_CROUCH  1
#define MT_NANOPOS 2
#define MT_AREA    3
#define MT_JUMP    4
#define MT_TAG     5
#define MT_SPAWN_BL 6   /* 出生点：MapManager.SP_BL（幽灵 / 潜伏者） */
#define MT_SPAWN_GR 7   /* 出生点：MapManager.SP_GR（保卫者 / 人类） */
#define MT_SPAWN_NT 8   /* 出生点：MapManager.SP_Netural（中立；个人竞技全员用它） */
#define WP_BRUSH_N 9    /* 笔刷总数（0 普通 / 1-5 点位类 / 6-8 三种出生点） */
/* 删除「点位」页最后一项"任意"：只扫点位型标记，不含守卫区（区域单独一页）。
 * 老的无类型删除（游戏内 Delete / delete_nearest()）仍是 0 = 任意含区域。 */
#define MT_ANY_POINT (-2)

/* ---- 朝向：蹲守点 / 守卫点 -------------------------------------------------
 * 2026-11-27（用户要求「光显示一个球看不出方向」）：
 *   游戏里这两类点「站定后朝哪看」都存在 zoomPos（Vector3[]）：
 *     Bot_GuardPos.zoomPos@0x10（蹲守点 Bot_CrouchPos 继承同一个字段）
 *     Bot_NanoGuardPos.zoomPos@0x10
 *   原生数据已用 UnityPy 解场景核实：**是世界目标点**，不是单位向量
 *   （实测距离 7~53 m，例如 生化酒店 (-48.5, 5.4, -18.1)）；人机站在点位上朝它看。
 *   守卫区 Init() 还会把 area.entrancePos 并进每个守卫点的 zoomPos ——
 *   所以原生守卫点多数 zoomPos 是空的，实际张望方向来自入口点（实测 沙漠要塞 51 个里
 *   只有 2 个自带 zoomPos）。
 * 我们只存一个角度（度，0=北、90=东，和屏幕罗盘 compass_bucket 同一套约定），
 * 写回游戏时换算成 p + dir*DIR_RANGE 的世界点（同高度 = 只定方向、不定俯仰）。
 * YAW_NONE = 没设过 / 读不到：画虚线 + 菜单写「未知」，绝不默认成 0° 骗人。 */
#define YAW_NONE   (-999.0f)
#define DIR_RANGE  10.0f     /* 写回游戏的视线长度（米）：只用来算方向 */
#define DIR_MAXN   3         /* 一个点多方向时最多画/记 3 个 */

/* 方向向量 → 角度（0=北=-Z，90=东=+X）。和 compass_bucket 同一套约定。 */
static float yaw_of_dir(const V3* d) {
  float y;
  if (!d) return YAW_NONE;
  if (fabsf(d->x) < 1e-4f && fabsf(d->z) < 1e-4f) return YAW_NONE;   /* 正上/正下：没有水平朝向 */
  y = atan2f(d->x, -d->z) * 57.29578f;
  if (y < 0.0f) y += 360.0f;
  if (y >= 360.0f) y -= 360.0f;
  return y;
}
/* 角度 → 水平单位方向（y 恒 0） */
static void dir_of_yaw(float yaw, V3* out) {
  float r = yaw / 57.29578f;
  out->x = sinf(r); out->y = 0.0f; out->z = -cosf(r);
}
/* zoomPos 读写（定义在 make_crouch 前面；read_nano / read_crouch 先用到） */
static int write_zoom(P comp, const V3* p, float yaw);
static int read_zoom(P comp, const V3* p, float* out, int cap);

static float yaw_norm(float yaw) {
  float y = fmodf(yaw, 360.0f);
  if (y < 0.0f) y += 360.0f;
  return y;
}
/* 八分区中文名：复用罗盘那张表，菜单里写「东北 42°」 */
static const char* yaw_zh(float yaw) {
  static const char* const cn[8] = { "北","东北","东","东南","南","西南","西","西北" };
  float a;
  int b;
  if (yaw <= YAW_NONE + 1.0f) return "未知";
  a = yaw_norm(yaw) + 22.5f;
  b = (int)(a / 45.0f) % 8;
  return cn[(b < 0) ? 0 : (b > 7 ? 7 : b)];
}

static MK g_mk[MAXM];
static P  g_aidMk[MAX_AID];
/* 1 = 这个 aid 的守卫区已经激活过（Awake 已跑、SpareAreaList 已登记）。
 * 守卫区建好先不激活：等第一个守卫点挂上去再激活，避免游戏拿到一个
 * "已登记但 posList 空"的守卫区（GetPos 返回 null，人机拿到后空转）。 */
static unsigned char g_areaLive[MAX_AID];
/* 槽位占用表：g_aidMk 里存的是「marker 下标」，下标 0 和「空槽」都是 0，分不清；
 * 单独记一份，删区/换图时清掉，重建时才不会互相覆盖。 */
static unsigned char g_aidUsed[MAX_AID];

/* ---- 出生点编辑（MapManager.SP_BL / SP_GR） --------------------------------
 * 出生点不是场景对象：场景里只有 MapManager.pointDic，Awake 时拆成
 * SP_BL/SP_GR 两个 SpawnPoint[]（元素 16 B = Vector3 + 朝向 float）。
 * 这里改的是运行时的数组，不写原图 —— 插件不在时游戏恢复原版。
 * 每张图的改动记在 markers.txt：
 *   spawn    <team> <x> <y> <z> <yaw>   用户新增的点
 *   spawndel <team> <x> <y> <z>         用户删掉的原生点（按坐标匹配）
 * 进图后 MapManager 就绪时按「原生 - 删除 + 新增」重建数组并写回字段。 */
#define MAX_SPAWN_ORIG 128
#define MAX_SPAWN_EDIT 64
/* 三个出生点数组都要能改（2026-11-27）：
 *   0 = SP_BL（潜伏者 / 生化幽灵）、1 = SP_GR（保卫者 / 生化人类）、
 *   2 = SP_Netural（中立；个人竞技全员 = Neutral，只读这个）。
 * 只改 0/1 的话，个人竞技里"加了出生点却没人出生"——游戏根本不读那两个数组。 */
#define SPAWN_TEAMS 3
typedef struct { V3 p; float yaw; } SPT;
static const int  SPAWN_OFF[SPAWN_TEAMS] = { 0x10, 0x14, 0x18 };   /* MapManager 字段偏移 */
static const char* SPAWN_NAME[SPAWN_TEAMS] = { "BL", "GR", "中立" };
static SPT g_spawnOrig[SPAWN_TEAMS][MAX_SPAWN_ORIG];
static int g_spawnOrigN[SPAWN_TEAMS];
static int g_spawnOrigOk[SPAWN_TEAMS];
static SPT g_spawnAdd[SPAWN_TEAMS][MAX_SPAWN_EDIT];
static int g_spawnAddN[SPAWN_TEAMS];
static SPT g_spawnDel[SPAWN_TEAMS][MAX_SPAWN_EDIT];
static int g_spawnDelN[SPAWN_TEAMS];
static P   g_spawnWritten[SPAWN_TEAMS];   /* 上次写回去的数组；游戏重建后指针会变 */
static P   g_spawnCaptured[SPAWN_TEAMS];  /* 原生数组快照对应的那一份（重进图/重建后要重拍） */
static int  spawn_hook_install(void);    /* 取点钩子（定义在出生点段） */
static void spawn_preload(void);
static int  g_hookOn;                    /* 取点钩子是否已装上（早 tick 要读） */
static P   g_spawnCls;                    /* SpawnPoint（值类型） */
static P   g_spidFld[SPAWN_TEAMS];        /* SPID_BL / SPID_GR / SPID_Netural 静态字段 */
/* 高度基准：原生出生点比"脚下地面"高多少（2026-11-27）。
 * 以前新增点 = 准星地面 + 0.05 m，比游戏自己的出生点低一截 —— 人机/玩家重生在
 * 平台面以下，CharacterController 直接穿下去（运输船上就是掉进虚空）。
 * 现在从本图原生点反推这个高度差，新增点一律按"地面 + 原生高度"摆。 */
static float g_spawnGap;          /* 原生点 y - 脚下地面 y */
static int   g_spawnGapOk;        /* 至少量到一个原生点 */
static int   g_spawnHeightsFixed; /* 本图已经把新增点高度对齐过一次 */

/* ---- 标记 / 出生点的撤销记录（2026-11-26）--------------------------------
 * 「撤销一步」以前只管点图（PointNode / 连边 / 跳链）：蹲守点 / 守卫区 / 守卫点 /
 * 标签 / 出生点的增删一条都不进栈。放完点按撤销，撤掉的是很早以前的一条点图编辑，
 * 或者干脆弹出「nothing to undo」——用户看到的就是「撤销没反应」。
 * 这里单独记一份（和点图共用步号 g_edStep，按步号比较先后），
 * 撤销 = 反做最近那一步；标记重建走 load_file 用的同一套 make_* 函数。 */
#define MKE_MAX 96
#define MKE_ADD 1
#define MKE_DEL 2
typedef struct {
  int step;      /* 撤销步号（和 NAVED.grp 同一套） */
  int kind;      /* MKE_ADD / MKE_DEL */
  int type;      /* MT_CROUCH / MT_TAG / MT_AREA / MT_NANOPOS / MT_JUMP / MT_SPAWN_BL / MT_SPAWN_GR */
  V3  p;         /* 标记位置（出生点 = 出生点坐标） */
  V3  b;         /* 跳链落点（其它类型为 0） */
  int aid, parent, prm;   /* MK 快照 */
  float yaw;     /* 出生点朝向 */
  float jspeed, jacc;     /* 跳链参数（重建时带回去） */
  int jdir;
  int wasAdd;    /* 出生点：删掉的是「本次新增清单」里的点（1）/ 原生点（0） */
  int spawnIdx;  /* 出生点：在 g_spawnAdd 里的下标（wasAdd 时有效） */
} MKE;
static MKE g_mke[MKE_MAX];
static int g_mkeN;
static MKE g_mkeRedo[MKE_MAX];
static int g_mkeRedoN;
static int g_mkeMute;      /* 撤销/重做自己增删标记时不要再记一笔 */
static void mke_note_add(int first);
static void mke_note_del(const MK* m, const NAVED* jump);
static void mke_note_spawn_add(int team, const SPT* s, int idx);
static void mke_note_spawn_del(int team, const SPT* s, int wasAdd, int idx);
/* 换图 / 换包 / 图被重扫：编辑清单整个换掉，撤销 + 重做历史必须一起作废。
 * 不清的话「重做」会把上一张图的条目重新套到新图上（标记也一样）。 */
static void ed_history_reset(void) {
  g_redoN = 0;
  g_mkeN = 0;
  g_mkeRedoN = 0;
  g_dropNext = 0;
}

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

/* 2026-11-26：给 elog 加 printf 格式检查。当天在日志里抓到一条参数少一个的调用
 * （`vis: … guard=%d …`：旧守卫删掉后计数器没了、格式串没跟着改），后面所有参数整体
 * 错位，badtr 打出垃圾值、还把野指针交给 %s 打印 —— 这种错不崩在写日志上也可能崩在
 * 别处，而且写得越久越难查。加上属性后 `-Wall` 会直接把这类调用点标出来。 */
static void elog(const char* fmt, ...) __attribute__((format(printf, 1, 2)));
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

/* ---- 蹲跳驱动（2026-11-27）-------------------------------------------------
 * 录到的蹲跳落在 jump add 第 10~12 列（ct0 / ct1 / ctb）。进图建跳链时把
 * 「起点节点 + 空中起蹲时间」记进这张小表；之后每 ~100 ms 扫一遍人机，只要它
 * 已经在空中、而且 nextJumpStartNode 正是这条链的起点，就把 Bot.crouchEndTime
 * 顶到 now+0.6。游戏自己的 Bot.TryCrouch 每帧算
 *   SetCrouchState(crouchEndTime > Time.time)
 * 所以这里不直接调 SetCrouchState —— 直接调会和游戏每帧的判定打架（蹲住不放）。
 * 关掉：ucf_mod.json 里 "bot_crouchjump": false。
 * 2026-11-27 现场：风暴那道 6.7 m 缺口，人机 5 次全跳了，但都差 10~15 cm
 * 撞在台沿下沿滑到地面；玩家同一条弧线蹲着就上去了。 */
#define CJ_MAX 32
static struct { P startNode; float ct0, ct1; } g_cj[CJ_MAX];
static int g_cjN;

static void cj_remember(P startNode, float ct0, float ct1) {
  int i;
  if (!startNode || g_cjN >= CJ_MAX) return;
  for (i = 0; i < g_cjN; i++) if (g_cj[i].startNode == startNode) return;
  g_cj[g_cjN].startNode = startNode;
  g_cj[g_cjN].ct0 = ct0;
  g_cj[g_cjN].ct1 = ct1;
  g_cjN++;
  elog("crouchjump: 登记蹲跳起点节点 %p（空中蹲 [%.2f, %.2f] s）", startNode, ct0, ct1);
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
/* 撤掉一个对象的根（对象销毁时用）：句柄表是固定 512 格，重建很勤的东西
 * （比如方向层每次换目标点都重建网格）不还句柄的话，几轮就把表占满 ——
 * 满了以后新对象都不再被钉住，GC 一来就可能收掉还在用的网格。
 * 2026-11-27 加。 */
static void root_drop(P o) {
  int i;
  if (!o || !g_rootsN) return;
  for (i = 0; i < g_rootsN; i++) {
    if (g_rootObj[i] != o) continue;
    if (g_rootH[i] && x_gchandle_free) x_gchandle_free(g_rootH[i]);
    g_rootsN--;
    g_rootObj[i] = g_rootObj[g_rootsN];
    g_rootH[i] = g_rootH[g_rootsN];
    g_rootObj[g_rootsN] = 0;
    g_rootH[g_rootsN] = 0;
    if (g_rootsN < ROOTS_MAX) g_rootsFull = 0;
    return;
  }
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
  RESOLVE(field_static_set_value);
  RESOLVE(array_new);
  RESOLVE(array_get_byte_length);
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
  elog("init: core classes ok");
  g_mmCls = find_cls("", "MapManager");
  if (g_mmCls && x_class_get_parent) {
    P base = x_class_get_parent(g_mmCls);
    if (base) g_mmInstField = x_class_get_field_from_name(base, "<instance>k__BackingField");
  }
  /* 出生点编辑：SpawnPoint 值类型 + SPID_BL/GR 静态计数器。
   * SpawnPoint 是全局命名空间的 struct，find_cls 找不到时再从 SP_BL 字段类型反推
   * （和上面 Bot_JumpLink.Link 同一套办法）。 */
  g_spawnCls = 0;
  if (g_mmCls && x_class_get_field_from_name && x_field_get_type &&
      x_class_from_il2cpp_type && x_class_get_element_class) {
    /* 优先从 SP_BL 字段类型反推：拿到的就是 SpawnPoint[] 的元素类，
     * 不会撞上别的程序集里同名的 SpawnPoint。 */
    P f = x_class_get_field_from_name(g_mmCls, "SP_BL");
    P ft = f ? x_field_get_type(f) : 0;
    P ac = ft ? x_class_from_il2cpp_type(ft) : 0;
    if (ac) g_spawnCls = x_class_get_element_class(ac);
  }
  if (!g_spawnCls) g_spawnCls = find_cls("", "SpawnPoint");
  elog("init: spawnCls=%p instance_size=%d value_size_api=%d",
       (void*)g_spawnCls,
       (g_spawnCls && x_class_instance_size) ? x_class_instance_size(g_spawnCls) : -1,
       x_array_get_byte_length ? 1 : 0);
  if (g_mmCls && x_class_get_field_from_name) {
    g_spidFld[0] = x_class_get_field_from_name(g_mmCls, "SPID_BL");
    g_spidFld[1] = x_class_get_field_from_name(g_mmCls, "SPID_GR");
    g_spidFld[2] = x_class_get_field_from_name(g_mmCls, "SPID_Netural");
  }
  elog("init: spawnCls=%p spid=%p/%p/%p", (void*)g_spawnCls,
       (void*)g_spidFld[0], (void*)g_spidFld[1], (void*)g_spidFld[2]);
  /* 出生点取点钩子：RVA 是相对 GameAssembly 的，必须等 g_ga 拿到 —— editor_start
   * 那会儿还没 ed_init，装不了（这就是 2026-11-27 10:54 那次"没装上"的原因）。
   * ed_init 在主线程第一拍跑，这时还没进任何地图，装上去最安全。 */
  if (cfg_bool("spawn_hook", 1)) spawn_hook_install();

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
  if (g_jumpCls) g_jumpType = x_type_get_object(x_class_get_type(g_jumpCls));
  if (g_tagCls) g_tagType = x_type_get_object(x_class_get_type(g_tagCls));

  /* 守卫区 / 守卫点的两个 List<T>.Add 方法：
   *   area.posList      = List<Bot_NanoGuardPos>      （挂新点位）
   *   SpareAreaList     = List<Bot_NanoGuardArea>     （点位被删空后补登记）
   * 泛型实例没法按名字 class_from_name 拿，只能从字段类型反查（同 navfix.c）。 */
  if (g_areaCls && x_class_get_field_from_name && x_field_get_type &&
      x_class_from_il2cpp_type && x_class_get_method_from_name) {
    P f = x_class_get_field_from_name(g_areaCls, "posList");
    P t = f ? x_field_get_type(f) : 0;
    g_nposListCls = t ? x_class_from_il2cpp_type(t) : 0;
    if (g_nposListCls) g_nposListAdd = x_class_get_method_from_name(g_nposListCls, "Add", 1);
    f = x_class_get_field_from_name(g_areaCls, "SpareAreaList");
    t = f ? x_field_get_type(f) : 0;
    {
      P c = t ? x_class_from_il2cpp_type(t) : 0;
      if (c) g_nareaListAdd = x_class_get_method_from_name(c, "Add", 1);
    }
    elog("init: posList=%p posList.Add=%p SpareAreaList.Add=%p",
         g_nposListCls, g_nposListAdd, g_nareaListAdd);
  }
  /* Bot_JumpLink.linkDic 的 Remove：删跳链时反登记用（异常走 exc，不闪退）。 */
  if (g_jumpCls && x_class_get_field_from_name && x_field_get_type &&
      x_class_from_il2cpp_type && x_class_get_method_from_name) {
    P f = x_class_get_field_from_name(g_jumpCls, "linkDic");
    P t = f ? x_field_get_type(f) : 0;
    g_linkDicCls = t ? x_class_from_il2cpp_type(t) : 0;
    if (g_linkDicCls) g_linkDicRemove = x_class_get_method_from_name(g_linkDicCls, "Remove", 1);
    elog("init: linkDic=%p linkDic.Remove=%p", g_linkDicCls, g_linkDicRemove);
  }

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

/* 屏幕中心射线和 transform.forward 的夹角（度）。0 = 相机投影严格居中；
 * 不是 0 说明屏幕中心那条射线和 forward 差一个角度 —— 旧实现（只认 forward）
 * 就是从这儿开始整体偏的。诊断用，不在主循环里打日志。 */
static float g_xrAng = -1.0f;

/* 屏幕中心（准星）射线：Camera.ScreenPointToRay(屏幕中心)。
 * 为什么不用 cam_ray()（相机位置 + transform.forward）：
 * 2026-11-26 用户反馈「连接路径选点，准星和路点之间得有偏差才能选中」。
 * forward 只有在投影矩阵严格居中时才等于准星那条线；相机带镜头位移/投影偏移时
 * （这个游戏用的是 Cinemachine，投影矩阵是后期算的），forward 指向的是「屏幕中心
 * 偏一点」的方向，拿它当准星使，落点就整体偏。ScreenPointToRay 走的是相机真实的
 * projection 矩阵，屏幕中心在哪它就指哪。取不到就退回老路子。 */
static int cam_xray(V3* o, V3* d) {
  P cam = ((cam_main_t)RVA(R_CAM_MAIN))(0);
  int w, h;
  if (!cam) return 0;
  w = ((screen_dim_t)RVA(R_SCREEN_W))(0);
  h = ((screen_dim_t)RVA(R_SCREEN_H))(0);
  if (w > 0 && h > 0) {
    V2 sp;
    RAY ray;
    sp.x = (float)w * 0.5f;
    sp.y = (float)h * 0.5f;
    memset(&ray, 0, sizeof ray);
    ((spr_t)RVA(R_SPR_INJ))(cam, &sp, 2 /* MonoOrStereoscopicEye.Mono */, &ray, 0);
    if (ray.d.x == ray.d.x && ray.d.y == ray.d.y && ray.d.z == ray.d.z) {
      float len = sqrtf(ray.d.x * ray.d.x + ray.d.y * ray.d.y + ray.d.z * ray.d.z);
      if (len > 0.5f && len < 1.5f) {
        V3 fo, ff;
        ray.d.x /= len; ray.d.y /= len; ray.d.z /= len;
        *o = ray.o;
        *d = ray.d;
        if (cam_ray(&fo, &ff)) {
          float dot = d->x * ff.x + d->y * ff.y + d->z * ff.z;
          if (dot > 1.0f) dot = 1.0f; else if (dot < -1.0f) dot = -1.0f;
          g_xrAng = (float)(acos((double)dot) * 57.29577951308232);
        }
        return 1;
      }
    }
  }
  if (!cam_ray(o, d)) return 0;
  g_xrAng = 0.0f;
  return 1;
}

/* 准星落点：屏幕中心射线打到地面/墙上的那个点（放置类功能用它）。
 * ro/rd 可选：把这条准星射线本身带出去，选点的人就不用再算一遍。 */
static int cam_point_ray(V3* out, V3* ro, V3* rd) {
  V3 pos, dir, fw;
  char hit[128];
  raycast_t rc = (raycast_t)RVA(R_RAYCAST);
  if (!cam_xray(&pos, &fw)) return 0;
  if (ro) *ro = pos;
  if (rd) *rd = fw;
  pos.x += fw.x * 0.4f; pos.y += fw.y * 0.4f; pos.z += fw.z * 0.4f;
  if (rc(pos, fw, hit, 300.0f, 1, 0)) { *out = *(V3*)hit; return 1; }
  dir.x = 0.0f; dir.y = -1.0f; dir.z = 0.0f;
  if (rc(pos, dir, hit, 120.0f, 1, 0)) { *out = *(V3*)hit; return 1; }
  return 0;
}

static int cam_point(V3* out) { return cam_point_ray(out, 0, 0); }


/* ---- 采样会话：录制 / 采集共用一套采样器（2026-11-27）---------------------
 * 以前 rec_tick / trace_sample 是两份几乎逐行相同的实现（hz 闸门、里程、相机兜底、
 * 按键、跳跃结算各持一份），同时开会把同一帧采两遍、写两个文件、跳结算两个状态机。
 * 现在只有一个采样会话，录制和采集只是"会话类型"：
 *
 *   cmd=rec     kind=rec     ：控制台「录制」页，结束 → 复盘成点图（要选图选包）
 *   cmd=trace   kind=trace   ：控制台「开发者选项」页，结束 → 只出日志 / 跳跃报告
 *
 * 采谁由 who=player|bots|all 决定（和功能无关）。**同一时刻只有一个写入者**：
 * ss_begin() 先把上一个会话收尾，所以控制台不再需要 stopall（命令仍保留兼容旧版）。
 * 录制的文件本来就是可分析的原始轨迹（同一格式），所以「忘了开采集」不用重录。
 *
 * 文件格式 ucf-trace/3（样本行和 2 版完全一样，header 多一个 who）：
 *   {"kind":"rec","schema":"ucf-trace/3","who":"player","hz":30,
 *    "t0":"2026-11-27 12:00:00","scene":"mp_x","map":"level1","label":"运输船",
 *    "pack":"...","fp":"...","src":"player","notes":"..."（字段表也在 header 里）}
 *   样本   {"t":12.345,"dt":0.033,"x":-52.8,"y":-16.59,"z":3.63,"g":1,"vy":0.02,"sp":0,"ct":0}
 *   人机   {"t":12.4,"k":"b","id":"0a1b2c3d","x":..,"y":..,"z":..,"spd":6.2,"act":".."}
 *   跳事件 {"t":12.9,"ev":"jump","a":[..],"b":[..],"h":..,"rise":..,"air":..,"v0":..,"run":..,"kind":"mount"}
 *   分段/场景 {"t":12.3,"ev":"cam"} / {"t":12.3,"ev":"scene","n":".."}；末行 end
 *
 * 时间用 QueryPerformanceCounter（60 Hz 下 GetTickCount64 的 1 ms 粒度太粗）。
 * 坐标是玩家脚底（Player.characterContainer）；拿不到玩家对象就退回相机 + 眼高估算，
 * header 写 src=camera，分析端一眼能看出这份数据能不能当准。
 */
#define SS_REC       1
#define SS_TRACE     2
#define SS_SCHEMA    "ucf-trace/3"
#define SS_BOT_HZ    10

typedef struct { V3 pos; int grounded; double vy; int ct; } PlSt;

/* 跳跃结算状态机：录制 / 采集各持一个实例（同一套判据：起跳看竖直速度，
 * 落地看游戏自己的 isGrounded）。
 * 2026-11-27 加蹲：ct0/ct1 是「空中开始 / 结束蹲」相对起跳的秒数（-1 = 没蹲 / 蹲到落地），
 * ctb = 起跳那一帧是不是已经蹲着。事件里带出去，复盘落盘进 jump add 的第 10~12 列。 */
typedef struct {
  FILE*  fp;
  int    air;                 /* 1 = 已起跳、等落地结算 */
  V3     prev;                /* 上一帧脚底（起跳点要从这里取） */
  int    hasPrev, grounded;   /* 上一帧有没有样本 / 在不在地面 */
  V3     a;                   /* 起跳点 */
  double t0, apex, v0, run, lastT;
  int    n, mount, gap, down, hop;
  double ct0, ct1;            /* 空中蹲的起止（相对起跳秒，-1 = 没有） */
  int    ctb, ctOn, prevCt;   /* 起跳时是否蹲着 / 空中现在蹲着 / 上一帧的蹲 */
} JumpRec;

/* 采样定时器（navfix.c 的 WM_TIMER 0xF3C1）：以前只在车测自由视角启动，所以
 * 正常游戏里只有 250 ms 心跳那 4 Hz。开始采样时借一次，停止时还掉（navfix 内部
 * 引用计数；没人在用时定时器关掉，不白耗 CPU）。
 * 借还只是「有机会采样」，真正的采样时刻由下面 ss_tick() 按 hz 闸门定 ——
 * 定时器快了不会被多记，游戏卡了也不会把样本挤成一串。 */
void navfix_hires_acquire(void);
void navfix_hires_release(void);
long navfix_hires_ticks(void);       /* WM_TIMER 到过的累计次数（自检用） */

/* 采样率自检：实测明显低于档位就大声喊一句。
 * 2026-11-24 的教训是「档位 60 Hz、实际 4 Hz」只在控制台状态条上显示，日志里
 * 一点痕迹都没有，三方（用户 / 控制台 / AI）谁都没看出是采样没跑满。 */
static void hz_warn(const char* who, unsigned n, double dur, int hz, long ticks) {
  double got;
  if (dur <= 2.0) return;                        /* 太短不算数 */
  got = (double)n / dur;
  if (got + 0.5 >= (double)hz * 0.75) return;
  elog("%s: !!! 采样没跑满：档位 %d Hz，实测 %.1f Hz（定时器派发 %ld 次 = %.1f/s）"
       " —— 多半是 ①游戏帧率不足 ②WM_TIMER 被主循环卡住 ③跑的还不是新 DLL",
       who, hz, got, ticks, dur > 0.2 ? (double)ticks / dur : 0.0);
}

/* ---- 会话状态（唯一一份） ---- */
typedef struct {
  FILE*  fp;
  char   path[MAX_PATH];
  int    on, paused;          /* 在采 / 暂停（暂停只对录制页开放，采集页没有按钮） */
  int    kind;                /* SS_REC / SS_TRACE（只影响 header 和日志） */
  int    hz;                  /* 玩家采样档位 */
  int    who;                 /* 1=玩家 2=人机 3=全部 */
  int    hdr, srcMode;        /* header 写没写 / 坐标来源（1=player 2=camera） */
  unsigned n;                 /* 玩家样本数 */
  unsigned bn;                /* 人机样本行数（只采人机时 n=0，报表要看 bn） */
  int    missed;              /* 调度落后 >0.5 s 的次数 */
  double dist, prevT, nextT, sceneT;
  V3     prev;
  int    hasPrev;
  P      obj;                 /* 上一帧的玩家对象（换图/重生会变，写一行 ev=cam 断段） */
  char   scene[64];
  char   meta[4][192];        /* map / label / pack / fp（navcmd 的 GBK 原文） */
  LARGE_INTEGER t0q, freq;
  long   tick0;               /* 开始采样时的定时器计数（算这次采到多少机会） */
  JumpRec jump;
  unsigned long long botNext; /* 人机采样闸门（SS_BOT_HZ） */
} SampleSess;

static SampleSess g_ss;

static void ss_sample_bots(void);            /* 定义在 bot 工具函数之后（依赖那一段） */

/* navcmd 是 GBK 写的；日志统一 UTF-8，中文图名 / 包名才不会变乱码。
 * 顺带把 " \ 和回车转义掉，保证每一行都是合法 JSON。 */
static void tr_json(const char* s, char* out, int cap) {
  wchar_t w[256];
  char u8[768];
  int i, j = 0, n;
  out[0] = 0;
  if (!s || !s[0] || cap < 4) return;
  u8[0] = 0;
  n = MultiByteToWideChar(CP_ACP, 0, s, -1, w, 256);
  if (n > 0 && WideCharToMultiByte(CP_UTF8, 0, w, -1, u8, sizeof u8, 0, 0) <= 0)
    u8[0] = 0;
  if (!u8[0]) {
    strncpy(u8, s, sizeof u8 - 1);
    u8[sizeof u8 - 1] = 0;
  }
  for (i = 0; u8[i] && j < cap - 2; i++) {
    unsigned char c = (unsigned char)u8[i];
    if (c == '"' || c == '\\') { out[j++] = '\\'; out[j++] = (char)c; }
    else if (c < 0x20) out[j++] = ' ';
    else out[j++] = (char)c;
  }
  out[j] = 0;
}

/* ---- 玩家状态读数（拿不到就退回相机 + 眼高估算）---- */
#define R_PL_ISMY     0xB55FD0        /* Player.get_isMyPlayer() -> bool          */
#define PL_CHAR_CONT  0x58            /* Transform characterContainer             */
#define PL_GROUNDED   0x70            /* bool isGrounded                          */
#define PL_VELDATA    0x90            /* PlayerVelocity* velData                  */
#define PV_VELOCITY   0x0C            /* Vector3 velocity（每小时 1 个 Vector3）   */
static P      g_plCls, g_plType, g_trPlayer;
static double g_trEye = 2.29;         /* 相机 − 脚底；只在退回相机时用 */

static void map_name_from_minimap(char* out, int cap);   /* 定义在后面 */

/* 会话内相对时间（秒）。t0q 在第一个样本落盘时重置，所以大厅里等的时间不计入。 */
static double ss_now(void) {
  LARGE_INTEGER c;
  QueryPerformanceCounter(&c);
  if (!g_ss.freq.QuadPart) return 0.0;
  return (double)(c.QuadPart - g_ss.t0q.QuadPart) / (double)g_ss.freq.QuadPart;
}

/* ---- 本地玩家 ----------------------------------------------------------
 * 2026-11-24 采样改造：坐标改成"玩家脚底"，不再用相机（相机比脚底高 2.3 m，
 * 蹲下还会变，用它算跳高/落点会系统性偏）。
 * 拿玩家靠 find_objs(Player) + get_isMyPlayer（RVA 见 dump.cs 234492），
 * 每 2 s 最多找一次，指针靠 m_CachedPtr 判活；拿不到就退回相机估算并在
 * header 里写 "src":"camera"，分析端能一眼看出这份数据能不能当准。 */
static void tr_player_lookup(void) {
  P arr;
  int n, i;
  if (!g_plType) {
    if (!g_plCls) g_plCls = find_cls("", "Player");
    if (g_plCls && x_class_get_type && x_type_get_object)
      g_plType = x_type_get_object(x_class_get_type(g_plCls));
    if (!g_plType) return;
  }
  arr = ((find_objs_t)RVA(R_FINDOBJS))(g_plType, 1, 0);
  if (!arr) return;
  n = *(int*)((char*)arr + 0xC);
  if (n <= 0 || n > 256) return;
  for (i = 0; i < n; i++) {
    P pl = *(P*)((char*)arr + 0x10 + i * 4);
    if (!pl || !uobj_live(pl)) continue;
    /* 返回值是 il2cpp 的 bool（只有 AL 有效），按 int 收会把高位垃圾当成 true，
     * 可能挑到一个人机的 Player —— 必须用 unsigned char。 */
    if (((unsigned char(*)(P))RVA(R_PL_ISMY))(pl)) { g_trPlayer = pl; return; }
  }
}

static P tr_player(void) {
  static unsigned long long lastTry;
  unsigned long long now;
  if (g_trPlayer && uobj_live(g_trPlayer)) return g_trPlayer;
  g_trPlayer = 0;
  now = GetTickCount64();
  if (lastTry && now - lastTry < 2000) return 0;   /* 找不到别每帧扫全场景 */
  lastTry = now;
  tr_player_lookup();
  return g_trPlayer;
}

static int tr_read_player(P pl, PlSt* st) {
  P tr, vel;
  if (!pl || !uobj_live(pl)) return 0;
  tr = *(P*)((char*)pl + PL_CHAR_CONT);
  if (!tr || !mem_ok(tr, 0x20)) return 0;
  ((get_pos_t)RVA(R_GET_POS_INJ))(tr, &st->pos, 0);
  if (!isfinite(st->pos.x) || !isfinite(st->pos.y) || !isfinite(st->pos.z)) return 0;
  if (fabsf(st->pos.x) > 100000.0f || fabsf(st->pos.z) > 100000.0f) return 0;
  st->grounded = (*(unsigned char*)((char*)pl + PL_GROUNDED) != 0);
  st->vy = 0.0;
  vel = *(P*)((char*)pl + PL_VELDATA);
  if (vel && mem_ok(vel, PV_VELOCITY + 12)) st->vy = *(float*)((char*)vel + PV_VELOCITY + 4);
  return 1;
}

/* ---- 跳跃结算 ----------------------------------------------------------
 * 2026-11-24：起跳判据从"离地 0.3 m"换成**竖直速度**（游戏 JumpPower = 10.5，
 * 玩家实测 9.5~10.5），落地用游戏自己的 isGrounded。落地那一帧直接结算一行事件：
 *   {"t":32.490,"ev":"jump","a":[起跳点],"b":[落点],"h":水平跳距,"rise":跳高,
 *    "air":滞空,"v0":起跳竖直速度,"run":起跳水平速度,"kind":"gap|mount|down|hop"}
 * kind：h < 0.5 = hop（原地小跳）；落点比起点高 0.5 m 以上 = mount（跳上高台/箱子）；
 *       低 0.5 m 以上 = down（跳下）；否则 gap（同高度跨缺口）。 */
static void jr_reset(JumpRec* j, FILE* fp) {
  memset(j, 0, sizeof *j);
  j->fp = fp;
}

static void jr_line(JumpRec* j, const PlSt* st, double t) {
  double h, dy, rise, air;
  const char* kind;
  V3 a = j->a, b = st->pos;
  if (!j->fp) return;
  air = t - j->t0;
  if (air < 0.06 || air > 3.0) return;
  h = sqrt((double)(b.x - a.x) * (b.x - a.x) + (double)(b.z - a.z) * (b.z - a.z));
  dy = (double)b.y - (double)a.y;
  rise = j->apex - (double)a.y;
  if (h < 0.5) kind = "hop";
  else if (dy > 0.5) kind = "mount";
  /* 2026-11-27：主动起跳优先于「跳下」。v0 够大 + 滞空够久就是真跳，落点低一点也按 gap；
   * 否则蹲跳 / 跨缺口落到低 0.5~1 m 的台子会被记成 down，然后因为落差不够 2 m 被静默丢掉
   * （11-27 风暴那次 6.93 m 蹲跳就是这么没的）。判据和 ucf_rec._kind 必须一致。 */
  else if (j->v0 >= 9.0 && air >= 0.3) kind = "gap";
  else if (dy < -0.5) kind = "down";
  else kind = "gap";
  if (!strcmp(kind, "gap")) j->gap++;
  else if (!strcmp(kind, "mount")) j->mount++;
  else if (!strcmp(kind, "down")) j->down++;
  else j->hop++;
  j->n++;
  fprintf(j->fp, "{\"t\":%.3f,\"ev\":\"jump\",\"a\":[%.3f,%.3f,%.3f],"
                 "\"b\":[%.3f,%.3f,%.3f],\"h\":%.3f,\"rise\":%.3f,"
                 "\"air\":%.3f,\"v0\":%.1f,\"run\":%.1f,\"kind\":\"%s\","
                 "\"ct\":[%.3f,%.3f],\"ctb\":%d}\n",
          t, a.x, a.y, a.z, b.x, b.y, b.z, h, rise, air, j->v0, j->run, kind,
          j->ct0, j->ct1, j->ctb);
}

static void jr_step(JumpRec* j, const PlSt* st, double t, double run) {
  if (!j->air) {
    if (st->vy > 6.0 && j->hasPrev && j->grounded) {
      j->air = 1;
      j->a = j->prev;                 /* 离地前最后一个接地样本 = 起跳点 */
      j->t0 = j->lastT;
      j->v0 = st->vy;
      j->run = run;
      j->apex = j->prev.y;            /* 跳高基准 = 起跳脚底 */
      j->ctb = j->prevCt;             /* 起跳前那一帧蹲着 = 「蹲着起跳」 */
      j->ct0 = -1.0;
      j->ct1 = -1.0;
      j->ctOn = 0;
    }
  } else {
    if ((double)st->pos.y > j->apex) j->apex = st->pos.y;
    /* 空中蹲的起止：只记「离地 -> 落地」这一段；落地后的蹲行不算进这一跳 */
    if (st->ct) {
      if (!j->ctOn) {
        j->ctOn = 1;
        if (j->ct0 < 0.0) j->ct0 = t - j->t0;
      }
    } else if (j->ctOn) {
      j->ctOn = 0;
      if (j->ct1 < 0.0) j->ct1 = t - j->t0;
    }
    if (st->grounded && (t - j->t0) > 0.06) {
      jr_line(j, st, t);
      j->air = 0;
    } else if (t - j->t0 > 3.0) {
      j->air = 0;                     /* 卡住 / 掉进虚空：这一跳作废 */
    }
  }
  j->prev = st->pos;
  j->hasPrev = 1;
  j->grounded = st->grounded;
  j->lastT = t;
  j->prevCt = st->ct;
}

/* 读一帧玩家状态：1 = 从玩家对象读到，2 = 退回相机 + 眼高估算，0 = 这一帧拿不到。
 * 相机模式的射线只用来判"是否在地面"和跟住眼高，绝不再当成坐标高度
 * （它会被楼层/平台骗，2026-11-24 实测一帧能跳 9.5 m）。 */
static int tr_read_state(PlSt* st, P* objOut) {
  V3 camPos, dir;
  char hb[128];
  P cam, go, tr;
  double gap = 0.0;
  int hit = 0;
  P obj = tr_player();
  if (obj && tr_read_player(obj, st)) {
    if (objOut) *objOut = obj;
    return 1;
  }
  cam = ((cam_main_t)RVA(R_CAM_MAIN))(0);
  if (!cam) return 0;
  go = ((get_go_t)RVA(R_GETGO))(cam, 0);
  tr = get_tr(go);
  if (!tr) return 0;
  ((get_pos_t)RVA(R_GET_POS_INJ))(tr, &camPos, 0);
  dir.x = 0.0f; dir.y = -1.0f; dir.z = 0.0f;
  if (((raycast_t)RVA(R_RAYCAST))(camPos, dir, hb, 120.0f, 1, 0)) {
    gap = (double)camPos.y - (double)((V3*)hb)->y;
    hit = 1;
  }
  st->grounded = 0;
  if (hit && fabs(gap - g_trEye) < 0.35) {
    st->grounded = 1;
    g_trEye += (gap - g_trEye) * 0.02;
  }
  st->pos.x = camPos.x;
  st->pos.y = (float)((double)camPos.y - g_trEye);
  st->pos.z = camPos.z;
  st->vy = 0.0;      /* 相机模式没有真实竖直速度：调用方用相邻两帧的位移补 */
  if (objOut) *objOut = cam;
  return 2;
}

/* ---- header / stop / begin -------------------------------------------- */
static const char* ss_kind_name(void) { return (g_ss.kind == SS_REC) ? "rec" : "trace"; }

static const char* ss_who_name(void) {
  return (g_ss.who == 1) ? "player" : ((g_ss.who == 2) ? "bots" : "all");
}

/* 第一行：字段表自描述。第一个样本落盘时才写 —— 这时才知道图名、也才知道
 * 坐标到底是玩家脚底还是相机估算。 */
static void ss_header(void) {
  SYSTEMTIME st;
  char sc[72], map[384], lab[384], pk[384], fp[128];
  const char* srcName = (g_ss.srcMode == 1) ? "player" : "camera";
  GetLocalTime(&st);
  map_name_from_minimap(sc, sizeof sc);
  if (sc[0]) strcpy(g_ss.scene, sc);
  tr_json(g_ss.meta[0], map, sizeof map);
  tr_json(g_ss.meta[1], lab, sizeof lab);
  tr_json(g_ss.meta[2], pk, sizeof pk);
  tr_json(g_ss.meta[3], fp, sizeof fp);
  fprintf(g_ss.fp,
          "{\"kind\":\"%s\",\"schema\":\"" SS_SCHEMA "\",\"who\":\"%s\",\"hz\":%d,"
          "\"t0\":\"%04d-%02d-%02d %02d:%02d:%02d\",\"scene\":\"%s\","
          "\"map\":\"%s\",\"label\":\"%s\",\"pack\":\"%s\",\"fp\":\"%s\","
          "\"src\":\"%s\","
          "\"fields\":[\"t\",\"dt\",\"x\",\"y\",\"z\",\"g\",\"vy\",\"sp\",\"ct\"],"
          "\"notes\":\"t/dt s; xyz = player feet in world; g = grounded 1/0; "
          "vy = vertical speed m/s; sp/ct = space/ctrl; "
          "jump event line: {t,ev:jump,a:[x,y,z] takeoff,b:[x,y,z] landing,h,rise,air,v0,run,kind,"
          "ct:[c0,c1] crouch start/end in air (s from takeoff, -1 = none),ctb: crouched at takeoff}; "
          "bot line: {t,k:b,id,spd,act,tgt}\","
          "\"kind_note\":\"gap = 同高度跨缺口, mount = 跳上高台, down = 跳下, hop = 原地小跳\"}\n",
          ss_kind_name(), ss_who_name(), g_ss.hz,
          st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond,
          g_ss.scene, map, lab, pk, fp, srcName);
  g_ss.hdr = 1;
}

static void ss_stop(const char* why) {
  double dur;
  long ticks;
  if (!g_ss.fp) { g_ss.on = g_ss.paused = 0; return; }
  dur = ss_now();
  ticks = navfix_hires_ticks() - g_ss.tick0;
  if (g_ss.hdr)
    fprintf(g_ss.fp, "{\"end\":1,\"t\":%.3f,\"n\":%u,\"bots\":%u,\"dist\":%.2f,"
                     "\"missed\":%d,\"ticks\":%ld,\"jumps\":%d}\n",
            dur, g_ss.n, g_ss.bn, g_ss.dist, g_ss.missed, ticks, g_ss.jump.n);
  fflush(g_ss.fp);
  fclose(g_ss.fp);
  g_ss.fp = 0;
  g_ss.on = g_ss.paused = 0;
  g_ss.jump.air = 0;                  /* 半空停止：这一跳不结算（样本还在，离线可算） */
  g_ss.jump.fp = 0;
  navfix_hires_release();
  elog("sample: stop kind=%s (%s) samples=%u bots=%u dur=%.1fs avg=%.1fHz missed=%d ticks=%ld "
       "jumps=%d (gap=%d mount=%d down=%d hop=%d) who=%s src=%s -> %s",
       ss_kind_name(), why, g_ss.n, g_ss.bn, dur, dur > 0.2 ? (double)g_ss.n / dur : 0.0,
       g_ss.missed, ticks, g_ss.jump.n, g_ss.jump.gap, g_ss.jump.mount,
       g_ss.jump.down, g_ss.jump.hop, ss_who_name(),
       g_ss.srcMode == 1 ? "player" : "camera", g_ss.path);
  if (g_ss.n > 1) hz_warn(ss_kind_name(), g_ss.n, dur, g_ss.hz, ticks);
}

static int ss_begin(int kind, const char* path, int hz, int who,
                    const char* map, const char* label, const char* pack, const char* fp) {
  PlSt st;
  if (!path || !path[0]) {
    elog("%s: start without out= path", kind == SS_REC ? "rec" : "trace");
    return 0;
  }
  if (strlen(path) >= sizeof g_ss.path) {
    elog("%s: path too long", kind == SS_REC ? "rec" : "trace");
    return 0;
  }
  ss_stop("restart");                  /* 一个写入者：接管前先把上一个会话收尾 */
  strcpy(g_ss.path, path);
  g_ss.fp = fopen(g_ss.path, "wb");
  if (!g_ss.fp) {
    elog("%s: cannot create %s", kind == SS_REC ? "rec" : "trace", g_ss.path);
    return 0;
  }
  navfix_hires_acquire();
  g_ss.tick0 = navfix_hires_ticks();
  g_ss.kind = kind;
  g_ss.hz = (hz >= 5 && hz <= 120) ? hz : 30;
  g_ss.who = (who & 3) ? (who & 3) : 1;
  g_ss.on = 1; g_ss.paused = 0;
  g_ss.hdr = 0; g_ss.srcMode = 0;
  g_ss.n = 0; g_ss.bn = 0; g_ss.missed = 0; g_ss.dist = 0.0;
  g_ss.hasPrev = 0; g_ss.prevT = 0.0; g_ss.nextT = 0.0; g_ss.sceneT = 0.0;
  g_ss.obj = 0; g_ss.scene[0] = 0; g_ss.botNext = 0;
  strncpy(g_ss.meta[0], map ? map : "", sizeof g_ss.meta[0] - 1);
  g_ss.meta[0][sizeof g_ss.meta[0] - 1] = 0;
  strncpy(g_ss.meta[1], label ? label : "", sizeof g_ss.meta[1] - 1);
  g_ss.meta[1][sizeof g_ss.meta[1] - 1] = 0;
  strncpy(g_ss.meta[2], pack ? pack : "", sizeof g_ss.meta[2] - 1);
  g_ss.meta[2][sizeof g_ss.meta[2] - 1] = 0;
  strncpy(g_ss.meta[3], fp ? fp : "", sizeof g_ss.meta[3] - 1);
  g_ss.meta[3][sizeof g_ss.meta[3] - 1] = 0;
  jr_reset(&g_ss.jump, g_ss.fp);
  QueryPerformanceFrequency(&g_ss.freq);
  QueryPerformanceCounter(&g_ss.t0q);
  {  /* 先试玩家对象：拿到就能写脚底坐标 + 真实 grounded / vy */
    g_trPlayer = 0;
    if (tr_player() && tr_read_player(g_trPlayer, &st)) {
      V3 camPos;
      P cam = ((cam_main_t)RVA(R_CAM_MAIN))(0);
      g_ss.srcMode = 1;
      camPos.x = camPos.y = camPos.z = 0.0f;
      if (cam) {
        P go = ((get_go_t)RVA(R_GETGO))(cam, 0);
        P ctr = get_tr(go);
        if (ctr) ((get_pos_t)RVA(R_GET_POS_INJ))(ctr, &camPos, 0);
      }
      /* 一行标定：玩家容器 vs 相机，差多少就是"眼睛比脚底高多少" —— 第一次跑完看这行
       * 就知道 characterContainer 是不是脚底；就算它是模型胸口，也是常量偏移，
       * 跳高/高差都是差值，不受影响。 */
      elog("%s: player=%p feet=(%.2f %.2f %.2f) grounded=%d vy=%.2f cam=(%.2f %.2f %.2f) dy=%.2f",
           ss_kind_name(), (void*)g_trPlayer, st.pos.x, st.pos.y, st.pos.z,
           st.grounded, st.vy, camPos.x, camPos.y, camPos.z,
           cam ? (double)camPos.y - (double)st.pos.y : 0.0);
    } else {
      g_ss.srcMode = 2;
      elog("%s: player object NOT found - 退回相机坐标 + 眼高估算（header src=camera）",
           ss_kind_name());
    }
  }
  elog("sample: start kind=%s %d Hz who=%s (timer ticks=%ld) -> %s",
       ss_kind_name(), g_ss.hz, ss_who_name(), g_ss.tick0, g_ss.path);
  return 1;
}

/* ---- 采样 ------------------------------------------------------------- */
/* 玩家：一个样本一行（字段表见 header 的 fields），落地那一帧插件多写一行 ev=jump。
 * 换玩家对象（换图 / 重生）写 ev=cam 断段；场景名变了每秒最多写一行 ev=scene。 */
static void ss_sample_player(void) {
  PlSt st;
  P obj;
  double t, dt, run;
  int sp, ct, src;

  if (!g_ss.fp || !(g_ss.who & 1)) return;
  t = ss_now();
  src = tr_read_state(&st, &obj);
  if (!src) return;
  if (!g_ss.hdr) {
    /* 第一个样本才写 header：这时才知道图名、也才知道坐标来源。
     * 同时把时间原点挪到这里 —— 在大厅等的那几分钟不该算进轨迹。 */
    g_ss.srcMode = (src == 1) ? 1 : 2;
    QueryPerformanceCounter(&g_ss.t0q);
    g_ss.nextT = 1.0 / (double)g_ss.hz;      /* 下一条按正常间隔来 */
    g_ss.sceneT = 0.0;
    t = 0.0;
    ss_header();
  }
  if (src == 2 && g_ss.hasPrev && t > g_ss.prevT + 0.0005)   /* 相机模式：速度靠差分 */
    st.vy = ((double)st.pos.y - (double)g_ss.prev.y) / (t - g_ss.prevT);
  if (obj != g_ss.obj) {
    if (g_ss.obj) {
      fprintf(g_ss.fp, "{\"t\":%.3f,\"ev\":\"cam\"}\n", t);
      g_ss.jump.air = 0;                      /* 换图时半空的跳不结算 */
    }
    g_ss.obj = obj;
    g_ss.hasPrev = 0;
  }
  /* 场景名（小地图贴图名）变了也留一行；每秒最多查一次 */
  if (t - g_ss.sceneT >= 1.0) {
    char sc[72];
    g_ss.sceneT = t;
    map_name_from_minimap(sc, sizeof sc);
    if (sc[0] && strcmp(sc, g_ss.scene)) {
      char esc[160];
      tr_json(sc, esc, sizeof esc);
      strcpy(g_ss.scene, sc);
      fprintf(g_ss.fp, "{\"t\":%.3f,\"ev\":\"scene\",\"n\":\"%s\"}\n", t, esc);
    }
  }
  dt = g_ss.hasPrev ? t - g_ss.prevT : 0.0;
  if (dt < 0.0) dt = 0.0;
  run = (g_ss.hasPrev && dt > 0.0005)
          ? sqrt(((double)st.pos.x - g_ss.prev.x) * ((double)st.pos.x - g_ss.prev.x) +
                 ((double)st.pos.z - g_ss.prev.z) * ((double)st.pos.z - g_ss.prev.z)) / dt
          : 0.0;
  if (g_ss.hasPrev) {
    double dx = (double)st.pos.x - g_ss.prev.x, dz = (double)st.pos.z - g_ss.prev.z;
    double dd = sqrt(dx * dx + dz * dz);
    if (dd < 20.0) g_ss.dist += dd;           /* 传送 / 换图不计进里程 */
  }
  sp = (GetAsyncKeyState(VK_SPACE) & 0x8000) ? 1 : 0;
  ct = (GetAsyncKeyState(VK_CONTROL) & 0x8000) ? 1 : 0;
  st.ct = ct;                                 /* 跳事件按这一帧的蹲状态结算（空中蹲） */
  jr_step(&g_ss.jump, &st, t, run);           /* 起跳/落地结算（录制和采集同一套） */
  fprintf(g_ss.fp, "{\"t\":%.3f,\"dt\":%.3f,\"x\":%.3f,\"y\":%.3f,\"z\":%.3f,"
                   "\"g\":%d,\"vy\":%.2f,\"sp\":%d,\"ct\":%d}\n",
          t, dt, st.pos.x, st.pos.y, st.pos.z, st.grounded ? 1 : 0, st.vy, sp, ct);
  g_ss.prev = st.pos;
  g_ss.hasPrev = 1;
  g_ss.prevT = t;
  g_ss.n++;
  if ((g_ss.n % 32) == 0) fflush(g_ss.fp);     /* 控制台 0.5 s 读一次 */
  if ((g_ss.n % 300) == 0)
    elog("sample: %u samples, %.1f m, %.1f s, jumps=%d", g_ss.n, g_ss.dist, t, g_ss.jump.n);
}

/* 采样闸门：按 hz 定采样时刻。25% 提前量是 2026-11-24 实测定下来的 ——
 * WM_TIMER 只在游戏主循环泵消息时派发，档位接近帧率时（60 Hz 配 60 fps）
 * 严格「到点才采」会因为 ±1 帧抖动隔三差五丢一帧，实测只有 ~50 Hz。
 * 时间表仍是绝对的（nextT += iv），所以平均频率不会跑偏。 */
static void ss_tick(void) {
  double now, iv;
  if (!g_ss.on || !g_ss.fp || g_ss.paused) return;
  if (g_ss.who & 2) ss_sample_bots();        /* 人机：自己还有 SS_BOT_HZ 闸门 */
  if (!(g_ss.who & 1)) return;
  now = ss_now();
  iv = 1.0 / (double)g_ss.hz;
  if (now + iv * 0.25 < g_ss.nextT) return;
  if (now - g_ss.nextT > 0.5) {
    g_ss.nextT = now;                        /* 卡顿超过 0.5 s：重新对齐，记一次 missed */
    g_ss.missed++;
  } else {
    g_ss.nextT += iv;
  }
  if (g_ss.nextT < now) g_ss.nextT = now + iv;
  ss_sample_player();
}

/* navfix 的采样定时器（10 ms）也调一次：editor_tick 只跟着 4 Hz 心跳走，
 * 只靠它会录成 4 Hz；这里补到 ~100 次/秒的机会（ss_tick 自己按 hz 闸门采，
 * 重复调用没事）。名字沿用 editor_rec_tick：navfix.c 只认这个入口。 */
void editor_rec_tick(void) {
  ss_tick();
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
  /* 上一次一个候选都没拿到：冷却 1 秒再试（换图瞬间 shader 可能还没加载回来），
   * 冷却期一过就重试，别一失败就整局不画；也不会每帧跑 8 次 Shader.Find。 */
  if (g_matSetupFailMs && GetTickCount() - g_matSetupFailMs < 1000) return 0;
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
      g_matProtoH = x_gchandle_new ? x_gchandle_new(m, 1) : 0;
      g_matSetupFailMs = 0;
      g_matReady = 1;
      strncpy(g_shaderName, cand[i], sizeof(g_shaderName) - 1);
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
        g_matProtoH = x_gchandle_new ? x_gchandle_new(m, 1) : 0;
        g_matSetupFailMs = 0;
        g_matReady = 1;
        str_ascii(((get_name_t)RVA(R_OBJ_NAME))(src, 0), nm, sizeof(nm));
        elog("mat: cloned scene material '%s'", nm);
        return 1;
      }
    }
  }
  elog("mat: no usable shader - markers stay invisible");
  g_matSetupFailMs = GetTickCount();
  if (!g_matSetupFailMs) g_matSetupFailMs = 1;   /* 0 是"没失败"，别撞上 */
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
  /* root: C globals are not GC roots。句柄要存下来，换图时 mat_reset 才能还回去
   * （以前是建了句柄就丢，每换一张图漏 15 个）。 */
  g_matSlotH[slot] = x_gchandle_new ? x_gchandle_new(m, 1) : 0;
  return m;
}

/* ---- 材质有效性 / 换图重建 ------------------------------------------------
 * 2026-11-20：同一张图、同一个 DLL，两次启动一次线框是绿的、一次是洋红 #FF00FF。
 * 取色证实洋红不是调色板里的任何颜色，而是 Unity 对「没有 shader 的材质」的兜底
 * 错误材质（Hidden/InternalErrorShader）。根因：g_matSlot 是「这一局第一张图」
 * 建的那套材质，换图只重建网格、从不重建材质（vis_scene_reset 只清网格和计数），
 * 旧材质的 shader 随场景资源卸载后就一直失效 —— 整局洋红，重启才重掷一次。
 * 处理：① 换图时把材质缓存整批丢掉，下一张图重新 Shader.Find + 上色；
 *       ② 用之前自检一次，死了就地重建，重建不出来就这一帧不画，
 *          绝不把网格挂到坏材质上（那条路必出洋红）。
 * ------------------------------------------------------------------------- */
static int mat_alive(P m) {
  P sh;
  if (!m || !uobj_live(m)) return 0;                 /* 材质对象本身被销毁 */
  sh = ((get_shader_t)RVA(R_MAT_GETSH))(m, 0);
  if (!sh || !uobj_live(sh)) return 0;               /* shader 被卸载 */
  return 1;
}

static void mat_drop(int slot) {
  if (slot < 1 || slot > 15) return;
  if (g_matSlotH[slot] && x_gchandle_free) x_gchandle_free((P)g_matSlotH[slot]);
  g_matSlotH[slot] = 0;
  g_matSlot[slot] = 0;
}

/* 换图 / 检测到材质失效：整批丢掉，下一帧按当前场景重新建 */
static void mat_reset(const char* why) {
  int i, n = 0;
  for (i = 1; i <= 15; i++) { if (g_matSlot[i]) n++; mat_drop(i); }
  if (g_matProtoH && x_gchandle_free) x_gchandle_free((P)g_matProtoH);
  g_matProtoH = 0;
  g_matProto = 0;
  g_matReady = 0;
  g_matSetupFailMs = 0;
  g_shaderName[0] = 0;
  g_tintLogged = 0;
  g_matDeadLog = 0;
  if (n) elog("mat: reset %d slot(s) (%s) - rebuild for this scene", n, why);
}

static void tint(P go, int slot) {
  P rend, mat;
  if (!go || !g_rendType) return;
  rend = ((getcomp_t)RVA(R_GETCOMP))(go, g_rendType, 0);
  if (!rend) return;
  ((set_int1_t)RVA(R_REND_SHADOW))(rend, 0, 0);      /* no shadows */
  mat = mat_for(slot);
  if (mat && !mat_alive(mat)) { mat_drop(slot); g_matReady = 0; mat = mat_for(slot); }
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
  /* 2026-11-26：不再看 g_vis —— 球一律建出来，显隐统一交给 mk_vis_apply（Ctrl+V 且 Ctrl+0）。
   * 以前 Ctrl+0 关着时放的点根本没有球，之后再打开也变不出来，只能重进图。 */
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
P navfix_add_point_graph(void);   /* 纯面图：现场补一张 0 节点的 PointGraph */
int navfix_drop_navmesh(void);    /* 纯面图：grow 时把可走面摘掉，人机才走点图 */
void navfix_pg_reset(void);
P navfix_astar(void);
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
/* 4 / 5 原先是旧守卫点 / 旧守卫区（2026-11-26 删），编号留空不复用 */
#define K_SPAWN   6
#define K_JUMP    7
#define K_TAG     8

typedef struct { V3 p; int tag; int walk; unsigned int pen; } VN;
/* 反向连接查询：read_nav 扫边时要用（定义在导航段，先声明） */
static int nav_conn_has(P nd, P other);

/* dir: 0 = 双向；1 = a->b 单向；2 = b->a 单向（2026-11-20 方向可视化） */
typedef struct { int a, b; unsigned char dir; } VE;
/* yaw[] = 这个点「看哪儿」（度，0=北）：蹲守点 / 守卫点从 zoomPos 读出来，最多 3 个。
 * nyaw = 0 表示读不到（原生没写 / 还没轮到读）→ 画虚线 + 菜单写「未知」。 */
typedef struct { V3 p; int kind; int aux; char name[48]; float yaw[DIR_MAXN]; unsigned char nyaw; } VF;

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
static P g_edgeArrowGo;      /* 单向边箭头层：只在 F2 菜单打开时显示 */
static int g_edgeArrowOn = -1;

/* 2026-11-26 用户要求删除 Ctrl+E 导出与 Ctrl+Shift+X 只读采集：
 * export_* / collect_only / editor 三个开关连同全部代码一起清掉。
 * 留下的只有可视化、菜单和可走面落盘（控制台 3D 视图要用 navmesh_*.bin）。 */
static int g_visOn;
static int g_visDirty, g_visNoMesh;
static int g_nmVert, g_nmTri;     /* 最近一次落盘的 NavMeshGraph 顶点/三角形数 */
static int g_nmShow = 1;          /* cfg: navmesh_show —— 画不画 A* 可走面线框 */
/* cfg: vis_* —— 每一类一个开关，同时决定「读不读」和「画不画」。
 * 「名单」= 游戏加载场景时登记出来、一直挂在类上的静态 List，不是实时算出来的；
 * 换图瞬间它们还指着上一张图正在销毁的组件，读位置就是野指针（2026-11-17 沙漠要塞
 * 进图闪退就是这么死的）。哪一类出问题就单独关哪一类。 */
static int g_visNodes  = 1;       /* PointGraph 路点 / 连线（A* 图，不是名单） */
static int g_visNano   = 1;       /* SpareAreaList：守卫区 + 守卫点 */
static int g_visCrouch = 1;       /* SpareList_BL/GR：人类蹲守点（蓝/红） */
static int g_visBorn   = 1;       /* MapManager：幽灵出生 / 保卫者出生 */
static int g_visSupply = 1;       /* MapManager：中立点 / 补给箱 / 红箱 / 蓝箱 */
static int g_visJump   = 1;       /* Bot_JumpLink：跳点（FindObjectsOfType，不是名单） */
static int g_visTag    = 1;       /* PointNodeTagModifier：标签区（同上） */
static int g_visPm     = 1;       /* 玩家坐标记录：只画本次记下的位置（金色方块，不画折线） */
/* 玩家坐标记录：控制台点「记录当前位置」-> ucf_navcmd.txt 的 cmd=mark ->
 * 这里向下打射线取脚下地面点，追加进 <插件目录>\player_marks.txt。
 * 控制台负责删除（直接改文件），这里每 0.5 s 比一次修改时间重读。
 * 2026-11-21 用户要求：文件只是日志 —— 场景里只画「本次」记下的点（g_pmSesP），
 * 换图 / 重开游戏就不画了；历史记录不再进场景，也不再连折线。 */
#define PM_MAX 256
static V3   g_pmP[PM_MAX];        /* 文件里的全部记录：只当日志 / 给补蹲守点用，不画 */
static int  g_pmN;
static V3   g_pmSesP[PM_MAX];     /* 本次（当前场景）记下的点：唯一会画出来的东西 */
static int  g_pmSesN;
static unsigned g_pmMtime;
static int  g_pmLoaded;
static char g_pmPath[MAX_PATH];
static int g_visCompass = 1;      /* 方向罗盘：屏幕下方汉字东南西北（独立于可视化总开关） */
static int g_nmWireTri, g_nmWireVert;  /* 可走面当前三角形/顶点数（日志显示） */
static P   g_nmObj[16];           /* 可走面自己的网格对象（和可视化对象分开） */
static int g_nmObjN;
static int g_nmDirty = 1;         /* 换图/开关变化后要重建 */
static int g_sceneAge;            /* 进图后过了多少帧（VIS_SCENE_WAIT 之前不碰游戏组件表） */
static int g_sceneReadyOnce;      /* 本张图已经稳定过一次 */

static P   g_trKlass;             /* Transform 的 il2cpp 类：comp_pos 用它挡掉「不是 Transform」的指针 */
static P   g_trBaseKlass;         /* 普通 GameObject 的 Transform 类（g_trKlass 若是 RectTransform，父类就是它） */
static int g_badTr;               /* comp_pos 拦下的坏指针个数（日志可看） */
static unsigned long long nm_seenFp;  /* 已落盘的导航网格指纹 */
static int nm_seen;
static int g_cArea, g_cPos, g_cCrouch, g_cSpawn, g_cJump, g_cTag;
static void overlay_refresh(void);
static void overlay_reset(void);
static void menu_refresh(void);   /* 保存后立刻刷新「未保存 / 已保存」这一行 */
static void nm_tick(void);           /* A* 可走面：按需重建（定义在 nm_dump 之后） */
static void nm_toggle(void);
static void ghost_reset(void);       /* 预置预览：换图时清掉（定义在 wp_place 之前） */
static void nm_walk(int draw);       /* 只统计 = 0 / 画 = 1 */
static P comp_tr(P comp);
static void mk_vis_apply(void);       /* 标记球显隐 = Ctrl+V 开 且 Ctrl+0 开（定义在 add_mk 之前） */

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
/* 把当前批（g_bV / g_bI）做成一个 Mesh 对象；调用者自己挂到 MeshFilter 上。
 * 预置预览（ghost）和可视化层共用这一份，别写两套顶点/索引搬运。 */
static P build_mesh(void) {
  P mesh, av, ai;
  if (g_bNI == 0 || g_bNV == 0) return 0;
  if (!g_meshCls || !g_vec3Cls || !g_i32Cls || !x_array_new) return 0;
  mesh = x_object_new(g_meshCls);
  if (!mesh) return 0;
  ((mesh_ctor_t)RVA(R_MESH_CTOR))(mesh, 0);
  av = x_array_new(g_vec3Cls, (unsigned)g_bNV);
  ai = x_array_new(g_i32Cls, (unsigned)g_bNI);
  if (!av || !ai) return 0;
  {
    /* 长度必须和请求的完全一致：万一 il2cpp 给的数组比要的小（元素类型不对），
     * memcpy 就会越界写花隔壁的托管对象（12:39 那次 SpareAreaList 野值）。 */
    int vlen = *(int*)((char*)av + 0xC);
    int ilen = *(int*)((char*)ai + 0xC);
    if (vlen != g_bNV || ilen != g_bNI) {
      elog("!!! mesh: ARRAY LEN MISMATCH vec3 %d/%d i32 %d/%d - skip (would overflow)",
           vlen, g_bNV, ilen, g_bNI);
      return 0;
    }
  }
  memcpy((char*)av + 0x10, g_bV, (size_t)g_bNV * 12);
  memcpy((char*)ai + 0x10, g_bI, (size_t)g_bNI * 4);
  ((mesh_arr_t)RVA(R_MESH_VERTS))(mesh, av, 0);
  ((mesh_arr_t)RVA(R_MESH_TRIS))(mesh, ai, 0);
  ((mesh_1_t)RVA(R_MESH_BOUNDS))(mesh, 0);
  return mesh;
}
static int flush_mesh_to(const char* name, int slot, int items, P* list, int* count, int cap) {
  P go, mf, mr, mesh, mat;
  if (g_bNI == 0) return 1;
  /* 材质必须先活着：以前是先把 GO/网格建好、最后才拿材质，材质死了就直接
   * 挂空材质 —— Unity 渲染成洋红 #FF00FF，看起来像"这条线自己变了颜色"。 */
  mat = mat_for(slot);
  if (!mat_alive(mat)) {
    if (!g_matDeadLog) {
      elog("vis: material slot=%d dead (shader unloaded) - rebuild", slot);
      g_matDeadLog = 1;
    }
    mat_drop(slot);
    g_matReady = 0;   /* 连原型都可能死了：让 mat_setup 重来（它自己有 5 秒冷却） */
    mat = mat_for(slot);
    if (!mat_alive(mat)) {
      elog("vis: slot=%d has no usable material - skip mesh '%s' (no magenta)", slot, name);
      return 0;
    }
  }
  if (!g_meshCls || !g_mfType || !g_mrType || !g_vec3Cls || !g_i32Cls || !x_array_new) {
    if (!g_visNoMesh) {
      elog("vis: mesh classes missing (mesh=%p mf=%p mr=%p vec3=%p i32=%p arr=%p)",
           g_meshCls, g_mfType, g_mrType, g_vec3Cls, g_i32Cls, (void*)x_array_new);
      g_visNoMesh = 1;
    }
    return 0;
  }
  mesh = build_mesh();
  if (!mesh) return 0;
  go = new_go(name);
  if (!go) return 0;
  ((set_layer_t)RVA(R_SETLAYER))(go, 0, 0);
  mf = ((addcomp_t)RVA(R_ADDCOMP))(go, g_mfType, 0);
  mr = ((addcomp_t)RVA(R_ADDCOMP))(go, g_mrType, 0);
  if (!mf || !mr) { elog("vis: MeshFilter/MeshRenderer add failed"); return 0; }
  ((mf_setmesh_t)RVA(R_MF_SETMESH))(mf, mesh, 0);
  ((set_shmat_t)RVA(R_REND_SETSM))(mr, mat, 0);
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
 * 守卫区 x 各自 posList，一秒 4 遍就是几十万次 VirtualQuery。同一个列表里的槽位几乎
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
  /* 每个守卫区自己的 posList（List<Bot_NanoGuardPos>）也一起体检：
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
  if (g_trKlass && *(P*)tr != g_trKlass && *(P*)tr != g_trBaseKlass) { g_badTr++; return 0; }
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
  f->nyaw = 0;                       /* 默认未知：读得到 zoomPos 的再填 */
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
  if (!g_visNodes) return;
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
      int back;
      if (oi < 0 || oi == i) continue;
      /* 每条无向边只记一次（索引小的当 a），方向在这里就判掉：
       *   back = 对方也连回来 → 双向；否则只有 i->oi 一条。
       * 旧代码只记 oi > i，单向边 b->a（大索引指向小索引）会被整条漏掉，
       * 画面上看就是"这条路不存在"。 */
      back = nav_conn_has(other, nd);
      if (oi > i) {
        g_ve[g_veN].a = i;
        g_ve[g_veN].b = oi;
        g_ve[g_veN].dir = back ? 0 : 1;
        g_veN++;
      } else if (!back) {
        g_ve[g_veN].a = oi;
        g_ve[g_veN].b = i;
        g_ve[g_veN].dir = 2;      /* 真正方向是 b->a */
        g_veN++;
      }
    }
  }
}

/* read_nano 这一轮真正从 SpareAreaList 里读到的守卫区组件。
 * pend_area_tick 用它判重：已经在列表里的区，可视化层会画绿框，我们不必再补一份
 * （否则两个网格重叠、闪 z-fighting）；没读到的才由我们顶上。 */
#define NANO_SEEN_MAX 128
static P g_nanoSeen[NANO_SEEN_MAX];
static int g_nanoSeenN;

static void read_nano(void) {
  P l, items, aptr[VIS_MAXF];
  V3 apos[VIS_MAXF];
  int n, an = 0, i;
  g_nanoSeenN = 0;                 /* 每次读都重算：读不到 = 这一轮没有可信列表 */
  if (!g_visNano || !g_areaCls) return;
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
    if (an < NANO_SEEN_MAX) g_nanoSeen[g_nanoSeenN++] = a;
    an++;
  }
  for (i = 0; i < an; i++) {
    P a = aptr[i];
    V3 p = apos[i];
    int j;
    vf_add(p, K_NAREA, i, "守卫区");
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
        {
          /* 守卫点的「看哪儿」= zoomPos（Init 已把守卫区 entrancePos 并进来） */
          int vi = vf_add(q, K_NPOS, *(int*)((char*)gp + 0x1C), "守卫点");
          if (vi >= 0) g_vf[vi].nyaw = (unsigned char)read_zoom(gp, &q, g_vf[vi].yaw, DIR_MAXN);
        }
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
  if (!g_visCrouch || !g_crouchCls) return;
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
      {
        /* 蹲守点：zoomPos 继承自 Bot_GuardPos，同一个字段 0x10（原生点实测都有 1 个） */
        int vi = vf_add(p, K_CROUCH, k, nm[k]);
        if (vi >= 0) g_vf[vi].nyaw = (unsigned char)read_zoom(c, &p, g_vf[vi].yaw, DIR_MAXN);
      }
      g_cCrouch++;
    }
  }
}

static void read_spawns(void) {
  static const char* nm[6] = { "幽灵出生", "保卫者出生", "中立点", "补给箱", "红箱", "蓝箱" };
  static const int off[6] = { 0x10, 0x14, 0x18, 0x1C, 0x20, 0x24 };
  P mm = 0;
  int k;
  if (!g_visBorn && !g_visSupply) return;
  if (g_mmInstField) x_field_static_get_value(g_mmInstField, &mm);
  if (!uobj_live(mm)) { miss("MapManager"); return; }
  for (k = 0; k < 6; k++) {
    P arr;
    int n, i;
    /* cfg: vis_born —— k 0..2 幽灵出生 / 保卫者出生 / 中立点；
     * cfg: vis_supply —— k 3..5 补给箱 / 红箱 / 蓝箱。两类各自管理：
     * 关掉哪一类，对应的数组都不读（连同 mem_ok 校验一起跳过）。
     * 这些开关只管「读不读 + 画不画」（导出功能已删）。 */
    if (k <= 2 ? !g_visBorn : !g_visSupply) continue;
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

static int g_nativeJumpLogged;   /* 原生跳链参数只打前 2 条 */

static void read_jump(void) {
  P arr;
  int n, i;
  if (!g_visJump || !g_jumpType) return;
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
    /* 2026-11-25：把原生跳链的参数打出来当基准（用户要求"参考其他跳链"）。
     * 每张图只打前 2 条，字段就是 Link 结构：endNode +0x14 / needSpeed +0x18 /
     * accuracy +0x1C / direction +0x20..+0x28。 */
    if (ln > 0 && g_nativeJumpLogged < 2 && links) {
      P en = *(P*)((char*)links + 0x14);
      float ns = *(float*)((char*)links + 0x18);
      float ac = *(float*)((char*)links + 0x1C);
      float dx = *(float*)((char*)links + 0x20);
      float dy = *(float*)((char*)links + 0x24);
      float dz = *(float*)((char*)links + 0x28);
      elog("jumpbase: native link at (%.2f %.2f %.2f) endNode=%p needSpeed=%.2f accuracy=%.2f dir=(%.2f %.2f %.2f)",
           p.x, p.y, p.z, (void*)en, ns, ac, dx, dy, dz);
      g_nativeJumpLogged++;
    }
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
  if (!g_visTag || !g_tagType) return;
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

/* ---- 玩家坐标记录：读文件 / 记一条 -------------------------------------- */
/* 文件格式（控制台负责删除，这里只追加）：
 *   # ucf player marks
 *   1 -55.919 -16.590 1.235  2026-11-20 21:30:11
 * 返回 1 = 内容变了（要重画），0 = 没变。 */
static int pm_load(int force) {
  WIN32_FILE_ATTRIBUTE_DATA fa;
  unsigned mtime = 0;
  FILE* f;
  char line[256];
  int n = 0;
  if (!g_pmPath[0]) return 0;
  if (GetFileAttributesExA(g_pmPath, GetFileExInfoStandard, &fa))
    mtime = fa.ftLastWriteTime.dwLowDateTime ^ (unsigned)fa.ftLastWriteTime.dwHighDateTime;
  if (!force && g_pmLoaded && mtime == g_pmMtime) return 0;
  g_pmMtime = mtime;
  g_pmLoaded = 1;
  f = fopen(g_pmPath, "r");
  if (!f) { g_pmN = 0; return 1; }
  while (fgets(line, sizeof line, f) && n < PM_MAX) {
    int idx;
    float x, y, z;
    if (line[0] == '#') continue;
    if (sscanf(line, "%d %f %f %f", &idx, &x, &y, &z) == 4) {
      g_pmP[n].x = x; g_pmP[n].y = y; g_pmP[n].z = z;
      n++;
    }
  }
  fclose(f);
  g_pmN = n;
  return 1;
}

/* 控制台「记录当前位置」：相机向下打射线取脚下地面点（和路点同一套口径），
 * 追加一行到文件，不覆盖；序号取现有最大值 +1，删中间也不会重号。 */
static int pm_mark(void) {
  P cam, go, tr;
  V3 pos, dir;
  char hitbuf[128];
  FILE* f;
  int idx = 0;
  char line[256];
  SYSTEMTIME st;
  if (!g_pmPath[0]) { elog("pmark: no path (g_dir not ready)"); return 0; }
  cam = ((cam_main_t)RVA(R_CAM_MAIN))(0);
  if (!cam) { elog("pmark: no main camera"); return 0; }
  go = ((get_go_t)RVA(R_GETGO))(cam, 0);
  tr = get_tr(go);
  if (!tr) { elog("pmark: no camera transform"); return 0; }
  ((get_pos_t)RVA(R_GET_POS_INJ))(tr, &pos, 0);
  dir.x = 0.0f; dir.y = -1.0f; dir.z = 0.0f;
  if (!((raycast_t)RVA(R_RAYCAST))(pos, dir, hitbuf, 120.0f, 1, 0)) {
    elog("pmark: no ground below camera (%.2f %.2f %.2f)", pos.x, pos.y, pos.z);
    return 0;
  }
  f = fopen(g_pmPath, "r");
  if (f) {
    while (fgets(line, sizeof line, f)) {
      int k;
      if (line[0] == '#') continue;
      if (sscanf(line, "%d", &k) == 1 && k > idx) idx = k;
    }
    fclose(f);
  }
  f = fopen(g_pmPath, "a");
  if (!f) { elog("pmark: append open failed: %s", g_pmPath); return 0; }
  GetLocalTime(&st);
  fprintf(f, "%d %.3f %.3f %.3f %04d-%02d-%02d %02d:%02d:%02d\n",
          idx + 1, ((V3*)hitbuf)->x, ((V3*)hitbuf)->y, ((V3*)hitbuf)->z,
          st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond);
  fclose(f);
  elog("pmark: #%d (%.3f %.3f %.3f) -> %s",
       idx + 1, ((V3*)hitbuf)->x, ((V3*)hitbuf)->y, ((V3*)hitbuf)->z, g_pmPath);
  pm_load(1);
  /* 只在本次画：新点进会话表，换图即清；文件照旧留一份日志（控制台读写它） */
  if (g_pmSesN < PM_MAX) g_pmSesP[g_pmSesN++] = *(V3*)hitbuf;
  elog("pmark: session #%d, drawn in this scene only (file keeps the log)", g_pmSesN);
  g_visDirty = 1;          /* 下一帧重画，新点立刻出现在游戏里 */
  return 1;
}

/* 方向箭头：在 a->b 这条线的 62% 处画一个「>」形（两条短线），
 * 世界坐标直接算，不用旋转 —— 网格只在可视化重建时做一次。 */
static void edge_arrow(V3 a, V3 b) {
  V3 d, tip, b1, b2, perp;
  float len, pl;
  d.x = b.x - a.x; d.y = b.y - a.y; d.z = b.z - a.z;
  len = sqrtf(d.x * d.x + d.y * d.y + d.z * d.z);
  if (len < 0.8f) return;                     /* 太短的边塞不下箭头 */
  d.x /= len; d.y /= len; d.z /= len;
  tip.x = a.x + d.x * len * 0.62f;
  tip.y = a.y + d.y * len * 0.62f;
  tip.z = a.z + d.z * len * 0.62f;
  /* 侧向 = d × up；边接近竖直时退化，随便给个 X 轴 */
  perp.x = d.z; perp.y = 0.0f; perp.z = -d.x;
  pl = sqrtf(perp.x * perp.x + perp.z * perp.z);
  if (pl < 0.2f) { perp.x = 1.0f; perp.y = 0.0f; perp.z = 0.0f; pl = 1.0f; }
  perp.x /= pl; perp.z /= pl;
  b1.x = tip.x - d.x * 0.30f + perp.x * 0.17f;
  b1.y = tip.y - d.y * 0.30f;
  b1.z = tip.z - d.z * 0.30f + perp.z * 0.17f;
  b2.x = tip.x - d.x * 0.30f - perp.x * 0.17f;
  b2.y = tip.y - d.y * 0.30f;
  b2.z = tip.z - d.z * 0.30f - perp.z * 0.17f;
  bs_line(tip, b1, 0.07f);
  bs_line(tip, b2, 0.07f);
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
    /* 单向边箭头（橙，slot 7）：双向边不画，所以一千多条边的图也不会糊。
     * 这一层默认关着，只在 F2 菜单打开时由 edge_dir_sync() 打开。 */
    g_edgeArrowGo = 0;
    {
      int c = 0;
      bs_reset();
      for (i = 0; i < g_veN; i++) {
        V3 a, b;
        if (!g_ve[i].dir) continue;
        a = g_vn[g_ve[i].a].p;
        b = g_vn[g_ve[i].b].p;
        if (g_ve[i].dir == 2) { V3 t = a; a = b; b = t; }   /* dir=2：真正方向是 b->a */
        edge_arrow(a, b);
        c++;
      }
      if (c) {
        int before = g_visObjN;
        if (vis_flush_mesh("vis_edge_dir", 7, c) && g_visObjN > before)
          g_edgeArrowGo = g_visObj[g_visObjN - 1];
      }
    }
    g_edgeArrowOn = -1;
  }
  if (g_visJump && g_jN) {
    bs_reset();
    for (i = 0; i < g_jN; i++) bs_line(g_jA[i], g_jB[i], 0.10f);
    vis_flush_mesh("vis_jump", 4, g_jN);
    /* 端点也画成小方块：跳链是「起点路点 + 落点路点」一对，只画线容易被当成普通连线 */
    bs_reset();
    for (i = 0; i < g_jN; i++) {
      V3 h;
      h.x = 0.20f; h.y = 0.20f; h.z = 0.20f;
      bs_solid(g_jA[i], h);
      bs_solid(g_jB[i], h);
    }
    vis_flush_mesh("vis_jump_pt", 4, g_jN * 2);
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
  if (g_visNano) {
    /* 绿框只画 SpareAreaList 里的区（read_nano）。新建但还没挂守卫点的区不在这里，
     * 由 pend_area_tick() 单独用金色线框画 —— 它不受 VIS_SCENE_WAIT 的推迟影响。 */
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
  /* 玩家坐标记录：只画本次记下的金色方块。
   * 2026-11-21 用户要求：历史记录只留在 player_marks.txt 当日志，不进场景；
   * 也不再连折线（那条金线会被当成跳点）。 */
  if (g_visPm && g_pmSesN) {
    bs_reset();
    for (i = 0; i < g_pmSesN; i++) {
      V3 h;
      h.x = 0.22f; h.y = 0.22f; h.z = 0.22f;
      bs_solid(g_pmSesP[i], h);
    }
    vis_flush_mesh("vis_pmarks", 14, g_pmSesN);
  }
}

/* ---- 守卫区自己的线框：待激活=金色，已挂点但可视化层还没重建=绿色 ----------
 * 为什么不放进 vis_rebuild：进图后前 VIS_SCENE_WAIT 个心跳（心跳 4 Hz，≈22 s）整层
 * 可视化是推迟的 —— 那段时间读游戏组件表（SpareAreaList / SpareList_BL/GR …）会撞上
 * 上一张图正在销毁的对象，2026-11-17 沙漠要塞的闪退就是这么来的。可用户偏偏最爱刚进图
 * 就改图，于是「新建守卫区」只有一颗标记球，看上去像没建出来。
 * 这段只用**我们自己的标记表**（g_mk）+ 网格构建，不读任何游戏组件表，所以可以每 tick
 * 维护，两套框各一个网格：
 *   金框 = 还没挂守卫点（未激活，人机不认）；
 *   绿框 = 已经挂上第一个守卫点，但这一轮 read_nano 还没把它读出来（重建被推迟 / 刚好
 *          没轮到）—— 先由我们顶上，否则「一点下去框就没了」，等 22 秒才冒出来更慌。
 * read_nano 一旦把这个区读进 SpareAreaList（g_nanoSeen），我们就让位给可视化层。 */
#define PEND_MAXA 8
static P g_pendMesh[2], g_pendGo[2], g_pendMf[2], g_pendMr[2];
static unsigned g_pendSig[2];              /* 各自集合的指纹（变了才重建网格） */
static unsigned char g_pendShownA[2];

static void pend_draw_set(int k, const V3* pos, int n, int slot, unsigned sig) {
  V3 hh;
  int i;
  if (g_pendGo[k] && !uobj_live(g_pendGo[k])) { g_pendGo[k] = 0; g_pendMf[k] = g_pendMr[k] = 0; }
  if (g_pendMesh[k] && !uobj_live(g_pendMesh[k])) g_pendMesh[k] = 0;
  if (n <= 0) {
    if (g_pendShownA[k] && g_pendGo[k] && uobj_live(g_pendGo[k]))
      ((set_active_t)RVA(R_SETACTIVE))(g_pendGo[k], 0, 0);
    g_pendShownA[k] = 0;
    return;
  }
  if (!g_pendMesh[k] || sig != g_pendSig[k]) {
    if (!g_meshCls || !g_vec3Cls || !g_i32Cls || !x_array_new) return;
    if (g_pendMesh[k] && uobj_live(g_pendMesh[k])) { ((destroy_t)RVA(R_DESTROY))(g_pendMesh[k], 0); }
    g_pendMesh[k] = 0;
    hh.x = 2.4f; hh.y = 1.7f; hh.z = 2.4f;      /* 和 K_NAREA 绿框同尺寸（半尺寸） */
    bs_reset();
    for (i = 0; i < n; i++) bs_wbox(pos[i], hh, 0.05f);
    g_pendMesh[k] = build_mesh();
    g_pendSig[k] = sig;
    if (g_pendMesh[k]) root_put(g_pendMesh[k]);
    elog("area: 守卫区线框 %d 个（%s）", n, k ? "已挂点、可视化还没重建：先画绿框"
                                              : "待激活：金色线框");
  }
  if (!g_pendMesh[k]) return;
  if (!g_pendGo[k]) {
    P mat = mat_for(slot);                     /* 0=金(14) 1=绿(2) */
    if (!mat_alive(mat)) return;
    g_pendGo[k] = new_go(k ? "UCF_AreaLive" : "UCF_AreaPending");
    if (!g_pendGo[k]) return;
    ((set_layer_t)RVA(R_SETLAYER))(g_pendGo[k], 0, 0);
    g_pendMf[k] = ((addcomp_t)RVA(R_ADDCOMP))(g_pendGo[k], g_mfType, 0);
    g_pendMr[k] = ((addcomp_t)RVA(R_ADDCOMP))(g_pendGo[k], g_mrType, 0);
    if (!g_pendMf[k] || !g_pendMr[k]) {
      ((destroy_t)RVA(R_DESTROY))(g_pendGo[k], 0);
      g_pendGo[k] = g_pendMf[k] = g_pendMr[k] = 0;
      return;
    }
    ((set_shmat_t)RVA(R_REND_SETSM))(g_pendMr[k], mat, 0);
    ((set_int1_t)RVA(R_REND_SHADOW))(g_pendMr[k], 0, 0);
    root_put(g_pendGo[k]);
  }
  if (g_pendMf[k]) ((mf_setmesh_t)RVA(R_MF_SETMESH))(g_pendMf[k], g_pendMesh[k], 0);
  ((set_active_t)RVA(R_SETACTIVE))(g_pendGo[k], 1, 0);
  g_pendShownA[k] = 1;
}

static void pend_area_tick(void) {
  V3 posP[PEND_MAXA], posL[PEND_MAXA];
  int i, j, np = 0, nl = 0, seen, live;
  unsigned hp = 2166136261u, hl = 2166136261u;
  if (!g_visOn || !g_visNano) {
    pend_draw_set(0, 0, 0, 14, 0);
    pend_draw_set(1, 0, 0, 2, 0);
    return;
  }
  for (i = 0; i < g_n; i++) {
    V3 q = g_mk[i].p;
    int aid = g_mk[i].aid;
    if (g_mk[i].type != MT_AREA) continue;
    seen = 0;
    for (j = 0; j < g_nanoSeenN; j++) if (g_nanoSeen[j] == g_mk[i].comp) { seen = 1; break; }
    if (seen) continue;                        /* 可视化层已经在画这个区的绿框 */
    live = (aid >= 0 && aid < MAX_AID && g_areaLive[aid]) ? 1 : 0;
    if (live) {
      if (nl < PEND_MAXA) posL[nl++] = q;
      hl = (hl ^ (unsigned)(int)(q.x * 10.0f)) * 16777619u;
      hl = (hl ^ (unsigned)(int)(q.y * 10.0f)) * 16777619u;
      hl = (hl ^ (unsigned)(int)(q.z * 10.0f)) * 16777619u;
    } else {
      if (np < PEND_MAXA) posP[np++] = q;
      hp = (hp ^ (unsigned)(int)(q.x * 10.0f)) * 16777619u;
      hp = (hp ^ (unsigned)(int)(q.y * 10.0f)) * 16777619u;
      hp = (hp ^ (unsigned)(int)(q.z * 10.0f)) * 16777619u;
    }
  }
  pend_draw_set(0, posP, np, 14, hp);
  pend_draw_set(1, posL, nl, 2, hl);
}

/* ================= 方向层：蹲守点 / 守卫点「朝哪看」 =========================
 * 2026-11-27（用户：「蹲守点、守卫点有方向，可是光显示一个球，看不出来」）
 * 只做这两类（用户指定范围），罗盘不算在内。
 *
 * 数据：MK.yaw（我们自己建的）/ VF.yaw[]（从游戏 zoomPos 读的，见 read_zoom）。
 * 显示（方案 C = 射线 + 近点度数文本，用户 2026-11-27 选定）：
 *   默认只画**准星正对着的那一个点**（仅瞄准点），避免几百个点的箭头糊成一片；
 *   射线 = 1.4 m 粗线 + 箭头尖；多方向时主方向粗、次方向细（最多 DIR_MAXN 条）；
 *   读不到方向 = 半径 0.35 m 的虚线小圈，菜单/浮字写「未知」，绝不默认成 0°。
 *   准星下方一行字：「蹲守点 · 朝向 东北 42°」/「守卫点 · 3 个方向」。
 * 变换：整个方向层是**世界坐标网格**，内容变了才重建（不每帧建）。
 * 关闭：朝向工具页「显示样式」选「关」，或 Ctrl+V 关掉可视化。
 * ------------------------------------------------------------------------- */
static void dir_label_build(P canvasTr);   /* 定义在 toast_build 后面（要用 mk_text_ui） */

#define DIR_RAY_LEN  1.4f
#define DIR_RAY_W    0.06f
#define DIR_RAY_W2   0.035f
#define DIR_FAN_R    1.8f
#define DIR_FAN_HALF 30.0f

static int  g_dirStyle = 1;        /* 0=关 1=射线 2=扇形 */
static P    g_dirMesh, g_dirGo, g_dirMf, g_dirMr;
static unsigned g_dirSig;
static int  g_dirShown;
static P    g_dirLabel, g_dirLabelGo;
static char g_dirText[128];
static int  g_dirSrc;              /* 0=没有 1=自己的标记(g_mk) 2=游戏里的点(g_vf) */
static int  g_dirIdx = -1;         /* 对应来源的下标（菜单里操作同一个点） */
static V3   g_dirP;                /* 当前方向的点位 */
static float g_dirYawArr[DIR_MAXN];
static int  g_dirYawN;
static int  g_dirUnknown;

static void dir_hide(void) {
  if (g_dirShown && g_dirGo && uobj_live(g_dirGo)) ((set_active_t)RVA(R_SETACTIVE))(g_dirGo, 0, 0);
  if (g_dirLabelGo && uobj_live(g_dirLabelGo)) ((set_active_t)RVA(R_SETACTIVE))(g_dirLabelGo, 0, 0);
  g_dirShown = 0;
  g_dirSrc = 0; g_dirIdx = -1;
}

/* 准星正对着的有方向点位：先看我们自己建的（刚放下的点还没进游戏列表），
 * 再看游戏里的（原生点 / 已经读到的点）。判定和 delete_nearest_of 同一套：
 * 射线垂直距离 ≤ 0.9 m 且在前方 60 m 内，取最近的那个。 */
static int dir_pick(int* src, int* idx, V3* p, float* yaw, int* nyaw, int* unknown) {
  V3 cp, fw;
  float best = 1e9f;
  int i, besti = -1;
  if (src) *src = 0;
  if (idx) *idx = -1;
  if (nyaw) *nyaw = 0;
  if (unknown) *unknown = 0;
  if (!cam_ray(&cp, &fw)) return 0;
  for (i = 0; i < g_n; i++) {
    float vx, vy, vz, t, px, py, pz, perp;
    if (g_mk[i].type != MT_CROUCH && g_mk[i].type != MT_NANOPOS) continue;
    vx = g_mk[i].p.x - cp.x; vy = g_mk[i].p.y - cp.y; vz = g_mk[i].p.z - cp.z;
    t = vx * fw.x + vy * fw.y + vz * fw.z;
    if (t <= 0.2f || t > 60.0f) continue;
    px = vx - fw.x * t; py = vy - fw.y * t; pz = vz - fw.z * t;
    perp = sqrtf(px * px + py * py + pz * pz);
    if (perp <= 0.9f && perp < best) { best = perp; besti = i; }
  }
  if (besti >= 0) {
    if (src) *src = 1;
    if (idx) *idx = besti;
    *p = g_mk[besti].p;
    if (nyaw) *nyaw = 1;
    yaw[0] = g_mk[besti].yaw;
    if (unknown) *unknown = (yaw[0] <= YAW_NONE + 1.0f);
    return 1;
  }
  best = 1e9f; besti = -1;
  for (i = 0; i < g_vfN; i++) {
    float vx, vy, vz, t, px, py, pz, perp;
    if (g_vf[i].kind != K_CROUCH && g_vf[i].kind != K_NPOS) continue;
    vx = g_vf[i].p.x - cp.x; vy = g_vf[i].p.y - cp.y; vz = g_vf[i].p.z - cp.z;
    t = vx * fw.x + vy * fw.y + vz * fw.z;
    if (t <= 0.2f || t > 60.0f) continue;
    px = vx - fw.x * t; py = vy - fw.y * t; pz = vz - fw.z * t;
    perp = sqrtf(px * px + py * py + pz * pz);
    if (perp <= 0.9f && perp < best) { best = perp; besti = i; }
  }
  if (besti >= 0) {
    int k, nn = g_vf[besti].nyaw;
    if (nn > DIR_MAXN) nn = DIR_MAXN;
    if (src) *src = 2;
    if (idx) *idx = besti;
    *p = g_vf[besti].p;
    for (k = 0; k < nn; k++) yaw[k] = g_vf[besti].yaw[k];
    if (nyaw) *nyaw = nn;
    if (unknown) *unknown = (nn == 0);
    return 1;
  }
  return 0;
}

/* 方向层网格：世界坐标，内容变了才重建 */
static void dir_build_mesh(void) {
  int i, k;
  V3 base = g_dirP;
  base.y += 0.06f;
  bs_reset();
  if (g_dirUnknown) {
    /* 未知：半径 0.35 m 的虚线小圈（8 段），告诉用户「这里读不到朝向」 */
    for (k = 0; k < 8; k++) {
      float a0 = (float)k * 45.0f, a1 = a0 + 20.0f;
      V3 s, e;
      dir_of_yaw(a0, &s); dir_of_yaw(a1, &e);
      s.x = base.x + s.x * 0.35f; s.y = base.y; s.z = base.z + s.z * 0.35f;
      e.x = base.x + e.x * 0.35f; e.y = base.y; e.z = base.z + e.z * 0.35f;
      bs_line(s, e, 0.045f);
    }
  } else if (g_dirStyle == 2) {
    /* 扇形：半角 30°、半径 1.8 m 的弧 + 两条边 + 中心射线（线框，不做半透明：
     * 游戏材质是 Opaque，alpha 不生效，画填充反而会变成一块实心色板）。 */
    float y0 = g_dirYawArr[0];
    int seg = 6;
    V3 prev;
    dir_of_yaw(y0 - DIR_FAN_HALF, &prev);
    prev.x = base.x + prev.x * DIR_FAN_R; prev.y = base.y; prev.z = base.z + prev.z * DIR_FAN_R;
    for (k = 1; k <= seg; k++) {
      V3 cur, edge;
      float a = y0 - DIR_FAN_HALF + (2.0f * DIR_FAN_HALF) * (float)k / (float)seg;
      dir_of_yaw(a, &cur);
      cur.x = base.x + cur.x * DIR_FAN_R; cur.y = base.y; cur.z = base.z + cur.z * DIR_FAN_R;
      bs_line(prev, cur, 0.05f);
      if (k == 1) bs_line(base, prev, 0.05f);
      edge = cur;
      if (k == seg) bs_line(base, edge, 0.05f);
      prev = cur;
    }
    {
      V3 d, tip, bl, br, perp;
      dir_of_yaw(y0, &d);
      tip.x = base.x + d.x * DIR_FAN_R; tip.y = base.y; tip.z = base.z + d.z * DIR_FAN_R;
      bs_line(base, tip, 0.06f);
      perp.x = d.z; perp.y = 0.0f; perp.z = -d.x;
      bl.x = tip.x - d.x * 0.30f + perp.x * 0.17f; bl.y = tip.y; bl.z = tip.z - d.z * 0.30f + perp.z * 0.17f;
      br.x = tip.x - d.x * 0.30f - perp.x * 0.17f; br.y = tip.y; br.z = tip.z - d.z * 0.30f - perp.z * 0.17f;
      bs_line(tip, bl, 0.06f);
      bs_line(tip, br, 0.06f);
    }
  } else {
    /* 射线：主方向粗 + 箭头尖；次方向细 + 末端小方块 */
    for (i = 0; i < g_dirYawN; i++) {
      V3 d, tip, bl, br, perp;
      float len = (i == 0) ? DIR_RAY_LEN : 0.9f;
      float w = (i == 0) ? DIR_RAY_W : DIR_RAY_W2;
      dir_of_yaw(g_dirYawArr[i], &d);
      tip.x = base.x + d.x * len; tip.y = base.y; tip.z = base.z + d.z * len;
      bs_line(base, tip, w);
      perp.x = d.z; perp.y = 0.0f; perp.z = -d.x;
      if (i == 0) {
        bl.x = tip.x - d.x * 0.32f + perp.x * 0.18f; bl.y = tip.y; bl.z = tip.z - d.z * 0.32f + perp.z * 0.18f;
        br.x = tip.x - d.x * 0.32f - perp.x * 0.18f; br.y = tip.y; br.z = tip.z - d.z * 0.32f - perp.z * 0.18f;
        bs_line(tip, bl, w);
        bs_line(tip, br, w);
      } else {
        V3 hh;
        hh.x = 0.06f; hh.y = 0.06f; hh.z = 0.06f;
        bs_solid(tip, hh);
      }
    }
  }
  g_dirMesh = build_mesh();
  if (g_dirMesh) root_put(g_dirMesh);
}

static unsigned dir_sig(void) {
  unsigned h = 2166136261u;
  int i;
  h = (h ^ (unsigned)g_dirStyle) * 16777619u;
  h = (h ^ (unsigned)g_dirUnknown) * 16777619u;
  h = (h ^ (unsigned)g_dirYawN) * 16777619u;
  h = (h ^ (unsigned)(int)(g_dirP.x * 10.0f)) * 16777619u;
  h = (h ^ (unsigned)(int)(g_dirP.y * 10.0f)) * 16777619u;
  h = (h ^ (unsigned)(int)(g_dirP.z * 10.0f)) * 16777619u;
  for (i = 0; i < g_dirYawN; i++) h = (h ^ (unsigned)(int)(g_dirYawArr[i] * 2.0f)) * 16777619u;
  return h;
}

/* 建立/刷新方向层的渲染对象（每个点只有一个，不存在批量上限问题） */
static void dir_draw(void) {
  P mat;
  int slot = 2;                    /* 2 = 绿（守卫点），1 = 红（蹲守点） */
  if (g_dirSrc == 1 && g_dirIdx >= 0) slot = (g_mk[g_dirIdx].type == MT_CROUCH) ? 1 : 2;
  else if (g_dirSrc == 2 && g_dirIdx >= 0) slot = (g_vf[g_dirIdx].kind == K_CROUCH) ? 1 : 2;
  if (g_dirGo && !uobj_live(g_dirGo)) { g_dirGo = 0; g_dirMf = g_dirMr = 0; }
  if (g_dirMesh && !uobj_live(g_dirMesh)) g_dirMesh = 0;
  {
    unsigned sig = dir_sig();
    if (!g_dirMesh || sig != g_dirSig) {
      if (g_dirMesh && uobj_live(g_dirMesh)) {
        root_drop(g_dirMesh);                       /* 句柄表只有 512 格，还回去 */
        ((destroy_t)RVA(R_DESTROY))(g_dirMesh, 0);
      }
      g_dirMesh = 0;
      dir_build_mesh();
      g_dirSig = sig;
      if (!g_dirMesh) return;
    }
  }
  if (!g_dirGo) {
    mat = mat_for(slot);
    if (!mat_alive(mat)) return;
    g_dirGo = new_go("UCF_DirMark");
    if (!g_dirGo) return;
    ((set_layer_t)RVA(R_SETLAYER))(g_dirGo, 0, 0);
    g_dirMf = ((addcomp_t)RVA(R_ADDCOMP))(g_dirGo, g_mfType, 0);
    g_dirMr = ((addcomp_t)RVA(R_ADDCOMP))(g_dirGo, g_mrType, 0);
    if (!g_dirMf || !g_dirMr) {
      ((destroy_t)RVA(R_DESTROY))(g_dirGo, 0);
      g_dirGo = g_dirMf = g_dirMr = 0;
      return;
    }
    ((set_shmat_t)RVA(R_REND_SETSM))(g_dirMr, mat, 0);
    ((set_int1_t)RVA(R_REND_SHADOW))(g_dirMr, 0, 0);
    root_put(g_dirGo);
  }
  if (g_dirMf) ((mf_setmesh_t)RVA(R_MF_SETMESH))(g_dirMf, g_dirMesh, 0);
  /* 颜色跟着类型走：同一个对象会从蹲守点（红）切到守卫点（绿），
   * 只建的时候设一次材质会让后一个点用前一个的颜色。 */
  mat = mat_for(slot);
  if (mat_alive(mat)) ((set_shmat_t)RVA(R_REND_SETSM))(g_dirMr, mat, 0);
  ((set_active_t)RVA(R_SETACTIVE))(g_dirGo, 1, 0);
  g_dirShown = 1;
}

/* 准星下方那行字：只在内容变了才 SetText（每帧建字符串会喂 GC） */
static void dir_label_set(const char* s, const COL* col) {
  if (!g_dirLabel || !uobj_live(g_dirLabel)) {
    g_dirLabel = 0; g_dirLabelGo = 0;
    return;
  }
  if (strcmp(g_dirText, s) != 0) {
    strncpy(g_dirText, s, sizeof(g_dirText) - 1);
    g_dirText[sizeof(g_dirText) - 1] = 0;
    ((set_txt_t)RVA(R_TEXT_SETTEXT))(g_dirLabel, x_string_new(g_dirText), 0);
    elog("dir: %s", g_dirText);
  }
  ((set_col_t)RVA(R_GRAPHIC_COL))(g_dirLabel, *col, 0);
  if (g_dirLabelGo) ((set_active_t)RVA(R_SETACTIVE))(g_dirLabelGo, 1, 0);
}

static void dir_tick(void) {
  V3 p;
  float yaw[DIR_MAXN];
  int src = 0, idx = -1, n = 0, unknown = 0;
  int ok;
  /* 只在 F2 菜单开着时显示：和单向边箭头同一个口径（关菜单 = 正常游玩画面干净）。
   * 编辑 / 放置 / 改朝向本来就都在菜单里做，菜单关掉时不需要这层。 */
  if (!g_visOn || g_dirStyle == 0 || !g_inited || !g_wpMenuOpen) { dir_hide(); return; }
  ok = dir_pick(&src, &idx, &p, yaw, &n, &unknown);
  if (!ok) { dir_hide(); return; }
  g_dirSrc = src; g_dirIdx = idx; g_dirP = p;
  g_dirYawN = (n > DIR_MAXN) ? DIR_MAXN : n;
  g_dirUnknown = unknown;
  if (g_dirYawN > 0) g_dirYawArr[0] = yaw[0];
  if (g_dirYawN > 1) g_dirYawArr[1] = yaw[1];
  if (g_dirYawN > 2) g_dirYawArr[2] = yaw[2];
  dir_draw();
  {
    char s[128];
    const char* what = "点位";
    if (src == 1) what = (g_mk[idx].type == MT_CROUCH) ? "蹲守点" : "守卫点";
    else if (src == 2) what = (g_vf[idx].kind == K_CROUCH) ? "蹲守点" : "守卫点";
    if (unknown)
      snprintf(s, sizeof s, "%s · 朝向未知（读不到 zoomPos）", what);
    else if (g_dirYawN > 1)
      snprintf(s, sizeof s, "%s · 朝向 %s %.0f° · %d 个方向", what, yaw_zh(g_dirYawArr[0]), g_dirYawArr[0], g_dirYawN);
    else
      snprintf(s, sizeof s, "%s · 朝向 %s %.0f°", what, yaw_zh(g_dirYawArr[0]), g_dirYawArr[0]);
    dir_label_set(s, (src == 1 && g_mk[idx].type == MT_CROUCH) || (src == 2 && g_vf[idx].kind == K_CROUCH)
                       ? &COL_CROUCH : &COL_POS);
  }
}

static void vis_show(int on) {
  int i;
  for (i = 0; i < g_visObjN; i++) if (g_visObj[i]) ((set_active_t)RVA(R_SETACTIVE))(g_visObj[i], (unsigned char)on, 0);
}

/* 单向边箭头只在 F2 菜单打开时显示：关菜单就藏起来，正常游玩画面干净。
 * 状态没变就不碰 SetActive（每 tick 都会调）。 */
static void edge_dir_sync(void) {
  int want = g_wpMenuOpen ? 1 : 0;
  if (!g_edgeArrowGo || !uobj_live(g_edgeArrowGo)) { g_edgeArrowOn = -1; return; }
  if (want == g_edgeArrowOn) return;
  ((set_active_t)RVA(R_SETACTIVE))(g_edgeArrowGo, (unsigned char)want, 0);
  g_edgeArrowOn = want;
}

static void vis_clear(void) {
  int i;
  for (i = 0; i < g_visObjN; i++) if (g_visObj[i]) ((destroy_t)RVA(R_DESTROY))(g_visObj[i], 0);
  g_visObjN = 0;
  g_edgeArrowGo = 0;
  g_edgeArrowOn = -1;
  g_vnN = g_veN = g_vfN = 0;
  g_nN = g_eN = g_jN = g_tpN = 0;
  g_pmN = 0;
}

static void vis_rebuild(void) {
  vis_clear();
  g_cArea = g_cPos = g_cCrouch = g_cSpawn = g_cJump = g_cTag = 0;
  g_miss[0] = 0;
  read_nav();
  if (g_visNano)   read_nano();   else miss("vis_nano=off");
  if (g_visCrouch) read_crouch(); else miss("vis_crouch=off");
  if (g_visBorn || g_visSupply) read_spawns();
  else miss("vis_born/supply=off");
  /* 跳点 / 标签区走 FindObjectsOfType，不碰静态名单，各有一个自己的开关。 */
  if (g_visJump) read_jump(); else miss("vis_jump=off");
  if (g_visTag)  read_tags(); else miss("vis_tag=off");
  if (g_visPm)   pm_load(1);  else g_pmN = 0;   /* 玩家坐标记录：读文件 */
  vis_draw();
  vis_show(1);
  edge_dir_sync();          /* 刚重建的对象默认是 show 的，按菜单状态立刻纠正 */
  /* 2026-11-26：删掉 `guard=%d`。guard（旧 Bot_GuardArea）随旧守卫一起删了，计数器
   * 早没了、格式串漏改，结果从这里往后所有参数整体错位：spawn/jump/tag 打的是别的数，
   * badtr 打垃圾、missing 把野指针交给 %s。日志是排查的唯一入口，错位比没日志更坑。 */
  elog("vis: nodes=%d edges=%d features=%d (area=%d pos=%d crouch=%d spawn=%d jump=%d tag=%d) badnode=%d badconn=%d badtr=%d missing=[%s]",
       g_vnN, g_veN, g_vfN, g_cArea, g_cPos, g_cCrouch, g_cSpawn, g_cJump, g_cTag,
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
  g_pmSesN = 0;            /* 本次记的方块只活在这一张图：换图即清（文件里的日志不动） */
  g_edgeArrowGo = 0;
  g_edgeArrowOn = -1;
  g_vnN = g_veN = g_vfN = 0;
  g_nN = g_eN = g_jN = g_tpN = 0;
  g_miss[0] = 0;
  g_sceneAge = 0;          /* 新图：组件表要等稳定才读 */
  g_badTr = 0;
  g_visDirty = g_visOn;
  /* 守卫区线框对象随旧图一起销毁：指针作废，下一 tick 重新建 */
  {
    int pi;
    for (pi = 0; pi < 2; pi++) {
      g_pendGo[pi] = g_pendMesh[pi] = g_pendMf[pi] = g_pendMr[pi] = 0;
      g_pendSig[pi] = 0;
      g_pendShownA[pi] = 0;
    }
  }
  g_nanoSeenN = 0;
  /* 可走面的 Mesh 对象随旧场景一起被销毁：指针作废，下一帧重建 */
  g_nmObjN = 0;
  g_nmDirty = 1;
  /* 材质同样是"上一张图"的东西：旧图的 shader 会被游戏卸载，留着就是洋红。
   * 换图一律丢掉，下一帧按新场景重新 Shader.Find + 上色（2026-11-20 修）。 */
  mat_reset("scene change");
}

static void vis_toggle(void) {
  g_visOn = !g_visOn;
  if (g_visOn) { g_visDirty = 0; vis_rebuild(); }
  else vis_show(0);
  /* 2026-11-26：标记球跟着总开关一起显隐（以前它们脱离 Ctrl+V，关掉可视化还漂在场景里） */
  mk_vis_apply();
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
  if (!g_nmShow) return;
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
  /* 网格已经建好、但材质后来死了（换图资源卸载/被 GC）：整块重建一次，
   * 否则屏幕上就是一片洋红三角网。 */
  if (g_nmObjN && !mat_alive(g_matSlot[15])) {
    elog("navmesh: material dead - rebuild");
    nm_clear();
    mat_drop(15);
    g_matReady = 0;   /* 旧原型/旧 shader 可能一起没了，重新 mat_setup */
    g_nmDirty = 1;
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

/* ---- 方向罗盘（屏幕下方正中，汉字；刻意做成和工作台 3D 罗盘一个样子）----
 * 和路点工作台（workbench/nav-studio-app.js）、3D 查看器（tools/navview.html）
 * 的罗盘是同一套方向约定，改一处必须三处一起改：
 *     北 = 世界 -Z（俯视 / 平面图的正上方）   东 = 世界 +X（右）
 *     南 = 世界 +Z（下）                     西 = 世界 -X（左）
 *
 * 样子：
 *   · 一圈**刻度**围成表盘（每 10° 一根：每 90° 金色长刻度、每 30° 亮短刻度、
 *     其余小点）。刻度是「丨/|」这类竖线字形绕圆心摆出来的，所以天生是径向的。
 *   · 表盘挂在「旋转容器」下面，容器绕 Z 转 = 圈在转：相机朝向 a（0=北、90=东）
 *     时容器转 a 度，当前那一格正好转到正上方。
 *   · 北/东/南/西 四个汉字**不挂在容器里、也从不旋转**：位置按「方位角 - 相机
 *     朝向」摆到圈上（compass_move_rose），字本身永远是正的。
 *     2026-11-20 用户反馈：以前四个字跟着容器一起转，转到东南就必须歪着头看，
 *     截图里 东/南 就是躺着的 —— 所以改成「刻度转、字不转」。
 *   · 最靠近正上方的那一格点亮成金色（其余灰蓝），圈心写八向朝向（不转）
 *   · 圈外正上方一个金色三角 = 指针
 * 每帧只改「容器一个 eulerAngles + 四个字的 anchoredPosition」，不重建文字网格，
 * 10 ms 采样定时器里节流到 ~30 Hz 也几乎不花 CPU。
 * 开关：ucf_mod.json 的 vis_compass（默认开），游戏内 Ctrl+Shift+7 随时切。
 * 与可视化总开关无关：visualizer 关着也照样显示。 */
#define COMPASS_CY      112.0f  /* 圈心离屏幕下沿的像素 */
#define COMPASS_LABEL_R 44.0f   /* 方位字半径（在刻度圈里面） */
#define COMPASS_PTR_DY  84.0f   /* 金三角在圈心上方多少像素（贴在刻度圈外沿） */
#define COMPASS_TICK_R  64.0f   /* 刻度圈半径 */
#define COMPASS_TICKS   36      /* 刻度数：每 10° 一根（90/180/270 处正好是直角刻度） */
static const char* const g_dirCn[8] = { "北","东北","东","东南","南","西南","西","西北" };
static const char* const g_dirEn[8] = { "N","NE","E","SE","S","SW","W","NW" };
static const COL COL_DIR_ROSE = { 0.66f, 0.75f, 0.86f, 1.0f };   /* 方位字：灰蓝（同工作台 #a8bed6） */
static const COL COL_DIR_HEAD = { 1.00f, 0.82f, 0.29f, 1.0f };   /* 当前朝向：金（同工作台 #ffd24a） */
static const COL COL_DIR_CENT = { 0.91f, 0.95f, 1.00f, 1.0f };   /* 圈心朝向字（同工作台 #e8f2ff） */
static const COL COL_DIR_RING = { 0.49f, 0.62f, 0.77f, 0.45f };   /* 细圈 ○ */
static P g_compRoot;        /* 罗盘根：显隐只动它一个 */
static P g_compRing;        /* 旋转容器：四个方位字挂它下面，转它 = 圈在转 */
static P g_compRose[4];     /* 北 东 南 西（挂在 g_compRing 下，本地坐标不动） */
static P g_compHead;        /* 圈心：当前朝向（不转） */
static P g_compPtr;         /* 顶部金色三角（不转） */
static float g_compRot = -999.0f;  /* 上次写进容器的 Z 旋转（度，-999 = 还没写） */
static int g_compDir = -1;  /* 上次写进圈心的扇区（0=北 … 7=西北，-1=还没写） */
static int g_compLit = -1;  /* 上次点亮的是哪个方位字（0=北 1=东 2=南 3=西） */
static int g_compOn;        /* 现在是不是显示着（省掉重复 SetActive） */

static void overlay_reset(void);

/* ---- 临时实验开关（2026-11-20 排查「进图闪退」用，定位完就删）---------- */
static int dbg_env(const char* name) {
  char v[32];
  DWORD n;
  memset(v, 0, sizeof v);
  n = GetEnvironmentVariableA(name, v, (DWORD)sizeof v);
  return (n > 0 && n < (DWORD)sizeof v && v[0] && v[0] != '0') ? 1 : 0;
}
static int g_dbgRead;
static int g_dbgNoEmpty, g_dbgInactive, g_dbgNoDots, g_dbgNoCompass, g_dbgNoSetText;
static void dbg_init(void) {
  if (g_dbgRead) return;
  g_dbgRead = 1;
  g_dbgNoEmpty   = dbg_env("UCF_UI_NOEMPTY");
  g_dbgInactive  = dbg_env("UCF_UI_INACTIVE");
  g_dbgNoDots    = dbg_env("UCF_UI_NODOTS");
  g_dbgNoCompass = dbg_env("UCF_UI_NOCOMPASS");
  g_dbgNoSetText = dbg_env("UCF_UI_NOSETTEXT");
  elog("ui: dbg flags noempty=%d inactive=%d nodots=%d nocompass=%d nosettext=%d",
       g_dbgNoEmpty, g_dbgInactive, g_dbgNoDots, g_dbgNoCompass, g_dbgNoSetText);
}

static void compass_reset(void) {
  int i;
  g_compRoot = 0;
  g_compRing = 0;
  for (i = 0; i < 4; i++) g_compRose[i] = 0;
  g_compHead = 0;
  g_compPtr = 0;
  g_compRot = -999.0f;
  g_compDir = -1;
  g_compLit = -1;
  g_compOn = 0;
}

static void compass_text(P t, const char* s, const COL* col) {
  if (!t || !uobj_live(t)) return;
  ((set_txt_t)RVA(R_TEXT_SETTEXT))(t, x_string_new(s), 0);
  if (col) ((set_col_t)RVA(R_GRAPHIC_COL))(t, *col, 0);
}

/* 静默版：刻度有 36 根，逐根打 compass: text 会把日志刷爆 */
static void txt_quiet(P t, const char* s, const COL* col) {
  dbg_init();
  if (g_dbgNoSetText) return;
  if (g_dbgNoEmpty && (!s || !s[0])) return;
  if (!t || !uobj_live(t)) return;
  ((set_txt_t)RVA(R_TEXT_SETTEXT))(t, x_string_new(s), 0);
  if (col) ((set_col_t)RVA(R_GRAPHIC_COL))(t, *col, 0);
}

/* 四个方位字绕圈心摆位：bearing = 方位角(0=北) - 相机朝向 a。
 * 只改 anchoredPosition，**从不改 rotation** —— 这就是「字永远是正的」。
 * 屏幕坐标：x 右、y 上；bearing 从正上方顺时针量。 */

static void compass_move_rose(float a) {
  int i;
  V2 v;
  for (i = 0; i < 4; i++) {
    P tr;
    float b, rad;
    if (!g_compRose[i] || !uobj_live(g_compRose[i])) continue;
    tr = comp_tr(g_compRose[i]);
    if (!tr) continue;
    b = (float)i * 90.0f - a;
    rad = b * 0.0174533f;
    v.x = sinf(rad) * COMPASS_LABEL_R;
    v.y = cosf(rad) * COMPASS_LABEL_R;
    ((set_v2_t)RVA(R_RT_APOS))(tr, v, 0);
  }
}

/* 所有零件都挂在 g_compRoot 下，显隐只动根物体一次 */
static void compass_show(int on) {
  P go;
  if (!g_compRoot || !uobj_live(g_compRoot)) { g_compOn = 0; return; }
  go = ((get_go_t)RVA(R_GETGO))(g_compRoot, 0);
  if (go) ((set_active_t)RVA(R_SETACTIVE))(go, (unsigned char)(on ? 1 : 0), 0);
  g_compOn = on ? 1 : 0;
}

/* 视线 → 八向扇区（0 = 北）。只看水平分量，抬头低头不影响方向。 */
static int compass_bucket(const V3* fwd) {
  float a = atan2f(fwd->x, -fwd->z) * 57.29578f;
  int b;
  if (!(a == a)) return -1;                  /* NaN：相机还没就位 */
  a += 22.5f;
  a = fmodf(a, 360.0f);
  if (a < 0.0f) a += 360.0f;
  b = (int)(a / 45.0f) % 8;
  return b;
}

/* 一圈转到位：容器绕 Z 转 a 度 → 当前朝向那一格正好在正上方 */
static void compass_update(void) {
  V3 pos, fwd, eul;
  float a, best = 1e9f;
  int b, i, lit = 0;
  if (!g_compHead || !uobj_live(g_compHead)) return;
  if (!cam_ray(&pos, &fwd)) return;
  a = atan2f(fwd.x, -fwd.z) * 57.29578f;      /* 0 = 北，90 = 东：和工作台/游戏里同一个方向约定 */
  if (!(a == a)) return;                       /* NaN：相机还没就位 */
  a -= floorf(a / 360.0f) * 360.0f;            /* 归到 [0,360) */
  {
    /* 节流：转不到 0.08° 就一次都不算。表盘（刻度）和四个字共用一个阈值，
     * 这样「刻度转到哪、字就摆到哪」永远同步。 */
    float d = a - g_compRot;
    while (d > 180.0f) d -= 360.0f;
    while (d < -180.0f) d += 360.0f;
    if (fabsf(d) > 0.08f) {
      if (g_compRing && uobj_live(g_compRing)) {
        P tr = comp_tr(g_compRing);            /* 组件 → Transform 必须用 Component.get_transform */
        if (tr) {
          eul.x = 0.0f; eul.y = 0.0f; eul.z = a;
          ((set_pos_t)RVA(R_SET_EULER))(tr, eul, 0);
        }
      }
      compass_move_rose(a);                    /* 字只挪位置、不转，见 compass_move_rose */
      g_compRot = a;
    }
  }
  /* 离正上方最近的方位字点亮（正好 45° 时取先出现的那个，和网页端同一规则） */
  for (i = 0; i < 4; i++) {
    float d = a - i * 90.0f;
    while (d > 180.0f) d -= 360.0f;
    while (d < -180.0f) d += 360.0f;
    if (fabsf(d) < best) { best = fabsf(d); lit = i; }
  }
  b = compass_bucket(&fwd);
  if (b < 0) return;
  if (b == g_compDir && lit == g_compLit) return;
  g_compDir = b;
  if (lit != g_compLit) {
    g_compLit = lit;
    for (i = 0; i < 4; i++)
      compass_text(g_compRose[i], g_cjk ? g_dirCn[i * 2] : g_dirEn[i * 2],
                   i == lit ? &COL_DIR_HEAD : &COL_DIR_ROSE);
  }
  compass_text(g_compHead, g_cjk ? g_dirCn[b] : g_dirEn[b], &COL_DIR_CENT);
}

/* 挂在 UCF_HUD 这张 Canvas 下：锚点 = 屏幕下沿正中，锚点坐标是像素。
 * 结构：根 → { 表盘小点 ×32（不转）, 旋转容器 → 四个方位字, 圈心朝向, 指针 }
 * 建的顺序 = 绘制顺序，所以小点在字下面。 */
static void compass_build(P canvasTr) {
  static const float lx[4] = { 0.0f, COMPASS_LABEL_R, 0.0f, -COMPASS_LABEL_R };   /* 北 东 南 西 */
  static const float ly[4] = { COMPASS_LABEL_R, 0.0f, -COMPASS_LABEL_R, 0.0f };
  static const char* const nm[4] = { "UCF_HUD_DirN", "UCF_HUD_DirE", "UCF_HUD_DirS", "UCF_HUD_DirW" };
  const char* dot = "|";
  const char* minor = "·";
  P rootTr = 0, ringTr = 0;
  int i;
  compass_reset();
  if (!canvasTr) return;

  /* 根：空 Text 只当 RectTransform 用；显隐、定位都动它 */
  g_compRoot = mk_text_ui(canvasTr, "UCF_HUD_DirRoot", 0.5f, 0.0f, 0.5f, 0.5f,
                          0.0f, COMPASS_CY, 8.0f, 8.0f, 10);
  if (!g_compRoot) { elog("compass: root text failed"); return; }
  root_put(g_compRoot);
  compass_text(g_compRoot, "", 0);
  rootTr = comp_tr(g_compRoot);   /* 传 GameObject 的 get_transform 会把 Text* 当 GameObject* 用 → 崩 */

  /* 旋转容器：只装**刻度**。转它 = 表盘在转，刻度天然是径向的。 */
  elog("compass: stage ring");
  g_compRing = mk_text_ui(rootTr ? rootTr : canvasTr, "UCF_HUD_DirRing", 0.5f, 0.5f, 0.5f, 0.5f,
                          0.0f, 0.0f, 8.0f, 8.0f, 10);
  if (g_compRing) {
    root_put(g_compRing);
    compass_text(g_compRing, "", 0);
    ringTr = comp_tr(g_compRing);
  }
  elog("compass: stage ticks ringTr=%p", ringTr);

  /* 刻度圈：每 10° 一根。竖线字形绕圆心摆 + 各自转成径向：
   *   每 90°（0/90/180/270）金色长刻度，每 30° 亮短刻度，其余小点。 */
  if (g_guiFont && ((has_char_t)RVA(R_FONT_HASCHAR))(g_guiFont, 0x4E28, 0)) dot = "丨";
  else if (g_guiFont && ((has_char_t)RVA(R_FONT_HASCHAR))(g_guiFont, 0x007C, 0)) dot = "|";
  else dot = ".";   /* 字体里连竖线都没有（几乎不可能）：退化成小点 */
  if (!(g_guiFont && ((has_char_t)RVA(R_FONT_HASCHAR))(g_guiFont, 0x00B7, 0))) minor = ".";
  elog("compass: stage ticks (%d, bar='%s')", COMPASS_TICKS, dot);
  for (i = 0; i < COMPASS_TICKS && !g_dbgNoDots; i++) {
    float deg = (float)i * (360.0f / (float)COMPASS_TICKS);
    float rad = deg * 0.0174533f;
    int cardinal = ((i % (COMPASS_TICKS / 4)) == 0);    /* 0 / 90 / 180 / 270 */
    int major = ((i % (COMPASS_TICKS / 12)) == 0);      /* 每 30° */
    const char* glyph = major ? dot : minor;
    P t = mk_text_ui(ringTr ? ringTr : canvasTr, "UCF_HUD_DirTick", 0.5f, 0.5f, 0.5f, 0.5f,
                     sinf(rad) * COMPASS_TICK_R, cosf(rad) * COMPASS_TICK_R,
                     16.0f, 18.0f, cardinal ? 15 : (major ? 12 : 10));
    if (!t) continue;
    ((set_int1_t)RVA(R_TEXT_ALIGN))(t, 4, 0);           /* MiddleCenter */
    root_put(t);
    txt_quiet(t, glyph, cardinal ? &COL_DIR_HEAD : (major ? &COL_DIR_ROSE : &COL_DIR_RING));
    {
      P tr = comp_tr(t);
      V3 e;
      if (tr) {
        e.x = 0.0f; e.y = 0.0f; e.z = -deg;             /* 竖线转成「指向圆心」的径向刻度 */
        ((set_pos_t)RVA(R_SET_EULER))(tr, e, 0);
      }
    }
  }

  /* 四个方位字：挂根物体、**从不旋转**（跟着容器转会变成截图里那种歪字），
   * 位置由 compass_move_rose() 每帧按「方位角 - 朝向」摆到圈上。 */
  elog("compass: stage labels");
  for (i = 0; i < 4; i++) {
    P t = mk_text_ui(rootTr ? rootTr : canvasTr, nm[i], 0.5f, 0.5f, 0.5f, 0.5f,
                     lx[i], ly[i], 56.0f, 20.0f, 13);
    if (!t) continue;
    ((set_int1_t)RVA(R_TEXT_ALIGN))(t, 4, 0);           /* MiddleCenter */
    g_compRose[i] = t;
    root_put(t);
    compass_text(t, g_cjk ? g_dirCn[i * 2] : g_dirEn[i * 2], &COL_DIR_ROSE);
  }

  /* 圈心朝向（不转）+ 顶部金三角指针（不转） */
  elog("compass: stage head");
  g_compHead = mk_text_ui(rootTr ? rootTr : canvasTr, "UCF_HUD_DirHead", 0.5f, 0.5f, 0.5f, 0.5f,
                          0.0f, 0.0f, 60.0f, 20.0f, 15);
  if (g_compHead) {
    ((set_int1_t)RVA(R_TEXT_ALIGN))(g_compHead, 4, 0);
    root_put(g_compHead);
    compass_text(g_compHead, "--", &COL_DIR_CENT);   /* 紧接着的 compass_update 会写成真朝向 */
  }
  {
    const char* ptr = 0;
    if (g_guiFont && ((has_char_t)RVA(R_FONT_HASCHAR))(g_guiFont, 0x25B2, 0)) ptr = "▲";
    else if (g_guiFont && ((has_char_t)RVA(R_FONT_HASCHAR))(g_guiFont, 0x25B3, 0)) ptr = "△";
    else ptr = "^";
    g_compPtr = mk_text_ui(rootTr ? rootTr : canvasTr, "UCF_HUD_DirPtr", 0.5f, 0.5f, 0.5f, 0.5f,
                           0.0f, COMPASS_PTR_DY, 34.0f, 24.0f, 18);
    if (g_compPtr) {
      ((set_int1_t)RVA(R_TEXT_ALIGN))(g_compPtr, 4, 0);
      root_put(g_compPtr);
      compass_text(g_compPtr, ptr, &COL_DIR_HEAD);
    }
  }

  g_compOn = 1;
  g_compRot = -999.0f;
  g_compDir = -1;
  g_compLit = -1;
  elog("compass: stage update");
  compass_update();                    /* 立刻写一次，别等下一个 tick */
  elog("compass: stage update done");
  if (!g_visCompass) compass_show(0);
  elog("compass: built (%s) root=%p dot='%s' x%d ring=%p rose=%p head=%p ptr='%s'",
       g_cjk ? "CJK" : "ASCII", g_compRoot, dot, COMPASS_TICKS, g_compRing,
       g_compRose[0], g_compHead, g_compPtr ? "set" : "none");
}

/* 每 tick（navfix 的 250 ms 心跳）跑一次：管建 / 显示 / 隐藏 */
static void compass_tick(void) {
  if (!g_visCompass) {
    if (g_compOn) compass_show(0);
    return;
  }
  if (!g_compHead || !uobj_live(g_compHead)) return;   /* 还没建 / 换图重建中 */
  if (!g_compOn) compass_show(1);
  compass_update();
}

/* 转镜头时用的快 tick（navfix 的 10 ms 采样定时器，节流到 ~30 Hz）：
 * 只做「容器转几度 + 换字/换色」，对象没建好时立刻返回。 */
void editor_compass_tick(void) {
  static int spin;
  if (!g_visCompass || !g_compOn) return;
  if (!g_compRing || !uobj_live(g_compRing)) return;
  if (spin++ & 1) return;
  compass_update();
}

/* 罗盘开关（控制台「可视化」页 vis_compass 实时下发；原来的 Ctrl+Shift+7 已下线） */
static void compass_apply(int on) {
  g_visCompass = on ? 1 : 0;
  elog("compass: %s (vis_compass)", g_visCompass ? "ON" : "OFF");
  if (!g_visCompass) { compass_show(0); return; }
  if (!g_compHead || !uobj_live(g_compHead)) {          /* 画布还没建：整块重建 */
    overlay_reset();
    overlay_refresh();
  }
  compass_tick();
}

static void toast_build(P canvasTr);
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
  /* 2026-11-20：删掉「退回 Resources.GetBuiltinResource(Arial.ttf)」这条兜底。
   * 场景里一个 UGUI Text 都没有时（车测 / 直进图 LoadScene 的瞬间，
   * find_cjk_font 会报 "no cjk font among 0 Text objects"），那条兜底拿到的
   * Font 去 SetFont + SetText 会让 UnityPlayer 在 +0x76019d 直接 0xC0000005
   * （读 0xfffffc4a）—— 2026-11-19 与 2026-11-20 两次车测崩的都是这条路径。
   * 现在改成：这一次不建覆盖层，等场景 UI 起来（下一个 2 s 心跳）再建。 */
  if (!g_guiFont) {
    elog("ui: no font in scene yet (0 Text objects) - overlay skipped, retry on next tick");
    return 0;
  }
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
  dbg_init();
  if (g_dbgInactive) ((set_active_t)RVA(R_SETACTIVE))(canvasGo, 0, 0);
  canvasTr = get_tr(canvasGo);

  /* left-edge legend: three horizontal rows, stacked vertically */
  g_cat = mk_text_ui(canvasTr, "UCF_HUD_Cats", 0.0f, 0.5f, 0.0f, 0.5f, 14.0f, -140.0f, 520.0f, 132.0f, 26);
  root_put(g_cat);
  if (g_cat) {
    elog("ui: step cat-align");
    ((set_int1_t)RVA(R_TEXT_ALIGN))(g_cat, 3, 0);   /* MiddleLeft */
    elog("ui: step cat-go");
    g_catGo = ((get_go_t)RVA(R_GETGO))(g_cat, 0);
    elog("ui: step cat-done");
  }
  /* 路点菜单：左中一列，默认空；F2 / 长按 E 才填内容 */
  g_menu = mk_text_ui(canvasTr, "UCF_HUD_Menu", 0.0f, 0.5f, 0.0f, 0.5f, 14.0f, 30.0f, 560.0f, 400.0f, 16);
  root_put(g_menu);
  if (g_menu) {
    elog("ui: step menu-align");
    ((set_int1_t)RVA(R_TEXT_ALIGN))(g_menu, 3, 0);   /* MiddleLeft */
    elog("ui: step menu-go");
    g_menuGo = ((get_go_t)RVA(R_GETGO))(g_menu, 0);
    elog("ui: step menu-done");
  }
  /* 屏幕中央提示（toast）：先建好、默认隐藏，toast_show 时才填字 */
  toast_build(canvasTr);
  /* 方向浮字（瞄准蹲守点 / 守卫点时显示「朝向 东北 42°」） */
  dir_label_build(canvasTr);
  /* 方向罗盘（东南西北）：和出生点图例共用这张 Canvas，开关见 vis_compass */
  dbg_init();
  elog("ui: step compass-begin");
  if (!g_dbgNoCompass) compass_build(canvasTr);
  elog("ui: step compass-done");
  /* 记下 Transform 的类对象：comp_pos 用它区分「真 Transform」和野指针 */
  if (!g_trKlass && g_cat) {
    P t = comp_tr(g_cat);
    if (t && mem_ok(t, 0x10) && uobj_live(t)) {
      g_trKlass = *(P*)t;
      /* UI 的 transform 是 RectTransform，普通 GameObject 的是 Transform（父类）。
       * 只记 UI 那个类会让 comp_pos 把所有非 UI 组件都当成野指针：
       * 跳跃/蹲守/守卫区一个都读不出来（日志里 badtr 恰好等于跳链个数就是这么来的）。 */
      g_trBaseKlass = x_class_get_parent ? x_class_get_parent(g_trKlass) : 0;
      elog("ui: transform klass=%p base=%p", g_trKlass, g_trBaseKlass);
    }
  }
  if (g_dbgInactive) ((set_active_t)RVA(R_SETACTIVE))(canvasGo, 1, 0);
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

static void overlay_reset(void) {
  g_cat = 0; g_catGo = 0; g_menu = 0; g_menuGo = 0;
  g_toast = 0; g_toastGo = 0; g_toastSh = 0; g_toastShGo = 0; g_toastUntil = 0;
  g_dirLabel = 0; g_dirLabelGo = 0; g_dirText[0] = 0;
  g_dirGo = 0; g_dirMf = 0; g_dirMr = 0; g_dirMesh = 0; g_dirSig = 0; g_dirShown = 0;
  compass_reset();          /* 罗盘挂在同一张 Canvas 上，一起丢 */
}

/* ---- 屏幕中央提示（toast）------------------------------------------------
 * 2026-11-26 用户要求：不能做的操作（比如这张图没有空槽位、加不了点）必须给反馈，
 * 在屏幕中央显示文字、颜色明显，不要弹窗。
 * 实现：和 F2 菜单同一张 ScreenSpaceOverlay Canvas，两个 UGUI Text（黑影 + 亮红字），
 * 锚点/轴心都在屏幕中心、Y 上移 TOAST_Y（不压准星），TOAST_MS 后自动隐藏。
 * 换图时旧 Canvas 随场景销毁：overlay_reset 清零指针，toast_show 里验活重建。 */
static void toast_build(P canvasTr) {
  g_toastSh = mk_text_ui(canvasTr, "UCF_HUD_ToastSh", 0.5f, 0.5f, 0.5f, 0.5f,
                         2.0f, TOAST_Y - 2.0f, 1100.0f, 96.0f, 34);
  if (g_toastSh) {
    root_put(g_toastSh);
    ((set_int1_t)RVA(R_TEXT_ALIGN))(g_toastSh, 4, 0);        /* MiddleCenter */
    ((set_col_t)RVA(R_GRAPHIC_COL))(g_toastSh, COL_TOAST_SH, 0);
    g_toastShGo = ((get_go_t)RVA(R_GETGO))(g_toastSh, 0);
    if (g_toastShGo) ((set_active_t)RVA(R_SETACTIVE))(g_toastShGo, 0, 0);
  }
  g_toast = mk_text_ui(canvasTr, "UCF_HUD_Toast", 0.5f, 0.5f, 0.5f, 0.5f,
                       0.0f, TOAST_Y, 1100.0f, 96.0f, 34);
  if (g_toast) {
    root_put(g_toast);
    ((set_int1_t)RVA(R_TEXT_ALIGN))(g_toast, 4, 0);
    ((set_col_t)RVA(R_GRAPHIC_COL))(g_toast, COL_TOAST, 0);
    g_toastGo = ((get_go_t)RVA(R_GETGO))(g_toast, 0);
    if (g_toastGo) ((set_active_t)RVA(R_SETACTIVE))(g_toastGo, 0, 0);
  }
}
/* 方向浮字：准星下方一行（锚点屏幕中心、轴心在上边 → 字在准星下方 58 px）。
 * 只在瞄准有方向的点位时显示；内容不变不重设文本（每帧 x_string_new 会喂 GC）。 */
static void dir_label_build(P canvasTr) {
  g_dirLabel = mk_text_ui(canvasTr, "UCF_HUD_DirText", 0.5f, 0.5f, 0.5f, 1.0f,
                          0.0f, -58.0f, 900.0f, 40.0f, 16);
  g_dirLabelGo = 0;
  g_dirText[0] = 0;
  if (!g_dirLabel) return;
  root_put(g_dirLabel);
  ((set_int1_t)RVA(R_TEXT_ALIGN))(g_dirLabel, 4, 0);      /* MiddleCenter */
  ((set_col_t)RVA(R_GRAPHIC_COL))(g_dirLabel, COL_WHITE, 0);
  g_dirLabelGo = ((get_go_t)RVA(R_GETGO))(g_dirLabel, 0);
  if (g_dirLabelGo) ((set_active_t)RVA(R_SETACTIVE))(g_dirLabelGo, 0, 0);
}

/* 弹一条提示：col 决定颜色，ms 决定停留时间；同一条消息 0.5 s 内只刷一次（连按不闪）。 */
static void toast_v(const COL* col, unsigned ms, const char* fmt, va_list ap) {
  char msg[320];
  static char prev[320];
  static unsigned lastMs;
  unsigned now = GetTickCount();
  vsnprintf(msg, sizeof msg, fmt, ap);
  if (!msg[0]) return;
  if (lastMs && !strcmp(prev, msg) && now - lastMs < 500) return;   /* 连按：不重复闪 */
  strncpy(prev, msg, sizeof prev - 1);
  prev[sizeof prev - 1] = 0;
  lastMs = now;
  if (!g_toast || !uobj_live(g_toast)) {
    /* 换图 / 第一次：Canvas 可能整个没了，重建一次 */
    overlay_reset();
    overlay_refresh();
  }
  if (!g_toast || !uobj_live(g_toast)) { elog("toast: ui not ready: %s", msg); return; }
  ((set_txt_t)RVA(R_TEXT_SETTEXT))(g_toast, x_string_new(msg), 0);
  ((set_col_t)RVA(R_GRAPHIC_COL))(g_toast, *col, 0);
  if (g_toastSh && uobj_live(g_toastSh))
    ((set_txt_t)RVA(R_TEXT_SETTEXT))(g_toastSh, x_string_new(msg), 0);
  if (g_toastGo) ((set_active_t)RVA(R_SETACTIVE))(g_toastGo, 1, 0);
  if (g_toastShGo) ((set_active_t)RVA(R_SETACTIVE))(g_toastShGo, 1, 0);
  g_toastUntil = now + ms;
  elog("toast: %s", msg);
}
/* 两种语义：成功（绿，短）/ 禁止失败（红，长）。
 * 「提示下一步」那类黄字（已选 A、当前类型…）用户明确说不要，已删除 ——
 * 下一步怎么做菜单里本来就写着，屏幕上再弹一遍只会挡视线。 */
static void toast_ok(const char* fmt, ...) {
  va_list ap;
  va_start(ap, fmt);
  toast_v(&COL_TOAST_OK, TOAST_MS_OK, fmt, ap);
  va_end(ap);
}
static void toast_bad(const char* fmt, ...) {
  va_list ap;
  va_start(ap, fmt);
  toast_v(&COL_TOAST, TOAST_MS_ERR, fmt, ap);
  va_end(ap);
}
/* 到点隐藏（主线程 tick 调） */
static void toast_tick(void) {
  if (!g_toastUntil) return;
  if (!g_toast || !uobj_live(g_toast)) { g_toastUntil = 0; return; }
  if ((int)(GetTickCount() - g_toastUntil) >= 0) {
    if (g_toastGo) ((set_active_t)RVA(R_SETACTIVE))(g_toastGo, 0, 0);
    if (g_toastShGo) ((set_active_t)RVA(R_SETACTIVE))(g_toastShGo, 0, 0);
    g_toastUntil = 0;
  }
}

/* ---- marker store ------------------------------------------------------- */
/* 标记球（markers.txt 里的蹲守点 / 守卫点 / 守卫区 / 跳链 / 标签区长得像"小圆球"的
 * 那个可视化物体）的显隐。2026-11-26 用户要求：球必须跟着可视化总开关走，不能是两套。
 * 规则：Ctrl+V 开 且 Ctrl+0 开 → 显示；任一关掉 → 藏起来。
 * 为什么取交集：Ctrl+V 是"整个场景要干净"的总闸，Ctrl+0 只是"编辑时单独把球收掉"
 * 的细开关，各自都要管用。 */
static void mk_vis_apply(void) {
  int i, on = g_visOn ? 1 : 0;
  for (i = 0; i < g_n; i++) {
    P v = g_mk[i].vis;
    if (!v || !uobj_live(v)) continue;
    ((set_active_t)RVA(R_SETACTIVE))(v, (unsigned char)on, 0);
  }
}

static int add_mk(int type, V3 p, int aid, int parent, int prm, P go, P comp, P vis) {
  MK* m;
  if (g_n >= MAXM) { elog("marker store full (%d)", MAXM); return 0; }
  m = &g_mk[g_n];
  m->type = type; m->p = p; m->aid = aid; m->parent = parent; m->prm = prm;
  m->yaw = YAW_NONE;      /* 有朝向的类型由 make_* 自己填（蹲守点 / 守卫点） */
  m->go = go; m->comp = comp; m->vis = vis;
  g_n++;
  /* 新点的球也要按当前两个开关摆好：Ctrl+V 关着时建点不能在场景里冒出一个球。
   * 只处理这一个（不调 mk_vis_apply）：读图时几百个点逐个进来，全量刷 = 几十万次
   * SetActive，白等。 */
  if (vis && !g_visOn) ((set_active_t)RVA(R_SETACTIVE))(vis, 0, 0);
  g_visDirty = 1;      /* 新建标记后让可视化/计数下一帧重读 */
  return 1;
}

/* 守卫点 / 蹲守点「看哪儿」的读写（zoomPos@0x10，Vector3[]，世界目标点）
 * 写：数组只有一个元素 = p + dir(yaw)*DIR_RANGE，和点同高（只表达水平朝向）。
 * 读：原生/我们建的点都走这条。返回方向个数（可能 0 = 未知）。 */
static P vec3_arr_new(const V3* v, int n);      /* 定义在 make_crouch 后面 */
static int write_zoom(P comp, const V3* p, float yaw) {
  V3 d, t;
  P arr;
  unsigned h = 0;
  if (!comp || !p) return 0;
  if (yaw <= YAW_NONE + 1.0f) return 0;
  if (!mem_ok(comp, 0x14)) return 0;
  dir_of_yaw(yaw, &d);
  t.x = p->x + d.x * DIR_RANGE;
  t.y = p->y;
  t.z = p->z + d.z * DIR_RANGE;
  arr = vec3_arr_new(&t, 1);
  if (!arr) return 0;
  if (x_gchandle_new) h = x_gchandle_new(arr, 0);          /* 写字段期间先钉住 */
  if (x_gc_wbarrier_set_field) x_gc_wbarrier_set_field(comp, (char*)comp + 0x10, arr);
  *(P*)((char*)comp + 0x10) = arr;
  if (h && x_gchandle_free) x_gchandle_free((P)(size_t)h);
  return 1;
}
static int read_zoom(P comp, const V3* p, float* out, int cap) {
  P arr;
  int n, i, k = 0;
  if (!comp || !p || !out || cap <= 0) return 0;
  if (!mem_ok(comp, 0x14)) return 0;
  arr = *(P*)((char*)comp + 0x10);
  if (!arr || !mem_ok(arr, 0x14)) return 0;
  n = *(int*)((char*)arr + 0x0C);
  if (n <= 0 || n > 64) return 0;
  if (!mem_ok((char*)arr + 0x10, (size_t)n * 12)) return 0;
  for (i = 0; i < n && k < cap; i++) {
    V3 v = *(V3*)((char*)arr + 0x10 + i * 12);
    V3 d;
    float y;
    d.x = v.x - p->x; d.y = 0.0f; d.z = v.z - p->z;
    if (d.x * d.x + d.z * d.z < 0.25f) continue;           /* 目标贴在点上：没有意义 */
    y = yaw_of_dir(&d);
    if (y <= YAW_NONE + 1.0f) continue;
    if (k > 0 && fabsf(y - out[0]) < 2.0f) continue;       /* 和主方向重复（并入口点常见） */
    out[k++] = y;
  }
  return k;
}

static int make_crouch(V3 p, float yaw) {
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
  g_mk[g_n - 1].yaw = yaw;
  /* 2026-11-27：以前这里不写 zoomPos（null）→ 人机在这个点蹲下后「朝哪架枪」是未定义的。
   * 现在按放置时的相机朝向写一个世界目标点（见文件顶部 zoomPos 说明）。 */
  if (yaw > YAW_NONE + 1.0f && write_zoom(comp, &p, yaw))
    elog("crouch: 朝向 %.0f°（%s）→ zoomPos = p + %.0f m", yaw, yaw_zh(yaw), DIR_RANGE);
  else
    elog("crouch: 朝向未知（不写 zoomPos，人机朝向未定义）");
  elog("crouch #%d at %.2f %.2f %.2f team=%d type=%s", g_n, p.x, p.y, p.z, g_team,
       comp ? type_name(*(P*)comp) : "?");
  overlay_refresh();
  return 1;
}

/* ---- 守卫区 / 守卫点：现造要补的字段（2026-11-25 修「加守卫点」闪退）------
 * 细节见文件头那段说明。要点：数组先补成空数组/至少 1 个 zoom 方向，再 Init，
 * 最后把点挂进 area.posList；守卫区等第一个点挂好再激活。 */
static P vec3_arr_new(const V3* v, int n) {
  P a;
  if (!x_array_new || !g_vec3Cls) return 0;
  if (n < 0) n = 0;
  a = x_array_new(g_vec3Cls, (unsigned)n);
  if (a && v && n > 0) memcpy((char*)a + 0x10, v, (size_t)n * 12);
  return a;
}

static int list_count(P l) {
  int n;
  if (!l || !mem_ok(l, 0x14)) return -1;
  n = *(int*)((char*)l + 0x0C);
  return (n < 0 || n > 200000) ? -1 : n;
}

static int list_has(P l, P item) {
  int i, n = list_count(l);
  P items = list_items(l);
  if (n <= 0 || !items || !mem_ok((char*)items + 0x10, (size_t)n * 4)) return 0;
  for (i = 0; i < n; i++) {
    unsigned tmp = 0;
    memcpy(&tmp, (char*)items + 0x10 + i * 4, 4);   /* 4 字节读：别信宽写，见 purge 注释 */
    if ((P)tmp == item) return 1;
  }
  return 0;
}

/* 用游戏自己的 List<T>.Add 挂对象。exc 传非空指针 -> 托管异常变成返回值，
 * 不会一路 terminate 成闪退。 */
static int list_add_via(P madd, P l, P item, const char* tag) {
  void* args[1];
  P exc = 0;
  if (!madd || !l || !item || !x_runtime_invoke) { elog("%s: List.Add 不可用", tag); return 0; }
  if (list_has(l, item)) return 1;                   /* 已经在里面就别重复挂 */
  args[0] = item;
  x_runtime_invoke(madd, l, args, &exc);
  if (exc) { elog("%s: List.Add 抛异常（已吞掉）", tag); return 0; }
  return 1;
}

/* 守卫区四个数组补成空数组：null 会让 Bot_NanoGuardPos.Init() 的 AddRange 抛异常。
 * （GetRandomEscapePos / GetNeighborArea / GetEscapeArea 本身判空，空数组语义相同。） */
static int area_fields_ok(P comp) {
  P a;
  if (!comp) return 0;
  if (!mem_ok(comp, 0x20)) { elog("area: 组件不可读"); return 0; }
  if (!*(P*)((char*)comp + 0x0C)) {                       /* entrancePos */
    if (!(a = vec3_arr_new(0, 0))) return 0;
    *(P*)((char*)comp + 0x0C) = a;
    elog("area: entrancePos 补空数组（运行时 AddComponent 不会初始化它）");
  }
  if (!*(P*)((char*)comp + 0x14)) {                       /* neighborAreas */
    if (!g_areaCls || !x_array_new || !(a = x_array_new(g_areaCls, 0))) return 0;
    *(P*)((char*)comp + 0x14) = a;
  }
  if (!*(P*)((char*)comp + 0x18)) {                       /* escapeAreas */
    if (!g_areaCls || !x_array_new || !(a = x_array_new(g_areaCls, 0))) return 0;
    *(P*)((char*)comp + 0x18) = a;
  }
  if (!*(P*)((char*)comp + 0x1C)) {                       /* escapePos */
    if (!(a = vec3_arr_new(0, 0))) return 0;
    *(P*)((char*)comp + 0x1C) = a;
  }
  if (!*(P*)((char*)comp + 0x10)) {                       /* posList（.ctor 里 new 的） */
    elog("area: posList 是 null（.ctor 没跑？），不能挂守卫点");
    return 0;
  }
  return 1;
}

/* 点位被删空后，游戏在 GetPos 里会自己把守卫区从 SpareAreaList 摘掉；
 * 之后再加点要登记回去，不然人机永远看不到这个区。已在列表里就不重复加。 */
static void area_register(P comp) {
  P f, l = 0;
  if (!comp || !g_areaCls || !x_class_get_field_from_name || !x_field_static_get_value) return;
  f = x_class_get_field_from_name(g_areaCls, "SpareAreaList");
  if (!f) return;
  x_field_static_get_value(f, &l);
  if (!l) return;
  list_add_via(g_nareaListAdd, l, comp, "area: SpareAreaList");
}

static int make_area_aid(int scale10, V3 p, int aid) {
  P go, comp, box;
  V3 sc;
  float s = scale10 / 10.0f;
  if (aid < 0 || aid >= MAX_AID) { elog("area: bad aid=%d", aid); return 0; }
  if (g_aidUsed[aid]) {
    /* 老版本存的文件里可能出现重复 aid（删区后 g_areaCount 被减过）。
     * 这种情况下另分配一个空槽，别把别的区的槽位覆盖掉。 */
    elog("area: aid=%d 已被占用，改用新槽位", aid);
    for (aid = 0; aid < MAX_AID && g_aidUsed[aid]; aid++) ;
    if (aid >= MAX_AID) { elog("area limit %d", MAX_AID); return 0; }
  }
  if (s < 1.0f) s = 1.0f;
  go = new_go("UCF_GuardArea");
  if (!go) return 0;
  /* 先不激活：Awake 会 GetComponentsInChildren 数子物体并登记 SpareAreaList。
   * 现在还没字段/没点位就 Awake，人机就会拿到一个 posList 空的守卫区。 */
  ((set_active_t)RVA(R_SETACTIVE))(go, 0, 0);
  sc.x = s; sc.y = s; sc.z = s;
  ((set_scale_t)RVA(R_SET_SCALE))(get_tr(go), sc, 0);
  ((set_pos_t)RVA(R_SET_POS))(get_tr(go), p, 0);
  comp = ((addcomp_t)RVA(R_ADDCOMP))(go, g_areaType, 0);
  if (!comp) { elog("area: AddComponent failed"); return 0; }
  if (!area_fields_ok(comp)) { elog("area: 字段补不齐，放弃新建守卫区"); return 0; }
  if (g_boxType) {
    box = ((addcomp_t)RVA(R_ADDCOMP))(go, g_boxType, 0);
    if (box) ((set_trigger_t)RVA(R_IS_TRIGGER))(box, 1, 0);
    else elog("area: BoxCollider add failed");
  }
  g_aidMk[aid] = (P)(g_n);
  g_aidUsed[aid] = 1;
  g_areaLive[aid] = 0;
  if (aid >= g_areaCount) g_areaCount = aid + 1;   /* 上界：下一个新区的默认 aid */
  if (!add_mk(3, p, aid, -1, scale10, go, comp, spawn_vis(p, 0.42f, 3))) return 0;
  g_curArea = g_n - 1;
  elog("area #%d (aid=%d scale=%.1f) at %.2f %.2f %.2f -> current（等第一个守卫点再激活）",
       g_n - 1, aid, s, p.x, p.y, p.z);
  overlay_refresh();
  return 1;
}

static int make_area(int scale10, V3 p) {
  int aid = g_areaCount;
  if (aid >= MAX_AID) { elog("area limit %d", MAX_AID); return 0; }
  while (aid < MAX_AID && g_aidUsed[aid]) aid++;     /* 兜底：跳过被占的槽 */
  if (aid >= MAX_AID) { elog("area limit %d", MAX_AID); return 0; }
  return make_area_aid(scale10, p, aid);
}

static int make_nanopos(int aid, V3 p, int safety, float yaw) {
  P go, comp, areaGo, areaComp, areaTr, tr, list, za;
  V3 zd, zt;
  int parent, live;
  if (aid < 0 || aid >= g_areaCount) { elog("nanopos: no area aid=%d", aid); return 0; }
  parent = (int)(INT_PTR)g_aidMk[aid];
  if (parent < 0 || parent >= g_n || g_mk[parent].type != 3) { elog("nanopos: bad parent aid=%d", aid); return 0; }
  areaGo = g_mk[parent].go;
  areaComp = g_mk[parent].comp;
  if (!areaGo || !uobj_live(areaGo) || !areaComp || !uobj_live(areaComp)) {
    elog("nanopos: 守卫区对象已销毁 aid=%d（先重新建区）", aid);
    return 0;
  }
  if (!area_fields_ok(areaComp)) { elog("nanopos: 守卫区字段补不齐 aid=%d", aid); return 0; }
  go = new_go("UCF_NanoGuardPos");
  if (!go) return 0;
  ((set_active_t)RVA(R_SETACTIVE))(go, 0, 0);
  comp = ((addcomp_t)RVA(R_ADDCOMP))(go, g_posType, 0);
  if (!comp) { elog("nanopos: AddComponent failed"); return 0; }
  if (!mem_ok(comp, 0x20)) { elog("nanopos: 组件不可读"); return 0; }
  *(int*)((char*)comp + 0x1C) = safety;                 /* _safety */
  /* zoomPos 至少 1 个：Init() 里 AddRange(zoomPos) 碰 null 就抛，GetRandomZoomPos()
   * 还要按随机下标取。
   * 2026-11-27：以前给的是两个固定值 {(0,0,1),(1,0,0)}，被游戏当成**世界点** ——
   * 所有人机都朝世界原点方向看（和点位无关），这就是「设了方向也看不出来」的根因。
   * 现在按放置时的相机朝向写一个 p + dir*DIR_RANGE 的目标点；朝向未知时给正北，
   * 只保证 Init 不炸，菜单/显示里照样标「未知」。 */
  if (yaw > YAW_NONE + 1.0f) {
    dir_of_yaw(yaw, &zd);
    zt.x = p.x + zd.x * DIR_RANGE;
    zt.y = p.y;
    zt.z = p.z + zd.z * DIR_RANGE;
  } else {
    zt.x = p.x; zt.y = p.y; zt.z = p.z - DIR_RANGE;   /* 正北兜底 */
  }
  za = vec3_arr_new(&zt, 1);
  if (!za) { elog("nanopos: zoomPos 分配失败"); return 0; }
  *(P*)((char*)comp + 0x10) = za;
  areaTr = get_tr(areaGo);
  tr = get_tr(go);
  if (areaTr && tr) ((set_parent_t)RVA(R_SET_PARENT))(tr, areaTr, 0, 0);
  if (tr) ((set_pos_t)RVA(R_SET_POS))(tr, p, 0);
  /* 到这里 zoomPos / entrancePos 都非空了，Init 只做 area= 和
   * zoomPos = (zoomPos + entrancePos)，不会再抛托管异常。 */
  ((pos_init_t)RVA(R_POS_INIT))(comp, areaComp, 0);
  ((set_active_t)RVA(R_SETACTIVE))(go, 1, 0);
  list = *(P*)((char*)areaComp + 0x10);
  live = (aid >= 0 && aid < MAX_AID) ? g_areaLive[aid] : 0;
  if (!live) {
    /* 第一个守卫点：现在才激活守卫区。Awake 的 GetComponentsInChildren 会把刚挂上的
     * 子点收进 posList，同时把自己登记进 SpareAreaList —— 一步到位且不会重复。 */
    ((set_active_t)RVA(R_SETACTIVE))(areaGo, 1, 0);
    if (aid < MAX_AID) g_areaLive[aid] = 1;
    /* 兜底 1：GetComponentsInChildren 没收到这个点（比如激活前子物体刚挂上、
     * 层级还没刷新）就自己挂一次，绝不让守卫区带着空 posList 注册进去。 */
    if (list_count(list) == 0)
      list_add_via(g_nposListAdd, list, comp, "nanopos: posList(Awake 没收到)");
    /* 兜底 2：Awake 没登记成功时补一次（已在列表里会判重） */
    area_register(areaComp);
    elog("area aid=%d 激活（第一个守卫点）posList=%d", aid, list_count(list));
  } else {
    /* Awake 只在激活那一刻数一遍子物体；之后新建的点得自己挂进 posList，
     * 否则 Bot 的 Bot_NanoGuardArea.GetPos() 永远看不到这个点。 */
    list_add_via(g_nposListAdd, list, comp, "nanopos: posList");
    if (list_count(list) == 0) area_register(areaComp);   /* 删空过的区补登记 */
  }
  if (!add_mk(2, p, aid, parent, safety, go, comp, spawn_vis(p, 0.32f, 2))) return 0;
  g_mk[g_n - 1].yaw = yaw;
  elog("nanopos: 朝向 %s（yaw=%.1f -> zoomPos z=%.1f）",
       (yaw > YAW_NONE + 1.0f) ? yaw_zh(yaw) : "未知", yaw, zt.z);
  elog("nanopos #%d at %.2f %.2f %.2f aid=%d safety=%d areaPosList=%d",
       g_n, p.x, p.y, p.z, aid, safety, list_count(*(P*)((char*)areaComp + 0x10)));
  overlay_refresh();
  return 1;
}

/* 准星落点落在哪个守卫区的 3 m 框里（BoxCollider 半宽 1.5 m，留 0.1 m 容差）。
 * 2026-11-26 用户报「加了守卫点为什么没变绿」：日志里点是 -41.6、区中心在 -55.5
 * （14 m 外）还照样挂过去 —— 因为「加守卫点」只认「当前区」（g_curArea = 最后新建
 * 的那个），站多远都往它里面塞。现在改成按落点归区：落在哪个 3 m 框里就挂哪个；
 * 一个都不在才新建区。返回 g_mk 下标，-1 = 不在任何区里。 */
static int area_at(const V3* p) {
  int i, best = -1;
  float bestd = 1e30f;
  for (i = 0; i < g_n; i++) {
    float dx, dy, dz, d;
    if (g_mk[i].type != MT_AREA) continue;
    dx = fabsf(p->x - g_mk[i].p.x);
    dy = fabsf(p->y - g_mk[i].p.y);
    dz = fabsf(p->z - g_mk[i].p.z);
    if (dx > 1.6f || dy > 1.6f || dz > 1.6f) continue;   /* 3 m 框外 */
    d = dx + dy + dz;
    if (d < bestd) { bestd = d; best = i; }               /* 落在两个区交界时取近的 */
  }
  return best;
}

/* delete marker at idx, its children, and fix every index reference */
static void del_index(int idx);
static int  save_file(void);
static int editor_spawn_delete(int team);   /* 出生点：准星最近的一个（定义在 load_file 后面） */
void editor_delete_nearest(void);          /* 定义在文件末尾；菜单里的 Delete 也走它 */
/* 删跳链时把点图日志里的 jump add 一起摘掉（定义在点图编辑区，那里才有 g_ned）。 */
static int nav_drop_jump(const V3* takeoff);

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

/* 跳链销毁前先把它从 Bot_JumpLink.linkDic 里摘掉。
 * GetLink（0x10B2F5E0）只查字典、不判 Unity 假空：TryGetValue 命中就直接返回 1，
 * 所以不摘的话人机会一直拿到这个已销毁的组件 —— 删除看着成功、跳链照用，
 * 重进图也还在（linkDic 是静态字段）。这里用游戏自己的 Dictionary.Remove 搬桶，
 * 不手写字典布局（2026-11-17 的闪退就是手写 List 摘除踩到写花槽位）。
 * 托管异常走 exc 返回，不往 std::terminate 上撞。 */
static void jump_unregister(P comp) {
  P f, dic = 0, startNode;
  void* args[1];
  P exc = 0;
  if (!comp || !g_jumpCls || !x_field_static_get_value) return;
  if (!uobj_live(comp) || !mem_ok(comp, 0x28)) return;
  startNode = *(P*)((char*)comp + 0x20);          /* Bot_JumpLink.startNode */
  f = x_class_get_field_from_name ? x_class_get_field_from_name(g_jumpCls, "linkDic") : 0;
  if (f) x_field_static_get_value(f, &dic);
  if (!dic || !mem_ok(dic, 0x24)) { elog("jump: linkDic 不可读，跳过反登记"); return; }
  if (!startNode) { elog("jump: startNode 还没解析（OnLatePostScan 没跑），跳过反登记"); return; }
  if (!g_linkDicRemove || !x_runtime_invoke) { elog("jump: Dictionary.Remove 没找到，跳过反登记"); return; }
  args[0] = startNode;
  x_runtime_invoke(g_linkDicRemove, dic, args, &exc);
  if (exc) { elog("jump: linkDic.Remove 抛异常（已吞掉）"); return; }
  elog("jump: 已从 linkDic 摘掉 startNode=%p", (void*)startNode);
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
  } else if (m->type == MT_JUMP) {
    jump_unregister(m->comp);
  }
}

/* drop_nav=0：调用者自己处理点图清单（撤销跳点用，见 mk_kill_jump）。
 * 其余路径一律 1：删跳链时必须把清单里的 jump add 一起摘掉。 */
static void del_index_ex(int idx, int drop_nav) {
  MK m;
  int i;
  if (idx < 0 || idx >= g_n) return;
  /* 子项先删，且从后往前：删子项不会移动父项下标。
   * 旧实现先取 &g_mk[idx] 再 kill_children()，数组一左移，指针就指向了别人的
   * 对象——删守卫区时真正销毁的是下一个标记。 */
  for (i = g_n - 1; i > idx; i--) {
    if (g_mk[i].parent == idx) del_index_ex(i, drop_nav);
  }
  m = g_mk[idx];
  marker_unregister(&m);
  if (m.vis) ((destroy_t)RVA(R_DESTROY))(m.vis, 0);
  if (m.go) ((destroy_t)RVA(R_DESTROY))(m.go, 0);
  if (m.type == 3) {
    if (m.aid >= 0 && m.aid < MAX_AID) {
      g_aidMk[m.aid] = 0;
      g_areaLive[m.aid] = 0;
      g_aidUsed[m.aid] = 0;
    }
    /* 不递减 g_areaCount：它是「已分配 aid 的上界」，递减会让下一个新建的守卫区
     * 拿到别的区还在用的 aid（g_aidMk 互相覆盖，后面加的守卫点就挂到错的区上）。
     * 删掉的槽位就空着，用到 MAX_AID 为止。 */
  }
  if (m.type == MT_JUMP && drop_nav) {
    /* 跳链是点图日志的 jump add 建出来的：不摘掉这条，重进图 nav_apply_jumps
     * 会再建一遍，用户看到的就是"删了又回来"。 */
    if (nav_drop_jump(&m.p)) elog("delete: jump add 已从点图日志摘掉");
    else elog("delete: 点图日志里没有对应 jump add（套包时建的？）");
  }
  /* 撤销记录：被删的标记记一笔（跳链把落点/参数一起记，撤销才能重建） */
  if (drop_nav)
    mke_note_del(&m, (m.type == MT_JUMP && g_lastJump.kind == JADD) ? &g_lastJump : 0);
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
static void del_index(int idx) { del_index_ex(idx, 1); }

static const char* mt_name(int t) {
  switch (t) {
    case MT_CROUCH:   return "蹲守点";
    case MT_NANOPOS:  return "守卫点";
    case MT_AREA:     return "守卫区";
    case MT_JUMP:     return "跳跃点/跳链";
    case MT_TAG:      return "标签/范围";
    case MT_SPAWN_BL: return "出生点 BL";
    case MT_SPAWN_GR: return "出生点 GR";
    case MT_SPAWN_NT: return "出生点 中立";
    case MT_ANY_POINT:return "任意点位";
    default:          return "任意标记";
  }
}
static int mt_count(int t) {
  int i, c = 0;
  for (i = 0; i < g_n; i++) if (g_mk[i].type == t) c++;
  return c;
}

/* 删准星最近的标记。want <= 0 = 任意类型；MT_* = 只在这个类型里挑。
 * 2026-11-25 用户要求：蹲守点 / 守卫点 / 守卫区 / 跳跃点 / 标签 分开删 ——
 * 守卫点就落在守卫区那个 3 m 框里，只按"最近"挑很容易删错对象。
 * 判定顺序不变：准星射线偏移 <=1 m -> 落点 12 m 内最近 -> 相机 12 m 内最近。 */
static int delete_nearest_of(int want) {
  V3 cp, fw, hp;
  int i, byRay = -1, byHit = -1, target = -1, cand = 0;
  float bestPerp = 1e9f, bestHit = 1e9f, bestCam = 1e9f;
  int haveHit, byCam = -1;
  const char* wn;
  ed_step();                  /* 一次删除 = 一步撤销（守卫区连带它下面的点位算同一组） */
  /* 出生点不在 g_mk 里，单独走数组编辑；其它类型仍走场景标记。 */
  if (want == MT_SPAWN_BL) return editor_spawn_delete(0);
  if (want == MT_SPAWN_GR) return editor_spawn_delete(1);
  if (want == MT_SPAWN_NT) return editor_spawn_delete(2);
  wn = (want == MT_ANY_POINT) ? "任意点位" : (want > 0 ? mt_name(want) : "任意");
  if (!g_n) { elog("delete: no markers"); toast_bad("图里还没有任何标记可删"); return 0; }
  if (!cam_ray(&cp, &fw)) { elog("delete: no camera"); toast_bad("取不到相机，删不了"); return 0; }
  haveHit = cam_point(&hp);
  for (i = 0; i < g_n; i++) {
    float vx, vy, vz, t;
    /* 删除点位页的"任意"不碰守卫区（区域在单独一页删）。 */
    if (want == MT_ANY_POINT) { if (g_mk[i].type == MT_AREA) continue; }
    else if (want > 0 && g_mk[i].type != want) continue;
    cand++;
    vx = g_mk[i].p.x - cp.x; vy = g_mk[i].p.y - cp.y; vz = g_mk[i].p.z - cp.z;
    t = vx * fw.x + vy * fw.y + vz * fw.z;
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
  if (!cand) {
    elog("delete: 这张图没有%s标记（共 %d 个标记）", wn, g_n);
    toast_bad("图里没有%s", wn);
    return 0;
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
    elog("delete: nothing chosen (want=%s, markers=%d, ray %.2f m, aim %.2f m, cam %.2f m) - aim at a marker",
         wn, g_n,
         byRay >= 0 ? bestPerp : -1.0f,
         haveHit ? sqrt(bestHit) : -1.0f,
         byCam >= 0 ? sqrt(bestCam) : -1.0f);
    toast_bad("没选中%s：准星对准它再按 5", wn);
    return 0;
  }
  if (target >= 0) {
    /* 先记下来：del_index 会让数组左移，删完就取不到名字/坐标了 */
    const char* dname = mt_name(g_mk[target].type);
    V3 dp = g_mk[target].p;
    elog("delete: removing #%d type=%d(%s) at %.2f %.2f %.2f", target, g_mk[target].type,
         dname, dp.x, dp.y, dp.z);
    del_index(target);
    /* 2026-11-25：不再立刻落盘。删掉的点只从当前场景 / 内存清单里消失，
     * Ctrl+S 之后才写 markers.txt；不保存就退房间 = 删了也白删（用户要求）。 */
    editor_dirty_mk();
    elog("delete: 未保存（Ctrl+S 保存，退房间前不存会恢复）");
    toast_ok("已删%s (%.1f %.1f %.1f)：可撤销", dname, dp.x, dp.y, dp.z);
    overlay_refresh();
    return 1;
  }
  return 0;
}
static int delete_nearest(void) { return delete_nearest_of(0); }

static void make_tag(V3 p, int tag, float radius);

/* 编辑标记（蹲守点 / 守卫点 / 守卫区 / tag）按**地图**分文件夹存（2026-11-24 用户要求）：
 *   <插件目录>\markers\<包名>\markers.txt
 *   例：markers\01_TransportShip运输船\markers.txt
 * 以前是一个 markers\markers.txt 全图共用 —— 换一张图，别的图的蹲守点也会被加载进来
 * （现场就见过 y=+27 的悬空蹲守点，人机选中后原地"到达"不动）。包名 = 中英文地图名。 */
static void mk_set_path(void) {
  char base[MAX_PATH], dir[MAX_PATH], cfg[MAX_PATH];
  /* 成品档没有 UCF_PACK，图名来自“按指纹搜到的那个文件夹”（g_mapDirName） */
  const char* name = g_mapDirName[0] ? g_mapDirName
                   : (g_packName[0] ? g_packName : "_未分类");
  base[0] = 0;
  /* 根目录优先级：UCF_MARKERS_DIR（控制台注入 = 工程端 data\navdata\dev\markers）
   *              > ucf_mod.json 的 markers_dir > <插件目录>\markers（兜底） */
  if (GetEnvironmentVariableA("UCF_MARKERS_DIR", base, sizeof base) <= 0 || !base[0]) {
    cfg[0] = 0;
    cfg_str("markers_dir", "", cfg, sizeof cfg);
    if (cfg[0]) snprintf(base, sizeof base, "%s", cfg);
    else snprintf(base, sizeof base, "%s\\markers", g_dir);
  }
  ucf_mkdir_p(base);
  snprintf(dir, sizeof dir, "%s\\%s", base, name);
  ucf_mkdir_p(dir);
  snprintf(g_file, sizeof g_file, "%s\\markers.txt", dir);
}

static int save_file(void) {
  FILE* f;
  int i, t, c1 = 0, c2 = 0, c3 = 0, c5 = 0, sa = 0, sd = 0;
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
  for (t = 0; t < SPAWN_TEAMS; t++) { sa += g_spawnAddN[t]; sd += g_spawnDelN[t]; }
  fprintf(f, "# ucf_mod markers v1  crouch=%d nanopos=%d area=%d tag=%d spawnadd=%d spawndel=%d\n",
          c1, c2, c3, c5, sa, sd);
  fprintf(f, "# crouch <team> <x> <y> <z> [yaw]        yaw = 朝向(度,0=北,90=东)，未知则省略\n");
  fprintf(f, "# area <scale*10> <x> <y> <z> [aid]\n");
  fprintf(f, "# nanopos <areaId> <x> <y> <z> <safety> [yaw]   同上\n");
  fprintf(f, "# tag <tag> <x> <y> <z>\n");
  fprintf(f, "# spawn <team 0BL/1GR/2中立> <x> <y> <z> <yaw>   / spawndel <team> <x> <y> <z>\n");
  for (i = 0; i < g_n; i++) {
    MK* m = &g_mk[i];
    if (m->type == 1) {
      /* 第 5 列 = 朝向（度，0=北）。未知就不写，保持老格式（旧版插件照样能读） */
      if (m->yaw > YAW_NONE + 1.0f)
        fprintf(f, "crouch %d %.3f %.3f %.3f %.1f\n", m->prm, m->p.x, m->p.y, m->p.z, m->yaw);
      else
        fprintf(f, "crouch %d %.3f %.3f %.3f\n", m->prm, m->p.x, m->p.y, m->p.z);
    }
    /* 2026-11-25：area 行补上 aid。以前靠「建的顺序」推 aid，删过区再进图，
     * nanopos 的 areaId 就对不上了（点位静默丢失）。旧文件只有 4 列，照样能读。 */
    else if (m->type == 3) fprintf(f, "area %d %.3f %.3f %.3f %d\n", m->prm, m->p.x, m->p.y, m->p.z, m->aid);
    else if (m->type == 2) {
      if (m->yaw > YAW_NONE + 1.0f)
        fprintf(f, "nanopos %d %.3f %.3f %.3f %d %.1f\n", m->aid, m->p.x, m->p.y, m->p.z, m->prm, m->yaw);
      else
        fprintf(f, "nanopos %d %.3f %.3f %.3f %d\n", m->aid, m->p.x, m->p.y, m->p.z, m->prm);
    }
    else if (m->type == 5) fprintf(f, "tag %d %.3f %.3f %.3f\n", m->prm, m->p.x, m->p.y, m->p.z);
  }
  for (t = 0; t < SPAWN_TEAMS; t++) {
    for (i = 0; i < g_spawnAddN[t]; i++)
      fprintf(f, "spawn %d %.3f %.3f %.3f %.1f\n", t,
              g_spawnAdd[t][i].p.x, g_spawnAdd[t][i].p.y, g_spawnAdd[t][i].p.z,
              g_spawnAdd[t][i].yaw);
    for (i = 0; i < g_spawnDelN[t]; i++)
      fprintf(f, "spawndel %d %.3f %.3f %.3f\n", t,
              g_spawnDel[t][i].p.x, g_spawnDel[t][i].p.y, g_spawnDel[t][i].p.z);
  }
  fclose(f);
  elog("saved %d markers (crouch=%d nanopos=%d area=%d tag=%d spawnadd=%d spawndel=%d) -> %s",
       g_n, c1, c2, c3, c5, sa, sd, g_file);
  overlay_refresh();
  return 1;
}

static void reset_markers(void) {
  g_n = 0;
  g_areaCount = 0;
  g_curArea = -1;
  memset(g_aidMk, 0, sizeof(g_aidMk));
  memset(g_areaLive, 0, sizeof(g_areaLive));   /* 换图：旧守卫区随场景销毁，激活标记一起清 */
  memset(g_aidUsed, 0, sizeof(g_aidUsed));
  /* 出生点：换图后 MapManager 是新的，原生快照/写回指针全部作废，等下次进图重拍。
   * 新增/删除清单来自 markers.txt，由 load_file() 重新读进来。 */
  memset(g_spawnOrigN, 0, sizeof(g_spawnOrigN));
  memset(g_spawnOrigOk, 0, sizeof(g_spawnOrigOk));
  memset(g_spawnAddN, 0, sizeof(g_spawnAddN));
  memset(g_spawnDelN, 0, sizeof(g_spawnDelN));
  memset(g_spawnWritten, 0, sizeof(g_spawnWritten));
  memset(g_spawnCaptured, 0, sizeof(g_spawnCaptured));
  g_spawnGap = 0.0f;
  g_spawnGapOk = 0;
  g_spawnHeightsFixed = 0;
}

/* markers.txt 里只跟出生点有关的两行（load_file 和「开局抢跑」共用一份解析）：
 *   spawn <team> <x> <y> <z> <yaw>   /   spawndel <team> <x> <y> <z>
 * 返回 1 = 这行是出生点（已经记进 g_spawnAdd / g_spawnDel）。 */
static int spawn_parse_line(const char* line) {
  float x, y, z, yaw = 0.0f;
  int a;
  if (!line) return 0;
  if (sscanf(line, "spawndel %d %f %f %f", &a, &x, &y, &z) == 4) {
    if (a >= 0 && a < SPAWN_TEAMS && g_spawnDelN[a] < MAX_SPAWN_EDIT) {
      SPT* s = &g_spawnDel[a][g_spawnDelN[a]++];
      memset(s, 0, sizeof *s);
      s->p.x = x; s->p.y = y; s->p.z = z;
    }
    return 1;
  }
  if (sscanf(line, "spawn %d %f %f %f %f", &a, &x, &y, &z, &yaw) == 5) {
    if (a >= 0 && a < SPAWN_TEAMS && g_spawnAddN[a] < MAX_SPAWN_EDIT) {
      SPT* s = &g_spawnAdd[a][g_spawnAddN[a]++];
      s->p.x = x; s->p.y = y; s->p.z = z; s->yaw = yaw;
    }
    return 1;
  }
  return 0;
}

static int load_file(void) {
  FILE* f;
  char line[256];
  int made = 0;
  if (!g_file[0]) return 0;
  f = fopen(g_file, "r");
  if (!f) { elog("load: no markers file yet (%s)", g_file); return 0; }
  while (fgets(line, sizeof(line), f)) {
    float x, y, z, yaw = YAW_NONE;      /* yaw：crouch / nanopos 的可选朝向列 */
    int a, b;
    if (line[0] == '#' || line[0] == '\n' || line[0] == '\r') continue;
    if (spawn_parse_line(line)) continue;   /* spawn / spawndel */
    if (sscanf(line, "area %d %f %f %f %d", &a, &x, &y, &z, &b) == 5) {
      V3 p; p.x = x; p.y = y; p.z = z;
      if (make_area_aid(a, p, b)) made++;
    } else if (sscanf(line, "area %d %f %f %f", &a, &x, &y, &z) == 4) {
      V3 p; p.x = x; p.y = y; p.z = z;          /* 旧文件：没有 aid 列，按顺序分配 */
      if (make_area(a, p)) made++;
    } else if (sscanf(line, "nanopos %d %f %f %f %d %f", &a, &x, &y, &z, &b, &yaw) >= 5) {
      /* 老文件只有 5 列（没有 yaw）：sscanf 返回 5，yaw 保持 YAW_NONE = 未知 */
      V3 p; p.x = x; p.y = y; p.z = z;
      if (make_nanopos(a, p, b, yaw)) made++;
    } else if (sscanf(line, "crouch %d %f %f %f %f", &a, &x, &y, &z, &yaw) >= 4) {
      V3 p; p.x = x; p.y = y; p.z = z;
      /* 文件里的队伍列要生效：make_crouch 用的是 g_team，临时切过去再还原 */
      int savedTeam = g_team;
      g_team = a ? 1 : 0;
      if (make_crouch(p, yaw)) made++;
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


/* ================= 出生点编辑：MapManager.SP_BL / SP_GR / SP_Netural =================
 * 数据来源：0x10 = SP_BL（team 0 幽灵/潜伏者）、0x14 = SP_GR（team 1 保卫者）、
 * 0x18 = SP_Netural（team 2 中立；个人竞技里 gameMode=DeathMatch，AddPlayer 会把全员
 * 设成 Neutral，重生只读这个数组 —— 只改 BL/GR 时个人竞技"加了点也没人出生"）；
 * 数组头和 IL2CPP 数组一样：长度 +0xC，元素 +0x10 起、每个 16 B。
 * 原生点只在进图时拍一次快照（g_spawnOrig），之后所有改动都在
 * 「新增（优先）- 原生去删除」上重算；不碰场景里的 pointDic，也不写原图。
 *
 * 2026-11-27 反编译核实（GameAssembly RVA）：
 *   Player.Spawn（0xB53760，内联了 <Spawn>g__MoveToRespawnPos）每次重生都
 *   call MapManager.GetSpawnPoint(team)（0xAEB6E0），人机也是走这条路
 *   （Mode_TeamDeath/Mode_DeathMatch.DeathEvent -> Player.Respawn -> 协程 -> Player.Spawn）。
 *   取点用静态计数器 SPID_*：MapManager.NewGameRoundStart 每回合把它设成
 *   Random.Range(0, len)，之后顺序轮转。所以新增点必须排在数组前面，
 *   否则要轮完一遍原生点才轮到它，看起来就是"加了没用"。 */

static P mm_inst(void) {
  P mm = 0;
  if (g_mmInstField && x_field_static_get_value) x_field_static_get_value(g_mmInstField, &mm);
  if (mm && !uobj_live(mm)) mm = 0;
  return mm;
}

/* 从 p 上方 up 米往下打一条射线取脚下地面（返回碰撞点 y）。层掩码 1 和
 * cam_point_ray / 贴地用的同一条（地图地面在 Default 层）。 */
static int ground_below(V3 p, float up, float maxd, V3* out) {
  V3 o, d;
  char hit[128];
  raycast_t rc = (raycast_t)RVA(R_RAYCAST);
  o.x = p.x; o.y = p.y + up; o.z = p.z;
  d.x = 0.0f; d.y = -1.0f; d.z = 0.0f;
  if (!rc(o, d, hit, maxd, 1, 0)) return 0;
  if (out) *out = *(V3*)hit;
  return 1;
}

/* 本图"原生出生点比地面高多少"：拿原生点逐个往下打射线，取平均。
 * 只采样"明显站在地面上"的点（-0.5 ~ 3 m），量不到就退回 0.05 m（老行为）。 */
static float spawn_height_gap(void) {
  int team, i, n = 0;
  float sum = 0.0f;
  if (g_spawnGapOk) return g_spawnGap;
  for (team = 0; team < SPAWN_TEAMS && n < 12; team++) {
    for (i = 0; i < g_spawnOrigN[team] && n < 12; i++) {
      V3 s = g_spawnOrig[team][i].p, g;
      float d;
      if (!ground_below(s, 1.5f, 40.0f, &g)) continue;
      d = s.y - g.y;
      if (d < -0.5f || d > 3.0f) continue;
      sum += d; n++;
    }
  }
  g_spawnGap = (n > 0) ? (sum / (float)n) : 0.05f;
  if (!(g_spawnGap > 0.02f && g_spawnGap < 3.0f)) g_spawnGap = 0.05f;
  g_spawnGapOk = (n > 0) ? 1 : 0;
  if (n > 0)
    elog("spawn: 高度基准 = 脚下地面 + %.2f m（按 %d 个原生出生点测得）", g_spawnGap, n);
  return g_spawnGap;
}

/* 把新增点抬到和游戏原生点一样高：地面 + gap。底下是空的（平台外/虚空）就不动，
 * 免得把一个本来就该悬空/在别处的点拽到看不见的地方。 */
static void spawn_fix_height(V3* p) {
  V3 g;
  float want, gap;
  if (!p) return;
  if (!ground_below(*p, 1.0f, 40.0f, &g)) return;
  gap = spawn_height_gap();
  want = g.y + gap;
  if (fabsf(p->y - want) < 0.02f) { p->y = want; return; }
  elog("spawn: 高度对齐 y %.2f → %.2f（地面 %.2f + 原生高度 %.2f）",
       p->y, want, g.y, gap);
  p->y = want;
}

/* 原生点抓到之后跑一次：把 markers 里读进来的历史新增点（旧版本存的低高度）一起对齐。 */
static void spawn_fix_heights_all(void) {
  int team, i, k = 0;
  for (team = 0; team < SPAWN_TEAMS; team++)
    for (i = 0; i < g_spawnAddN[team]; i++) {
      float y0 = g_spawnAdd[team][i].p.y;
      spawn_fix_height(&g_spawnAdd[team][i].p);
      if (g_spawnAdd[team][i].p.y != y0) k++;
    }
  if (k) elog("spawn: 已把 %d 个新增出生点的高度对齐到原生高度（Ctrl+S 后落盘）", k);
}

static void spawn_capture(int team, P arr) {
  int n = 0;
  if (arr && mem_ok(arr, 0x10)) {
    n = *(int*)((char*)arr + 0xC);
    if (n < 0) n = 0;
    if (n > MAX_SPAWN_ORIG) {
      elog("spawn: 原生 team=%d 有 %d 个，超过上限 %d，只取前 %d 个",
           team, n, MAX_SPAWN_ORIG, MAX_SPAWN_ORIG);
      n = MAX_SPAWN_ORIG;
    }
    if (n && !mem_ok((char*)arr + 0x10, (size_t)n * 16)) {
      elog("spawn: 原生 team=%d 数据不可读，按 0 个处理", team);
      n = 0;
    }
    if (n) memcpy(g_spawnOrig[team], (char*)arr + 0x10, (size_t)n * 16);
  }
  g_spawnOrigN[team] = n;
  g_spawnOrigOk[team] = 1;
  g_spawnCaptured[team] = arr;
  elog("spawn: 原生快照 team=%d n=%d", team, n);
}

/* 新增点排前面 + 原生（去掉删掉的）按原顺序接在后面；addIdx 回填新增点在
 * g_spawnAdd 里的下标（-1 = 原生点），删除时据此决定摘哪一边。
 * 为什么新增优先：游戏的 SPID_* 每回合随机起头再顺序轮转，新增点排在末尾时要
 * 轮到它得先走完一串原生点，玩家看到的就是"出生点没用"。 */
static int spawn_effective(int team, SPT* out, int* addIdx, int cap) {
  unsigned char drop[MAX_SPAWN_ORIG];
  int i, j, n = 0;
  memset(drop, 0, sizeof drop);
  for (i = 0; i < g_spawnDelN[team]; i++) {
    for (j = 0; j < g_spawnOrigN[team]; j++) {
      if (drop[j]) continue;
      if (fabsf(g_spawnOrig[team][j].p.x - g_spawnDel[team][i].p.x) < 0.02f &&
          fabsf(g_spawnOrig[team][j].p.y - g_spawnDel[team][i].p.y) < 0.02f &&
          fabsf(g_spawnOrig[team][j].p.z - g_spawnDel[team][i].p.z) < 0.02f) {
        drop[j] = 1;
        break;
      }
    }
  }
  for (i = 0; i < g_spawnAddN[team] && n < cap; i++) {
    out[n] = g_spawnAdd[team][i];
    if (addIdx) addIdx[n] = i;
    n++;
  }
  for (j = 0; j < g_spawnOrigN[team] && n < cap; j++) {
    if (drop[j]) continue;
    out[n] = g_spawnOrig[team][j];
    if (addIdx) addIdx[n] = -1;
    n++;
  }
  return n;
}

static int spawn_count(int team) {
  unsigned char drop[MAX_SPAWN_ORIG];
  int i, j, n = 0;
  if (team < 0 || team >= SPAWN_TEAMS || !g_spawnOrigOk[team]) return -1;
  memset(drop, 0, sizeof drop);
  for (i = 0; i < g_spawnDelN[team]; i++)
    for (j = 0; j < g_spawnOrigN[team]; j++)
      if (!drop[j] &&
          fabsf(g_spawnOrig[team][j].p.x - g_spawnDel[team][i].p.x) < 0.02f &&
          fabsf(g_spawnOrig[team][j].p.y - g_spawnDel[team][i].p.y) < 0.02f &&
          fabsf(g_spawnOrig[team][j].p.z - g_spawnDel[team][i].p.z) < 0.02f) {
        drop[j] = 1;
        break;
      }
  for (j = 0; j < g_spawnOrigN[team]; j++) if (!drop[j]) n++;
  return n + g_spawnAddN[team];
}

static int spawn_arr_same(P arr, const SPT* pts, int n) {
  int i;
  if (!arr || !mem_ok(arr, 0x10)) return n == 0;
  if (*(int*)((char*)arr + 0xC) != n) return 0;
  if (n <= 0) return 1;
  if (!mem_ok((char*)arr + 0x10, (size_t)n * 16)) return 0;
  for (i = 0; i < n; i++)
    if (memcmp((char*)arr + 0x10 + i * 16, &pts[i], 16) != 0) return 0;
  return 1;
}

/* 三个取点计数器一起清零：数组长度可能变短，SPID 越界会让 GetSpawnPoint 抛异常；
 * 长度变长时清零也正好让"下一次取点"从第 1 个（= 新增点）开始。 */
static void spawn_clear_ids(void) {
  int t, zero = 0;
  if (!x_field_static_set_value) return;
  for (t = 0; t < SPAWN_TEAMS; t++)
    if (g_spidFld[t]) x_field_static_set_value(g_spidFld[t], &zero);
}

static int spawn_write(int team, P mm, const SPT* pts, int n) {
  P na;
  unsigned h = 0;
  int off = SPAWN_OFF[team];
  if (!g_spawnCls || !x_array_new || !mm) return 0;
  if (n <= 0) return 0;
  if (sizeof(SPT) != 16) {
    elog("spawn: SPT 大小 %d != 16，禁用以防写花托管堆", (int)sizeof(SPT));
    return 0;
  }
  na = x_array_new(g_spawnCls, (unsigned)n);
  if (!na) { elog("spawn: array_new(%d) 失败", n); return 0; }
  if (*(int*)((char*)na + 0xC) != n) {
    elog("spawn: 新数组长度 %d != %d，放弃写入", *(int*)((char*)na + 0xC), n);
    return 0;
  }
  /* 最硬的防线：数组字节长度必须正好 n*16。元素类拿错时这里会拦住，
   * 不会把 memcpy 写到托管堆外面。 */
  if (x_array_get_byte_length && x_array_get_byte_length(na) != n * 16) {
    elog("spawn: 数组字节长度 %d != %d（元素不是 16 B），放弃写入",
         x_array_get_byte_length(na), n * 16);
    return 0;
  }
  /* 填数据期间先拿句柄钉住：这段是原生代码，GC 不知道 na 是活的。
   * （plugin.c 注入数组时也是同一套做法。） */
  if (x_gchandle_new) h = x_gchandle_new(na, 0);
  memcpy((char*)na + 0x10, pts, (size_t)n * 16);
  /* 和 navfix / plugin.c 同一套写法：先写屏障再显式写字段。 */
  if (x_gc_wbarrier_set_field) x_gc_wbarrier_set_field(mm, (char*)mm + off, na);
  *(P*)((char*)mm + off) = na;
  if (h && x_gchandle_free) x_gchandle_free((P)(size_t)h);
  /* 数组长度变了：SPID_* 可能已经超过新长度（取点函数会越界检查），
   * 每写一次就清零 —— 新增点现在排在最前面，清零 = 下一次重生就用第 1 个新增点。
   * 还原原生数组（spawn_restore_orig）也走这里，同样安全。 */
  spawn_clear_ids();
  g_spawnWritten[team] = na;
  return 1;
}

static int spawn_apply(void) {
  SPT fin[MAX_SPAWN_ORIG + MAX_SPAWN_EDIT];
  P mm;
  int team, ok = 1, edits = 0;
  for (team = 0; team < SPAWN_TEAMS; team++)
    if (g_spawnAddN[team] || g_spawnDelN[team]) edits = 1;
  if (!edits) return 1;
  mm = mm_inst();
  if (!mm) return 0;
  for (team = 0; team < SPAWN_TEAMS; team++) {
    P cur;
    int n;
    if (!g_spawnAddN[team] && !g_spawnDelN[team]) continue;
    cur = *(P*)((char*)mm + SPAWN_OFF[team]);
    /* 指针既不是我们写回去的那份、也不是拍快照时那份 = 游戏重建了数组
     * （最典型：进图时我们先写、MapManager.Awake 后跑）。重新拍快照。 */
    if (!g_spawnOrigOk[team] ||
        (cur != g_spawnWritten[team] && cur != g_spawnCaptured[team])) {
      spawn_capture(team, cur);
      g_spawnWritten[team] = 0;
    }
    if (!g_spawnHeightsFixed && g_spawnOrigOk[team]) {
      spawn_fix_heights_all();      /* 旧值（+0.05）在这里一次性改正 */
      g_spawnHeightsFixed = 1;
    }
    n = spawn_effective(team, fin, 0, (int)(sizeof fin / sizeof fin[0]));
    if (n <= 0) {
      /* 原生还没读到（进图瞬间）时安静等着；真把点删空了才值得报一行。 */
      if (g_spawnOrigN[team] > 0)
        elog("spawn: team=%s 结果为空，保留原生 %d 个（空数组会让游戏越界）",
             SPAWN_NAME[team], g_spawnOrigN[team]);
      continue;
    }
    if (spawn_arr_same(cur, fin, n)) { g_spawnWritten[team] = cur; continue; }
    if (!spawn_write(team, mm, fin, n)) { ok = 0; continue; }
    elog("spawn: team=%s 写回 新增 %d + 原生 %d - 删除 %d = %d 个；"
         "顺序[0]=%0.2f %0.2f %0.2f，SPID 清零（下一次取点 = 第 1 个）",
         SPAWN_NAME[team], g_spawnAddN[team], g_spawnOrigN[team], g_spawnDelN[team], n,
         fin[0].p.x, fin[0].p.y, fin[0].p.z);
  }
  return ok;
}

/* 每 tick 保活：没编辑时也拍一次原生快照（删除页要显示计数/找目标）；
 * 有编辑时核对数组，被游戏重建就自动重套。场景切换后等几帧再碰 MapManager。 */
static void spawn_tick(void) {
  P mm;
  int team, edits = 0;
  /* 2026-11-27：进图第 1 个心跳就套（以前等 4 拍 ≈1 s）—— 死亡重生 2 s 后才取点，
   * 但开局那一轮可能在等待窗口里就 spawn 完了，越早套上越不会"第一轮没生效"。 */
  if (!g_inited || g_sceneAge < 1) return;
  mm = mm_inst();
  if (!mm) return;
  for (team = 0; team < SPAWN_TEAMS; team++) {
    P cur = *(P*)((char*)mm + SPAWN_OFF[team]);
    if (!g_spawnOrigOk[team] && cur) spawn_capture(team, cur);
    if (g_spawnAddN[team] || g_spawnDelN[team]) edits = 1;
  }
  if (edits) spawn_apply();
}

static float cam_yaw(void) {
  V3 cp, fw;
  if (!cam_ray(&cp, &fw)) return 0.0f;
  return atan2f(fw.x, fw.z) * 57.29578f;
}

/* 相机朝向，按「方向」那套约定给（0=北 90=东，和屏幕罗盘 / 朝向工具页同一个数）。
 * 出生点仍然用 cam_yaw（游戏里 SpawnPoint.yaw 是另一套：atan2(x,z)，0=+Z），别混用。 */
static float cam_dir_yaw(void) {
  V3 cp, fw;
  if (!cam_ray(&cp, &fw)) return YAW_NONE;
  return yaw_of_dir(&fw);
}

static int spawn_add_point(int team, V3 p, float yaw) {
  int n;
  if (team < 0 || team >= SPAWN_TEAMS) return 0;
  if (!g_spawnCls) { elog("spawn: SpawnPoint 类没找到，不能加出生点"); return 0; }
  if (g_spawnAddN[team] >= MAX_SPAWN_EDIT) {
    elog("spawn: team=%d 新增到上限 %d", team, MAX_SPAWN_EDIT);
    return 0;
  }
  n = spawn_count(team);
  if (n >= MAX_SPAWN_ORIG + MAX_SPAWN_EDIT - 1) {
    elog("spawn: team=%d 总数到上限 %d", team, MAX_SPAWN_ORIG + MAX_SPAWN_EDIT);
    return 0;
  }
  spawn_fix_height(&p);          /* 和游戏原生出生点同高（地面 + gap） */
  g_spawnAdd[team][g_spawnAddN[team]].p = p;
  g_spawnAdd[team][g_spawnAddN[team]].yaw = yaw;
  g_spawnAddN[team]++;
  mke_note_spawn_add(team, &g_spawnAdd[team][g_spawnAddN[team] - 1], g_spawnAddN[team] - 1);
  if (!spawn_apply()) elog("spawn: MapManager 还没就绪，进图后自动重试");
  /* 新增点已经排到数组第 1 个：计数器再清一次，保证"下一次重生"就落到这个点上，
   * 不用等游戏把原生点轮一遍（用户按完 5 抬头就能看到人机从这里出生）。 */
  spawn_clear_ids();
  editor_dirty_mk();          /* 手动保存：Ctrl+S 才写 markers.txt */
  g_visDirty = 1;
  elog("spawn: 新增 %s (%0.2f %0.2f %0.2f) yaw=%.0f（地面 + 原生高度 %.2f），本图 %s 新增 %d 个（未保存，Ctrl+S）",
       SPAWN_NAME[team], p.x, p.y, p.z, yaw, g_spawnGap, SPAWN_NAME[team], g_spawnAddN[team]);
  return 1;
}

/* 准星最近的一个出生点：和 delete_nearest_of 同一套判定
 * （射线偏移 <=1 m -> 落点 12 m 内 -> 相机 12 m 内）。
 * 命中原生点记 spawndel；命中自己新增的点直接摘新增清单。 */
static int editor_spawn_delete(int team) {
  SPT eff[MAX_SPAWN_ORIG + MAX_SPAWN_EDIT];
  int addIdx[MAX_SPAWN_ORIG + MAX_SPAWN_EDIT];
  int n, i, target = -1, byRay = -1, byHit = -1, byCam = -1;
  float bestPerp = 1e9f, bestHit = 1e9f, bestCam = 1e9f;
  V3 cp, fw, hp;
  int haveHit;
  if (team < 0 || team >= SPAWN_TEAMS) return 0;
  if (!g_spawnOrigOk[team]) {
    /* 菜单刚打开 / 进图不到 1 s：现场补拍一次，别让"删除"第一下落空。 */
    P mm = mm_inst();
    if (mm) {
      P cur = *(P*)((char*)mm + SPAWN_OFF[team]);
      if (cur) spawn_capture(team, cur);
    }
  }
  if (!g_spawnOrigOk[team] && !g_spawnAddN[team]) {
    elog("spawn: team=%s 的数组还没读到（进图后再试）", SPAWN_NAME[team]);
    toast_bad("出生点还没读到，进图后再试");
    return 0;
  }
  n = spawn_effective(team, eff, addIdx, (int)(sizeof eff / sizeof eff[0]));
  if (n <= 0) { elog("spawn: team=%s 没有出生点可删", SPAWN_NAME[team]); toast_bad("这个阵营没有出生点可删"); return 0; }
  if (n <= 1) {
    elog("spawn: team=%s 只剩 1 个出生点，不能再删（空数组会让游戏越界）", SPAWN_NAME[team]);
    toast_bad("只剩 1 个出生点了：再删游戏会崩，不允许");
    return 0;
  }
  if (!cam_ray(&cp, &fw)) { elog("spawn: no camera"); toast_bad("取不到相机，删不了"); return 0; }
  haveHit = cam_point(&hp);
  for (i = 0; i < n; i++) {
    float vx = eff[i].p.x - cp.x, vy = eff[i].p.y - cp.y, vz = eff[i].p.z - cp.z;
    float t = vx * fw.x + vy * fw.y + vz * fw.z;
    if (t > 0.3f && t < 60.0f) {
      float px = vx - fw.x * t, py = vy - fw.y * t, pz = vz - fw.z * t;
      float perp = sqrtf(px * px + py * py + pz * pz);
      if (perp < bestPerp) { bestPerp = perp; byRay = i; }
    }
    if (haveHit) {
      float dx = eff[i].p.x - hp.x, dy = eff[i].p.y - hp.y, dz = eff[i].p.z - hp.z;
      float d2 = dx * dx + dy * dy + dz * dz;
      if (d2 < bestHit) { bestHit = d2; byHit = i; }
    }
    {
      float d2 = vx * vx + vy * vy + vz * vz;
      if (d2 < bestCam) { bestCam = d2; byCam = i; }
    }
  }
  if (byRay >= 0 && bestPerp <= 1.0f) target = byRay;
  else if (byHit >= 0 && bestHit <= 144.0f) target = byHit;
  else if (byCam >= 0 && bestCam <= 144.0f) target = byCam;
  if (target < 0) {
    elog("spawn: team=%s 没选中（%d 个点，射线偏移 %.2f m）—— 准星对准出生点再按 5",
         SPAWN_NAME[team], n, byRay >= 0 ? bestPerp : -1.0f);
    toast_bad("没选中出生点：准星对准它再按 5");
    return 0;
  }
  if (addIdx[target] >= 0) {
    int k = addIdx[target];
    elog("spawn: 删除新增 team=%s idx=%d (%.2f %.2f %.2f)", SPAWN_NAME[team], k,
         eff[target].p.x, eff[target].p.y, eff[target].p.z);
    mke_note_spawn_del(team, &eff[target], 1, k);
    for (i = k; i < g_spawnAddN[team] - 1; i++) g_spawnAdd[team][i] = g_spawnAdd[team][i + 1];
    g_spawnAddN[team]--;
  } else {
    if (g_spawnDelN[team] >= MAX_SPAWN_EDIT) {
      elog("spawn: team=%s 删除记录到上限 %d", SPAWN_NAME[team], MAX_SPAWN_EDIT);
      toast_bad("出生点删除记录到上限（%d）", MAX_SPAWN_EDIT);
      return 0;
    }
    elog("spawn: 删除原生 team=%s (%.2f %.2f %.2f)", SPAWN_NAME[team],
         eff[target].p.x, eff[target].p.y, eff[target].p.z);
    mke_note_spawn_del(team, &eff[target], 0, -1);
    g_spawnDel[team][g_spawnDelN[team]] = eff[target];
    g_spawnDel[team][g_spawnDelN[team]].yaw = 0.0f;
    g_spawnDelN[team]++;
  }
  if (!spawn_apply()) elog("spawn: MapManager 还没就绪，进图后自动重试");
  editor_dirty_mk();          /* 手动保存：Ctrl+S 才写 markers.txt */
  g_visDirty = 1;
  elog("spawn: 删除已生效，未保存（Ctrl+S 保存，退房间前不存会恢复）");
  toast_ok("已删出生点 %s (%.1f %.1f %.1f)：可撤销", SPAWN_NAME[team],
           eff[target].p.x, eff[target].p.y, eff[target].p.z);
  overlay_refresh();
  return 1;
}

/* ---- 开局抢跑（2026-11-27）---------------------------------------------
 * 现象：进房间第一波人机**先**在原生点出生（连删掉的原生点也照样被用），
 *       打死之后才在改过的点上复活。
 * 原因：出生点数组以前只在 editor_on_scene 里套 —— 那是 navfix 的"场景通知"，
 *       要等 PointGraph 扫完（换图后常要 1~3 s），而人机第一次出生早就过去了。
 * 做法：不等场景通知。主线程高频 tick（hi-res WM_TIMER ≈15 ms，兜底 4 Hz）里盯着
 *       MapManager 实例：一换实例（= 新的一局 / 换图）且 SP_* 已经拆出来（Awake 跑过），
 *       立刻只从 markers 里读 spawn / spawndel 两行并写回数组。
 *       其他标记（蹲守/守卫区/标签）仍等 editor_on_scene，那些要等组件就绪。 */
static P g_spawnEarlyMm;      /* 已经抢跑过的 MapManager 实例（只比指针，不解引用） */

static int spawn_early_load(void) {
  FILE* f;
  char line[256];
  if (!g_file[0]) return 0;
  memset(g_spawnAddN, 0, sizeof g_spawnAddN);
  memset(g_spawnDelN, 0, sizeof g_spawnDelN);
  f = fopen(g_file, "r");
  if (!f) return 0;             /* 这张图没存过 markers：清空即可（没有编辑） */
  while (fgets(line, sizeof line, f)) spawn_parse_line(line);
  fclose(f);
  return 1;
}

static void spawn_early_tick(void) {
  P mm;
  int t, edits = 0, ready = 0;
  if (!g_inited || !g_file[0]) return;
  mm = mm_inst();
  if (!mm) return;
  for (t = 0; t < SPAWN_TEAMS; t++)
    if (*(P*)((char*)mm + SPAWN_OFF[t])) ready = 1;
  if (!ready) return;           /* MapManager.Awake 还没把 SP_* 拆出来 */
  if (mm != g_spawnEarlyMm) {
    g_spawnEarlyMm = mm;
    for (t = 0; t < SPAWN_TEAMS; t++) {
      g_spawnOrigN[t] = 0; g_spawnOrigOk[t] = 0;
      g_spawnWritten[t] = 0; g_spawnCaptured[t] = 0;
    }
    g_spawnGap = 0.0f; g_spawnGapOk = 0; g_spawnHeightsFixed = 0;
    if (!spawn_early_load()) return;
    elog("spawn: 开局抢跑 MapManager=%p  markers 出生点 新增 %d+%d+%d / 删除 %d+%d+%d",
         (void*)mm, g_spawnAddN[0], g_spawnAddN[1], g_spawnAddN[2],
         g_spawnDelN[0], g_spawnDelN[1], g_spawnDelN[2]);
  }
  if (!g_hookOn) spawn_hook_install();   /* 兜底重试：直到装上（失败过就不再刷屏） */
  for (t = 0; t < SPAWN_TEAMS; t++)
    if (g_spawnAddN[t] || g_spawnDelN[t]) edits = 1;
  if (edits) spawn_apply();     /* 数组被游戏重建时也在这里自愈 */
}

/* 高频 tick 入口（navfix 的 hi-res WM_TIMER 和 4 Hz 的 editor_tick 都会调） */
void editor_spawn_tick(void) { spawn_early_tick(); }

/* ============ 取点钩子：整函数替换 MapManager.GetSpawnPoint ============
 * 为什么必须在这一层：人机第一次出生发生在「地图加载那一帧」，任何 tick 都晚一步；
 * 写数组只是改结果，改不到「游戏向谁要这个点」。所以直接把取点函数换掉 ——
 * 游戏每次出生（首波 + 复活）都来问我们，我们直接给「新增优先 + 原生去删除」的点。
 *
 * 目标函数（反汇编核实，RVA 0xAEB6E0，开头 55 8B EC = push ebp; mov ebp,esp）：
 *   void __cdecl GetSpawnPoint(SpawnPoint* ret, int team, const MethodInfo*)
 *   ret = 16 B（Vector3 + 朝向）；team 0=BL / 1=GR / 其他=Neutral；调用方 add esp,0Ch。
 * 我们完全接管、不调用原函数；某队没有编辑时按原逻辑复刻（读游戏数组 + 自己的轮转）。
 * ucf_mod.json 里 "spawn_hook": false 就完全不碰游戏代码。 */
#define R_GET_SPAWN 0xAEB6E0
static int g_hookId[SPAWN_TEAMS];    /* 我们自己的取点轮转（对应游戏的 SPID_*） */
static int g_hookCalls, g_hookLogs;
static unsigned char g_hookSave[5];

/* markers 里的 spawn/spawndel 不依赖场景：初始化时就先读进来，
 * 这样「第一波出生」——它比任何 tick 都早——钩子手里已经有数据。 */
void spawn_preload(void) {
  int t, any = 0;
  for (t = 0; t < SPAWN_TEAMS; t++) if (g_spawnAddN[t] || g_spawnDelN[t]) any = 1;
  if (any) return;                    /* 已经读过：别把用户正在编的改动冲掉 */
  if (!spawn_early_load()) return;
  elog("spawn: 预读 markers 出生点 新增 %d+%d+%d / 删除 %d+%d+%d",
       g_spawnAddN[0], g_spawnAddN[1], g_spawnAddN[2],
       g_spawnDelN[0], g_spawnDelN[1], g_spawnDelN[2]);
}

/* 这张图的钩子数据必须对得上：MapManager 换了实例 = 新的一局 / 换图，
 * 旧图的原生快照和编辑清单都不能再用（否则第一波会拿到上一张图的坐标）。 */
static P g_hookMm;

static void hook_sync(void) {
  P mm = mm_inst();
  int t;
  if (!mm) return;
  if (mm == g_hookMm) return;
  g_hookMm = mm;
  for (t = 0; t < SPAWN_TEAMS; t++) {
    g_spawnOrigN[t] = 0; g_spawnOrigOk[t] = 0;
    g_spawnWritten[t] = 0; g_spawnCaptured[t] = 0;
  }
  g_spawnGap = 0.0f; g_spawnGapOk = 0; g_spawnHeightsFixed = 0;
  spawn_early_load();                 /* 只读这张图 markers 里的 spawn / spawndel */
  memset(g_hookId, 0, sizeof g_hookId);
  elog("spawn: hook 换图 → 重读 markers 出生点 新增 %d+%d+%d / 删除 %d+%d+%d",
       g_spawnAddN[0], g_spawnAddN[1], g_spawnAddN[2],
       g_spawnDelN[0], g_spawnDelN[1], g_spawnDelN[2]);
}

/* 取 team 的生效点。数组换了（新图 / 游戏 Awake 重建）就重拍原生快照；
 * 这张图本来没有这个数组（例：团队图没有 Neutral）但我们有新增点，就按"原生 0 个"算。 */
static int hook_points(int team, SPT* out, int cap) {
  P mm, arr;
  int has;
  if (team < 0 || team >= SPAWN_TEAMS) return 0;
  mm = mm_inst();
  if (!mm) return 0;
  arr = *(P*)((char*)mm + SPAWN_OFF[team]);
  has = (arr && mem_ok(arr, 0x10)) ? 1 : 0;
  if (!has && !g_spawnAddN[team] && !g_spawnDelN[team]) return 0;
  if (has && (!g_spawnOrigOk[team] ||
              (arr != g_spawnCaptured[team] && arr != g_spawnWritten[team]))) {
    spawn_capture(team, arr);         /* 新图 / 游戏 Awake 重建：以它为原生 */
    g_spawnWritten[team] = 0;
    g_hookId[team] = 0;
  } else if (!has && !g_spawnOrigOk[team]) {
    g_spawnOrigN[team] = 0;
    g_spawnOrigOk[team] = 1;
    g_spawnCaptured[team] = 0;
  }
  return spawn_effective(team, out, 0, cap);
}

/* 注意返回值：这是 16 B 结构体的 sret 调用方（Player.Spawn / MoveToRespawnPos）在
 * call 之后是 `movups xmm0,[eax]` —— 要求把返回缓冲区指针放在 EAX。
 * 所以这个钩子必须原样把 ret 返回，不能是 void（否则 [eax] 取到垃圾，直接崩/乱出生）。 */
static void* __cdecl spawn_hook_get(SPT* ret, int team, void* method) {
  static SPT pts[MAX_SPAWN_ORIG + MAX_SPAWN_EDIT];
  int t, n, k;
  (void)method;
  if (!ret) return 0;
  g_hookCalls++;
  hook_sync();
  t = (team == 0 || team == 1) ? team : 2;
  n = hook_points(t, pts, (int)(sizeof pts / sizeof pts[0]));
  if (n <= 0 && t == 2) {             /* 个人竞技图没有 Neutral：借用 BL/GR（和模式兜底同一套） */
    n = hook_points(0, pts, (int)(sizeof pts / sizeof pts[0]));
    if (n <= 0) n = hook_points(1, pts, (int)(sizeof pts / sizeof pts[0]));
    /* 轮转仍记在请求的队上（t 不变），只是数据来自借用队 */
  }
  if (n <= 0) {
    memset(ret, 0, 16);
    if (g_hookLogs < 8) {
      g_hookLogs++;
      elog("spawn: hook team=%d 没有可用出生点（这张图没数据？）→ 返回零点", team);
    }
    return ret;
  }
  k = g_hookId[t];
  if (k < 0 || k >= n) k = 0;
  g_hookId[t] = (k + 1 >= n) ? 0 : (k + 1);
  *ret = pts[k];
  if (g_hookLogs < 10) {
    g_hookLogs++;
    elog("spawn: hook GetSpawnPoint team=%d → #%d/%d (%.2f %.2f %.2f)",
         team, k, n, ret->p.x, ret->p.y, ret->p.z);
  }
  return ret;
}

/* 打补丁：入口 5 字节改成 E9 rel32，跳到 spawn_hook_get。只在初始化、场景未加载时做。 */
static int spawn_hook_install(void) {
  static int warnedNoGa, tried;
  unsigned char* p;
  DWORD old;
  long rel;
  if (g_hookOn) return 1;
  if (tried) return 0;                  /* 校验/改页失败过：别再重试刷屏 */
  if (!g_ga) {
    if (!warnedNoGa) {                  /* 初始化还没跑完：下一拍再装（别静默） */
      warnedNoGa = 1;
      elog("spawn: hook 等 GameAssembly 基址（ed_init 还没跑），下一拍再装");
    }
    return 0;
  }
  p = (unsigned char*)RVA(R_GET_SPAWN);
  if (!p) return 0;
  if (!(p[0] == 0x55 && p[1] == 0x8B && p[2] == 0xEC)) {
    tried = 1;
    elog("spawn: hook 放弃 —— 0x%X 处不是 push ebp;mov ebp,esp（字节 %02X %02X %02X），版本对不上？",
         (unsigned)R_GET_SPAWN, p[0], p[1], p[2]);
    return 0;
  }
  memcpy(g_hookSave, p, 5);
  rel = (long)((unsigned char*)(void*)spawn_hook_get - (p + 5));
  if (!VirtualProtect(p, 16, PAGE_EXECUTE_READWRITE, &old)) {
    tried = 1;
    elog("spawn: hook VirtualProtect 失败 err=%lu", GetLastError());
    return 0;
  }
  p[0] = 0xE9;
  { int r32 = (int)rel; memcpy(p + 1, &r32, 4); }
  VirtualProtect(p, 16, old, &old);
  FlushInstructionCache(GetCurrentProcess(), p, 16);
  g_hookOn = 1;
  elog("spawn: hook GetSpawnPoint @%p → %p（原字节 %02X %02X %02X %02X %02X）",
       (void*)p, (void*)&spawn_hook_get,
       g_hookSave[0], g_hookSave[1], g_hookSave[2], g_hookSave[3], g_hookSave[4]);
  return 1;
}

/* Ctrl+7「重读 markers」前把数组还原成原生：否则 reset 之后会把
 * 我们写回去的（含新增点的）数组当成原生快照，再套一遍就重复了。 */
static void spawn_restore_orig(void) {
  P mm = mm_inst();
  int team;
  if (!mm) return;
  for (team = 0; team < SPAWN_TEAMS; team++) {
    int off = SPAWN_OFF[team];
    P cur = *(P*)((char*)mm + off);
    if (!g_spawnOrigOk[team] || !g_spawnWritten[team] || cur != g_spawnWritten[team]) continue;
    if (g_spawnOrigN[team] > 0 &&
        spawn_write(team, mm, g_spawnOrig[team], g_spawnOrigN[team]))
      elog("spawn: 重读前还原原生 team=%s %d 个", SPAWN_NAME[team], g_spawnOrigN[team]);
    else if (g_spawnOrigN[team] <= 0) {
      /* 这张图本来没有这个数组（例：团队图没有 Neutral）：我们把新增点写进去过，
       * 还原就得写回 null，否则"原生 0 个"留在场上。 */
      if (x_gc_wbarrier_set_field) x_gc_wbarrier_set_field(mm, (char*)mm + off, 0);
      *(P*)((char*)mm + off) = 0;
      elog("spawn: 重读前还原原生 team=%s（原生 0 个 → 字段写回 null）", SPAWN_NAME[team]);
    }
    g_spawnWritten[team] = 0;
    g_spawnCaptured[team] = 0;
    g_spawnOrigOk[team] = 0;
  }
}

/* how many crouch markers this editor created (so navfix can tell them apart
 * from the map's own points before deciding to bulk-inject its draft grid) */
int editor_crouch_made(void) {
  int i, c = 0;
  for (i = 0; i < g_n; i++) if (g_mk[i].type == 1) c++;
  return c;
}

/* 玩家坐标记录点：导出给 navfix，用来在记录位置直接造蹲守点
 * （用户站在箱子顶/路口记一条，人机就会把那里当目标走过去）。 */
int editor_pm_count(void) {
  return g_pmN;
}

int editor_pm_get(int idx, float* x, float* y, float* z) {
  if (idx < 0 || idx >= g_pmN) return 0;
  if (x) *x = g_pmP[idx].x;
  if (y) *y = g_pmP[idx].y;
  if (z) *z = g_pmP[idx].z;
  return 1;
}

void editor_on_scene(void* astar) {
  if (!astar) return;
  if (!ed_init()) return;
  if (astar == g_lastAstar) return;
  elog("scene: enter astar=%p inited=%d", astar, g_inited);
  g_lastAstar = (P)astar;
  /* 2026-11-25：换房间 = 没按 Ctrl+S 的编辑作废（用户要求：不保存，退出房间就没了）。
   * 这里先按旧图的状态打一行日志，再交给下面的 reset/load 清内存。 */
  if (editor_unsaved()) {
    elog("scene: 退出房间，丢弃未保存的编辑（点图 %d 项 / 标记 %d 个 / 出生点 新增 %d+%d+%d 删除 %d+%d+%d）"
         "-- 只有 Ctrl+S 才会落盘",
         g_nedN, g_n, g_spawnAddN[0], g_spawnAddN[1], g_spawnAddN[2],
         g_spawnDelN[0], g_spawnDelN[1], g_spawnDelN[2]);
  }
  g_dirtyNav = 0;
  g_dirtyMk = 0;
  /* 换图前如果字段里还是我们写回去的数组，先还原成快照里的原生点脚，
   * 再 reset/load；避免上一张图的改动静默留在新图数组里。 */
  spawn_restore_orig();
  reset_markers();
  elog("scene: markers reset");
  overlay_reset();
  elog("scene: ui reset");
  vis_scene_reset();
  elog("scene: vis reset");
  ghost_reset();          /* 预置虚线框/虚线点随场景一起没了，网格缓存也要重来 */
  roots_clear();          /* 上一张图的对象已经销毁，句柄还回去 */
  g_rootsFull = 0;
  g_sceneAge = 0;
  g_sceneReadyOnce = 0;
  g_nedGraph = 0;
  g_nedApplied = 0;
  g_nedWaitN = -1;
  g_nedHasA = 0;
  g_nedN = 0;
  ed_history_reset();
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
/* grow 模式（真·新建节点）要用的 A* 内部入口。2026-11-19 对 GameAssembly.dll
 * 做静态核对（x86 32-bit；VA = RVA + 0x10000000）：
 *   PathProcessor.Lock(bool) -> int      0x5E9660   queue.Block() 后自旋等线程停
 *   PathProcessor.Unlock(int id)         0x5E9910
 *   PointGraph.AddNode(Int3) -> PointNode 0x5EE7D0  自己扩 nodes 数组
 * 关键：PathProcessor.InitializeNode 第一件事就是
 *     if (!queue.AllReceiversBlocked) throw ...
 * 所以建点必须整段发生在 Lock(true) … Unlock 之间，否则节点拿到 nodeIndex 却没
 * 进每一条线程的 PathHandler，第一条路径就在 GetPathNode(idx) 越界。
 * 扩容本身由引擎负责（PathHandler.InitializeNode: Max(len*2, 0x80)），
 * 这里没有 786 这类数量上限。 */
#define R_PP_LOCK      0x5E9660
#define R_PP_UNLOCK    0x5E9910
#define R_PG_ADD_NODE  0x5EE7D0


/* 被禁用的点会被挪到这么深的地下：游戏用 GetNearest(pos)（NNConstraint.None，
 * 不看可走性）取人机脚下最近的节点，死点留在原地就会一直赢过真正可走的点。
 * 挪走之后按原坐标还能找回它（nav_find_any 会试着加回这个高度）。 */
#define NAV_DEAD_DY 20000.0f
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
    /* 死点被挪到地下：还没超出容差就再按原高度试一次，撤销/重套才找得到它 */
    if (d >= bestd && !nav_walk(nd)) {
      V3 q2 = q;
      q2.y += NAV_DEAD_DY;
      d = nav_d2(p, &q2);
    }
    if (d < bestd) { bestd = d; best = i; }
  }
  return best;
}
/* 找「被删掉的那个点」：死点会被挪到地下 NAV_DEAD_DY，重套一次可能多挪一次，
 * 而 nav_find_any 只补一次高度。撤销删点必须找对原来的槽位 —— 找错就等于把别的
 * 死点搬过来（原来的点还是回不来）。这里按整数倍高度逐个试。 */
static int nav_find_dead_at(P g, const V3* p) {
  int i, k, n;
  if (!g) return -1;
  n = nav_count(g);
  for (k = 0; k <= 4; k++) {
    V3 q = *p;
    float best = 0.35f * 0.35f;
    int bestI = -1;
    q.y -= (float)k * NAV_DEAD_DY;
    for (i = 0; i < n; i++) {
      P nd = nav_node(g, i);
      V3 r;
      float d;
      if (!nd || nav_walk(nd)) continue;
      nav_pos(nd, &r);
      d = nav_d2(&q, &r);
      if (d < best) { best = d; bestI = i; }
    }
    if (bestI >= 0) return bestI;
  }
  return -1;
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
  if (g_nedGrow && g_packName[0]) {
    /* grow：原生点本来就永久标死，没有「原生点复活」这回事；节点数已由上面的
     * g_nedExpect 兜住。这里只核对边，省掉 n×M 的坐标扫描（grow 图节点更多）。 */
    int j;
    if (!g_nedN) return 0;
    for (j = 0; j < g_nedN; j++) {
      NAVED* e = &g_ned[j];
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
    if (e->kind == JADD) continue;        /* 跳链建完就留着，不参与边的核对 */
    if (e->kind == NPOPADD) continue;     /* 会话级辅助条目：只影响撤销，不进图 */
    if (e->kind == NMOVE) {               /* 贴地：点没摆在新位置上就重套 */
      if (nav_find_any(g, &e->b, 0.35f) < 0) return 1;
      continue;
    }
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
  /* 2026-11-19 更正：PathHandler 不是进图时一次分配——它按节点创建懒增长，
   * 786 不是上限。这里仍然只借槽位（稳妥路径）；要真·新增节点用 grow/keep 包，
   * 见 nav_apply_grow（必须在 PathProcessor.Lock(true) 窗口里建点）。
   * 这条日志 ~5 s 内只打一次：真正的反馈走屏幕中央 toast（toast_show）。 */
  {
    static unsigned lastMs;
    unsigned now = GetTickCount();
    if (!lastMs || now - lastMs > 5000) {
      lastMs = now;
      elog("naved: add refused: no free slot (graph full, %d nodes) - delete a node first, "
           "or use a grow pack (真·新增节点)", n);
    }
  }
  return -1;
}
static void nav_refresh(P g) {
  if (g && g_ga) ((void (*)(P))RVA(R_PG_REBUILD))(g);
  g_visDirty = 1;
}
/* 彻底断开一个节点（不可走 + 清连接 + 清别人的反向引用） */
static void nav_kill_node(P g, P nd) {
  int i, n = nav_count(g);
  V3 p;
  nav_set_walk(nd, 0);
  nav_conn_clear(nd);
  /* 就地删掉的点也挪走：游戏取脚下最近节点不看可走性，留在原地会挡人机的路。
   * 撤销时 nav_undo 会把坐标写回来。 */
  nav_pos(nd, &p);
  p.y -= NAV_DEAD_DY;
  nav_put_pos(nd, &p);
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
/* ---- 编辑清单的落盘/读取（每张图一个文件） ----
 * 指纹只算「进图时的原生点数」：grow 新建的点会把 nav_count 变大，
 * 要是也算进去，重新应用 / 切回正式版时指纹就变了，文件反而找不到。 */
static P g_fpGraph;
static int g_fpBaseN = -1;        /* <0 = 还不知道；0 = 空图（0 点图也合法） */
static void nav_fp(char* out, int cap) {
  P g = navfix_point_graph();
  unsigned long long xr = 0;
  int i, n = nav_count(g);
  /* 原生点数由 nav_edit_tick 在「图稳定」那一刻记下来（g_fpBaseN），这里只截断：
   * grow 新建的点不参与指纹，否则文件名会从 n786-… 变成 n786+N-…。 */
  if (g && g_fpBaseN >= 0 && n > g_fpBaseN) n = g_fpBaseN;
  for (i = 0; i < n; i++) {
    P nd = nav_node(g, i);
    V3 p;
    if (!nd) continue;
    /* grow 会把禁用掉的原生点挪到地下，指纹要用快照里的原版坐标，否则换了值 */
    if (g_navBase && g_navBaseG == g && i < g_navBaseN) p = g_navBase[i].pos;
    else nav_pos(nd, &p);
    xr ^= pt_hash(&p, 0);
  }
  sprintf(out, "n%d-%016llx", n, xr);
  (void)cap;
}
/* 整行 token：line 以 tok 开头，后面就是行尾或空白（防止 "grown" 之类误判）。 */
static int nav_tok(const char* line, const char* tok) {
  size_t n = strlen(tok);
  return !strncmp(line, tok, n) &&
         (line[n] == 0 || line[n] == ' ' || line[n] == '\r' || line[n] == '\n');
}
/* 0 节点图（飓风危城）：只有空白地图（grow）能套——它不需要原生槽位。
 * 进图初期图可能还没扫出来，所以只在「测试包 + 文件里有 grow/keep」时放行，
 * 其它 0 节点情况继续等下一帧。 */
static int nav_zero_grow_ready(void) {
  char path[MAX_PATH], line[64];
  FILE* f;
  int grow = 0;
  if (!g_packName[0] || !g_navDir[0]) return 0;
  nav_fp(g_nedFp, sizeof(g_nedFp));
  sprintf(path, "%s\\%s.txt", g_navDir, g_nedFp);
  f = fopen(path, "r");
  if (!f) return 0;
  while (fgets(line, sizeof line, f)) {
    if (nav_tok(line, "grow") || nav_tok(line, "keep") || nav_tok(line, "blank")) {
      grow = 1;
      break;
    }
  }
  fclose(f);
  return grow;
}
/* 返回 1 = 写成功（含「没有点图改动 → 删掉文件」），0 = 被拒 / 失败。
 * 2026-11-25 起只由 editor_save_all（Ctrl+S）和控制台 cmd=save 调用。 */
static int nav_save(void) {
  FILE* f;
  int i, session = 0;
  int blank = g_nedBlank && g_packName[0];
  int keep = g_nedKeep && g_packName[0];
  if (!g_nedPath[0]) { elog("naved: save skipped (no edit file for this map)"); return 0; }
  /* 四版纪律：正式版 nav\ 只允许控制台从 ② 开发版推过来，游戏内不许直接写 ③。
   * 想边玩边改就先选一个测试包（④ packs），或去网页编辑器改 ②。 */
  if (g_navReadOnly && !g_packName[0]) {
    if (!g_saveWarned) {
      g_saveWarned = 1;
      elog("naved: save blocked - official nav\\ is read-only (UCF_NAV_READONLY); "
           "use a test pack or the web editor (navdata\\dev)");
    }
    return 0;
  }
  /* 只统计真正会落盘的条目：会话级的贴地 / 删自加点辅助条目不算数 */
  for (i = 0; i < g_nedN; i++)
    if (g_ned[i].kind == NMOVE || g_ned[i].kind == NPOPADD) session++;
  if (g_nedN - session <= 0 && !blank && !keep) { DeleteFileA(g_nedPath); return 1; }
  f = fopen(g_nedPath, "w");
  if (!f) { elog("naved: save failed %s", g_nedPath); return 0; }
  fprintf(f, "# ucf-navedit v1 fp=%s\n", g_nedFp);
  if (blank) fprintf(f, "grow\n");   /* 空白地图 = grow（不再写 blank 兼容行） */
  if (keep) fprintf(f, "keep\n");    /* keep 自带 grow 语义，不写 grow */
  for (i = 0; i < g_nedN; i++) {
    NAVED* e = &g_ned[i];
    /* NMOVE / NPOPADD 是会话级的撤销辅助条目，不写盘：
     * 贴地本来就没有 move 格式（文件只认坐标），删掉自己加的点则只该少一条 node add。 */
    if (e->kind == NMOVE || e->kind == NPOPADD) continue;
    if (e->kind == NADD)
      fprintf(f, "node add %.3f %.3f %.3f\n", e->a.x, e->a.y, e->a.z);
    else if (e->kind == NDEL)
      fprintf(f, "node del %.3f %.3f %.3f\n", e->a.x, e->a.y, e->a.z);
    else if (e->kind == JADD) {
      /* 2026-11-25：needSpeed / accuracy / direction 不是默认值时一起写回。
       * 否则文件里调好的「0 0.5 0」只要在游戏内保存一次就退回 0 / 1.0（站着不跳）。
       * 2026-11-27：带蹲信息的跳要写满 12 列，否则游戏里保存一次蹲信息就没了。 */
      if (e->jctb >= 0)
        fprintf(f, "jump add %.3f %.3f %.3f %.3f %.3f %.3f %.2f %.2f %d %.2f %.2f %d\n",
                e->a.x, e->a.y, e->a.z, e->b.x, e->b.y, e->b.z,
                (e->jspeed >= 0.0f) ? e->jspeed : 0.0f,
                (e->jacc >= 0.0f) ? e->jacc : 0.5f, e->jdir,
                e->jct0, e->jct1, e->jctb);
      else if (e->jspeed >= 0.0f || e->jacc >= 0.0f || e->jdir != 0)
        fprintf(f, "jump add %.3f %.3f %.3f %.3f %.3f %.3f %.2f %.2f %d\n",
                e->a.x, e->a.y, e->a.z, e->b.x, e->b.y, e->b.z,
                e->jspeed, e->jacc, e->jdir);
      else
        fprintf(f, "jump add %.3f %.3f %.3f %.3f %.3f %.3f\n",
                e->a.x, e->a.y, e->a.z, e->b.x, e->b.y, e->b.z);
    }
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
  elog("naved: saved %d edits -> %s%s%s%s%s", g_nedN - session, g_nedPath,
       blank ? " (blank base)" : "", (blank && g_nedGrow) ? " [grow]" : "",
       keep ? " [keep native]" : "",
       session ? "（本次会话的贴地/删自加点辅助条目不落盘）" : "");
  return 1;
}

/* ---- 唯一的保存入口（2026-11-25 用户要求）----------------------------------
 * Ctrl+S / F2 菜单「撤销 / 保存」→「保存」/ 控制台 cmd=save 都走这里。
 * 只写脏的那一边；两边都没改就不写 —— 控制台和录制会直接改盘上的同一个文件，
 * 没改过的文件重写一次就可能把它们刚追加的行盖掉。 */
void editor_save_all(void) {
  int ok = 1, wrote = 0;
  if (!ed_init()) return;
  if (!navfix_point_graph()) {
    elog("save: 不在房间里（没有 PointGraph），没有可保存的编辑");
    toast_bad("不在房间里：没有可保存的编辑");
    return;
  }
  if (!editor_unsaved()) {
    elog("save: 没有改动（Ctrl+S 只保存改过的内容；不保存就退房间 = 改动丢弃）");
    toast_ok("没有改动：当前内容已经是保存状态");
    menu_refresh();
    return;
  }
  if (g_dirtyNav) {
    if (!g_nedPath[0]) {
      elog("save: 本图没有点图编辑文件（测试包被跳过 / 图还没就绪），点图改动没保存");
      ok = 0;
    } else if (!nav_save()) {
      ok = 0;
    } else {
      g_dirtyNav = 0;
      wrote = 1;
    }
  }
  if (g_dirtyMk) {
    if (!save_file()) ok = 0;
    else { g_dirtyMk = 0; wrote = 1; }
  }
  if (ok && wrote) {
    elog("save: 已保存（Ctrl+S）-- 点图 %d 项 / 标记 %d 个 / 出生点 新增 %d+%d+%d 删除 %d+%d+%d；退出房间后仍然有效",
         g_nedN, g_n, g_spawnAddN[0], g_spawnAddN[1], g_spawnAddN[2],
         g_spawnDelN[0], g_spawnDelN[1], g_spawnDelN[2]);
    toast_ok("已保存：点图 %d 项 / 标记 %d 个（退房间后仍然有效）", g_nedN, g_n);
  } else if (!ok) {
    elog("save: 有改动没写进去（见上面的错误），未保存状态保留");
    toast_bad("有改动没写进去（看游戏日志），还是未保存状态");
  }
  menu_refresh();
  overlay_refresh();
}
static void nav_edit_load(const char* path) {
  FILE* f = fopen(path, "r");
  char line[256];
  g_nedN = 0;
  g_redoN = 0;
  g_cjN = 0;                 /* 换图 / 重载清单：节点指针全变了，蹲跳表作废重登记 */
  g_nedBlank = 0;
  g_nedGrow = 0;
  g_nedKeep = 0;
  if (!f) return;
  while (fgets(line, sizeof(line), f)) {
    NAVED e;
    int n = 0, jdir = 0, jctb = -1;
    float x, y, z, x2, y2, z2, jspeed = -1.0f, jacc = -1.0f;
    float jct0 = -1.0f, jct1 = -1.0f;
    char k1[16];
    memset(&e, 0, sizeof e);
    e.jspeed = -1.0f;
    e.jacc = -1.0f;
    e.jct0 = -1.0f;
    e.jct1 = -1.0f;
    e.jctb = -1;
    if (line[0] == '#' || line[0] == '\n') continue;
    /* 空白地图（grow）：原生点全禁 + AddNode 新建，文件里的 node add / edge add
     * 就是进图后的全部路线。旧的 blank 写法等价于 grow（借槽位那套已经删掉了），
     * 照旧认，老包和网页编辑器写的文件不用改。只有测试包才允许替换底图。 */
    if (nav_tok(line, "grow") || nav_tok(line, "blank")) {
      g_nedGrow = 1;
      g_nedBlank = 1;
      continue;
    }
    /* keep：原版底图 + 新增——原生点一个都不动，只把文件里的 node add 加到图上。 */
    if (nav_tok(line, "keep")) {
      g_nedKeep = 1;
      g_nedGrow = 1;
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
    } else if ((n = sscanf(line, "jump %15s %f %f %f %f %f %f %f %f %d %f %f %d",
                            k1, &x, &y, &z, &x2, &y2, &z2,
                            &jspeed, &jacc, &jdir, &jct0, &jct1, &jctb)) >= 7) {
      /* 跳跃链接：起点 A（人机跑到这里起跳）-> 落点 B（踩箱子 / 上层平台）。
       * 可选三个参数（2026-11-25 为对照实验加的，不写就是老行为）：
       *   needSpeed  accuracy  direction(0=沿A->B / 1=正上 / 2=前上)
       * 只在点铺好之后建，见 nav_apply_jumps。 */
      if (k1[0] != 'a') continue;
      e.kind = JADD;
      e.a.x = x; e.a.y = y; e.a.z = z;
      e.b.x = x2; e.b.y = y2; e.b.z = z2;
      e.jspeed = (n >= 8) ? jspeed : -1.0f;
      e.jacc   = (n >= 9) ? jacc   : -1.0f;
      e.jdir   = (n >= 10) ? jdir  : 0;
      /* 2026-11-27：第 11~13 列是蹲（老文件没有 = 未知，-1） */
      e.jct0 = (n >= 11) ? jct0 : -1.0f;
      e.jct1 = (n >= 12) ? jct1 : -1.0f;
      e.jctb = (n >= 13) ? jctb : -1;
    } else {
      continue;
    }
    if (g_nedN < NAV_ED_MAX) g_ned[g_nedN++] = e;
  }
  fclose(f);
  if (g_nedKeep) g_nedBlank = 0;   /* keep 与 blank 互斥：残留的 blank/grow 行不能把它降级 */
  elog("naved: loaded %d edits from %s%s%s", g_nedN, path,
       g_nedBlank ? " (blank base)" : "", g_nedKeep ? " [keep native]" : "");
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
  if (n < 0 || n > NAV_MAXN) return;
  nav_fp(fp, sizeof fp);
  /* 快照只收原生点：grow 新建出来的点不属于「底图」，不能写进快照，
   * 否则切包/回正式版时会把它们当成原生点复活。0 点图也拍一份空快照，
   * 这样「回正式版」能把 grow 出来的点全部收回。 */
  if (g_fpBaseN >= 0 && n > g_fpBaseN) n = g_fpBaseN;
  if (g_navBase && g_navBaseG == g && g_navBaseN == n && !strcmp(g_navBaseFp, fp)) return;
  nav_base_free();
  g_navBase = (NAVBASENODE*)calloc((size_t)(n > 0 ? n : 1), sizeof(NAVBASENODE));
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
  /* grow 之后 n > 快照点数：快照仍是前 g_navBaseN 个节点的原生状态，
   * 超出部分（我们自己新建的）在下面统一标死。 */
  if (!g_navBase || g_navBaseG != g || n < g_navBaseN) return 0;
  if (!g_connCls || !x_array_new) {
    elog("naved: restore skipped (connection class unavailable)");
    return 0;
  }
  for (i = 0; i < g_navBaseN; i++) {
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
  /* grow 加出来的点不在快照里：标死 + 断边，别让它们留在正式版 / 别的包里 */
  for (i = g_navBaseN; i < n; i++) {
    P ex = nav_node(g, i);
    if (!ex) continue;
    nav_set_walk(ex, 0);
    nav_conn_clear(ex);
  }
  g_navDeadN = 0;
  nav_refresh(g);
  elog("naved: base restored (%d native nodes%s)", g_navBaseN,
       (n > g_navBaseN) ? ", extra grow nodes disabled" : "");
  return 1;
}

/* 撤销「删点」用：只把这一个点的原始连接从底图快照搬回来，别的点不动。
 * 删点时 nav_kill_node 会清掉自己的连接表 + 摘掉别人的反向引用，只把 walk/坐标
 * 写回来是不够的（点回来了、线全没了）。搬完再由 nav_apply_edges 把清单里剩下的
 * EADD/EDEL 重新校正一遍（用户加的边 / 断的边就不会被底图覆盖）。
 * 返回 0 = 没有可用快照（grow 之后图换了、或者根本没拍过）。 */
static int nav_base_restore_conns(P g, int idx) {
  int i, j, n, v = 0;
  NAVBASENODE* s;
  P nd, nc;
  if (!g || !g_navBase || g_navBaseG != g) return 0;
  n = nav_count(g);
  if (idx < 0 || idx >= g_navBaseN || idx >= n) return 0;
  if (!g_connCls || !x_array_new) return 0;
  nd = nav_node(g, idx);
  if (!nd) return 0;
  s = &g_navBase[idx];
  if (s->cn < 0) return 0;
  for (j = 0; j < s->cn; j++) {
    int k;
    memcpy(&k, s->conn + j * 12, 4);
    if (k >= 0 && k < n && k != idx && nav_node(g, k)) v++;
  }
  nc = x_array_new(g_connCls, (unsigned)v);
  if (!nc) return 0;
  v = 0;
  for (j = 0; j < s->cn; j++) {
    int k;
    P o;
    memcpy(&k, s->conn + j * 12, 4);
    o = (k >= 0 && k < n && k != idx) ? nav_node(g, k) : 0;
    if (!o) continue;
    *(P*)((char*)nc + 0x10 + v * 12) = o;
    memcpy((char*)nc + 0x14 + v * 12, s->conn + j * 12 + 4, 4);
    *(unsigned char*)((char*)nc + 0x18 + v * 12) = s->conn[j * 12 + 8];
    v++;
  }
  nav_conn_bind(nd, nc);
  /* 别人的反向引用：底图里有 idx 的，把那条补回来 */
  for (i = 0; i < g_navBaseN && i < n; i++) {
    NAVBASENODE* t = &g_navBase[i];
    P o = nav_node(g, i);
    if (!o || o == nd || t->cn <= 0) continue;
    for (j = 0; j < t->cn; j++) {
      int k;
      memcpy(&k, t->conn + j * 12, 4);
      if (k == idx) { nav_conn_set(o, nd, 1); break; }
    }
  }
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
/* ---- grow：空白地图 = 原生点全禁 + 真正新建节点 ------------------------
 * 不再借原生槽位（借槽位永远受原生点数限制，运输船 786 点就是天花板）。
 * grow 不动原生点的数量：原生点照样全部标死，然后用 PointGraph.AddNode 新建节点，
 * nodeIndex 直接超过原生数量。数量只受 NAV_MAXN（20000）和内存限制。
 *
 * 2026-11-16「append 之后只会直走」的真正原因不是数组不能长，而是建点没在阻塞窗口：
 * PathProcessor.InitializeNode 第一件事就是 queue.AllReceiversBlocked 检查，
 * 不满足就抛异常；节点于是「有 nodeIndex、没进 handler」，寻路线程在
 * PointNode.Open -> GetPathNode(idx) 越界，A* 停摆。Lock(true) 会一直等到线程停。
 *
 * 已知边界（step 1 故意不做，日志里写清楚）：
 *   - 节点只增不减：同一张图只新建一次；要重来得重进图（场景重建后图从原生点重扫）。
 *   - 边仍按坐标 ±0.35 m 匹配，点位不能比这个容差更近。 */
static P nav_pp(void) {
  P a = navfix_astar();
  return a ? *(P*)((char*)a + 0x88) : 0;      /* AstarPath.pathProcessor @0x88 */
}
static int nav_grow_enabled(void) {
  char v[8];
  if (GetEnvironmentVariableA("UCF_NAVGROW", v, sizeof v) > 0 && v[0] == '0') return 0;
  return 1;
}
/* 2026-11-27：给纯面图现场补 PointGraph 的试验开关（车测/命令行用；正常靠「选了测试包」触发） */
static int nav_pg_test(void) {
  static int cached = -1;
  char v[8];
  if (cached >= 0) return cached;
  cached = (GetEnvironmentVariableA("UCF_PG_TEST", v, sizeof v) > 0 && v[0] == '1');
  return cached;
}
static P nav_grow_node(P g, const V3* p) {
  return ((P (*)(P, int, int, int, void*))RVA(R_PG_ADD_NODE))(
      g, (int)(p->x * 1000.0f), (int)(p->y * 1000.0f), (int)(p->z * 1000.0f), 0);
}
/* 跳链创建在菜单动作区（session-only 那条路径），这里先声明，套包时复用同一份实现。 */
static int make_jump_link_ex(V3 a, V3 b, float jspeed, float jacc, int jdir);
/* 菜单里手建跳链：参数用老默认（needSpeed 0 / accuracy 1.0 / 方向沿 A->B） */
static int make_jump_link(V3 a, V3 b) { return make_jump_link_ex(a, b, -1.0f, -1.0f, 0); }

/* 这条跳链本次进图建过没有（按起终点坐标比对） */
static int jump_seen(const V3* a, const V3* b) {
  int i;
  for (i = 0; i < g_jumpSeenN; i++)
    if (nav_d2(&g_jumpSeenA[i], a) < 1e-4f && nav_d2(&g_jumpSeenB[i], b) < 1e-4f) return 1;
  return 0;
}
/* 撤销跳点：把「本次建过」的记录一起摘掉。不摘的话重读包时 nav_apply_jumps
 * 会以为已经建过而跳过，用户撤销过的跳链就再也回不来了。 */
static void jump_unsee(const V3* a, const V3* b) {
  int i, j = 0;
  for (i = 0; i < g_jumpSeenN; i++) {
    if (nav_d2(&g_jumpSeenA[i], a) < 1e-4f && nav_d2(&g_jumpSeenB[i], b) < 1e-4f) continue;
    g_jumpSeenA[j] = g_jumpSeenA[i];
    g_jumpSeenB[j] = g_jumpSeenB[i];
    j++;
  }
  g_jumpSeenN = j;
}

/* 套用文件里的 jump add 行：必须晚于点/边全部生效（OnLatePostScan 要按坐标找节点）。
 * 按坐标去重：同一张图重套包时只补新建的跳链，已建过的跳过。 */
static int nav_apply_jumps(P g) {
  int i, made = 0, bad = 0, fixed = 0;
  if (!g) return 0;
  for (i = 0; i < g_nedN; i++) {
    NAVED* e = &g_ned[i];
    int ia, ib;
    if (e->kind != JADD) continue;
    if (jump_seen(&e->a, &e->b)) continue;
    /* 体检（和 tools/check_jumps.py 同一套判据）：太短 / 端点没路点 / 两端同一个点，
     * 这三种跳链人机永远不会用，建出来只会白占 GameObject 和 linkDic。 */
    if (nav_d2(&e->a, &e->b) < 2.25f) { bad++; continue; }
    ia = nav_find(g, &e->a, 1.0f);
    ib = nav_find(g, &e->b, 1.0f);
    if (ia < 0 || ib < 0 || ia == ib) { bad++; continue; }
    if (e->jctb >= 0)
      elog("naved: jump (%.2f %.2f %.2f)->(%.2f %.2f %.2f) 带蹲: 空中蹲 [%.2f, %.2f] s, 起跳时蹲=%d",
           e->a.x, e->a.y, e->a.z, e->b.x, e->b.y, e->b.z, e->jct0, e->jct1, e->jctb);
    if (!make_jump_link_ex(e->a, e->b, e->jspeed, e->jacc, e->jdir)) continue;
    /* 带蹲的跳：把起点节点登记下来，飞行中把人机顶成蹲（crouch_jump_tick） */
    if (e->jctb >= 0) cj_remember(nav_node(g, ia), e->jct0, e->jct1);
    made++;
    if (g_jumpSeenN < JSEEN_MAX) {
      g_jumpSeenA[g_jumpSeenN] = e->a;
      g_jumpSeenB[g_jumpSeenN] = e->b;
      g_jumpSeenN++;
    }
    /* 跳链只在路径里「起点节点 -> 落点节点」相邻时才插跳跃段，
     * 这两点之间没有边的话 A* 永远排不出来，跳链一次都不会触发。 */
    if (!nav_conn_has(nav_node(g, ia), nav_node(g, ib))) {
      nav_conn_set(nav_node(g, ia), nav_node(g, ib), 1);
      fixed++;
    }
  }
  if (made) elog("naved: %d jump link(s) created from pack (+%d A->B edge)", made, fixed);
  if (bad) elog("naved: %d jump line(s) skipped: 两端都要是路点、不能同一个点、长度 >= 1.5 m"
                " (python tools/check_jumps.py 可体检包文件)", bad);
  if (fixed) nav_refresh(g);
  return made;
}
static int nav_apply_grow(P g) {
  P pp, nd;
  int i, n, killed = 0, made = 0, skipped = 0, ops = 0, lockId;
  int keep = g_nedKeep;           /* keep：原生点原样保留，只新增节点 */
  if (!g) return 0;
  /* 2026-11-27 纯面图：点图是插件现场补的、这份草稿又是空白/grow —— 把这张图的可走面摘掉。
   * 不摘的话人机「脚下最近节点」永远落在三角网上（A* 多图不跨图连边），画的点等于没画。 */
  if (!keep && g_pgSynthetic && !g_pgNmDropped) {
    if (navfix_drop_navmesh()) g_pgNmDropped = 1;
  }
  n = nav_count(g);
  /* n == 0 也允许：0 点图（飓风危城）正是 grow 唯一能用的场景 */
  if (n < 0 || n > NAV_MAXN) { elog("naved: grow skipped: bad node count %d", n); return 0; }
  /* 同一张图只新建一次：重套 / 重新应用只补边和新建的跳链，不再加点 */
  if (g == g_growGraph && nav_count(g) == g_growBase + g_growMade) {
    ops = nav_apply_edges(g);
    ops += nav_apply_jumps(g);   /* 后加的跳链也要补建，不能只补边 */
    elog("naved: %s already applied on this graph (%d base + %d new); edges+jumps (%d)",
         keep ? "keep" : "grow", g_growBase, g_growMade, ops);
    return ops;
  }
  pp = nav_pp();
  if (!pp) {                      /* AstarPath.Awake 还没跑完：下一个 tick 再来 */
    elog("naved: grow waiting: pathProcessor not ready yet");
    return -1;
  }
  lockId = ((int (*)(P, int, void*))RVA(R_PP_LOCK))(pp, 1, 0);
  /* 1) 原生点全部标死 + 清边：不留任何一条原生路线。
   *    keep 模式整段跳过：原生点一个都不碰，这样才能把「新节点不被认」和
   *    「我们改坏了原图」分开。 */
  if (!keep) {
    for (i = 0; i < n; i++) {
      V3 p;
      nd = nav_node(g, i);
      if (!nd) continue;
      if (nav_walk(nd)) killed++;
      nav_set_walk(nd, 0);
      nav_conn_clear(nd);
      /* 关键：游戏取「脚下最近的节点」当寻路起点用的是
       *     AstarPath.GetNearest(Vector3)   == NNConstraint.None（不看可走性）
       * （Bot.UpdateNearestGraphNode 0xB33260 的单参重载，2026-11-20 IDA 核对）
       * 死点留在原地会一直赢过新点：实测 seed 图里 b0 near=43/0 next=43/0，
       * 人机认了个不可走的原生点，于是再也不动。这里把死点挪到地下 5000 m，
       * 索引和连接表都不动，只是不再参与就近查询（边早就清空了）。 */
      nav_pos(nd, &p);
      p.y -= NAV_DEAD_DY;
      nav_put_pos(nd, &p);
    }
  }
  /* 2) 新建点：AddNode 自己扩 nodes 数组、分配 nodeIndex、注册到每条 PathHandler */
  for (i = 0; i < g_nedN; i++) {
    NAVED* e = &g_ned[i];
    if (e->kind != NADD) continue;
    if (!nav_grow_node(g, &e->a)) { skipped++; continue; }
    made++;
  }
  if (!made && !keep) {
    elog("naved: grow WARNING: no 'node add' lines - this map now has 0 walkable nodes; "
         "bots will stand until the file has points");
  }
  /* 3) 查表树 + 边（边按坐标匹配，必须在点建完之后） */
  nav_refresh(g);
  ops = nav_apply_edges(g);
  ((void (*)(P, int, void*))RVA(R_PP_UNLOCK))(pp, lockId, 0);
  g_growGraph = g;
  g_growBase = n;
  g_growMade = made;
  /* 跳链放在解锁之后：建 GameObject / AddComponent 会触发 Unity 的 Awake，
   * 在 Lock 窗口里做等于把寻路线程和主线程对锁。 */
  ops += nav_apply_jumps(g);
  elog("naved: %s: %d native %s, %d new nodes, %d adds skipped, %d edges "
       "(graph %d -> %d nodes)", keep ? "keep" : "grow",
       keep ? n : killed, keep ? "kept" : "disabled", made, skipped, ops, n, nav_count(g));
  return made + ops;
}

/* 运行中加一个点：grow / keep 包里原生槽位全占着，借不到空槽，必须真·新建；
 * 其它情况（正式版 / 增量测试包）仍然借空槽位。返回 nodeIndex，失败 -1。
 * 2026-11-26：借不到就明确拒绝（不偷偷切 keep、不越权新建）——
 * 但**必须在屏幕上说清楚为什么**（以前只有控制台日志，菜单里按 5 看着像没反应）。 */
static int nav_add_live(P g, const V3* p) {
  P pp, nd;
  int lockId, idx;
  if (g_nedGrow && g_packName[0] && nav_grow_enabled()) {
    pp = nav_pp();
    if (!pp) { toast_bad("加点失败：寻路还没就绪，等一秒再试"); return -1; }
    lockId = ((int (*)(P, int, void*))RVA(R_PP_LOCK))(pp, 1, 0);
    nd = nav_grow_node(g, p);
    ((void (*)(P, int, void*))RVA(R_PP_UNLOCK))(pp, lockId, 0);
    if (!nd) { toast_bad("加点失败：AddNode 没成功（看游戏日志）"); return -1; }
    if (g == g_growGraph) g_growMade++;   /* 让「同一张图只新建一次」的判据继续成立 */
    return *(int*)((char*)nd + 0x8);
  }
  idx = nav_add_node(g, p);
  if (idx >= 0) return idx;
  /* 借不到空槽位：屏幕中央说明原因 + 怎么办 */
  if (!g_nedPath[0] || !g_packName[0])
    toast_bad("加不了点：本图没有空槽位，也没有可写的点图草稿（测试包是别的图的）");
  else
    toast_bad("本图 %d 个点全都可走、没有空槽位：先删一个点，或用 keep 测试包",
               nav_count(g));
  return -1;
}
static int nav_apply_core(P g) {
  int i, n, kill = 0, revived = 0, skipped = 0, moved = 0, ok = 0;
  if (!g) return 0;
  n = nav_count(g);
  if (n <= 0) { elog("naved: graph is empty (0 nodes), nothing to edit"); return 0; }
  if (n > NAV_MAXN) { elog("naved: graph too big (%d > %d), skipped", n, NAV_MAXN); return 0; }
  memset(g_navDead, 0, (size_t)n);
  g_navDeadN = n;
  /* 1) 删点：只标不可走 */
  for (i = 0; i < g_nedN; i++) {
    NAVED* e = &g_ned[i];
    int k;
    if (e->kind != NDEL) continue;
    k = nav_find_any(g, &e->a, 0.35f);
    if (k >= 0 && k < n && !g_navDead[k]) { g_navDead[k] = 1; kill++; ok++; }
  }
  if (kill) {
    /* 2) 活点：摘掉指向死点的边（每点最多重分配一次连接表）。 */
    for (i = 0; i < n; i++) {
      P nd;
      if (g_navDead[i]) continue;
      nd = nav_node(g, i);
      if (nd) nav_conn_filter_dead(nd);
    }
    /* 3) 死点置不可走 + 挪到地下 5000 m。
     *    连接表保留（带野指针的 bot 指过来也不会越界），但**位置必须挪走**：
     *    游戏用 AstarPath.GetNearest(pos)（NNConstraint.None，不看可走性）取脚下最近节点，
     *    死点留在原地就会一直抢走人机的起点（2026-11-20 grow 实测 near=43/0，人机全程站桩）。
     *    被 node add 借回去的槽位会重新写坐标，所以借点/撤销都不受影响。 */
    for (i = 0; i < n; i++) {
      P nd;
      V3 p;
      if (!g_navDead[i]) continue;
      nd = nav_node(g, i);
      if (!nd) continue;
      nav_set_walk(nd, 0);
      nav_pos(nd, &p);
      p.y -= NAV_DEAD_DY;
      nav_put_pos(nd, &p);
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
  /* 5) 贴地（会话级）：按新坐标把点摆回去。重套（图被游戏重扫）后位置不能丢，
   *    否则撤销栈里的贴地记录和图上对不上。 */
  for (i = 0; i < g_nedN; i++) {
    NAVED* e = &g_ned[i];
    int k;
    if (e->kind != NMOVE) continue;
    k = nav_find_any(g, &e->b, 0.35f);
    if (k < 0) k = nav_find_any(g, &e->a, 0.35f);
    if (k < 0) continue;
    nav_put_pos(nav_node(g, k), &e->b);
    moved++;
  }
  if (!kill && !revived && !moved) return nav_apply_edges(g);   /* 只是连边/断边 */
  nav_refresh(g);
  ok += nav_apply_edges(g);
  elog("naved: applied in place: %d disabled, %d revived, %d moved, %d adds skipped (graph stays %d nodes)",
       kill, revived, moved, skipped, n);
  return ok;
}
/* 把清单套到活图上；返回实际生效条数 */
static int nav_apply_all(P g) {
  int ok;
  if (g_nedGrow && g_packName[0]) {
    /* 空白地图 / 原版+新增都走 AddNode。借槽位那套已经删掉，所以 UCF_NAVGROW=0
     * 只剩「整包先不套用」这一种含义（按增量套会把原生点当成活的，结果更怪）。 */
    if (!nav_grow_enabled()) {
      elog("naved: grow/keep disabled by UCF_NAVGROW=0; pack not applied");
      g_nedExpect = nav_count(g);
      return 0;
    }
    ok = nav_apply_grow(g);
    if (ok < 0) return ok;            /* grow 还没就绪：本帧不标记已套用 */
  } else {
    ok = nav_apply_core(g);
    /* 正式版 / 增量包也要建 jump add：以前只有 grow 包走 nav_apply_jumps，
     * 在 ③ 正式图里加好的跳点重进图就不见了。内部按坐标去重，重套只补新建的。 */
    ok += nav_apply_jumps(g);
  }
  g_nedExpect = nav_count(g);
  return ok;
}
/* ======================= 撤销 / 重做（2026-11-26 重写）=======================
 * 老实现是「栈顶一条 = 一步」，而且好几类动作根本没进栈：
 *   1) 加点时若已选中 A，会顺手连一条边 = 两条记录，按一次撤销只撤一半；
 *   2) 跳点一次压三条（落点 / A->B 边 / jump add），jump add 那条干脆没有可见效果，
 *      按下去像「撤销坏了」；
 *   3) 删掉「本次会话里加的点」时走 nav_drop_add 把记录直接摘掉，什么都不压 ——
 *      撤销就弹到更早的一步去撤别的，删掉的点永远回不来（用户实测就是这个）；
 *   4) 删点撤销只把点放回来，nav_kill_node 摘掉的连线不恢复（点回来、线全没了）；
 *   5) 贴地（nav_ground_here）完全不记录。
 * 现在：按「用户动作」分组（NAVED.grp），一次动作整组反做，并且每条都如实报告
 * 「到底有没有在图上生效」，不再静默出栈、不再假装成功。 */
static int nav_drop_add(const V3* p);          /* 定义在下面 */

/* 跳链组件不会自己消失：撤销跳点必须真把场景里那条 Bot_JumpLink 删掉，
 * 否则按撤销什么都不会变。按起跳点坐标找到标记，走 del_index 同一套清理
 * （linkDic 反登记 + Destroy），但不碰点图清单（调用者正在处理 JADD 条目）。 */
static int mk_kill_jump(const V3* takeoff, const V3* landing) {
  int i;
  for (i = 0; i < g_n; i++) {
    if (g_mk[i].type != MT_JUMP) continue;
    if (nav_d2(&g_mk[i].p, takeoff) > 0.0025f) continue;
    del_index_ex(i, 0);
    jump_unsee(takeoff, landing);
    elog("naved: undo jump: 跳链已销毁（起跳点 %.2f %.2f %.2f）",
         takeoff->x, takeoff->y, takeoff->z);
    return 1;
  }
  elog("naved: undo jump: 场景里没有这条跳链（可能已经删过）");
  return 0;
}

/* 菜单里显示「最近一步是什么」 */
static void nav_ed_desc(const NAVED* e, char* out, int cap) {
  const char* dirn = "";
  if (!out || cap <= 0) return;
  if (!e) { snprintf(out, (size_t)cap, "（点图没有可撤销的编辑）"); return; }
  if (e->dir == 1) dirn = " 单向A->B";
  else if (e->dir == 2) dirn = " 单向B->A";
  switch (e->kind) {
    case NADD:    snprintf(out, (size_t)cap, "加点 (%.1f %.1f %.1f)", e->a.x, e->a.y, e->a.z); break;
    case NDEL:    snprintf(out, (size_t)cap, "删点 (%.1f %.1f %.1f)", e->a.x, e->a.y, e->a.z); break;
    case NMOVE:   snprintf(out, (size_t)cap, "贴地 y %.1f -> %.1f", e->a.y, e->b.y); break;
    case NPOPADD: snprintf(out, (size_t)cap, "删掉自己加的点 (%.1f %.1f %.1f)", e->a.x, e->a.y, e->a.z); break;
    case JADD:    snprintf(out, (size_t)cap, "跳点 (%.1f %.1f %.1f)->(%.1f %.1f %.1f)",
                           e->a.x, e->a.y, e->a.z, e->b.x, e->b.y, e->b.z); break;
    case EADD:    snprintf(out, (size_t)cap, "连边%s", dirn); break;
    default:      snprintf(out, (size_t)cap, "断边%s", dirn); break;
  }
}

/* 反做一条。返回 1 = 图上确实变了（0 = 这条本来就没东西可反做，要如实说）。 */
static int nav_undo_one(P g, NAVED* e) {
  int ia;
  switch (e->kind) {
    case NADD:
      ia = nav_find(g, &e->a, 0.35f);
      if (ia < 0) {
        elog("naved: undo add: 图上没有这个可走点 (%.2f %.2f %.2f)，跳过",
             e->a.x, e->a.y, e->a.z);
        return 0;
      }
      nav_kill_node(g, nav_node(g, ia));
      return 1;
    case NDEL:
      /* 死点被挪到地下（可能挪过不止一次）：按整数倍高度把原来那个槽位找回来，
       * 再把它自己的连线从底图快照搬回来，最后用清单里剩下的边记录校正一遍。 */
      ia = nav_find_dead_at(g, &e->a);
      if (ia < 0) {
        ia = nav_add_node(g, &e->a);
        if (ia < 0) { elog("naved: undo del: 找不到原点，也没有空槽位可用，跳过"); return 0; }
        elog("naved: undo del: 原点不在图上，按坐标补了一个空点（原来的连线找不回来）");
        return 1;
      }
      nav_put_pos(nav_node(g, ia), &e->a);
      nav_set_walk(nav_node(g, ia), 1);
      if (nav_base_restore_conns(g, ia)) nav_apply_edges(g);
      else elog("naved: undo del: 没有底图快照，只把点放回来（连线要自己重连）");
      return 1;
    case NMOVE:
      ia = nav_find_any(g, &e->b, 0.35f);
      if (ia < 0) ia = nav_find_any(g, &e->a, 0.35f);
      if (ia < 0) { elog("naved: undo move: 找不到被贴地的点，跳过"); return 0; }
      nav_put_pos(nav_node(g, ia), &e->a);
      return 1;
    case NPOPADD:
      ia = nav_find_dead_at(g, &e->a);
      if (ia < 0) ia = nav_add_node(g, &e->a);
      if (ia < 0) { elog("naved: undo del-added: 补不回这个点（没有空槽位）"); return 0; }
      nav_put_pos(nav_node(g, ia), &e->a);
      nav_set_walk(nav_node(g, ia), 1);
      {
        /* 把删点时摘掉的 node add / 边条目补回清单（顺序照旧） */
        int d = e->dir, k;
        NAVDROP* dp = (d >= 0 && d < NAVDROP_MAX && g_drop[d].step == e->grp) ? &g_drop[d] : 0;
        if (dp) {
          for (k = 0; k < dp->n; k++)
            if (g_nedN < NAV_ED_MAX) g_ned[g_nedN++] = dp->e[k];
        } else {
          elog("naved: undo del-added: 摘掉的条目已过期，只把点放回来");
        }
      }
      return 1;
    case JADD:
      return mk_kill_jump(&e->a, &e->b);
    default:                       /* EADD / EDEL */
      if (!nav_conn_apply(g, e, e->kind == EDEL)) {
        elog("naved: undo edge: 端点已经不在图上（或这条边本来就是这个状态），跳过");
        return 0;
      }
      return 1;
  }
}

/* 再做一遍（重做）。返回 1 = 图上确实变了。 */
static int nav_redo_one(P g, NAVED* e) {
  int ia;
  switch (e->kind) {
    case NADD:
      ia = nav_add_live(g, &e->a);
      if (ia < 0) { elog("naved: redo add: 加点失败（没有空槽位）"); return 0; }
      return 1;
    case NDEL:
      ia = nav_find(g, &e->a, 0.35f);
      if (ia < 0) { elog("naved: redo del: 图上没有这个可走点，跳过"); return 0; }
      nav_kill_node(g, nav_node(g, ia));
      return 1;
    case NMOVE:
      ia = nav_find_any(g, &e->a, 0.35f);
      if (ia < 0) ia = nav_find_any(g, &e->b, 0.35f);
      if (ia < 0) { elog("naved: redo move: 找不到点，跳过"); return 0; }
      nav_put_pos(nav_node(g, ia), &e->b);
      return 1;
    case NPOPADD:
      ia = nav_find(g, &e->a, 0.35f);
      if (ia < 0) { elog("naved: redo del-added: 图上没有这个点，跳过"); return 0; }
      nav_kill_node(g, nav_node(g, ia));
      if (nav_drop_add(&e->a)) {         /* 再摘一遍清单，重新记槽位（撤销还要用） */
        int d = g_dropNext;
        g_dropNext = (g_dropNext + 1) % NAVDROP_MAX;
        g_drop[d] = g_lastDrop;
        g_drop[d].step = e->grp;
        e->dir = d;
      }
      return 1;
    case JADD:
      if (jump_seen(&e->a, &e->b)) return 1;
      return make_jump_link_ex(e->a, e->b, e->jspeed, e->jacc, e->jdir) ? 1 : 0;
    default:                       /* EADD / EDEL */
      if (!nav_conn_apply(g, e, e->kind == EADD)) {
        elog("naved: redo edge: 端点已经不在图上，跳过");
        return 0;
      }
      return 1;
  }
}

/* 撤销：一次「用户动作」整组反做（同 grp 的连续条目）。 */
static void nav_undo(void) {
  P g = navfix_point_graph();
  int n = 0, changed = 0, grp;
  char desc[128];
  if (!g || !g_nedN) {
    wp_hint("撤销：点图没有可撤销的编辑");
    elog("naved: nothing to undo");
    return;
  }
  grp = g_ned[g_nedN - 1].grp;
  nav_ed_desc(&g_ned[g_nedN - 1], desc, sizeof desc);
  while (g_nedN > 0 && n < 128) {
    NAVED* e = &g_ned[g_nedN - 1];
    NAVED rec;
    if (grp > 0 && e->grp != grp) break;
    rec = *e;
    g_nedN--;                 /* 先出栈：反做时可能要往清单里补回条目 */
    if (nav_undo_one(g, &rec)) changed++;
    if (g_redoN < NAV_ED_MAX) g_redo[g_redoN++] = rec;
    n++;
    if (grp <= 0) break;      /* 读盘的旧条目没有步号：一次只撤一条 */
  }
  nav_refresh(g);
  editor_dirty_nav();         /* 手动保存：Ctrl+S 才写 <指纹>.txt */
  wp_hint("撤销 %d 条（%s）：%s", n, desc, changed ? "已生效" : "图上没有可反做的变化");
  if (changed) toast_ok("已撤销 %d 条：%s", n, desc);
  else toast_bad("撤销了 %d 条，但图上没有变化（%s）", n, desc);
  elog("naved: undo %d edit(s), %d applied, %d left (redo=%d) 未保存（Ctrl+S）",
       n, changed, g_nedN, g_redoN);
}

/* 重做：按撤销时记下的顺序整组再做一遍。 */
static void nav_redo(void) {
  P g = navfix_point_graph();
  int n = 0, changed = 0, grp;
  char desc[128];
  if (!g || !g_redoN) { wp_hint("恢复：没有可恢复的编辑"); elog("naved: nothing to redo"); return; }
  grp = g_redo[g_redoN - 1].grp;
  nav_ed_desc(&g_redo[g_redoN - 1], desc, sizeof desc);
  while (g_redoN > 0 && n < 128) {
    NAVED e;
    if (grp > 0 && g_redo[g_redoN - 1].grp != grp) break;
    e = g_redo[g_redoN - 1];
    g_redoN--;
    if (nav_redo_one(g, &e)) changed++;
    if (g_nedN < NAV_ED_MAX) g_ned[g_nedN++] = e;
    n++;
    if (grp <= 0) break;
  }
  nav_refresh(g);
  editor_dirty_nav();         /* 手动保存：Ctrl+S 才写 <指纹>.txt */
  wp_hint("恢复 %d 条（%s）：%s", n, desc, changed ? "已生效" : "图上没有可恢复的变化");
  if (changed) toast_ok("已重做 %d 条：%s", n, desc);
  else toast_bad("重做了 %d 条，但图上没有变化（%s）", n, desc);
  elog("naved: redo %d edit(s), %d applied, %d left (redo=%d) 未保存（Ctrl+S）",
       n, changed, g_nedN, g_redoN);
}

/* ======================= 标记 / 出生点撤销（2026-11-26）=======================
 * 记录在 mke_note_* 里（del_index_ex / spawn_add_point / editor_spawn_delete /
 * wp_place / 守卫区工具 调用），反做在 mke_undo_one / mke_redo_one 里。
 * 重建走 load_file 同一套 make_*，所以和重进图读 markers.txt 的结果一致。 */
static void mke_push(const MKE* src) {
  MKE* m;
  if (g_mkeMute || !src) return;
  if (g_mkeN >= MKE_MAX) {              /* 满了丢最老的：保证最近的动作能撤 */
    memmove(g_mke, g_mke + 1, sizeof(MKE) * (MKE_MAX - 1));
    g_mkeN = MKE_MAX - 1;
  }
  m = &g_mke[g_mkeN++];
  *m = *src;
  m->step = g_edStep;
  g_mkeRedoN = 0;
  g_redoN = 0;                          /* 新动作：两套重做栈一起作废 */
}
/* 【first, g_n) 是这次动作新建出来的标记（守卫点没现成区时会一次建 2 个） */
static void mke_note_add(int first) {
  int i;
  if (g_mkeMute) return;
  for (i = first; i < g_n; i++) {
    MK* mk = &g_mk[i];
    MKE e;
    if (mk->type == MT_JUMP) continue;  /* 跳点由点图 jump add 那条负责撤销 */
    memset(&e, 0, sizeof e);
    e.kind = MKE_ADD;
    e.type = mk->type;
    e.p = mk->p; e.aid = mk->aid; e.parent = mk->parent; e.prm = mk->prm;
    e.yaw = mk->yaw;                    /* 蹲守点 / 守卫点：撤销重建时朝向要一起回来 */
    mke_push(&e);
  }
}
static void mke_note_del(const MK* mk, const NAVED* jump) {
  MKE e;
  if (g_mkeMute || !mk) return;
  memset(&e, 0, sizeof e);
  e.kind = MKE_DEL;
  e.type = mk->type;
  e.p = mk->p; e.aid = mk->aid; e.parent = mk->parent; e.prm = mk->prm;
  if (mk->type == MT_JUMP && jump) {    /* 删跳链时清单里的 jump add 被摘掉了 */
    e.b = jump->b;
    e.jspeed = jump->jspeed; e.jacc = jump->jacc; e.jdir = jump->jdir;
  }
  mke_push(&e);
}
/* 出生点队号 <-> 撤销记录里的类型（team 2 = 中立） */
static int spawn_mt_of_team(int team) {
  if (team == 1) return MT_SPAWN_GR;
  if (team == 2) return MT_SPAWN_NT;
  return MT_SPAWN_BL;
}
static int spawn_team_of_mt(int t) {
  if (t == MT_SPAWN_GR) return 1;
  if (t == MT_SPAWN_NT) return 2;
  return 0;
}
static void mke_note_spawn_add(int team, const SPT* s, int idx) {
  MKE e;
  if (g_mkeMute || !s) return;
  memset(&e, 0, sizeof e);
  e.kind = MKE_ADD;
  e.type = spawn_mt_of_team(team);
  e.p = s->p; e.yaw = s->yaw; e.spawnIdx = idx;
  mke_push(&e);
}
static void mke_note_spawn_del(int team, const SPT* s, int wasAdd, int idx) {
  MKE e;
  if (g_mkeMute || !s) return;
  memset(&e, 0, sizeof e);
  e.kind = MKE_DEL;
  e.type = spawn_mt_of_team(team);
  e.p = s->p; e.yaw = s->yaw; e.wasAdd = wasAdd; e.spawnIdx = idx;
  mke_push(&e);
}
/* 出生点：新增清单的下标 / 摘除 / 插入 / 删除清单同上 */
static int spawn_add_index(int team, const V3* p) {
  int i;
  for (i = 0; i < g_spawnAddN[team]; i++)
    if (nav_d2(&g_spawnAdd[team][i].p, p) < 0.0025f) return i;
  return -1;
}
static void spawn_add_remove(int team, int k) {
  int i;
  if (k < 0 || k >= g_spawnAddN[team]) return;
  for (i = k; i < g_spawnAddN[team] - 1; i++) g_spawnAdd[team][i] = g_spawnAdd[team][i + 1];
  g_spawnAddN[team]--;
}
static void spawn_add_insert(int team, int k, const V3* p, float yaw) {
  int i;
  if (g_spawnAddN[team] >= MAX_SPAWN_EDIT) return;
  if (k < 0 || k > g_spawnAddN[team]) k = g_spawnAddN[team];
  for (i = g_spawnAddN[team]; i > k; i--) g_spawnAdd[team][i] = g_spawnAdd[team][i - 1];
  g_spawnAdd[team][k].p = *p;
  g_spawnAdd[team][k].yaw = yaw;
  g_spawnAddN[team]++;
}
static int spawn_del_index(int team, const V3* p) {
  int i;
  for (i = 0; i < g_spawnDelN[team]; i++)
    if (nav_d2(&g_spawnDel[team][i].p, p) < 0.0025f) return i;
  return -1;
}
static void spawn_del_remove(int team, int k) {
  int i;
  if (k < 0 || k >= g_spawnDelN[team]) return;
  for (i = k; i < g_spawnDelN[team] - 1; i++) g_spawnDel[team][i] = g_spawnDel[team][i + 1];
  g_spawnDelN[team]--;
}
static void spawn_del_append(int team, const V3* p) {
  SPT* s;
  if (g_spawnDelN[team] >= MAX_SPAWN_EDIT) return;
  s = &g_spawnDel[team][g_spawnDelN[team]++];
  memset(s, 0, sizeof *s);
  s->p = *p;
}
/* 按类型 + 坐标找标记（数组下标会随删除左移，不能存下标） */
static int mk_find(int type, const V3* p) {
  int i;
  for (i = 0; i < g_n; i++) {
    if (g_mk[i].type != type) continue;
    if (nav_d2(&g_mk[i].p, p) > 0.0025f) continue;
    return i;
  }
  return -1;
}
/* 重建一个被删掉的标记。返回 1 = 建回来了。 */
static int mk_recreate(const MKE* e) {
  int savedTeam = g_team, ok = 0;
  switch (e->type) {
    case MT_CROUCH:
      g_team = e->prm ? 1 : 0;
      ok = make_crouch(e->p, e->yaw);
      g_team = savedTeam;
      break;
    case MT_TAG:
      make_tag(e->p, e->prm, 3.0f);
      ok = 1;
      break;
    case MT_AREA:
      ok = make_area_aid(e->prm, e->p, e->aid);
      break;
    case MT_NANOPOS:
      ok = make_nanopos(e->aid, e->p, e->prm, e->yaw);
      break;
    case MT_JUMP:
      /* 落点没记下来（这条跳链是套包时建的、清单里没有 jump add）：不能凭原点瞎建一个 */
      if (nav_d2(&e->b, &e->p) < 2.25f) {
        elog("mkundo: 这条跳链没有落点记录，重建跳过（重进图会按包文件重建）");
        return 0;
      }
      ok = make_jump_link_ex(e->p, e->b, e->jspeed, e->jacc, e->jdir) ? 1 : 0;
      if (ok) {
        /* 清单里也补回 jump add，重进图才会自动重建 */
        if (g_nedN < NAV_ED_MAX) {
          NAVED n;
          memset(&n, 0, sizeof n);
          n.kind = JADD; n.a = e->p; n.b = e->b;
          n.jspeed = e->jspeed; n.jacc = e->jacc; n.jdir = e->jdir;
          n.grp = e->step;
          g_ned[g_nedN++] = n;
        }
        if (g_jumpSeenN < JSEEN_MAX) {
          g_jumpSeenA[g_jumpSeenN] = e->p;
          g_jumpSeenB[g_jumpSeenN] = e->b;
          g_jumpSeenN++;
        }
      }
      break;
    default: break;
  }
  return ok;
}
static void mke_desc(const MKE* e, char* out, int cap) {
  const char* what = "";
  if (!out || cap <= 0) return;
  if (!e) { snprintf(out, (size_t)cap, "（没有可撤销的标记编辑）"); return; }
  switch (e->type) {
    case MT_CROUCH:   what = "蹲守点"; break;
    case MT_NANOPOS:  what = "守卫点"; break;
    case MT_AREA:     what = "守卫区"; break;
    case MT_JUMP:     what = "跳链"; break;
    case MT_TAG:      what = "标签区"; break;
    case MT_SPAWN_BL: what = "出生点 BL"; break;
    case MT_SPAWN_GR: what = "出生点 GR"; break;
    case MT_SPAWN_NT: what = "出生点 中立"; break;
    default:          what = "标记"; break;
  }
  snprintf(out, (size_t)cap, "%s %s (%.1f %.1f %.1f)",
           e->kind == MKE_ADD ? "加" : "删", what, e->p.x, e->p.y, e->p.z);
}
static int mke_undo_one(const MKE* e) {
  int idx, ok = 0;
  g_mkeMute = 1;
  if (e->type == MT_SPAWN_BL || e->type == MT_SPAWN_GR || e->type == MT_SPAWN_NT) {
    int team = spawn_team_of_mt(e->type);
    if (e->kind == MKE_ADD) {
      idx = spawn_add_index(team, &e->p);
      if (idx >= 0) { spawn_add_remove(team, idx); ok = 1; }
    } else if (e->wasAdd) {
      spawn_add_insert(team, e->spawnIdx, &e->p, e->yaw);
      ok = 1;
    } else {
      idx = spawn_del_index(team, &e->p);
      if (idx >= 0) { spawn_del_remove(team, idx); ok = 1; }
    }
    if (ok) spawn_apply();
  } else if (e->kind == MKE_ADD) {
    idx = mk_find(e->type, &e->p);
    if (idx >= 0) { del_index_ex(idx, 1); ok = 1; }
  } else {
    ok = mk_recreate(e);
  }
  g_mkeMute = 0;
  return ok;
}
static int mke_redo_one(const MKE* e) {
  int idx, ok = 0;
  g_mkeMute = 1;
  if (e->type == MT_SPAWN_BL || e->type == MT_SPAWN_GR || e->type == MT_SPAWN_NT) {
    int team = spawn_team_of_mt(e->type);
    if (e->kind == MKE_ADD) {
      spawn_add_insert(team, -1, &e->p, e->yaw);
      ok = 1;
    } else if (e->wasAdd) {
      idx = spawn_add_index(team, &e->p);
      if (idx >= 0) { spawn_add_remove(team, idx); ok = 1; }
    } else {
      spawn_del_append(team, &e->p);
      ok = 1;
    }
    if (ok) spawn_apply();
  } else if (e->kind == MKE_ADD) {
    ok = mk_recreate(e);
  } else {
    idx = mk_find(e->type, &e->p);
    if (idx >= 0) { del_index_ex(idx, 1); ok = 1; }
  }
  g_mkeMute = 0;
  return ok;
}
/* 撤销/重做一组标记动作（同 step）。 */
static void mke_undo(void) {
  int n = 0, changed = 0, step;
  char desc[128];
  if (!g_mkeN) return;
  step = g_mke[g_mkeN - 1].step;
  mke_desc(&g_mke[g_mkeN - 1], desc, sizeof desc);
  while (g_mkeN > 0 && n < 64 && g_mke[g_mkeN - 1].step == step) {
    MKE e = g_mke[--g_mkeN];
    if (mke_undo_one(&e)) changed++;
    if (g_mkeRedoN < MKE_MAX) g_mkeRedo[g_mkeRedoN++] = e;
    n++;
  }
  if (changed) { editor_dirty_mk(); g_visDirty = 1; overlay_refresh(); }
  wp_hint("撤销 %d 个标记动作（%s）：%s", n, desc, changed ? "已生效" : "没有变化");
  if (changed) toast_ok("已撤销 %d 个标记动作：%s", n, desc);
  else toast_bad("撤销了 %d 个标记动作，但没有变化（%s）", n, desc);
  elog("mkundo: %d action(s), %d applied -> markers=%d 未保存（Ctrl+S）", n, changed, g_n);
}
static void mke_redo(void) {
  int n = 0, changed = 0, step;
  char desc[128];
  if (!g_mkeRedoN) return;
  step = g_mkeRedo[g_mkeRedoN - 1].step;
  mke_desc(&g_mkeRedo[g_mkeRedoN - 1], desc, sizeof desc);
  while (g_mkeRedoN > 0 && n < 64 && g_mkeRedo[g_mkeRedoN - 1].step == step) {
    MKE e = g_mkeRedo[--g_mkeRedoN];
    if (mke_redo_one(&e)) changed++;
    if (g_mkeN < MKE_MAX) g_mke[g_mkeN++] = e;
    n++;
  }
  if (changed) { editor_dirty_mk(); g_visDirty = 1; overlay_refresh(); }
  wp_hint("恢复 %d 个标记动作（%s）：%s", n, desc, changed ? "已生效" : "没有变化");
  if (changed) toast_ok("已重做 %d 个标记动作：%s", n, desc);
  else toast_bad("重做了 %d 个标记动作，但没有变化（%s）", n, desc);
  elog("mkredo: %d action(s), %d applied -> markers=%d 未保存（Ctrl+S）", n, changed, g_n);
}
/* ---- 统一入口：点图和标记共用一个步号，撤销永远反做「最近那一步」-------- */
static int ed_top_nav(void) { return g_nedN > 0 ? g_ned[g_nedN - 1].grp : -1; }
static int ed_top_mke(void) { return g_mkeN > 0 ? g_mke[g_mkeN - 1].step : -1; }
static void ed_undo(void) {
  if (!g_nedN && !g_mkeN) {
    wp_hint("撤销：没有可撤销的编辑");
    toast_bad("没有可撤销的编辑");
    elog("naved: nothing to undo");
    return;
  }
  if (ed_top_mke() > ed_top_nav()) mke_undo();
  else nav_undo();
}
static void ed_redo(void) {
  int a = g_redoN > 0 ? (g_redo[g_redoN - 1].grp > 0 ? g_redo[g_redoN - 1].grp : 0) : 0x7fffffff;
  int b = g_mkeRedoN > 0 ? g_mkeRedo[g_mkeRedoN - 1].step : 0x7fffffff;
  if (a == 0x7fffffff && b == 0x7fffffff) {
    wp_hint("恢复：没有可恢复的编辑");
    toast_bad("没有可重做的编辑");
    elog("naved: nothing to redo");
    return;
  }
  if (b < a) mke_redo();
  else nav_redo();
}

/* 删掉自己加的点时，把清单里对应的 node add / 相关边一起摘掉。
 * 否则重进图会先 node del 再 node add，点又活过来（空白底图尤其明显）。
 * 摘掉的条目同时抄进 g_lastDrop：以前只摘不记，用户按「撤销一步」会弹到更早的
 * 一步去撤别的，删掉的点永远回不来（2026-11-26 用户报的「撤销没撤回来」）。 */
static int nav_drop_add(const V3* p) {
  int i, j = 0, hit = 0;
  g_lastDrop.n = 0;
  g_lastDrop.step = g_edStep;
  for (i = 0; i < g_nedN; i++) {
    NAVED* e = &g_ned[i];
    int isAdd = (e->kind == NADD && nav_d2(&e->a, p) <= 0.0025f);
    int isEdge = (e->kind == EADD || e->kind == EDEL || e->kind == NMOVE) &&
                 (nav_d2(&e->a, p) <= 0.0025f || nav_d2(&e->b, p) <= 0.0025f);
    if (isAdd || isEdge) {
      if (isAdd) hit = 1;
      if (g_lastDrop.n < NAVDROP_SLOTS) g_lastDrop.e[g_lastDrop.n++] = *e;
      continue;
    }
    g_ned[j++] = *e;
  }
  g_nedN = j;
  return hit;
}
/* 删跳链：把点图日志里对应那条 jump add 摘掉，重进图 nav_apply_jumps 就不会再建。
 * 只按起点坐标匹配（jump add 的第一个点就是起跳点，标记 m.p 也是它）。 */
static int nav_drop_jump(const V3* takeoff) {
  int i, j = 0, hit = 0;
  memset(&g_lastJump, 0, sizeof g_lastJump);
  for (i = 0; i < g_nedN; i++) {
    NAVED* e = &g_ned[i];
    if (e->kind == JADD && nav_d2(&e->a, takeoff) <= 0.0025f) {
      if (!hit) g_lastJump = *e;      /* 撤销「删跳链」要把落点/参数带回来 */
      hit = 1;
      continue;
    }
    g_ned[j++] = *e;
  }
  if (!hit) return 0;
  g_nedN = j;
  editor_dirty_nav();         /* 2026-11-25：删跳链也只改内存，Ctrl+S 才落盘 */
  return 1;
}
/* 记录一条编辑：只改内存 / 当前图，Ctrl+S 才落盘（2026-11-25 用户要求） */
static void nav_push(int kind, const V3* a, const V3* b) {
  NAVED* e;
  if (g_nedN >= NAV_ED_MAX) { elog("naved: edit list full"); return; }
  e = &g_ned[g_nedN++];
  e->kind = kind;
  e->dir = 0;
  e->jct0 = -1.0f;
  e->jct1 = -1.0f;
  e->jctb = -1;                 /* 菜单里手建的跳链没有蹲信息 */
  e->a = *a;
  if (b) e->b = *b; else memset(&e->b, 0, sizeof(e->b));
  e->grp = g_edStep;
  g_redoN = 0;
  g_mkeRedoN = 0;             /* 有新的编辑动作：两套重做栈一起作废 */
  editor_dirty_nav();
}
static void nav_push_dir(int kind, const V3* a, const V3* b, int dir) {
  nav_push(kind, a, b);        /* 内部已 mark dirty；dir 补齐后不需要再存一次 */
  if (g_nedN > 0) g_ned[g_nedN - 1].dir = dir;
}
/* ---- 交互：加点 / 删点 / 连断边 / 选 A ---- */
/* 准星选点：按「路点到准星射线的垂直距离」挑，不再用「落点 3 m 内最近」。
 *
 * 旧做法先 cam_point() 拿到准星射线打中的那层表面，再找落点 3 m 内的路点。
 * 路点只要不在那一层表面上（台阶边缘、半空、跳点、隔一层楼、方块半嵌在墙里），
 * 落点就和方块差好几米 —— 表现出来就是「准星明明压在方块上却选不中，得把准星
 * 偏到旁边才对得上」。2026-11-26 的日志里连着 6 行 no node near crosshair
 * 就是这个：用户对着方块按了 6 次，第 7 次偏开才删掉。
 *
 * 容差 = 0.45 m + 2% 距离，上限 3 m。方块半边长 0.14 m：近处（3~10 m）大约是
 * 「方块周围 3~4 个方块半径」，远处再按 2% 放宽（60 m 时屏幕上还有 ~26 px 的可瞄
 * 范围，不会因为方块变小就选不中）。既跟手，也不会一按就抓到旁边的点。
 * nearIdx/nearPerp 即使没选中也带回最近的那颗，方便日志写清差多少。 */
static int nav_pick_ray(P g, const V3* o, const V3* d, int* nearIdx, float* nearPerp) {
  int i, best = -1, nbest = -1;
  float bestPerp = 1e9f, bestT = 1e9f;
  float nPerp = 1e9f;
  if (!g) return -1;
  for (i = 0; i < nav_count(g); i++) {
    P nd = nav_node(g, i);
    V3 q, v;
    float t, perp, tol;
    if (!nd || !nav_walk(nd)) continue;
    nav_pos(nd, &q);
    v.x = q.x - o->x; v.y = q.y - o->y; v.z = q.z - o->z;
    t = v.x * d->x + v.y * d->y + v.z * d->z;
    if (t < 0.25f) continue;                     /* 相机背后 / 贴脸：屏幕中心没意义 */
    perp = v.x * v.x + v.y * v.y + v.z * v.z - t * t;
    if (perp < 0.0f) perp = 0.0f;
    perp = sqrtf(perp);
    if (perp < nPerp) { nPerp = perp; nbest = i; }
    tol = 0.45f + 0.02f * t;
    if (tol > 3.0f) tol = 3.0f;
    if (perp > tol) continue;
    /* 同样贴住准星时取近的：一前一后两颗点叠在一起，选你看得见的那颗 */
    if (perp < bestPerp - 1e-4f || (perp <= bestPerp + 1e-4f && t < bestT)) {
      bestPerp = perp; bestT = t; best = i;
    }
  }
  if (nearIdx) *nearIdx = best >= 0 ? best : nbest;
  if (nearPerp) *nearPerp = best >= 0 ? bestPerp : nPerp;
  return best;
}

/* 按键选点（A / B / 删点 / 断边 / 贴地 / 跳点两端）：自己算一次准星射线，成功后
 * 顺手把「偏了多少」写进日志 —— 下次再有人反馈选不中，日志能直接看出差几米。 */
static int nav_pick_menu(const char* who, const char* failMsg) {
  V3 o, d;
  int i, nr = -1;               /* 别把变量叫 near：windef.h 里 near/far 是宏 */
  float perp = 0.0f;
  P g = navfix_point_graph();
  if (!g) { elog("%s: no point graph", who); toast_bad("这里没有点图（不在房间里？）"); return -1; }
  if (!cam_xray(&o, &d)) {
    elog("%s: no camera / no crosshair ray", who);
    toast_bad("取不到准星射线（相机没就绪）");
    return -1;
  }
  i = nav_pick_ray(g, &o, &d, &nr, &perp);
  if (i < 0) {
    elog("%s: 准星没压住路点（最近 #%d 偏 %.2f m；屏幕中心射线和 forward 差 %.2f°）",
         who, nr, perp, g_xrAng);
    toast_bad("%s", failMsg ? failMsg : "准星没压住路点");
  } else {
    elog("%s: 准星选中 #%d（偏 %.2f m；屏幕中心射线和 forward 差 %.2f°）", who, i, perp, g_xrAng);
  }
  return i;
}

static void nav_sel_a(void) {
  P g = navfix_point_graph();
  int i;
  if (!g) { elog("naved: no point graph"); return; }
  i = nav_pick_menu("naved: A", "没选到 A：准星对准起点的方块再按 5");
  if (i < 0) return;
  nav_pos(nav_node(g, i), &g_nedA);
  g_nedHasA = 1;
  elog("naved: A selected idx=%d at %.2f %.2f %.2f", i, g_nedA.x, g_nedA.y, g_nedA.z);
}
static void nav_add_here(void) {
  P g = navfix_point_graph();
  V3 p;
  int idx, ia = -1;
  if (!g) return;
  if (!cam_point(&p)) {
    elog("naved: no ground under crosshair");
    toast_bad("准星下面没有地面，换个位置再放");
    return;
  }
  ed_step();                  /* 加点 + 自动连边算同一个动作，撤销一次全撤 */
  p.y += 0.05f;
  if (nav_find(g, &p, 0.4f) >= 0) {
    elog("naved: node already exists here");
    toast_bad("这里已经有一个路点了");
    return;
  }
  idx = nav_add_live(g, &p);
  if (idx < 0) { elog("naved: add node failed"); return; }   /* 原因已在屏幕上说明（nav_add_live） */
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
  if (g_nedHasA && ia >= 0) toast_ok("已放路点 #%d (%.1f %.1f %.1f)，并连到 A", idx, p.x, p.y, p.z);
  else toast_ok("已放路点 #%d (%.1f %.1f %.1f)", idx, p.x, p.y, p.z);
}
static void nav_del_here(void) {
  P g = navfix_point_graph();
  V3 q;
  int i;
  if (!g) { toast_bad("这里没有点图（不在房间里？）"); return; }
  i = nav_pick_menu("naved: 删点", "没删到：准星对准要删的路点方块再按 5");
  if (i < 0) return;
  ed_step();
  nav_pos(nav_node(g, i), &q);
  nav_kill_node(g, nav_node(g, i));
  if (!nav_drop_add(&q)) {
    nav_push(NDEL, &q, 0);
  } else {
    /* 删的是「本次会话里加的点」：清单里那条 node add（和相关边）已经摘掉。
     * 再压一条 NPOPADD（dir = 摘掉的条目在 g_drop 里的槽位），撤销时把点放回来、
     * 把条目补回清单 —— 以前这里什么都不压，用户按撤销只会弹到更早的一步。 */
    int d = g_dropNext;
    g_dropNext = (g_dropNext + 1) % NAVDROP_MAX;
    g_drop[d] = g_lastDrop;
    g_drop[d].step = g_edStep;
    nav_push(NPOPADD, &q, 0);
    if (g_nedN > 0) g_ned[g_nedN - 1].dir = d;
    elog("naved: 删掉的是自己加的点：%d 条记录已从清单摘掉（撤销可原样放回）", g_lastDrop.n);
  }
  nav_refresh(g);
  wp_hint("删点 (%.1f %.1f %.1f)：可撤销", q.x, q.y, q.z);
  toast_ok("已删路点 (%.1f %.1f %.1f)：可撤销", q.x, q.y, q.z);
  elog("naved: node disabled idx=%d at %.2f %.2f %.2f 未保存（Ctrl+S）", i, q.x, q.y, q.z);
}
/* 2026-11-26 用户要求：菜单里的「重读并套用」整项删除（不再需要）。
 * 想重读点图 / 切包，走控制台「重新应用 / 载入到游戏」（cmd=reload → nav_cmd_set_pack），
 * 那条路径连 markers.txt 一起重读。 */
/* ---- 菜单动作：断边 / 落地 / 单向连边 / 标签区 / 放置 ---- */
static void menu_refresh(void);
static void nav_unlink_here(void) {
  P g = navfix_point_graph();
  V3 p, nb[64];
  int i, n, cnt = 0;
  P c = 0;
  if (!g) { elog("wpmenu: no point graph"); toast_bad("这里没有点图（不在房间里？）"); return; }
  i = nav_pick_menu("wpmenu: 断边", "没断到：准星对准要断连线的路点方块");
  if (i < 0) return;
  ed_step();                  /* 一次「断边」= 一组撤销（一个点可能同时断好几条） */
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
  if (cnt <= 0) toast_bad("这个点本来就没有连线，没断到东西");
  else toast_ok("已断开 %d 条连线（可撤销）", cnt);
}

/* 只把点贴到地面（Y 对齐）；水平移动/写盘格式本轮不做。 */
static void nav_ground_here(void) {
  P g = navfix_point_graph();
  V3 p, q, ro, rd;
  int i, nr = -1;
  float perp = 0.0f;
  if (!g) { toast_bad("这里没有点图（不在房间里？）"); return; }
  if (!cam_point_ray(&q, &ro, &rd)) {
    elog("wpmenu: 贴地: 准星下没有地面");
    toast_bad("贴地失败：准星下面没有地面");
    return;
  }
  i = nav_pick_ray(g, &ro, &rd, &nr, &perp);
  if (i < 0) {
    elog("wpmenu: 贴地: 准星没压住路点（最近 #%d 偏 %.2f m）", nr, perp);
    toast_bad("贴地失败：准星对准要贴地的路点方块再按 5");
    return;
  }
  ed_step();                  /* 一次贴地 = 一步撤销（别和上一条编辑并成一组） */
  nav_pos(nav_node(g, i), &p);
  {
    /* 贴地以前完全不进撤销栈：按「撤销一步」会去撤上一条别的编辑，贴过的点不动。
     * 记成 NMOVE（a = 原坐标 / b = 新坐标，只在会话里，不落盘）。 */
    V3 oldp = p;
    p.y = q.y + 0.05f;
    if (fabsf(oldp.y - p.y) < 0.01f) {
      elog("wpmenu: node already at ground y=%.2f (no change)", p.y);
      toast_bad("这个点已经在地面高度了（y=%.1f），没有变化", p.y);
      return;
    }
    nav_put_pos(nav_node(g, i), &p);
    nav_push(NMOVE, &oldp, &p);
    wp_hint("贴地 y %.1f -> %.1f（会话级，不落盘）", oldp.y, p.y);
    nav_refresh(g);
    toast_ok("已贴地：y %.1f -> %.1f（会话级，Ctrl+S 不落盘）", oldp.y, p.y);
    elog("wpmenu: node grounded to y=%.2f (session only; 撤销可还原)", p.y);
  }
}

/* A 已选时，把 A 和准星点按 g_wpPath 连一条边。 */
static void nav_link_one(void) {
  P g = navfix_point_graph();
  V3 q;
  int i, ia;
  if (!g) { elog("wpmenu: no point graph"); toast_bad("这里没有点图（不在房间里？）"); return; }
  if (g_wpLinkStep == 1) {
    nav_sel_a();                       /* 成败都在里面弹字 */
    if (g_nedHasA) g_wpLinkStep = 2;
    elog("wpmenu: link step=%d A=%d", g_wpLinkStep, g_nedHasA);
    return;
  }
  if (!g_nedHasA) {
    elog("wpmenu: select A first");
    g_wpLinkStep = 1;
    toast_bad("先选 A：准星对准起点方块按 5");
    return;
  }
  i = nav_pick_menu("wpmenu: 连边 B", "没连上：准星对准 B 点的方块再按 5");
  if (i < 0) return;
  ia = nav_find(g, &g_nedA, 1.5f);
  if (ia < 0) {
    elog("wpmenu: A disappeared, select again");
    g_nedHasA = 0;
    g_wpLinkStep = 1;
    toast_bad("A 已经不在图上了，重新选一次 A");
    return;
  }
  if (ia == i) {
    elog("wpmenu: A 和准星是同一个点（自环跳过）；换个点继续，Esc 结束连线");
    toast_bad("A 和准星是同一个点：换个点再连");
    return;                         /* 保持连续连线，不要退回主菜单 */
  }
  nav_pos(nav_node(g, i), &q);
  ed_step();                  /* 一次「连一条边」= 一步撤销 */
  /* 注意：一次连边只压一条 EADD，和加点时自动连的边不同（那条在 nav_add_here 里同组）。 */
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
  {
    float d = sqrtf(nav_d2(&g_nedA, &q));
    const char* w = (g_wpPath == 1) ? "A→B 单向" : (g_wpPath == 2 ? "B→A 单向" : "双向");
    toast_ok("已连边 %s：%.1f m（A 已前进到终点）", w, d);
  }
  /* 2026-11-20 连续编辑：连完一条不退出连线模式，A 自动前进到刚落下的 B，
   * 接着点下一个就连 B->下一个（画折线不用重复选 A）；Esc 才结束，1-3 换方向。 */
  g_nedA = q;
  g_nedHasA = 1;
  g_wpLinkStep = 2;
  elog("wpmenu: A 前进到 (%.2f %.2f %.2f)；继续点下一个连边，Esc 结束", q.x, q.y, q.z);
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

/* =============== 预置预览（ghost）：准星处的虚线框 ===============
 * 需求（2026-11-20 用户）：菜单里选好类型后，先在准星落点画一个虚线框，
 * 表示「如果现在按下去，东西会放在这里」；已选 A 时再从 A 拉一条虚线到准星。
 * 位置满意才按小键盘 5 / 左键实体化。
 *
 * 实现取舍：
 *   - 虚线框尺寸对每种笔刷是固定的，所以网格只建一次缓存起来，每帧只改
 *     GameObject 的 position 和显隐 —— 不重建网格、不分配托管数组，没 GC 抖动；
 *   - 虚线 = 一串薄方块拼的边（bs_dash_line），材质直接用调色板槽位。
 *     不用透明材质：URP 下改透明要动 shader 关键字/渲染队列，换图后很容易
 *     退化成洋红（见 mat_reset 那段注释），而虚线本身已经够「虚」了；
 *   - A→准星 那条虚线用一串小方块沿直线摆开，不做旋转（省掉四元数/欧拉那套）。
 * ---------------------------------------------------------------------- */
#define GHOST_MAXDOT 24
static P g_ghostMesh[6];              /* 虚线框网格：按尺寸缓存，area/tag 共用 3 m */
static P g_ghostMeshDot;              /* 虚线点：小实心方块 */
static P g_ghostGo, g_ghostMf, g_ghostMr;   /* 准星处的虚线框 */
static P g_ghostDots[GHOST_MAXDOT];   /* A→准星 的虚线点 */
static P g_ghostDotMr[GHOST_MAXDOT];
static int g_ghostShown;
static V3  g_ghostPv;                 /* 本帧预置点（菜单里显示坐标用） */
static int g_ghostPvOk;
static int g_ghostValid;              /* 0 = 这个位置按下去会被拒绝（画灰框，菜单里提示） */
static int g_ghostPrev;               /* 1 = 这帧只是「守卫区工具」的落点预览：没开笔刷，按 5 才创建 */
static int g_ghostPvIdx = -1;         /* 预置点吸到的路点索引；-1 = 新点 / 没吸到 */

/* 2026-11-26 用户要求：「守卫区工具」里的「新建守卫区 / 加守卫点」以前点下去才知道
 * 落在哪（准星处直接创建，没有任何预览）。现在没按 5 之前先画同一个虚线框 ——
 * 只看位置，不创建、不进撤销栈、不动任何状态；按 5 才实体化。
 * 只在这两项的**选中行**上预览：挪到「入口 / 逃跑点」（还没接）就收起来，
 * 免得让人以为那一项也会建东西。 */
static int wp_guard_preview(void) {
  return g_wpMenuSub == 3 && (g_wpMenuSubSel == 0 || g_wpMenuSubSel == 1);
}

/* 2026-11-20 用户需求：连路点时看不出谁是起点、方向朝哪。
 *   - A 起点：绿色方块 + 细竖条，换位置跟着走；
 *   - 终点 B：准星框变红；单向时在落点端画橙色箭头；
 *   - 已建成的单向边：中线画小箭头（见 edge_arrow / vis_draw）。 */
static P g_aMarkMesh, g_aMarkGo;
static P g_ghostArrowMesh, g_ghostArrowGo;

/* 一段虚线：从 a 到 b，按 dash/gap 切开，每小段一个薄方块 */
static void bs_dash_line(V3 a, V3 b, float dash, float gap, float w) {
  V3 d;
  float len, step, t;
  d.x = b.x - a.x; d.y = b.y - a.y; d.z = b.z - a.z;
  len = sqrtf(d.x * d.x + d.y * d.y + d.z * d.z);
  if (len < 0.05f) { bs_line(a, b, w); return; }
  if (dash < 0.01f) dash = 0.01f;
  if (gap < 0.0f) gap = 0.0f;
  step = dash + gap;
  for (t = 0.0f; t < len - 0.001f; t += step) {
    float t0 = t, t1 = t + dash;
    V3 p0, p1;
    if (t1 > len) t1 = len;
    p0.x = a.x + d.x * (t0 / len); p0.y = a.y + d.y * (t0 / len); p0.z = a.z + d.z * (t0 / len);
    p1.x = a.x + d.x * (t1 / len); p1.y = a.y + d.y * (t1 / len); p1.z = a.z + d.z * (t1 / len);
    bs_line(p0, p1, w);
  }
}
/* 虚线长方体框（12 条边全虚线）：c = 中心，h = 半尺寸 */
static void bs_dash_box(V3 c, V3 h, float dash, float gap, float w) {
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
  for (i = 0; i < 12; i++) bs_dash_line(p[eg[i][0]], p[eg[i][1]], dash, gap, w);
}

/* 预置框多大：跟着「真正会被创建的东西」走，别凭感觉 */
static float ghost_size(int brush) {
  switch (brush) {
    case 1: return 0.60f;   /* 跳跃点：起点/落点框，比 0.28 的标记框大一圈才看得见 */
    case 2: return 0.50f;   /* 蹲守点（标记 0.24） */
    case 3: return 0.66f;   /* 守卫点（标记 0.32） */
    case 4: return 3.00f;   /* 守卫区：游戏里就是 3 m 的 BoxCollider */
    case 5: return 3.00f;   /* 标签区：make_tag 半径 3.0 m */
    default: return 0.30f;  /* 普通路点（标记 0.14） */
  }
}
/* 预置框用什么颜色槽：和实体标记/图层同一套调色板，看到什么颜色就是什么类型 */
static int ghost_slot(int brush) {
  switch (brush) {
    case 1: return 4;       /* 跳跃 = 青 */
    case 2: return 1;       /* 蹲守 = 琥珀 */
    case 3: return 2;       /* 守卫点 */
    case 4: return 3;       /* 守卫区 */
    case 5: return 6;       /* 标签区 */
    case 6: return 11;      /* 出生点 BL：和 read_spawns 的幽灵出生同色（蓝） */
    case 7: return 12;      /* 出生点 GR：和保卫者出生同色（红） */
    case 8: return 13;      /* 出生点 中立：和中立点同色（灰） */
    default: return 5;      /* 普通路点 */
  }
}
static int ghost_mesh_key(int brush) {
  if (brush < 0 || brush > 5) return 0;
  return brush == 5 ? 4 : brush;   /* 标签区复用守卫区那个 3 m 框 */
}
static P ghost_box_mesh(int brush) {
  int key = ghost_mesh_key(brush);
  float s = ghost_size(brush), dash, gap;
  V3 c, h;
  if (g_ghostMesh[key] && uobj_live(g_ghostMesh[key])) return g_ghostMesh[key];
  g_ghostMesh[key] = 0;
  if (!g_meshCls || !g_vec3Cls || !g_i32Cls || !x_array_new) return 0;
  dash = s / 6.0f;
  if (dash < 0.06f) dash = 0.06f;   /* 小框的虚线也得看得见 */
  gap = dash * 0.7f;
  bs_reset();
  h.x = s * 0.5f; h.y = h.x; h.z = h.x;
  c.x = 0.0f; c.y = h.y; c.z = 0.0f;   /* 贴地：框底正好落在准星落点上 */
  bs_dash_box(c, h, dash, gap, 0.012f + s * 0.008f);
  g_ghostMesh[key] = build_mesh();
  if (g_ghostMesh[key]) {
    root_put(g_ghostMesh[key]);     /* 网格只建一次：钉住，别让 GC 回收 */
    elog("ghost: mesh brush=%d size=%.2f verts=%d tris=%d", key, s, g_bNV, g_bNI / 3);
  }
  return g_ghostMesh[key];
}
static P ghost_dot_mesh(void) {
  V3 c = { 0.0f, 0.0f, 0.0f }, h = { 0.045f, 0.045f, 0.045f };
  if (g_ghostMeshDot && uobj_live(g_ghostMeshDot)) return g_ghostMeshDot;
  g_ghostMeshDot = 0;
  if (!g_meshCls || !g_vec3Cls || !g_i32Cls || !x_array_new) return 0;
  bs_reset();
  bs_solid(c, h);
  g_ghostMeshDot = build_mesh();
  if (g_ghostMeshDot) root_put(g_ghostMeshDot);
  return g_ghostMeshDot;
}
/* 建一个只挂网格的 GameObject（MeshFilter + MeshRenderer，关阴影，不参与碰撞：
 * new_go 出来的对象本来就没有 Collider）。mrOut 拿回渲染器，后面要换材质。 */
static P ghost_go_new(const char* name, P mesh, int slot, P* mrOut) {
  P go, mf, mr, mat;
  if (mrOut) *mrOut = 0;
  if (!mesh || !g_mfType || !g_mrType) return 0;
  mat = mat_for(slot);
  if (!mat_alive(mat)) return 0;
  go = new_go(name);
  if (!go) return 0;
  ((set_layer_t)RVA(R_SETLAYER))(go, 0, 0);
  mf = ((addcomp_t)RVA(R_ADDCOMP))(go, g_mfType, 0);
  mr = ((addcomp_t)RVA(R_ADDCOMP))(go, g_mrType, 0);
  if (!mf || !mr) { ((destroy_t)RVA(R_DESTROY))(go, 0); return 0; }
  ((mf_setmesh_t)RVA(R_MF_SETMESH))(mf, mesh, 0);
  ((set_shmat_t)RVA(R_REND_SETSM))(mr, mat, 0);
  ((set_int1_t)RVA(R_REND_SHADOW))(mr, 0, 0);
  root_put(go);
  if (mrOut) *mrOut = mr;
  return go;
}

/* 起点 A 的立体标记：绿色方块 + 一根细竖条（远处也看得见）。
 * 网格只建一次，之后每帧只改坐标/显隐。 */
static P a_mark_mesh(void) {
  V3 c, h;
  if (g_aMarkMesh && uobj_live(g_aMarkMesh)) return g_aMarkMesh;
  g_aMarkMesh = 0;
  if (!g_meshCls || !g_vec3Cls || !g_i32Cls || !x_array_new) return 0;
  bs_reset();
  c.x = 0.0f; c.y = 0.18f; c.z = 0.0f; h.x = 0.17f; h.y = 0.17f; h.z = 0.17f;
  bs_solid(c, h);
  c.x = 0.0f; c.y = 0.95f; c.z = 0.0f; h.x = 0.035f; h.y = 0.85f; h.z = 0.035f;
  bs_solid(c, h);
  g_aMarkMesh = build_mesh();
  if (g_aMarkMesh) root_put(g_aMarkMesh);
  return g_aMarkMesh;
}
static void a_mark_hide(void) {
  if (g_aMarkGo && uobj_live(g_aMarkGo))
    ((set_active_t)RVA(R_SETACTIVE))(g_aMarkGo, 0, 0);
}
static void a_mark_tick(void) {
  P mesh;
  V3 q;
  if (!g_nedHasA) { a_mark_hide(); return; }
  mesh = a_mark_mesh();
  if (!mesh) return;
  if (!g_aMarkGo || !uobj_live(g_aMarkGo)) {
    g_aMarkGo = ghost_go_new("UCF_AMark", mesh, 2, 0);   /* slot 2 = 绿 */
    if (!g_aMarkGo) return;
    elog("ghost: A 起点标记已创建（绿色方块 + 竖条）");
  }
  q = g_nedA;
  q.y += 0.02f;
  ((set_pos_t)RVA(R_SET_POS))(get_tr(g_aMarkGo), q, 0);
  ((set_active_t)RVA(R_SETACTIVE))(g_aMarkGo, 1, 0);
}

/* 方向箭头网格：本地 +Z 指向箭头前方（用 euler Y 转到实际方向，不用四元数） */
static P ghost_arrow_mesh(void) {
  V3 tip, l, r;
  if (g_ghostArrowMesh && uobj_live(g_ghostArrowMesh)) return g_ghostArrowMesh;
  g_ghostArrowMesh = 0;
  if (!g_meshCls || !g_vec3Cls || !g_i32Cls || !x_array_new) return 0;
  bs_reset();
  tip.x = 0.0f; tip.y = 0.0f; tip.z = 0.42f;
  l.x = -0.19f; l.y = 0.0f; l.z = 0.0f;
  r.x = 0.19f; r.y = 0.0f; r.z = 0.0f;
  bs_line(tip, l, 0.075f);
  bs_line(tip, r, 0.075f);
  g_ghostArrowMesh = build_mesh();
  if (g_ghostArrowMesh) root_put(g_ghostArrowMesh);
  return g_ghostArrowMesh;
}
static void ghost_arrow_hide(void) {
  if (g_ghostArrowGo && uobj_live(g_ghostArrowGo))
    ((set_active_t)RVA(R_SETACTIVE))(g_ghostArrowGo, 0, 0);
}
/* dirMode: 1 = A->B，2 = B->A（单向才有）。pos/hint 都按「箭头指向哪边」来摆。 */
static void ghost_arrow_tick(int dirMode, V3 from, V3 to) {
  P mesh;
  V3 d, q, e;
  float len;
  if (dirMode != 1 && dirMode != 2) { ghost_arrow_hide(); return; }
  d.x = to.x - from.x; d.y = to.y - from.y; d.z = to.z - from.z;
  len = sqrtf(d.x * d.x + d.y * d.y + d.z * d.z);
  if (len < 0.9f) { ghost_arrow_hide(); return; }   /* 太近：跳点和边都不允许 */
  d.x /= len; d.y /= len; d.z /= len;
  mesh = ghost_arrow_mesh();
  if (!mesh) { ghost_arrow_hide(); return; }
  if (!g_ghostArrowGo || !uobj_live(g_ghostArrowGo)) {
    g_ghostArrowGo = ghost_go_new("UCF_GhostArrow", mesh, 7, 0);   /* slot 7 = 橙 */
    if (!g_ghostArrowGo) return;
    elog("ghost: 方向箭头已创建（橙色，dirMode=%d）", dirMode);
  }
  if (dirMode == 1) {   /* A->B：箭头摆在落点前，指向落点 */
    q.x = to.x - d.x * 0.55f; q.y = to.y - d.y * 0.55f; q.z = to.z - d.z * 0.55f;
    e.x = 0.0f; e.y = atan2f(d.x, d.z) * 57.29578f; e.z = 0.0f;
  } else {              /* B->A：箭头摆在起点前，指回起点 */
    q.x = from.x + d.x * 0.55f; q.y = from.y + d.y * 0.55f; q.z = from.z + d.z * 0.55f;
    e.x = 0.0f; e.y = atan2f(-d.x, -d.z) * 57.29578f; e.z = 0.0f;
  }
  q.y += 0.12f;
  ((set_pos_t)RVA(R_SET_POS))(get_tr(g_ghostArrowGo), q, 0);
  ((set_pos_t)RVA(R_SET_EULER))(get_tr(g_ghostArrowGo), e, 0);
  ((set_active_t)RVA(R_SETACTIVE))(g_ghostArrowGo, 1, 0);
}

/* 放置预览的方向箭头（2026-11-27）：蹲守点 / 守卫点按 5 之前，先把
 * 「放下后人机朝哪看」画出来（朝向 = 当前相机朝向，和真正写进 zoomPos 的一致）。
 * 复用 A->B 那个橙色箭头网格（本地 +Z 指向前方），另开一个对象免得互相抢显隐。 */
static P g_dirGhostGo = 0;
static void ghost_dir_arrow_hide(void) {
  if (g_dirGhostGo && uobj_live(g_dirGhostGo)) ((set_active_t)RVA(R_SETACTIVE))(g_dirGhostGo, 0, 0);
}
static void ghost_dir_arrow_tick(V3 p, float yaw) {
  P mesh;
  V3 d, q, e;
  if (yaw <= YAW_NONE + 1.0f) { ghost_dir_arrow_hide(); return; }
  mesh = ghost_arrow_mesh();
  if (!mesh) { ghost_dir_arrow_hide(); return; }
  if (!g_dirGhostGo || !uobj_live(g_dirGhostGo)) {
    g_dirGhostGo = ghost_go_new("UCF_GhostDir", mesh, 7, 0);   /* slot 7 = 橙 */
    if (!g_dirGhostGo) return;
    elog("ghost: 朝向预览箭头已创建（橙色）");
  }
  dir_of_yaw(yaw, &d);
  q.x = p.x + d.x * 0.55f;
  q.y = p.y + 0.10f;
  q.z = p.z + d.z * 0.55f;
  e.x = 0.0f;
  e.y = atan2f(d.x, d.z) * 57.29578f;
  e.z = 0.0f;
  ((set_pos_t)RVA(R_SET_POS))(get_tr(g_dirGhostGo), q, 0);
  ((set_pos_t)RVA(R_SET_EULER))(get_tr(g_dirGhostGo), e, 0);
  ((set_active_t)RVA(R_SETACTIVE))(g_dirGhostGo, 1, 0);
}
/* 换图 / 退出时把预览全部丢掉（对象已经随场景销毁，网格缓存也要重来） */
static void ghost_reset(void) {
  int i;
  g_ghostGo = g_ghostMf = g_ghostMr = 0;
  for (i = 0; i < GHOST_MAXDOT; i++) { g_ghostDots[i] = 0; g_ghostDotMr[i] = 0; }
  for (i = 0; i < 6; i++) g_ghostMesh[i] = 0;
  g_ghostMeshDot = 0;
  g_ghostShown = 0;
  g_ghostPvOk = 0;
  g_ghostValid = 0;
  g_ghostPrev = 0;
  g_ghostPvIdx = -1;
  g_aMarkGo = g_aMarkMesh = 0;
  g_ghostArrowGo = g_ghostArrowMesh = 0;
  g_dirGhostGo = 0;
}
static void ghost_hide(void) {
  int i;
  if (g_ghostShown) {
    if (g_ghostGo && uobj_live(g_ghostGo))
      ((set_active_t)RVA(R_SETACTIVE))(g_ghostGo, 0, 0);
    for (i = 0; i < GHOST_MAXDOT; i++)
      if (g_ghostDots[i] && uobj_live(g_ghostDots[i]))
        ((set_active_t)RVA(R_SETACTIVE))(g_ghostDots[i], 0, 0);
  }
  g_ghostShown = 0;
  g_ghostPvOk = 0;
  g_ghostValid = 0;
  g_ghostPrev = 0;
  ghost_arrow_hide();
  ghost_dir_arrow_hide();
}

/* 每帧（主线程）：摆好虚线框 + A→准星 的虚线点 */
static void ghost_tick(void) {
  V3 p, from, ro, rd;
  P mesh, dot;
  int brush, line, i, ok = 1, needNode = 0, slot = 5, arrowMode = 0;
  int used = 0, preview = 0;
  static int uiTick;

  /* 除了「已开笔刷 / 正在连线」，菜单停在「守卫区工具」的选中行时也要画框（只预览） */
  if (!g_wpMenuOpen || (!g_wpArm && !g_wpLinkStep && !wp_guard_preview())) {
    ghost_hide();
    a_mark_hide();          /* A 标记只在编菜单里出现，关掉菜单就收起来 */
    return;
  }
  /* A 起点的绿标记先摆好：后面就算准星没打到地面（抬头看天）也留着 */
  a_mark_tick();
  if (!g_ghostGo || !uobj_live(g_ghostGo)) { g_ghostGo = g_ghostMf = g_ghostMr = 0; }
  if (!cam_point_ray(&p, &ro, &rd)) { ghost_hide(); return; }
  /* 没开笔刷却走到这里 = 「守卫区工具」的落点预览：尺寸/颜色按真会建的东西取 */
  preview = (!g_wpArm && !g_wpLinkStep);
  brush = preview ? (g_wpMenuSubSel == 0 ? 4 : 3) : (g_wpArm ? g_wpBrush : 0);
  if (brush < 0 || brush >= WP_BRUSH_N) brush = 0;

  /* 预置点必须和真正落点的规则一致，否则预览就是在骗人：
   *   跳跃起点 / 路径两端   必须是准星压住的路点（nav_pick_ray 和按键时同一个选点器，
   *                         wp_place / nav_link_one 也这么找）—— 2026-11-26 起不再看
   *                         「落点 3 m 内」，方块挂在哪层表面上都行；
   *   跳跃落点             准星压住的路点（不是起点）就用它，没有就按准星补一个；
   *   普通/蹲守/守卫点/守卫区/标签区  就是准星落点。
   * 准星没压住节点 / 离起点太近（<1.5 m）时画灰框（slot 13）：这一下按下去会被拒绝。 */
  ok = 1;
  needNode = 0;
  g_ghostPvIdx = -1;
  if (g_wpLinkStep == 1 || g_wpLinkStep == 2) needNode = 1;
  else if (g_wpArm && brush == 1 && !g_nedHasA) needNode = 1;
  if (needNode) {
    /* 和真正按下去用同一个选点器（准星射线）：预览绿了，按下去一定选中 */
    P g = navfix_point_graph();
    int ni = g ? nav_pick_ray(g, &ro, &rd, 0, 0) : -1;
    if (ni >= 0) { nav_pos(nav_node(g, ni), &p); g_ghostPvIdx = ni; }
    else ok = 0;
  } else if (g_wpArm && brush == 1 && g_nedHasA) {
    P g = navfix_point_graph();
    int nb = g ? nav_pick_ray(g, &ro, &rd, 0, 0) : -1;
    int na = g ? nav_find(g, &g_nedA, 0.6f) : -1;
    if (nb >= 0 && nb != na) { nav_pos(nav_node(g, nb), &p); g_ghostPvIdx = nb; }
    else if (nav_d2(&g_nedA, &p) < 2.25f) ok = 0;   /* 1.5 m：太近会「原地跳」 */
  }
  /* 2026-11-27：守卫点只挂在已有守卫区里（不再连带建区）。区外按 5 会被拒绝，
   * 预览框就照这个规则变灰（slot 13），别让虚线框看起来「按下去就能建」。 */
  if (ok && brush == 3 && area_at(&p) < 0) ok = 0;
  /* 颜色语义：这一步会变成「起点」就绿，会变成「终点」就红，其余按类型色。
   * （跳跃点两次点击也是先起点后落点，规则一样） */
  {
    int isStart = (g_wpLinkStep == 1) || (g_wpArm && brush == 1 && !g_nedHasA);
    int isEnd   = (g_wpLinkStep == 2) || (g_wpArm && brush == 1 && g_nedHasA);
    if (!ok) slot = 13;            /* 灰 = 这里按下去会被拒绝 */
    else if (isStart) slot = 2;    /* 起点绿 */
    else if (isEnd) slot = 12;     /* 终点红 */
    else slot = ghost_slot(brush);
  }

  /* A -> 预置点 的虚线什么时候画：
   *   跳跃点且 A 已选；或者「建立路径」已选 A 等 B（g_wpLinkStep==2）。 */
  line = 0;
  from.x = from.y = from.z = 0.0f;
  if (g_nedHasA && ((g_wpArm && brush == 1) || g_wpLinkStep == 2)) {
    line = 1;
    from = g_nedA;
  }
  /* 方向箭头：跳跃链接固定 A->B；建立路径按 g_wpPath（0 = 双向不画） */
  if (line) {
    if (g_wpLinkStep == 2) arrowMode = g_wpPath;
    else if (g_wpArm && brush == 1) arrowMode = 1;
  }

  /* 预览「按下去会建在哪」：menu_activate 里给守卫区/守卫点也是先 +0.05，跟着来。
   * 出生点例外：真正写进去的高度是"地面 + 原生高度"（spawn_fix_height），
   * 预览也按同一套摆，否则框在脚下、建出来却在半空。 */
  if (brush == MT_SPAWN_BL || brush == MT_SPAWN_GR || brush == MT_SPAWN_NT) {
    V3 g;
    if (ground_below(p, 1.0f, 40.0f, &g)) p.y = g.y + spawn_height_gap();
    else p.y += 0.05f;
  } else if (preview) {
    p.y += 0.05f;
  }
  p.y += 0.02f;   /* 抬高 2 cm：虚线和地面 z-fighting 会闪 */
  g_ghostPv = p;
  g_ghostPvOk = 1;
  g_ghostValid = ok;
  g_ghostPrev = preview;

  mesh = ghost_box_mesh(brush);
  if (!mesh) { ghost_hide(); return; }
  if (!g_ghostGo) {
    g_ghostGo = ghost_go_new("UCF_Ghost", mesh, slot, &g_ghostMr);
    if (!g_ghostGo) { ghost_hide(); return; }
    g_ghostMf = ((getcomp_t)RVA(R_GETCOMP))(g_ghostGo, g_mfType, 0);
  }
  if (g_ghostMf) ((mf_setmesh_t)RVA(R_MF_SETMESH))(g_ghostMf, mesh, 0);
  if (g_ghostMr) {
    P mat = mat_for(slot);
    if (mat_alive(mat)) ((set_shmat_t)RVA(R_REND_SETSM))(g_ghostMr, mat, 0);
  }
  /* 守卫区的 BoxCollider 是「以 transform 为中心」的 3 m 立方体（make_area 只改
   * scale、不改 offset）：预览框得按同样的中心摆，否则「框底贴地」看着对、建出来
   * 却是上下各伸 1.5 m，位置就骗人了。点位型（守卫点）沿用原来的「框底贴地」，
   * 和蹲守点 / 普通路点的预览一致。 */
  {
    V3 q = p;
    if (preview && brush == 4) q.y -= ghost_size(4) * 0.5f;
    ((set_pos_t)RVA(R_SET_POS))(get_tr(g_ghostGo), q, 0);
  }
  ((set_active_t)RVA(R_SETACTIVE))(g_ghostGo, 1, 0);
  g_ghostShown = 1;

  /* 终点方向箭头：只有单向（A->B / B->A）才画；位置不合法时也收起来 */
  if (line && ok) ghost_arrow_tick(arrowMode, from, p);
  else ghost_arrow_hide();
  /* 蹲守点 / 守卫点的朝向预览：放之前先看见「人机会朝哪看」（= 相机朝向） */
  if ((g_wpArm || preview) && (brush == 2 || brush == 3) && ok)
    ghost_dir_arrow_tick(p, cam_dir_yaw());
  else ghost_dir_arrow_hide();

  /* A -> 准星：等距一串小方块（不做旋转，省掉四元数那套） */
  if (line) {
    V3 d;
    float len;
    d.x = p.x - from.x; d.y = p.y - from.y; d.z = p.z - from.z;
    len = sqrtf(d.x * d.x + d.y * d.y + d.z * d.z);
    dot = (len > 0.4f) ? ghost_dot_mesh() : 0;
    if (dot) {
      int want = (int)(len / 0.55f) + 1;
      if (want > GHOST_MAXDOT) want = GHOST_MAXDOT;
      if (want < 2) want = 2;
      for (i = 1; i < want; i++) {
        float t = (float)i / (float)want;
        V3 q;
        q.x = from.x + d.x * t;
        q.y = from.y + d.y * t + 0.05f;
        q.z = from.z + d.z * t;
        if (!g_ghostDots[used] || !uobj_live(g_ghostDots[used])) {
          g_ghostDots[used] = ghost_go_new("UCF_GhostDot", dot, slot, &g_ghostDotMr[used]);
          if (!g_ghostDots[used]) break;
        }
        ((set_pos_t)RVA(R_SET_POS))(get_tr(g_ghostDots[used]), q, 0);
        ((set_active_t)RVA(R_SETACTIVE))(g_ghostDots[used], 1, 0);
        used++;
      }
    }
  }
  /* 虚线点的颜色跟着当前笔刷走（切类型时旧点是别的颜色，看着会串味） */
  if (used) {
    P mat = mat_for(slot);
    if (mat_alive(mat))
      for (i = 0; i < used; i++)
        if (g_ghostDotMr[i] && uobj_live(g_ghostDotMr[i]))
          ((set_shmat_t)RVA(R_REND_SETSM))(g_ghostDotMr[i], mat, 0);
  }
  for (i = used; i < GHOST_MAXDOT; i++)
    if (g_ghostDots[i] && uobj_live(g_ghostDots[i]))
      ((set_active_t)RVA(R_SETACTIVE))(g_ghostDots[i], 0, 0);

  /* 菜单里那行「预置点 (x y z)」要跟着准星走：文字是 UGUI，只在 ~5 Hz 刷 */
  if ((++uiTick % 12) == 0) menu_refresh();
}

/* 跳跃链接：Bot_JumpLink.Link[] 只有一个元素，endTransform 指向终点。
 * 2026-11-20 起可持久化：菜单里建一次会写 `jump add`，进图套包时 nav_apply_jumps 重建。 */
static int make_jump_link_ex(V3 a, V3 b, float jspeed, float jacc, int jdir) {
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
  *(float*)((char*)links + 0x18) = (jspeed < 0.0f) ? 0.0f : jspeed;   /* needSpeed */
  *(float*)((char*)links + 0x1C) = (jacc < 0.0f) ? 1.0f : jacc;       /* accuracy */
  /* direction：0 = 沿 A->B（原来的行为）/ 1 = 正上 / 2 = 前上（水平分量 + 抬升）
   * 2026-11-25 对照实验用：看游戏到底是拿这个方向做什么。 */
  if (jdir == 1) {
    *(float*)((char*)links + 0x20) = 0.0f;
    *(float*)((char*)links + 0x24) = 1.0f;
    *(float*)((char*)links + 0x28) = 0.0f;
  } else if (jdir == 2) {
    float hx = dx, hz = dz;
    float hl = sqrtf(hx * hx + hz * hz);
    float up = (dy > 0.0f ? dy : 1.0f) + 1.0f;
    float n2 = sqrtf(hl * hl + up * up);
    *(float*)((char*)links + 0x20) = (hl > 1e-5f) ? hx / hl * (hl / n2) : 0.0f;
    *(float*)((char*)links + 0x24) = (n2 > 1e-5f) ? up / n2 : 1.0f;
    *(float*)((char*)links + 0x28) = (hl > 1e-5f) ? hz / hl * (hl / n2) : 0.0f;
  } else {
    *(float*)((char*)links + 0x20) = dx / len;
    *(float*)((char*)links + 0x24) = dy / len;
    *(float*)((char*)links + 0x28) = dz / len;
  }
  *(P*)((char*)comp + 0x24) = links;               /* links */
  ((set_active_t)RVA(R_SETACTIVE))(startGo, 1, 0);

  method = x_class_get_method_from_name ? x_class_get_method_from_name(g_jumpCls, "OnLatePostScan", 0) : 0;
  if (method && x_runtime_invoke) {
    P startNode, endNode;
    x_runtime_invoke(method, comp, 0, 0);
    /* OnLatePostScan 会按坐标把两端挂到图上：Bot_JumpLink.<startNode> @0x20，
     * Link.endNode @0x14。读到空就是「最近节点没找到」，人机不会走这条跳链。 */
    startNode = *(P*)((char*)comp + 0x20);
    endNode = *(P*)((char*)links + 0x14);
    elog("wpmenu: jump link created start=(%.2f %.2f %.2f) end=(%.2f %.2f %.2f) "
         "needSpeed=%.1f accuracy=%.2f dir=%d method=%p startNode=%p endNode=%p",
         a.x, a.y, a.z, b.x, b.y, b.z,
         *(float*)((char*)links + 0x18), *(float*)((char*)links + 0x1C), jdir,
         method, startNode, endNode);
    if (!startNode || !endNode)
      elog("wpmenu: jump link NOT hooked (startNode=%p endNode=%p); 起点要落在已有路点附近",
           startNode, endNode);
    /* ---- 注册校验 / 自愈（2026-11-24 现场：路径下一个节点确实是 endNode，人机仍不跳）----
     * 人机在 OnPathComplete 里用的是 static Bot_JumpLink.GetLink(startNode, out link)，
     * 它查的是静态字典 linkDic；OnLatePostScan 只把 startNode/endNode 填上，
     * 字典里有没有这一条是另一回事。这里直接查一次，没有就手工登记。 */
    if (startNode) {
      P gm = x_class_get_method_from_name ? x_class_get_method_from_name(g_jumpCls, "GetLink", 2) : 0;
      if (gm && x_runtime_invoke) {
        void* args[2];
        P outLink = 0;
        args[0] = startNode;
        args[1] = &outLink;
        x_runtime_invoke(gm, 0, args, 0);
        elog("wpmenu: GetLink(startNode=%p) -> %s", startNode, outLink ? "YES" : "NO");
        if (!outLink) {
          P fld = x_class_get_field_from_name ? x_class_get_field_from_name(g_jumpCls, "linkDic") : 0;
          P ftype = (fld && x_field_get_type) ? x_field_get_type(fld) : 0;
          P dcls = (ftype && x_class_from_il2cpp_type) ? x_class_from_il2cpp_type(ftype) : 0;
          P dic = 0;
          P setItem = 0;
          if (fld && x_field_static_get_value) x_field_static_get_value(fld, &dic);
          if (dcls && x_class_get_method_from_name) setItem = x_class_get_method_from_name(dcls, "set_Item", 2);
          if (dic && setItem) {
            void* a2[2];
            a2[0] = startNode;
            a2[1] = comp;
            x_runtime_invoke(setItem, dic, a2, 0);
            outLink = 0;
            a2[0] = 0;
            args[0] = startNode;
            args[1] = &outLink;
            x_runtime_invoke(gm, 0, args, 0);
            elog("wpmenu: linkDic 手工登记 -> %s (dic=%p)",
                 outLink ? "OK（跳链现在能被 GetLink 查到）" : "FAILED", (void*)dic);
          } else {
            elog("wpmenu: linkDic 登记失败 (dic=%p cls=%p set_Item=%p)",
                 (void*)dic, (void*)dcls, (void*)setItem);
          }
        }
      } else {
        elog("wpmenu: GetLink 方法没找到 (%p)，没法校验注册", (void*)gm);
      }
    }
  } else {
    elog("wpmenu: jump component created but OnLatePostScan missing; link inactive");
  }
  if (h && x_gchandle_free) x_gchandle_free((P)h);
  add_mk(4, a, -1, -1, 0, startGo, comp, spawn_vis(a, 0.28f, 4));
  g_visDirty = 1;
  return 1;
}

static void wp_place(void) {
  V3 p, ro, rd;
  int n0;
  if (!cam_point_ray(&p, &ro, &rd)) {
    elog("wpmenu: no ground under crosshair");
    toast_bad("准星下面没有地面：对准地面 / 方块再按 5");
    return;
  }
  /* 2026-11-27（用户：「守卫点只是设立点」）：守卫点不再连带新建守卫区。
   * 以前落点不在任何 3 m 框里时会先 make_area 再 make_nanopos —— 一次点击在同一
   * 坐标冒出「区 + 点」两个物体，看上去就像「我加点，结果多出来一个区」。
   * 现在区外直接拒绝：不建、不进撤销栈、也不点亮 Ctrl+S 的「未保存」。 */
  if (g_wpBrush == 3 && area_at(&p) < 0) {
    elog("wpmenu: 准星不在任何守卫区里（%.2f %.2f %.2f）-> 不建守卫点；先「1 新建守卫区」",
         p.x, p.y, p.z);
    toast_bad("这里没有守卫区：先按 1 建区，再在区里加点");
    return;
  }
  ed_step();                  /* 一次放置 = 一步撤销（跳点 / 守卫区连带点位都算一组） */
  n0 = g_n;                   /* 这一手新建了哪些标记（撤销要能反做） */
  p.y += 0.05f;
  if (g_wpAutoGround) { /* cam_point already returns the ground point */ }
  switch (g_wpBrush) {
    case 0: nav_add_here(); break;
    case 1: {
      /* 跳跃点 = 两次点击，而且两端都必须是图上真实的路点。
       *
       * 游戏的判定（GameAssembly 反汇编：Bot.OnPathComplete + Bot_JumpLink.GetLink /
       * GetLinkEndByGraphNode）：遍历 A* 路径的节点序列，只有「路径里 起点节点 的下一个
       * 节点 正好就是这条跳链的 endNode」时才插跳跃段。也就是说
       *   ① 起点、落点都得分到图上的节点（linkDic 按起点节点登记，endNode 由落点最近节点解析）；
       *   ② 这两个节点之间必须有一条 A->B 的边，否则 A* 永远不会把它们连着排，跳链一次都不触发。
       * 所以这里：起点必须吸到路点；落点没有路点就顺手补一个；建完跳链再补 A->B 的单向边。 */
      P g = navfix_point_graph();
      int ia, ib;
      float len;
      V3 b;
      if (!g) { elog("wpmenu: jump: no point graph"); toast_bad("这里没有点图（不在房间里？）"); break; }
      if (!g_nedHasA) {
        ia = nav_pick_ray(g, &ro, &rd, 0, 0);
        if (ia < 0) {
          elog("wpmenu: jump start: 准星没压住路点（要压在方块上）；先在起跳处放一个普通路点再建跳链");
          toast_bad("起跳点要压在路点上：先在起跳处放一个普通路点");
          break;
        }
        nav_pos(nav_node(g, ia), &g_nedA);
        g_nedHasA = 1;
        elog("wpmenu: jump start = node idx=%d (%.2f %.2f %.2f); 对准落点再按 5",
             ia, g_nedA.x, g_nedA.y, g_nedA.z);
        {
          P c0 = 0;
          if (nav_conn_get(nav_node(g, ia), &c0) <= 0)
            elog("wpmenu: jump start node %d 一条边都没有，Bot 根本走不到它；先给它连边", ia);
        }
        break;
      }
      ia = nav_find(g, &g_nedA, 0.6f);
      if (ia < 0) {
        elog("wpmenu: jump start node lost (起点已不在图上); 重新选起点");
        g_nedHasA = 0;
        toast_bad("起点已经不在图上了，重新选起跳点");
        break;
      }
      ib = nav_pick_ray(g, &ro, &rd, 0, 0);
      if (ib >= 0 && ib != ia) {
        nav_pos(nav_node(g, ib), &b);          /* 落点已有路点：直接用它 */
      } else if (nav_d2(&g_nedA, &p) < 2.25f) {  /* 1.5^2 */
        elog("wpmenu: jump landing 离起点太近（<1.5 m）；跳链没意义，换个地方再按 5");
        toast_bad("落点离起跳点太近（<1.5 m）：换个地方再按 5");
        break;
      } else {
        /* 落点附近没有路点（或最近的点又是起点）：就地补一个落点路点。
         * 不补的话 endNode 会解析回起点，变成「原地跳」，永远不会触发。 */
        ib = nav_add_live(g, &p);
        if (ib < 0) { elog("wpmenu: jump landing: 新建落点路点失败"); break; }
        nav_push(NADD, &p, 0);
        nav_refresh(g);
        b = p;
        elog("wpmenu: jump landing: 新建路点 idx=%d (%.2f %.2f %.2f)", ib, b.x, b.y, b.z);
      }
      len = sqrtf(nav_d2(&g_nedA, &b));
      if (len < 1.5f) {
        elog("wpmenu: jump too short (%.2f m < 1.5); 换一个落点", len);
        toast_bad("跳点太短（%.2f m < 1.5 m）：换个落点", len);
        break;
      }
      if (!make_jump_link(g_nedA, b)) {
        toast_bad("跳链组件没建出来（看游戏日志）");
        break;
      }
      /* 跳链要能被用上，两点之间必须有 A->B 的边（见上面 ②） */
      ia = nav_find(g, &g_nedA, 0.6f);
      ib = nav_find(g, &b, 0.6f);
      if (ia >= 0 && ib >= 0 && ia != ib) {
        if (!nav_conn_has(nav_node(g, ia), nav_node(g, ib))) {
          nav_conn_set(nav_node(g, ia), nav_node(g, ib), 1);
          nav_push_dir(EADD, &g_nedA, &b, 1);   /* edge out：单向 A -> B */
          nav_refresh(g);
          elog("wpmenu: jump edge A->B added (idx %d -> %d)", ia, ib);
        }
        nav_push(JADD, &g_nedA, &b);            /* 落盘成 jump add，重进图自动重建 */
        elog("wpmenu: jump saved: node %d -> node %d (%.2f m)", ia, ib, len);
        toast_ok("跳点已建：%d → %d（%.1f m）", ia, ib, len);
        {
          /* 落点只有 A->B 这一条边 = 跳过去是死胡同：只有「目标就是落点」时才有用，
           * 要接着往别处走就得先给落点连边（和放普通路点后做的事一样）。 */
          P c1 = 0;
          if (nav_conn_get(nav_node(g, ib), &c1) <= 1)
            elog("wpmenu: jump landing node %d 目前只连着起点：跳过去没法继续走"
                 "（除非落点就是目标，否则再给它连几条边）", ib);
        }
      } else {
        elog("wpmenu: jump saved but nodes not resolvable (A=%d B=%d); 跳链不会触发", ia, ib);
        toast_bad("跳点存下了，但两端节点对不上：可能不会触发（看日志）");
      }
      g_nedHasA = 0;                            /* 下一次点击重新设起点 */
      break;
    }
    case 2: {
      float yw = cam_dir_yaw();       /* 朝向 = 相机朝向（放之前虚线框已经画给你看） */
      if (make_crouch(p, yw))
        toast_ok("蹲守点已放 (%.1f %.1f %.1f) 朝向 %s", p.x, p.y, p.z, yaw_zh(yw));
      else toast_bad("蹲守点没放上（看游戏日志）");
      break;
    }
    case 3: {
      /* 2026-11-26：按落点归区（以前只认 g_curArea，站在别处加点会静默挂到十几米外的区上）。
       * 2026-11-27：区外不再自动建区 —— 走到这里一定在某个区的 3 m 框里（函数开头已拦掉
       * 区外的落点），这里只负责把点挂到那个区上。 */
      int ai = area_at(&p);
      if (ai >= 0) {
        if (ai != g_curArea) {
          g_curArea = ai;
          elog("wpmenu: 准星落在守卫区 #%d（aid=%d）里，改成挂这个区", ai, g_mk[ai].aid);
        }
        if (make_nanopos(g_mk[ai].aid, p, 3, cam_dir_yaw()))
          toast_ok("守卫点已加到守卫区 #%d（aid=%d）朝向 %s", ai, g_mk[ai].aid, yaw_zh(cam_dir_yaw()));
        else toast_bad("守卫点没加上（区没激活？看日志）");
        elog("wpmenu: guard pos added under area #%d aid=%d", ai, g_mk[ai].aid);
      }
      break;
    }
    case 4:
      if (make_area(30, p)) toast_ok("守卫区已建 (%.1f %.1f %.1f)", p.x, p.y, p.z);
      else toast_bad("守卫区没建出来（到上限了？看日志）");
      break;
    case 5:
      make_tag(p, 7, 3.0f);
      toast_ok("标签区已建（tag=7，半径 3 m）");
      break;
    case 6:   /* 出生点 BL */
      if (spawn_add_point(0, p, cam_yaw())) toast_ok("出生点 BL 已加 (%.1f %.1f %.1f)", p.x, p.y, p.z);
      else toast_bad("出生点 BL 加不了（看游戏日志）");
      break;
    case 7:   /* 出生点 GR */
      if (spawn_add_point(1, p, cam_yaw())) toast_ok("出生点 GR 已加 (%.1f %.1f %.1f)", p.x, p.y, p.z);
      else toast_bad("出生点 GR 加不了（看游戏日志）");
      break;
    case 8:   /* 出生点 中立（个人竞技全员走这个数组） */
      if (spawn_add_point(2, p, cam_yaw())) toast_ok("出生点 中立 已加 (%.1f %.1f %.1f)", p.x, p.y, p.z);
      else toast_bad("出生点 中立 加不了（看游戏日志）");
      break;
    default: break;
  }
  /* 2026-11-25：蹲守 / 守卫 / 标签 / 出生点只记在内存里，Ctrl+S 才写文件。
   * 路点 / 跳链由 nav_push 自己 mark（g_dirtyNav），这里只管 marker 这边。 */
  mke_note_add(n0);           /* 标记也能撤销了（蹲守 / 守卫 / 标签 / 出生点） */
  if (g_wpBrush == 2 || g_wpBrush == 3 || g_wpBrush == 4 || g_wpBrush == 5)
    editor_dirty_mk();
  overlay_refresh();
  menu_refresh();
}

/* ---- 测试包：把环境变量翻译成「读哪个目录」+ 日志一行数据来源 ------------ */
static void pack_stat(void) {
  const char* want = g_packFpLabel[0] ? g_packFpLabel : g_packFp;
  if (!g_packName[0]) {
    if (g_navSearch)
      snprintf(g_packStat, sizeof g_packStat, "数据 成品（各图 %s\\，按指纹找）%s",
               g_navSub[0] ? g_navSub : ".", g_mapDirName[0] ? g_mapDirName : " · 当前图无成品");
    else
      snprintf(g_packStat, sizeof g_packStat, "数据 正式版（nav）");
  } else if (!g_packFp[0]) {
    snprintf(g_packStat, sizeof g_packStat, "数据 测试包 %s · 不限图%s",
             g_packName, g_nedBlank ? " · 空白地图" : "");
  } else if (g_packSkip) {
    snprintf(g_packStat, sizeof g_packStat,
             "数据 测试包 %s · 只对 %s 生效 · 当前图已跳过", g_packName, want);
  } else {
    snprintf(g_packStat, sizeof g_packStat,
             "数据 测试包 %s · 只对 %s 生效 · 包内 %d 项改动%s",
             g_packName, want, g_nedN, g_nedBlank ? " · 空白地图" : "");
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

/* 测试包 id：允许一层地图子目录，如 TransportShip运输船\blank_b（/ 也认）。
 * 地图文件夹可以是中文（系统代码页 GBK 下 ANSI 路径能读；UTF-8 beta 模式会挂）。
 * 只挡 Windows 非法字符、空格（navcmd 用空格分字段）和 . / .. 段。 */
static int pack_ok_id(const char* s) {
  int i, segs = 1, seglen = 0, dot = 0;
  unsigned char c;
  if (!s || !s[0] || strlen(s) > 120) return 0;
  for (i = 0; s[i]; i++) {
    c = (unsigned char)s[i];
    if (c == '\\' || c == '/') {
      int only_dots = (dot && (seglen == dot));
      if (seglen == 0 || segs >= 2) return 0;
      if (only_dots && seglen <= 2) return 0;   /* "." / ".." */
      segs++;
      seglen = 0;
      dot = 0;
      continue;
    }
    if (c < 0x20 || c == ' ' || strchr(":*?\"<>|", c)) return 0;
    if (c == '.') dot++;
    if (++seglen > 60) return 0;
  }
  if (seglen == 0) return 0;
  if (dot && seglen == dot && seglen <= 2) return 0;   /* "." / ".." */
  return 1;
}

/* / 统一成 \，拼路径和日志都省心。 */
static void pack_norm_id(char* s) {
  int i;
  for (i = 0; s[i]; i++) if (s[i] == '/') s[i] = '\\';
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
/* 正式版数据目录：UCF_NAV_DIR > cfg nav_dir > <插件目录>\nav。
 * 2026-11-19：nav\ 不再写死在游戏目录里——工程端可以把正式版数据放到游戏外，
 * 让游戏目录只读（写盘全部落在插件自己的目录或工程端）。 */
static void nav_dir_official(char* out, int cap) {
  char def[MAX_PATH];
  sprintf(def, "%s\\nav", g_dir);
  dir_choice("UCF_NAV_DIR", "nav_dir", def, out, cap);
}

/* 成品档：按指纹在 <root>\<图>\<sub>\<指纹>.txt 里找。
 * 找到 1：path 填完整文件路径，folder 填图文件夹名（markers 要跟着走）。 */
static int nav_find_fp_file(const char* root, const char* sub, const char* fp,
                            char* path, int cap, char* folder, int folderCap) {
  char pat[MAX_PATH];
  WIN32_FIND_DATAA fd;
  HANDLE h;
  if (!root || !root[0] || !fp || !fp[0]) return 0;
  snprintf(pat, sizeof pat, "%s\\*", root);
  h = FindFirstFileA(pat, &fd);
  if (h == INVALID_HANDLE_VALUE) return 0;
  do {
    char p[MAX_PATH];
    FILE* f;
    if (!(fd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)) continue;
    if (!fd.cFileName[0] || fd.cFileName[0] == '.') continue;
    if (sub && sub[0]) snprintf(p, sizeof p, "%s\\%s\\%s\\%s.txt", root, fd.cFileName, sub, fp);
    else snprintf(p, sizeof p, "%s\\%s\\%s.txt", root, fd.cFileName, fp);
    f = fopen(p, "rb");
    if (!f) continue;
    fclose(f);
    if (path && cap) snprintf(path, cap, "%s", p);
    if (folder && folderCap) snprintf(folder, folderCap, "%s", fd.cFileName);
    FindClose(h);
    return 1;
  } while (FindNextFileA(h, &fd));
  FindClose(h);
  return 0;
}

static void pack_init(void) {
  char buf[320];
  g_packName[0] = g_packFp[0] = g_packFpLabel[0] = 0;
  g_packSkip = 0;
  g_mapDirName[0] = 0;
  g_mkFp[0] = 0;
  g_navSearch = 0;
  g_navSub[0] = 0;
  if (GetEnvironmentVariableA("UCF_NAV_SEARCH", buf, sizeof buf) > 0 && buf[0] && strcmp(buf, "0")) {
    g_navSearch = 1;
    if (GetEnvironmentVariableA("UCF_NAV_SUB", buf, sizeof buf) > 0 && buf[0] && pack_ok_id(buf))
      strcpy(g_navSub, buf);
    /* 成品档没有“这一张图”，也就不该在插件目录里建 nav\：根指向 packRoot 就够了 */
    snprintf(g_navDir, sizeof g_navDir, "%s", g_packRoot);
  } else {
    nav_dir_official(g_navDir, sizeof g_navDir);
  }
  if (GetEnvironmentVariableA("UCF_PACK", buf, sizeof buf) > 0 && buf[0]) {
    if (!pack_ok_id(buf)) {
      elog("pack: ignore UCF_PACK=%s (map/pack, [A-Za-z0-9_-], <=60 chars)", buf);
    } else {
      strcpy(g_packName, buf);
      pack_norm_id(g_packName);
      ucf_mkdir_p(g_packRoot);
      sprintf(g_navDir, "%s\\%s", g_packRoot, g_packName);
      ucf_mkdir_p(g_navDir);          /* 地图文件夹 + 包目录一起建 */
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
  if (pack && pack[0] && !pack_ok_id(pack)) {
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
  /* 2026-11-25：切包 / 重新载入 = 以磁盘为准；内存里没按 Ctrl+S 的编辑会被丢掉。
   * 用户从控制台主动点「载入到游戏」时这是有意的，但日志里必须留一行。 */
  if (editor_unsaved())
    elog("navcmd: 切包 / 重新载入会丢弃未保存的游戏内编辑（点图 %d 项 / 标记 %d 个）-- 先 Ctrl+S 才能保留",
         g_nedN, g_n);
  mapChanged = !fp || !fp[0] || strcmp(fp, g_packFp) != 0;
  if (pack && pack[0]) {
    strcpy(g_packName, pack);
    pack_norm_id(g_packName);
    ucf_mkdir_p(g_packRoot);
    sprintf(g_navDir, "%s\\%s", g_packRoot, g_packName);
    ucf_mkdir_p(g_navDir);          /* 地图文件夹 + 包目录一起建 */
    if (fp && fp[0]) strcpy(g_packFp, fp);
    else g_packFp[0] = 0;
  } else {
    g_packName[0] = 0;
    g_packFp[0] = 0;
    nav_dir_official(g_navDir, sizeof g_navDir);
  }
  if (mapChanged) g_packFpLabel[0] = 0;   /* 换图后旧图名不再适用，宁可显示指纹 */
  g_packSkip = 0;
  g_nedApplied = 0;
  g_nedWaitN = -1;
  g_nedN = 0;
  ed_history_reset();
  g_nedBlank = 0;
  g_nedGrow = 0;
  g_nedKeep = 0;
  g_growGraph = 0;
  g_growBase = 0;
  g_growMade = 0;
  g_jumpSeenN = 0;
  g_nedPath[0] = 0;
  g_nedExpect = 0;
  g_nedGraph = g;
  /* 换包 = 换地图：编辑标记换成这张图自己的那份（markers\<包名>\markers.txt），
   * 顺手把场景里的旧标记重放一遍，别让上一张图的蹲守点留在这一张图里。 */
  mk_set_path();
  spawn_restore_orig();       /* 换包前先把数组还原成原生，别把上一次的出生点当原生快照 */
  reset_markers();
  load_file();
  g_dirtyNav = 0;             /* 内存清单 / 标记都换成磁盘内容了 */
  g_dirtyMk = 0;
  elog("markers: map file -> %s", g_file);
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
  char pack[160] = "";
  char fp[48] = "";
  char brush[24] = "";
  char menu[8] = "";
  char act[16] = "";
  char who[16] = "";
  char mapname[64] = "";
  char label[64] = "";
  char out[MAX_PATH] = "";
  int hz = 0;
  unsigned long long seq = 0;
  int have = 0;
  /* 可视化实时下发（控制台「插件开关 → 可视化」）：-1 = 这条命令没带这个字段，别动 */
  int v_on = -1, v_nodes = -1, v_nano = -1, v_crouch = -1, v_born = -1, v_supply = -1;
  int v_jump = -1, v_tag = -1, v_navmesh = -1, v_compass = -1, v_marks = -1;
  /* 控制台删了坐标：文件修改时间变了就重读并重画（0.5 s 一次，文件很小） */
  if (g_pmPath[0] && g_visPm && pm_load(0)) {
    elog("pmark: reloaded %d mark(s)", g_pmN);
    g_visDirty = 1;
  }
  if (!g_navCmdPath[0]) return;
  f = fopen(g_navCmdPath, "r");
  if (!f) return;
  while (fgets(line, sizeof line, f)) {
    if (sscanf(line, "seq=%llu", &seq) == 1) { have = 1; continue; }
    if (sscanf(line, "cmd=%23s", cmd) == 1) continue;
    if (sscanf(line, "pack=%159s", pack) == 1) continue;
    if (sscanf(line, "fp=%47s", fp) == 1) continue;
    if (sscanf(line, "brush=%23s", brush) == 1) continue;
    if (sscanf(line, "menu=%7s", menu) == 1) continue;
    if (sscanf(line, "act=%15s", act) == 1) continue;
    if (sscanf(line, "who=%15s", who) == 1) continue;
    if (sscanf(line, "hz=%d", &hz) == 1) continue;
    if (sscanf(line, "map=%63s", mapname) == 1) continue;
    if (sscanf(line, "label=%63s", label) == 1) continue;
    if (sscanf(line, "on=%d", &v_on) == 1) continue;
    if (sscanf(line, "nodes=%d", &v_nodes) == 1) continue;
    if (sscanf(line, "nano=%d", &v_nano) == 1) continue;
    if (sscanf(line, "crouch=%d", &v_crouch) == 1) continue;
    if (sscanf(line, "born=%d", &v_born) == 1) continue;
    if (sscanf(line, "supply=%d", &v_supply) == 1) continue;
    if (sscanf(line, "jump=%d", &v_jump) == 1) continue;
    if (sscanf(line, "tag=%d", &v_tag) == 1) continue;
    if (sscanf(line, "navmesh=%d", &v_navmesh) == 1) continue;
    if (sscanf(line, "compass=%d", &v_compass) == 1) continue;
    if (sscanf(line, "marks=%d", &v_marks) == 1) continue;
    if (!strncmp(line, "out=", 4)) {              /* 路径里可能有空格：取整行 */
      char* q = line + 4;
      size_t n2;
      while (*q == ' ' || *q == '\t') q++;
      n2 = strlen(q);
      while (n2 && (q[n2 - 1] == '\n' || q[n2 - 1] == '\r' || q[n2 - 1] == ' ')) q[--n2] = 0;
      strncpy(out, q, sizeof out - 1);
      out[sizeof out - 1] = 0;
      continue;
    }
  }
  fclose(f);
  if (!have || seq == g_navCmdSeq) return;
  g_navCmdSeq = seq;
  elog("navcmd: seq=%llu cmd=%s pack=%s fp=%s", seq,
       cmd[0] ? cmd : "(none)", pack[0] ? pack : "(none)", fp[0] ? fp : "(any)");
  if (!strcmp(cmd, "save")) {
    /* 控制台 / 自动化：和 Ctrl+S 走同一个入口（只写改过的那一边） */
    editor_save_all();
    return;
  }
  if (!strcmp(cmd, "undo")) { ed_undo(); return; }
  if (!strcmp(cmd, "redo")) { ed_redo(); return; }
  if (!strcmp(cmd, "brush")) { set_brush(brush_from_name(brush)); return; }
  if (!strcmp(cmd, "mark")) { pm_mark(); return; }
  if (!strcmp(cmd, "menu")) {
    if (menu[0] == '0' || !strcmp(menu, "off")) menu_close();
    else if (menu[0] == '1' || !strcmp(menu, "on")) menu_open();
    return;
  }
  /* 录制 / 采集：同一套采样会话（2026-11-27）。kind 只决定 header 和控制台怎么用：
   * rec = 走完一段 → 复盘成点图；trace = 只留日志 / 跳跃报告。who 是会话参数。 */
  if (!strcmp(cmd, "rec") || !strcmp(cmd, "trace")) {
    int kind = (!strcmp(cmd, "rec")) ? SS_REC : SS_TRACE;
    int whoMask = 1;
    if (!strcmp(who, "bots")) whoMask = 2;
    else if (!strcmp(who, "all")) whoMask = 3;
    if (!strcmp(act, "start")) {
      ss_begin(kind, out, hz, whoMask, mapname, label, pack, fp);
    } else if (!strcmp(act, "stop")) {
      ss_stop("console");
    } else if (!strcmp(act, "pause")) {
      g_ss.paused = 1;
      elog("sample: paused (%s)", ss_kind_name());
    } else if (!strcmp(act, "resume")) {
      g_ss.paused = 0;
      g_ss.nextT = ss_now();
      elog("sample: resumed (%s)", ss_kind_name());
    } else {
      elog("navcmd: %s needs act=start|stop|pause|resume", cmd);
    }
    return;
  }
  if (!strcmp(cmd, "vis")) {                      /* 可视化实时开关：控制台勾选框下发，不重进图 */
    if (v_nodes   >= 0) g_visNodes  = v_nodes ? 1 : 0;
    if (v_nano    >= 0) g_visNano   = v_nano ? 1 : 0;
    if (v_crouch  >= 0) g_visCrouch = v_crouch ? 1 : 0;
    if (v_born    >= 0) g_visBorn   = v_born ? 1 : 0;
    if (v_supply  >= 0) g_visSupply = v_supply ? 1 : 0;
    if (v_jump    >= 0) g_visJump   = v_jump ? 1 : 0;
    if (v_tag     >= 0) g_visTag    = v_tag ? 1 : 0;
    if (v_marks   >= 0) g_visPm     = v_marks ? 1 : 0;
    if (v_on      >= 0) g_visOn     = v_on ? 1 : 0;
    if (v_navmesh >= 0) { g_nmShow = v_navmesh ? 1 : 0; g_nmDirty = 1; nm_tick(); }
    if (g_visOn) vis_rebuild();
    else { vis_show(0); g_visDirty = 0; }
    mk_vis_apply();
    if (v_compass >= 0) compass_apply(v_compass);
    elog("vis cmd: on=%d nodes=%d nano=%d crouch=%d born=%d supply=%d jump=%d tag=%d nm=%d compass=%d marks=%d",
         g_visOn, g_visNodes, g_visNano, g_visCrouch, g_visBorn, g_visSupply,
         g_visJump, g_visTag, g_nmShow, g_visCompass, g_visPm);
    return;
  }
  if (!strcmp(cmd, "stopall")) {                  /* 关控制台的收尾命令（旧版控制台还在发） */
    ss_stop("console");
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
  int n, ops, made = 0;
  if (!ed_init()) return;
  g = navfix_point_graph();
  nav_cmd_tick(g);            /* 控制台命令：运行中切包 / 重读 / 保存 */
  if (!g && (g_packName[0] || nav_pg_test())) {
    /* 2026-11-27 纯面图（胜利广场 / 死亡擂台）：场景 A* 里连 PointGraph 都没有，
     * 插件没有 AddNode 的地方。选着测试包（或 UCF_PG_TEST=1 试验）时现场补一张，
     * 补上之后就和飓风危城一样是「0 点图 + grow」。 */
    g = navfix_add_point_graph();
    if (g) {
      made = 1;                 /* 下面「图变了」那段会清标记，补完再置位 */
      elog("naved: 本图没有 PointGraph，已现场补一张（0 节点，走 grow）");
    }
  }
  if (!g) { g_nedGraph = 0; g_nedApplied = 0; g_nedWaitN = -1; return; }
  if (g != g_nedGraph) {
    /* 换图 / 图被重建：内存里的点图改动不再对得上，直接作废（和退房间同一原则） */
    if (g_dirtyNav && g_nedN)
      elog("naved: 点图对象换了，丢弃未保存的 %d 项编辑 -- 只有 Ctrl+S 才会落盘", g_nedN);
    g_dirtyNav = 0;
    g_nedGraph = g;
    g_nedApplied = 0;
    g_nedWaitN = -1;
    g_nedHasA = 0;
    g_nedN = 0;
    ed_history_reset();
    g_nedBlank = 0;
    g_nedGrow = 0;
    g_nedKeep = 0;
    g_nedPath[0] = 0;
    g_growGraph = 0;     /* 换图：grow 记录只对旧图有效 */
    g_growBase = 0;
    g_growMade = 0;
    g_jumpSeenN = 0;     /* 换图：跳链只对旧图建过一次，新图要重来 */
  g_nativeJumpLogged = 0;
    g_packSkip = 0;      /* 换图：让下一张图重新判断一次，并在日志里各记一行 */
    nav_base_free();     /* 旧图的快照只对旧图有效 */
    navfix_pg_reset();   /* 换图：纯面图补 PointGraph 的「试过一次」也清掉 */
    g_pgSynthetic = 0;   /* 换图：补图 / 摘可走面只对旧图有效（补完当场会再置 1） */
    g_pgNmDropped = 0;
    g_fpGraph = 0;       /* 指纹的原生点数只对这张图有效 */
    g_fpBaseN = -1;
    g_nedZeroTicks = 0;
  }
  if (made) g_pgSynthetic = 1;   /* 这一 tick 刚补的图：标记要盖过上面的清零 */
  n = nav_count(g);
  if (!g_nedApplied) {
    /* 0 节点图只能靠 grow：它不需要原生槽位。图可能还没扫出来，所以要求
     * 「文件里有 grow + 连续 5 帧都是 0」才放行，避免空图瞬间误建点。 */
    if (n <= 0) {
      if (!nav_zero_grow_ready()) { g_nedZeroTicks = 0; return; }
      if (++g_nedZeroTicks < 5) return;
    } else {
      g_nedZeroTicks = 0;
    }
    if (n != g_nedWaitN) { g_nedWaitN = n; return; }       /* 等两跳稳定 */
    if (g != g_fpGraph || g_fpBaseN < 0) {                 /* 图稳定了：记下原生点数 */
      g_fpGraph = g;
      g_fpBaseN = n;
    }
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
    if (g_navSearch) {
      /* 成品档：按这张图的指纹去 <packRoot>\<图>\<sub>\ 里找 */
      char folder[160] = {0};
      if (nav_find_fp_file(g_packRoot, g_navSub, g_nedFp,
                           g_nedPath, sizeof g_nedPath, folder, sizeof folder)) {
        if (strcmp(folder, g_mapDirName) != 0) {
          /* 换图：markers.txt 也跟着这张图走，重读一次（先 reset 掉上一张图的标记） */
          snprintf(g_mapDirName, sizeof g_mapDirName, "%s", folder);
          reset_markers();
          mk_set_path();
          snprintf(g_mkFp, sizeof g_mkFp, "%s", g_nedFp);
          load_file();
          elog("markers: 成品档 -> %s", g_file);
        }
      } else {
        g_nedPath[0] = 0;      /* 这张图没有成品：什么都不套（= 原版） */
        if (g_mapDirName[0]) {
          g_mapDirName[0] = 0;
          reset_markers();
          mk_set_path();
          g_mkFp[0] = 0;
          load_file();
        }
      }
    } else {
      sprintf(g_nedPath, "%s\\%s.txt", g_navDir, g_nedFp);
    }
    nav_base_take(g);     /* 先拍原生底图，再套文件；切包时才能还原 */
    if (g_nedPath[0]) nav_edit_load(g_nedPath);
    /* 防御：套文件前如果内存里已经有未保存的点图编辑（进图第一秒就加点的极端情况），
     * 它们会被文件内容覆盖；清掉脏标记，别让后面 Ctrl+S 拿空清单去删文件。 */
    if (g_dirtyNav) {
      elog("naved: 套用磁盘内容前有未保存的点图编辑，已被覆盖（Ctrl+S 才能保留）");
      g_dirtyNav = 0;
    }
    if ((g_nedBlank || g_nedGrow) && !g_packName[0]) {
      g_nedBlank = 0;
      g_nedGrow = 0;
      g_nedKeep = 0;
      elog("naved: ignore blank/grow/keep (only a test pack may replace the base)");
    }
    g_nedBaseN = n;
    ops = nav_apply_all(g);
    if (ops < 0) { g_nedWaitN = -1; return; }   /* grow 要等 A* 就绪：下一帧重来 */
    g_nedApplied = 1;
    pack_stat();
    if (ops) elog("naved: applied %d/%d edits on %s (nodes %d -> %d)%s%s",
                  ops, g_nedN, g_nedFp, g_nedBaseN, nav_count(g),
                  g_nedBlank ? " [blank base]" : "", g_nedKeep ? " [keep native]" : "");
    else if (g_nedN || g_nedKeep)
      elog("naved: %d edits loaded, 0 effective on %s (nodes %d)%s",
           g_nedN, g_nedFp, nav_count(g), g_nedKeep ? " [keep native]" : "");
    else elog("naved: no edit file for %s (dir %s)", g_nedFp, g_navDir);
    return;
  }
  /* 图被游戏重扫/重建过 -> 改动没了，重新套用（每 ~1 s 检查一次） */
  if (g_nedN || (g_nedBlank && g_packName[0])) {
    static int probe;
    if ((++probe % 16) == 0 && nav_needs_apply(g)) {
      ops = nav_apply_all(g);
      if (ops < 0) return;
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
/* 2026-11-20：删掉原第 2 项「设置笔刷 / 标记」——它和「添加点位」走的是
 * 同一条「选类型 → 左键放置」路径，纯重复。类型统一在「添加点位」子菜单选。
 * 2026-11-25：守卫点 / 守卫区 从「添加点位」移回「守卫区工具」——
 * 同一件事只留一个入口，不再两处都能新建。 */
/* 2026-11-27：主菜单加第 9 项「朝向工具」（蹲守点 / 守卫点的朝向）。
 * 放在「显示图层」前面 = 数字键 9 给朝向工具，「显示图层」挪到第 10 项（8/2 移过去），
 * 1-8 的数字键完全不变，不会打乱已经用熟的手感。 */
static const char* WP_MENU[] = {
  "添加点位", "建立路径", "守卫区工具", "删除点图连线 / 路点",
  "删除点位（按类型选）", "删除区域（守卫区）", "落地 / 贴地", "撤销 / 恢复 / 保存",
  "朝向工具（蹲守点 / 守卫点）", "显示图层", "关闭菜单（Esc 逐级返回）"
};
#define WP_MENU_N ((int)(sizeof WP_MENU / sizeof WP_MENU[0]))
/* 添加点位子菜单只放点位型标记；守卫点/守卫区走「守卫区工具」，
 * 标签区不再从菜单提供（控制台 brush tag 仍可用）。
 * 2026-11-25：加出生点 BL/GR；2026-11-27 加中立（SP_Netural）并把新增点排到数组最前。 */
#define WP_TYPE_N 6
static const char* WP_TYPES[WP_TYPE_N] = {
  "普通路点（可走的 PointNode）",
  "跳跃点（Bot_JumpLink）",
  "蹲守点（Bot_CrouchPos）",
  "出生点 BL（幽灵 / 潜伏者）",
  "出生点 GR（保卫者 / 人类）",
  "出生点 中立（个人竞技全员 / 缺 BL、GR 时兜底）"
};
/* 子菜单序号 → 实际笔刷编号（3=守卫点、4=守卫区、5=标签区 不在这里） */
static const int WP_TYPE_BRUSH[WP_TYPE_N] = { 0, 1, 2, 6, 7, 8 };

static int wp_type_index(int brush) {
  int i;
  for (i = 0; i < WP_TYPE_N; i++) if (WP_TYPE_BRUSH[i] == brush) return i;
  return 0;
}
static int wp_type_brush(int idx) {
  return (idx >= 0 && idx < WP_TYPE_N) ? WP_TYPE_BRUSH[idx] : 0;
}
/* 提示文字用：按笔刷编号取名字（含菜单里不提供的守卫点/守卫区） */
static const char* wp_brush_label(int brush) {
  switch (brush) {
    case 1: return WP_TYPES[1];
    case 2: return WP_TYPES[2];
    case 3: return "守卫点（Bot_NanoGuardPos）";
    case 4: return "守卫区（Bot_NanoGuardArea）";
    case 5: return "标签区";
    case 6: return "出生点 BL（幽灵 / 潜伏者）";
    case 7: return "出生点 GR（保卫者 / 人类）";
    case 8: return "出生点 中立（个人竞技全员）";
    default: return WP_TYPES[0];
  }
}
static const char* WP_PATHS[3] = { "双向", "单向 A -> B", "单向 B -> A" };
static const char* WP_AREAS[4] = {
  "新建守卫区（Bot_NanoGuardArea）", "加守卫点（Bot_NanoGuardPos）",
  "加入口 entrancePos", "加逃跑点 escapePos"
};
/* 2026-11-25：保存改成唯一入口 Ctrl+S；菜单文字直接写出来，别再藏「保存到文件」。
 * 2026-11-26 用户要求：第 2 项「重做一步」改名「恢复」并带一句解释（撤销的反操作）；
 * 「重读并套用」整项删除 —— 想重读走控制台的「重新应用 / 载入到游戏」。 */
static const char* WP_EDIT[3] = { "撤销一步", "恢复（撤销的反操作）", "保存（Ctrl+S）" };
static const char* WP_LAYERS[3] = { "路点/连线", "可走面", "路点总开关" };
/* 朝向工具页（2026-11-27）：只操作我们自己放的蹲守点 / 守卫点。
 * 方向 = 游戏 zoomPos 里的世界目标点，改成「点位 + 朝向*10 m」。
 * 「设为相机朝向」= 你站在哪、看哪，它就朝哪（和放置时同一套）。 */
#define WP_DIR_N 5
static const char* WP_DIR[WP_DIR_N] = {
  "设为相机朝向（你看着哪，它就朝哪）",
  "顺时针 +15°（→ 连续转，Shift 精调 1°）",
  "逆时针 -15°（← 连续转，Shift 精调 1°）",
  "清空方向（回到未知：画虚线，人机朝向不确定）",
  "显示样式：射线 / 扇形 / 关"
};
static const char* WP_DEL[2] = { "删除点图连线（A-B）", "删除路点（A* 节点）" };
/* 删除点位：按类型定向，最后一项才是老的"准星最近"。
 * 2026-11-25 用户要求：原来的「删除标记」拆成「删除点位 / 删除区域」两页；
 * 区域单独一页，点位页的"任意"也不含守卫区，避免手滑删掉整片守卫区。 */
#define WP_DELPT_N 8
static const char* WP_DELPT[WP_DELPT_N] = {
  "蹲守点（Bot_CrouchPos）",
  "守卫点（Bot_NanoGuardPos）",
  "跳跃点 / 跳链（Bot_JumpLink）",
  "标签 / 范围（tag，只删标记）",
  "出生点 BL（幽灵 / 潜伏者）",
  "出生点 GR（保卫者 / 人类）",
  "出生点 中立（个人竞技全员）",
  "任意点位（准星最近 · 老行为）"
};
static const int WP_DELPT_TYPE[WP_DELPT_N] = {
  MT_CROUCH, MT_NANOPOS, MT_JUMP, MT_TAG, MT_SPAWN_BL, MT_SPAWN_GR, MT_SPAWN_NT, MT_ANY_POINT
};
/* 删除区域页：目前只有守卫区（旧的 Bot_GuardArea 是死数据，不单列）。 */
static const char* WP_DELAREA[1] = { "守卫区（连带它下面的守卫点）" };

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
  /* 2026-11-20 用户需求：选定类型后停在「连续编辑」页，不要回主菜单。
   * 标题直接写清楚现在是哪种模式；Esc 才一级一级往回退。 */
  if (g_wpMenuSub == 1) s = g_wpArm ? "添加点位：连续放置中" : "添加点位：选类型";
  else if (g_wpMenuSub == 2) s = g_wpLinkStep ? "建立路径：连续连线中" : "建立路径：选方向";
  else if (g_wpMenuSub == 3) s = "守卫区工具（虚线框 = 预置落点）";
  else if (g_wpMenuSub == 4) s = "撤销 / 恢复 / 保存";
  else if (g_wpMenuSub == 5) s = "显示图层";
  else if (g_wpMenuSub == 6) s = "删除：选类型（可连续删）";
  else if (g_wpMenuSub == 7) {
    if (g_delType < 0) s = "删除点位：先选类型（1-8）";
    else if (g_delType == MT_ANY_POINT) s = "删除点位：任意点位（准星最近）";
    else {
      snprintf(out, (size_t)cap, "删除点位：%s（5/Delete 删）", mt_name(g_delType));
      return;
    }
  }

  else if (g_wpMenuSub == 8) s = "删除区域：守卫区（5/Delete 删）";
  else if (g_wpMenuSub == 9) s = "朝向工具（准星对着你放的蹲守点 / 守卫点）";
  snprintf(out, (size_t)cap, "%s", s);
}

static int menu_sub_count(void) {
  if (g_wpMenuSub == 1) return WP_TYPE_N;
  if (g_wpMenuSub == 2) return 3;
  if (g_wpMenuSub == 3) return 4;
  if (g_wpMenuSub == 4) return 3;
  if (g_wpMenuSub == 5) return 3;
  if (g_wpMenuSub == 6) return 2;
  if (g_wpMenuSub == 7) return WP_DELPT_N;
  if (g_wpMenuSub == 8) return 1;
  if (g_wpMenuSub == 9) return WP_DIR_N;
  return WP_MENU_N;
}

static const char* menu_sub_label(int i) {
  if (g_wpMenuSub == 1) return (i >= 0 && i < WP_TYPE_N) ? WP_TYPES[i] : "";
  if (g_wpMenuSub == 2) return (i >= 0 && i < 3) ? WP_PATHS[i] : "";
  if (g_wpMenuSub == 3) return (i >= 0 && i < 4) ? WP_AREAS[i] : "";
  if (g_wpMenuSub == 4) return (i >= 0 && i < 3) ? WP_EDIT[i] : "";
  if (g_wpMenuSub == 5) return (i >= 0 && i < 3) ? WP_LAYERS[i] : "";
  if (g_wpMenuSub == 6) return (i >= 0 && i < 2) ? WP_DEL[i] : "";
  if (g_wpMenuSub == 7) return (i >= 0 && i < WP_DELPT_N) ? WP_DELPT[i] : "";
  if (g_wpMenuSub == 8) return (i >= 0 && i < 1) ? WP_DELAREA[i] : "";
  if (g_wpMenuSub == 9) {
    /* 第 5 项动态写当前样式，省得再进一页 */
    static char sty[64];
    if (i < 0 || i >= WP_DIR_N) return "";
    if (i != 4) return WP_DIR[i];
    snprintf(sty, sizeof sty, "%s（当前：%s）", WP_DIR[4],
             g_dirStyle == 0 ? "关" : (g_dirStyle == 2 ? "扇形" : "射线"));
    return sty;
  }
  return "";
}

/* 菜单选中项的高亮：UGUI Text 的富文本（这个 Text 是我们自己 AddComponent 建的，
 * 默认 supportRichText 就是开着的）。#FFD24A 和罗盘「当前朝向」同一个金 —— 深色场景
 * 上比纯黄 #FFFF00 更清楚，也不至于和守卫区金框撞色到分不出来。 */
#define MENU_HI_ON  "<color=#FFD24A>"
#define MENU_HI_OFF "</color>"

static void menu_refresh(void) {
  char s[2048];
  char title[64];
  int i, n, off = 0;
  if (g_menu && !uobj_live(g_menu)) overlay_reset();
  /* 2026-11-20 现场反馈「编辑一次菜单就没了」：换图 / overlay_reset 之后 g_menu 会被
   * 置 0，而 g_wpMenuOpen 还是 1。以前这里直接 return，菜单就凭空消失：按 F2 的第一下
   * 只是把 open 清掉（看着像关了），第二下才重新出现。现在缺对象就地重建，别让菜单
   * 自己"退出"。 */
  if (!g_menu && g_wpMenuOpen && g_wpMenuOn) {
    static unsigned lastTry;
    unsigned now = GetTickCount();
    if (now - lastTry >= 1000) {
      lastTry = now;
      if (!overlay_init()) return;
    } else {
      return;
    }
  }
  if (!g_menu) return;
  if (!g_wpMenuOn || !g_wpMenuOpen) {
    ((set_txt_t)RVA(R_TEXT_SETTEXT))(g_menu, x_string_new(""), 0);
    return;
  }
  menu_sub_title(title, sizeof title);
  /* 2026-11-25：菜单第一行常驻保存状态 —— 用户要求「必须手动保存」，
   * 不能等退房间才发现没存。 */
  off += snprintf(s + off, sizeof s - (size_t)off,
                  "%s   [F2/长按E 关]   %s\n", title,
                  editor_unsaved() ? "● 未保存 · Ctrl+S 保存" : "已保存 · Ctrl+S 保存");
  if (g_wpMenuSub == 0) {
    for (i = 0; i < WP_MENU_N && off < (int)sizeof s - 80; i++) {
      /* 主菜单最后一项是「关闭菜单」：显示成 0（数字键 0 也走这一项）。
       * 2026-11-26 用户要求：选中项整行变黄，别只靠行首那个 "> " 认。 */
      int key = (i == WP_MENU_N - 1) ? 0 : i + 1;
      int on = (i == g_wpMenuSel);
      off += snprintf(s + off, sizeof s - (size_t)off, "%s%s%d  %s%s\n",
                      on ? MENU_HI_ON : "", on ? "> " : "  ", key, WP_MENU[i],
                      on ? MENU_HI_OFF : "");
    }
  } else {
    n = menu_sub_count();
    for (i = 0; i < n && off < (int)sizeof s - 80; i++) {
      int on = (i == g_wpMenuSubSel);
      off += snprintf(s + off, sizeof s - (size_t)off, "%s%s%d  %s%s\n",
                      on ? MENU_HI_ON : "", on ? "> " : "  ", i + 1, menu_sub_label(i),
                      on ? MENU_HI_OFF : "");
    }
    /* 这几页的数字键只是选中，得写出来，不然用户会以为按了没反应 */
    if ((g_wpMenuSub == 4 || g_wpMenuSub == 6) && off < (int)sizeof s - 160)
      off += snprintf(s + off, sizeof s - (size_t)off,
                      "1-%d / 8/2 只切换选中 · 5 / 左键 / 回车 才执行\n", n);
  }
  /* 主菜单停在「6 落地 / 贴地」时提示一句：按 6 只是选中，按 5 才贴 */
  if (g_wpMenuSub == 0 && g_wpMenuSel == 6 && off < (int)sizeof s - 160)
    off += snprintf(s + off, sizeof s - (size_t)off,
                    "\n落地 / 贴地：按 6 只是选中，按 5 / 左键 才执行（改点图 Y，可撤销一步）\n");
  if (g_wpMenuSub == 4 && off < (int)sizeof s - 400) {
    char desc[160];
    if (ed_top_mke() > ed_top_nav()) mke_desc(&g_mke[g_mkeN - 1], desc, sizeof desc);
    else nav_ed_desc(g_nedN > 0 ? &g_ned[g_nedN - 1] : 0, desc, sizeof desc);
    off += snprintf(s + off, sizeof s - (size_t)off,
                    "\n撤销栈：点图 %d 条 · 标记 %d 个（可恢复 点图 %d / 标记 %d）\n"
                    "最近一步：%s\n"
                    "撤销：反做最近一步（点 / 线 / 跳链 / 标记，同一次动作一起撤）\n"
                    "恢复：把刚撤销的那一步原样放回来；做过新的编辑后就不能恢复了\n"
                    "Ctrl+S 保存全部（点图 + 标记 / 出生点）；不保存就退房间 = 改动丢弃\n",
                    g_nedN, g_mkeN, g_redoN, g_mkeRedoN, desc);
  }
  if (g_wpMenuSub == 7) {
    char bls[12], grs[12], nts[12];
    int bl = spawn_count(0), gr = spawn_count(1), nt = spawn_count(2);
    if (bl < 0) strcpy(bls, "?"); else snprintf(bls, sizeof bls, "%d", bl);
    if (gr < 0) strcpy(grs, "?"); else snprintf(grs, sizeof grs, "%d", gr);
    if (nt < 0) strcpy(nts, "?"); else snprintf(nts, sizeof nts, "%d", nt);
    off += snprintf(s + off, sizeof s - (size_t)off,
                    "\n图里现有：蹲守 %d · 守卫点 %d · 跳链 %d · 标签 %d · 出生点 BL %s / GR %s / 中立 %s\n",
                    mt_count(MT_CROUCH), mt_count(MT_NANOPOS), mt_count(MT_JUMP),
                    mt_count(MT_TAG), bls, grs, nts);
    if (off < (int)sizeof s - 300)
      off += snprintf(s + off, sizeof s - (size_t)off,
                      "1-8 选类型 · 准星对准对象按 小键盘5 / Enter / Delete 删除（可连续）· 0 返回\n"
                      "出生点按坐标匹配原生数组，至少保留 1 个；加/删只改内存，Ctrl+S 才写文件\n");
  }
  if (g_wpMenuSub == 8) {
    off += snprintf(s + off, sizeof s - (size_t)off,
                    "\n图里现有：守卫区 %d\n", mt_count(MT_AREA));
    if (off < (int)sizeof s - 160)
      off += snprintf(s + off, sizeof s - (size_t)off,
                      "准星对准守卫区按 5/Delete 删除（连同它下面的守卫点）· 0 返回\n");
  }
  if (g_wpMenuSub == 2 && off < (int)sizeof s - 120) {
    off += snprintf(s + off, sizeof s - (size_t)off,
                    "\n类型：点图连线（PointNode.connections）\n");
  }
  if (g_wpArm) {
    off += snprintf(s + off, sizeof s - (size_t)off,
                    "\n[%s] 小键盘5 / 左键 放置 · 可以一直放\n", wp_brush_label(g_wpBrush));
    if (g_wpBrush == 1 && off < (int)sizeof s - 96) {
      if (g_nedHasA) {
        P pg = navfix_point_graph();
        int ai = pg ? nav_find(pg, &g_nedA, 0.6f) : -1;
        off += snprintf(s + off, sizeof s - (size_t)off,
                        "起点 A #%d (%.1f %.1f %.1f)：对准落点再按 5（落点没路点会自动补一个 + 补 A->B 连线）\n",
                        ai, g_nedA.x, g_nedA.y, g_nedA.z);
      }
      else
        off += snprintf(s + off, sizeof s - (size_t)off,
                        "两次点击：第 1 次对准起跳处（要在路点上），第 2 次对准落点\n");
    }
    if (off < (int)sizeof s - 96)
      off += snprintf(s + off, sizeof s - (size_t)off,
                      "换类型：1-5 直选或 8/2 · 结束放置：0 / Esc（菜单不会关）\n");
  } else if (g_wpLinkStep == 1) {
    off += snprintf(s + off, sizeof s - (size_t)off,
                    "\n对准起点（准星框变绿 = 就是它），小键盘5 选 A\n"
                    "连完一条 A 会自动前进到落点，接着连下一个\n");
    if (off < (int)sizeof s - 96)
      off += snprintf(s + off, sizeof s - (size_t)off,
                      "换方向：1-3 直选或 8/2 · 结束连线：0 / Esc（菜单不会关）\n");
  } else if (g_wpLinkStep == 2) {
    P pg = navfix_point_graph();
    int ai = pg ? nav_find(pg, &g_nedA, 0.6f) : -1;
    const char* mode = g_wpPath == 1 ? "单向 A->B" : (g_wpPath == 2 ? "单向 B->A" : "双向");
    off += snprintf(s + off, sizeof s - (size_t)off,
                    "\n起点 A #%d (%.1f %.1f %.1f)\n", ai, g_nedA.x, g_nedA.y, g_nedA.z);
    if (g_ghostPvOk && off < (int)sizeof s - 160) {
      float dm = sqrtf(nav_d2(&g_nedA, &g_ghostPv));
      if (g_ghostPvIdx >= 0)
        off += snprintf(s + off, sizeof s - (size_t)off,
                        "终点 B #%d (%.1f %.1f %.1f)  %.1f m  %s\n",
                        g_ghostPvIdx, g_ghostPv.x, g_ghostPv.y, g_ghostPv.z, dm, mode);
      else
        off += snprintf(s + off, sizeof s - (size_t)off,
                        "终点 B 新点 (%.1f %.1f %.1f)  %.1f m  %s\n",
                        g_ghostPv.x, g_ghostPv.y, g_ghostPv.z, dm, mode);
    } else if (off < (int)sizeof s - 96) {
      off += snprintf(s + off, sizeof s - (size_t)off,
                      "终点 B：准星压在路点方块上（绿 = 起点，红 = 终点；没压中就画灰）\n");
    }
    off += snprintf(s + off, sizeof s - (size_t)off,
                    "按 5 连边 · 连完 A 前进到落点 · 0 / Esc 结束连线\n");
  } else if (g_wpMenuSub != 3 && g_wpMenuSub != 7 && g_wpMenuSub != 8) {
    off += snprintf(s + off, sizeof s - (size_t)off, "\n当前笔刷: %s  A: %s\n",
                    wp_brush_label(g_wpBrush), g_nedHasA ? "已选" : "未选");
  }
  /* 守卫区工具：写清「选中的这一项按下去会建什么、建在哪」（2026-11-26）。
   * 以前这一页只有四项名字，光看菜单根本不知道准星会落在哪，也没有任何预览。 */
  if (g_wpMenuSub == 3 && off < (int)sizeof s - 460) {
    if (g_wpMenuSubSel == 0) {
      off += snprintf(s + off, sizeof s - (size_t)off,
                      "\n虚线框 = 预置落点：守卫区 3.0 m 见方（BoxCollider 中心在准星落点）\n"
                      "按 5 / 左键 才真正创建；蓝色框 = 守卫区\n"
                      "建好后场上立刻出现金色线框；挂上第一个守卫点才变绿框（激活，人机才认）\n");
    } else if (g_wpMenuSubSel == 1) {
      /* 2026-11-26 起「加守卫点」按落点归区（area_at），不再认「当前区」：
       * 站远处加点会挂到别的区上，用户看到的就是「加了点也没变绿」。 */
      int ai = g_ghostPvOk ? area_at(&g_ghostPv) : -1;
      off += snprintf(s + off, sizeof s - (size_t)off,
                      "\n虚线框 = 预置落点：守卫点（Bot_NanoGuardPos，标记 0.32，绿色框）\n"
                      "挂了点，这个点所在的守卫区就被激活：金色线框 → 绿框\n");
      if (ai >= 0)
        off += snprintf(s + off, sizeof s - (size_t)off,
                        "准星在守卫区 #%d（aid=%d）里：按 5 就挂进这个区\n",
                        ai, g_mk[ai].aid);
      else
        off += snprintf(s + off, sizeof s - (size_t)off,
                        "准星不在任何守卫区里：按 5 不会建点（守卫点只挂在区里）—— 先按 1 建区，再回来加点\n");
    } else {
      off += snprintf(s + off, sizeof s - (size_t)off,
                      "\n入口 / 逃跑点还没接（按 5 只写一行日志，图上不会变，也没有虚线）\n");
    }
    if (off < (int)sizeof s - 120)
      off += snprintf(s + off, sizeof s - (size_t)off,
                      "1-4 / 8/2 只切换选中 · 5 / 左键 / 回车 才真正执行\n");
    if (g_wpMenuSubSel <= 1 && !g_ghostPvOk && off < (int)sizeof s - 200)
      off += snprintf(s + off, sizeof s - (size_t)off,
                      "准星没打到地面（朝天 / 太远）：虚线框不显示\n");
  }
  /* 准星处那个虚线框的坐标（ghost_tick 每帧更新，文字 ~5 Hz 刷新）：
   * 位置不合法（附近没路点 / 离起点太近）时框变灰，这里也直说。 */
  {
    /* wp_guard_preview() 现算一遍：8/2 挪到「入口 / 逃跑点」时，上一帧的
     * g_ghostPrev 还是 1，别让文字里多留一行过期坐标。 */
    int prev = (g_ghostPrev && wp_guard_preview());
    if ((g_wpArm || g_wpLinkStep || prev) && g_ghostPvOk && off < (int)sizeof s - 128)
      off += snprintf(s + off, sizeof s - (size_t)off, "预置 (%.1f %.1f %.1f)%s%s\n",
                      g_ghostPv.x, g_ghostPv.y, g_ghostPv.z,
                      g_ghostValid ? "" : "  × 这里按下去会被拒绝",
                      prev ? "  仅预览 · 按 5 创建" : "");
  }
  /* 朝向工具页（2026-11-27）：把「准星现在对着谁、它朝哪」写在菜单里，
   * 不然按 5 之前完全不知道会改哪个点。 */
  if (g_wpMenuSub == 9 && off < (int)sizeof s - 700) {
    if (g_dirSrc == 1 && g_dirIdx >= 0 && g_dirIdx < g_n) {
      const MK* m = &g_mk[g_dirIdx];
      const char* nm2 = (m->type == MT_CROUCH) ? "蹲守点" : "守卫点";
      if (m->yaw > YAW_NONE + 1.0f)
        off += snprintf(s + off, sizeof s - (size_t)off,
                        "\n准星：%s #%d  朝向 %s %.0f°\n", nm2, g_dirIdx, yaw_zh(m->yaw), m->yaw);
      else
        off += snprintf(s + off, sizeof s - (size_t)off,
                        "\n准星：%s #%d  朝向未知（还没设）\n", nm2, g_dirIdx);
    } else if (g_dirSrc == 2 && g_dirIdx >= 0) {
      int nn = g_vf[g_dirIdx].nyaw;
      if (nn > 0)
        off += snprintf(s + off, sizeof s - (size_t)off,
                        "\n准星：原生%s  朝向 %s %.0f°%s（原生点不能改）\n",
                        g_vf[g_dirIdx].kind == K_CROUCH ? "蹲守点" : "守卫点",
                        yaw_zh(g_vf[g_dirIdx].yaw[0]), g_vf[g_dirIdx].yaw[0],
                        nn > 1 ? " · 多个方向" : "");
      else
        off += snprintf(s + off, sizeof s - (size_t)off,
                        "\n准星：原生%s  朝向未知（zoomPos 是空的）\n",
                        g_vf[g_dirIdx].kind == K_CROUCH ? "蹲守点" : "守卫点");
    } else {
      off += snprintf(s + off, sizeof s - (size_t)off,
                      "\n准星没对着蹲守点 / 守卫点：先把准星移过去\n");
    }
    off += snprintf(s + off, sizeof s - (size_t)off,
                    "← / → 直接转（Shift 1°，普通 15°）· 5 执行选中项 · 0 返回\n"
                    "方向写进 zoomPos（世界目标点 = 点位 + 朝向×10 m，同高）：\n"
                    "  人机站到点上没敌人时，就朝这个方向张望\n");
  }
  /* 上一手到底做了什么（撤销/重做没有可见变化时，这里能看见原因） */
  if (g_wpHint[0] && off < (int)sizeof s - 220)
    off += snprintf(s + off, sizeof s - (size_t)off, "· %s\n", g_wpHint);
  if (off < (int)sizeof s - 80)
    off += snprintf(s + off, sizeof s - (size_t)off, "小键盘 8/2 上下   5 确认   0 返回   数字直选\n");
  ((set_txt_t)RVA(R_TEXT_SETTEXT))(g_menu, x_string_new(s), 0);
}

static void menu_open(void) {
  if (!g_wpMenuOn) { elog("wpmenu: disabled by cfg wp_menu=0"); return; }
  if (g_menu && !uobj_live(g_menu)) overlay_reset();
  if (!g_menu) overlay_init();
  g_wpMenuOpen = 1;
  g_wpMenuSel = 0;
  g_wpMenuSub = 0;
  g_wpMenuSubSel = 0;
  g_wpArm = 0;
  g_wpLinkStep = 0;
  elog("wpmenu: open");
  /* 准星射线自检（2026-11-26）：屏幕中心射线和 transform.forward 差多少度。
   * 0.00° = 投影本来就居中，以前选不中全是「落点不在方块那层表面」；
   * 明显不是 0 = 旧实现拿 forward 当准星使确实整体偏，这条就是修复的证据。 */
  {
    V3 o, d;
    char cn[64] = "?";
    P cam = ((cam_main_t)RVA(R_CAM_MAIN))(0);
    if (cam) {
      P go = ((get_go_t)RVA(R_GETGO))(cam, 0);
      P nm = go ? ((get_name_t)RVA(R_OBJ_NAME))(go, 0) : 0;
      if (nm) str_ascii(nm, cn, sizeof cn);
    }
    if (cam_xray(&o, &d))
      elog("wpmenu: 准星射线 o=(%.2f %.2f %.2f) d=(%.2f %.2f %.2f)，和 forward 差 %.2f°（相机 '%s'）",
           o.x, o.y, o.z, d.x, d.y, d.z, g_xrAng, cn);
    else
      elog("wpmenu: 准星射线取不到（Camera.main / ScreenPointToRay 失败），选点退回 forward");
  }
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
  /* 连续模式下的 Esc / 0：只结束"当前这种动作"，人停在类型页/方向页，
   * 想换类型直接 1-6、想换方向直接 1-3，不用重开菜单（2026-11-20 用户需求：
   * "保持某一种类型的编辑，除非想换种类再 Esc 回退一下"）。 */
  if (g_wpArm) {
    g_wpArm = 0;
    if (g_wpMenuSub != 1) g_wpMenuSub = 1;
    elog("wpmenu: 结束连续放置（类型 %s 记着，Esc 再按一次回主菜单）", wp_brush_label(g_wpBrush));
    menu_refresh();
    return;
  }
  if (g_wpLinkStep) {
    g_wpLinkStep = 0;
    g_nedHasA = 0;
    if (g_wpMenuSub != 2) g_wpMenuSub = 2;
    elog("wpmenu: 结束连续连线（方向 %s 记着，Esc 再按一次回主菜单）", WP_PATHS[g_wpPath]);
    menu_refresh();
    return;
  }
  if (g_wpMenuSub) { g_wpMenuSub = 0; g_wpMenuSubSel = 0; menu_refresh(); return; }
  menu_close();
}

static void menu_move(int delta) {
  int n = g_wpMenuSub ? menu_sub_count() : WP_MENU_N;
  if (!n) return;
  if (g_wpMenuSub) {
    g_wpMenuSubSel = (g_wpMenuSubSel + delta + n) % n;
    /* 连续模式里 8/2 就是"换类型 / 换方向"：高亮一变就生效，
     * 否则 8/2 挪了高亮、按 5 放的却还是旧类型，很容易放错。 */
    if (g_wpMenuSub == 1 && g_wpArm) {
      set_brush(wp_type_brush(g_wpMenuSubSel));
    } else if (g_wpMenuSub == 2 && g_wpLinkStep) {
      g_wpPath = g_wpMenuSubSel;
      g_nedHasA = 0;
      g_wpLinkStep = 1;
      elog("wpmenu: 换方向 dir=%d（A 清掉，重新选起点）", g_wpPath);
    } else if (g_wpMenuSub == 7) {
      /* 高亮即选中：8/2 挪到哪一类，5/Delete 就删哪一类 */
      g_delType = WP_DELPT_TYPE[g_wpMenuSubSel];
      elog("wpmenu: 删除类型 = %s", mt_name(g_delType));
    } else if (g_wpMenuSub == 8) {
      g_delType = MT_AREA;
      elog("wpmenu: 删除区域 = 守卫区");
    }
  } else {
    g_wpMenuSel = (g_wpMenuSel + delta + n) % n;
  }
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
  if (!strcmp(name, "spawn_bl") || !strcmp(name, "spawnbl")) return 6;
  if (!strcmp(name, "spawn_gr") || !strcmp(name, "spawngr")) return 7;
  if (!strcmp(name, "spawn_nt") || !strcmp(name, "spawnnt")) return 8;
  if (!strcmp(name, "spawn_neutral") || !strcmp(name, "neutral")) return 8;
  return 0;
}

static const char* brush_name(int b) {
  static const char* n[WP_BRUSH_N] = { "normal", "jump", "crouch", "guard", "area", "tag",
                                       "spawn_bl", "spawn_gr", "spawn_nt" };
  return (b >= 0 && b < WP_BRUSH_N) ? n[b] : "normal";
}

static void set_brush(int b) {
  if (b < 0 || b >= WP_BRUSH_N) b = 0;
  g_wpBrush = b;
  strncpy(g_wpBrushName, brush_name(b), sizeof g_wpBrushName - 1);
  g_wpBrushName[sizeof g_wpBrushName - 1] = 0;
  elog("wpmenu: brush=%s", g_wpBrushName);
  menu_refresh();
}

/* ---- 朝向工具：把准星对着的那个点位改朝向（2026-11-27）--------------------
 * 只改**我们自己放的**蹲守点 / 守卫点（g_mk）：原生点是场景资产，改了不落盘、
 * 重进图就没了，所以直接拒绝并说明，而不是给个假象。
 * 写游戏 = zoomPos 一个元素 {p + dir*10 m, 同高}；见文件顶部 zoomPos 说明。 */
static int dir_apply(float yaw, const char* why) {
  MK* m;
  if (g_dirSrc != 1 || g_dirIdx < 0 || g_dirIdx >= g_n) {
    if (g_dirSrc == 2) toast_bad("这是原生点位，朝向改不了（只能改自己放的）");
    else toast_bad("准星先对着你放的蹲守点 / 守卫点");
    elog("dir: 无法设置朝向（src=%d idx=%d why=%s）", g_dirSrc, g_dirIdx, why ? why : "?");
    return 0;
  }
  m = &g_mk[g_dirIdx];
  if (m->type != MT_CROUCH && m->type != MT_NANOPOS) {
    toast_bad("这个点上没有朝向（只有蹲守点 / 守卫点有）");
    return 0;
  }
  if (yaw <= YAW_NONE + 1.0f) {
    /* 清空：游戏要求 zoomPos 至少 1 个（AddRange / GetRandomZoomPos 都会碰它），
     * 所以留一个正北兜底，但**我们不认这个值**：MK.yaw = 未知，显示照旧画虚线。
     * 这样既不崩，也不骗人 —— 菜单/浮字写「未知」。 */
    m->yaw = YAW_NONE;
    if (m->comp) write_zoom(m->comp, &m->p, 0.0f);
    elog("dir: #%d 朝向清空（游戏侧兜底正北，插件按未知显示）", g_dirIdx);
    toast_ok("已清空朝向：显示为未知（游戏里兜底朝北）");
  } else {
    m->yaw = yaw_norm(yaw);
    if (m->comp) write_zoom(m->comp, &m->p, m->yaw);
    elog("dir: #%d 朝向 -> %.0f°（%s）", g_dirIdx, m->yaw, yaw_zh(m->yaw));
    toast_ok("朝向 %s %.0f° %s", yaw_zh(m->yaw), m->yaw, why ? why : "");
  }
  editor_dirty_mk();
  g_dirSig = 0;                 /* 强制下一帧重建方向层 */
  menu_refresh();
  return 1;
}
static int dir_rotate(float delta) {
  float base;
  if (g_dirSrc != 1 || g_dirIdx < 0 || g_dirIdx >= g_n) {
    dir_apply(0.0f, "?");       /* 走同一条提示（会 toast 原因） */
    return 0;
  }
  base = (g_mk[g_dirIdx].yaw > YAW_NONE + 1.0f) ? g_mk[g_dirIdx].yaw : 0.0f;
  return dir_apply(base + delta, delta > 0 ? "顺时针" : "逆时针");
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
    if (i == 0) { g_wpMenuSub = 1; g_wpMenuSubSel = wp_type_index(g_wpBrush); menu_refresh(); return; }
    if (i == 1) { g_wpMenuSub = 2; g_wpMenuSubSel = g_wpPath; menu_refresh(); return; }
    /* 2026-11-25 用户要求：守卫区工具从第 6 项挪到第 3 项（建立路径之后、
     * 删除点图连线之前）——新建/加点用得最多，别每次往下数到 6。 */
    if (i == 2) {
      g_wpMenuSub = 3;
      g_wpMenuSubSel = 0;
      elog("wpmenu: 守卫区工具 —— 选中项在准星处画虚线预置框（只预览），按 5 才创建");
      menu_refresh();
      return;
    }
    if (i == 3) { g_wpMenuSub = 6; g_wpMenuSubSel = 0; menu_refresh(); return; }
    if (i == 4) {
      /* 删除点位：先进类型页，别在"最近"上盲删（2026-11-25 用户要求）。
       * 这里只切类型；真正删除要再按 5 / Delete，防手滑。 */
      int k;
      g_wpMenuSub = 7;
      g_wpMenuSubSel = -1;
      for (k = 0; k < WP_DELPT_N; k++) if (WP_DELPT_TYPE[k] == g_delType) g_wpMenuSubSel = k;
      /* 刚从「删除区域」页过来时 g_delType 还是 MT_AREA：点位页没有这个类型，
       * 不清掉的话按 5 会在点位页里把守卫区删了。 */
      if (g_wpMenuSubSel < 0) g_delType = -1;
      menu_refresh();
      return;
    }
    if (i == 5) {
      /* 删除区域：单独一页，默认就是守卫区。 */
      g_wpMenuSub = 8;
      g_wpMenuSubSel = 0;
      g_delType = MT_AREA;
      menu_refresh();
      return;
    }
    if (i == 6) { nav_ground_here(); menu_refresh(); return; }
    if (i == 7) { g_wpMenuSub = 4; g_wpMenuSubSel = 0; menu_refresh(); return; }
    if (i == 8) {
      g_wpMenuSub = 9;
      g_wpMenuSubSel = 0;
      elog("wpmenu: 朝向工具 —— 准星对着你放的蹲守点/守卫点，5 执行；←/→ 直接转（Shift 1°）");
      menu_refresh();
      return;
    }
    if (i == 9) { g_wpMenuSub = 5; g_wpMenuSubSel = 0; menu_refresh(); return; }   /* 显示图层 */
    if (i == 10) { menu_close(); return; }
    return;
  }
  i = g_wpMenuSubSel;
  if (g_wpMenuSub == 1) {                 /* 类型：停在类型页，连续放置 */
    g_wpArm = 1;                          /* 先置位再 set_brush：它内部会重画一次 */
    g_wpMenuSubSel = i;
    set_brush(wp_type_brush(i));          /* 不再 g_wpMenuSub = 0：换类型不用重开菜单 */
    return;
  }
  if (g_wpMenuSub == 2) {                 /* 路径方向：停在方向页，连续连线 */
    g_wpPath = i;
    g_wpMenuSubSel = i;
    g_wpLinkStep = 1;
    g_nedHasA = 0;
    elog("wpmenu: path dir=%d 连续连线：先按 5 选 A（Esc 结束）", g_wpPath);
    menu_refresh();
    return;
  }
  if (g_wpMenuSub == 3) {                 /* 守卫区 */
    V3 p;
    int n0;
    if (i > 1) {                          /* 入口 / 逃跑点还没接：别开空步、别动脏标记 */
      elog("wpmenu: entrance/escape not wired yet（这一项还没接，图上不会变）");
      toast_bad("入口 / 逃跑点还没接线：这一项不会改图");
      menu_refresh();
      return;
    }
    if (!cam_point(&p)) { elog("wpmenu: no ground under crosshair"); return; }
    /* 2026-11-27：「加守卫点」只在已有守卫区里进行。区外不建点、也不连带新建一个区
     * （以前这里会 make_area + make_nanopos 一次建两个，看着像「点变成了区」）。 */
    if (i == 1 && area_at(&p) < 0) {
      elog("wpmenu: 准星不在任何守卫区里（%.2f %.2f %.2f）-> 不建守卫点；先「1 新建守卫区」",
           p.x, p.y, p.z);
      toast_bad("这里没有守卫区：先按 1 建区，再在区里加点");
      menu_refresh();
      return;
    }
    ed_step();
    n0 = g_n;
    p.y += 0.05f;
    if (i == 0) { make_area(30, p); }
    else if (i == 1) {
      /* 按落点归区：落在哪个 3 m 框里就挂哪个（区外已经被上面拦掉了） */
      int ai = area_at(&p);
      if (ai >= 0) {
        if (ai != g_curArea) {
          g_curArea = ai;
          elog("wpmenu: 准星落在守卫区 #%d（aid=%d）里，改成挂这个区", ai, g_mk[ai].aid);
        }
        make_nanopos(g_mk[ai].aid, p, 3, cam_dir_yaw());
      }
    } else {
      elog("wpmenu: entrance/escape not wired yet");
      toast_bad("入口 / 逃跑点还没接线：这一项不会改图");
    }
    mke_note_add(n0);                   /* 守卫区 / 守卫点也进撤销栈 */
    editor_dirty_mk();                  /* 手动保存：Ctrl+S 才写 markers.txt */
    menu_refresh();
    return;
  }
  if (g_wpMenuSub == 4) {                 /* 撤销 / 恢复 / 保存 */
    if (i == 0) ed_undo();
    else if (i == 1) ed_redo();
    else if (i == 2) editor_save_all();   /* 唯一保存入口：点图 + 标记一起写 */
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
  if (g_wpMenuSub == 6) {                 /* 删除：路径 / 路点（连续删，不弹回主菜单） */
    if (i == 0) nav_unlink_here();
    else nav_del_here();
    g_wpMenuSubSel = i;
    menu_refresh();
    return;
  }
  if (g_wpMenuSub == 7) {                 /* 删除点位：先选类型，真正删要再按 5/Delete */
    if (i < 0 || i >= 7) return;          /* 防御：menu_activate 的其它入口 */
    g_delType = WP_DELPT_TYPE[i];
    g_wpMenuSubSel = i;
    elog("wpmenu: 删除类型 = %s（准星对准对象后 5 / Delete 删除，可连续）", mt_name(g_delType));
    menu_refresh();
    return;
  }
  if (g_wpMenuSub == 8) {                 /* 删除区域：守卫区 */
    if (i < 0 || i >= 1) return;
    g_delType = MT_AREA;
    g_wpMenuSubSel = 0;
    elog("wpmenu: 删除区域 = 守卫区（准星对准区后 5 / Delete 删除）");
    menu_refresh();
    return;
  }
  if (g_wpMenuSub == 9) {                 /* 朝向工具 */
    if (i < 0 || i >= WP_DIR_N) return;
    g_wpMenuSubSel = i;
    if (i == 0) dir_apply(cam_dir_yaw(), "（相机朝向）");
    else if (i == 1) dir_rotate(+15.0f);
    else if (i == 2) dir_rotate(-15.0f);
    else if (i == 3) dir_apply(YAW_NONE, "清空");
    else {
      /* 射线 -> 扇形 -> 关 -> 射线：一次按键切一档，菜单里直接看当前值 */
      g_dirStyle = (g_dirStyle == 1) ? 2 : ((g_dirStyle == 2) ? 0 : 1);
      g_dirSig = 0;
      elog("wpmenu: 方向显示样式 -> %s", g_dirStyle == 0 ? "关" : (g_dirStyle == 2 ? "扇形" : "射线"));
      toast_ok("方向显示：%s", g_dirStyle == 0 ? "关" : (g_dirStyle == 2 ? "扇形" : "射线"));
    }
    menu_refresh();
    return;
  }
}

/* 菜单打开时，Enter / 左键：先放点，再执行当前项 */
static void menu_confirm(void) {
  if (!g_wpMenuOpen) return;
  if (g_wpArm) { wp_place(); menu_refresh(); return; }
  if (g_wpLinkStep) { nav_link_one(); menu_refresh(); return; }
  if (g_wpMenuSub == 7 || g_wpMenuSub == 8) {   /* 删除页：5 = 删当前选中的类型 */
    if (g_delType < 0) { elog("wpmenu: 先选删除类型（1-8）再按 5"); toast_bad("先选删除类型（1-8）再按 5"); }
    else if (!delete_nearest_of(g_delType))
      elog("wpmenu: 没删到（类型 %s）", mt_name(g_delType));
    menu_refresh();
    return;
  }
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
   * 这里直接走和游戏内 Delete 同一条路径；删除标记页里只删当前选中的类型。 */
  if (vk == VK_DELETE) {
    if (g_wpMenuSub == 7 || g_wpMenuSub == 8) {
      if (g_delType < 0) { elog("wpmenu: 先选删除类型（1-8）再按 Delete"); toast_bad("先选删除类型（1-8）再按 Delete"); }
      else if (!delete_nearest_of(g_delType))
        elog("wpmenu: 没删到（类型 %s）", mt_name(g_delType));
      menu_refresh();
    } else {
      editor_delete_nearest();
    }
    return 1;
  }

  /* 朝向工具页：← / → 直接转准星对着的那个点（Shift = 1°，普通 = 15°）。
   * 这两个键在菜单里原本是空着的（菜单只用 8/2/5/0），不会和移动、开火冲突。 */
  if (g_wpMenuSub == 9 && (vk == VK_LEFT || vk == VK_RIGHT)) {
    float step = (GetAsyncKeyState(VK_SHIFT) & 0x8000) ? 1.0f : 15.0f;
    dir_rotate(vk == VK_RIGHT ? step : -step);
    return 1;
  }
  if (vk == VK_NUMPAD8 || vk == VK_UP) { menu_move(-1); return 1; }
  if (vk == VK_NUMPAD2 || vk == VK_DOWN) { menu_move(1); return 1; }
  if (vk == VK_NUMPAD5 || vk == VK_CLEAR || vk == VK_RETURN) { menu_confirm(); return 1; }
  if (vk == VK_ESCAPE) {
    menu_back();
    return 1;
  }
  if (vk >= '0' && vk <= '9') {
    int i = (int)(vk - '1');
    if (vk == '0') {
      if (g_wpMenuSub) menu_back();
      else { g_wpMenuSel = WP_MENU_N - 1; menu_activate(); }
      return 1;
    }
    if (g_wpMenuSub) {
      if (i < menu_sub_count()) {
        g_wpMenuSubSel = i;
        /* 2026-11-26 用户要求：这几页的数字键只是「切换选中」，5 / 左键 / 回车才执行 ——
         *   3 守卫区工具：想选 1 结果直接建了一个区；
         *   4 撤销 / 恢复 / 保存：按 1 就直接撤销；
         *   6 删除点图连线 / 路点：按 1 就直接断边（破坏性最强）。
         * 添加点位(1)/建立路径(2) 不在此列：那里数字键=选类型/方向并上膛，是效率来源。 */
        if (g_wpMenuSub == 3 || g_wpMenuSub == 4 || g_wpMenuSub == 6) {
          elog("wpmenu: 选中 %d（%s）—— 按 5 / 左键 才执行", i + 1, menu_sub_label(i));
          menu_refresh();
        } else {
          menu_activate();
        }
      }
    } else if (i >= 0 && i < WP_MENU_N) {
      g_wpMenuSel = i;
      /* 主菜单里只有第 6 项「落地 / 贴地」是直接改数据的动作：也先选，5 才执行。
       * 1-5 / 7 / 8 是进子页、9 是关菜单，属于导航，按数字照旧立刻生效。 */
      if (i == 6) {
        elog("wpmenu: 选中 6（落地 / 贴地）—— 按 5 / 左键 才执行");
        menu_refresh();
      } else {
        menu_activate();
      }
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
  /* 抬起 E 无条件复位。以前这行藏在 !g_wpEFired 里面，第一次长按成功后
   * g_wpEFired 一直是 1，复位永远执行不到，g_wpEDownAt 再也清不掉，
   * 于是整个进程里长按 E 只有第一次有效。 */
  if (!(GetAsyncKeyState('E') & 0x8000)) { g_wpEDownAt = 0; g_wpEFired = 0; }
  if (g_wpMenuOn && g_wpEDownAt && !g_wpEFired) {
    if (GetTickCount() - g_wpEDownAt >= 450) {
      g_wpEFired = 1;
      menu_toggle();
    }
  }
  if (g_wpMenuOpen && (tick % 3) == 0) menu_refresh();
}

/* ---- 人机探针 / bot 采样共用的小工具 --------------------------------------
 * 2026-11-27 删掉了「人机巡线驱动 drive」（用户实测判定没用：空白图上没有可走点
 * 时它完全静默、对正常地图又不生效，留着只会误导）。这里保留探针与 bot 采样
 * 还要用的声明。 */
static P g_prBotCls, g_prBotType, g_prStopFld;
static int pr_readable(P p, size_t n);
typedef struct { P bot; V3 p; unsigned t; } BPOS;
static BPOS g_bp[32];

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
      {
        /* 2026-11-24：给 beh 行补「是否在地面 / 竖直速度」——判断人机到底有没有起跳
         * 就靠这两个：起跳瞬间 vy 会到 10 左右、g 变 0；光看 5 s 一次的坐标会漏掉 0.7 s 的跳。 */
        P bpl = pr_readable((char*)b + 0x24, 0x10) ? *(P*)((char*)b + 0x24) : 0;
        int bg = -1;
        double bvy = 0.0;
        if (bpl && pr_readable(bpl, 0x100)) {
          P vel = *(P*)((char*)bpl + 0x90);
          bg = *(unsigned char*)((char*)bpl + 0x70) ? 1 : 0;
          if (vel && pr_readable(vel, 0x18)) bvy = *(float*)((char*)vel + 0x10);
        }
        /* 2026-11-24：把 Bot 的跳跃状态也打出来 —— 人机到底有没有"认出这条跳链"，
         * 就看 nextJumpStartNode(+0xC8) 是不是空：
         *   空   = OnPathComplete 里那段"路径下一个节点 == 跳链 endNode"的判定没命中
         *   非空 = 认出来了，但 canJump / isArriveJumpStartNode / needSpeed 把它挡住了 */
        {
          P njs = pr_readable((char*)b + 0xC8, 4) ? *(P*)((char*)b + 0xC8) : 0;
          P nend = pr_readable((char*)b + 0xD0, 4) ? *(P*)((char*)b + 0xD0) : 0;
          float nspd = pr_readable((char*)b + 0xD4, 4) ? *(float*)((char*)b + 0xD4) : -1.0f;
          float nacc = pr_readable((char*)b + 0xD8, 4) ? *(float*)((char*)b + 0xD8) : -1.0f;
          float ntime = pr_readable((char*)b + 0xE8, 4) ? *(float*)((char*)b + 0xE8) : -1.0f;
          elog("beh: bot=%p p=(%.1f,%.1f,%.1f) spd=%.2f acts=[%s] isS=%d tgt=(%.1f,%.1f,%.1f) over=%d reach=%d path=%p pts=%d enemy=%p enemyD=%.1f nearN=%p nearD=%.1f nextN=%p g=%d vy=%.1f njs=%p njend=%p njspeed=%.1f njacc=%.2f njtime=%.2f",
               b, p.x, p.y, p.z, spd, names, isS, tp.x, tp.y, tp.z, over, reach,
               path, pts, enemy, enemyD, gnear, d, gnext, bg, bvy,
               njs, nend, nspd, nacc, ntime);
        }
      }
    }
    shown++;
  }
  elog("probe: bots=%d stopAllBot=%d", cnt, (int)st);
}

/* ---- 2026-11-20 寻路诊断：grow / keep 图里人机不动时，用一行日志定位 --------
 * 字段偏移（dump.cs，x86 32-bit）：
 *   AstarPath.pathProcessor    +0x88
 *   PathProcessor: queue +0x14, pathHandlers +0x20
 *   ThreadControlQueue: head +0x8, tail +0xC, numReceivers +0x14,
 *                       blocked +0x18, blockedReceivers +0x1C
 *   PathHandler:  pathID(ushort) +0x8       每条线程算一条路就 +1
 *   GraphNode:    nodeIndex +0x8, flags +0xC（bit0 = 可走）
 *   Bot:          path +0x80, gNode_Nearset +0x88, gNode_Next +0x8C,
 *                 nextFindPathTime +0xB8（只有 Bot.PathSetting 会写它）, blockedTime +0xEC
 * 判读（ask = 1 s 内 nextFindPathTime 变了几次）：
 *   ask 涨、phSum 不动        → 人机请求了，但 path 没开始算（StartPath 被拒 / 队列卡住）
 *   ask 涨、phSum 涨、path=0  → 算完了没装车（回调没触发 / OnPathComplete 丢弃）
 *   ask 恒 0                  → 上层 AI 根本没请求移动，和寻路无关
 * qBlk=1 = 队列还停在 blocked（我们的 Lock 没解开）；qRcv = 寻路线程数。
 * b0 near/next 的 /1 = 该节点可走，/0 = 不可走（指向被标死的原生点就会是 0）；
 * near 下标 < walk 基线时是原生点，>= 基线就是新建点。 */
static P bot_type_get(void) {
  if (g_prBotType) return g_prBotType;
  g_prBotCls = find_cls("", "Bot");
  if (!g_prBotCls || !x_class_get_type) return 0;
  g_prBotType = x_type_get_object ? x_type_get_object(x_class_get_type(g_prBotCls)) : 0;
  if (x_class_get_field_from_name) g_prStopFld = x_class_get_field_from_name(g_prBotCls, "stopAllBot");
  return g_prBotType;
}
/* ---- 人机会话采样（10 Hz，k="b"）2026-11-26，2026-11-27 并入采样会话 ----
 * 字段只取「分析用得上」的：位置/着地/竖直速度/水平速度/行为名/闲逛目标/有没有敌人。
 * id 用 Bot 指针（同一次会话内稳定）。只在 who=bots|all 时才跑，只采玩家时一行不写。
 * 录制页（人机验证）和采集页（批量取证）走的是同一个函数。 */
/* 蹲跳：每 ~100 ms 扫一遍人机，空中 + 正走这条蹲跳链 -> 把 crouchEndTime 顶住。
 * 判据只用「已经在空中」（g=0）：「还在地面」时先不蹲，免得蹲着跳不起来。 */
static void crouch_jump_tick(void) {
  static unsigned last;
  static unsigned long long lastLog;
  unsigned long long now = GetTickCount64();
  P arr, bt;
  int n, i, k;
  if (!g_cjN) return;
  if (!cfg_bool("bot_crouchjump", 1)) return;
  if (now - last < 100) return;
  last = (unsigned)now;
  bt = bot_type_get();
  if (!bt) return;
  arr = ((find_objs_t)RVA(R_FINDOBJS))(bt, 1, 0);
  if (!arr) return;
  n = *(int*)((char*)arr + 0x0C);
  if (n <= 0 || n > 32) return;
  for (i = 0; i < n; i++) {
    P b = *(P*)((char*)arr + 0x10 + i * 4), pl, njs;
    if (!b || !uobj_live(b) || !pr_readable(b, 0xF4)) continue;
    njs = *(P*)((char*)b + 0xC8);                       /* Bot.nextJumpStartNode */
    if (!njs) continue;
    for (k = 0; k < g_cjN; k++) if (g_cj[k].startNode == njs) break;
    if (k >= g_cjN) continue;
    pl = pr_readable((char*)b + 0x24, 0x10) ? *(P*)((char*)b + 0x24) : 0;
    if (!pl || !pr_readable(pl, 0x100)) continue;
    if (*(unsigned char*)((char*)pl + 0x70)) continue;   /* 还在地面：等它跳起来 */
    *(float*)((char*)b + 0xF0) =                         /* Bot.crouchEndTime */
        ((float (*)(void*))RVA(R_TIME_GET))(0) + 0.6f;
    if (now - lastLog > 1000) {
      lastLog = now;
      elog("crouchjump: bot=%p 空中，顶 crouchEndTime（链 ct=[%.2f, %.2f]）",
           b, g_cj[k].ct0, g_cj[k].ct1);
    }
  }
}

static void ss_sample_bots(void) {
  static struct { P bot; V3 p; unsigned t; } bp[32];
  unsigned long long now = GetTickCount64();
  double t;
  P arr, bt;
  int n, i, k;
  if (!g_ss.fp || !(g_ss.who & 2)) return;
  if (now < g_ss.botNext) return;
  g_ss.botNext = now + (1000 / SS_BOT_HZ);
  if (!g_ss.hdr) {
    /* 只采人机（who=bots）时没有玩家样本，header 在这里写：时间原点从这台人机算起 */
    QueryPerformanceCounter(&g_ss.t0q);
    g_ss.srcMode = 1;
    g_ss.nextT = 1.0 / (double)g_ss.hz;
    memset(bp, 0, sizeof bp);          /* 新会话：速度基线别拿上一场的样本算 */
    ss_header();
  }
  t = ss_now();
  bt = bot_type_get();
  if (!bt) return;
  arr = ((find_objs_t)RVA(R_FINDOBJS))(bt, 1, 0);
  if (!arr) return;
  n = *(int*)((char*)arr + 0x0C);
  if (n < 0) n = 0;
  if (n > 32) n = 32;
  for (i = 0; i < n; i++) {
    P b = *(P*)((char*)arr + 0x10 + i * 4), tr, sa, pl, vel, acts;
    V3 p, tgt;
    P njs = 0, nearN = 0, path = 0;
    int pts = -1;
    float vy = 0.0f, spd = -1.0f, dt;
    int g = -1, en = 0, j = 0, an = 0, ai;
    char names[120];
    if (!b || !uobj_live(b) || !pr_readable(b, 0xE0)) continue;
    tr = ((get_tr_t)RVA(R_COMP_TR))(b, 0);
    if (!tr) continue;
    ((get_pos_t)RVA(R_GET_POS_INJ))(tr, &p, 0);
    pl = pr_readable((char*)b + 0x24, 0x10) ? *(P*)((char*)b + 0x24) : 0;
    if (pl && pr_readable(pl, 0x100)) {
      g = *(unsigned char*)((char*)pl + 0x70) ? 1 : 0;
      vel = *(P*)((char*)pl + 0x90);
      if (vel && pr_readable(vel, 0x18)) vy = *(float*)((char*)vel + 0x10);
    }
    j = (g == 0) ? 1 : 0;
    sa = pr_readable((char*)b + 0x64, 0x30) ? *(P*)((char*)b + 0x64) : 0;
    tgt.x = tgt.y = tgt.z = 0.0f;
    if (sa && pr_readable(sa, 0x30)) {
      tgt.x = *(float*)((char*)sa + 0x14);
      tgt.y = *(float*)((char*)sa + 0x18);
      tgt.z = *(float*)((char*)sa + 0x1C);
    }
    if (pr_readable((char*)b + 0x28, 0x10)) en = *(P*)((char*)b + 0x28) ? 1 : 0;
    acts = *(P*)((char*)b + 0x58);
    names[0] = 0;
    if (pr_readable(acts, 0x20)) {
      P items = *(P*)((char*)acts + 0x8);
      an = *(int*)((char*)acts + 0xC);
      if (pr_readable(items, 0x20)) {
        int lim = an > 3 ? 3 : an;
        for (ai = 0; ai < lim; ai++) {
          P o = *(P*)((char*)items + 0x10 + ai * 4);
          const char* nm = pr_readable(o, 0x10) ? type_name(*(P*)o) : "?";
          if (nm && !strncmp(nm, "BotAction.", 10)) nm += 10;
          if (ai) strncat(names, "|", sizeof names - strlen(names) - 1);
          strncat(names, nm ? nm : "?", sizeof names - strlen(names) - 1);
        }
      }
    }
    for (k = 0; k < 32; k++) if (bp[k].bot == b) break;
    if (k == 32) {
      for (k = 0; k < 32; k++) if (!bp[k].bot) { bp[k].bot = b; bp[k].p = p; bp[k].t = (unsigned)now; break; }
    }
    if (k < 32 && bp[k].bot == b) {
      dt = (float)((unsigned)now - bp[k].t) / 1000.0f;
      if (dt > 0.05f) {
        spd = sqrtf((p.x - bp[k].p.x) * (p.x - bp[k].p.x) + (p.z - bp[k].p.z) * (p.z - bp[k].p.z)) / dt;
        bp[k].p = p; bp[k].t = (unsigned)now;
      }
    }
    njs = pr_readable((char*)b + 0xC8, 4) ? *(P*)((char*)b + 0xC8) : 0;
    nearN = pr_readable((char*)b + 0x88, 4) ? *(P*)((char*)b + 0x88) : 0;
    path = *(P*)((char*)b + 0x80);
    if (pr_readable(path, 0x40)) {
      P lst = *(P*)((char*)path + 0x2C);
      if (pr_readable(lst, 0x20)) pts = *(int*)((char*)lst + 0xC);
    }
    fprintf(g_ss.fp,
            "{\"t\":%.3f,\"k\":\"b\",\"id\":\"%08x\",\"x\":%.3f,\"y\":%.3f,\"z\":%.3f,"
            "\"g\":%d,\"vy\":%.2f,\"spd\":%.2f,\"j\":%d,\"en\":%d,\"act\":\"%s\","
            "\"tgt\":[%.2f,%.2f,%.2f],\"njs\":\"%08x\",\"near\":\"%08x\",\"pts\":%d}\n",
            t, (unsigned)(size_t)b,
            p.x, p.y, p.z, g, vy, spd, j, en, names, tgt.x, tgt.y, tgt.z,
            (unsigned)(size_t)njs, (unsigned)(size_t)nearN, pts);
    g_ss.bn++;
  }
  for (k = 0; k < 32; k++) if (bp[k].bot && !uobj_live(bp[k].bot)) bp[k].bot = 0;
  fflush(g_ss.fp);
}

static void diag_gn(P nd, int* idx, int* walk) {
  *idx = -1; *walk = -1;
  if (!pr_readable(nd, 0x20)) return;
  *idx = *(int*)((char*)nd + 0x8);
  *walk = (int)(*(unsigned*)((char*)nd + 0xC) & 1u);
}
static void nav_diag(void) {
  static int on = -1;
  static struct { P bot; float t; } dl[32];
  P g = navfix_point_graph(), a, pp, q, phs, bt, arr;
  int i, j, n, bots = 0, withPath = 0, asks = 0, phN = 0, phSum = 0, bad = 0;
  int qHead = -1, qBlk = -1, qBr = -1, qRcv = -1, shown = 0;
  char b0[160];
  if (on < 0) on = cfg_bool("nav_diag", 1) ? 1 : 0;
  if (!on) return;
  if (!g_packName[0] || !(g_nedGrow || g_nedBlank)) return;  /* 只看测试包的空白/grow/keep 图 */
  if (g_sceneAge < 12) return;
  b0[0] = 0;
  a = navfix_astar();
  pp = a ? *(P*)((char*)a + 0x88) : 0;
  if (pr_readable(pp, 0x40)) {
    q = *(P*)((char*)pp + 0x14);
    if (pr_readable(q, 0x28)) {
      qHead = *(P*)((char*)q + 0x8) ? 1 : 0;
      qRcv = *(int*)((char*)q + 0x14);
      qBlk = (int)*(unsigned char*)((char*)q + 0x18);
      qBr = *(int*)((char*)q + 0x1C);
    }
    phs = *(P*)((char*)pp + 0x20);           /* PathHandler[] */
    if (pr_readable(phs, 0x20)) {
      int hn = *(int*)((char*)phs + 0xC);
      for (i = 0; i < hn && i < 32; i++) {
        P ph = *(P*)((char*)phs + 0x10 + i * 4);
        if (!pr_readable(ph, 0x20)) continue;
        phSum += (int)*(unsigned short*)((char*)ph + 0x8);
        phN++;
      }
    }
  }
  bt = bot_type_get();
  arr = bt ? ((find_objs_t)RVA(R_FINDOBJS))(bt, 1, 0) : 0;
  if (arr) {
    n = *(int*)((char*)arr + 0xC);
    if (n < 0) n = 0;
    if (n > 32) n = 32;
    for (i = 0; i < n; i++) {
      P b = *(P*)((char*)arr + 0x10 + i * 4);
      float t;
      if (!b || !uobj_live(b) || !pr_readable(b, 0xC0)) continue;
      bots++;
      if (*(P*)((char*)b + 0x80)) withPath++;
      t = *(float*)((char*)b + 0xB8);
      for (j = 0; j < 32; j++) if (dl[j].bot == b) break;
      if (j == 32)
        for (j = 0; j < 32; j++) if (!dl[j].bot) { dl[j].bot = b; dl[j].t = -1.0f; break; }
      if (j < 32) {
        if (dl[j].t >= 0.0f && dl[j].t != t) asks++;
        dl[j].t = t;
      }
      {
        int ni, nw;
        diag_gn(*(P*)((char*)b + 0x88), &ni, &nw);
        if (nw != 1) bad++;          /* 最近的节点不可走（或被死点顶掉）= 人机必站桩 */
        if (!shown) {
          int xi, xw;
          diag_gn(*(P*)((char*)b + 0x8C), &xi, &xw);
          sprintf(b0, " b0 near=%d/%d next=%d/%d p=%d blk=%.2f",
                  ni, nw, xi, xw, *(P*)((char*)b + 0x80) ? 1 : 0,
                  *(float*)((char*)b + 0xEC));
          shown = 1;
        }
      }
    }
    for (j = 0; j < 32; j++)
      if (dl[j].bot && !uobj_live(dl[j].bot)) { dl[j].bot = 0; dl[j].t = -1.0f; }
  }
  elog("diag: bots=%d path=%d bad=%d ask=%d phSum=%d phN=%d qHead=%d qBlk=%d qBr=%d qRcv=%d "
       "walk=%d/%d%s", bots, withPath, bad, asks, phSum, phN, qHead, qBlk, qBr, qRcv,
       pr_walk_count(g), g ? nav_count(g) : -1, b0);
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
  spawn_early_tick();         /* 出生点：MapManager 一出现就套（抢在人机第一次出生前） */
  spawn_tick();               /* 出生点覆盖：进图后重套 / 游戏重建数组后自愈 */
  menu_tick();                /* F2 / 长按 E 路点菜单 */
  toast_tick();               /* 屏幕中央提示：到点隐藏 */
  ss_tick();                  /* 采样会话（录制 / 采集同一套）：控制台开了才写文件，与可视化无关 */
  nav_edit_tick();            /* 等图稳定后自动套用本图的编辑（不看 vis 开关） */
  { static int pr; if ((++pr % 20) == 0) bot_probe(); }   /* 人机状态探针：~5 s 一次 */
  crouch_jump_tick();         /* 蹲跳：录到 ct 的跳链，人机在空中时顶成蹲（~10 Hz） */
  { static int dg; if ((++dg % 4) == 0) nav_diag(); }      /* 寻路诊断：~1 s 一行（只在测试包） */
  nm_tick();                  /* 可走面独立于可视化：Ctrl+V 关着也能显示 */
  compass_tick();             /* 方向罗盘独立于可视化：Ctrl+Shift+7 开关 */
  ghost_tick();               /* 放置前的虚影预览：独立于可视化，菜单一开就在 */
  dir_tick();                 /* 蹲守点 / 守卫点的朝向：只画准星正对着的那一个 */
  edge_dir_sync();            /* 单向边箭头：只有菜单开着才显示 */
  if (!g_visOn) {
    if ((++ticks % 8) == 0) overlay_refresh();   /* 可视化关着也保持面板数字是活的 */
    return;
  }
  if ((ticks % 60) == 0) {
    P pg = navfix_point_graph();
    elog("hb: interactive tick=%d age=%d nodes=%d vis=%d dirty=%d badtr=%d",
         ticks, g_sceneAge, pg ? *(int*)((char*)pg + 0xEC) : -1, g_visOn, g_visDirty, g_badTr);
  }
  /* 材质被卸载后，已经建好的那些网格不会自己换材质 —— 查一次，死了就整层重建 */
  if (g_visObjN && (ticks % 8) == 0) {
    int mi, dead = 0;
    for (mi = 1; mi <= 15; mi++)
      if (g_matSlot[mi] && !mat_alive(g_matSlot[mi])) { dead = 1; break; }
    if (dead) {
      elog("vis: material dead after scene load - rebuild all layers");
      mat_reset("material dead");
      g_visDirty = 1;
    }
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
  /* 待激活守卫区的金框每 tick 维护：不吃 VIS_SCENE_WAIT 的推迟（见 pend_area_tick 注释） */
  pend_area_tick();
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
  if (!ed_init()) return;

  /* 2026-11-26 用户要求：游戏内只留 F2 菜单 + Ctrl+S + Ctrl+V + Delete。
   * 下线的键：Ctrl+0/1/2/3/4/5/6/7/8/9（编辑模式那一套）、Ctrl+Shift+A/N/J/D/Z/R/S、
   * Ctrl+Shift+6/+7（可走面 / 罗盘）。理由：它们做的事 F2 菜单里都有；
   * 可视化那几类改成控制台「插件开关 → 可视化」实时下发（ucf_navcmd 的 cmd=vis），
   * 不再占手键，也不用为了切图层去记键位。
   * 同一天又删了 Ctrl+E（手动导出 JSON）和 Ctrl+Shift+X（只读采集）。 */
  if (shift) return;
  if (vk == 'S') { editor_save_all(); return; }          /* 唯一保存入口 */
  if (vk == 'V') { vis_toggle(); return; }               /* 可视化总开关（含标记球） */
  if (vk == VK_DELETE) { delete_nearest(); return; }     /* 删准星最近标记（原在编辑模式内） */
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
  if (editor_unsaved())
    elog("quit: 退出游戏，丢弃未保存的游戏内编辑（点图 %d 项 / 标记 %d 个）-- 只有 Ctrl+S 会落盘",
         g_nedN, g_n);
  ss_stop("quit");            /* 游戏退出：把采样文件收尾（写 end 行），别留半截 */
  elog("quit: editor stop (markers=%d vis nodes=%d features=%d)", g_n, g_vnN, g_vfN);
  nav_conn_roots_release();
}

/* ---- 车测自由视角（2026-11-18）----------------------------------------
 * 为什么需要：车测用 SceneManager.LoadScene 直接进图，没有玩家、没有玩家控制器，
 * 视角没人管。地图场景自带 Main Camera + CM FreeLook（Cinemachine 虚拟相机），
 * 所以不新建相机，只做两件事：
 *   1) 关掉 CM FreeLook，否则 CinemachineBrain 每帧把相机拽回它的机位；
 *   2) 每 10 ms（navfix 的 WM_TIMER）写一次 position / eulerAngles。
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
  ucf_log_file(g_log, sizeof g_log, g_dir, "ucf_mod.log");
  /* 四版路径先定下来：pack_init 要用 g_packRoot，可走面落盘要用 g_expDir。
   * 控制台启动游戏时会带 UCF_EXPORT_DIR / UCF_PACK_DIR / UCF_NAV_READONLY。 */
  {
    char def[MAX_PATH], ro[8];
    sprintf(def, "%s\\vis", g_dir);
    dir_choice("UCF_EXPORT_DIR", "export_dir", def, g_expDir, sizeof g_expDir);
    sprintf(def, "%s\\packs", g_dir);
    dir_choice("UCF_PACK_DIR", "pack_dir", def, g_packRoot, sizeof g_packRoot);
    ucf_mkdir_p(g_expDir);
    ucf_mkdir_p(g_packRoot);
    g_navReadOnly = (GetEnvironmentVariableA("UCF_NAV_READONLY", ro, sizeof ro) > 0 &&
                     ro[0] == '1') ? 1 : 0;
  }
  pack_init();   /* UCF_PACK / UCF_FP：这次读哪个目录、只对哪张图生效 */
  mk_set_path(); /* 编辑标记按地图分文件夹：markers\<包名>\markers.txt（pack_init 之后才知道包名） */
  /* 玩家坐标记录：和日志一起放 log\（控制台读同一份；旧部署的根目录那份仍兼容） */
  ucf_log_file(g_pmPath, sizeof g_pmPath, g_dir, "player_marks.txt");
  pm_load(0);
  /* 开关全部来自 ucf_mod.json（cfg.c）：这里各取一次，日志里写清楚，
   * 关掉哪个在日志里都看得见，不用猜。 */
  g_visOn      = cfg_bool("visualizer", 0);
  g_nmShow     = cfg_bool("navmesh_show", 1);
  g_visNodes   = cfg_bool("vis_nodes", 1);
  g_visNano    = cfg_bool("vis_nano", 1);
  g_visCrouch  = cfg_bool("vis_crouch", 1);
  g_visBorn    = cfg_bool("vis_born", 1);
  g_visSupply  = cfg_bool("vis_supply", 1);
  g_visJump    = cfg_bool("vis_jump", 1);
  g_visTag     = cfg_bool("vis_tag", 1);
  g_visPm      = cfg_bool("vis_player_marks", 1);
  g_visCompass = cfg_bool("vis_compass", 1);
  g_wpMenuOn   = cfg_bool("wp_menu", 1);
  g_wpAutoGround = cfg_bool("wp_autoground", 1);
  /* 方向层样式：0=关 1=射线 2=扇形（游戏里用「朝向工具」页切，cfg 只是记住上次） */
  g_dirStyle = cfg_int("wp_dir_style", 1);
  if (g_dirStyle < 0 || g_dirStyle > 2) g_dirStyle = 1;
  cfg_str("wp_brush", "normal", g_wpBrushName, sizeof g_wpBrushName);
  g_wpBrush    = brush_from_name(g_wpBrushName);
  /* 出生点：先把 markers 里的 spawn 行读进来（进图第一波出生比任何 tick 都早），
   * 再把游戏的取点函数换成我们的（spawn_hook=false 可整体关掉）。 */
  spawn_preload();
  /* 钩子不在这里装：此时 g_ga 还没有（ed_init 未跑），装了也是静默失败。
   * 真正安装点在 ed_init 末尾（日志里会出现 "spawn: hook GetSpawnPoint @…"）。 */
  if (!cfg_bool("spawn_hook", 1))
    elog("spawn: hook 被配置关掉（spawn_hook=false），第一波出生仍会用原生点");
  elog("editor ready: visualizer=%d navmesh=%d file=%s", g_visOn, g_nmShow, g_file);
  elog("wpmenu: on=%d autoground=%d brush=%s", g_wpMenuOn, g_wpAutoGround, g_wpBrushName);
  elog("vis data: nodes=%d nano=%d crouch=%d born=%d supply=%d jump=%d tag=%d",
       g_visNodes, g_visNano, g_visCrouch, g_visBorn, g_visSupply, g_visJump, g_visTag);
  elog("compass: vis_compass=%d (屏幕下方汉字罗盘；北=世界 -Z，Ctrl+Shift+7 开关)", g_visCompass);
  elog("navmesh dump dir=%s packs=%s officialNavSave=%s",
       g_expDir, g_packRoot, g_navReadOnly ? "blocked(read-only)" : "allowed");
  veh_install();   /* 挂了 VEH：任何崩溃都会把调用链写进 ucf_mod.log */
  { void autotest_start(const char*); autotest_start(g_dir); }   /* UCF_AUTOTEST=7,10 才动作 */
}
