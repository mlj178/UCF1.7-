
p = r".dsh-tmp-dis\fixsrc\editor.c"
s = open(p, encoding="utf-8", errors="surrogateescape").read()
old = '''typedef void* P;
typedef struct { float x, y, z; } V3;
typedef struct { float x, y; } V2;
typedef struct { float r, g, b, a; } COL;
'''
new = '''typedef void* P;
typedef struct { float x, y, z; } V3;
typedef struct { float x, y; } V2;
typedef struct { float r, g, b, a; } COL;

/* UnityEngine.Object.m_CachedPtr (+0x8) is cleared when the native object is
 * destroyed.  Touching a destroyed component from native code raises a managed
 * MissingReferenceException; IL2CPP cannot unwind into C, so it aborts. */
static int uobj_live(P o) { return o && *(P*)((char*)o + 0x8) != 0; }
'''
assert s.count(old) == 1
s = s.replace(old, new)
old2 = ''' * Everything that walks a game-owned static list after a scene change must
 * test this first. */
static int uobj_live(P o) { return o && *(P*)((char*)o + 0x8) != 0; }
static P comp_tr(P comp) {
'''
new2 = ''' * Everything that walks a game-owned static list after a scene change must
 * test this first. */
static P comp_tr(P comp) {
'''
assert s.count(old2) == 1
s = s.replace(old2, new2)
open(p, "w", encoding="utf-8", errors="surrogateescape", newline="").write(s)
print("moved uobj_live")
