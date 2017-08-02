# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-23 02:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import month.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lots', '0002_auto_20170717_2115'),
        ('ledger', '0002_auto_20170717_2255'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeeLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=13)),
                ('date_start', month.models.MonthField(db_index=True)),
                ('date_end', month.models.MonthField(db_index=True)),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lots.Lot')),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True)),
                ('number', models.IntegerField(blank=True, db_index=True, null=True)),
                ('details', models.CharField(blank=True, max_length=254)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=13)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lots.Contact')),
                ('entry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ledger.Entry')),
            ],
        ),
        migrations.AddField(
            model_name='feeline',
            name='receipt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='revenue.Receipt'),
        ),
    ]