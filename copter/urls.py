from django.conf.urls import url

from copter.views import views


urlpatterns = [
    url('api/mavlink/connect/(?P<pk>[0-9]+)$', views.MavlinkConnectListCreate.as_view(), name='mavlink_connect'),
    url('api/mavlink/arm/(?P<pk>[0-9]+)$', views.MavlinkArmListCreate.as_view(), name='mavlink_arm'),
    url('api/mavlink/goto/(?P<pk>[0-9]+)$', views.MavlinkGoToViews.as_view(), name='mavlink goto'),
    url('api/mavlink/data/(?P<pk>[0-9]+)$', views.MavlinkDataListCreate.as_view(), name='mavlink data'),
    url('api/mavlink/engine/(?P<pk>[0-9]+)$', views.MavlinkEngineListCreate.as_view(), name='mavlink engine'),

    url('api/mavlink/mission/(?P<pk>[0-9]+)$', views.MavlinkMissionViews.as_view(), name='mavlink mission'),
    url('api/mavlink/gps/(?P<pk>[0-9]+)$', views.GpsPositionViews.as_view(), name='gps'),
    url('api/mavlink/aerial_gps/(?P<pk>[0-9]+)$', views.AerialPositionView.as_view(), name='aerial_gps'),
    url('api/mavlink/waypoint/(?P<pk>[0-9]+)$', views.WaypointView.as_view(), name='waypoint'),

]

# from .engine import engine_main
#
# from background_task import background
#
#
# @background()
# def engine_daemon():
#     engine_main.main()
#
#
# engine_daemon()
