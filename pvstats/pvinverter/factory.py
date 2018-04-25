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

from pymodbus.constants import Defaults
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.transaction import ModbusSocketFramer

from pvstats.pvinverter.sungrow_sg5ktl import PVInverter_SunGrow, PVInverter_SunGrowRTU
from pvstats.pvinverter.base import BasePVInverter

class PVInverter_Test(BasePVInverter):
  def __init__(self):
    self.registers = {'timestamp':datetime.now(),
                      'daily_pv_power':2300,
                      'total_pv_power':2100,
                      'internal_temp': 41.2,
                      'pv1_voltage':213,
                      'pv2_voltage':125}

  def connect(self): pass
  def read(self): pass
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
  else:
    raise ValueError("Unable to find PVInverter for {}".format(model))


#-----------------
# Exported symbols
#-----------------
__all__ = [
  "PVInverterFactory"
]

# vim: set expandtab ts=2 sw=2:
