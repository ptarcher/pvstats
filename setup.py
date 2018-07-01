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

"""
Installs pvstats using distutils
Run:
    python setup.py install
to install the package from the source archive.
"""

from distutils.core import setup
from setuptools import find_packages

print find_packages(exclude=['test'])

setup(name='pvstats',
      version='1.0',
      description='Photovoltaic Inverter Statistics Scanner and Uploader',
      long_description="""
        TODO
      """,
      url='https://www.github.com/ptarcher/pvstats/',
      author='Paul Archer',
      author_email='ptarcher@gmail.com',
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: Apache 2.0 License',
        'Programming Language :: Python :: 2.7',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
      ],
      keywords='photovoltaics,influxdb,pvoutput.org',
      # TODO: I don't really understand packages
      packages=find_packages(exclude=['test']),
      install_requires=[
        'pymodbus',
        'influxdb',
        'paho-mqtt',
        'pyserial >= 2.6'
      ],
      data_files=[
        ('/usr/bin',           ['bin/pvstats']),
        ('/etc',               ['pvstats.conf']),
        ('/etc/systemd/system',['pvstats.service']),
      ],

      platforms=['Linux', 'Mac OS X', 'Win'],
     )
