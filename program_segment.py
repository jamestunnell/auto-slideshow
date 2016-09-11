import glob
import os
import eyed3

class ProgramSegment:
    def __init__(self,folder):
        self.folder = folder        
        print("Looking for images and songs in %s:" % folder)
        
        jpgs = glob.glob(os.path.join(folder,"*.jpg"))
        pngs = glob.glob(os.path.join(folder,"*.png"))
        bmps = glob.glob(os.path.join(folder,"*.bmp"))
        bmps = glob.glob(os.path.join(folder,"*.gif"))
        self.images = jpgs + pngs + bmps
        
        song_formats = ["mp3"]#"m4a","mp3","flv","ogg","wav"]
        self.songs = []
        self.song_durations = {}
        for song_format in song_formats:
            files = glob.glob(os.path.join(folder,"*.%s" % song_format))
            for f in files:
                audiofile = eyed3.load(f)
                self.song_durations[f] = audiofile.info.time_secs
            self.songs += files
        
        # sort songs and images
        self.songs = sorted(self.songs)
        self.images = sorted(self.images)
        
        print("found image files: %s" % [ os.path.basename(i) for i in self.images])    
        print("found song files: %s" % [ os.path.basename(s) for s in self.songs])

        if len(self.images) == 0:
            raise RuntimeError("Ach! No images found in %s, so this \
            is an invalid slideshow program segment." % folder)
            
        self.img_idx = 0
        self.song_idx = 0

    def folder(self):
        return self.folder
            
    def song_durations(self):
        return self.song_durations
        
    def duration_sec(self):
        return sum(self.song_durations.values())
        
    def images(self):
        return self.images
        
    def songs(self):
        return self.songs
        
    def has_next_img(self):
        return self.img_idx < len(self.images)

    def has_next_song(self):
        return self.song_idx < len(self.songs)
        
    def next_img(self):
        if self.img_idx >= len(self.images):
            return None
        else:
            img = self.images[self.img_idx]
            self.img_idx += 1
            return img
        
    def next_song(self):
        if self.song_idx >= len(self.songs):
            return None
        else:
            song = self.songs[self.song_idx]
            self.song_idx += 1
            return song
