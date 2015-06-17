import logging

from madli import *

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )
import rethinkdb as r
conn = r.connect("localhost").repl()

db = r.db("engine")
lamps_table = db.table("lamps")
command_table = db.table("commands")
cursor = lamps_table.changes().run(conn)


def read_task(task):
    try:
        logging.debug('Trying to read the value')
        actual_driver_value = call(task['command'], task['lampNumber'], task['address']).get('data1')
        lamp = dict(id=task['lamp_id'], actual_driver_value=actual_driver_value)
        logging.debug('Uploading value to rethink')
        lamps_table.update(lamp).run(conn)

        logging.debug('Uploaded value was: ' + str(actual_driver_value))
        command_table.get(task['id']).delete().run(conn)
    except Exception(), e:
        logging.error('Error: ' + e)


def write_task(task):
    try:
        logging.debug('Trying send fast command')
        call(task['command'], task['lampNumber'], task['address']).get('data1')
        command_table.get(task['id']).delete().run(conn)
    except Exception(), e:
        logging.error('Error: ' + e)


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
                logging.debug('Detected a task scheduled')

                write_task(task)

        # execute one slow task
        if cmd_low:
            read_task(task_low)





worker()
