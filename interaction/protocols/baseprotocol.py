from abc import ABCMeta, abstractmethod
import socket
import logging
import os
import subprocess
import serial
from django.conf import settings
from random import randint
from time import sleep
from observation.models import Quality


class BaseProtocol(metaclass=ABCMeta):
    def __init__(self, dev, qry):
        self.dev = dev
        self.qry = qry
        self.mess = bytes()
        self.resp = bytes()
        self.tosave = ''
        self.db_logger = logging.getLogger('db')

    def exec_command(self):
        self.form_request()
        self.send_request()
        self.response_processing()
        if self.tosave:
            Quality.objects.create(dev=self.dev, qry=self.qry, value=self.tosave)

    def send_request(self):
        if self.dev.is_portforwarding:
            socat = getattr(settings, 'SOCAT_PATH', None)
            if socat:
                client_port = f'{self.dev.hub}'
                dirdev = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'dev')
                while True:
                    sport = 'ttyNET' + str(randint(0, 127))
                    if sport not in os.listdir(dirdev):
                        break
                device_port = os.path.join(dirdev, sport)
                cmd = [socat, 'pty,link=%s,waitslave' % device_port, 'tcp:%s' % client_port]
                try:
                    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                except (OSError, EnvironmentError, ValueError) as err:
                    self.db_logger.error(f'{err}')
                else:
                    sleep(1)
                    try:
                        vserial = serial.serial_for_url(device_port, do_not_open=True)
                    except serial.SerialException as err:
                        self.db_logger.error(f'{err}')
                    else:
                        vserial.baudrate = self.dev.baudrate
                        vserial.parity = self.dev.parity
                        vserial.bytesize = self.dev.bytesize
                        vserial.stopbits = self.dev.stopbits
                        vserial.timeout = getattr(settings, 'SERIAL_PORT_TIMEOUT', 1)
                        self.db_logger.info(f'Параметры порта: {vserial.baudrate}, {vserial.parity}, '
                                            f'{vserial.bytesize}, {vserial.stopbits}')
                        try:
                            vserial.open()
                        except serial.SerialException as err:
                            self.db_logger.error(f'{err}')
                        else:
                            vserial.write(self.mess)
                            sleep(1)
                            self.db_logger.info(f'Device {self.dev.id} request {self.qry.id}. '
                                                f'Запрос {self.mess.hex()}')
                            self.resp = vserial.read(1024)
                            self.db_logger.info(f'Device {self.dev.id} request {self.qry.id}. '
                                                f'Получен ответ {self.resp.hex()}')
                            vserial.close()
                    finally:
                        proc.terminate()
            else:
                self.db_logger.error(f'Device {self.dev.id}. SOCAT_PATH is none')
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            try:
                sock.connect((self.dev.hub.host, self.dev.hub.port))
            except socket.error as err:
                self.db_logger.error(f'Connection to {self.dev.hub.host}:{self.dev.hub.port} not successful: {err}')
            else:
                sock.send(self.mess)
                self.db_logger.info(f'Device {self.dev.id} request {self.qry.id}. Запрос {self.mess.hex()}')
                try:
                    self.resp = sock.recv(1024)
                except socket.error as err:
                    self.db_logger.error(f'Device {self.dev}:{self.dev.addr} not responding: {err}')
                else:
                    self.db_logger.info(f'Device {self.dev.id} request {self.qry.id}. Получен ответ {self.resp.hex()}')
                finally:
                    sock.shutdown(socket.SHUT_RDWR)
                    sock.close()

    @abstractmethod
    def form_request(self):
        pass

    @abstractmethod
    def response_processing(self):
        pass

#    @abstractmethod
#    def init_exchange(self):
#        pass
