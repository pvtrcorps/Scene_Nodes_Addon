import bpy
from bpy.types import Node
from ..node_tree import get_socket_value

class NODE_OT_list_find(Node):
    bl_idname = 'NODE_OT_list_find'
    bl_label = 'Find Item in List'
    bl_icon = 'VIEWZOOM'

    def init(self, context):
        sock = self.inputs.new('ListNodeSocketType', 'List')
        sock.display_shape = 'SQUARE'
        sock.items = []
        self.inputs.new('NodeSocketString', 'Name')
        self.outputs.new('SceneNodeSocketType', 'Scene')
        self.outputs.new('ObjectNodeSocketType', 'Object')
        self.outputs.new('MaterialNodeSocketType', 'Material')
        self.outputs.new('WorldNodeSocketType', 'World')
        self.outputs.new('NodeSocketInt', 'Index')

    def update(self):
        list_socket = self.inputs.get('List')
        items = get_socket_value(list_socket, 'items') or []
        if callable(items):
            items = []
        item_type = getattr(list_socket, 'items_type', '')

        name = get_socket_value(self.inputs.get('Name'), 'default_value') or ''
        idx = -1
        item = None
        if name:
            for i, it in enumerate(items):
                if getattr(it, 'name', '') == name:
                    idx = i
                    item = it
                    break

        if not self.outputs:
            return

        expected = {
            'SCENE': ['Scene', 'Index'],
            'OBJECT': ['Object', 'Index'],
            'MATERIAL': ['Material', 'Index'],
            'WORLD': ['World', 'Index'],
        }.get(item_type, ['Index'])

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
                if hasattr(socket, 'default_value'):
                    socket.default_value = -1

        if 'Scene' in self.outputs:
            self.outputs['Scene'].scene = item if item_type == 'SCENE' else None
        if 'Object' in self.outputs:
            self.outputs['Object'].object = item if item_type == 'OBJECT' else None
        if 'Material' in self.outputs:
            self.outputs['Material'].material = item if item_type == 'MATERIAL' else None
        if 'World' in self.outputs:
            self.outputs['World'].world = item if item_type == 'WORLD' else None
        if 'Index' in self.outputs:
            self.outputs['Index'].default_value = idx
