import ply.lex as lex

tokens = (
    'PROGRAM',
    'VAR',
    'BEGIN',
    'END',
    'IF',
    'THEN',
    'ELSE',
    'FOR',
    'DO',
    'AND',
    'VIRGULA',
    'PONTO',
    'PONTO_VIRGULA',
    'ASSIGN',
    'DOIS_PONTOS',
    'PARENT_A',
    'PARENT_F',
    'ID',     
    'NUM_INT',
    'NUM_REAL', 
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
)

t_PROGRAM       = r'PROGRAM'
t_VAR           = r'VAR' 
t_BEGIN         = r'BEGIN'
t_END           = r'END'
t_IF            = r'IF'
t_THEN          = r'THEN'
t_ELSE          = r'ELSE'
t_FOR           = r'FOR'
t_DO            = r'DO'
t_AND           = r'AND'
t_VIRGULA       = r','
t_PONTO         = r'\.'
t_PONTO_VIRGULA = r';'
t_ASSIGN        = r':='
t_DOIS_PONTOS   = r':'
t_PARENT_A      = r'\('
t_PARENT_F      = r'\)'
t_PLUS          = r'\+'
t_MINUS         = r'-'
t_TIMES         = r'\*'
t_DIVIDE        = r'/'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
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

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)