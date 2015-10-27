# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0013_punch_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='routine',
            name='video',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
