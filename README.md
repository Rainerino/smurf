# Smurf
---
A python package that will push telemetry Ardupliot based Copter data to the postgresql database

## Overview
#### The function provided are: 

```bash 
python smurf.py --connect --baud
```

#### Helper function 
Helping the database connection

```python
def access_database(type="get", app="mavlink", model="mavlinkdata", data_name="connected", data=""):
```
```python
def config(filename='database.ini', section='postgresql')
def connect_to_gcomv2()
```

## Installation
To set up the package
```bash
./tools/setup.sh
```

## Execution
#### UNIX

With ardupliot stimulation:
```bash
python smurf.py --connect '127.0.0.1:14550'--baud 115200
```
With dronekit-sitl stimulation:
```bash
dronekit-sitl copter &

python smurf.py --connect 'tcp:127.0.0.1:5760'--baud 115200
```
Wired connection to pixhawk. It depends on the port! Use this to check.
```bash
ls /dev | grep 'ttyU'
```
If it's connected to ttyUSB0
```bash
python smurf.py --connect '/dev/ttyUSB0'--baud 57600
```
#### WINDOW

Just don't use it.