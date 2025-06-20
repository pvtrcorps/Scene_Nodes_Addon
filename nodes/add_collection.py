import bpy
from bpy.types import Node

from ..node_tree import hash_inputs


class NODE_OT_add_collection(Node):
    bl_idname = 'NODE_OT_add_collection'
    bl_label = 'Add Collection'
    bl_icon = 'RADIOBUT_OFF'

    def init(self, context):
        self.outputs.new('CollectionNodeSocketType', "Collection")

    def draw_buttons(self, context, layout):
        from ..executor import draw_execute_button
        draw_execute_button(self, layout)

    def update(self):
        output = self.outputs.get("Collection")
        if not output:
            return

        base_name = "Collection"
        name = base_name
        index = 1
        while name in bpy.data.collections:
            name = f"{base_name}.{index:03d}"
            index += 1

        new_col = bpy.data.collections.new(name)
        output.collection = new_col
        self.node_hash = hash_inputs(new_col)


def register():
    bpy.utils.register_class(NODE_OT_add_collection)


def unregister():
    bpy.utils.unregister_class(NODE_OT_add_collection)
