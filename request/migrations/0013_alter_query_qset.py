# Generated by Django 4.0.3 on 2022-05-20 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0012_alter_query_attribute'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='qset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='request.queryset', verbose_name='Набор'),
        ),
    ]