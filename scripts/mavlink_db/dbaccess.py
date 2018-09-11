import os
import subprocess
import sys
from configparser import ConfigParser

from django.conf import settings
from django.db import DatabaseError

import psycopg2


def configure_database(filename='scripts/mavlink_db/database.ini', section='postgresql'):
    """

    :param filename:
    :param section:
    :return:
    """
    # create a parser
    parser = ConfigParser()
    # read config file
    config_file = os.path.join(os.getcwd(), filename)

    parser.read(config_file)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, config_file))

    return db


def connect_to_gcomv2(filename='scripts/mavlink_db/database.ini'):
    """ Connect to the PostgreSQL database server,
     Used for mainly check the connection
     """
    conn = None
    try:
        # read connection parameters
        params = configure_database(filename)

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
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
            return 0


def refresh_database(fixture_file='mavlinks'):
    """ This function will load the fixture to the database, essentally refresh the database"""
    fnull = open(os.devnull, 'w')

    # return_flush = subprocess.call(["python", "manage.py", 'flush', '--no-input'], stdout=fnull,
    #                                stderr=subprocess.STDOUT)
    return_load = subprocess.call(["python", "manage.py", "loaddata", fixture_file], stdout=fnull,
                                  stderr=subprocess.STDOUT)

    if settings.ENGINE_DEBUG:
        print("load exit code: %s" % return_load)
        if not return_load:
            print("Database is refreshed to default.")

    try:
        # database is avaible and connected, validated
        if return_load:
            raise DatabaseError

    except DatabaseError as e:
        if settings.ENGINE_DEBUG:
            print("Database Error! Check fixtures and database configurations")
        raise e
    else:
        return 0


# TODO replace this please
def update_mavlink_mavlinkdata(name_data_dict):
    conn = None

    try:
        # read database configuration
        # connect to the PostgreSQL database
        params = configure_database()

        conn = psycopg2.connect(**params)

        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement

        sql = """ UPDATE mavlink_mavlinkdata
                            SET firmware_version = %s"""
        cur.execute(sql, [name_data_dict["firmware_version"]])

        conn.commit()

        sql = """ UPDATE mavlink_mavlinkdata
                            SET longitude = %s"""
        cur.execute(sql, [name_data_dict["longitude"]])

        conn.commit()

        sql = """ UPDATE mavlink_mavlinkdata
                            SET latitude = %s"""
        cur.execute(sql, [name_data_dict["latitude"]])

        conn.commit()

        sql = """ UPDATE mavlink_mavlinkdata
                            SET altitude = %s"""
        cur.execute(sql, [name_data_dict["altitude"]])

        conn.commit()

        sql = """ UPDATE mavlink_mavlinkdata
                             SET velocity = %s"""
        cur.execute(sql, [name_data_dict["velocity"]])

        conn.commit()

        sql = """ UPDATE mavlink_mavlinkdata
                             SET gps = %s"""
        cur.execute(sql, [name_data_dict["gps"]])

        conn.commit()

        sql = """ UPDATE mavlink_mavlinkdata
                             SET groundspeed = %s"""
        cur.execute(sql, [name_data_dict["groundspeed"]])

        conn.commit()

        sql = """ UPDATE mavlink_mavlinkdata
                             SET airspeed = %s"""
        cur.execute(sql, [name_data_dict["airspeed"]])

        conn.commit()

        sql = """ UPDATE mavlink_mavlinkdata
                             SET battery = %s"""
        cur.execute(sql, [name_data_dict["battery"]])
        conn.commit()

        sql = """ UPDATE mavlink_mavlinkdata
                             SET last_heartbeat = %s"""
        cur.execute(sql, [name_data_dict["last_heartbeat"]])

        conn.commit()

        sql = """ UPDATE mavlink_mavlinkdata
                             SET heading = %s"""
        cur.execute(sql, [name_data_dict["heading"]])

        conn.commit()

        sql = """ UPDATE mavlink_mavlinkdata
                     SET armed = %s"""
        cur.execute(sql, [name_data_dict["armed"]])

        # get the number of updated rows

        # Commit the changes to the database
        conn.commit()

        sql = """ UPDATE mavlink_mavlinkdata
                     SET system_status = %s"""
        cur.execute(sql, [name_data_dict["system_status"]])
        # get the number of updated rows

        conn.commit()

        sql = """ UPDATE mavlink_mavlinkdata
                     SET mode = %s"""
        cur.execute(sql, [name_data_dict["mode"]])

        conn.commit()

        sql = """ UPDATE mavlink_mavlinkdata
                     SET ekf_ok = %s"""
        cur.execute(sql, [name_data_dict["ekf_ok"]])

        conn.commit()

        sql = """ UPDATE mavlink_mavlinkdata
                     SET home_location_lon = %s"""
        cur.execute(sql, [name_data_dict["home_location_lon"]])

        conn.commit()

        sql = """ UPDATE mavlink_mavlinkdata
                     SET home_location_lat = %s"""
        cur.execute(sql, [name_data_dict["home_location_lat"]])

        conn.commit()

        sql = """ UPDATE mavlink_mavlinkdata
                     SET home_location_alt_abs = %s"""
        cur.execute(sql, [name_data_dict["home_location_alt_abs"]])

        conn.commit()

        # print("Updated connection_status_message with %s" % data)
        # Close communication with the PostgreSQL database
        cur.close()


    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise
    finally:
        if conn is not None:
            conn.close()

    return 0
