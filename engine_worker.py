# coding: utf-8

import logging
import rethinkdb as r

conn = r.connect("localhost").repl()
db = r.db("engine")
lamps_table = db.table("lamps")
command_table = db.table("commands")
cursor = lamps_table.changes().run(conn)

logger = logging.getLogger('engine_worker')
logger.setLevel(logging.DEBUG)
hdlr = logging.FileHandler('logs/engine_worker.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)


def quick_commands():

    for feed in cursor:
        logger.debug('New change in Rethink DB detected!')
        old_lamp = feed['old_val']
        lamp = feed['new_val']

        lamp['scheduled_read'] = lamp['change_required']
        if lamp['scheduled_read']:
#            logger.debug('Read scheduled detected')

            command_table.insert(dict(command="GetRam", prio='low', lampNumber=lamp[
                                 'hardware']['address'], address=25, lamp_id=lamp['id'])).run(conn)
            lamp['scheduled_read'] = False
            lamp['change_required'] = False

            lamps_table.update(lamp).run(conn)
        if old_lamp['special_l_setting'] != lamp['special_l_setting']:
            logger.debug('User wants to change lamp {} the lightning level!'.format(lamp['id']))

            lamp['wanted_l_level'] = lamp['special_l_setting']

            if lamp['wanted_l_level'] == 0:
                logger.debug('Turning off')
                command_table.insert(dict(command="Off", prio='high', lampNumber=lamp[
                                     'hardware']['address'], address=1, lamp_id=lamp['id'])).run(conn)

            else:
                logger.debug('Turning on')
                command_table.insert(dict(command="On", prio='high',
                                          lampNumber=lamp['hardware'][
                                              'address'], address=lamp['wanted_l_level'],
                                          lamp_id=lamp['id'])).run(conn)


logger.warn('Initializing Engine Worker.')
quick_commands()
