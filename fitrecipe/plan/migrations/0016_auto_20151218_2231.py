# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0015_auto_20151217_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='routines',
            field=models.TextField(default=b'[]', help_text='<code>\n        [{\n          "video": "http://video.url",\n          "dish": [{\n            "type": 0,\n            "ingredient": [{\n              "amount": 50,\n              "id": 2\n            }],\n            "recipe": [{\n              "amount": 50,\n              "id": 4\n            }]\n          }]\n        }]\n    </code>'),
        ),
    ]
