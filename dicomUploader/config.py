# -*- coding: UTF-8 -*-
# ver 0.1
# 2013-12-09

import ConfigParser
import codecs
import os.path
from os.path import join


class UnicodeConfigParser(ConfigParser.RawConfigParser):

    def __init__(self, defaults=None, dict_type=dict):
        ConfigParser.RawConfigParser.__init__(self, defaults, dict_type)

    def write(self, fp):
        """Fixed for Unicode output"""
        if self._defaults:
            fp.write("[%s]\n" % DEFAULTSECT)
            for (key, value) in self._defaults.items():
                fp.write("%s = %s\n" % (key, unicode(value).replace('\n', '\n\t')))
            fp.write("\n")
        for section in self._sections:
            fp.write("[%s]\n" % section)
            for (key, value) in self._sections[section].items():
                if key != "__name__":
                    fp.write("%s = %s\n" %
                             (key, unicode(value).replace('\n', '\n\t')))
            fp.write("\n")

    # This function is needed to override default lower-case conversion
    # of the parameter's names. They will be saved 'as is'.
    def optionxform(self, strOut):
        return strOut


Config = UnicodeConfigParser()

localDir = os.path.dirname(__file__)
configFile = join(localDir, "config.ini")


def open_config():    
    # открывает файл конфига, если такового нет - записывает значения из примера
    if os.path.exists(configFile):
        Config.readfp(codecs.open(configFile, 'r', 'utf-8'))
    else:
        configSampleFile = join(localDir, "config.ini.sample")
        if os.path.exists(configSampleFile):
            print("[INFO] Creating new config file from example - please fill it in and restart")
            Config.readfp(codecs.open(configSampleFile, 'r', 'utf-8'))
        else:
            print("[ERROR] You have to fill in config manually!")


def get_config_value(section, parameter):
    # получаем значение параметра из конфига
    if Config.has_section(section):
        if Config.has_option(section, parameter):
            return Config.get(section, parameter)
    print "No such section and/or parameter"
    return ""


def get_config_section(section):
    dictl = {}
    if Config.has_section(section):
        options = Config.options(section)
        for option in options:
            try:
                dictl[option] = Config.get(section, option)
                if dictl[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dictl[option] = None
    else:
        print "No such section and/or parameter"
    return dictl


def set_config_value(section, parameter, value):
    # дописывает новый параметр или изменяет его в конфиге
    if not Config.has_section(section):
        Config.add_section(section)
    Config.set(section, parameter, value)
    confFile = codecs.open(configFile, 'w', 'utf-8')
    Config.write(confFile)
    confFile.close()
        
open_config()