from os import listdir
from os.path import isfile, isdir, join

import ConfigParser

def fileLister(path):
    mypath=path
    
    fileList=[f for f in listdir(mypath)]
    for file in fileList:
        if (isdir(join(mypath,file))):
            print file, isfile(join(mypath,file))

    print fileList

fileLister("/Users/AlexanderK/")
