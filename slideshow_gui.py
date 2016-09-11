#!/usr/bin/python

import wx
import os

class RowPanel(wx.Panel):
    def __init__(self, parent, controls):
        wx.Panel.__init__( self, parent=parent, id=-1 )
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        for control in controls:
            sizer.Add(control)
        self.SetSizer(sizer)
        self.Layout()
        
#class SlideshowLauncherPanel(wx.Panel):
#    def __init__( self, parent):
#        wx.Panel.__init__( self, parent=parent, id=-1 )
#
#        self.root_dir_txtbox = wx.TextCtrl(self, size=(300,30))
#        self.browse_btn = wx.Button(self, label="Browse", size=(100,30))
#        self.auto_restart_chkbox = wx.CheckBox(self, label="Auto Restart")
#        self.launch_btn = wx.Button(self, label="Launch", size=(100,30))
#        
#        panel_vertSizer = wx.BoxSizer( wx.VERTICAL )
#        panel_vertSizer.Add(self.root_dir_txtbox, proportion=0, flag=wx.CENTER)
#        panel_vertSizer.Add(self.browse_btn, proportion=0, flag=wx.CENTER)
#        panel_vertSizer.Add(self.auto_restart_chkbox, proportion=0, flag=wx.CENTER)
#        panel_vertSizer.Add(self.launch_btn, proportion=0, flag=wx.CENTER)
#
#        self.SetSizer(panel_vertSizer)
#        self.Fit()        # Make "self" (the panel) shrink to the minimum size required by the controls.
#
#    def GetAutoRestartCheckBox(self):
#        return self.auto_restart_chkbox
#
#    def GetRootDirTextCtrl(self):
#        return self.root_dir_txtbox
#                    
#    def GetBrowseButton(self):
#        return self.browse_btn
#
#    def GetLaunchButton(self):
#        return self.launch_btn
        
class SlideshowLauncherFrame(wx.Frame):
    def __init__(self,**kwargs):
        wx.Frame.__init__ ( self, **kwargs)
        #sacrificial_frmCtrl = wx.Panel( self ).Hide()
   
        self.mainPanel = wx.Panel(self)

        # 1st row
        self.root_dir_txtbox = wx.TextCtrl(self.mainPanel, size=(300,30))
        self.browse_btn = wx.Button(self.mainPanel, label="Browse", size=(100,30))
        
        # 2nd row
        self.auto_restart_chkbox = wx.CheckBox(self.mainPanel, label="Auto Restart")
        self.launch_btn = wx.Button(self.mainPanel, label="Launch", size=(100,30))
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        row1 = wx.BoxSizer(wx.HORIZONTAL)        
        row1.Add((20,-1))  # spacer
        row1.Add(self.root_dir_txtbox, 0, wx.ALL|wx.ALIGN_RIGHT, 5)
        row1.Add(self.browse_btn, 0, wx.ALL|wx.ALIGN_LEFT, 5)

        row2 = wx.BoxSizer(wx.HORIZONTAL)        
        row2.Add((20,-1))  # spacer
        row2.Add(self.auto_restart_chkbox, 0, wx.ALL|wx.ALIGN_RIGHT, 5)
        row2.Add(self.launch_btn, 0, wx.ALL|wx.ALIGN_LEFT, 5)
        
        mainSizer.Add(row1)
        mainSizer.Add(row2)
        
        self.mainPanel.SetSizer(mainSizer)
        mainSizer.Fit(self)   # self.Fit()  # always use one or the other
        
        self.Bind(wx.EVT_BUTTON, self.OnLaunch, self.launch_btn)
        self.Bind(wx.EVT_BUTTON, self.OnBrowse, self.browse_btn)

    def OnBrowse(self, event):
        dialog = wx.DirDialog(self,message="Select a slideshow root directory")
        if dialog.ShowModal() == wx.ID_OK:
            self.root_dir_txtbox.SetValue(dialog.GetPath())
        dialog.Destroy()
        
    def OnLaunch(self, event):
        auto_restart = self.auto_restart_chkbox.GetValue()
        root_dir = self.root_dir_txtbox.GetValue()
        
        self.launch_btn.Disable()
        
        cli_path = os.path.join(os.path.dirname(__file__),"slideshow_cli.py")
        command_line = "python " + cli_path + " --root_dir " + root_dir
        if auto_restart:
            command_line += " --auto_restart"
        os.system(command_line)
        
        self.launch_btn.Enable()

class SlideshowLauncherApp(wx.App):
    def OnInit(self):
        self.frame = SlideshowLauncherFrame(parent=None, id=-1, title="Slideshow Launcher")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True
        
if __name__ == '__main__':
    app = SlideshowLauncherApp()
    app.MainLoop()
