# # Create your views here.
# from django.http import JsonResponse
#
# from rest_framework import generics, status
# from rest_framework.response import Response
#
# from copter.serializers.serializers import *
#
# from copter.Copter import drone
#
# class MavlinkConnectListCreate(generics.RetrieveUpdateDestroyAPIView):
#     queryset = MavlinkConnect.objects.all()
#     serializer_class = MavlinkConnectionSerializer
#
#     def get(self, request, *args, **kwargs):
#         pass
#
# class MavlinkArmListCreate(generics.RetrieveUpdateDestroyAPIView):
#     queryset = MavlinkArm.objects.all()
#     serializer_class = MavlinkArmSerializer
#
#
# class MavlinkDataListCreate(generics.RetrieveUpdateDestroyAPIView):
#     queryset = MavlinkData.objects.all()
#     serializer_class = MavlinkDataSerializer
#
#
# class MavlinkEngineListCreate(generics.RetrieveUpdateDestroyAPIView):
#     queryset = MavlinkEngine.objects.all()
#     serializer_class = MavlinkEngineSerializer
#
#
# class MavlinkMissionViews(generics.RetrieveUpdateDestroyAPIView):
#     queryset = MavlinkMission.objects.all()
#     serializer_class = MavlinkMissionSerializer
#
#
# class GpsPositionViews(generics.ListCreateAPIView):
#     queryset = GpsPosition.objects.all()
#     serializer_class = GpsPositionSerializer
#
#
# class AerialPositionView(generics.ListCreateAPIView):
#     queryset = AerialPosition.objects.all()
#     serializer_class = AerailPositionSerializer
#
#
# class WaypointView(generics.ListCreateAPIView):
#     queryset = Waypoint.objects.all()
#     serializer_class = WaypointSerializer
#
#
# # http://www.django-rest-framework.org/tutorial/1-serialization/
# class MavlinkGoToViews(generics.RetrieveUpdateAPIView):
#     queryset = MavlinkGoTo.objects.all()
#     serializer_class = MavlinkGoToSerializer
#
#     def put(self, request, *args, **kwargs):
#         """
#         :param request:
#         :param args:
#         :param kwargs:
#         """
#         serializer = MavlinkGoToSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#         if serializer.validated_data.get('guided_waypoint_confirmed'):
#             # TODO add duplicate rejection
#             guided_waypoint_latitude = serializer.validated_data.get('guided_waypoint_latitude')
#             guided_waypoint_longitude = serializer.validated_data.get('guided_waypoint_longitude')
#             guided_waypoint_altitude = serializer.validated_data.get('guided_waypoint_altitude')
#
#             gps = GpsPosition(latitude=guided_waypoint_latitude, longitude=guided_waypoint_longitude)
#             gps.save()
#             aerial = AerialPosition(gps_position=gps, relative_altitude=guided_waypoint_altitude)
#             aerial.save()
#
#             print(aerial.__str__())
#             waypoint_order = 1 + Waypoint.objects.order_by('order').reverse()[0].order
#
#             waypoint = Waypoint(order=waypoint_order, aerial_position=aerial, accomplished=False)
#             waypoint.save()
#
#             print(waypoint.__str__())
#             print(serializer.data)
#             m = MavlinkGoTo.objects.get(pk=1)
#             m.guided_waypoint_list.add(waypoint)
#             m.guided_waypoint_confirmed = False
#             m.save()
#
#             serializer = MavlinkGoToSerializer(data=m)
#             if serializer.is_valid():
#                 serializer.save()
#                 return JsonResponse(serializer.data, status=201)
#             return JsonResponse(serializer.data, status=400)
#
#         return JsonResponse(serializer.data, status=200)
