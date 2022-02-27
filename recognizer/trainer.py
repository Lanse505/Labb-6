###################################################################################################################
#                                   Produced for GMI2BT - Skriptprogrammering                                     #
#                                                                                                                 #
# Based off: https://github.com/Mjrovai/OpenCV-Face-Recognition/blob/master/FacialRecognition/02_face_training.py #
# Based off: https://github.com/thecodacus/Face-Recognition                                                       #
#                                                                                                                 #
###################################################################################################################

from typing import Any
import cv2
import face_off
import numpy as np
import os
from PIL import Image
import recognizer


# function to get the images and label data
def getImagesAndLabels(path: str, detector: cv2.CascadeClassifier):
  imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
  faceSamples = []
  ids = []
  for path in imagePaths:
    PIL_image = Image.open(path).convert('L')
    img_numpy = np.array(PIL_image, 'uint8')
    id = int(os.path.split(path)[1].split('.')[2])
    faces = detector.detectMultiScale(img_numpy)
    for (xPos, yPos, width, height) in faces:
      faceSamples.append(img_numpy[yPos : yPos + height, xPos : xPos + width])
      ids.append(id)
  return (faceSamples, ids)

def main(args: dict[str: any]):
  logger = recognizer.logger.Logger(identity="Trainer", debugEnabled=args["debug"])
  path = args["dspath"] # Grabs the dataset path from program arguments
  recog = cv2.face.LBPHFaceRecognizer_create() # Creates the recognizer using the LBPH template, See: https://docs.opencv.org/4.x/df/d25/classcv_1_1face_1_1LBPHFaceRecognizer.html for full documentation
  detector = cv2.CascadeClassifier(args["cascade"])

  logger.info(input="Training faces. It will take a few seconds. Wait...")
  faces, ids = getImagesAndLabels(path=path, detector=detector)
  recog.train(faces, np.array(ids))

  path = args["tpath"] + "/trainer.yml"
  with open(file=path, mode='w', encoding='utf-8'):
    pass
  recog.write(path)
  logger.info(input=f"{len(np.unique(ids))} faces trained. Exiting Program")