#Program to populate table i.e. grid
from random import randrange
import wx
import wx.lib.scrolledpanel
import os
import sys
import subprocess

from general import *

import time
import threading
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

#from webmain import *
 
 
class MyForm(wx.Frame):
 
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "List Control Tutorial")
        pub.subscribe(self.OnNewLabels, "NEW_LABELS")
 
        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        self.index = 0
 
        self.list_ctrl = wx.ListCtrl(panel, size=(-1,750),
                         style=wx.LC_REPORT
                         |wx.BORDER_SUNKEN
                         )
        self.list_ctrl.InsertColumn(0, 'parent url', width=560)
        self.list_ctrl.InsertColumn(1, 'linked url', width=560)
        self.list_ctrl.InsertColumn(2, 'time', width=165)
        self.list_ctrl.SetBackgroundColour((204,255,255))
 
        #btn = wx.Button(panel, label="Add Line")
        #btn2 = wx.Button(panel, label="Get Data")
        btn3 = wx.Button(panel, label="Crawl")
        btn3.SetBackgroundColour((0,204,204))
        #btn.Bind(wx.EVT_BUTTON, self.add_line)
        #btn2.Bind(wx.EVT_BUTTON, self.get_data)
        btn3.Bind(wx.EVT_BUTTON, self.refresh_data)

        #############################################
        #self.button = wx.Button(panel1, label="Crawl")
        self.lblname = wx.StaticText(panel, label="URL:")
        self.editname = wx.TextCtrl(panel, size=(600, -1))
        bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
        bSizer1.AddStretchSpacer(250) 
        bSizer1.Add( self.lblname, 0, wx.ALIGN_RIGHT, 20)
        bSizer1.Add( self.editname, 0, wx.ALIGN_RIGHT, 20)
        bSizer1.Add( btn3, 0, wx.ALIGN_RIGHT, 20)
        #panel.SetSizer(bSizer1)
        #############################################
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(bSizer1, 0, wx.ALL|wx.CENTER, 5)
        sizer.Add(self.list_ctrl, 0, wx.ALL|wx.EXPAND, 5)
        
        #sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
        #sizer.Add(btn2, 0, wx.ALL|wx.CENTER, 5)
        #sizer.Add(btn3, 0, wx.ALL|wx.CENTER, 5)
        panel.SetSizer(sizer)

    def OnNewLabels(self, label1,label2,label3):
        len1=len(label1)
        len2=len(label2)
        len3=len(label3)
        if (len1>len2):
            len1=len2
        if (len1>len3):
            len1=len3 

        
        for i in range(len1):
            self.list_ctrl.InsertStringItem(self.index, label1[i])
            print(label1[i])
            self.list_ctrl.SetStringItem(self.index, 1, label2[i])
            print(label2[i])
            self.list_ctrl.SetStringItem(self.index, 2, label3[i])
            print(label3[i])
            self.index +=1
 
    def add_line(self, event):
        line = "Line %s" % self.index
        self.list_ctrl.InsertStringItem(self.index, line)
        self.list_ctrl.SetStringItem(self.index, 1, "01/19/2010")
        self.list_ctrl.SetStringItem(self.index, 2, "USA")
        self.index += 1
 
    def get_data(self, event):
        count = self.list_ctrl.GetItemCount()
        cols = self.list_ctrl.GetColumnCount()
        for row in range(count):
            for col in range(cols):
                item = self.list_ctrl.GetItem(itemId=row, col=col)
                print(item.GetText())
    ######################################
    def refresh_data(self, event):
        os.system("pkill -f main.py")
        while(self.index!=0):
            self.list_ctrl.DeleteItem(self.index-1)
            self.index -=1
        crawl_thread = threading.Thread(target = StartCrawlThread, args = ()) 
        crawl_thread.start()
        print(self.editname.GetValue())

        try:
            fifourlpath = "my_baseurl.fifo"
            #os.mkfifo(fifourlpath)
            fifourl = open(fifourlpath, "w")

            fifourl.write(self.editname.GetValue())
            fifourl.close()

        except Exception as e:
            print("OS fifo error ..")
        ########
        
        #subprocess.Popen("main.py", shell=True)
        #############




        print("before system call..")

        #os.system('python main.py')

        print("before system call..")

        time.sleep(5)



        

###############################
#
#

def StartCrawlThread():
    os.system("python main.py")

def InterfaceThread():

    #time.sleep(20)

    while True:
        # get the info from the server
        mylist1=[]
        mylist2=[]
        mylist3=[]
        #i = randrange(10)
        #for k in range(1,i+1):
        #   mylist.append(randrange(10))
        try:
            path = "my_result.fifo"
            fifo = open(path, "r")
            for line in fifo:
               if line=="":
                   break
               print "Received: " + line+"\n"
               word=line.split()
               if(len(word)>=3):
                   mylist1.append(word[0])
                   mylist2.append(word[1])
                   mylist3.append(word[2])

            fifo.close()

        except Exception as e:
            print("OS fifo error ..")

        # Tell the GUI about them
        wx.CallAfter(pub.sendMessage, "NEW_LABELS", label1= mylist1, label2= mylist2, label3= mylist3)
        print("coming here..")
        time.sleep(0.5)

#################################
class ServerInterface():

    def __init__(self):
        interface_thread = threading.Thread(target = InterfaceThread, args = ()) 
        interface_thread.start()
        
        


# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    create_fifo()
    crawl_thread = threading.Thread(target = StartCrawlThread, args = ()) 
    crawl_thread.start()
    frame = MyForm()

    frame.Show()
    server_interface = ServerInterface()
    app.MainLoop()