"""Gera lista de tags candidatas a entrar no thesaurus VOSviewer.

Cruza as tags do Zotero atual com o thesaurus VOSviewer existente (CSV) e
gera um markdown com tags que ainda NÃO estão no thesaurus e poderiam entrar.

EDITE a seção CONFIG abaixo antes de rodar.
"""
import re, unicodedata, sqlite3, csv
from pathlib import Path
from collections import Counter

# ============================== CONFIG ==============================
THES_PATH = Path(r'C:\Users\SEU_USUARIO\Documents\vosviewer_thesaurus.csv')
ZOTERO_DB = 'C:/Users/SEU_USUARIO/Zotero/zotero.sqlite'
OUT_MD = Path(r'C:\Users\SEU_USUARIO\Documents\meu-vault\_meta\candidatas-thesaurus.md')
# ====================================================================


def normalize(s):
    if not s: return ''
    s = unicodedata.normalize('NFKD', s).encode('ASCII','ignore').decode('ASCII').lower()
    return re.sub(r'[^a-z0-9 ]+', ' ', s).strip()


thes_path = THES_PATH
thes_labels = set()
thes_replacements = set()
with thes_path.open(encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) >= 2:
            thes_labels.add(normalize(row[0]))
            thes_replacements.add(normalize(row[1]))

uri = f'file:{ZOTERO_DB}?mode=ro&immutable=1'
conn = sqlite3.connect(uri, uri=True)
cur = conn.cursor()
cur.execute("""SELECT t.name, COUNT(DISTINCT it.itemID) FROM tags t
               JOIN itemTags it USING (tagID) JOIN items i USING (itemID)
               JOIN itemTypes itp USING (itemTypeID)
               WHERE i.itemID NOT IN (SELECT itemID FROM deletedItems)
                 AND itp.typeName NOT IN ('attachment','note','annotation')
               GROUP BY t.name ORDER BY 2 DESC""")
zot = [(r[0], r[1]) for r in cur.fetchall()]

GENERIC_STOP = {
    'humans','human','procedures','article','female','male','adult','child','aged',
    'middle aged','young adult','adolescent','controlled study','clinical article',
    'human experiment','priority journal','review','validation study','prospective study'
}


def categorize(name):
    n = name.lower()
    n_norm = normalize(name)
    if n_norm in GENERIC_STOP: return 'ignorar-mesh-generico'
    if any(x in n for x in ['covid','coronavirus','pandemic','sars-cov']): return 'covid'
    if any(x in n for x in ['e-learning','online','distance','remote','google classroom','edmodo','moodle','platform','digital','technology','ict','ai','artificial']): return 'tecnologia-digital'
    if any(x in n for x in ['learning','teaching','education','pedagog','curriculum','classroom','student','teacher','faculty','training']): return 'pedagogia-aprendizagem'
    if any(x in n for x in ['health','medical','clinic','hospital','patient','disease','pathology','nurs','therap','anatomy','psychology']): return 'saude-medicina'
    if any(x in n for x in ['questionnaire','survey','methodology','qualitative','quantitative','review','meta-analysis']): return 'metodologia-pesquisa'
    if any(x in n for x in ['brazil','portugal','spain','africa','asia','europe','university','school']): return 'instituicao-pais'
    if re.match(r'^[A-Z][a-z]+\s[A-Z]', name) and len(name) < 30: return 'autor-pessoa'
    return 'outras-relevantes'


candidatas = []
ja_consolidadas = []
for name, count in zot:
    n_norm = normalize(name)
    if n_norm in thes_labels or n_norm in thes_replacements:
        ja_consolidadas.append((name, count))
        continue
    if count < 5: continue
    if name.startswith(('teoria_','gap_','fonte_','base_')): continue
    cat = categorize(name)
    candidatas.append({'name': name, 'count': count, 'cat': cat})


def sugerir(name, cat):
    n = name.lower()
    if 'covid' in n or 'coronavirus' in n: return '`covid-19`'
    if 'e-learning' in n or 'distance' in n or 'online learning' in n or 'remote' in n: return '`educacao a distancia`'
    if 'google classroom' in n: return '`google classroom`'
    if 'questionnaire' in n or 'survey' in n: return '`questionario`'
    if 'higher education' in n: return '`ensino superior`'
    if n in ('ict','icts'): return '`tecnologias digitais de informacao e comunicacao`'
    if 'teacher' in n or 'faculty' in n or 'training' in n: return '`formacao docente`'
    if cat == 'ignorar-mesh-generico': return '_ignorar_'
    return ''


from datetime import date as _date

_hoje = _date.today().isoformat()
lines = [
    '---',
    'type: candidatas-thesaurus',
    f'data: {_hoje}',
    'origem: Zotero tags vs vosviewer_thesaurus.csv',
    'tags: [thesaurus, candidatas, taxonomia, zotero, vosviewer]',
    '---',
    '',
    '# Candidatas a entrar no thesaurus VOSviewer',
    '',
    f'> Análise {_hoje}: {len(zot)} tags únicas no Zotero, {len(ja_consolidadas)} já consolidadas pelo thesaurus existente. **{len(candidatas)} candidatas** com 5+ ocorrências e fora da taxonomia manual (`gap_*`, `teoria_*`, `fonte_*`, `base_*`).',
    '',
    '## Como usar',
    '',
    '1. Revise cada categoria abaixo',
    '2. Decida: mapeia para canônico (entra no thesaurus) ou ignora',
    '3. Adicione ao `vosviewer_thesaurus.csv` antes do próximo build VOSviewer',
    '',
]

ordem = ['covid','tecnologia-digital','pedagogia-aprendizagem','saude-medicina',
         'metodologia-pesquisa','instituicao-pais','autor-pessoa','outras-relevantes',
         'ignorar-mesh-generico']

for cat in ordem:
    grupo = sorted([c for c in candidatas if c['cat']==cat], key=lambda x: -x['count'])
    if not grupo: continue
    lines.append(f'### {cat}')
    lines.append('')
    if cat == 'ignorar-mesh-generico':
        lines.append('_Auto-tags MeSH/genéricas — sugestão: **ignorar no thesaurus**._')
        lines.append('')
    lines.append('| Tag (variante) | Refs | Canônico sugerido |')
    lines.append('|---|---:|---|')
    for c in grupo[:25]:
        lines.append(f'| `{c["name"]}` | {c["count"]} | {sugerir(c["name"], c["cat"])} |')
    if len(grupo) > 25:
        lines.append(f'| _... +{len(grupo)-25} outras_ | | |')
    lines.append('')

lines += [
    '## Estatísticas',
    '',
    f'- Total Zotero tags únicas: {len(zot)}',
    f'- Já consolidadas no thesaurus: {len(ja_consolidadas)}',
    f'- Candidatas relevantes (count >= 5): {len(candidatas)}',
    f'- Ruído MeSH genérico (a ignorar): {sum(1 for c in candidatas if c["cat"]=="ignorar-mesh-generico")}',
    f'- Úteis a consolidar: {sum(1 for c in candidatas if c["cat"]!="ignorar-mesh-generico")}',
]

out = OUT_MD
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text('\n'.join(lines), encoding='utf-8')
print(f'OK -> {out}')
print(f'Total Zotero: {len(zot)}')
print(f'Consolidadas: {len(ja_consolidadas)}')
print(f'Candidatas: {len(candidatas)}')
print(f'Por categoria:')
from collections import Counter as C
counts = C(c['cat'] for c in candidatas)
for cat in ordem:
    if cat in counts:
        print(f'  {cat:30s} {counts[cat]}')
