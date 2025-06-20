import bpy

# In-memory store for object transform edits made by the user.
# Keys are Blender object names, values hold location/rotation/scale copies.
_USER_TRANSFORMS = {}


def record_object_transform(obj):
    """Store the current transform values of ``obj`` for later use."""
    if obj is None:
        return
    _USER_TRANSFORMS[obj.name] = {
        "location": obj.location.copy(),
        "rotation_euler": obj.rotation_euler.copy(),
        "scale": obj.scale.copy(),
    }


def apply_object_transform(obj):
    """Apply stored transform values back onto ``obj`` if present."""
    data = _USER_TRANSFORMS.get(obj.name)
    if not data:
        return
    obj.location = data["location"]
    obj.rotation_euler = data["rotation_euler"]
    obj.scale = data["scale"]


def clear_object_transform(obj):
    """Remove stored transform data for ``obj`` if it exists."""
    _USER_TRANSFORMS.pop(obj.name, None)


def apply_user_edits(obj):
    """Convenience wrapper to reapply all known edits for ``obj``."""
    apply_object_transform(obj)
