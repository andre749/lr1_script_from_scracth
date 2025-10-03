from graphviz import Digraph
from pythonProject1.afd_lr1 import AfnNode,AfdNode


def create_AFNgraph(node:AfnNode, graph:Digraph)->None:

    if node is None:
        return
    id=node.get_rule()
    if id in graph.source:
        return
    graph.node(id,id)
    create_AFNgraph(node.child, graph)
    if node.child is not None:
        graph.edge(id,node.child.get_rule(),node.shift_token)
    if len(node.epsilon_transitions)==0:
        return
    for n in node.epsilon_transitions:
        create_AFNgraph(n, graph)
        graph.edge(id,n.get_rule(),"e")

def create_AFDgraph(node:AfdNode, graph:Digraph)->None:
    id=node.get_rules()
    if id in graph.source:
        return
    graph.node(id,id)
    for key,afd_node in node.transitions.items():
        create_AFDgraph(afd_node,graph)
        graph.edge(id,afd_node.get_rules(),key)

    return
