import cv2
#
# def on_threshold(pos):
#     _, dst = cv2.threshold(src, pos, 255, cv2.THRESH_BINARY)
#     cv2.imshow('dst', dst)
#
# src = cv2.imread('assets/lec13_rice.png', cv2.IMREAD_GRAYSCALE)
#
# cv2.imshow('src', src)
# cv2.namedWindow('dst')
# cv2.createTrackbar('Threshold', 'dst', 0, 255, on_threshold)
# cv2.setTrackbarPos('Threshold', 'dst', 128)
#
# while True:
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cv2.destroyAllWindows()


def main():
    src = cv2.imread('assets/lec13_sudoku.jpg', cv2.IMREAD_GRAYSCALE)

    def on_threshold(pos):
        bsize = pos
        if bsize % 2 == 0:
            bsize = bsize - 1
        if bsize < 3:
            bsize = 3
        dst = cv2.adaptiveThreshold(src, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, bsize, 5)
        cv2.imshow('dst', dst)

    cv2.namedWindow('dst')
    cv2.createTrackbar('Threshold', 'dst', 0, 255, on_threshold)
    cv2.setTrackbarPos('Threshold', 'dst', 128)

    cv2.waitKey(0)

if __name__ == '__main__':
    main()
