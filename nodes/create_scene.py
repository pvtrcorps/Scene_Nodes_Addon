import bpy
from bpy.types import Node

from ..node_tree import SceneNodeSocket

class NODE_OT_create_scene(Node):
    bl_idname = 'NODE_OT_create_scene'
    bl_label = 'Create Scene'
    bl_icon = 'RADIOBUT_OFF'

    scene_name: bpy.props.StringProperty(name="Scene Name", default="")

    def init(self, context):
        self.inputs.new('NodeSocketString', "Name")
        self.outputs.new('SceneNodeSocketType', "Scene")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'scene_name', text="")



    def update(self):
        output = self.outputs.get("Scene")
        if not output:
            return

        tree = self.id_data
        scene = getattr(tree, "dynamic_scene", None)

        name_socket = self.inputs.get("Name")
        name = None
        if name_socket:
            if name_socket.is_linked:
                for link in name_socket.links:
                    value = getattr(link.from_socket, "default_value", None)
                    if value:
                        name = value
                        break
            else:
                name = getattr(name_socket, "default_value", None)

        if not name:
            name = self.scene_name or "Scene"

        if scene is None or scene.name not in bpy.data.scenes:
            base_name = name
            unique = base_name
            index = 1
            while unique in bpy.data.scenes:
                unique = f"{base_name}.{index:03d}"
                index += 1
            scene = bpy.data.scenes.new(unique)
            tree.dynamic_scene = scene
        else:
            if scene.name != name and name not in bpy.data.scenes:
                scene.name = name

        output.scene = scene

def register():
    bpy.utils.register_class(NODE_OT_create_scene)

def unregister():
    bpy.utils.unregister_class(NODE_OT_create_scene)
