# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0006_auto_20150909_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='unread',
        ),
    ]
