from cv2 import cv2 as cv
import numpy as np

# cloak color is color_chosen in RGB
color_chosen = np.uint8([[[255, 0, 0]]])
hsv = cv.cvtColor(color_chosen, cv.COLOR_BGR2HSV)
print(hsv)
