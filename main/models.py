from django.db import models


class Card(models.Model):
    TYPE_CHOICES = [
        ('youtube', 'YouTube видео'),
        ('playlist', 'YouTube плейлист'),
        ('internal', 'Внутренняя страница'),
        ('telegram', 'Telegram канал'),
        ('external', 'Внешняя ссылка'),
    ]

    title = models.CharField('Заголовок', max_length=300)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Картинка', upload_to='cards/', blank=True, null=True)
    image_url = models.URLField('URL картинки (если нет файла)', blank=True)
    url = models.CharField('Ссылка (URL или name)', max_length=500)
    card_type = models.CharField('Тип', max_length=20, choices=TYPE_CHOICES, default='youtube')
    bg_color = models.CharField('Фон карточки', max_length=20, blank=True, help_text='Например #f8c512')
    order = models.IntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активна', default=True)
    published = models.DateField('Дата', null=True, blank=True)
    duration = models.CharField(max_length=16, blank=True)

    # новые поля для парсера
    channel_id = models.CharField(max_length=64, blank=True, db_index=True)
    channel_name = models.CharField(max_length=255, blank=True)
    video_id = models.CharField(max_length=32, blank=True, db_index=True)

    class Meta:
        ordering = ['order', '-published']
        verbose_name = 'Карточка'
        verbose_name_plural = 'Карточки'

    def __str__(self):
        return self.title

    def get_url(self):
        """Возвращает правильный URL: либо внешний, либо внутренний name."""
        if self.card_type == 'internal':
            from django.urls import reverse
            return reverse(self.url)
        return self.url

    def get_image(self):
        """Возвращает картинку: сначала файл, потом URL."""
        if self.image:
            return self.image.url
        return self.image_url or ''