#------------------------------------
#-- Tabela de Simbolos Global ---
tabela = {}

#------------------------------------
#-- Obter tipos ---

def obter_tipo(nodo):
    if not isinstance(nodo, tuple):
        return None

    caixa = nodo[0]

    if caixa == 'NUM':
        return 'INTEGER'
    if caixa == 'REAL':
        return 'REAL'
    if caixa == 'STR':
        return 'STRING'
    if caixa == 'TRUE' or caixa == 'FALSE': 
        return 'BOOLEAN'

    if caixa == 'VAR':
        var = nodo[1]
        if var in tabela:
            # Garante que devolvemos a string do tipo
            info = tabela[var]
            if isinstance(info, dict):
                return info['type'].upper()
            return str(info).upper()
        else:
            print(f"Erro semântico: variável '{var}' não declarada.")
            return None

    if caixa == 'ARRAY_ACCESS':
        nome_array = nodo[1]
        indice_expr = nodo[2]
        
        if nome_array not in tabela:
            print(f"Erro semântico: array '{nome_array}' não declarado.")
            return None
        
        tipo_indice = obter_tipo(indice_expr)
        if tipo_indice != 'INTEGER':
            print(f"Erro semântico: O índice do array '{nome_array}' deve ser inteiro. Recebido: {tipo_indice}")
        
        tipo_base_info = tabela[nome_array]['type']
        
        if isinstance(tipo_base_info, dict):
            return tipo_base_info['type'].upper()
        else:
            return str(tipo_base_info).upper()

    if caixa == 'CONTA':
        op = nodo[1]
        tipo_esq = obter_tipo(nodo[2])
        tipo_dir = obter_tipo(nodo[3])

        if op in ['=', '<', '>', '<=', '>=', 'and', 'or']:
            return 'BOOLEAN'
        
        if tipo_esq == 'INTEGER' and tipo_dir == 'INTEGER':
            if op == '/': return 'REAL'
            return 'INTEGER'
            
        print(f"Erro semântico: tipos incompatíveis na operação '{op}': '{tipo_esq}' vs '{tipo_dir}'")
        return None

#------------------------------------
#-- Analisador Semântico ---

def analisador_semantico(nodo):
    if nodo is None: return
    if isinstance(nodo, list):
        for n in nodo: analisador_semantico(n)
        return
    if not isinstance(nodo, tuple): return
    
    caixa = nodo[0]

    if caixa == 'PROGRAM':
        analisador_semantico(nodo[2])

    elif caixa == 'VARS':
        lista_vars = nodo[1]
        tipo_info = nodo[2] # Dicionário {'cat':..., 'type':...}

        # Normalizar string do tipo para maiúsculas
        if isinstance(tipo_info, dict) and 'type' in tipo_info:
             if isinstance(tipo_info['type'], str):
                 tipo_info['type'] = tipo_info['type'].upper()
        
        for var in lista_vars:
            if var in tabela:
                print(f"Erro semantico: variavel '{var}' redeclarada.")
            else:
                tabela[var] = tipo_info

    elif caixa == 'RESTO':
        analisador_semantico(nodo[1])  # vars
        analisador_semantico(nodo[2])  # codigo

    elif caixa == 'ASSIGN':
        var = nodo[1]
        expressao = nodo[2]
        if var not in tabela:
            print(f"Erro semântico: variável '{var}' não declarada.")
        else:
            # CORREÇÃO: Aceder a ['type']
            tipo_var = tabela[var]['type'].upper()
            tipo_obtido = obter_tipo(expressao)
            
            if tipo_obtido and tipo_var != tipo_obtido:
                print(f"Erro semântico: Atribuição inválida para '{var}'. Esperado {tipo_var}, obtido {tipo_obtido}")
            
            analisador_semantico(expressao)

    # NOVO: Atribuição a Array (ex: vec[i] := 10)
    elif caixa == 'ASSIGN_ARRAY':
        nome = nodo[1]
        idx_expr = nodo[2]
        val_expr = nodo[3]
        
        if nome not in tabela:
            print(f"Erro semântico: Array '{nome}' não declarado.")
        else:
            # 1. Verificar se é mesmo um array
            if tabela[nome]['cat'] != 'array':
                print(f"Erro semântico: '{nome}' não é um array.")
            
            # 2. Verificar se o índice é inteiro
            tipo_idx = obter_tipo(idx_expr)
            if tipo_idx != 'INTEGER':
                print(f"Erro semântico: Índice de '{nome}' deve ser INTEGER, recebido {tipo_idx}.")

            # 3. Verificar se o valor corresponde ao tipo do array
            tipo_esperado = tabela[nome]['type'].upper()
            tipo_valor = obter_tipo(val_expr)
            if tipo_valor and tipo_esperado != tipo_valor:
                print(f"Erro semântico: Array '{nome}' espera {tipo_esperado}, recebido {tipo_valor}.")

            analisador_semantico(idx_expr)
            analisador_semantico(val_expr)
        
    elif caixa == 'CONTA':
        analisador_semantico(nodo[2])
        analisador_semantico(nodo[3])
    
    elif caixa == 'WHILE':
        tipo_cond = obter_tipo(nodo[1])
        if tipo_cond != 'BOOLEAN':
             print("Aviso: Condição do WHILE não é booleana.") # Pascal permite? Normalmente sim, mas bom avisar
        analisador_semantico(nodo[2])

    elif caixa == 'IF':
        condicao = nodo[1]
        bloco_then = nodo[2]
        
        tipo_cond = obter_tipo(condicao)
        if tipo_cond != 'BOOLEAN':
            print(f"Erro semântico: A condição do IF deve ser BOOLEAN. Encontrado: {tipo_cond}")
        
        analisador_semantico(bloco_then)

    elif caixa == 'IF_ELSE':
        condicao = nodo[1]
        bloco_then = nodo[2]
        bloco_else = nodo[3]
        
        tipo_cond = obter_tipo(condicao)
        if tipo_cond != 'BOOLEAN':
            print(f"Erro semântico: A condição do IF deve ser BOOLEAN. Encontrado: {tipo_cond}")
        
        analisador_semantico(bloco_then)
        analisador_semantico(bloco_else)

    elif caixa == 'FOR':
        var = nodo[1]
        inicio = nodo[2]
        fim = nodo[3]
        
        if var not in tabela:
            print(f"Erro semântico: variável '{var}' não declarada.")
        else:
            # CORREÇÃO: Aceder a ['type']
            if tabela[var]['type'].upper() != 'INTEGER':
                print(f"(FOR) Erro: Variável de controle '{var}' deve ser INTEGER.")
            
            if obter_tipo(inicio) != 'INTEGER':
                print(f"(FOR) Erro: Valor inicial deve ser INTEGER.")
            
            if obter_tipo(fim) != 'INTEGER':
                print(f"(FOR) Erro: Valor final deve ser INTEGER.")

            analisador_semantico(nodo[4]) # comandos

    elif caixa == 'WRITELN':
        # Validar argumentos se necessário
        pass 

    elif caixa == 'READLN':
        item = nodo[1]
        # Se for variável simples
        if isinstance(item, str):
            if item not in tabela:
                print(f"Erro: Variável '{item}' no READLN não existe.")
        # Se for acesso a array (ex: readln(v[i]))
        elif isinstance(item, tuple) and item[0] == 'ARRAY_ACCESS':
            nome = item[1]
            idx = item[2]
            if nome not in tabela:
                print(f"Erro: Array '{nome}' no READLN não existe.")
            elif obter_tipo(idx) != 'INTEGER':
                print(f"Erro: Índice do array no READLN deve ser inteiro.")