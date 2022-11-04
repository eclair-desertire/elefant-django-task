# Generated by Django 4.0 on 2022-11-04 20:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('genre_id', models.AutoField(primary_key=True, serialize=False)),
                ('genre', models.CharField(default='', max_length=255, unique=True, verbose_name='Жанр')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('explanation', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('rate', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)], verbose_name='Оценка')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_id', models.AutoField(primary_key=True, serialize=False)),
                ('book_name', models.CharField(default='', max_length=255, verbose_name='Наименование книги')),
                ('author', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Автор')),
                ('description', models.TextField(blank=True, default='', null=True, verbose_name='Описание книги')),
                ('published_date', models.DateTimeField()),
                ('avg_rate', models.IntegerField(verbose_name='Средний рейтинг книги')),
                ('genre', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='catalog.genre')),
                ('reviews', models.ManyToManyField(blank=True, null=True, related_name='books', to='catalog.Review')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.EmailField(default='', max_length=50, unique=True, verbose_name='email')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(choices=[(True, 'Не заблокирован'), (False, 'Заблокирован')], default=True, verbose_name='Статус доступа')),
                ('fav_books', models.ManyToManyField(blank=True, null=True, related_name='users', to='catalog.Book')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('reviews', models.ManyToManyField(blank=True, null=True, related_name='users', to='catalog.Review')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
