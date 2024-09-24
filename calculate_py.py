from tree import Tree, Node, print_tree
import sys, copy

def calculate(node, runner, debug):
    if not hasattr(node, 'type'):
        print('Warning: ' + str(node) + ' is not a node')
        return node
    if debug:
        print('calculating: ')
        print_tree(node)
    if node.type == "print_num":
        print(int(calculate(node.children[0], runner, debug)))
    if node.type == "print_bool":
        if calculate(node.children[0], runner, debug) == True:
            print("#t")
        else:
            print("#f")
    
    if node.type == "bool":
        if debug:
            print('returning: ' + str(node.value))
        return node.value
    
    if node.type == "number":
        if debug:
            print('returning: ' + str(node.value))
        return node.value
    
    if node.type == "variable":
        if debug:
            print(runner.var)
            print(runner.fun_trees)
            print("variable:")
            print_tree(node)
        if node.value in runner.var: # variable存int, bool
            if debug:
                if hasattr(runner.var[node.value], 'type'):
                    print("runner.var[node.value]:")
                    print_tree(runner.var[node.value])
                else:
                    print(runner.var[node.value])
            return calculate(runner.var[node.value], runner, debug)
        elif node.value in runner.fun_trees: #variable存fun
            if debug:
                if hasattr(runner.fun_trees[node.value], 'root'):
                    print("runner.fun_trees[node.value].root:")
                    print_tree(runner.fun_trees[node.value].root)
                else:
                    print(runner.fun_trees[node.value])
            return runner.fun_trees[node.value]
        
        if runner.definer != None: # 往下找
            definer = runner.definer
            while definer != None:
                if node.value in definer.var: # variable存int, bool 
                    if debug:
                        print("definer.var[node.value]:")
                        print_tree(definer.var[node.value])
                    return calculate(definer.var[node.value], definer, debug)
                elif node.value in runner.fun_trees: #variable存fun return tree
                    if debug:
                        print("runner.fun_trees[node.value].root:")
                        print_tree(runner.fun_trees[node.value].root)
                    return runner.fun_trees[node.value]
                definer = definer.definer
        print('variable ' + str(node.value) + ' not defined')
        sys.exit(1)
    
    if node.type == "+":
        res = 0
        for child in node.children:
            value = calculate(child, runner, debug)
            if isinstance(value, Tree):
                print("Type Error: Expect \'number\' but got \'function\'")
                sys.exit(1)
            elif type(value) is not int:
                print("Type Error: Expect \'number\' but got \'boolean\'")
                sys.exit(1)
            res += value
        if debug:
            print('returning: ' + str(res))
        return res
    if node.type == "-":
        first = calculate(node.children[0], runner, debug)
        second = calculate(node.children[1], runner, debug)
        if isinstance(first, Tree) or isinstance(second, Tree):
            print("Type Error: Expect \'number\' but got \'function\'")
            sys.exit(1)
        elif (type(first) is not int) or (type(second) is not int):
            print("Type Error: Expect \'number\' but got \'boolean\'")
            sys.exit(1)
        res = first - second
        if debug:
            print('returning: ' + str(res))
        return res
    if node.type == "*":
        res = 1
        for child in node.children:
            value = calculate(child, runner, debug)
            if isinstance(value, Tree):
                print("Type Error: Expect \'number\' but got \'function\'")
                sys.exit(1)
            elif type(value) is not int:
                print("Type Error: Expect \'number\' but got \'boolean\'")
                sys.exit(1)
            res *= value
        if debug:
            print('returning: ' + str(res))
        return res
    if node.type == "//":
        first = calculate(node.children[0], runner, debug)
        second = calculate(node.children[1], runner, debug)
        if isinstance(first, Tree) or isinstance(second, Tree):
            print("Type Error: Expect \'number\' but got \'function\'")
            sys.exit(1)
        elif (type(first) is not int) or (type(second) is not int):
            print("Type Error: Expect \'number\' but got \'boolean\'")
            sys.exit(1)
        res = first // second
        if debug:
            print('returning: ' + str(res))
        return res
    if node.type == "%":
        first = calculate(node.children[0], runner, debug)
        second = calculate(node.children[1], runner, debug)
        if isinstance(first, Tree) or isinstance(second, Tree):
            print("Type Error: Expect \'number\' but got \'function\'")
            sys.exit(1)
        elif (type(first) is not int) or (type(second) is not int):
            print("Type Error: Expect \'number\' but got \'boolean\'")
            sys.exit(1)
        res = first % second
        if debug:
            print('returning: ' + str(res))
        return res
    if node.type == ">":
        first = calculate(node.children[0], runner, debug)
        second = calculate(node.children[1], runner, debug)
        if isinstance(first, Tree) or isinstance(second, Tree):
            print("Type Error: Expect \'number\' but got \'function\'")
            sys.exit(1)
        elif (type(first) is not int) or (type(second) is not int):
            print("Type Error: Expect \'number\' but got \'boolean\'")
            sys.exit(1)
        res = (first > second)
        if debug:
            print('returning: ' + str(res))
        return res
    if node.type == "<":
        first = calculate(node.children[0], runner, debug)
        second = calculate(node.children[1], runner, debug)
        if isinstance(first, Tree) or isinstance(second, Tree):
            print("Type Error: Expect \'number\' but got \'function\'")
            sys.exit(1)
        elif (type(first) is not int) or (type(second) is not int):
            print("Type Error: Expect \'number\' but got \'boolean\'")
            sys.exit(1)
        res = (first < second)
        if debug:
            print('returning: ' + str(res))
        return res
    if node.type == "=":
        res = True
        value = calculate(node.children[0], runner, debug)
        if isinstance(value, Tree):
            print("Type Error: Expect \'number\' but got \'function\'")
            sys.exit(1)
        if type(value) is not int:
            print("Type Error: Expect \'number\' but got \'boolean\'")
            sys.exit(1)
        for child in node.children:
            next_value = calculate(child, runner, debug)
            if isinstance(next_value, Tree):
                print("Type Error: Expect \'number\' but got \'function\'")
                sys.exit(1)
            if type(next_value) is not int:
                print("Type Error: Expect \'number\' but got \'boolean\'")
                sys.exit(1)
            res = (res and (next_value == value))
        if debug:
            print('returning: ' + str(res))
        return res
    if node.type == "and":
        res = True
        for child in node.children:
            value = calculate(child, runner, debug)
            if isinstance(value, Tree):
                print("Type Error: Expect \'boolean\' but got \'function\'")
                sys.exit(1)
            elif type(value) is not bool:
                print("Type Error: Expect \'boolean\' but got \'number\'")
                sys.exit(1)
            res = (value and res)
        if debug:
            print('returning: ' + str(res))
        return res
    if node.type == "or":
        res = False
        for child in node.children:
            value = calculate(child, runner, debug)
            if isinstance(value, Tree):
                print("Type Error: Expect \'boolean\' but got \'function\'")
                sys.exit(1)
            elif type(value) is not bool:
                print("Type Error: Expect \'boolean\' but got \'number\'")
                sys.exit(1)
            res = (value or res)
        if debug:
            print('returning: ' + str(res))
        return res
    if node.type == "not":
        value = calculate(node.children[0], runner, debug)
        if isinstance(value, Tree):
            print("Type Error: Expect \'boolean\' but got \'function\'")
            sys.exit(1)
        elif type(value) is not bool:
            print("Type Error: Expect \'boolean\' but got \'number\'")
            sys.exit(1)
        res = not value
        if debug:
            print('returning: ' + str(res))
        return res
        
    if node.type == 'call_exp_no_param':
        return calculate(node.children[0].children[1], runner, debug)
    if node.type == 'call_exp_params': # [fun[ids[], define_in_fun[exp, def_stmts[def_stmts]]], params[params]]
        if debug:
            print('variables: ' + str(runner.var))
            print('functions: ' + str(runner.fun_trees))
            print('definer: ' + str(runner.definer))
        tmp_tree = Tree(node.children[0].children[1], runner)
        for index, id in enumerate(node.children[0].children[0].value):
            if node.children[1].children[index].type == 'fun': # param is fun
                tmp_tree.fun_trees[id] = Tree(node.children[1].children[index], runner)
                if debug:
                    print(f"fun_tree.fun_trees[{id}].root:")
                    print_tree(fun_tree.fun_trees[id].root)
            else:
                id_value = calculate(node.children[1].children[index], runner, debug) #param_inputs
                if isinstance(id_value, Tree): # param of fun
                    tmp_tree.fun_trees[id] = id_value
                    if debug:
                        print(f"fun_tree.fun_trees[{id}].root:")
                        print_tree(fun_tree.fun_trees[id].root)
                else: # param of int or bool
                    tmp_tree.var[id] = node.children[1].children[index]
                    if debug:
                        print(f"tmp_tree.var[{id}]:")
                        print_tree(tmp_tree.var[id])
        if debug:
            print(tmp_tree.var)
            print(tmp_tree.fun_trees)
        return calculate(tmp_tree.root, tmp_tree, debug)
    if node.type == 'call_name_no_param':
        if debug:
            print('variables: ' + str(runner.var))
            print('functions: ' + str(runner.fun_trees))
            print('definer: ' + str(runner.definer))
        fun_name = node.children[0].value
        if fun_name in runner.fun_trees: # fun_name in fun tree
            fun_tree = runner.fun_trees[fun_name]
            if debug:
                print(fun_tree.root)
                print_tree(fun_tree.root)
            if fun_tree.root.children[1].type == 'fun':
                return Tree(fun_tree.root.children[1], fun_tree)
            return calculate(fun_tree.root.children[1], fun_tree, debug)
        elif fun_name in runner.var: # fun_name is variable
            fun_tree = calculate(runner.var[fun_name], runner, debug)
            if isinstance(fun_tree, Tree): # the variable is fun
                fun_tree = Tree(fun_tree, runner)
                if debug:
                    print(fun_tree.root)
                    print_tree(fun_tree.root)
                if fun_tree.root.children[1].type == 'fun':
                    return Tree(fun_tree.root.children[1], fun_tree)
                return calculate(fun_tree.root.children[1], fun_tree, debug)
            else:
                if type(fun_tree) is int:
                    print("Type Error: Expect \'function\' but got \'number\'")
                else:
                    print("Type Error: Expect \'function\' but got \'boolean\'")
                sys.exit(1)
        if runner.definer != None: # 往下找
            definer = runner.definer
            while definer != None:
                if fun_name in definer.fun_trees: # fun_name in fun tree
                    fun_tree = definer.fun_trees[fun_name]
                    if debug:
                        print("fun_tree.root")
                        print_tree(fun_tree.root)
                    if fun_tree.root.children[1].type == 'fun':
                        return Tree(fun_tree.root.children[1], fun_tree)
                    return calculate(fun_tree.root.children[1], fun_tree, debug) #body
                elif fun_name in runner.var: # fun_name is variable
                    fun_tree = calculate(runner.var[fun_name], runner, debug)
                    if isinstance(fun_tree, Tree): # the variable is fun
                        if debug:
                            print(fun_tree.root)
                            print_tree(fun_tree.root)
                        if fun_tree.root.children[1].type == 'fun':
                            return Tree(fun_tree.root.children[1], fun_tree)
                        return calculate(fun_tree.root.children[1], fun_tree, debug)
                    else:
                        if type(fun_tree) is int:
                            print("Type Error: Expect \'function\' but got \'number\'")
                        else:
                            print("Type Error: Expect \'function\' but got \'boolean\'")
                        sys.exit(1)
                definer = definer.definer
        print('function ' + str(fun_name) + ' not defined')
        sys.exit(1)
    if node.type == 'call_name_params':
        if debug:
            print('variables: ' + str(runner.var))
            print('functions: ' + str(runner.fun_trees))
            print('definer: ' + str(runner.definer))
        fun_name = node.children[0].value
        if fun_name in runner.fun_trees: # fun_name in fun tree
            fun_tree = copy.deepcopy(runner.fun_trees[fun_name])
            for index, id in enumerate(fun_tree.root.children[0].value): # params
                if node.children[1].children[index].type == 'fun': # param is fun
                    fun_tree.fun_trees[id] = Tree(node.children[1].children[index], runner)
                    if debug:
                        print(f"fun_tree.fun_trees[{id}].root:")
                        print_tree(fun_tree.fun_trees[id].root)
                else: 
                    id_value = calculate(node.children[1].children[index], runner, debug) #param_inputs
                    if isinstance(id_value, Tree): # param of fun
                        fun_tree.fun_trees[id] = id_value
                        if debug:
                            print(f"fun_tree.fun_trees[{id}].root:")
                            print_tree(fun_tree.fun_trees[id].root)
                    else: # param of value
                        if type(id_value) is int:
                            id_node = Node("number", value=id_value)
                        elif type(id_value) is bool:
                            id_node = Node("bool", value=id_value)
                        fun_tree.var[id] = id_node
                        if debug:
                            print(f"fun_tree.var[{id}]:")
                            print_tree(fun_tree.var[id])
            if fun_tree.root.children[1].type == 'fun':
                return Tree(fun_tree.root.children[1], fun_tree)
            return calculate(fun_tree.root.children[1], fun_tree, debug)
        elif fun_name in runner.var: # fun_name is variable
            fun_tree = calculate(runner.var[fun_name], runner, debug)
            if isinstance(fun_tree, Tree): # the variable is fun
                for index, id in enumerate(fun_tree.root.children[0].value): # params
                    if node.children[1].children[index].type == 'fun': # param is fun
                        fun_tree.fun_trees[id] = Tree(node.children[1].children[index], runner)
                        if debug:
                            print(f"fun_tree.fun_trees[{id}].root:")
                            print_tree(fun_tree.fun_trees[id].root)
                    else:
                        id_value = calculate(node.children[1].children[index], runner, debug) #param_inputs
                        if isinstance(id_value, Tree): # param of fun
                            if id_value.root.type == 'fun':
                                fun_tree.fun_trees[id] = id_value
                                if debug:
                                    print(f"fun_tree.fun_trees[{id}].root:")
                                    print_tree(fun_tree.fun_trees[id].root)
                            else:
                                if type(calculate(id_value.root, id_value, debug)) is int:
                                    print("Type Error: Expect \'function\' but got \'number\'")
                                else:
                                    print("Type Error: Expect \'function\' but got \'boolean\'")
                                sys.exit(1)
                        else: # param of value
                            if type(id_value) is int:
                                id_node = Node("number", value=id_value)
                            elif type(id_value) is bool:
                                id_node = Node("bool", value=id_value)
                            fun_tree.var[id] = id_node
                            if debug:
                                print(f"fun_tree.var[{id}]:")
                                print_tree(fun_tree.var[id])
                if fun_tree.root.children[1].type == 'fun':
                    return Tree(fun_tree.root.children[1], fun_tree)
                return calculate(fun_tree.root.children[1], fun_tree, debug)
            else:
                if type(fun_tree) is int:
                    print("Type Error: Expect \'function\' but got \'number\'")
                else:
                    print("Type Error: Expect \'function\' but got \'boolean\'")
                sys.exit(1)
            
        if runner.definer != None: # 往下找
            definer = runner.definer
            while definer != None:
                if fun_name in definer.fun_trees:  # fun_name in fun tree
                    fun_tree = copy.deepcopy(definer.fun_trees[fun_name])
                    for index, id in enumerate(fun_tree.root.children[0].value):
                        if node.children[1].children[index].type == 'fun': # param is fun
                            fun_tree.fun_trees[id] = Tree(node.children[1].children[index], runner)
                            if debug:
                                print(f"fun_tree.fun_trees[{id}].root:")
                                print_tree(fun_tree.fun_trees[id].root)
                        else: 
                            id_value = calculate(node.children[1].children[index], runner, debug) #param_inputs
                            if isinstance(id_value, Tree): # param of fun
                                fun_tree.fun_trees[id] = id_value
                                if debug:
                                    print(f"fun_tree.fun_trees[{id}].root:")
                                    print_tree(fun_tree.fun_trees[id].root)
                            else: # param of value
                                if type(id_value) is int:
                                    id_node = Node("number", value=id_value)
                                elif type(id_value) is bool:
                                    id_node = Node("bool", value=id_value)
                                fun_tree.var[id] = id_node
                                if debug:
                                    print(f"fun_tree.var[{id}]:")
                                    print_tree(fun_tree.var[id])
                    if fun_tree.root.children[1].type == 'fun':
                        return Tree(fun_tree.root.children[1], fun_tree)
                    return calculate(fun_tree.root.children[1], fun_tree, debug)
                elif fun_name in runner.var:  # fun_name is variable
                    fun_tree = calculate(runner.var[fun_name], runner, debug)
                    if isinstance(fun_tree, Tree): # the variable store fun
                        for index, id in enumerate(fun_tree.root.children[0].value): # params
                            if node.children[1].children[index].type == 'fun': # param is fun
                                fun_tree.fun_trees[id] = Tree(node.children[1].children[index], runner)
                                if debug:
                                    print(f"fun_tree.fun_trees[{id}].root:")
                                    print_tree(fun_tree.fun_trees[id].root)
                            else:
                                id_value = calculate(node.children[1].children[index], runner, debug) #param_inputs
                                if isinstance(id_value, Tree): # param of fun
                                    fun_tree.fun_trees[id] = id_value
                                    if debug:
                                        print(f"fun_tree.fun_trees[{id}].root:")
                                        print_tree(fun_tree.fun_trees[id].root)
                                else:  # param of var
                                    if type(id_value) is int:
                                        id_node = Node("number", value=id_value)
                                    elif type(id_value) is bool:
                                        id_node = Node("bool", value=id_value)
                                    fun_tree.var[id] = id_node
                                    if debug:
                                        print(f"fun_tree.var[{id}]:")
                                        print_tree(fun_tree.var[id])
                        if fun_tree.root.children[1].type == 'fun':
                            return Tree(fun_tree.root.children[1], fun_tree)
                        return calculate(fun_tree.root.children[1], fun_tree, debug)
                    else:
                        if type(fun_tree) is int:
                            print("Type Error: Expect \'function\' but got \'number\'")
                        else:
                            print("Type Error: Expect \'function\' but got \'boolean\'")
                        sys.exit(1)
                definer = definer.definer
        print('function ' + str(fun_name) + ' not defined')
        sys.exit(1)
    
    if node.type == "if_branch": # if[test, [then, else]]
        res = None
        test_value = calculate(node.children[0], runner, debug)
        if type(test_value) is not bool:
            print("Type Error: Expect \'boolean\' but got \'number\'")
            sys.exit(1)
        if test_value:
            res = calculate(node.children[1].children[0], runner, debug)
        else:
            res = calculate(node.children[1].children[1], runner, debug)
        if debug:
            print('returning:'+ str(res))
        return res