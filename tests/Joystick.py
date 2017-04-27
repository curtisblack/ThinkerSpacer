import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# This is a sample script for reading the controller
# state of the Sparkfun Joystick Shield

from ThinkerSpacer import *

up = D4
down = D5
left = D6
right = D3

X = A1
Y = A0

pinMode(up, INPUT_PULLUP)
pinMode(down, INPUT_PULLUP)
pinMode(left, INPUT_PULLUP)
pinMode(right, INPUT_PULLUP)

while True:
    x = -1 + 2 * analogRead(X) / 1023.0
    y = -1 + 2 * analogRead(Y) / 1023.0
    print x, y

    if digitalRead(up) == LOW:
        print "UP Pressed"
    if digitalRead(down) == LOW:
        print "Down Pressed"
    if digitalRead(left) == LOW:
        print "Left Pressed"
    if digitalRead(right) == LOW:
        print "Right Pressed"
