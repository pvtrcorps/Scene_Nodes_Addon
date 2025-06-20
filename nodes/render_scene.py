import bpy
from bpy.types import Node

from ..node_tree import SceneNodeSocket

class NODE_OT_render_scene(Node):
    bl_idname = 'NODE_OT_render_scene'
    bl_label = 'Render Scene'
    bl_icon = 'RADIOBUT_OFF'

    def init(self, context):
        self.inputs.new('SceneNodeSocketType', "Scene")

    def draw_buttons(self, context, layout):
        icon = 'RADIOBUT_ON' if self.id_data.active_node_name == self.name else 'RADIOBUT_OFF'
        op = layout.operator('scene_nodes.execute_to_node', text='', icon=icon, emboss=False)
        op.node_name = self.name



    def update(self):
        tree = self.id_data
        if not getattr(tree, "is_executing", False):
            return

        input_socket = self.inputs.get("Scene")
        if not input_socket:
            return

        scene = None
        # if the socket is linked, get the scene from the connected socket
        if input_socket.is_linked:
            for link in input_socket.links:
                source = link.from_socket
                scene = getattr(source, "scene", None)
                if scene:
                    break
        else:
            scene = getattr(input_socket, "scene", None)

        if not scene:
            return

        window = bpy.context.window
        if not window:
            return

        current_scene = window.scene
        try:
            window.scene = scene
            bpy.ops.render.render()
        finally:
            window.scene = current_scene
