#!/usr/bin/env python

# Copyright 2018 Paul Archer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pvstats.pvinverter.base import BasePVInverter

from pymodbus.constants import Defaults
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.transaction import ModbusSocketFramer
from pymodbus.exceptions import ModbusIOException
from pymodbus.payload import BinaryPayloadDecoder
from datetime import datetime
from time import sleep

import serial.rs485

from decimal import *
getcontext().prec = 9

import logging
_logger = logging.getLogger(__name__)

_register_map = {
  'input': {
    5000:  {'name': '5000',                       'scale': Decimal(1),   'units': 'W'},
    5001:  {'name': '5001',                       'scale': Decimal(1),   'units': 'W'},
    5002:  {'name': '5002',                       'scale': Decimal(1),   'units': 'W'},
    5003:  {'name': 'daily_pv_power',             'scale': Decimal(100),   'units': 'W'},
    5004:  {'name': 'lifetime_pv_power',          'scale': Decimal(1),     'units': 'kW'},
    5005:  {'name': '5005',                       'scale': Decimal(1),   'units': 'W'},
    5006:  {'name': '5006',                       'scale': Decimal(1),   'units': 'W'},
    5007:  {'name': '5007',                       'scale': Decimal(1),   'units': 'W'},
    5008:  {'name': 'internal_temp',              'scale': Decimal('0.1'), 'units': 'C'},
    5009:  {'name': '5009',                       'scale': Decimal(1),   'units': 'W'},
    5010:  {'name': '5010',                       'scale': Decimal(1),   'units': 'W'},
    5011:  {'name': 'pv1_voltage',                'scale': Decimal('0.1'), 'units': 'V'},
    5012:  {'name': 'pv1_current',                'scale': Decimal('0.1'), 'units': 'A'},
    5013:  {'name': 'pv2_voltage',                'scale': Decimal('0.1'), 'units': 'V'},
    5014:  {'name': 'pv2_current',                'scale': Decimal('0.1'), 'units': 'A'},
    5015:  {'name': '5015',                       'scale': Decimal(1),   'units': 'W'},
    5016:  {'name': '5016',                       'scale': Decimal(1),   'units': 'W'},
    5017:  {'name': 'total_pv_power',             'scale': Decimal(1),     'units': 'W'},
    5018:  {'name': '5018',                       'scale': Decimal(1),   'units': 'W'},
    5019:  {'name': 'grid_voltage',               'scale': Decimal('0.1'), 'units': 'V'},
    5020:  {'name': '5020',                       'scale': Decimal(1),   'units': 'W'},
    5021:  {'name': '5021',                       'scale': Decimal(1),   'units': 'W'},
    5022:  {'name': 'inverter_current',           'scale': Decimal('0.1'), 'units': 'A'},
    5023:  {'name': '5023',                       'scale': Decimal(1),   'units': 'W'},
    5024:  {'name': '5024',                       'scale': Decimal(1),   'units': 'W'},
    5025:  {'name': '5025',                       'scale': Decimal(1),   'units': 'W'},
    5026:  {'name': '5026',                       'scale': Decimal(1),   'units': 'W'},
    5027:  {'name': '5027',                       'scale': Decimal(1),   'units': 'W'},
    5028:  {'name': '5028',                       'scale': Decimal(1),   'units': 'W'},
    5029:  {'name': '5029',                       'scale': Decimal(1),   'units': 'W'},
    5030:  {'name': '5030',                       'scale': Decimal(1),   'units': 'W'},
    5031:  {'name': '5031',                       'scale': Decimal(1),   'units': 'W'},
    5032:  {'name': '5032',                       'scale': Decimal(1),   'units': 'W'},
    5033:  {'name': '5033',                       'scale': Decimal(1),   'units': 'W'},
    5034:  {'name': '5034',                       'scale': Decimal(1),   'units': 'W'},
    5035:  {'name': '5035',                       'scale': Decimal(1),   'units': 'W'},
    5036:  {'name': 'grid_frequency',             'scale': Decimal('0.1'), 'units': 'Hz'},
    5037:  {'name': '5037',                       'scale': Decimal(1),   'units': 'W'},
    5038:  {'name': '5038',                       'scale': Decimal(1),   'units': 'W'},
    5039:  {'name': '5039',                       'scale': Decimal(1),   'units': 'W'},
    5040:  {'name': '5040',                       'scale': Decimal(1),   'units': 'W'},
    5041:  {'name': '5041',                       'scale': Decimal(1),   'units': 'W'},
    5042:  {'name': '5042',                       'scale': Decimal(1),   'units': 'W'},
    5043:  {'name': '5043',                       'scale': Decimal(1),   'units': 'W'},
    5044:  {'name': '5044',                       'scale': Decimal(1),   'units': 'W'},
    5045:  {'name': '5045',                       'scale': Decimal(1),   'units': 'W'},
    5046:  {'name': '5046',                       'scale': Decimal(1),   'units': 'W'},
    5047:  {'name': '5047',                       'scale': Decimal(1),   'units': 'W'},
    13001: {'name': 'running_state',              'scale': Decimal('0.1'), 'units': '?'},
    13002: {'name': 'daily_pv_energy_10',         'scale': Decimal('0.1'), 'units': 'Wh'},
    13003: {'name': 'total_pv_energy_10',         'scale': Decimal('0.1'), 'units': 'Wh'},
    13004: {'name': '13004',                      'scale': Decimal('0.1'), 'units': 'Wh'},
    13005: {'name': 'daily_export_energy_10',     'scale': Decimal('0.1'), 'units': 'Wh'},
    13006: {'name': 'total_export_energy_10',     'scale': Decimal('0.1'), 'units': 'Wh'},
    13007: {'name': '13007',                      'scale': Decimal('0.1'), 'units': 'Wh'},
    13008: {'name': 'load_power',                 'scale': Decimal('1'),   'units': 'W'},
    13009: {'name': '13009',                      'scale': Decimal('1'),   'units': 'W'},
    13010: {'name': 'export_power',               'scale': Decimal('1'),   'units': 'W'},
    13011: {'name': 'grid_import_or_export',      'scale': Decimal('1'),   'units': '?'},
    13012: {'name': 'daily_charge_energy_10',     'scale': Decimal('0.1'), 'units': 'Wh'},
    13013: {'name': 'total_charge_energy_10',     'scale': Decimal('0.1'), 'units': 'Wh'},
    13014: {'name': '13014',                      'scale': Decimal('0.1'), 'units': 'Wh'},
    13015: {'name': 'co2_emission_reduction',     'scale': Decimal('0.1'), 'units': 'Kg CO2'},
    13016: {'name': '13016',                      'scale': Decimal('0.1'), 'units': 'Kg CO2'},
    13017: {'name': 'daily_use_energy_10',        'scale': Decimal('0.1'), 'units': 'Wh'},
    13018: {'name': 'total_use_energy_10',        'scale': Decimal('0.1'), 'units': 'Wh'},
    13019: {'name': '13019',                      'scale': Decimal('0.1'), 'units': 'Wh'},
    13020: {'name': 'battery_voltage_10',         'scale': Decimal('0.1'), 'units': 'V'},
    13021: {'name': 'battery_current_10',         'scale': Decimal('0.1'), 'units': 'A'},
    13022: {'name': 'battery_power',              'scale': Decimal('1'),   'units': 'W'},
    13023: {'name': 'battery_level_10',           'scale': Decimal('0.1'), 'units': '%'},
    13024: {'name': 'battery_health_10',          'scale': Decimal('0.1'), 'units': '%'},
    13025: {'name': 'battery_temp_10',            'scale': Decimal('0.1'), 'units': '°C'},
    13026: {'name': 'daily_discharge_energy_10',  'scale': Decimal('0.1'), 'units': 'Wh'},
    13027: {'name': 'total_discharge_energy_10',  'scale': Decimal('0.1'), 'units': 'Wh'},
    13028: {'name': '13028',                      'scale': Decimal('0.1'), 'units': 'Wh'},
    13029: {'name': 'use_power',                  'scale': Decimal('0.1'), 'units': 'W'},
    13030: {'name': '13030',                      'scale': Decimal('0.1'), 'units': 'W'},
    13031: {'name': 'inverter_current_10',        'scale': Decimal('0.1'), 'units': 'A'},
    13032: {'name': '13032',                      'scale': Decimal('0.1'), 'units': 'A'},
    13033: {'name': '13033',                      'scale': Decimal('0.1'), 'units': 'A'},
    13034: {'name': 'pv_power',                   'scale': Decimal('0.1'), 'units': 'W'},
    13035: {'name': '13035',                      'scale': Decimal('0.1'), 'units': 'W'},
    13036: {'name': '13036',                      'scale': Decimal('0.1'), 'units': 'W'},
    13037: {'name': '13037',                      'scale': Decimal('0.1'), 'units': 'W'},
    13038: {'name': '13038',                      'scale': Decimal('0.1'), 'units': 'W'},
  },

  'holding': {
    5000:  {'name': 'date_year',         'scale': 1,              'units': 'year'},
    5001:  {'name': 'date_month',        'scale': 1,              'units': 'month'},
    5002:  {'name': 'date_day',          'scale': 1,              'units': 'day'},
    5003:  {'name': 'date_hour',         'scale': 1,              'units': 'hour'},
    5004:  {'name': 'date_minute',       'scale': 1,              'units': 'minute'},
    5005:  {'name': 'date_second',       'scale': 1,              'units': 'second'},
  }
}

class PVInverter_SunGrow_sh5k_20(BasePVInverter):
  def __init__(self, cfg, **kwargs):
    super(PVInverter_SunGrow_sh5k_20, self).__init__()
    self.cfg = cfg
    self.init_modbus_client()

  def init_modbus_client(self):
    self.client = ModbusTcpClient(self.cfg['host'],          port=self.cfg['port'],
                                  framer=ModbusSocketFramer, timeout=5,
                                  RetryOnEmpty=True,         retries=5)

  def connect(self):
    self.client.connect()

  def close(self):
    self.client.close()

  def read(self):
    """Reads the PV inverters status"""

    # Read holding and input registers in groups aligned on the 100
    for func in _register_map:
      start = -1
      for k in sorted(_register_map[func].keys()):
        group  = int(k) - int(k) % 100
        if (start < group):
          # Wait 500ms between modbus reads as per https://c.tjhowse.com/misc/SolarInfo%20Logger%20User%20Manual.pdf page 89
          sleep(0.5)
          self._load_registers(func, group, 100)
          start = group + 100

    # Manually calculate the power and the timestamps
    self.registers['pv1_power'] = round(self.registers['pv1_current'] * self.registers['pv1_voltage'])
    self.registers['pv2_power'] = round(self.registers['pv2_current'] * self.registers['pv2_voltage'])
    self.registers['timestamp'] = datetime(self.registers['date_year'],   self.registers['date_month'],
                                           self.registers['date_day'],    self.registers['date_hour'],
                                           self.registers['date_minute'], self.registers['date_second'])

    floaty = {}
    for key in self.registers.keys():
      try:
        floaty[key] = float(self.registers[key])
      except:
        floaty[key] = self.registers[key]
    self.registers = floaty


  def _load_registers(self,func,start,count=100):
    try:
      if func == 'input':
        rq = self.client.read_input_registers(start, count, unit=0x01)
      elif func == 'holding':
        # Holding registers need an offset
        start = start - 1
        rq = self.client.read_holding_registers(start, count, unit=0x01)
      else:
        raise Exception("Unknown register type: {}".format(type))


      if isinstance(rq, ModbusIOException):
        _logger.error("Error: {}".format(rq))
        self.init_modbus_client()
        raise Exception("ModbusIOException")

      for x in range(0, count):
        key  = start + x + 1
        val  = rq.registers[x]

        if key in _register_map[func]:
          reg = _register_map[func][key]
          self.registers[reg['name']] = val * reg['scale']


    except Exception as err:
      _logger.error("Error: %s" % err)
      _logger.debug("{}, start: {}, count: {}".format(type, start, count))
      raise

class PVInverter_SunGrow_sh5k_20RTU(PVInverter_SunGrow_sh5k_20):
  def __init__(self, cfg, **kwargs):
    super(PVInverter_SunGrow_sh5k_20, self).__init__()

    # Configure the Modbus Remote Terminal Unit settings
    self.client = ModbusSerialClient(method='rtu', port=cfg['dev'], timeout=0.5,
                                     stopbits = 1, bytesize =8, parity='N', baudrate=9600)

  def connect(self):
    # Connect then configure the port
    self.client.connect()

    # Configure the RS485 port - This seems not needed
    #rs485_mode = serial.rs485.RS485Settings(delay_before_tx = 0, delay_before_rx = 0,
    #                                        rts_level_for_tx=True, rts_level_for_rx=False,
    #                                        loopback=False)
    #self.client.socket.rs485_mode = rs485_mode


#-----------------
# Exported symbols
#-----------------
__all__ = [
  "PVInverter_SunGrow_sh5k_20", "PVInverter_SunGrow_sh5k_20RTU"
]

# vim: set expandtab ts=2 sw=2:
