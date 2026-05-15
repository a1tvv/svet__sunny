from django.db import models

class Track(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    audio_file = models.FileField(upload_to='audio/', verbose_name="Аудиофайл")

    def __str__(self):
        return self.title
    
    
class RiyadhAsSalihin(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название урока")
    
    # Добавили null=True, чтобы не было ошибки "non-nullable" при миграции
    audio_url = models.URLField(
        max_length=500, 
        verbose_name="Ссылка на аудио (S3)", 
        null=True, 
        blank=True
    )
    
    description = models.TextField(verbose_name="Описание/Вопросы", blank=True)
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок вывода")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Урок Рияд ас-Салихин"
        verbose_name_plural = "Уроки Рияд ас-Салихин"

    def __str__(self):
        return self.title