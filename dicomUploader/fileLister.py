# -*- coding: UTF-8 -*-
from os import listdir
from os.path import isfile, isdir, join


def file_lister(path):
    mypath=path
    
    fileList=[f for f in listdir(mypath)]
    for file in fileList:
        if (isdir(join(mypath,file))):
            print file, isfile(join(mypath,file))

    print fileList

file_lister("/Users/AlexanderK/")
