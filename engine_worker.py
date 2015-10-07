# coding: utf-8

import logging
import rethinkdb as r

# NEW PUB SUB BEGIN
from config import config
amqp_address = config['rabbit_url']
from pubsub.notification_emiter import NotificationEmiter
emitter = NotificationEmiter(amqp_address)
topic = "commands"
#

conn = r.connect("localhost").repl()
db = r.db("engine")
lamps_table = db.table("lamps")


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
            logger.debug('Read scheduled detected')

            emitter.notify(topic, dict(type="write", command="GetRam", prio='low', lampNumber=lamp[
                                 'hardware']['address'], address=25, lamp_id=lamp['id']))

            lamp['scheduled_read'] = False
            lamp['change_required'] = False

            lamps_table.update(lamp).run(conn)
        if old_lamp['special_l_setting'] != lamp['special_l_setting']:
            logger.debug('User wants to change the lightning level!')

            lamp['wanted_l_level'] = lamp['special_l_setting']

            if lamp['wanted_l_level'] == 0:
                logger.debug('Turning lamp off')
                emitter.notify(topic, dict(type="write", command="Off", prio='high', lampNumber=lamp[
                                     'hardware']['address'], address=1, lamp_id=lamp['id']))

            else:
                logger.debug('Turning lamp on')
                emitter.notify(topic, dict(type="write", command="On", prio='high',
                                          lampNumber=lamp['hardware'][
                                              'address'], address=lamp['wanted_l_level'],
                                          lamp_id=lamp['id']))


logger.warn('Initializing Engine Worker.')
quick_commands()
