# -*- coding: utf-8 -*-
"""
Created on Tue May 15 22:23:30 2018

@author: Amauri
"""
import os
import stat
import time
import wx
import re

import numpy as np
import pandas as pd
import backend as bkend
from ObjectListView import ObjectListView, ColumnDefn
 
########################################################################
class MyFileDropTarget(wx.FileDropTarget):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, window):
        """Constructor"""
        wx.FileDropTarget.__init__(self)
        self.window = window
 
    #----------------------------------------------------------------------
    def OnDropFiles(self, x, y, filenames):
        """
        When files are dropped, update the display
        """
        self.window.updateDisplay(filenames)
        print(list(filenames))
 
########################################################################
class FileInfo(object):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, path, date_created, date_modified, size):
        """Constructor"""
        self.name = os.path.basename(path)
        self.path = path
        self.date_created = date_created
        self.date_modified = date_modified
        self.size = size
########################################################################
class MainPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.file_list = []
 
        file_drop_target = MyFileDropTarget(self)
        self.olv = ObjectListView(self, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.olv.SetDropTarget(file_drop_target)
        self.setFiles()
        print(self.file_list)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.olv, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        updateBtn = wx.Button(self, wx.ID_ANY, "Execute Treatment Process")
        updateBtn.Bind(wx.EVT_BUTTON, self.treatBtnEvnt)
        
        dropBtn = wx.Button(self, wx.ID_ANY, "Drop Database")
        dropBtn.Bind(wx.EVT_BUTTON, self.dropDbEvnt)
        
        # Create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)        
 
        mainSizer.Add(self.olv, 1, wx.ALL|wx.EXPAND, 5)
        mainSizer.Add(updateBtn, 0, wx.ALL|wx.CENTER, 5)
        mainSizer.Add(dropBtn, 0, wx.ALL|wx.RIGHT, 5)
        self.SetSizer(mainSizer)
 
    #----------------------------------------------------------------------
    def updateDisplay(self, file_list):
        """"""
        for path in file_list:
            file_stats = os.stat(path)
            creation_time = time.strftime("%m/%d/%Y %I:%M %p",
                                          time.localtime(file_stats[stat.ST_CTIME]))
            modified_time = time.strftime("%m/%d/%Y %I:%M %p",
                                          time.localtime(file_stats[stat.ST_MTIME]))
            file_size = file_stats[stat.ST_SIZE]
            if file_size > 1024:
                file_size = file_size / 1024.0
                file_size = "%.2f KB" % file_size
            self.file_list.append(FileInfo(path,
                                           creation_time,
                                           modified_time,
                                           file_size))
 
        self.olv.SetObjects(self.file_list)
        
        
 
    #----------------------------------------------------------------------
    def setFiles(self):
        """"""
        self.olv.SetColumns([
            ColumnDefn("Name", "left", 220, "name"),
            ColumnDefn("Date created", "left", 150, "date_created"),
            ColumnDefn("Date modified", "left", 150, "date_modified"),
            ColumnDefn("Size", "left", 100, "size"),
            ColumnDefn("Add to Database", "left", 200, "size")
            ])
        self.olv.SetObjects(self.file_list)
    
    #----------------------------------------------------------------------   
    def dropDbEvnt(self, event):
        """"""
        rowObj = self.olv.GetSelectedObjects()
        b = bkend.back()
        b.dropDatabase(rowObj)
        
    #----------------------------------------------------------------------   
    def treatBtnEvnt(self, event):
        """"""
        rowObj = self.olv.GetSelectedObjects()
        b = bkend.back()
        b.addToDatabase(rowObj)
 
########################################################################
class MainFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="MAS", size=(800,600))
        panel = MainPanel(self)
        self.Show()
 
#----------------------------------------------------------------------
def call_inteface():
    """"""
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()

