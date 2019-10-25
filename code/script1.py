#!/usr/bin/env python3
# PROJECT DESCRIPTION _______________________________
'''Morphological operations

https://docs.opencv.org/3.4/dd/dd7/tutorial_morph_lines_detection.html


    1.) We need to get the far edge where the text starts and define a verticle line.
        We might achieve this by iterating the matrix and recording at which step the majority
        of the pixels deviate from 255.  Then we can simply redefine the pixels at that
        index to be all black.
    2.) draw boxes or lines separating each line of data. Once we have these markers,
        we should be able to source the lines individually and process them via OCR.
'''

# PYTHON MODULES ------------------------------------
import pytesseract
import cv2
import numpy as np
import random as rng


# PROJECT MODULES -----------------------------------
import module1 as m1


# IMPORT FILES --------------------------------------
dir_data = r'./data'
dir_images = r'./output/images'


def main_process_image(path2image=dir_images + '/' + 'cash_flow_statement.jpg', show_edges=False):
    # Pre-Process Image
    img_read = cv2.imread(path2image)
    img_gray = cv2.cvtColor(img_read, cv2.COLOR_BGR2GRAY)
    img_gray_orig = img_gray.copy()
    img_blur = cv2.GaussianBlur(img_gray, (9, 9), 0)
    # cv2.imshow('test1', img_blur)

    # Add Vertical Lines
    col_left = m1.get_far_left_pixel(img_blur)
    col_right = m1.get_far_right_pixel(img_blur)
    # img_vlines = m1.draw_bounding_lines(img_blur, col_left, col_right)

    # Black Out Text Lines
    img_black_out_text = m1.black_out_lines_text(img_blur)

    # Invert
    img_inverted = cv2.threshold(img_black_out_text, 200, 255, cv2.THRESH_BINARY_INV)[1]

    # Black Out Right and Left Ares w/ No Text
    img_inverted[:, 0: col_left] = 0
    img_inverted[:, col_right: img_read.shape[1]] = 0

    # Edges
    img_edges = cv2.Canny(img_inverted, 100, 255)

    # Find Contours
    contours, _ = cv2.findContours(img_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get Convex Hull
    hull_list = [cv2.convexHull(x) for x in contours]

    if show_edges:
        # Draw contours + hull results
        drawing = np.zeros((img_edges.shape[0], img_edges.shape[1], 3), dtype=np.uint8)
        for i in range(len(contours)):
            color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
            cv2.drawContours(drawing, contours, i, color)
            cv2.drawContours(drawing, hull_list, i, color)
        # Show in a window
        cv2.imshow('Contours', drawing)
        cv2.waitKey(0)

    # Iterate Through Bounding Boxes - OCR Text
    for n in range(0, len(contours)):
        (x, y, w, h) = cv2.boundingRect(contours[n])

        img_cropped = img_gray_orig[y:y + h, x:x + w]

        cv2.imshow('test', img_cropped)
        cv2.waitKey(0)
        text = pytesseract.image_to_string(img_cropped)
        print(text)

    return None


if __name__ == '__main__':
    main_process_image()
