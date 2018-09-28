from django.db import models
from copter.models.aerial_position import AerialPosition
from dronekit import Vehicle

class DroneStatus(models.Model):
	"""
	These are the states of the copter, read only
	"""
	is_armed = models.BooleanField(default=False)
	is_arming = models.BooleanField(default=False)
	is_connected = models.BooleanField(default=False)
	is_connecting = models.BooleanField(default=False)

	arm_status_message = models.TextField(default="")
	connection_status_message = models.TextField(default="")

	"""
	Read only telemetry data
	"""
	firmware_version = models.TextField(default="")

	current_location = models.ForeignKey(AerialPosition, on_delete=models.CASCADE, related_name="current_location")

	home_location = models.ForeignKey(AerialPosition, on_delete=models.CASCADE, related_name="home_location")

	velocity = models.TextField(default="")
	# this is the gps message data
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

	# home_location_lon = models.DecimalField(default=0, max_digits=11, decimal_places=8)
	# home_location_lat = models.DecimalField(default=0, max_digits=11, decimal_places=8)
	# home_location_alt_abs = models.DecimalField(default=0, max_digits=7, decimal_places=4)

	# longitude = models.DecimalField(default=0, max_digits=11, decimal_places=8)
	# latitude = models.DecimalField(default=0, max_digits=11, decimal_places=8)
	# altitude = models.DecimalField(default=0, max_digits=7, decimal_places=4)

	vehicle = Vehicle
