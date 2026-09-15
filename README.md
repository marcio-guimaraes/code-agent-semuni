# code-agent-semuni

## Definição

### Modelo Utilizado
* **Nome:** Llama 3.1 (8B Parâmetros)
* **Comando de execução:** `ollama run llama3.1:8b`
* **Arquitetura:** LLM focado em execução local.
* **Motivo da escolha:** Melhor capacidade de raciocínio lógico e suporte a ferramentas (Function Calling) mais robusto e consistente em relação à versão 3.2 (3B), evitando alucinações e loops infinitos.

## Roadmap do Agente (Tasks)

### 🗂️ Fase 1: Ferramentas de Sistema de Arquivos (CRUD Completo)
- [x] **Interação básica com o sistema (I/O):** Agente consegue conversar, ler e escrever arquivos.
- [x] **[#1] Task 1.1a - Substituição Cirúrgica:** Implementar `substituir_no_arquivo(caminho, texto_antigo, texto_novo)` para alterar trechos específicos sem sobrescrever o arquivo inteiro.
- [ ] **[#2] Task 1.1b - Inserção / Append:** Implementar `inserir_no_arquivo(caminho, conteudo)` para adicionar código ao final do arquivo sem apagar o conteúdo existente.
- [ ] **[#3] Task 1.2 - Criação Segura:** Modificar `escrever_arquivo` para criar diretórios pai automaticamente com `os.makedirs`.
- [ ] **[#4] Task 1.3 - Exclusão:** Criar ferramenta `deletar_arquivo` (`os.remove`) e registrá-la no LLM.

### 🧠 Fase 2: Memória e Consciência de Contexto
- [x] **[#5] Task 2.1 - Gerador de Mapa (`contexto.txt`):** Função que varre os diretórios (ignorando `.git`, `__pycache__`, etc.) e gera uma árvore do projeto.
- [x] **[#6] Task 2.2 - Injeção de Contexto:** Ler `contexto.txt` no início da execução e injetar no `system prompt` para o LLM conhecer a arquitetura antes de agir.
- [x] **[#7] Task 2.3 - Atualização Automática do Contexto:** Regenerar `contexto.txt` automaticamente após qualquer operação de criação, escrita ou exclusão de arquivos.

### 🏗️ Fase 3: Refatoração e Arquitetura do Código
- [ ] **[#8] Task 3.1a - Extrair Ferramentas:** Mover todas as funções de ferramentas e suas definições JSON para `tools.py`.
- [ ] **[#9] Task 3.1b - Extrair Configuração:** Mover system prompt, nome do modelo e constantes para `config.py`.
- [ ] **[#10] Task 3.1c - Loop Principal Limpo:** Refatorar `agente.py` para conter apenas o loop de conversa, importando de `tools.py` e `config.py`.
- [ ] **[#11] Task 3.2 - Tratamento de Erros:** Padronizar retorno de erros das ferramentas para que o LLM consiga interpretar e corrigir sozinho.

### Fase 4: Segurança e UX — EXTRA
- [x] **[#12] Task 4.1 - Human-in-the-loop:** Solicitar confirmação `(s/n)` no terminal antes de ações destrutivas (sobrescrever ou deletar arquivos).
- [ ] **[#13] Task 4.2 - Sandboxing:** Validar caminhos de arquivos para impedir que o agente altere arquivos fora do diretório do projeto (Path Traversal).
- [ ] **[#14] Task 4.3 - Logging:** Registrar em `agent.log` toda ação executada pelo agente (ferramenta chamada, argumentos, resultado) para facilitar debug.
