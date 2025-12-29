from semantica import tabela, obter_tipo

#------------------------------------
#-- Geração de Código ---
#------------------------------------

endereco = {}
label_counter = 0

def reset_label():
    global label_counter
    label_counter = 0

def nova_label():
    global label_counter
    label_counter += 1
    return f"L{label_counter}"

def geracao_codigo(nodo):
    global endereco 
    
    if nodo is None: return
    if isinstance(nodo, list):
        for n in nodo: geracao_codigo(n)
        return
    if not isinstance(nodo, tuple): return

    caixa = nodo[0]

    if caixa == 'PROGRAM':
        print("start")
        
        # --- CORREÇÃO: Alocações PRIMEIRO, Jump DEPOIS ---
        
        # 1. Alocar variáveis globais
        for var, info_tipo in tabela.items():
            # Proteção para saber se é dicionário ou string
            tipo_cat = info_tipo['cat'] if isinstance(info_tipo, dict) else 'simple'
            
            if tipo_cat == 'array':
                tamanho = info_tipo['max'] - info_tipo['min'] + 1
                print(f"\tpushi {tamanho}")
                print(f"\tallocn")
                print(f"\tstoreg {endereco[var]}")
            elif tipo_cat == 'simple': 
                # Inicializa inteiros e bools a 0
                if info_tipo.get('type') == 'STRING':
                     print(f"\tpushs \"\"")
                else:
                     print(f"\tpushi 0")
                print(f"\tstoreg {endereco[var]}")
        
        # 2. Agora sim, saltamos as funções para ir para o MAIN
        print("\tjump MAIN")
        
        # 3. Gerar o resto (Funções + Label MAIN + Código)
        geracao_codigo(nodo[2])
        print("stop")
    
    elif caixa == 'RESTO':
        funcoes = nodo[2]
        codigo_main = nodo[3]
        geracao_codigo(funcoes)
        
        # CORREÇÃO 1: Label MAIN limpa
        print("MAIN:")
        geracao_codigo(codigo_main)

    # --- CORREÇÃO: Função tem de devolver valor ---
    elif caixa == 'DEF_FUNCTION':
        nome = nodo[1]
        corpo = nodo[5]
        
        print(f"FUNC{nome}:")
        geracao_codigo(corpo)
        
        # IMPORTANTE: Pôr o resultado na stack antes de sair!
        # O resultado está guardado na variável com o nome da função
        if nome in endereco:
             print(f"\tpushg {endereco[nome]}")
             
        print("\treturn")

    elif caixa == 'CALL':
        nome = nodo[1]
        args_lista = nodo[2]
        
        if nome.lower() == 'length':
            geracao_codigo(args_lista[0])
            # CORREÇÃO: A instrução documentada é STRLEN
            print("\tstrlen")  
        else:
            geracao_codigo(args_lista)
            print(f"\tpusha FUNC{nome}")
            print("\tcall")

    elif caixa == 'WRITELN':
        args = nodo[1]
        for arg in args:
            # Caso especial para strings diretas no writeln
            if isinstance(arg, tuple) and arg[0] == 'STR':
                print(f"\tpushs \"{arg[1]}\"")
                print("\twrites")
            else:
                geracao_codigo(arg)
                tipo = obter_tipo(arg)
                if tipo == 'REAL': print("\twritef")
                elif tipo == 'STRING': print("\twrites")
                else: print("\twritei")
        print("\twriteln")
            
    elif caixa == 'READLN':
        item = nodo[1]
        
        # Leitura de variável simples
        if isinstance(item, str):
            var_e = endereco[item]
            print("\tread")
            
            # Só fazemos atoi se NÃO for String!
            # Precisamos de ir à tabela ver o tipo
            info = tabela.get(item)
            # Proteção: se info for dict usa ['type'], senão usa str(info)
            tipo_var = info['type'] if isinstance(info, dict) else str(info)
            
            if tipo_var.upper() != 'STRING':
                print("\tatoi")
                
            print(f"\tstoreg {var_e}")
            
        # Leitura de Array (mantém-se, assumindo array de inteiros)
        elif isinstance(item, tuple) and item[0] == 'ARRAY_ACCESS':
            nome = item[1]
            idx_expr = item[2]
            info = tabela[nome]
            
            if info.get('type') == 'STRING': offset = 1
            else: offset = info['min']
            
            print(f"\tpushg {endereco[nome]}") 
            geracao_codigo(idx_expr)         
            print(f"\tpushi {offset}")
            print("\tsub")                   
            print("\tread")                  
            print("\tatoi")
            print("\tstoren")
    
    elif caixa == 'ASSIGN':
        var = nodo[1]
        valor = nodo[2]
        geracao_codigo(valor)
        print(f"\tstoreg {endereco[var]}")

    elif caixa == 'ASSIGN_ARRAY':
        nome = nodo[1]
        idx_expr = nodo[2]
        val_expr = nodo[3]
        info = tabela[nome]
        
        if info.get('type') == 'STRING': offset = 1
        else: offset = info['min']

        print(f"\tpushg {endereco[nome]}") 
        geracao_codigo(idx_expr)         
        print(f"\tpushi {offset}")
        print("\tsub")                   
        geracao_codigo(val_expr)         
        print("\tstoren")

    elif caixa == 'NUM':
        print(f"\tpushi {nodo[1]}")
    
    # --- CORREÇÃO 2: ESTE BLOCO FALTAVA! ---
    # Sem isto, strings em comparações (ex: if x = '1') não são colocadas na stack!
    # Adiciona/Substitui este bloco no teu codeGen.py
    elif caixa == 'STR':
        valor = nodo[1]
        # TRUQUE: Se for um único caracter, tratamos como Inteiro ASCII para comparações
        if len(valor) == 1:
            print(f"\tpushi {ord(valor)}")
        else:
            print(f"\tpushs \"{valor}\"")

    elif caixa == 'TRUE':
        print(f"\tpushi 1")
        
    elif caixa == 'FALSE':
        print(f"\tpushi 0")

    elif caixa == 'VAR':
        print(f"\tpushg {endereco[nodo[1]]}")
        
    elif caixa == 'ARRAY_ACCESS':
        nome = nodo[1]
        idx_expr = nodo[2]
        
        info = tabela[nome]
        
        # Strings na VM começam no 0, Pascal no 1 -> offset 1
        if info.get('type') == 'STRING': 
            offset = 1
        else: 
            offset = info['min']

        print(f"\tpushg {endereco[nome]}") # Stack: [String]
        geracao_codigo(idx_expr)         # Stack: [String, IndiceBruto]
        print(f"\tpushi {offset}")
        print("\tsub")                   # Stack: [String, IndiceReal]
        
        if info.get('type') == 'STRING':
            # CORREÇÃO: CHARAT tira o caracter na posição n da string m
            print("\tcharat") 
        else:
            print("\tloadn") 
        
    elif caixa == 'CONTA':
        sinal = nodo[1]
        geracao_codigo(nodo[2])
        geracao_codigo(nodo[3])

        sinais = {
            '+': 'add', '-': 'sub', '*': 'mul', '/': 'div', 
            'div': 'div', 'mod': 'mod', 'and': 'mul',
            '=': 'equal', '<': 'inf', '>': 'sup', 
            '<=': 'infeq', '>=': 'supeq', 'or': 'or'
        }
        instrucao = sinais.get(sinal)
        if instrucao: print(f"\t{instrucao}")

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

    # --- CORREÇÃO 3: Lógica DOWNTO robusta ---
    elif caixa == 'FOR':
        var = nodo[1]
        inicio = nodo[2]
        fim = nodo[3]
        corpo = nodo[4]
        
        sentido = 'TO'
        # Garante que lê string independentemente de maiusculas/minusculas
        if len(nodo) > 5 and isinstance(nodo[5], str):
            sentido = nodo[5].upper()

        lbl_in = nova_label()
        lbl_out = nova_label()

        geracao_codigo(inicio)
        print(f"\tstoreg {endereco[var]}")
        
        print(f"{lbl_in}:")
        print(f"\tpushg {endereco[var]}")
        geracao_codigo(fim)
        
        # Lógica invertida para downto
        if sentido == 'DOWNTO':
            print(f"\tsupeq") # i >= n  (CORREÇÃO AQUI)
        else:
            print(f"\tinfeq") # i <= n
            
        print(f"\tjz {lbl_out}")

        geracao_codigo(corpo)

        print(f"\tpushg {endereco[var]}")
        print(f"\tpushi 1")
        
        # Decremento para downto
        if sentido == 'DOWNTO':
            print(f"\tsub")   # i - 1 (CORREÇÃO AQUI)
        else:
            print(f"\tadd")
            
        print(f"\tstoreg {endereco[var]}")

        print(f"\tjump {lbl_in}")
        print(f"{lbl_out}:")