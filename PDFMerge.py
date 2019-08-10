#-*- coding: utf-8 -*-
import wx
import win32api
import sys, os
import logging

from FileListTable import *
from APDFTool import APDFTool

APP_TITLE = u'PDF Document Merge Tool'
APP_ICON = 'pdf_maker.ico'

class MyLogHandler(logging.Handler):
    def __init__(self,obj):
        logging.Handler.__init__(self);
        self.Object = obj;

    def emit(self,record):
        if record.levelno<self.level: return;
        tstr = time.strftime('%Y-%m-%d_%H:%M:%S.%U');
        self.Object.AppendText("[%s][%s] %s\\n"%(tstr,record.levelname,record.getMessage()));

class mainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, APP_TITLE, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        # 默认style是下列项的组合：wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN 
        
        self.SetBackgroundColour(wx.Colour(224,224,224))
        self.SetSize((800, 600))
        self.Center()

        if hasattr(sys, "frozen") and getattr(sys, "frozen"):
            exeName = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
            icon = wx.Icon(exeName, wx.BITMAP_TYPE_ICO)
        else:
            icon = wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        
        # left
        panelLeft = wx.BoxSizer(wx.VERTICAL)
        
        gridDatas = []

        self.gridTable = wx.grid.Grid(self, -1, pos=(5,5), size=(400, 400), style=wx.WANTS_CHARS)
        
        self.infoTable = FileListGridTable(gridDatas)
        self.gridTable.SetTable(self.infoTable, True)

        self.gauge = wx.Gauge(self, range = 20, size = (250, 25), style = wx.GA_HORIZONTAL)
        panelLeft.Add(self.gridTable, 0, wx.EXPAND|wx.ALL, 5)
        panelLeft.Add(self.gauge, 0, wx.EXPAND|wx.ALL, 5)

        # right
        panelRight = wx.BoxSizer(wx.VERTICAL)

        btnOpenFiles = wx.Button(self, -1, u'Open', size=(50, 50))
        btnOpenFiles.Bind(wx.EVT_BUTTON, self.OpenFiles)
        btnMoveUp = wx.Button(self, -1, u'↑', size=(50, 50))
        btnMoveUp.Bind(wx.EVT_BUTTON, self.MoveUp)
        btnMoveDown = wx.Button(self, -1, u'↓', size=(50, 50))
        btnMoveDown.Bind(wx.EVT_BUTTON, self.MoveDown)
        btnMerge = wx.Button(self, -1, u'Merge', size=(50,50))
        btnMerge.Bind(wx.EVT_BUTTON, self.MergePDFFiles)
        btnClear = wx.Button(self, -1, u'Clear', size=(50,50))
        btnClear.Bind(wx.EVT_BUTTON, self.ClearFiles)
        panelRight.Add(btnOpenFiles, 0, wx.ALL, 10)  
        panelRight.Add(btnMoveUp, 0, wx.ALL, 10)  
        panelRight.Add(btnMoveDown, 0, wx.ALL, 10)  
        panelRight.Add(btnMerge, 0, wx.ALL, 10)
        panelRight.Add(btnClear, 0, wx.ALL, 10)


        mainBox = wx.BoxSizer(wx.HORIZONTAL)
        mainBox.Add(panelLeft, 1, wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, 5)     
        mainBox.Add(panelRight, 0, wx.EXPAND|wx.ALL, 20)          
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_SIZE, self.OnResize)     
        
        self.SetAutoLayout(True)
        self.SetSizer(mainBox)
        self.Layout()
          
        logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def MoveUp(self, evt):
        selectedRows = self.gridTable.GetSelectedRows()      
        self.logger.info(selectedRows)  
        for row in selectedRows:
            self.logger.info(row)
            self.infoTable.RowMoveUp(row)

    def MoveDown(self, evt):
        selectedRows = self.gridTable.GetSelectedRows()      
        self.logger.info(selectedRows)  
        for row in selectedRows:
            self.logger.info(row)
            self.infoTable.RowMoveDown(row)

    def ClearFiles(self, evt):
        self.infoTable.ClearRows()

    def MergePDFFiles(self, evt):
        def SetUageValue(value):
            self.gauge.SetValue(value)

        rowsCount = self.infoTable.GetNumberRows()
        files = []
        for i in range(rowsCount):
             files.append(self.infoTable.GetValue(i, 1))
        if len(files):
            tool = APDFTool(files)
            pageCount = tool.getTotalPageCount()
            self.gauge.SetRange(pageCount)
            tool.merge("output", SetUageValue)

    def OpenFiles(self, evt):
        '''
        temporary 
        '''
        file_wildcard = "PDF files(*.pdf)|*.pdf" 
        dlg = wx.FileDialog(self, "Choose PDF files to merge...",
                            os.getcwd(), 
                            style = wx.FD_OPEN|wx.FD_MULTIPLE,
                            wildcard = file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            for path in paths:
                files = []
                files.append(path)
                tool = APDFTool(files)
                count = tool.getTotalPageCount()
                self.infoTable.AppendRows([os.path.basename(path), path, count])
            
        dlg.Destroy()
    
    def OnResize(self, evt): 
        self.Refresh()
        evt.Skip() 
        
    def OnClose(self, evt):
        self.Destroy()

class mainApp(wx.App):
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.Frame = mainFrame()
        self.Frame.Show()
        return True

if __name__ == "__main__":
    app = mainApp(redirect=True, filename="debug.log")
    app.MainLoop()