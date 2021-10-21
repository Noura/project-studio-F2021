from time import sleep, time

start_time = time()
def print_elapsed_time(msg):
    elapsed_time = time() - start_time
    print('% 12.2f' % elapsed_time, ' ', msg)

from PIL import Image
from picamera import PiCamera
import numpy as np
import face_recognition
import cv2
import tflite_runtime.interpreter as tflite
print_elapsed_time('imported libraries')


filename_base = 'output_images/image'
filename_ext = '.jpeg'
filename_count = 0

model_filename = "models/model.tflite"

emotion_dict = { \
                '0': 'Angry', \
                '1': 'Disgust', \
                '2': 'Fear', \
                '3': 'Happy', \
                '4': 'Neutral', \
                '5': 'Sad', \
                '6': 'Surprise'}

emotion_list = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

interpreter = tflite.Interpreter(model_path=model_filename)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_shape = input_details[0]['shape']
print_elapsed_time('created tflite emotion ml model')


camera = PiCamera()
print_elapsed_time('created camera = PiCamera()')

sleep(5)
print_elapsed_time('slept for 5 sec')


while filename_count < 10:

    filename = filename_base + str(filename_count) + filename_ext
    camera.capture(filename)
    filename_count += 1
    print_elapsed_time('took one snapshot saved to ' + filename)
    
    image = cv2.imread(filename)
    print_elapsed_time('read in the snapshot with CV2')
    
    # getting the bounding boxes of all faces detected
    # each element of this list is a tuple (top, right, bottom, left)
    face_locations = face_recognition.face_locations(image)
    print('face_locations:  ', face_locations)
    print_elapsed_time('detected the face')
    
    # getting the bounding box of the first face detected
    # this assumes a face was detected
    top, right, bottom, left = face_locations[0]
    
    # cropping the image to the face bounding box
    image_edited = image[top:bottom, left:right]
    print_elapsed_time('cropped image to the face')
    
    # resizing the image
    image_edited = cv2.resize(image_edited, (48,48))
    print_elapsed_time('resized image to 48 by 48')
    
    # make the image black and white
    image_edited = cv2.cvtColor(image_edited, cv2.COLOR_BGR2GRAY)
    print_elapsed_time('made the image black and white')
    
    # write the edited image to a file
    filename = filename_base + str(filename_count-1) + '_edited' + filename_ext
    cv2.imwrite(filename, image_edited)
    print_elapsed_time('saved the edited image to ' + filename)
    
    image_edited = np.reshape(image_edited, input_shape)
    print_elapsed_time('reshaped the image')
    
    image_edited = image_edited.astype('float32')
    print_elapsed_time('made the image float32')
    
    interpreter.set_tensor(input_details[0]['index'], image_edited )
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    print_elapsed_time('ran the emotion ML interpreter model on the image')
    
    print('output data ', output_data)
    
    # processing the output data to get the emotion name
    
    for i in range(7):
        print('Emotion ', emotion_list[i], ':  ', output_data[0][i])
    
    
    
    
    
