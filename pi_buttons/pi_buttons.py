import RPi.GPIO as GPIO
from picamera import PiCamera
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Use pin 18 for activating LED
GPIO.setup(18, GPIO.OUT)

# Use pin 17 for button pressing
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

camera = PiCamera()
takePicture = False
pictureNum = 0

while(True):
    if(takePicture):
        # preview only shows on desktop view
        camera.start_preview()

        # turn on LED in button to show pic is being taken
        GPIO.output(18, GPIO.HIGH)

        # sleep for 5 to allow camera to adjust to light
        time.sleep(5)

        # image will be stored at below path
        camera.capture('/home/pi/Work/image' + str(pictureNum) + '.jpg')

        # turn off preview (only for desktop view)
        camera.stop_preview()

        # turn off LED after picture is taken
        GPIO.output(18, GPIO.LOW)

        pictureNum += 1
        takePicture = False
        continue
    else:
        btn = GPIO.input(17)

        # If button is pressed, take picture on next loop
        if(btn == GPIO.HIGH):
            takePicture = True
            continue

GPIO.cleanup()
