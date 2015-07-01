#!/usr/bin/python
"""Testing File

Example of a Metro Daemon with 10 priority queues

"""

import serial
from metro import sendHex, sendHexNoReturn, makeCommand, readCommand

from libmadli import getCommandNumber

from time import time, sleep

import itertools, sys


serObj = serial.Serial('/dev/ttyAMA0',
                       baudrate=4800,
                       bytesize=serial.EIGHTBITS,
                       parity=serial.PARITY_NONE,
                       stopbits=serial.STOPBITS_ONE,
#                        timeout=1,
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
    return executeCommand('GetRam', lamp_number, range(address, address + 1))


def executeCommand(command_string, device_number, memory_range):

    time_debug = False

    # print "METER 0.3.1"
    # print
    # print command_string
    # print "-----------"
    # print "[ LOGS ]"
    # print

    command_number = getCommandNumber(command_string)

    t0 = time()
    for memory_address in memory_range:
        # print memory_address
        hexstr = makeCommand(command_number, 0, device_number, memory_address)

#        print "Lamp: " + str(device_number)
        lampData = ''
#        print "what we're sending"
#        print hexstr

        if command_string == "SetAddr" or command_string == "WriteAddr":
            value = shxNR(hexstr)
#            print "Getting: " + value
        else:
            value = shx(hexstr)
            # print readCommand(value)
#            print "Getting: " + value
            if(value):
                lampData = readCommand(value)

        # print value
        # if value:
        #    r_server.set("Warehouse:1:Device:" + str(device_number) + ":"+command_string+":" + str(memory_address), int("0x"+value[3:5],16))

    t1 = time()
    if time_debug:
        print "device_number: " + str(device_number)
        print '[ Sending command took %f sec ]' % (t1 - t0)
    t2 = time()
    if time_debug:
        print '[ Getting response took %f sec ]' % (t2 - t1)

    return lampData


def scanMadli(scanRange = range(1, 1023), skipLamps = []):
    scanSet = sorted(set(scanRange).difference(skipLamps))
    scanned = 0
    found = 0
#    dic = {}
    for lId in scanSet:
        slamp = getRamValue(lId, 0)
        if(slamp):
#            dic[i] = "Lamp id: " + str(i) + " " + str(slamp)
            print "Lamp id: " + str(lId) + " " + str(slamp)
            found += 1
        msg = "Checking lamp " + str(lId)
        sys.stdout.write(msg)  # write the next character
        sys.stdout.flush()  # flush stdout buffer (actual character display)
        sys.stdout.write('\b' * (len(msg)-1))  # erase the last written char
        scanned += 1
#        if(i % 10 == 0):
#            print i % 100
#            sleep(2)
#    print dic
    print "Scanned: " + str(scanned) + " lamps"
    print "Found: " + str(found) + " lamps"


lamp_num = 9

skipLamps = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 54, 61, 63, 77, 91, 93, 94, 96, 100, 105, 124, 125, 127, 128, 129, 130, 131, 132, 139, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 163, 164, 165, 166, 167, 168, 169, 170, 171, 202, 257, 264, 295, 297, 319, 326, 331, 335, 339, 341, 342, 343, 344, 346, 348, 349, 350, 353, 354, 355, 356, 357, 359, 360, 364, 391, 407, 409, 418, 421, 431, 432, 535, 539, 541, 556, 603, 622, 623, 625, 627, 666, 682, 687, 693, 696, 700, 707, 709, 711, 743, 770, 776, 785, 789, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 812, 813, 814, 815, 816, 817, 818, 820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 830, 831, 833, 834, 835, 836, 837, 838, 839, 841, 843, 844, 847, 848, 849, 850, 852, 853, 854, 876, 878, 880, 887, 893, 959, 969, 972]

scanFor = [111, 126, 862, 984, 843]
skip = [11, 984]
scanMadli(scanFor, skip)


"""
Turn on
"""


# turnOff(126)
# turnOn(126, 255)
# setDim(lamp_num, 0, 244)
# setDim(lamp_num, 0, 244)

"""
Reads Ram Value from a Lamp
"""

# getRamValue(843,0)


"""
send raw command, just 4 hexes
this one is basically the same as getRamValue(lamp_num,0)
"""
# print readCommand(shx("10 09 00 19"))
