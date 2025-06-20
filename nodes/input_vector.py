import bpy
from bpy.types import Node


class NODE_OT_input_vector(Node):
    bl_idname = 'NODE_OT_input_vector'
    bl_label = 'Vector Input'
    bl_icon = 'EMPTY_ARROWS'

    value: bpy.props.FloatVectorProperty(name="Value")

    def init(self, context):
        self.outputs.new('NodeSocketVector', "Vector")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'value', text="")

    def update(self):
        if self.outputs:
            self.outputs[0].default_value = self.value
