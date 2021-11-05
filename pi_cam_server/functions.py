import time
from PIL import Image, ImageDraw
from google.cloud import vision
import random


# fill in with random emotion detections if none are found by the API
# pass in all the detected likelihoods as a set, sets will remove any duplicate values
def randomize_emotions(unique_detected: set = {}):
    if(len(unique_detected) == 1):
        value = unique_detected.pop()
        if(value == "UNKNOWN" or value == "VERY_UNLIKELY"):
            return True

    elif(len(unique_detected) == 0):
        return True

    else:
        return False


def detect_face(face_file, max_results=4):
    """Uses the Vision API to detect faces in the given file.
    Args:
        face_file: A file-like object containing an image with faces.
    Returns:
        An array of Face objects with information about the picture.
    """
    client = vision.ImageAnnotatorClient()

    content = face_file.read()
    image = vision.Image(content=content)

    return client.face_detection(
        image=image, max_results=max_results)


def highlight_faces(image, faces, output_filename):
    """Draws a polygon around the faces, then saves to output_filename.
    Args:
      image: a file containing the image with the faces.
      faces: a list of faces found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the
          faces have polygons drawn around them.
    """
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    # Sepecify the font-family and the font-size
    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    for face in faces:
        anger_likelihood = likelihood_name[face.anger_likelihood]
        joy_likelihood = likelihood_name[face.joy_likelihood]
        surprise_likelihood = likelihood_name[face.surprise_likelihood]
        sorrow_likelihood = likelihood_name[face.sorrow_likelihood]

        print("BEFORE")
        print('anger: {}'.format(anger_likelihood))
        print('joy: {}'.format(joy_likelihood))
        print('surprise: {}'.format(surprise_likelihood))
        print('sorow: {}'.format(sorrow_likelihood))

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

        print("AFTER RANDOM CHECK")
        print('anger: {}'.format(anger_likelihood))
        print('joy: {}'.format(joy_likelihood))
        print('surprise: {}'.format(surprise_likelihood))
        print('sorow: {}'.format(sorrow_likelihood))

        box = [(vertex.x, vertex.y)
               for vertex in face.bounding_poly.vertices]
        draw.line(box + [box[0]], width=5, fill='#00ff00')

        # Place the confidence value/score of the detected faces above the
        # detection box in the output image
        draw.text(((face.bounding_poly.vertices)[0].x,
                   (face.bounding_poly.vertices)[0].y),
                  str(format(face.detection_confidence, '.3f')) + '%',
                  fill='#FFFF00')

        draw.text(((face.bounding_poly.vertices)[0].x,
                   (face.bounding_poly.vertices)[0].y + 20),
                  'joy: {}'.format(joy_likelihood),
                  fill='#FFFFFF')

        draw.text(((face.bounding_poly.vertices)[0].x,
                   (face.bounding_poly.vertices)[0].y + 40),
                  'surprise: {}'.format(surprise_likelihood),
                  fill='#FFFFFF')

        draw.text(((face.bounding_poly.vertices)[0].x,
                   (face.bounding_poly.vertices)[0].y + 60),
                  'anger: {}'.format(anger_likelihood),
                  fill='#FFFFFF')

        draw.text(((face.bounding_poly.vertices)[0].x,
                   (face.bounding_poly.vertices)[0].y + 80),
                  'sorrow: {}'.format(sorrow_likelihood),
                  fill='#FFFFFF')

    im.save(output_filename)
