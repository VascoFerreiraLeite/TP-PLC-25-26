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



#------------------------------------
#-- Obter tipos (incompleto) ---


def obter_tipo(nodo):
    #if isinstance(nodo, int):
        #return 'INTEGER'
    #if isinstance(nodo, str):
        #return 'STRING'
    #if isinstance(nodo, float):
        #return 'REAL'
    #if nodo == 'true' or nodo == 'false':
        #return 'BOOLEAN'

    caixa=nodo[0]

    if caixa=='NUM':
        return 'INTEGER'
    if caixa=='REAL':
        return 'REAL'
    if caixa=='STR':
        return 'STRING'
    if caixa == 'TRUE' or caixa == 'FALSE': 
        return 'BOOLEAN'

    if caixa=='VAR':
        var=nodo[1]
        if var in tabela:
            return tabela[var].upper()
        else:
            #debug
            print(f"Erro semântico: variável '{var}' não declarada.")
            return None

    if caixa=='CONTA':
        op = nodo[1]
        tipo_esq=obter_tipo(nodo[2])
        tipo_dir=obter_tipo(nodo[3])

        # Operadores Lógicos/Comparação retornam sempre BOOLEAN
        if op in ['=', '<', '>', '<=', '>=', 'and']:
            return 'BOOLEAN'
        
        if tipo_esq=='INTEGER' and tipo_dir=='INTEGER':
            return 'INTEGER'
        else:
            print(f"Erro semântico: tipos diferentes esq: '{tipo_esq}', dir: '{tipo_dir}'")
            return None


#------------------------------------
#-- Analisador Semântico (incompleto) ---

tabela={}

def analisador_semantico(nodo):
    #talvez tirar

    if nodo is None:
        return
    if isinstance(nodo, list):
        for n in nodo:
            analisador_semantico(n)
        return
    if not isinstance(nodo, tuple):
        return
    
    caixa=nodo[0]

    if caixa=='PROGRAM':
        analisador_semantico(nodo[2])

    elif caixa=='VARS':
        vars_lista=nodo[1]
        tipo=nodo[2].upper()
        for var in vars_lista:
            if var in tabela:
                print(f"Erro semântico: variável '{var}' já declarada.")
            else:
                tabela[var]=tipo
                #debug tirar dps
                print(f"Variável '{var}' declarada como '{tipo}'.")

    elif caixa=='RESTO':
        analisador_semantico(nodo[1])  #vars
        analisador_semantico(nodo[2])  #codigo

    elif caixa=='ASSIGN':
        var=nodo[1]
        expressao=nodo[2]
        if var not in tabela:
            print(f"Erro semântico: variável '{var}' não declarada.")
        else:
            tipo_var=tabela[var].upper()
            tipo_obtido=obter_tipo(expressao)
            if tipo_var != tipo_obtido:
                print(f"Erro semântico: tipo esperado diferente do obtido, esperado: '{tipo_var}', obtido: '{tipo_obtido}'")
            else:
                #debug
                print(f"(ASSIGN)Atribuição válida à variável '{var}' do tipo '{tipo_var}'.")
            analisador_semantico(expressao)
        
    elif caixa=='CONTA':
        analisador_semantico(nodo[2])
        analisador_semantico(nodo[3])
    
    elif caixa=='WHILE':
        analisador_semantico(nodo[1])
        analisador_semantico(nodo[2])
    
    elif caixa=='FOR':
        var=nodo[1]
        inicio=nodo[2]
        fim=nodo[3]
        if var not in tabela:
            print(f"Erro semântico: variável '{var}' não declarada.")
        else:
            tipo_var=tabela[var].upper()
            if tipo_var!='INTEGER':
                print(f"(FOR)Erro semântico: contador não é inteiro")
            tipo_inicio=obter_tipo(inicio)
            tipo_fim=obter_tipo(fim)
            if tipo_inicio!= 'INTEGER':
                print(f"(FOR)Erro semântico: valor incial não é inteiro")
            else:
                print(f"(FOR) Inicialização válida do ciclo: '{var}' <- {tipo_inicio}")            
            if tipo_fim!= 'INTEGER':
                print(f"(FOR)Erro semântico: valor final não é inteiro")

            analisador_semantico(nodo[4])#comandos

    elif caixa=='WRITELN':
        argumentos=nodo[1]
        for arg in argumentos:
            analisador_semantico(arg)


#------------------------------------
#-- geraçao de codigo (incompleto) ---

endereco={}
indice=0
qt_for=0

for i in tabela:
    endereco[i]=indice
    indice+=1

# --- Contador Global para as Labels ---
label_counter = 0

def nova_label():
    global label_counter
    label_counter += 1
    return f"L{label_counter}"

def geracao_codigo(nodo):
    global qt_for # Mantemos a tua variavel antiga se quiseres, mas o nova_label substitui bem
    
    if nodo is None: return
    if isinstance(nodo, list):
        for n in nodo: geracao_codigo(n)
        return
    if not isinstance(nodo, tuple): return

    caixa = nodo[0]

    if caixa == 'PROGRAM':
        print("start")
        # Inicializa variáveis com 0 ou string vazia
        variaveis_ordenadas = sorted(tabela.keys(), key=lambda k: endereco[k])
        for var in variaveis_ordenadas:
            tipo = tabela[var]            
            if tipo == 'STRING':
                print(f"\tpushs \"\"")
            else:
                print(f"\tpushi 0")
        
        geracao_codigo(nodo[2])
        print("stop")
    
    elif caixa == 'RESTO':
        geracao_codigo(nodo[2])

    elif caixa == 'WRITELN':
        args = nodo[1]
        for arg in args:
            if isinstance(arg, tuple) and arg[0] == 'STR':
                print(f"\tpushs \"{arg[1]}\"")
                print("\twrites")
            else:
                geracao_codigo(arg) 
                print("\twritei") # Simplificação: assume que escreve inteiros/bools
            
    elif caixa == 'READLN':
        var_e = endereco[nodo[1]]
        print("\tread")
        print("\tatoi")
        print(f"\tstoreg {var_e}")
    
    elif caixa == 'ASSIGN':
        var = nodo[1]
        valor = nodo[2]
        geracao_codigo(valor)
        print(f"\tstoreg {endereco[var]}")

    elif caixa == 'NUM':
        print(f"\tpushi {nodo[1]}")
    
    elif caixa == 'TRUE':  # Tratamento do TRUE
        print(f"\tpushi 1")
        
    elif caixa == 'FALSE': # Tratamento do FALSE
        print(f"\tpushi 0")

    elif caixa == 'VAR':
        print(f"\tpushg {endereco[nodo[1]]}")

    elif caixa == 'CONTA':
        sinal = nodo[1]
        geracao_codigo(nodo[2])
        geracao_codigo(nodo[3])
        
        # AQUI ESTAVA O PROBLEMA DOS "NONE"
        # O dicionário tem de ter TODAS as operações usadas
        sinais = {
            '+': 'add', '-': 'sub', '*': 'mul', '/': 'div', 
            'div': 'div',   # 'div' (palavra) é diferente de '/' (símbolo)
            'mod': 'mod',
            'and': 'mul',   # AND logico
            '=':  'equal',
            '<':  'inf',
            '>':  'sup',
            '<=': 'infeq',
            '>=': 'supeq'
        }
        instrucao = sinais.get(sinal)
        if instrucao:
            print(f"\t{instrucao}")
        else:
            print(f"\tErr_Op_Desconhecida_{sinal}") # Debug caso falte algo

    elif caixa == 'WHILE':
        lbl_ini = nova_label()
        lbl_fim = nova_label()
        
        print(f"{lbl_ini}:")
        geracao_codigo(nodo[1])    # Condição
        print(f"\tjz {lbl_fim}")
        geracao_codigo(nodo[2])    # Corpo
        print(f"\tjump {lbl_ini}")
        print(f"{lbl_fim}:")

    elif caixa == 'IF':
        lbl_fim = nova_label()
        geracao_codigo(nodo[1])
        print(f"\tjz {lbl_fim}")
        geracao_codigo(nodo[2])
        print(f"{lbl_fim}:")

    elif caixa == 'IF_ELSE':
        lbl_else = nova_label()
        lbl_fim = nova_label()
        
        geracao_codigo(nodo[1])      # Condição
        print(f"\tjz {lbl_else}")    # Salta para o else se falso
        geracao_codigo(nodo[2])      # Bloco Then
        print(f"\tjump {lbl_fim}")   # Salta o bloco else
        
        print(f"{lbl_else}:")
        geracao_codigo(nodo[3])      # Bloco Else
        print(f"{lbl_fim}:")

    elif caixa == 'FOR':
        # Mantive o teu código original do FOR, só adaptei ligeiramente
        var = nodo[1]
        inicio = nodo[2]
        fim = nodo[3]
        resto = nodo[4]
        
        lbl_in = nova_label()
        lbl_out = nova_label()

        geracao_codigo(inicio)
        print(f"\tstoreg {endereco[var]}")
        
        print(f"{lbl_in}:")
        print(f"\tpushg {endereco[var]}")
        geracao_codigo(fim)
        print(f"\tinfeq")           # i <= n ?
        print(f"\tjz {lbl_out}")

        geracao_codigo(resto)

        print(f"\tpushg {endereco[var]}")
        print(f"\tpushi 1")
        print(f"\tadd")
        print(f"\tstoreg {endereco[var]}")

        print(f"\tjump {lbl_in}")
        print(f"{lbl_out}:")





if __name__ == '__main__':
    # Exemplo do Fatorial
    pascal_code = """
program NumeroPrimo;
var
num, i: integer;
primo: boolean;
begin
writeln('Introduza um número inteiro positivo:');
readln(num);
primo := true;
i := 2;
while (i <= (num div 2)) and primo do
begin
if (num mod i) = 0 then
primo := false;
i := i + 1;
end;
if primo then
writeln(num, ' é um número primo')
else
writeln(num, ' não é um número primo')
end.
"""

    print("--- 1. LEXER & PARSER ---")
    lexer.input(pascal_code)
    try:
        arvore = parser.parse(pascal_code, lexer=lexer)
    except Exception as e:
        print(f"Erro Fatal no Parser: {e}")
        arvore = None

    if arvore:
        print("\n--- 2. ANÁLISE SEMÂNTICA ---")
        # Limpar tabela antes de começar (boa prática)
        tabela.clear() 
        analisador_semantico(arvore)
        
        print("\n>> Tabela de Símbolos:")
        print(tabela)

        print("\n--- 3. GERAÇÃO DE CÓDIGO (Assembly) ---")
        
        # Passo A: Mapear Variáveis para Endereços (0, 1, 2...)
        # Usamos a ordem da tabela de símbolos
        idx = 0
        for nome_var in tabela:
            endereco[nome_var] = idx
            idx += 1
        
        print(f">> Mapa de Memória: {endereco}\n")
        print("---------------- CÓDIGO GERADO ----------------")
        
        # Passo B: Gerar o Código
        geracao_codigo(arvore)
        
        print("-----------------------------------------------")
