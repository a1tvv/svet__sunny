from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.dateparse import parse_datetime

from .models import RiyadhAsSalihin, FeaturedVideo
from .youtube import fetch_latest_video


def check_new_video(request):
    """
    Дергается по расписанию (Vercel Cron). Проверяет RSS-фид канала
    и, если появилось новое видео, сохраняет его в базу.
    Защищён секретом: Vercel сам шлёт заголовок
    Authorization: Bearer <CRON_SECRET>, если в проекте задана
    переменная окружения CRON_SECRET.
    """
    auth_header = request.headers.get('Authorization', '')
    if not settings.CRON_SECRET or auth_header != f'Bearer {settings.CRON_SECRET}':
        return JsonResponse({'error': 'unauthorized'}, status=401)

    data = fetch_latest_video(settings.YOUTUBE_CHANNEL_ID)
    if not data:
        return JsonResponse({'status': 'no_data'}, status=200)

    published_at = parse_datetime(data['published_at'])

    obj, created = FeaturedVideo.objects.get_or_create(
        video_id=data['video_id'],
        defaults={
            'title': data['title'],
            'url': data['url'],
            'published_at': published_at,
        },
    )

    return JsonResponse({
        'status': 'created' if created else 'already_known',
        'video_id': obj.video_id,
        'title': obj.title,
    })

def index(request):
    sheikh = {
        'links': {
            'rinat': 'https://t.me/toislam',
            'abu_yahya': 'https://t.me/abuyahya_net',
            'siraj': 'https://t.me/sirajabutalha',
        }
    }
    return render(request, 'index.html', sheikh)

def tafsir(request):
    return render(request,  'tafsir.html')


def riyad_useimin(request):
    lessons_list = RiyadhAsSalihin.objects.all()
    paginator = Paginator(lessons_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    elided_pages = paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=2)

    return render(request, 'riyad_useimin.html', {
        'page_obj': page_obj,
        'lessons': page_obj.object_list, # Теперь в цикле можно писать {% for lesson in lessons %}
        'elided_pages': elided_pages
    })