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
    IDItem,
    SceneNodeSocket,
    CollectionNodeSocket,
    ObjectNodeSocket,
    CameraNodeSocket,
    MaterialNodeSocket,
    WorldNodeSocket,
    ListNodeSocket,
    ImportTypeNodeSocket,
    SCENE_NODES_TREE,
)
from .nodes.create_scene import NODE_OT_create_scene
from .nodes.render_scene import NODE_OT_render_scene
from .nodes.add_collection import NODE_OT_add_collection
from .nodes.set_material import NODE_OT_set_material
from .nodes.set_world import NODE_OT_set_world
from .nodes.input_string import NODE_OT_input_string
from .nodes.input_bool import NODE_OT_input_bool
from .nodes.input_float import NODE_OT_input_float
from .nodes.input_integer import NODE_OT_input_integer
from .nodes.input_vector import NODE_OT_input_vector
from .nodes.input_material import NODE_OT_input_material
from .nodes.input_world import NODE_OT_input_world
from .nodes.input_object import NODE_OT_input_object
from .nodes.read_blend_file import NODE_OT_read_blend_file
from .nodes.list_index import NODE_OT_list_index
from .nodes.list_find import NODE_OT_list_find
from .nodes.list_length import NODE_OT_list_length
from .executor import SCENE_OT_execute_to_node
from .handlers import register_handlers, unregister_handlers

classes = (
    IDItem,
    SceneNodeSocket,
    CollectionNodeSocket,
    ObjectNodeSocket,
    CameraNodeSocket,
    MaterialNodeSocket,
    WorldNodeSocket,
    ListNodeSocket,
    ImportTypeNodeSocket,
    SCENE_NODES_TREE,
    NODE_OT_create_scene,
    NODE_OT_render_scene,
    NODE_OT_add_collection,
    NODE_OT_set_material,
    NODE_OT_set_world,
    NODE_OT_input_string,
    NODE_OT_input_bool,
    NODE_OT_input_float,
    NODE_OT_input_integer,
    NODE_OT_input_vector,
    NODE_OT_input_material,
    NODE_OT_input_world,
    NODE_OT_input_object,
    NODE_OT_read_blend_file,
    NODE_OT_list_index,
    NODE_OT_list_find,
    NODE_OT_list_length,
    SCENE_OT_execute_to_node,
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
        NodeItem(NODE_OT_input_string.bl_idname),
        NodeItem(NODE_OT_input_bool.bl_idname),
        NodeItem(NODE_OT_input_float.bl_idname),
        NodeItem(NODE_OT_input_integer.bl_idname),
        NodeItem(NODE_OT_input_vector.bl_idname),
        NodeItem(NODE_OT_input_material.bl_idname),
        NodeItem(NODE_OT_input_world.bl_idname),
        NodeItem(NODE_OT_input_object.bl_idname),
        NodeItem(NODE_OT_read_blend_file.bl_idname),
        NodeItem(NODE_OT_list_index.bl_idname),
        NodeItem(NODE_OT_list_find.bl_idname),
        NodeItem(NODE_OT_list_length.bl_idname),
    ]),
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.scene_nodes_tree = bpy.props.PointerProperty(type=SCENE_NODES_TREE)
    register_node_categories('SCENE_NODES', node_categories)
    register_handlers()

def unregister():
    unregister_handlers()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.scene_nodes_tree
    unregister_node_categories('SCENE_NODES')

if __name__ == "__main__":
    register()
