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


def executeCommand(command_string, device_number, memory_range):

    serObj = serial.Serial('/dev/ttyUSB0',
                           baudrate=4800,
                           bytesize=serial.EIGHTBITS,
                           parity=serial.PARITY_NONE,
                           stopbits=serial.STOPBITS_ONE,
                           timeout=1,
                           xonxoff=0,
                           rtscts=0
                           )

    command_number = getCommandNumber(command_string)

    for memory_address in memory_range:
        # print memory_addres
        hexstr = makeCommand(command_number, 0, device_number, memory_address)

        if command_string == "SetAddr" or command_string == "WriteAddr":
            value = shxNR(hexstr, serObj)
        else:
            value = shx(hexstr, serObj)
            return readCommand(value)


def setDim(lamp_number, dim_level):
    executeCommand('On', lamp_number, range(dim_level, dim_level + 1))
    executeCommand('On', lamp_number, range(dim_level, dim_level + 1))


def Off(lamp_number, dim_level):
    executeCommand('Off', lamp_number, range(dim_level, dim_level + 1))
    executeCommand('Off', lamp_number, range(dim_level, dim_level + 1))

def readValue(command, lamp_number, address):
    return executeCommand(command, lamp_number, range(address, address+1))

