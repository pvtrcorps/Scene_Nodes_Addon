import bpy
from bpy.types import Node

from ..node_tree import SceneNodeSocket

class NODE_OT_create_scene(Node):
    bl_idname = 'NODE_OT_create_scene'
    bl_label = 'Create Scene'
    bl_icon = 'RADIOBUT_OFF'

    def init(self, context):
        self.outputs.new('SceneNodeSocketType', "Scene")



    def update(self):
        output = self.outputs.get("Scene")
        if not output:
            return

        tree = self.id_data
        scene = getattr(tree, "dynamic_scene", None)

        if scene is None or scene.name not in bpy.data.scenes:
            base_name = "Scene"
            name = base_name
            index = 1
            while name in bpy.data.scenes:
                name = f"{base_name}.{index:03d}"
                index += 1
            scene = bpy.data.scenes.new(name)
            tree.dynamic_scene = scene

        output.scene = scene

def register():
    bpy.utils.register_class(NODE_OT_create_scene)

def unregister():
    bpy.utils.unregister_class(NODE_OT_create_scene)
