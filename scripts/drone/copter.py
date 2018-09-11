# coding=utf-8
import socket
import threading
import time
import traceback

from django.db.models import QuerySet
from preconditions import preconditions

from mavlink.models.connection import MavlinkConnect
from mavlink.models.guided_waypoint import MavlinkGoTo
from mavlink.models.mission import MavlinkMission
from mavlink.models.models import *
from mavlink.models.waypoint import Waypoint
from scripts.drone.copter_error import *
from scripts.drone.message import Messages
from scripts.mavlink_db.dbaccess import refresh_database, update_mavlink_mavlinkdata
from django.conf import settings


class Copter:
    """
    Class that represents a fully featured copter and operations that can be applied to it
    """

    def __init__(self):
        self.vehicle = None
        self.current_waypoint = None
        self.mission_not_init = True

    def received_connect_signal(self):
        """Attempting connect to the drone with current connection configurations

        precondition:
            connect_object is a MavlinkConnect model type, no_test is True for anything except
            software testing.All connect_object data are validated
        postcondition:
            Copter's vehicle object is a dronekit.Vehicle object that can be interacted with.
            TODO: vehicle object has passed the connection check, done by wait_ready()
            If there is a exception, it will be raised by the function. In that case the vehicle object
                is not valid

        """
        connect_object = MavlinkConnect.objects.get(pk=1)
        try:
            connection_port = connect_object.connection_port
            baud_rate = connect_object.connection_baud_rate

            if not (baud_rate == 115200 or baud_rate == 57600):
                raise CopterConnectTimeoutError

            connect_object.connection_status_message = Messages.CONNECTING % connection_port
            connect_object.save()

            mission = MavlinkMission.objects.get(pk=1)
            mission.mission_status_message = Messages.MISSION_NOT_READY
            mission.save()

            if settings.ENGINE_DEBUG:
                print("Connecting to %s with %s " % (connection_port, baud_rate))
            # for some reason the connection fails some times
            # TODO figure out why: For some retraded reasons wait ready fails, even if the connection is good
            self.vehicle = dronekit.connect(connection_port, wait_ready=False, baud=baud_rate, heartbeat_timeout=10)

            # self.vehicle.wait_ready('is_armable', timeout=240)
            self.vehicle.wait_ready(True, timeout=30)

        # API Error
        except dronekit.APIException:
            if settings.ENGINE_DEBUG:
                print('Timeout!')
            connect_object.connection_status_message = Messages.CONNECTION_TIMEOUT

            connect_object.attempt_connect = False

            connect_object.save()

            raise CopterConnectTimeoutError

        except Exception as e:
            # Exceptions list:
            # PreconditionError, ConnectionErrors from dronekit

            # need to reset the button and all that
            refresh_database()

            if self.vehicle is not None:
                self.vehicle.close()

            traceback.print_tb(e.__traceback__)

            # failed to connect, reset everything and display mesage

            connect_object.connection_status_message = Messages.FAILED_CONNECTION % connect_object.connection_port

            connect_object.attempt_connect = False

            connect_object.save()

            raise e

        else:
            # Connection is success
            connect_object.connection_status_message = Messages.CONNECTED % connection_port

            connect_object.connected = True

            connect_object.attempt_connect = False

            connect_object.save()

            if settings.ENGINE_DEBUG:
                print("Connected to %s with %s" % (connection_port, baud_rate))

    def connect_to_drone(self):
        """
        :return:
        """
        while not MavlinkConnect.objects.get(pk=1).connected:

            # if the connect button is clicked
            if MavlinkConnect.objects.get(pk=1).attempt_connect:

                self.received_connect_signal()

            else:
                # Not attempting connecting, means the connect button is not clicked

                m = MavlinkConnect.objects.get(pk=1)
                m.connection_status_message = Messages.INITIALIZATION
                m.save()
                time.sleep(2)
                print("Not connecting")

    def home_location_check(self):
        """
        This function check if the home location is recevied
        since we used not wait ready, it means that the quad is not ready to be controlled
        thus we wait for gps lock fix, then enable the control interface.
        For Copter the home position is set as the location where the copter was armed.
        """
        try:

            m = MavlinkConnect.objects.get(pk=1)
            m.connection_status_message = Messages.HOME_LOCATION_PENDING
            m.save()

            while not self.vehicle.home_location:
                self.connection_interrupt_check()
                cmds = self.vehicle.commands
                cmds.download()
                cmds.wait_ready(timeout=5)
                if not self.vehicle.home_location:

                    if settings.ENGINE_DEBUG:
                        print(" Waiting for home location ...")
                time.sleep(1)

        except CopterConnectionInterruptError as e:
            traceback.print_tb(e.__traceback__)
            raise CopterConnectionInterruptError
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            raise e

        # We have a home location, so print it!

        m = MavlinkConnect.objects.get(pk=1)
        m.connection_status_message = Messages.HOME_LOCATION_RECEIVED
        m.save()

    def arm_check(self):
        """
        Precondition:
        Model initialized, vehicle is connected
        Check if the vehicle can be armed"""
        m = MavlinkConnect.objects.get(pk=1)
        m.connection_status_message = Messages.ARM_CHECKING
        m.save()
        try:
            count = 0
            while not self.vehicle.is_armable:
                self.connection_interrupt_check()
                if settings.ENGINE_DEBUG:
                    print("Passing Arm check")
                time.sleep(1)
                count += 1
                if count > 20:
                    break
            if not self.vehicle.is_armable:
                raise CopterArmTimeoutError
        except CopterConnectionInterruptError as e:
            traceback.print_tb(e.__traceback__)
            raise e
        except CopterArmTimeoutError as e:
            traceback.print_tb(e.__traceback__)
            raise e
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            raise e

        m = MavlinkConnect.objects.get(pk=1)
        m.connection_status_message = Messages.CONNECTED_DISARMED
        m.save()

    def arm_and_takeoff(self, alt):
        """

        :param alt: altitude to takeoff to

        """
        print("Arming motors")
        # Copter should arm in GUIDED mode
        self.vehicle.mode = dronekit.VehicleMode("GUIDED")
        self.vehicle.armed = True

        time.sleep(3)

        # Confirm vehicle armed before attempting to take off
        while not self.vehicle.armed:
            self.connection_interrupt_check()
            print(" Waiting for arming...")
            time.sleep(1)

        m = MavlinkConnect.objects.get(pk=1)
        m.connection_status_message = Messages.CONNECTED_ARMED
        m.save()

        print("Taking off!")
        self.vehicle.simple_takeoff(alt)  # Take off to target altitude

    def connection_interrupt_check(self):
        """ Check if the user attempt to disconnect the drone"""
        if self.vehicle is None:
            return
        if MavlinkConnect.objects.get(pk=1).attempt_connect and MavlinkConnect.objects.get(pk=1).connected:
            if settings.ENGINE_DEBUG:
                print("Mannual break the connection")
                # disconnect from the data link
            m = MavlinkConnect.objects.get(pk=1)
            m.connected = False
            m.attempt_connect = False

            m.connection_status_message = Messages.DISCONNECTING
            m.save()

            raise CopterConnectionInterruptError

    def data_thread(self):
        """
        :return: the data reading thread object
        """

        def helper(self):
            """

            :param self:
            """
            t = threading.current_thread()
            while getattr(t, 'not_terminate', True):
                self.home_location_check()
                try:
                    name_data_dict = dict()
                    name_data_dict['armed'] = "%s" % self.vehicle.armed
                    name_data_dict['mode'] = "%s" % self.vehicle.mode.name
                    name_data_dict['system_status'] = "%s" % self.vehicle.system_status.state
                    name_data_dict['longitude'] = self.vehicle.location.global_relative_frame.lon
                    name_data_dict['altitude'] = self.vehicle.location.global_relative_frame.alt
                    name_data_dict['latitude'] = self.vehicle.location.global_relative_frame.lat
                    name_data_dict['gps'] = "%s" % self.vehicle.gps_0
                    # TODO figure out WTF is wrong with version
                    name_data_dict['firmware_version'] = "BUGGED"
                    name_data_dict['velocity'] = "%s" % self.vehicle.velocity
                    name_data_dict['groundspeed'] = "%s" % self.vehicle.groundspeed
                    name_data_dict['battery'] = "%s" % self.vehicle.battery
                    name_data_dict['ekf_ok'] = "%s" % self.vehicle.ekf_ok
                    name_data_dict['last_heartbeat'] = "%s" % self.vehicle.last_heartbeat
                    name_data_dict['heading'] = "%s" % self.vehicle.heading
                    name_data_dict['airspeed'] = "%s" % self.vehicle.airspeed

                    name_data_dict['home_location_lat'] = self.vehicle.home_location.lat
                    name_data_dict['home_location_lon'] = self.vehicle.home_location.lon
                    name_data_dict['home_location_alt_abs'] = self.vehicle.home_location.alt

                    # print(name_data_dict)

                    update_mavlink_mavlinkdata(name_data_dict)

                    # TODO change the refresh time to the same as rate
                    time.sleep(settings.DATA_LINK_REFRESH_RATE)

                except Exception as e:
                    import sys
                    print("=====================Data Link failed ===========++")
                    traceback.print_tb(e.__traceback__)
                    raise CopterDataLinkError
            print("Stopped by main thread")

        return threading.Thread(target=helper, args=(self,))

    def operation_mission_main(self):
        """ This function This function is literating all the time when mission starts
            Only enter this function when the precondition is meet.
        precondition:
    :   1. the drone has passed the heartbeat check and arm check, received home location
        2. The drone is armed and
        :return 0:
        """
        # check the current flight mode
        # check mission mode

        if MavlinkMission.objects.get(pk=1).is_attempt_mission:

            if not MavlinkMission.objects.get(pk=1).is_mission_running:
                m = MavlinkMission.objects.get(pk=1)
                m.is_mission_running = True
                m.is_attempt_mission = False
                m.save()
                # get the next waypoing
                # change the mission trigger and set mission running to true
            else:
                # stop the mission
                m = MavlinkMission.objects.get(pk=1)
                m.is_mission_running = False
                m.is_attempt_mission = False
                m.save()
        else:
            if MavlinkMission.objects.get(pk=1).is_mission_running:
                # keep running

                self.operation_get_next_waypoint()

                if self.current_waypoint is None:
                    # mission is completed
                    pass
                else:
                    self.operation_go_to_current_waypoint()

            else:
                # not doing anything
                if settings.ENGINE_DEBUG:
                    print("Armed, just idling")

                m = MavlinkMission.objects.get(pk=1)
                m.mission_status_message = Messages.MISSION_IDLE
                m.save()

        time.sleep(settings.MISSION_REFRESH_RATE)

    def operation_get_next_waypoint(self):
        """Get the next waypoint to go to from guided and mission mode. If there is none left, return None to
        current waypoint"""

        # Guided GoTo mode loop
        if len(MavlinkGoTo.objects.get(pk=1).guided_waypoint_list.all()):

            # pass this point we are sure that there is at least one waypoint in the object
            guided = MavlinkGoTo.objects.get(pk=1)
            guided_list = guided.guided_waypoint_list.filter(accomplished=False).order_by('order')

            guided.guided_waypoint_message = Messages.GUIDED_MODE_READY
            guided.save()

            m = MavlinkMission.objects.get(pk=1)
            m.mission_status_message = Messages.MISSION_INTERRUPTED_BY_GUIDED
            m.save()

            if not self.current_waypoint:
                self.current_waypoint = guided_list[0].aerial_position

            elif self.current_waypoint.within_arrive_range(
                self.vehicle.location.global_relative_frame) and self.current_waypoint.duplicate(
                guided_list[0].aerial_position):

                waypoint = guided_list[0]
                waypoint.accomplished = True
                waypoint.save()
                # reload the new waypoint list
                guided_list = guided.guided_waypoint_list.filter(accomplished=False).order_by('order')

                if len(guided_list) is not 0:
                    # len() > 1 -> len >= 2
                    if settings.ENGINE_DEBUG:
                        print("Guided Added")

                    self.current_waypoint = guided_list[0].aerial_position
                    guided.guided_waypoint_message = Messages.GUIDED_ARRIVED_AT % (
                        self.current_waypoint.gps_position.latitude,
                        self.current_waypoint.gps_position.longitude,
                        self.current_waypoint.relative_altitude)
                    guided.save()
                else:
                    guided = MavlinkGoTo.objects.get(pk=1)
                    guided.guided_waypoint_list.filter(accomplished=True).delete()
                    guided.save()

            else:
                # when switch from mission to guided, we need to make sure that the waypoint is changed
                if not self.current_waypoint.duplicate(guided_list[0].aerial_position):
                    self.current_waypoint = guided_list[0].aerial_position

                if settings.ENGINE_DEBUG:
                    print("Guided Running")
                guided.guided_waypoint_message = Messages.GUIDED_HEADING_TO % (
                    self.current_waypoint.gps_position.latitude,
                    self.current_waypoint.gps_position.longitude,
                    self.current_waypoint.relative_altitude,
                    self.current_waypoint.distance_to(self.vehicle.location.global_relative_frame))
                guided.save()
        else:
            # Mission Mode loop
            mission = MavlinkMission.objects.get(pk=1)
            waypoint_list = mission.waypoint_list.filter(accomplished=False).order_by('order')  # typ
            # e: QuerySet[Waypoint]

            # Go here only if the guided waypoint is empty, and there are still waypoints left in the mission mode
            # catch current position is none:

            if len(waypoint_list) is 0:

                if settings.ENGINE_DEBUG:
                    print("Mission completed")

                mission.mission_status_message = Messages.MISSION_COMPLETED
                mission.is_mission_running = False
                mission.save()
                self.current_waypoint = None

            # there is at least one wya point left, or the mission only has one
            elif not self.current_waypoint:
                self.current_waypoint = waypoint_list[0].aerial_position

            # arrived at the final position, get next waypoint or mission completed
            elif self.current_waypoint.within_arrive_range(
                self.vehicle.location.global_relative_frame) and self.current_waypoint.duplicate(
                waypoint_list[0].aerial_position):
                # update the waypoint
                waypoint = waypoint_list[0]
                waypoint.accomplished = True
                waypoint.save()
                # reload the new waypoint list
                waypoint_list = mission.waypoint_list.filter(accomplished=False).order_by('order')

                if len(waypoint_list) is not 0:
                    # len() > 1 -> len >= 2
                    if settings.ENGINE_DEBUG:
                        print("Waypoint Changed")

                    self.current_waypoint = waypoint_list[0].aerial_position
                    mission.mission_status_message = Messages.MISSION_WAYPOINT_CHANGE % (
                        self.current_waypoint.gps_position.latitude,
                        self.current_waypoint.gps_position.longitude,
                        self.current_waypoint.relative_altitude)
                    mission.save()

            # Not arrived
            else:
                # when change from guided to mission
                if not self.current_waypoint.duplicate(waypoint_list[0].aerial_position):
                    self.current_waypoint = waypoint_list[0].aerial_position
                if settings.ENGINE_DEBUG:
                    print("Mission Running")
                mission.mission_status_message = Messages.MISSION_RUNNING % (
                    self.current_waypoint.gps_position.latitude,
                    self.current_waypoint.gps_position.longitude,
                    self.current_waypoint.relative_altitude,
                    self.current_waypoint.distance_to(self.vehicle.location.global_relative_frame))
                mission.save()

    def operation_go_to_current_waypoint(self):
        """Go to the point that the vehicle object is currently assigned to"""
        location = dronekit.LocationGlobalRelative(
            self.current_waypoint.gps_position.latitude,
            self.current_waypoint.gps_position.longitude,
            self.current_waypoint.relative_altitude,
        )
        self.vehicle.simple_goto(location)

    def operation_check_prerequisites(self):
        # TODO finish the checking function
        # TODO: pause if the mode changed
        """Check whether:
        1. Guided mode
        2. Armed
        3. connected
        4. have heartbeat
        5. attempt connect = false
        6. attempt_mission = false

        Any of them failed will set mission_running to false, and also throw an exceptoin
        """
        # mode:

        if self.mission_not_init:
            self.vehicle.mode = dronekit.VehicleMode("GUIDED")
            self.mission_not_init = False
        if not self.mission_not_init and self.vehicle.mode:
            pass

        # check connection
        # condition one: connection button is clicked
        try:
            self.connection_interrupt_check()

        except CopterConnectionInterruptError as e:
            traceback.print_tb(e.__traceback__)
            raise e
        else:
            pass
        """
        Most standalone apps should monitor the Vehicle.mode and stop sending commands if the mode changes unexpectedly 
            (this usually indicates that the user has taken control of the vehicle).
        Apps might monitor Vehicle.last_heartbeat and could attempt to reconnect if the value gets too high.
        Apps could monitor Vehicle.system_status for CRITICAL or EMERGENCY in order to implement 
            specific emergency handling.
        """
