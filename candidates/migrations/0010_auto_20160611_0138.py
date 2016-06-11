# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0009_auto_20160611_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='note',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
