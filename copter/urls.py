from django.conf.urls import url

from copter.views.view_drone_status import DroneStatusListCreate
from copter.views.view_command_mode import DroneCommandListCreate
from copter.views.view_guided_mode import GuidedWaypointListCreate
from copter.views.view_mission_mode import FlightMissionListCreate

urlpatterns = [

	url('api/copter/command/(?P<pk>[0-9]+)$', DroneCommandListCreate.as_view(), name='command'),
	url('api/copter/status/(?P<pk>[0-9]+)$', DroneStatusListCreate.as_view(), name='status'),
	url('api/copter/mission/(?P<pk>[0-9]+)$', FlightMissionListCreate.as_view(), name='mission'),
	url('api/copter/guided/(?P<pk>[0-9]+)$', GuidedWaypointListCreate.as_view(), name='guided'),
]


