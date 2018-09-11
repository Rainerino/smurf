from django.conf import settings
from django.db import models

import dronekit

from copter.models.distance_func import *


# class MavlinkGPS(models.Model):
#     longitude = models.DecimalField(default=0, max_digits=11, decimal_places=8)
#     latitude = models.DecimalField(default=0, max_digits=11, decimal_places=8)
#     altitude = models.DecimalField(default=0, max_digits=7, decimal_places=4)


class MavlinkArm(models.Model):
    armed = models.BooleanField(default=False)
    attempt_arm = models.BooleanField(default=False)
    arm_status_message = models.TextField(default="failed")


class MavlinkData(models.Model):
    firmware_version = models.TextField(default="")
    longitude = models.DecimalField(default=0, max_digits=11, decimal_places=8)
    latitude = models.DecimalField(default=0, max_digits=11, decimal_places=8)
    altitude = models.DecimalField(default=0, max_digits=7, decimal_places=4)
    velocity = models.TextField(default="")
    gps = models.TextField(default="")
    groundspeed = models.TextField(default="")
    airspeed = models.TextField(default="")
    ekf_ok = models.TextField(default="")
    battery = models.TextField(default="")
    last_heartbeat = models.TextField(default="")
    heading = models.TextField(default="")
    mode = models.TextField(default="")
    armed = models.TextField(default="")
    system_status = models.TextField(default="")
    # home_location = models.ForeignKey(MavlinkGPS, on_delete=models.CASCADE)

    home_location_lon = models.DecimalField(default=0, max_digits=11, decimal_places=8)
    home_location_lat = models.DecimalField(default=0, max_digits=11, decimal_places=8)
    home_location_alt_abs = models.DecimalField(default=0, max_digits=7, decimal_places=4)


class MavlinkEngine(models.Model):
    engine_running = models.BooleanField(default=False)
    engine_attempt_running = models.BooleanField(default=False)
    engine_terminate = models.BooleanField(default=False)
    engine_status_message = models.TextField(default="")
