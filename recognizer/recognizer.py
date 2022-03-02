##################################################################################################################
#                                   Produced for GMI2BT - Skriptprogrammering                                    #
#                                                                                                                #
# Based off: https://github.com/Mjrovai/OpenCV-Face-Recognition/blob/master/FacialRecognition/01_face_dataset.py #
# Based off: https://github.com/thecodacus/Face-Recognition                                                      #
#                                                                                                                #
##################################################################################################################

import cv2
import recognizer


def main(args: dict[str: any]):
    logger = recognizer.logger.Logger(
        identity="Recognizer", debugEnabled=args["debug"])  # Setups Logger
    # Creates the recognizer using the LBPH template, See: https://docs.opencv.org/4.x/df/d25/classcv_1_1face_1_1LBPHFaceRecognizer.html for full documentation
    recog = cv2.face.LBPHFaceRecognizer_create()
    recog.read(args['tpath'] + "/trainer.yml")
    # Detector to use, Path grabbed from program arguments
    detector = cv2.CascadeClassifier(args["cascade"])
    font = cv2.FONT_HERSHEY_SIMPLEX  # Font to use

    id = 0  # Id of Target

    names = ['Ben Affleck', "CohhCarnage", "Vladimir Putin",
             "Robert Downey Jr", "Simon"]  # Default Trained Targets

    cam = cv2.VideoCapture(0)  # Opens the Video Default Camera

    # Video Capture Values: https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
    cam.set(3, 640)  # 3 = Width
    cam.set(4, 480)  # 4 = Height

    # Sets the minimum width and height the detector can use as a target
    minWidth = 0.1 * cam.get(3)  # 3 = Width
    minHeight = 0.1 * cam.get(4)  # 4 = Height

    while True:
        # Grabs the current "return value" as well as the image.
        # The return value indicates if any images was captured, returns false in cases where the camera has been disconnected or there are no more frames in the video file.
        # See: https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html#a473055e77dd7faa4d26d686226b292c1 for full documentation
        ret, img = cam.read()

        # Flips the provided image in some way.
        # Takes in a src input, dst output and a flip-code
        # The flip-code indicates how the image should be flipped, where in:
        #
        # -1 = flip along both x-axis and y-axis
        # 0  = flip along x-axis (Vertical Flip)
        # 1  = flip along y-axis (Horizontal Flip)
        #
        # See: https://docs.opencv.org/3.4/d2/de8/group__core__array.html#gaca7be533e3dac7feb70fc60635adf441 for full documentation
        img = cv2.flip(img, 1)

        # Converts the image from BGR (BGR-Colored) into Grayscale
        # See: https://docs.opencv.org/3.4/d8/d01/group__imgproc__color__conversions.html#ga397ae87e1288a81d2363b61574eb8cab for full documentation
        gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)

        # Tries to detect any and all faces present in the Grayscale image using a scaleFactor of 1.3, a minNeighbor count of 5 and a minSize of minWidth and minHeight
        # For more information on valid inputs for detectMultiScale see: https://docs.opencv.org/3.4/da/dd5/classcv_1_1BaseCascadeClassifier.html#aa4c96739e441adda5005ae58fd95a5a2 for full documentation
        faces = detector.detectMultiScale(
            image=gray, scaleFactor=1.3, minNeighbors=5, minSize=(int(minWidth), int(minHeight)),)

        for(xPos, yPos, width, height) in faces:
            # Draws a rectangle over each face found by the face_detector using the positions found as well as the width and height.
            # It takes in the following values in order:
            #
            # img                                                                   = The original image to draw on
            # (xPos, yPos)                                                          = The first Vertex point of the rectangle (See https://www.mathopenref.com/vertex.html for info on Vertices)
            # (xPos + width + yPos + height)                                        = The second Vertex point of the rectangle
            # (args["recogRectRed"], args["recogRectGreen"], args["recogRectBlue"]) = The color for the rectangle to be rendered as, this takes the values passed in by the args parser defaulting to (255,0,0) or solid Red
            # 2                                                                     = The thickness of the rectangle lines
            #
            # See: https://docs.opencv.org/3.4/d6/d6e/group__imgproc__draw.html#ga07d2f74cadcf8e305e810ce8eed13bc9 for full documentation
            cv2.rectangle(img=img, pt1=(xPos, yPos), pt2=(xPos + width, yPos + height), color=(
                args["recogRectRed"], args["recogRectGreen"], args["recogRectBlue"]), thickness=2)

            # Asks the trained Recognizer to attempt to predict the target as well as the confidence of it's prediction
            id, confidence = recog.predict(
                gray[yPos: yPos + height, xPos: xPos + width])

            # If it tries to predict the target and recognizes it and provides a confidence value
            # Then it sets id to the name from the list and sets the confidence to a % value for printing on screen
            if (confidence < 100):
                # Grabs the name based off ID from the predefined list
                id = names[id]
                # Turns the confidence value into a % string value
                confidence = f"  {round(100 - confidence)}%"
            else:  # If unable to recognize the target
                id = "unknown"  # Name becomes unknown
                # Confidence on it being a face
                confidence = f"  {round(100 - confidence)}%"

            # Writes the recognized name
            cv2.putText(img, str(id), (xPos + 5, yPos - 5), font, 1, (int(
                args["recogTextBlue"]), int(args["recogTextGreen"]), int(args["recogTextRed"])), 2)
            # Writes the confidence value next to said name.
            cv2.putText(img, str(confidence), (xPos + 5, yPos + height - 5), font, 1, (int(
                args["recogTextConfBlue"]), int(args["recogTextConfGreen"]), int(args["recogTextConfRed"])), 1)

        # Displays the image with the found face
        # It takes in the following values in order:
        #
        # 'camera' = The name of the window
        # img     = The image data being passed in, in this case the non-grayscale image
        #
        # See: https://docs.opencv.org/3.4/d7/dfc/group__highgui.html#ga453d42fe4cb60e5723281a89973ee563 for full documentation
        cv2.imshow(winname='camera', mat=img)

        # Awaits any key being pressed for at least 10 ms or 0.01 seconds
        # See: https://docs.opencv.org/3.4/d7/dfc/group__highgui.html#ga5628525ad33f52eab17feebcfba38bd7 for full documentation on waitKey
        k = cv2.waitKey(10) & 0xff

        # If the key was 27 aka Esc then break
        if k == 27:
            break

    # Information Print about it shutting down
    logger.info(input="Exiting Program and doing Clean-Up")
    cam.release()  # Release the camera so it's no longer being actively used
    cv2.destroyAllWindows()  # Closes all CV2 windows
