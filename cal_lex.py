'''
banana = (40, 10, 5, 4)
12/5/2022 -> [banana, arroz]
?12/5/2022
?[banana, arroz]
'''

import ply.lex as lex

literals = ['=', '(', ')', '-', '>', '/', '[', ']', '?', ',', '*']
tokens = ['ID', 'NUM', 'DIA']

t_ID = r'[A-Za-z][A-Za-z_]*'

def t_DIA(t):
    r'\d+\/\d+\/\d+'
    return t

def t_NUM(t):
    r'\d+(.\d+)?'
    t.value = float(t.value)
    return t

t_ignore = " \t\n"

def t_error(t):
    print('Carácter ilegal: ', t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()