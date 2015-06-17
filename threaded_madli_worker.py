# coding: utf-8

from madli import *

import rethinkdb as r
conn = r.connect("localhost").repl()

db = r.db("engine")
lamps_table = db.table("lamps")
cursor = lamps_table.changes().run(conn)

import logging
import threading
import time

lock = threading.Lock()
slow_reads = []

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )


def quick_commands():
    for feed in cursor:
        logging.debug('New change in Rethink DB detected!')
        with lock:
            logging.debug(feed)
            old_lamp = feed['old_val']
            lamp = feed['new_val']
                
            lamp['scheduled_read'] = True
            if lamp['scheduled_read']:
                logging.debug('Read scheduled detected')

                slow_reads.append(dict(command="GetRam", lampNumber=lamp['hardware']['address'], address=1, id=lamp['id']))    
                lamp['scheduled_read'] = False
                lamp['change_required'] = False
                
                lamps_table.update(lamp).run(conn)            
            if old_lamp['special_l_setting'] != lamp['special_l_setting']:
                logging.debug('User wants to change the lightning level!')
 
                if old_lamp['special_l_setting'] != lamp['special_l_setting']:
                    lamp['wanted_l_level'] = lamp['special_l_setting']
                
import time
def slow_commands():
    while True:
        time.sleep(10)
        with lock:
            if slow_reads:
                task = slow_reads.pop()
                if task:
                    try:
                        actual_driver_value = readValue(task['command'], task['lampNumber'], task['address']).get('data1')
                        lamp = dict(id=task['id'], actual_driver_value=actual_driver_value)
                        lamp['change_required'] = False

                        lamps_table.update(lamp).run(conn)            

                        print actual_driver_value
                    except Exception(), e:
                        print e
                        
                                        


def writes():
    logging.debug('Starting')
    slow_commands()
    logging.debug('Exiting')


def reads():
    logging.debug('Starting')
    quick_commands()
    logging.debug('Exiting')

writes = threading.Thread(name='writes', target=writes)
reads = threading.Thread(name='reads', target=reads)

writes.start()
reads.start()
