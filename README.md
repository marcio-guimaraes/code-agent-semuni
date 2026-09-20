# code-agent-semuni

## Definição

### Modelo Utilizado
* **Nome:** Llama 3.1 (8B Parâmetros)
* **Comando de execução:** `ollama run llama3.1:8b`
* **Arquitetura:** LLM focado em execução local.
* **Motivo da escolha:** Melhor capacidade de raciocínio lógico e suporte a ferramentas (Function Calling) mais robusto e consistente em relação à versão 3.2 (3B), evitando alucinações e loops infinitos.
* **Arquitetura:** LLM focado em execução local com suporte a Tool Calling.
* **Motivo da escolha:** Melhor capacidade de raciocínio lógico, recuperação de erros e suporte a ferramentas (Function Calling) em relação aos modelos concorrentes testados.

## Roadmap do Agente (Tasks)

### 🗂️ Fase 1: Ferramentas de Sistema de Arquivos (CRUD Completo)
- [x] **Interação básica com o sistema (I/O):** Agente consegue conversar, ler e escrever arquivos.
- [x] **[#1]** Implementar ferramenta substituir_no_arquivo
- [x] **[#2]** Implementar ferramenta inserir_no_arquivo
- [x] **[#3]** Adicionar criacao automatica de diretorios em escrever_arquivo
- [x] **[#3]** Adicionar criação automática de diretórios em escrever_arquivo
- [x] **[#4]** Criar ferramenta deletar_arquivo

### 🧠 Fase 2: Memória e Consciência de Contexto
- [x] **[#5]** Implementar gerador de contexto.txt (mapa do projeto)
- [x] **[#6]** Injetar contexto.txt no system prompt do agente
- [x] **[#7]** Regenerar contexto.txt apos operacoes de escrita/criacao/exclusao
- [x] **[#7]** Regenerar contexto.txt após operações de escrita/criação/exclusão

### 🏗️ Fase 3: Refatoração e Arquitetura do Código
- [x] **[#8]** Mover funcoes de ferramentas e definicoes JSON para tools.py
- [x] **[#9]** Centralizar configuracoes em config.py
- [x] **[#10]** Limpar agente.py para conter apenas o loop de conversa
- [ ] **[#11]** Padronizar retorno de erros para o LLM interpretar
- [x] **[#8]** Mover funções de ferramentas e definições JSON para tools.py
- [x] **[#9]** Centralizar configurações em config.py
- [x] **[#10]** Limpar agente.py para conter o loop principal e os Guards de segurança
- [x] **[#11]** Padronizar retorno de erros para o LLM interpretar

### Fase 4: Segurança e UX — EXTRA
- [ ] **[#12]** [DESAFIO] Implementar human-in-the-loop para acoes destrutivas
- [ ] **[#13]** [DESAFIO] Implementar validacao de path traversal (sandboxing)
- [ ] **[#14]** [DESAFIO] Criar sistema de logging em agent.log
### 🛡️ Fase 4: Segurança, Guards e UX
- [x] **[#12]** Implementar Human-in-the-Loop (`pedir_autorizacao`) para ações de execução
- [x] **[#13]** Implementar Guard de Cegueira (bloqueio de escrita sem leitura prévia)
- [x] **[#14]** Implementar Guard de Validação Física de Arquivos Existentes
- [x] **[#15]** Implementar Guard Anti-loop para evitar leituras redundantes
