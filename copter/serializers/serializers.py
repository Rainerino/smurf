from rest_framework import serializers

from copter.models.aerial_position import AerialPosition
from copter.models.connection import MavlinkConnect
from copter.models.gps_position import GpsPosition
from copter.models.guided_waypoint import MavlinkGoTo
from copter.models.mission import MavlinkMission
from copter.models.models import *
from copter.models.waypoint import Waypoint


class MavlinkConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MavlinkConnect
        fields = '__all__'


class MavlinkArmSerializer(serializers.ModelSerializer):
    class Meta:
        model = MavlinkArm
        fields = '__all__'


class MavlinkGoToSerializer(serializers.ModelSerializer):
    guided_waypoint_list = serializers.PrimaryKeyRelatedField(many=True, queryset=Waypoint.objects.all(),
                                                              required=False)

    class Meta:
        model = MavlinkGoTo
        fields = '__all__'


class MavlinkDataSerializer(serializers.ModelSerializer):
    # gps = MavlinkGPSSerializer(required=True)

    class Meta:
        model = MavlinkData
        fields = "__all__"


class MavlinkEngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = MavlinkEngine
        fields = '__all__'


class GpsPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GpsPosition
        fields = '__all__'


class MavlinkMissionSerializer(serializers.ModelSerializer):
    waypoint_list = serializers.PrimaryKeyRelatedField(many=True, queryset=Waypoint.objects.all(), required=False)

    class Meta:
        model = MavlinkMission
        fields = '__all__'


class AerailPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AerialPosition
        fields = '__all__'


class WaypointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waypoint
        fields = '__all__'
