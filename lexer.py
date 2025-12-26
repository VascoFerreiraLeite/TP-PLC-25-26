import ply.lex as lex

# Palavras reservadas
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
    'or'       : 'OR',      # Adicionei OR pois tinhas no codeGen
    'downto'   : 'DOWNTO',
    'true'     : 'TRUE',
    'false'    : 'FALSE'
}

# Lista de Tokens
tokens = [
    'ID',     
    'NUM_INT',
    'NUM_REAL', 
    'LIT_STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQUAL', 'MENOR', 'MAIOR', 'MENOR_IGUAL', 'MAIOR_IGUAL',
    'VIRGULA', 'PONTO', 'PONTO_VIRGULA', 'DOIS_PONTOS',
    'ASSIGN', 
    'PARENT_A', 'PARENT_F', 
    'LBRACKET', 'RBRACKET', # Usar estes para [ ]
    'DOTDOT',
    'APOST' # Normalmente nao é token isolado, mas se a tua gramatica usa, mantem
] + list(reserved.values())

# Regras de Expressões Regulares para tokens simples
# NOTA: O PLY ordena strings por tamanho (maiores primeiro), 
# por isso := ganha a : e .. ganha a . automaticamente.

t_VIRGULA       = r','
t_PONTO_VIRGULA = r';'
t_ASSIGN        = r':='
t_DOIS_PONTOS   = r':'
t_PARENT_A      = r'\('
t_PARENT_F      = r'\)'
t_LBRACKET      = r'\['  # Substitui PARENT_Q_A
t_RBRACKET      = r'\]'  # Substitui PARENT_Q_F
t_PLUS          = r'\+'
t_MINUS         = r'-'
t_TIMES         = r'\*'
t_DIVIDE        = r'/'
t_EQUAL         = r'='
t_MENOR_IGUAL   = r'<='
t_MAIOR_IGUAL   = r'>='
t_MENOR         = r'<'
t_MAIOR         = r'>'
t_APOST         = r'\''
t_DOTDOT        = r'\.\.' # Substitui PONTO se vier seguido
t_PONTO         = r'\.'

# Ignorar espaços e tabs
t_ignore  = ' \t'

# Regra para ID (Identificadores e Palavras Reservadas)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Verifica se é palavra reservada (case-insensitive)
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

# Regra para Strings (remove as plicas)
def t_LIT_STRING(t):
    r"'.*?'" 
    t.value = t.value[1:-1]
    return t

# Regra para Reais (deve vir antes de INT)
def t_NUM_REAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Regra para Inteiros
def t_NUM_INT(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Contagem de linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Tratamento de erros
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# Inicializa o lexer
lexer = lex.lex()