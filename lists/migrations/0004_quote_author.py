# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='author',
            field=models.TextField(default=''),
        ),
    ]
