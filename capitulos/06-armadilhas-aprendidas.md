# Capítulo 6 — Armadilhas aprendidas

> Este capítulo é a lista de pegadinhas que custaram tempo durante o setup e os primeiros usos do pipeline. Cada armadilha vem com diagnóstico, sintoma observado, e solução. Leia antes de começar a trabalhar — vai economizar horas.

## 6.1 OneDrive sincronizando storage do Zotero

**Sintoma**: Zotero corrompe a database. Erro "I/O error" ou refs sumindo da lista.

**Diagnóstico**: O Zotero usa SQLite com WAL (Write-Ahead Logging). O OneDrive (e Dropbox, iCloud, Drive) sincroniza arquivos a cada mudança, criando **locks paralelos** no `.sqlite-wal` que corrompem o banco.

**Solução**:

1. Em **Edit → Preferences → Advanced → Files and Folders**, verifique o caminho da **Data Directory**.
2. **NÃO** ponha dentro de pasta sincronizada (`~/OneDrive`, `~/Dropbox`).
3. Use o local padrão (`~/Zotero/` no Windows, `~/Zotero/` no macOS).
4. Para backup, use **Zotero Sync** nativo (servidor da própria Zotero), não OneDrive.

🎯 **Vault Obsidian, por outro lado, PODE ficar no OneDrive** — são arquivos `.md` texto puro, sem WAL. Sem risco de corrupção.

## 6.2 Subagent Claude Code sendo read-only quando precisava escrever

**Sintoma**: o pipeline Graphify falha porque os arquivos `.graphify_chunk_NN.json` não aparecem na pasta. Mensagem "chunk N missing from disk".

**Diagnóstico**: alguns subagents do ECC (plugin Everything Claude Code) são tipo **Explore** — só leem, não escrevem. Especialmente `code-explorer`. Quando a skill `/graphify` dispatch agents, se o tipo escolhido for read-only, eles tentam escrever e falham silenciosamente.

**Solução**:

Forçar `subagent_type="general-purpose"` explicitamente quando criar Agent calls:

```javascript
Agent({
  description: "Graphify chunk 1",
  subagent_type: "general-purpose",  // ← obrigatório se ECC instalado
  prompt: "...",
})
```

🎯 Se você usa só skills nativas (sem ECC), não tem esse problema. ECC trouxe muitos agents, alguns deles read-only.

## 6.3 Encoding UTF-8 no PowerShell

**Sintoma**: scripts Python imprimem caracteres `?` em vez de acentos. Comandos `graphify merge-graphs` falham com `UnicodeEncodeError: 'charmap' codec can't encode character '→'`.

**Diagnóstico**: o PowerShell em Windows usa por padrão **cp1252** (Latin-1 extended). Caracteres como `→` (seta), `é`, `ã`, símbolos matemáticos não estão no cp1252.

**Solução**:

Antes de rodar comandos com output Unicode pesado:

```bash
# PowerShell
$env:PYTHONIOENCODING = "utf-8"
```

```bash
# Git Bash
export PYTHONIOENCODING=utf-8
```

Ou setar permanentemente:

- **Windows**: Settings → Time & Language → Language & Region → Administrative Language Settings → Change system locale → **Use Unicode UTF-8 for worldwide language support**
- Reinicie o sistema

🎯 **Não use `cp1252` em pipelines de pesquisa em português.** Vai te custar tempo eternamente.

## 6.4 Better BibTeX exportando para pasta sincronizada simultaneamente

**Sintoma**: O `.bib` auto-exportado pelo Better BibTeX fica inconsistente. Plugin Obsidian Zotero Integration reclama de citation keys que não existem.

**Diagnóstico**: você pediu pro Better BibTeX exportar o `.bib` para uma pasta que está sincronizando ativamente (OneDrive, por exemplo). O sync pode mover o arquivo durante a escrita.

**Solução**:

Exportar para uma pasta **dentro do vault Obsidian** (vault está sincronizado via OneDrive sem problema, mas o ciclo de escrita é menor):

```
mestrado-vault/
  _meta/
    library.bib  ← aqui
```

E exclua `library.bib` do Git (já está no `.gitignore` do livrinho).

## 6.5 Léxico de classificação errando direção temporal do Overlay

**Sintoma**: você lê o Overlay do VOSviewer e conclui "tecnologia caiu, humanas subiram". Depois roda análise quantitativa e descobre que humanas caíram em densidade. Confusão sobre o argumento da tese.

**Diagnóstico**: dois erros possíveis:

**Erro A** — Confundir cor: muita gente lê **azul = recente** e **amarelo = antigo**. A escala padrão do VOSviewer é o contrário: **azul-escuro = primeiros anos do corpus**, **amarelo = últimos anos**. Sempre confira a legenda no canto inferior direito.

**Erro B** — Confundir prevalência visual com proporção: termos podem aparecer brilhantes no Overlay (amarelos) porque você adicionou refs recentes daquele tema. Mas em PROPORÇÃO do total, podem ter caído.

**Solução**:

Sempre faça **dupla validação**:

1. Leitura visual do Overlay (ganha intuição)
2. Análise quantitativa via script (`analise_shift_v2.py`) (ganha precisão)

Em caso de divergência, **dados quantitativos vencem**. Os mapas visuais servem pra fazer perguntas e narrar, não pra concluir.

## 6.6 Cluster COVID inflando a análise

**Sintoma**: você está pesquisando "ensino remoto no contexto da formação docente em IES brasileiras". Análises mostram cluster gigante chamado "COVID-19" dominando o mapa. Sua tese não é sobre pandemia.

**Diagnóstico**: refs de 2020-2022 sobre qualquer aspecto de educação têm tag automática `covid-19`, `pandemic`, `coronavirus` adicionadas pelo Zotero auto-tag ou pelo SciHub/CAPES quando você baixou em massa. Essas tags inflam contagens.

**Solução**:

Decisão metodológica: **excluir COVID se a análise é pós-pandêmica**.

Como excluir:

1. **No Zotero**: criar tag `_excluir_da_bibliometria` e atribuir manualmente às refs covid. Filtrar no VOSviewer.
2. **No VOSviewer**: adicionar termos COVID ao **thesaurus** como `replace by ""` (string vazia) — isso remove o termo do mapa.
3. **Em script Python**: filtrar antes do cálculo (veja `scripts/analise_shift_v2.py` para léxico COVID).

🎯 **Documente essa decisão** no apêndice metodológico da sua tese. Banca pode questionar — e você precisa ter resposta.

## 6.7 `showTags: true` no graph view do Obsidian poluindo visualização

**Sintoma**: o graph view do Obsidian mostra milhares de pontinhos verdes espalhados, mais que o número de notas. Difícil ver os clusters.

**Diagnóstico**: você habilitou **Show tags** no graph view. Cada tag única vira um node. Se você tem 2.500 tags únicas no Zotero (export gerou tags como properties), seu graph tem ~2.500 nodes verdes extras.

**Solução**:

- No painel direito do graph view, desligue **Mostrar tags**
- OU edite `.obsidian/graph.json` linha `"showTags": false`

Agora você só vê notas (.md) como nodes, e arestas só onde há `[[wikilinks]]` reais.

🎯 Tags são úteis pra **filtrar grupos por cor** (regras de grupo no painel direito), não pra ver como nodes individuais. Use o **Tag Pane** lateral pra explorar tags.

## 6.8 Cache de Graphify levando a falha em re-run

**Sintoma**: você roda `graphify update .` esperando re-processar arquivos modificados. Ele responde "0 files changed". Mas você mudou conteúdo.

**Diagnóstico**: o Graphify tem cache em `graphify-out/cache/` que indexa por hash de conteúdo. Se você mudou só metadados (mtime sem mudar bytes), o cache acha que está tudo igual.

**Solução**:

Força a re-extração:

```bash
graphify update . --force
```

OU limpe o cache manualmente:

```bash
rm -rf graphify-out/cache/
graphify update .
```

🎯 Não cacheie `graphify-out/cache/` no git. Inclua no `.gitignore`.

## 6.9 Refs no Zotero sem DOI fazendo cruzamento RIS×Zotero falhar

**Sintoma**: você exporta RIS do Zotero, importa em outra ferramenta, e várias refs aparecem duplicadas.

**Diagnóstico**: o cruzamento por DOI é o método mais preciso. Refs sem DOI caem em cruzamento por **título normalizado**, que falha com:
- Acentos diferentes (`educação` vs `educacao`)
- Pontuação (`Vol. 12` vs `Vol 12`)
- Subtítulos truncados

**Solução**:

1. No Zotero, periodicamente rode **Edit → Find Item by DOI** para refs sem DOI
2. Use o plugin **Zotero Robust Links** para buscar metadados que o Zotero não pegou
3. Em scripts, faça cascata: tentar DOI → tentar título normalizado completo → tentar primeiros N caracteres do título

🎯 Idealmente, 90%+ das suas refs deveriam ter DOI. Auto-tag inflação MeSH é menos problema que falta de DOI.

## 6.10 Esquecer de versionar antes de mudanças grandes

**Sintoma**: você roda script que sobrescreve 1.893 notas. Algumas tinham fichamento manual seu. Perdeu tudo.

**Diagnóstico**: scripts batch são poderosos. Sem versionamento, são também perigosos.

**Solução**:

Antes de **qualquer operação de massa** (script que escreve em muitos arquivos), **commit o estado atual**:

```bash
cd <vault>
git add -A
git commit -m "snapshot before <script_name>"
git tag pre-<script_name>  # tag para retorno fácil
```

Se algo der errado:

```bash
git reset --hard pre-<script_name>
```

🎯 Plugin **Obsidian Git** com auto-commit a cada 30s te dá segurança contínua, mas tag manual antes de operações grandes é melhor.

## 6.11 Confundir vault privado com público no GitHub

**Sintoma**: você publicou um repo no GitHub achando que era privado. Descobre meses depois que seu fichamento de tese está público.

**Diagnóstico**: o `gh repo create` sem flag `--private` cria público por padrão (dependendo da versão).

**Solução**:

**Sempre explicite**:

```bash
gh repo create user/repo-name --private --source=. --remote=origin --push
```

Para auditar repos atuais:

```bash
gh repo list --visibility public
```

🎯 Vaults pessoais e profissionais → privados.  
🎯 Tutoriais e livros (este!) → públicos.  
🎯 Em dúvida, comece privado. É fácil tornar público depois; o inverso requer apagar histórico.

## 6.12 Bonus: 5 hábitos que economizam horas

| Hábito | Frequência | Por quê |
|---|---|---|
| Rodar `git status` em todos vaults | Diária | Saber o que falta commitar |
| Re-exportar RIS do Zotero | Mensal | Manter VOSviewer atualizado |
| `graphify update .` no vault de pesquisa | Semanal | Grafo nunca fica obsoleto |
| Tag manual de refs novas (não só auto-tag) | Por leitura | Taxonomia consistente |
| Backup zotero.sqlite | Mensal | Sequencer evento Murphy |

---

> 📚 **Próximo capítulo:** [07 — Como replicar](07-replicacao.md)
