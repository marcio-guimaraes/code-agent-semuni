# Code Agent — Oficina de Agentes com Python e Ollama

Este repositório contém o projeto desenvolvido na oficina de criação de um
agente de IA com Python e Ollama. A proposta é mostrar, de forma prática e
incremental, como um modelo de linguagem conversa com um programa Python e
utiliza ferramentas para realizar ações no sistema de arquivos.

O projeto foi preparado para ser acompanhado durante a oficina: os alunos
clonam o repositório, implementam as etapas propostas e podem consultar a
versão completa na branch main.

## Tutorial da oficina

O passo a passo completo, incluindo a configuração do ambiente e a
implementação das fases, está disponível em:

- [Tutorial em PDF](https://drive.google.com/file/d/1kobYpYrliUvK63x8ufZsajVcxQuPbYY3/view?usp=sharing)

## O que o projeto demonstra

Ao final, o agente consegue:

- conversar com o usuário usando um modelo executado localmente;
- interpretar pedidos e decidir quando utilizar uma ferramenta;
- ler, criar, escrever, inserir, substituir e excluir arquivos;
- pedir autorização antes de ações que alteram o sistema de arquivos;
- gerar e utilizar um arquivo de contexto sobre a estrutura do projeto;
- devolver os resultados das ferramentas ao modelo para continuar a conversa.

O fluxo central é:

1. O usuário envia um pedido.
2. O modelo interpreta a intenção.
3. O modelo solicita uma ferramenta e seus argumentos.
4. O Python valida a solicitação e pode pedir autorização.
5. A ferramenta é executada.
6. O resultado retorna ao histórico da conversa.

## Organização do projeto

- app.py: ponto de entrada da aplicação.
- src/agente.py: coordena conversa, histórico e chamadas ao modelo.
- src/tools.py: implementa ferramentas e descrições para Function Calling.
- src/config.py: centraliza modelo, diretório de trabalho e configurações.
- contexto.txt: mapa gerado da estrutura do projeto, utilizado como contexto.

## Fases da oficina

O repositório possui branches que representam os momentos da implementação.

### Fase 1 — Ferramentas

Na branch Fase1-apresentacao, são trabalhados o fluxo básico do agente, o
conceito de prompt e a integração com ferramentas de leitura e escrita.

### Fase 2 — Contexto e Function Calling

Na branch Fase2-apresetancao (o nome contém intencionalmente essa grafia), a
implementação avança para descrições estruturadas de ferramentas, despacho das
funções, autorização e geração/injeção de contexto.

### Versão completa

A branch main reúne a implementação final, incluindo as fases anteriores,
refatorações e funcionalidades adicionais. Ela pode ser usada para consultar
o resultado ou recuperar uma implementação quando necessário.

## Como começar

### Clonar a versão completa

    git clone -b main https://github.com/marcio-guimaraes/code-agent-semuni.git
    cd code-agent-semuni

Para acompanhar a oficina desde o início, clone a branch da Fase 1:

    git clone -b Fase1-apresentacao https://github.com/marcio-guimaraes/code-agent-semuni.git
    cd code-agent-semuni

Depois, avance para a Fase 2:

    git fetch origin
    git switch Fase2-apresetancao

### Configurar o ambiente

Instale Python, Git e Ollama, crie um ambiente virtual e instale a biblioteca
Python do Ollama:

    python -m venv .venv

    # Linux/macOS
    source .venv/bin/activate

    # Windows PowerShell
    .venv\\Scripts\\Activate.ps1

    pip install ollama
    ollama pull llama3.1:8b

O modelo padrão é llama3.1:8b. Em computadores com menos recursos, é possível
usar llama3.2:3b, que consome menos memória, mas pode apresentar menor
desempenho em tarefas complexas.

Para executar:

    python app.py

Consulte o tutorial para ver os comandos completos de instalação no Windows e
no Linux.

## Roadmap

### Fase 1 — Ferramentas de sistema de arquivos

- [x] Interação básica com o sistema: conversar, ler e escrever arquivos.
- [x] Substituir conteúdo em arquivo.
- [x] Inserir conteúdo em arquivo.
- [x] Criar diretórios automaticamente ao escrever.
- [x] Excluir arquivos.

### Fase 2 — Memória e contexto

- [x] Gerar contexto.txt com o mapa do projeto.
- [x] Injetar o contexto no system prompt.
- [x] Regenerar o contexto após operações de escrita, criação ou exclusão.

### Fase 3 — Organização do código

- [x] Centralizar ferramentas em src/tools.py.
- [x] Centralizar configurações em src/config.py.
- [x] Separar o loop de conversa em src/agente.py.
- [x] Padronizar retornos de erro para o modelo.

### Fase 4 — Desafios extras

- [ ] Implementar autorização específica para ações destrutivas.
- [ ] Validar path traversal e reforçar o sandboxing.
- [ ] Criar um sistema de logging em agent.log.

## Modelo utilizado

O modelo padrão é o llama3.1:8b, executado localmente pelo Ollama:

    ollama run llama3.1:8b

O código também pode usar llama3.2:3b em máquinas com menos memória. A escolha
do modelo influencia a qualidade das decisões, a capacidade de seguir
instruções, o consumo de memória e a velocidade da execução.
