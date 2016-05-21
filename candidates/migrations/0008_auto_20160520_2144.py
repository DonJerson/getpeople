# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0007_auto_20160517_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='note',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='email',
            field=models.EmailField(unique=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='phone',
            field=models.CharField(default=uuid.uuid1, unique=True, max_length=20),
        ),
    ]
