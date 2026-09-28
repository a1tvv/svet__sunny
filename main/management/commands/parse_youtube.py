import re
import feedparser
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.utils import timezone

from main.models import Card


def clean_title(title: str) -> str:
    """Убирает эмодзи и лишние пробелы в начале заголовка."""
    title = re.sub(r'^[\U0001F300-\U0001FAFF\U00002600-\U000027BF\s]+', '', title)
    return title.strip()


class Command(BaseCommand):
    help = 'Парсит последние видео с нескольких YouTube-каналов через RSS'

    def handle(self, *args, **options):
        channel_ids = getattr(settings, 'YOUTUBE_CHANNEL_IDS', [])

        if not channel_ids:
            self.stdout.write(self.style.ERROR(
                'YOUTUBE_CHANNEL_IDS не задан в settings'
            ))
            return

        total_new = 0

        for channel_id in channel_ids:
            rss_url = f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'
            self.stdout.write(f'Загружаю RSS: {rss_url}')

            feed = feedparser.parse(rss_url)

            if not feed.entries:
                self.stdout.write(self.style.WARNING(
                    f'  ⚠ Канал {channel_id}: RSS пустой или недоступен'
                ))
                continue

            channel_name = getattr(feed.feed, 'title', channel_id)

            new_for_channel = 0
            for entry in feed.entries:
                video_id = entry.id.split(':')[-1]
                url = entry.link

                if Card.objects.filter(url=url).exists():
                    continue

                if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                    thumbnail_url = entry.media_thumbnail[0]['url']
                else:
                    thumbnail_url = f'https://i.ytimg.com/vi/{video_id}/hqdefault.jpg'

                published_dt = parse_datetime(entry.published)
                published_date = published_dt.date() if published_dt else timezone.now().date()

                Card.objects.create(
                    title=clean_title(entry.title),
                    description=f'Новое видео на канале «{channel_name}»',
                    image_url=thumbnail_url,
                    url=url,
                    card_type='youtube',
                    order=0,
                    is_active=True,
                    published=published_date,
                )
                new_for_channel += 1

            self.stdout.write(self.style.SUCCESS(
                f'  ✓ {channel_name}: +{new_for_channel} новых'
            ))
            total_new += new_for_channel

        self.stdout.write(self.style.SUCCESS(
            f'\nГотово. Всего новых видео: {total_new}. '
            f'Всего карточек в БД: {Card.objects.count()}'
        ))