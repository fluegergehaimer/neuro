# Generated by Django 5.1.6 on 2025-02-06 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='neurouser',
            name='is_paid_subscriber',
            field=models.BooleanField(default=False, verbose_name='Платный подписчик'),
        ),
    ]
