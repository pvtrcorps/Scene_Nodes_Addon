import bpy
from bpy.types import Node


class NODE_OT_input_object(Node):
    bl_idname = 'NODE_OT_input_object'
    bl_label = 'Object Input'
    bl_icon = 'OBJECT_DATA'

    object: bpy.props.PointerProperty(type=bpy.types.Object)

    def init(self, context):
        self.outputs.new('ObjectNodeSocketType', "Object")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'object')

    def update(self):
        if self.outputs and self.object:
            self.outputs[0].object = self.object
