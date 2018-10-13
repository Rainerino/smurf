from configparser import ConfigParser

import psycopg2


def config(filename='database.ini', section='postgresql'):
	"""

	Args:
		filename: confguration file
		section: the type of database from the configuraiton file.
	Raise: Exception('Section {0} not found in the {1} file'.format(section, filename))
	Returns:
		connected psycog 2 database object

	"""
	# create a parser
	parser = ConfigParser()
	# read config file
	parser.read(filename)

	# get section, default to postgresql
	db = {}
	if parser.has_section(section):
		params = parser.items(section)
		for param in params:
			db[param[0]] = param[1]
	else:
		raise Exception('Section {0} not found in the {1} file'.format(section, filename))
	return db


def connect_to_gcomv2():
	"""
	Connect to the PostgreSQL database server

	Returns:
		true of connected, false if not.
	"""

	conn = None
	try:
		# read connection parameters
		params = config()

		# connect to the PostgreSQL server
		print('Connecting to the PostgreSQL database...')
		conn = psycopg2.connect(**params)

		# create a cursor
		cur = conn.cursor()

		# execute a statement
		print('PostgreSQL database version:')
		cur.execute('SELECT version()')

		# display the PostgreSQL database server version
		db_version = cur.fetchone()
		print(db_version)

		# close the communication with the PostgreSQL
		cur.close()
	except Exception:
		import traceback
		traceback.print_exc()
		return False
	finally:
		if conn is not None:
			conn.close()
			print('Database connection Failed.')
			return False
		else:
			return True


def check_db_connection():
	"""
	Check if still connected to the database
	Returns:

	"""
	pass