import pickle
import os

#put index into a file
def saveIndex(filename, invIndex):
        file = open(filename, "wb")
        pickle.dump(invIndex, file)
        file.close()

#load existing index data
def loadIndex(filename):
       return pickle.load(open(filename, 'rb'))
