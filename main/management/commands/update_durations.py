import time

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from main.models import Card
from main.youtube import api_get, chunks, format_duration


class Command(BaseCommand):
    help = 'Обновляет duration у существующих youtube-карточек'

    def handle(self, *args, **options):
        if not settings.YOUTUBE_API_KEY:
            raise CommandError('YOUTUBE_API_KEY не задан в .env')

        video_ids = list(
            Card.objects.filter(card_type='youtube', duration='')
            .exclude(video_id='')
            .values_list('video_id', flat=True)
        )
        self.stdout.write(f'К обновлению: {len(video_ids)}')

        updated = 0
        done = 0
        for batch in chunks(video_ids):
            try:
                data = api_get('videos', part='contentDetails', id=','.join(batch))
            except RuntimeError as error:
                self.stderr.write(self.style.ERROR(str(error)))
                continue

            for item in data.get('items', []):
                duration = format_duration(item.get('contentDetails', {}).get('duration'))
                if duration:
                    Card.objects.filter(video_id=item['id']).update(duration=duration)
                    updated += 1

            done += len(batch)
            self.stdout.write(f'  {done}/{len(video_ids)} (обновлено: {updated})')
            time.sleep(0.05)

        self.stdout.write(self.style.SUCCESS(f'Готово. Обновлено: {updated}'))
