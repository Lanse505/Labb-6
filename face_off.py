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
  ap.add_argument("-dsp", "--dspath", default="./dataset",
                help="The default path to save the datasets to")
  # Argument for specifying the dataset save path
  ap.add_argument("-tp", "--tpath", default="./trainer",
                help="The default path to save the datasets to")
  # Argument for debug logging
  ap.add_argument("-d", "--debug", default=False, help="Enables Debug Logging")


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

  logger = recognizer.logger.Logger(identity="Main", debugEnabled=args["debug"])
  print(menu)
  input = input()

  while not is_int(input) and not is_within_range(input, 1, 4):
    logger.warn(input="Invalid Program Input!")
    logger.warn(input="Please select an OpenCV Operation: ")
    input = input()

  menuId = int(input)

  if menuId == 1:
    resetMenu()
    recognizer.gatherer.main(args)
  elif menuId == 2:
    resetMenu()
    recognizer.trainer.main(args)
  elif menuId == 3:
    resetMenu()
    recognizer.recognizer.main(args)
  else:
    sys.exit()