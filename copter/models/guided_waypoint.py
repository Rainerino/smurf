# coding=utf-8
from django.db import models

from copter.models.waypoint import Waypoint


class MavlinkGoTo(models.Model):
    """"""
    guided_waypoint_longitude = models.FloatField(default=0)
    guided_waypoint_latitude = models.FloatField(default=0)
    guided_waypoint_altitude = models.FloatField(default=0)
    guided_waypoint_list = models.ManyToManyField(Waypoint, related_name="guided_list")
    guided_waypoint_confirmed = models.BooleanField(default=False)
    guided_waypoint_message = models.TextField(default="System Idle")
