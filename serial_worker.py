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

db = r.db("engine")
lamps_table = db.table("lamps")
command_table = db.table("commands")
cursor = lamps_table.changes().run(conn)


def read_task(task):
    try:
        logger.debug('Trying to read the value')
        actual_driver_value = call(
            task['command'], task['lampNumber'], task['address'])
        lamp = dict(
            id=task['lamp_id'], actual_driver_value=actual_driver_value)
        logger.debug('Uploading value to rethink')
        lamps_table.filter(id=task['lamp_id']).update(lamp).run(conn)

        logger.debug('Uploaded value was: ' + str(actual_driver_value))
        command_table.get(task['id']).delete().run(conn)
    except Exception, e:
        logger.error('Error: ' + str(e))
        command_table.get(task['id']).delete().run(conn)


def write_task(task):
    try:
        logger.debug('Trying send fast command')
        call(task['command'], task['lampNumber'], task['address'])
        command_table.get(task['id']).delete().run(conn)
    except Exception, e:
        logger.error('Error: ' + str(e))
        command_table.get(task['id']).delete().run(conn)


def worker():

    while True:

        cmd_low = command_table.filter({'prio': 'low'}).limit(1).run(conn)
        cmd_high = command_table.filter({'prio': 'high'}).run(conn)

        try:
            task_low = cmd_low.next()
        except:
            cmd_low = None

        # execute all fast tasks
        for task_high in cmd_high:
            task = task_high
            if task:
                logger.debug('Detected a task scheduled')
                # try:
                write_task(task)
                # except Exception, e:
                #    logger.error(e)

        # execute one slow task
        if cmd_low:
            # try:
            read_task(task_low)
        #   except Exception, e:
        #       logger.error(e)


logger.warn('Initializing Serial Worker.')
worker()
