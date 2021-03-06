import argparse
import cv2
import os
import recognizer
import sys

menu = r'''
#######################################################################################
#      ______                   ____                              _                   #
#     / ____/___ _________     / __ \___  _________  ____ _____  (_)___  ___  _____   #
#    / /_  / __ `/ ___/ _ \   / /_/ / _ \/ ___/ __ \/ __ `/ __ \/ /_  / / _ \/ ___/   #
#   / __/ / /_/ / /__/  __/  / _, _/  __/ /__/ /_/ / /_/ / / / / / / /_/  __/ /       #
#  /_/    \__,_/\___/\___/  /_/ |_|\___/\___/\____/\__, /_/ /_/_/ /___/\___/_/        #
#                                                 /____/                              #
#                                                                                     #
#######################################################################################

####################################
1. Face Detect and Data Gathering
2. Face Training
3. Face Recognition
4. Quit
####################################
Please select an OpenCV Operation: 
'''

menuId = -1


def is_int(input):
    try:
        int(input)
        return True
    except BaseException as err:
        return False


def is_within_range(input, min, max):
    if min <= input <= max:
        return True
    return False


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def resetMenu():
    menuId = -1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    # GENERAL ARGUMENTS #
    # Argument for specifying the specific cascade file to use
    ap.add_argument("-c", "--cascade", default=cv2.data.haarcascades +
                    "haarcascade_frontalface_default.xml", help="path to face detector haar cascade")
    # Argument for specifying the dataset save path
    ap.add_argument("-dsp", "--dspath", default="./dataset/",
                    help="The default path to save the datasets to")
    # Argument for specifying the dataset save path
    ap.add_argument("-tp", "--tpath", default="./trainer/",
                    help="The default path to save the datasets to")
    # Argument for specifying the image save path
    ap.add_argument("-dr", "--driver", default="./driver/chromedriver.exe",
                    help="The path to the chromedriver.exe")
    # Argument for debug logging
    ap.add_argument("-d", "--debug", default=False,
                    help="Enables Debug Logging")

    # RECTANGLE ARGUMENTS #
    # Argument for Rectangle Red-value
    ap.add_argument("-rr", "--rectRed", default=255,
                    help="The Red-value for the rectangle coloring")
    # Argument for Rectangle Green-value
    ap.add_argument("-rg", "--rectGreen", default=0,
                    help="The Green-value for the rectangle coloring")
    # Argument for Rectangle Blue-value
    ap.add_argument("-rb", "--rectBlue", default=0,
                    help="The Blue-value for the rectangle coloring")

    # Argument for Rectangle Red-value for Recognizer
    ap.add_argument("-rrr", "--recogRectRed", default=0, help="")
    # Argument for Rectangle Red-value for Recognizer
    ap.add_argument("-rrg", "--recogRectGreen", default=255, help="")
    # Argument for Rectangle Red-value for Recognizer
    ap.add_argument("-rrb", "--recogRectBlue", default=0, help="")

    # TEXT ARGUMENTS #
    # Argument for Text Blue-value
    ap.add_argument("-tb", "--textBlue", default=0,
                    help="The Blue-value for the text coloring")
    # Argument for Text Green-value
    ap.add_argument("-tg", "--textGreen", default=0,
                    help="The Green-value for the text coloring")
    # Argument for Text Red-value
    ap.add_argument("-tr", "--textRed", default=255,
                    help="The Red-value for the text coloring")

    # Argument for Text Blue-value for Recognizer
    ap.add_argument("-rtb", "--recogTextBlue", default=255,
                    help="The Blue-value for the text coloring")
    # Argument for Text Green-value for Recognizer
    ap.add_argument("-rtg", "--recogTextGreen", default=255,
                    help="The Green-value for the text coloring")
    # Argument for Text Red-value for Recognizer
    ap.add_argument("-rtr", "--recogTextRed", default=255,
                    help="The Red-value for the text coloring")

    # Argument for Text Blue-value for Recognizer Confidence
    ap.add_argument("-rtcb", "--recogTextConfBlue", default=255,
                    help="The Blue-value for the text coloring")
    # Argument for Text Green-value for Recognizer Confidence
    ap.add_argument("-rtcg", "--recogTextConfGreen", default=255,
                    help="The Green-value for the text coloring")
    # Argument for Text Red-value for Recognizer Confidence
    ap.add_argument("-rtcr", "--recogTextConfRed", default=255,
                    help="The Red-value for the text coloring")

    # Parse any input arguments
    args = vars(ap.parse_args())

    logger = recognizer.logger.Logger(
        identity="Main", debugEnabled=args["debug"])  # Setups a Main Logger
    print(menu)  # Prints the Main Menu
    user_input = input()  # Take in user input

    # Validate the input as an integer and with a valid value between 1 and 4
    while not is_int(user_input) and not is_within_range(user_input, 1, 4):
        logger.warn("Invalid Program Input!")  # Warning about invalid input
        # Warn-level re-entry question
        logger.warn("Please select an OpenCV Operation: ")
        user_input = input()  # Take in user input

    menuId = int(user_input)  # Parse the input MenuID

    if menuId == 1:  # If ID is 1 (Detect and Gather)
        logger.info(
            "Would you like to search of images on the web, or use a local camera?")
        logger.info("[0 = Search, 1 = Camera]: ")
        isCamera = input()
        while not is_int(isCamera) and not is_within_range(isCamera, 0, 1):
            logger.warn("Error: Invalid input!")
            logger.warn("[0 = Camera, 1 = Search]: ")
            isCamera = input()

        isCamera = int(isCamera) > 0
        recognizer.gatherer.main(args, isCamera)
    elif menuId == 2:  # If ID is 2 (Train)
        recognizer.trainer.main(args)
    elif menuId == 3:  # If ID is 3 (Recognize)
        recognizer.recognizer.main(args)
    else:
        sys.exit()
