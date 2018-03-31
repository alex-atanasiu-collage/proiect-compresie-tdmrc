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

    return [initialStreamLength, finalStreamLength, initialStreamLength - finalStreamLength, compressionRatio, maxBitsNeeded]

def chunckCompression(stream, predictor, numberOfChunks):
    initialStreamLength = 16 * len(stream)
    
    chunkSize = int(len(stream) / numberOfChunks)

    totalSize = 0
    for i in range(numberOfChunks):
        start = i * chunkSize
        finish = min((i + 1) * chunkSize - 1, len(stream))
        # TODO compress subchunks in order to get better compression
        chunkCompression = compression(stream[start:finish], predictor)
        totalSize += chunkCompression[1]


    compressionRatio = 1.0 * totalSize / initialStreamLength
    return [initialStreamLength, totalSize, initialStreamLength - totalSize, compressionRatio]


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

    # single compression
    results = [['Initial number of bits', 'Final number of bits', 'Removed bits', 'Compression ratio',  'Bits needed for residue (< 16)', 'Predictor']]
    for length in lengthsArray:
        for predictor in predictorsArray:
            result = compression(actualSampleArray[:length], predictor)
            result.append(predictor)
            results.append(result)

    table = AsciiTable(results)
    print(table.table)


    numberOfChunksArray = [2, 3, 5, 10, 20, 50]
    print("")
    print("Chunk split")
    for numberOfChunks in numberOfChunksArray:
        print(str(numberOfChunks) + " chunks")
        print("`````````")
        lengthsArray2 = [1000, 5000, 10000, 20000, numberOfFrames]
        results2 =  [['Initial number of bits', 'Final number of bits', 'Removed bits', 'Compression ratio', 'Predictor']]    
        for length in lengthsArray2:
            for predictor in predictorsArray:
                result = chunckCompression(actualSampleArray[:length], predictor, numberOfChunks)
                result.append(predictor)
                results2.append(result)
        table = AsciiTable(results2)
        print(table.table)
        