import bpy
from bpy.types import Node


class NODE_OT_input_material(Node):
    bl_idname = 'NODE_OT_input_material'
    bl_label = 'Material Input'
    bl_icon = 'MATERIAL'

    material: bpy.props.PointerProperty(type=bpy.types.Material)

    def init(self, context):
        self.outputs.new('MaterialNodeSocketType', "Material")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'material')

    def update(self):
        if self.outputs and self.material:
            self.outputs[0].material = self.material
