from django.conf import settings
from django.db import models

class Entry(models.Model):
    name = models.CharField('Имя', max_length=50)
    message = models.TextField('Сообщение', max_length=500)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='entries',
        null=True, blank=True,
        verbose_name='Автор'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return f"{self.name}: {self.message[:30]}"
