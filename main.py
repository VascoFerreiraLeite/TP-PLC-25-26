import sys
import os
from lexer import lexer
from parser import parser
from semantica import analisador_semantico, tabela
from codeGen import geracao_codigo, endereco, label_counter

def processar_ficheiro(caminho_input, pasta_output):
    nome_ficheiro = os.path.basename(caminho_input)
    print(f"--> A processar: {nome_ficheiro}")
    
    # 1. Ler o ficheiro
    try:
        with open(caminho_input, 'r', encoding='utf-8') as f:
            conteudo = f.read()
    except Exception as e:
        print(f"Erro ao ler '{nome_ficheiro}': {e}")
        return

    # 2. Resetar estruturas (CRUCIAL para processamento em lote)
    lexer.lineno = 1
    tabela.clear()
    endereco.clear()
    # Se tiveres um contador global de labels no codegen.py, reseta-o também se possível
    # Exemplo: codegen.label_counter = 0 

    # 3. Parsing
    try:
        arvore = parser.parse(conteudo, lexer=lexer)
    except Exception as e:
        print(f"Erro fatal no parser para '{nome_ficheiro}': {e}")
        return

    if not arvore:
        print(f"Aviso: Árvore vazia ou erro de sintaxe em '{nome_ficheiro}'.")
        return

    # 4. Semântica
    analisador_semantico(arvore)
    
    # 5. Definir caminho de saída
    # Mantém o nome original mas muda a extensão para .vm
    nome_base, _ = os.path.splitext(nome_ficheiro)
    nome_output = nome_base + ".vm"
    caminho_output = os.path.join(pasta_output, nome_output)

    # Configurar endereços de memória
    idx = 0
    for nome_var in tabela:
        endereco[nome_var] = idx
        idx += 1

    # 6. Geração de código (Redirecionar stdout)
    stdout_original = sys.stdout
    try:
        with open(caminho_output, 'w', encoding='utf-8') as f_out:
            sys.stdout = f_out
            geracao_codigo(arvore)
    except Exception as e:
        sys.stdout = stdout_original
        print(f"Erro ao escrever output: {e}")
    finally:
        sys.stdout = stdout_original
    
    print(f"    Gerado: {caminho_output}")

def main():
    # Validação de argumentos
    if len(sys.argv) < 2:
        print("Uso: python main.py <pasta_input> [pasta_output]")
        print("Exemplo: python main.py testes resultados")
        return

    input_folder = sys.argv[1]
    # Se não for dada pasta de output, usa uma chamada 'output' por defeito
    output_folder = sys.argv[2] if len(sys.argv) > 2 else "output"

    # Verificar se pasta de input existe
    if not os.path.isdir(input_folder):
        print(f"Erro: A pasta de entrada '{input_folder}' não existe.")
        return

    # Criar pasta de output se não existir
    os.makedirs(output_folder, exist_ok=True)
    print(f"--- A ler de: '{input_folder}' | A escrever em: '{output_folder}' ---\n")

    # Iterar sobre os ficheiros
    ficheiros_processados = 0
    for nome_ficheiro in os.listdir(input_folder):
        caminho_completo = os.path.join(input_folder, nome_ficheiro)
        
        # Ignorar subpastas, processar apenas ficheiros
        if os.path.isfile(caminho_completo):
            # Opcional: Filtrar extensão (ex: apenas .txt ou .pas)
            # if not nome_ficheiro.endswith('.txt'): continue
            
            processar_ficheiro(caminho_completo, output_folder)
            ficheiros_processados += 1

    print(f"\n--- Concluído: {ficheiros_processados} ficheiros processados. ---")

if __name__ == "__main__":
    main()