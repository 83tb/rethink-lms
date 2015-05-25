# coding: utf-8

from madli import *

import rethinkdb as r
conn = r.connect( "localhost").repl()

lamps_table = r.db("engine").table("lamps")

cursor = lamps_table.changes().run(conn)

for feed in cursor:
    old_lamp = feed['old_val']
    lamp = feed['new_val']

    if old_lamp['wanted_l_level'] != lamp['wanted_l_level']:

        if lamp['wanted_l_level'] == 0:
            Off(lamp['hardware']['address'], lamp['wanted_l_level'])
        else:
            setDim(lamp['hardware']['address'], lamp['wanted_l_level'])





