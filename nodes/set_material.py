import bpy
from bpy.types import Node

from ..node_tree import hash_inputs, get_socket_value
from ..user_edits import apply_user_edits


class NODE_OT_set_material(Node):
    bl_idname = 'NODE_OT_set_material'
    bl_label = 'Set Material'
    bl_icon = 'RADIOBUT_OFF'

    def init(self, context):
        self.inputs.new('ObjectNodeSocketType', "Object")
        self.inputs.new('MaterialNodeSocketType', "Material")
        self.outputs.new('ObjectNodeSocketType', "Object")

    def update(self):
        tree = self.id_data
        if not getattr(tree, "is_executing", False):
            return

        obj = get_socket_value(self.inputs.get("Object"), 'object')
        mat = get_socket_value(self.inputs.get("Material"), 'material')
        if obj:
            apply_user_edits(obj)
        if obj and mat and hasattr(obj.data, 'materials'):
            if len(obj.data.materials):
                obj.data.materials[0] = mat
            else:
                obj.data.materials.append(mat)
        if obj:
            self.outputs["Object"].object = obj
        self.node_hash = hash_inputs(obj, mat)

