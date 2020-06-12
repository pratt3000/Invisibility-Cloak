from cv2 import cv2
import numpy as np
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("--video", help="Input video path")
args = parser.parse_args()

cap = cv2.VideoCapture(args.video if args.video else 0)

time.sleep(3)

for i in range(0, 60):
    ret, background = cap.read()

# convert fourcc format to string
fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
out = cv2.VideoWriter(
    "data/output.mp4",
    fourcc,
    cap.get(cv2.CAP_PROP_FPS),
    (background.shape[1], background.shape[0]),
)
out2 = cv2.VideoWriter(
    "data/original.mp4",
    fourcc,
    cap.get(cv2.CAP_PROP_FPS),
    (background.shape[1], background.shape[0]),
)

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break

    # convert color format BGR to HSV
    # hue-saturation-value(brightness)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # two ranges because red appears in two ranges in hsv format
    # setting range for mask1
    # 100, 40, 40 - 100 255 255
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask1 = mask1 + mask2

    # get rid of noise dots etc
    mask_cloak = cv2.morphologyEx(
        mask1, op=cv2.MORPH_OPEN, kernel=np.ones((3, 3), np.uint8), iterations=2
    )
    # expands the selected part out from boundary
    mask_cloak = cv2.dilate(mask_cloak, kernel=np.ones((3, 3), np.uint8), iterations=1)
    # get bacground
    mask_bg = cv2.bitwise_not(mask_cloak)

    cv2.imshow("mask_cloak", mask_cloak)

    res1 = cv2.bitwise_and(background, background, mask=mask_cloak)
    res2 = cv2.bitwise_and(img, img, mask=mask_bg)
    result = cv2.addWeighted(src1=res1, alpha=1, src2=res2, beta=1, gamma=0)

    cv2.imshow("res1", res1)

    # cv2.imshow('ori', img)
    cv2.imshow("result", result)
    out.write(result)
    out2.write(img)

    if cv2.waitKey(1) == ord("q"):
        break

out.release()
out2.release()
cap.release()
