import glob
import os


#load books from folder
def loadBooksFromFolder(path):
    os.chdir(path)
    books = []
    for file in glob.glob("*.txt"):
        books.append(file)

    return books


