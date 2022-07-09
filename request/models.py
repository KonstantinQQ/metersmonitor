from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


def validate_len_even(value):
    if len(value) % 2 == 0:
        return value
    else:
        raise ValidationError('Длина строки в 16-ричном виде должна быть четной')


class QuerySet(models.Model):
    setname = models.CharField(unique=True, max_length=50, verbose_name='Наименование')
    fn = models.CharField(max_length=400, blank=True, null=True, verbose_name='Примечание')

    class Meta:
        managed = True
        db_table = 'querysets'
        verbose_name_plural = 'Наборы запросов'
        verbose_name = 'Набор'
        ordering = ['setname']

    def __str__(self):
        return self.setname


class Query(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='ИН')
    attribute = models.CharField(null=False, blank=False, max_length=50, verbose_name='Свойство')
    qset = models.ForeignKey(QuerySet, models.DO_NOTHING, verbose_name='Набор')
    func = models.CharField(null=False, blank=False, max_length=4,
                            validators=[RegexValidator('^[A-Fa-f0-9]+$'), validate_len_even], verbose_name='Команда')
    req = models.CharField(null=False, blank=False, max_length=40,
                           validators=[RegexValidator('^[A-Fa-f0-9]+$'), validate_len_even], verbose_name='Данные')
    unit = models.CharField(null=True, blank=True, max_length=40, verbose_name='Ед. изм.')
    factor = models.FloatField(null=True, blank=True, verbose_name='Множитель')
    handler = models.CharField(null=False, blank=False, max_length=40, verbose_name='Обработчик')
    fn = models.CharField(max_length=160, blank=True, null=True, verbose_name='Примечание')

    class Meta:
        managed = True
        db_table = 'queries'
        verbose_name_plural = 'Запросы'
        verbose_name = 'Запрос'
        unique_together = ('qset', 'attribute')
        index_together = ('qset', 'attribute')
        ordering = ('qset', 'attribute')

    def __str__(self):
        return f'{self.qset}:{self.attribute}'
