import secrets
from urllib.parse import urlencode

from django.conf import settings
from django.core.management import call_command
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render

from main.models import Card
from main.search import smart_search
from main.sira_data import SIRA_PAGES

CARDS_PER_PAGE = 50
PARAM_MAX_LEN = 200


def _get_param(request, name):
    return request.GET.get(name, '').strip()[:PARAM_MAX_LEN]


def _search_page(query, channel, page_number):
    """Страница результатов умного поиска: id приходят по релевантности, карточки подгружаем одним запросом."""
    ids, query_used = smart_search(query, channel)
    page_obj = Paginator(ids, CARDS_PER_PAGE).get_page(page_number)
    cards_by_id = Card.objects.in_bulk(page_obj.object_list)
    page_obj.object_list = [cards_by_id[card_id] for card_id in page_obj.object_list if card_id in cards_by_id]
    return page_obj, query_used


def index(request):
    query = _get_param(request, 'q')
    channel = _get_param(request, 'channel')
    page_number = request.GET.get('page')

    youtube_cards = Card.objects.filter(card_type='youtube', is_active=True)

    # Один запрос даёт и вкладки авторов, и общее число, и число карточек для пагинации
    channel_counts = list(
        youtube_cards.values('channel_id', 'channel_name')
        .annotate(n=Count('id'))
        .order_by('-n')
    )
    total_count = sum(row['n'] for row in channel_counts)

    if query:
        page_obj, query_used = _search_page(query, channel, page_number)
    else:
        query_used = query
        cards = youtube_cards.filter(channel_id=channel) if channel else youtube_cards
        paginator = Paginator(cards.order_by('-published', '-id'), CARDS_PER_PAGE)
        paginator.count = (  # count — cached_property, задаём заранее вместо отдельного COUNT(*)
            sum(row['n'] for row in channel_counts if row['channel_id'] == channel) if channel else total_count
        )
        page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {
        'page_obj': page_obj,
        'q': query,
        'q_used': query_used,
        'selected_channel': channel,
        'channels': [row for row in channel_counts if row['channel_name']],
        'total_count': total_count,
        # query-string без номера страницы, уже экранированный — для ссылок пагинации
        'page_query': urlencode({k: v for k, v in (('q', query), ('channel', channel)) if v}),
        'search_query': urlencode({'q': query}) if query else '',
    })


def admin_info(request):
    admin_data = {
        'name': 'Группа разработчиков проекта «Свет Сунны»',
        'email': 'alraiabdurahim07@gmail.com',
        'telegram': 'https://t.me/dusi84',
        'youtube': 'https://youtube.com/@abdurtwhd',
        'about': 'По всем вопросам пишите в Telegram. '
                 'Проект не нуждается в финансировании, достаточно просто поделиться ссылкой с близкими.',
    }
    return render(request, 'admin_info.html', {'admin': admin_data})


def latest_video(request):
    card = Card.objects.filter(card_type='youtube').order_by('-id').first()
    if not card:
        return JsonResponse({'id': None})
    return JsonResponse({
        'id': card.url,
        'title': card.title,
        'url': card.url,
        'image': card.get_image(),
    })


def riyad_useimin(request):
    return render(request, 'riyad_useimin.html')


def tafsir(request):
    return render(request, 'tafsir.html')


def cron_parse_youtube(request):
    """Вызывается Vercel Cron, который сам шлёт `Authorization: Bearer <CRON_SECRET>`."""
    expected = f'Bearer {settings.CRON_SECRET}'.encode()
    given = request.headers.get('Authorization', '').encode()
    if not settings.CRON_SECRET or not secrets.compare_digest(given, expected):
        return JsonResponse({'error': 'forbidden'}, status=403)

    try:
        call_command('parse_youtube')
    except Exception as error:
        return JsonResponse({'status': 'error', 'message': str(error)[:300]}, status=500)
    return JsonResponse({'status': 'ok'})


def sira(request):
    paginator = Paginator(SIRA_PAGES, 1)  # одна часть курса на страницу
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'sira.html', {
        'page_obj': page_obj,
        'data': page_obj[0],
        'elided_pages': paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=2),
    })
