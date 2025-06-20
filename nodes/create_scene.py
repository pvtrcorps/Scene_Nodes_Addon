import bpy
from bpy.types import Node

from ..node_tree import SceneNodeSocket

class NODE_OT_create_scene(Node):
    bl_idname = 'NODE_OT_create_scene'
    bl_label = 'Create Scene'
    bl_icon = 'SCENE_DATA'

    def init(self, context):
        self.outputs.new('SceneNodeSocketType', "Scene")

    def update(self):
        # placeholder: create a new scene on execution
        pass

def register():
    bpy.utils.register_class(NODE_OT_create_scene)

def unregister():
    bpy.utils.unregister_class(NODE_OT_create_scene)
