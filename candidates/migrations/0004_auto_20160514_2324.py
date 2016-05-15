# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0003_auto_20160514_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='priority',
            field=models.IntegerField(default=0),
        ),
    ]
