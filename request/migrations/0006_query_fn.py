# Generated by Django 4.0.2 on 2022-02-28 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0005_queryset_fn'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='fn',
            field=models.CharField(blank=True, max_length=160, null=True, verbose_name='Примечание'),
        ),
    ]
