# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-18 02:15
from __future__ import unicode_literals

from django.db import models, migrations


def load_data(apps, schema_editor):
    LotType = apps.get_model("lots", "LotType")

    LotType(name="Casa").save()
    LotType(name="Lote").save()


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data)
    ]
