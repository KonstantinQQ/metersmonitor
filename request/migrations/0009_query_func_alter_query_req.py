# Generated by Django 4.0.3 on 2022-04-08 15:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0008_alter_query_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='func',
            field=models.CharField(default='03', max_length=4, validators=[django.core.validators.RegexValidator('^[A-Fa-f0-9]+$')], verbose_name='Команда'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='query',
            name='req',
            field=models.CharField(max_length=40, validators=[django.core.validators.RegexValidator('^[A-Fa-f0-9]+$')], verbose_name='Параметры'),
        ),
    ]