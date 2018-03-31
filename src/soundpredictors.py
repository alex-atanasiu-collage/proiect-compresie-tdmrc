# This module uses different predictors to check out sound signals from a raw input

import wave # we use wave to open wav files for test
import struct
import constants

def SAME(value):
    return value

def compression(stream, predictor = None):
    print("Initial stream length is " + str(2 * len(stream)) + " bytes")

    if(predictor == None):
        print("Final stream length is " + str(2 * len(stream)) + " bytes with no predictor")
        return


def test():
    print("")
    print("This is a test for sound predictors")
    print("```````````````````````````````````")

    wavFile = wave.open(constants.RAW_PATH + "test.wav")
    numberOfFrames = wavFile.getnframes()
    actualFrames = wavFile.readframes(numberOfFrames)
    sampleWidth = wavFile.getsampwidth() # 2 for our case
    actualSampleArray = struct.unpack('h'*numberOfFrames,actualFrames)
    
    print("Sample array has: " + str(len(actualSampleArray)) + " samples")

    wavFile.close();

    lengthsArray = [10, 25, 100, 1000, 5000, numberOfFrames]
    predictorsArray = [None,SAME]

    for length in lengthsArray:
        for predictor in predictorsArray:
            compression(actualSampleArray[:length], predictor)