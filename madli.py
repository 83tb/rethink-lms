#!/usr/bin/python
"""Testing File

Example of a Metro Daemon with 10 priority queues

"""

import serial
from metro.metro import sendHex, sendHexNoReturn, makeCommand, readCommand
from config import config

from metro.libmadli import getCommandNumber

serObj = serial.Serial(config['serial_port'],
                       baudrate=4800,
                       bytesize=serial.EIGHTBITS,
                       parity=serial.PARITY_NONE,
                       stopbits=serial.STOPBITS_ONE,
                       #timeout=1,
                       # Below works in madli test/madliscan
                       timeout=0.04,
                       writeTimeout=0.1,
                       xonxoff=0,
                       rtscts=0
                       )


def shxNR(arg):
    hexstr = arg
    # print "Sending: " + hexstr
    return sendHexNoReturn(hexstr, serObj)


def shx(arg):

    hexstr = arg
    # print "Sending: " + hexstr
    return sendHex(hexstr, serObj)



from time import time, sleep


def executeCommand(command_string, device_number, memory_range):

    time_debug = False

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

        # print "what we're sending"
        # print hexstr

        value = shx(hexstr)
            # print readCommand(value)
        # Check if value is returned before reading it
        if(value):
            return readCommand(value)
        # print "Getting: " + value

        # print value
        # if value:
        #    r_server.set("Warehouse:1:Device:" + str(device_number) + ":"+command_string+":" + str(memory_address), int("0x"+value[3:5],16))

    t1 = time()
    if time_debug:
        # print '[ Sending command took %f sec ]' % (t1 - t0)
        pass
    
    t2 = time()
    if time_debug:
        # print '[ Getting response took %f sec ]' % (t2 - t1)
        pass

def turnOn(lamp_number, dim_level):
    executeCommand('On', lamp_number, range(dim_level, dim_level + 1))
    print executeCommand('On', lamp_number, range(dim_level, dim_level + 1))


def turnOff(lamp_number):
    executeCommand('Off', lamp_number, range(0, 1))
    executeCommand('Off', lamp_number, range(0, 1))
    # sleep(1)


def setDim(lamp_number, dim_ad, dim_level):
    executeCommand('Lock', lamp_number, range(dim_ad, dim_ad + 1))
    executeCommand('SetEEAddr', lamp_number, range(dim_ad, dim_ad + 1))
    executeCommand('SetEEData', lamp_number, range(dim_level, dim_level + 1))
    # executeCommand('WriteAddr',lamp_number,range(dim_level,dim_level+1))


def getRamValue(lamp_number, address):
    print executeCommand('GetRam', lamp_number, range(address, address + 1))

import logging
logger = logging.getLogger('serial_worker')
logger.setLevel(logging.DEBUG)

hdlr = logging.FileHandler('logs/serial_worker.log')

logger.addHandler(hdlr)


def call(command, lamp_number, address):
    logger.debug("Executing command: " + str(command))
    executeCommand(command, lamp_number, range(address - 1, address))
    executeCommand(command, lamp_number, range(address - 1, address))





# setDim(lamp_num, 0, 244)
# setDim(lamp_num, 0, 244)

"""
Reads Ram Value from a Lamp
"""
# getRamValue(lamp_num,0)


"""
send raw command, just 4 hexes
this one is basically the same as getRamValue(lamp_num,0)
"""
# print readCommand(shx("10 09 00 19"))
