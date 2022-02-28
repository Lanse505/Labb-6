###################################################################################################################
#                                   Produced for GMI2BT - Skriptprogrammering                                     #
#                                                                                                                 #
# Based off: https://github.com/Mjrovai/OpenCV-Face-Recognition/blob/master/FacialRecognition/02_face_training.py #
# Based off: https://github.com/thecodacus/Face-Recognition                                                       #
#                                                                                                                 #
###################################################################################################################

from typing import Any
import cv2
import numpy as np
import os
from PIL import Image
import recognizer


# function to get the images and label data
def getImagesAndLabels(path: str, detector: cv2.CascadeClassifier):
  imagePaths = [os.path.join(path, f) for f in os.listdir(path)] # Creates a list of all of the image paths based on the path string joint with each of the filenames.
  faceSamples = [] # Creates an empty list of faceSamples
  ids = [] # Creates an empty list for ids
  for path in imagePaths: # Loops over all of the image paths
    PIL_image = Image.open(path).convert('L') # Opens the image using PIL#Image and converts it to a black and white 8-bit pixel image
    img_numpy = np.array(PIL_image, 'uint8') # Converts the image to an numpy array consisting of uint8 values
    id = int(os.path.split(path)[1].split('.')[2]) # Grabs the ID from the image
    faces = detector.detectMultiScale(img_numpy) # Attempts to detect a face in the image
    for (xPos, yPos, width, height) in faces:
      faceSamples.append(img_numpy[yPos : yPos + height, xPos : xPos + width]) # If it detects a face then it appends it to the faceSamples array
      ids.append(id) # Appends the id to the ids array
  return (faceSamples, ids) # Returns a tuple of faceSamples and ids once done

def main(args: dict[str: any]):
  logger = recognizer.logger.Logger(identity="Trainer", debugEnabled=args["debug"]) # Setups up our logger with the identity of Trainer
  path = args["dspath"] # Grabs the dataset path from program arguments
  recog = cv2.face.LBPHFaceRecognizer_create() # Creates the recognizer using the LBPH template, See: https://docs.opencv.org/4.x/df/d25/classcv_1_1face_1_1LBPHFaceRecognizer.html for full documentation
  detector = cv2.CascadeClassifier(args["cascade"]) # Grabs the CascadeClassifier for our passed in Cascade path

  logger.info(input="Training faces. It will take a few seconds. Wait...") # Informational logging
  faces, ids = getImagesAndLabels(path=path, detector=detector) # Calls getImagesAndLabels to attempt to get all of the faces and ids to learn.
  recog.train(faces, np.array(ids)) # Calls the train method of the LBPHFaceRecognizer to learn the faces and associated ids.

  path = args["tpath"] + "/trainer.yml" # Parses the path for the trainer.yml file
  with open(file=path, mode='w', encoding='utf-8'): # Makes sure the file gets generated
    recog.write(path) # Writes the training data to the trainer.yml
  logger.info(input=f"{len(np.unique(ids))} faces trained. Exiting Program") # Informational Logging