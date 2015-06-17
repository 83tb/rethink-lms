import wiringpi2

wiringpi2.wiringPiSetup()
print "Pin 29 (21 -40) - " + str(wiringpi2.digitalRead(29)) # Read pin 21
print "Pin 25 (26 - 37) - " + str(wiringpi2.digitalRead(25)) # Read pin 13
print "Pin 24 (19 - 35) - " + str(wiringpi2.digitalRead(24)) # Read pin 19
print "Pin 23 (13 - 33) - " + str(wiringpi2.digitalRead(23)) # Read pin 26
print "Pin 22 (6 - 31) - " + str(wiringpi2.digitalRead(22)) # Read pin 26
print "Pin 21 (5 - 29) - " + str(wiringpi2.digitalRead(21)) # Read pin 26
print "Pin 14 (11 - 23) - " + str(wiringpi2.digitalRead(14)) # Read pin 26
print "Pin 13 (9 - 21) - " + str(wiringpi2.digitalRead(13)) # Read pin 26


