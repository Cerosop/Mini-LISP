import sys
import ply.yacc as yacc
from lex import tokens 
from tree import Tree, Node, print_tree

main_tree = Tree(Node('root'))

def p_PROGRAM(p):
    'PROGRAM : STMT_PLUS'

def p_STMT_PLUS(p):
    '''STMT_PLUS    : STMT
                    | STMT STMT_PLUS'''
    p[1].parent = main_tree.root

def p_STMT_exp(p):
    '''STMT : EXP'''
    p[0] = Node("stmt")
    p[1].parent = p[0]
def p_STMT_def(p):
    '''STMT : DEF_STMT'''
    p[0] = p[1]
def p_STMT_print(p):
    '''STMT : PRINT_STMT'''
    p[0] = Node("stmt")
    p[1].parent = p[0]

def p_PRINT_STMT_num(p):
    '''PRINT_STMT : lpr print_num EXP rpr'''
    p[0] = Node("print_num")
    p[3].parent = p[0]
def p_PRINT_STMT_bool(p):
    '''PRINT_STMT : lpr print_bool EXP rpr'''
    p[0] = Node("print_bool")
    p[3].parent = p[0]

def p_EXP_bool(p):
    '''EXP : bool_'''
    p[0] = Node("bool", value=p[1])
def p_EXP_number(p):
    '''EXP : number'''
    p[0] = Node("number", value=p[1])
def p_EXP_var(p):
    '''EXP : VARIABLE'''
    p[0] = Node("variable", value=p[1])
def p_EXP_num_op(p):
    '''EXP : NUM_OP'''
    p[0] = p[1]
def p_EXP_logical_op(p):
    '''EXP : LOGICAL_OP'''
    p[0] = p[1]
def p_EXP_fun_exp(p):
    '''EXP : FUN_EXP'''
    p[0] = p[1]
def p_EXP_fun_call(p):
    '''EXP : FUN_CALL'''
    p[0] = p[1]
def p_EXP_if(p):
    '''EXP : IF_EXP'''
    p[0] = p[1]

def p_VARIABLE(p):
    '''VARIABLE : id'''
    p[0] = p[1]

def p_NUM_OP(p):
    '''NUM_OP   : PLUS
                | MINUS
                | MULTIPLY
                | DIVIDE
                | MODULUS
                | GREATER
                | SMALLER
                | EQUAL'''
    p[0] = p[1]

def p_PLUS(p):
    '''PLUS : lpr plus EXP PLUS_EXP_PLUS rpr'''
    p[0] = Node("+")
    p[3].parent = p[0]
    p[4].parent = p[0]
def p_PLUS_EXP_PLUS_one(p):
    '''PLUS_EXP_PLUS : EXP'''
    p[0] = p[1]
def p_PLUS_EXP_PLUS_more(p):
    '''PLUS_EXP_PLUS : EXP PLUS_EXP_PLUS'''
    p[0] = Node("+")
    p[1].parent = p[0]
    p[2].parent = p[0]

def p_MINUS(p):
    '''MINUS : lpr minus EXP EXP rpr'''
    p[0] = Node("-")
    p[3].parent = p[0]
    p[4].parent = p[0]

def p_MULTIPLY(p):
    '''MULTIPLY : lpr mul EXP MUL_EXP_PLUS rpr'''
    p[0] = Node("*")
    p[3].parent = p[0]
    p[4].parent = p[0]
def p_MUL_EXP_PLUS_one(p):
    '''MUL_EXP_PLUS : EXP'''
    p[0] = p[1]
def p_MUL_EXP_PLUS_more(p):
    '''MUL_EXP_PLUS : EXP MUL_EXP_PLUS'''
    p[0] = Node("*")
    p[1].parent = p[0]
    p[2].parent = p[0]

def p_DIVIDE(p):
    '''DIVIDE : lpr div EXP EXP rpr'''
    p[0] = Node("//")
    p[3].parent = p[0]
    p[4].parent = p[0]

def p_MODULUS(p):
    '''MODULUS : lpr mod EXP EXP rpr'''
    p[0] = Node("%")
    p[3].parent = p[0]
    p[4].parent = p[0]

def p_GREATER(p):
    '''GREATER : lpr greater EXP EXP rpr'''
    p[0] = Node(">")
    p[3].parent = p[0]
    p[4].parent = p[0]

def p_SMALLER(p):
    '''SMALLER : lpr smaller EXP EXP rpr'''
    p[0] = Node("<")
    p[3].parent = p[0]
    p[4].parent = p[0]

def p_EQUAL(p):
    '''EQUAL : lpr equal EXP EQUAL_EXP_PLUS rpr'''
    p[0] = Node("=")
    p[3].parent = p[0]
    if p[4].type == "=":
        for node in p[4].children:
            node.parent = p[0]
    else:
        p[4].parent = p[0]
def p_EQUAL_EXP_PLUS_one(p):
    '''EQUAL_EXP_PLUS   : EXP'''
    p[0] = p[1]
def p_EQUAL_EXP_PLUS_more(p):
    '''EQUAL_EXP_PLUS   : EXP EQUAL_EXP_PLUS'''
    p[0] = Node("=")
    p[1].parent = p[0]
    if p[2].type == "=":
        for node in p[2].children:
            node.parent = p[0]
    else:
        p[2].parent = p[0]

def p_LOGICAL_OP(p):
    '''LOGICAL_OP : AND_OP
                  | OR_OP
                  | NOT_OP'''
    p[0] = p[1]

def p_AND_OP(p):
    '''AND_OP : lpr and EXP AND_EXP_PLUS rpr'''
    p[0] = Node("and")
    p[3].parent = p[0]
    p[4].parent = p[0]
def p_AND_EXP_PLUS_one(p):
    '''AND_EXP_PLUS : EXP'''
    p[0] = p[1]
def p_AND_EXP_PLUS_more(p):
    '''AND_EXP_PLUS : EXP AND_EXP_PLUS'''
    p[0] = Node("and")
    p[1].parent = p[0]
    p[2].parent = p[0]

def p_OR_OP(p):
    '''OR_OP : lpr or EXP OR_EXP_PLUS rpr'''
    p[0] = Node("or")
    p[3].parent = p[0]
    p[4].parent = p[0]
def p_OR_EXP_PLUS_one(p):
    '''OR_EXP_PLUS  : EXP'''
    p[0] = p[1]
def p_OR_EXP_PLUS_more(p):
    '''OR_EXP_PLUS  : EXP OR_EXP_PLUS'''
    p[0] = Node("or")
    p[1].parent = p[0]
    p[2].parent = p[0]

def p_NOT_OP(p):
    '''NOT_OP : lpr not EXP rpr'''
    p[0] = Node("not")
    p[3].parent = p[0]

def p_DEF_STMT(p):
    '''DEF_STMT : lpr define VARIABLE EXP rpr'''
    name = Node("define_name", value=p[3])
    p[0] = Node("define")
    name.parent = p[0]
    p[4].parent = p[0]

def p_FUN_EXP(p):
    '''FUN_EXP : lpr fun_ FUN_IDs FUN_BODY rpr'''
    p[0] = Node("fun")
    p[3].parent = p[0]
    p[4].parent = p[0]

def p_FUN_IDs_no_id(p):
    '''FUN_IDs  : lpr rpr'''
    p[0] = Node("no_id")
def p_FUN_IDs_ids(p):
    '''FUN_IDs  : lpr ID_PLUS rpr'''
    p[0] = Node("ids", value=p[2])
def p_ID_PLUS_id_one(p):
    '''ID_PLUS  : id'''
    p[0] = [p[1]]
def p_ID_PLUS_id_more(p):
    '''ID_PLUS  : id ID_PLUS'''
    p[0] = p[2] + [p[1]]

def p_FUN_BODY_no_def(p):
    '''FUN_BODY  : EXP'''
    p[0] = p[1]
def p_FUN_BODY_has_def(p):
    '''FUN_BODY  : DEF_STMT_PLUS EXP'''
    p[0] = Node("define_in_fun")
    p[2].parent = p[0]
    def_stmts = Node("def_stmts")
    for def_stmt in p[1]:
        def_stmt.parent = def_stmts
    def_stmts.parent = p[0]
def p_DEF_STMT_PLUS_one(p):
    '''DEF_STMT_PLUS : DEF_STMT'''
    p[0] = [p[1]]
def p_DEF_STMT_PLUS_more(p):
    '''DEF_STMT_PLUS : DEF_STMT_PLUS DEF_STMT'''
    p[0] = [p[2]] + p[1]

def p_FUN_CALL_exp_no_param(p):
    '''FUN_CALL : lpr FUN_EXP rpr'''
    p[0] = Node("call_exp_no_param")
    p[2].parent = p[0]
def p_FUN_CALL_exp_params(p): 
    '''FUN_CALL : lpr FUN_EXP PARAM_PLUS rpr'''
    p[0] = Node("call_exp_params")
    p[2].parent = p[0]
    params = Node("params")
    for param in p[3]:
        param.parent = params
    params.parent = p[0]
def p_FUN_CALL_name_no_param(p):
    '''FUN_CALL : lpr FUN_NAME rpr'''
    p[0] = Node("call_name_no_param")
    p[2].parent = p[0]
def p_FUN_CALL_name_params(p):
    '''FUN_CALL : lpr FUN_NAME PARAM_PLUS rpr'''
    p[0] = Node("call_name_params")
    p[2].parent = p[0]
    params = Node("params")
    for param in p[3]:
        param.parent = params
    params.parent = p[0]
def p_PARAM(p):
    '''PARAM : EXP'''
    p[0] = p[1]
def p_PARAM_PLUS_one(p):
    '''PARAM_PLUS   : PARAM'''
    p[0] = [p[1]]
def p_PARAM_PLUS_more(p):
    '''PARAM_PLUS   : PARAM PARAM_PLUS'''
    p[0] = p[2] + [p[1]]
def p_FUN_NAME(p):
    '''FUN_NAME  : id'''
    p[0] = Node("fun_name", value=p[1])

def p_IF_EXP(p):
    '''IF_EXP : lpr if_ TEST_EXP THEN_EXP ELSE_EXP rpr'''
    assign = Node("assign")
    p[4].parent = assign
    p[5].parent = assign
    p[0] = Node("if_branch")
    p[3].parent = p[0]
    assign.parent = p[0]
def p_TEST_EXP(p):
    '''TEST_EXP : EXP'''
    p[0] = p[1]
def p_THEN_EXP(p):
    '''THEN_EXP : EXP'''
    p[0] = p[1]
def p_ELSE_EXP(p):
    '''ELSE_EXP : EXP'''
    p[0] = p[1]

def p_error(p):
    # print("error: ")
    # print_tree(main_tree.root)
    # print("Syntax error in input: ", p)       # for debugging
    print("syntax error")
    sys.exit(1)

def Reverse(tuples):
    new_tup = tuples[::-1]
    return new_tup


parser = yacc.yacc()

# with open(sys.argv[1]) as f:
#     s = f.read()
debug = False
s = '''
(define fact
  (fun (n) (if (< n 3) n
               (* n (fact (- n 1))))))

(print-num (fact 11))
(print-num (fact 12))
(print-num (fact 13))
(print-num (fact 14))

(define fib (fun (x)
  (if (< x 2) x (+
                 (fib (- x 1))
                 (fib (- x 2))))))

(print-num (fib 2))
(print-num (fib 4))
(print-num (fib 6))
(print-num (fib 11))
(print-num (fib 21))

'''
# debug = True

parser.parse(s)
main_tree.root.children = Reverse(main_tree.root.children)
if debug:
    print_tree(main_tree.root)

from define_py import define_
from calculate_py import calculate
for node in main_tree.root.children:
    if node.type == "stmt":
        calculate(node.children[0], main_tree, debug)
    elif node.type == "define":
        define_(node, main_tree, debug)


# '''
# (define d (fun (y) (+ 1 y)))
# (define add-x
#   (fun () d))

# (define z (add-x))

# (print-num (z 1))
# '''->d not define