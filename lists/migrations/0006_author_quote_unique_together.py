# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0005_auto_20161122_1554'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quote',
            options={'ordering': ('id',)},
        ),
        migrations.AlterUniqueTogether(
            name='quote',
            unique_together=set([('author', 'text')]),
        ),
    ]
