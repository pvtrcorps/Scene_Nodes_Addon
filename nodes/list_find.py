import bpy
from bpy.types import Node
from ..node_tree import get_socket_value

class NODE_OT_list_find(Node):
    bl_idname = 'NODE_OT_list_find'
    bl_label = 'Find Item in List'
    bl_icon = 'VIEWZOOM'

    def init(self, context):
        self.inputs.new('NodeSocketString', 'List')
        self.inputs.new('NodeSocketString', 'Name')
        self.outputs.new('NodeSocketString', 'Item')
        self.outputs.new('NodeSocketInt', 'Index')

    def update(self):
        list_str = get_socket_value(self.inputs.get('List'), 'default_value') or ''
        name = get_socket_value(self.inputs.get('Name'), 'default_value') or ''
        items = [it for it in list_str.split(';') if it]
        idx = -1
        item = ''
        if name:
            try:
                idx = items.index(name)
                item = items[idx]
            except ValueError:
                idx = -1
                item = ''
        if self.outputs:
            self.outputs['Item'].default_value = item
            self.outputs['Index'].default_value = idx
