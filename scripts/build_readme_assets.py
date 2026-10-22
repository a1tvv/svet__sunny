"""Пересобирает картинки для README (docs/assets) в стиле iOS.

Цифры в плитках считаются сами: лекции и части — из main/sira_data.py, тесты — из main/tests.py.
Запуск: python3 scripts/build_readme_assets.py
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from main.sira_data import SIRA_PAGES  # noqa: E402

OUT = os.path.join(ROOT, 'docs', 'assets')
FONT = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', SFMono-Regular, Menlo, Consolas, monospace"
AI = ('<stop offset="0" stop-color="#ff9f0a"/><stop offset="0.35" stop-color="#ff375f"/>'
      '<stop offset="0.7" stop-color="#bf5af2"/><stop offset="1" stop-color="#0a84ff"/>')
TILE = ('<linearGradient id="tile" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#161618"/>'
        '<stop offset="1" stop-color="#000000"/></linearGradient>')
TITANIUM = ('<linearGradient id="titanium" x1="0" y1="0" x2="0" y2="1"><stop offset="0.2" stop-color="#ffffff"/>'
            '<stop offset="1" stop-color="#8e8e93"/></linearGradient>')
ICONS = {
    'red': ('#ff6961', '#d70015'), 'blue': ('#64d2ff', '#0a84ff'), 'violet': ('#d48cff', '#7d3bd1'),
    'green': ('#4ade80', '#1e9e47'), 'orange': ('#ffb340', '#d26a00'), 'gray': ('#8e8e93', '#48484a'),
}
esc = html.escape


def save(path, w, h, label, defs, body):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
           f'role="img" aria-label="{esc(label)}">\n<defs>{defs}</defs>\n'
           f'<g font-family="{FONT}">\n{body}\n</g>\n</svg>\n')
    open(full, 'w', encoding='utf-8').write(svg)


def moon(cx, cy, r, fill):
    """Полумесяц: большой круг минус смещённый."""
    return (f'<path d="M{cx + r * 0.35:.1f} {cy - r:.1f}A{r} {r} 0 1 0 {cx + r * 0.35:.1f} {cy + r:.1f}'
            f'A{r * 1.3:.1f} {r * 1.3:.1f} 0 0 1 {cx + r * 0.35:.1f} {cy - r:.1f}Z" fill="{fill}"/>')


# ───────────────────────── баннер ─────────────────────────

def banner():
    defs = (f'<linearGradient id="ai" x1="0" y1="0" x2="1" y2="1">{AI}'
            '<animateTransform attributeName="gradientTransform" type="rotate" from="0 0.5 0.5" to="360 0.5 0.5" '
            'dur="9s" repeatCount="indefinite"/></linearGradient>'
            f'<linearGradient id="aiText" x1="0" y1="0" x2="1" y2="0">{AI}</linearGradient>{TITANIUM}'
            '<radialGradient id="spot" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#ffffff" stop-opacity="0.07"/>'
            '<stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>'
            '<filter id="edgeGlow" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="20"/></filter>'
            '<clipPath id="card"><rect width="1200" height="600" rx="32"/></clipPath>')
    body = (
        '<g clip-path="url(#card)"><rect width="1200" height="600" fill="#000000"/>'
        '<ellipse cx="600" cy="320" rx="560" ry="260" fill="url(#spot)"/>'
        '<rect width="1200" height="600" rx="32" fill="none" stroke="url(#ai)" stroke-width="40" filter="url(#edgeGlow)" opacity="0.85"/>'
        '<rect x="1.5" y="1.5" width="1197" height="597" rx="30.5" fill="none" stroke="url(#ai)" stroke-width="3"/></g>'
        # пилюля с адресом сайта
        '<rect x="410" y="30" width="380" height="46" rx="23" fill="#000000" stroke="#ffffff" stroke-opacity="0.16"/>'
        '<circle cx="443" cy="53" r="8" fill="#30d158"><animate attributeName="opacity" values="1;0.35;1" dur="2.4s" repeatCount="indefinite"/></circle>'
        '<text x="466" y="59.5" font-size="18" font-weight="600" fill="#ffffff">nur-as-sunnah.com</text>'
        '<text x="772" y="59.5" font-size="18" font-weight="600" fill="#30d158" text-anchor="end">online</text>'
        '<text x="600" y="206" text-anchor="middle" font-size="28" font-weight="600" fill="url(#aiText)">Призыв к пониманию первых поколений мусульман</text>'
        + moon(268, 292, 52, 'url(#aiText)') +
        '<text x="640" y="318" text-anchor="middle" font-size="112" font-weight="700" letter-spacing="-3" fill="url(#titanium)">Свет Сунны</text>'
        '<text x="600" y="392" text-anchor="middle" font-size="36" font-weight="600" fill="#86868b">Уроки. Поиск. Сира Пророка.</text>'
        '<text x="600" y="466" text-anchor="middle" font-size="26" font-weight="500" fill="#2997ff">Открыть сайт ›</text>')
    save('banner.svg', 1200, 600, 'Свет Сунны — призыв к пониманию первых поколений мусульман', defs, body)


# ───────────────────────── заголовки секций ─────────────────────────

def title(name, text, hint):
    defs = f'<linearGradient id="ai" x1="0" y1="0" x2="1" y2="0">{AI}</linearGradient>'
    body = (f'<text x="2" y="62" font-size="54" font-weight="700" letter-spacing="-1.2" fill="url(#ai)">{esc(text)}</text>'
            f'<text x="3" y="104" font-size="25" font-weight="500" fill="#8e8e93">{esc(hint)}</text>')
    save(f'titles/{name}.svg', 1200, 130, text, defs, body)


# ───────────────────────── строки-фичи ─────────────────────────

def row(name, color, glyph, heading, text, tag, mono_tag=True):
    top, bottom = ICONS[color]
    defs = (TILE + f'<linearGradient id="ic" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
            f'<stop offset="1" stop-color="{bottom}"/></linearGradient>')
    tag_w = int(len(tag) * 11.5 + 36)
    tag_x = 1128 - tag_w
    tag_font = f' font-family="{MONO}"' if mono_tag else ''
    body = (
        '<rect x="0.5" y="6.5" width="1199" height="119" rx="26" fill="url(#tile)" stroke="#ffffff" stroke-opacity="0.1"/>'
        '<rect x="22" y="24" width="84" height="84" rx="21.84" fill="url(#ic)"/>'
        '<rect x="22.5" y="24.5" width="83" height="83" rx="21.84" fill="none" stroke="#ffffff" stroke-opacity="0.18"/>'
        + glyph +
        f'<text x="128" y="61" font-size="30" font-weight="600" fill="#f5f5f7">{esc(heading)}</text>'
        f'<text x="128" y="99" font-size="21" font-weight="500" fill="#86868b">{esc(text)}</text>'
        f'<rect x="{tag_x}" y="48" width="{tag_w}" height="36" rx="18" fill="#ffffff" fill-opacity="0.08"/>'
        f'<text x="{tag_x + tag_w / 2}" y="72"{tag_font} font-size="19" font-weight="600" fill="#f5f5f7" text-anchor="middle">{esc(tag)}</text>'
        '<path d="M1160 53l12 13-12 13" fill="none" stroke="#636366" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')
    save(f'rows/{name}.svg', 1200, 132, f'{heading} — {text}', defs, body)


G_PLAY = '<path d="M51 44v44l38-22z" fill="#ffffff"/>'
G_SEARCH = ('<circle cx="62" cy="62" r="15" fill="none" stroke="#ffffff" stroke-width="6"/>'
            '<path d="M73 73l15 15" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>')
G_WAVE = ''.join(f'<rect x="{x}" y="{66 - h / 2}" width="8" height="{h}" rx="4" fill="#ffffff"/>'
                 for x, h in ((36, 16), (49, 34), (62, 50), (75, 30), (88, 14)))
G_CLOCK = ('<circle cx="64" cy="66" r="24" fill="none" stroke="#ffffff" stroke-width="6"/>'
           '<path d="M64 52v14l10 6" fill="none" stroke="#ffffff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
G_SLIDERS = ('<path d="M42 52h44M42 66h44M42 80h44" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/>'
             '<circle cx="76" cy="52" r="7" fill="#ffffff"/><circle cx="54" cy="66" r="7" fill="#ffffff"/><circle cx="72" cy="80" r="7" fill="#ffffff"/>')


# ───────────────────────── плитки-цифры ─────────────────────────

def stats(items):
    """items: [(число, подпись, цвет)] — три плитки в ряд."""
    n = len(items)
    gap = 20
    w = (1200 - gap * (n - 1)) / n
    defs = (TILE + f'<linearGradient id="ai" x1="0" y1="0" x2="1" y2="1">{AI}</linearGradient>'
            '<filter id="blur" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="50"/></filter>'
            + ''.join(f'<clipPath id="c{i}"><rect width="{w}" height="260" rx="32"/></clipPath>' for i in range(n)))
    body = ''
    for i, (value, label, _) in enumerate(items):
        x = i * (w + gap)
        body += (f'<g transform="translate({x:.1f} 0)"><g clip-path="url(#c{i})"><rect width="{w}" height="260" fill="url(#tile)"/>'
                 f'<circle cx="{w - 60:.0f}" cy="230" r="110" fill="url(#ai)" opacity="0.3" filter="url(#blur)"/></g>'
                 f'<rect x="0.5" y="0.5" width="{w - 1}" height="259" rx="31.5" fill="none" stroke="#ffffff" stroke-opacity="0.1"/>'
                 f'<text x="40" y="176" font-size="150" font-weight="700" letter-spacing="-5" fill="url(#ai)">{value}</text>'
                 f'<text x="42" y="226" font-size="24" font-weight="600" fill="#86868b">{esc(label)}</text></g>')
    save('stats.svg', 1200, 260, ', '.join(f'{v} {l}' for v, l, _ in items), defs, body)


# ───────────────────────── стек ─────────────────────────

def stack(groups):
    defs = TILE
    body = ''
    y = 0
    for heading, chips in groups:
        body += f'<text x="4" y="{y + 28}" font-size="22" font-weight="600" fill="#86868b">{esc(heading)}</text>'
        x = 0
        y += 48
        for chip in chips:
            w = int(len(chip) * 12.2 + 44)
            if x + w > 1200:
                x = 0
                y += 64
            body += (f'<rect x="{x + 0.5}" y="{y + 0.5}" width="{w - 1}" height="51" rx="25.5" fill="url(#tile)" '
                     f'stroke="#ffffff" stroke-opacity="0.12"/>'
                     f'<text x="{x + w / 2}" y="{y + 33}" font-size="21" font-weight="600" fill="#f5f5f7" text-anchor="middle">{esc(chip)}</text>')
            x += w + 14
        y += 76
    save('stack.svg', 1200, y - 12, 'Стек: ' + ', '.join(c for _, cs in groups for c in cs), defs, body)


# ───────────────────────── терминал ─────────────────────────

def terminal(name, label, title_text, lines):
    """lines: список строк-списков (текст, цвет); пустой список — пропуск строки."""
    h = 60 + 40 + len(lines) * 36 + 16
    defs = TILE
    body = (f'<rect x="0.5" y="0.5" width="1199" height="{h - 1}" rx="23.5" fill="url(#tile)" stroke="#ffffff" stroke-opacity="0.1"/>'
            '<rect x="1" y="1" width="1198" height="59" rx="23" fill="#ffffff" fill-opacity="0.04"/>'
            '<line x1="1" y1="60.5" x2="1199" y2="60.5" stroke="#ffffff" stroke-opacity="0.08"/>'
            '<circle cx="34" cy="30" r="7" fill="#ff5f57"/><circle cx="58" cy="30" r="7" fill="#febc2e"/><circle cx="82" cy="30" r="7" fill="#28c840"/>'
            f'<text x="600" y="36" font-family="{MONO}" font-size="16" fill="#8e8e93" text-anchor="middle">{esc(title_text)}</text>')
    for i, parts in enumerate(lines):
        if not parts:
            continue
        spans = ''.join(f'<tspan fill="{color}">{esc(text)}</tspan>' for text, color in parts)
        body += (f'<text x="48" y="{60 + 62 + i * 36}" font-family="{MONO}" font-size="20" '
                 f'xml:space="preserve" style="white-space:pre">{spans}</text>')
    save(f'{name}.svg', 1200, h, label, defs, body)


GRAY, GREEN, WHITE, BLUE, PINK, YELLOW = '#636366', '#30d158', '#f5f5f7', '#64d2ff', '#ff375f', '#ffd60a'


def cmd(text, comment=None):
    parts = [('$ ', GREEN), (text, WHITE)]
    return parts


# ───────────────────────── контакты ─────────────────────────

def contact(name, color, heading, value, glyph):
    top, bottom = ICONS[color]
    defs = (TILE + f'<linearGradient id="ic" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
            f'<stop offset="1" stop-color="{bottom}"/></linearGradient>')
    body = ('<rect x="0.5" y="0.5" width="387" height="119" rx="26" fill="url(#tile)" stroke="#ffffff" stroke-opacity="0.1"/>'
            '<rect x="22" y="22" width="76" height="76" rx="19" fill="url(#ic)"/>'
            '<rect x="22.5" y="22.5" width="75" height="75" rx="19" fill="none" stroke="#ffffff" stroke-opacity="0.18"/>'
            + glyph +
            f'<text x="116" y="54" font-size="21" font-weight="500" fill="#86868b">{esc(heading)}</text>'
            f'<text x="116" y="86" font-size="25" font-weight="600" fill="#f5f5f7">{esc(value)}</text>')
    save(f'contact/{name}.svg', 388, 120, f'{heading}: {value}', defs, body)


C_PLANE = '<path d="M36 62l48-20-10 40-14-10-8 8-2-14z" fill="#ffffff"/>'
C_PLAY = '<rect x="34" y="44" width="52" height="34" rx="10" fill="#ffffff"/><path d="M54 52v18l15-9z" fill="#d70015"/>'
C_CAM = ('<rect x="36" y="38" width="48" height="48" rx="14" fill="none" stroke="#ffffff" stroke-width="5"/>'
         '<circle cx="60" cy="62" r="11" fill="none" stroke="#ffffff" stroke-width="5"/><circle cx="74" cy="48" r="3.5" fill="#ffffff"/>')


# ───────────────────────── цитата ─────────────────────────

def quote():
    defs = f'<linearGradient id="ai" x1="0" y1="0" x2="1" y2="0">{AI}</linearGradient>'
    body = ('<g text-anchor="middle">'
            '<text x="600" y="64" font-size="40" font-weight="600" fill="#f5f5f7">«Пролить свет знания о пути Пророка</text>'
            '<text x="600" y="116" font-size="40" font-weight="600" fill="#f5f5f7">и его сподвижников»</text>'
            '<text x="600" y="160" font-size="22" font-weight="600" fill="#86868b">Цель проекта «Свет Сунны»</text></g>')
    save('quote.svg', 1200, 190, 'Цель проекта — пролить свет знания о пути Пророка и его сподвижников', defs, body)


# ───────────────────────── подвал ─────────────────────────

def footer():
    defs = (TITANIUM + f'<linearGradient id="ai" x1="0" y1="0" x2="1" y2="0">{AI}'
            '<animateTransform attributeName="gradientTransform" type="translate" values="-0.3 0;0.3 0;-0.3 0" dur="8s" repeatCount="indefinite"/>'
            '</linearGradient><radialGradient id="spot" cx="0.5" cy="1" r="0.7"><stop offset="0" stop-color="#bf5af2" stop-opacity="0.22"/>'
            '<stop offset="1" stop-color="#bf5af2" stop-opacity="0"/></radialGradient>'
            '<clipPath id="card"><rect width="1200" height="380" rx="32"/></clipPath>')
    body = ('<g clip-path="url(#card)"><rect width="1200" height="380" fill="#000000"/><rect width="1200" height="380" fill="url(#spot)"/></g>'
            '<rect x="0.5" y="0.5" width="1199" height="379" rx="31.5" fill="none" stroke="#ffffff" stroke-opacity="0.1"/>'
            '<g font-weight="700" text-anchor="middle">'
            '<text x="600" y="160" font-size="96" letter-spacing="-3" fill="url(#titanium)">Свет знания.</text>'
            '<text x="600" y="262" font-size="96" letter-spacing="-3" fill="url(#ai)">Путь сподвижников.</text>'
            '<text x="600" y="326" font-size="22" font-weight="600" fill="#86868b">Свет Сунны · ١٤٤٧</text></g>')
    save('footer.svg', 1200, 380, 'Свет знания. Путь сподвижников.', defs, body)


banner()
title('features', 'Возможности', 'Всё, что есть на сайте, — от ленты до автообновления.')
title('stack', 'Стек', 'Простой Django без лишнего — и деплой на Vercel.')
title('run', 'Запуск', 'Пять команд — и сайт открыт на localhost.')
title('structure', 'Структура', 'Где что лежит в репозитории.')
title('contact', 'Связаться', 'Идеи и поправки — в Telegram.')

row('feed', 'red', G_PLAY, 'Лента видео', 'Уроки с нескольких YouTube-каналов: вкладки по авторам и пагинация', 'YouTube', False)
row('search', 'blue', G_SEARCH, 'Умный поиск', 'Падежи, опечатки, ё/е, неверная раскладка: cthf → сира', 'search.py')
row('sira', 'violet', G_WAVE, 'Сира Пророка', 'Аудиолекции по частям и контрольные вопросы к каждой', '100 лекций', False)
row('cron', 'green', G_CLOCK, 'Автообновление', 'Раз в сутки Vercel Cron подтягивает новые видео из RSS', 'cron', False)
row('admin', 'orange', G_SLIDERS, 'Админка', 'Ручное управление карточками: порядок, видимость, поиск', '/admin')

lectures = sum(len(page['tracks']) for page in SIRA_PAGES)
tests = len(re.findall(r'^\s+def test_', open(os.path.join(ROOT, 'main', 'tests.py'), encoding='utf-8').read(), re.M))
stats([(lectures, 'аудиолекций по Сире', ''), (len(SIRA_PAGES), 'частей курса', ''), (tests, 'тестов', '')])

stack([
    ('Основной', ['Python', 'Django 5.1', 'SQLite', 'PostgreSQL']),
    ('Интеграции', ['YouTube RSS', 'YouTube Data API', 'feedparser', 'requests', 'DigitalOcean Spaces']),
    ('Деплой', ['Vercel', 'Vercel Cron', 'WhiteNoise', 'dj-database-url']),
])

terminal('run', 'Запуск сайта в терминале', 'zsh — svet__sunny', [
    [('# Установка', GRAY)],
    cmd('python -m venv .venv && source .venv/bin/activate'),
    cmd('pip install -r requirements.txt'),
    [],
    [('# База и админ', GRAY)],
    cmd('python manage.py migrate'),
    cmd('python manage.py createsuperuser'),
    [],
    [('# Подтянуть видео и запустить', GRAY)],
    cmd('python manage.py parse_youtube'),
    cmd('python manage.py runserver'),
    [('Starting development server at ', BLUE), ('http://127.0.0.1:8000/', BLUE)],
])

terminal('structure', 'Структура репозитория', 'tree — svet__sunny', [
    [('main/', BLUE), ('          лента, поиск, команды парсинга', GRAY)],
    [('  search.py', WHITE), ('    умный поиск по карточкам', GRAY)],
    [('  sira_data.py', WHITE), ('  треки и вопросы курса по Сире', GRAY)],
    [('  youtube.py', WHITE), ('    общие функции для YouTube API', GRAY)],
    [('content/', BLUE), ('       вспомогательное приложение', GRAY)],
    [('templates/', BLUE), ('     HTML-шаблоны', GRAY)],
    [('static/', BLUE), ('        CSS и изображения', GRAY)],
    [('vercel.json', WHITE), ('    деплой и расписание cron', GRAY)],
])

contact('telegram', 'blue', 'Telegram', '@svettsunny', C_PLANE)
contact('youtube', 'red', 'YouTube', '@abdurtwhd', C_PLAY)
contact('instagram', 'violet', 'Instagram', '@abdurtwhd', C_CAM)

quote()
footer()
