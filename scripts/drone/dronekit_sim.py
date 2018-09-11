# # from dronekit import connect, VehicleMode, LocationGlobalRelative
# import argparse
# import time
#
# import dronekit
# from pymavlink import mavutil
#
#
# parser = argparse.ArgumentParser()
# parser.add_argument('--connect', default='127.0.0.1:14550')
# args = parser.parse_args()
#
# # Connect to the Vehicle
# print
# 'Connecting to vehicle on: %s' % args.connect
# vehicle = dronekit.connect(args.connect,  wait_ready=True)
#
#
# # Function to arm and then takeoff to a user specified altitude
# def arm_and_takeoff(aTargetAltitude):
# 	print
# 	"Basic pre-arm checks"
# 	# Don't let the user try to arm until autopilot is ready
#
# 	if vehicle.mode.name == "INITIALISING":
# 		print
# 		" Waiting for vehicle to initialise..."
# 	time.sleep(1)
#
# 	print
# 	"Waiting for GPS...:", vehicle.gps_0.fix_type
# 	# time.sleep(1)
#
# 	print
# 	"Arming motors"
# 	# Copter should arm in GUIDED mode
#
# 	vehicle.mode = dronekit.VehicleMode("GUIDED")
# 	vehicle.armed = True
#
# 	print
# 	"Taking off!"
# 	vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude
#
# 	# Check that vehicle has reached takeoff altitude
#
# 	while True:
# 		print
# 		" Altitude: ", vehicle.location.global_relative_frame.alt
# 		print
# 		" Waiting for arming..."
# 		print
# 		"Autopilot Firmware version: %a" % vehicle.version
# 		print
# 		"Autopilot capabilities (supports ftp): %s" % vehicle.capabilities.ftp
# 		print
# 		"Global Location: %s" % vehicle.location.global_frame
# 		print
# 		"Global Location (relative altitude): %s" % vehicle.location.global_relative_frame
# 		print
# 		"Local Location: %s" % vehicle.location.local_frame  # NED
# 		print
# 		"Attitude: %s" % vehicle.attitude
# 		print
# 		"Velocity: %s" % vehicle.velocity
# 		print
# 		"GPS: %s" % vehicle.gps_0
# 		print
# 		"Groundspeed: %s" % vehicle.groundspeed
# 		print
# 		"Airspeed: %s" % vehicle.airspeed
# 		print
# 		"Gimbal status: %s" % vehicle.gimbal
# 		print
# 		"Battery: %s" % vehicle.battery
# 		print
# 		"EKF OK?: %s" % vehicle.ekf_ok
# 		print
# 		"Last Heartbeat: %s" % vehicle.last_heartbeat
# 		print
# 		"Rangefinder: %s" % vehicle.rangefinder
# 		print
# 		"Rangefinder distance: %s" % vehicle.rangefinder.distance
# 		print
# 		"Rangefinder voltage: %s" % vehicle.rangefinder.voltage
# 		print
# 		"Heading: %s" % vehicle.heading
# 		print
# 		"Is Armable?: %s" % vehicle.is_armable
# 		print
# 		"System status: %s" % vehicle.system_status.state
# 		print
# 		"Mode: %s" % vehicle.mode.name  # settable
# 		print
# 		"Armed: %s" % vehicle.armed  # settableprintMSG
# 		print
# 		""
# 		# Break and return from function just below target altitude.
# 		if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
# 			print
# 			"Reached target altitude"
# 			break
# 		time.sleep(1)
#
#
# # vehicle is an instance of the Vehicle class
#
#
# # Initialize the takeoff sequence to 20m
# arm_and_takeoff(20)
#
# print("Take off complete")
#
# # Hover for 10 seconds
# time.sleep(10)
#
# print("Now let's land")
# vehicle.mode = dronekit.VehicleMode("LAND")
#
# # Close vehicle object
# vehicle.close()
#
# # FNULL = open(os.devnull, 'w')
# # drone_sitl = subprocess.Popen(
# #     ['dronekit-sitl', 'copter', '--home=49.259223,-123.2415589,96,138'],
# #     stdout=FNULL, stderr=subprocess.STDOUT)
# #
# # try:
# #     sitl = dronekit_sitl.start_default(49.259223, -123.2415589)
# # except Exception as e:
# #     print("Dronekit sitl cannot be started %s " % e)
# #     sys.exit(1)
