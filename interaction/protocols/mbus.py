from interaction.protocols.baseprotocol import BaseProtocol
import struct


class Mbus(BaseProtocol):

    def form_request(self):
        addr = self.dev.addr
        func = self.qry.func
        self.mess += bytes.fromhex(func)
        self.mess += addr.to_bytes(1, 'big')
        self.mess += self.calc_crc(self.mess)
        self.mess = bytes.fromhex('10') + self.mess + bytes.fromhex('16')

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
        crc = 0
        for byte in data:
            crc += byte
        crc = crc % 256
        crc8 = crc.to_bytes(1, 'big')
        return crc8

    def check_response(self) -> bool:
        check = False
        lenresp = len(self.resp)
        if lenresp > 6:
            check = self.calc_crc(self.resp[4:-2]) == self.resp[-2:-1]
        return check

    def rounding(self, factor):
        return len(str(factor).split('.')[1]) if (factor - int(factor)) != 0 else 0

    def resp_dummy(self):
        pass

    def resp_sint2(self):
        sub = bytes.fromhex(self.qry.req)
        pos = self.resp.find(sub)
        if pos >= 0:
            dpos = pos + len(sub)
            value = struct.unpack('<h', self.resp[dpos:dpos + 2])[0]
            if self.qry.factor is not None and self.qry.factor != 1.0:
                value *= self.qry.factor
                value = round(value, self.rounding(self.qry.factor))
            self.tosave = str(value)
        else:
            self.db_logger.error(f'Device {self.dev.id} request {self.qry.id}. No data')

    def resp_uint4(self):
        sub = bytes.fromhex(self.qry.req)
        pos = self.resp.find(sub)
        if pos >= 0:
            dpos = pos + len(sub)
            value = struct.unpack('<I', self.resp[dpos:dpos + 4])[0]
            if self.qry.factor is not None and self.qry.factor != 1.0:
                value *= self.qry.factor
                value = round(value, self.rounding(self.qry.factor))
            self.tosave = str(value)
        else:
            self.db_logger.error(f'Device {self.dev.id} request {self.qry.id}. No data')
