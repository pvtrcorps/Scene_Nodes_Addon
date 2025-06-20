import bpy
from bpy.types import Node

from ..node_tree import hash_inputs, get_socket_value


class NODE_OT_set_world(Node):
    bl_idname = 'NODE_OT_set_world'
    bl_label = 'Set World'
    bl_icon = 'RADIOBUT_OFF'

    def init(self, context):
        self.inputs.new('SceneNodeSocketType', "Scene")
        self.inputs.new('WorldNodeSocketType', "World")

    def draw_buttons(self, context, layout):
        from ..executor import draw_execute_button
        draw_execute_button(self, layout)

    def update(self):
        scene = get_socket_value(self.inputs.get("Scene"), 'scene')
        world = get_socket_value(self.inputs.get("World"), 'world')
        if scene and world:
            scene.world = world
        self.node_hash = hash_inputs(scene, world)


def register():
    bpy.utils.register_class(NODE_OT_set_world)


def unregister():
    bpy.utils.unregister_class(NODE_OT_set_world)
