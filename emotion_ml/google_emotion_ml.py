from picamera import PiCamera
from time import sleep
import os
from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/pi/thematic-envoy-319518-95fe136b7595.json'

image_filename = '/home/pi/Desktop/image.jpg'

camera = PiCamera()

sleep(2) # to let the camera adjust to ambient light
camera.capture(image_filename)

with open(image_filename, 'rb') as image_file:
    image_content = image_file.read()

client = vision.ImageAnnotatorClient()

my_image = vision.Image(content=image_content)

response = client.face_detection(image=my_image)

print(response)

# Come up with a better way to display the results.
# Feel free to adapt the code from our prior Colab examples.
# You could start by using print(...) statements to print
# just the parts of the response you want to focus on.
# Then, use different camera effects depending on the response.