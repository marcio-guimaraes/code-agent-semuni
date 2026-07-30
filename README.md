# code-agent-semuni

## Definição

### Modelo Utilizado
* **Nome:** Llama 3.2 (3B Parâmetros)
* **Comando de execução:** `ollama run llama3.2`
* **Arquitetura:** SLM (Small Language Model) focado em execução local.
* **Motivo da escolha:** Baixo consumo de hardware (roda sem GPU dedicada) e suporte nativo a Function Calling, permitindo ao agente executar ferramentas locais.

## Roadmap do Agente (Tasks)

- [x] **1. Interação básica com o sistema (I/O):** Agente consegue conversar com o usuário, ler e escrever arquivos de código de forma autônoma.
- [ ] **2. Corrigir a "amnésia" de código:** Melhorar a edição de arquivos para que o agente não apague o código existente. (Implementar edição inteligente ou modo append `a`).
- [ ] **3. Criação de arquivos:** Garantir que a ferramenta de escrita consiga criar arquivos do zero em diretórios específicos.
- [ ] **4. Exclusão de arquivos:** Criar uma nova ferramenta que dê ao agente a capacidade de deletar arquivos obsoletos.
- [ ] **5. Mapeamento de Contexto do Repositório:** Implementar um sistema onde o agente lê os arquivos do projeto e gera um arquivo `contexto.txt` (um mapa do repositório). O agente usará esse arquivo para saber a arquitetura do projeto e onde deve mexer antes de executar uma ação.