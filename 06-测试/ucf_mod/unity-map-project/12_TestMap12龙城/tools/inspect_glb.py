
import bpy, os, json, mathutils, sys

GLB = "D:/BaiduNetdiskDownload/ForbiddenTD_Classic.GLB"
OUTDIR = "D:/ucf_unity/out"
os.makedirs(OUTDIR, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
print("IMPORT_START", flush=True)
bpy.ops.import_scene.gltf(filepath=GLB)
print("IMPORT_DONE", flush=True)

objs = list(bpy.data.objects)
meshes = [o for o in objs if o.type == 'MESH']

tot_v = sum(len(o.data.vertices) for o in meshes)
tot_p = sum(len(o.data.polygons) for o in meshes)
tot_tris = 0
for o in meshes:
    o.data.calc_loop_triangles()
    tot_tris += len(o.data.loop_triangles)

mins = [1e30]*3
maxs = [-1e30]*3
for o in meshes:
    for c in o.bound_box:
        w = o.matrix_world @ mathutils.Vector(c)
        for i in range(3):
            mins[i] = min(mins[i], w[i])
            maxs[i] = max(maxs[i], w[i])
size = [maxs[i]-mins[i] for i in range(3)]

rank = []
for o in meshes:
    n = len(o.data.loop_triangles)
    rank.append((n, o.name, tuple(round(x,2) for x in o.dimensions)))
rank.sort(reverse=True)

mats = [m.name for m in bpy.data.materials]
imgs = []
for im in bpy.data.images:
    imgs.append({"name": im.name, "size": list(im.size), "packed": bool(im.packed_file)})

roots = [o for o in objs if o.parent is None]

info = {
  "objects": len(objs),
  "meshes": len(meshes),
  "verts": tot_v,
  "polys": tot_p,
  "tris": tot_tris,
  "materials": len(mats),
  "images": len(imgs),
  "bbox_min": [round(v,3) for v in mins],
  "bbox_max": [round(v,3) for v in maxs],
  "bbox_size": [round(v,3) for v in size],
  "top_meshes": [{"tris": n, "name": nm, "dims": list(d)} for n, nm, d in rank[:20]],
  "material_sample": mats[:30],
  "root_objects": [o.name for o in roots][:20],
  "image_sample": imgs[:10],
}
print("INFO " + json.dumps(info, ensure_ascii=False), flush=True)

with open(os.path.join(OUTDIR, "glb_info.json"), "w", encoding="utf-8") as f:
    json.dump(info, f, ensure_ascii=False, indent=2)

fp = os.path.join(OUTDIR, "ForbiddenTD_Classic.fbx")
bpy.ops.object.select_all(action='SELECT')
try:
    bpy.ops.export_scene.fbx(
        filepath=fp,
        use_selection=False,
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_ALL',
        path_mode='COPY',
        embed_textures=True,
        mesh_smooth_type='FACE',
        bake_anim=False,
    )
    print("FBX_OK " + fp + " size=" + str(os.path.getsize(fp)), flush=True)
except Exception as e:
    print("FBX_FAIL " + repr(e), flush=True)
    try:
        bpy.ops.export_scene.fbx(filepath=fp)
        print("FBX_OK_MINIMAL " + fp + " size=" + str(os.path.getsize(fp)), flush=True)
    except Exception as e2:
        print("FBX_FAIL2 " + repr(e2), flush=True)
