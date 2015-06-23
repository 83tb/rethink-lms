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

wiringpi2.wiringPiSetup()


button_lamp_mapping = {
    '19': [191,]
}

button_states = {
    '19': 0
}

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
        lamps_table.filter({'address' : lamp_number}).update(new)


def check_pin(button):
    return wiringpi2.digitalRead(button)


def listen_on_pins():
    for button, state in button_states.items():
        if check_pin(button) != state:
            change(button, state)
            button_states[button] = state

while True:
    listen_on_pins()
    time.sleep(1)
