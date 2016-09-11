import wx
import wx.media
from pubsub import pub
from slideshow_frame import SlideshowFrame
import platform

def figure_mediabackend():
    platsys = platform.system()
    if platsys == "Windows":
        return wx.media.MEDIABACKEND_WMP10
    elif platsys == "Linux":
        return wx.media.MEDIABACKEND_GSTREAMER
    elif platsys == "Darwin": # Mac OS X
        return wx.media.MEDIABACKEND_QUICKTIME
    else:
        raise RuntimeError("Could not figure media backend. Platform %s is not supported" % platsys)
        
class SlideshowApp(wx.App):
    def __init__(self, program, auto_start=True):
        wx.App.__init__(self)        

        self.program = program
        self.mediabackend = figure_mediabackend()
        self.auto_start = auto_start
        
        print("Using %s for media backend" % self.mediabackend)
        
        pub.subscribe(self.__handle_load_img_msg, "load_img")
        pub.subscribe(self.__handle_load_song_msg, "load_song")
        pub.subscribe(self.__handle_close_msg, "close")

        W,H = wx.Display(0).GetGeometry().GetSize()
        size = (W,H)
        pos = (0,0)
        self.frame = SlideshowFrame(
            pos=pos,
            size=size,
            parent=None, 
            title='Slideshow')
        self.mediaCtrl = wx.media.MediaCtrl(self.frame, 
                                            style=wx.TRANSPARENT_WINDOW,
                                            szBackend=self.mediabackend)        
        self.Bind(event=wx.media.EVT_MEDIA_LOADED, handler=self.__handle_media_loaded_evt)        
        
        self.frame.ShowFullScreen(True)
        if self.auto_start:
            self.program.start()        

    def __handle_close_msg(self):
        self.frame.Close()
        
    def __handle_load_img_msg(self,data):
        self.frame.load_img(data)

    def __handle_load_song_msg(self,data):
        self.load_song(data)
        
    def load_song(self, song_path):
        if self.mediaCtrl.GetState() == wx.media.MEDIASTATE_PLAYING:
            self.mediaCtrl.Stop()
        
        loaded = self.mediaCtrl.Load(song_path)
        if not loaded:
            print("Could not load song file %s" % song_path)
      
    def __handle_media_loaded_evt(self,event):
        self.mediaCtrl.Play()

