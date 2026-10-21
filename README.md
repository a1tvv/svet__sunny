<div align="center">

<img src="static/img/banner.png" alt="Свет Сунны" width="100%">

# Свет Сунны 🌙✨

**Призыв к пониманию первых поколений мусульман**

Единая лента уроков с YouTube-каналов, умный поиск и аудиокурс по Сире Пророка ﷺ.

<br>

![Django](https://img.shields.io/badge/Django-5.1-0f0f0f?style=for-the-badge&logo=django&logoColor=f1f1f1)
![Python](https://img.shields.io/badge/Python-3.12-0f0f0f?style=for-the-badge&logo=python&logoColor=3ea6ff)
![YouTube](https://img.shields.io/badge/YouTube-RSS%20%2B%20API-0f0f0f?style=for-the-badge&logo=youtube&logoColor=ff0000)
![Vercel](https://img.shields.io/badge/Vercel-deploy-0f0f0f?style=for-the-badge&logo=vercel&logoColor=f1f1f1)

[Telegram](https://t.me/svettsunny) · [YouTube](https://youtube.com/@abdurtwhd) · [Instagram](https://www.instagram.com/abdurtwhd) · [Pinterest](https://ru.pinterest.com/abdurtawhidi)

</div>

---

## ✨ Возможности

- 🎬 **Лента видео** с нескольких YouTube-каналов, вкладки по авторам и пагинация.
- 🔎 **Умный поиск** ([main/search.py](main/search.py)): не зависит от регистра, `ё/е`, апострофов и удвоенных букв, понимает падежи, опечатки и неполные слова, исправляет неверную раскладку и латиницу (`cthf` → «сира»).
- 🎧 **Сира Пророка ﷺ** — аудиолекции по частям с контрольными вопросами ([main/sira_data.py](main/sira_data.py)).
- 🔄 **Автообновление**: раз в сутки Vercel Cron подтягивает новые видео из RSS.
- 🛠 **Админка Django** для ручного управления карточками.

## 🚀 Запуск локально

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env        # заполните значения
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Сайт будет на http://127.0.0.1:8000, админка — на `/admin/`.

## 📥 Загрузка видео

| Команда | Что делает |
| --- | --- |
| `python manage.py parse_youtube` | Последние видео каналов из RSS (без API-ключа). Её же запускает cron. |
| `python manage.py parse_youtube_full [--channel ID]` | Все видео канала через YouTube Data API v3. |
| `python manage.py update_durations` | Дописывает длительность карточкам, у которых её нет. |

## ⚙️ Переменные окружения

| Переменная | Назначение |
| --- | --- |
| `DJANGO_SECRET_KEY` | Секретный ключ. **Обязателен на Vercel.** |
| `DJANGO_DEBUG` | `1` — включить отладку локально. |
| `DATABASE_URL` | Строка подключения к БД. Без неё используется SQLite. |
| `YOUTUBE_CHANNEL_IDS` | ID каналов через запятую. |
| `YOUTUBE_API_KEY` | Ключ YouTube Data API (для `parse_youtube_full` и `update_durations`). |
| `CRON_SECRET` | Секрет для `/api/cron/parse-youtube/`. |
| `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | Доступ к хранилищу медиа (DigitalOcean Spaces). |

## 🧪 Тесты

```bash
DATABASE_URL=sqlite:///:memory: python manage.py test main
```

`DATABASE_URL` переопределяется нарочно, чтобы тесты не обращались к базе из `.env`.

## 🗂 Структура

```
main/        лента, поиск, страницы, команды парсинга
content/     вспомогательное приложение (модели уроков)
templates/   HTML-шаблоны
static/      CSS и изображения
vercel.json  деплой и расписание cron
```

## 🤝 Связаться

Идеи и поправки — в Telegram: [@abdurtwhd](https://t.me/abdurtwhd).
Проект не нуждается в финансировании — достаточно поделиться ссылкой с близкими.

<div align="center">

© Свет Сунны ١٤٤٧

</div>
