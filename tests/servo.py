import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ThinkerSpacer import *

servo = D10

# Setup the servo. We don't need to call pinMode for servos.
pinMode(servo, OUTPUT)

# Define the min and max pulse time in microseconds
servoMin = 1000
servoMax = 2000
servoStop = 1500

while True:
    servoWrite(servo, servoMin)
    delay(1000)
    servoWrite(servo, servoMax)
    delay(1000)
    servoWrite(servo, servoStop)
    delay(1000)
