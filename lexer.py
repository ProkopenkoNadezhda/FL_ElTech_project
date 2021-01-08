import ply.lex as lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'func': 'FUNC',
    'return': 'RETURN',
    'while': 'WHILE',
    'repeat': 'REPEAT',
    'id': 'ID'
}

tokens = [
    'NUM',
    'PLUS', # +
    'POW',  # **
    'MULT', # *
    'MINUS',    # -
    'DIV',  # /
    'NAME',
    'DIS',  # ||
    'CON',  # &&
    'NEG',  # --
    'COMMA',   # ,
    'LBR',  # (
    'LFB',     # {
    'RFB',  # }
    'RBR',   # )
    'ASSIGN',   # =
    'END',    # ;
    'LT',   # <
    'GT',   # >
    'LE',   # <=
    'GE',   # >=
    'EQ',   # ==
    'NE'    # /=
] + list(reserved.values())


precedence = (
    ('right', 'DIS'),
    ('right', 'CON'),
    ('nonassoc', 'NEG'),
    ('nonassoc', 'LT', 'GT', 'LE', 'GE', 'EQ', 'NE' ),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
    ('right', 'POW'),
)


def t_NAME(t):
    r'[A-z_][a-z_0-9]*'
    t.type = reserved.get(str(t.value), 'NAME')
    return t


def t_NUM(t):
    r'[0-9]+'
    if len(t.value) > 1:
        if str(t.value)[0]:
            print()
            t_error(t)
    t.value = int(t.value)
    return t


t_PLUS = r'\+'
t_MULT = r'\*'
t_LBR = r'\('
t_RBR = r'\)'
t_LFB = r'\{'
t_RFB = r'\}'
t_MINUS = r'\-'
t_POW = r'\*\*'  # **
t_DIV = r'/'
t_DIS = r'\|\|'  # ||
t_CON = r'&&'
t_NEG = r'\-\-'  # --
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'/='
t_ASSIGN = r'='
t_END = r';'
t_COMMA = r','

t_ignore = ' \t\n'

def t_error(t):
    print("Illegal character '%s'" % t.value)
    raise SystemExit(1)


lexer = lex.lex()