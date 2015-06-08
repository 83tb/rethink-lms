import os
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.IN)

is_on = False

if (GPIO.input(18) == True):
    pass
else:
    pass


