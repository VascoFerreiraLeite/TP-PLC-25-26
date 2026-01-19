from semantica import tabela, obter_tipo

endereco={}
label_counter=0

def reset_label():
    global label_counter
    label_counter=0

def nova_label():
    global label_counter
    label_counter+=1
    return f"L{label_counter}"

def geracao_codigo(nodo):
    global endereco 
    
    if nodo is None:
        return
    if isinstance(nodo, list):
        for n in nodo:
            geracao_codigo(n)
        return
    if not isinstance(nodo, tuple):
        return

    caixa=nodo[0]

    if caixa=='NUM':
        print(f"\tpushi {nodo[1]}")
    elif caixa=='REAL':
        print(f"\tpushf {nodo[1]}")

    elif caixa == 'PROGRAM':
        print("start")
        endereco.clear()
        
        for var, info in tabela.items():
            if isinstance(info, tuple):
                if info[0] == 'ARRAY':
                    tamanho = info[2] - info[1] + 1
                    print(f"\tpushi {tamanho}")
                    print(f"\tallocn")
                    print(f"\tstoreg {len(endereco)}")
                    endereco[var] = len(endereco)
                elif info[0] == 'FUNCTION':
                    if info[1] == 'STRING': print(f"\tpushs \"\"")
                    else: print(f"\tpushi 0")
                    print(f"\tstoreg {len(endereco)}")
                    endereco[var] = len(endereco)
            else:
                if info == 'STRING': print(f"\tpushs \"\"")
                else: print(f"\tpushi 0")
                print(f"\tstoreg {len(endereco)}")
                endereco[var] = len(endereco)

        print("\tjump MAIN")
        geracao_codigo(nodo[2])
        print("stop")
    
    elif caixa == 'RESTO':
        funcoes = nodo[2]
        codigo_main = nodo[3]
        geracao_codigo(funcoes)
        print("MAIN:")
        geracao_codigo(codigo_main)

    elif caixa == 'DEF_FUNCTION':
        nome = nodo[1]
        corpo = nodo[5]
        print(f"FUNC{nome}:")
        
        
        geracao_codigo(corpo)
        
        if nome in endereco:
             print(f"\tpushg {endereco[nome]}")
        print("\treturn")

    elif caixa == 'CALL':
        nome = nodo[1]
        args_expressao = nodo[2]
        
        if nome.lower() == 'length':
            geracao_codigo(args_expressao[0])
            print("\tstrlen")  
        else:
            info = tabela.get(nome)
            if info and isinstance(info, tuple) and info[0] == 'FUNCTION':
                lista_args_nomes = info[2]
                for nome_arg, expr in zip(lista_args_nomes, args_expressao):
                    geracao_codigo(expr)
                    if nome_arg in endereco:
                        print(f"\tstoreg {endereco[nome_arg]}")

            print(f"\tpusha FUNC{nome}")
            print("\tcall")

    elif caixa == 'WRITELN':
        args = nodo[1]
        for arg in args:
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
        arg = nodo[1]
        if arg[0] == 'VAR':
            nome = arg[1]
            print("\tread")
            info = tabela.get(nome)
            is_string = False
            if info == 'STRING': is_string = True
            elif isinstance(info, tuple) and info[0] == 'FUNCTION' and info[1] == 'STRING': is_string = True
            
            if not is_string: print("\tatoi")
            print(f"\tstoreg {endereco[nome]}")

        elif arg[0] == 'ARRAY':
            nome = arg[1]
            idx_expr = arg[2]
            info = tabela[nome]
            offset = info[1] 
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
        valor_expr = nodo[3]
        info = tabela[nome]
        offset = info[1] if isinstance(info, tuple) else 1
        
        print(f"\tpushg {endereco[nome]}") 
        geracao_codigo(idx_expr)         
        print(f"\tpushi {offset}")
        print("\tsub")                  
        geracao_codigo(valor_expr)       
        print("\tstoren")               

    elif caixa == 'ARRAY':
        nome = nodo[1]
        idx_expr = nodo[2]
        info = tabela[nome]
        offset = info[1] if isinstance(info, tuple) else 1
        
        print(f"\tpushg {endereco[nome]}") 
        geracao_codigo(idx_expr)        
        print(f"\tpushi {offset}")
        print("\tsub")                  
        
        if info == 'STRING' or (isinstance(info, tuple) and info[3] == 'STRING'):
             print("\tcharat")
        else:
             print("\tloadn")

    elif caixa == 'STR':
        valor = nodo[1]
        if len(valor) == 1: print(f"\tpushi {ord(valor)}")
        else: print(f"\tpushs \"{valor}\"")

    elif caixa == 'TRUE': print(f"\tpushi 1")
    elif caixa == 'FALSE': print(f"\tpushi 0")
    elif caixa == 'VAR': print(f"\tpushg {endereco[nodo[1]]}")
        
    elif caixa == 'CONTA':
        sinal = nodo[1]
        geracao_codigo(nodo[2])
        geracao_codigo(nodo[3])
        sinais = {'+': 'add', '-': 'sub', '*': 'mul', '/': 'div', 'div': 'div', 'mod': 'mod', 'and': 'mul', '=': 'equal', '<': 'inf', '>': 'sup', '<=': 'infeq', '>=': 'supeq', 'or': 'or'}
        if sinal in sinais: print(f"\t{sinais[sinal]}")

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
        sentido = nodo[3]
        fim = nodo[4]
        corpo = nodo[5]
        
        if isinstance(sentido, str): sentido = sentido.upper()
        else: sentido = 'TO'

        lbl_in = nova_label()
        lbl_out = nova_label()

        geracao_codigo(inicio)
        print(f"\tstoreg {endereco[var]}")
        
        print(f"{lbl_in}:")
        print(f"\tpushg {endereco[var]}")
        geracao_codigo(fim)
        
        if sentido == 'DOWNTO': print(f"\tsupeq")
        else: print(f"\tinfeq")
            
        print(f"\tjz {lbl_out}")

        geracao_codigo(corpo)

        print(f"\tpushg {endereco[var]}")
        print(f"\tpushi 1")
        if sentido == 'DOWNTO': print(f"\tsub")
        else: print(f"\tadd")
        print(f"\tstoreg {endereco[var]}")

        print(f"\tjump {lbl_in}")
        print(f"{lbl_out}:")