from gpiozero import LED
from time import sleep

red = LED(17)
blue = LED(27)
green = LED(22)

while True:
    red.on()
    sleep(.05)
    blue.on()
    sleep(.05)
    green.on()
    sleep(.05)
    red.off()
    sleep(.05)
    blue.off()
    sleep(.05)
    green.off()
    sleep(.05)