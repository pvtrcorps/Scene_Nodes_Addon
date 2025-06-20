class NodeExecutor:
    """Utility class to evaluate Scene Node graphs."""
    def __init__(self, node_tree):
        self.node_tree = node_tree

    def _build_graph(self):
        graph = {node: set() for node in self.node_tree.nodes}
        for link in self.node_tree.links:
            graph.setdefault(link.from_node, set()).add(link.to_node)
            graph.setdefault(link.to_node, set())
        return graph

    def _topological_order(self):
        graph = self._build_graph()
        indegree = {node: 0 for node in graph}
        for frm, targets in graph.items():
            for tgt in targets:
                indegree[tgt] += 1
        queue = [n for n, d in indegree.items() if d == 0]
        order = []
        while queue:
            node = queue.pop(0)
            order.append(node)
            for tgt in graph[node]:
                indegree[tgt] -= 1
                if indegree[tgt] == 0:
                    queue.append(tgt)
        return order

    def execute_until(self, target_node=None):
        """Execute nodes in topological order up to ``target_node``."""
        tree = self.node_tree
        tree.is_executing = True
        try:
            order = self._topological_order()
            for node in order:
                if hasattr(node, 'evaluate'):
                    node.evaluate()
                elif hasattr(node, 'update'):
                    node.update()
                if target_node and node == target_node:
                    break
        finally:
            tree.is_executing = False


import bpy
from bpy.types import Operator


def update_node_icons(tree):
    """Redraw node editors so execution buttons refresh their icons."""
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'NODE_EDITOR':
                area.tag_redraw()


class SCENE_OT_execute_to_node(Operator):
    bl_idname = 'scene_nodes.execute_to_node'
    bl_label = 'Execute Scene Nodes'

    node_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return getattr(context.space_data, 'node_tree', None) is not None

    def execute(self, context):
        tree = context.space_data.node_tree
        node = tree.nodes.get(self.node_name)
        if node is None:
            self.report({'ERROR'}, 'Node not found')
            return {'CANCELLED'}
        executor = NodeExecutor(tree)
        executor.execute_until(node)
        tree.active_node_name = node.name
        update_node_icons(tree)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SCENE_OT_execute_to_node)


def unregister():
    bpy.utils.unregister_class(SCENE_OT_execute_to_node)
