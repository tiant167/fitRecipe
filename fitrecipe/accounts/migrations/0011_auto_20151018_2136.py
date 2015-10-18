# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20151018_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='user',
            field=models.OneToOneField(verbose_name='\u7528\u6237', to='accounts.Account'),
        ),
    ]
