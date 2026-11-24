
import bpy, os, math, mathutils

GLB = "D:/BaiduNetdiskDownload/ForbiddenTD_Classic.GLB"
OUTDIR = "D:/ucf_unity/out"
os.makedirs(OUTDIR, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)

sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = 40
sc.cycles.use_denoising = True
sc.render.resolution_x = 1000
sc.render.resolution_y = 750
sc.render.film_transparent = False
sc.view_settings.view_transform = 'Standard'

world = bpy.data.worlds.new("W")
sc.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.55, 0.65, 0.8, 1)
bg.inputs[1].default_value = 1.2

mins = [1e30]*3
maxs = [-1e30]*3
for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    for c in o.bound_box:
        w = o.matrix_world @ mathutils.Vector(c)
        for i in range(3):
            mins[i] = min(mins[i], w[i])
            maxs[i] = max(maxs[i], w[i])
center = mathutils.Vector(((mins[0]+maxs[0])/2, (mins[1]+maxs[1])/2, (mins[2]+maxs[2])/2))
size = [maxs[i]-mins[i] for i in range(3)]
diag = max(size[0], size[1])
print("CENTER", tuple(round(v,2) for v in center), "SIZE", [round(v,2) for v in size], flush=True)

def look_at(obj, target):
    d = target - obj.location
    obj.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

cam_data = bpy.data.cameras.new("Cam")
cam = bpy.data.objects.new("Cam", cam_data)
sc.collection.objects.link(cam)
sc.camera = cam

# sun
sd = bpy.data.lights.new("Sun", 'SUN')
sd.energy = 3.0
sd.angle = math.radians(6)
sun = bpy.data.objects.new("Sun", sd)
sun.rotation_euler = (math.radians(50), 0, math.radians(35))
sc.collection.objects.link(sun)

# ---- view 1: perspective 3/4
cam.location = center + mathutils.Vector((diag*0.95, -diag*1.05, diag*1.15))
look_at(cam, center)
cam_data.lens = 42
sc.render.filepath = os.path.join(OUTDIR, "map_persp.png")
bpy.ops.render.render(write_still=True)
print("RENDER1_OK", flush=True)

# ---- view 2: top-down ortho
cam_data.type = 'ORTHO'
cam_data.ortho_scale = diag * 1.12
cam.location = mathutils.Vector((center.x, center.y, maxs[2] + 60))
cam.rotation_euler = (0, 0, 0)
sc.render.filepath = os.path.join(OUTDIR, "map_top.png")
bpy.ops.render.render(write_still=True)
print("RENDER2_OK", flush=True)
