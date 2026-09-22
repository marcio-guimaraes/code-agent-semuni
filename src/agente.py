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
    # montar o system prompt com a estrutura e o contexto do projeto.
    raise NotImplementedError


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
    # chamar o modelo, processar tool calls e devolver a resposta final.
    raise NotImplementedError


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
