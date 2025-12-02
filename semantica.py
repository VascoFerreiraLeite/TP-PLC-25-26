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