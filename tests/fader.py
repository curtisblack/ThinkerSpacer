import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ThinkerSpacer import *

led = D13

pinMode(led, OUTPUT)

while True:
    for i in range(256):
        analogWrite(led, i)
        delay(2)
    for i in range(255, -1, -1):
        analogWrite(led, i)
        delay(2)
