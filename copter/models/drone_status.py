from django.db import models

class DroneStatus:
	# read only data
	# is_armed, is_arming, is_connected, is_connecting, is_mission_running
	#  mission_status_message, arm_status_message,connection_status_message,

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

	pass

