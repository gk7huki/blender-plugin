"""
Name:    init
Purpose: Init file for the Blender Add-On

Description:
Marv's Add-On for Re-Volt with Theman's Update 
"""

# Global debug flag
DEBUG_MODE = True

from tokenize import Ignore
from xml.dom.domreg import well_known_implementations
import bpy
import bmesh
import os
import os.path
import importlib
from bpy.app.handlers import persistent  # For the scene update handler
from bpy.app.handlers import load_post

# Importing modules from the add-on's package

from .props import (
    props_mesh,
    props_obj,
    props_scene,
)

from . import (
    carinfo,
    common,
    fin_in,
    fin_out,
    hul_in,
    hul_out,
    img_in,
    layers,
    ncp_in,
    ncp_out,
    operators,
    parameters_in,
    parameters_out,
    prm_in,
    prm_out,
    rim_in,
    rim_out,
    rvstruct,
    taz_in,
    taz_out,
    ta_csv_in,
    ta_csv_out,
    texanim,
    tools,
    w_in,
    w_out,
)

from .ui import (
    faceprops,
    headers,
    helpers,
    instances,
    light,
    objectpanel,
    settings,
    texanim,
    vertex,
    zone,
)

# Reloads potentially changed modules on reload (F8 in Blender)
importlib.reload(props_mesh)
importlib.reload(props_obj)
importlib.reload(props_scene)

importlib.reload(common)
importlib.reload(layers)
importlib.reload(operators)
importlib.reload(texanim)
importlib.reload(tools)

# Reloads ui
importlib.reload(headers)
importlib.reload(faceprops)
importlib.reload(instances)
importlib.reload(light)
importlib.reload(objectpanel)
importlib.reload(vertex)
importlib.reload(texanim)
importlib.reload(helpers)
importlib.reload(settings)

if "bpy" in locals():
    importlib.reload(props_scene)
if "fin_in" in locals():
    importlib.reload(fin_in)
if "fin_out" in locals():
    importlib.reload(fin_out)
if "hul_in" in locals():
    importlib.reload(hul_in)
if "hul_out" in locals():
    importlib.reload(hul_out)
if "img_in" in locals():
    importlib.reload(img_in)
if "prm_in" in locals():
    importlib.reload(prm_in)
if "prm_out" in locals():
    importlib.reload(prm_out)
if "ncp_in" in locals():
    importlib.reload(ncp_in)
if "ncp_out" in locals():
    importlib.reload(ncp_out)
if "parameters_in" in locals():
    importlib.reload(parameters_in)
if "ta_csv_in" in locals():
    importlib.reload(ta_csv_in)
if "ta_csv_out" in locals():
    importlib.reload(ta_csv_out)
if "w_in" in locals():
    importlib.reload(w_in)
if "w_out" in locals():
    importlib.reload(w_out)
if "rim_in" in locals():
    importlib.reload(rim_in)
if "rim_out" in locals():
    importlib.reload(rim_out)

from .props.props_mesh import RVMeshProperties
from .props.props_obj import RVObjectProperties
from .props.props_scene import RVSceneProperties
from .common import DialogOperator, TEX_ANIM_MAX, TEX_PAGES_MAX, BAKE_LIGHTS, BAKE_LIGHT_ORIENTATIONS, BAKE_SHADOW_METHODS
from .common import FACE_DOUBLE, FACE_TRANSLUCENT, FACE_MIRROR, FACE_TRANSL_TYPE, FACE_TEXANIM, FACE_NOENV, FACE_ENV, FACE_CLOTH, FACE_SKIP
from .common import NCP_DOUBLE, NCP_NO_SKID, NCP_OIL, NCP_OBJECT_ONLY, NCP_CAMERA_ONLY, NCP_NOCOLL, MATERIALS
from .layers import select_ncp_material, get_face_material, set_face_material, set_face_texture, get_face_texture
from .layers import set_face_ncp_property, get_face_ncp_property, get_face_env, set_face_env, get_face_property, set_face_property
from .operators import ImportRV, ExportRV, RVIO_OT_ReadCarParameters, RVIO_OT_SelectRevoltDirectory, ButtonReExport
from .operators import SelectNCPMaterial, VertexColorRemove, SetVertexColor
from .operators import VertexColorCreateLayer, TexAnimDirection
from .operators import ButtonRenameAllObjects, SelectByName, SelectByData, UseTextureNumber
from .operators import SetInstanceProperty, RemoveInstanceProperty, LaunchRV, TexturesSave
from .operators import TexturesRename, CarParametersExport, ButtonZoneHide, AddTrackZone
from .operators import ToggleTriangulateNgons, ExportWithoutTexture, ToggleApplyScale, ToggleApplyRotation
from .operators import BakeShadow, ToggleEnvironmentMap, ToggleNoMirror, ToggleModelRGB, ToggleFinHide
from .operators import SetEnvironmentMapColor, ToggleNoLights, ToggleNoCameraCollision, ToggleFinPriority
from .operators import ToggleNoObjectCollision, ToggleMirrorPlane, InstanceColor, ResetFinLoDBias
from .operators import SetBCubeMeshIndices, ButtonHullGenerate, ButtonHullSphere, RVIO_OT_ToggleWParentMeshes
from .operators import RVIO_OT_ToggleWImportBoundBoxes, RVIO_OT_ToggleWImportCubes, RVIO_OT_ToggleWImportBigCubes
from .operators import RVIO_OT_NCPExportSelected, RVIO_OT_NCPExportCollgrid, ToggleApplyTranslation, RVIO_OT_NCPGridSize
from .operators import ButtonCopyUvToFrame, ButtonCopyFrameToUv, TexAnimTransform, TexAnimGrid, OBJECT_OT_add_texanim_uv
from .rvstruct import World, PRM, Mesh, BoundingBox, Vector, Matrix, Polygon, Vertex, UV, BigCube, TexAnimation
from .rvstruct import Frame, Color, Instances, Instance, PosNodes, PosNode, NCP, Polyhedron, Plane, LookupGrid
from .rvstruct import LookupList, Hull, ConvexHull, Edge, Interior, Sphere, RIM, MirrorPlane, TrackZones, Zone
from .texanim import update_ta_max_frames, update_ta_current_slot, update_ta_current_frame, update_ta_current_frame_uv
from .texanim import update_ta_current_frame_delay, update_ta_current_frame_tex, get_texture_items, update_ta_max_slots
from .ui.faceprops import RVIO_PT_RevoltFacePropertiesPanel
from .ui.headers import RVIO_PT_RevoltIOToolPanel
from .ui.helpers import RVIO_PT_RevoltHelpersPanelMesh
from .ui.instances import RVIO_PT_RevoltInstancesPanel
from .ui.light import RVIO_PT_RevoltLightPanel
from .ui.texanim import RVIO_PT_AnimModesPanel
from .ui.objectpanel import RVIO_PT_RevoltObjectPanel
from .ui.settings import RVIO_PT_RevoltSettingsPanel
from .ui.vertex import RVIO_PT_VertexPanel
from .ui.zone import RVIO_PT_RevoltZonePanel

bl_info = {
"name": "Re-Volt",
"author": "Marvin Thiel & Theman",
"version": (20, 24, 3),
"blender": (4, 0, 1),
"location": "File > Import-Export",
"description": "Import and export Re-Volt file formats.",
"wiki_url": "https://re-volt.github.io/re-volt-addon/",
"tracker_url": "https://github.com/breathingstatue/blender-plugin/issues",
"support": 'COMMUNITY',
"category": "Import-Export"
}

bmesh_dic = {}  # This global dictionary will store your BMesh objects

@persistent
def edit_object_change_handler(scene):
    """Makes the edit mode bmesh available for use in GUI panels."""
    obj = bpy.context.view_layer.objects.active

    # If no active object or the active object is not a mesh, clear the dictionary and return
    if obj is None or obj.type != 'MESH':
        bmesh_dic.clear()
        return

    # Handle the case where the object is in edit mode
    if obj.mode == 'EDIT':
        try:
            # Set default only if obj.name is not in bmesh_dic, to avoid creating a new bmesh each time
            if obj.name not in bmesh_dic:
                bmesh_dic[obj.name] = bmesh.from_edit_mesh(obj.data)
        except KeyError as e:
            print(f"Error accessing BMesh for object: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    else:
        # If the object is not in edit mode, clear the dictionary
        bmesh_dic.clear()

def register():
    
    # Register Classes
   
    #Register Custom Properties
    props_scene.register()
    props_obj.register()
    props_mesh.register()
    
    bpy.types.Object.is_instance = bpy.props.BoolProperty(
        name = "Is Instance",
        default = False,
        description = "Object is an instanced mesh"
    )
    
    bpy.types.Object.fin_env = bpy.props.BoolProperty(
        name="Use Environment Map",
        default=True
    )
    
    bpy.types.Object.fin_no_mirror = bpy.props.BoolProperty(
        name="Don't show in Mirror Mode",
        default=False
    )
    
    bpy.types.Object.fin_no_lights = bpy.props.BoolProperty(
        name="Is affected by Light",
        default=False
    )
    
    bpy.types.Object.fin_no_cam_coll = bpy.props.BoolProperty(
        name="No Camera Collision",
        default=False
    )
    
    bpy.types.Object.fin_no_obj_coll = bpy.props.BoolProperty(
        name="No Object Collision",
        default=False
    )

    bpy.types.Scene.envidx = bpy.props.IntProperty(
        name="envidx",
        default=0,
        min=0,
        description="Current env color index for importing. Internal only"
    )

    bpy.types.Object.fin_col = bpy.props.FloatVectorProperty(
        name="Model Color",
        subtype='COLOR',
        default=(0.5, 0.5, 0.5),
        min=0.0, max=1.0,
        description="Model RGB color to be added/subtracted:\n1.0: Bright, overrides vertex colors\n"
            "0.5: Default, leaves vertex colors intact\n"
            "0.0: Dark"
    )
    
    bpy.types.Object.fin_envcol = bpy.props.FloatVectorProperty(
        name="Env Color",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0, 1.0),
        min=0.0, max=1.0,
        description="Color of the EnvMap",
        size=4
    )
    
    bpy.types.Object.fin_model_rgb = bpy.props.BoolProperty(
        name="Use Model Color",
        description="Toggle to use the model's color",
        default=False
    )
    
    bpy.types.Object.fin_hide = bpy.props.BoolProperty(
        name="Hide",
        description="Toggle to hide the object in a specific context",
        default=False
    )
    
    bpy.types.Object.fin_priority = bpy.props.IntProperty(
        name="Priority",
        description="Priority for instance. Instance will always be shown if set to 1, hidden if 0.",
        default=1,
        min=0,
        max=1
    )
    
    bpy.types.Object.fin_lod_bias = bpy.props.IntProperty(
        name="LoD Bias",
        description="Level of Detail Bias",
        default=1024,
        min=1,
        max=8192,
        soft_min=1,  # Recommended range start for the slider
        soft_max=8192,  # Recommended range end for the slider
        subtype='UNSIGNED'
    )
    
    bpy.types.Scene.texture_animations = bpy.props.StringProperty(
        name="Texture Animations",
        default="[]",
        description="Storage for Texture animations. Should not be changed by hand"
    )
    
    bpy.types.Scene.ta_max_frames = bpy.props.IntProperty(
        name = "Max Frames",
        min = 1,
        max = TEX_PAGES_MAX,
        default = 2,
        description = "Total number of frames of the current slot. "
                      "All higher frames will be ignored on export"
    )
    
    bpy.types.Scene.ta_max_slots = bpy.props.IntProperty(
        name="Max Used Slots",
        min=1,
        max=TEX_PAGES_MAX,
        default=1,
        description="Total number of texture animation slots. All higher slots will be ignored on export"
    )
    
    bpy.types.Scene.rvio_frame_start = bpy.props.IntProperty(
        name="Start Frame",
        description="Start frame of the animation",
        default=1,
        min=0,
        max=TEX_PAGES_MAX-1
    )

    bpy.types.Scene.rvio_frame_end = bpy.props.IntProperty(
        name="End Frame",
        description="End frame of the animation",
        default=2,
        min=0,
        max=TEX_PAGES_MAX-1
    )

    bpy.types.Scene.delay = bpy.props.FloatProperty(
        name="Frame Duration",
        description="Duration of every frame",
        default=0.02,
        min=0.0,
        max=2.0
    )

    bpy.types.Scene.texture = bpy.props.EnumProperty(
        name="",
        description="Choose a texture",
        items=get_texture_items
    )
    
    bpy.types.Scene.ta_current_slot = bpy.props.IntProperty(
        name = "Texture Slot",
        default = 1,
        min = 0,
        max = TEX_ANIM_MAX-1,
        update = update_ta_current_slot,
        description = "Texture animation slot"
    )
    
    bpy.types.Scene.ta_current_frame_tex = bpy.props.IntProperty(
        name = "Texture",
        default = 0,
        min = -1,
        max = TEX_PAGES_MAX-1,
        update = update_ta_current_frame_tex,
        description = "Texture of the current frame"
    )
    
    bpy.types.Scene.ta_current_frame_delay = bpy.props.FloatProperty(
        name = "Duration",
        default = 0.02,
        min = 0,
        update = update_ta_current_frame_delay,
        description = "Duration of the current frame"
    )
    
    bpy.types.Scene.ta_current_frame = bpy.props.IntProperty(
        name = "Frame",
        default = 1,
        min = 0,
        update = update_ta_current_frame,
        description = "Current frame"
    )
        
    bpy.types.Scene.ta_current_frame_uv0 = bpy.props.FloatVectorProperty(
        name = "UV 0",
        size = 2,
        default = (0, 0),
        update = lambda self, context: update_ta_current_frame_uv(context, 0),
        description = "UV coordinate of the first vertex"
    )
    
    bpy.types.Scene.ta_current_frame_uv1 = bpy.props.FloatVectorProperty(
        name = "UV 1",
        size = 2,
        default = (0, 0),
        update = lambda self, context: update_ta_current_frame_uv(context, 1),
        description = "UV coordinate of the second vertex"
    )
    
    bpy.types.Scene.ta_current_frame_uv2 = bpy.props.FloatVectorProperty(
        name = "UV 2",
        size = 2,
        default = (0, 0),
        update = lambda self, context: update_ta_current_frame_uv(context, 2),
        description = "UV coordinate of the third vertex"
    )
    
    bpy.types.Scene.ta_current_frame_uv3 = bpy.props.FloatVectorProperty(
        name = "UV 3",
        size = 2,
        default = (0, 0),
        update = lambda self, context: update_ta_current_frame_uv(context, 3),
        description = "UV coordinate of the fourth vertex"
    )
    
    bpy.types.Scene.grid_x = bpy.props.IntProperty(
        name="X Resolution",
        min=1,
        default=2,
        max= 256,
        description="Amount of frames along the X axis"
    )
    bpy.types.Scene.grid_y = bpy.props.IntProperty(
        name="Y Resolution",
        min=1,
        default=2,
        max = 256,
        description="Amount of frames along the Y axis"
    )    
    
    bpy.types.Scene.w_parent_meshes = bpy.props.BoolProperty(
        name="Toggle Parent Meshes",
        description="Enable or disable parent meshes",
        default=False
    )
    
    bpy.types.Scene.w_import_bound_boxes = bpy.props.BoolProperty(
        name="Toggle Import Bound Boxes",
        description="Enable or disable import of bounding boxes",
        default=False
    )
    
    bpy.types.Scene.w_import_cubes = bpy.props.BoolProperty(
        name="Import Cubes",
        default=False
    )
    
    bpy.types.Scene.w_import_big_cubes = bpy.props.BoolProperty(
        name="Import Big Cubes",
        default=False
    )

    bpy.types.Scene.triangulate_ngons = bpy.props.BoolProperty(
        name="Triangulate Ngons",
        description="Enable or disable ngon triangulation",
        default=True
    )
  
    bpy.types.Scene.use_tex_num = bpy.props.BoolProperty(
        name = "Use Number for Textures",
        default = False,
        description = "Uses the texture number from the texture layer "
                      "accessible in the tool shelf in Edit mode.\n"
                      "Otherwise, it uses the texture from the texture file"
    )

    bpy.types.Scene.apply_scale = bpy.props.BoolProperty(
        name="Apply Scale on Export",
        default=True,
        description="Apply object scale during export"
    )
    
    bpy.types.Scene.apply_rotation = bpy.props.BoolProperty(
        name="Apply Rotation on Export",
        default=True,
        description="Apply object rotation during export"
    )
    
    bpy.types.Scene.apply_translation = bpy.props.BoolProperty(
        name = "Apply Translation",
        default = False,
        description = "Applies the object location on export. Should be disabled for single/instance ncp files"
    )
    
    bpy.types.Object.is_hull_sphere = bpy.props.BoolProperty(
        name = "Is Interior Sphere",
        default = False,
        description = ""
    )
    
    bpy.types.Object.is_hull_convex = bpy.props.BoolProperty(
        name = "Is Convex Hull",
        default = False,
        description = ""
    )
    
    bpy.types.Object.is_mirror_plane = bpy.props.BoolProperty(
        name = "Is Mirror Plane",
        default = False,
        description = "Object is a mirror plane (.rim)"
    )
    
    bpy.types.Scene.rvgl_dir = bpy.props.StringProperty(
        name="RVGL Directory",
        subtype='DIR_PATH',
        description="Directory where RVGL is located"
    )
    
    bpy.types.Scene.ncp_export_selected = bpy.props.BoolProperty(
        name = "Only export selected",
        default = False,
        description = "Only exports the selected objects"
    )
    
    bpy.types.Scene.ncp_export_collgrid = bpy.props.BoolProperty(
        name = "Export Collision Grid (.w)",
        default = True,
        description = "Export a collision grid to the .ncp file:\n\n"
                      "Enable this if you want to export a level (.w) "
                      ".ncp file"
    )

    bpy.types.Scene.ncp_collgrid_size = bpy.props.IntProperty(
        name="NCP Grid Size",
        default=1024,
        min=512,
        max=8192,
        description="Size of the lookup grid"
    )

    bpy.types.Scene.last_exported_filepath = bpy.props.StringProperty(
        name="Last Exported Filepath",
        description="Filepath used for the last export",
        default="",
        subtype='FILE_PATH'
    )
    
    bpy.types.Object.is_bcube = bpy.props.BoolProperty(
        name="Object is a BigCube",
        description="Makes BigCube properties visible for this object",
        default=False
    )

    bpy.types.Object.is_cube = bpy.props.BoolProperty(
        name="Object is a Cube",
        description="Makes Cube properties visible for this object",
        default=False
    )

    bpy.types.Object.is_bbox = bpy.props.BoolProperty(
        name="Object is a Boundary Box",
        description="Makes BoundBox properties visible for this object",
        default=False
    )
    
    bpy.types.Object.ignore_ncp = bpy.props.BoolProperty(
        name="Ignore Collision (.ncp)",
        description="Ignores the object when exporting to NCP",
        default=False
    )
    
    bpy.types.Scene.prm_check_parameters = bpy.props.BoolProperty(
        name = "Check Parameters for texture",
        default = True,
        description = "Checks car parameters.txt for the texture"
    )
    

    bpy.types.Scene.shadow_quality = bpy.props.IntProperty(
        name = "Quality",
        min = 0,
        max = 32,
        default = 15,
        description = "The amount of samples the shadow is rendered with "
                      "(number of samples taken extra)"
    )
    
    bpy.types.Scene.shadow_resolution = bpy.props.IntProperty(
        name = "Resolution",
        min = 32,
        max = 8192,
        default = 128,
        description = "Texture resolution of the shadow.\n"
                      "Default: 128x128 pixels"
    )
    
    bpy.types.Scene.shadow_softness = bpy.props.FloatProperty(
        name = "Softness",
        min = 0.1,
        max = 100.0,
        default = 1,
        description = "Softness of the shadow "
                      "(Light size for ray shadow sampling)"
    )
    
    bpy.types.Scene.shadow_table = bpy.props.StringProperty(
        name = "Shadowtable",
        default = "",
        description = "Shadow coordinates for use in parameters.txt of cars.\n"
                      "Click to select all, then CTRL C to copy"
    )
    
    bpy.types.Scene.texanim_delta_u = bpy.props.FloatProperty(name="TexAnim Delta U")
    bpy.types.Scene.texanim_delta_v = bpy.props.FloatProperty(name="TexAnim Delta V")
    
    bpy.types.Mesh.select_material = bpy.props.EnumProperty(
        name = "Select Material",
        items = MATERIALS,
        update = select_ncp_material,
        description = "Selects all faces with the selected material"
    )
    
    bpy.types.Mesh.face_material = bpy.props.EnumProperty(
        name = "Material",
        items = MATERIALS,
        get = get_face_material,
        set = set_face_material,
        description = "Surface Material"
    )
    
    bpy.types.Mesh.face_texture = bpy.props.IntProperty(
        name = "Texture",
        get = get_face_texture,
        set = set_face_texture,
        default = 0,
        min = -1,
        max = TEX_PAGES_MAX-1,
        description = "Texture page number:\n-1 is none,\n"
                      "0 is texture page A\n"
                      "1 is texture page B\n"
                      "2 is texture page C\n"
                      "3 is texture page D\n"
                      "4 is texture page E\n"
                      "5 is texture page F\n"
                      "6 is texture page G\n"
                      "7 is texture page H\n"
                      "8 is texture page I\n"
                      "9 is texture page J\n"
                      "For this number to have an effect, "
                      "the \"Use Texture Number\" export setting needs to be "
                      "enabled"
    )
    
    bpy.types.Mesh.face_double_sided = bpy.props.BoolProperty(
        name = "Double sided",
        get = lambda s: bool(get_face_property(s) & FACE_DOUBLE),
        set = lambda s, v: set_face_property(s, v, FACE_DOUBLE),
        description = "The polygon will be visible from both sides in-game"
    )
    
    bpy.types.Mesh.face_translucent = bpy.props.BoolProperty(
        name = "Translucent",
        get = lambda s: bool(get_face_property(s) & FACE_TRANSLUCENT),
        set = lambda s, v: set_face_property(s, v, FACE_TRANSLUCENT),
        description = "Renders the polyon transparent\n(takes transparency "
                      "from the \"Alpha\" vertex color layer or the alpha "
                      "layer of the texture"
    )
    
    bpy.types.Mesh.face_mirror = bpy.props.BoolProperty(
        name = "Mirror",
        get = lambda s: bool(get_face_property(s) & FACE_MIRROR),
        set = lambda s, v: set_face_property(s, v, FACE_MIRROR),
        description = "This polygon covers a mirror area. (?)"
    )
    
    bpy.types.Mesh.face_additive = bpy.props.BoolProperty(
        name = "Additive blending",
        get = lambda s: bool(get_face_property(s) & FACE_TRANSL_TYPE),
        set = lambda s, v: set_face_property(s, v, FACE_TRANSL_TYPE),
        description = "Renders the polygon with additive blending (black "
                      "becomes transparent, bright colors are added to colors "
                      "beneath)"
    )
    
    bpy.types.Mesh.face_texture_animation = bpy.props.BoolProperty(
        name = "Animated",
        get = lambda s: bool(get_face_property(s) & FACE_TEXANIM),
        set = lambda s, v: set_face_property(s, v, FACE_TEXANIM),
        description = "Uses texture animation for this poly (only in .w files)"
    )
    
    bpy.types.Mesh.face_no_envmapping = bpy.props.BoolProperty(
        name = "No EnvMap (.prm)",
        get = lambda s: bool(get_face_property(s) & FACE_NOENV),
        set = lambda s, v: set_face_property(s, v, FACE_NOENV),
        description = "Disables the environment map for this poly (.prm only)"
    )
    
    bpy.types.Mesh.face_envmapping = bpy.props.BoolProperty(
        name = "EnvMapping (.w)",
        get = lambda s: bool(get_face_property(s) & FACE_ENV),
        set = lambda s, v: set_face_property(s, v, FACE_ENV),
        description = "Enables the environment map for this poly (.w only).\n\n"
                      "If enabled on pickup.m, sparks will appear"
                      "around the poly"
    )
    
    bpy.types.Mesh.face_cloth = bpy.props.BoolProperty(
        name = "Cloth effect (.prm)",
        get = lambda s: bool(get_face_property(s) & FACE_CLOTH),
        set = lambda s, v: set_face_property(s, v, FACE_CLOTH),
        description = "Enables the cloth effect used on the Mystery car"
    )
    
    bpy.types.Mesh.face_skip = bpy.props.BoolProperty(
        name = "Do not export",
        get = lambda s: bool(get_face_property(s) & FACE_SKIP),
        set = lambda s, v: set_face_property(s, v, FACE_SKIP),
        description = "Skips the polygon when exporting (not Re-Volt related)"
    )
    
    bpy.types.Mesh.face_env = bpy.props.FloatVectorProperty(
        name = "Environment Color",
        subtype = "COLOR",
        size = 4,
        min = 0.0,
        max = 1.0,
        soft_min = 0.0,
        soft_max = 1.0,
        get = get_face_env,
        set = set_face_env,
        description = "Color of the environment map for World meshes"
    )
    
    bpy.types.Mesh.face_ncp_double = bpy.props.BoolProperty(
        name = "Double-sided",
        get=lambda s: bool(get_face_ncp_property(s) & NCP_DOUBLE),
        set=lambda s, v: set_face_ncp_property(s, v, NCP_DOUBLE),
        description="Enables double-sided collision"
    )
    
    bpy.types.Mesh.face_ncp_object_only = bpy.props.BoolProperty(
        name = "Object Only",
        get=lambda s: bool(get_face_ncp_property(s) & NCP_OBJECT_ONLY),
        set=lambda s, v: set_face_ncp_property(s, v, NCP_OBJECT_ONLY),
        description="Enable collision for objects only (ignores camera)"
    )
    
    bpy.types.Mesh.face_ncp_camera_only = bpy.props.BoolProperty(
        name = "Camera Only",
        get=lambda s: bool(get_face_ncp_property(s) & NCP_CAMERA_ONLY),
        set=lambda s, v: set_face_ncp_property(s, v, NCP_CAMERA_ONLY),
        description="Enable collision for camera only"
    )
    
    bpy.types.Mesh.face_ncp_non_planar = bpy.props.BoolProperty(
        name = "Non-planar",
        get=lambda s: bool(get_face_ncp_property(s) & NCP_NON_PLANAR),
        set=lambda s, v: set_face_ncp_property(s, v, NCP_NON_PLANAR),
        description="Face is non-planar"
    )
    
    bpy.types.Mesh.face_ncp_no_skid = bpy.props.BoolProperty(
        name = "No Skid Marks",
        get=lambda s: bool(get_face_ncp_property(s) & NCP_NO_SKID),
        set=lambda s, v: set_face_ncp_property(s, v, NCP_NO_SKID),
        description="Disable skid marks"
    )
    
    bpy.types.Mesh.face_ncp_oil = bpy.props.BoolProperty(
        name = "Oil",
        get=lambda s: bool(get_face_ncp_property(s) & NCP_OIL),
        set=lambda s, v: set_face_ncp_property(s, v, NCP_OIL),
        description="Ground is oil"
    )
    
    bpy.types.Mesh.face_ncp_nocoll = bpy.props.BoolProperty(
        name = "No Collision",
        get=lambda s: bool(get_face_ncp_property(s) & NCP_NOCOLL),
        set=lambda s, v: set_face_ncp_property(s, v, NCP_NOCOLL),
        description="Face will be ignored when exporting"
    )    
    
    bpy.types.Scene.vertex_color_picker = bpy.props.FloatVectorProperty(
        name = "Object Color",
        subtype = 'COLOR',
        default = (0, 0, 1.0),
        min = 0.0, max=1.0,
        description = "Color picker for painting custom vertex colors"
    )

    
    #Register Operators
    bpy.utils.register_class(DialogOperator)
    bpy.utils.register_class(ImportRV)
    bpy.utils.register_class(ExportRV)
    bpy.utils.register_class(RVIO_OT_ReadCarParameters)
    bpy.utils.register_class(ButtonReExport)
    bpy.utils.register_class(SelectNCPMaterial)
    bpy.utils.register_class(VertexColorCreateLayer)
    bpy.utils.register_class(VertexColorRemove)
    bpy.utils.register_class(SetVertexColor)
    bpy.utils.register_class(TexAnimDirection)
    bpy.utils.register_class(ButtonRenameAllObjects)
    bpy.utils.register_class(SelectByName)
    bpy.utils.register_class(SelectByData)
    bpy.utils.register_class(SetInstanceProperty)
    bpy.utils.register_class(RemoveInstanceProperty)
    bpy.utils.register_class(LaunchRV)
    bpy.utils.register_class(TexturesSave)
    bpy.utils.register_class(TexturesRename)
    bpy.utils.register_class(UseTextureNumber)
    bpy.utils.register_class(CarParametersExport)
    bpy.utils.register_class(ButtonHullGenerate)  
    bpy.utils.register_class(BakeShadow)
    bpy.utils.register_class(ButtonHullSphere)
    bpy.utils.register_class(ButtonCopyUvToFrame)
    bpy.utils.register_class(ButtonCopyFrameToUv)
    bpy.utils.register_class(TexAnimTransform)
    bpy.utils.register_class(TexAnimGrid)
    bpy.utils.register_class(OBJECT_OT_add_texanim_uv)
    bpy.utils.register_class(ButtonZoneHide)
    bpy.utils.register_class(AddTrackZone)
    bpy.utils.register_class(ToggleTriangulateNgons)
    bpy.utils.register_class(ExportWithoutTexture)
    bpy.utils.register_class(ToggleApplyScale)
    bpy.utils.register_class(ToggleApplyRotation)
    bpy.utils.register_class(SetBCubeMeshIndices)
    bpy.utils.register_class(ToggleEnvironmentMap)
    bpy.utils.register_class(SetEnvironmentMapColor)
    bpy.utils.register_class(ToggleModelRGB)
    bpy.utils.register_class(ToggleFinHide)
    bpy.utils.register_class(ToggleFinPriority)
    bpy.utils.register_class(ToggleNoMirror)
    bpy.utils.register_class(ToggleNoLights)
    bpy.utils.register_class(ToggleNoCameraCollision)
    bpy.utils.register_class(ToggleNoObjectCollision)
    bpy.utils.register_class(ToggleMirrorPlane)
    bpy.utils.register_class(InstanceColor)
    bpy.utils.register_class(ResetFinLoDBias)
    bpy.utils.register_class(RVIO_OT_SelectRevoltDirectory)
    bpy.utils.register_class(RVIO_OT_ToggleWParentMeshes)
    bpy.utils.register_class(RVIO_OT_ToggleWImportBoundBoxes)
    bpy.utils.register_class(RVIO_OT_ToggleWImportCubes)
    bpy.utils.register_class(RVIO_OT_ToggleWImportBigCubes)
    bpy.utils.register_class(RVIO_OT_NCPExportSelected)
    bpy.utils.register_class(RVIO_OT_NCPExportCollgrid)
    bpy.utils.register_class(ToggleApplyTranslation)
    bpy.utils.register_class(RVIO_OT_NCPGridSize)
    
    # Register UI
    bpy.utils.register_class(RVIO_PT_RevoltFacePropertiesPanel)
    bpy.utils.register_class(RVIO_PT_RevoltIOToolPanel)
    bpy.utils.register_class(RVIO_PT_RevoltHelpersPanelMesh)
    bpy.utils.register_class(RVIO_PT_RevoltSettingsPanel)
    bpy.utils.register_class(RVIO_PT_AnimModesPanel)
    bpy.utils.register_class(RVIO_PT_VertexPanel)
    bpy.utils.register_class(RVIO_PT_RevoltZonePanel)
    bpy.utils.register_class(RVIO_PT_RevoltInstancesPanel)
    bpy.utils.register_class(RVIO_PT_RevoltLightPanel)
    bpy.utils.register_class(RVIO_PT_RevoltObjectPanel)
    
    # UI and Handlers Registration
    bpy.app.handlers.depsgraph_update_pre.append(edit_object_change_handler)

def unregister():
    
    # UI and Handlers Unregistration
    bpy.app.handlers.depsgraph_update_pre.remove(edit_object_change_handler)
     
    # Unregister Classes

    # Unregister UI
    bpy.utils.unregister_class(RVIO_PT_RevoltObjectPanel)
    bpy.utils.unregister_class(RVIO_PT_RevoltLightPanel)
    bpy.utils.unregister_class(RVIO_PT_RevoltInstancesPanel)
    bpy.utils.unregister_class(RVIO_PT_RevoltZonePanel)
    bpy.utils.unregister_class(RVIO_PT_VertexPanel)
    bpy.utils.unregister_class(RVIO_PT_AnimModesPanel)
    bpy.utils.unregister_class(RVIO_PT_RevoltSettingsPanel)
    bpy.utils.unregister_class(RVIO_PT_RevoltHelpersPanelMesh)
    bpy.utils.unregister_class(RVIO_PT_RevoltIOToolPanel)
    bpy.utils.unregister_class(RVIO_PT_RevoltFacePropertiesPanel)
    
    # Unregister Operators
    bpy.utils.unregister_class(RVIO_OT_NCPGridSize)
    bpy.utils.unregister_class(ToggleApplyTranslation)
    bpy.utils.unregister_class(RVIO_OT_NCPExportCollgrid)
    bpy.utils.unregister_class(RVIO_OT_NCPExportSelected)
    bpy.utils.unregister_class(RVIO_OT_ToggleWImportBigCubes)
    bpy.utils.unregister_class(RVIO_OT_ToggleWImportCubes)
    bpy.utils.unregister_class(RVIO_OT_ToggleWImportBoundBoxes)
    bpy.utils.unregister_class(RVIO_OT_ToggleWParentMeshes)
    bpy.utils.unregister_class(RVIO_OT_SelectRevoltDirectory)
    bpy.utils.unregister_class(ResetFinLoDBias)
    bpy.utils.unregister_class(InstanceColor)
    bpy.utils.unregister_class(ToggleMirrorPlane)
    bpy.utils.unregister_class(ToggleNoObjectCollision)
    bpy.utils.unregister_class(ToggleNoCameraCollision)
    bpy.utils.unregister_class(ToggleNoLights)
    bpy.utils.unregister_class(ToggleNoMirror)
    bpy.utils.unregister_class(ToggleFinPriority)
    bpy.utils.unregister_class(ToggleFinHide)
    bpy.utils.unregister_class(ToggleModelRGB)
    bpy.utils.unregister_class(SetEnvironmentMapColor)
    bpy.utils.unregister_class(ToggleEnvironmentMap)
    bpy.utils.unregister_class(SetBCubeMeshIndices)
    bpy.utils.unregister_class(ToggleApplyRotation)
    bpy.utils.unregister_class(ToggleApplyScale)
    bpy.utils.unregister_class(ExportWithoutTexture)
    bpy.utils.unregister_class(ToggleTriangulateNgons)
    bpy.utils.unregister_class(AddTrackZone)
    bpy.utils.unregister_class(ButtonZoneHide)
    bpy.utils.unregister_class(OBJECT_OT_add_texanim_uv)
    bpy.utils.unregister_class(TexAnimGrid)
    bpy.utils.unregister_class(TexAnimTransform)
    bpy.utils.unregister_class(ButtonCopyFrameToUv)
    bpy.utils.unregister_class(ButtonCopyUvToFrame)
    bpy.utils.unregister_class(ButtonHullSphere)
    bpy.utils.unregister_class(BakeShadow)
    bpy.utils.unregister_class(ButtonHullGenerate) 
    bpy.utils.unregister_class(CarParametersExport)
    bpy.utils.unregister_class(UseTextureNumber)
    bpy.utils.unregister_class(TexturesRename)
    bpy.utils.unregister_class(TexturesSave)
    bpy.utils.unregister_class(LaunchRV)
    bpy.utils.unregister_class(RemoveInstanceProperty)
    bpy.utils.unregister_class(SetInstanceProperty)
    bpy.utils.unregister_class(SelectByData)
    bpy.utils.unregister_class(SelectByName)
    bpy.utils.unregister_class(ButtonRenameAllObjects)
    bpy.utils.unregister_class(TexAnimDirection)
    bpy.utils.unregister_class(VertexColorRemove)
    bpy.utils.unregister_class(SetVertexColor)
    bpy.utils.unregister_class(VertexColorCreateLayer)
    bpy.utils.unregister_class(SelectNCPMaterial)
    bpy.utils.unregister_class(ButtonReExport)
    bpy.utils.unregister_class(RVIO_OT_ReadCarParameters)
    bpy.utils.unregister_class(ExportRV)
    bpy.utils.unregister_class(ImportRV)
    bpy.utils.unregister_class(DialogOperator)
    
    # Unregister Custom Properties
    
    del bpy.types.Scene.vertex_color_picker
    del bpy.types.Mesh.face_ncp_nocoll
    del bpy.types.Mesh.face_ncp_oil
    del bpy.types.Mesh.face_ncp_no_skid
    del bpy.types.Mesh.face_ncp_non_planar
    del bpy.types.Mesh.face_ncp_camera_only
    del bpy.types.Mesh.face_ncp_object_only
    del bpy.types.Mesh.face_ncp_double
    del bpy.types.Mesh.face_env
    del bpy.types.Mesh.face_skip
    del bpy.types.Mesh.face_cloth
    del bpy.types.Mesh.face_envmapping
    del bpy.types.Mesh.face_no_envmapping
    del bpy.types.Mesh.face_texture_animation
    del bpy.types.Mesh.face_additive
    del bpy.types.Mesh.face_mirror
    del bpy.types.Mesh.face_translucent
    del bpy.types.Mesh.face_double_sided
    del bpy.types.Mesh.face_texture
    del bpy.types.Mesh.face_material
    del bpy.types.Mesh.select_material
    del bpy.types.Scene.texanim_delta_v
    del bpy.types.Scene.texanim_delta_u
    del bpy.types.Scene.shadow_table
    del bpy.types.Scene.shadow_softness
    del bpy.types.Scene.shadow_resolution
    del bpy.types.Scene.shadow_quality
    del bpy.types.Scene.prm_check_parameters
    del bpy.types.Object.ignore_ncp
    del bpy.types.Object.is_bbox
    del bpy.types.Object.is_cube
    del bpy.types.Object.is_bcube
    del bpy.types.Scene.last_exported_filepath    
    del bpy.types.Scene.ncp_export_selected
    del bpy.types.Scene.ncp_export_collgrid
    del bpy.types.Scene.ncp_collgrid_size
    del bpy.types.Scene.rvgl_dir
    del bpy.types.Object.is_mirror_plane
    del bpy.types.Object.is_hull_convex
    del bpy.types.Object.is_hull_sphere
    del bpy.types.Scene.apply_scale
    del bpy.types.Scene.triangulate_ngons
    
    del bpy.types.Scene.w_import_cubes
    del bpy.types.Scene.w_import_big_cubes
    del bpy.types.Scene.w_import_bound_boxes
    del bpy.types.Scene.w_parent_meshes
    
    del bpy.types.Scene.grid_y
    del bpy.types.Scene.grid_x
    del bpy.types.Scene.ta_current_frame_uv3
    del bpy.types.Scene.ta_current_frame_uv2
    del bpy.types.Scene.ta_current_frame_uv1
    del bpy.types.Scene.ta_current_frame_uv0
    del bpy.types.Scene.ta_current_frame
    del bpy.types.Scene.ta_current_frame_delay
    del bpy.types.Scene.ta_current_frame_tex
    del bpy.types.Scene.ta_current_slot
    del bpy.types.Scene.texture    
    del bpy.types.Scene.delay
    del bpy.types.Scene.rvio_frame_end
    del bpy.types.Scene.rvio_frame_start
    del bpy.types.Scene.ta_max_frames
    del bpy.types.Scene.ta_max_slots
    del bpy.types.Scene.texture_animations
    del bpy.types.Object.fin_lod_bias
    del bpy.types.Object.fin_priority
    del bpy.types.Object.fin_hide
    del bpy.types.Object.fin_model_rgb
    del bpy.types.Object.fin_envcol
    del bpy.types.Object.fin_col
    del bpy.types.Scene.envidx
    del bpy.types.Object.is_instance
    del bpy.types.Object.fin_no_obj_coll
    del bpy.types.Object.fin_no_cam_coll
    del bpy.types.Object.fin_no_lights
    del bpy.types.Object.fin_no_mirror
    del bpy.types.Object.fin_env
    
    props_mesh.unregister()
    props_obj.unregister()
    props_scene.unregister()

if __name__ == "__main__":
    register()

def dprint(*args):
    """ Debug print function """
    if DEBUG_MODE:
        print("DEBUG:", *args)

dprint("Re-Volt addon successfully registered.")
