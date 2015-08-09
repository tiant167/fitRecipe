# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0006_auto_20150725_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='collection_count',
            field=models.IntegerField(default=0, verbose_name='\u6536\u85cf\u6570'),
        ),
    ]
