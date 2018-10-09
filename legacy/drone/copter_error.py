# coding=utf-8


class CopterDataLinkError(ConnectionError):
    """ Error caused by Data link thread, when getting data from the vehicle, some connection
    error happened or the return data is None"""

    def __init__(self):
        ConnectionError.__init__(self,
                                 "Data link threadfailed after connecting to dronekit, check"
                                 "GPS lock and pixhawk connection")


class CopterHomeLocationNotReceivedError(ConnectionRefusedError):
    """ When doing the home location check for RTL mode and safety, the wait ready function failed
    or gps lock not obtained. """

    def __init__(self):
        ConnectionRefusedError.__init__(self, "Home location not received after 30 seconds timeout, "
                                              "please check GPS Lock and Arm check, or see set home location at:"
                                              "http://ardupilot.org/copter/docs/common-planning-a-mission-with"
                                              "-waypoints-and-events.html")


# TODO: change error type
class CopterConnectionInterruptError(InterruptedError):
    """ Connection button was pressed by the user to attempt interrupt the connection"""

    def __init__(self):
        InterruptedError.__init__(self, "Connection was interrupted by the user, resetting Engine")


class CopterArmTimeoutError(TimeoutError):
    def __init__(self):
        TimeoutError.__init__(self, "Arm check time out! Please start the engine after you have passed the"
                                    "HITL arm check!")


class CopterConnectTimeoutError(TimeoutError):
    def __init__(self):
        TimeoutError.__init__(self, "Connect time out! Check the port number, the baud rate, if it's wired it should "
                                    "be 115200, wireless is 57600")

class CopterConnectError(IOError):
    def __init__(self):
        TimeoutError.__init__(self, "Connection failed! It's not timed out tho. ")