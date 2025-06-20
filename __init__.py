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
from nodeitems_utils import (
    NodeCategory,
    NodeItem,
    register_node_categories,
    unregister_node_categories,
)
from .node_tree import (
    SceneNodeSocket,
    CollectionNodeSocket,
    ObjectNodeSocket,
    CameraNodeSocket,
    MaterialNodeSocket,
    WorldNodeSocket,
    SCENE_NODES_TREE,
)
from .nodes.create_scene import NODE_OT_create_scene
from .nodes.render_scene import NODE_OT_render_scene
from .nodes.add_collection import NODE_OT_add_collection
from .nodes.set_material import NODE_OT_set_material
from .nodes.set_world import NODE_OT_set_world

classes = (
    SceneNodeSocket,
    CollectionNodeSocket,
    ObjectNodeSocket,
    CameraNodeSocket,
    MaterialNodeSocket,
    WorldNodeSocket,
    SCENE_NODES_TREE,
    NODE_OT_create_scene,
    NODE_OT_render_scene,
    NODE_OT_add_collection,
    NODE_OT_set_material,
    NODE_OT_set_world,
)

# node categories for the Add menu
class SceneNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == SCENE_NODES_TREE.bl_idname

node_categories = [
    SceneNodeCategory('SCENE_NODES', 'Scene Nodes', items=[
        NodeItem(NODE_OT_create_scene.bl_idname),
        NodeItem(NODE_OT_render_scene.bl_idname),
        NodeItem(NODE_OT_add_collection.bl_idname),
        NodeItem(NODE_OT_set_material.bl_idname),
        NodeItem(NODE_OT_set_world.bl_idname),
    ]),
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.scene_nodes_tree = bpy.props.PointerProperty(type=SCENE_NODES_TREE)
    register_node_categories('SCENE_NODES', node_categories)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.scene_nodes_tree
    unregister_node_categories('SCENE_NODES')

if __name__ == "__main__":
    register()
