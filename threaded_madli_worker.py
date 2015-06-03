# coding: utf-8

from madli import *

import rethinkdb as r
conn = r.connect( "localhost").repl()

lamps_table = r.db("engine").table("lamps")

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
        with lock:
            old_lamp = feed['old_val']
            lamp = feed['new_val']
            
            schedule_read = True
            if schedule_read:
                slow_reads.append(dict(command="Read"))    
            
            if old_lamp['wanted_l_level'] != lamp['wanted_l_level']:
                if lamp['wanted_l_level'] == 0:
                    Off(lamp['hardware']['address'], lamp['wanted_l_level'])
                else:
                    setDim(lamp['hardware']['address'], lamp['wanted_l_level'])

def slow_commands():
    while True:
        if not lock.locked():
            with lock:
                task = slow_reads.pop()
                if task:
                    # execute task
                    # write to rethink
                    pass
    


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
