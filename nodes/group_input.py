import bpy
from bpy.types import Node


class NODE_OT_group_input(Node):
    bl_idname = 'NODE_OT_group_input'
    bl_label = 'Group Input'
    bl_icon = 'GROUP_VERTEX'

    def init(self, context):
        self.outputs.new('SceneNodeSocketType', 'Scene')
        self.outputs.new('FileNodeSocketType', 'File')

    def update(self):
        scene_out = self.outputs.get('Scene')
        file_out = self.outputs.get('File')
        if scene_out:
            scene_out.scene = bpy.context.scene
        if file_out:
            file_out.filepath = bpy.data.filepath
