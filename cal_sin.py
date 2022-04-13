# gramática
'''
Z -> Comandos

Comandos -> Comandos Comando
          | Comando

Comando -> ID '=' '(' NUM ',' NUM ',' NUM ',' NUM ')'
         | DIA '-''>' Lista
         | '?' DIA
         | '?' Lista

Lista -> '[' Lista2

Lista2 -> ']'
        | LCont ']'

LCont -> Cont LCont2

LCont2 -> ',' LCont
        |

Cont -> ID
      | NUM '*' ID
      | ID '*' NUM
'''

import ply.yacc as yacc
from cal_lex import tokens, literals

# definição das regras de produção
def p_Z(p):
    "Z : Comandos"

def p_Comandos_Lista(p):
    "Comandos : Comandos Comando"

def p_Comandos_Simples(p):
    "Comandos : Comando"

def p_Comando_CREATEFOOD(p):
    "Comando : ID '=' '(' NUM ',' NUM ',' NUM ',' NUM ')'"
    p.parser.food[p[1]] = (p[4], p[6], p[8], p[10])

def p_Comando_ATRIBDAY(p):
    "Comando : DIA '-' '>' Lista"
    p.parser.days[p[1]] = p[4]

def p_Comando_VALUEDAY(p):
    "Comando : '?' DIA"
    if p[2] in p.parser.days:
        print('\nDados referentes ao dia ' + p[2] + ': ', end='\n')
        kcal = fat = hydro = prot = 0
        for food in p.parser.days[p[2]]:
            if food[0] in p.parser.food:
                kcal += p.parser.food[food[0]][0] * food[1]
                fat += p.parser.food[food[0]][1] * food[1]
                hydro += p.parser.food[food[0]][2] * food[1]
                prot += p.parser.food[food[0]][3] * food[1]
            else:
                print('Aviso: Não há qualquer informação nutricional sobre ' + food[0], end='\n')
        print('\n' + 'kcal: ' + '{:.2f}'.format(kcal))
        print('lípidos: ' + '{:.2f}'.format(fat))
        print('hidratos de carbono: ' + '{:.2f}'.format(hydro))
        print('proteína: ' + '{:.2f}'.format(prot), end='\n\n\n')
    else:
        print('Não há qualquer informação sobre esse dia. :(\n\n')

def p_Comando_VALUELIST(p):
    "Comando : '?' Lista"
    kcal = fat = hydro = prot = 0
    for food in p[2]:
        if food[0] in p.parser.food:
            kcal += p.parser.food[food[0]][0] * food[1]
            fat += p.parser.food[food[0]][1] * food[1]
            hydro += p.parser.food[food[0]][2] * food[1]
            prot += p.parser.food[food[0]][3] * food[1]
        else:
            print('Aviso: Não há qualquer informação nutricional sobre ' + food[0], end='\n')
    print('\n' + 'kcal: ' + '{:.2f}'.format(kcal))
    print('lípidos: ' + '{:.2f}'.format(fat))
    print('hidratos de carbono: ' + '{:.2f}'.format(hydro))
    print('proteína: ' + '{:.2f}'.format(prot), end='\n\n\n')

def p_Lista(p):
    "Lista : '[' Lista2"
    p[0] = p[2]

def p_Lista2_empty(p):
    "Lista2 : ']'"
    p[0] = []

def p_Lista2_cont(p):
    "Lista2 : LCont ']'"
    p[0] = p[1]

def p_LCont(p):
    "LCont : Cont LCont2"
    p[0] = [p[1]] + p[2]

def p_LCont2_cont(p):
    "LCont2 : ',' LCont"
    p[0] = p[2]

def p_LCont2_empty(p):
    "LCont2 : "
    p[0] = []

def p_Cont_ID(p):
    "Cont : ID"
    p[0] = (p[1], 1)

def p_Cont_Mult(p):
    "Cont : ID '*' NUM"
    p[0] = (p[1], p[3])

def p_Cont_MultRev(p):
    "Cont : NUM '*' ID"
    p[0] = (p[3], p[1])

def p_error(p):
    print('Erro Sintático: ', p, end='\n')
    print()
    parser.success = False

parser = yacc.yacc()
parser.food = {}
parser.days = {}

# ler input de um ficheiro indicado como argumento
import sys
if len(sys.argv) != 1:
    file = open(sys.argv[1], "r")
    for linha in file:
        parser.success = True
        if linha != '\n':
            parser.parse(linha)

# apresentação da "Base de Dados"
def printSortedList(l):
    newSorted = sorted(l)
    for i in range(0, len(newSorted)):
        print(str(i + 1) + ": " + newSorted[i])

print('Alimentos na "Base de Dados":\n')
printSortedList(parser.food.keys())
print()

# recebe input do utilizador
print('Inserir comando: ')
for linha in sys.stdin:
    parser.success = True
    if linha != '\n':
        parser.parse(linha)
    print('Inserir comando: ')

if len(sys.argv) != 1:
    file.close()