from random import randrange
import wx
import wx.lib.scrolledpanel
import os
import sys

import time
import threading
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

######Good for updating panel ##################

class GUI(wx.Frame):

    def __init__(self, parent, id, title):
        screenWidth = 800
        screenHeight = 450
        screenSize = (screenWidth, screenHeight)
        wx.Frame.__init__(self, None, id, title, size=screenSize)
        self.locationFont = locationFont = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = panel = wx.lib.scrolledpanel.ScrolledPanel(self, -1, style=wx.SIMPLE_BORDER)
        panel.SetupScrolling()
        panel.SetBackgroundColour('#FFFFFF')
        panel.SetSizer(sizer)
        mainSizer.Add(panel, 10, wx.EXPAND|wx.ALL)
        self.SetSizer(mainSizer)

        self.text_labels = []  # Stores the labels where server data is displayed

        pub.subscribe(self.OnNewLabels, "NEW_LABELS")


    def OnNewLabels(self, labels):
        locations = labels
        print locations
        if len(self.text_labels) < len(labels):
            new_labels_needed = len(labels) - len(self.text_labels) 
            label = "(no data)"
            for i in range(new_labels_needed):
                sPanels = wx.Panel(self.panel)
                text = wx.StaticText(sPanels, -1, label)
                text.SetFont(self.locationFont)
                text.SetForegroundColour('#0101DF')
                self.sizer.Add(sPanels, 0, wx.ALL, 5)
                self.sizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 0)
                self.text_labels.append(text)
            self.sizer.Layout()            
        k = 0
        for label in locations:
            self.text_labels[k].SetLabel(str(label))
            k=k+1


###############################
#
#

def InterfaceThread():
    while True:
        # get the info from the server
        mylist =[]
        #i = randrange(10)
        #for k in range(1,i+1):
        #   mylist.append(randrange(10))
        path = "my_program.fifo"
        fifo = open(path, "r")
        for line in fifo:
           print "Received: " + line+"\n"
           mylist.append(line)

        fifo.close()

        # Tell the GUI about them
        wx.CallAfter(pub.sendMessage, "NEW_LABELS", labels = mylist)
        time.sleep(0.5)


class ServerInterface():

    def __init__(self):
        interface_thread = threading.Thread(target = InterfaceThread, args = ()) 
        interface_thread.start()



#############
#

if __name__=='__main__':
    app = wx.App()
    frame = GUI(parent=None, id=-1, title="Test")
    frame.Show()
    server_interface = ServerInterface()
    app.MainLoop()
