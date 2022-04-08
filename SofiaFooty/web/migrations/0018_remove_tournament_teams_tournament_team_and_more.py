# Generated by Django 4.0.3 on 2022-03-30 15:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0017_remove_team_members_player_team_alter_match_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournament',
            name='teams',
        ),
        migrations.AddField(
            model_name='tournament',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.team'),
        ),
        migrations.AlterField(
            model_name='team',
            name='captain',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
