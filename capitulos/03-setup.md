# Capítulo 3 — Setup

> Este capítulo se faz **uma vez só**. Você vai gastar 2 a 3 horas. Depois, nunca mais precisa repetir. A recompensa: anos de pesquisa fluindo num pipeline que você controla.

## 3.1 Pré-requisitos

Antes de começar, garanta:

- **Windows 10/11** (este livro usa Windows como referência; equivalentes para macOS e Linux estão entre parênteses quando relevantes)
- **Conta GitHub** (para versionar os vaults — opcional mas fortemente recomendado)
- **Python 3.10+** instalado (verifique com `python --version` no terminal)
- **PowerShell** ou **Git Bash** (use Git Bash neste livro, mais consistente com Linux/macOS)
- **6 GB livres em disco** (Zotero + 3 vaults + caches diversos)

🎯 Se você não tem Python: instale via [python.org](https://python.org) ou via `winget install Python.Python.3.12`.

## 3.2 Instalando o Zotero

### Passo 1 — Download e instalação

1. Acesse https://www.zotero.org/download/
2. Baixe o Zotero 7+ para sua plataforma
3. Instale com as opções padrão
4. **NÃO** salve a pasta `storage/` dentro do OneDrive/Dropbox — o sqlite com WAL corrompe com sync em paralelo. Use o local padrão (`C:\Users\<user>\Zotero\`)

### Passo 2 — Instalar o Better BibTeX

O **Better BibTeX** é essencial para integração com Obsidian.

1. Baixe o `.xpi` em https://retorque.re/zotero-better-bibtex/installation/
2. No Zotero: **Tools → Add-ons → ⚙ → Install Add-on From File…**
3. Selecione o `.xpi` baixado
4. Reinicie o Zotero
5. Em **Edit → Preferences → Better BibTeX → Citation Keys**, configure:
   - Citation key format: `auth.lower + year + shorttitle.lower` (gera `silva2024letramento`)
   - Aplique a todas as refs existentes (botão **Refresh**)

### Passo 3 — Configurar auto-export (Better BibTeX)

Better BibTeX pode manter um arquivo `.bib` sempre atualizado:

1. Selecione uma coleção (ex.: sua biblioteca inteira ou a do mestrado)
2. **File → Export Library**
3. Format: **Better BibLaTeX** (ou Better BibTeX se preferir)
4. Marque **Keep updated**
5. Salve o arquivo em local conhecido (ex.: `~/Documents/<seu-vault-mestrado>/_meta/library.bib`)
6. Daí em diante, qualquer mudança no Zotero atualiza o `.bib` automaticamente

### Passo 4 — Estilo de citação ABNT

1. **Edit → Preferences → Cite → Styles → Get additional styles…**
2. Procure por **ABNT (Universidade Federal do Paraná)** ou **ABNT (Universidade de São Paulo)**
3. Instale o que melhor representa seu programa de pós-graduação

🎯 Para mestrado/doutorado brasileiro, eu recomendo o estilo da **Universidade de São Paulo** que segue a NBR 6023:2018 mais fielmente.

### Passo 5 — Configurar tags

Tags no Zotero são o esqueleto da sua taxonomia. Recomendações:

- **Tags com prefixo padronizado** facilitam filtrar:
  - `gap_X` para gaps na sua dissertação (ex.: `gap_dissertacao_letramento`)
  - `teoria_X` para autores-fonte (ex.: `teoria_ausubel`, `teoria_vygotsky`)
  - `fonte_X` para origem da ref (ex.: `fonte_scholar`, `fonte_capes`)
  - `status_X` para etapas de leitura (ex.: `status_a_ler`, `status_fichado`)
- Tags com **espaços e maiúsculas** funcionam, mas dificultam scripting. Prefira `gap_x` a `Gap X`.
- **Desligue auto-tagging** (em **Edit → Preferences → General**) se ele vier ativo — vai poluir sua taxonomia com tags MeSH genéricas (`Humans`, `Article`, etc.) que você terá que filtrar depois.

## 3.3 Instalando o Obsidian

### Passo 1 — Download

1. Acesse https://obsidian.md
2. Baixe e instale a versão para sua plataforma
3. Abra o Obsidian — vai aparecer o vault switcher

### Passo 2 — Criar o vault da sua pesquisa

🎯 **Decisão importante**: tenha **vaults separados** para domínios diferentes da sua vida acadêmica. Eu uso 3:

- **Cerebro** (PKM pessoal — projetos, decisões, diários, capturas rápidas)
- **anamnese-vault** (projeto institucional — produto Anamnese, NIT-CEUNSP)
- **mestrado-vault** (dissertação, referências do Zotero, escrita de capítulos)

Cada vault é uma pasta separada. Eles podem dialogar via **meta-grafo Graphify** (ver Cap. 6) sem misturar conteúdo.

Para criar o vault da pesquisa:

1. No Obsidian Vault Switcher: **Open folder as vault**
2. Crie uma pasta nova: `~/Documents/<sua-instituicao>/mestrado-vault` (ou nome que faça sentido)
3. Selecione essa pasta
4. **Trust author and enable plugins**

### Passo 3 — Estrutura PARA dentro do vault

A estrutura **PARA** (Tiago Forte: Projects, Areas, Resources, Archives) é uma das mais robustas para gestão pessoal de conhecimento. Adapto para o contexto de mestrado/doutorado:

```
<seu-vault>/
├── 00 - Inbox/              # captura rápida, ideias soltas a processar
├── 10 - Tese/               # capítulos em construção (1 arquivo por capítulo)
├── 20 - Referencias/        # 1 nota por entrada do Zotero (auto-gerada)
│   ├── P1_TemaPrimario/
│   ├── P2_TemaSecundario/
│   ├── P3_TemaTerciario/
│   ├── P4_BaseTeorica/
│   └── _imports/            # refs ainda não categorizadas
├── 30 - Conceitos/          # ideias centrais (subsunçor, organizador prévio, etc.)
├── 40 - Disciplinas/        # material das disciplinas do mestrado
├── 50 - Analises/           # análises bibliométricas, VOSviewer maps, scripts
├── 60 - Orientacao/         # encontros com orientador, feedback, marcos
├── 90 - Arquivo/            # rascunhos antigos, versões superadas
└── _meta/
    ├── dashboard.md
    ├── templates/
    │   ├── nota-referencia.md
    │   ├── capitulo.md
    │   ├── reuniao-orientacao.md
    │   └── daily.md
    └── attachments/
```

Crie as pastas vazias no Obsidian (clique direito → New folder) ou via terminal:

```bash
cd ~/Documents/mestrado-vault
mkdir -p "00 - Inbox" "10 - Tese" "20 - Referencias" "30 - Conceitos" \
         "40 - Disciplinas" "50 - Analises" "60 - Orientacao" "90 - Arquivo" \
         "_meta/templates" "_meta/attachments"
```

### Passo 4 — Plugins essenciais

Em **Settings → Community plugins → Turn on community plugins**, instale:

| Plugin | Para que serve |
|---|---|
| **Dataview** | Queries SQL-like nas notas (dashboards dinâmicos) |
| **Templater** | Templates dinâmicos com JavaScript |
| **Tasks** | Gestão `- [ ]` avançada (filtros, repetição, due dates) |
| **Obsidian Git** | Versionamento automático (commit a cada 30s, push a cada 60s) |
| **Zotero Integration** | Sincronização contínua com Zotero via Better BibTeX |
| **Calendar** | Daily notes integrado a calendário |
| **Excalidraw** (opcional) | Diagramas livres tipo whiteboard |

### Passo 5 — Configurar templates

Em **Settings → Templates → Template folder location**, aponte para `_meta/templates`.

Crie templates essenciais (use os do livrinho como base):

- `_meta/templates/nota-referencia.md` — template para fichamento de ref Zotero
- `_meta/templates/capitulo.md` — template para começar um capítulo da tese
- `_meta/templates/reuniao-orientacao.md` — template para registrar encontros
- `_meta/templates/daily.md` — daily note

Os templates completos estão em [`exemplos/`](../exemplos/) deste repositório.

### Passo 6 — Configurar Zotero Integration

Após instalar o plugin **Zotero Integration**:

1. **Settings → Zotero Integration**
2. **Database**: aponte para o `.bib` do auto-export do Better BibTeX (`_meta/library.bib`)
3. **Notes folder**: `20 - Referencias`
4. **Citation template**: vincule ao seu template `nota-referencia.md`
5. **Atalhos**:
   - `Ctrl+Shift+O` — Insert citation inline (busca no Zotero)
   - `Ctrl+Shift+I` — Import note from Zotero (gera .md completa)

### Passo 7 — Configurar Obsidian Git

1. Plugin **Obsidian Git** → Settings
2. **Vault backup interval (minutes)**: 0.5 (auto-commit a cada 30s)
3. **Auto pull interval (minutes)**: 1
4. **Auto push interval (minutes)**: 1
5. **Commit message**: `vault: backup {{date}} {{hostname}}`

Pra isso funcionar, o vault precisa ter um remote Git configurado. Veja §3.6.

## 3.4 Instalando o Graphify

### Passo 1 — Instalar via uv

O **uv** é o instalador Python mais rápido em 2025. Se você não tem:

```bash
# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Depois:

```bash
uv tool install graphifyy
```

(Sim, com 2 y's no fim — o pacote no PyPI é `graphifyy`.)

Verifique:

```bash
graphify --help
```

### Passo 2 — Instalar a skill `/graphify` no Claude Code

Se você usa Claude Code, instale a skill que orquestra o pipeline completo (extração com subagents em paralelo):

```bash
graphify claude install
```

Isso adiciona uma seção no seu `~/.claude/CLAUDE.md` global e um hook `PreToolUse` que consulta o grafo automaticamente.

### Passo 3 — Hook de git post-commit (opcional)

Para auto-atualizar o grafo depois de cada commit no vault:

```bash
cd ~/Documents/mestrado-vault
graphify hook install
```

Daí em diante, todo `git commit` no vault dispara `graphify update .` em background.

## 3.5 Instalando o VOSviewer

### Passo 1 — Download

1. https://www.vosviewer.com/download
2. Baixe a versão para sua plataforma (Windows: ZIP; macOS: DMG)
3. Extraia em local conhecido (ex.: `~/Documents/CEUNSP MED/VOSViewer/`)
4. Execute `VOSviewer.exe` (Windows) ou `.app` (macOS)

### Passo 2 — Verificar Java

VOSviewer precisa de **Java 11+**. Se não tem:

```bash
# Windows
winget install Oracle.JavaRuntimeEnvironment
```

### Passo 3 — Familiarizar com a UI

Recomendo abrir um exemplo embutido (File → Open) e clicar pelas abas:
- **Items**: lista de termos/refs do mapa
- **Links**: lista de conexões (pares de termos com co-ocorrência)
- **Network/Density/Overlay**: três visualizações do mesmo mapa

## 3.6 Versionamento Git dos vaults

Para cada vault, configurar Git:

```bash
cd ~/Documents/mestrado-vault
git init -b main
git config user.email "seu@email.com"
git config user.name "Seu Nome"

# Adicionar .gitignore
cat > .gitignore <<EOF
.obsidian/workspace.json
.obsidian/cache
.obsidian/graph.json
graphify-out/cache/
graphify-out/.graphify_*
_meta/library.bib   # gerado pelo Better BibTeX
.DS_Store
Thumbs.db
EOF

git add -A
git commit -m "init: skeleton do vault"
```

Para subir pro GitHub (privado):

```bash
gh repo create ricamesq/mestrado-vault --private --source=. --remote=origin --push
```

Substitua `ricamesq` pelo seu username.

### Por que privado

Se o vault contém:
- Fichamentos com ideias originais ainda não publicadas
- Notas de orientação confidenciais
- PDFs de refs com direito autoral
- Anotações pessoais

→ deve ser **privado**. Você pode tornar público depois de defendido, se quiser.

## 3.7 Instalando o Claude Code

### Passo 1 — Conta Anthropic

1. https://console.anthropic.com — crie conta
2. Decida entre:
   - **Claude Pro** ($20/mês com limite alto, sem cobrança por token)
   - **API pay-per-use** (preço por token, mais flexível)

### Passo 2 — Instalar Claude Code CLI

```bash
# macOS/Linux
curl -fsSL https://claude.ai/install.sh | bash

# Windows
# Baixe o instalador em https://claude.ai/code
```

Verifique:

```bash
claude --version
```

### Passo 3 — Autenticar

```bash
claude login
```

Vai abrir o navegador para você logar.

### Passo 4 — Instalar plugins úteis (opcional)

```bash
# Plugin Everything Claude Code (60 agents + 225 skills)
claude plugin marketplace add https://github.com/affaan-m/everything-claude-code
claude plugin install ecc@ecc
```

Veja Cap. 9 (anexos) para o catálogo completo.

## 3.8 Checklist de sanity

Antes de prosseguir, verifique cada item:

- [ ] Zotero abre e tem pelo menos 10 refs
- [ ] Better BibTeX instalado e auto-export funciona (arquivo `.bib` se atualiza)
- [ ] Obsidian abre o vault com a estrutura PARA
- [ ] Plugins Dataview, Templater, Tasks, Git, Zotero Integration ativos
- [ ] Graphify roda `graphify --help`
- [ ] VOSviewer abre e mostra exemplo embutido
- [ ] Claude Code roda `claude --version`
- [ ] Git inicializado no vault e remote GitHub configurado (opcional)
- [ ] Você consegue rodar Python 3.10+ no terminal

Se tudo OK, parta para o **Cap. 4** se quiser ver o pipeline orquestrado pelo Claude Code, ou direto para o **Cap. 5** — o fluxo integrado.

---

> 📚 **Próximo capítulo:** [04 — Setup via Claude Code (modo agêntico)](04-setup-via-claude-code.md)
>
> 🤖 Ou pule direto para: [05 — Fluxo integrado](05-fluxo-integrado.md) (se já fez o setup)
