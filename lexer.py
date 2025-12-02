import ply.lex as lex

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