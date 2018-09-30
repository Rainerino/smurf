class Messages:

    # CONNECTION Messages
    CONNECTING = "Attempting connect to %s"
    CONNECTED = "Connected to drone at %s"
    DISCONNECTING = "Disconnecting from vehicle"
    DISCONNECTED = "Disconnected from vehicle"
    FAILED_CONNECTION = "Connection to %s Failed! Please try again"
    INITIALIZATION = "System idle, not connected"
    ARM_CHECKING = "Currently checking arm"
    CONNECTED_ARMED = "Drone is ARMED"
    CONNECTED_DISARMED = "Drone is DISARMED"
    HOME_LOCATION_RECEIVED = "Home location received"
    HOME_LOCATION_PENDING = "Waiting for home location..."
    CONNECTION_TIMEOUT = "Connecting to the drone has timeout! "



    # GUIDED message
    GUIDED_MODE_READY = "Currently at Guided mode, ready to go to"
    GUIDED_HEADING_TO = "Guided, Heading to %s, %s, %s, distance: %s"
    GUIDED_ARRIVED_AT = "Guided, Arrived at %s, %s, %s"


    # MIssion Meeage
    MISSION_NOT_READY = "Connected, Mission mode not ready"
    MISSION_READY = "ARMED, ready to start mission"
    MISSION_NEED_ARM  = "Require Armed"
    MISSION_RUNNING = "Mission is running, going to %s %s %s, distance is %s"
    MISSION_IDLE = "Mission paused, idling"
    MISSION_COMPLETED = "Mission is completed"
    MISSION_WAYPOINT_CHANGE = "Mission changed waypoint to : %s %s %s"
    MISSION_INTERRUPTED_BY_GUIDED = "Mission interrupted by Guided GoTo mode"


