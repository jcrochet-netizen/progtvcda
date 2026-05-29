#!/usr/bin/env python3
"""Build the WordPress-embeddable football TV widget from merged sources."""
import html as html_lib

# Channel filter slugs (used for CSS filtering)
# Each match row gets classes for the filters it matches.
FILTERS = [
    ('all', 'Tutte'),
    ('dazn', 'DAZN'),
    ('sky', 'Sky'),
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
    'DAZN':              ('DAZN',             'b-dazn',       'dazn'),
    'Sky Sport':         ('Sky Sport',        'b-sky',        'sky'),
    'Sky Sport Uno':     ('Sky Sport Uno',    'b-sky',        'sky'),
    'Sky Sport 1':       ('Sky Sport Uno',    'b-sky',        'sky'),
    'Sky Sport 2':       ('Sky Sport 2',      'b-sky',        'sky'),
    'Sky Sport 3':       ('Sky Sport 3',      'b-sky',        'sky'),
    'Sky Sport Max':     ('Sky Sport Max',    'b-sky',        'sky'),
    'Sky Sport 251':     ('Sky Sport 251',    'b-sky',        'sky'),
    'Sky':               ('Sky',              'b-sky',        'sky'),
    'Sky Sport Calcio':  ('Sky Sport Calcio', 'b-sky-calcio', 'sky'),
    'NOW':               ('NOW',             'b-now',         'now'),
    'Como TV':           ('Como TV',         'b-como',        'como'),
    'Apple TV':          ('Apple TV',        'b-apple',       'apple'),
    'Sportitalia':       ('Sportitalia',     'b-sportitalia', 'sportitalia'),
    'Rai 1':             ('Rai 1',           'b-rai',         'rai'),
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
    (1, 'Ven', '29 Mag'),
    (2, 'Sab', '30 Mag'),
    (3, 'Dom', '31 Mag'),
    (4, 'Lun', '1 Giu'),
    (5, 'Mar', '2 Giu'),
    (6, 'Mer', '3 Giu'),
    (7, 'Gio', '4 Giu'),
]

# Merged matches: (day_idx, time, match, competition, [channels])
MATCHES = [
    # Day 1 - Ven 29 Mag (Oggi)
    (1, '00:00', 'Cerro Porteno - Sporting Cristal', 'Copa Libertadores', ['Como TV']),
    (1, '00:00', 'Palmeiras - Junior', 'Copa Libertadores', ['Como TV']),
    (1, '02:30', 'Boca Juniors - Universidad Catolica', 'Copa Libertadores', ['Como TV']),
    (1, '02:30', 'Cruzeiro - Barcelona', 'Copa Libertadores', ['Como TV']),
    (1, '02:30', 'America Cali - Macará', 'Copa Sudamericana', ['Como TV']),
    (1, '02:30', 'Tigre - Alianza Atletico', 'Copa Sudamericana', ['Como TV']),
    (1, '20:00', 'Monza - Catanzaro', 'Serie B Playoff', ['DAZN', 'Sky Sport Uno', 'TV8', 'LAB Channel']),
    (1, '20:30', 'Bosnia Erzegovina - Macedonia del Nord', 'Amichevole Internazionale', ['Sky Sport Max']),
    (1, '20:45', 'Nizza - Saint Etienne', 'Ligue 1', ['Sky Sport Calcio']),

    # Day 2 - Sab 30 Mag (Domani)
    (2, '14:00', 'Scozia - Curacao', 'Amichevole Internazionale', ['Sky Sport Calcio']),
    (2, '18:00', 'PSG - Arsenal', 'UEFA Champions League Final', ['Sky', 'Sky Sport Calcio', 'Sky Sport Uno', 'Sky Sport 251', 'NOW']),

    # Day 3 - Dom 31 Mag
    (3, '13:30', 'Belgio - Estonia', 'Europei Under 17', []),
    (3, '13:30', 'Spagna - Croazia', 'Europei Under 17', []),
    (3, '15:00', 'Svizzera - Giordania', 'Amichevole Internazionale', ['Sky Sport Calcio']),
    (3, '20:45', 'Germania - Finlandia', 'Amichevole Internazionale', ['Sky Sport Calcio']),

    # Day 4 - Lun 1 Giu
    (4, '19:30', 'Turchia - Macedonia del Nord', 'Amichevole Internazionale', ['Sky Sport Calcio']),

    # Day 5 - Mar 2 Giu
    (5, '18:00', 'Croazia - Belgio', 'Amichevole Internazionale', ['Sky Sport Calcio']),
    (5, '20:45', 'Galles - Ghana', 'Amichevole Internazionale', ['Sky Sport Calcio']),

    # Day 6 - Mer 3 Giu
    (6, '18:15', 'Serie C Playoff - Finale Andata', 'Serie C', ['Sky Sport Calcio']),
    (6, '20:45', 'Lussemburgo - Italia', 'Amichevole Internazionale', ['Rai 1']),
    (6, '20:45', 'Olanda - Algeria', 'Amichevole Internazionale', ['Sky Sport Calcio']),

    # Day 7 - Gio 4 Giu
    (7, '21:10', 'Francia - Costa D\'Avorio', 'Amichevole Internazionale', ['Sky Sport Calcio']),
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

# Standalone page for GitHub Pages preview
index_html = f'''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Programma TV Calcio</title>
<style>body{{margin:0;padding:24px 16px;background:#f1f5f9;min-height:100vh;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}}</style>
</head>
<body>
{html_out}
</body>
</html>
'''
with open('index.html', 'w') as f:
    f.write(index_html)

print(f"Generated widget with {len(MATCHES)} matches over {len(DAYS)} days")
