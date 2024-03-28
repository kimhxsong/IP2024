import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image


def load_videos(video1_path, video2_path):
    cap1 = cv2.VideoCapture(video1_path)
    cap2 = cv2.VideoCapture(video2_path)

    if not cap1.isOpened() or not cap2.isOpened():
        print('Error: Video file not found')
        return None, None

    return cap1, cap2


def create_output(cap, output_path):
    fps = cap.get(cv2.CAP_PROP_FPS)
    shape = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # The 'XVID' codec is utilized for AVI file format
    fourcc = cv2.VideoWriter.fourcc(*'XVID')
    output = cv2.VideoWriter(output_path, fourcc, fps, shape)

    return output


def create_mask(frame):
    lower_green = np.array([0, 100, 0])
    upper_green = np.array([100, 255, 100])
    mask = cv2.inRange(frame, lower_green, upper_green)

    return mask


def apply_chroma_key(frame1, frame2, mask, chroma_key_mode):
    if chroma_key_mode:
        frame1 = cv2.bitwise_and(frame1, frame1, mask=~mask)
        frame2 = cv2.bitwise_and(frame2, frame2, mask=mask)
        composite = cv2.add(frame1, frame2)
    else:
        composite = frame1

    return composite


def add_text(composite, chroma_key_mode, frame_index):
    composite_pil = Image.fromarray(cv2.cvtColor(composite, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(composite_pil)
    fontpath = "./assets/PretendardVariable.ttf"
    # The font was downloaded from the following source: https://cactus.tistory.com/306
    try:
        font = ImageFont.truetype(fontpath, 32)
    except IOError:
        print(f"Error: Font file not found at {fontpath}")
        return

    draw.text((40, 40), "201710906 김현송", font=font, fill=(255, 255, 0))
    draw.text((40, 80), f"Chroma key mode: {'On' if chroma_key_mode is True else 'Off'}", font=font, fill=(255, 255, 0))
    draw.text((40, 120), f"Frame: {frame_index}", font=font, fill=(255, 255, 0))

    composite = cv2.cvtColor(np.array(composite_pil), cv2.COLOR_RGB2BGR)

    return composite


def write_frame(output, composite):
    output.write(composite)


def listen_for_spacebar(chroma_key_mode):
    key = cv2.waitKey(1) & 0xFF
    if key == ord(' '):
        chroma_key_mode = not chroma_key_mode

    return chroma_key_mode


def main():
    cap1, cap2 = load_videos('./assets/lec6_woman.mp4', './assets/lec6_raining.mp4')
    if cap1 is None or cap2 is None:
        return

    output = create_output(cap1, 'hw2_201710906.avi')

    chroma_key_mode = True
    frame_index = 0

    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if not ret1 or not ret2:
            break

        mask = create_mask(frame1)
        composite = apply_chroma_key(frame1, frame2, mask, chroma_key_mode)
        composite = add_text(composite, chroma_key_mode, frame_index)
        cv2.imshow('Video', composite)
        write_frame(output, composite)
        chroma_key_mode = listen_for_spacebar(chroma_key_mode)

        frame_index += 1

    cap1.release()
    cap2.release()
    output.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
