import board
import digitalio
import neopixel
import time
import keypad
from adafruit_emc2101 import EMC2101

i2c = board.I2C()  # uses board.SCL and board.SDA
emc = EMC2101(i2c)

powerMeter = neopixel.NeoPixel(board.A2, 8)

keys = keypad.Keys((board.A0, board.A1), value_when_pressed=True, pull=True)

fanValue = 0.0
stripValue = 0

# This adds 1/8 of a power level to the fan
def stepUp(currentValue):
    currentValue += 12.5
    if currentValue > 100:
        currentValue = 100
    return currentValue


# This subtracts 1/8 of a power level from the fan
def stepDown(currentValue):
    currentValue -= 12.5
    if currentValue < 0:
        currentValue = 0
    return currentValue


# This increments the led level of the led strip
def incrementStrip(stripLevel):
    stripLevel += 1
    if stripLevel >= 7:
        stripLevel = 7
    return stripLevel


# This decrements the led level of the led strip
def decrementStrip(stripLevel):
    stripLevel -= 1
    if stripLevel <= 0:
        stripLevel = 0
    return stripLevel


# This sets the color for each LED in the strip
def colorManager(stripLevel):
    r = 255 - ((255 / 8) * stripLevel)
    g = 0 + (255 / 8 * stripLevel)
    b = 0
    return r, g, b


print("loop starting")
while True:
    event = keys.events.get()
    if event:
        if event.pressed:
            if event.key_number == 0:
                fanValue = stepUp(fanValue)
                emc.manual_fan_speed = fanValue

                colors = colorManager(stripValue)
                powerMeter[stripValue] = colors
                powerMeter.show
                stripValue = incrementStrip(stripValue)
            if event.key_number == 1:

                fanValue = stepDown(fanValue)
                emc.manual_fan_speed = fanValue

                powerMeter[stripValue] = (0, 0, 0)
                powerMeter.show
                stripValue = decrementStrip(stripValue)

time.wait(0.05)
