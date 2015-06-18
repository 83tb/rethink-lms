from metro.metro import sendHex, sendHexNoReturn, makeCommand, readCommand
from metro.libmadli import getCommandNumber


def shxNR(arg, serObj):
    hexstr = arg
    # print "Sending: " + hexstr
    return sendHexNoReturn(hexstr, serObj)


def shx(arg, serObj):

    hexstr = arg
    # print "Sending: " + hexstr
    return sendHex(hexstr, serObj)

import serial

"""
serObj = serial.Serial('/dev/ttyUSB0',
                           baudrate=4800,
                           bytesize=serial.EIGHTBITS,
                           parity=serial.PARITY_NONE,
                           stopbits=serial.STOPBITS_ONE,
                           timeout=1,
                           xonxoff=0,
                           rtscts=0
                           )
"""

from time import time
def executeCommand(command_string, device_number, memory_range, fast=True):


    serObj = serial.Serial('/dev/ttyUSB0',
                           baudrate=4800,
                           bytesize=serial.EIGHTBITS,
                           parity=serial.PARITY_NONE,
                           stopbits=serial.STOPBITS_ONE,
                           timeout=1,
                           xonxoff=0,
                           rtscts=0
                           )

    time_debug = True

    # print "METER 0.3.1"
    # print
    # print command_string
    # print "-----------"
    # print "[ LOGS ]"
    # print
    t0 = time()

    command_number = getCommandNumber(command_string)

    for memory_address in memory_range:
        # print memory_address
        hexstr = makeCommand(command_number, 0, device_number, memory_address)

        print "what we're sending"
        print hexstr

        if command_string == "On" or command_string == "Off":
            value = shxNR(hexstr, serObj)

        else:
            value = shx(hexstr, serObj)
            # print readCommand(value)
            return readCommand(value)
        # print "Getting: " + value

        # print value
        # if value:
        #    r_server.set("Warehouse:1:Device:" + str(device_number) + ":"+command_string+":" + str(memory_address), int("0x"+value[3:5],16))

    t1 = time()
    if time_debug:
        print '[ Sending command took %f sec ]' % (t1 - t0)

    t2 = time()
    if time_debug:
        print '[ Getting response took %f sec ]' % (t2 - t1)



def setDim(lamp_number, dim_level):
    executeCommand('On', lamp_number, range(dim_level, dim_level + 1))
    executeCommand('On', lamp_number, range(dim_level, dim_level + 1))


def Off(lamp_number, dim_level):
    executeCommand('Off', lamp_number, range(dim_level, dim_level + 1))
    executeCommand('Off', lamp_number, range(dim_level, dim_level + 1))

import logging
logger = logging.getLogger('serial_worker')
logger.setLevel(logging.DEBUG)

hdlr = logging.FileHandler('logs/serial_worker.log')

logger.addHandler(hdlr)


def call(command, lamp_number, address):
    logger.debug("Executing command: " + str(command))
    if command == "Off" or command == "On":
        executeCommand(command, lamp_number, range(address-1, address))
        executeCommand(command, lamp_number, range(address-1, address))
    
    else:
        return executeCommand(command, lamp_number, range(address-1, address), fast=False)
