from madli import *
import rethinkdb as r
import logging
from time import time, sleep

logger = logging.getLogger('serial_worker')
logger.setLevel(logging.DEBUG)

hdlr = logging.FileHandler('logs/serial_worker.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)

conn = r.connect("localhost").repl()


db = r.db("engine")
lamps_table = db.table("lamps")
command_table = db.table("commands")
sensor_table = db.table("sensors")
sensor_reads_table = db.table("sensor_reads")

cursor = lamps_table.changes().run(conn)


def read_task(task):
    try:
        logger.debug('Trying to read the value')
        actual_driver_value = call(
                task['command'], task['lampNumber'], task['address']
            ).get('data1', None)
        lamp = dict(
            id=task['lamp_id'], actual_driver_value=actual_driver_value)
        logger.debug('Uploading value to rethink')
        lamps_table.get(task['lamp_id']).update(lamp).run(conn)
        logger.debug('Uploaded value was: ' + str(actual_driver_value))
        command_table.get(task['id']).delete().run(conn)
    except Exception, e:
        logger.error('Error: ' + str(e))
        command_table.get(task['id']).delete().run(conn)


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
        command_table.get(task['id']).delete().run(conn)
    except Exception, e:
        logger.error('Error: ' + str(e))
        command_table.get(task['id']).delete().run(conn)


def write_task(task):
    try:
        logger.debug('Trying send fast command')
        logger.info('Trying set lamp id: {} cmd: {} task: {}'.format(task['lampNumber'], task['command'], task['address']))

        call(task['command'], task['lampNumber'], task['address'])
        command_table.get(task['id']).delete().run(conn)
    except Exception, e:
        logger.error('Error: ' + str(e))
        try:
            logger.info('Trying again!'.format(task['command'], task['lampNumber'], task['address']))
            sleep(1)
            call(task['command'], task['lampNumber'], task['address'])
        except Exception, e:
            logger.error('Failed again!')
            logger.error('Error: ' + str(e))

        command_table.get(task['id']).delete().run(conn)


def worker():
    while True:
        t0 = time()
        cmd_low = command_table.filter(
            {'prio': 'low'}).limit(1).run(conn)  # slow?!?!?!
        cmd_high = command_table.filter(
            {'prio': 'high'}).run(conn)  # slow?!?!?!?!
#        sensors = sensor_reads_table.get_all().limit(1).run(conn)

        t1 = time()
#        logger.debug('[ Sending command took %f sec ]' % (t1 - t0))
        try:
            task_low = cmd_low.next()
        except:
            cmd_low = None

        try:
            sensor_read = sensors.next()
        except:
            sensor_read = None

        # execute all fast tasks
        for task_high in cmd_high:
            task = task_high
            if task:
                logger.debug('Detected a task scheduled')

                write_task(task)

        # execute one slow task
        if cmd_low:
            read_task(task_low)

        if sensor_read:
            sense(sensor_read)

logger.warn('Initializing Serial Worker.')
worker()
