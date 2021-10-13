import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM) # use GPIO numbers instead of board numbers

my_pin = 17 # use GPIO pin 17

secs = 0 # how many seconds have elapsed, approximately
end_duration = 2 * 60  # running for a couple hours is plenty

GPIO.setup(my_pin, GPIO.OUT) # we are using this pin as an output

# our main code will loop for a long time
try: 
    while secs < end_duration:
        GPIO.output(my_pin, GPIO.LOW)
        sleep(1)
        GPIO.output(my_pin, GPIO.HIGH)
        sleep(1)
        secs = secs + 2


# when you press CTRL+C to exit, the program will go here 
except KeyboardInterrupt: 
    print('exited with keyboard interrupt')    

# when any other exception occurs, including errors, 
# the program will go here
except:
    print('a different exception occurred')

# the program will go here as the last thing before exiting
finally:
    GPIO.cleanup() # ensures a clean exit with the pins

