from django.db import models

class Record(models.Model):
    name = models.CharField(
        max_length=49,  # меньше 50 символов
        verbose_name="Название"
    )
    date = models.DateTimeField(
        verbose_name="Дата и время",
        help_text="Формат: YYYY-MM-DD_HH:mm"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"