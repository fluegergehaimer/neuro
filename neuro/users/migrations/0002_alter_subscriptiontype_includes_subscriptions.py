# Generated by Django 5.1.7 on 2025-03-11 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptiontype',
            name='includes_subscriptions',
            field=models.ManyToManyField(blank=True, related_name='included_in', to='users.subscriptiontype', verbose_name='Подписка'),
        ),
    ]
