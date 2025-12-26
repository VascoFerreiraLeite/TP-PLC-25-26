from semantica import tabela

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

def reset_label():
    global label_counter
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