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

## Limitations
The Raspberry Pi GPIO pins operate at 3.3V, therefore shields must also be 3.3V compatible.
If the shield uses the IOREF pin to determine logic voltage this should be ok however some shields may require 5V logic which may result in incorrect functioning or damage to the Raspbery Pi.

The analog inputs A0-7 can only be used as inputs, not outputs (either digital or analog).
Inbuilt pull-up resistors are available on the digital IO pins (using INPUT_PULLUP) but are not available on the analog input pins.

Software PWM is supported on all digital outputs.
Hardware PWM is not available so shields which require high precision IO may not function correctly.
