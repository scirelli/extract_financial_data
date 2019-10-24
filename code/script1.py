# PROJECT DESCRIPTION _______________________________
'''Morphological operations

https://docs.opencv.org/3.4/dd/dd7/tutorial_morph_lines_detection.html


Why don't you just code this yourself?
'''

# PYTHON MODULES ------------------------------------
import os
import pandas as pd
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from pdf2image.exceptions import (
        PDFInfoNotInstalledError,
        PDFPageCountError,
        PDFSyntaxError
        )
import nltk
from nltk.stem import *
stemmer = PorterStemmer()
from nltk import corpus
import cv2
import numpy as np

# PROJECT MODULES -----------------------------------
import module1 as m1


# IMPORT FILES --------------------------------------
dir_data        = r'/home/ccirelli2/Desktop/repositories/extract_financial_data/data'
afile           = 'fin1.pdf'
path2file       = dir_data + '/' + afile
dir_images      = r'/home/ccirelli2/Desktop/repositories/extract_financial_data/output/images'
dir_txt_files   = r'/home/ccirelli2/Desktop/repositories/extract_financial_data/output/text'

# OCR PDF -------------------------------------------
#m1.convert_pdf_2_image(path2file, 200, dir_images, 'jpg', True)

# Convert Each Page to Text -------------------------
'Save text files to output'
#m1.convert_image2text(dir_images, dir_txt_files)


# PROCESS IMAGE - OPENCV ----------------------------
'''
    1.) We need to get the far edge where the text starts and define a verticle line. 
        We might achieve this by iterating the matrix and recording at which step the majority
        of the pixels deviate from 255.  Then we can simply redefine the pixels at that 
        index to be all black. 
    2.) draw boxes or lines separating each line of data. Once we have these markers, 
        we should be able to source the lines individually and process them via OCR. 
'''


def main_process_image():
    path2image = dir_images + '/' + 'balance_sheet.jpg'

    # Pre-Process Image
    img_read = cv2.imread(path2image)
    img_gray = cv2.cvtColor(img_read, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5,5), 0)

    # Add Vertical Lines
    col_left = m1.get_far_left_pixel(img_blur)
    col_right = m1.get_far_right_pixel(img_blur)

    img = m1.draw_bounding_lines(img_blur, col_left, col_right)

    cv2.imshow('test', img)
    cv2.waitKey(0)


main_process_image()












