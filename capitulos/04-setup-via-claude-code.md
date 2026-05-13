# Capítulo 4 — Setup via Claude Code (modo agêntico)

> Este capítulo é alternativa ao Cap. 3. Se você prefere instalar tudo na unha lendo cada linha do terminal, fica no Cap. 3. Se você prefere conversar com um agente que detecta seu sistema, instala, valida e propõe o próximo passo, fica aqui.
>
> **Spoiler:** mesmo escolhendo o modo agêntico, leia o Cap. 3 depois. Saber o que está acontecendo por baixo do capô é fundamental para depurar quando algo quebra.

## 4.1 Por que usar Claude Code para o setup

Setup manual exige que você decore: o nome do package, a versão correta, a flag certa, a ordem dos passos, o caminho do `.sqlite`. Você sai do capítulo 3 com 40 comandos na cabeça e vai esquecer metade na semana seguinte.

Setup via Claude Code inverte: **você descreve o objetivo**, ele propõe os passos, executa, valida, e narra o que fez. Você termina sabendo o que **você** quer, não o que cada package faz.

| Aspecto | Setup manual (Cap. 3) | Setup via Claude Code (este cap.) |
|---|---|---|
| Tempo total | 3-4h | 1-2h |
| Curva inicial | Alta | Suave — aprende fazendo |
| Erros | Difícil voltar atrás | Claude Code propõe rollback |
| Documentação | Você anota tudo | Claude Code escreve enquanto faz |
| Reuso em outra máquina | Você recomeça o checklist | Cole os mesmos prompts |
| Para quem | Quer entender cada linha | Quer chegar no resultado |

🎯 Recomendação prática: **modo agêntico no primeiro setup**, depois **modo manual** para ajustes pontuais.

## 4.2 Pré-requisitos antes de abrir o Claude Code

Você precisa de **só duas coisas** instaladas previamente:

1. **Node.js 18+** (para rodar o CLI)
2. **Conta Anthropic** com créditos ou plano (Pro $20/mês é o ponto-doce)

Tudo o resto — Python, Git, Obsidian, Zotero, VOSviewer, Graphify — o próprio Claude Code instala (ou te ensina a instalar) conforme o caminho avança.

Instale o CLI:

```bash
# Windows PowerShell ou Mac/Linux
npm install -g @anthropic-ai/claude-code
claude login
```

Verifique que funcionou:

```bash
claude --version
```

## 4.3 Anatomia de uma sessão de setup agêntica

Antes dos prompts canônicos, entenda o ritmo da conversa:

```
Você abre a CLI:
  $ cd ~/Documents/meu-vault-novo
  $ claude

Claude Code:
  "Olá. Em que diretório estamos? O que você quer fazer aqui?"

Você:
  "Aqui vai ser o vault Obsidian do meu mestrado em [área]. 
   Quero pipeline com Zotero + Graphify + VOSviewer integrados."

Claude Code:
  "Detectei: Windows 11, PowerShell, sem repo Git, pasta vazia.
   Proponho começar por:
   1. Verificar se você tem Python 3.10+
   2. Criar estrutura PARA do vault
   3. Inicializar git
   4. Instalar Graphify
   Posso seguir?"

Você:
  "pode"

Claude Code roda comandos, mostra output, e propõe o próximo passo.
```

**Pontos críticos** desse ritmo:
- Claude Code **propõe** — você **aprova ou ajusta**
- Cada comando aparece na tela antes de rodar
- Erros disparam re-proposta, não pânico
- A conversa fica salva no histórico do projeto

## 4.4 Roteiro de prompts canônicos

Estes prompts foram testados. Cole-os adaptando ao seu contexto. Eles cobrem do zero ao pipeline operacional em ~5 turnos.

### Prompt 1 — Diagnóstico inicial

```
Sou pesquisador em [SUA ÁREA]. Vou montar pipeline de pesquisa com 
Obsidian + Zotero + Graphify + VOSviewer integrado, gerenciado por 
você. Antes de começar, faça um diagnóstico:

1. Qual meu sistema operacional e shell?
2. Tenho Python 3.10+ instalado?
3. Tenho Git configurado?
4. Tenho Node.js? (já que você está rodando, óbvio sim)
5. Quanto de espaço livre tenho no disco?

Liste o que falta e proponha ordem de instalação.
```

### Prompt 2 — Criar vault Obsidian

```
Crie estrutura de vault Obsidian PARA adaptada para pesquisa em 
[SUA ÁREA]. Use esta convenção de pastas:

- 00 - Inbox
- 10 - [tópico-principal]
- 20 - Referencias (subdividida por linhas de pesquisa)
- 30 - Conceitos
- 40 - Pessoas e Instituicoes
- 50 - Analises
- 60 - Disciplinas
- 90 - Arquivo
- _meta (templates, scripts, library.bib)

Crie um README.md na raiz explicando a estrutura. Crie 5 templates 
básicos em _meta/templates/: nota-referencia, capitulo, reuniao, 
daily, dashboard.

NÃO crie templates específicos da minha área ainda — vou pedir 
adaptações depois.
```

### Prompt 3 — Git + GitHub privado

```
Inicialize git no vault, crie .gitignore apropriado (excluir 
.obsidian/workspace*, _build, *.tmp), crie repo PRIVADO no GitHub 
chamado [SEU-USUARIO]/[NOME-VAULT], faça o primeiro commit e push.

Importante: PRIVADO. Confirme o flag --private antes de criar.
```

### Prompt 4 — Importar Zotero

```
Meu Zotero local tem [N] referências. Quero importar para o vault 
gerando 1 nota .md por referência em 20 - Referencias.

Passos:
1. Verifique se zotero.sqlite existe em ~/Zotero/zotero.sqlite
2. Baixe o script export_zotero_to_vault.py do livrinho 
   github.com/ricamesq/pesquisa-ia-praxis/blob/main/scripts/
3. Edite a seção CONFIG com meus caminhos
4. Rode em modo dry-run primeiro (mostra quantas notas geraria 
   sem escrever nada)
5. Se OK, rode de verdade
6. Faça commit do vault

Se o Zotero estiver aberto durante a importação, NÃO peça pra eu 
fechar — o script usa URI read-only.
```

### Prompt 5 — Primeira indexação Graphify

```
Instale o Graphify (uv tool install graphifyy), instale a skill 
no Claude Code (graphify claude install), e rode /graphify no 
vault.

Quando o pipeline terminar, abra graph.html no navegador e me 
explique os 5 god nodes principais e as 3 conexões surpreendentes 
mais interessantes do GRAPH_REPORT.md.
```

### Prompt 6 — Primeiro mapa VOSviewer

```
Exporte o corpus do Zotero em RIS:
- Collection: [nome da collection principal]
- Formato: RIS
- Destino: _meta/exports/corpus-aaaa-mm-dd.ris

Abra o VOSviewer e proponha:
1. Tipo de análise: co-occurrence de palavras-chave
2. Min occurrences: 5 ou 10 (você decide baseado no tamanho do corpus)
3. Salvar 3 mapas (network, density, overlay) em 50 - Analises/

Depois me explique o que cada mapa mostra em uma frase.
```

Pronto — em 6 prompts você sai do zero para um vault pronto, indexado, com primeiro mapa bibliométrico salvo.

## 4.5 Skills e Agents que ajudam

A Claude Code tem extensões via plugins (skills) e agentes (subagents). Para pesquisa, três são especialmente úteis:

### Skills nativas

- **`/graphify`** — gera knowledge graph (capítulo central deste livrinho)
- **`/init`** — inicializa CLAUDE.md no diretório atual (registra convenções do projeto)

### Plugin ECC (Everything Claude Code)

Instalação opcional:

```bash
claude plugin marketplace add affaan-m/everything-claude-code
claude plugin install ecc@ecc
```

Skills e agents do ECC úteis em pesquisa (ver Cap. 9 para catálogo completo):

- Agent `code-reviewer` — revisa seus scripts Python antes de commit
- Skill `scientific-thinking-literature-review` — apoio metodológico em revisão de literatura
- Skill `scientific-db-pubmed-database` — busca no PubMed via E-Utilities (útil em saúde)
- Skill `repo-scan` — audita seu vault antes de publicar (acha PII, credenciais)
- Skill `documentation-lookup` — busca docs de bibliotecas Python sem sair da CLI

⚠️ ECC traz 60 agents + 225 skills. Não tente conhecer todos — instale, deixe ali, e descubra na demanda.

## 4.6 O que o Claude Code NÃO deve fazer

Limites importantes para você impor à conversa:

1. **Não decidir taxonomia por você.** Quais tags usar, como nomear linhas de pesquisa, qual classificação metodológica — isso é decisão sua. Use Claude Code para implementar sua escolha, não para inventar.

2. **Não fichar referências sem você ler.** Você pode pedir resumo automático para triagem, mas o fichamento que vai para a tese precisa do seu engajamento. Caso contrário, você vira curador de output de LLM, não pesquisador.

3. **Não rodar batches grandes sem dry-run.** Sempre pedir: "antes de escrever, me mostra o que vai gerar". Especialmente em scripts que reescrevem o vault.

4. **Não fazer git push sem você confirmar.** Especialmente em repos públicos. Sempre conferir o `git status` e o diff antes do push.

5. **Não usar `--no-verify` em commits.** Os hooks existem por motivo (lint, testes, segurança). Se um hook falha, descubra o porquê.

🎯 Regra geral: **read-only é livre, write requer confirmação, push requer revisão.**

## 4.7 Auto-memory: a vantagem da retomada

O Claude Code mantém um sistema de memória persistente em `~/.claude/projects/[hash-do-projeto]/memory/`. Cada sessão pode salvar e recuperar memórias de tipos:

- **user** — quem você é (sua área, nível de experiência)
- **feedback** — guidance que você deu ("não rode batches sem dry-run")
- **project** — estado da pesquisa ("estou no capítulo 3 da revisão de literatura")
- **reference** — onde estão recursos externos ("meu Zotero está em X path")

Ao começar nova sessão semanas depois, o Claude Code lê essa memória e **retoma onde parou** — você não precisa re-explicar o projeto inteiro.

Use as palavras-chave para acionar memórias específicas. Exemplo:

```
Você: "retomar pipeline mestrado"

Claude Code lê: project_pipeline_mestrado.md
                 + feedback_taxonomia_personalizada.md
                 + reference_zotero_path.md

Claude Code: "Continuando de onde paramos: você está com 
              1.847 refs no Zotero, último Graphify rodou em 
              [data], pendente: aplicar thesaurus atualizado 
              no VOSviewer. Quer seguir por aí?"
```

🎯 **Salve memórias deliberadamente.** Ao tomar decisão metodológica importante, fale: "salva isso na memória — decisão sobre [X] é [Y] porque [Z]". Você está construindo seu cérebro externo permanente.

## 4.8 Quando NÃO usar o modo agêntico

Algumas situações em que o setup manual é melhor:

- **Você precisa entender o stack profundamente** (estudante novo em Python e shell que está se formando)
- **Sua organização proíbe LLM em fluxo de pesquisa** (questões éticas/políticas)
- **Internet ruim ou intermitente** (Claude Code precisa de conexão pra cada turno)
- **Você é pesquisador-engenheiro experiente** e o overhead da conversa custa mais que a execução manual

Para todos os outros casos, modo agêntico ganha.

## 4.9 Checklist mínimo de validação

Após o setup via Claude Code, valide manualmente que você consegue:

- [ ] Abrir o vault no Obsidian e ver a estrutura PARA
- [ ] Rodar `git log --oneline` e ver pelo menos um commit
- [ ] Ver `library.bib` ou `references/*.md` no vault
- [ ] Abrir `graphify-out/graph.html` no navegador e clicar em um nó
- [ ] Abrir um `.png` de mapa VOSviewer

Se um desses falha, **abra nova sessão Claude Code e relata o falha exata** — ele propõe diagnóstico e fix. Não tente consertar na mão antes de tentar reportar.

---

> 📚 **Próximo capítulo:** [05 — Fluxo integrado](05-fluxo-integrado.md) (visão sistêmica do pipeline)
