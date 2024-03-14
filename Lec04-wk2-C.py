import cv2
import numpy as np

def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Left button pressed", (x, y))
    elif event == cv2.EVENT_RBUTTONDOWN:
        print("Right button pressed", (x, y))


def onChange(value):
    global img
    img[:] = value
    cv2.imshow('window', img)


img = np.full((300, 500), 255, np.uint8)
cv2.imshow('window', img)

cv2.setMouseCallback('window', onMouse)
cv2.createTrackbar("Brightness", 'window', 0, 255, onChange)
cv2.waitKey(0)
