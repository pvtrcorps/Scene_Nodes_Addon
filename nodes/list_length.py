import bpy
from bpy.types import Node
from ..node_tree import get_socket_value

class NODE_OT_list_length(Node):
    bl_idname = 'NODE_OT_list_length'
    bl_label = 'List Length'
    bl_icon = 'ALIGN_JUSTIFY'

    def init(self, context):
        self.inputs.new('ListNodeSocketType', 'List')
        self.outputs.new('NodeSocketInt', 'Length')

    def update(self):
        items = get_socket_value(self.inputs.get('List'), 'items') or []
        length = len(items)
        if self.outputs:
            self.outputs['Length'].default_value = length
