# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0013_auto_20151217_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='components',
            field=json_field.fields.JSONField(default='null', help_text='<code>[{"ingredient": "\u732a\u8089", "amount": 100, "remark": "this is remark tips"}]</code>', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='procedures',
            field=json_field.fields.JSONField(default='null', help_text='<code>[{"content": "this is content", "img": "http://img.url"}]</code>', null=True, blank=True),
        ),
    ]
