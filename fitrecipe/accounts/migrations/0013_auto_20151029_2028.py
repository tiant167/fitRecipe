# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_evaluation_exercisetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='avatar',
            field=models.URLField(default=b'http://7xk6xp.com1.z0.glb.clouddn.com/default_header.png'),
        ),
    ]
