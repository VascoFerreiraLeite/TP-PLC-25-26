import ply.yacc as yacc
from lexer import tokens

precedence = (
    ('left', 'AND', 'OR'),
    ('nonassoc', 'EQUAL', 'MENOR_IGUAL', 'MAIOR', 'MENOR', 'MAIOR_IGUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'DIV', 'MOD'),
)

start = 'program'

def p_program(p):
    'program : PROGRAM ID PONTO_VIRGULA resto'
    p[0]=('PROGRAM', p[2], p[4])
    print(f"Programa valido")

def p_resto(p):
    'resto : vars funcoes vars BEGIN codigo END PONTO'
    v1=p[1] if p[1] else []
    v2=p[3] if p[3] else []
    tudo=v1+v2
    p[0]=('RESTO', tudo, p[2], p[5])
    print("Resto valido")

def p_vars(p):
    '''vars : VAR var_list
            | empty'''
    print("Vars valido")
    if len(p)>2:
        p[0]=p[2]
    else:
        p[0]=[]

def p_var_list(p):
    '''var_list : var
                | var_list var'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_var(p):
    'var : id_list DOIS_PONTOS tipo PONTO_VIRGULA'
    p[0] = ('VARS', p[1], p[3])

def p_id_list(p):
    '''id_list : ID
            | id_list VIRGULA ID'''
    if len(p) == 2:
        p[0]=[p[1]] 
    else:
        p[0]=p[1] + [p[3]]

def p_funcoes(p):
    '''funcoes : funcoes funcao
               | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_funcao(p):
    'funcao : FUNCTION ID PARENT_A argumentos_decl PARENT_F DOIS_PONTOS tipo PONTO_VIRGULA vars BEGIN codigo END PONTO_VIRGULA'
    p[0] = ('DEF_FUNCTION', p[2], p[4], p[7], p[9], p[11])

def p_argumentos_decl(p):
    '''argumentos_decl : id_list DOIS_PONTOS tipo
                       | argumentos_decl PONTO_VIRGULA id_list DOIS_PONTOS tipo
                       | empty'''
    if len(p) == 4:
        p[0] = [('ARG', p[1], p[3])]
    elif len(p) == 6:
        p[0] = p[1] + [('ARG', p[3], p[5])]
    else:
        p[0] = []
        
def p_tipo(p):
    '''tipo : INTEGER
            | STRING
            | BOOLEAN
            | tipo_array'''
    if isinstance(p[1], str):
        p[0]=p[1].upper()
    else:
        p[0]=p[1]

def p_tipo_array(p):
    'tipo_array : ARRAY LBRACKET NUM_INT DOTDOT NUM_INT RBRACKET OF tipo'
    p[0] = ('ARRAY', p[3], p[5], p[8])

def p_codigo(p):
    '''codigo : comando_lista
            | codigo PONTO_VIRGULA comando_lista'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]+[p[3]]

def p_comando_lista(p):
    '''comando_lista : comando_assign
                    | comando_while
                    | comando_for
                    | comando_if
                    | comando_writeln
                    | comando_readln
                    | comando_begin
                    | empty'''
    p[0] = p[1]
    
def p_comando_assign(p):
    '''comando_assign : ID ASSIGN expressao
                      | ID LBRACKET expressao RBRACKET ASSIGN expressao'''
    if len(p) == 4:
        p[0] = ('ASSIGN', p[1], p[3])
    else:
        p[0] = ('ASSIGN_ARRAY', p[1], p[3], p[6])

def p_while(p):
    'comando_while : WHILE expressao DO comando_lista'
    p[0] = ('WHILE', p[2], p[4])

def p_comando_for(p):
    '''comando_for : FOR ID ASSIGN expressao TO expressao DO comando_lista
                   | FOR ID ASSIGN expressao DOWNTO expressao DO comando_lista'''
    p[0] = ('FOR', p[2], p[4], p[5], p[6], p[8])


def p_if(p):
    '''comando_if : IF expressao THEN comando_lista
                  | IF expressao THEN comando_lista ELSE comando_lista'''
    if len(p) == 5:
        p[0] = ('IF', p[2], p[4])
    else:
        p[0] = ('IF_ELSE', p[2], p[4], p[6])
    
def p_comando_writeln(p):
    'comando_writeln : WRITELN PARENT_A argumentos PARENT_F' 
    p[0] = ('WRITELN', p[3])

def p_comando_readln(p):
    'comando_readln : READLN PARENT_A expressao PARENT_F'
    p[0] = ('READLN', p[3])

def p_begin(p):
    'comando_begin : BEGIN codigo END'
    p[0] = p[2]

def p_expressao(p):
    '''expressao : termo
                 | expressao PLUS termo
                 | expressao MINUS termo
                 | expressao TIMES termo
                 | expressao DIVIDE termo
                 | expressao DIV termo
                 | expressao MOD termo
                 | expressao AND expressao
                 | expressao OR expressao
                 | expressao EQUAL expressao
                 | expressao MENOR expressao
                 | expressao MAIOR expressao
                 | expressao MENOR_IGUAL expressao
                 | expressao MAIOR_IGUAL expressao'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('CONTA', p[2], p[1], p[3])

def p_termo(p):
    '''termo : NUM_INT
            | NUM_REAL 
            | ID
            | LIT_STRING
            | TRUE
            | FALSE
            | PARENT_A expressao PARENT_F
            | ID LBRACKET expressao RBRACKET
            | ID PARENT_A argumentos PARENT_F'''
    if len(p)==2:
        tipo_t=p.slice[1].type

        if tipo_t== 'NUM_INT':
            p[0] = ('NUM', p[1])
        elif tipo_t== 'NUM_REAL':
            p[0] = ('REAL', p[1])
        elif tipo_t== 'ID':
            p[0] = ('VAR', p[1])
        elif tipo_t== 'LIT_STRING':
            p[0] = ('STR', p[1])
        elif tipo_t=='TRUE':
            p[0] = ('TRUE', 1)
        elif tipo_t=='FALSE':
            p[0] = ('FALSE', 0)
    elif len(p)==4:
        p[0]=p[2]
    elif len(p)==5:
        if p.slice[2].type == "LBRACKET":
            p[0]=('ARRAY', p[1], p[3])
        else:
            p[0]=('CALL', p[1], p[3])

def p_argumentos(p):
    '''argumentos : expressao
                | argumentos VIRGULA expressao'''
    if len(p) == 2:
        p[0] = [p[1]]  
    else: 
        p[0] = p[1] + [p[3]]

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Erro de sintaxe: '{p.value}' na linha {p.lineno}")
    else:
        print("Erro de sintaxe: Fim inesperado do ficheiro")
    
parser = yacc.yacc()