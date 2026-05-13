# Capítulo 4 — Fluxo integrado

> Este é o **coração do livro**. O passo a passo de cinco etapas que, juntas, transformam uma biblioteca Zotero em um sistema de pesquisa navegável, analisável e versionado. Cada etapa funciona sozinha. Juntas, viram um pipeline.

## 4.1 Visão geral do fluxo

```
   ┌─────────────────────┐
   │   Zotero local      │  ← você cura aqui (collections, tags)
   │   (sqlite + PDFs)   │
   └──────────┬──────────┘
              │ Etapa 1: export Python
              ▼
   ┌─────────────────────┐
   │  Obsidian vault     │  ← onde fichamentos vivem
   │  20 - Referencias/  │
   │    @ref1.md         │
   │    @ref2.md         │
   │    ...              │
   └──────────┬──────────┘
              │ Etapa 2: Graphify
              ▼
   ┌─────────────────────┐
   │  graphify-out/      │  ← knowledge graph
   │   graph.json        │
   │   graph.html        │
   │   GRAPH_REPORT.md   │
   └──────────┬──────────┘
              │ Etapa 3: VOSviewer
              ▼
   ┌─────────────────────┐
   │  network.png        │  ← bibliometria visual
   │  density.png        │
   │  overlay.png        │
   └──────────┬──────────┘
              │ Etapa 4: comparação temporal
              ▼
   ┌─────────────────────┐
   │  shift-tematico.md  │  ← capítulo da tese
   └──────────┬──────────┘
              │ Etapa 5: meta-grafo
              ▼
   ┌─────────────────────┐
   │  merged-graph.json  │  ← múltiplos vaults dialogando
   └─────────────────────┘
```

Cada etapa tem entrada bem definida, saída bem definida, e é reprodutível. Você pode rodar uma sem rodar as outras. Rodar em sequência produz uma cadeia de conhecimento.

## 4.2 Etapa 1 — Exportar Zotero para Obsidian

### O que essa etapa faz

Lê o `zotero.sqlite` local (em modo read-only para não interferir no Zotero rodando), pega todas as referências (excluindo notas/anexos/deletadas), e gera **uma nota Markdown por referência** no vault Obsidian.

Cada nota tem:
- **Frontmatter YAML** completo (zotero_id, citekey, title, authors, year, type, publication, DOI, URL, collection, tags, status, prioridade)
- **Body em Markdown** com seções pré-formatadas para fichamento (Resumo · Pontos-chave · Como uso na dissertação · Conexões · Notas pessoais)
- **Tags Zotero preservadas** (no frontmatter + na seção "Tags Zotero originais" do body, com acentos e espaços)

### Por que via script Python (e não só pelo plugin Obsidian Zotero Integration)

O plugin **Zotero Integration** é excelente para uso contínuo (importar uma ref por vez durante a escrita). Mas para o **bootstrap inicial** (importar todas as 1.000+ refs do seu Zotero de uma vez), o script é mais rápido, idempotente e auditável.

Você usa o **script no início** (bootstrap) e o **plugin no dia-a-dia** (importar refs novas conforme você as cria).

### Como rodar

1. Copie o script [`scripts/export_zotero_to_vault.py`](../scripts/export_zotero_to_vault.py) para a pasta `_meta/scripts/` do seu vault (ou para qualquer lugar)
2. Edite as variáveis no topo do script:
   ```python
   ZOTERO_DB = "C:/Users/<seu-user>/Zotero/zotero.sqlite"
   VAULT_REFS = Path(r"C:\Users\<seu-user>\Documents\<seu-vault>\20 - Referencias")
   COLLECTIONS_FOLDERS = {
       "P1_TemaPrimario": "P1_TemaPrimario",
       # ... ajuste para suas collections
   }
   ```
3. Rode:
   ```bash
   python export_zotero_to_vault.py
   ```

### O que esperar

Para 1.893 referências, leva ~15 segundos. Saída:

```
Lendo Zotero (read-only)...
Total items: 1893
OK -- 1893 notas, 0 erros, 12105 atribuicoes de tag preservadas.

Por folder:
  _imports/pedagogica                      717
  _imports/capes-scholar                   428
  _imports/mestrado                        337
  _imports/busca-dirigida                  333
  P1_Letramento                            59
  P4_Teorico                               17
  _sem-collection                            2
```

### Exemplo de nota gerada

Veja [`exemplos/nota-referencia-exemplo.md`](../exemplos/nota-referencia-exemplo.md).

### ⚠️ Armadilha: Zotero rodando trava o sqlite

O Zotero, quando aberto, tem lock exclusivo sobre o `zotero.sqlite`. Você **não pode** abrir o arquivo em modo normal:

```python
# ISSO FALHA com Zotero rodando:
conn = sqlite3.connect('zotero.sqlite')
```

A solução: usar **URI com modo read-only e immutable**:

```python
# ISSO FUNCIONA mesmo com Zotero rodando:
uri = 'file:C:/Users/<user>/Zotero/zotero.sqlite?mode=ro&immutable=1'
conn = sqlite3.connect(uri, uri=True)
```

O modo `immutable=1` ignora o lock e oferece uma view consistente do snapshot atual. **Não escreve** — é só leitura.

### Idempotência

O script é **idempotente**: se a nota já existe (mesmo citekey), pula. Você pode rodar quantas vezes quiser. Para refazer tudo do zero (perdendo anotações manuais nas notas existentes), apague `20 - Referencias/*/*.md` antes de rodar.

## 4.3 Etapa 2 — Indexar o vault com Graphify

### O que essa etapa faz

Gera um **knowledge graph** a partir do conteúdo do vault Obsidian:
- **Nodes** = arquivos .md + conceitos extraídos
- **Edges** = referências cruzadas (wiki-links, tags compartilhadas, semelhança semântica)
- **Hyperedges** = grupos de 3+ nodes participando do mesmo conceito
- **Communities** = clusters detectados via Louvain (ou Graspologic)

### Como rodar

#### Opção A — Skill Claude Code

Se você instalou a skill `/graphify` no Claude Code:

```
/graphify "C:\Users\<user>\Documents\<seu-vault>" --update
```

A skill orquestra:
1. Detect dos arquivos do vault
2. Dispatch de subagents em paralelo para extração semântica (LLM)
3. Merge dos resultados
4. Build do grafo + cluster + community labels
5. Geração do HTML + JSON + report

Custo aproximado: para um vault de 1.900 notas (Markdown puro), ~500k-1M tokens. Tempo: 3-10 minutos.

#### Opção B — CLI direta

```bash
cd ~/Documents/<seu-vault>
graphify update . --force
```

Limitação: a CLI direta só usa AST (não LLM), então para Markdown puro gera poucos edges. Para corpus rico, prefira a skill.

### Output esperado

```
<seu-vault>/graphify-out/
├── graph.json          # nodes + edges em formato GraphRAG-ready
├── graph.html          # visualização interativa (abre no browser)
├── GRAPH_REPORT.md     # relatório em texto com god nodes, surprises, questions
├── manifest.json       # snapshot do filesystem para próximo --update
└── cache/              # caches LLM para incremental
```

### Como ler o `GRAPH_REPORT.md`

Três seções importantes:

1. **God Nodes** — os nodes mais conectados. São suas **abstrações centrais**. Em pesquisa, costumam ser conceitos-chave (ex.: `letramento_digital`, `formacao_docente`, `inteligencia_artificial`).

2. **Surprising Connections** — arestas `INFERRED` (deduzidas pelo LLM) que vinculam nodes em communities diferentes. São candidatas a **insights** que você não tinha visto.

3. **Suggested Questions** — perguntas que o grafo é uniquamente capaz de responder (ex.: "Por que `NIT-CEUNSP` conecta `justificativa institucional` a `cluster científico Campinas`?").

### Quando rodar

- **1ª vez**: depois do bootstrap das refs (Etapa 1). Pode ser caro em tokens — vale fazer 1× e cachear.
- **Atualizações**: usar `--update` (incremental). Só re-processa arquivos modificados.
- **Antes de capítulos teóricos**: rodar para descobrir conexões que talvez você não tenha mapeado.

### ⚠️ Armadilha: ECC vs general-purpose subagents

Se você usa Claude Code com plugin ECC instalado, ele adiciona um agent chamado **`code-explorer`** que é **read-only** (tipo Explore). A skill `/graphify` precisa de subagents que possam **escrever em arquivo** (`.graphify_chunk_NN.json`). Use `subagent_type="general-purpose"` explicitamente.

## 4.4 Etapa 3 — Gerar mapas VOSviewer

### O que essa etapa faz

Produz os 3 mapas bibliométricos clássicos:
- **Network** — clusters por co-ocorrência de keywords
- **Density** — heatmap de concentração temática
- **Overlay** — mesmo network com superposição temporal (ano de publicação)

### Pré-requisito — Exportar RIS atualizado do Zotero

1. No Zotero, selecione a coleção que você quer mapear (ex.: biblioteca inteira ou só uma collection)
2. **File → Export Library**
3. Format: **RIS**
4. Marque **Keep updated** se quiser auto-export
5. Salve em `_meta/exports/corpus_<data>.ris`

### Como rodar no VOSviewer

1. Abra VOSviewer
2. **File → Create a map → Create a map based on bibliographic data**
3. **Read data from bibliographic database files → Choose files → seu RIS**
4. **Co-occurrence → All keywords** (ou Author keywords, dependendo da sua estratégia)
5. **Minimum number of occurrences of a keyword**: tente 5 ou 10 (filtra ruído)
6. **Map options**: deixe padrão
7. **Finish**

VOSviewer mostra o mapa. Para exportar:
- **File → Save as → PNG** (três vezes, uma para cada visualização: Network, Density, Overlay)
- Salve em `50 - Analises/vosviewer-<data>/`

### Aplicar thesaurus customizado

Antes de gerar o mapa final, aplique seu thesaurus (consolidação de termos):

1. Crie um arquivo `vosviewer_thesaurus.csv`:
   ```
   label,replace by
   ia,inteligencia artificial
   ai,artificial intelligence
   teacher education,formacao docente
   teachers,docentes
   digital literacy,letramento digital
   ```
2. No assistente de criação de mapa, **upload thesaurus** quando perguntado
3. VOSviewer aplica o mapping antes de calcular co-ocorrências

### Ler o mapa **Overlay temporal**

O Overlay é o **mapa mais informativo** para detectar mudanças no foco do seu corpus.

- **Cor azul escuro** = ref publicada mais antiga (ex.: 2021)
- **Cor amarela** = ref publicada mais recente (ex.: 2024)

Termos que aparecem em **amarelo concentrado** indicam **temas em ascensão**.

Termos em **azul escuro** são **temas que dominavam mas perderam espaço**.

🎯 Para a sua tese: capture screenshot do overlay, anote os clusters de cada era (azul/verde/amarelo) e use como evidência bibliométrica de shift temático no capítulo de revisão de literatura.

## 4.5 Etapa 4 — Detectar shifts temáticos (comparação RIS × Zotero)

### Quando essa etapa faz sentido

Se você gerou um mapa VOSviewer em algum momento passado, e quer comparar com seu corpus Zotero atual (que cresceu), essa análise revela:

- Quais refs novas entraram no Zotero depois do último RIS
- Quais tags/keywords novas surgiram
- Quais co-ocorrências apareceram OU fortaleceram (clusters emergentes)
- Quais eixos temáticos cresceram em proporção (shift estrutural)

### Como rodar

Use o script [`scripts/analise_shift_v2.py`](../scripts/analise_shift_v2.py).

1. Edite as variáveis no topo:
   ```python
   ZOTERO_DB = "C:/Users/<user>/Zotero/zotero.sqlite"
   RIS_FILE = "C:/Users/<user>/Documents/.../corpus_antigo.ris"
   ```
2. Edite o léxico `LEX` para refletir os eixos temáticos da sua pesquisa:
   ```python
   LEX = {
       'tecnologia': ['ai', 'machine learning', 'platform', ...],
       'ciencias_humanas': ['philosophy', 'sociology', 'ethics', ...],
       'pedagogia_aprendizagem': ['learning', 'curriculum', 'student', ...],
       'covid_excluido': ['covid', 'pandemic', ...],  # opcional
   }
   ```
3. Rode:
   ```bash
   python analise_shift_v2.py
   ```

### Output esperado

```
RIS refs: 1443 | Zot refs: 1824

=== Refs com tag do eixo ===
Eixo                                RIS      %      Zot      %     Δ pp
tecnologia                         1066  73.9%     1245  68.3%    -5.6
ciencias_humanas                    895  62.0%     1026  56.2%    -5.8
pedagogia_aprendizagem              514  35.6%      792  43.4%    +7.8

=== Co-ocorrência entre eixos ===
Par                                                     RIS      Zot        Δ
ciencias_humanas + tecnologia                           651      747      +96
ciencias_humanas + pedagogia_aprendizagem               487      595     +108
pedagogia_aprendizagem + tecnologia                     433      585     +152
```

### O que esses números significam

- **Δ pp negativo** = eixo perdeu peso relativo (mesmo crescendo em valor absoluto, cresceu menos que outros)
- **Δ pp positivo** = eixo ganhou peso relativo
- **Co-ocorrência crescendo** = clusters intersetoriais se fortalecendo (pedagogia + tecnologia, por exemplo)

### Como narrar isso na sua tese

O Cap. 6 deste livro tem exemplos de narrativas. A regra: **vá da observação visual (overlay VOSviewer) para a confirmação quantitativa (script Python)**. Não use o script como ponto de partida — use como validação.

## 4.6 Etapa 5 — Meta-grafo cross-vault

### Quando essa etapa faz sentido

Se você tem **múltiplos vaults Obsidian** (PKM pessoal + projeto institucional + dissertação, por exemplo), pode querer:

- Saber **quais conceitos aparecem em mais de um vault** (overlap)
- Detectar **conceitos isolados** em apenas um vault (gaps de governança)
- Cruzar buscas sem misturar conteúdo físico

O **meta-grafo** do Graphify resolve isso: gera um JSON unificado a partir de múltiplos `graph.json`, **mantendo cada vault em sua pasta original**.

### Como rodar

Pressuposto: cada vault já tem seu `graphify-out/graph.json` (Etapa 2 rodada em cada).

```bash
graphify merge-graphs \
  "C:/Users/<user>/.../vault1/graphify-out/graph.json" \
  "C:/Users/<user>/.../vault2/graphify-out/graph.json" \
  "C:/Users/<user>/.../vault3/graphify-out/graph.json" \
  --out "~/.graphify/meta-graph/merged-graph.json"
```

### Consultar o meta-grafo

```bash
graphify query "letramento digital docente" \
  --graph ~/.graphify/meta-graph/merged-graph.json

graphify path "<conceito A>" "<conceito B>" \
  --graph ~/.graphify/meta-graph/merged-graph.json

graphify explain "<conceito X>" \
  --graph ~/.graphify/meta-graph/merged-graph.json
```

### Análise de overlap

Para detectar conceitos compartilhados entre vaults, use [`scripts/compare_cooccurrence.py`](../scripts/compare_cooccurrence.py). Ele cruza nodes por label normalizada e por tokens, identificando:

- **Direct overlap** (mesma label nos dois vaults)
- **Substring overlap** (label parcial)
- **Conceitos isolados** (em um vault e não no outro)

### Por que isso importa

A regra de ouro de **vaults separados** é não misturar conteúdo de domínios diferentes (vida pessoal vs. projeto institucional vs. mestrado). Mas você ainda quer **buscar transversalmente** quando precisar.

O meta-grafo resolve essa tensão: **separação física** (cada vault na sua pasta) + **busca unificada** (via índice meta).

## 4.7 Versionamento e auditoria

Cada etapa do fluxo deve ser **rastreável**:

- Vault Obsidian: Git commit a cada 30s (plugin Obsidian Git)
- Scripts Python: versionados em `scripts/` no repo do livrinho
- Mapas VOSviewer: arquivos PNG datados (`50 - Analises/vosviewer-2026-05/`)
- RIS exportado: versionado com timestamp (`_meta/exports/corpus_2026-05-12.ris`)
- Análises de shift: arquivos `.md` em `50 - Analises/`

### Por que isso importa

Em pesquisa acadêmica, **reprodutibilidade** é critério de validade. Se você não consegue refazer o caminho que te levou a um achado bibliométrico, você não tem direito de afirmar o achado.

Versionar tudo te protege em três frentes:
- **Defesa**: você prova que a análise é reprodutível
- **Comunidade**: outros podem rodar seus scripts contra os próprios corpora
- **Sua memória futura**: 6 meses depois, você lembra o que fez

## 4.8 Ciclo recomendado

Para uso contínuo, sugiro este ciclo semanal:

| Frequência | Ação |
|---|---|
| **Diária** | Ficha refs novas que leu (no Obsidian, abrir nota da ref e preencher Pontos-chave + Como uso) |
| **Semanal** | Rodar `graphify update .` no vault de pesquisa |
| **Mensal** | Re-exportar RIS do Zotero + atualizar VOSviewer (mapas novos) |
| **Trimestral** | Rodar `analise_shift_v2.py` para detectar evolução do corpus |
| **Por capítulo** | Rodar `compare_cooccurrence.py` para encontrar refs-âncora cross-tema |

---

> 📚 **Próximo capítulo:** [06 — Análises possíveis](06-analises-possiveis.md)
