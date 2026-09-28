import re
import time
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.utils import timezone

from main.models import Card


API_BASE = 'https://www.googleapis.com/youtube/v3'


def _format_duration(iso_duration: str) -> str:
    """
    ISO 8601 → "H:MM:SS" или "M:SS".
    Пример: PT53M56S → "53:56", PT1H20M15S → "1:20:15"
    """
    if not iso_duration:
        return ''
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso_duration)
    if not m:
        return ''
    h = int(m.group(1) or 0)
    mi = int(m.group(2) or 0)
    s = int(m.group(3) or 0)
    if h:
        return f'{h}:{mi:02d}:{s:02d}'
    return f'{mi}:{s:02d}'


class Command(BaseCommand):
    help = 'Полный парсинг всех видео каналов через YouTube Data API v3'

    def add_arguments(self, parser):
        parser.add_argument('--channel', type=str, default=None)

    def handle(self, *args, **options):
        if not settings.YOUTUBE_API_KEY:
            self.stdout.write(self.style.ERROR('YOUTUBE_API_KEY не задан в .env'))
            return

        channel_ids = (
            [options['channel']]
            if options['channel']
            else getattr(settings, 'YOUTUBE_CHANNEL_IDS', [])
        )
        if not channel_ids:
            self.stdout.write(self.style.ERROR('YOUTUBE_CHANNEL_IDS пуст'))
            return

        total_new = 0
        for ch_id in channel_ids:
            self.stdout.write(f'\n=== Канал {ch_id} ===')
            total_new += self._parse_channel(ch_id)

        self.stdout.write(self.style.SUCCESS(
            f'\nГотово. Новых карточек: {total_new}. '
            f'Всего в БД: {Card.objects.filter(card_type="youtube").count()}'
        ))

    def _api_get(self, endpoint, **params):
        params['key'] = settings.YOUTUBE_API_KEY
        r = requests.get(f'{API_BASE}/{endpoint}', params=params, timeout=30)
        if r.status_code != 200:
            raise RuntimeError(f'{endpoint} → {r.status_code}: {r.text[:300]}')
        return r.json()

    def _parse_channel(self, channel_id):
        data = self._api_get('channels', part='snippet,contentDetails', id=channel_id)
        if not data.get('items'):
            self.stdout.write(self.style.WARNING(f'  ⚠ Канал {channel_id} не найден'))
            return 0

        ch = data['items'][0]
        ch_title = ch['snippet']['title']
        uploads_playlist = ch['contentDetails']['relatedPlaylists']['uploads']
        self.stdout.write(f'  Название: {ch_title}')

        video_ids = []
        page_token = None
        page = 0
        while True:
            page += 1
            params = {
                'part': 'contentDetails',
                'playlistId': uploads_playlist,
                'maxResults': 50,
            }
            if page_token:
                params['pageToken'] = page_token
            data = self._api_get('playlistItems', **params)
            for item in data.get('items', []):
                vid = item['contentDetails'].get('videoId')
                if vid:
                    video_ids.append(vid)
            self.stdout.write(f'    стр. {page}: всего ID = {len(video_ids)}')
            page_token = data.get('nextPageToken')
            if not page_token:
                break

        existing = set(
            Card.objects.filter(channel_id=channel_id)
            .values_list('video_id', flat=True)
        )

        new_cards = []
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i:i + 50]
            data = self._api_get(
                'videos',
                part='snippet,contentDetails',   # ← добавили contentDetails
                id=','.join(batch),
                maxResults=50,
            )
            for v in data.get('items', []):
                vid = v['id']
                if vid in existing:
                    continue
                snippet = v['snippet']
                content = v.get('contentDetails', {})

                published = parse_datetime(snippet['publishedAt'])
                published_date = published.date() if published else timezone.now().date()

                thumb = (
                    snippet.get('thumbnails', {}).get('high', {}).get('url')
                    or snippet.get('thumbnails', {}).get('medium', {}).get('url')
                    or snippet.get('thumbnails', {}).get('default', {}).get('url')
                    or f'https://i.ytimg.com/vi/{vid}/hqdefault.jpg'
                )

                new_cards.append(Card(
                    title=snippet['title'][:500],
                    description=(snippet.get('description') or '')[:1000],
                    image_url=thumb,
                    url=f'https://www.youtube.com/watch?v={vid}',
                    card_type='youtube',
                    order=0,
                    is_active=True,
                    published=published_date,
                    channel_id=channel_id,
                    channel_name=ch_title,
                    video_id=vid,
                    duration=_format_duration(content.get('duration', '')),
                ))
            self.stdout.write(f'    videos.list {i // 50 + 1}: +{len(new_cards)} новых')
            time.sleep(0.05)

        if new_cards:
            Card.objects.bulk_create(new_cards, batch_size=500)

        self.stdout.write(self.style.SUCCESS(f'  ✓ {ch_title}: +{len(new_cards)}'))
        return len(new_cards)