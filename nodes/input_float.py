import bpy
from bpy.types import Node


class NODE_OT_input_float(Node):
    bl_idname = 'NODE_OT_input_float'
    bl_label = 'Float Input'
    bl_icon = 'LINENUMBERS_ON'

    value: bpy.props.FloatProperty(name="Value")

    def init(self, context):
        self.outputs.new('NodeSocketFloat', "Float")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'value', text="")

    def update(self):
        if self.outputs:
            self.outputs[0].default_value = self.value
