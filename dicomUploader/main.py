#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import gui
import wx


if __name__ == '__main__':
    app = wx.App(0)
    frame = gui.MyFrame()
    app.MainLoop()