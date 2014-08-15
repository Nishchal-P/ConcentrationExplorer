__author__ = 'Peter'
from logical_tier import Tracking_system


import wx
from presentation_tier import Output
import datetime


class ScrollbarFrame(wx.Frame):
    #options_reason = ['Ik nam notities', 'Ik zocht een document', 'Ik pauzeerde', 'Ik was afgeleid', 'andere:']
    options_reason = [['Notes','I was taking notes',1], ['Document','I was searching/reading a document',1], ['Break','I took a break',0], ['Distracted','I was distracted',0], ['Screen','I was looking to the screen',1],['Other','Other',0]]
    treshold_important_unimportant = 30

    def __init__(self,title):
        wx.Frame.__init__(self, None, -1, title, size=(380, 200))
        panel = wx.Panel(self)

        #Menu
        menubar = wx.MenuBar()
        options = wx.Menu()

        options.Append(1,'&Tracking')
        options.Append(2,'&Results')

        menubar.Append(options,'&Options')
        self.SetMenuBar(menubar)

        # arrays
        tracking_array = []
        result_array = []


        box = wx.BoxSizer(wx.VERTICAL)
        box_tracking = wx.BoxSizer(wx.VERTICAL)
        box_result = wx.BoxSizer(wx.VERTICAL)

        # Tracking
        #wx.StaticBox(panel, -1, 'Tracking', (5, 5), size=(280, 120))
        label_RescueTime_key = wx.StaticText(panel,-1,"Enter your RescueTime key:")
        box_tracking.Add(label_RescueTime_key,0,wx.ALL,10)
        tracking_array.append(label_RescueTime_key)

        text_RescueTime_key = wx.TextCtrl(panel, -1, '',  style=wx.TE_RIGHT)
        box_tracking.Add(text_RescueTime_key,0,wx.ALL,10)
        tracking_array.append(text_RescueTime_key)

        # A button
        button_tracking =wx.Button(panel, wx.ID_CLOSE,"Start tracking")
        button_tracking.Bind(wx.EVT_BUTTON, lambda event : self.evtStartTracking(event,text_RescueTime_key.GetValue()),button_tracking)
        box_tracking.Add(button_tracking,0,wx.ALL,10)
        tracking_array.append(button_tracking)

        # resultaat tonen

        label_title = wx.StaticText(panel,-1,"Enter the start and end datetime in the format 'yyyy-mm-dd HH:MM:SS'")
        box_result.Add(label_title,0,wx.ALL,10)

        result_array.append(label_title)
        box_from_to_date = wx.BoxSizer(wx.HORIZONTAL)

        text_date_from = wx.TextCtrl(panel, -1, '',  style=wx.TE_RIGHT)
        box_from_to_date.Add(text_date_from,0,wx.ALL,10)
        result_array.append(text_date_from)

        label_to = wx.StaticText(panel,-1,"to")
        box_from_to_date.Add(label_to,0,wx.ALL,10)
        result_array.append(label_to)

        text_date_to = wx.TextCtrl(panel, -1, '',  style=wx.TE_RIGHT)
        box_from_to_date.Add(text_date_to,0,wx.ALL,10)
        result_array.append(text_date_to)

        box_result.Add(box_from_to_date,0,wx.ALL,5)

        button_show_result =wx.Button(panel, wx.ID_CLOSE,"Show Result")
        button_show_result.Bind(wx.EVT_BUTTON, lambda event : self.evtShowResult(event,text_date_from.GetValue(),text_date_to.GetValue()),button_tracking)
        box_result.Add(button_show_result,0,wx.ALL,10)
        result_array.append(button_show_result)

        #box.Add(box_tracking,0,wx.ALL,10)
        #box.Add(box_result,0,wx.ALL,10)

        self.Bind(wx.EVT_MENU, lambda event : self.evtTracking(event,tracking_array,result_array,box_tracking,panel), id=1)
        self.Bind(wx.EVT_MENU, lambda event : self.evtResult(event,tracking_array,result_array,box_result,panel), id=2)

        self.buildTrackingForm(tracking_array,result_array,box_tracking,panel)

    def evtStartTracking(self,event,RescueTime_key):
        self.Close(True)
        Tracking_system.Tracking(RescueTime_key)


    def evtShowResult(self,event,strStart_datetime, strEnd_datetime):
        start_datetime =  datetime.datetime.strptime(strStart_datetime, "%Y-%m-%d %H:%M:%S")
        end_datetime = datetime.datetime.strptime(strEnd_datetime, "%Y-%m-%d %H:%M:%S")
        Output.show_results(start_datetime,end_datetime,self.options_reason,self.treshold_important_unimportant)
        Output.showgraph(start_datetime,end_datetime,self.options_reason)


    def evtTracking(self,event,tracking_array,result_array,box_tracking,panel):
        self.buildTrackingForm(tracking_array,result_array,box_tracking,panel)

    def evtResult(self,event,tracking_array, result_array,box_result,panel):
        for item in result_array :
            item.Show(True)

        for item in tracking_array :
            item.Show(False)

        panel.SetSizer(box_result)
        panel.Layout()

    def buildTrackingForm(self,tracking_array,result_array,box_tracking,panel):
        for item in result_array :
            item.Show(False)

        for item in tracking_array :
            item.Show(True)

        panel.SetSizer(box_tracking)
        panel.Layout()


def call_form() :
    app = wx.PySimpleApp()
    frame = ScrollbarFrame('Main')
    frame.Show()
    app.MainLoop()

call_form()