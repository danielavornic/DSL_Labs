from graphviz import Digraph
from ast_definitions import ASTNode


def render_ast_diagram(node, graph, parent=None):
    if isinstance(node, ASTNode):
        label = f'{node.__class__.__name__}: <B>{node.name}</B>'
        if hasattr(node, 'value'):
            label += f'<BR/>value: {node.value}'

        node_id = str(id(node))
        graph.node(node_id, label=f'<{label}>')

        if parent:
            graph.edge(parent, node_id)

        for attr in ['target_flag', 'command_sequence', 'commands', 'flags', 'next_command']:
            child = getattr(node, attr, None)
            if isinstance(child, list):
                for item in child:
                    render_ast_diagram(item, graph, node_id)
            elif child:
                render_ast_diagram(child, graph, node_id)

    elif isinstance(node, (str, int)):
        label = str(node)
        node_id = str(id(node))
        graph.node(node_id, label=f'<{label}>')
        if parent:
            graph.edge(parent, node_id)
