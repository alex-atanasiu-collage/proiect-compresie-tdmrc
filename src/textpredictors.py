# This module uses different predictors to check out text from a raw input

import constants
from terminaltables import AsciiTable
import huffman as huff
import ast, os

LUT = {'a': 'n', 'b': 'e', 'c': 'o', 'd': 'e', 'e': 'r', 'f': 'o', 'g': 'e', 'h': 'e', 'i': 'n', 'j': 'u', 'k': 'e', 'l': 'e', 'm': 'e', 'n': 'd', 'o': 'n', 'p': 'e', 'q': 'u', 'r': 'e', 's': 't', 't': 'h', 'u': 'r', 'v': 'e', 'w': 'a', 'x': 'p', 'y': 'o', 'z': 'e', ' ' : 's', '.' : ' '}


def NEXT(letter):
    return LUT[letter]

PREDICTORS = {"NEXT" : NEXT}

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


##############################################################      
def test():
    print("")
    print("This is a test for text predictors")
    print("```````````````````````````````````")

    testFile = 'text1.txt'
    print("Testing: " + testFile)
    with open(constants.RAW_PATH + testFile, 'r') as myfile:
        data = myfile.read().replace('\n', ' ').lower()

    saveTextHuffman(data, "text.temp", "NEXT")
    data = restoreFileData("text.temp.arch")
    with open(constants.RAW_PATH + testFile + "_restored", 'w') as myfile:
        myfile.write(data)
##############################################################

def saveTextHuffman(inStream, filename, predictor):

    stream = ""
    (codings, residues) = getHuffman(inStream, predictor)

    for residue in residues:
        stream += codings[residue]

    stream_file = open(filename, "w")
    dict_file = open(filename + ".dict", "w")

    stream_file.write(stream)
    dict_file.write(predictor + "\n")
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
    residues = [ord(stream[0])]
    predictorFunciton = PREDICTORS[predictor]

    for i in range(0, len(stream) - 1):
        currentValue = stream[i]
        actualNextValue = stream[i+1]
        
        predictedValue = '';
        if currentValue in LUT.keys():
            predictedValue = predictorFunciton(currentValue)
        else:
            predictedValue = currentValue

        residue = ord(predictedValue) - ord(actualNextValue)
        residues.append(residue)

    return residues

def restoreValue(predictor, lastValue, residue):
    if lastValue is None:
        return residue
    return ord(LUT[chr(lastValue)]) - residue


def restoreFileData(filename):

    (residues, predictor) = decodeResidues(filename)
    fileData = ""
    lastValue = None
    for residue in residues:
        decodedValue = restoreValue(predictor, lastValue, residue)
        lastValue = decodedValue
        fileData += chr(decodedValue)
    return fileData



def decodeResidues(filename):

    (codings, stream, predictor) = loadTextHuffman(filename)
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

    return (residuums, predictor)

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
    codings = ast.literal_eval(dict_file.read())
    stream_file.close()
    dict_file.close()

    return (codings, stream, predictor)