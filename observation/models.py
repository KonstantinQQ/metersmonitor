from django.db import models
from control.models import Device
from request.models import Query


class Quality(models.Model):
    dev = models.ForeignKey(Device, models.DO_NOTHING, verbose_name='Устройство')
    qry = models.ForeignKey(Query, models.DO_NOTHING, verbose_name='Атрибут')
    value = models.CharField(max_length=30, default=None, verbose_name='Значение')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Метка')

    class Meta:
        managed = True
        db_table = 'attributes'
        verbose_name = 'Значение'
        verbose_name_plural = 'Значения атрибутов'
        index_together = ('timestamp', 'dev')
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.qry}:{self.value}'
