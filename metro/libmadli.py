"""Metrolight main library


Place to hold static info about configs
"""



commands = {
    'On' : 0,
    'Off' : 1,
    'GetRam' : 2,
    'GetEE' : 3,
    'SetAddr' : 4,
    'SetGrp0' : 5,
    'SetGrp1' : 6,
    'SetGrp2' : 7,
    'SetGrp3' : 8,
    'Lock' : 9,
    'WriteAddr' : 10,
    'SetEEAddr' : 11,
    'SetEEData' : 12,
    'Test' : 13,
    'Prefix' : 14,
    }


st7st4 = {
    0: 'Ok',
    1: 'PFC High',
    2: 'PFC Low',
    3: 'Cap mode',
    4: 'Switch Off',
    5: 'Overtemperature',
    6: 'Extinguish',
    7: 'Vin low',
    8: 'Error'
}


st3st0 = {
    0: 'Off',
    1: 'Not ignite',
    2: 'Start',
    3: 'On',
    4: 'Cap test',
    5: 'Ignition',
    6: 'Warm-up',
    7: 'Normal',

}

def getSt3st0(number):
    return st3st0[number]

def getSt7st4(number):
    return st7st4[number]

def getCommandNumber(name):
    return commands[name]


