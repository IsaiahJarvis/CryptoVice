# Generated by Django 4.2.16 on 2024-11-14 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CryptoApp', '0007_alter_coin_circulating_supply'),
    ]

    operations = [
        migrations.AddField(
            model_name='coin',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='coin',
            name='market_cap',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=100, null=True),
        ),
    ]