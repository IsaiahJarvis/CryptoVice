# Generated by Django 4.2.16 on 2024-11-07 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CryptoApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Coins',
            new_name='Coin',
        ),
    ]