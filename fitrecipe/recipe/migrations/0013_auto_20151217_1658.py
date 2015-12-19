# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0012_auto_20151217_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='carbohydrate',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cholesterol',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='energy',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='fat',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='fatty_acids',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='fiber',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='protein',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='sodium',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='total_amount',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='vc',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='vd',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='water',
            field=models.FloatField(default=0.0),
        ),
    ]
