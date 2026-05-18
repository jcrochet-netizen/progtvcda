#!/usr/bin/env python3
"""Build the WordPress-embeddable football TV widget from merged sources."""
import html as html_lib

# Channel filter slugs (used for CSS filtering)
# Each match row gets classes for the filters it matches.
FILTERS = [
    ('all', 'Tutte'),
    ('dazn', 'DAZN'),
    ('sky', 'Sky Sport'),
    ('sky-calcio', 'Sky Sport Calcio'),
    ('now', 'NOW'),
    ('como', 'Como TV'),
    ('apple', 'Apple TV'),
    ('sportitalia', 'Sportitalia'),
    ('rai', 'Rai'),
    ('tv8', 'TV8'),
    ('lab', 'LAB Channel'),
    ('disney', 'Disney+'),
    ('solocalcio', 'Solocalcio'),
]

# Per-channel badge styles + filter mapping
# (display_name, badge_class, filter_slug)
CHANNEL_MAP = {
    'DAZN':              ('DAZN',            'b-dazn',        'dazn'),
    'Sky Sport':         ('Sky Sport',       'b-sky',         'sky'),
    'Sky Sport Uno':     ('Sky Sport Uno',   'b-sky',         'sky'),
    'Sky Sport 1':       ('Sky Sport Uno',   'b-sky',         'sky'),
    'Sky Sport 4K':      ('Sky Sport 4K',    'b-sky',         'sky'),
    'Sky':               ('Sky Sport',       'b-sky',         'sky'),
    'Sky Sport Calcio':  ('Sky Sport Calcio','b-sky-calcio',  'sky-calcio'),
    'NOW':               ('NOW',             'b-now',         'now'),
    'Como TV':           ('Como TV',         'b-como',        'como'),
    'Apple TV':          ('Apple TV',        'b-apple',       'apple'),
    'Sportitalia':       ('Sportitalia',     'b-sportitalia', 'sportitalia'),
    'Rai 2':             ('Rai 2',           'b-rai',         'rai'),
    'Rai Sport':         ('Rai Sport',       'b-rai',         'rai'),
    'TV8':               ('TV8',             'b-tv8',         'tv8'),
    'LAB Channel':       ('LAB Channel',     'b-lab',         'lab'),
    'Disney+':           ('Disney+',         'b-disney',      'disney'),
    'Solocalcio':        ('Solocalcio',      'b-solocalcio',  'solocalcio'),
    'OneFootball':       ('OneFootball',     'b-onefootball', None),
    'Vivo Azzurro TV':   ('Vivo Azzurro',    'b-vivo',        None),
}

# Days (index, label_short, label_date)
DAYS = [
    (1, 'Lun', '18 Mag'),
    (2, 'Mar', '19 Mag'),
    (3, 'Mer', '20 Mag'),
    (4, 'Gio', '21 Mag'),
    (5, 'Ven', '22 Mag'),
    (6, 'Sab', '23 Mag'),
    (7, 'Dom', '24 Mag'),
]

# Merged matches: (day_idx, time, match, competition, [channels])
MATCHES = [
    # Day 1 - 18 Mag (Lun)
    (1, '00:00', 'Inter Miami - Portland Timbers', 'MLS', ['Apple TV']),
    (1, '02:00', 'Nashville - Los Angeles FC', 'MLS', ['Apple TV']),
    (1, '21:00', 'Arsenal - Burnley', 'Premier League', ['Sky Sport Calcio', 'Sky Sport Uno', 'Sky Sport 4K', 'NOW']),

    # Day 2 - 19 Mag (Mar)
    (2, '17:00', 'Italia - Serbia U15', 'Amichevole', ['Vivo Azzurro TV']),
    (2, '20:00', 'Monza - Juve Stabia', 'Serie B', ['DAZN', 'LAB Channel']),
    (2, '20:30', 'Bournemouth - Manchester City', 'Premier League', ['Sky Sport Uno', 'Sky Sport 4K', 'NOW']),
    (2, '21:15', 'Chelsea - Tottenham', 'Premier League', ['Sky Sport Calcio', 'NOW']),

    # Day 3 - 20 Mag (Mer)
    (3, '00:00', 'Coquimbo - Tolima', 'Copa Libertadores', ['Como TV']),
    (3, '00:00', 'Fluminense - Bolivar', 'Copa Libertadores', ['Como TV']),
    (3, '00:00', 'Rosario Central - Universidad Central', 'Copa Libertadores', ['Como TV']),
    (3, '00:00', 'Audax Italiano - Barracas Central', 'Copa Sudamericana', ['Como TV']),
    (3, '00:00', 'Montevideo City Torque - Deportivo Riestra', 'Copa Sudamericana', ['Como TV']),
    (3, '02:00', 'Always Ready - Mirassol', 'Copa Libertadores', ['Como TV']),
    (3, '02:00', 'Santa Fe - Platense', 'Copa Libertadores', ['Como TV']),
    (3, '02:30', 'Boca Juniors - Cruzeiro', 'Copa Libertadores', ['Como TV']),
    (3, '02:30', 'San Paolo - Millonarios', 'Copa Sudamericana', ['Como TV']),
    (3, '04:00', 'Independiente del Valle - Libertad', 'Copa Libertadores', ['Como TV']),
    (3, '04:00', 'America Cali - Tigre', 'Copa Sudamericana', ['Como TV']),
    (3, '04:00', 'Deportivo Cuenca - Recoleta', 'Copa Sudamericana', ['Como TV']),
    (3, '20:00', 'Palermo - Catanzaro', 'Playoff Serie B', ['DAZN', 'LAB Channel']),
    (3, '20:00', 'Union Brescia - Casarano', 'Playoff Serie C', ['Sky Sport', 'NOW']),
    (3, '20:00', 'Ascoli - Potenza', 'Playoff Serie C', ['Sky Sport', 'NOW']),
    (3, '20:00', 'Al Khaleej - Al Ahli', 'Saudi League', ['Sportitalia', 'Como TV']),
    (3, '20:30', 'Catania - Lecco', 'Playoff Serie C', ['Sky Sport', 'NOW']),
    (3, '20:45', 'Ravenna - Salernitana', 'Playoff Serie C', ['Rai Sport', 'Sky Sport', 'NOW']),
    (3, '21:00', 'Friburgo - Aston Villa', 'UEFA Europa League Final', ['Sky Sport', 'Sky Sport Uno', 'Sky Sport 4K', 'NOW']),

    # Day 4 - 21 Mag (Gio)
    (4, '00:00', 'Nacional - Universitario', 'Copa Libertadores', ['Como TV']),
    (4, '00:00', 'Boston River - O\'Higgins', 'Copa Sudamericana', ['Como TV']),
    (4, '00:00', 'Olimpia - Vasco da Gama', 'Copa Sudamericana', ['Como TV']),
    (4, '00:00', 'Santos - San Lorenzo', 'Copa Sudamericana', ['Como TV']),
    (4, '02:00', 'Gremio - Palestino', 'Copa Sudamericana', ['Como TV']),
    (4, '02:00', 'Independiente Petrolero - Botafogo', 'Copa Sudamericana', ['Como TV']),
    (4, '02:30', 'Flamengo - Estudiantes', 'Copa Libertadores', ['Como TV']),
    (4, '02:30', 'LDU Quito - Lanus', 'Copa Libertadores', ['Como TV']),
    (4, '02:30', 'Palmeiras - Cerro Porteño', 'Copa Libertadores', ['Como TV']),
    (4, '02:30', 'River Plate - Bragantino', 'Copa Sudamericana', ['Como TV']),
    (4, '04:00', 'Cusco - Independiente Medellin', 'Copa Libertadores', ['Como TV']),
    (4, '04:00', 'Junior - Sporting Cristal', 'Copa Libertadores', ['Como TV']),
    (4, '15:00', 'Roma - Bologna', 'Playoff Primavera', ['Sportitalia']),
    (4, '18:00', 'Primavera 1', 'Primavera 1', ['Sportitalia']),
    (4, '20:00', 'Al Nassr - Damac', 'Saudi League', ['Sportitalia', 'Como TV']),
    (4, '20:00', 'Al Fayha - Al Hilal', 'Saudi League', ['Solocalcio', 'Como TV']),
    (4, '20:00', 'Diretta Gol Saudi League', 'Saudi League', ['Sportitalia']),

    # Day 5 - 22 Mag (Ven)
    (5, '00:00', 'La Guaira - Independiente Rivadavia', 'Copa Libertadores', ['Como TV']),
    (5, '00:00', 'Atletico Mineiro - Cienciano', 'Copa Sudamericana', ['Como TV']),
    (5, '00:00', 'Puerto Cabello - Juventud', 'Copa Sudamericana', ['Como TV']),
    (5, '02:00', 'Racing - Caracas', 'Copa Sudamericana', ['Como TV']),
    (5, '02:30', 'Peñarol - Corinthians', 'Copa Libertadores', ['Como TV']),
    (5, '02:30', 'Universidad Catolica - Barcelona', 'Copa Libertadores', ['Como TV']),
    (5, '02:30', 'Blooming - Carabobo', 'Copa Sudamericana', ['Como TV']),
    (5, '04:00', 'Macará - Alianza Atletico', 'Copa Sudamericana', ['Como TV']),
    (5, '15:00', 'Cesena - Inter', 'Playoff Primavera', ['Sportitalia']),
    (5, '20:00', 'Sudtirol - Bari', 'Playout Serie B', ['DAZN', 'LAB Channel']),
    (5, '21:00', 'Lens - Nizza', 'Coppa di Francia Final', ['Como TV']),

    # Day 6 - 23 Mag (Sab)
    (6, '18:00', 'Barcellona - Lione', 'Champions League Femminile Final', ['Disney+']),
    (6, '20:00', 'Bayern - Stoccarda', 'Coppa di Germania Final', ['Sky Sport', 'NOW']),
    (6, '20:30', 'St. Louis City - Austin', 'MLS', ['Apple TV']),
    (6, '21:00', 'Alaves - Rayo Vallecano', 'La Liga', ['DAZN']),
    (6, '21:00', 'Betis - Levante', 'La Liga', ['DAZN']),
    (6, '21:00', 'Celta - Siviglia', 'La Liga', ['DAZN']),
    (6, '21:00', 'Espanyol - Real Sociedad', 'La Liga', ['DAZN']),
    (6, '21:00', 'Getafe - Osasuna', 'La Liga', ['DAZN']),
    (6, '21:00', 'Girona - Elche', 'La Liga', ['DAZN']),
    (6, '21:00', 'Maiorca - Oviedo', 'La Liga', ['DAZN']),
    (6, '21:00', 'Real Madrid - Athletic', 'La Liga', ['DAZN']),
    (6, '21:00', 'Valencia - Barcellona', 'La Liga', ['DAZN']),
    (6, '21:00', 'Villarreal - Atletico Madrid', 'La Liga', ['DAZN']),
    (6, '22:30', 'Minnesota United - Real Salt Lake', 'MLS', ['Apple TV']),

    # Day 7 - 24 Mag (Dom)
    (7, '01:30', 'Charlotte - New England Revolution', 'MLS', ['Apple TV']),
    (7, '01:30', 'Cincinnati - Orlando City', 'MLS', ['Apple TV']),
    (7, '01:30', 'DC United - Montreal Impact', 'MLS', ['Apple TV']),
    (7, '02:30', 'Chicago Fire - Toronto', 'MLS', ['Apple TV']),
    (7, '02:30', 'Nashville - New York City', 'MLS', ['Apple TV']),
    (7, '02:30', 'Sporting KC - New York RB', 'MLS', ['Apple TV']),
    (7, '03:30', 'Colorado Rapids - Dallas', 'MLS', ['Apple TV']),
    (7, '03:30', 'Portland Timbers - San Jose Earthquakes', 'MLS', ['Apple TV']),
    (7, '03:30', 'San Diego - Vancouver Whitecaps', 'MLS', ['Apple TV']),
    (7, '04:30', 'LA Galaxy - Houston Dynamo', 'MLS', ['Apple TV']),
    (7, '18:00', 'Juventus - Roma', 'Coppa Italia Femminile', ['Rai 2']),
    (7, '20:30', 'Serie B', 'Serie B', ['TV8']),
    (7, '21:00', 'Playoff Serie B Final (Andata)', 'Serie B', ['DAZN', 'LAB Channel']),
    (7, '23:00', 'Columbus Crew - Atlanta United', 'MLS', ['Apple TV']),
]

# Sort matches per day by time
MATCHES.sort(key=lambda x: (x[0], x[1]))

def build_filter_classes(channels):
    """Return space-separated CSS classes for the filter system, plus a list of (display_name, badge_class)."""
    filter_slugs = set()
    badges = []
    seen_badges = set()
    for ch in channels:
        if ch not in CHANNEL_MAP:
            continue
        disp, badge_cls, fslug = CHANNEL_MAP[ch]
        if fslug:
            filter_slugs.add(fslug)
        # Avoid duplicate badges (e.g. Sky Sport 1 + Sky Sport Uno)
        if disp not in seen_badges:
            badges.append((disp, badge_cls))
            seen_badges.add(disp)
    return ' '.join(f'ch-{s}' for s in sorted(filter_slugs)), badges

def esc(s):
    return html_lib.escape(s)

# Build tab style selectors
tab_active = ',\n'.join(
    f'.ptv-w #ptv-d{i}:checked~.ptv-tabs label[for=ptv-d{i}]'
    for i, _, _ in DAYS
)
tab_active_after = ',\n'.join(
    f'.ptv-w #ptv-d{i}:checked~.ptv-tabs label[for=ptv-d{i}]:after'
    for i, _, _ in DAYS
)

# Build filter chip active style selectors
filt_active = ',\n'.join(
    f'.ptv-w #ptv-c-{slug}:checked~.ptv-filt label[for=ptv-c-{slug}]'
    for slug, _ in FILTERS
)

# Build show-row selectors: for each (day, filter) combination
show_selectors = []
for i, _, _ in DAYS:
    for slug, _ in FILTERS:
        if slug == 'all':
            show_selectors.append(
                f'.ptv-w #ptv-d{i}:checked~#ptv-c-all:checked~.ptv-body .ptv-row.d-{i}'
            )
        else:
            show_selectors.append(
                f'.ptv-w #ptv-d{i}:checked~#ptv-c-{slug}:checked~.ptv-body .ptv-row.d-{i}.ch-{slug}'
            )
show_block = ',\n'.join(show_selectors)

# Build empty-state selectors per (day, filter): show empty when no match shown
# Simpler: show generic empty when there are no visible rows. Pure CSS doesn't allow "if no children visible".
# We use a per-day empty placeholder shown when day has 0 matches; for filter combinations producing 0, we don't show empty.
# Determine days with zero matches:
days_with_matches = {d for d, _, _, _, _ in MATCHES}
empty_day_selectors = []
for i, _, _ in DAYS:
    if i not in days_with_matches:
        empty_day_selectors.append(
            f'.ptv-w #ptv-d{i}:checked~.ptv-body .ptv-empty-d{i}'
        )
empty_block = ',\n'.join(empty_day_selectors) if empty_day_selectors else ''

# Build rows HTML
rows_html = []
for day_idx, time, match, comp, channels in MATCHES:
    filter_classes, badges = build_filter_classes(channels)
    badges_html = ''.join(
        f'<span class="ptv-bdg {cls}">{esc(name)}</span>' for name, cls in badges
    )
    rows_html.append(
        f'<div class="ptv-row d-{day_idx} {filter_classes}">'
        f'<div class="ptv-time">{esc(time)}</div>'
        f'<div class="ptv-match"><span class="ptv-match-name">{esc(match)}</span>'
        f'<span class="ptv-comp">{esc(comp)}</span></div>'
        f'<div class="ptv-chs">{badges_html}</div>'
        f'</div>'
    )

# Empty placeholders
empty_html = []
for i, short, date in DAYS:
    if i not in days_with_matches:
        empty_html.append(
            f'<div class="ptv-empty ptv-empty-d{i}">Nessun match in programma.</div>'
        )

# Day radios + tab labels
day_radios = '\n'.join(
    f'<input type="radio" name="ptv-day" id="ptv-d{i}" class="ptv-rd"'
    + (' checked' if i == 1 else '') + '>'
    for i, _, _ in DAYS
)
day_tabs = '\n'.join(
    f'<label for="ptv-d{i}">{short}<small>{date}</small></label>'
    for i, short, date in DAYS
)

# Channel radios + filter labels
ch_radios = '\n'.join(
    f'<input type="radio" name="ptv-ch" id="ptv-c-{slug}" class="ptv-rc"'
    + (' checked' if slug == 'all' else '') + '>'
    for slug, _ in FILTERS
)
ch_labels = '\n'.join(
    f'<label for="ptv-c-{slug}">{esc(label)}</label>'
    for slug, label in FILTERS
)

html_out = f'''<div class="ptv-w">
<style>
.ptv-w{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;max-width:820px;margin:0 auto;color:#1a1a1a;background:#fff;border:1px solid #e5e7eb;border-radius:12px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.04)}}
.ptv-w *{{box-sizing:border-box}}
.ptv-w .ptv-rd,.ptv-w .ptv-rc{{position:absolute;opacity:0;pointer-events:none;width:0;height:0}}
.ptv-w .ptv-tabs{{display:flex;flex-wrap:wrap;gap:0;background:#f8fafc;border-bottom:1px solid #e5e7eb;padding:8px 8px 0}}
.ptv-w .ptv-tabs label{{flex:1 1 auto;min-width:80px;text-align:center;padding:10px 8px;cursor:pointer;font-size:13px;font-weight:600;color:#64748b;border-radius:8px 8px 0 0;border:1px solid transparent;border-bottom:none;transition:background .15s,color .15s;line-height:1.3}}
.ptv-w .ptv-tabs label small{{display:block;font-size:11px;font-weight:500;opacity:.75;margin-top:2px}}
.ptv-w .ptv-tabs label:hover{{background:#eef2f7;color:#0f172a}}
.ptv-w .ptv-filt{{display:flex;flex-wrap:wrap;gap:6px;padding:12px;background:#fff;border-bottom:1px solid #f1f5f9}}
.ptv-w .ptv-filt label{{padding:6px 12px;border:1px solid #e2e8f0;border-radius:999px;cursor:pointer;font-size:12px;font-weight:500;color:#475569;background:#fff;transition:all .15s}}
.ptv-w .ptv-filt label:hover{{border-color:#94a3b8;color:#0f172a}}
.ptv-w .ptv-body{{padding:0;max-height:560px;overflow-y:auto}}
.ptv-w .ptv-row{{display:none;align-items:center;gap:14px;padding:14px 16px;border-bottom:1px solid #f1f5f9}}
.ptv-w .ptv-row:last-child{{border-bottom:none}}
.ptv-w .ptv-row:hover{{background:#fafbfc}}
.ptv-w .ptv-time{{flex:0 0 60px;font-size:16px;font-weight:700;color:#0f172a;font-variant-numeric:tabular-nums}}
.ptv-w .ptv-match{{flex:1 1 auto;min-width:0}}
.ptv-w .ptv-match-name{{font-size:14px;font-weight:600;color:#0f172a;line-height:1.3;display:block}}
.ptv-w .ptv-comp{{display:block;font-size:11px;color:#64748b;margin-top:2px;text-transform:uppercase;letter-spacing:.3px;font-weight:500}}
.ptv-w .ptv-chs{{flex:0 0 auto;display:flex;flex-wrap:wrap;gap:4px;justify-content:flex-end;max-width:220px}}
.ptv-w .ptv-bdg{{display:inline-flex;align-items:center;padding:4px 9px;border-radius:6px;font-size:11px;font-weight:700;color:#fff;letter-spacing:.2px;white-space:nowrap;line-height:1}}
.ptv-w .b-dazn{{background:#fb7700}}
.ptv-w .b-sky{{background:#0571c1}}
.ptv-w .b-sky-calcio{{background:#003d7a}}
.ptv-w .b-now{{background:#00b3a4}}
.ptv-w .b-como{{background:#7c3aed}}
.ptv-w .b-apple{{background:#000000}}
.ptv-w .b-sportitalia{{background:#1e40af}}
.ptv-w .b-rai{{background:#0ea5e9}}
.ptv-w .b-tv8{{background:#f97316}}
.ptv-w .b-lab{{background:#475569}}
.ptv-w .b-disney{{background:#0c2a5f}}
.ptv-w .b-solocalcio{{background:#16a34a}}
.ptv-w .b-onefootball{{background:#0a5cd6}}
.ptv-w .b-vivo{{background:#0284c7}}
.ptv-w .ptv-empty{{display:none;padding:32px 16px;text-align:center;color:#94a3b8;font-size:13px;font-style:italic}}

{tab_active}{{background:#fff;color:#0f172a;border-color:#e5e7eb;position:relative}}
{tab_active_after}{{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:#fff}}

{filt_active}{{background:#0f172a;color:#fff;border-color:#0f172a}}

{show_block}{{display:flex}}

{empty_block + "{display:block}" if empty_block else ""}

@media (max-width:520px){{
.ptv-w .ptv-tabs label{{font-size:12px;padding:8px 4px;min-width:60px}}
.ptv-w .ptv-tabs label small{{font-size:10px}}
.ptv-w .ptv-row{{padding:12px;gap:10px;flex-wrap:wrap}}
.ptv-w .ptv-time{{flex:0 0 50px;font-size:14px}}
.ptv-w .ptv-match-name{{font-size:13px}}
.ptv-w .ptv-chs{{max-width:100%;justify-content:flex-start;flex-basis:100%;padding-left:60px}}
.ptv-w .ptv-bdg{{font-size:10px;padding:3px 7px}}
}}
</style>
{day_radios}
{ch_radios}
<div class="ptv-tabs">
{day_tabs}
</div>
<div class="ptv-filt">
{ch_labels}
</div>
<div class="ptv-body">
{chr(10).join(rows_html)}
{chr(10).join(empty_html)}
</div>
</div>
'''

with open('widget-prog-tv.html', 'w') as f:
    f.write(html_out)
print(f"Generated widget with {len(MATCHES)} matches over {len(DAYS)} days")
