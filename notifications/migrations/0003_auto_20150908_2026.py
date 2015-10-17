# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20150908_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='action_content_type',
            field=models.ForeignKey(related_name='notify_action', blank=True, to='contenttypes.ContentType', null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='target_content_type',
            field=models.ForeignKey(related_name='notify_target', blank=True, to='contenttypes.ContentType', null=True),
        ),
    ]
