
import UnityPy, os, math
BASE = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\\UnityCrossFire_Data"
def load(lvl):
    env = UnityPy.load(os.path.join(BASE,lvl))
    sf = list(env.files.values())[0]; objs = sf.objects
    tr_go, trd, goes = {}, {}, {}
    for pid_, o in objs.items():
        t = o.type.name
        if t == "GameObject":
            go = o.read(); goes[pid_] = (go.m_Tag, go.m_IsActive)
            for c in go.m_Component:
                p = c.component
                if p.path_id in objs and objs[p.path_id].type.name in ("Transform","RectTransform"):
                    tr_go[pid_] = p.path_id; break
        elif t in ("Transform","RectTransform"):
            tr = o.read()
            trd[pid_] = ((tr.m_LocalPosition.x,tr.m_LocalPosition.y,tr.m_LocalPosition.z),
                         (tr.m_LocalRotation.x,tr.m_LocalRotation.y,tr.m_LocalRotation.z,tr.m_LocalRotation.w),
                         (tr.m_LocalScale.x,tr.m_LocalScale.y,tr.m_LocalScale.z), tr.m_Father.path_id)
    return tr_go, trd, goes
for lvl in ["level1","level8","level10","level5","level7","level3"]:
    tr_go, trd, goes = load(lvl)
    rot = scale = depthmax = 0; n = 0
    for gid,(tag,on) in goes.items():
        if tag!=20022 or not on: continue
        tid = tr_go.get(gid)
        if tid is None: continue
        n += 1
        d = 0; tid2 = tid; has_rot = has_scale = False
        while tid2 and tid2 in trd and d < 64:
            pos,q,s,fa = trd[tid2]
            if abs(q[3]) < 0.99999: has_rot = True
            if abs(s[0]-1)>1e-4 or abs(s[1]-1)>1e-4 or abs(s[2]-1)>1e-4: has_scale = True
            tid2 = fa; d += 1
        depthmax = max(depthmax, d)
        if has_rot: rot += 1
        if has_scale: scale += 1
    print(f"{lvl}: waypoints={n} under_rotated_parent={rot} under_scaled_parent={scale} max_depth={depthmax}")
