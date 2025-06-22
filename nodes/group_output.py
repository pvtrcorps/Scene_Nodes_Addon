import bpy
from bpy.types import Node


class NODE_OT_group_output(Node):
    bl_idname = 'NODE_OT_group_output'
    bl_label = 'Group Output'
    bl_icon = 'GROUP_VERTEX'

    def init(self, context):
        self.inputs.new('SceneNodeSocketType', 'Scene')
        self.inputs.new('FileNodeSocketType', 'File')

    def update(self):
        pass
