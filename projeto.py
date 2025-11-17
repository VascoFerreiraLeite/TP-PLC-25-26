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


start = 'program'

def p_program(p):
    'program : PROGRAM ID PONTO_VIRGULA resto'
    print(f"Programa valido")

def p_resto(p):
    'resto : vars BEGIN codigo END PONTO'
    print("Resto valido")

def p_vars(p):
    '''vars : VAR var_list
            | empty'''
    print("Vars valido")

def p_var_list(p):
    '''var_list : var
                | var_list var'''

def p_var(p):
    'var : id_list DOIS_PONTOS tipo PONTO_VIRGULA'

def p_id_list(p):
    '''id_list : ID
               | id_list VIRGULA ID'''
    
def p_tipo(p):
    '''tipo : INTEGER
            | STRING
            | BOOLEAN'''
    
def p_codigo(p):
    '''codigo: comando_lista
             | comando_lista PONTO_VIRGULA codigo'''

def p_comando_lista(p):
    '''comando_lista : comando
                     | comando_atribuicao
                     | comando_while
                     | comando_for
                     | comando_if
                     | comando_readln
                     | comando_writeln
                     | comando_begin
                     | empty'''
    
def p_comando_atribuicao(p):
    'comando_atribuicao : ID ASSIGN expressao'

#falta mais tipo for e chamda de funcao
def p_expressao(p):
    '''expressao : termo
                 | expressao PLUS termo
                 | expressao MINUS termo
                 | expressao TIMES termo
                 | expressao DIVIDE termo
                 | expressao BOOLEAN'''

#NUM_REAL inutil? falta chamada de funcao
def p_termo(p):
    '''termo : NUM_INT
             | NUM_REAL 
             | ID
             | PARENT_A expressao PARENT_F'''


def p_comando_writeln(p):
    'comando_writeln : WRITELN PARENT_A LIT_STRING PARENT_F PONTO_VIRGULA' 

def p_comando_readln(p):
    'comando_readln : READLN PARENT_A ID PARENT_F PONTO_VIRGULA'

def p_comando_for(p):
    'comando_for : FOR ID ASSIGN expressao TO expressao DO comando_atribuicao'
    #falta downto






def p_empty(p):
    'empty :'
    pass
    
parser = yacc.yacc()

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

    