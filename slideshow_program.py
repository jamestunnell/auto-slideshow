from program_segment import ProgramSegment
from pubsub import pub
import wx
import time
import os.path

class SlideshowProgram():
    def __init__(self, root_dir, auto_restart=True, slide_time_ms=3000):
        
        self.root_dir = root_dir
        self.segments = []
        for root, dirs, files in os.walk(root_dir):
            try:
                self.segments.append(ProgramSegment(root))
                print("segment found at %s" % root)
            except:
                print("not a valid segment folder: %s" % root)
        
        if len(self.segments) == 0:
            raise RuntimeError("No folders containing files were found in \
            root dir %s. It's an outrage (and an error)." % root_dir)
        
        self.segments = sorted(self.segments, key = lambda x: x.folder)
        self.segment_idx = 0
        self.timers = { "img": None, "song": None, "segment": None }
        self.current_segment = None
        
        self.auto_restart = auto_restart
        self.slide_time_ms = slide_time_ms
    
    def __handle_img_timer_evt(self,event):
        self.change_img()

    def __handle_song_timer_evt(self,event):
        print("%s: recieved song timer event" % time.ctime())
        self.change_song()

    def __handle_segment_timer_evt(self,event):
        self.change_segment()
            
    def has_next_segment(self):
        return self.segment_idx < len(self.segments)
    
    def next_segment(self):
        if self.segment_idx < len(self.segments):
            i = self.segment_idx
            self.segment_idx += 1
            return self.segments[i]
        else:
            return None
        
    def change_img(self):
        if self.current_segment.has_next_img():
           img = self.current_segment.next_img()
           pub.sendMessage("load_img",data=img)
        else:
           self.timers["img"].Stop()

    def change_song(self):
        if self.current_segment.has_next_song():
           song = self.current_segment.next_song()
           pub.sendMessage("load_song",data=song)
           # one-shot timer needs restarted with every song
           song_duration_ms = int(1000*self.current_segment.song_durations[song])
           print("%s: loading song %s, lasting %0.3f sec" %(time.ctime(),os.path.basename(song),song_duration_ms/1000.))
           self.timers["song"].Start(song_duration_ms,True)
        
    def change_segment(self):
        if self.has_next_segment():
            self.current_segment = self.next_segment()
            
            print("%s: starting segment in folder %s" % (time.ctime(),self.current_segment.folder))
            if len(self.current_segment.songs) > 0:
                total_time_ms = int(1000 * self.current_segment.duration_sec())
                slide_time_ms = int(total_time_ms / float(len(self.current_segment.images)))
            else:
                slide_time_ms = int(self.slide_time_ms)
                total_time_ms = int(slide_time_ms * len(self.current_segment.images))
            
            self.change_img()
            self.change_song()
            
            # do not start the song timer. It is a one-shot and 
            # will be started every time change_song is called.
            self.timers["img"].Start(slide_time_ms, False)
            self.timers["segment"].Start(total_time_ms,True)
        else:
            if self.auto_restart:
                print("%s: restarting show at first segment." % time.ctime())
                self.start()
            else:
                print("%s: no more segments left. Stopping show..." % time.ctime())
                self.stop()
                pub.sendMessage("close")
        
    def start(self):
        self.segment_idx = 0
    
        if self.timers["img"] is None:
            self.timers["img"] = wx.Timer(None)
            self.timers["img"].Bind(wx.EVT_TIMER, self.__handle_img_timer_evt)
        if self.timers["song"] is None:
            self.timers["song"] = wx.Timer(None)
            self.timers["song"].Bind(wx.EVT_TIMER, self.__handle_song_timer_evt)
        if self.timers["segment"] is None:
            self.timers["segment"] = wx.Timer(None)
            self.timers["segment"].Bind(wx.EVT_TIMER, self.__handle_segment_timer_evt)
        
        self.change_segment()

    def stop(self):
        for t in self.timers.values():
            t.Stop()
