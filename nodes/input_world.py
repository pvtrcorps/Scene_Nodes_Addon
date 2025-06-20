import bpy
from bpy.types import Node


class NODE_OT_input_world(Node):
    bl_idname = 'NODE_OT_input_world'
    bl_label = 'World Input'
    bl_icon = 'WORLD'

    world: bpy.props.PointerProperty(type=bpy.types.World)

    def init(self, context):
        self.outputs.new('WorldNodeSocketType', "World")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'world')

    def update(self):
        if self.outputs and self.world:
            self.outputs[0].world = self.world
