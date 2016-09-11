from slideshow_program import SlideshowProgram
import time
import wx
from wx.lib.pubsub import Publisher

def handle_load_song_msg(msg):
    print("%s: load_song msg recieved w/ data: %s" % (time.ctime(),msg.data))
    
def handle_load_img_msg(msg):
    print("%s: load_img msg recieved w/ data: %s" % (time.ctime(),msg.data))

Publisher().subscribe(handle_load_img_msg, ("load_img"))
Publisher().subscribe(handle_load_song_msg, ("load_song"))

program = SlideshowProgram(["./test"], default_slide_time_ms = 500)
app = wx.App()
program.start(app)
app.MainLoop()
