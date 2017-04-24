import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ThinkerSpacer import *

led1 = D8
led2 = D9
led3 = D10
led4 = D11
led5 = D12
led6 = D13
buzzer = D3
button = D7
pot = A5
ldr = A4

pinMode(led1, OUTPUT)
pinMode(led2, OUTPUT)
pinMode(led3, OUTPUT)
pinMode(led4, OUTPUT)
pinMode(led5, OUTPUT)
pinMode(led6, OUTPUT)
pinMode(buzzer, OUTPUT)
pinMode(button, INPUT)
pinMode(pot, INPUT)
pinMode(ldr, INPUT)

while True:
    ledState = ((millis() / 1000) % 2) == 0
    digitalWrite(led1, ledState)
    digitalWrite(led2, ledState)
    digitalWrite(led3, ledState)
    digitalWrite(led4, ledState)
    digitalWrite(led5, ledState)
    digitalWrite(led6, ledState)
    if digitalRead(button):
        tone(buzzer, 262)
    else:
        noTone(buzzer)
                    
