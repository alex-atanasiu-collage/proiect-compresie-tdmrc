# This module uses different predictors to check out sound signals from a raw input

from terminaltables import AsciiTable

import wave # we use wave to open wav files for test
import struct
import constants
import huffman as huff
import ast, os

# PREDICTORS
def SAME(value):
    return value

def NEXT(value):
    return value+1

def PREV(value):
    return value-1

PREDICTORS = {"SAME" : SAME, "NEXT": NEXT, PREV: "PREV"}

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

def run_singleTest(file):
    wavFile = wave.open(constants.RAW_PATH + file)
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


    numberOfChunksArray = [2, 3, 5, 10, 20, 50, 100, 200, 500]
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

#######################################################      
def test():
    print("")
    print("This is a test for sound predictors")
    print("```````````````````````````````````")

    testFile = 'test2.wav'
    print("Testing: " + testFile)

    saveTextHuffman(testFile, "test.wav.temp", "NEXT")
    restoreFileData("test.wav.temp.arch")
    
########################################################

def saveTextHuffman(inFilename, filename, predictor):

    wavFile = wave.open(constants.RAW_PATH + inFilename)
    numberOfChannels = wavFile.getnchannels()
    numberOfFrames = wavFile.getnframes()
    actualFrames = wavFile.readframes(numberOfFrames)
    sampleWidth = wavFile.getsampwidth() 
    actualSampleArray = struct.unpack('h'*numberOfFrames,actualFrames)

    

    stream = ""
    (codings, residues) = getHuffman(actualSampleArray, predictor)

    for residue in residues:
        stream += codings[residue]

    stream_file = open(filename, "w")
    dict_file = open(filename + ".dict", "w")

    stream_file.write(stream)
    dict_file.write(predictor + "\n")
    dict_file.write(str(numberOfChannels) + "\n")
    dict_file.write(str(numberOfFrames) + "\n")
    dict_file.write(str(sampleWidth) + "\n")
    dict_file.write(str(sampleRate) + "\n")
    dict_file.write(str(codings))

    stream_file.close()
    dict_file.close()

    os.system(constants.EXECUTABLE + " u " + filename + " "  + filename + ".arch")
    os.system("rm -f " + filename)

def getHuffman(inStream, predictor):

    residues = getRezidues(inStream, predictor)
    num_appearances = {}
    for residue in residues:
        if residue not in num_appearances:
            num_appearances[residue] = 1
        else:
            num_appearances[residue] += 1

    huff_coll = []
    for entry in num_appearances:
        huff_coll += [(entry, num_appearances[entry])]

    huff_coll = huff.codebook(huff_coll)
    return (huff_coll, residues)



def getRezidues(stream, predictor):
    residues = [stream[0]]
    predictorFunciton = PREDICTORS[predictor]

    for i in range(0, len(stream) - 1):
        currentValue = stream[i]
        actualNextValue = stream[i+1]
        

        predictedValue = predictorFunciton(currentValue)
        
        residue = predictedValue - actualNextValue
        residues.append(residue)

    return residues

def restoreValue(predictor, lastValue, residue):
    predictorFunciton = PREDICTORS[predictor]
    if lastValue is None:
        return residue
    return predictorFunciton(lastValue) - residue


def restoreFileData(filename):

    (residues, predictor, numberOfFrames, sampleWidth, numberOfChannels, sampleRate) = decodeResidues(filename)

    fileData = []
    lastValue = None
    for residue in residues:
        decodedValue = restoreValue(predictor, lastValue, residue)
        lastValue = decodedValue
        fileData.append(decodedValue)
    
    wavef = wave.open(constants.RAW_PATH + "test2_restored.wav",'w')
    wavef.setnchannels(numberOfChannels)
    wavef.setsampwidth(sampleWidth) 
    wavef.setframerate(sampleRate)

    for dataPiece in fileData:
        data = struct.pack('<h', dataPiece)
        wavef.writeframesraw( data )

    wavef.writeframes('')
    wavef.close()



def decodeResidues(filename):

    (codings, stream, predictor, numberOfFrames, sampleWidth, numberOfChannels, sampleRate) = loadTextHuffman(filename)
    decodings = {}
    residuums = []
    for (key, value) in codings.iteritems():
        decodings[value] = key

    key = ""
    index = 0
    i = 0
    while index < len(stream):
        key += stream[index]
        index += 1
        if key in decodings:
            residuums += [decodings[key]]
            key = ""

    return (residuums, predictor, numberOfFrames, sampleWidth, numberOfChannels, sampleRate)

def loadTextHuffman(filename):

    if ".arch" not in filename:
        print "Not a valid format... We need .arch files"
        return None

    tmp_file = filename.split(".arch")[0]
    os.system(constants.EXECUTABLE + " v " + filename + " " + tmp_file)
 
    stream_file = open(tmp_file, "r")
    dict_file = open(tmp_file + ".dict", "r")

    stream = stream_file.read()
    predictor = dict_file.readline().split('\n')[0]
    numberOfChannels = ast.literal_eval(dict_file.readline())
    numberOfFrames = ast.literal_eval(dict_file.readline())
    sampleWidth = ast.literal_eval(dict_file.readline())
    sampleRate = ast.literal_eval(dict_file.readline())
    codings = ast.literal_eval(dict_file.read())
    stream_file.close()
    dict_file.close()

    return (codings, stream, predictor, numberOfFrames, sampleWidth, numberOfChannels, sampleRate)