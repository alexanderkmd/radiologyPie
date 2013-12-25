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


def is_dicom_file(filename):
    # заготовка под определитель дикомовский ли файл
    return True


def upload_files(filelist):
    putpath = datetime.now().strftime("%Y/%m/%d/%H/%M/%S")

    # длина префикса мониторируемой папки для отрезания этой части от пути
    # (формирование относительного пути) + 1 для backslash
    pathprefix = config.get_config_value("Local", "MonitorPath")
    pathprefixlen = pathprefix.__len__() + 1

    for file in filelist:
        meta = {}  # dict для метаданных, передаваемых с файлом

        hash = md5_for_file(file)
        # отрезание префикса и формирование относительного пути
        originalpath = file[pathprefixlen:]
        meta['md5'] = hash
        meta['path'] = originalpath

        print meta #originalpath + " - " + hash
        amazon.put_item_to_bucket(file, hash, putpath, meta)
        pass
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
        f.close()  # закрываем файл, если мы его открывали
    return md5.hexdigest()

file_list = list_monitor_folder()

upload_files(file_list)

print file_list.__len__()