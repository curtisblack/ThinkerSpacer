import RPi.GPIO as _GPIO
import time as _time

_GPIO.setmode(_GPIO.BCM)
_GPIO.setwarnings(False)

# convert from arduino pins to raspberry pi BCM pin numbers

# I2C
SDA = 2
SCL = 3

# Serial
TX = 14
RX = 15

# Digital Input/Output
D0 = RX
D1 = TX
D2 = SDA
D3 = SCL
D4 = 4
D5 = 5
D6 = 6
D7 = 12
D8 = 13
D9 = 16
D10 = 17
D11 = 19
D12 = 20
D13 = 21
#D14 = 22
#D15 = 23
#D16 = 18

_digitalPins = [D0, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13]

# Analog Input
A0 = 30 # D14
A1 = 31 # D15
A2 = 32 # D16
A3 = 33 # D17
A4 = 34 # D18
A5 = 35 # D19
A6 = 36 # D4
A7 = 37 # D6

_analogPins = [A0, A1, A2, A3, A4, A5, A6, A7]
_analogChannels = { A0: 0,
                    A1: 1,
                    A2: 2,
                    A3: 3,
                    A4: 4,
                    A5: 5,
                    A6: 6,
                    A7: 7 }

# ADC
_CLK = 24
_DOUT = 25
_DIN = 26
_CS = 27
_SPIMOSI = _DIN
_SPIMISO = _DOUT
_SPICLK = _CLK
_SPICS = _CS

# Arduino constants
INPUT = _GPIO.IN
OUTPUT = _GPIO.OUT
INPUT_PULLUP = None

HIGH = True
LOW = False

# set up the SPI interface pins
_GPIO.setup(_SPIMOSI, _GPIO.OUT)
_GPIO.setup(_SPIMISO, _GPIO.IN)
_GPIO.setup(_SPICLK, _GPIO.OUT)
_GPIO.setup(_SPICS, _GPIO.OUT)

# store the pwm outputs
_outputs = {}

import atexit as _atexit
def cleanup():
    for o in _outputs:
        _outputs[o].stop()
    _outputs.clear()
    _GPIO.cleanup()
_atexit.register(cleanup)

def _isAnalogInput(pin):
    return pin in _analogPins

# Arduino functions

def pinMode(pin, mode):
    if pin not in _digitalPins and pin not in _analogPins:
        raise ValueError("pin must be one of the digital or analog pins.")
    if mode == OUTPUT:
        if pin not in _outputs:
            _GPIO.setup(pin, mode)
            _outputs[pin] = _GPIO.PWM(pin, 50) # 50 Hz works for most servos
            _outputs[pin].start(0)
    elif mode == INPUT:
        if pin in _outputs:
            _outputs[pin].stop()
            _outputs.pop(pin)
        _GPIO.setup(pin, mode)
    elif mode == INPUT_PULLUP:
        if pin in _outputs:
            _outputs[pin].stop()
            _outputs.pop(pin)
        _GPIO.setup(pin, _GPIO.IN, pull_up_down = _GPIO.PUD_UP)

def analogRead(pin):
    # read SPI data from MCP3008 chip,
    # 8 possible adc's (0 thru 7)

    if not _isAnalogInput(pin):
        raise ValueError("analogRead() is only supported for analog input pins A0-7.")

    adcnum = _analogChannels[pin]

    _GPIO.output(_SPICS, True)

    _GPIO.output(_SPICLK, False)  # start clock low
    _GPIO.output(_SPICS, False)   # bring CS low
 
    commandout = adcnum
    commandout |= 0x18  # start bit + single-ended bit
    commandout <<= 3    # we only need to send 5 bits here
    for i in range(5):
        if (commandout & 0x80):
            _GPIO.output(_SPIMOSI, True)
        else:
            _GPIO.output(_SPIMOSI, False)
        commandout <<= 1
        _GPIO.output(_SPICLK, True)
        _GPIO.output(_SPICLK, False)
 
    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
        _GPIO.output(_SPICLK, True)
        _GPIO.output(_SPICLK, False)
        adcout <<= 1
        if (_GPIO.input(_SPIMISO)):
            adcout |= 0x1
 
    _GPIO.output(_SPICS, True)
        
    adcout >>= 1       # first bit is 'null' so drop it
    return adcout

def analogWrite(pin, value):
    if value < 0 or value > 255:
        raise ValueError("value should be in the range [0, 255]")
    if pin in _outputs:
        _outputs[pin].ChangeFrequency(100)
        _outputs[pin].ChangeDutyCycle((value * 100) / 255)
    else:
        raise ValueError("Initialise pin with pinMode() before using analogWrite().")

def digitalWrite(pin, value):
    if pin in _outputs:
        _outputs[pin].ChangeDutyCycle(100 if value else 0)
    else:
        raise ValueError("Initialise pin with pinMode() before using digitalWrite().")

def digitalRead(pin):
    if pin in _analogPins:
        return analogRead(pin) > 1023 / 2
    elif pin in _digitalPins:
        return _GPIO.input(pin)
    else:
        raise ValueError("pin must be one of the digital or analog pins.")

def tone(pin, frequency, duration=None):
    if frequency <= 0:
        raise ValueError("frequency must be a positive number")
    if pin in _outputs:
        _outputs[pin].ChangeDutyCycle(50)
        _outputs[pin].ChangeFrequency(frequency)
        if duration != None:
            _time.sleep(duration / 1000.0)
            noTone(pin)
    else:
        raise ValueError("Initialise pin with pinMode() before using tone().")

def noTone(pin):
    if pin in _outputs:
        _outputs[pin].ChangeDutyCycle(0)
    else:
        raise ValueError("Initialise pin with pinMode() before using noTone().")

def delay(millis):
    _time.sleep(millis / 1000.0)

def millis():
    return int(_time.time() * 1000)

# I2C

class _I2C:
    def __init__(self):
        pass

    def begin(self, bus=1):
        import smbus
        try:
            self.i2c = smbus.SMBus(bus)
        except IOError:
            raise IOError("Please enable I2C in raspi-config and choose bus=1 for RPi v3+, bus=0 for RPi v1/2")
        
    def write(self, address, value):
        self.i2c.write_byte(address, value)

    def read(self, address):
        self.i2c.read_byte(address)

Wire = _I2C()

# Serial

class _Serial:
    def __init__(self):
        pass

    def begin(self, baud=9600):
        try:
            pass
        except IOError:
            raise IOError("Please enable Serial in raspi-config.")

Serial = _Serial()

# Helper functions

def servoWrite(pin, micros):
    if pin in _outputs:
        period = 1.0 / 50.0 * 1e6
        _outputs[pin].ChangeDutyCycle(100 * micros / period)
        _outputs[pin].ChangeFrequency(50)
    else:
        raise ValueError("Initialise pin with pinMode() before using servoWrite().")

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def mapRange(v, r1, r2):
    return (v-r1[0])/(r1[1]-r1[0]) * (r2[1]-r2[0]) + r2[0]
