# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0005_notification_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='unread',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='sender_content_type',
            field=models.ForeignKey(related_name='nofity_sender', to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='verb',
            field=models.CharField(max_length=255),
        ),
    ]
