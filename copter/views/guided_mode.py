
from copter.models.guided_waypoint import GuidedWaypoint

from copter.serializers.mission import GuidedWaypointSerializer
from rest_framework import generics


class GuidedWaypointListCreate(generics.RetrieveUpdateDestroyAPIView):
	queryset = GuidedWaypoint.objects.all()
	serializer_class = GuidedWaypointSerializer
