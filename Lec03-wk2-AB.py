import numpy as np
import cv2


def main():
    img = np.zeros((300,400), np.uint8)
    img.fill(200)
    img[100:200, 50:100] = 255
    cv2.imshow('window title', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
    main()

# https://www.jetbrains.com/help/pycharm/에서 PyCharm 도움말 참조
