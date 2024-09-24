from anytree import NodeMixin, RenderTree

class Tree(object):
    def __init__(self, root, definer = None):
        self.root = root
        self.var = {}
        self.fun_trees = {} #name->tree(exp)
        self.definer = definer

class Node(NodeMixin):
    def __init__(self, type, value = None, parent = None):
        self.type = type
        if value != None:
            self.value = value
        self.parent = parent

def print_tree(tree):
    for pre, _, node in RenderTree(tree):
        tree_str = u"%s%s" % (pre, node.type)
        if hasattr(node, 'value'):
            print(tree_str.ljust(8), node.value)
        else:
            print(tree_str.ljust(8))
    print('\n')
