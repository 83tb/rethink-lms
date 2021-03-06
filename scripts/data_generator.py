#!/usr/bin/env python
import rethinkdb as r
import logging


def setup_db(db_name="engine", tables=['lamps', ]):
    connection = r.connect(host="localhost")
    try:
        r.db_create(db_name).run(connection)
        for tbl in tables:
            r.db(db_name).table_create(tbl, durability="hard").run(connection)
        logging.info('Database setup completed.')
        # r.db(db_name).table('lamps').index_create('location', geo=True).run(connection)

    except r.RqlRuntimeError:
        logging.warn('Database/Table already exists.')
    finally:
        connection.close()

db = r.db("engine")
db_lamps = db.table('lamps')
c = r.connect(host="localhost")

setup_db()
try:
    db_lamps.index_create('location', geo=True).run(c)
except r.RqlRuntimeError:
    logging.warn('Index already exists.')

location = {
    "type": "Point",
            "coordinates": [125.6, 10.1]
}

geo_position = r.geojson(location)

location2 = {
    "type": "Point",
            "coordinates": [15.6, 10.1]
}

geo_position2 = r.geojson(location2)

lamp = {
    "identifier": "Lamp Test",
    "group": [],
    "hardware": {
        "protocol": "madli",
                    "building": "stn",
                    "is_sensor": "false",
                    "type": "madli lamp",
                    "computer_ip": "10.1.2.55",
                    "address": "481"
    },
    "working_l_setting": 244,
    "special_l_setting": 26,
    "presence_l_setting": 40,
    "wanted_l_level": 26,
    "actual_driver_value": 26,
    "presence_flag": "false",
    "special_flag": "true",
    "working_flag": "true",
    "change_required": "true",
    "location": geo_position,
}

lamp2 = {
    "identifier": "Wow",
    "group": [],
    "hardware": {
        "protocol": "madli",
                    "building": "stn",
                    "is_sensor": "false",
                    "type": "madli lamp",
                    "computer_ip": "10.1.2.55",
                    "address": "480"
    },
    "working_l_setting": 244,
    "special_l_setting": 26,
    "presence_l_setting": 40,
    "wanted_l_level": 26,
    "actual_driver_value": 26,
    "presence_flag": "false",
    "special_flag": "true",
    "working_flag": "true",
    "change_required": "true",
    "location": geo_position2,
}

db_lamps.insert(lamp).run(c)
db_lamps.insert(lamp2).run(c)
