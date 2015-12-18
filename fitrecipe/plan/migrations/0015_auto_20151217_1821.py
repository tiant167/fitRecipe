# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0014_routine_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='routine',
        ),
        migrations.RemoveField(
            model_name='routine',
            name='plan',
        ),
        migrations.RemoveField(
            model_name='singleingredient',
            name='dish',
        ),
        migrations.RemoveField(
            model_name='singleingredient',
            name='ingredient',
        ),
        migrations.RemoveField(
            model_name='singlerecipe',
            name='dish',
        ),
        migrations.RemoveField(
            model_name='singlerecipe',
            name='recipe',
        ),
        migrations.AddField(
            model_name='plan',
            name='routines',
            field=models.TextField(default=b'[]', help_text='<code>\n        [{\n          "video": "http://video.url",\n          "dishes": [{\n            "type": 0,\n            "ingredients": [{\n              "amount": 50,\n              "id": 2\n            }],\n            "recipes": [{\n              "amount": 50,\n              "id": 4\n            }]\n          }]\n        }]\n    </code>'),
        ),
        migrations.DeleteModel(
            name='Dish',
        ),
        migrations.DeleteModel(
            name='Routine',
        ),
        migrations.DeleteModel(
            name='SingleIngredient',
        ),
        migrations.DeleteModel(
            name='SingleRecipe',
        ),
    ]
