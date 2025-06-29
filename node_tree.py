import bpy
from bpy.types import NodeTree, Node, NodeSocket


def _new_scene_property():
    """Pointer property for storing a Blender Scene."""
    return bpy.props.PointerProperty(name="Scene", type=bpy.types.Scene)

def _new_collection_property():
    """Pointer property for storing a Blender Collection."""
    return bpy.props.PointerProperty(name="Collection", type=bpy.types.Collection)

def _new_object_property():
    """Pointer property for storing a Blender Object."""
    return bpy.props.PointerProperty(name="Object", type=bpy.types.Object)

def _new_camera_property():
    """Pointer property for storing a Blender Camera."""
    return bpy.props.PointerProperty(name="Camera", type=bpy.types.Camera)

def _new_material_property():
    """Pointer property for storing a Blender Material."""
    return bpy.props.PointerProperty(name="Material", type=bpy.types.Material)

def _new_world_property():
    """Pointer property for storing a Blender World."""
    return bpy.props.PointerProperty(name="World", type=bpy.types.World)


class IDItem(bpy.types.PropertyGroup):
    """Collection item storing a reference to any ID datablock."""
    id: bpy.props.PointerProperty(type=bpy.types.ID)

class SceneNodeSocket(NodeSocket):
    bl_idname = 'SceneNodeSocketType'
    bl_label = 'Scene Socket'
    scene: _new_scene_property()
    # socket color
    def draw(self, context, layout, node, text):
        layout.label(text=text)
        if self.is_output and (hasattr(node, 'update') or hasattr(node, 'evaluate')):
            tree = node.id_data
            icon = 'RADIOBUT_ON' if getattr(tree, 'active_node_name', '') == node.name else 'RADIOBUT_OFF'
            op = layout.operator('scene_nodes.execute_to_node', text='', icon=icon, emboss=False)
            op.node_name = node.name

    def draw_color(self, context, node):
        return (0.6, 0.8, 0.2, 1.0)


class CollectionNodeSocket(NodeSocket):
    bl_idname = 'CollectionNodeSocketType'
    bl_label = 'Collection Socket'
    collection: _new_collection_property()

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.8, 0.4, 0.1, 1.0)


class ObjectNodeSocket(NodeSocket):
    bl_idname = 'ObjectNodeSocketType'
    bl_label = 'Object Socket'
    object: _new_object_property()

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.4, 0.6, 0.8, 1.0)


class CameraNodeSocket(NodeSocket):
    bl_idname = 'CameraNodeSocketType'
    bl_label = 'Camera Socket'
    camera: _new_camera_property()

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.7, 0.7, 0.3, 1.0)


class MaterialNodeSocket(NodeSocket):
    bl_idname = 'MaterialNodeSocketType'
    bl_label = 'Material Socket'
    material: _new_material_property()

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.9, 0.5, 0.9, 1.0)


class WorldNodeSocket(NodeSocket):
    bl_idname = 'WorldNodeSocketType'
    bl_label = 'World Socket'
    world: _new_world_property()

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.2, 0.4, 0.8, 1.0)


class ListNodeSocket(NodeSocket):
    """Socket to pass around lists of datablocks."""
    bl_idname = 'ListNodeSocketType'
    bl_label = 'List Socket'
    items_type: bpy.props.StringProperty(name="Items Type", default="")
    items: bpy.props.CollectionProperty(type=IDItem)

    # The square socket shape will be assigned when inputs are created.

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        colors = {
            'SCENE': (0.6, 0.8, 0.2, 1.0),
            'OBJECT': (0.4, 0.6, 0.8, 1.0),
            'MATERIAL': (0.9, 0.5, 0.9, 1.0),
            'WORLD': (0.2, 0.4, 0.8, 1.0),
            'COLLECTION': (0.8, 0.4, 0.1, 1.0),
        }
        return colors.get(self.items_type, (0.8, 0.8, 0.1, 1.0))


class ImportTypeNodeSocket(NodeSocket):
    """Socket to choose how libraries are imported."""
    bl_idname = 'ImportTypeNodeSocketType'
    bl_label = 'Import Type'

    import_type: bpy.props.EnumProperty(
        name="Import Type",
        items=[
            ('APPEND', 'Append', 'Append data blocks'),
            ('LINK', 'Link', 'Link data blocks'),
        ],
        default='APPEND',
    )

    def draw(self, context, layout, node, text):
        layout.prop(self, 'import_type', text=text)

    def draw_color(self, context, node):
        return (0.5, 0.5, 0.8, 1.0)


class FileNodeSocket(NodeSocket):
    """Socket holding a path to a .blend file."""
    bl_idname = 'FileNodeSocketType'
    bl_label = 'File Socket'

    filepath: bpy.props.StringProperty(name="File Path", subtype='FILE_PATH')

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.6, 0.6, 0.6, 1.0)


def get_socket_value(socket, attribute):
    """Retrieve the value from a socket, considering links."""
    if not socket:
        return None
    if socket.is_linked:
        for link in socket.links:
            source = link.from_socket
            value = getattr(source, attribute, None)
            if value is not None and not callable(value):
                return value
    value = getattr(socket, attribute, None)
    if callable(value):
        return None
    return value


def hash_inputs(*values):
    """Return a combined hash of the given values."""
    ids = []
    for val in values:
        if val is None:
            ids.append(None)
        elif hasattr(val, "name"):
            ids.append(val.name)
        else:
            ids.append(val)
    return hash(tuple(ids))

class SCENE_NODES_TREE(NodeTree):
    bl_idname = 'SCENE_NODES_TREE'
    bl_label = 'Scene Nodes'
    bl_icon = 'SCENE_DATA'

    active_node_name: bpy.props.StringProperty(name="Active Node", default="")
    dynamic_scene: _new_scene_property()
    start_scene: _new_scene_property()
    is_executing: bpy.props.BoolProperty(default=False, options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        return True

    def draw_buttons(self, context, layout):
        layout.label(text="Scene Nodes MVP")

