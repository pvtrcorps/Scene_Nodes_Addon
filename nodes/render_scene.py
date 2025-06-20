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
        # placeholder: trigger render on execution
        pass

def register():
    bpy.utils.register_class(NODE_OT_render_scene)

def unregister():
    bpy.utils.unregister_class(NODE_OT_render_scene)
