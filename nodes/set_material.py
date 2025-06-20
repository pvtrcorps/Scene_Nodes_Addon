import bpy
from bpy.types import Node

from ..node_tree import hash_inputs, get_socket_value


class NODE_OT_set_material(Node):
    bl_idname = 'NODE_OT_set_material'
    bl_label = 'Set Material'
    bl_icon = 'MATERIAL'

    def init(self, context):
        self.inputs.new('ObjectNodeSocketType', "Object")
        self.inputs.new('MaterialNodeSocketType', "Material")
        self.outputs.new('ObjectNodeSocketType', "Object")

    def update(self):
        obj = get_socket_value(self.inputs.get("Object"), 'object')
        mat = get_socket_value(self.inputs.get("Material"), 'material')
        if obj and mat and hasattr(obj.data, 'materials'):
            if len(obj.data.materials):
                obj.data.materials[0] = mat
            else:
                obj.data.materials.append(mat)
        if obj:
            self.outputs["Object"].object = obj
        self.node_hash = hash_inputs(obj, mat)


def register():
    bpy.utils.register_class(NODE_OT_set_material)


def unregister():
    bpy.utils.unregister_class(NODE_OT_set_material)
