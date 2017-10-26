# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-16 19:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import month.models
from django.utils import timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lots', '0002_auto_20170717_2115'),
        ('ledger', '0002_auto_20170717_2255'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', month.models.MonthField(db_index=True, default=django.utils.timezone.now)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=13)),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lots.Lot')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='FeeLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=13)),
                ('date', month.models.MonthField(db_index=True, default=django.utils.timezone.now)),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lots.Lot')),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True, default=timezone.now)),
                ('number', models.CharField(blank=True, max_length=254, db_index=True, null=True)),
                ('details', models.CharField(blank=True, max_length=254)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=13)),
                ('save_in_ledger', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('debit_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receipt_debit_accounts', to='ledger.Account')),
                ('credit_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, default=3, related_name='receipt_credit_accounts', to='ledger.Account')),
                ('contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='lots.Contact')),
                ('entry', models.OneToOneField(on_delete=django.db.models.deletion.SET_NULL, blank=True, null=True, to='ledger.Entry')),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=13)),
                ('discount_rate', models.IntegerField(blank=True)),
            ],
            options={
                'abstract': False,
                'ordering': ['date', 'id'],
            },
        ),
        migrations.AddField(
            model_name='feeline',
            name='receipt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='revenue.Receipt'),
        ),
    ]
