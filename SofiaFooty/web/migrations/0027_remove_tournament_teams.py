# Generated by Django 4.0.3 on 2022-04-10 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0026_tournament_teams'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournament',
            name='teams',
        ),
    ]