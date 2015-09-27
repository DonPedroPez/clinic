# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_auto_20150927_0937'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='duty',
            options={'verbose_name_plural': 'duties'},
        ),
    ]
