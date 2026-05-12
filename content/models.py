from django.db import models

class Track(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    audio_file = models.FileField(upload_to='audio/', verbose_name="Аудиофайл")

    def __str__(self):
        return self.title