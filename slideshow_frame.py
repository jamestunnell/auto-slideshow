import wx

class SlideshowFrame(wx.Frame):
    def __init__(self,**kwargs):
        wx.Frame.__init__(self, **kwargs)
        self.SetBackgroundColour(wx.BLACK)

        self.panel = wx.Panel(self, pos=self.Rect.GetPosition(), size=self.Rect.GetSize())
        self.empty_img = wx.EmptyImage(self.Rect.GetWidth(),
                                       self.Rect.GetHeight())
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.BitmapFromImage(self.empty_img))
        #self.verSizer = wx.BoxSizer(wx.VERTICAL)
        #self.horSizer = wx.BoxSizer(wx.HORIZONTAL)
        #self.mainSizer.Add(self.imageCtrl, 0, wx.ALL|wx.ALIGN_CENTER, 0)
        #self.panel.SetSizer(self.mainSizer)
        #self.mainSizer.Fit(self)
        #self.panel.Layout()
    
    def load_img(self, img_path):
        if img_path is None:
            img = self.empty_img
        else:
            img = wx.Image(img_path, wx.BITMAP_TYPE_ANY)
        
        #
        # scale the image, preserving the aspect ratio
        #
        
        w = img.GetWidth()
        h = img.GetHeight()
        
        W = self.Rect.GetWidth()
        H = self.Rect.GetHeight()
        
        # scale w to match W, and see if height is over/under H. If so, scale
        # h to match H instead.
        w2, h2 = W, h*(float(W)/w)
        if h2 > H:
            w2, h2 = w*(float(H)/h), H

        img = img.Scale(w2,h2,quality=wx.IMAGE_QUALITY_HIGH)
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        #self.panel.Layout()
        
        O = self.Rect.GetPosition() # frame origin
        X,Y = (O[0] + (W-w2)/2, O[1] + (H-h2)/2)
        self.panel.SetRect((X,Y,w2,h2))
        #self.mainSizer.Fit(self)
        #self.panel.Layout()
        self.panel.Refresh()
