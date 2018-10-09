import time

import dronekit
from django.conf import settings
from django.db import models
from preconditions import preconditions

from copter.models.aerial_position import AerialPosition
from copter.models.copter_message import Messages
from copter.models.drone_command import DroneCommand
from copter.models.drone_status import DroneStatus
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
    is_pause_mission = models.BooleanField(default=False)
    is_mission_accomplished = models.BooleanField(default=False)
    # aerial point 3 is the default go to point
    current_guided_waypoint = models.ForeignKey(AerialPosition, on_delete=models.CASCADE,
                                                related_name="guided_waypoint", default=3)
    waypoint_list = models.ManyToManyField(Waypoint, related_name="waypoint_list")
    mission_status_message = models.TextField(default="No message")

    # init guided mode
    mission_not_init = True

    def __str__(self):
        return "Mission is %s, status: %s" % ("Running" if self.is_mission_running else "Idling",
                                              self.mission_status_message)

    def operation_get_next_waypoint(self):
        """Get the next waypoint"""
        # Mission Mode loop
        waypoint_list = self.waypoint_list.filter(accomplished=False).order_by('order')  # typ
        current_copter = DroneStatus.objects.get(pk=1).vehicle
        # e: QuerySet[Waypoint]

        # Go here only if the guided waypoint is empty, and there are still waypoints left in the mission mode
        # catch current position is none:

        if len(waypoint_list) is 0:

            if settings.COPTER_DEBUG:
                print("No waypoints left")

            self.is_mission_running = False
            self.is_mission_accomplished = True
            self.is_pause_mission = False
            self.is_attempt_mission = False
            self.save()
            self.current_guided_waypoint_id = 1

        # there is at least one wya point left, or the mission only has one

        # arrived at the final position, get next waypoint or mission completed
        elif self.current_guided_waypoint.within_arrive_range(current_copter.location.global_relative_frame):
            # update the waypoint
            waypoint = waypoint_list[0]
            waypoint.accomplished = True
            waypoint.save()
            # reload the new waypoint list
            waypoint_list = self.waypoint_list.filter(accomplished=False).order_by('order')

            if len(waypoint_list) is not 0:
                # len() > 1 -> len >= 2
                if settings.ENGINE_DEBUG:
                    print("Waypoint Changed")

                self.current_guided_waypoint = waypoint_list[0].aerial_position
                self.mission_status_message = Messages.MISSION_WAYPOINT_CHANGE % (
                    self.current_guided_waypoint.gps_position.latitude,
                    self.current_guided_waypoint.gps_position.longitude,
                    self.current_guided_waypoint.relative_altitude)
                self.save()

        # Not arrived
        else:
            # when change from guided to mission
            if settings.ENGINE_DEBUG:
                print("Mission Running")
            self.mission_status_message = Messages.MISSION_RUNNING % (
                self.current_guided_waypoint.gps_position.latitude,
                self.current_guided_waypoint.gps_position.longitude,
                self.current_guided_waypoint.relative_altitude,
                self.current_guided_waypoint.distance_to(DroneStatus.objects.get(pk=1).vehicle.location.global_relative_frame))
            self.save()
            location = dronekit.LocationGlobalRelative(
                self.current_guided_waypoint.gps_position.latitude,
                self.current_guided_waypoint.gps_position.longitude,
                self.current_guided_waypoint.relative_altitude,
            )
            DroneStatus.objects.get(pk=1).vehicle.simple_goto(location)

    def start_mission(self):
        """Function to call when starting the mission
        Triggered by is_attempt_mission. This function will iterate at MISSION_REFRESH_RATE,
        Until all waypoints has been reached and it will return, with is_mission_accomplished toggled to True
        is_attempt_mission will suppress all triggers, and reset the mission, use with care!
        This will trap the operation into a loop that will only terminate after mission is accomplished

        1. finish the mission
        2. is_attempt_mission to reset
        precondition: vehicle is connected and is armable, with home location receviced
        postcondition:

        """
        while not self.is_attempt_mission and self.is_mission_running and not self.is_mission_accomplished:
            # TODO: Take off and Land!
            # keep running
            mission_status = self.check_mission_status()
            if mission_status == 0:
                self.operation_get_next_waypoint()
            elif mission_status == 1:
                if settings.COPTER_DEBUG:
                    print("MISSION PAUSED")
            elif mission_status == 2:
                if settings.COPTER_DEBUG:
                    print("Failed: During mission mode, failed connection!")
                break
            else:
                if settings.COPTER_DEBUG:
                    print("=====================Unreachable branch at start_mission!")
                break
            time.sleep(settings.MISSION_REFRESH_RATE)

        if self.is_attempt_mission:
            # force reset everything!
            self.is_mission_running = True
            self.is_attempt_mission = False
            self.is_mission_accomplished = False
            self.is_pause_mission = False
            self.save()
        else:
            # not attempting mission, not running mission and mission is accomplished:
            if settings.COPTER_DEBUG:
                print("Mission Finished, idling")

    def update_waypoint_list(self):
        pass

    def pause_mission(self):
        """
        There are two ways to pause the mission:
        1. toggle pause mission
        2. change flight mode
        When the mission is paused, it will remember the next waypoint, and after unpausing, means
        if is_pause _mission is toggle to false (check flight mode == GUIDED), it wil go to the next point
        :return:
        """
        pass

    def check_mission_status(self):
        """
        Check the mission status

        postcondition:
        nothing if everything is ok,
        set mission signals to false if not connected,
        change mission siagal if paused
        Returns:
            0: normal
            1: paused
            2: Connection Error!
        """
        if not DroneStatus.objects.get(pk=1).check_connection():
            self.is_mission_running = False
            self.is_attempt_mission = False
            self.is_mission_accomplished = False
            self.is_pause_mission = False
            return 2

        if not self.is_mission_running:
            # mission should always nbe running when checking!
            # prob a false reset data error
            return 2
        elif self.mission_not_init:
            DroneCommand.objects.get(pk=1).vehicle.mode = dronekit.VehicleMode("GUIDED")
            self.mission_not_init = False
            return 0
        elif not self.mission_not_init and DroneCommand.objects.get(pk=1).mode.name != "GUIDED":
            # after change mode to guided, the mode was changed to something else
            self.pause_mission()
            return 1
        elif self.is_pause_mission:
            self.pause_mission()
            return 1
        else:
            return 0