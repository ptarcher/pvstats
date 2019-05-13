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
from datetime import datetime
from decimal import *
import urllib2
import json

getcontext().prec = 9

import logging
_logger = logging.getLogger(__name__)


class PVInverter_Solax(BasePVInverter):
  def __init__(self, cfg, **kwargs):
    self.url = "http://{}:{}/api/realTimeData.htm".format(cfg["host"],cfg["port"])

    
  def connect(self):
    pass

  def close(self):
    pass

  def read(self):
    """Reads the PV inverters status"""

    response = urllib2.urlopen(self.url).read().decode("utf-8").replace(",,",",0,").replace(",,",",0,")
    data = json.loads(response)
    #print json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '),default=str)

    self.registers = {'timestamp':     datetime.now(),
                      'daily_pv_power':Decimal(data['Data'][8]*1000),
                      'total_pv_power':Decimal(data['Data'][6]),
                      'internal_temp': Decimal(data['Data'][7]),
                      'pv1_voltage':   Decimal(data['Data'][2]).quantize(Decimal('.1')),
                      'pv2_voltage':   Decimal(data['Data'][3]).quantize(Decimal('.1'))}


#-----------------
# Exported symbols
#-----------------
__all__ = [
  "PVInverter_Solax"
]

# vim: set expandtab ts=2 sw=2:
