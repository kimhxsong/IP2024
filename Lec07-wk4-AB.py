import cv2

src = cv2.imread('./assets/lec7_candies.png')
src_hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

def on_trackbar(pos):
    hmin = cv2.getTrackbarPos('Hue_min', 'dst')
    hmax = cv2.getTrackbarPos('Hue_max', 'dst')
    dst = cv2.inRange(src_hsv, (hmin, 150, 0), (0, 255, hmax))
    cv2.imshow('dst', dst)

dst = cv2.inRange(src_hsv, (60, 150, 0), (80, 255, 100))
cv2.imshow('src', src)
cv2.imshow('dst', dst)
cv2.createTrackbar('Hue_min', 'dst', 50, 179, on_trackbar)
cv2.createTrackbar('Hue_max', 'dst', 80, 179, on_trackbar)
cv2.waitKey(0)

