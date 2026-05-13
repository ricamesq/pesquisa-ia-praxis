# Capítulo 5 — Análises possíveis

> Tendo seu corpus organizado nos cinco sistemas integrados (Cap. 5), abre-se um leque de análises que antes seriam inviáveis pra uma única pessoa em tempo razoável. Este capítulo cataloga as **seis análises mais úteis** e mostra **como interpretar cada resultado** sem cair em armadilhas comuns.

## 5.1 Análise descritiva — o que você tem

A primeira pergunta a fazer ao seu corpus, na ordem:

| Pergunta | Onde responder | Como |
|---|---|---|
| Quantas refs eu tenho? | Zotero ou Obsidian | SQL contra `zotero.sqlite` ou query Dataview no vault |
| Por ano de publicação? | Zotero | `Items by Type → Year` ou query SQL |
| Por idioma? | Zotero | `Items by Language` (se preenchido) |
| Quais autores aparecem com mais frequência? | Script Python | Query `itemCreators` no sqlite |
| Quais journals/conferences? | Script Python | Query `publicationTitle` |
| Quantas refs têm DOI? | Script Python | `WHERE fieldName='DOI'` |
| Tags mais frequentes? | Script Python ou Dataview | `GROUP BY t.name ORDER BY COUNT DESC` |

🧰 **Comando prático**: para fazer descrição rápida do corpus, salve este script como `descritiva.py`:

```python
import sqlite3
uri = 'file:C:/Users/<user>/Zotero/zotero.sqlite?mode=ro&immutable=1'
conn = sqlite3.connect(uri, uri=True)
cur = conn.cursor()

# Total por tipo
cur.execute("""SELECT typeName, COUNT(*) FROM itemTypes JOIN items USING (itemTypeID)
               WHERE itemID NOT IN (SELECT itemID FROM deletedItems)
               GROUP BY typeName ORDER BY 2 DESC""")
print("=== Itens por tipo ===")
for r in cur.fetchall(): print(f"  {r[1]:5d}  {r[0]}")

# Refs por ano
cur.execute("""SELECT substr(value, 1, 4) AS year, COUNT(*)
               FROM itemDataValues JOIN itemData USING (valueID)
               WHERE fieldID = (SELECT fieldID FROM fields WHERE fieldName='date')
               GROUP BY year ORDER BY year DESC LIMIT 15""")
print("\n=== Refs por ano (últimos 15) ===")
for r in cur.fetchall(): print(f"  {r[0]}: {r[1]}")
```

### Por que começar pelo descritivo

Pesquisador iniciante tende a pular esse passo (parece chato). É erro. Você precisa **saber o tamanho e a forma do seu corpus** antes de qualquer análise sofisticada. Senão você fala "minha pesquisa cobre a literatura..." sem ter ideia se cobre, e a banca te pega.

## 5.2 Análise temporal — onde o corpus está

Pergunta: **como o foco temático do meu corpus mudou ao longo dos anos?**

A ferramenta principal aqui é o **mapa Overlay do VOSviewer** (Cap. 5 §5.4).

### O que procurar no Overlay

1. **Clusters em amarelo** (publicações recentes) — temas em ascensão.
2. **Clusters em azul-escuro** (publicações antigas) — temas que dominavam.
3. **Termos verdes (transição)** — temas que cresceram durante o período e estabilizaram.

### Cuidado interpretativo

🎯 **Não confunda "publicado recente" com "tema em alta"**. Termos podem aparecer em amarelo no Overlay simplesmente porque sua busca recente trouxe mais material desse tema. O Overlay reflete **seu corpus**, não o estado real da literatura.

🎯 **Análise temporal precisa de filtro de pandemia**. Refs de 2020-2022 sobre educação foram inundadas por COVID. Se você está pesquisando temas adjacentes (e-learning, distance education), considere **excluir tags `covid`, `coronavirus`, `pandemic` do thesaurus VOSviewer** antes do build. Este livro inclui [`scripts/analise_shift_v2.py`](../scripts/analise_shift_v2.py) que já faz isso.

### Validação quantitativa

O Overlay é visual. Para fundamentar argumento na tese, complemente com **análise quantitativa**:

```bash
python scripts/analise_shift_v2.py
```

Produz tabela:

```
Eixo                                RIS      %      Zot      %     Δ pp
tecnologia                         1066  73.9%     1245  68.3%    -5.6
ciencias_humanas                    895  62.0%     1026  56.2%    -5.8
pedagogia_aprendizagem              514  35.6%      792  43.4%    +7.8
```

A coluna **Δ pp** (delta em pontos percentuais) é o que importa para fundamentar shift. Mudança de **+/- 5 pp** em proporção é significativa estatisticamente; +/- 8 pp é fortíssima.

### Narrativa típica

> "Entre 2021 e 2024, a vertente tecnológica do corpus recuou em 5,6 pontos percentuais (de 73,9% para 68,3% das refs), enquanto a vertente pedagógica avançou 7,8 pontos percentuais (35,6% → 43,4%). O Overlay do VOSviewer (Figura X) corrobora visualmente esse deslocamento: as publicações de 2024 (em amarelo) concentram-se nos clusters humanístico-pedagógicos, enquanto as de 2021-2022 (em azul) ainda eram dominadas por termos de tecnologia educacional aplicada (educational technology, learning analytics, software)."

## 5.3 Análise de co-ocorrência — quais temas andam juntos

Pergunta: **quais temas aparecem juntos com frequência no meu corpus?**

A bibliometria chama isso de **co-citation** (refs citadas juntas) ou **co-occurrence** (palavras-chave que aparecem juntas). Para uma única pessoa, **co-occurrence de keywords/tags** é o mais prático.

### Como rodar

Use [`scripts/compare_cooccurrence.py`](../scripts/compare_cooccurrence.py).

### O que cada output significa

```
=== Co-ocorrência entre eixos ===
Par                                                     RIS      Zot        Δ
eixo_A + eixo_B                                         650      750     +100
eixo_A + eixo_C                                         430      580     +150
eixo_B + eixo_C                                         485      595     +110
```

(Exemplo ilustrativo — adapte os eixos à sua taxonomia.)

Como ler:
- **+100 em A + B**: aumentou de 650 para 750 refs que têm tag dos dois eixos. Isso indica que a literatura está **dialogando** mais entre esses dois temas.
- **+150 em A + C** (maior aumento absoluto): essa é a intersecção que mais ganhou peso. Tema natural pra capítulo de revisão.
- **+110 em B + C**: outro cruzamento ascendente, requer leitura interpretativa para entender a direção do diálogo.

### Pares "novos" vs "fortalecidos"

O script também distingue:
- **Pares novos** = co-ocorrências que não existiam no corpus antigo (RIS). São temas **emergentes**.
- **Pares fortalecidos** = co-ocorrências que existiam mas cresceram em peso. São temas **consolidando**.

### Cuidado interpretativo

⚠️ Co-ocorrência **não é causalidade**. Que duas tags apareçam juntas em refs não significa que os autores estão fazendo o cruzamento conceitual. Pode ser só keyword inflation (autores adicionam muitas tags para SEO acadêmico).

🎯 Para validar, **leia uma amostra** das refs com aquela co-ocorrência. Se 7 em 10 fazem ponte explícita, o cluster é real. Se 3 em 10, é ruído.

## 5.4 Detecção de gaps — o que falta

Pergunta: **quais autores/temas estão sub-representados no meu corpus?**

Essa pergunta tem duas variantes:

### Variante A — Gap em relação à comunidade

"O Ausubel é citado em N% dos papers do meu campo. No meu corpus, está em M%. Se N >> M, eu tenho gap."

Você compara seu corpus contra um **corpus de referência** (ex.: Web of Science query do seu campo). Custoso mas viável.

### Variante B — Gap em relação à sua própria taxonomia

"Eu defini tags `teoria_ausubel`, `teoria_vygotsky`, `teoria_freire`. Quantas refs têm cada uma?"

Isso é trivial via SQL ou Dataview. Te revela **se você está balanceando suas bases teóricas** ou se uma está dominando.

```python
# Quantas refs por teoria?
cur.execute("""SELECT t.name, COUNT(DISTINCT it.itemID) FROM tags t
               JOIN itemTags it USING (tagID) JOIN items i USING (itemID)
               WHERE i.itemID NOT IN (SELECT itemID FROM deletedItems)
                 AND t.name LIKE 'teoria_%'
               GROUP BY t.name ORDER BY 2 DESC""")
```

### Variante C — Gap em relação ao thesaurus VOSviewer

Se você criou um thesaurus customizado (consolidação manual de termos), pode comparar **quais tags Zotero existem mas não foram consolidadas**.

```bash
python scripts/gen_candidatas.py
```

Output: lista de tags candidatas a entrar no thesaurus, categorizadas (tecnologia, pedagogia, COVID, MeSH ruidoso).

## 5.5 Análise de meta-grafo cross-vault

Pergunta: **quais conceitos aparecem em mais de um vault meu?**

Útil se você tem múltiplos vaults (PKM pessoal + projeto institucional + dissertação). Veja Cap. 5 §5.6.

### Tipos de overlap a procurar

1. **Conceitos compartilhados legítimos**: aparecem em ambos com função análoga
   - Ex.: `NIT-CEUNSP` aparece no PKM (como projeto pessoal) e no vault institucional (como entidade administrativa)
2. **Conceitos compartilhados COM função diferente**: aparecem em ambos mas significam coisas distintas
   - Ex.: `LGPD` no PKM = aspecto de propriedade intelectual; no vault institucional = dado sensível clínico
3. **Conceitos isolados em um vault**: pertinentes a um domínio só
4. **Duplicações reais** (mesmo conceito, fraseado diferente): candidatos a consolidação

### O que fazer com os resultados

- Conceitos **compartilhados com mesma função**: ok, são bridges entre seus mundos
- Conceitos **compartilhados com função diferente**: documente a diferença (evita confusão futura)
- Conceitos **duplicados**: consolide (sinônimo)
- Conceitos **isolados**: confirme que estão no vault certo (não erraram de pasta)

## 5.6 Análise de god-nodes e pontes (Graphify)

Pergunta: **quais conceitos sustentam toda a estrutura do meu corpus?**

O Graphify identifica **god nodes** (nós mais conectados) automaticamente. Veja `graphify-out/GRAPH_REPORT.md`.

### Tipos de god nodes a esperar

- **Projetos seus**: ex. `NIT-CEUNSP`, `Anamnese` (porque você os menciona em muitas notas)
- **Conceitos centrais da tese**: ex. `letramento_digital`, `formacao_docente`, `aprendizagem_significativa`
- **Pessoas-chave**: ex. orientador, autores citados em vários capítulos
- **Tags-âncora**: ex. `gap_dissertacao_eixo1`

### Bridge nodes (alta betweenness centrality)

São nodes que **conectam comunidades distintas**. Em um corpus de pesquisa, costumam ser conceitos transversais — provavelmente os mais valiosos para o argumento da tese.

Identifique-os com:

```bash
graphify explain "<nome do conceito>" --graph graphify-out/graph.json
```

A saída lista o grau e os vizinhos por comunidade. Quando um nó tem vizinhos em 3-4 comunidades diferentes, ele é ponte.

### Como usar isso na tese

Capítulo de fundamentação teórica deve **abrir e fechar com god nodes** — porque são as ideias que sustentam todo o resto.

Subseções devem ser organizadas por **bridge nodes** — porque eles fazem a conexão entre os campos disciplinares que você está atravessando.

Citações pontuais podem usar **nodes periféricos** — refs específicas que ancoram um ponto particular.

## 5.7 Análise por status de leitura

Pergunta: **das minhas refs, quantas eu já li, fichei, citei?**

O frontmatter da nota de referência (criada pelo script Etapa 1) inclui:

```yaml
status: a-ler  # a-ler | lendo | fichado | citado
prioridade: media  # alta | media | baixa
```

Você atualiza manualmente conforme avança.

### Dashboard recomendado

No dashboard do vault (`_meta/dashboard.md`), tenha esta query Dataview:

```dataview
TABLE WITHOUT ID
  status,
  length(rows) AS "Refs"
FROM "20 - Referencias"
WHERE type = "reference"
GROUP BY status
SORT length(rows) DESC
```

Output (exemplo ilustrativo, corpus de ~2.000 refs):

```
status        Refs
a-ler         1800
lendo            8
fichado         40
citado          90
```

Lê-se: **só ~5% foram efetivamente citadas em alguma escrita** — e ~92% nem foram lidas. Isso é normal num corpus bibliográfico amplo — a função do corpus é dar **profundidade defensiva** ("o que mais existe?") e cobertura ("o que falta?").

### Por que isso importa

🎯 **Não confunda volume com profundidade.** Ter milhares de refs no Zotero não te dá direito a dizer "minha pesquisa cobre essa literatura". Você cobre o que **fichou e citou** (~50-150 refs por capítulo, no máximo).

🎯 As outras refs servem para: (1) defesa quando perguntarem "e o autor X você considerou?"; (2) buscas pontuais por tema; (3) curadoria editorial (o que essa literatura está dizendo no agregado).

## 5.8 Análise de bibliometria comparativa (refs-charneira)

Pergunta: **quais refs do meu corpus combinam várias categorias da minha taxonomia?**

São as **refs-charneira**: ref que tem tags `teoria_X` + `gap_Y` + `conceito_Z` + `metodo_W` ao mesmo tempo. Tipicamente, são as refs mais valiosas para argumentação.

### Como rodar

```python
# Top 20 refs por contagem de tags
cur.execute("""
SELECT i.itemID, COUNT(it.tagID) AS n_tags,
       (SELECT idv.value FROM itemData id JOIN itemDataValues idv USING (valueID)
        JOIN fields f USING (fieldID)
        WHERE id.itemID=i.itemID AND f.fieldName='title' LIMIT 1) AS title
FROM items i JOIN itemTags it ON it.itemID = i.itemID
JOIN itemTypes itp USING (itemTypeID)
WHERE i.itemID NOT IN (SELECT itemID FROM deletedItems)
  AND itp.typeName NOT IN ('attachment','note','annotation')
GROUP BY i.itemID
ORDER BY n_tags DESC LIMIT 20
""")
```

### Filtro pela sua taxonomia

Limite às tags da sua taxonomia manual (descarta auto-tags MeSH):

```python
WHERE (t.name LIKE 'teoria_%' OR t.name LIKE 'gap_%' OR t.name LIKE 'fonte_%')
```

Daí pra cima fica fácil identificar as refs-âncora.

## 5.9 Síntese — quando usar cada análise

| Pergunta da pesquisa | Análise recomendada | Capítulo de uso |
|---|---|---|
| O que eu tenho? (descritivo) | §5.1 | Apêndice metodológico |
| Como o corpus mudou no tempo? | §5.2 (Overlay VOSviewer + script shift) | Cap. 2 (Revisão de literatura) |
| Quais temas dialogam? | §5.3 (co-ocorrência) | Cap. 2 (mapeamento conceitual) |
| O que falta no meu corpus? | §5.4 (gaps) | Justificativa / introdução |
| Como meus vaults se conversam? | §5.5 (cross-vault) | Apêndice metodológico |
| Quais conceitos sustentam tudo? | §5.6 (god nodes Graphify) | Cap. 1 (introdução) |
| Quanto eu já li/fichei? | §5.7 (status) | Cap. 3 (metodologia) |
| Quais refs são as mais densas? | §5.8 (refs-charneira) | Cap. 2 (revisão de literatura) |

---

> 📚 **Próximo capítulo:** [07 — Armadilhas aprendidas](07-armadilhas-aprendidas.md)
