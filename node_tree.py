import bpy
from bpy.types import NodeTree, Node, NodeSocket


def _new_scene_property():
    """Pointer property for storing a Blender Scene."""
    return bpy.props.PointerProperty(name="Scene", type=bpy.types.Scene)

class SceneNodeSocket(NodeSocket):
    bl_idname = 'SceneNodeSocketType'
    bl_label = 'Scene Socket'
    scene: _new_scene_property()
    # socket color
    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.6, 0.8, 0.2, 1.0)

class SCENE_NODES_TREE(NodeTree):
    bl_idname = 'SCENE_NODES_TREE'
    bl_label = 'Scene Nodes'
    bl_icon = 'SCENE_DATA'

    @classmethod
    def poll(cls, context):
        return True

    def draw_buttons(self, context, layout):
        layout.label(text="Scene Nodes MVP")

