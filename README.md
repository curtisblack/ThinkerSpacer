# ThinkerSpacer
This is a python module to allow the use of Arduino shields using the ThinkerSpacer board.

## Setup

## Usage

Once you import the library the functions mostly follow the Arduino API.

### Blink an LED
```python
from ThinkerSpacer import *

ledPin = D13

pinMode(ledPin, OUTPUT)

while True:
    digitalWrite(ledPin, HIGH)
    delay(1000)
    digitalWrite(ledPin, LOW)
    delay(1000)
```

