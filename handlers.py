import bpy
from bpy.app.handlers import persistent
from .user_edits import record_object_transform

_LAST_TRANSFORMS = {}

def _transform_state(obj):
    return (
        tuple(obj.location),
        tuple(obj.rotation_euler),
        tuple(obj.scale),
    )

@persistent
def record_transforms(scene, depsgraph):
    """Record object transform changes after depsgraph updates."""
    for update in depsgraph.updates:
        id_ = update.id
        if isinstance(id_, bpy.types.Object):
            obj = id_
            current = _transform_state(obj)
            prev = _LAST_TRANSFORMS.get(obj.name)
            if prev != current:
                record_object_transform(obj)
                _LAST_TRANSFORMS[obj.name] = current

def register_handlers():
    if record_transforms not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(record_transforms)

def unregister_handlers():
    if record_transforms in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(record_transforms)
    _LAST_TRANSFORMS.clear()
