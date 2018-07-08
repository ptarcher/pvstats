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
import time

from influxdb import InfluxDBClient
from pvstats.pvoutput import PVOutputClient

#import context
import json
import paho.mqtt.client as mqtt

import logging
logging.basicConfig()
_log = logging.getLogger()

class BasePVOutput():
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def publish(self, data): pass

class PVReport_pvoutput(BasePVOutput):
  def __init__(self, cfg):
    self.samples     = []
    self.rate_limit  = int(cfg['rate_limit'])
    self.last_status = time.time()

    self.client = PVOutputClient(cfg['host'],
                                 cfg['key'],
                                 cfg['system_id'])

  def publish(self, data):
    sample = {'date':             data['timestamp'].strftime("%Y%m%d"),
              'time':             data['timestamp'].strftime("%H:%M"),
              'energy_generation':data['daily_pv_power'],
              'power_generation': data['total_pv_power'],
              'temperature':      data['internal_temp'],
              'voltage':         (data['pv1_voltage'] + data['pv2_voltage'])}

    if (time.time() - self.last_status > 3*self.rate_limit):
      # If the last successful sample was a long time ago, flush the samples
      self.samples     = []


    self.samples.append(sample)

    if (time.time() - self.last_status > self.rate_limit):
      # Last result: Date, Time & EnergyGeneration
      # Average:     PowerGeneration, Temperature & Voltage
      # Note: This asssumes all samples are sampled at the same sample rate
      d = {
        'date'             :self.samples[-1]['date'],
        'time'             :self.samples[-1]['time'],
        'energy_generation':self.samples[-1]['energy_generation'],
        'power_generation' :sum(s['power_generation'] for s in self.samples) / len(self.samples),
        'temperature'      :sum(s['temperature']      for s in self.samples) / len(self.samples),
        'voltage'          :sum(s['voltage']          for s in self.samples) / len(self.samples)
      }

      # Clear out the old results
      self.last_status = time.time()
      self.samples     = []

      # Send the new result to the server
      self.client.add_status(d['date'], d['time'],
                             energy_generation = d['energy_generation'],
                             power_generation  = d['power_generation'],
                             temperature       = d['temperature'],
                             voltage           = d['voltage'])


class PVReport_mqtt(BasePVOutput):
  def __init__(self, cfg):
    self.client = mqtt.Client()

    # Turn on user/password login
    if cfg['user']:
      self.client.username_pw_set(cfg['user'],cfg['password'])

    # Turn on TLS encryption
    if cfg['tls']:
      self.client.tls_set()

    # Connect and run the call back functions
    self.client.connect(cfg['host'],cfg['port'])
    self.client.loop_start()

    # Save config data for later
    self.topic = cfg['topic']
    self.qos   = cfg['qos']

  def publish(self, data):
    d = json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '),default=str)
    self.client.publish(self.topic, d, qos=self.qos)

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
  elif (cfg['type'] == "mqtt"):
    return PVReport_mqtt(cfg)
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
