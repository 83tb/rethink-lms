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
                command_table.insert(dict(command="On", prio='high',
                                          lampNumber=lamp['hardware']['address'], address=lamp['wanted_l_level'],
                                          lamp_id=lamp['id'])).run(conn)



quick_commands()
