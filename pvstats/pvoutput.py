#!/usr/bin/env python

# Based on xxx from yyy
#
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

import urllib
import httplib

class PVOutputClient():
	def __init__(self, host, api_key, system_id):
		self.host = host
		self.api_key = api_key
		self.system_id = system_id

	def add_output(self, date, generated, exported=None, peak_power=None, peak_time=None, condition=None,
			min_temperature=None, max_temperature=None, comments=None, import_peak=None, import_offpeak=None, import_shoulder=None):
		"""
		Uploads end of day output information
		"""
		path = '/service/r1/addoutput.jsp'
		params = {
				'd': date,
				'g': generated
				}
		if exported:
			params['e'] = exported
		if peak_power:
			params['pp'] = peak_power
		if peak_time:
			params['pt'] = peak_time
		if condition:
			params['cd'] = condition
		if min_temperature:
			params['tm'] = min_temperature
		if max_temperature:
			params['tx'] = max_temperature
		if comments:
			params['cm'] = comments
		if import_peak:
			params['ip'] = import_peak
		if import_offpeak:
			params['op'] = import_offpeak
		if import_shoulder:
			params['is'] = import_shoulder

		response = self.make_request('POST', path, params)

		if response.status == 400:
			raise ValueError(response.read())
		if response.status != 200:
			raise StandardError(response.read())

	def add_status(self, date, time, energy_generation=None, power_generation=None, energy_consumption=None, power_consumption=None, temperature=None, voltage=None, cumulative=False):
		"""
		Uploads live output data
		"""
		path = '/service/r2/addstatus.jsp'
		params = {
				'd': date,
				't': time
				}
		if energy_generation:
			params['v1'] = energy_generation
		if power_generation:
			params['v2'] = power_generation
		if energy_consumption:
			params['v3'] = energy_consumption
		if power_consumption:
			params['v4'] = power_consumption
		if temperature:
			params['v5'] = temperature
		if voltage:
			params['v6'] = voltage
		if cumulative:
			params['c1'] = 1
		params = urllib.urlencode(params)

		response = self.make_request('POST', path, params)

		if response.status == 400:
			raise ValueError(response.read())
		if response.status != 200:
			raise StandardError(response.read())

	def get_status(self, date=None, time=None):
		"""
		Retrieves status information
		"""
		path = '/service/r2/getstatus.jsp'
		params = {}
		if date:
			params['d'] = date
		if time:
			params['t'] = time
		params = urllib.urlencode(params)

		response = self.make_request("GET", path, params)

		if response.status == 400:
			raise ValueError(response.read())
		if response.status != 200:
			raise StandardError(response.read())

		rsp = response.read().split(",")
		return {'date':rsp[0],'time':rsp[1],'energy_generation':rsp[2],'power_generation':rsp[3],
				'energy_consumption':rsp[4],'power_consumption':rsp[5],'normalised_output':rsp[6],
		   		'temperature':rsp[7],'voltage':rsp[8]}

	def delete_status(self, date, time):
		"""
		Removes an existing status
		"""
		path = '/service/r1/deletestatus.jsp'
		params = {
				'd': date,
				't': time
				}
		params = urllib.urlencode(params)

		response = self.make_request("POST", path, params)

		if response.status == 400:
			raise ValueError(response.read())
		if response.status != 200:
			raise StandardError(response.read())

		return response.read()

	def make_request(self, method, path, params=None):
		conn = httplib.HTTPConnection(self.host)
		headers = {
				'Content-type': 'application/x-www-form-urlencoded',
				'Accept': 'text/plain',
				'X-Pvoutput-Apikey': self.api_key,
				'X-Pvoutput-SystemId': self.system_id
				}
		conn.request(method, path, params, headers)

		return conn.getresponse()

#-----------------
# Exported symbols
#-----------------
__all__ = [
  "PVOutputClient"
]

# vim: set expandtab ts=2 sw=2:
