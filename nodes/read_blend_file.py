import bpy
from bpy.types import Node

from ..node_tree import get_socket_value


class NODE_OT_read_blend_file(Node):
    bl_idname = 'NODE_OT_read_blend_file'
    bl_label = 'Read Blend File'
    bl_icon = 'FILE_FOLDER'

    filepath: bpy.props.StringProperty(name="File Path", subtype='FILE_PATH')

    def init(self, context):
        self.inputs.new('NodeSocketString', 'File Path')
        sock = self.inputs.new('ImportTypeNodeSocketType', 'Import Type')
        sock.import_type = 'APPEND'
        scenes = self.outputs.new('ListNodeSocketType', 'Scenes')
        scenes.display_shape = 'SQUARE'
        objects = self.outputs.new('ListNodeSocketType', 'Objects')
        objects.display_shape = 'SQUARE'
        materials = self.outputs.new('ListNodeSocketType', 'Materials')
        materials.display_shape = 'SQUARE'
        worlds = self.outputs.new('ListNodeSocketType', 'Worlds')
        worlds.display_shape = 'SQUARE'

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
                for item in list(sock.items):
                    datablock = item.id
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
        import_type = get_socket_value(self.inputs.get('Import Type'), 'import_type') or 'APPEND'
        link = import_type == 'LINK'
        try:
            with bpy.data.libraries.load(path, link=link) as (data_from, data_to):
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
            mapping = {
                'Scenes': (scenes, 'SCENE'),
                'Objects': (objects, 'OBJECT'),
                'Materials': (materials, 'MATERIAL'),
                'Worlds': (worlds, 'WORLD'),
            }
            for name, (items, typ) in mapping.items():
                sock = out.get(name)
                if not sock:
                    continue
                sock.items.clear()
                for datablock in items:
                    item = sock.items.add()
                    item.id = datablock
                sock.items_type = typ
                for link in sock.links:
                    link.to_node.update()
