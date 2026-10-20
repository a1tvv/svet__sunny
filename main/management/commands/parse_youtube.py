import re

import feedparser
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from main.models import Card

FEED_URL = 'https://www.youtube.com/feeds/videos.xml?channel_id={}'


def clean_title(title):
    """Убирает эмодзи и лишние пробелы в начале заголовка."""
    title = re.sub(r'^[\U0001F300-\U0001FAFF\U00002600-\U000027BF\s]+', '', title)
    return title.strip()


class Command(BaseCommand):
    help = 'Парсит последние видео с нескольких YouTube-каналов через RSS'

    def handle(self, *args, **options):
        if not settings.YOUTUBE_CHANNEL_IDS:
            raise CommandError('YOUTUBE_CHANNEL_IDS не задан в settings')

        total_new = 0
        for channel_id in settings.YOUTUBE_CHANNEL_IDS:
            total_new += self._parse_channel(channel_id)

        self.stdout.write(self.style.SUCCESS(
            f'\nГотово. Всего новых видео: {total_new}. '
            f'Всего карточек в БД: {Card.objects.count()}'
        ))

    def _parse_channel(self, channel_id):
        rss_url = FEED_URL.format(channel_id)
        self.stdout.write(f'Загружаю RSS: {rss_url}')

        feed = feedparser.parse(rss_url)
        if not feed.entries:
            self.stdout.write(self.style.WARNING(
                f'  ⚠ Канал {channel_id}: RSS пустой или недоступен'
            ))
            return 0

        channel_name = getattr(feed.feed, 'title', channel_id)
        known_urls = set(
            Card.objects.filter(url__in=[entry.link for entry in feed.entries])
            .values_list('url', flat=True)
        )

        new_cards = [
            self._build_card(entry, channel_id, channel_name)
            for entry in feed.entries
            if entry.link not in known_urls
        ]
        Card.objects.bulk_create(new_cards)

        self.stdout.write(self.style.SUCCESS(f'  ✓ {channel_name}: +{len(new_cards)} новых'))
        return len(new_cards)

    @staticmethod
    def _build_card(entry, channel_id, channel_name):
        video_id = entry.id.split(':')[-1]

        if getattr(entry, 'media_thumbnail', None):
            thumbnail_url = entry.media_thumbnail[0]['url']
        else:
            thumbnail_url = f'https://i.ytimg.com/vi/{video_id}/hqdefault.jpg'

        published = parse_datetime(entry.published)

        return Card(
            title=clean_title(entry.title),
            description=f'Новое видео на канале «{channel_name}»',
            image_url=thumbnail_url,
            url=entry.link,
            card_type='youtube',
            order=0,
            is_active=True,
            published=published.date() if published else timezone.now().date(),
            channel_id=channel_id,
            channel_name=channel_name,
            video_id=video_id,
        )
