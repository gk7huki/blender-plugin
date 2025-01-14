"""
Name:    tools
Purpose: Provides functions for operators

Description:
Some functions that are called by operators 
(e.g. the light panel, helpers, etc.).

"""

import bpy
import bmesh
import mathutils
from math import pi
import time
from .common import create_material, COL_HULL
import importlib

from bpy.props import (
    FloatProperty,
    IntProperty,
    StringProperty,
)

# Reloading the 'common' module if it's already in locals
if "common" in locals():
    importlib.reload(common)


def bake_shadow(self, context):
    original_active = context.view_layer.objects.active
    original_location = original_active.location
    scene = context.scene
    original_engine = scene.render.engine
    # Activate Cycles
    bpy.context.scene.render.engine = 'CYCLES'
    scene.cycles.samples = 32  # Set sampling for baking quality
    scene.cycles.max_bounces = 4  # Total maximum bounces
    scene.cycles.diffuse_bounces = 2  # Diffuse bounces
    scene.cycles.glossy_bounces = 2  # Glossy bounces
    scene.cycles.transmission_bounces = 2  # Transmission bounces
    scene.cycles.transparent_max_bounces = 2  # Transparency bounces
    scene.cycles.volume_bounces = 1  # Volume bounces
    scene = bpy.context.scene
    resolution = scene.shadow_resolution
    quality = scene.shadow_quality
    softness = scene.shadow_softness
    method = scene.shadow_method
    shtable = scene.shadow_table

    # Create a hemi light (positive)
    lamp_data_pos = bpy.data.lights.new(name="ShadePositive", type="SUN")
    lamp_data_pos.energy = 1.0
    lamp_positive = bpy.data.objects.new(name="ShadePositive", object_data=lamp_data_pos)

    # Link lights to the scene
    scene.collection.objects.link(lamp_positive)

    # Create a texture for the shadow
    shadow_tex = bpy.data.images.new("Shadow", width=resolution, height=resolution)

    all_objs = [ob_child for ob_child in context.scene.objects if ob_child.parent == shade_obj] + [shade_obj]

    # Get the bounds taking in account all child objects (wheels, etc.)
    # Using the world matrix here to get positions from child objects
    far_left = min([min([(ob.matrix_world[0][3] + ob.bound_box[i][0] * shade_obj.scale[0]) for i in range(0, 8)]) for ob in all_objs])
    far_right = max([max([(ob.matrix_world[0][3] + ob.bound_box[i][0] * shade_obj.scale[0]) for i in range(0, 8)]) for ob in all_objs])
    far_front = max([max([(ob.matrix_world[1][3] + ob.bound_box[i][1] * shade_obj.scale[1]) for i in range(0, 8)]) for ob in all_objs])
    far_back = min([min([(ob.matrix_world[1][3] + ob.bound_box[i][1] * shade_obj.scale[1]) for i in range(0, 8)]) for ob in all_objs])
    far_top = max([max([(ob.matrix_world[2][3] + ob.bound_box[i][2] * shade_obj.scale[2]) for i in range(0, 8)]) for ob in all_objs])
    far_bottom = min([min([(ob.matrix_world[2][3] + ob.bound_box[i][2] * shade_obj.scale[2]) for i in range(0, 8)]) for ob in all_objs])

    # Get the dimensions to set the scale
    dim_x = abs(far_left - far_right)
    dim_y = abs(far_front - far_back)

    # Location for the shadow plane
    loc = ((far_right + far_left)/2,
           (far_front + far_back)/2,
            far_bottom)

    # Create the shadow plane and map it
    bpy.ops.mesh.primitive_plane_add(location=loc, enter_editmode=True)
    bpy.ops.uv.unwrap()
    bpy.ops.object.mode_set(mode='OBJECT')
    shadow_plane = context.object

    # Set the scale for the shadow plane
    scale = max(dim_x, dim_y)
    shadow_plane.scale.x = scale / 1.5
    shadow_plane.scale.y = scale / 1.5

    # Unwrap the shadow plane
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.bake(type='SHADOW')

    # Set the image for the shadow plane UV map
    uv_layer = shadow_plane.data.uv_layers.active
    for polygon in shadow_plane.data.polygons:
        for loop_index in polygon.loop_indices:
            loop = shadow_plane.data.loops[loop_index]
            uv_layer.data[loop.index].image = shadow_tex

    # And finally select it and delete it
    shade_obj.select = False
    shadow_plane.select = False
    lamp_positive.select = True
    bpy.ops.object.delete()

    # select the other object again
    shade_obj.select = True
    scene.objects.active = shade_obj

    # space between the car body center and the edge of the shadow plane
    sphor = (shadow_plane.location[0] - (shadow_plane.dimensions[0]/2))
    spver = ((shadow_plane.dimensions[1]/2) - shadow_plane.location[1])

    # Generates shadowtable
    sleft = (sphor - shade_obj.location[0]) * 100
    sright = (shade_obj.location[0] - sphor) * 100
    sfront = (spver - shade_obj.location[1]) * 100
    sback = (shade_obj.location[1] - spver) * 100
    sheight = (far_bottom - shade_obj.location[2]) * 100
    shtable = ";)SHADOWTABLE {:.4f} {:.4f} {:.4f} {:.4f} {:.4f}".format(
        sleft, sright, sfront, sback, sheight
    )
    scene.shadow_table = shtable
    scene.render.engine = original_engine
    
def bake_vertex(self, context):
    scene = context.scene
    rd = scene.render
    rd.use_bake_to_vertex_color = True
    rd.use_textures = False

    shade_obj = context.object

    if scene.light1 != "None":
        light_location1, light_rotation1 = self.determine_light_position(scene.light_orientation, 1)
        lamp_object1 = self.setup_light(scene.light1, "ShadeLight1", scene.light_intensity1, light_location1, light_rotation1)

    if scene.light2 != "None":
        light_location2, light_rotation2 = self.determine_light_position(scene.light_orientation, 2)
        lamp_object2 = self.setup_light(scene.light2, "ShadeLight2", scene.light_intensity2, light_location2, light_rotation2)

    # Assuming additional steps for preparation before baking...
    bpy.ops.object.bake_image()

    # Cleanup
    bpy.data.objects.remove(lamp_object1)
    bpy.data.objects.remove(lamp_object2)

    shade_obj.select_set(True)
    bpy.context.view_layer.objects.active = shade_obj
    bpy.context.view_layer.update()


def rename_all_objects(self, context):
    for obj in context.scene.selected_objects:
        obj.name = scene.rename_all_name

    return len(context.selected_objects)


def select_by_name(self, context):
    sce = context.scene

    objs = [obj for obj in sce.objects if scene.rename_all_name in obj.name]

    for obj in objs:
        obj.select = True

    return len(objs)

def select_by_data(self, context):
    sce = context.scene
    compare = context.object

    objs = [obj for obj in sce.objects if obj.data == compare.data]

    for obj in objs:
            obj.select = True

    return len(objs)


def set_property_to_selected(self, context, prop, value):
    for obj in context.selected_objects:
        setattr(obj, prop, value)
    return len(context.selected_objects)


def batch_bake(self, context):

    rd = context.scene.render

    # Saves old render settings
    old_bake_vcol = rd.use_bake_to_vertex_color
    old_bake_type = rd.bake_type

    # Sets render settings
    rd.use_bake_to_vertex_color = True
    rd.bake_type = "FULL"

    # Bakes all selected objects
    for obj in context.selected_objects:

        # Skips unsupported objects
        if not hasattr(obj.data, "vertex_colors"):
            continue

        print("Baking at {}...".format(obj.name))
        context.scene.objects.active = obj

        # Gets currently selected layers
        old_active_render_layer = None
        old_active = None
        for vclayer in obj.data.vertex_colors:
            if vclayer.active_render:
                old_active_render_layer = vclayer.name
            if vclayer.active:
                old_active = vclayer.name

        print("Currently active layer:", old_active)
        print("Currently active layer (render):", old_active_render_layer)
        
        # Creates a temporary layer for baking a full render to
        if not "temp" in obj.data.vertex_colors:
            obj.data.vertex_colors.new(name="temp")
        tmp_layer = obj.data.vertex_colors.get("temp")
        tmp_layer.active = True
        tmp_layer.active_render = True
        print("TMP layer:", tmp_layer.name)
        print("TMP is active render:", tmp_layer.active_render)
        
        # Bakes the image onto that layer
        print("Baking...")
        bpy.ops.object.bake_image()
        print("done.")

        print("Calculating mean color...")
        
        bm = bmesh.new()
        bm.from_mesh(obj.data)

        vcol_layer = bm.loops.layers.color.get("temp")
        
        avg_col = [0.0, 0.0, 0.0]
        
        count = 0

        for face in bm.faces:
            for loop in face.loops:
                for c in range(3):
                    avg_col[c] += loop[vcol_layer][c]
                count += 1

        #TODO: Figure out if brightness is right
        inf_col = [c / count for c in avg_col]
        bm.free()

        for c in range(3):
            if context.scene.batch_bake_model_rgb:
                obj.revolt.fin_col[c] = inf_col[c]
            if context.scene.batch_bake_model_env:
                obj.fin_envcol[c] = inf_col[c]
        obj.fin_model_rgb = True

        # Removes the temporary render layer
        obj.data.vertex_colors.remove(tmp_layer)

        print("Restoring selection...")
        # Restores active layers
        if old_active_render_layer is not None:
            obj.data.vertex_colors[old_active_render_layer].active_render = True
        if old_active is not None:
            obj.data.vertex_colors[old_active].active = True
        print("done.")


    # Restores baking settings
    rd.use_bake_to_vertex_color = old_bake_vcol
    rd.bake_type = old_bake_type
    return len(context.selected_objects)

def generate_chull(context):
    hull_name = f"is_hull_convex"  # Prefix for naming the hull object

    scene = context.scene
    obj = context.object

    bm = bmesh.new()
    bm.from_mesh(obj.data)

    # Adds a convex hull to the bmesh
    chull_out = bmesh.ops.convex_hull(bm, input=bm.verts)
    
    try:
        # Gets rid of interior geometry
        for face in bm.faces:
            if face not in chull_out["geom"]:
                bm.faces.remove(face)

        for edge in bm.edges:
            if edge not in chull_out["geom"]:
                bm.edges.remove(edge)

        for vert in bm.verts:
            if vert not in chull_out["geom"]:
                bm.verts.remove(vert)

        me = bpy.data.meshes.new(hull_name)
        bm.to_mesh(me)
        bm.free()

        # Create new hull object
        hull_ob = bpy.data.objects.new(hull_name, me)

        # Set custom property
        hull_ob.is_hull_convex = True

        # Setup materials and other properties
        hull_ob.show_transparent = True
        hull_ob.show_wire = True
        hull_ob.matrix_world = obj.matrix_world.copy()
        me.materials.append(create_material("RVHull", COL_HULL, 0.3))

        # Link new hull object to the same collections as the original object
        for collection in bpy.data.collections:
            if obj.name in collection.objects:
                collection.objects.link(hull_ob)

        # Remove the original object
        bpy.data.objects.remove(obj, do_unlink=True)

        # Select and activate hull object
        context.view_layer.objects.active = hull_ob
        hull_ob.select_set(True)

        context.view_layer.update()

        return hull_ob
    except Exception as e:
        print(f"An error occurred while generating the hull: {e}")
        return None
