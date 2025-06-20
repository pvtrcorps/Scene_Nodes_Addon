import bpy
from bpy.types import Node


class NODE_OT_input_integer(Node):
    bl_idname = 'NODE_OT_input_integer'
    bl_label = 'Integer Input'
    bl_icon = 'LINENUMBERS_ON'

    value: bpy.props.IntProperty(name="Value")

    def init(self, context):
        self.outputs.new('NodeSocketInt', "Integer")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'value', text="")

    def update(self):
        if self.outputs:
            self.outputs[0].default_value = self.value
