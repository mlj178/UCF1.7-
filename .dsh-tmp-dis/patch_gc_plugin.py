
import os
base = r".dsh-tmp-dis\fixsrc"
p = os.path.join(base,"plugin.c")
s = open(p, encoding="utf-8", errors="surrogateescape").read()
def rep(s, old, new, name, count=1):
    n=s.count(old)
    if n!=count: raise SystemExit("PATTERN %s count=%d expected %d" % (name,n,count))
    return s.replace(old,new)

old = '''static P (*p_thread_attach)(P);
static void (*p_runtime_class_init)(P);
'''
new = '''static P (*p_thread_attach)(P);
static void (*p_runtime_class_init)(P);
static P (*p_gchandle_new)(P, unsigned char);
static void (*p_gchandle_free)(P);
'''
s = rep(s, old, new, "plugin globals")

old = '''  RE(string_new); RE(thread_attach);
'''
new = '''  RE(string_new); RE(thread_attach);
  RE(gchandle_new); RE(gchandle_free);
'''
s = rep(s, old, new, "plugin RE")

old = '''static int inject_one(P ma) {
  P arr;
  if (!p_live(ma)) return 0;
  arr = *(P*)((char*)ma + 0x14);
  if (!arr) return 0;
  int n = *(int*)((char*)arr + 0xC);
  char* data = (char*)arr + 0x10;
  for (int i = 0; i < n; i++) if (str_eq_il2cpp(*(P*)(data + i*0x1C), gScene)) return 0;
  P klass = *(P*)arr;
  P elem = p_class_get_element_class(klass);
  P na = p_array_new(elem, n+1);
  if (!na) return 0;
  memcpy((char*)na + 0x10, data, n*0x1C);
  memcpy((char*)na + 0x10 + n*0x1C, data, 0x1C);
  *(P*)((char*)na + 0x10 + n*0x1C) = p_string_new(gScene);
  *(P*)((char*)na + 0x10 + n*0x1C + 4) = p_string_new(gLabel);
  p_wbarrier(ma, (char*)ma + 0x14, na);
  *(P*)((char*)ma + 0x14) = na;
  return n + 1;
}
'''
new = '''static int inject_one(P ma) {
  P arr, klass, elem, na, sScene, sLabel;
  P hna = 0, hs = 0, hl = 0;
  int n, i;
  char* data;
  if (!p_live(ma)) return 0;
  arr = *(P*)((char*)ma + 0x14);
  if (!arr) return 0;
  n = *(int*)((char*)arr + 0xC);
  data = (char*)arr + 0x10;
  for (i = 0; i < n; i++) if (str_eq_il2cpp(*(P*)(data + i*0x1C), gScene)) return 0;

  /* Strings/arrays are managed objects held only in native locals here.  Root
   * them across the next allocations: a GC in p_array_new/p_string_new would
   * otherwise free them and the MapAsset field would point at dead memory,
   * which crashes the next GC (0xC0000005 in GameAssembly GC mark). */
  sScene = p_string_new(gScene);
  if (p_gchandle_new) hs = (P)p_gchandle_new(sScene, 0);
  sLabel = p_string_new(gLabel);
  if (p_gchandle_new) hl = (P)p_gchandle_new(sLabel, 0);

  klass = *(P*)arr;
  elem = p_class_get_element_class(klass);
  na = p_array_new(elem, n+1);
  if (!na) {
    if (hs && p_gchandle_free) p_gchandle_free(hs);
    if (hl && p_gchandle_free) p_gchandle_free(hl);
    return 0;
  }
  if (p_gchandle_new) hna = (P)p_gchandle_new(na, 0);

  memcpy((char*)na + 0x10, data, n*0x1C);
  memcpy((char*)na + 0x10 + n*0x1C, data, 0x1C);
  *(P*)((char*)na + 0x10 + n*0x1C) = sScene;
  *(P*)((char*)na + 0x10 + n*0x1C + 4) = sLabel;
  p_wbarrier(ma, (char*)ma + 0x14, na);
  *(P*)((char*)ma + 0x14) = na;

  if (hna && p_gchandle_free) p_gchandle_free(hna);
  if (hl && p_gchandle_free) p_gchandle_free(hl);
  if (hs && p_gchandle_free) p_gchandle_free(hs);
  return n + 1;
}
'''
s = rep(s, old, new, "inject_one gchandles")

open(p,"w",encoding="utf-8",errors="surrogateescape",newline="").write(s)
print("plugin patched")
