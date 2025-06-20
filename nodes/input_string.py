import bpy
from bpy.types import Node


class NODE_OT_input_string(Node):
    bl_idname = 'NODE_OT_input_string'
    bl_label = 'String Input'
    bl_icon = 'SORTALPHA'

    value: bpy.props.StringProperty(name="Value")

    def init(self, context):
        self.outputs.new('NodeSocketString', "String")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'value', text="")

    def update(self):
        if self.outputs:
            self.outputs[0].default_value = self.value
