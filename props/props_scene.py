"""
Name:    props_scene
Purpose: Provides the scene data class for Re-Volt meshes

Description:
The scene properties are misused for storing settings as well as 
level information.

"""

import bpy
import bmesh

from bpy.props import (
    BoolProperty,
    BoolVectorProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
    StringProperty,
    CollectionProperty,
    IntVectorProperty,
    FloatVectorProperty,
    PointerProperty
)

from ..common import *
from ..layers import *
from ..texanim import *


class RVSceneProperties(bpy.types.PropertyGroup):
    bl_idname = "RVSceneProperties"
    
    # User interface and misc.
    face_edit_mode = bpy.props.EnumProperty(
        name = "Face Edit Mode",
        description = "Select the Edit Mode",
        items=(
            ("prm", "PRM/World", "Meshes (.prm/.m, .w)"),
            ("ncp", "NCP", "Collision (.ncp)")
        ),
        default = "prm"
    )
    
    select_material = bpy.props.EnumProperty(
        name = "Select Material",
        items = MATERIALS,
        update = select_ncp_material,
        description = "Selects all faces with the selected material"
    )
    
    last_exported_filepath = bpy.props.StringProperty(
        name = "Last Exported Filepath",
        default = ""
    )
    
    enable_tex_mode = bpy.props.BoolProperty(
        name = "Material Preview after Import",
        default = True,
        description = "Enables Material Preview mode after mesh import to show textures and materials"
    )
    
    prefer_tex_solid_mode = bpy.props.BoolProperty(
        name = "Prefer Solid Shading Mode",
        default = False,
        description = "Prefer Solid shading mode over Material Preview mode in the 3D view:\n\n"
                  "When enabled, Solid mode will be used as the default shading mode, "
                  "which is beneficial for working with untextured meshes or focusing on mesh structure.\n"
                  "This setting affects functions that switch shading modes."
    )
        
    vertex_color_picker = bpy.props.FloatVectorProperty(
        name = "Object Color",
        subtype = 'COLOR',
        default = (0, 0, 1.0),
        min = 0.0, max=1.0,
        description = "Color picker for painting custom vertex colors"
    )
    
    envidx = bpy.props.IntProperty(
        name = "envidx",
        default = 0,
        min = 0,
        description = "Current env color index for importing. Internal only"
    )
    
    rvgl_dir = bpy.props.StringProperty(
        name = "Re-Volt Directory",
        default = "",
        description = "Manually define a Re-Volt installation for loading "
                      "stock files. If left empty, the directory will be "
                      "automatically detected"
    )
    
    batch_bake_model_rgb = bpy.props.BoolProperty(
        name = "Bake to Model RGB",
        default = True,
        description = "Bake scene lighting to Instance model RGB"
    )
    
    batch_bake_model_env = bpy.props.BoolProperty(
        name = "Bake to Model Env",
        default = True,
        description = "Bake scene lighting to Instance model environment color"
    )
    
    # Export properties
    triangulate_ngons = bpy.props.BoolProperty(
        name = "Triangulate n-gons",
        default = True,
        description = "Triangulate n-gons when exporting.\n"
                     "Re-Volt only supports tris and quads, n-gons will not be "
                     "exported correctly.\nOnly turn this off if you know what "
                     "you're doing!"
    )
    
    use_tex_num = bpy.props.BoolProperty(
        name = "Use Number for Textures",
        default = False,
        description = "Uses the texture number from the texture layer "
                      "accessible in the tool shelf in Edit mode.\n"
                      "Otherwise, it uses the texture from the texture file"
    )
    
    apply_scale = bpy.props.BoolProperty(
        name = "Apply Scale",
        default = True,
        description = "Applies the object scale on export"
    )
    
    apply_rotation = bpy.props.BoolProperty(
        name = "Apply Rotation",
        default = True,
        description = "Applies the object rotation on export"
    )
    
    apply_translation = bpy.props.BoolProperty(
        name = "Apply Translation",
        default = False,
        description = "Applies the object location on export. Should be disabled for single/instance ncp files"
    )

    prm_check_parameters = bpy.props.BoolProperty(
        name = "Check Parameters for texture",
        default = True,
        description = "Checks car parameters.txt for the texture"
    )
    
    # World import properties
    w_parent_meshes = bpy.props.BoolProperty(
        name = "Parent .w meshes to Empty",
        default = False,
        description = "Parents all .w meshes to an Empty object, resulting in "
                      "less clutter in the object outliner"
    )
    
    w_import_bound_boxes = bpy.props.BoolProperty(
        name = "Import Bound Boxes",
        default = False,
        description = "Imports the boundary box of each .w mesh for debugging "
                      "purposes"
    )
    
    w_bound_box_layers = bpy.props.BoolVectorProperty(
        name = "Bound Box Layers",
        subtype = "LAYER",
        size = 20,
        default = [True]+[False for x in range(0, 19)],
        description = "Sets the layers the objecs will be be imported to. "
                      "Select multiple by dragging or holding down Shift.\n"
                      "Activate multiple layers by pressing Shift + numbers"
    )
    
    w_import_cubes = bpy.props.BoolProperty(
        name = "Import Cubes",
        default = False,
        description = "Imports the cube of each .w mesh for debugging "
                      "purposes"
    )
    
    w_cube_layers = bpy.props.BoolVectorProperty(
        name = "Cube Layers",
        subtype = "LAYER",
        size = 20,
        default = [True]+[False for x in range(0, 19)],
        description = "Sets the layers the objecs will be be imported to. "
                      "Select multiple by dragging or holding down Shift.\n"
                      "Activate multiple layers by pressing Shift + numbers"
    )
    
    w_import_big_cubes = bpy.props.BoolProperty(
        name = "Import Big Cubes",
        default = False,
        description = "Imports Big Cubes for debugging purposes"
    )
    
    w_big_cube_layers = bpy.props.BoolVectorProperty(
        name = "Big Cube Layers",
        subtype = "LAYER",
        size = 20,
        default = [True]+[False for x in range(0, 19)],
        description = "Sets the layers the objecs will be be imported to. "
                      "Select multiple by dragging or holding down Shift.\n"
                      "Activate multiple layers by pressing Shift + numbers"
    )
    
    # NCP
    ncp_export_collgrid = bpy.props.BoolProperty(
        name = "Export Collision Grid (.w)",
        default = True,
        description = "Export a collision grid to the .ncp file:\n\n"
                      "Enable this if you want to export a level (.w) "
                      ".ncp file"
    )
    
    ncp_collgrid_size = bpy.props.IntProperty(
        name = "Grid Size",
        default = 1024,
        min = 512,
        max = 8192,
        description = "Size of the lookup grid"
    )
    
    ncp_export_selected = bpy.props.BoolProperty(
        name = "Only export selected",
        default = False,
        description = "Only exports the selected objects"
    )
    
    # Light tools
    light1 = bpy.props.EnumProperty(
        name = "Light 1",
        items = BAKE_LIGHTS,
        default = "SUN",
        description = "Type of light"
    )
    
    light2 = bpy.props.EnumProperty(
        name = "Light 2",
        items = BAKE_LIGHTS,
        default = "HEMI",
        description = "Type of light"
    )
    
    light_intensity1 = bpy.props.FloatProperty(
        name = "Intensity 1",
        min = 0.0,
        default = 1.5,
        description = "Intensity of Light 1"
    )
    
    light_intensity2 = bpy.props.FloatProperty(
        name = "Intensity 2",
        min = 0.0,
        default = .05,
        description = "Intensity of Light 2"
    )
    
    light_orientation = bpy.props.EnumProperty(
        name = "Orientation",
        items = BAKE_LIGHT_ORIENTATIONS,
        default = "Z",
        description = "Directions of the lights"
    )
    
    shadow_method = bpy.props.EnumProperty(
        name = "Method",
        items = BAKE_SHADOW_METHODS,
        description = "Default (Adaptive QMC):\nFaster option, recommended "
                      "for testing the shadow settings.\n\n"
                      "High Quality:\nSlower and less grainy option, "
                      "recommended for creating the final shadow"
    )
    
    shadow_quality = bpy.props.IntProperty(
        name = "Quality",
        min = 0,
        max = 32,
        default = 15,
        description = "The amount of samples the shadow is rendered with "
                      "(number of samples taken extra)"
    )
    
    shadow_resolution = bpy.props.IntProperty(
        name = "Resolution",
        min = 32,
        max = 8192,
        default = 128,
        description = "Texture resolution of the shadow.\n"
                      "Default: 128x128 pixels"
    )
    
    shadow_softness = bpy.props.FloatProperty(
        name = "Softness",
        min = 0.0,
        max = 100.0,
        default = 1,
        description = "Softness of the shadow "
                      "(Light size for ray shadow sampling)"
    )
    
    shadow_table = bpy.props.StringProperty(
        name = "Shadowtable",
        default = "",
        description = "Shadow coordinates for use in parameters.txt of cars.\n"
                      "Click to select all, then CTRL C to copy"
    )
    
    # Texture Animation
    texture_animations = bpy.props.StringProperty(
        name = "Texture Animations",
        default = "[]",
        description = "Storage for Texture animations. Should not be changed "
                      "by hand"
    )
    
    ta_max_slots = bpy.props.IntProperty(
        name = "Slots",
        min = 0,
        max = TEX_ANIM_MAX,
        default = 0,
        update = update_ta_max_slots,
        description = "Total number of texture animation slots. "
                      "All higher slots will be ignored on export"
    )
    
    ta_current_slot = bpy.props.IntProperty(
        name = "Animation",
        default = 0,
        min = 0,
        max = TEX_ANIM_MAX-1,
        update = update_ta_current_slot,
        description = "Texture animation slot"
    )
    
    ta_max_frames = bpy.props.IntProperty(
        name = "Frames",
        min = 2,
        default = 2,
        update = update_ta_max_frames,
        description = "Total number of frames of the current slot. "
                      "All higher frames will be ignored on export"
    )
    
    ta_current_frame = bpy.props.IntProperty(
        name = "Frame",
        default = 0,
        min = 0,
        update = update_ta_current_frame,
        description = "Current frame"
    )
    
    ta_current_frame_tex = bpy.props.IntProperty(
        name = "Texture",
        default = 0,
        min = -1,
        max = TEX_PAGES_MAX-1,
        update = update_ta_current_frame_tex,
        description = "Texture of the current frame"
    )
    
    ta_current_frame_delay = bpy.props.FloatProperty(
        name = "Duration",
        default = 0.01,
        min = 0,
        update = update_ta_current_frame_delay,
        description = "Duration of the current frame"
    )
    
    ta_current_frame_uv0 = bpy.props.FloatVectorProperty(
        name = "UV 0",
        size = 2,
        default = (0, 0),
        #min = 0.0,
        #max = 1.0,
        update = lambda self, context: update_ta_current_frame_uv(context, 0),
        description = "UV coordinate of the first vertex"
    )
    
    ta_current_frame_uv1 = bpy.props.FloatVectorProperty(
        name = "UV 1",
        size = 2,
        default = (0, 0),
        #min = 0.0,
        #max = 1.0,
        update = lambda self, context: update_ta_current_frame_uv(context, 1),
        description = "UV coordinate of the second vertex"
    )
    
    ta_current_frame_uv2 = bpy.props.FloatVectorProperty(
        name = "UV 2",
        size = 2,
        default = (0, 0),
        #min = 0.0,
        #max = 1.0,
        update = lambda self, context: update_ta_current_frame_uv(context, 2),
        description = "UV coordinate of the third vertex"
    )
    
    ta_current_frame_uv3 = bpy.props.FloatVectorProperty(
        name = "UV 3",
        size = 2,
        default = (0, 0),
        #min = 0.0,
        #max = 1.0,
        update = lambda self, context: update_ta_current_frame_uv(context, 3),
        description = "UV coordinate of the fourth vertex"
    )
    
    ta_sync_with_face = bpy.props.BoolProperty(
        name = "Sync UV with Selection",
        default = False,
        description = "Updates the UV mapping of the currently selected face "
                    "with the UV coordinates of the texture animation frame.\n"
                    "Texture animation needs to be enabled for the selected "
                    "face"
    )

def register():
    bpy.utils.register_class(RVSceneProperties)
    bpy.types.Scene.revolt = bpy.props.PointerProperty(type=RVSceneProperties)
    
def unregister():
    del bpy.types.Scene.revolt
    bpy.utils.unregister_class(RVSceneProperties)


dprint