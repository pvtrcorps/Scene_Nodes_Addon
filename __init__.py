bl_info = {
    "name": "Scene Nodes",
    "author": "Your Name",
    "version": (0, 1),
    "blender": (3, 0, 0),
    "location": "Node Editor > Scene Nodes",
    "description": "MVP for procedural scene management via nodes",
    "warning": "",
    "category": "Node",
}

import bpy
from .node_tree import SCENE_NODES_TREE
from .nodes.create_scene import NODE_OT_create_scene
from .nodes.render_scene import NODE_OT_render_scene

classes = (
    SCENE_NODES_TREE,
    NODE_OT_create_scene,
    NODE_OT_render_scene,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.scene_nodes_tree = bpy.props.PointerProperty(type=SCENE_NODES_TREE)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.scene_nodes_tree

if __name__ == "__main__":
    register()
