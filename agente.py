import os
import ollama

def listar_arquivos(diretorio: str) -> str:
    try:
        return "\n".join(os.listdir(diretorio))
    except Exception as e:
        return str(e)

def ler_arquivo(caminho: str) -> str:
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return str(e)

def escrever_arquivo(caminho: str, conteudo: str) -> str:
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(conteudo)
        return "Arquivo atualizado com sucesso."
    except Exception as e:
        return str(e)

ferramentas = [
    {
        'type': 'function',
        'function': {
            'name': 'listar_arquivos',
            'description': 'Lista os arquivos em um diretorio',
            'parameters': {
                'type': 'object',
                'properties': {
                    'diretorio': {'type': 'string', 'description': 'Caminho do diretorio'}
                },
                'required': ['diretorio']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'ler_arquivo',
            'description': 'Le o conteudo de um arquivo',
            'parameters': {
                'type': 'object',
                'properties': {
                    'caminho': {'type': 'string', 'description': 'Caminho do arquivo'}
                },
                'required': ['caminho']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'escrever_arquivo',
            'description': 'Sobrescreve um arquivo com novo conteudo',
            'parameters': {
                'type': 'object',
                'properties': {
                    'caminho': {'type': 'string', 'description': 'Caminho do arquivo'},
                    'conteudo': {'type': 'string', 'description': 'Novo codigo'}
                },
                'required': ['caminho', 'conteudo']
            }
        }
    }
]

print("Agente iniciado! Converse normalmente ou peca para editar arquivos. Digite 'sair' para encerrar.")

mensagens = [
    {
        'role': 'system',
        'content': 'Voce e um assistente de IA conversacional. Converse normalmente com o usuario. Apenas utilize as ferramentas de listar, ler ou escrever arquivos quando o usuario pedir de forma explicita.'
    }
]

while True:
    pedido = input("\nVocê: ")
    if pedido.lower() == 'sair':
        break
        
    mensagens.append({'role': 'user', 'content': pedido})

    resposta_inicial = ollama.chat(
        model='llama3.2',
        messages=mensagens,
        tools=ferramentas
    )

    if resposta_inicial.message.tool_calls:
        mensagens.append(resposta_inicial.message)
        
        for tool in resposta_inicial.message.tool_calls:
            nome_funcao = tool.function.name
            args = tool.function.arguments
            
            if nome_funcao == 'listar_arquivos':
                resultado = listar_arquivos(args['diretorio'])
            elif nome_funcao == 'ler_arquivo':
                resultado = ler_arquivo(args['caminho'])
            elif nome_funcao == 'escrever_arquivo':
                resultado = escrever_arquivo(args['caminho'], args['conteudo'])
                print(f"[{args['caminho']} foi atualizado pelo agente]")
            else:
                resultado = "Ferramenta desconhecida."
                
            mensagens.append({
                'role': 'tool',
                'content': resultado,
                'name': nome_funcao
            })
        
        resposta_final = ollama.chat(
            model='llama3.2',
            messages=mensagens
        )
        print("\nAgente:", resposta_final.message.content)
        mensagens.append(resposta_final.message)
    else:
        print("\nAgente:", resposta_inicial.message.content)
        mensagens.append(resposta_inicial.message)