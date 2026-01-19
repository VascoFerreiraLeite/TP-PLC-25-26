tabela = {}

def obter_tipo(nodo):
    if not isinstance(nodo, tuple): return 'INTEGER'
    caixa = nodo[0]

    if caixa=='NUM':
        return 'INTEGER'
    if caixa=='REAL':
        return 'REAL'
    if caixa=='STR':
        return 'STRING'
    if caixa=='TRUE' or caixa=='FALSE':
        return 'BOOLEAN'

    if caixa=='VAR':
        var=nodo[1]
        if var in tabela:
            info=tabela[var]
            if isinstance(info, tuple):
                if info[0]=='FUNCTION':
                    return info[1].upper()
                if info[0]=='ARRAY':
                    return info[3].upper()
                return str(info[0]).upper()
            return info.upper()
        print(f"Erro semântico: variável '{var}' não declarada.")
        return None

    if caixa=='ARRAY':
        nome=nodo[1]
        if nome in tabela:
            info=tabela[nome]
            if isinstance(info, tuple) and info[0] == 'ARRAY':
                 return info[3].upper()
            return None
        print(f"Erro semântico: array '{nome}' não declarado.")
        return None

    if caixa=='CONTA':
        op = nodo[1]
        tipo_esq=obter_tipo(nodo[2])
        tipo_dir=obter_tipo(nodo[3])
        if op in ['=', '<', '>', '<=', '>=', 'and', 'or']:
            return 'BOOLEAN'
        if tipo_esq == 'INTEGER' and tipo_dir == 'INTEGER':
            if op == '/':
                return 'REAL'
            return 'INTEGER'
        if tipo_esq == 'REAL' and tipo_dir == 'REAL':
            return 'REAL'
        print(f"Erro semântico: tipos diferentes esq: '{tipo_esq}', dir: '{tipo_dir}'")
        return None

    if caixa == 'CALL':
        nome=nodo[1]
        if nome.lower()=='length':
            return 'INTEGER'
        if nome in tabela:
            info = tabela[nome]
            if isinstance(info, tuple) and info[0] == 'FUNCTION':
                return info[1].upper()
            return str(info).upper()
        return None

    return None

def analisador_semantico(nodo):
    if nodo is None:
        return
    if isinstance(nodo, list):
        for n in nodo: 
            analisador_semantico(n)
        return
    if not isinstance(nodo, tuple):
        return
    
    caixa=nodo[0]

    if caixa == 'PROGRAM':
        tabela.clear()
        analisador_semantico(nodo[2])

    elif caixa == 'RESTO':
        analisador_semantico(nodo[1])
        analisador_semantico(nodo[2])
        analisador_semantico(nodo[3])

    elif caixa=='VARS':
        vars_lista=nodo[1]
        tipo=nodo[2]
        if not isinstance(tipo, tuple):
            tipo=tipo.upper()
        for var in vars_lista:
            tabela[var]=tipo

    elif caixa == 'ARG':
        ids=nodo[1]
        tipo=nodo[2]
        if not isinstance(tipo, tuple):
            tipo=tipo.upper()            
        for var in ids:
            tabela[var]=tipo

    elif caixa=='DEF_FUNCTION':
        nome=nodo[1]
        tipo= nodo[3]
        argumentos_nodo=nodo[2]
        lista_args_nomes=[]
        if argumentos_nodo:
             for arg_pack in argumentos_nodo:
                 lista_args_nomes.extend(arg_pack[1])

        tabela[nome] = ('FUNCTION', tipo.upper(), lista_args_nomes)
        
        analisador_semantico(nodo[2])
        analisador_semantico(nodo[4])
        analisador_semantico(nodo[5])

    elif caixa=='ASSIGN':
        var=nodo[1]
        expressao=nodo[2]
        if var not in tabela:
            print(f"Erro semântico: variável '{var}' não declarada.")
        else:
            tipo_var=obter_tipo(('VAR', var))
            tipo_obtido=obter_tipo(expressao)
            if tipo_var != tipo_obtido:
                print(f"Erro semântico: tipo esperado diferente do obtido, esperado: '{tipo_var}', obtido: '{tipo_obtido}'")

            analisador_semantico(expressao)

    elif caixa=='ASSIGN_ARRAY':
        var=nodo[1]
        expressao=nodo[2]
        valor=nodo[3]
        if var not in tabela:
            print(f"Erro semântico: variável '{var}' não declarada.")
        analisador_semantico(expressao)
        analisador_semantico(valor)
        
    elif caixa=='CONTA':
        analisador_semantico(nodo[2])
        analisador_semantico(nodo[3])
    
    elif caixa=='IF' or caixa=='IF_ELSE':
        obter_tipo(nodo[1])
        analisador_semantico(nodo[2])
        if caixa == 'IF_ELSE':
            analisador_semantico(nodo[3])

    elif caixa == 'WHILE':
        analisador_semantico(nodo[1])
        analisador_semantico(nodo[2])
    
    elif caixa == 'FOR':
        var=nodo[1]
        inicio=nodo[2]
        fim=nodo[3]
        if var not in tabela:
            print(f"Erro semântico: variável '{var}' não declarada.")
        else:
            info = tabela[var]
            if isinstance(info, tuple):
                 print(f"Erro semântico: Variável de ciclo '{var}' inválida.")
            elif info.upper() != 'INTEGER':
                 print(f"(FOR)Erro semântico: contador não é inteiro")
            analisador_semantico(nodo[4])

    elif caixa == 'WRITELN':
        argumentos=nodo[1]
        for arg in argumentos:
            analisador_semantico(arg)

    elif caixa == 'READLN':
        arg=nodo[1]
        if arg[0]== 'VAR':
            nome=arg[1]
            if nome not in tabela:
                print(f"Erro semântico: variável '{nome}' não declarada.")
        elif arg[0] == 'ARRAY':
            nome = arg[1]
            if nome not in tabela:
                 print(f"Erro semântico: array '{nome}' não declarado.")
            analisador_semantico(arg[2])