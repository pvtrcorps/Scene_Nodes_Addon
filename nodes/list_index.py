import bpy
from bpy.types import Node
from ..node_tree import get_socket_value

class NODE_OT_list_index(Node):
    bl_idname = 'NODE_OT_list_index'
    bl_label = 'List Item by Index'
    bl_icon = 'LINENUMBERS_ON'

    def init(self, context):
        self.inputs.new('NodeSocketString', 'List')
        self.inputs.new('NodeSocketInt', 'Index')
        self.outputs.new('NodeSocketString', 'Item')

    def update(self):
        list_str = get_socket_value(self.inputs.get('List'), 'default_value') or ''
        index = get_socket_value(self.inputs.get('Index'), 'default_value')
        try:
            idx = int(index)
        except (TypeError, ValueError):
            idx = -1
        items = [it for it in list_str.split(';') if it]
        item = items[idx] if 0 <= idx < len(items) else ''
        if self.outputs:
            self.outputs['Item'].default_value = item
