import cv2 as cv
import numpy as np

# Different predictors for images
# For now only the base predictors are implemented
# There are linear combinations for the base predictors to create more complex ones
# Here you add more predictors

PREDICTORS = ["N", "NW", "W", "NE"]

def _N(i, j, image):

    if i > 0:
        return image[i-1, j]
    else:
        return None

def _NW(i, j, image):

    if i > 0 and j > 0:
        return image[i-1, j-1]
    else:
        return None

def _W(i, j, image):

    if j > 0:
        return image[i, j-1]
    else:
        return None

def _NE(i, j, image):

    (height, width) = image.shape
    if j < width - 1:
       return image[i-1, j+1]
    else:
       return None

def predict_value(predictor, i, j, image):
    if predictor == "N":
       return _N(i, j, image)
    elif predictor == "NW":
       return _NW(i, j, image)
    elif predictor == "W":
       return _W(i, j, image)
    elif predictor == "NE":
       return _NE(i, j, image)
