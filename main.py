import ply.yacc as yacc
from lexer import tokens, precedence
import os
import sys


temp_list = []

class Node:
    def __init__(self, type, children=None):
         self.type = type
         self.children = children

    def add_children(self, children):
        self.children += children
        return self

    def children_str(self):
        st = []
        for part in self.children:
            st.append(str(part))
        return "\n\n|__".join(st)

    def __repr__(self):
        if self.type == 'return':
            return self.type + ":\n\t|__" + self.children
        return self.type + ":\n\t|__" + self.children_str().replace("\n", "\n\t")

def p_program(p):
    '''program : program_body func'''
    p[0] = Node('program', [p[1], p[2]])

def p_program_body(p):
    '''program_body :
                    | program_body func'''
    if len(p) > 1:
        if p[1] is None:
            p[1] = Node('body', [])
        p[0] = p[1].add_children([p[2]])

def p_func(p):
    '''func : FUNC NAME LBR args RBR LFB func_body RFB'''
    p[0] = Node(p[2], [p[4], p[7]])

def p_args(p):
    '''args :
            | expression
            | args COMMA NAME'''
    if len(p) == 1:
        p[0] = Node('args', [])
    elif len(p) == 2:
        p[0] = Node('args', [p[1]])
        temp_list.append(str(p[1]))
    else:
        temp_list.append(str(p[3]))
        p[0] = p[1].add_children([p[3]])


def p_func_body(p):
    '''func_body :
                | func_body if
                | func_body call
                | func_body id
                | func_body assign
                | func_body while
                | func_body return'''
    if len(p) == 1:
        p[0] = Node('func_body', [])
    else:
        p[0] = p[1].add_children([p[2]])


def p_id(p):
    '''id : ID NAME ASSIGN expression END
          | ID NAME ASSIGN call'''
    temp_list.append(p[2])
    p[0] = Node('=', [p[2], p[4]])

def p_assign(p):
    '''assign : NAME ASSIGN expression END
              | NAME ASSIGN call'''
    flag = False
    for i in temp_list:
        if i == str(p[1]):
            flag = True
            break
    if flag:
        p[0] = Node('=', [p[1], p[3]])
    else:
        p_error(p)

def p_call(p):
    '''call : NAME LBR args RBR END
            | NAME LBR call_1 RBR END'''
    p[0] = Node('call func ' + p[1], [p[3]])

def p_call_1(p):
    '''call_1 : NAME LBR args RBR'''
    p[0] = Node('call func ' + p[1], [p[3]])


def p_if(p):
    '''if : IF LBR expression RBR LFB func_body RFB ELSE LFB func_body RFB'''
    if len(p) == 12:
        p[0] = Node('if', [p[3], p[6]])
        p[1] = Node('else', [p[10]])
        p[0] = p[0].add_children([p[1]])


def p_while(p):
    '''while : WHILE LBR expression RBR LFB func_body RFB
             | REPEAT LBR expression RBR LFB func_body RFB'''
    if p[1] == 'repeat':
        p[0] = str(p[6]) + '\n|__' + str(Node('while', [p[3], p[6]]))
    else:
        p[0] = Node('while', [p[3], p[6]])


def p_return(p):
    '''return : RETURN expression END'''
    p[2] = (str(p[2]).replace("\n", "\n\t"))
    p[0] = Node('return', str(p[2]))


def p_expression_plus_minus(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression'''
    p[0] = Node(p[2], [p[1], p[3]])


def p_expression_comp(p):
    '''expression : expression LT expression
                  | expression GT expression
                  | expression LE expression
                  | expression GE expression
                  | expression EQ expression
                  | expression NE expression'''
    p[0] = Node(p[2], [p[1], p[3]])

def p_expression_term(p):
    '''expression : term'''
    p[0] = p[1]

def p_term_times_div(p):
    '''term : term MULT term
            | term DIV term'''
    p[0] = Node(p[2], [p[1], p[3]])

def p_expression_con(p):
    '''expression : expression CON expression'''
    p[0] = Node(p[2], [p[1], p[3]])

def p_expression_dis(p):
    '''expression : expression DIS expression'''
    p[0] = Node(p[2], [p[1], p[3]])

def p_term_neg(p):
    '''expression : NEG term'''
    p[0] = Node(p[1], [p[2]])

def p_term_pow(p):
    '''factor : term POW expression'''
    p[0] = Node(p[2], [p[1], p[3]])

def p_term_factor(p):
    '''term : factor
            | NAME'''
    p[0] = p[1]

def p_factor_num(p):
    '''factor : NUM
              | call_1'''
    p[0] = p[1]


def p_factor_expr(p):
    'factor : LBR expression RBR'
    p[0] = p[2]

def p_error(p):
    print("Unexpected token:", p)
    print("Syntax error")
    raise SystemExit(2)

def build_tree():
    name = sys.argv[1]
    parser = yacc.yacc()
    if name.endswith(".txt"):
        try:
            with open(name, 'r') as text:
                result = text.read()
                result = str(parser.parse(result))
                with open(name + '.out', 'w') as write_file:
                    write_file.write(result)
        except FileNotFoundError:
            print('The file does not exist!')
    else:
        print("File opening error")

build_tree()
