from datetime import date
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from main import search
from main.models import Card
from main.sira_data import SIRA_PAGES
from main.youtube import format_duration


class FormatDurationTests(SimpleTestCase):
    def test_minutes_and_seconds(self):
        self.assertEqual(format_duration('PT53M56S'), '53:56')

    def test_hours_are_zero_padded(self):
        self.assertEqual(format_duration('PT1H20M15S'), '1:20:15')
        self.assertEqual(format_duration('PT2H'), '2:00:00')

    def test_only_seconds(self):
        self.assertEqual(format_duration('PT45S'), '0:45')

    def test_empty_or_garbage(self):
        self.assertEqual(format_duration(''), '')
        self.assertEqual(format_duration(None), '')
        self.assertEqual(format_duration('abc'), '')


class NormalizeTests(SimpleTestCase):
    def test_case_yo_and_apostrophes(self):
        self.assertEqual(search.normalize('Исма’иль'), search.normalize('исмаиль'))
        self.assertEqual(search.normalize('Ёж'), search.normalize('еж'))

    def test_double_letters(self):
        self.assertEqual(search.normalize('Мухаммад'), search.normalize('Мухамад'))

    def test_empty(self):
        self.assertEqual(search.normalize(None), '')
        self.assertEqual(search.normalize('  '), '')

    def test_layout_and_translit_variants(self):
        self.assertIn('сира', search._query_variants('sira'))
        self.assertIn('привет', search._query_variants('ghbdtn'))


def make_card(title, **kwargs):
    defaults = {
        'url': f'https://www.youtube.com/watch?v={abs(hash(title))}',
        'card_type': 'youtube',
        'channel_id': 'chan1',
        'channel_name': 'Канал',
        'published': date(2026, 1, 1),
    }
    return Card.objects.create(title=title, **{**defaults, **kwargs})


class SmartSearchTests(TestCase):
    def setUp(self):
        search._INDEX = None
        self.sira = make_card('Сира Пророка Мухаммада')
        self.tafsir = make_card('Тафсир суры аль-Фатиха', channel_id='chan2')

    def test_finds_by_stem_and_typo(self):
        for query in ('пророк', 'пророку', 'прорка'):
            ids, _ = search.smart_search(query)
            self.assertEqual(ids, [self.sira.id], query)

    def test_wrong_keyboard_layout(self):
        ids, used = search.smart_search('cbhf')  # «сира»
        self.assertEqual(ids, [self.sira.id])
        self.assertEqual(used, 'сира')

    def test_channel_filter(self):
        ids, _ = search.smart_search('тафсир', channel='chan1')
        self.assertEqual(ids, [])

    def test_inactive_cards_are_hidden(self):
        make_card('Скрытое видео про сиру', is_active=False)
        search._INDEX = None
        ids, _ = search.smart_search('скрытое')
        self.assertEqual(ids, [])


class IndexViewTests(TestCase):
    def setUp(self):
        search._INDEX = None
        for number in range(3):
            make_card(f'Урок {number}', published=date(2026, 1, number + 1))

    def test_lists_cards_newest_first(self):
        response = self.client.get(reverse('index'))
        titles = [card.title for card in response.context['page_obj']]
        self.assertEqual(titles, ['Урок 2', 'Урок 1', 'Урок 0'])
        self.assertEqual(response.context['total_count'], 3)

    def test_search(self):
        response = self.client.get(reverse('index'), {'q': 'урок 1'})
        self.assertEqual([c.title for c in response.context['page_obj']][0], 'Урок 1')

    def test_pagination_links_keep_query_escaped(self):
        with patch('main.views.CARDS_PER_PAGE', 1):
            response = self.client.get(reverse('index'), {'q': 'урок & тест'})
        self.assertEqual(response.context['page_query'], 'q=%D1%83%D1%80%D0%BE%D0%BA+%26+%D1%82%D0%B5%D1%81%D1%82')

    def test_bad_page_number_falls_back_to_first(self):
        response = self.client.get(reverse('index'), {'page': 'abc'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].number, 1)


class StaticPagesTests(TestCase):
    def test_simple_pages_open(self):
        for name in ('riyad_useimin', 'tafsir', 'admin_info'):
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)

    def test_sira_pages(self):
        ids = [page['id'] for page in SIRA_PAGES]
        self.assertEqual(len(ids), len(set(ids)))
        response = self.client.get(reverse('sira'), {'page': 2})
        self.assertEqual(response.context['page_obj'].number, 2)
        self.assertEqual(response.context['data'], SIRA_PAGES[1])


class LatestVideoTests(TestCase):
    def test_empty(self):
        self.assertEqual(self.client.get(reverse('latest_video')).json(), {'id': None})

    def test_returns_last_added_card(self):
        make_card('Старое')
        last = make_card('Новое', image_url='https://example.com/a.jpg')
        data = self.client.get(reverse('latest_video')).json()
        self.assertEqual(data['title'], 'Новое')
        self.assertEqual(data['url'], last.url)
        self.assertEqual(data['image'], 'https://example.com/a.jpg')


@override_settings(CRON_SECRET='s3cret')
class CronTests(TestCase):
    url = '/api/cron/parse-youtube/'

    def test_rejects_without_or_with_wrong_secret(self):
        self.assertEqual(self.client.get(self.url).status_code, 403)
        response = self.client.get(self.url, headers={'Authorization': 'Bearer nope'})
        self.assertEqual(response.status_code, 403)

    @override_settings(CRON_SECRET='')
    def test_rejects_when_secret_is_not_configured(self):
        response = self.client.get(self.url, headers={'Authorization': 'Bearer '})
        self.assertEqual(response.status_code, 403)

    @patch('main.views.call_command')
    def test_runs_parser(self, call_command):
        response = self.client.get(self.url, headers={'Authorization': 'Bearer s3cret'})
        self.assertEqual(response.json(), {'status': 'ok'})
        call_command.assert_called_once_with('parse_youtube')

    @patch('main.views.call_command', side_effect=RuntimeError('boom'))
    def test_reports_parser_failure(self, _):
        response = self.client.get(self.url, headers={'Authorization': 'Bearer s3cret'})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['message'], 'boom')


@override_settings(YOUTUBE_CHANNEL_IDS=['chan1'])
class ParseYoutubeCommandTests(TestCase):
    @staticmethod
    def fake_feed():
        entry = type('Entry', (), {
            'id': 'yt:video:abc123',
            'link': 'https://www.youtube.com/watch?v=abc123',
            'title': '🔥 Новый урок',
            'published': '2026-03-05T10:00:00+00:00',
        })()
        feed = type('Feed', (), {'title': 'Канал'})()
        return type('Parsed', (), {'entries': [entry], 'feed': feed})()

    @patch('main.management.commands.parse_youtube.feedparser.parse')
    def test_creates_card_once(self, parse):
        parse.return_value = self.fake_feed()

        call_command('parse_youtube', stdout=StringIO())
        call_command('parse_youtube', stdout=StringIO())

        card = Card.objects.get()
        self.assertEqual(card.title, 'Новый урок')
        self.assertEqual(card.video_id, 'abc123')
        self.assertEqual(card.channel_name, 'Канал')
        self.assertEqual(card.published, date(2026, 3, 5))
        self.assertIn('abc123', card.image_url)

    @override_settings(YOUTUBE_CHANNEL_IDS=[])
    def test_fails_without_channels(self):
        with self.assertRaises(CommandError):
            call_command('parse_youtube', stdout=StringIO())
