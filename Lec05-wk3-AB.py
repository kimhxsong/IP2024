import cv2


# from Common.utils import print_matinfo
# 행렬 정보 출력 함수 임포트

def main():
    img_gray = cv2.imread('./assets/lec5_imread_gray.jpg', cv2.IMREAD_GRAYSCALE)
    img_color = cv2.imread('./assets/lec5_imread_color.jpg', cv2.IMREAD_COLOR)

    img_g2c = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
    print(img_gray.shape, img_color.shape)

    img_color[100:200, 100:300] = 255
    img_color[:, 200:] = img_g2c[:, 200:]

    cv2.imshow("Grayscale", img_gray)
    cv2.imshow("Color", img_color)
    cv2.waitKey(0)

    cv2.imwrite('./lec5_imwrite_color.jpg', img_color)


def main2():
    cap = cv2.VideoCapture('./assets/lec5_video2.mp4')
    if not cap.isOpened():
        print('Video open failed!')
        return

    fps = cap.get(cv2.CAP_PROP_FPS)  # FPS=24
    delay = round(1000 / fps)

    w, h = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter.fourcc(*'DIVX')
    output = cv2.VideoWriter('./lec5_video2_output.avi', fourcc, fps, (w, h))  # Changed file extension to .mp4
    if not output.isOpened():
        print('Video Writer open failed!')
        return

    while True:
        ret, frame = cap.read()  # cap.read()는 frame 한 장을 반환
        if not ret:
            break
        inversed = ~frame
        output.write(inversed)
        # if cv2.waitKey(delay) == 27:
        #     break

    cap.release()
    output.release()


if __name__ == '__main__':
    main2()
