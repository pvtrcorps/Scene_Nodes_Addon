# Scene Nodes Addon

This is a simple example addon that demonstrates a basic node tree for procedural scene management in Blender.

## Installation

1. Download or clone this repository.
2. In Blender, go to *Edit > Preferences > Add-ons* and click *Install*.
3. Select the directory containing this addon and enable **Scene Nodes**.

## Usage

Once enabled, open the *Geometry Node Editor* and switch the tree type to **Scene Nodes**. Use the **Add** menu to access the custom nodes:

- **Create Scene** — outputs a dynamic scene reused across executions.
- **Render Scene** — takes a scene input and renders it.
- **Add Collection** — creates a new collection datablock.
- **Set Material** — assign a material to an object.
- **Set World** — assign a world to a scene.
- **Read Blend File** — load datablock names from an external blend file.
- **Input Nodes** — provide basic values (String, Bool, Float, Integer, Vector, Object, Material, World).
- **List Nodes** — work with semicolon separated string lists (Length, Item by Index, Find Item).

These nodes are registered under the *Scene Nodes* category.

### Manual Execution

Only nodes that operate on scenes display a small circle icon in their header.
Clicking this icon evaluates the graph up to the clicked node using a simple
dependency solver. The circle for the most recently executed node is filled to
indicate the active scene state.

## User Edits

Object transforms or other adjustments made manually after evaluating the node tree can be stored so they persist across updates. Use the helper functions in `user_edits.py` to manage these values:

```python
from .user_edits import record_object_transform, apply_object_transform

# After editing an object
record_object_transform(obj)

# Before a node overwrites an object transform
apply_object_transform(obj)
```

Nodes may call `apply_object_transform` (or the convenience wrapper `apply_user_edits`) when they need to preserve user tweaks while re-evaluating the graph.

The addon also registers a handler on Blender's dependency graph updates that automatically calls `record_object_transform` whenever an object is moved, rotated or scaled. Transform values are stored for each node so manual adjustments persist across evaluations.
