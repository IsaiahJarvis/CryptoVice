# Generated by Django 4.2.16 on 2025-01-29 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CryptoApp', '0011_coin_network'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Coin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('crypto_id', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=100)),
                ('image_link', models.URLField(blank=True, max_length=2000, null=True)),
                ('fdv', models.DecimalField(blank=True, decimal_places=10, max_digits=100, null=True)),
                ('market_cap', models.DecimalField(blank=True, decimal_places=10, max_digits=100, null=True)),
                ('circulating_supply', models.CharField(blank=True, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=10, max_digits=100, null=True)),
                ('contract_address', models.CharField(blank=True, null=True)),
                ('network', models.CharField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
