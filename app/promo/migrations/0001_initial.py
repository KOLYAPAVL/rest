# Generated by Django 4.1.4 on 2023-01-01 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Promocode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='promocode/', verbose_name='Изображение')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Промокод')),
                ('discount', models.IntegerField(default=0, verbose_name='Скидки (%)')),
                ('color', models.CharField(max_length=10, verbose_name='Цвет')),
            ],
            options={
                'verbose_name': 'Промокод',
                'verbose_name_plural': 'Промокоды',
            },
        ),
    ]