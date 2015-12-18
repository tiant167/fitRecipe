# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0015_auto_20151217_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='components',
            field=models.TextField(default='[]', help_text='JSON \u5b57\u7b26\u4e32<code>\n        [{\n          "ingredient": "\u732a\u8089",\n          "amount": 100,\n          "remark": "this is remark tips"\n        }]\n    </code>'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='procedures',
            field=models.TextField(default='[]', help_text='JSON \u5b57\u7b26\u4e32 <code>\n        [{\n          "content": "this is content",\n          "img": "http://img.url"\n        }]\n    </code>'),
        ),
    ]
