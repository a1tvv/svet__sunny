import time
import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from main.models import Card


API_BASE = 'https://www.googleapis.com/youtube/v3'


def _format_duration(iso_duration: str) -> str:
    import re
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
    help = 'Обновляет duration у существующих youtube-карточек'

    def handle(self, *args, **options):
        cards = Card.objects.filter(card_type='youtube', duration='')
        total = cards.count()
        self.stdout.write(f'К обновлению: {total}')

        # Собираем id пачками по 50
        ids = list(cards.values_list('video_id', flat=True))
        updated = 0

        for i in range(0, len(ids), 50):
            batch = ids[i:i + 50]
            r = requests.get(
                f'{API_BASE}/videos',
                params={
                    'part': 'contentDetails',
                    'id': ','.join(batch),
                    'maxResults': 50,
                    'key': settings.YOUTUBE_API_KEY,
                },
                timeout=30,
            )
            if r.status_code != 200:
                self.stdout.write(self.style.ERROR(f'API error: {r.text[:200]}'))
                continue

            data = r.json()
            for item in data.get('items', []):
                vid = item['id']
                dur = _format_duration(item.get('contentDetails', {}).get('duration', ''))
                if dur:
                    Card.objects.filter(video_id=vid).update(duration=dur)
                    updated += 1

            self.stdout.write(f'  {i + len(batch)}/{len(ids)} (обновлено: {updated})')
            time.sleep(0.05)

        self.stdout.write(self.style.SUCCESS(f'Готово. Обновлено: {updated}'))