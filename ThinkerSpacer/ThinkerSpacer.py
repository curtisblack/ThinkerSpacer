import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

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

# Analog Input
A0 = 0 # D14
A1 = 1 # D15
A2 = 2 # D16
A3 = 3 # D17
A4 = 4 # D18
A5 = 5 # D19
A6 = 6 # D4
A7 = 7 # D6

# ADC
CLK = 24
DOUT = 25
DIN = 26
CS = 27
SPIMOSI = DIN
SPIMISO = DOUT
SPICLK = CLK
SPICS = CS

# Arduino constants
INPUT = GPIO.IN
OUTPUT = GPIO.OUT
INPUT_PULLUP = None

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# store the pwm outputs
outputs = {}

def isAnalogInput(pin):
    return pin in [A0, A1, A2, A3, A4, A5, A6, A7]

# Arduino functions

def pinMode(pin, mode):
    if mode == OUTPUT:
        GPIO.setup(pin, mode)
        outputs[pin] = GPIO.PWM(pin, 100)
        outputs[pin].start(0)
    elif mode == INPUT:
        if pin in outputs:
            outputs[pin].stop()
            outputs.pop(pin)
        GPIO.setup(pin, mode)
    elif mode == INPUT_PULLUP:
        if pin in outputs:
            outputs[pin].stop()
            outputs.pop(pin)
        GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def analogRead(adcnum):
    # read SPI data from MCP3008 chip,
    # 8 possible adc's (0 thru 7)

    if not isAnalogInput(adcnum):
        return -1
    GPIO.output(SPICS, True)

    GPIO.output(SPICLK, False)  # start clock low
    GPIO.output(SPICS, False)   # bring CS low
 
    commandout = adcnum
    commandout |= 0x18  # start bit + single-ended bit
    commandout <<= 3    # we only need to send 5 bits here
    for i in range(5):
        if (commandout & 0x80):
            GPIO.output(SPIMOSI, True)
        else:
            GPIO.output(SPIMOSI, False)
        commandout <<= 1
        GPIO.output(SPICLK, True)
        GPIO.output(SPICLK, False)
 
    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
        GPIO.output(SPICLK, True)
        GPIO.output(SPICLK, False)
        adcout <<= 1
        if (GPIO.input(SPIMSIO)):
            adcout |= 0x1
 
    GPIO.output(SPICS, True)
        
    adcout >>= 1       # first bit is 'null' so drop it
    return adcout

def analogWrite(pin, value):
    if value < 0 or value > 255:
        return
    if pin in outputs:
        outputs[pin].ChangeFrequency(100)
        outputs[pin].ChangeDutyCycle((value * 100) / 255)

def digitalWrite(pin, value):
    if pin in outputs:
        outputs[pin].ChangeDutyCycle(100 if value else 0)

def digitalRead(pin):
    return GPIO.input(pin)

def tone(pin, frequency, duration=None):
    if pin in outputs:
        outputs[pin].ChangeDutyCycle(50)
        outputs[pin].ChangeFrequency(frequency)
        if duration != None:
            time.sleep(duration / 1000.0)
            noTone(pin)

def noTone(pin):
    if pin in outputs:
        outputs[pin].ChangeDutyCycle(0)

def delay(millis):
    time.sleep(millis / 1000.0)

# Helper functions

def servo(pin):
    pinMode(pin, OUTPUT)
    return GPIO.PWM(pin, 50)

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def mapRange(v, r1, r2):
    return (v-r1[0])/(r1[1]-r1[0]) * (r2[1]-r2[0]) + r2[0]
