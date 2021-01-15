from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, verbose_name="Пользователь")
    first_name = models.CharField(max_length=20, db_index=True, verbose_name="Имя", null=True)
    last_name = models.CharField(max_length=20, db_index=True, verbose_name="Фамилия", null=True)
    email = models.EmailField(db_index=True, verbose_name="Email", null=True)
    about = models.TextField(db_index=True, null=True, blank=True, verbose_name="О себе")

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return str(self.user)


class Response(models.Model):
    """Отклики"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь")
    text = models.TextField(verbose_name="Сообщение", max_length=5000)
    post = models.ForeignKey(Bb, verbose_name="Пост", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.post}"

    class Meta:
        verbose_name = "Отклик"
        verbose_name_plural = "Отклики"


