# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 10:21:31 2023

@author: blumera
"""

import os
import cv2 as cv

def white_balance(img):
    b, g, r = cv.split(img)
    r_avg = cv.mean(r)[0]
    g_avg = cv.mean(g)[0]
    b_avg = cv.mean(b)[0]

    k = (r_avg + g_avg + b_avg) / 3
    kr = k / r_avg
    kg = k / g_avg
    kb = k / b_avg

    r = cv.addWeighted(src1=r, alpha=kr, src2=0, beta=0, gamma=0)
    g = cv.addWeighted(src1=g, alpha=kg, src2=0, beta=0, gamma=0)
    b = cv.addWeighted(src1=b, alpha=kb, src2=0, beta=0, gamma=0)

    balance_img = cv.merge([b, g, r])
    return balance_img

source_folder = "C:/Users/schmidj1s/Desktop/color"
output_folder = "C:/Users/schmidj1s/Desktop/color_balanced"

for root, _, files in os.walk(source_folder):
    for file in files:
        if file.lower().endswith('.tif'):
            input_path = os.path.join(root, file)
            output_path = input_path.replace(source_folder, output_folder)

            output_dir = os.path.dirname(output_path)
            os.makedirs(output_dir, exist_ok=True)

            img = cv.imread(input_path, cv.IMREAD_UNCHANGED)  # Read TIFF image

            # After reading the image
            print(f"Processing: '{input_path}'")
            
            if img is None:
                print(f"Error: Could not read image at '{input_path}'")
                continue
            
            balanced_img = white_balance(img)
            if balanced_img is None:
                print(f"Error: White balance failed for image at '{input_path}'")
                continue
            
            print(f"Saving: '{output_path}'")
            
            cv.imwrite(output_path, balanced_img)
            print(f"Processed and saved: '{output_path}'")

print("White balancing and saving completed.")