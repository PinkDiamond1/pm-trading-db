# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-12 13:37
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('address', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('factory', models.CharField(max_length=20)),
                ('creator', models.CharField(max_length=20)),
                ('creation_date', models.DateTimeField()),
                ('creation_block', models.PositiveIntegerField()),
                ('collateral_token', models.CharField(max_length=20)),
                ('is_winning_outcome_set', models.BooleanField()),
                ('winning_outcome', models.BigIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('resolution_date', models.DateTimeField()),
                ('ipfs_hash', models.CharField(max_length=46, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('address', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('factory', models.CharField(max_length=20)),
                ('creator', models.CharField(max_length=20)),
                ('creation_date', models.DateTimeField()),
                ('creation_block', models.PositiveIntegerField()),
                ('market_maker', models.CharField(max_length=20)),
                ('fee', models.PositiveIntegerField()),
                ('funding', models.BigIntegerField()),
                ('net_outcome_tokens_sold', models.TextField(validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('stage', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Oracle',
            fields=[
                ('address', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('factory', models.CharField(max_length=20)),
                ('creator', models.CharField(max_length=20)),
                ('creation_date', models.DateTimeField()),
                ('creation_block', models.PositiveIntegerField()),
                ('is_outcome_set', models.BooleanField(default=False)),
                ('outcome', models.BigIntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OutcomeToken',
            fields=[
                ('address', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('factory', models.CharField(max_length=20)),
                ('creator', models.CharField(max_length=20)),
                ('creation_date', models.DateTimeField()),
                ('creation_block', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CategoricalEvent',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='relationaldb.Event')),
            ],
            options={
                'abstract': False,
            },
            bases=('relationaldb.event',),
        ),
        migrations.CreateModel(
            name='CategoricalEventDescription',
            fields=[
                ('eventdescription_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='relationaldb.EventDescription')),
                ('outcomes', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
            ],
            bases=('relationaldb.eventdescription',),
        ),
        migrations.CreateModel(
            name='CentralizedOracle',
            fields=[
                ('oracle_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='relationaldb.Oracle')),
                ('owner', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
            bases=('relationaldb.oracle',),
        ),
        migrations.CreateModel(
            name='ScalarEvent',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='relationaldb.Event')),
                ('lower_bound', models.BigIntegerField()),
                ('upper_bound', models.BigIntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('relationaldb.event',),
        ),
        migrations.CreateModel(
            name='ScalarEventDescription',
            fields=[
                ('eventdescription_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='relationaldb.EventDescription')),
                ('unit', models.TextField()),
                ('decimals', models.PositiveIntegerField()),
            ],
            bases=('relationaldb.eventdescription',),
        ),
        migrations.CreateModel(
            name='UltimateOracle',
            fields=[
                ('oracle_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='relationaldb.Oracle')),
                ('collateral_token', models.CharField(max_length=20)),
                ('spread_multiplier', models.PositiveIntegerField()),
                ('challenge_period', models.BigIntegerField()),
                ('challenge_amount', models.BigIntegerField()),
                ('front_runner_period', models.BigIntegerField()),
                ('forwarded_outcome', models.BigIntegerField(null=True)),
                ('outcome_set_at_timestamp', models.BigIntegerField(null=True)),
                ('front_runner', models.BigIntegerField(null=True)),
                ('front_runner_set_at_timestamp', models.BigIntegerField(null=True)),
                ('total_amount', models.BigIntegerField(null=True)),
                ('forwarded_oracle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ultimate_oracle_forwarded_oracle', to='relationaldb.Oracle')),
            ],
            options={
                'abstract': False,
            },
            bases=('relationaldb.oracle',),
        ),
        migrations.AddField(
            model_name='outcometoken',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='relationaldb.Event'),
        ),
        migrations.AddField(
            model_name='market',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='relationaldb.Event'),
        ),
        migrations.AddField(
            model_name='event',
            name='oracle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='relationaldb.Oracle'),
        ),
        migrations.AddField(
            model_name='centralizedoracle',
            name='event_description',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='relationaldb.EventDescription'),
        ),
    ]
