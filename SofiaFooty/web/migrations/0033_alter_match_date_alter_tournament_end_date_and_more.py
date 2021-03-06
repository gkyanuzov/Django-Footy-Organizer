# Generated by Django 4.0.3 on 2022-04-22 18:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0032_alter_match_away_team_goals_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateField(default=datetime.date(2022, 4, 22)),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='end_date',
            field=models.DateField(default=datetime.date(2022, 4, 22)),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='start_date',
            field=models.DateField(default=datetime.date(2022, 4, 22)),
        ),
    ]
