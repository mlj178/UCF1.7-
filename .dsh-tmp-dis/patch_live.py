
import io, sys, os

base = r".dsh-tmp-dis\fixsrc"
ed = os.path.join(base, "editor.c")
nv = os.path.join(base, "navfix.c")
pl = os.path.join(base, "plugin.c")

def load(p):
    return open(p, encoding="utf-8", errors="surrogateescape").read()

def save(p, s):
    open(p, "w", encoding="utf-8", errors="surrogateescape", newline="").write(s)

def rep(s, old, new, name, count=1):
    n = s.count(old)
    if n != count:
        raise SystemExit("PATTERN %s count=%d (expected %d)" % (name, n, count))
    return s.replace(old, new)

# ---------------- editor.c ----------------
s = load(ed)

old = '''static int list_n(P l) { return l ? *(int*)((char*)l + 0x0C) : 0; }
static P list_items(P l) { return l ? *(P*)((char*)l + 0x08) : 0; }
static P comp_tr(P comp) { return ((get_tr_t)RVA(R_COMP_TR))(comp, 0); }
'''
new = '''static int list_n(P l) { return l ? *(int*)((char*)l + 0x0C) : 0; }
static P list_items(P l) { return l ? *(P*)((char*)l + 0x08) : 0; }
/* A destroyed UnityEngine.Object keeps its managed wrapper but clears
 * m_CachedPtr (+0x8).  Calling GetComponent/GetPosition on it raises a
 * managed MissingReferenceException.  There is no managed catch here, so
 * IL2CPP calls abort() -> the "Microsoft Visual C++ Runtime Library"
 * dialog.  This happens right after a scene change, when SpareAreaList /
 * SpareList_BL/GR still hold components from the previous level. */
static int uobj_live(P o) { return o && *(P*)((char*)o + 0x8) != 0; }
static P comp_tr(P comp) {
  if (!uobj_live(comp)) return 0;
  return ((get_tr_t)RVA(R_COMP_TR))(comp, 0);
}
'''
s = rep(s, old, new, "comp_tr")

# read_jump: guard endTr before Transform.get_position
old = '''      P endTr = *(P*)((char*)links + 0x10 + j * 28);
      V3 ep;
      if (!endTr) continue;
      ((get_pos_t)RVA(R_GET_POS_INJ))(endTr, &ep, 0);
'''
new = '''      P endTr = *(P*)((char*)links + 0x10 + j * 28);
      V3 ep;
      if (!uobj_live(endTr)) continue;
      ((get_pos_t)RVA(R_GET_POS_INJ))(endTr, &ep, 0);
'''
s = rep(s, old, new, "read_jump endTr")

# read_spawns: stale MapManager
old = '''  if (g_mmInstField) x_field_static_get_value(g_mmInstField, &mm);
  if (!mm) { miss("MapManager"); return; }
'''
new = '''  if (g_mmInstField) x_field_static_get_value(g_mmInstField, &mm);
  if (!uobj_live(mm)) { miss("MapManager"); return; }
'''
s = rep(s, old, new, "read_spawns mm")

# vis_clear: GetGameObject on stale label components
old = '''    if (g_lblComp[i]) {
      P go = ((get_go_t)RVA(R_GETGO))(g_lblComp[i], 0);
      if (go) ((destroy_t)RVA(R_DESTROY))(go, 0);
      g_lblComp[i] = 0;
      g_lblHidden[i] = 0;
    }
'''
new = '''    if (g_lblComp[i]) {
      if (uobj_live(g_lblComp[i])) {
        P go = ((get_go_t)RVA(R_GETGO))(g_lblComp[i], 0);
        if (uobj_live(go)) ((destroy_t)RVA(R_DESTROY))(go, 0);
      }
      g_lblComp[i] = 0;
      g_lblHidden[i] = 0;
    }
'''
s = rep(s, old, new, "vis_clear labels")

# vis_label_tick: main camera may be destroyed mid scene change
old = '''  cam = ((cam_main_t)RVA(R_CAM_MAIN))(0);
  if (!cam) return;
  ctr = get_tr(((get_go_t)RVA(R_GETGO))(cam, 0));
'''
new = '''  cam = ((cam_main_t)RVA(R_CAM_MAIN))(0);
  if (!uobj_live(cam)) return;
  ctr = get_tr(((get_go_t)RVA(R_GETGO))(cam, 0));
'''
s = rep(s, old, new, "vis_label cam")

save(ed, s)

# ---------------- navfix.c ----------------
s = load(nv)

old = '''static P rptr(P o, int off) { return *(P*)((char*)o + off); }
'''
new = '''static P rptr(P o, int off) { return *(P*)((char*)o + off); }
/* UnityEngine.Object.m_CachedPtr; 0 means the native object was destroyed. */
static int n_live(P o) { return o && *(P*)((char*)o + 0x8) != 0; }
'''
s = rep(s, old, new, "n_live")

old = '''  P v = 0;
  i_field_static_get_value(f, &v);
  return v;
}

static P point_graph(P astar) {
  if (!astar) return 0;
'''
new = '''  P v = 0;
  i_field_static_get_value(f, &v);
  return n_live(v) ? v : 0;
}

static P point_graph(P astar) {
  if (!n_live(astar)) return 0;
'''
s = rep(s, old, new, "astar_active + point_graph")

# get_mm live check
old = '''static P get_mm(void) {
  P v = 0;
  if (!g_mmInstField) return 0;
  i_field_static_get_value(g_mmInstField, &v);
  return v;
}
'''
new = '''static P get_mm(void) {
  P v = 0;
  if (!g_mmInstField) return 0;
  i_field_static_get_value(g_mmInstField, &v);
  return n_live(v) ? v : 0;
}
'''
s = rep(s, old, new, "get_mm")

# purge bounds
old = '''  items = *(P*)((char*)list + 0x8);
  n = *(int*)((char*)list + 0xC);
  if (!items || n <= 0) return;
  for (i = 0; i < n; i++) {
'''
new = '''  items = *(P*)((char*)list + 0x8);
  n = *(int*)((char*)list + 0xC);
  if (!items || n <= 0) return;
  {
    int cap = *(int*)((char*)items + 0xC);   /* array length, not list size */
    if (cap <= 0 || n > cap) { nlog("guard areas: bad list size %d/%d, skip purge", n, cap); return; }
  }
  for (i = 0; i < n; i++) {
'''
s = rep(s, old, new, "purge bounds")

# purge keep only live
old = '''    if (o && *(P*)((char*)o + 0x8)) *(P*)((char*)items + 0x10 + w++) = o;
'''
new = '''    if (n_live(o)) *(P*)((char*)items + 0x10 + w++) = o;
'''
s = rep(s, old, new, "purge live")

save(nv, s)

# ---------------- plugin.c ----------------
s = load(pl)

old = '''static P g_field;   /* UI_GameRoom singleton instance field */
'''
new = '''static P g_field;   /* UI_GameRoom singleton instance field */

/* UnityEngine.Object.m_CachedPtr; destroyed components leave a fake-null
 * managed wrapper.  Touching one from native code raises a managed
 * MissingReferenceException and aborts the process. */
static int p_live(P o) { return o && *(P*)((char*)o + 0x8) != 0; }
'''
s = rep(s, old, new, "p_live")

old = '''  p_field_static_get_value(g_field, &inst);
  if (!inst) return;
'''
new = '''  p_field_static_get_value(g_field, &inst);
  if (!p_live(inst)) return;
'''
s = rep(s, old, new, "plugin inst")

old = '''        P ma = *(P*)((char*)mapDatas + 0x10 + i*4);
        if (!ma) continue;
'''
new = '''        P ma = *(P*)((char*)mapDatas + 0x10 + i*4);
        if (!p_live(ma)) continue;
'''
s = rep(s, old, new, "plugin ma")

old = '''static int inject_one(P ma) {
  P arr = *(P*)((char*)ma + 0x14);
  if (!arr) return 0;
'''
new = '''static int inject_one(P ma) {
  P arr;
  if (!p_live(ma)) return 0;
  arr = *(P*)((char*)ma + 0x14);
  if (!arr) return 0;
'''
s = rep(s, old, new, "inject_one ma")

save(pl, s)

print("patched editor.c navfix.c plugin.c")
