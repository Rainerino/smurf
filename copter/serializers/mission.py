from copter.models.aerial_position import AerialPosition
from rest_framework import serializers

from copter.models.gps_position import GpsPosition
from copter.models.waypoint import Waypoint
from copter.models.flight_mission import FlightMission
from copter.models.guided_waypoint import GuidedWaypoint


class FlightMissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = FlightMission
		fields = '__all__'


class AerailPositionSerializer(serializers.ModelSerializer):
	class Meta:
		model = AerialPosition
		fields = '__all__'


class WaypointSerializer(serializers.ModelSerializer):
	class Meta:
		model = Waypoint
		fields = '__all__'


class GpsPositionSerializer(serializers.ModelSerializer):
	class Meta:
		model = GpsPosition
		fields = '__all__'


class GuidedWaypointSerializer(serializers.ModelSerializer):
	class Meta:
		model = GuidedWaypoint
		fields = '__all__'

# class MavlinkGoToSerializer(serializers.ModelSerializer):
#     guided_waypoint_list = serializers.PrimaryKeyRelatedField(many=True, queryset=Waypoint.objects.all(),
#                                                               required=False)
#     class Meta:
#         model = MavlinkGoTo
#         fields = '__all__'
