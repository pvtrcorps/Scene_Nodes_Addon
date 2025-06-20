import bpy
from bpy.types import Node
from ..node_tree import get_socket_value

class NODE_OT_list_index(Node):
    bl_idname = 'NODE_OT_list_index'
    bl_label = 'List Item by Index'
    bl_icon = 'LINENUMBERS_ON'

    def init(self, context):
        self.inputs.new('ListNodeSocketType', 'List')
        self.inputs.new('NodeSocketInt', 'Index')
        self.outputs.new('SceneNodeSocketType', 'Scene')
        self.outputs.new('ObjectNodeSocketType', 'Object')
        self.outputs.new('MaterialNodeSocketType', 'Material')
        self.outputs.new('WorldNodeSocketType', 'World')

    def update(self):
        items = get_socket_value(self.inputs.get('List'), 'items') or []
        item_type = getattr(self.inputs.get('List'), 'items_type', '')
        index = get_socket_value(self.inputs.get('Index'), 'default_value')
        try:
            idx = int(index)
        except (TypeError, ValueError):
            idx = -1
        item = items[idx] if 0 <= idx < len(items) else None
        if self.outputs:
            self.outputs['Scene'].scene = item if item_type == 'SCENE' else None
            self.outputs['Object'].object = item if item_type == 'OBJECT' else None
            self.outputs['Material'].material = item if item_type == 'MATERIAL' else None
            self.outputs['World'].world = item if item_type == 'WORLD' else None
