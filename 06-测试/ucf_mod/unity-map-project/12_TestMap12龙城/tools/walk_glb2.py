
import bpy, mathutils, json
from mathutils.bvhtree import BVHTree

GLB = "D:/BaiduNetdiskDownload/ForbiddenTD_Classic.GLB"
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)

meshes = [o for o in bpy.data.objects if o.type == 'MESH']
bpy.ops.object.select_all(action='DESELECT')
for o in meshes:
    o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.join()
merged = bpy.context.view_layer.objects.active
print("MERGED_OK polys=" + str(len(merged.data.polygons)), flush=True)

dg = bpy.context.evaluated_depsgraph_get()
bvh = BVHTree.FromObject(merged, dg)

wd = merged.matrix_world
mins = [1e30]*3
maxs = [-1e30]*3
for c in merged.bound_box:
    w = wd @ mathutils.Vector(c)
    for i in range(3):
        mins[i] = min(mins[i], w[i])
        maxs[i] = max(maxs[i], w[i])
size = [maxs[i]-mins[i] for i in range(3)]
print("BBOX_WORLD " + json.dumps({"min": [round(v,2) for v in mins], "max": [round(v,2) for v in maxs], "size": [round(v,2) for v in size]}), flush=True)

N = 140
buckets = {"below0": 0, "ground": 0, "low": 0, "mid": 0, "roof": 0, "none": 0}
zs = []
for i in range(N):
    for j in range(N):
        x = mins[0] + (i + 0.5) / N * size[0]
        y = mins[1] + (j + 0.5) / N * size[1]
        org = mathutils.Vector((x, y, maxs[2] + 100))
        loc, nor, idx, dist = bvh.ray_cast(org, mathutils.Vector((0, 0, -1)))
        if loc is None:
            buckets["none"] += 1
            continue
        z = loc.z
        zs.append(z)
        if z < -0.5:
            buckets["below0"] += 1
        elif z <= 1.5:
            buckets["ground"] += 1
        elif z <= 6.0:
            buckets["low"] += 1
        elif z <= 20.0:
            buckets["mid"] += 1
        else:
            buckets["roof"] += 1

tot = N * N
out = dict(buckets)
out["grid"] = tot
out["pct"] = {k: round(100.0 * v / tot, 1) for k, v in buckets.items()}
out["hit_z_min"] = round(min(zs), 2) if zs else None
out["hit_z_max"] = round(max(zs), 2) if zs else None
print("WALK " + json.dumps(out), flush=True)

# surface area at ground level vs above
area = sum(p.area for p in merged.data.polygons)
print("AREA " + str(round(area, 1)), flush=True)
