from django.core.management import call_command
from django.db import DatabaseError
from django.test import TestCase

import psycopg2

import scripts.mavlink_db.dbaccess as func
from copter.models.connection import MavlinkConnect


class TestDBAccess(TestCase):

    def test_refresh_failed(self):
        with self.assertRaises(DatabaseError):
            func.refresh_database("DoesntExistFileName")

    def test_refresh_success(self):
        self.assertEqual(0, func.refresh_database())
        # the test database is different from the manage.py one
        # self.assertFalse(MavlinkConnect.objects.get(pk=1).attempt_connect)

    def test_connect_success(self):
        # TODO how to test this?
        pass

    def test_connect_failed(self):
        with self.assertRaises(Exception):
            func.connect_to_gcomv2("Just a random file?")

    def setUp(self):
        self.connect = MavlinkConnect()
        self.connect.save()

    def test_django_database_model(self):

        self.connect.connection_port = "test"
        self.connect.connection_baud_rate = 115200

        result_1 = self.connect.connection_port
        result_2 = self.connect.connection_baud_rate

        self.assertEqual(result_1, "test")
        self.assertEqual(result_2, 115200)

    def test_django_database_save(self):
        call_command('loaddata', 'mavlinks')
        m = MavlinkConnect.objects.get(pk=1)
        m.attempt_connect = True
        m.save()
        k = MavlinkConnect.objects.get(pk=1)
        self.assertTrue(MavlinkConnect.objects.get(pk=1).attempt_connect)

