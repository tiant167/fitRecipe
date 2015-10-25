# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20151018_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='exerciseTime',
            field=models.IntegerField(default=0, verbose_name='\u8fd0\u52a8\u65f6\u95f4'),
            preserve_default=False,
        ),
    ]
