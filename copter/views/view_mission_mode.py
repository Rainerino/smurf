from copter.models.flight_mission import FlightMission

from copter.serializers.mission import FlightMissionSerializer
from rest_framework import generics


class FlightMissionListCreate(generics.RetrieveUpdateDestroyAPIView):
	queryset = FlightMission.objects.all()
	serializer_class = FlightMissionSerializer
