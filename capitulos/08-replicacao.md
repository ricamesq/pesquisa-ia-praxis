# Capítulo 7 — Como replicar do zero

> Checklist consolidado. Se você fez tudo nos capítulos anteriores, este capítulo é resumo. Se está com pressa, pode pular pra cá — mas volta para os capítulos de fundamentação depois pra entender por que cada passo importa.

## 7.1 Tempo estimado total

| Estágio | Tempo |
|---|---|
| Setup (uma vez só) | 2-3 horas |
| Bootstrap Zotero → vault (1.000 refs) | 10-20 minutos |
| Primeira indexação Graphify do vault | 5-15 minutos |
| Primeiro mapa VOSviewer | 30 minutos |
| Análise temporal e co-ocorrência | 20 minutos |
| **Total para ter sistema funcionando** | **3-4 horas** |
| Manutenção semanal a partir daí | 30-60 minutos |

## 7.2 Checklist do zero

### Etapa 0 — Pré-requisitos

- [ ] Python 3.10+ instalado (`python --version`)
- [ ] Git instalado e configurado (`git config --global user.email "..."`)
- [ ] Conta GitHub criada
- [ ] 6 GB de espaço em disco
- [ ] Conta Zotero criada (gratuita)
- [ ] Conta Anthropic criada (para Claude Code)

### Etapa 1 — Instalar ferramentas (1-2h)

- [ ] Zotero 7+ instalado
- [ ] Better BibTeX instalado no Zotero
- [ ] Auto-tagging desabilitado no Zotero
- [ ] Estilo ABNT instalado no Zotero
- [ ] Obsidian instalado
- [ ] Plugins Obsidian instalados: Dataview, Templater, Tasks, Obsidian Git, Zotero Integration
- [ ] Templates do vault criados
- [ ] Graphify instalado: `uv tool install graphifyy`
- [ ] Skill `/graphify` instalada no Claude Code: `graphify claude install`
- [ ] VOSviewer 1.6.20+ instalado
- [ ] Java 11+ instalado (para VOSviewer)
- [ ] Claude Code CLI instalado e autenticado: `claude login`

### Etapa 2 — Criar e versionar vault (30 min)

- [ ] Pasta do vault criada (ex.: `~/Documents/<sua-instituicao>/<seu-vault>`)
- [ ] Estrutura PARA criada (00-Inbox, 10-Tese, 20-Referencias, ...)
- [ ] Templates copiados para `_meta/templates/`
- [ ] Dashboard criado em `_meta/dashboard.md`
- [ ] Vault aberto no Obsidian
- [ ] `git init` no vault
- [ ] `.gitignore` configurado
- [ ] Repo GitHub privado criado: `gh repo create <user>/<vault-name> --private --source=. --remote=origin --push`
- [ ] Plugin Obsidian Git configurado (auto-commit 30s, auto-push 60s)

### Etapa 3 — Curar Zotero (varia: 30 min a 30 horas)

⚠️ Essa etapa é **proporcional à bagunça atual da sua biblioteca**. Se você já tem Zotero organizado, são 30 minutos. Se você tem 1.000 PDFs perdidos no Drive, é dia inteiro.

- [ ] Importar todas as refs de fontes (PDFs locais, exports de bases bibliográficas, links de papers)
- [ ] Criar collections temáticas (ex.: `P1_X`, `P2_Y`, `P3_Z`, `P4_BaseTeorica`)
- [ ] Tags manuais consistentes (`gap_*`, `teoria_*`, `fonte_*`, `status_*`)
- [ ] Remover refs duplicadas (Tools → Find Duplicate Items)
- [ ] Preencher DOIs faltantes
- [ ] Auto-export do `.bib` para `<vault>/_meta/library.bib`

### Etapa 4 — Bootstrap vault com Zotero (15 min)

- [ ] Copiar `scripts/export_zotero_to_vault.py` do livrinho para `<vault>/_meta/scripts/`
- [ ] Editar variáveis do script (ZOTERO_DB, VAULT_REFS, COLLECTIONS_FOLDERS)
- [ ] Rodar: `python export_zotero_to_vault.py`
- [ ] Verificar contagem (deve bater com total no Zotero)
- [ ] Commit no vault: `git add -A && git commit -m "feat: bootstrap refs do Zotero"`

### Etapa 5 — Configurar Zotero Integration (10 min)

- [ ] Settings → Zotero Integration → Database: `_meta/library.bib`
- [ ] Notes folder: `20 - Referencias`
- [ ] Citation template: vincular ao seu `nota-referencia.md`
- [ ] Testar atalho: `Ctrl+Shift+O` busca ref no Zotero e insere citação

### Etapa 6 — Primeira indexação Graphify (10 min)

- [ ] No Claude Code: `/graphify "<caminho do vault>"`
- [ ] Aguardar pipeline (subagents em paralelo)
- [ ] Verificar saída: `<vault>/graphify-out/graph.json`, `graph.html`, `GRAPH_REPORT.md`
- [ ] Abrir `graph.html` no navegador — explorar o grafo
- [ ] Ler god nodes e surprising connections no GRAPH_REPORT.md

### Etapa 7 — Primeiro mapa VOSviewer (30 min)

- [ ] Exportar RIS do Zotero: File → Export Library → RIS → `_meta/exports/corpus_<data>.ris`
- [ ] Abrir VOSviewer
- [ ] Create map → Bibliographic data → Choose files → RIS
- [ ] Co-occurrence → All keywords
- [ ] Minimum occurrences: 5 ou 10
- [ ] Salvar 3 PNGs em `<vault>/50 - Analises/vosviewer-<data>/`
- [ ] (Opcional) Aplicar thesaurus customizado se você já tem um

### Etapa 8 — Análise descritiva (10 min)

- [ ] Rodar `descritiva.py` (do Cap. 6 §6.1) — total por tipo, ano, autor
- [ ] Anotar resultados em `<vault>/50 - Analises/descritiva-corpus-<data>.md`
- [ ] Refletir: o corpus tem o tamanho que eu esperava? A distribuição faz sentido?

### Etapa 9 — Dashboard e ciclo semanal

- [ ] Dashboard funcional com queries Dataview (top tags, refs por status, refs por collection)
- [ ] Adicionar evento recorrente no calendário: "Atualizar pipeline pesquisa — Quintas-feiras 17h"
- [ ] Decidir frequência de mapas VOSviewer (mensal? trimestral?)

## 7.3 Adaptação por área do conhecimento

Este livrinho usa pesquisa em **educação + saúde digital** como exemplo. Para outras áreas, ajuste:

### Direito
- Foco em fichamento de jurisprudência (criar `30 - Jurisprudencias/`)
- Tags `lei_*`, `decreto_*`, `acordao_*`
- Citações em Vancouver ou ABNT NBR 6023 (jurídica)
- Adicionar plugin Pdf++ para destaque colorido de partes do PDF

### Engenharia
- Vault com pasta `30 - Patentes/` (importar metadata via Google Patents)
- Mais peso em código (scripts, simulações) — pode integrar com IDE
- Graphify pega imports de código bem

### Ciências da Saúde / Medicina
- Adicionar tag `nivel_evidencia` (1, 2A, 2B, ...) por ref
- Integrar com PubMed via E-Utilities API (script Python)
- Anotações em PDF mais relevantes — incluir Zotfile + extrator de annotations

### Ciências Sociais Aplicadas
- Foco em entrevistas / grupos focais → pasta `30 - Coleta de Dados/`
- Integração com NVivo ou Atlas.ti via export
- Análise temática complementar ao bibliométrico

### Humanidades (Filosofia, Literatura, História)
- Foco em fichamento profundo (notas longas por ref)
- Tags por **conceito** + **autor** + **período** + **escola filosófica**
- Menos peso em bibliometria visual, mais peso em graph view conceitual

## 7.4 Custo total

| Item | Custo (USD/mês) | Alternativa |
|---|---|---|
| Zotero | $0 | — |
| Obsidian | $0 (Sync e Publish opcionais) | — |
| Graphify | $0 (Python) + tokens LLM | — |
| VOSviewer | $0 (academic) | — |
| Claude Code Pro | $20 | API pay-per-use; ou Aider open-source |
| GitHub | $0 (private repos free) | — |
| **Total mínimo** | **$0** (sem Claude Code) | — |
| **Total recomendado** | **~$20/mês** | — |

## 7.5 Quanto tempo o pipeline economiza

Comparação subjetiva entre **antes** (sem pipeline) e **depois**:

| Tarefa | Tempo antes | Tempo depois |
|---|---|---|
| Achar uma ref específica que você lembra ter lido | 10-30 min | 30 s (busca no vault) |
| Listar todas as refs de um autor | 5 min | 10 s |
| Comparar como dois autores tratam um conceito | 1-3 horas | 15 min |
| Atualizar revisão de literatura com refs novas | 1 dia | 1 hora |
| Gerar mapa bibliométrico para apresentar em qualificação | 1-2 dias | 1 hora |
| Detectar shift temático no corpus | inviável | 30 min |

🎯 ROI: o pipeline paga seu setup (3-4 horas) **na primeira semana** de pesquisa séria.

## 7.6 O que você NÃO precisa fazer

Para evitar a tentação de over-engineer:

- ❌ **Não migre fichamentos antigos** para o vault novo de uma vez. Migre on-demand, conforme volta a usar.
- ❌ **Não tag tudo manualmente**. Use script + auto-tags + curadoria pontual.
- ❌ **Não rode Graphify diariamente**. Semanal ou após mudanças grandes basta.
- ❌ **Não fique configurando plugins novos** toda semana. Trava versão estável e usa.
- ❌ **Não compare seu vault com vaults de outros pesquisadores**. Cada pesquisa tem ritmo próprio.

## 7.7 Quando NÃO usar esse pipeline

Algumas situações em que esse pipeline é overkill:

- Você é pesquisador iniciante com < 50 refs no total. Use Zotero simples.
- Você está em fase final de redação. Setup novo agora atrasa em vez de ajudar.
- Você trabalha em equipe densa que já tem outro sistema. Use o sistema do grupo.
- Sua pesquisa é muito específica e o corpus é pequeno (< 100 refs). Bibliometria não rende.

🎯 O pipeline é **mais útil para mestrado de 2-4 anos e doutorado** — quando você precisa de profundidade defensiva e cobertura.

## 7.8 Próximos passos depois do setup

Uma vez que o sistema esteja rodando, considere:

- **Treinar colegas do grupo de pesquisa** no fluxo (pode virar grupo de estudo)
- **Adaptar este livrinho para sua área** e republicar como fork
- **Contribuir scripts/templates** para o repositório original
- **Documentar achados bibliométricos** em posts de blog científico

---

> 📚 **Próximo capítulo:** [09 — Anexos e catálogo](09-anexo-catalogo.md)
