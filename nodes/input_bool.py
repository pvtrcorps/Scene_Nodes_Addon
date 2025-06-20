import bpy
from bpy.types import Node


class NODE_OT_input_bool(Node):
    bl_idname = 'NODE_OT_input_bool'
    bl_label = 'Boolean Input'
    bl_icon = 'CHECKBOX_HLT'

    value: bpy.props.BoolProperty(name="Value")

    def init(self, context):
        self.outputs.new('NodeSocketBool', "Boolean")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'value', text="")

    def update(self):
        if self.outputs:
            self.outputs[0].default_value = self.value
