import bpy
from bpy.types import Node

from ..node_tree import SceneNodeSocket

class NODE_OT_create_scene(Node):
    bl_idname = 'NODE_OT_create_scene'
    bl_label = 'Create Scene'
    bl_icon = 'RADIOBUT_OFF'

    def init(self, context):
        self.outputs.new('SceneNodeSocketType', "Scene")

    def draw_buttons(self, context, layout):
        from ..executor import draw_execute_button
        draw_execute_button(self, layout)

    def update(self):
        output = self.outputs.get("Scene")
        if not output:
            return

        base_name = "Scene"
        name = base_name
        index = 1
        # ensure unique scene name
        while name in bpy.data.scenes:
            name = f"{base_name}.{index:03d}"
            index += 1

        new_scene = bpy.data.scenes.new(name)
        # store the created scene on the socket so it can be passed to other nodes
        output.scene = new_scene

def register():
    bpy.utils.register_class(NODE_OT_create_scene)

def unregister():
    bpy.utils.unregister_class(NODE_OT_create_scene)
