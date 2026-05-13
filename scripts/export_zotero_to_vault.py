"""Export Zotero local SQLite -> 1 .md per reference inside Obsidian vault.

Idempotente: preserva corpo manual de notas existentes (não sobrescreve arquivos).

== EDITE A SEÇÃO `CONFIG` ABAIXO antes de rodar ==

Lê o `zotero.sqlite` em modo read-only via URI (`?mode=ro&immutable=1`), portanto
pode rodar com o Zotero aberto sem risco de corromper o banco.

Uso:
    python export_zotero_to_vault.py
"""
from __future__ import annotations
import sqlite3
import re
import unicodedata
from pathlib import Path
from collections import defaultdict
import sys

# ============================== CONFIG ==============================
# 1) Caminho do zotero.sqlite (Windows padrão: ~/Zotero/zotero.sqlite)
ZOTERO_DB = "C:/Users/SEU_USUARIO/Zotero/zotero.sqlite"

# 2) Pasta DESTINO dentro do seu vault Obsidian (onde as notas serão criadas)
VAULT_REFS = Path(r"C:\Users\SEU_USUARIO\Documents\meu-vault\20 - Referencias")

# 3) Mapeamento collection do Zotero -> subpasta destino dentro de VAULT_REFS.
#    Exemplo abaixo segue o padrão "P1_Tema, P2_Tema..." comum em mestrado.
#    Refs em collections NÃO listadas caem em "_sem-collection".
COLLECTIONS_FOLDERS = {
    "P1_Tema": "P1_Tema",
    "P2_Tema": "P2_Tema",
    "P3_Tema": "P3_Tema",
    "P4_Teorico": "P4_Teorico",
    "zotero_import_busca_dirigida": "_imports/busca-dirigida",
    "zotero_import_bases_indexadas": "_imports/bases-indexadas",
}
# ====================================================================

SAFE = re.compile(r"[^a-z0-9\-]+")

def slugify(s: str, max_len: int = 70) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ASCII", "ignore").decode("ASCII")
    s = s.lower()
    s = SAFE.sub("-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:max_len]

def yaml_escape(s: str | None) -> str:
    if s is None:
        return '""'
    s = str(s).replace('"', '\\"').replace("\n", " ").strip()
    return f'"{s}"'

def yaml_list(items: list[str]) -> str:
    if not items:
        return "[]"
    cleaned = [it.replace('"', '\\"').replace("\n", " ").strip() for it in items if it]
    return "[" + ", ".join(f'"{it}"' for it in cleaned) + "]"

def fetch_zotero():
    uri = f"file:{ZOTERO_DB}?mode=ro&immutable=1"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Fetch items + type
    cur.execute("""
        SELECT i.itemID, i.libraryID, i.key, it.typeName
        FROM items i
        JOIN itemTypes it USING (itemTypeID)
        WHERE i.itemID NOT IN (SELECT itemID FROM deletedItems)
          AND it.typeName NOT IN ('attachment', 'note', 'annotation')
        ORDER BY i.itemID
    """)
    items = {r["itemID"]: dict(r) for r in cur.fetchall()}

    # Field data
    cur.execute("""
        SELECT id.itemID, f.fieldName, idv.value
        FROM itemData id
        JOIN fieldsCombined f USING (fieldID)
        JOIN itemDataValues idv USING (valueID)
    """)
    item_fields = defaultdict(dict)
    for r in cur.fetchall():
        if r["itemID"] in items:
            item_fields[r["itemID"]][r["fieldName"]] = r["value"]

    # Creators
    cur.execute("""
        SELECT ic.itemID, c.firstName, c.lastName, ct.creatorType, ic.orderIndex
        FROM itemCreators ic
        JOIN creators c USING (creatorID)
        JOIN creatorTypes ct USING (creatorTypeID)
        ORDER BY ic.itemID, ic.orderIndex
    """)
    item_creators = defaultdict(list)
    for r in cur.fetchall():
        if r["itemID"] in items:
            full = f"{r['firstName'] or ''} {r['lastName'] or ''}".strip()
            item_creators[r["itemID"]].append({
                "name": full,
                "lastName": r["lastName"] or "",
                "type": r["creatorType"],
                "order": r["orderIndex"],
            })

    # Tags
    cur.execute("""
        SELECT it.itemID, t.name
        FROM itemTags it
        JOIN tags t USING (tagID)
    """)
    item_tags = defaultdict(list)
    for r in cur.fetchall():
        if r["itemID"] in items:
            item_tags[r["itemID"]].append(r["name"])

    # Collections
    cur.execute("""
        SELECT ci.itemID, c.collectionName
        FROM collectionItems ci
        JOIN collections c USING (collectionID)
    """)
    item_collections = defaultdict(list)
    for r in cur.fetchall():
        if r["itemID"] in items:
            item_collections[r["itemID"]].append(r["collectionName"])

    conn.close()
    return items, item_fields, item_creators, item_tags, item_collections


def extract_year(date_str: str | None) -> str:
    if not date_str:
        return ""
    m = re.search(r"(19|20)\d{2}", date_str)
    return m.group(0) if m else ""


def build_citekey(creators: list[dict], year: str, title: str) -> str:
    # FirstAuthor-Year-FirstSignificantWord (lower, slugified)
    if creators:
        first_last = creators[0]["lastName"] or creators[0]["name"].split()[-1]
    else:
        first_last = "anon"
    first_last = slugify(first_last, max_len=20)
    year_s = year or "sd"
    # First non-stopword from title
    stops = {"the","a","an","of","in","on","and","or","de","da","do","das","dos","la","el","los"}
    title_words = [w for w in re.findall(r"[a-zA-Z0-9]+", title or "") if w.lower() not in stops]
    word = slugify(title_words[0], max_len=25) if title_words else "untitled"
    return f"{first_last}-{year_s}-{word}"


def build_note(item, fields, creators, tags, collections) -> tuple[str, str, str]:
    """Returns (folder, filename, content)."""
    title = fields.get("title", "Sem título")
    date = fields.get("date") or fields.get("year")
    year = extract_year(date)
    publication = fields.get("publicationTitle") or fields.get("bookTitle") or fields.get("conferenceName") or fields.get("publisher", "")
    doi = fields.get("DOI", "")
    url = fields.get("url", "")
    abstract = fields.get("abstractNote", "")
    item_type = item.get("typeName", "")

    citekey = build_citekey(creators, year, title)
    filename = f"@{citekey}.md"

    # Folder by first collection match
    folder_name = "_sem-collection"
    for col in collections:
        if col in COLLECTIONS_FOLDERS:
            folder_name = COLLECTIONS_FOLDERS[col]
            break

    authors_list = [c["name"] for c in creators if c["type"] == "author"]
    if not authors_list:
        authors_list = [c["name"] for c in creators][:3]

    # Frontmatter
    fm = [
        "---",
        "type: reference",
        f"zotero_id: {item['itemID']}",
        f"zotero_key: {item['key']}",
        f"citekey: {citekey}",
        f"title: {yaml_escape(title)}",
        f"authors: {yaml_list(authors_list)}",
        f"year: {year_or_empty_yaml(year)}",
        f"item_type: {yaml_escape(item_type)}",
        f"publication: {yaml_escape(publication)}",
        f"doi: {yaml_escape(doi)}",
        f"url: {yaml_escape(url)}",
        f"collection: {yaml_escape(collections[0] if collections else '')}",
        f"collections: {yaml_list(collections)}",
        f"tags: {yaml_list(tags)}",
        "status: a-ler",
        "prioridade: media",
        "---",
        "",
    ]

    # Body
    body = [f"# {title}", ""]
    if authors_list:
        body.append(f"> **{', '.join(authors_list)}**" + (f" ({year})" if year else ""))
        if publication:
            body[-1] += f" · *{publication}*"
        body.append("")
    if doi:
        body.append(f"**DOI:** [{doi}](https://doi.org/{doi})  ")
    if url and url != doi:
        body.append(f"**URL:** {url}  ")
    if doi or url:
        body.append("")
    if abstract:
        body += ["## Abstract", "", abstract, ""]

    body += [
        "## Pontos-chave",
        "",
        "- ",
        "",
        "## Como uso na dissertação",
        "",
        "- **Capítulo:** ",
        "- **Argumento:** ",
        "- **Posição:** corrobora / contesta / complementa",
        "",
        "## Conexões",
        "",
        "- Relacionado a: [[]]",
        "",
        "## Notas pessoais",
        "",
        "<!-- anotações livres -->",
    ]

    return folder_name, filename, "\n".join(fm + body)


def year_or_empty_yaml(year: str) -> str:
    return year if year else '""'


def main():
    print("Lendo Zotero SQLite (read-only)...")
    items, item_fields, item_creators, item_tags, item_collections = fetch_zotero()
    print(f"Total items: {len(items)}")

    counts = defaultdict(int)
    written = 0
    skipped_existing = 0
    errors = 0
    seen_filenames = defaultdict(int)

    for item_id, item in items.items():
        try:
            folder_name, filename, content = build_note(
                item,
                item_fields.get(item_id, {}),
                item_creators.get(item_id, []),
                item_tags.get(item_id, []),
                item_collections.get(item_id, []),
            )
            target_dir = VAULT_REFS / folder_name
            target_dir.mkdir(parents=True, exist_ok=True)

            # Handle filename collision
            base_key = f"{folder_name}/{filename}"
            seen_filenames[base_key] += 1
            if seen_filenames[base_key] > 1:
                name_part = filename[:-3]  # strip .md
                filename = f"{name_part}-{seen_filenames[base_key]}.md"

            target = target_dir / filename
            if target.exists():
                skipped_existing += 1
                continue

            target.write_text(content, encoding="utf-8")
            counts[folder_name] += 1
            written += 1
        except Exception as e:
            errors += 1
            print(f"ERROR item {item_id}: {e}", file=sys.stderr)

    print()
    print(f"OK — escreveu {written} notas, pulou {skipped_existing} existentes, {errors} erros.")
    print()
    print("Por folder:")
    for folder, n in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {folder:40s} {n}")


if __name__ == "__main__":
    main()
