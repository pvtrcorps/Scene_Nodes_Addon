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
        self.outputs.new('SceneNodeSocketType', "Scene")

    def draw_buttons(self, context, layout):
        icon = 'RADIOBUT_ON' if self.id_data.active_node_name == self.name else 'RADIOBUT_OFF'
        op = layout.operator('scene_nodes.execute_to_node', text='', icon=icon, emboss=False)
        op.node_name = self.name



    def update(self):
        tree = self.id_data
        if not getattr(tree, "is_executing", False):
            return

        scene = get_socket_value(self.inputs.get("Scene"), 'scene')
        world = get_socket_value(self.inputs.get("World"), 'world')
        if scene and world:
            scene.world = world
        if scene:
            self.outputs["Scene"].scene = scene
        self.node_hash = hash_inputs(scene, world)

