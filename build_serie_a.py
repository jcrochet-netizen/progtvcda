#!/usr/bin/env python3
"""Build the Serie A matchday widget (subset of main widget)."""
import html as html_lib

FILTERS = [
    ('all', 'Tutte'),
    ('dazn', 'DAZN'),
    ('sky', 'Sky'),
]

CHANNEL_MAP = {
    'DAZN':       ('DAZN',       'b-dazn',  'dazn'),
    'Sky Sport':  ('Sky Sport',  'b-sky',   'sky'),
    'Sky':        ('Sky',        'b-sky',   'sky'),
}

DAYS = [
    (1, 'Ven', '22 Mag'),
    (2, 'Sab', '23 Mag'),
    (3, 'Dom', '24 Mag'),
]

MATCHES = [
    (1, '20:45', 'Fiorentina - Atalanta', 'Serie A', ['DAZN']),
    (2, '18:00', 'Bologna - Inter', 'Serie A', ['DAZN']),
    (2, '20:45', 'Lazio - Pisa', 'Serie A', ['DAZN', 'Sky Sport']),
    (3, '15:00', 'Parma - Sassuolo', 'Serie A', ['DAZN']),
    (3, '18:00', 'Napoli - Udinese', 'Serie A', ['DAZN']),
    (3, '20:45', 'Cremonese - Como', 'Serie A', ['DAZN']),
    (3, '20:45', 'Lecce - Genoa', 'Serie A', ['DAZN', 'Sky Sport']),
    (3, '20:45', 'Milan - Cagliari', 'Serie A', ['DAZN']),
    (3, '20:45', 'Torino - Juventus', 'Serie A', ['DAZN', 'Sky Sport']),
    (3, '20:45', 'Verona - Roma', 'Serie A', ['DAZN']),
]
MATCHES.sort(key=lambda x: (x[0], x[1]))

NS = 'sera'  # CSS / id namespace, distinct from main widget (.ptv-w)

def esc(s):
    return html_lib.escape(s)

def build_filter_classes(channels):
    filter_slugs = set()
    badges = []
    seen = set()
    for ch in channels:
        if ch not in CHANNEL_MAP:
            continue
        disp, badge_cls, fslug = CHANNEL_MAP[ch]
        if fslug:
            filter_slugs.add(fslug)
        if disp not in seen:
            badges.append((disp, badge_cls))
            seen.add(disp)
    return ' '.join(f'ch-{s}' for s in sorted(filter_slugs)), badges

tab_active = ',\n'.join(
    f'.{NS}-w #{NS}-d{i}:checked~.{NS}-tabs label[for={NS}-d{i}]' for i, _, _ in DAYS
)
tab_active_after = ',\n'.join(
    f'.{NS}-w #{NS}-d{i}:checked~.{NS}-tabs label[for={NS}-d{i}]:after' for i, _, _ in DAYS
)
filt_active = ',\n'.join(
    f'.{NS}-w #{NS}-c-{slug}:checked~.{NS}-filt label[for={NS}-c-{slug}]' for slug, _ in FILTERS
)
show_selectors = []
for i, _, _ in DAYS:
    for slug, _ in FILTERS:
        if slug == 'all':
            show_selectors.append(
                f'.{NS}-w #{NS}-d{i}:checked~#{NS}-c-all:checked~.{NS}-body .{NS}-row.d-{i}'
            )
        else:
            show_selectors.append(
                f'.{NS}-w #{NS}-d{i}:checked~#{NS}-c-{slug}:checked~.{NS}-body .{NS}-row.d-{i}.ch-{slug}'
            )
show_block = ',\n'.join(show_selectors)

rows_html = []
for day_idx, time, match, comp, channels in MATCHES:
    filter_classes, badges = build_filter_classes(channels)
    badges_html = ''.join(
        f'<span class="{NS}-bdg {cls}">{esc(name)}</span>' for name, cls in badges
    )
    rows_html.append(
        f'<div class="{NS}-row d-{day_idx} {filter_classes}">'
        f'<div class="{NS}-time">{esc(time)}</div>'
        f'<div class="{NS}-match"><span class="{NS}-match-name">{esc(match)}</span>'
        f'<span class="{NS}-comp">{esc(comp)}</span></div>'
        f'<div class="{NS}-chs">{badges_html}</div>'
        f'</div>'
    )

day_radios = '\n'.join(
    f'<input type="radio" name="{NS}-day" id="{NS}-d{i}" class="{NS}-rd"'
    + (' checked' if i == 1 else '') + '>'
    for i, _, _ in DAYS
)
day_tabs = '\n'.join(
    f'<label for="{NS}-d{i}">{short}<small>{date}</small></label>'
    for i, short, date in DAYS
)
ch_radios = '\n'.join(
    f'<input type="radio" name="{NS}-ch" id="{NS}-c-{slug}" class="{NS}-rc"'
    + (' checked' if slug == 'all' else '') + '>'
    for slug, _ in FILTERS
)
ch_labels = '\n'.join(
    f'<label for="{NS}-c-{slug}">{esc(label)}</label>' for slug, label in FILTERS
)

html_out = f'''<div class="{NS}-w">
<style>
.{NS}-w{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;max-width:820px;margin:0 auto;color:#1a1a1a;background:#fff;border:1px solid #e5e7eb;border-radius:12px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.04)}}
.{NS}-w *{{box-sizing:border-box}}
.{NS}-w .{NS}-rd,.{NS}-w .{NS}-rc{{position:absolute;opacity:0;pointer-events:none;width:0;height:0}}
.{NS}-w .{NS}-tabs{{display:flex;flex-wrap:wrap;gap:0;background:#f8fafc;border-bottom:1px solid #e5e7eb;padding:8px 8px 0}}
.{NS}-w .{NS}-tabs label{{flex:1 1 auto;min-width:80px;text-align:center;padding:10px 8px;cursor:pointer;font-size:13px;font-weight:600;color:#64748b;border-radius:8px 8px 0 0;border:1px solid transparent;border-bottom:none;transition:background .15s,color .15s;line-height:1.3}}
.{NS}-w .{NS}-tabs label small{{display:block;font-size:11px;font-weight:500;opacity:.75;margin-top:2px}}
.{NS}-w .{NS}-tabs label:hover{{background:#eef2f7;color:#0f172a}}
.{NS}-w .{NS}-filt{{display:flex;flex-wrap:wrap;gap:6px;padding:12px;background:#fff;border-bottom:1px solid #f1f5f9}}
.{NS}-w .{NS}-filt label{{padding:6px 12px;border:1px solid #e2e8f0;border-radius:999px;cursor:pointer;font-size:12px;font-weight:500;color:#475569;background:#fff;transition:all .15s}}
.{NS}-w .{NS}-filt label:hover{{border-color:#94a3b8;color:#0f172a}}
.{NS}-w .{NS}-body{{padding:0}}
.{NS}-w .{NS}-row{{display:none;align-items:center;gap:14px;padding:14px 16px;border-bottom:1px solid #f1f5f9}}
.{NS}-w .{NS}-row:last-child{{border-bottom:none}}
.{NS}-w .{NS}-row:hover{{background:#fafbfc}}
.{NS}-w .{NS}-time{{flex:0 0 60px;font-size:16px;font-weight:700;color:#0f172a;font-variant-numeric:tabular-nums}}
.{NS}-w .{NS}-match{{flex:1 1 auto;min-width:0}}
.{NS}-w .{NS}-match-name{{font-size:14px;font-weight:600;color:#0f172a;line-height:1.3;display:block}}
.{NS}-w .{NS}-comp{{display:block;font-size:11px;color:#64748b;margin-top:2px;text-transform:uppercase;letter-spacing:.3px;font-weight:500}}
.{NS}-w .{NS}-chs{{flex:0 0 auto;display:flex;flex-wrap:wrap;gap:4px;justify-content:flex-end;max-width:220px}}
.{NS}-w .{NS}-bdg{{display:inline-flex;align-items:center;padding:4px 9px;border-radius:6px;font-size:11px;font-weight:700;color:#fff;letter-spacing:.2px;white-space:nowrap;line-height:1}}
.{NS}-w .b-dazn{{background:#fb7700}}
.{NS}-w .b-sky{{background:#0571c1}}

{tab_active}{{background:#fff;color:#0f172a;border-color:#e5e7eb;position:relative}}
{tab_active_after}{{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:#fff}}

{filt_active}{{background:#0f172a;color:#fff;border-color:#0f172a}}

{show_block}{{display:flex}}

@media (max-width:520px){{
.{NS}-w .{NS}-tabs label{{font-size:12px;padding:8px 4px;min-width:60px}}
.{NS}-w .{NS}-tabs label small{{font-size:10px}}
.{NS}-w .{NS}-row{{padding:12px;gap:10px;flex-wrap:wrap}}
.{NS}-w .{NS}-time{{flex:0 0 50px;font-size:14px}}
.{NS}-w .{NS}-match-name{{font-size:13px}}
.{NS}-w .{NS}-chs{{max-width:100%;justify-content:flex-start;flex-basis:100%;padding-left:60px}}
.{NS}-w .{NS}-bdg{{font-size:10px;padding:3px 7px}}
}}
</style>
{day_radios}
{ch_radios}
<div class="{NS}-tabs">
{day_tabs}
</div>
<div class="{NS}-filt">
{ch_labels}
</div>
<div class="{NS}-body">
{chr(10).join(rows_html)}
</div>
</div>
'''

with open('serie-a-widget.html', 'w') as f:
    f.write(html_out)

# Standalone page for iframe embedding
serie_a_page = f'''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Serie A - Programma TV</title>
<style>html,body{{margin:0;padding:0;background:transparent;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}}body{{padding:8px}}</style>
</head>
<body>
{html_out}
</body>
</html>
'''
with open('serie-a.html', 'w') as f:
    f.write(serie_a_page)

print(f"Generated Serie A widget with {len(MATCHES)} matches over {len(DAYS)} days")
