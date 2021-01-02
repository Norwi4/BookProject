from django.db import models
from django.contrib.auth.models import User
from django.db import models


class Bb(models.Model):
    title = models.CharField(max_length=50, verbose_name="Товар")
    content = models.TextField(null=True, blank=True, verbose_name="Описание")
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name="Рубрика")
    price = models.FloatField(null=True, blank=True, verbose_name="Цена")
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Опубликовано")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=User, verbose_name="Пользователь")

    class Meta:
        verbose_name = "Обьявление"
        verbose_name_plural = "Обьявления"
        ordering = ['-published']

    def __str__(self):
        return self.title


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name="Название")

    class Meta:
        verbose_name = "Рубрика"
        verbose_name_plural = "Рубрики"
        ordering = ['name']

    def __str__(self):
        return self.name

