import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ThinkerSpacer import *

led = D13

pinMode(led, OUTPUT)

while True:
    digitalWrite(led, HIGH)
    delay(1000)
    digitalWrite(led, LOW)
    delay(1000)
