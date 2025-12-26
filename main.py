import sys
import os
from lexer import lexer
from parser import parser
from semantica import analisador_semantico, tabela
from codeGen import geracao_codigo, endereco, label_counter, reset_label

def processar_ficheiro(caminho_input, pasta_output):
    nome_ficheiro = os.path.basename(caminho_input)
    print(f"--> A processar: {nome_ficheiro}")
    
    try:
        with open(caminho_input, 'r', encoding='utf-8') as f:
            conteudo = f.read()
    except Exception as e:
        print(f"Erro ao ler '{nome_ficheiro}': {e}")
        return

    lexer.lineno = 1
    tabela.clear()
    endereco.clear()
    reset_label()

    try:
        arvore = parser.parse(conteudo, lexer=lexer)
    except Exception as e:
        print(f"Erro fatal no parser para '{nome_ficheiro}': {e}")
        return

    if not arvore:
        print(f"Aviso: Árvore vazia ou erro de sintaxe em '{nome_ficheiro}'.")
        return

    analisador_semantico(arvore)
    
    nome_base, _ = os.path.splitext(nome_ficheiro)
    nome_output = nome_base + ".vm"
    caminho_output = os.path.join(pasta_output, nome_output)

    idx = 0
    for nome_var in tabela:
        endereco[nome_var] = idx
        idx += 1

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
    if len(sys.argv) < 2:
        print("Uso: python main.py <pasta_input> pasta_output (opcional)")
        return

    input_folder = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else "output"

    if not os.path.isdir(input_folder):
        print(f"Erro: A pasta de entrada '{input_folder}' não existe.")
        return

    os.makedirs(output_folder, exist_ok=True)
    print(f"--- A ler de: '{input_folder}' | A escrever em: '{output_folder}' ---\n")

    ficheiros_processados = 0
    for nome_ficheiro in os.listdir(input_folder):
        caminho_completo = os.path.join(input_folder, nome_ficheiro)
        
        if os.path.isfile(caminho_completo):
            processar_ficheiro(caminho_completo, output_folder)
            ficheiros_processados += 1

    print(f"\n--- Concluído: {ficheiros_processados} ficheiros processados. ---")

if __name__ == "__main__":
    main()