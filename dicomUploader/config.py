# ver 0.1
# 2013-12-09

import ConfigParser
import os.path
from os.path import join

Config = ConfigParser.ConfigParser()

localDir = os.path.dirname(__file__)
configFile=join(localDir,"config.ini")

openConfig()

def openConfig():    
    # открывает файл конфига, если такового нет - записывает дефолтные значения в новый файл
    if (os.path.exists(configFile)):
        Config.read(configFile)
    else:
        print("Creating new config file - please fill it in and restart")
        setConfigValue('Local', 'MonitorPath', '/your/monitor/Path')
        setConfigValue('Amazon', 'AccessKey', 'yourAWS_AccessKeyId')
        setConfigValue('Amazon', 'SecretKey', 'yourAWS_SecretKeyId')
        setConfigValue('Amazon', 'bucket', 'yourUploadBucketName')


def getConfigValue(section, parameter):
    # получаем значение параметра из конфига
    if Config.has_section(section):
        if Config.has_option(section, parameter):
            return Config.get(section, parameter)
    print "No such section and/or parameter"
    return ""
                
def setConfigValue(section, parameter, value):
    # дописывает новый параметр или изменяет его в конфиге
    if (Config.has_section(section) == False):
        Config.add_section(section)
    Config.set(section, parameter, value)
    with open(configFile, 'wb') as conf:
        Config.write(conf)