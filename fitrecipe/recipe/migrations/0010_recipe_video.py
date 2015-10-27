# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0009_auto_20150809_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='video',
            field=models.CharField(default=b'', max_length=100, verbose_name='\u83dc\u8c31\u89c6\u9891ID'),
        ),
    ]
