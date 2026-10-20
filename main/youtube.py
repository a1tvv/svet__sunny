import re

import requests
from django.conf import settings

API_BASE = 'https://www.googleapis.com/youtube/v3'
BATCH_SIZE = 50  # столько id за раз принимает videos.list

_DURATION_RE = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')


def format_duration(iso_duration):
    """ISO 8601 → «H:MM:SS» или «M:SS». PT53M56S → «53:56», PT1H20M15S → «1:20:15»."""
    match = _DURATION_RE.match(iso_duration or '')
    if not match:
        return ''
    hours, minutes, seconds = (int(part or 0) for part in match.groups())
    if hours:
        return f'{hours}:{minutes:02d}:{seconds:02d}'
    return f'{minutes}:{seconds:02d}'


def api_get(endpoint, **params):
    """GET-запрос к YouTube Data API. При ошибке бросает RuntimeError."""
    params['key'] = settings.YOUTUBE_API_KEY
    response = requests.get(f'{API_BASE}/{endpoint}', params=params, timeout=30)
    if response.status_code != 200:
        raise RuntimeError(f'{endpoint} → {response.status_code}: {response.text[:300]}')
    return response.json()


def chunks(items, size=BATCH_SIZE):
    for start in range(0, len(items), size):
        yield items[start:start + size]
