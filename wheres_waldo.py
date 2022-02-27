import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to input image")
ap.add_argument("-c", "--cascade", default=cv2.data.haarcascades + "haarcascade_frontalface_default.xml", help="path to face detector haar cascade")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

detector = cv2.CascadeClassifier(args["cascade"])
rects = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

if rects is ():
  print("No faces found")

for (i, (x, y, w, h)) in enumerate(rects):
	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
	cv2.putText(image, "Face #{}".format(i + 1), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)

cv2.imshow("Faces", image)
cv2.waitKey(0)
cv2.destroyAllWindows()