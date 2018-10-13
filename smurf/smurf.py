#!/usr/bin/env python

"""
This module will take x arguments:
- baud_rate:
- port_number:

Smurf will update the database once it's connected. It will have the following models:

is_connect=false
current_latitude=49.1
current_longtitude=128.0.1
current_altitude_msl=20.1
current_heading=0

These should be added to database.ini
"""
import dronekit
import argparse
import serial
import traceback
import time
import signal
import sys

HOME_LOCATION_TIMEOUT = 5
DEBUG = 1
FREQ = 0.5
ATTEMPT_DELAY = 1
def update_database(data_dict):
	"""

	Args:
		data_dict: the data we want to print.

	Returns:
		updated database or not.
	"""
	return True


def loop_for_connection(connection_string, baud_rate):
	"""
	Keep checking the port provided until connected
	Args:
		connection_string: the port number given
		baud_rate: baud rate of the connection
	Returns:
		None
	"""

	def signal_handler(sig, frame):
		# this function will trap the ctrl C inputs, in case when the user when to terminate the program.
		print('=============You pressed Ctrl+C!')
		if vehicle:
			vehicle.close()
			if DEBUG:
				print("Vehicle disconnected and closed!")
		else:
			if DEBUG:
				print("Vehicle not connected!")

		sys.exit(0)

	signal.signal(signal.SIGINT, signal_handler)

	is_connected = False

	vehicle = None

	while True:

		if DEBUG:
			print "\nAttempting to connecting to vehicle on: %s" % connection_string

		# This try catch block will attempt to connect to the vehicle.
		try:
			#
			vehicle = dronekit.connect(connection_string, wait_ready=True, baud=baud_rate, heartbeat_timeout=5)

		# try to catch the serial false.

		except serial.SerialException as e:
			traceback.print_exc()
		except dronekit.APIException as e:
			traceback.print_exc()
		except Exception as e:
			traceback.print_exc()
		else:
			# connection is established.
			is_connected = True
			if DEBUG:
				print("Vehicle connected at %s %s" % (connection_string, baud_rate))
		# the last 		
		if not is_connected and not vehicle:
			continue
		else:
			prev_last_heartbeat = -1

			while is_connected and prev_last_heartbeat != vehicle.last_heartbeat:
				"""
				This is the operation loop. At this point the copter should be connected
				We should expect disconnection at this loop
				"""
				try:
					prev_last_heartbeat = vehicle.last_heartbeat

					# if the home location is not received, just busy wait.
					while not vehicle.home_location:
						cmds = vehicle.commands
						cmds.download()
						cmds.wait_ready()
						time.sleep(1)
						if DEBUG:
							print("Waiting for home location")

					# We have a home location, so print it!

					print " current location lon: %s" % vehicle.location.global_relative_frame.lon
					print " current location lat: %s" % vehicle.location.global_relative_frame.lat
					print " current location alt: %s" % vehicle.location.global_relative_frame.alt
					print " Heading: %s" % vehicle.heading

					print(prev_last_heartbeat)

					# update_database()
				except Exception:
					print(traceback.print_exc())
					is_connected = False
					if DEBUG:
						print("Unexpeceted connection failed in loop!")

				time.sleep(FREQ)

			is_connected = False
			if DEBUG:
				print("Connection failed when looping!")
			time.sleep(ATTEMPT_DELAY)

def main():
	"""
	The main execution loop of
	Args:

	Returns:

	"""
	parser = argparse.ArgumentParser(
		description='Print out vehicle state information. Connects to SITL on local PC by default.')
	parser.add_argument('--connect',
	                    help="vehicle connection target string. If not specified, SITL automatically started and used.")
	parser.add_argument('--baud', help="vehicle connection baud rate. If not specified, the deafult will be 115200")
	args = parser.parse_args()

	connection_string = args.connect
	baud_rate = args.baud

	# Start SITL if no connection string specified
	if not connection_string or not baud_rate:
		print "Please provide valid script inputs. Need both port and baud rate!"
		import sys
		sys.exit(1)

	loop_for_connection(connection_string, baud_rate)


if __name__ == '__main__':
	main()

