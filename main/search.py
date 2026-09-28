"""
main/search.py — умный поиск по карточкам «Свет Сунны».

Что умеет:
  • регистр, ё/е, й/и, ъ/ь, апострофы (Исма’иль = Исмаиль), удвоенные буквы (Мухаммад = Мухамад)
  • лишние / пропущенные пробелы («сирапророка», «си ра пророка»)
  • опечатки и перестановки букв («прорка», «тфасир»)
  • окончания и падежи («пророка» находит «пророк», «пророку», «пророков»)
  • неполные слова («мухам» находит «Мухаммад»)
  • не та раскладка («cthf ghjhjrf» → «сира пророка») и латиница («sira» → «сира»)
  • сортировка по релевантности, при равенстве — новые выше
  • если не нашлось по всем словам — показывает то, что совпало хотя бы частично

Работает одинаково на SQLite и PostgreSQL, потому что вся логика в Python
(в SQLite icontains вообще не понимает регистр кириллицы).
"""
import re
import time
import unicodedata

from django.db.models import Count, Max

CACHE_TTL = 600          # сек. Индекс пересобирается раз в 10 минут или при появлении новых карточек
DESC_LIMIT = 600         # сколько символов описания индексируем
MAX_QUERY_TOKENS = 8

# ───────────────────────── нормализация ─────────────────────────

_KZ = str.maketrans({
    'ә': 'а', 'ғ': 'г', 'қ': 'к', 'ң': 'н', 'ө': 'о',
    'ұ': 'у', 'ү': 'у', 'һ': 'х', 'і': 'и', 'ъ': '', 'ь': '',
})
_APOSTROPHES = re.compile(r"[’'`ʼʻʾʿ‘´]")
_NON_WORD = re.compile(r'[\W_]+')
_DOUBLE = re.compile(r'([^\W\d_])\1+')

STOP = {'про', 'как', 'что', 'это', 'для', 'или', 'при', 'над', 'под', 'все', 'его', 'ее', 'их'}


def normalize(text):
    """Приводит текст к виду, в котором сравнивать безопасно."""
    if not text:
        return ''
    text = unicodedata.normalize('NFKD', str(text).casefold())
    text = ''.join(c for c in text if not unicodedata.combining(c))  # й→и, ё→е
    text = text.translate(_KZ)
    text = _APOSTROPHES.sub('', text)
    text = _NON_WORD.sub(' ', text)
    text = _DOUBLE.sub(r'\1', text)
    return re.sub(r'\s+', ' ', text).strip()


_ENDINGS = sorted([
    'ами', 'ями', 'ого', 'его', 'ому', 'ему', 'ыми', 'ими', 'ать', 'ять', 'ить', 'еть',
    'ах', 'ях', 'ов', 'ев', 'ом', 'ем', 'ам', 'ям', 'ая', 'яя', 'ое', 'ее', 'ые', 'ие',
    'ои', 'еи', 'ыи', 'ую', 'юю', 'ою', 'ею', 'а', 'я', 'у', 'ю', 'ы', 'и', 'е', 'о',
], key=len, reverse=True)


def stem(word):
    """Грубое отрезание окончания. Для поиска этого достаточно."""
    if len(word) < 5:
        return word
    for end in _ENDINGS:
        if word.endswith(end) and len(word) - len(end) >= 3:
            return word[:-len(end)]
    return word


# ───────────────────────── раскладки / транслит ─────────────────────────

_EN = "qwertyuiop[]asdfghjkl;'zxcvbnm,./"
_RU = "йцукенгшщзхъфывапролджэячсмитьбю."
_EN2RU = str.maketrans(_EN, _RU)
_RU2EN = str.maketrans(_RU, _EN)

_TRANSLIT = [
    ('sch', 'щ'), ('sh', 'ш'), ('ch', 'ч'), ('zh', 'ж'), ('kh', 'х'), ('ts', 'ц'),
    ('yu', 'ю'), ('ya', 'я'), ('yo', 'е'), ('ye', 'е'),
    ('a', 'а'), ('b', 'б'), ('v', 'в'), ('w', 'в'), ('g', 'г'), ('d', 'д'), ('e', 'е'),
    ('z', 'з'), ('i', 'и'), ('y', 'и'), ('j', 'дж'), ('k', 'к'), ('q', 'к'), ('l', 'л'),
    ('m', 'м'), ('n', 'н'), ('o', 'о'), ('p', 'п'), ('r', 'р'), ('s', 'с'), ('t', 'т'),
    ('u', 'у'), ('f', 'ф'), ('h', 'х'), ('c', 'к'), ('x', 'кс'),
]
_TRANSLIT_MAP = dict(_TRANSLIT)
_TRANSLIT_RE = re.compile('|'.join(k for k, _ in _TRANSLIT))

_HAS_LAT = re.compile(r'[a-z]')
_HAS_CYR = re.compile(r'[а-яё]')


def _query_variants(raw):
    """Запрос как есть + запасные варианты на случай неверной раскладки/латиницы."""
    low = str(raw).casefold()
    variants = [normalize(low)]
    if _HAS_LAT.search(low) and not _HAS_CYR.search(low):
        variants.append(normalize(low.translate(_EN2RU)))                        # ghbdtn → привет
        variants.append(normalize(_TRANSLIT_RE.sub(lambda m: _TRANSLIT_MAP[m.group(0)], low)))  # sira → сира
    elif _HAS_CYR.search(low) and not _HAS_LAT.search(low):
        variants.append(normalize(low.translate(_RU2EN)))
    seen, result = set(), []
    for v in variants:
        if v and v not in seen:
            seen.add(v)
            result.append(v)
    return result


# ───────────────────────── сравнение слов ─────────────────────────

def _edit_distance(a, b, limit):
    """Расстояние Дамерау–Левенштейна с ранним выходом. Перестановка соседних букв = 1."""
    la, lb = len(a), len(b)
    if abs(la - lb) > limit:
        return limit + 1
    prev2 = None
    prev = list(range(lb + 1))
    for i in range(1, la + 1):
        cur = [i] + [0] * lb
        ca = a[i - 1]
        row_min = i
        for j in range(1, lb + 1):
            cost = 0 if ca == b[j - 1] else 1
            v = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
            if i > 1 and j > 1 and ca == b[j - 2] and a[i - 2] == b[j - 1]:
                v = min(v, prev2[j - 2] + 1)
            cur[j] = v
            if v < row_min:
                row_min = v
        if row_min > limit:
            return limit + 1
        prev2, prev = prev, cur
    return prev[lb]


def token_match(q, sq, t, fuzzy):
    """Насколько слово запроса q (основа sq) похоже на слово из карточки t. 0..1"""
    if q == t:
        return 1.0
    lq = len(q)
    if lq >= 2 and t.startswith(q):
        return 0.92
    st = stem(t)
    if sq == st:
        return 0.88
    if len(sq) >= 3 and st.startswith(sq):
        return 0.8
    if lq >= 4 and q in t:
        return 0.62
    if fuzzy:
        allowed = 0 if len(sq) <= 3 else (1 if len(sq) <= 6 else 2)
        if allowed:
            d = _edit_distance(sq, st, allowed)
            if d <= allowed:
                return 0.75 - 0.12 * d
            if lq >= 5 and len(t) >= lq:      # человек не дописал слово и ошибся
                d = _edit_distance(q, t[:lq], allowed)
                if d <= allowed:
                    return 0.6 - 0.1 * d
    return 0.0


# ───────────────────────── индекс ─────────────────────────

class _Index:
    __slots__ = ('key', 'built', 'docs', 'title_vocab', 'desc_vocab', 'maps')


def _build_index(rows, key=None):
    """rows: (id, channel_id, title, description, channel_name, published) — уже отсортированы по дате ↓"""
    idx = _Index()
    idx.key, idx.built, idx.maps = key, time.time(), {}
    idx.docs, idx.title_vocab, idx.desc_vocab = [], set(), set()
    for cid, channel_id, title, desc, channel_name, _published in rows:
        tnorm = normalize(title)
        ttoks = frozenset(tnorm.split())
        dnorm = normalize(f"{(desc or '')[:DESC_LIMIT]} {channel_name or ''}")
        dtoks = frozenset(t for t in dnorm.split() if 2 <= len(t) <= 25)
        idx.title_vocab |= ttoks
        idx.desc_vocab |= dtoks
        idx.docs.append((cid, channel_id, ttoks, tnorm, tnorm.replace(' ', ''), dtoks))
    return idx


def _match_map(idx, q):
    cached = idx.maps.get(q)
    if cached:
        return cached
    sq = stem(q)
    tm = {t: s for t in idx.title_vocab if (s := token_match(q, sq, t, True))}
    dm = {t: s for t in idx.desc_vocab if (s := token_match(q, sq, t, False))}
    if len(idx.maps) > 500:
        idx.maps.clear()
    idx.maps[q] = (tm, dm)
    return tm, dm


def _run(idx, qnorm, channel=''):
    tokens = [t for t in qnorm.split() if t not in STOP and (len(t) >= 2 or t.isdigit())]
    if not tokens:
        tokens = qnorm.split()
    tokens = tokens[:MAX_QUERY_TOKENS]
    if not tokens:
        return []

    maps = [_match_map(idx, t) for t in tokens]
    qcompact = qnorm.replace(' ', '')
    n = len(tokens)
    need = n - n // 3        # 1→1, 2→2, 3→2, 4→3, 5→4 ...

    strict, relaxed = [], []
    for cid, channel_id, ttoks, tnorm, tcompact, dtoks in idx.docs:
        if channel and channel_id != channel:
            continue
        total, matched = 0.0, 0
        for tm, dm in maps:
            best = 0.0
            for t in ttoks:
                s = tm.get(t)
                if s and s > best:
                    best = s
            if dm and best < 0.9:
                for t in dtoks:
                    s = dm.get(t)
                    if s and s * 0.55 > best:
                        best = s * 0.55
            total += best
            if best >= 0.5:
                matched += 1

        bonus = 0.0
        if len(qcompact) >= 3 and qcompact in tcompact:
            bonus += 0.4                 # склеенный/разлепленный запрос
        if qnorm in tnorm:
            bonus += 0.3                 # фраза целиком, подряд
        if matched == 0 and bonus == 0:
            continue

        score = total / n + bonus
        (strict if (matched >= need or bonus > 0) else relaxed).append((score, cid))

    found = strict or relaxed
    found.sort(key=lambda r: -r[0])      # sort стабильный → при равенстве остаётся порядок «новые выше»
    return [cid for _, cid in found]


_INDEX = None


def _get_index():
    global _INDEX
    from main.models import Card

    qs = Card.objects.filter(card_type='youtube', is_active=True)
    stamp = qs.aggregate(n=Count('id'), m=Max('id'))
    key = (stamp['n'], stamp['m'])
    if _INDEX and _INDEX.key == key and time.time() - _INDEX.built < CACHE_TTL:
        return _INDEX
    rows = qs.order_by('-published', '-id').values_list(
        'id', 'channel_id', 'title', 'description', 'channel_name', 'published'
    )
    _INDEX = _build_index(rows, key)
    return _INDEX


def smart_search(query, channel=''):
    """
    Возвращает (список id карточек по релевантности, фактический запрос).
    Фактический запрос отличается от введённого, если пришлось исправить раскладку/транслит.
    """
    idx = _get_index()
    for variant in _query_variants(query):
        ids = _run(idx, variant, channel)
        if ids:
            return ids, variant
    return [], query
