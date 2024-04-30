import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

def add_text(composite):
    composite_pil = Image.fromarray(cv2.cvtColor(composite, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(composite_pil)
    fontpath = "./assets/PretendardVariable.ttf"
    # The font was downloaded from the following source: https://cactus.tistory.com/306
    try:
        font = ImageFont.truetype(fontpath, 18)
    except IOError:
        print(f"Error: Font file not found at {fontpath}")
        return

    draw.text((20, 20), "201710906 김현송", font=font, fill=(255, 255, 0))
    composite = cv2.cvtColor(np.array(composite_pil), cv2.COLOR_RGB2BGR)

    return composite

def main():
    # Load the images
    img1 = cv2.imread('./assets/lec8_field.bmp')
    img2 = cv2.imread('./assets/lec8_airplane.bmp')

    if img1 is None or img2 is None:
        print('Error: Video file not found')
        exit(1)

    # Create the VideoWriter object
    fps = 30
    height, width = img1.shape[:2]
    shape = (width, height)
    fourcc = cv2.VideoWriter.fourcc(*'XVID')
    output = cv2.VideoWriter('hw3_201710906.avi', fourcc, fps, shape)

    # For each frame in the video
    for i in range(5 * fps):
        # Calculate the weights for the two images
        weight1 = max(0, (120. - i) / 90) if i >= 30 else 1.
        weight2 = 1. - weight1

        # Calculate the weighted sum of the two images
        frame = cv2.addWeighted(img1, weight1, img2, weight2, 0)

        # Add the student number and name to the frame
        composite = add_text(frame)

        # Write the frame to the output video
        output.write(composite)

    # Release the VideoWriter object and close all OpenCV windows
    output.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()