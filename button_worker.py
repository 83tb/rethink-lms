import rethinkdb as r
conn = r.connect("localhost").repl()

db = r.db("engine")
lamps_table = db.table("lamps")

import logging
logging.basicConfig(format='%(asctime)s %(message)s')

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

# temporary, this is not a configuration
button_states = {}

ON_VALUE = config['ON_VALUE']
OFF_VALUE = config['OFF_VALUE']



def set_initial_button_states():
    for button, pin_config in pin_mapping.items():
        button_states[button] = wiringpi2.digitalRead(pin_config[2])

def judge_rules(active_state, current_state):
    if active_state:
        return current_state
    else:
        return not current_state



def change(button, current_state):
    lamp_numbers = button_lamp_mapping[button]
    active_state = pin_mapping[button][3]
    state = judge_rules(active_state, current_state)

    for lamp_number in lamp_numbers:
        special_l_setting = OFF_VALUE
        if state:
            special_l_setting = ON_VALUE

        new = dict(
            special_l_setting=special_l_setting,
            change_required=True
        )


        lamps_table.filter({'hardware':{'address':str(lamp_number)}}).update(new).run(conn)


def check_pin(button):
    pin = pin_mapping[button]
    return wiringpi2.digitalRead(pin[2])


def listen_on_pins():
    for button, state in button_states.items():
        pin_now = check_pin(button)
        if pin_now != state:
            change(button, pin_now)
            button_states[button] = pin_now


set_initial_button_states()
while True:
    listen_on_pins()
    time.sleep(1)
