#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'AlexanderK'

# пока тупой скрипт, для разбора в нормальные, подходящие под стандарт, файлы, получаемые с передвижного рентгена

import dicom
import time
import wx

from os import walk
from os.path import join, basename

# обход ошибки в pydicom 0.9.8 с unicode в пути к файлу
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def process_dicom_file(ds):
    # на входе - датасет диком файла
    #TODO прикрутить возможные изменения под типовые ошибки с разных аппаратов - пока только под передвижной рентген
     # причесываем даты
    date = time.strptime(ds.AcquisitionDate.replace(".", ""), "%Y%m%d")
    if date.tm_year < 1950:
        print "replace date was - " + ds.AcquisitionDate
        ds.AcquisitionDate = ds.StudyDate.replace(".", "")
    ds.StudyDate = ds.StudyDate.replace(".", "")
    ds.SeriesDate = ds.SeriesDate.replace(".", "")
    ds.ContentDate = ds.ContentDate.replace(".", "")
    ds.PatientBirthDate = ds.PatientBirthDate.replace(".", "")

    #забиваем unicode как чарсет по умолчанию, если не указан другой
    if not "SpecificCharacterSet" in ds:
        #print ds[0x08,0x05].value
        ds.SpecificCharacterSet = "ISO_IR 192"  # UTF-8

    # Прописываем имя пациента, расшифровывая его из того, что есть
    name = ds.PatientName
    ds.PatientName = name.decode("windows-1251").encode("utf-8").__str__()

    if not "WindowWidth" in ds:
        ds.WindowWidth = 500
        ds.WindowCenter = 1000




app = wx.App()
dlg = wx.DirDialog(None, "Выбрать папку с файлами")
if dlg.ShowModal() == wx.ID_OK:
    folder = dlg.GetPath()
    pass
else:
    folder = ""
dlg.Destroy()

app.MainLoop()


file_list = []

for root, subFolders, files in walk(folder):
    for file in files:
        file_list.append(join(root, file))

for file in file_list:
    print file
    try:
        ds = dicom.read_file(file)
        process_dicom_file(ds)

        newfilename = "corrected-" + basename(file)
        ds.save_as(join(folder, newfilename))
    except Exception as e:
        print "Non DICOM File" + e.message
    print "##################################################################"
