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

import abc
import json

from influxdb import InfluxDBClient
from pvstats.pvoutput import PVOutputClient

import logging
logging.basicConfig()
_log = logging.getLogger()

class BasePVOutput():
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def publish(self, data): pass

class PVReport_pvoutput(BasePVOutput):
  def __init__(self, cfg):
    self.client = PVOutputClient(cfg['host'],
                                 cfg['key'],
                                 cfg['system_id'])

  def publish(self, data):
    self.client.add_status(data['timestamp'].strftime("%Y%m%d"), data['timestamp'].strftime("%H:%M"),
                           energy_generation = data['daily_pv_power'],
                           power_generation  = data['total_pv_power'],
                           temperature       = data['internal_temp'],
                           voltage           = (data['pv1_voltage'] + data['pv2_voltage']))



class PVReport_influxdb(BasePVOutput):
  def __init__(self, cfg):
    self.client = InfluxDBClient(cfg['host'], cfg['port'],
                                 cfg['user'], cfg['password'],
                                 cfg['db'],   ssl=cfg['ssl'],
                                 verify_ssl=cfg['verify_ssl'])

  def publish(self, data):
    # TODO
    metrics = {'measurement': 'sungrow',
               'tags':        {'location': 'Sydney'},
               'fields':      data}

    #fields  = {}
    #metrics['measurement'] = "sungrow"
    #metrics['tags']        = {'location': 'Sydney'}
    #metrics['fields']      = {'test': 10}

    #target = self.client.write_points([metrics])
    _log.debug("[INFO] Sent to InfluxDB")

class PVReport_test(BasePVOutput):
  def __init__(self, cfg):
    pass

  def publish(self, data):
    _log.debug(json.dumps(data, sort_keys=True,
                         indent=4, separators=(',', ': '),default=str))


def PVReportFactory(cfg):
  if (cfg['type'] == "test"):
    return PVReport_test(cfg)
  elif (cfg['type'] == "pvoutput"):
    return PVReport_pvoutput(cfg)
  elif (cfg['type'] == "influxdb"):
    return PVReport_influxdb(cfg)
  else:
    raise ValueError("Unable to find PVReport for {}".format(cfg['type']))


#-----------------
# Exported symbols
#-----------------
__all__ = [
  "PVReportFactory"
]
# vim: set expandtab ts=2 sw=2:
