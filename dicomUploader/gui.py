#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx
import config
import fileworker


class Form(wx.Panel):
    
    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        self.create_controls()
        self.bind_events()
        self.do_layout()
        
    def create_controls(self):
        self.logger = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.labelChangeMonitorFolder = wx.StaticText(self, label="Отслеживаемая папка")
        self.btnChangeMonitorFolder = wx.Button(self, label="...")
        self.textMonitorFolder = wx.TextCtrl(self, style=wx.TE_READONLY, value=config.get_config_value("Local", "MonitorPath"))
        self.labelAccessKey = wx.StaticText(self, label="Ключ доступа")
        self.textAccessKey = wx.TextCtrl(self, value=config.get_config_value("Amazon", "AccessKey"))
        self.btnSecretKeyChange = wx.Button(self, label="Изменить секрет")
        #self.labelSecretKey = wx.StaticText(self, label="Секретный ключ")
        #self.textSecretKey = wx.TextCtrl(self, value="Введите секретный ключ")
        self.labelBucket = wx.StaticText(self, label="Репозиторий")
        self.textBucket = wx.TextCtrl(self, value=config.get_config_value("Amazon", "bucket"))
        
    def bind_events(self):
        for control, event, handler in \
            [(self.btnChangeMonitorFolder, wx.EVT_BUTTON, self.change_monitor_folder),
                (self.btnSecretKeyChange, wx.EVT_BUTTON, self.change_secret_key)]:
            control.Bind(event, handler)
            
    def do_layout(self):
        boxSizer = wx.BoxSizer(orient=wx.VERTICAL)
        gridSizer = wx.FlexGridSizer(rows=5, cols=3, vgap=10, hgap=5)
        
        expandOption = dict(flag=wx.EXPAND)
        noOptions = dict()
        emptySpace = ((0,0), noOptions)
        
        for control, options in \
            [(self.labelAccessKey, noOptions),
                (self.textAccessKey, expandOption), (self.btnSecretKeyChange, noOptions),
                #(self.labelSecretKey, noOptions),
                #(self.textSecretKey, expandOption), emptySpace,
                (self.labelBucket, noOptions),
                (self.textBucket, expandOption), emptySpace,
                (self.labelChangeMonitorFolder, noOptions),
                (self.textMonitorFolder, expandOption), (self.btnChangeMonitorFolder, noOptions)]:
            gridSizer.Add(control, **options)
        
        for control, options in \
            [(gridSizer, dict(border=5, flag=wx.ALL)),
                (self.logger, dict(border=5, flag=wx.ALL | wx.EXPAND, proportion=1))]:
            boxSizer.Add(control, **options)
        
        self.SetSizerAndFit(boxSizer)
        
        '''for control, x, y, width, height in 
        [(self.logger, 1, 400, 400, 100),
            (self.textMonitorFolder, 1, 100, 345, -1),
            (self.btnChangeMonitorFolder, 365, 100, 30, -1),
            (self.labelAccessKey, 1, -1, -1, -1),
            (self.textAccessKey, 50, -1, -1, -1),
            (self.labelSecretKey, 1, -1, -1, -1),
            (self.textSecretKey, 50, -1, -1, -1),
            (self.labelBucket, 1, -1, -1, -1),
            (self.textBucket, 50, -1, -1, -1)]:
            control.SetDimensions(x=x, y=y, width=width, height=height)'''
            
    def change_monitor_folder(self, event):
        self.__log('Change Monitor Folder button clicked')
        dlg = wx.DirDialog(self, "Выберите папку для мониторинга")
        if dlg.ShowModal() == wx.ID_OK:
            directory = dlg.GetPath()
            self.__log('Chosen %s' % directory)
            self.textMonitorFolder.Value = directory
            config.set_config_value('Local', 'MonitorPath', directory)
        dlg.Destroy()

    def change_secret_key(self, event):
        self.__log('Change secret button pressed')
        dlg = wx.TextEntryDialog(None, "Введите секретный ключ, выданный вам", "Секретный ключ",
                                 config.get_config_value("Amazon", "SecretKey"), style=wx.OK|wx.CANCEL)

        if dlg.ShowModal() == wx.ID_OK:
            config.set_config_value("Amazon", "SecretKey", dlg.GetValue())
            self.__log("SecretKey changed")
        dlg.Destroy()

    def __log(self, message):
        self.logger.AppendText("%s\n" % message)

        
class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, None)
        self.form = Form(self)
        self.Show()
        
#if __name__ == '__main__':
#    app = wx.App(0)
#    frame = MyFrame()
#    app.MainLoop()