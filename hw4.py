import numpy as np
import os
import pandas as pd
import cv2
import math

def set_label(image, text, contour):
    fontface = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.5
    thickness = 1
    baseline = 0

    text_size = cv2.getTextSize(text, fontface, scale, thickness)
    text_width = text_size[0][0]
    text_height = text_size[0][1]

    r = cv2.boundingRect(np.array(contour))

    pt = (r[0] + ((r[2] - text_width) // 2), r[1] + ((r[3] + text_height) // 2))
    cv2.rectangle(image, (pt[0], pt[1] + baseline), (pt[0] + text_width, pt[1] - text_height), (200, 200, 200), cv2.FILLED)
    cv2.putText(image, text, pt, fontface, scale, (0, 0, 0), thickness, 8)

def slope(p1, p2):
    return (p2[0][1]-p1[0][1]) / (p2[0][0]-p1[0][0]) if not np.array_equal(p2[0][0], p1[0][0]) else float('inf')

def is_trapezoid(hull):
    # Calculate the slopes of the sides
    side_slopes = [slope(hull[i], hull[(i+1)%4]) for i in range(4)]

    # Check if one pair of opposite sides have the same slope (are parallel)
    return (math.isclose(side_slopes[0], side_slopes[2], rel_tol=0.1) and not math.isclose(side_slopes[1], side_slopes[3], rel_tol=0.1)) or \
        (math.isclose(side_slopes[1], side_slopes[3], rel_tol=0.1) and not math.isclose(side_slopes[0], side_slopes[2], rel_tol=0.1))

# Now, use these functions to classify the shape

def main(img_input):
    shape_counts = {
        "triangle": 0,
        "rectangle": 0,
        "trapezoid": 0,
        "quadrangle": 0,
        "concave_shape_1": 0,
        "concave_shape_3": 0,
        "circle": 0,
        "ellipse": 0
    }

    if img_input is None:
        print("Could not open or find the image")
        exit(-1)

    thresh, img_gray = cv2.threshold(img_input, 250, 255, cv2.THRESH_BINARY_INV  )
    contours, _ = cv2.findContours(img_gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    img_result = img_input.copy()

    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if abs(cv2.contourArea(approx)) > 50:  # 면적이 일정크기 이상이어야 한다.
            size = len(approx)

            cv2.drawContours(img_result, [approx], -1, (0, 255, 0), 1)
            for point in approx:
                cv2.circle(img_result, tuple(point[0]), 3, (0, 0, 255))

            if size == 3:
                set_label(img_result, "triangle", contour)  # 삼각형
                shape_counts['triangle'] += 1

            elif size == 4:
                if cv2.isContourConvex(approx):
                    # Calculate the actual contour area
                    area = cv2.contourArea(contour)
                    # Get the minimum bounding rectangle
                    rect = cv2.minAreaRect(approx)
                    # Calculate the area of the minimum bounding rectangle
                    box = cv2.boxPoints(rect)
                    area2 = cv2.contourArea(box)
                    # Calculate the ratio
                    ratio = area / area2 if area2 != 0 else 0
                    hull = cv2.convexHull(approx)

                    # Set the label
                    if ratio >= 0.95:
                        set_label(img_result, "rectangle", contour)
                        shape_counts['rectangle'] += 1
                    else:
                        if is_trapezoid(hull):
                            set_label(img_result, "trapezoid", contour)
                            shape_counts['trapezoid'] += 1
                        else:
                            set_label(img_result, "quadrangle", contour)
                            shape_counts['quadrangle'] += 1

                else:
                    set_label(img_result, "concave_shape_1", contour)
                    shape_counts['concave_shape_1'] += 1

            elif size == 6 and cv2.isContourConvex(approx) is False:
                set_label(img_result, "concave_shape_3", contour)  # 육각형
                shape_counts['concave_shape_3'] += 1

            else:
                length = cv2.arcLength(contour, True)
                area = cv2.contourArea(contour)
                ratio = 4. * math.pi * area / (length * length)
                if ratio >= 0.895:
                    set_label(img_result, f"circle", contour)
                    shape_counts['circle'] += 1
                else:
                    set_label(img_result, "ellipse", contour)
                    shape_counts['ellipse'] += 1

    # cv2.imshow("input", img_input)
    # cv2.imshow("result", img_result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return shape_counts

# 이미지 파일의 경로


if __name__ == '__main__':
    image_dir = 'assets/image'
    result_dict = {}

    for filename in os.listdir(image_dir):
        if filename.endswith('.png'):
            img_input = cv2.imread(os.path.join(image_dir, filename), cv2.IMREAD_GRAYSCALE)
            shape_counts = main(img_input)  # main 함수를 수정하여 도형의 개수를 반환하도록 합니다.
            name, extension = os.path.splitext(filename)
            result_dict['img' + name] = shape_counts

    df = pd.DataFrame(result_dict).T
    df = df.sort_index(axis=0).sort_index(axis=1)
    df.to_csv('shape_counts.csv')