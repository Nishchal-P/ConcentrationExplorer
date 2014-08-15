import wx
from data_tier import DAUserGone_SQLite
import winsound


class ScrollbarFrame(wx.Frame):
    reden_antwoord = ""
    radioListReden = []
    def __init__(self,title,interval_user_gone,from_datetime, to_datetime,options_reden):
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)

        wx.Frame.__init__(self, None, -1, title, size=(300, 300))
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        self.options_reden = options_reden
        self.radioListReden = []
        for reden in options_reden :
            self.radioListReden.append(reden[1])

        self.reden_antwoord = self.radioListReden[0]
        #panel.scroll = wx.ScrolledWindow(panel, -1)
        #panel.scroll.SetScrollbars(1, 1, 500, 400)

      # Reden

        #rbReden = wx.RadioBox(panel, label="Je was weg voor " + str(interval_user_gone) + " seconden. Waarom?", pos=(20, 120), choices=self.radioListReden,  majorDimension=5, style=wx.RA_VERTICAL)
        rbReden = wx.RadioBox(panel, label="You were gone for " + str(interval_user_gone) + " seconden. What was the reason?", pos=(20, 120), choices=self.radioListReden,  majorDimension=len(self.radioListReden), style=wx.RA_VERTICAL)
        rbReden.Bind(wx.EVT_RADIOBOX, self.EvtRadioBoxReden, rbReden)
        box.Add(rbReden,0,wx.ALL,10)

        text_other = wx.TextCtrl(panel, -1, '',  style=wx.TE_RIGHT)
        box.Add(text_other,0,wx.ALL,10)


        # A button
        button =wx.Button(panel, wx.ID_CLOSE,"Save")
        button.Bind(wx.EVT_BUTTON, lambda event : self.OnClick(event,rbReden,from_datetime, to_datetime,text_other),button)
        box.Add(button,0,wx.ALL,10)


        panel.SetSizer(box)
        panel.Layout()


    def EvtRadioBoxReden(self, event):
        index = event.GetInt()
        self.reden_antwoord = self.radioListReden[index]

    def OnClick(self,event,rbReden,datetime_from, datetime_to,text_other):
        reden = []

        for item in self.options_reden :
            print reden
            print item[1]
            print self.reden_antwoord
            print '---'
            if item[1]==self.reden_antwoord:
                reden = item

        if (reden[1]=='Other'):
            DAUserGone_SQLite.insert_row_user_gone(datetime_from,datetime_to,reden[0],text_other.GetValue(),reden[2])
        else:
            DAUserGone_SQLite.insert_row_user_gone(datetime_from,datetime_to,reden[0],'',reden[2])

        self.Close(True)


def call_form(options_reden,interval_user_gone,from_datetime, to_datetime) :
    app = wx.PySimpleApp()
    frame = ScrollbarFrame('You were gone',interval_user_gone,from_datetime, to_datetime,options_reden)
    frame.Show()
    app.MainLoop()
