import cv2 as cv
import numpy as np
from image_predictors import *

images = ["../raw/light.bmp", "../raw/marbles.bmp"]
INFINITE = 999999

def get_image_info(file_path):

    image = cv.imread(file_path, cv.IMREAD_GRAYSCALE)
    return image

def get_residuum(image, i, j):

    min_res = INFINITE
    
    for predictor in PREDICTORS:
        pvalue = predict_value(predictor, i, j, image)
        if pvalue:
            residuum = pvalue - image[i, j]
            if min_res > abs(residuum):
                min_res = residuum

    return min_res
        

def predict_values(image):

    residuums = []

    (height, width) = image.shape
    for i in range(height):
        for j in range(width):
            residuum = get_residuum(image, i, j)
            if residuum == INFINITE:
                residuums.append(image[i, j])
            else:
                residuums.append(residuum)

    return residuums

def compress_statistics(image):

    residuums = predict_values(image)
    (height, width) = image.shape
    num_bits = 0

    """ Decoment this following section if you want to visualize the residuum
    new_image = np.zeros((height, width), np.uint8)
    for i in range(height):
        for j in range(width):
            new_image[i, j] = residuums[i * height + j]
    
    cv.imshow("residuum", new_image)
    cv.waitKey(0)
    """
    for residuum in residuums:
        if residuum != 0:
            num_bits += int.bit_length(int(residuum))

    print ("Original image has the size of: " + str(image.size * 8) + " bits")
    print ("Compressed file has the size of: " + str(num_bits) + " bits")
    print ("Compression ratio is the size of " + str(float(num_bits) / (image.size * 8)))


if __name__ == "__main__":
    image = get_image_info(images[1])
    compress_statistics(image)
