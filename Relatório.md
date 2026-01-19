
# PLC – TP – G05 – 2025/2026

## Compilador de Pascal Standard para Assembly (VM)

**Trabalho realizado por:**  
Vasco Leite (A108399)  
Afonso Leal (A108472)  
Gustavo Faria (A108575)

**Universidade do Minho**  
Braga, Portugal


## Introdução

Este projeto consiste no desenvolvimento de um compilador para a linguagem **Pascal Standard**. O compilador realiza a análise léxica, sintáctica e semântica e gera como resultado código semelhante a **Assembly**, para a [**Máquina Virtual (VM)** ](https://ewvm.epl.di.uminho.pt) disponibilizada no contexto da unidade curricular.

----
### Como Executar

 Pré-requisitos:
Para executar este projeto, é necessário ter o **Python 3** instalado e a biblioteca **PLY** (Python Lex-Yacc).

Utilização
`` 
python main.py <pasta_input> \[pasta_output]``

## Implementação do Analisador Lexical (Lexer)

O analisador lexical do compilador foi implementado recorrendo à biblioteca **PLY (Python Lex-Yacc)**, de forma a definir os tokens e as regras de reconhecimento léxico da linguagem Pascal.

### Palavras reservadas

As palavras reservadas da linguagem Pascal são definidas através de um dicionário (`reserved`), onde a chave corresponde à palavra tal como aparece no código-fonte e o valor corresponde ao tipo de token associado. 

Como a linguagem de programação Pascal Standard não distingue entre maiúsculas ou minúsculas, o lexer converte as palavras para minúsculas antes de serem comparadas com o dicionário de palavras reservadas.

### Definição de tokens

A lista `tokens` contém todos os tipos de tokens reconhecidos pelo lexer. Esta lista inclui:

-   **Identificadores e literais**: identificadores (`ID`), números inteiros (`NUM_INT`), números reais (`NUM_REAL`) e literais de string (`LIT_STRING`);
    
-   **Operadores aritméticos**: soma, subtracção, multiplicação e divisão;
    
-   **Operadores relacionais**: igualdade, menor, maior, menor ou igual e maior ou igual;
    
-   **Símbolos de pontuação**: vírgula, ponto, ponto e vírgula, dois pontos;
    
-   **Delimitadores**: parênteses e parênteses rectos;
    
-   **Operadores especiais**: atribuição (`:=`) e intervalo (`..`);
    
-   Todas as **palavras reservadas**.
    

### Expressões regulares simples

Os tokens mais simples, como operadores e símbolos de pontuação, são definidos através de expressões regulares associadas directamente a variáveis com o prefixo `t_`. Por exemplo, o símbolo `+` é reconhecido pelo token `PLUS`, enquanto `:=` corresponde ao token `ASSIGN`. 

### Comentários

O lexer suporta dois tipos de comentários da linguagem Pascal:

-   Comentários delimitados por `{ }`;
    
-   Comentários delimitados por `(* *)`.
    

Sempre que um comentário é encontrado, o seu conteúdo é ignorado e o número da linha é actualizado de acordo com o número de newlines (\n) presentes no comentário. Desta forma, os comentários não interferem com a análise sintáctica nem com a contagem das linhas para efeitos de debugging.

### Identificadores e palavras reservadas

Os identificadores são reconhecidos por uma expressão regular que permite letras, números e o carácter `_`, desde que não comecem por um número. Após o reconhecimento, o lexer verifica se o identificador corresponde a uma palavra reservada. Caso corresponda, o tipo do token é actualizado para o tipo adequado; caso contrário, é classificado como `ID`.

### Literais de string

Os literais de string são definidos como sequências de caracteres delimitadas por plicas (`'`). O lexer remove automaticamente as plicas exteriores, armazenando apenas o conteúdo da string no valor do token.

### Números inteiros e reais

Os números reais são reconhecidos como uma sequência de dígitos seguida de um ponto e outra sequência de dígitos, sendo convertidos para o tipo `float`. Os números inteiros são reconhecidos como uma sequência de dígitos e convertidos para o tipo `int`. 

### Controlo de linhas e espaços em branco

As quebras de linha (\n) são tratadas explicitamente para manter o número da linha actualizado, o que garante que as mensagens de erro apontam para a linha correta. Espaços e tabulações (\t) são ignorados através da variável `t_ignore`.

### Tratamento de erros lexicais

Sempre que o lexer encontra um carácter que não corresponde a nenhum token válido, é emitida uma mensagem de erro indicando o carácter ilegal e a linha onde ocorreu o erro. O lexer avança então para o carácter seguinte, permitindo continuar a análise do resto do programa.

## Implementação do Analisador Sintáctico (Parser)

O analisador sintáctico do compilador foi implementado utilizando o módulo **`ply.yacc`**. O parser tem como principal objectivo validar a estrutura sintáctica dos programas escritos em Pascal e construir uma **representação intermédia** (árvore sintáctica abstracta) que será utilizada nas fases seguintes do compilador, nomeadamente na análise semântica e na geração de código assembly.

O parser utiliza os tokens definidos pelo analisador lexical, importados directamente a partir do módulo do lexer.

### Símbolo inicial e precedência de operadores

O símbolo inicial da gramática é definido como `program`, correspondendo à estrutura global de um programa Pascal.

Para evitar ambiguidades na análise de expressões, é definida uma tabela de **precedência e associatividade de operadores**. Esta tabela estabelece:

-   Prioridade mais baixa para os operadores lógicos `AND` e `OR`;
    
-   Prioridade intermédia para operadores relacionais (`=`, `<`, `>`, `<=`, `>=`);
    
-   Prioridade superior para operadores aritméticos aditivos (`+` e `-`);
    
-   Prioridade mais elevada para operadores multiplicativos (`*`, `/`, `div` e `mod`).
    
Esta definição garante que as expressões são interpretadas de acordo com as regras da linguagem Pascal.

### Estrutura geral do programa

A produção `program` define a estrutura base de um programa Pascal, que começa com a palavra `PROGRAM`, seguida do identificador do programa, de um ponto e vírgula e do restante conteúdo. O nó sintáctico gerado armazena o nome do programa e o corpo correspondente.

A regra `resto` descreve a organização interna do programa, incluindo:

-   Declarações de variáveis globais;
    
-   Declarações de funções;
    
-   Um bloco principal delimitado por `BEGIN` e `END`.
    

As variáveis declaradas antes e depois das funções são juntas num único conjunto, de forma que seja mais simples trabalhar com as mesmas posteriormente 

### Declaração de variáveis

As declarações de variáveis são opcionais e iniciadas pela palavra `VAR`. Cada declaração associa uma lista de identificadores a um determinado tipo. O parser suporta múltiplas declarações consecutivas, permitindo agrupar variáveis do mesmo tipo numa única instrução.

Os tipos suportados incluem:

-   Tipos simples (`INTEGER`, `STRING` e `BOOLEAN`);
    
-   Tipos estruturados, como **arrays**, definidos através de um intervalo de índices.
    

### Declaração de funções

O parser permite a definição de funções através da produção `funcao`. Cada função inclui:

-   Um identificador;
    
-   Uma lista de argumentos, com respectivos tipos;
    
-   Um tipo de retorno;
    
-   Declarações de variáveis locais;
    
-   Um corpo de código delimitado por `BEGIN` e `END`.
    

As funções são armazenadas numa estrutura que inclui toda a informação necessária para a geração de código e para a verificação semântica.

### Comandos e blocos de código

O código executável do programa é representado por uma lista de comandos. O parser suporta os principais comandos da linguagem Pascal, nomeadamente:

-   Atribuições simples e a elementos de arrays;
    
-   Estruturas de controlo de fluxo (`if`, `if-else`, `while` e `for`);
    
-   Escrita e leitura (`writeln` e `readln`);
    
-   Blocos de código delimitados por `BEGIN` e `END`.

### Expressões

O parcer tem suporte para as seguintes operações:

-   Operações aritméticas;
    
-   Operações relacionais;
    
-   Operações lógicas.
    

As expressões são identificadas pelo operador, e contêm os operandos esquerdo e direito.

### Termos

Os termos representam os elementos básicos das expressões, podendo ser:

-   Constantes inteiras ou reais;
    
-   Literais de string;
    
-   Valores booleanos (`true` e `false`);
    
-   Variáveis;
    
-   Acessos a arrays;
    
-   Chamadas a funções;
    
-   Expressões entre parênteses.
    

Cada termo é convertido num nó que identifica explicitamente o seu tipo.

### Argumentos de funções e procedimentos

O parser suporta listas de argumentos tanto na declaração como na chamada de funções. Os argumentos são tratados como listas ordenadas de expressões, respeitando a sintaxe da linguagem Pascal.

### Produções vazias

A produção `empty` é utilizada para representar componentes opcionais da gramática, como declarações de variáveis ou listas de comandos vazias. 

### Tratamento de erros sintácticos

O parser inclui um mecanismo de tratamento de erros que detecta e reporta erros de sintaxe, indicando o token problemático e a linha onde ocorreu o erro. Em caso de fim inesperado do ficheiro, é apresentada uma mensagem apropriada.


## Implementação da Análise Semântica

A análise semântica é realizada pelo módulo `semantica.py`, que percorre a Árvore de Sintaxe Abstrata (AST) gerada pelo *parser* para validar o significado das instruções e garantir a coerência do código. Esta etapa foca-se na verificação de tipos, declaração de identificadores e validação de operações.

### Tabela de Símbolos

Para gerir o contexto do programa, foi utilizada uma estrutura de dados global designada por `tabela` (um dicionário de Python). Esta tabela armazena informações sobre todos os identificadores declarados, permitindo verificar se variáveis e funções são utilizadas corretamente.

A tabela associa o nome do identificador (chave) à sua informação de tipo (valor):

* **Variáveis Simples:** O valor é uma string com o tipo (ex: `'INTEGER'`, `'BOOLEAN'`).
* **Arrays:** O valor é um tuplo contendo a estrutura do array, limites e tipo base (ex: `('ARRAY', min, max, 'INTEGER')`).
* **Funções:** O valor é um tuplo que armazena a assinatura da função, incluindo o tipo de retorno e a lista de nomes dos argumentos (ex: `('FUNCTION', 'INTEGER', ['arg1', 'arg2'])`).

### Inferência e Verificação de Tipos

A verificação de tipos é suportada pela função auxiliar `obter_tipo(nodo)`, que determina recursivamente o tipo de uma expressão ou termo na AST.

O sistema de tipos implementado segue as seguintes regras:

* **Literais:** Números inteiros são identificados como `'INTEGER'`, reais como `'REAL'`, strings como `'STRING'` e valores lógicos como `'BOOLEAN'`.
* **Variáveis e Chamadas:** O tipo é recuperado através da consulta à tabela de símbolos.
* **Operações Aritméticas (`CONTA`):**
* Operações entre dois inteiros resultam num `'INTEGER'` (exceto a divisão `/`, que resulta em `'REAL'`).
* Operações que envolvam reais resultam em `'REAL'`.
* Operações relacionais (como `=`, `<`, `>=`) resultam sempre em `'BOOLEAN'`.



### Validações Implementadas

O analisador semântico (`analisador_semantico`) percorre os nós da AST e aplica regras específicas para cada estrutura:

1. **Declarações (`VARS` e `DEF_FUNCTION`):**
As variáveis e funções são inseridas na tabela de símbolos. No caso das funções, é também processado o contexto dos seus argumentos e corpo.
2. **Atribuições (`ASSIGN`):**
Verifica-se se a variável alvo foi declarada e se o tipo da expressão atribuída é compatível com o tipo da variável. Caso contrário, é reportado um erro semântico de incompatibilidade de tipos.
3. **Estruturas de Controlo (`IF`, `WHILE`, `FOR`):**
* No laço `FOR`, valida-se se a variável de controlo foi declarada e se é, obrigatoriamente, do tipo `'INTEGER'`, conforme exigido pelo standard Pascal simplificado.
* Nas estruturas condicionais, verifica-se a validade das expressões de teste.


4. **Entrada e Saída (`READLN`):**
Verifica-se se as variáveis passadas como argumento para leitura foram previamente declaradas.

### Tratamento de Erros

Quando uma violação das regras semânticas é detetada (como o uso de uma variável não declarada ou uma operação inválida entre tipos), o compilador emite uma mensagem de erro indicando a natureza do problema (ex: `Erro semântico: tipos diferentes esq: 'INTEGER', dir: 'STRING'`), permitindo ao utilizador corrigir o código fonte antes da fase de geração de código.


## Implementação da Geração de Código

Esta etapa final dedica-se à geração do código para a Máquina Virtual (VM), percorrendo a árvore de sintaxe dada pelas intruções anteriores e traduz as instruções de Pascal para a linguagem assembly suportada pela VM


### Gestão de Memória

No início da execução, no nó PROGRAM, o gerador irá percorrer a tabela de símbolos e vai alocar espaço na heap da VM conforme as variáveis declaradas, INTEGER e BOOLEAN, são alocadas com **pushi 0**(ou pushi 1 caso seja TRUE) e armazenadas numa posição de memória global **(storeg)**. Strings são inicializadas como strings vazias **pushs ""** e relativamente a arrays, o espaço é reservado utilizando a instrução **allocn**.
Para gerir os endereços, o compilador mantém um dicionário auxiliar endereco que mapeia o nome de cada variável ao seu índice correspondente na memória da VM.

### Controlo de Fluxo

As estruturas de controlo de fluxo do Pascal (for, while, if e if-else) são convertidas utilizando etiquetas (labels) e instruções de salto. A função auxiliar **nova_label** gera identificadores únicos para seram usados nos seus respetivos pontos de salto. Utiliza-se a instrução jump e as suas variações para então saltar blocos de código. Por exemplo, usa-se **jz** (jump se zero) para saltar o bloco then caso a condição seja falsa e ir para o else caso este exista. Nos ciclos **while**, usa-se duas labels, uma para marcar o início e a outra para marcar o fim deste ciclo. Caso a condição de saída se encontre verdadeira, este iŕa então sair do ciclo. No ciclo **for**, o compilador gera código para inicializar a variável de controlo, testá-la e verificar a condição de paragem (infeq para TO ou supeq para DOWNTO) e incrementar ou decrementar a variável no final de cada iteração.

### Funções e Procedimentos

Antes de invocar a função **CALL**, os argumentos são avaliados e os seus valores são armazenados diretamente nas variáveis globais correspondentes aos parâmetros da função (storeg). De seguida, executa-se a instrução pusha (para carregar o endereço da função) e call.
Na **DEF_FUNCTION**, o corpo da função é identificado por uma label (ex: FUNCBinToInt). No final da execução, o valor de retorno (armazenado numa variável com o mesmo nome da função) é colocado no topo da pilha (pushg) antes da instrução return.

### Arrays

Para aceder a um array, o gerador coloca o endereço base e o valor do índice i na pilha. De seguida, subtrai o limite inferior do array (offset) e utiliza as instruções loadn (para leitura) ou storen (para escrita).

### Input e Output

A VM fornece a instrução read, que lê sempre uma sequência de caracteres (string) do input. É emitida a instrução read para colocar a string lida na pilha, se este for Integer, então usa-se atoi para tornar a string no valor númerico correspondente. Para a escrita, usa-se a instrução write que, conforme as suas variações (writei para tipo INTEGER, writef para tipo REAL, writes para tipo STRING), escreve o que for necessário. Usa-se writeln para quebra linha.