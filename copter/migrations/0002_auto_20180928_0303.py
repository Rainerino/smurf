# Generated by Django 2.1.1 on 2018-09-28 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('copter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DroneCommand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_attempt_connect', models.BooleanField(default=False)),
                ('is_attempt_arm', models.BooleanField(default=False)),
                ('is_attempt_disarm', models.BooleanField(default=False)),
                ('connection_port', models.TextField(default=False)),
                ('connection_baud_rate', models.IntegerField(default=115200)),
            ],
        ),
        migrations.CreateModel(
            name='DroneStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_armed', models.BooleanField(default=False)),
                ('is_arming', models.BooleanField(default=False)),
                ('is_connected', models.BooleanField(default=False)),
                ('is_connecting', models.BooleanField(default=False)),
                ('arm_status_message', models.TextField(default='')),
                ('connection_status_message', models.TextField(default='')),
                ('firmware_version', models.TextField(default='')),
                ('velocity', models.TextField(default='')),
                ('gps', models.TextField(default='')),
                ('groundspeed', models.TextField(default='')),
                ('airspeed', models.TextField(default='')),
                ('ekf_ok', models.TextField(default='')),
                ('battery', models.TextField(default='')),
                ('last_heartbeat', models.TextField(default='')),
                ('heading', models.TextField(default='')),
                ('mode', models.TextField(default='')),
                ('armed', models.TextField(default='')),
                ('system_status', models.TextField(default='')),
                ('current_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='copter.AerialPosition')),
                ('home_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='copter.AerialPosition')),
            ],
        ),
        migrations.CreateModel(
            name='GuidedWaypoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_guided_running', models.BooleanField(default=False)),
                ('is_attempt_guided', models.BooleanField(default=False)),
                ('guided_status_message', models.TextField(default='No message')),
                ('current_guided_waypoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='copter.AerialPosition')),
            ],
        ),
        migrations.RenameModel(
            old_name='MavlinkMission',
            new_name='FlightMission',
        ),
        migrations.DeleteModel(
            name='MavlinkArm',
        ),
        migrations.DeleteModel(
            name='MavlinkConnect',
        ),
        migrations.DeleteModel(
            name='MavlinkData',
        ),
        migrations.DeleteModel(
            name='MavlinkEngine',
        ),
        migrations.RemoveField(
            model_name='mavlinkgoto',
            name='guided_waypoint_list',
        ),
        migrations.DeleteModel(
            name='MavlinkGoTo',
        ),
    ]