import gpiozero
from time import sleep

led = gpiozero.RGBLED("GPIO18", "GPIO17", "GPIO27")

while True:
    led.color = (0, 0, 0)
    sleep(1)
    led.color = (1, 0, 0)
    sleep(1)
    led.color = (0, 1, 0)
    sleep(1)
    led.color = (0, 0, 1)
    sleep(1)




