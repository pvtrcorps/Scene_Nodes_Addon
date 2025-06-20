import bpy
from bpy.types import Node


class NODE_OT_read_blend_file(Node):
    bl_idname = 'NODE_OT_read_blend_file'
    bl_label = 'Read Blend File'
    bl_icon = 'FILE_FOLDER'

    filepath: bpy.props.StringProperty(name="File Path", subtype='FILE_PATH')

    def init(self, context):
        self.inputs.new('NodeSocketString', 'File Path')
        scenes = self.outputs.new('ListNodeSocketType', 'Scenes')
        scenes.display_shape = 'SQUARE'
        scenes.items = []
        objects = self.outputs.new('ListNodeSocketType', 'Objects')
        objects.display_shape = 'SQUARE'
        objects.items = []
        materials = self.outputs.new('ListNodeSocketType', 'Materials')
        materials.display_shape = 'SQUARE'
        materials.items = []
        worlds = self.outputs.new('ListNodeSocketType', 'Worlds')
        worlds.display_shape = 'SQUARE'
        worlds.items = []

    def draw_buttons(self, context, layout):
        layout.prop(self, 'filepath', text="")

    def update(self):
        tree = self.id_data
        if not getattr(tree, "is_executing", False):
            return

        if self.outputs:
            collections = {
                'Scenes': bpy.data.scenes,
                'Objects': bpy.data.objects,
                'Materials': bpy.data.materials,
                'Worlds': bpy.data.worlds,
            }
            for name, data in collections.items():
                sock = self.outputs.get(name)
                if not sock:
                    continue
                items_attr = getattr(sock, 'items', [])
                if callable(items_attr):
                    items = []
                else:
                    items = list(items_attr)
                for datablock in items:
                    try:
                        if getattr(datablock, 'users', 0) == 0:
                            data.remove(datablock)
                    except Exception:
                        pass
                if isinstance(sock.items, list):
                    sock.items.clear()
                else:
                    sock.items = []

        path = None
        path_socket = self.inputs.get('File Path')
        if path_socket:
            if path_socket.is_linked:
                for link in path_socket.links:
                    value = getattr(link.from_socket, 'default_value', None)
                    if value:
                        path = value
                        break
            else:
                path = getattr(path_socket, 'default_value', None)
        if not path:
            path = self.filepath
        if not path:
            return
        try:
            with bpy.data.libraries.load(path, link=False) as (data_from, data_to):
                data_to.scenes = list(data_from.scenes)
                data_to.objects = list(data_from.objects)
                data_to.materials = list(data_from.materials)
                data_to.worlds = list(data_from.worlds)
            scenes = list(data_to.scenes)
            objects = list(data_to.objects)
            materials = list(data_to.materials)
            worlds = list(data_to.worlds)
        except Exception:
            scenes = objects = materials = worlds = []
        if self.outputs:
            out = self.outputs
            out['Scenes'].items = scenes
            out['Scenes'].items_type = 'SCENE'
            out['Objects'].items = objects
            out['Objects'].items_type = 'OBJECT'
            out['Materials'].items = materials
            out['Materials'].items_type = 'MATERIAL'
            out['Worlds'].items = worlds
            out['Worlds'].items_type = 'WORLD'
