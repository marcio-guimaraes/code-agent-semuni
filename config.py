import os

# Configurações do LLM
MODEL = 'llama3.1:8b'

# Configurações de Diretórios e Contexto
DIRETORIO_TRABALHO = os.path.dirname(os.path.abspath(__file__))
IGNORAR_PASTAS = {'.git', '__pycache__', 'node_modules', 'venv', '.venv', '.idea', '.vscode'}
ARQUIVO_ESTRUTURA = 'ESTRUTURA_PROJETO.md'
ARQUIVO_CONTEXTO = 'contexto.txt'

