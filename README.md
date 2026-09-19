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
- [x] **[#1]** Implementar ferramenta substituir_no_arquivo
- [x] **[#2]** Implementar ferramenta inserir_no_arquivo
- [x] **[#3]** Adicionar criacao automatica de diretorios em escrever_arquivo
- [x] **[#4]** Criar ferramenta deletar_arquivo

### 🧠 Fase 2: Memória e Consciência de Contexto
- [x] **[#5]** Implementar gerador de contexto.txt (mapa do projeto)
- [x] **[#6]** Injetar contexto.txt no system prompt do agente
- [x] **[#7]** Regenerar contexto.txt apos operacoes de escrita/criacao/exclusao

### 🏗️ Fase 3: Refatoração e Arquitetura do Código
- [x] **[#8]** Mover funcoes de ferramentas e definicoes JSON para tools.py
- [x] **[#9]** Centralizar configuracoes em config.py
- [x] **[#10]** Limpar agente.py para conter apenas o loop de conversa
- [ ] **[#11]** Padronizar retorno de erros para o LLM interpretar

### Fase 4: Segurança e UX — EXTRA
- [ ] **[#12]** [DESAFIO] Implementar human-in-the-loop para acoes destrutivas
- [ ] **[#13]** [DESAFIO] Implementar validacao de path traversal (sandboxing)
- [ ] **[#14]** [DESAFIO] Criar sistema de logging em agent.log
