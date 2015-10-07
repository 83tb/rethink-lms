from madli import *
import rethinkdb as r
import logging


logger = logging.getLogger('serial_worker')
logger.setLevel(logging.DEBUG)

hdlr = logging.FileHandler('logs/serial_worker.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)

conn = r.connect("localhost").repl()


# NEW PUB SUB BEGIN
amqp_address = "amqp://guest:guest@192.168.99.100:32769"
from pubsub.notification_rec import NotificationReceiver
rec = NotificationReceiver(amqp_address)
topic = "commands"
#


db = r.db("engine")
lamps_table = db.table("lamps")
sensor_table = db.table("sensors")

cursor = lamps_table.changes().run(conn)


def read(task):
    try:
        logger.debug('Trying to read the value')
        actual_driver_value = call(
            task['command'], task['lampNumber'], task['address']).get('data1', None)
        lamp = dict(
            id=task['lamp_id'], actual_driver_value=actual_driver_value)
        logger.debug('Uploading value to rethink')
        lamps_table.get(task['lamp_id']).update(lamp).run(conn)
        logger.debug('Uploaded value was: ' + str(actual_driver_value))
    except Exception, e:
        logger.error('Error: ' + str(e))


def sense(task):
    try:
        logger.debug('Trying to read the value')
        sensor_value = call(
            task['command'], task['lampNumber'], task['address']).get('data1', None)

        sensor = dict(
            id=task['sensor_id'], sensor_value=sensor_value)
        logger.debug('Uploading value to rethink')
        try:
            sensor_table.get(task['sensor_id']).update(sensor).run(conn)
        except:
            del sensor['id']
            sensor_table.insert(sensor)

        logger.debug('Uploaded value was: ' + str(sensor_value))
    except Exception, e:
        logger.error('Error: ' + str(e))




def write(task):
    try:
        logger.debug('Trying send fast command')
        call(task['command'], task['lampNumber'], task['address'])
    except Exception, e:
        logger.error('Error: ' + str(e))


def worker():
    with rec:
        task = rec.listen()
        if task['type'] == "write":
            write(task)
        if task['type'] == "read":
            read(task)
        if task['type'] == "sense":
            sense(task)

logger.warn('Initializing Serial Worker.')
worker()
