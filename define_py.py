from tree import Tree, Node, print_tree
import sys, copy

def define_(node, definer, debug):
    if debug:
        print('defining: ')
        print_tree(node)
    if node.children[1].type != 'fun':  # define value
        if node.children[0].value in definer.var:
            print('Redefining is not allowed.')
            sys.exit(0)
        definer.var[node.children[0].value] = node.children[1]
    elif node.children[1].children[1].type != 'define_in_fun': # define FUN_BODY_no_def
        definer.fun_trees[node.children[0].value] = Tree(node.children[1], definer)
    else: # define FUN_BODY_has_def  define[name, [fun[ids[], body[exp, def_stmts[def_stmts]]]]
        new_fun_tree_root = Node("fun")
        new_fun_ids = copy.deepcopy(node.children[1].children[0])
        new_fun_body = copy.deepcopy(node.children[1].children[1].children[0])
        new_fun_ids.parent = new_fun_tree_root
        new_fun_body.parent = new_fun_tree_root
        if debug:
            print('new_fun_tree_root: ')
            print_tree(new_fun_tree_root)
        new_fun_tree = definer.fun_trees[node.children[0].value] = Tree(new_fun_tree_root, definer)
        for i in range(len(node.children[1].children[1].children[1].children)):
            sub_fun_define = node.children[1].children[1].children[1].children[i]
            define_(sub_fun_define, new_fun_tree, debug)