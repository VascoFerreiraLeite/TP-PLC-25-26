import ply.lex as lex
import ply.yacc as yacc

#INCOMPLETO AINDA
tokens = (
    'PROGRAM',
    'VAR',
    'BEGIN',
    'END',
    'IF',
    'THEN',
    'ELSE',
    'FOR',
    'TO',
    'DO',
    'WHILE',
    'WRITELN',
    'READLN',
    'INTEGER',
    'BOOLEAN',
    'STRING',
    'ARRAY',
    'OF',
    'FUNCTION',
    'DIV',
    'MOD',
    'AND',
    'DOWNTO',
    'TRUE',
    'FALSE',
    'VIRGULA',
    'PONTO',
    'PONTO_VIRGULA',
    'ASSIGN',
    'DOIS_PONTOS',
    'PARENT_A',
    'PARENT_F',
    'PARENT_Q_A',
    'PARENT_Q_F',
    'ID',     
    'NUM_INT',
    'NUM_REAL', #inutil?
    'LIT_STRING',
    'PLUS',
    'MINUS',
    'EQUAL', 
    'MENOR', 
    'MAIOR', 
    'MENOR_IGUAL', 
    'MAIOR_IGUAL',
    'TIMES',
    'DIVIDE',
    'APOST',
)

reserved = {
    'program'  : 'PROGRAM',
    'var'      : 'VAR',
    'begin'    : 'BEGIN',
    'end'      : 'END',
    'if'       : 'IF',
    'then'     : 'THEN',
    'else'     : 'ELSE',
    'for'      : 'FOR',
    'to'       : 'TO',
    'do'       : 'DO',
    'while'    : 'WHILE',
    'writeln'  : 'WRITELN',
    'readln'   : 'READLN',
    'integer'  : 'INTEGER',
    'boolean'  : 'BOOLEAN',
    'string'   : 'STRING',
    'array'    : 'ARRAY',
    'of'       : 'OF',
    'function' : 'FUNCTION',
    'div'      : 'DIV',
    'mod'      : 'MOD',
    'and'      : 'AND',
    'downto'   : 'DOWNTO',
    'true'     : 'TRUE',
    'false'    : 'FALSE',
}

t_VIRGULA = r','
t_PONTO = r'\.'
t_PONTO_VIRGULA = r';'
t_ASSIGN = r':='
t_DOIS_PONTOS = r':'
t_PARENT_A = r'\('
t_PARENT_F = r'\)'
t_PARENT_Q_A = r'\['
t_PARENT_Q_F = r'\]'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUAL = r'='
t_MENOR = r'<'
t_MAIOR = r'>'
t_MENOR_IGUAL = r'<='
t_MAIOR_IGUAL = r'>='
t_APOST = r'\''

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

def t_LIT_STRING(t):
    r"'.*?'" 
    t.value = t.value[1:-1]
    return t

def t_NUM_REAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUM_INT(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

#YACC

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

start = 'program'

def p_program(p):
    'program : PROGRAM ID PONTO_VIRGULA resto'
    p[0] = ('PROGRAM', p[2], p[4])
    print(f"Programa valido")

def p_resto(p):
    'resto : vars BEGIN codigo END PONTO'
    print("Resto valido")
    
    p[0] = p[2]

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
        p[0]=p[1] 
    else:
        p[0]=p[1] + [p[3]]
    
def p_tipo(p):
    '''tipo : INTEGER
            | STRING
            | BOOLEAN'''
    p[0] = p[1]
    
def p_codigo(p):
    '''codigo: comando_lista
             | codigo PONTO_VIRGULA comando_lista'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]+[p[3]]

def p_comando_lista(p):
    '''comando_lista : comando_atribuicao
                     | comando_while
                     | comando_for
                     | comando_if
                     | comando_writeln
                     | comando_readln
                     | comando_begin
                     | empty'''
    p[0] = p[1]
    
def p_comando_atribuicao(p):
    'comando_atribuicao : ID ASSIGN expressao'
    p[0] = ('ASSIGN', p[1], p[3])

def p_while(p):
    'comando_while : WHILE expressao DO comando_lista'
    p[0] = ('WHILE', p[2], p[4])

def p_comando_for(p):
    'comando_for : FOR ID ASSIGN expressao TO expressao DO comando_lista'
    p[0] = ('FOR', p[2], p[4], p[6], p[8])
    #falta downto

def p_if(p):
    '''comando_if : IF expressao THEN comando_lista'''
    p[0] = ('IF', p[2], p[4])
    
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
                 | expressao BOOL'''
    p[0] = ('CONTA', p[2], p[1], p[3])

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
             | PARENT_A expressao PARENT_F'''
    if p[1]=='(':
        p[0]=p[2]
    else:
        p[0] = p[1]

def p_argumentos(p):
    '''argumentos : expressao
                  | argumentos VIRGULA expressao'''
    if len(p) == 2:
        p[0] = [p[1]]  
    else: 
        p[1] + [p[3]]



def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Erro de sintaxe: '{p.value}' na linha {p.lineno}")
    else:
        print("Erro de sintaxe: Fim inesperado do ficheiro")
    
parser = yacc.yacc()

#------------------------------------
#-- Analisador Semântico (incompleto) ---

tabela={}


def analisador_semantico():
    #talvez tirar
    if not isinstance(nodo, tuple):
        return

    if isinstance(nodo, list):
        for n in nodo:
            anasalisador_semantico(n)
        return
    
    caixa=nodo[0]

    if caixa=='PROGRAM':
        analisador_semantico(nodo[2])

    elif caixa=='VARS':
        vars_lista=nodo[1]
        tipo=nodo[2]
        for var in vars_lista:
            if var in tabela:
                print(f"Erro semântico: variável '{var}' já declarada.")
        else:
            tabela[var]=tipo
            #debug tirar dps
            print(f"Variável '{var}' declarada como '{tipo}'.")

    elif caixa=='ASSIGN':
        var=nodo[1]
        expressao=nodo[2]
        if var not in tabela:
            print(f"Erro semântico: variável '{var}' não declarada.")
        else:
            analisador_semantico(expressao)










#--
def percorre(p):
    etiqueta=p[0]
    #if etiqueta=='PROGRAM':
    if etiqueta=='VARS':
        ids=p[1]
        tipo=p[3]
        if isinstance(ids, list):
            for id in ids:
                tabela[id]=tipo
        else:
            tabela[ids]=tipo





if __name__ == '__main__':
    #codigo teste
    pascal_code = """
program Fatorial;
var
 n, i, fat: integer;
begin
 writeln('Introduza um número inteiro positivo:');
 readln(n);
 fat := 1;
 for i := 1 to n do
 fat := fat * i;
 writeln('Fatorial de ', n, ': ', fat);
end.
"""

    lexer.input(pascal_code)
    parser.parse(pascal_code, lexer=lexer)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

    