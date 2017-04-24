import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ThinkerSpacer import *

button = D4
led = D13

pinMode(button, INPUT)
pinMode(led, OUTPUT)

state = LOW

while True:
    s = digitalRead(button)
    digitalWrite(led, s)
    if s != state:
        state = s
        print state
        
