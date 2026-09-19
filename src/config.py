import os
import sys

# Configurações do LLM
MODEL = 'llama3.1:8b'

# ==============================================================================
# DEFINIÇÃO DINÂMICA DO LOCAL DE TRABALHO
# Permite rodar o agente em qualquer projeto passando o caminho como argumento
# Ex: python src/agente.py "C:\Users\User\Desktop\outro-projeto"
# ==============================================================================
if len(sys.argv) > 1:
    alvo = sys.argv[1]
    # Se passou um caminho absoluto, usa ele. Se for relativo, resolve para o absoluto.
    DIRETORIO_TRABALHO = alvo if os.path.isabs(alvo) else os.path.abspath(alvo)
else:
    # Se não passar nada, trabalha no diretório de onde o usuário chamou o script no terminal
    DIRETORIO_TRABALHO = os.getcwd()

# Configurações de Contexto e Arquivos ignorados
IGNORAR_PASTAS = {'.git', '__pycache__', 'node_modules', 'venv', '.venv', '.idea', '.vscode', 'src'}
ARQUIVO_ESTRUTURA = 'ESTRUTURA_PROJETO.md'
ARQUIVO_CONTEXTO = 'contexto.txt'
