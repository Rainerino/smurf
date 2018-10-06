import sys
import traceback

import dronekit
from django.core.management import call_command
from django.db import models
from preconditions import preconditions
from copter.models.copter_message import Messages
from copter.models.copter_error import *
from django.conf import settings
from copter.models.drone_status import DroneStatus


class DroneCommand(models.Model):
	"""
	These are the variables for controlling drone, abstract manual copter control
	Command data can be read and write
	"""

	# this is connected to a connection button on the GUI
	is_attempt_connect = models.BooleanField(default=False)

	# this is connected to a disconnection button on the GUI
	is_attempt_disconnect = models.BooleanField(default=False)

	is_attempt_arm = models.BooleanField(default=False)

	is_attempt_disarm = models.BooleanField(default=True)

	connection_port = models.TextField(default="tcp:127.0.0.1:5760")

	# current_mission = mission blah
	def __str__(self):
		return "Vehicle at connection_port"

	@preconditions(lambda self: self.is_attempt_connect)
	def connect_to_vehicle(self, connection_port):
		"""This function will connect to a physical drone
			if vehicle is already connected, the function will return false with is_attempt_connect off, and not
				modifying anything
			precondition:
			is_attempt_connect is set to True
			the physical drone that is connected to the port should be ABSOLUTELY READY TO GO
				checklist include: gps lock, armable,

			postcondition:
			is_attempt_connect is set to False
			is_attempt_disconnect is set to False
			is_attempt_arm is False
			is_attempt_disarm is False
			is_connected is True if Result = True else False
			is_connecting is False
			is_armed is False
			is_arming is False
			The vehicle object is has passed all the checks if is_connected is True
			all drone status will get wiped iff connected

			Args:
				connectoin port to be consider
			Return:
				0: All good
				1: Bad input
				2: Failed connection
			"""

		# TODO: parallelism!
		# The reason being is when having multiple posts
		if DroneStatus.objects.get(pk=1).is_connected:
			if settings.ENGINE_DEBUG:
				print("The copter is already connected")
			self.is_attempt_connect = False
			self.save()
			return 1
		if settings.ENGINE_DEBUG:
			print("starting to connect vehicle")

		self.connection_port = connection_port
		self.save()
		connect_object = DroneStatus.objects.get(pk=1)
		connect_object.connection_status_message = Messages.INITIALIZATION
		connect_object.is_connecting = True
		connect_object.save()

		no_error = True

		try:
			connect_object.connection_status_message = Messages.CONNECTING % self.connection_port
			connect_object.save()

			if settings.ENGINE_DEBUG:
				print("Connecting to %s " % self.connection_port)
			# for some reason the connection fails some times

			""" 
			there are some really hard requirements for this function. If not ready, or a bad connection port, it will 
			get traped in a parented exception. We don't want to handle that since the thread will be somehow unkilable
			i.e. the exception will not be aught somehow. So we add it to the precondition
			"""
			if not settings.TESTING:
				connect_object.vehicle = dronekit.connect(self.connection_port, wait_ready=True, heartbeat_timeout=10)
			else:
				print("TESTING: connected to dummy copter")
		except Exception as e:
			print(traceback.print_tb(e.__traceback__))
			no_error = False
		finally:
			if no_error:
				# Connection is success
				connect_object.connection_status_message = Messages.CONNECTED % self.connection_port

				connect_object.is_connected = True
				connect_object.is_connecting = False
				connect_object.is_armed = False
				connect_object.is_arming = False
				connect_object.save()

				self.is_attempt_connect = False
				self.is_attempt_arm = False
				self.is_attempt_disarm = False
				self.is_attempt_disconnect = False

				self.save()

				if settings.ENGINE_DEBUG:
					print("Connected to %s " % self.connection_port)

				return 0
			else:
				connect_object.is_connecting = False
				connect_object.is_connected = False
				connect_object.vehicle = None
				connect_object.connection_status_message = Messages.FAILED_CONNECTION % self.connection_port
				connect_object.save()

				self.is_attempt_connect = False
				self.is_attempt_arm = False
				self.is_attempt_disarm = False
				self.is_attempt_disconnect = False
				self.save()

				if settings.ENGINE_DEBUG:
					print("=====================================================================")
					print("ERROR WAS HANDLED")

				return 2

	@preconditions(lambda self, delay: self.is_attempt_arm and not self.is_attempt_disarm and isinstance(delay, int))
	def arm_vehicle(self, delay=0):
		""""
		Arm vehicle function

		precondition: vehicle is connected, and user is attempt arm
		postcondition: vehicle is armed

		Args:
			delay: the duration of the delay to wait before arming
		Return:
			bool indicate if arming failed or not
		"""
		pass

	def disarm_vehicle(self):
		""""Disarm vehicle function
		precondition: vehicle is connected, and user is attempt arm
		postcondition: vehicle is armed

		Args:
			delay: the duration of the delay to wait before arming
		Return:
			bool indicate if arming failed or not
		"""
		pass

	def disconnect_from_vehicle(self):
		"""This function will disconnect from a connected vehicle
		precondition: connected to a vehicle
		postcondition:


		"""
		pass
