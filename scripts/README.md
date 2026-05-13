# Scripts — Pesquisa IA Práxis

Coleção mínima de scripts Python para o pipeline descrito no livrinho. **Comentados para você adaptar.**

> ⚠️ **Edite a seção `CONFIG`** no topo de cada script antes de rodar. Os caminhos hardcoded apontam para `C:\Users\SEU_USUARIO\...` — substitua pelo seu.

## Pré-requisitos

- Python 3.10+
- `pip install` nada (todos usam apenas a stdlib — `sqlite3`, `re`, `pathlib`, `csv`, `unicodedata`)
- Zotero 7+ instalado, com `zotero.sqlite` no caminho padrão

## Scripts

### `export_zotero_to_vault.py`

Lê o `zotero.sqlite` em modo **read-only** (URI `?mode=ro&immutable=1`, portanto seguro rodar com Zotero aberto) e gera **1 nota `.md` por referência** no seu vault Obsidian.

- Idempotente: não sobrescreve notas existentes (preserva seu fichamento manual)
- Citation key no padrão `@SobrenomeAnoPrimeiraPalavra`
- Frontmatter YAML com `zotero_id`, `tags`, `collections`, `doi`, etc.
- Mapa configurável de **collection Zotero → subpasta destino**

**Uso típico:** primeiro bootstrap do vault. Roda em ~15 s para 2.000 refs.

### `analise_shift_v2.py`

Compara dois cortes do corpus (RIS exportado em data X **vs.** Zotero atual) classificando keywords/tags em 4 eixos temáticos:

- `ciencias_humanas` (humanidades, ética, filosofia, etc.)
- `tecnologia` (IA, ML, plataformas, ferramentas digitais)
- `pedagogia_aprendizagem` (formação docente, ensino, currículo)
- `covid_excluido` (excluído da análise principal)

Útil para detectar **shift temático** entre versões do corpus. Léxico pode ser adaptado para sua área.

### `compare_cooccurrence.py`

Identifica pares de tags que:

1. **JÁ co-ocorriam** no RIS anterior (estabilidade)
2. **NOVOS** que surgiram só no Zotero (clusters emergentes)
3. **Aumentaram** expressivamente (>= +50% de co-ocorrência)

Gera markdown que abre direto no Obsidian.

### `gen_candidatas.py`

Cruza o thesaurus VOSviewer atual (`vosviewer_thesaurus.csv`) com tags do Zotero. Lista candidatas que ainda não estão consolidadas — agrupa por tipo (MeSH genérico vs. termos relevantes) para você curar antes da próxima rodada de mapas.

## Adaptação para outras ferramentas gerenciadoras

Os scripts são feitos para **Zotero**. Para adaptar:

- **Mendeley**: usar o export BibTeX e parsear o `.bib`
- **EndNote**: exportar XML e parsear via `xml.etree`
- **Paperpile**: exportar BibTeX (idem Mendeley)

Pull requests com versões adaptadas são bem-vindas.

## Licença

CC BY-SA 4.0 (ver `../LICENSE`).
