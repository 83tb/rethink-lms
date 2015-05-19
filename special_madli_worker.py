# coding: utf-8

from metro.metro import sendHex, sendHexNoReturn, makeCommand, readCommand
from metro.libmadli import getCommandNumber

def shxNR(arg, serObj):
    hexstr = arg
    #print "Sending: " + hexstr
    return sendHexNoReturn(hexstr, serObj)


def shx(arg, serObj):

    hexstr = arg
    #print "Sending: " + hexstr
    return sendHex(hexstr, serObj)

import serial

def executeCommand(command_string, device_number, memory_range):


    serObj = serial.Serial('/dev/ttyUSB1',
                       baudrate=4800,
                       bytesize=serial.EIGHTBITS,
                       parity=serial.PARITY_NONE,
                       stopbits=serial.STOPBITS_ONE,
                       timeout=1,
                       xonxoff=0,
                       rtscts=0
                       )


    time_debug = False

    #print "METER 0.3.1"
    #print
    #print command_string
    #print "-----------"
    #print "[ LOGS ]"
    #print



    command_number = getCommandNumber(command_string)


    for memory_address in memory_range:
        #print memory_addres
        hexstr = makeCommand(command_number,0,device_number,memory_address)

        if command_string == "SetAddr" or command_string == "WriteAddr":
            value = shxNR(hexstr,serObj)
        else:
            value =  shx(hexstr,serObj)

def setDim(lamp_number, dim_level):
    executeCommand('On',lamp_number,range(dim_level,dim_level+1))
    executeCommand('On',lamp_number,range(dim_level,dim_level+1))

def Off(lamp_number, dim_level):
    executeCommand('Off',lamp_number,range(dim_level,dim_level+1))
    executeCommand('Off',lamp_number,range(dim_level,dim_level+1))

import rethinkdb as r
conn = r.connect( "localhost").repl()

lamps_table = r.db("engine").table("lamps")

cursor = lamps_table.changes().run(conn)

for feed in cursor:
    lamp = feed['new_val']
    print "Something changed and need to be changed? " + str(lamp['change_required'])
    if lamp['change_required'] == True:
        print lamp['special_l_setting']
        if lamp['special_l_setting']==0:
            Off(lamp['hardware']['address'], lamp['special_l_setting'])
        else:
            setDim(lamp['hardware']['address'], lamp['special_l_setting'])
        lamp['change_required'] = False
        lamps_table.update(lamp).run()


