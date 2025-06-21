import bpy
from bpy.types import Node

from ..node_tree import hash_inputs


class NODE_OT_add_collection(Node):
    bl_idname = 'NODE_OT_add_collection'
    bl_label = 'Add Collection'
    bl_icon = 'RADIOBUT_OFF'

    collection: bpy.props.PointerProperty(type=bpy.types.Collection)

    def init(self, context):
        self.outputs.new('CollectionNodeSocketType', "Collection")

    def draw_buttons(self, context, layout):
        pass

    def update(self):
        tree = self.id_data
        if not getattr(tree, "is_executing", False):
            return

        output = self.outputs.get("Collection")
        if not output:
            return

        base_name = "Collection"
        col = getattr(self, "collection", None)

        if col is None or col.name not in bpy.data.collections:
            name = base_name
            index = 1
            while name in bpy.data.collections:
                name = f"{base_name}.{index:03d}"
                index += 1
            col = bpy.data.collections.new(name)
            self.collection = col
        else:
            if col.name != base_name and base_name not in bpy.data.collections:
                col.name = base_name

        output.collection = col
        self.node_hash = hash_inputs(col)

    def free(self):
        """Remove the stored collection when the node is deleted."""
        col = getattr(self, "collection", None)
        if col and col.name in bpy.data.collections:
            try:
                if col.users == 0:
                    bpy.data.collections.remove(col)
            except Exception:
                pass
        self.collection = None

