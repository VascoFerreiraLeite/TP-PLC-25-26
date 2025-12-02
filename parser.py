import ply.yacc as yacc
from lexer import tokens

#YACC

precedence = (
    ('left', 'AND'),                      # Para o ... and primo
    ('nonassoc', 'EQUAL', 'MENOR_IGUAL'), # Para o = e <=
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'DIV', 'MOD'),
)

start = 'program'

def p_program(p):
    'program : PROGRAM ID PONTO_VIRGULA resto'
    p[0] = ('PROGRAM', p[2], p[4])
    print(f"Programa valido")

def p_resto(p):
    'resto : vars BEGIN codigo END PONTO'
    print("Resto valido")
    
    p[0] = ('RESTO', p[1], p[3])

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
    
def p_tipo(p):
    '''tipo : INTEGER
            | STRING
            | BOOLEAN'''
    p[0] = p[1]
    
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
    'comando_assign : ID ASSIGN expressao'
    p[0] = ('ASSIGN', p[1], p[3])

def p_while(p):
    'comando_while : WHILE expressao DO comando_lista'
    p[0] = ('WHILE', p[2], p[4])

def p_comando_for(p):
    'comando_for : FOR ID ASSIGN expressao TO expressao DO comando_lista'
    p[0] = ('FOR', p[2], p[4], p[6], p[8])
    #falta downto

def p_if(p):
    '''comando_if : IF expressao THEN comando_lista
                  | IF expressao THEN comando_lista ELSE comando_lista'''
    if len(p) == 5:
        p[0] = ('IF', p[2], p[4])
    else:
        p[0] = ('IF_ELSE', p[2], p[4], p[6]) # NOVO: Tuplo diferente para quando tem Else
    
def p_comando_writeln(p):
    'comando_writeln : WRITELN PARENT_A argumentos PARENT_F' 
    p[0] = ('WRITELN', p[3])

def p_comando_readln(p):
    'comando_readln : READLN PARENT_A ID PARENT_F'
    p[0] = ('READLN', p[3])

def p_begin(p):
    'comando_begin : BEGIN codigo END'
    p[0] = p[2]


#falta mais tipo for e chamda de funcao
def p_expressao(p):
    '''expressao : termo
                | expressao PLUS termo
                | expressao MINUS termo
                | expressao TIMES termo
                | expressao DIVIDE termo
                | expressao DIV termo           
                | expressao MOD termo           
                | expressao AND expressao       
                | expressao EQUAL expressao     
                | expressao MENOR_IGUAL expressao
                | expressao BOOL'''
    # Nota: mudei termo para expressao nas novas regras para permitir recursividade correta
    if len(p)>2:
        p[0] = ('CONTA', p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_BOOL(p):
    '''BOOL : TRUE
            | FALSE'''  
    p[0] = p[1]

#NUM_REAL inutil? falta chamada de funcao
def p_termo(p):
    '''termo : NUM_INT
            | NUM_REAL 
            | ID
            | LIT_STRING
            | TRUE
            | FALSE
            | PARENT_A expressao PARENT_F'''
    if len(p)>2:
        p[0]=p[2]
    else:

        # Verifica o tipo do token que foi encontrado
        tipo_token = p.slice[1].type

        if p.slice[1].type == 'NUM_INT':
            p[0] = ('NUM', p[1])
        elif p.slice[1].type == 'NUM_REAL':
            p[0] = ('REAL', p[1])
        elif p.slice[1].type == 'ID':
            p[0] = ('VAR', p[1]) # Importante para ir buscar à tabela
        elif p.slice[1].type == 'LIT_STRING':
            p[0] = ('STR', p[1])
        elif tipo_token == 'TRUE':
            p[0] = ('TRUE', 1)  # Guardamos como 1
        elif tipo_token == 'FALSE':
            p[0] = ('FALSE', 0) # Guardamos como 0

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