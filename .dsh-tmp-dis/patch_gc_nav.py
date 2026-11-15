
import os
base = r".dsh-tmp-dis\fixsrc"
def load(p): return open(p, encoding="utf-8", errors="surrogateescape").read()
def save(p,s): open(p,"w",encoding="utf-8",errors="surrogateescape",newline="").write(s)
def rep(s, old, new, name, count=1):
    n=s.count(old)
    if n!=count: raise SystemExit("PATTERN %s count=%d expected %d" % (name,n,count))
    return s.replace(old,new)

p = os.path.join(base,"navfix.c")
s = load(p)

old = '''static P (*i_array_new)(P,unsigned int);
static P (*i_class_get_element_class)(P);
static void (*i_field_static_set_value)(P,void*);
'''
new = '''static P (*i_array_new)(P,unsigned int);
static P (*i_class_get_element_class)(P);
static void (*i_field_static_set_value)(P,void*);
static P (*i_gchandle_new)(P,unsigned char);
static void (*i_gchandle_free)(P);
'''
s = rep(s, old, new, "nav globals")

old = '''  RE(field_static_set_value);
  RE(field_static_get_value);
'''
new = '''  RE(field_static_set_value);
  RE(field_static_get_value);
  RE(gchandle_new); RE(gchandle_free);
'''
s = rep(s, old, new, "nav RE")

old = '''  list = i_object_new(g_listCls);
  if (!list) return 0;
  i_runtime_invoke(g_listCtor, list, 0, 0);
  wfield(comp, 0x10, list);                       /* posList (non-null, Awake iterates it) */

  nameStr = i_string_new("UCF_GuardPos");
  for (i = 0; i < npos; i++) {
'''
new = '''  list = i_object_new(g_listCls);
  if (!list) return 0;
  if (i_gchandle_new) hlist = (P)i_gchandle_new(list, 0);   /* List is not native-rooted */
  i_runtime_invoke(g_listCtor, list, 0, 0);
  wfield(comp, 0x10, list);                       /* posList (non-null, Awake iterates it) */

  nameStr = i_string_new("UCF_GuardPos");
  if (i_gchandle_new) hname = (P)i_gchandle_new(nameStr, 0);
  for (i = 0; i < npos; i++) {
'''
s = rep(s, old, new, "make_guard_area handles")

old = '''static P make_guard_area(V3 p, int npos) {
  P go, comp, list, nameStr;
'''
new = '''static P make_guard_area(V3 p, int npos) {
  P go, comp, list, nameStr;
  P hlist = 0, hname = 0;
'''
s = rep(s, old, new, "make_guard_area decl")

old = '''  if (madePos == 0) { nlog("area: no pos created"); return 0; }

  set_pos_of(go, p);
'''
new = '''  if (madePos == 0) {
    nlog("area: no pos created");
    if (hname && i_gchandle_free) i_gchandle_free(hname);
    if (hlist && i_gchandle_free) i_gchandle_free(hlist);
    return 0;
  }

  set_pos_of(go, p);
'''
s = rep(s, old, new, "make_guard_area cleanup")

old = '''  for (i = 0; i < madePos; i++) ((set_active_t)RVA(0x331CF0))(posgo[i], 1, 0);
  return comp;
'''
new = '''  for (i = 0; i < madePos; i++) ((set_active_t)RVA(0x331CF0))(posgo[i], 1, 0);
  if (hname && i_gchandle_free) i_gchandle_free(hname);
  if (hlist && i_gchandle_free) i_gchandle_free(hlist);
  return comp;
'''
s = rep(s, old, new, "make_guard_area release")

old = '''  for (i = 0; i < n; i++) {
    P arr = arr_new(g_areaCls, 3);
    P esc = arr_new(g_areaCls, 2);
    if (!arr) continue;
    {
      P* d = (P*)((char*)arr + 0x10);
      d[0] = g_areaComps[(i + 1) % n];
      d[1] = g_areaComps[(i + 5) % n];
      d[2] = g_areaComps[(i + 11) % n];
    }
    wfield(g_areaComps[i], 0x14, arr);
    if (esc) {
      P* e = (P*)((char*)esc + 0x10);
      e[0] = g_areaComps[(i + 3) % n];
      e[1] = g_areaComps[(i + 7) % n];
      wfield(g_areaComps[i], 0x18, esc);
    }
  }
'''
new = '''  for (i = 0; i < n; i++) {
    P arr = arr_new(g_areaCls, 3);
    P esc = 0;
    P harr = 0, hesc = 0;
    if (arr && i_gchandle_new) harr = (P)i_gchandle_new(arr, 0);
    esc = arr_new(g_areaCls, 2);
    if (esc && i_gchandle_new) hesc = (P)i_gchandle_new(esc, 0);
    if (!arr) {
      if (hesc && i_gchandle_free) i_gchandle_free(hesc);
      continue;
    }
    {
      P* d = (P*)((char*)arr + 0x10);
      d[0] = g_areaComps[(i + 1) % n];
      d[1] = g_areaComps[(i + 5) % n];
      d[2] = g_areaComps[(i + 11) % n];
    }
    wfield(g_areaComps[i], 0x14, arr);
    if (esc) {
      P* e = (P*)((char*)esc + 0x10);
      e[0] = g_areaComps[(i + 3) % n];
      e[1] = g_areaComps[(i + 7) % n];
      wfield(g_areaComps[i], 0x18, esc);
    }
    if (hesc && i_gchandle_free) i_gchandle_free(hesc);
    if (harr && i_gchandle_free) i_gchandle_free(harr);
  }
'''
s = rep(s, old, new, "link_guard_areas handles")

old = '''  P childName = i_string_new("wp");
  int made = 0;
'''
new = '''  P childName = i_string_new("wp");
  P hchild = 0;
  if (i_gchandle_new) hchild = (P)i_gchandle_new(childName, 0);
  int made = 0;
'''
s = rep(s, old, new, "childName handle")

old = '''  nlog("waypoint objects created=%d", made);
  if (made < 8) { nlog("waypoints too few, abort"); hold_bots(0); return; }
'''
new = '''  nlog("waypoint objects created=%d", made);
  if (made < 8) {
    nlog("waypoints too few, abort");
    if (hchild && i_gchandle_free) i_gchandle_free(hchild);
    hold_bots(0); return;
  }
'''
s = rep(s, old, new, "childName early release")

old = '''      P nameStr = i_string_new("CrouchPos");
      int made2 = 0;
'''
new = '''      P nameStr = i_string_new("CrouchPos");
      P hname2 = 0;
      if (i_gchandle_new) hname2 = (P)i_gchandle_new(nameStr, 0);
      int made2 = 0;
'''
s = rep(s, old, new, "crouch name handle")

old = '''      int now = spareList2 ? *(int*)((char*)spareList2 + 0xC) : -1;
      nlog("crouch: created=%d registered=%d", made2, now);
'''
new = '''      int now = spareList2 ? *(int*)((char*)spareList2 + 0xC) : -1;
      nlog("crouch: created=%d registered=%d", made2, now);
      if (hname2 && i_gchandle_free) i_gchandle_free(hname2);
'''
s = rep(s, old, new, "crouch name release")

old = '''  hold_bots(0);
  { void editor_mark_dirty(void); editor_mark_dirty(); }
}
'''
new = '''  if (hchild && i_gchandle_free) i_gchandle_free(hchild);
  hold_bots(0);
  { void editor_mark_dirty(void); editor_mark_dirty(); }
}
'''
s = rep(s, old, new, "childName release")

save(p,s)
print("navfix patched")
