#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx

class Form(wx.Panel):
    
    def __init__ (self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        self.createControls()
        self.bindEvents()
        self.doLayout()
        
    def createControls(self):
        self.logger = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.labelChangeMonitorFolder = wx.StaticText(self, label="Folder")
        self.btnChangeMonitorFolder = wx.Button(self, label="...")
        self.textMonitorFolder = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.labelAccessKey = wx.StaticText(self, label="Access Key")
        self.textAccessKey = wx.TextCtrl(self, value="Enter Access Key")
        self.labelSecretKey = wx.StaticText(self, label="Secret Key")
        self.textSecretKey = wx.TextCtrl(self, value="Enter Secret Key")
        self.labelBucket = wx.StaticText(self, label="Bucket")
        self.textBucket = wx.TextCtrl(self, value="Upload Bucket")
        
    def bindEvents(self):
        for control, event, handler in \
        [(self.btnChangeMonitorFolder, wx.EVT_BUTTON, self.changeMonitorFolder)]:
            control.Bind(event, handler)
            
    def doLayout(self):
        boxSizer = wx.BoxSizer(orient=wx.VERTICAL)
        gridSizer = wx.FlexGridSizer (rows=5, cols=3, vgap=10, hgap=10)
        
        expandOption = dict(flag=wx.EXPAND)
        noOptions = dict()
        emptySpace = ((0,0), noOptions)
        
        for control, options in \
        [(self.labelAccessKey, noOptions),
            (self.textAccessKey, expandOption), emptySpace,
            (self.labelSecretKey, noOptions),
            (self.textSecretKey, expandOption), emptySpace,
            (self.labelBucket, noOptions),
            (self.textBucket, expandOption), emptySpace,
            (self.labelChangeMonitorFolder, noOptions),
            (self.textMonitorFolder, expandOption), (self.btnChangeMonitorFolder, noOptions)]:
            gridSizer.Add(control, **options)
        
        for control, options in \
        [(gridSizer, dict(border=5, flag=wx.ALL)),
            (self.logger, dict(border=5, flag=wx.ALL|wx.EXPAND, proportion=1))]:
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
            
    def changeMonitorFolder(self, event):
		self.__log('Change Monitor Folder button clicked')
		dlg = wx.DirDialog(self, "Выберите папку для мониторинга")
		if dlg.ShowModal() == wx.ID_OK:
			dir = dlg.GetPath()
			self.__log('Chosen %s'%dir)
			self.textMonitorFolder.Value = dir
		else:
			self.__log('Folder not changed')
		dlg.Destroy()
		
        
    def __log(self, message):
        self.logger.AppendText("%s\n"%message)

        
class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, None)
        self.form = Form(self)
        self.Show()
        
if __name__ == '__main__':        
    app = wx.App(0)
    frame = MyFrame()
    app.MainLoop()