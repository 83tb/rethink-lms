import rethinkdb as r
import logging
import wiringpi2
import time
from config import config

time.sleep(5)

conn = r.connect("localhost").repl()
db = r.db("engine")
lamps_table = db.table("lamps")

logger = logging.getLogger('button_worker2')
logger.setLevel(logging.DEBUG)
hdlr = logging.FileHandler('logs/button_worker2.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)

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
        change(button, button_states[button])


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
        logger.info("changing setting for lamp %s", lamp_number)
        special_l_setting = OFF_VALUE
        if state:
            special_l_setting = ON_VALUE

        new = dict(
            special_l_setting=special_l_setting,
            change_required=True
        )

        logger.debug("Sent to rethinkdb: %s", str(
            lamps_table.filter({'hardware': {'address': str(lamp_number)}}).update(new)))
        a = lamps_table.filter(
            {'hardware': {'address': str(lamp_number)}}).update(new).run(conn)
        logger.debug("Received from rethinkdb: %s", str(a))


def check_pin(button):
    pin = pin_mapping[button]
    return wiringpi2.digitalRead(pin[2])


def listen_on_pins():
    for button, state in button_states.items():
        pin_now = check_pin(button)
        if pin_now != state:
            logger.info("change on pin %s", button)
            change(button, pin_now)
            button_states[button] = pin_now


change(9, 1)

set_initial_button_states()
logger.info(str(button_states))
#while True:
#    listen_on_pins()
#    time.sleep(1)
