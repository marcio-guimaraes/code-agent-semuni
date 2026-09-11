import os
import json
import re
import sys
import ollama

sys.stdout.reconfigure(encoding='utf-8')

MODEL = 'llama3.1:8b'

def resolver_caminho(caminho: str) -> str:
    if os.path.isabs(caminho):
        return caminho
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), caminho)

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
        with open(resolver_caminho(caminho), "w", encoding="utf-8") as f:
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
            'description': 'Sobrescreve um arquivo com novo conteudo completo. Use quando o usuario pedir para criar ou reescrever um arquivo inteiro.',
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
    }
]

FERRAMENTAS_VALIDAS = {f['function']['name'] for f in ferramentas}

DIRETORIO_TRABALHO = os.path.dirname(os.path.abspath(__file__))

IGNORAR_PASTAS = {'.git', '__pycache__', 'node_modules', 'venv', '.venv', '.idea', '.vscode'}
ARQUIVO_ESTRUTURA = 'ESTRUTURA_PROJETO.md'
ARQUIVO_CONTEXTO = 'contexto.txt'


def gerar_arvore_projeto(diretorio_raiz: str) -> str:
    """Percorre o projeto recursivamente e monta uma árvore de pastas/arquivos
    em texto, ignorando pastas de ruído (.git, __pycache__, venv, etc.)."""
    linhas = [os.path.basename(diretorio_raiz) + '/']
    for raiz, pastas, arquivos in os.walk(diretorio_raiz):
        pastas[:] = sorted(p for p in pastas if p not in IGNORAR_PASTAS and not p.startswith('.'))
        rel = os.path.relpath(raiz, diretorio_raiz)
        nivel = 0 if rel == '.' else rel.count(os.sep) + 1
        prefixo = '    ' * nivel
        if rel != '.':
            linhas.append(f'{prefixo}{os.path.basename(raiz)}/')
        for arquivo in sorted(arquivos):
            if rel == '.' and arquivo == ARQUIVO_ESTRUTURA:
                continue  # não lista o próprio arquivo de estrutura
            prefixo_arquivo = '    ' * (nivel + (0 if rel == '.' else 1))
            linhas.append(f'{prefixo_arquivo}{arquivo}')
    return '\n'.join(linhas)


def atualizar_estrutura_projeto() -> str:
    """Gera a árvore atual do projeto, salva em ESTRUTURA_PROJETO.md e
    retorna o texto da árvore para uso no system prompt."""
    arvore = gerar_arvore_projeto(DIRETORIO_TRABALHO)
    conteudo = (
        '# Estrutura do projeto\n\n'
        'Gerado automaticamente pelo agente. Esta é a lista REAL de arquivos e pastas '
        'no momento da geração — não invente nomes que não estejam aqui.\n\n'
        f'```\n{arvore}\n```\n'
    )
    try:
        with open(resolver_caminho(ARQUIVO_ESTRUTURA), 'w', encoding='utf-8') as f:
            f.write(conteudo)
    except Exception:
        pass  # se não conseguir salvar em disco, ainda usamos a árvore em memória
    return arvore


def ler_contexto() -> str:
    try:
        with open(resolver_caminho(ARQUIVO_CONTEXTO), 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return ''


def montar_system_prompt() -> str:
    arvore = atualizar_estrutura_projeto()
    contexto = ler_contexto()
    contexto_prompt = ' '
    if contexto:
        contexto_prompt = (f'\n\nContexto adicional do projeto (arquivo {ARQUIVO_CONTEXTO}):\n' f'{contexto}\n' )
    return (
        f'Voce e um assistente de IA com ferramentas locais de sistema de arquivos.\n'
        f'Diretorio raiz do projeto: {DIRETORIO_TRABALHO}\n'
        f'\n'
        f'Esta e a estrutura REAL e completa do projeto (pastas e arquivos), tambem salva '
        f'em {ARQUIVO_ESTRUTURA}:\n'
        f'```\n{arvore}\n```\n'
        f'\n'
        f'REGRA VITAL: VOCE E CEGO PARA O CONTEUDO DE ARQUIVOS ATE USAR A FERRAMENTA ler_arquivo. '
        f'Nunca adivinhe, simule ou finja saber o conteudo de um arquivo antes de chamar a '
        f'ferramenta correspondente e receber a resposta.\n'
        f'\n'
        f'REGRA CRITICA SOBRE NOMES DE ARQUIVO: NUNCA invente ou chute um nome de arquivo ou pasta '
        f'que nao esteja na estrutura acima. Se o usuario se referir a um arquivo de forma vaga '
        f'(ex: "o arquivo do projeto", "o app", "o codigo"), escolha o item mais provavel dentre os '
        f'listados na estrutura (por exemplo, app.py). Se houver mais de uma opcao plausivel ou nenhuma '
        f'corresponder, NAO chame nenhuma ferramenta: pergunte ao usuario qual arquivo ele quer, '
        f'citando os nomes reais da estrutura.\n'
        f'\n'
        f'REGRAS GERAIS:\n'
        f'1. Para saudacoes (oi, ola) ou perguntas gerais, APENAS escreva a resposta em texto. NAO chame ferramentas.\n'
        f'2. NUNCA tente ler, listar, escrever ou editar arquivos a menos que o usuario peca explicitamente.\n'
        f'3. "listar_arquivos" recebe uma PASTA. "ler_arquivo" recebe um ARQUIVO. Nunca use uma no lugar da outra.\n'
        f'4. Caminhos relativos devem ser resolvidos usando o diretorio raiz do projeto como base.\n'
        f'5. Quando precisar usar uma ferramenta, SEMPRE use o mecanismo nativo de tool calling. '
        f'Nunca escreva o JSON da chamada como texto normal na resposta.'
        f'{contexto_prompt}'
    )


def extrair_tool_call_do_texto(texto: str) -> dict | None:
    """Fallback: alguns modelos pequenos às vezes escrevem a tool call como
    JSON solto no texto em vez de usar o tool calling nativo. Tentamos
    recuperar esse caso aqui."""
    if not texto:
        return None
    match = re.search(r'\{.*\}', texto.strip(), re.DOTALL)
    if not match:
        return None
    json_str = match.group(0)
    # Corrige barras invertidas de caminhos Windows que quebrariam o JSON
    json_str = re.sub(r'\\(?![/"\\bfnrtu])', r'\\\\', json_str)
    try:
        dados = json.loads(json_str)
        if 'name' in dados and 'parameters' in dados:
            return dados
    except (json.JSONDecodeError, ValueError):
        pass
    return None


def executar_ferramenta(nome_funcao: str, args: dict) -> str:
    if nome_funcao == 'listar_arquivos':
        return listar_arquivos(args['diretorio'])
    elif nome_funcao == 'ler_arquivo':
        return ler_arquivo(args['caminho'])
    elif nome_funcao == 'escrever_arquivo':
        resultado = escrever_arquivo(args['caminho'], args['conteudo'])
        print(f"[{args['caminho']} foi atualizado pelo agente]")
        atualizar_estrutura_projeto()  # pode ter criado um arquivo novo
        return resultado
    elif nome_funcao == 'substituir_no_arquivo':
        resultado = substituir_no_arquivo(args['caminho'], args['texto_antigo'], args['texto_novo'])
        print(f"[{args['caminho']} foi atualizado pelo agente]")
        return resultado
    elif nome_funcao == 'inserir_no_arquivo':
        resultado = inserir_no_arquivo(args['caminho'], args['conteudo'])
        print(f"[{args['caminho']} foi atualizado pelo agente]")
        atualizar_estrutura_projeto()  # pode ter criado um arquivo novo
        return resultado
    return "Ferramenta desconhecida."


def pedir_autorizacao(nome_ferramenta: str, args_ferramenta) -> bool:
    print(f"\n[Ação do Agente]")
    print(f"   Ferramenta: {nome_ferramenta}")
    print(f"   Argumentos: {args_ferramenta}")
    autorizado = input("   Permitir execução? (s/n): ").strip().lower()
    if autorizado != 's':
        print("   [Ação cancelada]")
    return autorizado == 's'


def processar_turno(mensagens: list, max_rodadas: int = 6) -> None:
    """Loop do agente: repete enquanto o modelo pedir ferramentas (nativas ou
    em texto), até ele dar uma resposta final sem tool call."""
    for _ in range(max_rodadas):
        resposta = ollama.chat(
            model=MODEL,
            messages=mensagens,
            tools=ferramentas
        )
        msg = resposta.message
        conteudo = msg.content or ""

        chamadas = []
        if msg.tool_calls:
            for t in msg.tool_calls:
                chamadas.append((t.function.name, t.function.arguments))
        else:
            tool_call_textual = extrair_tool_call_do_texto(conteudo)
            if tool_call_textual:
                chamadas.append((tool_call_textual['name'], tool_call_textual['parameters']))

        if not chamadas:
            # resposta final de verdade, sem pedido de ferramenta
            mensagens.append(msg)
            print("\nAgente:", conteudo)
            return

        mensagens.append(msg)

        for nome_ferramenta, args_ferramenta in chamadas:
            if nome_ferramenta not in FERRAMENTAS_VALIDAS:
                resultado = f"Erro: A ferramenta '{nome_ferramenta}' nao existe."
            elif pedir_autorizacao(nome_ferramenta, args_ferramenta):
                resultado = executar_ferramenta(nome_ferramenta, args_ferramenta)
            else:
                resultado = "Aviso: O usuário negou permissão para executar esta ferramenta. Continue a conversa informando que você não tem permissão."

            mensagens.append({
                'role': 'tool',
                'content': resultado,
                'name': nome_ferramenta
            })
            if nome_ferramenta in ('escrever_arquivo', 'inserir_no_arquivo') and mensagens and mensagens[0]['role'] == 'system':
                mensagens[0]['content'] = montar_system_prompt()
        # volta ao topo do for para o modelo ver o resultado da tool e responder de novo

    print("\nAgente: (número máximo de rodadas de ferramentas atingido nesta interação)")


def main():
    print("Agente iniciado! Converse normalmente ou peça para editar arquivos. Digite 'sair' para encerrar.")

    mensagens = [
        {'role': 'system', 'content': montar_system_prompt()}
    ]

    while True:
        pedido = input("\nVocê: ")
        if pedido.lower() == 'sair':
            break

        mensagens.append({'role': 'user', 'content': pedido})
        processar_turno(mensagens)


if __name__ == '__main__':
    main()