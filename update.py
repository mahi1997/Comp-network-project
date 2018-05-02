import wx
import time
class MyFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, size=(290,200))
        self.panel = wx.Panel(self, -1)
        wx.StaticText(self.panel, -1, "Hello World", (20,20))
        self.gauge = wx.Gauge(self.panel, -1, 50, pos=(20,50), size=(250, 20))
        self.Show()
        n = 0
        while n < 50:
            n = n+1
            self.gauge.SetValue(n)
            wx.Yield()
            time.sleep(1)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, -1)
        self.SetTopWindow(self.frame)
        return True

def run():
    app = MyApp()

run()
