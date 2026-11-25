
import bpy
import os
import sys
import math
import argparse

# Roblox AI Video Generator
# Detailed 3D avatar pipeline - starter version

OUTPUT_DIR = "output"
ASSET_DIR = "assets/characters"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ASSET_DIR, exist_ok=True)

parser = argparse.ArgumentParser()
parser.add_argument("--topic", default="Noob's First Day at School")
args, unknown = parser.parse_known_args(
    sys.argv[sys.argv.index("--") + 1:]
    if "--" in sys.argv else []
)

TOPIC = args.topic

# Reset Blender scene
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

# Vertical video settings
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 540
scene.render.resolution_y = 960
scene.render.resolution_percentage = 100
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 480

# Create materials
def create_material(name, color):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    return mat

skin = create_material("Yellow Skin", (1.0, 0.72, 0.35))
shirt = create_material("Blue Shirt", (0.03, 0.18, 0.85))
pants = create_material("Dark Pants", (0.04, 0.04, 0.08))

# Character asset importer
def import_character(name, model_path):
    if not os.path.exists(model_path):
        print("Character model missing:", model_path)
        return None

    before = set(bpy.data.objects)

    bpy.ops.wm.import_scene.gltf(filepath=model_path)

    imported = set(bpy.data.objects) - before

    for obj in imported:
        obj.name = name + "_" + obj.name

    return list(imported)

# Character library
CHARACTER_LIBRARY = {
    "noob": ASSET_DIR + "/noob.glb",
    "friend": ASSET_DIR + "/friend.glb",
    "teacher": ASSET_DIR + "/teacher.glb",
    "dad": ASSET_DIR + "/dad.glb",
    "mom": ASSET_DIR + "/mom.glb",
}

# Load available character models
characters = {}

for name, path in CHARACTER_LIBRARY.items():
    characters[name] = import_character(name, path)

# Ground
bpy.ops.mesh.primitive_plane_add(size=100)
ground = bpy.context.object
ground.name = "Environment_Ground"

# Camera
bpy.ops.object.camera_add(location=(0, -12, 5))
camera = bpy.context.object
camera.rotation_euler = (
    math.radians(75), 0, 0
)
scene.camera = camera

# Lighting
bpy.ops.object.light_add(type="AREA", location=(0, -5, 9))
light = bpy.context.object
light.data.energy = 1200
light.data.shape = "DISK"
light.data.size = 7

# Render output
scene.render.image_settings.file_format = "FFMPEG"
scene.render.ffmpeg.format = "MPEG4"
scene.render.filepath = os.path.abspath(
    OUTPUT_DIR + "/roblox_story.mp4"
)

print("Topic:", TOPIC)
print("Character pipeline initialized.")
print("Available models:", list(CHARACTER_LIBRARY.keys()))
print("Detailed character assets must be added before rendering.")
