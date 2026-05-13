# Capítulo 8 — Anexos e catálogo

## 8.1 Scripts incluídos no repositório

Todos em [`scripts/`](../scripts/). Comentados para você adaptar.

| Script | Função | Quando rodar |
|---|---|---|
| `export_zotero_to_vault.py` | Lê `zotero.sqlite` (read-only) e gera 1 nota .md por ref no vault | Bootstrap inicial e re-sync periódico |
| `analise_shift_v2.py` | Compara dois cortes do corpus (RIS antigo × Zotero atual) por eixos temáticos | Antes de capítulo de revisão de literatura |
| `compare_cooccurrence.py` | Pares de tags co-ocorrendo no Zotero × no RIS antigo | Detectar clusters emergentes |
| `gen_candidatas.py` | Tags Zotero candidatas a entrar no thesaurus VOSviewer | Antes de regenerar mapa bibliométrico |

Adicione seus scripts próprios conforme adaptar. Pull requests são bem-vindas no repo.

## 8.2 Templates de Obsidian

Em [`exemplos/`](../exemplos/):

- `nota-referencia.md` — template de fichamento de ref do Zotero
- `capitulo.md` — template para iniciar um capítulo da tese
- `reuniao-orientacao.md` — template para registrar encontros
- `daily.md` — daily note
- `dashboard.md` — painel central com queries Dataview

## 8.3 Catálogo do plugin ECC (Everything Claude Code)

Se você instalou o ECC (`claude plugin install ecc@ecc`), tem disponíveis **60 agents** e **225 skills**. Os mais úteis para pesquisa:

### Agents úteis em contexto acadêmico

| Agent | Para que serve |
|---|---|
| `code-reviewer` | Revisar código de scripts seus antes de commitar |
| `code-explorer` | Explorar codebases complexas (útil ao adaptar scripts deste livro) |
| `doc-updater` | Manter documentação em sincronia com código |
| `tdd-guide` | Acompanhar testes ao desenvolver scripts próprios |

### Skills úteis em contexto acadêmico

| Skill | Para que serve |
|---|---|
| `agentic-engineering` | Boas práticas para trabalho com agentes |
| `prompt-optimizer` | Otimizar prompts que você reusa |
| `documentation-lookup` | Buscar docs de bibliotecas Python |
| `repo-scan` | Auditar repositório antes de publicar |
| `code-tour` | Walkthrough de codebase para retomada |
| `scientific-db-pubmed-database` | Integrar com PubMed |
| `scientific-thinking-literature-review` | Apoio metodológico em revisão de literatura |
| `scientific-thinking-scholar-evaluation` | Critérios para avaliar fontes |

Catálogo completo: https://github.com/affaan-m/everything-claude-code

## 8.4 Comandos cheatsheet

### Zotero (via Better BibTeX)

| Comando | Função |
|---|---|
| `Ctrl+Shift+Z` (no Word/LibreOffice) | Inserir citação inline |
| Better BibTeX → Refresh All | Re-gerar citation keys após mudança no padrão |
| File → Export Library → Better BibLaTeX | Export contínuo do `.bib` |

### Obsidian

| Atalho | Função |
|---|---|
| `Ctrl+P` | Command palette |
| `Ctrl+O` | Quick switcher (abrir nota por nome) |
| `Ctrl+G` | Graph view |
| `Ctrl+,` | Settings |
| `Ctrl+Shift+O` | (Zotero Integration) Insert citation |
| `Ctrl+Shift+I` | (Zotero Integration) Import note from Zotero |

### Graphify

| Comando | Função |
|---|---|
| `graphify update <path>` | Re-extrair só arquivos modificados |
| `graphify update <path> --force` | Re-extrair tudo |
| `graphify query "<pergunta>"` | Consulta BFS no grafo |
| `graphify path "A" "B"` | Caminho mais curto entre dois conceitos |
| `graphify explain "X"` | Explicação de um nó e seus vizinhos |
| `graphify merge-graphs g1 g2 g3 --out merged.json` | Meta-grafo multi-vault |
| `graphify claude install` | Instalar skill no Claude Code |

### VOSviewer

| Função | Onde |
|---|---|
| Criar mapa novo | File → Create a map |
| Importar thesaurus | Wizard de criação → "Use thesaurus" |
| Exportar PNG | File → Save as → seleção do tipo de visualização |
| Compartilhar online | Save to VOSviewer Online |

### Claude Code

| Comando | Função |
|---|---|
| `claude` | Iniciar sessão (CLI) |
| `claude --bare` | Sessão mínima sem hooks/auto-memory |
| `claude plugin list` | Listar plugins instalados |
| `claude plugin install <name>@<marketplace>` | Instalar plugin |
| `/skill <nome>` (na CLI) | Invocar skill manualmente |
| `/graphify <path>` (na CLI) | Rodar pipeline Graphify completo |

## 8.5 Glossário

| Termo | Significado |
|---|---|
| **AST** | Abstract Syntax Tree. Representação estrutural de código-fonte usada por Graphify para extrair entidades de arquivos de código (deterministic, sem LLM). |
| **Bibliometria** | Análise estatística de produção científica (publicações, citações, palavras-chave). |
| **BibTeX** | Formato de citação criado por Oren Patashnik em 1985. Padrão de fato em TeX/LaTeX. |
| **Bridge node** | Em grafo, nó com alta betweenness centrality — fica entre comunidades distintas, intermedia caminhos. |
| **Citekey** | Identificador único de uma referência (ex.: `silva2024letramento`). Gerado por Better BibTeX. |
| **Cluster** | Grupo de nós em um grafo, detectado por algoritmo (Louvain, Leiden, Graspologic). |
| **Co-citação** | Duas refs aparecem citadas juntas em um terceiro paper. Métrica bibliométrica. |
| **Co-ocorrência** | Duas palavras-chave aparecem juntas em uma mesma ref. Métrica bibliométrica. |
| **CSL** | Citation Style Language. Padrão para definir formatos de citação (ABNT, APA, Vancouver, etc.). |
| **DOI** | Digital Object Identifier. Identificador permanente de publicações acadêmicas. |
| **God node** | Nó mais conectado em um grafo. Representa abstração central do corpus. |
| **Graph view** | Visualização de rede do vault Obsidian (nós = notas, arestas = wikilinks). |
| **Hyperedge** | Aresta que conecta 3+ nós ao mesmo tempo (em vez de 2). Capta relações de grupo. |
| **LLM** | Large Language Model. Modelo de linguagem usado por Claude, GPT, Gemini etc. |
| **MCP** | Model Context Protocol. Padrão de comunicação entre LLMs e ferramentas externas. |
| **MeSH** | Medical Subject Headings. Vocabulário controlado da PubMed. Auto-tags Zotero usam MeSH (fonte do ruído `Humans`, `Article` etc.) |
| **Multi-tenant** | Sistema que serve múltiplas organizações em isolamento lógico (não relevante aqui, mas aparece no Anamnese). |
| **Overlay** | No VOSviewer, visualização de mapa com cor adicional indicando uma variável (ano, citações). |
| **PARA** | Projects-Areas-Resources-Archives. Sistema de organização de PKM de Tiago Forte. |
| **PKM** | Personal Knowledge Management. |
| **RIS** | Research Information Systems. Formato padrão de citação. |
| **Subagent** | No Claude Code, agent secundário instanciado para tarefa específica (ex.: extração de um chunk de Graphify). |
| **Subsunçor** | Conceito da Aprendizagem Significativa (Ausubel). Estrutura cognitiva ancorada que recebe nova informação. |
| **Thesaurus** | Lista controlada que consolida sinônimos. No VOSviewer, mapa de `label → replace_by`. |
| **TUG** | Timed Up and Go. Teste funcional clínico. |
| **Vault** | No Obsidian, pasta de arquivos `.md` tratada como sistema único de notas. |
| **VOS** | Visualization of Similarities. Algoritmo de projeção 2D do VOSviewer. |
| **Wikilink** | `[[Nota X]]` no Obsidian. Link bidirecional entre notas. |

## 8.6 Recursos externos recomendados

### Livros

- Ahrens, Sönke. *How to Take Smart Notes* (2017). Método Zettelkasten. Fundamentação para PKM.
- Forte, Tiago. *Building a Second Brain* (2022). Método PARA. Mais aplicado/operacional.
- Donovan, Brian, et al. *Citation Metrics in Academia: A Comprehensive Handbook* (2024).

### Cursos online

- Curso de VOSviewer por Nees Jan van Eck e Ludo Waltman (CWTS/Leiden) — gratuito
- Obsidian Sandbox e Forum oficial — https://forum.obsidian.md
- Anthropic Cookbook — exemplos práticos com Claude Code

### Comunidades

- Reddit: r/Zotero, r/ObsidianMD, r/AcademiaBR
- Discord: Obsidian Community, Anthropic Discord
- GitHub Discussions: cada uma das ferramentas tem fórum próprio

### Artigos seminais

- Eck, Nees Jan van; Waltman, Ludo. **Software survey: VOSviewer, a computer program for bibliometric mapping**. *Scientometrics*, v. 84, n. 2, p. 523-538, 2010.
- Redecker, Christine. **European Framework for the Digital Competence of Educators: DigCompEdu** (JRC, 2017).
- Ausubel, David P. **Educational Psychology: A Cognitive View** (1968).
- Moreira, Marco A. **Aprendizagem significativa crítica** (2012).
- Freire, Paulo. **Pedagogia da Autonomia** (1996).

## 8.7 Roadmap deste livrinho

| Versão | Conteúdo | ETA |
|---|---|---|
| **0.1** (atual) | Versão alfa. 9 capítulos. Scripts funcionais. Em português. | Maio/2026 |
| **0.2** | Capturas de tela em todos os capítulos. Vídeo walkthrough complementar (YouTube). | Q3/2026 |
| **0.3** | Tradução para inglês. Capítulo extra: integração com Notion e Roam (para quem não usa Obsidian). | Q4/2026 |
| **1.0** | Versão revisada por banca de mestrado. Capítulo extra: variações por área (direito, engenharia, ciências exatas). PDF impresso disponível em open access. | 2027 |

## 8.8 Contribuir

Issues e pull requests em https://github.com/ricamesq/pesquisa-ia-praxis.

Áreas onde contribuição é especialmente bem-vinda:

- Tradução de templates para outras áreas (direito, engenharia, biologia)
- Scripts adaptados para Mendeley/EndNote (em vez de Zotero)
- Versão macOS dos scripts (este livro foca em Windows)
- Capturas de tela e walkthroughs em vídeo
- Discussão de armadilhas novas que você encontrar

---

> 📚 **Próximo:** [99 — Referências](99-referencias.md)
