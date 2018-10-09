from django.conf.urls import url

from copter.views.view_drone_status import DroneStatusListCreate
from copter.views.view_command_mode import DroneCommandListCreate
from copter.views.view_mission_mode import FlightMissionListCreate

urlpatterns = [

	url('api/copter/command/(?P<pk>[0-9]+)$', DroneCommandListCreate.as_view(), name='copter_command'),
	url('api/copter/status/(?P<pk>[0-9]+)$', DroneStatusListCreate.as_view(), name='copter_status'),
	url('api/copter/mission/(?P<pk>[0-9]+)$', FlightMissionListCreate.as_view(), name='copter_mission'),
	# url('api/copter/gps/(?P<pk>[0-9]+)$', )
]


