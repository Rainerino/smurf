from django.db import models

from copter.models.waypoint import Waypoint


class FlightMission(models.Model):
    """ Mission that consist of the state of the current mission, the waypoint list that
    It will execute

    Attributes:
        mission_running: Whether there is a mission running or not
        is_attempt_mission: If the user has toggled the mission start/terminate button
                If it's set to true when the mission is running, it will terinmate the mission
        waypoint_list: The map of waypoint the current mission should follow
        mission_status_message: The infomative message for users of the status of the mission

    """
    is_mission_running = models.BooleanField(default=False)
    is_attempt_mission = models.BooleanField(default=False)
    waypoint_list = models.ManyToManyField(Waypoint, related_name="waypoint_list")
    mission_status_message = models.TextField(default="No message")

    def __str__(self):
        return "Mission is %s, status: %s" % ("Running" if self.is_mission_running else "Idling",
                                              self.mission_status_message)



