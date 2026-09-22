import os
import json
import re
import sys
import ollama

import config
import tools

sys.stdout.reconfigure(encoding='utf-8')

MODEL = config.MODEL


def montar_system_prompt() -> str:
    arvore = tools.atualizar_estrutura_projeto()
    contexto = tools.ler_contexto()
    contexto_prompt = ' '
    if contexto:
        contexto_prompt = (f'\n\nContexto adicional do projeto (arquivo {config.ARQUIVO_CONTEXTO}):\n' f'{contexto}\n')
    return (
        f'Voce e um assistente de IA com ferramentas locais de sistema de arquivos.\n'
        f'Diretorio raiz do projeto: {config.DIRETORIO_TRABALHO}\n'
        f'\n'
        f'Esta e a estrutura REAL e completa do projeto, tambem salva em '
        f'{config.ARQUIVO_ESTRUTURA}:\n'
        f'```\n{arvore}\n```\n'
        f'\n'
        f'REGRA VITAL: VOCE E CEGO PARA O CONTEUDO DE ARQUIVOS ATE USAR a ferramenta '
        f'ler_arquivo. Nunca adivinhe, simule ou finja saber o conteudo de um arquivo.\n'
        f'\n'
        f'REGRAS GERAIS:\n'
        f'1. Para saudacoes ou perguntas gerais, responda apenas em texto.\n'
        f'2. NUNCA tente ler, listar, escrever ou editar arquivos sem um pedido explicito.\n'
        f'3. "listar_arquivos" recebe uma PASTA e "ler_arquivo" recebe um ARQUIVO.\n'
        f'4. Caminhos relativos usam o diretorio raiz do projeto como base.\n'
        f'5. Use sempre o mecanismo nativo de tool calling quando precisar de uma ferramenta. '
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


def pedir_autorizacao(nome_ferramenta: str, args_ferramenta) -> bool:
    print(f"\n[Ação do Agente]")
    print(f"   Ferramenta: {nome_ferramenta}")
    print(f"   Argumentos: {args_ferramenta}")
    autorizado = input("   Permitir execução? (s/n): ").strip().lower()
    if autorizado != 's':
        print("   [Ação cancelada]")
    return autorizado == 's'


def processar_turno(mensagens: list, max_rodadas: int = 6) -> None:
    """Repete a conversa enquanto o modelo solicitar ferramentas."""
    for _ in range(max_rodadas):
        resposta = ollama.chat(
            model=MODEL,
            messages=mensagens,
            tools=tools.ferramentas
        )
        msg = resposta.message
        conteudo = msg.content or ''

        chamadas = []
        if msg.tool_calls:
            for chamada in msg.tool_calls:
                chamadas.append((chamada.function.name, chamada.function.arguments))
        else:
            chamada_textual = extrair_tool_call_do_texto(conteudo)
            if chamada_textual:
                chamadas.append((chamada_textual['name'], chamada_textual['parameters']))

        if not chamadas:
            mensagens.append(msg)
            print('\nAgente:', conteudo)
            return

        mensagens.append(msg)

        for nome_ferramenta, args_ferramenta in chamadas:
            if nome_ferramenta not in tools.FERRAMENTAS_VALIDAS:
                resultado = f"Erro: A ferramenta '{nome_ferramenta}' nao existe."
            elif pedir_autorizacao(nome_ferramenta, args_ferramenta):
                resultado = tools.executar_ferramenta(nome_ferramenta, args_ferramenta)
            else:
                resultado = 'Aviso: O usuario negou permissao para executar esta ferramenta.'

            mensagens.append({
                'role': 'tool',
                'content': resultado,
                'name': nome_ferramenta
            })

            if nome_ferramenta in ('escrever_arquivo', 'inserir_no_arquivo', 'deletar_arquivo', 'substituir_no_arquivo'):
                if mensagens and mensagens[0]['role'] == 'system':
                    mensagens[0]['content'] = montar_system_prompt()

    print('\nAgente: (numero maximo de rodadas de ferramentas atingido nesta interacao)')


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
