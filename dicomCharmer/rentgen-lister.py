#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'AlexanderK'

# пока тупой скрипт, для разбора в нормальные, подходящие под стандарт, файлы, получаемые с передвижного рентгена

import dicom
import time
import wx
import MySQLdb
import shutil
import datetime

from os import walk
from os.path import join, basename, exists
from os import walk, makedirs
from os.path import join, basename, exists, isdir

# обход ошибки в pydicom 0.9.8 с unicode в пути к файлу
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

dbpass = ""
db = MySQLdb.connect("adress", "user", dbpass, "db", charset='utf8')
cursor = db.cursor()

def process_dicom_file(ds, filename):
    # на входе - датасет диком файла
    #TODO прикрутить возможные изменения под типовые ошибки с разных аппаратов - пока только под передвижной рентген
     # причесываем даты
    date = time.strptime(ds.AcquisitionDate.replace(".", ""), "%Y%m%d")
    if date.tm_year < 1950:
        #print "replace date was - " + ds.AcquisitionDate + " now - " + ds.StudyDate.replace(".", "")
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

    name = ds.PatientName
    #print name
    names = name.split("^")
    first_name = ""
    second_name = ""
    middle_name = ""
    try:
        first_name = names[1]   # имя
    except IndexError:
        print "No first Name"

    try:
        middle_name = names[2]   # имя
    except IndexError:
        print "No Middle Name"

    try:
        second_name = names[0]   # имя
    except IndexError:
        print "No Second Name"

    fluoro_date = ds.StudyDate.replace(".", "-")  # дата исследования
    fluoro_birth_date = ds.PatientBirthDate.replace(".", "-")

    #print "Фамилия - " + second_name + " Имя - " + first_name + " Отчество - " + middle_name
    #print "Исследование - " + fluoro_date + " Дата рождения - " + fluoro_birth_date

    if not "WindowWidth" in ds:
        ds.WindowWidth = 500
        ds.WindowCenter = 1000

    sql = "INSERT INTO `security`.`fluoro` (`fluoroSecondName`, `fluoroFirstName`, `fluoroMiddleName`," \
          + " `fluoroBirthDate`, `fluoroDate`, `filename`) VALUES (" \
          + "'" + second_name + "', '" + first_name + "', '" + middle_name + "'," \
          + " '" + fluoro_birth_date + "', '" + fluoro_date + "', '" + filename + "');"
    #print sql

    cursor.execute(sql)
    db.commit()




app = wx.App()
dlg = wx.DirDialog(None, "Выбрать папку с файлами")
if dlg.ShowModal() == wx.ID_OK:
    folder = dlg.GetPath()
    pass
else:
    folder = ""
dlg.Destroy()

dlg = wx.TextEntryDialog(None, "Введите дату исследования в формате ГГГГ-ММ-ДД:")
#Использоуется для создания папки с зачищенными файлами, и в случае промахов в структуре файлов
while True:
    dlg.ShowModal()
    global_fluoro_date = dlg.GetValue()
    try:
        datetime.datetime.strptime(global_fluoro_date, '%Y-%m-%d')
        break
    except ValueError:
        msgbox = wx.MessageDialog(None, "Введена некорректная дата", "Ошибка ввода", wx.OK | wx.ICON_WARNING)
        msgbox.ShowModal()
        msgbox.Destroy()
        pass
dlg.Destroy()

outDlg = wx.DirDialog(None, "Выбрать целевую папку для файлов")
if outDlg.ShowModal() == wx.ID_OK:
    outputFolder = outDlg.GetPath()
    pass
else:
    outputFolder = ""
outDlg.Destroy()

app.MainLoop()

outputFolder = join(outputFolder, global_fluoro_date)
# создаем папку для файлов на выход
if not isdir(outputFolder):
    makedirs(outputFolder)


file_list = []

for root, subFolders, files in walk(folder):
    for file in files:
        file_list.append(join(root, file))

skipped = []
counter = 0

for file in file_list:
    counter=counter+1
    #print file
    newfilename = "corrected-" + basename(file)
    filename = basename(file)

    if exists(join(outputFolder, newfilename)):
        print file + " Already checked"
    elif file.find("corrected-") >= 0:
        print file + " is a corrected version"
    else:
        print file
        try:
            ds = dicom.read_file(file)
            process_dicom_file(ds, filename)
            ds.save_as(join(outputFolder, newfilename))
        except Exception as e:
            print "Error processing File - " + e.message
            print "SKIPPED " + basename(file) + "!!!!!!!!!!!!!!!"
            skipped.append(basename(file) + " - " + e.message)
            skipped_name = "skipped-" + basename(file)
            skipped_name = join(outputFolder, skipped_name)
            shutil.copyfile(file, skipped_name)
            sql = "INSERT INTO `security`.`fluoro` (`fluoroSecondName`, `fluoroFirstName`, `fluoroMiddleName`," \
                  + " `fluoroBirthDate`, `fluoroDate`, `filename`, `zakl`) VALUES (" \
                  + "'Пропущен', 'Брак', 'Файла'," \
                  + " '2014-01-01', '" + global_fluoro_date + "', '" + filename + "', " \
                  + "'Файл был пропущен или забракован парсером - внутренний брак файла, возможно не читаемый: " + db.escape_string(e.message) + "');"
            print sql
            cursor.execute(sql)
            db.commit()
            

        print "##################################################################"

print "Total files - " + str(counter)
print "Skipped files:"
for skipper in skipped:
    print skipper
