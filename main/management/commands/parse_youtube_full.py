import time

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from main.models import Card
from main.youtube import api_get, chunks, format_duration


class Command(BaseCommand):
    help = 'Полный парсинг всех видео каналов через YouTube Data API v3'

    def add_arguments(self, parser):
        parser.add_argument('--channel', type=str, default=None)

    def handle(self, *args, **options):
        if not settings.YOUTUBE_API_KEY:
            raise CommandError('YOUTUBE_API_KEY не задан в .env')

        channel_ids = [options['channel']] if options['channel'] else settings.YOUTUBE_CHANNEL_IDS
        if not channel_ids:
            raise CommandError('YOUTUBE_CHANNEL_IDS пуст')

        total_new = 0
        for channel_id in channel_ids:
            self.stdout.write(f'\n=== Канал {channel_id} ===')
            total_new += self._parse_channel(channel_id)

        self.stdout.write(self.style.SUCCESS(
            f'\nГотово. Новых карточек: {total_new}. '
            f'Всего в БД: {Card.objects.filter(card_type="youtube").count()}'
        ))

    def _parse_channel(self, channel_id):
        data = api_get('channels', part='snippet,contentDetails', id=channel_id)
        if not data.get('items'):
            self.stdout.write(self.style.WARNING(f'  ⚠ Канал {channel_id} не найден'))
            return 0

        channel = data['items'][0]
        channel_name = channel['snippet']['title']
        uploads_playlist = channel['contentDetails']['relatedPlaylists']['uploads']
        self.stdout.write(f'  Название: {channel_name}')

        video_ids = self._uploaded_video_ids(uploads_playlist)
        known = set(
            Card.objects.filter(channel_id=channel_id).values_list('video_id', flat=True)
        )

        new_cards = []
        for batch in chunks(video_ids):
            data = api_get('videos', part='snippet,contentDetails', id=','.join(batch))
            for video in data.get('items', []):
                if video['id'] not in known:
                    new_cards.append(self._build_card(video, channel_id, channel_name))
            self.stdout.write(f'    videos.list: новых {len(new_cards)}')
            time.sleep(0.05)

        Card.objects.bulk_create(new_cards, batch_size=500)
        self.stdout.write(self.style.SUCCESS(f'  ✓ {channel_name}: +{len(new_cards)}'))
        return len(new_cards)

    def _uploaded_video_ids(self, playlist_id):
        video_ids = []
        page_token = None
        while True:
            params = {'part': 'contentDetails', 'playlistId': playlist_id, 'maxResults': 50}
            if page_token:
                params['pageToken'] = page_token
            data = api_get('playlistItems', **params)

            for item in data.get('items', []):
                video_id = item['contentDetails'].get('videoId')
                if video_id:
                    video_ids.append(video_id)
            self.stdout.write(f'    собрано ID: {len(video_ids)}')

            page_token = data.get('nextPageToken')
            if not page_token:
                return video_ids

    @staticmethod
    def _build_card(video, channel_id, channel_name):
        snippet = video['snippet']
        video_id = video['id']

        published = parse_datetime(snippet['publishedAt'])
        thumbnails = snippet.get('thumbnails', {})
        thumbnail = next(
            (thumbnails[size]['url'] for size in ('high', 'medium', 'default') if size in thumbnails),
            f'https://i.ytimg.com/vi/{video_id}/hqdefault.jpg',
        )

        return Card(
            title=snippet['title'][:300],
            description=(snippet.get('description') or '')[:1000],
            image_url=thumbnail,
            url=f'https://www.youtube.com/watch?v={video_id}',
            card_type='youtube',
            order=0,
            is_active=True,
            published=published.date() if published else timezone.now().date(),
            channel_id=channel_id,
            channel_name=channel_name,
            video_id=video_id,
            duration=format_duration(video.get('contentDetails', {}).get('duration')),
        )
