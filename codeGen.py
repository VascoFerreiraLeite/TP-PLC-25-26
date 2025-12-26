from semantica import tabela
from semantica import tabela, obter_tipo

#------------------------------------
#-- Geração de Código ---
#------------------------------------

# O dicionário 'endereco' será preenchido pela main.py antes de chamar a geracao_codigo
endereco = {}

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
    # Acede à variavel global preenchida na main
    global endereco 
    
    if nodo is None: return
    if isinstance(nodo, list):
        for n in nodo: geracao_codigo(n)
        return
    if not isinstance(nodo, tuple): return

    caixa = nodo[0]

    if caixa == 'PROGRAM':
        print("start")
        
        # AQUI: Assume que 'endereco' e 'tabela' já estão preenchidos (pela main.py)
        for var, info_tipo in tabela.items():
            if info_tipo['cat'] == 'array':
                tamanho = info_tipo['max'] - info_tipo['min'] + 1
                print(f"\tpushi {tamanho}")
                print(f"\tallocn")
                print(f"\tstoreg {endereco[var]}")
            elif info_tipo['cat'] == 'simple' or info_tipo['cat'] == 'integer': 
                print(f"\tpushi 0")
                print(f"\tstoreg {endereco[var]}")
        
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
                
                tipo = obter_tipo(arg)
                
                if tipo == 'INTEGER':
                    print("\twritei")
                elif tipo == 'BOOLEAN':
                    print("\twritei") # A VM não tem writeb, usamos writei (0 ou 1)
                elif tipo == 'REAL':
                    print("\twritef")
                elif tipo == 'STRING':
                    print("\twrites")
                else:
                    print("\twritei") 
        print("\twriteln")
            
    elif caixa == 'READLN':
        # Nota: Se quiseres suportar readln(arr[i]), precisas de logica extra aqui
        # Para variaveis simples funciona assim:
        if isinstance(nodo[1], str):
            var_e = endereco[nodo[1]]
            print("\tread")
            print("\tatoi")
            print(f"\tstoreg {var_e}")
        elif isinstance(nodo[1], tuple) and nodo[1][0] == 'ARRAY_ACCESS':
            # Suporte para ler para um array: readln(vec[i])
            nome = nodo[1][1]
            idx_expr = nodo[1][2]
            info = tabela[nome]
            offset = info['min']
            
            # 1. Preparar endereço e índice
            print(f"\tpushg {endereco[nome]}") # Endereço Base
            geracao_codigo(idx_expr)         # Índice i
            print(f"\tpushi {offset}")
            print("\tsub")                   # i - min
            
            # 2. Ler valor
            print("\tread")
            print("\tatoi")
            
            # 3. Guardar (Stack: Addr, Index, Value)
            print("\tstoren")
    
    elif caixa == 'ASSIGN':
        var = nodo[1]
        valor = nodo[2]
        geracao_codigo(valor)
        print(f"\tstoreg {endereco[var]}")

    elif caixa == 'NUM':
        print(f"\tpushi {nodo[1]}")
    
    elif caixa == 'TRUE':
        print(f"\tpushi 1")
        
    elif caixa == 'FALSE':
        print(f"\tpushi 0")

    elif caixa == 'VAR':
        print(f"\tpushg {endereco[nodo[1]]}")

    elif caixa == 'CONTA':
        sinal = nodo[1]
        geracao_codigo(nodo[2])
        geracao_codigo(nodo[3])

        sinais = {
            '+': 'add', '-': 'sub', '*': 'mul', '/': 'div', 
            'div': 'div', 'mod': 'mod', 'and': 'mul',
            '=': 'equal', '<': 'inf', '>': 'sup', 
            '<=': 'infeq', '>=': 'supeq', 'or': 'or' # Adicionei 'or' caso tenhas
        }
        instrucao = sinais.get(sinal)
        if instrucao:
            print(f"\t{instrucao}")

    elif caixa == 'WHILE':
        lbl_ini = nova_label()
        lbl_fim = nova_label()
        print(f"{lbl_ini}:")
        geracao_codigo(nodo[1])
        print(f"\tjz {lbl_fim}")
        geracao_codigo(nodo[2])
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
        geracao_codigo(nodo[1])
        print(f"\tjz {lbl_else}")
        geracao_codigo(nodo[2])
        print(f"\tjump {lbl_fim}")
        print(f"{lbl_else}:")
        geracao_codigo(nodo[3])
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
        print(f"\tinfeq")
        print(f"\tjz {lbl_out}")

        geracao_codigo(resto)

        print(f"\tpushg {endereco[var]}")
        print(f"\tpushi 1")
        print(f"\tadd")
        print(f"\tstoreg {endereco[var]}")

        print(f"\tjump {lbl_in}")
        print(f"{lbl_out}:")

    # --- CORREÇÃO AQUI ---
    # Usar 'caixa' ou 'nodo' em vez de 't'
    elif caixa == 'ASSIGN_ARRAY':
        nome = nodo[1]
        idx_expr = nodo[2]
        val_expr = nodo[3]
        
        info = tabela[nome]
        offset = info['min']

        print(f"\tpushg {endereco[nome]}") # Base
        geracao_codigo(idx_expr)         # Indice expr
        print(f"\tpushi {offset}")
        print("\tsub")                   # Indice real
        geracao_codigo(val_expr)         # Valor
        print("\tstoren")

    elif caixa == 'ARRAY_ACCESS':
        nome = nodo[1]
        idx_expr = nodo[2]
        
        info = tabela[nome]
        offset = info['min']

        print(f"\tpushg {endereco[nome]}")
        geracao_codigo(idx_expr)
        print(f"\tpushi {offset}")
        print("\tsub")
        print("\tloadn")