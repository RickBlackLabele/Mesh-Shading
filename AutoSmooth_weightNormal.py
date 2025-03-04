bl_info = {
    "name": "Mesh Shading",
    "author": "Rick Black Labele",
    "version": (1, 2),
    "blender": (3, 3, 0),
    "support": 'OFFICIAL',
    "category": "VIEW_3D",
}

import bpy

class MeshShadingPanel(bpy.types.Panel):
    """Panel for mesh shading settings"""
    bl_label = "Mesh Shading"
    bl_idname = "OBJECT_PT_mesh_shading"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Mesh Shading"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Mesh Shading Settings:")
        layout.prop(context.object.data, "use_auto_smooth")
        layout.prop(context.object.data, "auto_smooth_angle", text="Smooth Angle")
        layout.separator()
        layout.operator("object.weight_normal_add", text="Add Weight Normal Modifier")
        layout.operator("object.weight_normal_keep_sharp", text="Keep Sharp")
        layout.operator("object.freeze_rotation_scale", text="Freeze Rotation & Scale")
        layout.operator("object.shade_smooth", text="Shade Smooth/Flat")
        layout.operator("object.shade_smooth_faces", text="Shade Smooth Faces")
        layout.separator()
        layout.operator("mesh.customdata_custom_splitnormals_clear", text="Clear Custom Split Normals")
        layout.separator()
        layout.separator()
        layout.prop(context.space_data.overlay, "show_extra_edge_length", text="Show Extra Edge Length")
        layout.separator()

        # Button to toggle orient matrix usage
        layout.operator("object.toggle_transform_data_origin", text="Pivot Manipulation")

        # Button to set Blend Mode to Alpha Blend
        layout.operator("object.set_blend_mode_alpha", text="Set Blend Mode to Alpha Blend")

        # Extra paragraph for Weight Painting info
        layout.separator()
        layout.label(text="Weight Painting Info:")
        layout.separator()
        layout.label(text="Set Object/Data/Bone Name:")
        layout.prop(context.scene, "custom_weight_painting_name", text="")

        # Button for setting name
        layout.operator("object.weight_painting_operator", text="Set Name")


class UVImageEditorPanel(bpy.types.Panel):
    """UV/Image Editor Panel for UV-related settings"""
    bl_label = "UV Settings"
    bl_idname = "IMAGE_PT_uv_settings"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "UV Tool"

    def draw(self, context):
        layout = self.layout
        layout.label(text="UV Settings:")
        # Add UV-related settings here as needed
        layout.operator("uv.custom1_operator", text="Axis Y Scale 0")
        layout.operator("uv.custom2_operator", text="Axis X Scale 0")
        layout.separator()
        layout.operator("uv.custom3_operator", text="Copy UVs").operation_type = 'COPY'
        layout.operator("uv.custom3_operator", text="Paste UVs").operation_type = 'PASTE'


class SetBlendModeAlphaOperator(bpy.types.Operator):
    """Set Blend Mode to Alpha Blend"""
    bl_idname = "object.set_blend_mode_alpha"
    bl_label = "Set Blend Mode to Alpha Blend"

    def execute(self, context):
        if context.object and context.object.active_material:
            context.object.active_material.blend_method = 'BLEND'
            self.report({'INFO'}, 'Blend Mode set to Alpha Blend')
        else:
            self.report({'WARNING'}, 'No active material found')
        return {'FINISHED'}


class Custom1UVOperator(bpy.types.Operator):
    """Custom UV Operator"""
    bl_idname = "uv.custom1_operator"
    bl_label = "Custom UV Operator"

    def execute(self, context):
        bpy.ops.transform.resize(value=(1, 0, 1),
                                  orient_type='GLOBAL',
                                  orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                  orient_matrix_type='GLOBAL',
                                  constraint_axis=(False, True, False),
                                  mirror=False,
                                  use_proportional_edit=False,
                                  proportional_edit_falloff='SMOOTH',
                                  proportional_size=1,
                                  use_proportional_connected=False,
                                  use_proportional_projected=False,
                                  snap=False,
                                  snap_elements={'INCREMENT'},
                                  use_snap_project=False,
                                  snap_target='CLOSEST',
                                  use_snap_self=True,
                                  use_snap_edit=True,
                                  use_snap_nonedit=True,
                                  use_snap_selectable=False,
                                  alt_navigation=True)

        self.report({'INFO'}, 'Custom UV Operator executed')
        return {'FINISHED'}
        
class Custom2UVOperator(bpy.types.Operator):
    """Custom UV Operator"""
    bl_idname = "uv.custom2_operator"
    bl_label = "Custom UV Operator"

    def execute(self, context):
        bpy.ops.transform.resize(value=(0, 1, 1),
                                  orient_type='GLOBAL',
                                  orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                  orient_matrix_type='GLOBAL',
                                  constraint_axis=(False, True, False),
                                  mirror=False,
                                  use_proportional_edit=False,
                                  proportional_edit_falloff='SMOOTH',
                                  proportional_size=1,
                                  use_proportional_connected=False,
                                  use_proportional_projected=False,
                                  snap=False,
                                  snap_elements={'INCREMENT'},
                                  use_snap_project=False,
                                  snap_target='CLOSEST',
                                  use_snap_self=True,
                                  use_snap_edit=True,
                                  use_snap_nonedit=True,
                                  use_snap_selectable=False,
                                  alt_navigation=True)

        self.report({'INFO'}, 'Custom UV Operator executed')
        return {'FINISHED'}
        
class Custom3UVOperator(bpy.types.Operator):
    """Custom UV Operator"""
    bl_idname = "uv.custom3_operator"
    bl_label = "Custom UV Operator"
    
    operation_type: bpy.props.EnumProperty(
        items=[('COPY', 'Copy', 'Copy UVs'),
               ('PASTE', 'Paste', 'Paste UVs')],
        default='COPY'
    )

    def execute(self, context):
        if self.operation_type == 'COPY':
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.uv.copy()
            self.report({'INFO'}, 'UVs copied')
        elif self.operation_type == 'PASTE':
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.uv.paste()
            self.report({'INFO'}, 'UVs pasted')
            
        return {'FINISHED'}

class WeightNormalAdd(bpy.types.Operator):
    """Add Weight Normal Modifier"""
    bl_idname = "object.weight_normal_add"
    bl_label = "Weight Normal Add"

    def execute(self, context):
        bpy.ops.object.modifier_add(type='WEIGHTED_NORMAL')
        return {'FINISHED'}

class WeightNormalKeepSharp(bpy.types.Operator):
    """Keep Sharp Edges"""
    bl_idname = "object.weight_normal_keep_sharp"
    bl_label = "Weight Normal Keep Sharp"

    def execute(self, context):
        for mod in context.object.modifiers:
            if mod.type == 'WEIGHTED_NORMAL':
                mod.keep_sharp = True
                break
        return {'FINISHED'}

class FreezeRotationScale(bpy.types.Operator):
    """Freeze Rotation and Scale"""
    bl_idname = "object.freeze_rotation_scale"
    bl_label = "Freeze Rotation & Scale"

    def execute(self, context):
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        return {'FINISHED'}

class ShadeSmoothOperator(bpy.types.Operator):
    """Toggle between smooth and flat shading"""
    bl_idname = "object.shade_smooth"
    bl_label = "Shade Smooth/Flat"

    def execute(self, context):
        obj = context.active_object
        for face in obj.data.polygons:
            face.use_smooth = not face.use_smooth
        return {'FINISHED'}

class ShadeSmoothFacesOperator(bpy.types.Operator):
    """Shade Smooth Selected Faces"""
    bl_idname = "object.shade_smooth_faces"
    bl_label = "Shade Smooth Faces"

    def execute(self, context):
        obj = context.active_object
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.mesh.faces_shade_smooth()
        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}
        
class ClearCustomSplitNormals(bpy.types.Operator):
    """Clear Custom Split Normals"""
    bl_idname = "mesh.clear_custom_splitnormals"
    bl_label = "Clear Custom Split Normals"

    def execute(self, context):
        bpy.ops.mesh.customdata_custom_splitnormals_clear()
        return {'FINISHED'}        
        
class WeightPaintingOperator(bpy.types.Operator):
    """Weight Painting Operator"""
    bl_idname = "object.weight_painting_operator"
    bl_label = "Weight Painting Operator"

    def execute(self, context):
        name = context.scene.custom_weight_painting_name
        if context.object:
            context.object.name = name
            if context.object.data:
                context.object.data.name = name
        if context.object and context.object.type == 'ARMATURE':
            armature = context.object
            for bone in armature.pose.bones:
                bone.name = name
            armature_data = armature.data
            if hasattr(armature_data, 'collections'):
                for bone_collection in armature_data.collections:
                    bone_collection.name = name
        return {'FINISHED'}
        
        
class ToggleTransformDataOrigin(bpy.types.Operator):
    """Toggle Transform Data Origin"""
    bl_idname = "object.toggle_transform_data_origin"
    bl_label = "Pivot Manipulation"

    def execute(self, context):
        bpy.context.tool_settings.use_transform_data_origin = not bpy.context.tool_settings.use_transform_data_origin
        return {'FINISHED'}

def register():
    bpy.types.Scene.custom_weight_painting_name = bpy.props.StringProperty(name="Name for Object/Data/Bone")
    bpy.utils.register_class(MeshShadingPanel)
    bpy.utils.register_class(WeightNormalAdd)
    bpy.utils.register_class(WeightNormalKeepSharp)
    bpy.utils.register_class(FreezeRotationScale)
    bpy.utils.register_class(ShadeSmoothFacesOperator)
    bpy.utils.register_class(ClearCustomSplitNormals)
    bpy.utils.register_class(UVImageEditorPanel)
    bpy.utils.register_class(Custom1UVOperator)
    bpy.utils.register_class(Custom2UVOperator) 
    bpy.utils.register_class(Custom3UVOperator)
    bpy.utils.register_class(WeightPaintingOperator)
    bpy.utils.register_class(ToggleTransformDataOrigin)
    bpy.utils.register_class(SetBlendModeAlphaOperator)
    
def unregister():
    bpy.utils.unregister_class(MeshShadingPanel)
    bpy.utils.unregister_class(WeightNormalAdd)
    bpy.utils.unregister_class(WeightNormalKeepSharp)
    bpy.utils.unregister_class(FreezeRotationScale)
    bpy.utils.unregister_class(ShadeSmoothFacesOperator)
    bpy.utils.unregister_class(ClearCustomSplitNormals)
    bpy.utils.unregister_class(UVImageEditorPanel)
    bpy.utils.unregister_class(Custom1UVOperator) 
    bpy.utils.unregister_class(Custom2UVOperator) 
    bpy.utils.unregister_class(Custom3UVOperator)
    bpy.utils.unregister_class(WeightPaintingOperator)
    bpy.utils.unregister_class(ToggleTransformDataOrigin)
    bpy.utils.unregister_class(SetBlendModeAlphaOperator)

if __name__ == "__main__":
    register()
