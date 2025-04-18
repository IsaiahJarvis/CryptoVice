# Generated by Django 4.2.16 on 2024-11-07 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('crypto_id', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=100)),
                ('market_cap', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('circulating_supply', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
