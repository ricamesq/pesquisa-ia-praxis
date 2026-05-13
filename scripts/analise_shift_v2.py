"""Versão 2: análise do shift com eixo CIÊNCIAS HUMANAS corretamente definido.

Léxico revisado a partir da releitura visual do overlay (12/05/2026):
- Termos AMARELOS (2024) → Ciências Humanas / Reflexão Crítica
- Termos AZUIS (2021-2022) → Tecnologia Educacional Aplicada
- Eixo Pedagogia mantido (alguns termos ficam fronteira)
- COVID continua excluído
"""
import re, unicodedata, sqlite3, json
from pathlib import Path
from collections import Counter, defaultdict
from itertools import combinations


def normalize(s):
    if not s: return ''
    s = unicodedata.normalize('NFKD', s).encode('ASCII','ignore').decode('ASCII').lower()
    return re.sub(r'[^a-z0-9 ]+', ' ', s).strip()


# Léxico revisado em 12/05/2026 baseado no overlay VOSviewer real
LEX = {
    # Antes era "bem_estar" — agora explicitamente Ciências Humanas + Reflexão Crítica
    # Inclui termos que aparecem em AMARELO (2024) no overlay
    'ciencias_humanas': [
        'humanities','humanidades','philosophy','filosofia','art','arte','sociology','sociologia',
        'political science','ciencia politica','politica','politics','qualitative research',
        'pesquisa qualitativa','epistemology','epistemologia','context archaeology','contexto',
        'data collection','coleta de dados','citizenship','cidadania','ethics','etica',
        'social psychology','psicologia social','sociocultural','aesthetics','estetica',
        'humanism','humanismo','humanization','humanizacao','citizen journalism',
        'creativity','criatividade','dialogic','dialogo','dialogue','ideology','ideologia',
        'critical thinking','pensamento critico','public relations','relacoes publicas',
        'media','midia','sustainable development','desenvolvimento sustentavel','sustainability',
        'inclusion','inclusao','autonomy','autonomia','critical literacy','letramento critico',
        'medicine','medicina','health care','saude','wellbeing','well-being','well being',
        'bem-estar','bem estar','mental health','saude mental'
    ],
    # Tecnologia (mantida — refs azuis 2021-2022 e verdes 2023 do mapa)
    'tecnologia': [
        'artificial intelligence','intelligence artificial','inteligencia artificial','ia','ai',
        'machine learning','aprendizado de maquina','deep learning','algorithm','algoritmo',
        'automation','automacao','computer science','computing','computacao','software',
        'platform','plataforma','digital','technology','technologies','tecnologia','tecnologias',
        'ict','icts','tdic','tdics','data','big data','blockchain','iot','virtual','virtual reality',
        'realidade virtual','generative ai','llm','chatbot','natural language','natural language processing',
        'social media','networks','internet','online','digital tools','engineering','engenharia',
        'programming','programacao','innovation','inovacao','generative grammar','process computing',
        'human-computer interaction','interface','data science','ciencia de dados','engineering management',
        'engineering ethics','etica em engenharia','learning analytics','technology integration',
        'integracao tecnologica','educational technology','tecnologia educacional','metacognition',
        'metacognicao','task project management','knowledge management','gestao do conhecimento',
        'structural equation modeling','modelagem de equacoes','library science','biblioteconomia',
        'information literacy','letramento informacional','digital literacy','letramento digital'
    ],
    # Pedagogia / Aprendizagem (refs do meio — verde e cinza-pedagógico)
    'pedagogia_aprendizagem': [
        'learning','aprendizagem','teaching','ensino','pedagogy','pedagogia','meaningful learning',
        'aprendizagem significativa','curriculum','curriculo','classroom','sala de aula',
        'student','aluno','teacher','professor','docente','faculty','education','educacao',
        'training','formacao','teacher education','teacher training','formacao docente',
        'continuing education','educacao continuada','competence human resources','competencia',
        'digital competence','competencia digital','digcompedu','higher education','ensino superior',
        'educacao superior','pedagogical','psychology','psicologia','psychological','cognition',
        'cognicao','autoregulated','self-regulation','autorregulacao','active learning',
        'scaffold','scaffolds','andaime','foreign language','lingua estrangeira','mathematics education',
        'medical education','educacao medica','distance education','educacao a distancia',
        'online learning','e-learning','google classroom','edmodo','moodle','psychological intervention'
    ],
    # COVID — excluído da análise principal (metodologicamente)
    'covid_excluido': [
        'covid','coronavirus','pandemic','pandemia','sars-cov','sars cov','quarantine','quarentena',
        'lockdown','isolamento','remote teaching','ensino remoto','emergency remote',
        'covid 19','covid-19','virology','virologia'
    ],
}


def classify_tag(name):
    n_norm = normalize(name)
    matched = []
    for axis, terms in LEX.items():
        for t in terms:
            if t in n_norm or n_norm in t:
                if abs(len(t) - len(n_norm)) <= max(20, len(t)):
                    matched.append(axis)
                    break
    if not matched: return 'outros'
    # Prioridade: covid > ciencias_humanas > pedagogia > tecnologia
    if 'covid_excluido' in matched: return 'covid_excluido'
    if 'ciencias_humanas' in matched: return 'ciencias_humanas'
    if 'pedagogia_aprendizagem' in matched: return 'pedagogia_aprendizagem'
    if 'tecnologia' in matched: return 'tecnologia'
    return matched[0]


# ============================== CONFIG ==============================
# EDITE estes 2 caminhos antes de rodar:
RIS_PATH = Path(r'C:\Users\SEU_USUARIO\Documents\corpus_vosviewer.ris')
ZOTERO_DB = 'C:/Users/SEU_USUARIO/Zotero/zotero.sqlite'
# ====================================================================

# === RIS ===
content = RIS_PATH.read_text(encoding='utf-8', errors='replace')
records = re.split(r'\nER\s*-\s*\n?', content)
ris_refs = []
for rec in records:
    kws = re.findall(r'^KW\s*-\s*(.+)$', rec, re.MULTILINE)
    kws = [k.strip() for k in kws if k.strip()]
    if kws: ris_refs.append({'kws': kws})

# === Zotero ===
uri = f'file:{ZOTERO_DB}?mode=ro&immutable=1'
conn = sqlite3.connect(uri, uri=True)
cur = conn.cursor()
cur.execute("""SELECT i.itemID, t.name FROM items i
               JOIN itemTags it USING (itemID) JOIN tags t USING (tagID)
               JOIN itemTypes itp USING (itemTypeID)
               WHERE i.itemID NOT IN (SELECT itemID FROM deletedItems)
                 AND itp.typeName NOT IN ('attachment','note','annotation')""")
zot_per_ref = defaultdict(list)
for r in cur.fetchall():
    zot_per_ref[r[0]].append(r[1])
zot_refs = [{'kws': list(v)} for v in zot_per_ref.values()]


def axis_stats(refs):
    n = len(refs)
    refs_per_axis = defaultdict(int)
    tag_freq = Counter()
    for r in refs:
        axes_in_ref = set()
        for k in r['kws']:
            ax = classify_tag(k)
            if ax not in ('outros',):
                tag_freq[ax] += 1
                axes_in_ref.add(ax)
        for ax in axes_in_ref:
            refs_per_axis[ax] += 1
    return refs_per_axis, tag_freq, n


ris_refs_per_axis, ris_tag_freq, n_ris = axis_stats(ris_refs)
zot_refs_per_axis, zot_tag_freq, n_zot = axis_stats(zot_refs)

# Co-occurrence axes
def cooccur_axes(refs):
    co = Counter()
    for r in refs:
        axes = set()
        for k in r['kws']:
            ax = classify_tag(k)
            if ax not in ('outros','covid_excluido'): axes.add(ax)
        for a, b in combinations(sorted(axes), 2):
            co[(a, b)] += 1
    return co

ris_co = cooccur_axes(ris_refs)
zot_co = cooccur_axes(zot_refs)

print(f'RIS refs: {n_ris} | Zot refs: {n_zot}\n')
print('=== Refs com tag do eixo ===')
print(f'{"Eixo":30s} {"RIS":>8s} {"%":>6s} {"Zot":>8s} {"%":>6s} {"Δ pp":>8s}')
for ax in ('tecnologia','ciencias_humanas','pedagogia_aprendizagem','covid_excluido'):
    r = ris_refs_per_axis.get(ax, 0); z = zot_refs_per_axis.get(ax, 0)
    pr = r*100/n_ris; pz = z*100/n_zot
    print(f'{ax:30s} {r:>8d} {pr:>5.1f}% {z:>8d} {pz:>5.1f}% {pz-pr:>+7.1f}')

print('\n=== Densidade de tags por eixo ===')
tot_ris = sum(ris_tag_freq.values()) or 1
tot_zot = sum(zot_tag_freq.values()) or 1
print(f'{"Eixo":30s} {"RIS":>8s} {"%":>6s} {"Zot":>8s} {"%":>6s} {"Δ pp":>8s}')
for ax in ('tecnologia','ciencias_humanas','pedagogia_aprendizagem','covid_excluido'):
    r = ris_tag_freq.get(ax, 0); z = zot_tag_freq.get(ax, 0)
    pr = r*100/tot_ris; pz = z*100/tot_zot
    print(f'{ax:30s} {r:>8d} {pr:>5.1f}% {z:>8d} {pz:>5.1f}% {pz-pr:>+7.1f}')

print('\n=== Co-ocorrência entre eixos (excl. COVID) ===')
all_pairs = set(ris_co) | set(zot_co)
rows = sorted(all_pairs, key=lambda p: -(zot_co.get(p,0)))
print(f'{"Par":50s} {"RIS":>8s} {"Zot":>8s} {"Δ":>8s}')
for p in rows:
    rv = ris_co.get(p, 0); zv = zot_co.get(p, 0)
    print(f'{p[0]+" + "+p[1]:50s} {rv:>8d} {zv:>8d} {zv-rv:>+8d}')

# Save data for markdown
out_data = {
    'n_ris': n_ris, 'n_zot': n_zot,
    'ris_refs_per_axis': dict(ris_refs_per_axis),
    'zot_refs_per_axis': dict(zot_refs_per_axis),
    'ris_tag_freq': dict(ris_tag_freq),
    'zot_tag_freq': dict(zot_tag_freq),
    'ris_co': {f'{a}|{b}': c for (a, b), c in ris_co.items()},
    'zot_co': {f'{a}|{b}': c for (a, b), c in zot_co.items()},
}
Path('/tmp/shift_v2.json').write_text(json.dumps(out_data, indent=2, ensure_ascii=False), encoding='utf-8')
print('\nDados salvos em /tmp/shift_v2.json')
