import os
import json
import config

def resolver_caminho(caminho: str) -> str:
    if os.path.isabs(caminho):
        return caminho
    return os.path.join(config.DIRETORIO_TRABALHO, caminho)

def listar_arquivos(diretorio: str) -> str:
    try:
        return "\n".join(os.listdir(resolver_caminho(diretorio)))
    except Exception as e:
        return f"ERRO: Não foi possível listar arquivos no diretório '{diretorio}'. Detalhes: {str(e)}"

def ler_arquivo(caminho: str) -> str:
    try:
        with open(resolver_caminho(caminho), "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"ERRO: Não foi possível ler o arquivo '{caminho}'. Detalhes: {str(e)}"

def escrever_arquivo(caminho: str, conteudo: str) -> str:
    try:
        caminho_resolvido = resolver_caminho(caminho)
        diretorio_pai = os.path.dirname(caminho_resolvido)
        os.makedirs(diretorio_pai, exist_ok=True)

        with open(caminho_resolvido, "w", encoding="utf-8") as f:
            f.write(conteudo)
        return "Arquivo atualizado com sucesso."
    except Exception as e:
        return f"ERRO: Falha ao escrever no arquivo '{caminho}'. Detalhes: {str(e)}"

def substituir_no_arquivo(caminho: str, texto_antigo: str, texto_novo: str) -> str:
    try:
        caminho_resolvido = resolver_caminho(caminho)
        with open(caminho_resolvido, "r", encoding="utf-8") as f:
            conteudo = f.read()

        ocorrencias = conteudo.count(texto_antigo)

        if ocorrencias == 0:
            return f"ERRO: O texto solicitado não foi encontrado no arquivo '{caminho}'."

        if ocorrencias > 1:
            return (
                f"ERRO: O texto fornecido aparece {ocorrencias} vezes no arquivo '{caminho}'. "
                f"Forneça um trecho mais especifico (com mais contexto ao redor) para identificar "
                f"exatamente qual ocorrencia deve ser substituida."
            )

        novo_conteudo = conteudo.replace(texto_antigo, texto_novo, 1)

        with open(caminho_resolvido, "w", encoding="utf-8") as f:
            f.write(novo_conteudo)

        return "Substituição realizada com sucesso."
    except Exception as e:
        return f"ERRO: Falha ao substituir texto no arquivo '{caminho}'. Detalhes: {str(e)}"


def inserir_no_arquivo(caminho: str, conteudo: str) -> str:
    try:
        caminho_resolvido = resolver_caminho(caminho)
        with open(caminho_resolvido, "a", encoding="utf-8") as f:
            f.write(conteudo)
        return "Conteúdo inserido com sucesso ao final do arquivo."
    except Exception as e:
        return f"ERRO: Falha ao inserir conteúdo no arquivo '{caminho}'. Detalhes: {str(e)}"


def deletar_arquivo(caminho: str) -> str:
    try:
        caminho_resolvido = resolver_caminho(caminho)
        if not os.path.isfile(caminho_resolvido):
            return f"ERRO: O arquivo '{caminho}' não existe."
        os.remove(caminho_resolvido)
        return f"Arquivo '{caminho}' deletado com sucesso."
    except Exception as e:
        return f"ERRO: Falha ao deletar o arquivo '{caminho}'. Detalhes: {str(e)}"


# descrever aqui as ferramentas que o modelo pode chamar.
ferramentas = []

FERRAMENTAS_VALIDAS = {f['function']['name'] for f in ferramentas}


def gerar_arvore_projeto(diretorio_raiz: str) -> str:
    """Percorre o projeto recursivamente e monta uma árvore de pastas/arquivos
    em texto, ignorando pastas de ruído (.git, __pycache__, venv, etc.)."""
    linhas = [os.path.basename(diretorio_raiz) + '/']
    for raiz, pastas, arquivos in os.walk(diretorio_raiz):
        pastas[:] = sorted(p for p in pastas if p not in config.IGNORAR_PASTAS and not p.startswith('.'))
        rel = os.path.relpath(raiz, diretorio_raiz)
        nivel = 0 if rel == '.' else rel.count(os.sep) + 1
        prefixo = '    ' * nivel
        if rel != '.':
            linhas.append(f'{prefixo}{os.path.basename(raiz)}/')
        for arquivo in sorted(arquivos):
            if rel == '.' and arquivo in (config.ARQUIVO_ESTRUTURA, config.ARQUIVO_CONTEXTO):
                continue  # não lista arquivos gerados pelo agente
            prefixo_arquivo = '    ' * (nivel + (0 if rel == '.' else 1))
            linhas.append(f'{prefixo_arquivo}{arquivo}')
    return '\n'.join(linhas)


def gerar_contexto(diretorio_raiz: str) -> str:
    # gerar e salvar o contexto do projeto.
    raise NotImplementedError


def atualizar_estrutura_projeto() -> str:
    """Gera a árvore atual do projeto, salva em ESTRUTURA_PROJETO.md e
    retorna o texto da árvore para uso no system prompt."""
    arvore = gerar_arvore_projeto(config.DIRETORIO_TRABALHO)
    conteudo = (
        '# Estrutura do projeto\n\n'
        'Gerado automaticamente pelo agente. Esta é a lista REAL de arquivos e pastas '
        'no momento da geração — não invente nomes que não estejam aqui.\n\n'
        f'```\n{arvore}\n```\n'
    )
    try:
        with open(resolver_caminho(config.ARQUIVO_ESTRUTURA), 'w', encoding='utf-8') as f:
            f.write(conteudo)
    except Exception:
        pass  # se não conseguir salvar em disco, ainda usamos a árvore em memória
    return arvore


def atualizar_contexto() -> None:
    gerar_contexto(config.DIRETORIO_TRABALHO)


def ler_contexto() -> str:
    try:
        with open(resolver_caminho(config.ARQUIVO_CONTEXTO), 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return ''


def executar_ferramenta(nome_funcao: str, args: dict) -> str:
    # TODO: encaminhar o nome da ferramenta para a função correspondente.
    raise NotImplementedError
