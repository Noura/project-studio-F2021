from PIL import Image
import numpy as np
import face_recognition
import cv2
import tflite_runtime.interpreter as tflite

image_filename = "images/image1.jpg"

model_filename = "models/model.tflite"



# DETECTING AND CROPPING FACES
# image = face_recognition.load_image_file("../image2.jpg")
image = cv2.imread(image_filename)

# getting the bounding boxes of all faces detected
# each element of this list is a tuple (top, right, bottom, left)
face_locations = face_recognition.face_locations(image)
print('face_locations:  ', face_locations)

# getting the bounding box of the first face detected
# this assumes a face was detected
top, right, bottom, left = face_locations[0]

# cropping the image to the face bounding box
image_edited = image[top:bottom, left:right]

# resizing the image
image_edited = cv2.resize(image_edited, (48,48))

# make the image black and white
image_edited = cv2.cvtColor(image_edited, cv2.COLOR_BGR2GRAY)

# write the image to a file
# cv2.imwrite('image_edited.jpg', image_edited)

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
print('interpreter:  ', interpreter)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
print('input details:  ', input_details)

output_details = interpreter.get_output_details()
print('output details:  ', output_details)

input_shape = input_details[0]['shape']
print('input shape:  ', input_shape)

image_edited = np.reshape(image_edited, input_shape)

image_edited = image_edited.astype('float32')

interpreter.set_tensor(input_details[0]['index'], image_edited )

interpreter.invoke()

output_data = interpreter.get_tensor(output_details[0]['index'])

print('output data ', output_data)

# processing the output data to get the emotion name

for i in range(7):
    print('Emotion ', emotion_list[i], ':  ', output_data[0][i])





