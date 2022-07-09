# Generated by Django 4.0.5 on 2022-06-09 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0015_device_serial_port_exchange_parameters'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='device',
            name='serial_port_exchange_parameters',
        ),
        migrations.AddConstraint(
            model_name='device',
            constraint=models.CheckConstraint(check=models.Q(('is_active__istrue', True)), name='serial_port_exchange_parameters'),
        ),
    ]