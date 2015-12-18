# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0014_auto_20151217_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='components',
            field=models.TextField(help_text='JSON \u5b57\u7b26\u4e32<code>[{"ingredient": "\u732a\u8089", "amount": 100, "remark": "this is remark tips"}]</code>', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='procedures',
            field=models.TextField(help_text='JSON \u5b57\u7b26\u4e32<code>[{"content": "this is content", "img": "http://img.url"}]</code>', null=True, blank=True),
        ),
    ]
