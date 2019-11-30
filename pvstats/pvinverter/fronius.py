#!/usr/bin/env python

# Copyright 2019 Paul Archer
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

import logging
_logger = logging.getLogger(__name__)

class PVInverter_Fronius(BasePVInverter):
  def __init__(self, cfg, **kwargs):
    self.url = "http://{}:{}/solar_api/v1/GetInverterRealtimeData.cgi?Scope=Device&DeviceID=1&DataCollection=CommonInverterData".format(cfg["host"],cfg["port"])
    self.http_timeout_sec = cfg.get("http_timeout_sec", 10)

  def connect(self):
    pass

  def close(self):
    pass

  def read(self):
    """Reads the PV inverters status"""

    # Dummy data
    response = """
{
  "Body": {
    "Data": {
      "DAY_ENERGY": {
        "Unit": "Wh",
        "Value": 55550
      },
      "DeviceStatus": {
        "ErrorCode": 567,
        "LEDColor": 2,
        "LEDState": 0,
        "MgmtTimerRemainingTime": -1,
        "StateToReset": true,
        "StatusCode": 7
      },
      "FAC": {
        "Unit": "Hz",
        "Value": 50.03
      },
      "IAC": {
        "Unit": "A",
        "Value": 16.27
      },
      "IDC": {
        "Unit": "A",
        "Value": 9.74
      },
      "PAC": {
        "Unit": "W",
        "Value": 4051
      },
      "TOTAL_ENERGY": {
        "Unit": "Wh",
        "Value": 14272110
      },
      "UAC": {
        "Unit": "V",
        "Value": 245.6
      },
      "UDC": {
        "Unit": "V",
        "Value": 407.8
      },
      "YEAR_ENERGY": {
        "Unit": "Wh",
        "Value": 2512712
      }
    }
  },
  "Head": {
    "RequestArguments": {
      "DataCollection": "CommonInverterData",
      "DeviceClass": "Inverter",
      "DeviceId": "1",
      "Scope": "Device"
    },
    "Status": {
      "Code": 0,
      "Reason": "",
      "UserMessage": ""
    },
    "Timestamp": "2019-02-10T17:23:28+11:00"
  }
}
"""

    response = urllib2.urlopen(self.url, None, self.http_timeout_sec).read()
    data = json.loads(response)
    d = json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '),default=str)
    print d

    self.registers = {'timestamp':     datetime.strptime(data['Head']['Timestamp'][:-6], "%Y-%m-%dT%H:%M:%S"),
                      'daily_pv_power':Decimal(data['Body']['Data']['DAY_ENERGY']['Value']),
                      'total_pv_power':Decimal(data['Body']['Data']['PAC']['Value']),
                      #'internal_temp': Decimal(data['Body']['Data']['T_AMBIENT']['Value']).quantize(Decimal('.1')),
                      'internal_temp': Decimal(0),
                      'pv1_voltage':   Decimal(data['Body']['Data']['UDC']['Value']),
                      'pv2_voltage':   Decimal('0')}

    print self.registers


#-----------------
# Exported symbols
#-----------------
__all__ = [
  "PVInverter_Fronius"
]

# vim: set expandtab ts=2 sw=2:
