import wx
import wx.lib.scrolledpanel
import socket, sys

class GUI(wx.Frame):
    
    def __init__(self,parent,id,title,port,host):
        #First retrieve the screen size of the device
        screenSize = wx.DisplaySize()
        screenWidth = screenSize[0]
        screenHeight = screenSize[1]
        ################################
        #port = 8787
        #host = "127.0.0.1"

        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.bind(('', 0))
        client.sendto('request', (host, port))

        daytime, server = client.recvfrom(1024)

        print daytime
        #################################
        #Create a frame
        wx.Frame.__init__(self,parent,id,title,size=screenSize, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        panel1 = wx.Panel(self,size=(screenWidth,120), pos=(0,0), style=wx.SIMPLE_BORDER)
        panel1.SetBackgroundColour('#FDDF99')
        panel2 = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(screenWidth,screenHeight-150), pos=(0,120), style=wx.SIMPLE_BORDER)
        panel2.SetupScrolling()
        panel2.SetBackgroundColour('#FFFFFF')
        self.button = wx.Button(panel1, label="Crawl")
        self.lblname = wx.StaticText(panel1, label="URL:")
        self.editname = wx.TextCtrl(panel1, size=(350, -1))
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        bSizer1.Add( self.button, 0, wx.ALL, 5 )
        bSizer1.Add( self.lblname, 0, wx.ALL, 5 )
        bSizer1.Add( self.editname, 0, wx.ALL, 5 )
        panel1.SetSizer( bSizer1)
        self.button.Bind(wx.EVT_BUTTON, self.OnButton)
        x=10
        y=10
        i=0 
       
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        for i in range(50):
            lb1="f"+str(i)
            lb2="l"+str(i)
            lb3="t"+str(i)
            lb1=wx.StaticText(panel2 ,5, "mahendra "+str(i),pos= (x,y))
            lb2=wx.StaticText(panel2 ,5, "hiii", pos=(x+600,y))
            lb3=wx.StaticText(panel2 ,5, "10:20", pos=(x+1200,y))
            y=y+20
            bSizer2.Add( lb1, 1, wx.ALL|wx.EXPAND, 5 )
            bSizer2.Add( lb2, 1, wx.ALL|wx.EXPAND, 5 )
            bSizer2.Add( lb3, 1, wx.ALL|wx.EXPAND, 5 )
            panel2.SetSizer( bSizer2 )
            i= i+1

        
    def OnButton(self, e):
        print(self.editname.GetValue()) 

    #def print_sim(c_From,c_link, c_time):
        

if __name__=='__main__':
   port=int(sys.argv[1])
   host=sys.argv[2]
   app = wx.App()
   frame = GUI(parent=None, id=-1, title="WebCrawler Sim",port=port,host=host)
   frame.Show()
   app.MainLoop()
   print("hii can I reach here..?")