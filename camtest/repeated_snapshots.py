# testing how fast we can take pictures

from time import sleep, time

start_time = time()
def print_elapsed_time(msg):
    elapsed_time = time() - start_time
    print('% 12.2f' % elapsed_time, ' ', msg)

from picamera import PiCamera

print_elapsed_time('imported camera')

filename_base = 'image'
filename_ext = '.jpeg'
filename_count = 0

camera = PiCamera()
print_elapsed_time('camera = PiCamera()')

sleep(5)
print_elapsed_time('sleep for 5 sec')

while filename_count < 10:
    filename = filename_base + str(filename_count) + filename_ext
    camera.capture(filename)
    filename_count += 1

    print_elapsed_time('took one snapshot')
