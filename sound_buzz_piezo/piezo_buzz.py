import gpiozero
from time import sleep

piezo = gpiozero.PWMOutputDevice(17)
piezo.value = 0

vals = [0.1, 0.3, 0.25, 0.5, 0.45]

while True:
    for val in vals:
        piezo.value = val
        sleep(1)

#while True:
#    piezo.value = 0.25
#    sleep(1)
#    piezo.value = 0.5
#    sleep(1)

#while True:
#    val = 0.0
#    for i in range(10):
#        piezo.value = val
#        sleep(1)
#        val += 0.1

