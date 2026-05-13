"""Compara co-ocorrência tag-tag entre RIS VOSviewer e Zotero atual.

Identifica:
- Pares de tags que JÁ co-ocorriam no RIS (snapshot anterior)
- Pares NOVOS que surgiram no Zotero (refs adicionadas depois)
- Pares com aumento expressivo de co-ocorrência

EDITE a seção CONFIG abaixo antes de rodar.
"""
import re, unicodedata, sqlite3, csv
from pathlib import Path
from collections import Counter, defaultdict
from itertools import combinations

# ============================== CONFIG ==============================
RIS_PATH = Path(r'C:\Users\SEU_USUARIO\Documents\corpus_vosviewer.ris')
ZOTERO_DB = 'C:/Users/SEU_USUARIO/Zotero/zotero.sqlite'
OUT_MD = Path(r'C:\Users\SEU_USUARIO\Documents\meu-vault\50 - Analises\cooccurrence-ris-vs-zotero.md')
# ====================================================================


def normalize(s):
    if not s: return ''
    s = unicodedata.normalize('NFKD', s).encode('ASCII','ignore').decode('ASCII').lower()
    return re.sub(r'[^a-z0-9 ]+', ' ', s).strip()


# === RIS keywords por ref ===
content = RIS_PATH.read_text(encoding='utf-8', errors='replace')
records = re.split(r'\nER\s*-\s*\n?', content)

ris_kws_per_ref = []
for rec in records:
    kws = re.findall(r'^KW\s*-\s*(.+)$', rec, re.MULTILINE)
    kws_norm = sorted({normalize(k) for k in kws if k.strip()})
    if len(kws_norm) >= 2:
        ris_kws_per_ref.append(kws_norm)

print(f'RIS refs com 2+ keywords: {len(ris_kws_per_ref)}')

# === Zotero tags por ref ===
uri = f'file:{ZOTERO_DB}?mode=ro&immutable=1'
conn = sqlite3.connect(uri, uri=True)
cur = conn.cursor()
cur.execute("""SELECT i.itemID, t.name FROM items i
               JOIN itemTags it USING (itemID) JOIN tags t USING (tagID)
               JOIN itemTypes itp USING (itemTypeID)
               WHERE i.itemID NOT IN (SELECT itemID FROM deletedItems)
                 AND itp.typeName NOT IN ('attachment','note','annotation')""")
zot_per_ref = defaultdict(set)
for r in cur.fetchall():
    zot_per_ref[r[0]].add(normalize(r[1]))
zot_kws_per_ref = [sorted(tags) for tags in zot_per_ref.values() if len(tags) >= 2]
print(f'Zotero refs com 2+ tags: {len(zot_kws_per_ref)}')

# === Counts de tag (pra filtrar pares só de tags top) ===
ris_kw_total = Counter()
for kws in ris_kws_per_ref:
    ris_kw_total.update(kws)
zot_kw_total = Counter()
for kws in zot_kws_per_ref:
    zot_kw_total.update(kws)

# Pega tags com 20+ ocorrências em qualquer corpus
top_tags = {k for k, c in ris_kw_total.items() if c >= 20}
top_tags |= {k for k, c in zot_kw_total.items() if c >= 20}
print(f'Top tags (>=20 refs em algum corpus): {len(top_tags)}')

# === Co-occurrence ===
def cooccur(refs_kws, restrict):
    c = Counter()
    for kws in refs_kws:
        kws = [k for k in kws if k in restrict]
        if len(kws) < 2: continue
        for a, b in combinations(sorted(set(kws)), 2):
            c[(a, b)] += 1
    return c

ris_co = cooccur(ris_kws_per_ref, top_tags)
zot_co = cooccur(zot_kws_per_ref, top_tags)
print(f'Pares de co-ocorrencia (RIS): {len(ris_co)}')
print(f'Pares de co-ocorrencia (Zotero): {len(zot_co)}')

# Pares NOVOS (no Zotero mas não no RIS)
novos = [(p, c) for p, c in zot_co.items() if p not in ris_co]
novos.sort(key=lambda x: -x[1])

# Aumento expressivo (delta >= 3 e proporcionalmente >= 30%)
delta = []
for p, c_zot in zot_co.items():
    c_ris = ris_co.get(p, 0)
    if c_ris == 0: continue
    d = c_zot - c_ris
    if d >= 3 and (d / c_ris) >= 0.3:
        delta.append({'pair': p, 'ris': c_ris, 'zot': c_zot, 'delta': d, 'pct': d/c_ris})
delta.sort(key=lambda x: -x['delta'])

# === Output ===
out_lines = [
    '---',
    'type: analise-cooccurrence',
    'data: 2026-05-12',
    'comparacao: corpus_vosviewer.ris vs Zotero local',
    'tags: [analise, cooccurrence, bibliometria, vosviewer, zotero, mestrado]',
    '---',
    '',
    '# Análise de co-ocorrência — RIS VOSviewer × Zotero atual',
    '',
    f'> Compara co-ocorrência de tags entre o **corpus RIS antigo** ({len(ris_kws_per_ref)} refs com 2+ keywords) usado pelo último VOSviewer e o **Zotero atual** ({len(zot_kws_per_ref)} refs com 2+ tags). Restrito a tags com 20+ ocorrências em algum dos corpora.',
    '',
    '## Sumário',
    '',
    f'- Pares de co-ocorrência RIS: **{len(ris_co)}**',
    f'- Pares de co-ocorrência Zotero: **{len(zot_co)}** ({len(zot_co)-len(ris_co):+d})',
    f'- Pares NOVOS no Zotero (não existiam no RIS): **{len(novos)}**',
    f'- Pares com aumento expressivo (Δ ≥ 3 e ≥ +30%): **{len(delta)}**',
    '',
    '## 🆕 Top 20 pares NOVOS de co-ocorrência',
    '',
    '> Relações temáticas que **emergiram nas refs adicionadas depois do VOSviewer atual**. Esses são candidatos a aparecer em destaque no próximo mapa bibliométrico.',
    '',
    '| Tag A | Tag B | Refs (Zotero) |',
    '|---|---|---:|',
]
for (a, b), c in novos[:20]:
    out_lines.append(f'| `{a}` | `{b}` | {c} |')

out_lines += [
    '',
    '## 📈 Top 20 pares com AUMENTO expressivo',
    '',
    '> Co-ocorrências que **fortaleceram** desde o RIS. Provável: novas refs reforçam relação já existente — ou seja, **o cluster bibliométrico está crescendo**.',
    '',
    '| Tag A | Tag B | RIS | Zotero | Δ | %  |',
    '|---|---|---:|---:|---:|---:|',
]
for d in delta[:20]:
    a, b = d['pair']
    out_lines.append(f'| `{a}` | `{b}` | {d["ris"]} | {d["zot"]} | +{d["delta"]} | +{d["pct"]*100:.0f}% |')

# Top 20 ABSOLUTAS Zotero
all_zot = sorted(zot_co.items(), key=lambda x: -x[1])[:20]
out_lines += [
    '',
    '## 🔝 Top 20 co-ocorrências ABSOLUTAS no Zotero (independente do RIS)',
    '',
    '| Tag A | Tag B | Refs |',
    '|---|---|---:|',
]
for (a, b), c in all_zot:
    is_new = (a, b) not in ris_co
    badge = ' 🆕' if is_new else ''
    out_lines.append(f'| `{a}` | `{b}`{badge} | {c} |')

out_lines += [
    '',
    '## Interpretação',
    '',
    'Os pares **novos** revelam onde o corpus cresceu tematicamente. Os pares com **aumento** mostram onde clusters existentes consolidaram.',
    '',
    '### O que fazer com isso',
    '',
    '1. Olhar os pares **novos** — pode haver eixo temático que merece capítulo ou subseção na dissertação que não estava previsto',
    '2. Pares com aumento >= +50% sugerem **temas que merecem atenção privilegiada** na revisão de literatura',
    '3. Próximo mapa VOSviewer (após re-export RIS com 1.893 refs) vai refletir exatamente esses pares novos',
    '',
    '## Próximos passos',
    '',
    '- [ ] Re-exportar RIS do Zotero (1.893 refs)',
    '- [ ] Aplicar `vosviewer_thesaurus.csv` (existente) + adições de [[candidatas-thesaurus-2026-05-12]]',
    '- [ ] Gerar mapas VOSviewer (network, density, overlay) atualizados',
    '- [ ] Comparar visualmente novos clusters vs. atuais',
]

OUT_MD.parent.mkdir(parents=True, exist_ok=True)
OUT_MD.write_text('\n'.join(out_lines), encoding='utf-8')
print(f'\nOK -> {OUT_MD}')

# Print preview
print('\n=== TOP 10 PARES NOVOS ===')
for (a, b), c in novos[:10]:
    print(f'  [{c:3d}] {a:35s} <-> {b}')

print('\n=== TOP 10 PARES COM AUMENTO ===')
for d in delta[:10]:
    a, b = d['pair']
    print(f'  +{d["delta"]:3d} ({d["pct"]*100:3.0f}%)  {a:30s} <-> {b}  ({d["ris"]} -> {d["zot"]})')
