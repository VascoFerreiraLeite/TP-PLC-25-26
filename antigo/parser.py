import ply.yacc as yacc
from lexer import tokens

# --- Precedência ---
precedence = (
    ('left', 'AND', 'OR'),                # Adicionei OR caso uses
    ('nonassoc', 'EQUAL', 'MENOR_IGUAL', 'MAIOR', 'MENOR', 'MAIOR_IGUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'DIV', 'MOD'),
)

start = 'program'

# --- Regras da Gramática ---

def p_program(p):
    'program : PROGRAM ID PONTO_VIRGULA resto'
    p[0] = ('PROGRAM', p[2], p[4])
    print(f"Programa valido")

def p_resto(p):
    '''resto : vars funcoes vars BEGIN codigo END PONTO'''
    # Agora aceitamos vars antes (p[1]) e depois (p[3]) das funções
    
    # 1. Juntar as listas de variáveis (pode haver vars no inicio e no fim)
    vars1 = p[1] if p[1] else []
    vars2 = p[3] if p[3] else []
    todas_vars = vars1 + vars2
    
    # 2. Manter a estrutura que o resto do programa espera: 
    # ('RESTO', todas_as_vars, funcoes, codigo)
    p[0] = ('RESTO', todas_vars, p[2], p[5])
    
    print("Resto valido")

def p_vars(p):
    '''vars : VAR var_list
            | empty'''
    print("Vars valido")
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = []

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
        p[0] = [p[1]] 
    else:
        p[0] = p[1] + [p[3]]

# --- Funções ---

def p_funcoes(p):
    '''funcoes : funcoes funcao
               | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_funcao(p):
    # function Nome(args) : Tipo; vars begin ... end;
    'funcao : FUNCTION ID PARENT_A args_decl PARENT_F DOIS_PONTOS tipo PONTO_VIRGULA vars BEGIN codigo END PONTO_VIRGULA'
    # Guardamos: ('DEF_FUNCTION', nome, args, tipo_retorno, vars_locais, corpo)
    p[0] = ('DEF_FUNCTION', p[2], p[4], p[7], p[9], p[11])

def p_args_decl(p):
    '''args_decl : args_decl_lista
                 | empty'''
    p[0] = p[1] if p[1] is not None else []

def p_args_decl_lista(p):
    '''args_decl_lista : id_list DOIS_PONTOS tipo
                       | args_decl_lista PONTO_VIRGULA id_list DOIS_PONTOS tipo'''
    # Esta lógica é chata: agrupar (v1, v2 : int)
    if len(p) == 4:
        # Caso base: v1, v2 : tipo
        lista_ids = p[1]
        tipo = p[3]
        args = []
        for nome in lista_ids:
            args.append((nome, tipo))
        p[0] = args
    else:
        # Caso recursivo: ... ; v3 : tipo
        lista_ids = p[3]
        tipo = p[5]
        args = p[1]
        for nome in lista_ids:
            args.append((nome, tipo))
        p[0] = args
    
# --- Tipos (Simples e Arrays) ---

def p_tipo_simples(p):
    '''tipo : INTEGER
            | STRING
            | BOOLEAN'''
    p[0] = {'cat': 'simple', 'type': p[1]}

def p_tipo_array(p):
    '''tipo : ARRAY LBRACKET NUM_INT DOTDOT NUM_INT RBRACKET OF tipo''' 
    p[0] = {'cat': 'array', 'min': int(p[3]), 'max': int(p[5]), 'type': p[8]}

# --- Comandos e Código ---

def p_codigo(p):
    '''codigo : comando_lista
              | codigo PONTO_VIRGULA comando_lista'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_comando_lista(p):
    '''comando_lista : comando_assign
                     | comando_assign_array
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

def p_comando_assign_array(p):
    'comando_assign_array : ID LBRACKET expressao RBRACKET ASSIGN expressao'
    p[0] = ('ASSIGN_ARRAY', p[1], p[3], p[6])

def p_while(p):
    'comando_while : WHILE expressao DO comando_lista'
    p[0] = ('WHILE', p[2], p[4])

def p_comando_for(p):
    '''comando_for : FOR ID ASSIGN expressao TO expressao DO comando_lista
                   | FOR ID ASSIGN expressao DOWNTO expressao DO comando_lista'''
    # p[5] diz-nos se é 'to' ou 'downto'
    p[0] = ('FOR', p[2], p[4], p[6], p[8], p[5])

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
    '''comando_readln : READLN PARENT_A variavel PARENT_F''' 
    # CORREÇÃO: mudei 'comando' para 'comando_readln' para bater certo com p_comando_lista
    p[0] = ('READLN', p[3])

def p_begin(p):
    'comando_begin : BEGIN codigo END'
    p[0] = p[2]

# --- Variáveis e Expressões ---

def p_variavel(p):
    '''variavel : ID
                | ID LBRACKET expressao RBRACKET'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('ARRAY_ACCESS', p[1], p[3])

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
                 | expressao MENOR_IGUAL expressao
                 | expressao MAIOR_IGUAL expressao
                 | expressao MENOR expressao
                 | expressao MAIOR expressao'''
    # CORREÇÃO: Removi '| expressao BOOL' (BOOL é um termo, não um operador)
    if len(p) > 2:
        p[0] = ('CONTA', p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_termo(p):
    '''termo : NUM_INT
             | NUM_REAL 
             | ID
             | LIT_STRING
             | TRUE
             | FALSE
             | PARENT_A expressao PARENT_F
             | termo_array_access 
             | ID PARENT_A argumentos PARENT_F'''
             # Adicionei explicitamente o array access como termo
    
    if len(p) == 2:
        # Lógica para determinar o tipo baseada no token
        # Nota: O p.slice depende da implementação do PLY, mas geralmente funciona.
        tipo_token = p.slice[1].type
        
        if tipo_token == 'NUM_INT':
            p[0] = ('NUM', p[1])
        elif tipo_token == 'NUM_REAL':
            p[0] = ('REAL', p[1])
        elif tipo_token == 'ID':
            p[0] = ('VAR', p[1])
        elif tipo_token == 'LIT_STRING':
            p[0] = ('STR', p[1])
        elif tipo_token == 'TRUE':
            p[0] = ('TRUE', 1)
        elif tipo_token == 'FALSE':
            p[0] = ('FALSE', 0)
        # Se for termo_array_access (definido abaixo), p[1] já vem processado
        else:
            p[0] = p[1] 
    elif len(p) == 4: # ( expressao )
        p[0] = p[2]

    elif len(p) == 5: # ID ( argumentos ) -> Chamada de função
        p[0] = ('CALL', p[1], p[3])

def p_termo_array_access(p):
    '''termo_array_access : ID LBRACKET expressao RBRACKET'''
    p[0] = ('ARRAY_ACCESS', p[1], p[3])

def p_argumentos(p):
    '''argumentos : expressao
                  | argumentos VIRGULA expressao'''
    if len(p) == 2:
        p[0] = [p[1]]  
    else: 
        p[0] = p[1] + [p[3]]

# --- Empty e Error ---

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Erro de sintaxe: '{p.value}' na linha {p.lineno}")
    else:
        print("Erro de sintaxe: Fim inesperado do ficheiro")
    
parser = yacc.yacc()