import rethinkdb as r
conn = r.connect("localhost").repl()

db = r.db("engine")
lamps_table = db.table("lamps")

import logging
logger = logging.getLogger('button_worker')
logger.setLevel(logging.DEBUG)

hdlr = logging.FileHandler('logs/button_worker.log')

logger.addHandler(hdlr)

import wiringpi2
import time
from config import config

wiringpi2.wiringPiSetup()

pin_mapping = config['pin_mapping']
button_lamp_mapping = config['button_lamp_mapping']
button_states = config['button_states']

def change(button, state):
    lamp_numbers = button_lamp_mapping[button]
    for lamp_number in lamp_numbers:
        special_l_setting = 255
        if state:
            special_l_setting = 0

        new = dict(
            special_l_setting=special_l_setting,
            change_required=True
        )

        print lamps_table.filter({'hardware':{'address':str(lamp_number)}}).update(new)
        print lamps_table.filter({'hardware':{'address':str(lamp_number)}}).update(new).run(conn)


def check_pin(button):
    pin = pin_mapping[button]
    return wiringpi2.digitalRead(pin[2])


def listen_on_pins():
    for button, state in button_states.items():
        pin_now = check_pin(button)
        if pin_now != state:
            change(button, pin_now)
            button_states[button] = pin_now

while True:
    listen_on_pins()
    time.sleep(1)
