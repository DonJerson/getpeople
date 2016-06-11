# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0008_auto_20160520_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='note',
            field=models.TextField(max_length=300, null=True, blank=True),
        ),
    ]
