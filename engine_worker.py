# coding: utf-8



import rethinkdb as r
conn = r.connect("localhost").repl()

db = r.db("engine")
lamps_table = db.table("lamps")
command_table = db.table("commands")
cursor = lamps_table.changes().run(conn)

import logging



logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )


def quick_commands():

    for feed in cursor:
        logging.debug('New change in Rethink DB detected!')

        logging.debug('Obtaining lock for a quick command!')
        old_lamp = feed['old_val']
        lamp = feed['new_val']

        lamp['scheduled_read'] = lamp['change_required']
        if lamp['scheduled_read']:
            logging.debug('Read scheduled detected')

            command_table.insert(dict(command="GetRam", prio='low', lampNumber=lamp['hardware']['address'], address=1, lamp_id=lamp['id'])).run(conn)
            lamp['scheduled_read'] = False
            lamp['change_required'] = False

            lamps_table.update(lamp).run(conn)
        if old_lamp['special_l_setting'] != lamp['special_l_setting']:
            logging.debug('User wants to change the lightning level!')

            lamp['wanted_l_level'] = lamp['special_l_setting']

            if lamp['wanted_l_level'] == 0:
                logging.debug('Turning lamp off')
                command_table.insert(dict(command="Off", prio='high', lampNumber=lamp['hardware']['address'], address=1, lamp_id=lamp['id'])).run(conn)


            else:
                logging.debug('Turning lamp on')
                command_table.insert(dict(command="SetDim", prio='high',
                                          lampNumber=lamp['hardware']['address'], address=lamp['wanted_l_level'],
                                          lamp_id=lamp['id'])).run(conn)




import time
def slow_commands():

    while True:
        logging.debug('Going to sleep for 10 seconds')
        time.sleep(10)
        logging.debug('Waking up!')

        cmd = command_table.limit(1).run(conn)


        try:
            task = cmd.next()
        except:
            pass

        else:
            with lock:
                if task:
                    logging.debug('Detected a task scheduled')

                    if task:
                        logging.debug('Task is: ' + str(task))

                        try:
                            logging.debug('Trying to read the value')
                            actual_driver_value = readValue(task['command'], task['lampNumber'], task['address']).get('data1')
                            lamp = dict(id=task['lamp_id'], actual_driver_value=actual_driver_value)
                            logging.debug('Uploading value to rethink')
                            lamps_table.update(lamp).run(conn)

                            logging.debug('Uploaded value was: ' + str(actual_driver_value))
                            command_table.get(task['id']).delete().run(conn)
                        except Exception(), e:
                            logging.error('Error: ' + e)




def reads():
    logging.debug('Starting Read Process')
    slow_commands()
    logging.debug('Exiting')


def writes():
    logging.debug('Starting Write Process')
    quick_commands()
    logging.debug('Exiting')

writes = threading.Thread(name='writes', target=writes)
reads = threading.Thread(name='reads', target=reads)

writes.start()

reads.start()


