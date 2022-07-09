from interaction.protocols.baseprotocol import BaseProtocol
from datetime import datetime
import struct


class Modbus(BaseProtocol):

    def form_request(self):
        addr = self.dev.addr
        self.mess += addr.to_bytes(1, 'big')
        func = self.qry.func
        self.mess += bytes.fromhex(func)
        req = self.qry.req
        self.mess += bytes.fromhex(req)
        self.mess += self.calc_crc(self.mess)

    def response_processing(self):
        if self.check_response():
            func = getattr(self, 'resp_' + self.qry.handler, None)
            if func is not None:
                func()
            else:
                self.db_logger.warning(f'Method resp_{self.qry.handler} for class {self.__class__.__name__} not found')
        else:
            self.db_logger.error(f'Device {self.dev.id} request {self.qry.id}. Response error')

    def calc_crc(self, data: bytes) -> bytes:
        crc = 0xFFFF
        poly = 0xA001
        for byte in data:
            crc ^= byte
            for _ in range(8):
                temp = crc & 0x0001
                crc >>= 1
                if temp:
                    crc ^= poly

        crc16modbus = crc.to_bytes(2, 'little')
        return crc16modbus

    def check_response(self) -> bool:
        check = False
        lenresp = len(self.resp)
        if lenresp > 2:
            check = self.calc_crc(self.resp[:lenresp-2]) == self.resp[-2:]
        return check

    def rounding(self, factor):
        return len(str(factor).split('.')[1]) if (factor - int(factor)) != 0 else 0

    def resp_uint4(self):
        res = self.resp[3:3 + self.resp[2]]
        value = struct.unpack('>I', res[2:] + res[:2])[0]
        if self.qry.factor is not None and self.qry.factor != 1.0:
            value *= self.qry.factor
            value = round(value, self.rounding(self.qry.factor))
        self.tosave = str(value)

    def resp_sint2(self):
        res = self.resp[3:3 + self.resp[2]]
        value = struct.unpack('>h', res)[0]
        if self.qry.factor is not None and self.qry.factor != 1.0:
            value *= self.qry.factor
            value = round(value, self.rounding(self.qry.factor))
        self.tosave = str(value)

    def resp_datetime4(self):
        res = self.resp[3:3 + self.resp[2]]
        value = struct.unpack('>I', res[2:] + res[:2])[0]
        self.tosave = datetime.utcfromtimestamp(value).strftime('%d.%m.%Y %H:%M:%S')
