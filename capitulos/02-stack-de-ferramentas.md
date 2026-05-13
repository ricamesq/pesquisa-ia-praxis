# Capítulo 2 — Stack de ferramentas

Antes de mergulhar em setup e fluxo, é importante entender **o que cada peça faz e por que ela está aqui**. Você vai gastar tempo configurando estas ferramentas. Vale saber por quê.

Apresento cada uma na ordem em que entram no fluxo: o que faz, alternativas que considerei, decisão final, limites conhecidos.

## 2.1 Zotero — o banco de dados pessoal de referências

### O que faz

O **Zotero** é um gerenciador de referências bibliográficas open-source criado pela George Mason University (EUA) em 2006. Funciona como:

- **Capturador** de metadados de páginas web, PDFs, arquivos ENW/RIS/BibTeX (via clip de navegador)
- **Armazenador local** de PDFs anotáveis (com sidecar de anotações estruturadas desde versão 6)
- **Banco de dados SQLite** com ~30 campos por referência (autor, ano, título, abstract, DOI, URL, ISSN, páginas, editor, tags, coleções, etc.)
- **Exportador** para qualquer formato de citação (BibTeX, RIS, CSL JSON, EndNote XML, Word/LibreOffice citation, formato ABNT via CSL)
- **Sincronizador** opcional via Zotero Sync (servidor próprio)

### Alternativas consideradas

| Ferramenta | Por que descartei |
|---|---|
| **Mendeley** | Comprada pela Elsevier; trajetória de cancelamento de features. Não é mais escolha técnica responsável. |
| **EndNote** | Proprietário, caro, formato fechado, exportação ruim |
| **Citavi** | Boa mas Windows-only e proprietária |
| **Paperpile** | Cloud-only, dependência de Google Drive, $36/ano. Bom mas você não controla os dados. |
| **JabRef** | Boa alternativa, BibTeX-nativo, mas integração com Word/LibreOffice é mais frágil que Zotero |

### Decisão: Zotero

Critérios decisórios:
- **Open-source** (você pode inspecionar e modificar)
- **Local-first** (sincronização opcional, mas database local primário)
- **Plugin ecosystem rico** (Better BibTeX, Zotfile, Zutilo, Mdnotes)
- **API local** (porta 23119 via Better BibTeX, acessível por scripts)
- **Citação em LibreOffice/Word** funcional
- **ABNT via CSL** vem pronto (precisa só plugar o style)

### Limites conhecidos

- **Performance degrada** com 5.000+ refs (mais devagar pra abrir lista, mas SQLite aguenta bem queries diretas)
- **Sync via servidor próprio é limitado** (300 MB grátis); soluciona-se pondo PDFs em pasta separada (Zotfile)
- **Anotações em PDF não exportam** facilmente para texto fora do Zotero (o plugin Mdnotes ajuda, mas é frágil)
- **Tag autotagging** (que adiciona MeSH/Wikidata automaticamente) produz ruído (`human`, `procedures`, `article` aparecem em centenas de refs sem agregar valor)

### Versão usada neste livro

Zotero **7.x** (2025+) com plugins:
- **Better BibTeX** (auto-export, citekey persistente, integração com Obsidian)
- **Zotfile** (opcional — gestão de PDFs em pasta separada)

## 2.2 Obsidian — o cérebro de trabalho

### O que faz

O **Obsidian** é um editor de Markdown que trata uma pasta de arquivos `.md` como um "vault" (cofre) navegável por:

- **Wikilinks** (`[[Nome da Nota]]`) que criam hyperlinks bidirecionais
- **Tags** (`#letramento-digital`) que indexam temas cross-pastas
- **Backlinks automáticos** (quais notas linkam pra essa)
- **Graph view** (visualização de rede do vault inteiro)
- **Templates** (boilerplate reusável de notas)
- **Plugins** (mais de 1.500 da comunidade, incluindo Dataview, Templater, Tasks, Zotero Integration, Obsidian Git)

### Alternativas consideradas

| Ferramenta | Por que descartei |
|---|---|
| **Notion** | Excelente UX, mas vendor lock-in total. Dados ficam na nuvem deles. Exportação é ruim. Inviável para projeto de longo prazo. |
| **Roam Research** | Pioneiro do bidirectional linking, mas cloud-only, caro ($15/mês), e a empresa tem trajetória instável. |
| **Logseq** | Excelente alternativa open-source e local-first. Estrutura **outliner-first** (bullets nested) é poderosa mas tem curva de aprendizagem alta. Para escrita acadêmica longa, document-first do Obsidian é mais natural. |
| **Joplin** | Decente, mas plugin ecosystem mais raso |
| **Standard Notes** | Foco em segurança, plugins limitados |
| **TiddlyWiki** | Único arquivo HTML; engenhoso mas ergonomia limitada para corpora grandes |
| **Markdown puro + VS Code** | Funciona mas perde graph view, dataview, backlinks automáticos |

### Decisão: Obsidian

Critérios decisórios:
- **Plain-text Markdown** (você possui as notas para sempre)
- **Local-first** (vault é uma pasta no disco, sincroniza com OneDrive/Dropbox/Git/iCloud)
- **Plugin ecosystem** maduro e ativo
- **Graph view nativo** com filtros por tag/path/cor
- **Dataview** transforma o vault em banco de dados consultável
- **Free para uso pessoal** (Sync e Publish são pagos mas opcionais)

### Limites conhecidos

- **Não é colaborativo em tempo real** (multi-cursor estilo Google Docs). Soluciona-se com Git pra colaboração assíncrona.
- **Plugin de terceiros pode quebrar** entre versões. Recomenda-se travar versões de plugins críticos.
- **Performance degrada** com vaults > 50.000 notas. Soluciona-se separando vaults por domínio.
- **App mobile** é separado (Obsidian Mobile) e tem latência maior.

### Versão usada neste livro

Obsidian **1.12.x** (Windows). Plugins essenciais:
- **Dataview** (queries SQL-like nas notas)
- **Templater** (templates dinâmicos com JS)
- **Tasks** (gestão `- [ ]` avançada)
- **Obsidian Git** (versionamento automático)
- **Zotero Integration** (sincronização contínua com Zotero via Better BibTeX)

## 2.3 Graphify — o knowledge graph universal

### O que faz

O **Graphify** (criado por Safi Shamsi em 2024) é uma CLI Python que recebe uma pasta de arquivos (qualquer mix de código, docs, papers PDF, imagens, vídeos) e produz:

- Um **JSON do grafo** (`graphify-out/graph.json`)
- Uma **visualização HTML interativa** (`graph.html`)
- Um **relatório markdown** (`GRAPH_REPORT.md`) com god nodes, surprising connections, suggested questions
- Opcional: vault Obsidian gerado a partir do grafo, ou export para Neo4j

A extração combina **AST** (para arquivos de código) com **subagents LLM** (para arquivos de texto/imagem). Cada aresta é tagueada como `EXTRACTED` (relação explícita), `INFERRED` (relação inferida pelo LLM) ou `AMBIGUOUS` (incerta).

### Alternativas consideradas

| Ferramenta | Por que descartei |
|---|---|
| **Roam-style outliner** (manual) | Não escala para corpora grandes |
| **Excalidraw** | Excelente para esquemas, mas requer trabalho manual de desenho |
| **D3.js + script custom** | Reinventa a roda |
| **Neo4j Bloom** | Pesado e caro; bom para empresas, não pra pesquisa pessoal |
| **TheBrain** | Proprietário, fechado, formato bloqueado |

### Decisão: Graphify

Critérios decisórios:
- **Open-source** (instala via `uv tool install graphifyy`)
- **Multimodal** (lê código, markdown, PDF, imagens)
- **Audit trail** explícito (EXTRACTED vs INFERRED — você sabe o que foi encontrado vs inferido)
- **Incremental** (`--update` re-extrai só arquivos novos)
- **Output em formatos padrão** (JSON, HTML, Markdown, Cypher, GraphML)
- **Pipeline integrável** com Claude Code (via skill `/graphify`)

### Limites conhecidos

- **Custo de extração inicial é alto** (LLM tokens). Vault de 1.900 notas custa ~500k-1M tokens.
- **Markdown puro produz menos arestas** que código (já que markdown não tem imports explícitos)
- **Comunidades detectadas dependem do algoritmo** (Louvain ou Graspologic; este é instável em Windows)
- **HTML viz fica lenta** com > 5.000 nós

### Versão usada neste livro

Graphify **0.3.x** (2025+) instalado via uv tool.

## 2.4 VOSviewer — o mapa bibliométrico

### O que faz

O **VOSviewer** (criado por Nees Jan van Eck e Ludo Waltman na Universidade de Leiden em 2010) é uma aplicação Java desktop (multi-plataforma) que produz mapas de redes bibliométricas:

- **Co-autoria** (quais autores colaboram com quais)
- **Co-citação** (quais refs são citadas juntas com frequência)
- **Co-ocorrência de palavras-chave** (quais termos aparecem juntos em refs)
- **Acoplamento bibliográfico**

Três visualizações para cada análise:
- **Network** — nós, arestas, clusters por cor
- **Density** — heatmap de concentração
- **Overlay** — superposição com variável adicional (ano, citações, etc.) — usado para **detectar shifts temporais**

### Alternativas consideradas

| Ferramenta | Por que descartei |
|---|---|
| **Gephi** | Mais flexível, mas curva de aprendizagem alta. Para bibliometria, VOSviewer é mais especializado. |
| **Bibliometrix (R)** | Excelente pacote estatístico, mas requer R. VOSviewer é point-and-click. |
| **CiteSpace** | Boa alternativa, mas UI mais datada e curva de aprendizagem. |
| **Litmaps / Connected Papers** | Cloud-only, dados deles. Excluído por princípio local-first. |
| **Sci2 Tool** | Antigo, pouco mantido. |
| **Networkx + Python custom** | Reinventa visualização e clustering. Bom pra produção específica, ruim pra exploração. |

### Decisão: VOSviewer

Critérios decisórios:
- **Free para uso acadêmico** (proprietário mas gratuito)
- **Aceita formatos abertos** (RIS, CSV, BibTeX)
- **Algoritmo VOS** (Visualization of Similarities) é matematicamente sólido
- **Overlay temporal** é killer feature
- **Thesaurus customizável** (consolidação manual de termos)
- **Export para web** (VOSviewer Online) permite compartilhamento

### Limites conhecidos

- **Java desktop** — não é responsivo, não roda em mobile
- **Não é open-source** (mas é gratuito)
- **Algoritmo de clustering às vezes produz cluster gigante** que precisa de re-clusterização manual
- **Difícil rodar headless** (em servidor sem GUI)

### Versão usada neste livro

VOSviewer **1.6.20** (2024+).

## 2.5 Claude Code — o orquestrador agêntico

### O que faz

O **Claude Code** (criado pela Anthropic em 2024-2025) é uma CLI baseada em LLM (Claude Opus/Sonnet) que opera como um agente de programação:

- **Lê e escreve arquivos** no seu sistema
- **Executa comandos** no terminal
- **Encadeia ações** (planning + execution)
- **Mantém memória persistente** entre sessões (em arquivo local `~/.claude/`)
- **Tem skills e plugins** (instaláveis via `claude plugin marketplace`)
- **Suporta sub-agents** (delegação paralela para tarefas independentes)

Não é um chatbot. É um **operador agêntico** que faz trabalho.

### Alternativas consideradas

| Ferramenta | Por que descartei |
|---|---|
| **GitHub Copilot CLI** | Mais limitado em encadeamento de ações |
| **Aider** | Open-source e bom, mas integração mais difícil com Obsidian |
| **Cursor (IDE)** | Excelente IDE mas vendor lock-in. CLI agente é alternativa mais portável. |
| **Cline** (VS Code extension) | Bom mas amarrado ao VS Code |
| **OpenAI Codex / Operator** | Promissor mas pago e fechado |
| **Llama agents locais** | Funciona mas qualidade de raciocínio ainda inferior ao Claude para tarefas complexas |

### Decisão: Claude Code

Critérios decisórios:
- **Qualidade de raciocínio** alta (Opus 4.x em complexity-heavy work)
- **Multimodal** (lê imagens, PDFs)
- **Plugins/skills** (rico ecossistema, incl. ECC com 60 agents + 225 skills)
- **MCP servers** (Model Context Protocol — integração com qualquer serviço externo)
- **Memória persistente** entre sessões (essencial para projetos longos)

### Limites conhecidos

- **Não é gratuito** (Anthropic API ou Claude Pro). Mas há free tier limitado.
- **Não substitui o pesquisador** — apenas o aumenta
- **Pode alucinar** em domínios fora do treinamento. Precisa de verificação humana.
- **Privacy** — código enviado pra API da Anthropic (data não usada pra treino, mas você está enviando)

### Versão usada neste livro

Claude Code **2.x** rodando Claude **Opus 4.x** (2025+).

## 2.6 Por que essas cinco, juntas

A lógica do stack é **uma para cada camada do ciclo de pesquisa**:

| Camada | Pergunta da pesquisa | Ferramenta |
|---|---|---|
| **Coleta** | Onde guardar os PDFs e metadados? | Zotero |
| **Escrita e síntese** | Onde fichar, anotar, escrever capítulos? | Obsidian |
| **Estrutura conceitual** | Como o corpus se relaciona consigo? | Graphify |
| **Análise bibliométrica** | Que padrões emergem do corpus como um todo? | VOSviewer |
| **Orquestração** | Quem cose as outras quatro? | Claude Code |

Cada uma é especialista. O orquestrador (Claude Code) é o conector — mas você é quem decide o que vale a pena conectar.

## 2.7 Custo total

| Item | Custo monetário | Custo de tempo (setup) |
|---|---|---|
| Zotero | gratuito | 1 h |
| Obsidian | gratuito (Sync e Publish são pagos opcionais) | 1 h |
| Graphify | gratuito (Python) — LLM tokens custam | 30 min |
| VOSviewer | gratuito (acadêmico) | 30 min |
| Claude Code | $20/mês (Claude Pro) ou API pay-per-use | 0 (já instalado se você usa Claude Code) |
| **Total** | ~$20/mês + tokens LLM | ~3 horas (uma vez só) |

Para um pesquisador acadêmico, o ROI é absurdo. Apenas a economia de tempo de re-busca paga em uma semana.

---

> 📚 **Próximo capítulo:** [03 — Setup](03-setup.md)
