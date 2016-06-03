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

import json
with open("../templates/json/lamps-stn.json") as json_file:
    json_data = json.load(json_file)
    for lampData in json_data['lamps']:
        print "Adding " + lampData["identifier"] + " - id: " + lampData["hardware"]["address"] + " at " + str(lampData["location"]["coordinates"])
        db_lamps.insert(lampData).run(c)

# db_lamps.insert(lamp).run(c)
# db_lamps.insert(lamp2).run(c)
