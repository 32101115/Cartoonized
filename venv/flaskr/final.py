# Final Project
# Jitae Kim

import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')
import numpy as np
import scipy as sp
import cv2
import math

def filtering(image):
    """
    Before any further processing, a median filter is applied in order to 
    reduce any salt and pepper noise that may be in the image.
    bilateralFilter can reduce unwanted noise very well 
    while keeping edges fairly sharp. However, it is very slow compared to most filters.
    Filter size: Large filters (d > 5) are very slow, 
    so it is recommended to use d=5 for real-time applications, 
    and perhaps d=9 for offline applications that need heavy noise filtering.
    Sigma values: For simplicity, 
    you can set the 2 sigma values to be the same. 
    If they are small (< 10), the filter will not have much effect, 
    whereas if they are large (> 150), they will have a very strong effect, 
    making the image look cartoonish.

    the bilateral filter run- time is dependent on the kernel size,
    """
    output = np.array(image)
    for x in xrange(0,1):
        bilateralFilter_img = cv2.bilateralFilter(output,5, 75, 75)

    return bilateralFilter_img

def quantizeColor(bilateralFilter_img, a, ksize):
    """ 
    Quantize Colors
    Blurs an image using the median filter

    ksize is aperture linear size; it must be odd and greater than 1
    a is the factor by which the number of colors in each channel is to be reduced:

    This means that
    the standard RGB color palette of 256^3 colors is reduced to a
    palette of [256/24]^3 unique colors.

    medianBlur is highly effective against salt-and-pepper noise in the images
    """
    medianBlur_img = cv2.medianBlur(bilateralFilter_img,ksize)
    [rows,cols,c] = medianBlur_img.shape
    quantizeColor_img = medianBlur_img
    for i in xrange(0,rows):
        for j in xrange(0,cols):
            pixel_b = medianBlur_img.item(i,j,0)
            pixel_g = medianBlur_img.item(i,j,1)
            pixel_r = medianBlur_img.item(i,j,2)  
            pixel_b = math.floor(pixel_b/a)*a 
            pixel_g = math.floor(pixel_g/a)*a
            pixel_r = math.floor(pixel_r/a)*a
            quantizeColor_img.itemset((i,j,0),pixel_b)
            quantizeColor_img.itemset((i,j,1),pixel_g)
            quantizeColor_img.itemset((i,j,2),pixel_r)

    return quantizeColor_img

def edgeDetection(image):
    """
    Canny edge detector instead of a Laplacian kernel is that the edges are all single
    pixel edges in the resulting image

    morphological operations, dilate: 
    The purpose of this step is to both bolden and smooth the contours of the edges slightly

    Edge Filter: Finally, the edge image is separated into its constituent regions, 
    and any region with an area below a certain threshold is removed. 
    In this way, small contours picked up by the Canny edge detector are 
    ignored in the final image, which helps reduce unwanted line clutter in the result.
    """
    output = np.array(image)
    #ksize determines details
    median_filtimg2 = cv2.medianBlur(output,5)
    lowThreshold = 100
    edges = cv2.Canny(median_filtimg2,lowThreshold,lowThreshold*2)

    #kernel size determines the bold
    kernel = np.ones((1,1), np.uint8)
    dialateimg =  cv2.dilate(edges, kernel)
    #Inverts every bit of an array.
    edges_inv = cv2.bitwise_not(dialateimg)
    ret,thresh = cv2.threshold(edges_inv,127,255, 0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    img_contours = cv2.drawContours(thresh, contours, -1, (0,255,0), 3)
    return edges_inv

def recombine(colorquantimg,edges_inv):
    [rows, cols, c] = colorquantimg.shape
    output = colorquantimg

    for i in xrange(0,rows):
        for j in xrange(0,cols):
            if edges_inv[i][j] == 0:
                output.itemset((i,j,0),0)
                output.itemset((i,j,1),0)
                output.itemset((i,j,2),0)
    return output