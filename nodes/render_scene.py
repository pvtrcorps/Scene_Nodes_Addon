import bpy
from bpy.types import Node

from ..node_tree import SceneNodeSocket

class NODE_OT_render_scene(Node):
    bl_idname = 'NODE_OT_render_scene'
    bl_label = 'Render Scene'
    bl_icon = 'RENDER_STILL'

    def init(self, context):
        self.inputs.new('SceneNodeSocketType', "Scene")

    def update(self):
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

def register():
    bpy.utils.register_class(NODE_OT_render_scene)

def unregister():
    bpy.utils.unregister_class(NODE_OT_render_scene)
