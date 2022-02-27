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
    logger = recognizer.logger.Logger(identity="Gatherer", debugEnabled=args["debug"])
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Opens the Video Default Camera

    # Video Capture Values: https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
    cam.set(3, 640)  # 3 = Width
    cam.set(4, 480)  # 4 = Height

    # Grabs the CascadeClassifier using the passed in --cascade argument
    # See: https://docs.opencv.org/3.4/d1/de5/classcv_1_1CascadeClassifier.html#ab3e572643114c43b21074df48c565a27 for full documentation
    face_detector = cv2.CascadeClassifier(args["cascade"])
    # Name of the image data-set to use
    logger.info(input="Enter user id end press <return> --> '")
    face_id = input()

    # Information Print-Out
    logger.info(input="Initializing face capture. Look at the camera and wait...")

    count = 0  # Inits a Count variable for the number of found faces

    while(True):
        # Grabs the current "return value" as well as the image.
        # The return value indicates if any images was captured, returns false in cases where the camera has been disconnected or there are no more frames in the video file.
        # See: https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html#a473055e77dd7faa4d26d686226b292c1 for full documentation
        ret, img = cam.read()

        while not ret:
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

        # Tries to detect any and all faces present in the Grayscale image using a scaleFactor of 1.3 and a minNeighbor count of 5
        # For more information on valid inputs for detectMultiScale see: https://docs.opencv.org/3.4/da/dd5/classcv_1_1BaseCascadeClassifier.html#aa4c96739e441adda5005ae58fd95a5a2 for full documentation
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        # Loops over the xPos, yPos, width and height variables for any faces found by the face_detector on the grayscale
        for (xPos, yPos, width, height) in faces:
            count += 1  # Increments the amount of found faces

            # Draws a rectangle over each face found by the face_detector using the positions found as well as the width and height.
            # It takes in the following values in order:
            #
            # img                                                    = The original image to draw on
            # (xPos, yPos)                                           = The first Vertex point of the rectangle (See https://www.mathopenref.com/vertex.html for info on Vertices)
            # (xPos + width + yPos + height)                         = The second Vertex point of the rectangle
            # (args["rectRed"], args["rectGreen"], args["rectBlue"]) = The color for the rectangle to be rendered as, this takes the values passed in by the args parser defaulting to (255,0,0) or solid Red
            # 2                                                      = The thickness of the rectangle lines
            #
            # See: https://docs.opencv.org/3.4/d6/d6e/group__imgproc__draw.html#ga07d2f74cadcf8e305e810ce8eed13bc9 for full documentation
            cv2.rectangle(img=img, pt1=(xPos, yPos), pt2=(xPos + width, yPos + height),
                          color=(args["rectRed"], args["rectGreen"], args["rectBlue"]), thickness=2)

            # Adds some text to identify each "face-box"
            #
            # It takes in the following values in order:
            #
            # img                                                    = The original image to draw on
            # f"Face #{count + 1}"                                   = The actual text being printed in this case "Face #0" for example
            # (xPos, yPos - 10)                                      = The position of where the text should be placed, in this case it's based off xPos and yPos, where yPos is offset 10 units upwards.
            # cv2.FONT_HERSHEY_SIMPLEX                               = The Font to use, in this case we're using a normal-sized sans-serif font. See documentation: https://docs.opencv.org/4.x/d6/d6e/group__imgproc__draw.html#gga0f9314ea6e35f99bb23f29567fc16e11afff8b973668df2e4028dddc5274310c9
            # 0.55                                                   = The scale of the Font being drawn
            # (args["rectBlue"], args["rectGreen"], args["rectRed"]) = This is NOT a typo! This is the color being represented as a BGR format which is an alternative color representation order than RGB!
            # 2                                                      = The thickness of the text
            #
            # See: https://docs.opencv.org/3.4/d6/d6e/group__imgproc__draw.html#ga5126f47f883d730f633d74f07456c576 for full documentation
            cv2.putText(img=img, text=f"Face #{count}", org=(xPos, yPos - 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.55, color=(args["rectBlue"], args["rectGreen"], args["rectRed"]), thickness=2)

            # Writes the grayscale image to file using the default format "dataset/User.{face_id}.{count}.jpg" so for example "dataset/User.Simon.0.jpg"
            # It takes in the following values in order:
            #
            # args["dataset-path"] + "/User." + str(face_id) + "." + str(count) + ".jpg" = The file-name to use for the image
            # gray[yPos : yPos + height, xPos : xPos + width]                            = The image itself, in this case the gray-scale picture grabbing the pixels between yPos to yPos + height and xPos to xPos + width
            #
            # See: https://docs.opencv.org/3.4/d4/da8/group__imgcodecs.html#gabbc7ef1aa2edfaa87772f1202d67e0ce for full documentation
            with open(file=args["dspath"] + "/User." + str(face_id) + "." + str(count) + ".jpg", mode='w', encoding='utf-8'):
                pass
            cv2.imwrite(filename=args["dspath"] + "/User." + str(face_id) + "." + str(count) + ".jpg", img=gray[yPos: yPos + height, xPos: xPos + width])

            # Displays the image with the found faces
            # It takes in the following values in order:
            #
            # 'image' = The name of the window
            # img     = The image data being passed in, in this case the non-grayscale image
            #
            # See: https://docs.opencv.org/3.4/d7/dfc/group__highgui.html#ga453d42fe4cb60e5723281a89973ee563 for full documentation
            cv2.imshow(winname='image', mat=img)

            # Awaits any key being pressed for at least 100 ms or 0.1 seconds
            # See: https://docs.opencv.org/3.4/d7/dfc/group__highgui.html#ga5628525ad33f52eab17feebcfba38bd7 for full documentation on waitKey
            k = cv2.waitKey(delay=10000) & 0xff  # Press 'ESC' for exiting video

            # If the key was 27 aka Esc then break
            if k == 27:
                break
            # Else if the count was greater than 30 frames then break
            if count >= 30:
                break
    # Information Print about it shutting down
    logger.info(input="Exiting Program and doing Clean-Up")
    cam.release()  # Release the camera so it's no longer being actively used
    cv2.destroyAllWindows()  # Closes all CV2 windows
