# Generated by Django 4.0.5 on 2022-06-09 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0006_device_baudrate_device_bytesize_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='device',
            constraint=models.CheckConstraint(check=models.Q(('baudrate__isnull', False), ('is_portforwarding', True)), name='serial_port_exchange_parameters'),
        ),
    ]