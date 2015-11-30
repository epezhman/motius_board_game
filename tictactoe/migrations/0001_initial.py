# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('start_game', models.DateTimeField(auto_now_add=True)),
                ('last_active', models.DateTimeField(auto_now=True)),
                ('state', models.CharField(choices=[('A', 'Active Game'), ('F', 'First Player Won'), ('S', 'Second Player Won'), ('D', 'Draw Game')], default='A', max_length=1)),
                ('first_player', models.ForeignKey(related_name='as_first_player', to=settings.AUTH_USER_MODEL)),
                ('next_to_play', models.ForeignKey(related_name='next_games', to=settings.AUTH_USER_MODEL)),
                ('second_player', models.ForeignKey(related_name='as_second_player', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('comment', models.CharField(verbose_name='Invitation Comment', help_text='Write some comment to the user when invitating', blank=True, max_length=300)),
                ('sent_time', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(related_name='from_invitations', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(verbose_name='User to Invite', related_name='to_invitations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('x', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)])),
                ('y', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)])),
                ('comment', models.CharField(blank=True, max_length=300)),
                ('by_first_player', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(to='tictactoe.Game')),
            ],
            options={
                'get_latest_by': 'timestamp',
            },
        ),
    ]
