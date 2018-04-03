# This module uses different predictors to check out text from a raw input

import constants
from terminaltables import AsciiTable

LUT = {'a': 'n', 'b': 'e', 'c': 'o', 'd': 'e', 'e': 'r', 'f': 'o', 'g': 'e', 'h': 'e', 'i': 'n', 'j': 'u', 'k': 'e', 'l': 'e', 'm': 'e', 'n': 'd', 'o': 'n', 'p': 'e', 'q': 'u', 'r': 'e', 's': 't', 't': 'h', 'u': 'r', 'v': 'e', 'w': 'a', 'x': 'p', 'y': 'o', 'z': 'e', ' ' : 's'}

def NEXT(letter):
    return LUT[letter]

# compression function
def compression(stream, predictor):
    initialStreamLength = 16 * len(stream)

    #print("Initial stream length is " + str(initialStreamLength) + " bits")

    compressedArray = []
    maxBitsNeeded = 0

    for i in range(0, len(stream) - 1):
        currentValue = stream[i]
        actualNextValue = stream[i+1]
        
        predictedValue = '';
        if currentValue in LUT.keys():
            predictedValue = predictor(currentValue)
        else:
            predictedValue = currentValue

        residue = ord(predictedValue) - ord(actualNextValue)
        compressedArray.append(residue)

        actualBitsNeeded = int.bit_length(residue)
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

    if chunkSize == 1:
        return None
        
    totalSize = 0
    for i in range(numberOfChunks):
        start = i * chunkSize
        finish = min((i + 1) * chunkSize - 1, len(stream))
        # TODO compress subchunks in order to get better compression
        chunkCompression = compression(stream[start:finish], predictor)
        totalSize += chunkCompression[1]

    compressionRatio = 1.0 * totalSize / initialStreamLength
    return [initialStreamLength, totalSize, initialStreamLength - totalSize, compressionRatio]

def run_singleTest(file):
    with open(constants.RAW_PATH + file, 'r') as myfile:
        data = myfile.read().replace('\n', '')
    
    print("Text file has: " + str(len(data)) + " characters")
    
    predictorsArray = [NEXT]
    # single compression
    results = [['Initial number of bits', 'Final number of bits', 'Removed bits', 'Compression ratio',  'Bits needed for residue (< 16)', 'Predictor']]
    for predictor in predictorsArray:
        result = compression(data, predictor)
        result.append(predictor)
        results.append(result)

    table = AsciiTable(results)
    print(table.table)

    numberOfChunksArray = [2, 3, 5, 10, 20, 50, 100, 200, 500]
    print("")
    print("Chunk split")
    for numberOfChunks in numberOfChunksArray:
        print(str(numberOfChunks) + " chunks")
        print("`````````")
        results2 =  [['Initial number of bits', 'Final number of bits', 'Removed bits', 'Compression ratio', 'Predictor']]    
        for predictor in predictorsArray:
            result = chunckCompression(data, predictor, numberOfChunks)
            if result is None:
                continue
            result.append(predictor)
            results2.append(result)
        
        table = AsciiTable(results2)
        print(table.table)
        
def test():
    print("")
    print("This is a test for text predictors")
    print("```````````````````````````````````")

    testFiles = ['text0.txt']
    for testFile in testFiles:
        print("Testing: " + testFile)
        run_singleTest(testFile)