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
        contexto_prompt = (f'\n\nContexto adicional do projeto (arquivo {config.ARQUIVO_CONTEXTO}):\n' f'{contexto}\n' )
    return (
        f'Voce e um assistente de IA com ferramentas locais de sistema de arquivos.\n'
        f'Diretorio raiz do projeto: {config.DIRETORIO_TRABALHO}\n'
        f'\n'
        f'Esta e a estrutura REAL e completa do projeto (pastas e arquivos), tambem salva '
        f'em {config.ARQUIVO_ESTRUTURA}:\n'
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
            tools=tools.ferramentas
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
            if nome_ferramenta not in tools.FERRAMENTAS_VALIDAS:
                resultado = f"Erro: A ferramenta '{nome_ferramenta}' nao existe."
            elif pedir_autorizacao(nome_ferramenta, args_ferramenta):
                resultado = tools.executar_ferramenta(nome_ferramenta, args_ferramenta)
            else:
                resultado = "Aviso: O usuário negou permissão para executar esta ferramenta. Continue a conversa informando que você não tem permissão."

            mensagens.append({
                'role': 'tool',
                'content': resultado,
                'name': nome_ferramenta
            })
            if nome_ferramenta in ('escrever_arquivo', 'inserir_no_arquivo', 'deletar_arquivo', 'substituir_no_arquivo') and mensagens and mensagens[0]['role'] == 'system':
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
