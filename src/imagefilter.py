import cv2 as cv
import numpy as np
from image_predictors import *

images = ["../raw/light.bmp"]

def get_image_info(file_path):

    image = cv.imread(file_path, cv.IMREAD_GRAYSCALE)
    return image

def predict_values(image):
    (height, width) = image.shape
    for i in range(height):
        for j in range(width):
            for predictor in PREDICTORS:
                pass

if __name__ == "__main__":
    image = get_image_info(images[0])
    predict_values(image)
