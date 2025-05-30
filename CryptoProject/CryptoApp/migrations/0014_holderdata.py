# Generated by Django 4.2.16 on 2025-02-12 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CryptoApp', '0013_delete_user_coin'),
    ]

    operations = [
        migrations.CreateModel(
            name='HolderData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(max_length=255, unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('total_holders', models.IntegerField()),
                ('holders_over_10', models.IntegerField()),
                ('holders_over_50', models.IntegerField()),
                ('holders_over_100', models.IntegerField()),
                ('holders_over_500', models.IntegerField()),
                ('holders_over_1000', models.IntegerField()),
                ('holders_over_2500', models.IntegerField()),
            ],
        ),
    ]
