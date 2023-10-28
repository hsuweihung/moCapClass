from __future__ import print_function
from builtins import input
import cv2 
import numpy as np
import argparse
import time
from tqdm import tqdm
from IPython.display import display
from PIL import Image

# Read image given by user
image = cv2.imread('lena.bmp')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Converting BGR to RGB

new_image_A = np.zeros_like(image)
new_image_B = np.zeros_like(image)

if image is None:
    print('Could not open or find the image: ', args.input)
    exit(0)

for y in tqdm(range(image.shape[0])):
    for x in range(image.shape[1]):
                if(y%8==0 or x%8==0):
                    new_image_A[y,x] = 0
                else:  
                    new_image_A[y,x] = image[y-(y%8),x-(x%8)]


for y in range(image.shape[0]):
    for x in range(image.shape[1]):
                if(y%8==0 or x%8==0):
                    new_image_B[y,x] = 0
                else:  
                    eight_block = image[y:y+8, x:x+8]#圖片切成 8*8 個 block
                    average_color = np.mean(eight_block)#算平均顏色
                    new_image_B[y:y+8, x:x+8] = average_color#把new_image_B賦予成 64像素的圖片，每個 block 賦予平均顏色


# Initialize values
print(' Tile Style ')
print('-------------------------')

#cv2.imshow('Original Image', image)
#cv2.imshow('New Image', new_image)
display(Image.fromarray(image))
display(Image.fromarray(new_image_A))
display(Image.fromarray(new_image_B))

# Wait until user press some key
#cv2.waitKey()