import signal
import sys
import time
import traceback

from django.conf import settings
from django.db import DatabaseError

import dronekit

from mavlink.models.models import *
from scripts.drone.copter import Copter
from scripts.mavlink_db.dbaccess import connect_to_gcomv2, refresh_database
from scripts.drone.message import Messages


# https://django-extensions.readthedocs.io/en/latest/runscript.html
# the script require run as the function name
def run():
    """Main functions
    TODO:
    """
    m = MavlinkEngine.objects.get(pk=1)
    m.engine_status_message = Messages.ENGINE_STARTING
    m.save()

    # TODO pre program checks

    # start the sitl

    if settings.ENGINE_DEBUG:
        print("SITL Debugging mode")

    else:
        print("HITL mode")

    def handler(signum, frame):
        """overwrite the default function of signal interrupt with messages and exit"""
        if signum == 2:
            print('Received Ctrl-C, notified GCOM_V2')

            m = MavlinkEngine.objects.get(pk=1)
            m.engine_status_message = Messages.ENGINE_INTERRUPTED
            m.save()

            # next to do is to set a bit in the database to notify
            sys.exit(0)

    signal.signal(signal.SIGINT, handler)

    connected_drone = None
    data_thread = None
    while True:
        try:

            m = MavlinkEngine.objects.get(pk=1)
            m.engine_status_message = Messages.ENGINE_STARTED
            m.save()

            connect_to_gcomv2()

            refresh_database('mavlinks')

            m = MavlinkEngine.objects.get(pk=1)
            m.engine_status_message = Messages.ENGINE_RUNNING
            m.save()

            # This wile will get connection
            connected_drone = Copter()

            # raise exceptions here
            connected_drone.connect_to_drone()

            connected_drone.arm_check()

            connected_drone.home_location_check()

            # ==================== Pre mission checks

            """At this point, drone is ready to do any operations"""
            data_thread = connected_drone.data_thread()

            data_thread.start()

            # This is important!

            time.sleep(5)

            connected_drone.arm_and_takeoff(20)

            # Mission loop
            while True:

                connected_drone.operation_check_prerequisites()

                # if mission mode
                # Mode based
                connected_drone.operation_mission_main()

        except Exception as e:

            m = MavlinkEngine.objects.get(pk=1)
            m.engine_status_message = Messages.ENGINE_ERROR % e
            m.save()
            traceback.print_tb(e.__traceback__)
            print(e)

            if data_thread is not None:
                data_thread.not_terminate = False

            if connected_drone.vehicle is not None:
                # TODO bugged here
                connected_drone.vehicle.close()

            time.sleep(3)

            print("=======================FAILED=============")

        finally:
            print("============Engine Restart ===========")

        # if exit, means the connection failed

        # send error message

        # delay

        # clean up

    # This should not be reached!


if __name__ == '__main__':
    """
    function naming convention:
        start with command, then the model of data, then full signature of the json object
    """
