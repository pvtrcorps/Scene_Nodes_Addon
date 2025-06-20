import bpy
from bpy.types import Node


class NODE_OT_read_blend_file(Node):
    bl_idname = 'NODE_OT_read_blend_file'
    bl_label = 'Read Blend File'
    bl_icon = 'FILE_FOLDER'

    filepath: bpy.props.StringProperty(name="File Path", subtype='FILE_PATH')

    def init(self, context):
        self.inputs.new('NodeSocketString', 'File Path')
        self.outputs.new('NodeSocketString', 'Scenes')
        self.outputs.new('NodeSocketString', 'Objects')
        self.outputs.new('NodeSocketString', 'Materials')
        self.outputs.new('NodeSocketString', 'Worlds')

    def draw_buttons(self, context, layout):
        layout.prop(self, 'filepath', text="")

    def update(self):
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
            with bpy.data.libraries.load(path, link=False) as (data_from, _):
                scenes = ';'.join(data_from.scenes)
                objects = ';'.join(data_from.objects)
                materials = ';'.join(data_from.materials)
                worlds = ';'.join(data_from.worlds)
        except Exception:
            scenes = objects = materials = worlds = ''
        if self.outputs:
            self.outputs['Scenes'].default_value = scenes
            self.outputs['Objects'].default_value = objects
            self.outputs['Materials'].default_value = materials
            self.outputs['Worlds'].default_value = worlds
