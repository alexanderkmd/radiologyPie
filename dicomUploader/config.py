# -*- coding: UTF-8 -*-
# ver 0.1
# 2013-12-09

import ConfigParser
import os.path
from os.path import join

Config = ConfigParser.ConfigParser()

localDir = os.path.dirname(__file__)
configFile=join(localDir,"config.ini")

def open_config():    
    # открывает файл конфига, если такового нет - записывает дефолтные значения в новый файл
    if (os.path.exists(configFile)):
        Config.read(configFile)
    else:
        print("Creating new config file - please fill it in and restart")
        set_config_value('Local', 'MonitorPath', '/your/monitor/Path')
        set_config_value('Amazon', 'AccessKey', 'yourAWS_AccessKeyId')
        set_config_value('Amazon', 'SecretKey', 'yourAWS_SecretKeyId')
        set_config_value('Amazon', 'bucket', 'yourUploadBucketName')


def get_config_value(section, parameter):
    # получаем значение параметра из конфига
    if Config.has_section(section):
        if Config.has_option(section, parameter):
            return Config.get(section, parameter)
    print "No such section and/or parameter"
    return ""
                
def set_config_value(section, parameter, value):
    # дописывает новый параметр или изменяет его в конфиге
    if (Config.has_section(section) == False):
        Config.add_section(section)
    Config.set(section, parameter, value)
    with open(configFile, 'wb') as conf:
        Config.write(conf)
        
open_config()