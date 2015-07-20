#!/usr/bin/env python
import csv, json
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

def returnLampObj(id, coords):
	location = {
		"type": "Point",
		"coordinates": coords
	}

	geo_position = r.geojson(location)

	lamp = {
		"identifier": "UED " + str(id),
		"group": [],
		"hardware": {
			"protocol": "madli",
			"building": "MLP2 A2",
			"is_sensor": "false",
			"type": "madli lamp",
			"computer_ip": "10.1.202.11",
			"address": id
		},
		"working_l_setting": 244,
		"special_l_setting": 255,
		"presence_l_setting": 40,
		"wanted_l_level": 255,
		"actual_driver_value": 255,
		"presence_flag": "false",
		"special_flag": "true",
		"working_flag": "false",
		"change_required": "true",
		"location": geo_position,
	}
	return lamp


db_lamps.delete().run(c)

with open('lamps.csv', 'rb') as csvfile:
	base_coords = [20.74764, 52.17831]
	#jsonData = []
	iCY = 0
	i = 0
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in spamreader:
		coordY = base_coords[1] - iCY
		iCY += 0.0001
		iCX = 0
		for lid in row:
			coordX = base_coords[0] + iCX
			iCX += 0.0001
			coords = [coordX, coordY]
			if(lid):
				i += 1
				print "Lamp: " + str([i, lid, coords])
#				jsonData.append(returnLampObj(lid, coords))
				db_lamps.insert(returnLampObj(lid, coords)).run(c)
print "Total " + str(i) + " lamps"
#print jsonData

#with open('universal-lamps.json', 'w') as outfile:
#	json.dump(jsonData, outfile, sort_keys=True, indent=4,
#ensure_ascii=False)

