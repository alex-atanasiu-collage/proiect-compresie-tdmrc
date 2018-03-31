# This module uses different predictors to check out sound signals from a raw input

from terminaltables import AsciiTable

import wave # we use wave to open wav files for test
import struct
import constants


# PREDICTORS
def SAME(value):
    return value

def NEXT(value):
    return value+1

def PREV(value):
    return value-1

# compression function
def compression(stream, predictor):
    initialStreamLength = 16 * len(stream)

    #print("Initial stream length is " + str(initialStreamLength) + " bits")

    compressedArray = []
    maxBitsNeeded = 0

    for i in range(0, len(stream) - 1):
        currentValue = stream[i]
        actualNextValue = stream[i+1]
        predictedValue = predictor(currentValue)

        residue = predictedValue - actualNextValue
        compressedArray.append(residue)

        actualBitsNeeded = int.bit_length(residue) + 1 # + 1 sign bit
        if(maxBitsNeeded < actualBitsNeeded):
            maxBitsNeeded = actualBitsNeeded

    finalStreamLength = 16 + (len(stream) - 1) * maxBitsNeeded
    #print("Final stream length is " + str(finalStreamLength) + " bits with no predictor")
    compressionRatio = 1.0 * finalStreamLength / initialStreamLength
    #print("Compression ration is " + str(compressionRatio))

    return [initialStreamLength, finalStreamLength, initialStreamLength - finalStreamLength, compressionRatio]

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

    wavFile.close()

    lengthsArray = [10, 25, 100, 1000, 5000, numberOfFrames]
    predictorsArray = [SAME, NEXT, PREV]


    results = [['Initial number of bits', 'Final number of bits', 'Removed bits', 'Compression ratio', 'Predictor']]
    for length in lengthsArray:
        for predictor in predictorsArray:
            result = compression(actualSampleArray[:length], predictor)
            result.append(predictor)
            results.append(result)

    table = AsciiTable(results)
    print(table.table)