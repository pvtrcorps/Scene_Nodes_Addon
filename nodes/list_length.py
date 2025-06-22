import bpy
from bpy.types import Node
from ..node_tree import get_socket_value

class NODE_OT_list_length(Node):
    bl_idname = 'NODE_OT_list_length'
    bl_label = 'List Length'
    bl_icon = 'ALIGN_JUSTIFY'

    def init(self, context):
        sock = self.inputs.new('ListNodeSocketType', 'List')
        sock.display_shape = 'SQUARE'
        self.outputs.new('NodeSocketInt', 'Length')

    def update(self):
        items_prop = get_socket_value(self.inputs.get('List'), 'items')
        if not items_prop or callable(items_prop):
            length = 0
        else:
            length = len(items_prop)
        if self.outputs:
            self.outputs['Length'].default_value = length
