from unittest import TestCase
from smurf import db_connect

class TestDBConnect(TestCase):

	def setUp(self):
		pass

	def test_success_connect(self):
		db_connect.connect_to_gcomv2()