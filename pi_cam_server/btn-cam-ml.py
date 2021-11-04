import io
from picamera import PiCamera
from google.cloud import vision
import time
import random
import json
import RPi.GPIO as GPIO

from functions import *

SERVER_FOLDER = 'SHARE'
FILE_EXT = '.jpg'

ledPin = 12
btnPin = 4

# set up GPIIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(btnPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

ledPwm = GPIO.PWM(ledPin, 1000)
ledPwm.start(0)
camera = PiCamera()

ledPercentage = 100.0
takingPicture = False
imgNumber = 0


def __img_file_name():
    global imgNumber
    return str(imgNumber) + FILE_EXT


def __img_file_path():
    return '/home/pi/' + SERVER_FOLDER + '/' + __img_file_name()


def __json_file_path():
    global imgNumber
    return '/home/pi/' + SERVER_FOLDER + '/' + str(imgNumber) + '.json'


def take_picture():
    global takingPicture
    global imgNumber

    takingPicture = True

    # blink the LED  to show the picture is being taken
    camera.start_preview()
    print('Taking picture in 5...')
    ledPwm.ChangeDutyCycle(0)
    time.sleep(.5)
    ledPwm.ChangeDutyCycle(100)
    time.sleep(.5)
    print('4...')
    ledPwm.ChangeDutyCycle(0)
    time.sleep(.5)
    ledPwm.ChangeDutyCycle(100)
    time.sleep(.5)
    print('3...')
    ledPwm.ChangeDutyCycle(0)
    time.sleep(.5)
    ledPwm.ChangeDutyCycle(100)
    time.sleep(.5)
    print('2...')
    ledPwm.ChangeDutyCycle(0)
    time.sleep(.5)
    ledPwm.ChangeDutyCycle(100)
    time.sleep(.5)
    print('1...')
    ledPwm.ChangeDutyCycle(0)
    time.sleep(.5)
    ledPwm.ChangeDutyCycle(100)
    time.sleep(.5)
    print('takin pic')
    ledPwm.ChangeDutyCycle(0)
    camera.capture(__img_file_path())
    camera.stop_preview()

    ledPwm.ChangeDutyCycle(100)
    time.sleep(0.25)
    ledPwm.ChangeDutyCycle(0)
    time.sleep(0.25)
    ledPwm.ChangeDutyCycle(100)
    time.sleep(0.25)
    ledPwm.ChangeDutyCycle(0)
    time.sleep(0.25)
    ledPwm.ChangeDutyCycle(100)

    # Loads the image into memory
    with io.open(__img_file_path(), 'rb') as image_file:
        # Names of likelihood from google.cloud.vision.enums
        likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                           'LIKELY', 'VERY_LIKELY')
        max_results = 1
        results = detect_face(image_file, max_results)
        faces = results.face_annotations

        if(len(faces) <= 0):
            print('No faces detected!')

        for face in faces:
            print('face detected, checking for emotions...')

            anger_likelihood = likelihood_name[face.anger_likelihood]
            joy_likelihood = likelihood_name[face.joy_likelihood]
            surprise_likelihood = likelihood_name[face.surprise_likelihood]
            sorrow_likelihood = likelihood_name[face.sorrow_likelihood]

            # print("BEFORE")
            # print('anger: {}'.format(anger_likelihood))
            # print('joy: {}'.format(joy_likelihood))
            # print('surprise: {}'.format(surprise_likelihood))
            # print('sorrow: {}'.format(sorrow_likelihood))

            should_randomize = randomize_emotions({
                anger_likelihood,
                joy_likelihood,
                surprise_likelihood,
                sorrow_likelihood
            })

            if(should_randomize is True):
                random_num = random.randrange(0, 4)
                if(random_num == 0):
                    anger_likelihood = "VERY_LIKELY"
                elif(random_num == 1):
                    joy_likelihood = "VERY_LIKELY"
                elif(random_num == 2):
                    surprise_likelihood = "VERY_LIKELY"
                elif(random_num == 3):
                    sorrow_likelihood = "VERY_LIKELY"

            # print("AFTER RANDOM CHECK")
            # print('anger: {}'.format(anger_likelihood))
            # print('joy: {}'.format(joy_likelihood))
            # print('surprise: {}'.format(surprise_likelihood))
            # print('sorrow: {}'.format(sorrow_likelihood))

            # write json file with detections
            emotions = {
                'anger': anger_likelihood,
                'joy': joy_likelihood,
                'surprise': surprise_likelihood,
                'sorrow': sorrow_likelihood
            }

            print('saving emotions to json file: ' + __json_file_path())
            with open(__json_file_path(), 'w', encoding='utf-8') as f:
                json.dump(emotions, f, ensure_ascii=False, indent=4)

        imgNumber += 1
        takingPicture = False


print('Starting...')
try:
    print('Waiting for button...')
    while(True):
        if GPIO.input(btnPin) == GPIO.HIGH and takingPicture is False:
            ledPercentage = 0.0
            print('Button was pushed!')
            take_picture()
        else:
            # Pulse the LED while waiting for a button press
            ledPercentage = ledPercentage - 25.0
            if(ledPercentage < 0.0):
                ledPercentage = 100.0

            time.sleep(0.4)
            ledPwm.ChangeDutyCycle(ledPercentage)
            print('.')

except KeyboardInterrupt:
    print('exiting...')
    ledPwm.stop()
    GPIO.cleanup()
    exit()
