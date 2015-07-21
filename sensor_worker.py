# coding: utf-8

import logging
import rethinkdb as r

conn = r.connect("localhost").repl()
db = r.db("engine")
lamps_table = db.table("lamps")
command_table = db.table("sensors")
cursor = lamps_table.changes().run(conn)

logger = logging.getLogger('engine_worker')
logger.setLevel(logging.DEBUG)
hdlr = logging.FileHandler('logs/engine_worker.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)


import time

def sensord():
    command_table.insert(dict(command="GetRam", prio='low', lampNumber=999, address=25, sensord_id=0)).run(conn)
    time.sleep(10)

logger.warn('Initializing Sensor Worker.')
sensord()
