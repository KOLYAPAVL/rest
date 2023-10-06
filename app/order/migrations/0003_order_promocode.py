# Generated by Django 4.1.4 on 2023-01-01 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('promo', '0001_initial'),
        ('order', '0002_order_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='promocode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='promo.promocode', verbose_name='Промокод'),
        ),
    ]
