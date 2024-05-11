import board
import digitalio
import neopixel
import time
import math
from adafruit_emc2101 import EMC2101

i2c = board.I2C()  # uses board.SCL and board.SDA

# pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
powerMeter = neopixel.NeoPixel(board.A2, 8)


emc = EMC2101(i2c)

button_up = digitalio.DigitalInOut(board.A0)
button_down = digitalio.DigitalInOut(board.A1)

# button = digitalio.DigitalInOut(board.A0)
button_up.switch_to_input(pull=digitalio.Pull.DOWN)
button_down.switch_to_input(pull=digitalio.Pull.DOWN)

fanValue = 0.0
stripValue = 0


def stepUp(currentValue):
    currentValue += 12.5
    if currentValue > 100:
        currentValue = 100
    return currentValue


def stepDown(currentValue):
    currentValue -= 12.5
    if currentValue < 0:
        currentValue = 0
    return currentValue


def incrementStrip(stripLevel):
    stripLevel += 1
    if stripLevel >= 7:
        stripLevel = 7
    return stripLevel


def decrementStrip(stripLevel):
    stripLevel -= 1
    if stripLevel <= 0:
        stripLevel = 0
    return stripLevel


def colorManager(stripLevel):
    
    if stripLevel == 0:
        stripLevel = 1  # To avoid logarithm of 0
        r = 255
        g = 0
        b = 0    
    else:
        r = 255 - ((255/8) * stripLevel)
        g = 0 + (255/8*stripLevel)
        #print(g)
        b = 0
    return r, g, b
    
def pulser(position, color = (0,0,0)):
    brightness = 0.5+(0.5*math.sin(2*time.monotonic()))
    # print(brightness)
    pulseColor = tuple(value * brightness for value in color)
    return pulseColor
  
    

print("loop starting")
while True:
    if button_up.value is True:
        
        fanValue = stepUp(fanValue)
        emc.manual_fan_speed = fanValue
        
        r, g, b = colorManager(stripValue)
        powerMeter[stripValue] = (r, g, b)
        powerMeter.show
        stripValue = incrementStrip(stripValue)
        
            
    elif button_down.value is True:
        fanValue = stepDown(fanValue)
        emc.manual_fan_speed = fanValue
        
        
        powerMeter[stripValue] = (0, 0, 0)
        powerMeter.show
        stripValue = decrementStrip(stripValue)
        
    time.sleep(0.05)
