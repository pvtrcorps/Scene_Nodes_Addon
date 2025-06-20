import bpy
from bpy.types import Node


class NODE_OT_read_blend_file(Node):
    bl_idname = 'NODE_OT_read_blend_file'
    bl_label = 'Read Blend File'
    bl_icon = 'FILE_FOLDER'

    filepath: bpy.props.StringProperty(name="File Path", subtype='FILE_PATH')

    def init(self, context):
        self.inputs.new('NodeSocketString', 'File Path')
        self.outputs.new('ListNodeSocketType', 'Scenes').display_shape = 'SQUARE'
        self.outputs.new('ListNodeSocketType', 'Objects').display_shape = 'SQUARE'
        self.outputs.new('ListNodeSocketType', 'Materials').display_shape = 'SQUARE'
        self.outputs.new('ListNodeSocketType', 'Worlds').display_shape = 'SQUARE'

    def draw_buttons(self, context, layout):
        layout.prop(self, 'filepath', text="")

    def update(self):
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
                items = list(getattr(sock, 'items', []))
                for datablock in items:
                    try:
                        if getattr(datablock, 'users', 0) == 0:
                            data.remove(datablock)
                    except Exception:
                        pass
                sock.items.clear()

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
