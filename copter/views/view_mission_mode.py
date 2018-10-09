from copter.models.flight_mission import FlightMission
from copter.models.aerial_position import AerialPosition
from copter.models.gps_position import GpsPosition
from copter.models.waypoint import Waypoint
from rest_framework import generics
from copter.serializers.mission import GpsPositionSerializer, AerailPositionSerializer, WaypointSerializer, \
	FlightMissionSerializer

class GpsPositionViews(generics.ListCreateAPIView):
    queryset = GpsPosition.objects.all()
    serializer_class = GpsPositionSerializer


class AerialPositionView(generics.ListCreateAPIView):
    queryset = AerialPosition.objects.all()
    serializer_class = AerailPositionSerializer


class WaypointView(generics.ListCreateAPIView):
    queryset = Waypoint.objects.all()
    serializer_class = WaypointSerializer


class FlightMissionListCreate(generics.RetrieveUpdateDestroyAPIView):
	queryset = FlightMission.objects.all()
	serializer_class = FlightMissionSerializer
