from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from request.models import QuerySet


class DeviceType(models.Model):
    typename = models.CharField(unique=True, max_length=400, verbose_name='Наименование')
    shortname = models.CharField(unique=True, max_length=40, verbose_name='Краткое наименование')

    class Meta:
        managed = True
        db_table = 'devicetypes'
        verbose_name_plural = 'Типы устройств'
        verbose_name = 'Тип'
        ordering = ['shortname']

    def __str__(self):
        return self.shortname


class Hub(models.Model):
    host = models.CharField(null=False, blank=False, max_length=40, verbose_name='Адрес')
    port = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(65535)],
                                       verbose_name='Порт')

    class Meta:
        managed = True
        db_table = 'hubs'
        verbose_name_plural = 'Контроллеры УСПД'
        verbose_name = 'Контроллер'
        unique_together = ('host', 'port')
        index_together = ('host', 'port')
        ordering = ('host', 'port')

    def __str__(self):
        return f'{self.host}:{self.port}'


class Protocol(models.Model):
    name = models.CharField(unique=True, max_length=40, verbose_name='Наименование')

    class Meta:
        managed = True
        db_table = 'protocols'
        verbose_name_plural = 'Протоколы связи'
        verbose_name = 'Протокол'
        ordering = ['name']

    def __str__(self):
        return self.name


class Device(models.Model):
    RATE = (
        (2400, '2400'),
        (4800, '4800'),
        (9600, '9600'),
        (19200, '19200'),
        (38400, '38400'),
        (57600, '57600'),
        (115200, '115200')
    )
    PAR = (
        ('N', 'Нет'),
        ('E', 'Четный'),
        ('O', 'Нечетный')
    )
    LDATA = (
        (7, '7'),
        (8, '8')
    )
    STOPS = (
        (1, '1'),
        (2, '2')
    )
    id = models.BigAutoField(primary_key=True, verbose_name='ИН')
    type = models.ForeignKey(DeviceType, models.DO_NOTHING, verbose_name='Тип')
    model = models.CharField(null=False, blank=False, max_length=40, verbose_name='Модель')
    mk = models.CharField(unique=True, max_length=40, verbose_name='Заводской №')
    protocol = models.ForeignKey(Protocol, models.DO_NOTHING, verbose_name='Протокол')
    hub = models.ForeignKey(Hub, models.DO_NOTHING, verbose_name='Контроллер')
    addr = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)],
                                       verbose_name='Адрес')
    qset = models.ForeignKey(QuerySet, models.DO_NOTHING, verbose_name='Набор запросов')
    is_active = models.BooleanField(default=True, verbose_name='Активное')
    is_portforwarding = models.BooleanField(default=False, verbose_name='Проброс порта')
    baudrate = models.PositiveIntegerField(null=True, choices=RATE, verbose_name='Скорость бит/с')
    parity = models.CharField(null=True, choices=PAR, max_length=1, verbose_name='Контроль четности')
    bytesize = models.PositiveSmallIntegerField(null=True, choices=LDATA, verbose_name='Длина слова бит')
    stopbits = models.PositiveSmallIntegerField(null=True, choices=STOPS, verbose_name='Стоповые биты')
    fn = models.CharField(max_length=400, blank=True, null=True, verbose_name='Примечание')

    class Meta:
        managed = True
        db_table = 'devices'
        verbose_name_plural = 'Список устройств'
        verbose_name = 'Устройство'
        unique_together = ('hub', 'addr')
        index_together = ('hub', 'addr')
        ordering = ('hub', 'addr')

    def __str__(self):
        return f'{self.type} {self.model} №{self.mk}'
