# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Object',
            fields=[
                ('uuid', models.CharField(primary_key=True, default=uuid.uuid4, serialize=False, max_length=50, unique=True, verbose_name=b'uuid')),
                ('scad_file', models.FileField(upload_to=b'', verbose_name=b'Openscad File', blank=True)),
                ('stl_file', models.FileField(upload_to=b'', verbose_name=b'STL File', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
