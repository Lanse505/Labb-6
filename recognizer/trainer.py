###################################################################################################################
#                                   Produced for GMI2BT - Skriptprogrammering                                     #
#                                                                                                                 #
# Based off: https://github.com/Mjrovai/OpenCV-Face-Recognition/blob/master/FacialRecognition/02_face_training.py #
# Based off: https://github.com/thecodacus/Face-Recognition                                                       #
#                                                                                                                 #
###################################################################################################################

import cv2
import numpy as np
import os
from PIL import Image
import recognizer


# function to get the images and label data
def getImagesAndLabels(path: str, detector: cv2.CascadeClassifier):
    # Creates a list of all of the image paths based on the path string joint with each of the filenames.
    profilePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []  # Creates an empty list of faceSamples
    ids = []  # Creates an empty list for ids
    setId = 0
    for profile in profilePaths:  # Loops over all of the image paths
        for image_path in os.listdir(profile):
            # Opens the image using PIL#Image and converts it to a black and white 8-bit pixel image
            PIL_image = Image.open(profile + "/" + image_path).convert('L')
            # Converts the image to an numpy array consisting of uint8 values
            img_numpy = np.array(PIL_image, 'uint8')
            # Attempts to detect a face in the image
            faces = detector.detectMultiScale(img_numpy)
            for (xPos, yPos, width, height) in faces:  # Loops over the values in the detectMultiScale
                # If it detects a face then it appends it to the faceSamples array
                faceSamples.append(
                    img_numpy[yPos: yPos + height, xPos: xPos + width])
                ids.append(setId)  # Appends the id to the ids array
        setId += 1
    # Returns a tuple of faceSamples and ids once done
    return (faceSamples, ids)


def main(args: dict[str: any]):
    # Setups up our logger with the identity of Trainer
    logger = recognizer.logger.Logger(
        identity="Trainer", debugEnabled=args["debug"])
    path = args["dspath"]  # Grabs the dataset path from program arguments
    # Creates the recognizer using the LBPH template, See: https://docs.opencv.org/4.x/df/d25/classcv_1_1face_1_1LBPHFaceRecognizer.html for full documentation
    recog = cv2.face.LBPHFaceRecognizer_create()
    # Grabs the CascadeClassifier for our passed in Cascade path
    detector = cv2.CascadeClassifier(args["cascade"])

    # Informational logging
    logger.info(input="Training faces. It will take a few seconds. Wait...")
    # Calls getImagesAndLabels to attempt to get all of the faces and ids to learn.
    faces, ids = getImagesAndLabels(path=path, detector=detector)
    # Calls the train method of the LBPHFaceRecognizer to learn the faces and associated ids.
    recog.train(faces, np.array(ids))

    # Parses the path for the trainer.yml file
    path = args["tpath"] + "/trainer.yml"
    with open(file=path, mode='w', encoding='utf-8'):  # Makes sure the file gets generated
        recog.write(path)  # Writes the training data to the trainer.yml
    # Informational Logging
    logger.info(input=f"{len(np.unique(ids))} faces trained. Exiting Program")
