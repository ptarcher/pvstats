#!/usr/bin/env python

# Based on xxx from yyy

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

from datetime import datetime
from decimal import *

from pymodbus.constants import Defaults
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.transaction import ModbusSocketFramer

from pvstats.pvinverter.fronius import PVInverter_Fronius
from pvstats.pvinverter.solax import PVInverter_Solax
from pvstats.pvinverter.sungrow_sg5ktl import PVInverter_SunGrow, PVInverter_SunGrowRTU
from pvstats.pvinverter.base import BasePVInverter

from random import randint

class PVInverter_Test(BasePVInverter):
  def __init__(self): pass
  def connect(self): pass
  def read(self):
    self.registers = {'timestamp':datetime.now(),
                      'daily_pv_power':Decimal('2300') + randint(0,1000),
                      'total_pv_power':Decimal('2100') + randint(0,1000),
                      'internal_temp': Decimal('41.2') + randint(0,10),
                      'pv1_voltage':   Decimal('213')  + randint(0,30),
                      'pv2_voltage':   Decimal('125')  + randint(0,20)}

  def close(self): pass

# Factory class for the PV Inverter
def PVInverterFactory(model, cfg):
  if (model == "test"):
    return PVInverter_Test()
  elif (model == "sungrow-sg5ktl" and cfg['mode'] == 'rtu'):
    return PVInverter_SunGrowRTU(cfg)
  elif (model == "sungrow-sg5ktl"):
    # Assume TCP
    return PVInverter_SunGrow(cfg)
  elif (model == "fronius"):
    # Assume TCP
    return PVInverter_Fronius(cfg)
  elif (model == "solax"):
    # Assume TCP
    return PVInverter_Solax(cfg)
  else:
    raise ValueError("Unable to find PVInverter for {}".format(model))


#-----------------
# Exported symbols
#-----------------
__all__ = [
  "PVInverterFactory"
]

# vim: set expandtab ts=2 sw=2:
