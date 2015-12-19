# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0001_initial'),
        ('recipe', '0011_auto_20151112_0152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='component',
            name='ingredient',
        ),
        migrations.RemoveField(
            model_name='component',
            name='recipe',
        ),
        migrations.RemoveField(
            model_name='nutrition',
            name='ingredient',
        ),
        migrations.RemoveField(
            model_name='procedure',
            name='recipe',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='effect_labels',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='meat_labels',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='other_labels',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='time_labels',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='carbohydrate',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='cholesterol',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='energy',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='fat',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='fatty_acids',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='fiber',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='protein',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='sodium',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='vc',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='vd',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='water',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='carbohydrate',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='cholesterol',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='components',
            field=jsonfield.fields.JSONField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='energy',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='fat',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='fatty_acids',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='fiber',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='labels',
            field=models.ManyToManyField(to='label.Label', verbose_name='\u6807\u7b7e'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='procedures',
            field=jsonfield.fields.JSONField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='protein',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='sodium',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='total_amount',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='vc',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='vd',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='water',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='calories',
            field=models.FloatField(default=0, verbose_name='\u6bcf\u767e\u514b\u5361\u8def\u91cc'),
        ),
        migrations.DeleteModel(
            name='Component',
        ),
        migrations.DeleteModel(
            name='Nutrition',
        ),
        migrations.DeleteModel(
            name='Procedure',
        ),
    ]
