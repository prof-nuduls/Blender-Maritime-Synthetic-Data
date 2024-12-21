import bpy
import os
import random
from mathutils import Vector
import math
import argparse
import sys


# Paths and settings
blend_file_path = "/mnt/f/project/Lake_with_sky.blend"
asset_library_path = "./Assets"
output_dir = "/mnt/f/Derick/Project"
images_dir = os.path.join(output_dir, "images")
labels_dir = os.path.join(output_dir, "labels")
os.makedirs(images_dir, exist_ok=True)
os.makedirs(labels_dir, exist_ok=True)

# Camera settings
camera_name = "Camera"
camera_min_height = 25
camera_max_height = 150

# Object settings
object_assets = {
    "swimmers": ["swimmer_1", "swimmer_2"],
    "boats": ["Boat_1", "Boat_2", "Boat_3"],
    "jetskis": ["Jetski_1", "Jetski_2"],
    "life_preservers": ["life_preserver_1", "life_preserver_2"],
    "buoys": ["buoy_1", "buoy_2"],
}
object_classes = {
    "swimmers": 0,
    "boats": 1,
    "jetskis": 2,
    "life_preservers": 3,
    "buoys": 4,
}
object_counts = {
    "swimmers": (1, 20),
    "boats": (0, 5),
    "jetskis": (0, 4),
    "life_preservers": (0, 4),
    "buoys": (0, 4),
}
bounds = (-100, 100)

# Reload scene
def reload_scene():
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)
    camera = bpy.data.objects.get(camera_name)
    if not camera:
        raise ValueError(f"Camera '{camera_name}' not found!")
    return camera

# Append object or group
def append_object_or_group(library_path, name, is_group=False):
    object_blend_path = os.path.join(library_path, f"{name}.blend")
    if not os.path.exists(object_blend_path):
        raise FileNotFoundError(f"Asset '{name}' not found in {library_path}")
    bpy.ops.wm.append(
        filepath=os.path.join(object_blend_path, "Collection" if is_group else "Object", name),
        directory=os.path.join(object_blend_path, "Collection" if is_group else "Object"),
        filename=name,
    )
    if is_group:
        group = bpy.data.collections.get(name)
        if not group:
            raise ValueError(f"Group '{name}' not properly appended.")
        parent_obj = bpy.data.objects.new(name=f"{name}_parent", object_data=None)
        bpy.context.scene.collection.objects.link(parent_obj)
        for obj in group.objects:
            obj.parent = parent_obj
        return parent_obj
    return bpy.data.objects.get(name)

# Append swimmer group
def append_swimmer_group(library_path, name):
    """Append a swimmer group as a unified entity."""
    object_blend_path = os.path.join(library_path, f"{name}.blend")
    if not os.path.exists(object_blend_path):
        raise FileNotFoundError(f"Swimmer asset '{name}' not found in {library_path}")

    # Append the entire swimmer group collection
    with bpy.data.libraries.load(object_blend_path, link=False) as (data_from, data_to):
        if name in data_from.collections:
            data_to.collections = [name]

    # Link the collection to the current scene
    if data_to.collections:
        collection = data_to.collections[0]
        bpy.context.scene.collection.children.link(collection)
        print(f"Successfully appended collection '{name}'.")

    return collection  # Return the collection for use

# Position swimmer group
def position_swimmer_group(swimmer_collection, bounds):
    """Position all components in the swimmer group randomly within bounds with additional Y-axis rotation."""
    new_x, new_y = random.uniform(bounds[0], bounds[1]), random.uniform(bounds[0], bounds[1])
    z_rotation = random.uniform(0, 360)
    y_rotation = random.uniform(-15, 15)  # Add random Y-axis rotation between -15 and +15 degrees

    offset = Vector((new_x, new_y, 0))

    for obj in swimmer_collection.objects:
        if obj.type == 'MESH':  # Only move mesh components
            obj.location += offset
            obj.rotation_euler.z += math.radians(z_rotation)
            obj.rotation_euler.y += math.radians(y_rotation)  # Apply Y-axis rotation

    print(f"Swimmer group '{swimmer_collection.name}' positioned at ({new_x}, {new_y}, 0) with Z rotation {z_rotation} degrees and Y rotation {y_rotation} degrees.")


# Position objects randomly with Z-rotation
def position_objects_randomly(objects):
    for obj, _ in objects:
        x, y = random.uniform(bounds[0], bounds[1]), random.uniform(bounds[0], bounds[1])
        z_rotation = random.uniform(0, 360)  # Add random Z-axis rotation
        obj.location = Vector((x, y, 0))
        obj.rotation_euler = Vector((0, 0, math.radians(z_rotation)))
        print(f"Placed '{obj.name}' at {obj.location} with rotation {obj.rotation_euler}")

# Calculate bounding box
def calculate_bounding_box(obj, camera):
    if obj.type == 'MESH':
        return camera_view_bounds_2d(bpy.context.scene, camera, obj)
    print(f"Object '{obj.name}' is not a mesh and cannot have a bounding box.")
    return None

# Calculate swimmer group bounding box
def calculate_swimmer_group_bounds(swimmer_collection, camera):
    """Calculate bounding box for the swimmer group using collection."""
    bounds_list = []
    for obj in swimmer_collection.objects:
        if obj.type == 'MESH' and obj.visible_get():
            bb = camera_view_bounds_2d(bpy.context.scene, camera, obj)
            if bb and bb[2] > 0 and bb[3] > 0:  # Ensure valid bounding box
                bounds_list.append(bb)

    if not bounds_list:
        return None  # No valid bounding boxes found

    # Combine all bounding boxes into one
    min_x = min(b[0] for b in bounds_list)
    min_y = min(b[1] for b in bounds_list)
    max_x = max(b[0] + b[2] for b in bounds_list)
    max_y = max(b[1] + b[3] for b in bounds_list)

    return (min_x, min_y, max_x - min_x, max_y - min_y)

# Helper functions for bounding box calculation
def clamp(x, minimum, maximum): 
    return max(minimum, min(x, maximum))

def camera_view_bounds_2d(scene, cam_ob, me_ob):
    mat = cam_ob.matrix_world.normalized().inverted()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    mesh_eval = me_ob.evaluated_get(depsgraph)
    me = mesh_eval.to_mesh()
    me.transform(me_ob.matrix_world)
    me.transform(mat)

    camera = cam_ob.data
    frame = [-v for v in camera.view_frame(scene=scene)[:3]]
    camera_persp = camera.type != 'ORTHO'

    lx = []
    ly = []

    for v in me.vertices:
        co_local = v.co
        z = -co_local.z

        if camera_persp:
            if z == 0.0:
                lx.append(0.5)
                ly.append(0.5)
            else:
                frame = [(v / (v.z / z)) for v in frame]

        min_x, max_x = frame[1].x, frame[2].x
        min_y, max_y = frame[0].y, frame[1].y

        x = (co_local.x - min_x) / (max_x - min_x)
        y = (co_local.y - min_y) / (max_y - min_y)

        lx.append(x)
        ly.append(y)

    min_x = clamp(min(lx), 0.0, 1.0)
    max_x = clamp(max(lx), 0.0, 1.0)
    min_y = clamp(min(ly), 0.0, 1.0)
    max_y = clamp(max(ly), 0.0, 1.0)

    mesh_eval.to_mesh_clear()

    r = scene.render
    fac = r.resolution_percentage * 0.01
    dim_x = r.resolution_x * fac
    dim_y = r.resolution_y * fac

    if round((max_x - min_x) * dim_x) == 0 or round((max_y - min_y) * dim_y) == 0:
        return (0, 0, 0, 0)

    return (
        round(min_x * dim_x),            # X
        round(dim_y - max_y * dim_y),    # Y
        round((max_x - min_x) * dim_x),  # Width
        round((max_y - min_y) * dim_y)   # Height
    )

# Generate YOLO labels
def generate_yolo_labels(objects, camera, image_index):
    labels_path = os.path.join(labels_dir, f"blender_{image_index:04d}.txt")
    with open(labels_path, "w") as f:
        unique_bbs = set()
        for obj, class_id in objects:
            bb = None
            if class_id == 0:  # Swimmer class
                bb = calculate_swimmer_group_bounds(obj, camera)
            else:
                bb = calculate_bounding_box(obj, camera)

            if bb and len(bb) == 4 and bb not in unique_bbs:
                center_x = (bb[0] + bb[2] / 2) / bpy.context.scene.render.resolution_x
                center_y = (bb[1] + bb[3] / 2) / bpy.context.scene.render.resolution_y
                width = bb[2] / bpy.context.scene.render.resolution_x
                height = bb[3] / bpy.context.scene.render.resolution_y

                # Calculate the area of the bounding box as a fraction of the window
                bbox_area = width * height

                # Skip if class 0 and takes up more than 95% of the window
                if class_id == 0 and bbox_area > 0.95:
                    print(f"Skipping class 0 object '{obj.name}' with bounding box taking {bbox_area*100:.2f}% of the window.")
                    continue

                if 0 < width <= 1 and 0 < height <= 1:
                    f.write(f"{class_id} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}\n")
                    unique_bbs.add(bb)
                else:
                    print(f"Invalid dimensions for object '{obj.name}': {bb}")

# Remove objects at origin
def remove_objects_at_origin():
    origin_threshold = 2
    exempt_objects = ["Lake"]
    for obj in list(bpy.context.scene.objects):
        if obj.name in exempt_objects:
            print(f"Exempting object from removal: {obj.name}")
            continue
        if obj.location.length <= origin_threshold:
            print(f"Removing object at origin: {obj.name}")
            bpy.data.objects.remove(obj, do_unlink=True)
# Position camera
def position_camera_around_origin(camera):
    height = random.uniform(camera_min_height, camera_max_height)
    radius = random.uniform(5, camera_max_height)
    hypotenuse = math.sqrt(radius**2 + height**2)
    tilt_angle = math.asin(radius / hypotenuse)
    azimuth_degrees = random.uniform(0, 360)
    azimuth_radians = math.radians(azimuth_degrees)

    x = radius * math.cos(azimuth_radians)
    y = radius * math.sin(azimuth_radians)
    z = height

    camera.location = Vector((x, y, z))
    direction = Vector((0, 0, 0)) - camera.location
    camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    camera.rotation_euler.x = tilt_angle


    print(f"Camera positioned at {camera.location}.")

def reset_camera_if_no_objects_visible(camera, objects):
    """
    Reset the camera position if no objects are visible to the camera.
    """
    for obj, _ in objects:
        # Handle both single objects and collections
        if isinstance(obj, bpy.types.Collection):
            # Iterate through the objects in the collection
            for sub_obj in obj.objects:
                if sub_obj.type in ['MESH', 'EMPTY'] and sub_obj.visible_get():
                    bb = calculate_bounding_box(sub_obj, camera)
                    if bb and bb[2] > 0 and bb[3] > 0:  # Check if the bounding box is valid
                        print(f"Object '{sub_obj.name}' is visible to the camera.")
                        return  # At least one object is visible
        else:
            if obj.type in ['MESH', 'EMPTY'] and obj.visible_get():
                bb = calculate_bounding_box(obj, camera)
                if bb and bb[2] > 0 and bb[3] > 0:  # Check if the bounding box is valid
                    print(f"Object '{obj.name}' is visible to the camera.")
                    return  # At least one object is visible

    # If no objects are visible, reset the camera
    print("No objects visible to the camera. Resetting camera position.")
    position_camera_around_origin(camera)

# Main function
def main():
    # Exclude Blender's own arguments
    argv = sys.argv[sys.argv.index("--") + 1:]  # Only keep args after the `--` separator

    parser = argparse.ArgumentParser(description="Generate images using Blender.")
    parser.add_argument("--start", type=int, required=True, help="Starting index of images to generate.")
    parser.add_argument("--end", type=int, required=True, help="Ending index of images to generate.")
    args = parser.parse_args(argv)  # Pass the filtered arguments

    start = args.start
    end = args.end
    print(f"Generating images from {start} to {end}")

    print(f"Generating images from {start} to {end}")
    # Set rendering engine to Cycles (if not already set)
    bpy.context.scene.render.engine = 'CYCLES'

    # Ensure the device is set to CPU
    cycles_prefs = bpy.context.preferences.addons['cycles'].preferences
    cycles_prefs.compute_device_type = 'CUDA'  # NONE forces CPU rendering
    print("Rendering set to GPU.")

    for i in range(start, end):
        print(f"\n--- Generating Image {i + 1}/{end} ---")
        bpy.ops.wm.open_mainfile(filepath=blend_file_path)

        camera = bpy.data.objects.get(camera_name)
        if not camera:
            raise ValueError(f"Camera '{camera_name}' not found!")
        position_camera_around_origin(camera)
        all_objects = []

        for category, (min_count, max_count) in object_counts.items():
            num_objects = random.randint(min_count, max_count)
            for _ in range(num_objects):
                if category == "swimmers":
                    model = random.choice(object_assets[category])
                    swimmer_control = append_swimmer_group(asset_library_path, model)
                    position_swimmer_group(swimmer_control, bounds)
                    all_objects.append((swimmer_control, object_classes[category]))
                else:
                    model = random.choice(object_assets[category])
                    obj = append_object_or_group(asset_library_path, model, is_group=False)
                    position_objects_randomly([(obj, object_classes[category])])
                    all_objects.append((obj, object_classes[category]))

        remove_objects_at_origin()
        reset_camera_if_no_objects_visible(camera, all_objects)
        generate_yolo_labels(all_objects, camera, i)

        image_path = os.path.join(images_dir, f"blender_{i:04d}.png")
        bpy.context.scene.render.filepath = image_path
        bpy.ops.render.render(write_still=True)
        print(f"Rendered image saved to {image_path}")


if __name__ == "__main__":
    main()