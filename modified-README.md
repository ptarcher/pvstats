Setup the venv, install modules required.

mkdir -p /opt/python3/venv/pvstats
python -m venv /opt/python3/venv/pvstats
/opt/python3/venv/pvstats/bin/python /opt/python3/venv/pvstats/bin/pip install pymodbus
# probably not needed /opt/python3/venv/pvstats/bin/python /opt/python3/venv/pvstats/bin/pip install serial
/opt/python3/venv/pvstats/bin/python /opt/python3/venv/pvstats/bin/pip install pyserial
/opt/python3/venv/pvstats/bin/python /opt/python3/venv/pvstats/bin/pip install influxdb
/opt/python3/venv/pvstats/bin/python /opt/python3/venv/pvstats/bin/pip install httplib2
/opt/python3/venv/pvstats/bin/python /opt/python3/venv/pvstats/bin/pip install paho-mqtt
/opt/python3/venv/pvstats/bin/python /usr/bin/pvstats --cfg /etc/pvstats.conf

Put 'pvstats' directory from this codebase in /opt/python3/lib/  (or modify bin/pvstats to change where it appends pvstats to the sys.path)
