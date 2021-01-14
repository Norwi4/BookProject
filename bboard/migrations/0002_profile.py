# Generated by Django 3.1.4 on 2021-01-14 13:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(db_index=True, max_length=20, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(db_index=True, max_length=20, null=True, verbose_name='Фамилия')),
                ('email', models.EmailField(db_index=True, max_length=254, null=True, verbose_name='Email')),
                ('about', models.TextField(blank=True, db_index=True, null=True, verbose_name='О себе')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
