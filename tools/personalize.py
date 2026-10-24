"""Build index.html from src/template.html + src/data/portfolio.json.

    python3 tools/personalize.py
"""
import html
import json
import pathlib
import re

R = pathlib.Path(__file__).resolve().parent.parent
d = json.loads((R / 'src/data/portfolio.json').read_text())
tpl = (R / 'src/template.html').read_text()

e = lambda t: html.escape(t, quote=False).replace("'", '&#x27;')
REV = 'style="opacity:0;transform:translateY(24px)"'
STRIP = lambda u: u.split('://', 1)[-1]


def facts():
    row = ('<div class="grid grid-cols-[7rem_1fr] gap-4 border-t border-line py-4 sm:grid-cols-[9rem_1fr]">'
           '<dt class="text-label pt-0.5 text-muted">{k}</dt><dd class="text-[15px] leading-relaxed text-ink">{v}</dd></div>')
    return '<dl class="mt-12">' + ''.join(row.format(k=e(k), v=e(v)) for k, v in d['facts']) + '</dl>'


def what_i_do():
    return ''.join(
        f'<div {REV}><div class="grid gap-2 border-t border-line py-7 lg:grid-cols-12 lg:gap-10"><h3 class="text-display-sm text-ink lg:col-span-5">{e(k)}</h3>'
        f'<p class="self-center leading-relaxed text-muted lg:col-span-6 lg:col-start-7">{e(v)}</p></div></div>' for k, v in d['whatIDo'])


def skills():
    out = ''
    for cat, items in d['skills']:
        core = [n for n, strong in items if strong]
        more = [n for n, strong in items if not strong]
        spans = ''
        for i, name in enumerate(core):
            sep = '<span aria-hidden="true" class="text-line-strong"> · </span>' if i < len(core) - 1 else ''
            spans += f'<span><span class="whitespace-nowrap text-ink">{e(name)}</span>{sep}</span>'
        also = f'<p class="mt-3 text-[15px] leading-relaxed text-muted">Also used: {e(", ".join(more))}</p>' if more else ''
        out += (f'<div {REV}><div class="grid gap-3 border-t border-line py-8 lg:grid-cols-12 lg:gap-10"><h3 class="text-label pt-1 text-muted lg:col-span-3">{e(cat)}</h3>'
                f'<div class="lg:col-span-9"><p class="text-lg leading-[1.9]">{spans}</p>{also}</div></div></div>')
    return '<div class="mt-16 lg:mt-20">' + out


def bold(t):
    return re.sub(r'\*\*(.+?)\*\*', r'<strong class="font-semibold text-ink">\1</strong>', t)


def experience():
    def one(x):
        bl = ''.join(f'<li class="border-l border-line-strong pl-4 leading-relaxed text-muted">{bold(e(b))}</li>' for b in x['bullets'])
        return (f'<li><div {REV}><div class="grid gap-4 border-t border-line py-10 lg:grid-cols-12 lg:gap-10"><div class="text-label space-y-1.5 text-muted lg:col-span-3 lg:pt-2"><p>{x["dates"]}</p><p>{e(x["place"])}</p></div>'
                f'<div class="lg:col-span-9"><h3 class="text-display-sm text-ink">{e(x["role"])}<span class="text-muted"> — </span><span class="text-accent">{e(x["org"])}</span></h3>'
                f'<ul class="mt-5 max-w-[68ch] space-y-2.5">{bl}</ul></div></div></div></li>')
    return '<ol class="mt-16 lg:mt-20">' + ''.join(one(x) for x in d['experience']) + '</ol>'


def media(p, src):
    img = (f'<img alt="{e(p["name"])} preview" loading="lazy" width="1600" height="900" decoding="async" '
           f'class="aspect-video w-full rounded-sm border border-line object-cover object-top" style="color:transparent" src="{src}"/>')
    if p.get('video'):
        return (f'<button type="button" aria-label="Watch {e(p["name"])} demo video" data-video="{p["video"].lstrip("/")}" class="group/media relative block w-full cursor-pointer text-left">'
                f'{img}<span class="text-label absolute bottom-0 left-0 border border-line bg-bg/90 px-4 py-3 text-ink" style="margin:1rem">▶ Watch demo</span></button>')
    if p.get('videoSoon'):
        return (f'<div class="relative">{img}<span class="text-label absolute bottom-0 left-0 border border-line bg-bg/90 px-4 py-3 text-muted" style="margin:1rem">▶ Demo video — coming soon</span></div>')
    return img


def projects():
    def one(i, p):
        flip = i % 2 == 1
        mc = 'lg:col-span-7 lg:order-2 lg:col-start-6' if flip else 'lg:col-span-7 '
        tc = 'lg:col-span-5 lg:order-1 lg:col-start-1' if flip else 'lg:col-span-5 '
        img = p.get('image', '')
        src = img.lstrip('/') if img and (R / 'public' / img.lstrip('/')).exists() else 'projects/placeholder.png'
        tag = (p['year'] + ' · ' if p['year'] else '') + p['tag']
        links = ''
        if p['live']:
            links += f'<a href="{p["live"]}" target="_blank" rel="noopener noreferrer" class="link-underline is-drawn" style="color:var(--row-accent)">Live ↗</a>'
        if p['code']:
            links += f'<a href="{p["code"]}" target="_blank" rel="noopener noreferrer" class="link-underline text-muted hover:text-ink">Code ↗</a>'
        links = f'<div class="mt-7 flex items-center gap-7">{links}</div>' if links else ''
        metric = f'<p class="text-label mt-5" style="color:var(--row-accent)">{e(p["metric"])}</p>' if p['metric'] else ''
        return (f'<article class="border-t border-line py-14 lg:py-20" style="--row-accent:var(--hue-{p["accent"]})"><div class="grid gap-10 lg:grid-cols-12 lg:items-center">'
                f'<div class="{mc}" {REV}>{media(p, src)}</div>'
                f'<div class="{tc}"><div {REV}><span aria-hidden="true" class="index-numeral block" style="color:color-mix(in srgb, var(--row-accent) 40%, transparent)">{i + 1:02d}</span>'
                f'<p class="text-label mt-4" style="color:var(--row-accent)">{e(tag)}</p><h3 class="text-display-sm mt-3 text-ink">{e(p["name"])}</h3><p class="mt-2 text-lg text-muted">{e(p["subtitle"])}</p>'
                f'<p class="mt-5 leading-[1.8] text-muted">{e(p["description"])}</p>{metric}<p class="mt-5 font-mono text-[13px] leading-relaxed text-muted">{e(p["stack"])}</p>{links}</div></div></div></article>')
    return '<div class="mt-16 lg:mt-20">' + ''.join(one(i, p) for i, p in enumerate(x for x in d['projects'] if not x.get('hidden')))


def contact_rows():
    def row(href, label, text, extra=''):
        return (f'<div {REV}><a href="{href}" {extra}class="group grid grid-cols-[7rem_1fr_auto] items-baseline gap-4 border-t border-line py-5 transition-colors hover:bg-surface sm:grid-cols-[10rem_1fr_auto]">'
                f'<span class="text-label text-muted">{label}</span><span class="truncate text-ink transition-colors group-hover:text-accent">{text}</span>'
                f'<span aria-hidden="true" class="text-muted transition-colors group-hover:text-accent">↗</span></a></div>')
    ext = 'target="_blank" rel="noopener noreferrer" '
    out = '<div class="mt-16 lg:mt-24">'
    if d['linkedin']:
        out += row(d['linkedin'], 'LinkedIn', STRIP(d['linkedin']), ext)
    if d['github']:
        out += row(d['github'], 'GitHub', STRIP(d['github']), ext)
    out += row('resume.pdf', 'Resume', 'Download PDF', f'download="{d["resumeFile"]}" ')
    return out


tokens = {
    '@facts': facts(), '@whatIDo': what_i_do(), '@skills': skills(),
    '@experience': experience(), '@projects': projects(), '@contactRows': contact_rows(),
    'metaDescription': e(d['metaDescription']), 'title': d['title'], 'keywords': d['keywords'],
    'name': d['name'], 'headline': d['headline'], 'city': d['city'], 'status': d['status'],
    'heroLine1': d['heroLines'][0],
    'heroLine2': d['heroLines'][1].replace('<em>', '<em class="not-italic text-accent">'),
    'heroIntro': e(d['heroIntro']), 'resumeFile': d['resumeFile'],
    'aboutLead': e(d['aboutLead']), 'aboutP1': e(d['aboutParagraphs'][0]), 'aboutP2': e(d['aboutParagraphs'][1]),
    'photo': d.get('photo', 'suyash.jpg').lstrip('/'), 'coords': d['coords'],
    'skillsHeading': e(d['skillsHeading']), 'experienceHeading': e(d['experienceHeading']),
    'projectsHeading': e(d['projectsHeading']), 'contactHeading': e(d['contactHeading']),
    'contactIntro': e(d['contactIntro']), 'email': d['email'], 'contactNote': e(d['contactNote']),
    'siteUrl': d['siteUrl'], 'location': d['location'], 'tzShort': d['timezone'].split('(')[1][:-1],
}
for i, (num, label) in enumerate(d['stats']):
    tokens[f'stat{i}Num'] = num
    tokens[f'stat{i}Label'] = label

out = tpl
for key, val in tokens.items():
    out = out.replace('{{' + key + '}}', val)
assert '{{' not in out, 'unfilled placeholder: ' + out[out.index('{{'):][:40]

(R / 'index.html').write_text(out)
print('index.html written')
