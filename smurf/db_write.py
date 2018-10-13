from db_connect import config
import psycopg2


def access_database(type="get", app="mavlink", model="mavlinkdata", data_name="connected", data=""):
	"""
	 Wriute data to the database with specific
	Args:
	    type:
	    app:
	    model:
	    data_name:
	    data:

	Returns:
		true of access successful, else false.
	"""
	conn = None
	cmd = None

	if isinstance(data, str) and ' ' in data:
		data = "\'" + data + "\'"

	if type == "get":
		cmd = "SELECT %s FROM %s_%s" % (data_name, app, model)
	elif type == "update":
		cmd = "UPDATE %s_%s SET %s = %s" % (app, model, data_name, data)

	try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()
		cur.execute(cmd)

		if type == "get":
			row = cur.fetchone()
			output = row[0]
			cur.close()
			return output
		elif type == "update":
			conn.commit()
			return data
	except Exception:
		import traceback
		traceback.print_exc()
	finally:
		if conn is not None:
			conn.close()
