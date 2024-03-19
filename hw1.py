import cv2


def main():
    cap1 = cv2.VideoCapture('./assets/lec5_video1.mp4')
    cap2 = cv2.VideoCapture('./assets/lec5_video2.mp4')

    fps = cap1.get(cv2.CAP_PROP_FPS)
    shape = (int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fourcc = cv2.VideoWriter.fourcc(*'XVID')
    output = cv2.VideoWriter('./lec5_video_output.avi', fourcc, fps, shape)

    count = 1
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    while ret1 and frame1 is not None and count <= 24:
        output.write(frame1)

        ret1, frame1 = cap1.read()
        count += 1

    step = (shape[0] / 48)
    while ret1 and frame1 is not None and ret2 and frame2 is not None and count <= (24 * 3):  # FPS * SEC
        transition_frame = frame1.copy()
        transition_frame[:, -int(step * (count - 24)):] = frame2[:, -int(step * (count - 24)):]
        output.write(transition_frame)

        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        count += 1

    ret2, frame2 = cap2.read()
    while ret2 and frame2 is not None and count <= 24 * 6:
        output.write(frame2)

        ret2, frame2 = cap2.read()
        count += 1

    cap1.release()
    cap2.release()
    output.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
