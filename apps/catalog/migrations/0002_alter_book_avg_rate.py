# Generated by Django 4.0 on 2022-11-04 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='avg_rate',
            field=models.IntegerField(default=0, verbose_name='Средний рейтинг книги'),
        ),
    ]
