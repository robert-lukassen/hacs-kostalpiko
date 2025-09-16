import socket
import datetime
from typing import Optional, Tuple, List
from dataclasses import dataclass

@dataclass 
class KostalPikoInfo:
    serial_no: str = 'unknown'
    typ : str = 'unknown'


@dataclass
class KostalPikoReport:
    connected: bool = False
    state: int = 0
    total_yield: int = 0
    daily_yield: int = 0

    dc_volt : Tuple[int, int, int] = (0,0,0)
    dc_current : Tuple[int, int, int] = (0,0,0)
    dc_power : Tuple[int, int, int] = (0,0,0)
    ac_volt : Tuple[int, int, int] = (0,0,0)
    ac_current : Tuple[int, int, int] = (0,0,0)
    ac_power : Tuple[int, int, int] = (0,0,0)

    def __repr__(self):
        return f'{self.connect};{self.state};{self.total_yield};{self.daily_yield};' \
               f'{self.dc_volt[0]};{self.dc_volt[1]};{self.dc_volt[2]};' \
               f'{self.dc_current[0]};{self.dc_current[1]};{self.dc_current[2]};' \
               f'{self.dc_power[0]};{self.dc_power[1]};{self.dc_power[2]};' \
               f'{self.ac_volt[0]};{self.ac_volt[1]};{self.ac_volt[2]};' \
               f'{self.ac_current[0]};{self.ac_current[1]};{self.ac_current[2]};' \
               f'{self.ac_power[0]};{self.ac_power[1]};{self.ac_power[2]}'

class KostalPiko:
    def __init__(self, ip_address: str):
        self._inet_addr = ip_address
        self._sock = None
        self._query_times = {}

    def _is_connected(self) -> bool:
        return self._sock

    def _disconnect(self):
        if not self._is_connected():
            return

        self._sock.close()
        self._sock = None

    def _connect(self):
        if self._is_connected():
            return

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((self._inet_addr, 81))


    def _has_valid_header(self, data: bytes) -> bool:
        return data and data.startswith(b'\xe2\xff\x03\xff\x00')

    def _query(self, request: bytes, response_length: int) -> Optional[bytes]:
        if not self._is_connected():
            self._connect()

        if not self._is_connected():
            return None

        self._sock.send(request)
        data = self._sock.recv(response_length)
        if not self._has_valid_header(data):
            data = None
        return data

    def _fetch_state(self) -> int:
        state_response = self._query(b'\x62\xff\x03\xff\x00\x57\x46\x00', 15)
        if state_response:
            self._state = int.from_bytes(state_response[5:6], 'little')
            return self._state
        return 0

    def _fetch_total_yield(self) -> int:
        response = self._query(b'\x62\xff\x03\xff\x00\x45\x58\x00', 11)
        if response:
            self._total_yield = int.from_bytes(response[5:9], 'little')
            return self._total_yield
        return 0

    def _fetch_daily_yield(self) -> int:
        response = self._query(b'\x62\xff\x03\xff\x00\x9d\x00\x00', 11)
        if response:
            return int.from_bytes(response[5:9], 'little')
        return 0

    def _fetch_details(self) -> List[int]:
        response = self._query(b'\x62\xff\x03\xff\x00\x43\x5a\x00', 73)
        if response:
            return [ int.from_bytes(response[n:n+2], 'little') for n in range(5, 57, 2) ]
        return 0

    def info(self) -> KostalPikoInfo:
        info = KostalPikoInfo()
        return info

    def report(self) -> KostalPikoReport:
        rep = KostalPikoReport()

        self._connect()
        if self._is_connected:
            rep.connected = True
            rep.state = self._fetch_state()
            rep.total_yield = self._fetch_total_yield()
            rep.daily_yield = self._fetch_daily_yield()
            if rep.state:
                details = self._fetch_details()
                if len(details) == 18:
                    rep.dc_volt = (details[0], details[3], details[6])
                    rep.dc_current = (details[1], details[4], details[7])
                    rep.dc_power = (details[2], details[5], details[8])
                    rep.ac_volt = (details[9], details[12], details[15])
                    rep.ac_current = (details[10], details[13], details[16])
                    rep.ac_power = (details[11], details[14], details[17])
            self._disconnect()

        return rep
