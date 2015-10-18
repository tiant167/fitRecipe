# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20150927_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='date',
            field=models.DateField(default=datetime.date(2015, 10, 18), verbose_name='\u65e5\u671f'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='user',
            field=models.ForeignKey(verbose_name='\u7528\u6237', to='accounts.Account', unique=True),
        ),
    ]
