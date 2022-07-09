# Generated by Django 4.0.5 on 2022-06-09 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0009_remove_device_serial_port_exchange_parameters_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='device',
            name='serial_port_exchange_parameters',
        ),
        migrations.AddConstraint(
            model_name='device',
            constraint=models.CheckConstraint(check=models.Q(('is_portforwarding', True), ('baudrate__isnull', False)), name='serial_port_exchange_parameters'),
        ),
    ]
