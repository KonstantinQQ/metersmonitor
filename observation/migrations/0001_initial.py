# Generated by Django 4.0.2 on 2022-02-28 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('control', '0001_initial'),
        ('request', '0006_query_fn'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(default=None, max_length=20, verbose_name='Значение')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('dev', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='control.device', verbose_name='Устройство')),
                ('qry', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='request.query', verbose_name='Атрибут')),
            ],
            options={
                'verbose_name_plural': 'Значения',
                'db_table': 'attributes',
                'ordering': ('dev', 'qry'),
                'managed': True,
                'index_together': {('dev', 'qry')},
            },
        ),
    ]
