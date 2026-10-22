<a href="https://nur-as-sunnah.com"><img src="docs/assets/banner.svg" alt="Свет Сунны — призыв к пониманию первых поколений мусульман" width="100%"></a>

<p align="center">
  <a href="#features">Возможности&nbsp;›</a>&emsp;
  <a href="#stack">Стек&nbsp;›</a>&emsp;
  <a href="#run">Запуск&nbsp;›</a>&emsp;
  <a href="#structure">Структура&nbsp;›</a>&emsp;
  <a href="#contact">Связаться&nbsp;›</a>
</p>

<br>

<img src="docs/assets/stats.svg" alt="100 аудиолекций по Сире, 9 частей курса, 26 тестов" width="100%">

<br>
<br>

<img src="docs/assets/quote.svg" alt="Пролить свет знания о пути Пророка и его сподвижников — цель проекта" width="100%">

<br>
<br>

<a name="features"></a>
<img src="docs/assets/titles/features.svg" alt="Возможности" width="100%">

<a href="https://nur-as-sunnah.com"><img src="docs/assets/rows/feed.svg" alt="Лента видео — уроки с нескольких YouTube-каналов: вкладки по авторам и пагинация" width="100%"></a>
<a href="main/search.py"><img src="docs/assets/rows/search.svg" alt="Умный поиск — падежи, опечатки, ё/е, неверная раскладка" width="100%"></a>
<a href="main/sira_data.py"><img src="docs/assets/rows/sira.svg" alt="Сира Пророка — аудиолекции по частям и контрольные вопросы" width="100%"></a>
<a href="vercel.json"><img src="docs/assets/rows/cron.svg" alt="Автообновление — раз в сутки Vercel Cron подтягивает новые видео из RSS" width="100%"></a>
<a href="main/admin.py"><img src="docs/assets/rows/admin.svg" alt="Админка — ручное управление карточками" width="100%"></a>

<br>
<br>

<a name="stack"></a>
<img src="docs/assets/titles/stack.svg" alt="Стек" width="100%">

<img src="docs/assets/stack.svg" alt="Python, Django 5.1, SQLite, PostgreSQL, YouTube RSS, YouTube Data API, feedparser, requests, DigitalOcean Spaces, Vercel, Vercel Cron, WhiteNoise, dj-database-url" width="100%">

<br>
<br>

<a name="run"></a>
<img src="docs/assets/titles/run.svg" alt="Запуск" width="100%">

<img src="docs/assets/run.svg" alt="Запуск сайта в терминале" width="100%">

<details>
<summary>Скопировать команды</summary>
<br>

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env        # заполните значения
python manage.py migrate
python manage.py createsuperuser

python manage.py parse_youtube
python manage.py runserver
```

Сайт — на http://127.0.0.1:8000, админка — на `/admin/`.

**Команды загрузки видео**

| Команда | Что делает |
| --- | --- |
| `parse_youtube` | Последние видео каналов из RSS, без API-ключа. Её же запускает cron. |
| `parse_youtube_full [--channel ID]` | Все видео канала через YouTube Data API v3. |
| `update_durations` | Дописывает длительность карточкам, у которых её нет. |

**Тесты**

```bash
DATABASE_URL=sqlite:///:memory: python manage.py test main
```

**Пересобрать картинки README**

```bash
python3 scripts/build_readme_assets.py
```

</details>

<details>
<summary>Переменные окружения</summary>
<br>

| Переменная | Назначение |
| --- | --- |
| `DJANGO_SECRET_KEY` | Секретный ключ. Обязателен на Vercel. |
| `DJANGO_DEBUG` | `1` — включить отладку локально. |
| `DATABASE_URL` | Строка подключения к БД. Без неё используется SQLite. |
| `YOUTUBE_CHANNEL_IDS` | ID каналов через запятую. |
| `YOUTUBE_API_KEY` | Ключ YouTube Data API. |
| `CRON_SECRET` | Секрет для `/api/cron/parse-youtube/`. |
| `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | Доступ к хранилищу медиа (DigitalOcean Spaces). |

</details>

<br>
<br>

<a name="structure"></a>
<img src="docs/assets/titles/structure.svg" alt="Структура" width="100%">

<img src="docs/assets/structure.svg" alt="Структура репозитория" width="100%">

<br>
<br>

<a name="contact"></a>
<img src="docs/assets/titles/contact.svg" alt="Связаться" width="100%">

<p>
<a href="https://t.me/svettsunny"><img src="docs/assets/contact/telegram.svg" alt="Telegram: @svettsunny" width="32.5%"></a><a href="https://youtube.com/@abdurtwhd"><img src="docs/assets/contact/youtube.svg" alt="YouTube: @abdurtwhd" width="32.5%"></a><a href="https://www.instagram.com/abdurtwhd"><img src="docs/assets/contact/instagram.svg" alt="Instagram: @abdurtwhd" width="32.5%"></a>
</p>

<br>

<img src="docs/assets/footer.svg" alt="Свет знания. Путь сподвижников." width="100%">

<p align="center">
  <sub>Проект не нуждается в финансировании — достаточно поделиться ссылкой с близкими.</sub>
</p>
