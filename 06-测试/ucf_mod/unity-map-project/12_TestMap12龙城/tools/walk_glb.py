
import bpy, mathutils, json
from mathutils.bvhtree import BVHTree

GLB = "D:/BaiduNetdiskDownload/ForbiddenTD_Classic.GLB"
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)

meshes = [o for o in bpy.data.objects if o.type == 'MESH']
mins = [1e30]*3
maxs = [-1e30]*3
for o in meshes:
    for c in o.bound_box:
        w = o.matrix_world @ mathutils.Vector(c)
        for i in range(3):
            mins[i] = min(mins[i], w[i])
            maxs[i] = max(maxs[i], w[i])
size = [maxs[i]-mins[i] for i in range(3)]

bpy.ops.object.select_all(action='DESELECT')
for o in meshes:
    o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
bpy.ops.object.join()
merged = bpy.context.view_layer.objects.active
print("MERGED_OK polys=" + str(len(merged.data.polygons)), flush=True)

dg = bpy.context.evaluated_depsgraph_get()
bvh = BVHTree.FromObject(merged, dg)

N = 120
below0 = 0
ground = 0
low = 0
mid = 0
roof = 0
none = 0
zs = []
for i in range(N):
    for j in range(N):
        x = mins[0] + (i + 0.5) / N * size[0]
        y = mins[1] + (j + 0.5) / N * size[1]
        org = mathutils.Vector((x, y, maxs[2] + 100))
        loc, nor, idx, dist = bvh.ray_cast(org, mathutils.Vector((0, 0, -1)))
        if loc is None:
            none += 1
            continue
        z = loc.z
        zs.append(z)
        if z < -0.5:
            below0 += 1
        elif z <= 1.5:
            ground += 1
        elif z <= 6.0:
            low += 1
        elif z <= 20.0:
            mid += 1
        else:
            roof += 1

tot = N * N
res = {
    "grid": tot,
    "ground_z_le_1.5": ground,
    "low_1.5_6": low,
    "mid_6_20": mid,
    "roof_gt_20": roof,
    "below0": below0,
    "no_hit": none,
    "walkable_pct": round(100.0 * ground / tot, 1),
    "roof_pct": round(100.0 * roof / tot, 1),
    "empty_pct": round(100.0 * none / tot, 1),
    "z_min": round(min(zs), 2) if zs else None,
    "z_max": round(max(zs), 2) if zs else None,
}
print("WALK " + json.dumps(res), flush=True)

# also: total surface area
area = sum(p.area for p in merged.data.polygons)
print("AREA " + str(round(area, 1)) + " sq units", flush=True)

# material slot count on merged
print("MATSLOTS " + str(len(merged.data.materials)), flush=True)
