#+-----+-----+---------+------+---+---Pi 2---+---+------+---------+-----+-----+
# | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
# +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
# |     |     |    3.3v |      |   |  1 || 2  |   |      | 5v      |     |     |
# |   2 |   8 |   SDA.1 |   IN | 1 |  3 || 4  |   |      | 5V      |     |     |
# |   3 |   9 |   SCL.1 |   IN | 1 |  5 || 6  |   |      | 0v      |     |     |
# |   4 |   7 | GPIO. 7 |   IN | 1 |  7 || 8  | 1 | ALT0 | TxD     | 15  | 14  |
# |     |     |      0v |      |   |  9 || 10 | 1 | ALT0 | RxD     | 16  | 15  |
# |  17 |   0 | GPIO. 0 |   IN | 0 | 11 || 12 | 0 | IN   | GPIO. 1 | 1   | 18  |
# |  27 |   2 | GPIO. 2 |   IN | 0 | 13 || 14 |   |      | 0v      |     |     |
# |  22 |   3 | GPIO. 3 |   IN | 0 | 15 || 16 | 0 | IN   | GPIO. 4 | 4   | 23  |
# |     |     |    3.3v |      |   | 17 || 18 | 0 | IN   | GPIO. 5 | 5   | 24  |
# |  10 |  12 |    MOSI |   IN | 0 | 19 || 20 |   |      | 0v      |     |     |
# |   9 |  13 |    MISO |   IN | 0 | 21 || 22 | 0 | IN   | GPIO. 6 | 6   | 25  |
# |  11 |  14 |    SCLK |   IN | 0 | 23 || 24 | 1 | IN   | CE0     | 10  | 8   |
# |     |     |      0v |      |   | 25 || 26 | 1 | IN   | CE1     | 11  | 7   |
# |   0 |  30 |   SDA.0 |   IN | 1 | 27 || 28 | 1 | IN   | SCL.0   | 31  | 1   |
# |   5 |  21 | GPIO.21 |   IN | 1 | 29 || 30 |   |      | 0v      |     |     |
# |   6 |  22 | GPIO.22 |   IN | 1 | 31 || 32 | 0 | IN   | GPIO.26 | 26  | 12  |
# |  13 |  23 | GPIO.23 |   IN | 0 | 33 || 34 |   |      | 0v      |     |     |
# |  19 |  24 | GPIO.24 |   IN | 0 | 35 || 36 | 0 | IN   | GPIO.27 | 27  | 16  |
# |  26 |  25 | GPIO.25 |   IN | 0 | 37 || 38 | 0 | IN   | GPIO.28 | 28  | 20  |
# |     |     |      0v |      |   | 39 || 40 | 0 | IN   | GPIO.29 | 29  | 21  |
# +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
# | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
# +-----+-----+---------+------+---+---Pi 2---+---+------+---------+-----+-----+


pins = [
#	[Physical, BCM, wPi]
#    [7, 4, 7, ''],
#    [11, 17, 0, 'use '],
#    [12, 18, 1, ''],
#    [13, 27, 2, ''],
#    [15, 22, 3, 'use '],
    [16, 23, 4, 'use '], 
    [18, 24, 5, 'use '],
#    
#    [21, 9, 13, 'SPI used'],
#    
    [22, 25, 6, 'use '], 
#    
#    [23, 11, 14, 'SPI used'],
#
    [29, 5, 21, 'use used'],
    [31, 6, 22, 'use used'],
#    [32, 12, 26, ''],
    [33, 13, 23, 'use used'],
#    [35, 19, 24, 'used'],
    [36, 16, 27, 'use '],
    [37, 26, 25, 'use used'],
#    [38, 20, 28, ''],
#    [40, 21, 29, 'used']
    ]

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

import wiringpi2

wiringpi2.wiringPiSetup()
#wiringpi2.wiringPiSetupGpio()
#wiringpi2.wiringPiSetupSys()
#wiringpi2.wiringPiSetupPhys()

for pin in pins:
#	[Physical, BCM, wPi]
    print pin[0]
    rpin = pin[2]
    wiringpi2.pinMode(rpin, 0);
    IOstate = wiringpi2.digitalRead(rpin);
    if IOstate:
	IO = color.BOLD + str(IOstate) + color.END
    else:
	IO = str(IOstate)
    print "Pin Physical " + str(pin[0]).rjust(2) + " (wPi " + str(pin[2]).rjust(2) + " BCM " + str(pin[1]).rjust(2) + ") - state: " + IO + " " + pin[3].ljust(8) + " " + str(wiringpi2.wpiPinToGpio(rpin)).rjust(2)


