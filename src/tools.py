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
        return str(e)

def ler_arquivo(caminho: str) -> str:
    try:
        with open(resolver_caminho(caminho), "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return str(e)

def escrever_arquivo(caminho: str, conteudo: str) -> str:
    try:
        caminho_resolvido = resolver_caminho(caminho)
        diretorio_pai = os.path.dirname(caminho_resolvido)
        os.makedirs(diretorio_pai, exist_ok=True)

        with open(caminho_resolvido, "w", encoding="utf-8") as f:
            f.write(conteudo)
        return "Arquivo atualizado com sucesso."
    except Exception as e:
        return str(e)

def substituir_no_arquivo(caminho: str, texto_antigo: str, texto_novo: str) -> str:
    try:
        caminho_resolvido = resolver_caminho(caminho)
        with open(caminho_resolvido, "r", encoding="utf-8") as f:
            conteudo = f.read()

        ocorrencias = conteudo.count(texto_antigo)

        if ocorrencias == 0:
            return f"Erro: o texto '{texto_antigo}' não foi encontrado no arquivo '{caminho}'."

        if ocorrencias > 1:
            return (
                f"Erro: o texto '{texto_antigo}' aparece {ocorrencias} vezes no arquivo '{caminho}'. "
                f"Forneça um trecho mais especifico (com mais contexto ao redor) para identificar "
                f"exatamente qual ocorrencia deve ser substituida."
            )

        novo_conteudo = conteudo.replace(texto_antigo, texto_novo, 1)

        with open(caminho_resolvido, "w", encoding="utf-8") as f:
            f.write(novo_conteudo)

        return "Substituição realizada com sucesso."
    except Exception as e:
        return str(e)


def inserir_no_arquivo(caminho: str, conteudo: str) -> str:
    try:
        caminho_resolvido = resolver_caminho(caminho)
        with open(caminho_resolvido, "a", encoding="utf-8") as f:
            f.write(conteudo)
        return "Conteúdo inserido com sucesso ao final do arquivo."
    except Exception as e:
        return str(e)


def deletar_arquivo(caminho: str) -> str:
    try:
        caminho_resolvido = resolver_caminho(caminho)
        if not os.path.isfile(caminho_resolvido):
            return f"Erro: o arquivo '{caminho}' não existe."
        os.remove(caminho_resolvido)
        return f"Arquivo '{caminho}' deletado com sucesso."
    except Exception as e:
        return str(e)


ferramentas = [
    {
        'type': 'function',
        'function': {
            'name': 'listar_arquivos',
            'description': 'Lista os arquivos e pastas em um DIRETORIO (nunca um arquivo). Use quando o usuario pedir para ver, listar ou conhecer os arquivos de uma pasta.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'diretorio': {'type': 'string', 'description': 'Caminho absoluto de um DIRETORIO (pasta), nunca de um arquivo, a ser listado'}
                },
                'required': ['diretorio']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'ler_arquivo',
            'description': 'Le e retorna o conteudo de um ARQUIVO especifico (nunca uma pasta). Use SEMPRE que o usuario pedir para ler, ver, abrir ou mostrar um arquivo. Nunca recuse esta acao.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'caminho': {'type': 'string', 'description': 'Caminho absoluto do ARQUIVO a ser lido'}
                },
                'required': ['caminho']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'escrever_arquivo',
            'description': 'Cria ou sobrescreve um arquivo com novo conteudo completo, criando diretorios pai automaticamente quando necessario.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'caminho': {'type': 'string', 'description': 'Caminho absoluto do arquivo'},
                    'conteudo': {'type': 'string', 'description': 'Conteudo completo a ser escrito no arquivo'}
                },
                'required': ['caminho', 'conteudo']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'substituir_no_arquivo',
            'description': 'Substitui um trecho de texto por outro dentro de um arquivo existente. Use para edicoes pontuais, sem reescrever o arquivo inteiro. O texto_antigo deve ser especifico o suficiente para aparecer apenas UMA VEZ no arquivo (inclua linhas de contexto ao redor se necessario) — se aparecer mais de uma vez, a ferramenta recusa a operacao.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'caminho': {'type': 'string', 'description': 'Caminho absoluto do arquivo'},
                    'texto_antigo': {'type': 'string', 'description': 'Trecho exato de texto a ser substituido'},
                    'texto_novo': {'type': 'string', 'description': 'Novo trecho de texto'}
                },
                'required': ['caminho', 'texto_antigo', 'texto_novo']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'inserir_no_arquivo',
            'description': 'Adiciona conteudo novo ao FINAL de um arquivo existente, sem apagar o conteudo atual. Use quando o usuario pedir para adicionar codigo novo (ex: uma funcao nova) a um arquivo, em vez de substituir algo que ja existe.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'caminho': {'type': 'string', 'description': 'Caminho absoluto do arquivo'},
                    'conteudo': {'type': 'string', 'description': 'Conteudo a ser adicionado ao final do arquivo'}
                },
                'required': ['caminho', 'conteudo']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'deletar_arquivo',
            'description': 'Exclui um arquivo existente. Use somente quando o usuario pedir explicitamente para excluir ou apagar um arquivo.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'caminho': {'type': 'string', 'description': 'Caminho absoluto do arquivo a ser excluido'}
                },
                'required': ['caminho']
            }
        }
    }
]

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
    arvore = gerar_arvore_projeto(diretorio_raiz)
    caminho_contexto = os.path.join(diretorio_raiz, config.ARQUIVO_CONTEXTO)
    try:
        with open(caminho_contexto, 'w', encoding='utf-8') as f:
            f.write(arvore + '\n')
    except Exception:
        pass
    return arvore


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
    if nome_funcao == 'listar_arquivos':
        return listar_arquivos(args['diretorio'])
    elif nome_funcao == 'ler_arquivo':
        return ler_arquivo(args['caminho'])
    elif nome_funcao == 'escrever_arquivo':
        resultado = escrever_arquivo(args['caminho'], args['conteudo'])
        print(f"[{args['caminho']} foi atualizado pelo agente]")
        if resultado == "Arquivo atualizado com sucesso.":
            atualizar_estrutura_projeto()
            atualizar_contexto()
        return resultado
    elif nome_funcao == 'substituir_no_arquivo':
        resultado = substituir_no_arquivo(args['caminho'], args['texto_antigo'], args['texto_novo'])
        print(f"[{args['caminho']} foi atualizado pelo agente]")
        if resultado == "Substituição realizada com sucesso.":
            atualizar_contexto()
        return resultado
    elif nome_funcao == 'inserir_no_arquivo':
        resultado = inserir_no_arquivo(args['caminho'], args['conteudo'])
        print(f"[{args['caminho']} foi atualizado pelo agente]")
        if resultado == "Conteúdo inserido com sucesso ao final do arquivo.":
            atualizar_estrutura_projeto()
            atualizar_contexto()
        return resultado
    elif nome_funcao == 'deletar_arquivo':
        resultado = deletar_arquivo(args['caminho'])
        print(f"[{args['caminho']} foi excluido pelo agente]")
        if "sucesso" in resultado:
            atualizar_estrutura_projeto()
            atualizar_contexto()
        return resultado
    return "Ferramenta desconhecida."

