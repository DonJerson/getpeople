# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('candidates', '0002_auto_20160512_0419'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LogTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.CharField(max_length=100)),
                ('priority_offset', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Recruiter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameField(
            model_name='position',
            old_name='salary',
            new_name='salary_anual',
        ),
        migrations.AddField(
            model_name='candidate',
            name='priority',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='position',
            name='location',
            field=models.CharField(default='en la nada', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='position',
            name='skills',
            field=models.TextField(default='pendejo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='log',
            name='candidate',
            field=models.ForeignKey(to='candidates.Candidate'),
        ),
        migrations.AddField(
            model_name='log',
            name='recruiter',
            field=models.ForeignKey(to='candidates.Recruiter'),
        ),
    ]
