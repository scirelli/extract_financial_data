# PYTHON MODULES ------------------------------
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


def convert_pdf_2_image(pdf_path, DPI, output_folder, FMT, print_feedback=False): 
    ''' Description:    This function converts a pdf into individual images of its
                        pages. 
        Inputs          File_in:        Full path of target pdf file to be OCR'd
                        File_out:       Root name of image file to save to drive. 
                        Output_folder:  Full path to output folder to save files.  
                        FMT:            Image format type.  ex 'jpeg'
        Output:         Individual images of each page of the pdf.
                        Saved down to a specified location. 
    '''
    # Main Function
    images = convert_from_path(pdf_path, 
                               dpi  = DPI, 
                               output_folder = output_folder, 
                               fmt  = FMT) 
    # User Feedback
    if print_feedback == True:
        print('OCR of pdf successful.  File saved to => {}'.format(output_folder))



def convert_image2text(dir_images, output_txt_files):
    # Change Directory to where images are located
    os.chdir(dir_images)
   
    # Create Count Object
    Count = 0

    # Iterate Files in Directory
    for afile in os.listdir():
        # Assertaine File Type (hope that there are no other periods in name)
        file_type = afile.split('.')[1]
        # If jpeg
        if file_type == 'jpg':

            # Increase Count Object
            Count +=1

            # Convert Image 2 Text
            text = pytesseract.image_to_string(Image.open(afile))
   
            # Write Text 2 File
            with open(output_txt_files + '/' + 'page_{}.txt'.format(Count), 'w') as f:
                f.write(text)
                f.close()
            
            print('File => {} written to {}'.format(afile, output_txt_files))



def motion_blur(img):
   
    # Define Kernel Size
    kernel_size = 30
    # Create MxN Matrix filled w/ zeros
    kernel_h = np.zeros((kernel_size, kernel_size))
    # Fill Middle Row W/ Ones
    kernel_h[:, int((kernel_size -1)/2)] = np.ones(kernel_size)
    # Apply Filter 2 Image
    horizontal_mb = cv2.filter2D(img_blur, -2, kernel_h)

    cv2.imshow('img_blur', horizontal_mb)
    cv2.waitKey(0)
    

def get_far_left_pixel(img):

    # Define Farthest Left Non-White Pixel
    far_left_nonwhite_pixel = img.shape[1]

    # Iterate Matrix
    for nparray in img:

        # Col_count
        Col_count = -1

        # Iterate Each Array
        for pixel in nparray:
            # Increase Col_count
            Col_count += 1

            if pixel < 200 and Col_count < far_left_nonwhite_pixel:
                far_left_nonwhite_pixel = Col_count
                print(Col_count)
                break

    # Return pixel
    print('Far left pixel => {}'.format(far_left_nonwhite_pixel))
    return far_left_nonwhite_pixel




def get_far_right_col(img):

    # Get Image Dimensions
    img_num_cols = img.shape[1]

    # Define Farthest Right Non-White Pixel
    farthest_right_col = []

        
    # Iterate the Columns From Right To Left 
    for col_num in range(img_num_cols-1, 0, -1):
        # If the list is empty
        if len(farthest_right_col) == 0:
            # Index Column in question
            col = img[: , col_num - 1]
            for pixel in col:
                # If there is a non-white pixel
                if pixel < 200:
                    # Append the column number ot the list and break
                    farthest_right_col.append(col_num)
                    break
    
    # Return pixel
    print('Farthest right col => {}'.format(farthest_right_col))
    return farthest_right_col[0] 



def draw_vertical_line(img, col_left, col_right):
    
    # Add Vertical Left:
    v_left = img[:, col_left - 1: col_left] = 0

    # Add Vertical Right:
    v_right = img[:, col_right - 1: col_right] = 0


    # Return Image
    return img

















