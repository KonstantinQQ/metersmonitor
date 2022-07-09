from celery import shared_task
from importlib import import_module
from control.models import Device
from request.models import Query
import logging


@shared_task(name='Get/Set Attribute')
def pull_attribute(**kwargs):
    devices = kwargs.get('device_id', [])
    requests = kwargs.get('query_id', [])
    req_size = len(requests)
    db_logger = logging.getLogger('db')
    for dev_id in devices:
        try:
            device = Device.objects.get(pk=dev_id)
        except Device.DoesNotExist as err:
            db_logger.error(f'device_id:{dev_id} {err}')
        else:
            db_logger.info(f'device_id:{dev_id}, protocol:{device.protocol}, hub:{device.hub}, addr:{device.addr}')
            if device.is_active:
                module_name = 'interaction.protocols.' + device.protocol.name.lower()
                try:
                    module = import_module(module_name)
                except ModuleNotFoundError as err:
                    db_logger.error(f'({device.protocol.name}) {err}')
                else:
                    try:
                        clss = getattr(module, device.protocol.name)
                    except AttributeError as err:
                        db_logger.error(f'({device.protocol.name}) {err}')
                    else:
                        if req_size == 0:
                            db_logger.warning('Perform all requests from the set')
                            queries = Query.objects.filter(qset=device.qset)
                        else:
                            queries = Query.objects.filter(qset=device.qset).filter(pk__in=requests)
                        for qry in queries:
                            inst = clss(device, qry)
                            inst.exec_command()
                            del inst
                    finally:
                        del module
