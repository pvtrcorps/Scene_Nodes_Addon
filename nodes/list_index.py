import bpy
from bpy.types import Node
from ..node_tree import get_socket_value

class NODE_OT_list_index(Node):
    bl_idname = 'NODE_OT_list_index'
    bl_label = 'List Item by Index'
    bl_icon = 'LINENUMBERS_ON'

    def init(self, context):
        sock = self.inputs.new('ListNodeSocketType', 'List')
        sock.display_shape = 'SQUARE'
        sock.items = []
        self.inputs.new('NodeSocketInt', 'Index')
        self.outputs.new('SceneNodeSocketType', 'Scene')
        self.outputs.new('ObjectNodeSocketType', 'Object')
        self.outputs.new('MaterialNodeSocketType', 'Material')
        self.outputs.new('WorldNodeSocketType', 'World')

    def update(self):
        list_socket = self.inputs.get('List')
        items = get_socket_value(list_socket, 'items') or []
        if callable(items):
            items = []
        item_type = getattr(list_socket, 'items_type', '')

        index = get_socket_value(self.inputs.get('Index'), 'default_value')
        try:
            idx = int(index)
        except (TypeError, ValueError):
            idx = -1
        item = items[idx] if 0 <= idx < len(items) else None

        if not self.outputs:
            return

        expected = {
            'SCENE': ['Scene'],
            'OBJECT': ['Object'],
            'MATERIAL': ['Material'],
            'WORLD': ['World'],
        }.get(item_type, [])

        for socket in self.outputs:
            socket.hide = socket.name not in expected
            if socket.hide:
                if hasattr(socket, 'scene'):
                    socket.scene = None
                if hasattr(socket, 'object'):
                    socket.object = None
                if hasattr(socket, 'material'):
                    socket.material = None
                if hasattr(socket, 'world'):
                    socket.world = None

        if 'Scene' in self.outputs:
            self.outputs['Scene'].scene = item if item_type == 'SCENE' else None
        if 'Object' in self.outputs:
            self.outputs['Object'].object = item if item_type == 'OBJECT' else None
        if 'Material' in self.outputs:
            self.outputs['Material'].material = item if item_type == 'MATERIAL' else None
        if 'World' in self.outputs:
            self.outputs['World'].world = item if item_type == 'WORLD' else None
