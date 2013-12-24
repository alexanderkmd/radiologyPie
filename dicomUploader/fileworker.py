#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import config
import amazon
import hashlib
from datetime import datetime


from os import walk, listdir
from os.path import join, isfile


def list_monitor_folder():
    # возвращает список файлов в директории (из настроек), рекурсивно
    path = config.get_config_value("Local", "MonitorPath")
    file_list = list_files(path)
    return file_list


def list_files(path, recursive=True):
    # возвращает список файлов в директории, по умолчанию - рекурсивно
    file_list = []

    if recursive:
        for root, subFolders, files in walk(path):
            for file in files:
                #file_list.append(file)
                file_list.append(join(root, file))
    else:
        file_list = [f for f in listdir(path) if isfile(join(path, f))]

    #for file in file_list:
    #    print file

    return file_list


def isdicomfile(filename):
    # заготовка под определитель дикомовский ли файл
    return True


def uploadFiles(filelist):
    i=1
    putpath = datetime.now().strftime("%Y/%m/%d/%H/%M/%S")
    print putpath
    for file in filelist:
        #amazon.put_item_to_bucket(file, str(i), putpath)
        i += 1
        pass
    #загружает
    return True

	
def md5_for_file(file, block_size=2**20):
    # проверка - если строка - то это путь к фалу, который надо открыть
	# если передана ссылка на файл, то должен быть скормлен двоичный ввод ('rb') при открытии
    if isinstance(file, basestring):
		f = open(file, 'rb')
    else:
	    f = file
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    if isinstance(file, basestring):
	    # закрываем файл, если мы его открывали
	    f.close()
    return md5.hexdigest()
	
filelist = list_monitor_folder()

uploadFiles(filelist)

print filelist.__len__()

now = datetime.now()

#now.strftime("%Y/%m/%d/%H/%M/%S")



